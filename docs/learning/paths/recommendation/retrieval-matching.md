---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 候选生成与搜索匹配

[搜广推](index.md) / 36 个问题 · 36 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">36 个问题 · 36 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pair" data-paper-title="PAIR: Preference-Aligned Intent Retrieval for Premium People Recommendation at LinkedIn" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="PAIR: Preference-Aligned Intent Retrieval for Premium People Recommendation at LinkedIn 搜广推与 LLM 应用 LinkedIn 2026-10-22 职业社交中的相关性往往是互补而非相似：求职者可能需要招聘者，不是与自己背景最相近的人。PAIR 从被点击候选、同次曝光未点击候选和随机会员构造偏好，训练共享的 profile/document 编码器，并用历史塔刻画短期意图。论文明确说它不是 token 级 DPO，也没有显式参考模型或 KL 项；损失在计算形式上就是多负例对比学习，差别在曝光条件下的监督语义。 成本过高，不复现（审查 DONE）；这些是公式与接口诊断，不是模型准确率、完整推荐能力或线上提升。固定三种子证据见组件指标，真实CUDA回执为 docs/gpu-validations/pair-a100-20261023.json。验证比较独立标量余弦/交叉熵公式与梯度，执行三次真实更新，检查掩码历史无影响、位置顺序有效、曝光负例不混入点击正例。这些是公式与接口诊断，不是模型准确率、完整推荐能力或线上提升。  召回与匹配 曝光偏好与历史意图 搜广推 候选生成与搜索匹配 PAIR 的偏好损失形式像多负例对比学习，为什么不能把它称作 token 级 DPO？ PAIR 用点击候选、同次曝光未点击候选和随机会员构造偏好，训练资料编码器与历史塔，使相关性表达互补需求而非只看相似。其计算形式是多负例对比目标，没有逐 token 概率比、显式参考策略或 KL 项。定义性差别在曝光条件下的监督语义，不能因使用“偏好”一词就等同于语言模型 DPO。 示意：求职者点击了招聘者而略过另一位求职者。两位求职者资料可能更相似，但这种曝光偏好要求编码器学会互补关系；训练比较的是候选表示得分，不是回答文本的 token 概率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-pair-40d29d93" class="ar-learning-paper-anchor"></span>
<h2 id="qa-41753ca1acfbc839">PAIR 的偏好损失形式像多负例对比学习，为什么不能把它称作 token 级 DPO？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apair">PAIR: Preference-Aligned Intent Retrieval for Premium People Recommendation at LinkedIn</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>PAIR 用点击候选、同次曝光未点击候选和随机会员构造偏好，训练资料编码器与历史塔，使相关性表达互补需求而非只看相似。其计算形式是多负例对比目标，没有逐 token 概率比、显式参考策略或 KL 项。定义性差别在曝光条件下的监督语义，不能因使用“偏好”一词就等同于语言模型 DPO。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>求职者点击了招聘者而略过另一位求职者。两位求职者资料可能更相似，但这种曝光偏好要求编码器学会互补关系；训练比较的是候选表示得分，不是回答文本的 token 概率。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与服务边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30941v1">原论文</a> · <a href="../../../../recommendation-components/2610.30941-pair/">实现解读</a> · <a href="#qa-41753ca1acfbc839">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:snap-dpa-relevance" data-paper-title="LLM-based User-Product Relevance Evaluation for Dynamic Product Advertising" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="LLM-based User-Product Relevance Evaluation for Dynamic Product Advertising 搜广推与 LLM 应用 Snap Inc. 2026-10-10 广告召回的点击信号稀疏且有偏，单纯离线命中率难以代表用户真实需求。该方法按语义ID与事件类型压缩历史意图，通过自动发现且人工业务对齐的相关性准则训练学生判别器，再聚合为用户与流量组的相关性指标。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文§4–5依赖10K私有日志经GPT-5、Gemini-2.5-Pro与多轮人工审定；生产student为Gemini-2.5-Flash微调并经Vertex AI调用。商业API、人工标注和私有数据不是当前单卡可直接复现的资源；未测量本地或API总成本，不启动付费教师调用或替换为启发式judge。  ads-retrieval llm-judge evaluation 搜广推 候选生成与搜索匹配 Snap DPA 相关性指标为什么区分 MicroRel 与 MacroRel，还要先审定判别准则？ 历史按语义与事件压缩成意图组，再由经准则训练的判别器评价候选相关性。MicroRel 对用户—候选对等权，容易受候选多的用户影响；MacroRel 对用户等权，观察的是另一种群体平均。准则发现与人工业务对齐决定“相关”含义，聚合公式不能补救错误判别；本地没有复现私有评审数据和商业模型流程。 示意：一个用户有一百条候选，另一个只有十条。按候选对平均时前者权重大十倍，按用户平均时两者相同；两种结果都应先建立在可靠的相关性判断上。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-snap-dpa-relevance-9f0c9ccb" class="ar-learning-paper-anchor"></span>
<h2 id="qa-9d5c6706cb902a75">Snap DPA 相关性指标为什么区分 MicroRel 与 MacroRel，还要先审定判别准则？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asnap-dpa-relevance">LLM-based User-Product Relevance Evaluation for Dynamic Product Advertising</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Snap Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>历史按语义与事件压缩成意图组，再由经准则训练的判别器评价候选相关性。MicroRel 对用户—候选对等权，容易受候选多的用户影响；MacroRel 对用户等权，观察的是另一种群体平均。准则发现与人工业务对齐决定“相关”含义，聚合公式不能补救错误判别；本地没有复现私有评审数据和商业模型流程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个用户有一百条候选，另一个只有十条。按候选对平均时前者权重大十倍，按用户平均时两者相同；两种结果都应先建立在可靠的相关性判断上。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14550">原论文</a> · <a href="../../../../reproductions/2610.14550-snap-dpa-relevance/">实现解读</a> · <a href="#qa-9d5c6706cb902a75">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rptune" data-paper-title="RPTune: Learned Context Curation for LLM Catalog Search" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="RPTune: Learned Context Curation for LLM Catalog Search 搜广推与 LLM 应用 Google 2026-10-01 用查询-商品编码器、可学习调整项和下游 LLM 反馈共同决定商品保留与摆放顺序；高优商品靠近提示词末端，再对编排后的目录做选择后训练。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。只执行 rank/prune/position 核心编排，不调用 Gemini/Gemma、商家目录或论文训练。只执行 rank/prune/position 核心编排，不调用 Gemini/Gemma、商家目录或论文训练。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  search llm-recommendation context-curation 搜广推 候选生成与搜索匹配 RPTune 为什么把高优商品按升序放到提示末端，而不是简单按相关性降序塞满上下文？ 目录选择与提示位置都会影响下游语言模型利用信息的方式。查询—商品得分加可学习调整项先决定保留谁，再把高优项靠近末端，让编排本身成为可优化变量；后训练适配这种目录输入。它不只是换排序展示顺序，本地只检验定义性编排算子，不能据此声称所有模型都必然有相同位置偏好。 示意：提示只能容纳三件商品，先删掉低相关候选，再把最符合预算的商品放在靠近回答的位置。模型看到的内容与位置同时变化，需要分别检查各自贡献。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-rptune-1e6a74b6" class="ar-learning-paper-anchor"></span>
<h2 id="qa-e2aa86945fffe4e8">RPTune 为什么把高优商品按升序放到提示末端，而不是简单按相关性降序塞满上下文？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arptune">RPTune: Learned Context Curation for LLM Catalog Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目录选择与提示位置都会影响下游语言模型利用信息的方式。查询—商品得分加可学习调整项先决定保留谁，再把高优项靠近末端，让编排本身成为可优化变量；后训练适配这种目录输入。它不只是换排序展示顺序，本地只检验定义性编排算子，不能据此声称所有模型都必然有相同位置偏好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>提示只能容纳三件商品，先删掉低相关候选，再把最符合预算的商品放在靠近回答的位置。模型看到的内容与位置同时变化，需要分别检查各自贡献。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00964">原论文</a> · <a href="../../../../reproductions/2610.00964-rptune/">实现解读</a> · <a href="#qa-e2aa86945fffe4e8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:muser" data-paper-title="MuSeR: Scalable Long-sequence Recommendation with Multi-interest Modeling" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="MuSeR: Scalable Long-sequence Recommendation with Multi-interest Modeling 搜广推与 LLM 应用 Baidu 2026-09-20 工业用户长期行为可达十万级，直接截断丢掉稳定偏好，直接 Transformer 编码又超预算。MuSeR 将最近行为原样保留，中期与远期行为分别用更大步幅汇聚；压缩后的序列由轻量 Transformer 编码。多组可学习 query 从序列状态提取不同兴趣，候选物品再通过相似度 softmax 选择兴趣。论文还把 ERNIE 生成的内容摘要蒸馏后用 BGE 编码，与 ID embedding 对齐并融合；训练使用 next-K 对比目标和兴趣正交正则。 复现级别：概念验证（非论文完整复现）。复现级别：概念验证（非论文完整复现）。本地训练了分层时间压缩、Transformer 编码、可学习多查询兴趣、候选自适应兴趣融合与正交约束；但论文的 ERNIE→BGE 多模态语义链路被公开商品标签替代，因此不能把本地结果称为 MuSeR 论文效果。公开数据只有视频标签作为内容特征，没有论文使用的 ERNIE 摘要、ERNIE-Speed 蒸馏、BGE 文本/视频向量；这决定了本实验只能列为概念验证。本地对照口径：最近序列单兴趣 ID 为基线，三 seed test Recall@10 均值 0.0100；完整本地实验组 0.0257，相对 +156.7%、绝对 +0.0157。  retrieval long-sequence multi-interest 搜广推 候选生成与搜索匹配 MuSeR 为什么近、中、远期历史用不同压缩步幅，还要让候选选择不同兴趣？ 近期行为保留细节以捕捉即时意图，较远历史用更大步幅汇聚以控制长序列成本。多个可学习查询再从压缩序列提取不同兴趣，候选依据相似度选择合适的兴趣组合。时间压缩解决“读多少历史”，多兴趣选择解决“读完后用哪部分”；二者互补，但汇聚仍可能损失远期稀有事件。 示意：用户长期爱摄影，近期在准备露营。远期摄影行为可合并保留稳定偏好，最近露营浏览逐条保留；相机候选与帐篷候选再分别激活不同兴趣向量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-muser-f887e208" class="ar-learning-paper-anchor"></span>
<h2 id="qa-96e91ee29d96d6b7">MuSeR 为什么近、中、远期历史用不同压缩步幅，还要让候选选择不同兴趣？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amuser">MuSeR: Scalable Long-sequence Recommendation with Multi-interest Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Baidu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>近期行为保留细节以捕捉即时意图，较远历史用更大步幅汇聚以控制长序列成本。多个可学习查询再从压缩序列提取不同兴趣，候选依据相似度选择合适的兴趣组合。时间压缩解决“读多少历史”，多兴趣选择解决“读完后用哪部分”；二者互补，但汇聚仍可能损失远期稀有事件。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户长期爱摄影，近期在准备露营。远期摄影行为可合并保留稳定偏好，最近露营浏览逐条保留；相机候选与帐篷候选再分别激活不同兴趣向量。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.23677">原论文</a> · <a href="../../../../reproductions/2609.23677-muser/">实现解读</a> · <a href="#qa-96e91ee29d96d6b7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mima" data-paper-title="MIMA: Multi-Interest Recommendation via Multi-Positive Exclusive Assignment" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="MIMA: Multi-Interest Recommendation via Multi-Positive Exclusive Assignment 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-09-11 传统多兴趣召回每个训练样本只有一个正例，容易反复更新同一个最相似兴趣并造成 interest collapse。MIMA 把同一请求共同出现的物品视为多正例集合，用 causal decoder 生成多个兴趣，再用 Hungarian matching 强制正例与兴趣一对一监督；routing 模块估计每个兴趣的激活概率，使不同通道的分数可比较。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行多正例分组、一对一最小成本分配、互补兴趣更新和兴趣激活校准；生产 causal Transformer 由公开序列特征替代。公开数据没有生产“同请求多成交”日志，本地以相邻行为组替代；未复刻阿里私有 catalog、生产 causal Transformer checkpoint 和在线召回系统。当前不映射 evolve，避免只有 registry 标签而无可执行候选协议。MovieLens 100K、seeds 42/43/44 的统一结果见 metrics/movielens-100k-seeds42-44.json。  retrieval multi-interest exclusive-assignment industrial-recommendation 搜广推 候选生成与搜索匹配 为什么 MIMA 要把同一请求的多个正例一对一分配给兴趣，而不是让每个正例选择最相似的兴趣？ 独立选择最相似兴趣会让多个正例持续更新同一个通道，其余兴趣得不到监督。MIMA 先构造兴趣与正例的相似度代价矩阵，再求全局最优的一对一匹配，让不同兴趣分别承担正例。激活概率进一步校准通道得分；分工由集合监督产生，不只是增加向量数量。 示意：同一请求有跑鞋、登山包两个正例。若都更新“运动”通道，另一个兴趣闲置；一对一匹配迫使两个通道各解释一个正例，再按激活概率参与召回。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-mima-5191fe9f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-a7737838b5685202">为什么 MIMA 要把同一请求的多个正例一对一分配给兴趣，而不是让每个正例选择最相似的兴趣？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amima">MIMA: Multi-Interest Recommendation via Multi-Positive Exclusive Assignment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立选择最相似兴趣会让多个正例持续更新同一个通道，其余兴趣得不到监督。MIMA 先构造兴趣与正例的相似度代价矩阵，再求全局最优的一对一匹配，让不同兴趣分别承担正例。激活概率进一步校准通道得分；分工由集合监督产生，不只是增加向量数量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一请求有跑鞋、登山包两个正例。若都更新“运动”通道，另一个兴趣闲置；一对一匹配迫使两个通道各解释一个正例，再按激活概率参与召回。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.12842">原论文</a> · <a href="../../../../reproductions/2609.12842-mima/">实现解读</a> · <a href="#qa-a7737838b5685202">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:allecompanion" data-paper-title="Beyond Co-purchase Relation: Evolution of Complementary Recommendations at Allegro" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Beyond Co-purchase Relation: Evolution of Complementary Recommendations at Allegro 搜广推与 LLM 应用 Allegro.com 2026-09-04 共购不等于互补：相机与另一台相机可能经常一起浏览，却不如镜头真正互补。AlleCompanion 先用 ComCat 融合专家规则、人工反馈、LLM 推理和统计挖掘形成类别关系，再用类别约束双塔和 Category Adapter 把候选限制在合理的互补空间。 复现级别：CPU 可训练检索核心。复现级别：CPU 可训练检索核心。共享内容/类别编码器、Category Adapter、混合负样本检索损失和类别重建损失均参与反向传播。MovieLens 邻接关系不是商品互补性，不声称复现 ComCat 或线上效果。ComCat 原始映射、Allegro 行为数据和生产服务未公开；本地实现的是可审计核心机制，不是生产系统复刻。2026-09-08 更正：旧版固定加权打分结果作废。  complementary-recommendation two-tower category-adapter e-commerce 搜广推 候选生成与搜索匹配 为什么有强共现关系的两件商品，仍可能不适合作为互补推荐？ 共现可以来自替代比较或流行度，互补却要求两件商品能共同完成需求。AlleCompanion先用多来源证据建立类别互补关系，再以类别约束双塔与Category Adapter学习具体匹配，避免只按相似或共购打分。推理必须对候选类别进行合法计算，不能提前读取待预测商品类别来选路。 示意：用户比较过两台相机，不代表需要一起买；镜头可能才与相机互补。类别先限定可用配件，再比较具体接口和用途是否匹配。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-allecompanion-f53aba66" class="ar-learning-paper-anchor"></span>
<h2 id="qa-2957cba162130ef2">为什么有强共现关系的两件商品，仍可能不适合作为互补推荐？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aallecompanion">Beyond Co-purchase Relation: Evolution of Complementary Recommendations at Allegro</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Allegro.com</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共现可以来自替代比较或流行度，互补却要求两件商品能共同完成需求。AlleCompanion先用多来源证据建立类别互补关系，再以类别约束双塔与Category Adapter学习具体匹配，避免只按相似或共购打分。推理必须对候选类别进行合法计算，不能提前读取待预测商品类别来选路。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户比较过两台相机，不代表需要一起买；镜头可能才与相机互补。类别先限定可用配件，再比较具体接口和用途是否匹配。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.05063">原论文</a> · <a href="../../../../reproductions/2609.05063-allecompanion/">实现解读</a> · <a href="#qa-2957cba162130ef2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:setmir" data-paper-title="SetMIR: Multi-Interest Retrieval as Set Prediction" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="SetMIR: Multi-Interest Retrieval as Set Prediction 搜广推与 LLM 应用 Snap Inc. 2026-08-31 SetMIR 用 K 个可学习 query 解码无序兴趣集合，Hungarian matching 强制一对一分工以抑制兴趣坍缩；presence head 判断本次请求实际需要哪些兴趣，服务时再用 query-level NMS 删除重复 ANN 请求。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现兴趣集合、presence 门控和 query-level NMS。未复刻私有 DPA 历史、生产 Transformer checkpoint 与 ANN dispatch；仅声明 CPU 公共数据路径。用公开类型簇代理兴趣 query，执行 presence 与相关性 NMS；NDCG@10 从 0.05401 到 0.05665。三 seed 产物见 metrics/public-seeds42-44.json。  multi-interest-retrieval set-prediction dynamic-dispatch 搜广推 候选生成与搜索匹配 SetMIR 为什么训练时用一对一集合匹配，服务时仍要 presence head 和 query NMS？ 匹配监督让多个兴趣查询分工，减少它们都解释同一正例的坍缩，但固定查询数不代表每次请求都有同样多的真实兴趣。presence head 决定哪些查询应激活，NMS 再删除高度重复的检索请求，分别处理训练分工与服务冗余。多兴趣表达丰富并不意味着把所有查询都发出去最有效。 示意：模型最多有八个兴趣，但某次请求只明显有摄影和露营。presence 只启用相关查询，若两个都指向同一种相机，再用 NMS 合并，避免浪费两次近邻检索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-setmir-231692c0" class="ar-learning-paper-anchor"></span>
<h2 id="qa-92167d9dee9cf98d">SetMIR 为什么训练时用一对一集合匹配，服务时仍要 presence head 和 query NMS？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asetmir">SetMIR: Multi-Interest Retrieval as Set Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Snap Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>匹配监督让多个兴趣查询分工，减少它们都解释同一正例的坍缩，但固定查询数不代表每次请求都有同样多的真实兴趣。presence head 决定哪些查询应激活，NMS 再删除高度重复的检索请求，分别处理训练分工与服务冗余。多兴趣表达丰富并不意味着把所有查询都发出去最有效。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型最多有八个兴趣，但某次请求只明显有摄影和露营。presence 只启用相关查询，若两个都指向同一种相机，再用 NMS 合并，避免浪费两次近邻检索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.30251">原论文</a> · <a href="../../../../reproductions/2608.30251-setmir/">实现解读</a> · <a href="#qa-92167d9dee9cf98d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:friend-gnn" data-paper-title="Scaling Graph Neural Networks for Friend Recommendation: Multi-Hash User Embeddings and Temporal Neighbor Sampling" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Scaling Graph Neural Networks for Friend Recommendation: Multi-Hash User Embeddings and Temporal Neighbor Sampling 搜广推与 LLM 应用 AI VK 2026-08-27 超大社交图既放不下完整用户 ID 表，又必须防止采到未来好友边。论文用三个独立 hash 查共享表并拼接投影，以 timestamp-sorted CSR + binary search 得到历史邻居前缀，再由 GATv2 和 query/candidate 双头打分。 Fidelity：核心机制复现。本地执行多哈希共享表、按时间排序邻接与二分 cutoff，并在公开数据上与同候选集基线比较。MovieLens 物品转移图不是好友图；未复刻 VK 私有日志、194M 用户图、分布式 GATv2 和生产 ranker。本地对照口径：基线为相同全候选目录上的 popularity ranker，实验组为 Friend-GNN 时序图 proxy；Hit@10 相对提升 247.62%，仅用于本地机制对照。  friend-recommendation graph-ranking multi-hash-embedding temporal-sampling 搜广推 候选生成与搜索匹配 Friend-GNN为什么既使用多哈希用户表示，又按时间前缀采邻居？ 多哈希共享表减少超大用户词表的存储，但哈希压缩并不解决时间泄漏。时序CSR把邻居按时间排序，查询只允许访问截止点之前的边，再由图网络聚合；否则模型可能通过未来已成好友关系猜中当前推荐。两部分分别控制内存与观测合法性，不能用图分数提高代替这两项检查。 示意：周二推荐好友时不能使用周五才新增的连接；即使用户embedding压缩得很省，采到这条未来边仍会让离线结果失真，因此必须按请求时刻截断邻居。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-friend-gnn-0f3bf9e0" class="ar-learning-paper-anchor"></span>
<h2 id="qa-991287c8e490534e">Friend-GNN为什么既使用多哈希用户表示，又按时间前缀采邻居？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Afriend-gnn">Scaling Graph Neural Networks for Friend Recommendation: Multi-Hash User Embeddings and Temporal Neighbor Sampling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AI VK</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多哈希共享表减少超大用户词表的存储，但哈希压缩并不解决时间泄漏。时序CSR把邻居按时间排序，查询只允许访问截止点之前的边，再由图网络聚合；否则模型可能通过未来已成好友关系猜中当前推荐。两部分分别控制内存与观测合法性，不能用图分数提高代替这两项检查。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>周二推荐好友时不能使用周五才新增的连接；即使用户embedding压缩得很省，采到这条未来边仍会让离线结果失真，因此必须按请求时刻截断邻居。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27413">原论文</a> · <a href="../../../../reproductions/2608.27413-friend-gnn/">实现解读</a> · <a href="#qa-991287c8e490534e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:transretrieval" data-paper-title="TransRetrieval: Scaling Up Transformer-Based Retrieval for Industrial Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="TransRetrieval: Scaling Up Transformer-Based Retrieval for Industrial Recommendation 搜广推与 LLM 应用 Renmin University of China / Taobao &amp; Tmall Group, Alibaba 2026-08-26 跨域广告召回同时受源域噪声、目标域 token 成本和域信息混淆影响。论文按 token norm 聚合源历史，把多个 target tokens 压为一个，并以位置形式注入 domain embedding，减少 target attention 开销。 85% target FLOPs reduction 是结构诊断，不是端到端延迟实测。Fidelity：核心机制复现。本地执行 norm-aware 聚合、target-token 压缩和位置化 domain embedding。未使用论文的 400 亿交互、5200 万广告和生产 ANN；85% target FLOPs reduction 是结构诊断，不是端到端延迟实测。本地对照口径：基线为 Transformer two-tower；实验组加入三项核心机制。MovieLens-1M Hit@10 0.1063 → 0.1187（+11.76%），NDCG@10 0.05429 → 0.05473（+0.81%）。  retrieval transformer-scaling target-token-compression multi-domain 搜广推 候选生成与搜索匹配 TransRetrieval 为什么按 token norm 聚合源域历史，并压缩目标域 token、注入域位置信息？ 源域行为多却可能带噪声，范数加权聚合提供不同于等权平均的信号选择；目标 token 压缩减少跨域注意力成本，域位置信息帮助模型区分相同表示在不同业务中的含义。三项分别控制源噪声、目标计算和域混淆，但高范数不必然等于高相关，压缩也可能损失目标域细节。 示意：阅读域历史迁移到广告召回时，先聚合行为，再把目标侧多种字段压成紧凑表示，同时标明来自哪个域，避免把“收藏文章”和“购买商品”误作相同动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-transretrieval-4252b15a" class="ar-learning-paper-anchor"></span>
<h2 id="qa-246f8113bd997f04">TransRetrieval 为什么按 token norm 聚合源域历史，并压缩目标域 token、注入域位置信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atransretrieval">TransRetrieval: Scaling Up Transformer-Based Retrieval for Industrial Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Renmin University of China / Taobao &amp; Tmall Group, Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>源域行为多却可能带噪声，范数加权聚合提供不同于等权平均的信号选择；目标 token 压缩减少跨域注意力成本，域位置信息帮助模型区分相同表示在不同业务中的含义。三项分别控制源噪声、目标计算和域混淆，但高范数不必然等于高相关，压缩也可能损失目标域细节。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>阅读域历史迁移到广告召回时，先聚合行为，再把目标侧多种字段压成紧凑表示，同时标明来自哪个域，避免把“收藏文章”和“购买商品”误作相同动作。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25528">原论文</a> · <a href="../../../../reproductions/2608.25528-transretrieval/">实现解读</a> · <a href="#qa-246f8113bd997f04">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:spear" data-paper-title="SPEAR: Selection-aware Personalized End-to-end Adaptive Rewriting and Retrieval for Community Search" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="SPEAR: Selection-aware Personalized End-to-end Adaptive Rewriting and Retrieval for Community Search 搜广推与 LLM 应用 Dewu 2026-08-03 端到端改写—检索容易让通用词凭高 path score 胜出、偏离原 query。SPEAR 用双 embedding 和梯度隔离保护 recall 语义，以 rewrite confidence × item relevance 的乘法门消除捷径，再由动态 selector 产生 request-specific 权重、scale 和 bias。 Fidelity：核心机制复现。公开数据只验证论文机制，不模拟生产流量。MovieLens item 内容代理商品/帖子，未复刻得物 query rewrite generator、私有 session 与线上排序链路。本地对照口径：基线为共享 transition + content scorer，实验组只加入 SPEAR 核心机制；相对 NDCG@10 +26.95%。  search query-rewriting retrieval personalization 搜广推 候选生成与搜索匹配 SPEAR 为什么将改写置信度与物品相关性相乘，并隔离召回与排序 embedding 的梯度？ 端到端训练可能让泛化词靠高路径分数取胜，即使它偏离原查询。乘法门要求改写可信且对应物品相关，单项再高也不能轻易走捷径；双表示与梯度隔离保护召回语义不被排序目标任意扭曲。动态 selector 再做请求级校准，仍需检查置信度是否可靠，不能只用一个高总分证明改写正确。 示意：把“防水登山鞋”改成“热门商品”可能得到高点击路径，但改写置信度应低；乘法门压低这条捷径，让真正保留防水需求的改写更有机会。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-spear-7c6c6f8e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-df3bee67260ec58e">SPEAR 为什么将改写置信度与物品相关性相乘，并隔离召回与排序 embedding 的梯度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aspear">SPEAR: Selection-aware Personalized End-to-end Adaptive Rewriting and Retrieval for Community Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dewu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>端到端训练可能让泛化词靠高路径分数取胜，即使它偏离原查询。乘法门要求改写可信且对应物品相关，单项再高也不能轻易走捷径；双表示与梯度隔离保护召回语义不被排序目标任意扭曲。动态 selector 再做请求级校准，仍需检查置信度是否可靠，不能只用一个高总分证明改写正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把“防水登山鞋”改成“热门商品”可能得到高点击路径，但改写置信度应低；乘法门压低这条捷径，让真正保留防水需求的改写更有机会。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01738">原论文</a> · <a href="../../../../reproductions/2608.01738-spear/">实现解读</a> · <a href="#qa-df3bee67260ec58e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:asarl" data-paper-title="ASARL: Autonomous Social-Aware Relevance Learning for QQ Search" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="ASARL: Autonomous Social-Aware Relevance Learning for QQ Search 搜广推与 LLM 应用 Tencent PCG 2026-07-29 QQ 群与频道搜索面对口语化标题、长尾数据和行为漂移。ASARL 用 ReasonAgent 产出 intent–attribute reasoning 与三级相关性标签，CriticAgent 反复校验并检测分布缺口，GenAgent 为长尾区域补样本；随后执行 Social Context Training、基于交互信号的 Preference-Guided Optimization，最后蒸馏到可在线服务的小模型。 Fidelity: 核心机制复现。实际执行多 Agent 数据整理、SCT、偏好优化与 social distillation；闭源 LLM 和 QQ 私有日志未复刻。没有 QQ 私有 query-title 日志、生产 LLM 标注 Agent 或线上 RoBERTa。这里验证的是闭环数据整理、偏好阶段和蒸馏路径；MovieLens genre 代理造成的负迁移被原样保留。本地对照口径：基线与实验组使用同一 MovieLens relevance proxy、student 参数量、训练划分和 seed；实验组增加 Reason/Critic/Gen、PGO 与蒸馏，相对 NDCG@10 为 -72.72%。  search-relevance multi-agent-data-curation knowledge-distillation 搜广推 候选生成与搜索匹配 ASARL中的Critic与GenAgent为什么不能被一次LLM标注替代？ 一次标注可能沿用原数据的偏差并漏掉长尾意图。ReasonAgent提出推理与等级，Critic反复校验并定位分布缺口，GenAgent再补对应样本；随后用交互反馈优化偏好并蒸馏给低延迟学生。补样本必须服务已识别的缺口，不能把未经行为校验的生成理由直接视作真标签。 示意：群名中的口语缩写被误判后，Critic发现某类校园查询持续出错，生成模块补这类对照，而不是均匀增加一批与缺口无关的样本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-asarl-181d0e5f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-2bf061e90f455235">ASARL中的Critic与GenAgent为什么不能被一次LLM标注替代？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aasarl">ASARL: Autonomous Social-Aware Relevance Learning for QQ Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent PCG</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一次标注可能沿用原数据的偏差并漏掉长尾意图。ReasonAgent提出推理与等级，Critic反复校验并定位分布缺口，GenAgent再补对应样本；随后用交互反馈优化偏好并蒸馏给低延迟学生。补样本必须服务已识别的缺口，不能把未经行为校验的生成理由直接视作真标签。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>群名中的口语缩写被误判后，Critic发现某类校园查询持续出错，生成模块补这类对照，而不是均匀增加一批与缺口无关的样本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26593">原论文</a> · <a href="../../../../reproductions/2607.26593-asarl/">实现解读</a> · <a href="#qa-2bf061e90f455235">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:oneshot-index" data-paper-title="OneShot: Index-in-Ranking with Neural Scoring for Large-Scale Retrieval" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="OneShot: Index-in-Ranking with Neural Scoring for Large-Scale Retrieval 搜广推与 LLM 应用 Meta / Instagram 2026-07-29 传统 ANN 索引按 embedding 几何邻近性组织物品，而排序目标直接优化用户行为，两者不一致。OneShot 在模型内共同学习层级索引和排序：前向使用离散路径，反向用 straight-through estimator；全局路径平衡避免热门桶拥塞；候选进入路径后再使用比点积更强的 neural scoring。 Fidelity: 核心机制复现。本地执行 ranking-shaped 分层索引、路径探测和非点积 neural scoring；确定性 assignment 代理生产训练中的 STE 与全局平衡优化。未复刻 Instagram 私有数据、十亿物品多机索引、STE 训练 kernel、SCO 全局平衡与线上检索服务；本地结果不等同论文复现指标。本地对照口径：基线为同数据、同全库评测的 two-tower 点积检索；实验组加入 ranking-shaped 分层索引和 neural scoring，NDCG@10 相对 -7.70%。  retrieval learnable-index neural-scoring serving 搜广推 候选生成与搜索匹配 OneShot 如何让离散层级索引受到排序目标训练，而不只按 embedding 距离分桶？ 前向时物品走离散索引路径，反向用 straight-through 近似把排序损失传回路径分配参数，因此“分到哪个桶”能受到行为目标影响。全局平衡抑制热门路径拥塞，入桶候选再用更强的神经评分。索引与排序共同学习减少目标割裂，但梯度是近似的，桶平衡也不能代替真实相关性。 示意：两个商品文本相似，却面向不同购买人群。几何索引可能把它们放在一起，排序监督则可推动路径分开；同时平衡约束避免所有热门商品挤进同一个桶。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-oneshot-index-d86efe4f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-43a83253198c0a11">OneShot 如何让离散层级索引受到排序目标训练，而不只按 embedding 距离分桶？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aoneshot-index">OneShot: Index-in-Ranking with Neural Scoring for Large-Scale Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta / Instagram</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前向时物品走离散索引路径，反向用 straight-through 近似把排序损失传回路径分配参数，因此“分到哪个桶”能受到行为目标影响。全局平衡抑制热门路径拥塞，入桶候选再用更强的神经评分。索引与排序共同学习减少目标割裂，但梯度是近似的，桶平衡也不能代替真实相关性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个商品文本相似，却面向不同购买人群。几何索引可能把它们放在一起，排序监督则可推动路径分开；同时平衡约束避免所有热门商品挤进同一个桶。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27475">原论文</a> · <a href="../../../../reproductions/2607.27475-oneshot-index/">实现解读</a> · <a href="#qa-43a83253198c0a11">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:core-relevance" data-paper-title="CORE: A Unified Cascaded Ordinal Relevance Estimation Framework for E-commerce Search" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="CORE: A Unified Cascaded Ordinal Relevance Estimation Framework for E-commerce Search 搜广推与 LLM 应用 Meituan / Beijing Institute of Technology 2026-07-27 电商相关性是有序的 High/Mid/Low，但 flat 三分类把三个边界视为对称。CORE 先判断 High vs. Non-High；只有第一步为 Non-High 时才判断 Mid vs. Low，使两个 head 分别专注严格实体/意图匹配和较软的替代性边界。 Fidelity: 核心机制复现。实际执行 flat/cascade 分类、条件 step reward、group-normalized clipped GRPO 和 PostCoT logit 聚合蒸馏；缩小 encoder、数据和 LLM。MovieLens 用户 genre 画像与候选 genre overlap 构造可审计的三级序数标签，替代美团私有 query-item 标注；小型 MLP 替代 Qwen3-14B 与生产 BERT。结果只验证级联、step credit 和 PostCoT 蒸馏链路，不能外推到搜索语义或线上阈值。  search-ranking ordinal-relevance step-grpo llm-distillation 搜广推 候选生成与搜索匹配 CORE为什么先判High与Non-High，再只对Non-High判Mid与Low？ 三档相关性有顺序且边界含义不同，平面三分类会混合严格匹配与宽松替代判断。级联让两个条件头分别专注边界，训练中的逐步奖励也只作用于实际经过的步骤；若已判High，就不应为未执行的Mid/Low步骤制造梯度。蒸馏时须把三类教师概率正确汇总成条件分布。 示意：搜索特定型号时先核对是否精确命中；未命中才区分可替代型号与完全无关商品。不能因为第一步已通过，还要求模型回答一个没必要执行的第二步。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-core-relevance-f3a9a752" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b18203bd21d4b568">CORE为什么先判High与Non-High，再只对Non-High判Mid与Low？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acore-relevance">CORE: A Unified Cascaded Ordinal Relevance Estimation Framework for E-commerce Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan / Beijing Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>三档相关性有顺序且边界含义不同，平面三分类会混合严格匹配与宽松替代判断。级联让两个条件头分别专注边界，训练中的逐步奖励也只作用于实际经过的步骤；若已判High，就不应为未执行的Mid/Low步骤制造梯度。蒸馏时须把三类教师概率正确汇总成条件分布。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>搜索特定型号时先核对是否精确命中；未命中才区分可替代型号与完全无关商品。不能因为第一步已通过，还要求模型回答一个没必要执行的第二步。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24417">原论文</a> · <a href="../../../../reproductions/2607.24417-core-relevance/">实现解读</a> · <a href="#qa-b18203bd21d4b568">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:melo" data-paper-title="Melo: A Production LLM-Powered Music Recommendation Agent" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Melo: A Production LLM-Powered Music Recommendation Agent 搜广推与 LLM 应用 NetEase Cloud Music / Zhejiang University of Technology 2026-07-26 用多节点 Agent 编排意图、检索、推荐与解释，以实体目录 grounding 阻止幻觉，并在失败时触发反思重试。 Fidelity: 核心机制复现。本地执行意图路由、grounded 检索与失败反思重试；不把公开代理环境冒充网易云音乐生产系统。无法隔离论文系统 A/B 中模型、产品面和 UI 的贡献，论文也未给置信区间；本站明确保留该归因限制。本地对照口径：基线为无运行时修复的 catalog recommender，实验组为 grounding + retry；Hit@10 -20.00%、NDCG@10 -8.16%，fresh Hit@10 +50.00%。  llm-recommendation agent entity-grounding reflection 搜广推 候选生成与搜索匹配 Melo为什么必须在推荐后做实体grounding，并在失败时反思重试？ 语言模型能生成合理的音乐描述，却可能给出不存在或名称不一致的实体。grounding把输出映射到真实目录，验证后才进入推荐结果；反思重试利用失败原因修正意图或检索，而非任意换一份列表。合法实体也未必符合偏好，修复成功率和推荐质量需要分别观察。 示意：模型写出一首听起来像真的歌，目录却找不到；系统应回到意图和检索节点修正，而不是把相似名称强行当成成功，也不能因歌名合法就认定用户会喜欢。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-melo-f661791b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-8e338a94d4aae060">Melo为什么必须在推荐后做实体grounding，并在失败时反思重试？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amelo">Melo: A Production LLM-Powered Music Recommendation Agent</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NetEase Cloud Music / Zhejiang University of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语言模型能生成合理的音乐描述，却可能给出不存在或名称不一致的实体。grounding把输出映射到真实目录，验证后才进入推荐结果；反思重试利用失败原因修正意图或检索，而非任意换一份列表。合法实体也未必符合偏好，修复成功率和推荐质量需要分别观察。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型写出一首听起来像真的歌，目录却找不到；系统应回到意图和检索节点修正，而不是把相似名称强行当成成功，也不能因歌名合法就认定用户会喜欢。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.23718">原论文</a> · <a href="../../../../reproductions/2607.23718-melo/">实现解读</a> · <a href="#qa-8e338a94d4aae060">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mesh" data-paper-title="MESH: Scaling Up Retrieval with Heterogeneous Content Unification" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="MESH: Scaling Up Retrieval with Heterogeneous Content Unification 搜广推与 LLM 应用 Pinterest 2026-07-14 统一放大 flat retrieval 容易让高频 evergreen 梯度淹没 fresh/tail 信号。MESH 先把 user/item/context 分到独立 sub-tower，各自在全局交互前用 residual crossing 放大；RGBC 再用 context gate 调节纯 user-item affinity，服务端可并行各塔并异步缓存 item tower。 Fidelity: 核心机制复现。分组 manifold、独立 residual signal amplifier、全局 crossing 与 RGBC 均实际执行。未复刻 DHEN 全算子与生产 GPU inter-op；不引用本地微基准支持论文吞吐结论。本地对照口径：基线是 flat retrieval；实验组 MESH 使用三塔放大与 RGBC，验证集选 blend 0.1，相对基线 Hit@10 +0.00%、NDCG@10 -3.54%。  retrieval fresh-content serving 搜广推 候选生成与搜索匹配 MESH为什么先分别放大user、item、context子塔，再做全局交互？ 过早平铺所有输入，常见内容的强梯度可能掩盖新鲜和长尾信号。独立子塔先在各自空间做残差交叉，保留专门容量，再用context gate调节用户—物品亲和力，使交互受请求语境影响。可缓存item子塔并不代表最终打分完全解耦，后续候选相关计算仍需按实际服务路径核算。 示意：长尾商品的内容特征先有独立建模空间，不必一开始就与热门曝光统计竞争同一层；随后在当前场景中再判断用户与该商品的匹配程度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-mesh-881b1237" class="ar-learning-paper-anchor"></span>
<h2 id="qa-23bf7dbdc9d448ab">MESH为什么先分别放大user、item、context子塔，再做全局交互？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amesh">MESH: Scaling Up Retrieval with Heterogeneous Content Unification</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>过早平铺所有输入，常见内容的强梯度可能掩盖新鲜和长尾信号。独立子塔先在各自空间做残差交叉，保留专门容量，再用context gate调节用户—物品亲和力，使交互受请求语境影响。可缓存item子塔并不代表最终打分完全解耦，后续候选相关计算仍需按实际服务路径核算。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>长尾商品的内容特征先有独立建模空间，不必一开始就与热门曝光统计竞争同一层；随后在当前场景中再判断用户与该商品的匹配程度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12392">原论文</a> · <a href="../../../../reproductions/2607.12392-mesh/">实现解读</a> · <a href="#qa-23bf7dbdc9d448ab">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:zorro" data-paper-title="ZoRRO: A Zero-Weight Personalized Recommender System for Scalable News Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="ZoRRO: A Zero-Weight Personalized Recommender System for Scalable News Recommendation 搜广推与 LLM 应用 Technical University of Denmark 2026-07-12 不用模型训练，直接融合历史文章的时间衰减、语义相似度和类别关系，面向高吞吐新闻候选排序。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 ZoRRO 为 0.05201，相对变化 -3.70%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  news-recommendation training-free recency 搜广推 候选生成与搜索匹配 ZoRRO 为什么无需模型训练也能做候选排序，又在哪些信息上受限？ 它直接用历史的时间衰减、语义相似与类别关系组合候选得分，偏好规则与内容向量足以构成可运行排序器，省去参数拟合和训练更新。新历史可立即改变权重，但组合关系由设计固定，难自动学习复杂协同与用户差异。适合检验轻量规则价值，不能把无训练误解为没有特征、超参数或数据依赖。 示意：用户刚读多篇科技新闻，最近文章权重更高，语义相近且同类候选得分上升。系统能立刻响应，但无法自行学出“某用户周末更想看文化内容”的复杂规律。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-zorro-2da90bec" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f97bf40ce835734e">ZoRRO 为什么无需模型训练也能做候选排序，又在哪些信息上受限？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Azorro">ZoRRO: A Zero-Weight Personalized Recommender System for Scalable News Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Technical University of Denmark</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它直接用历史的时间衰减、语义相似与类别关系组合候选得分，偏好规则与内容向量足以构成可运行排序器，省去参数拟合和训练更新。新历史可立即改变权重，但组合关系由设计固定，难自动学习复杂协同与用户差异。适合检验轻量规则价值，不能把无训练误解为没有特征、超参数或数据依赖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户刚读多篇科技新闻，最近文章权重更高，语义相近且同类候选得分上升。系统能立刻响应，但无法自行学出“某用户周末更想看文化内容”的复杂规律。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.10910">原论文</a> · <a href="../../../../reproductions/2607.10910-zorro/">实现解读</a> · <a href="#qa-f97bf40ce835734e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:elise" data-paper-title="Multilingual Semantic Retrieval for Apple Music Search" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Multilingual Semantic Retrieval for Apple Music Search 搜广推与 LLM 应用 Apple 2026-07-11 Siamese bi-encoder 补充词法倒排，再用分位数分布匹配把 dense 与 token score 校准到同一尺度并限制语义结果数量。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 ELISE 为 0.04739，相对变化 -12.24%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  search multilingual-retrieval score-calibration 搜广推 候选生成与搜索匹配 ELISE为什么先做分位数匹配，再融合语义召回和词法检索分数？ 两种模型的原始分数尺度和分布不同，直接加权可能让数值范围较大的一路支配结果。分位数映射先表达各自分布中的相对位置，再进行受控融合并限制语义结果数量。百分位不是校准点击概率，也不能替代对精确实体匹配的检查；跨语言分布变化后映射同样可能需要更新。 示意：词法分常在几十，向量相似度在零到一，直接相加几乎只看词法；映射到各自百分位后才可公平组合，同时保留精确歌名匹配的控制。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-elise-a73bc968" class="ar-learning-paper-anchor"></span>
<h2 id="qa-67a17072942f12de">ELISE为什么先做分位数匹配，再融合语义召回和词法检索分数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aelise">Multilingual Semantic Retrieval for Apple Music Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Apple</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两种模型的原始分数尺度和分布不同，直接加权可能让数值范围较大的一路支配结果。分位数映射先表达各自分布中的相对位置，再进行受控融合并限制语义结果数量。百分位不是校准点击概率，也不能替代对精确实体匹配的检查；跨语言分布变化后映射同样可能需要更新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>词法分常在几十，向量相似度在零到一，直接相加几乎只看词法；映射到各自百分位后才可公平组合，同时保留精确歌名匹配的控制。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.10239">原论文</a> · <a href="../../../../reproductions/2607.10239-elise/">实现解读</a> · <a href="#qa-67a17072942f12de">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cluster-goobs" data-paper-title="Real-Time Hard Negative Sampling via LLM-based Clustering for Large-Scale Two-Tower Retrieval" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Real-Time Hard Negative Sampling via LLM-based Clustering for Large-Scale Two-Tower Retrieval 搜广推与 LLM 应用 Meta 2026-07-01 大规模双塔召回常从 out-of-batch（OOB）池随机抽负例。绝大多数负例过于容易，梯度弱；同时热门物品更常进入池，形成曝光反馈循环。论文先用 LLM/多模态 embedding 把物品划入语义 cluster，再让 GOOBS 的 update engine 按 cluster 分段写入实时 OOB 池，sample engine 大概率从正例所在 cluster 抽 hard negative。这样不增加在线模型结构，采样仍是 O(1)。 Fidelity: 核心机制复现。cluster-conditioned online hard-negative sampler 实际执行；MovieLens genre 替换私有 LLM 多模态 cluster，分布式 GOOBS serving 未复刻。本地对照口径：基线是 Random OOB negative sampler；实验组是 Cluster GOOBS sampler；NDCG@10 +0.98%、head share -1.81%。这是负采样策略消融，不是完整双塔相对 DIN 的比较。   搜广推 候选生成与搜索匹配 Cluster GOOBS为什么大概率在正例所在语义簇里抽负例，又保留随机负例？ 同簇物品在内容上接近，更可能落在模型真实选择边界，能避免大部分随机负例太容易。保留少量随机采样则提供全局覆盖，减轻只学簇内区分的局限。核心变化在实时OOB池的分段更新与采样分布，而非给线上双塔再加一个LLM；同簇物品也可能是假负例，比例需验证。 示意：正例是跑鞋时，与另一款跑鞋比较比与冰箱比较更难；偶尔仍抽跨类物品，避免模型只会区分鞋款，却不知道鞋和家电的整体差异。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-cluster-goobs-3f572e40" class="ar-learning-paper-anchor"></span>
<h2 id="qa-6937b4d52e6ff1ef">Cluster GOOBS为什么大概率在正例所在语义簇里抽负例，又保留随机负例？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acluster-goobs">Real-Time Hard Negative Sampling via LLM-based Clustering for Large-Scale Two-Tower Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同簇物品在内容上接近，更可能落在模型真实选择边界，能避免大部分随机负例太容易。保留少量随机采样则提供全局覆盖，减轻只学簇内区分的局限。核心变化在实时OOB池的分段更新与采样分布，而非给线上双塔再加一个LLM；同簇物品也可能是假负例，比例需验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>正例是跑鞋时，与另一款跑鞋比较比与冰箱比较更难；偶尔仍抽跨类物品，避免模型只会区分鞋款，却不知道鞋和家电的整体差异。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.00448">原论文</a> · <a href="../../../../reproductions/2607.00448-cluster-goobs/">实现解读</a> · <a href="#qa-6937b4d52e6ff1ef">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:next-vlm" data-paper-title="NEXT: Reasoning-Driven Video Recommendation via a Vision-Language Model" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="NEXT: Reasoning-Driven Video Recommendation via a Vision-Language Model 搜广推与 LLM 应用 Meta 2026-06-27 共现和语义相似只能回答“哪些视频相近”，难以推断用户看完当前视频后下一步想做什么。NEXT 先识别显式续集；对隐式关系让 NEXT-8B VLM 生成 next-intent query，再检索并验证候选，形成 directed Next Knowledge Graph。推理放在离线，线上只在用户正反馈后注入高置信边，避免把 8B VLM 放进请求链路。 这是公开代理任务的单 seed 诊断结果，不是 Meta 线上收益复现。Fidelity: 核心机制复现。本地执行 item→intent→item、离线 directed edge 生成/验证和线上加性注入；没有把规则或 embedding 代理写成“训练了 NEXT-8B”。本地用电影标题/genre 和协同转移代理视觉语义与 VLM 验证；未训练 8B VLM、GRPO/SFT 偏好阶段，也没有短视频画面、私有安全模型和实时 serving。本地对照口径：基线为同数据的 transition+semantic 多路径 ranker；  multimodal reasoning retrieval knowledge-graph vlm 搜广推 候选生成与搜索匹配 NEXT 为什么先生成 next-intent 再检索和验证，而不直接连接语义最相似的视频？ 语义相似描述内容接近，未必描述用户看完后的下一步需求。NEXT 用视觉语言模型从当前视频推断后续意图，再检索满足该意图的候选并验证，形成有方向的边。昂贵推理离线执行，在线在正反馈后注入高置信连接；因此图表达的是可能的后续关系，而非无方向的内容相似网络。 示意：看完“咖啡机开箱”后，下一需求可能是“如何萃取”，未必是另一条开箱。先生成这个后续意图，再检索教学视频，便能产生开箱到使用教程的有向边。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-next-vlm-e4f6498d" class="ar-learning-paper-anchor"></span>
<h2 id="qa-7f831990d7e747ab">NEXT 为什么先生成 next-intent 再检索和验证，而不直接连接语义最相似的视频？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Anext-vlm">NEXT: Reasoning-Driven Video Recommendation via a Vision-Language Model</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语义相似描述内容接近，未必描述用户看完后的下一步需求。NEXT 用视觉语言模型从当前视频推断后续意图，再检索满足该意图的候选并验证，形成有方向的边。昂贵推理离线执行，在线在正反馈后注入高置信连接；因此图表达的是可能的后续关系，而非无方向的内容相似网络。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>看完“咖啡机开箱”后，下一需求可能是“如何萃取”，未必是另一条开箱。先生成这个后续意图，再检索教学视频，便能产生开箱到使用教程的有向边。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24789">原论文</a> · <a href="../../../../reproductions/2607.24789-next-vlm/">实现解读</a> · <a href="#qa-7f831990d7e747ab">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rankgraph2" data-paper-title="RankGraph-2: Lifecycle Co-Design for Billion-Node Graph Learning in Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="RankGraph-2: Lifecycle Co-Design for Billion-Node Graph Learning in Recommendation 搜广推与 LLM 应用 Meta 2026-06-16 直接在线跑多层 GNN 成本高且易受热门边支配。RankGraph-2 对边做 popularity correction，离线预计算多跳 PPR，再用共同学习的 residual/cluster index 压缩服务。 复现保真度：核心机制复现。复现保真度：核心机制复现。流行度校正、离线 PPR 和 cluster index 均实际执行。MovieLens item graph 上真实执行去偏转移、多跳 PPR 与 PPR 表征聚类索引。  graph-retrieval ppr residual-quantization 搜广推 候选生成与搜索匹配 RankGraph-2 为什么先校正热门边再离线计算多跳 PPR，而不在线堆更深 GNN？ 多跳传播能发现间接关系，但热门节点容易吸走大量概率，在线逐层图计算也昂贵。先按流行度校正转移，再离线求个性化 PageRank，可把去偏多跳关系预先写入表示；残差与聚类索引进一步压缩服务。校正改变传播偏好，并不保证消除全部曝光偏差，离线图也需随数据更新。 示意：所有用户都看过一部大片时，它可能把很多无关电影连在一起。降低通向热门节点的传播权重后，再计算多跳邻近，更有机会保留小众但相关的关联。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-rankgraph2-ef314ec2" class="ar-learning-paper-anchor"></span>
<h2 id="qa-ac6d4c7748c03d76">RankGraph-2 为什么先校正热门边再离线计算多跳 PPR，而不在线堆更深 GNN？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arankgraph2">RankGraph-2: Lifecycle Co-Design for Billion-Node Graph Learning in Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多跳传播能发现间接关系，但热门节点容易吸走大量概率，在线逐层图计算也昂贵。先按流行度校正转移，再离线求个性化 PageRank，可把去偏多跳关系预先写入表示；残差与聚类索引进一步压缩服务。校正改变传播偏好，并不保证消除全部曝光偏差，离线图也需随数据更新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>所有用户都看过一部大片时，它可能把很多无关电影连在一起。降低通向热门节点的传播权重后，再计算多跳邻近，更有机会保留小众但相关的关联。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.18379">原论文</a> · <a href="../../../../reproductions/2606.18379-rankgraph2/">实现解读</a> · <a href="#qa-ac6d4c7748c03d76">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:toolrec" data-paper-title="ToolRec: Calibrated Preference Alignment for Query Recommendation in On-Device Assistants" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="ToolRec: Calibrated Preference Alignment for Query Recommendation in On-Device Assistants 搜广推与 LLM 应用 Huazhong University of Science and Technology 2026-06-07 在 KTO 式偏好目标上同时加入用户侧校准与工具频率驱动的动态系统侧校准，提升会触发工具的查询，同时约束上下文相关性下降。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04819，相对变化 -10.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。  query-recommendation preference-alignment tool-use 搜广推 候选生成与搜索匹配 ToolRec 为什么同时校准用户偏好与系统工具频率，而不只奖励触发工具？ 只奖励工具调用容易让模型对不相关请求也强行调用，单看用户侧偏好又可能忽略工具在系统中的供需失衡。双侧校准分别约束用户相关性与工具频率，动态系统权重调节偏好目标，让适合的查询更易触发工具。频率是治理信号而非质量本身，必须同时检查上下文相关性是否下降。 示意：用户问实时航班时适合查工具，问概念定义时未必需要。即使某工具使用率偏低，也不能为了拉高频次让所有问题都调用它，用户侧校准应约束这种倾向。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-toolrec-2caef440" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b4bbc0c6ac0744e7">ToolRec 为什么同时校准用户偏好与系统工具频率，而不只奖励触发工具？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atoolrec">ToolRec: Calibrated Preference Alignment for Query Recommendation in On-Device Assistants</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huazhong University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只奖励工具调用容易让模型对不相关请求也强行调用，单看用户侧偏好又可能忽略工具在系统中的供需失衡。双侧校准分别约束用户相关性与工具频率，动态系统权重调节偏好目标，让适合的查询更易触发工具。频率是治理信号而非质量本身，必须同时检查上下文相关性是否下降。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户问实时航班时适合查工具，问概念定义时未必需要。即使某工具使用率偏低，也不能为了拉高频次让所有问题都调用它，用户侧校准应约束这种倾向。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.08466">原论文</a> · <a href="../../../../reproductions/2606.08466-toolrec/">实现解读</a> · <a href="#qa-b4bbc0c6ac0744e7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:harness-lm" data-paper-title="HARNESS-LM: A Three-Phase Training Recipe for Harnessing SLMs in Sponsored Search Retrieval" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="HARNESS-LM: A Three-Phase Training Recipe for Harnessing SLMs in Sponsored Search Retrieval 搜广推与 LLM 应用 Microsoft AI / Bing Ads 2026-05-22 Sponsored Search 可以离线使用昂贵文档编码器，却要求在线 query encoder 足够小。HARNESS-LM 先训练强 teacher，再让小 query encoder 直接对齐 teacher query 空间，最后冻结 teacher 文档塔做监督对比精修，避免重建索引。 Fidelity: 核心机制复现。Teacher、L2 embedding alignment、冻结 teacher document index 的 contrastive refinement 三阶段均实际执行。协同 SVD+内容代理 Qwen3-Embedding teacher；未复刻 4B/0.6B 规模、GPT expansion 与 CPU pruning frontier。本地对照口径：基线是小型对称内容 retriever；实验组 HARNESS-LM 使用强协同文档空间、L2 对齐与对比精修，相对基线 Hit@10 -23.08%、NDCG@10 -28.05%。  llm-recommendation retrieval distillation 搜广推 候选生成与搜索匹配 HARNESS-LM精修时为什么冻结强文档塔，只训练小query encoder？ 文档向量可以提前离线计算，在线请求侧却需要轻量且低延迟。小查询塔先对齐teacher查询空间，再在固定文档空间里用对比监督精修，避免一边训练一边让索引坐标漂移、反复重建全库。冻结减少部署变化，也限制目标域适应能力，不能默认小模型必然达到teacher质量。 示意：已有百万广告向量由强文档塔建好，小查询塔只需学会在这套坐标里找对象；若同时更新文档塔，旧索引可能失效，部署成本远不止查询模型变小。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-harness-lm-9919eb79" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d02a310dcb03bd2f">HARNESS-LM精修时为什么冻结强文档塔，只训练小query encoder？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aharness-lm">HARNESS-LM: A Three-Phase Training Recipe for Harnessing SLMs in Sponsored Search Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft AI / Bing Ads</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档向量可以提前离线计算，在线请求侧却需要轻量且低延迟。小查询塔先对齐teacher查询空间，再在固定文档空间里用对比监督精修，避免一边训练一边让索引坐标漂移、反复重建全库。冻结减少部署变化，也限制目标域适应能力，不能默认小模型必然达到teacher质量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>已有百万广告向量由强文档塔建好，小查询塔只需学会在这套坐标里找对象；若同时更新文档塔，旧索引可能失效，部署成本远不止查询模型变小。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.23572">原论文</a> · <a href="../../../../reproductions/2605.23572-harness-lm/">实现解读</a> · <a href="#qa-d02a310dcb03bd2f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:llm-ad-retrieval" data-paper-title="LLM Retrieval for Stable and Predictable Ad Recommendations" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="LLM Retrieval for Stable and Predictable Ad Recommendations 搜广推与 LLM 应用 Meta 2026-05-21 广告候选生成通常只优化点击/转化预测与 Recall，轻微修改 creative 后却可能因为 ID 或稀疏特征变化而得到完全不同的投放结果。论文新增 A/A&#x27; predictability 框架：复制 primary ad 为 shadow ad，只做不改变语义的输入扰动，再衡量两者转换和曝光差异。模型侧用经过广告检索任务适配的 LLM 从标题、描述等 creative 中抽取层级 category、brand、product 和 context 属性； Fidelity: 核心机制复现。本地实际执行成对 creative 的领域 SFT、LLM hidden-state 属性头、层级离散语义表示、phrase→token 两级 Jaccard 建图、协同图融合、validation 选权重，以及扰动稳定性评估；未复刻 Meta 私有广告语料、Llama-3-8B、分布式推理、线上转换与 shadow-ad 流量系统。本地对照口径：基线是 Collaborative Item Graph；实验组是在固定候选预算下加入 LLM Semantic Graph；Recall@20 +11.90%、NDCG@20 +3.03%，边分数漂移 -77.36%。  llm-recommendation retrieval stability 搜广推 候选生成与搜索匹配 LLM广告召回为什么增加A/A′可预测性检查，而不只看Recall？ 语义几乎不变的创意轻微改动可能因ID与稀疏信号导致投放剧烈变化，Recall却未必暴露这种不稳定。primary与shadow对照衡量扰动后的转换和曝光差异；层级语义属性与广告图提供较可迁移的召回关系。稳定性评价仍需控制统计噪声，不能把任何小样本差异都判为模型失效。 示意：广告只换了不改变产品含义的措辞，却几乎失去曝光，普通命中率可能仍很好；复制对照能专门检查系统是否对这种语义等价变化过度敏感。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-llm-ad-retrieval-68e38a71" class="ar-learning-paper-anchor"></span>
<h2 id="qa-a8d03d3e65df1df8">LLM广告召回为什么增加A/A′可预测性检查，而不只看Recall？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Allm-ad-retrieval">LLM Retrieval for Stable and Predictable Ad Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语义几乎不变的创意轻微改动可能因ID与稀疏信号导致投放剧烈变化，Recall却未必暴露这种不稳定。primary与shadow对照衡量扰动后的转换和曝光差异；层级语义属性与广告图提供较可迁移的召回关系。稳定性评价仍需控制统计噪声，不能把任何小样本差异都判为模型失效。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>广告只换了不改变产品含义的措辞，却几乎失去曝光，普通命中率可能仍很好；复制对照能专门检查系统是否对这种语义等价变化过度敏感。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.21969">原论文</a> · <a href="../../../../reproductions/2605.21969-llm-ad-retrieval/">实现解读</a> · <a href="#qa-a8d03d3e65df1df8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mdcns" data-paper-title="Divergence Meets Consensus: A Multi-Source Negative Sampling Framework for Sequential Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Divergence Meets Consensus: A Multi-Source Negative Sampling Framework for Sequential Recommendation 搜广推与 LLM 应用 论文作者团队（原文未标注公司） 2026-05-19 随机负采样太容易，DNS 只追逐单模型高分负例又容易产生 false negative、低多样性和模型偏置。MDCNS 受“最近发展区”启发，引入 Self、Peer、Teacher 三个视角：Self 与异构 Peer 分别评分，Teacher 聚合两者；再用两模型分歧提升“困难且有信息量”的候选，最后把 Teacher 在完整候选池上的分布蒸馏回 Self，避免候选打分只利用一个负例。 Fidelity: 核心机制复现。三源负采样、双模型分歧/共识选择与更新实际执行；推荐 backbone 缩小为本地可训练模型。本地对照口径：主基线是 Uniform negative sampling，辅助基线是 DNS；实验组是 MDCNS；NDCG@10 相对 Uniform 从 0.003016 升至 0.006175（+104.75%）。这是采样策略消融；DIN 不适用于该采样器级比较。   搜广推 候选生成与搜索匹配 MDCNS为什么同时看Self与Peer分歧，而不是永远选择Self分最高的负例？ 单模型高分可能只是自身偏置或潜在正例，始终追它会降低多样性。异构Peer提供另一视角，分歧帮助识别值得学习的候选，Teacher再把完整候选池关系蒸馏回Self，避免只利用一个负例。分歧不等于标签为负的证据，采样仍需控制假负例风险与训练稳定性。 示意：Self把某类热门商品都打高，Peer并不认同；只按Self挖负例会重复其偏见，多视角可暴露这种不确定性，但不能断言所有分歧商品都不相关。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-mdcns-8e8ced60" class="ar-learning-paper-anchor"></span>
<h2 id="qa-451af1c0d313f3a2">MDCNS为什么同时看Self与Peer分歧，而不是永远选择Self分最高的负例？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amdcns">Divergence Meets Consensus: A Multi-Source Negative Sampling Framework for Sequential Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文作者团队（原文未标注公司）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单模型高分可能只是自身偏置或潜在正例，始终追它会降低多样性。异构Peer提供另一视角，分歧帮助识别值得学习的候选，Teacher再把完整候选池关系蒸馏回Self，避免只利用一个负例。分歧不等于标签为负的证据，采样仍需控制假负例风险与训练稳定性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>Self把某类热门商品都打高，Peer并不认同；只按Self挖负例会重复其偏见，多视角可暴露这种不确定性，但不能断言所有分歧商品都不相关。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.19651">原论文</a> · <a href="../../../../reproductions/2605.19651-mdcns/">实现解读</a> · <a href="#qa-451af1c0d313f3a2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:policy-facet" data-paper-title="Policy-Grounded Dynamic Facet Suggestions for Job Search" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Policy-Grounded Dynamic Facet Suggestions for Job Search 搜广推与 LLM 应用 LinkedIn 2026-05-15 先由人工与 LLM 维护符合产品策略的 facet taxonomy，再用 embedding SLM 召回候选，以生成式 SLM 做单 token 点式评分；前缀缓存和批处理满足实时延迟。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04713，相对变化 -12.73%。本地代理目标与论文生产任务不同，不能外推线上 lift。  job-search facet-retrieval policy-ranking 搜广推 候选生成与搜索匹配 Policy Facet 为什么先维护受产品策略约束的分类，再用小模型召回和单 token 评分？ 受维护的 facet 集合先限定可推荐的主题边界，避免生成器随意提出不符合策略的选项。嵌入模型在集合内低成本召回，生成式小模型再根据用户与查询输出“Okay”等单 token 的概率评分。它把开放生成转为受控候选判断，并用缓存和批处理降延迟；概率高仍不等于策略已经自动完备。 示意：搜索亲子旅行时，系统只从经过维护的目的地与活动主题里选候选，再判断哪些最适合当前查询。模型不需要现场编造新的分类名称，也更便于检查推荐范围。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-policy-facet-10555aa9" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1a873ae567d00c7d">Policy Facet 为什么先维护受产品策略约束的分类，再用小模型召回和单 token 评分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apolicy-facet">Policy-Grounded Dynamic Facet Suggestions for Job Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>受维护的 facet 集合先限定可推荐的主题边界，避免生成器随意提出不符合策略的选项。嵌入模型在集合内低成本召回，生成式小模型再根据用户与查询输出“Okay”等单 token 的概率评分。它把开放生成转为受控候选判断，并用缓存和批处理降延迟；概率高仍不等于策略已经自动完备。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>搜索亲子旅行时，系统只从经过维护的目的地与活动主题里选候选，再判断哪些最适合当前查询。模型不需要现场编造新的分类名称，也更便于检查推荐范围。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.16479">原论文</a> · <a href="../../../../reproductions/2605.16479-policy-facet/">实现解读</a> · <a href="#qa-1a873ae567d00c7d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cs3" data-paper-title="CS3: Efficient Online Capability Synergy for Two-Tower Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="CS3: Efficient Online Capability Synergy for Two-Tower Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-04-21 传统双塔为 ANN 解耦 user/item 表征，牺牲交叉能力。CS3 通过离线/在线可部署的循环修正和知识协同增强塔间交互。 三 seed NDCG@10 相对 -16.06%，当前小数据未复现线上收益。Fidelity: 核心机制复现。实现双塔间的循环自修正、显式交叉同步与级联教师辅助目标。没有 4 亿 DAU 的在线缓存、EMA 跨塔向量和生产 QPS 链路。本地对照口径：基线是 matched two-tower；实验组加入 cycle、cross sync 与 teacher loss；三 seed NDCG@10 相对 -16.06%，当前小数据未复现线上收益。  retrieval two-tower online-learning 搜广推 候选生成与搜索匹配 CS3想增强双塔交互，为什么不能直接把候选向量写回所有共享用户表示？ 双塔高效检索依赖用户与物品表征可分别计算，一旦用户表示依赖具体候选，就不能直接用同一向量检索全库。CS3以可部署的循环修正和知识协同增强交互，需要明确哪些更新可离线物化、哪些仍随候选变化。不能把训练时可用的强交互路径直接当成免费ANN服务能力。 示意：给用户向量加入商品A的细节后，它可能更擅长评A，却不再是检索商品B、C的同一查询；修正必须有清楚的缓存和在线执行边界。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-cs3-e2cd1a82" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1f1f4ef09f0f9947">CS3想增强双塔交互，为什么不能直接把候选向量写回所有共享用户表示？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acs3">CS3: Efficient Online Capability Synergy for Two-Tower Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>双塔高效检索依赖用户与物品表征可分别计算，一旦用户表示依赖具体候选，就不能直接用同一向量检索全库。CS3以可部署的循环修正和知识协同增强交互，需要明确哪些更新可离线物化、哪些仍随候选变化。不能把训练时可用的强交互路径直接当成免费ANN服务能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>给用户向量加入商品A的细节后，它可能更擅长评A，却不再是检索商品B、C的同一查询；修正必须有清楚的缓存和在线执行边界。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.19269">原论文</a> · <a href="../../../../reproductions/2604.19269-cs3/">实现解读</a> · <a href="#qa-1f1f4ef09f0f9947">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hill-index" data-paper-title="Efficient Retrieval Scaling with Hierarchical Indexing for Large Scale Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Efficient Retrieval Scaling with Hierarchical Indexing for Large Scale Recommendation 搜广推与 LLM 应用 Meta / Facebook and Instagram Ads 2026-04-14 大型 retrieval foundation model 若对全部 user-item pair 执行复杂 interaction tower，线上成本不可接受。HILL 不再独立地按 item embedding 建 ANN，而是让 MoNN 的用户、item 与交互信号参与 index-node 学习；第一层用 attention-style soft assignment，下一层量化上一层未解释的 residual。 Fidelity: 核心机制复现。本地执行 soft assignment、跨层 residual quantization、层级 beam retrieval 与固定公开切分评测；不是把离线 k-means 树直接命名为 HILL。本地没有 MoNN 的千级特征、多任务半监督训练、Meta Ads 十亿级索引、FAISS EM 和真实 QPS；中间节点数量只作为公开的 TTT-data proxy，未宣称完成线上 test-time training。  retrieval hierarchical-index residual-quantization test-time-training serving 搜广推 候选生成与搜索匹配 HILL为什么学习索引节点时也让用户与交互塔参与，而不只对item向量聚类？ 普通索引主要保持item几何近邻，未必与复杂交互模型的选择目标一致。HILL让节点作为可训练替代表示进入用户—物品交互，再用下一层残差补足上层未表达信息，使粗细索引共同服务检索。层级beam仍可能漏掉路径，少量test-time样本也不能用隔离测试答案来挑选或更新。 示意：两个商品内容向量很近，却被不同人群偏好；只按item距离可能分到同桶，交互驱动的节点学习可让索引更贴近实际用户选择，再逐层缩小候选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-hill-index-46d50ccf" class="ar-learning-paper-anchor"></span>
<h2 id="qa-0781092bdcfe4d94">HILL为什么学习索引节点时也让用户与交互塔参与，而不只对item向量聚类？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahill-index">Efficient Retrieval Scaling with Hierarchical Indexing for Large Scale Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta / Facebook and Instagram Ads</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>普通索引主要保持item几何近邻，未必与复杂交互模型的选择目标一致。HILL让节点作为可训练替代表示进入用户—物品交互，再用下一层残差补足上层未表达信息，使粗细索引共同服务检索。层级beam仍可能漏掉路径，少量test-time样本也不能用隔离测试答案来挑选或更新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个商品内容向量很近，却被不同人群偏好；只按item距离可能分到同桶，交互驱动的节点学习可让索引更贴近实际用户选择，再逐层缩小候选。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.12965">原论文</a> · <a href="../../../../reproductions/2604.12965-hill-index/">实现解读</a> · <a href="#qa-0781092bdcfe4d94">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:genfacet" data-paper-title="GenFacet: End-to-End Generative Faceted Search via Multi-Task Preference Alignment in E-Commerce" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="GenFacet: End-to-End Generative Faceted Search via Multi-Task Preference Alignment in E-Commerce 搜广推与 LLM 应用 JD.com 2026-03-20 GenFacet 把电商分面搜索统一为上下文分面生成与意图驱动 query 改写两个生成任务，并以教师蒸馏加 GRPO 的多任务偏好对齐直接优化下游搜索满意度，闭合“分面选择—检索”链路。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05171，相对变化 -4.26%。本地代理目标与论文生产任务不同，不能外推线上 lift。  e-commerce-search facet-generation preference-alignment 搜广推 候选生成与搜索匹配 GenFacet为什么把分面生成和query改写一起按下游检索反馈优化？ 分面文本看起来合理，不一定能带来可用搜索结果；选定分面后的改写也必须保持用户意图。多任务偏好对齐把这两步放进同一检索链路，用分面质量与实际结果共同约束策略，减少局部生成目标错位。反馈仍可能偏向热门分面，因此不能只用生成流畅度或单项命中率评价整体。 示意：用户搜轻便电脑，生成重量分面后应形成可检索的重量条件；若分面漂亮却改写成性能排名，局部文本都通顺，最终结果仍偏离需求。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-genfacet-00b00c8d" class="ar-learning-paper-anchor"></span>
<h2 id="qa-c5bc783ab3fe2880">GenFacet为什么把分面生成和query改写一起按下游检索反馈优化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agenfacet">GenFacet: End-to-End Generative Faceted Search via Multi-Task Preference Alignment in E-Commerce</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · JD.com</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分面文本看起来合理，不一定能带来可用搜索结果；选定分面后的改写也必须保持用户意图。多任务偏好对齐把这两步放进同一检索链路，用分面质量与实际结果共同约束策略，减少局部生成目标错位。反馈仍可能偏向热门分面，因此不能只用生成流畅度或单项命中率评价整体。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户搜轻便电脑，生成重量分面后应形成可检索的重量条件；若分面漂亮却改写成性能排名，局部文本都通顺，最终结果仍偏离需求。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.19665">原论文</a> · <a href="../../../../reproductions/2603.19665-genfacet/">实现解读</a> · <a href="#qa-c5bc783ab3fe2880">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hap" data-paper-title="Not All Candidates are Created Equal: Heterogeneity-Aware Pre-ranking" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Not All Candidates are Created Equal: Heterogeneity-Aware Pre-ranking 搜广推与 LLM 应用 ByteDance / Toutiao 2026-03-04 按候选难度把样本路由到轻量或强预排分支，再以跨分支 harmonization 约束不同计算预算下的排序尺度。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 hap 核心机制；相对 NDCG@10 +4.90%。  pre-ranking contrastive-learning dynamic-routing 搜广推 候选生成与搜索匹配 HAP把困难候选送到强分支，为什么还要harmonization对齐分支分数？ 分支计算量不同，输出分布可能具有不同尺度；直接混排会把模型尺度误当物品价值。HAP先按候选难度分配轻重计算，再用跨分支协调约束，让有限预算下的结果仍能比较。路由错误也会把真正难例送入弱路径，因此不能只报告省下多少算力，而忽略统一排序质量。 示意：轻分支输出常在0.8附近，强分支输出常在0.4附近，二者直接比较会系统偏向前者；对齐尺度后，才能判断不同分支评分的候选谁应排前。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-hap-86607d9e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-886b08d0b9de067d">HAP把困难候选送到强分支，为什么还要harmonization对齐分支分数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahap">Not All Candidates are Created Equal: Heterogeneity-Aware Pre-ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Toutiao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分支计算量不同，输出分布可能具有不同尺度；直接混排会把模型尺度误当物品价值。HAP先按候选难度分配轻重计算，再用跨分支协调约束，让有限预算下的结果仍能比较。路由错误也会把真正难例送入弱路径，因此不能只报告省下多少算力，而忽略统一排序质量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>轻分支输出常在0.8附近，强分支输出常在0.4附近，二者直接比较会系统偏向前者；对齐尺度后，才能判断不同分支评分的候选谁应排前。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.03770">原论文</a> · <a href="../../../../reproductions/2603.03770-hap/">实现解读</a> · <a href="#qa-886b08d0b9de067d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mfli" data-paper-title="Rethinking ANN-based Retrieval: Multifaceted Learnable Index for Large-scale Recommendation System" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Rethinking ANN-based Retrieval: Multifaceted Learnable Index for Large-scale Recommendation System 搜广推与 LLM 应用 Meta 2026-02-18 ANN 把所有召回目标压进一个几何空间，离线建索引导致新内容滞后，在线近邻搜索又随候选规模变贵。MFLI 将 index 作为模型参数联合学习，并用多个 facet 表达语义、受欢迎度和时效性；请求侧直接分配各 facet 的检索预算。 Fidelity: 核心机制复现。本地构建并学习 genre、两层 semantic code、freshness 四个 facet，而非用单一 ANN 空间代替论文方法。全目录打分用于公平实验，不测 Meta 的十亿级实时索引、GPU QPS 或私有新鲜度标签。本地对照口径：基线为同切分的 single-space ANN proxy，实验组加入四 facet MFLI；NDCG@10 相对 -10.01%。  retrieval learnable-index fresh-content diversity serving 搜广推 候选生成与搜索匹配 MFLI为什么把索引作为模型参数，并让请求按facet分配检索预算？ 一个几何空间难同时表达语义、热度和时效性，独立离线索引也可能落后于模型。多facet学习式索引为不同目标保留不同组织方式，请求再决定各路投入多少候选配额，避免统一搜索策略。可学习索引仍需维护新内容与路径一致性，不能只凭省去传统ANN就宣称质量与更新成本都更好。 示意：探索请求可多给新鲜内容facet预算，明确品类请求多给语义facet；如果所有请求固定平均分配，即使有多个索引，也未真正利用上下文需求。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-mfli-7f2af977" class="ar-learning-paper-anchor"></span>
<h2 id="qa-75db5ab44a747faf">MFLI为什么把索引作为模型参数，并让请求按facet分配检索预算？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amfli">Rethinking ANN-based Retrieval: Multifaceted Learnable Index for Large-scale Recommendation System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一个几何空间难同时表达语义、热度和时效性，独立离线索引也可能落后于模型。多facet学习式索引为不同目标保留不同组织方式，请求再决定各路投入多少候选配额，避免统一搜索策略。可学习索引仍需维护新内容与路径一致性，不能只凭省去传统ANN就宣称质量与更新成本都更好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>探索请求可多给新鲜内容facet预算，明确品类请求多给语义facet；如果所有请求固定平均分配，即使有多个索引，也未真正利用上下文需求。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.16124">原论文</a> · <a href="../../../../reproductions/2602.16124-mfli/">实现解读</a> · <a href="#qa-75db5ab44a747faf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:capts" data-paper-title="CAPTS: Channel-Aware, Preference-Aligned Trigger Selection for Multi-Channel Item-to-Item Retrieval" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="CAPTS: Channel-Aware, Preference-Aligned Trigger Selection for Multi-Channel Item-to-Item Retrieval 搜广推与 LLM 应用 Kuaishou Technology 2026-02-13 VAM 不只看触发物品本身的反馈，而把两跳召回物品的下游消费价值归因回 trigger；CATR 再联合决定 trigger 到各 I2I 通道的路由，减少通道重叠并提升互补覆盖。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05500，相对变化 +1.84%。本地代理目标与论文生产任务不同，不能外推线上 lift。  retrieval trigger-selection multi-channel-routing 搜广推 候选生成与搜索匹配 CAPTS为什么用trigger召回出的内容消费价值评价trigger，而不只看trigger自身点击？ 触发物品是召回入口，其直接反馈未必反映后续能带来什么候选。VAM把两跳内容的下游消费归因回入口，再由CATR联合分配trigger与I2I通道，既考虑价值又惩罚重叠。单独挑最热门入口可能让多个通道召回相同内容，浪费有限候选配额。 示意：两个热门视频都导向同一批搞笑片，第三个较冷入口却能召回高价值科普；按下游价值和通道互补分配，可能比全选热门入口覆盖更好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-capts-e4a04e24" class="ar-learning-paper-anchor"></span>
<h2 id="qa-696381a02e76aa05">CAPTS为什么用trigger召回出的内容消费价值评价trigger，而不只看trigger自身点击？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acapts">CAPTS: Channel-Aware, Preference-Aligned Trigger Selection for Multi-Channel Item-to-Item Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>触发物品是召回入口，其直接反馈未必反映后续能带来什么候选。VAM把两跳内容的下游消费归因回入口，再由CATR联合分配trigger与I2I通道，既考虑价值又惩罚重叠。单独挑最热门入口可能让多个通道召回相同内容，浪费有限候选配额。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个热门视频都导向同一批搞笑片，第三个较冷入口却能召回高价值科普；按下游价值和通道互补分配，可能比全选热门入口覆盖更好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12564">原论文</a> · <a href="../../../../reproductions/2602.12564-capts/">实现解读</a> · <a href="#qa-696381a02e76aa05">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:airbnb-ebr" data-paper-title="Applying Embedding-Based Retrieval to Airbnb Search" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Applying Embedding-Based Retrieval to Airbnb Search 搜广推与 LLM 应用 Airbnb 2026-01-11 按搜索—浏览—预订的多阶段旅程构造正例和 hard negatives，以流量 replay 对齐第一阶段召回口径；线上结合 HNSW/IVF、地理过滤与高频库存更新。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04943，相对变化 -8.48%。本地代理目标与论文生产任务不同，不能外推线上 lift。  search-retrieval embedding-retrieval hard-negative-mining 搜广推 候选生成与搜索匹配 Airbnb EBR为什么要沿搜索—浏览—预订旅程构造难负例，而不只用随机房源？ 随机房源往往地域或条件明显不符，模型容易只学到粗差别。旅程内浏览过但未预订的房源提供更接近实际选择边界的对照，训练因此更贴合第一阶段召回；服务时还需结合地理、库存和索引更新。未预订不必然是不喜欢，所以难负例与采样口径必须一起解释。 示意：巴黎行程中用东京房源作负例太容易；同区域、相近价格但未预订的房源更能检验细粒度需求，同时要避免把已订满当作不相关。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-airbnb-ebr-a90e62e0" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b96313817395d985">Airbnb EBR为什么要沿搜索—浏览—预订旅程构造难负例，而不只用随机房源？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aairbnb-ebr">Applying Embedding-Based Retrieval to Airbnb Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Airbnb</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>随机房源往往地域或条件明显不符，模型容易只学到粗差别。旅程内浏览过但未预订的房源提供更接近实际选择边界的对照，训练因此更贴合第一阶段召回；服务时还需结合地理、库存和索引更新。未预订不必然是不喜欢，所以难负例与采样口径必须一起解释。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>巴黎行程中用东京房源作负例太容易；同区域、相近价格但未预订的房源更能检验细粒度需求，同时要避免把已订满当作不相关。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.06873">原论文</a> · <a href="../../../../reproductions/2601.06873-airbnb-ebr/">实现解读</a> · <a href="#qa-b96313817395d985">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:crsd" data-paper-title="From Reasoning LLMs to BERT: A Two-Stage Distillation Framework for Search Relevance" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="From Reasoning LLMs to BERT: A Two-Stage Distillation Framework for Search Relevance 搜广推与 LLM 应用 Meituan 2025-10-13 先以 CPT、SFT 和多维偏好优化构建领域 reasoning LLM，再让同一轻量学生的普通输入与 reasoning-augmented 输入做对比式自蒸馏，线上无需推理链。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上执行论文的候选相关检索、层级压缩或蒸馏目标；未使用公司私有日志与线上 serving，线上 A/B 只引用原文。本地相对变化不得与原文指标混写。本地对照口径：基线为 shared transition + content baseline，实验组为 CRSD，只改变论文核心机制；ndcg_at_10 0.0354 → 0.0346，相对基线 -2.14%。  search content-understanding llm-distillation 搜广推 候选生成与搜索匹配 CRSD为何让同一学生比较有reasoning和无reasoning的输入，而不是上线时始终携带推理链？ reasoning视图提供更丰富的关系线索，普通视图对应实际低延迟服务输入。自蒸馏与对比目标把丰富视图的判断压入学生，使其不依赖每次生成推理文本；标签监督继续约束任务正确性。若教师理由含答案泄漏或两种视图在服务时分布不一致，蒸馏损失下降也未必意味着有效迁移。 示意：训练时给商品相关性学生看一段属性比较理由，再要求无理由输入也作出相近判断；上线只给查询和商品，不必为每个候选额外生成一段解释。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-crsd-bbd3991b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-3ef068bf8e66afc1">CRSD为何让同一学生比较有reasoning和无reasoning的输入，而不是上线时始终携带推理链？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acrsd">From Reasoning LLMs to BERT: A Two-Stage Distillation Framework for Search Relevance</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>reasoning视图提供更丰富的关系线索，普通视图对应实际低延迟服务输入。自蒸馏与对比目标把丰富视图的判断压入学生，使其不依赖每次生成推理文本；标签监督继续约束任务正确性。若教师理由含答案泄漏或两种视图在服务时分布不一致，蒸馏损失下降也未必意味着有效迁移。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练时给商品相关性学生看一段属性比较理由，再要求无理由输入也作出相近判断；上线只给查询和商品，不必为每个候选额外生成一段解释。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.11056">原论文</a> · <a href="../../../../reproductions/2510.11056-crsd/">实现解读</a> · <a href="#qa-3ef068bf8e66afc1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mpformer" data-paper-title="MPFormer: Adaptive Framework for Industrial Multi-Task Personalized Sequential Retriever" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="MPFormer: Adaptive Framework for Industrial Multi-Task Personalized Sequential Retriever 搜广推与 LLM 应用 Kuaishou Technology 2025-08-28 以 objective token 驱动同一序列检索器完成多种行为目标，并按任务难度动态分配容量和候选配额。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 mpformer 核心机制；相对 NDCG@10 -7.15%。  retrieval multi-task sequence serving 搜广推 候选生成与搜索匹配 MPFormer 的 objective token 如何让同一段历史产生面向不同目标的召回表示？ 目标 token 与历史一起进入序列模型，为编码过程提供当前任务条件，所以同一用户可以形成面向不同行为目标的表示。动态权重和候选配额再根据任务难度调整训练与检索资源。它共享主干却保留目标差异，代价是各目标的权重和配额需要校准，不能把多个目标当作完全相同的下一物品预测。 示意：同一段浏览历史，点击目标更关注新奇内容，购买目标更关注近期反复比较的商品。切换目标 token 后，模型可以从同一历史中提取不同信号并分配候选数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-mpformer-268b1045" class="ar-learning-paper-anchor"></span>
<h2 id="qa-76a6ff70ef5af788">MPFormer 的 objective token 如何让同一段历史产生面向不同目标的召回表示？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ampformer">MPFormer: Adaptive Framework for Industrial Multi-Task Personalized Sequential Retriever</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标 token 与历史一起进入序列模型，为编码过程提供当前任务条件，所以同一用户可以形成面向不同行为目标的表示。动态权重和候选配额再根据任务难度调整训练与检索资源。它共享主干却保留目标差异，代价是各目标的权重和配额需要校准，不能把多个目标当作完全相同的下一物品预测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一段浏览历史，点击目标更关注新奇内容，购买目标更关注近期反复比较的商品。切换目标 token 后，模型可以从同一历史中提取不同信号并分配候选数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.20400">原论文</a> · <a href="../../../../reproductions/2508.20400-mpformer/">实现解读</a> · <a href="#qa-76a6ff70ef5af788">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:beque" data-paper-title="Large Language Model based Long-tail Query Rewriting in Taobao Search" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Large Language Model based Long-tail Query Rewriting in Taobao Search 搜广推与 LLM 应用 Alibaba 2023-11-07 长尾电商 query 存在语义缺口，单纯 SFT 只模仿人工 rewrite，未直接对齐召回质量。BEQUE 先用拒绝采样和多指令数据 SFT，再让模型为每个 query 自采样多个 rewrite；淘宝离线搜索系统从 relevance、retrieval increment、hit rate 打分并形成偏序，最后用 Preference Ranking Optimization（PRO）把排序反馈对齐回 LLM。生产 serving 采用离线刷库 + 在线 KV，不把 7B 自回归模型放进请求链路。 Fidelity: 完整核心链路复现。真实执行 seq2seq SFT、beam self-sampling、离线检索反馈、partial order 构造和 rank-aware PRO；Qwen-7B/淘宝搜索替换为 T5-small/MovieLens 公开目录。本地对照口径：基线是 T5 SFT；实验组是同一模型继续做 PRO；主组合反馈从 0.62102 升至 0.80750（+30.03%），但 increment -66.02%。这是对齐阶段消融；DIN 不适用于 query rewriting 任务。  llm-recommendation query-rewriting preference-optimization search 搜广推 候选生成与搜索匹配 BEQUE完成SFT后为什么还要对多个自采样rewrite做PRO？ SFT学习示范怎么改写，却未必优化改写后的检索结果。BEQUE让同一查询生成多个候选，由离线搜索反馈形成偏序，再用长度归一化序列分数学习更好的相对选择。反馈同时含相关性与新增召回等目标，因此组合分上涨仍可能牺牲某一子项，不能把流畅改写当检索成功。 示意：两种改写都很通顺，一种只召回原有热门商品，另一种补到相关长尾；搜索反馈可提供文字示范里没有的区别，但需同时看新增覆盖是否退化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-beque-26cd2487" class="ar-learning-paper-anchor"></span>
<h2 id="qa-5ca47927da463164">BEQUE完成SFT后为什么还要对多个自采样rewrite做PRO？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Abeque">Large Language Model based Long-tail Query Rewriting in Taobao Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>SFT学习示范怎么改写，却未必优化改写后的检索结果。BEQUE让同一查询生成多个候选，由离线搜索反馈形成偏序，再用长度归一化序列分数学习更好的相对选择。反馈同时含相关性与新增召回等目标，因此组合分上涨仍可能牺牲某一子项，不能把流畅改写当检索成功。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两种改写都很通顺，一种只召回原有热门商品，另一种补到相关长尾；搜索反馈可提供文字示范里没有的区别，但需同时看新增覆盖是否退化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2311.03758">原论文</a> · <a href="../../../../reproductions/2311.03758-beque/">实现解读</a> · <a href="#qa-5ca47927da463164">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:youtube-dnn" data-paper-title="Deep Neural Networks for YouTube Recommendations" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Deep Neural Networks for YouTube Recommendations 搜广推与 LLM 应用 Google / YouTube 2016-09-15 YouTube 将推荐拆成候选生成与精排。候选阶段要从百万量级视频中快速召回，传统矩阵分解难以吸收异构历史和上下文。观看历史 embedding 经过聚合和多层网络形成用户向量，训练目标把下一次观看建模为大规模多分类；服务时用近邻检索取候选。 三 seed 下 NDCG@10 为 0.02854→0.02666，该缩放设置未复现论文方向性收益，作为负结果保留。复现级别：核心机制复现。复现级别：核心机制复现。实际训练历史聚合、非线性用户塔和 item embedding 打分；YouTube 私有日志及生产 sampled softmax 未复刻。本地对照口径：基线为历史均值 two-tower，实验组增加 YouTube DNN 非线性用户塔；NDCG@10 相对 -6.61%，见 metrics/movielens-100k-seeds42-44.json。  retrieval ranking classic two-stage 搜广推 候选生成与搜索匹配 YouTube DNN 为什么把下一观看训练为大规模分类，却在服务时只做向量近邻检索？ 用户历史与上下文经非线性网络形成向量，训练用物品向量点积的多分类目标，使观看过的目标比负例更匹配。相同点积结构允许服务端预建物品索引，快速寻找高分候选，避免逐视频运行复杂网络。它是候选生成器的效率设计，不能把召回分数直接等同于精排最终效用。 示意：训练时让用户向量更靠近真实下一视频，远离采样负例；请求时只算一次用户向量，再从百万视频索引取近邻，后续精排继续处理更复杂的候选特征。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-youtube-dnn-d653b9f6" class="ar-learning-paper-anchor"></span>
<h2 id="qa-a551ec9fc486cffb">YouTube DNN 为什么把下一观看训练为大规模分类，却在服务时只做向量近邻检索？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ayoutube-dnn">Deep Neural Networks for YouTube Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用户历史与上下文经非线性网络形成向量，训练用物品向量点积的多分类目标，使观看过的目标比负例更匹配。相同点积结构允许服务端预建物品索引，快速寻找高分候选，避免逐视频运行复杂网络。它是候选生成器的效率设计，不能把召回分数直接等同于精排最终效用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练时让用户向量更靠近真实下一视频，远离采样负例；请求时只算一次用户向量，再从百万视频索引取近邻，后续精排继续处理更复杂的候选特征。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://research.google/pubs/deep-neural-networks-for-youtube-recommendations/">原论文</a> · <a href="../../../../reproductions/recsys2016-youtube-dnn-youtube-dnn/">实现解读</a> · <a href="#qa-a551ec9fc486cffb">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

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

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
