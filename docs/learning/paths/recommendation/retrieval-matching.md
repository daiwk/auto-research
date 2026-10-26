---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 候选生成与搜索匹配

[搜广推](index.md) / 子主题导学 · 约 3 分钟 · 36 张论文卡

## 先想一个问题

精排模型再强，能否找回召回阶段漏掉的好内容？

## 记住这一点

召回先决定哪些物品有机会被精排。双塔把请求和物品分别编码，便于预计算与近邻检索；多兴趣方法则让多个用户兴趣分别提出候选。搜索改写、难负例、图关系、目录校验和学习式索引都在改变候选覆盖或匹配精度。候选确定后如何利用列表上下文，接着看重排主题。

## 一个例子

一个人既看跑步装备也看露营视频。若召回的100条全是跑步内容，再强的精排也排不出露营视频；先保留两个兴趣通道，才有机会让后续模型比较两类候选。

## 什么时候要小心

把召回数从100增加到1000会自然提高覆盖，不能据此认定表征更好。比较时要对齐候选预算、负例范围、索引快照和可用库存；本地代理日志也不能证明论文线上收益。

## 先读这几篇

先用YouTube DNN理解召回与精排分工，再读Airbnb EBR看难负例和库存约束，最后用MIMA理解多兴趣为何需要互补监督；后两篇的公开数据替代边界需同时阅读。

