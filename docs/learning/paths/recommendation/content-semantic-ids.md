---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 语义表征、用户知识与冷启动

[搜广推](index.md) / 60 个问题 · 60 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">60 个问题 · 60 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:finesid" data-paper-title="Progressive Learning from Content to Relevance to Personalization for CTR Prediction" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Progressive Learning from Content to Relevance to Personalization for CTR Prediction 搜广推与 LLM 应用 Alibaba Group 2026-10-21 将内容直接压成一个语义ID会丢失局部视觉细节；只对 embedding 做相关性预训又不能给最终交互网络提供足够初始化。FineSID 用细粒度离散视觉/文本 token，先把完整共享预测器训成 query-item 语义相关性模型，再迁移到个性化 CTR。关键不是单独的 SID lookup，而是三个阶段之间保留同一交互骨干并迁移完整参数/状态。把随机 token 或简单加权器接到现有 CTR 模型，不能替代整篇论文。 因此本轮只完成论文、方法与线上证据收录，成本过高，不复现（审查 DONE）。完整训练使用64张 H20，每卡 batch4096、全局 batch262144。数据包含512亿曝光、2.51亿用户、2亿 query、4.18亿商品，以及4.53亿次测试曝光；相关性教师还依赖大规模专家标注/私有数据。  排序与长序列建模 预训练与参数高效迁移 搜广推 语义表征、用户知识与冷启动 FineSID从相关性预训迁移到CTR时，为什么不能只复制SID embedding？ 相关性阶段训练的是包含有序内容融合与HiFormer交互的完整共享预测器，知识同时存在于embedding、稠密层和归一化状态。只复制词表会丢掉大部分已学交互；迁移还须按约定更换CTR头并处理优化器状态。原文大规模实验成本过高，本库只收录方法与证据，不能用随机token小夹具替代整条链路。 示意：预训已学会查询中的用途如何与图像局部细节交叉，只搬商品短码就像只带走字典、不带走阅读能力；后续点击训练还得从头重学这些交互。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-finesid-1b73a633" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sid-topology" data-paper-title="Don&#x27;t Rewrite the SID Map: Topology Preservation for Generative Retrieval in Dynamic E-Commerce Search" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Don&#x27;t Rewrite the SID Map: Topology Preservation for Generative Retrieval in Dynamic E-Commerce Search 搜广推与 LLM 应用 Alibaba / Taobao &amp; Tmall Group 2026-10-19 生成式检索学习的是从查询到多级SID的解码路径，重新按业务价值排序旧商品会改变路径含义。论文把“映射更新”和“继续训练”拆开，发现大beam可以掩盖窄beam下的严重漂移；短预算warm-start也不能修复任意重映射。方法保留全部旧商品的三层SID，新商品先由外部RQ-VAE得到两层语义前缀，再按当前业务价值排名插入第三层。头部初始分配独占token，尾部采用固定容量共享桶；新商品插入头部时可以与原独占token碰撞，但不能顺移旧商品来强行消碰撞。 64卡完整训练和生产实验成本过高，不复现（审查 DONE）。已实现CPU映射组件，证据为L1机制诊断；已实现CPU映射组件，证据为L1机制诊断；不是RQ-VAE/LLM检索能力复现。64卡完整训练和生产实验成本过高，不复现（审查 DONE）。真实执行价值先验、初始HC分配、新商品插入、碰撞展开、旧路径漂移统计；用独立预期桶、插入顺序不变性、头部碰撞和全重映射负对照验收。frozen_old_path_address_recovery只是合成映射中旧地址仍能找回成员，不是推荐准确率、HitRate或模型成功率。没有量化器、语义编码器、beam-search模型或生产A/B，也未接入Evolve。  生成式推荐 语义标识与增量更新 搜广推 语义表征、用户知识与冷启动 SID-Topology 为什么允许新商品与旧头部 token 碰撞，却不顺移旧商品来消除碰撞？ 生成器已经学会查询到旧 SID 路径的含义，顺移旧商品会把原有概率质量导向别的对象，短预算继续训练也未必修复。保留旧路径把更新影响局限于新商品插入，头部碰撞由展开处理，而非全局重映射。大 beam 可能掩盖窄 beam 的漂移，因此评估需检查路径稳定性，不能只看宽束结果。 示意：模型熟悉编码 A 指向旧商品甲，新商品乙加入时若把甲改到 B，原来生成 A 的请求就错位。宁可让 A 对应可展开的碰撞集合，也先保留甲的旧地址。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-sid-topology-a240bd6b" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:agent-web-rec" data-paper-title="AgentWebRec: Compact Evidence Fusion over the Agent Web for Personalized Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="AgentWebRec: Compact Evidence Fusion over the Agent Web for Personalized Recommendation 搜广推与 LLM 应用 Beihang University 2026-10-01 先从平台获取候选语义，再按语义相关性和时间衰减检索目标用户私有记忆；仅在本地证据置信度不足时查询邻居 Agent 的紧凑偏好模式。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。只执行有界检索与置信门控；不暴露私有记录，不运行 LLM Agent Web。只执行有界检索与置信门控；不暴露私有记录，不运行 LLM Agent Web。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  agent-recommendation private-memory evidence-fusion 搜广推 语义表征、用户知识与冷启动 AgentWebRec为什么只在私有记忆证据不足时才向邻居Agent协作？ 目标用户的相关记忆通常比他人的概括偏好更直接，因此先按语义相关性与时间衰减检索本地证据。置信度不足才请求邻居提供紧凑模式，减少无关迁移与私有历史传播；协作是补证据而非把全网记忆无条件拼进提示。本地仅检验门控与证据融合，不等于验证完整推荐Agent能力。 示意：用户已多次记录素食偏好时无需询问邻居；若只留下模糊旅行兴趣，可借邻居的景点偏好模式补充，但不用发送用户原始行程。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-agent-web-rec-883c9fbf" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gris" data-paper-title="Neither Black nor White: Balancing Semantic and Collaborative Signals with Graph-Informed Semantic IDs (GrIS)" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Neither Black nor White: Balancing Semantic and Collaborative Signals with Graph-Informed Semantic IDs (GrIS) 搜广推与 LLM 应用 Huawei Ireland Research Centre 2026-10-01 把 Semantic ID 构造重写为层级图划分：节点承载内容语义，边承载协同信号；图为空时退化为内容量化。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 graph-informed 层级二分 ID；用户批准为学术/Evolve 例外，无线上 A/B，不进入工业证据结论。收录例外：用户于 2026-10-02 明确批准的学术/Evolve 机制例外；论文没有量化线上 A/B，不进入工业证据结论。执行 graph-informed 层级二分 ID；用户批准为学术/Evolve 例外，无线上 A/B，不进入工业证据结论。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  generative-recommendation semantic-id graph-partition 搜广推 语义表征、用户知识与冷启动 GrIS把SID构造写成图划分，为什么要同时看内容节点和协同边？ 内容相近与共同消费并不总重合，单纯内容量化可能错过偏好结构。图划分让语义特征与协同连接共同影响层级编码，保留两类信号间的折中；图缺失时则退回内容信息，而不能伪造协同关系。本地只检查划分与状态机制，层级结构本身并不证明生成推荐或线上效果已经成立。 示意：两件外观不同的露营用品经常被共同消费，协同边会提示它们的关系；刚上线的商品还没有边时，只能主要依据内容，而非假装已有行为支持。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-gris-e106351a" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:kuafu" data-paper-title="KuaFu: Compressing Long User Behavior into Understanding at Billion Scale" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="KuaFu: Compressing Long User Behavior into Understanding at Billion Scale 搜广推与 LLM 应用 Tencent 2026-09-25 腾讯需要每周为海量用户刷新画像。逐条把原始行为文本送进大模型既慢又占空间；只截断长历史又容易遗漏时间、兴趣和因果信息。KuaFu 把单个行为条目作为最小压缩单位：压缩器对每条独立编码；投影器把 m 个高维记忆 token 降为 k 个低维缓存向量；解码器按用户行为顺序接收这些向量和任务提示。这样同一条目可以跨用户复用，不必因为某个用户新增行为而重算整个历史。原论文的Figure 1 和 Figure 2分别展示生产缓存链路及双轴投影结构；图片版权归原作者。 复现级别：公开数据概念验证，尚未复现论文效果。复现级别：公开数据概念验证，尚未复现论文效果。本地真实运行 Qwen3-4B-Instruct、独立条目压缩、双轴投影和三段监督训练；幻觉感知 DAPO 的代码已实现并在 A100 执行采样与打分，但固定公开样例同组奖励相同，更新被正确跳过。不能把该运行称作四阶段训练完成，更不能将 MRQA 指标等同于腾讯线上 GMV。本地对照口径：同解码器、同源 token 数的开头截断输入作为诊断基线，压缩缓存为实验组；dev F1 相对 -23.4%，但该输入消融不是独立训练的正式基线。  long-behavior item-compression hallucination-aware-rl 搜广推 语义表征、用户知识与冷启动 KuaFu为什么按单条行为压缩和缓存，而不是先把整段用户历史压成一份向量？ 单条行为可被多个用户或不同画像任务复用，独立压缩后新增一条事件只需补充对应缓存。整段历史压缩则会把共享内容与用户上下文绑定，任何变化都可能要求重算。解码器仍按时间顺序读取压缩结果，保留组合解释机会；压缩会损失信息，本地诊断负结果不能被缓存效率掩盖。 示意：同一条视频行为的内容编码可供多位用户复用；某人今天多看一条，只增加该条缓存再按其历史顺序解码，不必重跑所有旧行为的文本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-kuafu-25c887d3" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:music-rationales" data-paper-title="Explainable Recommendations at Scale: LLM Rationales for YouTube Music Artist Discovery" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Explainable Recommendations at Scale: LLM Rationales for YouTube Music Artist Discovery 搜广推与 LLM 应用 Google 2026-09-20 用户愿意听熟悉的艺人，却可能不敢点开陌生艺人。论文将计算昂贵的 Gemini 推理移到异步离线阶段：根据完整的听歌历史生成“发现画像”，包含未听过的艺人和个性化理由；通过实体标准化与 LLM 评审过滤不可信理由；在线阶段只取缓存的画像，缺失时退回原有推荐。这样既能给候选附上解释，又避免在用户请求链路上运行大模型。论文的多臂 holdback 把新增提名与理由标注分开，发现理由是主导 shelf engagement 提升的因素。 复现级别：公开数据概念验证。复现级别：公开数据概念验证。本地使用真实 Qwen2.5-7B-Instruct 生成新艺人提名与自然语言理由，执行目录映射、已听过过滤、理由证据检查及只读缓存在线回退。Google 的 Gemini、私有音乐知识图谱、LLM-as-a-Judge 和线上多臂 A/B 不可公开复刻；公开 Last.fm 命中率不是用户信任或线上互动效果。本地确实运行 7B 权重推理、目录/新颖性/共享标签约束以及缓存/回退路径；但既未调用 Gemini，也未复刻 Google 的专有 KG 和线上 judge。本地对照口径：原 CF 基线 test Hit@5 0.40；  music-discovery llm-rationale offline-online-decoupling 搜广推 语义表征、用户知识与冷启动 Music Rationales 为什么把陌生艺人推荐理由离线生成，并把“提名”和“展示理由”分开评估？ 离线生成让模型能利用完整历史做昂贵推理，再经实体规范化和理由过滤，在线只读取缓存，避免请求延迟。提名改变推荐谁，理由改变用户是否愿意点同一候选，两条路径可能独立影响互动。分开设置实验臂才能区分增益来自候选变化还是解释作用；理由可信也不能只靠语言流畅判断。 示意：同一位陌生爵士艺人，一组只展示名字，另一组增加“延续你常听的钢琴三重奏风格”。保持候选相同，才更接近检验理由本身是否帮助用户决定。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-music-rationales-61aa6d5c" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sirf" data-paper-title="SIRF: A Spec-Internalized Risk Foundation Model for Industrial Content Risk Control" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SIRF: A Spec-Internalized Risk Foundation Model for Industrial Content Risk Control 搜广推与 LLM 应用 Xiaohongshu 2026-09-10 SIRF 用 EntiGraph、MAGA 改写和账户级 CoT 合成长尾风控规则数据，通过 CPT 把复杂 trigger/exemption 规则写进模型权重，以单次 verdict 和可调阈值满足秒级线上判定。 复现级别：概念诊断。复现级别：概念诊断。执行规则关系合成、trigger/exemption 内化和 P95 阈值选择；线性模型替代 8B LLM CPT。没有私有账户数据、8B CPT、EntiGraph/MAGA 语言生成和线上 serving，因此本地结果不能验证论文业务提升。本地对照口径：同源线性特征为基线，加入规则交互项的实验组在三 seed 上 Black Recall@P95 相对提高 65.81%（绝对约 33.84 个百分点）；这不是论文 8B 模型或线上流量结果。  content-understanding risk-control foundation-model industrial-deployment 搜广推 语义表征、用户知识与冷启动 SIRF 为什么用包含 trigger 与 exemption 的合成规则训练模型，再以阈值控制判定？ 长尾风控规则不仅要识别触发条件，还要处理豁免及其组合，单靠常见日志容易漏学。规则图、改写和账户级推理提供覆盖训练，通过继续预训练把复杂模式写入模型，再用单次 verdict 降低在线开销。阈值调节精确率与召回的取舍；本地规则交互诊断不能当作原文大模型的生产能力复现。 示意：频繁交易可能触发风险，但经过验证的商户活动又构成豁免。训练样本需同时覆盖两者及交互，否则模型可能只记住“频繁就是风险”，提高误报。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-sirf-2c896048" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:camie" data-paper-title="CAMIE: Co-Engagement-Aware Multimodal Item Embeddings for Snap Dynamic Product Ads Retrieval" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="CAMIE: Co-Engagement-Aware Multimodal Item Embeddings for Snap Dynamic Product Ads Retrieval 搜广推与 LLM 应用 Snap Inc. 2026-08-31 CAMIE 用同一个 LLM/MLLM 接口编码图片和商品元数据，再从用户旅程挖掘共同互动商品对，以对称 in-batch InfoNCE 把“内容相近”校正为“行为上会共同转化”。同一 checkpoint 同时支持多模态和纯文本召回。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现内容向量、共同互动正对和对称检索打分。未包含私有 DPA 用户旅程、生产 MLLM checkpoint 与 ANN 服务；仅声明 CPU 核心机制。公开 MovieLens 的内容特征和共现 transition 代理共同互动，NDCG@10 为 0.05121（基线 0.05401）；负结果保留在 metrics/public-seeds42-44.json，不把小数据退化包装成提升。  multimodal-retrieval co-engagement advertising 搜广推 语义表征、用户知识与冷启动 CAMIE为什么不用纯图文相似度训练商品向量，还要加入co-engagement对比学习？ 图文相似度只表达内容接近，不保证商品在人类消费过程中有关联。CAMIE用用户旅程中共同互动的商品对形成对称对比监督，把多模态表示拉向推荐相关关系；共享编码接口还能支持不同模态可用性。共同互动本身仍受曝光和场景影响，不能把它等同于普遍互补或因果需求。 示意：图片里很像的两件家具可能尺寸用途不合，而外观不同的桌子和椅子经常一起被考虑；行为对比为内容编码补上这种推荐语义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-camie-634faffd" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dynamic-codebook" data-paper-title="From a Static Multi-Level Small Semantic Codebook to a Dynamic Single-Level Large Semantic Codebook for Generative Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="From a Static Multi-Level Small Semantic Codebook to a Dynamic Single-Level Large Semantic Codebook for Generative Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-08-21 把多级小语义码本压缩为动态更新的单级大码本，再保留独立碰撞码；既减少自回归步数，也用曝光加权更新抵抗码本漂移。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation semantic-id serving-efficiency 搜广推 语义表征、用户知识与冷启动 单级大码本缩短了解码，为什么还需要独立碰撞码与曝光加权更新？ 少生成几个语义层能降低自回归开销，但多个物品仍可能落入同一码，必须保留额外区分入口。动态更新让码中心跟随实际使用分布，曝光权重影响哪些区域更精细地被表示；与此同时更新会改变索引语义，需要维持生成器与服务映射的一致性，不能只比较token数量。 示意：单枚主码已定位一组热门商品，额外碰撞码负责区分组内物品；如果码中心更新后服务仍读旧映射，即使解码快了，也可能返回错误商品。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-dynamic-codebook-fbc8657c" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:netflix-mediafm" data-paper-title="Multimedia Asset Personalization via Multimodal Embeddings at Netflix" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Multimedia Asset Personalization via Multimodal Embeddings at Netflix 搜广推与 LLM 应用 Netflix 2026-08-18 把冻结的 CLIP/MediaFM 多模态表示作为共享在线特征接入资产双塔，并以查询相似度增强搜索画布；离线 IPS 与 winner proxy 先筛选 checkpoint。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  multimodal-recommendation content-understanding cold-start 搜广推 语义表征、用户知识与冷启动 Netflix MediaFM 为什么冻结多模态表示并让多个资产任务共享，而不是每个任务各训一个视觉模型？ 冻结的共享表示把媒体理解成本集中到可复用特征层，下游双塔再学习用户、查询与资产之间的适配。查询相似度可补充个性化相似度，使搜索场景兼顾当前意图。共享减少重复编码与特征分裂，但冻结表示不能靠下游训练自动补回缺失的视觉细节，离线代理筛选也不能替代线上验证。 示意：同一张海报的多模态向量可供首页选图和搜索画布共同使用。搜索“海边喜剧”时增加查询匹配权重，首页则更多结合用户长期口味，无须重算媒体编码。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-netflix-mediafm-31c991d9" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:connectionmind" data-paper-title="ConnectionMind: A General Social-Personalized Recommendation System with LLM Reasoning" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="ConnectionMind: A General Social-Personalized Recommendation System with LLM Reasoning 搜广推与 LLM 应用 Michigan State University 2026-08-10 传统社交推荐通常把好友关系压成静态 embedding，难以回答“某物品为什么经由哪条社交/兴趣路径被推荐”。ConnectionMind 把用户、物品和语义实体组成带关系类型、时间与权重的异构图；LLM policy 在任务相关子图内逐步扩展 frontier，同时输出推荐物品和对应证据路径。训练先从正反馈目标的最短路径做逐步 SFT，再用格式、最终推荐 F1 和最短路径 shaping 三类规则奖励做端到端 GRPO。 Fidelity：核心机制复现。使用论文同款 Delicious 公开数据，实际执行异构图构建、最短正路径 SFT、规则奖励 GRPO、学生蒸馏和重用户混合推理；本地负结果如实保留。没有复刻 Meta 私有视频图、Llama-3.1 3B/8B、生产级 GNN 和 serving；本地结果只验证完整算法路径，不代表复现论文线上增益。本地对照口径：基线为同一 Delicious 图、切分与候选集上的固定异构图聚合；实验组为 SFT+GRPO 路径 policy、蒸馏 student 与 10% 重用户混合推理，相对 NDCG@10 -7.44%。  social-recommendation llm-recommendation graph-reasoning reinforcement-learning distillation 搜广推 语义表征、用户知识与冷启动 ConnectionMind为什么输出证据路径，还把路径教师蒸馏给GNN？ 路径明确了推荐经由哪些关系逐步得到，能对中间扩展施加监督与奖励，而非只训练最终物品分数。复杂用户可用LLM在异构子图中搜索，较多普通流量交给蒸馏学生以控制成本。路径必须来自当前可见图；训练的最短正路径不能作为评估时已知答案直接提供给策略。 示意：从用户关注的作者走到摄影话题，再到教程，是一条可检查的证据链；简单场景可让学生复用这种关系模式，不必每次重新运行长程LLM搜索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-connectionmind-47def159" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dme" data-paper-title="Douyin Multimodal Embedding Model Technical Report" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Douyin Multimodal Embedding Model Technical Report 搜广推与 LLM 应用 ByteDance / Douyin 2026-08-03 对比学习向量服务高效但监督过粗，显式 CoT 又无法在线服务。DME 先做大规模多模态对比预训练，再以 Evidence-Grounded Typed Latent Reasoning 整理检索证据，并用 Cross-Conditional Reconstruction 保留对侧细粒度语义；两个生成头只在训练期使用。 Fidelity：核心机制复现。公开数据只验证论文机制，不模拟生产流量。未复刻 2B/9B 多模态 backbone、抖音私有语料和十亿级向量索引。本地对照口径：基线为共享 transition + content scorer，实验组只加入 DME 核心机制；相对 NDCG@10 -8.84%。  content-understanding multimodal-retrieval embedding llm-recommendation 搜广推 语义表征、用户知识与冷启动 DME的推理与重建生成头为什么只在训练期使用？ 对比向量便于在线检索，但可能忽略细粒度证据；训练期的typed latent目标和交叉重建要求表示保留对侧相关信息，再把这些能力压进检索向量。在线仍可只计算高效相似度，避免逐候选生成推理文本。辅助损失提供的是表示约束，不代表服务向量能忠实输出一条可解释推理链。 示意：训练中让查询向量保留商品的关键材质和用途，借重建任务检查是否丢失；上线直接用向量检索，不必为每一对查询和商品生成长解释。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-dme-01722658" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:kgd" data-paper-title="Knowledge–Geometry Decoupling: Refreshable Pretrained Transfer for Streaming Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Knowledge–Geometry Decoupling: Refreshable Pretrained Transfer for Streaming Recommendation 搜广推与 LLM 应用 Xiamen University / Shopee 2026-08-03 主题：流式推荐预训练与迁移。相邻点击并不总是有效依赖。KGD 用 BMTP 筛出协同或语义相关的未来物品；迁移时冻结可刷新知识编码器，用只读 cross-attention 读取知识，并以与锚点正交的 ACR 写入任务几何。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。MovieLens-1M 上比较相邻 NTP 与 BMTP+冻结知识+正交 ACR，执行全库排序。  sequential-recommendation pretraining streaming transfer 搜广推 语义表征、用户知识与冷启动 KGD为什么筛选相关未来物品，并让迁移残差与知识锚点正交？ 紧邻点击可能是噪声或任务切换，BMTP选择协同或语义相关的未来目标，让预训练知识更集中。迁移时冻结可刷新的知识编码器，任务侧只读它，再用去除锚点投影的残差补充新几何，减少直接覆盖已有知识。正交限制只规定更新方向，不能保证所有任务信息都能无损共存。 示意：相邻一次误触不应和稳定摄影需求同等监督；新任务要增加价格敏感信息时，可尽量沿知识锚点之外补充，而不是把已有摄影语义整体改写。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-kgd-b25439a8" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gala" data-paper-title="GALA: Generative Aligned Learning for Adaptive Multimodal Representation in the Taobao Shangou Recommender System" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="GALA: Generative Aligned Learning for Adaptive Multimodal Representation in the Taobao Shangou Recommender System 搜广推与 LLM 应用 Rajax Network Technology / Taobao Shangou / Alibaba 2026-07-31 先在 query-image-text 三元组上预训练多模态表示，再以行为奖励做 GRPO 对齐，最后用自适应门控融合多模态与 ID 表示。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  multimodal-recommendation representation-alignment reinforcement-learning 搜广推 语义表征、用户知识与冷启动 GALA完成图文预训练后，为什么仍要用行为奖励对齐并门控融合ID表示？ 图文相互匹配不代表符合个性化消费偏好，行为奖励让多模态表示朝推荐任务调整。门控再根据样本决定语义和ID信息的比例，避免内容优势覆盖已有协同知识，也让新物品更有机会利用内容。奖励有偏或门控塌到单一路径时仍可能失效，不能把多模态检索能力直接当最终推荐收益。 示意：商品图片和文案彼此一致，却不一定适合某位用户；行为对齐补上偏好信号，门控对有大量反馈的老商品和无反馈新品采用不同依赖。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-gala-83e5be9a" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:open-web-ufm" data-paper-title="Building a User Foundation Model for the Open Web" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Building a User Foundation Model for the Open Web 搜广推与 LLM 应用 Teads 2026-07-30 开放网络 RTB 的用户身份不连续、历史短且受隐私选择影响。论文以 MLM 与序列级对比学习预训练浏览历史 Transformer，再向 CTR、赢标率等任务输出统一用户表示；训练配方由可审计 lifter 组成的 LLM-in-the-loop 搜索改进。 Fidelity: 核心机制复现。实现共享序列 encoder、双视图对比预训练和下游微调。未包含 Teads RTB 私有特征、Claude Opus lifter 搜索及生产 GDCN adapter。本地对照口径：基线与实验组使用同一 encoder、数据和 45 steps；实验组加入双视图预训练，相对基线 NDCG@10 +0.00%。  advertising user-foundation-model self-supervised-learning llm-optimizer 搜广推 语义表征、用户知识与冷启动 开放网络 UFM 为什么联合掩码预测与序列对比学习，而不只训练某一个 CTR 标签？ 掩码预测要求编码器从残缺浏览上下文恢复局部事件，对比学习要求同一用户序列的不同视图保持一致，分别提供局部与整体监督。预训练表示再供 CTR、赢标率等任务使用，减少对单一稀疏标签的依赖。但身份不连续和隐私选择仍影响输入分布，本地小切片的零增益不能被改写成跨任务有效性证据。 示意：一个短历史只有三次访问且没有点击标签。遮住其中一次仍可做上下文训练，同一历史的两种扰动也可构成正对；之后再用少量 CTR 标签训练任务头。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-open-web-ufm-467147f2" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:reco-reward" data-paper-title="RecoReward: Recommender-Guided Multimodal Description Generation for Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RecoReward: Recommender-Guided Multimodal Description Generation for Recommendation 搜广推与 LLM 应用 Kuaishou / Nankai University / Chinese Academy of Sciences 2026-07-28 冻结双塔推荐器，以目标用户与非目标用户的亲和力差作为奖励训练内容描述；线上 serving 只消费描述，不依赖用户画像。 Fidelity: 核心机制复现。本地执行推荐奖励目标与公开数据对照，不声称复刻生产 reward pipeline。没有微调 Qwen3.5-9B，也没有直播视频和快手私有行为；本地结果只验证 RAS 奖励可执行。本地对照口径：基线为 content-only semantic recall，实验组为 RAS 选择；Hit@10 -16.00%、NDCG@10 -9.68%，head share -24.14%（负结果）。  llm-recommendation multimodal reinforcement-learning retrieval 搜广推 语义表征、用户知识与冷启动 Reco-Reward 为什么奖励目标用户亲和力减去非目标用户亲和力，而不是只最大化通用吸引力？ 只提高目标用户得分可能产生对所有人都相似的热门描述。减去非目标用户亲和力，鼓励描述保留能区分目标受众的特征，冻结双塔又提供稳定奖励接口。线上只消费优化后的内容描述，不需要实时用户画像；但奖励模型可能有盲点，差分得分提高不等于真实用户满意度已被验证。 示意：把咖啡描述写成“品质好、人人爱喝”可能吸引所有人却缺少区分。针对手冲爱好者突出酸质与冲煮参数，才可能提高目标人群相对其他人群的亲和力。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-reco-reward-d01ebaa7" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mosaic" data-paper-title="Mosaic: A Fleet of User Embedding Specialists for Recommendation at Meta" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Mosaic: A Fleet of User Embedding Specialists for Recommendation at Meta 搜广推与 LLM 应用 Meta 2026-07-27 单个通用 user embedding 很难同时覆盖长期记忆、稠密特征、长序列兴趣和特定下游任务。Mosaic 把用户表征组织成可独立演进的 specialist fleet：memorization-driven、dense-heavy、sequential HSTU+MoE 和与下游任务联合训练的 CoTrain。下游排序器按需消费多个 embedding，而不是让一个网络承担所有目标。随着 fleet 增大，新 embedding 容易复制旧 embedding 的信息。 Fidelity: 核心机制复现。实际训练四类 specialist、MRM 复合任务和 cosine redundancy loss；缩小数据、序列长度和 serving 链路。MovieLens genre/popularity 代理 Meta 的多表面私有行为标签；本地 sequential specialist 是 GRU 而非 2048-token HSTU，CoTrain 也缩为小型 routed MoE。未复刻跨产品特征、CoEval、User Tower Zero-Out、AOTI、memcache 和线上混合 CPU/GPU serving，不能把本地 +3.49% 与论文线上 lift 直接比较。  user-embedding multi-task-learning sequential-recommendation mixture-of-experts 搜广推 语义表征、用户知识与冷启动 Mosaic 已经有多个专长用户向量，为什么还要对新向量施加去冗余目标？ 新增网络可能再次编码旧向量已有的信息，增加服务开销却不给下游新线索。Mosaic 把不同专长模型组成表征集合，并用任务关系挖掘学习联合行为，再约束新专长与既有表示的冗余。目标是增加互补信息，供下游按需使用；向量更正交只是一种训练约束，不等同于业务信息必然独立。 示意：已有向量擅长记住常买品牌，新模型若也只记品牌就价值有限。让新专长学习跨任务组合并减少重复，可补充“何时愿意探索新品”这类不同线索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-mosaic-eb607f0f" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dual-sid" data-paper-title="Tokens are All You Need: Dual-purpose Semantic IDs for Achieving LLM-Level I/O Efficiency in Recommendation Systems" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Tokens are All You Need: Dual-purpose Semantic IDs for Achieving LLM-Level I/O Efficiency in Recommendation Systems 搜广推与 LLM 应用 Google DeepMind / YouTube 2026-07-26 传统 SID 擅长表达协同身份，却仍需把大规模内容 embedding 输入推荐模型。论文以层次量化生成 SID，并加入 Semantic Decoder（SiDec）从 SID 重建内容表示，让同一串 token 同时支持生成式检索、排序和低 I/O 的在线 embedding reconstruction。 Fidelity: 核心机制复现。本地训练分层 SID、SID 转移与 Semantic Decoder 内容重建，并用于检索评分。genre 替代 YouTube 多模态内容；未复刻超大 codebook、线上 embedding reconstruction 和私有日志。本地对照口径：基线为同切分的 dense transition-content retrieval，实验组加入 Dual-purpose SID 与 SiDec；NDCG@10 相对 -12.40%。  semantic-id retrieval ranking content-understanding serving 搜广推 语义表征、用户知识与冷启动 Dual-purpose SID为什么还要用Semantic Decoder重建内容embedding？ 普通SID适合承载离散身份，却未必能替代下游需要的高维内容输入。SiDec训练从短码恢复内容表示，让同一码同时服务推荐身份与低I/O内容访问，减少反复搬运大向量。重建存在信息瓶颈，短码越省并不一定越好；本地小码本的质量损失说明压缩收益与推荐效果必须分开衡量。 示意：服务端只取三枚短码，再在模型内恢复商品内容向量，可减少外部读取；但若不同用途商品被压成同一码，解码器也无法凭空还原丢失差异。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-dual-sid-924ced9f" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pin-scale" data-paper-title="Pin-SCALE: Semantic Cascading and Alignment Learning for Engagement-Aware IDs in Cold-Start Recommendations" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Pin-SCALE: Semantic Cascading and Alignment Learning for Engagement-Aware IDs in Cold-Start Recommendations 搜广推与 LLM 应用 Pinterest 2026-07-19 Semantic ID 擅长冷启动，但在判别式 dense retrieval 中缺乏系统接入方案。Pin-SCALE 保留 residual hierarchy 做 cascading pooling，以 engagement-aware tokenization 引入协同信号，再用 query-item 与 item-item 多视角对比学习对齐 SID 和参与度预测。 Fidelity: 核心机制复现。执行 engagement-aware residual codebook 和 SID 级联相似度。SIGIR program 是当前可核验原始入口；没有伪造 arXiv ID。公开 popularity/transition 仅代理 Pinterest engagement。本地对照口径：基线是 unweighted semantic/content ranker；实验组使用 engagement-weighted 三层 SID，NDCG@10 0.03540→0.04022，相对 +13.61%，fresh Hit@10 相对 +50.00%。  semantic-id engagement-aware generative-retrieval 搜广推 语义表征、用户知识与冷启动 Pin-SCALE 为什么保留 Semantic ID 的残差层级，并加入参与度与多视角对比监督？ 纯语义离散码有利于新物品共享内容知识，却未必对推荐行为最有辨别力。保留残差层级并逐级聚合，可利用粗到细的信息；参与度感知训练和查询—物品、物品—物品对比目标，再把码与推荐相关性连接起来。SID 因而是参与检索训练的表示部件，而不只是把文本向量换成整数标签。 示意：两个“客厅装修”内容语义相近，但服务不同兴趣人群。粗层码保留主题，细层码补充差别；参与度和共现对比使检索表示进一步反映用户实际使用关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-pin-scale-f40ee8a5" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recap" data-paper-title="RECAP: Feedback-Driven Streaming Semantic User Profiles for Short-Video Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RECAP: Feedback-Driven Streaming Semantic User Profiles for Short-Video Recommendation 搜广推与 LLM 应用 Kuaishou Technology / USTC 2026-07-17 传统 LLM 用户画像只追求“总结得像”，没有直接优化未来推荐。RECAP 把画像变成带容量约束的结构化流式状态：LLM 负责语义 update，确定性逻辑负责生命周期、合并与淘汰；再用 LLM judge 筛出标签一致的行为 pair，训练双塔 evaluator，把匹配分数作为 GRPO reward 闭环更新画像生成器。 Fidelity: 核心机制复现。真实训练 causal Transformer updater、双塔评价器和 clipped GRPO，并执行固定容量画像状态机。自然语言画像和工业 LLM 缩为 category-token causal Transformer；没有快手私有日志、生产 LLM judge 和在线闭环。核心 SFT→evaluator→GRPO→bounded state 链路实际执行，但不声称复现线上收益。本地对照口径：基线是 open-loop SFT 流式画像；实验组增加反馈 evaluator 与 GRPO，NDCG@10 相对 -6.77%。  llm-recommendation semantic-profile grpo 搜广推 语义表征、用户知识与冷启动 RECAP 为什么把画像更新拆成 LLM 语义修改和确定性生命周期管理，再用推荐反馈训练？ 语言模型擅长理解新行为，却不适合独自保证容量、合并与淘汰规则。确定性状态机约束画像大小和生命周期，LLM 在其中更新语义；评价器再把画像与后续行为的匹配转成奖励，使训练目标从“摘要像不像”转向“是否有助预测”。奖励仍是代理，需防止评价器偏差被策略放大。 示意：用户从跑步转向骑行，新行为可更新运动偏好，但过期条目由规则淘汰以免画像无限增长。若新画像更能匹配后续骑行行为，反馈再鼓励这种更新方式。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-recap-84f36c5b" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:proximity-features" data-paper-title="Proximity Features: Privacy-Compliant Cold-Start Personalization at Airbnb" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Proximity Features: Privacy-Compliant Cold-Start Personalization at Airbnb 搜广推与 LLM 应用 Airbnb 2026-07-14 匿名用户没有 user ID。Airbnb 把 consented geo-IP population-center 坐标聚成约 1,000 用户的 proximity key：密集位置用 IP hash 细分，稀疏位置逐级降低地理精度合并；群体行为按稳定 key 每日聚合，线上无需持久个人标识。 Fidelity: 核心机制复现。dense hash refinement、sparse fine-to-coarse clustering、稳定 proximity key、群体聚合与冷启动 scoring 均实际执行。ZIP prefix 不是 geo-IP 坐标；阈值缩为 12，只验证算法，不构成论文约 1,000 用户的隐私保证。本地对照口径：基线是 global cold-start aggregate；实验组用 MovieLens ZIP 的 adaptive proximity aggregate，验证集选择 blend 1.0，相对基线 Hit@10 +16.67%、NDCG@10 +22.91%。  cold-start privacy features 搜广推 语义表征、用户知识与冷启动 Airbnb 的 proximity key 为什么在密集地区细分、稀疏地区合并，而不使用固定地理网格？ 固定网格在城市可能过大，在稀疏地区又可能只包含极少用户。自适应 key 以人群数量为约束，密集处用哈希进一步拆分，稀疏处降低地理精度合并，使群体特征有足够支持。每日聚合提供匿名冷启动信号，而不是持久识别个人；空间邻近也只是群体偏好的代理，不能等同于个人兴趣。 示意：市中心一小块已有数千人，可再细分；郊区相同面积只有十人，就要扩大区域再聚合。两者都争取形成有足够样本的群体，而不是强行使用同样大小的格子。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-proximity-features-c055e9e4" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tokenminds" data-paper-title="TokenMinds: Pretrained User Tokens and Embeddings for User Understanding in Large Recommender Systems" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="TokenMinds: Pretrained User Tokens and Embeddings for User Understanding in Large Recommender Systems 搜广推与 LLM 应用 Google DeepMind / YouTube 2026-06-23 传统工业用户建模把完整兴趣压入少量稠密向量，容易损失细粒度、多峰兴趣；直接让 LLM 输出文本画像又难以与非文本 item ID 和下游排序模型对齐。TokenMinds 将 PLUM 的 item Semantic ID（SID）体系扩展到用户侧：encoder 读取视频 SID、观看特征和搜索文本并输出稠密用户向量，decoder 则自回归生成若干代表未来兴趣的 SID 用户 token。下游同时使用两种表示，从而保留现有 dense feature 兼容性并引入离散、可落到内容语义空间的兴趣表示。 Fidelity: 核心机制复现。本地实际训练共享序列编码器、稠密用户向量、分层 SID 用户 token 预测头及下游融合排序；Google 的 Gemini MoE、YouTube 私有数据和异步生产服务不在本地冒充复刻。本地训练了论文中心的 dual-output 路径，而不是只把配置命名为 TokenMinds。MovieLens genre 取代 YouTube 多模态内容，320 users / 480 items 与 32 条历史取代数十亿用户、1,200 watches 和搜索序列；  llm-recommendation user-modeling semantic-id cross-scenario ranking serving 搜广推 语义表征、用户知识与冷启动 TokenMinds 为什么同时输出稠密用户向量和代表未来兴趣的 SID 用户 token？ 单个稠密向量容易压平多峰兴趣，纯文本画像又难与非文本物品和排序器对接。encoder 保留通用稠密接口，decoder 以物品 SID 空间生成多个未来兴趣前缀，使下游同时获得连续概况与可落到内容空间的离散兴趣。未来窗口采样降低紧邻下一步偏好，但这些目标只用于训练，不能进入在线历史。 示意：用户同时喜欢烘焙和摄影，稠密向量给出总体偏好，两个 SID 前缀分别指向相关内容簇。排序器可同时读取两种表示，而不必从一段模糊文本里再猜商品编码。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-tokenminds-03a3a530" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:g2rec" data-paper-title="Structuring and Tokenizing Distributed User Interest Context for Generative Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Structuring and Tokenizing Distributed User Interest Context for Generative Recommendation 搜广推与 LLM 应用 Meta 2026-06-18 生成式推荐把 item 当 token，但纯 item 序列难以表达一个物品跨多个兴趣簇的语义，也难以利用分散在不同用户行为中的共现结构。G2Rec 从全站 co-engagement 构造 item-item 图，以可微 soft modularity 学习一个 item 对多个 interest prototype 的软归属，再把 item token 与其 interest-profile token 交替输入生成模型，并增加 profile prediction loss。 Fidelity: 完整核心链路复现。当前代码实际优化稀疏图 soft modularity，并训练交替 item/continuous-interest token 的自回归 Transformer、next-item loss 与 profile loss。本地对照口径：基线是参数级别匹配的 Item-only Autoregressive Decoder；实验组是 G2Rec Item+Interest Decoder；NDCG@10 从 0.0474 升至 0.0530（+11.92%）。这是 interest-token 组织与辅助目标的联合消融，不是相对 DIN。   搜广推 语义表征、用户知识与冷启动 G2Rec为什么允许一个item软归属多个兴趣prototype？ 同一内容可被不同兴趣群体共同消费，硬分到单簇会抹掉跨兴趣联系。G2Rec利用全站共参与图学习软归属，再把由prototype组合成的兴趣token与item交替输入生成器，补充单个ID看不到的分布式上下文。图构造只能使用可见训练行为，否则兴趣结构本身也会泄漏测试关系。 示意：一段露营做饭视频同时属于户外与烹饪，两个软归属能影响后续预测；硬塞进单一标签会让模型难以解释另一群用户为什么也会喜欢它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-g2rec-310e6cb6" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:atomic-intent" data-paper-title="Atomic Intent Reasoning: Bringing LLM Semantics to Industrial Cross-Domain Recommendations" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Atomic Intent Reasoning: Bringing LLM Semantics to Industrial Cross-Domain Recommendations 搜广推与 LLM 应用 The Hong Kong Polytechnic University 2026-06-09 将昂贵的 LLM 推理移至离线，把单次行为转成可缓存的层级原子意图；在线按目标商品检索意图链，并用多头注意力聚合跨域证据。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05240，相对变化 -2.98%。本地代理目标与论文生产任务不同，不能外推线上 lift。  cross-domain llm-recommendation intent-retrieval 搜广推 语义表征、用户知识与冷启动 把跨域行为先变成原子意图并缓存，为什么不等同于直接缓存一个用户向量？ 原子意图保留可检索的层级证据，在线还能按目标商品选择相关意图链，而一个固定用户向量往往已把不同需求揉在一起。昂贵推理离线完成，候选条件化检索与聚合在线执行，兼顾复用和针对性。本地代理评分没有验证完整LLM意图生成链路，不能由其指标推断线上推理质量。 示意：一次观看可以留下户外、露营、轻便装备等层级意图；推荐帐篷时取露营链，推荐通勤包时取轻便需求，而不必重跑整段LLM历史推理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-atomic-intent-04e8fc99" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ssrlive" data-paper-title="SSRLive: Live Streaming Recommendation with Dynamic Semantic ID" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SSRLive: Live Streaming Recommendation with Dynamic Semantic ID 搜广推与 LLM 应用 Taobao &amp; Tmall Group, Alibaba 2026-06-05 用静态语义 ID 表达主播长期内容，用动态语义 ID 捕获实时直播状态，再融合用户—主播交互特征完成观看、交易与互动多任务预测。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05351，相对变化 -0.92%。本地代理目标与论文生产任务不同，不能外推线上 lift。  live-streaming semantic-id multitask-ranking 搜广推 语义表征、用户知识与冷启动 SSRLive 为什么同时保留主播静态 SID 与直播动态 SID，而不持续覆盖同一份语义码？ 静态 SID 表达主播长期内容，动态 SID 描述当前直播状态，两者时间尺度不同。分开保留能让模型区分稳定定位与临时变化，再结合用户—主播互动做多任务预测；若只覆盖同一份码，短期话题可能抹去长期信息，旧状态也易误当实况。动态码仍受提取与更新延迟限制，不能保证实时完全准确。 示意：主播长期做美妆，今天临时讲旅行收纳。静态码保留美妆受众基础，动态码说明当前主题，让模型决定此刻更适合推给哪类用户，而不是永久改写主播身份。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-ssrlive-efb93285" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pinterest-ads-llm" data-paper-title="Fine-Tuned LLM as a Complementary Predictor Improving Ads System" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Fine-Tuned LLM as a Complementary Predictor Improving Ads System 搜广推与 LLM 应用 Pinterest 2026-05-27 论文没有让 LLM 替换广告召回或排序，而是把它作为 ancillary predictor：输入用户画像、历史转化、搜索、URL、品类和品牌，预测下一批高转化意图 advertiser 与兴趣。预测结果一方面成为 advertiser 定向的补充召回通道，另一方面作为 ctcvr/vtcvr 特征进入后续排序。训练分三层：先用单一 next-advertiser 标签做 SFT；再用 GRPO 生成 20 个 advertiser 与 5 个兴趣，并用命中位置和严格输出长度计算 reward； 未运行 Pinterest 私有 PinCLIP SID 三阶段 CPT，也不声称本地 AUC/Recall 可外推 RoAS。Fidelity: 完整核心链路。本地实际执行开源 causal LLM 的 LoRA SFT、论文位置/格式 reward 驱动的 clipped GRPO、受约束 advertiser 解码、训练式 two-tower、validation 配额选择的补充召回，以及 LLM advertiser score 作为排序特征。Pinterest 私有广告与跨站转化数据由公开商品品牌和购买序列替换。使用真实预训练语言模型和可训练 LoRA，不是规则或 embedding 打分替代 SFT/GRPO。  advertising llm-sft grpo candidate-generation 搜广推 语义表征、用户知识与冷启动 Pinterest Ads LLM 为什么只预测辅助 advertiser 与兴趣，而不接管实时广告排序？ 大模型汇总画像与跨来源行为后，离线预测高转化意图的 advertiser 和兴趣，再作为补充召回通道及转化率特征输入现有链路。SFT 学下一 advertiser，GRPO 用命中位置和输出长度奖励调整列表。每日批推理把成本移出请求路径，因此它改善的是现有系统的辅助信息，不等于端到端替代召回和排序。 示意：模型夜间预测某用户可能关注露营品牌，次日广告链路多一条相关召回和兴趣特征；是否展示某条广告，仍由实时转化模型和竞价规则共同决定。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-pinterest-ads-llm-d99be125" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:l2rec" data-paper-title="L2Rec: Towards Dual-View Understanding of LLMs for Personalized Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="L2Rec: Towards Dual-View Understanding of LLMs for Personalized Recommendation 搜广推与 LLM 应用 NetEase Cloud Music 2026-05-26 共享 LLM 中插入按用户路由的双视图 LoRA-MoE，分别适配语义视图和行为视图，再由自适应跨视图门控融合。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  llm-recommendation parameter-efficient-tuning multi-view 搜广推 语义表征、用户知识与冷启动 L2Rec为什么为语义视图和行为视图分别配置用户路由的LoRA专家？ 语义与协同行为可能互补也可能冲突，共用一套适配参数容易让强信号覆盖另一种。双视图低秩专家分别学习各自更新方向，用户路由再选择合适组合，跨视图gate决定最终融合。参数高效不代表无需足够监督；若路由总选同一专家，仍可能退化成没有分工的共享适配器。 示意：新用户主要靠内容语义，老用户可借丰富共同行为；两个视图分别保留能力后按用户组合，比一套LoRA强行同时解释所有场景更有弹性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-l2rec-4fe523da" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:muchator" data-paper-title="MuChator: Enabling Active Music Discovery via Conversational Music LLMs in Douyin Music" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="MuChator: Enabling Active Music Discovery via Conversational Music LLMs in Douyin Music 搜广推与 LLM 应用 ByteDance 2026-05-26 围绕音乐领域继续预训练、SFT 与强化学习，让对话模型从用户即时表达中解析音乐意图，并主动探索而非只复述历史偏好。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04477，相对变化 -17.09%。本地代理目标与论文生产任务不同，不能外推线上 lift。  music-recommendation conversational-llm active-discovery 搜广推 语义表征、用户知识与冷启动 MuChaToR 为什么在音乐领域预训练和指令学习之外，还要优化意图、探索与对话奖励？ 领域预训练主要补音乐知识，指令学习教模型按示例回答，却未必让它处理即时偏好和探索之间的取舍。强化学习把意图满足、新发现与对话质量转成行为反馈，并用参考策略约束更新。模型因此有机会学会何时沿用熟悉风格、何时主动探索；本地代理排序结果不能当作真实音乐对话效果。 示意：用户说“通勤想听轻松点，但别总是老歌”。只模仿历史可能继续推熟悉艺人，奖励设计则让模型同时顾及轻松氛围和适度的新艺人发现。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-muchator-f63c99f7" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:akt-rec" data-paper-title="From Head to Tail: Asymmetric Knowledge Transfer in Long-tail Recommendation with Generative Semantic IDs" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="From Head to Tail: Asymmetric Knowledge Transfer in Long-tail Recommendation with Generative Semantic IDs 搜广推与 LLM 应用 Alibaba Group / Peking University 2026-05-22 工业推荐的用户与物品都呈强长尾分布。直接共享表示可能把尾部稀疏且噪声较大的信号反向传给头部，普通对称对比学习因此不一定安全。AKT-Rec 先用 MLLM 对齐内容和协同信号，再用 RQ-VAE 把用户、物品量化成层级 Semantic ID，以同一高层 ID 定义语义簇。排序阶段为每个 ID 同时学习 cluster view 和 individual view。非对称 InfoNCE 对 tail→head 方向赋更大权重，并在作为 teacher 的一侧 stop-gradient； Fidelity: 核心机制复现。本地对真实 SmolLM2-135M 注入 LoRA，实际执行物品共现对比微调、用户兴趣/类别监督、残差 Semantic ID、cluster/individual 双视图、head-to-tail 非对称 stop-gradient、正交约束与两级活动度门控。真实训练开源 causal LM 的 LoRA，并分别执行物品协同对齐和用户监督；没有用哈希或静态文本向量替代这两步。本地对照口径：基线是只使用 individual embedding 和实例级 target attention 的 online_base；  llm-recommendation semantic-id long-tail ctr-ranking 搜广推 语义表征、用户知识与冷启动 AKT-Rec为什么让长尾更多地向头部学习，并阻断teacher一侧梯度？ 头部交互更丰富，通常可为同语义簇的长尾提供较稳定知识。非对称迁移加强尾部向头部对齐，并用stop-gradient避免尾部噪声反向拖动teacher；cluster与individual两视图及活动度门控又保留个体差异。若完全共享或双向同权，就可能既污染头部，又把不同长尾物品揉成一团。 示意：一款新品鞋可借同簇热销鞋的共同知识，但保留自己的尺码与用途；新品少量偶然点击不应立即改写整个热销簇的表示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-akt-rec-be638f5f" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:fluid" data-paper-title="FLUID: From Ephemeral IDs to Multimodal Semantic Codes for Industrial-Scale Livestreaming Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="FLUID: From Ephemeral IDs to Multimodal Semantic Codes for Industrial-Scale Livestreaming Recommendation 搜广推与 LLM 应用 TikTok / ByteDance 2026-05-20 直播间通常只存活几十分钟，候选 item ID 来不及积累协同信号。FLUID 用 SigLIP2 与 Qwen3-Embedding 跨域编码短视频和直播的两分钟切片，再用四层 RQ-KMeans 得到 LUCID。slice LUCID 表示当前内容，room LUCID 对历史切片逐层多数投票；两者以独立 token 晚融合，最终完全移除候选 item ID，并用“加 slice—退 ID—加 room”三阶段避免切换不稳定。 未运行 SigLIP2、Qwen3-Embedding-0.6B、直播 ASR/OCR、真实两分钟切片和生产增量训练；Fidelity: 核心机制复现。执行跨域内容融合、slice/room 两级 LUCID、RQ-KMeans、prefix n-gram、ID-free late fusion 与三阶段 warmup；公开数据替代生产多模态流量。未运行 SigLIP2、Qwen3-Embedding-0.6B、直播 ASR/OCR、真实两分钟切片和生产增量训练；本地证明的是 LUCID/去 ID/分阶段迁移链路可运行，不声称复现论文线上收益。  llm-recommendation multimodal semantic-id cold-start ranking 搜广推 语义表征、用户知识与冷启动 FLUID为何同时保留slice和room两种LUCID，并逐步退出item ID？ 短命直播间来不及积累稳定ID信号，slice码表达当前切片内容，room码从历史切片聚合较稳定语义。两者分开并晚融合，避免把瞬时内容与长期房间特征混成一个标签；分阶段加入切片、退ID、加房间，则降低特征切换对训练的冲击。退掉ID并不意味着内容码没有碰撞或新鲜度问题。 示意：同一房间平时卖运动服，此刻切片却在展示鞋；room码保留长期定位，slice码响应当前商品，不能只用一个已经过时的房间身份解释两种信号。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-fluid-d95a4248" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mm-llm" data-paper-title="A General Framework for Multimodal LLM-Based Multimedia Understanding in Large-Scale Recommendation Systems" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="A General Framework for Multimodal LLM-Based Multimedia Understanding in Large-Scale Recommendation Systems 搜广推与 LLM 应用 Meta 2026-05-10 视觉 embedding 难表达细粒度语义。论文用视觉 encoder+Q-Former 对齐 LLaMA2 生成 caption，再规范化为 categorical token IDs；item tokens 和用户历史 token profile 与 ID/视觉特征拼接进入生产排序模型，LLM 推理脱离在线主链路。 caption 模块相对 ID+content 内部基线仅 +0.03% 且 Hit 下降，本地未验证有效收益。Fidelity: 核心机制复现。内容 encoder、query cross-attention、离散 caption token、用户语义兴趣和 ID/视觉排序融合均训练；原始私有图片及 BLIP-2/LLaMA2-1.5B 规模未复刻。本地对照口径：统一跨模型基线是 DIN，MM-LLM NDCG@10 相对 DIN -13.23%；内部 ID+content 基线加入 caption token 后仅 +0.03% 且 Hit 下降。内部持平不代表优于经典模型。  multimodal llm-recommendation ranking 搜广推 语义表征、用户知识与冷启动 MM-LLM 为什么把视觉内容先转成规范化语义 token，而不在每次排序时直接调用大模型？ 视觉向量包含丰富信息，却不容易让排序器稳定利用细粒度语义。论文离线用视觉编码器、Q-Former 与语言模型生成描述，再规范化为可复用的类别 token；排序器融合这些语义与 ID、视觉特征。大模型负责提炼内容，在线小模型负责结合行为打分，两阶段把语义成本摊到多次请求。 示意：一张视频封面可离线得到“雨天、露营、装备教学”等 token。用户请求时排序器只读取这些特征和历史偏好，无须重新让语言模型看图解释。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-mm-llm-7bcb82aa" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recgpt-mobile" data-paper-title="RecGPT-Mobile: On-Device Large Language Models for User Intent Understanding in Taobao Feed Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RecGPT-Mobile: On-Device Large Language Models for User Intent Understanding in Taobao Feed Recommendation 搜广推与 LLM 应用 Alibaba / Taobao 2026-05-06 云端 LLM 能把点击、加购、收藏、购买等隐式行为翻译成显式搜索意图，但频繁上传行为并推理会增加成本、延迟和隐私风险。RecGPT-Mobile 把 Qwen3-0.6B 量化模型放到手机端，形成“本地收集行为→自适应构造 prompt→生成下一 query→服务端检索”的链路。训练数据由行为/搜索日志 60%、共购关系 20%、GPT 改写 15% 和人工标注 5% 组成；LoRA SFT 学习行为到 query 的映射。 Fidelity: 核心机制复现。实际执行 causal LM LoRA SFT、预算约束 adaptive prompt、意图漂移触发与 INT8 权重量化；私有数据和手机端系统缩小。本地模型是真实 causal LM 和 LoRA，不是类型分类 MLP；adaptive prompt、三项漂移公式和量化路径均执行。MovieLens 类型替代淘宝搜索 query，没有 GPT 改写、人工标注、生产检索和真机 fleet，故只验证方法链路与相对趋势。本地对照口径：基线为同一 SmolLM2-135M-Instruct 的零样本 intent completion；  llm-recommendation on-device intent-understanding serving-efficiency 搜广推 语义表征、用户知识与冷启动 RecGPT-Mobile 为什么只在联合漂移信号越过阈值时重新生成 query，而不是每次行为都触发？ 端侧推理虽减少行为上传，仍消耗电量和延迟。熵变化、集合重叠与分布散度共同判断意图是否实质变化，再按预算选择 prompt 组件，避免重复生成几乎相同的查询。生成结果交给服务端检索，所以端侧承担的是行为到意图的转换；漂移门控仍可能漏掉小幅但关键的新需求。 示意：连续浏览同类跑鞋不必每点一次都重跑模型；突然转向婴儿用品时，多种漂移指标共同变化才触发新查询。端侧给出意图后，服务器继续执行商品检索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-recgpt-mobile-6c2409d1" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:adasid" data-paper-title="Beyond Static Collision Handling: Adaptive Semantic ID Learning for Multimodal Recommendation at Industrial Scale" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Beyond Static Collision Handling: Adaptive Semantic ID Learning for Multimodal Recommendation at Industrial Scale 搜广推与 LLM 应用 University of Electronic Science and Technology of China / Kuaishou 2026-04-26 按碰撞负载、语义相容性和训练阶段动态放松 SID 重叠约束，避免把所有碰撞等价惩罚。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 adasid 核心机制，相对 NDCG@10 -6.30%。  semantic-id multimodal-recommendation retrieval 搜广推 语义表征、用户知识与冷启动 为什么AdaSID不把所有共享语义ID的物品都施加同样的碰撞惩罚？ 同码重叠有时表示有用的语义共享，有时才是无法区分的拥塞。AdaSID依据碰撞负载、物品语义相容性和训练阶段改变约束强度，在保留相关物品共性与区分不相关物品之间取得平衡。统一强惩罚可能把本来应靠近的内容硬拉开，统一放松则会掩盖高负载冲突。 示意：两款相近跑鞋共享粗层码可能合理，跑鞋与烤箱共享热门码却可能是拥塞；训练早期和码本趋稳后也未必该用相同惩罚强度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-adasid-04146a65" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:marc" data-paper-title="Modular Representation Compression: Adapting LLMs for Efficient and Effective Recommendations" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Modular Representation Compression: Adapting LLMs for Efficient and Effective Recommendations 搜广推与 LLM 应用 Shanghai Jiao Tong University 2026-04-20 论文发现 LLM 的中间层在推荐压缩后可能优于末层（MRA）。MARC 将压缩模块与任务适配模块显式拆开，并用信息约束解耦代理任务和推荐任务，保留任务相关信息的同时降低表征维度。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04693，相对变化 -13.11%。本地代理目标与论文生产任务不同，不能外推线上 lift。  llm-recommendation representation-compression modular-learning 搜广推 语义表征、用户知识与冷启动 MARC为什么把表征压缩与推荐适配拆开，并可能选择LLM中间层？ 末层偏向原语言任务，中间层有时包含更适合压缩的通用特征；但压缩保留的信息与推荐所需信息并不完全相同。分开两个模块并施加信息约束，能分别管理维度成本与任务选择，减少代理任务牵着推荐目标走。中间层优势属于需要检验的经验现象，不能默认对所有模型和数据成立。 示意：末层很擅长预测接下来的词，中间层却更容易保留商品用途；若只追重建原向量，可把与购买偏好无关的语言信息一起昂贵地保存。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-marc-216b86ce" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:lwgr" data-paper-title="LWGR: Lagrangian-Constrained Personalized World Knowledge for Generative Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="LWGR: Lagrangian-Constrained Personalized World Knowledge for Generative Recommendation 搜广推与 LLM 应用 Alibaba International / CAS 2026-04-16 固定人工 prompt 提取的 LLM 知识既不能表达用户兴趣异质性，也可能与行为信号冲突。LWGR 将用户上下文切成多个子空间，每个子空间从独立 codebook 选择 codeword，形成可端到端学习的个性化 soft instruction；soft tokens 与历史商品文本共同通过 LLM，得到用户级 world knowledge。生成式推荐 decoder 在 BOS 处 cross-attend 这些知识，同时用相对冻结 reference 的置信度退化约束控制有害融合。 因此本地只验证实现和梯度路径，未验证约束有效性或论文准确率收益。Fidelity: 完整核心链路。本地实际执行 parallel codebook、IBQ straight-through、用户 soft instruction 进入真实冻结 causal LLM、BOS cross-attention、冻结生成式 reference，以及逐步 primal-dual 更新。未用静态文本向量替代个性化 LLM 前向。使用真实 SmolLM2-135M 前向，soft instruction 的梯度穿过冻结 LLM 回到 codebook；未用预计算常量冒充该步骤。  generative-recommendation soft-prompt world-knowledge lagrangian 搜广推 语义表征、用户知识与冷启动 LWGR为什么学习个性化soft instruction，还要约束相对冻结reference的退化？ 固定prompt难以适应不同用户，分子空间codebook生成可训练soft tokens，让外部知识提取随偏好变化。但LLM知识也可能与行为模型冲突，冻结reference提供比较锚点，用置信度退化约束限制有害融合；nearline预计算控制服务成本。学到prompt并不保证知识真实或比行为信号更可靠。 示意：同样喜欢旅行，有人关注低价、有人关注摄影，soft instruction可引出不同知识；若新知识使既有可靠候选明显降分，约束应阻止无条件覆盖旧模型。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-lwgr-831cc9dc" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sid-coord" data-paper-title="SID-Coord: Coordinating Semantic IDs for ID-based Ranking in Short-Video Search" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SID-Coord: Coordinating Semantic IDs for ID-based Ranking in Short-Video Search 搜广推与 LLM 应用 Kuaishou Technology 2026-04-12 SID-Coord 不把语义信号仅作为普通稠密特征，而是构造多层离散 SID；再通过层级融合、目标感知 HID–SID 门控和历史兴趣对齐，在头部物品记忆与长尾泛化之间逐样本协调。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04970，相对变化 -7.97%。本地代理目标与论文生产任务不同，不能外推线上 lift。  short-video-search semantic-id long-tail-ranking 搜广推 语义表征、用户知识与冷启动 SID-Coord 为什么让 HID 与多层 SID 的融合 gate 依赖目标，而不是固定比例相加？ 头部物品的哈希 ID 有充分行为记忆，长尾物品更需要语义码共享知识，固定比例无法兼顾每个样本。目标感知 gate 决定两类信号的使用程度，多层融合保留粗细语义，历史对齐再连接用户兴趣。门控是在两种信息来源间协调，不代表 SID 能替代所有记忆，也不能保证每个长尾样本都会受益。 示意：热门电影已有大量点击，评分可多用 ID 记忆；刚上线电影行为少，更多依赖主题与风格 SID。即使同一用户，两种候选也可使用不同融合比例。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-sid-coord-811302bf" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cross-domain-kd" data-paper-title="Zero-shot Cross-domain Knowledge Distillation: A Case study on YouTube Music" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Zero-shot Cross-domain Knowledge Distillation: A Case study on YouTube Music 搜广推与 LLM 应用 Google / YouTube 2026-03-30 低流量产品无力训练大型专用 teacher。论文直接把数据丰富的 YouTube 多任务 teacher 应用于 YouTube Music 样本，把 serving task 与辅助 task logits 蒸馏到小模型，不要求源域数据或匹配的界面特征。 Fidelity: 核心机制复现。源域大 teacher、目标域小 student、目标样本上的 zero-shot logits 和 non-serving auxiliary-task distillation 均执行；私有跨产品 schema 未复刻。本地对照口径：跨模型基线是在相同 target split 上训练的 DIN，实验组 KD student 的 NDCG@10 相对 DIN -68.46%；内部基线 target-only student 加蒸馏后 +3.02%。后者只说明 KD 对弱 student 的增量，不能表述成优于 DIN。  distillation cross-domain ranking 搜广推 语义表征、用户知识与冷启动 跨域蒸馏为什么能不拿源域训练数据，却仍不能无条件信任源域teacher？ teacher可以直接对目标域样本输出任务与辅助任务知识，学生只需学习这些响应，因而不必获得源域日志。但源域模型面对新产品时仍可能校准错误或缺少关键特征，监督应与目标任务联合使用。知识可迁移不等于效果必然迁移；本地跨域对照的负结果不能被teacher规模掩盖。 示意：视频平台大模型给音乐场景样本提供偏好分布，学生可借到兴趣模式；但如果teacher把视频观看习惯等同于听歌习惯，蒸馏也会传入错误偏好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-cross-domain-kd-40631210" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gatesid" data-paper-title="GateSID: Adaptive Gating for Semantic-Collaborative Alignment in Cold-Start Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="GateSID: Adaptive Gating for Semantic-Collaborative Alignment in Cold-Start Recommendation 搜广推与 LLM 应用 Alibaba International Digital Commerce 2026-03-24 共享注意力融合语义与协同行为，再用冷启动感知 gate 调节对比对齐强度：新物品偏语义，热门物品保留协同信号。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 gatesid 核心机制，相对 NDCG@10 +34.95%。  semantic-id cold-start contrastive-learning 搜广推 语义表征、用户知识与冷启动 GateSID为什么让冷启动程度影响语义—协同融合和对比对齐强度？ 新物品缺少可靠行为，强行与稀疏协同向量一致可能引入噪声；热门物品已有丰富反馈，过度语义化又会损伤偏好差异。冷启动感知gate据状态调节两类信号及其对齐力度，使共享随证据强弱变化。它不是给所有新品永久使用纯内容，随着交互积累，融合策略也应能改变。 示意：两件文字相似商品中，一件已有大量特定人群购买记录，另一件刚上线；前者应保留协同特性，后者先借语义，而不是统一设一半一半。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-gatesid-592868f0" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tagllm" data-paper-title="TagLLM: A Fine-Grained Tag Generation Approach for Note Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="TagLLM: A Fine-Grained Tag Generation Approach for Note Recommendation 搜广推与 LLM 应用 Tongji University 2026-03-23 TagLLM 按笔记类目构建用户兴趣手册，用多模态 CoT 按兴趣维度抽取细粒度标签，再通过两阶段知识蒸馏把大模型标签能力迁移到小模型，兼顾解释性和线上效率。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05147，相对变化 -4.69%。本地代理目标与论文生产任务不同，不能外推线上 lift。  content-understanding tag-generation knowledge-distillation 搜广推 语义表征、用户知识与冷启动 TagLLM 为什么先按类目建立兴趣手册，再把多模态标签能力分阶段蒸馏给小模型？ 统一粗标签容易混淆不同类目的兴趣维度，手册先规定每类内容应从哪些方面理解，多模态推理再提取细粒度标签。大模型负责提供较丰富监督，小模型通过蒸馏学习稳定输出，使线上不必重复昂贵推理。可解释标签仍是对用户和内容的建模选择，手册遗漏的维度不会被蒸馏自动补齐。 示意：美食类关注口味与烹饪方法，旅行类关注目的地与出行方式。先建立不同维度，再教小模型抽取，避免把“轻松”在两类内容中都当作同一种兴趣标签。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-tagllm-3f53935e" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pinclip" data-paper-title="PinCLIP: Large-scale Foundational Multimodal Representation at Pinterest" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="PinCLIP: Large-scale Foundational Multimodal Representation at Pinterest 搜广推与 LLM 应用 Pinterest 2026-03-03 通用 VLM 的训练目标与推荐不一致，且新内容缺少行为。PinCLIP 以 VLM 为 backbone，混合多粒度图文特征，并加入 Pin-Board 图邻居对齐目标，让表征同时掌握内容和推荐图语义。 实验组学习内容—共现图 canonical alignment，NDCG@10 0.03540→0.03490，相对 -1.41%，未复现论文增益。Fidelity: 核心机制复现。执行内容—图邻居对比对齐和 fresh cohort 评估；不训练视觉 backbone。无图像像素、VLM 预训练和 Pinterest 全图；只验证 neighbor alignment 路径，不能据此否定原论文。本地对照口径：基线是 raw genre/content similarity；  multimodal contrastive-learning cold-start 搜广推 语义表征、用户知识与冷启动 PinCLIP 为什么在图文对齐之外加入 Pin-Board 邻居对齐？ 通用图文模型主要学内容相容性，而推荐还依赖用户把哪些内容组织到同一兴趣集合中。邻居对齐把图上的关联加入训练，使内容表示获得推荐语义；多粒度图文特征保留细节。这样新内容可凭内容进入已有空间，但邻居关系也可能含曝光偏置，不能把图对齐等同于真实偏好的无偏估计。 示意：两张图片一张是餐桌、一张是吊灯，视觉不相似，却经常出现在同一个北欧装修收藏板。邻居目标可把这种搭配关系写入表示，帮助新灯具连接装修兴趣。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-pinclip-b1beb580" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:idproxy" data-paper-title="IDProxy: Cold-Start CTR Prediction for Ads and Recommendation at Xiaohongshu with Multimodal LLMs" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="IDProxy: Cold-Start CTR Prediction for Ads and Recommendation at Xiaohongshu with Multimodal LLMs 搜广推与 LLM 应用 Xiaohongshu / Shanghai Jiao Tong University / Fudan University 2026-03-02 多模态 LLM 的语义空间与 CTR 模型长期学习的 item-ID 协同空间并不一致。IDProxy 先用粗粒度对比目标对齐两者，再从多层 hidden state 生成 proxy，通过 residual gate 注入工业排序网络。 复现保真度：核心机制复现。复现保真度：核心机制复现。粗对齐、多层 proxy adapter 和残差门控实际执行；InternVL 与私有图文未复刻。MovieLens genre 作为公开内容模态，先投影到双向行为转移 ID 空间，再执行多层非线性 proxy 和 gate。  multimodal-llm id-alignment ranking 搜广推 语义表征、用户知识与冷启动 IDProxy为什么先对齐MLLM与ID空间，再用多层proxy残差接入排序器？ 多模态语义能描述内容，却与长期CTR训练形成的协同坐标不一致，直接替换ID向量可能破坏已有几何关系。粗粒度对比先建立两空间对应，多层proxy再提取不同抽象程度的知识，通过gate控制注入幅度。残差保留原路径不代表无需对照，过强语义仍可能淹没有效协同差异。 示意：两件外观相似商品可能面向不同人群，语义向量不能直接覆盖ID偏好；先学会对应关系，再按状态借用形状、用途等不同层次信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-idproxy-2c030d0d" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:quasid" data-paper-title="Stop Treating Collisions Equally: Qualification-Aware Semantic ID Learning for Recommendation at Industrial Scale" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Stop Treating Collisions Equally: Qualification-Aware Semantic ID Learning for Recommendation at Industrial Scale 搜广推与 LLM 应用 University of Electronic Science and Technology of China / Kuaishou 2026-02-28 用业务资格信号决定碰撞对的 margin，而不是统一排斥；反馈稀疏或冷启动 item 得到更强的可辨识 SID。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 quasid 核心机制，相对 NDCG@10 -0.55%。  semantic-id collision-handling e-commerce 搜广推 语义表征、用户知识与冷启动 QuaSID 为什么对 SID 碰撞使用业务资格相关的 margin，而不是把所有相近物品等量推开？ 相近编码有助共享语义，但真正需要区分的物品若碰撞，会在生成和服务映射时混淆。资格信号决定哪些碰撞应更强排斥，以及需要多大距离，使有限码空间优先保留关键差异，尤其照顾反馈稀疏物品。统一排斥会破坏有用语义邻近；资格加权仍取决于业务信号质量，不能凭距离推断效果。 示意：两件几乎相同商品可共享粗码，但配送资格不同且必须分别服务，就应在细码上拉开；另两件差异无关当前业务，不必浪费同样强的分离约束。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-quasid-4adc5716" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rq-gmm" data-paper-title="RQ-GMM: Residual Quantized Gaussian Mixture Model for Multimodal Semantic Discretization in CTR Prediction" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RQ-GMM: Residual Quantized Gaussian Mixture Model for Multimodal Semantic Discretization in CTR Prediction 搜广推与 LLM 应用 Tencent 2026-02-13 把图文多模态 embedding 逐层做残差量化，每层以高斯混合后验进行软分配，避免硬聚类的 codebook 利用率不足；语义离散化与 CTR 偏好建模解耦训练。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04685，相对变化 -13.25%。本地代理目标与论文生产任务不同，不能外推线上 lift。  multimodal-recommendation semantic-tokenization ctr-prediction 搜广推 语义表征、用户知识与冷启动 RQ-GMM 在每层残差量化用高斯混合软分配，和最近中心硬量化有何取舍？ 硬分配只选择一个中心，边界样本容易跳变，少数中心也可能长期闲置。软后验让一个残差按概率组合多个高斯均值，再把量化结果从残差中减去进入下一层，使码本使用更平滑。代价是软表示与最终离散服务接口仍需衔接；语义量化与 CTR 训练解耦，也不保证码本天然最优于点击目标。 示意：一条视频同时像烹饪教学和生活记录，硬分配只能先选一类；软后验可按比例表达两者，再让下一层补残差，减少处在类别边界时的突然跳码。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-rq-gmm-d5d0f9d6" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sarm" data-paper-title="SARM: LLM-Augmented Semantic Anchor for End-to-End Live-Streaming Ranking" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SARM: LLM-Augmented Semantic Anchor for End-to-End Live-Streaming Ranking 搜广推与 LLM 应用 Institute of Information Engineering, CAS / Kuaishou 2026-02-10 离线 MLLM 生成直播语义 anchor，轻量 SAE 将 anchor 注入端到端排序；非对称部署只在线更新排序器，避免 MLLM 时延。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 sarm 核心机制，相对 NDCG@10 +44.74%。  live-streaming semantic-anchor multimodal-recommendation 搜广推 语义表征、用户知识与冷启动 SARM 为什么离线生成直播语义 anchor，却只在线更新轻量排序器？ 直播语义复杂，大多模态模型能提炼较丰富的锚点，但请求时调用会增加延迟。离线先产出 anchor，轻量语义模块将其接入端到端排序，再在线学习用户和候选的匹配关系，把内容理解与实时行为适配分开。anchor 若过时或遗漏动态内容，排序器也无法凭空恢复，因此异步更新频率是实际取舍。 示意：离线为直播提炼“户外装备讲解、价格比较”等锚点，请求到来时小排序器结合用户兴趣打分。直播主题突然切换时，旧锚点需更新，不能长期当作准确实况。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-sarm-37e57a11" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pit" data-paper-title="PIT: A Dynamic Personalized Item Tokenizer for End-to-End Generative Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="PIT: A Dynamic Personalized Item Tokenizer for End-to-End Generative Recommendation 搜广推与 LLM 应用 Beijing University of Posts and Telecommunications 2026-02-09 tokenizer 与生成推荐器共同训练，以用户引导的最小损失从多个候选 SID 中选出更契合当前偏好的编码；一对多 beam index 保留替代编码，减轻流式分布漂移。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05305，相对变化 -1.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation semantic-id dynamic-tokenizer 搜广推 语义表征、用户知识与冷启动 PIT 为什么允许一个物品保留多个候选 SID，再按用户推荐损失选择编码？ 固定单码把所有用户对物品的理解压成同一路径，流式偏好变化时也难调整。PIT 联合训练 tokenizer 与推荐器，并在替代编码中选使当前推荐损失更小的路径，让离散表示受到用户偏好监督。一对多索引保留路径选择余地，但增加索引与去重复杂度，不能把同一物品的多个码当作多个独立商品。 示意：一段“办公室拉伸”视频可从健身或久坐健康两个语义路径到达。面向不同用户选择更合适的编码有利于生成，但最终必须映回同一视频并去重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-pit-181d335d" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dos" data-paper-title="DOS: Dual-Flow Orthogonal Semantic IDs for Recommendation in Meituan" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="DOS: Dual-Flow Orthogonal Semantic IDs for Recommendation in Meituan 搜广推与 LLM 应用 Meituan 2026-02-04 普通 Semantic ID 的内容 codebook 与生成任务存在间隙。DOS 以用户行为流和商品语义流共同对齐 codebook，并用可约束的正交旋转把主语义与次语义解耦后逐层量化。 Fidelity: 核心机制复现。执行协同/语义双流、正交旋转及 residual quantization。公开 genre/共现替代美团 LLM item embedding 和生产生成器，不能与论文收入增益直接比较。本地对照口径：基线是未旋转的 content/collaborative ensemble；实验组执行 Procrustes 正交对齐与三层 ORQ，NDCG@10 0.03540→0.03938，相对 +11.26%。  generative-recommendation semantic-id orthogonal-quantization 搜广推 语义表征、用户知识与冷启动 DOS为什么先做正交旋转，再逐层量化，而不直接量化原始内容向量？ 内容空间的坐标方向未必适合分配语义码，直接切分可能把主要信息集中在少数方向。正交旋转在尽量保持几何关系的同时调整信息布局，再用残差量化分担主次信息；行为流与内容流共同校准codebook。正交并不自动产生独立语义，码的推荐价值仍需由行为目标验证。 示意：一段商品向量的大部分变化都挤在前几个坐标，旋转后可更均衡地分配给各层码；但是否区分了用户真正关心的属性，不能只看旋转矩阵满足正交。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-dos-16f0eac2" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recgpt-v2" data-paper-title="RecGPT-V2 Technical Report" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RecGPT-V2 Technical Report 搜广推与 LLM 应用 Alibaba / Taobao 2025-12-16 RecGPT-V1 的多条固定推理链重复且难泛化。V2 用层级多 Agent 拆解意图，混合压缩行为表示，动态生成 meta-prompt，再用多奖励约束 RL 和 Agent-as-a-Judge 对齐。 Fidelity: 核心机制复现。实际执行短期/长期/类目 agent、meta-router、混合表示与 KL 约束偏好更新。Agent 是公开数据上的可训练小型专家，不是淘宝私有 LLM；没有人工 Judge 标注、解释生成或线上资源测量。本地对照口径：相对 RecGPT-V1 单路兴趣基线，实验组 NDCG@10 +18.52%。  llm-recommendation multi-agent reinforcement-learning ranking 搜广推 语义表征、用户知识与冷启动 RecGPT-V2 为什么用层级多 Agent 和动态 meta-prompt 替代固定多条推理链？ 固定推理链容易重复覆盖同一兴趣，且难随用户上下文改变分工。层级 agent 先拆解意图，压缩行为表示，再动态构造适配当前任务的提示，使不同路径有更明确职责。多奖励与 judge 进一步调整输出质量，但增加 agent 数不自动带来独立知识，仍需检查重复推理、评判偏差和服务成本。 示意：用户近期既准备旅行又关注摄影，系统可分别提炼出行与设备需求，再按当前请求生成综合提示；若只套三条固定模板，可能三次都复述“喜欢摄影”。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-recgpt-v2-f68ee63c" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:saviorrec" data-paper-title="SaviorRec: Semantic-Behavior Alignment for Cold-Start Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SaviorRec: Semantic-Behavior Alignment for Cold-Start Recommendation 搜广推与 LLM 应用 Alibaba 2025-08-02 冷启动排序依赖内容语义，但通用多模态 encoder 的相似度不等于平台用户的共点/共购关系，而且行为分布持续变化。SaviorRec 先以真实交互监督训练 SaviorEnc，再用 RQ-VAE 把表示离散为 Semantic ID；线上排序阶段冻结 SID，同时用零初始化的 Modal-Behavior Alignment（MBA）码本学习相对当前行为空间的残差，并用 target 与历史双向注意力完成 CTR 预测。 Fidelity: 核心机制复现。真实执行行为监督内容编码、RQ Semantic ID、零初始化 MBA 残差码本、双向 target/history attention 和 CTR 训练；MovieLens genre 替代私有图文模型。本地对照口径：基线是等预算 Content Ranker；实验组是 SaviorRec；总体 AUC +1.56%、cold AUC +6.92%，但都只有 1/3 seeds 正向。这是语义—行为对齐模块消融，不是相对 DIN。  cold start semantic ID multimodal recommendation 搜广推 语义表征、用户知识与冷启动 SaviorRec 为什么冻结 SID，却用零初始化 MBA 码本学习行为残差？ 先用行为监督训练内容编码并量化，得到可迁移的语义骨架；部署后若直接重写 SID，会影响码的稳定性和历史映射。MBA 从零开始按同一离散码学习当前行为空间的残差，初始不扰动原表示，再逐步适配行为变化。目标与历史双向交互用于 CTR，但稳定编码也可能限制对大幅分布变化的响应。 示意：一类露营内容的语义码保持不变，季节变化使用户偏好从夏季轻装转向保暖。残差可调整该码当前的行为表示，而不必让所有内容重新换一套编码。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-saviorrec-24eec791" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:filterllm" data-paper-title="FilterLLM: Text-To-Distribution LLM for Billion-Scale Cold-Start Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="FilterLLM: Text-To-Distribution LLM for Billion-Scale Cold-Start Recommendation 搜广推与 LLM 应用 Alibaba 2025-02-24 逐用户判断难以服务十亿用户冷启动。FilterLLM 把商品文本一次映射为用户分布，通过用户词表压缩输出空间，并用历史行为指导分布学习。 Fidelity: 核心机制复现。实际学习文本到压缩用户词表分布，并用行为分布约束冷启动表示。用户词表由公开交互 SVD 压缩，不是十亿用户 LLM token；没有淘宝新品文本、流量和延迟栈。本地对照口径：相对 content-to-item judgment 基线，实验组 NDCG@10 -9.82%。  llm-recommendation cold-start retrieval text-to-distribution 搜广推 语义表征、用户知识与冷启动 FilterLLM为什么从商品文本直接预测用户分布，而不逐用户问LLM是否推荐？ 逐对判断的成本随用户数量扩大，新商品需要接触海量潜在用户时尤其昂贵。FilterLLM把一次内容编码映射到压缩用户词表上的概率分布，再用历史行为监督，让一个商品侧计算覆盖更多受众。词表压缩引入共享与分辨率取舍，预测分布也不意味着每个具体用户都已经获得可靠个性化判断。 示意：一篇新文章先产生对几类用户兴趣的分布，再把它接入候选流程；无需为每位用户重新生成一次LLM回答，但细粒度差异仍可能在压缩中丢失。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-filterllm-8613b323" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:seral" data-paper-title="Bursting Filter Bubble: Enhancing Serendipity Recommendations with Aligned Large Language Models" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Bursting Filter Bubble: Enhancing Serendipity Recommendations with Aligned Large Language Models 搜广推与 LLM 应用 Alibaba / Taobao 2025-02-19 惊喜推荐需同时相关且未见。SERAL 压缩超长历史为多层认知画像，以 LLM/人工 CDI 打破日志反馈环，用 IPO 对齐 SerenGPT，最后 nearline 生成并缓存候选。 内部消融中 IPO 相对纯 SFT 为 +8.59%，但 category-novelty 0.05542→0.05444，仍未复现惊喜度提升。Fidelity: 完整核心链路复现。静态/短期/长期 cognition profile、SFT、CDI 偏好对、IPO+SFT 与 nearline 全库缓存均执行；GPT-4/人工标注由公开内容和协同信号替代。本地对照口径：统一跨模型基线是 DIN，SERAL NDCG@10 相对 DIN +50.60%；内部基线是纯 SFT，增加 CDI+IPO 后 +8.59%，但 novelty 下降。排序收益与惊喜度结论分开报告。  llm-recommendation preference-alignment serendipity 搜广推 语义表征、用户知识与冷启动 SERAL 为什么引入 LLM 与人工的 CDI 偏好，再用 IPO 对齐，而不直接最大化历史命中？ 历史日志倾向重复已有曝光，单纯拟合会把未见但可能合适的内容排除。多层认知画像提供压缩上下文，CDI 补充日志外的偏好判断，IPO 对齐胜负并保留 SFT 约束，近线生成缓存降低服务成本。相关性与未见性需分别验证；本地排序提高但新颖度下降，不能只凭命中改善就称为更惊喜。 示意：用户一直看熟悉导演，日志只教会重复推荐。人工与模型可比较一部未看过却题材合适的新片和普通熟片，为探索提供信号，但仍需验证用户是否真的接受。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-seral-54db17e6" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:lum" data-paper-title="Unlocking Scaling Law in Industrial Recommendation Systems with a Three-step Paradigm based Large User Model" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Unlocking Scaling Law in Industrial Recommendation Systems with a Three-step Paradigm based Large User Model 搜广推与 LLM 应用 Alibaba 2025-02-12 端到端生成推荐能够扩展 Transformer 参数，却难以兼容长期演化的线上 DLRM、复杂特征和毫秒延迟。LUM 将问题拆成三步：先用生成任务构建用户知识，再用条件 token 离线查询不同兴趣，最后把固定知识特征接入任意判别式 DLRM。关键 token 顺序是：condition 描述即将预测的 item 所属场景、搜索词或类别，而不是事后附着在上一 item 上的 action。 Fidelity: 完整核心链路复现。真实执行 condition/item 异构 token encoder、causal next-condition-item InfoNCE、屏蔽式 group query、离线知识缓存、direct feature、interest matching 与下游 CTR DLRM；不声称复现 7B scaling law。本地对照口径：基线是 ID-DLRM；实验组是加入 LUM 离线知识的相同下游 DLRM；AUC 从 0.58233 升至 0.66734（+14.60%）。这是 LUM 知识特征消融，不是相对 DIN。  large user model generative pretraining knowledge querying CTR 搜广推 语义表征、用户知识与冷启动 LUM中的condition为什么要放在即将预测的item之前，而不是当上一item的反馈？ condition表达接下来选择发生的场景、查询或类别，它应约束未来物品分布；若附在上一物品上，就改变为解释过去行为的信号。LUM用条件化生成建立可查询的用户知识，再离线抽取多种兴趣特征供DLRM使用，而不是要求线上直接运行大生成模型。两种token语义不能只因形式相似就互换。 示意：用户接下来进入厨房品类，condition应帮助预测将看的锅具；若把它当成上一双跑鞋的反馈，训练就会学到完全不同的条件关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-lum-66a3db6d" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mim" data-paper-title="MIM: Multi-modal Content Interest Modeling Paradigm for User Behavior Modeling" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="MIM: Multi-modal Content Interest Modeling Paradigm for User Behavior Modeling 搜广推与 LLM 应用 Alibaba / Taobao 2025-02-01 纯 ID 行为模型难以理解新品内容。MIM 先遮盖重建多模态内容，再用 content-interest-aware SFT 对齐内容与协同兴趣，最后由 CiUBM 融合内容兴趣和 ID 兴趣。 Fidelity: 核心机制复现。实际执行遮盖内容重建、内容—协同对比对齐和 CiUBM 风格兴趣融合。genre 代理图文模态；没有淘宝私有曝光、真实多模态 encoder 与生产 serving。本地与论文线上数值不可直接比较。本地对照口径：相对 ID 共现兴趣基线，实验组 NDCG@10 +0.94%。  multimodal-recommendation user-modeling pretraining ranking 搜广推 语义表征、用户知识与冷启动 MIM先做多模态遮盖重建后，为什么还要content-interest-aware SFT？ 重建能学习内容内部结构，却不告诉模型哪些语义与用户偏好有关。后续SFT用消费兴趣对齐内容空间，再融合内容兴趣和ID兴趣，让新品知识与已有协同信号相互补充。若只完成内容重建，就不能声称已学到推荐相关性；ID与内容融合也需避免一侧完全压过另一侧。 示意：模型能补回商品图片的颜色，不代表知道用户关心轻便还是耐用；兴趣对齐把这些消费差异引入内容表示，之后再与有行为的老商品ID知识结合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-mim-fdc0fc79" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:msd" data-paper-title="Balancing Efficiency and Effectiveness: An LLM-Infused Approach for Optimized CTR Prediction" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Balancing Efficiency and Effectiveness: An LLM-Infused Approach for Optimized CTR Prediction 搜广推与 LLM 应用 Meituan 2024-12-09 直接在 CTR 链路调用大模型效果好但成本不可接受；只缓存静态 embedding 又无法跟随 CTR 目标更新。MSD 的 MKDM 先让大 teacher 为用户和物品生成关键词与推理，再让较小 student 自回归学习这些输出。MKIM 对蒸馏后的 student 做 LoRA CTR 对齐，并用 user/target/history adapter 融合推荐特征。高频物品优先走预计算缓存，低频或未命中物品在线编码，同时只融合与 target 最相关的历史。 Fidelity: 完整核心链路复现。真实执行 teacher 知识生成、T5 自回归蒸馏、student q/v-LoRA CTR 对齐、多层特征 adapter、频次自适应缓存/在线计算和相关历史融合；生产广告特征与缓存服务未复刻。本地对照口径：基线是 ID-only CTR ranker；实验组是完整 MSD；AUC 从 0.68449 升至 0.69510（+1.55%）。这是 LLM 蒸馏与缓存语义特征的联合消融，不是相对 DIN。  LLM distillation CTR serving efficiency 搜广推 语义表征、用户知识与冷启动 MSD 为什么先蒸馏大模型的关键词与推理，再对学生做 CTR 对齐，而不只缓存大模型 embedding？ 静态 embedding 能降低推理成本，却不会随点击目标调整。MSD 先让小学生通过自回归蒸馏学到教师的语义输出，再用 LoRA 和推荐适配器学习 CTR 相关表示。高频物品优先使用缓存，未命中部分在线编码，并只融合相关历史；这同时处理语义迁移、任务适配与服务成本，而非一次静态特征提取。 示意：教师离线解释一件外套的保暖与通勤属性，学生学会这种语义。CTR 阶段再根据用户行为调整表示；热门外套直接读缓存，新商品才触发在线编码。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-msd-3339b303" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:precise" data-paper-title="PRECISE: Pre-training Sequential Recommenders with Collaborative and Semantic Information" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="PRECISE: Pre-training Sequential Recommenders with Collaborative and Semantic Information 搜广推与 LLM 应用 Tencent / WeChat 2024-12-09 纯 ID 序列模型能学协同关系，但长尾物品训练不足；纯文本/LLM 方法能迁移语义，却容易丢掉协同信号。PRECISE 将二者在 item 层融合，并把训练拆为 Universal Training（全场景兴趣）和 Targeted Training（稀疏目标场景/任务）。论文还针对文本表示过强导致 ID 学不动的问题，先冻结 token 训练 ID，再解冻联合训练。 Fidelity: 完整核心链路复现。实际执行 LLM token hidden-state 初始化、可训练 token、top-k MoE attention、ID/text 交替训练、全场景 causal NIP、目标场景双向 Transformer、序列拼接 MLP 与 cross-user BPR。Qwen2-1.5B 缩为 SmolLM2-135M，WeChat 私有日志替换为 MovieLens-1M。本地对照口径：基线是只做目标任务训练的 PRECISE-TT；实验组是 UT 全场景预训练后再 TT；  LLM semantic embedding sequential pre-training MoE targeted training 搜广推 语义表征、用户知识与冷启动 PRECISE 为什么先冻结文本表示训练 ID，再解冻联合训练？ 预训练文本表示一开始可能远强于随机 ID 分支，优化器容易直接依赖文本，使 ID 得不到足够学习，协同信息因而缺席。先固定文本侧迫使 ID 学到可用差异，再联合训练让两者互补。全场景预训练到稀疏目标任务适配则解决迁移范围；总体指标改善并不保证长尾或冷启动子集同步改善。 示意：两部题材相近的电影文本很像，用户群却不同。若模型一直靠文本完成训练，ID 难学到群体差别；分阶段训练让 ID 先获得区分能力，再融合语义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-precise-dd30948e" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:learn" data-paper-title="Knowledge Adaptation from Large Language Model to Recommendation for Practical Industrial Application" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Knowledge Adaptation from Large Language Model to Recommendation for Practical Industrial Application 搜广推与 LLM 应用 Kuaishou 2024-05-07 直接把冻结 LLM embedding 用作推荐表示存在开放世界语义域与协同域的差距。LEARN 的 CEG 冻结 LLM 并平均池化 item 文本，PCH 用可训练因果 Transformer 从历史 content embeddings 学用户偏好，再投影到线上推荐空间。 Fidelity: 完整核心链路复现。真实执行冻结预训练 LM 的 CEG、缓存 item embedding、因果 PCH、dense all-position loss 和 online projection；BERT-tiny/MovieLens 替代 Baichuan2-7B/快手日志。本地对照口径：基线是 frozen LLM semantic mean；实验组是 LEARN CEG+PCH；NDCG@10 从 0.00487 升至 0.01622（+233.10%），同时 head share 升至 69.50%。这是知识适配模块消融，不是相对 DIN。  llm-recommendation knowledge-adaptation cold-start 搜广推 语义表征、用户知识与冷启动 LEARN为什么冻结LLM内容编码，却训练因果PCH来学习用户偏好？ 冻结内容编码保留开放世界语义并降低更新成本，但内容接近不等于共同消费。PCH在历史内容向量上学习顺序与下一物品目标，再投影到推荐空间，把通用语义转成偏好表示。模型仍需遵守历史时间边界；冻结LLM不意味着整个系统没有训练，也不能仅凭语义相似度判断迁移完成。 示意：两部电影文本都写冒险，用户却偏好其中一种叙事风格；固定内容向量给出基础语义，训练过的PCH可从其真实观看顺序中学习更细偏好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-learn-c99c03ce" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:bahe" data-paper-title="Breaking the Length Barrier: LLM-Enhanced CTR Prediction in Long Textual User Behaviors" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Breaking the Length Barrier: LLM-Enhanced CTR Prediction in Long Textual User Behaviors 搜广推与 LLM 应用 Ant Group 2024-03-28 直接把长用户行为文本反复送入 LLM，会重复编码同一原子行为，并把低层语义提取与高层行为交互强耦合。BAHE 在浅层编码每个原子行为并离线存储；训练时只取行为向量，以更深的可训练层聚合，再与候选物品一起完成 CTR 预测。这样既缩短上层序列，也允许浅层异步、低频更新。 Fidelity: 完整核心链路复现。真实执行冻结浅层 LLM 的原子行为编码与落盘、可训练上层 Transformer 的行为聚合和 CTR 训练；生产 LLM/广告日志替换为 BERT-tiny/MovieLens-100K。本地对照口径：基线是逐样本运行完整文本上层微调；实验组是 BAHE 原子缓存与层次聚合；耗时 -53.61%，但 AUC -2.94%。这是效率—效果对照，不是准确率提升。  llm-recommendation ctr-ranking long-sequence efficiency 搜广推 语义表征、用户知识与冷启动 BAHE缓存原子行为的浅层编码，为什么还需要在线训练的高层聚合？ 浅层主要提取单个行为文本的语义，可被不同请求重复使用；高层需要结合当前历史组合和候选判断兴趣，不能冻结为一份通用答案。分层把重复文本计算移出训练与请求路径，同时保留跨行为交互。缓存刷新过慢或压缩过强仍可能损害质量，效率改善不自动意味着准确率提高。 示意：一条电影标题只编码一次，但用户把它与科幻片还是家庭片一起看，会改变高层兴趣判断；遇到不同候选时也应重新聚合这些行为向量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-bahe-7645b8ec" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:lsvcr" data-paper-title="A Large Language Model Enhanced Sequential Recommender for Joint Video and Comment Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="A Large Language Model Enhanced Sequential Recommender for Joint Video and Comment Recommendation 搜广推与 LLM 应用 Kuaishou 2024-03-20 短视频用户会同时消费视频和评论。纯序列模型能高效服务，但难以理解评论语义；直接让 LLM 在线推荐又太慢。LSVCR 用 LLM 同时担任离线文本 encoder 和仅训练期存在的 supplemental recommender，再把 LLM 的个性化偏好对齐到可部署的双序列 SR 模型。部署时不需要运行生成式 LLM。 对齐 loss 明显下降，排除了 alignment 根本未训练的情况。Fidelity: 完整核心链路复现。真实执行 causal LM q/v-LoRA SFT、LLM 文本编码、随机位置扩展、商品/评论双 Transformer、双向 cross-attention、SSC/VCC 对齐和联合微调；ChatGLM3 与快手私有日志缩小替换。本地对照口径：基线是相同 SR 网络但不做 LLM preference alignment；实验组是完整 LSVCR；Comment NDCG@10 +50.40%，Item NDCG@10 -56.42%。这是 alignment 消融，不能概括成整体推荐效果提升。  LLM recommendation comment recommendation preference alignment 搜广推 语义表征、用户知识与冷启动 LSVCR上线不用生成式LLM，为什么训练时还让LLM提供个性化偏好？ 视频和评论包含不同语义，纯ID序列难以充分理解，LLM偏好可在训练中补充内容关系。双序列模型通过交叉融合及对齐目标吸收这些知识，部署时只保留可服务的推荐模型。两种任务可能相互牵制，本地评论与视频指标方向不同，不能只报告某一路改善就宣称整体成功。 示意：一条评论表达反讽，视频点击本身看不出来；训练期教师可补充语义，但上线学生仍需仅凭可用双序列作判断，不能每次暗中调用老师解释。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-lsvcr-e1dd0222" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:notellm" data-paper-title="NoteLLM: A Retrievable Large Language Model for Note Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="NoteLLM: A Retrievable Large Language Model for Note Recommendation 搜广推与 LLM 应用 Xiaohongshu 2024-03-04 纯文本 embedding 缺少协同信号，纯对比学习又可能损害 LLM 生成能力。NoteLLM 用统一 compression prompt 将内容压到特殊 token；GCL 拉近用户共读 note，CSFT 从同一压缩状态生成 hashtag/category。 Fidelity: 完整核心链路复现。真实执行 note compression special token、行为共现 GCL、类别生成 CSFT 和压缩状态 I2I 检索；T5-small/MovieLens 替代 7B LLM/小红书 note。本地对照口径：基线是冻结 compression-state embedding；实验组是 NoteLLM 的 GCL+CSFT embedding；NDCG@10 从 0.01142 升至 0.01224（+7.15%）。这是表征训练消融，不是端到端排序模型相对 DIN 的提升。  llm-recommendation contrastive-learning i2i-retrieval 搜广推 语义表征、用户知识与冷启动 NoteLLM 为什么让压缩状态同时接受共读对比学习和内容生成监督？ 共读对比学习把用户实际共同阅读的内容拉近，让表示获得协同关系；但单独追求相似度可能丢失细粒度文本语义。内容监督从同一压缩状态生成标签和类别，要求它保留可生成的内容信息。两个目标共同塑造瓶颈表示，使向量既适合检索，又不轻易退化为只记共现关系的编码。 示意：两篇都被露营用户阅读的笔记应在向量空间接近，但一篇讲帐篷、一篇讲炊具。生成各自标签的任务迫使压缩表示在共享兴趣之外仍保留内容差别。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-notellm-9364e133" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:kar" data-paper-title="Towards Open-World Recommendation with Knowledge Augmentation from Large Language Models" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Towards Open-World Recommendation with Knowledge Augmentation from Large Language Models 搜广推与 LLM 应用 Huawei 2023-06-19 封闭域推荐只能从本域交互学习，难以理解物品事实和用户偏好背后的常识。KAR 不把 LLM 直接当在线推荐器，而是通过 factorization prompting 让 LLM 分别产出用户偏好推理知识与物品事实知识，再用 hybrid-expert adapter 压缩成与 ID 推荐模型兼容的向量。知识可预生成并缓存，因此线上不承担 LLM 自回归延迟。 Fidelity: 完整核心链路复现。真实执行 factorization prompts、用户偏好/物品事实知识生成、离线缓存、hybrid-expert adapter 和下游 CTR 训练；PanGu 与华为日志替换为 SmolLM2-135M-Instruct 和 MovieLens-100K。本地对照口径：基线是纯 ID ranker；实验组是加入 LLM 知识与四专家 adapter 的 KAR；AUC 从 0.72188 升至 0.72774（+0.81%）。这是知识增强模块消融，不是相对 DIN 的比较。  llm-recommendation knowledge-augmentation ctr-ranking 搜广推 语义表征、用户知识与冷启动 KAR为什么分开生成用户偏好知识和物品事实，再用hybrid-expert adapter接入？ 用户知识描述为何可能喜欢，物品知识描述内容具有什么属性，二者来源与语义不同，直接拼接可能难与ID模型兼容。adapter通过共享及专属专家压缩和对齐，再与原表示共同预测；知识可离线缓存，线上不必自回归生成。LLM推断仍可能错误，不能把偏好解释当用户真实表态。 示意：物品事实是鞋具防水材质，用户知识是近期常看雨天徒步内容；两类信息通过适配器形成有用关系，但不能据此断言用户已经表示一定想买这双鞋。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-kar-c442fbbf" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:m6rec" data-paper-title="M6-Rec: Generative Pretrained Language Models are Open-Ended Recommender Systems" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="M6-Rec: Generative Pretrained Language Models are Open-Ended Recommender Systems 搜广推与 LLM 应用 Alibaba 2022-05-17 传统推荐模型为排序、召回、解释、对话分别维护架构。M6-Rec 把匿名行为序列和候选物品都改写成自然语言，让一个生成式预训练模型统一完成排序、召回、zero-shot、解释、内容生成和对话。为避免每个场景完整微调巨型 M6，论文提出 option tuning 和 option-adapter tuning，只训练约 1% 的任务参数；线上再用 late interaction、early exit、参数共享和剪枝得到 10M/2M 的 M6-Edge。 Fidelity: 核心机制复现。真实执行冻结预训练 Transformer、自然语言用户行为、option tuning 与逐层 bottleneck option-adapter tuning；M6 生产模型、私有数据和 early-exit/pruning serving 未复刻。本地对照口径：基线是只训练 option prototype 的 Option Tuning；实验组额外训练 24d adapter；AUC 从 0.53832 升至 0.53890（+0.12%）。这是 adapter 增量消融，不代表完整 M6-Rec 相对 DIN 或工业基线的提升。  llm-recommendation foundation-model parameter-efficient-tuning 搜广推 语义表征、用户知识与冷启动 M6-Rec统一多个推荐任务时，option tuning和adapter分别改动哪一部分？ 冻结主干保留预训练能力，option参数为任务选择提供轻量可学习接口，逐层adapter再增加小规模任务变换。两者让不同任务共享大模型而不必各自全量微调；但参数占比小不等于推理成本自然低，边缘部署仍需独立压缩与服务设计。本地小任务对照也不能证明巨型M6全部能力已迁移。 示意：同一冻结模型处理相关性判断与内容解释，可用不同任务option和小adapter适配；只训练很少参数仍可能需要经过大主干，因此不能直接声称已适合端侧。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<span id="paper-recommendation-m6rec-d70d1b1b" class="ar-learning-paper-anchor"></span>
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
