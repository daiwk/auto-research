---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 语义表征、用户知识与冷启动

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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:finesid" data-paper-title="Progressive Learning from Content to Relevance to Personalization for CTR Prediction" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Progressive Learning from Content to Relevance to Personalization for CTR Prediction 搜广推与 LLM 应用 Alibaba Group 2026-10-21 将内容直接压成一个语义ID会丢失局部视觉细节；只对 embedding 做相关性预训又不能给最终交互网络提供足够初始化。FineSID 用细粒度离散视觉/文本 token，先把完整共享预测器训成 query-item 语义相关性模型，再迁移到个性化 CTR。关键不是单独的 SID lookup，而是三个阶段之间保留同一交互骨干并迁移完整参数/状态。把随机 token 或简单加权器接到现有 CTR 模型，不能替代整篇论文。 因此本轮只完成论文、方法与线上证据收录，成本过高，不复现（审查 DONE）。完整训练使用64张 H20，每卡 batch4096、全局 batch262144。数据包含512亿曝光、2.51亿用户、2亿 query、4.18亿商品，以及4.53亿次测试曝光；相关性教师还依赖大规模专家标注/私有数据。  排序与长序列建模 预训练与参数高效迁移 搜广推 语义表征、用户知识与冷启动 FineSID 为什么保留细粒度视觉与文本 token，而不只生成一个商品摘要码？ 单个码会压掉局部纹理、区域和文本细节，相关性与点击判断却可能恰好依赖这些差别。细粒度离散 token 提供更丰富交互单位，再经相关性预训连接查询与商品。更多 token 也增加训练与服务成本，不能把细粒度直接等同于更好推荐。 示意：两件外套整体相似，用户只关心袖口或口袋设计；单个摘要码可能混淆，局部 token 才有机会保留决定点击的细节。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-finesid-1b73a633" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e9710414fc4bd3e4">FineSID 为什么保留细粒度视觉与文本 token，而不只生成一个商品摘要码？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Afinesid">Progressive Learning from Content to Relevance to Personalization for CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单个码会压掉局部纹理、区域和文本细节，相关性与点击判断却可能恰好依赖这些差别。细粒度离散 token 提供更丰富交互单位，再经相关性预训连接查询与商品。更多 token 也增加训练与服务成本，不能把细粒度直接等同于更好推荐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两件外套整体相似，用户只关心袖口或口袋设计；单个摘要码可能混淆，局部 token 才有机会保留决定点击的细节。</p>
<p class="ar-learning-sources">依据：背景与主要改动、三阶段结构、成本判定：不执行复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.29138v1">原论文</a> · <a href="../../../../recommendation-components/2610.29138-finesid/">实现解读</a> · <a href="#qa-e9710414fc4bd3e4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:finesid" data-paper-title="Progressive Learning from Content to Relevance to Personalization for CTR Prediction" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Progressive Learning from Content to Relevance to Personalization for CTR Prediction 搜广推与 LLM 应用 Alibaba Group 2026-10-21 将内容直接压成一个语义ID会丢失局部视觉细节；只对 embedding 做相关性预训又不能给最终交互网络提供足够初始化。FineSID 用细粒度离散视觉/文本 token，先把完整共享预测器训成 query-item 语义相关性模型，再迁移到个性化 CTR。关键不是单独的 SID lookup，而是三个阶段之间保留同一交互骨干并迁移完整参数/状态。把随机 token 或简单加权器接到现有 CTR 模型，不能替代整篇论文。 因此本轮只完成论文、方法与线上证据收录，成本过高，不复现（审查 DONE）。完整训练使用64张 H20，每卡 batch4096、全局 batch262144。数据包含512亿曝光、2.51亿用户、2亿 query、4.18亿商品，以及4.53亿次测试曝光；相关性教师还依赖大规模专家标注/私有数据。  排序与长序列建模 预训练与参数高效迁移 搜广推 语义表征、用户知识与冷启动 FineSID从相关性预训迁移到CTR时，为什么不能只复制SID embedding？ 相关性阶段训练的是包含有序内容融合与HiFormer交互的完整共享预测器，知识同时存在于embedding、稠密层和归一化状态。只复制词表会丢掉大部分已学交互；迁移还须按约定更换CTR头并处理优化器状态。原文大规模实验成本过高，本库只收录方法与证据，不能用随机token小夹具替代整条链路。 示意：预训已学会查询中的用途如何与图像局部细节交叉，只搬商品短码就像只带走字典、不带走阅读能力；后续点击训练还得从头重学这些交互。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f378d3166750e8f2">FineSID从相关性预训迁移到CTR时，为什么不能只复制SID embedding？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Afinesid">Progressive Learning from Content to Relevance to Personalization for CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相关性阶段训练的是包含有序内容融合与HiFormer交互的完整共享预测器，知识同时存在于embedding、稠密层和归一化状态。只复制词表会丢掉大部分已学交互；迁移还须按约定更换CTR头并处理优化器状态。原文大规模实验成本过高，本库只收录方法与证据，不能用随机token小夹具替代整条链路。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>预训已学会查询中的用途如何与图像局部细节交叉，只搬商品短码就像只带走字典、不带走阅读能力；后续点击训练还得从头重学这些交互。</p>
<p class="ar-learning-sources">依据：背景与主要改动、三阶段结构、成本判定：不执行复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.29138v1">原论文</a> · <a href="../../../../recommendation-components/2610.29138-finesid/">实现解读</a> · <a href="#qa-f378d3166750e8f2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:finesid" data-paper-title="Progressive Learning from Content to Relevance to Personalization for CTR Prediction" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Progressive Learning from Content to Relevance to Personalization for CTR Prediction 搜广推与 LLM 应用 Alibaba Group 2026-10-21 将内容直接压成一个语义ID会丢失局部视觉细节；只对 embedding 做相关性预训又不能给最终交互网络提供足够初始化。FineSID 用细粒度离散视觉/文本 token，先把完整共享预测器训成 query-item 语义相关性模型，再迁移到个性化 CTR。关键不是单独的 SID lookup，而是三个阶段之间保留同一交互骨干并迁移完整参数/状态。把随机 token 或简单加权器接到现有 CTR 模型，不能替代整篇论文。 因此本轮只完成论文、方法与线上证据收录，成本过高，不复现（审查 DONE）。完整训练使用64张 H20，每卡 batch4096、全局 batch262144。数据包含512亿曝光、2.51亿用户、2亿 query、4.18亿商品，以及4.53亿次测试曝光；相关性教师还依赖大规模专家标注/私有数据。  排序与长序列建模 预训练与参数高效迁移 搜广推 语义表征、用户知识与冷启动 FineSID 的完整预测器迁移与冻结内容 encoder 后加新 CTR 头，知识复用层次有什么不同？ 后者主要搬运内容表征，FineSID 还保留相关性阶段学到的跨 token 融合、交互网络与状态，让 CTR 接着已有匹配能力适配个性化。迁移更完整也更昂贵，阶段接口需严格一致；来源本库是成本审查完成，没有缩小模型效果证据。 示意：只带走内容词典与连阅读理解网络一起迁移不同；前者知道词含义，后者还保留查询条件怎样与商品局部特征组合的能力。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a81772613dcdad3d">FineSID 的完整预测器迁移与冻结内容 encoder 后加新 CTR 头，知识复用层次有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Afinesid">Progressive Learning from Content to Relevance to Personalization for CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>后者主要搬运内容表征，FineSID 还保留相关性阶段学到的跨 token 融合、交互网络与状态，让 CTR 接着已有匹配能力适配个性化。迁移更完整也更昂贵，阶段接口需严格一致；来源本库是成本审查完成，没有缩小模型效果证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>只带走内容词典与连阅读理解网络一起迁移不同；前者知道词含义，后者还保留查询条件怎样与商品局部特征组合的能力。</p>
<p class="ar-learning-sources">依据：背景与主要改动、三阶段结构、成本判定：不执行复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.29138v1">原论文</a> · <a href="../../../../recommendation-components/2610.29138-finesid/">实现解读</a> · <a href="#qa-a81772613dcdad3d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:finesid" data-paper-title="Progressive Learning from Content to Relevance to Personalization for CTR Prediction" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Progressive Learning from Content to Relevance to Personalization for CTR Prediction 搜广推与 LLM 应用 Alibaba Group 2026-10-21 将内容直接压成一个语义ID会丢失局部视觉细节；只对 embedding 做相关性预训又不能给最终交互网络提供足够初始化。FineSID 用细粒度离散视觉/文本 token，先把完整共享预测器训成 query-item 语义相关性模型，再迁移到个性化 CTR。关键不是单独的 SID lookup，而是三个阶段之间保留同一交互骨干并迁移完整参数/状态。把随机 token 或简单加权器接到现有 CTR 模型，不能替代整篇论文。 因此本轮只完成论文、方法与线上证据收录，成本过高，不复现（审查 DONE）。完整训练使用64张 H20，每卡 batch4096、全局 batch262144。数据包含512亿曝光、2.51亿用户、2亿 query、4.18亿商品，以及4.53亿次测试曝光；相关性教师还依赖大规模专家标注/私有数据。  排序与长序列建模 预训练与参数高效迁移 搜广推 语义表征、用户知识与冷启动 实现 FineSID 阶段切换时，为什么 optimizer 状态与归一化状态也需要明确处理？ 完整参数迁移不能只复制 SID embedding，交互层和归一化统计同样影响输出；优化器状态保留还是重置必须按阶段约定，否则训练动力学改变。CTR 任务头转换也需显式匹配。这里是论文关键实现契约，本地没有运行训练可供效果验收。 示意：搬了权重却丢失对应归一化状态，表示尺度可能突变；把旧任务的优化动量无说明套到新 CTR 头，也不能称无差别复现阶段迁移。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1f9ddee4a7682fef">实现 FineSID 阶段切换时，为什么 optimizer 状态与归一化状态也需要明确处理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Afinesid">Progressive Learning from Content to Relevance to Personalization for CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>完整参数迁移不能只复制 SID embedding，交互层和归一化统计同样影响输出；优化器状态保留还是重置必须按阶段约定，否则训练动力学改变。CTR 任务头转换也需显式匹配。这里是论文关键实现契约，本地没有运行训练可供效果验收。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>搬了权重却丢失对应归一化状态，表示尺度可能突变；把旧任务的优化动量无说明套到新 CTR 头，也不能称无差别复现阶段迁移。</p>
<p class="ar-learning-sources">依据：三阶段结构、成本判定：不执行复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.29138v1">原论文</a> · <a href="../../../../recommendation-components/2610.29138-finesid/">实现解读</a> · <a href="#qa-1f9ddee4a7682fef">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sid-topology" data-paper-title="Don&#x27;t Rewrite the SID Map: Topology Preservation for Generative Retrieval in Dynamic E-Commerce Search" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Don&#x27;t Rewrite the SID Map: Topology Preservation for Generative Retrieval in Dynamic E-Commerce Search 搜广推与 LLM 应用 Alibaba / Taobao &amp; Tmall Group 2026-10-19 生成式检索学习的是从查询到多级SID的解码路径，重新按业务价值排序旧商品会改变路径含义。论文把“映射更新”和“继续训练”拆开，发现大beam可以掩盖窄beam下的严重漂移；短预算warm-start也不能修复任意重映射。方法保留全部旧商品的三层SID，新商品先由外部RQ-VAE得到两层语义前缀，再按当前业务价值排名插入第三层。头部初始分配独占token，尾部采用固定容量共享桶；新商品插入头部时可以与原独占token碰撞，但不能顺移旧商品来强行消碰撞。 64卡完整训练和生产实验成本过高，不复现（审查 DONE）。已实现CPU映射组件，证据为L1机制诊断；已实现CPU映射组件，证据为L1机制诊断；不是RQ-VAE/LLM检索能力复现。64卡完整训练和生产实验成本过高，不复现（审查 DONE）。真实执行价值先验、初始HC分配、新商品插入、碰撞展开、旧路径漂移统计；用独立预期桶、插入顺序不变性、头部碰撞和全重映射负对照验收。frozen_old_path_address_recovery只是合成映射中旧地址仍能找回成员，不是推荐准确率、HitRate或模型成功率。没有量化器、语义编码器、beam-search模型或生产A/B，也未接入Evolve。  生成式推荐 语义标识与增量更新 搜广推 语义表征、用户知识与冷启动 SID Topology为什么把映射更新与继续训练分开审查？ 生成检索学到的是query到SID路径，重映射旧商品会改变已学路径含义。继续训练不必修复任意重排，因此更新目录与模型是两个独立变化。 例如原码通向鞋，重排后通向包，旧模型即便输出同码也已指错商品。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-sid-topology-a240bd6b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8465febb5f404e8f">SID Topology为什么把映射更新与继续训练分开审查？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asid-topology">Don&#x27;t Rewrite the SID Map: Topology Preservation for Generative Retrieval in Dynamic E-Commerce Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao &amp; Tmall Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>生成检索学到的是query到SID路径，重映射旧商品会改变已学路径含义。继续训练不必修复任意重排，因此更新目录与模型是两个独立变化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如原码通向鞋，重排后通向包，旧模型即便输出同码也已指错商品。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.26105v1">原论文</a> · <a href="../../../../recommendation-components/2610.26105-sid-topology/">实现解读</a> · <a href="#qa-8465febb5f404e8f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sid-topology" data-paper-title="Don&#x27;t Rewrite the SID Map: Topology Preservation for Generative Retrieval in Dynamic E-Commerce Search" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Don&#x27;t Rewrite the SID Map: Topology Preservation for Generative Retrieval in Dynamic E-Commerce Search 搜广推与 LLM 应用 Alibaba / Taobao &amp; Tmall Group 2026-10-19 生成式检索学习的是从查询到多级SID的解码路径，重新按业务价值排序旧商品会改变路径含义。论文把“映射更新”和“继续训练”拆开，发现大beam可以掩盖窄beam下的严重漂移；短预算warm-start也不能修复任意重映射。方法保留全部旧商品的三层SID，新商品先由外部RQ-VAE得到两层语义前缀，再按当前业务价值排名插入第三层。头部初始分配独占token，尾部采用固定容量共享桶；新商品插入头部时可以与原独占token碰撞，但不能顺移旧商品来强行消碰撞。 64卡完整训练和生产实验成本过高，不复现（审查 DONE）。已实现CPU映射组件，证据为L1机制诊断；已实现CPU映射组件，证据为L1机制诊断；不是RQ-VAE/LLM检索能力复现。64卡完整训练和生产实验成本过高，不复现（审查 DONE）。真实执行价值先验、初始HC分配、新商品插入、碰撞展开、旧路径漂移统计；用独立预期桶、插入顺序不变性、头部碰撞和全重映射负对照验收。frozen_old_path_address_recovery只是合成映射中旧地址仍能找回成员，不是推荐准确率、HitRate或模型成功率。没有量化器、语义编码器、beam-search模型或生产A/B，也未接入Evolve。  生成式推荐 语义标识与增量更新 搜广推 语义表征、用户知识与冷启动 SID-Topology 为什么允许新商品与旧头部 token 碰撞，却不顺移旧商品来消除碰撞？ 生成器已经学会查询到旧 SID 路径的含义，顺移旧商品会把原有概率质量导向别的对象，短预算继续训练也未必修复。保留旧路径把更新影响局限于新商品插入，头部碰撞由展开处理，而非全局重映射。大 beam 可能掩盖窄 beam 的漂移，因此评估需检查路径稳定性，不能只看宽束结果。 示意：模型熟悉编码 A 指向旧商品甲，新商品乙加入时若把甲改到 B，原来生成 A 的请求就错位。宁可让 A 对应可展开的碰撞集合，也先保留甲的旧地址。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f1d31f957c262580">SID-Topology 为什么允许新商品与旧头部 token 碰撞，却不顺移旧商品来消除碰撞？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asid-topology">Don&#x27;t Rewrite the SID Map: Topology Preservation for Generative Retrieval in Dynamic E-Commerce Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao &amp; Tmall Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>生成器已经学会查询到旧 SID 路径的含义，顺移旧商品会把原有概率质量导向别的对象，短预算继续训练也未必修复。保留旧路径把更新影响局限于新商品插入，头部碰撞由展开处理，而非全局重映射。大 beam 可能掩盖窄 beam 的漂移，因此评估需检查路径稳定性，不能只看宽束结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型熟悉编码 A 指向旧商品甲，新商品乙加入时若把甲改到 B，原来生成 A 的请求就错位。宁可让 A 对应可展开的碰撞集合，也先保留甲的旧地址。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.26105v1">原论文</a> · <a href="../../../../recommendation-components/2610.26105-sid-topology/">实现解读</a> · <a href="#qa-f1d31f957c262580">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sid-topology" data-paper-title="Don&#x27;t Rewrite the SID Map: Topology Preservation for Generative Retrieval in Dynamic E-Commerce Search" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Don&#x27;t Rewrite the SID Map: Topology Preservation for Generative Retrieval in Dynamic E-Commerce Search 搜广推与 LLM 应用 Alibaba / Taobao &amp; Tmall Group 2026-10-19 生成式检索学习的是从查询到多级SID的解码路径，重新按业务价值排序旧商品会改变路径含义。论文把“映射更新”和“继续训练”拆开，发现大beam可以掩盖窄beam下的严重漂移；短预算warm-start也不能修复任意重映射。方法保留全部旧商品的三层SID，新商品先由外部RQ-VAE得到两层语义前缀，再按当前业务价值排名插入第三层。头部初始分配独占token，尾部采用固定容量共享桶；新商品插入头部时可以与原独占token碰撞，但不能顺移旧商品来强行消碰撞。 64卡完整训练和生产实验成本过高，不复现（审查 DONE）。已实现CPU映射组件，证据为L1机制诊断；已实现CPU映射组件，证据为L1机制诊断；不是RQ-VAE/LLM检索能力复现。64卡完整训练和生产实验成本过高，不复现（审查 DONE）。真实执行价值先验、初始HC分配、新商品插入、碰撞展开、旧路径漂移统计；用独立预期桶、插入顺序不变性、头部碰撞和全重映射负对照验收。frozen_old_path_address_recovery只是合成映射中旧地址仍能找回成员，不是推荐准确率、HitRate或模型成功率。没有量化器、语义编码器、beam-search模型或生产A/B，也未接入Evolve。  生成式推荐 语义标识与增量更新 搜广推 语义表征、用户知识与冷启动 大beam效果尚可为何不证明重映射没有损伤？ 宽搜索可能掩盖窄beam路径漂移，实际服务预算较窄时损害更明显。应分别测映射与训练影响，不用宽beam平均结果替代路径稳定性证据。 例如正确商品还在很深候选里，宽beam找到它不代表首几条路径仍正常。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-6d059fc4eff6fbca">大beam效果尚可为何不证明重映射没有损伤？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asid-topology">Don&#x27;t Rewrite the SID Map: Topology Preservation for Generative Retrieval in Dynamic E-Commerce Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao &amp; Tmall Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>宽搜索可能掩盖窄beam路径漂移，实际服务预算较窄时损害更明显。应分别测映射与训练影响，不用宽beam平均结果替代路径稳定性证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如正确商品还在很深候选里，宽beam找到它不代表首几条路径仍正常。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.26105v1">原论文</a> · <a href="../../../../recommendation-components/2610.26105-sid-topology/">实现解读</a> · <a href="#qa-6d059fc4eff6fbca">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sid-topology" data-paper-title="Don&#x27;t Rewrite the SID Map: Topology Preservation for Generative Retrieval in Dynamic E-Commerce Search" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Don&#x27;t Rewrite the SID Map: Topology Preservation for Generative Retrieval in Dynamic E-Commerce Search 搜广推与 LLM 应用 Alibaba / Taobao &amp; Tmall Group 2026-10-19 生成式检索学习的是从查询到多级SID的解码路径，重新按业务价值排序旧商品会改变路径含义。论文把“映射更新”和“继续训练”拆开，发现大beam可以掩盖窄beam下的严重漂移；短预算warm-start也不能修复任意重映射。方法保留全部旧商品的三层SID，新商品先由外部RQ-VAE得到两层语义前缀，再按当前业务价值排名插入第三层。头部初始分配独占token，尾部采用固定容量共享桶；新商品插入头部时可以与原独占token碰撞，但不能顺移旧商品来强行消碰撞。 64卡完整训练和生产实验成本过高，不复现（审查 DONE）。已实现CPU映射组件，证据为L1机制诊断；已实现CPU映射组件，证据为L1机制诊断；不是RQ-VAE/LLM检索能力复现。64卡完整训练和生产实验成本过高，不复现（审查 DONE）。真实执行价值先验、初始HC分配、新商品插入、碰撞展开、旧路径漂移统计；用独立预期桶、插入顺序不变性、头部碰撞和全重映射负对照验收。frozen_old_path_address_recovery只是合成映射中旧地址仍能找回成员，不是推荐准确率、HitRate或模型成功率。没有量化器、语义编码器、beam-search模型或生产A/B，也未接入Evolve。  生成式推荐 语义标识与增量更新 搜广推 语义表征、用户知识与冷启动 新增商品占到旧独占token时能顺移旧商品消碰撞吗？ 不能，保留式更新冻结所有旧SID，允许规定碰撞并解码全部成员；尾桶容量须显式，耗尽报错。未出现的旧商品也要保留，不能静默取模或重编码。 例如新商品进头部，不应把旧目录一串token向后挪一格。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0e6377b739111aaa">新增商品占到旧独占token时能顺移旧商品消碰撞吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asid-topology">Don&#x27;t Rewrite the SID Map: Topology Preservation for Generative Retrieval in Dynamic E-Commerce Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao &amp; Tmall Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，保留式更新冻结所有旧SID，允许规定碰撞并解码全部成员；尾桶容量须显式，耗尽报错。未出现的旧商品也要保留，不能静默取模或重编码。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如新商品进头部，不应把旧目录一串token向后挪一格。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.26105v1">原论文</a> · <a href="../../../../recommendation-components/2610.26105-sid-topology/">实现解读</a> · <a href="#qa-0e6377b739111aaa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:agent-web-rec" data-paper-title="AgentWebRec: Compact Evidence Fusion over the Agent Web for Personalized Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="AgentWebRec: Compact Evidence Fusion over the Agent Web for Personalized Recommendation 搜广推与 LLM 应用 Beihang University 2026-10-01 先从平台获取候选语义，再按语义相关性和时间衰减检索目标用户私有记忆；仅在本地证据置信度不足时查询邻居 Agent 的紧凑偏好模式。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。只执行有界检索与置信门控；不暴露私有记录，不运行 LLM Agent Web。只执行有界检索与置信门控；不暴露私有记录，不运行 LLM Agent Web。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  agent-recommendation private-memory evidence-fusion 搜广推 语义表征、用户知识与冷启动 AgentWebRec 的私有记忆与邻居偏好模式分别提供什么证据？ 私有记忆记录目标用户自身经历，候选语义与时间衰减用于检索当前相关部分；邻居模式补充本地证据不足时的群体线索。两者置信来源不同，协作不应覆盖已有强个人证据，也不应把邻居摘要当作目标用户已经发生的真实行为。 示意：用户自己明确偏好轻便相机时优先用这段记忆；只有新出现的户外需求缺少记录，才询问邻居的紧凑模式作为补充。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-agent-web-rec-883c9fbf" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4a24e04c7fcabf5a">AgentWebRec 的私有记忆与邻居偏好模式分别提供什么证据？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aagent-web-rec">AgentWebRec: Compact Evidence Fusion over the Agent Web for Personalized Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>私有记忆记录目标用户自身经历，候选语义与时间衰减用于检索当前相关部分；邻居模式补充本地证据不足时的群体线索。两者置信来源不同，协作不应覆盖已有强个人证据，也不应把邻居摘要当作目标用户已经发生的真实行为。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户自己明确偏好轻便相机时优先用这段记忆；只有新出现的户外需求缺少记录，才询问邻居的紧凑模式作为补充。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01705">原论文</a> · <a href="../../../../reproductions/2610.01705-agent-web-rec/">实现解读</a> · <a href="#qa-4a24e04c7fcabf5a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:agent-web-rec" data-paper-title="AgentWebRec: Compact Evidence Fusion over the Agent Web for Personalized Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="AgentWebRec: Compact Evidence Fusion over the Agent Web for Personalized Recommendation 搜广推与 LLM 应用 Beihang University 2026-10-01 先从平台获取候选语义，再按语义相关性和时间衰减检索目标用户私有记忆；仅在本地证据置信度不足时查询邻居 Agent 的紧凑偏好模式。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。只执行有界检索与置信门控；不暴露私有记录，不运行 LLM Agent Web。只执行有界检索与置信门控；不暴露私有记录，不运行 LLM Agent Web。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  agent-recommendation private-memory evidence-fusion 搜广推 语义表征、用户知识与冷启动 AgentWebRec为什么只在私有记忆证据不足时才向邻居Agent协作？ 目标用户的相关记忆通常比他人的概括偏好更直接，因此先按语义相关性与时间衰减检索本地证据。置信度不足才请求邻居提供紧凑模式，减少无关迁移与私有历史传播；协作是补证据而非把全网记忆无条件拼进提示。本地仅检验门控与证据融合，不等于验证完整推荐Agent能力。 示意：用户已多次记录素食偏好时无需询问邻居；若只留下模糊旅行兴趣，可借邻居的景点偏好模式补充，但不用发送用户原始行程。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f4633804b5ff7685">AgentWebRec为什么只在私有记忆证据不足时才向邻居Agent协作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aagent-web-rec">AgentWebRec: Compact Evidence Fusion over the Agent Web for Personalized Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标用户的相关记忆通常比他人的概括偏好更直接，因此先按语义相关性与时间衰减检索本地证据。置信度不足才请求邻居提供紧凑模式，减少无关迁移与私有历史传播；协作是补证据而非把全网记忆无条件拼进提示。本地仅检验门控与证据融合，不等于验证完整推荐Agent能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户已多次记录素食偏好时无需询问邻居；若只留下模糊旅行兴趣，可借邻居的景点偏好模式补充，但不用发送用户原始行程。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01705">原论文</a> · <a href="../../../../reproductions/2610.01705-agent-web-rec/">实现解读</a> · <a href="#qa-f4633804b5ff7685">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:agent-web-rec" data-paper-title="AgentWebRec: Compact Evidence Fusion over the Agent Web for Personalized Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="AgentWebRec: Compact Evidence Fusion over the Agent Web for Personalized Recommendation 搜广推与 LLM 应用 Beihang University 2026-10-01 先从平台获取候选语义，再按语义相关性和时间衰减检索目标用户私有记忆；仅在本地证据置信度不足时查询邻居 Agent 的紧凑偏好模式。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。只执行有界检索与置信门控；不暴露私有记录，不运行 LLM Agent Web。只执行有界检索与置信门控；不暴露私有记录，不运行 LLM Agent Web。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  agent-recommendation private-memory evidence-fusion 搜广推 语义表征、用户知识与冷启动 AgentWebRec 的条件协作与始终聚合邻居信息相比，主要取舍是什么？ 始终协作可能提高覆盖，却为每次请求增加通信与外部噪声；置信门控先使用个人证据，只在不足时扩展信息来源。代价是置信度若过于乐观会错过帮助，过低又近似总协作。来源本地仅诊断这条门控，不提供完整多 agent 能力提升证据。 示意：已有清晰摄影偏好时额外问邻居可能引入热门游戏内容；遇到全新需求再协作可以少传无关信息，但前提是系统能识别自己确实缺少证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0465c8ff0561e985">AgentWebRec 的条件协作与始终聚合邻居信息相比，主要取舍是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aagent-web-rec">AgentWebRec: Compact Evidence Fusion over the Agent Web for Personalized Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>始终协作可能提高覆盖，却为每次请求增加通信与外部噪声；置信门控先使用个人证据，只在不足时扩展信息来源。代价是置信度若过于乐观会错过帮助，过低又近似总协作。来源本地仅诊断这条门控，不提供完整多 agent 能力提升证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>已有清晰摄影偏好时额外问邻居可能引入热门游戏内容；遇到全新需求再协作可以少传无关信息，但前提是系统能识别自己确实缺少证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01705">原论文</a> · <a href="../../../../reproductions/2610.01705-agent-web-rec/">实现解读</a> · <a href="#qa-0465c8ff0561e985">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:agent-web-rec" data-paper-title="AgentWebRec: Compact Evidence Fusion over the Agent Web for Personalized Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="AgentWebRec: Compact Evidence Fusion over the Agent Web for Personalized Recommendation 搜广推与 LLM 应用 Beihang University 2026-10-01 先从平台获取候选语义，再按语义相关性和时间衰减检索目标用户私有记忆；仅在本地证据置信度不足时查询邻居 Agent 的紧凑偏好模式。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。只执行有界检索与置信门控；不暴露私有记录，不运行 LLM Agent Web。只执行有界检索与置信门控；不暴露私有记录，不运行 LLM Agent Web。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  agent-recommendation private-memory evidence-fusion 搜广推 语义表征、用户知识与冷启动 AgentWebRec 的时间衰减与协作阈值实现中，哪些边界要分开检查？ 记忆权重混合语义项和指数时间衰减，时间差应使用一致单位并避免未来事件得到反常增益；协作由本地置信 κ 与阈值比较，和记忆排序分不是同一个量。诊断需分别验证权重排序、过期行为处理与触发条件。 示意：一天与一小时若混用单位，旧行为可能几乎不衰减；即使检索到了最高分记忆，也仍要判断证据是否足够，不能把最高分自动视为高置信。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a6ad3296c97edfb6">AgentWebRec 的时间衰减与协作阈值实现中，哪些边界要分开检查？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aagent-web-rec">AgentWebRec: Compact Evidence Fusion over the Agent Web for Personalized Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>记忆权重混合语义项和指数时间衰减，时间差应使用一致单位并避免未来事件得到反常增益；协作由本地置信 κ 与阈值比较，和记忆排序分不是同一个量。诊断需分别验证权重排序、过期行为处理与触发条件。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一天与一小时若混用单位，旧行为可能几乎不衰减；即使检索到了最高分记忆，也仍要判断证据是否足够，不能把最高分自动视为高置信。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01705">原论文</a> · <a href="../../../../reproductions/2610.01705-agent-web-rec/">实现解读</a> · <a href="#qa-a6ad3296c97edfb6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gris" data-paper-title="Neither Black nor White: Balancing Semantic and Collaborative Signals with Graph-Informed Semantic IDs (GrIS)" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Neither Black nor White: Balancing Semantic and Collaborative Signals with Graph-Informed Semantic IDs (GrIS) 搜广推与 LLM 应用 Huawei Ireland Research Centre 2026-10-01 把 Semantic ID 构造重写为层级图划分：节点承载内容语义，边承载协同信号；图为空时退化为内容量化。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 graph-informed 层级二分 ID；用户批准为学术/Evolve 例外，无线上 A/B，不进入工业证据结论。收录例外：用户于 2026-10-02 明确批准的学术/Evolve 机制例外；论文没有量化线上 A/B，不进入工业证据结论。执行 graph-informed 层级二分 ID；用户批准为学术/Evolve 例外，无线上 A/B，不进入工业证据结论。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  generative-recommendation semantic-id graph-partition 搜广推 语义表征、用户知识与冷启动 GrIS 为什么把 SID 构造看成层级图划分？ 节点内容给出语义，协同边提供共同消费关系，递归划分将两者组织为粗到细的离散路径，使码不只优化内容重构。图结构也受曝光和热门度影响，层级不自动等同于真实兴趣 taxonomy，划分质量需独立检验。 示意：视觉不同的相机与镜头可能因共同消费连接，在上层形成相关兴趣区；下层再按内容区分，不能只按图片颜色分码。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-gris-e106351a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4ea41541f1d110b0">GrIS 为什么把 SID 构造看成层级图划分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agris">Neither Black nor White: Balancing Semantic and Collaborative Signals with Graph-Informed Semantic IDs (GrIS)</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Ireland Research Centre</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>节点内容给出语义，协同边提供共同消费关系，递归划分将两者组织为粗到细的离散路径，使码不只优化内容重构。图结构也受曝光和热门度影响，层级不自动等同于真实兴趣 taxonomy，划分质量需独立检验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>视觉不同的相机与镜头可能因共同消费连接，在上层形成相关兴趣区；下层再按内容区分，不能只按图片颜色分码。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01533">原论文</a> · <a href="../../../../reproductions/2610.01533-gris/">实现解读</a> · <a href="#qa-4ea41541f1d110b0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gris" data-paper-title="Neither Black nor White: Balancing Semantic and Collaborative Signals with Graph-Informed Semantic IDs (GrIS)" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Neither Black nor White: Balancing Semantic and Collaborative Signals with Graph-Informed Semantic IDs (GrIS) 搜广推与 LLM 应用 Huawei Ireland Research Centre 2026-10-01 把 Semantic ID 构造重写为层级图划分：节点承载内容语义，边承载协同信号；图为空时退化为内容量化。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 graph-informed 层级二分 ID；用户批准为学术/Evolve 例外，无线上 A/B，不进入工业证据结论。收录例外：用户于 2026-10-02 明确批准的学术/Evolve 机制例外；论文没有量化线上 A/B，不进入工业证据结论。执行 graph-informed 层级二分 ID；用户批准为学术/Evolve 例外，无线上 A/B，不进入工业证据结论。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  generative-recommendation semantic-id graph-partition 搜广推 语义表征、用户知识与冷启动 GrIS把SID构造写成图划分，为什么要同时看内容节点和协同边？ 内容相近与共同消费并不总重合，单纯内容量化可能错过偏好结构。图划分让语义特征与协同连接共同影响层级编码，保留两类信号间的折中；图缺失时则退回内容信息，而不能伪造协同关系。本地只检查划分与状态机制，层级结构本身并不证明生成推荐或线上效果已经成立。 示意：两件外观不同的露营用品经常被共同消费，协同边会提示它们的关系；刚上线的商品还没有边时，只能主要依据内容，而非假装已有行为支持。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-362f60f3895a3566">GrIS把SID构造写成图划分，为什么要同时看内容节点和协同边？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agris">Neither Black nor White: Balancing Semantic and Collaborative Signals with Graph-Informed Semantic IDs (GrIS)</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Ireland Research Centre</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>内容相近与共同消费并不总重合，单纯内容量化可能错过偏好结构。图划分让语义特征与协同连接共同影响层级编码，保留两类信号间的折中；图缺失时则退回内容信息，而不能伪造协同关系。本地只检查划分与状态机制，层级结构本身并不证明生成推荐或线上效果已经成立。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两件外观不同的露营用品经常被共同消费，协同边会提示它们的关系；刚上线的商品还没有边时，只能主要依据内容，而非假装已有行为支持。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01533">原论文</a> · <a href="../../../../reproductions/2610.01533-gris/">实现解读</a> · <a href="#qa-362f60f3895a3566">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gris" data-paper-title="Neither Black nor White: Balancing Semantic and Collaborative Signals with Graph-Informed Semantic IDs (GrIS)" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Neither Black nor White: Balancing Semantic and Collaborative Signals with Graph-Informed Semantic IDs (GrIS) 搜广推与 LLM 应用 Huawei Ireland Research Centre 2026-10-01 把 Semantic ID 构造重写为层级图划分：节点承载内容语义，边承载协同信号；图为空时退化为内容量化。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 graph-informed 层级二分 ID；用户批准为学术/Evolve 例外，无线上 A/B，不进入工业证据结论。收录例外：用户于 2026-10-02 明确批准的学术/Evolve 机制例外；论文没有量化线上 A/B，不进入工业证据结论。执行 graph-informed 层级二分 ID；用户批准为学术/Evolve 例外，无线上 A/B，不进入工业证据结论。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  generative-recommendation semantic-id graph-partition 搜广推 语义表征、用户知识与冷启动 GrIS 图为空时退化为内容量化，与无图仍编造邻接有何不同？ 退化路径承认缺少协同证据，只使用可用内容，保留定义清晰的对照。虚构边会把启发规则伪装为观测行为，改变学习目标。图有无应作为机制条件报告，本地诊断不意味着大规模推荐质量已验证。 示意：新品完全无互动时可按标题语义分层，不能随便连到几个热门商品再声称学到了协同图；两条路径证据来源不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4acebc44815e676c">GrIS 图为空时退化为内容量化，与无图仍编造邻接有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agris">Neither Black nor White: Balancing Semantic and Collaborative Signals with Graph-Informed Semantic IDs (GrIS)</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Ireland Research Centre</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>退化路径承认缺少协同证据，只使用可用内容，保留定义清晰的对照。虚构边会把启发规则伪装为观测行为，改变学习目标。图有无应作为机制条件报告，本地诊断不意味着大规模推荐质量已验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新品完全无互动时可按标题语义分层，不能随便连到几个热门商品再声称学到了协同图；两条路径证据来源不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01533">原论文</a> · <a href="../../../../reproductions/2610.01533-gris/">实现解读</a> · <a href="#qa-4acebc44815e676c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gris" data-paper-title="Neither Black nor White: Balancing Semantic and Collaborative Signals with Graph-Informed Semantic IDs (GrIS)" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Neither Black nor White: Balancing Semantic and Collaborative Signals with Graph-Informed Semantic IDs (GrIS) 搜广推与 LLM 应用 Huawei Ireland Research Centre 2026-10-01 把 Semantic ID 构造重写为层级图划分：节点承载内容语义，边承载协同信号；图为空时退化为内容量化。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 graph-informed 层级二分 ID；用户批准为学术/Evolve 例外，无线上 A/B，不进入工业证据结论。收录例外：用户于 2026-10-02 明确批准的学术/Evolve 机制例外；论文没有量化线上 A/B，不进入工业证据结论。执行 graph-informed 层级二分 ID；用户批准为学术/Evolve 例外，无线上 A/B，不进入工业证据结论。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  generative-recommendation semantic-id graph-partition 搜广推 语义表征、用户知识与冷启动 实现 GrIS 递归划分时，为什么每层要同时保存节点身份与父路径？ 下一层只能在当前子图或节点组内继续细分，若丢掉父路径就可能把不同分支的局部编号混为同一码。图平滑、语义组合和空图处理也应显式执行。代码产生若干整数并不证明实现了内容—协同共同驱动的层级结构。 示意：两个父簇都有子编号二，完整 SID 应不同；只保存二会让两个不相关子簇碰撞，失去递归划分的地址含义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b80b3cbd72b4d963">实现 GrIS 递归划分时，为什么每层要同时保存节点身份与父路径？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agris">Neither Black nor White: Balancing Semantic and Collaborative Signals with Graph-Informed Semantic IDs (GrIS)</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Ireland Research Centre</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>下一层只能在当前子图或节点组内继续细分，若丢掉父路径就可能把不同分支的局部编号混为同一码。图平滑、语义组合和空图处理也应显式执行。代码产生若干整数并不证明实现了内容—协同共同驱动的层级结构。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个父簇都有子编号二，完整 SID 应不同；只保存二会让两个不相关子簇碰撞，失去递归划分的地址含义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01533">原论文</a> · <a href="../../../../reproductions/2610.01533-gris/">实现解读</a> · <a href="#qa-b80b3cbd72b4d963">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:kuafu" data-paper-title="KuaFu: Compressing Long User Behavior into Understanding at Billion Scale" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="KuaFu: Compressing Long User Behavior into Understanding at Billion Scale 搜广推与 LLM 应用 Tencent 2026-09-25 腾讯需要每周为海量用户刷新画像。逐条把原始行为文本送进大模型既慢又占空间；只截断长历史又容易遗漏时间、兴趣和因果信息。KuaFu 把单个行为条目作为最小压缩单位：压缩器对每条独立编码；投影器把 m 个高维记忆 token 降为 k 个低维缓存向量；解码器按用户行为顺序接收这些向量和任务提示。这样同一条目可以跨用户复用，不必因为某个用户新增行为而重算整个历史。原论文的Figure 1 和 Figure 2分别展示生产缓存链路及双轴投影结构；图片版权归原作者。 复现级别：公开数据概念验证，尚未复现论文效果。复现级别：公开数据概念验证，尚未复现论文效果。本地真实运行 Qwen3-4B-Instruct、独立条目压缩、双轴投影和三段监督训练；幻觉感知 DAPO 的代码已实现并在 A100 执行采样与打分，但固定公开样例同组奖励相同，更新被正确跳过。不能把该运行称作四阶段训练完成，更不能将 MRQA 指标等同于腾讯线上 GMV。本地对照口径：同解码器、同源 token 数的开头截断输入作为诊断基线，压缩缓存为实验组；dev F1 相对 -23.4%，但该输入消融不是独立训练的正式基线。  long-behavior item-compression hallucination-aware-rl 搜广推 语义表征、用户知识与冷启动 KuaFu 为什么同时在记忆 token 数和通道维度上压缩？ 每条行为先由高维记忆表达，再投影到更少、更低维的缓存，分别减少序列位置和存储带宽；解码器按顺序组合这些条目。两轴都压缩会增加信息损失风险，不能把能重建部分回答理解为保留全部时间与因果关系。 示意：一条二十四词事件压成两个低维向量，比仅把词数减半更省缓存，但其中人名或时间可能丢失，需由任务指标检验而非只数压缩率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-kuafu-25c887d3" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0262d391f69475fd">KuaFu 为什么同时在记忆 token 数和通道维度上压缩？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Akuafu">KuaFu: Compressing Long User Behavior into Understanding at Billion Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每条行为先由高维记忆表达，再投影到更少、更低维的缓存，分别减少序列位置和存储带宽；解码器按顺序组合这些条目。两轴都压缩会增加信息损失风险，不能把能重建部分回答理解为保留全部时间与因果关系。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一条二十四词事件压成两个低维向量，比仅把词数减半更省缓存，但其中人名或时间可能丢失，需由任务指标检验而非只数压缩率。</p>
<p class="ar-learning-sources">依据：背景与主要改动、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.31045">原论文</a> · <a href="../../../../reproductions/2609.31045-kuafu/">实现解读</a> · <a href="#qa-0262d391f69475fd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:kuafu" data-paper-title="KuaFu: Compressing Long User Behavior into Understanding at Billion Scale" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="KuaFu: Compressing Long User Behavior into Understanding at Billion Scale 搜广推与 LLM 应用 Tencent 2026-09-25 腾讯需要每周为海量用户刷新画像。逐条把原始行为文本送进大模型既慢又占空间；只截断长历史又容易遗漏时间、兴趣和因果信息。KuaFu 把单个行为条目作为最小压缩单位：压缩器对每条独立编码；投影器把 m 个高维记忆 token 降为 k 个低维缓存向量；解码器按用户行为顺序接收这些向量和任务提示。这样同一条目可以跨用户复用，不必因为某个用户新增行为而重算整个历史。原论文的Figure 1 和 Figure 2分别展示生产缓存链路及双轴投影结构；图片版权归原作者。 复现级别：公开数据概念验证，尚未复现论文效果。复现级别：公开数据概念验证，尚未复现论文效果。本地真实运行 Qwen3-4B-Instruct、独立条目压缩、双轴投影和三段监督训练；幻觉感知 DAPO 的代码已实现并在 A100 执行采样与打分，但固定公开样例同组奖励相同，更新被正确跳过。不能把该运行称作四阶段训练完成，更不能将 MRQA 指标等同于腾讯线上 GMV。本地对照口径：同解码器、同源 token 数的开头截断输入作为诊断基线，压缩缓存为实验组；dev F1 相对 -23.4%，但该输入消融不是独立训练的正式基线。  long-behavior item-compression hallucination-aware-rl 搜广推 语义表征、用户知识与冷启动 KuaFu为什么按单条行为压缩和缓存，而不是先把整段用户历史压成一份向量？ 单条行为可被多个用户或不同画像任务复用，独立压缩后新增一条事件只需补充对应缓存。整段历史压缩则会把共享内容与用户上下文绑定，任何变化都可能要求重算。解码器仍按时间顺序读取压缩结果，保留组合解释机会；压缩会损失信息，本地诊断负结果不能被缓存效率掩盖。 示意：同一条视频行为的内容编码可供多位用户复用；某人今天多看一条，只增加该条缓存再按其历史顺序解码，不必重跑所有旧行为的文本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-dfd1f5565460f95f">KuaFu为什么按单条行为压缩和缓存，而不是先把整段用户历史压成一份向量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Akuafu">KuaFu: Compressing Long User Behavior into Understanding at Billion Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单条行为可被多个用户或不同画像任务复用，独立压缩后新增一条事件只需补充对应缓存。整段历史压缩则会把共享内容与用户上下文绑定，任何变化都可能要求重算。解码器仍按时间顺序读取压缩结果，保留组合解释机会；压缩会损失信息，本地诊断负结果不能被缓存效率掩盖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一条视频行为的内容编码可供多位用户复用；某人今天多看一条，只增加该条缓存再按其历史顺序解码，不必重跑所有旧行为的文本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.31045">原论文</a> · <a href="../../../../reproductions/2609.31045-kuafu/">实现解读</a> · <a href="#qa-dfd1f5565460f95f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:kuafu" data-paper-title="KuaFu: Compressing Long User Behavior into Understanding at Billion Scale" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="KuaFu: Compressing Long User Behavior into Understanding at Billion Scale 搜广推与 LLM 应用 Tencent 2026-09-25 腾讯需要每周为海量用户刷新画像。逐条把原始行为文本送进大模型既慢又占空间；只截断长历史又容易遗漏时间、兴趣和因果信息。KuaFu 把单个行为条目作为最小压缩单位：压缩器对每条独立编码；投影器把 m 个高维记忆 token 降为 k 个低维缓存向量；解码器按用户行为顺序接收这些向量和任务提示。这样同一条目可以跨用户复用，不必因为某个用户新增行为而重算整个历史。原论文的Figure 1 和 Figure 2分别展示生产缓存链路及双轴投影结构；图片版权归原作者。 复现级别：公开数据概念验证，尚未复现论文效果。复现级别：公开数据概念验证，尚未复现论文效果。本地真实运行 Qwen3-4B-Instruct、独立条目压缩、双轴投影和三段监督训练；幻觉感知 DAPO 的代码已实现并在 A100 执行采样与打分，但固定公开样例同组奖励相同，更新被正确跳过。不能把该运行称作四阶段训练完成，更不能将 MRQA 指标等同于腾讯线上 GMV。本地对照口径：同解码器、同源 token 数的开头截断输入作为诊断基线，压缩缓存为实验组；dev F1 相对 -23.4%，但该输入消融不是独立训练的正式基线。  long-behavior item-compression hallucination-aware-rl 搜广推 语义表征、用户知识与冷启动 KuaFu 的输入消融与独立训练原文对照，为什么证据强度不同？ 复用压缩输入训练过的解码器再换原文，比较受输入分布适配影响；独立对照至少另起相同模型按原文预算训练，才更接近训练路径比较。来源补做独立对照后仍为负，且并非等 FLOPs 正式对比，不能只报压缩效率。 示意：让只练过压缩码的解码器突然读截断文字，差结果可能来自没适应；重新训练原文分支再比较，才能减少这项混淆。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-27c383a0aff67bc2">KuaFu 的输入消融与独立训练原文对照，为什么证据强度不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Akuafu">KuaFu: Compressing Long User Behavior into Understanding at Billion Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>复用压缩输入训练过的解码器再换原文，比较受输入分布适配影响；独立对照至少另起相同模型按原文预算训练，才更接近训练路径比较。来源补做独立对照后仍为负，且并非等 FLOPs 正式对比，不能只报压缩效率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>让只练过压缩码的解码器突然读截断文字，差结果可能来自没适应；重新训练原文分支再比较，才能减少这项混淆。</p>
<p class="ar-learning-sources">依据：背景与主要改动、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.31045">原论文</a> · <a href="../../../../reproductions/2609.31045-kuafu/">实现解读</a> · <a href="#qa-27c383a0aff67bc2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:kuafu" data-paper-title="KuaFu: Compressing Long User Behavior into Understanding at Billion Scale" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="KuaFu: Compressing Long User Behavior into Understanding at Billion Scale 搜广推与 LLM 应用 Tencent 2026-09-25 腾讯需要每周为海量用户刷新画像。逐条把原始行为文本送进大模型既慢又占空间；只截断长历史又容易遗漏时间、兴趣和因果信息。KuaFu 把单个行为条目作为最小压缩单位：压缩器对每条独立编码；投影器把 m 个高维记忆 token 降为 k 个低维缓存向量；解码器按用户行为顺序接收这些向量和任务提示。这样同一条目可以跨用户复用，不必因为某个用户新增行为而重算整个历史。原论文的Figure 1 和 Figure 2分别展示生产缓存链路及双轴投影结构；图片版权归原作者。 复现级别：公开数据概念验证，尚未复现论文效果。复现级别：公开数据概念验证，尚未复现论文效果。本地真实运行 Qwen3-4B-Instruct、独立条目压缩、双轴投影和三段监督训练；幻觉感知 DAPO 的代码已实现并在 A100 执行采样与打分，但固定公开样例同组奖励相同，更新被正确跳过。不能把该运行称作四阶段训练完成，更不能将 MRQA 指标等同于腾讯线上 GMV。本地对照口径：同解码器、同源 token 数的开头截断输入作为诊断基线，压缩缓存为实验组；dev F1 相对 -23.4%，但该输入消融不是独立训练的正式基线。  long-behavior item-compression hallucination-aware-rl 搜广推 语义表征、用户知识与冷启动 KuaFu 的 RL smoke 全部 reward 相同时，为什么应记录 skipped_zero_advantage？ 组内奖励相同没有相对优势，策略梯度目标没有有效学习信号，调用优化器也不代表完成强化学习。来源明确保留空更新，QA 压缩训练与 RL 状态分别验收。不能将 GPU 上执行过一次前向写成奖励优化成功。 示意：四个回答奖励都一分，归一后优势为零，模型没有依据偏向哪条；应报告没有更新，而不是把四次高 reward 当作学会更好生成。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-766156687183b855">KuaFu 的 RL smoke 全部 reward 相同时，为什么应记录 skipped_zero_advantage？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Akuafu">KuaFu: Compressing Long User Behavior into Understanding at Billion Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>组内奖励相同没有相对优势，策略梯度目标没有有效学习信号，调用优化器也不代表完成强化学习。来源明确保留空更新，QA 压缩训练与 RL 状态分别验收。不能将 GPU 上执行过一次前向写成奖励优化成功。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>四个回答奖励都一分，归一后优势为零，模型没有依据偏向哪条；应报告没有更新，而不是把四次高 reward 当作学会更好生成。</p>
<p class="ar-learning-sources">依据：本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.31045">原论文</a> · <a href="../../../../reproductions/2609.31045-kuafu/">实现解读</a> · <a href="#qa-766156687183b855">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:music-rationales" data-paper-title="Explainable Recommendations at Scale: LLM Rationales for YouTube Music Artist Discovery" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Explainable Recommendations at Scale: LLM Rationales for YouTube Music Artist Discovery 搜广推与 LLM 应用 Google 2026-09-20 用户愿意听熟悉的艺人，却可能不敢点开陌生艺人。论文将计算昂贵的 Gemini 推理移到异步离线阶段：根据完整的听歌历史生成“发现画像”，包含未听过的艺人和个性化理由；通过实体标准化与 LLM 评审过滤不可信理由；在线阶段只取缓存的画像，缺失时退回原有推荐。这样既能给候选附上解释，又避免在用户请求链路上运行大模型。论文的多臂 holdback 把新增提名与理由标注分开，发现理由是主导 shelf engagement 提升的因素。 复现级别：公开数据概念验证。复现级别：公开数据概念验证。本地使用真实 Qwen2.5-7B-Instruct 生成新艺人提名与自然语言理由，执行目录映射、已听过过滤、理由证据检查及只读缓存在线回退。Google 的 Gemini、私有音乐知识图谱、LLM-as-a-Judge 和线上多臂 A/B 不可公开复刻；公开 Last.fm 命中率不是用户信任或线上互动效果。本地确实运行 7B 权重推理、目录/新颖性/共享标签约束以及缓存/回退路径；但既未调用 Gemini，也未复刻 Google 的专有 KG 和线上 judge。本地对照口径：原 CF 基线 test Hit@5 0.40；  music-discovery llm-rationale offline-online-decoupling 搜广推 语义表征、用户知识与冷启动 Music Rationales 的发现画像为什么包含未听艺人和个性化理由？ 陌生候选需要解释与用户既有兴趣的联系，画像将提名与理由一起准备，异步生成并校验实体和可信度。它帮助用户理解发现，而不是证明艺人真的符合口味；理由必须基于历史与内容，不能为了说服随意编造经历。 示意：用户常听钢琴三重奏，可说明新艺人与该编制的联系；若系统声称用户听过某艺人但记录没有，这不是个性化而是虚构。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-music-rationales-61aa6d5c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4fcfcf53f4a25dd8">Music Rationales 的发现画像为什么包含未听艺人和个性化理由？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amusic-rationales">Explainable Recommendations at Scale: LLM Rationales for YouTube Music Artist Discovery</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>陌生候选需要解释与用户既有兴趣的联系，画像将提名与理由一起准备，异步生成并校验实体和可信度。它帮助用户理解发现，而不是证明艺人真的符合口味；理由必须基于历史与内容，不能为了说服随意编造经历。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户常听钢琴三重奏，可说明新艺人与该编制的联系；若系统声称用户听过某艺人但记录没有，这不是个性化而是虚构。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与机制；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.23877">原论文</a> · <a href="../../../../reproductions/2609.23877-music-rationales/">实现解读</a> · <a href="#qa-4fcfcf53f4a25dd8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:music-rationales" data-paper-title="Explainable Recommendations at Scale: LLM Rationales for YouTube Music Artist Discovery" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Explainable Recommendations at Scale: LLM Rationales for YouTube Music Artist Discovery 搜广推与 LLM 应用 Google 2026-09-20 用户愿意听熟悉的艺人，却可能不敢点开陌生艺人。论文将计算昂贵的 Gemini 推理移到异步离线阶段：根据完整的听歌历史生成“发现画像”，包含未听过的艺人和个性化理由；通过实体标准化与 LLM 评审过滤不可信理由；在线阶段只取缓存的画像，缺失时退回原有推荐。这样既能给候选附上解释，又避免在用户请求链路上运行大模型。论文的多臂 holdback 把新增提名与理由标注分开，发现理由是主导 shelf engagement 提升的因素。 复现级别：公开数据概念验证。复现级别：公开数据概念验证。本地使用真实 Qwen2.5-7B-Instruct 生成新艺人提名与自然语言理由，执行目录映射、已听过过滤、理由证据检查及只读缓存在线回退。Google 的 Gemini、私有音乐知识图谱、LLM-as-a-Judge 和线上多臂 A/B 不可公开复刻；公开 Last.fm 命中率不是用户信任或线上互动效果。本地确实运行 7B 权重推理、目录/新颖性/共享标签约束以及缓存/回退路径；但既未调用 Gemini，也未复刻 Google 的专有 KG 和线上 judge。本地对照口径：原 CF 基线 test Hit@5 0.40；  music-discovery llm-rationale offline-online-decoupling 搜广推 语义表征、用户知识与冷启动 Music Rationales 为什么把陌生艺人推荐理由离线生成，并把“提名”和“展示理由”分开评估？ 离线生成让模型能利用完整历史做昂贵推理，再经实体规范化和理由过滤，在线只读取缓存，避免请求延迟。提名改变推荐谁，理由改变用户是否愿意点同一候选，两条路径可能独立影响互动。分开设置实验臂才能区分增益来自候选变化还是解释作用；理由可信也不能只靠语言流畅判断。 示意：同一位陌生爵士艺人，一组只展示名字，另一组增加“延续你常听的钢琴三重奏风格”。保持候选相同，才更接近检验理由本身是否帮助用户决定。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c2c4588e9452cf62">Music Rationales 为什么把陌生艺人推荐理由离线生成，并把“提名”和“展示理由”分开评估？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amusic-rationales">Explainable Recommendations at Scale: LLM Rationales for YouTube Music Artist Discovery</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>离线生成让模型能利用完整历史做昂贵推理，再经实体规范化和理由过滤，在线只读取缓存，避免请求延迟。提名改变推荐谁，理由改变用户是否愿意点同一候选，两条路径可能独立影响互动。分开设置实验臂才能区分增益来自候选变化还是解释作用；理由可信也不能只靠语言流畅判断。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一位陌生爵士艺人，一组只展示名字，另一组增加“延续你常听的钢琴三重奏风格”。保持候选相同，才更接近检验理由本身是否帮助用户决定。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与机制；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.23877">原论文</a> · <a href="../../../../reproductions/2609.23877-music-rationales/">实现解读</a> · <a href="#qa-c2c4588e9452cf62">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:music-rationales" data-paper-title="Explainable Recommendations at Scale: LLM Rationales for YouTube Music Artist Discovery" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Explainable Recommendations at Scale: LLM Rationales for YouTube Music Artist Discovery 搜广推与 LLM 应用 Google 2026-09-20 用户愿意听熟悉的艺人，却可能不敢点开陌生艺人。论文将计算昂贵的 Gemini 推理移到异步离线阶段：根据完整的听歌历史生成“发现画像”，包含未听过的艺人和个性化理由；通过实体标准化与 LLM 评审过滤不可信理由；在线阶段只取缓存的画像，缺失时退回原有推荐。这样既能给候选附上解释，又避免在用户请求链路上运行大模型。论文的多臂 holdback 把新增提名与理由标注分开，发现理由是主导 shelf engagement 提升的因素。 复现级别：公开数据概念验证。复现级别：公开数据概念验证。本地使用真实 Qwen2.5-7B-Instruct 生成新艺人提名与自然语言理由，执行目录映射、已听过过滤、理由证据检查及只读缓存在线回退。Google 的 Gemini、私有音乐知识图谱、LLM-as-a-Judge 和线上多臂 A/B 不可公开复刻；公开 Last.fm 命中率不是用户信任或线上互动效果。本地确实运行 7B 权重推理、目录/新颖性/共享标签约束以及缓存/回退路径；但既未调用 Gemini，也未复刻 Google 的专有 KG 和线上 judge。本地对照口径：原 CF 基线 test Hit@5 0.40；  music-discovery llm-rationale offline-online-decoupling 搜广推 语义表征、用户知识与冷启动 保持 CF 顺序只附解释，与把 LLM 提名放前面，两臂能回答什么不同问题？ 提名臂改变候选覆盖与位置，可影响离线命中；只附解释不改变列表，其 Hit 必然与原列表相同，离线只能看解释覆盖。理由对真实互动的作用需实际用户实验，不能由消费标签推断。两臂隔离可避免把候选变化误归解释。 示意：同五位艺人加理由后离线正确数不变，却可能让用户更愿意点击；这种行为改变需要曝光实验，不会自动出现在静态 Hit@5。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-3a76079ab40e8461">保持 CF 顺序只附解释，与把 LLM 提名放前面，两臂能回答什么不同问题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amusic-rationales">Explainable Recommendations at Scale: LLM Rationales for YouTube Music Artist Discovery</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>提名臂改变候选覆盖与位置，可影响离线命中；只附解释不改变列表，其 Hit 必然与原列表相同，离线只能看解释覆盖。理由对真实互动的作用需实际用户实验，不能由消费标签推断。两臂隔离可避免把候选变化误归解释。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同五位艺人加理由后离线正确数不变，却可能让用户更愿意点击；这种行为改变需要曝光实验，不会自动出现在静态 Hit@5。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与机制；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.23877">原论文</a> · <a href="../../../../reproductions/2609.23877-music-rationales/">实现解读</a> · <a href="#qa-3a76079ab40e8461">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:music-rationales" data-paper-title="Explainable Recommendations at Scale: LLM Rationales for YouTube Music Artist Discovery" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Explainable Recommendations at Scale: LLM Rationales for YouTube Music Artist Discovery 搜广推与 LLM 应用 Google 2026-09-20 用户愿意听熟悉的艺人，却可能不敢点开陌生艺人。论文将计算昂贵的 Gemini 推理移到异步离线阶段：根据完整的听歌历史生成“发现画像”，包含未听过的艺人和个性化理由；通过实体标准化与 LLM 评审过滤不可信理由；在线阶段只取缓存的画像，缺失时退回原有推荐。这样既能给候选附上解释，又避免在用户请求链路上运行大模型。论文的多臂 holdback 把新增提名与理由标注分开，发现理由是主导 shelf engagement 提升的因素。 复现级别：公开数据概念验证。复现级别：公开数据概念验证。本地使用真实 Qwen2.5-7B-Instruct 生成新艺人提名与自然语言理由，执行目录映射、已听过过滤、理由证据检查及只读缓存在线回退。Google 的 Gemini、私有音乐知识图谱、LLM-as-a-Judge 和线上多臂 A/B 不可公开复刻；公开 Last.fm 命中率不是用户信任或线上互动效果。本地确实运行 7B 权重推理、目录/新颖性/共享标签约束以及缓存/回退路径；但既未调用 Gemini，也未复刻 Google 的专有 KG 和线上 judge。本地对照口径：原 CF 基线 test Hit@5 0.40；  music-discovery llm-rationale offline-online-decoupling 搜广推 语义表征、用户知识与冷启动 Music Rationales 的目录过滤和缓存回退，为什么要保留拒绝与缺失状态？ 生成的艺人需标准化到真实目录，理由不可信则拒绝，缓存缺失走原推荐，不应强行填一段故事。提名结果与回退后的最终列表分开评估；来源单 seed 概念诊断没有解释 CTR，不能把有效理由率当用户受益。 示意：生成不存在的艺人时直接回 CF 比勉强匹配同名错误对象可靠；回退保障可服务，却不说明 LLM 提名本身成功。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f97298e1fc83f412">Music Rationales 的目录过滤和缓存回退，为什么要保留拒绝与缺失状态？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amusic-rationales">Explainable Recommendations at Scale: LLM Rationales for YouTube Music Artist Discovery</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>生成的艺人需标准化到真实目录，理由不可信则拒绝，缓存缺失走原推荐，不应强行填一段故事。提名结果与回退后的最终列表分开评估；来源单 seed 概念诊断没有解释 CTR，不能把有效理由率当用户受益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>生成不存在的艺人时直接回 CF 比勉强匹配同名错误对象可靠；回退保障可服务，却不说明 LLM 提名本身成功。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与机制；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.23877">原论文</a> · <a href="../../../../reproductions/2609.23877-music-rationales/">实现解读</a> · <a href="#qa-f97298e1fc83f412">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sirf" data-paper-title="SIRF: A Spec-Internalized Risk Foundation Model for Industrial Content Risk Control" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SIRF: A Spec-Internalized Risk Foundation Model for Industrial Content Risk Control 搜广推与 LLM 应用 Xiaohongshu 2026-09-10 SIRF 用 EntiGraph、MAGA 改写和账户级 CoT 合成长尾风控规则数据，通过 CPT 把复杂 trigger/exemption 规则写进模型权重，以单次 verdict 和可调阈值满足秒级线上判定。 复现级别：概念诊断。复现级别：概念诊断。执行规则关系合成、trigger/exemption 内化和 P95 阈值选择；线性模型替代 8B LLM CPT。没有私有账户数据、8B CPT、EntiGraph/MAGA 语言生成和线上 serving，因此本地结果不能验证论文业务提升。本地对照口径：同源线性特征为基线，加入规则交互项的实验组在三 seed 上 Black Recall@P95 相对提高 65.81%（绝对约 33.84 个百分点）；这不是论文 8B 模型或线上流量结果。  content-understanding risk-control foundation-model industrial-deployment 搜广推 语义表征、用户知识与冷启动 SIRF为什么把trigger和exemption都写进训练规则？ 风控不仅要识别触发条件，还需处理合法豁免，长尾组合单凭常见标签容易误伤。合成规则与CPT希望内化复杂决策，阈值再控制高精度要求。 例如出现某关键词不必违规，还要检查是否处于规则允许的说明场景。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-sirf-2c896048" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4bba0f8aa5a2e65c">SIRF为什么把trigger和exemption都写进训练规则？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asirf">SIRF: A Spec-Internalized Risk Foundation Model for Industrial Content Risk Control</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>风控不仅要识别触发条件，还需处理合法豁免，长尾组合单凭常见标签容易误伤。合成规则与CPT希望内化复杂决策，阈值再控制高精度要求。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如出现某关键词不必违规，还要检查是否处于规则允许的说明场景。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11752">原论文</a> · <a href="../../../../reproductions/2609.11752-sirf/">实现解读</a> · <a href="#qa-4bba0f8aa5a2e65c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sirf" data-paper-title="SIRF: A Spec-Internalized Risk Foundation Model for Industrial Content Risk Control" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SIRF: A Spec-Internalized Risk Foundation Model for Industrial Content Risk Control 搜广推与 LLM 应用 Xiaohongshu 2026-09-10 SIRF 用 EntiGraph、MAGA 改写和账户级 CoT 合成长尾风控规则数据，通过 CPT 把复杂 trigger/exemption 规则写进模型权重，以单次 verdict 和可调阈值满足秒级线上判定。 复现级别：概念诊断。复现级别：概念诊断。执行规则关系合成、trigger/exemption 内化和 P95 阈值选择；线性模型替代 8B LLM CPT。没有私有账户数据、8B CPT、EntiGraph/MAGA 语言生成和线上 serving，因此本地结果不能验证论文业务提升。本地对照口径：同源线性特征为基线，加入规则交互项的实验组在三 seed 上 Black Recall@P95 相对提高 65.81%（绝对约 33.84 个百分点）；这不是论文 8B 模型或线上流量结果。  content-understanding risk-control foundation-model industrial-deployment 搜广推 语义表征、用户知识与冷启动 SIRF 为什么用包含 trigger 与 exemption 的合成规则训练模型，再以阈值控制判定？ 长尾风控规则不仅要识别触发条件，还要处理豁免及其组合，单靠常见日志容易漏学。规则图、改写和账户级推理提供覆盖训练，通过继续预训练把复杂模式写入模型，再用单次 verdict 降低在线开销。阈值调节精确率与召回的取舍；本地规则交互诊断不能当作原文大模型的生产能力复现。 示意：频繁交易可能触发风险，但经过验证的商户活动又构成豁免。训练样本需同时覆盖两者及交互，否则模型可能只记住“频繁就是风险”，提高误报。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-02322f33c7044fe8">SIRF 为什么用包含 trigger 与 exemption 的合成规则训练模型，再以阈值控制判定？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asirf">SIRF: A Spec-Internalized Risk Foundation Model for Industrial Content Risk Control</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长尾风控规则不仅要识别触发条件，还要处理豁免及其组合，单靠常见日志容易漏学。规则图、改写和账户级推理提供覆盖训练，通过继续预训练把复杂模式写入模型，再用单次 verdict 降低在线开销。阈值调节精确率与召回的取舍；本地规则交互诊断不能当作原文大模型的生产能力复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>频繁交易可能触发风险，但经过验证的商户活动又构成豁免。训练样本需同时覆盖两者及交互，否则模型可能只记住“频繁就是风险”，提高误报。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11752">原论文</a> · <a href="../../../../reproductions/2609.11752-sirf/">实现解读</a> · <a href="#qa-02322f33c7044fe8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sirf" data-paper-title="SIRF: A Spec-Internalized Risk Foundation Model for Industrial Content Risk Control" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SIRF: A Spec-Internalized Risk Foundation Model for Industrial Content Risk Control 搜广推与 LLM 应用 Xiaohongshu 2026-09-10 SIRF 用 EntiGraph、MAGA 改写和账户级 CoT 合成长尾风控规则数据，通过 CPT 把复杂 trigger/exemption 规则写进模型权重，以单次 verdict 和可调阈值满足秒级线上判定。 复现级别：概念诊断。复现级别：概念诊断。执行规则关系合成、trigger/exemption 内化和 P95 阈值选择；线性模型替代 8B LLM CPT。没有私有账户数据、8B CPT、EntiGraph/MAGA 语言生成和线上 serving，因此本地结果不能验证论文业务提升。本地对照口径：同源线性特征为基线，加入规则交互项的实验组在三 seed 上 Black Recall@P95 相对提高 65.81%（绝对约 33.84 个百分点）；这不是论文 8B 模型或线上流量结果。  content-understanding risk-control foundation-model industrial-deployment 搜广推 语义表征、用户知识与冷启动 规则内化与运行时纯规则引擎有什么差别？ 参数模型可泛化表达和上下文，却不保证严格逐条逻辑满足；规则引擎显式执行条件但覆盖受编写范围限制。不能把神经判定高分当所有规则的形式证明。 例如规则改版后模型权重未更新，可能仍按旧习惯判定。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f64f6bf87f503425">规则内化与运行时纯规则引擎有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asirf">SIRF: A Spec-Internalized Risk Foundation Model for Industrial Content Risk Control</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>参数模型可泛化表达和上下文，却不保证严格逐条逻辑满足；规则引擎显式执行条件但覆盖受编写范围限制。不能把神经判定高分当所有规则的形式证明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如规则改版后模型权重未更新，可能仍按旧习惯判定。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11752">原论文</a> · <a href="../../../../reproductions/2609.11752-sirf/">实现解读</a> · <a href="#qa-f64f6bf87f503425">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sirf" data-paper-title="SIRF: A Spec-Internalized Risk Foundation Model for Industrial Content Risk Control" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SIRF: A Spec-Internalized Risk Foundation Model for Industrial Content Risk Control 搜广推与 LLM 应用 Xiaohongshu 2026-09-10 SIRF 用 EntiGraph、MAGA 改写和账户级 CoT 合成长尾风控规则数据，通过 CPT 把复杂 trigger/exemption 规则写进模型权重，以单次 verdict 和可调阈值满足秒级线上判定。 复现级别：概念诊断。复现级别：概念诊断。执行规则关系合成、trigger/exemption 内化和 P95 阈值选择；线性模型替代 8B LLM CPT。没有私有账户数据、8B CPT、EntiGraph/MAGA 语言生成和线上 serving，因此本地结果不能验证论文业务提升。本地对照口径：同源线性特征为基线，加入规则交互项的实验组在三 seed 上 Black Recall@P95 相对提高 65.81%（绝对约 33.84 个百分点）；这不是论文 8B 模型或线上流量结果。  content-understanding risk-control foundation-model industrial-deployment 搜广推 语义表征、用户知识与冷启动 SIRF本地高精度阈值结果对应完整8B CPT吗？ 不对应，当前触发豁免特征代理，未执行私有账户数据、EntiGraph/MAGA生成和大模型训练。阈值应在允许验证集选，held-out报告不能再被用来挑最优点。 例如小规则分类器达到目标精度，不等于原内容风控基础模型已复现。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-5f6775ad35692318">SIRF本地高精度阈值结果对应完整8B CPT吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asirf">SIRF: A Spec-Internalized Risk Foundation Model for Industrial Content Risk Control</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不对应，当前触发豁免特征代理，未执行私有账户数据、EntiGraph/MAGA生成和大模型训练。阈值应在允许验证集选，held-out报告不能再被用来挑最优点。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如小规则分类器达到目标精度，不等于原内容风控基础模型已复现。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11752">原论文</a> · <a href="../../../../reproductions/2609.11752-sirf/">实现解读</a> · <a href="#qa-5f6775ad35692318">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:camie" data-paper-title="CAMIE: Co-Engagement-Aware Multimodal Item Embeddings for Snap Dynamic Product Ads Retrieval" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="CAMIE: Co-Engagement-Aware Multimodal Item Embeddings for Snap Dynamic Product Ads Retrieval 搜广推与 LLM 应用 Snap Inc. 2026-08-31 CAMIE 用同一个 LLM/MLLM 接口编码图片和商品元数据，再从用户旅程挖掘共同互动商品对，以对称 in-batch InfoNCE 把“内容相近”校正为“行为上会共同转化”。同一 checkpoint 同时支持多模态和纯文本召回。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现内容向量、共同互动正对和对称检索打分。未包含私有 DPA 用户旅程、生产 MLLM checkpoint 与 ANN 服务；仅声明 CPU 核心机制。公开 MovieLens 的内容特征和共现 transition 代理共同互动，NDCG@10 为 0.05121（基线 0.05401）；负结果保留在 metrics/public-seeds42-44.json，不把小数据退化包装成提升。  multimodal-retrieval co-engagement advertising 搜广推 语义表征、用户知识与冷启动 CAMIE 为什么要求同一 checkpoint 能处理图文与纯文本商品？ 实际商品模态可用性不同，统一接口让缺图片的商品也进入同一检索空间，减少为各模态维护割裂模型。内容输入经共同训练与行为对齐后可互相匹配，但缺失模态仍会减少信息，统一 checkpoint 不代表两种输入拥有完全相同精度。 示意：一件新品只有标题，另一件有图和详细属性，两者都要进入商品向量索引；统一接口允许检索，但不能凭空补出新品没有提供的视觉细节。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-camie-634faffd" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5287e4bcfb9cffed">CAMIE 为什么要求同一 checkpoint 能处理图文与纯文本商品？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acamie">CAMIE: Co-Engagement-Aware Multimodal Item Embeddings for Snap Dynamic Product Ads Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Snap Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>实际商品模态可用性不同，统一接口让缺图片的商品也进入同一检索空间，减少为各模态维护割裂模型。内容输入经共同训练与行为对齐后可互相匹配，但缺失模态仍会减少信息，统一 checkpoint 不代表两种输入拥有完全相同精度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一件新品只有标题，另一件有图和详细属性，两者都要进入商品向量索引；统一接口允许检索，但不能凭空补出新品没有提供的视觉细节。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.30255">原论文</a> · <a href="../../../../reproductions/2608.30255-camie/">实现解读</a> · <a href="#qa-5287e4bcfb9cffed">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:camie" data-paper-title="CAMIE: Co-Engagement-Aware Multimodal Item Embeddings for Snap Dynamic Product Ads Retrieval" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="CAMIE: Co-Engagement-Aware Multimodal Item Embeddings for Snap Dynamic Product Ads Retrieval 搜广推与 LLM 应用 Snap Inc. 2026-08-31 CAMIE 用同一个 LLM/MLLM 接口编码图片和商品元数据，再从用户旅程挖掘共同互动商品对，以对称 in-batch InfoNCE 把“内容相近”校正为“行为上会共同转化”。同一 checkpoint 同时支持多模态和纯文本召回。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现内容向量、共同互动正对和对称检索打分。未包含私有 DPA 用户旅程、生产 MLLM checkpoint 与 ANN 服务；仅声明 CPU 核心机制。公开 MovieLens 的内容特征和共现 transition 代理共同互动，NDCG@10 为 0.05121（基线 0.05401）；负结果保留在 metrics/public-seeds42-44.json，不把小数据退化包装成提升。  multimodal-retrieval co-engagement advertising 搜广推 语义表征、用户知识与冷启动 CAMIE为什么不用纯图文相似度训练商品向量，还要加入co-engagement对比学习？ 图文相似度只表达内容接近，不保证商品在人类消费过程中有关联。CAMIE用用户旅程中共同互动的商品对形成对称对比监督，把多模态表示拉向推荐相关关系；共享编码接口还能支持不同模态可用性。共同互动本身仍受曝光和场景影响，不能把它等同于普遍互补或因果需求。 示意：图片里很像的两件家具可能尺寸用途不合，而外观不同的桌子和椅子经常一起被考虑；行为对比为内容编码补上这种推荐语义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-1b92b9cd74adef7f">CAMIE为什么不用纯图文相似度训练商品向量，还要加入co-engagement对比学习？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acamie">CAMIE: Co-Engagement-Aware Multimodal Item Embeddings for Snap Dynamic Product Ads Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Snap Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>图文相似度只表达内容接近，不保证商品在人类消费过程中有关联。CAMIE用用户旅程中共同互动的商品对形成对称对比监督，把多模态表示拉向推荐相关关系；共享编码接口还能支持不同模态可用性。共同互动本身仍受曝光和场景影响，不能把它等同于普遍互补或因果需求。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>图片里很像的两件家具可能尺寸用途不合，而外观不同的桌子和椅子经常一起被考虑；行为对比为内容编码补上这种推荐语义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.30255">原论文</a> · <a href="../../../../reproductions/2608.30255-camie/">实现解读</a> · <a href="#qa-1b92b9cd74adef7f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:camie" data-paper-title="CAMIE: Co-Engagement-Aware Multimodal Item Embeddings for Snap Dynamic Product Ads Retrieval" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="CAMIE: Co-Engagement-Aware Multimodal Item Embeddings for Snap Dynamic Product Ads Retrieval 搜广推与 LLM 应用 Snap Inc. 2026-08-31 CAMIE 用同一个 LLM/MLLM 接口编码图片和商品元数据，再从用户旅程挖掘共同互动商品对，以对称 in-batch InfoNCE 把“内容相近”校正为“行为上会共同转化”。同一 checkpoint 同时支持多模态和纯文本召回。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现内容向量、共同互动正对和对称检索打分。未包含私有 DPA 用户旅程、生产 MLLM checkpoint 与 ANN 服务；仅声明 CPU 核心机制。公开 MovieLens 的内容特征和共现 transition 代理共同互动，NDCG@10 为 0.05121（基线 0.05401）；负结果保留在 metrics/public-seeds42-44.json，不把小数据退化包装成提升。  multimodal-retrieval co-engagement advertising 搜广推 语义表征、用户知识与冷启动 CAMIE 的 co-engagement 对齐与通用图文对比，正例语义有何不同？ 图文对比通常连接同一内容的图和文字，co-engagement 连接旅程中共同互动的不同商品，把用户行为关系写入空间。前者关注内容一致，后者可能反映搭配或连续需求；共同互动仍含曝光因素，不是天然无偏的互补标签。 示意：帐篷和睡袋画面不同，却在同次露营采购里共同转化。行为对齐可拉近它们，但两个共同出现的热门商品也可能只是曝光多。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-76fca7b0a2ff4204">CAMIE 的 co-engagement 对齐与通用图文对比，正例语义有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acamie">CAMIE: Co-Engagement-Aware Multimodal Item Embeddings for Snap Dynamic Product Ads Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Snap Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>图文对比通常连接同一内容的图和文字，co-engagement 连接旅程中共同互动的不同商品，把用户行为关系写入空间。前者关注内容一致，后者可能反映搭配或连续需求；共同互动仍含曝光因素，不是天然无偏的互补标签。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>帐篷和睡袋画面不同，却在同次露营采购里共同转化。行为对齐可拉近它们，但两个共同出现的热门商品也可能只是曝光多。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.30255">原论文</a> · <a href="../../../../reproductions/2608.30255-camie/">实现解读</a> · <a href="#qa-76fca7b0a2ff4204">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:camie" data-paper-title="CAMIE: Co-Engagement-Aware Multimodal Item Embeddings for Snap Dynamic Product Ads Retrieval" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="CAMIE: Co-Engagement-Aware Multimodal Item Embeddings for Snap Dynamic Product Ads Retrieval 搜广推与 LLM 应用 Snap Inc. 2026-08-31 CAMIE 用同一个 LLM/MLLM 接口编码图片和商品元数据，再从用户旅程挖掘共同互动商品对，以对称 in-batch InfoNCE 把“内容相近”校正为“行为上会共同转化”。同一 checkpoint 同时支持多模态和纯文本召回。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现内容向量、共同互动正对和对称检索打分。未包含私有 DPA 用户旅程、生产 MLLM checkpoint 与 ANN 服务；仅声明 CPU 核心机制。公开 MovieLens 的内容特征和共现 transition 代理共同互动，NDCG@10 为 0.05121（基线 0.05401）；负结果保留在 metrics/public-seeds42-44.json，不把小数据退化包装成提升。  multimodal-retrieval co-engagement advertising 搜广推 语义表征、用户知识与冷启动 CAMIE 对称 in-batch InfoNCE 为什么要计算两个方向？ 一个方向以 a 为查询、b 为正目标，与批中其他 b 比较；反向交换两者，使两侧编码都接受匹配监督，再取平均。批中配对必须对应同一旅程关系，温度控制分布锐度，不能把重复正例未经处理地当负例解释。 示意：批中相机—镜头与帐篷—睡袋是两对，既用相机找镜头，也用镜头找相机；若把同一镜头重复行当作独立负例，会产生矛盾监督。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-74acf9ceaf1f9727">CAMIE 对称 in-batch InfoNCE 为什么要计算两个方向？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acamie">CAMIE: Co-Engagement-Aware Multimodal Item Embeddings for Snap Dynamic Product Ads Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Snap Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一个方向以 a 为查询、b 为正目标，与批中其他 b 比较；反向交换两者，使两侧编码都接受匹配监督，再取平均。批中配对必须对应同一旅程关系，温度控制分布锐度，不能把重复正例未经处理地当负例解释。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>批中相机—镜头与帐篷—睡袋是两对，既用相机找镜头，也用镜头找相机；若把同一镜头重复行当作独立负例，会产生矛盾监督。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.30255">原论文</a> · <a href="../../../../reproductions/2608.30255-camie/">实现解读</a> · <a href="#qa-74acf9ceaf1f9727">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dynamic-codebook" data-paper-title="From a Static Multi-Level Small Semantic Codebook to a Dynamic Single-Level Large Semantic Codebook for Generative Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="From a Static Multi-Level Small Semantic Codebook to a Dynamic Single-Level Large Semantic Codebook for Generative Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-08-21 把多级小语义码本压缩为动态更新的单级大码本，再保留独立碰撞码；既减少自回归步数，也用曝光加权更新抵抗码本漂移。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation semantic-id serving-efficiency 搜广推 语义表征、用户知识与冷启动 单级大码本为什么可缩短生成，却仍不等同于唯一 item ID？ 减少层数使语义路径更短，但有限中心仍可能分到多个物品，需要独立碰撞码完成唯一映射。大词表增加候选与更新压力，不能只数自回归步数就判断所有成本下降。单级结构仍要维持语义与可服务身份的联系。 示意：一本书一次选到大码后，可能与另一书同桶，仍需碰撞码区分；只输出桶编号并不能确定最后展示哪一本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-dynamic-codebook-fbc8657c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-bc885da512bc2b5b">单级大码本为什么可缩短生成，却仍不等同于唯一 item ID？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adynamic-codebook">From a Static Multi-Level Small Semantic Codebook to a Dynamic Single-Level Large Semantic Codebook for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>减少层数使语义路径更短，但有限中心仍可能分到多个物品，需要独立碰撞码完成唯一映射。大词表增加候选与更新压力，不能只数自回归步数就判断所有成本下降。单级结构仍要维持语义与可服务身份的联系。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一本书一次选到大码后，可能与另一书同桶，仍需碰撞码区分；只输出桶编号并不能确定最后展示哪一本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.21012">原论文</a> · <a href="../../../../reproductions/2608.21012-dynamic-codebook/">实现解读</a> · <a href="#qa-bc885da512bc2b5b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dynamic-codebook" data-paper-title="From a Static Multi-Level Small Semantic Codebook to a Dynamic Single-Level Large Semantic Codebook for Generative Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="From a Static Multi-Level Small Semantic Codebook to a Dynamic Single-Level Large Semantic Codebook for Generative Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-08-21 把多级小语义码本压缩为动态更新的单级大码本，再保留独立碰撞码；既减少自回归步数，也用曝光加权更新抵抗码本漂移。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation semantic-id serving-efficiency 搜广推 语义表征、用户知识与冷启动 单级大码本缩短了解码，为什么还需要独立碰撞码与曝光加权更新？ 少生成几个语义层能降低自回归开销，但多个物品仍可能落入同一码，必须保留额外区分入口。动态更新让码中心跟随实际使用分布，曝光权重影响哪些区域更精细地被表示；与此同时更新会改变索引语义，需要维持生成器与服务映射的一致性，不能只比较token数量。 示意：单枚主码已定位一组热门商品，额外碰撞码负责区分组内物品；如果码中心更新后服务仍读旧映射，即使解码快了，也可能返回错误商品。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-378a7edc8250a731">单级大码本缩短了解码，为什么还需要独立碰撞码与曝光加权更新？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adynamic-codebook">From a Static Multi-Level Small Semantic Codebook to a Dynamic Single-Level Large Semantic Codebook for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>少生成几个语义层能降低自回归开销，但多个物品仍可能落入同一码，必须保留额外区分入口。动态更新让码中心跟随实际使用分布，曝光权重影响哪些区域更精细地被表示；与此同时更新会改变索引语义，需要维持生成器与服务映射的一致性，不能只比较token数量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>单枚主码已定位一组热门商品，额外碰撞码负责区分组内物品；如果码中心更新后服务仍读旧映射，即使解码快了，也可能返回错误商品。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.21012">原论文</a> · <a href="../../../../reproductions/2608.21012-dynamic-codebook/">实现解读</a> · <a href="#qa-378a7edc8250a731">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dynamic-codebook" data-paper-title="From a Static Multi-Level Small Semantic Codebook to a Dynamic Single-Level Large Semantic Codebook for Generative Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="From a Static Multi-Level Small Semantic Codebook to a Dynamic Single-Level Large Semantic Codebook for Generative Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-08-21 把多级小语义码本压缩为动态更新的单级大码本，再保留独立碰撞码；既减少自回归步数，也用曝光加权更新抵抗码本漂移。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation semantic-id serving-efficiency 搜广推 语义表征、用户知识与冷启动 动态码本与冻结码本，对分布变化和路径稳定性怎样取舍？ 冻结保留旧路径含义，动态更新可跟随新曝光与内容，但中心移动可能让旧生成器与索引错位。曝光加权也可能强化旧策略偏差，并不天然去偏。机制比较需同时检查更新收益、漂移与版本维护，不能把变化更快直接称为更准确。 示意：节日新品增多时中心可调整，但旧商品若悄悄换码，模型仍按旧概率生成就会错位；需要同步映射而非只更新均值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-335cd5a8867b9d57">动态码本与冻结码本，对分布变化和路径稳定性怎样取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adynamic-codebook">From a Static Multi-Level Small Semantic Codebook to a Dynamic Single-Level Large Semantic Codebook for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冻结保留旧路径含义，动态更新可跟随新曝光与内容，但中心移动可能让旧生成器与索引错位。曝光加权也可能强化旧策略偏差，并不天然去偏。机制比较需同时检查更新收益、漂移与版本维护，不能把变化更快直接称为更准确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>节日新品增多时中心可调整，但旧商品若悄悄换码，模型仍按旧概率生成就会错位；需要同步映射而非只更新均值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.21012">原论文</a> · <a href="../../../../reproductions/2608.21012-dynamic-codebook/">实现解读</a> · <a href="#qa-335cd5a8867b9d57">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dynamic-codebook" data-paper-title="From a Static Multi-Level Small Semantic Codebook to a Dynamic Single-Level Large Semantic Codebook for Generative Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="From a Static Multi-Level Small Semantic Codebook to a Dynamic Single-Level Large Semantic Codebook for Generative Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-08-21 把多级小语义码本压缩为动态更新的单级大码本，再保留独立碰撞码；既减少自回归步数，也用曝光加权更新抵抗码本漂移。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation semantic-id serving-efficiency 搜广推 语义表征、用户知识与冷启动 动态码本加权更新遇到空桶，为什么必须有明确规则？ 新中心分母是桶内权重和，空桶没有可估计均值，应按约定保留或受控处理，不能除零后随机补数。EMA、物品分配和碰撞映射需同版本发布，才避免无依据漂移。数值兜底若改变算法，应作为不同实现而非静默等价。 示意：本批没有商品进入码七，就没有数据支持其新位置；把中心随手重置会改变旧码七含义，已有生成路径也跟着失效。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-84a3e3fd94a94437">动态码本加权更新遇到空桶，为什么必须有明确规则？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adynamic-codebook">From a Static Multi-Level Small Semantic Codebook to a Dynamic Single-Level Large Semantic Codebook for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>新中心分母是桶内权重和，空桶没有可估计均值，应按约定保留或受控处理，不能除零后随机补数。EMA、物品分配和碰撞映射需同版本发布，才避免无依据漂移。数值兜底若改变算法，应作为不同实现而非静默等价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>本批没有商品进入码七，就没有数据支持其新位置；把中心随手重置会改变旧码七含义，已有生成路径也跟着失效。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.21012">原论文</a> · <a href="../../../../reproductions/2608.21012-dynamic-codebook/">实现解读</a> · <a href="#qa-84a3e3fd94a94437">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:netflix-mediafm" data-paper-title="Multimedia Asset Personalization via Multimodal Embeddings at Netflix" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Multimedia Asset Personalization via Multimodal Embeddings at Netflix 搜广推与 LLM 应用 Netflix 2026-08-18 把冻结的 CLIP/MediaFM 多模态表示作为共享在线特征接入资产双塔，并以查询相似度增强搜索画布；离线 IPS 与 winner proxy 先筛选 checkpoint。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  multimodal-recommendation content-understanding cold-start 搜广推 语义表征、用户知识与冷启动 MediaFM 为什么作为共享媒体特征，而不直接输出最终推荐概率？ 多模态表示提供内容理解，用户、查询与任务目标再由下游双塔适配，不同资产任务可复用同一媒体编码。冻结接口降低重复计算，但缺失细节不会因下游训练自动出现。共享特征与最终业务价值需分别验证。 示意：同一海报向量可用于首页选图和搜索画布，任务头结合不同用户意图；向量相似高不等于该海报在每个场景都最好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-netflix-mediafm-31c991d9" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e014134d24b2b7e0">MediaFM 为什么作为共享媒体特征，而不直接输出最终推荐概率？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Anetflix-mediafm">Multimedia Asset Personalization via Multimodal Embeddings at Netflix</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Netflix</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多模态表示提供内容理解，用户、查询与任务目标再由下游双塔适配，不同资产任务可复用同一媒体编码。冻结接口降低重复计算，但缺失细节不会因下游训练自动出现。共享特征与最终业务价值需分别验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一海报向量可用于首页选图和搜索画布，任务头结合不同用户意图；向量相似高不等于该海报在每个场景都最好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.18322">原论文</a> · <a href="../../../../reproductions/2608.18322-netflix-mediafm/">实现解读</a> · <a href="#qa-e014134d24b2b7e0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:netflix-mediafm" data-paper-title="Multimedia Asset Personalization via Multimodal Embeddings at Netflix" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Multimedia Asset Personalization via Multimodal Embeddings at Netflix 搜广推与 LLM 应用 Netflix 2026-08-18 把冻结的 CLIP/MediaFM 多模态表示作为共享在线特征接入资产双塔，并以查询相似度增强搜索画布；离线 IPS 与 winner proxy 先筛选 checkpoint。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  multimodal-recommendation content-understanding cold-start 搜广推 语义表征、用户知识与冷启动 Netflix MediaFM 为什么冻结多模态表示并让多个资产任务共享，而不是每个任务各训一个视觉模型？ 冻结的共享表示把媒体理解成本集中到可复用特征层，下游双塔再学习用户、查询与资产之间的适配。查询相似度可补充个性化相似度，使搜索场景兼顾当前意图。共享减少重复编码与特征分裂，但冻结表示不能靠下游训练自动补回缺失的视觉细节，离线代理筛选也不能替代线上验证。 示意：同一张海报的多模态向量可供首页选图和搜索画布共同使用。搜索“海边喜剧”时增加查询匹配权重，首页则更多结合用户长期口味，无须重算媒体编码。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8a14f7828b81c132">Netflix MediaFM 为什么冻结多模态表示并让多个资产任务共享，而不是每个任务各训一个视觉模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Anetflix-mediafm">Multimedia Asset Personalization via Multimodal Embeddings at Netflix</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Netflix</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冻结的共享表示把媒体理解成本集中到可复用特征层，下游双塔再学习用户、查询与资产之间的适配。查询相似度可补充个性化相似度，使搜索场景兼顾当前意图。共享减少重复编码与特征分裂，但冻结表示不能靠下游训练自动补回缺失的视觉细节，离线代理筛选也不能替代线上验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一张海报的多模态向量可供首页选图和搜索画布共同使用。搜索“海边喜剧”时增加查询匹配权重，首页则更多结合用户长期口味，无须重算媒体编码。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.18322">原论文</a> · <a href="../../../../reproductions/2608.18322-netflix-mediafm/">实现解读</a> · <a href="#qa-8a14f7828b81c132">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:netflix-mediafm" data-paper-title="Multimedia Asset Personalization via Multimodal Embeddings at Netflix" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Multimedia Asset Personalization via Multimodal Embeddings at Netflix 搜广推与 LLM 应用 Netflix 2026-08-18 把冻结的 CLIP/MediaFM 多模态表示作为共享在线特征接入资产双塔，并以查询相似度增强搜索画布；离线 IPS 与 winner proxy 先筛选 checkpoint。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  multimodal-recommendation content-understanding cold-start 搜广推 语义表征、用户知识与冷启动 查询相似度增强与纯用户个性化匹配，相比当前搜索意图如何进入？ 用户相似度表达长期口味，查询相似度补充当前明确需求，通过权重取舍。只个性化可能忽略搜索词，只查询又丢个人差异。机制对比不是普遍权重结论，离线 IPS 与 winner proxy 筛选也不能替代真实线上效果。 示意：爱动作片用户搜索温馨喜剧时，应让查询覆盖部分长期偏好；若仍全按动作兴趣排，搜索画布可能相关性不足。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-065b8f3cc5f30c5a">查询相似度增强与纯用户个性化匹配，相比当前搜索意图如何进入？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Anetflix-mediafm">Multimedia Asset Personalization via Multimodal Embeddings at Netflix</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Netflix</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用户相似度表达长期口味，查询相似度补充当前明确需求，通过权重取舍。只个性化可能忽略搜索词，只查询又丢个人差异。机制对比不是普遍权重结论，离线 IPS 与 winner proxy 筛选也不能替代真实线上效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>爱动作片用户搜索温馨喜剧时，应让查询覆盖部分长期偏好；若仍全按动作兴趣排，搜索画布可能相关性不足。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.18322">原论文</a> · <a href="../../../../reproductions/2608.18322-netflix-mediafm/">实现解读</a> · <a href="#qa-065b8f3cc5f30c5a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:netflix-mediafm" data-paper-title="Multimedia Asset Personalization via Multimodal Embeddings at Netflix" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Multimedia Asset Personalization via Multimodal Embeddings at Netflix 搜广推与 LLM 应用 Netflix 2026-08-18 把冻结的 CLIP/MediaFM 多模态表示作为共享在线特征接入资产双塔，并以查询相似度增强搜索画布；离线 IPS 与 winner proxy 先筛选 checkpoint。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  multimodal-recommendation content-understanding cold-start 搜广推 语义表征、用户知识与冷启动 MediaFM 融合两类点积分时，为什么三侧向量尺度要一致？ 用户、查询和资产需位于可比较空间或按定义校准，否则 α 表面平衡实际被一侧范数支配。checkpoint 筛选与融合权重不能用 test 反复挑选，冻结媒体特征也要绑定版本。本地电影内容代理不等于原多模态生产链路。 示意：查询向量范数十倍大，五五权重仍几乎只看查询；先明确归一与校准，才能解释融合比例而非仅看公式系数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-5b81e344e6b05c3a">MediaFM 融合两类点积分时，为什么三侧向量尺度要一致？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Anetflix-mediafm">Multimedia Asset Personalization via Multimodal Embeddings at Netflix</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Netflix</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用户、查询和资产需位于可比较空间或按定义校准，否则 α 表面平衡实际被一侧范数支配。checkpoint 筛选与融合权重不能用 test 反复挑选，冻结媒体特征也要绑定版本。本地电影内容代理不等于原多模态生产链路。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>查询向量范数十倍大，五五权重仍几乎只看查询；先明确归一与校准，才能解释融合比例而非仅看公式系数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.18322">原论文</a> · <a href="../../../../reproductions/2608.18322-netflix-mediafm/">实现解读</a> · <a href="#qa-5b81e344e6b05c3a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:connectionmind" data-paper-title="ConnectionMind: A General Social-Personalized Recommendation System with LLM Reasoning" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="ConnectionMind: A General Social-Personalized Recommendation System with LLM Reasoning 搜广推与 LLM 应用 Michigan State University 2026-08-10 传统社交推荐通常把好友关系压成静态 embedding，难以回答“某物品为什么经由哪条社交/兴趣路径被推荐”。ConnectionMind 把用户、物品和语义实体组成带关系类型、时间与权重的异构图；LLM policy 在任务相关子图内逐步扩展 frontier，同时输出推荐物品和对应证据路径。训练先从正反馈目标的最短路径做逐步 SFT，再用格式、最终推荐 F1 和最短路径 shaping 三类规则奖励做端到端 GRPO。 Fidelity：核心机制复现。使用论文同款 Delicious 公开数据，实际执行异构图构建、最短正路径 SFT、规则奖励 GRPO、学生蒸馏和重用户混合推理；本地负结果如实保留。没有复刻 Meta 私有视频图、Llama-3.1 3B/8B、生产级 GNN 和 serving；本地结果只验证完整算法路径，不代表复现论文线上增益。本地对照口径：基线为同一 Delicious 图、切分与候选集上的固定异构图聚合；实验组为 SFT+GRPO 路径 policy、蒸馏 student 与 10% 重用户混合推理，相对 NDCG@10 -7.44%。  social-recommendation llm-recommendation graph-reasoning reinforcement-learning distillation 搜广推 语义表征、用户知识与冷启动 ConnectionMind 为什么输出图证据路径，而不只给一个社交推荐分数？ 路径明确推荐经由哪些用户、物品与语义关系产生，使结果能接受关系、时间和权重的检查，也给分步训练提供监督。它是显式图搜索轨迹，不是事后自由编写理由；存在一条合法路径也不保证最终推荐有用，需独立评价结果。 示意：用户经好友的摄影收藏连到某教程，可以展示具体边；若只说“朋友可能喜欢”而没有图中对应节点与关系，就不是可核验的搜索证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-connectionmind-47def159" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-efd96cc24e42c304">ConnectionMind 为什么输出图证据路径，而不只给一个社交推荐分数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aconnectionmind">ConnectionMind: A General Social-Personalized Recommendation System with LLM Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Michigan State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>路径明确推荐经由哪些用户、物品与语义关系产生，使结果能接受关系、时间和权重的检查，也给分步训练提供监督。它是显式图搜索轨迹，不是事后自由编写理由；存在一条合法路径也不保证最终推荐有用，需独立评价结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户经好友的摄影收藏连到某教程，可以展示具体边；若只说“朋友可能喜欢”而没有图中对应节点与关系，就不是可核验的搜索证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.10187">原论文</a> · <a href="../../../../reproductions/2608.10187-connectionmind/">实现解读</a> · <a href="#qa-efd96cc24e42c304">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:connectionmind" data-paper-title="ConnectionMind: A General Social-Personalized Recommendation System with LLM Reasoning" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="ConnectionMind: A General Social-Personalized Recommendation System with LLM Reasoning 搜广推与 LLM 应用 Michigan State University 2026-08-10 传统社交推荐通常把好友关系压成静态 embedding，难以回答“某物品为什么经由哪条社交/兴趣路径被推荐”。ConnectionMind 把用户、物品和语义实体组成带关系类型、时间与权重的异构图；LLM policy 在任务相关子图内逐步扩展 frontier，同时输出推荐物品和对应证据路径。训练先从正反馈目标的最短路径做逐步 SFT，再用格式、最终推荐 F1 和最短路径 shaping 三类规则奖励做端到端 GRPO。 Fidelity：核心机制复现。使用论文同款 Delicious 公开数据，实际执行异构图构建、最短正路径 SFT、规则奖励 GRPO、学生蒸馏和重用户混合推理；本地负结果如实保留。没有复刻 Meta 私有视频图、Llama-3.1 3B/8B、生产级 GNN 和 serving；本地结果只验证完整算法路径，不代表复现论文线上增益。本地对照口径：基线为同一 Delicious 图、切分与候选集上的固定异构图聚合；实验组为 SFT+GRPO 路径 policy、蒸馏 student 与 10% 重用户混合推理，相对 NDCG@10 -7.44%。  social-recommendation llm-recommendation graph-reasoning reinforcement-learning distillation 搜广推 语义表征、用户知识与冷启动 ConnectionMind为什么输出证据路径，还把路径教师蒸馏给GNN？ 路径明确了推荐经由哪些关系逐步得到，能对中间扩展施加监督与奖励，而非只训练最终物品分数。复杂用户可用LLM在异构子图中搜索，较多普通流量交给蒸馏学生以控制成本。路径必须来自当前可见图；训练的最短正路径不能作为评估时已知答案直接提供给策略。 示意：从用户关注的作者走到摄影话题，再到教程，是一条可检查的证据链；简单场景可让学生复用这种关系模式，不必每次重新运行长程LLM搜索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-9ac4878088ac5aa1">ConnectionMind为什么输出证据路径，还把路径教师蒸馏给GNN？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aconnectionmind">ConnectionMind: A General Social-Personalized Recommendation System with LLM Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Michigan State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>路径明确了推荐经由哪些关系逐步得到，能对中间扩展施加监督与奖励，而非只训练最终物品分数。复杂用户可用LLM在异构子图中搜索，较多普通流量交给蒸馏学生以控制成本。路径必须来自当前可见图；训练的最短正路径不能作为评估时已知答案直接提供给策略。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>从用户关注的作者走到摄影话题，再到教程，是一条可检查的证据链；简单场景可让学生复用这种关系模式，不必每次重新运行长程LLM搜索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.10187">原论文</a> · <a href="../../../../reproductions/2608.10187-connectionmind/">实现解读</a> · <a href="#qa-9ac4878088ac5aa1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:connectionmind" data-paper-title="ConnectionMind: A General Social-Personalized Recommendation System with LLM Reasoning" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="ConnectionMind: A General Social-Personalized Recommendation System with LLM Reasoning 搜广推与 LLM 应用 Michigan State University 2026-08-10 传统社交推荐通常把好友关系压成静态 embedding，难以回答“某物品为什么经由哪条社交/兴趣路径被推荐”。ConnectionMind 把用户、物品和语义实体组成带关系类型、时间与权重的异构图；LLM policy 在任务相关子图内逐步扩展 frontier，同时输出推荐物品和对应证据路径。训练先从正反馈目标的最短路径做逐步 SFT，再用格式、最终推荐 F1 和最短路径 shaping 三类规则奖励做端到端 GRPO。 Fidelity：核心机制复现。使用论文同款 Delicious 公开数据，实际执行异构图构建、最短正路径 SFT、规则奖励 GRPO、学生蒸馏和重用户混合推理；本地负结果如实保留。没有复刻 Meta 私有视频图、Llama-3.1 3B/8B、生产级 GNN 和 serving；本地结果只验证完整算法路径，不代表复现论文线上增益。本地对照口径：基线为同一 Delicious 图、切分与候选集上的固定异构图聚合；实验组为 SFT+GRPO 路径 policy、蒸馏 student 与 10% 重用户混合推理，相对 NDCG@10 -7.44%。  social-recommendation llm-recommendation graph-reasoning reinforcement-learning distillation 搜广推 语义表征、用户知识与冷启动 ConnectionMind 的逐步 policy 与固定 GNN 聚合，相比推理范围和服务成本有何差别？ policy 可按当前任务逐步扩展 frontier，选择特定关系路径，GNN 则以固定传播结构汇聚邻域。前者更灵活也更昂贵，因此论文只让复杂少数流量走完整模型，其余蒸馏到 student。灵活搜索不保证精度更好，本地路径合法率满分仍伴随推荐负结果。 示意：复杂需求可先查好友再查共同标签，普通请求用蒸馏图模型快速返回；动作序列每步都合法，也可能一直走向过热门物品。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c016e4a2ff19e166">ConnectionMind 的逐步 policy 与固定 GNN 聚合，相比推理范围和服务成本有何差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aconnectionmind">ConnectionMind: A General Social-Personalized Recommendation System with LLM Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Michigan State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>policy 可按当前任务逐步扩展 frontier，选择特定关系路径，GNN 则以固定传播结构汇聚邻域。前者更灵活也更昂贵，因此论文只让复杂少数流量走完整模型，其余蒸馏到 student。灵活搜索不保证精度更好，本地路径合法率满分仍伴随推荐负结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>复杂需求可先查好友再查共同标签，普通请求用蒸馏图模型快速返回；动作序列每步都合法，也可能一直走向过热门物品。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.10187">原论文</a> · <a href="../../../../reproductions/2608.10187-connectionmind/">实现解读</a> · <a href="#qa-c016e4a2ff19e166">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:connectionmind" data-paper-title="ConnectionMind: A General Social-Personalized Recommendation System with LLM Reasoning" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="ConnectionMind: A General Social-Personalized Recommendation System with LLM Reasoning 搜广推与 LLM 应用 Michigan State University 2026-08-10 传统社交推荐通常把好友关系压成静态 embedding，难以回答“某物品为什么经由哪条社交/兴趣路径被推荐”。ConnectionMind 把用户、物品和语义实体组成带关系类型、时间与权重的异构图；LLM policy 在任务相关子图内逐步扩展 frontier，同时输出推荐物品和对应证据路径。训练先从正反馈目标的最短路径做逐步 SFT，再用格式、最终推荐 F1 和最短路径 shaping 三类规则奖励做端到端 GRPO。 Fidelity：核心机制复现。使用论文同款 Delicious 公开数据，实际执行异构图构建、最短正路径 SFT、规则奖励 GRPO、学生蒸馏和重用户混合推理；本地负结果如实保留。没有复刻 Meta 私有视频图、Llama-3.1 3B/8B、生产级 GNN 和 serving；本地结果只验证完整算法路径，不代表复现论文线上增益。本地对照口径：基线为同一 Delicious 图、切分与候选集上的固定异构图聚合；实验组为 SFT+GRPO 路径 policy、蒸馏 student 与 10% 重用户混合推理，相对 NDCG@10 -7.44%。  social-recommendation llm-recommendation graph-reasoning reinforcement-learning distillation 搜广推 语义表征、用户知识与冷启动 ConnectionMind 的最短路径示范在训练与评估中分别能否使用目标答案？ 训练可以从正反馈目标构造逐步监督，教策略合法动作；评估搜索状态不能读取 held-out 目标或 gold 路径，只能按当前图和上下文扩展。格式、推荐与路径 shaping 奖励也要区分。若评估直接给最短答案路径，只能算诊断，不能当作搜索能力。 示意：训练演示如何到达已知目标是合理监督；测试时若先告诉 agent 正确电影节点再导航，它只是跟答案走，无法证明能推荐该电影。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a25300cbe57ccb6c">ConnectionMind 的最短路径示范在训练与评估中分别能否使用目标答案？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aconnectionmind">ConnectionMind: A General Social-Personalized Recommendation System with LLM Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Michigan State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>训练可以从正反馈目标构造逐步监督，教策略合法动作；评估搜索状态不能读取 held-out 目标或 gold 路径，只能按当前图和上下文扩展。格式、推荐与路径 shaping 奖励也要区分。若评估直接给最短答案路径，只能算诊断，不能当作搜索能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练演示如何到达已知目标是合理监督；测试时若先告诉 agent 正确电影节点再导航，它只是跟答案走，无法证明能推荐该电影。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.10187">原论文</a> · <a href="../../../../reproductions/2608.10187-connectionmind/">实现解读</a> · <a href="#qa-a25300cbe57ccb6c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dme" data-paper-title="Douyin Multimodal Embedding Model Technical Report" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Douyin Multimodal Embedding Model Technical Report 搜广推与 LLM 应用 ByteDance / Douyin 2026-08-03 对比学习向量服务高效但监督过粗，显式 CoT 又无法在线服务。DME 先做大规模多模态对比预训练，再以 Evidence-Grounded Typed Latent Reasoning 整理检索证据，并用 Cross-Conditional Reconstruction 保留对侧细粒度语义；两个生成头只在训练期使用。 Fidelity：核心机制复现。公开数据只验证论文机制，不模拟生产流量。未复刻 2B/9B 多模态 backbone、抖音私有语料和十亿级向量索引。本地对照口径：基线为共享 transition + content scorer，实验组只加入 DME 核心机制；相对 NDCG@10 -8.84%。  content-understanding multimodal-retrieval embedding llm-recommendation 搜广推 语义表征、用户知识与冷启动 DME 为什么不仅做向量对比，还要求跨条件重建对侧细粒度语义？ 对比监督通常只强调哪些样本更近，可能忽略能区分近邻的细节。跨条件重建要求查询向量支持恢复文档信息、文档向量支持恢复查询信息，让压缩表示保存更多可用语义。重建并不保证无损，训练期信息也不能在服务时额外取回。 示意：两篇露营文档都相近，一篇讲冬季保暖、一篇讲轻量化；重建任务鼓励向量保留这些差别，而不是只记共同主题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-dme-01722658" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-de44944ba6c76358">DME 为什么不仅做向量对比，还要求跨条件重建对侧细粒度语义？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adme">Douyin Multimodal Embedding Model Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>对比监督通常只强调哪些样本更近，可能忽略能区分近邻的细节。跨条件重建要求查询向量支持恢复文档信息、文档向量支持恢复查询信息，让压缩表示保存更多可用语义。重建并不保证无损，训练期信息也不能在服务时额外取回。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两篇露营文档都相近，一篇讲冬季保暖、一篇讲轻量化；重建任务鼓励向量保留这些差别，而不是只记共同主题。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.02148">原论文</a> · <a href="../../../../reproductions/2608.02148-dme/">实现解读</a> · <a href="#qa-de44944ba6c76358">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dme" data-paper-title="Douyin Multimodal Embedding Model Technical Report" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Douyin Multimodal Embedding Model Technical Report 搜广推与 LLM 应用 ByteDance / Douyin 2026-08-03 对比学习向量服务高效但监督过粗，显式 CoT 又无法在线服务。DME 先做大规模多模态对比预训练，再以 Evidence-Grounded Typed Latent Reasoning 整理检索证据，并用 Cross-Conditional Reconstruction 保留对侧细粒度语义；两个生成头只在训练期使用。 Fidelity：核心机制复现。公开数据只验证论文机制，不模拟生产流量。未复刻 2B/9B 多模态 backbone、抖音私有语料和十亿级向量索引。本地对照口径：基线为共享 transition + content scorer，实验组只加入 DME 核心机制；相对 NDCG@10 -8.84%。  content-understanding multimodal-retrieval embedding llm-recommendation 搜广推 语义表征、用户知识与冷启动 DME的推理与重建生成头为什么只在训练期使用？ 对比向量便于在线检索，但可能忽略细粒度证据；训练期的typed latent目标和交叉重建要求表示保留对侧相关信息，再把这些能力压进检索向量。在线仍可只计算高效相似度，避免逐候选生成推理文本。辅助损失提供的是表示约束，不代表服务向量能忠实输出一条可解释推理链。 示意：训练中让查询向量保留商品的关键材质和用途，借重建任务检查是否丢失；上线直接用向量检索，不必为每一对查询和商品生成长解释。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-602408aa518e2b96">DME的推理与重建生成头为什么只在训练期使用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adme">Douyin Multimodal Embedding Model Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>对比向量便于在线检索，但可能忽略细粒度证据；训练期的typed latent目标和交叉重建要求表示保留对侧相关信息，再把这些能力压进检索向量。在线仍可只计算高效相似度，避免逐候选生成推理文本。辅助损失提供的是表示约束，不代表服务向量能忠实输出一条可解释推理链。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练中让查询向量保留商品的关键材质和用途，借重建任务检查是否丢失；上线直接用向量检索，不必为每一对查询和商品生成长解释。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.02148">原论文</a> · <a href="../../../../reproductions/2608.02148-dme/">实现解读</a> · <a href="#qa-602408aa518e2b96">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dme" data-paper-title="Douyin Multimodal Embedding Model Technical Report" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Douyin Multimodal Embedding Model Technical Report 搜广推与 LLM 应用 ByteDance / Douyin 2026-08-03 对比学习向量服务高效但监督过粗，显式 CoT 又无法在线服务。DME 先做大规模多模态对比预训练，再以 Evidence-Grounded Typed Latent Reasoning 整理检索证据，并用 Cross-Conditional Reconstruction 保留对侧细粒度语义；两个生成头只在训练期使用。 Fidelity：核心机制复现。公开数据只验证论文机制，不模拟生产流量。未复刻 2B/9B 多模态 backbone、抖音私有语料和十亿级向量索引。本地对照口径：基线为共享 transition + content scorer，实验组只加入 DME 核心机制；相对 NDCG@10 -8.84%。  content-understanding multimodal-retrieval embedding llm-recommendation 搜广推 语义表征、用户知识与冷启动 DME 的 typed latent evidence 与在线显式 CoT，相比保留和放弃了什么？ typed latent 以结构化内部证据训练表示，服务仍使用高效向量；显式 CoT 每次生成可读步骤但增加延迟。前者放弃在线完整文字解释来保留检索效率，也不能据内部状态存在就声称推理链忠实。来源本地的重建代理不等于完整多模态生成头。 示意：训练教模型区分地点、用途等证据类型，线上只返回向量检索结果；读者不能因此要求它展示逐步原文理由，因为该路径并未在线生成。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a00832a5e933a66e">DME 的 typed latent evidence 与在线显式 CoT，相比保留和放弃了什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adme">Douyin Multimodal Embedding Model Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>typed latent 以结构化内部证据训练表示，服务仍使用高效向量；显式 CoT 每次生成可读步骤但增加延迟。前者放弃在线完整文字解释来保留检索效率，也不能据内部状态存在就声称推理链忠实。来源本地的重建代理不等于完整多模态生成头。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练教模型区分地点、用途等证据类型，线上只返回向量检索结果；读者不能因此要求它展示逐步原文理由，因为该路径并未在线生成。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.02148">原论文</a> · <a href="../../../../reproductions/2608.02148-dme/">实现解读</a> · <a href="#qa-a00832a5e933a66e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dme" data-paper-title="Douyin Multimodal Embedding Model Technical Report" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Douyin Multimodal Embedding Model Technical Report 搜广推与 LLM 应用 ByteDance / Douyin 2026-08-03 对比学习向量服务高效但监督过粗，显式 CoT 又无法在线服务。DME 先做大规模多模态对比预训练，再以 Evidence-Grounded Typed Latent Reasoning 整理检索证据，并用 Cross-Conditional Reconstruction 保留对侧细粒度语义；两个生成头只在训练期使用。 Fidelity：核心机制复现。公开数据只验证论文机制，不模拟生产流量。未复刻 2B/9B 多模态 backbone、抖音私有语料和十亿级向量索引。本地对照口径：基线为共享 transition + content scorer，实验组只加入 DME 核心机制；相对 NDCG@10 -8.84%。  content-understanding multimodal-retrieval embedding llm-recommendation 搜广推 语义表征、用户知识与冷启动 DME 实现验收时，为什么要确认生成头确实从 serving 路径移除？ 两个生成头只应在训练损失中提供监督，推理输出取编码向量用于匹配。若在线仍执行重建，延迟和依赖就不符合预期；若训练头从未更新，又不能声称完成重建学习。本地 ridge 头诊断与原文大型多模态头需保留范围差异。 示意：训练记录可包含双向重建 loss，部署导出只保留两塔；若测延迟时关闭头、效果时开启头，两个结果就不是同一服务模型。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-9c41913d999f5f16">DME 实现验收时，为什么要确认生成头确实从 serving 路径移除？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adme">Douyin Multimodal Embedding Model Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两个生成头只应在训练损失中提供监督，推理输出取编码向量用于匹配。若在线仍执行重建，延迟和依赖就不符合预期；若训练头从未更新，又不能声称完成重建学习。本地 ridge 头诊断与原文大型多模态头需保留范围差异。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练记录可包含双向重建 loss，部署导出只保留两塔；若测延迟时关闭头、效果时开启头，两个结果就不是同一服务模型。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.02148">原论文</a> · <a href="../../../../reproductions/2608.02148-dme/">实现解读</a> · <a href="#qa-9c41913d999f5f16">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:kgd" data-paper-title="Knowledge–Geometry Decoupling: Refreshable Pretrained Transfer for Streaming Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Knowledge–Geometry Decoupling: Refreshable Pretrained Transfer for Streaming Recommendation 搜广推与 LLM 应用 Xiamen University / Shopee 2026-08-03 主题：流式推荐预训练与迁移。相邻点击并不总是有效依赖。KGD 用 BMTP 筛出协同或语义相关的未来物品；迁移时冻结可刷新知识编码器，用只读 cross-attention 读取知识，并以与锚点正交的 ACR 写入任务几何。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。MovieLens-1M 上比较相邻 NTP 与 BMTP+冻结知识+正交 ACR，执行全库排序。  sequential-recommendation pretraining streaming transfer 搜广推 语义表征、用户知识与冷启动 KGD 的 BMTP 为什么筛选相关未来物品，而非所有相邻点击都等价监督？ 相邻事件可能偶然出现或属于不同需求，盲目预测会将无效转移写进知识。BMTP 用协同或语义关系挑更有意义未来目标，再让迁移任务只读知识。筛选依赖关系质量，可能错过真实新兴趣；未来标签仍限训练监督。 示意：看相机后误点一条体育新闻，不一定应强学这条转移；相关未来镜头更像同一需求，但不能因此永久排斥跨主题探索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-kgd-b25439a8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-28611cd58dfcd19a">KGD 的 BMTP 为什么筛选相关未来物品，而非所有相邻点击都等价监督？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Akgd">Knowledge–Geometry Decoupling: Refreshable Pretrained Transfer for Streaming Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiamen University / Shopee</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相邻事件可能偶然出现或属于不同需求，盲目预测会将无效转移写进知识。BMTP 用协同或语义关系挑更有意义未来目标，再让迁移任务只读知识。筛选依赖关系质量，可能错过真实新兴趣；未来标签仍限训练监督。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>看相机后误点一条体育新闻，不一定应强学这条转移；相关未来镜头更像同一需求，但不能因此永久排斥跨主题探索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.02738">原论文</a> · <a href="../../../../reproductions/2608.02738-kgd/">实现解读</a> · <a href="#qa-28611cd58dfcd19a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:kgd" data-paper-title="Knowledge–Geometry Decoupling: Refreshable Pretrained Transfer for Streaming Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Knowledge–Geometry Decoupling: Refreshable Pretrained Transfer for Streaming Recommendation 搜广推与 LLM 应用 Xiamen University / Shopee 2026-08-03 主题：流式推荐预训练与迁移。相邻点击并不总是有效依赖。KGD 用 BMTP 筛出协同或语义相关的未来物品；迁移时冻结可刷新知识编码器，用只读 cross-attention 读取知识，并以与锚点正交的 ACR 写入任务几何。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。MovieLens-1M 上比较相邻 NTP 与 BMTP+冻结知识+正交 ACR，执行全库排序。  sequential-recommendation pretraining streaming transfer 搜广推 语义表征、用户知识与冷启动 KGD为什么筛选相关未来物品，并让迁移残差与知识锚点正交？ 紧邻点击可能是噪声或任务切换，BMTP选择协同或语义相关的未来目标，让预训练知识更集中。迁移时冻结可刷新的知识编码器，任务侧只读它，再用去除锚点投影的残差补充新几何，减少直接覆盖已有知识。正交限制只规定更新方向，不能保证所有任务信息都能无损共存。 示意：相邻一次误触不应和稳定摄影需求同等监督；新任务要增加价格敏感信息时，可尽量沿知识锚点之外补充，而不是把已有摄影语义整体改写。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c9bfc27b1d0a91a3">KGD为什么筛选相关未来物品，并让迁移残差与知识锚点正交？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Akgd">Knowledge–Geometry Decoupling: Refreshable Pretrained Transfer for Streaming Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiamen University / Shopee</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>紧邻点击可能是噪声或任务切换，BMTP选择协同或语义相关的未来目标，让预训练知识更集中。迁移时冻结可刷新的知识编码器，任务侧只读它，再用去除锚点投影的残差补充新几何，减少直接覆盖已有知识。正交限制只规定更新方向，不能保证所有任务信息都能无损共存。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>相邻一次误触不应和稳定摄影需求同等监督；新任务要增加价格敏感信息时，可尽量沿知识锚点之外补充，而不是把已有摄影语义整体改写。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.02738">原论文</a> · <a href="../../../../reproductions/2608.02738-kgd/">实现解读</a> · <a href="#qa-c9bfc27b1d0a91a3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:kgd" data-paper-title="Knowledge–Geometry Decoupling: Refreshable Pretrained Transfer for Streaming Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Knowledge–Geometry Decoupling: Refreshable Pretrained Transfer for Streaming Recommendation 搜广推与 LLM 应用 Xiamen University / Shopee 2026-08-03 主题：流式推荐预训练与迁移。相邻点击并不总是有效依赖。KGD 用 BMTP 筛出协同或语义相关的未来物品；迁移时冻结可刷新知识编码器，用只读 cross-attention 读取知识，并以与锚点正交的 ACR 写入任务几何。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。MovieLens-1M 上比较相邻 NTP 与 BMTP+冻结知识+正交 ACR，执行全库排序。  sequential-recommendation pretraining streaming transfer 搜广推 语义表征、用户知识与冷启动 KGD 的正交 ACR 与普通残差 adapter，相比限制了哪种改写？ 从残差中去除沿知识锚点的投影，意在让任务补充方向不直接覆写已有主方向。普通残差可任意叠加，表达更自由也更可能干扰。正交只是几何约束，不代表知识完全不变或语义独立，效果需按任务验证。 示意：知识已有“摄影”方向，适配器可补预算差别而非仅把摄影强度放大；但垂直向量仍可能编码噪声，不能因正交就认定有用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0265ca8ff93aafab">KGD 的正交 ACR 与普通残差 adapter，相比限制了哪种改写？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Akgd">Knowledge–Geometry Decoupling: Refreshable Pretrained Transfer for Streaming Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiamen University / Shopee</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>从残差中去除沿知识锚点的投影，意在让任务补充方向不直接覆写已有主方向。普通残差可任意叠加，表达更自由也更可能干扰。正交只是几何约束，不代表知识完全不变或语义独立，效果需按任务验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>知识已有“摄影”方向，适配器可补预算差别而非仅把摄影强度放大；但垂直向量仍可能编码噪声，不能因正交就认定有用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.02738">原论文</a> · <a href="../../../../reproductions/2608.02738-kgd/">实现解读</a> · <a href="#qa-0265ca8ff93aafab">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:kgd" data-paper-title="Knowledge–Geometry Decoupling: Refreshable Pretrained Transfer for Streaming Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Knowledge–Geometry Decoupling: Refreshable Pretrained Transfer for Streaming Recommendation 搜广推与 LLM 应用 Xiamen University / Shopee 2026-08-03 主题：流式推荐预训练与迁移。相邻点击并不总是有效依赖。KGD 用 BMTP 筛出协同或语义相关的未来物品；迁移时冻结可刷新知识编码器，用只读 cross-attention 读取知识，并以与锚点正交的 ACR 写入任务几何。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。MovieLens-1M 上比较相邻 NTP 与 BMTP+冻结知识+正交 ACR，执行全库排序。  sequential-recommendation pretraining streaming transfer 搜广推 语义表征、用户知识与冷启动 KGD 的只读知识与正交投影应怎样检查梯度和零范数边界？ 冻结知识编码器或明确刷新版本，任务损失不得通过只读接口更新它；ACR 投影分母依赖锚点范数，零或近零需定义处理。代码若只写 r−e 而非投影，就不是正交残差。本地有界机制不能代表流式生产迁移全部完成。 示意：锚点为零时没有方向可投影，不能直接除以零；一次反传后知识参数若变化，也已违背只读迁移，哪怕输出维度正常。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c165c1f6afe4f688">KGD 的只读知识与正交投影应怎样检查梯度和零范数边界？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Akgd">Knowledge–Geometry Decoupling: Refreshable Pretrained Transfer for Streaming Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiamen University / Shopee</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冻结知识编码器或明确刷新版本，任务损失不得通过只读接口更新它；ACR 投影分母依赖锚点范数，零或近零需定义处理。代码若只写 r−e 而非投影，就不是正交残差。本地有界机制不能代表流式生产迁移全部完成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>锚点为零时没有方向可投影，不能直接除以零；一次反传后知识参数若变化，也已违背只读迁移，哪怕输出维度正常。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.02738">原论文</a> · <a href="../../../../reproductions/2608.02738-kgd/">实现解读</a> · <a href="#qa-c165c1f6afe4f688">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gala" data-paper-title="GALA: Generative Aligned Learning for Adaptive Multimodal Representation in the Taobao Shangou Recommender System" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="GALA: Generative Aligned Learning for Adaptive Multimodal Representation in the Taobao Shangou Recommender System 搜广推与 LLM 应用 Rajax Network Technology / Taobao Shangou / Alibaba 2026-07-31 先在 query-image-text 三元组上预训练多模态表示，再以行为奖励做 GRPO 对齐，最后用自适应门控融合多模态与 ID 表示。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  multimodal-recommendation representation-alignment reinforcement-learning 搜广推 语义表征、用户知识与冷启动 GALA 为什么把多模态与 ID 表示视为互补，而非互相替代？ 多模态编码可迁移内容语义，ID 表示保留平台行为记忆，可靠性随物品和上下文变化。门控融合让模型选择两侧贡献，行为奖励再把预训语义拉向推荐目标。内容强不保证协同无用，ID 强也不能解决新品缺反馈。 示意：新品先靠图文判断用途，热门老品可借丰富点击历史；同一用户面对两件商品，融合比例不必相同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-gala-83e5be9a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2bc4828f01afa008">GALA 为什么把多模态与 ID 表示视为互补，而非互相替代？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agala">GALA: Generative Aligned Learning for Adaptive Multimodal Representation in the Taobao Shangou Recommender System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Rajax Network Technology / Taobao Shangou / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多模态编码可迁移内容语义，ID 表示保留平台行为记忆，可靠性随物品和上下文变化。门控融合让模型选择两侧贡献，行为奖励再把预训语义拉向推荐目标。内容强不保证协同无用，ID 强也不能解决新品缺反馈。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新品先靠图文判断用途，热门老品可借丰富点击历史；同一用户面对两件商品，融合比例不必相同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.29213">原论文</a> · <a href="../../../../reproductions/2607.29213-gala/">实现解读</a> · <a href="#qa-2bc4828f01afa008">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gala" data-paper-title="GALA: Generative Aligned Learning for Adaptive Multimodal Representation in the Taobao Shangou Recommender System" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="GALA: Generative Aligned Learning for Adaptive Multimodal Representation in the Taobao Shangou Recommender System 搜广推与 LLM 应用 Rajax Network Technology / Taobao Shangou / Alibaba 2026-07-31 先在 query-image-text 三元组上预训练多模态表示，再以行为奖励做 GRPO 对齐，最后用自适应门控融合多模态与 ID 表示。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  multimodal-recommendation representation-alignment reinforcement-learning 搜广推 语义表征、用户知识与冷启动 GALA完成图文预训练后，为什么仍要用行为奖励对齐并门控融合ID表示？ 图文相互匹配不代表符合个性化消费偏好，行为奖励让多模态表示朝推荐任务调整。门控再根据样本决定语义和ID信息的比例，避免内容优势覆盖已有协同知识，也让新物品更有机会利用内容。奖励有偏或门控塌到单一路径时仍可能失效，不能把多模态检索能力直接当最终推荐收益。 示意：商品图片和文案彼此一致，却不一定适合某位用户；行为对齐补上偏好信号，门控对有大量反馈的老商品和无反馈新品采用不同依赖。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-a98952ce877a50dd">GALA完成图文预训练后，为什么仍要用行为奖励对齐并门控融合ID表示？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agala">GALA: Generative Aligned Learning for Adaptive Multimodal Representation in the Taobao Shangou Recommender System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Rajax Network Technology / Taobao Shangou / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>图文相互匹配不代表符合个性化消费偏好，行为奖励让多模态表示朝推荐任务调整。门控再根据样本决定语义和ID信息的比例，避免内容优势覆盖已有协同知识，也让新物品更有机会利用内容。奖励有偏或门控塌到单一路径时仍可能失效，不能把多模态检索能力直接当最终推荐收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>商品图片和文案彼此一致，却不一定适合某位用户；行为对齐补上偏好信号，门控对有大量反馈的老商品和无反馈新品采用不同依赖。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.29213">原论文</a> · <a href="../../../../reproductions/2607.29213-gala/">实现解读</a> · <a href="#qa-a98952ce877a50dd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gala" data-paper-title="GALA: Generative Aligned Learning for Adaptive Multimodal Representation in the Taobao Shangou Recommender System" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="GALA: Generative Aligned Learning for Adaptive Multimodal Representation in the Taobao Shangou Recommender System 搜广推与 LLM 应用 Rajax Network Technology / Taobao Shangou / Alibaba 2026-07-31 先在 query-image-text 三元组上预训练多模态表示，再以行为奖励做 GRPO 对齐，最后用自适应门控融合多模态与 ID 表示。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  multimodal-recommendation representation-alignment reinforcement-learning 搜广推 语义表征、用户知识与冷启动 GALA 的行为 GRPO 与图文预训练，相比正例与奖励来源有什么变化？ 预训练学习 query、图像、文字间对齐，行为后训练利用实际推荐目标比较生成或表示选择，使语义不只停在内容相似。反馈仍可能有曝光偏差，目标变化也可能损害语义能力；不能把一个公开代理权重结果当作完整多模态策略训练。 示意：两张外套图很像，平台用户却在通勤场景更喜欢其中一件，行为对齐尝试保留这种差别，而非继续只追图文配对正确。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0b1a61d045c96205">GALA 的行为 GRPO 与图文预训练，相比正例与奖励来源有什么变化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agala">GALA: Generative Aligned Learning for Adaptive Multimodal Representation in the Taobao Shangou Recommender System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Rajax Network Technology / Taobao Shangou / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>预训练学习 query、图像、文字间对齐，行为后训练利用实际推荐目标比较生成或表示选择，使语义不只停在内容相似。反馈仍可能有曝光偏差，目标变化也可能损害语义能力；不能把一个公开代理权重结果当作完整多模态策略训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两张外套图很像，平台用户却在通勤场景更喜欢其中一件，行为对齐尝试保留这种差别，而非继续只追图文配对正确。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.29213">原论文</a> · <a href="../../../../reproductions/2607.29213-gala/">实现解读</a> · <a href="#qa-0b1a61d045c96205">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gala" data-paper-title="GALA: Generative Aligned Learning for Adaptive Multimodal Representation in the Taobao Shangou Recommender System" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="GALA: Generative Aligned Learning for Adaptive Multimodal Representation in the Taobao Shangou Recommender System 搜广推与 LLM 应用 Rajax Network Technology / Taobao Shangou / Alibaba 2026-07-31 先在 query-image-text 三元组上预训练多模态表示，再以行为奖励做 GRPO 对齐，最后用自适应门控融合多模态与 ID 表示。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  multimodal-recommendation representation-alignment reinforcement-learning 搜广推 语义表征、用户知识与冷启动 GALA 的 sigmoid gate 在融合前为什么要求两侧维度及 item 身份对齐？ 逐元素 g 作用于多模态与 ID 向量，两侧需同维、同候选，gate 输入也应来自该配对。错位向量不会因 sigmoid 有界而变正确，冷启动 ID 缺失应按定义处理。生产大模型训练和本地内容代理需分别记录。 示意：甲商品的图文向量不能与乙商品 ID 混合；即使结果数值有限，融合已失去商品含义，单看前向通过无法发现。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0b28d03f4103a30f">GALA 的 sigmoid gate 在融合前为什么要求两侧维度及 item 身份对齐？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agala">GALA: Generative Aligned Learning for Adaptive Multimodal Representation in the Taobao Shangou Recommender System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Rajax Network Technology / Taobao Shangou / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>逐元素 g 作用于多模态与 ID 向量，两侧需同维、同候选，gate 输入也应来自该配对。错位向量不会因 sigmoid 有界而变正确，冷启动 ID 缺失应按定义处理。生产大模型训练和本地内容代理需分别记录。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>甲商品的图文向量不能与乙商品 ID 混合；即使结果数值有限，融合已失去商品含义，单看前向通过无法发现。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.29213">原论文</a> · <a href="../../../../reproductions/2607.29213-gala/">实现解读</a> · <a href="#qa-0b28d03f4103a30f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:open-web-ufm" data-paper-title="Building a User Foundation Model for the Open Web" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Building a User Foundation Model for the Open Web 搜广推与 LLM 应用 Teads 2026-07-30 开放网络 RTB 的用户身份不连续、历史短且受隐私选择影响。论文以 MLM 与序列级对比学习预训练浏览历史 Transformer，再向 CTR、赢标率等任务输出统一用户表示；训练配方由可审计 lifter 组成的 LLM-in-the-loop 搜索改进。 Fidelity: 核心机制复现。实现共享序列 encoder、双视图对比预训练和下游微调。未包含 Teads RTB 私有特征、Claude Opus lifter 搜索及生产 GDCN adapter。本地对照口径：基线与实验组使用同一 encoder、数据和 45 steps；实验组加入双视图预训练，相对基线 NDCG@10 +0.00%。  advertising user-foundation-model self-supervised-learning llm-optimizer 搜广推 语义表征、用户知识与冷启动 开放网络 UFM 为什么不能默认稳定的长期 user ID 与完整历史？ RTB 身份受权限、平台和隐私选择限制，用户轨迹可能短且不连续。预训需从有限浏览学习可迁移表示，再服务 CTR、赢标等任务。这个数据条件与登录平台长序列不同，不能把 MovieLens 结果直接当开放网络身份建模证据。 示意：同一人跨设备可能被看成不同短轨迹，模型不能假设每条日志都能拼成多年历史；实验设计应承认缺失而非用全局 ID 补齐。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-open-web-ufm-467147f2" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f33b067fd0273ebc">开放网络 UFM 为什么不能默认稳定的长期 user ID 与完整历史？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aopen-web-ufm">Building a User Foundation Model for the Open Web</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Teads</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>RTB 身份受权限、平台和隐私选择限制，用户轨迹可能短且不连续。预训需从有限浏览学习可迁移表示，再服务 CTR、赢标等任务。这个数据条件与登录平台长序列不同，不能把 MovieLens 结果直接当开放网络身份建模证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一人跨设备可能被看成不同短轨迹，模型不能假设每条日志都能拼成多年历史；实验设计应承认缺失而非用全局 ID 补齐。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28019">原论文</a> · <a href="../../../../reproductions/2607.28019-open-web-ufm/">实现解读</a> · <a href="#qa-f33b067fd0273ebc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:open-web-ufm" data-paper-title="Building a User Foundation Model for the Open Web" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Building a User Foundation Model for the Open Web 搜广推与 LLM 应用 Teads 2026-07-30 开放网络 RTB 的用户身份不连续、历史短且受隐私选择影响。论文以 MLM 与序列级对比学习预训练浏览历史 Transformer，再向 CTR、赢标率等任务输出统一用户表示；训练配方由可审计 lifter 组成的 LLM-in-the-loop 搜索改进。 Fidelity: 核心机制复现。实现共享序列 encoder、双视图对比预训练和下游微调。未包含 Teads RTB 私有特征、Claude Opus lifter 搜索及生产 GDCN adapter。本地对照口径：基线与实验组使用同一 encoder、数据和 45 steps；实验组加入双视图预训练，相对基线 NDCG@10 +0.00%。  advertising user-foundation-model self-supervised-learning llm-optimizer 搜广推 语义表征、用户知识与冷启动 开放网络 UFM 为什么联合掩码预测与序列对比学习，而不只训练某一个 CTR 标签？ 掩码预测要求编码器从残缺浏览上下文恢复局部事件，对比学习要求同一用户序列的不同视图保持一致，分别提供局部与整体监督。预训练表示再供 CTR、赢标率等任务使用，减少对单一稀疏标签的依赖。但身份不连续和隐私选择仍影响输入分布，本地小切片的零增益不能被改写成跨任务有效性证据。 示意：一个短历史只有三次访问且没有点击标签。遮住其中一次仍可做上下文训练，同一历史的两种扰动也可构成正对；之后再用少量 CTR 标签训练任务头。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-ad5326f868c277b5">开放网络 UFM 为什么联合掩码预测与序列对比学习，而不只训练某一个 CTR 标签？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aopen-web-ufm">Building a User Foundation Model for the Open Web</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Teads</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>掩码预测要求编码器从残缺浏览上下文恢复局部事件，对比学习要求同一用户序列的不同视图保持一致，分别提供局部与整体监督。预训练表示再供 CTR、赢标率等任务使用，减少对单一稀疏标签的依赖。但身份不连续和隐私选择仍影响输入分布，本地小切片的零增益不能被改写成跨任务有效性证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个短历史只有三次访问且没有点击标签。遮住其中一次仍可做上下文训练，同一历史的两种扰动也可构成正对；之后再用少量 CTR 标签训练任务头。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28019">原论文</a> · <a href="../../../../reproductions/2607.28019-open-web-ufm/">实现解读</a> · <a href="#qa-ad5326f868c277b5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:open-web-ufm" data-paper-title="Building a User Foundation Model for the Open Web" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Building a User Foundation Model for the Open Web 搜广推与 LLM 应用 Teads 2026-07-30 开放网络 RTB 的用户身份不连续、历史短且受隐私选择影响。论文以 MLM 与序列级对比学习预训练浏览历史 Transformer，再向 CTR、赢标率等任务输出统一用户表示；训练配方由可审计 lifter 组成的 LLM-in-the-loop 搜索改进。 Fidelity: 核心机制复现。实现共享序列 encoder、双视图对比预训练和下游微调。未包含 Teads RTB 私有特征、Claude Opus lifter 搜索及生产 GDCN adapter。本地对照口径：基线与实验组使用同一 encoder、数据和 45 steps；实验组加入双视图预训练，相对基线 NDCG@10 +0.00%。  advertising user-foundation-model self-supervised-learning llm-optimizer 搜广推 语义表征、用户知识与冷启动 MLM 局部恢复与序列 InfoNCE，两种自监督对哪类一致性施压？ MLM 要从上下文恢复被遮事件，关注局部内容关系；序列对比让同轨迹不同视图接近，关注整体稳定性。两者可补充，但视图破坏过强或假负例会误教。联合目标存在不证明跨任务迁移获益，来源本地为零结果。 示意：遮一次网站访问仍可由邻居推断，删部分行为后的整段也应保留相近兴趣；若两视图已代表不同需求，硬拉近可能有害。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-aa71a813cea60613">MLM 局部恢复与序列 InfoNCE，两种自监督对哪类一致性施压？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aopen-web-ufm">Building a User Foundation Model for the Open Web</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Teads</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>MLM 要从上下文恢复被遮事件，关注局部内容关系；序列对比让同轨迹不同视图接近，关注整体稳定性。两者可补充，但视图破坏过强或假负例会误教。联合目标存在不证明跨任务迁移获益，来源本地为零结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>遮一次网站访问仍可由邻居推断，删部分行为后的整段也应保留相近兴趣；若两视图已代表不同需求，硬拉近可能有害。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28019">原论文</a> · <a href="../../../../reproductions/2607.28019-open-web-ufm/">实现解读</a> · <a href="#qa-aa71a813cea60613">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:open-web-ufm" data-paper-title="Building a User Foundation Model for the Open Web" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Building a User Foundation Model for the Open Web 搜广推与 LLM 应用 Teads 2026-07-30 开放网络 RTB 的用户身份不连续、历史短且受隐私选择影响。论文以 MLM 与序列级对比学习预训练浏览历史 Transformer，再向 CTR、赢标率等任务输出统一用户表示；训练配方由可审计 lifter 组成的 LLM-in-the-loop 搜索改进。 Fidelity: 核心机制复现。实现共享序列 encoder、双视图对比预训练和下游微调。未包含 Teads RTB 私有特征、Claude Opus lifter 搜索及生产 GDCN adapter。本地对照口径：基线与实验组使用同一 encoder、数据和 45 steps；实验组加入双视图预训练，相对基线 NDCG@10 +0.00%。  advertising user-foundation-model self-supervised-learning llm-optimizer 搜广推 语义表征、用户知识与冷启动 UFM 配方搜索中的 lifter 为什么要可审计而不能任意改数据与评测？ 搜索算子需明确定义允许变化，才能将反馈归给实际配方，保留预算与数据契约。随意换样本或评测可制造假改善，LLM 提案不应拥有改答案权限。本地同 encoder、同四十五步对照的零变化也应如实保留，不能靠扩大搜索口径隐藏。 示意：一个 lifter 只改 mask 比例可比较；若同时删除困难测试用户，再说预训更好，就已改变问题而非找到有效训练配方。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d3a95c8f2ee5f83e">UFM 配方搜索中的 lifter 为什么要可审计而不能任意改数据与评测？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aopen-web-ufm">Building a User Foundation Model for the Open Web</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Teads</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>搜索算子需明确定义允许变化，才能将反馈归给实际配方，保留预算与数据契约。随意换样本或评测可制造假改善，LLM 提案不应拥有改答案权限。本地同 encoder、同四十五步对照的零变化也应如实保留，不能靠扩大搜索口径隐藏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个 lifter 只改 mask 比例可比较；若同时删除困难测试用户，再说预训更好，就已改变问题而非找到有效训练配方。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28019">原论文</a> · <a href="../../../../reproductions/2607.28019-open-web-ufm/">实现解读</a> · <a href="#qa-d3a95c8f2ee5f83e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:reco-reward" data-paper-title="RecoReward: Recommender-Guided Multimodal Description Generation for Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RecoReward: Recommender-Guided Multimodal Description Generation for Recommendation 搜广推与 LLM 应用 Kuaishou / Nankai University / Chinese Academy of Sciences 2026-07-28 冻结双塔推荐器，以目标用户与非目标用户的亲和力差作为奖励训练内容描述；线上 serving 只消费描述，不依赖用户画像。 Fidelity: 核心机制复现。本地执行推荐奖励目标与公开数据对照，不声称复刻生产 reward pipeline。没有微调 Qwen3.5-9B，也没有直播视频和快手私有行为；本地结果只验证 RAS 奖励可执行。本地对照口径：基线为 content-only semantic recall，实验组为 RAS 选择；Hit@10 -16.00%、NDCG@10 -9.68%，head share -24.14%（负结果）。  llm-recommendation multimodal reinforcement-learning retrieval 搜广推 语义表征、用户知识与冷启动 Reco-Reward 为什么训练内容描述而不是在线生成用户画像？ 冻结推荐器提供受众亲和奖励，优化描述让商品内容更能表达适合谁，服务只消费描述，不依赖请求时个人画像生成。用户参与训练监督不等于线上暴露用户资料。描述仍应忠于商品，不能为拉亲和虚构事实。 示意：为手冲咖啡突出酸质与冲煮参数，面向目标受众而非每次实时写一段用户画像；若原商品不含这些属性，就不能凭奖励编造。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-reco-reward-d01ebaa7" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ea7638de3d26e2b0">Reco-Reward 为什么训练内容描述而不是在线生成用户画像？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Areco-reward">RecoReward: Recommender-Guided Multimodal Description Generation for Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou / Nankai University / Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冻结推荐器提供受众亲和奖励，优化描述让商品内容更能表达适合谁，服务只消费描述，不依赖请求时个人画像生成。用户参与训练监督不等于线上暴露用户资料。描述仍应忠于商品，不能为拉亲和虚构事实。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>为手冲咖啡突出酸质与冲煮参数，面向目标受众而非每次实时写一段用户画像；若原商品不含这些属性，就不能凭奖励编造。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25901">原论文</a> · <a href="../../../../reproductions/2607.25901-reco-reward/">实现解读</a> · <a href="#qa-ea7638de3d26e2b0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:reco-reward" data-paper-title="RecoReward: Recommender-Guided Multimodal Description Generation for Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RecoReward: Recommender-Guided Multimodal Description Generation for Recommendation 搜广推与 LLM 应用 Kuaishou / Nankai University / Chinese Academy of Sciences 2026-07-28 冻结双塔推荐器，以目标用户与非目标用户的亲和力差作为奖励训练内容描述；线上 serving 只消费描述，不依赖用户画像。 Fidelity: 核心机制复现。本地执行推荐奖励目标与公开数据对照，不声称复刻生产 reward pipeline。没有微调 Qwen3.5-9B，也没有直播视频和快手私有行为；本地结果只验证 RAS 奖励可执行。本地对照口径：基线为 content-only semantic recall，实验组为 RAS 选择；Hit@10 -16.00%、NDCG@10 -9.68%，head share -24.14%（负结果）。  llm-recommendation multimodal reinforcement-learning retrieval 搜广推 语义表征、用户知识与冷启动 Reco-Reward 为什么奖励目标用户亲和力减去非目标用户亲和力，而不是只最大化通用吸引力？ 只提高目标用户得分可能产生对所有人都相似的热门描述。减去非目标用户亲和力，鼓励描述保留能区分目标受众的特征，冻结双塔又提供稳定奖励接口。线上只消费优化后的内容描述，不需要实时用户画像；但奖励模型可能有盲点，差分得分提高不等于真实用户满意度已被验证。 示意：把咖啡描述写成“品质好、人人爱喝”可能吸引所有人却缺少区分。针对手冲爱好者突出酸质与冲煮参数，才可能提高目标人群相对其他人群的亲和力。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-e8f960e892ab7740">Reco-Reward 为什么奖励目标用户亲和力减去非目标用户亲和力，而不是只最大化通用吸引力？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Areco-reward">RecoReward: Recommender-Guided Multimodal Description Generation for Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou / Nankai University / Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只提高目标用户得分可能产生对所有人都相似的热门描述。减去非目标用户亲和力，鼓励描述保留能区分目标受众的特征，冻结双塔又提供稳定奖励接口。线上只消费优化后的内容描述，不需要实时用户画像；但奖励模型可能有盲点，差分得分提高不等于真实用户满意度已被验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把咖啡描述写成“品质好、人人爱喝”可能吸引所有人却缺少区分。针对手冲爱好者突出酸质与冲煮参数，才可能提高目标人群相对其他人群的亲和力。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25901">原论文</a> · <a href="../../../../reproductions/2607.25901-reco-reward/">实现解读</a> · <a href="#qa-e8f960e892ab7740">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:reco-reward" data-paper-title="RecoReward: Recommender-Guided Multimodal Description Generation for Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RecoReward: Recommender-Guided Multimodal Description Generation for Recommendation 搜广推与 LLM 应用 Kuaishou / Nankai University / Chinese Academy of Sciences 2026-07-28 冻结双塔推荐器，以目标用户与非目标用户的亲和力差作为奖励训练内容描述；线上 serving 只消费描述，不依赖用户画像。 Fidelity: 核心机制复现。本地执行推荐奖励目标与公开数据对照，不声称复刻生产 reward pipeline。没有微调 Qwen3.5-9B，也没有直播视频和快手私有行为；本地结果只验证 RAS 奖励可执行。本地对照口径：基线为 content-only semantic recall，实验组为 RAS 选择；Hit@10 -16.00%、NDCG@10 -9.68%，head share -24.14%（负结果）。  llm-recommendation multimodal reinforcement-learning retrieval 搜广推 语义表征、用户知识与冷启动 Reco-Reward 的冻结模型奖励升高，与真实用户更喜欢描述，为什么不是同一证据？ RAS 由固定双塔估计目标与非目标亲和差，优化可以学会利用这把尺子的盲点；真实用户反应还受事实、表达与场景影响。冻结保证比较尺子不跟着动，却不保证尺子正确。应分别验证奖励、内容忠实和独立行为结果，不能用模型高分替代用户实验。 示意：反复堆目标人群关联词可能抬高双塔亲和，却让文案难读或夸大商品；模型奖励上升并不说明真实读者因此更愿意购买。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-874889432bfcaf0c">Reco-Reward 的冻结模型奖励升高，与真实用户更喜欢描述，为什么不是同一证据？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Areco-reward">RecoReward: Recommender-Guided Multimodal Description Generation for Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou / Nankai University / Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>RAS 由固定双塔估计目标与非目标亲和差，优化可以学会利用这把尺子的盲点；真实用户反应还受事实、表达与场景影响。冻结保证比较尺子不跟着动，却不保证尺子正确。应分别验证奖励、内容忠实和独立行为结果，不能用模型高分替代用户实验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>反复堆目标人群关联词可能抬高双塔亲和，却让文案难读或夸大商品；模型奖励上升并不说明真实读者因此更愿意购买。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25901">原论文</a> · <a href="../../../../reproductions/2607.25901-reco-reward/">实现解读</a> · <a href="#qa-874889432bfcaf0c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:reco-reward" data-paper-title="RecoReward: Recommender-Guided Multimodal Description Generation for Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RecoReward: Recommender-Guided Multimodal Description Generation for Recommendation 搜广推与 LLM 应用 Kuaishou / Nankai University / Chinese Academy of Sciences 2026-07-28 冻结双塔推荐器，以目标用户与非目标用户的亲和力差作为奖励训练内容描述；线上 serving 只消费描述，不依赖用户画像。 Fidelity: 核心机制复现。本地执行推荐奖励目标与公开数据对照，不声称复刻生产 reward pipeline。没有微调 Qwen3.5-9B，也没有直播视频和快手私有行为；本地结果只验证 RAS 奖励可执行。本地对照口径：基线为 content-only semantic recall，实验组为 RAS 选择；Hit@10 -16.00%、NDCG@10 -9.68%，head share -24.14%（负结果）。  llm-recommendation multimodal reinforcement-learning retrieval 搜广推 语义表征、用户知识与冷启动 RAS 实现为何要冻结双塔，并记录非目标样本来自哪里？ 奖励器若随策略一起变，分数可因教师漂移升高而非描述改善；非目标分布也影响扣减项。生成或选择描述与评估集合必须隔离，测试用户不能作为训练金标准。本地用历史质心代理用户塔，不能视为完整生产推荐器。 示意：描述变差但奖励网络同时调整也给高分，会造成自我强化；冻结后至少固定尺子，但尺子自身偏差仍需独立评价。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f2287813475ac9e0">RAS 实现为何要冻结双塔，并记录非目标样本来自哪里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Areco-reward">RecoReward: Recommender-Guided Multimodal Description Generation for Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou / Nankai University / Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>奖励器若随策略一起变，分数可因教师漂移升高而非描述改善；非目标分布也影响扣减项。生成或选择描述与评估集合必须隔离，测试用户不能作为训练金标准。本地用历史质心代理用户塔，不能视为完整生产推荐器。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>描述变差但奖励网络同时调整也给高分，会造成自我强化；冻结后至少固定尺子，但尺子自身偏差仍需独立评价。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25901">原论文</a> · <a href="../../../../reproductions/2607.25901-reco-reward/">实现解读</a> · <a href="#qa-f2287813475ac9e0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mosaic" data-paper-title="Mosaic: A Fleet of User Embedding Specialists for Recommendation at Meta" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Mosaic: A Fleet of User Embedding Specialists for Recommendation at Meta 搜广推与 LLM 应用 Meta 2026-07-27 单个通用 user embedding 很难同时覆盖长期记忆、稠密特征、长序列兴趣和特定下游任务。Mosaic 把用户表征组织成可独立演进的 specialist fleet：memorization-driven、dense-heavy、sequential HSTU+MoE 和与下游任务联合训练的 CoTrain。下游排序器按需消费多个 embedding，而不是让一个网络承担所有目标。随着 fleet 增大，新 embedding 容易复制旧 embedding 的信息。 Fidelity: 核心机制复现。实际训练四类 specialist、MRM 复合任务和 cosine redundancy loss；缩小数据、序列长度和 serving 链路。MovieLens genre/popularity 代理 Meta 的多表面私有行为标签；本地 sequential specialist 是 GRU 而非 2048-token HSTU，CoTrain 也缩为小型 routed MoE。未复刻跨产品特征、CoEval、User Tower Zero-Out、AOTI、memcache 和线上混合 CPU/GPU serving，不能把本地 +3.49% 与论文线上 lift 直接比较。  user-embedding multi-task-learning sequential-recommendation mixture-of-experts 搜广推 语义表征、用户知识与冷启动 Mosaic 的 specialist fleet 为什么不等同于扩大一个通用用户向量？ 不同 specialist 分别优化记忆、稠密交互、序列和下游共训，让各自学习互补信息并可独立演进，下游按需消费多个接口。单模型扩宽仍可能被同一目标支配。fleet 也增加存储和维护成本，多个 embedding 不保证信息独立。 示意：记忆专家保留常买品牌，序列专家捕捉本周出游，共训专家适配购买目标；把向量简单加宽未必让这三类知识自然分工。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-mosaic-eb607f0f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8998ade858b0c37d">Mosaic 的 specialist fleet 为什么不等同于扩大一个通用用户向量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amosaic">Mosaic: A Fleet of User Embedding Specialists for Recommendation at Meta</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同 specialist 分别优化记忆、稠密交互、序列和下游共训，让各自学习互补信息并可独立演进，下游按需消费多个接口。单模型扩宽仍可能被同一目标支配。fleet 也增加存储和维护成本，多个 embedding 不保证信息独立。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>记忆专家保留常买品牌，序列专家捕捉本周出游，共训专家适配购买目标；把向量简单加宽未必让这三类知识自然分工。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24015">原论文</a> · <a href="../../../../reproductions/2607.24015-mosaic/">实现解读</a> · <a href="#qa-8998ade858b0c37d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mosaic" data-paper-title="Mosaic: A Fleet of User Embedding Specialists for Recommendation at Meta" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Mosaic: A Fleet of User Embedding Specialists for Recommendation at Meta 搜广推与 LLM 应用 Meta 2026-07-27 单个通用 user embedding 很难同时覆盖长期记忆、稠密特征、长序列兴趣和特定下游任务。Mosaic 把用户表征组织成可独立演进的 specialist fleet：memorization-driven、dense-heavy、sequential HSTU+MoE 和与下游任务联合训练的 CoTrain。下游排序器按需消费多个 embedding，而不是让一个网络承担所有目标。随着 fleet 增大，新 embedding 容易复制旧 embedding 的信息。 Fidelity: 核心机制复现。实际训练四类 specialist、MRM 复合任务和 cosine redundancy loss；缩小数据、序列长度和 serving 链路。MovieLens genre/popularity 代理 Meta 的多表面私有行为标签；本地 sequential specialist 是 GRU 而非 2048-token HSTU，CoTrain 也缩为小型 routed MoE。未复刻跨产品特征、CoEval、User Tower Zero-Out、AOTI、memcache 和线上混合 CPU/GPU serving，不能把本地 +3.49% 与论文线上 lift 直接比较。  user-embedding multi-task-learning sequential-recommendation mixture-of-experts 搜广推 语义表征、用户知识与冷启动 Mosaic 已经有多个专长用户向量，为什么还要对新向量施加去冗余目标？ 新增网络可能再次编码旧向量已有的信息，增加服务开销却不给下游新线索。Mosaic 把不同专长模型组成表征集合，并用任务关系挖掘学习联合行为，再约束新专长与既有表示的冗余。目标是增加互补信息，供下游按需使用；向量更正交只是一种训练约束，不等同于业务信息必然独立。 示意：已有向量擅长记住常买品牌，新模型若也只记品牌就价值有限。让新专长学习跨任务组合并减少重复，可补充“何时愿意探索新品”这类不同线索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-bc7d4916c8920301">Mosaic 已经有多个专长用户向量，为什么还要对新向量施加去冗余目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amosaic">Mosaic: A Fleet of User Embedding Specialists for Recommendation at Meta</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>新增网络可能再次编码旧向量已有的信息，增加服务开销却不给下游新线索。Mosaic 把不同专长模型组成表征集合，并用任务关系挖掘学习联合行为，再约束新专长与既有表示的冗余。目标是增加互补信息，供下游按需使用；向量更正交只是一种训练约束，不等同于业务信息必然独立。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>已有向量擅长记住常买品牌，新模型若也只记品牌就价值有限。让新专长学习跨任务组合并减少重复，可补充“何时愿意探索新品”这类不同线索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24015">原论文</a> · <a href="../../../../reproductions/2607.24015-mosaic/">实现解读</a> · <a href="#qa-bc7d4916c8920301">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mosaic" data-paper-title="Mosaic: A Fleet of User Embedding Specialists for Recommendation at Meta" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Mosaic: A Fleet of User Embedding Specialists for Recommendation at Meta 搜广推与 LLM 应用 Meta 2026-07-27 单个通用 user embedding 很难同时覆盖长期记忆、稠密特征、长序列兴趣和特定下游任务。Mosaic 把用户表征组织成可独立演进的 specialist fleet：memorization-driven、dense-heavy、sequential HSTU+MoE 和与下游任务联合训练的 CoTrain。下游排序器按需消费多个 embedding，而不是让一个网络承担所有目标。随着 fleet 增大，新 embedding 容易复制旧 embedding 的信息。 Fidelity: 核心机制复现。实际训练四类 specialist、MRM 复合任务和 cosine redundancy loss；缩小数据、序列长度和 serving 链路。MovieLens genre/popularity 代理 Meta 的多表面私有行为标签；本地 sequential specialist 是 GRU 而非 2048-token HSTU，CoTrain 也缩为小型 routed MoE。未复刻跨产品特征、CoEval、User Tower Zero-Out、AOTI、memcache 和线上混合 CPU/GPU serving，不能把本地 +3.49% 与论文线上 lift 直接比较。  user-embedding multi-task-learning sequential-recommendation mixture-of-experts 搜广推 语义表征、用户知识与冷启动 Mosaic 的 MRM 联合标签与分别预测每个二元任务，增加什么监督？ 边际标签只约束各事件频率，笛卡尔积标签表示它们一起发生的组合，鼓励 specialist 学依赖结构。相关任务挖掘决定哪些组合值得学，标签空间也会增长。联合信号不等于真实因果关系，相关性高也可能只是曝光共同影响。 示意：点击与长看各半可能同时发生也可能错开，联合组合区分两者；只训练两个独立头无法由边际唯一确定这份关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c49d70463f59f969">Mosaic 的 MRM 联合标签与分别预测每个二元任务，增加什么监督？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amosaic">Mosaic: A Fleet of User Embedding Specialists for Recommendation at Meta</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>边际标签只约束各事件频率，笛卡尔积标签表示它们一起发生的组合，鼓励 specialist 学依赖结构。相关任务挖掘决定哪些组合值得学，标签空间也会增长。联合信号不等于真实因果关系，相关性高也可能只是曝光共同影响。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>点击与长看各半可能同时发生也可能错开，联合组合区分两者；只训练两个独立头无法由边际唯一确定这份关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24015">原论文</a> · <a href="../../../../reproductions/2607.24015-mosaic/">实现解读</a> · <a href="#qa-c49d70463f59f969">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mosaic" data-paper-title="Mosaic: A Fleet of User Embedding Specialists for Recommendation at Meta" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Mosaic: A Fleet of User Embedding Specialists for Recommendation at Meta 搜广推与 LLM 应用 Meta 2026-07-27 单个通用 user embedding 很难同时覆盖长期记忆、稠密特征、长序列兴趣和特定下游任务。Mosaic 把用户表征组织成可独立演进的 specialist fleet：memorization-driven、dense-heavy、sequential HSTU+MoE 和与下游任务联合训练的 CoTrain。下游排序器按需消费多个 embedding，而不是让一个网络承担所有目标。随着 fleet 增大，新 embedding 容易复制旧 embedding 的信息。 Fidelity: 核心机制复现。实际训练四类 specialist、MRM 复合任务和 cosine redundancy loss；缩小数据、序列长度和 serving 链路。MovieLens genre/popularity 代理 Meta 的多表面私有行为标签；本地 sequential specialist 是 GRU 而非 2048-token HSTU，CoTrain 也缩为小型 routed MoE。未复刻跨产品特征、CoEval、User Tower Zero-Out、AOTI、memcache 和线上混合 CPU/GPU serving，不能把本地 +3.49% 与论文线上 lift 直接比较。  user-embedding multi-task-learning sequential-recommendation mixture-of-experts 搜广推 语义表征、用户知识与冷启动 Mosaic 的 cosine redundancy loss 为什么要 warm up，并与实际互补效用分开验收？ 主任务尚未成形时强推不同方向可能只制造随机分离，warm-up 让表示先有任务信息，再逐渐降冗余。余弦降低甚至负值只说明几何变化，不证明增加了可用信息。来源本地 Hit 下降与头部上升必须保留，不能用正交趋势代替质量。 示意：两个随机向量本就可不相关，却都不会推荐；先学有效兴趣再检查新增 specialist 是否补充，才有理由讨论去冗余价值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1753a2d5f97516bd">Mosaic 的 cosine redundancy loss 为什么要 warm up，并与实际互补效用分开验收？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amosaic">Mosaic: A Fleet of User Embedding Specialists for Recommendation at Meta</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>主任务尚未成形时强推不同方向可能只制造随机分离，warm-up 让表示先有任务信息，再逐渐降冗余。余弦降低甚至负值只说明几何变化，不证明增加了可用信息。来源本地 Hit 下降与头部上升必须保留，不能用正交趋势代替质量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个随机向量本就可不相关，却都不会推荐；先学有效兴趣再检查新增 specialist 是否补充，才有理由讨论去冗余价值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24015">原论文</a> · <a href="../../../../reproductions/2607.24015-mosaic/">实现解读</a> · <a href="#qa-1753a2d5f97516bd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dual-sid" data-paper-title="Tokens are All You Need: Dual-purpose Semantic IDs for Achieving LLM-Level I/O Efficiency in Recommendation Systems" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Tokens are All You Need: Dual-purpose Semantic IDs for Achieving LLM-Level I/O Efficiency in Recommendation Systems 搜广推与 LLM 应用 Google DeepMind / YouTube 2026-07-26 传统 SID 擅长表达协同身份，却仍需把大规模内容 embedding 输入推荐模型。论文以层次量化生成 SID，并加入 Semantic Decoder（SiDec）从 SID 重建内容表示，让同一串 token 同时支持生成式检索、排序和低 I/O 的在线 embedding reconstruction。 Fidelity: 核心机制复现。本地训练分层 SID、SID 转移与 Semantic Decoder 内容重建，并用于检索评分。genre 替代 YouTube 多模态内容；未复刻超大 codebook、线上 embedding reconstruction 和私有日志。本地对照口径：基线为同切分的 dense transition-content retrieval，实验组加入 Dual-purpose SID 与 SiDec；NDCG@10 相对 -12.40%。  semantic-id retrieval ranking content-understanding serving 搜广推 语义表征、用户知识与冷启动 Dual-purpose SID 为什么要求短码还能重建内容向量？ 离散码不只服务生成提名，还要为排序提供语义特征。SiDec 从小索引恢复近似内容，减少逐物品存储与传输大向量，同时用重建约束防止只剩协同身份。重建有损，短码不能保存所有原信息，需与质量代价一起衡量。 示意：商品只传三枚码再还原向量，带宽更小；若码没有保留防水属性，公共解码器也无法为这件商品凭空补回该细节。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-dual-sid-924ced9f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-46865ea59a025071">Dual-purpose SID 为什么要求短码还能重建内容向量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adual-sid">Tokens are All You Need: Dual-purpose Semantic IDs for Achieving LLM-Level I/O Efficiency in Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>离散码不只服务生成提名，还要为排序提供语义特征。SiDec 从小索引恢复近似内容，减少逐物品存储与传输大向量，同时用重建约束防止只剩协同身份。重建有损，短码不能保存所有原信息，需与质量代价一起衡量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>商品只传三枚码再还原向量，带宽更小；若码没有保留防水属性，公共解码器也无法为这件商品凭空补回该细节。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24865">原论文</a> · <a href="../../../../reproductions/2607.24865-dual-sid/">实现解读</a> · <a href="#qa-46865ea59a025071">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dual-sid" data-paper-title="Tokens are All You Need: Dual-purpose Semantic IDs for Achieving LLM-Level I/O Efficiency in Recommendation Systems" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Tokens are All You Need: Dual-purpose Semantic IDs for Achieving LLM-Level I/O Efficiency in Recommendation Systems 搜广推与 LLM 应用 Google DeepMind / YouTube 2026-07-26 传统 SID 擅长表达协同身份，却仍需把大规模内容 embedding 输入推荐模型。论文以层次量化生成 SID，并加入 Semantic Decoder（SiDec）从 SID 重建内容表示，让同一串 token 同时支持生成式检索、排序和低 I/O 的在线 embedding reconstruction。 Fidelity: 核心机制复现。本地训练分层 SID、SID 转移与 Semantic Decoder 内容重建，并用于检索评分。genre 替代 YouTube 多模态内容；未复刻超大 codebook、线上 embedding reconstruction 和私有日志。本地对照口径：基线为同切分的 dense transition-content retrieval，实验组加入 Dual-purpose SID 与 SiDec；NDCG@10 相对 -12.40%。  semantic-id retrieval ranking content-understanding serving 搜广推 语义表征、用户知识与冷启动 Dual-purpose SID为什么还要用Semantic Decoder重建内容embedding？ 普通SID适合承载离散身份，却未必能替代下游需要的高维内容输入。SiDec训练从短码恢复内容表示，让同一码同时服务推荐身份与低I/O内容访问，减少反复搬运大向量。重建存在信息瓶颈，短码越省并不一定越好；本地小码本的质量损失说明压缩收益与推荐效果必须分开衡量。 示意：服务端只取三枚短码，再在模型内恢复商品内容向量，可减少外部读取；但若不同用途商品被压成同一码，解码器也无法凭空还原丢失差异。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-1f49a93e9e5190c4">Dual-purpose SID为什么还要用Semantic Decoder重建内容embedding？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adual-sid">Tokens are All You Need: Dual-purpose Semantic IDs for Achieving LLM-Level I/O Efficiency in Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>普通SID适合承载离散身份，却未必能替代下游需要的高维内容输入。SiDec训练从短码恢复内容表示，让同一码同时服务推荐身份与低I/O内容访问，减少反复搬运大向量。重建存在信息瓶颈，短码越省并不一定越好；本地小码本的质量损失说明压缩收益与推荐效果必须分开衡量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>服务端只取三枚短码，再在模型内恢复商品内容向量，可减少外部读取；但若不同用途商品被压成同一码，解码器也无法凭空还原丢失差异。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24865">原论文</a> · <a href="../../../../reproductions/2607.24865-dual-sid/">实现解读</a> · <a href="#qa-1f49a93e9e5190c4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dual-sid" data-paper-title="Tokens are All You Need: Dual-purpose Semantic IDs for Achieving LLM-Level I/O Efficiency in Recommendation Systems" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Tokens are All You Need: Dual-purpose Semantic IDs for Achieving LLM-Level I/O Efficiency in Recommendation Systems 搜广推与 LLM 应用 Google DeepMind / YouTube 2026-07-26 传统 SID 擅长表达协同身份，却仍需把大规模内容 embedding 输入推荐模型。论文以层次量化生成 SID，并加入 Semantic Decoder（SiDec）从 SID 重建内容表示，让同一串 token 同时支持生成式检索、排序和低 I/O 的在线 embedding reconstruction。 Fidelity: 核心机制复现。本地训练分层 SID、SID 转移与 Semantic Decoder 内容重建，并用于检索评分。genre 替代 YouTube 多模态内容；未复刻超大 codebook、线上 embedding reconstruction 和私有日志。本地对照口径：基线为同切分的 dense transition-content retrieval，实验组加入 Dual-purpose SID 与 SiDec；NDCG@10 相对 -12.40%。  semantic-id retrieval ranking content-understanding serving 搜广推 语义表征、用户知识与冷启动 短 SID 加 SiDec 与直接缓存 dense embedding，资源取舍是什么？ 直接缓存保留向量但占存储与 I/O，短码将逐物品负担转成小索引和共享解码参数，增加在线重建计算及近似误差。低 I/O 不必然等于低端到端延迟，来源小码本的检索负结果也不能被重建误差或接口优势掩盖。 示意：百万件商品的大向量可换成短码表，但每次需调用解码矩阵；若计算繁忙或码本太小，整体速度和相关性未必划算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5608c346f04ecf0b">短 SID 加 SiDec 与直接缓存 dense embedding，资源取舍是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adual-sid">Tokens are All You Need: Dual-purpose Semantic IDs for Achieving LLM-Level I/O Efficiency in Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直接缓存保留向量但占存储与 I/O，短码将逐物品负担转成小索引和共享解码参数，增加在线重建计算及近似误差。低 I/O 不必然等于低端到端延迟，来源小码本的检索负结果也不能被重建误差或接口优势掩盖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>百万件商品的大向量可换成短码表，但每次需调用解码矩阵；若计算繁忙或码本太小，整体速度和相关性未必划算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24865">原论文</a> · <a href="../../../../reproductions/2607.24865-dual-sid/">实现解读</a> · <a href="#qa-5608c346f04ecf0b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dual-sid" data-paper-title="Tokens are All You Need: Dual-purpose Semantic IDs for Achieving LLM-Level I/O Efficiency in Recommendation Systems" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Tokens are All You Need: Dual-purpose Semantic IDs for Achieving LLM-Level I/O Efficiency in Recommendation Systems 搜广推与 LLM 应用 Google DeepMind / YouTube 2026-07-26 传统 SID 擅长表达协同身份，却仍需把大规模内容 embedding 输入推荐模型。论文以层次量化生成 SID，并加入 Semantic Decoder（SiDec）从 SID 重建内容表示，让同一串 token 同时支持生成式检索、排序和低 I/O 的在线 embedding reconstruction。 Fidelity: 核心机制复现。本地训练分层 SID、SID 转移与 Semantic Decoder 内容重建，并用于检索评分。genre 替代 YouTube 多模态内容；未复刻超大 codebook、线上 embedding reconstruction 和私有日志。本地对照口径：基线为同切分的 dense transition-content retrieval，实验组加入 Dual-purpose SID 与 SiDec；NDCG@10 相对 -12.40%。  semantic-id retrieval ranking content-understanding serving 搜广推 语义表征、用户知识与冷启动 SiDec 为什么要将每一级 one-hot 分开占列后再拼接？ 同一整数在不同残差层代表不同码字，分层偏移保留其身份，再由解码矩阵输出内容维度。若共用列，层次信息混淆；重建标签需对应同一物品与版本。本地 ridge 解码是明确缩比路径，不能把形状可运行当作全原文训练已完成。 示意：第一层码三与第二层码三是不同输入列；合成一个列会把粗主题与细残差混为一谈，解码器无法知道三来自哪层。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0c88c2829edde23f">SiDec 为什么要将每一级 one-hot 分开占列后再拼接？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adual-sid">Tokens are All You Need: Dual-purpose Semantic IDs for Achieving LLM-Level I/O Efficiency in Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一整数在不同残差层代表不同码字，分层偏移保留其身份，再由解码矩阵输出内容维度。若共用列，层次信息混淆；重建标签需对应同一物品与版本。本地 ridge 解码是明确缩比路径，不能把形状可运行当作全原文训练已完成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第一层码三与第二层码三是不同输入列；合成一个列会把粗主题与细残差混为一谈，解码器无法知道三来自哪层。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24865">原论文</a> · <a href="../../../../reproductions/2607.24865-dual-sid/">实现解读</a> · <a href="#qa-0c88c2829edde23f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pin-scale" data-paper-title="Pin-SCALE: Semantic Cascading and Alignment Learning for Engagement-Aware IDs in Cold-Start Recommendations" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Pin-SCALE: Semantic Cascading and Alignment Learning for Engagement-Aware IDs in Cold-Start Recommendations 搜广推与 LLM 应用 Pinterest 2026-07-19 Semantic ID 擅长冷启动，但在判别式 dense retrieval 中缺乏系统接入方案。Pin-SCALE 保留 residual hierarchy 做 cascading pooling，以 engagement-aware tokenization 引入协同信号，再用 query-item 与 item-item 多视角对比学习对齐 SID 和参与度预测。 Fidelity: 核心机制复现。执行 engagement-aware residual codebook 和 SID 级联相似度。SIGIR program 是当前可核验原始入口；没有伪造 arXiv ID。公开 popularity/transition 仅代理 Pinterest engagement。本地对照口径：基线是 unweighted semantic/content ranker；实验组使用 engagement-weighted 三层 SID，NDCG@10 0.03540→0.04022，相对 +13.61%，fresh Hit@10 相对 +50.00%。  semantic-id engagement-aware generative-retrieval 搜广推 语义表征、用户知识与冷启动 Pin-SCALE 为什么将层级 SID 用在判别式 dense retrieval，而非只做生成？ 粗细码可提供可迁移语义，cascading pooling 将层级信息转成检索表示，参与度与多视角目标让它适应推荐。输出仍可进入判别检索空间，不必逐码生成。SID 是输入知识组织，不意味着所有下游都应采用同种生成解码。 示意：新品有园艺粗码与室内种植细码，聚成向量供双塔匹配；系统可以一次近邻检索，不必先自回归输出两枚码。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-pin-scale-f40ee8a5" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e632fcb5a486d1d0">Pin-SCALE 为什么将层级 SID 用在判别式 dense retrieval，而非只做生成？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apin-scale">Pin-SCALE: Semantic Cascading and Alignment Learning for Engagement-Aware IDs in Cold-Start Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>粗细码可提供可迁移语义，cascading pooling 将层级信息转成检索表示，参与度与多视角目标让它适应推荐。输出仍可进入判别检索空间，不必逐码生成。SID 是输入知识组织，不意味着所有下游都应采用同种生成解码。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新品有园艺粗码与室内种植细码，聚成向量供双塔匹配；系统可以一次近邻检索，不必先自回归输出两枚码。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://sigir2026.org/SIGIR2026_program.pdf">原论文</a> · <a href="../../../../reproductions/sigir2026-pin-scale-pin-scale/">实现解读</a> · <a href="#qa-e632fcb5a486d1d0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pin-scale" data-paper-title="Pin-SCALE: Semantic Cascading and Alignment Learning for Engagement-Aware IDs in Cold-Start Recommendations" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Pin-SCALE: Semantic Cascading and Alignment Learning for Engagement-Aware IDs in Cold-Start Recommendations 搜广推与 LLM 应用 Pinterest 2026-07-19 Semantic ID 擅长冷启动，但在判别式 dense retrieval 中缺乏系统接入方案。Pin-SCALE 保留 residual hierarchy 做 cascading pooling，以 engagement-aware tokenization 引入协同信号，再用 query-item 与 item-item 多视角对比学习对齐 SID 和参与度预测。 Fidelity: 核心机制复现。执行 engagement-aware residual codebook 和 SID 级联相似度。SIGIR program 是当前可核验原始入口；没有伪造 arXiv ID。公开 popularity/transition 仅代理 Pinterest engagement。本地对照口径：基线是 unweighted semantic/content ranker；实验组使用 engagement-weighted 三层 SID，NDCG@10 0.03540→0.04022，相对 +13.61%，fresh Hit@10 相对 +50.00%。  semantic-id engagement-aware generative-retrieval 搜广推 语义表征、用户知识与冷启动 Pin-SCALE 为什么保留 Semantic ID 的残差层级，并加入参与度与多视角对比监督？ 纯语义离散码有利于新物品共享内容知识，却未必对推荐行为最有辨别力。保留残差层级并逐级聚合，可利用粗到细的信息；参与度感知训练和查询—物品、物品—物品对比目标，再把码与推荐相关性连接起来。SID 因而是参与检索训练的表示部件，而不只是把文本向量换成整数标签。 示意：两个“客厅装修”内容语义相近，但服务不同兴趣人群。粗层码保留主题，细层码补充差别；参与度和共现对比使检索表示进一步反映用户实际使用关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-44d732d6513a5be6">Pin-SCALE 为什么保留 Semantic ID 的残差层级，并加入参与度与多视角对比监督？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apin-scale">Pin-SCALE: Semantic Cascading and Alignment Learning for Engagement-Aware IDs in Cold-Start Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>纯语义离散码有利于新物品共享内容知识，却未必对推荐行为最有辨别力。保留残差层级并逐级聚合，可利用粗到细的信息；参与度感知训练和查询—物品、物品—物品对比目标，再把码与推荐相关性连接起来。SID 因而是参与检索训练的表示部件，而不只是把文本向量换成整数标签。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个“客厅装修”内容语义相近，但服务不同兴趣人群。粗层码保留主题，细层码补充差别；参与度和共现对比使检索表示进一步反映用户实际使用关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://sigir2026.org/SIGIR2026_program.pdf">原论文</a> · <a href="../../../../reproductions/sigir2026-pin-scale-pin-scale/">实现解读</a> · <a href="#qa-44d732d6513a5be6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pin-scale" data-paper-title="Pin-SCALE: Semantic Cascading and Alignment Learning for Engagement-Aware IDs in Cold-Start Recommendations" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Pin-SCALE: Semantic Cascading and Alignment Learning for Engagement-Aware IDs in Cold-Start Recommendations 搜广推与 LLM 应用 Pinterest 2026-07-19 Semantic ID 擅长冷启动，但在判别式 dense retrieval 中缺乏系统接入方案。Pin-SCALE 保留 residual hierarchy 做 cascading pooling，以 engagement-aware tokenization 引入协同信号，再用 query-item 与 item-item 多视角对比学习对齐 SID 和参与度预测。 Fidelity: 核心机制复现。执行 engagement-aware residual codebook 和 SID 级联相似度。SIGIR program 是当前可核验原始入口；没有伪造 arXiv ID。公开 popularity/transition 仅代理 Pinterest engagement。本地对照口径：基线是 unweighted semantic/content ranker；实验组使用 engagement-weighted 三层 SID，NDCG@10 0.03540→0.04022，相对 +13.61%，fresh Hit@10 相对 +50.00%。  semantic-id engagement-aware generative-retrieval 搜广推 语义表征、用户知识与冷启动 参与度感知 tokenization 与纯内容重构，为什么优化重心不同？ 纯重构保留内容几何，参与度信号强调影响消费的差异，让语义码更适合推荐而非只还原向量。它也会引入曝光与热门度偏差，需要平衡长尾泛化。来源 fresh 分母小，不能把大相对变化直接视作工业新品收益。 示意：两种装修图片像素相近但用户用途不同，行为目标可强化这份差别；若只看互动量，热门风格也可能压过新内容。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-3f1b52aab5ba2f5b">参与度感知 tokenization 与纯内容重构，为什么优化重心不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apin-scale">Pin-SCALE: Semantic Cascading and Alignment Learning for Engagement-Aware IDs in Cold-Start Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>纯重构保留内容几何，参与度信号强调影响消费的差异，让语义码更适合推荐而非只还原向量。它也会引入曝光与热门度偏差，需要平衡长尾泛化。来源 fresh 分母小，不能把大相对变化直接视作工业新品收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两种装修图片像素相近但用户用途不同，行为目标可强化这份差别；若只看互动量，热门风格也可能压过新内容。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://sigir2026.org/SIGIR2026_program.pdf">原论文</a> · <a href="../../../../reproductions/sigir2026-pin-scale-pin-scale/">实现解读</a> · <a href="#qa-3f1b52aab5ba2f5b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pin-scale" data-paper-title="Pin-SCALE: Semantic Cascading and Alignment Learning for Engagement-Aware IDs in Cold-Start Recommendations" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Pin-SCALE: Semantic Cascading and Alignment Learning for Engagement-Aware IDs in Cold-Start Recommendations 搜广推与 LLM 应用 Pinterest 2026-07-19 Semantic ID 擅长冷启动，但在判别式 dense retrieval 中缺乏系统接入方案。Pin-SCALE 保留 residual hierarchy 做 cascading pooling，以 engagement-aware tokenization 引入协同信号，再用 query-item 与 item-item 多视角对比学习对齐 SID 和参与度预测。 Fidelity: 核心机制复现。执行 engagement-aware residual codebook 和 SID 级联相似度。SIGIR program 是当前可核验原始入口；没有伪造 arXiv ID。公开 popularity/transition 仅代理 Pinterest engagement。本地对照口径：基线是 unweighted semantic/content ranker；实验组使用 engagement-weighted 三层 SID，NDCG@10 0.03540→0.04022，相对 +13.61%，fresh Hit@10 相对 +50.00%。  semantic-id engagement-aware generative-retrieval 搜广推 语义表征、用户知识与冷启动 Pin-SCALE 单个样本同层权重 wi 对最近码选择，为什么不能仅从公式就断言改了 argmin？ 若 wi 是对全部候选码相同的正标量，乘距离不会改变该样本最近中心；作用可能体现于码本学习与全局目标而非这次分配。实现必须检查权重实际施加位置，零权重与候选相关权重又不同，不能靠符号名称补出不存在的变化。 示意：距离二与五同时乘三，最近仍是二；只有中心更新受样本权重影响或各候选系数不同，后续分配才可能改变。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c46a225e046b55e5">Pin-SCALE 单个样本同层权重 wi 对最近码选择，为什么不能仅从公式就断言改了 argmin？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apin-scale">Pin-SCALE: Semantic Cascading and Alignment Learning for Engagement-Aware IDs in Cold-Start Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若 wi 是对全部候选码相同的正标量，乘距离不会改变该样本最近中心；作用可能体现于码本学习与全局目标而非这次分配。实现必须检查权重实际施加位置，零权重与候选相关权重又不同，不能靠符号名称补出不存在的变化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>距离二与五同时乘三，最近仍是二；只有中心更新受样本权重影响或各候选系数不同，后续分配才可能改变。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://sigir2026.org/SIGIR2026_program.pdf">原论文</a> · <a href="../../../../reproductions/sigir2026-pin-scale-pin-scale/">实现解读</a> · <a href="#qa-c46a225e046b55e5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recap" data-paper-title="RECAP: Feedback-Driven Streaming Semantic User Profiles for Short-Video Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RECAP: Feedback-Driven Streaming Semantic User Profiles for Short-Video Recommendation 搜广推与 LLM 应用 Kuaishou Technology / USTC 2026-07-17 传统 LLM 用户画像只追求“总结得像”，没有直接优化未来推荐。RECAP 把画像变成带容量约束的结构化流式状态：LLM 负责语义 update，确定性逻辑负责生命周期、合并与淘汰；再用 LLM judge 筛出标签一致的行为 pair，训练双塔 evaluator，把匹配分数作为 GRPO reward 闭环更新画像生成器。 Fidelity: 核心机制复现。真实训练 causal Transformer updater、双塔评价器和 clipped GRPO，并执行固定容量画像状态机。自然语言画像和工业 LLM 缩为 category-token causal Transformer；没有快手私有日志、生产 LLM judge 和在线闭环。核心 SFT→evaluator→GRPO→bounded state 链路实际执行，但不声称复现线上收益。本地对照口径：基线是 open-loop SFT 流式画像；实验组增加反馈 evaluator 与 GRPO，NDCG@10 相对 -6.77%。  llm-recommendation semantic-profile grpo 搜广推 语义表征、用户知识与冷启动 RECAP 的 LLM judge 与双塔 evaluator 是同一个角色吗？ 不是。LLM judge 用于筛出标签一致的行为 pair，为 evaluator 提供较可靠训练材料；双塔 evaluator 学习画像与行为匹配，并把分数作为画像更新的奖励。前者审数据，后者提供可学习评估接口，二者都可能有误，不能把任一输出当真实用户满意度。 示意：judge 先检查一对行为是否符合标签语义，双塔再学如何给画像匹配打分；让 judge 说一声“不错”不等于已训练出可部署的双塔奖励器。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-recap-84f36c5b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-1e280fb604e68e0c">RECAP 的 LLM judge 与双塔 evaluator 是同一个角色吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecap">RECAP: Feedback-Driven Streaming Semantic User Profiles for Short-Video Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology / USTC</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。LLM judge 用于筛出标签一致的行为 pair，为 evaluator 提供较可靠训练材料；双塔 evaluator 学习画像与行为匹配，并把分数作为画像更新的奖励。前者审数据，后者提供可学习评估接口，二者都可能有误，不能把任一输出当真实用户满意度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>judge 先检查一对行为是否符合标签语义，双塔再学如何给画像匹配打分；让 judge 说一声“不错”不等于已训练出可部署的双塔奖励器。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.15730">原论文</a> · <a href="../../../../reproductions/2607.15730-recap/">实现解读</a> · <a href="#qa-1e280fb604e68e0c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recap" data-paper-title="RECAP: Feedback-Driven Streaming Semantic User Profiles for Short-Video Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RECAP: Feedback-Driven Streaming Semantic User Profiles for Short-Video Recommendation 搜广推与 LLM 应用 Kuaishou Technology / USTC 2026-07-17 传统 LLM 用户画像只追求“总结得像”，没有直接优化未来推荐。RECAP 把画像变成带容量约束的结构化流式状态：LLM 负责语义 update，确定性逻辑负责生命周期、合并与淘汰；再用 LLM judge 筛出标签一致的行为 pair，训练双塔 evaluator，把匹配分数作为 GRPO reward 闭环更新画像生成器。 Fidelity: 核心机制复现。真实训练 causal Transformer updater、双塔评价器和 clipped GRPO，并执行固定容量画像状态机。自然语言画像和工业 LLM 缩为 category-token causal Transformer；没有快手私有日志、生产 LLM judge 和在线闭环。核心 SFT→evaluator→GRPO→bounded state 链路实际执行，但不声称复现线上收益。本地对照口径：基线是 open-loop SFT 流式画像；实验组增加反馈 evaluator 与 GRPO，NDCG@10 相对 -6.77%。  llm-recommendation semantic-profile grpo 搜广推 语义表征、用户知识与冷启动 RECAP 为什么把画像更新拆成 LLM 语义修改和确定性生命周期管理，再用推荐反馈训练？ 语言模型擅长理解新行为，却不适合独自保证容量、合并与淘汰规则。确定性状态机约束画像大小和生命周期，LLM 在其中更新语义；评价器再把画像与后续行为的匹配转成奖励，使训练目标从“摘要像不像”转向“是否有助预测”。奖励仍是代理，需防止评价器偏差被策略放大。 示意：用户从跑步转向骑行，新行为可更新运动偏好，但过期条目由规则淘汰以免画像无限增长。若新画像更能匹配后续骑行行为，反馈再鼓励这种更新方式。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-b85fc63690d9f881">RECAP 为什么把画像更新拆成 LLM 语义修改和确定性生命周期管理，再用推荐反馈训练？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecap">RECAP: Feedback-Driven Streaming Semantic User Profiles for Short-Video Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology / USTC</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语言模型擅长理解新行为，却不适合独自保证容量、合并与淘汰规则。确定性状态机约束画像大小和生命周期，LLM 在其中更新语义；评价器再把画像与后续行为的匹配转成奖励，使训练目标从“摘要像不像”转向“是否有助预测”。奖励仍是代理，需防止评价器偏差被策略放大。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户从跑步转向骑行，新行为可更新运动偏好，但过期条目由规则淘汰以免画像无限增长。若新画像更能匹配后续骑行行为，反馈再鼓励这种更新方式。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.15730">原论文</a> · <a href="../../../../reproductions/2607.15730-recap/">实现解读</a> · <a href="#qa-b85fc63690d9f881">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recap" data-paper-title="RECAP: Feedback-Driven Streaming Semantic User Profiles for Short-Video Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RECAP: Feedback-Driven Streaming Semantic User Profiles for Short-Video Recommendation 搜广推与 LLM 应用 Kuaishou Technology / USTC 2026-07-17 传统 LLM 用户画像只追求“总结得像”，没有直接优化未来推荐。RECAP 把画像变成带容量约束的结构化流式状态：LLM 负责语义 update，确定性逻辑负责生命周期、合并与淘汰；再用 LLM judge 筛出标签一致的行为 pair，训练双塔 evaluator，把匹配分数作为 GRPO reward 闭环更新画像生成器。 Fidelity: 核心机制复现。真实训练 causal Transformer updater、双塔评价器和 clipped GRPO，并执行固定容量画像状态机。自然语言画像和工业 LLM 缩为 category-token causal Transformer；没有快手私有日志、生产 LLM judge 和在线闭环。核心 SFT→evaluator→GRPO→bounded state 链路实际执行，但不声称复现线上收益。本地对照口径：基线是 open-loop SFT 流式画像；实验组增加反馈 evaluator 与 GRPO，NDCG@10 相对 -6.77%。  llm-recommendation semantic-profile grpo 搜广推 语义表征、用户知识与冷启动 RECAP 的闭环 GRPO 与 open-loop SFT，为什么可能 reward 升而 test 排名降？ SFT 模仿更新示例，GRPO 优化 evaluator 的代理偏好；若 evaluator 与真实下一物品不一致，策略会更讨好它而伤泛化。来源确有这种分离，不能只看训练奖励证明画像更好。需要独立评估与参考、格式、多样性约束。 示意：评审喜欢丰富兴趣标签，策略不断增加多样描述，奖励升高，却把用户实际最重要需求稀释；静态文字看着更好不等于推荐更准。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4e8ae9dc0e877508">RECAP 的闭环 GRPO 与 open-loop SFT，为什么可能 reward 升而 test 排名降？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecap">RECAP: Feedback-Driven Streaming Semantic User Profiles for Short-Video Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology / USTC</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>SFT 模仿更新示例，GRPO 优化 evaluator 的代理偏好；若 evaluator 与真实下一物品不一致，策略会更讨好它而伤泛化。来源确有这种分离，不能只看训练奖励证明画像更好。需要独立评估与参考、格式、多样性约束。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>评审喜欢丰富兴趣标签，策略不断增加多样描述，奖励升高，却把用户实际最重要需求稀释；静态文字看着更好不等于推荐更准。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.15730">原论文</a> · <a href="../../../../reproductions/2607.15730-recap/">实现解读</a> · <a href="#qa-4e8ae9dc0e877508">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recap" data-paper-title="RECAP: Feedback-Driven Streaming Semantic User Profiles for Short-Video Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RECAP: Feedback-Driven Streaming Semantic User Profiles for Short-Video Recommendation 搜广推与 LLM 应用 Kuaishou Technology / USTC 2026-07-17 传统 LLM 用户画像只追求“总结得像”，没有直接优化未来推荐。RECAP 把画像变成带容量约束的结构化流式状态：LLM 负责语义 update，确定性逻辑负责生命周期、合并与淘汰；再用 LLM judge 筛出标签一致的行为 pair，训练双塔 evaluator，把匹配分数作为 GRPO reward 闭环更新画像生成器。 Fidelity: 核心机制复现。真实训练 causal Transformer updater、双塔评价器和 clipped GRPO，并执行固定容量画像状态机。自然语言画像和工业 LLM 缩为 category-token causal Transformer；没有快手私有日志、生产 LLM judge 和在线闭环。核心 SFT→evaluator→GRPO→bounded state 链路实际执行，但不声称复现线上收益。本地对照口径：基线是 open-loop SFT 流式画像；实验组增加反馈 evaluator 与 GRPO，NDCG@10 相对 -6.77%。  llm-recommendation semantic-profile grpo 搜广推 语义表征、用户知识与冷启动 RECAP 的容量 |Pt|≤C 应由谁强制，为什么不能只写在 prompt？ 确定性状态机负责条目生命周期、合并与淘汰，LLM 输出再经验证进入状态，prompt 只是意图约束不能保证执行。新状态、证据与 evaluator reward 要绑定同一轮，测试目标不能进入更新。无效格式或超容量应显式处理，不凭后处理掩盖模型错误。 示意：模型返回七项而容量四，应按规则拒绝或合并并记录；若无声截前四再把结果当模型完整遵守，就失去约束可审计性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7a0b55f001b5c722">RECAP 的容量 |Pt|≤C 应由谁强制，为什么不能只写在 prompt？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecap">RECAP: Feedback-Driven Streaming Semantic User Profiles for Short-Video Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology / USTC</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>确定性状态机负责条目生命周期、合并与淘汰，LLM 输出再经验证进入状态，prompt 只是意图约束不能保证执行。新状态、证据与 evaluator reward 要绑定同一轮，测试目标不能进入更新。无效格式或超容量应显式处理，不凭后处理掩盖模型错误。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型返回七项而容量四，应按规则拒绝或合并并记录；若无声截前四再把结果当模型完整遵守，就失去约束可审计性。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.15730">原论文</a> · <a href="../../../../reproductions/2607.15730-recap/">实现解读</a> · <a href="#qa-7a0b55f001b5c722">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:proximity-features" data-paper-title="Proximity Features: Privacy-Compliant Cold-Start Personalization at Airbnb" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Proximity Features: Privacy-Compliant Cold-Start Personalization at Airbnb 搜广推与 LLM 应用 Airbnb 2026-07-14 匿名用户没有 user ID。Airbnb 把 consented geo-IP population-center 坐标聚成约 1,000 用户的 proximity key：密集位置用 IP hash 细分，稀疏位置逐级降低地理精度合并；群体行为按稳定 key 每日聚合，线上无需持久个人标识。 Fidelity: 核心机制复现。dense hash refinement、sparse fine-to-coarse clustering、稳定 proximity key、群体聚合与冷启动 scoring 均实际执行。ZIP prefix 不是 geo-IP 坐标；阈值缩为 12，只验证算法，不构成论文约 1,000 用户的隐私保证。本地对照口径：基线是 global cold-start aggregate；实验组用 MovieLens ZIP 的 adaptive proximity aggregate，验证集选择 blend 1.0，相对基线 Hit@10 +16.67%、NDCG@10 +22.91%。  cold-start privacy features 搜广推 语义表征、用户知识与冷启动 Proximity Features 为什么是群体键而不是匿名个人 ID？ key 将达到人数门槛的地理邻近群体聚合，密处细分稀处合并，线上消费群体行为，不持久追踪每个人。群体信号可帮助冷启动，却无法表达个人精细偏好，也不应把代理 ZIP 实验人数当原生产隐私阈值。 示意：同区域多人近期偏好城市短租，可作为新匿名请求先验；不能说这个键唯一识别其中某人或知道他个人订过什么。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-proximity-features-c055e9e4" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-41229477669023db">Proximity Features 为什么是群体键而不是匿名个人 ID？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aproximity-features">Proximity Features: Privacy-Compliant Cold-Start Personalization at Airbnb</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Airbnb</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>key 将达到人数门槛的地理邻近群体聚合，密处细分稀处合并，线上消费群体行为，不持久追踪每个人。群体信号可帮助冷启动，却无法表达个人精细偏好，也不应把代理 ZIP 实验人数当原生产隐私阈值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同区域多人近期偏好城市短租，可作为新匿名请求先验；不能说这个键唯一识别其中某人或知道他个人订过什么。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12246">原论文</a> · <a href="../../../../reproductions/2607.12246-proximity-features/">实现解读</a> · <a href="#qa-41229477669023db">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:proximity-features" data-paper-title="Proximity Features: Privacy-Compliant Cold-Start Personalization at Airbnb" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Proximity Features: Privacy-Compliant Cold-Start Personalization at Airbnb 搜广推与 LLM 应用 Airbnb 2026-07-14 匿名用户没有 user ID。Airbnb 把 consented geo-IP population-center 坐标聚成约 1,000 用户的 proximity key：密集位置用 IP hash 细分，稀疏位置逐级降低地理精度合并；群体行为按稳定 key 每日聚合，线上无需持久个人标识。 Fidelity: 核心机制复现。dense hash refinement、sparse fine-to-coarse clustering、稳定 proximity key、群体聚合与冷启动 scoring 均实际执行。ZIP prefix 不是 geo-IP 坐标；阈值缩为 12，只验证算法，不构成论文约 1,000 用户的隐私保证。本地对照口径：基线是 global cold-start aggregate；实验组用 MovieLens ZIP 的 adaptive proximity aggregate，验证集选择 blend 1.0，相对基线 Hit@10 +16.67%、NDCG@10 +22.91%。  cold-start privacy features 搜广推 语义表征、用户知识与冷启动 Airbnb 的 proximity key 为什么在密集地区细分、稀疏地区合并，而不使用固定地理网格？ 固定网格在城市可能过大，在稀疏地区又可能只包含极少用户。自适应 key 以人群数量为约束，密集处用哈希进一步拆分，稀疏处降低地理精度合并，使群体特征有足够支持。每日聚合提供匿名冷启动信号，而不是持久识别个人；空间邻近也只是群体偏好的代理，不能等同于个人兴趣。 示意：市中心一小块已有数千人，可再细分；郊区相同面积只有十人，就要扩大区域再聚合。两者都争取形成有足够样本的群体，而不是强行使用同样大小的格子。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-2b212bc7d176d0cc">Airbnb 的 proximity key 为什么在密集地区细分、稀疏地区合并，而不使用固定地理网格？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aproximity-features">Proximity Features: Privacy-Compliant Cold-Start Personalization at Airbnb</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Airbnb</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定网格在城市可能过大，在稀疏地区又可能只包含极少用户。自适应 key 以人群数量为约束，密集处用哈希进一步拆分，稀疏处降低地理精度合并，使群体特征有足够支持。每日聚合提供匿名冷启动信号，而不是持久识别个人；空间邻近也只是群体偏好的代理，不能等同于个人兴趣。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>市中心一小块已有数千人，可再细分；郊区相同面积只有十人，就要扩大区域再聚合。两者都争取形成有足够样本的群体，而不是强行使用同样大小的格子。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12246">原论文</a> · <a href="../../../../reproductions/2607.12246-proximity-features/">实现解读</a> · <a href="#qa-2b212bc7d176d0cc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:proximity-features" data-paper-title="Proximity Features: Privacy-Compliant Cold-Start Personalization at Airbnb" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Proximity Features: Privacy-Compliant Cold-Start Personalization at Airbnb 搜广推与 LLM 应用 Airbnb 2026-07-14 匿名用户没有 user ID。Airbnb 把 consented geo-IP population-center 坐标聚成约 1,000 用户的 proximity key：密集位置用 IP hash 细分，稀疏位置逐级降低地理精度合并；群体行为按稳定 key 每日聚合，线上无需持久个人标识。 Fidelity: 核心机制复现。dense hash refinement、sparse fine-to-coarse clustering、稳定 proximity key、群体聚合与冷启动 scoring 均实际执行。ZIP prefix 不是 geo-IP 坐标；阈值缩为 12，只验证算法，不构成论文约 1,000 用户的隐私保证。本地对照口径：基线是 global cold-start aggregate；实验组用 MovieLens ZIP 的 adaptive proximity aggregate，验证集选择 blend 1.0，相对基线 Hit@10 +16.67%、NDCG@10 +22.91%。  cold-start privacy features 搜广推 语义表征、用户知识与冷启动 Airbnb proximity aggregate 相比 global cold-start aggregate，多加入了什么条件信息？ global 聚合给所有匿名请求同一总体先验，proximity 聚合按人数足够的邻近群体读取统计，允许不同地区有不同需求。它提高局部性，也降低单桶样本量并可能放大地域偏差。来源 ZIP 代理比较检验这一局部信号，不能据此宣称恢复了个人偏好。 示意：整体用户常找热门城市，某邻近群体近期更多周末短途，局部聚合可反映差别；但同桶里准备跨国旅行的人仍可能不符合群体趋势。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d24a218d06f62fb0">Airbnb proximity aggregate 相比 global cold-start aggregate，多加入了什么条件信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aproximity-features">Proximity Features: Privacy-Compliant Cold-Start Personalization at Airbnb</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Airbnb</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>global 聚合给所有匿名请求同一总体先验，proximity 聚合按人数足够的邻近群体读取统计，允许不同地区有不同需求。它提高局部性，也降低单桶样本量并可能放大地域偏差。来源 ZIP 代理比较检验这一局部信号，不能据此宣称恢复了个人偏好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>整体用户常找热门城市，某邻近群体近期更多周末短途，局部聚合可反映差别；但同桶里准备跨国旅行的人仍可能不符合群体趋势。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12246">原论文</a> · <a href="../../../../reproductions/2607.12246-proximity-features/">实现解读</a> · <a href="#qa-d24a218d06f62fb0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:proximity-features" data-paper-title="Proximity Features: Privacy-Compliant Cold-Start Personalization at Airbnb" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Proximity Features: Privacy-Compliant Cold-Start Personalization at Airbnb 搜广推与 LLM 应用 Airbnb 2026-07-14 匿名用户没有 user ID。Airbnb 把 consented geo-IP population-center 坐标聚成约 1,000 用户的 proximity key：密集位置用 IP hash 细分，稀疏位置逐级降低地理精度合并；群体行为按稳定 key 每日聚合，线上无需持久个人标识。 Fidelity: 核心机制复现。dense hash refinement、sparse fine-to-coarse clustering、稳定 proximity key、群体聚合与冷启动 scoring 均实际执行。ZIP prefix 不是 geo-IP 坐标；阈值缩为 12，只验证算法，不构成论文约 1,000 用户的隐私保证。本地对照口径：基线是 global cold-start aggregate；实验组用 MovieLens ZIP 的 adaptive proximity aggregate，验证集选择 blend 1.0，相对基线 Hit@10 +16.67%、NDCG@10 +22.91%。  cold-start privacy features 搜广推 语义表征、用户知识与冷启动 生成 proximity key 为什么要固定坐标量化、hash 和每日聚合版本？ 群体行为按稳定键累积，量化精度或哈希规则变化会让同一区域换桶，历史与线上读错组。应显式处理人数不足与缺坐标，不用个人精确位置暗补。MovieLens 桶规模远小生产约千人，结果只支持代理信号，不证明真实隐私或业务效果。 示意：今天改小数精度却继续读昨天旧键，会将新桶匹配到不相关聚合；稳定命名与版本比把字符串成功 base64 更关键。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-61996e1d79f98663">生成 proximity key 为什么要固定坐标量化、hash 和每日聚合版本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aproximity-features">Proximity Features: Privacy-Compliant Cold-Start Personalization at Airbnb</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Airbnb</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>群体行为按稳定键累积，量化精度或哈希规则变化会让同一区域换桶，历史与线上读错组。应显式处理人数不足与缺坐标，不用个人精确位置暗补。MovieLens 桶规模远小生产约千人，结果只支持代理信号，不证明真实隐私或业务效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>今天改小数精度却继续读昨天旧键，会将新桶匹配到不相关聚合；稳定命名与版本比把字符串成功 base64 更关键。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12246">原论文</a> · <a href="../../../../reproductions/2607.12246-proximity-features/">实现解读</a> · <a href="#qa-61996e1d79f98663">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tokenminds" data-paper-title="TokenMinds: Pretrained User Tokens and Embeddings for User Understanding in Large Recommender Systems" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="TokenMinds: Pretrained User Tokens and Embeddings for User Understanding in Large Recommender Systems 搜广推与 LLM 应用 Google DeepMind / YouTube 2026-06-23 传统工业用户建模把完整兴趣压入少量稠密向量，容易损失细粒度、多峰兴趣；直接让 LLM 输出文本画像又难以与非文本 item ID 和下游排序模型对齐。TokenMinds 将 PLUM 的 item Semantic ID（SID）体系扩展到用户侧：encoder 读取视频 SID、观看特征和搜索文本并输出稠密用户向量，decoder 则自回归生成若干代表未来兴趣的 SID 用户 token。下游同时使用两种表示，从而保留现有 dense feature 兼容性并引入离散、可落到内容语义空间的兴趣表示。 Fidelity: 核心机制复现。本地实际训练共享序列编码器、稠密用户向量、分层 SID 用户 token 预测头及下游融合排序；Google 的 Gemini MoE、YouTube 私有数据和异步生产服务不在本地冒充复刻。本地训练了论文中心的 dual-output 路径，而不是只把配置命名为 TokenMinds。MovieLens genre 取代 YouTube 多模态内容，320 users / 480 items 与 32 条历史取代数十亿用户、1,200 watches 和搜索序列；  llm-recommendation user-modeling semantic-id cross-scenario ranking serving 搜广推 语义表征、用户知识与冷启动 TokenMinds为什么同时输出dense向量与SID用户token？ dense兼容既有排序特征，离散token落在内容语义空间表达多峰未来兴趣，两路共同供下游。它不是让LLM写自由文字画像，也不把用户压成单一SID。 例如保留整体用户向量，同时生成几个代表不同未来兴趣的内容前缀。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-tokenminds-03a3a530" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-846365a6dbcec9e1">TokenMinds为什么同时输出dense向量与SID用户token？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atokenminds">TokenMinds: Pretrained User Tokens and Embeddings for User Understanding in Large Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>dense兼容既有排序特征，离散token落在内容语义空间表达多峰未来兴趣，两路共同供下游。它不是让LLM写自由文字画像，也不把用户压成单一SID。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如保留整体用户向量，同时生成几个代表不同未来兴趣的内容前缀。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.25147">原论文</a> · <a href="../../../../reproductions/2606.25147-tokenminds/">实现解读</a> · <a href="#qa-846365a6dbcec9e1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tokenminds" data-paper-title="TokenMinds: Pretrained User Tokens and Embeddings for User Understanding in Large Recommender Systems" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="TokenMinds: Pretrained User Tokens and Embeddings for User Understanding in Large Recommender Systems 搜广推与 LLM 应用 Google DeepMind / YouTube 2026-06-23 传统工业用户建模把完整兴趣压入少量稠密向量，容易损失细粒度、多峰兴趣；直接让 LLM 输出文本画像又难以与非文本 item ID 和下游排序模型对齐。TokenMinds 将 PLUM 的 item Semantic ID（SID）体系扩展到用户侧：encoder 读取视频 SID、观看特征和搜索文本并输出稠密用户向量，decoder 则自回归生成若干代表未来兴趣的 SID 用户 token。下游同时使用两种表示，从而保留现有 dense feature 兼容性并引入离散、可落到内容语义空间的兴趣表示。 Fidelity: 核心机制复现。本地实际训练共享序列编码器、稠密用户向量、分层 SID 用户 token 预测头及下游融合排序；Google 的 Gemini MoE、YouTube 私有数据和异步生产服务不在本地冒充复刻。本地训练了论文中心的 dual-output 路径，而不是只把配置命名为 TokenMinds。MovieLens genre 取代 YouTube 多模态内容，320 users / 480 items 与 32 条历史取代数十亿用户、1,200 watches 和搜索序列；  llm-recommendation user-modeling semantic-id cross-scenario ranking serving 搜广推 语义表征、用户知识与冷启动 TokenMinds 为什么同时输出稠密用户向量和代表未来兴趣的 SID 用户 token？ 单个稠密向量容易压平多峰兴趣，纯文本画像又难与非文本物品和排序器对接。encoder 保留通用稠密接口，decoder 以物品 SID 空间生成多个未来兴趣前缀，使下游同时获得连续概况与可落到内容空间的离散兴趣。未来窗口采样降低紧邻下一步偏好，但这些目标只用于训练，不能进入在线历史。 示意：用户同时喜欢烘焙和摄影，稠密向量给出总体偏好，两个 SID 前缀分别指向相关内容簇。排序器可同时读取两种表示，而不必从一段模糊文本里再猜商品编码。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-b1cf1ca5c78c492c">TokenMinds 为什么同时输出稠密用户向量和代表未来兴趣的 SID 用户 token？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atokenminds">TokenMinds: Pretrained User Tokens and Embeddings for User Understanding in Large Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单个稠密向量容易压平多峰兴趣，纯文本画像又难与非文本物品和排序器对接。encoder 保留通用稠密接口，decoder 以物品 SID 空间生成多个未来兴趣前缀，使下游同时获得连续概况与可落到内容空间的离散兴趣。未来窗口采样降低紧邻下一步偏好，但这些目标只用于训练，不能进入在线历史。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户同时喜欢烘焙和摄影，稠密向量给出总体偏好，两个 SID 前缀分别指向相关内容簇。排序器可同时读取两种表示，而不必从一段模糊文本里再猜商品编码。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.25147">原论文</a> · <a href="../../../../reproductions/2606.25147-tokenminds/">实现解读</a> · <a href="#qa-b1cf1ca5c78c492c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tokenminds" data-paper-title="TokenMinds: Pretrained User Tokens and Embeddings for User Understanding in Large Recommender Systems" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="TokenMinds: Pretrained User Tokens and Embeddings for User Understanding in Large Recommender Systems 搜广推与 LLM 应用 Google DeepMind / YouTube 2026-06-23 传统工业用户建模把完整兴趣压入少量稠密向量，容易损失细粒度、多峰兴趣；直接让 LLM 输出文本画像又难以与非文本 item ID 和下游排序模型对齐。TokenMinds 将 PLUM 的 item Semantic ID（SID）体系扩展到用户侧：encoder 读取视频 SID、观看特征和搜索文本并输出稠密用户向量，decoder 则自回归生成若干代表未来兴趣的 SID 用户 token。下游同时使用两种表示，从而保留现有 dense feature 兼容性并引入离散、可落到内容语义空间的兴趣表示。 Fidelity: 核心机制复现。本地实际训练共享序列编码器、稠密用户向量、分层 SID 用户 token 预测头及下游融合排序；Google 的 Gemini MoE、YouTube 私有数据和异步生产服务不在本地冒充复刻。本地训练了论文中心的 dual-output 路径，而不是只把配置命名为 TokenMinds。MovieLens genre 取代 YouTube 多模态内容，320 users / 480 items 与 32 条历史取代数十亿用户、1,200 watches 和搜索序列；  llm-recommendation user-modeling semantic-id cross-scenario ranking serving 搜广推 语义表征、用户知识与冷启动 未来24小时多目标与只预测下一次观看有什么差别？ 多目标look-ahead降低紧邻偶然行为的支配，粗SID前缀又强调较广语义。训练可看未来目标作标签，但用户encoder输入仍截止当前，不能把未来行为作为历史。 例如下一条误点不应完全覆盖当天其余稳定兴趣。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e3f9a311830fc3ad">未来24小时多目标与只预测下一次观看有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atokenminds">TokenMinds: Pretrained User Tokens and Embeddings for User Understanding in Large Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多目标look-ahead降低紧邻偶然行为的支配，粗SID前缀又强调较广语义。训练可看未来目标作标签，但用户encoder输入仍截止当前，不能把未来行为作为历史。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如下一条误点不应完全覆盖当天其余稳定兴趣。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.25147">原论文</a> · <a href="../../../../reproductions/2606.25147-tokenminds/">实现解读</a> · <a href="#qa-e3f9a311830fc3ad">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tokenminds" data-paper-title="TokenMinds: Pretrained User Tokens and Embeddings for User Understanding in Large Recommender Systems" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="TokenMinds: Pretrained User Tokens and Embeddings for User Understanding in Large Recommender Systems 搜广推与 LLM 应用 Google DeepMind / YouTube 2026-06-23 传统工业用户建模把完整兴趣压入少量稠密向量，容易损失细粒度、多峰兴趣；直接让 LLM 输出文本画像又难以与非文本 item ID 和下游排序模型对齐。TokenMinds 将 PLUM 的 item Semantic ID（SID）体系扩展到用户侧：encoder 读取视频 SID、观看特征和搜索文本并输出稠密用户向量，decoder 则自回归生成若干代表未来兴趣的 SID 用户 token。下游同时使用两种表示，从而保留现有 dense feature 兼容性并引入离散、可落到内容语义空间的兴趣表示。 Fidelity: 核心机制复现。本地实际训练共享序列编码器、稠密用户向量、分层 SID 用户 token 预测头及下游融合排序；Google 的 Gemini MoE、YouTube 私有数据和异步生产服务不在本地冒充复刻。本地训练了论文中心的 dual-output 路径，而不是只把配置命名为 TokenMinds。MovieLens genre 取代 YouTube 多模态内容，320 users / 480 items 与 32 条历史取代数十亿用户、1,200 watches 和搜索序列；  llm-recommendation user-modeling semantic-id cross-scenario ranking serving 搜广推 语义表征、用户知识与冷启动 本地TokenMinds是否执行了完整生产multi-context decoding？ 没有，小GRU加SID heads只保留dual-output中心路径，未复刻Gemini规模、15目标、40beam或KV刷新服务。不能把双输出跑通说成场景共享prefill全部实现。 例如同时有dense和码输出，不代表已支持多场景并行生成及百万读缓存。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1834c322e1c99368">本地TokenMinds是否执行了完整生产multi-context decoding？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atokenminds">TokenMinds: Pretrained User Tokens and Embeddings for User Understanding in Large Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有，小GRU加SID heads只保留dual-output中心路径，未复刻Gemini规模、15目标、40beam或KV刷新服务。不能把双输出跑通说成场景共享prefill全部实现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同时有dense和码输出，不代表已支持多场景并行生成及百万读缓存。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.25147">原论文</a> · <a href="../../../../reproductions/2606.25147-tokenminds/">实现解读</a> · <a href="#qa-1834c322e1c99368">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:g2rec" data-paper-title="Structuring and Tokenizing Distributed User Interest Context for Generative Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Structuring and Tokenizing Distributed User Interest Context for Generative Recommendation 搜广推与 LLM 应用 Meta 2026-06-18 生成式推荐把 item 当 token，但纯 item 序列难以表达一个物品跨多个兴趣簇的语义，也难以利用分散在不同用户行为中的共现结构。G2Rec 从全站 co-engagement 构造 item-item 图，以可微 soft modularity 学习一个 item 对多个 interest prototype 的软归属，再把 item token 与其 interest-profile token 交替输入生成模型，并增加 profile prediction loss。 Fidelity: 完整核心链路复现。当前代码实际优化稀疏图 soft modularity，并训练交替 item/continuous-interest token 的自回归 Transformer、next-item loss 与 profile loss。本地对照口径：基线是参数级别匹配的 Item-only Autoregressive Decoder；实验组是 G2Rec Item+Interest Decoder；NDCG@10 从 0.0474 升至 0.0530（+11.92%）。这是 interest-token 组织与辅助目标的联合消融，不是相对 DIN。   搜广推 语义表征、用户知识与冷启动 G2Rec 为什么在 item token 之间插入 interest-profile token？ 物品身份记忆具体对象，interest profile 将全站共参与图里的软兴趣关系显式接入序列，帮助模型连接分散在不同用户的结构。一个物品可属于多兴趣，交替输入让两类信息共同参与生成。profile 不是额外真实行为，不能把序列加长误读为用户消费了更多物品。 示意：一本摄影旅行书同时连接摄影与旅行簇，在书 token 后插入混合兴趣表示，下一步可利用两类关联而非只能记该书编号。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-g2rec-310e6cb6" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-32417801d1e00372">G2Rec 为什么在 item token 之间插入 interest-profile token？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ag2rec">Structuring and Tokenizing Distributed User Interest Context for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>物品身份记忆具体对象，interest profile 将全站共参与图里的软兴趣关系显式接入序列，帮助模型连接分散在不同用户的结构。一个物品可属于多兴趣，交替输入让两类信息共同参与生成。profile 不是额外真实行为，不能把序列加长误读为用户消费了更多物品。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一本摄影旅行书同时连接摄影与旅行簇，在书 token 后插入混合兴趣表示，下一步可利用两类关联而非只能记该书编号。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.20554">原论文</a> · <a href="../../../../reproductions/2606.20554-g2rec/">实现解读</a> · <a href="#qa-32417801d1e00372">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:g2rec" data-paper-title="Structuring and Tokenizing Distributed User Interest Context for Generative Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Structuring and Tokenizing Distributed User Interest Context for Generative Recommendation 搜广推与 LLM 应用 Meta 2026-06-18 生成式推荐把 item 当 token，但纯 item 序列难以表达一个物品跨多个兴趣簇的语义，也难以利用分散在不同用户行为中的共现结构。G2Rec 从全站 co-engagement 构造 item-item 图，以可微 soft modularity 学习一个 item 对多个 interest prototype 的软归属，再把 item token 与其 interest-profile token 交替输入生成模型，并增加 profile prediction loss。 Fidelity: 完整核心链路复现。当前代码实际优化稀疏图 soft modularity，并训练交替 item/continuous-interest token 的自回归 Transformer、next-item loss 与 profile loss。本地对照口径：基线是参数级别匹配的 Item-only Autoregressive Decoder；实验组是 G2Rec Item+Interest Decoder；NDCG@10 从 0.0474 升至 0.0530（+11.92%）。这是 interest-token 组织与辅助目标的联合消融，不是相对 DIN。   搜广推 语义表征、用户知识与冷启动 G2Rec为什么允许一个item软归属多个兴趣prototype？ 同一内容可被不同兴趣群体共同消费，硬分到单簇会抹掉跨兴趣联系。G2Rec利用全站共参与图学习软归属，再把由prototype组合成的兴趣token与item交替输入生成器，补充单个ID看不到的分布式上下文。图构造只能使用可见训练行为，否则兴趣结构本身也会泄漏测试关系。 示意：一段露营做饭视频同时属于户外与烹饪，两个软归属能影响后续预测；硬塞进单一标签会让模型难以解释另一群用户为什么也会喜欢它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-262f93f892309abd">G2Rec为什么允许一个item软归属多个兴趣prototype？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ag2rec">Structuring and Tokenizing Distributed User Interest Context for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一内容可被不同兴趣群体共同消费，硬分到单簇会抹掉跨兴趣联系。G2Rec利用全站共参与图学习软归属，再把由prototype组合成的兴趣token与item交替输入生成器，补充单个ID看不到的分布式上下文。图构造只能使用可见训练行为，否则兴趣结构本身也会泄漏测试关系。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一段露营做饭视频同时属于户外与烹饪，两个软归属能影响后续预测；硬塞进单一标签会让模型难以解释另一群用户为什么也会喜欢它。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.20554">原论文</a> · <a href="../../../../reproductions/2606.20554-g2rec/">实现解读</a> · <a href="#qa-262f93f892309abd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:g2rec" data-paper-title="Structuring and Tokenizing Distributed User Interest Context for Generative Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Structuring and Tokenizing Distributed User Interest Context for Generative Recommendation 搜广推与 LLM 应用 Meta 2026-06-18 生成式推荐把 item 当 token，但纯 item 序列难以表达一个物品跨多个兴趣簇的语义，也难以利用分散在不同用户行为中的共现结构。G2Rec 从全站 co-engagement 构造 item-item 图，以可微 soft modularity 学习一个 item 对多个 interest prototype 的软归属，再把 item token 与其 interest-profile token 交替输入生成模型，并增加 profile prediction loss。 Fidelity: 完整核心链路复现。当前代码实际优化稀疏图 soft modularity，并训练交替 item/continuous-interest token 的自回归 Transformer、next-item loss 与 profile loss。本地对照口径：基线是参数级别匹配的 Item-only Autoregressive Decoder；实验组是 G2Rec Item+Interest Decoder；NDCG@10 从 0.0474 升至 0.0530（+11.92%）。这是 interest-token 组织与辅助目标的联合消融，不是相对 DIN。   搜广推 语义表征、用户知识与冷启动 G2Rec 的 soft modularity 与按固定品类分桶，相比如何形成兴趣群？ 固定品类由外部 taxonomy 决定，soft modularity 根据共参与图优化软归属，允许一个物品跨群并扣除度数背景影响。它学习的是图社区结构，未必等同人类品类，也会受曝光图影响。图结构好不自动代表序列推荐提升。 示意：相机和旅行背包可能在同群，虽然商品品类不同；一本书又可部分属于另一群，软归属不强迫它只选一个目录。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-54e73b36a95c0b86">G2Rec 的 soft modularity 与按固定品类分桶，相比如何形成兴趣群？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ag2rec">Structuring and Tokenizing Distributed User Interest Context for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定品类由外部 taxonomy 决定，soft modularity 根据共参与图优化软归属，允许一个物品跨群并扣除度数背景影响。它学习的是图社区结构，未必等同人类品类，也会受曝光图影响。图结构好不自动代表序列推荐提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>相机和旅行背包可能在同群，虽然商品品类不同；一本书又可部分属于另一群，软归属不强迫它只选一个目录。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.20554">原论文</a> · <a href="../../../../reproductions/2606.20554-g2rec/">实现解读</a> · <a href="#qa-54e73b36a95c0b86">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:g2rec" data-paper-title="Structuring and Tokenizing Distributed User Interest Context for Generative Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Structuring and Tokenizing Distributed User Interest Context for Generative Recommendation 搜广推与 LLM 应用 Meta 2026-06-18 生成式推荐把 item 当 token，但纯 item 序列难以表达一个物品跨多个兴趣簇的语义，也难以利用分散在不同用户行为中的共现结构。G2Rec 从全站 co-engagement 构造 item-item 图，以可微 soft modularity 学习一个 item 对多个 interest prototype 的软归属，再把 item token 与其 interest-profile token 交替输入生成模型，并增加 profile prediction loss。 Fidelity: 完整核心链路复现。当前代码实际优化稀疏图 soft modularity，并训练交替 item/continuous-interest token 的自回归 Transformer、next-item loss 与 profile loss。本地对照口径：基线是参数级别匹配的 Item-only Autoregressive Decoder；实验组是 G2Rec Item+Interest Decoder；NDCG@10 从 0.0474 升至 0.0530（+11.92%）。这是 interest-token 组织与辅助目标的联合消融，不是相对 DIN。   搜广推 语义表征、用户知识与冷启动 G2Rec 的 prototype 加权均值和交替序列，哪些边界需要检查？ 每个 prototype 按物品软归属加权并除总权重，空或近空簇分母需明确处理；item 与 profile 的位置和因果 mask 要对齐，辅助目标不能读未来 item。来源本地是一正加九十九负评估，不能把该结果称为全库排名收益。 示意：物品甲后应接甲的 profile，错位接乙会泄漏或误教关系；即使 loss 正常下降，位置对不上也不代表实现了论文序列。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d0bb6b1185f0a09e">G2Rec 的 prototype 加权均值和交替序列，哪些边界需要检查？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ag2rec">Structuring and Tokenizing Distributed User Interest Context for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每个 prototype 按物品软归属加权并除总权重，空或近空簇分母需明确处理；item 与 profile 的位置和因果 mask 要对齐，辅助目标不能读未来 item。来源本地是一正加九十九负评估，不能把该结果称为全库排名收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>物品甲后应接甲的 profile，错位接乙会泄漏或误教关系；即使 loss 正常下降，位置对不上也不代表实现了论文序列。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.20554">原论文</a> · <a href="../../../../reproductions/2606.20554-g2rec/">实现解读</a> · <a href="#qa-d0bb6b1185f0a09e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:atomic-intent" data-paper-title="Atomic Intent Reasoning: Bringing LLM Semantics to Industrial Cross-Domain Recommendations" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Atomic Intent Reasoning: Bringing LLM Semantics to Industrial Cross-Domain Recommendations 搜广推与 LLM 应用 The Hong Kong Polytechnic University 2026-06-09 将昂贵的 LLM 推理移至离线，把单次行为转成可缓存的层级原子意图；在线按目标商品检索意图链，并用多头注意力聚合跨域证据。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05240，相对变化 -2.98%。本地代理目标与论文生产任务不同，不能外推线上 lift。  cross-domain llm-recommendation intent-retrieval 搜广推 语义表征、用户知识与冷启动 Atomic Intent 为什么把单次行为拆成层级意图，而不只给它一个宽泛品类标签？ 宽泛类别保留“看了什么”，层级原子意图还尝试表达用途和需求结构，方便跨域行为在共享意图上连接。离线生成后保留细粒度可缓存单位，在线目标商品再检索相关链条。语义解释仍可能出错，不能把模型推断意图当作用户明确声明。 示意：浏览相机既可能为了旅行轻便，也可能为了棚拍画质。都写“摄影”会混在一起，细分意图后才能给轻便背包或专业灯具提供不同证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-atomic-intent-04e8fc99" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-39f0b65e8c995c63">Atomic Intent 为什么把单次行为拆成层级意图，而不只给它一个宽泛品类标签？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aatomic-intent">Atomic Intent Reasoning: Bringing LLM Semantics to Industrial Cross-Domain Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hong Kong Polytechnic University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>宽泛类别保留“看了什么”，层级原子意图还尝试表达用途和需求结构，方便跨域行为在共享意图上连接。离线生成后保留细粒度可缓存单位，在线目标商品再检索相关链条。语义解释仍可能出错，不能把模型推断意图当作用户明确声明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>浏览相机既可能为了旅行轻便，也可能为了棚拍画质。都写“摄影”会混在一起，细分意图后才能给轻便背包或专业灯具提供不同证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.10357">原论文</a> · <a href="../../../../reproductions/2606.10357-atomic-intent/">实现解读</a> · <a href="#qa-39f0b65e8c995c63">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:atomic-intent" data-paper-title="Atomic Intent Reasoning: Bringing LLM Semantics to Industrial Cross-Domain Recommendations" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Atomic Intent Reasoning: Bringing LLM Semantics to Industrial Cross-Domain Recommendations 搜广推与 LLM 应用 The Hong Kong Polytechnic University 2026-06-09 将昂贵的 LLM 推理移至离线，把单次行为转成可缓存的层级原子意图；在线按目标商品检索意图链，并用多头注意力聚合跨域证据。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05240，相对变化 -2.98%。本地代理目标与论文生产任务不同，不能外推线上 lift。  cross-domain llm-recommendation intent-retrieval 搜广推 语义表征、用户知识与冷启动 把跨域行为先变成原子意图并缓存，为什么不等同于直接缓存一个用户向量？ 原子意图保留可检索的层级证据，在线还能按目标商品选择相关意图链，而一个固定用户向量往往已把不同需求揉在一起。昂贵推理离线完成，候选条件化检索与聚合在线执行，兼顾复用和针对性。本地代理评分没有验证完整LLM意图生成链路，不能由其指标推断线上推理质量。 示意：一次观看可以留下户外、露营、轻便装备等层级意图；推荐帐篷时取露营链，推荐通勤包时取轻便需求，而不必重跑整段LLM历史推理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-bc84ca215cad39e2">把跨域行为先变成原子意图并缓存，为什么不等同于直接缓存一个用户向量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aatomic-intent">Atomic Intent Reasoning: Bringing LLM Semantics to Industrial Cross-Domain Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hong Kong Polytechnic University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原子意图保留可检索的层级证据，在线还能按目标商品选择相关意图链，而一个固定用户向量往往已把不同需求揉在一起。昂贵推理离线完成，候选条件化检索与聚合在线执行，兼顾复用和针对性。本地代理评分没有验证完整LLM意图生成链路，不能由其指标推断线上推理质量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次观看可以留下户外、露营、轻便装备等层级意图；推荐帐篷时取露营链，推荐通勤包时取轻便需求，而不必重跑整段LLM历史推理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.10357">原论文</a> · <a href="../../../../reproductions/2606.10357-atomic-intent/">实现解读</a> · <a href="#qa-bc84ca215cad39e2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:atomic-intent" data-paper-title="Atomic Intent Reasoning: Bringing LLM Semantics to Industrial Cross-Domain Recommendations" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Atomic Intent Reasoning: Bringing LLM Semantics to Industrial Cross-Domain Recommendations 搜广推与 LLM 应用 The Hong Kong Polytechnic University 2026-06-09 将昂贵的 LLM 推理移至离线，把单次行为转成可缓存的层级原子意图；在线按目标商品检索意图链，并用多头注意力聚合跨域证据。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05240，相对变化 -2.98%。本地代理目标与论文生产任务不同，不能外推线上 lift。  cross-domain llm-recommendation intent-retrieval 搜广推 语义表征、用户知识与冷启动 Atomic Intent 的目标条件检索与一次性生成静态文本画像，有什么更新与使用差别？ 静态画像将多种需求压进一段固定摘要，每次候选只能读取同一份概况；原子链保留可索引片段，新增行为可增量补充，候选按需取不同证据。代价是离线解析、存储和检索维护，若索引漏取关键意图，下游聚合也无法恢复。 示意：鞋候选检索运动需求，相机候选检索旅行拍摄需求；固定画像若只剩“爱户外”，两种候选难以获得各自具体的历史理由。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a4a523cd28e8acb5">Atomic Intent 的目标条件检索与一次性生成静态文本画像，有什么更新与使用差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aatomic-intent">Atomic Intent Reasoning: Bringing LLM Semantics to Industrial Cross-Domain Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hong Kong Polytechnic University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>静态画像将多种需求压进一段固定摘要，每次候选只能读取同一份概况；原子链保留可索引片段，新增行为可增量补充，候选按需取不同证据。代价是离线解析、存储和检索维护，若索引漏取关键意图，下游聚合也无法恢复。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>鞋候选检索运动需求，相机候选检索旅行拍摄需求；固定画像若只剩“爱户外”，两种候选难以获得各自具体的历史理由。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.10357">原论文</a> · <a href="../../../../reproductions/2606.10357-atomic-intent/">实现解读</a> · <a href="#qa-a4a523cd28e8acb5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:atomic-intent" data-paper-title="Atomic Intent Reasoning: Bringing LLM Semantics to Industrial Cross-Domain Recommendations" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Atomic Intent Reasoning: Bringing LLM Semantics to Industrial Cross-Domain Recommendations 搜广推与 LLM 应用 The Hong Kong Polytechnic University 2026-06-09 将昂贵的 LLM 推理移至离线，把单次行为转成可缓存的层级原子意图；在线按目标商品检索意图链，并用多头注意力聚合跨域证据。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05240，相对变化 -2.98%。本地代理目标与论文生产任务不同，不能外推线上 lift。  cross-domain llm-recommendation intent-retrieval 搜广推 语义表征、用户知识与冷启动 实现 Atomic Intent 的时间与频率权重时，为什么要把意图提取和在线聚合分别验收？ 频次对数与时间衰减只是证据加权，不能替代离线语言模型实际提取层级意图；相似度检索和多头聚合也应使用已缓存链条。若本地只有确定性代理分数，应明确其范围，不能因公式可执行就声称完成原文大模型解析。 示意：把十次浏览按时间加权能够生成一个数，却没有自动解释“旅行轻量化”意图；先检查缓存内容，再检查在线如何选择，才能定位两层误差。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-fa74ccdb0259971a">实现 Atomic Intent 的时间与频率权重时，为什么要把意图提取和在线聚合分别验收？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aatomic-intent">Atomic Intent Reasoning: Bringing LLM Semantics to Industrial Cross-Domain Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hong Kong Polytechnic University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>频次对数与时间衰减只是证据加权，不能替代离线语言模型实际提取层级意图；相似度检索和多头聚合也应使用已缓存链条。若本地只有确定性代理分数，应明确其范围，不能因公式可执行就声称完成原文大模型解析。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把十次浏览按时间加权能够生成一个数，却没有自动解释“旅行轻量化”意图；先检查缓存内容，再检查在线如何选择，才能定位两层误差。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.10357">原论文</a> · <a href="../../../../reproductions/2606.10357-atomic-intent/">实现解读</a> · <a href="#qa-fa74ccdb0259971a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ssrlive" data-paper-title="SSRLive: Live Streaming Recommendation with Dynamic Semantic ID" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SSRLive: Live Streaming Recommendation with Dynamic Semantic ID 搜广推与 LLM 应用 Taobao &amp; Tmall Group, Alibaba 2026-06-05 用静态语义 ID 表达主播长期内容，用动态语义 ID 捕获实时直播状态，再融合用户—主播交互特征完成观看、交易与互动多任务预测。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05351，相对变化 -0.92%。本地代理目标与论文生产任务不同，不能外推线上 lift。  live-streaming semantic-id multitask-ranking 搜广推 语义表征、用户知识与冷启动 SSRLive为什么分静态与动态语义ID？ 主播长期风格与当前直播内容变化速度不同，一套固定码难同时表达。两种码和用户主播交互融合，支持观看交易互动等多任务，仍需实时内容更新可靠。 例如主播通常讲数码，但此刻在户外旅行，长期与当前语义应可区分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-ssrlive-efb93285" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e818177365a5cf26">SSRLive为什么分静态与动态语义ID？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Assrlive">SSRLive: Live Streaming Recommendation with Dynamic Semantic ID</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group, Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>主播长期风格与当前直播内容变化速度不同，一套固定码难同时表达。两种码和用户主播交互融合，支持观看交易互动等多任务，仍需实时内容更新可靠。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如主播通常讲数码，但此刻在户外旅行，长期与当前语义应可区分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.06970">原论文</a> · <a href="../../../../reproductions/2606.06970-ssrlive/">实现解读</a> · <a href="#qa-e818177365a5cf26">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ssrlive" data-paper-title="SSRLive: Live Streaming Recommendation with Dynamic Semantic ID" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SSRLive: Live Streaming Recommendation with Dynamic Semantic ID 搜广推与 LLM 应用 Taobao &amp; Tmall Group, Alibaba 2026-06-05 用静态语义 ID 表达主播长期内容，用动态语义 ID 捕获实时直播状态，再融合用户—主播交互特征完成观看、交易与互动多任务预测。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05351，相对变化 -0.92%。本地代理目标与论文生产任务不同，不能外推线上 lift。  live-streaming semantic-id multitask-ranking 搜广推 语义表征、用户知识与冷启动 SSRLive 为什么同时保留主播静态 SID 与直播动态 SID，而不持续覆盖同一份语义码？ 静态 SID 表达主播长期内容，动态 SID 描述当前直播状态，两者时间尺度不同。分开保留能让模型区分稳定定位与临时变化，再结合用户—主播互动做多任务预测；若只覆盖同一份码，短期话题可能抹去长期信息，旧状态也易误当实况。动态码仍受提取与更新延迟限制，不能保证实时完全准确。 示意：主播长期做美妆，今天临时讲旅行收纳。静态码保留美妆受众基础，动态码说明当前主题，让模型决定此刻更适合推给哪类用户，而不是永久改写主播身份。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-57f100938c149e13">SSRLive 为什么同时保留主播静态 SID 与直播动态 SID，而不持续覆盖同一份语义码？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Assrlive">SSRLive: Live Streaming Recommendation with Dynamic Semantic ID</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group, Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>静态 SID 表达主播长期内容，动态 SID 描述当前直播状态，两者时间尺度不同。分开保留能让模型区分稳定定位与临时变化，再结合用户—主播互动做多任务预测；若只覆盖同一份码，短期话题可能抹去长期信息，旧状态也易误当实况。动态码仍受提取与更新延迟限制，不能保证实时完全准确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>主播长期做美妆，今天临时讲旅行收纳。静态码保留美妆受众基础，动态码说明当前主题，让模型决定此刻更适合推给哪类用户，而不是永久改写主播身份。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.06970">原论文</a> · <a href="../../../../reproductions/2606.06970-ssrlive/">实现解读</a> · <a href="#qa-57f100938c149e13">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ssrlive" data-paper-title="SSRLive: Live Streaming Recommendation with Dynamic Semantic ID" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SSRLive: Live Streaming Recommendation with Dynamic Semantic ID 搜广推与 LLM 应用 Taobao &amp; Tmall Group, Alibaba 2026-06-05 用静态语义 ID 表达主播长期内容，用动态语义 ID 捕获实时直播状态，再融合用户—主播交互特征完成观看、交易与互动多任务预测。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05351，相对变化 -0.92%。本地代理目标与论文生产任务不同，不能外推线上 lift。  live-streaming semantic-id multitask-ranking 搜广推 语义表征、用户知识与冷启动 动态SID与给静态embedding简单加时间戳有什么差别？ 动态码旨在表达内容状态变化，时间戳只表示时刻，不必包含具体内容。若没有真实状态生成，不能因多一列时间就声称完成动态语义建模。 例如知道晚上八点，不等于知道直播正在演示哪款商品。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-8142e4c5acb949a1">动态SID与给静态embedding简单加时间戳有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Assrlive">SSRLive: Live Streaming Recommendation with Dynamic Semantic ID</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group, Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>动态码旨在表达内容状态变化，时间戳只表示时刻，不必包含具体内容。若没有真实状态生成，不能因多一列时间就声称完成动态语义建模。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如知道晚上八点，不等于知道直播正在演示哪款商品。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.06970">原论文</a> · <a href="../../../../reproductions/2606.06970-ssrlive/">实现解读</a> · <a href="#qa-8142e4c5acb949a1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ssrlive" data-paper-title="SSRLive: Live Streaming Recommendation with Dynamic Semantic ID" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SSRLive: Live Streaming Recommendation with Dynamic Semantic ID 搜广推与 LLM 应用 Taobao &amp; Tmall Group, Alibaba 2026-06-05 用静态语义 ID 表达主播长期内容，用动态语义 ID 捕获实时直播状态，再融合用户—主播交互特征完成观看、交易与互动多任务预测。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05351，相对变化 -0.92%。本地代理目标与论文生产任务不同，不能外推线上 lift。  live-streaming semantic-id multitask-ranking 搜广推 语义表征、用户知识与冷启动 SSRLive本地MovieLens能支持哪些结论？ 只验证静动态表示与交互的中心计算，缺少真实直播帧、交易与多任务生产日志。各任务标签和时间快照需隔离，不能用目标结果反推当前动态ID。 例如把下一次评分塞进动态特征，会提前泄露待预测行为。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a690900cba37e414">SSRLive本地MovieLens能支持哪些结论？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Assrlive">SSRLive: Live Streaming Recommendation with Dynamic Semantic ID</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group, Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只验证静动态表示与交互的中心计算，缺少真实直播帧、交易与多任务生产日志。各任务标签和时间快照需隔离，不能用目标结果反推当前动态ID。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把下一次评分塞进动态特征，会提前泄露待预测行为。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.06970">原论文</a> · <a href="../../../../reproductions/2606.06970-ssrlive/">实现解读</a> · <a href="#qa-a690900cba37e414">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pinterest-ads-llm" data-paper-title="Fine-Tuned LLM as a Complementary Predictor Improving Ads System" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Fine-Tuned LLM as a Complementary Predictor Improving Ads System 搜广推与 LLM 应用 Pinterest 2026-05-27 论文没有让 LLM 替换广告召回或排序，而是把它作为 ancillary predictor：输入用户画像、历史转化、搜索、URL、品类和品牌，预测下一批高转化意图 advertiser 与兴趣。预测结果一方面成为 advertiser 定向的补充召回通道，另一方面作为 ctcvr/vtcvr 特征进入后续排序。训练分三层：先用单一 next-advertiser 标签做 SFT；再用 GRPO 生成 20 个 advertiser 与 5 个兴趣，并用命中位置和严格输出长度计算 reward； 未运行 Pinterest 私有 PinCLIP SID 三阶段 CPT，也不声称本地 AUC/Recall 可外推 RoAS。Fidelity: 完整核心链路。本地实际执行开源 causal LLM 的 LoRA SFT、论文位置/格式 reward 驱动的 clipped GRPO、受约束 advertiser 解码、训练式 two-tower、validation 配额选择的补充召回，以及 LLM advertiser score 作为排序特征。Pinterest 私有广告与跨站转化数据由公开商品品牌和购买序列替换。使用真实预训练语言模型和可训练 LoRA，不是规则或 embedding 打分替代 SFT/GRPO。  advertising llm-sft grpo candidate-generation 搜广推 语义表征、用户知识与冷启动 Pinterest Ads LLM 同时输出 advertiser 与兴趣，这两个粒度是不是一一对应？ 不是。advertiser 指向具体广告主，兴趣概括用户可能关心的主题，多个广告主可服务同一兴趣，一个广告主也可覆盖多种主题。两类输出能提供不同召回与特征线索，不能将兴趣名称直接当广告主 ID，更不能把任一预测当成已经发生的转化。 示意：露营兴趣可关联多个户外广告主，同一百货广告主又覆盖露营与家居；把“露营”替换成某一家品牌，会无端缩小可用候选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-pinterest-ads-llm-d99be125" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7200a906a9dc8325">Pinterest Ads LLM 同时输出 advertiser 与兴趣，这两个粒度是不是一一对应？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apinterest-ads-llm">Fine-Tuned LLM as a Complementary Predictor Improving Ads System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。advertiser 指向具体广告主，兴趣概括用户可能关心的主题，多个广告主可服务同一兴趣，一个广告主也可覆盖多种主题。两类输出能提供不同召回与特征线索，不能将兴趣名称直接当广告主 ID，更不能把任一预测当成已经发生的转化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>露营兴趣可关联多个户外广告主，同一百货广告主又覆盖露营与家居；把“露营”替换成某一家品牌，会无端缩小可用候选。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.27856">原论文</a> · <a href="../../../../reproductions/2605.27856-pinterest-ads-llm/">实现解读</a> · <a href="#qa-7200a906a9dc8325">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pinterest-ads-llm" data-paper-title="Fine-Tuned LLM as a Complementary Predictor Improving Ads System" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Fine-Tuned LLM as a Complementary Predictor Improving Ads System 搜广推与 LLM 应用 Pinterest 2026-05-27 论文没有让 LLM 替换广告召回或排序，而是把它作为 ancillary predictor：输入用户画像、历史转化、搜索、URL、品类和品牌，预测下一批高转化意图 advertiser 与兴趣。预测结果一方面成为 advertiser 定向的补充召回通道，另一方面作为 ctcvr/vtcvr 特征进入后续排序。训练分三层：先用单一 next-advertiser 标签做 SFT；再用 GRPO 生成 20 个 advertiser 与 5 个兴趣，并用命中位置和严格输出长度计算 reward； 未运行 Pinterest 私有 PinCLIP SID 三阶段 CPT，也不声称本地 AUC/Recall 可外推 RoAS。Fidelity: 完整核心链路。本地实际执行开源 causal LLM 的 LoRA SFT、论文位置/格式 reward 驱动的 clipped GRPO、受约束 advertiser 解码、训练式 two-tower、validation 配额选择的补充召回，以及 LLM advertiser score 作为排序特征。Pinterest 私有广告与跨站转化数据由公开商品品牌和购买序列替换。使用真实预训练语言模型和可训练 LoRA，不是规则或 embedding 打分替代 SFT/GRPO。  advertising llm-sft grpo candidate-generation 搜广推 语义表征、用户知识与冷启动 Pinterest Ads LLM 为什么只预测辅助 advertiser 与兴趣，而不接管实时广告排序？ 大模型汇总画像与跨来源行为后，离线预测高转化意图的 advertiser 和兴趣，再作为补充召回通道及转化率特征输入现有链路。SFT 学下一 advertiser，GRPO 用命中位置和输出长度奖励调整列表。每日批推理把成本移出请求路径，因此它改善的是现有系统的辅助信息，不等于端到端替代召回和排序。 示意：模型夜间预测某用户可能关注露营品牌，次日广告链路多一条相关召回和兴趣特征；是否展示某条广告，仍由实时转化模型和竞价规则共同决定。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-9b124905c1042fcc">Pinterest Ads LLM 为什么只预测辅助 advertiser 与兴趣，而不接管实时广告排序？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apinterest-ads-llm">Fine-Tuned LLM as a Complementary Predictor Improving Ads System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>大模型汇总画像与跨来源行为后，离线预测高转化意图的 advertiser 和兴趣，再作为补充召回通道及转化率特征输入现有链路。SFT 学下一 advertiser，GRPO 用命中位置和输出长度奖励调整列表。每日批推理把成本移出请求路径，因此它改善的是现有系统的辅助信息，不等于端到端替代召回和排序。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型夜间预测某用户可能关注露营品牌，次日广告链路多一条相关召回和兴趣特征；是否展示某条广告，仍由实时转化模型和竞价规则共同决定。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.27856">原论文</a> · <a href="../../../../reproductions/2605.27856-pinterest-ads-llm/">实现解读</a> · <a href="#qa-9b124905c1042fcc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pinterest-ads-llm" data-paper-title="Fine-Tuned LLM as a Complementary Predictor Improving Ads System" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Fine-Tuned LLM as a Complementary Predictor Improving Ads System 搜广推与 LLM 应用 Pinterest 2026-05-27 论文没有让 LLM 替换广告召回或排序，而是把它作为 ancillary predictor：输入用户画像、历史转化、搜索、URL、品类和品牌，预测下一批高转化意图 advertiser 与兴趣。预测结果一方面成为 advertiser 定向的补充召回通道，另一方面作为 ctcvr/vtcvr 特征进入后续排序。训练分三层：先用单一 next-advertiser 标签做 SFT；再用 GRPO 生成 20 个 advertiser 与 5 个兴趣，并用命中位置和严格输出长度计算 reward； 未运行 Pinterest 私有 PinCLIP SID 三阶段 CPT，也不声称本地 AUC/Recall 可外推 RoAS。Fidelity: 完整核心链路。本地实际执行开源 causal LLM 的 LoRA SFT、论文位置/格式 reward 驱动的 clipped GRPO、受约束 advertiser 解码、训练式 two-tower、validation 配额选择的补充召回，以及 LLM advertiser score 作为排序特征。Pinterest 私有广告与跨站转化数据由公开商品品牌和购买序列替换。使用真实预训练语言模型和可训练 LoRA，不是规则或 embedding 打分替代 SFT/GRPO。  advertising llm-sft grpo candidate-generation 搜广推 语义表征、用户知识与冷启动 SFT+GRPO 对 SFT 的比较与 LLM feature 对 two-tower 的比较，为什么应分开？ 前者检验 advertiser 生成后训练增量，后者检验将预测接入下游的价值，两者基线和指标不同。来源 GRPO 没提高 Recall，特征 AUC 有小改善，补充召回 quota 又选零，不能拼成“LLM 所有阶段都有效”。 示意：生成器没变准，但一个 log-prob 特征可能帮助点击判断；这不意味着更多品牌候选值得加入，也不能把 AUC 增量说成生成 Recall 增量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-654736ff6cb03e48">SFT+GRPO 对 SFT 的比较与 LLM feature 对 two-tower 的比较，为什么应分开？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apinterest-ads-llm">Fine-Tuned LLM as a Complementary Predictor Improving Ads System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者检验 advertiser 生成后训练增量，后者检验将预测接入下游的价值，两者基线和指标不同。来源 GRPO 没提高 Recall，特征 AUC 有小改善，补充召回 quota 又选零，不能拼成“LLM 所有阶段都有效”。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>生成器没变准，但一个 log-prob 特征可能帮助点击判断；这不意味着更多品牌候选值得加入，也不能把 AUC 增量说成生成 Recall 增量。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.27856">原论文</a> · <a href="../../../../reproductions/2605.27856-pinterest-ads-llm/">实现解读</a> · <a href="#qa-654736ff6cb03e48">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pinterest-ads-llm" data-paper-title="Fine-Tuned LLM as a Complementary Predictor Improving Ads System" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Fine-Tuned LLM as a Complementary Predictor Improving Ads System 搜广推与 LLM 应用 Pinterest 2026-05-27 论文没有让 LLM 替换广告召回或排序，而是把它作为 ancillary predictor：输入用户画像、历史转化、搜索、URL、品类和品牌，预测下一批高转化意图 advertiser 与兴趣。预测结果一方面成为 advertiser 定向的补充召回通道，另一方面作为 ctcvr/vtcvr 特征进入后续排序。训练分三层：先用单一 next-advertiser 标签做 SFT；再用 GRPO 生成 20 个 advertiser 与 5 个兴趣，并用命中位置和严格输出长度计算 reward； 未运行 Pinterest 私有 PinCLIP SID 三阶段 CPT，也不声称本地 AUC/Recall 可外推 RoAS。Fidelity: 完整核心链路。本地实际执行开源 causal LLM 的 LoRA SFT、论文位置/格式 reward 驱动的 clipped GRPO、受约束 advertiser 解码、训练式 two-tower、validation 配额选择的补充召回，以及 LLM advertiser score 作为排序特征。Pinterest 私有广告与跨站转化数据由公开商品品牌和购买序列替换。使用真实预训练语言模型和可训练 LoRA，不是规则或 embedding 打分替代 SFT/GRPO。  advertising llm-sft grpo candidate-generation 搜广推 语义表征、用户知识与冷启动 严格输出长度 reward 与命中位置 reward，为什么需要同时验收？ 命中位置鼓励正确 advertiser 靠前，长度罚防止模型通过输出过多名称增加碰中机会。解析去重、advertiser 与兴趣分别计数，缩比五项规则也需明确。验证选择 SFT 或 quota 零应保留，不能看 test mean rank 再改选。 示意：要求五个品牌却输出五十个，即使包含真目标也违规；只看命中会奖励这种投机，长度项使输出预算成为训练目标的一部分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7f2c2561b0e640a5">严格输出长度 reward 与命中位置 reward，为什么需要同时验收？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apinterest-ads-llm">Fine-Tuned LLM as a Complementary Predictor Improving Ads System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>命中位置鼓励正确 advertiser 靠前，长度罚防止模型通过输出过多名称增加碰中机会。解析去重、advertiser 与兴趣分别计数，缩比五项规则也需明确。验证选择 SFT 或 quota 零应保留，不能看 test mean rank 再改选。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>要求五个品牌却输出五十个，即使包含真目标也违规；只看命中会奖励这种投机，长度项使输出预算成为训练目标的一部分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.27856">原论文</a> · <a href="../../../../reproductions/2605.27856-pinterest-ads-llm/">实现解读</a> · <a href="#qa-7f2c2561b0e640a5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:l2rec" data-paper-title="L2Rec: Towards Dual-View Understanding of LLMs for Personalized Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="L2Rec: Towards Dual-View Understanding of LLMs for Personalized Recommendation 搜广推与 LLM 应用 NetEase Cloud Music 2026-05-26 共享 LLM 中插入按用户路由的双视图 LoRA-MoE，分别适配语义视图和行为视图，再由自适应跨视图门控融合。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  llm-recommendation parameter-efficient-tuning multi-view 搜广推 语义表征、用户知识与冷启动 L2Rec 为什么在共享 LLM 内区分语义视图与行为视图的 LoRA 专家？ 文本含义与协同消费关系不完全一致，单一适配可能让一侧占主导。双视图专家分别更新低秩路径，再按用户路由和跨视图 gate 组合，保留共用主干与不同任务几何。多专家不是每用户独立模型，个性化程度受路由与数据支持限制。 示意：用户既喜欢题材语义又有特定共同消费习惯，语义专家理解“悬疑”，行为专家利用该用户群偏好；两者不必输出同一方向。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-l2rec-4fe523da" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-1acdc921702b9a6f">L2Rec 为什么在共享 LLM 内区分语义视图与行为视图的 LoRA 专家？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Al2rec">L2Rec: Towards Dual-View Understanding of LLMs for Personalized Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NetEase Cloud Music</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文本含义与协同消费关系不完全一致，单一适配可能让一侧占主导。双视图专家分别更新低秩路径，再按用户路由和跨视图 gate 组合，保留共用主干与不同任务几何。多专家不是每用户独立模型，个性化程度受路由与数据支持限制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户既喜欢题材语义又有特定共同消费习惯，语义专家理解“悬疑”，行为专家利用该用户群偏好；两者不必输出同一方向。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.26717">原论文</a> · <a href="../../../../reproductions/2605.26717-l2rec/">实现解读</a> · <a href="#qa-1acdc921702b9a6f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:l2rec" data-paper-title="L2Rec: Towards Dual-View Understanding of LLMs for Personalized Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="L2Rec: Towards Dual-View Understanding of LLMs for Personalized Recommendation 搜广推与 LLM 应用 NetEase Cloud Music 2026-05-26 共享 LLM 中插入按用户路由的双视图 LoRA-MoE，分别适配语义视图和行为视图，再由自适应跨视图门控融合。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  llm-recommendation parameter-efficient-tuning multi-view 搜广推 语义表征、用户知识与冷启动 L2Rec为什么为语义视图和行为视图分别配置用户路由的LoRA专家？ 语义与协同行为可能互补也可能冲突，共用一套适配参数容易让强信号覆盖另一种。双视图低秩专家分别学习各自更新方向，用户路由再选择合适组合，跨视图gate决定最终融合。参数高效不代表无需足够监督；若路由总选同一专家，仍可能退化成没有分工的共享适配器。 示意：新用户主要靠内容语义，老用户可借丰富共同行为；两个视图分别保留能力后按用户组合，比一套LoRA强行同时解释所有场景更有弹性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-0f9d51153d32097b">L2Rec为什么为语义视图和行为视图分别配置用户路由的LoRA专家？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Al2rec">L2Rec: Towards Dual-View Understanding of LLMs for Personalized Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NetEase Cloud Music</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语义与协同行为可能互补也可能冲突，共用一套适配参数容易让强信号覆盖另一种。双视图低秩专家分别学习各自更新方向，用户路由再选择合适组合，跨视图gate决定最终融合。参数高效不代表无需足够监督；若路由总选同一专家，仍可能退化成没有分工的共享适配器。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新用户主要靠内容语义，老用户可借丰富共同行为；两个视图分别保留能力后按用户组合，比一套LoRA强行同时解释所有场景更有弹性。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.26717">原论文</a> · <a href="../../../../reproductions/2605.26717-l2rec/">实现解读</a> · <a href="#qa-0f9d51153d32097b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:l2rec" data-paper-title="L2Rec: Towards Dual-View Understanding of LLMs for Personalized Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="L2Rec: Towards Dual-View Understanding of LLMs for Personalized Recommendation 搜广推与 LLM 应用 NetEase Cloud Music 2026-05-26 共享 LLM 中插入按用户路由的双视图 LoRA-MoE，分别适配语义视图和行为视图，再由自适应跨视图门控融合。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  llm-recommendation parameter-efficient-tuning multi-view 搜广推 语义表征、用户知识与冷启动 按用户路由 LoRA-MoE 与一份全局 LoRA，相比参数共享发生什么变化？ 全局 LoRA 对所有用户使用同一低秩增量，MoE 从共享专家池按用户挑不同组合，增加条件容量而不为每个人存全量模型。路由会带来稀疏训练与专家饥饿问题，不能只按总参数量判断有效容量或推荐效果。 示意：摄影用户和烘焙用户可使用不同专家比例，但仍共享其中通用部分；若路由总选同一个专家，表面多专家也退化近似全局 LoRA。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-6d206ae586f50093">按用户路由 LoRA-MoE 与一份全局 LoRA，相比参数共享发生什么变化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Al2rec">L2Rec: Towards Dual-View Understanding of LLMs for Personalized Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NetEase Cloud Music</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全局 LoRA 对所有用户使用同一低秩增量，MoE 从共享专家池按用户挑不同组合，增加条件容量而不为每个人存全量模型。路由会带来稀疏训练与专家饥饿问题，不能只按总参数量判断有效容量或推荐效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>摄影用户和烘焙用户可使用不同专家比例，但仍共享其中通用部分；若路由总选同一个专家，表面多专家也退化近似全局 LoRA。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.26717">原论文</a> · <a href="../../../../reproductions/2605.26717-l2rec/">实现解读</a> · <a href="#qa-6d206ae586f50093">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:l2rec" data-paper-title="L2Rec: Towards Dual-View Understanding of LLMs for Personalized Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="L2Rec: Towards Dual-View Understanding of LLMs for Personalized Recommendation 搜广推与 LLM 应用 NetEase Cloud Music 2026-05-26 共享 LLM 中插入按用户路由的双视图 LoRA-MoE，分别适配语义视图和行为视图，再由自适应跨视图门控融合。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  llm-recommendation parameter-efficient-tuning multi-view 搜广推 语义表征、用户知识与冷启动 L2Rec 的 BA 低秩增量与 Top-K gate，哪些轴和参数需要分开？ 每个视图每个专家有独立 A、B，先形成与原权重同形增量，再按用户 gate 加权；路由只在专家维选择，跨视图融合另行处理。语义与行为状态错配不能由形状检查发现。本地代理分数不代表完整 LLM 专家路径都被训练。 示意：语义专家的 A 不能误配行为专家的 B，虽然尺寸一样也会形成另一映射；Top-K 在用户轴选人更是不同算法。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1bcc8694671b1b66">L2Rec 的 BA 低秩增量与 Top-K gate，哪些轴和参数需要分开？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Al2rec">L2Rec: Towards Dual-View Understanding of LLMs for Personalized Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NetEase Cloud Music</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每个视图每个专家有独立 A、B，先形成与原权重同形增量，再按用户 gate 加权；路由只在专家维选择，跨视图融合另行处理。语义与行为状态错配不能由形状检查发现。本地代理分数不代表完整 LLM 专家路径都被训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>语义专家的 A 不能误配行为专家的 B，虽然尺寸一样也会形成另一映射；Top-K 在用户轴选人更是不同算法。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.26717">原论文</a> · <a href="../../../../reproductions/2605.26717-l2rec/">实现解读</a> · <a href="#qa-1bcc8694671b1b66">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:muchator" data-paper-title="MuChator: Enabling Active Music Discovery via Conversational Music LLMs in Douyin Music" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="MuChator: Enabling Active Music Discovery via Conversational Music LLMs in Douyin Music 搜广推与 LLM 应用 ByteDance 2026-05-26 围绕音乐领域继续预训练、SFT 与强化学习，让对话模型从用户即时表达中解析音乐意图，并主动探索而非只复述历史偏好。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04477，相对变化 -17.09%。本地代理目标与论文生产任务不同，不能外推线上 lift。  music-recommendation conversational-llm active-discovery 搜广推 语义表征、用户知识与冷启动 MuChaToR 为什么把音乐推荐放进对话而非只做历史下一首？ 用户即时表达包含心情、场景和探索意愿，可能与长期播放记录不同，对话可澄清这些需求并组织发现。领域预训提供音乐知识，SFT 与 RL 再连接交互。模型能聊音乐不意味着推荐实际合口味，仍需专门评价与合法曲库映射。 示意：用户说“通勤轻松一点但别全是老歌”，下一首历史模型可能重复熟悉艺人，对话目标则要同时满足氛围与适度探索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-muchator-f63c99f7" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d872f4ff94de9805">MuChaToR 为什么把音乐推荐放进对话而非只做历史下一首？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amuchator">MuChator: Enabling Active Music Discovery via Conversational Music LLMs in Douyin Music</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用户即时表达包含心情、场景和探索意愿，可能与长期播放记录不同，对话可澄清这些需求并组织发现。领域预训提供音乐知识，SFT 与 RL 再连接交互。模型能聊音乐不意味着推荐实际合口味，仍需专门评价与合法曲库映射。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户说“通勤轻松一点但别全是老歌”，下一首历史模型可能重复熟悉艺人，对话目标则要同时满足氛围与适度探索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.27103">原论文</a> · <a href="../../../../reproductions/2605.27103-muchator/">实现解读</a> · <a href="#qa-d872f4ff94de9805">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:muchator" data-paper-title="MuChator: Enabling Active Music Discovery via Conversational Music LLMs in Douyin Music" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="MuChator: Enabling Active Music Discovery via Conversational Music LLMs in Douyin Music 搜广推与 LLM 应用 ByteDance 2026-05-26 围绕音乐领域继续预训练、SFT 与强化学习，让对话模型从用户即时表达中解析音乐意图，并主动探索而非只复述历史偏好。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04477，相对变化 -17.09%。本地代理目标与论文生产任务不同，不能外推线上 lift。  music-recommendation conversational-llm active-discovery 搜广推 语义表征、用户知识与冷启动 MuChaToR 为什么在音乐领域预训练和指令学习之外，还要优化意图、探索与对话奖励？ 领域预训练主要补音乐知识，指令学习教模型按示例回答，却未必让它处理即时偏好和探索之间的取舍。强化学习把意图满足、新发现与对话质量转成行为反馈，并用参考策略约束更新。模型因此有机会学会何时沿用熟悉风格、何时主动探索；本地代理排序结果不能当作真实音乐对话效果。 示意：用户说“通勤想听轻松点，但别总是老歌”。只模仿历史可能继续推熟悉艺人，奖励设计则让模型同时顾及轻松氛围和适度的新艺人发现。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-9c20977be1c72097">MuChaToR 为什么在音乐领域预训练和指令学习之外，还要优化意图、探索与对话奖励？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amuchator">MuChator: Enabling Active Music Discovery via Conversational Music LLMs in Douyin Music</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>领域预训练主要补音乐知识，指令学习教模型按示例回答，却未必让它处理即时偏好和探索之间的取舍。强化学习把意图满足、新发现与对话质量转成行为反馈，并用参考策略约束更新。模型因此有机会学会何时沿用熟悉风格、何时主动探索；本地代理排序结果不能当作真实音乐对话效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户说“通勤想听轻松点，但别总是老歌”。只模仿历史可能继续推熟悉艺人，奖励设计则让模型同时顾及轻松氛围和适度的新艺人发现。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.27103">原论文</a> · <a href="../../../../reproductions/2605.27103-muchator/">实现解读</a> · <a href="#qa-9c20977be1c72097">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:muchator" data-paper-title="MuChator: Enabling Active Music Discovery via Conversational Music LLMs in Douyin Music" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="MuChator: Enabling Active Music Discovery via Conversational Music LLMs in Douyin Music 搜广推与 LLM 应用 ByteDance 2026-05-26 围绕音乐领域继续预训练、SFT 与强化学习，让对话模型从用户即时表达中解析音乐意图，并主动探索而非只复述历史偏好。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04477，相对变化 -17.09%。本地代理目标与论文生产任务不同，不能外推线上 lift。  music-recommendation conversational-llm active-discovery 搜广推 语义表征、用户知识与冷启动 MuChaToR 的 discovery reward 与只奖励意图匹配，有何可能冲突？ 完全贴近历史意图可能不给新体验，发现奖励鼓励扩展，但过强又可能推不相关内容；对话质量也可能偏向好听解释。多目标与 KL 尝试平衡，不能把其中任一奖励升高当总体满意提升。电影代理不包含真实音乐对话反应。 示意：推荐全新实验音乐很新颖却不适合轻松通勤，熟悉流行歌很契合却没有发现；两者取舍需要反馈，不是简单越新越好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7ab48c3662179e27">MuChaToR 的 discovery reward 与只奖励意图匹配，有何可能冲突？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amuchator">MuChator: Enabling Active Music Discovery via Conversational Music LLMs in Douyin Music</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>完全贴近历史意图可能不给新体验，发现奖励鼓励扩展，但过强又可能推不相关内容；对话质量也可能偏向好听解释。多目标与 KL 尝试平衡，不能把其中任一奖励升高当总体满意提升。电影代理不包含真实音乐对话反应。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>推荐全新实验音乐很新颖却不适合轻松通勤，熟悉流行歌很契合却没有发现；两者取舍需要反馈，不是简单越新越好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.27103">原论文</a> · <a href="../../../../reproductions/2605.27103-muchator/">实现解读</a> · <a href="#qa-7ab48c3662179e27">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:muchator" data-paper-title="MuChator: Enabling Active Music Discovery via Conversational Music LLMs in Douyin Music" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="MuChator: Enabling Active Music Discovery via Conversational Music LLMs in Douyin Music 搜广推与 LLM 应用 ByteDance 2026-05-26 围绕音乐领域继续预训练、SFT 与强化学习，让对话模型从用户即时表达中解析音乐意图，并主动探索而非只复述历史偏好。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04477，相对变化 -17.09%。本地代理目标与论文生产任务不同，不能外推线上 lift。  music-recommendation conversational-llm active-discovery 搜广推 语义表征、用户知识与冷启动 MuChaToR 本地 MovieLens 排序结果为什么不能验证音乐继续预训与对话 RL？ 公开代理没有真实音乐知识语料、轮次对话和对应奖励环境，固定候选 NDCG 只反映实际核心评分路径。要声称对话训练需展示参数更新与合法任务日志，不能借论文术语补齐缺失。来源负结果应保留而非替换成原文业务值。 示意：把电影 genre 当音乐兴趣可以做接口示意，却不能证明模型懂和声、能澄清歌单需求；即使命中变好也不等于对话发现能力。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1bdf37c113e2ddfe">MuChaToR 本地 MovieLens 排序结果为什么不能验证音乐继续预训与对话 RL？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amuchator">MuChator: Enabling Active Music Discovery via Conversational Music LLMs in Douyin Music</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>公开代理没有真实音乐知识语料、轮次对话和对应奖励环境，固定候选 NDCG 只反映实际核心评分路径。要声称对话训练需展示参数更新与合法任务日志，不能借论文术语补齐缺失。来源负结果应保留而非替换成原文业务值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把电影 genre 当音乐兴趣可以做接口示意，却不能证明模型懂和声、能澄清歌单需求；即使命中变好也不等于对话发现能力。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.27103">原论文</a> · <a href="../../../../reproductions/2605.27103-muchator/">实现解读</a> · <a href="#qa-1bdf37c113e2ddfe">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:akt-rec" data-paper-title="From Head to Tail: Asymmetric Knowledge Transfer in Long-tail Recommendation with Generative Semantic IDs" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="From Head to Tail: Asymmetric Knowledge Transfer in Long-tail Recommendation with Generative Semantic IDs 搜广推与 LLM 应用 Alibaba Group / Peking University 2026-05-22 工业推荐的用户与物品都呈强长尾分布。直接共享表示可能把尾部稀疏且噪声较大的信号反向传给头部，普通对称对比学习因此不一定安全。AKT-Rec 先用 MLLM 对齐内容和协同信号，再用 RQ-VAE 把用户、物品量化成层级 Semantic ID，以同一高层 ID 定义语义簇。排序阶段为每个 ID 同时学习 cluster view 和 individual view。非对称 InfoNCE 对 tail→head 方向赋更大权重，并在作为 teacher 的一侧 stop-gradient； Fidelity: 核心机制复现。本地对真实 SmolLM2-135M 注入 LoRA，实际执行物品共现对比微调、用户兴趣/类别监督、残差 Semantic ID、cluster/individual 双视图、head-to-tail 非对称 stop-gradient、正交约束与两级活动度门控。真实训练开源 causal LM 的 LoRA，并分别执行物品协同对齐和用户监督；没有用哈希或静态文本向量替代这两步。本地对照口径：基线是只使用 individual embedding 和实例级 target attention 的 online_base；  llm-recommendation semantic-id long-tail ctr-ranking 搜广推 语义表征、用户知识与冷启动 AKT-Rec 的 cluster view 与 individual view 为什么都保留，而不只给长尾物品一个语义簇向量？ 簇表示共享同类物品知识，缓解长尾反馈不足；个体表示保留已有行为差异，避免同簇物品完全同质化。活动度门控决定共享比例，软正交又鼓励两视图互补。尾部需要借力并不意味着放弃身份信息，头部也可能从簇结构受益。 示意：两部同题材电影共享科幻簇，但一部偏动作、一部偏哲思，个体分支保留受众差别。新片可多借簇知识，老片则利用充分反馈。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-akt-rec-be638f5f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-839084f49fa9670e">AKT-Rec 的 cluster view 与 individual view 为什么都保留，而不只给长尾物品一个语义簇向量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aakt-rec">From Head to Tail: Asymmetric Knowledge Transfer in Long-tail Recommendation with Generative Semantic IDs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group / Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>簇表示共享同类物品知识，缓解长尾反馈不足；个体表示保留已有行为差异，避免同簇物品完全同质化。活动度门控决定共享比例，软正交又鼓励两视图互补。尾部需要借力并不意味着放弃身份信息，头部也可能从簇结构受益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两部同题材电影共享科幻簇，但一部偏动作、一部偏哲思，个体分支保留受众差别。新片可多借簇知识，老片则利用充分反馈。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.23310">原论文</a> · <a href="../../../../reproductions/2605.23310-akt-rec/">实现解读</a> · <a href="#qa-839084f49fa9670e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:akt-rec" data-paper-title="From Head to Tail: Asymmetric Knowledge Transfer in Long-tail Recommendation with Generative Semantic IDs" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="From Head to Tail: Asymmetric Knowledge Transfer in Long-tail Recommendation with Generative Semantic IDs 搜广推与 LLM 应用 Alibaba Group / Peking University 2026-05-22 工业推荐的用户与物品都呈强长尾分布。直接共享表示可能把尾部稀疏且噪声较大的信号反向传给头部，普通对称对比学习因此不一定安全。AKT-Rec 先用 MLLM 对齐内容和协同信号，再用 RQ-VAE 把用户、物品量化成层级 Semantic ID，以同一高层 ID 定义语义簇。排序阶段为每个 ID 同时学习 cluster view 和 individual view。非对称 InfoNCE 对 tail→head 方向赋更大权重，并在作为 teacher 的一侧 stop-gradient； Fidelity: 核心机制复现。本地对真实 SmolLM2-135M 注入 LoRA，实际执行物品共现对比微调、用户兴趣/类别监督、残差 Semantic ID、cluster/individual 双视图、head-to-tail 非对称 stop-gradient、正交约束与两级活动度门控。真实训练开源 causal LM 的 LoRA，并分别执行物品协同对齐和用户监督；没有用哈希或静态文本向量替代这两步。本地对照口径：基线是只使用 individual embedding 和实例级 target attention 的 online_base；  llm-recommendation semantic-id long-tail ctr-ranking 搜广推 语义表征、用户知识与冷启动 AKT-Rec为什么让长尾更多地向头部学习，并阻断teacher一侧梯度？ 头部交互更丰富，通常可为同语义簇的长尾提供较稳定知识。非对称迁移加强尾部向头部对齐，并用stop-gradient避免尾部噪声反向拖动teacher；cluster与individual两视图及活动度门控又保留个体差异。若完全共享或双向同权，就可能既污染头部，又把不同长尾物品揉成一团。 示意：一款新品鞋可借同簇热销鞋的共同知识，但保留自己的尺码与用途；新品少量偶然点击不应立即改写整个热销簇的表示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-45241ee3447dbb5c">AKT-Rec为什么让长尾更多地向头部学习，并阻断teacher一侧梯度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aakt-rec">From Head to Tail: Asymmetric Knowledge Transfer in Long-tail Recommendation with Generative Semantic IDs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group / Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>头部交互更丰富，通常可为同语义簇的长尾提供较稳定知识。非对称迁移加强尾部向头部对齐，并用stop-gradient避免尾部噪声反向拖动teacher；cluster与individual两视图及活动度门控又保留个体差异。若完全共享或双向同权，就可能既污染头部，又把不同长尾物品揉成一团。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一款新品鞋可借同簇热销鞋的共同知识，但保留自己的尺码与用途；新品少量偶然点击不应立即改写整个热销簇的表示。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.23310">原论文</a> · <a href="../../../../reproductions/2605.23310-akt-rec/">实现解读</a> · <a href="#qa-45241ee3447dbb5c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:akt-rec" data-paper-title="From Head to Tail: Asymmetric Knowledge Transfer in Long-tail Recommendation with Generative Semantic IDs" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="From Head to Tail: Asymmetric Knowledge Transfer in Long-tail Recommendation with Generative Semantic IDs 搜广推与 LLM 应用 Alibaba Group / Peking University 2026-05-22 工业推荐的用户与物品都呈强长尾分布。直接共享表示可能把尾部稀疏且噪声较大的信号反向传给头部，普通对称对比学习因此不一定安全。AKT-Rec 先用 MLLM 对齐内容和协同信号，再用 RQ-VAE 把用户、物品量化成层级 Semantic ID，以同一高层 ID 定义语义簇。排序阶段为每个 ID 同时学习 cluster view 和 individual view。非对称 InfoNCE 对 tail→head 方向赋更大权重，并在作为 teacher 的一侧 stop-gradient； Fidelity: 核心机制复现。本地对真实 SmolLM2-135M 注入 LoRA，实际执行物品共现对比微调、用户兴趣/类别监督、残差 Semantic ID、cluster/individual 双视图、head-to-tail 非对称 stop-gradient、正交约束与两级活动度门控。真实训练开源 causal LM 的 LoRA，并分别执行物品协同对齐和用户监督；没有用哈希或静态文本向量替代这两步。本地对照口径：基线是只使用 individual embedding 和实例级 target attention 的 online_base；  llm-recommendation semantic-id long-tail ctr-ranking 搜广推 语义表征、用户知识与冷启动 AKT-Rec 的非对称迁移与普通对称 InfoNCE，区别仅是正负例更多吗？ 不是。它对 tail 向 head 学习赋更大权重，并在教师侧停止梯度，控制知识迁移方向，避免稀疏噪声同等反向改写可靠表示。对称对比则让双方共同调整。这个假设依赖头部确实更可靠，不保证所有语义簇都适合如此迁移。 示意：冷门新片向已有丰富反馈的同簇老片学习较合理；若同时让老片被少量噪声新片强烈拉动，就可能破坏稳定表征，增加样本数本身解决不了方向问题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5233252aac6658c3">AKT-Rec 的非对称迁移与普通对称 InfoNCE，区别仅是正负例更多吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aakt-rec">From Head to Tail: Asymmetric Knowledge Transfer in Long-tail Recommendation with Generative Semantic IDs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group / Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。它对 tail 向 head 学习赋更大权重，并在教师侧停止梯度，控制知识迁移方向，避免稀疏噪声同等反向改写可靠表示。对称对比则让双方共同调整。这个假设依赖头部确实更可靠，不保证所有语义簇都适合如此迁移。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>冷门新片向已有丰富反馈的同簇老片学习较合理；若同时让老片被少量噪声新片强烈拉动，就可能破坏稳定表征，增加样本数本身解决不了方向问题。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.23310">原论文</a> · <a href="../../../../reproductions/2605.23310-akt-rec/">实现解读</a> · <a href="#qa-5233252aac6658c3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:akt-rec" data-paper-title="From Head to Tail: Asymmetric Knowledge Transfer in Long-tail Recommendation with Generative Semantic IDs" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="From Head to Tail: Asymmetric Knowledge Transfer in Long-tail Recommendation with Generative Semantic IDs 搜广推与 LLM 应用 Alibaba Group / Peking University 2026-05-22 工业推荐的用户与物品都呈强长尾分布。直接共享表示可能把尾部稀疏且噪声较大的信号反向传给头部，普通对称对比学习因此不一定安全。AKT-Rec 先用 MLLM 对齐内容和协同信号，再用 RQ-VAE 把用户、物品量化成层级 Semantic ID，以同一高层 ID 定义语义簇。排序阶段为每个 ID 同时学习 cluster view 和 individual view。非对称 InfoNCE 对 tail→head 方向赋更大权重，并在作为 teacher 的一侧 stop-gradient； Fidelity: 核心机制复现。本地对真实 SmolLM2-135M 注入 LoRA，实际执行物品共现对比微调、用户兴趣/类别监督、残差 Semantic ID、cluster/individual 双视图、head-to-tail 非对称 stop-gradient、正交约束与两级活动度门控。真实训练开源 causal LM 的 LoRA，并分别执行物品协同对齐和用户监督；没有用哈希或静态文本向量替代这两步。本地对照口径：基线是只使用 individual embedding 和实例级 target attention 的 online_base；  llm-recommendation semantic-id long-tail ctr-ranking 搜广推 语义表征、用户知识与冷启动 AKT-Rec 两级活动度 gate 分别放在什么信息融合位置？ 第一层 gate 在 cluster 与 individual embedding 之间分配权重；第二层 gate 在簇级历史与实例级历史之间融合，条件包含用户、物品及交叉活动度。两者作用于不同表示层，不能合并成一个固定 blend。对比目标的 stop-gradient 也应只阻断指定教师侧。 示意：新商品先在物品表示上多借簇知识；同一请求再因用户历史稀疏而提高簇级历史权重。只调第一个系数，不能替代后一个历史层选择。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-904bf22dbb99d023">AKT-Rec 两级活动度 gate 分别放在什么信息融合位置？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aakt-rec">From Head to Tail: Asymmetric Knowledge Transfer in Long-tail Recommendation with Generative Semantic IDs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group / Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>第一层 gate 在 cluster 与 individual embedding 之间分配权重；第二层 gate 在簇级历史与实例级历史之间融合，条件包含用户、物品及交叉活动度。两者作用于不同表示层，不能合并成一个固定 blend。对比目标的 stop-gradient 也应只阻断指定教师侧。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新商品先在物品表示上多借簇知识；同一请求再因用户历史稀疏而提高簇级历史权重。只调第一个系数，不能替代后一个历史层选择。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.23310">原论文</a> · <a href="../../../../reproductions/2605.23310-akt-rec/">实现解读</a> · <a href="#qa-904bf22dbb99d023">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:fluid" data-paper-title="FLUID: From Ephemeral IDs to Multimodal Semantic Codes for Industrial-Scale Livestreaming Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="FLUID: From Ephemeral IDs to Multimodal Semantic Codes for Industrial-Scale Livestreaming Recommendation 搜广推与 LLM 应用 TikTok / ByteDance 2026-05-20 直播间通常只存活几十分钟，候选 item ID 来不及积累协同信号。FLUID 用 SigLIP2 与 Qwen3-Embedding 跨域编码短视频和直播的两分钟切片，再用四层 RQ-KMeans 得到 LUCID。slice LUCID 表示当前内容，room LUCID 对历史切片逐层多数投票；两者以独立 token 晚融合，最终完全移除候选 item ID，并用“加 slice—退 ID—加 room”三阶段避免切换不稳定。 未运行 SigLIP2、Qwen3-Embedding-0.6B、直播 ASR/OCR、真实两分钟切片和生产增量训练；Fidelity: 核心机制复现。执行跨域内容融合、slice/room 两级 LUCID、RQ-KMeans、prefix n-gram、ID-free late fusion 与三阶段 warmup；公开数据替代生产多模态流量。未运行 SigLIP2、Qwen3-Embedding-0.6B、直播 ASR/OCR、真实两分钟切片和生产增量训练；本地证明的是 LUCID/去 ID/分阶段迁移链路可运行，不声称复现论文线上收益。  llm-recommendation multimodal semantic-id cold-start ranking 搜广推 语义表征、用户知识与冷启动 FLUID 为什么把直播切片与房间历史摘要当作两个独立 token？ 直播当前内容变化快，slice LUCID 捕捉此刻状态，room LUCID 汇总过去切片的稳定语义。晚融合让模型同时看到当前与长期定位，避免多数历史盖过新主题。room 多数投票仍会丢少数变化，不能替代当前切片。 示意：主播长期讲美妆，今天切到旅行收纳；room 仍表示长期定位，slice 表示当前主题，模型需要两者而非把今天内容平均抹掉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-fluid-d95a4248" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a48a51ad5530b68f">FLUID 为什么把直播切片与房间历史摘要当作两个独立 token？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Afluid">FLUID: From Ephemeral IDs to Multimodal Semantic Codes for Industrial-Scale Livestreaming Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · TikTok / ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直播当前内容变化快，slice LUCID 捕捉此刻状态，room LUCID 汇总过去切片的稳定语义。晚融合让模型同时看到当前与长期定位，避免多数历史盖过新主题。room 多数投票仍会丢少数变化，不能替代当前切片。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>主播长期讲美妆，今天切到旅行收纳；room 仍表示长期定位，slice 表示当前主题，模型需要两者而非把今天内容平均抹掉。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.21832">原论文</a> · <a href="../../../../reproductions/2605.21832-fluid/">实现解读</a> · <a href="#qa-a48a51ad5530b68f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:fluid" data-paper-title="FLUID: From Ephemeral IDs to Multimodal Semantic Codes for Industrial-Scale Livestreaming Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="FLUID: From Ephemeral IDs to Multimodal Semantic Codes for Industrial-Scale Livestreaming Recommendation 搜广推与 LLM 应用 TikTok / ByteDance 2026-05-20 直播间通常只存活几十分钟，候选 item ID 来不及积累协同信号。FLUID 用 SigLIP2 与 Qwen3-Embedding 跨域编码短视频和直播的两分钟切片，再用四层 RQ-KMeans 得到 LUCID。slice LUCID 表示当前内容，room LUCID 对历史切片逐层多数投票；两者以独立 token 晚融合，最终完全移除候选 item ID，并用“加 slice—退 ID—加 room”三阶段避免切换不稳定。 未运行 SigLIP2、Qwen3-Embedding-0.6B、直播 ASR/OCR、真实两分钟切片和生产增量训练；Fidelity: 核心机制复现。执行跨域内容融合、slice/room 两级 LUCID、RQ-KMeans、prefix n-gram、ID-free late fusion 与三阶段 warmup；公开数据替代生产多模态流量。未运行 SigLIP2、Qwen3-Embedding-0.6B、直播 ASR/OCR、真实两分钟切片和生产增量训练；本地证明的是 LUCID/去 ID/分阶段迁移链路可运行，不声称复现论文线上收益。  llm-recommendation multimodal semantic-id cold-start ranking 搜广推 语义表征、用户知识与冷启动 FLUID为何同时保留slice和room两种LUCID，并逐步退出item ID？ 短命直播间来不及积累稳定ID信号，slice码表达当前切片内容，room码从历史切片聚合较稳定语义。两者分开并晚融合，避免把瞬时内容与长期房间特征混成一个标签；分阶段加入切片、退ID、加房间，则降低特征切换对训练的冲击。退掉ID并不意味着内容码没有碰撞或新鲜度问题。 示意：同一房间平时卖运动服，此刻切片却在展示鞋；room码保留长期定位，slice码响应当前商品，不能只用一个已经过时的房间身份解释两种信号。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c0acb1d4423aebec">FLUID为何同时保留slice和room两种LUCID，并逐步退出item ID？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Afluid">FLUID: From Ephemeral IDs to Multimodal Semantic Codes for Industrial-Scale Livestreaming Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · TikTok / ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>短命直播间来不及积累稳定ID信号，slice码表达当前切片内容，room码从历史切片聚合较稳定语义。两者分开并晚融合，避免把瞬时内容与长期房间特征混成一个标签；分阶段加入切片、退ID、加房间，则降低特征切换对训练的冲击。退掉ID并不意味着内容码没有碰撞或新鲜度问题。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一房间平时卖运动服，此刻切片却在展示鞋；room码保留长期定位，slice码响应当前商品，不能只用一个已经过时的房间身份解释两种信号。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.21832">原论文</a> · <a href="../../../../reproductions/2605.21832-fluid/">实现解读</a> · <a href="#qa-c0acb1d4423aebec">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:fluid" data-paper-title="FLUID: From Ephemeral IDs to Multimodal Semantic Codes for Industrial-Scale Livestreaming Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="FLUID: From Ephemeral IDs to Multimodal Semantic Codes for Industrial-Scale Livestreaming Recommendation 搜广推与 LLM 应用 TikTok / ByteDance 2026-05-20 直播间通常只存活几十分钟，候选 item ID 来不及积累协同信号。FLUID 用 SigLIP2 与 Qwen3-Embedding 跨域编码短视频和直播的两分钟切片，再用四层 RQ-KMeans 得到 LUCID。slice LUCID 表示当前内容，room LUCID 对历史切片逐层多数投票；两者以独立 token 晚融合，最终完全移除候选 item ID，并用“加 slice—退 ID—加 room”三阶段避免切换不稳定。 未运行 SigLIP2、Qwen3-Embedding-0.6B、直播 ASR/OCR、真实两分钟切片和生产增量训练；Fidelity: 核心机制复现。执行跨域内容融合、slice/room 两级 LUCID、RQ-KMeans、prefix n-gram、ID-free late fusion 与三阶段 warmup；公开数据替代生产多模态流量。未运行 SigLIP2、Qwen3-Embedding-0.6B、直播 ASR/OCR、真实两分钟切片和生产增量训练；本地证明的是 LUCID/去 ID/分阶段迁移链路可运行，不声称复现论文线上收益。  llm-recommendation multimodal semantic-id cold-start ranking 搜广推 语义表征、用户知识与冷启动 FLUID 移除瞬时 item ID 与给新房间随机初始化 ID，相比借用了什么共享信息？ 随机 ID 需等待互动才能学会，语义前缀可从跨域内容编码中借用已见模式，适合短寿命直播间。代价是失去独立身份记忆，内容不足时会退化；来源本地去 ID 的整体质量下降，不能只报 fresh 指标提高。 示意：新直播间上线十分钟就结束，随机 ID 很难积累；内容码可立即连接同类主题，但若两个房间风格差异未进内容，移除 ID 也会丢区分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-66592890548a71b4">FLUID 移除瞬时 item ID 与给新房间随机初始化 ID，相比借用了什么共享信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Afluid">FLUID: From Ephemeral IDs to Multimodal Semantic Codes for Industrial-Scale Livestreaming Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · TikTok / ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>随机 ID 需等待互动才能学会，语义前缀可从跨域内容编码中借用已见模式，适合短寿命直播间。代价是失去独立身份记忆，内容不足时会退化；来源本地去 ID 的整体质量下降，不能只报 fresh 指标提高。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新直播间上线十分钟就结束，随机 ID 很难积累；内容码可立即连接同类主题，但若两个房间风格差异未进内容，移除 ID 也会丢区分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.21832">原论文</a> · <a href="../../../../reproductions/2605.21832-fluid/">实现解读</a> · <a href="#qa-66592890548a71b4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:fluid" data-paper-title="FLUID: From Ephemeral IDs to Multimodal Semantic Codes for Industrial-Scale Livestreaming Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="FLUID: From Ephemeral IDs to Multimodal Semantic Codes for Industrial-Scale Livestreaming Recommendation 搜广推与 LLM 应用 TikTok / ByteDance 2026-05-20 直播间通常只存活几十分钟，候选 item ID 来不及积累协同信号。FLUID 用 SigLIP2 与 Qwen3-Embedding 跨域编码短视频和直播的两分钟切片，再用四层 RQ-KMeans 得到 LUCID。slice LUCID 表示当前内容，room LUCID 对历史切片逐层多数投票；两者以独立 token 晚融合，最终完全移除候选 item ID，并用“加 slice—退 ID—加 room”三阶段避免切换不稳定。 未运行 SigLIP2、Qwen3-Embedding-0.6B、直播 ASR/OCR、真实两分钟切片和生产增量训练；Fidelity: 核心机制复现。执行跨域内容融合、slice/room 两级 LUCID、RQ-KMeans、prefix n-gram、ID-free late fusion 与三阶段 warmup；公开数据替代生产多模态流量。未运行 SigLIP2、Qwen3-Embedding-0.6B、直播 ASR/OCR、真实两分钟切片和生产增量训练；本地证明的是 LUCID/去 ID/分阶段迁移链路可运行，不声称复现论文线上收益。  llm-recommendation multimodal semantic-id cold-start ranking 搜广推 语义表征、用户知识与冷启动 LUCID 每层 embedding 为什么索引完整前缀，而不是单独的 codeword？ 同一后层码字在不同上层残差条件下含义不同，前缀累积索引保留路径身份。直接查孤立码字会错误合并不同语义分支。最终候选 token 只包含 room 与 slice，若仍混入候选 item ID，就没完成论文定义的退出过程。 示意：粗码“美妆”后细码三与粗码“旅行”后细码三不是同一语义，应占不同表项；只用整数三查同一向量会混淆两条路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ddf0ab5507e099e9">LUCID 每层 embedding 为什么索引完整前缀，而不是单独的 codeword？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Afluid">FLUID: From Ephemeral IDs to Multimodal Semantic Codes for Industrial-Scale Livestreaming Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · TikTok / ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一后层码字在不同上层残差条件下含义不同，前缀累积索引保留路径身份。直接查孤立码字会错误合并不同语义分支。最终候选 token 只包含 room 与 slice，若仍混入候选 item ID，就没完成论文定义的退出过程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>粗码“美妆”后细码三与粗码“旅行”后细码三不是同一语义，应占不同表项；只用整数三查同一向量会混淆两条路径。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.21832">原论文</a> · <a href="../../../../reproductions/2605.21832-fluid/">实现解读</a> · <a href="#qa-ddf0ab5507e099e9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mm-llm" data-paper-title="A General Framework for Multimodal LLM-Based Multimedia Understanding in Large-Scale Recommendation Systems" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="A General Framework for Multimodal LLM-Based Multimedia Understanding in Large-Scale Recommendation Systems 搜广推与 LLM 应用 Meta 2026-05-10 视觉 embedding 难表达细粒度语义。论文用视觉 encoder+Q-Former 对齐 LLaMA2 生成 caption，再规范化为 categorical token IDs；item tokens 和用户历史 token profile 与 ID/视觉特征拼接进入生产排序模型，LLM 推理脱离在线主链路。 caption 模块相对 ID+content 内部基线仅 +0.03% 且 Hit 下降，本地未验证有效收益。Fidelity: 核心机制复现。内容 encoder、query cross-attention、离散 caption token、用户语义兴趣和 ID/视觉排序融合均训练；原始私有图片及 BLIP-2/LLaMA2-1.5B 规模未复刻。本地对照口径：统一跨模型基线是 DIN，MM-LLM NDCG@10 相对 DIN -13.23%；内部 ID+content 基线加入 caption token 后仅 +0.03% 且 Hit 下降。内部持平不代表优于经典模型。  multimodal llm-recommendation ranking 搜广推 语义表征、用户知识与冷启动 MM-LLM 为什么把 caption 规范化成 categorical token IDs？ 自由描述表达丰富但长度和措辞变化大，规范化标签提供较稳定可缓存接口，便于与 ID、视觉特征和用户历史 profile 融合。规范化也会损失细节、继承 caption 错误，不能因变成离散 ID 就当作真实标注。 示意：同一画面被描述成“户外雨天露营”和“下雨时搭帐篷”，可归到相近属性 token，排序更易复用；若描述错了天气，标签也会错。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-mm-llm-7bcb82aa" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-933964f78c96769a">MM-LLM 为什么把 caption 规范化成 categorical token IDs？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amm-llm">A General Framework for Multimodal LLM-Based Multimedia Understanding in Large-Scale Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>自由描述表达丰富但长度和措辞变化大，规范化标签提供较稳定可缓存接口，便于与 ID、视觉特征和用户历史 profile 融合。规范化也会损失细节、继承 caption 错误，不能因变成离散 ID 就当作真实标注。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一画面被描述成“户外雨天露营”和“下雨时搭帐篷”，可归到相近属性 token，排序更易复用；若描述错了天气，标签也会错。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.09338">原论文</a> · <a href="../../../../reproductions/2605.09338-mm-llm/">实现解读</a> · <a href="#qa-933964f78c96769a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mm-llm" data-paper-title="A General Framework for Multimodal LLM-Based Multimedia Understanding in Large-Scale Recommendation Systems" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="A General Framework for Multimodal LLM-Based Multimedia Understanding in Large-Scale Recommendation Systems 搜广推与 LLM 应用 Meta 2026-05-10 视觉 embedding 难表达细粒度语义。论文用视觉 encoder+Q-Former 对齐 LLaMA2 生成 caption，再规范化为 categorical token IDs；item tokens 和用户历史 token profile 与 ID/视觉特征拼接进入生产排序模型，LLM 推理脱离在线主链路。 caption 模块相对 ID+content 内部基线仅 +0.03% 且 Hit 下降，本地未验证有效收益。Fidelity: 核心机制复现。内容 encoder、query cross-attention、离散 caption token、用户语义兴趣和 ID/视觉排序融合均训练；原始私有图片及 BLIP-2/LLaMA2-1.5B 规模未复刻。本地对照口径：统一跨模型基线是 DIN，MM-LLM NDCG@10 相对 DIN -13.23%；内部 ID+content 基线加入 caption token 后仅 +0.03% 且 Hit 下降。内部持平不代表优于经典模型。  multimodal llm-recommendation ranking 搜广推 语义表征、用户知识与冷启动 MM-LLM 为什么把视觉内容先转成规范化语义 token，而不在每次排序时直接调用大模型？ 视觉向量包含丰富信息，却不容易让排序器稳定利用细粒度语义。论文离线用视觉编码器、Q-Former 与语言模型生成描述，再规范化为可复用的类别 token；排序器融合这些语义与 ID、视觉特征。大模型负责提炼内容，在线小模型负责结合行为打分，两阶段把语义成本摊到多次请求。 示意：一张视频封面可离线得到“雨天、露营、装备教学”等 token。用户请求时排序器只读取这些特征和历史偏好，无须重新让语言模型看图解释。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-5ea845fc58225065">MM-LLM 为什么把视觉内容先转成规范化语义 token，而不在每次排序时直接调用大模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amm-llm">A General Framework for Multimodal LLM-Based Multimedia Understanding in Large-Scale Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>视觉向量包含丰富信息，却不容易让排序器稳定利用细粒度语义。论文离线用视觉编码器、Q-Former 与语言模型生成描述，再规范化为可复用的类别 token；排序器融合这些语义与 ID、视觉特征。大模型负责提炼内容，在线小模型负责结合行为打分，两阶段把语义成本摊到多次请求。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一张视频封面可离线得到“雨天、露营、装备教学”等 token。用户请求时排序器只读取这些特征和历史偏好，无须重新让语言模型看图解释。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.09338">原论文</a> · <a href="../../../../reproductions/2605.09338-mm-llm/">实现解读</a> · <a href="#qa-5ea845fc58225065">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mm-llm" data-paper-title="A General Framework for Multimodal LLM-Based Multimedia Understanding in Large-Scale Recommendation Systems" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="A General Framework for Multimodal LLM-Based Multimedia Understanding in Large-Scale Recommendation Systems 搜广推与 LLM 应用 Meta 2026-05-10 视觉 embedding 难表达细粒度语义。论文用视觉 encoder+Q-Former 对齐 LLaMA2 生成 caption，再规范化为 categorical token IDs；item tokens 和用户历史 token profile 与 ID/视觉特征拼接进入生产排序模型，LLM 推理脱离在线主链路。 caption 模块相对 ID+content 内部基线仅 +0.03% 且 Hit 下降，本地未验证有效收益。Fidelity: 核心机制复现。内容 encoder、query cross-attention、离散 caption token、用户语义兴趣和 ID/视觉排序融合均训练；原始私有图片及 BLIP-2/LLaMA2-1.5B 规模未复刻。本地对照口径：统一跨模型基线是 DIN，MM-LLM NDCG@10 相对 DIN -13.23%；内部 ID+content 基线加入 caption token 后仅 +0.03% 且 Hit 下降。内部持平不代表优于经典模型。  multimodal llm-recommendation ranking 搜广推 语义表征、用户知识与冷启动 MM-LLM 的 caption token 与直接使用视觉 embedding，相比补充哪类信息？ 视觉向量保留连续感知结构，caption 尝试提炼语言可用的细粒度概念，可能补用途与属性。二者也可能重复或互相矛盾，融合需要门控而非盲目相加。来源内部 caption 消融近乎持平且 Hit 下降，不支持把语义可读性直接当推荐收益。 示意：封面向量知道颜色布局，caption 可指出防水演示主题；若标题式概念没有超出视觉信息，加入它也可能只增加噪声与参数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-16be0a596f577f16">MM-LLM 的 caption token 与直接使用视觉 embedding，相比补充哪类信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amm-llm">A General Framework for Multimodal LLM-Based Multimedia Understanding in Large-Scale Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>视觉向量保留连续感知结构，caption 尝试提炼语言可用的细粒度概念，可能补用途与属性。二者也可能重复或互相矛盾，融合需要门控而非盲目相加。来源内部 caption 消融近乎持平且 Hit 下降，不支持把语义可读性直接当推荐收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>封面向量知道颜色布局，caption 可指出防水演示主题；若标题式概念没有超出视觉信息，加入它也可能只增加噪声与参数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.09338">原论文</a> · <a href="../../../../reproductions/2605.09338-mm-llm/">实现解读</a> · <a href="#qa-16be0a596f577f16">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mm-llm" data-paper-title="A General Framework for Multimodal LLM-Based Multimedia Understanding in Large-Scale Recommendation Systems" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="A General Framework for Multimodal LLM-Based Multimedia Understanding in Large-Scale Recommendation Systems 搜广推与 LLM 应用 Meta 2026-05-10 视觉 embedding 难表达细粒度语义。论文用视觉 encoder+Q-Former 对齐 LLaMA2 生成 caption，再规范化为 categorical token IDs；item tokens 和用户历史 token profile 与 ID/视觉特征拼接进入生产排序模型，LLM 推理脱离在线主链路。 caption 模块相对 ID+content 内部基线仅 +0.03% 且 Hit 下降，本地未验证有效收益。Fidelity: 核心机制复现。内容 encoder、query cross-attention、离散 caption token、用户语义兴趣和 ID/视觉排序融合均训练；原始私有图片及 BLIP-2/LLaMA2-1.5B 规模未复刻。本地对照口径：统一跨模型基线是 DIN，MM-LLM NDCG@10 相对 DIN -13.23%；内部 ID+content 基线加入 caption token 后仅 +0.03% 且 Hit 下降。内部持平不代表优于经典模型。  multimodal llm-recommendation ranking 搜广推 语义表征、用户知识与冷启动 MM-LLM 本地四 caption token 为什么不能冒充完整视觉—LLaMA2 训练？ 公开 content vector 代替私有图片，轻量 query cross-attention 生成少量代理 token，验证的是缩比融合，不含原视觉 encoder、Q-Former 和大模型全链路。应分别报告内部 ID+content 对照与 DIN 参照，不能把两种比较混成同一正收益。 示意：电影类型向量上产生四个 token，并不能证明模型看懂图片细节；即使融合 loss 下降，也不等同于实际生成高质量视觉描述。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-236a3f04620a3cd6">MM-LLM 本地四 caption token 为什么不能冒充完整视觉—LLaMA2 训练？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amm-llm">A General Framework for Multimodal LLM-Based Multimedia Understanding in Large-Scale Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>公开 content vector 代替私有图片，轻量 query cross-attention 生成少量代理 token，验证的是缩比融合，不含原视觉 encoder、Q-Former 和大模型全链路。应分别报告内部 ID+content 对照与 DIN 参照，不能把两种比较混成同一正收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>电影类型向量上产生四个 token，并不能证明模型看懂图片细节；即使融合 loss 下降，也不等同于实际生成高质量视觉描述。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.09338">原论文</a> · <a href="../../../../reproductions/2605.09338-mm-llm/">实现解读</a> · <a href="#qa-236a3f04620a3cd6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recgpt-mobile" data-paper-title="RecGPT-Mobile: On-Device Large Language Models for User Intent Understanding in Taobao Feed Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RecGPT-Mobile: On-Device Large Language Models for User Intent Understanding in Taobao Feed Recommendation 搜广推与 LLM 应用 Alibaba / Taobao 2026-05-06 云端 LLM 能把点击、加购、收藏、购买等隐式行为翻译成显式搜索意图，但频繁上传行为并推理会增加成本、延迟和隐私风险。RecGPT-Mobile 把 Qwen3-0.6B 量化模型放到手机端，形成“本地收集行为→自适应构造 prompt→生成下一 query→服务端检索”的链路。训练数据由行为/搜索日志 60%、共购关系 20%、GPT 改写 15% 和人工标注 5% 组成；LoRA SFT 学习行为到 query 的映射。 Fidelity: 核心机制复现。实际执行 causal LM LoRA SFT、预算约束 adaptive prompt、意图漂移触发与 INT8 权重量化；私有数据和手机端系统缩小。本地模型是真实 causal LM 和 LoRA，不是类型分类 MLP；adaptive prompt、三项漂移公式和量化路径均执行。MovieLens 类型替代淘宝搜索 query，没有 GPT 改写、人工标注、生产检索和真机 fleet，故只验证方法链路与相对趋势。本地对照口径：基线为同一 SmolLM2-135M-Instruct 的零样本 intent completion；  llm-recommendation on-device intent-understanding serving-efficiency 搜广推 语义表征、用户知识与冷启动 RecGPT-Mobile 为什么把行为到 query 放到端侧，而检索仍留服务端？ 端侧可少传原始行为并利用即时上下文，小量化模型生成意图，服务端继续维护大目录与检索。任务边界减少全量端侧系统压力，却仍有算力、电量和模型更新成本。隐私取决于实际传输内容，不是只因端侧二字就自动保证。 示意：手机本地把最近浏览转成露营灯查询，服务器只查商品；若同时把完整行为日志上传，实际隐私路径就不再符合预期分工。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-recgpt-mobile-6c2409d1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d3538151a4afc483">RecGPT-Mobile 为什么把行为到 query 放到端侧，而检索仍留服务端？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecgpt-mobile">RecGPT-Mobile: On-Device Large Language Models for User Intent Understanding in Taobao Feed Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>端侧可少传原始行为并利用即时上下文，小量化模型生成意图，服务端继续维护大目录与检索。任务边界减少全量端侧系统压力，却仍有算力、电量和模型更新成本。隐私取决于实际传输内容，不是只因端侧二字就自动保证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>手机本地把最近浏览转成露营灯查询，服务器只查商品；若同时把完整行为日志上传，实际隐私路径就不再符合预期分工。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.04726">原论文</a> · <a href="../../../../reproductions/2605.04726-recgpt-mobile/">实现解读</a> · <a href="#qa-d3538151a4afc483">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recgpt-mobile" data-paper-title="RecGPT-Mobile: On-Device Large Language Models for User Intent Understanding in Taobao Feed Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RecGPT-Mobile: On-Device Large Language Models for User Intent Understanding in Taobao Feed Recommendation 搜广推与 LLM 应用 Alibaba / Taobao 2026-05-06 云端 LLM 能把点击、加购、收藏、购买等隐式行为翻译成显式搜索意图，但频繁上传行为并推理会增加成本、延迟和隐私风险。RecGPT-Mobile 把 Qwen3-0.6B 量化模型放到手机端，形成“本地收集行为→自适应构造 prompt→生成下一 query→服务端检索”的链路。训练数据由行为/搜索日志 60%、共购关系 20%、GPT 改写 15% 和人工标注 5% 组成；LoRA SFT 学习行为到 query 的映射。 Fidelity: 核心机制复现。实际执行 causal LM LoRA SFT、预算约束 adaptive prompt、意图漂移触发与 INT8 权重量化；私有数据和手机端系统缩小。本地模型是真实 causal LM 和 LoRA，不是类型分类 MLP；adaptive prompt、三项漂移公式和量化路径均执行。MovieLens 类型替代淘宝搜索 query，没有 GPT 改写、人工标注、生产检索和真机 fleet，故只验证方法链路与相对趋势。本地对照口径：基线为同一 SmolLM2-135M-Instruct 的零样本 intent completion；  llm-recommendation on-device intent-understanding serving-efficiency 搜广推 语义表征、用户知识与冷启动 RecGPT-Mobile 为什么只在联合漂移信号越过阈值时重新生成 query，而不是每次行为都触发？ 端侧推理虽减少行为上传，仍消耗电量和延迟。熵变化、集合重叠与分布散度共同判断意图是否实质变化，再按预算选择 prompt 组件，避免重复生成几乎相同的查询。生成结果交给服务端检索，所以端侧承担的是行为到意图的转换；漂移门控仍可能漏掉小幅但关键的新需求。 示意：连续浏览同类跑鞋不必每点一次都重跑模型；突然转向婴儿用品时，多种漂移指标共同变化才触发新查询。端侧给出意图后，服务器继续执行商品检索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-6d40e87b3bf547f6">RecGPT-Mobile 为什么只在联合漂移信号越过阈值时重新生成 query，而不是每次行为都触发？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecgpt-mobile">RecGPT-Mobile: On-Device Large Language Models for User Intent Understanding in Taobao Feed Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>端侧推理虽减少行为上传，仍消耗电量和延迟。熵变化、集合重叠与分布散度共同判断意图是否实质变化，再按预算选择 prompt 组件，避免重复生成几乎相同的查询。生成结果交给服务端检索，所以端侧承担的是行为到意图的转换；漂移门控仍可能漏掉小幅但关键的新需求。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>连续浏览同类跑鞋不必每点一次都重跑模型；突然转向婴儿用品时，多种漂移指标共同变化才触发新查询。端侧给出意图后，服务器继续执行商品检索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.04726">原论文</a> · <a href="../../../../reproductions/2605.04726-recgpt-mobile/">实现解读</a> · <a href="#qa-6d40e87b3bf547f6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recgpt-mobile" data-paper-title="RecGPT-Mobile: On-Device Large Language Models for User Intent Understanding in Taobao Feed Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RecGPT-Mobile: On-Device Large Language Models for User Intent Understanding in Taobao Feed Recommendation 搜广推与 LLM 应用 Alibaba / Taobao 2026-05-06 云端 LLM 能把点击、加购、收藏、购买等隐式行为翻译成显式搜索意图，但频繁上传行为并推理会增加成本、延迟和隐私风险。RecGPT-Mobile 把 Qwen3-0.6B 量化模型放到手机端，形成“本地收集行为→自适应构造 prompt→生成下一 query→服务端检索”的链路。训练数据由行为/搜索日志 60%、共购关系 20%、GPT 改写 15% 和人工标注 5% 组成；LoRA SFT 学习行为到 query 的映射。 Fidelity: 核心机制复现。实际执行 causal LM LoRA SFT、预算约束 adaptive prompt、意图漂移触发与 INT8 权重量化；私有数据和手机端系统缩小。本地模型是真实 causal LM 和 LoRA，不是类型分类 MLP；adaptive prompt、三项漂移公式和量化路径均执行。MovieLens 类型替代淘宝搜索 query，没有 GPT 改写、人工标注、生产检索和真机 fleet，故只验证方法链路与相对趋势。本地对照口径：基线为同一 SmolLM2-135M-Instruct 的零样本 intent completion；  llm-recommendation on-device intent-understanding serving-efficiency 搜广推 语义表征、用户知识与冷启动 INT8 存储量下降与 INT8 推理加速，为什么是不同证据？ 权重以八位保存可减少文件体积，但若运行时先反量化回浮点并用普通 kernel，延迟可能不降反升。真实量化计算需支持硬件和算子。来源 Mac 未启 INT8 linear，不能把序列化省一半写成手机速度提升一半。 示意：压缩文件更小但每次解压再计算，传输省了、计算没省；端侧用户感到的延迟还包含解量化和生成步骤。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-020a897cd156903d">INT8 存储量下降与 INT8 推理加速，为什么是不同证据？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecgpt-mobile">RecGPT-Mobile: On-Device Large Language Models for User Intent Understanding in Taobao Feed Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>权重以八位保存可减少文件体积，但若运行时先反量化回浮点并用普通 kernel，延迟可能不降反升。真实量化计算需支持硬件和算子。来源 Mac 未启 INT8 linear，不能把序列化省一半写成手机速度提升一半。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>压缩文件更小但每次解压再计算，传输省了、计算没省；端侧用户感到的延迟还包含解量化和生成步骤。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.04726">原论文</a> · <a href="../../../../reproductions/2605.04726-recgpt-mobile/">实现解读</a> · <a href="#qa-020a897cd156903d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recgpt-mobile" data-paper-title="RecGPT-Mobile: On-Device Large Language Models for User Intent Understanding in Taobao Feed Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RecGPT-Mobile: On-Device Large Language Models for User Intent Understanding in Taobao Feed Recommendation 搜广推与 LLM 应用 Alibaba / Taobao 2026-05-06 云端 LLM 能把点击、加购、收藏、购买等隐式行为翻译成显式搜索意图，但频繁上传行为并推理会增加成本、延迟和隐私风险。RecGPT-Mobile 把 Qwen3-0.6B 量化模型放到手机端，形成“本地收集行为→自适应构造 prompt→生成下一 query→服务端检索”的链路。训练数据由行为/搜索日志 60%、共购关系 20%、GPT 改写 15% 和人工标注 5% 组成；LoRA SFT 学习行为到 query 的映射。 Fidelity: 核心机制复现。实际执行 causal LM LoRA SFT、预算约束 adaptive prompt、意图漂移触发与 INT8 权重量化；私有数据和手机端系统缩小。本地模型是真实 causal LM 和 LoRA，不是类型分类 MLP；adaptive prompt、三项漂移公式和量化路径均执行。MovieLens 类型替代淘宝搜索 query，没有 GPT 改写、人工标注、生产检索和真机 fleet，故只验证方法链路与相对趋势。本地对照口径：基线为同一 SmolLM2-135M-Instruct 的零样本 intent completion；  llm-recommendation on-device intent-understanding serving-efficiency 搜广推 语义表征、用户知识与冷启动 RecGPT-Mobile 的 prompt 组件预算与漂移触发应如何分别检查？ 组件按边际收益和 token 上限加入，触发则由熵、Jaccard、JS 组合比较前后意图，两者控制单次成本和调用频率。不能用测试下一 query 来决定何时触发或加组件。本地小样本 semantic accuracy 不等于真实端侧交互成功率。 示意：某次需要重算意图，不代表可以无限长 prompt；即使 prompt 很短，意图未变化也应复用旧结果，两个门槛不能合并成一个开关。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7d7a9b183c9fd8b1">RecGPT-Mobile 的 prompt 组件预算与漂移触发应如何分别检查？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecgpt-mobile">RecGPT-Mobile: On-Device Large Language Models for User Intent Understanding in Taobao Feed Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>组件按边际收益和 token 上限加入，触发则由熵、Jaccard、JS 组合比较前后意图，两者控制单次成本和调用频率。不能用测试下一 query 来决定何时触发或加组件。本地小样本 semantic accuracy 不等于真实端侧交互成功率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某次需要重算意图，不代表可以无限长 prompt；即使 prompt 很短，意图未变化也应复用旧结果，两个门槛不能合并成一个开关。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.04726">原论文</a> · <a href="../../../../reproductions/2605.04726-recgpt-mobile/">实现解读</a> · <a href="#qa-7d7a9b183c9fd8b1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:adasid" data-paper-title="Beyond Static Collision Handling: Adaptive Semantic ID Learning for Multimodal Recommendation at Industrial Scale" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Beyond Static Collision Handling: Adaptive Semantic ID Learning for Multimodal Recommendation at Industrial Scale 搜广推与 LLM 应用 University of Electronic Science and Technology of China / Kuaishou 2026-04-26 按碰撞负载、语义相容性和训练阶段动态放松 SID 重叠约束，避免把所有碰撞等价惩罚。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 adasid 核心机制，相对 NDCG@10 -6.30%。  semantic-id multimodal-recommendation retrieval 搜广推 语义表征、用户知识与冷启动 AdaSID 所说的 SID 重叠为什么不一定都是坏事？ 语义相近物品共享部分编码可以迁移知识，完全排斥会破坏有用邻近；真正有害的是服务区分或学习负载受影响的碰撞。方法依据负载、语义相容性和训练阶段调节惩罚，让码空间在共享与可辨识之间取舍，而不是追求所有物品都远离。 示意：两件同款不同颜色可共享粗码，但库存不同仍需在细码区分；把连粗码都强行推开，反而会丢掉它们共同的服装语义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-adasid-04146a65" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-604711a6c316538a">AdaSID 所说的 SID 重叠为什么不一定都是坏事？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aadasid">Beyond Static Collision Handling: Adaptive Semantic ID Learning for Multimodal Recommendation at Industrial Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Electronic Science and Technology of China / Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语义相近物品共享部分编码可以迁移知识，完全排斥会破坏有用邻近；真正有害的是服务区分或学习负载受影响的碰撞。方法依据负载、语义相容性和训练阶段调节惩罚，让码空间在共享与可辨识之间取舍，而不是追求所有物品都远离。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两件同款不同颜色可共享粗码，但库存不同仍需在细码区分；把连粗码都强行推开，反而会丢掉它们共同的服装语义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.23522">原论文</a> · <a href="../../../../reproductions/2604.23522-adasid/">实现解读</a> · <a href="#qa-604711a6c316538a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:adasid" data-paper-title="Beyond Static Collision Handling: Adaptive Semantic ID Learning for Multimodal Recommendation at Industrial Scale" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Beyond Static Collision Handling: Adaptive Semantic ID Learning for Multimodal Recommendation at Industrial Scale 搜广推与 LLM 应用 University of Electronic Science and Technology of China / Kuaishou 2026-04-26 按碰撞负载、语义相容性和训练阶段动态放松 SID 重叠约束，避免把所有碰撞等价惩罚。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 adasid 核心机制，相对 NDCG@10 -6.30%。  semantic-id multimodal-recommendation retrieval 搜广推 语义表征、用户知识与冷启动 为什么AdaSID不把所有共享语义ID的物品都施加同样的碰撞惩罚？ 同码重叠有时表示有用的语义共享，有时才是无法区分的拥塞。AdaSID依据碰撞负载、物品语义相容性和训练阶段改变约束强度，在保留相关物品共性与区分不相关物品之间取得平衡。统一强惩罚可能把本来应靠近的内容硬拉开，统一放松则会掩盖高负载冲突。 示意：两款相近跑鞋共享粗层码可能合理，跑鞋与烤箱共享热门码却可能是拥塞；训练早期和码本趋稳后也未必该用相同惩罚强度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-eb18b863121823e9">为什么AdaSID不把所有共享语义ID的物品都施加同样的碰撞惩罚？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aadasid">Beyond Static Collision Handling: Adaptive Semantic ID Learning for Multimodal Recommendation at Industrial Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Electronic Science and Technology of China / Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同码重叠有时表示有用的语义共享，有时才是无法区分的拥塞。AdaSID依据碰撞负载、物品语义相容性和训练阶段改变约束强度，在保留相关物品共性与区分不相关物品之间取得平衡。统一强惩罚可能把本来应靠近的内容硬拉开，统一放松则会掩盖高负载冲突。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两款相近跑鞋共享粗层码可能合理，跑鞋与烤箱共享热门码却可能是拥塞；训练早期和码本趋稳后也未必该用相同惩罚强度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.23522">原论文</a> · <a href="../../../../reproductions/2604.23522-adasid/">实现解读</a> · <a href="#qa-eb18b863121823e9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:adasid" data-paper-title="Beyond Static Collision Handling: Adaptive Semantic ID Learning for Multimodal Recommendation at Industrial Scale" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Beyond Static Collision Handling: Adaptive Semantic ID Learning for Multimodal Recommendation at Industrial Scale 搜广推与 LLM 应用 University of Electronic Science and Technology of China / Kuaishou 2026-04-26 按碰撞负载、语义相容性和训练阶段动态放松 SID 重叠约束，避免把所有碰撞等价惩罚。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 adasid 核心机制，相对 NDCG@10 -6.30%。  semantic-id multimodal-recommendation retrieval 搜广推 语义表征、用户知识与冷启动 AdaSID 与固定系数的碰撞损失相比，多出的自适应项改变了什么？ 固定损失把所有碰撞在整个训练期视为同样严重。自适应系数将碰撞对和训练时点作为条件，允许早期学习语义结构、后期再强化需要区分的关系。它增加调度灵活性，也增加校准复杂度；机制上的优势不能代替相同预算的实际验证。 示意：训练早期两本同主题书共码可先保留，码本成形后再对高负载且需区分的那一对加重惩罚，而不是全程使用同一个排斥强度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5e97e8e859bc568b">AdaSID 与固定系数的碰撞损失相比，多出的自适应项改变了什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aadasid">Beyond Static Collision Handling: Adaptive Semantic ID Learning for Multimodal Recommendation at Industrial Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Electronic Science and Technology of China / Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定损失把所有碰撞在整个训练期视为同样严重。自适应系数将碰撞对和训练时点作为条件，允许早期学习语义结构、后期再强化需要区分的关系。它增加调度灵活性，也增加校准复杂度；机制上的优势不能代替相同预算的实际验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练早期两本同主题书共码可先保留，码本成形后再对高负载且需区分的那一对加重惩罚，而不是全程使用同一个排斥强度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.23522">原论文</a> · <a href="../../../../reproductions/2604.23522-adasid/">实现解读</a> · <a href="#qa-5e97e8e859bc568b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:adasid" data-paper-title="Beyond Static Collision Handling: Adaptive Semantic ID Learning for Multimodal Recommendation at Industrial Scale" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Beyond Static Collision Handling: Adaptive Semantic ID Learning for Multimodal Recommendation at Industrial Scale 搜广推与 LLM 应用 University of Electronic Science and Technology of China / Kuaishou 2026-04-26 按碰撞负载、语义相容性和训练阶段动态放松 SID 重叠约束，避免把所有碰撞等价惩罚。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 adasid 核心机制，相对 NDCG@10 -6.30%。  semantic-id multimodal-recommendation retrieval 搜广推 语义表征、用户知识与冷启动 AdaSID 的碰撞系数应作为单一标量还是逐物品对、逐阶段的量？ 来源写成 λij(t)，意味着系数由碰撞负载、两物品语义关系与训练阶段共同决定，应用到对应重叠项后再求和。若实现退化成一个常数，只保留了固定碰撞正则，丢掉定义性自适应条件；评估也要记录调度口径。 示意：高负载的鞋码碰撞和低负载的书码碰撞可以使用不同系数；进入后期后再更新，不能给整个批次统一乘一个固定常数就称为自适应。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6575b5aeeca1f0cc">AdaSID 的碰撞系数应作为单一标量还是逐物品对、逐阶段的量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aadasid">Beyond Static Collision Handling: Adaptive Semantic ID Learning for Multimodal Recommendation at Industrial Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Electronic Science and Technology of China / Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>来源写成 λij(t)，意味着系数由碰撞负载、两物品语义关系与训练阶段共同决定，应用到对应重叠项后再求和。若实现退化成一个常数，只保留了固定碰撞正则，丢掉定义性自适应条件；评估也要记录调度口径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>高负载的鞋码碰撞和低负载的书码碰撞可以使用不同系数；进入后期后再更新，不能给整个批次统一乘一个固定常数就称为自适应。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.23522">原论文</a> · <a href="../../../../reproductions/2604.23522-adasid/">实现解读</a> · <a href="#qa-6575b5aeeca1f0cc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:marc" data-paper-title="Modular Representation Compression: Adapting LLMs for Efficient and Effective Recommendations" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Modular Representation Compression: Adapting LLMs for Efficient and Effective Recommendations 搜广推与 LLM 应用 Shanghai Jiao Tong University 2026-04-20 论文发现 LLM 的中间层在推荐压缩后可能优于末层（MRA）。MARC 将压缩模块与任务适配模块显式拆开，并用信息约束解耦代理任务和推荐任务，保留任务相关信息的同时降低表征维度。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04693，相对变化 -13.11%。本地代理目标与论文生产任务不同，不能外推线上 lift。  llm-recommendation representation-compression modular-learning 搜广推 语义表征、用户知识与冷启动 MARC 为什么可能选择 LLM 中间层，而不是默认最后层表示最好？ 末层更贴近预训输出目标，未必最适合推荐压缩，中间层可能保留更可迁移结构。MRA 的观察促使压缩与适配分别设计，去除代理任务干扰同时保留推荐相关信息。层选择仍应依验证，不是中间层普遍优于末层的定理。 示意：语言末层擅长预测下个词，却可能忽略区分两类用户的细节；某中间层更适合小推荐向量，但需实际任务验证而非凭层号猜。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-marc-216b86ce" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-23b84a11d274b3f0">MARC 为什么可能选择 LLM 中间层，而不是默认最后层表示最好？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amarc">Modular Representation Compression: Adapting LLMs for Efficient and Effective Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Jiao Tong University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>末层更贴近预训输出目标，未必最适合推荐压缩，中间层可能保留更可迁移结构。MRA 的观察促使压缩与适配分别设计，去除代理任务干扰同时保留推荐相关信息。层选择仍应依验证，不是中间层普遍优于末层的定理。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>语言末层擅长预测下个词，却可能忽略区分两类用户的细节；某中间层更适合小推荐向量，但需实际任务验证而非凭层号猜。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.18146">原论文</a> · <a href="../../../../reproductions/2604.18146-marc/">实现解读</a> · <a href="#qa-23b84a11d274b3f0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:marc" data-paper-title="Modular Representation Compression: Adapting LLMs for Efficient and Effective Recommendations" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Modular Representation Compression: Adapting LLMs for Efficient and Effective Recommendations 搜广推与 LLM 应用 Shanghai Jiao Tong University 2026-04-20 论文发现 LLM 的中间层在推荐压缩后可能优于末层（MRA）。MARC 将压缩模块与任务适配模块显式拆开，并用信息约束解耦代理任务和推荐任务，保留任务相关信息的同时降低表征维度。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04693，相对变化 -13.11%。本地代理目标与论文生产任务不同，不能外推线上 lift。  llm-recommendation representation-compression modular-learning 搜广推 语义表征、用户知识与冷启动 MARC为什么把表征压缩与推荐适配拆开，并可能选择LLM中间层？ 末层偏向原语言任务，中间层有时包含更适合压缩的通用特征；但压缩保留的信息与推荐所需信息并不完全相同。分开两个模块并施加信息约束，能分别管理维度成本与任务选择，减少代理任务牵着推荐目标走。中间层优势属于需要检验的经验现象，不能默认对所有模型和数据成立。 示意：末层很擅长预测接下来的词，中间层却更容易保留商品用途；若只追重建原向量，可把与购买偏好无关的语言信息一起昂贵地保存。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-e7980095d4e002eb">MARC为什么把表征压缩与推荐适配拆开，并可能选择LLM中间层？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amarc">Modular Representation Compression: Adapting LLMs for Efficient and Effective Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Jiao Tong University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>末层偏向原语言任务，中间层有时包含更适合压缩的通用特征；但压缩保留的信息与推荐所需信息并不完全相同。分开两个模块并施加信息约束，能分别管理维度成本与任务选择，减少代理任务牵着推荐目标走。中间层优势属于需要检验的经验现象，不能默认对所有模型和数据成立。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>末层很擅长预测接下来的词，中间层却更容易保留商品用途；若只追重建原向量，可把与购买偏好无关的语言信息一起昂贵地保存。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.18146">原论文</a> · <a href="../../../../reproductions/2604.18146-marc/">实现解读</a> · <a href="#qa-e7980095d4e002eb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:marc" data-paper-title="Modular Representation Compression: Adapting LLMs for Efficient and Effective Recommendations" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Modular Representation Compression: Adapting LLMs for Efficient and Effective Recommendations 搜广推与 LLM 应用 Shanghai Jiao Tong University 2026-04-20 论文发现 LLM 的中间层在推荐压缩后可能优于末层（MRA）。MARC 将压缩模块与任务适配模块显式拆开，并用信息约束解耦代理任务和推荐任务，保留任务相关信息的同时降低表征维度。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04693，相对变化 -13.11%。本地代理目标与论文生产任务不同，不能外推线上 lift。  llm-recommendation representation-compression modular-learning 搜广推 语义表征、用户知识与冷启动 MARC 的压缩与适配分离，相比一个线性降维器承担全部任务，有何好处与风险？ 单一投影同时丢信息与学推荐易混淆目标，分开可检查压缩损失和任务适配各自作用。模块增加也带来目标耦合与选择空间，错误剔除所谓 nuisance 仍可能删有用信号。来源公开代理为负，不支持仅凭信息约束宣称泛化更好。 示意：先减少与内容预训特有风格相关的方向，再学用户匹配；若风格恰是用户偏好，去干扰步骤也可能错删，因此需要两阶段消融。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c62caff06e1cb6d1">MARC 的压缩与适配分离，相比一个线性降维器承担全部任务，有何好处与风险？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amarc">Modular Representation Compression: Adapting LLMs for Efficient and Effective Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Jiao Tong University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单一投影同时丢信息与学推荐易混淆目标，分开可检查压缩损失和任务适配各自作用。模块增加也带来目标耦合与选择空间，错误剔除所谓 nuisance 仍可能删有用信号。来源公开代理为负，不支持仅凭信息约束宣称泛化更好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先减少与内容预训特有风格相关的方向，再学用户匹配；若风格恰是用户偏好，去干扰步骤也可能错删，因此需要两阶段消融。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.18146">原论文</a> · <a href="../../../../reproductions/2604.18146-marc/">实现解读</a> · <a href="#qa-c62caff06e1cb6d1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:marc" data-paper-title="Modular Representation Compression: Adapting LLMs for Efficient and Effective Recommendations" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Modular Representation Compression: Adapting LLMs for Efficient and Effective Recommendations 搜广推与 LLM 应用 Shanghai Jiao Tong University 2026-04-20 论文发现 LLM 的中间层在推荐压缩后可能优于末层（MRA）。MARC 将压缩模块与任务适配模块显式拆开，并用信息约束解耦代理任务和推荐任务，保留任务相关信息的同时降低表征维度。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04693，相对变化 -13.11%。本地代理目标与论文生产任务不同，不能外推线上 lift。  llm-recommendation representation-compression modular-learning 搜广推 语义表征、用户知识与冷启动 MARC 的中层选择与 nuisance 投影，怎样防止验证和测试混用？ 层号、维度及被去除方向都是模型选择，应由训练估计和验证确定后冻结，测试只报告。投影应匹配所选 hidden state 空间，不能用末层矩阵套中层而无说明。本地固定打分代理若未训练完整信息目标，结论需按实际范围限定。 示意：测试看哪层 NDCG 最高再宣布该层最佳，会把 test 变成调参；应先选层，再用独立目标检验压缩是否真有迁移价值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-db89084985cb4dc0">MARC 的中层选择与 nuisance 投影，怎样防止验证和测试混用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amarc">Modular Representation Compression: Adapting LLMs for Efficient and Effective Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Jiao Tong University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>层号、维度及被去除方向都是模型选择，应由训练估计和验证确定后冻结，测试只报告。投影应匹配所选 hidden state 空间，不能用末层矩阵套中层而无说明。本地固定打分代理若未训练完整信息目标，结论需按实际范围限定。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>测试看哪层 NDCG 最高再宣布该层最佳，会把 test 变成调参；应先选层，再用独立目标检验压缩是否真有迁移价值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.18146">原论文</a> · <a href="../../../../reproductions/2604.18146-marc/">实现解读</a> · <a href="#qa-db89084985cb4dc0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:lwgr" data-paper-title="LWGR: Lagrangian-Constrained Personalized World Knowledge for Generative Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="LWGR: Lagrangian-Constrained Personalized World Knowledge for Generative Recommendation 搜广推与 LLM 应用 Alibaba International / CAS 2026-04-16 固定人工 prompt 提取的 LLM 知识既不能表达用户兴趣异质性，也可能与行为信号冲突。LWGR 将用户上下文切成多个子空间，每个子空间从独立 codebook 选择 codeword，形成可端到端学习的个性化 soft instruction；soft tokens 与历史商品文本共同通过 LLM，得到用户级 world knowledge。生成式推荐 decoder 在 BOS 处 cross-attend 这些知识，同时用相对冻结 reference 的置信度退化约束控制有害融合。 因此本地只验证实现和梯度路径，未验证约束有效性或论文准确率收益。Fidelity: 完整核心链路。本地实际执行 parallel codebook、IBQ straight-through、用户 soft instruction 进入真实冻结 causal LLM、BOS cross-attention、冻结生成式 reference，以及逐步 primal-dual 更新。未用静态文本向量替代个性化 LLM 前向。使用真实 SmolLM2-135M 前向，soft instruction 的梯度穿过冻结 LLM 回到 codebook；未用预计算常量冒充该步骤。  generative-recommendation soft-prompt world-knowledge lagrangian 搜广推 语义表征、用户知识与冷启动 LWGR 的 soft instruction 为什么能表达用户差异，而不只是另一段人工提示？ 用户上下文分子空间，在独立码本选择 codeword，形成可端到端优化的软 token，和历史文本共同产生用户知识。提示参数可随推荐监督改变，不只依人工措辞。软指令仍受码本容量与训练支持限制，不保证对应可读语言意图。 示意：摄影初学者与专业用户可选择不同软 token 组合，即使人工提示都写“分析兴趣”，模型仍有可学习的个性化接口。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-lwgr-831cc9dc" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b637c222009ec19f">LWGR 的 soft instruction 为什么能表达用户差异，而不只是另一段人工提示？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alwgr">LWGR: Lagrangian-Constrained Personalized World Knowledge for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International / CAS</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用户上下文分子空间，在独立码本选择 codeword，形成可端到端优化的软 token，和历史文本共同产生用户知识。提示参数可随推荐监督改变，不只依人工措辞。软指令仍受码本容量与训练支持限制，不保证对应可读语言意图。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>摄影初学者与专业用户可选择不同软 token 组合，即使人工提示都写“分析兴趣”，模型仍有可学习的个性化接口。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.18771">原论文</a> · <a href="../../../../reproductions/2605.18771-lwgr/">实现解读</a> · <a href="#qa-b637c222009ec19f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:lwgr" data-paper-title="LWGR: Lagrangian-Constrained Personalized World Knowledge for Generative Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="LWGR: Lagrangian-Constrained Personalized World Knowledge for Generative Recommendation 搜广推与 LLM 应用 Alibaba International / CAS 2026-04-16 固定人工 prompt 提取的 LLM 知识既不能表达用户兴趣异质性，也可能与行为信号冲突。LWGR 将用户上下文切成多个子空间，每个子空间从独立 codebook 选择 codeword，形成可端到端学习的个性化 soft instruction；soft tokens 与历史商品文本共同通过 LLM，得到用户级 world knowledge。生成式推荐 decoder 在 BOS 处 cross-attend 这些知识，同时用相对冻结 reference 的置信度退化约束控制有害融合。 因此本地只验证实现和梯度路径，未验证约束有效性或论文准确率收益。Fidelity: 完整核心链路。本地实际执行 parallel codebook、IBQ straight-through、用户 soft instruction 进入真实冻结 causal LLM、BOS cross-attention、冻结生成式 reference，以及逐步 primal-dual 更新。未用静态文本向量替代个性化 LLM 前向。使用真实 SmolLM2-135M 前向，soft instruction 的梯度穿过冻结 LLM 回到 codebook；未用预计算常量冒充该步骤。  generative-recommendation soft-prompt world-knowledge lagrangian 搜广推 语义表征、用户知识与冷启动 LWGR为什么学习个性化soft instruction，还要约束相对冻结reference的退化？ 固定prompt难以适应不同用户，分子空间codebook生成可训练soft tokens，让外部知识提取随偏好变化。但LLM知识也可能与行为模型冲突，冻结reference提供比较锚点，用置信度退化约束限制有害融合；nearline预计算控制服务成本。学到prompt并不保证知识真实或比行为信号更可靠。 示意：同样喜欢旅行，有人关注低价、有人关注摄影，soft instruction可引出不同知识；若新知识使既有可靠候选明显降分，约束应阻止无条件覆盖旧模型。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-e153cabf62c29685">LWGR为什么学习个性化soft instruction，还要约束相对冻结reference的退化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alwgr">LWGR: Lagrangian-Constrained Personalized World Knowledge for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International / CAS</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定prompt难以适应不同用户，分子空间codebook生成可训练soft tokens，让外部知识提取随偏好变化。但LLM知识也可能与行为模型冲突，冻结reference提供比较锚点，用置信度退化约束限制有害融合；nearline预计算控制服务成本。学到prompt并不保证知识真实或比行为信号更可靠。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同样喜欢旅行，有人关注低价、有人关注摄影，soft instruction可引出不同知识；若新知识使既有可靠候选明显降分，约束应阻止无条件覆盖旧模型。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.18771">原论文</a> · <a href="../../../../reproductions/2605.18771-lwgr/">实现解读</a> · <a href="#qa-e153cabf62c29685">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:lwgr" data-paper-title="LWGR: Lagrangian-Constrained Personalized World Knowledge for Generative Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="LWGR: Lagrangian-Constrained Personalized World Knowledge for Generative Recommendation 搜广推与 LLM 应用 Alibaba International / CAS 2026-04-16 固定人工 prompt 提取的 LLM 知识既不能表达用户兴趣异质性，也可能与行为信号冲突。LWGR 将用户上下文切成多个子空间，每个子空间从独立 codebook 选择 codeword，形成可端到端学习的个性化 soft instruction；soft tokens 与历史商品文本共同通过 LLM，得到用户级 world knowledge。生成式推荐 decoder 在 BOS 处 cross-attend 这些知识，同时用相对冻结 reference 的置信度退化约束控制有害融合。 因此本地只验证实现和梯度路径，未验证约束有效性或论文准确率收益。Fidelity: 完整核心链路。本地实际执行 parallel codebook、IBQ straight-through、用户 soft instruction 进入真实冻结 causal LLM、BOS cross-attention、冻结生成式 reference，以及逐步 primal-dual 更新。未用静态文本向量替代个性化 LLM 前向。使用真实 SmolLM2-135M 前向，soft instruction 的梯度穿过冻结 LLM 回到 codebook；未用预计算常量冒充该步骤。  generative-recommendation soft-prompt world-knowledge lagrangian 搜广推 语义表征、用户知识与冷启动 LWGR 的 reference 置信度退化约束与普通 KL，相比保护什么量？ 来源约束正目标平均 token log-prob 相对参考的下降超容忍部分，关注有害融合导致的置信损失；KL 则衡量整个分布偏离，两者不等价。约束需要实际满足而非只更新乘子，本地 λ 变化但退化未改善，不能宣称保护有效。 示意：模型可把概率移给另一合理候选使 KL 增大，却未严重损害原目标；反过来原目标下降很大时，单边退化约束才明确施压。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a7040336605d65fd">LWGR 的 reference 置信度退化约束与普通 KL，相比保护什么量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alwgr">LWGR: Lagrangian-Constrained Personalized World Knowledge for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International / CAS</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>来源约束正目标平均 token log-prob 相对参考的下降超容忍部分，关注有害融合导致的置信损失；KL 则衡量整个分布偏离，两者不等价。约束需要实际满足而非只更新乘子，本地 λ 变化但退化未改善，不能宣称保护有效。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型可把概率移给另一合理候选使 KL 增大，却未严重损害原目标；反过来原目标下降很大时，单边退化约束才明确施压。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.18771">原论文</a> · <a href="../../../../reproductions/2605.18771-lwgr/">实现解读</a> · <a href="#qa-a7040336605d65fd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:lwgr" data-paper-title="LWGR: Lagrangian-Constrained Personalized World Knowledge for Generative Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="LWGR: Lagrangian-Constrained Personalized World Knowledge for Generative Recommendation 搜广推与 LLM 应用 Alibaba International / CAS 2026-04-16 固定人工 prompt 提取的 LLM 知识既不能表达用户兴趣异质性，也可能与行为信号冲突。LWGR 将用户上下文切成多个子空间，每个子空间从独立 codebook 选择 codeword，形成可端到端学习的个性化 soft instruction；soft tokens 与历史商品文本共同通过 LLM，得到用户级 world knowledge。生成式推荐 decoder 在 BOS 处 cross-attend 这些知识，同时用相对冻结 reference 的置信度退化约束控制有害融合。 因此本地只验证实现和梯度路径，未验证约束有效性或论文准确率收益。Fidelity: 完整核心链路。本地实际执行 parallel codebook、IBQ straight-through、用户 soft instruction 进入真实冻结 causal LLM、BOS cross-attention、冻结生成式 reference，以及逐步 primal-dual 更新。未用静态文本向量替代个性化 LLM 前向。使用真实 SmolLM2-135M 前向，soft instruction 的梯度穿过冻结 LLM 回到 codebook；未用预计算常量冒充该步骤。  generative-recommendation soft-prompt world-knowledge lagrangian 搜广推 语义表征、用户知识与冷启动 LWGR 的 straight-through code 选择与 dual update，分别应怎样检查？ 前向用硬码而反向保留软分布梯度，需验证 soft-instruction 参数实际更新；λ 则按 C−ε 更新并投到非负。乘子变大只说明违反约束产生响应，不证明已满足。冻结 reference、BOS 融合和 nearline 缓存是不同接口，不能互相替代。 示意：C 仍高于容限而 λ 稍升，应报告约束未达成；若硬索引彻底切断梯度，模型也没真正学习个性化指令，即使代码能选码。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7c6d7ced9871671c">LWGR 的 straight-through code 选择与 dual update，分别应怎样检查？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alwgr">LWGR: Lagrangian-Constrained Personalized World Knowledge for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International / CAS</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前向用硬码而反向保留软分布梯度，需验证 soft-instruction 参数实际更新；λ 则按 C−ε 更新并投到非负。乘子变大只说明违反约束产生响应，不证明已满足。冻结 reference、BOS 融合和 nearline 缓存是不同接口，不能互相替代。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>C 仍高于容限而 λ 稍升，应报告约束未达成；若硬索引彻底切断梯度，模型也没真正学习个性化指令，即使代码能选码。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.18771">原论文</a> · <a href="../../../../reproductions/2605.18771-lwgr/">实现解读</a> · <a href="#qa-7c6d7ced9871671c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sid-coord" data-paper-title="SID-Coord: Coordinating Semantic IDs for ID-based Ranking in Short-Video Search" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SID-Coord: Coordinating Semantic IDs for ID-based Ranking in Short-Video Search 搜广推与 LLM 应用 Kuaishou Technology 2026-04-12 SID-Coord 不把语义信号仅作为普通稠密特征，而是构造多层离散 SID；再通过层级融合、目标感知 HID–SID 门控和历史兴趣对齐，在头部物品记忆与长尾泛化之间逐样本协调。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04970，相对变化 -7.97%。本地代理目标与论文生产任务不同，不能外推线上 lift。  short-video-search semantic-id long-tail-ranking 搜广推 语义表征、用户知识与冷启动 SID-Coord为什么同时保留HID与SID？ HID擅长头部记忆，分层SID帮助语义共享和长尾泛化；按目标门控及历史对齐逐样本协调，而非一律换成语义表示。两者贡献随数据密度变化。 例如热门物品可依ID经验，新物品更多依赖相近语义码。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-sid-coord-811302bf" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-540fd173d5fef393">SID-Coord为什么同时保留HID与SID？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asid-coord">SID-Coord: Coordinating Semantic IDs for ID-based Ranking in Short-Video Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>HID擅长头部记忆，分层SID帮助语义共享和长尾泛化；按目标门控及历史对齐逐样本协调，而非一律换成语义表示。两者贡献随数据密度变化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如热门物品可依ID经验，新物品更多依赖相近语义码。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.10471">原论文</a> · <a href="../../../../reproductions/2604.10471-sid-coord/">实现解读</a> · <a href="#qa-540fd173d5fef393">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sid-coord" data-paper-title="SID-Coord: Coordinating Semantic IDs for ID-based Ranking in Short-Video Search" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SID-Coord: Coordinating Semantic IDs for ID-based Ranking in Short-Video Search 搜广推与 LLM 应用 Kuaishou Technology 2026-04-12 SID-Coord 不把语义信号仅作为普通稠密特征，而是构造多层离散 SID；再通过层级融合、目标感知 HID–SID 门控和历史兴趣对齐，在头部物品记忆与长尾泛化之间逐样本协调。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04970，相对变化 -7.97%。本地代理目标与论文生产任务不同，不能外推线上 lift。  short-video-search semantic-id long-tail-ranking 搜广推 语义表征、用户知识与冷启动 SID-Coord 为什么让 HID 与多层 SID 的融合 gate 依赖目标，而不是固定比例相加？ 头部物品的哈希 ID 有充分行为记忆，长尾物品更需要语义码共享知识，固定比例无法兼顾每个样本。目标感知 gate 决定两类信号的使用程度，多层融合保留粗细语义，历史对齐再连接用户兴趣。门控是在两种信息来源间协调，不代表 SID 能替代所有记忆，也不能保证每个长尾样本都会受益。 示意：热门电影已有大量点击，评分可多用 ID 记忆；刚上线电影行为少，更多依赖主题与风格 SID。即使同一用户，两种候选也可使用不同融合比例。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-d6262c1fa258fc52">SID-Coord 为什么让 HID 与多层 SID 的融合 gate 依赖目标，而不是固定比例相加？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asid-coord">SID-Coord: Coordinating Semantic IDs for ID-based Ranking in Short-Video Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>头部物品的哈希 ID 有充分行为记忆，长尾物品更需要语义码共享知识，固定比例无法兼顾每个样本。目标感知 gate 决定两类信号的使用程度，多层融合保留粗细语义，历史对齐再连接用户兴趣。门控是在两种信息来源间协调，不代表 SID 能替代所有记忆，也不能保证每个长尾样本都会受益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>热门电影已有大量点击，评分可多用 ID 记忆；刚上线电影行为少，更多依赖主题与风格 SID。即使同一用户，两种候选也可使用不同融合比例。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.10471">原论文</a> · <a href="../../../../reproductions/2604.10471-sid-coord/">实现解读</a> · <a href="#qa-d6262c1fa258fc52">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sid-coord" data-paper-title="SID-Coord: Coordinating Semantic IDs for ID-based Ranking in Short-Video Search" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SID-Coord: Coordinating Semantic IDs for ID-based Ranking in Short-Video Search 搜广推与 LLM 应用 Kuaishou Technology 2026-04-12 SID-Coord 不把语义信号仅作为普通稠密特征，而是构造多层离散 SID；再通过层级融合、目标感知 HID–SID 门控和历史兴趣对齐，在头部物品记忆与长尾泛化之间逐样本协调。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04970，相对变化 -7.97%。本地代理目标与论文生产任务不同，不能外推线上 lift。  short-video-search semantic-id long-tail-ranking 搜广推 语义表征、用户知识与冷启动 SID-Coord的层级权重α与HID–SID样本gate，是同一个混合轴吗？ 不是。α在同一物品的多级SID之间分配贡献，gate在该样本的HID记忆与SID语义分支之间协调。把两者折成一个常数会同时抹掉层级与样本差异；它们虽都叫权重，却作用于不同信息来源和张量维度。 教学例子：先决定粗细两级语义怎样组合，再决定这份语义与HID记忆如何取舍，是两次不同的加权。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-24d82f6edd335d8c">SID-Coord的层级权重α与HID–SID样本gate，是同一个混合轴吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asid-coord">SID-Coord: Coordinating Semantic IDs for ID-based Ranking in Short-Video Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。α在同一物品的多级SID之间分配贡献，gate在该样本的HID记忆与SID语义分支之间协调。把两者折成一个常数会同时抹掉层级与样本差异；它们虽都叫权重，却作用于不同信息来源和张量维度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先决定粗细两级语义怎样组合，再决定这份语义与HID记忆如何取舍，是两次不同的加权。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.10471">原论文</a> · <a href="../../../../reproductions/2604.10471-sid-coord/">实现解读</a> · <a href="#qa-24d82f6edd335d8c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sid-coord" data-paper-title="SID-Coord: Coordinating Semantic IDs for ID-based Ranking in Short-Video Search" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SID-Coord: Coordinating Semantic IDs for ID-based Ranking in Short-Video Search 搜广推与 LLM 应用 Kuaishou Technology 2026-04-12 SID-Coord 不把语义信号仅作为普通稠密特征，而是构造多层离散 SID；再通过层级融合、目标感知 HID–SID 门控和历史兴趣对齐，在头部物品记忆与长尾泛化之间逐样本协调。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04970，相对变化 -7.97%。本地代理目标与论文生产任务不同，不能外推线上 lift。  short-video-search semantic-id long-tail-ranking 搜广推 语义表征、用户知识与冷启动 SID-Coord的分层α和样本gate需怎样对齐？ 层权重对应同一物品各级SID，gate对应当前用户目标对，不能混广播成全批常数。当前MovieLens代理未复刻生产语义码和线上流量，公开变化不等同原文业务增益。 例如把候选A的细码分配给B，形状相同仍会造成语义错位。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-9f543dce94b8b1e6">SID-Coord的分层α和样本gate需怎样对齐？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asid-coord">SID-Coord: Coordinating Semantic IDs for ID-based Ranking in Short-Video Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>层权重对应同一物品各级SID，gate对应当前用户目标对，不能混广播成全批常数。当前MovieLens代理未复刻生产语义码和线上流量，公开变化不等同原文业务增益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把候选A的细码分配给B，形状相同仍会造成语义错位。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.10471">原论文</a> · <a href="../../../../reproductions/2604.10471-sid-coord/">实现解读</a> · <a href="#qa-9f543dce94b8b1e6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cross-domain-kd" data-paper-title="Zero-shot Cross-domain Knowledge Distillation: A Case study on YouTube Music" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Zero-shot Cross-domain Knowledge Distillation: A Case study on YouTube Music 搜广推与 LLM 应用 Google / YouTube 2026-03-30 低流量产品无力训练大型专用 teacher。论文直接把数据丰富的 YouTube 多任务 teacher 应用于 YouTube Music 样本，把 serving task 与辅助 task logits 蒸馏到小模型，不要求源域数据或匹配的界面特征。 Fidelity: 核心机制复现。源域大 teacher、目标域小 student、目标样本上的 zero-shot logits 和 non-serving auxiliary-task distillation 均执行；私有跨产品 schema 未复刻。本地对照口径：跨模型基线是在相同 target split 上训练的 DIN，实验组 KD student 的 NDCG@10 相对 DIN -68.46%；内部基线 target-only student 加蒸馏后 +3.02%。后者只说明 KD 对弱 student 的增量，不能表述成优于 DIN。  distillation cross-domain ranking 搜广推 语义表征、用户知识与冷启动 跨域 KD 为什么可以在目标域样本上调用源域 teacher，而无需取得源域原始训练数据？ 知识通过 teacher 的输出分布和辅助任务信号迁移，student 学习这些响应而非重放源域数据。目标标签仍约束实际服务任务，因此教师需要能理解目标样本可用特征。没有源数据降低接入门槛，却不能证明源教师在新域校准正确。 示意：大视频 teacher 对音乐样本输出偏好分布，小音乐 student 学习这些软信号；系统并没有拿到全部原视频日志，也不能假设视频偏好全部适用于音乐。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-cross-domain-kd-40631210" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-dcb82583790cb527">跨域 KD 为什么可以在目标域样本上调用源域 teacher，而无需取得源域原始训练数据？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Across-domain-kd">Zero-shot Cross-domain Knowledge Distillation: A Case study on YouTube Music</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>知识通过 teacher 的输出分布和辅助任务信号迁移，student 学习这些响应而非重放源域数据。目标标签仍约束实际服务任务，因此教师需要能理解目标样本可用特征。没有源数据降低接入门槛，却不能证明源教师在新域校准正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>大视频 teacher 对音乐样本输出偏好分布，小音乐 student 学习这些软信号；系统并没有拿到全部原视频日志，也不能假设视频偏好全部适用于音乐。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.28994">原论文</a> · <a href="../../../../reproductions/2603.28994-cross-domain-kd/">实现解读</a> · <a href="#qa-dcb82583790cb527">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cross-domain-kd" data-paper-title="Zero-shot Cross-domain Knowledge Distillation: A Case study on YouTube Music" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Zero-shot Cross-domain Knowledge Distillation: A Case study on YouTube Music 搜广推与 LLM 应用 Google / YouTube 2026-03-30 低流量产品无力训练大型专用 teacher。论文直接把数据丰富的 YouTube 多任务 teacher 应用于 YouTube Music 样本，把 serving task 与辅助 task logits 蒸馏到小模型，不要求源域数据或匹配的界面特征。 Fidelity: 核心机制复现。源域大 teacher、目标域小 student、目标样本上的 zero-shot logits 和 non-serving auxiliary-task distillation 均执行；私有跨产品 schema 未复刻。本地对照口径：跨模型基线是在相同 target split 上训练的 DIN，实验组 KD student 的 NDCG@10 相对 DIN -68.46%；内部基线 target-only student 加蒸馏后 +3.02%。后者只说明 KD 对弱 student 的增量，不能表述成优于 DIN。  distillation cross-domain ranking 搜广推 语义表征、用户知识与冷启动 跨域蒸馏为什么能不拿源域训练数据，却仍不能无条件信任源域teacher？ teacher可以直接对目标域样本输出任务与辅助任务知识，学生只需学习这些响应，因而不必获得源域日志。但源域模型面对新产品时仍可能校准错误或缺少关键特征，监督应与目标任务联合使用。知识可迁移不等于效果必然迁移；本地跨域对照的负结果不能被teacher规模掩盖。 示意：视频平台大模型给音乐场景样本提供偏好分布，学生可借到兴趣模式；但如果teacher把视频观看习惯等同于听歌习惯，蒸馏也会传入错误偏好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-a9d9d3587756f447">跨域蒸馏为什么能不拿源域训练数据，却仍不能无条件信任源域teacher？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Across-domain-kd">Zero-shot Cross-domain Knowledge Distillation: A Case study on YouTube Music</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>teacher可以直接对目标域样本输出任务与辅助任务知识，学生只需学习这些响应，因而不必获得源域日志。但源域模型面对新产品时仍可能校准错误或缺少关键特征，监督应与目标任务联合使用。知识可迁移不等于效果必然迁移；本地跨域对照的负结果不能被teacher规模掩盖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>视频平台大模型给音乐场景样本提供偏好分布，学生可借到兴趣模式；但如果teacher把视频观看习惯等同于听歌习惯，蒸馏也会传入错误偏好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.28994">原论文</a> · <a href="../../../../reproductions/2603.28994-cross-domain-kd/">实现解读</a> · <a href="#qa-a9d9d3587756f447">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cross-domain-kd" data-paper-title="Zero-shot Cross-domain Knowledge Distillation: A Case study on YouTube Music" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Zero-shot Cross-domain Knowledge Distillation: A Case study on YouTube Music 搜广推与 LLM 应用 Google / YouTube 2026-03-30 低流量产品无力训练大型专用 teacher。论文直接把数据丰富的 YouTube 多任务 teacher 应用于 YouTube Music 样本，把 serving task 与辅助 task logits 蒸馏到小模型，不要求源域数据或匹配的界面特征。 Fidelity: 核心机制复现。源域大 teacher、目标域小 student、目标样本上的 zero-shot logits 和 non-serving auxiliary-task distillation 均执行；私有跨产品 schema 未复刻。本地对照口径：跨模型基线是在相同 target split 上训练的 DIN，实验组 KD student 的 NDCG@10 相对 DIN -68.46%；内部基线 target-only student 加蒸馏后 +3.02%。后者只说明 KD 对弱 student 的增量，不能表述成优于 DIN。  distillation cross-domain ranking 搜广推 语义表征、用户知识与冷启动 跨域 KD 的 target-only student 对照和同域 DIN 对照，分别检验什么？ target-only 与 KD student 隔离蒸馏增加的知识，DIN 则提供不同模型的整体水平参照。学生内部改善并不代表达到强基线；来源两种结果相差很大，必须分别说明。温度蒸馏机制对比也不能代替统一数据、候选和预算的实测。 示意：学生从十分快到十一分是内部正增量，但 DIN 有三十分，不能把前者写成超越现有模型；两组比较回答不同问题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d39e67ee64576bf2">跨域 KD 的 target-only student 对照和同域 DIN 对照，分别检验什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Across-domain-kd">Zero-shot Cross-domain Knowledge Distillation: A Case study on YouTube Music</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>target-only 与 KD student 隔离蒸馏增加的知识，DIN 则提供不同模型的整体水平参照。学生内部改善并不代表达到强基线；来源两种结果相差很大，必须分别说明。温度蒸馏机制对比也不能代替统一数据、候选和预算的实测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>学生从十分快到十一分是内部正增量，但 DIN 有三十分，不能把前者写成超越现有模型；两组比较回答不同问题。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.28994">原论文</a> · <a href="../../../../reproductions/2603.28994-cross-domain-kd/">实现解读</a> · <a href="#qa-d39e67ee64576bf2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cross-domain-kd" data-paper-title="Zero-shot Cross-domain Knowledge Distillation: A Case study on YouTube Music" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Zero-shot Cross-domain Knowledge Distillation: A Case study on YouTube Music 搜广推与 LLM 应用 Google / YouTube 2026-03-30 低流量产品无力训练大型专用 teacher。论文直接把数据丰富的 YouTube 多任务 teacher 应用于 YouTube Music 样本，把 serving task 与辅助 task logits 蒸馏到小模型，不要求源域数据或匹配的界面特征。 Fidelity: 核心机制复现。源域大 teacher、目标域小 student、目标样本上的 zero-shot logits 和 non-serving auxiliary-task distillation 均执行；私有跨产品 schema 未复刻。本地对照口径：跨模型基线是在相同 target split 上训练的 DIN，实验组 KD student 的 NDCG@10 相对 DIN -68.46%；内部基线 target-only student 加蒸馏后 +3.02%。后者只说明 KD 对弱 student 的增量，不能表述成优于 DIN。  distillation cross-domain ranking 搜广推 语义表征、用户知识与冷启动 跨域 KD 温度蒸馏项为什么包含 T²，辅助 logits 又应如何对齐？ 温度改变 softmax 的锐度，也缩放梯度，T² 用于补偿相应训练尺度。teacher 与 student 任务维度和类别含义必须对应，辅助项不能因形状相同就任意配对。服务只保留 student，教师输出是训练信号而非必须在线调用的特征。 示意：教师的“长看”辅助头不能与学生的“付费”头逐维拟合；提高温度可揭示软关系，但不能修复任务语义配错。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c569ebb41759c020">跨域 KD 温度蒸馏项为什么包含 T²，辅助 logits 又应如何对齐？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Across-domain-kd">Zero-shot Cross-domain Knowledge Distillation: A Case study on YouTube Music</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>温度改变 softmax 的锐度，也缩放梯度，T² 用于补偿相应训练尺度。teacher 与 student 任务维度和类别含义必须对应，辅助项不能因形状相同就任意配对。服务只保留 student，教师输出是训练信号而非必须在线调用的特征。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教师的“长看”辅助头不能与学生的“付费”头逐维拟合；提高温度可揭示软关系，但不能修复任务语义配错。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.28994">原论文</a> · <a href="../../../../reproductions/2603.28994-cross-domain-kd/">实现解读</a> · <a href="#qa-c569ebb41759c020">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gatesid" data-paper-title="GateSID: Adaptive Gating for Semantic-Collaborative Alignment in Cold-Start Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="GateSID: Adaptive Gating for Semantic-Collaborative Alignment in Cold-Start Recommendation 搜广推与 LLM 应用 Alibaba International Digital Commerce 2026-03-24 共享注意力融合语义与协同行为，再用冷启动感知 gate 调节对比对齐强度：新物品偏语义，热门物品保留协同信号。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 gatesid 核心机制，相对 NDCG@10 +34.95%。  semantic-id cold-start contrastive-learning 搜广推 语义表征、用户知识与冷启动 GateSID 为什么让冷启动程度影响语义与协同的比例？ 反馈少时协同表示不可靠，语义可提供共享知识；反馈丰富时 ID 行为差别又不应被内容平均化。冷启动 gate 随状态调节融合与对齐强度，意在避免一个固定比例处理所有物品。活动度不是唯一可靠性指标，门控仍可能误判。 示意：两件同样是跑鞋，新品更多借内容，老品则保留其不同受众反馈；不能因为内容相似就让两者完全共用协同表示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-gatesid-592868f0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6e3b073964f33ff7">GateSID 为什么让冷启动程度影响语义与协同的比例？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agatesid">GateSID: Adaptive Gating for Semantic-Collaborative Alignment in Cold-Start Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>反馈少时协同表示不可靠，语义可提供共享知识；反馈丰富时 ID 行为差别又不应被内容平均化。冷启动 gate 随状态调节融合与对齐强度，意在避免一个固定比例处理所有物品。活动度不是唯一可靠性指标，门控仍可能误判。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两件同样是跑鞋，新品更多借内容，老品则保留其不同受众反馈；不能因为内容相似就让两者完全共用协同表示。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.22916">原论文</a> · <a href="../../../../reproductions/2603.22916-gatesid/">实现解读</a> · <a href="#qa-6e3b073964f33ff7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gatesid" data-paper-title="GateSID: Adaptive Gating for Semantic-Collaborative Alignment in Cold-Start Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="GateSID: Adaptive Gating for Semantic-Collaborative Alignment in Cold-Start Recommendation 搜广推与 LLM 应用 Alibaba International Digital Commerce 2026-03-24 共享注意力融合语义与协同行为，再用冷启动感知 gate 调节对比对齐强度：新物品偏语义，热门物品保留协同信号。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 gatesid 核心机制，相对 NDCG@10 +34.95%。  semantic-id cold-start contrastive-learning 搜广推 语义表征、用户知识与冷启动 GateSID为什么让冷启动程度影响语义—协同融合和对比对齐强度？ 新物品缺少可靠行为，强行与稀疏协同向量一致可能引入噪声；热门物品已有丰富反馈，过度语义化又会损伤偏好差异。冷启动感知gate据状态调节两类信号及其对齐力度，使共享随证据强弱变化。它不是给所有新品永久使用纯内容，随着交互积累，融合策略也应能改变。 示意：两件文字相似商品中，一件已有大量特定人群购买记录，另一件刚上线；前者应保留协同特性，后者先借语义，而不是统一设一半一半。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-e115da7ec1187834">GateSID为什么让冷启动程度影响语义—协同融合和对比对齐强度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agatesid">GateSID: Adaptive Gating for Semantic-Collaborative Alignment in Cold-Start Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>新物品缺少可靠行为，强行与稀疏协同向量一致可能引入噪声；热门物品已有丰富反馈，过度语义化又会损伤偏好差异。冷启动感知gate据状态调节两类信号及其对齐力度，使共享随证据强弱变化。它不是给所有新品永久使用纯内容，随着交互积累，融合策略也应能改变。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两件文字相似商品中，一件已有大量特定人群购买记录，另一件刚上线；前者应保留协同特性，后者先借语义，而不是统一设一半一半。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.22916">原论文</a> · <a href="../../../../reproductions/2603.22916-gatesid/">实现解读</a> · <a href="#qa-e115da7ec1187834">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gatesid" data-paper-title="GateSID: Adaptive Gating for Semantic-Collaborative Alignment in Cold-Start Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="GateSID: Adaptive Gating for Semantic-Collaborative Alignment in Cold-Start Recommendation 搜广推与 LLM 应用 Alibaba International Digital Commerce 2026-03-24 共享注意力融合语义与协同行为，再用冷启动感知 gate 调节对比对齐强度：新物品偏语义，热门物品保留协同信号。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 gatesid 核心机制，相对 NDCG@10 +34.95%。  semantic-id cold-start contrastive-learning 搜广推 语义表征、用户知识与冷启动 GateSID 的对齐强度门控与只在最终打分时混合，相比训练影响在哪里？ 最终混合只调整现有表示的使用，训练期对齐强度还决定两侧相互靠近的程度，直接改变学到的空间。若一侧噪声大，过强对齐会污染另一侧，条件门控试图减少这种风险。机制不同不意味着所有冷启动段都已实测改善。 示意：先把新品噪声 ID 强拉近内容，再在末端降低 ID 权重，可能已经来不及消除污染；训练时就减弱不可靠对齐是另一种控制。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ea48736e0ac71216">GateSID 的对齐强度门控与只在最终打分时混合，相比训练影响在哪里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agatesid">GateSID: Adaptive Gating for Semantic-Collaborative Alignment in Cold-Start Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最终混合只调整现有表示的使用，训练期对齐强度还决定两侧相互靠近的程度，直接改变学到的空间。若一侧噪声大，过强对齐会污染另一侧，条件门控试图减少这种风险。机制不同不意味着所有冷启动段都已实测改善。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先把新品噪声 ID 强拉近内容，再在末端降低 ID 权重，可能已经来不及消除污染；训练时就减弱不可靠对齐是另一种控制。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.22916">原论文</a> · <a href="../../../../reproductions/2603.22916-gatesid/">实现解读</a> · <a href="#qa-ea48736e0ac71216">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gatesid" data-paper-title="GateSID: Adaptive Gating for Semantic-Collaborative Alignment in Cold-Start Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="GateSID: Adaptive Gating for Semantic-Collaborative Alignment in Cold-Start Recommendation 搜广推与 LLM 应用 Alibaba International Digital Commerce 2026-03-24 共享注意力融合语义与协同行为，再用冷启动感知 gate 调节对比对齐强度：新物品偏语义，热门物品保留协同信号。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 gatesid 核心机制，相对 NDCG@10 +34.95%。  semantic-id cold-start contrastive-learning 搜广推 语义表征、用户知识与冷启动 GateSID 实现时，冷启动特征为什么只能来自训练截止前？ 频次与活动度决定 gate，使用测试未来交互会提前知道物品后来的成熟度，改变真实冷启动条件。语义和协同向量先对齐维度再按 gate 融合，不能把门控写成固定验证常数却仍宣称逐样本自适应。 示意：新品在测试周突然爆红，评估时若用整周点击数判它为头部，就已读取未来；应按推荐时已累计的历史决定 gate。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-62b81621b4bfe67a">GateSID 实现时，冷启动特征为什么只能来自训练截止前？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agatesid">GateSID: Adaptive Gating for Semantic-Collaborative Alignment in Cold-Start Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>频次与活动度决定 gate，使用测试未来交互会提前知道物品后来的成熟度，改变真实冷启动条件。语义和协同向量先对齐维度再按 gate 融合，不能把门控写成固定验证常数却仍宣称逐样本自适应。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新品在测试周突然爆红，评估时若用整周点击数判它为头部，就已读取未来；应按推荐时已累计的历史决定 gate。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.22916">原论文</a> · <a href="../../../../reproductions/2603.22916-gatesid/">实现解读</a> · <a href="#qa-62b81621b4bfe67a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tagllm" data-paper-title="TagLLM: A Fine-Grained Tag Generation Approach for Note Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="TagLLM: A Fine-Grained Tag Generation Approach for Note Recommendation 搜广推与 LLM 应用 Tongji University 2026-03-23 TagLLM 按笔记类目构建用户兴趣手册，用多模态 CoT 按兴趣维度抽取细粒度标签，再通过两阶段知识蒸馏把大模型标签能力迁移到小模型，兼顾解释性和线上效率。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05147，相对变化 -4.69%。本地代理目标与论文生产任务不同，不能外推线上 lift。  content-understanding tag-generation knowledge-distillation 搜广推 语义表征、用户知识与冷启动 TagLLM为什么用类目兴趣手册抽细粒度标签？ 不同笔记类目有不同可解释维度，手册和多模态CoT提供结构，帮助标签比通用主题更细。标签用于推荐也需和真实用户兴趣验证，不能只看名称丰富。 例如美食笔记可关注口味与做法，而非只有一个美食大类。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-tagllm-3f53935e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f1b41d8cb3298d8d">TagLLM为什么用类目兴趣手册抽细粒度标签？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atagllm">TagLLM: A Fine-Grained Tag Generation Approach for Note Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tongji University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同笔记类目有不同可解释维度，手册和多模态CoT提供结构，帮助标签比通用主题更细。标签用于推荐也需和真实用户兴趣验证，不能只看名称丰富。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如美食笔记可关注口味与做法，而非只有一个美食大类。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.21481">原论文</a> · <a href="../../../../reproductions/2603.21481-tagllm/">实现解读</a> · <a href="#qa-f1b41d8cb3298d8d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tagllm" data-paper-title="TagLLM: A Fine-Grained Tag Generation Approach for Note Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="TagLLM: A Fine-Grained Tag Generation Approach for Note Recommendation 搜广推与 LLM 应用 Tongji University 2026-03-23 TagLLM 按笔记类目构建用户兴趣手册，用多模态 CoT 按兴趣维度抽取细粒度标签，再通过两阶段知识蒸馏把大模型标签能力迁移到小模型，兼顾解释性和线上效率。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05147，相对变化 -4.69%。本地代理目标与论文生产任务不同，不能外推线上 lift。  content-understanding tag-generation knowledge-distillation 搜广推 语义表征、用户知识与冷启动 TagLLM 为什么先按类目建立兴趣手册，再把多模态标签能力分阶段蒸馏给小模型？ 统一粗标签容易混淆不同类目的兴趣维度，手册先规定每类内容应从哪些方面理解，多模态推理再提取细粒度标签。大模型负责提供较丰富监督，小模型通过蒸馏学习稳定输出，使线上不必重复昂贵推理。可解释标签仍是对用户和内容的建模选择，手册遗漏的维度不会被蒸馏自动补齐。 示意：美食类关注口味与烹饪方法，旅行类关注目的地与出行方式。先建立不同维度，再教小模型抽取，避免把“轻松”在两类内容中都当作同一种兴趣标签。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-30c451bb8509b956">TagLLM 为什么先按类目建立兴趣手册，再把多模态标签能力分阶段蒸馏给小模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atagllm">TagLLM: A Fine-Grained Tag Generation Approach for Note Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tongji University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>统一粗标签容易混淆不同类目的兴趣维度，手册先规定每类内容应从哪些方面理解，多模态推理再提取细粒度标签。大模型负责提供较丰富监督，小模型通过蒸馏学习稳定输出，使线上不必重复昂贵推理。可解释标签仍是对用户和内容的建模选择，手册遗漏的维度不会被蒸馏自动补齐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>美食类关注口味与烹饪方法，旅行类关注目的地与出行方式。先建立不同维度，再教小模型抽取，避免把“轻松”在两类内容中都当作同一种兴趣标签。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.21481">原论文</a> · <a href="../../../../reproductions/2603.21481-tagllm/">实现解读</a> · <a href="#qa-30c451bb8509b956">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tagllm" data-paper-title="TagLLM: A Fine-Grained Tag Generation Approach for Note Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="TagLLM: A Fine-Grained Tag Generation Approach for Note Recommendation 搜广推与 LLM 应用 Tongji University 2026-03-23 TagLLM 按笔记类目构建用户兴趣手册，用多模态 CoT 按兴趣维度抽取细粒度标签，再通过两阶段知识蒸馏把大模型标签能力迁移到小模型，兼顾解释性和线上效率。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05147，相对变化 -4.69%。本地代理目标与论文生产任务不同，不能外推线上 lift。  content-understanding tag-generation knowledge-distillation 搜广推 语义表征、用户知识与冷启动 大模型两阶段蒸馏与线上每条笔记直接调用大模型有何区别？ 蒸馏把昂贵标签知识迁移到小模型，线上执行成本下降但受学生容量和训练覆盖限制。只缓存一批教师标签不等于两阶段训练真正完成。 例如小模型能快速标新笔记，需要实际学会教师任务，而非仅查旧标签表。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e275c4ad6f37f4ce">大模型两阶段蒸馏与线上每条笔记直接调用大模型有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atagllm">TagLLM: A Fine-Grained Tag Generation Approach for Note Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tongji University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>蒸馏把昂贵标签知识迁移到小模型，线上执行成本下降但受学生容量和训练覆盖限制。只缓存一批教师标签不等于两阶段训练真正完成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如小模型能快速标新笔记，需要实际学会教师任务，而非仅查旧标签表。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.21481">原论文</a> · <a href="../../../../reproductions/2603.21481-tagllm/">实现解读</a> · <a href="#qa-e275c4ad6f37f4ce">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tagllm" data-paper-title="TagLLM: A Fine-Grained Tag Generation Approach for Note Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="TagLLM: A Fine-Grained Tag Generation Approach for Note Recommendation 搜广推与 LLM 应用 Tongji University 2026-03-23 TagLLM 按笔记类目构建用户兴趣手册，用多模态 CoT 按兴趣维度抽取细粒度标签，再通过两阶段知识蒸馏把大模型标签能力迁移到小模型，兼顾解释性和线上效率。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05147，相对变化 -4.69%。本地代理目标与论文生产任务不同，不能外推线上 lift。  content-understanding tag-generation knowledge-distillation 搜广推 语义表征、用户知识与冷启动 TagLLM本地MovieLens代理能证明真实多模态笔记标注吗？ 不能，公开类型和行为仅验证中心机制，不含私有笔记图片、兴趣手册生成及生产模型。teacher条件H只用于允许监督，测试标签不应参与构造。 例如电影genre分配不是图文笔记细粒度CoT标签能力。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-935cce9ec30720fc">TagLLM本地MovieLens代理能证明真实多模态笔记标注吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atagllm">TagLLM: A Fine-Grained Tag Generation Approach for Note Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tongji University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，公开类型和行为仅验证中心机制，不含私有笔记图片、兴趣手册生成及生产模型。teacher条件H只用于允许监督，测试标签不应参与构造。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如电影genre分配不是图文笔记细粒度CoT标签能力。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.21481">原论文</a> · <a href="../../../../reproductions/2603.21481-tagllm/">实现解读</a> · <a href="#qa-935cce9ec30720fc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pinclip" data-paper-title="PinCLIP: Large-scale Foundational Multimodal Representation at Pinterest" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="PinCLIP: Large-scale Foundational Multimodal Representation at Pinterest 搜广推与 LLM 应用 Pinterest 2026-03-03 通用 VLM 的训练目标与推荐不一致，且新内容缺少行为。PinCLIP 以 VLM 为 backbone，混合多粒度图文特征，并加入 Pin-Board 图邻居对齐目标，让表征同时掌握内容和推荐图语义。 实验组学习内容—共现图 canonical alignment，NDCG@10 0.03540→0.03490，相对 -1.41%，未复现论文增益。Fidelity: 核心机制复现。执行内容—图邻居对比对齐和 fresh cohort 评估；不训练视觉 backbone。无图像像素、VLM 预训练和 Pinterest 全图；只验证 neighbor alignment 路径，不能据此否定原论文。本地对照口径：基线是 raw genre/content similarity；  multimodal contrastive-learning cold-start 搜广推 语义表征、用户知识与冷启动 PinCLIP 为什么让新内容从内容向量接入推荐图空间？ 新物品缺协同行为，图邻居目标从已有共组织关系学习平台语义，内容 encoder 再将这种知识迁给未见内容。多粒度图文保留细节，但图数据也可能偏曝光，不能把邻居关系当真实无偏偏好。冷启动需有独立评估。 示意：新吊灯无点击，却可凭图文接近同一装修兴趣板里的家具关系；这不是已观察用户共购，只是内容向图空间的迁移。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-pinclip-b1beb580" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6f7bc96645434ce7">PinCLIP 为什么让新内容从内容向量接入推荐图空间？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apinclip">PinCLIP: Large-scale Foundational Multimodal Representation at Pinterest</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>新物品缺协同行为，图邻居目标从已有共组织关系学习平台语义，内容 encoder 再将这种知识迁给未见内容。多粒度图文保留细节，但图数据也可能偏曝光，不能把邻居关系当真实无偏偏好。冷启动需有独立评估。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新吊灯无点击，却可凭图文接近同一装修兴趣板里的家具关系；这不是已观察用户共购，只是内容向图空间的迁移。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.03544">原论文</a> · <a href="../../../../reproductions/2603.03544-pinclip/">实现解读</a> · <a href="#qa-6f7bc96645434ce7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pinclip" data-paper-title="PinCLIP: Large-scale Foundational Multimodal Representation at Pinterest" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="PinCLIP: Large-scale Foundational Multimodal Representation at Pinterest 搜广推与 LLM 应用 Pinterest 2026-03-03 通用 VLM 的训练目标与推荐不一致，且新内容缺少行为。PinCLIP 以 VLM 为 backbone，混合多粒度图文特征，并加入 Pin-Board 图邻居对齐目标，让表征同时掌握内容和推荐图语义。 实验组学习内容—共现图 canonical alignment，NDCG@10 0.03540→0.03490，相对 -1.41%，未复现论文增益。Fidelity: 核心机制复现。执行内容—图邻居对比对齐和 fresh cohort 评估；不训练视觉 backbone。无图像像素、VLM 预训练和 Pinterest 全图；只验证 neighbor alignment 路径，不能据此否定原论文。本地对照口径：基线是 raw genre/content similarity；  multimodal contrastive-learning cold-start 搜广推 语义表征、用户知识与冷启动 PinCLIP 为什么在图文对齐之外加入 Pin-Board 邻居对齐？ 通用图文模型主要学内容相容性，而推荐还依赖用户把哪些内容组织到同一兴趣集合中。邻居对齐把图上的关联加入训练，使内容表示获得推荐语义；多粒度图文特征保留细节。这样新内容可凭内容进入已有空间，但邻居关系也可能含曝光偏置，不能把图对齐等同于真实偏好的无偏估计。 示意：两张图片一张是餐桌、一张是吊灯，视觉不相似，却经常出现在同一个北欧装修收藏板。邻居目标可把这种搭配关系写入表示，帮助新灯具连接装修兴趣。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-909083d23461a8ae">PinCLIP 为什么在图文对齐之外加入 Pin-Board 邻居对齐？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apinclip">PinCLIP: Large-scale Foundational Multimodal Representation at Pinterest</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>通用图文模型主要学内容相容性，而推荐还依赖用户把哪些内容组织到同一兴趣集合中。邻居对齐把图上的关联加入训练，使内容表示获得推荐语义；多粒度图文特征保留细节。这样新内容可凭内容进入已有空间，但邻居关系也可能含曝光偏置，不能把图对齐等同于真实偏好的无偏估计。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两张图片一张是餐桌、一张是吊灯，视觉不相似，却经常出现在同一个北欧装修收藏板。邻居目标可把这种搭配关系写入表示，帮助新灯具连接装修兴趣。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.03544">原论文</a> · <a href="../../../../reproductions/2603.03544-pinclip/">实现解读</a> · <a href="#qa-909083d23461a8ae">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pinclip" data-paper-title="PinCLIP: Large-scale Foundational Multimodal Representation at Pinterest" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="PinCLIP: Large-scale Foundational Multimodal Representation at Pinterest 搜广推与 LLM 应用 Pinterest 2026-03-03 通用 VLM 的训练目标与推荐不一致，且新内容缺少行为。PinCLIP 以 VLM 为 backbone，混合多粒度图文特征，并加入 Pin-Board 图邻居对齐目标，让表征同时掌握内容和推荐图语义。 实验组学习内容—共现图 canonical alignment，NDCG@10 0.03540→0.03490，相对 -1.41%，未复现论文增益。Fidelity: 核心机制复现。执行内容—图邻居对比对齐和 fresh cohort 评估；不训练视觉 backbone。无图像像素、VLM 预训练和 Pinterest 全图；只验证 neighbor alignment 路径，不能据此否定原论文。本地对照口径：基线是 raw genre/content similarity；  multimodal contrastive-learning cold-start 搜广推 语义表征、用户知识与冷启动 PinCLIP 的邻居对齐与仅做 image-text contrastive，相比正例来自哪里？ 图文对照多连接同内容两模态，邻居对照可连接不同内容的板图关系，学到搭配与兴趣结构。两类关系可能冲突，需要权重与采样控制。来源用稀疏 genre 代理无法恢复真实 VLM 多模态差别，因此负结果不可无边界外推。 示意：同一灯具图片与描述是图文正例，灯具与同板餐桌是图邻居正例；把后者误当同物品会丢掉跨内容关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1408018090c68888">PinCLIP 的邻居对齐与仅做 image-text contrastive，相比正例来自哪里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apinclip">PinCLIP: Large-scale Foundational Multimodal Representation at Pinterest</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>图文对照多连接同内容两模态，邻居对照可连接不同内容的板图关系，学到搭配与兴趣结构。两类关系可能冲突，需要权重与采样控制。来源用稀疏 genre 代理无法恢复真实 VLM 多模态差别，因此负结果不可无边界外推。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一灯具图片与描述是图文正例，灯具与同板餐桌是图邻居正例；把后者误当同物品会丢掉跨内容关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.03544">原论文</a> · <a href="../../../../reproductions/2603.03544-pinclip/">实现解读</a> · <a href="#qa-1408018090c68888">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pinclip" data-paper-title="PinCLIP: Large-scale Foundational Multimodal Representation at Pinterest" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="PinCLIP: Large-scale Foundational Multimodal Representation at Pinterest 搜广推与 LLM 应用 Pinterest 2026-03-03 通用 VLM 的训练目标与推荐不一致，且新内容缺少行为。PinCLIP 以 VLM 为 backbone，混合多粒度图文特征，并加入 Pin-Board 图邻居对齐目标，让表征同时掌握内容和推荐图语义。 实验组学习内容—共现图 canonical alignment，NDCG@10 0.03540→0.03490，相对 -1.41%，未复现论文增益。Fidelity: 核心机制复现。执行内容—图邻居对比对齐和 fresh cohort 评估；不训练视觉 backbone。无图像像素、VLM 预训练和 Pinterest 全图；只验证 neighbor alignment 路径，不能据此否定原论文。本地对照口径：基线是 raw genre/content similarity；  multimodal contrastive-learning cold-start 搜广推 语义表征、用户知识与冷启动 PinCLIP 图邻居训练为什么要排除测试未来边而不仅冻结图像 encoder？ 协同边若来自预测之后的消费，会把目标关系先写入表示，即使 encoder 冻结也可能泄漏。图构造、负例和新内容切分需按截止定义；本地 canonical alignment 与真实预训网络应分别说明，不能只看最终向量维度一致。 示意：测试用户后来收藏的新灯具边若提前入图，模型已知它适合该兴趣；冻结视觉参数不改变图里已包含答案这个事实。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7a3b464cdc396da7">PinCLIP 图邻居训练为什么要排除测试未来边而不仅冻结图像 encoder？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apinclip">PinCLIP: Large-scale Foundational Multimodal Representation at Pinterest</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>协同边若来自预测之后的消费，会把目标关系先写入表示，即使 encoder 冻结也可能泄漏。图构造、负例和新内容切分需按截止定义；本地 canonical alignment 与真实预训网络应分别说明，不能只看最终向量维度一致。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>测试用户后来收藏的新灯具边若提前入图，模型已知它适合该兴趣；冻结视觉参数不改变图里已包含答案这个事实。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.03544">原论文</a> · <a href="../../../../reproductions/2603.03544-pinclip/">实现解读</a> · <a href="#qa-7a3b464cdc396da7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:idproxy" data-paper-title="IDProxy: Cold-Start CTR Prediction for Ads and Recommendation at Xiaohongshu with Multimodal LLMs" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="IDProxy: Cold-Start CTR Prediction for Ads and Recommendation at Xiaohongshu with Multimodal LLMs 搜广推与 LLM 应用 Xiaohongshu / Shanghai Jiao Tong University / Fudan University 2026-03-02 多模态 LLM 的语义空间与 CTR 模型长期学习的 item-ID 协同空间并不一致。IDProxy 先用粗粒度对比目标对齐两者，再从多层 hidden state 生成 proxy，通过 residual gate 注入工业排序网络。 复现保真度：核心机制复现。复现保真度：核心机制复现。粗对齐、多层 proxy adapter 和残差门控实际执行；InternVL 与私有图文未复刻。MovieLens genre 作为公开内容模态，先投影到双向行为转移 ID 空间，再执行多层非线性 proxy 和 gate。  multimodal-llm id-alignment ranking 搜广推 语义表征、用户知识与冷启动 IDProxy 中的 proxy 为什么不直接等于原 MLLM embedding？ MLLM 主要学内容语义，排序 ID 空间积累协同行为，两者方向与尺度不一致。proxy 经过粗对齐与多层适配后，作为受门控的增量进入原 ID 表示，保留既有知识又补内容。不能把语义向量直接拼接后的可运行性当作完成空间适配。 示意：两个视觉相似商品受众可能不同，原内容向量分不清，ID 行为可保留这份差异；proxy 应补充而非覆盖它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-idproxy-2c030d0d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0e485c22823c9b5a">IDProxy 中的 proxy 为什么不直接等于原 MLLM embedding？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aidproxy">IDProxy: Cold-Start CTR Prediction for Ads and Recommendation at Xiaohongshu with Multimodal LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu / Shanghai Jiao Tong University / Fudan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>MLLM 主要学内容语义，排序 ID 空间积累协同行为，两者方向与尺度不一致。proxy 经过粗对齐与多层适配后，作为受门控的增量进入原 ID 表示，保留既有知识又补内容。不能把语义向量直接拼接后的可运行性当作完成空间适配。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个视觉相似商品受众可能不同，原内容向量分不清，ID 行为可保留这份差异；proxy 应补充而非覆盖它。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.01590">原论文</a> · <a href="../../../../reproductions/2603.01590-idproxy/">实现解读</a> · <a href="#qa-0e485c22823c9b5a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:idproxy" data-paper-title="IDProxy: Cold-Start CTR Prediction for Ads and Recommendation at Xiaohongshu with Multimodal LLMs" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="IDProxy: Cold-Start CTR Prediction for Ads and Recommendation at Xiaohongshu with Multimodal LLMs 搜广推与 LLM 应用 Xiaohongshu / Shanghai Jiao Tong University / Fudan University 2026-03-02 多模态 LLM 的语义空间与 CTR 模型长期学习的 item-ID 协同空间并不一致。IDProxy 先用粗粒度对比目标对齐两者，再从多层 hidden state 生成 proxy，通过 residual gate 注入工业排序网络。 复现保真度：核心机制复现。复现保真度：核心机制复现。粗对齐、多层 proxy adapter 和残差门控实际执行；InternVL 与私有图文未复刻。MovieLens genre 作为公开内容模态，先投影到双向行为转移 ID 空间，再执行多层非线性 proxy 和 gate。  multimodal-llm id-alignment ranking 搜广推 语义表征、用户知识与冷启动 IDProxy为什么先对齐MLLM与ID空间，再用多层proxy残差接入排序器？ 多模态语义能描述内容，却与长期CTR训练形成的协同坐标不一致，直接替换ID向量可能破坏已有几何关系。粗粒度对比先建立两空间对应，多层proxy再提取不同抽象程度的知识，通过gate控制注入幅度。残差保留原路径不代表无需对照，过强语义仍可能淹没有效协同差异。 示意：两件外观相似商品可能面向不同人群，语义向量不能直接覆盖ID偏好；先学会对应关系，再按状态借用形状、用途等不同层次信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-94883dce7d68b562">IDProxy为什么先对齐MLLM与ID空间，再用多层proxy残差接入排序器？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aidproxy">IDProxy: Cold-Start CTR Prediction for Ads and Recommendation at Xiaohongshu with Multimodal LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu / Shanghai Jiao Tong University / Fudan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多模态语义能描述内容，却与长期CTR训练形成的协同坐标不一致，直接替换ID向量可能破坏已有几何关系。粗粒度对比先建立两空间对应，多层proxy再提取不同抽象程度的知识，通过gate控制注入幅度。残差保留原路径不代表无需对照，过强语义仍可能淹没有效协同差异。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两件外观相似商品可能面向不同人群，语义向量不能直接覆盖ID偏好；先学会对应关系，再按状态借用形状、用途等不同层次信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.01590">原论文</a> · <a href="../../../../reproductions/2603.01590-idproxy/">实现解读</a> · <a href="#qa-94883dce7d68b562">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:idproxy" data-paper-title="IDProxy: Cold-Start CTR Prediction for Ads and Recommendation at Xiaohongshu with Multimodal LLMs" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="IDProxy: Cold-Start CTR Prediction for Ads and Recommendation at Xiaohongshu with Multimodal LLMs 搜广推与 LLM 应用 Xiaohongshu / Shanghai Jiao Tong University / Fudan University 2026-03-02 多模态 LLM 的语义空间与 CTR 模型长期学习的 item-ID 协同空间并不一致。IDProxy 先用粗粒度对比目标对齐两者，再从多层 hidden state 生成 proxy，通过 residual gate 注入工业排序网络。 复现保真度：核心机制复现。复现保真度：核心机制复现。粗对齐、多层 proxy adapter 和残差门控实际执行；InternVL 与私有图文未复刻。MovieLens genre 作为公开内容模态，先投影到双向行为转移 ID 空间，再执行多层非线性 proxy 和 gate。  multimodal-llm id-alignment ranking 搜广推 语义表征、用户知识与冷启动 IDProxy 的 residual gate 与完全替换 item-ID 表示，相比保留什么退路？ 替换会丢已有协同记忆，残差从原 ID 出发按 gate 注入适配语义，允许模型限制不可靠增量。门控仍可能过度依赖一侧，需要分别检查冷尾和头部。对比预训 loss 下降不等于排序必然改善，来源只支持其公开小规模口径。 示意：热门老商品已有充分反馈，门控可少加语义；新品 ID 弱时多借内容，但若内容提取错，gate 也不能保证自行识别所有错误。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c2785150af7e1a5e">IDProxy 的 residual gate 与完全替换 item-ID 表示，相比保留什么退路？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aidproxy">IDProxy: Cold-Start CTR Prediction for Ads and Recommendation at Xiaohongshu with Multimodal LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu / Shanghai Jiao Tong University / Fudan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>替换会丢已有协同记忆，残差从原 ID 出发按 gate 注入适配语义，允许模型限制不可靠增量。门控仍可能过度依赖一侧，需要分别检查冷尾和头部。对比预训 loss 下降不等于排序必然改善，来源只支持其公开小规模口径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>热门老商品已有充分反馈，门控可少加语义；新品 ID 弱时多借内容，但若内容提取错，gate 也不能保证自行识别所有错误。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.01590">原论文</a> · <a href="../../../../reproductions/2603.01590-idproxy/">实现解读</a> · <a href="#qa-c2785150af7e1a5e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:idproxy" data-paper-title="IDProxy: Cold-Start CTR Prediction for Ads and Recommendation at Xiaohongshu with Multimodal LLMs" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="IDProxy: Cold-Start CTR Prediction for Ads and Recommendation at Xiaohongshu with Multimodal LLMs 搜广推与 LLM 应用 Xiaohongshu / Shanghai Jiao Tong University / Fudan University 2026-03-02 多模态 LLM 的语义空间与 CTR 模型长期学习的 item-ID 协同空间并不一致。IDProxy 先用粗粒度对比目标对齐两者，再从多层 hidden state 生成 proxy，通过 residual gate 注入工业排序网络。 复现保真度：核心机制复现。复现保真度：核心机制复现。粗对齐、多层 proxy adapter 和残差门控实际执行；InternVL 与私有图文未复刻。MovieLens genre 作为公开内容模态，先投影到双向行为转移 ID 空间，再执行多层非线性 proxy 和 gate。  multimodal-llm id-alignment ranking 搜广推 语义表征、用户知识与冷启动 IDProxy 粗对齐的正负配对为什么必须按同一 item 身份构造？ PAL 将 MLLM zi 与对应 ID ei 拉近，批内其他 ID 进入分母，列身份错位会把不同商品强行对齐。残差 Adapter 还需映到原 ID 维度再相加，gate 对应同一候选。多层 hidden state 应按实际模型版本采集，不能用随机向量替代。 示意：相机内容若配到童装 ID，loss 也能下降，却学成错误语义；查看形状与数值正常无法替代正例身份核对。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0fdf676b20910cb9">IDProxy 粗对齐的正负配对为什么必须按同一 item 身份构造？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aidproxy">IDProxy: Cold-Start CTR Prediction for Ads and Recommendation at Xiaohongshu with Multimodal LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu / Shanghai Jiao Tong University / Fudan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>PAL 将 MLLM zi 与对应 ID ei 拉近，批内其他 ID 进入分母，列身份错位会把不同商品强行对齐。残差 Adapter 还需映到原 ID 维度再相加，gate 对应同一候选。多层 hidden state 应按实际模型版本采集，不能用随机向量替代。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>相机内容若配到童装 ID，loss 也能下降，却学成错误语义；查看形状与数值正常无法替代正例身份核对。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.01590">原论文</a> · <a href="../../../../reproductions/2603.01590-idproxy/">实现解读</a> · <a href="#qa-0fdf676b20910cb9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:quasid" data-paper-title="Stop Treating Collisions Equally: Qualification-Aware Semantic ID Learning for Recommendation at Industrial Scale" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Stop Treating Collisions Equally: Qualification-Aware Semantic ID Learning for Recommendation at Industrial Scale 搜广推与 LLM 应用 University of Electronic Science and Technology of China / Kuaishou 2026-02-28 用业务资格信号决定碰撞对的 margin，而不是统一排斥；反馈稀疏或冷启动 item 得到更强的可辨识 SID。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 quasid 核心机制，相对 NDCG@10 -0.55%。  semantic-id collision-handling e-commerce 搜广推 语义表征、用户知识与冷启动 QuaSID 中两个码相距更远，是否说明用户更喜欢其中一个物品？ 不能。距离和 margin 在此用于区分编码，资格权重说明哪些物品对需要可辨识，不给出用户偏好的方向。两物品可以被充分分开却都不相关，也可以都很适合当前用户。最终推荐仍需要用户条件评分，不能把可分性当作相关性或增量价值。 示意：两件配送资格不同的商品被拉开，只表示服务时更易区分；用户可能都不想买，码距变大并没有让任一件自动变成好推荐。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-quasid-4adc5716" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b938437696f2b972">QuaSID 中两个码相距更远，是否说明用户更喜欢其中一个物品？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aquasid">Stop Treating Collisions Equally: Qualification-Aware Semantic ID Learning for Recommendation at Industrial Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Electronic Science and Technology of China / Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。距离和 margin 在此用于区分编码，资格权重说明哪些物品对需要可辨识，不给出用户偏好的方向。两物品可以被充分分开却都不相关，也可以都很适合当前用户。最终推荐仍需要用户条件评分，不能把可分性当作相关性或增量价值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两件配送资格不同的商品被拉开，只表示服务时更易区分；用户可能都不想买，码距变大并没有让任一件自动变成好推荐。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.00632">原论文</a> · <a href="../../../../reproductions/2603.00632-quasid/">实现解读</a> · <a href="#qa-b938437696f2b972">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:quasid" data-paper-title="Stop Treating Collisions Equally: Qualification-Aware Semantic ID Learning for Recommendation at Industrial Scale" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Stop Treating Collisions Equally: Qualification-Aware Semantic ID Learning for Recommendation at Industrial Scale 搜广推与 LLM 应用 University of Electronic Science and Technology of China / Kuaishou 2026-02-28 用业务资格信号决定碰撞对的 margin，而不是统一排斥；反馈稀疏或冷启动 item 得到更强的可辨识 SID。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 quasid 核心机制，相对 NDCG@10 -0.55%。  semantic-id collision-handling e-commerce 搜广推 语义表征、用户知识与冷启动 QuaSID 为什么对 SID 碰撞使用业务资格相关的 margin，而不是把所有相近物品等量推开？ 相近编码有助共享语义，但真正需要区分的物品若碰撞，会在生成和服务映射时混淆。资格信号决定哪些碰撞应更强排斥，以及需要多大距离，使有限码空间优先保留关键差异，尤其照顾反馈稀疏物品。统一排斥会破坏有用语义邻近；资格加权仍取决于业务信号质量，不能凭距离推断效果。 示意：两件几乎相同商品可共享粗码，但配送资格不同且必须分别服务，就应在细码上拉开；另两件差异无关当前业务，不必浪费同样强的分离约束。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-021d39c8f232816f">QuaSID 为什么对 SID 碰撞使用业务资格相关的 margin，而不是把所有相近物品等量推开？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aquasid">Stop Treating Collisions Equally: Qualification-Aware Semantic ID Learning for Recommendation at Industrial Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Electronic Science and Technology of China / Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相近编码有助共享语义，但真正需要区分的物品若碰撞，会在生成和服务映射时混淆。资格信号决定哪些碰撞应更强排斥，以及需要多大距离，使有限码空间优先保留关键差异，尤其照顾反馈稀疏物品。统一排斥会破坏有用语义邻近；资格加权仍取决于业务信号质量，不能凭距离推断效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两件几乎相同商品可共享粗码，但配送资格不同且必须分别服务，就应在细码上拉开；另两件差异无关当前业务，不必浪费同样强的分离约束。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.00632">原论文</a> · <a href="../../../../reproductions/2603.00632-quasid/">实现解读</a> · <a href="#qa-021d39c8f232816f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:quasid" data-paper-title="Stop Treating Collisions Equally: Qualification-Aware Semantic ID Learning for Recommendation at Industrial Scale" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Stop Treating Collisions Equally: Qualification-Aware Semantic ID Learning for Recommendation at Industrial Scale 搜广推与 LLM 应用 University of Electronic Science and Technology of China / Kuaishou 2026-02-28 用业务资格信号决定碰撞对的 margin，而不是统一排斥；反馈稀疏或冷启动 item 得到更强的可辨识 SID。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 quasid 核心机制，相对 NDCG@10 -0.55%。  semantic-id collision-handling e-commerce 搜广推 语义表征、用户知识与冷启动 QuaSID 的差异化 margin 与统一排斥所有碰撞，相比码空间如何分配？ 统一排斥给每对同样压力，可能浪费容量并破坏语义邻近；资格权重按业务必要性分配可辨性。它依赖信号可靠，资格变化还可能使旧编码过时。来源公开代理轻微退化，不能因设计更针对性便写成已验证改进。 示意：必须区分的库存资格得到较大间隔，无关差别少推开；若资格数据错，把两件本可替代商品强分离也可能损失共享。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7a10a25b1f687f6f">QuaSID 的差异化 margin 与统一排斥所有碰撞，相比码空间如何分配？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aquasid">Stop Treating Collisions Equally: Qualification-Aware Semantic ID Learning for Recommendation at Industrial Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Electronic Science and Technology of China / Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>统一排斥给每对同样压力，可能浪费容量并破坏语义邻近；资格权重按业务必要性分配可辨性。它依赖信号可靠，资格变化还可能使旧编码过时。来源公开代理轻微退化，不能因设计更针对性便写成已验证改进。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>必须区分的库存资格得到较大间隔，无关差别少推开；若资格数据错，把两件本可替代商品强分离也可能损失共享。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.00632">原论文</a> · <a href="../../../../reproductions/2603.00632-quasid/">实现解读</a> · <a href="#qa-7a10a25b1f687f6f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:quasid" data-paper-title="Stop Treating Collisions Equally: Qualification-Aware Semantic ID Learning for Recommendation at Industrial Scale" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Stop Treating Collisions Equally: Qualification-Aware Semantic ID Learning for Recommendation at Industrial Scale 搜广推与 LLM 应用 University of Electronic Science and Technology of China / Kuaishou 2026-02-28 用业务资格信号决定碰撞对的 margin，而不是统一排斥；反馈稀疏或冷启动 item 得到更强的可辨识 SID。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 quasid 核心机制，相对 NDCG@10 -0.55%。  semantic-id collision-handling e-commerce 搜广推 语义表征、用户知识与冷启动 QuaSID 的 hinge loss 在距离达到 margin 后，为何不应继续强推远？ [mij−d]+ 在满足界限后为零，目的在足够区分而非无限分散；qij 与 margin 应对应同一物品对，且来自训练可得资格。距离定义与对称性需固定，不能用未公开测试资格反推最有利配对。 示意：两码已足够分开，再施同样排斥会浪费空间；误写成一直减距离的线性目标，会让语义关系持续被推散，偏离有限 margin 设计。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6a6a211e585fea57">QuaSID 的 hinge loss 在距离达到 margin 后，为何不应继续强推远？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aquasid">Stop Treating Collisions Equally: Qualification-Aware Semantic ID Learning for Recommendation at Industrial Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Electronic Science and Technology of China / Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>[mij−d]+ 在满足界限后为零，目的在足够区分而非无限分散；qij 与 margin 应对应同一物品对，且来自训练可得资格。距离定义与对称性需固定，不能用未公开测试资格反推最有利配对。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两码已足够分开，再施同样排斥会浪费空间；误写成一直减距离的线性目标，会让语义关系持续被推散，偏离有限 margin 设计。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.00632">原论文</a> · <a href="../../../../reproductions/2603.00632-quasid/">实现解读</a> · <a href="#qa-6a6a211e585fea57">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rq-gmm" data-paper-title="RQ-GMM: Residual Quantized Gaussian Mixture Model for Multimodal Semantic Discretization in CTR Prediction" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RQ-GMM: Residual Quantized Gaussian Mixture Model for Multimodal Semantic Discretization in CTR Prediction 搜广推与 LLM 应用 Tencent 2026-02-13 把图文多模态 embedding 逐层做残差量化，每层以高斯混合后验进行软分配，避免硬聚类的 codebook 利用率不足；语义离散化与 CTR 偏好建模解耦训练。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04685，相对变化 -13.25%。本地代理目标与论文生产任务不同，不能外推线上 lift。  multimodal-recommendation semantic-tokenization ctr-prediction 搜广推 语义表征、用户知识与冷启动 RQ-GMM为什么逐层量化残差而不是只分一次簇？ 第一层捕捉粗语义，后续编码尚未解释的部分，形成分层离散表示。每层高斯后验软分配可缓和硬聚类利用不足，但仍受聚类质量和输入语义影响。 例如先编码大类，再对剩余细节编码，而非要求一个码包办全部语义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-rq-gmm-d5d0f9d6" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2e5696351b2fe603">RQ-GMM为什么逐层量化残差而不是只分一次簇？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arq-gmm">RQ-GMM: Residual Quantized Gaussian Mixture Model for Multimodal Semantic Discretization in CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>第一层捕捉粗语义，后续编码尚未解释的部分，形成分层离散表示。每层高斯后验软分配可缓和硬聚类利用不足，但仍受聚类质量和输入语义影响。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先编码大类，再对剩余细节编码，而非要求一个码包办全部语义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12593">原论文</a> · <a href="../../../../reproductions/2602.12593-rq-gmm/">实现解读</a> · <a href="#qa-2e5696351b2fe603">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rq-gmm" data-paper-title="RQ-GMM: Residual Quantized Gaussian Mixture Model for Multimodal Semantic Discretization in CTR Prediction" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RQ-GMM: Residual Quantized Gaussian Mixture Model for Multimodal Semantic Discretization in CTR Prediction 搜广推与 LLM 应用 Tencent 2026-02-13 把图文多模态 embedding 逐层做残差量化，每层以高斯混合后验进行软分配，避免硬聚类的 codebook 利用率不足；语义离散化与 CTR 偏好建模解耦训练。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04685，相对变化 -13.25%。本地代理目标与论文生产任务不同，不能外推线上 lift。  multimodal-recommendation semantic-tokenization ctr-prediction 搜广推 语义表征、用户知识与冷启动 RQ-GMM 在每层残差量化用高斯混合软分配，和最近中心硬量化有何取舍？ 硬分配只选择一个中心，边界样本容易跳变，少数中心也可能长期闲置。软后验让一个残差按概率组合多个高斯均值，再把量化结果从残差中减去进入下一层，使码本使用更平滑。代价是软表示与最终离散服务接口仍需衔接；语义量化与 CTR 训练解耦，也不保证码本天然最优于点击目标。 示意：一条视频同时像烹饪教学和生活记录，硬分配只能先选一类；软后验可按比例表达两者，再让下一层补残差，减少处在类别边界时的突然跳码。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-9e9e66d9a2ee6a73">RQ-GMM 在每层残差量化用高斯混合软分配，和最近中心硬量化有何取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arq-gmm">RQ-GMM: Residual Quantized Gaussian Mixture Model for Multimodal Semantic Discretization in CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>硬分配只选择一个中心，边界样本容易跳变，少数中心也可能长期闲置。软后验让一个残差按概率组合多个高斯均值，再把量化结果从残差中减去进入下一层，使码本使用更平滑。代价是软表示与最终离散服务接口仍需衔接；语义量化与 CTR 训练解耦，也不保证码本天然最优于点击目标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一条视频同时像烹饪教学和生活记录，硬分配只能先选一类；软后验可按比例表达两者，再让下一层补残差，减少处在类别边界时的突然跳码。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12593">原论文</a> · <a href="../../../../reproductions/2602.12593-rq-gmm/">实现解读</a> · <a href="#qa-9e9e66d9a2ee6a73">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rq-gmm" data-paper-title="RQ-GMM: Residual Quantized Gaussian Mixture Model for Multimodal Semantic Discretization in CTR Prediction" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RQ-GMM: Residual Quantized Gaussian Mixture Model for Multimodal Semantic Discretization in CTR Prediction 搜广推与 LLM 应用 Tencent 2026-02-13 把图文多模态 embedding 逐层做残差量化，每层以高斯混合后验进行软分配，避免硬聚类的 codebook 利用率不足；语义离散化与 CTR 偏好建模解耦训练。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04685，相对变化 -13.25%。本地代理目标与论文生产任务不同，不能外推线上 lift。  multimodal-recommendation semantic-tokenization ctr-prediction 搜广推 语义表征、用户知识与冷启动 RQ-GMM先学习语义码再接CTR训练，与让CTR损失端到端改写码本有什么不同？ 前者把语义量化与CTR优化解耦，后者允许点击目标直接改变离散表示的学习方向。解耦便于保留通用语义结构，却不保证当前CTR任务最优；端到端也可能失去原语义稳定性。这里比较训练耦合关系，不编造两种路径的效果优劣。 教学例子：商品内容相近时先得到相近语义码；若CTR梯度也能改码本，热门度差异可能进一步改变这些码的分配。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b688b0eaa9cebaca">RQ-GMM先学习语义码再接CTR训练，与让CTR损失端到端改写码本有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arq-gmm">RQ-GMM: Residual Quantized Gaussian Mixture Model for Multimodal Semantic Discretization in CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者把语义量化与CTR优化解耦，后者允许点击目标直接改变离散表示的学习方向。解耦便于保留通用语义结构，却不保证当前CTR任务最优；端到端也可能失去原语义稳定性。这里比较训练耦合关系，不编造两种路径的效果优劣。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>商品内容相近时先得到相近语义码；若CTR梯度也能改码本，热门度差异可能进一步改变这些码的分配。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12593">原论文</a> · <a href="../../../../reproductions/2602.12593-rq-gmm/">实现解读</a> · <a href="#qa-b688b0eaa9cebaca">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rq-gmm" data-paper-title="RQ-GMM: Residual Quantized Gaussian Mixture Model for Multimodal Semantic Discretization in CTR Prediction" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RQ-GMM: Residual Quantized Gaussian Mixture Model for Multimodal Semantic Discretization in CTR Prediction 搜广推与 LLM 应用 Tencent 2026-02-13 把图文多模态 embedding 逐层做残差量化，每层以高斯混合后验进行软分配，避免硬聚类的 codebook 利用率不足；语义离散化与 CTR 偏好建模解耦训练。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04685，相对变化 -13.25%。本地代理目标与论文生产任务不同，不能外推线上 lift。  multimodal-recommendation semantic-tokenization ctr-prediction 搜广推 语义表征、用户知识与冷启动 RQ-GMM下一层残差应减去哪个量？ 减本层后验加权重构而非任意最大中心，保持层间递推定义。概率需归一，码本版本与训练阶段分开；本地多模态特征代理不含生产图文模型。 例如先软重构却减硬中心，会让下一层学到另一种未说明残差。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-efde0c3f9921e8b5">RQ-GMM下一层残差应减去哪个量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arq-gmm">RQ-GMM: Residual Quantized Gaussian Mixture Model for Multimodal Semantic Discretization in CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>减本层后验加权重构而非任意最大中心，保持层间递推定义。概率需归一，码本版本与训练阶段分开；本地多模态特征代理不含生产图文模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先软重构却减硬中心，会让下一层学到另一种未说明残差。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12593">原论文</a> · <a href="../../../../reproductions/2602.12593-rq-gmm/">实现解读</a> · <a href="#qa-efde0c3f9921e8b5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sarm" data-paper-title="SARM: LLM-Augmented Semantic Anchor for End-to-End Live-Streaming Ranking" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SARM: LLM-Augmented Semantic Anchor for End-to-End Live-Streaming Ranking 搜广推与 LLM 应用 Institute of Information Engineering, CAS / Kuaishou 2026-02-10 离线 MLLM 生成直播语义 anchor，轻量 SAE 将 anchor 注入端到端排序；非对称部署只在线更新排序器，避免 MLLM 时延。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 sarm 核心机制，相对 NDCG@10 +44.74%。  live-streaming semantic-anchor multimodal-recommendation 搜广推 语义表征、用户知识与冷启动 SARM的semantic anchor是新的直播物品ID，还是内容理解产生的语义信息？ anchor承载离线多模态内容理解，随后经轻量语义模块接入排序；物品ID与行为信号仍是另一类输入。它不是替换目录身份的编号，也不是用户已点击的事实。先区分内容语义与交互身份，才能理解两者怎样补充而非互相冒充。 教学例子：同一直播间ID保持不变，语义anchor可描述当前内容主题；有该描述并不表示某用户已表现出兴趣。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-sarm-37e57a11" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-fc8f3fee4fd06a2a">SARM的semantic anchor是新的直播物品ID，还是内容理解产生的语义信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asarm">SARM: LLM-Augmented Semantic Anchor for End-to-End Live-Streaming Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Information Engineering, CAS / Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>anchor承载离线多模态内容理解，随后经轻量语义模块接入排序；物品ID与行为信号仍是另一类输入。它不是替换目录身份的编号，也不是用户已点击的事实。先区分内容语义与交互身份，才能理解两者怎样补充而非互相冒充。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一直播间ID保持不变，语义anchor可描述当前内容主题；有该描述并不表示某用户已表现出兴趣。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.09401">原论文</a> · <a href="../../../../reproductions/2602.09401-sarm/">实现解读</a> · <a href="#qa-fc8f3fee4fd06a2a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sarm" data-paper-title="SARM: LLM-Augmented Semantic Anchor for End-to-End Live-Streaming Ranking" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SARM: LLM-Augmented Semantic Anchor for End-to-End Live-Streaming Ranking 搜广推与 LLM 应用 Institute of Information Engineering, CAS / Kuaishou 2026-02-10 离线 MLLM 生成直播语义 anchor，轻量 SAE 将 anchor 注入端到端排序；非对称部署只在线更新排序器，避免 MLLM 时延。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 sarm 核心机制，相对 NDCG@10 +44.74%。  live-streaming semantic-anchor multimodal-recommendation 搜广推 语义表征、用户知识与冷启动 SARM 为什么离线生成直播语义 anchor，却只在线更新轻量排序器？ 直播语义复杂，大多模态模型能提炼较丰富的锚点，但请求时调用会增加延迟。离线先产出 anchor，轻量语义模块将其接入端到端排序，再在线学习用户和候选的匹配关系，把内容理解与实时行为适配分开。anchor 若过时或遗漏动态内容，排序器也无法凭空恢复，因此异步更新频率是实际取舍。 示意：离线为直播提炼“户外装备讲解、价格比较”等锚点，请求到来时小排序器结合用户兴趣打分。直播主题突然切换时，旧锚点需更新，不能长期当作准确实况。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-83d7cdb62eb6881b">SARM 为什么离线生成直播语义 anchor，却只在线更新轻量排序器？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asarm">SARM: LLM-Augmented Semantic Anchor for End-to-End Live-Streaming Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Information Engineering, CAS / Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直播语义复杂，大多模态模型能提炼较丰富的锚点，但请求时调用会增加延迟。离线先产出 anchor，轻量语义模块将其接入端到端排序，再在线学习用户和候选的匹配关系，把内容理解与实时行为适配分开。anchor 若过时或遗漏动态内容，排序器也无法凭空恢复，因此异步更新频率是实际取舍。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>离线为直播提炼“户外装备讲解、价格比较”等锚点，请求到来时小排序器结合用户兴趣打分。直播主题突然切换时，旧锚点需更新，不能长期当作准确实况。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.09401">原论文</a> · <a href="../../../../reproductions/2602.09401-sarm/">实现解读</a> · <a href="#qa-83d7cdb62eb6881b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sarm" data-paper-title="SARM: LLM-Augmented Semantic Anchor for End-to-End Live-Streaming Ranking" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SARM: LLM-Augmented Semantic Anchor for End-to-End Live-Streaming Ranking 搜广推与 LLM 应用 Institute of Information Engineering, CAS / Kuaishou 2026-02-10 离线 MLLM 生成直播语义 anchor，轻量 SAE 将 anchor 注入端到端排序；非对称部署只在线更新排序器，避免 MLLM 时延。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 sarm 核心机制，相对 NDCG@10 +44.74%。  live-streaming semantic-anchor multimodal-recommendation 搜广推 语义表征、用户知识与冷启动 SARM的内容语义anchor与在线ID行为特征，能提供相同的信息吗？ 不能。anchor主要提供内容含义，ID和用户行为特征提供平台内交互与匹配证据。相似内容不必让同一用户同样喜欢，行为反馈也未必解释内容在讲什么。异步语义与在线排序结合仍需处理新鲜度，不能只靠其中一类信号声称覆盖另一类。 教学例子：两个直播间都讲露营，但主播互动与用户偏好不同；相似anchor不能代替各自的点击或转化历史。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ae58a8ca3d3c68d0">SARM的内容语义anchor与在线ID行为特征，能提供相同的信息吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asarm">SARM: LLM-Augmented Semantic Anchor for End-to-End Live-Streaming Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Information Engineering, CAS / Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。anchor主要提供内容含义，ID和用户行为特征提供平台内交互与匹配证据。相似内容不必让同一用户同样喜欢，行为反馈也未必解释内容在讲什么。异步语义与在线排序结合仍需处理新鲜度，不能只靠其中一类信号声称覆盖另一类。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个直播间都讲露营，但主播互动与用户偏好不同；相似anchor不能代替各自的点击或转化历史。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.09401">原论文</a> · <a href="../../../../reproductions/2602.09401-sarm/">实现解读</a> · <a href="#qa-ae58a8ca3d3c68d0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sarm" data-paper-title="SARM: LLM-Augmented Semantic Anchor for End-to-End Live-Streaming Ranking" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SARM: LLM-Augmented Semantic Anchor for End-to-End Live-Streaming Ranking 搜广推与 LLM 应用 Institute of Information Engineering, CAS / Kuaishou 2026-02-10 离线 MLLM 生成直播语义 anchor，轻量 SAE 将 anchor 注入端到端排序；非对称部署只在线更新排序器，避免 MLLM 时延。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 sarm 核心机制，相对 NDCG@10 +44.74%。  live-streaming semantic-anchor multimodal-recommendation 搜广推 语义表征、用户知识与冷启动 SARM本地是否具备生产直播anchor生成与部署？ 没有，MovieLens固定候选只验证语义注入和打分路径，未复刻真实MLLM、私有直播模型与集群。anchor编码器与稀疏自编码器缩写不能仅凭SAE混同。 例如一个可审计语义向量代理，并不是实际直播片段的完整多模态总结。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-90e4815c43be3546">SARM本地是否具备生产直播anchor生成与部署？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asarm">SARM: LLM-Augmented Semantic Anchor for End-to-End Live-Streaming Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Information Engineering, CAS / Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有，MovieLens固定候选只验证语义注入和打分路径，未复刻真实MLLM、私有直播模型与集群。anchor编码器与稀疏自编码器缩写不能仅凭SAE混同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个可审计语义向量代理，并不是实际直播片段的完整多模态总结。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.09401">原论文</a> · <a href="../../../../reproductions/2602.09401-sarm/">实现解读</a> · <a href="#qa-90e4815c43be3546">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pit" data-paper-title="PIT: A Dynamic Personalized Item Tokenizer for End-to-End Generative Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="PIT: A Dynamic Personalized Item Tokenizer for End-to-End Generative Recommendation 搜广推与 LLM 应用 Beijing University of Posts and Telecommunications 2026-02-09 tokenizer 与生成推荐器共同训练，以用户引导的最小损失从多个候选 SID 中选出更契合当前偏好的编码；一对多 beam index 保留替代编码，减轻流式分布漂移。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05305，相对变化 -1.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation semantic-id dynamic-tokenizer 搜广推 语义表征、用户知识与冷启动 PIT 所针对的流式分布漂移，为什么会让原来好用的 SID 路径逐渐不合适？ 用户需求、新物品与交互频率会变化，固定编码与旧生成分布的匹配可能随时间减弱，即使商品文字没变也是如此。这里变化的是数据与偏好关系，不是每次生成随机噪声；诊断时应区分真实漂移、模型更新与地址改变，不能用一次波动证明需要重编码。 示意：同一件轻外套在春季通勤和秋季旅行中对应不同需求，内容未改，用户到达它的偏好路径却可能变；重复同一随机种子无法消除这种时间变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-pit-181d335d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8772b022688e6020">PIT 所针对的流式分布漂移，为什么会让原来好用的 SID 路径逐渐不合适？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apit">PIT: A Dynamic Personalized Item Tokenizer for End-to-End Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beijing University of Posts and Telecommunications</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用户需求、新物品与交互频率会变化，固定编码与旧生成分布的匹配可能随时间减弱，即使商品文字没变也是如此。这里变化的是数据与偏好关系，不是每次生成随机噪声；诊断时应区分真实漂移、模型更新与地址改变，不能用一次波动证明需要重编码。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一件轻外套在春季通勤和秋季旅行中对应不同需求，内容未改，用户到达它的偏好路径却可能变；重复同一随机种子无法消除这种时间变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.08530">原论文</a> · <a href="../../../../reproductions/2602.08530-pit/">实现解读</a> · <a href="#qa-8772b022688e6020">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pit" data-paper-title="PIT: A Dynamic Personalized Item Tokenizer for End-to-End Generative Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="PIT: A Dynamic Personalized Item Tokenizer for End-to-End Generative Recommendation 搜广推与 LLM 应用 Beijing University of Posts and Telecommunications 2026-02-09 tokenizer 与生成推荐器共同训练，以用户引导的最小损失从多个候选 SID 中选出更契合当前偏好的编码；一对多 beam index 保留替代编码，减轻流式分布漂移。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05305，相对变化 -1.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation semantic-id dynamic-tokenizer 搜广推 语义表征、用户知识与冷启动 PIT 为什么允许一个物品保留多个候选 SID，再按用户推荐损失选择编码？ 固定单码把所有用户对物品的理解压成同一路径，流式偏好变化时也难调整。PIT 联合训练 tokenizer 与推荐器，并在替代编码中选使当前推荐损失更小的路径，让离散表示受到用户偏好监督。一对多索引保留路径选择余地，但增加索引与去重复杂度，不能把同一物品的多个码当作多个独立商品。 示意：一段“办公室拉伸”视频可从健身或久坐健康两个语义路径到达。面向不同用户选择更合适的编码有利于生成，但最终必须映回同一视频并去重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-ecc9ec54ecfeaba4">PIT 为什么允许一个物品保留多个候选 SID，再按用户推荐损失选择编码？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apit">PIT: A Dynamic Personalized Item Tokenizer for End-to-End Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beijing University of Posts and Telecommunications</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定单码把所有用户对物品的理解压成同一路径，流式偏好变化时也难调整。PIT 联合训练 tokenizer 与推荐器，并在替代编码中选使当前推荐损失更小的路径，让离散表示受到用户偏好监督。一对多索引保留路径选择余地，但增加索引与去重复杂度，不能把同一物品的多个码当作多个独立商品。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一段“办公室拉伸”视频可从健身或久坐健康两个语义路径到达。面向不同用户选择更合适的编码有利于生成，但最终必须映回同一视频并去重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.08530">原论文</a> · <a href="../../../../reproductions/2602.08530-pit/">实现解读</a> · <a href="#qa-ecc9ec54ecfeaba4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pit" data-paper-title="PIT: A Dynamic Personalized Item Tokenizer for End-to-End Generative Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="PIT: A Dynamic Personalized Item Tokenizer for End-to-End Generative Recommendation 搜广推与 LLM 应用 Beijing University of Posts and Telecommunications 2026-02-09 tokenizer 与生成推荐器共同训练，以用户引导的最小损失从多个候选 SID 中选出更契合当前偏好的编码；一对多 beam index 保留替代编码，减轻流式分布漂移。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05305，相对变化 -1.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation semantic-id dynamic-tokenizer 搜广推 语义表征、用户知识与冷启动 PIT 的联合 tokenizer 与先冻结码本再训练生成器，相比梯度耦合在哪里？ 冻结方案让生成器适应既有码，PIT 让推荐损失参与编码选择与学习，语义路径可为用户偏好调整。耦合增加适应力也可能破坏稳定映射，需版本与漂移核验。来源机制不能证明每次流式更新都无损，也不能直接由小代理负差判普遍优劣。 示意：原码把视频放纯健身，推荐训练发现办公室需求重要，可保留另一入口；冻结码则只能在原路径内提高概率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c388d254bbd06a28">PIT 的联合 tokenizer 与先冻结码本再训练生成器，相比梯度耦合在哪里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apit">PIT: A Dynamic Personalized Item Tokenizer for End-to-End Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beijing University of Posts and Telecommunications</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冻结方案让生成器适应既有码，PIT 让推荐损失参与编码选择与学习，语义路径可为用户偏好调整。耦合增加适应力也可能破坏稳定映射，需版本与漂移核验。来源机制不能证明每次流式更新都无损，也不能直接由小代理负差判普遍优劣。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>原码把视频放纯健身，推荐训练发现办公室需求重要，可保留另一入口；冻结码则只能在原路径内提高概率。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.08530">原论文</a> · <a href="../../../../reproductions/2602.08530-pit/">实现解读</a> · <a href="#qa-c388d254bbd06a28">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pit" data-paper-title="PIT: A Dynamic Personalized Item Tokenizer for End-to-End Generative Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="PIT: A Dynamic Personalized Item Tokenizer for End-to-End Generative Recommendation 搜广推与 LLM 应用 Beijing University of Posts and Telecommunications 2026-02-09 tokenizer 与生成推荐器共同训练，以用户引导的最小损失从多个候选 SID 中选出更契合当前偏好的编码；一对多 beam index 保留替代编码，减轻流式分布漂移。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05305，相对变化 -1.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation semantic-id dynamic-tokenizer 搜广推 语义表征、用户知识与冷启动 PIT 的用户引导最小损失选择为什么只能在训练候选编码集合内进行？ argmin 用推荐目标挑监督路径，可借训练标签，但测试不能看 gold 损失替用户选码。推理应按模型分布和合法 beam index 展开，替代码需映回同 item。将真实测试答案用于选最好编码，会把学习问题变成有答案路由。 示意：测试若先知道正确视频，再从其多条码里挑模型最容易的那条，会人为抬高命中；合法推理必须先生成再检查实际物品。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-52b4d03ec7d37f66">PIT 的用户引导最小损失选择为什么只能在训练候选编码集合内进行？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apit">PIT: A Dynamic Personalized Item Tokenizer for End-to-End Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beijing University of Posts and Telecommunications</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>argmin 用推荐目标挑监督路径，可借训练标签，但测试不能看 gold 损失替用户选码。推理应按模型分布和合法 beam index 展开，替代码需映回同 item。将真实测试答案用于选最好编码，会把学习问题变成有答案路由。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>测试若先知道正确视频，再从其多条码里挑模型最容易的那条，会人为抬高命中；合法推理必须先生成再检查实际物品。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.08530">原论文</a> · <a href="../../../../reproductions/2602.08530-pit/">实现解读</a> · <a href="#qa-52b4d03ec7d37f66">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dos" data-paper-title="DOS: Dual-Flow Orthogonal Semantic IDs for Recommendation in Meituan" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="DOS: Dual-Flow Orthogonal Semantic IDs for Recommendation in Meituan 搜广推与 LLM 应用 Meituan 2026-02-04 普通 Semantic ID 的内容 codebook 与生成任务存在间隙。DOS 以用户行为流和商品语义流共同对齐 codebook，并用可约束的正交旋转把主语义与次语义解耦后逐层量化。 Fidelity: 核心机制复现。执行协同/语义双流、正交旋转及 residual quantization。公开 genre/共现替代美团 LLM item embedding 和生产生成器，不能与论文收入增益直接比较。本地对照口径：基线是未旋转的 content/collaborative ensemble；实验组执行 Procrustes 正交对齐与三层 ORQ，NDCG@10 0.03540→0.03938，相对 +11.26%。  generative-recommendation semantic-id orthogonal-quantization 搜广推 语义表征、用户知识与冷启动 DOS 为什么让用户行为流与商品语义流共同塑造 codebook？ 内容量化只优化重构，不一定保留推荐所需协同差别；行为流提供用户消费关系，语义流保留内容结构，两者共同对齐离散空间。它不是把所有共现都当语义相同，仍需平衡重构与任务信号，避免热门反馈压倒细粒度内容。 示意：同主题两部电影受众不同，行为流帮助分开；不同题材却共同满足旅行兴趣的内容，也可能获得更符合推荐的联系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-dos-16f0eac2" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0437ee0944985852">DOS 为什么让用户行为流与商品语义流共同塑造 codebook？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ados">DOS: Dual-Flow Orthogonal Semantic IDs for Recommendation in Meituan</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>内容量化只优化重构，不一定保留推荐所需协同差别；行为流提供用户消费关系，语义流保留内容结构，两者共同对齐离散空间。它不是把所有共现都当语义相同，仍需平衡重构与任务信号，避免热门反馈压倒细粒度内容。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同主题两部电影受众不同，行为流帮助分开；不同题材却共同满足旅行兴趣的内容，也可能获得更符合推荐的联系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.04460">原论文</a> · <a href="../../../../reproductions/2602.04460-dos/">实现解读</a> · <a href="#qa-0437ee0944985852">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dos" data-paper-title="DOS: Dual-Flow Orthogonal Semantic IDs for Recommendation in Meituan" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="DOS: Dual-Flow Orthogonal Semantic IDs for Recommendation in Meituan 搜广推与 LLM 应用 Meituan 2026-02-04 普通 Semantic ID 的内容 codebook 与生成任务存在间隙。DOS 以用户行为流和商品语义流共同对齐 codebook，并用可约束的正交旋转把主语义与次语义解耦后逐层量化。 Fidelity: 核心机制复现。执行协同/语义双流、正交旋转及 residual quantization。公开 genre/共现替代美团 LLM item embedding 和生产生成器，不能与论文收入增益直接比较。本地对照口径：基线是未旋转的 content/collaborative ensemble；实验组执行 Procrustes 正交对齐与三层 ORQ，NDCG@10 0.03540→0.03938，相对 +11.26%。  generative-recommendation semantic-id orthogonal-quantization 搜广推 语义表征、用户知识与冷启动 DOS为什么先做正交旋转，再逐层量化，而不直接量化原始内容向量？ 内容空间的坐标方向未必适合分配语义码，直接切分可能把主要信息集中在少数方向。正交旋转在尽量保持几何关系的同时调整信息布局，再用残差量化分担主次信息；行为流与内容流共同校准codebook。正交并不自动产生独立语义，码的推荐价值仍需由行为目标验证。 示意：一段商品向量的大部分变化都挤在前几个坐标，旋转后可更均衡地分配给各层码；但是否区分了用户真正关心的属性，不能只看旋转矩阵满足正交。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-74c3aabfa7722897">DOS为什么先做正交旋转，再逐层量化，而不直接量化原始内容向量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ados">DOS: Dual-Flow Orthogonal Semantic IDs for Recommendation in Meituan</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>内容空间的坐标方向未必适合分配语义码，直接切分可能把主要信息集中在少数方向。正交旋转在尽量保持几何关系的同时调整信息布局，再用残差量化分担主次信息；行为流与内容流共同校准codebook。正交并不自动产生独立语义，码的推荐价值仍需由行为目标验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一段商品向量的大部分变化都挤在前几个坐标，旋转后可更均衡地分配给各层码；但是否区分了用户真正关心的属性，不能只看旋转矩阵满足正交。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.04460">原论文</a> · <a href="../../../../reproductions/2602.04460-dos/">实现解读</a> · <a href="#qa-74c3aabfa7722897">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dos" data-paper-title="DOS: Dual-Flow Orthogonal Semantic IDs for Recommendation in Meituan" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="DOS: Dual-Flow Orthogonal Semantic IDs for Recommendation in Meituan 搜广推与 LLM 应用 Meituan 2026-02-04 普通 Semantic ID 的内容 codebook 与生成任务存在间隙。DOS 以用户行为流和商品语义流共同对齐 codebook，并用可约束的正交旋转把主语义与次语义解耦后逐层量化。 Fidelity: 核心机制复现。执行协同/语义双流、正交旋转及 residual quantization。公开 genre/共现替代美团 LLM item embedding 和生产生成器，不能与论文收入增益直接比较。本地对照口径：基线是未旋转的 content/collaborative ensemble；实验组执行 Procrustes 正交对齐与三层 ORQ，NDCG@10 0.03540→0.03938，相对 +11.26%。  generative-recommendation semantic-id orthogonal-quantization 搜广推 语义表征、用户知识与冷启动 DOS 的正交旋转与一般可学习投影，相比为什么更强调几何约束？ 正交变换在理想条件下保持距离与范数，只重排信息方向，便于后续分割量化；一般投影可任意缩放扭曲空间。约束减少某类自由度，不保证量化误差最小，更不说明语义因素已经严格独立。来源本地 Procrustes 是特定受控路径。 示意：旋转像转动坐标轴，不把两点突然拉远；任意矩阵则可拉伸某方向。量化网格方向可能更合适，但不代表用户偏好已被因果分解。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-639f0d81779c4784">DOS 的正交旋转与一般可学习投影，相比为什么更强调几何约束？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ados">DOS: Dual-Flow Orthogonal Semantic IDs for Recommendation in Meituan</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>正交变换在理想条件下保持距离与范数，只重排信息方向，便于后续分割量化；一般投影可任意缩放扭曲空间。约束减少某类自由度，不保证量化误差最小，更不说明语义因素已经严格独立。来源本地 Procrustes 是特定受控路径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>旋转像转动坐标轴，不把两点突然拉远；任意矩阵则可拉伸某方向。量化网格方向可能更合适，但不代表用户偏好已被因果分解。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.04460">原论文</a> · <a href="../../../../reproductions/2602.04460-dos/">实现解读</a> · <a href="#qa-639f0d81779c4784">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dos" data-paper-title="DOS: Dual-Flow Orthogonal Semantic IDs for Recommendation in Meituan" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="DOS: Dual-Flow Orthogonal Semantic IDs for Recommendation in Meituan 搜广推与 LLM 应用 Meituan 2026-02-04 普通 Semantic ID 的内容 codebook 与生成任务存在间隙。DOS 以用户行为流和商品语义流共同对齐 codebook，并用可约束的正交旋转把主语义与次语义解耦后逐层量化。 Fidelity: 核心机制复现。执行协同/语义双流、正交旋转及 residual quantization。公开 genre/共现替代美团 LLM item embedding 和生产生成器，不能与论文收入增益直接比较。本地对照口径：基线是未旋转的 content/collaborative ensemble；实验组执行 Procrustes 正交对齐与三层 ORQ，NDCG@10 0.03540→0.03938，相对 +11.26%。  generative-recommendation semantic-id orthogonal-quantization 搜广推 语义表征、用户知识与冷启动 DOS 在逐层残差量化后，为什么要分别检查正交误差与重构误差？ WᵀW 接近单位阵只证明旋转约束成立，逐层选码减残差是否准确还需看重构；两者都好也不等于检索效果好。码本训练与评估应使用相同旋转版本，不能更新 W 后继续读旧码而不记录映射变化。 示意：一张完全正交矩阵可能把数据转到不利于当前码本的方向；因此正交误差近零不能替代重构和推荐指标，更不能当成能力满分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-23e5ceb782b20c24">DOS 在逐层残差量化后，为什么要分别检查正交误差与重构误差？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ados">DOS: Dual-Flow Orthogonal Semantic IDs for Recommendation in Meituan</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>WᵀW 接近单位阵只证明旋转约束成立，逐层选码减残差是否准确还需看重构；两者都好也不等于检索效果好。码本训练与评估应使用相同旋转版本，不能更新 W 后继续读旧码而不记录映射变化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一张完全正交矩阵可能把数据转到不利于当前码本的方向；因此正交误差近零不能替代重构和推荐指标，更不能当成能力满分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.04460">原论文</a> · <a href="../../../../reproductions/2602.04460-dos/">实现解读</a> · <a href="#qa-23e5ceb782b20c24">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recgpt-v2" data-paper-title="RecGPT-V2 Technical Report" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RecGPT-V2 Technical Report 搜广推与 LLM 应用 Alibaba / Taobao 2025-12-16 RecGPT-V1 的多条固定推理链重复且难泛化。V2 用层级多 Agent 拆解意图，混合压缩行为表示，动态生成 meta-prompt，再用多奖励约束 RL 和 Agent-as-a-Judge 对齐。 Fidelity: 核心机制复现。实际执行短期/长期/类目 agent、meta-router、混合表示与 KL 约束偏好更新。Agent 是公开数据上的可训练小型专家，不是淘宝私有 LLM；没有人工 Judge 标注、解释生成或线上资源测量。本地对照口径：相对 RecGPT-V1 单路兴趣基线，实验组 NDCG@10 +18.52%。  llm-recommendation multi-agent reinforcement-learning ranking 搜广推 语义表征、用户知识与冷启动 RecGPT-V2 的压缩行为表示与 meta-prompt，分别是证据还是推理指令？ 压缩表示概括已观察行为，meta-prompt 指示系统当前怎样组织或利用这些证据，二者角色不同。换指令可改变关注点，却不能创造新消费事实；压缩也可能丢掉证据，指令写得再详细不能保证补回。层级 agent 应保持这种信息与控制的边界。 示意：同一旅行浏览摘要可配“优先探索”或“优先实用”的指令，结果取舍可变；但不能因指令要求推荐潜水，就声称用户已有潜水经历。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-recgpt-v2-f68ee63c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-649ef68870c76939">RecGPT-V2 的压缩行为表示与 meta-prompt，分别是证据还是推理指令？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecgpt-v2">RecGPT-V2 Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>压缩表示概括已观察行为，meta-prompt 指示系统当前怎样组织或利用这些证据，二者角色不同。换指令可改变关注点，却不能创造新消费事实；压缩也可能丢掉证据，指令写得再详细不能保证补回。层级 agent 应保持这种信息与控制的边界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一旅行浏览摘要可配“优先探索”或“优先实用”的指令，结果取舍可变；但不能因指令要求推荐潜水，就声称用户已有潜水经历。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2512.14503">原论文</a> · <a href="../../../../reproductions/2512.14503-recgpt-v2/">实现解读</a> · <a href="#qa-649ef68870c76939">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recgpt-v2" data-paper-title="RecGPT-V2 Technical Report" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RecGPT-V2 Technical Report 搜广推与 LLM 应用 Alibaba / Taobao 2025-12-16 RecGPT-V1 的多条固定推理链重复且难泛化。V2 用层级多 Agent 拆解意图，混合压缩行为表示，动态生成 meta-prompt，再用多奖励约束 RL 和 Agent-as-a-Judge 对齐。 Fidelity: 核心机制复现。实际执行短期/长期/类目 agent、meta-router、混合表示与 KL 约束偏好更新。Agent 是公开数据上的可训练小型专家，不是淘宝私有 LLM；没有人工 Judge 标注、解释生成或线上资源测量。本地对照口径：相对 RecGPT-V1 单路兴趣基线，实验组 NDCG@10 +18.52%。  llm-recommendation multi-agent reinforcement-learning ranking 搜广推 语义表征、用户知识与冷启动 RecGPT-V2 为什么用层级多 Agent 和动态 meta-prompt 替代固定多条推理链？ 固定推理链容易重复覆盖同一兴趣，且难随用户上下文改变分工。层级 agent 先拆解意图，压缩行为表示，再动态构造适配当前任务的提示，使不同路径有更明确职责。多奖励与 judge 进一步调整输出质量，但增加 agent 数不自动带来独立知识，仍需检查重复推理、评判偏差和服务成本。 示意：用户近期既准备旅行又关注摄影，系统可分别提炼出行与设备需求，再按当前请求生成综合提示；若只套三条固定模板，可能三次都复述“喜欢摄影”。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f1de662783c54e13">RecGPT-V2 为什么用层级多 Agent 和动态 meta-prompt 替代固定多条推理链？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecgpt-v2">RecGPT-V2 Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定推理链容易重复覆盖同一兴趣，且难随用户上下文改变分工。层级 agent 先拆解意图，压缩行为表示，再动态构造适配当前任务的提示，使不同路径有更明确职责。多奖励与 judge 进一步调整输出质量，但增加 agent 数不自动带来独立知识，仍需检查重复推理、评判偏差和服务成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户近期既准备旅行又关注摄影，系统可分别提炼出行与设备需求，再按当前请求生成综合提示；若只套三条固定模板，可能三次都复述“喜欢摄影”。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2512.14503">原论文</a> · <a href="../../../../reproductions/2512.14503-recgpt-v2/">实现解读</a> · <a href="#qa-f1de662783c54e13">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recgpt-v2" data-paper-title="RecGPT-V2 Technical Report" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RecGPT-V2 Technical Report 搜广推与 LLM 应用 Alibaba / Taobao 2025-12-16 RecGPT-V1 的多条固定推理链重复且难泛化。V2 用层级多 Agent 拆解意图，混合压缩行为表示，动态生成 meta-prompt，再用多奖励约束 RL 和 Agent-as-a-Judge 对齐。 Fidelity: 核心机制复现。实际执行短期/长期/类目 agent、meta-router、混合表示与 KL 约束偏好更新。Agent 是公开数据上的可训练小型专家，不是淘宝私有 LLM；没有人工 Judge 标注、解释生成或线上资源测量。本地对照口径：相对 RecGPT-V1 单路兴趣基线，实验组 NDCG@10 +18.52%。  llm-recommendation multi-agent reinforcement-learning ranking 搜广推 语义表征、用户知识与冷启动 Agent-as-a-Judge 与真实用户反馈，相比评价偏差为何不同？ judge 可快速提供语义或格式评价，真实反馈反映使用行为但也含曝光偏差；多奖励训练结合它们，不能把任何一个当全满意度真值。若 agent 同时提案和自评更可能循环强化偏见，需要独立验证。来源本地代理不证明完整生产 judge/RL。 示意：judge 喜欢详细解释，用户可能只想快速得到结果；奖励解释长不代表实际更有帮助，真实数据与语义评价应分开记录。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5830fcd0732f5656">Agent-as-a-Judge 与真实用户反馈，相比评价偏差为何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecgpt-v2">RecGPT-V2 Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>judge 可快速提供语义或格式评价，真实反馈反映使用行为但也含曝光偏差；多奖励训练结合它们，不能把任何一个当全满意度真值。若 agent 同时提案和自评更可能循环强化偏见，需要独立验证。来源本地代理不证明完整生产 judge/RL。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>judge 喜欢详细解释，用户可能只想快速得到结果；奖励解释长不代表实际更有帮助，真实数据与语义评价应分开记录。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2512.14503">原论文</a> · <a href="../../../../reproductions/2512.14503-recgpt-v2/">实现解读</a> · <a href="#qa-5830fcd0732f5656">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recgpt-v2" data-paper-title="RecGPT-V2 Technical Report" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RecGPT-V2 Technical Report 搜广推与 LLM 应用 Alibaba / Taobao 2025-12-16 RecGPT-V1 的多条固定推理链重复且难泛化。V2 用层级多 Agent 拆解意图，混合压缩行为表示，动态生成 meta-prompt，再用多奖励约束 RL 和 Agent-as-a-Judge 对齐。 Fidelity: 核心机制复现。实际执行短期/长期/类目 agent、meta-router、混合表示与 KL 约束偏好更新。Agent 是公开数据上的可训练小型专家，不是淘宝私有 LLM；没有人工 Judge 标注、解释生成或线上资源测量。本地对照口径：相对 RecGPT-V1 单路兴趣基线，实验组 NDCG@10 +18.52%。  llm-recommendation multi-agent reinforcement-learning ranking 搜广推 语义表征、用户知识与冷启动 RecGPT-V2 的混合 π=Σgkπk 应如何避免路径重复被当额外能力？ 每路分布需在同一候选空间对齐，gate 对实际路径归一，并检查输出重复与调用成本。相同策略复制几份后加权不会增加信息。层级 memory 和动态提示若只用固定分数替代，应明确是代理，不能把数学混合当完整多 agent 执行。 示意：三路都返回同一十件热门物品，混合仍是同一分布；不能因为调用三次就说兴趣覆盖三倍，更需看去重后的候选和证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d29b0614af4e29ed">RecGPT-V2 的混合 π=Σgkπk 应如何避免路径重复被当额外能力？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecgpt-v2">RecGPT-V2 Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每路分布需在同一候选空间对齐，gate 对实际路径归一，并检查输出重复与调用成本。相同策略复制几份后加权不会增加信息。层级 memory 和动态提示若只用固定分数替代，应明确是代理，不能把数学混合当完整多 agent 执行。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三路都返回同一十件热门物品，混合仍是同一分布；不能因为调用三次就说兴趣覆盖三倍，更需看去重后的候选和证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2512.14503">原论文</a> · <a href="../../../../reproductions/2512.14503-recgpt-v2/">实现解读</a> · <a href="#qa-d29b0614af4e29ed">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:saviorrec" data-paper-title="SaviorRec: Semantic-Behavior Alignment for Cold-Start Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SaviorRec: Semantic-Behavior Alignment for Cold-Start Recommendation 搜广推与 LLM 应用 Alibaba 2025-08-02 冷启动排序依赖内容语义，但通用多模态 encoder 的相似度不等于平台用户的共点/共购关系，而且行为分布持续变化。SaviorRec 先以真实交互监督训练 SaviorEnc，再用 RQ-VAE 把表示离散为 Semantic ID；线上排序阶段冻结 SID，同时用零初始化的 Modal-Behavior Alignment（MBA）码本学习相对当前行为空间的残差，并用 target 与历史双向注意力完成 CTR 预测。 Fidelity: 核心机制复现。真实执行行为监督内容编码、RQ Semantic ID、零初始化 MBA 残差码本、双向 target/history attention 和 CTR 训练；MovieLens genre 替代私有图文模型。本地对照口径：基线是等预算 Content Ranker；实验组是 SaviorRec；总体 AUC +1.56%、cold AUC +6.92%，但都只有 1/3 seeds 正向。这是语义—行为对齐模块消融，不是相对 DIN。  cold start semantic ID multimodal recommendation 搜广推 语义表征、用户知识与冷启动 SaviorRec为什么先用行为监督训练内容encoder？ 通用图文语义相似不等于平台共点共购偏好，SaviorEnc用真实交互把内容空间转向推荐需求，再离散SID。冷启动仍依赖内容可用与训练覆盖。 例如外观相似商品未必服务同一消费需求，行为可补充这种差别。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-saviorrec-24eec791" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-18d2fd9fc54a1713">SaviorRec为什么先用行为监督训练内容encoder？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asaviorrec">SaviorRec: Semantic-Behavior Alignment for Cold-Start Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>通用图文语义相似不等于平台共点共购偏好，SaviorEnc用真实交互把内容空间转向推荐需求，再离散SID。冷启动仍依赖内容可用与训练覆盖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如外观相似商品未必服务同一消费需求，行为可补充这种差别。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.01375">原论文</a> · <a href="../../../../reproductions/2508.01375-saviorrec/">实现解读</a> · <a href="#qa-18d2fd9fc54a1713">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:saviorrec" data-paper-title="SaviorRec: Semantic-Behavior Alignment for Cold-Start Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SaviorRec: Semantic-Behavior Alignment for Cold-Start Recommendation 搜广推与 LLM 应用 Alibaba 2025-08-02 冷启动排序依赖内容语义，但通用多模态 encoder 的相似度不等于平台用户的共点/共购关系，而且行为分布持续变化。SaviorRec 先以真实交互监督训练 SaviorEnc，再用 RQ-VAE 把表示离散为 Semantic ID；线上排序阶段冻结 SID，同时用零初始化的 Modal-Behavior Alignment（MBA）码本学习相对当前行为空间的残差，并用 target 与历史双向注意力完成 CTR 预测。 Fidelity: 核心机制复现。真实执行行为监督内容编码、RQ Semantic ID、零初始化 MBA 残差码本、双向 target/history attention 和 CTR 训练；MovieLens genre 替代私有图文模型。本地对照口径：基线是等预算 Content Ranker；实验组是 SaviorRec；总体 AUC +1.56%、cold AUC +6.92%，但都只有 1/3 seeds 正向。这是语义—行为对齐模块消融，不是相对 DIN。  cold start semantic ID multimodal recommendation 搜广推 语义表征、用户知识与冷启动 SaviorRec 为什么冻结 SID，却用零初始化 MBA 码本学习行为残差？ 先用行为监督训练内容编码并量化，得到可迁移的语义骨架；部署后若直接重写 SID，会影响码的稳定性和历史映射。MBA 从零开始按同一离散码学习当前行为空间的残差，初始不扰动原表示，再逐步适配行为变化。目标与历史双向交互用于 CTR，但稳定编码也可能限制对大幅分布变化的响应。 示意：一类露营内容的语义码保持不变，季节变化使用户偏好从夏季轻装转向保暖。残差可调整该码当前的行为表示，而不必让所有内容重新换一套编码。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-4516138032e18f25">SaviorRec 为什么冻结 SID，却用零初始化 MBA 码本学习行为残差？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asaviorrec">SaviorRec: Semantic-Behavior Alignment for Cold-Start Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>先用行为监督训练内容编码并量化，得到可迁移的语义骨架；部署后若直接重写 SID，会影响码的稳定性和历史映射。MBA 从零开始按同一离散码学习当前行为空间的残差，初始不扰动原表示，再逐步适配行为变化。目标与历史双向交互用于 CTR，但稳定编码也可能限制对大幅分布变化的响应。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一类露营内容的语义码保持不变，季节变化使用户偏好从夏季轻装转向保暖。残差可调整该码当前的行为表示，而不必让所有内容重新换一套编码。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.01375">原论文</a> · <a href="../../../../reproductions/2508.01375-saviorrec/">实现解读</a> · <a href="#qa-4516138032e18f25">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:saviorrec" data-paper-title="SaviorRec: Semantic-Behavior Alignment for Cold-Start Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SaviorRec: Semantic-Behavior Alignment for Cold-Start Recommendation 搜广推与 LLM 应用 Alibaba 2025-08-02 冷启动排序依赖内容语义，但通用多模态 encoder 的相似度不等于平台用户的共点/共购关系，而且行为分布持续变化。SaviorRec 先以真实交互监督训练 SaviorEnc，再用 RQ-VAE 把表示离散为 Semantic ID；线上排序阶段冻结 SID，同时用零初始化的 Modal-Behavior Alignment（MBA）码本学习相对当前行为空间的残差，并用 target 与历史双向注意力完成 CTR 预测。 Fidelity: 核心机制复现。真实执行行为监督内容编码、RQ Semantic ID、零初始化 MBA 残差码本、双向 target/history attention 和 CTR 训练；MovieLens genre 替代私有图文模型。本地对照口径：基线是等预算 Content Ranker；实验组是 SaviorRec；总体 AUC +1.56%、cold AUC +6.92%，但都只有 1/3 seeds 正向。这是语义—行为对齐模块消融，不是相对 DIN。  cold start semantic ID multimodal recommendation 搜广推 语义表征、用户知识与冷启动 SaviorRec用行为正对训练内容encoder，与只按内容自身相似性组织表示有何不同？ 行为正对把平台交互关系作为监督，让内容空间朝推荐需求调整；纯内容相似可能只保留图文表面接近。监督来源不同，并不表示行为标签天然没有曝光偏差。该步骤发生在量化前，不能只增加一个下游残差就宣称已完成内容encoder的行为训练。 教学例子：外观不同但经常共同被用户选择的商品，行为正对可拉近其表示；只看图片相似未必建立这种联系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7c34a38d5a8bc34d">SaviorRec用行为正对训练内容encoder，与只按内容自身相似性组织表示有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asaviorrec">SaviorRec: Semantic-Behavior Alignment for Cold-Start Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>行为正对把平台交互关系作为监督，让内容空间朝推荐需求调整；纯内容相似可能只保留图文表面接近。监督来源不同，并不表示行为标签天然没有曝光偏差。该步骤发生在量化前，不能只增加一个下游残差就宣称已完成内容encoder的行为训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>外观不同但经常共同被用户选择的商品，行为正对可拉近其表示；只看图片相似未必建立这种联系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.01375">原论文</a> · <a href="../../../../reproductions/2508.01375-saviorrec/">实现解读</a> · <a href="#qa-7c34a38d5a8bc34d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:saviorrec" data-paper-title="SaviorRec: Semantic-Behavior Alignment for Cold-Start Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SaviorRec: Semantic-Behavior Alignment for Cold-Start Recommendation 搜广推与 LLM 应用 Alibaba 2025-08-02 冷启动排序依赖内容语义，但通用多模态 encoder 的相似度不等于平台用户的共点/共购关系，而且行为分布持续变化。SaviorRec 先以真实交互监督训练 SaviorEnc，再用 RQ-VAE 把表示离散为 Semantic ID；线上排序阶段冻结 SID，同时用零初始化的 Modal-Behavior Alignment（MBA）码本学习相对当前行为空间的残差，并用 target 与历史双向注意力完成 CTR 预测。 Fidelity: 核心机制复现。真实执行行为监督内容编码、RQ Semantic ID、零初始化 MBA 残差码本、双向 target/history attention 和 CTR 训练；MovieLens genre 替代私有图文模型。本地对照口径：基线是等预算 Content Ranker；实验组是 SaviorRec；总体 AUC +1.56%、cold AUC +6.92%，但都只有 1/3 seeds 正向。这是语义—行为对齐模块消融，不是相对 DIN。  cold start semantic ID multimodal recommendation 搜广推 语义表征、用户知识与冷启动 MBA为什么从全零码本开始，双向target注意看什么？ 零起点初始不扰动冻结语义，随后按SID索引学习残差；target查询历史、历史也接收target条件。目标不能泄露未来行为标签，需区别双向交互与时间未来可见。 例如target候选可参与匹配，不表示模型能看用户之后真实点击。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b24c0cd2199d3061">MBA为什么从全零码本开始，双向target注意看什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asaviorrec">SaviorRec: Semantic-Behavior Alignment for Cold-Start Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>零起点初始不扰动冻结语义，随后按SID索引学习残差；target查询历史、历史也接收target条件。目标不能泄露未来行为标签，需区别双向交互与时间未来可见。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如target候选可参与匹配，不表示模型能看用户之后真实点击。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.01375">原论文</a> · <a href="../../../../reproductions/2508.01375-saviorrec/">实现解读</a> · <a href="#qa-b24c0cd2199d3061">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:filterllm" data-paper-title="FilterLLM: Text-To-Distribution LLM for Billion-Scale Cold-Start Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="FilterLLM: Text-To-Distribution LLM for Billion-Scale Cold-Start Recommendation 搜广推与 LLM 应用 Alibaba 2025-02-24 逐用户判断难以服务十亿用户冷启动。FilterLLM 把商品文本一次映射为用户分布，通过用户词表压缩输出空间，并用历史行为指导分布学习。 Fidelity: 核心机制复现。实际学习文本到压缩用户词表分布，并用行为分布约束冷启动表示。用户词表由公开交互 SVD 压缩，不是十亿用户 LLM token；没有淘宝新品文本、流量和延迟栈。本地对照口径：相对 content-to-item judgment 基线，实验组 NDCG@10 -9.82%。  llm-recommendation cold-start retrieval text-to-distribution 搜广推 语义表征、用户知识与冷启动 FilterLLM 为什么从新品文本预测受众分布，而不是下一物品？ 冷启动商品缺交互，目标是主动找到可能喜欢它的用户。一次商品编码输出压缩受众分布，摊销逐用户判断成本，再映回真实人群。概率代表模型倾向而非已观测反馈，低概率也不能直接当作用户明确拒绝。 示意：新帐篷上线先估计露营与旅行人群的兴趣，再接入分发，不必给十亿用户分别生成一次语言模型回答；这仍需要后续真实反馈。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-filterllm-8613b323" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-efbde829d9a93e90">FilterLLM 为什么从新品文本预测受众分布，而不是下一物品？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Afilterllm">FilterLLM: Text-To-Distribution LLM for Billion-Scale Cold-Start Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冷启动商品缺交互，目标是主动找到可能喜欢它的用户。一次商品编码输出压缩受众分布，摊销逐用户判断成本，再映回真实人群。概率代表模型倾向而非已观测反馈，低概率也不能直接当作用户明确拒绝。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新帐篷上线先估计露营与旅行人群的兴趣，再接入分发，不必给十亿用户分别生成一次语言模型回答；这仍需要后续真实反馈。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.16924">原论文</a> · <a href="../../../../reproductions/2502.16924-filterllm/">实现解读</a> · <a href="#qa-efbde829d9a93e90">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:filterllm" data-paper-title="FilterLLM: Text-To-Distribution LLM for Billion-Scale Cold-Start Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="FilterLLM: Text-To-Distribution LLM for Billion-Scale Cold-Start Recommendation 搜广推与 LLM 应用 Alibaba 2025-02-24 逐用户判断难以服务十亿用户冷启动。FilterLLM 把商品文本一次映射为用户分布，通过用户词表压缩输出空间，并用历史行为指导分布学习。 Fidelity: 核心机制复现。实际学习文本到压缩用户词表分布，并用行为分布约束冷启动表示。用户词表由公开交互 SVD 压缩，不是十亿用户 LLM token；没有淘宝新品文本、流量和延迟栈。本地对照口径：相对 content-to-item judgment 基线，实验组 NDCG@10 -9.82%。  llm-recommendation cold-start retrieval text-to-distribution 搜广推 语义表征、用户知识与冷启动 FilterLLM为什么从商品文本直接预测用户分布，而不逐用户问LLM是否推荐？ 逐对判断的成本随用户数量扩大，新商品需要接触海量潜在用户时尤其昂贵。FilterLLM把一次内容编码映射到压缩用户词表上的概率分布，再用历史行为监督，让一个商品侧计算覆盖更多受众。词表压缩引入共享与分辨率取舍，预测分布也不意味着每个具体用户都已经获得可靠个性化判断。 示意：一篇新文章先产生对几类用户兴趣的分布，再把它接入候选流程；无需为每位用户重新生成一次LLM回答，但细粒度差异仍可能在压缩中丢失。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-00503df2eae5a2ba">FilterLLM为什么从商品文本直接预测用户分布，而不逐用户问LLM是否推荐？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Afilterllm">FilterLLM: Text-To-Distribution LLM for Billion-Scale Cold-Start Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>逐对判断的成本随用户数量扩大，新商品需要接触海量潜在用户时尤其昂贵。FilterLLM把一次内容编码映射到压缩用户词表上的概率分布，再用历史行为监督，让一个商品侧计算覆盖更多受众。词表压缩引入共享与分辨率取舍，预测分布也不意味着每个具体用户都已经获得可靠个性化判断。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一篇新文章先产生对几类用户兴趣的分布，再把它接入候选流程；无需为每位用户重新生成一次LLM回答，但细粒度差异仍可能在压缩中丢失。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.16924">原论文</a> · <a href="../../../../reproductions/2502.16924-filterllm/">实现解读</a> · <a href="#qa-00503df2eae5a2ba">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:filterllm" data-paper-title="FilterLLM: Text-To-Distribution LLM for Billion-Scale Cold-Start Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="FilterLLM: Text-To-Distribution LLM for Billion-Scale Cold-Start Recommendation 搜广推与 LLM 应用 Alibaba 2025-02-24 逐用户判断难以服务十亿用户冷启动。FilterLLM 把商品文本一次映射为用户分布，通过用户词表压缩输出空间，并用历史行为指导分布学习。 Fidelity: 核心机制复现。实际学习文本到压缩用户词表分布，并用行为分布约束冷启动表示。用户词表由公开交互 SVD 压缩，不是十亿用户 LLM token；没有淘宝新品文本、流量和延迟栈。本地对照口径：相对 content-to-item judgment 基线，实验组 NDCG@10 -9.82%。  llm-recommendation cold-start retrieval text-to-distribution 搜广推 语义表征、用户知识与冷启动 压缩用户词表与逐用户二分类，输出规模与个性化细度怎样交换？ 逐用户配对规模巨大，压缩词表将相近用户组织为较小输出空间，一次分布覆盖多人，代价是组内差异难表示。分组与数据变化会影响映射，不是无损压缩。来源本地 genre 文本代理退化，不能仅凭可扩展设计宣称冷启动效果更好。 示意：摄影初学者群总体高分，其中刚买完相机的人也许暂时不需要新品；压缩组概率不能替代每位成员当前状态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7d3a5310eb724f26">压缩用户词表与逐用户二分类，输出规模与个性化细度怎样交换？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Afilterllm">FilterLLM: Text-To-Distribution LLM for Billion-Scale Cold-Start Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>逐用户配对规模巨大，压缩词表将相近用户组织为较小输出空间，一次分布覆盖多人，代价是组内差异难表示。分组与数据变化会影响映射，不是无损压缩。来源本地 genre 文本代理退化，不能仅凭可扩展设计宣称冷启动效果更好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>摄影初学者群总体高分，其中刚买完相机的人也许暂时不需要新品；压缩组概率不能替代每位成员当前状态。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.16924">原论文</a> · <a href="../../../../reproductions/2502.16924-filterllm/">实现解读</a> · <a href="#qa-7d3a5310eb724f26">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:filterllm" data-paper-title="FilterLLM: Text-To-Distribution LLM for Billion-Scale Cold-Start Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="FilterLLM: Text-To-Distribution LLM for Billion-Scale Cold-Start Recommendation 搜广推与 LLM 应用 Alibaba 2025-02-24 逐用户判断难以服务十亿用户冷启动。FilterLLM 把商品文本一次映射为用户分布，通过用户词表压缩输出空间，并用历史行为指导分布学习。 Fidelity: 核心机制复现。实际学习文本到压缩用户词表分布，并用行为分布约束冷启动表示。用户词表由公开交互 SVD 压缩，不是十亿用户 LLM token；没有淘宝新品文本、流量和延迟栈。本地对照口径：相对 content-to-item judgment 基线，实验组 NDCG@10 -9.82%。  llm-recommendation cold-start retrieval text-to-distribution 搜广推 语义表征、用户知识与冷启动 FilterLLM 的目标用户分布为什么要避免把未曝光直接当不喜欢？ 历史交互分布受曝光机会影响，未互动可能根本没见过商品。q(u|i) 的归一、词表映射和训练截止应明确，测试交互不能用于构造目标分布。否则会把旧政策或未来答案写入训练，无法检验新品是否真正找到潜在人群。 示意：某用户没看过帐篷不代表厌恶露营；若给所有未曝光者硬零概率，新分发器只会复制旧受众，错失本来可能喜欢的新用户。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a43ab96f505a54aa">FilterLLM 的目标用户分布为什么要避免把未曝光直接当不喜欢？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Afilterllm">FilterLLM: Text-To-Distribution LLM for Billion-Scale Cold-Start Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>历史交互分布受曝光机会影响，未互动可能根本没见过商品。q(u|i) 的归一、词表映射和训练截止应明确，测试交互不能用于构造目标分布。否则会把旧政策或未来答案写入训练，无法检验新品是否真正找到潜在人群。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某用户没看过帐篷不代表厌恶露营；若给所有未曝光者硬零概率，新分发器只会复制旧受众，错失本来可能喜欢的新用户。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.16924">原论文</a> · <a href="../../../../reproductions/2502.16924-filterllm/">实现解读</a> · <a href="#qa-a43ab96f505a54aa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:seral" data-paper-title="Bursting Filter Bubble: Enhancing Serendipity Recommendations with Aligned Large Language Models" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Bursting Filter Bubble: Enhancing Serendipity Recommendations with Aligned Large Language Models 搜广推与 LLM 应用 Alibaba / Taobao 2025-02-19 惊喜推荐需同时相关且未见。SERAL 压缩超长历史为多层认知画像，以 LLM/人工 CDI 打破日志反馈环，用 IPO 对齐 SerenGPT，最后 nearline 生成并缓存候选。 内部消融中 IPO 相对纯 SFT 为 +8.59%，但 category-novelty 0.05542→0.05444，仍未复现惊喜度提升。Fidelity: 完整核心链路复现。静态/短期/长期 cognition profile、SFT、CDI 偏好对、IPO+SFT 与 nearline 全库缓存均执行；GPT-4/人工标注由公开内容和协同信号替代。本地对照口径：统一跨模型基线是 DIN，SERAL NDCG@10 相对 DIN +50.60%；内部基线是纯 SFT，增加 CDI+IPO 后 +8.59%，但 novelty 下降。排序收益与惊喜度结论分开报告。  llm-recommendation preference-alignment serendipity 搜广推 语义表征、用户知识与冷启动 SERAL为什么把惊喜推荐定义为相关且未见？ 只新奇可能无关，只相关又易重复反馈环；多层用户画像与额外偏好对照尝试兼顾两者，再nearline生成候选供排序。新颖不等于用户一定满意。 例如推荐陌生但契合长期兴趣的内容，而不是随机冷门物品。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-seral-54db17e6" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-de3a9ef7e8a1c641">SERAL为什么把惊喜推荐定义为相关且未见？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aseral">Bursting Filter Bubble: Enhancing Serendipity Recommendations with Aligned Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只新奇可能无关，只相关又易重复反馈环；多层用户画像与额外偏好对照尝试兼顾两者，再nearline生成候选供排序。新颖不等于用户一定满意。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如推荐陌生但契合长期兴趣的内容，而不是随机冷门物品。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.13539">原论文</a> · <a href="../../../../reproductions/2502.13539-seral/">实现解读</a> · <a href="#qa-de3a9ef7e8a1c641">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:seral" data-paper-title="Bursting Filter Bubble: Enhancing Serendipity Recommendations with Aligned Large Language Models" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Bursting Filter Bubble: Enhancing Serendipity Recommendations with Aligned Large Language Models 搜广推与 LLM 应用 Alibaba / Taobao 2025-02-19 惊喜推荐需同时相关且未见。SERAL 压缩超长历史为多层认知画像，以 LLM/人工 CDI 打破日志反馈环，用 IPO 对齐 SerenGPT，最后 nearline 生成并缓存候选。 内部消融中 IPO 相对纯 SFT 为 +8.59%，但 category-novelty 0.05542→0.05444，仍未复现惊喜度提升。Fidelity: 完整核心链路复现。静态/短期/长期 cognition profile、SFT、CDI 偏好对、IPO+SFT 与 nearline 全库缓存均执行；GPT-4/人工标注由公开内容和协同信号替代。本地对照口径：统一跨模型基线是 DIN，SERAL NDCG@10 相对 DIN +50.60%；内部基线是纯 SFT，增加 CDI+IPO 后 +8.59%，但 novelty 下降。排序收益与惊喜度结论分开报告。  llm-recommendation preference-alignment serendipity 搜广推 语义表征、用户知识与冷启动 SERAL 为什么引入 LLM 与人工的 CDI 偏好，再用 IPO 对齐，而不直接最大化历史命中？ 历史日志倾向重复已有曝光，单纯拟合会把未见但可能合适的内容排除。多层认知画像提供压缩上下文，CDI 补充日志外的偏好判断，IPO 对齐胜负并保留 SFT 约束，近线生成缓存降低服务成本。相关性与未见性需分别验证；本地排序提高但新颖度下降，不能只凭命中改善就称为更惊喜。 示意：用户一直看熟悉导演，日志只教会重复推荐。人工与模型可比较一部未看过却题材合适的新片和普通熟片，为探索提供信号，但仍需验证用户是否真的接受。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-2bad333c1ee91eaa">SERAL 为什么引入 LLM 与人工的 CDI 偏好，再用 IPO 对齐，而不直接最大化历史命中？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aseral">Bursting Filter Bubble: Enhancing Serendipity Recommendations with Aligned Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>历史日志倾向重复已有曝光，单纯拟合会把未见但可能合适的内容排除。多层认知画像提供压缩上下文，CDI 补充日志外的偏好判断，IPO 对齐胜负并保留 SFT 约束，近线生成缓存降低服务成本。相关性与未见性需分别验证；本地排序提高但新颖度下降，不能只凭命中改善就称为更惊喜。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户一直看熟悉导演，日志只教会重复推荐。人工与模型可比较一部未看过却题材合适的新片和普通熟片，为探索提供信号，但仍需验证用户是否真的接受。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.13539">原论文</a> · <a href="../../../../reproductions/2502.13539-seral/">实现解读</a> · <a href="#qa-2bad333c1ee91eaa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:seral" data-paper-title="Bursting Filter Bubble: Enhancing Serendipity Recommendations with Aligned Large Language Models" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Bursting Filter Bubble: Enhancing Serendipity Recommendations with Aligned Large Language Models 搜广推与 LLM 应用 Alibaba / Taobao 2025-02-19 惊喜推荐需同时相关且未见。SERAL 压缩超长历史为多层认知画像，以 LLM/人工 CDI 打破日志反馈环，用 IPO 对齐 SerenGPT，最后 nearline 生成并缓存候选。 内部消融中 IPO 相对纯 SFT 为 +8.59%，但 category-novelty 0.05542→0.05444，仍未复现惊喜度提升。Fidelity: 完整核心链路复现。静态/短期/长期 cognition profile、SFT、CDI 偏好对、IPO+SFT 与 nearline 全库缓存均执行；GPT-4/人工标注由公开内容和协同信号替代。本地对照口径：统一跨模型基线是 DIN，SERAL NDCG@10 相对 DIN +50.60%；内部基线是纯 SFT，增加 CDI+IPO 后 +8.59%，但 novelty 下降。排序收益与惊喜度结论分开报告。  llm-recommendation preference-alignment serendipity 搜广推 语义表征、用户知识与冷启动 SERAL在本地命中提高但新颖度下降时，能称为惊喜推荐全面改善吗？ 不能。惊喜目标同时涉及相关性与未见性，历史命中只覆盖部分要求。若一种指标改善、另一种下降，应分别报告并讨论取舍，不能用单一排序分数替代整个目标；本地代理也不能外推真实用户惊喜或生产转化。 教学例子：推荐更多用户熟悉的热门内容可能更易命中，却更少带来未见内容；这两种变化应同时展示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ec570df74922742c">SERAL在本地命中提高但新颖度下降时，能称为惊喜推荐全面改善吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aseral">Bursting Filter Bubble: Enhancing Serendipity Recommendations with Aligned Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。惊喜目标同时涉及相关性与未见性，历史命中只覆盖部分要求。若一种指标改善、另一种下降，应分别报告并讨论取舍，不能用单一排序分数替代整个目标；本地代理也不能外推真实用户惊喜或生产转化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>推荐更多用户熟悉的热门内容可能更易命中，却更少带来未见内容；这两种变化应同时展示。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.13539">原论文</a> · <a href="../../../../reproductions/2502.13539-seral/">实现解读</a> · <a href="#qa-ec570df74922742c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:seral" data-paper-title="Bursting Filter Bubble: Enhancing Serendipity Recommendations with Aligned Large Language Models" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Bursting Filter Bubble: Enhancing Serendipity Recommendations with Aligned Large Language Models 搜广推与 LLM 应用 Alibaba / Taobao 2025-02-19 惊喜推荐需同时相关且未见。SERAL 压缩超长历史为多层认知画像，以 LLM/人工 CDI 打破日志反馈环，用 IPO 对齐 SerenGPT，最后 nearline 生成并缓存候选。 内部消融中 IPO 相对纯 SFT 为 +8.59%，但 category-novelty 0.05542→0.05444，仍未复现惊喜度提升。Fidelity: 完整核心链路复现。静态/短期/长期 cognition profile、SFT、CDI 偏好对、IPO+SFT 与 nearline 全库缓存均执行；GPT-4/人工标注由公开内容和协同信号替代。本地对照口径：统一跨模型基线是 DIN，SERAL NDCG@10 相对 DIN +50.60%；内部基线是纯 SFT，增加 CDI+IPO 后 +8.59%，但 novelty 下降。排序收益与惊喜度结论分开报告。  llm-recommendation preference-alignment serendipity 搜广推 语义表征、用户知识与冷启动 SERAL为什么nearline生成并缓存而不每请求生成？ 把重生成成本移出在线关键链路，在线ranker消费缓存候选；需记录画像和缓存版本及刷新，陈旧候选不自动适应即时需求。本地模块不代表生产库存与人类CDI全量实现。 例如用户兴趣转向后应更新缓存，而非永远复用旧候选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-93b5c6475f26e69f">SERAL为什么nearline生成并缓存而不每请求生成？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aseral">Bursting Filter Bubble: Enhancing Serendipity Recommendations with Aligned Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>把重生成成本移出在线关键链路，在线ranker消费缓存候选；需记录画像和缓存版本及刷新，陈旧候选不自动适应即时需求。本地模块不代表生产库存与人类CDI全量实现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户兴趣转向后应更新缓存，而非永远复用旧候选。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.13539">原论文</a> · <a href="../../../../reproductions/2502.13539-seral/">实现解读</a> · <a href="#qa-93b5c6475f26e69f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:lum" data-paper-title="Unlocking Scaling Law in Industrial Recommendation Systems with a Three-step Paradigm based Large User Model" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Unlocking Scaling Law in Industrial Recommendation Systems with a Three-step Paradigm based Large User Model 搜广推与 LLM 应用 Alibaba 2025-02-12 端到端生成推荐能够扩展 Transformer 参数，却难以兼容长期演化的线上 DLRM、复杂特征和毫秒延迟。LUM 将问题拆成三步：先用生成任务构建用户知识，再用条件 token 离线查询不同兴趣，最后把固定知识特征接入任意判别式 DLRM。关键 token 顺序是：condition 描述即将预测的 item 所属场景、搜索词或类别，而不是事后附着在上一 item 上的 action。 Fidelity: 完整核心链路复现。真实执行 condition/item 异构 token encoder、causal next-condition-item InfoNCE、屏蔽式 group query、离线知识缓存、direct feature、interest matching 与下游 CTR DLRM；不声称复现 7B scaling law。本地对照口径：基线是 ID-DLRM；实验组是加入 LUM 离线知识的相同下游 DLRM；AUC 从 0.58233 升至 0.66734（+14.60%）。这是 LUM 知识特征消融，不是相对 DIN。  large user model generative pretraining knowledge querying CTR 搜广推 语义表征、用户知识与冷启动 LUM 为什么把用户知识生成和在线 DLRM 排序分为三步？ 大生成模型先学用户条件关系，再离线查询不同兴趣并缓存，最后把知识向量及目标匹配分接到成熟判别模型，避免请求时重跑大模型。知识服务任意 DLRM 的接口并非自动无损迁移，缓存时效与条件定义仍重要。 示意：后台为用户按多个兴趣条件准备知识，线上原 DLRM 读取并与当前商品匹配；不用为了引入大模型知识替换全部实时特征系统。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-lum-66a3db6d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6dc046ca11652b26">LUM 为什么把用户知识生成和在线 DLRM 排序分为三步？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alum">Unlocking Scaling Law in Industrial Recommendation Systems with a Three-step Paradigm based Large User Model</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>大生成模型先学用户条件关系，再离线查询不同兴趣并缓存，最后把知识向量及目标匹配分接到成熟判别模型，避免请求时重跑大模型。知识服务任意 DLRM 的接口并非自动无损迁移，缓存时效与条件定义仍重要。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>后台为用户按多个兴趣条件准备知识，线上原 DLRM 读取并与当前商品匹配；不用为了引入大模型知识替换全部实时特征系统。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.08309">原论文</a> · <a href="../../../../reproductions/2502.08309-lum/">实现解读</a> · <a href="#qa-6dc046ca11652b26">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:lum" data-paper-title="Unlocking Scaling Law in Industrial Recommendation Systems with a Three-step Paradigm based Large User Model" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Unlocking Scaling Law in Industrial Recommendation Systems with a Three-step Paradigm based Large User Model 搜广推与 LLM 应用 Alibaba 2025-02-12 端到端生成推荐能够扩展 Transformer 参数，却难以兼容长期演化的线上 DLRM、复杂特征和毫秒延迟。LUM 将问题拆成三步：先用生成任务构建用户知识，再用条件 token 离线查询不同兴趣，最后把固定知识特征接入任意判别式 DLRM。关键 token 顺序是：condition 描述即将预测的 item 所属场景、搜索词或类别，而不是事后附着在上一 item 上的 action。 Fidelity: 完整核心链路复现。真实执行 condition/item 异构 token encoder、causal next-condition-item InfoNCE、屏蔽式 group query、离线知识缓存、direct feature、interest matching 与下游 CTR DLRM；不声称复现 7B scaling law。本地对照口径：基线是 ID-DLRM；实验组是加入 LUM 离线知识的相同下游 DLRM；AUC 从 0.58233 升至 0.66734（+14.60%）。这是 LUM 知识特征消融，不是相对 DIN。  large user model generative pretraining knowledge querying CTR 搜广推 语义表征、用户知识与冷启动 LUM中的condition为什么要放在即将预测的item之前，而不是当上一item的反馈？ condition表达接下来选择发生的场景、查询或类别，它应约束未来物品分布；若附在上一物品上，就改变为解释过去行为的信号。LUM用条件化生成建立可查询的用户知识，再离线抽取多种兴趣特征供DLRM使用，而不是要求线上直接运行大生成模型。两种token语义不能只因形式相似就互换。 示意：用户接下来进入厨房品类，condition应帮助预测将看的锅具；若把它当成上一双跑鞋的反馈，训练就会学到完全不同的条件关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c3f51ac8eb5bfaca">LUM中的condition为什么要放在即将预测的item之前，而不是当上一item的反馈？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alum">Unlocking Scaling Law in Industrial Recommendation Systems with a Three-step Paradigm based Large User Model</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>condition表达接下来选择发生的场景、查询或类别，它应约束未来物品分布；若附在上一物品上，就改变为解释过去行为的信号。LUM用条件化生成建立可查询的用户知识，再离线抽取多种兴趣特征供DLRM使用，而不是要求线上直接运行大生成模型。两种token语义不能只因形式相似就互换。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户接下来进入厨房品类，condition应帮助预测将看的锅具；若把它当成上一双跑鞋的反馈，训练就会学到完全不同的条件关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.08309">原论文</a> · <a href="../../../../reproductions/2502.08309-lum/">实现解读</a> · <a href="#qa-c3f51ac8eb5bfaca">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:lum" data-paper-title="Unlocking Scaling Law in Industrial Recommendation Systems with a Three-step Paradigm based Large User Model" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Unlocking Scaling Law in Industrial Recommendation Systems with a Three-step Paradigm based Large User Model 搜广推与 LLM 应用 Alibaba 2025-02-12 端到端生成推荐能够扩展 Transformer 参数，却难以兼容长期演化的线上 DLRM、复杂特征和毫秒延迟。LUM 将问题拆成三步：先用生成任务构建用户知识，再用条件 token 离线查询不同兴趣，最后把固定知识特征接入任意判别式 DLRM。关键 token 顺序是：condition 描述即将预测的 item 所属场景、搜索词或类别，而不是事后附着在上一 item 上的 action。 Fidelity: 完整核心链路复现。真实执行 condition/item 异构 token encoder、causal next-condition-item InfoNCE、屏蔽式 group query、离线知识缓存、direct feature、interest matching 与下游 CTR DLRM；不声称复现 7B scaling law。本地对照口径：基线是 ID-DLRM；实验组是加入 LUM 离线知识的相同下游 DLRM；AUC 从 0.58233 升至 0.66734（+14.60%）。这是 LUM 知识特征消融，不是相对 DIN。  large user model generative pretraining knowledge querying CTR 搜广推 语义表征、用户知识与冷启动 LUM 的多个条件查询与一个固定用户 embedding，信息组织有何不同？ 单向量压缩所有需求，多条件查询可提取不同场景或偏好切面的知识，再由下游结合目标使用。更多查询增加容量和缓存成本，且可能冗余。来源相对无序列 ID-DLRM 的增益含多种新增信息，不能只归给条件 token 本身。 示意：同一用户在“高评分”“低评分”条件下可得到不同物品倾向，下游看二者差别；一份平均向量可能把喜欢与回避混在一起。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-477cc9cf1c2b9611">LUM 的多个条件查询与一个固定用户 embedding，信息组织有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alum">Unlocking Scaling Law in Industrial Recommendation Systems with a Three-step Paradigm based Large User Model</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单向量压缩所有需求，多条件查询可提取不同场景或偏好切面的知识，再由下游结合目标使用。更多查询增加容量和缓存成本，且可能冗余。来源相对无序列 ID-DLRM 的增益含多种新增信息，不能只归给条件 token 本身。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一用户在“高评分”“低评分”条件下可得到不同物品倾向，下游看二者差别；一份平均向量可能把喜欢与回避混在一起。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.08309">原论文</a> · <a href="../../../../reproductions/2502.08309-lum/">实现解读</a> · <a href="#qa-477cc9cf1c2b9611">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:lum" data-paper-title="Unlocking Scaling Law in Industrial Recommendation Systems with a Three-step Paradigm based Large User Model" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Unlocking Scaling Law in Industrial Recommendation Systems with a Three-step Paradigm based Large User Model 搜广推与 LLM 应用 Alibaba 2025-02-12 端到端生成推荐能够扩展 Transformer 参数，却难以兼容长期演化的线上 DLRM、复杂特征和毫秒延迟。LUM 将问题拆成三步：先用生成任务构建用户知识，再用条件 token 离线查询不同兴趣，最后把固定知识特征接入任意判别式 DLRM。关键 token 顺序是：condition 描述即将预测的 item 所属场景、搜索词或类别，而不是事后附着在上一 item 上的 action。 Fidelity: 完整核心链路复现。真实执行 condition/item 异构 token encoder、causal next-condition-item InfoNCE、屏蔽式 group query、离线知识缓存、direct feature、interest matching 与下游 CTR DLRM；不声称复现 7B scaling law。本地对照口径：基线是 ID-DLRM；实验组是加入 LUM 离线知识的相同下游 DLRM；AUC 从 0.58233 升至 0.66734（+14.60%）。这是 LUM 知识特征消融，不是相对 DIN。  large user model generative pretraining knowledge querying CTR 搜广推 语义表征、用户知识与冷启动 LUM 离线一次追加多个 query condition，为什么要屏蔽 query-query attention？ 各查询应在同一公共历史上独立取证，互读会让一个条件结果依赖其他查询顺序，破坏可复用查询语义。训练目标落在 condition 输出以预测紧随 item，不是 item 后附 action。缓存特征需绑定同一前缀与条件版本。 示意：查询“高评分”和“低评分”一起计算时，两者不能交换预测线索；否则只改变查询排列就可能改变用户知识，无法当独立条件接口。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d46cbb9ff26d819d">LUM 离线一次追加多个 query condition，为什么要屏蔽 query-query attention？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alum">Unlocking Scaling Law in Industrial Recommendation Systems with a Three-step Paradigm based Large User Model</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>各查询应在同一公共历史上独立取证，互读会让一个条件结果依赖其他查询顺序，破坏可复用查询语义。训练目标落在 condition 输出以预测紧随 item，不是 item 后附 action。缓存特征需绑定同一前缀与条件版本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>查询“高评分”和“低评分”一起计算时，两者不能交换预测线索；否则只改变查询排列就可能改变用户知识，无法当独立条件接口。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.08309">原论文</a> · <a href="../../../../reproductions/2502.08309-lum/">实现解读</a> · <a href="#qa-d46cbb9ff26d819d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mim" data-paper-title="MIM: Multi-modal Content Interest Modeling Paradigm for User Behavior Modeling" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="MIM: Multi-modal Content Interest Modeling Paradigm for User Behavior Modeling 搜广推与 LLM 应用 Alibaba / Taobao 2025-02-01 纯 ID 行为模型难以理解新品内容。MIM 先遮盖重建多模态内容，再用 content-interest-aware SFT 对齐内容与协同兴趣，最后由 CiUBM 融合内容兴趣和 ID 兴趣。 Fidelity: 核心机制复现。实际执行遮盖内容重建、内容—协同对比对齐和 CiUBM 风格兴趣融合。genre 代理图文模态；没有淘宝私有曝光、真实多模态 encoder 与生产 serving。本地与论文线上数值不可直接比较。本地对照口径：相对 ID 共现兴趣基线，实验组 NDCG@10 +0.94%。  multimodal-recommendation user-modeling pretraining ranking 搜广推 语义表征、用户知识与冷启动 MIM 为什么在多模态重建后还要做内容—兴趣对齐？ 重建学习内容可恢复信息，却不直接教模型哪些内容差别对应用户偏好。content-interest-aware SFT 连接语义和协同，CiUBM 再融合内容与 ID 兴趣。内容理解与推荐选择是不同任务，重建 loss 低不能代替推荐效果证据。 示意：模型能复原电影海报颜色，不代表知道用户偏好硬科幻还是轻喜剧；对齐阶段需要真实行为监督把内容特征变成兴趣信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-mim-fdc0fc79" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-167d9287d182fc2d">MIM 为什么在多模态重建后还要做内容—兴趣对齐？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amim">MIM: Multi-modal Content Interest Modeling Paradigm for User Behavior Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>重建学习内容可恢复信息，却不直接教模型哪些内容差别对应用户偏好。content-interest-aware SFT 连接语义和协同，CiUBM 再融合内容与 ID 兴趣。内容理解与推荐选择是不同任务，重建 loss 低不能代替推荐效果证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型能复原电影海报颜色，不代表知道用户偏好硬科幻还是轻喜剧；对齐阶段需要真实行为监督把内容特征变成兴趣信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.00321">原论文</a> · <a href="../../../../reproductions/2502.00321-mim/">实现解读</a> · <a href="#qa-167d9287d182fc2d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mim" data-paper-title="MIM: Multi-modal Content Interest Modeling Paradigm for User Behavior Modeling" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="MIM: Multi-modal Content Interest Modeling Paradigm for User Behavior Modeling 搜广推与 LLM 应用 Alibaba / Taobao 2025-02-01 纯 ID 行为模型难以理解新品内容。MIM 先遮盖重建多模态内容，再用 content-interest-aware SFT 对齐内容与协同兴趣，最后由 CiUBM 融合内容兴趣和 ID 兴趣。 Fidelity: 核心机制复现。实际执行遮盖内容重建、内容—协同对比对齐和 CiUBM 风格兴趣融合。genre 代理图文模态；没有淘宝私有曝光、真实多模态 encoder 与生产 serving。本地与论文线上数值不可直接比较。本地对照口径：相对 ID 共现兴趣基线，实验组 NDCG@10 +0.94%。  multimodal-recommendation user-modeling pretraining ranking 搜广推 语义表征、用户知识与冷启动 MIM先做多模态遮盖重建后，为什么还要content-interest-aware SFT？ 重建能学习内容内部结构，却不告诉模型哪些语义与用户偏好有关。后续SFT用消费兴趣对齐内容空间，再融合内容兴趣和ID兴趣，让新品知识与已有协同信号相互补充。若只完成内容重建，就不能声称已学到推荐相关性；ID与内容融合也需避免一侧完全压过另一侧。 示意：模型能补回商品图片的颜色，不代表知道用户关心轻便还是耐用；兴趣对齐把这些消费差异引入内容表示，之后再与有行为的老商品ID知识结合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-b8fa8489000b3a6e">MIM先做多模态遮盖重建后，为什么还要content-interest-aware SFT？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amim">MIM: Multi-modal Content Interest Modeling Paradigm for User Behavior Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>重建能学习内容内部结构，却不告诉模型哪些语义与用户偏好有关。后续SFT用消费兴趣对齐内容空间，再融合内容兴趣和ID兴趣，让新品知识与已有协同信号相互补充。若只完成内容重建，就不能声称已学到推荐相关性；ID与内容融合也需避免一侧完全压过另一侧。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型能补回商品图片的颜色，不代表知道用户关心轻便还是耐用；兴趣对齐把这些消费差异引入内容表示，之后再与有行为的老商品ID知识结合。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.00321">原论文</a> · <a href="../../../../reproductions/2502.00321-mim/">实现解读</a> · <a href="#qa-b8fa8489000b3a6e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mim" data-paper-title="MIM: Multi-modal Content Interest Modeling Paradigm for User Behavior Modeling" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="MIM: Multi-modal Content Interest Modeling Paradigm for User Behavior Modeling 搜广推与 LLM 应用 Alibaba / Taobao 2025-02-01 纯 ID 行为模型难以理解新品内容。MIM 先遮盖重建多模态内容，再用 content-interest-aware SFT 对齐内容与协同兴趣，最后由 CiUBM 融合内容兴趣和 ID 兴趣。 Fidelity: 核心机制复现。实际执行遮盖内容重建、内容—协同对比对齐和 CiUBM 风格兴趣融合。genre 代理图文模态；没有淘宝私有曝光、真实多模态 encoder 与生产 serving。本地与论文线上数值不可直接比较。本地对照口径：相对 ID 共现兴趣基线，实验组 NDCG@10 +0.94%。  multimodal-recommendation user-modeling pretraining ranking 搜广推 语义表征、用户知识与冷启动 MIM 双兴趣融合与只用 ID 共现，相比对新品增加哪类可用线索？ ID 共现依赖反馈，内容兴趣能从多模态共享知识迁移到少交互物品，两者互补。内容噪声和兴趣映射错误也可能拖累排序；来源 NDCG 略升而 Hit 下降，不能挑一个指标称全面获益。新品表现还需独立分组。 示意：新电影无共现，内容分支仍可识别科幻主题；但若海报误导成动作片，加入内容也可能让原本稳定的 ID 评分退化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ccaad5564c0af13b">MIM 双兴趣融合与只用 ID 共现，相比对新品增加哪类可用线索？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amim">MIM: Multi-modal Content Interest Modeling Paradigm for User Behavior Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>ID 共现依赖反馈，内容兴趣能从多模态共享知识迁移到少交互物品，两者互补。内容噪声和兴趣映射错误也可能拖累排序；来源 NDCG 略升而 Hit 下降，不能挑一个指标称全面获益。新品表现还需独立分组。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新电影无共现，内容分支仍可识别科幻主题；但若海报误导成动作片，加入内容也可能让原本稳定的 ID 评分退化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.00321">原论文</a> · <a href="../../../../reproductions/2502.00321-mim/">实现解读</a> · <a href="#qa-ccaad5564c0af13b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mim" data-paper-title="MIM: Multi-modal Content Interest Modeling Paradigm for User Behavior Modeling" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="MIM: Multi-modal Content Interest Modeling Paradigm for User Behavior Modeling 搜广推与 LLM 应用 Alibaba / Taobao 2025-02-01 纯 ID 行为模型难以理解新品内容。MIM 先遮盖重建多模态内容，再用 content-interest-aware SFT 对齐内容与协同兴趣，最后由 CiUBM 融合内容兴趣和 ID 兴趣。 Fidelity: 核心机制复现。实际执行遮盖内容重建、内容—协同对比对齐和 CiUBM 风格兴趣融合。genre 代理图文模态；没有淘宝私有曝光、真实多模态 encoder 与生产 serving。本地与论文线上数值不可直接比较。本地对照口径：相对 ID 共现兴趣基线，实验组 NDCG@10 +0.94%。  multimodal-recommendation user-modeling pretraining ranking 搜广推 语义表征、用户知识与冷启动 MIM 的 mask 重建和推荐 target，为什么要使用不同的可见性规则？ 训练可遮住部分内容再重建，但推荐输入必须截止当前用户历史，未来物品及其反馈只能作目标。内容模态 mask 不能掩盖时序泄漏；若完整目标 item 提前进入用户兴趣，重建再困难也不是合法 next-item 评估。 示意：遮住历史海报的一块是内容训练，先把测试电影全向量放进历史再预测它则泄漏；两者都叫 mask，不代表约束相同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3115f2398f8704fd">MIM 的 mask 重建和推荐 target，为什么要使用不同的可见性规则？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amim">MIM: Multi-modal Content Interest Modeling Paradigm for User Behavior Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>训练可遮住部分内容再重建，但推荐输入必须截止当前用户历史，未来物品及其反馈只能作目标。内容模态 mask 不能掩盖时序泄漏；若完整目标 item 提前进入用户兴趣，重建再困难也不是合法 next-item 评估。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>遮住历史海报的一块是内容训练，先把测试电影全向量放进历史再预测它则泄漏；两者都叫 mask，不代表约束相同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.00321">原论文</a> · <a href="../../../../reproductions/2502.00321-mim/">实现解读</a> · <a href="#qa-3115f2398f8704fd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:msd" data-paper-title="Balancing Efficiency and Effectiveness: An LLM-Infused Approach for Optimized CTR Prediction" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Balancing Efficiency and Effectiveness: An LLM-Infused Approach for Optimized CTR Prediction 搜广推与 LLM 应用 Meituan 2024-12-09 直接在 CTR 链路调用大模型效果好但成本不可接受；只缓存静态 embedding 又无法跟随 CTR 目标更新。MSD 的 MKDM 先让大 teacher 为用户和物品生成关键词与推理，再让较小 student 自回归学习这些输出。MKIM 对蒸馏后的 student 做 LoRA CTR 对齐，并用 user/target/history adapter 融合推荐特征。高频物品优先走预计算缓存，低频或未命中物品在线编码，同时只融合与 target 最相关的历史。 Fidelity: 完整核心链路复现。真实执行 teacher 知识生成、T5 自回归蒸馏、student q/v-LoRA CTR 对齐、多层特征 adapter、频次自适应缓存/在线计算和相关历史融合；生产广告特征与缓存服务未复刻。本地对照口径：基线是 ID-only CTR ranker；实验组是完整 MSD；AUC 从 0.68449 升至 0.69510（+1.55%）。这是 LLM 蒸馏与缓存语义特征的联合消融，不是相对 DIN。  LLM distillation CTR serving efficiency 搜广推 语义表征、用户知识与冷启动 MSD 的 MKDM 与 MKIM 为什么分成知识蒸馏和 CTR 适配两步？ 先自回归学习教师关键词与推理，让小学生取得可迁移语义，再用 LoRA 和推荐 adapter 连接实际点击目标，避免静态知识不能随任务调整。两个阶段的监督和参数范围不同，蒸馏 loss 降低不等于 CTR 一定提高。 示意：先教学生理解外套保暖和通勤属性，再用用户点击训练如何组合这些属性；只复制描述向量不会自动完成后一任务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-msd-3339b303" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2fb8ddb268dd09af">MSD 的 MKDM 与 MKIM 为什么分成知识蒸馏和 CTR 适配两步？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amsd">Balancing Efficiency and Effectiveness: An LLM-Infused Approach for Optimized CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>先自回归学习教师关键词与推理，让小学生取得可迁移语义，再用 LoRA 和推荐 adapter 连接实际点击目标，避免静态知识不能随任务调整。两个阶段的监督和参数范围不同，蒸馏 loss 降低不等于 CTR 一定提高。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先教学生理解外套保暖和通勤属性，再用用户点击训练如何组合这些属性；只复制描述向量不会自动完成后一任务。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2412.06860">原论文</a> · <a href="../../../../reproductions/2412.06860-msd/">实现解读</a> · <a href="#qa-2fb8ddb268dd09af">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:msd" data-paper-title="Balancing Efficiency and Effectiveness: An LLM-Infused Approach for Optimized CTR Prediction" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Balancing Efficiency and Effectiveness: An LLM-Infused Approach for Optimized CTR Prediction 搜广推与 LLM 应用 Meituan 2024-12-09 直接在 CTR 链路调用大模型效果好但成本不可接受；只缓存静态 embedding 又无法跟随 CTR 目标更新。MSD 的 MKDM 先让大 teacher 为用户和物品生成关键词与推理，再让较小 student 自回归学习这些输出。MKIM 对蒸馏后的 student 做 LoRA CTR 对齐，并用 user/target/history adapter 融合推荐特征。高频物品优先走预计算缓存，低频或未命中物品在线编码，同时只融合与 target 最相关的历史。 Fidelity: 完整核心链路复现。真实执行 teacher 知识生成、T5 自回归蒸馏、student q/v-LoRA CTR 对齐、多层特征 adapter、频次自适应缓存/在线计算和相关历史融合；生产广告特征与缓存服务未复刻。本地对照口径：基线是 ID-only CTR ranker；实验组是完整 MSD；AUC 从 0.68449 升至 0.69510（+1.55%）。这是 LLM 蒸馏与缓存语义特征的联合消融，不是相对 DIN。  LLM distillation CTR serving efficiency 搜广推 语义表征、用户知识与冷启动 MSD 为什么先蒸馏大模型的关键词与推理，再对学生做 CTR 对齐，而不只缓存大模型 embedding？ 静态 embedding 能降低推理成本，却不会随点击目标调整。MSD 先让小学生通过自回归蒸馏学到教师的语义输出，再用 LoRA 和推荐适配器学习 CTR 相关表示。高频物品优先使用缓存，未命中部分在线编码，并只融合相关历史；这同时处理语义迁移、任务适配与服务成本，而非一次静态特征提取。 示意：教师离线解释一件外套的保暖与通勤属性，学生学会这种语义。CTR 阶段再根据用户行为调整表示；热门外套直接读缓存，新商品才触发在线编码。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-517fad13ebc6e70b">MSD 为什么先蒸馏大模型的关键词与推理，再对学生做 CTR 对齐，而不只缓存大模型 embedding？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amsd">Balancing Efficiency and Effectiveness: An LLM-Infused Approach for Optimized CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>静态 embedding 能降低推理成本，却不会随点击目标调整。MSD 先让小学生通过自回归蒸馏学到教师的语义输出，再用 LoRA 和推荐适配器学习 CTR 相关表示。高频物品优先使用缓存，未命中部分在线编码，并只融合相关历史；这同时处理语义迁移、任务适配与服务成本，而非一次静态特征提取。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教师离线解释一件外套的保暖与通勤属性，学生学会这种语义。CTR 阶段再根据用户行为调整表示；热门外套直接读缓存，新商品才触发在线编码。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2412.06860">原论文</a> · <a href="../../../../reproductions/2412.06860-msd/">实现解读</a> · <a href="#qa-517fad13ebc6e70b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:msd" data-paper-title="Balancing Efficiency and Effectiveness: An LLM-Infused Approach for Optimized CTR Prediction" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Balancing Efficiency and Effectiveness: An LLM-Infused Approach for Optimized CTR Prediction 搜广推与 LLM 应用 Meituan 2024-12-09 直接在 CTR 链路调用大模型效果好但成本不可接受；只缓存静态 embedding 又无法跟随 CTR 目标更新。MSD 的 MKDM 先让大 teacher 为用户和物品生成关键词与推理，再让较小 student 自回归学习这些输出。MKIM 对蒸馏后的 student 做 LoRA CTR 对齐，并用 user/target/history adapter 融合推荐特征。高频物品优先走预计算缓存，低频或未命中物品在线编码，同时只融合与 target 最相关的历史。 Fidelity: 完整核心链路复现。真实执行 teacher 知识生成、T5 自回归蒸馏、student q/v-LoRA CTR 对齐、多层特征 adapter、频次自适应缓存/在线计算和相关历史融合；生产广告特征与缓存服务未复刻。本地对照口径：基线是 ID-only CTR ranker；实验组是完整 MSD；AUC 从 0.68449 升至 0.69510（+1.55%）。这是 LLM 蒸馏与缓存语义特征的联合消融，不是相对 DIN。  LLM distillation CTR serving efficiency 搜广推 语义表征、用户知识与冷启动 MSD 高频缓存、低频在线与全部在线编码，相比依什么分摊计算？ 常出现物品预计算复用收益大，低频和未命中内容走在线补充，兼顾成本与覆盖；全部在线更及时却重复高频工作。缓存表示与当前 LoRA 版本可能不一致，刷新与命中率影响收益。来源本地未复刻生产 embedding 服务，不能按结构推真实效率。 示意：热门外套一天被评百万次可缓存，新上架雨衣先在线编码；若 LoRA 更新后缓存仍旧，频次门控就可能选择过时语义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e66fc937b374d9f9">MSD 高频缓存、低频在线与全部在线编码，相比依什么分摊计算？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amsd">Balancing Efficiency and Effectiveness: An LLM-Infused Approach for Optimized CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>常出现物品预计算复用收益大，低频和未命中内容走在线补充，兼顾成本与覆盖；全部在线更及时却重复高频工作。缓存表示与当前 LoRA 版本可能不一致，刷新与命中率影响收益。来源本地未复刻生产 embedding 服务，不能按结构推真实效率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>热门外套一天被评百万次可缓存，新上架雨衣先在线编码；若 LoRA 更新后缓存仍旧，频次门控就可能选择过时语义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2412.06860">原论文</a> · <a href="../../../../reproductions/2412.06860-msd/">实现解读</a> · <a href="#qa-e66fc937b374d9f9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:msd" data-paper-title="Balancing Efficiency and Effectiveness: An LLM-Infused Approach for Optimized CTR Prediction" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Balancing Efficiency and Effectiveness: An LLM-Infused Approach for Optimized CTR Prediction 搜广推与 LLM 应用 Meituan 2024-12-09 直接在 CTR 链路调用大模型效果好但成本不可接受；只缓存静态 embedding 又无法跟随 CTR 目标更新。MSD 的 MKDM 先让大 teacher 为用户和物品生成关键词与推理，再让较小 student 自回归学习这些输出。MKIM 对蒸馏后的 student 做 LoRA CTR 对齐，并用 user/target/history adapter 融合推荐特征。高频物品优先走预计算缓存，低频或未命中物品在线编码，同时只融合与 target 最相关的历史。 Fidelity: 完整核心链路复现。真实执行 teacher 知识生成、T5 自回归蒸馏、student q/v-LoRA CTR 对齐、多层特征 adapter、频次自适应缓存/在线计算和相关历史融合；生产广告特征与缓存服务未复刻。本地对照口径：基线是 ID-only CTR ranker；实验组是完整 MSD；AUC 从 0.68449 升至 0.69510（+1.55%）。这是 LLM 蒸馏与缓存语义特征的联合消融，不是相对 DIN。  LLM distillation CTR serving efficiency 搜广推 语义表征、用户知识与冷启动 MSD 本地历史 top-3 与缓存 gate，为什么要分别检查候选相关和共享部分？ 历史选取依 target 相似度，每个候选可得到不同子集；item 缓存则是可复用语义，不应夹带用户或目标专属交互。冻结 student 主干后仅更新约定 LoRA，需核对真实参数范围。两路混淆会让缓存污染或候选相关性消失。 示意：相机选摄影历史、跑鞋选运动历史，二者不能共用相机选过的 top-3；同一商品基础语义可共享，但筛选结果属于当前配对。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0de515730baa43a9">MSD 本地历史 top-3 与缓存 gate，为什么要分别检查候选相关和共享部分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amsd">Balancing Efficiency and Effectiveness: An LLM-Infused Approach for Optimized CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>历史选取依 target 相似度，每个候选可得到不同子集；item 缓存则是可复用语义，不应夹带用户或目标专属交互。冻结 student 主干后仅更新约定 LoRA，需核对真实参数范围。两路混淆会让缓存污染或候选相关性消失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>相机选摄影历史、跑鞋选运动历史，二者不能共用相机选过的 top-3；同一商品基础语义可共享，但筛选结果属于当前配对。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2412.06860">原论文</a> · <a href="../../../../reproductions/2412.06860-msd/">实现解读</a> · <a href="#qa-0de515730baa43a9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:precise" data-paper-title="PRECISE: Pre-training Sequential Recommenders with Collaborative and Semantic Information" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="PRECISE: Pre-training Sequential Recommenders with Collaborative and Semantic Information 搜广推与 LLM 应用 Tencent / WeChat 2024-12-09 纯 ID 序列模型能学协同关系，但长尾物品训练不足；纯文本/LLM 方法能迁移语义，却容易丢掉协同信号。PRECISE 将二者在 item 层融合，并把训练拆为 Universal Training（全场景兴趣）和 Targeted Training（稀疏目标场景/任务）。论文还针对文本表示过强导致 ID 学不动的问题，先冻结 token 训练 ID，再解冻联合训练。 Fidelity: 完整核心链路复现。实际执行 LLM token hidden-state 初始化、可训练 token、top-k MoE attention、ID/text 交替训练、全场景 causal NIP、目标场景双向 Transformer、序列拼接 MLP 与 cross-user BPR。Qwen2-1.5B 缩为 SmolLM2-135M，WeChat 私有日志替换为 MovieLens-1M。本地对照口径：基线是只做目标任务训练的 PRECISE-TT；实验组是 UT 全场景预训练后再 TT；  LLM semantic embedding sequential pre-training MoE targeted training 搜广推 语义表征、用户知识与冷启动 PRECISE 的 UT 与 TT 为什么分别面向全场景兴趣和稀疏目标？ 全场景训练利用更丰富序列获得基本偏好，目标训练再适配较少标签的具体需求，使稀疏任务不完全从零开始。两阶段目标与注意力规则不同，迁移也可能伤冷尾。来源总体提升而 Cold Recall 下降，不能宣称全面改善冷启动。 示意：所有正反馈训练兴趣后，再学高评分偏好；学到热门模式可提高总命中，却未必让新电影更易被推荐。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-precise-dd30948e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5ddcf43cd4f766e7">PRECISE 的 UT 与 TT 为什么分别面向全场景兴趣和稀疏目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aprecise">PRECISE: Pre-training Sequential Recommenders with Collaborative and Semantic Information</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent / WeChat</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全场景训练利用更丰富序列获得基本偏好，目标训练再适配较少标签的具体需求，使稀疏任务不完全从零开始。两阶段目标与注意力规则不同，迁移也可能伤冷尾。来源总体提升而 Cold Recall 下降，不能宣称全面改善冷启动。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>所有正反馈训练兴趣后，再学高评分偏好；学到热门模式可提高总命中，却未必让新电影更易被推荐。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2412.06308">原论文</a> · <a href="../../../../reproductions/2412.06308-precise/">实现解读</a> · <a href="#qa-5ddcf43cd4f766e7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:precise" data-paper-title="PRECISE: Pre-training Sequential Recommenders with Collaborative and Semantic Information" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="PRECISE: Pre-training Sequential Recommenders with Collaborative and Semantic Information 搜广推与 LLM 应用 Tencent / WeChat 2024-12-09 纯 ID 序列模型能学协同关系，但长尾物品训练不足；纯文本/LLM 方法能迁移语义，却容易丢掉协同信号。PRECISE 将二者在 item 层融合，并把训练拆为 Universal Training（全场景兴趣）和 Targeted Training（稀疏目标场景/任务）。论文还针对文本表示过强导致 ID 学不动的问题，先冻结 token 训练 ID，再解冻联合训练。 Fidelity: 完整核心链路复现。实际执行 LLM token hidden-state 初始化、可训练 token、top-k MoE attention、ID/text 交替训练、全场景 causal NIP、目标场景双向 Transformer、序列拼接 MLP 与 cross-user BPR。Qwen2-1.5B 缩为 SmolLM2-135M，WeChat 私有日志替换为 MovieLens-1M。本地对照口径：基线是只做目标任务训练的 PRECISE-TT；实验组是 UT 全场景预训练后再 TT；  LLM semantic embedding sequential pre-training MoE targeted training 搜广推 语义表征、用户知识与冷启动 PRECISE 为什么先冻结文本表示训练 ID，再解冻联合训练？ 预训练文本表示一开始可能远强于随机 ID 分支，优化器容易直接依赖文本，使 ID 得不到足够学习，协同信息因而缺席。先固定文本侧迫使 ID 学到可用差异，再联合训练让两者互补。全场景预训练到稀疏目标任务适配则解决迁移范围；总体指标改善并不保证长尾或冷启动子集同步改善。 示意：两部题材相近的电影文本很像，用户群却不同。若模型一直靠文本完成训练，ID 难学到群体差别；分阶段训练让 ID 先获得区分能力，再融合语义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-74ac61e57c3c2e60">PRECISE 为什么先冻结文本表示训练 ID，再解冻联合训练？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aprecise">PRECISE: Pre-training Sequential Recommenders with Collaborative and Semantic Information</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent / WeChat</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>预训练文本表示一开始可能远强于随机 ID 分支，优化器容易直接依赖文本，使 ID 得不到足够学习，协同信息因而缺席。先固定文本侧迫使 ID 学到可用差异，再联合训练让两者互补。全场景预训练到稀疏目标任务适配则解决迁移范围；总体指标改善并不保证长尾或冷启动子集同步改善。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两部题材相近的电影文本很像，用户群却不同。若模型一直靠文本完成训练，ID 难学到群体差别；分阶段训练让 ID 先获得区分能力，再融合语义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2412.06308">原论文</a> · <a href="../../../../reproductions/2412.06308-precise/">实现解读</a> · <a href="#qa-74ac61e57c3c2e60">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:precise" data-paper-title="PRECISE: Pre-training Sequential Recommenders with Collaborative and Semantic Information" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="PRECISE: Pre-training Sequential Recommenders with Collaborative and Semantic Information 搜广推与 LLM 应用 Tencent / WeChat 2024-12-09 纯 ID 序列模型能学协同关系，但长尾物品训练不足；纯文本/LLM 方法能迁移语义，却容易丢掉协同信号。PRECISE 将二者在 item 层融合，并把训练拆为 Universal Training（全场景兴趣）和 Targeted Training（稀疏目标场景/任务）。论文还针对文本表示过强导致 ID 学不动的问题，先冻结 token 训练 ID，再解冻联合训练。 Fidelity: 完整核心链路复现。实际执行 LLM token hidden-state 初始化、可训练 token、top-k MoE attention、ID/text 交替训练、全场景 causal NIP、目标场景双向 Transformer、序列拼接 MLP 与 cross-user BPR。Qwen2-1.5B 缩为 SmolLM2-135M，WeChat 私有日志替换为 MovieLens-1M。本地对照口径：基线是只做目标任务训练的 PRECISE-TT；实验组是 UT 全场景预训练后再 TT；  LLM semantic embedding sequential pre-training MoE targeted training 搜广推 语义表征、用户知识与冷启动 PRECISE 的 token attention MoE 与单独平均文本向量，相比保留哪些可选择细节？ 顺序 token 表示允许专家关注不同词段，top-k gate 组合多种语义视角，平均向量提前压平差别。它增加容量也可能重复或由强文本压制 ID，因此先冻结文本训练 ID。更多专家不能代替实际互补和冷尾证据。 示意：标题里“初学者”和“专业版”小词可由不同专家聚焦，简单均值可能淡化；但若所有专家只盯热门演员名，细节仍未真正保留。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-01d083c1aec8b3be">PRECISE 的 token attention MoE 与单独平均文本向量，相比保留哪些可选择细节？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aprecise">PRECISE: Pre-training Sequential Recommenders with Collaborative and Semantic Information</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent / WeChat</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>顺序 token 表示允许专家关注不同词段，top-k gate 组合多种语义视角，平均向量提前压平差别。它增加容量也可能重复或由强文本压制 ID，因此先冻结文本训练 ID。更多专家不能代替实际互补和冷尾证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>标题里“初学者”和“专业版”小词可由不同专家聚焦，简单均值可能淡化；但若所有专家只盯热门演员名，细节仍未真正保留。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2412.06308">原论文</a> · <a href="../../../../reproductions/2412.06308-precise/">实现解读</a> · <a href="#qa-01d083c1aec8b3be">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:precise" data-paper-title="PRECISE: Pre-training Sequential Recommenders with Collaborative and Semantic Information" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="PRECISE: Pre-training Sequential Recommenders with Collaborative and Semantic Information 搜广推与 LLM 应用 Tencent / WeChat 2024-12-09 纯 ID 序列模型能学协同关系，但长尾物品训练不足；纯文本/LLM 方法能迁移语义，却容易丢掉协同信号。PRECISE 将二者在 item 层融合，并把训练拆为 Universal Training（全场景兴趣）和 Targeted Training（稀疏目标场景/任务）。论文还针对文本表示过强导致 ID 学不动的问题，先冻结 token 训练 ID，再解冻联合训练。 Fidelity: 完整核心链路复现。实际执行 LLM token hidden-state 初始化、可训练 token、top-k MoE attention、ID/text 交替训练、全场景 causal NIP、目标场景双向 Transformer、序列拼接 MLP 与 cross-user BPR。Qwen2-1.5B 缩为 SmolLM2-135M，WeChat 私有日志替换为 MovieLens-1M。本地对照口径：基线是只做目标任务训练的 PRECISE-TT；实验组是 UT 全场景预训练后再 TT；  LLM semantic embedding sequential pre-training MoE targeted training 搜广推 语义表征、用户知识与冷启动 PRECISE 从 causal UT 切到非 causal TT，为什么依然必须排除目标 item？ TT 可双向读取已知历史，并不允许看到待预测事件。最后目标须在构序列前留出，拼接所有位置的 MLP 只能处理合法输入。重复 item 的 in-batch 目标也需避免假互斥，源码修复过这一点，不能因切 mask 就放宽测试隔离。 示意：历史甲乙可互读，测试丙仍不能放进 TT 输入；非 causal 只改变历史内部可见性，不是给模型使用未来答案的权限。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-fbde951e57959a36">PRECISE 从 causal UT 切到非 causal TT，为什么依然必须排除目标 item？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aprecise">PRECISE: Pre-training Sequential Recommenders with Collaborative and Semantic Information</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent / WeChat</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>TT 可双向读取已知历史，并不允许看到待预测事件。最后目标须在构序列前留出，拼接所有位置的 MLP 只能处理合法输入。重复 item 的 in-batch 目标也需避免假互斥，源码修复过这一点，不能因切 mask 就放宽测试隔离。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>历史甲乙可互读，测试丙仍不能放进 TT 输入；非 causal 只改变历史内部可见性，不是给模型使用未来答案的权限。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2412.06308">原论文</a> · <a href="../../../../reproductions/2412.06308-precise/">实现解读</a> · <a href="#qa-fbde951e57959a36">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:learn" data-paper-title="Knowledge Adaptation from Large Language Model to Recommendation for Practical Industrial Application" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Knowledge Adaptation from Large Language Model to Recommendation for Practical Industrial Application 搜广推与 LLM 应用 Kuaishou 2024-05-07 直接把冻结 LLM embedding 用作推荐表示存在开放世界语义域与协同域的差距。LEARN 的 CEG 冻结 LLM 并平均池化 item 文本，PCH 用可训练因果 Transformer 从历史 content embeddings 学用户偏好，再投影到线上推荐空间。 Fidelity: 完整核心链路复现。真实执行冻结预训练 LM 的 CEG、缓存 item embedding、因果 PCH、dense all-position loss 和 online projection；BERT-tiny/MovieLens 替代 Baichuan2-7B/快手日志。本地对照口径：基线是 frozen LLM semantic mean；实验组是 LEARN CEG+PCH；NDCG@10 从 0.00487 升至 0.01622（+233.10%），同时 head share 升至 69.50%。这是知识适配模块消融，不是相对 DIN。  llm-recommendation knowledge-adaptation cold-start 搜广推 语义表征、用户知识与冷启动 LEARN 为什么冻结内容 LLM，却允许 PCH 学习偏好？ 通用 LLM 提供稳定内容语义，用户行为关系仍需推荐目标适配；PCH 读取内容序列并学习因果偏好，再投到线上空间。冻结减少成本但限制内容端调整，不能把预训知识直接等同协同偏好，也不能假设所有迁移都改善冷启动。 示意：两部同题材电影语义相近，但人群消费不同，PCH 可从观看序列学差别；如果只是均值冻结向量，偏好结构没有被任务训练。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-learn-c99c03ce" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e3fa0af7e5835487">LEARN 为什么冻结内容 LLM，却允许 PCH 学习偏好？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alearn">Knowledge Adaptation from Large Language Model to Recommendation for Practical Industrial Application</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>通用 LLM 提供稳定内容语义，用户行为关系仍需推荐目标适配；PCH 读取内容序列并学习因果偏好，再投到线上空间。冻结减少成本但限制内容端调整，不能把预训知识直接等同协同偏好，也不能假设所有迁移都改善冷启动。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两部同题材电影语义相近，但人群消费不同，PCH 可从观看序列学差别；如果只是均值冻结向量，偏好结构没有被任务训练。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2405.03988">原论文</a> · <a href="../../../../reproductions/2405.03988-learn/">实现解读</a> · <a href="#qa-e3fa0af7e5835487">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:learn" data-paper-title="Knowledge Adaptation from Large Language Model to Recommendation for Practical Industrial Application" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Knowledge Adaptation from Large Language Model to Recommendation for Practical Industrial Application 搜广推与 LLM 应用 Kuaishou 2024-05-07 直接把冻结 LLM embedding 用作推荐表示存在开放世界语义域与协同域的差距。LEARN 的 CEG 冻结 LLM 并平均池化 item 文本，PCH 用可训练因果 Transformer 从历史 content embeddings 学用户偏好，再投影到线上推荐空间。 Fidelity: 完整核心链路复现。真实执行冻结预训练 LM 的 CEG、缓存 item embedding、因果 PCH、dense all-position loss 和 online projection；BERT-tiny/MovieLens 替代 Baichuan2-7B/快手日志。本地对照口径：基线是 frozen LLM semantic mean；实验组是 LEARN CEG+PCH；NDCG@10 从 0.00487 升至 0.01622（+233.10%），同时 head share 升至 69.50%。这是知识适配模块消融，不是相对 DIN。  llm-recommendation knowledge-adaptation cold-start 搜广推 语义表征、用户知识与冷启动 LEARN为什么冻结LLM内容编码，却训练因果PCH来学习用户偏好？ 冻结内容编码保留开放世界语义并降低更新成本，但内容接近不等于共同消费。PCH在历史内容向量上学习顺序与下一物品目标，再投影到推荐空间，把通用语义转成偏好表示。模型仍需遵守历史时间边界；冻结LLM不意味着整个系统没有训练，也不能仅凭语义相似度判断迁移完成。 示意：两部电影文本都写冒险，用户却偏好其中一种叙事风格；固定内容向量给出基础语义，训练过的PCH可从其真实观看顺序中学习更细偏好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-2eed10f4831732c0">LEARN为什么冻结LLM内容编码，却训练因果PCH来学习用户偏好？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alearn">Knowledge Adaptation from Large Language Model to Recommendation for Practical Industrial Application</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冻结内容编码保留开放世界语义并降低更新成本，但内容接近不等于共同消费。PCH在历史内容向量上学习顺序与下一物品目标，再投影到推荐空间，把通用语义转成偏好表示。模型仍需遵守历史时间边界；冻结LLM不意味着整个系统没有训练，也不能仅凭语义相似度判断迁移完成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两部电影文本都写冒险，用户却偏好其中一种叙事风格；固定内容向量给出基础语义，训练过的PCH可从其真实观看顺序中学习更细偏好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2405.03988">原论文</a> · <a href="../../../../reproductions/2405.03988-learn/">实现解读</a> · <a href="#qa-2eed10f4831732c0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:learn" data-paper-title="Knowledge Adaptation from Large Language Model to Recommendation for Practical Industrial Application" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Knowledge Adaptation from Large Language Model to Recommendation for Practical Industrial Application 搜广推与 LLM 应用 Kuaishou 2024-05-07 直接把冻结 LLM embedding 用作推荐表示存在开放世界语义域与协同域的差距。LEARN 的 CEG 冻结 LLM 并平均池化 item 文本，PCH 用可训练因果 Transformer 从历史 content embeddings 学用户偏好，再投影到线上推荐空间。 Fidelity: 完整核心链路复现。真实执行冻结预训练 LM 的 CEG、缓存 item embedding、因果 PCH、dense all-position loss 和 online projection；BERT-tiny/MovieLens 替代 Baichuan2-7B/快手日志。本地对照口径：基线是 frozen LLM semantic mean；实验组是 LEARN CEG+PCH；NDCG@10 从 0.00487 升至 0.01622（+233.10%），同时 head share 升至 69.50%。这是知识适配模块消融，不是相对 DIN。  llm-recommendation knowledge-adaptation cold-start 搜广推 语义表征、用户知识与冷启动 LEARN 相对 frozen semantic mean 的大增益，为什么不能直接称冷启动收益？ 均值基线缺少可训练偏好建模，PCH 增加序列学习可提高排名，但来源同时显示强烈头部集中。改善可能依赖热门协同而非更好理解新品。需要冷启动分组与匹配对照，不能把总体 NDCG 大百分比当所有群体受益。 示意：模型学会总推热门电影就可能大幅胜过语义均值，却未必帮新电影获得合适受众；总体指标与冷启结论不能互换。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d5d6d58a64e951ab">LEARN 相对 frozen semantic mean 的大增益，为什么不能直接称冷启动收益？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alearn">Knowledge Adaptation from Large Language Model to Recommendation for Practical Industrial Application</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>均值基线缺少可训练偏好建模，PCH 增加序列学习可提高排名，但来源同时显示强烈头部集中。改善可能依赖热门协同而非更好理解新品。需要冷启动分组与匹配对照，不能把总体 NDCG 大百分比当所有群体受益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型学会总推热门电影就可能大幅胜过语义均值，却未必帮新电影获得合适受众；总体指标与冷启结论不能互换。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2405.03988">原论文</a> · <a href="../../../../reproductions/2405.03988-learn/">实现解读</a> · <a href="#qa-d5d6d58a64e951ab">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:learn" data-paper-title="Knowledge Adaptation from Large Language Model to Recommendation for Practical Industrial Application" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Knowledge Adaptation from Large Language Model to Recommendation for Practical Industrial Application 搜广推与 LLM 应用 Kuaishou 2024-05-07 直接把冻结 LLM embedding 用作推荐表示存在开放世界语义域与协同域的差距。LEARN 的 CEG 冻结 LLM 并平均池化 item 文本，PCH 用可训练因果 Transformer 从历史 content embeddings 学用户偏好，再投影到线上推荐空间。 Fidelity: 完整核心链路复现。真实执行冻结预训练 LM 的 CEG、缓存 item embedding、因果 PCH、dense all-position loss 和 online projection；BERT-tiny/MovieLens 替代 Baichuan2-7B/快手日志。本地对照口径：基线是 frozen LLM semantic mean；实验组是 LEARN CEG+PCH；NDCG@10 从 0.00487 升至 0.01622（+233.10%），同时 head share 升至 69.50%。这是知识适配模块消融，不是相对 DIN。  llm-recommendation knowledge-adaptation cold-start 搜广推 语义表征、用户知识与冷启动 PCH 预测下一物品时，内容缓存冻结是否足以防止未来泄漏？ 不够。即使内容向量固定，PCH 输入序列仍需因果 mask 和截止，下一物品只在目标侧出现，池化也不能包含它。内容 encoder 版本与投影一致。冻结参数只说明没有梯度更新，不说明数据可见性正确。 示意：把测试电影的固定内容向量先放入历史，再猜它，依旧泄漏；“LLM 冻结”无法抵消模型已经读到目标这件事。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3fecff7cba4aa75c">PCH 预测下一物品时，内容缓存冻结是否足以防止未来泄漏？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alearn">Knowledge Adaptation from Large Language Model to Recommendation for Practical Industrial Application</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不够。即使内容向量固定，PCH 输入序列仍需因果 mask 和截止，下一物品只在目标侧出现，池化也不能包含它。内容 encoder 版本与投影一致。冻结参数只说明没有梯度更新，不说明数据可见性正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把测试电影的固定内容向量先放入历史，再猜它，依旧泄漏；“LLM 冻结”无法抵消模型已经读到目标这件事。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2405.03988">原论文</a> · <a href="../../../../reproductions/2405.03988-learn/">实现解读</a> · <a href="#qa-3fecff7cba4aa75c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:bahe" data-paper-title="Breaking the Length Barrier: LLM-Enhanced CTR Prediction in Long Textual User Behaviors" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Breaking the Length Barrier: LLM-Enhanced CTR Prediction in Long Textual User Behaviors 搜广推与 LLM 应用 Ant Group 2024-03-28 直接把长用户行为文本反复送入 LLM，会重复编码同一原子行为，并把低层语义提取与高层行为交互强耦合。BAHE 在浅层编码每个原子行为并离线存储；训练时只取行为向量，以更深的可训练层聚合，再与候选物品一起完成 CTR 预测。这样既缩短上层序列，也允许浅层异步、低频更新。 Fidelity: 完整核心链路复现。真实执行冻结浅层 LLM 的原子行为编码与落盘、可训练上层 Transformer 的行为聚合和 CTR 训练；生产 LLM/广告日志替换为 BERT-tiny/MovieLens-100K。本地对照口径：基线是逐样本运行完整文本上层微调；实验组是 BAHE 原子缓存与层次聚合；耗时 -53.61%，但 AUC -2.94%。这是效率—效果对照，不是准确率提升。  llm-recommendation ctr-ranking long-sequence efficiency 搜广推 语义表征、用户知识与冷启动 BAHE 的原子行为缓存与最终用户表示为什么不是同一种缓存？ 原子缓存保存单条内容经过浅层模型的编码，可跨历史组合复用；最终用户表示还依赖行为顺序、当前候选和高层交互。浅层异步更新把重复内容理解移出主路径，上层仍学习具体用户的组合。缓存粒度越细复用机会越多，但也要维护版本一致性与内容压缩损失。 示意：同一电影标题可只编码一次，不同用户按各自顺序读取该向量；用户甲和乙的最终兴趣仍不同，不能因共享原子缓存就共用最终评分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-bahe-7645b8ec" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-3738cc4f91a5ce4c">BAHE 的原子行为缓存与最终用户表示为什么不是同一种缓存？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Abahe">Breaking the Length Barrier: LLM-Enhanced CTR Prediction in Long Textual User Behaviors</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ant Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原子缓存保存单条内容经过浅层模型的编码，可跨历史组合复用；最终用户表示还依赖行为顺序、当前候选和高层交互。浅层异步更新把重复内容理解移出主路径，上层仍学习具体用户的组合。缓存粒度越细复用机会越多，但也要维护版本一致性与内容压缩损失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一电影标题可只编码一次，不同用户按各自顺序读取该向量；用户甲和乙的最终兴趣仍不同，不能因共享原子缓存就共用最终评分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2403.19347">原论文</a> · <a href="../../../../reproductions/2403.19347-bahe/">实现解读</a> · <a href="#qa-3738cc4f91a5ce4c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:bahe" data-paper-title="Breaking the Length Barrier: LLM-Enhanced CTR Prediction in Long Textual User Behaviors" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Breaking the Length Barrier: LLM-Enhanced CTR Prediction in Long Textual User Behaviors 搜广推与 LLM 应用 Ant Group 2024-03-28 直接把长用户行为文本反复送入 LLM，会重复编码同一原子行为，并把低层语义提取与高层行为交互强耦合。BAHE 在浅层编码每个原子行为并离线存储；训练时只取行为向量，以更深的可训练层聚合，再与候选物品一起完成 CTR 预测。这样既缩短上层序列，也允许浅层异步、低频更新。 Fidelity: 完整核心链路复现。真实执行冻结浅层 LLM 的原子行为编码与落盘、可训练上层 Transformer 的行为聚合和 CTR 训练；生产 LLM/广告日志替换为 BERT-tiny/MovieLens-100K。本地对照口径：基线是逐样本运行完整文本上层微调；实验组是 BAHE 原子缓存与层次聚合；耗时 -53.61%，但 AUC -2.94%。这是效率—效果对照，不是准确率提升。  llm-recommendation ctr-ranking long-sequence efficiency 搜广推 语义表征、用户知识与冷启动 BAHE缓存原子行为的浅层编码，为什么还需要在线训练的高层聚合？ 浅层主要提取单个行为文本的语义，可被不同请求重复使用；高层需要结合当前历史组合和候选判断兴趣，不能冻结为一份通用答案。分层把重复文本计算移出训练与请求路径，同时保留跨行为交互。缓存刷新过慢或压缩过强仍可能损害质量，效率改善不自动意味着准确率提高。 示意：一条电影标题只编码一次，但用户把它与科幻片还是家庭片一起看，会改变高层兴趣判断；遇到不同候选时也应重新聚合这些行为向量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-0e6d87b8ce07426e">BAHE缓存原子行为的浅层编码，为什么还需要在线训练的高层聚合？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Abahe">Breaking the Length Barrier: LLM-Enhanced CTR Prediction in Long Textual User Behaviors</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ant Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>浅层主要提取单个行为文本的语义，可被不同请求重复使用；高层需要结合当前历史组合和候选判断兴趣，不能冻结为一份通用答案。分层把重复文本计算移出训练与请求路径，同时保留跨行为交互。缓存刷新过慢或压缩过强仍可能损害质量，效率改善不自动意味着准确率提高。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一条电影标题只编码一次，但用户把它与科幻片还是家庭片一起看，会改变高层兴趣判断；遇到不同候选时也应重新聚合这些行为向量。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2403.19347">原论文</a> · <a href="../../../../reproductions/2403.19347-bahe/">实现解读</a> · <a href="#qa-0e6d87b8ce07426e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:bahe" data-paper-title="Breaking the Length Barrier: LLM-Enhanced CTR Prediction in Long Textual User Behaviors" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Breaking the Length Barrier: LLM-Enhanced CTR Prediction in Long Textual User Behaviors 搜广推与 LLM 应用 Ant Group 2024-03-28 直接把长用户行为文本反复送入 LLM，会重复编码同一原子行为，并把低层语义提取与高层行为交互强耦合。BAHE 在浅层编码每个原子行为并离线存储；训练时只取行为向量，以更深的可训练层聚合，再与候选物品一起完成 CTR 预测。这样既缩短上层序列，也允许浅层异步、低频更新。 Fidelity: 完整核心链路复现。真实执行冻结浅层 LLM 的原子行为编码与落盘、可训练上层 Transformer 的行为聚合和 CTR 训练；生产 LLM/广告日志替换为 BERT-tiny/MovieLens-100K。本地对照口径：基线是逐样本运行完整文本上层微调；实验组是 BAHE 原子缓存与层次聚合；耗时 -53.61%，但 AUC -2.94%。这是效率—效果对照，不是准确率提升。  llm-recommendation ctr-ranking long-sequence efficiency 搜广推 语义表征、用户知识与冷启动 BAHE 与每个样本都重新跑完整文本模型相比，节省来源与效果代价怎样区分？ 节省主要来自不再重复执行相同文本的浅层编码，上层处理的是行为数量而非全部词 token。压缩边界减少细节并改变模型容量，因此需要同时测耗时与质量。本地耗时下降伴随 AUC 下降，只支持效率机制，不能写成效果无损的等价替换。 示意：十个历史标题原有上百词，缓存后上层只读十个行为向量；运行更快，但某个关键措辞若被压掉，排序可能受损，两种指标应一起看。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-cdffe7e92c04133d">BAHE 与每个样本都重新跑完整文本模型相比，节省来源与效果代价怎样区分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Abahe">Breaking the Length Barrier: LLM-Enhanced CTR Prediction in Long Textual User Behaviors</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ant Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>节省主要来自不再重复执行相同文本的浅层编码，上层处理的是行为数量而非全部词 token。压缩边界减少细节并改变模型容量，因此需要同时测耗时与质量。本地耗时下降伴随 AUC 下降，只支持效率机制，不能写成效果无损的等价替换。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>十个历史标题原有上百词，缓存后上层只读十个行为向量；运行更快，但某个关键措辞若被压掉，排序可能受损，两种指标应一起看。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2403.19347">原论文</a> · <a href="../../../../reproductions/2403.19347-bahe/">实现解读</a> · <a href="#qa-cdffe7e92c04133d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:bahe" data-paper-title="Breaking the Length Barrier: LLM-Enhanced CTR Prediction in Long Textual User Behaviors" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Breaking the Length Barrier: LLM-Enhanced CTR Prediction in Long Textual User Behaviors 搜广推与 LLM 应用 Ant Group 2024-03-28 直接把长用户行为文本反复送入 LLM，会重复编码同一原子行为，并把低层语义提取与高层行为交互强耦合。BAHE 在浅层编码每个原子行为并离线存储；训练时只取行为向量，以更深的可训练层聚合，再与候选物品一起完成 CTR 预测。这样既缩短上层序列，也允许浅层异步、低频更新。 Fidelity: 完整核心链路复现。真实执行冻结浅层 LLM 的原子行为编码与落盘、可训练上层 Transformer 的行为聚合和 CTR 训练；生产 LLM/广告日志替换为 BERT-tiny/MovieLens-100K。本地对照口径：基线是逐样本运行完整文本上层微调；实验组是 BAHE 原子缓存与层次聚合；耗时 -53.61%，但 AUC -2.94%。这是效率—效果对照，不是准确率提升。  llm-recommendation ctr-ranking long-sequence efficiency 搜广推 语义表征、用户知识与冷启动 BAHE 本地两层 BERT-tiny 怎样划分缓存层和训练层？ 来源用第一层生成 MovieLens 标题原子向量并缓存，复制上层处理 CLS、十二条历史与候选；对照逐样本运行冻结低层和可训练上层。两边需共享数据与预算，缓存也应绑定相同浅层版本。小模型仅两层，不能由该耗时比例推算生产大模型收益。 示意：若缓存由旧版第一层生成，上层却换成另一版编码器，接口语义会失配；应把向量版本与上层配置一起记录，而非只保留一个裸数组。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c1dad8a6e15629cc">BAHE 本地两层 BERT-tiny 怎样划分缓存层和训练层？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Abahe">Breaking the Length Barrier: LLM-Enhanced CTR Prediction in Long Textual User Behaviors</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ant Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>来源用第一层生成 MovieLens 标题原子向量并缓存，复制上层处理 CLS、十二条历史与候选；对照逐样本运行冻结低层和可训练上层。两边需共享数据与预算，缓存也应绑定相同浅层版本。小模型仅两层，不能由该耗时比例推算生产大模型收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>若缓存由旧版第一层生成，上层却换成另一版编码器，接口语义会失配；应把向量版本与上层配置一起记录，而非只保留一个裸数组。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2403.19347">原论文</a> · <a href="../../../../reproductions/2403.19347-bahe/">实现解读</a> · <a href="#qa-c1dad8a6e15629cc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:lsvcr" data-paper-title="A Large Language Model Enhanced Sequential Recommender for Joint Video and Comment Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="A Large Language Model Enhanced Sequential Recommender for Joint Video and Comment Recommendation 搜广推与 LLM 应用 Kuaishou 2024-03-20 短视频用户会同时消费视频和评论。纯序列模型能高效服务，但难以理解评论语义；直接让 LLM 在线推荐又太慢。LSVCR 用 LLM 同时担任离线文本 encoder 和仅训练期存在的 supplemental recommender，再把 LLM 的个性化偏好对齐到可部署的双序列 SR 模型。部署时不需要运行生成式 LLM。 对齐 loss 明显下降，排除了 alignment 根本未训练的情况。Fidelity: 完整核心链路复现。真实执行 causal LM q/v-LoRA SFT、LLM 文本编码、随机位置扩展、商品/评论双 Transformer、双向 cross-attention、SSC/VCC 对齐和联合微调；ChatGLM3 与快手私有日志缩小替换。本地对照口径：基线是相同 SR 网络但不做 LLM preference alignment；实验组是完整 LSVCR；Comment NDCG@10 +50.40%，Item NDCG@10 -56.42%。这是 alignment 消融，不能概括成整体推荐效果提升。  LLM recommendation comment recommendation preference alignment 搜广推 语义表征、用户知识与冷启动 LSVCR 为什么分别编码视频消费与评论消费，而不把评论只当视频文本属性？ 评论有自己的阅读行为和语义偏好，不等同于视频附属元数据。双序列先保留两类行为，再交叉融合，LLM 训练期补充个性化语义。共同消费可有关联也可冲突，不能默认评论端变好就说明视频端同样改善。 示意：用户不喜欢某视频却爱看其讨论，评论消费与视频点击方向可能不同；只把评论拼进视频介绍会丢掉这种独立偏好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-lsvcr-e1dd0222" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-dbc93eb9f52f98ed">LSVCR 为什么分别编码视频消费与评论消费，而不把评论只当视频文本属性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alsvcr">A Large Language Model Enhanced Sequential Recommender for Joint Video and Comment Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>评论有自己的阅读行为和语义偏好，不等同于视频附属元数据。双序列先保留两类行为，再交叉融合，LLM 训练期补充个性化语义。共同消费可有关联也可冲突，不能默认评论端变好就说明视频端同样改善。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户不喜欢某视频却爱看其讨论，评论消费与视频点击方向可能不同；只把评论拼进视频介绍会丢掉这种独立偏好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2403.13574">原论文</a> · <a href="../../../../reproductions/2403.13574-lsvcr/">实现解读</a> · <a href="#qa-dbc93eb9f52f98ed">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:lsvcr" data-paper-title="A Large Language Model Enhanced Sequential Recommender for Joint Video and Comment Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="A Large Language Model Enhanced Sequential Recommender for Joint Video and Comment Recommendation 搜广推与 LLM 应用 Kuaishou 2024-03-20 短视频用户会同时消费视频和评论。纯序列模型能高效服务，但难以理解评论语义；直接让 LLM 在线推荐又太慢。LSVCR 用 LLM 同时担任离线文本 encoder 和仅训练期存在的 supplemental recommender，再把 LLM 的个性化偏好对齐到可部署的双序列 SR 模型。部署时不需要运行生成式 LLM。 对齐 loss 明显下降，排除了 alignment 根本未训练的情况。Fidelity: 完整核心链路复现。真实执行 causal LM q/v-LoRA SFT、LLM 文本编码、随机位置扩展、商品/评论双 Transformer、双向 cross-attention、SSC/VCC 对齐和联合微调；ChatGLM3 与快手私有日志缩小替换。本地对照口径：基线是相同 SR 网络但不做 LLM preference alignment；实验组是完整 LSVCR；Comment NDCG@10 +50.40%，Item NDCG@10 -56.42%。这是 alignment 消融，不能概括成整体推荐效果提升。  LLM recommendation comment recommendation preference alignment 搜广推 语义表征、用户知识与冷启动 LSVCR上线不用生成式LLM，为什么训练时还让LLM提供个性化偏好？ 视频和评论包含不同语义，纯ID序列难以充分理解，LLM偏好可在训练中补充内容关系。双序列模型通过交叉融合及对齐目标吸收这些知识，部署时只保留可服务的推荐模型。两种任务可能相互牵制，本地评论与视频指标方向不同，不能只报告某一路改善就宣称整体成功。 示意：一条评论表达反讽，视频点击本身看不出来；训练期教师可补充语义，但上线学生仍需仅凭可用双序列作判断，不能每次暗中调用老师解释。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-189ea1f5c254e5d0">LSVCR上线不用生成式LLM，为什么训练时还让LLM提供个性化偏好？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alsvcr">A Large Language Model Enhanced Sequential Recommender for Joint Video and Comment Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>视频和评论包含不同语义，纯ID序列难以充分理解，LLM偏好可在训练中补充内容关系。双序列模型通过交叉融合及对齐目标吸收这些知识，部署时只保留可服务的推荐模型。两种任务可能相互牵制，本地评论与视频指标方向不同，不能只报告某一路改善就宣称整体成功。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一条评论表达反讽，视频点击本身看不出来；训练期教师可补充语义，但上线学生仍需仅凭可用双序列作判断，不能每次暗中调用老师解释。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2403.13574">原论文</a> · <a href="../../../../reproductions/2403.13574-lsvcr/">实现解读</a> · <a href="#qa-189ea1f5c254e5d0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:lsvcr" data-paper-title="A Large Language Model Enhanced Sequential Recommender for Joint Video and Comment Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="A Large Language Model Enhanced Sequential Recommender for Joint Video and Comment Recommendation 搜广推与 LLM 应用 Kuaishou 2024-03-20 短视频用户会同时消费视频和评论。纯序列模型能高效服务，但难以理解评论语义；直接让 LLM 在线推荐又太慢。LSVCR 用 LLM 同时担任离线文本 encoder 和仅训练期存在的 supplemental recommender，再把 LLM 的个性化偏好对齐到可部署的双序列 SR 模型。部署时不需要运行生成式 LLM。 对齐 loss 明显下降，排除了 alignment 根本未训练的情况。Fidelity: 完整核心链路复现。真实执行 causal LM q/v-LoRA SFT、LLM 文本编码、随机位置扩展、商品/评论双 Transformer、双向 cross-attention、SSC/VCC 对齐和联合微调；ChatGLM3 与快手私有日志缩小替换。本地对照口径：基线是相同 SR 网络但不做 LLM preference alignment；实验组是完整 LSVCR；Comment NDCG@10 +50.40%，Item NDCG@10 -56.42%。这是 alignment 消融，不能概括成整体推荐效果提升。  LLM recommendation comment recommendation preference alignment 搜广推 语义表征、用户知识与冷启动 LSVCR 的 SSC 与 VCC 分别约束哪些关系？ SSC 对齐序列推荐器与 LLM 的用户偏好，VCC 联系视频或商品偏好与评论偏好，前者跨模型、后者跨消费对象。两个目标不能互代，可能带来任务冲突。来源本地评论端提高但商品端退化，必须按两任务报告而非概括整体提升。 示意：小模型要学懂 LLM 的摄影偏好是一项，判断摄影商品兴趣与评论阅读是否一致又是一项；一项对齐好不代表另一项无害。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-678f95df550c57b9">LSVCR 的 SSC 与 VCC 分别约束哪些关系？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alsvcr">A Large Language Model Enhanced Sequential Recommender for Joint Video and Comment Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>SSC 对齐序列推荐器与 LLM 的用户偏好，VCC 联系视频或商品偏好与评论偏好，前者跨模型、后者跨消费对象。两个目标不能互代，可能带来任务冲突。来源本地评论端提高但商品端退化，必须按两任务报告而非概括整体提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>小模型要学懂 LLM 的摄影偏好是一项，判断摄影商品兴趣与评论阅读是否一致又是一项；一项对齐好不代表另一项无害。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2403.13574">原论文</a> · <a href="../../../../reproductions/2403.13574-lsvcr/">实现解读</a> · <a href="#qa-678f95df550c57b9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:lsvcr" data-paper-title="A Large Language Model Enhanced Sequential Recommender for Joint Video and Comment Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="A Large Language Model Enhanced Sequential Recommender for Joint Video and Comment Recommendation 搜广推与 LLM 应用 Kuaishou 2024-03-20 短视频用户会同时消费视频和评论。纯序列模型能高效服务，但难以理解评论语义；直接让 LLM 在线推荐又太慢。LSVCR 用 LLM 同时担任离线文本 encoder 和仅训练期存在的 supplemental recommender，再把 LLM 的个性化偏好对齐到可部署的双序列 SR 模型。部署时不需要运行生成式 LLM。 对齐 loss 明显下降，排除了 alignment 根本未训练的情况。Fidelity: 完整核心链路复现。真实执行 causal LM q/v-LoRA SFT、LLM 文本编码、随机位置扩展、商品/评论双 Transformer、双向 cross-attention、SSC/VCC 对齐和联合微调；ChatGLM3 与快手私有日志缩小替换。本地对照口径：基线是相同 SR 网络但不做 LLM preference alignment；实验组是完整 LSVCR；Comment NDCG@10 +50.40%，Item NDCG@10 -56.42%。这是 alignment 消融，不能概括成整体推荐效果提升。  LLM recommendation comment recommendation preference alignment 搜广推 语义表征、用户知识与冷启动 LSVCR 的随机位置编码为什么要抽有序子集而非打乱位置顺序？ 短 alignment 序列要覆盖完整位置表的跨度，但仍应保留行为先后；有序子集表达不均匀位置采样，随机打乱则改变时间关系。双向跨序列融合也只能用当时已发生记录，测试目标评论或视频不能提前进入任一侧。 示意：从完整位置一到一百抽三、二十、八十给三条历史，先后仍正确；赋八十、三、二十则让旧事件在位置上变成新事件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ccd0b0d9cfb4fb94">LSVCR 的随机位置编码为什么要抽有序子集而非打乱位置顺序？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alsvcr">A Large Language Model Enhanced Sequential Recommender for Joint Video and Comment Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>短 alignment 序列要覆盖完整位置表的跨度，但仍应保留行为先后；有序子集表达不均匀位置采样，随机打乱则改变时间关系。双向跨序列融合也只能用当时已发生记录，测试目标评论或视频不能提前进入任一侧。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>从完整位置一到一百抽三、二十、八十给三条历史，先后仍正确；赋八十、三、二十则让旧事件在位置上变成新事件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2403.13574">原论文</a> · <a href="../../../../reproductions/2403.13574-lsvcr/">实现解读</a> · <a href="#qa-ccd0b0d9cfb4fb94">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:notellm" data-paper-title="NoteLLM: A Retrievable Large Language Model for Note Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="NoteLLM: A Retrievable Large Language Model for Note Recommendation 搜广推与 LLM 应用 Xiaohongshu 2024-03-04 纯文本 embedding 缺少协同信号，纯对比学习又可能损害 LLM 生成能力。NoteLLM 用统一 compression prompt 将内容压到特殊 token；GCL 拉近用户共读 note，CSFT 从同一压缩状态生成 hashtag/category。 Fidelity: 完整核心链路复现。真实执行 note compression special token、行为共现 GCL、类别生成 CSFT 和压缩状态 I2I 检索；T5-small/MovieLens 替代 7B LLM/小红书 note。本地对照口径：基线是冻结 compression-state embedding；实验组是 NoteLLM 的 GCL+CSFT embedding；NDCG@10 从 0.01142 升至 0.01224（+7.15%）。这是表征训练消融，不是端到端排序模型相对 DIN 的提升。  llm-recommendation contrastive-learning i2i-retrieval 搜广推 语义表征、用户知识与冷启动 NoteLLM 的 compression token 为什么同时承担检索与生成接口？ 内容先压到一个特定状态，对比学习用它作为向量，生成任务也从同状态恢复标签类别，迫使压缩兼顾协同与语义。若生成器能绕过瓶颈读所有原文，约束含义就不同。压缩仍有损，不表示整个笔记细节可完整恢复。 示意：一枚状态既要把同兴趣笔记拉近，又需生成“露营装备”标签，不能只编码共读热门度而忘掉内容在讲什么。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-notellm-9364e133" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2cf64a8c96cdbab5">NoteLLM 的 compression token 为什么同时承担检索与生成接口？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Anotellm">NoteLLM: A Retrievable Large Language Model for Note Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>内容先压到一个特定状态，对比学习用它作为向量，生成任务也从同状态恢复标签类别，迫使压缩兼顾协同与语义。若生成器能绕过瓶颈读所有原文，约束含义就不同。压缩仍有损，不表示整个笔记细节可完整恢复。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一枚状态既要把同兴趣笔记拉近，又需生成“露营装备”标签，不能只编码共读热门度而忘掉内容在讲什么。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2403.01744">原论文</a> · <a href="../../../../reproductions/2403.01744-notellm/">实现解读</a> · <a href="#qa-2cf64a8c96cdbab5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:notellm" data-paper-title="NoteLLM: A Retrievable Large Language Model for Note Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="NoteLLM: A Retrievable Large Language Model for Note Recommendation 搜广推与 LLM 应用 Xiaohongshu 2024-03-04 纯文本 embedding 缺少协同信号，纯对比学习又可能损害 LLM 生成能力。NoteLLM 用统一 compression prompt 将内容压到特殊 token；GCL 拉近用户共读 note，CSFT 从同一压缩状态生成 hashtag/category。 Fidelity: 完整核心链路复现。真实执行 note compression special token、行为共现 GCL、类别生成 CSFT 和压缩状态 I2I 检索；T5-small/MovieLens 替代 7B LLM/小红书 note。本地对照口径：基线是冻结 compression-state embedding；实验组是 NoteLLM 的 GCL+CSFT embedding；NDCG@10 从 0.01142 升至 0.01224（+7.15%）。这是表征训练消融，不是端到端排序模型相对 DIN 的提升。  llm-recommendation contrastive-learning i2i-retrieval 搜广推 语义表征、用户知识与冷启动 NoteLLM 为什么让压缩状态同时接受共读对比学习和内容生成监督？ 共读对比学习把用户实际共同阅读的内容拉近，让表示获得协同关系；但单独追求相似度可能丢失细粒度文本语义。内容监督从同一压缩状态生成标签和类别，要求它保留可生成的内容信息。两个目标共同塑造瓶颈表示，使向量既适合检索，又不轻易退化为只记共现关系的编码。 示意：两篇都被露营用户阅读的笔记应在向量空间接近，但一篇讲帐篷、一篇讲炊具。生成各自标签的任务迫使压缩表示在共享兴趣之外仍保留内容差别。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-fb498d5617532d9c">NoteLLM 为什么让压缩状态同时接受共读对比学习和内容生成监督？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Anotellm">NoteLLM: A Retrievable Large Language Model for Note Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共读对比学习把用户实际共同阅读的内容拉近，让表示获得协同关系；但单独追求相似度可能丢失细粒度文本语义。内容监督从同一压缩状态生成标签和类别，要求它保留可生成的内容信息。两个目标共同塑造瓶颈表示，使向量既适合检索，又不轻易退化为只记共现关系的编码。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两篇都被露营用户阅读的笔记应在向量空间接近，但一篇讲帐篷、一篇讲炊具。生成各自标签的任务迫使压缩表示在共享兴趣之外仍保留内容差别。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2403.01744">原论文</a> · <a href="../../../../reproductions/2403.01744-notellm/">实现解读</a> · <a href="#qa-fb498d5617532d9c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:notellm" data-paper-title="NoteLLM: A Retrievable Large Language Model for Note Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="NoteLLM: A Retrievable Large Language Model for Note Recommendation 搜广推与 LLM 应用 Xiaohongshu 2024-03-04 纯文本 embedding 缺少协同信号，纯对比学习又可能损害 LLM 生成能力。NoteLLM 用统一 compression prompt 将内容压到特殊 token；GCL 拉近用户共读 note，CSFT 从同一压缩状态生成 hashtag/category。 Fidelity: 完整核心链路复现。真实执行 note compression special token、行为共现 GCL、类别生成 CSFT 和压缩状态 I2I 检索；T5-small/MovieLens 替代 7B LLM/小红书 note。本地对照口径：基线是冻结 compression-state embedding；实验组是 NoteLLM 的 GCL+CSFT embedding；NDCG@10 从 0.01142 升至 0.01224（+7.15%）。这是表征训练消融，不是端到端排序模型相对 DIN 的提升。  llm-recommendation contrastive-learning i2i-retrieval 搜广推 语义表征、用户知识与冷启动 GCL 共读正例与纯文本相似正例，相比学到哪种不同关系？ 文本相似由内容决定，共读反映用户共同消费，可连接表面不同却同兴趣的笔记，也可能受曝光和热门度影响。CSFT 维持内容约束以免只追协同。两种信号互补不等于天然无偏，来源简化标签任务也不能代替真实 hashtag 生成。 示意：帐篷评测与露营食谱文字差异大，但同群用户共读；相似文本则可能只是两篇重复评测，二者提供不同检索关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-2fe13bdf9a3534e6">GCL 共读正例与纯文本相似正例，相比学到哪种不同关系？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Anotellm">NoteLLM: A Retrievable Large Language Model for Note Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文本相似由内容决定，共读反映用户共同消费，可连接表面不同却同兴趣的笔记，也可能受曝光和热门度影响。CSFT 维持内容约束以免只追协同。两种信号互补不等于天然无偏，来源简化标签任务也不能代替真实 hashtag 生成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>帐篷评测与露营食谱文字差异大，但同群用户共读；相似文本则可能只是两篇重复评测，二者提供不同检索关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2403.01744">原论文</a> · <a href="../../../../reproductions/2403.01744-notellm/">实现解读</a> · <a href="#qa-2fe13bdf9a3534e6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:notellm" data-paper-title="NoteLLM: A Retrievable Large Language Model for Note Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="NoteLLM: A Retrievable Large Language Model for Note Recommendation 搜广推与 LLM 应用 Xiaohongshu 2024-03-04 纯文本 embedding 缺少协同信号，纯对比学习又可能损害 LLM 生成能力。NoteLLM 用统一 compression prompt 将内容压到特殊 token；GCL 拉近用户共读 note，CSFT 从同一压缩状态生成 hashtag/category。 Fidelity: 完整核心链路复现。真实执行 note compression special token、行为共现 GCL、类别生成 CSFT 和压缩状态 I2I 检索；T5-small/MovieLens 替代 7B LLM/小红书 note。本地对照口径：基线是冻结 compression-state embedding；实验组是 NoteLLM 的 GCL+CSFT embedding；NDCG@10 从 0.01142 升至 0.01224（+7.15%）。这是表征训练消融，不是端到端排序模型相对 DIN 的提升。  llm-recommendation contrastive-learning i2i-retrieval 搜广推 语义表征、用户知识与冷启动 NoteLLM 的对比向量与 CSFT 初始状态如何确认来自同一个 compression 位置？ 应按特殊 token 身份读取同一 hidden state，而非一个用末尾、另一个用均值。batch 配对与因果生成 mask 需一致，padding 不进入池化。冻结基线与联合训练对照回答表征学习问题，不能描述为完整排序网络相对 DIN 的提升。 示意：若对比用标题均值、生成用独立 CLS，两项都能训练却不再共同约束同一瓶颈；需检查实际索引而不是只看损失名字。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-818da7eef23dbbae">NoteLLM 的对比向量与 CSFT 初始状态如何确认来自同一个 compression 位置？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Anotellm">NoteLLM: A Retrievable Large Language Model for Note Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>应按特殊 token 身份读取同一 hidden state，而非一个用末尾、另一个用均值。batch 配对与因果生成 mask 需一致，padding 不进入池化。冻结基线与联合训练对照回答表征学习问题，不能描述为完整排序网络相对 DIN 的提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>若对比用标题均值、生成用独立 CLS，两项都能训练却不再共同约束同一瓶颈；需检查实际索引而不是只看损失名字。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2403.01744">原论文</a> · <a href="../../../../reproductions/2403.01744-notellm/">实现解读</a> · <a href="#qa-818da7eef23dbbae">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:kar" data-paper-title="Towards Open-World Recommendation with Knowledge Augmentation from Large Language Models" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Towards Open-World Recommendation with Knowledge Augmentation from Large Language Models 搜广推与 LLM 应用 Huawei 2023-06-19 封闭域推荐只能从本域交互学习，难以理解物品事实和用户偏好背后的常识。KAR 不把 LLM 直接当在线推荐器，而是通过 factorization prompting 让 LLM 分别产出用户偏好推理知识与物品事实知识，再用 hybrid-expert adapter 压缩成与 ID 推荐模型兼容的向量。知识可预生成并缓存，因此线上不承担 LLM 自回归延迟。 Fidelity: 完整核心链路复现。真实执行 factorization prompts、用户偏好/物品事实知识生成、离线缓存、hybrid-expert adapter 和下游 CTR 训练；PanGu 与华为日志替换为 SmolLM2-135M-Instruct 和 MovieLens-100K。本地对照口径：基线是纯 ID ranker；实验组是加入 LLM 知识与四专家 adapter 的 KAR；AUC 从 0.72188 升至 0.72774（+0.81%）。这是知识增强模块消融，不是相对 DIN 的比较。  llm-recommendation knowledge-augmentation ctr-ranking 搜广推 语义表征、用户知识与冷启动 KAR 为什么分开用户偏好知识和物品事实知识？ 偏好解释用户为何可能喜欢，事实描述物品是什么，两者证据与更新频率不同。factorization prompting 分开生成，再经 hybrid-expert adapter 接入 ID 推荐器，避免让单段文本混杂猜测与事实。生成知识仍可能有幻觉，不能把其全部当作观测真值。 示意：用户喜欢轻松剧情是偏好推断，电影上映年份是事实；若模型把前者写成影片本身属性，就会污染后续匹配与解释。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-kar-c442fbbf" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-1b495bedf4e8e1f2">KAR 为什么分开用户偏好知识和物品事实知识？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Akar">Towards Open-World Recommendation with Knowledge Augmentation from Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>偏好解释用户为何可能喜欢，事实描述物品是什么，两者证据与更新频率不同。factorization prompting 分开生成，再经 hybrid-expert adapter 接入 ID 推荐器，避免让单段文本混杂猜测与事实。生成知识仍可能有幻觉，不能把其全部当作观测真值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户喜欢轻松剧情是偏好推断，电影上映年份是事实；若模型把前者写成影片本身属性，就会污染后续匹配与解释。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2306.10933">原论文</a> · <a href="../../../../reproductions/2306.10933-kar/">实现解读</a> · <a href="#qa-1b495bedf4e8e1f2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:kar" data-paper-title="Towards Open-World Recommendation with Knowledge Augmentation from Large Language Models" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Towards Open-World Recommendation with Knowledge Augmentation from Large Language Models 搜广推与 LLM 应用 Huawei 2023-06-19 封闭域推荐只能从本域交互学习，难以理解物品事实和用户偏好背后的常识。KAR 不把 LLM 直接当在线推荐器，而是通过 factorization prompting 让 LLM 分别产出用户偏好推理知识与物品事实知识，再用 hybrid-expert adapter 压缩成与 ID 推荐模型兼容的向量。知识可预生成并缓存，因此线上不承担 LLM 自回归延迟。 Fidelity: 完整核心链路复现。真实执行 factorization prompts、用户偏好/物品事实知识生成、离线缓存、hybrid-expert adapter 和下游 CTR 训练；PanGu 与华为日志替换为 SmolLM2-135M-Instruct 和 MovieLens-100K。本地对照口径：基线是纯 ID ranker；实验组是加入 LLM 知识与四专家 adapter 的 KAR；AUC 从 0.72188 升至 0.72774（+0.81%）。这是知识增强模块消融，不是相对 DIN 的比较。  llm-recommendation knowledge-augmentation ctr-ranking 搜广推 语义表征、用户知识与冷启动 KAR为什么分开生成用户偏好知识和物品事实，再用hybrid-expert adapter接入？ 用户知识描述为何可能喜欢，物品知识描述内容具有什么属性，二者来源与语义不同，直接拼接可能难与ID模型兼容。adapter通过共享及专属专家压缩和对齐，再与原表示共同预测；知识可离线缓存，线上不必自回归生成。LLM推断仍可能错误，不能把偏好解释当用户真实表态。 示意：物品事实是鞋具防水材质，用户知识是近期常看雨天徒步内容；两类信息通过适配器形成有用关系，但不能据此断言用户已经表示一定想买这双鞋。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-78a75af0fdb7fbca">KAR为什么分开生成用户偏好知识和物品事实，再用hybrid-expert adapter接入？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Akar">Towards Open-World Recommendation with Knowledge Augmentation from Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用户知识描述为何可能喜欢，物品知识描述内容具有什么属性，二者来源与语义不同，直接拼接可能难与ID模型兼容。adapter通过共享及专属专家压缩和对齐，再与原表示共同预测；知识可离线缓存，线上不必自回归生成。LLM推断仍可能错误，不能把偏好解释当用户真实表态。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>物品事实是鞋具防水材质，用户知识是近期常看雨天徒步内容；两类信息通过适配器形成有用关系，但不能据此断言用户已经表示一定想买这双鞋。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2306.10933">原论文</a> · <a href="../../../../reproductions/2306.10933-kar/">实现解读</a> · <a href="#qa-78a75af0fdb7fbca">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:kar" data-paper-title="Towards Open-World Recommendation with Knowledge Augmentation from Large Language Models" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Towards Open-World Recommendation with Knowledge Augmentation from Large Language Models 搜广推与 LLM 应用 Huawei 2023-06-19 封闭域推荐只能从本域交互学习，难以理解物品事实和用户偏好背后的常识。KAR 不把 LLM 直接当在线推荐器，而是通过 factorization prompting 让 LLM 分别产出用户偏好推理知识与物品事实知识，再用 hybrid-expert adapter 压缩成与 ID 推荐模型兼容的向量。知识可预生成并缓存，因此线上不承担 LLM 自回归延迟。 Fidelity: 完整核心链路复现。真实执行 factorization prompts、用户偏好/物品事实知识生成、离线缓存、hybrid-expert adapter 和下游 CTR 训练；PanGu 与华为日志替换为 SmolLM2-135M-Instruct 和 MovieLens-100K。本地对照口径：基线是纯 ID ranker；实验组是加入 LLM 知识与四专家 adapter 的 KAR；AUC 从 0.72188 升至 0.72774（+0.81%）。这是知识增强模块消融，不是相对 DIN 的比较。  llm-recommendation knowledge-augmentation ctr-ranking 搜广推 语义表征、用户知识与冷启动 KAR 的离线知识增强与在线 LLM 推荐，相比成本和错误传播有何不同？ 离线生成可复用缓存，在线仅运行适配器与原推荐器，减少自回归延迟；错误知识也会被多次复用，需要版本与更新。在线生成较灵活却每次付成本。来源二十用户缩比只有小幅趋势，不支持普遍工业收益。 示意：一部电影事实可离线编码供多用户读取，但若年份错了会持续传播；在线每次询问可更新，却增加所有请求的延迟和不一致。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-804816a74c553ef3">KAR 的离线知识增强与在线 LLM 推荐，相比成本和错误传播有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Akar">Towards Open-World Recommendation with Knowledge Augmentation from Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>离线生成可复用缓存，在线仅运行适配器与原推荐器，减少自回归延迟；错误知识也会被多次复用，需要版本与更新。在线生成较灵活却每次付成本。来源二十用户缩比只有小幅趋势，不支持普遍工业收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一部电影事实可离线编码供多用户读取，但若年份错了会持续传播；在线每次询问可更新，却增加所有请求的延迟和不一致。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2306.10933">原论文</a> · <a href="../../../../reproductions/2306.10933-kar/">实现解读</a> · <a href="#qa-804816a74c553ef3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:kar" data-paper-title="Towards Open-World Recommendation with Knowledge Augmentation from Large Language Models" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Towards Open-World Recommendation with Knowledge Augmentation from Large Language Models 搜广推与 LLM 应用 Huawei 2023-06-19 封闭域推荐只能从本域交互学习，难以理解物品事实和用户偏好背后的常识。KAR 不把 LLM 直接当在线推荐器，而是通过 factorization prompting 让 LLM 分别产出用户偏好推理知识与物品事实知识，再用 hybrid-expert adapter 压缩成与 ID 推荐模型兼容的向量。知识可预生成并缓存，因此线上不承担 LLM 自回归延迟。 Fidelity: 完整核心链路复现。真实执行 factorization prompts、用户偏好/物品事实知识生成、离线缓存、hybrid-expert adapter 和下游 CTR 训练；PanGu 与华为日志替换为 SmolLM2-135M-Instruct 和 MovieLens-100K。本地对照口径：基线是纯 ID ranker；实验组是加入 LLM 知识与四专家 adapter 的 KAR；AUC 从 0.72188 升至 0.72774（+0.81%）。这是知识增强模块消融，不是相对 DIN 的比较。  llm-recommendation knowledge-augmentation ctr-ranking 搜广推 语义表征、用户知识与冷启动 KAR 四专家 adapter 的 gate 与原 ID 表示为什么需要共同验收？ gate 在共享与专属专家中混合知识向量，输出再与用户、物品 ID 一起评分，维度、身份与参数梯度都要对应。只预生成知识并存文件不等于增强路径被训练使用。缓存应仅基于训练可见行为，避免偏好知识吸收测试答案。 示意：知识存在磁盘却从未送入 ranker，代码仍可输出分数，但不是 KAR；反之测试后总结用户偏好再评估，也已把目标信息带进模型。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-fccb1acc024f0dc4">KAR 四专家 adapter 的 gate 与原 ID 表示为什么需要共同验收？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Akar">Towards Open-World Recommendation with Knowledge Augmentation from Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>gate 在共享与专属专家中混合知识向量，输出再与用户、物品 ID 一起评分，维度、身份与参数梯度都要对应。只预生成知识并存文件不等于增强路径被训练使用。缓存应仅基于训练可见行为，避免偏好知识吸收测试答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>知识存在磁盘却从未送入 ranker，代码仍可输出分数，但不是 KAR；反之测试后总结用户偏好再评估，也已把目标信息带进模型。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2306.10933">原论文</a> · <a href="../../../../reproductions/2306.10933-kar/">实现解读</a> · <a href="#qa-fccb1acc024f0dc4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:m6rec" data-paper-title="M6-Rec: Generative Pretrained Language Models are Open-Ended Recommender Systems" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="M6-Rec: Generative Pretrained Language Models are Open-Ended Recommender Systems 搜广推与 LLM 应用 Alibaba 2022-05-17 传统推荐模型为排序、召回、解释、对话分别维护架构。M6-Rec 把匿名行为序列和候选物品都改写成自然语言，让一个生成式预训练模型统一完成排序、召回、zero-shot、解释、内容生成和对话。为避免每个场景完整微调巨型 M6，论文提出 option tuning 和 option-adapter tuning，只训练约 1% 的任务参数；线上再用 late interaction、early exit、参数共享和剪枝得到 10M/2M 的 M6-Edge。 Fidelity: 核心机制复现。真实执行冻结预训练 Transformer、自然语言用户行为、option tuning 与逐层 bottleneck option-adapter tuning；M6 生产模型、私有数据和 early-exit/pruning serving 未复刻。本地对照口径：基线是只训练 option prototype 的 Option Tuning；实验组额外训练 24d adapter；AUC 从 0.53832 升至 0.53890（+0.12%）。这是 adapter 增量消融，不代表完整 M6-Rec 相对 DIN 或工业基线的提升。  llm-recommendation foundation-model parameter-efficient-tuning 搜广推 语义表征、用户知识与冷启动 M6-Rec 为什么把匿名行为和候选转成自然语言以统一多个任务？ 文本接口让共享预训模型接收不同推荐问题，任务差异通过 option 和 adapter 表达，减少每场景维护独立大模型。统一语言不等于所有任务共享同一标签或同一解码成本，解释、召回与分类仍有不同输出契约。 示意：同一模型可读用户电影历史后做是否推荐判断，也可解释内容；不能因都用文本输入，就把解释正确率直接当召回命中率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-m6rec-d70d1b1b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-948a8e376d11e409">M6-Rec 为什么把匿名行为和候选转成自然语言以统一多个任务？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Am6rec">M6-Rec: Generative Pretrained Language Models are Open-Ended Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文本接口让共享预训模型接收不同推荐问题，任务差异通过 option 和 adapter 表达，减少每场景维护独立大模型。统一语言不等于所有任务共享同一标签或同一解码成本，解释、召回与分类仍有不同输出契约。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一模型可读用户电影历史后做是否推荐判断，也可解释内容；不能因都用文本输入，就把解释正确率直接当召回命中率。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2205.08084">原论文</a> · <a href="../../../../reproductions/2205.08084-m6rec/">实现解读</a> · <a href="#qa-948a8e376d11e409">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:m6rec" data-paper-title="M6-Rec: Generative Pretrained Language Models are Open-Ended Recommender Systems" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="M6-Rec: Generative Pretrained Language Models are Open-Ended Recommender Systems 搜广推与 LLM 应用 Alibaba 2022-05-17 传统推荐模型为排序、召回、解释、对话分别维护架构。M6-Rec 把匿名行为序列和候选物品都改写成自然语言，让一个生成式预训练模型统一完成排序、召回、zero-shot、解释、内容生成和对话。为避免每个场景完整微调巨型 M6，论文提出 option tuning 和 option-adapter tuning，只训练约 1% 的任务参数；线上再用 late interaction、early exit、参数共享和剪枝得到 10M/2M 的 M6-Edge。 Fidelity: 核心机制复现。真实执行冻结预训练 Transformer、自然语言用户行为、option tuning 与逐层 bottleneck option-adapter tuning；M6 生产模型、私有数据和 early-exit/pruning serving 未复刻。本地对照口径：基线是只训练 option prototype 的 Option Tuning；实验组额外训练 24d adapter；AUC 从 0.53832 升至 0.53890（+0.12%）。这是 adapter 增量消融，不代表完整 M6-Rec 相对 DIN 或工业基线的提升。  llm-recommendation foundation-model parameter-efficient-tuning 搜广推 语义表征、用户知识与冷启动 M6-Rec统一多个推荐任务时，option tuning和adapter分别改动哪一部分？ 冻结主干保留预训练能力，option参数为任务选择提供轻量可学习接口，逐层adapter再增加小规模任务变换。两者让不同任务共享大模型而不必各自全量微调；但参数占比小不等于推理成本自然低，边缘部署仍需独立压缩与服务设计。本地小任务对照也不能证明巨型M6全部能力已迁移。 示意：同一冻结模型处理相关性判断与内容解释，可用不同任务option和小adapter适配；只训练很少参数仍可能需要经过大主干，因此不能直接声称已适合端侧。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-7d3a6b15d0fd72c8">M6-Rec统一多个推荐任务时，option tuning和adapter分别改动哪一部分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Am6rec">M6-Rec: Generative Pretrained Language Models are Open-Ended Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冻结主干保留预训练能力，option参数为任务选择提供轻量可学习接口，逐层adapter再增加小规模任务变换。两者让不同任务共享大模型而不必各自全量微调；但参数占比小不等于推理成本自然低，边缘部署仍需独立压缩与服务设计。本地小任务对照也不能证明巨型M6全部能力已迁移。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一冻结模型处理相关性判断与内容解释，可用不同任务option和小adapter适配；只训练很少参数仍可能需要经过大主干，因此不能直接声称已适合端侧。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2205.08084">原论文</a> · <a href="../../../../reproductions/2205.08084-m6rec/">实现解读</a> · <a href="#qa-7d3a6b15d0fd72c8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:m6rec" data-paper-title="M6-Rec: Generative Pretrained Language Models are Open-Ended Recommender Systems" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="M6-Rec: Generative Pretrained Language Models are Open-Ended Recommender Systems 搜广推与 LLM 应用 Alibaba 2022-05-17 传统推荐模型为排序、召回、解释、对话分别维护架构。M6-Rec 把匿名行为序列和候选物品都改写成自然语言，让一个生成式预训练模型统一完成排序、召回、zero-shot、解释、内容生成和对话。为避免每个场景完整微调巨型 M6，论文提出 option tuning 和 option-adapter tuning，只训练约 1% 的任务参数；线上再用 late interaction、early exit、参数共享和剪枝得到 10M/2M 的 M6-Edge。 Fidelity: 核心机制复现。真实执行冻结预训练 Transformer、自然语言用户行为、option tuning 与逐层 bottleneck option-adapter tuning；M6 生产模型、私有数据和 early-exit/pruning serving 未复刻。本地对照口径：基线是只训练 option prototype 的 Option Tuning；实验组额外训练 24d adapter；AUC 从 0.53832 升至 0.53890（+0.12%）。这是 adapter 增量消融，不代表完整 M6-Rec 相对 DIN 或工业基线的提升。  llm-recommendation foundation-model parameter-efficient-tuning 搜广推 语义表征、用户知识与冷启动 Option tuning 与 option-adapter tuning，相比增加了哪部分可学习能力？ 只调 option 原型主要改变输出决策接口，adapter 还在冻结主干层间提供低秩非线性变换，能适配内部表示。后者参数更多但仍远少全量微调，效果取决于数据；来源本地只有微小且波动趋势，不足以宣称稳定生产增益。 示意：只移动“推荐/不推荐”两个原型像调整分类尺，加入 adapter 则可先调整被尺衡量的特征；两者不是相同参数预算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e2a1ebcf2997bc76">Option tuning 与 option-adapter tuning，相比增加了哪部分可学习能力？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Am6rec">M6-Rec: Generative Pretrained Language Models are Open-Ended Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只调 option 原型主要改变输出决策接口，adapter 还在冻结主干层间提供低秩非线性变换，能适配内部表示。后者参数更多但仍远少全量微调，效果取决于数据；来源本地只有微小且波动趋势，不足以宣称稳定生产增益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>只移动“推荐/不推荐”两个原型像调整分类尺，加入 adapter 则可先调整被尺衡量的特征；两者不是相同参数预算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2205.08084">原论文</a> · <a href="../../../../reproductions/2205.08084-m6rec/">实现解读</a> · <a href="#qa-e2a1ebcf2997bc76">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:m6rec" data-paper-title="M6-Rec: Generative Pretrained Language Models are Open-Ended Recommender Systems" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="M6-Rec: Generative Pretrained Language Models are Open-Ended Recommender Systems 搜广推与 LLM 应用 Alibaba 2022-05-17 传统推荐模型为排序、召回、解释、对话分别维护架构。M6-Rec 把匿名行为序列和候选物品都改写成自然语言，让一个生成式预训练模型统一完成排序、召回、zero-shot、解释、内容生成和对话。为避免每个场景完整微调巨型 M6，论文提出 option tuning 和 option-adapter tuning，只训练约 1% 的任务参数；线上再用 late interaction、early exit、参数共享和剪枝得到 10M/2M 的 M6-Edge。 Fidelity: 核心机制复现。真实执行冻结预训练 Transformer、自然语言用户行为、option tuning 与逐层 bottleneck option-adapter tuning；M6 生产模型、私有数据和 early-exit/pruning serving 未复刻。本地对照口径：基线是只训练 option prototype 的 Option Tuning；实验组额外训练 24d adapter；AUC 从 0.53832 升至 0.53890（+0.12%）。这是 adapter 增量消融，不代表完整 M6-Rec 相对 DIN 或工业基线的提升。  llm-recommendation foundation-model parameter-efficient-tuning 搜广推 语义表征、用户知识与冷启动 M6-Rec 本地冻结主干的二分类 option 得分，为什么要核验归一化与温度？ 来源比较归一表示和可训练原型的相似度，温度控制分类分布；若未归一，向量范数会改变机制。两臂主干均应冻结，只对 option 与允许 adapter 更新。本地 BERT-tiny 是缩比任务路径，不代表完整生成式 M6 所有能力。 示意：原型范数越大若可直接提高分数，模型可能只靠放大而非方向学分类；归一和温度把这项自由度按定义固定。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6e1fdaea7f5556ee">M6-Rec 本地冻结主干的二分类 option 得分，为什么要核验归一化与温度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Am6rec">M6-Rec: Generative Pretrained Language Models are Open-Ended Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>来源比较归一表示和可训练原型的相似度，温度控制分类分布；若未归一，向量范数会改变机制。两臂主干均应冻结，只对 option 与允许 adapter 更新。本地 BERT-tiny 是缩比任务路径，不代表完整生成式 M6 所有能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>原型范数越大若可直接提高分数，模型可能只靠放大而非方向学分类；归一和温度把这项自由度按定义固定。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2205.08084">原论文</a> · <a href="../../../../reproductions/2205.08084-m6rec/">实现解读</a> · <a href="#qa-6e1fdaea7f5556ee">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

一个没有点击记录的新物品，怎样进入依赖行为信号的推荐系统？

## 记住这一点

内容语义、协同身份和用户偏好是三类信号。KAR把离线生成的知识接入推荐器；NoteLLM用共读关系和生成任务共同训练内容向量；语义ID再把连续内容压缩为可索引或生成的短码。用户记忆与邻居证据可补足偏好，推荐反馈也可反过来训练内容描述。关键在于让表示与推荐目标对齐，不能把语言相似度直接当作用户会喜欢的程度。

## 一个例子

新品跑鞋没有点击日志，标题和图片仍能表达用途；但两双外观相似的鞋未必面向相同人群。可先用内容建立表示，再用已有商品的共购或共读信号对齐偏好，而不是直接把文本最近邻当最终排序。

## 什么时候要小心

内容重建误差下降不保证推荐指标提高；码本过小会碰撞，过大又可能学不到稳定协同关系。LLM生成的偏好描述仍需核验，不能当作真实点击标签；高成本资料收录也不代表已有可运行大模型。

## 先读这几篇

按离线知识增强→协同信号训练表征→用短ID承载内容的顺序读KAR、NoteLLM、Dual-purpose SID；三者均有本地机制路径，Dual-purpose SID的小码本负结果尤其适合理解质量与压缩的取舍。

1. [Towards Open-World Recommendation with Knowledge Augmentation from Large Language Models](../../../reproductions/2306.10933-kar/README.md) · [原论文](https://arxiv.org/abs/2306.10933)
2. [NoteLLM: A Retrievable Large Language Model for Note Recommendation](../../../reproductions/2403.01744-notellm/README.md) · [原论文](https://arxiv.org/abs/2403.01744)
3. [Tokens are All You Need: Dual-purpose Semantic IDs for Achieving LLM-Level I/O Efficiency in Recommendation Systems](../../../reproductions/2607.24865-dual-sid/README.md) · [原论文](https://arxiv.org/abs/2607.24865)

## 自测一下

语义ID的重建MSE变小，但相同协议下NDCG下降，应如何解释？

??? note "展开参考答案"

    压缩更好保留了内容，却未必更好保留协同偏好、区分候选或适配解码器。应分别检查码碰撞、内容—行为对齐及最终检索结果，不能只用重建指标宣布推荐有效。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