1. [Deep Neural Networks for YouTube Recommendations](../../../reproductions/recsys2016-youtube-dnn-youtube-dnn/README.md) · [原论文](https://research.google/pubs/deep-neural-networks-for-youtube-recommendations/)
2. [Applying Embedding-Based Retrieval to Airbnb Search](../../../reproductions/2601.06873-airbnb-ebr/README.md) · [原论文](https://arxiv.org/abs/2601.06873)
3. [MIMA: Multi-Interest Recommendation via Multi-Positive Exclusive Assignment](../../../reproductions/2609.12842-mima/README.md) · [原论文](https://arxiv.org/abs/2609.12842)

## 自测一下

只增加返回候选数后 Recall@K 上升，能证明用户编码器更好了吗？

??? note "展开参考答案"

    不能。候选预算同时改变了，提升可能只来自检索更多物品。应固定K与索引/过滤条件，再比较覆盖、质量和延迟。

## 这个子主题的论文卡片

导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">
<div class="ar-learning-controls">
<label for="learning-search">搜索卡片
<input id="learning-search" type="search" data-learning-search placeholder="搜索论文、机制、机构或本地边界"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">共 36 张卡片</p>
<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="PAIR: Preference-Aligned Intent Retrieval for Premium People Recommendation at LinkedIn 搜广推与 LLM 应用 LinkedIn 2026-10-22 职业社交中的相关性往往是互补而非相似：求职者可能需要招聘者，不是与自己背景最相近的人。PAIR 从被点击候选、同次曝光未点击候选和随机会员构造偏好，训练共享的 profile/document 编码器，并用历史塔刻画短期意图。论文明确说它不是 token 级 DPO，也没有显式参考模型或 KL 项；损失在计算形式上就是多负例对比学习，差别在曝光条件下的监督语义。 成本过高，不复现（审查 DONE）；这些是公式与接口诊断，不是模型准确率、完整推荐能力或线上提升。固定三种子证据见组件指标，真实CUDA回执为 docs/gpu-validations/pair-a100-20261023.json。验证比较独立标量余弦/交叉熵公式与梯度，执行三次真实更新，检查掩码历史无影响、位置顺序有效、曝光负例不混入点击正例。这些是公式与接口诊断，不是模型准确率、完整推荐能力或线上提升。  召回与匹配 曝光偏好与历史意图 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-pair-40d29d93">PAIR: Preference-Aligned Intent Retrieval for Premium People Recommendation at LinkedIn</h2>
<p class="ar-learning-card__meta">LinkedIn · 论文公开：2026-10-22</p>
<p><strong>方法要点：</strong>职业社交中的相关性往往是互补而非相似：求职者可能需要招聘者，不是与自己背景最相近的人。PAIR 从被点击候选、同次曝光未点击候选和随机会员构造偏好，训练共享的 profile/document 编码器，并用历史塔刻画短期意图。论文明确说它不是 token 级 DPO，也没有显式参考模型或 KL 项；损失在计算形式上就是多负例对比学习，差别在曝光条件下的监督语义。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）；这些是公式与接口诊断，不是模型准确率、完整推荐能力或线上提升。固定三种子证据见组件指标，真实CUDA回执为 docs/gpu-validations/pair-a100-20261023.json。验证比较独立标量余弦/交叉熵公式与梯度，执行三次真实更新，检查掩码历史无影响、位置顺序有效、曝光负例不混入点击正例。这些是公式与接口诊断，不是模型准确率、完整推荐能力或线上提升。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30941v1">原论文</a> · <a href="../../../../recommendation-components/2610.30941-pair/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="LLM-based User-Product Relevance Evaluation for Dynamic Product Advertising 搜广推与 LLM 应用 Snap Inc. 2026-10-10 广告召回的点击信号稀疏且有偏，单纯离线命中率难以代表用户真实需求。该方法按语义ID与事件类型压缩历史意图，通过自动发现且人工业务对齐的相关性准则训练学生判别器，再聚合为用户与流量组的相关性指标。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文§4–5依赖10K私有日志经GPT-5、Gemini-2.5-Pro与多轮人工审定；生产student为Gemini-2.5-Flash微调并经Vertex AI调用。商业API、人工标注和私有数据不是当前单卡可直接复现的资源；未测量本地或API总成本，不启动付费教师调用或替换为启发式judge。  ads-retrieval llm-judge evaluation 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-snap-dpa-relevance-9f0c9ccb">LLM-based User-Product Relevance Evaluation for Dynamic Product Advertising</h2>
<p class="ar-learning-card__meta">Snap Inc. · 论文公开：2026-10-10</p>
<p><strong>方法要点：</strong>广告召回的点击信号稀疏且有偏，单纯离线命中率难以代表用户真实需求。该方法按语义ID与事件类型压缩历史意图，通过自动发现且人工业务对齐的相关性准则训练学生判别器，再聚合为用户与流量组的相关性指标。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文§4–5依赖10K私有日志经GPT-5、Gemini-2.5-Pro与多轮人工审定；生产student为Gemini-2.5-Flash微调并经Vertex AI调用。商业API、人工标注和私有数据不是当前单卡可直接复现的资源；未测量本地或API总成本，不启动付费教师调用或替换为启发式judge。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14550">原论文</a> · <a href="../../../../reproductions/2610.14550-snap-dpa-relevance/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="RPTune: Learned Context Curation for LLM Catalog Search 搜广推与 LLM 应用 Google 2026-10-01 用查询-商品编码器、可学习调整项和下游 LLM 反馈共同决定商品保留与摆放顺序；高优商品靠近提示词末端，再对编排后的目录做选择后训练。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。只执行 rank/prune/position 核心编排，不调用 Gemini/Gemma、商家目录或论文训练。只执行 rank/prune/position 核心编排，不调用 Gemini/Gemma、商家目录或论文训练。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  search llm-recommendation context-curation 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-rptune-1e6a74b6">RPTune: Learned Context Curation for LLM Catalog Search</h2>
<p class="ar-learning-card__meta">Google · 论文公开：2026-10-01</p>
<p><strong>方法要点：</strong>用查询-商品编码器、可学习调整项和下游 LLM 反馈共同决定商品保留与摆放顺序；高优商品靠近提示词末端，再对编排后的目录做选择后训练。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。只执行 rank/prune/position 核心编排，不调用 Gemini/Gemma、商家目录或论文训练。只执行 rank/prune/position 核心编排，不调用 Gemini/Gemma、商家目录或论文训练。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00964">原论文</a> · <a href="../../../../reproductions/2610.00964-rptune/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="MuSeR: Scalable Long-sequence Recommendation with Multi-interest Modeling 搜广推与 LLM 应用 Baidu 2026-09-20 工业用户长期行为可达十万级，直接截断丢掉稳定偏好，直接 Transformer 编码又超预算。MuSeR 将最近行为原样保留，中期与远期行为分别用更大步幅汇聚；压缩后的序列由轻量 Transformer 编码。多组可学习 query 从序列状态提取不同兴趣，候选物品再通过相似度 softmax 选择兴趣。论文还把 ERNIE 生成的内容摘要蒸馏后用 BGE 编码，与 ID embedding 对齐并融合；训练使用 next-K 对比目标和兴趣正交正则。 复现级别：概念验证（非论文完整复现）。复现级别：概念验证（非论文完整复现）。本地训练了分层时间压缩、Transformer 编码、可学习多查询兴趣、候选自适应兴趣融合与正交约束；但论文的 ERNIE→BGE 多模态语义链路被公开商品标签替代，因此不能把本地结果称为 MuSeR 论文效果。公开数据只有视频标签作为内容特征，没有论文使用的 ERNIE 摘要、ERNIE-Speed 蒸馏、BGE 文本/视频向量；这决定了本实验只能列为概念验证。本地对照口径：最近序列单兴趣 ID 为基线，三 seed test Recall@10 均值 0.0100；完整本地实验组 0.0257，相对 +156.7%、绝对 +0.0157。  retrieval long-sequence multi-interest 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-muser-f887e208">MuSeR: Scalable Long-sequence Recommendation with Multi-interest Modeling</h2>
<p class="ar-learning-card__meta">Baidu · 论文公开：2026-09-20</p>
<p><strong>方法要点：</strong>工业用户长期行为可达十万级，直接截断丢掉稳定偏好，直接 Transformer 编码又超预算。MuSeR 将最近行为原样保留，中期与远期行为分别用更大步幅汇聚；压缩后的序列由轻量 Transformer 编码。多组可学习 query 从序列状态提取不同兴趣，候选物品再通过相似度 softmax 选择兴趣。论文还把 ERNIE 生成的内容摘要蒸馏后用 BGE 编码，与 ID embedding 对齐并融合；训练使用 next-K 对比目标和兴趣正交正则。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：概念验证（非论文完整复现）。复现级别：概念验证（非论文完整复现）。本地训练了分层时间压缩、Transformer 编码、可学习多查询兴趣、候选自适应兴趣融合与正交约束；但论文的 ERNIE→BGE 多模态语义链路被公开商品标签替代，因此不能把本地结果称为 MuSeR 论文效果。公开数据只有视频标签作为内容特征，没有论文使用的 ERNIE 摘要、ERNIE-Speed 蒸馏、BGE 文本/视频向量；这决定了本实验只能列为概念验证。本地对照口径：最近序列单兴趣 ID 为基线，三 seed test Recall@10 均值 0.0100；完整本地实验组 0.0257，相对 +156.7%、绝对 +0.0157。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.23677">原论文</a> · <a href="../../../../reproductions/2609.23677-muser/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="MIMA: Multi-Interest Recommendation via Multi-Positive Exclusive Assignment 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-09-11 传统多兴趣召回每个训练样本只有一个正例，容易反复更新同一个最相似兴趣并造成 interest collapse。MIMA 把同一请求共同出现的物品视为多正例集合，用 causal decoder 生成多个兴趣，再用 Hungarian matching 强制正例与兴趣一对一监督；routing 模块估计每个兴趣的激活概率，使不同通道的分数可比较。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行多正例分组、一对一最小成本分配、互补兴趣更新和兴趣激活校准；生产 causal Transformer 由公开序列特征替代。公开数据没有生产“同请求多成交”日志，本地以相邻行为组替代；未复刻阿里私有 catalog、生产 causal Transformer checkpoint 和在线召回系统。当前不映射 evolve，避免只有 registry 标签而无可执行候选协议。MovieLens 100K、seeds 42/43/44 的统一结果见 metrics/movielens-100k-seeds42-44.json。  retrieval multi-interest exclusive-assignment industrial-recommendation 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-mima-5191fe9f">MIMA: Multi-Interest Recommendation via Multi-Positive Exclusive Assignment</h2>
<p class="ar-learning-card__meta">Alibaba International Digital Commerce Group · 论文公开：2026-09-11</p>
<p><strong>方法要点：</strong>传统多兴趣召回每个训练样本只有一个正例，容易反复更新同一个最相似兴趣并造成 interest collapse。MIMA 把同一请求共同出现的物品视为多正例集合，用 causal decoder 生成多个兴趣，再用 Hungarian matching 强制正例与兴趣一对一监督；routing 模块估计每个兴趣的激活概率，使不同通道的分数可比较。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行多正例分组、一对一最小成本分配、互补兴趣更新和兴趣激活校准；生产 causal Transformer 由公开序列特征替代。公开数据没有生产“同请求多成交”日志，本地以相邻行为组替代；未复刻阿里私有 catalog、生产 causal Transformer checkpoint 和在线召回系统。当前不映射 evolve，避免只有 registry 标签而无可执行候选协议。MovieLens 100K、seeds 42/43/44 的统一结果见 metrics/movielens-100k-seeds42-44.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.12842">原论文</a> · <a href="../../../../reproductions/2609.12842-mima/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Beyond Co-purchase Relation: Evolution of Complementary Recommendations at Allegro 搜广推与 LLM 应用 Allegro.com 2026-09-04 共购不等于互补：相机与另一台相机可能经常一起浏览，却不如镜头真正互补。AlleCompanion 先用 ComCat 融合专家规则、人工反馈、LLM 推理和统计挖掘形成类别关系，再用类别约束双塔和 Category Adapter 把候选限制在合理的互补空间。 复现级别：CPU 可训练检索核心。复现级别：CPU 可训练检索核心。共享内容/类别编码器、Category Adapter、混合负样本检索损失和类别重建损失均参与反向传播。MovieLens 邻接关系不是商品互补性，不声称复现 ComCat 或线上效果。ComCat 原始映射、Allegro 行为数据和生产服务未公开；本地实现的是可审计核心机制，不是生产系统复刻。2026-09-08 更正：旧版固定加权打分结果作废。  complementary-recommendation two-tower category-adapter e-commerce 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-allecompanion-f53aba66">Beyond Co-purchase Relation: Evolution of Complementary Recommendations at Allegro</h2>
<p class="ar-learning-card__meta">Allegro.com · 论文公开：2026-09-04</p>
<p><strong>方法要点：</strong>共购不等于互补：相机与另一台相机可能经常一起浏览，却不如镜头真正互补。AlleCompanion 先用 ComCat 融合专家规则、人工反馈、LLM 推理和统计挖掘形成类别关系，再用类别约束双塔和 Category Adapter 把候选限制在合理的互补空间。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：CPU 可训练检索核心。复现级别：CPU 可训练检索核心。共享内容/类别编码器、Category Adapter、混合负样本检索损失和类别重建损失均参与反向传播。MovieLens 邻接关系不是商品互补性，不声称复现 ComCat 或线上效果。ComCat 原始映射、Allegro 行为数据和生产服务未公开；本地实现的是可审计核心机制，不是生产系统复刻。2026-09-08 更正：旧版固定加权打分结果作废。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.05063">原论文</a> · <a href="../../../../reproductions/2609.05063-allecompanion/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="SetMIR: Multi-Interest Retrieval as Set Prediction 搜广推与 LLM 应用 Snap Inc. 2026-08-31 SetMIR 用 K 个可学习 query 解码无序兴趣集合，Hungarian matching 强制一对一分工以抑制兴趣坍缩；presence head 判断本次请求实际需要哪些兴趣，服务时再用 query-level NMS 删除重复 ANN 请求。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现兴趣集合、presence 门控和 query-level NMS。未复刻私有 DPA 历史、生产 Transformer checkpoint 与 ANN dispatch；仅声明 CPU 公共数据路径。用公开类型簇代理兴趣 query，执行 presence 与相关性 NMS；NDCG@10 从 0.05401 到 0.05665。三 seed 产物见 metrics/public-seeds42-44.json。  multi-interest-retrieval set-prediction dynamic-dispatch 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-setmir-231692c0">SetMIR: Multi-Interest Retrieval as Set Prediction</h2>
<p class="ar-learning-card__meta">Snap Inc. · 论文公开：2026-08-31</p>
<p><strong>方法要点：</strong>SetMIR 用 K 个可学习 query 解码无序兴趣集合，Hungarian matching 强制一对一分工以抑制兴趣坍缩；presence head 判断本次请求实际需要哪些兴趣，服务时再用 query-level NMS 删除重复 ANN 请求。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现兴趣集合、presence 门控和 query-level NMS。未复刻私有 DPA 历史、生产 Transformer checkpoint 与 ANN dispatch；仅声明 CPU 公共数据路径。用公开类型簇代理兴趣 query，执行 presence 与相关性 NMS；NDCG@10 从 0.05401 到 0.05665。三 seed 产物见 metrics/public-seeds42-44.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.30251">原论文</a> · <a href="../../../../reproductions/2608.30251-setmir/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Scaling Graph Neural Networks for Friend Recommendation: Multi-Hash User Embeddings and Temporal Neighbor Sampling 搜广推与 LLM 应用 AI VK 2026-08-27 超大社交图既放不下完整用户 ID 表，又必须防止采到未来好友边。论文用三个独立 hash 查共享表并拼接投影，以 timestamp-sorted CSR + binary search 得到历史邻居前缀，再由 GATv2 和 query/candidate 双头打分。 Fidelity：核心机制复现。本地执行多哈希共享表、按时间排序邻接与二分 cutoff，并在公开数据上与同候选集基线比较。MovieLens 物品转移图不是好友图；未复刻 VK 私有日志、194M 用户图、分布式 GATv2 和生产 ranker。本地对照口径：基线为相同全候选目录上的 popularity ranker，实验组为 Friend-GNN 时序图 proxy；Hit@10 相对提升 247.62%，仅用于本地机制对照。  friend-recommendation graph-ranking multi-hash-embedding temporal-sampling 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-friend-gnn-0f3bf9e0">Scaling Graph Neural Networks for Friend Recommendation: Multi-Hash User Embeddings and Temporal Neighbor Sampling</h2>
<p class="ar-learning-card__meta">AI VK · 论文公开：2026-08-27</p>
<p><strong>方法要点：</strong>超大社交图既放不下完整用户 ID 表，又必须防止采到未来好友边。论文用三个独立 hash 查共享表并拼接投影，以 timestamp-sorted CSR + binary search 得到历史邻居前缀，再由 GATv2 和 query/candidate 双头打分。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity：核心机制复现。本地执行多哈希共享表、按时间排序邻接与二分 cutoff，并在公开数据上与同候选集基线比较。MovieLens 物品转移图不是好友图；未复刻 VK 私有日志、194M 用户图、分布式 GATv2 和生产 ranker。本地对照口径：基线为相同全候选目录上的 popularity ranker，实验组为 Friend-GNN 时序图 proxy；Hit@10 相对提升 247.62%，仅用于本地机制对照。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27413">原论文</a> · <a href="../../../../reproductions/2608.27413-friend-gnn/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="TransRetrieval: Scaling Up Transformer-Based Retrieval for Industrial Recommendation 搜广推与 LLM 应用 Renmin University of China / Taobao &amp; Tmall Group, Alibaba 2026-08-26 跨域广告召回同时受源域噪声、目标域 token 成本和域信息混淆影响。论文按 token norm 聚合源历史，把多个 target tokens 压为一个，并以位置形式注入 domain embedding，减少 target attention 开销。 85% target FLOPs reduction 是结构诊断，不是端到端延迟实测。Fidelity：核心机制复现。本地执行 norm-aware 聚合、target-token 压缩和位置化 domain embedding。未使用论文的 400 亿交互、5200 万广告和生产 ANN；85% target FLOPs reduction 是结构诊断，不是端到端延迟实测。本地对照口径：基线为 Transformer two-tower；实验组加入三项核心机制。MovieLens-1M Hit@10 0.1063 → 0.1187（+11.76%），NDCG@10 0.05429 → 0.05473（+0.81%）。  retrieval transformer-scaling target-token-compression multi-domain 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-transretrieval-4252b15a">TransRetrieval: Scaling Up Transformer-Based Retrieval for Industrial Recommendation</h2>
<p class="ar-learning-card__meta">Renmin University of China / Taobao &amp; Tmall Group, Alibaba · 论文公开：2026-08-26</p>
<p><strong>方法要点：</strong>跨域广告召回同时受源域噪声、目标域 token 成本和域信息混淆影响。论文按 token norm 聚合源历史，把多个 target tokens 压为一个，并以位置形式注入 domain embedding，减少 target attention 开销。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>85% target FLOPs reduction 是结构诊断，不是端到端延迟实测。Fidelity：核心机制复现。本地执行 norm-aware 聚合、target-token 压缩和位置化 domain embedding。未使用论文的 400 亿交互、5200 万广告和生产 ANN；85% target FLOPs reduction 是结构诊断，不是端到端延迟实测。本地对照口径：基线为 Transformer two-tower；实验组加入三项核心机制。MovieLens-1M Hit@10 0.1063 → 0.1187（+11.76%），NDCG@10 0.05429 → 0.05473（+0.81%）。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25528">原论文</a> · <a href="../../../../reproductions/2608.25528-transretrieval/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="SPEAR: Selection-aware Personalized End-to-end Adaptive Rewriting and Retrieval for Community Search 搜广推与 LLM 应用 Dewu 2026-08-03 端到端改写—检索容易让通用词凭高 path score 胜出、偏离原 query。SPEAR 用双 embedding 和梯度隔离保护 recall 语义，以 rewrite confidence × item relevance 的乘法门消除捷径，再由动态 selector 产生 request-specific 权重、scale 和 bias。 Fidelity：核心机制复现。公开数据只验证论文机制，不模拟生产流量。MovieLens item 内容代理商品/帖子，未复刻得物 query rewrite generator、私有 session 与线上排序链路。本地对照口径：基线为共享 transition + content scorer，实验组只加入 SPEAR 核心机制；相对 NDCG@10 +26.95%。  search query-rewriting retrieval personalization 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-spear-7c6c6f8e">SPEAR: Selection-aware Personalized End-to-end Adaptive Rewriting and Retrieval for Community Search</h2>
<p class="ar-learning-card__meta">Dewu · 论文公开：2026-08-03</p>
<p><strong>方法要点：</strong>端到端改写—检索容易让通用词凭高 path score 胜出、偏离原 query。SPEAR 用双 embedding 和梯度隔离保护 recall 语义，以 rewrite confidence × item relevance 的乘法门消除捷径，再由动态 selector 产生 request-specific 权重、scale 和 bias。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity：核心机制复现。公开数据只验证论文机制，不模拟生产流量。MovieLens item 内容代理商品/帖子，未复刻得物 query rewrite generator、私有 session 与线上排序链路。本地对照口径：基线为共享 transition + content scorer，实验组只加入 SPEAR 核心机制；相对 NDCG@10 +26.95%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01738">原论文</a> · <a href="../../../../reproductions/2608.01738-spear/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="ASARL: Autonomous Social-Aware Relevance Learning for QQ Search 搜广推与 LLM 应用 Tencent PCG 2026-07-29 QQ 群与频道搜索面对口语化标题、长尾数据和行为漂移。ASARL 用 ReasonAgent 产出 intent–attribute reasoning 与三级相关性标签，CriticAgent 反复校验并检测分布缺口，GenAgent 为长尾区域补样本；随后执行 Social Context Training、基于交互信号的 Preference-Guided Optimization，最后蒸馏到可在线服务的小模型。 Fidelity: 核心机制复现。实际执行多 Agent 数据整理、SCT、偏好优化与 social distillation；闭源 LLM 和 QQ 私有日志未复刻。没有 QQ 私有 query-title 日志、生产 LLM 标注 Agent 或线上 RoBERTa。这里验证的是闭环数据整理、偏好阶段和蒸馏路径；MovieLens genre 代理造成的负迁移被原样保留。本地对照口径：基线与实验组使用同一 MovieLens relevance proxy、student 参数量、训练划分和 seed；实验组增加 Reason/Critic/Gen、PGO 与蒸馏，相对 NDCG@10 为 -72.72%。  search-relevance multi-agent-data-curation knowledge-distillation 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-asarl-181d0e5f">ASARL: Autonomous Social-Aware Relevance Learning for QQ Search</h2>
<p class="ar-learning-card__meta">Tencent PCG · 论文公开：2026-07-29</p>
<p><strong>方法要点：</strong>QQ 群与频道搜索面对口语化标题、长尾数据和行为漂移。ASARL 用 ReasonAgent 产出 intent–attribute reasoning 与三级相关性标签，CriticAgent 反复校验并检测分布缺口，GenAgent 为长尾区域补样本；随后执行 Social Context Training、基于交互信号的 Preference-Guided Optimization，最后蒸馏到可在线服务的小模型。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。实际执行多 Agent 数据整理、SCT、偏好优化与 social distillation；闭源 LLM 和 QQ 私有日志未复刻。没有 QQ 私有 query-title 日志、生产 LLM 标注 Agent 或线上 RoBERTa。这里验证的是闭环数据整理、偏好阶段和蒸馏路径；MovieLens genre 代理造成的负迁移被原样保留。本地对照口径：基线与实验组使用同一 MovieLens relevance proxy、student 参数量、训练划分和 seed；实验组增加 Reason/Critic/Gen、PGO 与蒸馏，相对 NDCG@10 为 -72.72%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26593">原论文</a> · <a href="../../../../reproductions/2607.26593-asarl/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="OneShot: Index-in-Ranking with Neural Scoring for Large-Scale Retrieval 搜广推与 LLM 应用 Meta / Instagram 2026-07-29 传统 ANN 索引按 embedding 几何邻近性组织物品，而排序目标直接优化用户行为，两者不一致。OneShot 在模型内共同学习层级索引和排序：前向使用离散路径，反向用 straight-through estimator；全局路径平衡避免热门桶拥塞；候选进入路径后再使用比点积更强的 neural scoring。 Fidelity: 核心机制复现。本地执行 ranking-shaped 分层索引、路径探测和非点积 neural scoring；确定性 assignment 代理生产训练中的 STE 与全局平衡优化。未复刻 Instagram 私有数据、十亿物品多机索引、STE 训练 kernel、SCO 全局平衡与线上检索服务；本地结果不等同论文复现指标。本地对照口径：基线为同数据、同全库评测的 two-tower 点积检索；实验组加入 ranking-shaped 分层索引和 neural scoring，NDCG@10 相对 -7.70%。  retrieval learnable-index neural-scoring serving 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-oneshot-index-d86efe4f">OneShot: Index-in-Ranking with Neural Scoring for Large-Scale Retrieval</h2>
<p class="ar-learning-card__meta">Meta / Instagram · 论文公开：2026-07-29</p>
<p><strong>方法要点：</strong>传统 ANN 索引按 embedding 几何邻近性组织物品，而排序目标直接优化用户行为，两者不一致。OneShot 在模型内共同学习层级索引和排序：前向使用离散路径，反向用 straight-through estimator；全局路径平衡避免热门桶拥塞；候选进入路径后再使用比点积更强的 neural scoring。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地执行 ranking-shaped 分层索引、路径探测和非点积 neural scoring；确定性 assignment 代理生产训练中的 STE 与全局平衡优化。未复刻 Instagram 私有数据、十亿物品多机索引、STE 训练 kernel、SCO 全局平衡与线上检索服务；本地结果不等同论文复现指标。本地对照口径：基线为同数据、同全库评测的 two-tower 点积检索；实验组加入 ranking-shaped 分层索引和 neural scoring，NDCG@10 相对 -7.70%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27475">原论文</a> · <a href="../../../../reproductions/2607.27475-oneshot-index/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="CORE: A Unified Cascaded Ordinal Relevance Estimation Framework for E-commerce Search 搜广推与 LLM 应用 Meituan / Beijing Institute of Technology 2026-07-27 电商相关性是有序的 High/Mid/Low，但 flat 三分类把三个边界视为对称。CORE 先判断 High vs. Non-High；只有第一步为 Non-High 时才判断 Mid vs. Low，使两个 head 分别专注严格实体/意图匹配和较软的替代性边界。 Fidelity: 核心机制复现。实际执行 flat/cascade 分类、条件 step reward、group-normalized clipped GRPO 和 PostCoT logit 聚合蒸馏；缩小 encoder、数据和 LLM。MovieLens 用户 genre 画像与候选 genre overlap 构造可审计的三级序数标签，替代美团私有 query-item 标注；小型 MLP 替代 Qwen3-14B 与生产 BERT。结果只验证级联、step credit 和 PostCoT 蒸馏链路，不能外推到搜索语义或线上阈值。  search-ranking ordinal-relevance step-grpo llm-distillation 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-core-relevance-f3a9a752">CORE: A Unified Cascaded Ordinal Relevance Estimation Framework for E-commerce Search</h2>
<p class="ar-learning-card__meta">Meituan / Beijing Institute of Technology · 论文公开：2026-07-27</p>
<p><strong>方法要点：</strong>电商相关性是有序的 High/Mid/Low，但 flat 三分类把三个边界视为对称。CORE 先判断 High vs. Non-High；只有第一步为 Non-High 时才判断 Mid vs. Low，使两个 head 分别专注严格实体/意图匹配和较软的替代性边界。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。实际执行 flat/cascade 分类、条件 step reward、group-normalized clipped GRPO 和 PostCoT logit 聚合蒸馏；缩小 encoder、数据和 LLM。MovieLens 用户 genre 画像与候选 genre overlap 构造可审计的三级序数标签，替代美团私有 query-item 标注；小型 MLP 替代 Qwen3-14B 与生产 BERT。结果只验证级联、step credit 和 PostCoT 蒸馏链路，不能外推到搜索语义或线上阈值。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24417">原论文</a> · <a href="../../../../reproductions/2607.24417-core-relevance/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Melo: A Production LLM-Powered Music Recommendation Agent 搜广推与 LLM 应用 NetEase Cloud Music / Zhejiang University of Technology 2026-07-26 用多节点 Agent 编排意图、检索、推荐与解释，以实体目录 grounding 阻止幻觉，并在失败时触发反思重试。 Fidelity: 核心机制复现。本地执行意图路由、grounded 检索与失败反思重试；不把公开代理环境冒充网易云音乐生产系统。无法隔离论文系统 A/B 中模型、产品面和 UI 的贡献，论文也未给置信区间；本站明确保留该归因限制。本地对照口径：基线为无运行时修复的 catalog recommender，实验组为 grounding + retry；Hit@10 -20.00%、NDCG@10 -8.16%，fresh Hit@10 +50.00%。  llm-recommendation agent entity-grounding reflection 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-melo-f661791b">Melo: A Production LLM-Powered Music Recommendation Agent</h2>
<p class="ar-learning-card__meta">NetEase Cloud Music / Zhejiang University of Technology · 论文公开：2026-07-26</p>
<p><strong>方法要点：</strong>用多节点 Agent 编排意图、检索、推荐与解释，以实体目录 grounding 阻止幻觉，并在失败时触发反思重试。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地执行意图路由、grounded 检索与失败反思重试；不把公开代理环境冒充网易云音乐生产系统。无法隔离论文系统 A/B 中模型、产品面和 UI 的贡献，论文也未给置信区间；本站明确保留该归因限制。本地对照口径：基线为无运行时修复的 catalog recommender，实验组为 grounding + retry；Hit@10 -20.00%、NDCG@10 -8.16%，fresh Hit@10 +50.00%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.23718">原论文</a> · <a href="../../../../reproductions/2607.23718-melo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="MESH: Scaling Up Retrieval with Heterogeneous Content Unification 搜广推与 LLM 应用 Pinterest 2026-07-14 统一放大 flat retrieval 容易让高频 evergreen 梯度淹没 fresh/tail 信号。MESH 先把 user/item/context 分到独立 sub-tower，各自在全局交互前用 residual crossing 放大；RGBC 再用 context gate 调节纯 user-item affinity，服务端可并行各塔并异步缓存 item tower。 Fidelity: 核心机制复现。分组 manifold、独立 residual signal amplifier、全局 crossing 与 RGBC 均实际执行。未复刻 DHEN 全算子与生产 GPU inter-op；不引用本地微基准支持论文吞吐结论。本地对照口径：基线是 flat retrieval；实验组 MESH 使用三塔放大与 RGBC，验证集选 blend 0.1，相对基线 Hit@10 +0.00%、NDCG@10 -3.54%。  retrieval fresh-content serving 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-mesh-881b1237">MESH: Scaling Up Retrieval with Heterogeneous Content Unification</h2>
<p class="ar-learning-card__meta">Pinterest · 论文公开：2026-07-14</p>
<p><strong>方法要点：</strong>统一放大 flat retrieval 容易让高频 evergreen 梯度淹没 fresh/tail 信号。MESH 先把 user/item/context 分到独立 sub-tower，各自在全局交互前用 residual crossing 放大；RGBC 再用 context gate 调节纯 user-item affinity，服务端可并行各塔并异步缓存 item tower。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。分组 manifold、独立 residual signal amplifier、全局 crossing 与 RGBC 均实际执行。未复刻 DHEN 全算子与生产 GPU inter-op；不引用本地微基准支持论文吞吐结论。本地对照口径：基线是 flat retrieval；实验组 MESH 使用三塔放大与 RGBC，验证集选 blend 0.1，相对基线 Hit@10 +0.00%、NDCG@10 -3.54%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12392">原论文</a> · <a href="../../../../reproductions/2607.12392-mesh/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="ZoRRO: A Zero-Weight Personalized Recommender System for Scalable News Recommendation 搜广推与 LLM 应用 Technical University of Denmark 2026-07-12 不用模型训练，直接融合历史文章的时间衰减、语义相似度和类别关系，面向高吞吐新闻候选排序。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 ZoRRO 为 0.05201，相对变化 -3.70%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  news-recommendation training-free recency 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-zorro-2da90bec">ZoRRO: A Zero-Weight Personalized Recommender System for Scalable News Recommendation</h2>
<p class="ar-learning-card__meta">Technical University of Denmark · 论文公开：2026-07-12</p>
<p><strong>方法要点：</strong>不用模型训练，直接融合历史文章的时间衰减、语义相似度和类别关系，面向高吞吐新闻候选排序。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 ZoRRO 为 0.05201，相对变化 -3.70%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.10910">原论文</a> · <a href="../../../../reproductions/2607.10910-zorro/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Multilingual Semantic Retrieval for Apple Music Search 搜广推与 LLM 应用 Apple 2026-07-11 Siamese bi-encoder 补充词法倒排，再用分位数分布匹配把 dense 与 token score 校准到同一尺度并限制语义结果数量。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 ELISE 为 0.04739，相对变化 -12.24%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  search multilingual-retrieval score-calibration 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-elise-a73bc968">Multilingual Semantic Retrieval for Apple Music Search</h2>
<p class="ar-learning-card__meta">Apple · 论文公开：2026-07-11</p>
<p><strong>方法要点：</strong>Siamese bi-encoder 补充词法倒排，再用分位数分布匹配把 dense 与 token score 校准到同一尺度并限制语义结果数量。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 ELISE 为 0.04739，相对变化 -12.24%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.10239">原论文</a> · <a href="../../../../reproductions/2607.10239-elise/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Real-Time Hard Negative Sampling via LLM-based Clustering for Large-Scale Two-Tower Retrieval 搜广推与 LLM 应用 Meta 2026-07-01 大规模双塔召回常从 out-of-batch（OOB）池随机抽负例。绝大多数负例过于容易，梯度弱；同时热门物品更常进入池，形成曝光反馈循环。论文先用 LLM/多模态 embedding 把物品划入语义 cluster，再让 GOOBS 的 update engine 按 cluster 分段写入实时 OOB 池，sample engine 大概率从正例所在 cluster 抽 hard negative。这样不增加在线模型结构，采样仍是 O(1)。 Fidelity: 核心机制复现。cluster-conditioned online hard-negative sampler 实际执行；MovieLens genre 替换私有 LLM 多模态 cluster，分布式 GOOBS serving 未复刻。本地对照口径：基线是 Random OOB negative sampler；实验组是 Cluster GOOBS sampler；NDCG@10 +0.98%、head share -1.81%。这是负采样策略消融，不是完整双塔相对 DIN 的比较。   搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-cluster-goobs-3f572e40">Real-Time Hard Negative Sampling via LLM-based Clustering for Large-Scale Two-Tower Retrieval</h2>
<p class="ar-learning-card__meta">Meta · 论文公开：2026-07-01</p>
<p><strong>方法要点：</strong>大规模双塔召回常从 out-of-batch（OOB）池随机抽负例。绝大多数负例过于容易，梯度弱；同时热门物品更常进入池，形成曝光反馈循环。论文先用 LLM/多模态 embedding 把物品划入语义 cluster，再让 GOOBS 的 update engine 按 cluster 分段写入实时 OOB 池，sample engine 大概率从正例所在 cluster 抽 hard negative。这样不增加在线模型结构，采样仍是 O(1)。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。cluster-conditioned online hard-negative sampler 实际执行；MovieLens genre 替换私有 LLM 多模态 cluster，分布式 GOOBS serving 未复刻。本地对照口径：基线是 Random OOB negative sampler；实验组是 Cluster GOOBS sampler；NDCG@10 +0.98%、head share -1.81%。这是负采样策略消融，不是完整双塔相对 DIN 的比较。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.00448">原论文</a> · <a href="../../../../reproductions/2607.00448-cluster-goobs/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="NEXT: Reasoning-Driven Video Recommendation via a Vision-Language Model 搜广推与 LLM 应用 Meta 2026-06-27 共现和语义相似只能回答“哪些视频相近”，难以推断用户看完当前视频后下一步想做什么。NEXT 先识别显式续集；对隐式关系让 NEXT-8B VLM 生成 next-intent query，再检索并验证候选，形成 directed Next Knowledge Graph。推理放在离线，线上只在用户正反馈后注入高置信边，避免把 8B VLM 放进请求链路。 这是公开代理任务的单 seed 诊断结果，不是 Meta 线上收益复现。Fidelity: 核心机制复现。本地执行 item→intent→item、离线 directed edge 生成/验证和线上加性注入；没有把规则或 embedding 代理写成“训练了 NEXT-8B”。本地用电影标题/genre 和协同转移代理视觉语义与 VLM 验证；未训练 8B VLM、GRPO/SFT 偏好阶段，也没有短视频画面、私有安全模型和实时 serving。本地对照口径：基线为同数据的 transition+semantic 多路径 ranker；  multimodal reasoning retrieval knowledge-graph vlm 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-next-vlm-e4f6498d">NEXT: Reasoning-Driven Video Recommendation via a Vision-Language Model</h2>
<p class="ar-learning-card__meta">Meta · 论文公开：2026-06-27</p>
<p><strong>方法要点：</strong>共现和语义相似只能回答“哪些视频相近”，难以推断用户看完当前视频后下一步想做什么。NEXT 先识别显式续集；对隐式关系让 NEXT-8B VLM 生成 next-intent query，再检索并验证候选，形成 directed Next Knowledge Graph。推理放在离线，线上只在用户正反馈后注入高置信边，避免把 8B VLM 放进请求链路。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>这是公开代理任务的单 seed 诊断结果，不是 Meta 线上收益复现。Fidelity: 核心机制复现。本地执行 item→intent→item、离线 directed edge 生成/验证和线上加性注入；没有把规则或 embedding 代理写成“训练了 NEXT-8B”。本地用电影标题/genre 和协同转移代理视觉语义与 VLM 验证；未训练 8B VLM、GRPO/SFT 偏好阶段，也没有短视频画面、私有安全模型和实时 serving。本地对照口径：基线为同数据的 transition+semantic 多路径 ranker；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24789">原论文</a> · <a href="../../../../reproductions/2607.24789-next-vlm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="RankGraph-2: Lifecycle Co-Design for Billion-Node Graph Learning in Recommendation 搜广推与 LLM 应用 Meta 2026-06-16 直接在线跑多层 GNN 成本高且易受热门边支配。RankGraph-2 对边做 popularity correction，离线预计算多跳 PPR，再用共同学习的 residual/cluster index 压缩服务。 复现保真度：核心机制复现。复现保真度：核心机制复现。流行度校正、离线 PPR 和 cluster index 均实际执行。MovieLens item graph 上真实执行去偏转移、多跳 PPR 与 PPR 表征聚类索引。  graph-retrieval ppr residual-quantization 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-rankgraph2-ef314ec2">RankGraph-2: Lifecycle Co-Design for Billion-Node Graph Learning in Recommendation</h2>
<p class="ar-learning-card__meta">Meta · 论文公开：2026-06-16</p>
<p><strong>方法要点：</strong>直接在线跑多层 GNN 成本高且易受热门边支配。RankGraph-2 对边做 popularity correction，离线预计算多跳 PPR，再用共同学习的 residual/cluster index 压缩服务。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现保真度：核心机制复现。复现保真度：核心机制复现。流行度校正、离线 PPR 和 cluster index 均实际执行。MovieLens item graph 上真实执行去偏转移、多跳 PPR 与 PPR 表征聚类索引。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.18379">原论文</a> · <a href="../../../../reproductions/2606.18379-rankgraph2/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="ToolRec: Calibrated Preference Alignment for Query Recommendation in On-Device Assistants 搜广推与 LLM 应用 Huazhong University of Science and Technology 2026-06-07 在 KTO 式偏好目标上同时加入用户侧校准与工具频率驱动的动态系统侧校准，提升会触发工具的查询，同时约束上下文相关性下降。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04819，相对变化 -10.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。  query-recommendation preference-alignment tool-use 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-toolrec-2caef440">ToolRec: Calibrated Preference Alignment for Query Recommendation in On-Device Assistants</h2>
<p class="ar-learning-card__meta">Huazhong University of Science and Technology · 论文公开：2026-06-07</p>
<p><strong>方法要点：</strong>在 KTO 式偏好目标上同时加入用户侧校准与工具频率驱动的动态系统侧校准，提升会触发工具的查询，同时约束上下文相关性下降。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04819，相对变化 -10.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.08466">原论文</a> · <a href="../../../../reproductions/2606.08466-toolrec/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="HARNESS-LM: A Three-Phase Training Recipe for Harnessing SLMs in Sponsored Search Retrieval 搜广推与 LLM 应用 Microsoft AI / Bing Ads 2026-05-22 Sponsored Search 可以离线使用昂贵文档编码器，却要求在线 query encoder 足够小。HARNESS-LM 先训练强 teacher，再让小 query encoder 直接对齐 teacher query 空间，最后冻结 teacher 文档塔做监督对比精修，避免重建索引。 Fidelity: 核心机制复现。Teacher、L2 embedding alignment、冻结 teacher document index 的 contrastive refinement 三阶段均实际执行。协同 SVD+内容代理 Qwen3-Embedding teacher；未复刻 4B/0.6B 规模、GPT expansion 与 CPU pruning frontier。本地对照口径：基线是小型对称内容 retriever；实验组 HARNESS-LM 使用强协同文档空间、L2 对齐与对比精修，相对基线 Hit@10 -23.08%、NDCG@10 -28.05%。  llm-recommendation retrieval distillation 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-harness-lm-9919eb79">HARNESS-LM: A Three-Phase Training Recipe for Harnessing SLMs in Sponsored Search Retrieval</h2>
<p class="ar-learning-card__meta">Microsoft AI / Bing Ads · 论文公开：2026-05-22</p>
<p><strong>方法要点：</strong>Sponsored Search 可以离线使用昂贵文档编码器，却要求在线 query encoder 足够小。HARNESS-LM 先训练强 teacher，再让小 query encoder 直接对齐 teacher query 空间，最后冻结 teacher 文档塔做监督对比精修，避免重建索引。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。Teacher、L2 embedding alignment、冻结 teacher document index 的 contrastive refinement 三阶段均实际执行。协同 SVD+内容代理 Qwen3-Embedding teacher；未复刻 4B/0.6B 规模、GPT expansion 与 CPU pruning frontier。本地对照口径：基线是小型对称内容 retriever；实验组 HARNESS-LM 使用强协同文档空间、L2 对齐与对比精修，相对基线 Hit@10 -23.08%、NDCG@10 -28.05%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.23572">原论文</a> · <a href="../../../../reproductions/2605.23572-harness-lm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="LLM Retrieval for Stable and Predictable Ad Recommendations 搜广推与 LLM 应用 Meta 2026-05-21 广告候选生成通常只优化点击/转化预测与 Recall，轻微修改 creative 后却可能因为 ID 或稀疏特征变化而得到完全不同的投放结果。论文新增 A/A&#x27; predictability 框架：复制 primary ad 为 shadow ad，只做不改变语义的输入扰动，再衡量两者转换和曝光差异。模型侧用经过广告检索任务适配的 LLM 从标题、描述等 creative 中抽取层级 category、brand、product 和 context 属性； Fidelity: 核心机制复现。本地实际执行成对 creative 的领域 SFT、LLM hidden-state 属性头、层级离散语义表示、phrase→token 两级 Jaccard 建图、协同图融合、validation 选权重，以及扰动稳定性评估；未复刻 Meta 私有广告语料、Llama-3-8B、分布式推理、线上转换与 shadow-ad 流量系统。本地对照口径：基线是 Collaborative Item Graph；实验组是在固定候选预算下加入 LLM Semantic Graph；Recall@20 +11.90%、NDCG@20 +3.03%，边分数漂移 -77.36%。  llm-recommendation retrieval stability 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-llm-ad-retrieval-68e38a71">LLM Retrieval for Stable and Predictable Ad Recommendations</h2>
<p class="ar-learning-card__meta">Meta · 论文公开：2026-05-21</p>
<p><strong>方法要点：</strong>广告候选生成通常只优化点击/转化预测与 Recall，轻微修改 creative 后却可能因为 ID 或稀疏特征变化而得到完全不同的投放结果。论文新增 A/A&#x27; predictability 框架：复制 primary ad 为 shadow ad，只做不改变语义的输入扰动，再衡量两者转换和曝光差异。模型侧用经过广告检索任务适配的 LLM 从标题、描述等 creative 中抽取层级 category、brand、product 和 context 属性；</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地实际执行成对 creative 的领域 SFT、LLM hidden-state 属性头、层级离散语义表示、phrase→token 两级 Jaccard 建图、协同图融合、validation 选权重，以及扰动稳定性评估；未复刻 Meta 私有广告语料、Llama-3-8B、分布式推理、线上转换与 shadow-ad 流量系统。本地对照口径：基线是 Collaborative Item Graph；实验组是在固定候选预算下加入 LLM Semantic Graph；Recall@20 +11.90%、NDCG@20 +3.03%，边分数漂移 -77.36%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.21969">原论文</a> · <a href="../../../../reproductions/2605.21969-llm-ad-retrieval/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Divergence Meets Consensus: A Multi-Source Negative Sampling Framework for Sequential Recommendation 搜广推与 LLM 应用 论文作者团队（原文未标注公司） 2026-05-19 随机负采样太容易，DNS 只追逐单模型高分负例又容易产生 false negative、低多样性和模型偏置。MDCNS 受“最近发展区”启发，引入 Self、Peer、Teacher 三个视角：Self 与异构 Peer 分别评分，Teacher 聚合两者；再用两模型分歧提升“困难且有信息量”的候选，最后把 Teacher 在完整候选池上的分布蒸馏回 Self，避免候选打分只利用一个负例。 Fidelity: 核心机制复现。三源负采样、双模型分歧/共识选择与更新实际执行；推荐 backbone 缩小为本地可训练模型。本地对照口径：主基线是 Uniform negative sampling，辅助基线是 DNS；实验组是 MDCNS；NDCG@10 相对 Uniform 从 0.003016 升至 0.006175（+104.75%）。这是采样策略消融；DIN 不适用于该采样器级比较。   搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-mdcns-8e8ced60">Divergence Meets Consensus: A Multi-Source Negative Sampling Framework for Sequential Recommendation</h2>
<p class="ar-learning-card__meta">论文作者团队（原文未标注公司） · 论文公开：2026-05-19</p>
<p><strong>方法要点：</strong>随机负采样太容易，DNS 只追逐单模型高分负例又容易产生 false negative、低多样性和模型偏置。MDCNS 受“最近发展区”启发，引入 Self、Peer、Teacher 三个视角：Self 与异构 Peer 分别评分，Teacher 聚合两者；再用两模型分歧提升“困难且有信息量”的候选，最后把 Teacher 在完整候选池上的分布蒸馏回 Self，避免候选打分只利用一个负例。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。三源负采样、双模型分歧/共识选择与更新实际执行；推荐 backbone 缩小为本地可训练模型。本地对照口径：主基线是 Uniform negative sampling，辅助基线是 DNS；实验组是 MDCNS；NDCG@10 相对 Uniform 从 0.003016 升至 0.006175（+104.75%）。这是采样策略消融；DIN 不适用于该采样器级比较。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.19651">原论文</a> · <a href="../../../../reproductions/2605.19651-mdcns/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Policy-Grounded Dynamic Facet Suggestions for Job Search 搜广推与 LLM 应用 LinkedIn 2026-05-15 先由人工与 LLM 维护符合产品策略的 facet taxonomy，再用 embedding SLM 召回候选，以生成式 SLM 做单 token 点式评分；前缀缓存和批处理满足实时延迟。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04713，相对变化 -12.73%。本地代理目标与论文生产任务不同，不能外推线上 lift。  job-search facet-retrieval policy-ranking 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-policy-facet-10555aa9">Policy-Grounded Dynamic Facet Suggestions for Job Search</h2>
<p class="ar-learning-card__meta">LinkedIn · 论文公开：2026-05-15</p>
<p><strong>方法要点：</strong>先由人工与 LLM 维护符合产品策略的 facet taxonomy，再用 embedding SLM 召回候选，以生成式 SLM 做单 token 点式评分；前缀缓存和批处理满足实时延迟。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04713，相对变化 -12.73%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.16479">原论文</a> · <a href="../../../../reproductions/2605.16479-policy-facet/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="CS3: Efficient Online Capability Synergy for Two-Tower Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-04-21 传统双塔为 ANN 解耦 user/item 表征，牺牲交叉能力。CS3 通过离线/在线可部署的循环修正和知识协同增强塔间交互。 三 seed NDCG@10 相对 -16.06%，当前小数据未复现线上收益。Fidelity: 核心机制复现。实现双塔间的循环自修正、显式交叉同步与级联教师辅助目标。没有 4 亿 DAU 的在线缓存、EMA 跨塔向量和生产 QPS 链路。本地对照口径：基线是 matched two-tower；实验组加入 cycle、cross sync 与 teacher loss；三 seed NDCG@10 相对 -16.06%，当前小数据未复现线上收益。  retrieval two-tower online-learning 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-cs3-e2cd1a82">CS3: Efficient Online Capability Synergy for Two-Tower Recommendation</h2>
<p class="ar-learning-card__meta">Kuaishou Technology · 论文公开：2026-04-21</p>
<p><strong>方法要点：</strong>传统双塔为 ANN 解耦 user/item 表征，牺牲交叉能力。CS3 通过离线/在线可部署的循环修正和知识协同增强塔间交互。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>三 seed NDCG@10 相对 -16.06%，当前小数据未复现线上收益。Fidelity: 核心机制复现。实现双塔间的循环自修正、显式交叉同步与级联教师辅助目标。没有 4 亿 DAU 的在线缓存、EMA 跨塔向量和生产 QPS 链路。本地对照口径：基线是 matched two-tower；实验组加入 cycle、cross sync 与 teacher loss；三 seed NDCG@10 相对 -16.06%，当前小数据未复现线上收益。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.19269">原论文</a> · <a href="../../../../reproductions/2604.19269-cs3/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Efficient Retrieval Scaling with Hierarchical Indexing for Large Scale Recommendation 搜广推与 LLM 应用 Meta / Facebook and Instagram Ads 2026-04-14 大型 retrieval foundation model 若对全部 user-item pair 执行复杂 interaction tower，线上成本不可接受。HILL 不再独立地按 item embedding 建 ANN，而是让 MoNN 的用户、item 与交互信号参与 index-node 学习；第一层用 attention-style soft assignment，下一层量化上一层未解释的 residual。 Fidelity: 核心机制复现。本地执行 soft assignment、跨层 residual quantization、层级 beam retrieval 与固定公开切分评测；不是把离线 k-means 树直接命名为 HILL。本地没有 MoNN 的千级特征、多任务半监督训练、Meta Ads 十亿级索引、FAISS EM 和真实 QPS；中间节点数量只作为公开的 TTT-data proxy，未宣称完成线上 test-time training。  retrieval hierarchical-index residual-quantization test-time-training serving 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-hill-index-46d50ccf">Efficient Retrieval Scaling with Hierarchical Indexing for Large Scale Recommendation</h2>
<p class="ar-learning-card__meta">Meta / Facebook and Instagram Ads · 论文公开：2026-04-14</p>
<p><strong>方法要点：</strong>大型 retrieval foundation model 若对全部 user-item pair 执行复杂 interaction tower，线上成本不可接受。HILL 不再独立地按 item embedding 建 ANN，而是让 MoNN 的用户、item 与交互信号参与 index-node 学习；第一层用 attention-style soft assignment，下一层量化上一层未解释的 residual。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地执行 soft assignment、跨层 residual quantization、层级 beam retrieval 与固定公开切分评测；不是把离线 k-means 树直接命名为 HILL。本地没有 MoNN 的千级特征、多任务半监督训练、Meta Ads 十亿级索引、FAISS EM 和真实 QPS；中间节点数量只作为公开的 TTT-data proxy，未宣称完成线上 test-time training。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.12965">原论文</a> · <a href="../../../../reproductions/2604.12965-hill-index/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="GenFacet: End-to-End Generative Faceted Search via Multi-Task Preference Alignment in E-Commerce 搜广推与 LLM 应用 JD.com 2026-03-20 GenFacet 把电商分面搜索统一为上下文分面生成与意图驱动 query 改写两个生成任务，并以教师蒸馏加 GRPO 的多任务偏好对齐直接优化下游搜索满意度，闭合“分面选择—检索”链路。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05171，相对变化 -4.26%。本地代理目标与论文生产任务不同，不能外推线上 lift。  e-commerce-search facet-generation preference-alignment 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-genfacet-00b00c8d">GenFacet: End-to-End Generative Faceted Search via Multi-Task Preference Alignment in E-Commerce</h2>
<p class="ar-learning-card__meta">JD.com · 论文公开：2026-03-20</p>
<p><strong>方法要点：</strong>GenFacet 把电商分面搜索统一为上下文分面生成与意图驱动 query 改写两个生成任务，并以教师蒸馏加 GRPO 的多任务偏好对齐直接优化下游搜索满意度，闭合“分面选择—检索”链路。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05171，相对变化 -4.26%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.19665">原论文</a> · <a href="../../../../reproductions/2603.19665-genfacet/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Not All Candidates are Created Equal: Heterogeneity-Aware Pre-ranking 搜广推与 LLM 应用 ByteDance / Toutiao 2026-03-04 按候选难度把样本路由到轻量或强预排分支，再以跨分支 harmonization 约束不同计算预算下的排序尺度。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 hap 核心机制；相对 NDCG@10 +4.90%。  pre-ranking contrastive-learning dynamic-routing 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-hap-86607d9e">Not All Candidates are Created Equal: Heterogeneity-Aware Pre-ranking</h2>
<p class="ar-learning-card__meta">ByteDance / Toutiao · 论文公开：2026-03-04</p>
<p><strong>方法要点：</strong>按候选难度把样本路由到轻量或强预排分支，再以跨分支 harmonization 约束不同计算预算下的排序尺度。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 hap 核心机制；相对 NDCG@10 +4.90%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.03770">原论文</a> · <a href="../../../../reproductions/2603.03770-hap/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Rethinking ANN-based Retrieval: Multifaceted Learnable Index for Large-scale Recommendation System 搜广推与 LLM 应用 Meta 2026-02-18 ANN 把所有召回目标压进一个几何空间，离线建索引导致新内容滞后，在线近邻搜索又随候选规模变贵。MFLI 将 index 作为模型参数联合学习，并用多个 facet 表达语义、受欢迎度和时效性；请求侧直接分配各 facet 的检索预算。 Fidelity: 核心机制复现。本地构建并学习 genre、两层 semantic code、freshness 四个 facet，而非用单一 ANN 空间代替论文方法。全目录打分用于公平实验，不测 Meta 的十亿级实时索引、GPU QPS 或私有新鲜度标签。本地对照口径：基线为同切分的 single-space ANN proxy，实验组加入四 facet MFLI；NDCG@10 相对 -10.01%。  retrieval learnable-index fresh-content diversity serving 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-mfli-7f2af977">Rethinking ANN-based Retrieval: Multifaceted Learnable Index for Large-scale Recommendation System</h2>
<p class="ar-learning-card__meta">Meta · 论文公开：2026-02-18</p>
<p><strong>方法要点：</strong>ANN 把所有召回目标压进一个几何空间，离线建索引导致新内容滞后，在线近邻搜索又随候选规模变贵。MFLI 将 index 作为模型参数联合学习，并用多个 facet 表达语义、受欢迎度和时效性；请求侧直接分配各 facet 的检索预算。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地构建并学习 genre、两层 semantic code、freshness 四个 facet，而非用单一 ANN 空间代替论文方法。全目录打分用于公平实验，不测 Meta 的十亿级实时索引、GPU QPS 或私有新鲜度标签。本地对照口径：基线为同切分的 single-space ANN proxy，实验组加入四 facet MFLI；NDCG@10 相对 -10.01%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.16124">原论文</a> · <a href="../../../../reproductions/2602.16124-mfli/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="CAPTS: Channel-Aware, Preference-Aligned Trigger Selection for Multi-Channel Item-to-Item Retrieval 搜广推与 LLM 应用 Kuaishou Technology 2026-02-13 VAM 不只看触发物品本身的反馈，而把两跳召回物品的下游消费价值归因回 trigger；CATR 再联合决定 trigger 到各 I2I 通道的路由，减少通道重叠并提升互补覆盖。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05500，相对变化 +1.84%。本地代理目标与论文生产任务不同，不能外推线上 lift。  retrieval trigger-selection multi-channel-routing 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-capts-e4a04e24">CAPTS: Channel-Aware, Preference-Aligned Trigger Selection for Multi-Channel Item-to-Item Retrieval</h2>
<p class="ar-learning-card__meta">Kuaishou Technology · 论文公开：2026-02-13</p>
<p><strong>方法要点：</strong>VAM 不只看触发物品本身的反馈，而把两跳召回物品的下游消费价值归因回 trigger；CATR 再联合决定 trigger 到各 I2I 通道的路由，减少通道重叠并提升互补覆盖。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05500，相对变化 +1.84%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12564">原论文</a> · <a href="../../../../reproductions/2602.12564-capts/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Applying Embedding-Based Retrieval to Airbnb Search 搜广推与 LLM 应用 Airbnb 2026-01-11 按搜索—浏览—预订的多阶段旅程构造正例和 hard negatives，以流量 replay 对齐第一阶段召回口径；线上结合 HNSW/IVF、地理过滤与高频库存更新。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04943，相对变化 -8.48%。本地代理目标与论文生产任务不同，不能外推线上 lift。  search-retrieval embedding-retrieval hard-negative-mining 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-airbnb-ebr-a90e62e0">Applying Embedding-Based Retrieval to Airbnb Search</h2>
<p class="ar-learning-card__meta">Airbnb · 论文公开：2026-01-11</p>
<p><strong>方法要点：</strong>按搜索—浏览—预订的多阶段旅程构造正例和 hard negatives，以流量 replay 对齐第一阶段召回口径；线上结合 HNSW/IVF、地理过滤与高频库存更新。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04943，相对变化 -8.48%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.06873">原论文</a> · <a href="../../../../reproductions/2601.06873-airbnb-ebr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="From Reasoning LLMs to BERT: A Two-Stage Distillation Framework for Search Relevance 搜广推与 LLM 应用 Meituan 2025-10-13 先以 CPT、SFT 和多维偏好优化构建领域 reasoning LLM，再让同一轻量学生的普通输入与 reasoning-augmented 输入做对比式自蒸馏，线上无需推理链。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上执行论文的候选相关检索、层级压缩或蒸馏目标；未使用公司私有日志与线上 serving，线上 A/B 只引用原文。本地相对变化不得与原文指标混写。本地对照口径：基线为 shared transition + content baseline，实验组为 CRSD，只改变论文核心机制；ndcg_at_10 0.0354 → 0.0346，相对基线 -2.14%。  search content-understanding llm-distillation 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-crsd-bbd3991b">From Reasoning LLMs to BERT: A Two-Stage Distillation Framework for Search Relevance</h2>
<p class="ar-learning-card__meta">Meituan · 论文公开：2025-10-13</p>
<p><strong>方法要点：</strong>先以 CPT、SFT 和多维偏好优化构建领域 reasoning LLM，再让同一轻量学生的普通输入与 reasoning-augmented 输入做对比式自蒸馏，线上无需推理链。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上执行论文的候选相关检索、层级压缩或蒸馏目标；未使用公司私有日志与线上 serving，线上 A/B 只引用原文。本地相对变化不得与原文指标混写。本地对照口径：基线为 shared transition + content baseline，实验组为 CRSD，只改变论文核心机制；ndcg_at_10 0.0354 → 0.0346，相对基线 -2.14%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.11056">原论文</a> · <a href="../../../../reproductions/2510.11056-crsd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="MPFormer: Adaptive Framework for Industrial Multi-Task Personalized Sequential Retriever 搜广推与 LLM 应用 Kuaishou Technology 2025-08-28 以 objective token 驱动同一序列检索器完成多种行为目标，并按任务难度动态分配容量和候选配额。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 mpformer 核心机制；相对 NDCG@10 -7.15%。  retrieval multi-task sequence serving 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-mpformer-268b1045">MPFormer: Adaptive Framework for Industrial Multi-Task Personalized Sequential Retriever</h2>
<p class="ar-learning-card__meta">Kuaishou Technology · 论文公开：2025-08-28</p>
<p><strong>方法要点：</strong>以 objective token 驱动同一序列检索器完成多种行为目标，并按任务难度动态分配容量和候选配额。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 mpformer 核心机制；相对 NDCG@10 -7.15%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.20400">原论文</a> · <a href="../../../../reproductions/2508.20400-mpformer/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Large Language Model based Long-tail Query Rewriting in Taobao Search 搜广推与 LLM 应用 Alibaba 2023-11-07 长尾电商 query 存在语义缺口，单纯 SFT 只模仿人工 rewrite，未直接对齐召回质量。BEQUE 先用拒绝采样和多指令数据 SFT，再让模型为每个 query 自采样多个 rewrite；淘宝离线搜索系统从 relevance、retrieval increment、hit rate 打分并形成偏序，最后用 Preference Ranking Optimization（PRO）把排序反馈对齐回 LLM。生产 serving 采用离线刷库 + 在线 KV，不把 7B 自回归模型放进请求链路。 Fidelity: 完整核心链路复现。真实执行 seq2seq SFT、beam self-sampling、离线检索反馈、partial order 构造和 rank-aware PRO；Qwen-7B/淘宝搜索替换为 T5-small/MovieLens 公开目录。本地对照口径：基线是 T5 SFT；实验组是同一模型继续做 PRO；主组合反馈从 0.62102 升至 0.80750（+30.03%），但 increment -66.02%。这是对齐阶段消融；DIN 不适用于 query rewriting 任务。  llm-recommendation query-rewriting preference-optimization search 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-beque-26cd2487">Large Language Model based Long-tail Query Rewriting in Taobao Search</h2>
<p class="ar-learning-card__meta">Alibaba · 论文公开：2023-11-07</p>
<p><strong>方法要点：</strong>长尾电商 query 存在语义缺口，单纯 SFT 只模仿人工 rewrite，未直接对齐召回质量。BEQUE 先用拒绝采样和多指令数据 SFT，再让模型为每个 query 自采样多个 rewrite；淘宝离线搜索系统从 relevance、retrieval increment、hit rate 打分并形成偏序，最后用 Preference Ranking Optimization（PRO）把排序反馈对齐回 LLM。生产 serving 采用离线刷库 + 在线 KV，不把 7B 自回归模型放进请求链路。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 完整核心链路复现。真实执行 seq2seq SFT、beam self-sampling、离线检索反馈、partial order 构造和 rank-aware PRO；Qwen-7B/淘宝搜索替换为 T5-small/MovieLens 公开目录。本地对照口径：基线是 T5 SFT；实验组是同一模型继续做 PRO；主组合反馈从 0.62102 升至 0.80750（+30.03%），但 increment -66.02%。这是对齐阶段消融；DIN 不适用于 query rewriting 任务。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2311.03758">原论文</a> · <a href="../../../../reproductions/2311.03758-beque/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Deep Neural Networks for YouTube Recommendations 搜广推与 LLM 应用 Google / YouTube 2016-09-15 YouTube 将推荐拆成候选生成与精排。候选阶段要从百万量级视频中快速召回，传统矩阵分解难以吸收异构历史和上下文。观看历史 embedding 经过聚合和多层网络形成用户向量，训练目标把下一次观看建模为大规模多分类；服务时用近邻检索取候选。 三 seed 下 NDCG@10 为 0.02854→0.02666，该缩放设置未复现论文方向性收益，作为负结果保留。复现级别：核心机制复现。复现级别：核心机制复现。实际训练历史聚合、非线性用户塔和 item embedding 打分；YouTube 私有日志及生产 sampled softmax 未复刻。本地对照口径：基线为历史均值 two-tower，实验组增加 YouTube DNN 非线性用户塔；NDCG@10 相对 -6.61%，见 metrics/movielens-100k-seeds42-44.json。  retrieval ranking classic two-stage 搜广推 候选生成与搜索匹配">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<h2 id="paper-recommendation-youtube-dnn-d653b9f6">Deep Neural Networks for YouTube Recommendations</h2>
<p class="ar-learning-card__meta">Google / YouTube · 论文公开：2016-09-15</p>
<p><strong>方法要点：</strong>YouTube 将推荐拆成候选生成与精排。候选阶段要从百万量级视频中快速召回，传统矩阵分解难以吸收异构历史和上下文。观看历史 embedding 经过聚合和多层网络形成用户向量，训练目标把下一次观看建模为大规模多分类；服务时用近邻检索取候选。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>三 seed 下 NDCG@10 为 0.02854→0.02666，该缩放设置未复现论文方向性收益，作为负结果保留。复现级别：核心机制复现。复现级别：核心机制复现。实际训练历史聚合、非线性用户塔和 item embedding 打分；YouTube 私有日志及生产 sampled softmax 未复刻。本地对照口径：基线为历史均值 two-tower，实验组增加 YouTube DNN 非线性用户塔；NDCG@10 相对 -6.61%，见 metrics/movielens-100k-seeds42-44.json。</p></details>
<p class="ar-learning-card__links"><a href="https://research.google/pubs/deep-neural-networks-for-youtube-recommendations/">原论文</a> · <a href="../../../../reproductions/recsys2016-youtube-dnn-youtube-dnn/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
