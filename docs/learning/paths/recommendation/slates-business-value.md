---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 重排、展示与长期价值

[搜广推](index.md) / 子主题导学 · 约 3 分钟 · 36 张论文卡

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
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="MAPS: A Multi-Agent Personalized Script-Driven Video Advertising System Enhanced by Reinforcement Learning 搜广推与 LLM 应用 Beihang University 2026-10-19 从固定广告库存检索创意，无法及时适应个体偏好和反馈。MAPS以Profile提取画像、Scripter生成分镜、Director调用视频生成、Reflector归因反馈，区分画像问题与脚本问题并路由最小修改。画像不仅含兴趣，也包含呈现风格与决策倾向。脚本先SFT学习结构，再用结构正确性、个性化偏好和商品事实一致性构造混合奖励，以GRPO式组内标准化更新。它的关键是大模型/视频生成与私有反馈环境的组合，不是独立奖励公式。 成本过高，不复现（审查 DONE），不把通用GRPO或三个分数加权冒充视频广告生成系统。仅研究资料。成本过高，不复现（审查 DONE），不把通用GRPO或三个分数加权冒充视频广告生成系统。Profile/Reflector是Qwen3-VL-32B，Scripter是8B；SFT20epoch、最大8192tokens，随后RL5000步，原文在8张H100上实验。导演依赖Kling-Omni，反馈闭环依赖生产系统。单卡A100/A30与Mac不承担此完整矩阵，成本过高，不复现（审查 DONE）。没有本地模型、评测指标或GPU回执，不进入自动重试与Evolve。  展示层生成与个性化 个性化创意生成 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-maps-creative-255b1b1c">MAPS: A Multi-Agent Personalized Script-Driven Video Advertising System Enhanced by Reinforcement Learning</h2>
<p class="ar-learning-card__meta">Beihang University · 论文公开：2026-10-19</p>
<p><strong>方法要点：</strong>从固定广告库存检索创意，无法及时适应个体偏好和反馈。MAPS以Profile提取画像、Scripter生成分镜、Director调用视频生成、Reflector归因反馈，区分画像问题与脚本问题并路由最小修改。画像不仅含兴趣，也包含呈现风格与决策倾向。脚本先SFT学习结构，再用结构正确性、个性化偏好和商品事实一致性构造混合奖励，以GRPO式组内标准化更新。它的关键是大模型/视频生成与私有反馈环境的组合，不是独立奖励公式。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE），不把通用GRPO或三个分数加权冒充视频广告生成系统。仅研究资料。成本过高，不复现（审查 DONE），不把通用GRPO或三个分数加权冒充视频广告生成系统。Profile/Reflector是Qwen3-VL-32B，Scripter是8B；SFT20epoch、最大8192tokens，随后RL5000步，原文在8张H100上实验。导演依赖Kling-Omni，反馈闭环依赖生产系统。单卡A100/A30与Mac不承担此完整矩阵，成本过高，不复现（审查 DONE）。没有本地模型、评测指标或GPU回执，不进入自动重试与Evolve。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.25748v1">原论文</a> · <a href="../../../../recommendation-components/2610.25748-maps-creative/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Challenges and Solutions for Bandits in the Wild: Warm-Started Mixture Bandits for Cross-Cohort Slate Recommendation 搜广推与 LLM 应用 DFKI / RPTU Kaiserslautern-Landau 2026-09-29 从历史 cohort 学习用户群和 item arm，用元数据给新用户构造固定强度的混合 Beta 先验；每轮用 Thompson sampling 选择未曝光 slate，并按用户反馈独立更新后验。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行固定强度 mixture prior、Thompson slate 与 posterior update；未复刻历史矩阵分解和 25 天部署。执行固定强度 mixture prior、Thompson slate 与 posterior update；未复刻历史矩阵分解和 25 天部署。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  cold-start slate-bandit cross-cohort-transfer 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-cohortmix-ts-f84d0507">Challenges and Solutions for Bandits in the Wild: Warm-Started Mixture Bandits for Cross-Cohort Slate Recommendation</h2>
<p class="ar-learning-card__meta">DFKI / RPTU Kaiserslautern-Landau · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>从历史 cohort 学习用户群和 item arm，用元数据给新用户构造固定强度的混合 Beta 先验；每轮用 Thompson sampling 选择未曝光 slate，并按用户反馈独立更新后验。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行固定强度 mixture prior、Thompson slate 与 posterior update；未复刻历史矩阵分解和 25 天部署。执行固定强度 mixture prior、Thompson slate 与 posterior update；未复刻历史矩阵分解和 25 天部署。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37800">原论文</a> · <a href="../../../../reproductions/2609.37800-cohortmix-ts/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Generate to Explore, Select to Exploit: Aligning LLM-based Headline Generation with Personalized Recommendation 搜广推与 LLM 应用 Baidu 2026-09-14 集合级多样性/忠实度探索后，再以当前上下文选择个性化标题；生产系统报告 CTR +2.57%、停留时长 +0.87%。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。私有日志、生产 checkpoint 与 serving 栈均未复刻。本地只验证公开数据上的核心状态转换；未复刻私有训练数据、大模型生成器、生产流量反馈或在线服务。当前不映射 evolve，避免 registry-only 标签。线上数字来自论文正文 A/B，不与本地 MovieLens 结果混写。本地 seeds 42/43/44 见 metrics/movielens-100k-seeds42-44.json。首个 seed 的统一 NDCG@10 基线为 0.05401，实验组为 0.04421，相对变化 -18.15%。  presentation-layer headline-generation gspo bandit-selection 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-gese-4a69cb3b">Generate to Explore, Select to Exploit: Aligning LLM-based Headline Generation with Personalized Recommendation</h2>
<p class="ar-learning-card__meta">Baidu · 论文公开：2026-09-14</p>
<p><strong>方法要点：</strong>集合级多样性/忠实度探索后，再以当前上下文选择个性化标题；生产系统报告 CTR +2.57%、停留时长 +0.87%。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：公开数据核心机制。复现级别：公开数据核心机制。私有日志、生产 checkpoint 与 serving 栈均未复刻。本地只验证公开数据上的核心状态转换；未复刻私有训练数据、大模型生成器、生产流量反馈或在线服务。当前不映射 evolve，避免 registry-only 标签。线上数字来自论文正文 A/B，不与本地 MovieLens 结果混写。本地 seeds 42/43/44 见 metrics/movielens-100k-seeds42-44.json。首个 seed 的统一 NDCG@10 基线为 0.05401，实验组为 0.04421，相对变化 -18.15%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.15094">原论文</a> · <a href="../../../../reproductions/2609.15094-gese/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Once Generated, Ranked: End-to-End Generative Slate Recommendation with Unified Semantic-Collaborative IDs 搜广推与 LLM 应用 Kuaishou Technology 2026-08-18 TUSID 融合语义码与协同码，GL2P 直接规划整张 slate，SPA 再用保守策略优化对齐列表级反馈。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation slate-ranking semantic-id reinforcement-learning 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-ogr-bedfe7b4">Once Generated, Ranked: End-to-End Generative Slate Recommendation with Unified Semantic-Collaborative IDs</h2>
<p class="ar-learning-card__meta">Kuaishou Technology · 论文公开：2026-08-18</p>
<p><strong>方法要点：</strong>TUSID 融合语义码与协同码，GL2P 直接规划整张 slate，SPA 再用保守策略优化对齐列表级反馈。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.17613">原论文</a> · <a href="../../../../reproductions/2608.17613-ogr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DrEM: Dual-Side Robust Ensemble Ranking from Noisy User Preference Predictions in Video Recommendation 搜广推与 LLM 应用 Shenzhen University 2026-08-13 把多路 pxtr 先变换到 logit 空间，对预测噪声做偏好保持筛选，并利用 pair-label 翻转风险反演修正训练目标；最后用一致性融合减小输入扰动导致的排序漂移。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为朴素三路加权融合，实验组加入偏好保持筛选与风险修正；seed 42 的 NDCG@10 为 0.07726，基线为 0.07518。  ranking multi-objective robust-learning video-recommendation 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-drem-6dedd99f">DrEM: Dual-Side Robust Ensemble Ranking from Noisy User Preference Predictions in Video Recommendation</h2>
<p class="ar-learning-card__meta">Shenzhen University · 论文公开：2026-08-13</p>
<p><strong>方法要点：</strong>把多路 pxtr 先变换到 logit 空间，对预测噪声做偏好保持筛选，并利用 pair-label 翻转风险反演修正训练目标；最后用一致性融合减小输入扰动导致的排序漂移。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为朴素三路加权融合，实验组加入偏好保持筛选与风险修正；seed 42 的 NDCG@10 为 0.07726，基线为 0.07518。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.12778">原论文</a> · <a href="../../../../reproductions/2608.12778-drem/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DREAM: A Dual-Loop Recommendation Evolution Framework Powered by Large Language Models 搜广推与 LLM 应用 Taobao &amp; Tmall Group / Alibaba 2026-08-10 工业推荐长期依赖人工配置和逐层独立优化，LLM 若直接生成自由文本又难以满足稳定性与安全要求。DREAM 是覆盖现有召回、精排和重排之上的控制平面：Intent Engine 将端上信号、session 行为和实时上下文整理成 L0 物理、L1 需求、L2 偏好三层意图；Meta Engine 依次执行 M1 意图摘要、M2 结合 Strategy Memory 的策略规划和 M3 确定性参数翻译；Unified Outlet 只接受白名单、范围内的 typed 参数。 Fidelity：核心机制复现。保留原推荐 backbone，实际执行分层意图、策略记忆、typed 参数编译、安全护栏及离线/影子在线双环；不以普通重排器代替核心控制链路。没有复刻淘宝私有多源信号、Qwen3 Meta Engine、真实流量和线上结论回存；本地“在线环”是 validation 内独立影子组，test 从未参与策略选择。本地对照口径：基线为同一 MovieLens-1M 切分和候选上的原 retrieval/ranking backbone；实验组只增加 DREAM 控制层，相对 NDCG@10 +39.36%，同时 head share +94.37%，不能只报正向相关性指标。  llm-recommendation ranking reranking intent-understanding online-policy serving 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-dream-c0565aca">DREAM: A Dual-Loop Recommendation Evolution Framework Powered by Large Language Models</h2>
<p class="ar-learning-card__meta">Taobao &amp; Tmall Group / Alibaba · 论文公开：2026-08-10</p>
<p><strong>方法要点：</strong>工业推荐长期依赖人工配置和逐层独立优化，LLM 若直接生成自由文本又难以满足稳定性与安全要求。DREAM 是覆盖现有召回、精排和重排之上的控制平面：Intent Engine 将端上信号、session 行为和实时上下文整理成 L0 物理、L1 需求、L2 偏好三层意图；Meta Engine 依次执行 M1 意图摘要、M2 结合 Strategy Memory 的策略规划和 M3 确定性参数翻译；Unified Outlet 只接受白名单、范围内的 typed 参数。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity：核心机制复现。保留原推荐 backbone，实际执行分层意图、策略记忆、typed 参数编译、安全护栏及离线/影子在线双环；不以普通重排器代替核心控制链路。没有复刻淘宝私有多源信号、Qwen3 Meta Engine、真实流量和线上结论回存；本地“在线环”是 validation 内独立影子组，test 从未参与策略选择。本地对照口径：基线为同一 MovieLens-1M 切分和候选上的原 retrieval/ranking backbone；实验组只增加 DREAM 控制层，相对 NDCG@10 +39.36%，同时 head share +94.37%，不能只报正向相关性指标。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.09408">原论文</a> · <a href="../../../../reproductions/2608.09408-dream/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="MetaStrategy: Generative Ranking with Executable LLM Strategies 搜广推与 LLM 应用 Alibaba / Taobao 2026-08-10 固定打分网络难以按用户当下意图动态改变目标。MetaStrategy 让 LLM 输出带类型的 JSON 排序策略，包括目标权重、内容/类目偏好、约束与位置规则；确定性 compiler 将策略执行在候选列表上，避免自由文本直接控制线上排序。生产训练还用 replay 环境、自竞争 curriculum、evaluator-routed reward-augmented OPD 将 4B teacher 蒸馏到 0.8B student。 Fidelity：核心机制复现。实际训练上下文条件策略生成器，并以确定性 compiler 执行 typed strategy；本地负结果如实保留。未复刻淘宝私有日志、生产 replay、4B→0.8B OPD 与 nearline serving；公开实验只验证“生成 typed bundle → 校验 → 确定性执行”的核心路径。本地对照口径：基线为同预算单目标排序器，实验组为 typed strategy generator + deterministic compiler；NDCG@10 相对变化 -8.51%。  ranking llm-recommendation executable-strategy online-policy 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-metastrategy-1088d4bd">MetaStrategy: Generative Ranking with Executable LLM Strategies</h2>
<p class="ar-learning-card__meta">Alibaba / Taobao · 论文公开：2026-08-10</p>
<p><strong>方法要点：</strong>固定打分网络难以按用户当下意图动态改变目标。MetaStrategy 让 LLM 输出带类型的 JSON 排序策略，包括目标权重、内容/类目偏好、约束与位置规则；确定性 compiler 将策略执行在候选列表上，避免自由文本直接控制线上排序。生产训练还用 replay 环境、自竞争 curriculum、evaluator-routed reward-augmented OPD 将 4B teacher 蒸馏到 0.8B student。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity：核心机制复现。实际训练上下文条件策略生成器，并以确定性 compiler 执行 typed strategy；本地负结果如实保留。未复刻淘宝私有日志、生产 replay、4B→0.8B OPD 与 nearline serving；公开实验只验证“生成 typed bundle → 校验 → 确定性执行”的核心路径。本地对照口径：基线为同预算单目标排序器，实验组为 typed strategy generator + deterministic compiler；NDCG@10 相对变化 -8.51%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.09440">原论文</a> · <a href="../../../../reproductions/2608.09440-metastrategy/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DEGR: Dual Exploration-Driven Generative Re-Ranking for Adaptive Cross-Request Context Bridging 搜广推与 LLM 应用 JD.com 2026-08-05 逐请求优化容易反复暴露相似商品。DEGR 在生成目标外加入同 cohort item embedding 的平方余弦约束，并用探索反馈形成 reward-adaptive ORPO，使偏好强度随真实探索收益变化；推理时再执行 diversity-aware greedy selection。 Fidelity：核心机制复现。实现 next-item CE、cohort 内多样性约束、adaptive reward-weighted ORPO 和多样性感知 greedy 重排。公开 MovieLens 没有跨请求曝光与探索 reward；本地以逆流行度代理奖励，未复刻京东十亿请求 reward model。本地对照口径：基线为同预算 CE generator，实验组加入 diversity 与 adaptive reward ORPO；相对基线 NDCG@10 +0.00%。  reranking slate-optimization exploration preference-optimization 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-degr-c402d30b">DEGR: Dual Exploration-Driven Generative Re-Ranking for Adaptive Cross-Request Context Bridging</h2>
<p class="ar-learning-card__meta">JD.com · 论文公开：2026-08-05</p>
<p><strong>方法要点：</strong>逐请求优化容易反复暴露相似商品。DEGR 在生成目标外加入同 cohort item embedding 的平方余弦约束，并用探索反馈形成 reward-adaptive ORPO，使偏好强度随真实探索收益变化；推理时再执行 diversity-aware greedy selection。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity：核心机制复现。实现 next-item CE、cohort 内多样性约束、adaptive reward-weighted ORPO 和多样性感知 greedy 重排。公开 MovieLens 没有跨请求曝光与探索 reward；本地以逆流行度代理奖励，未复刻京东十亿请求 reward model。本地对照口径：基线为同预算 CE generator，实验组加入 diversity 与 adaptive reward ORPO；相对基线 NDCG@10 +0.00%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04809">原论文</a> · <a href="../../../../reproductions/2608.04809-degr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="A Self-Triggered Agentic Push Recommendation System 搜广推与 LLM 应用 ByteDance / Douyin 2026-08-03 固定频控无法实时调整，周期轮询又在成本与时机间冲突。STEPS 把“是否推送”和“何时再次唤醒”合成闭环：planning agent 用 gated ordinal regression 规划间隔，execution agent 用轨迹回报决定发送，轻量 filter agent 控制算力并拦截异常计划。 Fidelity：核心机制复现。公开数据只验证论文机制，不模拟生产流量。MovieLens 没有真实 push permission、触达成本和 wall-clock 唤醒器，只验证决策分解。本地对照口径：基线为共享 transition + content scorer，实验组只加入 STEPS 核心机制；相对 NDCG@10 +66.05%。  push-recommendation agentic-recommendation decision-transformer serving 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-steps-e0be3966">A Self-Triggered Agentic Push Recommendation System</h2>
<p class="ar-learning-card__meta">ByteDance / Douyin · 论文公开：2026-08-03</p>
<p><strong>方法要点：</strong>固定频控无法实时调整，周期轮询又在成本与时机间冲突。STEPS 把“是否推送”和“何时再次唤醒”合成闭环：planning agent 用 gated ordinal regression 规划间隔，execution agent 用轨迹回报决定发送，轻量 filter agent 控制算力并拦截异常计划。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity：核心机制复现。公开数据只验证论文机制，不模拟生产流量。MovieLens 没有真实 push permission、触达成本和 wall-clock 唤醒器，只验证决策分解。本地对照口径：基线为共享 transition + content scorer，实验组只加入 STEPS 核心机制；相对 NDCG@10 +66.05%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01949">原论文</a> · <a href="../../../../reproductions/2608.01949-steps/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DIRECTOR: Dynamic Index-based Recommendation with Transport-Optimized Retrieval 搜广推与 LLM 应用 University of Science and Technology of China 2026-07-29 每个展示位置生成动态索引分布，以 Sinkhorn 最优运输联合约束所有位置；最终用全局匹配而非独立 argmax 解码，减少冲突并一次并行产生整张 slate。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为各位置独立动态索引，实验组加入 Sinkhorn transport 与硬全局匹配；seed 42 的 NDCG@10 为 0.05334，基线为 0.03857。  reranking dynamic-index optimal-transport non-autoregressive 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-director-8aa08907">DIRECTOR: Dynamic Index-based Recommendation with Transport-Optimized Retrieval</h2>
<p class="ar-learning-card__meta">University of Science and Technology of China · 论文公开：2026-07-29</p>
<p><strong>方法要点：</strong>每个展示位置生成动态索引分布，以 Sinkhorn 最优运输联合约束所有位置；最终用全局匹配而非独立 argmax 解码，减少冲突并一次并行产生整张 slate。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为各位置独立动态索引，实验组加入 Sinkhorn transport 与硬全局匹配；seed 42 的 NDCG@10 为 0.05334，基线为 0.03857。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26418">原论文</a> · <a href="../../../../reproductions/2607.26418-director/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="PSG: Pair-Space Generation for Efficient Generative Reranking 搜广推与 LLM 应用 Kuaishou Technology 2026-07-29 把相邻两个 item 编成一个请求内 pair token，在 pair 空间生成半长度序列，再无损展开为 item slate；pair scorer 显式保留顺序，重复约束保证展开结果可用。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为六步 item-space 生成，实验组为三步 pair-space 生成与展开；seed 42 的 NDCG@10 为 0.04826，基线为 0.05401，负结果保留。  reranking generative-recommendation pair-token serving 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-psg-c3e023ce">PSG: Pair-Space Generation for Efficient Generative Reranking</h2>
<p class="ar-learning-card__meta">Kuaishou Technology · 论文公开：2026-07-29</p>
<p><strong>方法要点：</strong>把相邻两个 item 编成一个请求内 pair token，在 pair 空间生成半长度序列，再无损展开为 item slate；pair scorer 显式保留顺序，重复约束保证展开结果可用。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为六步 item-space 生成，实验组为三步 pair-space 生成与展开；seed 42 的 NDCG@10 为 0.04826，基线为 0.05401，负结果保留。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26427">原论文</a> · <a href="../../../../reproductions/2607.26427-psg/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Beyond Single-Episode Optimization: Sliding-Window Aware Generative Auto-Bidding for Long-Term Advertising Effectiveness 搜广推与 LLM 应用 Alibaba International Digital Commerce / Dalian University of Technology 2026-07-28 用 masked future plan 建模跨 episode 的七日滑窗目标，并以 per-step gate 将长期 guidance 注入当前 bid 决策。 Fidelity: 核心机制复现。本地执行论文的窗口感知出价目标与约束代理，不把公开离线实验写成生产广告系统。不是生产 Decision Transformer checkpoint，且公开数据没有 bid、budget、GMV，结果仅是结构消融。本地对照口径：基线为 single-episode Decision Transformer proxy，实验组为 sliding-window planner；同一小数据候选排序下 Hit@10 与 NDCG@10 均为 +0.00%。  advertising generative-model decision-transformer long-horizon 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-swag-bid-1ae52cbb">Beyond Single-Episode Optimization: Sliding-Window Aware Generative Auto-Bidding for Long-Term Advertising Effectiveness</h2>
<p class="ar-learning-card__meta">Alibaba International Digital Commerce / Dalian University of Technology · 论文公开：2026-07-28</p>
<p><strong>方法要点：</strong>用 masked future plan 建模跨 episode 的七日滑窗目标，并以 per-step gate 将长期 guidance 注入当前 bid 决策。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地执行论文的窗口感知出价目标与约束代理，不把公开离线实验写成生产广告系统。不是生产 Decision Transformer checkpoint，且公开数据没有 bid、budget、GMV，结果仅是结构消融。本地对照口径：基线为 single-episode Decision Transformer proxy，实验组为 sliding-window planner；同一小数据候选排序下 Hit@10 与 NDCG@10 均为 +0.00%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25233">原论文</a> · <a href="../../../../reproductions/2607.25233-swag-bid/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Breaking the Loop: An Empirical Comparison of Strategies for Novelty and Freshness in YouTube Music 搜广推与 LLM 应用 YouTube Music / Google 2026-07-26 系统比较 recency feature、IPS、可移除 bias tower 与 SNGP 不确定性探索，区分训练去偏和 serving 探索。 Fidelity: 核心机制复现。本地执行新鲜度感知的候选打分与公平对照；不复刻 YouTube 私有流量系统。没有 YouTube 连续训练基础设施和 SNGP 大模型；本地负结果不推翻论文各干预的在线结论。本地对照口径：基线为 popularity-biased continuous ranker，实验组为四机制组合；Hit@10 +0.00%、NDCG@10 -6.35%，head share -28.72%。  ranking feedback-loop freshness exploration 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-youtube-freshness-c4f4face">Breaking the Loop: An Empirical Comparison of Strategies for Novelty and Freshness in YouTube Music</h2>
<p class="ar-learning-card__meta">YouTube Music / Google · 论文公开：2026-07-26</p>
<p><strong>方法要点：</strong>系统比较 recency feature、IPS、可移除 bias tower 与 SNGP 不确定性探索，区分训练去偏和 serving 探索。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地执行新鲜度感知的候选打分与公平对照；不复刻 YouTube 私有流量系统。没有 YouTube 连续训练基础设施和 SNGP 大模型；本地负结果不推翻论文各干预的在线结论。本地对照口径：基线为 popularity-biased continuous ranker，实验组为四机制组合；Hit@10 +0.00%、NDCG@10 -6.35%，head share -28.72%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.23749">原论文</a> · <a href="../../../../reproductions/2607.23749-youtube-freshness/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="PinDCO: Whole-Page Aware Dynamic Creative Optimization at Scale 搜广推与 LLM 应用 Pinterest 2026-07-21 生成式创意使每个广告的候选图像、标题与版式迅速增多。PinDCO 用组件专属 tower 分别编码异构创意，再预测相对基础广告排序 logit 的增量；PAM 根据相对长宽比惩罚过度占用瀑布流像素的创意，前置轻量筛选、缓存和动态 batching 控制线上成本，ε-greedy 流量为新创意收集较少偏的反馈。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行组件专塔、基于广告分数的增量融合、像素惩罚公式与候选筛选；不把 MovieLens 内容特征冒充 Pinterest 创意或生产流量。未复刻 Pinterest 私有创意、用户/上下文特征、广告基线、在线 bandit 流量、缓存与服务集群。本实现不声明 CUDA 路径，也未接入 evolve，因为当前统一 evaluator 尚不能执行完整创意候选协议。MovieLens 100K、seeds 42/43/44 的固定公开口径见 metrics/movielens-100k-seeds42-44.json。  advertising creative-optimization whole-page-optimization multi-tower 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-pindco-94511583">PinDCO: Whole-Page Aware Dynamic Creative Optimization at Scale</h2>
<p class="ar-learning-card__meta">Pinterest · 论文公开：2026-07-21</p>
<p><strong>方法要点：</strong>生成式创意使每个广告的候选图像、标题与版式迅速增多。PinDCO 用组件专属 tower 分别编码异构创意，再预测相对基础广告排序 logit 的增量；PAM 根据相对长宽比惩罚过度占用瀑布流像素的创意，前置轻量筛选、缓存和动态 batching 控制线上成本，ε-greedy 流量为新创意收集较少偏的反馈。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行组件专塔、基于广告分数的增量融合、像素惩罚公式与候选筛选；不把 MovieLens 内容特征冒充 Pinterest 创意或生产流量。未复刻 Pinterest 私有创意、用户/上下文特征、广告基线、在线 bandit 流量、缓存与服务集群。本实现不声明 CUDA 路径，也未接入 evolve，因为当前统一 evaluator 尚不能执行完整创意候选协议。MovieLens 100K、seeds 42/43/44 的固定公开口径见 metrics/movielens-100k-seeds42-44.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11943">原论文</a> · <a href="../../../../reproductions/2609.11943-pindco/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Uncertainty as Remedy: Mitigating Satisfaction Label Bias in Short Video Multi-Objective Ensemble Ranking 搜广推与 LLM 应用 Kuaishou Technology 2026-07-19 点击、观看、点赞等 pxtr 只是不可观测“真实满意度”的冲突代理。UAME 在 EMER/EASQ 主干上增加共享表征的均值与方差双头，把分数视作 Gaussian 变量；用解析 pair probability 联合各 pxtr，令冲突更高的 pair 获得更大训练权重。线上只使用均值打分，因此不增加 serving 路径。 Fidelity: 核心机制复现。训练 Gaussian score 双头、概率 pairwise loss、冲突约束与不确定性加权；私有八路 pxtr 和生产 backbone 用公开 proxy 替代。未获得快手八路 pxtr、EMER/EASQ、问卷满意度和亿级流量；本地负结果说明这一公开 proxy 映射不能直接复现论文收益，不与线上 lift 混写。本地对照口径：基线是同 backbone 的 deterministic multi-objective pairwise ranker；实验组加入完整 UAME loss，NDCG@10 相对 -62.28%。  multi-objective-ranking uncertainty loss-design 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-uame-b8cd46d0">Uncertainty as Remedy: Mitigating Satisfaction Label Bias in Short Video Multi-Objective Ensemble Ranking</h2>
<p class="ar-learning-card__meta">Kuaishou Technology · 论文公开：2026-07-19</p>
<p><strong>方法要点：</strong>点击、观看、点赞等 pxtr 只是不可观测“真实满意度”的冲突代理。UAME 在 EMER/EASQ 主干上增加共享表征的均值与方差双头，把分数视作 Gaussian 变量；用解析 pair probability 联合各 pxtr，令冲突更高的 pair 获得更大训练权重。线上只使用均值打分，因此不增加 serving 路径。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。训练 Gaussian score 双头、概率 pairwise loss、冲突约束与不确定性加权；私有八路 pxtr 和生产 backbone 用公开 proxy 替代。未获得快手八路 pxtr、EMER/EASQ、问卷满意度和亿级流量；本地负结果说明这一公开 proxy 映射不能直接复现论文收益，不与线上 lift 混写。本地对照口径：基线是同 backbone 的 deterministic multi-objective pairwise ranker；实验组加入完整 UAME loss，NDCG@10 相对 -62.28%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.17092">原论文</a> · <a href="../../../../reproductions/2607.17092-uame/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="LLM-Based Re-Ranking for Real Estate Search 搜广推与 LLM 应用 QuintoAndar 2026-07-16 把对话需求、结构化房源属性、文本描述和候选集合统计交给 LLM 重排，用候选间比较补足向量召回的局部相关性。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  search-ranking llm-reranking content-understanding 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-real-estate-rerank-2009ea9f">LLM-Based Re-Ranking for Real Estate Search</h2>
<p class="ar-learning-card__meta">QuintoAndar · 论文公开：2026-07-16</p>
<p><strong>方法要点：</strong>把对话需求、结构化房源属性、文本描述和候选集合统计交给 LLM 重排，用候选间比较补足向量召回的局部相关性。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14835">原论文</a> · <a href="../../../../reproductions/2607.14835-real-estate-rerank/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Adaptive Ad Load Design for Sponsored Search Markets: Evidence, Theory, and Deployment 搜广推与 LLM 应用 University of Washington 2026-07-15 在收入与转化约束下动态决定每次搜索展示多少广告，利用随机现场实验估计供给曲线，再由轻量策略选择 ad load。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  advertising constrained-optimization marketplace 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-adaptive-ad-load-26eb54c1">Adaptive Ad Load Design for Sponsored Search Markets: Evidence, Theory, and Deployment</h2>
<p class="ar-learning-card__meta">University of Washington · 论文公开：2026-07-15</p>
<p><strong>方法要点：</strong>在收入与转化约束下动态决定每次搜索展示多少广告，利用随机现场实验估计供给曲线，再由轻量策略选择 ad load。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14418">原论文</a> · <a href="../../../../reproductions/2607.14418-adaptive-ad-load/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Long-term User Engagement Optimization through Model-agnostic Downstream Rewards Learning 搜广推与 LLM 应用 Pinterest 2026-07-15 只优化当前点击或保存可能牺牲用户后续活跃。Pinterest 的方法先离线提出并筛选能预测未来参与度的 downstream rewards，再把通过筛选的 reward head 作为模型无关附加目标接入 Homefeed、Search、Related Pins 和 Notifications 等不同系统，无需替换原有主排序器。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实执行 reward 筛选与附加头；Pinterest 私有跨 surface 长期标签未复刻。本地从 deeper transition、content depth、new use-case exploration 和 shallow closeup 四类 session 信号出发，以未来类型覆盖代理长期参与度做离线筛选，训练独立 reward head，再在 validation 上选择与即时排序分数的融合强度。  long-term-value reward-design multi-surface retention 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-downstream-rewards-21cba3a1">Long-term User Engagement Optimization through Model-agnostic Downstream Rewards Learning</h2>
<p class="ar-learning-card__meta">Pinterest · 论文公开：2026-07-15</p>
<p><strong>方法要点：</strong>只优化当前点击或保存可能牺牲用户后续活跃。Pinterest 的方法先离线提出并筛选能预测未来参与度的 downstream rewards，再把通过筛选的 reward head 作为模型无关附加目标接入 Homefeed、Search、Related Pins 和 Notifications 等不同系统，无需替换原有主排序器。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现保真度：核心机制复现。复现保真度：核心机制复现。真实执行 reward 筛选与附加头；Pinterest 私有跨 surface 长期标签未复刻。本地从 deeper transition、content depth、new use-case exploration 和 shallow closeup 四类 session 信号出发，以未来类型覆盖代理长期参与度做离线筛选，训练独立 reward head，再在 validation 上选择与即时排序分数的融合强度。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14192">原论文</a> · <a href="../../../../reproductions/2607.14192-downstream-rewards/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="GenPage: Towards End-to-End Generative Homepage Construction at Netflix 搜广推与 LLM 应用 Netflix 2026-06-30 用一个生成模型直接输出整页而非逐阶段召回排序，并在 WBC/SFT 后以生产长期奖励进行 RL 后训练，同时处理业务规则和冷启动。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation page-generation reinforcement-learning 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-genpage-e2b0c563">GenPage: Towards End-to-End Generative Homepage Construction at Netflix</h2>
<p class="ar-learning-card__meta">Netflix · 论文公开：2026-06-30</p>
<p><strong>方法要点：</strong>用一个生成模型直接输出整页而非逐阶段召回排序，并在 WBC/SFT 后以生产长期奖励进行 RL 后训练，同时处理业务规则和冷启动。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.31031">原论文</a> · <a href="../../../../reproductions/2606.31031-genpage/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="PIANO: Personalized Reranking via Information Aggregation Node for Music Search Optimization 搜广推与 LLM 应用 NetEase Cloud Music 2026-06-15 Query-Driven Interest Refiner 从历史中提取查询相关兴趣，Information Aggregation Node 汇总整张候选列表并反向条件化 item 级 CTR/CVR。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 PIANO 为 0.04988，相对变化 -7.65%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  search reranking listwise 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-piano-1fe78019">PIANO: Personalized Reranking via Information Aggregation Node for Music Search Optimization</h2>
<p class="ar-learning-card__meta">NetEase Cloud Music · 论文公开：2026-06-15</p>
<p><strong>方法要点：</strong>Query-Driven Interest Refiner 从历史中提取查询相关兴趣，Information Aggregation Node 汇总整张候选列表并反向条件化 item 级 CTR/CVR。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 PIANO 为 0.04988，相对变化 -7.65%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.16641">原论文</a> · <a href="../../../../reproductions/2606.16641-piano/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Taiji: Pareto Optimal Policy Optimization with Semantics-IDs Trade-off for Industrial LLM-Enhanced Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-06-02 先用反向工程偏好推理与拒绝采样激活推荐 CoT，再由 POPO 动态平衡 LLM 语义奖励和推荐协同 ID 奖励，避免固定权重遗漏非凸 Pareto 前沿。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.06448，相对变化 +19.39%。本地代理目标与论文生产任务不同，不能外推线上 lift。  advertising reinforcement-alignment pareto-optimization 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-taiji-2fa562ab">Taiji: Pareto Optimal Policy Optimization with Semantics-IDs Trade-off for Industrial LLM-Enhanced Recommendation</h2>
<p class="ar-learning-card__meta">Kuaishou Technology · 论文公开：2026-06-02</p>
<p><strong>方法要点：</strong>先用反向工程偏好推理与拒绝采样激活推荐 CoT，再由 POPO 动态平衡 LLM 语义奖励和推荐协同 ID 奖励，避免固定权重遗漏非凸 Pareto 前沿。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.06448，相对变化 +19.39%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.03866">原论文</a> · <a href="../../../../reproductions/2606.03866-taiji/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Stochastic Primal-Dual Decoding for Multiobjective Generative Recommender Systems 搜广推与 LLM 应用 Spotify 2026-05-26 不重训生成式推荐模型，在逐位置解码时把相关性 logits 与辅助目标贡献相加，并根据剩余约束松弛量以镜像下降动态更新拉格朗日乘子。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.02109，相对变化 -60.95%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation multiobjective constrained-decoding 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-primal-dual-decoding-161adf1d">Stochastic Primal-Dual Decoding for Multiobjective Generative Recommender Systems</h2>
<p class="ar-learning-card__meta">Spotify · 论文公开：2026-05-26</p>
<p><strong>方法要点：</strong>不重训生成式推荐模型，在逐位置解码时把相关性 logits 与辅助目标贡献相加，并根据剩余约束松弛量以镜像下降动态更新拉格朗日乘子。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.02109，相对变化 -60.95%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.19357">原论文</a> · <a href="../../../../reproductions/2607.19357-primal-dual-decoding/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DeGRe: Listwise Generative Reranking with Offline Lookahead Distillation 搜广推与 LLM 应用 Alibaba Group / Zhejiang University 2026-05-25 逐点生成器只学习日志中的单一路径，难以直接优化整张列表的长期价值。DeGRe 离线训练累计回报 evaluator，用 beam search 探索高价值列表，再把每个前缀下所有剩余候选的前瞻价值蒸馏为 dense soft label；线上只保留一次 greedy generator。 Fidelity: 核心机制复现。累计价值评估器、lookahead beam mining、逐前缀 dense label、beam weighting 与单次在线生成路径均实际执行。未复刻私有交易标签与工业 Transformer 规模；本地结果仅验证离线 evaluator→beam mining→dense distillation 链路。本地对照口径：基线是相同候选与特征的 pointwise generator；实验组 DeGRe 加入离线前瞻蒸馏，相对基线 Hit@10 +0.00%、NDCG@10 +3.31%。  generative-recommendation reranking distillation 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-degre-898bafc1">DeGRe: Listwise Generative Reranking with Offline Lookahead Distillation</h2>
<p class="ar-learning-card__meta">Alibaba Group / Zhejiang University · 论文公开：2026-05-25</p>
<p><strong>方法要点：</strong>逐点生成器只学习日志中的单一路径，难以直接优化整张列表的长期价值。DeGRe 离线训练累计回报 evaluator，用 beam search 探索高价值列表，再把每个前缀下所有剩余候选的前瞻价值蒸馏为 dense soft label；线上只保留一次 greedy generator。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。累计价值评估器、lookahead beam mining、逐前缀 dense label、beam weighting 与单次在线生成路径均实际执行。未复刻私有交易标签与工业 Transformer 规模；本地结果仅验证离线 evaluator→beam mining→dense distillation 链路。本地对照口径：基线是相同候选与特征的 pointwise generator；实验组 DeGRe 加入离线前瞻蒸馏，相对基线 Hit@10 +0.00%、NDCG@10 +3.31%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.25749">原论文</a> · <a href="../../../../reproductions/2605.25749-degre/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="A Production-Ready RL Framework for Personalized Utility Tuning with Pareto Sweeping in Pinterest Recommender Systems 搜广推与 LLM 应用 Pinterest 2026-05-08 双头 Q 网络分别估计 Repin 与 P2P utility，再通过 Pareto sweeping 离线筛选不劣策略；线上仅切换可治理的权重策略，不更换模型。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 prl-puts 核心机制，相对 NDCG@10 +39.64%。  reinforcement-learning multi-objective-ranking homefeed 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-prl-puts-9d4fc321">A Production-Ready RL Framework for Personalized Utility Tuning with Pareto Sweeping in Pinterest Recommender Systems</h2>
<p class="ar-learning-card__meta">Pinterest · 论文公开：2026-05-08</p>
<p><strong>方法要点：</strong>双头 Q 网络分别估计 Repin 与 P2P utility，再通过 Pareto sweeping 离线筛选不劣策略；线上仅切换可治理的权重策略，不更换模型。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 prl-puts 核心机制，相对 NDCG@10 +39.64%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.16344">原论文</a> · <a href="../../../../reproductions/2605.16344-prl-puts/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="From Local Indices to Global Identifiers: Generative Reranking via Global Action Space 搜广推与 LLM 应用 City University of Hong Kong / Kuaishou / UC San Diego 2026-04-28 全局 Semantic ID 空间把局部候选重排改写为全库生成；先做 listwise SFT，再用组相对奖励优化列表效用与长尾覆盖。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 glorank 核心机制；相对 NDCG@10 -44.26%。  reranking generative-recommendation semantic-id reinforcement-learning 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-glorank-9a7d512b">From Local Indices to Global Identifiers: Generative Reranking via Global Action Space</h2>
<p class="ar-learning-card__meta">City University of Hong Kong / Kuaishou / UC San Diego · 论文公开：2026-04-28</p>
<p><strong>方法要点：</strong>全局 Semantic ID 空间把局部候选重排改写为全库生成；先做 listwise SFT，再用组相对奖励优化列表效用与长尾覆盖。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 glorank 核心机制；相对 NDCG@10 -44.26%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.25291">原论文</a> · <a href="../../../../reproductions/2604.25291-glorank/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Dual-Rerank: Fusing Sequential Dependencies and Utility for Generative Reranking 搜广推与 LLM 应用 Kuaishou Technology 2026-04-08 AR 教师学习物品间顺序依赖，NAR 学生并行估计名次；效用蒸馏把效果与延迟共同写入训练目标。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 dual-rerank 核心机制；相对 NDCG@10 +10.66%。  reranking knowledge-distillation listwise-rl serving 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-dual-rerank-e775c831">Dual-Rerank: Fusing Sequential Dependencies and Utility for Generative Reranking</h2>
<p class="ar-learning-card__meta">Kuaishou Technology · 论文公开：2026-04-08</p>
<p><strong>方法要点：</strong>AR 教师学习物品间顺序依赖，NAR 学生并行估计名次；效用蒸馏把效果与延迟共同写入训练目标。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 dual-rerank 核心机制；相对 NDCG@10 +10.66%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.07420">原论文</a> · <a href="../../../../reproductions/2604.07420-dual-rerank/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="SaFRO: Satisfaction-Aware Fusion via Dual-Relative Policy Optimization for Short-Video Search 搜广推与 LLM 应用 Kuaishou Technology 2026-03-20 满意度 reward 同时建模即时互动与长期留存，Dual-Relative PO 在组内和任务间归一化优势，关系门控融合多搜索目标。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 safro 核心机制，相对 NDCG@10 +81.86%。  search-ranking reinforcement-learning multi-task-learning 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-safro-95b49eda">SaFRO: Satisfaction-Aware Fusion via Dual-Relative Policy Optimization for Short-Video Search</h2>
<p class="ar-learning-card__meta">Kuaishou Technology · 论文公开：2026-03-20</p>
<p><strong>方法要点：</strong>满意度 reward 同时建模即时互动与长期留存，Dual-Relative PO 在组内和任务间归一化优势，关系门控融合多搜索目标。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 safro 核心机制，相对 NDCG@10 +81.86%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.19585">原论文</a> · <a href="../../../../reproductions/2603.19585-safro/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Constraint-Aware Generative Re-ranking for Multi-Objective Optimization in Advertising Feeds 搜广推与 LLM 应用 Bilibili 2026-03-04 CGR 用一个网络同时完成序列生成和奖励估计，将广告位、广告负载等业务规则直接写入自回归解码；约束感知奖励剪枝提前排除不可行分支，避免生成后的启发式修补。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05715，相对变化 +5.82%。本地代理目标与论文生产任务不同，不能外推线上 lift。  advertising generative-reranking constraint-optimization 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-cgr-09571847">Constraint-Aware Generative Re-ranking for Multi-Objective Optimization in Advertising Feeds</h2>
<p class="ar-learning-card__meta">Bilibili · 论文公开：2026-03-04</p>
<p><strong>方法要点：</strong>CGR 用一个网络同时完成序列生成和奖励估计，将广告位、广告负载等业务规则直接写入自回归解码；约束感知奖励剪枝提前排除不可行分支，避免生成后的启发式修补。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05715，相对变化 +5.82%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.04227">原论文</a> · <a href="../../../../reproductions/2603.04227-cgr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="A Long-term Value Prediction Framework In Video Ranking 搜广推与 LLM 应用 Alibaba Group / Tsinghua University 2026-02-19 PDQ 消除位置偏差，归因模块分配会话内长期价值，作者周期任务再引入跨日优质创作者价值。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 ltv-video-ranking 核心机制，相对 NDCG@10 +9.73%。  ranking long-term-value debiasing 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-ltv-video-ranking-a90843c2">A Long-term Value Prediction Framework In Video Ranking</h2>
<p class="ar-learning-card__meta">Alibaba Group / Tsinghua University · 论文公开：2026-02-19</p>
<p><strong>方法要点：</strong>PDQ 消除位置偏差，归因模块分配会话内长期价值，作者周期任务再引入跨日优质创作者价值。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 ltv-video-ranking 核心机制，相对 NDCG@10 +9.73%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.17058">原论文</a> · <a href="../../../../reproductions/2602.17058-ltv-video-ranking/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Online Advertising with Spatial Interactions 搜广推与 LLM 应用 Google Research 2026-02-12 传统逐位置竞价忽略屏幕上的空间干扰。论文将最近邻外部性问题约化到分组伪圆盘选择，再将LP解舍入为可行圆盘集合；同时研究可分解价值的简单拍卖、二维PTAS与乘积距离模型的困难性。实现范围为v1 §2.2 Algorithm1及Eq2。 论文没有完整训练实验，故full_experiment_status=not_applicable_theoretical_paper，不伪造“高成本不复现”理由。属于L1机制诊断，不是线上广告收益。自建3点度量、3个圆盘的数学测试；检查LP可行、所有采样满足约束II，并以独立种子检验边际保留概率接近。属于L1机制诊断，不是线上广告收益。CPU无需GPU；稳定记录见metrics/component-cpu-seed42.json。  空间外部性与广告分配 LP随机舍入 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-spatial-ads-1dbea82c">Online Advertising with Spatial Interactions</h2>
<p class="ar-learning-card__meta">Google Research · 论文公开：2026-02-12</p>
<p><strong>方法要点：</strong>传统逐位置竞价忽略屏幕上的空间干扰。论文将最近邻外部性问题约化到分组伪圆盘选择，再将LP解舍入为可行圆盘集合；同时研究可分解价值的简单拍卖、二维PTAS与乘积距离模型的困难性。实现范围为v1 §2.2 Algorithm1及Eq2。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>论文没有完整训练实验，故full_experiment_status=not_applicable_theoretical_paper，不伪造“高成本不复现”理由。属于L1机制诊断，不是线上广告收益。自建3点度量、3个圆盘的数学测试；检查LP可行、所有采样满足约束II，并以独立种子检验边际保留概率接近。属于L1机制诊断，不是线上广告收益。CPU无需GPU；稳定记录见metrics/component-cpu-seed42.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12481">原论文</a> · <a href="../../../../recommendation-components/2602.12481-spatial-ads/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Hierarchical Contextual Uplift Bandits for Catalog Personalization 搜广推与 LLM 应用 Dream11 2026-01-20 在用户与系统上下文树上动态选择粒度，并让父节点奖励向稀疏子节点继承以改善冷启动；策略直接估计动作的增量收益，而不是只拟合观察到的绝对点击。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04886，相对变化 -9.53%。本地代理目标与论文生产任务不同，不能外推线上 lift。  bandit uplift-modeling catalog-personalization 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-hcub-b171df10">Hierarchical Contextual Uplift Bandits for Catalog Personalization</h2>
<p class="ar-learning-card__meta">Dream11 · 论文公开：2026-01-20</p>
<p><strong>方法要点：</strong>在用户与系统上下文树上动态选择粒度，并让父节点奖励向稀疏子节点继承以改善冷启动；策略直接估计动作的增量收益，而不是只拟合观察到的绝对点击。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04886，相对变化 -9.53%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.14333">原论文</a> · <a href="../../../../reproductions/2601.14333-hcub/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Rethinking Multi-objective Ranking Ensemble in Recommender System: From Score Fusion to Rank Consistency 搜广推与 LLM 应用 Kuaishou Technology 2026-01-06 第一阶段将 AUC 改写为可微 rank-sum 目标，使各任务从分类分数转向排序对齐；第二阶段用目标间 self-attention 学习购买、评论等目标的依赖，再输出统一序。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05203，相对变化 -3.65%。本地代理目标与论文生产任务不同，不能外推线上 lift。  multi-objective-ranking rank-consistency ensemble 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-harmonrank-1abfcd00">Rethinking Multi-objective Ranking Ensemble in Recommender System: From Score Fusion to Rank Consistency</h2>
<p class="ar-learning-card__meta">Kuaishou Technology · 论文公开：2026-01-06</p>
<p><strong>方法要点：</strong>第一阶段将 AUC 改写为可微 rank-sum 目标，使各任务从分类分数转向排序对齐；第二阶段用目标间 self-attention 学习购买、评论等目标的依赖，再输出统一序。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05203，相对变化 -3.65%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.02955">原论文</a> · <a href="../../../../reproductions/2601.02955-harmonrank/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="HiGR: Industrial-Scale Hierarchical Generative Slate Recommendation Framework in Tencent 搜广推与 LLM 应用 Tencent 2025-12-31 逐物品生成忽略 slate 内相互作用。HiGR 用 PCRQ-VAE 得到层级语义 ID，Hierarchical Slate Decoder 先选簇再选物品，并通过 ORPO 对齐整页偏好。 多样性更好但精度下降，未复现线上收益。Fidelity: 核心机制复现。实际学习两级 residual semantic ID，执行 coarse-to-fine slate 解码和 ORPO 风格偏好重排。MovieLens 单物品 next-item 目标并非视频 slate 反馈；本地 k-means residual ID 不等价于生产 PCRQ-VAE。本地对照口径：相对 flat item slate 基线，实验组 NDCG@10 -12.32%。  generative-recommendation slate-recommendation semantic-id preference-optimization 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-higr-d87ebf0f">HiGR: Industrial-Scale Hierarchical Generative Slate Recommendation Framework in Tencent</h2>
<p class="ar-learning-card__meta">Tencent · 论文公开：2025-12-31</p>
<p><strong>方法要点：</strong>逐物品生成忽略 slate 内相互作用。HiGR 用 PCRQ-VAE 得到层级语义 ID，Hierarchical Slate Decoder 先选簇再选物品，并通过 ORPO 对齐整页偏好。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>多样性更好但精度下降，未复现线上收益。Fidelity: 核心机制复现。实际学习两级 residual semantic ID，执行 coarse-to-fine slate 解码和 ORPO 风格偏好重排。MovieLens 单物品 next-item 目标并非视频 slate 反馈；本地 k-means residual ID 不等价于生产 PCRQ-VAE。本地对照口径：相对 flat item slate 基线，实验组 NDCG@10 -12.32%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2512.24787">原论文</a> · <a href="../../../../reproductions/2512.24787-higr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Deep Reinforcement Learning for Ranking Utility Tuning in the Ad Recommender System at Pinterest 搜广推与 LLM 应用 Pinterest 2025-09-05 广告排序的相关性、CTR、CVR 和收益权重通常靠人工调节。DRL-PUT 把权重组合视为动作，依据用户/请求状态选择动作，并从 logged behavior 和组合 reward 学习策略。 Fidelity: 核心机制复现。从公开交互构造带 propensity 的日志策略，并用 REINFORCE 学习效用权重动作。公开评分代理点击和收益，无法重建 Pinterest 拍卖、真实 counterfactual reward 与广告主约束。本地对照口径：相对固定 utility 权重基线，实验组 NDCG@10 +19.13%。  ads-ranking reinforcement-learning utility-tuning off-policy 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-drl-put-ba6d0f54">Deep Reinforcement Learning for Ranking Utility Tuning in the Ad Recommender System at Pinterest</h2>
<p class="ar-learning-card__meta">Pinterest · 论文公开：2025-09-05</p>
<p><strong>方法要点：</strong>广告排序的相关性、CTR、CVR 和收益权重通常靠人工调节。DRL-PUT 把权重组合视为动作，依据用户/请求状态选择动作，并从 logged behavior 和组合 reward 学习策略。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。从公开交互构造带 propensity 的日志策略，并用 REINFORCE 学习效用权重动作。公开评分代理点击和收益，无法重建 Pinterest 拍卖、真实 counterfactual reward 与广告主约束。本地对照口径：相对固定 utility 权重基线，实验组 NDCG@10 +19.13%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2509.05292">原论文</a> · <a href="../../../../reproductions/2509.05292-drl-put/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="A Generative Re-ranking Model for List-level Multi-objective Optimization at Taobao 搜广推与 LLM 应用 Alibaba / Taobao &amp; Tmall 2025-05-12 传统公式或 LTR 在 item level 优化 CTR、CVR、GMV，无法建模已选前缀对后续 item 的影响。SORT-Gen 用 causal Transformer 输入 item、user、position 和上游 CTR/CVR score，在每个前缀位置预测“累计行为数是否至少达到第档”的 ordered-regression 概率，从而估计加入 item 后的列表边际价值。推理先建立 CLICK、PAY、GMV 等目标队列，把搜索空间从全部候选降到队首。 Fidelity: 核心机制复现。实际训练 causal Transformer ordered regression，并执行多目标队列、mask-driven 单次批量评分和 MMR；私有曝光与线上 kernel 缩小。MovieLens rating/genre/popularity 分别代理点击、交易、商品内容和上游 score；没有淘宝真实曝光、CVR/GMV、用户商业特征和多模态 embedding。单次调用是 PyTorch 批量路径，不等价于论文生产 19 ms kernel；本地 proxy 指标不能和线上百分比直接比较。  reranking multi-objective ordered-regression diversity 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-sort-gen-b1c957ea">A Generative Re-ranking Model for List-level Multi-objective Optimization at Taobao</h2>
<p class="ar-learning-card__meta">Alibaba / Taobao &amp; Tmall · 论文公开：2025-05-12</p>
<p><strong>方法要点：</strong>传统公式或 LTR 在 item level 优化 CTR、CVR、GMV，无法建模已选前缀对后续 item 的影响。SORT-Gen 用 causal Transformer 输入 item、user、position 和上游 CTR/CVR score，在每个前缀位置预测“累计行为数是否至少达到第档”的 ordered-regression 概率，从而估计加入 item 后的列表边际价值。推理先建立 CLICK、PAY、GMV 等目标队列，把搜索空间从全部候选降到队首。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。实际训练 causal Transformer ordered regression，并执行多目标队列、mask-driven 单次批量评分和 MMR；私有曝光与线上 kernel 缩小。MovieLens rating/genre/popularity 分别代理点击、交易、商品内容和上游 score；没有淘宝真实曝光、CVR/GMV、用户商业特征和多模态 embedding。单次调用是 PyTorch 批量路径，不等价于论文生产 19 ms kernel；本地 proxy 指标不能和线上百分比直接比较。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.07197">原论文</a> · <a href="../../../../reproductions/2505.07197-sort-gen/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Contextual Distillation Model for Diversified Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2024-06-13 先用可控 MMR 教师产生兼顾相关性与多样性的列表，再把上下文边际收益蒸馏到可低延迟服务的学生。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 cdm 核心机制；相对 NDCG@10 +1.25%。  reranking diversity knowledge-distillation 搜广推 重排、展示与长期价值">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<h2 id="paper-recommendation-cdm-24f0cce6">Contextual Distillation Model for Diversified Recommendation</h2>
<p class="ar-learning-card__meta">Kuaishou Technology · 论文公开：2024-06-13</p>
<p><strong>方法要点：</strong>先用可控 MMR 教师产生兼顾相关性与多样性的列表，再把上下文边际收益蒸馏到可低延迟服务的学生。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 cdm 核心机制；相对 NDCG@10 +1.25%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2406.09021">原论文</a> · <a href="../../../../reproductions/2406.09021-cdm/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
