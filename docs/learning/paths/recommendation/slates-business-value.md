---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 重排、展示与长期价值

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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:maps-creative" data-paper-title="MAPS: A Multi-Agent Personalized Script-Driven Video Advertising System Enhanced by Reinforcement Learning" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="MAPS: A Multi-Agent Personalized Script-Driven Video Advertising System Enhanced by Reinforcement Learning 搜广推与 LLM 应用 Beihang University 2026-10-19 从固定广告库存检索创意，无法及时适应个体偏好和反馈。MAPS以Profile提取画像、Scripter生成分镜、Director调用视频生成、Reflector归因反馈，区分画像问题与脚本问题并路由最小修改。画像不仅含兴趣，也包含呈现风格与决策倾向。脚本先SFT学习结构，再用结构正确性、个性化偏好和商品事实一致性构造混合奖励，以GRPO式组内标准化更新。它的关键是大模型/视频生成与私有反馈环境的组合，不是独立奖励公式。 成本过高，不复现（审查 DONE），不把通用GRPO或三个分数加权冒充视频广告生成系统。仅研究资料。成本过高，不复现（审查 DONE），不把通用GRPO或三个分数加权冒充视频广告生成系统。Profile/Reflector是Qwen3-VL-32B，Scripter是8B；SFT20epoch、最大8192tokens，随后RL5000步，原文在8张H100上实验。导演依赖Kling-Omni，反馈闭环依赖生产系统。单卡A100/A30与Mac不承担此完整矩阵，成本过高，不复现（审查 DONE）。没有本地模型、评测指标或GPU回执，不进入自动重试与Evolve。  展示层生成与个性化 个性化创意生成 搜广推 重排、展示与长期价值 MAPS的Reflector为什么区分画像错误与脚本错误，再路由最小修改？ 低反馈可能来自理解错人，也可能来自表达和商品事实有问题，全部重做会浪费计算并破坏本来正确的部分。分角色归因后只修改相关环节，让画像、脚本与视频生成保持可检查接口；混合奖励还需评估结构、个性化和事实。该链路依赖大模型与私有环境，本库因成本只收录研究，不提供关键词奖励替代复现。 示意：用户偏好判断正确，但脚本夸大了商品性能，应修脚本而非重建画像；若根本把送礼对象理解错，再精修镜头也无法修正推荐方向。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-maps-creative-255b1b1c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d63df493a0c089e0">MAPS的Reflector为什么区分画像错误与脚本错误，再路由最小修改？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amaps-creative">MAPS: A Multi-Agent Personalized Script-Driven Video Advertising System Enhanced by Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>低反馈可能来自理解错人，也可能来自表达和商品事实有问题，全部重做会浪费计算并破坏本来正确的部分。分角色归因后只修改相关环节，让画像、脚本与视频生成保持可检查接口；混合奖励还需评估结构、个性化和事实。该链路依赖大模型与私有环境，本库因成本只收录研究，不提供关键词奖励替代复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户偏好判断正确，但脚本夸大了商品性能，应修脚本而非重建画像；若根本把送礼对象理解错，再精修镜头也无法修正推荐方向。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.25748v1">原论文</a> · <a href="../../../../recommendation-components/2610.25748-maps-creative/">实现解读</a> · <a href="#qa-d63df493a0c089e0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cohortmix-ts" data-paper-title="Challenges and Solutions for Bandits in the Wild: Warm-Started Mixture Bandits for Cross-Cohort Slate Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Challenges and Solutions for Bandits in the Wild: Warm-Started Mixture Bandits for Cross-Cohort Slate Recommendation 搜广推与 LLM 应用 DFKI / RPTU Kaiserslautern-Landau 2026-09-29 从历史 cohort 学习用户群和 item arm，用元数据给新用户构造固定强度的混合 Beta 先验；每轮用 Thompson sampling 选择未曝光 slate，并按用户反馈独立更新后验。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行固定强度 mixture prior、Thompson slate 与 posterior update；未复刻历史矩阵分解和 25 天部署。执行固定强度 mixture prior、Thompson slate 与 posterior update；未复刻历史矩阵分解和 25 天部署。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  cold-start slate-bandit cross-cohort-transfer 搜广推 重排、展示与长期价值 CohortMix-TS为什么用固定强度的混合Beta先验，而不直接搬来历史群组的全部计数？ 新用户可借相似群组的经验热启动，但历史样本规模若直接变成先验强度，会让个人新反馈长期无法改变判断。方法先混合群组均值，再用受控伪计数形成先验，并按个人曝光反馈独立更新。Thompson采样保留探索，不是永久按群组平均值确定推荐；本地只检验后验机制。 示意：群组有十万次反馈，新用户只有三次；若全部继承，三次反馈几乎不起作用。用固定先验强度，群体经验能引路，也允许个人兴趣逐渐接管。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-cohortmix-ts-f84d0507" class="ar-learning-paper-anchor"></span>
<h2 id="qa-a52b737be11c2a3b">CohortMix-TS为什么用固定强度的混合Beta先验，而不直接搬来历史群组的全部计数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acohortmix-ts">Challenges and Solutions for Bandits in the Wild: Warm-Started Mixture Bandits for Cross-Cohort Slate Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · DFKI / RPTU Kaiserslautern-Landau</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>新用户可借相似群组的经验热启动，但历史样本规模若直接变成先验强度，会让个人新反馈长期无法改变判断。方法先混合群组均值，再用受控伪计数形成先验，并按个人曝光反馈独立更新。Thompson采样保留探索，不是永久按群组平均值确定推荐；本地只检验后验机制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>群组有十万次反馈，新用户只有三次；若全部继承，三次反馈几乎不起作用。用固定先验强度，群体经验能引路，也允许个人兴趣逐渐接管。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37800">原论文</a> · <a href="../../../../reproductions/2609.37800-cohortmix-ts/">实现解读</a> · <a href="#qa-a52b737be11c2a3b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gese" data-paper-title="Generate to Explore, Select to Exploit: Aligning LLM-based Headline Generation with Personalized Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Generate to Explore, Select to Exploit: Aligning LLM-based Headline Generation with Personalized Recommendation 搜广推与 LLM 应用 Baidu 2026-09-14 集合级多样性/忠实度探索后，再以当前上下文选择个性化标题；生产系统报告 CTR +2.57%、停留时长 +0.87%。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。私有日志、生产 checkpoint 与 serving 栈均未复刻。本地只验证公开数据上的核心状态转换；未复刻私有训练数据、大模型生成器、生产流量反馈或在线服务。当前不映射 evolve，避免 registry-only 标签。线上数字来自论文正文 A/B，不与本地 MovieLens 结果混写。本地 seeds 42/43/44 见 metrics/movielens-100k-seeds42-44.json。首个 seed 的统一 NDCG@10 基线为 0.05401，实验组为 0.04421，相对变化 -18.15%。  presentation-layer headline-generation gspo bandit-selection 搜广推 重排、展示与长期价值 GESE为什么先探索一组多样且忠实的标题，再按当前上下文选择一个？ 只有一个固定标题无法适应不同用户，逐请求自由生成又可能昂贵且产生失真。集合探索先准备相互有区别、仍忠于内容的候选，selector再利用上下文选择，分离可复用创作与实时个性化。多样性不能以捏造事实换取；本地固定候选打分只验证选择组件，不等于重现完整标题生成训练。 示意：同一纪录片可有摄影视角或自然知识视角的忠实标题，面对不同用户选择其一；不能为了提高点击把影片没有的惊险情节写进候选集合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-gese-4a69cb3b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-31ed3abf673cb8cf">GESE为什么先探索一组多样且忠实的标题，再按当前上下文选择一个？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agese">Generate to Explore, Select to Exploit: Aligning LLM-based Headline Generation with Personalized Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Baidu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只有一个固定标题无法适应不同用户，逐请求自由生成又可能昂贵且产生失真。集合探索先准备相互有区别、仍忠于内容的候选，selector再利用上下文选择，分离可复用创作与实时个性化。多样性不能以捏造事实换取；本地固定候选打分只验证选择组件，不等于重现完整标题生成训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一纪录片可有摄影视角或自然知识视角的忠实标题，面对不同用户选择其一；不能为了提高点击把影片没有的惊险情节写进候选集合。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.15094">原论文</a> · <a href="../../../../reproductions/2609.15094-gese/">实现解读</a> · <a href="#qa-31ed3abf673cb8cf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ogr" data-paper-title="Once Generated, Ranked: End-to-End Generative Slate Recommendation with Unified Semantic-Collaborative IDs" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Once Generated, Ranked: End-to-End Generative Slate Recommendation with Unified Semantic-Collaborative IDs 搜广推与 LLM 应用 Kuaishou Technology 2026-08-18 TUSID 融合语义码与协同码，GL2P 直接规划整张 slate，SPA 再用保守策略优化对齐列表级反馈。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation slate-ranking semantic-id reinforcement-learning 搜广推 重排、展示与长期价值 OGR 为什么先融合语义码与协同码，再对整张 slate 做保守策略优化？ 语义码帮助内容相近物品共享结构，协同码补充用户行为关系，联合编码先决定生成空间怎样组织物品。列表规划再把整张推荐列表作为行动，使训练能考虑项目之间的配合；保守优化利用列表反馈调整策略，同时约束偏离已有监督策略的幅度。编码、规划和反馈分别解决表示、联合决策与稳定更新。 示意：一屏四个商品若逐个选最高分，可能全是相似运动鞋。联合列表目标可以考虑鞋、袜、背包的互补性，策略约束则防止为追求一次反馈突然生成完全陌生组合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-ogr-bedfe7b4" class="ar-learning-paper-anchor"></span>
<h2 id="qa-e953ac0fa93e88c7">OGR 为什么先融合语义码与协同码，再对整张 slate 做保守策略优化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aogr">Once Generated, Ranked: End-to-End Generative Slate Recommendation with Unified Semantic-Collaborative IDs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语义码帮助内容相近物品共享结构，协同码补充用户行为关系，联合编码先决定生成空间怎样组织物品。列表规划再把整张推荐列表作为行动，使训练能考虑项目之间的配合；保守优化利用列表反馈调整策略，同时约束偏离已有监督策略的幅度。编码、规划和反馈分别解决表示、联合决策与稳定更新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一屏四个商品若逐个选最高分，可能全是相似运动鞋。联合列表目标可以考虑鞋、袜、背包的互补性，策略约束则防止为追求一次反馈突然生成完全陌生组合。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.17613">原论文</a> · <a href="../../../../reproductions/2608.17613-ogr/">实现解读</a> · <a href="#qa-e953ac0fa93e88c7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:drem" data-paper-title="DrEM: Dual-Side Robust Ensemble Ranking from Noisy User Preference Predictions in Video Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DrEM: Dual-Side Robust Ensemble Ranking from Noisy User Preference Predictions in Video Recommendation 搜广推与 LLM 应用 Shenzhen University 2026-08-13 把多路 pxtr 先变换到 logit 空间，对预测噪声做偏好保持筛选，并利用 pair-label 翻转风险反演修正训练目标；最后用一致性融合减小输入扰动导致的排序漂移。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为朴素三路加权融合，实验组加入偏好保持筛选与风险修正；seed 42 的 NDCG@10 为 0.07726，基线为 0.07518。  ranking multi-objective robust-learning video-recommendation 搜广推 重排、展示与长期价值 DrEM为什么对偏好翻转风险修正损失，而不是只对多个预测分求平均？ 各路预测存在噪声时，组合得到的物品偏好可能被翻转，简单平均仍可能稳定地学到错误次序。DrEM先筛选扰动下保持偏好的样本，再根据翻转风险修正目标，并用一致性融合降低排序漂移。修正依赖对噪声机制的估计，翻转率接近不稳定边界时不能无条件套用公式。 示意：两件视频原本只差一点分，轻微CTR噪声就让正负对颠倒；与其把这种随机次序当可靠标签，更应识别其风险并约束融合结果对扰动的敏感度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-drem-6dedd99f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-bde83590cd02c905">DrEM为什么对偏好翻转风险修正损失，而不是只对多个预测分求平均？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adrem">DrEM: Dual-Side Robust Ensemble Ranking from Noisy User Preference Predictions in Video Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shenzhen University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>各路预测存在噪声时，组合得到的物品偏好可能被翻转，简单平均仍可能稳定地学到错误次序。DrEM先筛选扰动下保持偏好的样本，再根据翻转风险修正目标，并用一致性融合降低排序漂移。修正依赖对噪声机制的估计，翻转率接近不稳定边界时不能无条件套用公式。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两件视频原本只差一点分，轻微CTR噪声就让正负对颠倒；与其把这种随机次序当可靠标签，更应识别其风险并约束融合结果对扰动的敏感度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.12778">原论文</a> · <a href="../../../../reproductions/2608.12778-drem/">实现解读</a> · <a href="#qa-bde83590cd02c905">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dream" data-paper-title="DREAM: A Dual-Loop Recommendation Evolution Framework Powered by Large Language Models" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DREAM: A Dual-Loop Recommendation Evolution Framework Powered by Large Language Models 搜广推与 LLM 应用 Taobao &amp; Tmall Group / Alibaba 2026-08-10 工业推荐长期依赖人工配置和逐层独立优化，LLM 若直接生成自由文本又难以满足稳定性与安全要求。DREAM 是覆盖现有召回、精排和重排之上的控制平面：Intent Engine 将端上信号、session 行为和实时上下文整理成 L0 物理、L1 需求、L2 偏好三层意图；Meta Engine 依次执行 M1 意图摘要、M2 结合 Strategy Memory 的策略规划和 M3 确定性参数翻译；Unified Outlet 只接受白名单、范围内的 typed 参数。 Fidelity：核心机制复现。保留原推荐 backbone，实际执行分层意图、策略记忆、typed 参数编译、安全护栏及离线/影子在线双环；不以普通重排器代替核心控制链路。没有复刻淘宝私有多源信号、Qwen3 Meta Engine、真实流量和线上结论回存；本地“在线环”是 validation 内独立影子组，test 从未参与策略选择。本地对照口径：基线为同一 MovieLens-1M 切分和候选上的原 retrieval/ranking backbone；实验组只增加 DREAM 控制层，相对 NDCG@10 +39.36%，同时 head share +94.37%，不能只报正向相关性指标。  llm-recommendation ranking reranking intent-understanding online-policy serving 搜广推 重排、展示与长期价值 DREAM为什么让LLM输出有界语义级别，再由确定性模块翻译为参数？ 自由文本难以直接满足线上接口与取值约束，DREAM把意图理解、策略规划和参数编译分开。LLM只表达允许的调整方向与强度，统一出口再执行白名单与范围检查；离线和线上反馈验证后才写回策略记忆。这样语义推理可影响现有链路，却不能任意改写生产模型或无限放大权重。 示意：模型判断用户想多看新类目，只能提出规定级别的增加多样性；编译器把它转成有限的打散数量，而不会执行一句没有边界的“尽量推新内容”。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-dream-c0565aca" class="ar-learning-paper-anchor"></span>
<h2 id="qa-fd6aa07542d408de">DREAM为什么让LLM输出有界语义级别，再由确定性模块翻译为参数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adream">DREAM: A Dual-Loop Recommendation Evolution Framework Powered by Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>自由文本难以直接满足线上接口与取值约束，DREAM把意图理解、策略规划和参数编译分开。LLM只表达允许的调整方向与强度，统一出口再执行白名单与范围检查；离线和线上反馈验证后才写回策略记忆。这样语义推理可影响现有链路，却不能任意改写生产模型或无限放大权重。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型判断用户想多看新类目，只能提出规定级别的增加多样性；编译器把它转成有限的打散数量，而不会执行一句没有边界的“尽量推新内容”。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.09408">原论文</a> · <a href="../../../../reproductions/2608.09408-dream/">实现解读</a> · <a href="#qa-fd6aa07542d408de">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:metastrategy" data-paper-title="MetaStrategy: Generative Ranking with Executable LLM Strategies" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="MetaStrategy: Generative Ranking with Executable LLM Strategies 搜广推与 LLM 应用 Alibaba / Taobao 2026-08-10 固定打分网络难以按用户当下意图动态改变目标。MetaStrategy 让 LLM 输出带类型的 JSON 排序策略，包括目标权重、内容/类目偏好、约束与位置规则；确定性 compiler 将策略执行在候选列表上，避免自由文本直接控制线上排序。生产训练还用 replay 环境、自竞争 curriculum、evaluator-routed reward-augmented OPD 将 4B teacher 蒸馏到 0.8B student。 Fidelity：核心机制复现。实际训练上下文条件策略生成器，并以确定性 compiler 执行 typed strategy；本地负结果如实保留。未复刻淘宝私有日志、生产 replay、4B→0.8B OPD 与 nearline serving；公开实验只验证“生成 typed bundle → 校验 → 确定性执行”的核心路径。本地对照口径：基线为同预算单目标排序器，实验组为 typed strategy generator + deterministic compiler；NDCG@10 相对变化 -8.51%。  ranking llm-recommendation executable-strategy online-policy 搜广推 重排、展示与长期价值 MetaStrategy为什么让LLM生成typed策略而不是直接生成最终物品次序？ 结构化策略把目标权重、类目偏好和位置约束显式化，确定性compiler再对真实候选执行，便于限制范围与审计失败原因。LLM负责理解意图，排序逻辑负责保证可执行，二者可分别更新与评价。JSON格式正确只证明接口合法，不证明策略有用，更不能用模型自评分替代真实回放反馈。 示意：用户想少看重复内容，模型输出限定的类目打散与权重参数，compiler据现有候选排表；若没有相关候选，应暴露限制，而不是凭空生成不存在的商品。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-metastrategy-1088d4bd" class="ar-learning-paper-anchor"></span>
<h2 id="qa-931667540866622d">MetaStrategy为什么让LLM生成typed策略而不是直接生成最终物品次序？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ametastrategy">MetaStrategy: Generative Ranking with Executable LLM Strategies</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>结构化策略把目标权重、类目偏好和位置约束显式化，确定性compiler再对真实候选执行，便于限制范围与审计失败原因。LLM负责理解意图，排序逻辑负责保证可执行，二者可分别更新与评价。JSON格式正确只证明接口合法，不证明策略有用，更不能用模型自评分替代真实回放反馈。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户想少看重复内容，模型输出限定的类目打散与权重参数，compiler据现有候选排表；若没有相关候选，应暴露限制，而不是凭空生成不存在的商品。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.09440">原论文</a> · <a href="../../../../reproductions/2608.09440-metastrategy/">实现解读</a> · <a href="#qa-931667540866622d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:degr" data-paper-title="DEGR: Dual Exploration-Driven Generative Re-Ranking for Adaptive Cross-Request Context Bridging" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DEGR: Dual Exploration-Driven Generative Re-Ranking for Adaptive Cross-Request Context Bridging 搜广推与 LLM 应用 JD.com 2026-08-05 逐请求优化容易反复暴露相似商品。DEGR 在生成目标外加入同 cohort item embedding 的平方余弦约束，并用探索反馈形成 reward-adaptive ORPO，使偏好强度随真实探索收益变化；推理时再执行 diversity-aware greedy selection。 Fidelity：核心机制复现。实现 next-item CE、cohort 内多样性约束、adaptive reward-weighted ORPO 和多样性感知 greedy 重排。公开 MovieLens 没有跨请求曝光与探索 reward；本地以逆流行度代理奖励，未复刻京东十亿请求 reward model。本地对照口径：基线为同预算 CE generator，实验组加入 diversity 与 adaptive reward ORPO；相对基线 NDCG@10 +0.00%。  reranking slate-optimization exploration preference-optimization 搜广推 重排、展示与长期价值 DEGR为什么同时约束同cohort物品表示，并按探索收益调整偏好优化强度？ 逐请求追求高分可能跨请求反复暴露同类物品，表示约束先减少候选间的方向重叠。探索反馈再决定偏好更新应多强，避免对没有实际收益的探索机械强化；推理时的多样性选择补上输出层决策。训练表示分散不必然等于用户感知多样性，仍需同时看相关性与探索反馈。 示意：一组用户连续收到相似鞋款，单次列表看似合理却长期单调；模型既需减少候选同向集中，也需验证换入新类目是否真的带来有价值的探索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-degr-c402d30b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-86fa61ca0bb12fab">DEGR为什么同时约束同cohort物品表示，并按探索收益调整偏好优化强度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adegr">DEGR: Dual Exploration-Driven Generative Re-Ranking for Adaptive Cross-Request Context Bridging</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · JD.com</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>逐请求追求高分可能跨请求反复暴露同类物品，表示约束先减少候选间的方向重叠。探索反馈再决定偏好更新应多强，避免对没有实际收益的探索机械强化；推理时的多样性选择补上输出层决策。训练表示分散不必然等于用户感知多样性，仍需同时看相关性与探索反馈。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一组用户连续收到相似鞋款，单次列表看似合理却长期单调；模型既需减少候选同向集中，也需验证换入新类目是否真的带来有价值的探索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04809">原论文</a> · <a href="../../../../reproductions/2608.04809-degr/">实现解读</a> · <a href="#qa-86fa61ca0bb12fab">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:steps" data-paper-title="A Self-Triggered Agentic Push Recommendation System" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="A Self-Triggered Agentic Push Recommendation System 搜广推与 LLM 应用 ByteDance / Douyin 2026-08-03 固定频控无法实时调整，周期轮询又在成本与时机间冲突。STEPS 把“是否推送”和“何时再次唤醒”合成闭环：planning agent 用 gated ordinal regression 规划间隔，execution agent 用轨迹回报决定发送，轻量 filter agent 控制算力并拦截异常计划。 Fidelity：核心机制复现。公开数据只验证论文机制，不模拟生产流量。MovieLens 没有真实 push permission、触达成本和 wall-clock 唤醒器，只验证决策分解。本地对照口径：基线为共享 transition + content scorer，实验组只加入 STEPS 核心机制；相对 NDCG@10 +66.05%。  push-recommendation agentic-recommendation decision-transformer serving 搜广推 重排、展示与长期价值 STEPS 为什么把“下次何时唤醒”和“此刻是否推送”交给不同 agent，并加轻量过滤？ 固定频控不能适应用户状态，频繁轮询又浪费计算。规划 agent 用有序间隔预测决定何时再观察，执行 agent 根据轨迹回报选择发送，过滤器先拦截异常或低价值计划。分工把观察频率与发送决策联合成闭环，仍需区分等待收益与消息收益；本地代理排序结果不能替代真实推送留存实验。 示意：用户刚忽略一条通知，规划器可延长下次唤醒间隔；到时执行器发现没有值得发的内容，仍可选择不发。过滤器则避免异常计划让系统每秒反复唤醒。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-steps-e0be3966" class="ar-learning-paper-anchor"></span>
<h2 id="qa-c92364d01f8e886f">STEPS 为什么把“下次何时唤醒”和“此刻是否推送”交给不同 agent，并加轻量过滤？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asteps">A Self-Triggered Agentic Push Recommendation System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定频控不能适应用户状态，频繁轮询又浪费计算。规划 agent 用有序间隔预测决定何时再观察，执行 agent 根据轨迹回报选择发送，过滤器先拦截异常或低价值计划。分工把观察频率与发送决策联合成闭环，仍需区分等待收益与消息收益；本地代理排序结果不能替代真实推送留存实验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户刚忽略一条通知，规划器可延长下次唤醒间隔；到时执行器发现没有值得发的内容，仍可选择不发。过滤器则避免异常计划让系统每秒反复唤醒。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01949">原论文</a> · <a href="../../../../reproductions/2608.01949-steps/">实现解读</a> · <a href="#qa-c92364d01f8e886f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:director" data-paper-title="DIRECTOR: Dynamic Index-based Recommendation with Transport-Optimized Retrieval" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DIRECTOR: Dynamic Index-based Recommendation with Transport-Optimized Retrieval 搜广推与 LLM 应用 University of Science and Technology of China 2026-07-29 每个展示位置生成动态索引分布，以 Sinkhorn 最优运输联合约束所有位置；最终用全局匹配而非独立 argmax 解码，减少冲突并一次并行产生整张 slate。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为各位置独立动态索引，实验组加入 Sinkhorn transport 与硬全局匹配；seed 42 的 NDCG@10 为 0.05334，基线为 0.03857。  reranking dynamic-index optimal-transport non-autoregressive 搜广推 重排、展示与长期价值 DIRECTOR为什么用Sinkhorn加全局匹配，而不让每个位置独立挑最高分物品？ 独立位置预测可能都选择同一个热门物品，忽略位置之间争夺候选的耦合。Sinkhorn将分数转成受行列边际约束的软运输计划，训练时联合分配所有位置；最终再以全局匹配得到不冲突的硬列表。软分布本身还不是可展示排列，不能用独立argmax替代最后的组合解码。 示意：三个位置都最喜欢A，独立取最大会重复三次；全局匹配会同时考虑把A给最需要的位置、把B和C分给其余位置，从而形成一张合法列表。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-director-8aa08907" class="ar-learning-paper-anchor"></span>
<h2 id="qa-3f91ba74c893e498">DIRECTOR为什么用Sinkhorn加全局匹配，而不让每个位置独立挑最高分物品？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adirector">DIRECTOR: Dynamic Index-based Recommendation with Transport-Optimized Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立位置预测可能都选择同一个热门物品，忽略位置之间争夺候选的耦合。Sinkhorn将分数转成受行列边际约束的软运输计划，训练时联合分配所有位置；最终再以全局匹配得到不冲突的硬列表。软分布本身还不是可展示排列，不能用独立argmax替代最后的组合解码。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三个位置都最喜欢A，独立取最大会重复三次；全局匹配会同时考虑把A给最需要的位置、把B和C分给其余位置，从而形成一张合法列表。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26418">原论文</a> · <a href="../../../../reproductions/2607.26418-director/">实现解读</a> · <a href="#qa-3f91ba74c893e498">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:psg" data-paper-title="PSG: Pair-Space Generation for Efficient Generative Reranking" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="PSG: Pair-Space Generation for Efficient Generative Reranking 搜广推与 LLM 应用 Kuaishou Technology 2026-07-29 把相邻两个 item 编成一个请求内 pair token，在 pair 空间生成半长度序列，再无损展开为 item slate；pair scorer 显式保留顺序，重复约束保证展开结果可用。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为六步 item-space 生成，实验组为三步 pair-space 生成与展开；seed 42 的 NDCG@10 为 0.04826，基线为 0.05401，负结果保留。  reranking generative-recommendation pair-token serving 搜广推 重排、展示与长期价值 PSG 把两个相邻物品打包为 pair token，为什么能减少生成步数又必须保留内部顺序？ pair token 把两个位置联合建模，生成半长的 pair 序列后可无损展开，因此自回归步数减少。但一个 pair 的两个物品顺序会影响展示与后续条件，不能当作无序集合；重复约束还要保证不同 pair 展开后没有不可用重复。减少步数把一部分复杂度转移到配对空间和评分上，并非免费加速。 示意：六个位置原本生成六次，改成三次分别生成有序二元组。二元组“咖啡机、咖啡豆”与反过来不同；若第二组再次含咖啡机，展开前还需要处理重复。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-psg-c3e023ce" class="ar-learning-paper-anchor"></span>
<h2 id="qa-17163889d7416526">PSG 把两个相邻物品打包为 pair token，为什么能减少生成步数又必须保留内部顺序？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apsg">PSG: Pair-Space Generation for Efficient Generative Reranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>pair token 把两个位置联合建模，生成半长的 pair 序列后可无损展开，因此自回归步数减少。但一个 pair 的两个物品顺序会影响展示与后续条件，不能当作无序集合；重复约束还要保证不同 pair 展开后没有不可用重复。减少步数把一部分复杂度转移到配对空间和评分上，并非免费加速。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>六个位置原本生成六次，改成三次分别生成有序二元组。二元组“咖啡机、咖啡豆”与反过来不同；若第二组再次含咖啡机，展开前还需要处理重复。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26427">原论文</a> · <a href="../../../../reproductions/2607.26427-psg/">实现解读</a> · <a href="#qa-17163889d7416526">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:swag-bid" data-paper-title="Beyond Single-Episode Optimization: Sliding-Window Aware Generative Auto-Bidding for Long-Term Advertising Effectiveness" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Beyond Single-Episode Optimization: Sliding-Window Aware Generative Auto-Bidding for Long-Term Advertising Effectiveness 搜广推与 LLM 应用 Alibaba International Digital Commerce / Dalian University of Technology 2026-07-28 用 masked future plan 建模跨 episode 的七日滑窗目标，并以 per-step gate 将长期 guidance 注入当前 bid 决策。 Fidelity: 核心机制复现。本地执行论文的窗口感知出价目标与约束代理，不把公开离线实验写成生产广告系统。不是生产 Decision Transformer checkpoint，且公开数据没有 bid、budget、GMV，结果仅是结构消融。本地对照口径：基线为 single-episode Decision Transformer proxy，实验组为 sliding-window planner；同一小数据候选排序下 Hit@10 与 NDCG@10 均为 +0.00%。  advertising generative-model decision-transformer long-horizon 搜广推 重排、展示与长期价值 SWAG-Bid 为什么用跨 episode 的七日滑窗计划，还要逐步 gate 注入当前出价？ 单个 episode 的局部奖励可能忽视跨天预算与收益。滑窗状态承载更长目标，逐步 gate 再决定当前决策需要多少长期指导，避免固定强度压过即时市场信号。训练中的 masked future plan 提供监督，不意味着执行时可读取真实未来；本地小规模零变化也不能被解释成长期竞价收益已验证。 示意：今天竞争激烈但本周后面仍有机会，长期计划可能建议保留预算；当前遇到高价值请求时 gate 又允许即时信号更强。真实出价仍只能依据当时可得信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-swag-bid-1ae52cbb" class="ar-learning-paper-anchor"></span>
<h2 id="qa-7d8d241ec0fb2ef2">SWAG-Bid 为什么用跨 episode 的七日滑窗计划，还要逐步 gate 注入当前出价？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aswag-bid">Beyond Single-Episode Optimization: Sliding-Window Aware Generative Auto-Bidding for Long-Term Advertising Effectiveness</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce / Dalian University of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单个 episode 的局部奖励可能忽视跨天预算与收益。滑窗状态承载更长目标，逐步 gate 再决定当前决策需要多少长期指导，避免固定强度压过即时市场信号。训练中的 masked future plan 提供监督，不意味着执行时可读取真实未来；本地小规模零变化也不能被解释成长期竞价收益已验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>今天竞争激烈但本周后面仍有机会，长期计划可能建议保留预算；当前遇到高价值请求时 gate 又允许即时信号更强。真实出价仍只能依据当时可得信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25233">原论文</a> · <a href="../../../../reproductions/2607.25233-swag-bid/">实现解读</a> · <a href="#qa-7d8d241ec0fb2ef2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:youtube-freshness" data-paper-title="Breaking the Loop: An Empirical Comparison of Strategies for Novelty and Freshness in YouTube Music" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Breaking the Loop: An Empirical Comparison of Strategies for Novelty and Freshness in YouTube Music 搜广推与 LLM 应用 YouTube Music / Google 2026-07-26 系统比较 recency feature、IPS、可移除 bias tower 与 SNGP 不确定性探索，区分训练去偏和 serving 探索。 Fidelity: 核心机制复现。本地执行新鲜度感知的候选打分与公平对照；不复刻 YouTube 私有流量系统。没有 YouTube 连续训练基础设施和 SNGP 大模型；本地负结果不推翻论文各干预的在线结论。本地对照口径：基线为 popularity-biased continuous ranker，实验组为四机制组合；Hit@10 +0.00%、NDCG@10 -6.35%，head share -28.72%。  ranking feedback-loop freshness exploration 搜广推 重排、展示与长期价值 YouTube Freshness 为什么区分训练去偏与 serving 探索，而不把新鲜度特征当作完整解决方案？ 新鲜度特征告诉模型内容年龄，却不自动改变旧曝光造成的标签偏差。IPS 与可移除偏置塔在训练端处理数据选择，SNGP 不确定性奖励在服务端为未知内容分配探索，两者作用阶段不同。探索收集新反馈，去偏改善已有反馈利用；都依赖校准与假设，不能只因头部占比下降就认定用户满意度提高。 示意：新视频没有点击不一定质量差，可能从未曝光。训练端校正旧曝光偏差，服务端给高不确定候选少量机会，再根据真实反馈更新，而非仅给所有新视频固定加分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-youtube-freshness-c4f4face" class="ar-learning-paper-anchor"></span>
<h2 id="qa-0c80a24846ebefdf">YouTube Freshness 为什么区分训练去偏与 serving 探索，而不把新鲜度特征当作完整解决方案？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ayoutube-freshness">Breaking the Loop: An Empirical Comparison of Strategies for Novelty and Freshness in YouTube Music</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · YouTube Music / Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>新鲜度特征告诉模型内容年龄，却不自动改变旧曝光造成的标签偏差。IPS 与可移除偏置塔在训练端处理数据选择，SNGP 不确定性奖励在服务端为未知内容分配探索，两者作用阶段不同。探索收集新反馈，去偏改善已有反馈利用；都依赖校准与假设，不能只因头部占比下降就认定用户满意度提高。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新视频没有点击不一定质量差，可能从未曝光。训练端校正旧曝光偏差，服务端给高不确定候选少量机会，再根据真实反馈更新，而非仅给所有新视频固定加分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.23749">原论文</a> · <a href="../../../../reproductions/2607.23749-youtube-freshness/">实现解读</a> · <a href="#qa-0c80a24846ebefdf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pindco" data-paper-title="PinDCO: Whole-Page Aware Dynamic Creative Optimization at Scale" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="PinDCO: Whole-Page Aware Dynamic Creative Optimization at Scale 搜广推与 LLM 应用 Pinterest 2026-07-21 生成式创意使每个广告的候选图像、标题与版式迅速增多。PinDCO 用组件专属 tower 分别编码异构创意，再预测相对基础广告排序 logit 的增量；PAM 根据相对长宽比惩罚过度占用瀑布流像素的创意，前置轻量筛选、缓存和动态 batching 控制线上成本，ε-greedy 流量为新创意收集较少偏的反馈。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行组件专塔、基于广告分数的增量融合、像素惩罚公式与候选筛选；不把 MovieLens 内容特征冒充 Pinterest 创意或生产流量。未复刻 Pinterest 私有创意、用户/上下文特征、广告基线、在线 bandit 流量、缓存与服务集群。本实现不声明 CUDA 路径，也未接入 evolve，因为当前统一 evaluator 尚不能执行完整创意候选协议。MovieLens 100K、seeds 42/43/44 的固定公开口径见 metrics/movielens-100k-seeds42-44.json。  advertising creative-optimization whole-page-optimization multi-tower 搜广推 重排、展示与长期价值 PinDCO 为什么预测创意相对基础广告的增量，并额外惩罚长宽比带来的像素占用？ 基础广告分数包含商品和用户匹配信息，增量预测把学习重点放在图片、标题与版式改变了多少价值。较高创意还会占用更多瀑布流空间，像素调整乘子让收益与空间代价共同决定选择。探索流量为新创意补反馈；本地无真实像素实验，不能把代理特征结果解释为布局因果收益。 示意：同一广告有方图和长图，长图点击可能更高，却挤掉其他内容。只有增加的价值足以抵消像素惩罚时才选长图，而不是见到更高点击预测就直接占用更多版面。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-pindco-94511583" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d06f2355b72efe84">PinDCO 为什么预测创意相对基础广告的增量，并额外惩罚长宽比带来的像素占用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apindco">PinDCO: Whole-Page Aware Dynamic Creative Optimization at Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>基础广告分数包含商品和用户匹配信息，增量预测把学习重点放在图片、标题与版式改变了多少价值。较高创意还会占用更多瀑布流空间，像素调整乘子让收益与空间代价共同决定选择。探索流量为新创意补反馈；本地无真实像素实验，不能把代理特征结果解释为布局因果收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一广告有方图和长图，长图点击可能更高，却挤掉其他内容。只有增加的价值足以抵消像素惩罚时才选长图，而不是见到更高点击预测就直接占用更多版面。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11943">原论文</a> · <a href="../../../../reproductions/2609.11943-pindco/">实现解读</a> · <a href="#qa-d06f2355b72efe84">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:uame" data-paper-title="Uncertainty as Remedy: Mitigating Satisfaction Label Bias in Short Video Multi-Objective Ensemble Ranking" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Uncertainty as Remedy: Mitigating Satisfaction Label Bias in Short Video Multi-Objective Ensemble Ranking 搜广推与 LLM 应用 Kuaishou Technology 2026-07-19 点击、观看、点赞等 pxtr 只是不可观测“真实满意度”的冲突代理。UAME 在 EMER/EASQ 主干上增加共享表征的均值与方差双头，把分数视作 Gaussian 变量；用解析 pair probability 联合各 pxtr，令冲突更高的 pair 获得更大训练权重。线上只使用均值打分，因此不增加 serving 路径。 Fidelity: 核心机制复现。训练 Gaussian score 双头、概率 pairwise loss、冲突约束与不确定性加权；私有八路 pxtr 和生产 backbone 用公开 proxy 替代。未获得快手八路 pxtr、EMER/EASQ、问卷满意度和亿级流量；本地负结果说明这一公开 proxy 映射不能直接复现论文收益，不与线上 lift 混写。本地对照口径：基线是同 backbone 的 deterministic multi-objective pairwise ranker；实验组加入完整 UAME loss，NDCG@10 相对 -62.28%。  multi-objective-ranking uncertainty loss-design 搜广推 重排、展示与长期价值 UAME 为什么为排序分数学习均值和方差，训练时重点处理高冲突 pair，却线上只用均值？ 多个 pxtr 是满意度的冲突代理，确定性分数难表达其分歧。均值—方差双头把得分建成高斯变量，用解析胜出概率进行 pairwise 学习，再提高高不确定 pair 的权重并约束方差。方差在训练中组织困难关系，服务只读取均值以保持路径成本；它表示模型化的不确定性，不是已观测到的真实满意度方差。 示意：两个视频一个更易点击、一个更可能长看，模型对胜负不确定。训练重点处理这类冲突，并约束随意抬高方差；上线仍输出一个均值分数参与排序。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-uame-b8cd46d0" class="ar-learning-paper-anchor"></span>
<h2 id="qa-3dcc33d2640a4034">UAME 为什么为排序分数学习均值和方差，训练时重点处理高冲突 pair，却线上只用均值？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Auame">Uncertainty as Remedy: Mitigating Satisfaction Label Bias in Short Video Multi-Objective Ensemble Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多个 pxtr 是满意度的冲突代理，确定性分数难表达其分歧。均值—方差双头把得分建成高斯变量，用解析胜出概率进行 pairwise 学习，再提高高不确定 pair 的权重并约束方差。方差在训练中组织困难关系，服务只读取均值以保持路径成本；它表示模型化的不确定性，不是已观测到的真实满意度方差。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个视频一个更易点击、一个更可能长看，模型对胜负不确定。训练重点处理这类冲突，并约束随意抬高方差；上线仍输出一个均值分数参与排序。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.17092">原论文</a> · <a href="../../../../reproductions/2607.17092-uame/">实现解读</a> · <a href="#qa-3dcc33d2640a4034">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:real-estate-rerank" data-paper-title="LLM-Based Re-Ranking for Real Estate Search" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="LLM-Based Re-Ranking for Real Estate Search 搜广推与 LLM 应用 QuintoAndar 2026-07-16 把对话需求、结构化房源属性、文本描述和候选集合统计交给 LLM 重排，用候选间比较补足向量召回的局部相关性。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  search-ranking llm-reranking content-understanding 搜广推 重排、展示与长期价值 房产 LLM 重排为什么要读取候选集合统计，而不只独立比较查询与每套房源？ 对话需求可能包含预算、通勤和空间等互相制约条件，房源描述与结构化字段也需要共同解释。候选集合统计提供当前可选范围，使模型进行相对取舍，补足向量相似度的局部匹配。列表变化会改变比较背景，所以分数未必可跨集合直接复用；重排也不能补回召回阶段漏掉的房源。 示意：用户想要地铁近且安静，候选都难两者兼得。读取整组后可说明哪套在通勤与噪声之间更平衡，而不是把每套宣传文本单独与查询做相似度比较。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-real-estate-rerank-2009ea9f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-93d88b0ec85364b8">房产 LLM 重排为什么要读取候选集合统计，而不只独立比较查询与每套房源？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Areal-estate-rerank">LLM-Based Re-Ranking for Real Estate Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · QuintoAndar</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>对话需求可能包含预算、通勤和空间等互相制约条件，房源描述与结构化字段也需要共同解释。候选集合统计提供当前可选范围，使模型进行相对取舍，补足向量相似度的局部匹配。列表变化会改变比较背景，所以分数未必可跨集合直接复用；重排也不能补回召回阶段漏掉的房源。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户想要地铁近且安静，候选都难两者兼得。读取整组后可说明哪套在通勤与噪声之间更平衡，而不是把每套宣传文本单独与查询做相似度比较。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14835">原论文</a> · <a href="../../../../reproductions/2607.14835-real-estate-rerank/">实现解读</a> · <a href="#qa-93d88b0ec85364b8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:adaptive-ad-load" data-paper-title="Adaptive Ad Load Design for Sponsored Search Markets: Evidence, Theory, and Deployment" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Adaptive Ad Load Design for Sponsored Search Markets: Evidence, Theory, and Deployment 搜广推与 LLM 应用 University of Washington 2026-07-15 在收入与转化约束下动态决定每次搜索展示多少广告，利用随机现场实验估计供给曲线，再由轻量策略选择 ad load。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  advertising constrained-optimization marketplace 搜广推 重排、展示与长期价值 为什么搜索广告数量不能始终取使当前广告收入最大的那个值？ 广告数量同时影响收入、自然结果体验和转化，最优供给随请求而变。方法先借随机现场实验估计不同广告量的响应曲线，再在业务约束下选择请求级策略；拉格朗日权重表达目标之间的取舍。不能把相关性日志直接当增加一个广告位的因果收益，本地代理排序也未验证真实市场均衡。 示意：购物意图强的查询可容纳多个广告，导航型查询多塞广告反而妨碍用户；同样增加一格，两个请求的收入与体验变化可能相反。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-adaptive-ad-load-26eb54c1" class="ar-learning-paper-anchor"></span>
<h2 id="qa-367793246886ffd2">为什么搜索广告数量不能始终取使当前广告收入最大的那个值？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aadaptive-ad-load">Adaptive Ad Load Design for Sponsored Search Markets: Evidence, Theory, and Deployment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>广告数量同时影响收入、自然结果体验和转化，最优供给随请求而变。方法先借随机现场实验估计不同广告量的响应曲线，再在业务约束下选择请求级策略；拉格朗日权重表达目标之间的取舍。不能把相关性日志直接当增加一个广告位的因果收益，本地代理排序也未验证真实市场均衡。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>购物意图强的查询可容纳多个广告，导航型查询多塞广告反而妨碍用户；同样增加一格，两个请求的收入与体验变化可能相反。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14418">原论文</a> · <a href="../../../../reproductions/2607.14418-adaptive-ad-load/">实现解读</a> · <a href="#qa-367793246886ffd2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:downstream-rewards" data-paper-title="Long-term User Engagement Optimization through Model-agnostic Downstream Rewards Learning" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Long-term User Engagement Optimization through Model-agnostic Downstream Rewards Learning 搜广推与 LLM 应用 Pinterest 2026-07-15 只优化当前点击或保存可能牺牲用户后续活跃。Pinterest 的方法先离线提出并筛选能预测未来参与度的 downstream rewards，再把通过筛选的 reward head 作为模型无关附加目标接入 Homefeed、Search、Related Pins 和 Notifications 等不同系统，无需替换原有主排序器。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实执行 reward 筛选与附加头；Pinterest 私有跨 surface 长期标签未复刻。本地从 deeper transition、content depth、new use-case exploration 和 shallow closeup 四类 session 信号出发，以未来类型覆盖代理长期参与度做离线筛选，训练独立 reward head，再在 validation 上选择与即时排序分数的融合强度。  long-term-value reward-design multi-surface retention 搜广推 重排、展示与长期价值 下游reward为什么要先筛选对未来参与度的预测能力，而不是把所有即时行为都加进排序？ 即时行为和长期满意度可能相反，盲目增加目标会放大浅层互动或噪声。方法先提出多种下游信号并检验其与未来参与度的关系，只把通过筛选的reward head接入原有系统。预测关联仍不等于因果改善，因此跨产品接入后还需相应评价，不能把所有短期指标上涨相加当留存收益。 示意：一次点开大图可能只是误触，随后深入浏览相关收藏却更可能表示有价值的探索；先比较它们与未来活跃的关系，再决定哪种反馈值得成为附加目标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-downstream-rewards-21cba3a1" class="ar-learning-paper-anchor"></span>
<h2 id="qa-dbd417cacfc6a26d">下游reward为什么要先筛选对未来参与度的预测能力，而不是把所有即时行为都加进排序？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adownstream-rewards">Long-term User Engagement Optimization through Model-agnostic Downstream Rewards Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>即时行为和长期满意度可能相反，盲目增加目标会放大浅层互动或噪声。方法先提出多种下游信号并检验其与未来参与度的关系，只把通过筛选的reward head接入原有系统。预测关联仍不等于因果改善，因此跨产品接入后还需相应评价，不能把所有短期指标上涨相加当留存收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次点开大图可能只是误触，随后深入浏览相关收藏却更可能表示有价值的探索；先比较它们与未来活跃的关系，再决定哪种反馈值得成为附加目标。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14192">原论文</a> · <a href="../../../../reproductions/2607.14192-downstream-rewards/">实现解读</a> · <a href="#qa-dbd417cacfc6a26d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:genpage" data-paper-title="GenPage: Towards End-to-End Generative Homepage Construction at Netflix" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="GenPage: Towards End-to-End Generative Homepage Construction at Netflix 搜广推与 LLM 应用 Netflix 2026-06-30 用一个生成模型直接输出整页而非逐阶段召回排序，并在 WBC/SFT 后以生产长期奖励进行 RL 后训练，同时处理业务规则和冷启动。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation page-generation reinforcement-learning 搜广推 重排、展示与长期价值 GenPage直接生成整页，为什么还需要长期奖励后训练，而非只模仿已有页面？ 行为克隆或SFT主要重现日志中的展示分布，未必表达不同位置、内容组合对长期价值的共同影响。整页奖励把评价对象提升到页面决策，再通过后训练调整策略，同时保留业务可行性与冷启动处理。页面级建模不保证因果最优，尤其不能把公开代理列表收益当作生产长期留存。 示意：日志里每行都堆热门内容，模仿会复制这种布局；整页评价可能发现适量新内容有助持续探索，但需真实长期反馈，而不是只凭标题多样就假定收益。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-genpage-e2b0c563" class="ar-learning-paper-anchor"></span>
<h2 id="qa-fb061952942a7382">GenPage直接生成整页，为什么还需要长期奖励后训练，而非只模仿已有页面？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agenpage">GenPage: Towards End-to-End Generative Homepage Construction at Netflix</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Netflix</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>行为克隆或SFT主要重现日志中的展示分布，未必表达不同位置、内容组合对长期价值的共同影响。整页奖励把评价对象提升到页面决策，再通过后训练调整策略，同时保留业务可行性与冷启动处理。页面级建模不保证因果最优，尤其不能把公开代理列表收益当作生产长期留存。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>日志里每行都堆热门内容，模仿会复制这种布局；整页评价可能发现适量新内容有助持续探索，但需真实长期反馈，而不是只凭标题多样就假定收益。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.31031">原论文</a> · <a href="../../../../reproductions/2606.31031-genpage/">实现解读</a> · <a href="#qa-fb061952942a7382">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:piano" data-paper-title="PIANO: Personalized Reranking via Information Aggregation Node for Music Search Optimization" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="PIANO: Personalized Reranking via Information Aggregation Node for Music Search Optimization 搜广推与 LLM 应用 NetEase Cloud Music 2026-06-15 Query-Driven Interest Refiner 从历史中提取查询相关兴趣，Information Aggregation Node 汇总整张候选列表并反向条件化 item 级 CTR/CVR。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 PIANO 为 0.04988，相对变化 -7.65%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  search reranking listwise 搜广推 重排、展示与长期价值 PIANO 为什么同时提取查询相关历史兴趣，又用整张候选列表反向条件化单品预测？ 查询相关兴趣帮助模型从历史中选出当前搜索意图需要的部分；列表聚合节点则让单品 CTR/CVR 预测知道它处于怎样的候选集合中。前者解决用户历史与查询匹配，后者处理候选间的上下文关系。列表一变，条件化得分也可能变化，因此不能把它当作对每件商品独立、可任意跨列表复用的分数。 示意：用户平时买跑鞋，当前搜索登山鞋；先聚焦户外相关历史。同一双鞋放在全是高价专业鞋的列表中，与放在入门款列表中，选择概率也可能不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-piano-1fe78019" class="ar-learning-paper-anchor"></span>
<h2 id="qa-0c7a8b51cd4bdf5b">PIANO 为什么同时提取查询相关历史兴趣，又用整张候选列表反向条件化单品预测？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apiano">PIANO: Personalized Reranking via Information Aggregation Node for Music Search Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NetEase Cloud Music</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>查询相关兴趣帮助模型从历史中选出当前搜索意图需要的部分；列表聚合节点则让单品 CTR/CVR 预测知道它处于怎样的候选集合中。前者解决用户历史与查询匹配，后者处理候选间的上下文关系。列表一变，条件化得分也可能变化，因此不能把它当作对每件商品独立、可任意跨列表复用的分数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户平时买跑鞋，当前搜索登山鞋；先聚焦户外相关历史。同一双鞋放在全是高价专业鞋的列表中，与放在入门款列表中，选择概率也可能不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.16641">原论文</a> · <a href="../../../../reproductions/2606.16641-piano/">实现解读</a> · <a href="#qa-0c7a8b51cd4bdf5b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:taiji" data-paper-title="Taiji: Pareto Optimal Policy Optimization with Semantics-IDs Trade-off for Industrial LLM-Enhanced Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Taiji: Pareto Optimal Policy Optimization with Semantics-IDs Trade-off for Industrial LLM-Enhanced Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-06-02 先用反向工程偏好推理与拒绝采样激活推荐 CoT，再由 POPO 动态平衡 LLM 语义奖励和推荐协同 ID 奖励，避免固定权重遗漏非凸 Pareto 前沿。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.06448，相对变化 +19.39%。本地代理目标与论文生产任务不同，不能外推线上 lift。  advertising reinforcement-alignment pareto-optimization 搜广推 重排、展示与长期价值 TAIJI 为什么动态平衡语义奖励和协同 ID 奖励，而不使用一组固定权重？ 语义奖励衡量内容与解释的契合，协同奖励反映行为关系，不同样本可能需要不同取舍。固定加权只搜索有限方向，尤其可能遗漏非凸前沿上的有用方案；动态权重试图适配这些差异。反向偏好推理和拒绝采样先激活推荐推理，再做多目标对齐，但动态权重仍不能保证识别真实用户最优偏好。 示意：冷门新品缺乏行为反馈时多借语义，热门商品有充分交互时可更依赖协同信号。若所有样本都用七比三，可能同时不适合这两类物品。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-taiji-2fa562ab" class="ar-learning-paper-anchor"></span>
<h2 id="qa-681897908cf2d793">TAIJI 为什么动态平衡语义奖励和协同 ID 奖励，而不使用一组固定权重？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ataiji">Taiji: Pareto Optimal Policy Optimization with Semantics-IDs Trade-off for Industrial LLM-Enhanced Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语义奖励衡量内容与解释的契合，协同奖励反映行为关系，不同样本可能需要不同取舍。固定加权只搜索有限方向，尤其可能遗漏非凸前沿上的有用方案；动态权重试图适配这些差异。反向偏好推理和拒绝采样先激活推荐推理，再做多目标对齐，但动态权重仍不能保证识别真实用户最优偏好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>冷门新品缺乏行为反馈时多借语义，热门商品有充分交互时可更依赖协同信号。若所有样本都用七比三，可能同时不适合这两类物品。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.03866">原论文</a> · <a href="../../../../reproductions/2606.03866-taiji/">实现解读</a> · <a href="#qa-681897908cf2d793">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:primal-dual-decoding" data-paper-title="Stochastic Primal-Dual Decoding for Multiobjective Generative Recommender Systems" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Stochastic Primal-Dual Decoding for Multiobjective Generative Recommender Systems 搜广推与 LLM 应用 Spotify 2026-05-26 不重训生成式推荐模型，在逐位置解码时把相关性 logits 与辅助目标贡献相加，并根据剩余约束松弛量以镜像下降动态更新拉格朗日乘子。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.02109，相对变化 -60.95%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation multiobjective constrained-decoding 搜广推 重排、展示与长期价值 原始—对偶解码为什么要随剩余约束动态调整乘子，而不是固定加一个多样性分？ 固定权重无法根据已经生成的内容判断约束是否快要违约。原始—对偶解码在每个位置组合模型分数与辅助目标贡献，并按当前约束松弛量更新乘子，使后续选择补偿前面决策。不需要重训生成器，但只能在可选候选与局部解码范围内权衡，也可能牺牲相关性；并非所有硬约束都能自动满足。 示意：一张五条列表希望至少两条来自新作者。前四条只选到一条时，最后一步应提高新作者贡献权重；若早已满足，则无需继续用同样强度挤压相关性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-primal-dual-decoding-161adf1d" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1804a3b129c4958e">原始—对偶解码为什么要随剩余约束动态调整乘子，而不是固定加一个多样性分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aprimal-dual-decoding">Stochastic Primal-Dual Decoding for Multiobjective Generative Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Spotify</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定权重无法根据已经生成的内容判断约束是否快要违约。原始—对偶解码在每个位置组合模型分数与辅助目标贡献，并按当前约束松弛量更新乘子，使后续选择补偿前面决策。不需要重训生成器，但只能在可选候选与局部解码范围内权衡，也可能牺牲相关性；并非所有硬约束都能自动满足。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一张五条列表希望至少两条来自新作者。前四条只选到一条时，最后一步应提高新作者贡献权重；若早已满足，则无需继续用同样强度挤压相关性。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.19357">原论文</a> · <a href="../../../../reproductions/2607.19357-primal-dual-decoding/">实现解读</a> · <a href="#qa-1804a3b129c4958e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:degre" data-paper-title="DeGRe: Listwise Generative Reranking with Offline Lookahead Distillation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DeGRe: Listwise Generative Reranking with Offline Lookahead Distillation 搜广推与 LLM 应用 Alibaba Group / Zhejiang University 2026-05-25 逐点生成器只学习日志中的单一路径，难以直接优化整张列表的长期价值。DeGRe 离线训练累计回报 evaluator，用 beam search 探索高价值列表，再把每个前缀下所有剩余候选的前瞻价值蒸馏为 dense soft label；线上只保留一次 greedy generator。 Fidelity: 核心机制复现。累计价值评估器、lookahead beam mining、逐前缀 dense label、beam weighting 与单次在线生成路径均实际执行。未复刻私有交易标签与工业 Transformer 规模；本地结果仅验证离线 evaluator→beam mining→dense distillation 链路。本地对照口径：基线是相同候选与特征的 pointwise generator；实验组 DeGRe 加入离线前瞻蒸馏，相对基线 Hit@10 +0.00%、NDCG@10 +3.31%。  generative-recommendation reranking distillation 搜广推 重排、展示与长期价值 DeGRe离线做beam前瞻，为什么上线却只保留greedy generator？ 前瞻evaluator能比较不同前缀及其后续列表价值，但在线逐步搜索成本高。DeGRe离线探索高价值列表，再把每个前缀下剩余候选的价值分布蒸馏为软标签，让生成器在单步选择中近似吸收未来影响。蒸馏的是估计价值而非真实最优策略，evaluator偏差也可能被一起固化。 示意：第一项点分最高的候选可能使后面只能选重复内容；离线搜索发现另一开头能组成更好整页，再教greedy模型优先选它，而非上线每次重搜所有排列。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-degre-898bafc1" class="ar-learning-paper-anchor"></span>
<h2 id="qa-fa97ae7183cd68ce">DeGRe离线做beam前瞻，为什么上线却只保留greedy generator？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adegre">DeGRe: Listwise Generative Reranking with Offline Lookahead Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group / Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前瞻evaluator能比较不同前缀及其后续列表价值，但在线逐步搜索成本高。DeGRe离线探索高价值列表，再把每个前缀下剩余候选的价值分布蒸馏为软标签，让生成器在单步选择中近似吸收未来影响。蒸馏的是估计价值而非真实最优策略，evaluator偏差也可能被一起固化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第一项点分最高的候选可能使后面只能选重复内容；离线搜索发现另一开头能组成更好整页，再教greedy模型优先选它，而非上线每次重搜所有排列。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.25749">原论文</a> · <a href="../../../../reproductions/2605.25749-degre/">实现解读</a> · <a href="#qa-fa97ae7183cd68ce">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:prl-puts" data-paper-title="A Production-Ready RL Framework for Personalized Utility Tuning with Pareto Sweeping in Pinterest Recommender Systems" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="A Production-Ready RL Framework for Personalized Utility Tuning with Pareto Sweeping in Pinterest Recommender Systems 搜广推与 LLM 应用 Pinterest 2026-05-08 双头 Q 网络分别估计 Repin 与 P2P utility，再通过 Pareto sweeping 离线筛选不劣策略；线上仅切换可治理的权重策略，不更换模型。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 prl-puts 核心机制，相对 NDCG@10 +39.64%。  reinforcement-learning multi-objective-ranking homefeed 搜广推 重排、展示与长期价值 PRL-PUTS 为什么用双头 Q 值和 Pareto sweeping 预选权重，而不线上随意调单一奖励？ 两个 Q 头分别估计不同业务效用，权重组合对应不同策略取舍。离线扫描权重并筛掉被其他策略同时支配的选择，可形成可治理的候选前沿；线上切换权重即可改变目标平衡，无须替换整套模型。但 Q 值误差和分布变化仍影响前沿可靠性，离线不劣不能直接推出线上更优。 示意：一组权重带来更多收藏，另一组带来更多后续互动。若某组两项都更差就先淘汰；保留下来的取舍点再供业务选择，而不是在真实流量里盲目搜索所有权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-prl-puts-9d4fc321" class="ar-learning-paper-anchor"></span>
<h2 id="qa-5b30234155339f02">PRL-PUTS 为什么用双头 Q 值和 Pareto sweeping 预选权重，而不线上随意调单一奖励？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aprl-puts">A Production-Ready RL Framework for Personalized Utility Tuning with Pareto Sweeping in Pinterest Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两个 Q 头分别估计不同业务效用，权重组合对应不同策略取舍。离线扫描权重并筛掉被其他策略同时支配的选择，可形成可治理的候选前沿；线上切换权重即可改变目标平衡，无须替换整套模型。但 Q 值误差和分布变化仍影响前沿可靠性，离线不劣不能直接推出线上更优。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一组权重带来更多收藏，另一组带来更多后续互动。若某组两项都更差就先淘汰；保留下来的取舍点再供业务选择，而不是在真实流量里盲目搜索所有权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.16344">原论文</a> · <a href="../../../../reproductions/2605.16344-prl-puts/">实现解读</a> · <a href="#qa-5b30234155339f02">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:glorank" data-paper-title="From Local Indices to Global Identifiers: Generative Reranking via Global Action Space" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="From Local Indices to Global Identifiers: Generative Reranking via Global Action Space 搜广推与 LLM 应用 City University of Hong Kong / Kuaishou / UC San Diego 2026-04-28 全局 Semantic ID 空间把局部候选重排改写为全库生成；先做 listwise SFT，再用组相对奖励优化列表效用与长尾覆盖。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 glorank 核心机制；相对 NDCG@10 -44.26%。  reranking generative-recommendation semantic-id reinforcement-learning 搜广推 重排、展示与长期价值 GloRank把局部候选编号换成全局SID后，为什么任务已超出普通重排？ 局部编号只能指向上游给定的候选，生成这些编号仍受候选池上限限制。全局SID让模型在更大目录中表达选择，训练因而同时承担物品定位与列表效用对齐，不只是给既有项目换顺序。扩大动作空间也增加搜索与合法性难度，不能沿用封闭候选重排的简单评测口径。 示意：局部列表里只有十件商品，输出编号十一没有含义；全局码可指向原列表外的物品，但必须验证它在目录中可服务，而不是把新增搜索空间免费当成收益。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-glorank-9a7d512b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-0bebbdd575e1cb4b">GloRank把局部候选编号换成全局SID后，为什么任务已超出普通重排？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aglorank">From Local Indices to Global Identifiers: Generative Reranking via Global Action Space</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · City University of Hong Kong / Kuaishou / UC San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>局部编号只能指向上游给定的候选，生成这些编号仍受候选池上限限制。全局SID让模型在更大目录中表达选择，训练因而同时承担物品定位与列表效用对齐，不只是给既有项目换顺序。扩大动作空间也增加搜索与合法性难度，不能沿用封闭候选重排的简单评测口径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>局部列表里只有十件商品，输出编号十一没有含义；全局码可指向原列表外的物品，但必须验证它在目录中可服务，而不是把新增搜索空间免费当成收益。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.25291">原论文</a> · <a href="../../../../reproductions/2604.25291-glorank/">实现解读</a> · <a href="#qa-0bebbdd575e1cb4b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dual-rerank" data-paper-title="Dual-Rerank: Fusing Sequential Dependencies and Utility for Generative Reranking" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Dual-Rerank: Fusing Sequential Dependencies and Utility for Generative Reranking 搜广推与 LLM 应用 Kuaishou Technology 2026-04-08 AR 教师学习物品间顺序依赖，NAR 学生并行估计名次；效用蒸馏把效果与延迟共同写入训练目标。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 dual-rerank 核心机制；相对 NDCG@10 +10.66%。  reranking knowledge-distillation listwise-rl serving 搜广推 重排、展示与长期价值 Dual-Rerank的非自回归学生并行输出，怎样吸收自回归教师的顺序依赖？ 教师逐项条件化已有前缀，能学习列表中物品之间的作用，但服务成本随生成步骤增加。学生通过排序分布与utility蒸馏，把教师的顺序偏好压入可并行的名次估计，减少上线逐步调用。蒸馏只能近似教师依赖，并不使并行学生天然等价于每个前缀都重新计算的自回归模型。 示意：教师知道先展示教程会改变后面器材的价值，学生学习这种整体名次模式后一次给出列表；遇到新组合时仍可能无法完全复现教师的逐步判断。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-dual-rerank-e775c831" class="ar-learning-paper-anchor"></span>
<h2 id="qa-5a932ffec24fac84">Dual-Rerank的非自回归学生并行输出，怎样吸收自回归教师的顺序依赖？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adual-rerank">Dual-Rerank: Fusing Sequential Dependencies and Utility for Generative Reranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>教师逐项条件化已有前缀，能学习列表中物品之间的作用，但服务成本随生成步骤增加。学生通过排序分布与utility蒸馏，把教师的顺序偏好压入可并行的名次估计，减少上线逐步调用。蒸馏只能近似教师依赖，并不使并行学生天然等价于每个前缀都重新计算的自回归模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教师知道先展示教程会改变后面器材的价值，学生学习这种整体名次模式后一次给出列表；遇到新组合时仍可能无法完全复现教师的逐步判断。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.07420">原论文</a> · <a href="../../../../reproductions/2604.07420-dual-rerank/">实现解读</a> · <a href="#qa-5a932ffec24fac84">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:safro" data-paper-title="SaFRO: Satisfaction-Aware Fusion via Dual-Relative Policy Optimization for Short-Video Search" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="SaFRO: Satisfaction-Aware Fusion via Dual-Relative Policy Optimization for Short-Video Search 搜广推与 LLM 应用 Kuaishou Technology 2026-03-20 满意度 reward 同时建模即时互动与长期留存，Dual-Relative PO 在组内和任务间归一化优势，关系门控融合多搜索目标。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 safro 核心机制，相对 NDCG@10 +81.86%。  search-ranking reinforcement-learning multi-task-learning 搜广推 重排、展示与长期价值 SAFRO 为什么在组内和任务间都做相对 advantage 归一化？ 即时互动与长期留存的奖励尺度及难度可能不同，直接混合会让方差大或数值大的目标主导更新。组内归一化表达同一目标下哪些候选更好，任务间相对项再比较同一候选的多目标表现，关系门控组织搜索目标。归一化改善可比性，却不能自动决定长期价值权重，也不代表所有目标同时提升。 示意：点击分通常很密集，留存分稀疏且尺度更大。先在各自候选组里比较，再处理任务间差异，可减少模型只追逐数值最大的那一种奖励。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-safro-95b49eda" class="ar-learning-paper-anchor"></span>
<h2 id="qa-20b5c57f1b03818c">SAFRO 为什么在组内和任务间都做相对 advantage 归一化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asafro">SaFRO: Satisfaction-Aware Fusion via Dual-Relative Policy Optimization for Short-Video Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>即时互动与长期留存的奖励尺度及难度可能不同，直接混合会让方差大或数值大的目标主导更新。组内归一化表达同一目标下哪些候选更好，任务间相对项再比较同一候选的多目标表现，关系门控组织搜索目标。归一化改善可比性，却不能自动决定长期价值权重，也不代表所有目标同时提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>点击分通常很密集，留存分稀疏且尺度更大。先在各自候选组里比较，再处理任务间差异，可减少模型只追逐数值最大的那一种奖励。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.19585">原论文</a> · <a href="../../../../reproductions/2603.19585-safro/">实现解读</a> · <a href="#qa-20b5c57f1b03818c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cgr" data-paper-title="Constraint-Aware Generative Re-ranking for Multi-Objective Optimization in Advertising Feeds" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Constraint-Aware Generative Re-ranking for Multi-Objective Optimization in Advertising Feeds 搜广推与 LLM 应用 Bilibili 2026-03-04 CGR 用一个网络同时完成序列生成和奖励估计，将广告位、广告负载等业务规则直接写入自回归解码；约束感知奖励剪枝提前排除不可行分支，避免生成后的启发式修补。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05715，相对变化 +5.82%。本地代理目标与论文生产任务不同，不能外推线上 lift。  advertising generative-reranking constraint-optimization 搜广推 重排、展示与长期价值 CGR把广告负载约束放进解码，和列表生成后再删掉多余广告有什么不同？ 事后删除会改变上下文和剩余配额，原来为某个前缀估计的价值可能不再成立。CGR在逐步生成时维护可行集合，并结合奖励估计提前剪去不可行分支，使搜索预算集中在满足业务规则的列表上。它优化的是受约束的整体选择，不能把高分但不可执行的列表当作有效输出。 示意：五个位置最多允许两个广告，前两步已用满配额时，后续直接屏蔽广告；若先生成四个广告再删，剩余位置和原预测列表已不是同一对象。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-cgr-09571847" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1e6e21fd686061f7">CGR把广告负载约束放进解码，和列表生成后再删掉多余广告有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acgr">Constraint-Aware Generative Re-ranking for Multi-Objective Optimization in Advertising Feeds</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Bilibili</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>事后删除会改变上下文和剩余配额，原来为某个前缀估计的价值可能不再成立。CGR在逐步生成时维护可行集合，并结合奖励估计提前剪去不可行分支，使搜索预算集中在满足业务规则的列表上。它优化的是受约束的整体选择，不能把高分但不可执行的列表当作有效输出。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>五个位置最多允许两个广告，前两步已用满配额时，后续直接屏蔽广告；若先生成四个广告再删，剩余位置和原预测列表已不是同一对象。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.04227">原论文</a> · <a href="../../../../reproductions/2603.04227-cgr/">实现解读</a> · <a href="#qa-1e6e21fd686061f7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ltv-video-ranking" data-paper-title="A Long-term Value Prediction Framework In Video Ranking" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="A Long-term Value Prediction Framework In Video Ranking 搜广推与 LLM 应用 Alibaba Group / Tsinghua University 2026-02-19 PDQ 消除位置偏差，归因模块分配会话内长期价值，作者周期任务再引入跨日优质创作者价值。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 ltv-video-ranking 核心机制，相对 NDCG@10 +9.73%。  ranking long-term-value debiasing 搜广推 重排、展示与长期价值 LTV视频排序为什么先处理位置偏差，再把会话与跨日创作者价值纳入目标？ 前排内容更容易被看到，直接把观测互动当长期价值可能奖励展示机会而非真正贡献。位置校正先尽量对齐可比反馈，再通过会话归因与作者周期任务表达更长时间范围的价值。位置分位映射和长期归因各有假设，不能把两者叠加后的分数直接解释成已识别的因果留存增量。 示意：一个创作者总被放首位因而互动高，另一个常在后排；先控制展示机会，再看谁带来后续持续消费，才不至于把排位优势误当长期内容价值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-ltv-video-ranking-a90843c2" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d76f2f5cf0db518c">LTV视频排序为什么先处理位置偏差，再把会话与跨日创作者价值纳入目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Altv-video-ranking">A Long-term Value Prediction Framework In Video Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group / Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前排内容更容易被看到，直接把观测互动当长期价值可能奖励展示机会而非真正贡献。位置校正先尽量对齐可比反馈，再通过会话归因与作者周期任务表达更长时间范围的价值。位置分位映射和长期归因各有假设，不能把两者叠加后的分数直接解释成已识别的因果留存增量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个创作者总被放首位因而互动高，另一个常在后排；先控制展示机会，再看谁带来后续持续消费，才不至于把排位优势误当长期内容价值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.17058">原论文</a> · <a href="../../../../reproductions/2602.17058-ltv-video-ranking/">实现解读</a> · <a href="#qa-d76f2f5cf0db518c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:spatial-ads" data-paper-title="Online Advertising with Spatial Interactions" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Online Advertising with Spatial Interactions 搜广推与 LLM 应用 Google Research 2026-02-12 传统逐位置竞价忽略屏幕上的空间干扰。论文将最近邻外部性问题约化到分组伪圆盘选择，再将LP解舍入为可行圆盘集合；同时研究可分解价值的简单拍卖、二维PTAS与乘积距离模型的困难性。实现范围为v1 §2.2 Algorithm1及Eq2。 论文没有完整训练实验，故full_experiment_status=not_applicable_theoretical_paper，不伪造“高成本不复现”理由。属于L1机制诊断，不是线上广告收益。自建3点度量、3个圆盘的数学测试；检查LP可行、所有采样满足约束II，并以独立种子检验边际保留概率接近。属于L1机制诊断，不是线上广告收益。CPU无需GPU；稳定记录见metrics/component-cpu-seed42.json。  空间外部性与广告分配 LP随机舍入 搜广推 重排、展示与长期价值 Spatial Ads 的 LP 舍入为什么针对整个原始采样集合判冲突，而不是按贪心已选集合逐个接受？ 圆盘选择同时受空间冲突与同组约束，独立采样后的保留概率修正基于原始采样事件推导。若改成贪心逐个接受，后面的条件分布与冲突概率就变了，不能沿用原保证。真正求解 LP 并按规定舍入，是这里的算法核心；本地仅做小规模数学诊断，未验证线上广告收益。 示意：两个广告圆盘互相冲突，贪心先留下甲会改变乙面对的条件。原算法先固定整份随机采样，再据其中所有冲突决定保留，不能把二者当作同一个过程。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-spatial-ads-1dbea82c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-62aed40bc12e6f28">Spatial Ads 的 LP 舍入为什么针对整个原始采样集合判冲突，而不是按贪心已选集合逐个接受？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aspatial-ads">Online Advertising with Spatial Interactions</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>圆盘选择同时受空间冲突与同组约束，独立采样后的保留概率修正基于原始采样事件推导。若改成贪心逐个接受，后面的条件分布与冲突概率就变了，不能沿用原保证。真正求解 LP 并按规定舍入，是这里的算法核心；本地仅做小规模数学诊断，未验证线上广告收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个广告圆盘互相冲突，贪心先留下甲会改变乙面对的条件。原算法先固定整份随机采样，再据其中所有冲突决定保留，不能把二者当作同一个过程。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12481">原论文</a> · <a href="../../../../recommendation-components/2602.12481-spatial-ads/">实现解读</a> · <a href="#qa-62aed40bc12e6f28">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hcub" data-paper-title="Hierarchical Contextual Uplift Bandits for Catalog Personalization" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Hierarchical Contextual Uplift Bandits for Catalog Personalization 搜广推与 LLM 应用 Dream11 2026-01-20 在用户与系统上下文树上动态选择粒度，并让父节点奖励向稀疏子节点继承以改善冷启动；策略直接估计动作的增量收益，而不是只拟合观察到的绝对点击。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04886，相对变化 -9.53%。本地代理目标与论文生产任务不同，不能外推线上 lift。  bandit uplift-modeling catalog-personalization 搜广推 重排、展示与长期价值 HCUB为什么让稀疏上下文继承父节点奖励，同时仍保留探索项？ 细粒度用户群体数据少，完全独立估计会高方差；继承父节点提供较稳定起点，随着本地反馈增加再提高专属信息权重。动作选择依据增量收益并加入不确定性探索，避免永久锁定早期看似最好的动作。层级共享也可能掩盖少数群体差异，因此不能用父节点平均值替代所有局部证据。 示意：新出现的某设备用户群只有几次反馈，可先借更大地域群体经验；后续若本地偏好不同，估计应逐渐改写，而探索让这种差异有机会被发现。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-hcub-b171df10" class="ar-learning-paper-anchor"></span>
<h2 id="qa-92bc40ad4dfe9d20">HCUB为什么让稀疏上下文继承父节点奖励，同时仍保留探索项？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahcub">Hierarchical Contextual Uplift Bandits for Catalog Personalization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dream11</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>细粒度用户群体数据少，完全独立估计会高方差；继承父节点提供较稳定起点，随着本地反馈增加再提高专属信息权重。动作选择依据增量收益并加入不确定性探索，避免永久锁定早期看似最好的动作。层级共享也可能掩盖少数群体差异，因此不能用父节点平均值替代所有局部证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新出现的某设备用户群只有几次反馈，可先借更大地域群体经验；后续若本地偏好不同，估计应逐渐改写，而探索让这种差异有机会被发现。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.14333">原论文</a> · <a href="../../../../reproductions/2601.14333-hcub/">实现解读</a> · <a href="#qa-92bc40ad4dfe9d20">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:harmonrank" data-paper-title="Rethinking Multi-objective Ranking Ensemble in Recommender System: From Score Fusion to Rank Consistency" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Rethinking Multi-objective Ranking Ensemble in Recommender System: From Score Fusion to Rank Consistency 搜广推与 LLM 应用 Kuaishou Technology 2026-01-06 第一阶段将 AUC 改写为可微 rank-sum 目标，使各任务从分类分数转向排序对齐；第二阶段用目标间 self-attention 学习购买、评论等目标的依赖，再输出统一序。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05203，相对变化 -3.65%。本地代理目标与论文生产任务不同，不能外推线上 lift。  multi-objective-ranking rank-consistency ensemble 搜广推 重排、展示与长期价值 HarmonRank为什么先对齐各任务的名次，而不是直接融合未经处理的预测概率？ 不同目标的概率尺度与标签频率不一致，直接融合容易受校准或稀疏程度支配。可微rank-sum目标先让任务学习相对次序，再以任务间attention表示购买、评论等依赖并给出统一排序。名次对齐不保留全部绝对概率信息，适用目标和约束仍需单独检查，不能把它当通用概率校准器。 示意：购买率通常比点击率小很多，直接相加时点击可能压倒购买；先比较候选在各任务中的相对次序，再学习任务关系，可减少这种纯数值尺度支配。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-harmonrank-1abfcd00" class="ar-learning-paper-anchor"></span>
<h2 id="qa-460ed145b6ab2671">HarmonRank为什么先对齐各任务的名次，而不是直接融合未经处理的预测概率？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aharmonrank">Rethinking Multi-objective Ranking Ensemble in Recommender System: From Score Fusion to Rank Consistency</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同目标的概率尺度与标签频率不一致，直接融合容易受校准或稀疏程度支配。可微rank-sum目标先让任务学习相对次序，再以任务间attention表示购买、评论等依赖并给出统一排序。名次对齐不保留全部绝对概率信息，适用目标和约束仍需单独检查，不能把它当通用概率校准器。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>购买率通常比点击率小很多，直接相加时点击可能压倒购买；先比较候选在各任务中的相对次序，再学习任务关系，可减少这种纯数值尺度支配。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.02955">原论文</a> · <a href="../../../../reproductions/2601.02955-harmonrank/">实现解读</a> · <a href="#qa-460ed145b6ab2671">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:higr" data-paper-title="HiGR: Industrial-Scale Hierarchical Generative Slate Recommendation Framework in Tencent" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="HiGR: Industrial-Scale Hierarchical Generative Slate Recommendation Framework in Tencent 搜广推与 LLM 应用 Tencent 2025-12-31 逐物品生成忽略 slate 内相互作用。HiGR 用 PCRQ-VAE 得到层级语义 ID，Hierarchical Slate Decoder 先选簇再选物品，并通过 ORPO 对齐整页偏好。 多样性更好但精度下降，未复现线上收益。Fidelity: 核心机制复现。实际学习两级 residual semantic ID，执行 coarse-to-fine slate 解码和 ORPO 风格偏好重排。MovieLens 单物品 next-item 目标并非视频 slate 反馈；本地 k-means residual ID 不等价于生产 PCRQ-VAE。本地对照口径：相对 flat item slate 基线，实验组 NDCG@10 -12.32%。  generative-recommendation slate-recommendation semantic-id preference-optimization 搜广推 重排、展示与长期价值 HiGR先选语义簇再选物品，为什么还需要整页偏好对齐？ 层级ID降低了物品定位难度，但分别选中相关物品并不保证列表互补与顺序合理。Hierarchical Slate Decoder组织粗到细生成，ORPO再用好坏整页偏好调整组合分布。偏好反馈仍只覆盖已评估组合，不能因为有层级结构就声称长尾覆盖或页面效用必然提高。 示意：簇级选择都命中运动主题，生成结果却可能全是近似跑鞋；整页偏好可教模型换入袜子或训练内容，而不只是逐个奖励主题相关。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-higr-d87ebf0f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f29b5cfbf4107740">HiGR先选语义簇再选物品，为什么还需要整页偏好对齐？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahigr">HiGR: Industrial-Scale Hierarchical Generative Slate Recommendation Framework in Tencent</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>层级ID降低了物品定位难度，但分别选中相关物品并不保证列表互补与顺序合理。Hierarchical Slate Decoder组织粗到细生成，ORPO再用好坏整页偏好调整组合分布。偏好反馈仍只覆盖已评估组合，不能因为有层级结构就声称长尾覆盖或页面效用必然提高。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>簇级选择都命中运动主题，生成结果却可能全是近似跑鞋；整页偏好可教模型换入袜子或训练内容，而不只是逐个奖励主题相关。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2512.24787">原论文</a> · <a href="../../../../reproductions/2512.24787-higr/">实现解读</a> · <a href="#qa-f29b5cfbf4107740">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:drl-put" data-paper-title="Deep Reinforcement Learning for Ranking Utility Tuning in the Ad Recommender System at Pinterest" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Deep Reinforcement Learning for Ranking Utility Tuning in the Ad Recommender System at Pinterest 搜广推与 LLM 应用 Pinterest 2025-09-05 广告排序的相关性、CTR、CVR 和收益权重通常靠人工调节。DRL-PUT 把权重组合视为动作，依据用户/请求状态选择动作，并从 logged behavior 和组合 reward 学习策略。 Fidelity: 核心机制复现。从公开交互构造带 propensity 的日志策略，并用 REINFORCE 学习效用权重动作。公开评分代理点击和收益，无法重建 Pinterest 拍卖、真实 counterfactual reward 与广告主约束。本地对照口径：相对固定 utility 权重基线，实验组 NDCG@10 +19.13%。  ads-ranking reinforcement-learning utility-tuning off-policy 搜广推 重排、展示与长期价值 DRL-PUT学习的是推荐物品本身，还是多个utility分数的组合方式？ 动作是相关性、CTR、CVR等分数的权重配置，策略依据请求状态决定如何组合已有预测器。这样可以在不替换所有底层模型的情况下适配业务取舍；离线利用日志策略概率校正动作分布差异。若某些权重在历史中几乎没被采用，就缺少可靠反馈支持，不能凭离线大权重宣称线上最优。 示意：同一批广告已有点击与转化分，策略可对探索型请求更重相关性，对明确购买请求更重转化；变化的是决策组合，而非重新生成所有广告表示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-drl-put-ba6d0f54" class="ar-learning-paper-anchor"></span>
<h2 id="qa-a39e4cbdc0eedaf9">DRL-PUT学习的是推荐物品本身，还是多个utility分数的组合方式？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adrl-put">Deep Reinforcement Learning for Ranking Utility Tuning in the Ad Recommender System at Pinterest</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>动作是相关性、CTR、CVR等分数的权重配置，策略依据请求状态决定如何组合已有预测器。这样可以在不替换所有底层模型的情况下适配业务取舍；离线利用日志策略概率校正动作分布差异。若某些权重在历史中几乎没被采用，就缺少可靠反馈支持，不能凭离线大权重宣称线上最优。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一批广告已有点击与转化分，策略可对探索型请求更重相关性，对明确购买请求更重转化；变化的是决策组合，而非重新生成所有广告表示。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2509.05292">原论文</a> · <a href="../../../../reproductions/2509.05292-drl-put/">实现解读</a> · <a href="#qa-a39e4cbdc0eedaf9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sort-gen" data-paper-title="A Generative Re-ranking Model for List-level Multi-objective Optimization at Taobao" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="A Generative Re-ranking Model for List-level Multi-objective Optimization at Taobao 搜广推与 LLM 应用 Alibaba / Taobao &amp; Tmall 2025-05-12 传统公式或 LTR 在 item level 优化 CTR、CVR、GMV，无法建模已选前缀对后续 item 的影响。SORT-Gen 用 causal Transformer 输入 item、user、position 和上游 CTR/CVR score，在每个前缀位置预测“累计行为数是否至少达到第档”的 ordered-regression 概率，从而估计加入 item 后的列表边际价值。推理先建立 CLICK、PAY、GMV 等目标队列，把搜索空间从全部候选降到队首。 Fidelity: 核心机制复现。实际训练 causal Transformer ordered regression，并执行多目标队列、mask-driven 单次批量评分和 MMR；私有曝光与线上 kernel 缩小。MovieLens rating/genre/popularity 分别代理点击、交易、商品内容和上游 score；没有淘宝真实曝光、CVR/GMV、用户商业特征和多模态 embedding。单次调用是 PyTorch 批量路径，不等价于论文生产 19 ms kernel；本地 proxy 指标不能和线上百分比直接比较。  reranking multi-objective ordered-regression diversity 搜广推 重排、展示与长期价值 SORT-Gen 为什么用累计行为数的 ordered regression 估计前缀价值，而不把单品 CTR 相加？ 单品分数忽略已选列表对下一物品的影响。ordered regression 在每个前缀预测累计行为是否达到各档，从分布估计加入候选后的边际价值；目标队列减少搜索候选，张量掩码加速批量评估，MMR 直接参与选择。它建模的是列表条件价值，仍依赖代理标签和搜索范围，不能把加速队列当作全局最优搜索。 示意：前两条已经是相似手机，再放第三条手机未必增加多少互动。模型比较加入耳机后的累计行为分布，而不是只看第三条手机独立 CTR 是否略高。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-sort-gen-b1c957ea" class="ar-learning-paper-anchor"></span>
<h2 id="qa-ef21fc2427c55791">SORT-Gen 为什么用累计行为数的 ordered regression 估计前缀价值，而不把单品 CTR 相加？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asort-gen">A Generative Re-ranking Model for List-level Multi-objective Optimization at Taobao</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao &amp; Tmall</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单品分数忽略已选列表对下一物品的影响。ordered regression 在每个前缀预测累计行为是否达到各档，从分布估计加入候选后的边际价值；目标队列减少搜索候选，张量掩码加速批量评估，MMR 直接参与选择。它建模的是列表条件价值，仍依赖代理标签和搜索范围，不能把加速队列当作全局最优搜索。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>前两条已经是相似手机，再放第三条手机未必增加多少互动。模型比较加入耳机后的累计行为分布，而不是只看第三条手机独立 CTR 是否略高。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.07197">原论文</a> · <a href="../../../../reproductions/2505.07197-sort-gen/">实现解读</a> · <a href="#qa-ef21fc2427c55791">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cdm" data-paper-title="Contextual Distillation Model for Diversified Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Contextual Distillation Model for Diversified Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2024-06-13 先用可控 MMR 教师产生兼顾相关性与多样性的列表，再把上下文边际收益蒸馏到可低延迟服务的学生。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 cdm 核心机制；相对 NDCG@10 +1.25%。  reranking diversity knowledge-distillation 搜广推 重排、展示与长期价值 CDM把MMR教师蒸馏给学生，学生为什么必须看同请求候选的上下文？ 一个物品是否被MMR选中取决于其他候选及其重复程度，单看物品本身无法恢复这种集合关系。CDM学习目标物品相对上下文的入选倾向，再与原推荐分结合，把昂贵的逐步去冗余知识转成可服务的评分。学生近似不保证完全复刻教师列表，本地缩小实验也不能推出生产多样性收益。 示意：同一段旅行视频，在十段近似视频里可能被淘汰，在全是做饭视频的列表中却很独特；不输入候选上下文，学生无法区分这两种情况。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-cdm-24f0cce6" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1ab2a07320495384">CDM把MMR教师蒸馏给学生，学生为什么必须看同请求候选的上下文？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acdm">Contextual Distillation Model for Diversified Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一个物品是否被MMR选中取决于其他候选及其重复程度，单看物品本身无法恢复这种集合关系。CDM学习目标物品相对上下文的入选倾向，再与原推荐分结合，把昂贵的逐步去冗余知识转成可服务的评分。学生近似不保证完全复刻教师列表，本地缩小实验也不能推出生产多样性收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一段旅行视频，在十段近似视频里可能被淘汰，在全是做饭视频的列表中却很独特；不输入候选上下文，学生无法区分这两种情况。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2406.09021">原论文</a> · <a href="../../../../reproductions/2406.09021-cdm/">实现解读</a> · <a href="#qa-1ab2a07320495384">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

