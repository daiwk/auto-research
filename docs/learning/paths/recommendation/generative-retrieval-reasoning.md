---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 生成式召回与推理推荐

[搜广推](index.md) / 240 个问题 · 60 篇论文

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
<p class="ar-learning-status" data-learning-status role="status">240 个问题 · 60 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onelatent" data-paper-title="OneLatent: Latent Reasoning for Efficient Foundation Recommendation Models" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneLatent: Latent Reasoning for Efficient Foundation Recommendation Models 搜广推与 LLM 应用 Kuaishou Technology 2026-10-22 推荐FRM的显式CoT会增加生成时延，也可能过度思考或被固定推理模板带偏。OneLatent先用探索、评价、归因三视角生成自适应教师监督，再学习三个潜在token接口，最后只生成三层语义ID，避免在线输出长推理文本。 成本过高，不复现（审查 DONE），不下载235B教师、不做56卡训练的缩小替身、不自动重试因此本项是资料与成本审查完成，没有本地模型、诊断proxy、benchmark指标、GPU回执或evolve映射。Appendix A.1原配置为7节点×每节点8GPU，即56GPU、全参数BF16、4096tokens、两有效epochs；监督涉及Qwen3-235B-A22B教师及工业数据。单张A100/A30或Mac不适合照搬完整矩阵，本轮不先下载/试跑来验证它昂贵。  大模型能力与推荐融合 潜在推理与生成式推荐 搜广推 生成式召回与推理推荐 OneLatent 的三视角教师监督为什么是探索、评价和归因，而非固定一条长 CoT？ 不同视角提供候选发现、比较与解释线索，模型按样本可用视角学习潜在接口，减少固定模板可能带来的偏置与过度思考。它只减少在线显式文本输出，不能据此证明潜在 token 忠实保存每个推理步骤。全参数训练也共同影响结果。 示意：某样本只有可靠评价理由，另一样本还有探索与归因，不必给二者硬塞同一长度推理；内部表示学到多少仍需独立检查。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-onelatent-08691361" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7b09d92421cf94e0">OneLatent 的三视角教师监督为什么是探索、评价和归因，而非固定一条长 CoT？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonelatent">OneLatent: Latent Reasoning for Efficient Foundation Recommendation Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同视角提供候选发现、比较与解释线索，模型按样本可用视角学习潜在接口，减少固定模板可能带来的偏置与过度思考。它只减少在线显式文本输出，不能据此证明潜在 token 忠实保存每个推理步骤。全参数训练也共同影响结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某样本只有可靠评价理由，另一样本还有探索与归因，不必给二者硬塞同一长度推理；内部表示学到多少仍需独立检查。</p>
<p class="ar-learning-sources">依据：背景与主要改动、成本判断与本地边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30675v1">原论文</a> · <a href="../../../../recommendation-components/2610.30675-onelatent/">实现解读</a> · <a href="#qa-7b09d92421cf94e0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onelatent" data-paper-title="OneLatent: Latent Reasoning for Efficient Foundation Recommendation Models" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneLatent: Latent Reasoning for Efficient Foundation Recommendation Models 搜广推与 LLM 应用 Kuaishou Technology 2026-10-22 推荐FRM的显式CoT会增加生成时延，也可能过度思考或被固定推理模板带偏。OneLatent先用探索、评价、归因三视角生成自适应教师监督，再学习三个潜在token接口，最后只生成三层语义ID，避免在线输出长推理文本。 成本过高，不复现（审查 DONE），不下载235B教师、不做56卡训练的缩小替身、不自动重试因此本项是资料与成本审查完成，没有本地模型、诊断proxy、benchmark指标、GPU回执或evolve映射。Appendix A.1原配置为7节点×每节点8GPU，即56GPU、全参数BF16、4096tokens、两有效epochs；监督涉及Qwen3-235B-A22B教师及工业数据。单张A100/A30或Mac不适合照搬完整矩阵，本轮不先下载/试跑来验证它昂贵。  大模型能力与推荐融合 潜在推理与生成式推荐 搜广推 生成式召回与推理推荐 OneLatent 的潜在 token 为什么能省掉在线长推理，又不能被称为严格的推理信息瓶颈？ 训练用探索、评价、归因理由重建教学生通过潜在 token 组织推荐信息，随后只预测语义 ID，省去输出长理由的解码成本。但普通因果掩码仍允许输出读取原始画像和历史，且更新全部学生参数，所以效果不能归因于潜在 token 单独存储了全部推理。本地仅完成资料与成本审查，没有运行复现。 示意：训练时教模型用几个内部标记支持“为何适合这位用户”的回答，上线只输出物品编码。即使推荐更快，也不能据此断言这些标记完整保存了每一步推理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-edb5f88714252428">OneLatent 的潜在 token 为什么能省掉在线长推理，又不能被称为严格的推理信息瓶颈？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonelatent">OneLatent: Latent Reasoning for Efficient Foundation Recommendation Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>训练用探索、评价、归因理由重建教学生通过潜在 token 组织推荐信息，随后只预测语义 ID，省去输出长理由的解码成本。但普通因果掩码仍允许输出读取原始画像和历史，且更新全部学生参数，所以效果不能归因于潜在 token 单独存储了全部推理。本地仅完成资料与成本审查，没有运行复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练时教模型用几个内部标记支持“为何适合这位用户”的回答，上线只输出物品编码。即使推荐更快，也不能据此断言这些标记完整保存了每一步推理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、成本判断与本地边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30675v1">原论文</a> · <a href="../../../../recommendation-components/2610.30675-onelatent/">实现解读</a> · <a href="#qa-edb5f88714252428">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onelatent" data-paper-title="OneLatent: Latent Reasoning for Efficient Foundation Recommendation Models" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneLatent: Latent Reasoning for Efficient Foundation Recommendation Models 搜广推与 LLM 应用 Kuaishou Technology 2026-10-22 推荐FRM的显式CoT会增加生成时延，也可能过度思考或被固定推理模板带偏。OneLatent先用探索、评价、归因三视角生成自适应教师监督，再学习三个潜在token接口，最后只生成三层语义ID，避免在线输出长推理文本。 成本过高，不复现（审查 DONE），不下载235B教师、不做56卡训练的缩小替身、不自动重试因此本项是资料与成本审查完成，没有本地模型、诊断proxy、benchmark指标、GPU回执或evolve映射。Appendix A.1原配置为7节点×每节点8GPU，即56GPU、全参数BF16、4096tokens、两有效epochs；监督涉及Qwen3-235B-A22B教师及工业数据。单张A100/A30或Mac不适合照搬完整矩阵，本轮不先下载/试跑来验证它昂贵。  大模型能力与推荐融合 潜在推理与生成式推荐 搜广推 生成式召回与推理推荐 OneLatent 的潜在接口与额外 encoder/projector 的 latent MSE 蒸馏，为何不是同算法？ 来源用普通因果学生通过单、多视角理由重建再预测 SID，更新全部参数，没有额外投影器和严格 latent 瓶颈。向量 MSE 只对齐位置特征，不保留同样生成监督。任何小夹具若替换训练目标，只能作新诊断，本地未做这种替代复现。 示意：让学生从潜在标记重建理由与让两组向量欧氏距离接近，分别监督可生成内容和坐标；后者成功不证明前者能力。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ab91824a0488049a">OneLatent 的潜在接口与额外 encoder/projector 的 latent MSE 蒸馏，为何不是同算法？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonelatent">OneLatent: Latent Reasoning for Efficient Foundation Recommendation Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>来源用普通因果学生通过单、多视角理由重建再预测 SID，更新全部参数，没有额外投影器和严格 latent 瓶颈。向量 MSE 只对齐位置特征，不保留同样生成监督。任何小夹具若替换训练目标，只能作新诊断，本地未做这种替代复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>让学生从潜在标记重建理由与让两组向量欧氏距离接近，分别监督可生成内容和坐标；后者成功不证明前者能力。</p>
<p class="ar-learning-sources">依据：背景与主要改动、成本判断与本地边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30675v1">原论文</a> · <a href="../../../../recommendation-components/2610.30675-onelatent/">实现解读</a> · <a href="#qa-ab91824a0488049a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onelatent" data-paper-title="OneLatent: Latent Reasoning for Efficient Foundation Recommendation Models" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneLatent: Latent Reasoning for Efficient Foundation Recommendation Models 搜广推与 LLM 应用 Kuaishou Technology 2026-10-22 推荐FRM的显式CoT会增加生成时延，也可能过度思考或被固定推理模板带偏。OneLatent先用探索、评价、归因三视角生成自适应教师监督，再学习三个潜在token接口，最后只生成三层语义ID，避免在线输出长推理文本。 成本过高，不复现（审查 DONE），不下载235B教师、不做56卡训练的缩小替身、不自动重试因此本项是资料与成本审查完成，没有本地模型、诊断proxy、benchmark指标、GPU回执或evolve映射。Appendix A.1原配置为7节点×每节点8GPU，即56GPU、全参数BF16、4096tokens、两有效epochs；监督涉及Qwen3-235B-A22B教师及工业数据。单张A100/A30或Mac不适合照搬完整矩阵，本轮不先下载/试跑来验证它昂贵。  大模型能力与推荐融合 潜在推理与生成式推荐 搜广推 生成式召回与推理推荐 OneLatent 多视角重建为什么先按每条理由 token 数平均，再按可用视角平均？ 直接求和让长理由天然更重，视角数不同也会改变样本贡献。双层平均控制长度与缺失差异；教师可读正例构造理由，学生 prefix 却不能含目标 SID 或正例描述。服务异步缓存和大训练成本是另一边界，本地只有审查。 示意：一条二十词理由和一条二百词理由不应仅因长度十倍就支配学习；缺少归因视角时也不能用空文本当作真实第三项。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-5ab3166d1802984b">OneLatent 多视角重建为什么先按每条理由 token 数平均，再按可用视角平均？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonelatent">OneLatent: Latent Reasoning for Efficient Foundation Recommendation Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直接求和让长理由天然更重，视角数不同也会改变样本贡献。双层平均控制长度与缺失差异；教师可读正例构造理由，学生 prefix 却不能含目标 SID 或正例描述。服务异步缓存和大训练成本是另一边界，本地只有审查。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一条二十词理由和一条二百词理由不应仅因长度十倍就支配学习；缺少归因视角时也不能用空文本当作真实第三项。</p>
<p class="ar-learning-sources">依据：背景与主要改动、成本判断与本地边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30675v1">原论文</a> · <a href="../../../../recommendation-components/2610.30675-onelatent/">实现解读</a> · <a href="#qa-5ab3166d1802984b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:spar-prefix-balance" data-paper-title="SPAR: Stepwise Personalized Autoregressive Recommendation with Prefix-Balanced Semantic IDs" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="SPAR: Stepwise Personalized Autoregressive Recommendation with Prefix-Balanced Semantic IDs 搜广推与 LLM 应用 University of Electronic Science and Technology of China 2026-10-20 同一用户长历史中，有用证据随已生成SID前缀而变；热门前缀的交互负载还会压倒其他分支。SPAR由三部分组成：按前缀检索粗到细记忆的PATH、冻结残差码本后的RQ-PIB负载修复，以及SFT+DPO偏好对齐。本地只实现第二部分的修复子程序，不拿字典或K-means冒充整个推荐模型。 完整生产训练与A/B成本过高，不复现（审查 DONE）。已实现RQ-PIB的冻结码本修复阶段，仅L1机制诊断；已实现RQ-PIB的冻结码本修复阶段，仅L1机制诊断；没有实现PATH Decoder、RQ训练或偏好训练。完整生产训练与A/B成本过高，不复现（审查 DONE）。输入必须提供冻结码中心、残差、分配、训练期权重和父前缀。算法实现Eq13–15/Algorithm1的分支修复，以独立构造验证最小可行移动、空分支目的地、重商品上界、总负载守恒、至多一次移动和“不修复则超载”的负对照。合成权重不是推荐指标，也不能说明未来曝光更公平。  生成式推荐 前缀负载平衡 搜广推 生成式召回与推理推荐 SPAR为什么在父SID前缀内修复负载？ 热门分支的交互权重可压过其他分支，按父前缀比较兄弟负载，冻结码中心后小失真移动，保留语义路径层级。负载是训练交互次数，不只是物品数。 例如两个分支各十件商品，但一个包含热门款，其交互负载可远大。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-spar-prefix-balance-335a990d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c23aad85b0e6ef99">SPAR为什么在父SID前缀内修复负载？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aspar-prefix-balance">SPAR: Stepwise Personalized Autoregressive Recommendation with Prefix-Balanced Semantic IDs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Electronic Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>热门分支的交互权重可压过其他分支，按父前缀比较兄弟负载，冻结码中心后小失真移动，保留语义路径层级。负载是训练交互次数，不只是物品数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个分支各十件商品，但一个包含热门款，其交互负载可远大。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.27898v1">原论文</a> · <a href="../../../../recommendation-components/2610.27898-spar-prefix-balance/">实现解读</a> · <a href="#qa-c23aad85b0e6ef99">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:spar-prefix-balance" data-paper-title="SPAR: Stepwise Personalized Autoregressive Recommendation with Prefix-Balanced Semantic IDs" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="SPAR: Stepwise Personalized Autoregressive Recommendation with Prefix-Balanced Semantic IDs 搜广推与 LLM 应用 University of Electronic Science and Technology of China 2026-10-20 同一用户长历史中，有用证据随已生成SID前缀而变；热门前缀的交互负载还会压倒其他分支。SPAR由三部分组成：按前缀检索粗到细记忆的PATH、冻结残差码本后的RQ-PIB负载修复，以及SFT+DPO偏好对齐。本地只实现第二部分的修复子程序，不拿字典或K-means冒充整个推荐模型。 完整生产训练与A/B成本过高，不复现（审查 DONE）。已实现RQ-PIB的冻结码本修复阶段，仅L1机制诊断；已实现RQ-PIB的冻结码本修复阶段，仅L1机制诊断；没有实现PATH Decoder、RQ训练或偏好训练。完整生产训练与A/B成本过高，不复现（审查 DONE）。输入必须提供冻结码中心、残差、分配、训练期权重和父前缀。算法实现Eq13–15/Algorithm1的分支修复，以独立构造验证最小可行移动、空分支目的地、重商品上界、总负载守恒、至多一次移动和“不修复则超载”的负对照。合成权重不是推荐指标，也不能说明未来曝光更公平。  生成式推荐 前缀负载平衡 搜广推 生成式召回与推理推荐 SPAR 的 RQ-PIB 为什么只移动商品分支、不更新码中心，并用包含最重商品的负载上界？ 冻结码中心与父前缀可限制修复对语义路径的扰动，算法只在可行目的分支中选择距离代价最小的当前移动。商品不可分且权重不同，平均负载不一定可达，因此上界需考虑最重商品，不能强求严格等分。每件至多移动一次也限定修复范围；本地只实现这段子程序，没有整个记忆检索与偏好对齐模型。 示意：三个分支总负载十二，但某个商品单独重六，要求每支恰好四不可能。上界容纳不可分重商品，再从过载支选代价最小的可行移动，而非重训所有码中心。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-e5b3653237f86b16">SPAR 的 RQ-PIB 为什么只移动商品分支、不更新码中心，并用包含最重商品的负载上界？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aspar-prefix-balance">SPAR: Stepwise Personalized Autoregressive Recommendation with Prefix-Balanced Semantic IDs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Electronic Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冻结码中心与父前缀可限制修复对语义路径的扰动，算法只在可行目的分支中选择距离代价最小的当前移动。商品不可分且权重不同，平均负载不一定可达，因此上界需考虑最重商品，不能强求严格等分。每件至多移动一次也限定修复范围；本地只实现这段子程序，没有整个记忆检索与偏好对齐模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三个分支总负载十二，但某个商品单独重六，要求每支恰好四不可能。上界容纳不可分重商品，再从过载支选代价最小的可行移动，而非重训所有码中心。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.27898v1">原论文</a> · <a href="../../../../recommendation-components/2610.27898-spar-prefix-balance/">实现解读</a> · <a href="#qa-e5b3653237f86b16">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:spar-prefix-balance" data-paper-title="SPAR: Stepwise Personalized Autoregressive Recommendation with Prefix-Balanced Semantic IDs" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="SPAR: Stepwise Personalized Autoregressive Recommendation with Prefix-Balanced Semantic IDs 搜广推与 LLM 应用 University of Electronic Science and Technology of China 2026-10-20 同一用户长历史中，有用证据随已生成SID前缀而变；热门前缀的交互负载还会压倒其他分支。SPAR由三部分组成：按前缀检索粗到细记忆的PATH、冻结残差码本后的RQ-PIB负载修复，以及SFT+DPO偏好对齐。本地只实现第二部分的修复子程序，不拿字典或K-means冒充整个推荐模型。 完整生产训练与A/B成本过高，不复现（审查 DONE）。已实现RQ-PIB的冻结码本修复阶段，仅L1机制诊断；已实现RQ-PIB的冻结码本修复阶段，仅L1机制诊断；没有实现PATH Decoder、RQ训练或偏好训练。完整生产训练与A/B成本过高，不复现（审查 DONE）。输入必须提供冻结码中心、残差、分配、训练期权重和父前缀。算法实现Eq13–15/Algorithm1的分支修复，以独立构造验证最小可行移动、空分支目的地、重商品上界、总负载守恒、至多一次移动和“不修复则超载”的负对照。合成权重不是推荐指标，也不能说明未来曝光更公平。  生成式推荐 前缀负载平衡 搜广推 生成式召回与推理推荐 RQ-PIB可行移动与全局均等分桶有什么不同？ 它每步选当前可行的低失真增量，受最大单物品权重与上界限制，不保证完全均等或全局最优。简单平均分配会忽视语义失真和父前缀。 例如一个超热门物品不能拆成两份，负载完美相等可能本就不可能。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1bf28639da1e480d">RQ-PIB可行移动与全局均等分桶有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aspar-prefix-balance">SPAR: Stepwise Personalized Autoregressive Recommendation with Prefix-Balanced Semantic IDs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Electronic Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它每步选当前可行的低失真增量，受最大单物品权重与上界限制，不保证完全均等或全局最优。简单平均分配会忽视语义失真和父前缀。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个超热门物品不能拆成两份，负载完美相等可能本就不可能。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.27898v1">原论文</a> · <a href="../../../../recommendation-components/2610.27898-spar-prefix-balance/">实现解读</a> · <a href="#qa-1bf28639da1e480d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:spar-prefix-balance" data-paper-title="SPAR: Stepwise Personalized Autoregressive Recommendation with Prefix-Balanced Semantic IDs" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="SPAR: Stepwise Personalized Autoregressive Recommendation with Prefix-Balanced Semantic IDs 搜广推与 LLM 应用 University of Electronic Science and Technology of China 2026-10-20 同一用户长历史中，有用证据随已生成SID前缀而变；热门前缀的交互负载还会压倒其他分支。SPAR由三部分组成：按前缀检索粗到细记忆的PATH、冻结残差码本后的RQ-PIB负载修复，以及SFT+DPO偏好对齐。本地只实现第二部分的修复子程序，不拿字典或K-means冒充整个推荐模型。 完整生产训练与A/B成本过高，不复现（审查 DONE）。已实现RQ-PIB的冻结码本修复阶段，仅L1机制诊断；已实现RQ-PIB的冻结码本修复阶段，仅L1机制诊断；没有实现PATH Decoder、RQ训练或偏好训练。完整生产训练与A/B成本过高，不复现（审查 DONE）。输入必须提供冻结码中心、残差、分配、训练期权重和父前缀。算法实现Eq13–15/Algorithm1的分支修复，以独立构造验证最小可行移动、空分支目的地、重商品上界、总负载守恒、至多一次移动和“不修复则超载”的负对照。合成权重不是推荐指标，也不能说明未来曝光更公平。  生成式推荐 前缀负载平衡 搜广推 生成式召回与推理推荐 本地SPAR是否包含PATH检索和SFT+DPO整模型？ 没有，只实现冻结码本后的RQ-PIB子程序。零负载组不修，商品最多移一次，父前缀不变，中心也不更新；不能拿字典或K-means当完整推荐模型。 例如成功修复几条分支负载，只说明局部程序，不代表前缀个性化已训练。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-148a33689a91e77f">本地SPAR是否包含PATH检索和SFT+DPO整模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aspar-prefix-balance">SPAR: Stepwise Personalized Autoregressive Recommendation with Prefix-Balanced Semantic IDs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Electronic Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有，只实现冻结码本后的RQ-PIB子程序。零负载组不修，商品最多移一次，父前缀不变，中心也不更新；不能拿字典或K-means当完整推荐模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如成功修复几条分支负载，只说明局部程序，不代表前缀个性化已训练。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.27898v1">原论文</a> · <a href="../../../../recommendation-components/2610.27898-spar-prefix-balance/">实现解读</a> · <a href="#qa-148a33689a91e77f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unisgr-v2" data-paper-title="UniSGR-V2: Stepwise Target-Side Feature Anticipation and Crossing for Generative Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="UniSGR-V2: Stepwise Target-Side Feature Anticipation and Crossing for Generative Recommendation 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-10-12 生成式推荐尚未生成目标商品时无法读取其侧信息，导致逐级生成与最终排序同时缺少商品属性。TacGR在每级语义码之前预测连续侧信息并做解码器内交叉，同时用辅助排序塔防止回归目标坍塌、单向掩码隔离预测噪声。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文§4.1：24.2亿私有样本、646万用户、753万商品；8层512维GQA/SwiGLU-MoE解码器，64专家top-2、序列长度1024。数据不可用，原规模训练超出单卡A100/A30或Mac预算；没有实测本地耗时，不用昂贵试跑估算。  generative-recommendation target-side-feature multitask-ranking 搜广推 生成式召回与推理推荐 UniSGR-V2为什么预测还未生成目标商品的侧特征？ 生成到中途尚无确定item，无法直接读取最终侧信息。逐级预估连续属性并交叉，给SID生成和排序提供提前线索，辅助塔防止回归目标坍塌。 例如生成品牌相关语义码前，先估一份可能商品属性表示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-unisgr-v2-08304e35" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8a5a68bc5d810a6a">UniSGR-V2为什么预测还未生成目标商品的侧特征？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunisgr-v2">UniSGR-V2: Stepwise Target-Side Feature Anticipation and Crossing for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>生成到中途尚无确定item，无法直接读取最终侧信息。逐级预估连续属性并交叉，给SID生成和排序提供提前线索，辅助塔防止回归目标坍塌。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如生成品牌相关语义码前，先估一份可能商品属性表示。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.16132">原论文</a> · <a href="../../../../reproductions/2610.16132-unisgr-v2/">实现解读</a> · <a href="#qa-8a5a68bc5d810a6a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unisgr-v2" data-paper-title="UniSGR-V2: Stepwise Target-Side Feature Anticipation and Crossing for Generative Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="UniSGR-V2: Stepwise Target-Side Feature Anticipation and Crossing for Generative Recommendation 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-10-12 生成式推荐尚未生成目标商品时无法读取其侧信息，导致逐级生成与最终排序同时缺少商品属性。TacGR在每级语义码之前预测连续侧信息并做解码器内交叉，同时用辅助排序塔防止回归目标坍塌、单向掩码隔离预测噪声。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文§4.1：24.2亿私有样本、646万用户、753万商品；8层512维GQA/SwiGLU-MoE解码器，64专家top-2、序列长度1024。数据不可用，原规模训练超出单卡A100/A30或Mac预算；没有实测本地耗时，不用昂贵试跑估算。  generative-recommendation target-side-feature multitask-ranking 搜广推 生成式召回与推理推荐 TacGR 为什么先预测目标侧信息，又用单向掩码阻止语义 token 在注意力中读取预测 token？ 生成目标尚未确定时拿不到真实商品属性，先预测连续侧信息可为每级码提供条件。预测噪声若反复写回语义历史会累积，因此掩码限制这条注意力传播；预测特征仍通过输出条件进入生成，并非被禁用。辅助排序塔给可学习回归目标语义锚定，避免共同坍塌；本地因数据与预算没有完整复现。 示意：生成商品码前先估计价格与风格，输出头可利用这些估计；但不让估计 token 任意污染此前语义状态。若只把预测特征全部关掉，就失去了论文要补充的目标侧信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-0d266de6aee71fa6">TacGR 为什么先预测目标侧信息，又用单向掩码阻止语义 token 在注意力中读取预测 token？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunisgr-v2">UniSGR-V2: Stepwise Target-Side Feature Anticipation and Crossing for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>生成目标尚未确定时拿不到真实商品属性，先预测连续侧信息可为每级码提供条件。预测噪声若反复写回语义历史会累积，因此掩码限制这条注意力传播；预测特征仍通过输出条件进入生成，并非被禁用。辅助排序塔给可学习回归目标语义锚定，避免共同坍塌；本地因数据与预算没有完整复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>生成商品码前先估计价格与风格，输出头可利用这些估计；但不让估计 token 任意污染此前语义状态。若只把预测特征全部关掉，就失去了论文要补充的目标侧信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.16132">原论文</a> · <a href="../../../../reproductions/2610.16132-unisgr-v2/">实现解读</a> · <a href="#qa-0d266de6aee71fa6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unisgr-v2" data-paper-title="UniSGR-V2: Stepwise Target-Side Feature Anticipation and Crossing for Generative Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="UniSGR-V2: Stepwise Target-Side Feature Anticipation and Crossing for Generative Recommendation 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-10-12 生成式推荐尚未生成目标商品时无法读取其侧信息，导致逐级生成与最终排序同时缺少商品属性。TacGR在每级语义码之前预测连续侧信息并做解码器内交叉，同时用辅助排序塔防止回归目标坍塌、单向掩码隔离预测噪声。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文§4.1：24.2亿私有样本、646万用户、753万商品；8层512维GQA/SwiGLU-MoE解码器，64专家top-2、序列长度1024。数据不可用，原规模训练超出单卡A100/A30或Mac预算；没有实测本地耗时，不用昂贵试跑估算。  generative-recommendation target-side-feature multitask-ranking 搜广推 生成式召回与推理推荐 单向mask与完全禁用预测特征有什么不同？ 语义token不读取预测token，预测token可读历史语义，但预测特征仍通过输出条件进入生成。禁用会删掉方法核心，不是实现同一隔离。 例如阻止内部噪声互传，不表示最终生成头不能使用预测属性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7be92ca500e528ac">单向mask与完全禁用预测特征有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunisgr-v2">UniSGR-V2: Stepwise Target-Side Feature Anticipation and Crossing for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语义token不读取预测token，预测token可读历史语义，但预测特征仍通过输出条件进入生成。禁用会删掉方法核心，不是实现同一隔离。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如阻止内部噪声互传，不表示最终生成头不能使用预测属性。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.16132">原论文</a> · <a href="../../../../reproductions/2610.16132-unisgr-v2/">实现解读</a> · <a href="#qa-7be92ca500e528ac">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unisgr-v2" data-paper-title="UniSGR-V2: Stepwise Target-Side Feature Anticipation and Crossing for Generative Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="UniSGR-V2: Stepwise Target-Side Feature Anticipation and Crossing for Generative Recommendation 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-10-12 生成式推荐尚未生成目标商品时无法读取其侧信息，导致逐级生成与最终排序同时缺少商品属性。TacGR在每级语义码之前预测连续侧信息并做解码器内交叉，同时用辅助排序塔防止回归目标坍塌、单向掩码隔离预测噪声。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文§4.1：24.2亿私有样本、646万用户、753万商品；8层512维GQA/SwiGLU-MoE解码器，64专家top-2、序列长度1024。数据不可用，原规模训练超出单卡A100/A30或Mac预算；没有实测本地耗时，不用昂贵试跑估算。  generative-recommendation target-side-feature multitask-ranking 搜广推 生成式召回与推理推荐 真实属性辅助塔为什么不能被当前预测值自监督替代？ 可学习回归目标需业务标签锚定，纯自追预测可能共同坍塌。训练目标特征与未来标签隔离，mask按token类型判定，不可让语义状态读真实未来商品属性。 例如两网络一起输出常数也可互相拟合，辅助业务任务用于排除这种空解。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-632cf77864f1705d">真实属性辅助塔为什么不能被当前预测值自监督替代？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunisgr-v2">UniSGR-V2: Stepwise Target-Side Feature Anticipation and Crossing for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>可学习回归目标需业务标签锚定，纯自追预测可能共同坍塌。训练目标特征与未来标签隔离，mask按token类型判定，不可让语义状态读真实未来商品属性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两网络一起输出常数也可互相拟合，辅助业务任务用于排除这种空解。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.16132">原论文</a> · <a href="../../../../reproductions/2610.16132-unisgr-v2/">实现解读</a> · <a href="#qa-632cf77864f1705d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:wegr" data-paper-title="WeGR: Unified Generative Retrieval for Industrial Search Systems in WeChat" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="WeGR: Unified Generative Retrieval for Industrial Search Systems in WeChat 搜广推与 LLM 应用 WeChat E-commerce Search team（正文未单列作者机构） 2026-10-12 WeGR 联合优化协同语义编码和生成检索偏好：CoCo-VAE 让连续表示学习查询—商品与商品—商品共现，刷新低使用率码字，并用残差保真和跨样本碰撞损失改善码本利用率。DHPO 从短 SID 前缀逐步扩展到完整 SID，同时扩展奖励匹配和策略梯度范围，以多正例 SFT 稳定稀疏奖励下的训练。 三种子只是有界机制诊断，稳定相对提升不适用。本地对照口径：基线为 SFT 和完整 SID GRPO+MSFT，实验组为动态 horizon DHPO+MSFT；共用同一 CoCo-VAE 和 SFT 初始化。三种子只是有界机制诊断，稳定相对提升不适用。  generative-recommendation semantic-id preference-optimization 搜广推 生成式召回与推理推荐 WeGR为什么让偏好优化从短SID前缀逐步扩展？ 完整SID匹配奖励稀疏，先学粗前缀提供较多有效信号，再逐步扩大到完整路径。优化范围应和奖励horizon同步，避免奖励粗却惩罚整段无关后缀。 例如先确认大类，再要求具体细码，不是一开始就只接受完整串全对。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-wegr-8c03ebb0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-349baee34dd5d03a">WeGR为什么让偏好优化从短SID前缀逐步扩展？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Awegr">WeGR: Unified Generative Retrieval for Industrial Search Systems in WeChat</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · WeChat E-commerce Search team（正文未单列作者机构）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>完整SID匹配奖励稀疏，先学粗前缀提供较多有效信号，再逐步扩大到完整路径。优化范围应和奖励horizon同步，避免奖励粗却惩罚整段无关后缀。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先确认大类，再要求具体细码，不是一开始就只接受完整串全对。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.16979">原论文</a> · <a href="../../../../reproductions/2610.16979-wegr/">实现解读</a> · <a href="#qa-349baee34dd5d03a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:wegr" data-paper-title="WeGR: Unified Generative Retrieval for Industrial Search Systems in WeChat" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="WeGR: Unified Generative Retrieval for Industrial Search Systems in WeChat 搜广推与 LLM 应用 WeChat E-commerce Search team（正文未单列作者机构） 2026-10-12 WeGR 联合优化协同语义编码和生成检索偏好：CoCo-VAE 让连续表示学习查询—商品与商品—商品共现，刷新低使用率码字，并用残差保真和跨样本碰撞损失改善码本利用率。DHPO 从短 SID 前缀逐步扩展到完整 SID，同时扩展奖励匹配和策略梯度范围，以多正例 SFT 稳定稀疏奖励下的训练。 三种子只是有界机制诊断，稳定相对提升不适用。本地对照口径：基线为 SFT 和完整 SID GRPO+MSFT，实验组为动态 horizon DHPO+MSFT；共用同一 CoCo-VAE 和 SFT 初始化。三种子只是有界机制诊断，稳定相对提升不适用。  generative-recommendation semantic-id preference-optimization 搜广推 生成式召回与推理推荐 WeGR 的 DHPO 为什么从短 SID 前缀逐渐扩展奖励匹配与策略梯度范围？ 一开始要求完整长 SID 命中会让奖励极稀疏，模型难区分部分正确路径。动态 horizon 先奖励较短前缀，并只更新对应 token 范围，再随训练逐步扩到完整路径，使奖励粒度与优化范围一致。多正例 SFT 稳定更新，CoCo-VAE 另行改善编码；本地是有界机制诊断，不能据此宣称大规模稳定提升。 示意：先学对“户外”粗码就能获得反馈，之后要求“户外—露营”，最终才要求具体帐篷完整码。若只放宽奖励却仍强更新全部后缀，可能把未被评价的错误路径一起强化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-560f97a3aa5441bb">WeGR 的 DHPO 为什么从短 SID 前缀逐渐扩展奖励匹配与策略梯度范围？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Awegr">WeGR: Unified Generative Retrieval for Industrial Search Systems in WeChat</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · WeChat E-commerce Search team（正文未单列作者机构）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一开始要求完整长 SID 命中会让奖励极稀疏，模型难区分部分正确路径。动态 horizon 先奖励较短前缀，并只更新对应 token 范围，再随训练逐步扩到完整路径，使奖励粒度与优化范围一致。多正例 SFT 稳定更新，CoCo-VAE 另行改善编码；本地是有界机制诊断，不能据此宣称大规模稳定提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先学对“户外”粗码就能获得反馈，之后要求“户外—露营”，最终才要求具体帐篷完整码。若只放宽奖励却仍强更新全部后缀，可能把未被评价的错误路径一起强化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.16979">原论文</a> · <a href="../../../../reproductions/2610.16979-wegr/">实现解读</a> · <a href="#qa-560f97a3aa5441bb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:wegr" data-paper-title="WeGR: Unified Generative Retrieval for Industrial Search Systems in WeChat" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="WeGR: Unified Generative Retrieval for Industrial Search Systems in WeChat 搜广推与 LLM 应用 WeChat E-commerce Search team（正文未单列作者机构） 2026-10-12 WeGR 联合优化协同语义编码和生成检索偏好：CoCo-VAE 让连续表示学习查询—商品与商品—商品共现，刷新低使用率码字，并用残差保真和跨样本碰撞损失改善码本利用率。DHPO 从短 SID 前缀逐步扩展到完整 SID，同时扩展奖励匹配和策略梯度范围，以多正例 SFT 稳定稀疏奖励下的训练。 三种子只是有界机制诊断，稳定相对提升不适用。本地对照口径：基线为 SFT 和完整 SID GRPO+MSFT，实验组为动态 horizon DHPO+MSFT；共用同一 CoCo-VAE 和 SFT 初始化。三种子只是有界机制诊断，稳定相对提升不适用。  generative-recommendation semantic-id preference-optimization 搜广推 生成式召回与推理推荐 CoCo-VAE跨样本碰撞损失与单样本熵有什么区别？ 碰撞衡量不同样本分配重合，熵描述单样本分布扩散。高熵也可能所有样本都均匀重叠，不能用熵直接替代碰撞约束或码使用均衡。 例如每件商品都均匀给所有码，熵高但没有实现有区分的编码。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-985a686fe1d1692f">CoCo-VAE跨样本碰撞损失与单样本熵有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Awegr">WeGR: Unified Generative Retrieval for Industrial Search Systems in WeChat</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · WeChat E-commerce Search team（正文未单列作者机构）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>碰撞衡量不同样本分配重合，熵描述单样本分布扩散。高熵也可能所有样本都均匀重叠，不能用熵直接替代碰撞约束或码使用均衡。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如每件商品都均匀给所有码，熵高但没有实现有区分的编码。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.16979">原论文</a> · <a href="../../../../reproductions/2610.16979-wegr/">实现解读</a> · <a href="#qa-985a686fe1d1692f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:wegr" data-paper-title="WeGR: Unified Generative Retrieval for Industrial Search Systems in WeChat" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="WeGR: Unified Generative Retrieval for Industrial Search Systems in WeChat 搜广推与 LLM 应用 WeChat E-commerce Search team（正文未单列作者机构） 2026-10-12 WeGR 联合优化协同语义编码和生成检索偏好：CoCo-VAE 让连续表示学习查询—商品与商品—商品共现，刷新低使用率码字，并用残差保真和跨样本碰撞损失改善码本利用率。DHPO 从短 SID 前缀逐步扩展到完整 SID，同时扩展奖励匹配和策略梯度范围，以多正例 SFT 稳定稀疏奖励下的训练。 三种子只是有界机制诊断，稳定相对提升不适用。本地对照口径：基线为 SFT 和完整 SID GRPO+MSFT，实验组为动态 horizon DHPO+MSFT；共用同一 CoCo-VAE 和 SFT 初始化。三种子只是有界机制诊断，稳定相对提升不适用。  generative-recommendation semantic-id preference-optimization 搜广推 生成式召回与推理推荐 WeGR低利用率刷新是否对所有残差层都执行？ 规定只根据首层命中EMA刷新，深层不刷新；DHPO前h词元范围随调度同步，另加逐session多正例NLL。不得用固定全序列loss冒充渐进horizon。 例如h为一时，后面未匹配码不应按相同奖励获得完整策略梯度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d623e744cb8952fe">WeGR低利用率刷新是否对所有残差层都执行？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Awegr">WeGR: Unified Generative Retrieval for Industrial Search Systems in WeChat</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · WeChat E-commerce Search team（正文未单列作者机构）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>规定只根据首层命中EMA刷新，深层不刷新；DHPO前h词元范围随调度同步，另加逐session多正例NLL。不得用固定全序列loss冒充渐进horizon。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如h为一时，后面未匹配码不应按相同奖励获得完整策略梯度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.16979">原论文</a> · <a href="../../../../reproductions/2610.16979-wegr/">实现解读</a> · <a href="#qa-d623e744cb8952fe">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gear" data-paper-title="Generative End-to-end Ad Retrieval at Douyin" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Generative End-to-end Ad Retrieval at Douyin 搜广推与 LLM 应用 ByteDance 2026-09-30 GEAR 用正交基参数化 BasisVQ/BasisRQ，使码本更新具有全局共享和稳定旋转；生成器输出层级 token，碰撞 item 再由上下文条件 reranker 精排。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 BasisVQ、前缀残差量化接口与碰撞 rerank；不复刻流式 PS、分钟级索引和线上流量，不把本地随机张量作为广告效果。执行 BasisVQ、前缀残差量化接口与碰撞 rerank；不复刻流式 PS、分钟级索引和线上流量，不把本地随机张量作为广告效果。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  ad-retrieval generative-retrieval semantic-id 搜广推 生成式召回与推理推荐 GEAR 的 BasisVQ/BasisRQ 为什么把码表示为共享正交基上的坐标？ 共享基使更新可在统一结构内协调，正交性约束旋转，码字不再完全独立任意漂移。分层生成提供候选地址，碰撞组再用上下文精排。正交基并不保证语义独立或无碰撞，仍需检查量化与排序两个阶段。 示意：像共用一套坐标轴表达各商品，转动基可一致调整布局；即使坐标系统稳定，两件近似商品仍可能落入同一码桶。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-gear-42599d59" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-779db58082983dba">GEAR 的 BasisVQ/BasisRQ 为什么把码表示为共享正交基上的坐标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agear">Generative End-to-end Ad Retrieval at Douyin</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共享基使更新可在统一结构内协调，正交性约束旋转，码字不再完全独立任意漂移。分层生成提供候选地址，碰撞组再用上下文精排。正交基并不保证语义独立或无碰撞，仍需检查量化与排序两个阶段。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>像共用一套坐标轴表达各商品，转动基可一致调整布局；即使坐标系统稳定，两件近似商品仍可能落入同一码桶。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.39327">原论文</a> · <a href="../../../../reproductions/2609.39327-gear/">实现解读</a> · <a href="#qa-779db58082983dba">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gear" data-paper-title="Generative End-to-end Ad Retrieval at Douyin" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Generative End-to-end Ad Retrieval at Douyin 搜广推与 LLM 应用 ByteDance 2026-09-30 GEAR 用正交基参数化 BasisVQ/BasisRQ，使码本更新具有全局共享和稳定旋转；生成器输出层级 token，碰撞 item 再由上下文条件 reranker 精排。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 BasisVQ、前缀残差量化接口与碰撞 rerank；不复刻流式 PS、分钟级索引和线上流量，不把本地随机张量作为广告效果。执行 BasisVQ、前缀残差量化接口与碰撞 rerank；不复刻流式 PS、分钟级索引和线上流量，不把本地随机张量作为广告效果。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  ad-retrieval generative-retrieval semantic-id 搜广推 生成式召回与推理推荐 GEAR为什么把码本写成共享正交基，而不是任意更新每个码向量？ 共享基使码本变化受到整体几何结构约束，便于在更新中保留较稳定的表示关系；层级生成仍负责粗到细选择，碰撞组再交给上下文重排区分。结构化码本不自动消除碰撞，也不能代替推荐目标训练。本地只验证量化、状态与梯度组件，不支持将其说成完整广告检索收益。 示意：多个码共享一套坐标基，更新更像有组织地调整坐标而非各自乱漂；两件广告若仍落在同一码，必须根据当前用户再排，不能只返回一个固定热门广告。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-97a87993f2fd04a0">GEAR为什么把码本写成共享正交基，而不是任意更新每个码向量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agear">Generative End-to-end Ad Retrieval at Douyin</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共享基使码本变化受到整体几何结构约束，便于在更新中保留较稳定的表示关系；层级生成仍负责粗到细选择，碰撞组再交给上下文重排区分。结构化码本不自动消除碰撞，也不能代替推荐目标训练。本地只验证量化、状态与梯度组件，不支持将其说成完整广告检索收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>多个码共享一套坐标基，更新更像有组织地调整坐标而非各自乱漂；两件广告若仍落在同一码，必须根据当前用户再排，不能只返回一个固定热门广告。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.39327">原论文</a> · <a href="../../../../reproductions/2609.39327-gear/">实现解读</a> · <a href="#qa-97a87993f2fd04a0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gear" data-paper-title="Generative End-to-end Ad Retrieval at Douyin" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Generative End-to-end Ad Retrieval at Douyin 搜广推与 LLM 应用 ByteDance 2026-09-30 GEAR 用正交基参数化 BasisVQ/BasisRQ，使码本更新具有全局共享和稳定旋转；生成器输出层级 token，碰撞 item 再由上下文条件 reranker 精排。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 BasisVQ、前缀残差量化接口与碰撞 rerank；不复刻流式 PS、分钟级索引和线上流量，不把本地随机张量作为广告效果。执行 BasisVQ、前缀残差量化接口与碰撞 rerank；不复刻流式 PS、分钟级索引和线上流量，不把本地随机张量作为广告效果。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  ad-retrieval generative-retrieval semantic-id 搜广推 生成式召回与推理推荐 GEAR 的碰撞 reranker 与无限扩大 codebook，相比怎样分配区分能力？ 大码本尝试在离散地址直接区分更多物品，reranker 允许有限码内先共组，再按用户上下文细分。后者节省离散容量却增加桶内计算和召回限制，二者没有无条件优劣。来源本地仅验证机制状态，不能拿正交误差或碰撞展开当推荐质量证据。 示意：两件同码相机由用户用途再选，而非为每件都分独立大词表编号；桶太大时精排成本也会增长，不能只说短码总便宜。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-31adb8cf73ce4e1d">GEAR 的碰撞 reranker 与无限扩大 codebook，相比怎样分配区分能力？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agear">Generative End-to-end Ad Retrieval at Douyin</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>大码本尝试在离散地址直接区分更多物品，reranker 允许有限码内先共组，再按用户上下文细分。后者节省离散容量却增加桶内计算和召回限制，二者没有无条件优劣。来源本地仅验证机制状态，不能拿正交误差或碰撞展开当推荐质量证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两件同码相机由用户用途再选，而非为每件都分独立大词表编号；桶太大时精排成本也会增长，不能只说短码总便宜。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.39327">原论文</a> · <a href="../../../../reproductions/2609.39327-gear/">实现解读</a> · <a href="#qa-31adb8cf73ce4e1d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gear" data-paper-title="Generative End-to-end Ad Retrieval at Douyin" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Generative End-to-end Ad Retrieval at Douyin 搜广推与 LLM 应用 ByteDance 2026-09-30 GEAR 用正交基参数化 BasisVQ/BasisRQ，使码本更新具有全局共享和稳定旋转；生成器输出层级 token，碰撞 item 再由上下文条件 reranker 精排。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 BasisVQ、前缀残差量化接口与碰撞 rerank；不复刻流式 PS、分钟级索引和线上流量，不把本地随机张量作为广告效果。执行 BasisVQ、前缀残差量化接口与碰撞 rerank；不复刻流式 PS、分钟级索引和线上流量，不把本地随机张量作为广告效果。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  ad-retrieval generative-retrieval semantic-id 搜广推 生成式召回与推理推荐 GEAR 计算 zB 与回映射时，为什么要统一行向量约定并检查 B 的正交性？ 投影、最近码选择和从坐标回到原空间需要一致转置，方阵形状相同也可能写反。B 的正交误差、残差量化和碰撞候选映射应分别核验，不能用一个 loss 代替全部。来源诊断范围不包含生产生成器规模效果。 示意：若先按行向量乘 B，重建却又乘同一方向而非对应逆变换，数值可运行但坐标没回去；应拿已知向量验证往返。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-2eaf29cb6ed10361">GEAR 计算 zB 与回映射时，为什么要统一行向量约定并检查 B 的正交性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agear">Generative End-to-end Ad Retrieval at Douyin</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>投影、最近码选择和从坐标回到原空间需要一致转置，方阵形状相同也可能写反。B 的正交误差、残差量化和碰撞候选映射应分别核验，不能用一个 loss 代替全部。来源诊断范围不包含生产生成器规模效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>若先按行向量乘 B，重建却又乘同一方向而非对应逆变换，数值可运行但坐标没回去；应拿已知向量验证往返。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.39327">原论文</a> · <a href="../../../../reproductions/2609.39327-gear/">实现解读</a> · <a href="#qa-2eaf29cb6ed10361">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:grp" data-paper-title="GRP v0.1 Technical Report" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="GRP v0.1 Technical Report 搜广推与 LLM 应用 Snap Inc. 2026-09-29 GRP 不是一次性替换成熟推荐漏斗，而是逐步把统一生成模型作为召回源接入，再替换弱源、增加配额并逐步绕过排序器。模型用 encoder-decoder 生成多模态 Semantic ID；MHP 通过 stop-gradient 路径联合学习排序，之后冻结为 RL reward。mGRPO 在 GRPO 上增加以 logged target 为锚点的单边 margin，只在策略开始牺牲原目标召回时惩罚。 复现级别：L1 架构与目标机制。复现级别：L1 架构与目标机制。本地实现独立 SID block mask、生成/排序梯度隔离和 mGRPO 单边召回保护；不宣称复现 Snap 线上效果。未包含 Snap 私有数据、Qwen3-VL SID tokenizer、生产尺度训练、CUDA graph serving、反向目录和在线流量，因此标记 concept_demo / l1_mechanism，不进入 Evolve 的效果提升证据池。本地对照口径：基线为不触发 logged-target 单边保护的同一 GRPO surrogate，实验组启用保护项；  generative-recommendation ranking rl-alignment 搜广推 生成式召回与推理推荐 GRP 为什么采用逐步迁移推荐漏斗，而不是一次替换全部阶段？ 成熟系统承担多种目标和风险，先以额外召回源接入，再替换弱源、增配额和逐步绕过排序，可阶段性观察影响。统一模型仍需保护原目标召回，不能将架构愿景当作已完成替换。不同阶段证据和业务权限也应独立。 示意：生成器先只占少量候选，验证后再扩大，不因一轮离线好分就删掉全部已有召回器和精排路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-grp-12c5e416" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e4195cdb964d413c">GRP 为什么采用逐步迁移推荐漏斗，而不是一次替换全部阶段？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agrp">GRP v0.1 Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Snap Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>成熟系统承担多种目标和风险，先以额外召回源接入，再替换弱源、增配额和逐步绕过排序，可阶段性观察影响。统一模型仍需保护原目标召回，不能将架构愿景当作已完成替换。不同阶段证据和业务权限也应独立。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>生成器先只占少量候选，验证后再扩大，不因一轮离线好分就删掉全部已有召回器和精排路径。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36688">原论文</a> · <a href="../../../../reproductions/2609.36688-grp/">实现解读</a> · <a href="#qa-e4195cdb964d413c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:grp" data-paper-title="GRP v0.1 Technical Report" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="GRP v0.1 Technical Report 搜广推与 LLM 应用 Snap Inc. 2026-09-29 GRP 不是一次性替换成熟推荐漏斗，而是逐步把统一生成模型作为召回源接入，再替换弱源、增加配额并逐步绕过排序器。模型用 encoder-decoder 生成多模态 Semantic ID；MHP 通过 stop-gradient 路径联合学习排序，之后冻结为 RL reward。mGRPO 在 GRPO 上增加以 logged target 为锚点的单边 margin，只在策略开始牺牲原目标召回时惩罚。 复现级别：L1 架构与目标机制。复现级别：L1 架构与目标机制。本地实现独立 SID block mask、生成/排序梯度隔离和 mGRPO 单边召回保护；不宣称复现 Snap 线上效果。未包含 Snap 私有数据、Qwen3-VL SID tokenizer、生产尺度训练、CUDA graph serving、反向目录和在线流量，因此标记 concept_demo / l1_mechanism，不进入 Evolve 的效果提升证据池。本地对照口径：基线为不触发 logged-target 单边保护的同一 GRPO surrogate，实验组启用保护项；  generative-recommendation ranking rl-alignment 搜广推 生成式召回与推理推荐 GRP的logged-target单边margin为什么只在原目标召回被牺牲时激活？ 奖励优化可能把策略推向少数高分输出，同时降低原日志目标的概率。单边保护只惩罚超过容忍区间的下降，给新偏好改进留空间，又避免任意损伤基础召回；排序reward头停止梯度并冻结，也减少奖励与生成器相互追逐。本地仅验证目标与梯度组件，不能据此证明生产漏斗已被替换。 示意：新策略发现更有价值的候选且未明显损伤原目标时无需额外束缚；若只是把概率全部挪给一类高奖励物品，margin才对这种基础能力退化施加保护。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-7c1a13612a425df6">GRP的logged-target单边margin为什么只在原目标召回被牺牲时激活？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agrp">GRP v0.1 Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Snap Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>奖励优化可能把策略推向少数高分输出，同时降低原日志目标的概率。单边保护只惩罚超过容忍区间的下降，给新偏好改进留空间，又避免任意损伤基础召回；排序reward头停止梯度并冻结，也减少奖励与生成器相互追逐。本地仅验证目标与梯度组件，不能据此证明生产漏斗已被替换。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新策略发现更有价值的候选且未明显损伤原目标时无需额外束缚；若只是把概率全部挪给一类高奖励物品，margin才对这种基础能力退化施加保护。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36688">原论文</a> · <a href="../../../../reproductions/2609.36688-grp/">实现解读</a> · <a href="#qa-7c1a13612a425df6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:grp" data-paper-title="GRP v0.1 Technical Report" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="GRP v0.1 Technical Report 搜广推与 LLM 应用 Snap Inc. 2026-09-29 GRP 不是一次性替换成熟推荐漏斗，而是逐步把统一生成模型作为召回源接入，再替换弱源、增加配额并逐步绕过排序器。模型用 encoder-decoder 生成多模态 Semantic ID；MHP 通过 stop-gradient 路径联合学习排序，之后冻结为 RL reward。mGRPO 在 GRPO 上增加以 logged target 为锚点的单边 margin，只在策略开始牺牲原目标召回时惩罚。 复现级别：L1 架构与目标机制。复现级别：L1 架构与目标机制。本地实现独立 SID block mask、生成/排序梯度隔离和 mGRPO 单边召回保护；不宣称复现 Snap 线上效果。未包含 Snap 私有数据、Qwen3-VL SID tokenizer、生产尺度训练、CUDA graph serving、反向目录和在线流量，因此标记 concept_demo / l1_mechanism，不进入 Evolve 的效果提升证据池。本地对照口径：基线为不触发 logged-target 单边保护的同一 GRPO surrogate，实验组启用保护项；  generative-recommendation ranking rl-alignment 搜广推 生成式召回与推理推荐 GRP 的单边 margin 与对称约束所有概率变化，相比保留哪类改进自由？ 单边保护只在 logged target 相对参考下降超容忍区间时惩罚，不压制所有其他偏好改善；对称约束则连有益变化也可能限制。它防止牺牲已知目标，却不保证新奖励全面可靠。本地只检验 surrogate 目标与梯度，不是生产策略效果。 示意：新策略提高更优候选且原目标没明显下降时保护项不启动；若为奖励大幅抛弃原目标，才被拉回，而非任何变化都罚。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-094cd821bb640a1f">GRP 的单边 margin 与对称约束所有概率变化，相比保留哪类改进自由？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agrp">GRP v0.1 Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Snap Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单边保护只在 logged target 相对参考下降超容忍区间时惩罚，不压制所有其他偏好改善；对称约束则连有益变化也可能限制。它防止牺牲已知目标，却不保证新奖励全面可靠。本地只检验 surrogate 目标与梯度，不是生产策略效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新策略提高更优候选且原目标没明显下降时保护项不启动；若为奖励大幅抛弃原目标，才被拉回，而非任何变化都罚。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36688">原论文</a> · <a href="../../../../reproductions/2609.36688-grp/">实现解读</a> · <a href="#qa-094cd821bb640a1f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:grp" data-paper-title="GRP v0.1 Technical Report" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="GRP v0.1 Technical Report 搜广推与 LLM 应用 Snap Inc. 2026-09-29 GRP 不是一次性替换成熟推荐漏斗，而是逐步把统一生成模型作为召回源接入，再替换弱源、增加配额并逐步绕过排序器。模型用 encoder-decoder 生成多模态 Semantic ID；MHP 通过 stop-gradient 路径联合学习排序，之后冻结为 RL reward。mGRPO 在 GRPO 上增加以 logged target 为锚点的单边 margin，只在策略开始牺牲原目标召回时惩罚。 复现级别：L1 架构与目标机制。复现级别：L1 架构与目标机制。本地实现独立 SID block mask、生成/排序梯度隔离和 mGRPO 单边召回保护；不宣称复现 Snap 线上效果。未包含 Snap 私有数据、Qwen3-VL SID tokenizer、生产尺度训练、CUDA graph serving、反向目录和在线流量，因此标记 concept_demo / l1_mechanism，不进入 Evolve 的效果提升证据池。本地对照口径：基线为不触发 logged-target 单边保护的同一 GRPO surrogate，实验组启用保护项；  generative-recommendation ranking rl-alignment 搜广推 生成式召回与推理推荐 GRP 的 MHP 排序头为什么读取 stop-gradient 的生成表征？ 排序损失若直接反传共享编码与 SID 路径，可能破坏生成器已有召回能力。stop-gradient 让头学习排序关系而不从该损失改写生成主干，后续冻结为 RL reward 时也需明确版本。只注册排序头却不检查梯度隔离，不能验证这一机制。 示意：改变排序头权重可调整其判断，但一次排序 BCE 更新不应让生成 SID 的主干梯度发生变化；可用独立梯度检查确认。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-5ccd8a0812b61c8e">GRP 的 MHP 排序头为什么读取 stop-gradient 的生成表征？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agrp">GRP v0.1 Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Snap Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>排序损失若直接反传共享编码与 SID 路径，可能破坏生成器已有召回能力。stop-gradient 让头学习排序关系而不从该损失改写生成主干，后续冻结为 RL reward 时也需明确版本。只注册排序头却不检查梯度隔离，不能验证这一机制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>改变排序头权重可调整其判断，但一次排序 BCE 更新不应让生成 SID 的主干梯度发生变化；可用独立梯度检查确认。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36688">原论文</a> · <a href="../../../../reproductions/2609.36688-grp/">实现解读</a> · <a href="#qa-5ccd8a0812b61c8e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:xrec" data-paper-title="X-Rec Technical Report" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="X-Rec Technical Report 搜广推与 LLM 应用 TikTok (ByteDance) 2026-09-24 传统 U2I 召回将用户兴趣压缩为一个或少量向量，生成式语义 ID 方法则要逐 token 解码。X-Rec 直接在归一化 item embedding 球面上生成多个召回触发向量：先预测 item 所在的粗粒度聚类（anchor），再以该 anchor 为条件把球面噪声沿测地线流向目标 item。生成的向量与全量 item embedding 做近邻检索，可覆盖多个兴趣区域而无需语义 ID 量化。论文的另一个重点是计算结构：历史行为先经过前 L-1 层 Transformer； 未执行：TikTok 私有多属性日志与 streaming benchmark、工业 item encoder、ANN/在线 KV 服务、真实线上 A/B。Fidelity：核心机制复现；证据等级：L2 公开数据集。公开 MovieLens 任务只检验算法链路，不代表 TikTok 流量或论文绝对结果。当前是低预算机制实验；在 MovieLens-1M 上，X-Rec 的三种子均值低于 U2I，不能宣称收益。实际执行：item 对比学习、球面 anchor 聚类与 CE、测地线 RFM 监督、末层历史 K/V 复用、时间/anchor 调制、切空间速度、球面 Euler 和多 trigger 全目录检索。  retrieval generative-recommendation flow-matching 搜广推 生成式召回与推理推荐 X-Rec为什么在item embedding球面上生成trigger？ 直接生成归一向量后检索多个兴趣区，避免SID离散量化及逐码解码。anchor提供粗区域条件，流匹配学习从球面噪声到目标方向，仍需有效item近邻落地。 例如生成几个不同兴趣方向，再从目录找各方向相近内容。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-xrec-d9eceda3" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9284c7fba5ba0f2c">X-Rec为什么在item embedding球面上生成trigger？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Axrec">X-Rec Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · TikTok (ByteDance)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直接生成归一向量后检索多个兴趣区，避免SID离散量化及逐码解码。anchor提供粗区域条件，流匹配学习从球面噪声到目标方向，仍需有效item近邻落地。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如生成几个不同兴趣方向，再从目录找各方向相近内容。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.29180">原论文</a> · <a href="../../../../reproductions/2609.29180-xrec/">实现解读</a> · <a href="#qa-9284c7fba5ba0f2c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:xrec" data-paper-title="X-Rec Technical Report" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="X-Rec Technical Report 搜广推与 LLM 应用 TikTok (ByteDance) 2026-09-24 传统 U2I 召回将用户兴趣压缩为一个或少量向量，生成式语义 ID 方法则要逐 token 解码。X-Rec 直接在归一化 item embedding 球面上生成多个召回触发向量：先预测 item 所在的粗粒度聚类（anchor），再以该 anchor 为条件把球面噪声沿测地线流向目标 item。生成的向量与全量 item embedding 做近邻检索，可覆盖多个兴趣区域而无需语义 ID 量化。论文的另一个重点是计算结构：历史行为先经过前 L-1 层 Transformer； 未执行：TikTok 私有多属性日志与 streaming benchmark、工业 item encoder、ANN/在线 KV 服务、真实线上 A/B。Fidelity：核心机制复现；证据等级：L2 公开数据集。公开 MovieLens 任务只检验算法链路，不代表 TikTok 流量或论文绝对结果。当前是低预算机制实验；在 MovieLens-1M 上，X-Rec 的三种子均值低于 U2I，不能宣称收益。实际执行：item 对比学习、球面 anchor 聚类与 CE、测地线 RFM 监督、末层历史 K/V 复用、时间/anchor 调制、切空间速度、球面 Euler 和多 trigger 全目录检索。  retrieval generative-recommendation flow-matching 搜广推 生成式召回与推理推荐 X-Rec 为什么在归一化 embedding 球面上做条件流生成，而不是逐 token 生成 SID？ 连续 trigger 可直接对接近邻检索，避免离散量化与逐码路径的误差。先预测粗 anchor，再让球面噪声沿测地线流向目标向量，切空间投影和球面积分维持归一化几何；历史前层只算一次，去噪仅更新末层生成 token。它仍有多步采样与检索成本，本地低预算结果为负，不能据结构声称优于 SID。 示意：先定位摄影兴趣区域，再从球面噪声生成多个检索向量，分别覆盖相机与镜头。向量始终留在物品归一化空间，最后交给 ANN，而不是先生成一串整数码再查表。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-4756ebc069854072">X-Rec 为什么在归一化 embedding 球面上做条件流生成，而不是逐 token 生成 SID？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Axrec">X-Rec Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · TikTok (ByteDance)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>连续 trigger 可直接对接近邻检索，避免离散量化与逐码路径的误差。先预测粗 anchor，再让球面噪声沿测地线流向目标向量，切空间投影和球面积分维持归一化几何；历史前层只算一次，去噪仅更新末层生成 token。它仍有多步采样与检索成本，本地低预算结果为负，不能据结构声称优于 SID。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先定位摄影兴趣区域，再从球面噪声生成多个检索向量，分别覆盖相机与镜头。向量始终留在物品归一化空间，最后交给 ANN，而不是先生成一串整数码再查表。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.29180">原论文</a> · <a href="../../../../reproductions/2609.29180-xrec/">实现解读</a> · <a href="#qa-4756ebc069854072">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:xrec" data-paper-title="X-Rec Technical Report" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="X-Rec Technical Report 搜广推与 LLM 应用 TikTok (ByteDance) 2026-09-24 传统 U2I 召回将用户兴趣压缩为一个或少量向量，生成式语义 ID 方法则要逐 token 解码。X-Rec 直接在归一化 item embedding 球面上生成多个召回触发向量：先预测 item 所在的粗粒度聚类（anchor），再以该 anchor 为条件把球面噪声沿测地线流向目标 item。生成的向量与全量 item embedding 做近邻检索，可覆盖多个兴趣区域而无需语义 ID 量化。论文的另一个重点是计算结构：历史行为先经过前 L-1 层 Transformer； 未执行：TikTok 私有多属性日志与 streaming benchmark、工业 item encoder、ANN/在线 KV 服务、真实线上 A/B。Fidelity：核心机制复现；证据等级：L2 公开数据集。公开 MovieLens 任务只检验算法链路，不代表 TikTok 流量或论文绝对结果。当前是低预算机制实验；在 MovieLens-1M 上，X-Rec 的三种子均值低于 U2I，不能宣称收益。实际执行：item 对比学习、球面 anchor 聚类与 CE、测地线 RFM 监督、末层历史 K/V 复用、时间/anchor 调制、切空间速度、球面 Euler 和多 trigger 全目录检索。  retrieval generative-recommendation flow-matching 搜广推 生成式召回与推理推荐 球面流与普通欧氏向量插值有什么不同？ 球面路径沿测地线，速度需切空间投影，避免离开归一几何；欧氏直线可能穿球内部。多步计算不必每次重跑全部历史，末层复用缓存是另一独立设计。 例如两个单位向量的中点通常不再单位长度，不能直接当同样球面状态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a33bd2600d866b14">球面流与普通欧氏向量插值有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Axrec">X-Rec Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · TikTok (ByteDance)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>球面路径沿测地线，速度需切空间投影，避免离开归一几何；欧氏直线可能穿球内部。多步计算不必每次重跑全部历史，末层复用缓存是另一独立设计。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个单位向量的中点通常不再单位长度，不能直接当同样球面状态。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.29180">原论文</a> · <a href="../../../../reproductions/2609.29180-xrec/">实现解读</a> · <a href="#qa-a33bd2600d866b14">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:xrec" data-paper-title="X-Rec Technical Report" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="X-Rec Technical Report 搜广推与 LLM 应用 TikTok (ByteDance) 2026-09-24 传统 U2I 召回将用户兴趣压缩为一个或少量向量，生成式语义 ID 方法则要逐 token 解码。X-Rec 直接在归一化 item embedding 球面上生成多个召回触发向量：先预测 item 所在的粗粒度聚类（anchor），再以该 anchor 为条件把球面噪声沿测地线流向目标 item。生成的向量与全量 item embedding 做近邻检索，可覆盖多个兴趣区域而无需语义 ID 量化。论文的另一个重点是计算结构：历史行为先经过前 L-1 层 Transformer； 未执行：TikTok 私有多属性日志与 streaming benchmark、工业 item encoder、ANN/在线 KV 服务、真实线上 A/B。Fidelity：核心机制复现；证据等级：L2 公开数据集。公开 MovieLens 任务只检验算法链路，不代表 TikTok 流量或论文绝对结果。当前是低预算机制实验；在 MovieLens-1M 上，X-Rec 的三种子均值低于 U2I，不能宣称收益。实际执行：item 对比学习、球面 anchor 聚类与 CE、测地线 RFM 监督、末层历史 K/V 复用、时间/anchor 调制、切空间速度、球面 Euler 和多 trigger 全目录检索。  retrieval generative-recommendation flow-matching 搜广推 生成式召回与推理推荐 X-Rec本地有GPU吞吐回执吗，实际执行了什么？ 没有，目前CPU缩比执行anchor、测地RFM、末层KV复用及球面Euler等核心链。未有工业ANN、流式服务和线上A/B，CPU微基准不代表生产吞吐。 例如缓存历史后少算层能验证结构，但不能据此写A100速度提升。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-834265e483da0699">X-Rec本地有GPU吞吐回执吗，实际执行了什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Axrec">X-Rec Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · TikTok (ByteDance)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有，目前CPU缩比执行anchor、测地RFM、末层KV复用及球面Euler等核心链。未有工业ANN、流式服务和线上A/B，CPU微基准不代表生产吞吐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如缓存历史后少算层能验证结构，但不能据此写A100速度提升。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.29180">原论文</a> · <a href="../../../../reproductions/2609.29180-xrec/">实现解读</a> · <a href="#qa-834265e483da0699">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unique" data-paper-title="UNIQUE: A Unified Retrieval and Ranking System for Large-Scale Feed Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="UNIQUE: A Unified Retrieval and Ranking System for Large-Scale Feed Recommendation 搜广推与 LLM 应用 Beihang University 2026-09-20 传统召回与排序分开优化，召回侧较难利用排序反馈；多层残差量化又可能逐层积累误差。UNIQUE 将物品先映射到一个扁平 code：物品向量由用户反馈监督的双塔编码，最近邻分配经使用频率校正，并用 EMA 更新码本。用户静态特征、近期行为、中期行为及兴趣摘要构成前缀；候选 item/code 各自只关注这一前缀，而不读取其他候选。共享的编码结果同时训练 code 分布和多个排序目标，推理时先按 code 提名，再对对应物品排序。 复现级别：公开数据缩比机制实验（概念验证）。复现级别：公开数据缩比机制实验（概念验证）。执行了反馈感知单层扁平量化、EMA 与频率平衡、用户多粒度前缀、目标注意力分离、code 生成与曝光排序联合训练；缺少百度生产特征、多目标头和在线基础设施，不能称为完整论文复现。仅用公开 item ID、标签、点击/长播与播放时长；没有百度的文本、发布者、细粒度反馈和多场景目标头。本地对照口径：同一早融合排序器、同数据和训练预算下，去掉联合 code 生成是基线，三 seed test CTR-AUC 均值约 0.5282；完整缩比实验组约 0.5270，相对 -0.23%。本地没有观察到稳定提升。  retrieval ranking generative-recommendation 搜广推 生成式召回与推理推荐 UNIQUE为什么用一个扁平code而非多级残差SID？ 它试图避免逐层量化误差积累，以反馈双塔表示、频率校正分配及EMA维护单层码，同时训练code召回与多目标排序。扁平不意味着码一定唯一对应物品。 例如一次选语义桶后再排桶内商品，不必生成多级残差路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-unique-d194acb1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c1131a1665add327">UNIQUE为什么用一个扁平code而非多级残差SID？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunique">UNIQUE: A Unified Retrieval and Ranking System for Large-Scale Feed Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它试图避免逐层量化误差积累，以反馈双塔表示、频率校正分配及EMA维护单层码，同时训练code召回与多目标排序。扁平不意味着码一定唯一对应物品。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一次选语义桶后再排桶内商品，不必生成多级残差路径。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.23718">原论文</a> · <a href="../../../../reproductions/2609.23718-unique/">实现解读</a> · <a href="#qa-c1131a1665add327">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unique" data-paper-title="UNIQUE: A Unified Retrieval and Ranking System for Large-Scale Feed Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="UNIQUE: A Unified Retrieval and Ranking System for Large-Scale Feed Recommendation 搜广推与 LLM 应用 Beihang University 2026-09-20 传统召回与排序分开优化，召回侧较难利用排序反馈；多层残差量化又可能逐层积累误差。UNIQUE 将物品先映射到一个扁平 code：物品向量由用户反馈监督的双塔编码，最近邻分配经使用频率校正，并用 EMA 更新码本。用户静态特征、近期行为、中期行为及兴趣摘要构成前缀；候选 item/code 各自只关注这一前缀，而不读取其他候选。共享的编码结果同时训练 code 分布和多个排序目标，推理时先按 code 提名，再对对应物品排序。 复现级别：公开数据缩比机制实验（概念验证）。复现级别：公开数据缩比机制实验（概念验证）。执行了反馈感知单层扁平量化、EMA 与频率平衡、用户多粒度前缀、目标注意力分离、code 生成与曝光排序联合训练；缺少百度生产特征、多目标头和在线基础设施，不能称为完整论文复现。仅用公开 item ID、标签、点击/长播与播放时长；没有百度的文本、发布者、细粒度反馈和多场景目标头。本地对照口径：同一早融合排序器、同数据和训练预算下，去掉联合 code 生成是基线，三 seed test CTR-AUC 均值约 0.5282；完整缩比实验组约 0.5270，相对 -0.23%。本地没有观察到稳定提升。  retrieval ranking generative-recommendation 搜广推 生成式召回与推理推荐 UNIQUE 为什么采用扁平 code，并让候选 item/code 只读取公共前缀而不互读？ 扁平码避免多层残差量化逐层积累误差，反馈双塔、频率校正与 EMA 让分配兼顾行为和码使用。候选各自只读取公共用户前缀，既共享编码又保持候选隔离，联合训练 code 分布与排序目标连接召回和判别。它用较大单层空间换取路径简化，码利用与碰撞问题仍需监测。 示意：同一用户有十个候选，各自读一份共同历史，不读取邻居候选信息。物品先分到单层 code 提名，再对桶内商品排序，避免多层早期量化错误逐级传递。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-340940bae7589d13">UNIQUE 为什么采用扁平 code，并让候选 item/code 只读取公共前缀而不互读？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunique">UNIQUE: A Unified Retrieval and Ranking System for Large-Scale Feed Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>扁平码避免多层残差量化逐层积累误差，反馈双塔、频率校正与 EMA 让分配兼顾行为和码使用。候选各自只读取公共用户前缀，既共享编码又保持候选隔离，联合训练 code 分布与排序目标连接召回和判别。它用较大单层空间换取路径简化，码利用与碰撞问题仍需监测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一用户有十个候选，各自读一份共同历史，不读取邻居候选信息。物品先分到单层 code 提名，再对桶内商品排序，避免多层早期量化错误逐级传递。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.23718">原论文</a> · <a href="../../../../reproductions/2609.23718-unique/">实现解读</a> · <a href="#qa-340940bae7589d13">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unique" data-paper-title="UNIQUE: A Unified Retrieval and Ranking System for Large-Scale Feed Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="UNIQUE: A Unified Retrieval and Ranking System for Large-Scale Feed Recommendation 搜广推与 LLM 应用 Beihang University 2026-09-20 传统召回与排序分开优化，召回侧较难利用排序反馈；多层残差量化又可能逐层积累误差。UNIQUE 将物品先映射到一个扁平 code：物品向量由用户反馈监督的双塔编码，最近邻分配经使用频率校正，并用 EMA 更新码本。用户静态特征、近期行为、中期行为及兴趣摘要构成前缀；候选 item/code 各自只关注这一前缀，而不读取其他候选。共享的编码结果同时训练 code 分布和多个排序目标，推理时先按 code 提名，再对对应物品排序。 复现级别：公开数据缩比机制实验（概念验证）。复现级别：公开数据缩比机制实验（概念验证）。执行了反馈感知单层扁平量化、EMA 与频率平衡、用户多粒度前缀、目标注意力分离、code 生成与曝光排序联合训练；缺少百度生产特征、多目标头和在线基础设施，不能称为完整论文复现。仅用公开 item ID、标签、点击/长播与播放时长；没有百度的文本、发布者、细粒度反馈和多场景目标头。本地对照口径：同一早融合排序器、同数据和训练预算下，去掉联合 code 生成是基线，三 seed test CTR-AUC 均值约 0.5282；完整缩比实验组约 0.5270，相对 -0.23%。本地没有观察到稳定提升。  retrieval ranking generative-recommendation 搜广推 生成式召回与推理推荐 候选只读共享前缀与候选间setwise注意有什么差别？ 前者保持候选互不读取，便于共享用户编码及稳定打分；setwise会让候选集合改变相互表示。统一召回排序并不要求任意候选交互。 例如新增候选不应通过目标间attention改掉旧候选编码。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-3d728475f273bb67">候选只读共享前缀与候选间setwise注意有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunique">UNIQUE: A Unified Retrieval and Ranking System for Large-Scale Feed Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者保持候选互不读取，便于共享用户编码及稳定打分；setwise会让候选集合改变相互表示。统一召回排序并不要求任意候选交互。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如新增候选不应通过目标间attention改掉旧候选编码。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.23718">原论文</a> · <a href="../../../../reproductions/2609.23718-unique/">实现解读</a> · <a href="#qa-3d728475f273bb67">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unique" data-paper-title="UNIQUE: A Unified Retrieval and Ranking System for Large-Scale Feed Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="UNIQUE: A Unified Retrieval and Ranking System for Large-Scale Feed Recommendation 搜广推与 LLM 应用 Beihang University 2026-09-20 传统召回与排序分开优化，召回侧较难利用排序反馈；多层残差量化又可能逐层积累误差。UNIQUE 将物品先映射到一个扁平 code：物品向量由用户反馈监督的双塔编码，最近邻分配经使用频率校正，并用 EMA 更新码本。用户静态特征、近期行为、中期行为及兴趣摘要构成前缀；候选 item/code 各自只关注这一前缀，而不读取其他候选。共享的编码结果同时训练 code 分布和多个排序目标，推理时先按 code 提名，再对对应物品排序。 复现级别：公开数据缩比机制实验（概念验证）。复现级别：公开数据缩比机制实验（概念验证）。执行了反馈感知单层扁平量化、EMA 与频率平衡、用户多粒度前缀、目标注意力分离、code 生成与曝光排序联合训练；缺少百度生产特征、多目标头和在线基础设施，不能称为完整论文复现。仅用公开 item ID、标签、点击/长播与播放时长；没有百度的文本、发布者、细粒度反馈和多场景目标头。本地对照口径：同一早融合排序器、同数据和训练预算下，去掉联合 code 生成是基线，三 seed test CTR-AUC 均值约 0.5282；完整缩比实验组约 0.5270，相对 -0.23%。本地没有观察到稳定提升。  retrieval ranking generative-recommendation 搜广推 生成式召回与推理推荐 UNIQUE的直通量化与高均衡码使用能证明高质量召回吗？ 不能。直通估计让编码器得到梯度，频率校正改善使用，但均衡不等于用户相关。当前三seed仍小规模诊断，未重建工业索引和P99服务，不能外推线上收益。 例如所有桶数量相同，也可能把不相关商品均匀混在一起。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-10e739be835f7cb5">UNIQUE的直通量化与高均衡码使用能证明高质量召回吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunique">UNIQUE: A Unified Retrieval and Ranking System for Large-Scale Feed Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。直通估计让编码器得到梯度，频率校正改善使用，但均衡不等于用户相关。当前三seed仍小规模诊断，未重建工业索引和P99服务，不能外推线上收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如所有桶数量相同，也可能把不相关商品均匀混在一起。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.23718">原论文</a> · <a href="../../../../reproductions/2609.23718-unique/">实现解读</a> · <a href="#qa-10e739be835f7cb5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:angle" data-paper-title="One-Step Retrieval Framework for Real-Time Sponsored Search Ads Using Hierarchical Text Representations" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="One-Step Retrieval Framework for Real-Time Sponsored Search Ads Using Hierarchical Text Representations 搜广推与 LLM 应用 Tencent 2026-09-16 以意图标识×摘要标识组织广告语义层次，用生成、判别和排序联合目标训练，并在请求侧动态约束 beam 只产生合法标识。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地在 MovieLens 100K 执行层次标识、联合打分和受约束检索；不使用腾讯私有广告日志或生产索引。本地在 MovieLens 100K 执行层次标识、联合打分和受约束检索；不使用腾讯私有广告日志或生产索引。本地 seeds 42/43/44 见 metrics/movielens-100k-seeds42-44.json。  sponsored-search generative-retrieval hierarchical-identifiers 搜广推 生成式召回与推理推荐 ANGLE 的“意图标识×摘要标识”为什么是层次输出而不是普通广告 ID？ 意图层组织广告满足的需求，摘要层进一步区分具体语义，生成器可沿层次路径共享信息并缩小选择范围。联合生成、判别与排序目标让路径既可预测又可区分；它仍需映射到实际广告，不能把生成一个合理概念当作已经找到合法投放对象。 示意：先定位“旅行准备”意图，再选“便携收纳”摘要，比把每条广告视作完全无关编号更容易共享知识，但最终仍须落到真实广告。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-angle-c3d4b151" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b36cbacb54bf77e0">ANGLE 的“意图标识×摘要标识”为什么是层次输出而不是普通广告 ID？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aangle">One-Step Retrieval Framework for Real-Time Sponsored Search Ads Using Hierarchical Text Representations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>意图层组织广告满足的需求，摘要层进一步区分具体语义，生成器可沿层次路径共享信息并缩小选择范围。联合生成、判别与排序目标让路径既可预测又可区分；它仍需映射到实际广告，不能把生成一个合理概念当作已经找到合法投放对象。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先定位“旅行准备”意图，再选“便携收纳”摘要，比把每条广告视作完全无关编号更容易共享知识，但最终仍须落到真实广告。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.18296">原论文</a> · <a href="../../../../reproductions/2609.18296-angle/">实现解读</a> · <a href="#qa-b36cbacb54bf77e0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:angle" data-paper-title="One-Step Retrieval Framework for Real-Time Sponsored Search Ads Using Hierarchical Text Representations" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="One-Step Retrieval Framework for Real-Time Sponsored Search Ads Using Hierarchical Text Representations 搜广推与 LLM 应用 Tencent 2026-09-16 以意图标识×摘要标识组织广告语义层次，用生成、判别和排序联合目标训练，并在请求侧动态约束 beam 只产生合法标识。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地在 MovieLens 100K 执行层次标识、联合打分和受约束检索；不使用腾讯私有广告日志或生产索引。本地在 MovieLens 100K 执行层次标识、联合打分和受约束检索；不使用腾讯私有广告日志或生产索引。本地 seeds 42/43/44 见 metrics/movielens-100k-seeds42-44.json。  sponsored-search generative-retrieval hierarchical-identifiers 搜广推 生成式召回与推理推荐 ANGLE有了层次广告标识，为什么解码时还要施加请求侧动态约束？ 标识层次只描述广告的组织方式，不保证每个请求都能投放所有合法组合。请求侧约束将库存、资格等条件落实到beam搜索，使不可服务标识在生成过程中被排除；生成、判别和排序目标再共同训练相关性。先任意生成再事后删掉无效项，可能浪费搜索预算且漏掉可用候选。 示意：同一意图下有多个广告摘要码，其中一项当前不可投；若等生成完再过滤，beam可能已被它占满，动态约束则把预算留给可服务广告。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c4c49ab8f4fbbd8c">ANGLE有了层次广告标识，为什么解码时还要施加请求侧动态约束？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aangle">One-Step Retrieval Framework for Real-Time Sponsored Search Ads Using Hierarchical Text Representations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>标识层次只描述广告的组织方式，不保证每个请求都能投放所有合法组合。请求侧约束将库存、资格等条件落实到beam搜索，使不可服务标识在生成过程中被排除；生成、判别和排序目标再共同训练相关性。先任意生成再事后删掉无效项，可能浪费搜索预算且漏掉可用候选。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一意图下有多个广告摘要码，其中一项当前不可投；若等生成完再过滤，beam可能已被它占满，动态约束则把预算留给可服务广告。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.18296">原论文</a> · <a href="../../../../reproductions/2609.18296-angle/">实现解读</a> · <a href="#qa-c4c49ab8f4fbbd8c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:angle" data-paper-title="One-Step Retrieval Framework for Real-Time Sponsored Search Ads Using Hierarchical Text Representations" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="One-Step Retrieval Framework for Real-Time Sponsored Search Ads Using Hierarchical Text Representations 搜广推与 LLM 应用 Tencent 2026-09-16 以意图标识×摘要标识组织广告语义层次，用生成、判别和排序联合目标训练，并在请求侧动态约束 beam 只产生合法标识。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地在 MovieLens 100K 执行层次标识、联合打分和受约束检索；不使用腾讯私有广告日志或生产索引。本地在 MovieLens 100K 执行层次标识、联合打分和受约束检索；不使用腾讯私有广告日志或生产索引。本地 seeds 42/43/44 见 metrics/movielens-100k-seeds42-44.json。  sponsored-search generative-retrieval hierarchical-identifiers 搜广推 生成式召回与推理推荐 ANGLE 的判别分与生成路径概率联合使用，和只按生成似然选 beam 有何目标区别？ 生成概率描述路径在上下文下多可能，判别信号额外要求层次标识与目标有区分力，排序再连接推荐价值。组合可校正仅靠似然偏好的方向，但权重决定折中，不能因加入判别器就保证所有目标更好；来源本地系数只在验证集选择。 示意：两个路径都常见，生成器偏爱热门摘要；判别分若更支持当前用户的细分需求，可提高另一条路径，但过重权重也可能压过合理的生成先验。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4d08c0ebac8b3d6b">ANGLE 的判别分与生成路径概率联合使用，和只按生成似然选 beam 有何目标区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aangle">One-Step Retrieval Framework for Real-Time Sponsored Search Ads Using Hierarchical Text Representations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>生成概率描述路径在上下文下多可能，判别信号额外要求层次标识与目标有区分力，排序再连接推荐价值。组合可校正仅靠似然偏好的方向，但权重决定折中，不能因加入判别器就保证所有目标更好；来源本地系数只在验证集选择。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个路径都常见，生成器偏爱热门摘要；判别分若更支持当前用户的细分需求，可提高另一条路径，但过重权重也可能压过合理的生成先验。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.18296">原论文</a> · <a href="../../../../reproductions/2609.18296-angle/">实现解读</a> · <a href="#qa-4d08c0ebac8b3d6b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:angle" data-paper-title="One-Step Retrieval Framework for Real-Time Sponsored Search Ads Using Hierarchical Text Representations" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="One-Step Retrieval Framework for Real-Time Sponsored Search Ads Using Hierarchical Text Representations 搜广推与 LLM 应用 Tencent 2026-09-16 以意图标识×摘要标识组织广告语义层次，用生成、判别和排序联合目标训练，并在请求侧动态约束 beam 只产生合法标识。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地在 MovieLens 100K 执行层次标识、联合打分和受约束检索；不使用腾讯私有广告日志或生产索引。本地在 MovieLens 100K 执行层次标识、联合打分和受约束检索；不使用腾讯私有广告日志或生产索引。本地 seeds 42/43/44 见 metrics/movielens-100k-seeds42-44.json。  sponsored-search generative-retrieval hierarchical-identifiers 搜广推 生成式召回与推理推荐 ANGLE 的合法 beam 约束应在生成完成后过滤，还是在每步扩展时应用？ 来源要求请求侧动态约束 beam，扩展时只允许属于当前合法标识集合的路径，避免预算花在最终必被丢弃的广告上。集合应按请求更新，不能用全局词表替代当前资格；本地生成与判别融合系数也必须来自验证而非测试选择。 示意：某地区不能投放的一类广告，在首个相关标识扩展时就屏蔽，比生成十条后发现九条不合法再过滤更能保留有效候选预算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-2c29b4cbdc3fb8c6">ANGLE 的合法 beam 约束应在生成完成后过滤，还是在每步扩展时应用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aangle">One-Step Retrieval Framework for Real-Time Sponsored Search Ads Using Hierarchical Text Representations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>来源要求请求侧动态约束 beam，扩展时只允许属于当前合法标识集合的路径，避免预算花在最终必被丢弃的广告上。集合应按请求更新，不能用全局词表替代当前资格；本地生成与判别融合系数也必须来自验证而非测试选择。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某地区不能投放的一类广告，在首个相关标识扩展时就屏蔽，比生成十条后发现九条不合法再过滤更能保留有效候选预算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.18296">原论文</a> · <a href="../../../../reproductions/2609.18296-angle/">实现解读</a> · <a href="#qa-2c29b4cbdc3fb8c6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tgr" data-paper-title="TGR: Advancing Industrial Recommendation from Generative-Paradigm Ranking toward Unified Generation and Reasoning" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="TGR: Advancing Industrial Recommendation from Generative-Paradigm Ranking toward Unified Generation and Reasoning 搜广推与 LLM 应用 Tencent 2026-09-01 TGR 把工业推荐的三个方向纳入同一框架：CCFormer 承担可扩展排序，BARGE/HiGR 用分层语义 ID 生成单物品或整页列表，TGR-Reason 把离线生成的 reason token 注入在线解码，避免请求时再做昂贵 rollout。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现分层语义 ID 路径、列表目标和 reason-token 注入的组合。未复刻私有 semantic-ID catalog、生产 CCFormer checkpoint 与在线生成服务；仅实现公开数据可审计核心机制。MovieLens 100K 三 seed 固定协议下 NDCG@10 从 0.05401 提升到 0.05953。完整产物见 metrics/public-seeds42-44.json。  generative-recommendation ranking-network reason-token 搜广推 生成式召回与推理推荐 TGR为什么把排序、生成与离线reason一起组织？ 工业链路既要可扩展打分，也要生成候选或列表，还需可控推理成本。不同模块各承担职责，reason离线注入避免请求时额外昂贵rollout，不是单一新attention公式。 例如先准备推理条件，实时模型再生成或排序候选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-tgr-d333ba35" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7bd5864e166f1cb2">TGR为什么把排序、生成与离线reason一起组织？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atgr">TGR: Advancing Industrial Recommendation from Generative-Paradigm Ranking toward Unified Generation and Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>工业链路既要可扩展打分，也要生成候选或列表，还需可控推理成本。不同模块各承担职责，reason离线注入避免请求时额外昂贵rollout，不是单一新attention公式。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先准备推理条件，实时模型再生成或排序候选。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.00986">原论文</a> · <a href="../../../../reproductions/2609.00986-tgr/">实现解读</a> · <a href="#qa-7bd5864e166f1cb2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tgr" data-paper-title="TGR: Advancing Industrial Recommendation from Generative-Paradigm Ranking toward Unified Generation and Reasoning" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="TGR: Advancing Industrial Recommendation from Generative-Paradigm Ranking toward Unified Generation and Reasoning 搜广推与 LLM 应用 Tencent 2026-09-01 TGR 把工业推荐的三个方向纳入同一框架：CCFormer 承担可扩展排序，BARGE/HiGR 用分层语义 ID 生成单物品或整页列表，TGR-Reason 把离线生成的 reason token 注入在线解码，避免请求时再做昂贵 rollout。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现分层语义 ID 路径、列表目标和 reason-token 注入的组合。未复刻私有 semantic-ID catalog、生产 CCFormer checkpoint 与在线生成服务；仅实现公开数据可审计核心机制。MovieLens 100K 三 seed 固定协议下 NDCG@10 从 0.05401 提升到 0.05953。完整产物见 metrics/public-seeds42-44.json。  generative-recommendation ranking-network reason-token 搜广推 生成式召回与推理推荐 TGR 为什么把可扩展排序、分层 SID 生成和离线 reason token 放在同一技术框架？ 排序负责细粒度判别，层级 SID 支持从单物品到整页生成，离线 reason token 则把昂贵推理准备成在线可消费条件。框架连接的是不同阶段的信息与计算，而非用一个新公式取代全部模块。理解时应分别检查生成路径、列表目标和推理接口；本地路径分数实现不能代表所有生产子系统都已重建。 示意：先离线整理用户可能的兴趣理由，生成器据此产生一页候选，再由扩展排序模型判断价值。请求时直接读取准备好的理由 token，不必重新运行长推理搜索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-d75ea81538d30e34">TGR 为什么把可扩展排序、分层 SID 生成和离线 reason token 放在同一技术框架？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atgr">TGR: Advancing Industrial Recommendation from Generative-Paradigm Ranking toward Unified Generation and Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>排序负责细粒度判别，层级 SID 支持从单物品到整页生成，离线 reason token 则把昂贵推理准备成在线可消费条件。框架连接的是不同阶段的信息与计算，而非用一个新公式取代全部模块。理解时应分别检查生成路径、列表目标和推理接口；本地路径分数实现不能代表所有生产子系统都已重建。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先离线整理用户可能的兴趣理由，生成器据此产生一页候选，再由扩展排序模型判断价值。请求时直接读取准备好的理由 token，不必重新运行长推理搜索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.00986">原论文</a> · <a href="../../../../reproductions/2609.00986-tgr/">实现解读</a> · <a href="#qa-d75ea81538d30e34">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tgr" data-paper-title="TGR: Advancing Industrial Recommendation from Generative-Paradigm Ranking toward Unified Generation and Reasoning" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="TGR: Advancing Industrial Recommendation from Generative-Paradigm Ranking toward Unified Generation and Reasoning 搜广推与 LLM 应用 Tencent 2026-09-01 TGR 把工业推荐的三个方向纳入同一框架：CCFormer 承担可扩展排序，BARGE/HiGR 用分层语义 ID 生成单物品或整页列表，TGR-Reason 把离线生成的 reason token 注入在线解码，避免请求时再做昂贵 rollout。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现分层语义 ID 路径、列表目标和 reason-token 注入的组合。未复刻私有 semantic-ID catalog、生产 CCFormer checkpoint 与在线生成服务；仅实现公开数据可审计核心机制。MovieLens 100K 三 seed 固定协议下 NDCG@10 从 0.05401 提升到 0.05953。完整产物见 metrics/public-seeds42-44.json。  generative-recommendation ranking-network reason-token 搜广推 生成式召回与推理推荐 离线reason token与在线实时推理有什么覆盖取舍？ 离线省关键链时延，但可能陈旧且难回应突发上下文；实时更灵活却更贵。二者不能以相同token名当作等效能力，需要看生成条件和更新周期。 例如当天热点改变后，昨天离线reason可能不再贴当前请求。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-29d2f0e011d8ee0d">离线reason token与在线实时推理有什么覆盖取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atgr">TGR: Advancing Industrial Recommendation from Generative-Paradigm Ranking toward Unified Generation and Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>离线省关键链时延，但可能陈旧且难回应突发上下文；实时更灵活却更贵。二者不能以相同token名当作等效能力，需要看生成条件和更新周期。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如当天热点改变后，昨天离线reason可能不再贴当前请求。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.00986">原论文</a> · <a href="../../../../reproductions/2609.00986-tgr/">实现解读</a> · <a href="#qa-29d2f0e011d8ee0d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tgr" data-paper-title="TGR: Advancing Industrial Recommendation from Generative-Paradigm Ranking toward Unified Generation and Reasoning" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="TGR: Advancing Industrial Recommendation from Generative-Paradigm Ranking toward Unified Generation and Reasoning 搜广推与 LLM 应用 Tencent 2026-09-01 TGR 把工业推荐的三个方向纳入同一框架：CCFormer 承担可扩展排序，BARGE/HiGR 用分层语义 ID 生成单物品或整页列表，TGR-Reason 把离线生成的 reason token 注入在线解码，避免请求时再做昂贵 rollout。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现分层语义 ID 路径、列表目标和 reason-token 注入的组合。未复刻私有 semantic-ID catalog、生产 CCFormer checkpoint 与在线生成服务；仅实现公开数据可审计核心机制。MovieLens 100K 三 seed 固定协议下 NDCG@10 从 0.05401 提升到 0.05953。完整产物见 metrics/public-seeds42-44.json。  generative-recommendation ranking-network reason-token 搜广推 生成式召回与推理推荐 TGR本地路径置信累计式是否完整生产CCFormer？ 不是，当前公开核心机制没有私有SID目录、生产检查点或在线生成。层路径概率与列表分需按明示协议对齐，代理融合不能充当真实多模块部署收益。 例如几级码概率累积能算通，不代表整页生成器及精排服务均已搭好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f873bd8a2c7dea0f">TGR本地路径置信累计式是否完整生产CCFormer？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atgr">TGR: Advancing Industrial Recommendation from Generative-Paradigm Ranking toward Unified Generation and Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是，当前公开核心机制没有私有SID目录、生产检查点或在线生成。层路径概率与列表分需按明示协议对齐，代理融合不能充当真实多模块部署收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如几级码概率累积能算通，不代表整页生成器及精排服务均已搭好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.00986">原论文</a> · <a href="../../../../reproductions/2609.00986-tgr/">实现解读</a> · <a href="#qa-f873bd8a2c7dea0f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tagr" data-paper-title="TAGR: Temporally Adaptive Generative Recommendation for Industrial Live-Streaming Advertising" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="TAGR: Temporally Adaptive Generative Recommendation for Industrial Live-Streaming Advertising 搜广推与 LLM 应用 Kuaishou Technology 2026-08-25 直播间内容、商品和反馈高速变化，静态 semantic ID、单一时间尺度历史和离策略偏好优化都会过时。TAGR 在三层适配：LSID 周期刷新语义/协同分配但保持 token 词表稳定；IAG 融合短、中、长期意图；IOPO 间歇执行 on-policy GRPO，并在两次 burst 之间继续 NTP 维护，防止在线 RL 覆盖行为分布。 Fidelity：核心机制复现。本地执行稳定词表的可刷新 LSID、多尺度 intent 与行为/价值双分支；生产在线训练与广告系统未复刻。未使用快手私有日志、在线 reward model、真实 GRPO burst、广告价值标签和实时 serving；本地只验证三个核心适配结构及其在非时变公开数据上的失败边界。本地对照口径：基线为一阶转移与热度融合；实验组加入两级 LSID、三尺度 intent 和有界行为/价值门控。MovieLens-1M 上 NDCG@10 从 0.1123 降至 0.0821（-26.86%），但 head share 从 0.7275 降至 0.1303。  generative-recommendation live-streaming-advertising semantic-id online-rl 搜广推 生成式召回与推理推荐 TAGR为什么同时做LSID、IAG和IOPO三层适配？ 直播内容语义、用户意图和反馈政策都快速变化，动态码、多尺度历史及间歇在线优化分别对应这些漂移。单改一个层次不覆盖其余问题。 例如直播换品、用户本次意图变化与出价价值改变，发生在不同组件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-tagr-4f20f91f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-566653d184f1fc06">TAGR为什么同时做LSID、IAG和IOPO三层适配？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atagr">TAGR: Temporally Adaptive Generative Recommendation for Industrial Live-Streaming Advertising</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直播内容语义、用户意图和反馈政策都快速变化，动态码、多尺度历史及间歇在线优化分别对应这些漂移。单改一个层次不覆盖其余问题。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如直播换品、用户本次意图变化与出价价值改变，发生在不同组件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24034">原论文</a> · <a href="../../../../reproductions/2608.24034-tagr/">实现解读</a> · <a href="#qa-566653d184f1fc06">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tagr" data-paper-title="TAGR: Temporally Adaptive Generative Recommendation for Industrial Live-Streaming Advertising" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="TAGR: Temporally Adaptive Generative Recommendation for Industrial Live-Streaming Advertising 搜广推与 LLM 应用 Kuaishou Technology 2026-08-25 直播间内容、商品和反馈高速变化，静态 semantic ID、单一时间尺度历史和离策略偏好优化都会过时。TAGR 在三层适配：LSID 周期刷新语义/协同分配但保持 token 词表稳定；IAG 融合短、中、长期意图；IOPO 间歇执行 on-policy GRPO，并在两次 burst 之间继续 NTP 维护，防止在线 RL 覆盖行为分布。 Fidelity：核心机制复现。本地执行稳定词表的可刷新 LSID、多尺度 intent 与行为/价值双分支；生产在线训练与广告系统未复刻。未使用快手私有日志、在线 reward model、真实 GRPO burst、广告价值标签和实时 serving；本地只验证三个核心适配结构及其在非时变公开数据上的失败边界。本地对照口径：基线为一阶转移与热度融合；实验组加入两级 LSID、三尺度 intent 和有界行为/价值门控。MovieLens-1M 上 NDCG@10 从 0.1123 降至 0.0821（-26.86%），但 head share 从 0.7275 降至 0.1303。  generative-recommendation live-streaming-advertising semantic-id online-rl 搜广推 生成式召回与推理推荐 TAGR 为什么把直播适应拆成码分配、兴趣时间尺度和间歇式策略更新三层？ 直播内容、用户意图和反馈分布以不同速度变化，只更新一处容易仍受其他过时环节限制。LSID 刷新分配但保持词表接口，IAG 融合短中长期兴趣，IOPO 在 on-policy 更新之间继续 NTP 维护行为分布。三层分别处理物品、用户和策略变化；本地有界门控不等同于完整在线 GRPO 闭环。 示意：直播间突然换商品，用户刚转向新兴趣，旧偏好策略也需校准。只改商品码无法解决后两者；间歇强化学习又配合常规序列训练，避免一次更新忘掉基础分布。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-2515cfaf4e666dc8">TAGR 为什么把直播适应拆成码分配、兴趣时间尺度和间歇式策略更新三层？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atagr">TAGR: Temporally Adaptive Generative Recommendation for Industrial Live-Streaming Advertising</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直播内容、用户意图和反馈分布以不同速度变化，只更新一处容易仍受其他过时环节限制。LSID 刷新分配但保持词表接口，IAG 融合短中长期兴趣，IOPO 在 on-policy 更新之间继续 NTP 维护行为分布。三层分别处理物品、用户和策略变化；本地有界门控不等同于完整在线 GRPO 闭环。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>直播间突然换商品，用户刚转向新兴趣，旧偏好策略也需校准。只改商品码无法解决后两者；间歇强化学习又配合常规序列训练，避免一次更新忘掉基础分布。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24034">原论文</a> · <a href="../../../../reproductions/2608.24034-tagr/">实现解读</a> · <a href="#qa-2515cfaf4e666dc8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tagr" data-paper-title="TAGR: Temporally Adaptive Generative Recommendation for Industrial Live-Streaming Advertising" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="TAGR: Temporally Adaptive Generative Recommendation for Industrial Live-Streaming Advertising 搜广推与 LLM 应用 Kuaishou Technology 2026-08-25 直播间内容、商品和反馈高速变化，静态 semantic ID、单一时间尺度历史和离策略偏好优化都会过时。TAGR 在三层适配：LSID 周期刷新语义/协同分配但保持 token 词表稳定；IAG 融合短、中、长期意图；IOPO 间歇执行 on-policy GRPO，并在两次 burst 之间继续 NTP 维护，防止在线 RL 覆盖行为分布。 Fidelity：核心机制复现。本地执行稳定词表的可刷新 LSID、多尺度 intent 与行为/价值双分支；生产在线训练与广告系统未复刻。未使用快手私有日志、在线 reward model、真实 GRPO burst、广告价值标签和实时 serving；本地只验证三个核心适配结构及其在非时变公开数据上的失败边界。本地对照口径：基线为一阶转移与热度融合；实验组加入两级 LSID、三尺度 intent 和有界行为/价值门控。MovieLens-1M 上 NDCG@10 从 0.1123 降至 0.0821（-26.86%），但 head share 从 0.7275 降至 0.1303。  generative-recommendation live-streaming-advertising semantic-id online-rl 搜广推 生成式召回与推理推荐 LSID保持token词表稳定与冻结item到码映射是一回事吗？ 不是，词表符号可不变但商品分配周期刷新；冻结映射则连路径身份都不改。两种更新语义影响旧模型兼容性，不能把稳定词表写成永不重分配。 例如同一组数字token仍在，但某直播间可能换到另一条码路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-6930136a3fbe6260">LSID保持token词表稳定与冻结item到码映射是一回事吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atagr">TAGR: Temporally Adaptive Generative Recommendation for Industrial Live-Streaming Advertising</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是，词表符号可不变但商品分配周期刷新；冻结映射则连路径身份都不改。两种更新语义影响旧模型兼容性，不能把稳定词表写成永不重分配。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一组数字token仍在，但某直播间可能换到另一条码路径。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24034">原论文</a> · <a href="../../../../reproductions/2608.24034-tagr/">实现解读</a> · <a href="#qa-6930136a3fbe6260">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tagr" data-paper-title="TAGR: Temporally Adaptive Generative Recommendation for Industrial Live-Streaming Advertising" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="TAGR: Temporally Adaptive Generative Recommendation for Industrial Live-Streaming Advertising 搜广推与 LLM 应用 Kuaishou Technology 2026-08-25 直播间内容、商品和反馈高速变化，静态 semantic ID、单一时间尺度历史和离策略偏好优化都会过时。TAGR 在三层适配：LSID 周期刷新语义/协同分配但保持 token 词表稳定；IAG 融合短、中、长期意图；IOPO 间歇执行 on-policy GRPO，并在两次 burst 之间继续 NTP 维护，防止在线 RL 覆盖行为分布。 Fidelity：核心机制复现。本地执行稳定词表的可刷新 LSID、多尺度 intent 与行为/价值双分支；生产在线训练与广告系统未复刻。未使用快手私有日志、在线 reward model、真实 GRPO burst、广告价值标签和实时 serving；本地只验证三个核心适配结构及其在非时变公开数据上的失败边界。本地对照口径：基线为一阶转移与热度融合；实验组加入两级 LSID、三尺度 intent 和有界行为/价值门控。MovieLens-1M 上 NDCG@10 从 0.1123 降至 0.0821（-26.86%），但 head share 从 0.7275 降至 0.1303。  generative-recommendation live-streaming-advertising semantic-id online-rl 搜广推 生成式召回与推理推荐 TAGR本地是否执行真实GRPO burst与NTP间歇维护？ 没有生产在线burst和价值标签，当前只验证适配结构及非时变公开数据失败边界。完整调度需记录采样政策、两类reward和维护版本，不能只加目标名就称已在线。 例如一个静态数据loss相加，不等于按时间真实触发一次GRPO训练服务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d67eba5f33c53c0b">TAGR本地是否执行真实GRPO burst与NTP间歇维护？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atagr">TAGR: Temporally Adaptive Generative Recommendation for Industrial Live-Streaming Advertising</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有生产在线burst和价值标签，当前只验证适配结构及非时变公开数据失败边界。完整调度需记录采样政策、两类reward和维护版本，不能只加目标名就称已在线。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个静态数据loss相加，不等于按时间真实触发一次GRPO训练服务。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24034">原论文</a> · <a href="../../../../reproductions/2608.24034-tagr/">实现解读</a> · <a href="#qa-d67eba5f33c53c0b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sona" data-paper-title="Sona Technical Report" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Sona Technical Report 搜广推与 LLM 应用 Yandex 2026-08-11 Yandex Music 原链路有 15 个以上候选生成器与独立预排、精排。Sona 用 chronology event encoder 表示用户，以历史压缩控制长序列成本，自回归生成 Semantic ID，并用同一状态的 Ranking Module 对物品排序；高容量 teacher 只在训练期提供蒸馏监督。 Fidelity：核心机制复现。实际训练压缩历史编码器、三层自回归 Semantic ID 头与 item ranker；本地负迁移如实保留。未复刻私有音乐语义 tokenizer、完整 teacher、15+ 生产候选源和智能音箱 serving；本地仅验证核心训练与推理数据流。本地对照口径：基线为同预算共享 encoder 排序器，实验组为 history compression + SID decoder + item ranker；NDCG@10 相对变化 -92.05%。  generative-recommendation semantic-id ranking history-compression 搜广推 生成式召回与推理推荐 Sona为什么同时有SID生成器与Ranking Module？ 同一用户状态支持候选生成和精细排序，希望减少多级独立模型的重复表征；高容量教师仅训练期指导，线上以单一服务模型完成链路。 例如先由状态生成一批音乐，再用同状态评具体歌曲。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-sona-74c5ab5b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-db84c085c9995808">Sona为什么同时有SID生成器与Ranking Module？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asona">Sona Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Yandex</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一用户状态支持候选生成和精细排序，希望减少多级独立模型的重复表征；高容量教师仅训练期指导，线上以单一服务模型完成链路。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先由状态生成一批音乐，再用同状态评具体歌曲。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.11015">原论文</a> · <a href="../../../../reproductions/2608.11015-sona/">实现解读</a> · <a href="#qa-db84c085c9995808">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sona" data-paper-title="Sona Technical Report" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Sona Technical Report 搜广推与 LLM 应用 Yandex 2026-08-11 Yandex Music 原链路有 15 个以上候选生成器与独立预排、精排。Sona 用 chronology event encoder 表示用户，以历史压缩控制长序列成本，自回归生成 Semantic ID，并用同一状态的 Ranking Module 对物品排序；高容量 teacher 只在训练期提供蒸馏监督。 Fidelity：核心机制复现。实际训练压缩历史编码器、三层自回归 Semantic ID 头与 item ranker；本地负迁移如实保留。未复刻私有音乐语义 tokenizer、完整 teacher、15+ 生产候选源和智能音箱 serving；本地仅验证核心训练与推理数据流。本地对照口径：基线为同预算共享 encoder 排序器，实验组为 history compression + SID decoder + item ranker；NDCG@10 相对变化 -92.05%。  generative-recommendation semantic-id ranking history-compression 搜广推 生成式召回与推理推荐 Sona 为什么让 SID 生成与排序模块共享用户状态，并只在训练期使用高容量 teacher？ 独立候选生成器与排序器会重复理解历史，也容易优化不同表示。Sona 用按时间编码并压缩的同一状态支持生成与物品排序，联合目标连接两条路径；教师只在训练期提供额外监督，服务保持较轻结构。共享状态不消除生成漏召问题，历史压缩也有损失，本地负结果不能用生产统一架构的描述覆盖。 示意：用户最近转听古典乐，生成器和排序头都读取同一更新后的状态，避免一边还按旧摇滚偏好召回。大教师训练时指导表示，上线无需为每次请求调用它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-d656f31a07458ede">Sona 为什么让 SID 生成与排序模块共享用户状态，并只在训练期使用高容量 teacher？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asona">Sona Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Yandex</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立候选生成器与排序器会重复理解历史，也容易优化不同表示。Sona 用按时间编码并压缩的同一状态支持生成与物品排序，联合目标连接两条路径；教师只在训练期提供额外监督，服务保持较轻结构。共享状态不消除生成漏召问题，历史压缩也有损失，本地负结果不能用生产统一架构的描述覆盖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户最近转听古典乐，生成器和排序头都读取同一更新后的状态，避免一边还按旧摇滚偏好召回。大教师训练时指导表示，上线无需为每次请求调用它。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.11015">原论文</a> · <a href="../../../../reproductions/2608.11015-sona/">实现解读</a> · <a href="#qa-d656f31a07458ede">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sona" data-paper-title="Sona Technical Report" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Sona Technical Report 搜广推与 LLM 应用 Yandex 2026-08-11 Yandex Music 原链路有 15 个以上候选生成器与独立预排、精排。Sona 用 chronology event encoder 表示用户，以历史压缩控制长序列成本，自回归生成 Semantic ID，并用同一状态的 Ranking Module 对物品排序；高容量 teacher 只在训练期提供蒸馏监督。 Fidelity：核心机制复现。实际训练压缩历史编码器、三层自回归 Semantic ID 头与 item ranker；本地负迁移如实保留。未复刻私有音乐语义 tokenizer、完整 teacher、15+ 生产候选源和智能音箱 serving；本地仅验证核心训练与推理数据流。本地对照口径：基线为同预算共享 encoder 排序器，实验组为 history compression + SID decoder + item ranker；NDCG@10 相对变化 -92.05%。  generative-recommendation semantic-id ranking history-compression 搜广推 生成式召回与推理推荐 单模型替换级联与简单删除中间排序器有何不同？ 需联合学习生成、排序及蒸馏目标，并控制长历史，不是把原模型少跑几层。多源级联带来的覆盖和鲁棒性也需替代评估，不能只按模型数少就判更好。 例如删掉预排但未训练联合模型，可能只是丢掉功能而非统一。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f12020c85502e7d7">单模型替换级联与简单删除中间排序器有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asona">Sona Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Yandex</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>需联合学习生成、排序及蒸馏目标，并控制长历史，不是把原模型少跑几层。多源级联带来的覆盖和鲁棒性也需替代评估，不能只按模型数少就判更好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如删掉预排但未训练联合模型，可能只是丢掉功能而非统一。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.11015">原论文</a> · <a href="../../../../reproductions/2608.11015-sona/">实现解读</a> · <a href="#qa-f12020c85502e7d7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sona" data-paper-title="Sona Technical Report" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Sona Technical Report 搜广推与 LLM 应用 Yandex 2026-08-11 Yandex Music 原链路有 15 个以上候选生成器与独立预排、精排。Sona 用 chronology event encoder 表示用户，以历史压缩控制长序列成本，自回归生成 Semantic ID，并用同一状态的 Ranking Module 对物品排序；高容量 teacher 只在训练期提供蒸馏监督。 Fidelity：核心机制复现。实际训练压缩历史编码器、三层自回归 Semantic ID 头与 item ranker；本地负迁移如实保留。未复刻私有音乐语义 tokenizer、完整 teacher、15+ 生产候选源和智能音箱 serving；本地仅验证核心训练与推理数据流。本地对照口径：基线为同预算共享 encoder 排序器，实验组为 history compression + SID decoder + item ranker；NDCG@10 相对变化 -92.05%。  generative-recommendation semantic-id ranking history-compression 搜广推 生成式召回与推理推荐 Sona教师在在线推荐时还需要被调用吗？ 原设定教师训练期使用，线上不依赖它；本地未复刻完整教师、音乐tokenizer和十五余源生产链。生成与排序loss需共享状态且各目标mask清楚。 例如在线仍同时调用大teacher，就改变了单模型服务成本条件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d8da9beed55e2ba5">Sona教师在在线推荐时还需要被调用吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asona">Sona Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Yandex</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原设定教师训练期使用，线上不依赖它；本地未复刻完整教师、音乐tokenizer和十五余源生产链。生成与排序loss需共享状态且各目标mask清楚。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如在线仍同时调用大teacher，就改变了单模型服务成本条件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.11015">原论文</a> · <a href="../../../../reproductions/2608.11015-sona/">实现解读</a> · <a href="#qa-d8da9beed55e2ba5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pushdualgen" data-paper-title="PushDualGen: Enabling LLMs to Generate Semantic IDs with Interpretable Copy for Industrial Push Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="PushDualGen: Enabling LLMs to Generate Semantic IDs with Interpretable Copy for Industrial Push Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-08-08 先生成可服务的 Semantic ID，再按需生成可跳过的解释 copy；在线侧融合 SID 与 copy 表示，同时保留解释一致性。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation semantic-id llm-recommendation push 搜广推 生成式召回与推理推荐 PushDualGen 的 SID 合法时，解释 copy 就一定正确吗？ 不一定。SID 合法只说明推荐对象能映射到可服务目录，copy 还需忠于该对象的事实、匹配用户证据且不夸大。身份正确和解释可信是不同判据，二者应分别校验；不能用目录命中替代文案一致性，也不能用动听理由掩盖选错商品。 示意：确实选中了普通跑鞋，但文案声称它能防火，目录校验仍可通过，事实校验却应拒绝；推荐身份与说明质量不能只测一个。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-pushdualgen-379bfcda" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8086dc0e4ed1344b">PushDualGen 的 SID 合法时，解释 copy 就一定正确吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apushdualgen">PushDualGen: Enabling LLMs to Generate Semantic IDs with Interpretable Copy for Industrial Push Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不一定。SID 合法只说明推荐对象能映射到可服务目录，copy 还需忠于该对象的事实、匹配用户证据且不夸大。身份正确和解释可信是不同判据，二者应分别校验；不能用目录命中替代文案一致性，也不能用动听理由掩盖选错商品。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>确实选中了普通跑鞋，但文案声称它能防火，目录校验仍可通过，事实校验却应拒绝；推荐身份与说明质量不能只测一个。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.07989">原论文</a> · <a href="../../../../reproductions/2608.07989-pushdualgen/">实现解读</a> · <a href="#qa-8086dc0e4ed1344b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pushdualgen" data-paper-title="PushDualGen: Enabling LLMs to Generate Semantic IDs with Interpretable Copy for Industrial Push Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="PushDualGen: Enabling LLMs to Generate Semantic IDs with Interpretable Copy for Industrial Push Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-08-08 先生成可服务的 Semantic ID，再按需生成可跳过的解释 copy；在线侧融合 SID 与 copy 表示，同时保留解释一致性。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation semantic-id llm-recommendation push 搜广推 生成式召回与推理推荐 PushDualGen 为什么先生成可服务 SID，再按门控决定是否继续生成解释文案？ SID 是实际推荐对象的稳定接口，先生成它可让候选即刻进入服务链路；解释以 SID 和历史为条件，只在需要时额外生成，避免所有请求都承担长文本成本。融合两侧表示并约束一致性，意在让文案围绕已选对象，而不是文案和商品各说各话；跳过文案时推荐路径仍需独立可用。 示意：用户只需要普通推荐时，生成商品码便返回；推送通知需要一句理由时，再围绕同一码生成文案。这样不能把“推荐跑鞋”配上“这本小说适合你”的解释。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-2ef9c408f3412728">PushDualGen 为什么先生成可服务 SID，再按门控决定是否继续生成解释文案？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apushdualgen">PushDualGen: Enabling LLMs to Generate Semantic IDs with Interpretable Copy for Industrial Push Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>SID 是实际推荐对象的稳定接口，先生成它可让候选即刻进入服务链路；解释以 SID 和历史为条件，只在需要时额外生成，避免所有请求都承担长文本成本。融合两侧表示并约束一致性，意在让文案围绕已选对象，而不是文案和商品各说各话；跳过文案时推荐路径仍需独立可用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户只需要普通推荐时，生成商品码便返回；推送通知需要一句理由时，再围绕同一码生成文案。这样不能把“推荐跑鞋”配上“这本小说适合你”的解释。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.07989">原论文</a> · <a href="../../../../reproductions/2608.07989-pushdualgen/">实现解读</a> · <a href="#qa-2ef9c408f3412728">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pushdualgen" data-paper-title="PushDualGen: Enabling LLMs to Generate Semantic IDs with Interpretable Copy for Industrial Push Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="PushDualGen: Enabling LLMs to Generate Semantic IDs with Interpretable Copy for Industrial Push Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-08-08 先生成可服务的 Semantic ID，再按需生成可跳过的解释 copy；在线侧融合 SID 与 copy 表示，同时保留解释一致性。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation semantic-id llm-recommendation push 搜广推 生成式召回与推理推荐 按需生成 copy 与所有请求都生成完整解释，相比预算和覆盖怎样取舍？ 门控把额外解码留给需要理由的场景，普通排序可只走 SID，降低平均成本；某些用户可能因此缺少有帮助解释，门控质量需检验。两模式评分和缓存也要有一致契约，不能用无文案延迟搭配有文案效果冒充同一路径。 示意：普通 feed 只返回商品，推送通知再生成一句理由；若统计速度用前者、统计点击用后者，应明确是两种服务模式。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-964d9882edb789a4">按需生成 copy 与所有请求都生成完整解释，相比预算和覆盖怎样取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apushdualgen">PushDualGen: Enabling LLMs to Generate Semantic IDs with Interpretable Copy for Industrial Push Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>门控把额外解码留给需要理由的场景，普通排序可只走 SID，降低平均成本；某些用户可能因此缺少有帮助解释，门控质量需检验。两模式评分和缓存也要有一致契约，不能用无文案延迟搭配有文案效果冒充同一路径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>普通 feed 只返回商品，推送通知再生成一句理由；若统计速度用前者、统计点击用后者，应明确是两种服务模式。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.07989">原论文</a> · <a href="../../../../reproductions/2608.07989-pushdualgen/">实现解读</a> · <a href="#qa-964d9882edb789a4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pushdualgen" data-paper-title="PushDualGen: Enabling LLMs to Generate Semantic IDs with Interpretable Copy for Industrial Push Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="PushDualGen: Enabling LLMs to Generate Semantic IDs with Interpretable Copy for Industrial Push Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-08-08 先生成可服务的 Semantic ID，再按需生成可跳过的解释 copy；在线侧融合 SID 与 copy 表示，同时保留解释一致性。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation semantic-id llm-recommendation push 搜广推 生成式召回与推理推荐 PushDualGen 在 g=0 时，为什么 copy 相关张量与损失也要有清楚处理？ 跳过分支不应再要求未生成 copy 作为必需特征，训练需定义有效 mask 与回退表示；g=1 时 copy 以同一 SID 和历史条件生成。固定 placeholder 不能被当真实解释评价。来源本地核心 scorer 并不证明完整在线文案生成链路。 示意：未生成理由时用零向量可以是定义的缺失路径，但不能将零向量解码成一句默认赞美再称个性化 copy 已通过一致性检查。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-5368a0a2adb74791">PushDualGen 在 g=0 时，为什么 copy 相关张量与损失也要有清楚处理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apushdualgen">PushDualGen: Enabling LLMs to Generate Semantic IDs with Interpretable Copy for Industrial Push Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>跳过分支不应再要求未生成 copy 作为必需特征，训练需定义有效 mask 与回退表示；g=1 时 copy 以同一 SID 和历史条件生成。固定 placeholder 不能被当真实解释评价。来源本地核心 scorer 并不证明完整在线文案生成链路。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>未生成理由时用零向量可以是定义的缺失路径，但不能将零向量解码成一句默认赞美再称个性化 copy 已通过一致性检查。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.07989">原论文</a> · <a href="../../../../reproductions/2608.07989-pushdualgen/">实现解读</a> · <a href="#qa-5368a0a2adb74791">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gryphon-v2" data-paper-title="Gryphon-v2: One Model in Place of a Cascade — Generate-and-Rank Recommender with Rollout Distillation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Gryphon-v2: One Model in Place of a Cascade — Generate-and-Rank Recommender with Rollout Distillation 搜广推与 LLM 应用 Yandex 2026-08-06 Yandex 原系统包含 15 个以上召回器和独立预排/排序。Gryphon-v2 复用生成式推荐的共享 history encoder：生成头预测 Semantic ID，item-level ranking head 对生成候选直接排序；离线高容量 teacher 同时监督当前模型 rollout 和 logged impressions，从而让排序器见到 serving 分布与真实曝光分布。 Fidelity：核心机制复现。实现共享历史编码器、生成头、训练期 teacher、双来源 rollout 蒸馏与 item-level ranker；本地负结果如实保留。未复刻 Yandex 私有音乐/多模态 SID、8,000 长历史、十分钟在线更新和 Triton serving；公开数据只验证核心训练数据流。本地对照口径：基线为同预算生成式召回，实验组加入双来源蒸馏与 ranker；相对基线 NDCG@10 -26.84%。  generative-recommendation retrieval ranking rollout-distillation 搜广推 生成式召回与推理推荐 Gryphon-v2 为什么让生成头与 ranking head 共用 history encoder？ 两阶段反复编码相同历史既浪费计算，也可能形成不同用户状态。共享 encoder 同时支持 SID 提名与 item 排序，连接服务信息。排序头仍面对生成候选分布，不能仅凭共享就假定任务一致，也不代表生成漏掉的物品能被末端补回。 示意：用户刚转听爵士，两头读取同一最新状态，避免召回仍按摇滚而排序已按爵士；但未召回的爵士内容仍无从重排。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-gryphon-v2-65508cc1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a1a741eb904c4131">Gryphon-v2 为什么让生成头与 ranking head 共用 history encoder？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agryphon-v2">Gryphon-v2: One Model in Place of a Cascade — Generate-and-Rank Recommender with Rollout Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Yandex</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两阶段反复编码相同历史既浪费计算，也可能形成不同用户状态。共享 encoder 同时支持 SID 提名与 item 排序，连接服务信息。排序头仍面对生成候选分布，不能仅凭共享就假定任务一致，也不代表生成漏掉的物品能被末端补回。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户刚转听爵士，两头读取同一最新状态，避免召回仍按摇滚而排序已按爵士；但未召回的爵士内容仍无从重排。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06213">原论文</a> · <a href="../../../../reproductions/2608.06213-gryphon-v2/">实现解读</a> · <a href="#qa-a1a741eb904c4131">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gryphon-v2" data-paper-title="Gryphon-v2: One Model in Place of a Cascade — Generate-and-Rank Recommender with Rollout Distillation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Gryphon-v2: One Model in Place of a Cascade — Generate-and-Rank Recommender with Rollout Distillation 搜广推与 LLM 应用 Yandex 2026-08-06 Yandex 原系统包含 15 个以上召回器和独立预排/排序。Gryphon-v2 复用生成式推荐的共享 history encoder：生成头预测 Semantic ID，item-level ranking head 对生成候选直接排序；离线高容量 teacher 同时监督当前模型 rollout 和 logged impressions，从而让排序器见到 serving 分布与真实曝光分布。 Fidelity：核心机制复现。实现共享历史编码器、生成头、训练期 teacher、双来源 rollout 蒸馏与 item-level ranker；本地负结果如实保留。未复刻 Yandex 私有音乐/多模态 SID、8,000 长历史、十分钟在线更新和 Triton serving；公开数据只验证核心训练数据流。本地对照口径：基线为同预算生成式召回，实验组加入双来源蒸馏与 ranker；相对基线 NDCG@10 -26.84%。  generative-recommendation retrieval ranking rollout-distillation 搜广推 生成式召回与推理推荐 Gryphon-v2为什么同时蒸馏当前rollout候选和真实曝光候选？ 生成器改变后会产生日志中少见的候选，排序器若只学习旧曝光分布，就可能无法评价实际服务输出；只学当前rollout又会丢掉真实系统的成熟覆盖。双来源蒸馏让同一teacher同时校准两类候选，再通过共享encoder连接生成与排序。teacher偏差仍会传递，双数据源不等于自动消除分布错位。 示意：新生成器开始提出冷门电影，旧曝光日志只含热门片；rollout提供新候选判断，真实曝光保留既有经验，避免排序头只认识其中一种。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-68390dcde3890556">Gryphon-v2为什么同时蒸馏当前rollout候选和真实曝光候选？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agryphon-v2">Gryphon-v2: One Model in Place of a Cascade — Generate-and-Rank Recommender with Rollout Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Yandex</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>生成器改变后会产生日志中少见的候选，排序器若只学习旧曝光分布，就可能无法评价实际服务输出；只学当前rollout又会丢掉真实系统的成熟覆盖。双来源蒸馏让同一teacher同时校准两类候选，再通过共享encoder连接生成与排序。teacher偏差仍会传递，双数据源不等于自动消除分布错位。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新生成器开始提出冷门电影，旧曝光日志只含热门片；rollout提供新候选判断，真实曝光保留既有经验，避免排序头只认识其中一种。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06213">原论文</a> · <a href="../../../../reproductions/2608.06213-gryphon-v2/">实现解读</a> · <a href="#qa-68390dcde3890556">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gryphon-v2" data-paper-title="Gryphon-v2: One Model in Place of a Cascade — Generate-and-Rank Recommender with Rollout Distillation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Gryphon-v2: One Model in Place of a Cascade — Generate-and-Rank Recommender with Rollout Distillation 搜广推与 LLM 应用 Yandex 2026-08-06 Yandex 原系统包含 15 个以上召回器和独立预排/排序。Gryphon-v2 复用生成式推荐的共享 history encoder：生成头预测 Semantic ID，item-level ranking head 对生成候选直接排序；离线高容量 teacher 同时监督当前模型 rollout 和 logged impressions，从而让排序器见到 serving 分布与真实曝光分布。 Fidelity：核心机制复现。实现共享历史编码器、生成头、训练期 teacher、双来源 rollout 蒸馏与 item-level ranker；本地负结果如实保留。未复刻 Yandex 私有音乐/多模态 SID、8,000 长历史、十分钟在线更新和 Triton serving；公开数据只验证核心训练数据流。本地对照口径：基线为同预算生成式召回，实验组加入双来源蒸馏与 ranker；相对基线 NDCG@10 -26.84%。  generative-recommendation retrieval ranking rollout-distillation 搜广推 生成式召回与推理推荐 双来源蒸馏与只用 logged impressions，相比为何更贴近生成候选服务？ 曝光日志由旧系统选择，当前生成器 rollout 可能覆盖不同区域；同时监督两者可让排序头既看到真实反馈分布，也适应自身候选。teacher 在新区域仍可能不可靠，不能因覆盖变宽就宣称迁移成功，来源本地实际为负。 示意：生成器开始提名冷门器乐，旧曝光几乎没有；只学旧日志的 ranker 可能不会评它，rollout 蒸馏补机会但也可能继承教师偏见。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-98e08b58f6a6ac4b">双来源蒸馏与只用 logged impressions，相比为何更贴近生成候选服务？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agryphon-v2">Gryphon-v2: One Model in Place of a Cascade — Generate-and-Rank Recommender with Rollout Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Yandex</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>曝光日志由旧系统选择，当前生成器 rollout 可能覆盖不同区域；同时监督两者可让排序头既看到真实反馈分布，也适应自身候选。teacher 在新区域仍可能不可靠，不能因覆盖变宽就宣称迁移成功，来源本地实际为负。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>生成器开始提名冷门器乐，旧曝光几乎没有；只学旧日志的 ranker 可能不会评它，rollout 蒸馏补机会但也可能继承教师偏见。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06213">原论文</a> · <a href="../../../../reproductions/2608.06213-gryphon-v2/">实现解读</a> · <a href="#qa-98e08b58f6a6ac4b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gryphon-v2" data-paper-title="Gryphon-v2: One Model in Place of a Cascade — Generate-and-Rank Recommender with Rollout Distillation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Gryphon-v2: One Model in Place of a Cascade — Generate-and-Rank Recommender with Rollout Distillation 搜广推与 LLM 应用 Yandex 2026-08-06 Yandex 原系统包含 15 个以上召回器和独立预排/排序。Gryphon-v2 复用生成式推荐的共享 history encoder：生成头预测 Semantic ID，item-level ranking head 对生成候选直接排序；离线高容量 teacher 同时监督当前模型 rollout 和 logged impressions，从而让排序器见到 serving 分布与真实曝光分布。 Fidelity：核心机制复现。实现共享历史编码器、生成头、训练期 teacher、双来源 rollout 蒸馏与 item-level ranker；本地负结果如实保留。未复刻 Yandex 私有音乐/多模态 SID、8,000 长历史、十分钟在线更新和 Triton serving；公开数据只验证核心训练数据流。本地对照口径：基线为同预算生成式召回，实验组加入双来源蒸馏与 ranker；相对基线 NDCG@10 -26.84%。  generative-recommendation retrieval ranking rollout-distillation 搜广推 生成式召回与推理推荐 Gryphon-v2 的 rollout 与 impression 蒸馏目标为什么要分源记录？ 两源采样分布不同，数量、权重与实际候选身份影响 loss，合并无标记会隐藏哪边主导。teacher 与 student 应对同一 item 比较，训练截止一致；来源本地确有两类目标更新但质量退化，更新次数不是收益证据。 示意：六万次生成候选蒸馏不等于六万次真实曝光，若把两者都标成用户点击，就会错误解释监督可信度与评估结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-66abe065a27702a3">Gryphon-v2 的 rollout 与 impression 蒸馏目标为什么要分源记录？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agryphon-v2">Gryphon-v2: One Model in Place of a Cascade — Generate-and-Rank Recommender with Rollout Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Yandex</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两源采样分布不同，数量、权重与实际候选身份影响 loss，合并无标记会隐藏哪边主导。teacher 与 student 应对同一 item 比较，训练截止一致；来源本地确有两类目标更新但质量退化，更新次数不是收益证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>六万次生成候选蒸馏不等于六万次真实曝光，若把两者都标成用户点击，就会错误解释监督可信度与评估结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06213">原论文</a> · <a href="../../../../reproductions/2608.06213-gryphon-v2/">实现解读</a> · <a href="#qa-66abe065a27702a3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hrpo" data-paper-title="Hierarchical Residual Policy Optimization for Generative Recommendations" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Hierarchical Residual Policy Optimization for Generative Recommendations 搜广推与 LLM 应用 City University of Hong Kong / Kuaishou 2026-08-01 主题：生成式推荐后训练。最终物品回报直接广播给所有 SID token 会造成稀疏且高方差的信用。HRPO 在用户簇内平滑 prefix utility，再分解 residual token credit 并累积 credit-to-go，最后用 RRPO 做保守更新。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。MovieLens-1M 上构造二进制层级 SID，实际计算 prefix smoothing、residual credit 与 credit-to-go。  generative-recommendation reinforcement-learning semantic-id credit-assignment 搜广推 生成式召回与推理推荐 HRPO 为什么把前缀效用分解为 residual credit？ 最终物品奖励很稀疏，所有 SID token 同收一分难区分哪步贡献。前缀效用差给出新增码的边际信用，再累积后续 credit-to-go，让早期决策接受其后续影响。平滑依赖用户簇与估计质量，差分不是直接观测到的因果贡献。 示意：首层选对户外、次层偏到无关装饰，差分可把两步区分，不再让所有码因最终失败一律接受完全相同反馈。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-hrpo-d54751e8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-957dac4052db66ef">HRPO 为什么把前缀效用分解为 residual credit？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahrpo">Hierarchical Residual Policy Optimization for Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · City University of Hong Kong / Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最终物品奖励很稀疏，所有 SID token 同收一分难区分哪步贡献。前缀效用差给出新增码的边际信用，再累积后续 credit-to-go，让早期决策接受其后续影响。平滑依赖用户簇与估计质量，差分不是直接观测到的因果贡献。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>首层选对户外、次层偏到无关装饰，差分可把两步区分，不再让所有码因最终失败一律接受完全相同反馈。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.00750">原论文</a> · <a href="../../../../reproductions/2608.00750-hrpo/">实现解读</a> · <a href="#qa-957dac4052db66ef">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hrpo" data-paper-title="Hierarchical Residual Policy Optimization for Generative Recommendations" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Hierarchical Residual Policy Optimization for Generative Recommendations 搜广推与 LLM 应用 City University of Hong Kong / Kuaishou 2026-08-01 主题：生成式推荐后训练。最终物品回报直接广播给所有 SID token 会造成稀疏且高方差的信用。HRPO 在用户簇内平滑 prefix utility，再分解 residual token credit 并累积 credit-to-go，最后用 RRPO 做保守更新。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。MovieLens-1M 上构造二进制层级 SID，实际计算 prefix smoothing、residual credit 与 credit-to-go。  generative-recommendation reinforcement-learning semantic-id credit-assignment 搜广推 生成式召回与推理推荐 HRPO为什么把最终回报拆成prefix residual credit和credit-to-go？ 整件物品的奖励广播到每枚SID token，会让不同决策承担相同责任并增加方差。HRPO先在用户簇内平滑前缀效用，再用相邻前缀的增量形成局部信用，累积后续影响帮助早期决策学习长期贡献。前缀价值是估计量，分解并不自动消除偏差，也不能在推理时读取真实目标路径。 示意：第一层选错品类可能决定整条路径失败，末层只是在类内微调；把相同奖励平分给所有码，难以区分这两种作用，前缀信用尝试定位差异。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-d24dff680526ea54">HRPO为什么把最终回报拆成prefix residual credit和credit-to-go？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahrpo">Hierarchical Residual Policy Optimization for Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · City University of Hong Kong / Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>整件物品的奖励广播到每枚SID token，会让不同决策承担相同责任并增加方差。HRPO先在用户簇内平滑前缀效用，再用相邻前缀的增量形成局部信用，累积后续影响帮助早期决策学习长期贡献。前缀价值是估计量，分解并不自动消除偏差，也不能在推理时读取真实目标路径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第一层选错品类可能决定整条路径失败，末层只是在类内微调；把相同奖励平分给所有码，难以区分这两种作用，前缀信用尝试定位差异。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.00750">原论文</a> · <a href="../../../../reproductions/2608.00750-hrpo/">实现解读</a> · <a href="#qa-d24dff680526ea54">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hrpo" data-paper-title="Hierarchical Residual Policy Optimization for Generative Recommendations" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Hierarchical Residual Policy Optimization for Generative Recommendations 搜广推与 LLM 应用 City University of Hong Kong / Kuaishou 2026-08-01 主题：生成式推荐后训练。最终物品回报直接广播给所有 SID token 会造成稀疏且高方差的信用。HRPO 在用户簇内平滑 prefix utility，再分解 residual token credit 并累积 credit-to-go，最后用 RRPO 做保守更新。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。MovieLens-1M 上构造二进制层级 SID，实际计算 prefix smoothing、residual credit 与 credit-to-go。  generative-recommendation reinforcement-learning semantic-id credit-assignment 搜广推 生成式召回与推理推荐 HRPO 的 credit-to-go 与每个 token 只使用自身 δ，有什么未来归因差别？ 只用本步差分忽略早期选择如何限制后续，credit-to-go 汇总从本步到终点的残差信用，保留长期后果。它也可能累积估计噪声，RRPO 用保守更新限制偏移。机制不能推出方差一定降低或原目标梯度必然无偏，需按具体推导验证。 示意：早期选“相机”让后续优质镜头可达，收益不只在第一层立即出现；累积后续信用让早层看到这份影响，但错误效用也会传回。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1fdb54974977027f">HRPO 的 credit-to-go 与每个 token 只使用自身 δ，有什么未来归因差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahrpo">Hierarchical Residual Policy Optimization for Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · City University of Hong Kong / Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只用本步差分忽略早期选择如何限制后续，credit-to-go 汇总从本步到终点的残差信用，保留长期后果。它也可能累积估计噪声，RRPO 用保守更新限制偏移。机制不能推出方差一定降低或原目标梯度必然无偏，需按具体推导验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>早期选“相机”让后续优质镜头可达，收益不只在第一层立即出现；累积后续信用让早层看到这份影响，但错误效用也会传回。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.00750">原论文</a> · <a href="../../../../reproductions/2608.00750-hrpo/">实现解读</a> · <a href="#qa-1fdb54974977027f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hrpo" data-paper-title="Hierarchical Residual Policy Optimization for Generative Recommendations" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Hierarchical Residual Policy Optimization for Generative Recommendations 搜广推与 LLM 应用 City University of Hong Kong / Kuaishou 2026-08-01 主题：生成式推荐后训练。最终物品回报直接广播给所有 SID token 会造成稀疏且高方差的信用。HRPO 在用户簇内平滑 prefix utility，再分解 residual token credit 并累积 credit-to-go，最后用 RRPO 做保守更新。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。MovieLens-1M 上构造二进制层级 SID，实际计算 prefix smoothing、residual credit 与 credit-to-go。  generative-recommendation reinforcement-learning semantic-id credit-assignment 搜广推 生成式召回与推理推荐 HRPO 的前缀差分如何做一个基本 telescoping 自检？ 相邻 δt 应使用同一效用版本，求和可还原终前缀与空前缀效用差，credit-to-go 从当前位置累加而非从开头。用户簇平滑不能混入测试未来反馈。本地二进制 SID 只验证这一有界机制，不是大规模生成后训练效果。 示意：三个前缀效用一、三、二，差分一、二、负一，总和应为二；若误用不同平滑表算出别的和，信用分解已不一致。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c344642547d511ac">HRPO 的前缀差分如何做一个基本 telescoping 自检？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahrpo">Hierarchical Residual Policy Optimization for Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · City University of Hong Kong / Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相邻 δt 应使用同一效用版本，求和可还原终前缀与空前缀效用差，credit-to-go 从当前位置累加而非从开头。用户簇平滑不能混入测试未来反馈。本地二进制 SID 只验证这一有界机制，不是大规模生成后训练效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三个前缀效用一、三、二，差分一、二、负一，总和应为二；若误用不同平滑表算出别的和，信用分解已不一致。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.00750">原论文</a> · <a href="../../../../reproductions/2608.00750-hrpo/">实现解读</a> · <a href="#qa-c344642547d511ac">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:feedback-policy" data-paper-title="From Understanding to Action: Feedback-Grounded Policy Discovery for Generative Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="From Understanding to Action: Feedback-Grounded Policy Discovery for Generative Recommendation 搜广推与 LLM 应用 Huazhong Agricultural University (Kuaishou internship) 2026-07-30 从用户反馈发现生成策略，以双空间关系蒸馏把策略压入轻量排序器，从而避免线上调用 LLM。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation policy-optimization distillation 搜广推 生成式召回与推理推荐 Feedback Policy 为什么把反馈策略迁成关系监督，而不只缓存策略文字？ 反馈能揭示候选之间的相似与替代结构，关系矩阵让轻排序器实际学习这些偏好，无须在线调用大模型解释。矩阵仍是教师代理，不保证保存完整推理，也可能继承反馈偏差。存下文字策略与让参数学到可用关系是两件事。 示意：教师判断两条教程互相替代，学生可学习它们不该同时占满列表；仅写一句“注意多样性”并不会自动改变模型向量或排序。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-feedback-policy-7fbe9a73" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2df110b970fb5442">Feedback Policy 为什么把反馈策略迁成关系监督，而不只缓存策略文字？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Afeedback-policy">From Understanding to Action: Feedback-Grounded Policy Discovery for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huazhong Agricultural University (Kuaishou internship)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>反馈能揭示候选之间的相似与替代结构，关系矩阵让轻排序器实际学习这些偏好，无须在线调用大模型解释。矩阵仍是教师代理，不保证保存完整推理，也可能继承反馈偏差。存下文字策略与让参数学到可用关系是两件事。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教师判断两条教程互相替代，学生可学习它们不该同时占满列表；仅写一句“注意多样性”并不会自动改变模型向量或排序。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27789">原论文</a> · <a href="../../../../reproductions/2607.27789-feedback-policy/">实现解读</a> · <a href="#qa-2df110b970fb5442">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:feedback-policy" data-paper-title="From Understanding to Action: Feedback-Grounded Policy Discovery for Generative Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="From Understanding to Action: Feedback-Grounded Policy Discovery for Generative Recommendation 搜广推与 LLM 应用 Huazhong Agricultural University (Kuaishou internship) 2026-07-30 从用户反馈发现生成策略，以双空间关系蒸馏把策略压入轻量排序器，从而避免线上调用 LLM。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation policy-optimization distillation 搜广推 生成式召回与推理推荐 Feedback Policy为什么蒸馏教师的关系矩阵，而不只模仿每个物品的独立分数？ 策略知识不仅在单项分数里，也在候选之间的相对关系中。关系蒸馏要求学生保留教师在对应空间内的相似或偏好结构，使轻量排序器吸收反馈发现的模式，而不在服务时运行LLM。若教师关系本身受偏置影响，学生也会继承；匹配矩阵误差下降并不等于用户反馈必然改善。 示意：两个商品单独分数相近，但教师知道它们在当前意图下互为替代；学生保留这种关系后可更好选择组合，而不仅逐个复制一个静态高分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-3d327498079e2bb6">Feedback Policy为什么蒸馏教师的关系矩阵，而不只模仿每个物品的独立分数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Afeedback-policy">From Understanding to Action: Feedback-Grounded Policy Discovery for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huazhong Agricultural University (Kuaishou internship)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>策略知识不仅在单项分数里，也在候选之间的相对关系中。关系蒸馏要求学生保留教师在对应空间内的相似或偏好结构，使轻量排序器吸收反馈发现的模式，而不在服务时运行LLM。若教师关系本身受偏置影响，学生也会继承；匹配矩阵误差下降并不等于用户反馈必然改善。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个商品单独分数相近，但教师知道它们在当前意图下互为替代；学生保留这种关系后可更好选择组合，而不仅逐个复制一个静态高分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27789">原论文</a> · <a href="../../../../reproductions/2607.27789-feedback-policy/">实现解读</a> · <a href="#qa-3d327498079e2bb6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:feedback-policy" data-paper-title="From Understanding to Action: Feedback-Grounded Policy Discovery for Generative Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="From Understanding to Action: Feedback-Grounded Policy Discovery for Generative Recommendation 搜广推与 LLM 应用 Huazhong Agricultural University (Kuaishou internship) 2026-07-30 从用户反馈发现生成策略，以双空间关系蒸馏把策略压入轻量排序器，从而避免线上调用 LLM。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation policy-optimization distillation 搜广推 生成式召回与推理推荐 关系矩阵蒸馏与逐物品 logit 蒸馏，关注哪些不同误差？ 独立分数强调输出数值接近，关系矩阵强调样本或空间之间的相对布局，对某些整体尺度变化更不敏感。它能补充结构，却可能忽略真实概率校准，二者不必一致。更多成对约束不自动意味着质量更高，仍需固定协议比较。 示意：教师全部分数加同一常数时排序关系未变，独立拟合误差却变大；关系蒸馏可忽略这类变化，但也不再直接约束绝对点击概率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0876b9b0cd20266d">关系矩阵蒸馏与逐物品 logit 蒸馏，关注哪些不同误差？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Afeedback-policy">From Understanding to Action: Feedback-Grounded Policy Discovery for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huazhong Agricultural University (Kuaishou internship)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立分数强调输出数值接近，关系矩阵强调样本或空间之间的相对布局，对某些整体尺度变化更不敏感。它能补充结构，却可能忽略真实概率校准，二者不必一致。更多成对约束不自动意味着质量更高，仍需固定协议比较。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教师全部分数加同一常数时排序关系未变，独立拟合误差却变大；关系蒸馏可忽略这类变化，但也不再直接约束绝对点击概率。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27789">原论文</a> · <a href="../../../../reproductions/2607.27789-feedback-policy/">实现解读</a> · <a href="#qa-0876b9b0cd20266d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:feedback-policy" data-paper-title="From Understanding to Action: Feedback-Grounded Policy Discovery for Generative Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="From Understanding to Action: Feedback-Grounded Policy Discovery for Generative Recommendation 搜广推与 LLM 应用 Huazhong Agricultural University (Kuaishou internship) 2026-07-30 从用户反馈发现生成策略，以双空间关系蒸馏把策略压入轻量排序器，从而避免线上调用 LLM。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation policy-optimization distillation 搜广推 生成式召回与推理推荐 Feedback Policy 的教师和学生关系矩阵为什么必须按同一身份顺序排列？ 矩阵每个位置代表具体样本对，错序会使损失拟合错误关系，形状相同也无济于事。有效项、归一化和 padding mask 也要一致，教师矩阵应来自允许证据。本地核心代理不等于完成真实用户反馈的策略发现闭环。 示意：教师第二行是相机而学生第二行是小说，逐项相减就在强迫错误配对；先按物品 ID 对齐，结构损失才有可解释含义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-bbcf875d87142580">Feedback Policy 的教师和学生关系矩阵为什么必须按同一身份顺序排列？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Afeedback-policy">From Understanding to Action: Feedback-Grounded Policy Discovery for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huazhong Agricultural University (Kuaishou internship)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>矩阵每个位置代表具体样本对，错序会使损失拟合错误关系，形状相同也无济于事。有效项、归一化和 padding mask 也要一致，教师矩阵应来自允许证据。本地核心代理不等于完成真实用户反馈的策略发现闭环。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教师第二行是相机而学生第二行是小说，逐项相减就在强迫错误配对；先按物品 ID 对齐，结构损失才有可解释含义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27789">原论文</a> · <a href="../../../../reproductions/2607.27789-feedback-policy/">实现解读</a> · <a href="#qa-bbcf875d87142580">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:snaplgr" data-paper-title="LLM-Based Generative Retrieval for Snapchat Content Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="LLM-Based Generative Retrieval for Snapchat Content Recommendation 搜广推与 LLM 应用 Snap Inc. 2026-07-30 先从共参与图传播内容相关性，再用分层残差量化形成 semantic ID；训练时把 SID token 与真实内容表征对齐，并学习用户序列到下一 SID 的生成转移。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为普通 residual SID，实验组加入共参与传播、grounding 与 SID transition；  retrieval generative-recommendation semantic-id llm multimodal 搜广推 生成式召回与推理推荐 SnapLGR为什么先用共参与图再形成SID？ 图传播提供协同行为相关性，残差量化把它组织成层级码，再学习用户序列到码的生成。内容相似与用户共参与互补，不能只用随机码保留名字。 例如不同外观内容可能被同一兴趣人群一起消费，图能提供这种关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-snaplgr-28d916e6" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-86180448fcf71ebd">SnapLGR为什么先用共参与图再形成SID？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asnaplgr">LLM-Based Generative Retrieval for Snapchat Content Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Snap Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>图传播提供协同行为相关性，残差量化把它组织成层级码，再学习用户序列到码的生成。内容相似与用户共参与互补，不能只用随机码保留名字。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如不同外观内容可能被同一兴趣人群一起消费，图能提供这种关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28895">原论文</a> · <a href="../../../../reproductions/2607.28895-snaplgr/">实现解读</a> · <a href="#qa-86180448fcf71ebd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:snaplgr" data-paper-title="LLM-Based Generative Retrieval for Snapchat Content Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="LLM-Based Generative Retrieval for Snapchat Content Recommendation 搜广推与 LLM 应用 Snap Inc. 2026-07-30 先从共参与图传播内容相关性，再用分层残差量化形成 semantic ID；训练时把 SID token 与真实内容表征对齐，并学习用户序列到下一 SID 的生成转移。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为普通 residual SID，实验组加入共参与传播、grounding 与 SID transition；  retrieval generative-recommendation semantic-id llm multimodal 搜广推 生成式召回与推理推荐 SnapLGR 为什么先在共参与图传播，再量化为 SID，并对 token 做内容 grounding？ 原始内容向量未必包含平台上的协同行为，图传播先把共参与关系融入表示，再量化使这些关系进入离散路径。grounding 约束生成 token 仍对应实际内容，序列到下一 SID 的目标再学习用户转移。图信号、离散化与生成分别承担不同环节，热门共现偏差也可能沿传播进入码本。 示意：两类内容视觉不同却常被同一兴趣群体消费，传播后可在表示上关联；量化得到路径后仍需对齐原内容，避免用户生成某个码却无法稳定映回相关物品。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-e972912a0c70610f">SnapLGR 为什么先在共参与图传播，再量化为 SID，并对 token 做内容 grounding？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asnaplgr">LLM-Based Generative Retrieval for Snapchat Content Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Snap Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原始内容向量未必包含平台上的协同行为，图传播先把共参与关系融入表示，再量化使这些关系进入离散路径。grounding 约束生成 token 仍对应实际内容，序列到下一 SID 的目标再学习用户转移。图信号、离散化与生成分别承担不同环节，热门共现偏差也可能沿传播进入码本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两类内容视觉不同却常被同一兴趣群体消费，传播后可在表示上关联；量化得到路径后仍需对齐原内容，避免用户生成某个码却无法稳定映回相关物品。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28895">原论文</a> · <a href="../../../../reproductions/2607.28895-snaplgr/">实现解读</a> · <a href="#qa-e972912a0c70610f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:snaplgr" data-paper-title="LLM-Based Generative Retrieval for Snapchat Content Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="LLM-Based Generative Retrieval for Snapchat Content Recommendation 搜广推与 LLM 应用 Snap Inc. 2026-07-30 先从共参与图传播内容相关性，再用分层残差量化形成 semantic ID；训练时把 SID token 与真实内容表征对齐，并学习用户序列到下一 SID 的生成转移。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为普通 residual SID，实验组加入共参与传播、grounding 与 SID transition；  retrieval generative-recommendation semantic-id llm multimodal 搜广推 生成式召回与推理推荐 SID与内容表征对齐比单独预测离散编号多约束什么？ 对齐让生成token保留真实内容语义结构，单纯编号似然可只记码转移。它仍依赖表征与图质量，不保证任何语义码都比原ID强。 例如两个相关视频码的表示应有联系，而不是只学任意标签次序。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-42f47c26b383eb22">SID与内容表征对齐比单独预测离散编号多约束什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asnaplgr">LLM-Based Generative Retrieval for Snapchat Content Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Snap Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>对齐让生成token保留真实内容语义结构，单纯编号似然可只记码转移。它仍依赖表征与图质量，不保证任何语义码都比原ID强。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个相关视频码的表示应有联系，而不是只学任意标签次序。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28895">原论文</a> · <a href="../../../../reproductions/2607.28895-snaplgr/">实现解读</a> · <a href="#qa-42f47c26b383eb22">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:snaplgr" data-paper-title="LLM-Based Generative Retrieval for Snapchat Content Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="LLM-Based Generative Retrieval for Snapchat Content Recommendation 搜广推与 LLM 应用 Snap Inc. 2026-07-30 先从共参与图传播内容相关性，再用分层残差量化形成 semantic ID；训练时把 SID token 与真实内容表征对齐，并学习用户序列到下一 SID 的生成转移。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为普通 residual SID，实验组加入共参与传播、grounding 与 SID transition；  retrieval generative-recommendation semantic-id llm multimodal 搜广推 生成式召回与推理推荐 SnapLGR图传播与量化训练应使用哪些行为边界？ 仅用训练期允许共参与，避免测试未来边进入图；码本与SID映射需固定版本。当前公开特征代理不含Snap私有日志、生产规模或流量分配。 例如先把测试点击加入共现图，会使召回器提前获知评测关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6a48591353777092">SnapLGR图传播与量化训练应使用哪些行为边界？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asnaplgr">LLM-Based Generative Retrieval for Snapchat Content Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Snap Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>仅用训练期允许共参与，避免测试未来边进入图；码本与SID映射需固定版本。当前公开特征代理不含Snap私有日志、生产规模或流量分配。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先把测试点击加入共现图，会使召回器提前获知评测关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28895">原论文</a> · <a href="../../../../reproductions/2607.28895-snaplgr/">实现解读</a> · <a href="#qa-6a48591353777092">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:reward-guided-decoding" data-paper-title="Reward Guided Decoding for Generative Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Reward Guided Decoding for Generative Recommendation 搜广推与 LLM 应用 Institute of Information Engineering, Chinese Academy of Sciences 2026-07-28 保持生成器概率作为先验，在解码时用独立 reward 进行指数倾斜；闭式策略在提升期望 reward 的同时用 KL 温度限制偏离，无需重新训练生成器。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线按生成器似然解码，实验组用内容/新颖度 reward 做 KL 正则倾斜；seed 42 的 NDCG@10 为 0.02249，基线为 0.05401，负结果保留。  generative-recommendation decoding reward business-alignment 搜广推 生成式召回与推理推荐 奖励引导解码能给先验概率 P0=0 的序列分配正概率吗？ 按来源闭式公式不能。Q 与 P0 乘奖励指数成比例，先验严格为零时乘积仍为零，归一化也不会创造支持。奖励只重排已有支持内的质量；若额外平滑、扩展候选或修改生成器，需作为另外的算法步骤说明，不能归给指数倾斜本身。 示意：合法候选集合根本不包含某电影，给它再高新颖度也不会凭公式出现；必须先有可生成或可枚举的支持，奖励才能影响选择。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-reward-guided-decoding-a3100a32" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5f4bd9838c190a35">奖励引导解码能给先验概率 P0=0 的序列分配正概率吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Areward-guided-decoding">Reward Guided Decoding for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Information Engineering, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>按来源闭式公式不能。Q 与 P0 乘奖励指数成比例，先验严格为零时乘积仍为零，归一化也不会创造支持。奖励只重排已有支持内的质量；若额外平滑、扩展候选或修改生成器，需作为另外的算法步骤说明，不能归给指数倾斜本身。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>合法候选集合根本不包含某电影，给它再高新颖度也不会凭公式出现；必须先有可生成或可枚举的支持，奖励才能影响选择。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25344">原论文</a> · <a href="../../../../reproductions/2607.25344-reward-guided-decoding/">实现解读</a> · <a href="#qa-5f4bd9838c190a35">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:reward-guided-decoding" data-paper-title="Reward Guided Decoding for Generative Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Reward Guided Decoding for Generative Recommendation 搜广推与 LLM 应用 Institute of Information Engineering, Chinese Academy of Sciences 2026-07-28 保持生成器概率作为先验，在解码时用独立 reward 进行指数倾斜；闭式策略在提升期望 reward 的同时用 KL 温度限制偏离，无需重新训练生成器。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线按生成器似然解码，实验组用内容/新颖度 reward 做 KL 正则倾斜；seed 42 的 NDCG@10 为 0.02249，基线为 0.05401，负结果保留。  generative-recommendation decoding reward business-alignment 搜广推 生成式召回与推理推荐 奖励引导解码中的指数倾斜，为什么既保留生成器先验又受 KL 温度控制？ 最优受约束分布在原模型概率上乘以奖励的指数项，奖励较高的结果被提升，但原先极不可能的结果不会完全忽略先验地涌入。温度控制偏离代价，越小越强追逐奖励，越大越接近原分布。无需重训不代表无代价：奖励误差会改变解码方向，归一化与候选搜索也影响近似质量。 示意：原模型偏好熟悉影片，奖励鼓励新颖。适中温度可适度提升相关冷门片；温度过小则可能为新颖性挑出不合兴趣的片，因而不能只看奖励升高就说推荐更好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-0710a847a39d981a">奖励引导解码中的指数倾斜，为什么既保留生成器先验又受 KL 温度控制？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Areward-guided-decoding">Reward Guided Decoding for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Information Engineering, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最优受约束分布在原模型概率上乘以奖励的指数项，奖励较高的结果被提升，但原先极不可能的结果不会完全忽略先验地涌入。温度控制偏离代价，越小越强追逐奖励，越大越接近原分布。无需重训不代表无代价：奖励误差会改变解码方向，归一化与候选搜索也影响近似质量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>原模型偏好熟悉影片，奖励鼓励新颖。适中温度可适度提升相关冷门片；温度过小则可能为新颖性挑出不合兴趣的片，因而不能只看奖励升高就说推荐更好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25344">原论文</a> · <a href="../../../../reproductions/2607.25344-reward-guided-decoding/">实现解读</a> · <a href="#qa-0710a847a39d981a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:reward-guided-decoding" data-paper-title="Reward Guided Decoding for Generative Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Reward Guided Decoding for Generative Recommendation 搜广推与 LLM 应用 Institute of Information Engineering, Chinese Academy of Sciences 2026-07-28 保持生成器概率作为先验，在解码时用独立 reward 进行指数倾斜；闭式策略在提升期望 reward 的同时用 KL 温度限制偏离，无需重新训练生成器。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线按生成器似然解码，实验组用内容/新颖度 reward 做 KL 正则倾斜；seed 42 的 NDCG@10 为 0.02249，基线为 0.05401，负结果保留。  generative-recommendation decoding reward business-alignment 搜广推 生成式召回与推理推荐 指数倾斜与简单线性相加 logits，何时具有对应关系、何时不能乱换？ 在相同候选全集上，log Q 与 log P0+R/β 仅差共同归一常数，可用于排序；若把原概率 P0 而非 log P0 加奖励，就不是同分布。不同候选截断也改变归一与支持，不能无说明视为闭式策略精确实现。 示意：概率零点九与零点一直接加一分奖励，和对数概率加奖励会产生不同强度；公式里先验的尺度不是可随便替换的细节。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-94cf388dc09984d0">指数倾斜与简单线性相加 logits，何时具有对应关系、何时不能乱换？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Areward-guided-decoding">Reward Guided Decoding for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Information Engineering, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>在相同候选全集上，log Q 与 log P0+R/β 仅差共同归一常数，可用于排序；若把原概率 P0 而非 log P0 加奖励，就不是同分布。不同候选截断也改变归一与支持，不能无说明视为闭式策略精确实现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>概率零点九与零点一直接加一分奖励，和对数概率加奖励会产生不同强度；公式里先验的尺度不是可随便替换的细节。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25344">原论文</a> · <a href="../../../../reproductions/2607.25344-reward-guided-decoding/">实现解读</a> · <a href="#qa-94cf388dc09984d0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:reward-guided-decoding" data-paper-title="Reward Guided Decoding for Generative Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Reward Guided Decoding for Generative Recommendation 搜广推与 LLM 应用 Institute of Information Engineering, Chinese Academy of Sciences 2026-07-28 保持生成器概率作为先验，在解码时用独立 reward 进行指数倾斜；闭式策略在提升期望 reward 的同时用 KL 温度限制偏离，无需重新训练生成器。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线按生成器似然解码，实验组用内容/新颖度 reward 做 KL 正则倾斜；seed 42 的 NDCG@10 为 0.02249，基线为 0.05401，负结果保留。  generative-recommendation decoding reward business-alignment 搜广推 生成式召回与推理推荐 实现奖励指数倾斜为什么应使用 logsumexp 并测试温度极限？ 直接 exp 容易上溢，log 空间计算更稳定；β 大应更接近先验，β 小更追奖励，非法候选保持屏蔽。截断近似与完整闭式归一需区别。来源新颖度奖励导致 NDCG 明显下降，不能只看奖励升高就称更好推荐。 示意：奖励一千直接指数可能变无穷，稳定归一仍能比较；但数值稳定不等于策略合理，小温度仍可能极端挑新奇却无关内容。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-13edd1a09ebb9259">实现奖励指数倾斜为什么应使用 logsumexp 并测试温度极限？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Areward-guided-decoding">Reward Guided Decoding for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Information Engineering, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直接 exp 容易上溢，log 空间计算更稳定；β 大应更接近先验，β 小更追奖励，非法候选保持屏蔽。截断近似与完整闭式归一需区别。来源新颖度奖励导致 NDCG 明显下降，不能只看奖励升高就称更好推荐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>奖励一千直接指数可能变无穷，稳定归一仍能比较；但数值稳定不等于策略合理，小温度仍可能极端挑新奇却无关内容。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25344">原论文</a> · <a href="../../../../reproductions/2607.25344-reward-guided-decoding/">实现解读</a> · <a href="#qa-13edd1a09ebb9259">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:oxygenrec-v2" data-paper-title="OxygenREC-v2: Internalizing Discrimination into Generative Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OxygenREC-v2: Internalizing Discrimination into Generative Recommendation 搜广推与 LLM 应用 JD.COM 2026-07-27 工业生成式推荐通常先生成候选，再外挂判别器或 reward model 重排；重排只能改变顺序，不能补回生成阶段漏掉的商品。OxygenREC-v2 把 click/cart/order 行为作为 decoder instruction，从第一枚 SID token 起控制候选生成；后训练再使用仅训练期可见的未来交互，联合可验证轨迹优化、自蒸馏和高熵位置的 forward-KL。 Fidelity: 核心机制复现。实际训练行为 instruction、行为加权目标、未来交互 privileged view 与熵路由蒸馏；生产模型和私有漏斗数据未复刻。这是核心机制的小规模复现，不含京东私有多行为日志、三层生产 SID、3B-A1B MoE 和线上服务。负结果主要说明“流行度分位”不是购买意图的可靠替代，不否定论文的私有数据结论。本地对照口径：基线与实验组使用同一 MovieLens 切片、full-catalog 候选、训练步数和 seed；实验组只增加论文机制，相对 NDCG@10 为 -54.09%。  generative-recommendation privileged-distillation behavior-instruction 搜广推 生成式召回与推理推荐 OxygenREC-v2 为什么把 click、cart、order 放进 decoder instruction？ 行为目标不同会改变哪些候选值得生成，从首个 SID 起条件化比末端只改排序更早影响覆盖。加权预训与后训练再连接反馈。行为是合法任务条件，不应由当前测试目标反推；本地用热门度代理，不能当真实多行为监督。 示意：同一历史想优化加购与随手点击时，首层语义分支就可能不同；若只生成点击热门品再重排，下单候选可能早已漏掉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-oxygenrec-v2-987866fe" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-bf86223c11e363a4">OxygenREC-v2 为什么把 click、cart、order 放进 decoder instruction？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aoxygenrec-v2">OxygenREC-v2: Internalizing Discrimination into Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · JD.COM</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>行为目标不同会改变哪些候选值得生成，从首个 SID 起条件化比末端只改排序更早影响覆盖。加权预训与后训练再连接反馈。行为是合法任务条件，不应由当前测试目标反推；本地用热门度代理，不能当真实多行为监督。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一历史想优化加购与随手点击时，首层语义分支就可能不同；若只生成点击热门品再重排，下单候选可能早已漏掉。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24255">原论文</a> · <a href="../../../../reproductions/2607.24255-oxygenrec-v2/">实现解读</a> · <a href="#qa-bf86223c11e363a4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:oxygenrec-v2" data-paper-title="OxygenREC-v2: Internalizing Discrimination into Generative Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OxygenREC-v2: Internalizing Discrimination into Generative Recommendation 搜广推与 LLM 应用 JD.COM 2026-07-27 工业生成式推荐通常先生成候选，再外挂判别器或 reward model 重排；重排只能改变顺序，不能补回生成阶段漏掉的商品。OxygenREC-v2 把 click/cart/order 行为作为 decoder instruction，从第一枚 SID token 起控制候选生成；后训练再使用仅训练期可见的未来交互，联合可验证轨迹优化、自蒸馏和高熵位置的 forward-KL。 Fidelity: 核心机制复现。实际训练行为 instruction、行为加权目标、未来交互 privileged view 与熵路由蒸馏；生产模型和私有漏斗数据未复刻。这是核心机制的小规模复现，不含京东私有多行为日志、三层生产 SID、3B-A1B MoE 和线上服务。负结果主要说明“流行度分位”不是购买意图的可靠替代，不否定论文的私有数据结论。本地对照口径：基线与实验组使用同一 MovieLens 切片、full-catalog 候选、训练步数和 seed；实验组只增加论文机制，相对 NDCG@10 为 -54.09%。  generative-recommendation privileged-distillation behavior-instruction 搜广推 生成式召回与推理推荐 OxygenREC-v2 为什么从第一枚 SID 就注入行为指令，并按不确定性选择不同的后训练约束？ 只在生成后重排不能补回已经漏掉的商品，行为指令因此直接进入解码前缀，让点击、加购或下单目标影响整条生成路径。后训练借助仅训练时可见的未来交互，低熵位置接受较确定的教师信号，高熵位置用 forward-KL 保留多种可能。未来信息用于监督而不进入线上输入，是机制成立的关键边界。 示意：要优化下单时，模型从首个语义码就偏向可购买候选。若某一分支有多种合理商品，训练不把它硬压成唯一答案；请求时仍只能依据当前已知历史生成。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-707ccd2ae0c3750c">OxygenREC-v2 为什么从第一枚 SID 就注入行为指令，并按不确定性选择不同的后训练约束？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aoxygenrec-v2">OxygenREC-v2: Internalizing Discrimination into Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · JD.COM</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只在生成后重排不能补回已经漏掉的商品，行为指令因此直接进入解码前缀，让点击、加购或下单目标影响整条生成路径。后训练借助仅训练时可见的未来交互，低熵位置接受较确定的教师信号，高熵位置用 forward-KL 保留多种可能。未来信息用于监督而不进入线上输入，是机制成立的关键边界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>要优化下单时，模型从首个语义码就偏向可购买候选。若某一分支有多种合理商品，训练不把它硬压成唯一答案；请求时仍只能依据当前已知历史生成。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24255">原论文</a> · <a href="../../../../reproductions/2607.24255-oxygenrec-v2/">实现解读</a> · <a href="#qa-707ccd2ae0c3750c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:oxygenrec-v2" data-paper-title="OxygenREC-v2: Internalizing Discrimination into Generative Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OxygenREC-v2: Internalizing Discrimination into Generative Recommendation 搜广推与 LLM 应用 JD.COM 2026-07-27 工业生成式推荐通常先生成候选，再外挂判别器或 reward model 重排；重排只能改变顺序，不能补回生成阶段漏掉的商品。OxygenREC-v2 把 click/cart/order 行为作为 decoder instruction，从第一枚 SID token 起控制候选生成；后训练再使用仅训练期可见的未来交互，联合可验证轨迹优化、自蒸馏和高熵位置的 forward-KL。 Fidelity: 核心机制复现。实际训练行为 instruction、行为加权目标、未来交互 privileged view 与熵路由蒸馏；生产模型和私有漏斗数据未复刻。这是核心机制的小规模复现，不含京东私有多行为日志、三层生产 SID、3B-A1B MoE 和线上服务。负结果主要说明“流行度分位”不是购买意图的可靠替代，不否定论文的私有数据结论。本地对照口径：基线与实验组使用同一 MovieLens 切片、full-catalog 候选、训练步数和 seed；实验组只增加论文机制，相对 NDCG@10 为 -54.09%。  generative-recommendation privileged-distillation behavior-instruction 搜广推 生成式召回与推理推荐 privileged teacher 的未来监督与线上使用未来特征，为什么边界不同？ 训练教师可利用后续交互构造更丰富目标，再将知识传给仅当前输入的学生；线上未来尚未发生，不能进入 prefix。知识迁移允许标签更丰富，不允许评估读答案。高熵位置 forward-KL 也只是约束分布，不把未来变成实时可见信息。 示意：训练知道用户后来买了露营灯，可教当前历史模型；测试若先把这次购买放教师前缀再直接用于线上评分，就绕过了预测。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5890fd364fd8b45e">privileged teacher 的未来监督与线上使用未来特征，为什么边界不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aoxygenrec-v2">OxygenREC-v2: Internalizing Discrimination into Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · JD.COM</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>训练教师可利用后续交互构造更丰富目标，再将知识传给仅当前输入的学生；线上未来尚未发生，不能进入 prefix。知识迁移允许标签更丰富，不允许评估读答案。高熵位置 forward-KL 也只是约束分布，不把未来变成实时可见信息。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练知道用户后来买了露营灯，可教当前历史模型；测试若先把这次购买放教师前缀再直接用于线上评分，就绕过了预测。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24255">原论文</a> · <a href="../../../../reproductions/2607.24255-oxygenrec-v2/">实现解读</a> · <a href="#qa-5890fd364fd8b45e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:oxygenrec-v2" data-paper-title="OxygenREC-v2: Internalizing Discrimination into Generative Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OxygenREC-v2: Internalizing Discrimination into Generative Recommendation 搜广推与 LLM 应用 JD.COM 2026-07-27 工业生成式推荐通常先生成候选，再外挂判别器或 reward model 重排；重排只能改变顺序，不能补回生成阶段漏掉的商品。OxygenREC-v2 把 click/cart/order 行为作为 decoder instruction，从第一枚 SID token 起控制候选生成；后训练再使用仅训练期可见的未来交互，联合可验证轨迹优化、自蒸馏和高熵位置的 forward-KL。 Fidelity: 核心机制复现。实际训练行为 instruction、行为加权目标、未来交互 privileged view 与熵路由蒸馏；生产模型和私有漏斗数据未复刻。这是核心机制的小规模复现，不含京东私有多行为日志、三层生产 SID、3B-A1B MoE 和线上服务。负结果主要说明“流行度分位”不是购买意图的可靠替代，不否定论文的私有数据结论。本地对照口径：基线与实验组使用同一 MovieLens 切片、full-catalog 候选、训练步数和 seed；实验组只增加论文机制，相对 NDCG@10 为 -54.09%。  generative-recommendation privileged-distillation behavior-instruction 搜广推 生成式召回与推理推荐 OxygenREC-v2 本地推理为何边缘化三种代理行为，而不选真实目标所属一类？ MovieLens 没有 click/cart/order，若按 held-out 目标流行度选择条件，会泄漏答案身份线索。边缘化承认没有真实请求行为条件，但也改变原任务，结论限代理机制。未来 privileged view、高熵路由与损失仍应分别核验，不能用一项代表全链路。 示意：目标恰属低流行度组，评估先告诉模型“本次生成这组”就缩小搜索；对三个未知代理条件综合处理，才避免这种额外答案提示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-51c6f5f784b73056">OxygenREC-v2 本地推理为何边缘化三种代理行为，而不选真实目标所属一类？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aoxygenrec-v2">OxygenREC-v2: Internalizing Discrimination into Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · JD.COM</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>MovieLens 没有 click/cart/order，若按 held-out 目标流行度选择条件，会泄漏答案身份线索。边缘化承认没有真实请求行为条件，但也改变原任务，结论限代理机制。未来 privileged view、高熵路由与损失仍应分别核验，不能用一项代表全链路。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>目标恰属低流行度组，评估先告诉模型“本次生成这组”就缩小搜索；对三个未知代理条件综合处理，才避免这种额外答案提示。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24255">原论文</a> · <a href="../../../../reproductions/2607.24255-oxygenrec-v2/">实现解读</a> · <a href="#qa-51c6f5f784b73056">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unir2" data-paper-title="Unifying Generative Recall and Multi-Objective Ranking in a Single Decoder-Only Sequence" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Unifying Generative Recall and Multi-Objective Ranking in a Single Decoder-Only Sequence 搜广推与 LLM 应用 Kuaishou / IIE, CAS / UCAS 2026-07-27 传统工业 cascade 分别训练 recall 和 ranking：两边重复编码用户历史，生成轨迹在候选交接时丢失，训练目标也可能冲突。UniR² 把用户上下文、目标物品 SID 轨迹和 item ranking features 拼成一个 decoder-only 异构序列，让生成轨迹成为召回与排序之间的表示桥。DQ-PCA 为同一层提供两种 query：generation query 只能读取完整用户 prefix 和此前 SID； 本地使用两级 16-way SID，而非三层 8129 codebook，也未运行 beam search、3×640 服务模型和流水线并行。Fidelity: 核心机制复现。实际训练层级 SID、Dual-Query Prefix-Causal Attention、ranking-only LoRA 和生成/排序联合目标；缩小 codebook、模型和业务标签。MovieLens next-item 与 genre-affinity 代理快手 click/long-view/gift；  generative-recommendation unified-recall-ranking multi-objective-ranking lora 搜广推 生成式召回与推理推荐 UniR²为什么把生成SID轨迹作为排序桥？ 召回与排序共享用户编码还不够，生成路径包含选候选的中间信息。异构decoder让排序读取这条轨迹及item特征，减少交接时表示丢失。 例如不仅知道最终商品ID，还利用它经哪些语义前缀被生成。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-unir2-b2b6f557" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-38e98a94a6926bfc">UniR²为什么把生成SID轨迹作为排序桥？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunir2">Unifying Generative Recall and Multi-Objective Ranking in a Single Decoder-Only Sequence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou / IIE, CAS / UCAS</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>召回与排序共享用户编码还不够，生成路径包含选候选的中间信息。异构decoder让排序读取这条轨迹及item特征，减少交接时表示丢失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如不仅知道最终商品ID，还利用它经哪些语义前缀被生成。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24439">原论文</a> · <a href="../../../../reproductions/2607.24439-unir2/">实现解读</a> · <a href="#qa-38e98a94a6926bfc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unir2" data-paper-title="Unifying Generative Recall and Multi-Objective Ranking in a Single Decoder-Only Sequence" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Unifying Generative Recall and Multi-Objective Ranking in a Single Decoder-Only Sequence 搜广推与 LLM 应用 Kuaishou / IIE, CAS / UCAS 2026-07-27 传统工业 cascade 分别训练 recall 和 ranking：两边重复编码用户历史，生成轨迹在候选交接时丢失，训练目标也可能冲突。UniR² 把用户上下文、目标物品 SID 轨迹和 item ranking features 拼成一个 decoder-only 异构序列，让生成轨迹成为召回与排序之间的表示桥。DQ-PCA 为同一层提供两种 query：generation query 只能读取完整用户 prefix 和此前 SID； 本地使用两级 16-way SID，而非三层 8129 codebook，也未运行 beam search、3×640 服务模型和流水线并行。Fidelity: 核心机制复现。实际训练层级 SID、Dual-Query Prefix-Causal Attention、ranking-only LoRA 和生成/排序联合目标；缩小 codebook、模型和业务标签。MovieLens next-item 与 genre-affinity 代理快手 click/long-view/gift；  generative-recommendation unified-recall-ranking multi-objective-ranking lora 搜广推 生成式召回与推理推荐 UniR² 为什么让排序分支读取 SID 轨迹，却对共享输出 stop-gradient 并只学习 LoRA？ SID 轨迹包含召回时逐级选择的中间信息，保留它可作为生成与排序的表示桥。两类 query 用不同掩码读取所需上下文，排序分支再对共享输出停止梯度，只通过低秩增量学习专有交互，防止排序目标破坏生成主干。它共享前向知识但控制反向干扰，并非所有任务梯度都无约束混合。 示意：生成器先走“户外—露营—帐篷”路径，排序器可利用整条轨迹判断具体商品。若排序偏好变化，先调整排序 LoRA，而不直接把生成器原本学好的路径语义改乱。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-d829ee3c55f372e7">UniR² 为什么让排序分支读取 SID 轨迹，却对共享输出 stop-gradient 并只学习 LoRA？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunir2">Unifying Generative Recall and Multi-Objective Ranking in a Single Decoder-Only Sequence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou / IIE, CAS / UCAS</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>SID 轨迹包含召回时逐级选择的中间信息，保留它可作为生成与排序的表示桥。两类 query 用不同掩码读取所需上下文，排序分支再对共享输出停止梯度，只通过低秩增量学习专有交互，防止排序目标破坏生成主干。它共享前向知识但控制反向干扰，并非所有任务梯度都无约束混合。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>生成器先走“户外—露营—帐篷”路径，排序器可利用整条轨迹判断具体商品。若排序偏好变化，先调整排序 LoRA，而不直接把生成器原本学好的路径语义改乱。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24439">原论文</a> · <a href="../../../../reproductions/2607.24439-unir2/">实现解读</a> · <a href="#qa-d829ee3c55f372e7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unir2" data-paper-title="Unifying Generative Recall and Multi-Objective Ranking in a Single Decoder-Only Sequence" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Unifying Generative Recall and Multi-Objective Ranking in a Single Decoder-Only Sequence 搜广推与 LLM 应用 Kuaishou / IIE, CAS / UCAS 2026-07-27 传统工业 cascade 分别训练 recall 和 ranking：两边重复编码用户历史，生成轨迹在候选交接时丢失，训练目标也可能冲突。UniR² 把用户上下文、目标物品 SID 轨迹和 item ranking features 拼成一个 decoder-only 异构序列，让生成轨迹成为召回与排序之间的表示桥。DQ-PCA 为同一层提供两种 query：generation query 只能读取完整用户 prefix 和此前 SID； 本地使用两级 16-way SID，而非三层 8129 codebook，也未运行 beam search、3×640 服务模型和流水线并行。Fidelity: 核心机制复现。实际训练层级 SID、Dual-Query Prefix-Causal Attention、ranking-only LoRA 和生成/排序联合目标；缩小 codebook、模型和业务标签。MovieLens next-item 与 genre-affinity 代理快手 click/long-view/gift；  generative-recommendation unified-recall-ranking multi-objective-ranking lora 搜广推 生成式召回与推理推荐 generation query与ranking query为什么不能同一mask？ 生成需因果读取此前SID，排序可读完整轨迹与同步item tokens，信息需求不同。若生成读未来码会泄漏teacher-forcing目标，若全用生成mask又削弱排序。 例如预测第二级码不能看第三级真实码，排序则可用完整候选路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-801509b74030f2f3">generation query与ranking query为什么不能同一mask？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunir2">Unifying Generative Recall and Multi-Objective Ranking in a Single Decoder-Only Sequence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou / IIE, CAS / UCAS</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>生成需因果读取此前SID，排序可读完整轨迹与同步item tokens，信息需求不同。若生成读未来码会泄漏teacher-forcing目标，若全用生成mask又削弱排序。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如预测第二级码不能看第三级真实码，排序则可用完整候选路径。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24439">原论文</a> · <a href="../../../../reproductions/2607.24439-unir2/">实现解读</a> · <a href="#qa-801509b74030f2f3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unir2" data-paper-title="Unifying Generative Recall and Multi-Objective Ranking in a Single Decoder-Only Sequence" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Unifying Generative Recall and Multi-Objective Ranking in a Single Decoder-Only Sequence 搜广推与 LLM 应用 Kuaishou / IIE, CAS / UCAS 2026-07-27 传统工业 cascade 分别训练 recall 和 ranking：两边重复编码用户历史，生成轨迹在候选交接时丢失，训练目标也可能冲突。UniR² 把用户上下文、目标物品 SID 轨迹和 item ranking features 拼成一个 decoder-only 异构序列，让生成轨迹成为召回与排序之间的表示桥。DQ-PCA 为同一层提供两种 query：generation query 只能读取完整用户 prefix 和此前 SID； 本地使用两级 16-way SID，而非三层 8129 codebook，也未运行 beam search、3×640 服务模型和流水线并行。Fidelity: 核心机制复现。实际训练层级 SID、Dual-Query Prefix-Causal Attention、ranking-only LoRA 和生成/排序联合目标；缩小 codebook、模型和业务标签。MovieLens next-item 与 genre-affinity 代理快手 click/long-view/gift；  generative-recommendation unified-recall-ranking multi-objective-ranking lora 搜广推 生成式召回与推理推荐 UniR² ranking LoRA如何避免改坏共享生成主干？ 共享Q/K/V输出在ranking分支stop-gradient，只让ranking LoRA学特有交互。不是冻结整个模型，也不能把两个分支全梯度共享称隔离；本地缩比未跑生产beam与并行。 例如排序loss仍可更新LoRA，但不应沿共享输出回传修改生成投影。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-9a0ab5f3e0db431b">UniR² ranking LoRA如何避免改坏共享生成主干？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunir2">Unifying Generative Recall and Multi-Objective Ranking in a Single Decoder-Only Sequence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou / IIE, CAS / UCAS</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共享Q/K/V输出在ranking分支stop-gradient，只让ranking LoRA学特有交互。不是冻结整个模型，也不能把两个分支全梯度共享称隔离；本地缩比未跑生产beam与并行。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如排序loss仍可更新LoRA，但不应沿共享输出回传修改生成投影。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24439">原论文</a> · <a href="../../../../reproductions/2607.24439-unir2/">实现解读</a> · <a href="#qa-9a0ab5f3e0db431b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:egr" data-paper-title="EGR: Embedding-Native Generative Retrieval with a Shared LLM" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="EGR: Embedding-Native Generative Retrieval with a Shared LLM 搜广推与 LLM 应用 Snap Inc. 2026-07-25 同一编码骨干产生 item 索引向量和 user query 向量，并让 item representation learning 与 next-item prediction 全程联合训练。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 EGR 为 0.05025，相对变化 -6.95%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  retrieval generative-retrieval shared-encoder 搜广推 生成式召回与推理推荐 EGR 为什么联合训练 item representation learning 和 next-item prediction？ 物品表示只优化自身内容时，可能不利于用户查询；下一物品监督让索引空间保留推荐需要的差别，item 目标又约束其语义。共享骨干使两类信号共同更新，减少割裂，也可能带来梯度冲突，不能由共享结构直接推出自然对齐。 示意：两部同题材片内容接近，但不同人群消费模式不同，联合训练可让索引区分这种关系，而不只优化文本相似。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-egr-a66d7f0c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-544a8e3547557490">EGR 为什么联合训练 item representation learning 和 next-item prediction？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aegr">EGR: Embedding-Native Generative Retrieval with a Shared LLM</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Snap Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>物品表示只优化自身内容时，可能不利于用户查询；下一物品监督让索引空间保留推荐需要的差别，item 目标又约束其语义。共享骨干使两类信号共同更新，减少割裂，也可能带来梯度冲突，不能由共享结构直接推出自然对齐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两部同题材片内容接近，但不同人群消费模式不同，联合训练可让索引区分这种关系，而不只优化文本相似。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.23038">原论文</a> · <a href="../../../../reproductions/2607.23038-egr/">实现解读</a> · <a href="#qa-544a8e3547557490">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:egr" data-paper-title="EGR: Embedding-Native Generative Retrieval with a Shared LLM" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="EGR: Embedding-Native Generative Retrieval with a Shared LLM 搜广推与 LLM 应用 Snap Inc. 2026-07-25 同一编码骨干产生 item 索引向量和 user query 向量，并让 item representation learning 与 next-item prediction 全程联合训练。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 EGR 为 0.05025，相对变化 -6.95%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  retrieval generative-retrieval shared-encoder 搜广推 生成式召回与推理推荐 EGR让item索引与user查询共用骨干，为什么仍要联合训练两个任务？ 共享参数只提供计算与表示联系，不保证两侧在检索空间中自然匹配。item表示学习维护可索引内容，next-item目标让用户查询朝实际消费关系调整，两种监督共同决定空间几何。若独立冻结一侧而另一侧持续变化，索引可能陈旧；联合训练后的向量仍需以一致版本建库和评估。 示意：商品编码因新训练发生旋转，用户查询却沿旧方向打分，会破坏近邻关系；两个目标共同训练有助对齐，但服务索引也要按对应版本更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-72f235af74f628cc">EGR让item索引与user查询共用骨干，为什么仍要联合训练两个任务？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aegr">EGR: Embedding-Native Generative Retrieval with a Shared LLM</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Snap Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共享参数只提供计算与表示联系，不保证两侧在检索空间中自然匹配。item表示学习维护可索引内容，next-item目标让用户查询朝实际消费关系调整，两种监督共同决定空间几何。若独立冻结一侧而另一侧持续变化，索引可能陈旧；联合训练后的向量仍需以一致版本建库和评估。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>商品编码因新训练发生旋转，用户查询却沿旧方向打分，会破坏近邻关系；两个目标共同训练有助对齐，但服务索引也要按对应版本更新。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.23038">原论文</a> · <a href="../../../../reproductions/2607.23038-egr/">实现解读</a> · <a href="#qa-72f235af74f628cc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:egr" data-paper-title="EGR: Embedding-Native Generative Retrieval with a Shared LLM" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="EGR: Embedding-Native Generative Retrieval with a Shared LLM 搜广推与 LLM 应用 Snap Inc. 2026-07-25 同一编码骨干产生 item 索引向量和 user query 向量，并让 item representation learning 与 next-item prediction 全程联合训练。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 EGR 为 0.05025，相对变化 -6.95%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  retrieval generative-retrieval shared-encoder 搜广推 生成式召回与推理推荐 EGR 联合更新与先冻结 item encoder 再训练用户塔，有什么部署取舍？ 冻结稳定物品索引，用户目标却无法再修正物品空间；联合可持续对齐，但需要更新物品向量并保持服务版本一致。两种方案针对稳定性与适应性的取舍，来源本地负结果不能被共同训练的设计愿景取代。 示意：新 query 模型改变了科幻方向，若物品索引仍是旧版本，检索可能错位；冻结则更稳定，却无法修正旧空间难区分的问题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-aebfbc8434aabce5">EGR 联合更新与先冻结 item encoder 再训练用户塔，有什么部署取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aegr">EGR: Embedding-Native Generative Retrieval with a Shared LLM</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Snap Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冻结稳定物品索引，用户目标却无法再修正物品空间；联合可持续对齐，但需要更新物品向量并保持服务版本一致。两种方案针对稳定性与适应性的取舍，来源本地负结果不能被共同训练的设计愿景取代。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新 query 模型改变了科幻方向，若物品索引仍是旧版本，检索可能错位；冻结则更稳定，却无法修正旧空间难区分的问题。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.23038">原论文</a> · <a href="../../../../reproductions/2607.23038-egr/">实现解读</a> · <a href="#qa-aebfbc8434aabce5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:egr" data-paper-title="EGR: Embedding-Native Generative Retrieval with a Shared LLM" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="EGR: Embedding-Native Generative Retrieval with a Shared LLM 搜广推与 LLM 应用 Snap Inc. 2026-07-25 同一编码骨干产生 item 索引向量和 user query 向量，并让 item representation learning 与 next-item prediction 全程联合训练。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 EGR 为 0.05025，相对变化 -6.95%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  retrieval generative-retrieval shared-encoder 搜广推 生成式召回与推理推荐 EGR 的共享骨干更新后，为什么要校验 item 索引和 query 版本？ 两侧空间由同一参数约束，更新会改变点积含义，旧索引与新 query 不一定仍可比较。应记录重建、训练与切换边界，也确认 IRL 与 NIP 两项实际执行。仅共享类名而关闭一项损失，不满足全程联合训练定义。 示意：把物品向量留在旧坐标系、用户向量换到新坐标系，即使维度一样点积也可能无意义；版本化导出是实际接口要求。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-239efdbe5c28d9d1">EGR 的共享骨干更新后，为什么要校验 item 索引和 query 版本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aegr">EGR: Embedding-Native Generative Retrieval with a Shared LLM</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Snap Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两侧空间由同一参数约束，更新会改变点积含义，旧索引与新 query 不一定仍可比较。应记录重建、训练与切换边界，也确认 IRL 与 NIP 两项实际执行。仅共享类名而关闭一项损失，不满足全程联合训练定义。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把物品向量留在旧坐标系、用户向量换到新坐标系，即使维度一样点积也可能无意义；版本化导出是实际接口要求。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.23038">原论文</a> · <a href="../../../../reproductions/2607.23038-egr/">实现解读</a> · <a href="#qa-239efdbe5c28d9d1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:barge" data-paper-title="Bridging the Structural Gap: Adapting Autoregressive Generation for Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Bridging the Structural Gap: Adapting Autoregressive Generation for Recommendation 搜广推与 LLM 应用 Tencent 2026-07-23 RQ-VAE 把一个 item 展成多个 Semantic-ID token 后，普通 Transformer 会丢失 item 边界；单量化路径还会让早期 beam 偏差逐层放大。BARGE 用 ICA 将同一 item 的 token 聚合后门控回写，用 HPR 对累计语义路径做逐层对比重排，并通过正交切分产生两条互补解码路径。 Fidelity: 核心机制复现。实际训练 OSQ 双语义路径、ICA、HPR、双 decoder 与 item-space OR-fusion；缩小公开数据与服务规模。MovieLens genre 替代腾讯 item embedding；全库 teacher-forced path scoring 替代生产 beam kernel，未使用私有曝光负例和线上 serving。OSQ、ICA、HPR、DPD 均真实训练，但本地百分比不对应论文线上 lift。本地对照口径：基线是同 width、层数、训练行、optimizer 和 140 steps 的 single-path RQ-VAE/TIGER；  generative-recommendation semantic-id reranking 搜广推 生成式召回与推理推荐 BARGE 为什么认为一个物品的多枚 SID token 需要显式 item context？ SID 是同一物品的分解，普通序列注意力可能把各码当作独立事件，丢掉它们共同描述一个物品的边界。ICA 先在物品内部聚合上下文，再门控回写各码，保留整体与细节的连接。它修复的是编码组织，和跨物品历史的偏好关系仍是两个层面。 示意：一本书的主题、细分类和碰撞码应共同表示这一本书，不能把三枚码当成用户连续读了三本书；item context 把它们重新联系起来。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-barge-1cfb2666" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-321f5c75e23f3457">BARGE 为什么认为一个物品的多枚 SID token 需要显式 item context？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Abarge">Bridging the Structural Gap: Adapting Autoregressive Generation for Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>SID 是同一物品的分解，普通序列注意力可能把各码当作独立事件，丢掉它们共同描述一个物品的边界。ICA 先在物品内部聚合上下文，再门控回写各码，保留整体与细节的连接。它修复的是编码组织，和跨物品历史的偏好关系仍是两个层面。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一本书的主题、细分类和碰撞码应共同表示这一本书，不能把三枚码当成用户连续读了三本书；item context 把它们重新联系起来。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21028">原论文</a> · <a href="../../../../reproductions/2607.21028-barge/">实现解读</a> · <a href="#qa-321f5c75e23f3457">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:barge" data-paper-title="Bridging the Structural Gap: Adapting Autoregressive Generation for Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Bridging the Structural Gap: Adapting Autoregressive Generation for Recommendation 搜广推与 LLM 应用 Tencent 2026-07-23 RQ-VAE 把一个 item 展成多个 Semantic-ID token 后，普通 Transformer 会丢失 item 边界；单量化路径还会让早期 beam 偏差逐层放大。BARGE 用 ICA 将同一 item 的 token 聚合后门控回写，用 HPR 对累计语义路径做逐层对比重排，并通过正交切分产生两条互补解码路径。 Fidelity: 核心机制复现。实际训练 OSQ 双语义路径、ICA、HPR、双 decoder 与 item-space OR-fusion；缩小公开数据与服务规模。MovieLens genre 替代腾讯 item embedding；全库 teacher-forced path scoring 替代生产 beam kernel，未使用私有曝光负例和线上 serving。OSQ、ICA、HPR、DPD 均真实训练，但本地百分比不对应论文线上 lift。本地对照口径：基线是同 width、层数、训练行、optimizer 和 140 steps 的 single-path RQ-VAE/TIGER；  generative-recommendation semantic-id reranking 搜广推 生成式召回与推理推荐 BARGE为什么既修复同一物品的token边界，又对累计语义路径重排？ 一个物品被展开为多层SID后，普通序列注意力可能把局部码当独立事件，ICA先聚合物品上下文再门控回写。HPR则对已经生成的累计路径判断相关性，缓解早期beam偏差向深层扩散；互补量化路径进一步提供不同分解视角。三者分别处理表示边界、搜索误差和路径多样性。 示意：商品的三层码像同一地址的省、市、街道，不能当三次独立购买；若省级候选已选偏，后面只细分街道也难补救，因此要逐层检查路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-1164e6c8c83dd97c">BARGE为什么既修复同一物品的token边界，又对累计语义路径重排？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Abarge">Bridging the Structural Gap: Adapting Autoregressive Generation for Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一个物品被展开为多层SID后，普通序列注意力可能把局部码当独立事件，ICA先聚合物品上下文再门控回写。HPR则对已经生成的累计路径判断相关性，缓解早期beam偏差向深层扩散；互补量化路径进一步提供不同分解视角。三者分别处理表示边界、搜索误差和路径多样性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>商品的三层码像同一地址的省、市、街道，不能当三次独立购买；若省级候选已选偏，后面只细分街道也难补救，因此要逐层检查路径。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21028">原论文</a> · <a href="../../../../reproductions/2607.21028-barge/">实现解读</a> · <a href="#qa-1164e6c8c83dd97c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:barge" data-paper-title="Bridging the Structural Gap: Adapting Autoregressive Generation for Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Bridging the Structural Gap: Adapting Autoregressive Generation for Recommendation 搜广推与 LLM 应用 Tencent 2026-07-23 RQ-VAE 把一个 item 展成多个 Semantic-ID token 后，普通 Transformer 会丢失 item 边界；单量化路径还会让早期 beam 偏差逐层放大。BARGE 用 ICA 将同一 item 的 token 聚合后门控回写，用 HPR 对累计语义路径做逐层对比重排，并通过正交切分产生两条互补解码路径。 Fidelity: 核心机制复现。实际训练 OSQ 双语义路径、ICA、HPR、双 decoder 与 item-space OR-fusion；缩小公开数据与服务规模。MovieLens genre 替代腾讯 item embedding；全库 teacher-forced path scoring 替代生产 beam kernel，未使用私有曝光负例和线上 serving。OSQ、ICA、HPR、DPD 均真实训练，但本地百分比不对应论文线上 lift。本地对照口径：基线是同 width、层数、训练行、optimizer 和 140 steps 的 single-path RQ-VAE/TIGER；  generative-recommendation semantic-id reranking 搜广推 生成式召回与推理推荐 BARGE 的两条互补解码路径与单路径增加 beam width 相比，改变了什么搜索空间？ 加宽 beam 在同一编码结构下探索更多路径，两条正交子空间则先构造不同表示与量化视角，有机会避免同一早期偏差同时主导全部候选。HPR 再评价累计路径。多路径增加训练和合并成本，互补性仍需验证，不能把输出翻倍直接当成信息独立。 示意：单路径再宽可能仍围绕同一错误粗码扩展；另一子空间若保留不同语义线索，才有机会找到被第一路径遗漏的书，而不只是重复列相同书。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-63bc94c75b23ca7b">BARGE 的两条互补解码路径与单路径增加 beam width 相比，改变了什么搜索空间？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Abarge">Bridging the Structural Gap: Adapting Autoregressive Generation for Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>加宽 beam 在同一编码结构下探索更多路径，两条正交子空间则先构造不同表示与量化视角，有机会避免同一早期偏差同时主导全部候选。HPR 再评价累计路径。多路径增加训练和合并成本，互补性仍需验证，不能把输出翻倍直接当成信息独立。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>单路径再宽可能仍围绕同一错误粗码扩展；另一子空间若保留不同语义线索，才有机会找到被第一路径遗漏的书，而不只是重复列相同书。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21028">原论文</a> · <a href="../../../../reproductions/2607.21028-barge/">实现解读</a> · <a href="#qa-63bc94c75b23ca7b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:barge" data-paper-title="Bridging the Structural Gap: Adapting Autoregressive Generation for Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Bridging the Structural Gap: Adapting Autoregressive Generation for Recommendation 搜广推与 LLM 应用 Tencent 2026-07-23 RQ-VAE 把一个 item 展成多个 Semantic-ID token 后，普通 Transformer 会丢失 item 边界；单量化路径还会让早期 beam 偏差逐层放大。BARGE 用 ICA 将同一 item 的 token 聚合后门控回写，用 HPR 对累计语义路径做逐层对比重排，并通过正交切分产生两条互补解码路径。 Fidelity: 核心机制复现。实际训练 OSQ 双语义路径、ICA、HPR、双 decoder 与 item-space OR-fusion；缩小公开数据与服务规模。MovieLens genre 替代腾讯 item embedding；全库 teacher-forced path scoring 替代生产 beam kernel，未使用私有曝光负例和线上 serving。OSQ、ICA、HPR、DPD 均真实训练，但本地百分比不对应论文线上 lift。本地对照口径：基线是同 width、层数、训练行、optimizer 和 140 steps 的 single-path RQ-VAE/TIGER；  generative-recommendation semantic-id reranking 搜广推 生成式召回与推理推荐 BARGE 实现 HPR 时为何比较累计路径向量，而不只比较当前一级码？ 累计和包含从粗到细已经作出的选择，才能判断当前整条语义路线是否仍符合用户。只看本级码会忽略早期错误；推理融合的是生成 log-probability 与重排分，训练对累计路径做对比。DPD 的正交约束另作用于投影，不应混成同一损失或声称完全独立。 示意：细码“入门款”本身合理，但前缀已走进家居而用户要相机。累计路径会暴露整体偏离，只看最后一级就可能误把它留下。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-263c5784a60fb5af">BARGE 实现 HPR 时为何比较累计路径向量，而不只比较当前一级码？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Abarge">Bridging the Structural Gap: Adapting Autoregressive Generation for Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>累计和包含从粗到细已经作出的选择，才能判断当前整条语义路线是否仍符合用户。只看本级码会忽略早期错误；推理融合的是生成 log-probability 与重排分，训练对累计路径做对比。DPD 的正交约束另作用于投影，不应混成同一损失或声称完全独立。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>细码“入门款”本身合理，但前缀已走进家居而用户要相机。累计路径会暴露整体偏离，只看最后一级就可能误把它留下。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21028">原论文</a> · <a href="../../../../reproductions/2607.21028-barge/">实现解读</a> · <a href="#qa-263c5784a60fb5af">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tsgr" data-paper-title="TSGR: Taobao Search Generative Retrieval" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="TSGR: Taobao Search Generative Retrieval 搜广推与 LLM 应用 Taobao &amp; Tmall Group of Alibaba / Zhejiang University 2026-07-21 淘宝搜索的生成式召回不仅要找到相关商品，还要把商业价值直接带进生成路径。TSGR 先用 residual quantization 生成语义前缀，再为同一前缀下的商品并行分配全局价值码和 query-conditioned 价值码；最后用与生成 backbone 联合训练的 Value-aware Ranking Module（VRM）完成精细排序，避免把独立预排器硬接在生成器后面。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实执行并行价值 Semantic ID 和联合 VRM；私有淘宝日志与生产 serving 未复刻。本地在 MovieLens 100K 上真实构建两级 residual semantic prefix、全局/条件价值码，并用 23,027 个加权正例和 115,135 个负例拟合联合 VRM；融合权重只在 validation 上选择。  generative-retrieval semantic-id search pre-ranking 搜广推 生成式召回与推理推荐 TSGR为什么把商业价值编码进生成路径？ 只生成语义相关商品再外接独立预排，会割裂召回与价值目标。并行全局和query条件价值码配联合VRM，让生成状态与精细商业排序一起训练。 例如同语义候选中，当前query下更合适的交易价值可进入选择。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-tsgr-1abc60bc" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f23c7744979bd4a8">TSGR为什么把商业价值编码进生成路径？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atsgr">TSGR: Taobao Search Generative Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group of Alibaba / Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只生成语义相关商品再外接独立预排，会割裂召回与价值目标。并行全局和query条件价值码配联合VRM，让生成状态与精细商业排序一起训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同语义候选中，当前query下更合适的交易价值可进入选择。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.18796">原论文</a> · <a href="../../../../reproductions/2607.18796-tsgr/">实现解读</a> · <a href="#qa-f23c7744979bd4a8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tsgr" data-paper-title="TSGR: Taobao Search Generative Retrieval" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="TSGR: Taobao Search Generative Retrieval 搜广推与 LLM 应用 Taobao &amp; Tmall Group of Alibaba / Zhejiang University 2026-07-21 淘宝搜索的生成式召回不仅要找到相关商品，还要把商业价值直接带进生成路径。TSGR 先用 residual quantization 生成语义前缀，再为同一前缀下的商品并行分配全局价值码和 query-conditioned 价值码；最后用与生成 backbone 联合训练的 Value-aware Ranking Module（VRM）完成精细排序，避免把独立预排器硬接在生成器后面。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实执行并行价值 Semantic ID 和联合 VRM；私有淘宝日志与生产 serving 未复刻。本地在 MovieLens 100K 上真实构建两级 residual semantic prefix、全局/条件价值码，并用 23,027 个加权正例和 115,135 个负例拟合联合 VRM；融合权重只在 validation 上选择。  generative-retrieval semantic-id search pre-ranking 搜广推 生成式召回与推理推荐 TSGR 为什么在同一语义前缀下同时分配全局和 query-conditioned 价值码？ 语义前缀先组织商品相关性，但同一主题下的商业价值既有全局差异，也随查询而变。两套并行价值码把这两种信号带入生成路径，联合训练的 VRM 再结合生成状态与商品信息精细评分，避免完全独立的预排器割裂目标。价值代理与真实业务标签需区分，本地公开评分构造不能代表真实交易价值。 示意：同一款相机配件整体销量一般，但在“微距摄影”查询下很有价值。全局码表达总体表现，条件码表达该查询的特殊价值，精细模块再综合判断。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-3a964a889b237327">TSGR 为什么在同一语义前缀下同时分配全局和 query-conditioned 价值码？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atsgr">TSGR: Taobao Search Generative Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group of Alibaba / Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语义前缀先组织商品相关性，但同一主题下的商业价值既有全局差异，也随查询而变。两套并行价值码把这两种信号带入生成路径，联合训练的 VRM 再结合生成状态与商品信息精细评分，避免完全独立的预排器割裂目标。价值代理与真实业务标签需区分，本地公开评分构造不能代表真实交易价值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一款相机配件整体销量一般，但在“微距摄影”查询下很有价值。全局码表达总体表现，条件码表达该查询的特殊价值，精细模块再综合判断。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.18796">原论文</a> · <a href="../../../../reproductions/2607.18796-tsgr/">实现解读</a> · <a href="#qa-3a964a889b237327">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tsgr" data-paper-title="TSGR: Taobao Search Generative Retrieval" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="TSGR: Taobao Search Generative Retrieval 搜广推与 LLM 应用 Taobao &amp; Tmall Group of Alibaba / Zhejiang University 2026-07-21 淘宝搜索的生成式召回不仅要找到相关商品，还要把商业价值直接带进生成路径。TSGR 先用 residual quantization 生成语义前缀，再为同一前缀下的商品并行分配全局价值码和 query-conditioned 价值码；最后用与生成 backbone 联合训练的 Value-aware Ranking Module（VRM）完成精细排序，避免把独立预排器硬接在生成器后面。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实执行并行价值 Semantic ID 和联合 VRM；私有淘宝日志与生产 serving 未复刻。本地在 MovieLens 100K 上真实构建两级 residual semantic prefix、全局/条件价值码，并用 23,027 个加权正例和 115,135 个负例拟合联合 VRM；融合权重只在 validation 上选择。  generative-retrieval semantic-id search pre-ranking 搜广推 生成式召回与推理推荐 全局价值码与query-conditioned码为什么不能只留一种？ 全局反映跨query的总体价值，条件码表达特定需求下价值，两者参照不同。只留全局易偏头部，只留条件又需可靠query统计，不能用一个热度码冒充全部。 例如通用畅销商品在专业query中未必比小众适配款更有价值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-2d588b4c7cb0beac">全局价值码与query-conditioned码为什么不能只留一种？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atsgr">TSGR: Taobao Search Generative Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group of Alibaba / Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全局反映跨query的总体价值，条件码表达特定需求下价值，两者参照不同。只留全局易偏头部，只留条件又需可靠query统计，不能用一个热度码冒充全部。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如通用畅销商品在专业query中未必比小众适配款更有价值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.18796">原论文</a> · <a href="../../../../reproductions/2607.18796-tsgr/">实现解读</a> · <a href="#qa-2d588b4c7cb0beac">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tsgr" data-paper-title="TSGR: Taobao Search Generative Retrieval" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="TSGR: Taobao Search Generative Retrieval 搜广推与 LLM 应用 Taobao &amp; Tmall Group of Alibaba / Zhejiang University 2026-07-21 淘宝搜索的生成式召回不仅要找到相关商品，还要把商业价值直接带进生成路径。TSGR 先用 residual quantization 生成语义前缀，再为同一前缀下的商品并行分配全局价值码和 query-conditioned 价值码；最后用与生成 backbone 联合训练的 Value-aware Ranking Module（VRM）完成精细排序，避免把独立预排器硬接在生成器后面。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实执行并行价值 Semantic ID 和联合 VRM；私有淘宝日志与生产 serving 未复刻。本地在 MovieLens 100K 上真实构建两级 residual semantic prefix、全局/条件价值码，并用 23,027 个加权正例和 115,135 个负例拟合联合 VRM；融合权重只在 validation 上选择。  generative-retrieval semantic-id search pre-ranking 搜广推 生成式召回与推理推荐 TSGR本地ID和VRM实现应避免什么泄漏？ 价值统计和码分配只用训练时间数据，query条件与item身份对齐，VRM与backbone按协议联合更新。不能用测试转化率先造价值码，再称能预测未来商业收益。 例如将待预测订单金额编码到物品ID，会把答案直接写进输入。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-eea547b26501ff8d">TSGR本地ID和VRM实现应避免什么泄漏？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atsgr">TSGR: Taobao Search Generative Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group of Alibaba / Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>价值统计和码分配只用训练时间数据，query条件与item身份对齐，VRM与backbone按协议联合更新。不能用测试转化率先造价值码，再称能预测未来商业收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如将待预测订单金额编码到物品ID，会把答案直接写进输入。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.18796">原论文</a> · <a href="../../../../reproductions/2607.18796-tsgr/">实现解读</a> · <a href="#qa-eea547b26501ff8d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recgpt-v3" data-paper-title="RecGPT-V3 Technical Report" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="RecGPT-V3 Technical Report 搜广推与 LLM 应用 Alibaba / Taobao 2026-07-17 RecGPT-V1 把用户意图引入推荐链路，V2 用多智能体扩展推理，但每次请求仍重复读取最长约 55K token 的完整历史；自然语言 tag 到商品又形成有损瓶颈，显式 CoT 的数千 token 也无法承受高 QPS。V3 同时改造三处：Memory Hub 将完整行为压成带行为模式、偏好摘要、原始行为索引和时间信息的可追溯 memory unit；新行为只更新相关 unit 或创建新 unit。 Fidelity: 核心机制复现。实际训练两级 Semantic ID、结构化 Memory Hub、显式教师到 latent token 的重建蒸馏和 ranking-feedback；基础模型、数据与线上系统缩小。本地真实训练了两级 RQ-VAE、SID/text item tower、显式教师、memory attention、latent 多段重建和 dense ranking-feedback KL；MovieLens genre 替代淘宝文本/图像/属性，520 items 替代工业商品池，公开 teacher+popularity reward 替代生产 CTR ranker。  generative-recommendation semantic-id user-memory latent-reasoning 搜广推 生成式召回与推理推荐 RecGPT-V3 的 memory unit 为什么包含原始行为索引和时间，而不只一句偏好摘要？ 索引与时间让压缩知识可回溯到证据并增量更新，减少旧摘要无依据漂移；新行为只改相关单元，避免每次重读长史。可追溯不等于内容无损，也不能自动证明所谓因果信息准确，更新与过期规则仍关键。 示意：记录“近期准备露营”同时指向哪几次浏览与日期，后续需求改变时可更新对应单元，而不必依赖一条不知何时生成的旧句子。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-recgpt-v3-d1c7b19e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-506207a0481453a7">RecGPT-V3 的 memory unit 为什么包含原始行为索引和时间，而不只一句偏好摘要？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecgpt-v3">RecGPT-V3 Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>索引与时间让压缩知识可回溯到证据并增量更新，减少旧摘要无依据漂移；新行为只改相关单元，避免每次重读长史。可追溯不等于内容无损，也不能自动证明所谓因果信息准确，更新与过期规则仍关键。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>记录“近期准备露营”同时指向哪几次浏览与日期，后续需求改变时可更新对应单元，而不必依赖一条不知何时生成的旧句子。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.15591">原论文</a> · <a href="../../../../reproductions/2607.15591-recgpt-v3/">实现解读</a> · <a href="#qa-506207a0481453a7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recgpt-v3" data-paper-title="RecGPT-V3 Technical Report" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="RecGPT-V3 Technical Report 搜广推与 LLM 应用 Alibaba / Taobao 2026-07-17 RecGPT-V1 把用户意图引入推荐链路，V2 用多智能体扩展推理，但每次请求仍重复读取最长约 55K token 的完整历史；自然语言 tag 到商品又形成有损瓶颈，显式 CoT 的数千 token 也无法承受高 QPS。V3 同时改造三处：Memory Hub 将完整行为压成带行为模式、偏好摘要、原始行为索引和时间信息的可追溯 memory unit；新行为只更新相关 unit 或创建新 unit。 Fidelity: 核心机制复现。实际训练两级 Semantic ID、结构化 Memory Hub、显式教师到 latent token 的重建蒸馏和 ranking-feedback；基础模型、数据与线上系统缩小。本地真实训练了两级 RQ-VAE、SID/text item tower、显式教师、memory attention、latent 多段重建和 dense ranking-feedback KL；MovieLens genre 替代淘宝文本/图像/属性，520 items 替代工业商品池，公开 teacher+popularity reward 替代生产 CTR ranker。  generative-recommendation semantic-id user-memory latent-reasoning 搜广推 生成式召回与推理推荐 RecGPT-V3 为什么同时改记忆、商品接口和推理表示，而不是只压缩显式 CoT？ 仅压缩 CoT 仍会反复读取长历史，也保留自然语言标签映射商品的损失。Memory Hub 增量更新可追溯记忆单元，SID 连接模型与实际商品，潜在 token 再减少输出推理文本的成本。三者分别针对输入重算、输出落地与解码开销；生产排序反馈还参与对齐，不能把总体收益归因于单个压缩步骤。 示意：新增一次相机浏览时，只更新相关摄影记忆，而非重读所有历史；生成器直接输出商品码，内部短推理提供支持。三处节省来自不同环节，不能只统计少写了多少字。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-7fce71e69a1528f4">RecGPT-V3 为什么同时改记忆、商品接口和推理表示，而不是只压缩显式 CoT？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecgpt-v3">RecGPT-V3 Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>仅压缩 CoT 仍会反复读取长历史，也保留自然语言标签映射商品的损失。Memory Hub 增量更新可追溯记忆单元，SID 连接模型与实际商品，潜在 token 再减少输出推理文本的成本。三者分别针对输入重算、输出落地与解码开销；生产排序反馈还参与对齐，不能把总体收益归因于单个压缩步骤。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新增一次相机浏览时，只更新相关摄影记忆，而非重读所有历史；生成器直接输出商品码，内部短推理提供支持。三处节省来自不同环节，不能只统计少写了多少字。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.15591">原论文</a> · <a href="../../../../reproductions/2607.15591-recgpt-v3/">实现解读</a> · <a href="#qa-7fce71e69a1528f4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recgpt-v3" data-paper-title="RecGPT-V3 Technical Report" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="RecGPT-V3 Technical Report 搜广推与 LLM 应用 Alibaba / Taobao 2026-07-17 RecGPT-V1 把用户意图引入推荐链路，V2 用多智能体扩展推理，但每次请求仍重复读取最长约 55K token 的完整历史；自然语言 tag 到商品又形成有损瓶颈，显式 CoT 的数千 token 也无法承受高 QPS。V3 同时改造三处：Memory Hub 将完整行为压成带行为模式、偏好摘要、原始行为索引和时间信息的可追溯 memory unit；新行为只更新相关 unit 或创建新 unit。 Fidelity: 核心机制复现。实际训练两级 Semantic ID、结构化 Memory Hub、显式教师到 latent token 的重建蒸馏和 ranking-feedback；基础模型、数据与线上系统缩小。本地真实训练了两级 RQ-VAE、SID/text item tower、显式教师、memory attention、latent 多段重建和 dense ranking-feedback KL；MovieLens genre 替代淘宝文本/图像/属性，520 items 替代工业商品池，公开 teacher+popularity reward 替代生产 CTR ranker。  generative-recommendation semantic-id user-memory latent-reasoning 搜广推 生成式召回与推理推荐 latent internalization 与直接删掉显式 CoT，相比训练多了什么保障？ 分段、跨段和全链重建让潜 token 学习承接教师信息，直接删文本只省输出却未传知识。重建相似仍不证明步骤忠实，教师质量与冻结时机也影响结果。来源先同步漂移失败、后预热冻结才正向，应保留这一边界而非只看最终增益。 示意：让内部四个槽学会支持原解释，与上线直接不输出解释不同；若教师也同时随学生漂移，二者可能互相追逐而失去稳定目标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f3e873b9a1426179">latent internalization 与直接删掉显式 CoT，相比训练多了什么保障？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecgpt-v3">RecGPT-V3 Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分段、跨段和全链重建让潜 token 学习承接教师信息，直接删文本只省输出却未传知识。重建相似仍不证明步骤忠实，教师质量与冻结时机也影响结果。来源先同步漂移失败、后预热冻结才正向，应保留这一边界而非只看最终增益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>让内部四个槽学会支持原解释，与上线直接不输出解释不同；若教师也同时随学生漂移，二者可能互相追逐而失去稳定目标。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.15591">原论文</a> · <a href="../../../../reproductions/2607.15591-recgpt-v3/">实现解读</a> · <a href="#qa-f3e873b9a1426179">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recgpt-v3" data-paper-title="RecGPT-V3 Technical Report" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="RecGPT-V3 Technical Report 搜广推与 LLM 应用 Alibaba / Taobao 2026-07-17 RecGPT-V1 把用户意图引入推荐链路，V2 用多智能体扩展推理，但每次请求仍重复读取最长约 55K token 的完整历史；自然语言 tag 到商品又形成有损瓶颈，显式 CoT 的数千 token 也无法承受高 QPS。V3 同时改造三处：Memory Hub 将完整行为压成带行为模式、偏好摘要、原始行为索引和时间信息的可追溯 memory unit；新行为只更新相关 unit 或创建新 unit。 Fidelity: 核心机制复现。实际训练两级 Semantic ID、结构化 Memory Hub、显式教师到 latent token 的重建蒸馏和 ranking-feedback；基础模型、数据与线上系统缩小。本地真实训练了两级 RQ-VAE、SID/text item tower、显式教师、memory attention、latent 多段重建和 dense ranking-feedback KL；MovieLens genre 替代淘宝文本/图像/属性，520 items 替代工业商品池，公开 teacher+popularity reward 替代生产 CTR ranker。  generative-recommendation semantic-id user-memory latent-reasoning 搜广推 生成式召回与推理推荐 RecGPT-V3 本地多轮迭代后的最终数字，为什么要标明选择过程与头部变化？ 配置经过教师预热与冻结等调整，最终单 seed 是选中设置，不能冒充预注册稳定结论；head share 同时增，说明可能借热门捷径。memory 与 latent token 减少是结构计数，不等于生产延迟或真实 14B 效益测量。 示意：从四十事件压到十四输入说明预算变化，却不能按比例承诺快百分之六十五；内核、缓存与计算密度仍决定实际时间。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-04acbce36f43f346">RecGPT-V3 本地多轮迭代后的最终数字，为什么要标明选择过程与头部变化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecgpt-v3">RecGPT-V3 Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>配置经过教师预热与冻结等调整，最终单 seed 是选中设置，不能冒充预注册稳定结论；head share 同时增，说明可能借热门捷径。memory 与 latent token 减少是结构计数，不等于生产延迟或真实 14B 效益测量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>从四十事件压到十四输入说明预算变化，却不能按比例承诺快百分之六十五；内核、缓存与计算密度仍决定实际时间。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.15591">原论文</a> · <a href="../../../../reproductions/2607.15591-recgpt-v3/">实现解读</a> · <a href="#qa-04acbce36f43f346">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:guess-where-you-go" data-paper-title="Guess Where You Go: Generative Next Point-of-Interest Recommendation in Amap" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Guess Where You Go: Generative Next Point-of-Interest Recommendation in Amap 搜广推与 LLM 应用 Amap / Alibaba 2026-07-13 把下一 POI 编成 Semantic ID 序列，并用时空特征、课程式预训练/SFT 与 EAKTO 强化优化长周期用户反馈。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation next-poi semantic-id reinforcement-learning 搜广推 生成式召回与推理推荐 下一 POI 生成为什么比普通内容推荐更依赖时空条件？ 地点可达性、当前区域与时间共同决定合理去向，同一个名字的地点也受营业和旅程阶段影响。SID 提供离散生成接口，时空条件决定此刻哪些路径有意义。只学地点共现可能得到语义相近却无法到达的候选。 示意：午间在上海办公区更可能去附近餐饮，不能因历史喜欢北京咖啡馆就跨城推荐；地点语义相似不足以替代当前可达性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-guess-where-you-go-0a00ce9c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5c0182623a051bb9">下一 POI 生成为什么比普通内容推荐更依赖时空条件？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aguess-where-you-go">Guess Where You Go: Generative Next Point-of-Interest Recommendation in Amap</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Amap / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>地点可达性、当前区域与时间共同决定合理去向，同一个名字的地点也受营业和旅程阶段影响。SID 提供离散生成接口，时空条件决定此刻哪些路径有意义。只学地点共现可能得到语义相近却无法到达的候选。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>午间在上海办公区更可能去附近餐饮，不能因历史喜欢北京咖啡馆就跨城推荐；地点语义相似不足以替代当前可达性。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26073">原论文</a> · <a href="../../../../reproductions/2607.26073-guess-where-you-go/">实现解读</a> · <a href="#qa-5c0182623a051bb9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:guess-where-you-go" data-paper-title="Guess Where You Go: Generative Next Point-of-Interest Recommendation in Amap" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Guess Where You Go: Generative Next Point-of-Interest Recommendation in Amap 搜广推与 LLM 应用 Amap / Alibaba 2026-07-13 把下一 POI 编成 Semantic ID 序列，并用时空特征、课程式预训练/SFT 与 EAKTO 强化优化长周期用户反馈。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation next-poi semantic-id reinforcement-learning 搜广推 生成式召回与推理推荐 下一POI生成为什么需要时空上下文，不能只把地点名当普通商品ID？ 地点选择受距离、时间与出行状态限制，相同兴趣在不同位置未必可执行。语义ID提供层次表示，时空特征限定当前需求，课程式训练再逐步适应更复杂反馈。长期奖励优化仍需要对应观测，不能把静态地点共现或一次命中直接当真实路线规划与长期出行收益。 示意：用户喜欢咖啡馆，但早晨上班途中和周末远游时可去的店不同；模型要结合当前时间与位置，而不能只重复历史里最常访问的店名。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-51385eee77e0ff0e">下一POI生成为什么需要时空上下文，不能只把地点名当普通商品ID？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aguess-where-you-go">Guess Where You Go: Generative Next Point-of-Interest Recommendation in Amap</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Amap / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>地点选择受距离、时间与出行状态限制，相同兴趣在不同位置未必可执行。语义ID提供层次表示，时空特征限定当前需求，课程式训练再逐步适应更复杂反馈。长期奖励优化仍需要对应观测，不能把静态地点共现或一次命中直接当真实路线规划与长期出行收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户喜欢咖啡馆，但早晨上班途中和周末远游时可去的店不同；模型要结合当前时间与位置，而不能只重复历史里最常访问的店名。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26073">原论文</a> · <a href="../../../../reproductions/2607.26073-guess-where-you-go/">实现解读</a> · <a href="#qa-51385eee77e0ff0e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:guess-where-you-go" data-paper-title="Guess Where You Go: Generative Next Point-of-Interest Recommendation in Amap" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Guess Where You Go: Generative Next Point-of-Interest Recommendation in Amap 搜广推与 LLM 应用 Amap / Alibaba 2026-07-13 把下一 POI 编成 Semantic ID 序列，并用时空特征、课程式预训练/SFT 与 EAKTO 强化优化长周期用户反馈。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation next-poi semantic-id reinforcement-learning 搜广推 生成式召回与推理推荐 课程预训练/SFT 与直接按长期反馈更新 POI 策略，分别解决什么学习阶段？ 课程与监督先建立地点语义、时空关系和基本生成能力，反馈优化再调整长周期偏好，避免从稀疏奖励从零探索巨大空间。二者都依赖数据定义，公开电影代理缺少真实移动限制，不能当作 POI 能力结果。 示意：先学合法地区与出行序列，再用后续满意度调整路线；仅靠一次正负反馈很难从零学会所有城市地点关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-36999f29a5d3cc4f">课程预训练/SFT 与直接按长期反馈更新 POI 策略，分别解决什么学习阶段？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aguess-where-you-go">Guess Where You Go: Generative Next Point-of-Interest Recommendation in Amap</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Amap / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>课程与监督先建立地点语义、时空关系和基本生成能力，反馈优化再调整长周期偏好，避免从稀疏奖励从零探索巨大空间。二者都依赖数据定义，公开电影代理缺少真实移动限制，不能当作 POI 能力结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先学合法地区与出行序列，再用后续满意度调整路线；仅靠一次正负反馈很难从零学会所有城市地点关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26073">原论文</a> · <a href="../../../../reproductions/2607.26073-guess-where-you-go/">实现解读</a> · <a href="#qa-36999f29a5d3cc4f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:guess-where-you-go" data-paper-title="Guess Where You Go: Generative Next Point-of-Interest Recommendation in Amap" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Guess Where You Go: Generative Next Point-of-Interest Recommendation in Amap 搜广推与 LLM 应用 Amap / Alibaba 2026-07-13 把下一 POI 编成 Semantic ID 序列，并用时空特征、课程式预训练/SFT 与 EAKTO 强化优化长周期用户反馈。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation next-poi semantic-id reinforcement-learning 搜广推 生成式召回与推理推荐 实现 POI SID 生成时，哪些训练标签不能变成请求特征？ 目标地点及未来停留反馈可用于损失，当前输入只能包含已发生轨迹与当时可知时空信息；不能把下一站坐标提前用于筛选。生成码映射需对应同版本地点目录，公开 proxy 的混合分数不等于原文全流程策略训练。 示意：为了缩小候选而先用真实下一站所在商圈过滤，就泄漏了目标；应按当前区域和合法约束构造候选，再检验是否预测到下一站。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6eb83c37777015f5">实现 POI SID 生成时，哪些训练标签不能变成请求特征？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aguess-where-you-go">Guess Where You Go: Generative Next Point-of-Interest Recommendation in Amap</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Amap / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标地点及未来停留反馈可用于损失，当前输入只能包含已发生轨迹与当时可知时空信息；不能把下一站坐标提前用于筛选。生成码映射需对应同版本地点目录，公开 proxy 的混合分数不等于原文全流程策略训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>为了缩小候选而先用真实下一站所在商圈过滤，就泄漏了目标；应按当前区域和合法约束构造候选，再检验是否预测到下一站。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26073">原论文</a> · <a href="../../../../reproductions/2607.26073-guess-where-you-go/">实现解读</a> · <a href="#qa-6eb83c37777015f5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rag-generation" data-paper-title="Recommendation as Generation: Unifying Personalized Video Generation and Recommendation at Industrial Scale" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Recommendation as Generation: Unifying Personalized Video Generation and Recommendation at Industrial Scale 搜广推与 LLM 应用 Kuaishou / Beihang University 2026-06-24 用解耦语义 ID 连接生成式推荐与兴趣条件视频生成，并以跨域 reward 协调候选选择和内容创建。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 RaG 为 0.04235，相对变化 -21.59%。仅验证 D-SID 接口，视频生成器未复刻；生产线上 lift 的外推不适用。  generative-recommendation semantic-id video-generation 搜广推 生成式召回与推理推荐 RaG 的检索命中率能否单独评价新生成视频的质量？ 不能。检索指标检查既有候选是否符合目标，视频质量还涉及生成结果的视觉、事实与兴趣一致性，两个输出空间不同。D-SID 只提供衔接接口，不把检索正确自动转成制作成功。来源本地未复刻视频生成器，不能用排序数字填补这项证据。 示意：系统选对“露营教学”主题，却生成违反物理常识的画面，检索可命中、视频仍失败；反过来画面精美也不代表内容适合用户。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-rag-generation-6f1ef070" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d0026c4f21594df2">RaG 的检索命中率能否单独评价新生成视频的质量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arag-generation">Recommendation as Generation: Unifying Personalized Video Generation and Recommendation at Industrial Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou / Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。检索指标检查既有候选是否符合目标，视频质量还涉及生成结果的视觉、事实与兴趣一致性，两个输出空间不同。D-SID 只提供衔接接口，不把检索正确自动转成制作成功。来源本地未复刻视频生成器，不能用排序数字填补这项证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>系统选对“露营教学”主题，却生成违反物理常识的画面，检索可命中、视频仍失败；反过来画面精美也不代表内容适合用户。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.25496">原论文</a> · <a href="../../../../reproductions/2606.25496-rag-generation/">实现解读</a> · <a href="#qa-d0026c4f21594df2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rag-generation" data-paper-title="Recommendation as Generation: Unifying Personalized Video Generation and Recommendation at Industrial Scale" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Recommendation as Generation: Unifying Personalized Video Generation and Recommendation at Industrial Scale 搜广推与 LLM 应用 Kuaishou / Beihang University 2026-06-24 用解耦语义 ID 连接生成式推荐与兴趣条件视频生成，并以跨域 reward 协调候选选择和内容创建。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 RaG 为 0.04235，相对变化 -21.59%。仅验证 D-SID 接口，视频生成器未复刻；生产线上 lift 的外推不适用。  generative-recommendation semantic-id video-generation 搜广推 生成式召回与推理推荐 RaG 为什么用解耦 SID 连接推荐选择和内容生成，而不是把两者当成同一个输出任务？ 推荐需要在既有内容中找到合适对象，内容生成还要控制创作属性，两类信息若混在单一编码里会互相牵制。解耦 SID 为内容与创意因素提供接口，再以跨域奖励协调“推荐什么”和“怎样生成”。接口一致不代表已实现完整生成器；本地只验证离散接口，不能据此宣称视频生成质量或端到端业务收益。 示意：用户偏好露营教学，内容码表达露营主题，创意码控制镜头或呈现方式。推荐侧先判断主题是否合适，生成侧再按创意条件制作，二者共享接口而职责不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-151971fc5f0ff942">RaG 为什么用解耦 SID 连接推荐选择和内容生成，而不是把两者当成同一个输出任务？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arag-generation">Recommendation as Generation: Unifying Personalized Video Generation and Recommendation at Industrial Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou / Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>推荐需要在既有内容中找到合适对象，内容生成还要控制创作属性，两类信息若混在单一编码里会互相牵制。解耦 SID 为内容与创意因素提供接口，再以跨域奖励协调“推荐什么”和“怎样生成”。接口一致不代表已实现完整生成器；本地只验证离散接口，不能据此宣称视频生成质量或端到端业务收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户偏好露营教学，内容码表达露营主题，创意码控制镜头或呈现方式。推荐侧先判断主题是否合适，生成侧再按创意条件制作，二者共享接口而职责不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.25496">原论文</a> · <a href="../../../../reproductions/2606.25496-rag-generation/">实现解读</a> · <a href="#qa-151971fc5f0ff942">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rag-generation" data-paper-title="Recommendation as Generation: Unifying Personalized Video Generation and Recommendation at Industrial Scale" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Recommendation as Generation: Unifying Personalized Video Generation and Recommendation at Industrial Scale 搜广推与 LLM 应用 Kuaishou / Beihang University 2026-06-24 用解耦语义 ID 连接生成式推荐与兴趣条件视频生成，并以跨域 reward 协调候选选择和内容创建。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 RaG 为 0.04235，相对变化 -21.59%。仅验证 D-SID 接口，视频生成器未复刻；生产线上 lift 的外推不适用。  generative-recommendation semantic-id video-generation 搜广推 生成式召回与推理推荐 RaG 的跨域 reward 与只优化生成视觉质量，相比评价链路扩展到哪里？ 视觉质量只判断作品好不好看，跨域反馈还关注生成内容是否适合推荐用户，并协调候选选择与内容创建。奖励可能冲突或不可验证，不能由一个代理分数证明真实视频质量与个性化同时提升。来源本地只验证 D-SID 接口，未复刻生成器。 示意：画面精美的攀岩片对只想学轻松露营的人未必有用；推荐反馈要求主题契合，但仅关键词命中又无法判断视频是否真实可看。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-14e25ecd90c38481">RaG 的跨域 reward 与只优化生成视觉质量，相比评价链路扩展到哪里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arag-generation">Recommendation as Generation: Unifying Personalized Video Generation and Recommendation at Industrial Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou / Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>视觉质量只判断作品好不好看，跨域反馈还关注生成内容是否适合推荐用户，并协调候选选择与内容创建。奖励可能冲突或不可验证，不能由一个代理分数证明真实视频质量与个性化同时提升。来源本地只验证 D-SID 接口，未复刻生成器。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>画面精美的攀岩片对只想学轻松露营的人未必有用；推荐反馈要求主题契合，但仅关键词命中又无法判断视频是否真实可看。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.25496">原论文</a> · <a href="../../../../reproductions/2606.25496-rag-generation/">实现解读</a> · <a href="#qa-14e25ecd90c38481">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rag-generation" data-paper-title="Recommendation as Generation: Unifying Personalized Video Generation and Recommendation at Industrial Scale" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Recommendation as Generation: Unifying Personalized Video Generation and Recommendation at Industrial Scale 搜广推与 LLM 应用 Kuaishou / Beihang University 2026-06-24 用解耦语义 ID 连接生成式推荐与兴趣条件视频生成，并以跨域 reward 协调候选选择和内容创建。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 RaG 为 0.04235，相对变化 -21.59%。仅验证 D-SID 接口，视频生成器未复刻；生产线上 lift 的外推不适用。  generative-recommendation semantic-id video-generation 搜广推 生成式召回与推理推荐 RaG 本地仅实现 D-SID 时，哪些产物才能证明完整视频生成另已完成？ 需要真实生成模型与版本、条件输入、输出视频、训练或推理命令及质量评估，而非两个码向量和排序指标。接口测试只能说明内容与创作分量可传递，不能把未运行路径算实现。原论文线上收益也不能填补本地缺口。 示意：返回一对整数 content/creative 证明编码接口能调用，不等于生成了任何视频；把占位文件名当媒体产物更无法支持视觉效果声明。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c98a66fe78f4cef1">RaG 本地仅实现 D-SID 时，哪些产物才能证明完整视频生成另已完成？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arag-generation">Recommendation as Generation: Unifying Personalized Video Generation and Recommendation at Industrial Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou / Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>需要真实生成模型与版本、条件输入、输出视频、训练或推理命令及质量评估，而非两个码向量和排序指标。接口测试只能说明内容与创作分量可传递，不能把未运行路径算实现。原论文线上收益也不能填补本地缺口。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>返回一对整数 content/creative 证明编码接口能调用，不等于生成了任何视频；把占位文件名当媒体产物更无法支持视觉效果声明。</p>
<p class="ar-learning-sources">依据：本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.25496">原论文</a> · <a href="../../../../reproductions/2606.25496-rag-generation/">实现解读</a> · <a href="#qa-c98a66fe78f4cef1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:qgs" data-paper-title="From Item-Only to Query-Item: Query-Conditioned Generative Search with QGS in Quark" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="From Item-Only to Query-Item: Query-Conditioned Generative Search with QGS in Quark 搜广推与 LLM 应用 University of Science and Technology of China / Alibaba 2026-05-25 将 query 与 item 共同序列化做生成式搜索，Linear HSTU 以线性复杂度编码历史，HFG-Attention 再融合稀疏交叉特征。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-search search-ranking long-sequence 搜广推 生成式召回与推理推荐 QGS 的条件概率连乘，为什么描述一条完整生成路径而不是每一步各选最高分就够了？ p(y|q,h) 将各步在已有前缀下的条件概率相乘，后一步依赖前面已选输出。局部最高不必构成最高联合概率路径，比较时通常累加 log 概率并遵循目录合法性。这个基础关系不等于 QGS 全套搜索已被本地代理实现。 示意：首步甲概率稍高，但其合法后继都很弱；首步乙略低却有强后继，完整路径乙可能更可信，逐步贪心会漏掉它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-qgs-de75c3ea" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-3d9204e340d23d84">QGS 的条件概率连乘，为什么描述一条完整生成路径而不是每一步各选最高分就够了？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aqgs">From Item-Only to Query-Item: Query-Conditioned Generative Search with QGS in Quark</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>p(y|q,h) 将各步在已有前缀下的条件概率相乘，后一步依赖前面已选输出。局部最高不必构成最高联合概率路径，比较时通常累加 log 概率并遵循目录合法性。这个基础关系不等于 QGS 全套搜索已被本地代理实现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>首步甲概率稍高，但其合法后继都很弱；首步乙略低却有强后继，完整路径乙可能更可信，逐步贪心会漏掉它。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.25514">原论文</a> · <a href="../../../../reproductions/2605.25514-qgs/">实现解读</a> · <a href="#qa-3d9204e340d23d84">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:qgs" data-paper-title="From Item-Only to Query-Item: Query-Conditioned Generative Search with QGS in Quark" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="From Item-Only to Query-Item: Query-Conditioned Generative Search with QGS in Quark 搜广推与 LLM 应用 University of Science and Technology of China / Alibaba 2026-05-25 将 query 与 item 共同序列化做生成式搜索，Linear HSTU 以线性复杂度编码历史，HFG-Attention 再融合稀疏交叉特征。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-search search-ranking long-sequence 搜广推 生成式召回与推理推荐 QGS 为什么将 query 与 item 共同序列化，还要用特征交互模块补充历史编码？ 共同序列化使生成概率直接以当前查询和历史为条件，模型在生成物品路径时就处理搜索意图，而非先给出通用用户向量。历史编码控制长上下文开销，HFG-Attention 再融合稀疏字段交叉，补足仅靠序列表示难覆盖的异构关系。这里的效率设计属于该具体结构，不能推广成所有 HSTU 注意力都线性。 示意：同一用户搜索“旅行相机”和“室内灯具”应走不同生成路径。查询进入序列后，历史被按当前意图解释；设备、地区等稀疏字段再通过交互模块影响候选选择。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-9c44591d27ec4e42">QGS 为什么将 query 与 item 共同序列化，还要用特征交互模块补充历史编码？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aqgs">From Item-Only to Query-Item: Query-Conditioned Generative Search with QGS in Quark</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共同序列化使生成概率直接以当前查询和历史为条件，模型在生成物品路径时就处理搜索意图，而非先给出通用用户向量。历史编码控制长上下文开销，HFG-Attention 再融合稀疏字段交叉，补足仅靠序列表示难覆盖的异构关系。这里的效率设计属于该具体结构，不能推广成所有 HSTU 注意力都线性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一用户搜索“旅行相机”和“室内灯具”应走不同生成路径。查询进入序列后，历史被按当前意图解释；设备、地区等稀疏字段再通过交互模块影响候选选择。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.25514">原论文</a> · <a href="../../../../reproductions/2605.25514-qgs/">实现解读</a> · <a href="#qa-9c44591d27ec4e42">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:qgs" data-paper-title="From Item-Only to Query-Item: Query-Conditioned Generative Search with QGS in Quark" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="From Item-Only to Query-Item: Query-Conditioned Generative Search with QGS in Quark 搜广推与 LLM 应用 University of Science and Technology of China / Alibaba 2026-05-25 将 query 与 item 共同序列化做生成式搜索，Linear HSTU 以线性复杂度编码历史，HFG-Attention 再融合稀疏交叉特征。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-search search-ranking long-sequence 搜广推 生成式召回与推理推荐 QGS 的 Linear HSTU 与普通 HSTU，为什么不能只凭同名算同复杂度？ 线性版本需要特定核近似或重排条件，普通 SiLU(QKᵀ)V 仍含两两矩阵。HFG 特征融合又是另一项成本，不能只写长度线性就忽略维度和字段。来源简要正文不提供所有实现细节时，应限定结论而非猜核公式。 示意：去掉 softmax 并没有自动消除 N×N 关系矩阵；只有真实改写或稀疏结构执行后，才可讨论对应长序列成本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e11df1e8a7b730ad">QGS 的 Linear HSTU 与普通 HSTU，为什么不能只凭同名算同复杂度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aqgs">From Item-Only to Query-Item: Query-Conditioned Generative Search with QGS in Quark</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>线性版本需要特定核近似或重排条件，普通 SiLU(QKᵀ)V 仍含两两矩阵。HFG 特征融合又是另一项成本，不能只写长度线性就忽略维度和字段。来源简要正文不提供所有实现细节时，应限定结论而非猜核公式。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>去掉 softmax 并没有自动消除 N×N 关系矩阵；只有真实改写或稀疏结构执行后，才可讨论对应长序列成本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.25514">原论文</a> · <a href="../../../../reproductions/2605.25514-qgs/">实现解读</a> · <a href="#qa-e11df1e8a7b730ad">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:qgs" data-paper-title="From Item-Only to Query-Item: Query-Conditioned Generative Search with QGS in Quark" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="From Item-Only to Query-Item: Query-Conditioned Generative Search with QGS in Quark 搜广推与 LLM 应用 University of Science and Technology of China / Alibaba 2026-05-25 将 query 与 item 共同序列化做生成式搜索，Linear HSTU 以线性复杂度编码历史，HFG-Attention 再融合稀疏交叉特征。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-search search-ranking long-sequence 搜广推 生成式召回与推理推荐 QGS 本地 +0.73% NDCG 为什么不足以验证全文生成链路与线性 kernel？ 本地共享 scorer 上核心代理改变分数，没有真实工业 query 日志和完整 kernel 吞吐测量。需要分别核验联合输入、合法生成、字段交互及注意力实现，不能用最终排名标量证明所有组件存在；Hit 下降也需一起保留。 示意：给电影转移分加一项交叉可改变 NDCG，却没有产生任何 SID 解码轨迹，不能因此声称生成式搜索和线性注意力都已跑通。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-2af98e529550f6e3">QGS 本地 +0.73% NDCG 为什么不足以验证全文生成链路与线性 kernel？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aqgs">From Item-Only to Query-Item: Query-Conditioned Generative Search with QGS in Quark</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>本地共享 scorer 上核心代理改变分数，没有真实工业 query 日志和完整 kernel 吞吐测量。需要分别核验联合输入、合法生成、字段交互及注意力实现，不能用最终排名标量证明所有组件存在；Hit 下降也需一起保留。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>给电影转移分加一项交叉可改变 NDCG，却没有产生任何 SID 解码轨迹，不能因此声称生成式搜索和线性注意力都已跑通。</p>
<p class="ar-learning-sources">依据：本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.25514">原论文</a> · <a href="../../../../reproductions/2605.25514-qgs/">实现解读</a> · <a href="#qa-2af98e529550f6e3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:growthgr" data-paper-title="Towards Sustainable Growth: A Multi-Value-Aware Retrieval Framework for E-Commerce Search" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Towards Sustainable Growth: A Multi-Value-Aware Retrieval Framework for E-Commerce Search 搜广推与 LLM 应用 Alibaba Group / Taobao &amp; Tmall 2026-05-18 新品只按即时成交优化会持续缺曝光。GrowthGR 用 counterfactual ItemLTV 估计点击带来的长期订单增量，再以 RQ-VAE SID 和 decoder-only generator 召回；MoPO 联合购买、点击、曝光、排序和高 uplift 标签，并用 clipped inverse propensity 强化稀有高价值物品。 Fidelity: 核心机制复现。ItemLTV、三层 Semantic ID、NTP、MoPO/GRPO clipped update 与有效 SID 约束均实际执行。未来正反馈频次代理 7 日订单，公开数据不支持还原真实搜索漏斗和多模态商品 foundation embedding。本地对照口径：基线是同一 transition policy 的 NTP retrieval；实验组 GrowthGR 加入 ItemLTV 与 8 轮 MoPO，相对基线 Hit@10 +0.00%、NDCG@10 +2.05%。  generative-recommendation reinforcement-learning new-items 搜广推 生成式召回与推理推荐 GrowthGR 为什么用 ItemLTV 而不是只看新品即时成交？ 新品初始曝光少，单看即时成交会继续压低分发，难看到一次点击带来的长期订单变化。ItemLTV 分开基准与增量分量，MoPO 再将多种行为目标接到生成策略。长期代理需有可信反事实假设，模型输出增量并不自动成立因果解释。 示意：一次新品点击当天没买，却可能后续带来系列购买；仅看当天成交会错过这类潜力，但预测长期潜力也必须接受真实反馈检验。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-growthgr-aa9df061" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-caed8bc40762fb5b">GrowthGR 为什么用 ItemLTV 而不是只看新品即时成交？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agrowthgr">Towards Sustainable Growth: A Multi-Value-Aware Retrieval Framework for E-Commerce Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group / Taobao &amp; Tmall</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>新品初始曝光少，单看即时成交会继续压低分发，难看到一次点击带来的长期订单变化。ItemLTV 分开基准与增量分量，MoPO 再将多种行为目标接到生成策略。长期代理需有可信反事实假设，模型输出增量并不自动成立因果解释。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次新品点击当天没买，却可能后续带来系列购买；仅看当天成交会错过这类潜力，但预测长期潜力也必须接受真实反馈检验。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.17994">原论文</a> · <a href="../../../../reproductions/2605.17994-growthgr/">实现解读</a> · <a href="#qa-caed8bc40762fb5b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:growthgr" data-paper-title="Towards Sustainable Growth: A Multi-Value-Aware Retrieval Framework for E-Commerce Search" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Towards Sustainable Growth: A Multi-Value-Aware Retrieval Framework for E-Commerce Search 搜广推与 LLM 应用 Alibaba Group / Taobao &amp; Tmall 2026-05-18 新品只按即时成交优化会持续缺曝光。GrowthGR 用 counterfactual ItemLTV 估计点击带来的长期订单增量，再以 RQ-VAE SID 和 decoder-only generator 召回；MoPO 联合购买、点击、曝光、排序和高 uplift 标签，并用 clipped inverse propensity 强化稀有高价值物品。 Fidelity: 核心机制复现。ItemLTV、三层 Semantic ID、NTP、MoPO/GRPO clipped update 与有效 SID 约束均实际执行。未来正反馈频次代理 7 日订单，公开数据不支持还原真实搜索漏斗和多模态商品 foundation embedding。本地对照口径：基线是同一 transition policy 的 NTP retrieval；实验组 GrowthGR 加入 ItemLTV 与 8 轮 MoPO，相对基线 Hit@10 +0.00%、NDCG@10 +2.05%。  generative-recommendation reinforcement-learning new-items 搜广推 生成式召回与推理推荐 GrowthGR为什么用ItemLTV增量价值和多目标后训练，而不是只提高新品的即时曝光？ 给新品曝光本身不是最终目标，重要的是这次机会能否带来未来订单或其他长期价值。ItemLTV尝试区分原本会发生的结果与干预增量，多目标优化再协调点击、购买和覆盖；对稀有高价值动作的强化需要截断以防权重失控。反事实估计与奖励设计都需验证，不能把新品量增加直接当增长。 示意：两件新品同样少曝光，一件能打开持续消费场景，另一件只得到一次误触；均匀加流量无法区分，长期价值估计试图把机会分给更有增量的一件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-fcd351b4112088fb">GrowthGR为什么用ItemLTV增量价值和多目标后训练，而不是只提高新品的即时曝光？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agrowthgr">Towards Sustainable Growth: A Multi-Value-Aware Retrieval Framework for E-Commerce Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group / Taobao &amp; Tmall</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>给新品曝光本身不是最终目标，重要的是这次机会能否带来未来订单或其他长期价值。ItemLTV尝试区分原本会发生的结果与干预增量，多目标优化再协调点击、购买和覆盖；对稀有高价值动作的强化需要截断以防权重失控。反事实估计与奖励设计都需验证，不能把新品量增加直接当增长。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两件新品同样少曝光，一件能打开持续消费场景，另一件只得到一次误触；均匀加流量无法区分，长期价值估计试图把机会分给更有增量的一件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.17994">原论文</a> · <a href="../../../../reproductions/2605.17994-growthgr/">实现解读</a> · <a href="#qa-fcd351b4112088fb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:growthgr" data-paper-title="Towards Sustainable Growth: A Multi-Value-Aware Retrieval Framework for E-Commerce Search" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Towards Sustainable Growth: A Multi-Value-Aware Retrieval Framework for E-Commerce Search 搜广推与 LLM 应用 Alibaba Group / Taobao &amp; Tmall 2026-05-18 新品只按即时成交优化会持续缺曝光。GrowthGR 用 counterfactual ItemLTV 估计点击带来的长期订单增量，再以 RQ-VAE SID 和 decoder-only generator 召回；MoPO 联合购买、点击、曝光、排序和高 uplift 标签，并用 clipped inverse propensity 强化稀有高价值物品。 Fidelity: 核心机制复现。ItemLTV、三层 Semantic ID、NTP、MoPO/GRPO clipped update 与有效 SID 约束均实际执行。未来正反馈频次代理 7 日订单，公开数据不支持还原真实搜索漏斗和多模态商品 foundation embedding。本地对照口径：基线是同一 transition policy 的 NTP retrieval；实验组 GrowthGR 加入 ItemLTV 与 8 轮 MoPO，相对基线 Hit@10 +0.00%、NDCG@10 +2.05%。  generative-recommendation reinforcement-learning new-items 搜广推 生成式召回与推理推荐 GrowthGR 的稀有高价值加权与统一新品曝光奖励，有何选择差别？ 统一奖励只依据新旧身份，稀有价值权重还考虑旧策略概率与多目标价值，让缺机会但可能有益的物品获得更强学习。低概率不等于高质量，加权过强会放大噪声，所以使用裁剪。两者都不能无条件证明新品增长。 示意：两件新品曝光都少，一件预估长期价值高、一件相关性弱，不应只因都新就同等抬升；但高价值估错也会被加权放大。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b6962cf96eaddecd">GrowthGR 的稀有高价值加权与统一新品曝光奖励，有何选择差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agrowthgr">Towards Sustainable Growth: A Multi-Value-Aware Retrieval Framework for E-Commerce Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group / Taobao &amp; Tmall</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>统一奖励只依据新旧身份，稀有价值权重还考虑旧策略概率与多目标价值，让缺机会但可能有益的物品获得更强学习。低概率不等于高质量，加权过强会放大噪声，所以使用裁剪。两者都不能无条件证明新品增长。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两件新品曝光都少，一件预估长期价值高、一件相关性弱，不应只因都新就同等抬升；但高价值估错也会被加权放大。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.17994">原论文</a> · <a href="../../../../reproductions/2605.17994-growthgr/">实现解读</a> · <a href="#qa-b6962cf96eaddecd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:growthgr" data-paper-title="Towards Sustainable Growth: A Multi-Value-Aware Retrieval Framework for E-Commerce Search" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Towards Sustainable Growth: A Multi-Value-Aware Retrieval Framework for E-Commerce Search 搜广推与 LLM 应用 Alibaba Group / Taobao &amp; Tmall 2026-05-18 新品只按即时成交优化会持续缺曝光。GrowthGR 用 counterfactual ItemLTV 估计点击带来的长期订单增量，再以 RQ-VAE SID 和 decoder-only generator 召回；MoPO 联合购买、点击、曝光、排序和高 uplift 标签，并用 clipped inverse propensity 强化稀有高价值物品。 Fidelity: 核心机制复现。ItemLTV、三层 Semantic ID、NTP、MoPO/GRPO clipped update 与有效 SID 约束均实际执行。未来正反馈频次代理 7 日订单，公开数据不支持还原真实搜索漏斗和多模态商品 foundation embedding。本地对照口径：基线是同一 transition policy 的 NTP retrieval；实验组 GrowthGR 加入 ItemLTV 与 8 轮 MoPO，相对基线 Hit@10 +0.00%、NDCG@10 +2.05%。  generative-recommendation reinforcement-learning new-items 搜广推 生成式召回与推理推荐 GrowthGR 为什么裁剪 −log πold 对应的稀有性权重，并固定参考策略口径？ 很小旧概率会产生巨大权重，裁剪限制方差与单样本支配；πold 必须对应生成该样本的策略与上下文，不能拿当前更新后概率替换。policy ratio 与奖励权重作用不同，ItemLTV 代理和真实订单标签也需分开。 示意：某商品旧概率极低，未经裁剪可让一次噪声反馈压过整批；固定最大权重能限影响，却不能把不可靠价值估计变成可靠事实。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0acfd97ef595f1da">GrowthGR 为什么裁剪 −log πold 对应的稀有性权重，并固定参考策略口径？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agrowthgr">Towards Sustainable Growth: A Multi-Value-Aware Retrieval Framework for E-Commerce Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group / Taobao &amp; Tmall</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>很小旧概率会产生巨大权重，裁剪限制方差与单样本支配；πold 必须对应生成该样本的策略与上下文，不能拿当前更新后概率替换。policy ratio 与奖励权重作用不同，ItemLTV 代理和真实订单标签也需分开。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某商品旧概率极低，未经裁剪可让一次噪声反馈压过整批；固定最大权重能限影响，却不能把不可靠价值估计变成可靠事实。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.17994">原论文</a> · <a href="../../../../reproductions/2605.17994-growthgr/">实现解读</a> · <a href="#qa-0acfd97ef595f1da">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cq-sid" data-paper-title="Efficient Generative Retrieval for E-commerce Search with Semantic Cluster IDs and Expert-Guided RL" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Efficient Generative Retrieval for E-commerce Search with Semantic Cluster IDs and Expert-Guided RL 搜广推与 LLM 应用 Alibaba Taobao &amp; Tmall Group 2026-05-14 论文让首级 SID 服从商品类目，再用残差码表达类目内差异；Expert-Guided RL 组合点击、购买、语义与约束信号优化生成检索。 Fidelity: 核心机制复现。实现类目约束 Semantic ID、残差量化、多信号奖励和 EG-GRPO 更新。没有复刻 64-GPU 渐进训练、Tmall 私有 query log 和生产 beam service；EG-GRPO 更新本身真实执行。本地对照口径：基线是协同 item-ID 检索；实验组执行 CQ-SID 与 240 次 group-relative policy update；NDCG@10 相对 +1.66%。  generative-retrieval semantic-id reinforcement-learning 搜广推 生成式召回与推理推荐 CQ-SID 为什么让首级码对应商品类目，而后续码表达类目内残差？ 首级类目为生成建立可控语义边界，后续残差再区分同类商品的细节。这样容易对齐类目要求与检索路径，但错误类目会限制后续搜索，跨类相似也可能被切开。层级可解释性与灵活共享之间存在取舍。 示意：先选“相机”再区分微单与运动相机，便于按类目控制；若新品被错分成手机配件，细码再精确也会沿错误目录生成。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-cq-sid-a55bb5d1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7bbd4888f1acf964">CQ-SID 为什么让首级码对应商品类目，而后续码表达类目内残差？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acq-sid">Efficient Generative Retrieval for E-commerce Search with Semantic Cluster IDs and Expert-Guided RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Taobao &amp; Tmall Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>首级类目为生成建立可控语义边界，后续残差再区分同类商品的细节。这样容易对齐类目要求与检索路径，但错误类目会限制后续搜索，跨类相似也可能被切开。层级可解释性与灵活共享之间存在取舍。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先选“相机”再区分微单与运动相机，便于按类目控制；若新品被错分成手机配件，细码再精确也会沿错误目录生成。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.14434">原论文</a> · <a href="../../../../reproductions/2605.14434-cq-sid/">实现解读</a> · <a href="#qa-7bbd4888f1acf964">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cq-sid" data-paper-title="Efficient Generative Retrieval for E-commerce Search with Semantic Cluster IDs and Expert-Guided RL" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Efficient Generative Retrieval for E-commerce Search with Semantic Cluster IDs and Expert-Guided RL 搜广推与 LLM 应用 Alibaba Taobao &amp; Tmall Group 2026-05-14 论文让首级 SID 服从商品类目，再用残差码表达类目内差异；Expert-Guided RL 组合点击、购买、语义与约束信号优化生成检索。 Fidelity: 核心机制复现。实现类目约束 Semantic ID、残差量化、多信号奖励和 EG-GRPO 更新。没有复刻 64-GPU 渐进训练、Tmall 私有 query log 和生产 beam service；EG-GRPO 更新本身真实执行。本地对照口径：基线是协同 item-ID 检索；实验组执行 CQ-SID 与 240 次 group-relative policy update；NDCG@10 相对 +1.66%。  generative-retrieval semantic-id reinforcement-learning 搜广推 生成式召回与推理推荐 CQ-SID把商品类目固定在首级码，会给生成式召回带来什么好处与代价？ 首级类目为生成路径提供明确的粗层组织，使后续残差码只需表达类内差异，也方便加入业务与语义约束。代价是类目错误会在很早阶段限制可达候选，跨类替代关系也不能被默认当成同一路径。专家引导奖励用于协调点击、购买和约束，不能只靠类目结构保证相关性。 示意：先选鞋类再生成鞋款细码，搜索更有组织；若多功能商品被错误归为箱包，首层约束可能阻止模型在鞋类请求中找到它，需要单独处理分类和跨类需求。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-b4f87d7ed4915a2b">CQ-SID把商品类目固定在首级码，会给生成式召回带来什么好处与代价？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acq-sid">Efficient Generative Retrieval for E-commerce Search with Semantic Cluster IDs and Expert-Guided RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Taobao &amp; Tmall Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>首级类目为生成路径提供明确的粗层组织，使后续残差码只需表达类内差异，也方便加入业务与语义约束。代价是类目错误会在很早阶段限制可达候选，跨类替代关系也不能被默认当成同一路径。专家引导奖励用于协调点击、购买和约束，不能只靠类目结构保证相关性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先选鞋类再生成鞋款细码，搜索更有组织；若多功能商品被错误归为箱包，首层约束可能阻止模型在鞋类请求中找到它，需要单独处理分类和跨类需求。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.14434">原论文</a> · <a href="../../../../reproductions/2605.14434-cq-sid/">实现解读</a> · <a href="#qa-b4f87d7ed4915a2b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cq-sid" data-paper-title="Efficient Generative Retrieval for E-commerce Search with Semantic Cluster IDs and Expert-Guided RL" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Efficient Generative Retrieval for E-commerce Search with Semantic Cluster IDs and Expert-Guided RL 搜广推与 LLM 应用 Alibaba Taobao &amp; Tmall Group 2026-05-14 论文让首级 SID 服从商品类目，再用残差码表达类目内差异；Expert-Guided RL 组合点击、购买、语义与约束信号优化生成检索。 Fidelity: 核心机制复现。实现类目约束 Semantic ID、残差量化、多信号奖励和 EG-GRPO 更新。没有复刻 64-GPU 渐进训练、Tmall 私有 query log 和生产 beam service；EG-GRPO 更新本身真实执行。本地对照口径：基线是协同 item-ID 检索；实验组执行 CQ-SID 与 240 次 group-relative policy update；NDCG@10 相对 +1.66%。  generative-retrieval semantic-id reinforcement-learning 搜广推 生成式召回与推理推荐 CQ-SID 与完全自由学习的 RQ 首码相比，约束影响在哪个阶段？ 自由量化首先按表示距离组织粗码，CQ-SID 预先把首层对齐类目，训练和解码都在这个结构中学习。它减少粗码语义漂移，却依赖 taxonomy 质量，不能由分类清晰推断召回必然更高。Expert-Guided RL 另负责反馈对齐，不替代编码约束。 示意：内容相近的摄影书与相机教程视频，在自由码中可共享前缀；类目固定后可能分开，换来更明确的商品目录控制。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-fc84f38467d8d233">CQ-SID 与完全自由学习的 RQ 首码相比，约束影响在哪个阶段？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acq-sid">Efficient Generative Retrieval for E-commerce Search with Semantic Cluster IDs and Expert-Guided RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Taobao &amp; Tmall Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>自由量化首先按表示距离组织粗码，CQ-SID 预先把首层对齐类目，训练和解码都在这个结构中学习。它减少粗码语义漂移，却依赖 taxonomy 质量，不能由分类清晰推断召回必然更高。Expert-Guided RL 另负责反馈对齐，不替代编码约束。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>内容相近的摄影书与相机教程视频，在自由码中可共享前缀；类目固定后可能分开，换来更明确的商品目录控制。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.14434">原论文</a> · <a href="../../../../reproductions/2605.14434-cq-sid/">实现解读</a> · <a href="#qa-fc84f38467d8d233">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cq-sid" data-paper-title="Efficient Generative Retrieval for E-commerce Search with Semantic Cluster IDs and Expert-Guided RL" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Efficient Generative Retrieval for E-commerce Search with Semantic Cluster IDs and Expert-Guided RL 搜广推与 LLM 应用 Alibaba Taobao &amp; Tmall Group 2026-05-14 论文让首级 SID 服从商品类目，再用残差码表达类目内差异；Expert-Guided RL 组合点击、购买、语义与约束信号优化生成检索。 Fidelity: 核心机制复现。实现类目约束 Semantic ID、残差量化、多信号奖励和 EG-GRPO 更新。没有复刻 64-GPU 渐进训练、Tmall 私有 query log 和生产 beam service；EG-GRPO 更新本身真实执行。本地对照口径：基线是协同 item-ID 检索；实验组执行 CQ-SID 与 240 次 group-relative policy update；NDCG@10 相对 +1.66%。  generative-retrieval semantic-id reinforcement-learning 搜广推 生成式召回与推理推荐 CQ-SID 的组内 advantage 应按什么范围计算，不能跨请求混用？ 对同一上下文的一组 rollout 奖励计算均值和标准差，再标准化得到每条轨迹优势。不同请求奖励难度不同，混成一组会改变相对比较；标准差接近零需用定义的 epsilon。类目码与残差码也必须映到相同合法词表接口。 示意：简单请求的五个高奖励结果不应拿来压低另一个困难请求的全组优势；各请求内部比较，才能表达哪条生成对该请求更好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-11cee61cb6af22a3">CQ-SID 的组内 advantage 应按什么范围计算，不能跨请求混用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acq-sid">Efficient Generative Retrieval for E-commerce Search with Semantic Cluster IDs and Expert-Guided RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Taobao &amp; Tmall Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>对同一上下文的一组 rollout 奖励计算均值和标准差，再标准化得到每条轨迹优势。不同请求奖励难度不同，混成一组会改变相对比较；标准差接近零需用定义的 epsilon。类目码与残差码也必须映到相同合法词表接口。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>简单请求的五个高奖励结果不应拿来压低另一个困难请求的全组优势；各请求内部比较，才能表达哪条生成对该请求更好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.14434">原论文</a> · <a href="../../../../reproductions/2605.14434-cq-sid/">实现解读</a> · <a href="#qa-11cee61cb6af22a3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:univa" data-paper-title="Unified Value Alignment for Generative Recommendation in Industrial Advertising" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Unified Value Alignment for Generative Recommendation in Industrial Advertising 搜广推与 LLM 应用 Tencent / WeChat Channels 2026-05-07 传统生成式推荐主要优化用户行为匹配，却没有直接表示广告主的出价、ROI、优化目标等商业价值；工业广告还要求生成路径合法、满足请求级库存约束。UniVA 将“用户偏好、商业价值、可投放性”放进同一套生成式模型：Commercial SID 在语义 token 后编码商业属性；Generation-as-Ranking 用生成头和价值头联合给路径打分；eCPM-aware RL 让策略直接偏向请求内相对高价值广告；个性化 trie 则保证 beam 只沿当前请求可投放的广告路径展开。论文的三项关键改动是： Commercial token 的机制诊断是正向的：以相同前两级语义前缀分组，组内 bid proxy 的平均标准差由 0.34956 降至 0.09773（-72.04%）。Fidelity: 完整核心链路。本地实际执行 Commercial SID、HSTU 用户编码、cross-attention → causal self-attention 解码、MoR、共享专家 + top-k Sparse MoE、generation/value 双头、监督学习与 PPO/value 交替训练，以及 value-guided 个性化 trie beam search。  generative-advertising commercial-sid ppo value-aware-serving 搜广推 生成式召回与推理推荐 UniVA的商业SID最后一级，是再细分商品内容语义吗？ 不只是内容语义细化。它保留前两级语义码，末级引入商业属性组合与类内bid分桶，把广告目标和出价信息接到生成路径。末级的目录含义应由商业映射解释，不能直接按普通内容聚类标签读，也不能将代理bid视作真实收入。 教学例子：两条内容相近的广告可因商业属性或bid档不同落入不同末级码；差别不必来自画面或文本主题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-univa-ad679aba" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0de51f7643d33b41">UniVA的商业SID最后一级，是再细分商品内容语义吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Auniva">Unified Value Alignment for Generative Recommendation in Industrial Advertising</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent / WeChat Channels</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不只是内容语义细化。它保留前两级语义码，末级引入商业属性组合与类内bid分桶，把广告目标和出价信息接到生成路径。末级的目录含义应由商业映射解释，不能直接按普通内容聚类标签读，也不能将代理bid视作真实收入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两条内容相近的广告可因商业属性或bid档不同落入不同末级码；差别不必来自画面或文本主题。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.05803">原论文</a> · <a href="../../../../reproductions/2605.05803-univa/">实现解读</a> · <a href="#qa-0de51f7643d33b41">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:univa" data-paper-title="Unified Value Alignment for Generative Recommendation in Industrial Advertising" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Unified Value Alignment for Generative Recommendation in Industrial Advertising 搜广推与 LLM 应用 Tencent / WeChat Channels 2026-05-07 传统生成式推荐主要优化用户行为匹配，却没有直接表示广告主的出价、ROI、优化目标等商业价值；工业广告还要求生成路径合法、满足请求级库存约束。UniVA 将“用户偏好、商业价值、可投放性”放进同一套生成式模型：Commercial SID 在语义 token 后编码商业属性；Generation-as-Ranking 用生成头和价值头联合给路径打分；eCPM-aware RL 让策略直接偏向请求内相对高价值广告；个性化 trie 则保证 beam 只沿当前请求可投放的广告路径展开。论文的三项关键改动是： Commercial token 的机制诊断是正向的：以相同前两级语义前缀分组，组内 bid proxy 的平均标准差由 0.34956 降至 0.09773（-72.04%）。Fidelity: 完整核心链路。本地实际执行 Commercial SID、HSTU 用户编码、cross-attention → causal self-attention 解码、MoR、共享专家 + top-k Sparse MoE、generation/value 双头、监督学习与 PPO/value 交替训练，以及 value-guided 个性化 trie beam search。  generative-advertising commercial-sid ppo value-aware-serving 搜广推 生成式召回与推理推荐 UniVA 为什么同时需要 Commercial SID、生成价值头和请求级个性化 trie？ 商业码把出价等属性带入输出路径，生成与价值 logit 相加让解码同时考虑相关性和商业价值，eCPM 奖励再调整策略。请求级 trie 则解决另一件事：只有当前可投放广告才可沿路径生成。价值高不意味着合法可投放，合法也不意味着用户相关，三类信号缺一不可；本地价值是公开数据代理。 示意：某广告出价高，但当前地区无库存，必须由请求 trie 禁止生成；另一条合法广告再由相关性和价值联合评分，不能只凭商业码就绕过投放约束。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-9b382078c2f77bfb">UniVA 为什么同时需要 Commercial SID、生成价值头和请求级个性化 trie？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Auniva">Unified Value Alignment for Generative Recommendation in Industrial Advertising</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent / WeChat Channels</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>商业码把出价等属性带入输出路径，生成与价值 logit 相加让解码同时考虑相关性和商业价值，eCPM 奖励再调整策略。请求级 trie 则解决另一件事：只有当前可投放广告才可沿路径生成。价值高不意味着合法可投放，合法也不意味着用户相关，三类信号缺一不可；本地价值是公开数据代理。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某广告出价高，但当前地区无库存，必须由请求 trie 禁止生成；另一条合法广告再由相关性和价值联合评分，不能只凭商业码就绕过投放约束。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.05803">原论文</a> · <a href="../../../../reproductions/2605.05803-univa/">实现解读</a> · <a href="#qa-9b382078c2f77bfb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:univa" data-paper-title="Unified Value Alignment for Generative Recommendation in Industrial Advertising" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Unified Value Alignment for Generative Recommendation in Industrial Advertising 搜广推与 LLM 应用 Tencent / WeChat Channels 2026-05-07 传统生成式推荐主要优化用户行为匹配，却没有直接表示广告主的出价、ROI、优化目标等商业价值；工业广告还要求生成路径合法、满足请求级库存约束。UniVA 将“用户偏好、商业价值、可投放性”放进同一套生成式模型：Commercial SID 在语义 token 后编码商业属性；Generation-as-Ranking 用生成头和价值头联合给路径打分；eCPM-aware RL 让策略直接偏向请求内相对高价值广告；个性化 trie 则保证 beam 只沿当前请求可投放的广告路径展开。论文的三项关键改动是： Commercial token 的机制诊断是正向的：以相同前两级语义前缀分组，组内 bid proxy 的平均标准差由 0.34956 降至 0.09773（-72.04%）。Fidelity: 完整核心链路。本地实际执行 Commercial SID、HSTU 用户编码、cross-attention → causal self-attention 解码、MoR、共享专家 + top-k Sparse MoE、generation/value 双头、监督学习与 PPO/value 交替训练，以及 value-guided 个性化 trie beam search。  generative-advertising commercial-sid ppo value-aware-serving 搜广推 生成式召回与推理推荐 Generation-as-Ranking双logit与生成后独立精排有什么不同？ 生成头与价值头逐元素相加再归一，价值影响每步路径概率；独立精排只能在既有候选后调整。两者可达空间与成本不同，不能把最终线性打分称双头生成。 例如高价值路径可能更早进入beam，而不是等召回完才被看见。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-99696aa492087453">Generation-as-Ranking双logit与生成后独立精排有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Auniva">Unified Value Alignment for Generative Recommendation in Industrial Advertising</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent / WeChat Channels</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>生成头与价值头逐元素相加再归一，价值影响每步路径概率；独立精排只能在既有候选后调整。两者可达空间与成本不同，不能把最终线性打分称双头生成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如高价值路径可能更早进入beam，而不是等召回完才被看见。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.05803">原论文</a> · <a href="../../../../reproductions/2605.05803-univa/">实现解读</a> · <a href="#qa-99696aa492087453">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:univa" data-paper-title="Unified Value Alignment for Generative Recommendation in Industrial Advertising" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Unified Value Alignment for Generative Recommendation in Industrial Advertising 搜广推与 LLM 应用 Tencent / WeChat Channels 2026-05-07 传统生成式推荐主要优化用户行为匹配，却没有直接表示广告主的出价、ROI、优化目标等商业价值；工业广告还要求生成路径合法、满足请求级库存约束。UniVA 将“用户偏好、商业价值、可投放性”放进同一套生成式模型：Commercial SID 在语义 token 后编码商业属性；Generation-as-Ranking 用生成头和价值头联合给路径打分；eCPM-aware RL 让策略直接偏向请求内相对高价值广告；个性化 trie 则保证 beam 只沿当前请求可投放的广告路径展开。论文的三项关键改动是： Commercial token 的机制诊断是正向的：以相同前两级语义前缀分组，组内 bid proxy 的平均标准差由 0.34956 降至 0.09773（-72.04%）。Fidelity: 完整核心链路。本地实际执行 Commercial SID、HSTU 用户编码、cross-attention → causal self-attention 解码、MoR、共享专家 + top-k Sparse MoE、generation/value 双头、监督学习与 PPO/value 交替训练，以及 value-guided 个性化 trie beam search。  generative-advertising commercial-sid ppo value-aware-serving 搜广推 生成式召回与推理推荐 UniVA本地proxy与真实eCPM、个性trie需要怎样区分？ 本地有核心网络RL与trie链路，但bid和商业标签是确定代理，非真实广告收益。请求trie只允许当前库存前缀，累计融合logp；不能用全局trie放过不可投放广告。 例如某广告全局有效但当前地域不可投，仍应在本次beam被屏蔽。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-dbef2e81a2695f80">UniVA本地proxy与真实eCPM、个性trie需要怎样区分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Auniva">Unified Value Alignment for Generative Recommendation in Industrial Advertising</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent / WeChat Channels</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>本地有核心网络RL与trie链路，但bid和商业标签是确定代理，非真实广告收益。请求trie只允许当前库存前缀，累计融合logp；不能用全局trie放过不可投放广告。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某广告全局有效但当前地域不可投，仍应在本次beam被屏蔽。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.05803">原论文</a> · <a href="../../../../reproductions/2605.05803-univa/">实现解读</a> · <a href="#qa-dbef2e81a2695f80">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:genrec" data-paper-title="GenRec: A Preference-Oriented Generative Framework for Large-Scale Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="GenRec: A Preference-Oriented Generative Framework for Large-Scale Recommendation 搜广推与 LLM 应用 JD.com 2026-04-16 逐 item 生成忽略同一页面内的互补和顺序。GenRec 将下一页作为序列目标，用非对称 Token Merger 压缩输入，并以 GRPO-SR 的组内 reward 优化整页，同时保留 NLL 正则抑制策略漂移。 复现保真度：核心机制复现。复现保真度：核心机制复现。Page-wise NTP、非对称 Token Merger 与 GRPO-SR/NLL 约束实际执行。把连续三个正反馈组成一页，联合估计 page policy，并用序位 reward advantage 更新、NLL policy 约束。  generative-recommendation grpo page-wise 搜广推 生成式召回与推理推荐 GenRec 为什么把连续多个正反馈组织成下一页目标？ 用户同页消费存在互补与顺序关系，逐点预测只拟合某个下一项，难直接考虑页面组合。页序列让后续选择依赖前缀，组内奖励评价整页；公开数据按连续行为构造页面只是替代定义，未必等于真实曝光页。 示意：露营需求可能同时需要帐篷、睡袋和防潮垫，整页目标可学习它们配合；三个连续看过电影也能组成代理页，但不代表真实曾同时展示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-genrec-e5f875fa" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2f8db993ea0b2837">GenRec 为什么把连续多个正反馈组织成下一页目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agenrec">GenRec: A Preference-Oriented Generative Framework for Large-Scale Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · JD.com</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用户同页消费存在互补与顺序关系，逐点预测只拟合某个下一项，难直接考虑页面组合。页序列让后续选择依赖前缀，组内奖励评价整页；公开数据按连续行为构造页面只是替代定义，未必等于真实曝光页。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>露营需求可能同时需要帐篷、睡袋和防潮垫，整页目标可学习它们配合；三个连续看过电影也能组成代理页，但不代表真实曾同时展示。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.14878">原论文</a> · <a href="../../../../reproductions/2604.14878-genrec/">实现解读</a> · <a href="#qa-2f8db993ea0b2837">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:genrec" data-paper-title="GenRec: A Preference-Oriented Generative Framework for Large-Scale Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="GenRec: A Preference-Oriented Generative Framework for Large-Scale Recommendation 搜广推与 LLM 应用 JD.com 2026-04-16 逐 item 生成忽略同一页面内的互补和顺序。GenRec 将下一页作为序列目标，用非对称 Token Merger 压缩输入，并以 GRPO-SR 的组内 reward 优化整页，同时保留 NLL 正则抑制策略漂移。 复现保真度：核心机制复现。复现保真度：核心机制复现。Page-wise NTP、非对称 Token Merger 与 GRPO-SR/NLL 约束实际执行。把连续三个正反馈组成一页，联合估计 page policy，并用序位 reward advantage 更新、NLL policy 约束。  generative-recommendation grpo page-wise 搜广推 生成式召回与推理推荐 GenRec为什么把下一页作为序列目标，并在GRPO旁保留NLL约束？ 单item监督只告诉模型下一件是什么，不能直接学同页顺序与互补。页面序列目标表达组合关系，组内reward优势推动整页效果；NLL继续约束日志支持的行为，减少只追奖励造成的策略漂移。若页面奖励遗漏相关性或可行性，生成整页也可能放大偏差，不能把reward上升直接当用户满意。 示意：三件内容分别高分却高度重复，页面目标可以学到替换其中一件；但若只奖励新颖，可能生成不相关内容，NLL帮助限制这种偏离。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-e1b9b517b34000d1">GenRec为什么把下一页作为序列目标，并在GRPO旁保留NLL约束？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agenrec">GenRec: A Preference-Oriented Generative Framework for Large-Scale Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · JD.com</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单item监督只告诉模型下一件是什么，不能直接学同页顺序与互补。页面序列目标表达组合关系，组内reward优势推动整页效果；NLL继续约束日志支持的行为，减少只追奖励造成的策略漂移。若页面奖励遗漏相关性或可行性，生成整页也可能放大偏差，不能把reward上升直接当用户满意。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三件内容分别高分却高度重复，页面目标可以学到替换其中一件；但若只奖励新颖，可能生成不相关内容，NLL帮助限制这种偏离。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.14878">原论文</a> · <a href="../../../../reproductions/2604.14878-genrec/">实现解读</a> · <a href="#qa-e1b9b517b34000d1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:genrec" data-paper-title="GenRec: A Preference-Oriented Generative Framework for Large-Scale Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="GenRec: A Preference-Oriented Generative Framework for Large-Scale Recommendation 搜广推与 LLM 应用 JD.com 2026-04-16 逐 item 生成忽略同一页面内的互补和顺序。GenRec 将下一页作为序列目标，用非对称 Token Merger 压缩输入，并以 GRPO-SR 的组内 reward 优化整页，同时保留 NLL 正则抑制策略漂移。 复现保真度：核心机制复现。复现保真度：核心机制复现。Page-wise NTP、非对称 Token Merger 与 GRPO-SR/NLL 约束实际执行。把连续三个正反馈组成一页，联合估计 page policy，并用序位 reward advantage 更新、NLL policy 约束。  generative-recommendation grpo page-wise 搜广推 生成式召回与推理推荐 GenRec 保留 NLL 与仅追逐 GRPO-SR reward，相比约束了哪类漂移？ 组相对奖励让策略比较整页效用，NLL 继续约束日志行为拟合，防止稀疏或有偏奖励把生成分布拉得太远。两者权重是模仿与探索的取舍，不保证奖励增大即真实满意提升。来源本地大相对增幅也受代理标签与基线影响。 示意：多样性 reward 偏高可能鼓励不相关新奇列表，NLL 保留基础兴趣；若完全删掉它，模型更容易为单一代理目标走捷径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c79d1223eeb4334a">GenRec 保留 NLL 与仅追逐 GRPO-SR reward，相比约束了哪类漂移？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agenrec">GenRec: A Preference-Oriented Generative Framework for Large-Scale Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · JD.com</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>组相对奖励让策略比较整页效用，NLL 继续约束日志行为拟合，防止稀疏或有偏奖励把生成分布拉得太远。两者权重是模仿与探索的取舍，不保证奖励增大即真实满意提升。来源本地大相对增幅也受代理标签与基线影响。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>多样性 reward 偏高可能鼓励不相关新奇列表，NLL 保留基础兴趣；若完全删掉它，模型更容易为单一代理目标走捷径。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.14878">原论文</a> · <a href="../../../../reproductions/2604.14878-genrec/">实现解读</a> · <a href="#qa-c79d1223eeb4334a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:genrec" data-paper-title="GenRec: A Preference-Oriented Generative Framework for Large-Scale Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="GenRec: A Preference-Oriented Generative Framework for Large-Scale Recommendation 搜广推与 LLM 应用 JD.com 2026-04-16 逐 item 生成忽略同一页面内的互补和顺序。GenRec 将下一页作为序列目标，用非对称 Token Merger 压缩输入，并以 GRPO-SR 的组内 reward 优化整页，同时保留 NLL 正则抑制策略漂移。 复现保真度：核心机制复现。复现保真度：核心机制复现。Page-wise NTP、非对称 Token Merger 与 GRPO-SR/NLL 约束实际执行。把连续三个正反馈组成一页，联合估计 page policy，并用序位 reward advantage 更新、NLL policy 约束。  generative-recommendation grpo page-wise 搜广推 生成式召回与推理推荐 GenRec 的组内 advantage 为什么只能比较同一上下文生成的页面？ 同组页面共享用户历史与候选难度，均值扣除才表达相对好坏；跨用户混组会把请求难度误当动作优势。页前缀与重复 mask 也需同步更新，NLL 正则针对合法目标。Token Merger 压缩不允许把测试未来页写回输入。 示意：摄影用户本来易命中、冷用户较难，混组会让后者全负；分别比较各自几页生成，才能评价模型在该请求下哪种组合更好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-071c67569a5ee13d">GenRec 的组内 advantage 为什么只能比较同一上下文生成的页面？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agenrec">GenRec: A Preference-Oriented Generative Framework for Large-Scale Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · JD.com</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同组页面共享用户历史与候选难度，均值扣除才表达相对好坏；跨用户混组会把请求难度误当动作优势。页前缀与重复 mask 也需同步更新，NLL 正则针对合法目标。Token Merger 压缩不允许把测试未来页写回输入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>摄影用户本来易命中、冷用户较难，混组会让后者全负；分别比较各自几页生成，才能评价模型在该请求下哪种组合更好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.14878">原论文</a> · <a href="../../../../reproductions/2604.14878-genrec/">实现解读</a> · <a href="#qa-071c67569a5ee13d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unirec-coa" data-paper-title="UniRec: Bridging the Expressive Gap between Generative and Discriminative Recommendation via Chain-of-Attribute" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="UniRec: Bridging the Expressive Gap between Generative and Discriminative Recommendation via Chain-of-Attribute 搜广推与 LLM 应用 Authors did not disclose affiliation / large-scale e-commerce platform 2026-04-14 在 SID 前生成品类、卖家和品牌等属性链，用容量受限量化抑制热点 token 塌缩，并以任务上下文稳定多场景生成。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 unirec-coa 核心机制，相对 NDCG@10 -4.93%。  generative-recommendation semantic-id preference-alignment 搜广推 生成式召回与推理推荐 Chain-of-Attribute UniRec为什么在SID前生成属性链？ 品类、卖家和品牌等属性可给纯语义码增加显式商品条件，缓解生成与判别表达差距。属性链是内容引导，不等于自然语言CoT已经具备独立推理能力。 例如先决定品牌与品类，再生成具体语义路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-unirec-coa-7ee11184" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0d1560da99d7ac98">Chain-of-Attribute UniRec为什么在SID前生成属性链？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunirec-coa">UniRec: Bridging the Expressive Gap between Generative and Discriminative Recommendation via Chain-of-Attribute</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation / large-scale e-commerce platform</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>品类、卖家和品牌等属性可给纯语义码增加显式商品条件，缓解生成与判别表达差距。属性链是内容引导，不等于自然语言CoT已经具备独立推理能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先决定品牌与品类，再生成具体语义路径。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.12234">原论文</a> · <a href="../../../../reproductions/2604.12234-unirec-coa/">实现解读</a> · <a href="#qa-0d1560da99d7ac98">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unirec-coa" data-paper-title="UniRec: Bridging the Expressive Gap between Generative and Discriminative Recommendation via Chain-of-Attribute" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="UniRec: Bridging the Expressive Gap between Generative and Discriminative Recommendation via Chain-of-Attribute 搜广推与 LLM 应用 Authors did not disclose affiliation / large-scale e-commerce platform 2026-04-14 在 SID 前生成品类、卖家和品牌等属性链，用容量受限量化抑制热点 token 塌缩，并以任务上下文稳定多场景生成。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 unirec-coa 核心机制，相对 NDCG@10 -4.93%。  generative-recommendation semantic-id preference-alignment 搜广推 生成式召回与推理推荐 UniRec-CoA 为什么在 SID 前生成属性链，并对量化容量加约束？ 属性链先把品类、卖家、品牌等结构化条件显式带入生成，使后续 SID 依赖更具体的上下文；容量约束限制热门 token 挤占码空间，任务上下文再区分不同场景需求。链式分解提高条件组织能力，也会传播早期属性错误，不能把可解释链条的存在等同于最终生成必然正确。 示意：先确定运动鞋、目标品牌和卖家范围，再生成具体商品码。若第一步把品类选成皮鞋，后续再精细也容易偏离；容量约束则防止所有商品都挤向热门品牌路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-5ec2902153dfbf8c">UniRec-CoA 为什么在 SID 前生成属性链，并对量化容量加约束？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunirec-coa">UniRec: Bridging the Expressive Gap between Generative and Discriminative Recommendation via Chain-of-Attribute</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation / large-scale e-commerce platform</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>属性链先把品类、卖家、品牌等结构化条件显式带入生成，使后续 SID 依赖更具体的上下文；容量约束限制热门 token 挤占码空间，任务上下文再区分不同场景需求。链式分解提高条件组织能力，也会传播早期属性错误，不能把可解释链条的存在等同于最终生成必然正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先确定运动鞋、目标品牌和卖家范围，再生成具体商品码。若第一步把品类选成皮鞋，后续再精细也容易偏离；容量约束则防止所有商品都挤向热门品牌路径。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.12234">原论文</a> · <a href="../../../../reproductions/2604.12234-unirec-coa/">实现解读</a> · <a href="#qa-5ec2902153dfbf8c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unirec-coa" data-paper-title="UniRec: Bridging the Expressive Gap between Generative and Discriminative Recommendation via Chain-of-Attribute" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="UniRec: Bridging the Expressive Gap between Generative and Discriminative Recommendation via Chain-of-Attribute 搜广推与 LLM 应用 Authors did not disclose affiliation / large-scale e-commerce platform 2026-04-14 在 SID 前生成品类、卖家和品牌等属性链，用容量受限量化抑制热点 token 塌缩，并以任务上下文稳定多场景生成。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 unirec-coa 核心机制，相对 NDCG@10 -4.93%。  generative-recommendation semantic-id preference-alignment 搜广推 生成式召回与推理推荐 容量受限量化与只最大化热门码似然有什么差别？ 容量约束抑制热点token挤占，使码使用更分散；单似然易跟随频率。均衡仍需与相关性联合评估，不能只报码利用率就宣称推荐更好。 例如不让所有常见商品挤进同一桶，但也不能为了均匀随机分配。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1ca55275b4b52784">容量受限量化与只最大化热门码似然有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunirec-coa">UniRec: Bridging the Expressive Gap between Generative and Discriminative Recommendation via Chain-of-Attribute</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation / large-scale e-commerce platform</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>容量约束抑制热点token挤占，使码使用更分散；单似然易跟随频率。均衡仍需与相关性联合评估，不能只报码利用率就宣称推荐更好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如不让所有常见商品挤进同一桶，但也不能为了均匀随机分配。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.12234">原论文</a> · <a href="../../../../reproductions/2604.12234-unirec-coa/">实现解读</a> · <a href="#qa-1ca55275b4b52784">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unirec-coa" data-paper-title="UniRec: Bridging the Expressive Gap between Generative and Discriminative Recommendation via Chain-of-Attribute" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="UniRec: Bridging the Expressive Gap between Generative and Discriminative Recommendation via Chain-of-Attribute 搜广推与 LLM 应用 Authors did not disclose affiliation / large-scale e-commerce platform 2026-04-14 在 SID 前生成品类、卖家和品牌等属性链，用容量受限量化抑制热点 token 塌缩，并以任务上下文稳定多场景生成。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 unirec-coa 核心机制，相对 NDCG@10 -4.93%。  generative-recommendation semantic-id preference-alignment 搜广推 生成式召回与推理推荐 COA的属性标签可以用目标未来行为反推后输入吗？ 不能，属性来自训练允许商品信息，目标商品属性可作生成监督而非已知答案提示。当前固定MovieLens候选机制没有私有目录与生产多场景链路。 例如预测下一物品时先输入该物品真实品牌，会让任务过于容易。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-9e5f5e882d487833">COA的属性标签可以用目标未来行为反推后输入吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunirec-coa">UniRec: Bridging the Expressive Gap between Generative and Discriminative Recommendation via Chain-of-Attribute</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation / large-scale e-commerce platform</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，属性来自训练允许商品信息，目标商品属性可作生成监督而非已知答案提示。当前固定MovieLens候选机制没有私有目录与生产多场景链路。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如预测下一物品时先输入该物品真实品牌，会让任务过于容易。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.12234">原论文</a> · <a href="../../../../reproductions/2604.12234-unirec-coa/">实现解读</a> · <a href="#qa-9e5f5e882d487833">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mbgr" data-paper-title="MBGR: Multi-Business Generative Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="MBGR: Multi-Business Generative Recommendation 搜广推与 LLM 应用 Meituan 2026-04-03 多业务日志交错时，普通 next-item 监督只覆盖实际下一条业务。MBGR 用 business-conditioned autoencoder 保留 SID 语义，以共享 MoE 生成业务特定表示；LDR 在每个时刻为每个业务寻找最近未来交互，无标签业务被 mask。 Fidelity: 核心机制复现。Business-aware SID、共享 experts、逐业务预测与 Label Dynamic Routing 均实际执行。genre 是公开业务域代理，不能替代 Meituan 多业务私有日志与线上生成器规模。本地对照口径：基线是共享 next-item 模型；实验组 MBGR 用 genre 作为 19 个业务域并执行 BID/MBP/LDR，相对基线 Hit@10 -4.17%、NDCG@10 -5.92%。  generative-recommendation multi-domain semantic-id 搜广推 生成式召回与推理推荐 MBGR 为什么为每个业务分别找最近未来交互？ 多业务日志交错，单一步 next-item 只监督实际下一条业务，其他业务得不到同一时刻的目标。LDR 向后查每个业务最近事件，让共享状态学习多方向预测，无未来标签的业务被 mask。它是多任务监督，不允许把未来事件提前输入历史。 示意：下一条是短视频，但稍后还有购物，当前状态可分别学习两者；若只学全日志紧邻项，购物目标会被大量视频事件遮住。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-mbgr-3a21e1da" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2b13e572a09b32b8">MBGR 为什么为每个业务分别找最近未来交互？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ambgr">MBGR: Multi-Business Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多业务日志交错，单一步 next-item 只监督实际下一条业务，其他业务得不到同一时刻的目标。LDR 向后查每个业务最近事件，让共享状态学习多方向预测，无未来标签的业务被 mask。它是多任务监督，不允许把未来事件提前输入历史。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>下一条是短视频，但稍后还有购物，当前状态可分别学习两者；若只学全日志紧邻项，购物目标会被大量视频事件遮住。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.02684">原论文</a> · <a href="../../../../reproductions/2604.02684-mbgr/">实现解读</a> · <a href="#qa-2b13e572a09b32b8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mbgr" data-paper-title="MBGR: Multi-Business Generative Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="MBGR: Multi-Business Generative Recommendation 搜广推与 LLM 应用 Meituan 2026-04-03 多业务日志交错时，普通 next-item 监督只覆盖实际下一条业务。MBGR 用 business-conditioned autoencoder 保留 SID 语义，以共享 MoE 生成业务特定表示；LDR 在每个时刻为每个业务寻找最近未来交互，无标签业务被 mask。 Fidelity: 核心机制复现。Business-aware SID、共享 experts、逐业务预测与 Label Dynamic Routing 均实际执行。genre 是公开业务域代理，不能替代 Meituan 多业务私有日志与线上生成器规模。本地对照口径：基线是共享 next-item 模型；实验组 MBGR 用 genre 作为 19 个业务域并执行 BID/MBP/LDR，相对基线 Hit@10 -4.17%、NDCG@10 -5.92%。  generative-recommendation multi-domain semantic-id 搜广推 生成式召回与推理推荐 MBGR为什么为每个业务寻找最近未来交互，而不只监督日志中的下一条事件？ 多业务事件交错时，实际下一条可能属于高频业务，稀疏业务长期得不到直接监督。LDR在当前时刻为各业务寻找最近未来目标，结合业务条件表示，让同一上下文学习多条发展方向；没有对应未来事件时必须mask。构造这些标签仅限训练，评估策略不能把它们当作当前已知输入。 示意：用户先刷视频再搜索商品，下一条总是视频会淹没购物监督；按业务寻找未来目标能保留购物分支，但不能把未来购买ID直接喂给当前推荐器。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f28720ce81a7ef92">MBGR为什么为每个业务寻找最近未来交互，而不只监督日志中的下一条事件？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ambgr">MBGR: Multi-Business Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多业务事件交错时，实际下一条可能属于高频业务，稀疏业务长期得不到直接监督。LDR在当前时刻为各业务寻找最近未来目标，结合业务条件表示，让同一上下文学习多条发展方向；没有对应未来事件时必须mask。构造这些标签仅限训练，评估策略不能把它们当作当前已知输入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户先刷视频再搜索商品，下一条总是视频会淹没购物监督；按业务寻找未来目标能保留购物分支，但不能把未来购买ID直接喂给当前推荐器。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.02684">原论文</a> · <a href="../../../../reproductions/2604.02684-mbgr/">实现解读</a> · <a href="#qa-f28720ce81a7ef92">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mbgr" data-paper-title="MBGR: Multi-Business Generative Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="MBGR: Multi-Business Generative Recommendation 搜广推与 LLM 应用 Meituan 2026-04-03 多业务日志交错时，普通 next-item 监督只覆盖实际下一条业务。MBGR 用 business-conditioned autoencoder 保留 SID 语义，以共享 MoE 生成业务特定表示；LDR 在每个时刻为每个业务寻找最近未来交互，无标签业务被 mask。 Fidelity: 核心机制复现。Business-aware SID、共享 experts、逐业务预测与 Label Dynamic Routing 均实际执行。genre 是公开业务域代理，不能替代 Meituan 多业务私有日志与线上生成器规模。本地对照口径：基线是共享 next-item 模型；实验组 MBGR 用 genre 作为 19 个业务域并执行 BID/MBP/LDR，相对基线 Hit@10 -4.17%、NDCG@10 -5.92%。  generative-recommendation multi-domain semantic-id 搜广推 生成式召回与推理推荐 Business-conditioned MoE 与为每个业务独训生成器，相比共享发生在哪里？ 专家池共享通用变化，业务条件 gate 产生特定表示，business-conditioned autoencoder 还维持 SID 语义。独立模型容易重复学习但少冲突，共享则需防负迁移。业务以 genre 代理不等于真实跨产品标签，来源本地未见收益需保留。 示意：购物与内容业务可借同一语义专家，门控比例不同；若独立训，两者无法交换知识，但共享过强又可能让大流量内容压制购物。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-6183ac3f8450d70c">Business-conditioned MoE 与为每个业务独训生成器，相比共享发生在哪里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ambgr">MBGR: Multi-Business Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>专家池共享通用变化，业务条件 gate 产生特定表示，business-conditioned autoencoder 还维持 SID 语义。独立模型容易重复学习但少冲突，共享则需防负迁移。业务以 genre 代理不等于真实跨产品标签，来源本地未见收益需保留。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>购物与内容业务可借同一语义专家，门控比例不同；若独立训，两者无法交换知识，但共享过强又可能让大流量内容压制购物。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.02684">原论文</a> · <a href="../../../../reproductions/2604.02684-mbgr/">实现解读</a> · <a href="#qa-6183ac3f8450d70c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mbgr" data-paper-title="MBGR: Multi-Business Generative Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="MBGR: Multi-Business Generative Recommendation 搜广推与 LLM 应用 Meituan 2026-04-03 多业务日志交错时，普通 next-item 监督只覆盖实际下一条业务。MBGR 用 business-conditioned autoencoder 保留 SID 语义，以共享 MoE 生成业务特定表示；LDR 在每个时刻为每个业务寻找最近未来交互，无标签业务被 mask。 Fidelity: 核心机制复现。Business-aware SID、共享 experts、逐业务预测与 Label Dynamic Routing 均实际执行。genre 是公开业务域代理，不能替代 Meituan 多业务私有日志与线上生成器规模。本地对照口径：基线是共享 next-item 模型；实验组 MBGR 用 genre 作为 19 个业务域并执行 BID/MBP/LDR，相对基线 Hit@10 -4.17%、NDCG@10 -5.92%。  generative-recommendation multi-domain semantic-id 搜广推 生成式召回与推理推荐 MBGR 找不到某业务未来事件时，为什么不能用最后物品或 padding 充标签？ 该业务在当前监督窗口没有可观测目标，填补会制造虚假转移，必须 mask 对应 loss。t′ 应是严格晚于当前且满足业务身份的最早位置，不能只按品类相似替代。训练标签可见与推理输入可见应分开。 示意：用户后续再没购物，就不应把最后看过电影当购物正例；mask 会减少监督，却保留“未观测”而非编造答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3a0f76153c4a63db">MBGR 找不到某业务未来事件时，为什么不能用最后物品或 padding 充标签？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ambgr">MBGR: Multi-Business Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>该业务在当前监督窗口没有可观测目标，填补会制造虚假转移，必须 mask 对应 loss。t′ 应是严格晚于当前且满足业务身份的最早位置，不能只按品类相似替代。训练标签可见与推理输入可见应分开。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户后续再没购物，就不应把最后看过电影当购物正例；mask 会减少监督，却保留“未观测”而非编造答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.02684">原论文</a> · <a href="../../../../reproductions/2604.02684-mbgr/">实现解读</a> · <a href="#qa-3a0f76153c4a63db">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rclrec" data-paper-title="RCLRec: Reverse Curriculum Learning for Modeling Sparse Conversions in Generative Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="RCLRec: Reverse Curriculum Learning for Modeling Sparse Conversions in Generative Recommendation 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-03-30 RCLRec 从行为历史里选择与转化相关的短子序列，并按逆时间顺序作为 decoder 前缀。联合生成目标提供逐样本的中间监督，质量感知损失抑制无信息课程，缓解转化标签稀疏。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04768，相对变化 -11.71%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation conversion-modeling curriculum-learning 搜广推 生成式召回与推理推荐 RCLRec 的课程质量权重为零，是否意味着主目标也停止学习？ 不意味着。来源将损失写成主目标加 λq(C) 倍课程项，q(C)=0 会使该课程项在总损失数值中消失，主目标项仍保留。质量控制针对辅助监督的贡献，不应误改成遮掉整个样本。讨论梯度时还需区分权重是否也是可训练量。 示意：一条购买样本的课程片段很差，可以不计该辅助目标，仍用真实购买标签训练主预测；直接丢掉整条样本会连有价值监督也删除。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-rclrec-bd92f42c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-80bc5b5c19f75b0a">RCLRec 的课程质量权重为零，是否意味着主目标也停止学习？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arclrec">RCLRec: Reverse Curriculum Learning for Modeling Sparse Conversions in Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不意味着。来源将损失写成主目标加 λq(C) 倍课程项，q(C)=0 会使该课程项在总损失数值中消失，主目标项仍保留。质量控制针对辅助监督的贡献，不应误改成遮掉整个样本。讨论梯度时还需区分权重是否也是可训练量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一条购买样本的课程片段很差，可以不计该辅助目标，仍用真实购买标签训练主预测；直接丢掉整条样本会连有价值监督也删除。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.28124">原论文</a> · <a href="../../../../reproductions/2603.28124-rclrec/">实现解读</a> · <a href="#qa-80bc5b5c19f75b0a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rclrec" data-paper-title="RCLRec: Reverse Curriculum Learning for Modeling Sparse Conversions in Generative Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="RCLRec: Reverse Curriculum Learning for Modeling Sparse Conversions in Generative Recommendation 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-03-30 RCLRec 从行为历史里选择与转化相关的短子序列，并按逆时间顺序作为 decoder 前缀。联合生成目标提供逐样本的中间监督，质量感知损失抑制无信息课程，缓解转化标签稀疏。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04768，相对变化 -11.71%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation conversion-modeling curriculum-learning 搜广推 生成式召回与推理推荐 RCLRec 为什么把转化相关历史逆序放到 decoder 前缀，并按课程质量加权？ 转化标签稀疏时，最终目标难给长历史中的每一步充分监督。选择相关短子序列并逆序组织，使靠近转化的行为优先成为生成条件，联合目标提供中间学习信号。质量权重降低无信息课程的影响；但课程选择若只依赖错误相关性，也会强化偏差，因此不能把任意历史重排都称为有效课程。 示意：购买前先搜索、比较、加购，课程从更接近购买的加购行为向前组织，帮助模型学习关键链条；无关的偶然浏览被降低权重，而不是同等参与解释转化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-db3a9db18dacde46">RCLRec 为什么把转化相关历史逆序放到 decoder 前缀，并按课程质量加权？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arclrec">RCLRec: Reverse Curriculum Learning for Modeling Sparse Conversions in Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>转化标签稀疏时，最终目标难给长历史中的每一步充分监督。选择相关短子序列并逆序组织，使靠近转化的行为优先成为生成条件，联合目标提供中间学习信号。质量权重降低无信息课程的影响；但课程选择若只依赖错误相关性，也会强化偏差，因此不能把任意历史重排都称为有效课程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>购买前先搜索、比较、加购，课程从更接近购买的加购行为向前组织，帮助模型学习关键链条；无关的偶然浏览被降低权重，而不是同等参与解释转化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.28124">原论文</a> · <a href="../../../../reproductions/2603.28124-rclrec/">实现解读</a> · <a href="#qa-db3a9db18dacde46">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rclrec" data-paper-title="RCLRec: Reverse Curriculum Learning for Modeling Sparse Conversions in Generative Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="RCLRec: Reverse Curriculum Learning for Modeling Sparse Conversions in Generative Recommendation 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-03-30 RCLRec 从行为历史里选择与转化相关的短子序列，并按逆时间顺序作为 decoder 前缀。联合生成目标提供逐样本的中间监督，质量感知损失抑制无信息课程，缓解转化标签稀疏。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04768，相对变化 -11.71%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation conversion-modeling curriculum-learning 搜广推 生成式召回与推理推荐 质量加权课程与所有构造序列等权，相比怎样抑制无信息监督？ q(C) 调节课程损失贡献，弱或无关片段少影响主目标，避免稀疏转化被低质中间任务带偏。质量估计也可能错误，权重过度集中会减少覆盖。机制不等于效果保证，来源公开代理退化需保留。 示意：重复十次无关点击虽能组成长课程，不应比一次清楚的比较—加购链得到更多权重；质量系数控制它而不是按长度奖励。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e5a302e159bb2001">质量加权课程与所有构造序列等权，相比怎样抑制无信息监督？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arclrec">RCLRec: Reverse Curriculum Learning for Modeling Sparse Conversions in Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>q(C) 调节课程损失贡献，弱或无关片段少影响主目标，避免稀疏转化被低质中间任务带偏。质量估计也可能错误，权重过度集中会减少覆盖。机制不等于效果保证，来源公开代理退化需保留。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>重复十次无关点击虽能组成长课程，不应比一次清楚的比较—加购链得到更多权重；质量系数控制它而不是按长度奖励。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.28124">原论文</a> · <a href="../../../../reproductions/2603.28124-rclrec/">实现解读</a> · <a href="#qa-e5a302e159bb2001">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rclrec" data-paper-title="RCLRec: Reverse Curriculum Learning for Modeling Sparse Conversions in Generative Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="RCLRec: Reverse Curriculum Learning for Modeling Sparse Conversions in Generative Recommendation 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-03-30 RCLRec 从行为历史里选择与转化相关的短子序列，并按逆时间顺序作为 decoder 前缀。联合生成目标提供逐样本的中间监督，质量感知损失抑制无信息课程，缓解转化标签稀疏。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04768，相对变化 -11.71%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation conversion-modeling curriculum-learning 搜广推 生成式召回与推理推荐 RCLRec 的 reverse sequence 在实现时，为什么要保留事件时间与可见性含义？ 逆序是组织训练前缀，不允许把目标后的事件加入证据。选择范围、排序方向与质量 mask 都要明确，decoder 因果规则也要对应变换后布局。若仅反转 tensor 却沿用错误位置标签，模型学到的并非原定义课程。 示意：训练取购买前加购和比较可倒序呈现，购买后的退货不能因此混入前缀；倒序不改变事件本来何时才可知道。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-86f07186e44d3ca0">RCLRec 的 reverse sequence 在实现时，为什么要保留事件时间与可见性含义？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arclrec">RCLRec: Reverse Curriculum Learning for Modeling Sparse Conversions in Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>逆序是组织训练前缀，不允许把目标后的事件加入证据。选择范围、排序方向与质量 mask 都要明确，decoder 因果规则也要对应变换后布局。若仅反转 tensor 却沿用错误位置标签，模型学到的并非原定义课程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练取购买前加购和比较可倒序呈现，购买后的退货不能因此混入前缀；倒序不改变事件本来何时才可知道。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.28124">原论文</a> · <a href="../../../../reproductions/2603.28124-rclrec/">实现解读</a> · <a href="#qa-86f07186e44d3ca0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:aigq" data-paper-title="AIGQ: An End-to-End Hybrid Generative Architecture for E-commerce Query Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="AIGQ: An End-to-End Hybrid Generative Architecture for E-commerce Query Recommendation 搜广推与 LLM 应用 Taobao &amp; Tmall Group / Alibaba 2026-03-20 Direct 路径负责低时延，Reasoning 路径补足复杂意图；IL-GRPO 用线上 CTR 奖励优化整组 query，并采用离线/在线混合服务。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 aigq 核心机制，相对 NDCG@10 +8.09%。  query-recommendation generative-recommendation reinforcement-learning 搜广推 生成式召回与推理推荐 AIGQ 为什么把推荐 query 看作一组输出，而不是互不关联的多个字符串？ 一组查询共同决定用户可探索的入口，逐条看起来合理也可能全部重复同一意图。组级奖励让训练评价整组覆盖与参与价值，Direct 与 Reasoning 路径再承担不同复杂度请求。组级优化依赖奖励质量，不能仅用输出条数推断意图更丰富。 示意：五条都改写成“推荐好看的电影”没有增加选择；同一组覆盖导演、氛围和观看时长需求，才可能提供不同探索入口。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-aigq-4359f5f2" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-85620789beeec609">AIGQ 为什么把推荐 query 看作一组输出，而不是互不关联的多个字符串？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aaigq">AIGQ: An End-to-End Hybrid Generative Architecture for E-commerce Query Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一组查询共同决定用户可探索的入口，逐条看起来合理也可能全部重复同一意图。组级奖励让训练评价整组覆盖与参与价值，Direct 与 Reasoning 路径再承担不同复杂度请求。组级优化依赖奖励质量，不能仅用输出条数推断意图更丰富。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>五条都改写成“推荐好看的电影”没有增加选择；同一组覆盖导演、氛围和观看时长需求，才可能提供不同探索入口。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.19710">原论文</a> · <a href="../../../../reproductions/2603.19710-aigq/">实现解读</a> · <a href="#qa-85620789beeec609">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:aigq" data-paper-title="AIGQ: An End-to-End Hybrid Generative Architecture for E-commerce Query Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="AIGQ: An End-to-End Hybrid Generative Architecture for E-commerce Query Recommendation 搜广推与 LLM 应用 Taobao &amp; Tmall Group / Alibaba 2026-03-20 Direct 路径负责低时延，Reasoning 路径补足复杂意图；IL-GRPO 用线上 CTR 奖励优化整组 query，并采用离线/在线混合服务。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 aigq 核心机制，相对 NDCG@10 +8.09%。  query-recommendation generative-recommendation reinforcement-learning 搜广推 生成式召回与推理推荐 AIGQ为什么同时保留Direct与Reasoning两条查询推荐路径？ 简单意图需要低延迟直接生成，复杂意图则可能受益于更充分的推理，两路承担不同成本与质量需求。IL-GRPO用整组query的反馈对齐组合效果，并通过离线与在线混合服务减少请求时负担；它不是把单条查询得分独立最大化。本地代理实验不能证明完整线上CTR奖励和双路服务已复现。 示意：输入品牌名时直接补全即可；含糊的送礼需求可能先推断对象和用途，再提出互补查询，避免多条结果只是同一句话的改写。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-49d1587cf0ff9fec">AIGQ为什么同时保留Direct与Reasoning两条查询推荐路径？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aaigq">AIGQ: An End-to-End Hybrid Generative Architecture for E-commerce Query Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>简单意图需要低延迟直接生成，复杂意图则可能受益于更充分的推理，两路承担不同成本与质量需求。IL-GRPO用整组query的反馈对齐组合效果，并通过离线与在线混合服务减少请求时负担；它不是把单条查询得分独立最大化。本地代理实验不能证明完整线上CTR奖励和双路服务已复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>输入品牌名时直接补全即可；含糊的送礼需求可能先推断对象和用途，再提出互补查询，避免多条结果只是同一句话的改写。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.19710">原论文</a> · <a href="../../../../reproductions/2603.19710-aigq/">实现解读</a> · <a href="#qa-49d1587cf0ff9fec">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:aigq" data-paper-title="AIGQ: An End-to-End Hybrid Generative Architecture for E-commerce Query Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="AIGQ: An End-to-End Hybrid Generative Architecture for E-commerce Query Recommendation 搜广推与 LLM 应用 Taobao &amp; Tmall Group / Alibaba 2026-03-20 Direct 路径负责低时延，Reasoning 路径补足复杂意图；IL-GRPO 用线上 CTR 奖励优化整组 query，并采用离线/在线混合服务。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 aigq 核心机制，相对 NDCG@10 +8.09%。  query-recommendation generative-recommendation reinforcement-learning 搜广推 生成式召回与推理推荐 AIGQ 的 KL 约束与单纯最大化 CTR 奖励相比，限制了哪种更新风险？ 直接追逐奖励可能把查询推向狭窄、投机或偏离原任务的表达。相对参考策略的 KL 项为大幅分布偏移付出代价，在参与反馈与已有能力之间建立取舍。它不能保证奖励无偏，也不等于输出质量已获得独立验证。 示意：某类夸张查询一时更易被点击，纯奖励可能让整组都变成它；参考策略约束让模型提高这类概率时也考虑偏离原分布的代价。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-138f5c947c2e69f0">AIGQ 的 KL 约束与单纯最大化 CTR 奖励相比，限制了哪种更新风险？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aaigq">AIGQ: An End-to-End Hybrid Generative Architecture for E-commerce Query Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直接追逐奖励可能把查询推向狭窄、投机或偏离原任务的表达。相对参考策略的 KL 项为大幅分布偏移付出代价，在参与反馈与已有能力之间建立取舍。它不能保证奖励无偏，也不等于输出质量已获得独立验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某类夸张查询一时更易被点击，纯奖励可能让整组都变成它；参考策略约束让模型提高这类概率时也考虑偏离原分布的代价。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.19710">原论文</a> · <a href="../../../../reproductions/2603.19710-aigq/">实现解读</a> · <a href="#qa-138f5c947c2e69f0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:aigq" data-paper-title="AIGQ: An End-to-End Hybrid Generative Architecture for E-commerce Query Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="AIGQ: An End-to-End Hybrid Generative Architecture for E-commerce Query Recommendation 搜广推与 LLM 应用 Taobao &amp; Tmall Group / Alibaba 2026-03-20 Direct 路径负责低时延，Reasoning 路径补足复杂意图；IL-GRPO 用线上 CTR 奖励优化整组 query，并采用离线/在线混合服务。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 aigq 核心机制，相对 NDCG@10 +8.09%。  query-recommendation generative-recommendation reinforcement-learning 搜广推 生成式召回与推理推荐 本地 AIGQ 的 MovieLens 分数能验证线上 IL-GRPO 和延迟策略吗？ 不能。本地记录是同候选与种子下加入核心代理机制的公开数据排序结果，验证集选择混合权重；没有真实查询 CTR 奖励和线上混合服务链路。应将代理打分结果、组级策略训练与真实延迟测量分别记账。 示意：电影候选 NDCG 变好只能说明该公开代理排序变化，不能据此给真实查询服务承诺毫秒延迟，或声称线上 CTR 强化学习已经执行。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-83c770e041a1cce0">本地 AIGQ 的 MovieLens 分数能验证线上 IL-GRPO 和延迟策略吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aaigq">AIGQ: An End-to-End Hybrid Generative Architecture for E-commerce Query Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。本地记录是同候选与种子下加入核心代理机制的公开数据排序结果，验证集选择混合权重；没有真实查询 CTR 奖励和线上混合服务链路。应将代理打分结果、组级策略训练与真实延迟测量分别记账。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>电影候选 NDCG 变好只能说明该公开代理排序变化，不能据此给真实查询服务承诺毫秒延迟，或声称线上 CTR 强化学习已经执行。</p>
<p class="ar-learning-sources">依据：本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.19710">原论文</a> · <a href="../../../../reproductions/2603.19710-aigq/">实现解读</a> · <a href="#qa-83c770e041a1cce0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:glide" data-paper-title="Deploying Semantic ID-based Generative Retrieval for Large-Scale Podcast Discovery at Spotify" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Deploying Semantic ID-based Generative Retrieval for Large-Scale Podcast Discovery at Spotify 搜广推与 LLM 应用 Spotify 2026-03-18 纯近期序列容易只召回习惯内容。GLIDE 用 Semantic ID 自回归生成候选，同时把近期行为和长期用户 embedding 作为两类 prompt，兼顾即时意图与探索。 复现保真度：核心机制复现。复现保真度：核心机制复现。Residual Semantic ID、code 生成和双时间尺度 prompt 均实际执行。公开 item feature 做三级 residual quantization，以 code transition 生成并融合短期历史/长期内容画像。  generative-retrieval semantic-id soft-prompt 搜广推 生成式召回与推理推荐 GLIDE 为什么把近期行为与长期 embedding 分成两类 prompt？ 近期序列保留即时需求细节，长期向量概括稳定偏好，分开输入让生成器同时利用而非混成同一平均。SID 分层生成提供候选路径，探索仍受两类条件与码本覆盖限制，不能仅凭长短结合就断言缓解信息茧房。 示意：长期爱摄影、最近筹备露营，两类 prompt 可同时保留；模型生成户外相机或露营物品时有不同依据，而非只看最后一次点击。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-glide-1ae86d8e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0cbf0ecf4df68a6c">GLIDE 为什么把近期行为与长期 embedding 分成两类 prompt？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aglide">Deploying Semantic ID-based Generative Retrieval for Large-Scale Podcast Discovery at Spotify</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Spotify</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>近期序列保留即时需求细节，长期向量概括稳定偏好，分开输入让生成器同时利用而非混成同一平均。SID 分层生成提供候选路径，探索仍受两类条件与码本覆盖限制，不能仅凭长短结合就断言缓解信息茧房。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>长期爱摄影、最近筹备露营，两类 prompt 可同时保留；模型生成户外相机或露营物品时有不同依据，而非只看最后一次点击。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.17540">原论文</a> · <a href="../../../../reproductions/2603.17540-glide/">实现解读</a> · <a href="#qa-0cbf0ecf4df68a6c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:glide" data-paper-title="Deploying Semantic ID-based Generative Retrieval for Large-Scale Podcast Discovery at Spotify" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Deploying Semantic ID-based Generative Retrieval for Large-Scale Podcast Discovery at Spotify 搜广推与 LLM 应用 Spotify 2026-03-18 纯近期序列容易只召回习惯内容。GLIDE 用 Semantic ID 自回归生成候选，同时把近期行为和长期用户 embedding 作为两类 prompt，兼顾即时意图与探索。 复现保真度：核心机制复现。复现保真度：核心机制复现。Residual Semantic ID、code 生成和双时间尺度 prompt 均实际执行。公开 item feature 做三级 residual quantization，以 code transition 生成并融合短期历史/长期内容画像。  generative-retrieval semantic-id soft-prompt 搜广推 生成式召回与推理推荐 GLIDE为什么把近期行为和长期用户embedding分别作为prompt？ 近期序列能响应刚发生的意图，却容易反复推荐熟悉内容；长期表示补充更稳定、可能被短窗口遗漏的偏好。两类prompt共同条件化SID生成，让模型在即时需求与探索之间选择。长期向量不是永远正确的背景，兴趣漂移时仍需检查其影响，不能简单拼长历史后就声称具有探索能力。 示意：用户最近只听通勤播客，但长期喜欢科学主题；两路提示可让模型在满足当前场景时发现新的科学节目，而不是只复述刚听过的系列。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-0b2de1129245e709">GLIDE为什么把近期行为和长期用户embedding分别作为prompt？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aglide">Deploying Semantic ID-based Generative Retrieval for Large-Scale Podcast Discovery at Spotify</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Spotify</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>近期序列能响应刚发生的意图，却容易反复推荐熟悉内容；长期表示补充更稳定、可能被短窗口遗漏的偏好。两类prompt共同条件化SID生成，让模型在即时需求与探索之间选择。长期向量不是永远正确的背景，兴趣漂移时仍需检查其影响，不能简单拼长历史后就声称具有探索能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户最近只听通勤播客，但长期喜欢科学主题；两路提示可让模型在满足当前场景时发现新的科学节目，而不是只复述刚听过的系列。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.17540">原论文</a> · <a href="../../../../reproductions/2603.17540-glide/">实现解读</a> · <a href="#qa-0b2de1129245e709">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:glide" data-paper-title="Deploying Semantic ID-based Generative Retrieval for Large-Scale Podcast Discovery at Spotify" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Deploying Semantic ID-based Generative Retrieval for Large-Scale Podcast Discovery at Spotify 搜广推与 LLM 应用 Spotify 2026-03-18 纯近期序列容易只召回习惯内容。GLIDE 用 Semantic ID 自回归生成候选，同时把近期行为和长期用户 embedding 作为两类 prompt，兼顾即时意图与探索。 复现保真度：核心机制复现。复现保真度：核心机制复现。Residual Semantic ID、code 生成和双时间尺度 prompt 均实际执行。公开 item feature 做三级 residual quantization，以 code transition 生成并融合短期历史/长期内容画像。  generative-retrieval semantic-id soft-prompt 搜广推 生成式召回与推理推荐 GLIDE 的双 prompt 生成与传统 transition/content retrieval，相比输出接口怎样变化？ 传统方案直接组合相似度或转移得分，GLIDE 学习条件化 SID 路径概率，再映射到候选。它借离散结构共享语义，也增加量化与早期码错误风险。来源本地用 code transition 代理核心，不能据同名结果认定完整语言生成器已被训练。 示意：不是给每件相机加历史转移分，而是先生成摄影粗码再细化；若粗码选错，目标可能被提前排除，传统全库打分则是另一类覆盖。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e7e19c426f1e5e87">GLIDE 的双 prompt 生成与传统 transition/content retrieval，相比输出接口怎样变化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aglide">Deploying Semantic ID-based Generative Retrieval for Large-Scale Podcast Discovery at Spotify</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Spotify</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>传统方案直接组合相似度或转移得分，GLIDE 学习条件化 SID 路径概率，再映射到候选。它借离散结构共享语义，也增加量化与早期码错误风险。来源本地用 code transition 代理核心，不能据同名结果认定完整语言生成器已被训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>不是给每件相机加历史转移分，而是先生成摄影粗码再细化；若粗码选错，目标可能被提前排除，传统全库打分则是另一类覆盖。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.17540">原论文</a> · <a href="../../../../reproductions/2603.17540-glide/">实现解读</a> · <a href="#qa-e7e19c426f1e5e87">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:glide" data-paper-title="Deploying Semantic ID-based Generative Retrieval for Large-Scale Podcast Discovery at Spotify" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Deploying Semantic ID-based Generative Retrieval for Large-Scale Podcast Discovery at Spotify 搜广推与 LLM 应用 Spotify 2026-03-18 纯近期序列容易只召回习惯内容。GLIDE 用 Semantic ID 自回归生成候选，同时把近期行为和长期用户 embedding 作为两类 prompt，兼顾即时意图与探索。 复现保真度：核心机制复现。复现保真度：核心机制复现。Residual Semantic ID、code 生成和双时间尺度 prompt 均实际执行。公开 item feature 做三级 residual quantization，以 code transition 生成并融合短期历史/长期内容画像。  generative-retrieval semantic-id soft-prompt 搜广推 生成式召回与推理推荐 GLIDE 的长期 embedding 构造为什么不能使用测试后的全用户历史？ 长期画像应只汇总截止当前的可用行为，近期分支同样需截断。将最终测试目标放进长期向量会产生隐蔽泄漏，即使近期序列没有它。码本也应明确拟合口径，本地三级量化与公开代理的范围需记录。 示意：预测最后一部电影时，若长期画像已平均了这部电影向量，模型其实读到了答案；长短两个输入都必须检查截止时间。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c75b3e3a99ba4ee5">GLIDE 的长期 embedding 构造为什么不能使用测试后的全用户历史？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aglide">Deploying Semantic ID-based Generative Retrieval for Large-Scale Podcast Discovery at Spotify</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Spotify</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长期画像应只汇总截止当前的可用行为，近期分支同样需截断。将最终测试目标放进长期向量会产生隐蔽泄漏，即使近期序列没有它。码本也应明确拟合口径，本地三级量化与公开代理的范围需记录。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>预测最后一部电影时，若长期画像已平均了这部电影向量，模型其实读到了答案；长短两个输入都必须检查截止时间。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.17540">原论文</a> · <a href="../../../../reproductions/2603.17540-glide/">实现解读</a> · <a href="#qa-c75b3e3a99ba4ee5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:oneranker" data-paper-title="OneRanker: Unified Generation and Ranking with One Model in Industrial Advertising Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneRanker: Unified Generation and Ranking with One Model in Industrial Advertising Recommendation 搜广推与 LLM 应用 Tencent 2026-03-03 用 fake item token 统一生成、点击价值估计和广告排序，并通过分布一致性约束让生成概率与 value head 保持同一偏好。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 oneranker 核心机制；相对 NDCG@10 -7.65%。  advertising generative-recommendation ranking multi-task 搜广推 生成式召回与推理推荐 OneRanker 的 fake item token 统一了哪些预测接口？ 同一表示接口承接生成与价值判断，使广告候选的出现概率和后续排序有共同上下文，减少独立模块目标割裂。fake token 是模型结构角色，不是假造真实物品；仍须把输出映到合法目录，并区分生成头与价值头目标。 示意：一份候选状态同时支持“容易生成吗”和“预期价值多大”，但不能把内部占位 token 当成可投放广告返回给用户。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-oneranker-399e9549" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-66bd49fd12f9b319">OneRanker 的 fake item token 统一了哪些预测接口？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aoneranker">OneRanker: Unified Generation and Ranking with One Model in Industrial Advertising Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一表示接口承接生成与价值判断，使广告候选的出现概率和后续排序有共同上下文，减少独立模块目标割裂。fake token 是模型结构角色，不是假造真实物品；仍须把输出映到合法目录，并区分生成头与价值头目标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一份候选状态同时支持“容易生成吗”和“预期价值多大”，但不能把内部占位 token 当成可投放广告返回给用户。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.02999">原论文</a> · <a href="../../../../reproductions/2603.02999-oneranker/">实现解读</a> · <a href="#qa-66bd49fd12f9b319">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:oneranker" data-paper-title="OneRanker: Unified Generation and Ranking with One Model in Industrial Advertising Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneRanker: Unified Generation and Ranking with One Model in Industrial Advertising Recommendation 搜广推与 LLM 应用 Tencent 2026-03-03 用 fake item token 统一生成、点击价值估计和广告排序，并通过分布一致性约束让生成概率与 value head 保持同一偏好。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 oneranker 核心机制；相对 NDCG@10 -7.65%。  advertising generative-recommendation ranking multi-task 搜广推 生成式召回与推理推荐 OneRanker 为什么要约束生成分布和 value head 的偏好一致？ 生成头决定哪些候选容易出现，价值头决定出现后怎样排序。若两者偏好不一致，生成器可能持续漏掉价值头最看重的物品，末端重排也无法补回。共享 fake item token 提供统一接口，分布一致性损失进一步连接两条学习信号；代价是需要平衡生成拟合、价值预测和一致性约束，避免互相压制。 示意：生成器总给便宜配件高概率，价值头却更看好适合用户的耐用工具。只重排现有配件无法展示工具；一致性训练试图让工具在生成阶段也得到机会。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-7e52b4a05d3de442">OneRanker 为什么要约束生成分布和 value head 的偏好一致？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aoneranker">OneRanker: Unified Generation and Ranking with One Model in Industrial Advertising Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>生成头决定哪些候选容易出现，价值头决定出现后怎样排序。若两者偏好不一致，生成器可能持续漏掉价值头最看重的物品，末端重排也无法补回。共享 fake item token 提供统一接口，分布一致性损失进一步连接两条学习信号；代价是需要平衡生成拟合、价值预测和一致性约束，避免互相压制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>生成器总给便宜配件高概率，价值头却更看好适合用户的耐用工具。只重排现有配件无法展示工具；一致性训练试图让工具在生成阶段也得到机会。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.02999">原论文</a> · <a href="../../../../reproductions/2603.02999-oneranker/">实现解读</a> · <a href="#qa-7e52b4a05d3de442">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:oneranker" data-paper-title="OneRanker: Unified Generation and Ranking with One Model in Industrial Advertising Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneRanker: Unified Generation and Ranking with One Model in Industrial Advertising Recommendation 搜广推与 LLM 应用 Tencent 2026-03-03 用 fake item token 统一生成、点击价值估计和广告排序，并通过分布一致性约束让生成概率与 value head 保持同一偏好。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 oneranker 核心机制；相对 NDCG@10 -7.65%。  advertising generative-recommendation ranking multi-task 搜广推 生成式召回与推理推荐 生成一致性 KL 与只用共享主干，有什么额外约束？ 共享参数仍可让不同 head 学出相反偏好，KL 明确要求两个分布在相同候选空间接近。它可能减少冲突，也会限制各自专长，权重需校准。不能由一致性更高推断推荐更好，两个头也可能一致地偏向错误热门项。 示意：生成器爱配件、价值头爱耐用工具，共享主干不保证两者选同一对象；KL 才直接惩罚这种差异，但也要检查谁在教谁。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-fddb820b8e41367d">生成一致性 KL 与只用共享主干，有什么额外约束？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aoneranker">OneRanker: Unified Generation and Ranking with One Model in Industrial Advertising Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共享参数仍可让不同 head 学出相反偏好，KL 明确要求两个分布在相同候选空间接近。它可能减少冲突，也会限制各自专长，权重需校准。不能由一致性更高推断推荐更好，两个头也可能一致地偏向错误热门项。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>生成器爱配件、价值头爱耐用工具，共享主干不保证两者选同一对象；KL 才直接惩罚这种差异，但也要检查谁在教谁。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.02999">原论文</a> · <a href="../../../../reproductions/2603.02999-oneranker/">实现解读</a> · <a href="#qa-fddb820b8e41367d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:oneranker" data-paper-title="OneRanker: Unified Generation and Ranking with One Model in Industrial Advertising Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneRanker: Unified Generation and Ranking with One Model in Industrial Advertising Recommendation 搜广推与 LLM 应用 Tencent 2026-03-03 用 fake item token 统一生成、点击价值估计和广告排序，并通过分布一致性约束让生成概率与 value head 保持同一偏好。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 oneranker 核心机制；相对 NDCG@10 -7.65%。  advertising generative-recommendation ranking multi-task 搜广推 生成式召回与推理推荐 OneRanker 计算 pgen 与 prank 的 KL，为什么不能拿原始 logits 直接相减？ KL 比较归一概率分布，需要相同候选身份和温度口径，未归一数值差不是同一目标。非法或 padding 项应一致屏蔽，价值标签不得泄漏到生成输入。只靠固定分数加权代理，无法证明分布一致性梯度实际训练。 示意：两头 logits 同时加常数不改分布，直接平方差却变化；若一个在全库、另一个只在十项归一，也不能直接当相同 KL。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b88a0ca0f5a2a616">OneRanker 计算 pgen 与 prank 的 KL，为什么不能拿原始 logits 直接相减？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aoneranker">OneRanker: Unified Generation and Ranking with One Model in Industrial Advertising Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>KL 比较归一概率分布，需要相同候选身份和温度口径，未归一数值差不是同一目标。非法或 padding 项应一致屏蔽，价值标签不得泄漏到生成输入。只靠固定分数加权代理，无法证明分布一致性梯度实际训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两头 logits 同时加常数不改分布，直接平方差却变化；若一个在全库、另一个只在十项归一，也不能直接当相同 KL。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.02999">原论文</a> · <a href="../../../../reproductions/2603.02999-oneranker/">实现解读</a> · <a href="#qa-b88a0ca0f5a2a616">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:grc" data-paper-title="Learning to Reflect and Correct: Towards Better Decoding Trajectories for Large-Scale Generative Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Learning to Reflect and Correct: Towards Better Decoding Trajectories for Large-Scale Generative Recommendation 搜广推与 LLM 应用 Alibaba International / Wuhan University 2026-02-27 Semantic ID 自回归生成的早期错误会向后传播。GRC 把 draft SID、首错位置/属性一致性反思、corrected SID 串成结构化模板；再对完整轨迹做 GRPO，并用反思 token 熵把固定纠错预算分配给最不确定的 beam。 Fidelity: 核心机制复现。结构化 SFT、完整轨迹 GRPO 与 entropy-guided reflection scheduling 均实际执行。MovieLens genre 代理 category/seller/brand 属性；未复刻工业 LLM 参数量。本地对照口径：基线是同一 SID 的 GR backbone；实验组 GRC 加入 1,320 条结构化轨迹、10 轮 GRPO 与 EGRS，相对基线 Hit@10 -12.50%、NDCG@10 -11.12%。  generative-recommendation reinforcement-learning self-correction 搜广推 生成式召回与推理推荐 GRC 为什么把 draft、反思与 corrected SID 写成结构化轨迹？ 层级生成的早期错误会限制后续路径，显式记录草稿和纠正过程让模型学习定位与修复，而不是只看到最终正确码。结构化步骤仍是训练监督，推理必须自行判断哪里可能错，不能直接得到真实首错位置。轨迹格式正确也不保证修复有效。 示意：先走到家居粗码，再发现用户要摄影而改到相机路径；模型要学习如何发现偏离，而非测试时由答案告诉它第一层错了。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-grc-7f75523b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-22487c67ad9da2a1">GRC 为什么把 draft、反思与 corrected SID 写成结构化轨迹？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agrc">Learning to Reflect and Correct: Towards Better Decoding Trajectories for Large-Scale Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International / Wuhan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>层级生成的早期错误会限制后续路径，显式记录草稿和纠正过程让模型学习定位与修复，而不是只看到最终正确码。结构化步骤仍是训练监督，推理必须自行判断哪里可能错，不能直接得到真实首错位置。轨迹格式正确也不保证修复有效。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先走到家居粗码，再发现用户要摄影而改到相机路径；模型要学习如何发现偏离，而非测试时由答案告诉它第一层错了。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.23639">原论文</a> · <a href="../../../../reproductions/2602.23639-grc/">实现解读</a> · <a href="#qa-22487c67ad9da2a1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:grc" data-paper-title="Learning to Reflect and Correct: Towards Better Decoding Trajectories for Large-Scale Generative Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Learning to Reflect and Correct: Towards Better Decoding Trajectories for Large-Scale Generative Recommendation 搜广推与 LLM 应用 Alibaba International / Wuhan University 2026-02-27 Semantic ID 自回归生成的早期错误会向后传播。GRC 把 draft SID、首错位置/属性一致性反思、corrected SID 串成结构化模板；再对完整轨迹做 GRPO，并用反思 token 熵把固定纠错预算分配给最不确定的 beam。 Fidelity: 核心机制复现。结构化 SFT、完整轨迹 GRPO 与 entropy-guided reflection scheduling 均实际执行。MovieLens genre 代理 category/seller/brand 属性；未复刻工业 LLM 参数量。本地对照口径：基线是同一 SID 的 GR backbone；实验组 GRC 加入 1,320 条结构化轨迹、10 轮 GRPO 与 EGRS，相对基线 Hit@10 -12.50%、NDCG@10 -11.12%。  generative-recommendation reinforcement-learning self-correction 搜广推 生成式召回与推理推荐 GRC训练时标注首个错误SID位置，为什么评估时不能直接把这个位置交给纠错器？ 真实目标码只在训练监督中用于构造draft—反思—纠正轨迹。部署时模型必须从当前候选、属性一致性和自身不确定性判断哪里可能错，否则就是把答案泄漏给被评估策略。熵引导把有限纠错预算分给不确定beam，但高不确定也可能只是难例，不保证一定能修正或提高召回。 示意：训练可指出草稿城市码与目标不同；实际推荐时系统不知道用户最终会选哪件商品，只能检查语义与当前证据，不能预先读目标码来定位错误。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-34cb5a2e2828c895">GRC训练时标注首个错误SID位置，为什么评估时不能直接把这个位置交给纠错器？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agrc">Learning to Reflect and Correct: Towards Better Decoding Trajectories for Large-Scale Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International / Wuhan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>真实目标码只在训练监督中用于构造draft—反思—纠正轨迹。部署时模型必须从当前候选、属性一致性和自身不确定性判断哪里可能错，否则就是把答案泄漏给被评估策略。熵引导把有限纠错预算分给不确定beam，但高不确定也可能只是难例，不保证一定能修正或提高召回。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练可指出草稿城市码与目标不同；实际推荐时系统不知道用户最终会选哪件商品，只能检查语义与当前证据，不能预先读目标码来定位错误。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.23639">原论文</a> · <a href="../../../../reproductions/2602.23639-grc/">实现解读</a> · <a href="#qa-34cb5a2e2828c895">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:grc" data-paper-title="Learning to Reflect and Correct: Towards Better Decoding Trajectories for Large-Scale Generative Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Learning to Reflect and Correct: Towards Better Decoding Trajectories for Large-Scale Generative Recommendation 搜广推与 LLM 应用 Alibaba International / Wuhan University 2026-02-27 Semantic ID 自回归生成的早期错误会向后传播。GRC 把 draft SID、首错位置/属性一致性反思、corrected SID 串成结构化模板；再对完整轨迹做 GRPO，并用反思 token 熵把固定纠错预算分配给最不确定的 beam。 Fidelity: 核心机制复现。结构化 SFT、完整轨迹 GRPO 与 entropy-guided reflection scheduling 均实际执行。MovieLens genre 代理 category/seller/brand 属性；未复刻工业 LLM 参数量。本地对照口径：基线是同一 SID 的 GR backbone；实验组 GRC 加入 1,320 条结构化轨迹、10 轮 GRPO 与 EGRS，相对基线 Hit@10 -12.50%、NDCG@10 -11.12%。  generative-recommendation reinforcement-learning self-correction 搜广推 生成式召回与推理推荐 GRC 的不确定性纠错预算与给所有 beam 相同修复次数，相比有什么取舍？ 反思 token 熵用于选择更不确定的路径，把固定预算集中到可能值得纠正的分支，避免所有候选重复相同工作。高熵也可能只是无意义噪声，低熵可能自信地错，因此需要结果验证。来源 reward 上升但 test 排序下降，不能只挑训练奖励。 示意：十条 beam 中两条明显犹豫，优先修它们可省计算；但若一条错误路径十分自信，它也可能被漏过，熵不是正确率标签。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c072daa2eaad153e">GRC 的不确定性纠错预算与给所有 beam 相同修复次数，相比有什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agrc">Learning to Reflect and Correct: Towards Better Decoding Trajectories for Large-Scale Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International / Wuhan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>反思 token 熵用于选择更不确定的路径，把固定预算集中到可能值得纠正的分支，避免所有候选重复相同工作。高熵也可能只是无意义噪声，低熵可能自信地错，因此需要结果验证。来源 reward 上升但 test 排序下降，不能只挑训练奖励。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>十条 beam 中两条明显犹豫，优先修它们可省计算；但若一条错误路径十分自信，它也可能被漏过，熵不是正确率标签。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.23639">原论文</a> · <a href="../../../../reproductions/2602.23639-grc/">实现解读</a> · <a href="#qa-c072daa2eaad153e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:grc" data-paper-title="Learning to Reflect and Correct: Towards Better Decoding Trajectories for Large-Scale Generative Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Learning to Reflect and Correct: Towards Better Decoding Trajectories for Large-Scale Generative Recommendation 搜广推与 LLM 应用 Alibaba International / Wuhan University 2026-02-27 Semantic ID 自回归生成的早期错误会向后传播。GRC 把 draft SID、首错位置/属性一致性反思、corrected SID 串成结构化模板；再对完整轨迹做 GRPO，并用反思 token 熵把固定纠错预算分配给最不确定的 beam。 Fidelity: 核心机制复现。结构化 SFT、完整轨迹 GRPO 与 entropy-guided reflection scheduling 均实际执行。MovieLens genre 代理 category/seller/brand 属性；未复刻工业 LLM 参数量。本地对照口径：基线是同一 SID 的 GR backbone；实验组 GRC 加入 1,320 条结构化轨迹、10 轮 GRPO 与 EGRS，相对基线 Hit@10 -12.50%、NDCG@10 -11.12%。  generative-recommendation reinforcement-learning self-correction 搜广推 生成式召回与推理推荐 GRC 训练首错标签与测试反思输入应如何隔离？ 训练可比较草稿与 gold SID 定义首错，全部正确时使用 L+1；测试只能用模型自身草稿、属性和不确定性生成反思，不能传入 gold 差异。反思、纠正和奖励需绑定同一轨迹，避免用答案修补后再算能力。 示意：草稿三层都对时标记无错合法；评估若先拿真实码算出第二层错再告诉纠错器，就从自主纠正退化成有答案的组件诊断。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-bd4e3f5d3c957901">GRC 训练首错标签与测试反思输入应如何隔离？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agrc">Learning to Reflect and Correct: Towards Better Decoding Trajectories for Large-Scale Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International / Wuhan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>训练可比较草稿与 gold SID 定义首错，全部正确时使用 L+1；测试只能用模型自身草稿、属性和不确定性生成反思，不能传入 gold 差异。反思、纠正和奖励需绑定同一轨迹，避免用答案修补后再算能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>草稿三层都对时标记无错合法；评估若先拿真实码算出第二层错再告诉纠错器，就从自主纠正退化成有答案的组件诊断。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.23639">原论文</a> · <a href="../../../../reproductions/2602.23639-grc/">实现解读</a> · <a href="#qa-bd4e3f5d3c957901">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gr4ad" data-paper-title="Generative Recommendation for Large-Scale Advertising" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Generative Recommendation for Large-Scale Advertising 搜广推与 LLM 应用 Kuaishou 2026-02-26 广告生成式推荐同时受商业语义、实时更新和延迟约束。GR4AD 用多粒度 UA-SID 编码广告，LazyAR 放松层间自回归依赖，VSL 按商业价值加权监督，RSPO 直接优化列表排序，Dynamic Beam Serving 随负载调整 beam。 Fidelity: 核心机制复现。UA-SID、并行 LazyAR、VSL、list-wise RSPO 均训练；私有多模态广告、eCPM、在线持续学习和动态 beam 服务未复刻。本地对照口径：统一跨模型基线是 DIN，GR4AD NDCG@10 相对 DIN +69.67%；内部 DLRM 基线加入 UA-SID/LazyAR/VSL/RSPO 后 +49.88%。两项都伴随 head share 0.505 的偏置风险。60 steps、180 users/280 items、seeds 42–44。统一 DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；  generative-retrieval advertising reinforcement-learning serving 搜广推 生成式召回与推理推荐 GR4AD 为什么同时考虑商业 SID、生成依赖与负载下 beam 预算？ 广告不仅要相关，还需表达业务属性、快速适应更新并满足延迟。UA-SID 提供多粒度接口，LazyAR 减轻逐层依赖，价值训练与列表目标连接收益，动态 beam 管理服务成本。几个瓶颈不同，不能用单一 next-code 准确率代表整体成功。 示意：高价值广告若解码太慢仍不可服务，beam 太窄又可能漏候选；内容编码与调度预算都需参与，而不是只增加模型参数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-gr4ad-4d146b97" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5b9317365ed4f756">GR4AD 为什么同时考虑商业 SID、生成依赖与负载下 beam 预算？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agr4ad">Generative Recommendation for Large-Scale Advertising</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>广告不仅要相关，还需表达业务属性、快速适应更新并满足延迟。UA-SID 提供多粒度接口，LazyAR 减轻逐层依赖，价值训练与列表目标连接收益，动态 beam 管理服务成本。几个瓶颈不同，不能用单一 next-code 准确率代表整体成功。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>高价值广告若解码太慢仍不可服务，beam 太窄又可能漏候选；内容编码与调度预算都需参与，而不是只增加模型参数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.22732">原论文</a> · <a href="../../../../reproductions/2602.22732-gr4ad/">实现解读</a> · <a href="#qa-5b9317365ed4f756">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gr4ad" data-paper-title="Generative Recommendation for Large-Scale Advertising" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Generative Recommendation for Large-Scale Advertising 搜广推与 LLM 应用 Kuaishou 2026-02-26 广告生成式推荐同时受商业语义、实时更新和延迟约束。GR4AD 用多粒度 UA-SID 编码广告，LazyAR 放松层间自回归依赖，VSL 按商业价值加权监督，RSPO 直接优化列表排序，Dynamic Beam Serving 随负载调整 beam。 Fidelity: 核心机制复现。UA-SID、并行 LazyAR、VSL、list-wise RSPO 均训练；私有多模态广告、eCPM、在线持续学习和动态 beam 服务未复刻。本地对照口径：统一跨模型基线是 DIN，GR4AD NDCG@10 相对 DIN +69.67%；内部 DLRM 基线加入 UA-SID/LazyAR/VSL/RSPO 后 +49.88%。两项都伴随 head share 0.505 的偏置风险。60 steps、180 users/280 items、seeds 42–44。统一 DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；  generative-retrieval advertising reinforcement-learning serving 搜广推 生成式召回与推理推荐 GR4AD为什么既按商业价值加权监督，又用列表排序优化，而不只学习下一个广告码？ 单纯next-token学习曝光频率，可能让常见却价值较低的广告主导训练。价值加权改变不同样本的贡献，列表优化再关心候选之间的相对业务收益；多粒度SID和依赖放松则处理表示与计算问题。这些目标未必一致，必须检查是否牺牲相关性或过度集中头部，不能只报告收入代理的单项变化。 示意：一个广告出现很多却很少带来有效转化，另一个较少曝光但有较高业务价值；频率模仿会偏前者，价值监督与列表对齐允许表达这一区别。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-1aaa4f6709186ebb">GR4AD为什么既按商业价值加权监督，又用列表排序优化，而不只学习下一个广告码？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agr4ad">Generative Recommendation for Large-Scale Advertising</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单纯next-token学习曝光频率，可能让常见却价值较低的广告主导训练。价值加权改变不同样本的贡献，列表优化再关心候选之间的相对业务收益；多粒度SID和依赖放松则处理表示与计算问题。这些目标未必一致，必须检查是否牺牲相关性或过度集中头部，不能只报告收入代理的单项变化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个广告出现很多却很少带来有效转化，另一个较少曝光但有较高业务价值；频率模仿会偏前者，价值监督与列表对齐允许表达这一区别。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.22732">原论文</a> · <a href="../../../../reproductions/2602.22732-gr4ad/">实现解读</a> · <a href="#qa-1aaa4f6709186ebb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gr4ad" data-paper-title="Generative Recommendation for Large-Scale Advertising" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Generative Recommendation for Large-Scale Advertising 搜广推与 LLM 应用 Kuaishou 2026-02-26 广告生成式推荐同时受商业语义、实时更新和延迟约束。GR4AD 用多粒度 UA-SID 编码广告，LazyAR 放松层间自回归依赖，VSL 按商业价值加权监督，RSPO 直接优化列表排序，Dynamic Beam Serving 随负载调整 beam。 Fidelity: 核心机制复现。UA-SID、并行 LazyAR、VSL、list-wise RSPO 均训练；私有多模态广告、eCPM、在线持续学习和动态 beam 服务未复刻。本地对照口径：统一跨模型基线是 DIN，GR4AD NDCG@10 相对 DIN +69.67%；内部 DLRM 基线加入 UA-SID/LazyAR/VSL/RSPO 后 +49.88%。两项都伴随 head share 0.505 的偏置风险。60 steps、180 users/280 items、seeds 42–44。统一 DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；  generative-retrieval advertising reinforcement-learning serving 搜广推 生成式召回与推理推荐 GR4AD 的 VSL 与 RSPO，为何一个加权监督、一个对齐列表排序？ VSL 让高商业价值样本在码预测损失中更重要，RSPO 用价值奖励分布改变候选相对偏好，作用粒度不同。两者可能一起强化头部，不能只报告 NDCG 上涨；来源本地以热门度代理价值，集中风险尤需保留。 示意：高价物品在训练被多学是一种权重变化，给整组候选按奖励重新分布又是另一种排序目标；两者都偏热门时曝光可能过度集中。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-683a274918c2779d">GR4AD 的 VSL 与 RSPO，为何一个加权监督、一个对齐列表排序？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agr4ad">Generative Recommendation for Large-Scale Advertising</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>VSL 让高商业价值样本在码预测损失中更重要，RSPO 用价值奖励分布改变候选相对偏好，作用粒度不同。两者可能一起强化头部，不能只报告 NDCG 上涨；来源本地以热门度代理价值，集中风险尤需保留。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>高价物品在训练被多学是一种权重变化，给整组候选按奖励重新分布又是另一种排序目标；两者都偏热门时曝光可能过度集中。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.22732">原论文</a> · <a href="../../../../reproductions/2602.22732-gr4ad/">实现解读</a> · <a href="#qa-683a274918c2779d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gr4ad" data-paper-title="Generative Recommendation for Large-Scale Advertising" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Generative Recommendation for Large-Scale Advertising 搜广推与 LLM 应用 Kuaishou 2026-02-26 广告生成式推荐同时受商业语义、实时更新和延迟约束。GR4AD 用多粒度 UA-SID 编码广告，LazyAR 放松层间自回归依赖，VSL 按商业价值加权监督，RSPO 直接优化列表排序，Dynamic Beam Serving 随负载调整 beam。 Fidelity: 核心机制复现。UA-SID、并行 LazyAR、VSL、list-wise RSPO 均训练；私有多模态广告、eCPM、在线持续学习和动态 beam 服务未复刻。本地对照口径：统一跨模型基线是 DIN，GR4AD NDCG@10 相对 DIN +69.67%；内部 DLRM 基线加入 UA-SID/LazyAR/VSL/RSPO 后 +49.88%。两项都伴随 head share 0.505 的偏置风险。60 steps、180 users/280 items、seeds 42–44。统一 DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；  generative-retrieval advertising reinforcement-learning serving 搜广推 生成式召回与推理推荐 GR4AD 本地 RSPO 的 qj∝exp(rj/τ) 为什么要与候选概率空间一致？ 奖励分布在同一上下文合法候选上归一，再与学生相同身份概率交叉熵，温度决定锐度。候选错序、非法项或跨请求混组都会改变目标。公开价值代理与真实商业 eCPM 不同，代码执行这些损失不能自动证明 LazyAR 与动态 serving 已全部复现。 示意：奖励最高的相机在 q 的第二列，学生第二列若是童装，梯度会教错对象；先对齐身份，比只检查 q 和为一更重要。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8bae8a9f22f76a35">GR4AD 本地 RSPO 的 qj∝exp(rj/τ) 为什么要与候选概率空间一致？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agr4ad">Generative Recommendation for Large-Scale Advertising</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>奖励分布在同一上下文合法候选上归一，再与学生相同身份概率交叉熵，温度决定锐度。候选错序、非法项或跨请求混组都会改变目标。公开价值代理与真实商业 eCPM 不同，代码执行这些损失不能自动证明 LazyAR 与动态 serving 已全部复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>奖励最高的相机在 q 的第二列，学生第二列若是童装，梯度会教错对象；先对齐身份，比只检查 q 和为一更重要。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.22732">原论文</a> · <a href="../../../../reproductions/2602.22732-gr4ad/">实现解读</a> · <a href="#qa-8bae8a9f22f76a35">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sigma" data-paper-title="SIGMA: A Semantic-Grounded Instruction-Driven Generative Multi-Task Recommender at AliExpress" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="SIGMA: A Semantic-Grounded Instruction-Driven Generative Multi-Task Recommender at AliExpress 搜广推与 LLM 应用 Alibaba / AliExpress 2026-02-26 普通生成推荐只做 next-item，难以即时响应 Query、Category、Longtail、Discover、Season、Holiday 等业务任务。SIGMA 先通过搜索语义、视觉、世界知识和协同行为四类 relevance pair，把 LLM 语义与在线 ID embedding 对齐；随后用“短 SID prefix + unique item ID”同时保留生成效率和商品精度；七任务 instruction SFT 统一训练； 七任务分桶样本只有约 18/任务，逐任务数字只作诊断，不作结论。Fidelity: 完整核心链路。本地实际执行 causal-LM LoRA 多视角 InfoNCE+KD、RQ-SID prefix 与 unique ID 混合 token、七类 instruction SFT、SID-prefix NTP、同-prefix hard-negative InfoNCE、prefix beam→子目录 item retrieval→APF。不是用最终分数规则模拟 SIGMA。使用真实 SmolLM LoRA 编码与反向，不是固定 embedding 直接代替 multi-view grounding；  generative-recommendation multi-task-sft hybrid-token semantic-grounding 搜广推 生成式召回与推理推荐 SIGMA为什么用短SID prefix再接unique item？ 短前缀缩小生成搜索空间，独立item表征保留精确身份，再在前缀局部目录检索。它折中全SID长解码与全库ANN，不把共享语义码当唯一商品身份。 例如先选运动鞋语义区，再区内区分具体款式。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-sigma-3e17a33a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-354f3ed585098924">SIGMA为什么用短SID prefix再接unique item？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asigma">SIGMA: A Semantic-Grounded Instruction-Driven Generative Multi-Task Recommender at AliExpress</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / AliExpress</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>短前缀缩小生成搜索空间，独立item表征保留精确身份，再在前缀局部目录检索。它折中全SID长解码与全库ANN，不把共享语义码当唯一商品身份。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先选运动鞋语义区，再区内区分具体款式。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.22913">原论文</a> · <a href="../../../../reproductions/2602.22913-sigma/">实现解读</a> · <a href="#qa-354f3ed585098924">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sigma" data-paper-title="SIGMA: A Semantic-Grounded Instruction-Driven Generative Multi-Task Recommender at AliExpress" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="SIGMA: A Semantic-Grounded Instruction-Driven Generative Multi-Task Recommender at AliExpress 搜广推与 LLM 应用 Alibaba / AliExpress 2026-02-26 普通生成推荐只做 next-item，难以即时响应 Query、Category、Longtail、Discover、Season、Holiday 等业务任务。SIGMA 先通过搜索语义、视觉、世界知识和协同行为四类 relevance pair，把 LLM 语义与在线 ID embedding 对齐；随后用“短 SID prefix + unique item ID”同时保留生成效率和商品精度；七任务 instruction SFT 统一训练； 七任务分桶样本只有约 18/任务，逐任务数字只作诊断，不作结论。Fidelity: 完整核心链路。本地实际执行 causal-LM LoRA 多视角 InfoNCE+KD、RQ-SID prefix 与 unique ID 混合 token、七类 instruction SFT、SID-prefix NTP、同-prefix hard-negative InfoNCE、prefix beam→子目录 item retrieval→APF。不是用最终分数规则模拟 SIGMA。使用真实 SmolLM LoRA 编码与反向，不是固定 embedding 直接代替 multi-view grounding；  generative-recommendation multi-task-sft hybrid-token semantic-grounding 搜广推 生成式召回与推理推荐 SIGMA 为什么用“短 SID 前缀加唯一物品 ID”，而不完全生成 SID 或只做全库 ANN？ 短前缀让模型先按任务指令定位语义子目录，唯一 ID 再保留物品精度并避免同码混淆。检索只在对应子目录做近邻搜索，折中完整多级解码与全库检索成本；多视角对齐让语义与行为空间更相容。APF 根据前缀置信度调节精确性和多样性，但早期前缀漏掉的目录仍可能限制候选覆盖。 示意：先生成“户外装备”子目录，再在其中选具体帐篷 ID。置信度高时集中搜索，模糊时扩展多个前缀；若第一步只选家居目录，再强的目录内 ANN 也找不到帐篷。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-1ed6d59e347fea5a">SIGMA 为什么用“短 SID 前缀加唯一物品 ID”，而不完全生成 SID 或只做全库 ANN？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asigma">SIGMA: A Semantic-Grounded Instruction-Driven Generative Multi-Task Recommender at AliExpress</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / AliExpress</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>短前缀让模型先按任务指令定位语义子目录，唯一 ID 再保留物品精度并避免同码混淆。检索只在对应子目录做近邻搜索，折中完整多级解码与全库检索成本；多视角对齐让语义与行为空间更相容。APF 根据前缀置信度调节精确性和多样性，但早期前缀漏掉的目录仍可能限制候选覆盖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先生成“户外装备”子目录，再在其中选具体帐篷 ID。置信度高时集中搜索，模糊时扩展多个前缀；若第一步只选家居目录，再强的目录内 ANN 也找不到帐篷。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.22913">原论文</a> · <a href="../../../../reproductions/2602.22913-sigma/">实现解读</a> · <a href="#qa-1ed6d59e347fea5a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sigma" data-paper-title="SIGMA: A Semantic-Grounded Instruction-Driven Generative Multi-Task Recommender at AliExpress" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="SIGMA: A Semantic-Grounded Instruction-Driven Generative Multi-Task Recommender at AliExpress 搜广推与 LLM 应用 Alibaba / AliExpress 2026-02-26 普通生成推荐只做 next-item，难以即时响应 Query、Category、Longtail、Discover、Season、Holiday 等业务任务。SIGMA 先通过搜索语义、视觉、世界知识和协同行为四类 relevance pair，把 LLM 语义与在线 ID embedding 对齐；随后用“短 SID prefix + unique item ID”同时保留生成效率和商品精度；七任务 instruction SFT 统一训练； 七任务分桶样本只有约 18/任务，逐任务数字只作诊断，不作结论。Fidelity: 完整核心链路。本地实际执行 causal-LM LoRA 多视角 InfoNCE+KD、RQ-SID prefix 与 unique ID 混合 token、七类 instruction SFT、SID-prefix NTP、同-prefix hard-negative InfoNCE、prefix beam→子目录 item retrieval→APF。不是用最终分数规则模拟 SIGMA。使用真实 SmolLM LoRA 编码与反向，不是固定 embedding 直接代替 multi-view grounding；  generative-recommendation multi-task-sft hybrid-token semantic-grounding 搜广推 生成式召回与推理推荐 多任务instruction与只做next-item怎样改变可控性？ 任务指令区分query、长尾、发现等目标，训练同模型响应不同业务要求。是否真正遵循仍需对应数据和评估，不能给提示词就假定季节知识已学会。 例如相同历史要求探索新类与继续熟悉品类，可用不同指令。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-87385cdc98e69544">多任务instruction与只做next-item怎样改变可控性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asigma">SIGMA: A Semantic-Grounded Instruction-Driven Generative Multi-Task Recommender at AliExpress</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / AliExpress</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>任务指令区分query、长尾、发现等目标，训练同模型响应不同业务要求。是否真正遵循仍需对应数据和评估，不能给提示词就假定季节知识已学会。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如相同历史要求探索新类与继续熟悉品类，可用不同指令。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.22913">原论文</a> · <a href="../../../../reproductions/2602.22913-sigma/">实现解读</a> · <a href="#qa-87385cdc98e69544">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sigma" data-paper-title="SIGMA: A Semantic-Grounded Instruction-Driven Generative Multi-Task Recommender at AliExpress" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="SIGMA: A Semantic-Grounded Instruction-Driven Generative Multi-Task Recommender at AliExpress 搜广推与 LLM 应用 Alibaba / AliExpress 2026-02-26 普通生成推荐只做 next-item，难以即时响应 Query、Category、Longtail、Discover、Season、Holiday 等业务任务。SIGMA 先通过搜索语义、视觉、世界知识和协同行为四类 relevance pair，把 LLM 语义与在线 ID embedding 对齐；随后用“短 SID prefix + unique item ID”同时保留生成效率和商品精度；七任务 instruction SFT 统一训练； 七任务分桶样本只有约 18/任务，逐任务数字只作诊断，不作结论。Fidelity: 完整核心链路。本地实际执行 causal-LM LoRA 多视角 InfoNCE+KD、RQ-SID prefix 与 unique ID 混合 token、七类 instruction SFT、SID-prefix NTP、同-prefix hard-negative InfoNCE、prefix beam→子目录 item retrieval→APF。不是用最终分数规则模拟 SIGMA。使用真实 SmolLM LoRA 编码与反向，不是固定 embedding 直接代替 multi-view grounding；  generative-recommendation multi-task-sft hybrid-token semantic-grounding 搜广推 生成式召回与推理推荐 SIGMA本地精确cosine top-k能证明生产ANN延迟吗？ 不能，缩小目录精确检索验证逻辑，不测大规模索引速度；公开任务映射与原多视角数据不同。现有结果不支持APF或线上收益，需保留范围说明。 例如几千商品逐个算相似度，与亿级ANN服务不是同一吞吐场景。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a12be252b249dff8">SIGMA本地精确cosine top-k能证明生产ANN延迟吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asigma">SIGMA: A Semantic-Grounded Instruction-Driven Generative Multi-Task Recommender at AliExpress</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / AliExpress</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，缩小目录精确检索验证逻辑，不测大规模索引速度；公开任务映射与原多视角数据不同。现有结果不支持APF或线上收益，需保留范围说明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如几千商品逐个算相似度，与亿级ANN服务不是同一吞吐场景。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.22913">原论文</a> · <a href="../../../../reproductions/2602.22913-sigma/">实现解读</a> · <a href="#qa-a12be252b249dff8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:static-constraint-decoding" data-paper-title="Vectorizing the Trie: Efficient Constrained Decoding for LLM-based Generative Retrieval on Accelerators" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Vectorizing the Trie: Efficient Constrained Decoding for LLM-based Generative Retrieval on Accelerators 搜广推与 LLM 应用 Google 2026-02-26 生成式推荐常需要将解码限制在新鲜内容、库存或地域等合法 item 子集中。STATIC 将前缀树离线压成 CSR 迁移矩阵，浅层可用 dense lookup；每步在 GPU/TPU 上抽取合法候选，消除 CPU 指针追踪和设备往返。 成本过高，不复现（审查 DONE）：完整实验需要 TPU v6e、1B 模型及生产环境；本次实现 Algorithms 1/2 的独立 PyTorch 算子：CSR 离线构建、固定最大分支宽度的向量化 speculative gather、浅层 dense lookup、log-space 掩码、beam 父状态重排和显式 EOS。使用变长 ID 时必须保留 EOS，调用方需收集已结束 beam；不提供完整语言模型。  生成式推荐 约束解码与服务效率 搜广推 生成式召回与推理推荐 STATIC为什么把合法item树压成设备内迁移索引？ 生成推荐需遵守库存地域等约束，CPU逐节点追树带来指针与设备往返。CSR和浅层dense lookup把合法token与目标node变成连续可取索引，便于加速器执行。 例如当前前缀后只允许几个码，直接从一行索引拿候选而非回CPU遍历。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-static-constraint-decoding-c02cbeaf" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e0d73a2f68dae433">STATIC为什么把合法item树压成设备内迁移索引？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Astatic-constraint-decoding">Vectorizing the Trie: Efficient Constrained Decoding for LLM-based Generative Retrieval on Accelerators</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>生成推荐需遵守库存地域等约束，CPU逐节点追树带来指针与设备往返。CSR和浅层dense lookup把合法token与目标node变成连续可取索引，便于加速器执行。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如当前前缀后只允许几个码，直接从一行索引拿候选而非回CPU遍历。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.22647">原论文</a> · <a href="../../../../recommendation-components/2602.22647-static-constraint-decoding/">实现解读</a> · <a href="#qa-e0d73a2f68dae433">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:static-constraint-decoding" data-paper-title="Vectorizing the Trie: Efficient Constrained Decoding for LLM-based Generative Retrieval on Accelerators" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Vectorizing the Trie: Efficient Constrained Decoding for LLM-based Generative Retrieval on Accelerators 搜广推与 LLM 应用 Google 2026-02-26 生成式推荐常需要将解码限制在新鲜内容、库存或地域等合法 item 子集中。STATIC 将前缀树离线压成 CSR 迁移矩阵，浅层可用 dense lookup；每步在 GPU/TPU 上抽取合法候选，消除 CPU 指针追踪和设备往返。 成本过高，不复现（审查 DONE）：完整实验需要 TPU v6e、1B 模型及生产环境；本次实现 Algorithms 1/2 的独立 PyTorch 算子：CSR 离线构建、固定最大分支宽度的向量化 speculative gather、浅层 dense lookup、log-space 掩码、beam 父状态重排和显式 EOS。使用变长 ID 时必须保留 EOS，调用方需收集已结束 beam；不提供完整语言模型。  生成式推荐 约束解码与服务效率 搜广推 生成式召回与推理推荐 STATIC 为什么先做全词表 log-softmax 再屏蔽非法 token，而不在合法集合重新归一化？ 约束只限制可走路径，不应悄悄改变模型原本的条件概率尺度。在各前缀的合法集合上重归一化，会让候选少的前缀获得人为优势，改变跨 beam 的比较。CSR 把合法转移压成设备友好数组，加速查表；选择 beam 后还必须同步重排前缀与树状态，否则约束会套到错误路径上。 示意：两个前缀分别只剩一个和十个合法后继。若各自重归一化，前者唯一后继概率变成一，可能无端击败原模型更支持的另一条路径；保持原概率再掩码可避免这种偏移。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-9de99ca7ecd033e3">STATIC 为什么先做全词表 log-softmax 再屏蔽非法 token，而不在合法集合重新归一化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Astatic-constraint-decoding">Vectorizing the Trie: Efficient Constrained Decoding for LLM-based Generative Retrieval on Accelerators</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>约束只限制可走路径，不应悄悄改变模型原本的条件概率尺度。在各前缀的合法集合上重归一化，会让候选少的前缀获得人为优势，改变跨 beam 的比较。CSR 把合法转移压成设备友好数组，加速查表；选择 beam 后还必须同步重排前缀与树状态，否则约束会套到错误路径上。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个前缀分别只剩一个和十个合法后继。若各自重归一化，前者唯一后继概率变成一，可能无端击败原模型更支持的另一条路径；保持原概率再掩码可避免这种偏移。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.22647">原论文</a> · <a href="../../../../recommendation-components/2602.22647-static-constraint-decoding/">实现解读</a> · <a href="#qa-9de99ca7ecd033e3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:static-constraint-decoding" data-paper-title="Vectorizing the Trie: Efficient Constrained Decoding for LLM-based Generative Retrieval on Accelerators" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Vectorizing the Trie: Efficient Constrained Decoding for LLM-based Generative Retrieval on Accelerators 搜广推与 LLM 应用 Google 2026-02-26 生成式推荐常需要将解码限制在新鲜内容、库存或地域等合法 item 子集中。STATIC 将前缀树离线压成 CSR 迁移矩阵，浅层可用 dense lookup；每步在 GPU/TPU 上抽取合法候选，消除 CPU 指针追踪和设备往返。 成本过高，不复现（审查 DONE）：完整实验需要 TPU v6e、1B 模型及生产环境；本次实现 Algorithms 1/2 的独立 PyTorch 算子：CSR 离线构建、固定最大分支宽度的向量化 speculative gather、浅层 dense lookup、log-space 掩码、beam 父状态重排和显式 EOS。使用变长 ID 时必须保留 EOS，调用方需收集已结束 beam；不提供完整语言模型。  生成式推荐 约束解码与服务效率 搜广推 生成式召回与推理推荐 合法集合重softmax与先全词表log-softmax再mask有什么不同？ 前者改变前缀分数尺度，使不同合法集合大小影响beam；后者保留模型原概率，只排除非法项。原方法用后者，不能视作等价数值优化。 例如某父beam合法选择少，重归一会额外抬高其子beam得分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-94874bbc3ffd8e6f">合法集合重softmax与先全词表log-softmax再mask有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Astatic-constraint-decoding">Vectorizing the Trie: Efficient Constrained Decoding for LLM-based Generative Retrieval on Accelerators</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者改变前缀分数尺度，使不同合法集合大小影响beam；后者保留模型原概率，只排除非法项。原方法用后者，不能视作等价数值优化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某父beam合法选择少，重归一会额外抬高其子beam得分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.22647">原论文</a> · <a href="../../../../recommendation-components/2602.22647-static-constraint-decoding/">实现解读</a> · <a href="#qa-94874bbc3ffd8e6f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:static-constraint-decoding" data-paper-title="Vectorizing the Trie: Efficient Constrained Decoding for LLM-based Generative Retrieval on Accelerators" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Vectorizing the Trie: Efficient Constrained Decoding for LLM-based Generative Retrieval on Accelerators 搜广推与 LLM 应用 Google 2026-02-26 生成式推荐常需要将解码限制在新鲜内容、库存或地域等合法 item 子集中。STATIC 将前缀树离线压成 CSR 迁移矩阵，浅层可用 dense lookup；每步在 GPU/TPU 上抽取合法候选，消除 CPU 指针追踪和设备往返。 成本过高，不复现（审查 DONE）：完整实验需要 TPU v6e、1B 模型及生产环境；本次实现 Algorithms 1/2 的独立 PyTorch 算子：CSR 离线构建、固定最大分支宽度的向量化 speculative gather、浅层 dense lookup、log-space 掩码、beam 父状态重排和显式 EOS。使用变长 ID 时必须保留 EOS，调用方需收集已结束 beam；不提供完整语言模型。  生成式推荐 约束解码与服务效率 搜广推 生成式召回与推理推荐 STATIC beam选完后为什么prefix和trie node必须一起重排？ 每条beam的文本与合法状态成对，选出的子beam可能来自不同父节点。只重排分数或prefix会让下一步沿错合法路径；约束树更新也需版本一致。 例如文本走到服饰码却保留食品节点，下一步mask会错误限制。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-622b5fbde0e5eba1">STATIC beam选完后为什么prefix和trie node必须一起重排？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Astatic-constraint-decoding">Vectorizing the Trie: Efficient Constrained Decoding for LLM-based Generative Retrieval on Accelerators</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每条beam的文本与合法状态成对，选出的子beam可能来自不同父节点。只重排分数或prefix会让下一步沿错合法路径；约束树更新也需版本一致。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如文本走到服饰码却保留食品节点，下一步mask会错误限制。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.22647">原论文</a> · <a href="../../../../recommendation-components/2602.22647-static-constraint-decoding/">实现解读</a> · <a href="#qa-622b5fbde0e5eba1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:climber-pilot" data-paper-title="Climber-Pilot: A Non-Myopic Generative Recommendation Model Towards Better Instruction-Following" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Climber-Pilot: A Non-Myopic Generative Recommendation Model Towards Better Instruction-Following 搜广推与 LLM 应用 NetEase Cloud Music 2026-02-14 Climber-Pilot 用时间感知多物品预测把长周期、多物品消费前瞻蒸馏进单步生成模型；条件引导稀疏注意力在 attention 内注入类目和业务约束，无需额外过滤或多步推理。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.09251，相对变化 +71.29%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-retrieval long-horizon instruction-following 搜广推 生成式召回与推理推荐 Climber-Pilot 为什么训练预测多个未来物品，却仍只需单步服务？ 多个偏移目标在训练中把长周期消费结构写入共享状态，使一次预测不只追随紧邻事件；服务使用学到的模型，不必逐步模拟完整未来。时间权重表达不同距离的贡献。未来目标属于监督，不能转成实时可见输入。 示意：训练让当前状态同时预测接下来的相机、镜头和包，服务仍直接给当前候选打分；系统没有先看到这三次真实未来行为再推荐。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-climber-pilot-a97c0a4c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-96e822a73ea4b59e">Climber-Pilot 为什么训练预测多个未来物品，却仍只需单步服务？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aclimber-pilot">Climber-Pilot: A Non-Myopic Generative Recommendation Model Towards Better Instruction-Following</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NetEase Cloud Music</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多个偏移目标在训练中把长周期消费结构写入共享状态，使一次预测不只追随紧邻事件；服务使用学到的模型，不必逐步模拟完整未来。时间权重表达不同距离的贡献。未来目标属于监督，不能转成实时可见输入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练让当前状态同时预测接下来的相机、镜头和包，服务仍直接给当前候选打分；系统没有先看到这三次真实未来行为再推荐。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.13581">原论文</a> · <a href="../../../../reproductions/2602.13581-climber-pilot/">实现解读</a> · <a href="#qa-96e822a73ea4b59e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:climber-pilot" data-paper-title="Climber-Pilot: A Non-Myopic Generative Recommendation Model Towards Better Instruction-Following" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Climber-Pilot: A Non-Myopic Generative Recommendation Model Towards Better Instruction-Following 搜广推与 LLM 应用 NetEase Cloud Music 2026-02-14 Climber-Pilot 用时间感知多物品预测把长周期、多物品消费前瞻蒸馏进单步生成模型；条件引导稀疏注意力在 attention 内注入类目和业务约束，无需额外过滤或多步推理。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.09251，相对变化 +71.29%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-retrieval long-horizon instruction-following 搜广推 生成式召回与推理推荐 Climber-Pilot怎样让单步生成考虑更远消费，而不在服务时展开整条未来轨迹？ 时间感知多物品预测在训练中要求当前状态解释多个未来目标，把长周期前瞻压进参数；服务时仍可只生成当前结果。条件引导的注意力再把类目与业务限制纳入计算，而不是额外多步推理。未来监督只能来自训练轨迹，不能在评估请求中读取真实未来物品来决定当前推荐。 示意：训练时知道某次兴趣最终延伸到相机配件，可让当前表示学习这类后续需求；真正上线只看已有历史，不能把这位用户尚未发生的购买塞进输入。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-93eb6feb5d5e3d8d">Climber-Pilot怎样让单步生成考虑更远消费，而不在服务时展开整条未来轨迹？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aclimber-pilot">Climber-Pilot: A Non-Myopic Generative Recommendation Model Towards Better Instruction-Following</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NetEase Cloud Music</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>时间感知多物品预测在训练中要求当前状态解释多个未来目标，把长周期前瞻压进参数；服务时仍可只生成当前结果。条件引导的注意力再把类目与业务限制纳入计算，而不是额外多步推理。未来监督只能来自训练轨迹，不能在评估请求中读取真实未来物品来决定当前推荐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练时知道某次兴趣最终延伸到相机配件，可让当前表示学习这类后续需求；真正上线只看已有历史，不能把这位用户尚未发生的购买塞进输入。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.13581">原论文</a> · <a href="../../../../reproductions/2602.13581-climber-pilot/">实现解读</a> · <a href="#qa-93eb6feb5d5e3d8d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:climber-pilot" data-paper-title="Climber-Pilot: A Non-Myopic Generative Recommendation Model Towards Better Instruction-Following" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Climber-Pilot: A Non-Myopic Generative Recommendation Model Towards Better Instruction-Following 搜广推与 LLM 应用 NetEase Cloud Music 2026-02-14 Climber-Pilot 用时间感知多物品预测把长周期、多物品消费前瞻蒸馏进单步生成模型；条件引导稀疏注意力在 attention 内注入类目和业务约束，无需额外过滤或多步推理。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.09251，相对变化 +71.29%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-retrieval long-horizon instruction-following 搜广推 生成式召回与推理推荐 Climber-Pilot 的条件稀疏注意力与解码后过滤，约束进入计算的阶段有何不同？ 注意力内掩码改变模型用哪些证据形成表示，后过滤只删除已生成结果，无法修复生成前漏掉的合法候选。前者使条件参与建模，仍需保证掩码与业务规则一致；它不是无需任何合法性校验的保证，也没有证明所有后处理都可移除。 示意：只允许某品类时，在内部关注相关证据有助形成候选；事后删掉全部不符商品可能剩空列表，且已花费的生成预算无法追回。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-92cad7296cf78cda">Climber-Pilot 的条件稀疏注意力与解码后过滤，约束进入计算的阶段有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aclimber-pilot">Climber-Pilot: A Non-Myopic Generative Recommendation Model Towards Better Instruction-Following</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NetEase Cloud Music</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>注意力内掩码改变模型用哪些证据形成表示，后过滤只删除已生成结果，无法修复生成前漏掉的合法候选。前者使条件参与建模，仍需保证掩码与业务规则一致；它不是无需任何合法性校验的保证，也没有证明所有后处理都可移除。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>只允许某品类时，在内部关注相关证据有助形成候选；事后删掉全部不符商品可能剩空列表，且已花费的生成预算无法追回。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.13581">原论文</a> · <a href="../../../../reproductions/2602.13581-climber-pilot/">实现解读</a> · <a href="#qa-92cad7296cf78cda">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:climber-pilot" data-paper-title="Climber-Pilot: A Non-Myopic Generative Recommendation Model Towards Better Instruction-Following" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Climber-Pilot: A Non-Myopic Generative Recommendation Model Towards Better Instruction-Following 搜广推与 LLM 应用 NetEase Cloud Music 2026-02-14 Climber-Pilot 用时间感知多物品预测把长周期、多物品消费前瞻蒸馏进单步生成模型；条件引导稀疏注意力在 attention 内注入类目和业务约束，无需额外过滤或多步推理。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.09251，相对变化 +71.29%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-retrieval long-horizon instruction-following 搜广推 生成式召回与推理推荐 TAMIP 多未来损失中的时间权重应怎样与有效目标 mask 配合？ 每个未来偏移 k 的损失需对应真实存在的目标和定义好的 wk，短序列末端不能用 padding 当正例。各偏移可共享当前历史状态，但训练输入只到截止时刻。实现还应区分时间加权监督与注意力条件 mask，二者影响不同张量。 示意：某用户只剩两个未来事件，就只计算这两项，而非为第三个空位置训练一个假商品；权重更大也不允许把该未来事件拼进历史。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c107ef20782d3df8">TAMIP 多未来损失中的时间权重应怎样与有效目标 mask 配合？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aclimber-pilot">Climber-Pilot: A Non-Myopic Generative Recommendation Model Towards Better Instruction-Following</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NetEase Cloud Music</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每个未来偏移 k 的损失需对应真实存在的目标和定义好的 wk，短序列末端不能用 padding 当正例。各偏移可共享当前历史状态，但训练输入只到截止时刻。实现还应区分时间加权监督与注意力条件 mask，二者影响不同张量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某用户只剩两个未来事件，就只计算这两项，而非为第三个空位置训练一个假商品；权重更大也不允许把该未来事件拼进历史。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.13581">原论文</a> · <a href="../../../../reproductions/2602.13581-climber-pilot/">实现解读</a> · <a href="#qa-c107ef20782d3df8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rgalign-rec" data-paper-title="RGAlign-Rec: Ranking-Guided Alignment for Latent Query Reasoning in Recommendation Systems" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="RGAlign-Rec: Ranking-Guided Alignment for Latent Query Reasoning in Recommendation Systems 搜广推与 LLM 应用 Forth AI / Shopee / Singapore University of Technology and Design 2026-02-13 先让 LLM 从上下文生成潜在 query，再用真实排序模型的 item 偏好构建正负 query，通过 RG-SFT 与 DPO 对齐 top-rank 意图。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 rgalign-rec 核心机制，相对 NDCG@10 -14.03%。  llm-recommendation query-reasoning preference-alignment 搜广推 生成式召回与推理推荐 RGAlign-Rec的潜在query是用户真的输入过的搜索词吗？ 不是。它是从用户上下文生成的语言化意图，用来连接下游物品召回与排序需求。生成得通顺并不意味着用户明确说过这些话，因而不能把query当成直接观测的用户真值。先分清真实行为与生成意图，才能理解后续排序引导监督的来源。 教学例子：用户看过几条露营内容，系统生成“轻量帐篷”作为潜在query；这不等于日志里记录了用户搜索过该词。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-rgalign-rec-56b59d1c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-bdd19e3b729ffb62">RGAlign-Rec的潜在query是用户真的输入过的搜索词吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Argalign-rec">RGAlign-Rec: Ranking-Guided Alignment for Latent Query Reasoning in Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Forth AI / Shopee / Singapore University of Technology and Design</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。它是从用户上下文生成的语言化意图，用来连接下游物品召回与排序需求。生成得通顺并不意味着用户明确说过这些话，因而不能把query当成直接观测的用户真值。先分清真实行为与生成意图，才能理解后续排序引导监督的来源。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户看过几条露营内容，系统生成“轻量帐篷”作为潜在query；这不等于日志里记录了用户搜索过该词。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12968">原论文</a> · <a href="../../../../reproductions/2602.12968-rgalign-rec/">实现解读</a> · <a href="#qa-bdd19e3b729ffb62">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rgalign-rec" data-paper-title="RGAlign-Rec: Ranking-Guided Alignment for Latent Query Reasoning in Recommendation Systems" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="RGAlign-Rec: Ranking-Guided Alignment for Latent Query Reasoning in Recommendation Systems 搜广推与 LLM 应用 Forth AI / Shopee / Singapore University of Technology and Design 2026-02-13 先让 LLM 从上下文生成潜在 query，再用真实排序模型的 item 偏好构建正负 query，通过 RG-SFT 与 DPO 对齐 top-rank 意图。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 rgalign-rec 核心机制，相对 NDCG@10 -14.03%。  llm-recommendation query-reasoning preference-alignment 搜广推 生成式召回与推理推荐 RGAlign 为什么用排序模型对物品的偏好反过来选择 query 的胜负？ 语言上流畅的潜在 query 未必能召回排序器真正看重的物品。先生成多种 query，再依据它们对应物品的排序偏好构造监督与胜负对，可把意图生成目标对齐到下游 top-rank 需求。RG-SFT 建立基本映射，DPO 强化相对偏好；它仍继承排序器的判断，不能被当成独立用户满意度标签。 示意：历史可解释为“入门摄影”或“专业镜头”。若下游对该用户更看好轻便入门相机，就优先训练前一 query，而不是仅按哪句表达更自然来选胜者。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-6398abbf95278d4e">RGAlign 为什么用排序模型对物品的偏好反过来选择 query 的胜负？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Argalign-rec">RGAlign-Rec: Ranking-Guided Alignment for Latent Query Reasoning in Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Forth AI / Shopee / Singapore University of Technology and Design</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语言上流畅的潜在 query 未必能召回排序器真正看重的物品。先生成多种 query，再依据它们对应物品的排序偏好构造监督与胜负对，可把意图生成目标对齐到下游 top-rank 需求。RG-SFT 建立基本映射，DPO 强化相对偏好；它仍继承排序器的判断，不能被当成独立用户满意度标签。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>历史可解释为“入门摄影”或“专业镜头”。若下游对该用户更看好轻便入门相机，就优先训练前一 query，而不是仅按哪句表达更自然来选胜者。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12968">原论文</a> · <a href="../../../../reproductions/2602.12968-rgalign-rec/">实现解读</a> · <a href="#qa-6398abbf95278d4e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rgalign-rec" data-paper-title="RGAlign-Rec: Ranking-Guided Alignment for Latent Query Reasoning in Recommendation Systems" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="RGAlign-Rec: Ranking-Guided Alignment for Latent Query Reasoning in Recommendation Systems 搜广推与 LLM 应用 Forth AI / Shopee / Singapore University of Technology and Design 2026-02-13 先让 LLM 从上下文生成潜在 query，再用真实排序模型的 item 偏好构建正负 query，通过 RG-SFT 与 DPO 对齐 top-rank 意图。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 rgalign-rec 核心机制，相对 NDCG@10 -14.03%。  llm-recommendation query-reasoning preference-alignment 搜广推 生成式召回与推理推荐 排序引导query对齐与普通语言SFT有什么区别？ 普通SFT学习示范文本似然，排序引导用下游物品偏好构建正负query，额外约束语言意图是否服务排序。排序器也可能带偏差，不能把其偏好当用户因果真值。 例如更华丽的query未必带来更相关候选，排名反馈可区分这点。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-18b3599a62f2f2ae">排序引导query对齐与普通语言SFT有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Argalign-rec">RGAlign-Rec: Ranking-Guided Alignment for Latent Query Reasoning in Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Forth AI / Shopee / Singapore University of Technology and Design</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>普通SFT学习示范文本似然，排序引导用下游物品偏好构建正负query，额外约束语言意图是否服务排序。排序器也可能带偏差，不能把其偏好当用户因果真值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如更华丽的query未必带来更相关候选，排名反馈可区分这点。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12968">原论文</a> · <a href="../../../../reproductions/2602.12968-rgalign-rec/">实现解读</a> · <a href="#qa-18b3599a62f2f2ae">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rgalign-rec" data-paper-title="RGAlign-Rec: Ranking-Guided Alignment for Latent Query Reasoning in Recommendation Systems" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="RGAlign-Rec: Ranking-Guided Alignment for Latent Query Reasoning in Recommendation Systems 搜广推与 LLM 应用 Forth AI / Shopee / Singapore University of Technology and Design 2026-02-13 先让 LLM 从上下文生成潜在 query，再用真实排序模型的 item 偏好构建正负 query，通过 RG-SFT 与 DPO 对齐 top-rank 意图。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 rgalign-rec 核心机制，相对 NDCG@10 -14.03%。  llm-recommendation query-reasoning preference-alignment 搜广推 生成式召回与推理推荐 本地RGAlign的query与论文生产LLM链路怎样区分？ 当前公开MovieLens固定候选协议只验证排序引导的中心计算，未复刻私有特征、生产基础模型或在线流量。正负query需同上下文与同候选评判，不能用测试标签选优。 例如离线候选分数提高，不能直接写成线上推荐转化增长。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a57676e168ae136a">本地RGAlign的query与论文生产LLM链路怎样区分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Argalign-rec">RGAlign-Rec: Ranking-Guided Alignment for Latent Query Reasoning in Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Forth AI / Shopee / Singapore University of Technology and Design</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>当前公开MovieLens固定候选协议只验证排序引导的中心计算，未复刻私有特征、生产基础模型或在线流量。正负query需同上下文与同候选评判，不能用测试标签选优。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如离线候选分数提高，不能直接写成线上推荐转化增长。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12968">原论文</a> · <a href="../../../../reproductions/2602.12968-rgalign-rec/">实现解读</a> · <a href="#qa-a57676e168ae136a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rolegen" data-paper-title="Awakening Dormant Users: Generative Recommendation with Counterfactual Functional Role Reasoning" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Awakening Dormant Users: Generative Recommendation with Counterfactual Functional Role Reasoning 搜广推与 LLM 应用 Beihang University 2026-02-13 RoleGen 让 LLM Reasoner 判断物品在转化轨迹中的功能角色，并通过反事实路径估计其工具性作用；候选再进入 SID 生成骨干，通过推理—执行—反馈—反思闭环迭代，降低休眠用户兴趣坍缩。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05605，相对变化 +3.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation counterfactual-reasoning dormant-users 搜广推 生成式召回与推理推荐 RoleGen所说的role是用户画像身份，还是物品在转化路径中的功能？ 这里是物品在转化路径中承担的功能角色，不是给用户分配职业或人口属性。LLM Reasoner对轨迹中的物品作用作判断，再将候选交给SID生成骨干与反馈循环。角色是模型推断的解释，不能直接当成已经观测到的真实因果身份。 教学例子：同一商品可以在一次路径里帮助比较，在另一次路径里成为最终购买对象；这与用户是不是“学生”无关。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-rolegen-9ce78677" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5116f7e1f78cdcad">RoleGen所说的role是用户画像身份，还是物品在转化路径中的功能？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arolegen">Awakening Dormant Users: Generative Recommendation with Counterfactual Functional Role Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这里是物品在转化路径中承担的功能角色，不是给用户分配职业或人口属性。LLM Reasoner对轨迹中的物品作用作判断，再将候选交给SID生成骨干与反馈循环。角色是模型推断的解释，不能直接当成已经观测到的真实因果身份。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一商品可以在一次路径里帮助比较，在另一次路径里成为最终购买对象；这与用户是不是“学生”无关。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.13134">原论文</a> · <a href="../../../../reproductions/2602.13134-rolegen/">实现解读</a> · <a href="#qa-5116f7e1f78cdcad">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rolegen" data-paper-title="Awakening Dormant Users: Generative Recommendation with Counterfactual Functional Role Reasoning" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Awakening Dormant Users: Generative Recommendation with Counterfactual Functional Role Reasoning 搜广推与 LLM 应用 Beihang University 2026-02-13 RoleGen 让 LLM Reasoner 判断物品在转化轨迹中的功能角色，并通过反事实路径估计其工具性作用；候选再进入 SID 生成骨干，通过推理—执行—反馈—反思闭环迭代，降低休眠用户兴趣坍缩。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05605，相对变化 +3.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation counterfactual-reasoning dormant-users 搜广推 生成式召回与推理推荐 RoleGen 为什么要识别转化路径中的功能角色，而不只按物品相似度唤醒休眠用户？ 长期无活跃时，重复旧相似物品容易把兴趣收窄。功能角色把物品理解为探索、比较或促成转化等路径环节，再用反事实路径估计其工具性贡献，反馈给 SID 生成骨干并迭代反思。这里的作用估计依赖模型与数据假设，不能仅凭观测轨迹就把分数差解释成已识别的真实因果效应。 示意：用户买相机前看过评测和摄影教程，教程虽不似相机商品，却可能是重新激活兴趣的入口。按角色理解路径可考虑这个入口，而不只继续推荐相似相机。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c0450005c9756e63">RoleGen 为什么要识别转化路径中的功能角色，而不只按物品相似度唤醒休眠用户？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arolegen">Awakening Dormant Users: Generative Recommendation with Counterfactual Functional Role Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长期无活跃时，重复旧相似物品容易把兴趣收窄。功能角色把物品理解为探索、比较或促成转化等路径环节，再用反事实路径估计其工具性贡献，反馈给 SID 生成骨干并迭代反思。这里的作用估计依赖模型与数据假设，不能仅凭观测轨迹就把分数差解释成已识别的真实因果效应。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户买相机前看过评测和摄影教程，教程虽不似相机商品，却可能是重新激活兴趣的入口。按角色理解路径可考虑这个入口，而不只继续推荐相似相机。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.13134">原论文</a> · <a href="../../../../reproductions/2602.13134-rolegen/">实现解读</a> · <a href="#qa-c0450005c9756e63">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rolegen" data-paper-title="Awakening Dormant Users: Generative Recommendation with Counterfactual Functional Role Reasoning" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Awakening Dormant Users: Generative Recommendation with Counterfactual Functional Role Reasoning 搜广推与 LLM 应用 Beihang University 2026-02-13 RoleGen 让 LLM Reasoner 判断物品在转化轨迹中的功能角色，并通过反事实路径估计其工具性作用；候选再进入 SID 生成骨干，通过推理—执行—反馈—反思闭环迭代，降低休眠用户兴趣坍缩。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05605，相对变化 +3.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation counterfactual-reasoning dormant-users 搜广推 生成式召回与推理推荐 反事实工具性作用与普通共现相似度有什么区别？ 共现只描述一起发生，工具性问题关心移除该物品路径结果怎样变。若本地仅有代理条件，不能把do记号公式当已识别真实因果效应。 例如充电器与手机共购，不自动证明推荐充电器导致手机购买。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-56695ae911654777">反事实工具性作用与普通共现相似度有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arolegen">Awakening Dormant Users: Generative Recommendation with Counterfactual Functional Role Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共现只描述一起发生，工具性问题关心移除该物品路径结果怎样变。若本地仅有代理条件，不能把do记号公式当已识别真实因果效应。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如充电器与手机共购，不自动证明推荐充电器导致手机购买。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.13134">原论文</a> · <a href="../../../../reproductions/2602.13134-rolegen/">实现解读</a> · <a href="#qa-56695ae911654777">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rolegen" data-paper-title="Awakening Dormant Users: Generative Recommendation with Counterfactual Functional Role Reasoning" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Awakening Dormant Users: Generative Recommendation with Counterfactual Functional Role Reasoning 搜广推与 LLM 应用 Beihang University 2026-02-13 RoleGen 让 LLM Reasoner 判断物品在转化轨迹中的功能角色，并通过反事实路径估计其工具性作用；候选再进入 SID 生成骨干，通过推理—执行—反馈—反思闭环迭代，降低休眠用户兴趣坍缩。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05605，相对变化 +3.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation counterfactual-reasoning dormant-users 搜广推 生成式召回与推理推荐 RoleGen本地公开数据能证明休眠用户生产转化吗？ 不能，本地MovieLens子集与代理目标只检验中心路径，缺少私有休眠日志和真实分桶。反事实分数来源、候选和反馈需留痕，不可用代理Δ冒充线上干预效果。 例如电影偏好排序变化不是电商转化因果增量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3de78a17bbd52912">RoleGen本地公开数据能证明休眠用户生产转化吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arolegen">Awakening Dormant Users: Generative Recommendation with Counterfactual Functional Role Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，本地MovieLens子集与代理目标只检验中心路径，缺少私有休眠日志和真实分桶。反事实分数来源、候选和反馈需留痕，不可用代理Δ冒充线上干预效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如电影偏好排序变化不是电商转化因果增量。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.13134">原论文</a> · <a href="../../../../reproductions/2602.13134-rolegen/">实现解读</a> · <a href="#qa-3de78a17bbd52912">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:s-grec" data-paper-title="S-GRec: Personalized Semantic-Aware Generative Recommendation with Asymmetric Advantage" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="S-GRec: Personalized Semantic-Aware Generative Recommendation with Asymmetric Advantage 搜广推与 LLM 应用 Tencent / WeChat Channels 2026-02-11 生成式推荐通常只从行为日志学习 next-item likelihood，难以理解用户为何偏好某个内容；直接把 LLM 放到在线链路又无法满足工业延迟。S-GRec 将 LLM 仅作为离线语义 judge：两阶段 Personalized Semantic Judge（PSJ）先输出可解释的方面证据，再学习每个用户的方面权重；轻量生成器线上只生成 Semantic ID，不依赖 LLM。论文的第二个问题是语义目标可能与收入目标冲突。 这是最大的数据保真度差异。Fidelity: 完整核心链路。本地实际执行 causal LLM LoRA judge、方面打分 SFT+GRPO、用户条件权重 pairwise GRPO、SID 自回归生成器、5% 稀疏 semantic sampling，以及从相同 SFT checkpoint 初始化的 Reward-Sum、Adv-Sum、A2PO。模型规模与数据规模缩小，腾讯私有人工广告标注和 eCPM 模型由公开 Office 行为与 Qwen embedding 构造的监督替代。Qwen3-4B PSJ 缩小为 SmolLM2-135M；  generative-recommendation llm-as-judge grpo a2po 搜广推 生成式召回与推理推荐 S-GRec为何让大模型judge离开在线生成主链路？ 离线语义判断提供用户方面偏好，轻量生成器只输出SID，降低在线调用大模型的延迟依赖。judge质量仍需训练数据支持，轻量上线不等于语义监督免费。 例如昂贵老师预先教哪些方面重要，实时推荐由小生成器执行。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-s-grec-c5ba1bc0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2108822c2ae03b8d">S-GRec为何让大模型judge离开在线生成主链路？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3As-grec">S-GRec: Personalized Semantic-Aware Generative Recommendation with Asymmetric Advantage</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent / WeChat Channels</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>离线语义判断提供用户方面偏好，轻量生成器只输出SID，降低在线调用大模型的延迟依赖。judge质量仍需训练数据支持，轻量上线不等于语义监督免费。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如昂贵老师预先教哪些方面重要，实时推荐由小生成器执行。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.10606">原论文</a> · <a href="../../../../reproductions/2602.10606-s-grec/">实现解读</a> · <a href="#qa-2108822c2ae03b8d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:s-grec" data-paper-title="S-GRec: Personalized Semantic-Aware Generative Recommendation with Asymmetric Advantage" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="S-GRec: Personalized Semantic-Aware Generative Recommendation with Asymmetric Advantage 搜广推与 LLM 应用 Tencent / WeChat Channels 2026-02-11 生成式推荐通常只从行为日志学习 next-item likelihood，难以理解用户为何偏好某个内容；直接把 LLM 放到在线链路又无法满足工业延迟。S-GRec 将 LLM 仅作为离线语义 judge：两阶段 Personalized Semantic Judge（PSJ）先输出可解释的方面证据，再学习每个用户的方面权重；轻量生成器线上只生成 Semantic ID，不依赖 LLM。论文的第二个问题是语义目标可能与收入目标冲突。 这是最大的数据保真度差异。Fidelity: 完整核心链路。本地实际执行 causal LLM LoRA judge、方面打分 SFT+GRPO、用户条件权重 pairwise GRPO、SID 自回归生成器、5% 稀疏 semantic sampling，以及从相同 SFT checkpoint 初始化的 Reward-Sum、Adv-Sum、A2PO。模型规模与数据规模缩小，腾讯私有人工广告标注和 eCPM 模型由公开 Office 行为与 Qwen embedding 构造的监督替代。Qwen3-4B PSJ 缩小为 SmolLM2-135M；  generative-recommendation llm-as-judge grpo a2po 搜广推 生成式召回与推理推荐 S-GRec 的 A2PO 为什么只在语义与业务 advantage 同向时加入受限语义贡献？ 语义 judge 的分数与收入反馈量纲不同，直接相加可能让语义目标压倒业务。A2PO 先在各 rollout 组内分别标准化，以业务 advantage 为锚；仅同向时引入语义项，并把有效贡献限在业务幅度内。这样语义奖励提供辅助方向而非任意改写目标，但业务和 judge 本身仍可能有偏差。 示意：候选理由听来很贴合兴趣，但业务反馈为负时，不让高语义分把它翻成强正样本；两者都支持时才适度加分，避免模型为讨好评审牺牲业务目标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-ef678d9523c7b0d4">S-GRec 的 A2PO 为什么只在语义与业务 advantage 同向时加入受限语义贡献？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3As-grec">S-GRec: Personalized Semantic-Aware Generative Recommendation with Asymmetric Advantage</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent / WeChat Channels</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语义 judge 的分数与收入反馈量纲不同，直接相加可能让语义目标压倒业务。A2PO 先在各 rollout 组内分别标准化，以业务 advantage 为锚；仅同向时引入语义项，并把有效贡献限在业务幅度内。这样语义奖励提供辅助方向而非任意改写目标，但业务和 judge 本身仍可能有偏差。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>候选理由听来很贴合兴趣，但业务反馈为负时，不让高语义分把它翻成强正样本；两者都支持时才适度加分，避免模型为讨好评审牺牲业务目标。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.10606">原论文</a> · <a href="../../../../reproductions/2602.10606-s-grec/">实现解读</a> · <a href="#qa-ef678d9523c7b0d4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:s-grec" data-paper-title="S-GRec: Personalized Semantic-Aware Generative Recommendation with Asymmetric Advantage" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="S-GRec: Personalized Semantic-Aware Generative Recommendation with Asymmetric Advantage 搜广推与 LLM 应用 Tencent / WeChat Channels 2026-02-11 生成式推荐通常只从行为日志学习 next-item likelihood，难以理解用户为何偏好某个内容；直接把 LLM 放到在线链路又无法满足工业延迟。S-GRec 将 LLM 仅作为离线语义 judge：两阶段 Personalized Semantic Judge（PSJ）先输出可解释的方面证据，再学习每个用户的方面权重；轻量生成器线上只生成 Semantic ID，不依赖 LLM。论文的第二个问题是语义目标可能与收入目标冲突。 这是最大的数据保真度差异。Fidelity: 完整核心链路。本地实际执行 causal LLM LoRA judge、方面打分 SFT+GRPO、用户条件权重 pairwise GRPO、SID 自回归生成器、5% 稀疏 semantic sampling，以及从相同 SFT checkpoint 初始化的 Reward-Sum、Adv-Sum、A2PO。模型规模与数据规模缩小，腾讯私有人工广告标注和 eCPM 模型由公开 Office 行为与 Qwen embedding 构造的监督替代。Qwen3-4B PSJ 缩小为 SmolLM2-135M；  generative-recommendation llm-as-judge grpo a2po 搜广推 生成式召回与推理推荐 S-GRec的用户条件方面权重，与给所有用户固定一组语义权重有什么区别？ PSJ先给出多个方面分数，再由用户条件aggregator输出非负、归一的权重。固定权重对所有用户表达同一取舍，条件权重则允许相同内容因用户不同而得到不同语义总分。它仍依赖方面判断可靠，个性化权重本身不是真实满意度证明。 教学例子：两位用户面对同一内容，一位更重历史画像，一位更重探索新意；方面分可相同，聚合结果却不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-8b5a787178e7a276">S-GRec的用户条件方面权重，与给所有用户固定一组语义权重有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3As-grec">S-GRec: Personalized Semantic-Aware Generative Recommendation with Asymmetric Advantage</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent / WeChat Channels</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>PSJ先给出多个方面分数，再由用户条件aggregator输出非负、归一的权重。固定权重对所有用户表达同一取舍，条件权重则允许相同内容因用户不同而得到不同语义总分。它仍依赖方面判断可靠，个性化权重本身不是真实满意度证明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两位用户面对同一内容，一位更重历史画像，一位更重探索新意；方面分可相同，聚合结果却不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.10606">原论文</a> · <a href="../../../../reproductions/2602.10606-s-grec/">实现解读</a> · <a href="#qa-8b5a787178e7a276">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:s-grec" data-paper-title="S-GRec: Personalized Semantic-Aware Generative Recommendation with Asymmetric Advantage" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="S-GRec: Personalized Semantic-Aware Generative Recommendation with Asymmetric Advantage 搜广推与 LLM 应用 Tencent / WeChat Channels 2026-02-11 生成式推荐通常只从行为日志学习 next-item likelihood，难以理解用户为何偏好某个内容；直接把 LLM 放到在线链路又无法满足工业延迟。S-GRec 将 LLM 仅作为离线语义 judge：两阶段 Personalized Semantic Judge（PSJ）先输出可解释的方面证据，再学习每个用户的方面权重；轻量生成器线上只生成 Semantic ID，不依赖 LLM。论文的第二个问题是语义目标可能与收入目标冲突。 这是最大的数据保真度差异。Fidelity: 完整核心链路。本地实际执行 causal LLM LoRA judge、方面打分 SFT+GRPO、用户条件权重 pairwise GRPO、SID 自回归生成器、5% 稀疏 semantic sampling，以及从相同 SFT checkpoint 初始化的 Reward-Sum、Adv-Sum、A2PO。模型规模与数据规模缩小，腾讯私有人工广告标注和 eCPM 模型由公开 Office 行为与 Qwen embedding 构造的监督替代。Qwen3-4B PSJ 缩小为 SmolLM2-135M；  generative-recommendation llm-as-judge grpo a2po 搜广推 生成式召回与推理推荐 S-GRec本地business reward是否是真实eCPM？ 不是，公共数据无货币信号，用允许的next-item ranking proxy；原两阶段judge、生成和策略路径有缩小执行，但标签与模型规模不同。不能把公共代理分称广告收入。 例如命中下一部电影，只能代表该协议的行为偏好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1e67157c01accb0b">S-GRec本地business reward是否是真实eCPM？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3As-grec">S-GRec: Personalized Semantic-Aware Generative Recommendation with Asymmetric Advantage</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent / WeChat Channels</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是，公共数据无货币信号，用允许的next-item ranking proxy；原两阶段judge、生成和策略路径有缩小执行，但标签与模型规模不同。不能把公共代理分称广告收入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如命中下一部电影，只能代表该协议的行为偏好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.10606">原论文</a> · <a href="../../../../reproductions/2602.10606-s-grec/">实现解读</a> · <a href="#qa-1e67157c01accb0b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:diffureason" data-paper-title="DiffuReason: Bridging Latent Reasoning and Generative Refinement for Sequential Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="DiffuReason: Bridging Latent Reasoning and Generative Refinement for Sequential Recommendation 搜广推与 LLM 应用 Tencent 2026-02-10 Thinking Tokens 形成连续潜在意图，扩散去噪逐步修正冲突兴趣，GRPO 再把连续生成与离散排序奖励端到端对齐。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 diffureason 核心机制，相对 NDCG@10 -6.50%。  generative-recommendation diffusion reinforcement-learning 搜广推 生成式召回与推理推荐 DiffuReason 的连续 Thinking Tokens 为什么适合做逐步去噪，而非直接输出长语言推理？ 连续潜变量可承载多个兴趣线索，去噪步骤反复结合历史修正状态，避免每一步都解码自然语言。它提供可优化的内部表示，离散排序奖励再通过策略训练对齐。潜在 token 不自动具有可读推理含义，多步修正也不保证解决真实冲突。 示意：用户既想尝新又受预算限制，内部向量可逐步调整这两种方向；没有输出一段文字，不代表模型已经证明了每个取舍步骤。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-diffureason-5f379d3c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a862bbd127f5ec07">DiffuReason 的连续 Thinking Tokens 为什么适合做逐步去噪，而非直接输出长语言推理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adiffureason">DiffuReason: Bridging Latent Reasoning and Generative Refinement for Sequential Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>连续潜变量可承载多个兴趣线索，去噪步骤反复结合历史修正状态，避免每一步都解码自然语言。它提供可优化的内部表示，离散排序奖励再通过策略训练对齐。潜在 token 不自动具有可读推理含义，多步修正也不保证解决真实冲突。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户既想尝新又受预算限制，内部向量可逐步调整这两种方向；没有输出一段文字，不代表模型已经证明了每个取舍步骤。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.09744">原论文</a> · <a href="../../../../reproductions/2602.09744-diffureason/">实现解读</a> · <a href="#qa-a862bbd127f5ec07">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:diffureason" data-paper-title="DiffuReason: Bridging Latent Reasoning and Generative Refinement for Sequential Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="DiffuReason: Bridging Latent Reasoning and Generative Refinement for Sequential Recommendation 搜广推与 LLM 应用 Tencent 2026-02-10 Thinking Tokens 形成连续潜在意图，扩散去噪逐步修正冲突兴趣，GRPO 再把连续生成与离散排序奖励端到端对齐。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 diffureason 核心机制，相对 NDCG@10 -6.50%。  generative-recommendation diffusion reinforcement-learning 搜广推 生成式召回与推理推荐 DiffuReason为什么在潜在意图上做多步扩散修正，而不是一次生成最终推荐表示？ 一次预测可能将多个冲突兴趣压成不稳定方向，潜在Thinking Tokens先承载意图，再由逐步去噪反复修正表示，使不同线索有机会重新协调。GRPO随后用离散排序反馈对齐连续生成路径。多步过程增加计算且可能累积模型偏差，本地代理不能单独证明完整潜在推理能力。 示意：用户既搜健身器材又看甜品视频，一次融合可能摇摆；去噪过程可逐步形成更适合当前请求的意图，但不能把中间向量自动解释为真实的人类思考。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-fc1bd647de874fa4">DiffuReason为什么在潜在意图上做多步扩散修正，而不是一次生成最终推荐表示？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adiffureason">DiffuReason: Bridging Latent Reasoning and Generative Refinement for Sequential Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一次预测可能将多个冲突兴趣压成不稳定方向，潜在Thinking Tokens先承载意图，再由逐步去噪反复修正表示，使不同线索有机会重新协调。GRPO随后用离散排序反馈对齐连续生成路径。多步过程增加计算且可能累积模型偏差，本地代理不能单独证明完整潜在推理能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户既搜健身器材又看甜品视频，一次融合可能摇摆；去噪过程可逐步形成更适合当前请求的意图，但不能把中间向量自动解释为真实的人类思考。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.09744">原论文</a> · <a href="../../../../reproductions/2602.09744-diffureason/">实现解读</a> · <a href="#qa-fc1bd647de874fa4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:diffureason" data-paper-title="DiffuReason: Bridging Latent Reasoning and Generative Refinement for Sequential Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="DiffuReason: Bridging Latent Reasoning and Generative Refinement for Sequential Recommendation 搜广推与 LLM 应用 Tencent 2026-02-10 Thinking Tokens 形成连续潜在意图，扩散去噪逐步修正冲突兴趣，GRPO 再把连续生成与离散排序奖励端到端对齐。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 diffureason 核心机制，相对 NDCG@10 -6.50%。  generative-recommendation diffusion reinforcement-learning 搜广推 生成式召回与推理推荐 DiffuReason 与一次性用户向量预测相比，多步更新的收益假设和服务代价是什么？ 一次预测把全部条件压进单步映射，多步去噪允许在中间状态重新利用历史逐渐修正，但增加迭代计算和采样不确定性。若每步只重复同一偏置，更多步未必更好。来源的公开代理与真实扩散策略训练应区分，不能由最终分数声称全部链路被验证。 示意：第一步偏向热门电影，后续若看到用户小众偏好可回调；但若条件根本未包含这条偏好，再去噪十步也不会凭空获得证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ab604647335a9b32">DiffuReason 与一次性用户向量预测相比，多步更新的收益假设和服务代价是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adiffureason">DiffuReason: Bridging Latent Reasoning and Generative Refinement for Sequential Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一次预测把全部条件压进单步映射，多步去噪允许在中间状态重新利用历史逐渐修正，但增加迭代计算和采样不确定性。若每步只重复同一偏置，更多步未必更好。来源的公开代理与真实扩散策略训练应区分，不能由最终分数声称全部链路被验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第一步偏向热门电影，后续若看到用户小众偏好可回调；但若条件根本未包含这条偏好，再去噪十步也不会凭空获得证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.09744">原论文</a> · <a href="../../../../reproductions/2602.09744-diffureason/">实现解读</a> · <a href="#qa-ab604647335a9b32">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:diffureason" data-paper-title="DiffuReason: Bridging Latent Reasoning and Generative Refinement for Sequential Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="DiffuReason: Bridging Latent Reasoning and Generative Refinement for Sequential Recommendation 搜广推与 LLM 应用 Tencent 2026-02-10 Thinking Tokens 形成连续潜在意图，扩散去噪逐步修正冲突兴趣，GRPO 再把连续生成与离散排序奖励端到端对齐。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 diffureason 核心机制，相对 NDCG@10 -6.50%。  generative-recommendation diffusion reinforcement-learning 搜广推 生成式召回与推理推荐 DiffuReason 实现噪声过程与 GRPO 时，为什么不能只对最终分数加一个固定奖励项？ 去噪应有明确时间步、状态转移与随机项，策略更新则需要同上下文 rollout、奖励和对应概率口径。固定分数相加没有训练连续生成分布，也无法核验梯度路径。来源本地代理结果只按其实际范围解释，不能代替扩散与离散奖励端到端训练证据。 示意：给热门度乘零点一只改排序规则，不会教去噪器如何移动潜在 token；要声称策略训练，必须看到采样轨迹及真实参数更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-9a5e8953cc6bda38">DiffuReason 实现噪声过程与 GRPO 时，为什么不能只对最终分数加一个固定奖励项？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adiffureason">DiffuReason: Bridging Latent Reasoning and Generative Refinement for Sequential Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>去噪应有明确时间步、状态转移与随机项，策略更新则需要同上下文 rollout、奖励和对应概率口径。固定分数相加没有训练连续生成分布，也无法核验梯度路径。来源本地代理结果只按其实际范围解释，不能代替扩散与离散奖励端到端训练证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>给热门度乘零点一只改排序规则，不会教去噪器如何移动潜在 token；要声称策略训练，必须看到采样轨迹及真实参数更新。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.09744">原论文</a> · <a href="../../../../reproductions/2602.09744-diffureason/">实现解读</a> · <a href="#qa-9a5e8953cc6bda38">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rag-qac" data-paper-title="Unifying Ranking and Generation in Query Auto-Completion via Retrieval-Augmented Generation and Multi-Objective Alignment" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Unifying Ranking and Generation in Query Auto-Completion via Retrieval-Augmented Generation and Multi-Objective Alignment 搜广推与 LLM 应用 Apple 2026-02-01 先从可搜索目录检索补全证据，再以 SFT 和 DPO 同时对齐相关性、安全、参与度、目录/上下文 groundedness 与多样性。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 rag-qac 核心机制，相对 NDCG@10 -4.48%。  query-auto-completion retrieval-augmented-generation preference-alignment 搜广推 生成式召回与推理推荐 RAG-QAC 的“目录 groundedness”和“上下文 groundedness”为什么要分别判断？ 目录依据要求建议能落到实际可搜索内容，上下文依据要求它与用户前缀和已知需求一致。存在的商品也可能偏题，贴题表达也可能目录没有。二者是不同必要检查，不能以其中一项通过代替另一项，更不能从中直接推出安全和参与度达标。 示意：用户搜儿童雨鞋，目录里确有成人登山鞋，目录检查通过但上下文不符；编造一个完美儿童型号则相反，不能只看是否听起来合需求。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-rag-qac-5e006d24" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-09bb8a1517beab22">RAG-QAC 的“目录 groundedness”和“上下文 groundedness”为什么要分别判断？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arag-qac">Unifying Ranking and Generation in Query Auto-Completion via Retrieval-Augmented Generation and Multi-Objective Alignment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Apple</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目录依据要求建议能落到实际可搜索内容，上下文依据要求它与用户前缀和已知需求一致。存在的商品也可能偏题，贴题表达也可能目录没有。二者是不同必要检查，不能以其中一项通过代替另一项，更不能从中直接推出安全和参与度达标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户搜儿童雨鞋，目录里确有成人登山鞋，目录检查通过但上下文不符；编造一个完美儿童型号则相反，不能只看是否听起来合需求。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.01023">原论文</a> · <a href="../../../../reproductions/2602.01023-rag-qac/">实现解读</a> · <a href="#qa-09bb8a1517beab22">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rag-qac" data-paper-title="Unifying Ranking and Generation in Query Auto-Completion via Retrieval-Augmented Generation and Multi-Objective Alignment" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Unifying Ranking and Generation in Query Auto-Completion via Retrieval-Augmented Generation and Multi-Objective Alignment 搜广推与 LLM 应用 Apple 2026-02-01 先从可搜索目录检索补全证据，再以 SFT 和 DPO 同时对齐相关性、安全、参与度、目录/上下文 groundedness 与多样性。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 rag-qac 核心机制，相对 NDCG@10 -4.48%。  query-auto-completion retrieval-augmented-generation preference-alignment 搜广推 生成式召回与推理推荐 RAG-QAC 为什么先检索可搜索目录，再对补全建议做多目标偏好对齐？ 自由生成的查询补全可能语言合理却找不到商品或文档。目录检索先提供可追溯候选与证据，使建议有机会落到可服务对象；SFT 与 DPO 再联合权衡相关性、安全、参与度、上下文依据和多样性。多目标对齐不能弥补目录里本就不存在的内容，也需避免为参与度牺牲真实性。 示意：用户输入“轻便露营”，先从目录取得帐篷、炊具等真实类别再补全，避免生成商店根本没有的型号；两个都能搜到的补全再比较相关性与多样性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-d935bc68ea027e7f">RAG-QAC 为什么先检索可搜索目录，再对补全建议做多目标偏好对齐？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arag-qac">Unifying Ranking and Generation in Query Auto-Completion via Retrieval-Augmented Generation and Multi-Objective Alignment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Apple</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>自由生成的查询补全可能语言合理却找不到商品或文档。目录检索先提供可追溯候选与证据，使建议有机会落到可服务对象；SFT 与 DPO 再联合权衡相关性、安全、参与度、上下文依据和多样性。多目标对齐不能弥补目录里本就不存在的内容，也需避免为参与度牺牲真实性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户输入“轻便露营”，先从目录取得帐篷、炊具等真实类别再补全，避免生成商店根本没有的型号；两个都能搜到的补全再比较相关性与多样性。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.01023">原论文</a> · <a href="../../../../reproductions/2602.01023-rag-qac/">实现解读</a> · <a href="#qa-d935bc68ea027e7f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rag-qac" data-paper-title="Unifying Ranking and Generation in Query Auto-Completion via Retrieval-Augmented Generation and Multi-Objective Alignment" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Unifying Ranking and Generation in Query Auto-Completion via Retrieval-Augmented Generation and Multi-Objective Alignment 搜广推与 LLM 应用 Apple 2026-02-01 先从可搜索目录检索补全证据，再以 SFT 和 DPO 同时对齐相关性、安全、参与度、目录/上下文 groundedness 与多样性。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 rag-qac 核心机制，相对 NDCG@10 -4.48%。  query-auto-completion retrieval-augmented-generation preference-alignment 搜广推 生成式召回与推理推荐 RAG-QAC 的 SFT 与 DPO 对齐，相比一个只做检索模板的系统多了什么？ 模板可保证部分词项落地但表达和取舍固定，SFT 学习上下文生成，DPO 比较相关、安全、参与与多样性偏好。偏好奖励可能冲突，不应只追点击而丢真实性。来源本地固定 scorer 代理无法证明完整语言后训练效果。 示意：两条都能搜到的补全，一条更贴用户、另一条覆盖新方向，偏好对可以教取舍；模板一般只按规则顺序返回，缺少这种学习。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7a913fd0cd8f5c0d">RAG-QAC 的 SFT 与 DPO 对齐，相比一个只做检索模板的系统多了什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arag-qac">Unifying Ranking and Generation in Query Auto-Completion via Retrieval-Augmented Generation and Multi-Objective Alignment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Apple</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>模板可保证部分词项落地但表达和取舍固定，SFT 学习上下文生成，DPO 比较相关、安全、参与与多样性偏好。偏好奖励可能冲突，不应只追点击而丢真实性。来源本地固定 scorer 代理无法证明完整语言后训练效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两条都能搜到的补全，一条更贴用户、另一条覆盖新方向，偏好对可以教取舍；模板一般只按规则顺序返回，缺少这种学习。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.01023">原论文</a> · <a href="../../../../reproductions/2602.01023-rag-qac/">实现解读</a> · <a href="#qa-7a913fd0cd8f5c0d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rag-qac" data-paper-title="Unifying Ranking and Generation in Query Auto-Completion via Retrieval-Augmented Generation and Multi-Objective Alignment" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Unifying Ranking and Generation in Query Auto-Completion via Retrieval-Augmented Generation and Multi-Objective Alignment 搜广推与 LLM 应用 Apple 2026-02-01 先从可搜索目录检索补全证据，再以 SFT 和 DPO 同时对齐相关性、安全、参与度、目录/上下文 groundedness 与多样性。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 rag-qac 核心机制，相对 NDCG@10 -4.48%。  query-auto-completion retrieval-augmented-generation preference-alignment 搜广推 生成式召回与推理推荐 RAG-QAC 的检索证据与 gold 补全标签，为什么不能在输入中混成一份？ 证据应由请求与目录检索得到，gold 仅作为训练监督；若测试先取正确补全再检索证据，会绕过生成难点。目录、上下文 groundedness 也需独立 mask 和评判，不能把“在目录”当全部质量通过。 示意：测试答案是某帐篷型号，先把它插进证据再让模型复述，会虚高；合法链路应从用户前缀检索，再检查是否生成正确且有据的建议。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-5e959d9917f8d09a">RAG-QAC 的检索证据与 gold 补全标签，为什么不能在输入中混成一份？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arag-qac">Unifying Ranking and Generation in Query Auto-Completion via Retrieval-Augmented Generation and Multi-Objective Alignment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Apple</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>证据应由请求与目录检索得到，gold 仅作为训练监督；若测试先取正确补全再检索证据，会绕过生成难点。目录、上下文 groundedness 也需独立 mask 和评判，不能把“在目录”当全部质量通过。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>测试答案是某帐篷型号，先把它插进证据再让模型复述，会虚高；合法链路应从用户前缀检索，再检查是否生成正确且有据的建议。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.01023">原论文</a> · <a href="../../../../reproductions/2602.01023-rag-qac/">实现解读</a> · <a href="#qa-5e959d9917f8d09a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onemall" data-paper-title="OneMall: One Model, More Scenarios -- End-to-End Generative Recommender Family at Kuaishou E-Commerce" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneMall: One Model, More Scenarios -- End-to-End Generative Recommender Family at Kuaishou E-Commerce 搜广推与 LLM 应用 Kuaishou 2026-01-29 快手电商的商品卡、短视频和直播分发原本由不同链路维护。OneMall 用统一商品 Semantic ID、Query-Former 压缩、多行为 cross-attention、Sparse MoE 生成器及 RL 对齐，把多个场景收进一个生成推荐家族。 Fidelity: 核心机制复现。执行场景 prompt、三层 Semantic ID 和跨行为融合；缩小数据与模型规模。MovieLens genre 仅代理场景；未复刻快手私有商品特征、Sparse MoE、生产 RL 和线上 serving。本地对照口径：基线是共享 transition/content ensemble；实验组只增加场景 prompt、三层 residual SID 和跨行为融合，MovieLens-100K NDCG@10 0.03540→0.03693，相对 +4.33%，Hit@10 相对 -4.35%。  generative-recommendation multi-scenario semantic-id 搜广推 生成式召回与推理推荐 OneMall 的统一商品码为什么有助跨商品卡、短视频与直播？ 同一商品在多入口可共享输出身份，减少每个系统独立建模与映射的割裂，再由场景条件和多行为信息区分消费语境。统一码不表示曝光目标相同，内容、交易和直播停留仍有不同监督，跨场景迁移也可能冲突。 示意：同一夹克在视频介绍和商品卡点击都指向同一商品码，但视频完播和下单不是一个标签，不能把两者直接合并为同强度正反馈。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-onemall-15aa9dcd" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-3318c79302b636b6">OneMall 的统一商品码为什么有助跨商品卡、短视频与直播？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonemall">OneMall: One Model, More Scenarios -- End-to-End Generative Recommender Family at Kuaishou E-Commerce</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一商品在多入口可共享输出身份，减少每个系统独立建模与映射的割裂，再由场景条件和多行为信息区分消费语境。统一码不表示曝光目标相同，内容、交易和直播停留仍有不同监督，跨场景迁移也可能冲突。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一夹克在视频介绍和商品卡点击都指向同一商品码，但视频完播和下单不是一个标签，不能把两者直接合并为同强度正反馈。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.21770">原论文</a> · <a href="../../../../reproductions/2601.21770-onemall/">实现解读</a> · <a href="#qa-3318c79302b636b6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onemall" data-paper-title="OneMall: One Model, More Scenarios -- End-to-End Generative Recommender Family at Kuaishou E-Commerce" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneMall: One Model, More Scenarios -- End-to-End Generative Recommender Family at Kuaishou E-Commerce 搜广推与 LLM 应用 Kuaishou 2026-01-29 快手电商的商品卡、短视频和直播分发原本由不同链路维护。OneMall 用统一商品 Semantic ID、Query-Former 压缩、多行为 cross-attention、Sparse MoE 生成器及 RL 对齐，把多个场景收进一个生成推荐家族。 Fidelity: 核心机制复现。执行场景 prompt、三层 Semantic ID 和跨行为融合；缩小数据与模型规模。MovieLens genre 仅代理场景；未复刻快手私有商品特征、Sparse MoE、生产 RL 和线上 serving。本地对照口径：基线是共享 transition/content ensemble；实验组只增加场景 prompt、三层 residual SID 和跨行为融合，MovieLens-100K NDCG@10 0.03540→0.03693，相对 +4.33%，Hit@10 相对 -4.35%。  generative-recommendation multi-scenario semantic-id 搜广推 生成式召回与推理推荐 OneMall 用统一 Semantic ID 之后，为什么还要场景条件和多行为 cross-attention？ 统一编码只让商品在多个场景使用同一套输出词表，不能消除商品卡、短视频与直播的行为差异。场景条件告诉生成器当前目标，多行为交互再提取与该目标相关的历史信息；Query-Former 压缩和稀疏专家控制上下文与容量成本。因此统一的是模型家族和表示接口，场景特性仍需显式建模。 示意：同一件夹克在商品卡里对应点击，在直播里可能对应停留与下单。共用商品编码后，模型仍需知道当前是直播推荐，才能从用户多种行为中选择相关信号。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-361175a32963e5b8">OneMall 用统一 Semantic ID 之后，为什么还要场景条件和多行为 cross-attention？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonemall">OneMall: One Model, More Scenarios -- End-to-End Generative Recommender Family at Kuaishou E-Commerce</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>统一编码只让商品在多个场景使用同一套输出词表，不能消除商品卡、短视频与直播的行为差异。场景条件告诉生成器当前目标，多行为交互再提取与该目标相关的历史信息；Query-Former 压缩和稀疏专家控制上下文与容量成本。因此统一的是模型家族和表示接口，场景特性仍需显式建模。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一件夹克在商品卡里对应点击，在直播里可能对应停留与下单。共用商品编码后，模型仍需知道当前是直播推荐，才能从用户多种行为中选择相关信号。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.21770">原论文</a> · <a href="../../../../reproductions/2601.21770-onemall/">实现解读</a> · <a href="#qa-361175a32963e5b8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onemall" data-paper-title="OneMall: One Model, More Scenarios -- End-to-End Generative Recommender Family at Kuaishou E-Commerce" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneMall: One Model, More Scenarios -- End-to-End Generative Recommender Family at Kuaishou E-Commerce 搜广推与 LLM 应用 Kuaishou 2026-01-29 快手电商的商品卡、短视频和直播分发原本由不同链路维护。OneMall 用统一商品 Semantic ID、Query-Former 压缩、多行为 cross-attention、Sparse MoE 生成器及 RL 对齐，把多个场景收进一个生成推荐家族。 Fidelity: 核心机制复现。执行场景 prompt、三层 Semantic ID 和跨行为融合；缩小数据与模型规模。MovieLens genre 仅代理场景；未复刻快手私有商品特征、Sparse MoE、生产 RL 和线上 serving。本地对照口径：基线是共享 transition/content ensemble；实验组只增加场景 prompt、三层 residual SID 和跨行为融合，MovieLens-100K NDCG@10 0.03540→0.03693，相对 +4.33%，Hit@10 相对 -4.35%。  generative-recommendation multi-scenario semantic-id 搜广推 生成式召回与推理推荐 OneMall 的 Sparse MoE 与单一 dense 生成器，相比容量和场景分工如何变化？ 专家增加条件容量、部分激活控制每次计算，可让多场景有不同组合；dense 全共享更简单但可能被高频场景主导。专家也可能饥饿或重复，不能由参数总量断言有效容量。来源本地仅部分 SID 与场景融合，不等于完整生产 MoE/RL。 示意：直播交易和短视频兴趣可使用不同专家比例，但若 gate 永远只选同一专家，模型仍没真正分工，剩余参数也不会自动贡献。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5ad465e7480d6c89">OneMall 的 Sparse MoE 与单一 dense 生成器，相比容量和场景分工如何变化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonemall">OneMall: One Model, More Scenarios -- End-to-End Generative Recommender Family at Kuaishou E-Commerce</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>专家增加条件容量、部分激活控制每次计算，可让多场景有不同组合；dense 全共享更简单但可能被高频场景主导。专家也可能饥饿或重复，不能由参数总量断言有效容量。来源本地仅部分 SID 与场景融合，不等于完整生产 MoE/RL。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>直播交易和短视频兴趣可使用不同专家比例，但若 gate 永远只选同一专家，模型仍没真正分工，剩余参数也不会自动贡献。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.21770">原论文</a> · <a href="../../../../reproductions/2601.21770-onemall/">实现解读</a> · <a href="#qa-5ad465e7480d6c89">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onemall" data-paper-title="OneMall: One Model, More Scenarios -- End-to-End Generative Recommender Family at Kuaishou E-Commerce" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneMall: One Model, More Scenarios -- End-to-End Generative Recommender Family at Kuaishou E-Commerce 搜广推与 LLM 应用 Kuaishou 2026-01-29 快手电商的商品卡、短视频和直播分发原本由不同链路维护。OneMall 用统一商品 Semantic ID、Query-Former 压缩、多行为 cross-attention、Sparse MoE 生成器及 RL 对齐，把多个场景收进一个生成推荐家族。 Fidelity: 核心机制复现。执行场景 prompt、三层 Semantic ID 和跨行为融合；缩小数据与模型规模。MovieLens genre 仅代理场景；未复刻快手私有商品特征、Sparse MoE、生产 RL 和线上 serving。本地对照口径：基线是共享 transition/content ensemble；实验组只增加场景 prompt、三层 residual SID 和跨行为融合，MovieLens-100K NDCG@10 0.03540→0.03693，相对 +4.33%，Hit@10 相对 -4.35%。  generative-recommendation multi-scenario semantic-id 搜广推 生成式召回与推理推荐 OneMall 本地增加三层 SID 与场景 prompt，为什么不能证明 Query-Former、MoE 和 RL 都已复现？ 来源明确只加场景条件、残差码与跨行为融合，训练和服务范围应按实际算子说明。要扩展声明需看到查询压缩、真实路由和策略更新等证据。NDCG 小升且 Hit 降，不能用原文端到端家族描述覆盖本地有限模块。 示意：一个代码路径输出三枚商品码，并不自动拥有专家路由；若没有 rollout 与参数更新记录，也不能因损失写了 reward 名称就称 RL 完成。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-aaf4db271080494e">OneMall 本地增加三层 SID 与场景 prompt，为什么不能证明 Query-Former、MoE 和 RL 都已复现？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonemall">OneMall: One Model, More Scenarios -- End-to-End Generative Recommender Family at Kuaishou E-Commerce</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>来源明确只加场景条件、残差码与跨行为融合，训练和服务范围应按实际算子说明。要扩展声明需看到查询压缩、真实路由和策略更新等证据。NDCG 小升且 Hit 降，不能用原文端到端家族描述覆盖本地有限模块。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个代码路径输出三枚商品码，并不自动拥有专家路由；若没有 rollout 与参数更新记录，也不能因损失写了 reward 名称就称 RL 完成。</p>
<p class="ar-learning-sources">依据：本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.21770">原论文</a> · <a href="../../../../reproductions/2601.21770-onemall/">实现解读</a> · <a href="#qa-aaf4db271080494e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:s2gr" data-paper-title="S2GR: Stepwise Semantic-Guided Reasoning in Latent Space for Generative Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="S2GR: Stepwise Semantic-Guided Reasoning in Latent Space for Generative Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-01-26 在每一级 SID 生成前插入可解释 thinking token，并让它与真实 codebook 分布对比学习；协同共现图和负载均衡共同改善由粗到细的语义层级。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05463，相对变化 +1.15%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation latent-reasoning semantic-id 搜广推 生成式召回与推理推荐 S2GR的thinking token是自由生成的一大段自然语言思维链吗？ 这里的关键是每级SID前插入的中间状态，并把它与相应码本分布对齐；不能仅凭thinking这个名字就当成完整自然语言解释。SID仍是逐级生成的离散路径，理解这个输出结构比先把它类比聊天模型长思维链更直接。 教学例子：先出现本级中间状态，再选择本级语义码，然后进入下一级；这不要求先输出一篇可读的推理长文。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-s2gr-c72e2aca" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-870e580deebf4aef">S2GR的thinking token是自由生成的一大段自然语言思维链吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3As2gr">S2GR: Stepwise Semantic-Guided Reasoning in Latent Space for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这里的关键是每级SID前插入的中间状态，并把它与相应码本分布对齐；不能仅凭thinking这个名字就当成完整自然语言解释。SID仍是逐级生成的离散路径，理解这个输出结构比先把它类比聊天模型长思维链更直接。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先出现本级中间状态，再选择本级语义码，然后进入下一级；这不要求先输出一篇可读的推理长文。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.18664">原论文</a> · <a href="../../../../reproductions/2601.18664-s2gr/">实现解读</a> · <a href="#qa-870e580deebf4aef">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:s2gr" data-paper-title="S2GR: Stepwise Semantic-Guided Reasoning in Latent Space for Generative Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="S2GR: Stepwise Semantic-Guided Reasoning in Latent Space for Generative Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-01-26 在每一级 SID 生成前插入可解释 thinking token，并让它与真实 codebook 分布对比学习；协同共现图和负载均衡共同改善由粗到细的语义层级。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05463，相对变化 +1.15%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation latent-reasoning semantic-id 搜广推 生成式召回与推理推荐 S2GR 为什么在每一级 SID 前插入 thinking token，并把它与 codebook 分布对齐？ 粗到细 SID 的早期选择会限定后续路径，单独最大化码概率可能缺少明确的语义过渡。逐级 thinking token 提供中间状态，再用与真实码本分布的对比监督把它连接到合法语义空间，协同图与负载均衡补充行为关系和码使用。中间 token 可辅助解释，但不能仅凭名字就证明它进行了忠实的自然语言推理。 示意：先确定户外大类，再细分露营装备。每级中间状态都需贴近对应码本语义，避免出现解释像在谈露营，实际却跳到无关家居编码的脱节。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-833b7b1f56656208">S2GR 为什么在每一级 SID 前插入 thinking token，并把它与 codebook 分布对齐？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3As2gr">S2GR: Stepwise Semantic-Guided Reasoning in Latent Space for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>粗到细 SID 的早期选择会限定后续路径，单独最大化码概率可能缺少明确的语义过渡。逐级 thinking token 提供中间状态，再用与真实码本分布的对比监督把它连接到合法语义空间，协同图与负载均衡补充行为关系和码使用。中间 token 可辅助解释，但不能仅凭名字就证明它进行了忠实的自然语言推理。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先确定户外大类，再细分露营装备。每级中间状态都需贴近对应码本语义，避免出现解释像在谈露营，实际却跳到无关家居编码的脱节。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.18664">原论文</a> · <a href="../../../../reproductions/2601.18664-s2gr/">实现解读</a> · <a href="#qa-833b7b1f56656208">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:s2gr" data-paper-title="S2GR: Stepwise Semantic-Guided Reasoning in Latent Space for Generative Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="S2GR: Stepwise Semantic-Guided Reasoning in Latent Space for Generative Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-01-26 在每一级 SID 生成前插入可解释 thinking token，并让它与真实 codebook 分布对比学习；协同共现图和负载均衡共同改善由粗到细的语义层级。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05463，相对变化 +1.15%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation latent-reasoning semantic-id 搜广推 生成式召回与推理推荐 S2GR的thinking对齐损失与码本负载均衡，分别约束什么？ 对齐损失把中间状态连接到本级码本语义，负载均衡关注不同码是否被过度集中使用。前者改善语义关联的监督，后者处理码使用分布；均匀使用并不保证语义正确，语义对齐也不自动避免所有码坍缩，不能把两项互相替代。 教学例子：所有样本都选同一码时负载可能失衡；把样本随机均分到各码虽更均匀，却未必保留了内容含义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-30fd271baa0367d3">S2GR的thinking对齐损失与码本负载均衡，分别约束什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3As2gr">S2GR: Stepwise Semantic-Guided Reasoning in Latent Space for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>对齐损失把中间状态连接到本级码本语义，负载均衡关注不同码是否被过度集中使用。前者改善语义关联的监督，后者处理码使用分布；均匀使用并不保证语义正确，语义对齐也不自动避免所有码坍缩，不能把两项互相替代。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>所有样本都选同一码时负载可能失衡；把样本随机均分到各码虽更均匀，却未必保留了内容含义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.18664">原论文</a> · <a href="../../../../reproductions/2601.18664-s2gr/">实现解读</a> · <a href="#qa-30fd271baa0367d3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:s2gr" data-paper-title="S2GR: Stepwise Semantic-Guided Reasoning in Latent Space for Generative Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="S2GR: Stepwise Semantic-Guided Reasoning in Latent Space for Generative Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-01-26 在每一级 SID 生成前插入可解释 thinking token，并让它与真实 codebook 分布对比学习；协同共现图和负载均衡共同改善由粗到细的语义层级。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05463，相对变化 +1.15%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation latent-reasoning semantic-id 搜广推 生成式召回与推理推荐 S2GR本地码本和thinking是否原生产模型？ 不是，公开MovieLens固定子集只验证中心机制。需对齐本级码、前级历史与thinking位置，平衡目标不能读测试目录标签来挑配置，线上收益只作原文引用。 例如小目录的均匀码使用，不代表工业海量内容层级已训练好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ee90eadef5b0ee26">S2GR本地码本和thinking是否原生产模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3As2gr">S2GR: Stepwise Semantic-Guided Reasoning in Latent Space for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是，公开MovieLens固定子集只验证中心机制。需对齐本级码、前级历史与thinking位置，平衡目标不能读测试目录标签来挑配置，线上收益只作原文引用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如小目录的均匀码使用，不代表工业海量内容层级已训练好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.18664">原论文</a> · <a href="../../../../reproductions/2601.18664-s2gr/">实现解读</a> · <a href="#qa-ee90eadef5b0ee26">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:promise" data-paper-title="PROMISE: Process Reward Models Unlock Test-Time Scaling Laws in Generative Recommendations" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="PROMISE: Process Reward Models Unlock Test-Time Scaling Laws in Generative Recommendations 搜广推与 LLM 应用 Kuaishou Technology 2026-01-08 轻量 path-level PRM 在每个 SID 层级评价中间路径，训练时提供稠密反馈、推理时提前剪除已发生语义漂移的 beam；因此增加 beam width 能形成可控的 test-time scaling。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05929，相对变化 +9.79%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation process-reward test-time-scaling 搜广推 生成式召回与推理推荐 PROMISE 中 SID 前缀对应什么候选范围，为什么剪掉前缀会排除一整批物品？ 层级 SID 像目录地址，前缀确定共享该路径的物品子集，后续码只能在其后继续细分。因此 beam 上一个粗前缀不仅代表一条字符串，也代表一片可达候选；被剪后，其下所有未探索物品都失去本轮机会。这解释了过程评分错误为何可能造成大范围漏召。 示意：首层“摄影”下面有相机、镜头和配件；若首层被误剪，即使某个镜头非常适合用户，后层也不会再看到它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-promise-c348f413" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e151a7faaadabf83">PROMISE 中 SID 前缀对应什么候选范围，为什么剪掉前缀会排除一整批物品？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apromise">PROMISE: Process Reward Models Unlock Test-Time Scaling Laws in Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>层级 SID 像目录地址，前缀确定共享该路径的物品子集，后续码只能在其后继续细分。因此 beam 上一个粗前缀不仅代表一条字符串，也代表一片可达候选；被剪后，其下所有未探索物品都失去本轮机会。这解释了过程评分错误为何可能造成大范围漏召。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>首层“摄影”下面有相机、镜头和配件；若首层被误剪，即使某个镜头非常适合用户，后层也不会再看到它。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.04674">原论文</a> · <a href="../../../../reproductions/2601.04674-promise/">实现解读</a> · <a href="#qa-e151a7faaadabf83">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:promise" data-paper-title="PROMISE: Process Reward Models Unlock Test-Time Scaling Laws in Generative Recommendations" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="PROMISE: Process Reward Models Unlock Test-Time Scaling Laws in Generative Recommendations 搜广推与 LLM 应用 Kuaishou Technology 2026-01-08 轻量 path-level PRM 在每个 SID 层级评价中间路径，训练时提供稠密反馈、推理时提前剪除已发生语义漂移的 beam；因此增加 beam width 能形成可控的 test-time scaling。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05929，相对变化 +9.79%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation process-reward test-time-scaling 搜广推 生成式召回与推理推荐 PROMISE 为什么在 SID 中间路径就给奖励，而不等生成完整物品后才评分？ 层级生成一旦在早期走错语义分支，后续计算很可能继续细化错误方向。轻量过程奖励模型逐层评价路径，既给训练更稠密的反馈，也在推理中及早剪掉漂移 beam。增加束宽因此有机会探索更多有希望路径，但收益受过程评分可靠性与额外计算制约，束越宽并不保证越好。 示意：用户要登山装备，首层路径却进入家居装饰。等生成到具体抱枕才打低分会浪费后续步骤；路径评分可在粗层就淘汰它，把预算留给户外相关分支。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-bd05a70bed64223d">PROMISE 为什么在 SID 中间路径就给奖励，而不等生成完整物品后才评分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apromise">PROMISE: Process Reward Models Unlock Test-Time Scaling Laws in Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>层级生成一旦在早期走错语义分支，后续计算很可能继续细化错误方向。轻量过程奖励模型逐层评价路径，既给训练更稠密的反馈，也在推理中及早剪掉漂移 beam。增加束宽因此有机会探索更多有希望路径，但收益受过程评分可靠性与额外计算制约，束越宽并不保证越好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户要登山装备，首层路径却进入家居装饰。等生成到具体抱枕才打低分会浪费后续步骤；路径评分可在粗层就淘汰它，把预算留给户外相关分支。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.04674">原论文</a> · <a href="../../../../reproductions/2601.04674-promise/">实现解读</a> · <a href="#qa-bd05a70bed64223d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:promise" data-paper-title="PROMISE: Process Reward Models Unlock Test-Time Scaling Laws in Generative Recommendations" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="PROMISE: Process Reward Models Unlock Test-Time Scaling Laws in Generative Recommendations 搜广推与 LLM 应用 Kuaishou Technology 2026-01-08 轻量 path-level PRM 在每个 SID 层级评价中间路径，训练时提供稠密反馈、推理时提前剪除已发生语义漂移的 beam；因此增加 beam width 能形成可控的 test-time scaling。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05929，相对变化 +9.79%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation process-reward test-time-scaling 搜广推 生成式召回与推理推荐 PRM 引导加宽 beam 与纯 likelihood 加宽，相比增加哪种判断？ 纯束宽只探索模型高概率路径，PRM 另提供任务过程价值，允许低一些似然但更合目标分支保留。额外评估增加计算，也可能被奖励偏差带偏。test-time scaling 是预算与质量曲线，不能说束越宽必然越好。 示意：热门路径概率高但偏题，另一条略低却语义对；PRM 可改变保留集合，若它也只爱热门，加宽仍可能围绕同一错误区域。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f4c75f7ff9dd3eba">PRM 引导加宽 beam 与纯 likelihood 加宽，相比增加哪种判断？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apromise">PROMISE: Process Reward Models Unlock Test-Time Scaling Laws in Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>纯束宽只探索模型高概率路径，PRM 另提供任务过程价值，允许低一些似然但更合目标分支保留。额外评估增加计算，也可能被奖励偏差带偏。test-time scaling 是预算与质量曲线，不能说束越宽必然越好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>热门路径概率高但偏题，另一条略低却语义对；PRM 可改变保留集合，若它也只爱热门，加宽仍可能围绕同一错误区域。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.04674">原论文</a> · <a href="../../../../reproductions/2601.04674-promise/">实现解读</a> · <a href="#qa-f4c75f7ff9dd3eba">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:promise" data-paper-title="PROMISE: Process Reward Models Unlock Test-Time Scaling Laws in Generative Recommendations" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="PROMISE: Process Reward Models Unlock Test-Time Scaling Laws in Generative Recommendations 搜广推与 LLM 应用 Kuaishou Technology 2026-01-08 轻量 path-level PRM 在每个 SID 层级评价中间路径，训练时提供稠密反馈、推理时提前剪除已发生语义漂移的 beam；因此增加 beam width 能形成可控的 test-time scaling。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05929，相对变化 +9.79%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation process-reward test-time-scaling 搜广推 生成式召回与推理推荐 PROMISE 累积过程 reward 时，为什么要定义不同前缀长度的可比尺度？ 越长路径自然多项相加，若与不同深度候选直接比较可能产生长度偏好；同层 beam 应共享计算口径，生成 log-prob 与 λR 也需校准。合法目录约束、重复与终止规则另行保持，不能用高 PRM 分覆盖非法物品。 示意：三层有三次正奖励、一层只有一次，直接跨深度比较会偏长；应按定义在同一步或有明确长度处理下比较。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-93c178126616bf5a">PROMISE 累积过程 reward 时，为什么要定义不同前缀长度的可比尺度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apromise">PROMISE: Process Reward Models Unlock Test-Time Scaling Laws in Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>越长路径自然多项相加，若与不同深度候选直接比较可能产生长度偏好；同层 beam 应共享计算口径，生成 log-prob 与 λR 也需校准。合法目录约束、重复与终止规则另行保持，不能用高 PRM 分覆盖非法物品。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三层有三次正奖励、一层只有一次，直接跨深度比较会偏长；应按定义在同一步或有明确长度处理下比较。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.04674">原论文</a> · <a href="../../../../reproductions/2601.04674-promise/">实现解读</a> · <a href="#qa-93c178126616bf5a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dualgr" data-paper-title="DualGR: Generative Retrieval with Long and Short-Term Interests Modeling" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="DualGR: Generative Retrieval with Long and Short-Term Interests Modeling 搜广推与 LLM 应用 USTC / Kuaishou Technology 2025-11-16 短期兴趣与长期兴趣使用双路由器，约束 Semantic ID 前缀有效性，并以曝光感知项抑制头部坍缩。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 dualgr 核心机制；相对 NDCG@10 +6.73%。  retrieval generative-recommendation semantic-id long-short-interest 搜广推 生成式召回与推理推荐 DualGR 为什么保留短期与长期两份生成分布？ 即时需求与稳定偏好时间尺度不同，单一压缩可能让历史数量最多的方向占主导。两路分别学习，再由 gate 动态混合并施加合法前缀与曝光约束。分布混合不是新增两份重复向量，也不保证自动识别所有新兴趣。 示意：长期摄影兴趣仍重要，今天连续出现婴儿用品需求也应独立保留；模型可调整两路比例，而不让多年摄影次数总是压过近期信号。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-dualgr-b1420088" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c504ff33f2e6164e">DualGR 为什么保留短期与长期两份生成分布？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adualgr">DualGR: Generative Retrieval with Long and Short-Term Interests Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · USTC / Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>即时需求与稳定偏好时间尺度不同，单一压缩可能让历史数量最多的方向占主导。两路分别学习，再由 gate 动态混合并施加合法前缀与曝光约束。分布混合不是新增两份重复向量，也不保证自动识别所有新兴趣。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>长期摄影兴趣仍重要，今天连续出现婴儿用品需求也应独立保留；模型可调整两路比例，而不让多年摄影次数总是压过近期信号。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2511.12518">原论文</a> · <a href="../../../../reproductions/2511.12518-dualgr/">实现解读</a> · <a href="#qa-c504ff33f2e6164e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dualgr" data-paper-title="DualGR: Generative Retrieval with Long and Short-Term Interests Modeling" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="DualGR: Generative Retrieval with Long and Short-Term Interests Modeling 搜广推与 LLM 应用 USTC / Kuaishou Technology 2025-11-16 短期兴趣与长期兴趣使用双路由器，约束 Semantic ID 前缀有效性，并以曝光感知项抑制头部坍缩。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 dualgr 核心机制；相对 NDCG@10 +6.73%。  retrieval generative-recommendation semantic-id long-short-interest 搜广推 生成式召回与推理推荐 DualGR为什么分别路由长短期兴趣，而不是把全部历史拼成一条序列？ 短期兴趣反映当前意图，长期兴趣提供稳定偏好，两者可能在不同请求中权重相反。双路由器让模型按状态融合两种生成分布，前缀约束保证输出可对应物品，曝光感知项再抑制热门码垄断。分成两路本身不能保证分工，仍需检查路由是否坍缩以及两路是否学到不同信息。 示意：用户平时爱旅行，今天集中购买厨房用品；短期路应响应当下需求，长期路则保留旅行兴趣，不能让漫长旧历史把最近明显变化完全淹没。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-24d3da30a1a5d844">DualGR为什么分别路由长短期兴趣，而不是把全部历史拼成一条序列？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adualgr">DualGR: Generative Retrieval with Long and Short-Term Interests Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · USTC / Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>短期兴趣反映当前意图，长期兴趣提供稳定偏好，两者可能在不同请求中权重相反。双路由器让模型按状态融合两种生成分布，前缀约束保证输出可对应物品，曝光感知项再抑制热门码垄断。分成两路本身不能保证分工，仍需检查路由是否坍缩以及两路是否学到不同信息。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户平时爱旅行，今天集中购买厨房用品；短期路应响应当下需求，长期路则保留旅行兴趣，不能让漫长旧历史把最近明显变化完全淹没。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2511.12518">原论文</a> · <a href="../../../../reproductions/2511.12518-dualgr/">实现解读</a> · <a href="#qa-24d3da30a1a5d844">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dualgr" data-paper-title="DualGR: Generative Retrieval with Long and Short-Term Interests Modeling" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="DualGR: Generative Retrieval with Long and Short-Term Interests Modeling 搜广推与 LLM 应用 USTC / Kuaishou Technology 2025-11-16 短期兴趣与长期兴趣使用双路由器，约束 Semantic ID 前缀有效性，并以曝光感知项抑制头部坍缩。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 dualgr 核心机制；相对 NDCG@10 +6.73%。  retrieval generative-recommendation semantic-id long-short-interest 搜广推 生成式召回与推理推荐 双路由与固定指数时间衰减，相比多出什么自由度？ 固定衰减预设旧事件影响随时间变化，双路可学习不同的统计规律并按请求切换，适应非线性兴趣变化。代价是更多参数与门控校准，短期可能追噪声，长期可能过时。机制灵活性不构成对所有数据效果更好的证据。 示意：一次偶然点击可保持低短期权重，连续强需求则提高它；单个衰减常数较难同时表达这两种触发条件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-884b6556aed9923b">双路由与固定指数时间衰减，相比多出什么自由度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adualgr">DualGR: Generative Retrieval with Long and Short-Term Interests Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · USTC / Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定衰减预设旧事件影响随时间变化，双路可学习不同的统计规律并按请求切换，适应非线性兴趣变化。代价是更多参数与门控校准，短期可能追噪声，长期可能过时。机制灵活性不构成对所有数据效果更好的证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次偶然点击可保持低短期权重，连续强需求则提高它；单个衰减常数较难同时表达这两种触发条件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2511.12518">原论文</a> · <a href="../../../../reproductions/2511.12518-dualgr/">实现解读</a> · <a href="#qa-884b6556aed9923b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dualgr" data-paper-title="DualGR: Generative Retrieval with Long and Short-Term Interests Modeling" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="DualGR: Generative Retrieval with Long and Short-Term Interests Modeling 搜广推与 LLM 应用 USTC / Kuaishou Technology 2025-11-16 短期兴趣与长期兴趣使用双路由器，约束 Semantic ID 前缀有效性，并以曝光感知项抑制头部坍缩。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 dualgr 核心机制；相对 NDCG@10 +6.73%。  retrieval generative-recommendation semantic-id long-short-interest 搜广推 生成式召回与推理推荐 DualGR 为什么不能直接融合两套列顺序不同的 item 概率？ 两路必须对同一 item 身份赋值后才能按 gate 相加，码表与候选顺序需对齐；合法前缀也要映到实际可服务对象。曝光项应使用训练可用口径，不得从测试未来热门度构造。本地代理仍不代表生产动态路由全部细节。 示意：短期第一列是相机、长期第一列是童装，直接加总虽不报维度错，却没有概率含义；先按物品 ID 对齐才可融合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d3bcd19f48d36e04">DualGR 为什么不能直接融合两套列顺序不同的 item 概率？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adualgr">DualGR: Generative Retrieval with Long and Short-Term Interests Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · USTC / Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两路必须对同一 item 身份赋值后才能按 gate 相加，码表与候选顺序需对齐；合法前缀也要映到实际可服务对象。曝光项应使用训练可用口径，不得从测试未来热门度构造。本地代理仍不代表生产动态路由全部细节。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>短期第一列是相机、长期第一列是童装，直接加总虽不报维度错，却没有概率含义；先按物品 ID 对齐才可融合。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2511.12518">原论文</a> · <a href="../../../../reproductions/2511.12518-dualgr/">实现解读</a> · <a href="#qa-d3bcd19f48d36e04">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:plum" data-paper-title="PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations 搜广推与 LLM 应用 Google DeepMind / YouTube 2025-10-09 传统 large embedding model（LEM）把绝大多数参数放在千万级 ID embedding 表，神经网络容量反而很小，难以获得 LLM 式 scaling。PLUM 从 Gemini-1.5 MoE 初始化，把视频量化成 Semantic ID（SID），先用用户行为与视频文本/ASR/频道元数据做 continued pre-training（CPT），再以 next-SID generation 做生成式召回。线上用 beam search 直接生成候选 SID，不再维护点积检索索引。 LLM 初始化组在有无 CPT 时 Recall@10 都为 0，未复现论文中 LLM initialization 的增益。Fidelity: 完整核心链路复现。本地实际执行多层 RQ Semantic ID、预训练 decoder-only LM 的 CPT、next-SID SFT 和 token-level constrained beam search；只缩小模型/数据规模并替换私有模态。本地对照口径：基线是随机初始化无 CPT（R1），实验组是随机初始化有 CPT（CR1）；Recall@10 都是 0.0050（0.00%），但 SFT final loss 从 3.5023 降至 2.5933；   搜广推 生成式召回与推理推荐 PLUM 为什么用行为与 SID—元数据混合 CPT，而不只微调下一物品码？ 行为序列教消费转移，SID 与文本、ASR 等元数据连接离散地址和语言语义，CPT 将预训语言知识适配到推荐世界，之后 SFT 再专注召回。两类语料配比会影响能力，loss 更低并不保证搜索目标更准。 示意：模型既学“这串码是一部露营教程”，也学用户看完后常选什么；只背下一码可能保留协同却无法利用内容常识。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-plum-515f2ca7" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-099601afbacbb260">PLUM 为什么用行为与 SID—元数据混合 CPT，而不只微调下一物品码？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aplum">PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>行为序列教消费转移，SID 与文本、ASR 等元数据连接离散地址和语言语义，CPT 将预训语言知识适配到推荐世界，之后 SFT 再专注召回。两类语料配比会影响能力，loss 更低并不保证搜索目标更准。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型既学“这串码是一部露营教程”，也学用户看完后常选什么；只背下一码可能保留协同却无法利用内容常识。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.07784">原论文</a> · <a href="../../../../reproductions/2510.07784-plum/">实现解读</a> · <a href="#qa-099601afbacbb260">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:plum" data-paper-title="PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations 搜广推与 LLM 应用 Google DeepMind / YouTube 2025-10-09 传统 large embedding model（LEM）把绝大多数参数放在千万级 ID embedding 表，神经网络容量反而很小，难以获得 LLM 式 scaling。PLUM 从 Gemini-1.5 MoE 初始化，把视频量化成 Semantic ID（SID），先用用户行为与视频文本/ASR/频道元数据做 continued pre-training（CPT），再以 next-SID generation 做生成式召回。线上用 beam search 直接生成候选 SID，不再维护点积检索索引。 LLM 初始化组在有无 CPT 时 Recall@10 都为 0，未复现论文中 LLM initialization 的增益。Fidelity: 完整核心链路复现。本地实际执行多层 RQ Semantic ID、预训练 decoder-only LM 的 CPT、next-SID SFT 和 token-level constrained beam search；只缩小模型/数据规模并替换私有模态。本地对照口径：基线是随机初始化无 CPT（R1），实验组是随机初始化有 CPT（CR1）；Recall@10 都是 0.0050（0.00%），但 SFT final loss 从 3.5023 降至 2.5933；   搜广推 生成式召回与推理推荐 PLUM 为什么把视频变成层级 SID 并继续预训练语言模型，而不是继续扩大 ID embedding 表？ 巨型 ID 表把参数花在逐物品记忆上，新物品难共享知识，也不能充分利用大语言模型的网络容量。层级 SID 把输出分解为可组合的码，CPT 再把行为与文本、ASR 和元数据接入语言模型，随后学习 next-SID。线上直接束搜索生成候选，但 SID 的语义与协同质量仍决定路径是否适合推荐。 示意：新增一条烘焙视频时，独立 ID 只能从少量点击起步；若它拥有与已有烘焙内容共享的粗粒度码，生成器可先复用主题知识，再在细码上区分具体视频。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-0d1840f495739871">PLUM 为什么把视频变成层级 SID 并继续预训练语言模型，而不是继续扩大 ID embedding 表？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aplum">PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>巨型 ID 表把参数花在逐物品记忆上，新物品难共享知识，也不能充分利用大语言模型的网络容量。层级 SID 把输出分解为可组合的码，CPT 再把行为与文本、ASR 和元数据接入语言模型，随后学习 next-SID。线上直接束搜索生成候选，但 SID 的语义与协同质量仍决定路径是否适合推荐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新增一条烘焙视频时，独立 ID 只能从少量点击起步；若它拥有与已有烘焙内容共享的粗粒度码，生成器可先复用主题知识，再在细码上区分具体视频。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.07784">原论文</a> · <a href="../../../../reproductions/2510.07784-plum/">实现解读</a> · <a href="#qa-0d1840f495739871">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:plum" data-paper-title="PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations 搜广推与 LLM 应用 Google DeepMind / YouTube 2025-10-09 传统 large embedding model（LEM）把绝大多数参数放在千万级 ID embedding 表，神经网络容量反而很小，难以获得 LLM 式 scaling。PLUM 从 Gemini-1.5 MoE 初始化，把视频量化成 Semantic ID（SID），先用用户行为与视频文本/ASR/频道元数据做 continued pre-training（CPT），再以 next-SID generation 做生成式召回。线上用 beam search 直接生成候选 SID，不再维护点积检索索引。 LLM 初始化组在有无 CPT 时 Recall@10 都为 0，未复现论文中 LLM initialization 的增益。Fidelity: 完整核心链路复现。本地实际执行多层 RQ Semantic ID、预训练 decoder-only LM 的 CPT、next-SID SFT 和 token-level constrained beam search；只缩小模型/数据规模并替换私有模态。本地对照口径：基线是随机初始化无 CPT（R1），实验组是随机初始化有 CPT（CR1）；Recall@10 都是 0.0050（0.00%），但 SFT final loss 从 3.5023 降至 2.5933；   搜广推 生成式召回与推理推荐 PLUM 的随机初始化与 LLM 初始化四组消融，为什么要再交叉有无 CPT？ 只比较预训与随机会混入初始化和继续训练差异，四组分别检查两因素及其相互作用。来源本地 CPT 降 loss 却没提高 Recall，LLM 初始化组甚至零命中，不能把收敛改善当最终检索成功或普遍 scaling 证据。 示意：随机无 CPT、随机有 CPT、LLM 无 CPT、LLM 有 CPT分别运行，才能知道是语言初始化帮助，还是额外训练预算作用，而非合并成一个原因。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1fb69e0e018a5cfa">PLUM 的随机初始化与 LLM 初始化四组消融，为什么要再交叉有无 CPT？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aplum">PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只比较预训与随机会混入初始化和继续训练差异，四组分别检查两因素及其相互作用。来源本地 CPT 降 loss 却没提高 Recall，LLM 初始化组甚至零命中，不能把收敛改善当最终检索成功或普遍 scaling 证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>随机无 CPT、随机有 CPT、LLM 无 CPT、LLM 有 CPT分别运行，才能知道是语言初始化帮助，还是额外训练预算作用，而非合并成一个原因。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.07784">原论文</a> · <a href="../../../../reproductions/2510.07784-plum/">实现解读</a> · <a href="#qa-1fb69e0e018a5cfa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:plum" data-paper-title="PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations 搜广推与 LLM 应用 Google DeepMind / YouTube 2025-10-09 传统 large embedding model（LEM）把绝大多数参数放在千万级 ID embedding 表，神经网络容量反而很小，难以获得 LLM 式 scaling。PLUM 从 Gemini-1.5 MoE 初始化，把视频量化成 Semantic ID（SID），先用用户行为与视频文本/ASR/频道元数据做 continued pre-training（CPT），再以 next-SID generation 做生成式召回。线上用 beam search 直接生成候选 SID，不再维护点积检索索引。 LLM 初始化组在有无 CPT 时 Recall@10 都为 0，未复现论文中 LLM initialization 的增益。Fidelity: 完整核心链路复现。本地实际执行多层 RQ Semantic ID、预训练 decoder-only LM 的 CPT、next-SID SFT 和 token-level constrained beam search；只缩小模型/数据规模并替换私有模态。本地对照口径：基线是随机初始化无 CPT（R1），实验组是随机初始化有 CPT（CR1）；Recall@10 都是 0.0050（0.00%），但 SFT final loss 从 3.5023 降至 2.5933；   搜广推 生成式召回与推理推荐 PLUM 的 progressive masking 为什么只重构前 r 层码字和，而不是随机打乱层？ 残差层有粗到细累积顺序，随机深度训练要求各前缀本身有用，强化层级；任意打乱破坏残差含义。SFT prompt loss 屏蔽只监督目标 SID，catalog trie 保合法。prompt 文字也计 loss 则变成不同目标，不能无说明替换。 示意：有时只用粗码重建，有时用粗细码一起，促使首层承载主题；把第三层残差单独当首码，不再是同一渐进层级。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e504366a2a68836e">PLUM 的 progressive masking 为什么只重构前 r 层码字和，而不是随机打乱层？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aplum">PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>残差层有粗到细累积顺序，随机深度训练要求各前缀本身有用，强化层级；任意打乱破坏残差含义。SFT prompt loss 屏蔽只监督目标 SID，catalog trie 保合法。prompt 文字也计 loss 则变成不同目标，不能无说明替换。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>有时只用粗码重建，有时用粗细码一起，促使首层承载主题；把第三层残差单独当首码，不再是同一渐进层级。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.07784">原论文</a> · <a href="../../../../reproductions/2510.07784-plum/">实现解读</a> · <a href="#qa-e504366a2a68836e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:intsr" data-paper-title="IntSR: An Integrated Generative Framework for Search and Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="IntSR: An Integrated Generative Framework for Search and Recommendation 搜广推与 LLM 应用 Alibaba / Amap 2025-09-25 用显式查询和隐式会话意图共同生成 POI/物品，统一搜索与推荐词表，并加入时间上下文刻画意图漂移。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 intsr 核心机制；相对 NDCG@10 +33.56%。  search recommendation generative-retrieval content-understanding 搜广推 生成式召回与推理推荐 IntSR 为什么把显式 query 与隐式 session 意图合到同一物品空间？ 搜索词明确但可能省略背景，会话行为丰富却不直接表达当前请求，共同估计意图让搜索与推荐利用互补证据。统一词表避免两个入口输出身份割裂，时间再刻画漂移。没有查询时应有定义的缺失路径，而非伪造用户说过的话。 示意：用户只搜“附近”，历史显示最近找素食，可共同推断餐饮需求；无搜索入口则依会话推荐，不应随便补一条不存在的真实 query。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-intsr-9d48eca1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e9621be987a8d381">IntSR 为什么把显式 query 与隐式 session 意图合到同一物品空间？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aintsr">IntSR: An Integrated Generative Framework for Search and Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Amap</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>搜索词明确但可能省略背景，会话行为丰富却不直接表达当前请求，共同估计意图让搜索与推荐利用互补证据。统一词表避免两个入口输出身份割裂，时间再刻画漂移。没有查询时应有定义的缺失路径，而非伪造用户说过的话。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户只搜“附近”，历史显示最近找素食，可共同推断餐饮需求；无搜索入口则依会话推荐，不应随便补一条不存在的真实 query。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2509.21179">原论文</a> · <a href="../../../../reproductions/2509.21179-intsr/">实现解读</a> · <a href="#qa-e9621be987a8d381">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:intsr" data-paper-title="IntSR: An Integrated Generative Framework for Search and Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="IntSR: An Integrated Generative Framework for Search and Recommendation 搜广推与 LLM 应用 Alibaba / Amap 2025-09-25 用显式查询和隐式会话意图共同生成 POI/物品，统一搜索与推荐词表，并加入时间上下文刻画意图漂移。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 intsr 核心机制；相对 NDCG@10 +33.56%。  search recommendation generative-retrieval content-understanding 搜广推 生成式召回与推理推荐 IntSR怎样同时处理显式搜索词和没有搜索词的推荐意图？ 显式查询给出当前表达，隐式会话历史补充未说出的需求，两者共同推断潜在意图，再以统一物品或POI词表生成结果。时间上下文帮助区分需求是否仍有效，减少搜索与推荐之间的语义割裂。统一词表不意味着可以忽略查询约束，也不能把旧会话中的兴趣当成用户现在明确提出的要求。 示意：用户搜附近咖啡，历史显示偏好安静环境，模型可同时利用二者；若只是浏览推荐，则从会话推断需求，但不能把昨日地点当成今日仍然有效的位置。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-fb387442d699fb31">IntSR怎样同时处理显式搜索词和没有搜索词的推荐意图？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aintsr">IntSR: An Integrated Generative Framework for Search and Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Amap</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>显式查询给出当前表达，隐式会话历史补充未说出的需求，两者共同推断潜在意图，再以统一物品或POI词表生成结果。时间上下文帮助区分需求是否仍有效，减少搜索与推荐之间的语义割裂。统一词表不意味着可以忽略查询约束，也不能把旧会话中的兴趣当成用户现在明确提出的要求。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户搜附近咖啡，历史显示偏好安静环境，模型可同时利用二者；若只是浏览推荐，则从会话推断需求，但不能把昨日地点当成今日仍然有效的位置。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2509.21179">原论文</a> · <a href="../../../../reproductions/2509.21179-intsr/">实现解读</a> · <a href="#qa-fb387442d699fb31">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:intsr" data-paper-title="IntSR: An Integrated Generative Framework for Search and Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="IntSR: An Integrated Generative Framework for Search and Recommendation 搜广推与 LLM 应用 Alibaba / Amap 2025-09-25 用显式查询和隐式会话意图共同生成 POI/物品，统一搜索与推荐词表，并加入时间上下文刻画意图漂移。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 intsr 核心机制；相对 NDCG@10 +33.56%。  search recommendation generative-retrieval content-understanding 搜广推 生成式召回与推理推荐 IntSR 的潜意图混合与直接拼接 q、h 做打分，有何可解释分解？ 混合写成先估意图分布再按意图和时间生成物品，将不确定的多种需求显式保留；直接拼接可隐式表达但未必形成同样结构。潜变量不保证具有人类固定含义，输出更可分解也不代表真实意图已被识别。 示意：“周末活动”可能指徒步或展览，先保留两种意图概率再选地点，比强行当作唯一类别更自然；但概率仍只是模型估计。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-42ca84522a89bc1e">IntSR 的潜意图混合与直接拼接 q、h 做打分，有何可解释分解？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aintsr">IntSR: An Integrated Generative Framework for Search and Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Amap</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>混合写成先估意图分布再按意图和时间生成物品，将不确定的多种需求显式保留；直接拼接可隐式表达但未必形成同样结构。潜变量不保证具有人类固定含义，输出更可分解也不代表真实意图已被识别。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>“周末活动”可能指徒步或展览，先保留两种意图概率再选地点，比强行当作唯一类别更自然；但概率仍只是模型估计。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2509.21179">原论文</a> · <a href="../../../../reproductions/2509.21179-intsr/">实现解读</a> · <a href="#qa-42ca84522a89bc1e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:intsr" data-paper-title="IntSR: An Integrated Generative Framework for Search and Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="IntSR: An Integrated Generative Framework for Search and Recommendation 搜广推与 LLM 应用 Alibaba / Amap 2025-09-25 用显式查询和隐式会话意图共同生成 POI/物品，统一搜索与推荐词表，并加入时间上下文刻画意图漂移。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 intsr 核心机制；相对 NDCG@10 +33.56%。  search recommendation generative-retrieval content-understanding 搜广推 生成式召回与推理推荐 IntSR 实现无 query 场景时，怎样避免和空字符串真实搜索混淆？ 应按模型契约使用缺失标识或对应分支，使搜索存在性清楚；时间条件只能来自请求时刻，目标 POI 不得进入潜意图估计。两入口共享 item 身份但不意味着共享所有标签。来源电影核心代理不能检验真实位置和营业限制。 示意：没发起搜索与主动提交空白查询可能有不同日志含义，不能都无说明编码成同一字符串，再把差异全交给模型猜。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3b3becae3d60389c">IntSR 实现无 query 场景时，怎样避免和空字符串真实搜索混淆？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aintsr">IntSR: An Integrated Generative Framework for Search and Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Amap</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>应按模型契约使用缺失标识或对应分支，使搜索存在性清楚；时间条件只能来自请求时刻，目标 POI 不得进入潜意图估计。两入口共享 item 身份但不意味着共享所有标签。来源电影核心代理不能检验真实位置和营业限制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>没发起搜索与主动提交空白查询可能有不同日志含义，不能都无说明编码成同一字符串，再把差异全交给模型猜。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2509.21179">原论文</a> · <a href="../../../../reproductions/2509.21179-intsr/">实现解读</a> · <a href="#qa-3b3becae3d60389c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onerec-v2" data-paper-title="OneRec-V2 Technical Report" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneRec-V2 Technical Report 搜广推与 LLM 应用 Kuaishou 2025-08-28 OneRec-V1 用 encoder-decoder 生成推荐 session，但长历史 encoder 重复计算，偏好对齐又依赖额外 reward model。V2 只把最新曝光作为监督目标；Context Processor 一次生成所有 decoder 层共享的 K/V，目标侧只解码 [BOS,s1,s2]→[s1,s2,s3]。Lazy block 依次执行 cross-attention、causal self-attention 和 FFN，并结合 GQA、K=V、跨层 KV sharing。 Fidelity: 完整核心链路复现。实际训练三层 residual-quantized Semantic ID、newest-impression SFT、layer-shared K/V Lazy Decoder、Duration-Aware Reward Shaping 和 GBPO；仅缩小模型/数据，省略私有异构特征与分布式 serving。本地对照口径：效率基线是 Encoder-Decoder，实验组 Lazy SFT 的延迟 -54.78%、validation loss -0.34%；对齐基线是 Lazy SFT，加入 GBPO 后反馈加权概率 +21.66%。  llm-recommendation generative-retrieval reinforcement-learning 搜广推 生成式召回与推理推荐 OneRec-V2 为什么用真实播放与负反馈代替额外 reward model？ 后训练直接利用用户行为减少另训奖励器的成本与误差传播，DARS 校正时长机会，GBPO 控制正负更新。行为仍是代理且有偏，不能因标签真实就当满意度真值。省去奖励模型也不意味着后训练不需约束或数据校准。 示意：长视频播放多秒可能只是时长大，先在用户和时长桶内比较，再给正优势，比直接把所有长看当高满意更谨慎。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-onerec-v2-8a1036e5" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-92affcd5baccf4bd">OneRec-V2 为什么用真实播放与负反馈代替额外 reward model？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonerec-v2">OneRec-V2 Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>后训练直接利用用户行为减少另训奖励器的成本与误差传播，DARS 校正时长机会，GBPO 控制正负更新。行为仍是代理且有偏，不能因标签真实就当满意度真值。省去奖励模型也不意味着后训练不需约束或数据校准。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>长视频播放多秒可能只是时长大，先在用户和时长桶内比较，再给正优势，比直接把所有长看当高满意更谨慎。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.20900">原论文</a> · <a href="../../../../reproductions/2508.20900-onerec-v2/">实现解读</a> · <a href="#qa-92affcd5baccf4bd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onerec-v2" data-paper-title="OneRec-V2 Technical Report" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneRec-V2 Technical Report 搜广推与 LLM 应用 Kuaishou 2025-08-28 OneRec-V1 用 encoder-decoder 生成推荐 session，但长历史 encoder 重复计算，偏好对齐又依赖额外 reward model。V2 只把最新曝光作为监督目标；Context Processor 一次生成所有 decoder 层共享的 K/V，目标侧只解码 [BOS,s1,s2]→[s1,s2,s3]。Lazy block 依次执行 cross-attention、causal self-attention 和 FFN，并结合 GQA、K=V、跨层 KV sharing。 Fidelity: 完整核心链路复现。实际训练三层 residual-quantized Semantic ID、newest-impression SFT、layer-shared K/V Lazy Decoder、Duration-Aware Reward Shaping 和 GBPO；仅缩小模型/数据，省略私有异构特征与分布式 serving。本地对照口径：效率基线是 Encoder-Decoder，实验组 Lazy SFT 的延迟 -54.78%、validation loss -0.34%；对齐基线是 Lazy SFT，加入 GBPO 后反馈加权概率 +21.66%。  llm-recommendation generative-retrieval reinforcement-learning 搜广推 生成式召回与推理推荐 OneRec-V2 为什么只监督最新曝光，并让所有 decoder 层共享一次生成的上下文 K/V？ 最新曝光监督把训练目标集中到请求末端，避免为每个历史位置重复做完整目标解码。Context Processor 一次产生可被多个解码层复用的上下文 K/V，Lazy block 再按需交互并生成短 SID。它减少的是历史编码与逐层缓存的重复成本；后训练的真实反馈对齐是另一条改动，不能把全部效果归给共享 K/V。 示意：用户有很长历史，当前只需要预测最新请求的三层物品码。先把历史处理成一份共享记忆，解码各层重复读取它，比每层各自重新构造整段历史缓存更节省。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-6a8c770978f6160d">OneRec-V2 为什么只监督最新曝光，并让所有 decoder 层共享一次生成的上下文 K/V？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonerec-v2">OneRec-V2 Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最新曝光监督把训练目标集中到请求末端，避免为每个历史位置重复做完整目标解码。Context Processor 一次产生可被多个解码层复用的上下文 K/V，Lazy block 再按需交互并生成短 SID。它减少的是历史编码与逐层缓存的重复成本；后训练的真实反馈对齐是另一条改动，不能把全部效果归给共享 K/V。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户有很长历史，当前只需要预测最新请求的三层物品码。先把历史处理成一份共享记忆，解码各层重复读取它，比每层各自重新构造整段历史缓存更节省。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.20900">原论文</a> · <a href="../../../../reproductions/2508.20900-onerec-v2/">实现解读</a> · <a href="#qa-6a8c770978f6160d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onerec-v2" data-paper-title="OneRec-V2 Technical Report" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneRec-V2 Technical Report 搜广推与 LLM 应用 Kuaishou 2025-08-28 OneRec-V1 用 encoder-decoder 生成推荐 session，但长历史 encoder 重复计算，偏好对齐又依赖额外 reward model。V2 只把最新曝光作为监督目标；Context Processor 一次生成所有 decoder 层共享的 K/V，目标侧只解码 [BOS,s1,s2]→[s1,s2,s3]。Lazy block 依次执行 cross-attention、causal self-attention 和 FFN，并结合 GQA、K=V、跨层 KV sharing。 Fidelity: 完整核心链路复现。实际训练三层 residual-quantized Semantic ID、newest-impression SFT、layer-shared K/V Lazy Decoder、Duration-Aware Reward Shaping 和 GBPO；仅缩小模型/数据，省略私有异构特征与分布式 serving。本地对照口径：效率基线是 Encoder-Decoder，实验组 Lazy SFT 的延迟 -54.78%、validation loss -0.34%；对齐基线是 Lazy SFT，加入 GBPO 后反馈加权概率 +21.66%。  llm-recommendation generative-retrieval reinforcement-learning 搜广推 生成式召回与推理推荐 GBPO 的动态分母与 PPO clipping，为什么不是同一限制写法？ PPO 截断概率比区间，GBPO 按优势符号使用不同停止梯度分母，限制更新幅度的机制不同。把它改写成常见 clip 实现会丢定义性行为。来源本地反馈加权概率不是 NDCG 或线上收益，也不是三种子都正向。 示意：正优势与负优势使用不同分母，改变当前概率时梯度响应不一样；统一套一个正负对称 clip 不能仅凭名字叫策略优化就视为等价。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e475b3cbab1bb254">GBPO 的动态分母与 PPO clipping，为什么不是同一限制写法？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonerec-v2">OneRec-V2 Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>PPO 截断概率比区间，GBPO 按优势符号使用不同停止梯度分母，限制更新幅度的机制不同。把它改写成常见 clip 实现会丢定义性行为。来源本地反馈加权概率不是 NDCG 或线上收益，也不是三种子都正向。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>正优势与负优势使用不同分母，改变当前概率时梯度响应不一样；统一套一个正负对称 clip 不能仅凭名字叫策略优化就视为等价。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.20900">原论文</a> · <a href="../../../../reproductions/2508.20900-onerec-v2/">实现解读</a> · <a href="#qa-e475b3cbab1bb254">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onerec-v2" data-paper-title="OneRec-V2 Technical Report" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneRec-V2 Technical Report 搜广推与 LLM 应用 Kuaishou 2025-08-28 OneRec-V1 用 encoder-decoder 生成推荐 session，但长历史 encoder 重复计算，偏好对齐又依赖额外 reward model。V2 只把最新曝光作为监督目标；Context Processor 一次生成所有 decoder 层共享的 K/V，目标侧只解码 [BOS,s1,s2]→[s1,s2,s3]。Lazy block 依次执行 cross-attention、causal self-attention 和 FFN，并结合 GQA、K=V、跨层 KV sharing。 Fidelity: 完整核心链路复现。实际训练三层 residual-quantized Semantic ID、newest-impression SFT、layer-shared K/V Lazy Decoder、Duration-Aware Reward Shaping 和 GBPO；仅缩小模型/数据，省略私有异构特征与分布式 serving。本地对照口径：效率基线是 Encoder-Decoder，实验组 Lazy SFT 的延迟 -54.78%、validation loss -0.34%；对齐基线是 Lazy SFT，加入 GBPO 后反馈加权概率 +21.66%。  llm-recommendation generative-retrieval reinforcement-learning 搜广推 生成式召回与推理推荐 DARS 分位数为何必须在同用户、同时长桶内计算，GBPO 分母又为何 detach？ 分位数用于比较类似观看机会，跨用户或跨时长会混入习惯与长度；分母 stop-gradient 避免反传穿过限制项改变预期更新。显式 dislike 的负优势与其他零优势分开。训练标签只在后训练侧，不能作为当前请求输入。 示意：十秒与十分钟视频的三十秒观看不可直接排同一分位；分母若也跟概率求导，公式看着相同，实际梯度就不是原定义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6ddf463c07f9e6ca">DARS 分位数为何必须在同用户、同时长桶内计算，GBPO 分母又为何 detach？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonerec-v2">OneRec-V2 Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分位数用于比较类似观看机会，跨用户或跨时长会混入习惯与长度；分母 stop-gradient 避免反传穿过限制项改变预期更新。显式 dislike 的负优势与其他零优势分开。训练标签只在后训练侧，不能作为当前请求输入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>十秒与十分钟视频的三十秒观看不可直接排同一分位；分母若也跟概率求导，公式看着相同，实际梯度就不是原定义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.20900">原论文</a> · <a href="../../../../reproductions/2508.20900-onerec-v2/">实现解读</a> · <a href="#qa-6ddf463c07f9e6ca">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pinrec" data-paper-title="PinRec: Outcome-Conditioned, Multi-Token Generative Retrieval for Industry-Scale Recommendation Systems" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="PinRec: Outcome-Conditioned, Multi-Token Generative Retrieval for Industry-Scale Recommendation Systems 搜广推与 LLM 应用 Pinterest 2025-04-09 普通 next-item 只会延续用户最常见行为，且严格顺序不适合 feed session。PinRec 把期望 outcome 注入输出头，并在同一未来窗口一次生成多个 ANN-compatible item vectors。 Fidelity: 完整核心链路复现。真实执行因果 decoder、outcome embedding、归一化 ANN 输出、无序未来窗口 multi-token 对比学习；MovieLens 评分档位替代 Pinterest 多 surface action。本地对照口径：基线是 unconditioned next-token 模型；实验组是 outcome-conditioned 三 token window；Unordered Recall@10 -27.78%、NDCG@10 -34.82%。这是 outcome/multi-token 模块消融，不是相对 DIN。  generative-retrieval outcome-conditioning multi-token 搜广推 生成式召回与推理推荐 PinRec 的 outcome 条件为什么与用户实际下一次反馈标签不同？ desired outcome 是希望生成器面向的目标，可作为合法业务条件；实际未来动作尚未发生，只能作训练监督。混淆两者会在评估提前选对条件。多向量输出还针对窗口多兴趣，不代表生成用户必做的一串确定行为。 示意：请求希望发现可收藏内容可指定收藏目标，但不能看测试目标确实被收藏后才给条件，再宣称模型自主预测了这次偏好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-pinrec-66bf0193" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-98e4eb3523117a34">PinRec 的 outcome 条件为什么与用户实际下一次反馈标签不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apinrec">PinRec: Outcome-Conditioned, Multi-Token Generative Retrieval for Industry-Scale Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>desired outcome 是希望生成器面向的目标，可作为合法业务条件；实际未来动作尚未发生，只能作训练监督。混淆两者会在评估提前选对条件。多向量输出还针对窗口多兴趣，不代表生成用户必做的一串确定行为。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>请求希望发现可收藏内容可指定收藏目标，但不能看测试目标确实被收藏后才给条件，再宣称模型自主预测了这次偏好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.10507">原论文</a> · <a href="../../../../reproductions/2504.10507-pinrec/">实现解读</a> · <a href="#qa-98e4eb3523117a34">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pinrec" data-paper-title="PinRec: Outcome-Conditioned, Multi-Token Generative Retrieval for Industry-Scale Recommendation Systems" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="PinRec: Outcome-Conditioned, Multi-Token Generative Retrieval for Industry-Scale Recommendation Systems 搜广推与 LLM 应用 Pinterest 2025-04-09 普通 next-item 只会延续用户最常见行为，且严格顺序不适合 feed session。PinRec 把期望 outcome 注入输出头，并在同一未来窗口一次生成多个 ANN-compatible item vectors。 Fidelity: 完整核心链路复现。真实执行因果 decoder、outcome embedding、归一化 ANN 输出、无序未来窗口 multi-token 对比学习；MovieLens 评分档位替代 Pinterest 多 surface action。本地对照口径：基线是 unconditioned next-token 模型；实验组是 outcome-conditioned 三 token window；Unordered Recall@10 -27.78%、NDCG@10 -34.82%。这是 outcome/multi-token 模块消融，不是相对 DIN。  generative-retrieval outcome-conditioning multi-token 搜广推 生成式召回与推理推荐 PinRec 为什么把期望 outcome 注入输出头，并在未来窗口预测多个物品向量？ 单一 next-item 目标容易重复用户最常见行为，也把同一窗口的消费强加为固定顺序。期望 outcome 提供行为条件，多输出头预测窗口内多个 ANN 兼容向量，使检索能覆盖并存兴趣。向量可接现有近邻系统，但训练需要处理预测与窗口正例的对应，不能把多个头仅当成重复采样同一个最热门物品。 示意：希望用户收藏而非随手浏览时，输出条件切换为收藏。一个未来窗口同时有园艺和烘焙内容，多向量可以覆盖两类兴趣，不必认为先看园艺才是唯一正确顺序。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-2ea183949a2f6b44">PinRec 为什么把期望 outcome 注入输出头，并在未来窗口预测多个物品向量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apinrec">PinRec: Outcome-Conditioned, Multi-Token Generative Retrieval for Industry-Scale Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单一 next-item 目标容易重复用户最常见行为，也把同一窗口的消费强加为固定顺序。期望 outcome 提供行为条件，多输出头预测窗口内多个 ANN 兼容向量，使检索能覆盖并存兴趣。向量可接现有近邻系统，但训练需要处理预测与窗口正例的对应，不能把多个头仅当成重复采样同一个最热门物品。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>希望用户收藏而非随手浏览时，输出条件切换为收藏。一个未来窗口同时有园艺和烘焙内容，多向量可以覆盖两类兴趣，不必认为先看园艺才是唯一正确顺序。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.10507">原论文</a> · <a href="../../../../reproductions/2504.10507-pinrec/">实现解读</a> · <a href="#qa-2ea183949a2f6b44">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pinrec" data-paper-title="PinRec: Outcome-Conditioned, Multi-Token Generative Retrieval for Industry-Scale Recommendation Systems" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="PinRec: Outcome-Conditioned, Multi-Token Generative Retrieval for Industry-Scale Recommendation Systems 搜广推与 LLM 应用 Pinterest 2025-04-09 普通 next-item 只会延续用户最常见行为，且严格顺序不适合 feed session。PinRec 把期望 outcome 注入输出头，并在同一未来窗口一次生成多个 ANN-compatible item vectors。 Fidelity: 完整核心链路复现。真实执行因果 decoder、outcome embedding、归一化 ANN 输出、无序未来窗口 multi-token 对比学习；MovieLens 评分档位替代 Pinterest 多 surface action。本地对照口径：基线是 unconditioned next-token 模型；实验组是 outcome-conditioned 三 token window；Unordered Recall@10 -27.78%、NDCG@10 -34.82%。这是 outcome/multi-token 模块消融，不是相对 DIN。  generative-retrieval outcome-conditioning multi-token 搜广推 生成式召回与推理推荐 PinRec 的 unordered window 召回与严格 next-token 命中，评价对象为何不同？ 窗口多正例不要求唯一先后，多个向量可覆盖同时期需求；严格下一项只认可紧邻目标，可能惩罚合理但次序不同的输出。比较需要一致标签与候选口径，来源两类指标都负向，不能换一个更宽容指标隐藏失败。 示意：未来一天看相机和帐篷，多兴趣召回同时找到两类合理；若只以首个相机作唯一答案，帐篷命中不算同一意义的 next-token 成功。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-9ee1c6eb0e5343e2">PinRec 的 unordered window 召回与严格 next-token 命中，评价对象为何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apinrec">PinRec: Outcome-Conditioned, Multi-Token Generative Retrieval for Industry-Scale Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>窗口多正例不要求唯一先后，多个向量可覆盖同时期需求；严格下一项只认可紧邻目标，可能惩罚合理但次序不同的输出。比较需要一致标签与候选口径，来源两类指标都负向，不能换一个更宽容指标隐藏失败。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>未来一天看相机和帐篷，多兴趣召回同时找到两类合理；若只以首个相机作唯一答案，帐篷命中不算同一意义的 next-token 成功。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.10507">原论文</a> · <a href="../../../../reproductions/2504.10507-pinrec/">实现解读</a> · <a href="#qa-9ee1c6eb0e5343e2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pinrec" data-paper-title="PinRec: Outcome-Conditioned, Multi-Token Generative Retrieval for Industry-Scale Recommendation Systems" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="PinRec: Outcome-Conditioned, Multi-Token Generative Retrieval for Industry-Scale Recommendation Systems 搜广推与 LLM 应用 Pinterest 2025-04-09 普通 next-item 只会延续用户最常见行为，且严格顺序不适合 feed session。PinRec 把期望 outcome 注入输出头，并在同一未来窗口一次生成多个 ANN-compatible item vectors。 Fidelity: 完整核心链路复现。真实执行因果 decoder、outcome embedding、归一化 ANN 输出、无序未来窗口 multi-token 对比学习；MovieLens 评分档位替代 Pinterest 多 surface action。本地对照口径：基线是 unconditioned next-token 模型；实验组是 outcome-conditioned 三 token window；Unordered Recall@10 -27.78%、NDCG@10 -34.82%。这是 outcome/multi-token 模块消融，不是相对 DIN。  generative-retrieval outcome-conditioning multi-token 搜广推 生成式召回与推理推荐 PinRec 的多个 ANN-compatible 输出为什么要逐头归一并处理重复物品？ 各输出向量需在索引相同空间与尺度内检索，逐头归一避免范数差异支配，相同物品可被多头取回需按定义去重或合并。目标匹配与窗口正例身份一致。重复多个相同向量不能因为头数多就算已学到多兴趣。 示意：三头都检回同一热门相机，看似产生三份候选其实覆盖一件；应统计去重后的命中与兴趣差异，而非只数模型输出了三条向量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d2ba63933a870c32">PinRec 的多个 ANN-compatible 输出为什么要逐头归一并处理重复物品？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apinrec">PinRec: Outcome-Conditioned, Multi-Token Generative Retrieval for Industry-Scale Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>各输出向量需在索引相同空间与尺度内检索，逐头归一避免范数差异支配，相同物品可被多头取回需按定义去重或合并。目标匹配与窗口正例身份一致。重复多个相同向量不能因为头数多就算已学到多兴趣。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三头都检回同一热门相机，看似产生三份候选其实覆盖一件；应统计去重后的命中与兴趣差异，而非只数模型输出了三条向量。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.10507">原论文</a> · <a href="../../../../reproductions/2504.10507-pinrec/">实现解读</a> · <a href="#qa-d2ba63933a870c32">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cobra" data-paper-title="Sparse Meets Dense: Unified Generative Recommendations with Cascaded Sparse-Dense Representations" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Sparse Meets Dense: Unified Generative Recommendations with Cascaded Sparse-Dense Representations 搜广推与 LLM 应用 Baidu 2025-03-04 纯 Semantic ID 在量化阶段丢失细粒度信息。COBRA 先生成稀疏 code，再以 code 条件生成可端到端更新的 dense vector；推理先 beam 搜索 code，再用 dense 最近邻细排。 Fidelity: 完整核心链路复现。稀疏 S-ID、以 S-ID 为条件的稠密向量、联合训练和 coarse-to-fine BeamFusion 均执行；生产 ANN 服务未复刻。本地对照口径：统一跨模型基线是 DIN，COBRA NDCG@10 相对 DIN +25.75%；内部 sparse-only 基线加入 dense cascade 后 +45.83%。两项提升不能相互替代。180 users/280 items、seeds 42–44。统一 DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；  generative-retrieval semantic-id dense-retrieval 搜广推 生成式召回与推理推荐 COBRA 的 sparse code 与 dense vector 为什么分两阶段生成？ 离散码先定位语义区域，后续条件向量在该区域内保留细粒度差别，弥补量化损失。检索先用 beam 选码，再以条件向量近邻细排，把离散结构与连续精度结合。第二阶段仍受第一阶段覆盖限制，不能恢复未被选入任何区域的目标。 示意：先定位“科幻电影”，再用连续向量区分硬科幻与动作科幻；如果首层误选家庭喜剧，细排再精确也可能找不到目标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-cobra-75daff60" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-fe2b493774ecc359">COBRA 的 sparse code 与 dense vector 为什么分两阶段生成？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acobra">Sparse Meets Dense: Unified Generative Recommendations with Cascaded Sparse-Dense Representations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Baidu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>离散码先定位语义区域，后续条件向量在该区域内保留细粒度差别，弥补量化损失。检索先用 beam 选码，再以条件向量近邻细排，把离散结构与连续精度结合。第二阶段仍受第一阶段覆盖限制，不能恢复未被选入任何区域的目标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先定位“科幻电影”，再用连续向量区分硬科幻与动作科幻；如果首层误选家庭喜剧，细排再精确也可能找不到目标。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2503.02453">原论文</a> · <a href="../../../../reproductions/2503.02453-cobra/">实现解读</a> · <a href="#qa-fe2b493774ecc359">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cobra" data-paper-title="Sparse Meets Dense: Unified Generative Recommendations with Cascaded Sparse-Dense Representations" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Sparse Meets Dense: Unified Generative Recommendations with Cascaded Sparse-Dense Representations 搜广推与 LLM 应用 Baidu 2025-03-04 纯 Semantic ID 在量化阶段丢失细粒度信息。COBRA 先生成稀疏 code，再以 code 条件生成可端到端更新的 dense vector；推理先 beam 搜索 code，再用 dense 最近邻细排。 Fidelity: 完整核心链路复现。稀疏 S-ID、以 S-ID 为条件的稠密向量、联合训练和 coarse-to-fine BeamFusion 均执行；生产 ANN 服务未复刻。本地对照口径：统一跨模型基线是 DIN，COBRA NDCG@10 相对 DIN +25.75%；内部 sparse-only 基线加入 dense cascade 后 +45.83%。两项提升不能相互替代。180 users/280 items、seeds 42–44。统一 DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；  generative-retrieval semantic-id dense-retrieval 搜广推 生成式召回与推理推荐 COBRA已经生成了稀疏SID，为什么还要按SID条件生成稠密向量？ 语义量化保留粗结构，却会丢失码内的细节。COBRA先用离散路径缩小搜索范围，再让用户上下文与该路径共同产生稠密查询，区分共享粗码的物品；稀疏与稠密目标联合训练以减少接口错位。后级细排只能区分前级保留的候选，无法保证找回已被beam排除的正确路径。 示意：粗码先选中运动鞋，条件稠密向量再区分越野鞋与公路鞋；若第一步误去了家电分支，第二步再精细也难把正确鞋款补回来。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-fc61d6dcbcc97925">COBRA已经生成了稀疏SID，为什么还要按SID条件生成稠密向量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acobra">Sparse Meets Dense: Unified Generative Recommendations with Cascaded Sparse-Dense Representations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Baidu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语义量化保留粗结构，却会丢失码内的细节。COBRA先用离散路径缩小搜索范围，再让用户上下文与该路径共同产生稠密查询，区分共享粗码的物品；稀疏与稠密目标联合训练以减少接口错位。后级细排只能区分前级保留的候选，无法保证找回已被beam排除的正确路径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>粗码先选中运动鞋，条件稠密向量再区分越野鞋与公路鞋；若第一步误去了家电分支，第二步再精细也难把正确鞋款补回来。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2503.02453">原论文</a> · <a href="../../../../reproductions/2503.02453-cobra/">实现解读</a> · <a href="#qa-fc61d6dcbcc97925">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cobra" data-paper-title="Sparse Meets Dense: Unified Generative Recommendations with Cascaded Sparse-Dense Representations" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Sparse Meets Dense: Unified Generative Recommendations with Cascaded Sparse-Dense Representations 搜广推与 LLM 应用 Baidu 2025-03-04 纯 Semantic ID 在量化阶段丢失细粒度信息。COBRA 先生成稀疏 code，再以 code 条件生成可端到端更新的 dense vector；推理先 beam 搜索 code，再用 dense 最近邻细排。 Fidelity: 完整核心链路复现。稀疏 S-ID、以 S-ID 为条件的稠密向量、联合训练和 coarse-to-fine BeamFusion 均执行；生产 ANN 服务未复刻。本地对照口径：统一跨模型基线是 DIN，COBRA NDCG@10 相对 DIN +25.75%；内部 sparse-only 基线加入 dense cascade 后 +45.83%。两项提升不能相互替代。180 users/280 items、seeds 42–44。统一 DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；  generative-retrieval semantic-id dense-retrieval 搜广推 生成式召回与推理推荐 COBRA 与纯连续双塔、纯 SID 生成相比，分别借用了哪部分能力？ 连续双塔易对接 ANN 但通常把用户压成较少向量，纯 SID 可分层生成却有量化误差。COBRA 用码提供多区域提名，条件向量提供区域内细分。级联增加模块与校准成本，来源的内部 sparse-only 消融与跨 DIN 比较回答不同问题，不能互相替代。 示意：用户有摄影和烘焙两种兴趣，beam 先取两类码，分别生成细向量检索；相较只输出一个平均向量，区域划分更明确，但要维护两级得分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a4f74f5dbf88f5b3">COBRA 与纯连续双塔、纯 SID 生成相比，分别借用了哪部分能力？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acobra">Sparse Meets Dense: Unified Generative Recommendations with Cascaded Sparse-Dense Representations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Baidu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>连续双塔易对接 ANN 但通常把用户压成较少向量，纯 SID 可分层生成却有量化误差。COBRA 用码提供多区域提名，条件向量提供区域内细分。级联增加模块与校准成本，来源的内部 sparse-only 消融与跨 DIN 比较回答不同问题，不能互相替代。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户有摄影和烘焙两种兴趣，beam 先取两类码，分别生成细向量检索；相较只输出一个平均向量，区域划分更明确，但要维护两级得分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2503.02453">原论文</a> · <a href="../../../../reproductions/2503.02453-cobra/">实现解读</a> · <a href="#qa-a4f74f5dbf88f5b3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cobra" data-paper-title="Sparse Meets Dense: Unified Generative Recommendations with Cascaded Sparse-Dense Representations" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Sparse Meets Dense: Unified Generative Recommendations with Cascaded Sparse-Dense Representations 搜广推与 LLM 应用 Baidu 2025-03-04 纯 Semantic ID 在量化阶段丢失细粒度信息。COBRA 先生成稀疏 code，再以 code 条件生成可端到端更新的 dense vector；推理先 beam 搜索 code，再用 dense 最近邻细排。 Fidelity: 完整核心链路复现。稀疏 S-ID、以 S-ID 为条件的稠密向量、联合训练和 coarse-to-fine BeamFusion 均执行；生产 ANN 服务未复刻。本地对照口径：统一跨模型基线是 DIN，COBRA NDCG@10 相对 DIN +25.75%；内部 sparse-only 基线加入 dense cascade 后 +45.83%。两项提升不能相互替代。180 users/280 items、seeds 42–44。统一 DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；  generative-retrieval semantic-id dense-retrieval 搜广推 生成式召回与推理推荐 COBRA 推理时为什么要保留 code 的 beam 分与条件向量点积分，而不只看后者？ 点积分衡量所选码条件下的物品匹配，beam 分保留该语义路径本身的先验可信度，两者组合才能跨码比较。系数需要统一尺度与验证选择，不能把各码局部最高分当作同等可信。训练 dense loss 也应真实更新条件向量，不以固定打分混合替代。 示意：一条低概率码中有很高局部点积，另一条高概率码局部分数稍低；丢掉路径分会使前者无条件胜出，改变级联模型的原始判断。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-889c431918417b06">COBRA 推理时为什么要保留 code 的 beam 分与条件向量点积分，而不只看后者？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acobra">Sparse Meets Dense: Unified Generative Recommendations with Cascaded Sparse-Dense Representations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Baidu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>点积分衡量所选码条件下的物品匹配，beam 分保留该语义路径本身的先验可信度，两者组合才能跨码比较。系数需要统一尺度与验证选择，不能把各码局部最高分当作同等可信。训练 dense loss 也应真实更新条件向量，不以固定打分混合替代。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一条低概率码中有很高局部点积，另一条高概率码局部分数稍低；丢掉路径分会使前者无条件胜出，改变级联模型的原始判断。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2503.02453">原论文</a> · <a href="../../../../reproductions/2503.02453-cobra/">实现解读</a> · <a href="#qa-889c431918417b06">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onerec" data-paper-title="OneRec: Unifying Retrieve and Rank with Generative Recommender and Iterative Preference Alignment" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneRec: Unifying Retrieve and Rank with Generative Recommender and Iterative Preference Alignment 搜广推与 LLM 应用 Kuaishou 2025-02-26 传统 retrieve→rank 多阶段系统目标割裂；已有生成式召回又多为 point-wise next-item generation，难以保证一个推荐 session 内的连贯性与多样性。OneRec 用三层 RQ Semantic ID 表示物品，以 MoE 模型一次生成 5 个目标物品的完整 session，并训练个性化 reward model 预测 watch/interaction 指标。 Fidelity: 完整核心链路复现。当前代码实际训练 RQ Semantic IDs、session-wise encoder-decoder、稀疏 MoE、个性化 reward model 和 self-hard DPO；仅缩小模型、session 长度和公开数据规模。本地对照口径：基线是 Session Generator SFT；实验组是 reward model+self-hard DPO 后的 OneRec；NDCG@10 从 0.01565 降至 0（-100%）。这是 preference alignment 阶段消融，不是 OneRec 相对 DIN 的结果。   搜广推 生成式召回与推理推荐 OneRec 为什么将多个 item 的 SID 串成 session 自回归目标？ 单 item 生成不直接看到同组搭配，session 目标让后面的物品受前面已选内容影响，可学习连贯与重复取舍。层级 SID 提供可组合地址，reward model 再评价整组。完整 session 不是一个无顺序集合，也不自动保证多样性。 示意：先放基础摄影教程，后面可接进阶实操；若三条都独立生成，可能重复选三份入门教程，单条相关却缺少整体进展。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-onerec-bec96f9e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7150d36b246b8f85">OneRec 为什么将多个 item 的 SID 串成 session 自回归目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonerec">OneRec: Unifying Retrieve and Rank with Generative Recommender and Iterative Preference Alignment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单 item 生成不直接看到同组搭配，session 目标让后面的物品受前面已选内容影响，可学习连贯与重复取舍。层级 SID 提供可组合地址，reward model 再评价整组。完整 session 不是一个无顺序集合，也不自动保证多样性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先放基础摄影教程，后面可接进阶实操；若三条都独立生成，可能重复选三份入门教程，单条相关却缺少整体进展。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.18965">原论文</a> · <a href="../../../../reproductions/2502.18965-onerec/">实现解读</a> · <a href="#qa-7150d36b246b8f85">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onerec" data-paper-title="OneRec: Unifying Retrieve and Rank with Generative Recommender and Iterative Preference Alignment" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneRec: Unifying Retrieve and Rank with Generative Recommender and Iterative Preference Alignment 搜广推与 LLM 应用 Kuaishou 2025-02-26 传统 retrieve→rank 多阶段系统目标割裂；已有生成式召回又多为 point-wise next-item generation，难以保证一个推荐 session 内的连贯性与多样性。OneRec 用三层 RQ Semantic ID 表示物品，以 MoE 模型一次生成 5 个目标物品的完整 session，并训练个性化 reward model 预测 watch/interaction 指标。 Fidelity: 完整核心链路复现。当前代码实际训练 RQ Semantic IDs、session-wise encoder-decoder、稀疏 MoE、个性化 reward model 和 self-hard DPO；仅缩小模型、session 长度和公开数据规模。本地对照口径：基线是 Session Generator SFT；实验组是 reward model+self-hard DPO 后的 OneRec；NDCG@10 从 0.01565 降至 0（-100%）。这是 preference alignment 阶段消融，不是 OneRec 相对 DIN 的结果。   搜广推 生成式召回与推理推荐 OneRec 为什么从当前模型生成的完整 session 中选 self-hard 胜负对，而不是逐个物品做偏好训练？ 完整 session 把项目之间的连贯性与多样性纳入同一生成对象，奖励模型也据此评价整段推荐。当前模型产生的较难区分胜负对，能把偏好更新集中到模型实际容易混淆的方案上；DPO 比较胜负 session 相对参考模型的概率变化。奖励误差仍会影响方向，本地小规模结果也没有验证线上收益。 示意：两组五条视频都单条相关，但一组内容重复，另一组节奏更连贯。把整组作为胜负对象，模型才有机会学到“这几条放在一起更合适”，而非只提升某条视频概率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-4d76f811142e31ca">OneRec 为什么从当前模型生成的完整 session 中选 self-hard 胜负对，而不是逐个物品做偏好训练？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonerec">OneRec: Unifying Retrieve and Rank with Generative Recommender and Iterative Preference Alignment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>完整 session 把项目之间的连贯性与多样性纳入同一生成对象，奖励模型也据此评价整段推荐。当前模型产生的较难区分胜负对，能把偏好更新集中到模型实际容易混淆的方案上；DPO 比较胜负 session 相对参考模型的概率变化。奖励误差仍会影响方向，本地小规模结果也没有验证线上收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两组五条视频都单条相关，但一组内容重复，另一组节奏更连贯。把整组作为胜负对象，模型才有机会学到“这几条放在一起更合适”，而非只提升某条视频概率。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.18965">原论文</a> · <a href="../../../../reproductions/2502.18965-onerec/">实现解读</a> · <a href="#qa-4d76f811142e31ca">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onerec" data-paper-title="OneRec: Unifying Retrieve and Rank with Generative Recommender and Iterative Preference Alignment" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneRec: Unifying Retrieve and Rank with Generative Recommender and Iterative Preference Alignment 搜广推与 LLM 应用 Kuaishou 2025-02-26 传统 retrieve→rank 多阶段系统目标割裂；已有生成式召回又多为 point-wise next-item generation，难以保证一个推荐 session 内的连贯性与多样性。OneRec 用三层 RQ Semantic ID 表示物品，以 MoE 模型一次生成 5 个目标物品的完整 session，并训练个性化 reward model 预测 watch/interaction 指标。 Fidelity: 完整核心链路复现。当前代码实际训练 RQ Semantic IDs、session-wise encoder-decoder、稀疏 MoE、个性化 reward model 和 self-hard DPO；仅缩小模型、session 长度和公开数据规模。本地对照口径：基线是 Session Generator SFT；实验组是 reward model+self-hard DPO 后的 OneRec；NDCG@10 从 0.01565 降至 0（-100%）。这是 preference alignment 阶段消融，不是 OneRec 相对 DIN 的结果。   搜广推 生成式召回与推理推荐 OneRec 的 self-hard DPO 与仅加宽 beam，改变的是模型还是搜索？ 加宽 beam 只探索现有分布，DPO 利用当前生成 session 的胜负改变策略概率，属于训练更新。奖励模型弱时更新也可把质量拉坏，来源本地 DPO loss 迅速下降而 NDCG 归零，说明偏好拟合不等于推荐进步。 示意：搜索更多清单可找到好例子，但若训练把错误 judge 选出的清单强化，后续分布会更糟；loss 小不能替代真实排序验证。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-67abd43b2287aa84">OneRec 的 self-hard DPO 与仅加宽 beam，改变的是模型还是搜索？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonerec">OneRec: Unifying Retrieve and Rank with Generative Recommender and Iterative Preference Alignment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>加宽 beam 只探索现有分布，DPO 利用当前生成 session 的胜负改变策略概率，属于训练更新。奖励模型弱时更新也可把质量拉坏，来源本地 DPO loss 迅速下降而 NDCG 归零，说明偏好拟合不等于推荐进步。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>搜索更多清单可找到好例子，但若训练把错误 judge 选出的清单强化，后续分布会更糟；loss 小不能替代真实排序验证。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.18965">原论文</a> · <a href="../../../../reproductions/2502.18965-onerec/">实现解读</a> · <a href="#qa-67abd43b2287aa84">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onerec" data-paper-title="OneRec: Unifying Retrieve and Rank with Generative Recommender and Iterative Preference Alignment" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneRec: Unifying Retrieve and Rank with Generative Recommender and Iterative Preference Alignment 搜广推与 LLM 应用 Kuaishou 2025-02-26 传统 retrieve→rank 多阶段系统目标割裂；已有生成式召回又多为 point-wise next-item generation，难以保证一个推荐 session 内的连贯性与多样性。OneRec 用三层 RQ Semantic ID 表示物品，以 MoE 模型一次生成 5 个目标物品的完整 session，并训练个性化 reward model 预测 watch/interaction 指标。 Fidelity: 完整核心链路复现。当前代码实际训练 RQ Semantic IDs、session-wise encoder-decoder、稀疏 MoE、个性化 reward model 和 self-hard DPO；仅缩小模型、session 长度和公开数据规模。本地对照口径：基线是 Session Generator SFT；实验组是 reward model+self-hard DPO 后的 OneRec；NDCG@10 从 0.01565 降至 0（-100%）。这是 preference alignment 阶段消融，不是 OneRec 相对 DIN 的结果。   搜广推 生成式召回与推理推荐 OneRec 合法 SID 前缀约束为什么不能修复语义碰撞带来的全部身份问题？ 约束只保证路径在 catalog 中存在，多物品同码仍需明确展开或区分，唯一率不足可能影响评估。胜负 session 应来自当前模型而非注入 gold。目录合法、奖励有效与排序质量是三项不同检查，本地负结果不可被通过合法性覆盖。 示意：两个电影共用一串码，beam 合法也未确定是哪部；若测试先挑正确电影展开，就会用答案替模型消除碰撞。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a714ac3bdc5c99bd">OneRec 合法 SID 前缀约束为什么不能修复语义碰撞带来的全部身份问题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonerec">OneRec: Unifying Retrieve and Rank with Generative Recommender and Iterative Preference Alignment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>约束只保证路径在 catalog 中存在，多物品同码仍需明确展开或区分，唯一率不足可能影响评估。胜负 session 应来自当前模型而非注入 gold。目录合法、奖励有效与排序质量是三项不同检查，本地负结果不可被通过合法性覆盖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个电影共用一串码，beam 合法也未确定是哪部；若测试先挑正确电影展开，就会用答案替模型消除碰撞。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.18965">原论文</a> · <a href="../../../../reproductions/2502.18965-onerec/">实现解读</a> · <a href="#qa-a714ac3bdc5c99bd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sessionrec" data-paper-title="SessionRec: Next Session Prediction Paradigm For Generative Sequential Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="SessionRec: Next Session Prediction Paradigm For Generative Sequential Recommendation 搜广推与 LLM 应用 Meituan 2025-02-14 逐物品 next-item 训练把同一消费意图中的多个物品硬排成先后标签，也无法把“下一次访问会同时消费的一组物品”作为多正例。SessionRec 先由 Item-based Session Encoder（ISE）把一次访问中的物品聚合为 session token，再由 Session-based Sequence Encoder（SSE）建模跨 session 兴趣迁移，最终让一个 query 同时召回下一 session 的所有正例。 Fidelity: 核心机制复现。真实执行 session 内聚合、session 间 Transformer、多正例 next-session retrieval，以及 session 内曝光负例排序损失；私有特征与 ANN 服务未复刻。本地对照口径：基线是等预算的扁平 Item Transformer；实验组是 SessionRec Transformer；NDCG@20 从 0.004718 降至 0.003678（-22.05%）。这是 session 建模消融；DIN 未在 KuaiRand session 任务中参与比较。  session recommendation generative retrieval 搜广推 生成式召回与推理推荐 SessionRec中的session token是一件商品，还是同次访问的一组物品表示？ 它由会话内多个物品经ISE聚合得到，代表一次访问，再交给SSE建模会话间迁移。下一session也可能包含多条正反馈，不是给每个token重新取一个商品ID。先分清物品级与会话级单位，才能读懂多正例目标。 教学例子：一次访问看了甲乙丙，可先聚成一个session表示；下一次访问的丁戊仍可以共同成为目标集合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-sessionrec-2fd19641" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-1fad52275cdd3908">SessionRec中的session token是一件商品，还是同次访问的一组物品表示？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asessionrec">SessionRec: Next Session Prediction Paradigm For Generative Sequential Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它由会话内多个物品经ISE聚合得到，代表一次访问，再交给SSE建模会话间迁移。下一session也可能包含多条正反馈，不是给每个token重新取一个商品ID。先分清物品级与会话级单位，才能读懂多正例目标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次访问看了甲乙丙，可先聚成一个session表示；下一次访问的丁戊仍可以共同成为目标集合。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.10157">原论文</a> · <a href="../../../../reproductions/2502.10157-sessionrec/">实现解读</a> · <a href="#qa-1fad52275cdd3908">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sessionrec" data-paper-title="SessionRec: Next Session Prediction Paradigm For Generative Sequential Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="SessionRec: Next Session Prediction Paradigm For Generative Sequential Recommendation 搜广推与 LLM 应用 Meituan 2025-02-14 逐物品 next-item 训练把同一消费意图中的多个物品硬排成先后标签，也无法把“下一次访问会同时消费的一组物品”作为多正例。SessionRec 先由 Item-based Session Encoder（ISE）把一次访问中的物品聚合为 session token，再由 Session-based Sequence Encoder（SSE）建模跨 session 兴趣迁移，最终让一个 query 同时召回下一 session 的所有正例。 Fidelity: 核心机制复现。真实执行 session 内聚合、session 间 Transformer、多正例 next-session retrieval，以及 session 内曝光负例排序损失；私有特征与 ANN 服务未复刻。本地对照口径：基线是等预算的扁平 Item Transformer；实验组是 SessionRec Transformer；NDCG@20 从 0.004718 降至 0.003678（-22.05%）。这是 session 建模消融；DIN 未在 KuaiRand session 任务中参与比较。  session recommendation generative retrieval 搜广推 生成式召回与推理推荐 SessionRec 为什么先把一次访问聚成 session token，再预测下一 session 的多正例？ 同次访问的多个物品常共享一个意图，逐物品训练会把它们硬排成唯一先后关系。ISE 先聚合会话内部内容，SSE 再学习会话之间的兴趣迁移，目标将下一会话全部正反馈作为正例，并利用真实未点击曝光区分难负例。它改变了监督单位，不是单纯缩短序列；会话划分错误也可能混合不同意图。 示意：一次访问同时看帐篷、睡袋和防潮垫，下一次访问关注徒步鞋。先用一个会话 token 表达露营采购，再预测下一组需求，比认定“睡袋后唯一应看防潮垫”更贴近组消费。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-9400ea46fb6842b9">SessionRec 为什么先把一次访问聚成 session token，再预测下一 session 的多正例？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asessionrec">SessionRec: Next Session Prediction Paradigm For Generative Sequential Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同次访问的多个物品常共享一个意图，逐物品训练会把它们硬排成唯一先后关系。ISE 先聚合会话内部内容，SSE 再学习会话之间的兴趣迁移，目标将下一会话全部正反馈作为正例，并利用真实未点击曝光区分难负例。它改变了监督单位，不是单纯缩短序列；会话划分错误也可能混合不同意图。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次访问同时看帐篷、睡袋和防潮垫，下一次访问关注徒步鞋。先用一个会话 token 表达露营采购，再预测下一组需求，比认定“睡袋后唯一应看防潮垫”更贴近组消费。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.10157">原论文</a> · <a href="../../../../reproductions/2502.10157-sessionrec/">实现解读</a> · <a href="#qa-9400ea46fb6842b9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sessionrec" data-paper-title="SessionRec: Next Session Prediction Paradigm For Generative Sequential Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="SessionRec: Next Session Prediction Paradigm For Generative Sequential Recommendation 搜广推与 LLM 应用 Meituan 2025-02-14 逐物品 next-item 训练把同一消费意图中的多个物品硬排成先后标签，也无法把“下一次访问会同时消费的一组物品”作为多正例。SessionRec 先由 Item-based Session Encoder（ISE）把一次访问中的物品聚合为 session token，再由 Session-based Sequence Encoder（SSE）建模跨 session 兴趣迁移，最终让一个 query 同时召回下一 session 的所有正例。 Fidelity: 核心机制复现。真实执行 session 内聚合、session 间 Transformer、多正例 next-session retrieval，以及 session 内曝光负例排序损失；私有特征与 ANN 服务未复刻。本地对照口径：基线是等预算的扁平 Item Transformer；实验组是 SessionRec Transformer；NDCG@20 从 0.004718 降至 0.003678（-22.05%）。这是 session 建模消融；DIN 未在 KuaiRand session 任务中参与比较。  session recommendation generative retrieval 搜广推 生成式召回与推理推荐 SessionRec的ISE与SSE分别处理哪种顺序？ ISE聚合会话内物品，SSE处理会话间时间迁移；均值ISE弱化会话内先后，不能说整个模型无顺序。SSE可用Transformer或HSTU，不限定一个骨干。 例如午间与晚间两会话次序重要，午间同意图几次浏览未必需强行排序。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-3e0685c171309fa7">SessionRec的ISE与SSE分别处理哪种顺序？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asessionrec">SessionRec: Next Session Prediction Paradigm For Generative Sequential Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>ISE聚合会话内物品，SSE处理会话间时间迁移；均值ISE弱化会话内先后，不能说整个模型无顺序。SSE可用Transformer或HSTU，不限定一个骨干。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如午间与晚间两会话次序重要，午间同意图几次浏览未必需强行排序。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.10157">原论文</a> · <a href="../../../../reproductions/2502.10157-sessionrec/">实现解读</a> · <a href="#qa-3e0685c171309fa7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sessionrec" data-paper-title="SessionRec: Next Session Prediction Paradigm For Generative Sequential Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="SessionRec: Next Session Prediction Paradigm For Generative Sequential Recommendation 搜广推与 LLM 应用 Meituan 2025-02-14 逐物品 next-item 训练把同一消费意图中的多个物品硬排成先后标签，也无法把“下一次访问会同时消费的一组物品”作为多正例。SessionRec 先由 Item-based Session Encoder（ISE）把一次访问中的物品聚合为 session token，再由 Session-based Sequence Encoder（SSE）建模跨 session 兴趣迁移，最终让一个 query 同时召回下一 session 的所有正例。 Fidelity: 核心机制复现。真实执行 session 内聚合、session 间 Transformer、多正例 next-session retrieval，以及 session 内曝光负例排序损失；私有特征与 ANN 服务未复刻。本地对照口径：基线是等预算的扁平 Item Transformer；实验组是 SessionRec Transformer；NDCG@20 从 0.004718 降至 0.003678（-22.05%）。这是 session 建模消融；DIN 未在 KuaiRand session 任务中参与比较。  session recommendation generative retrieval 搜广推 生成式召回与推理推荐 SessionRec困难负例可以从全库随机补成未点击曝光吗？ 不可以，困难负例来自同session真实曝光未点击。当前训练轮采正例做CE但评估保留完整集合，不能把轮采一个误报成只剩单正例任务。 例如没展示过的电影不能伪标为用户看见却拒绝。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8fa08745cf9658a9">SessionRec困难负例可以从全库随机补成未点击曝光吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asessionrec">SessionRec: Next Session Prediction Paradigm For Generative Sequential Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不可以，困难负例来自同session真实曝光未点击。当前训练轮采正例做CE但评估保留完整集合，不能把轮采一个误报成只剩单正例任务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如没展示过的电影不能伪标为用户看见却拒绝。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.10157">原论文</a> · <a href="../../../../reproductions/2502.10157-sessionrec/">实现解读</a> · <a href="#qa-8fa08745cf9658a9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:leadre" data-paper-title="LEADRE: Multi-Faceted Knowledge Enhanced LLM Empowered Display Advertisement Recommender System" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="LEADRE: Multi-Faceted Knowledge Enhanced LLM Empowered Display Advertisement Recommender System 搜广推与 LLM 应用 Tencent / WeChat 2024-11-21 ID 召回难利用广告内容。LEADRE 以跨域行为、长期总结和实时行为构造 intent-aware prompt，将广告量化为 S-ID，并用广告语义/商业价值辅助任务和 DPO 对齐，线上把长期生成缓存与实时服务组合。 Fidelity: 完整核心链路复现。Semantic ID、长短期/商业意图、语义与价值辅助任务、SFT→DPO 和可缓存/实时双路径均执行；私有广告与生产服务未复刻。本地对照口径：统一跨模型基线是 DIN，LEADRE NDCG@10 相对 DIN +12.94%；内部基线是 S-ID 多任务 SFT，继续 DPO 后 -4.53%。主结论与对齐阶段消融分开报告。MovieLens-100K，180 users/280 items，seeds 42–44。统一 DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；  llm-recommendation generative-retrieval advertising preference-alignment 搜广推 生成式召回与推理推荐 LEADRE 的 intent-aware prompt 为什么组合跨域、长期总结和实时行为？ 跨域提供本广告域缺少的线索，长期总结保留稳定兴趣，实时行为反映当前变化，多源意图使 S-ID 生成不只记广告编号。总结和缓存都有时效损失，来源不同也可能冲突，不能把它们拼长就当作完整理解用户。 示意：长期摄影偏好、最近旅行搜索和当前相机浏览可共同支持便携装备广告；若只看本域点击，新广告可能没有任何可用连接。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-leadre-72cfaef2" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9a2a5492b043376d">LEADRE 的 intent-aware prompt 为什么组合跨域、长期总结和实时行为？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aleadre">LEADRE: Multi-Faceted Knowledge Enhanced LLM Empowered Display Advertisement Recommender System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent / WeChat</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>跨域提供本广告域缺少的线索，长期总结保留稳定兴趣，实时行为反映当前变化，多源意图使 S-ID 生成不只记广告编号。总结和缓存都有时效损失，来源不同也可能冲突，不能把它们拼长就当作完整理解用户。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>长期摄影偏好、最近旅行搜索和当前相机浏览可共同支持便携装备广告；若只看本域点击，新广告可能没有任何可用连接。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2411.13789">原论文</a> · <a href="../../../../reproductions/2411.13789-leadre/">实现解读</a> · <a href="#qa-9a2a5492b043376d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:leadre" data-paper-title="LEADRE: Multi-Faceted Knowledge Enhanced LLM Empowered Display Advertisement Recommender System" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="LEADRE: Multi-Faceted Knowledge Enhanced LLM Empowered Display Advertisement Recommender System 搜广推与 LLM 应用 Tencent / WeChat 2024-11-21 ID 召回难利用广告内容。LEADRE 以跨域行为、长期总结和实时行为构造 intent-aware prompt，将广告量化为 S-ID，并用广告语义/商业价值辅助任务和 DPO 对齐，线上把长期生成缓存与实时服务组合。 Fidelity: 完整核心链路复现。Semantic ID、长短期/商业意图、语义与价值辅助任务、SFT→DPO 和可缓存/实时双路径均执行；私有广告与生产服务未复刻。本地对照口径：统一跨模型基线是 DIN，LEADRE NDCG@10 相对 DIN +12.94%；内部基线是 S-ID 多任务 SFT，继续 DPO 后 -4.53%。主结论与对齐阶段消融分开报告。MovieLens-100K，180 users/280 items，seeds 42–44。统一 DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；  llm-recommendation generative-retrieval advertising preference-alignment 搜广推 生成式召回与推理推荐 LEADRE为什么用意图prompt、语义辅助任务和DPO共同训练广告SID生成？ 单独预测离散码可能只记住曝光ID，难利用广告内容与跨域需求。意图prompt整理长期与实时信号，语义和商业价值目标赋予码更明确的推荐含义，DPO再调整偏好取舍。偏好优化不保证每项检索指标都提高，内部SFT到DPO的变化应单独报告，而非借整体模型对另一基线的提升遮盖。 示意：同属家电类的两个广告可能一个符合当前装修意图、另一个只是高频曝光；语义与价值监督帮助区分，但DPO过度偏商业反馈也可能损害新增相关候选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-cbbfe12497e2d087">LEADRE为什么用意图prompt、语义辅助任务和DPO共同训练广告SID生成？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aleadre">LEADRE: Multi-Faceted Knowledge Enhanced LLM Empowered Display Advertisement Recommender System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent / WeChat</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单独预测离散码可能只记住曝光ID，难利用广告内容与跨域需求。意图prompt整理长期与实时信号，语义和商业价值目标赋予码更明确的推荐含义，DPO再调整偏好取舍。偏好优化不保证每项检索指标都提高，内部SFT到DPO的变化应单独报告，而非借整体模型对另一基线的提升遮盖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同属家电类的两个广告可能一个符合当前装修意图、另一个只是高频曝光；语义与价值监督帮助区分，但DPO过度偏商业反馈也可能损害新增相关候选。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2411.13789">原论文</a> · <a href="../../../../reproductions/2411.13789-leadre/">实现解读</a> · <a href="#qa-cbbfe12497e2d087">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:leadre" data-paper-title="LEADRE: Multi-Faceted Knowledge Enhanced LLM Empowered Display Advertisement Recommender System" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="LEADRE: Multi-Faceted Knowledge Enhanced LLM Empowered Display Advertisement Recommender System 搜广推与 LLM 应用 Tencent / WeChat 2024-11-21 ID 召回难利用广告内容。LEADRE 以跨域行为、长期总结和实时行为构造 intent-aware prompt，将广告量化为 S-ID，并用广告语义/商业价值辅助任务和 DPO 对齐，线上把长期生成缓存与实时服务组合。 Fidelity: 完整核心链路复现。Semantic ID、长短期/商业意图、语义与价值辅助任务、SFT→DPO 和可缓存/实时双路径均执行；私有广告与生产服务未复刻。本地对照口径：统一跨模型基线是 DIN，LEADRE NDCG@10 相对 DIN +12.94%；内部基线是 S-ID 多任务 SFT，继续 DPO 后 -4.53%。主结论与对齐阶段消融分开报告。MovieLens-100K，180 users/280 items，seeds 42–44。统一 DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；  llm-recommendation generative-retrieval advertising preference-alignment 搜广推 生成式召回与推理推荐 LEADRE 的完整系统与 DPO 阶段消融，为什么可能一个正向一个负向？ 完整系统包含 SID、语义与价值辅助任务等多个变化，DPO 对照只检验在同一 SFT 基础上增加偏好更新。整体强于 DIN 不代表每个新增阶段都有效。来源本地 DPO 相对 SFT 退化，收益不能全部归给偏好对齐。 示意：先预训带来大收益，随后 DPO 损失一部分，最终仍高于弱基线；只报最终比较会让读者错以为 DPO 也已被验证。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1e6da910e42ba711">LEADRE 的完整系统与 DPO 阶段消融，为什么可能一个正向一个负向？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aleadre">LEADRE: Multi-Faceted Knowledge Enhanced LLM Empowered Display Advertisement Recommender System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent / WeChat</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>完整系统包含 SID、语义与价值辅助任务等多个变化，DPO 对照只检验在同一 SFT 基础上增加偏好更新。整体强于 DIN 不代表每个新增阶段都有效。来源本地 DPO 相对 SFT 退化，收益不能全部归给偏好对齐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先预训带来大收益，随后 DPO 损失一部分，最终仍高于弱基线；只报最终比较会让读者错以为 DPO 也已被验证。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2411.13789">原论文</a> · <a href="../../../../reproductions/2411.13789-leadre/">实现解读</a> · <a href="#qa-1e6da910e42ba711">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:leadre" data-paper-title="LEADRE: Multi-Faceted Knowledge Enhanced LLM Empowered Display Advertisement Recommender System" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="LEADRE: Multi-Faceted Knowledge Enhanced LLM Empowered Display Advertisement Recommender System 搜广推与 LLM 应用 Tencent / WeChat 2024-11-21 ID 召回难利用广告内容。LEADRE 以跨域行为、长期总结和实时行为构造 intent-aware prompt，将广告量化为 S-ID，并用广告语义/商业价值辅助任务和 DPO 对齐，线上把长期生成缓存与实时服务组合。 Fidelity: 完整核心链路复现。Semantic ID、长短期/商业意图、语义与价值辅助任务、SFT→DPO 和可缓存/实时双路径均执行；私有广告与生产服务未复刻。本地对照口径：统一跨模型基线是 DIN，LEADRE NDCG@10 相对 DIN +12.94%；内部基线是 S-ID 多任务 SFT，继续 DPO 后 -4.53%。主结论与对齐阶段消融分开报告。MovieLens-100K，180 users/280 items，seeds 42–44。统一 DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；  llm-recommendation generative-retrieval advertising preference-alignment 搜广推 生成式召回与推理推荐 LEADRE 构造 DPO 胜负广告 SID 时，为什么 reference 与上下文必须固定对应？ 概率差比较同一用户意图下胜负路径相对参考的变化，错用另一请求或不断变化参考会改变目标。SID 合法映射与辅助任务标签应按截止构造，不能由测试答案生成 prompt。长期缓存与实时输入的版本也要一致。 示意：用户甲偏好的广告对不能配用户乙历史计算 reference；两个序列都是合法码也不意味着这份偏好比较仍有意义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-4b755cc139af50ae">LEADRE 构造 DPO 胜负广告 SID 时，为什么 reference 与上下文必须固定对应？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aleadre">LEADRE: Multi-Faceted Knowledge Enhanced LLM Empowered Display Advertisement Recommender System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent / WeChat</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>概率差比较同一用户意图下胜负路径相对参考的变化，错用另一请求或不断变化参考会改变目标。SID 合法映射与辅助任务标签应按截止构造，不能由测试答案生成 prompt。长期缓存与实时输入的版本也要一致。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户甲偏好的广告对不能配用户乙历史计算 reference；两个序列都是合法码也不意味着这份偏好比较仍有意义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2411.13789">原论文</a> · <a href="../../../../reproductions/2411.13789-leadre/">实现解读</a> · <a href="#qa-4b755cc139af50ae">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tiger" data-paper-title="Recommender Systems with Generative Retrieval" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Recommender Systems with Generative Retrieval 搜广推与 LLM 应用 Google / Google DeepMind 2023-05-08 传统召回为每个物品维护独立 ID embedding，难以共享语义，也无法自然生成新物品。TIGER 先把内容向量量化成分层 Semantic ID，再让 encoder-decoder 像生成 token 一样生成下一个物品；同一语义前缀的冲突由额外 token 消解。 保真度：核心机制复现。保真度：核心机制复现。RQ-VAE、残差语义 ID、collision token 和自回归 Transformer 检索链路均实际训练；MovieLens genre 替代 Sentence-T5 商品文本，省略 hashed user token 与 cold-start epsilon mixing。本地对照口径：基线是词表容量和参数量匹配的随机分层 ID 生成器；实验组是 TIGER Semantic ID；NDCG@10 从 0.01043 降至 0.00635（-39.16%）。这是 ID 方案消融，不是相对 DIN 的比较。   搜广推 生成式召回与推理推荐 TIGER为什么把内容量化成多级Semantic ID？ 用短离散序列共享语义并支持自回归生成，避免每物品只作无结构独立类别。内容向量和量化质量仍限制泛化，生成码最终需落到真实有效物品。 例如相近内容可共享前几级码，后几级再区分细节。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-tiger-7436853d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-602316de33d0b529">TIGER为什么把内容量化成多级Semantic ID？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atiger">Recommender Systems with Generative Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用短离散序列共享语义并支持自回归生成，避免每物品只作无结构独立类别。内容向量和量化质量仍限制泛化，生成码最终需落到真实有效物品。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如相近内容可共享前几级码，后几级再区分细节。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.05065">原论文</a> · <a href="../../../../reproductions/2305.05065-tiger/">实现解读</a> · <a href="#qa-602316de33d0b529">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tiger" data-paper-title="Recommender Systems with Generative Retrieval" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Recommender Systems with Generative Retrieval 搜广推与 LLM 应用 Google / Google DeepMind 2023-05-08 传统召回为每个物品维护独立 ID embedding，难以共享语义，也无法自然生成新物品。TIGER 先把内容向量量化成分层 Semantic ID，再让 encoder-decoder 像生成 token 一样生成下一个物品；同一语义前缀的冲突由额外 token 消解。 保真度：核心机制复现。保真度：核心机制复现。RQ-VAE、残差语义 ID、collision token 和自回归 Transformer 检索链路均实际训练；MovieLens genre 替代 Sentence-T5 商品文本，省略 hashed user token 与 cold-start epsilon mixing。本地对照口径：基线是词表容量和参数量匹配的随机分层 ID 生成器；实验组是 TIGER Semantic ID；NDCG@10 从 0.01043 降至 0.00635（-39.16%）。这是 ID 方案消融，不是相对 DIN 的比较。   搜广推 生成式召回与推理推荐 TIGER 的残差量化 SID 为什么比随机分层 ID 更有语义共享能力，还需要碰撞 token？ 残差量化先用粗层中心解释内容向量，再逐层编码剩余误差，因此相近内容有机会共享前缀，生成器可复用粗到细的决策。有限码本仍可能把不同物品映成同一路径，额外碰撞 token 才提供唯一地址。语义共享不保证推荐一定更好，随机分层对照能帮助隔离“有层级”和“层级有语义”的区别。 示意：两本园艺书先共享园艺前缀，后层区分室内种植与户外栽培；若细码仍相同，最后用碰撞码分开，避免生成同一条路径时不知道究竟服务哪本书。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-41bf45ff5bebea3c">TIGER 的残差量化 SID 为什么比随机分层 ID 更有语义共享能力，还需要碰撞 token？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atiger">Recommender Systems with Generative Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>残差量化先用粗层中心解释内容向量，再逐层编码剩余误差，因此相近内容有机会共享前缀，生成器可复用粗到细的决策。有限码本仍可能把不同物品映成同一路径，额外碰撞 token 才提供唯一地址。语义共享不保证推荐一定更好，随机分层对照能帮助隔离“有层级”和“层级有语义”的区别。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两本园艺书先共享园艺前缀，后层区分室内种植与户外栽培；若细码仍相同，最后用碰撞码分开，避免生成同一条路径时不知道究竟服务哪本书。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.05065">原论文</a> · <a href="../../../../reproductions/2305.05065-tiger/">实现解读</a> · <a href="#qa-41bf45ff5bebea3c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tiger" data-paper-title="Recommender Systems with Generative Retrieval" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Recommender Systems with Generative Retrieval 搜广推与 LLM 应用 Google / Google DeepMind 2023-05-08 传统召回为每个物品维护独立 ID embedding，难以共享语义，也无法自然生成新物品。TIGER 先把内容向量量化成分层 Semantic ID，再让 encoder-decoder 像生成 token 一样生成下一个物品；同一语义前缀的冲突由额外 token 消解。 保真度：核心机制复现。保真度：核心机制复现。RQ-VAE、残差语义 ID、collision token 和自回归 Transformer 检索链路均实际训练；MovieLens genre 替代 Sentence-T5 商品文本，省略 hashed user token 与 cold-start epsilon mixing。本地对照口径：基线是词表容量和参数量匹配的随机分层 ID 生成器；实验组是 TIGER Semantic ID；NDCG@10 从 0.01043 降至 0.00635（-39.16%）。这是 ID 方案消融，不是相对 DIN 的比较。   搜广推 生成式召回与推理推荐 额外collision token与语义前缀本身有什么区别？ 语义量化可能让多个物品落同一码，collision token消解身份，不应把任意唯一编号误称新语义层。没有消歧就不能假定一个生成路径唯一对应物品。 例如两个内容很近的视频共享三层码，还需最后标记区分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1e524d9ba84a0a5f">额外collision token与语义前缀本身有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atiger">Recommender Systems with Generative Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语义量化可能让多个物品落同一码，collision token消解身份，不应把任意唯一编号误称新语义层。没有消歧就不能假定一个生成路径唯一对应物品。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个内容很近的视频共享三层码，还需最后标记区分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.05065">原论文</a> · <a href="../../../../reproductions/2305.05065-tiger/">实现解读</a> · <a href="#qa-1e524d9ba84a0a5f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tiger" data-paper-title="Recommender Systems with Generative Retrieval" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Recommender Systems with Generative Retrieval 搜广推与 LLM 应用 Google / Google DeepMind 2023-05-08 传统召回为每个物品维护独立 ID embedding，难以共享语义，也无法自然生成新物品。TIGER 先把内容向量量化成分层 Semantic ID，再让 encoder-decoder 像生成 token 一样生成下一个物品；同一语义前缀的冲突由额外 token 消解。 保真度：核心机制复现。保真度：核心机制复现。RQ-VAE、残差语义 ID、collision token 和自回归 Transformer 检索链路均实际训练；MovieLens genre 替代 Sentence-T5 商品文本，省略 hashed user token 与 cold-start epsilon mixing。本地对照口径：基线是词表容量和参数量匹配的随机分层 ID 生成器；实验组是 TIGER Semantic ID；NDCG@10 从 0.01043 降至 0.00635（-39.16%）。这是 ID 方案消融，不是相对 DIN 的比较。   搜广推 生成式召回与推理推荐 TIGER本地推理得分是融合代理还是有效ID整链概率？ 当前对所有有效物品码逐token logp求和，非外加打分融合；训练与解码需同码本及碰撞映射，不能允许无效路径参与全库排名。 例如少乘一层条件概率，会改变完整item生成概率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-97a2c69cd47c2932">TIGER本地推理得分是融合代理还是有效ID整链概率？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atiger">Recommender Systems with Generative Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>当前对所有有效物品码逐token logp求和，非外加打分融合；训练与解码需同码本及碰撞映射，不能允许无效路径参与全库排名。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如少乘一层条件概率，会改变完整item生成概率。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.05065">原论文</a> · <a href="../../../../reproductions/2305.05065-tiger/">实现解读</a> · <a href="#qa-97a2c69cd47c2932">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

把物品改写成token后，推荐究竟改变了哪一步？

## 记住这一点

生成式召回把候选选择改为在用户上下文下生成物品码：先建立可还原到目录的标识，再学习码序列分布，最后用约束解码得到可服务物品。TIGER串起量化与自回归检索，COBRA进一步级联稀疏码和稠密表示，PLUM把推荐数据继续预训练接到已有语言模型。偏好优化与推理token是在这条链路上改变训练或搜索。

## 一个例子

目录里只有代码(3,7)和(3,9)，模型却给(3,5)很高概率。即使生成文本看起来合理，这也不是有效商品；解码必须服从目录约束。若两个商品共享同一码，还要处理碰撞或保留后续区分路径。

## 什么时候要小心

token loss下降不等于Recall提高，增加beam也不能恢复被错误码本或前缀约束排除的物品。部分论文同时生成列表，归组看主要生成机制，列表价值可接着读重排主题；本地缩小训练不等同于复现生产规模。

## 先读这几篇

按TIGER的离散ID生成→COBRA的稀疏—稠密级联→PLUM的已有LLM继续预训练阅读；这三篇有实际本地核心链路，但TIGER和PLUM的本地结果并未验证最终召回提升。

1. [Recommender Systems with Generative Retrieval](../../../reproductions/2305.05065-tiger/README.md) · [原论文](https://arxiv.org/abs/2305.05065)
2. [Sparse Meets Dense: Unified Generative Recommendations with Cascaded Sparse-Dense Representations](../../../reproductions/2503.02453-cobra/README.md) · [原论文](https://arxiv.org/abs/2503.02453)
3. [PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations](../../../reproductions/2510.07784-plum/README.md) · [原论文](https://arxiv.org/abs/2510.07784)

## 自测一下

模型能生成格式正确的三层SID，为什么仍可能没有有效召回？

??? note "展开参考答案"

    格式正确只保证长度和词表合法；组合可能不在目录中，也可能对应多个物品或错误兴趣。还需检查目录可达性、碰撞消解，以及隔离测试集上的候选覆盖和排序质量。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
