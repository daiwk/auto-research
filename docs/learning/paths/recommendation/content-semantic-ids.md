---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 语义表征、用户知识与冷启动

[搜广推](index.md) / 子主题导学 · 约 3 分钟 · 60 张论文卡

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

## 这个子主题的论文卡片

导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">
<div class="ar-learning-controls">
<label for="learning-search">搜索卡片
<input id="learning-search" type="search" data-learning-search placeholder="搜索论文、机制、机构或本地边界"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">共 60 张卡片</p>
<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Progressive Learning from Content to Relevance to Personalization for CTR Prediction 搜广推与 LLM 应用 Alibaba Group 2026-10-21 将内容直接压成一个语义ID会丢失局部视觉细节；只对 embedding 做相关性预训又不能给最终交互网络提供足够初始化。FineSID 用细粒度离散视觉/文本 token，先把完整共享预测器训成 query-item 语义相关性模型，再迁移到个性化 CTR。关键不是单独的 SID lookup，而是三个阶段之间保留同一交互骨干并迁移完整参数/状态。把随机 token 或简单加权器接到现有 CTR 模型，不能替代整篇论文。 因此本轮只完成论文、方法与线上证据收录，成本过高，不复现（审查 DONE）。完整训练使用64张 H20，每卡 batch4096、全局 batch262144。数据包含512亿曝光、2.51亿用户、2亿 query、4.18亿商品，以及4.53亿次测试曝光；相关性教师还依赖大规模专家标注/私有数据。  排序与长序列建模 预训练与参数高效迁移 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-finesid-1b73a633">Progressive Learning from Content to Relevance to Personalization for CTR Prediction</h2>
<p class="ar-learning-card__meta">Alibaba Group · 论文公开：2026-10-21</p>
<p><strong>方法要点：</strong>将内容直接压成一个语义ID会丢失局部视觉细节；只对 embedding 做相关性预训又不能给最终交互网络提供足够初始化。FineSID 用细粒度离散视觉/文本 token，先把完整共享预测器训成 query-item 语义相关性模型，再迁移到个性化 CTR。关键不是单独的 SID lookup，而是三个阶段之间保留同一交互骨干并迁移完整参数/状态。把随机 token 或简单加权器接到现有 CTR 模型，不能替代整篇论文。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>因此本轮只完成论文、方法与线上证据收录，成本过高，不复现（审查 DONE）。完整训练使用64张 H20，每卡 batch4096、全局 batch262144。数据包含512亿曝光、2.51亿用户、2亿 query、4.18亿商品，以及4.53亿次测试曝光；相关性教师还依赖大规模专家标注/私有数据。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.29138v1">原论文</a> · <a href="../../../../recommendation-components/2610.29138-finesid/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Don&#x27;t Rewrite the SID Map: Topology Preservation for Generative Retrieval in Dynamic E-Commerce Search 搜广推与 LLM 应用 Alibaba / Taobao &amp; Tmall Group 2026-10-19 生成式检索学习的是从查询到多级SID的解码路径，重新按业务价值排序旧商品会改变路径含义。论文把“映射更新”和“继续训练”拆开，发现大beam可以掩盖窄beam下的严重漂移；短预算warm-start也不能修复任意重映射。方法保留全部旧商品的三层SID，新商品先由外部RQ-VAE得到两层语义前缀，再按当前业务价值排名插入第三层。头部初始分配独占token，尾部采用固定容量共享桶；新商品插入头部时可以与原独占token碰撞，但不能顺移旧商品来强行消碰撞。 64卡完整训练和生产实验成本过高，不复现（审查 DONE）。已实现CPU映射组件，证据为L1机制诊断；已实现CPU映射组件，证据为L1机制诊断；不是RQ-VAE/LLM检索能力复现。64卡完整训练和生产实验成本过高，不复现（审查 DONE）。真实执行价值先验、初始HC分配、新商品插入、碰撞展开、旧路径漂移统计；用独立预期桶、插入顺序不变性、头部碰撞和全重映射负对照验收。frozen_old_path_address_recovery只是合成映射中旧地址仍能找回成员，不是推荐准确率、HitRate或模型成功率。没有量化器、语义编码器、beam-search模型或生产A/B，也未接入Evolve。  生成式推荐 语义标识与增量更新 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-sid-topology-a240bd6b">Don&#x27;t Rewrite the SID Map: Topology Preservation for Generative Retrieval in Dynamic E-Commerce Search</h2>
<p class="ar-learning-card__meta">Alibaba / Taobao &amp; Tmall Group · 论文公开：2026-10-19</p>
<p><strong>方法要点：</strong>生成式检索学习的是从查询到多级SID的解码路径，重新按业务价值排序旧商品会改变路径含义。论文把“映射更新”和“继续训练”拆开，发现大beam可以掩盖窄beam下的严重漂移；短预算warm-start也不能修复任意重映射。方法保留全部旧商品的三层SID，新商品先由外部RQ-VAE得到两层语义前缀，再按当前业务价值排名插入第三层。头部初始分配独占token，尾部采用固定容量共享桶；新商品插入头部时可以与原独占token碰撞，但不能顺移旧商品来强行消碰撞。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>64卡完整训练和生产实验成本过高，不复现（审查 DONE）。已实现CPU映射组件，证据为L1机制诊断；已实现CPU映射组件，证据为L1机制诊断；不是RQ-VAE/LLM检索能力复现。64卡完整训练和生产实验成本过高，不复现（审查 DONE）。真实执行价值先验、初始HC分配、新商品插入、碰撞展开、旧路径漂移统计；用独立预期桶、插入顺序不变性、头部碰撞和全重映射负对照验收。frozen_old_path_address_recovery只是合成映射中旧地址仍能找回成员，不是推荐准确率、HitRate或模型成功率。没有量化器、语义编码器、beam-search模型或生产A/B，也未接入Evolve。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.26105v1">原论文</a> · <a href="../../../../recommendation-components/2610.26105-sid-topology/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="AgentWebRec: Compact Evidence Fusion over the Agent Web for Personalized Recommendation 搜广推与 LLM 应用 Beihang University 2026-10-01 先从平台获取候选语义，再按语义相关性和时间衰减检索目标用户私有记忆；仅在本地证据置信度不足时查询邻居 Agent 的紧凑偏好模式。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。只执行有界检索与置信门控；不暴露私有记录，不运行 LLM Agent Web。只执行有界检索与置信门控；不暴露私有记录，不运行 LLM Agent Web。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  agent-recommendation private-memory evidence-fusion 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-agent-web-rec-883c9fbf">AgentWebRec: Compact Evidence Fusion over the Agent Web for Personalized Recommendation</h2>
<p class="ar-learning-card__meta">Beihang University · 论文公开：2026-10-01</p>
<p><strong>方法要点：</strong>先从平台获取候选语义，再按语义相关性和时间衰减检索目标用户私有记忆；仅在本地证据置信度不足时查询邻居 Agent 的紧凑偏好模式。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。只执行有界检索与置信门控；不暴露私有记录，不运行 LLM Agent Web。只执行有界检索与置信门控；不暴露私有记录，不运行 LLM Agent Web。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01705">原论文</a> · <a href="../../../../reproductions/2610.01705-agent-web-rec/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Neither Black nor White: Balancing Semantic and Collaborative Signals with Graph-Informed Semantic IDs (GrIS) 搜广推与 LLM 应用 Huawei Ireland Research Centre 2026-10-01 把 Semantic ID 构造重写为层级图划分：节点承载内容语义，边承载协同信号；图为空时退化为内容量化。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 graph-informed 层级二分 ID；用户批准为学术/Evolve 例外，无线上 A/B，不进入工业证据结论。收录例外：用户于 2026-10-02 明确批准的学术/Evolve 机制例外；论文没有量化线上 A/B，不进入工业证据结论。执行 graph-informed 层级二分 ID；用户批准为学术/Evolve 例外，无线上 A/B，不进入工业证据结论。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  generative-recommendation semantic-id graph-partition 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-gris-e106351a">Neither Black nor White: Balancing Semantic and Collaborative Signals with Graph-Informed Semantic IDs (GrIS)</h2>
<p class="ar-learning-card__meta">Huawei Ireland Research Centre · 论文公开：2026-10-01</p>
<p><strong>方法要点：</strong>把 Semantic ID 构造重写为层级图划分：节点承载内容语义，边承载协同信号；图为空时退化为内容量化。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 graph-informed 层级二分 ID；用户批准为学术/Evolve 例外，无线上 A/B，不进入工业证据结论。收录例外：用户于 2026-10-02 明确批准的学术/Evolve 机制例外；论文没有量化线上 A/B，不进入工业证据结论。执行 graph-informed 层级二分 ID；用户批准为学术/Evolve 例外，无线上 A/B，不进入工业证据结论。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01533">原论文</a> · <a href="../../../../reproductions/2610.01533-gris/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="KuaFu: Compressing Long User Behavior into Understanding at Billion Scale 搜广推与 LLM 应用 Tencent 2026-09-25 腾讯需要每周为海量用户刷新画像。逐条把原始行为文本送进大模型既慢又占空间；只截断长历史又容易遗漏时间、兴趣和因果信息。KuaFu 把单个行为条目作为最小压缩单位：压缩器对每条独立编码；投影器把 m 个高维记忆 token 降为 k 个低维缓存向量；解码器按用户行为顺序接收这些向量和任务提示。这样同一条目可以跨用户复用，不必因为某个用户新增行为而重算整个历史。原论文的Figure 1 和 Figure 2分别展示生产缓存链路及双轴投影结构；图片版权归原作者。 复现级别：公开数据概念验证，尚未复现论文效果。复现级别：公开数据概念验证，尚未复现论文效果。本地真实运行 Qwen3-4B-Instruct、独立条目压缩、双轴投影和三段监督训练；幻觉感知 DAPO 的代码已实现并在 A100 执行采样与打分，但固定公开样例同组奖励相同，更新被正确跳过。不能把该运行称作四阶段训练完成，更不能将 MRQA 指标等同于腾讯线上 GMV。本地对照口径：同解码器、同源 token 数的开头截断输入作为诊断基线，压缩缓存为实验组；dev F1 相对 -23.4%，但该输入消融不是独立训练的正式基线。  long-behavior item-compression hallucination-aware-rl 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-kuafu-25c887d3">KuaFu: Compressing Long User Behavior into Understanding at Billion Scale</h2>
<p class="ar-learning-card__meta">Tencent · 论文公开：2026-09-25</p>
<p><strong>方法要点：</strong>腾讯需要每周为海量用户刷新画像。逐条把原始行为文本送进大模型既慢又占空间；只截断长历史又容易遗漏时间、兴趣和因果信息。KuaFu 把单个行为条目作为最小压缩单位：压缩器对每条独立编码；投影器把 m 个高维记忆 token 降为 k 个低维缓存向量；解码器按用户行为顺序接收这些向量和任务提示。这样同一条目可以跨用户复用，不必因为某个用户新增行为而重算整个历史。原论文的Figure 1 和 Figure 2分别展示生产缓存链路及双轴投影结构；图片版权归原作者。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：公开数据概念验证，尚未复现论文效果。复现级别：公开数据概念验证，尚未复现论文效果。本地真实运行 Qwen3-4B-Instruct、独立条目压缩、双轴投影和三段监督训练；幻觉感知 DAPO 的代码已实现并在 A100 执行采样与打分，但固定公开样例同组奖励相同，更新被正确跳过。不能把该运行称作四阶段训练完成，更不能将 MRQA 指标等同于腾讯线上 GMV。本地对照口径：同解码器、同源 token 数的开头截断输入作为诊断基线，压缩缓存为实验组；dev F1 相对 -23.4%，但该输入消融不是独立训练的正式基线。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.31045">原论文</a> · <a href="../../../../reproductions/2609.31045-kuafu/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Explainable Recommendations at Scale: LLM Rationales for YouTube Music Artist Discovery 搜广推与 LLM 应用 Google 2026-09-20 用户愿意听熟悉的艺人，却可能不敢点开陌生艺人。论文将计算昂贵的 Gemini 推理移到异步离线阶段：根据完整的听歌历史生成“发现画像”，包含未听过的艺人和个性化理由；通过实体标准化与 LLM 评审过滤不可信理由；在线阶段只取缓存的画像，缺失时退回原有推荐。这样既能给候选附上解释，又避免在用户请求链路上运行大模型。论文的多臂 holdback 把新增提名与理由标注分开，发现理由是主导 shelf engagement 提升的因素。 复现级别：公开数据概念验证。复现级别：公开数据概念验证。本地使用真实 Qwen2.5-7B-Instruct 生成新艺人提名与自然语言理由，执行目录映射、已听过过滤、理由证据检查及只读缓存在线回退。Google 的 Gemini、私有音乐知识图谱、LLM-as-a-Judge 和线上多臂 A/B 不可公开复刻；公开 Last.fm 命中率不是用户信任或线上互动效果。本地确实运行 7B 权重推理、目录/新颖性/共享标签约束以及缓存/回退路径；但既未调用 Gemini，也未复刻 Google 的专有 KG 和线上 judge。本地对照口径：原 CF 基线 test Hit@5 0.40；  music-discovery llm-rationale offline-online-decoupling 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-music-rationales-61aa6d5c">Explainable Recommendations at Scale: LLM Rationales for YouTube Music Artist Discovery</h2>
<p class="ar-learning-card__meta">Google · 论文公开：2026-09-20</p>
<p><strong>方法要点：</strong>用户愿意听熟悉的艺人，却可能不敢点开陌生艺人。论文将计算昂贵的 Gemini 推理移到异步离线阶段：根据完整的听歌历史生成“发现画像”，包含未听过的艺人和个性化理由；通过实体标准化与 LLM 评审过滤不可信理由；在线阶段只取缓存的画像，缺失时退回原有推荐。这样既能给候选附上解释，又避免在用户请求链路上运行大模型。论文的多臂 holdback 把新增提名与理由标注分开，发现理由是主导 shelf engagement 提升的因素。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：公开数据概念验证。复现级别：公开数据概念验证。本地使用真实 Qwen2.5-7B-Instruct 生成新艺人提名与自然语言理由，执行目录映射、已听过过滤、理由证据检查及只读缓存在线回退。Google 的 Gemini、私有音乐知识图谱、LLM-as-a-Judge 和线上多臂 A/B 不可公开复刻；公开 Last.fm 命中率不是用户信任或线上互动效果。本地确实运行 7B 权重推理、目录/新颖性/共享标签约束以及缓存/回退路径；但既未调用 Gemini，也未复刻 Google 的专有 KG 和线上 judge。本地对照口径：原 CF 基线 test Hit@5 0.40；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.23877">原论文</a> · <a href="../../../../reproductions/2609.23877-music-rationales/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SIRF: A Spec-Internalized Risk Foundation Model for Industrial Content Risk Control 搜广推与 LLM 应用 Xiaohongshu 2026-09-10 SIRF 用 EntiGraph、MAGA 改写和账户级 CoT 合成长尾风控规则数据，通过 CPT 把复杂 trigger/exemption 规则写进模型权重，以单次 verdict 和可调阈值满足秒级线上判定。 复现级别：概念诊断。复现级别：概念诊断。执行规则关系合成、trigger/exemption 内化和 P95 阈值选择；线性模型替代 8B LLM CPT。没有私有账户数据、8B CPT、EntiGraph/MAGA 语言生成和线上 serving，因此本地结果不能验证论文业务提升。本地对照口径：同源线性特征为基线，加入规则交互项的实验组在三 seed 上 Black Recall@P95 相对提高 65.81%（绝对约 33.84 个百分点）；这不是论文 8B 模型或线上流量结果。  content-understanding risk-control foundation-model industrial-deployment 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-sirf-2c896048">SIRF: A Spec-Internalized Risk Foundation Model for Industrial Content Risk Control</h2>
<p class="ar-learning-card__meta">Xiaohongshu · 论文公开：2026-09-10</p>
<p><strong>方法要点：</strong>SIRF 用 EntiGraph、MAGA 改写和账户级 CoT 合成长尾风控规则数据，通过 CPT 把复杂 trigger/exemption 规则写进模型权重，以单次 verdict 和可调阈值满足秒级线上判定。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：概念诊断。复现级别：概念诊断。执行规则关系合成、trigger/exemption 内化和 P95 阈值选择；线性模型替代 8B LLM CPT。没有私有账户数据、8B CPT、EntiGraph/MAGA 语言生成和线上 serving，因此本地结果不能验证论文业务提升。本地对照口径：同源线性特征为基线，加入规则交互项的实验组在三 seed 上 Black Recall@P95 相对提高 65.81%（绝对约 33.84 个百分点）；这不是论文 8B 模型或线上流量结果。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11752">原论文</a> · <a href="../../../../reproductions/2609.11752-sirf/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="CAMIE: Co-Engagement-Aware Multimodal Item Embeddings for Snap Dynamic Product Ads Retrieval 搜广推与 LLM 应用 Snap Inc. 2026-08-31 CAMIE 用同一个 LLM/MLLM 接口编码图片和商品元数据，再从用户旅程挖掘共同互动商品对，以对称 in-batch InfoNCE 把“内容相近”校正为“行为上会共同转化”。同一 checkpoint 同时支持多模态和纯文本召回。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现内容向量、共同互动正对和对称检索打分。未包含私有 DPA 用户旅程、生产 MLLM checkpoint 与 ANN 服务；仅声明 CPU 核心机制。公开 MovieLens 的内容特征和共现 transition 代理共同互动，NDCG@10 为 0.05121（基线 0.05401）；负结果保留在 metrics/public-seeds42-44.json，不把小数据退化包装成提升。  multimodal-retrieval co-engagement advertising 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-camie-634faffd">CAMIE: Co-Engagement-Aware Multimodal Item Embeddings for Snap Dynamic Product Ads Retrieval</h2>
<p class="ar-learning-card__meta">Snap Inc. · 论文公开：2026-08-31</p>
<p><strong>方法要点：</strong>CAMIE 用同一个 LLM/MLLM 接口编码图片和商品元数据，再从用户旅程挖掘共同互动商品对，以对称 in-batch InfoNCE 把“内容相近”校正为“行为上会共同转化”。同一 checkpoint 同时支持多模态和纯文本召回。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现内容向量、共同互动正对和对称检索打分。未包含私有 DPA 用户旅程、生产 MLLM checkpoint 与 ANN 服务；仅声明 CPU 核心机制。公开 MovieLens 的内容特征和共现 transition 代理共同互动，NDCG@10 为 0.05121（基线 0.05401）；负结果保留在 metrics/public-seeds42-44.json，不把小数据退化包装成提升。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.30255">原论文</a> · <a href="../../../../reproductions/2608.30255-camie/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="From a Static Multi-Level Small Semantic Codebook to a Dynamic Single-Level Large Semantic Codebook for Generative Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-08-21 把多级小语义码本压缩为动态更新的单级大码本，再保留独立碰撞码；既减少自回归步数，也用曝光加权更新抵抗码本漂移。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation semantic-id serving-efficiency 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-dynamic-codebook-fbc8657c">From a Static Multi-Level Small Semantic Codebook to a Dynamic Single-Level Large Semantic Codebook for Generative Recommendation</h2>
<p class="ar-learning-card__meta">Kuaishou Technology · 论文公开：2026-08-21</p>
<p><strong>方法要点：</strong>把多级小语义码本压缩为动态更新的单级大码本，再保留独立碰撞码；既减少自回归步数，也用曝光加权更新抵抗码本漂移。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.21012">原论文</a> · <a href="../../../../reproductions/2608.21012-dynamic-codebook/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Multimedia Asset Personalization via Multimodal Embeddings at Netflix 搜广推与 LLM 应用 Netflix 2026-08-18 把冻结的 CLIP/MediaFM 多模态表示作为共享在线特征接入资产双塔，并以查询相似度增强搜索画布；离线 IPS 与 winner proxy 先筛选 checkpoint。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  multimodal-recommendation content-understanding cold-start 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-netflix-mediafm-31c991d9">Multimedia Asset Personalization via Multimodal Embeddings at Netflix</h2>
<p class="ar-learning-card__meta">Netflix · 论文公开：2026-08-18</p>
<p><strong>方法要点：</strong>把冻结的 CLIP/MediaFM 多模态表示作为共享在线特征接入资产双塔，并以查询相似度增强搜索画布；离线 IPS 与 winner proxy 先筛选 checkpoint。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.18322">原论文</a> · <a href="../../../../reproductions/2608.18322-netflix-mediafm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="ConnectionMind: A General Social-Personalized Recommendation System with LLM Reasoning 搜广推与 LLM 应用 Michigan State University 2026-08-10 传统社交推荐通常把好友关系压成静态 embedding，难以回答“某物品为什么经由哪条社交/兴趣路径被推荐”。ConnectionMind 把用户、物品和语义实体组成带关系类型、时间与权重的异构图；LLM policy 在任务相关子图内逐步扩展 frontier，同时输出推荐物品和对应证据路径。训练先从正反馈目标的最短路径做逐步 SFT，再用格式、最终推荐 F1 和最短路径 shaping 三类规则奖励做端到端 GRPO。 Fidelity：核心机制复现。使用论文同款 Delicious 公开数据，实际执行异构图构建、最短正路径 SFT、规则奖励 GRPO、学生蒸馏和重用户混合推理；本地负结果如实保留。没有复刻 Meta 私有视频图、Llama-3.1 3B/8B、生产级 GNN 和 serving；本地结果只验证完整算法路径，不代表复现论文线上增益。本地对照口径：基线为同一 Delicious 图、切分与候选集上的固定异构图聚合；实验组为 SFT+GRPO 路径 policy、蒸馏 student 与 10% 重用户混合推理，相对 NDCG@10 -7.44%。  social-recommendation llm-recommendation graph-reasoning reinforcement-learning distillation 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-connectionmind-47def159">ConnectionMind: A General Social-Personalized Recommendation System with LLM Reasoning</h2>
<p class="ar-learning-card__meta">Michigan State University · 论文公开：2026-08-10</p>
<p><strong>方法要点：</strong>传统社交推荐通常把好友关系压成静态 embedding，难以回答“某物品为什么经由哪条社交/兴趣路径被推荐”。ConnectionMind 把用户、物品和语义实体组成带关系类型、时间与权重的异构图；LLM policy 在任务相关子图内逐步扩展 frontier，同时输出推荐物品和对应证据路径。训练先从正反馈目标的最短路径做逐步 SFT，再用格式、最终推荐 F1 和最短路径 shaping 三类规则奖励做端到端 GRPO。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity：核心机制复现。使用论文同款 Delicious 公开数据，实际执行异构图构建、最短正路径 SFT、规则奖励 GRPO、学生蒸馏和重用户混合推理；本地负结果如实保留。没有复刻 Meta 私有视频图、Llama-3.1 3B/8B、生产级 GNN 和 serving；本地结果只验证完整算法路径，不代表复现论文线上增益。本地对照口径：基线为同一 Delicious 图、切分与候选集上的固定异构图聚合；实验组为 SFT+GRPO 路径 policy、蒸馏 student 与 10% 重用户混合推理，相对 NDCG@10 -7.44%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.10187">原论文</a> · <a href="../../../../reproductions/2608.10187-connectionmind/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Douyin Multimodal Embedding Model Technical Report 搜广推与 LLM 应用 ByteDance / Douyin 2026-08-03 对比学习向量服务高效但监督过粗，显式 CoT 又无法在线服务。DME 先做大规模多模态对比预训练，再以 Evidence-Grounded Typed Latent Reasoning 整理检索证据，并用 Cross-Conditional Reconstruction 保留对侧细粒度语义；两个生成头只在训练期使用。 Fidelity：核心机制复现。公开数据只验证论文机制，不模拟生产流量。未复刻 2B/9B 多模态 backbone、抖音私有语料和十亿级向量索引。本地对照口径：基线为共享 transition + content scorer，实验组只加入 DME 核心机制；相对 NDCG@10 -8.84%。  content-understanding multimodal-retrieval embedding llm-recommendation 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-dme-01722658">Douyin Multimodal Embedding Model Technical Report</h2>
<p class="ar-learning-card__meta">ByteDance / Douyin · 论文公开：2026-08-03</p>
<p><strong>方法要点：</strong>对比学习向量服务高效但监督过粗，显式 CoT 又无法在线服务。DME 先做大规模多模态对比预训练，再以 Evidence-Grounded Typed Latent Reasoning 整理检索证据，并用 Cross-Conditional Reconstruction 保留对侧细粒度语义；两个生成头只在训练期使用。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity：核心机制复现。公开数据只验证论文机制，不模拟生产流量。未复刻 2B/9B 多模态 backbone、抖音私有语料和十亿级向量索引。本地对照口径：基线为共享 transition + content scorer，实验组只加入 DME 核心机制；相对 NDCG@10 -8.84%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.02148">原论文</a> · <a href="../../../../reproductions/2608.02148-dme/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Knowledge–Geometry Decoupling: Refreshable Pretrained Transfer for Streaming Recommendation 搜广推与 LLM 应用 Xiamen University / Shopee 2026-08-03 主题：流式推荐预训练与迁移。相邻点击并不总是有效依赖。KGD 用 BMTP 筛出协同或语义相关的未来物品；迁移时冻结可刷新知识编码器，用只读 cross-attention 读取知识，并以与锚点正交的 ACR 写入任务几何。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。MovieLens-1M 上比较相邻 NTP 与 BMTP+冻结知识+正交 ACR，执行全库排序。  sequential-recommendation pretraining streaming transfer 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-kgd-b25439a8">Knowledge–Geometry Decoupling: Refreshable Pretrained Transfer for Streaming Recommendation</h2>
<p class="ar-learning-card__meta">Xiamen University / Shopee · 论文公开：2026-08-03</p>
<p><strong>方法要点：</strong>主题：流式推荐预训练与迁移。相邻点击并不总是有效依赖。KGD 用 BMTP 筛出协同或语义相关的未来物品；迁移时冻结可刷新知识编码器，用只读 cross-attention 读取知识，并以与锚点正交的 ACR 写入任务几何。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。MovieLens-1M 上比较相邻 NTP 与 BMTP+冻结知识+正交 ACR，执行全库排序。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.02738">原论文</a> · <a href="../../../../reproductions/2608.02738-kgd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="GALA: Generative Aligned Learning for Adaptive Multimodal Representation in the Taobao Shangou Recommender System 搜广推与 LLM 应用 Rajax Network Technology / Taobao Shangou / Alibaba 2026-07-31 先在 query-image-text 三元组上预训练多模态表示，再以行为奖励做 GRPO 对齐，最后用自适应门控融合多模态与 ID 表示。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  multimodal-recommendation representation-alignment reinforcement-learning 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-gala-83e5be9a">GALA: Generative Aligned Learning for Adaptive Multimodal Representation in the Taobao Shangou Recommender System</h2>
<p class="ar-learning-card__meta">Rajax Network Technology / Taobao Shangou / Alibaba · 论文公开：2026-07-31</p>
<p><strong>方法要点：</strong>先在 query-image-text 三元组上预训练多模态表示，再以行为奖励做 GRPO 对齐，最后用自适应门控融合多模态与 ID 表示。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.29213">原论文</a> · <a href="../../../../reproductions/2607.29213-gala/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Building a User Foundation Model for the Open Web 搜广推与 LLM 应用 Teads 2026-07-30 开放网络 RTB 的用户身份不连续、历史短且受隐私选择影响。论文以 MLM 与序列级对比学习预训练浏览历史 Transformer，再向 CTR、赢标率等任务输出统一用户表示；训练配方由可审计 lifter 组成的 LLM-in-the-loop 搜索改进。 Fidelity: 核心机制复现。实现共享序列 encoder、双视图对比预训练和下游微调。未包含 Teads RTB 私有特征、Claude Opus lifter 搜索及生产 GDCN adapter。本地对照口径：基线与实验组使用同一 encoder、数据和 45 steps；实验组加入双视图预训练，相对基线 NDCG@10 +0.00%。  advertising user-foundation-model self-supervised-learning llm-optimizer 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-open-web-ufm-467147f2">Building a User Foundation Model for the Open Web</h2>
<p class="ar-learning-card__meta">Teads · 论文公开：2026-07-30</p>
<p><strong>方法要点：</strong>开放网络 RTB 的用户身份不连续、历史短且受隐私选择影响。论文以 MLM 与序列级对比学习预训练浏览历史 Transformer，再向 CTR、赢标率等任务输出统一用户表示；训练配方由可审计 lifter 组成的 LLM-in-the-loop 搜索改进。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。实现共享序列 encoder、双视图对比预训练和下游微调。未包含 Teads RTB 私有特征、Claude Opus lifter 搜索及生产 GDCN adapter。本地对照口径：基线与实验组使用同一 encoder、数据和 45 steps；实验组加入双视图预训练，相对基线 NDCG@10 +0.00%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28019">原论文</a> · <a href="../../../../reproductions/2607.28019-open-web-ufm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RecoReward: Recommender-Guided Multimodal Description Generation for Recommendation 搜广推与 LLM 应用 Kuaishou / Nankai University / Chinese Academy of Sciences 2026-07-28 冻结双塔推荐器，以目标用户与非目标用户的亲和力差作为奖励训练内容描述；线上 serving 只消费描述，不依赖用户画像。 Fidelity: 核心机制复现。本地执行推荐奖励目标与公开数据对照，不声称复刻生产 reward pipeline。没有微调 Qwen3.5-9B，也没有直播视频和快手私有行为；本地结果只验证 RAS 奖励可执行。本地对照口径：基线为 content-only semantic recall，实验组为 RAS 选择；Hit@10 -16.00%、NDCG@10 -9.68%，head share -24.14%（负结果）。  llm-recommendation multimodal reinforcement-learning retrieval 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-reco-reward-d01ebaa7">RecoReward: Recommender-Guided Multimodal Description Generation for Recommendation</h2>
<p class="ar-learning-card__meta">Kuaishou / Nankai University / Chinese Academy of Sciences · 论文公开：2026-07-28</p>
<p><strong>方法要点：</strong>冻结双塔推荐器，以目标用户与非目标用户的亲和力差作为奖励训练内容描述；线上 serving 只消费描述，不依赖用户画像。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地执行推荐奖励目标与公开数据对照，不声称复刻生产 reward pipeline。没有微调 Qwen3.5-9B，也没有直播视频和快手私有行为；本地结果只验证 RAS 奖励可执行。本地对照口径：基线为 content-only semantic recall，实验组为 RAS 选择；Hit@10 -16.00%、NDCG@10 -9.68%，head share -24.14%（负结果）。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25901">原论文</a> · <a href="../../../../reproductions/2607.25901-reco-reward/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Mosaic: A Fleet of User Embedding Specialists for Recommendation at Meta 搜广推与 LLM 应用 Meta 2026-07-27 单个通用 user embedding 很难同时覆盖长期记忆、稠密特征、长序列兴趣和特定下游任务。Mosaic 把用户表征组织成可独立演进的 specialist fleet：memorization-driven、dense-heavy、sequential HSTU+MoE 和与下游任务联合训练的 CoTrain。下游排序器按需消费多个 embedding，而不是让一个网络承担所有目标。随着 fleet 增大，新 embedding 容易复制旧 embedding 的信息。 Fidelity: 核心机制复现。实际训练四类 specialist、MRM 复合任务和 cosine redundancy loss；缩小数据、序列长度和 serving 链路。MovieLens genre/popularity 代理 Meta 的多表面私有行为标签；本地 sequential specialist 是 GRU 而非 2048-token HSTU，CoTrain 也缩为小型 routed MoE。未复刻跨产品特征、CoEval、User Tower Zero-Out、AOTI、memcache 和线上混合 CPU/GPU serving，不能把本地 +3.49% 与论文线上 lift 直接比较。  user-embedding multi-task-learning sequential-recommendation mixture-of-experts 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-mosaic-eb607f0f">Mosaic: A Fleet of User Embedding Specialists for Recommendation at Meta</h2>
<p class="ar-learning-card__meta">Meta · 论文公开：2026-07-27</p>
<p><strong>方法要点：</strong>单个通用 user embedding 很难同时覆盖长期记忆、稠密特征、长序列兴趣和特定下游任务。Mosaic 把用户表征组织成可独立演进的 specialist fleet：memorization-driven、dense-heavy、sequential HSTU+MoE 和与下游任务联合训练的 CoTrain。下游排序器按需消费多个 embedding，而不是让一个网络承担所有目标。随着 fleet 增大，新 embedding 容易复制旧 embedding 的信息。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。实际训练四类 specialist、MRM 复合任务和 cosine redundancy loss；缩小数据、序列长度和 serving 链路。MovieLens genre/popularity 代理 Meta 的多表面私有行为标签；本地 sequential specialist 是 GRU 而非 2048-token HSTU，CoTrain 也缩为小型 routed MoE。未复刻跨产品特征、CoEval、User Tower Zero-Out、AOTI、memcache 和线上混合 CPU/GPU serving，不能把本地 +3.49% 与论文线上 lift 直接比较。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24015">原论文</a> · <a href="../../../../reproductions/2607.24015-mosaic/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Tokens are All You Need: Dual-purpose Semantic IDs for Achieving LLM-Level I/O Efficiency in Recommendation Systems 搜广推与 LLM 应用 Google DeepMind / YouTube 2026-07-26 传统 SID 擅长表达协同身份，却仍需把大规模内容 embedding 输入推荐模型。论文以层次量化生成 SID，并加入 Semantic Decoder（SiDec）从 SID 重建内容表示，让同一串 token 同时支持生成式检索、排序和低 I/O 的在线 embedding reconstruction。 Fidelity: 核心机制复现。本地训练分层 SID、SID 转移与 Semantic Decoder 内容重建，并用于检索评分。genre 替代 YouTube 多模态内容；未复刻超大 codebook、线上 embedding reconstruction 和私有日志。本地对照口径：基线为同切分的 dense transition-content retrieval，实验组加入 Dual-purpose SID 与 SiDec；NDCG@10 相对 -12.40%。  semantic-id retrieval ranking content-understanding serving 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-dual-sid-924ced9f">Tokens are All You Need: Dual-purpose Semantic IDs for Achieving LLM-Level I/O Efficiency in Recommendation Systems</h2>
<p class="ar-learning-card__meta">Google DeepMind / YouTube · 论文公开：2026-07-26</p>
<p><strong>方法要点：</strong>传统 SID 擅长表达协同身份，却仍需把大规模内容 embedding 输入推荐模型。论文以层次量化生成 SID，并加入 Semantic Decoder（SiDec）从 SID 重建内容表示，让同一串 token 同时支持生成式检索、排序和低 I/O 的在线 embedding reconstruction。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地训练分层 SID、SID 转移与 Semantic Decoder 内容重建，并用于检索评分。genre 替代 YouTube 多模态内容；未复刻超大 codebook、线上 embedding reconstruction 和私有日志。本地对照口径：基线为同切分的 dense transition-content retrieval，实验组加入 Dual-purpose SID 与 SiDec；NDCG@10 相对 -12.40%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24865">原论文</a> · <a href="../../../../reproductions/2607.24865-dual-sid/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Pin-SCALE: Semantic Cascading and Alignment Learning for Engagement-Aware IDs in Cold-Start Recommendations 搜广推与 LLM 应用 Pinterest 2026-07-19 Semantic ID 擅长冷启动，但在判别式 dense retrieval 中缺乏系统接入方案。Pin-SCALE 保留 residual hierarchy 做 cascading pooling，以 engagement-aware tokenization 引入协同信号，再用 query-item 与 item-item 多视角对比学习对齐 SID 和参与度预测。 Fidelity: 核心机制复现。执行 engagement-aware residual codebook 和 SID 级联相似度。SIGIR program 是当前可核验原始入口；没有伪造 arXiv ID。公开 popularity/transition 仅代理 Pinterest engagement。本地对照口径：基线是 unweighted semantic/content ranker；实验组使用 engagement-weighted 三层 SID，NDCG@10 0.03540→0.04022，相对 +13.61%，fresh Hit@10 相对 +50.00%。  semantic-id engagement-aware generative-retrieval 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-pin-scale-f40ee8a5">Pin-SCALE: Semantic Cascading and Alignment Learning for Engagement-Aware IDs in Cold-Start Recommendations</h2>
<p class="ar-learning-card__meta">Pinterest · 论文公开：2026-07-19</p>
<p><strong>方法要点：</strong>Semantic ID 擅长冷启动，但在判别式 dense retrieval 中缺乏系统接入方案。Pin-SCALE 保留 residual hierarchy 做 cascading pooling，以 engagement-aware tokenization 引入协同信号，再用 query-item 与 item-item 多视角对比学习对齐 SID 和参与度预测。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。执行 engagement-aware residual codebook 和 SID 级联相似度。SIGIR program 是当前可核验原始入口；没有伪造 arXiv ID。公开 popularity/transition 仅代理 Pinterest engagement。本地对照口径：基线是 unweighted semantic/content ranker；实验组使用 engagement-weighted 三层 SID，NDCG@10 0.03540→0.04022，相对 +13.61%，fresh Hit@10 相对 +50.00%。</p></details>
<p class="ar-learning-card__links"><a href="https://sigir2026.org/SIGIR2026_program.pdf">原论文</a> · <a href="../../../../reproductions/sigir2026-pin-scale-pin-scale/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RECAP: Feedback-Driven Streaming Semantic User Profiles for Short-Video Recommendation 搜广推与 LLM 应用 Kuaishou Technology / USTC 2026-07-17 传统 LLM 用户画像只追求“总结得像”，没有直接优化未来推荐。RECAP 把画像变成带容量约束的结构化流式状态：LLM 负责语义 update，确定性逻辑负责生命周期、合并与淘汰；再用 LLM judge 筛出标签一致的行为 pair，训练双塔 evaluator，把匹配分数作为 GRPO reward 闭环更新画像生成器。 Fidelity: 核心机制复现。真实训练 causal Transformer updater、双塔评价器和 clipped GRPO，并执行固定容量画像状态机。自然语言画像和工业 LLM 缩为 category-token causal Transformer；没有快手私有日志、生产 LLM judge 和在线闭环。核心 SFT→evaluator→GRPO→bounded state 链路实际执行，但不声称复现线上收益。本地对照口径：基线是 open-loop SFT 流式画像；实验组增加反馈 evaluator 与 GRPO，NDCG@10 相对 -6.77%。  llm-recommendation semantic-profile grpo 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-recap-84f36c5b">RECAP: Feedback-Driven Streaming Semantic User Profiles for Short-Video Recommendation</h2>
<p class="ar-learning-card__meta">Kuaishou Technology / USTC · 论文公开：2026-07-17</p>
<p><strong>方法要点：</strong>传统 LLM 用户画像只追求“总结得像”，没有直接优化未来推荐。RECAP 把画像变成带容量约束的结构化流式状态：LLM 负责语义 update，确定性逻辑负责生命周期、合并与淘汰；再用 LLM judge 筛出标签一致的行为 pair，训练双塔 evaluator，把匹配分数作为 GRPO reward 闭环更新画像生成器。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。真实训练 causal Transformer updater、双塔评价器和 clipped GRPO，并执行固定容量画像状态机。自然语言画像和工业 LLM 缩为 category-token causal Transformer；没有快手私有日志、生产 LLM judge 和在线闭环。核心 SFT→evaluator→GRPO→bounded state 链路实际执行，但不声称复现线上收益。本地对照口径：基线是 open-loop SFT 流式画像；实验组增加反馈 evaluator 与 GRPO，NDCG@10 相对 -6.77%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.15730">原论文</a> · <a href="../../../../reproductions/2607.15730-recap/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Proximity Features: Privacy-Compliant Cold-Start Personalization at Airbnb 搜广推与 LLM 应用 Airbnb 2026-07-14 匿名用户没有 user ID。Airbnb 把 consented geo-IP population-center 坐标聚成约 1,000 用户的 proximity key：密集位置用 IP hash 细分，稀疏位置逐级降低地理精度合并；群体行为按稳定 key 每日聚合，线上无需持久个人标识。 Fidelity: 核心机制复现。dense hash refinement、sparse fine-to-coarse clustering、稳定 proximity key、群体聚合与冷启动 scoring 均实际执行。ZIP prefix 不是 geo-IP 坐标；阈值缩为 12，只验证算法，不构成论文约 1,000 用户的隐私保证。本地对照口径：基线是 global cold-start aggregate；实验组用 MovieLens ZIP 的 adaptive proximity aggregate，验证集选择 blend 1.0，相对基线 Hit@10 +16.67%、NDCG@10 +22.91%。  cold-start privacy features 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-proximity-features-c055e9e4">Proximity Features: Privacy-Compliant Cold-Start Personalization at Airbnb</h2>
<p class="ar-learning-card__meta">Airbnb · 论文公开：2026-07-14</p>
<p><strong>方法要点：</strong>匿名用户没有 user ID。Airbnb 把 consented geo-IP population-center 坐标聚成约 1,000 用户的 proximity key：密集位置用 IP hash 细分，稀疏位置逐级降低地理精度合并；群体行为按稳定 key 每日聚合，线上无需持久个人标识。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。dense hash refinement、sparse fine-to-coarse clustering、稳定 proximity key、群体聚合与冷启动 scoring 均实际执行。ZIP prefix 不是 geo-IP 坐标；阈值缩为 12，只验证算法，不构成论文约 1,000 用户的隐私保证。本地对照口径：基线是 global cold-start aggregate；实验组用 MovieLens ZIP 的 adaptive proximity aggregate，验证集选择 blend 1.0，相对基线 Hit@10 +16.67%、NDCG@10 +22.91%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12246">原论文</a> · <a href="../../../../reproductions/2607.12246-proximity-features/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="TokenMinds: Pretrained User Tokens and Embeddings for User Understanding in Large Recommender Systems 搜广推与 LLM 应用 Google DeepMind / YouTube 2026-06-23 传统工业用户建模把完整兴趣压入少量稠密向量，容易损失细粒度、多峰兴趣；直接让 LLM 输出文本画像又难以与非文本 item ID 和下游排序模型对齐。TokenMinds 将 PLUM 的 item Semantic ID（SID）体系扩展到用户侧：encoder 读取视频 SID、观看特征和搜索文本并输出稠密用户向量，decoder 则自回归生成若干代表未来兴趣的 SID 用户 token。下游同时使用两种表示，从而保留现有 dense feature 兼容性并引入离散、可落到内容语义空间的兴趣表示。 Fidelity: 核心机制复现。本地实际训练共享序列编码器、稠密用户向量、分层 SID 用户 token 预测头及下游融合排序；Google 的 Gemini MoE、YouTube 私有数据和异步生产服务不在本地冒充复刻。本地训练了论文中心的 dual-output 路径，而不是只把配置命名为 TokenMinds。MovieLens genre 取代 YouTube 多模态内容，320 users / 480 items 与 32 条历史取代数十亿用户、1,200 watches 和搜索序列；  llm-recommendation user-modeling semantic-id cross-scenario ranking serving 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-tokenminds-03a3a530">TokenMinds: Pretrained User Tokens and Embeddings for User Understanding in Large Recommender Systems</h2>
<p class="ar-learning-card__meta">Google DeepMind / YouTube · 论文公开：2026-06-23</p>
<p><strong>方法要点：</strong>传统工业用户建模把完整兴趣压入少量稠密向量，容易损失细粒度、多峰兴趣；直接让 LLM 输出文本画像又难以与非文本 item ID 和下游排序模型对齐。TokenMinds 将 PLUM 的 item Semantic ID（SID）体系扩展到用户侧：encoder 读取视频 SID、观看特征和搜索文本并输出稠密用户向量，decoder 则自回归生成若干代表未来兴趣的 SID 用户 token。下游同时使用两种表示，从而保留现有 dense feature 兼容性并引入离散、可落到内容语义空间的兴趣表示。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地实际训练共享序列编码器、稠密用户向量、分层 SID 用户 token 预测头及下游融合排序；Google 的 Gemini MoE、YouTube 私有数据和异步生产服务不在本地冒充复刻。本地训练了论文中心的 dual-output 路径，而不是只把配置命名为 TokenMinds。MovieLens genre 取代 YouTube 多模态内容，320 users / 480 items 与 32 条历史取代数十亿用户、1,200 watches 和搜索序列；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.25147">原论文</a> · <a href="../../../../reproductions/2606.25147-tokenminds/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Structuring and Tokenizing Distributed User Interest Context for Generative Recommendation 搜广推与 LLM 应用 Meta 2026-06-18 生成式推荐把 item 当 token，但纯 item 序列难以表达一个物品跨多个兴趣簇的语义，也难以利用分散在不同用户行为中的共现结构。G2Rec 从全站 co-engagement 构造 item-item 图，以可微 soft modularity 学习一个 item 对多个 interest prototype 的软归属，再把 item token 与其 interest-profile token 交替输入生成模型，并增加 profile prediction loss。 Fidelity: 完整核心链路复现。当前代码实际优化稀疏图 soft modularity，并训练交替 item/continuous-interest token 的自回归 Transformer、next-item loss 与 profile loss。本地对照口径：基线是参数级别匹配的 Item-only Autoregressive Decoder；实验组是 G2Rec Item+Interest Decoder；NDCG@10 从 0.0474 升至 0.0530（+11.92%）。这是 interest-token 组织与辅助目标的联合消融，不是相对 DIN。   搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-g2rec-310e6cb6">Structuring and Tokenizing Distributed User Interest Context for Generative Recommendation</h2>
<p class="ar-learning-card__meta">Meta · 论文公开：2026-06-18</p>
<p><strong>方法要点：</strong>生成式推荐把 item 当 token，但纯 item 序列难以表达一个物品跨多个兴趣簇的语义，也难以利用分散在不同用户行为中的共现结构。G2Rec 从全站 co-engagement 构造 item-item 图，以可微 soft modularity 学习一个 item 对多个 interest prototype 的软归属，再把 item token 与其 interest-profile token 交替输入生成模型，并增加 profile prediction loss。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 完整核心链路复现。当前代码实际优化稀疏图 soft modularity，并训练交替 item/continuous-interest token 的自回归 Transformer、next-item loss 与 profile loss。本地对照口径：基线是参数级别匹配的 Item-only Autoregressive Decoder；实验组是 G2Rec Item+Interest Decoder；NDCG@10 从 0.0474 升至 0.0530（+11.92%）。这是 interest-token 组织与辅助目标的联合消融，不是相对 DIN。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.20554">原论文</a> · <a href="../../../../reproductions/2606.20554-g2rec/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Atomic Intent Reasoning: Bringing LLM Semantics to Industrial Cross-Domain Recommendations 搜广推与 LLM 应用 The Hong Kong Polytechnic University 2026-06-09 将昂贵的 LLM 推理移至离线，把单次行为转成可缓存的层级原子意图；在线按目标商品检索意图链，并用多头注意力聚合跨域证据。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05240，相对变化 -2.98%。本地代理目标与论文生产任务不同，不能外推线上 lift。  cross-domain llm-recommendation intent-retrieval 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-atomic-intent-04e8fc99">Atomic Intent Reasoning: Bringing LLM Semantics to Industrial Cross-Domain Recommendations</h2>
<p class="ar-learning-card__meta">The Hong Kong Polytechnic University · 论文公开：2026-06-09</p>
<p><strong>方法要点：</strong>将昂贵的 LLM 推理移至离线，把单次行为转成可缓存的层级原子意图；在线按目标商品检索意图链，并用多头注意力聚合跨域证据。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05240，相对变化 -2.98%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.10357">原论文</a> · <a href="../../../../reproductions/2606.10357-atomic-intent/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SSRLive: Live Streaming Recommendation with Dynamic Semantic ID 搜广推与 LLM 应用 Taobao &amp; Tmall Group, Alibaba 2026-06-05 用静态语义 ID 表达主播长期内容，用动态语义 ID 捕获实时直播状态，再融合用户—主播交互特征完成观看、交易与互动多任务预测。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05351，相对变化 -0.92%。本地代理目标与论文生产任务不同，不能外推线上 lift。  live-streaming semantic-id multitask-ranking 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-ssrlive-efb93285">SSRLive: Live Streaming Recommendation with Dynamic Semantic ID</h2>
<p class="ar-learning-card__meta">Taobao &amp; Tmall Group, Alibaba · 论文公开：2026-06-05</p>
<p><strong>方法要点：</strong>用静态语义 ID 表达主播长期内容，用动态语义 ID 捕获实时直播状态，再融合用户—主播交互特征完成观看、交易与互动多任务预测。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05351，相对变化 -0.92%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.06970">原论文</a> · <a href="../../../../reproductions/2606.06970-ssrlive/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Fine-Tuned LLM as a Complementary Predictor Improving Ads System 搜广推与 LLM 应用 Pinterest 2026-05-27 论文没有让 LLM 替换广告召回或排序，而是把它作为 ancillary predictor：输入用户画像、历史转化、搜索、URL、品类和品牌，预测下一批高转化意图 advertiser 与兴趣。预测结果一方面成为 advertiser 定向的补充召回通道，另一方面作为 ctcvr/vtcvr 特征进入后续排序。训练分三层：先用单一 next-advertiser 标签做 SFT；再用 GRPO 生成 20 个 advertiser 与 5 个兴趣，并用命中位置和严格输出长度计算 reward； 未运行 Pinterest 私有 PinCLIP SID 三阶段 CPT，也不声称本地 AUC/Recall 可外推 RoAS。Fidelity: 完整核心链路。本地实际执行开源 causal LLM 的 LoRA SFT、论文位置/格式 reward 驱动的 clipped GRPO、受约束 advertiser 解码、训练式 two-tower、validation 配额选择的补充召回，以及 LLM advertiser score 作为排序特征。Pinterest 私有广告与跨站转化数据由公开商品品牌和购买序列替换。使用真实预训练语言模型和可训练 LoRA，不是规则或 embedding 打分替代 SFT/GRPO。  advertising llm-sft grpo candidate-generation 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-pinterest-ads-llm-d99be125">Fine-Tuned LLM as a Complementary Predictor Improving Ads System</h2>
<p class="ar-learning-card__meta">Pinterest · 论文公开：2026-05-27</p>
<p><strong>方法要点：</strong>论文没有让 LLM 替换广告召回或排序，而是把它作为 ancillary predictor：输入用户画像、历史转化、搜索、URL、品类和品牌，预测下一批高转化意图 advertiser 与兴趣。预测结果一方面成为 advertiser 定向的补充召回通道，另一方面作为 ctcvr/vtcvr 特征进入后续排序。训练分三层：先用单一 next-advertiser 标签做 SFT；再用 GRPO 生成 20 个 advertiser 与 5 个兴趣，并用命中位置和严格输出长度计算 reward；</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>未运行 Pinterest 私有 PinCLIP SID 三阶段 CPT，也不声称本地 AUC/Recall 可外推 RoAS。Fidelity: 完整核心链路。本地实际执行开源 causal LLM 的 LoRA SFT、论文位置/格式 reward 驱动的 clipped GRPO、受约束 advertiser 解码、训练式 two-tower、validation 配额选择的补充召回，以及 LLM advertiser score 作为排序特征。Pinterest 私有广告与跨站转化数据由公开商品品牌和购买序列替换。使用真实预训练语言模型和可训练 LoRA，不是规则或 embedding 打分替代 SFT/GRPO。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.27856">原论文</a> · <a href="../../../../reproductions/2605.27856-pinterest-ads-llm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="L2Rec: Towards Dual-View Understanding of LLMs for Personalized Recommendation 搜广推与 LLM 应用 NetEase Cloud Music 2026-05-26 共享 LLM 中插入按用户路由的双视图 LoRA-MoE，分别适配语义视图和行为视图，再由自适应跨视图门控融合。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  llm-recommendation parameter-efficient-tuning multi-view 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-l2rec-4fe523da">L2Rec: Towards Dual-View Understanding of LLMs for Personalized Recommendation</h2>
<p class="ar-learning-card__meta">NetEase Cloud Music · 论文公开：2026-05-26</p>
<p><strong>方法要点：</strong>共享 LLM 中插入按用户路由的双视图 LoRA-MoE，分别适配语义视图和行为视图，再由自适应跨视图门控融合。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.26717">原论文</a> · <a href="../../../../reproductions/2605.26717-l2rec/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="MuChator: Enabling Active Music Discovery via Conversational Music LLMs in Douyin Music 搜广推与 LLM 应用 ByteDance 2026-05-26 围绕音乐领域继续预训练、SFT 与强化学习，让对话模型从用户即时表达中解析音乐意图，并主动探索而非只复述历史偏好。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04477，相对变化 -17.09%。本地代理目标与论文生产任务不同，不能外推线上 lift。  music-recommendation conversational-llm active-discovery 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-muchator-f63c99f7">MuChator: Enabling Active Music Discovery via Conversational Music LLMs in Douyin Music</h2>
<p class="ar-learning-card__meta">ByteDance · 论文公开：2026-05-26</p>
<p><strong>方法要点：</strong>围绕音乐领域继续预训练、SFT 与强化学习，让对话模型从用户即时表达中解析音乐意图，并主动探索而非只复述历史偏好。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04477，相对变化 -17.09%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.27103">原论文</a> · <a href="../../../../reproductions/2605.27103-muchator/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="From Head to Tail: Asymmetric Knowledge Transfer in Long-tail Recommendation with Generative Semantic IDs 搜广推与 LLM 应用 Alibaba Group / Peking University 2026-05-22 工业推荐的用户与物品都呈强长尾分布。直接共享表示可能把尾部稀疏且噪声较大的信号反向传给头部，普通对称对比学习因此不一定安全。AKT-Rec 先用 MLLM 对齐内容和协同信号，再用 RQ-VAE 把用户、物品量化成层级 Semantic ID，以同一高层 ID 定义语义簇。排序阶段为每个 ID 同时学习 cluster view 和 individual view。非对称 InfoNCE 对 tail→head 方向赋更大权重，并在作为 teacher 的一侧 stop-gradient； Fidelity: 核心机制复现。本地对真实 SmolLM2-135M 注入 LoRA，实际执行物品共现对比微调、用户兴趣/类别监督、残差 Semantic ID、cluster/individual 双视图、head-to-tail 非对称 stop-gradient、正交约束与两级活动度门控。真实训练开源 causal LM 的 LoRA，并分别执行物品协同对齐和用户监督；没有用哈希或静态文本向量替代这两步。本地对照口径：基线是只使用 individual embedding 和实例级 target attention 的 online_base；  llm-recommendation semantic-id long-tail ctr-ranking 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-akt-rec-be638f5f">From Head to Tail: Asymmetric Knowledge Transfer in Long-tail Recommendation with Generative Semantic IDs</h2>
<p class="ar-learning-card__meta">Alibaba Group / Peking University · 论文公开：2026-05-22</p>
<p><strong>方法要点：</strong>工业推荐的用户与物品都呈强长尾分布。直接共享表示可能把尾部稀疏且噪声较大的信号反向传给头部，普通对称对比学习因此不一定安全。AKT-Rec 先用 MLLM 对齐内容和协同信号，再用 RQ-VAE 把用户、物品量化成层级 Semantic ID，以同一高层 ID 定义语义簇。排序阶段为每个 ID 同时学习 cluster view 和 individual view。非对称 InfoNCE 对 tail→head 方向赋更大权重，并在作为 teacher 的一侧 stop-gradient；</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地对真实 SmolLM2-135M 注入 LoRA，实际执行物品共现对比微调、用户兴趣/类别监督、残差 Semantic ID、cluster/individual 双视图、head-to-tail 非对称 stop-gradient、正交约束与两级活动度门控。真实训练开源 causal LM 的 LoRA，并分别执行物品协同对齐和用户监督；没有用哈希或静态文本向量替代这两步。本地对照口径：基线是只使用 individual embedding 和实例级 target attention 的 online_base；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.23310">原论文</a> · <a href="../../../../reproductions/2605.23310-akt-rec/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="FLUID: From Ephemeral IDs to Multimodal Semantic Codes for Industrial-Scale Livestreaming Recommendation 搜广推与 LLM 应用 TikTok / ByteDance 2026-05-20 直播间通常只存活几十分钟，候选 item ID 来不及积累协同信号。FLUID 用 SigLIP2 与 Qwen3-Embedding 跨域编码短视频和直播的两分钟切片，再用四层 RQ-KMeans 得到 LUCID。slice LUCID 表示当前内容，room LUCID 对历史切片逐层多数投票；两者以独立 token 晚融合，最终完全移除候选 item ID，并用“加 slice—退 ID—加 room”三阶段避免切换不稳定。 未运行 SigLIP2、Qwen3-Embedding-0.6B、直播 ASR/OCR、真实两分钟切片和生产增量训练；Fidelity: 核心机制复现。执行跨域内容融合、slice/room 两级 LUCID、RQ-KMeans、prefix n-gram、ID-free late fusion 与三阶段 warmup；公开数据替代生产多模态流量。未运行 SigLIP2、Qwen3-Embedding-0.6B、直播 ASR/OCR、真实两分钟切片和生产增量训练；本地证明的是 LUCID/去 ID/分阶段迁移链路可运行，不声称复现论文线上收益。  llm-recommendation multimodal semantic-id cold-start ranking 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-fluid-d95a4248">FLUID: From Ephemeral IDs to Multimodal Semantic Codes for Industrial-Scale Livestreaming Recommendation</h2>
<p class="ar-learning-card__meta">TikTok / ByteDance · 论文公开：2026-05-20</p>
<p><strong>方法要点：</strong>直播间通常只存活几十分钟，候选 item ID 来不及积累协同信号。FLUID 用 SigLIP2 与 Qwen3-Embedding 跨域编码短视频和直播的两分钟切片，再用四层 RQ-KMeans 得到 LUCID。slice LUCID 表示当前内容，room LUCID 对历史切片逐层多数投票；两者以独立 token 晚融合，最终完全移除候选 item ID，并用“加 slice—退 ID—加 room”三阶段避免切换不稳定。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>未运行 SigLIP2、Qwen3-Embedding-0.6B、直播 ASR/OCR、真实两分钟切片和生产增量训练；Fidelity: 核心机制复现。执行跨域内容融合、slice/room 两级 LUCID、RQ-KMeans、prefix n-gram、ID-free late fusion 与三阶段 warmup；公开数据替代生产多模态流量。未运行 SigLIP2、Qwen3-Embedding-0.6B、直播 ASR/OCR、真实两分钟切片和生产增量训练；本地证明的是 LUCID/去 ID/分阶段迁移链路可运行，不声称复现论文线上收益。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.21832">原论文</a> · <a href="../../../../reproductions/2605.21832-fluid/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="A General Framework for Multimodal LLM-Based Multimedia Understanding in Large-Scale Recommendation Systems 搜广推与 LLM 应用 Meta 2026-05-10 视觉 embedding 难表达细粒度语义。论文用视觉 encoder+Q-Former 对齐 LLaMA2 生成 caption，再规范化为 categorical token IDs；item tokens 和用户历史 token profile 与 ID/视觉特征拼接进入生产排序模型，LLM 推理脱离在线主链路。 caption 模块相对 ID+content 内部基线仅 +0.03% 且 Hit 下降，本地未验证有效收益。Fidelity: 核心机制复现。内容 encoder、query cross-attention、离散 caption token、用户语义兴趣和 ID/视觉排序融合均训练；原始私有图片及 BLIP-2/LLaMA2-1.5B 规模未复刻。本地对照口径：统一跨模型基线是 DIN，MM-LLM NDCG@10 相对 DIN -13.23%；内部 ID+content 基线加入 caption token 后仅 +0.03% 且 Hit 下降。内部持平不代表优于经典模型。  multimodal llm-recommendation ranking 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-mm-llm-7bcb82aa">A General Framework for Multimodal LLM-Based Multimedia Understanding in Large-Scale Recommendation Systems</h2>
<p class="ar-learning-card__meta">Meta · 论文公开：2026-05-10</p>
<p><strong>方法要点：</strong>视觉 embedding 难表达细粒度语义。论文用视觉 encoder+Q-Former 对齐 LLaMA2 生成 caption，再规范化为 categorical token IDs；item tokens 和用户历史 token profile 与 ID/视觉特征拼接进入生产排序模型，LLM 推理脱离在线主链路。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>caption 模块相对 ID+content 内部基线仅 +0.03% 且 Hit 下降，本地未验证有效收益。Fidelity: 核心机制复现。内容 encoder、query cross-attention、离散 caption token、用户语义兴趣和 ID/视觉排序融合均训练；原始私有图片及 BLIP-2/LLaMA2-1.5B 规模未复刻。本地对照口径：统一跨模型基线是 DIN，MM-LLM NDCG@10 相对 DIN -13.23%；内部 ID+content 基线加入 caption token 后仅 +0.03% 且 Hit 下降。内部持平不代表优于经典模型。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.09338">原论文</a> · <a href="../../../../reproductions/2605.09338-mm-llm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RecGPT-Mobile: On-Device Large Language Models for User Intent Understanding in Taobao Feed Recommendation 搜广推与 LLM 应用 Alibaba / Taobao 2026-05-06 云端 LLM 能把点击、加购、收藏、购买等隐式行为翻译成显式搜索意图，但频繁上传行为并推理会增加成本、延迟和隐私风险。RecGPT-Mobile 把 Qwen3-0.6B 量化模型放到手机端，形成“本地收集行为→自适应构造 prompt→生成下一 query→服务端检索”的链路。训练数据由行为/搜索日志 60%、共购关系 20%、GPT 改写 15% 和人工标注 5% 组成；LoRA SFT 学习行为到 query 的映射。 Fidelity: 核心机制复现。实际执行 causal LM LoRA SFT、预算约束 adaptive prompt、意图漂移触发与 INT8 权重量化；私有数据和手机端系统缩小。本地模型是真实 causal LM 和 LoRA，不是类型分类 MLP；adaptive prompt、三项漂移公式和量化路径均执行。MovieLens 类型替代淘宝搜索 query，没有 GPT 改写、人工标注、生产检索和真机 fleet，故只验证方法链路与相对趋势。本地对照口径：基线为同一 SmolLM2-135M-Instruct 的零样本 intent completion；  llm-recommendation on-device intent-understanding serving-efficiency 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-recgpt-mobile-6c2409d1">RecGPT-Mobile: On-Device Large Language Models for User Intent Understanding in Taobao Feed Recommendation</h2>
<p class="ar-learning-card__meta">Alibaba / Taobao · 论文公开：2026-05-06</p>
<p><strong>方法要点：</strong>云端 LLM 能把点击、加购、收藏、购买等隐式行为翻译成显式搜索意图，但频繁上传行为并推理会增加成本、延迟和隐私风险。RecGPT-Mobile 把 Qwen3-0.6B 量化模型放到手机端，形成“本地收集行为→自适应构造 prompt→生成下一 query→服务端检索”的链路。训练数据由行为/搜索日志 60%、共购关系 20%、GPT 改写 15% 和人工标注 5% 组成；LoRA SFT 学习行为到 query 的映射。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。实际执行 causal LM LoRA SFT、预算约束 adaptive prompt、意图漂移触发与 INT8 权重量化；私有数据和手机端系统缩小。本地模型是真实 causal LM 和 LoRA，不是类型分类 MLP；adaptive prompt、三项漂移公式和量化路径均执行。MovieLens 类型替代淘宝搜索 query，没有 GPT 改写、人工标注、生产检索和真机 fleet，故只验证方法链路与相对趋势。本地对照口径：基线为同一 SmolLM2-135M-Instruct 的零样本 intent completion；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.04726">原论文</a> · <a href="../../../../reproductions/2605.04726-recgpt-mobile/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Beyond Static Collision Handling: Adaptive Semantic ID Learning for Multimodal Recommendation at Industrial Scale 搜广推与 LLM 应用 University of Electronic Science and Technology of China / Kuaishou 2026-04-26 按碰撞负载、语义相容性和训练阶段动态放松 SID 重叠约束，避免把所有碰撞等价惩罚。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 adasid 核心机制，相对 NDCG@10 -6.30%。  semantic-id multimodal-recommendation retrieval 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-adasid-04146a65">Beyond Static Collision Handling: Adaptive Semantic ID Learning for Multimodal Recommendation at Industrial Scale</h2>
<p class="ar-learning-card__meta">University of Electronic Science and Technology of China / Kuaishou · 论文公开：2026-04-26</p>
<p><strong>方法要点：</strong>按碰撞负载、语义相容性和训练阶段动态放松 SID 重叠约束，避免把所有碰撞等价惩罚。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 adasid 核心机制，相对 NDCG@10 -6.30%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.23522">原论文</a> · <a href="../../../../reproductions/2604.23522-adasid/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Modular Representation Compression: Adapting LLMs for Efficient and Effective Recommendations 搜广推与 LLM 应用 Shanghai Jiao Tong University 2026-04-20 论文发现 LLM 的中间层在推荐压缩后可能优于末层（MRA）。MARC 将压缩模块与任务适配模块显式拆开，并用信息约束解耦代理任务和推荐任务，保留任务相关信息的同时降低表征维度。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04693，相对变化 -13.11%。本地代理目标与论文生产任务不同，不能外推线上 lift。  llm-recommendation representation-compression modular-learning 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-marc-216b86ce">Modular Representation Compression: Adapting LLMs for Efficient and Effective Recommendations</h2>
<p class="ar-learning-card__meta">Shanghai Jiao Tong University · 论文公开：2026-04-20</p>
<p><strong>方法要点：</strong>论文发现 LLM 的中间层在推荐压缩后可能优于末层（MRA）。MARC 将压缩模块与任务适配模块显式拆开，并用信息约束解耦代理任务和推荐任务，保留任务相关信息的同时降低表征维度。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04693，相对变化 -13.11%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.18146">原论文</a> · <a href="../../../../reproductions/2604.18146-marc/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="LWGR: Lagrangian-Constrained Personalized World Knowledge for Generative Recommendation 搜广推与 LLM 应用 Alibaba International / CAS 2026-04-16 固定人工 prompt 提取的 LLM 知识既不能表达用户兴趣异质性，也可能与行为信号冲突。LWGR 将用户上下文切成多个子空间，每个子空间从独立 codebook 选择 codeword，形成可端到端学习的个性化 soft instruction；soft tokens 与历史商品文本共同通过 LLM，得到用户级 world knowledge。生成式推荐 decoder 在 BOS 处 cross-attend 这些知识，同时用相对冻结 reference 的置信度退化约束控制有害融合。 因此本地只验证实现和梯度路径，未验证约束有效性或论文准确率收益。Fidelity: 完整核心链路。本地实际执行 parallel codebook、IBQ straight-through、用户 soft instruction 进入真实冻结 causal LLM、BOS cross-attention、冻结生成式 reference，以及逐步 primal-dual 更新。未用静态文本向量替代个性化 LLM 前向。使用真实 SmolLM2-135M 前向，soft instruction 的梯度穿过冻结 LLM 回到 codebook；未用预计算常量冒充该步骤。  generative-recommendation soft-prompt world-knowledge lagrangian 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-lwgr-831cc9dc">LWGR: Lagrangian-Constrained Personalized World Knowledge for Generative Recommendation</h2>
<p class="ar-learning-card__meta">Alibaba International / CAS · 论文公开：2026-04-16</p>
<p><strong>方法要点：</strong>固定人工 prompt 提取的 LLM 知识既不能表达用户兴趣异质性，也可能与行为信号冲突。LWGR 将用户上下文切成多个子空间，每个子空间从独立 codebook 选择 codeword，形成可端到端学习的个性化 soft instruction；soft tokens 与历史商品文本共同通过 LLM，得到用户级 world knowledge。生成式推荐 decoder 在 BOS 处 cross-attend 这些知识，同时用相对冻结 reference 的置信度退化约束控制有害融合。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>因此本地只验证实现和梯度路径，未验证约束有效性或论文准确率收益。Fidelity: 完整核心链路。本地实际执行 parallel codebook、IBQ straight-through、用户 soft instruction 进入真实冻结 causal LLM、BOS cross-attention、冻结生成式 reference，以及逐步 primal-dual 更新。未用静态文本向量替代个性化 LLM 前向。使用真实 SmolLM2-135M 前向，soft instruction 的梯度穿过冻结 LLM 回到 codebook；未用预计算常量冒充该步骤。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.18771">原论文</a> · <a href="../../../../reproductions/2605.18771-lwgr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SID-Coord: Coordinating Semantic IDs for ID-based Ranking in Short-Video Search 搜广推与 LLM 应用 Kuaishou Technology 2026-04-12 SID-Coord 不把语义信号仅作为普通稠密特征，而是构造多层离散 SID；再通过层级融合、目标感知 HID–SID 门控和历史兴趣对齐，在头部物品记忆与长尾泛化之间逐样本协调。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04970，相对变化 -7.97%。本地代理目标与论文生产任务不同，不能外推线上 lift。  short-video-search semantic-id long-tail-ranking 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-sid-coord-811302bf">SID-Coord: Coordinating Semantic IDs for ID-based Ranking in Short-Video Search</h2>
<p class="ar-learning-card__meta">Kuaishou Technology · 论文公开：2026-04-12</p>
<p><strong>方法要点：</strong>SID-Coord 不把语义信号仅作为普通稠密特征，而是构造多层离散 SID；再通过层级融合、目标感知 HID–SID 门控和历史兴趣对齐，在头部物品记忆与长尾泛化之间逐样本协调。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04970，相对变化 -7.97%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.10471">原论文</a> · <a href="../../../../reproductions/2604.10471-sid-coord/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Zero-shot Cross-domain Knowledge Distillation: A Case study on YouTube Music 搜广推与 LLM 应用 Google / YouTube 2026-03-30 低流量产品无力训练大型专用 teacher。论文直接把数据丰富的 YouTube 多任务 teacher 应用于 YouTube Music 样本，把 serving task 与辅助 task logits 蒸馏到小模型，不要求源域数据或匹配的界面特征。 Fidelity: 核心机制复现。源域大 teacher、目标域小 student、目标样本上的 zero-shot logits 和 non-serving auxiliary-task distillation 均执行；私有跨产品 schema 未复刻。本地对照口径：跨模型基线是在相同 target split 上训练的 DIN，实验组 KD student 的 NDCG@10 相对 DIN -68.46%；内部基线 target-only student 加蒸馏后 +3.02%。后者只说明 KD 对弱 student 的增量，不能表述成优于 DIN。  distillation cross-domain ranking 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-cross-domain-kd-40631210">Zero-shot Cross-domain Knowledge Distillation: A Case study on YouTube Music</h2>
<p class="ar-learning-card__meta">Google / YouTube · 论文公开：2026-03-30</p>
<p><strong>方法要点：</strong>低流量产品无力训练大型专用 teacher。论文直接把数据丰富的 YouTube 多任务 teacher 应用于 YouTube Music 样本，把 serving task 与辅助 task logits 蒸馏到小模型，不要求源域数据或匹配的界面特征。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。源域大 teacher、目标域小 student、目标样本上的 zero-shot logits 和 non-serving auxiliary-task distillation 均执行；私有跨产品 schema 未复刻。本地对照口径：跨模型基线是在相同 target split 上训练的 DIN，实验组 KD student 的 NDCG@10 相对 DIN -68.46%；内部基线 target-only student 加蒸馏后 +3.02%。后者只说明 KD 对弱 student 的增量，不能表述成优于 DIN。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.28994">原论文</a> · <a href="../../../../reproductions/2603.28994-cross-domain-kd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="GateSID: Adaptive Gating for Semantic-Collaborative Alignment in Cold-Start Recommendation 搜广推与 LLM 应用 Alibaba International Digital Commerce 2026-03-24 共享注意力融合语义与协同行为，再用冷启动感知 gate 调节对比对齐强度：新物品偏语义，热门物品保留协同信号。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 gatesid 核心机制，相对 NDCG@10 +34.95%。  semantic-id cold-start contrastive-learning 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-gatesid-592868f0">GateSID: Adaptive Gating for Semantic-Collaborative Alignment in Cold-Start Recommendation</h2>
<p class="ar-learning-card__meta">Alibaba International Digital Commerce · 论文公开：2026-03-24</p>
<p><strong>方法要点：</strong>共享注意力融合语义与协同行为，再用冷启动感知 gate 调节对比对齐强度：新物品偏语义，热门物品保留协同信号。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 gatesid 核心机制，相对 NDCG@10 +34.95%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.22916">原论文</a> · <a href="../../../../reproductions/2603.22916-gatesid/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="TagLLM: A Fine-Grained Tag Generation Approach for Note Recommendation 搜广推与 LLM 应用 Tongji University 2026-03-23 TagLLM 按笔记类目构建用户兴趣手册，用多模态 CoT 按兴趣维度抽取细粒度标签，再通过两阶段知识蒸馏把大模型标签能力迁移到小模型，兼顾解释性和线上效率。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05147，相对变化 -4.69%。本地代理目标与论文生产任务不同，不能外推线上 lift。  content-understanding tag-generation knowledge-distillation 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-tagllm-3f53935e">TagLLM: A Fine-Grained Tag Generation Approach for Note Recommendation</h2>
<p class="ar-learning-card__meta">Tongji University · 论文公开：2026-03-23</p>
<p><strong>方法要点：</strong>TagLLM 按笔记类目构建用户兴趣手册，用多模态 CoT 按兴趣维度抽取细粒度标签，再通过两阶段知识蒸馏把大模型标签能力迁移到小模型，兼顾解释性和线上效率。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05147，相对变化 -4.69%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.21481">原论文</a> · <a href="../../../../reproductions/2603.21481-tagllm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="PinCLIP: Large-scale Foundational Multimodal Representation at Pinterest 搜广推与 LLM 应用 Pinterest 2026-03-03 通用 VLM 的训练目标与推荐不一致，且新内容缺少行为。PinCLIP 以 VLM 为 backbone，混合多粒度图文特征，并加入 Pin-Board 图邻居对齐目标，让表征同时掌握内容和推荐图语义。 实验组学习内容—共现图 canonical alignment，NDCG@10 0.03540→0.03490，相对 -1.41%，未复现论文增益。Fidelity: 核心机制复现。执行内容—图邻居对比对齐和 fresh cohort 评估；不训练视觉 backbone。无图像像素、VLM 预训练和 Pinterest 全图；只验证 neighbor alignment 路径，不能据此否定原论文。本地对照口径：基线是 raw genre/content similarity；  multimodal contrastive-learning cold-start 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-pinclip-b1beb580">PinCLIP: Large-scale Foundational Multimodal Representation at Pinterest</h2>
<p class="ar-learning-card__meta">Pinterest · 论文公开：2026-03-03</p>
<p><strong>方法要点：</strong>通用 VLM 的训练目标与推荐不一致，且新内容缺少行为。PinCLIP 以 VLM 为 backbone，混合多粒度图文特征，并加入 Pin-Board 图邻居对齐目标，让表征同时掌握内容和推荐图语义。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>实验组学习内容—共现图 canonical alignment，NDCG@10 0.03540→0.03490，相对 -1.41%，未复现论文增益。Fidelity: 核心机制复现。执行内容—图邻居对比对齐和 fresh cohort 评估；不训练视觉 backbone。无图像像素、VLM 预训练和 Pinterest 全图；只验证 neighbor alignment 路径，不能据此否定原论文。本地对照口径：基线是 raw genre/content similarity；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.03544">原论文</a> · <a href="../../../../reproductions/2603.03544-pinclip/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="IDProxy: Cold-Start CTR Prediction for Ads and Recommendation at Xiaohongshu with Multimodal LLMs 搜广推与 LLM 应用 Xiaohongshu / Shanghai Jiao Tong University / Fudan University 2026-03-02 多模态 LLM 的语义空间与 CTR 模型长期学习的 item-ID 协同空间并不一致。IDProxy 先用粗粒度对比目标对齐两者，再从多层 hidden state 生成 proxy，通过 residual gate 注入工业排序网络。 复现保真度：核心机制复现。复现保真度：核心机制复现。粗对齐、多层 proxy adapter 和残差门控实际执行；InternVL 与私有图文未复刻。MovieLens genre 作为公开内容模态，先投影到双向行为转移 ID 空间，再执行多层非线性 proxy 和 gate。  multimodal-llm id-alignment ranking 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-idproxy-2c030d0d">IDProxy: Cold-Start CTR Prediction for Ads and Recommendation at Xiaohongshu with Multimodal LLMs</h2>
<p class="ar-learning-card__meta">Xiaohongshu / Shanghai Jiao Tong University / Fudan University · 论文公开：2026-03-02</p>
<p><strong>方法要点：</strong>多模态 LLM 的语义空间与 CTR 模型长期学习的 item-ID 协同空间并不一致。IDProxy 先用粗粒度对比目标对齐两者，再从多层 hidden state 生成 proxy，通过 residual gate 注入工业排序网络。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现保真度：核心机制复现。复现保真度：核心机制复现。粗对齐、多层 proxy adapter 和残差门控实际执行；InternVL 与私有图文未复刻。MovieLens genre 作为公开内容模态，先投影到双向行为转移 ID 空间，再执行多层非线性 proxy 和 gate。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.01590">原论文</a> · <a href="../../../../reproductions/2603.01590-idproxy/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Stop Treating Collisions Equally: Qualification-Aware Semantic ID Learning for Recommendation at Industrial Scale 搜广推与 LLM 应用 University of Electronic Science and Technology of China / Kuaishou 2026-02-28 用业务资格信号决定碰撞对的 margin，而不是统一排斥；反馈稀疏或冷启动 item 得到更强的可辨识 SID。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 quasid 核心机制，相对 NDCG@10 -0.55%。  semantic-id collision-handling e-commerce 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-quasid-4adc5716">Stop Treating Collisions Equally: Qualification-Aware Semantic ID Learning for Recommendation at Industrial Scale</h2>
<p class="ar-learning-card__meta">University of Electronic Science and Technology of China / Kuaishou · 论文公开：2026-02-28</p>
<p><strong>方法要点：</strong>用业务资格信号决定碰撞对的 margin，而不是统一排斥；反馈稀疏或冷启动 item 得到更强的可辨识 SID。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 quasid 核心机制，相对 NDCG@10 -0.55%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.00632">原论文</a> · <a href="../../../../reproductions/2603.00632-quasid/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RQ-GMM: Residual Quantized Gaussian Mixture Model for Multimodal Semantic Discretization in CTR Prediction 搜广推与 LLM 应用 Tencent 2026-02-13 把图文多模态 embedding 逐层做残差量化，每层以高斯混合后验进行软分配，避免硬聚类的 codebook 利用率不足；语义离散化与 CTR 偏好建模解耦训练。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04685，相对变化 -13.25%。本地代理目标与论文生产任务不同，不能外推线上 lift。  multimodal-recommendation semantic-tokenization ctr-prediction 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-rq-gmm-d5d0f9d6">RQ-GMM: Residual Quantized Gaussian Mixture Model for Multimodal Semantic Discretization in CTR Prediction</h2>
<p class="ar-learning-card__meta">Tencent · 论文公开：2026-02-13</p>
<p><strong>方法要点：</strong>把图文多模态 embedding 逐层做残差量化，每层以高斯混合后验进行软分配，避免硬聚类的 codebook 利用率不足；语义离散化与 CTR 偏好建模解耦训练。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04685，相对变化 -13.25%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12593">原论文</a> · <a href="../../../../reproductions/2602.12593-rq-gmm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SARM: LLM-Augmented Semantic Anchor for End-to-End Live-Streaming Ranking 搜广推与 LLM 应用 Institute of Information Engineering, CAS / Kuaishou 2026-02-10 离线 MLLM 生成直播语义 anchor，轻量 SAE 将 anchor 注入端到端排序；非对称部署只在线更新排序器，避免 MLLM 时延。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 sarm 核心机制，相对 NDCG@10 +44.74%。  live-streaming semantic-anchor multimodal-recommendation 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-sarm-37e57a11">SARM: LLM-Augmented Semantic Anchor for End-to-End Live-Streaming Ranking</h2>
<p class="ar-learning-card__meta">Institute of Information Engineering, CAS / Kuaishou · 论文公开：2026-02-10</p>
<p><strong>方法要点：</strong>离线 MLLM 生成直播语义 anchor，轻量 SAE 将 anchor 注入端到端排序；非对称部署只在线更新排序器，避免 MLLM 时延。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 sarm 核心机制，相对 NDCG@10 +44.74%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.09401">原论文</a> · <a href="../../../../reproductions/2602.09401-sarm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="PIT: A Dynamic Personalized Item Tokenizer for End-to-End Generative Recommendation 搜广推与 LLM 应用 Beijing University of Posts and Telecommunications 2026-02-09 tokenizer 与生成推荐器共同训练，以用户引导的最小损失从多个候选 SID 中选出更契合当前偏好的编码；一对多 beam index 保留替代编码，减轻流式分布漂移。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05305，相对变化 -1.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation semantic-id dynamic-tokenizer 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-pit-181d335d">PIT: A Dynamic Personalized Item Tokenizer for End-to-End Generative Recommendation</h2>
<p class="ar-learning-card__meta">Beijing University of Posts and Telecommunications · 论文公开：2026-02-09</p>
<p><strong>方法要点：</strong>tokenizer 与生成推荐器共同训练，以用户引导的最小损失从多个候选 SID 中选出更契合当前偏好的编码；一对多 beam index 保留替代编码，减轻流式分布漂移。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05305，相对变化 -1.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.08530">原论文</a> · <a href="../../../../reproductions/2602.08530-pit/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="DOS: Dual-Flow Orthogonal Semantic IDs for Recommendation in Meituan 搜广推与 LLM 应用 Meituan 2026-02-04 普通 Semantic ID 的内容 codebook 与生成任务存在间隙。DOS 以用户行为流和商品语义流共同对齐 codebook，并用可约束的正交旋转把主语义与次语义解耦后逐层量化。 Fidelity: 核心机制复现。执行协同/语义双流、正交旋转及 residual quantization。公开 genre/共现替代美团 LLM item embedding 和生产生成器，不能与论文收入增益直接比较。本地对照口径：基线是未旋转的 content/collaborative ensemble；实验组执行 Procrustes 正交对齐与三层 ORQ，NDCG@10 0.03540→0.03938，相对 +11.26%。  generative-recommendation semantic-id orthogonal-quantization 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-dos-16f0eac2">DOS: Dual-Flow Orthogonal Semantic IDs for Recommendation in Meituan</h2>
<p class="ar-learning-card__meta">Meituan · 论文公开：2026-02-04</p>
<p><strong>方法要点：</strong>普通 Semantic ID 的内容 codebook 与生成任务存在间隙。DOS 以用户行为流和商品语义流共同对齐 codebook，并用可约束的正交旋转把主语义与次语义解耦后逐层量化。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。执行协同/语义双流、正交旋转及 residual quantization。公开 genre/共现替代美团 LLM item embedding 和生产生成器，不能与论文收入增益直接比较。本地对照口径：基线是未旋转的 content/collaborative ensemble；实验组执行 Procrustes 正交对齐与三层 ORQ，NDCG@10 0.03540→0.03938，相对 +11.26%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.04460">原论文</a> · <a href="../../../../reproductions/2602.04460-dos/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="RecGPT-V2 Technical Report 搜广推与 LLM 应用 Alibaba / Taobao 2025-12-16 RecGPT-V1 的多条固定推理链重复且难泛化。V2 用层级多 Agent 拆解意图，混合压缩行为表示，动态生成 meta-prompt，再用多奖励约束 RL 和 Agent-as-a-Judge 对齐。 Fidelity: 核心机制复现。实际执行短期/长期/类目 agent、meta-router、混合表示与 KL 约束偏好更新。Agent 是公开数据上的可训练小型专家，不是淘宝私有 LLM；没有人工 Judge 标注、解释生成或线上资源测量。本地对照口径：相对 RecGPT-V1 单路兴趣基线，实验组 NDCG@10 +18.52%。  llm-recommendation multi-agent reinforcement-learning ranking 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-recgpt-v2-f68ee63c">RecGPT-V2 Technical Report</h2>
<p class="ar-learning-card__meta">Alibaba / Taobao · 论文公开：2025-12-16</p>
<p><strong>方法要点：</strong>RecGPT-V1 的多条固定推理链重复且难泛化。V2 用层级多 Agent 拆解意图，混合压缩行为表示，动态生成 meta-prompt，再用多奖励约束 RL 和 Agent-as-a-Judge 对齐。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。实际执行短期/长期/类目 agent、meta-router、混合表示与 KL 约束偏好更新。Agent 是公开数据上的可训练小型专家，不是淘宝私有 LLM；没有人工 Judge 标注、解释生成或线上资源测量。本地对照口径：相对 RecGPT-V1 单路兴趣基线，实验组 NDCG@10 +18.52%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2512.14503">原论文</a> · <a href="../../../../reproductions/2512.14503-recgpt-v2/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="SaviorRec: Semantic-Behavior Alignment for Cold-Start Recommendation 搜广推与 LLM 应用 Alibaba 2025-08-02 冷启动排序依赖内容语义，但通用多模态 encoder 的相似度不等于平台用户的共点/共购关系，而且行为分布持续变化。SaviorRec 先以真实交互监督训练 SaviorEnc，再用 RQ-VAE 把表示离散为 Semantic ID；线上排序阶段冻结 SID，同时用零初始化的 Modal-Behavior Alignment（MBA）码本学习相对当前行为空间的残差，并用 target 与历史双向注意力完成 CTR 预测。 Fidelity: 核心机制复现。真实执行行为监督内容编码、RQ Semantic ID、零初始化 MBA 残差码本、双向 target/history attention 和 CTR 训练；MovieLens genre 替代私有图文模型。本地对照口径：基线是等预算 Content Ranker；实验组是 SaviorRec；总体 AUC +1.56%、cold AUC +6.92%，但都只有 1/3 seeds 正向。这是语义—行为对齐模块消融，不是相对 DIN。  cold start semantic ID multimodal recommendation 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-saviorrec-24eec791">SaviorRec: Semantic-Behavior Alignment for Cold-Start Recommendation</h2>
<p class="ar-learning-card__meta">Alibaba · 论文公开：2025-08-02</p>
<p><strong>方法要点：</strong>冷启动排序依赖内容语义，但通用多模态 encoder 的相似度不等于平台用户的共点/共购关系，而且行为分布持续变化。SaviorRec 先以真实交互监督训练 SaviorEnc，再用 RQ-VAE 把表示离散为 Semantic ID；线上排序阶段冻结 SID，同时用零初始化的 Modal-Behavior Alignment（MBA）码本学习相对当前行为空间的残差，并用 target 与历史双向注意力完成 CTR 预测。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。真实执行行为监督内容编码、RQ Semantic ID、零初始化 MBA 残差码本、双向 target/history attention 和 CTR 训练；MovieLens genre 替代私有图文模型。本地对照口径：基线是等预算 Content Ranker；实验组是 SaviorRec；总体 AUC +1.56%、cold AUC +6.92%，但都只有 1/3 seeds 正向。这是语义—行为对齐模块消融，不是相对 DIN。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.01375">原论文</a> · <a href="../../../../reproductions/2508.01375-saviorrec/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="FilterLLM: Text-To-Distribution LLM for Billion-Scale Cold-Start Recommendation 搜广推与 LLM 应用 Alibaba 2025-02-24 逐用户判断难以服务十亿用户冷启动。FilterLLM 把商品文本一次映射为用户分布，通过用户词表压缩输出空间，并用历史行为指导分布学习。 Fidelity: 核心机制复现。实际学习文本到压缩用户词表分布，并用行为分布约束冷启动表示。用户词表由公开交互 SVD 压缩，不是十亿用户 LLM token；没有淘宝新品文本、流量和延迟栈。本地对照口径：相对 content-to-item judgment 基线，实验组 NDCG@10 -9.82%。  llm-recommendation cold-start retrieval text-to-distribution 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-filterllm-8613b323">FilterLLM: Text-To-Distribution LLM for Billion-Scale Cold-Start Recommendation</h2>
<p class="ar-learning-card__meta">Alibaba · 论文公开：2025-02-24</p>
<p><strong>方法要点：</strong>逐用户判断难以服务十亿用户冷启动。FilterLLM 把商品文本一次映射为用户分布，通过用户词表压缩输出空间，并用历史行为指导分布学习。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。实际学习文本到压缩用户词表分布，并用行为分布约束冷启动表示。用户词表由公开交互 SVD 压缩，不是十亿用户 LLM token；没有淘宝新品文本、流量和延迟栈。本地对照口径：相对 content-to-item judgment 基线，实验组 NDCG@10 -9.82%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.16924">原论文</a> · <a href="../../../../reproductions/2502.16924-filterllm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Bursting Filter Bubble: Enhancing Serendipity Recommendations with Aligned Large Language Models 搜广推与 LLM 应用 Alibaba / Taobao 2025-02-19 惊喜推荐需同时相关且未见。SERAL 压缩超长历史为多层认知画像，以 LLM/人工 CDI 打破日志反馈环，用 IPO 对齐 SerenGPT，最后 nearline 生成并缓存候选。 内部消融中 IPO 相对纯 SFT 为 +8.59%，但 category-novelty 0.05542→0.05444，仍未复现惊喜度提升。Fidelity: 完整核心链路复现。静态/短期/长期 cognition profile、SFT、CDI 偏好对、IPO+SFT 与 nearline 全库缓存均执行；GPT-4/人工标注由公开内容和协同信号替代。本地对照口径：统一跨模型基线是 DIN，SERAL NDCG@10 相对 DIN +50.60%；内部基线是纯 SFT，增加 CDI+IPO 后 +8.59%，但 novelty 下降。排序收益与惊喜度结论分开报告。  llm-recommendation preference-alignment serendipity 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-seral-54db17e6">Bursting Filter Bubble: Enhancing Serendipity Recommendations with Aligned Large Language Models</h2>
<p class="ar-learning-card__meta">Alibaba / Taobao · 论文公开：2025-02-19</p>
<p><strong>方法要点：</strong>惊喜推荐需同时相关且未见。SERAL 压缩超长历史为多层认知画像，以 LLM/人工 CDI 打破日志反馈环，用 IPO 对齐 SerenGPT，最后 nearline 生成并缓存候选。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>内部消融中 IPO 相对纯 SFT 为 +8.59%，但 category-novelty 0.05542→0.05444，仍未复现惊喜度提升。Fidelity: 完整核心链路复现。静态/短期/长期 cognition profile、SFT、CDI 偏好对、IPO+SFT 与 nearline 全库缓存均执行；GPT-4/人工标注由公开内容和协同信号替代。本地对照口径：统一跨模型基线是 DIN，SERAL NDCG@10 相对 DIN +50.60%；内部基线是纯 SFT，增加 CDI+IPO 后 +8.59%，但 novelty 下降。排序收益与惊喜度结论分开报告。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.13539">原论文</a> · <a href="../../../../reproductions/2502.13539-seral/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Unlocking Scaling Law in Industrial Recommendation Systems with a Three-step Paradigm based Large User Model 搜广推与 LLM 应用 Alibaba 2025-02-12 端到端生成推荐能够扩展 Transformer 参数，却难以兼容长期演化的线上 DLRM、复杂特征和毫秒延迟。LUM 将问题拆成三步：先用生成任务构建用户知识，再用条件 token 离线查询不同兴趣，最后把固定知识特征接入任意判别式 DLRM。关键 token 顺序是：condition 描述即将预测的 item 所属场景、搜索词或类别，而不是事后附着在上一 item 上的 action。 Fidelity: 完整核心链路复现。真实执行 condition/item 异构 token encoder、causal next-condition-item InfoNCE、屏蔽式 group query、离线知识缓存、direct feature、interest matching 与下游 CTR DLRM；不声称复现 7B scaling law。本地对照口径：基线是 ID-DLRM；实验组是加入 LUM 离线知识的相同下游 DLRM；AUC 从 0.58233 升至 0.66734（+14.60%）。这是 LUM 知识特征消融，不是相对 DIN。  large user model generative pretraining knowledge querying CTR 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-lum-66a3db6d">Unlocking Scaling Law in Industrial Recommendation Systems with a Three-step Paradigm based Large User Model</h2>
<p class="ar-learning-card__meta">Alibaba · 论文公开：2025-02-12</p>
<p><strong>方法要点：</strong>端到端生成推荐能够扩展 Transformer 参数，却难以兼容长期演化的线上 DLRM、复杂特征和毫秒延迟。LUM 将问题拆成三步：先用生成任务构建用户知识，再用条件 token 离线查询不同兴趣，最后把固定知识特征接入任意判别式 DLRM。关键 token 顺序是：condition 描述即将预测的 item 所属场景、搜索词或类别，而不是事后附着在上一 item 上的 action。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 完整核心链路复现。真实执行 condition/item 异构 token encoder、causal next-condition-item InfoNCE、屏蔽式 group query、离线知识缓存、direct feature、interest matching 与下游 CTR DLRM；不声称复现 7B scaling law。本地对照口径：基线是 ID-DLRM；实验组是加入 LUM 离线知识的相同下游 DLRM；AUC 从 0.58233 升至 0.66734（+14.60%）。这是 LUM 知识特征消融，不是相对 DIN。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.08309">原论文</a> · <a href="../../../../reproductions/2502.08309-lum/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="MIM: Multi-modal Content Interest Modeling Paradigm for User Behavior Modeling 搜广推与 LLM 应用 Alibaba / Taobao 2025-02-01 纯 ID 行为模型难以理解新品内容。MIM 先遮盖重建多模态内容，再用 content-interest-aware SFT 对齐内容与协同兴趣，最后由 CiUBM 融合内容兴趣和 ID 兴趣。 Fidelity: 核心机制复现。实际执行遮盖内容重建、内容—协同对比对齐和 CiUBM 风格兴趣融合。genre 代理图文模态；没有淘宝私有曝光、真实多模态 encoder 与生产 serving。本地与论文线上数值不可直接比较。本地对照口径：相对 ID 共现兴趣基线，实验组 NDCG@10 +0.94%。  multimodal-recommendation user-modeling pretraining ranking 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-mim-fdc0fc79">MIM: Multi-modal Content Interest Modeling Paradigm for User Behavior Modeling</h2>
<p class="ar-learning-card__meta">Alibaba / Taobao · 论文公开：2025-02-01</p>
<p><strong>方法要点：</strong>纯 ID 行为模型难以理解新品内容。MIM 先遮盖重建多模态内容，再用 content-interest-aware SFT 对齐内容与协同兴趣，最后由 CiUBM 融合内容兴趣和 ID 兴趣。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。实际执行遮盖内容重建、内容—协同对比对齐和 CiUBM 风格兴趣融合。genre 代理图文模态；没有淘宝私有曝光、真实多模态 encoder 与生产 serving。本地与论文线上数值不可直接比较。本地对照口径：相对 ID 共现兴趣基线，实验组 NDCG@10 +0.94%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.00321">原论文</a> · <a href="../../../../reproductions/2502.00321-mim/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Balancing Efficiency and Effectiveness: An LLM-Infused Approach for Optimized CTR Prediction 搜广推与 LLM 应用 Meituan 2024-12-09 直接在 CTR 链路调用大模型效果好但成本不可接受；只缓存静态 embedding 又无法跟随 CTR 目标更新。MSD 的 MKDM 先让大 teacher 为用户和物品生成关键词与推理，再让较小 student 自回归学习这些输出。MKIM 对蒸馏后的 student 做 LoRA CTR 对齐，并用 user/target/history adapter 融合推荐特征。高频物品优先走预计算缓存，低频或未命中物品在线编码，同时只融合与 target 最相关的历史。 Fidelity: 完整核心链路复现。真实执行 teacher 知识生成、T5 自回归蒸馏、student q/v-LoRA CTR 对齐、多层特征 adapter、频次自适应缓存/在线计算和相关历史融合；生产广告特征与缓存服务未复刻。本地对照口径：基线是 ID-only CTR ranker；实验组是完整 MSD；AUC 从 0.68449 升至 0.69510（+1.55%）。这是 LLM 蒸馏与缓存语义特征的联合消融，不是相对 DIN。  LLM distillation CTR serving efficiency 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-msd-3339b303">Balancing Efficiency and Effectiveness: An LLM-Infused Approach for Optimized CTR Prediction</h2>
<p class="ar-learning-card__meta">Meituan · 论文公开：2024-12-09</p>
<p><strong>方法要点：</strong>直接在 CTR 链路调用大模型效果好但成本不可接受；只缓存静态 embedding 又无法跟随 CTR 目标更新。MSD 的 MKDM 先让大 teacher 为用户和物品生成关键词与推理，再让较小 student 自回归学习这些输出。MKIM 对蒸馏后的 student 做 LoRA CTR 对齐，并用 user/target/history adapter 融合推荐特征。高频物品优先走预计算缓存，低频或未命中物品在线编码，同时只融合与 target 最相关的历史。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 完整核心链路复现。真实执行 teacher 知识生成、T5 自回归蒸馏、student q/v-LoRA CTR 对齐、多层特征 adapter、频次自适应缓存/在线计算和相关历史融合；生产广告特征与缓存服务未复刻。本地对照口径：基线是 ID-only CTR ranker；实验组是完整 MSD；AUC 从 0.68449 升至 0.69510（+1.55%）。这是 LLM 蒸馏与缓存语义特征的联合消融，不是相对 DIN。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2412.06860">原论文</a> · <a href="../../../../reproductions/2412.06860-msd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="PRECISE: Pre-training Sequential Recommenders with Collaborative and Semantic Information 搜广推与 LLM 应用 Tencent / WeChat 2024-12-09 纯 ID 序列模型能学协同关系，但长尾物品训练不足；纯文本/LLM 方法能迁移语义，却容易丢掉协同信号。PRECISE 将二者在 item 层融合，并把训练拆为 Universal Training（全场景兴趣）和 Targeted Training（稀疏目标场景/任务）。论文还针对文本表示过强导致 ID 学不动的问题，先冻结 token 训练 ID，再解冻联合训练。 Fidelity: 完整核心链路复现。实际执行 LLM token hidden-state 初始化、可训练 token、top-k MoE attention、ID/text 交替训练、全场景 causal NIP、目标场景双向 Transformer、序列拼接 MLP 与 cross-user BPR。Qwen2-1.5B 缩为 SmolLM2-135M，WeChat 私有日志替换为 MovieLens-1M。本地对照口径：基线是只做目标任务训练的 PRECISE-TT；实验组是 UT 全场景预训练后再 TT；  LLM semantic embedding sequential pre-training MoE targeted training 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-precise-dd30948e">PRECISE: Pre-training Sequential Recommenders with Collaborative and Semantic Information</h2>
<p class="ar-learning-card__meta">Tencent / WeChat · 论文公开：2024-12-09</p>
<p><strong>方法要点：</strong>纯 ID 序列模型能学协同关系，但长尾物品训练不足；纯文本/LLM 方法能迁移语义，却容易丢掉协同信号。PRECISE 将二者在 item 层融合，并把训练拆为 Universal Training（全场景兴趣）和 Targeted Training（稀疏目标场景/任务）。论文还针对文本表示过强导致 ID 学不动的问题，先冻结 token 训练 ID，再解冻联合训练。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 完整核心链路复现。实际执行 LLM token hidden-state 初始化、可训练 token、top-k MoE attention、ID/text 交替训练、全场景 causal NIP、目标场景双向 Transformer、序列拼接 MLP 与 cross-user BPR。Qwen2-1.5B 缩为 SmolLM2-135M，WeChat 私有日志替换为 MovieLens-1M。本地对照口径：基线是只做目标任务训练的 PRECISE-TT；实验组是 UT 全场景预训练后再 TT；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2412.06308">原论文</a> · <a href="../../../../reproductions/2412.06308-precise/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Knowledge Adaptation from Large Language Model to Recommendation for Practical Industrial Application 搜广推与 LLM 应用 Kuaishou 2024-05-07 直接把冻结 LLM embedding 用作推荐表示存在开放世界语义域与协同域的差距。LEARN 的 CEG 冻结 LLM 并平均池化 item 文本，PCH 用可训练因果 Transformer 从历史 content embeddings 学用户偏好，再投影到线上推荐空间。 Fidelity: 完整核心链路复现。真实执行冻结预训练 LM 的 CEG、缓存 item embedding、因果 PCH、dense all-position loss 和 online projection；BERT-tiny/MovieLens 替代 Baichuan2-7B/快手日志。本地对照口径：基线是 frozen LLM semantic mean；实验组是 LEARN CEG+PCH；NDCG@10 从 0.00487 升至 0.01622（+233.10%），同时 head share 升至 69.50%。这是知识适配模块消融，不是相对 DIN。  llm-recommendation knowledge-adaptation cold-start 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-learn-c99c03ce">Knowledge Adaptation from Large Language Model to Recommendation for Practical Industrial Application</h2>
<p class="ar-learning-card__meta">Kuaishou · 论文公开：2024-05-07</p>
<p><strong>方法要点：</strong>直接把冻结 LLM embedding 用作推荐表示存在开放世界语义域与协同域的差距。LEARN 的 CEG 冻结 LLM 并平均池化 item 文本，PCH 用可训练因果 Transformer 从历史 content embeddings 学用户偏好，再投影到线上推荐空间。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 完整核心链路复现。真实执行冻结预训练 LM 的 CEG、缓存 item embedding、因果 PCH、dense all-position loss 和 online projection；BERT-tiny/MovieLens 替代 Baichuan2-7B/快手日志。本地对照口径：基线是 frozen LLM semantic mean；实验组是 LEARN CEG+PCH；NDCG@10 从 0.00487 升至 0.01622（+233.10%），同时 head share 升至 69.50%。这是知识适配模块消融，不是相对 DIN。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2405.03988">原论文</a> · <a href="../../../../reproductions/2405.03988-learn/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Breaking the Length Barrier: LLM-Enhanced CTR Prediction in Long Textual User Behaviors 搜广推与 LLM 应用 Ant Group 2024-03-28 直接把长用户行为文本反复送入 LLM，会重复编码同一原子行为，并把低层语义提取与高层行为交互强耦合。BAHE 在浅层编码每个原子行为并离线存储；训练时只取行为向量，以更深的可训练层聚合，再与候选物品一起完成 CTR 预测。这样既缩短上层序列，也允许浅层异步、低频更新。 Fidelity: 完整核心链路复现。真实执行冻结浅层 LLM 的原子行为编码与落盘、可训练上层 Transformer 的行为聚合和 CTR 训练；生产 LLM/广告日志替换为 BERT-tiny/MovieLens-100K。本地对照口径：基线是逐样本运行完整文本上层微调；实验组是 BAHE 原子缓存与层次聚合；耗时 -53.61%，但 AUC -2.94%。这是效率—效果对照，不是准确率提升。  llm-recommendation ctr-ranking long-sequence efficiency 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-bahe-7645b8ec">Breaking the Length Barrier: LLM-Enhanced CTR Prediction in Long Textual User Behaviors</h2>
<p class="ar-learning-card__meta">Ant Group · 论文公开：2024-03-28</p>
<p><strong>方法要点：</strong>直接把长用户行为文本反复送入 LLM，会重复编码同一原子行为，并把低层语义提取与高层行为交互强耦合。BAHE 在浅层编码每个原子行为并离线存储；训练时只取行为向量，以更深的可训练层聚合，再与候选物品一起完成 CTR 预测。这样既缩短上层序列，也允许浅层异步、低频更新。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 完整核心链路复现。真实执行冻结浅层 LLM 的原子行为编码与落盘、可训练上层 Transformer 的行为聚合和 CTR 训练；生产 LLM/广告日志替换为 BERT-tiny/MovieLens-100K。本地对照口径：基线是逐样本运行完整文本上层微调；实验组是 BAHE 原子缓存与层次聚合；耗时 -53.61%，但 AUC -2.94%。这是效率—效果对照，不是准确率提升。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2403.19347">原论文</a> · <a href="../../../../reproductions/2403.19347-bahe/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="A Large Language Model Enhanced Sequential Recommender for Joint Video and Comment Recommendation 搜广推与 LLM 应用 Kuaishou 2024-03-20 短视频用户会同时消费视频和评论。纯序列模型能高效服务，但难以理解评论语义；直接让 LLM 在线推荐又太慢。LSVCR 用 LLM 同时担任离线文本 encoder 和仅训练期存在的 supplemental recommender，再把 LLM 的个性化偏好对齐到可部署的双序列 SR 模型。部署时不需要运行生成式 LLM。 对齐 loss 明显下降，排除了 alignment 根本未训练的情况。Fidelity: 完整核心链路复现。真实执行 causal LM q/v-LoRA SFT、LLM 文本编码、随机位置扩展、商品/评论双 Transformer、双向 cross-attention、SSC/VCC 对齐和联合微调；ChatGLM3 与快手私有日志缩小替换。本地对照口径：基线是相同 SR 网络但不做 LLM preference alignment；实验组是完整 LSVCR；Comment NDCG@10 +50.40%，Item NDCG@10 -56.42%。这是 alignment 消融，不能概括成整体推荐效果提升。  LLM recommendation comment recommendation preference alignment 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-lsvcr-e1dd0222">A Large Language Model Enhanced Sequential Recommender for Joint Video and Comment Recommendation</h2>
<p class="ar-learning-card__meta">Kuaishou · 论文公开：2024-03-20</p>
<p><strong>方法要点：</strong>短视频用户会同时消费视频和评论。纯序列模型能高效服务，但难以理解评论语义；直接让 LLM 在线推荐又太慢。LSVCR 用 LLM 同时担任离线文本 encoder 和仅训练期存在的 supplemental recommender，再把 LLM 的个性化偏好对齐到可部署的双序列 SR 模型。部署时不需要运行生成式 LLM。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>对齐 loss 明显下降，排除了 alignment 根本未训练的情况。Fidelity: 完整核心链路复现。真实执行 causal LM q/v-LoRA SFT、LLM 文本编码、随机位置扩展、商品/评论双 Transformer、双向 cross-attention、SSC/VCC 对齐和联合微调；ChatGLM3 与快手私有日志缩小替换。本地对照口径：基线是相同 SR 网络但不做 LLM preference alignment；实验组是完整 LSVCR；Comment NDCG@10 +50.40%，Item NDCG@10 -56.42%。这是 alignment 消融，不能概括成整体推荐效果提升。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2403.13574">原论文</a> · <a href="../../../../reproductions/2403.13574-lsvcr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="NoteLLM: A Retrievable Large Language Model for Note Recommendation 搜广推与 LLM 应用 Xiaohongshu 2024-03-04 纯文本 embedding 缺少协同信号，纯对比学习又可能损害 LLM 生成能力。NoteLLM 用统一 compression prompt 将内容压到特殊 token；GCL 拉近用户共读 note，CSFT 从同一压缩状态生成 hashtag/category。 Fidelity: 完整核心链路复现。真实执行 note compression special token、行为共现 GCL、类别生成 CSFT 和压缩状态 I2I 检索；T5-small/MovieLens 替代 7B LLM/小红书 note。本地对照口径：基线是冻结 compression-state embedding；实验组是 NoteLLM 的 GCL+CSFT embedding；NDCG@10 从 0.01142 升至 0.01224（+7.15%）。这是表征训练消融，不是端到端排序模型相对 DIN 的提升。  llm-recommendation contrastive-learning i2i-retrieval 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-notellm-9364e133">NoteLLM: A Retrievable Large Language Model for Note Recommendation</h2>
<p class="ar-learning-card__meta">Xiaohongshu · 论文公开：2024-03-04</p>
<p><strong>方法要点：</strong>纯文本 embedding 缺少协同信号，纯对比学习又可能损害 LLM 生成能力。NoteLLM 用统一 compression prompt 将内容压到特殊 token；GCL 拉近用户共读 note，CSFT 从同一压缩状态生成 hashtag/category。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 完整核心链路复现。真实执行 note compression special token、行为共现 GCL、类别生成 CSFT 和压缩状态 I2I 检索；T5-small/MovieLens 替代 7B LLM/小红书 note。本地对照口径：基线是冻结 compression-state embedding；实验组是 NoteLLM 的 GCL+CSFT embedding；NDCG@10 从 0.01142 升至 0.01224（+7.15%）。这是表征训练消融，不是端到端排序模型相对 DIN 的提升。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2403.01744">原论文</a> · <a href="../../../../reproductions/2403.01744-notellm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="Towards Open-World Recommendation with Knowledge Augmentation from Large Language Models 搜广推与 LLM 应用 Huawei 2023-06-19 封闭域推荐只能从本域交互学习，难以理解物品事实和用户偏好背后的常识。KAR 不把 LLM 直接当在线推荐器，而是通过 factorization prompting 让 LLM 分别产出用户偏好推理知识与物品事实知识，再用 hybrid-expert adapter 压缩成与 ID 推荐模型兼容的向量。知识可预生成并缓存，因此线上不承担 LLM 自回归延迟。 Fidelity: 完整核心链路复现。真实执行 factorization prompts、用户偏好/物品事实知识生成、离线缓存、hybrid-expert adapter 和下游 CTR 训练；PanGu 与华为日志替换为 SmolLM2-135M-Instruct 和 MovieLens-100K。本地对照口径：基线是纯 ID ranker；实验组是加入 LLM 知识与四专家 adapter 的 KAR；AUC 从 0.72188 升至 0.72774（+0.81%）。这是知识增强模块消融，不是相对 DIN 的比较。  llm-recommendation knowledge-augmentation ctr-ranking 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-kar-c442fbbf">Towards Open-World Recommendation with Knowledge Augmentation from Large Language Models</h2>
<p class="ar-learning-card__meta">Huawei · 论文公开：2023-06-19</p>
<p><strong>方法要点：</strong>封闭域推荐只能从本域交互学习，难以理解物品事实和用户偏好背后的常识。KAR 不把 LLM 直接当在线推荐器，而是通过 factorization prompting 让 LLM 分别产出用户偏好推理知识与物品事实知识，再用 hybrid-expert adapter 压缩成与 ID 推荐模型兼容的向量。知识可预生成并缓存，因此线上不承担 LLM 自回归延迟。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 完整核心链路复现。真实执行 factorization prompts、用户偏好/物品事实知识生成、离线缓存、hybrid-expert adapter 和下游 CTR 训练；PanGu 与华为日志替换为 SmolLM2-135M-Instruct 和 MovieLens-100K。本地对照口径：基线是纯 ID ranker；实验组是加入 LLM 知识与四专家 adapter 的 KAR；AUC 从 0.72188 升至 0.72774（+0.81%）。这是知识增强模块消融，不是相对 DIN 的比较。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2306.10933">原论文</a> · <a href="../../../../reproductions/2306.10933-kar/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/content-semantic-ids" data-search="M6-Rec: Generative Pretrained Language Models are Open-Ended Recommender Systems 搜广推与 LLM 应用 Alibaba 2022-05-17 传统推荐模型为排序、召回、解释、对话分别维护架构。M6-Rec 把匿名行为序列和候选物品都改写成自然语言，让一个生成式预训练模型统一完成排序、召回、zero-shot、解释、内容生成和对话。为避免每个场景完整微调巨型 M6，论文提出 option tuning 和 option-adapter tuning，只训练约 1% 的任务参数；线上再用 late interaction、early exit、参数共享和剪枝得到 10M/2M 的 M6-Edge。 Fidelity: 核心机制复现。真实执行冻结预训练 Transformer、自然语言用户行为、option tuning 与逐层 bottleneck option-adapter tuning；M6 生产模型、私有数据和 early-exit/pruning serving 未复刻。本地对照口径：基线是只训练 option prototype 的 Option Tuning；实验组额外训练 24d adapter；AUC 从 0.53832 升至 0.53890（+0.12%）。这是 adapter 增量消融，不代表完整 M6-Rec 相对 DIN 或工业基线的提升。  llm-recommendation foundation-model parameter-efficient-tuning 搜广推 语义表征、用户知识与冷启动">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 语义表征、用户知识与冷启动</a></p>
<h2 id="paper-recommendation-m6rec-d70d1b1b">M6-Rec: Generative Pretrained Language Models are Open-Ended Recommender Systems</h2>
<p class="ar-learning-card__meta">Alibaba · 论文公开：2022-05-17</p>
<p><strong>方法要点：</strong>传统推荐模型为排序、召回、解释、对话分别维护架构。M6-Rec 把匿名行为序列和候选物品都改写成自然语言，让一个生成式预训练模型统一完成排序、召回、zero-shot、解释、内容生成和对话。为避免每个场景完整微调巨型 M6，论文提出 option tuning 和 option-adapter tuning，只训练约 1% 的任务参数；线上再用 late interaction、early exit、参数共享和剪枝得到 10M/2M 的 M6-Edge。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。真实执行冻结预训练 Transformer、自然语言用户行为、option tuning 与逐层 bottleneck option-adapter tuning；M6 生产模型、私有数据和 early-exit/pruning serving 未复刻。本地对照口径：基线是只训练 option prototype 的 Option Tuning；实验组额外训练 24d adapter；AUC 从 0.53832 升至 0.53890（+0.12%）。这是 adapter 增量消融，不代表完整 M6-Rec 相对 DIN 或工业基线的提升。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2205.08084">原论文</a> · <a href="../../../../reproductions/2205.08084-m6rec/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