把单个物品按分数排好，为什么还不等于一张好列表？

## 记住这一点

列表价值依赖邻居、位置和已选前缀。去冗余方法比较新增物品的边际贡献；SORT-Gen用前缀条件估计列表多目标价值；策略方法再调整探索、广告量、收益与长期反馈的取舍。标题、创意和页面布局也会改变用户看到什么，需把内容选择与呈现决策放进同一评估口径。

## 一个例子

前三个候选都是同一滑雪镜头，分数为0.90、0.89、0.88，第四个是0.85的露营视频。逐项排序会选前三个；若重复内容的边际价值下降，列表模型可能选第四个。但是否值得牺牲即时分数，需要用相应目标与约束判断。

## 什么时候要小心

把多个目标加权，不保证满足广告量或覆盖率的硬约束；提高多样性也不必然提高满意度。MovieLens上构造的点击、付费和GMV代理值只用于机制实验，不能写成真实收入；长期价值必须有相应时间范围的证据。

## 先读这几篇

先用CDM理解相关性与去冗余，再读SORT-Gen理解前缀条件下的边际价值，最后用PRL-PUTS区分预测器和多目标策略选择；重点检查其本地代理与真实线上目标的差距。

1. [Contextual Distillation Model for Diversified Recommendation](../../../reproductions/2406.09021-cdm/README.md) · [原论文](https://arxiv.org/abs/2406.09021)
2. [A Generative Re-ranking Model for List-level Multi-objective Optimization at Taobao](../../../reproductions/2505.07197-sort-gen/README.md) · [原论文](https://arxiv.org/abs/2505.07197)
3. [A Production-Ready RL Framework for Personalized Utility Tuning with Pareto Sweeping in Pinterest Recommender Systems](../../../reproductions/2605.16344-prl-puts/README.md) · [原论文](https://arxiv.org/abs/2605.16344)

## 自测一下

每个物品的CTR预测完全相同，换排列顺序后整页点击还可能不同吗？

??? note "展开参考答案"

    可能。位置曝光、相邻内容重复和前缀对意图的影响都会改变列表收益。点式模型保持分数不变，并不意味着列表条件下的真实行为不变。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
