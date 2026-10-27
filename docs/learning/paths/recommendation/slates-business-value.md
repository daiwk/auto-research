---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 重排、展示与长期价值

[搜广推](index.md) / 144 个问题 · 36 篇论文

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
<p class="ar-learning-status" data-learning-status role="status">144 个问题 · 36 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:maps-creative" data-paper-title="MAPS: A Multi-Agent Personalized Script-Driven Video Advertising System Enhanced by Reinforcement Learning" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="MAPS: A Multi-Agent Personalized Script-Driven Video Advertising System Enhanced by Reinforcement Learning 搜广推与 LLM 应用 Beihang University 2026-10-19 从固定广告库存检索创意，无法及时适应个体偏好和反馈。MAPS以Profile提取画像、Scripter生成分镜、Director调用视频生成、Reflector归因反馈，区分画像问题与脚本问题并路由最小修改。画像不仅含兴趣，也包含呈现风格与决策倾向。脚本先SFT学习结构，再用结构正确性、个性化偏好和商品事实一致性构造混合奖励，以GRPO式组内标准化更新。它的关键是大模型/视频生成与私有反馈环境的组合，不是独立奖励公式。 成本过高，不复现（审查 DONE），不把通用GRPO或三个分数加权冒充视频广告生成系统。仅研究资料。成本过高，不复现（审查 DONE），不把通用GRPO或三个分数加权冒充视频广告生成系统。Profile/Reflector是Qwen3-VL-32B，Scripter是8B；SFT20epoch、最大8192tokens，随后RL5000步，原文在8张H100上实验。导演依赖Kling-Omni，反馈闭环依赖生产系统。单卡A100/A30与Mac不承担此完整矩阵，成本过高，不复现（审查 DONE）。没有本地模型、评测指标或GPU回执，不进入自动重试与Evolve。  展示层生成与个性化 个性化创意生成 搜广推 重排、展示与长期价值 MAPS 为什么把广告创作拆成 Profile、Scripter、Director、Reflector 四种角色？ 画像提炼需求与风格，脚本表达商品与分镜，视频执行负责呈现，反思将反馈归回可修改环节。分工让错误可定位，避免低反馈就重做全部链路。角色名不构成能力，实际需要语义模型、视频生成器与可信环境，本地因成本仅审查。 示意：用户理解正确但脚本夸大性能，应修文案；若视频执行违反脚本，则修生成环节，而非让画像 agent 背锅重写偏好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-maps-creative-255b1b1c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9827f5fc7350a04f">MAPS 为什么把广告创作拆成 Profile、Scripter、Director、Reflector 四种角色？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amaps-creative">MAPS: A Multi-Agent Personalized Script-Driven Video Advertising System Enhanced by Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>画像提炼需求与风格，脚本表达商品与分镜，视频执行负责呈现，反思将反馈归回可修改环节。分工让错误可定位，避免低反馈就重做全部链路。角色名不构成能力，实际需要语义模型、视频生成器与可信环境，本地因成本仅审查。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户理解正确但脚本夸大性能，应修文案；若视频执行违反脚本，则修生成环节，而非让画像 agent 背锅重写偏好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.25748v1">原论文</a> · <a href="../../../../recommendation-components/2610.25748-maps-creative/">实现解读</a> · <a href="#qa-9827f5fc7350a04f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:maps-creative" data-paper-title="MAPS: A Multi-Agent Personalized Script-Driven Video Advertising System Enhanced by Reinforcement Learning" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="MAPS: A Multi-Agent Personalized Script-Driven Video Advertising System Enhanced by Reinforcement Learning 搜广推与 LLM 应用 Beihang University 2026-10-19 从固定广告库存检索创意，无法及时适应个体偏好和反馈。MAPS以Profile提取画像、Scripter生成分镜、Director调用视频生成、Reflector归因反馈，区分画像问题与脚本问题并路由最小修改。画像不仅含兴趣，也包含呈现风格与决策倾向。脚本先SFT学习结构，再用结构正确性、个性化偏好和商品事实一致性构造混合奖励，以GRPO式组内标准化更新。它的关键是大模型/视频生成与私有反馈环境的组合，不是独立奖励公式。 成本过高，不复现（审查 DONE），不把通用GRPO或三个分数加权冒充视频广告生成系统。仅研究资料。成本过高，不复现（审查 DONE），不把通用GRPO或三个分数加权冒充视频广告生成系统。Profile/Reflector是Qwen3-VL-32B，Scripter是8B；SFT20epoch、最大8192tokens，随后RL5000步，原文在8张H100上实验。导演依赖Kling-Omni，反馈闭环依赖生产系统。单卡A100/A30与Mac不承担此完整矩阵，成本过高，不复现（审查 DONE）。没有本地模型、评测指标或GPU回执，不进入自动重试与Evolve。  展示层生成与个性化 个性化创意生成 搜广推 重排、展示与长期价值 MAPS的Reflector为什么区分画像错误与脚本错误，再路由最小修改？ 低反馈可能来自理解错人，也可能来自表达和商品事实有问题，全部重做会浪费计算并破坏本来正确的部分。分角色归因后只修改相关环节，让画像、脚本与视频生成保持可检查接口；混合奖励还需评估结构、个性化和事实。该链路依赖大模型与私有环境，本库因成本只收录研究，不提供关键词奖励替代复现。 示意：用户偏好判断正确，但脚本夸大了商品性能，应修脚本而非重建画像；若根本把送礼对象理解错，再精修镜头也无法修正推荐方向。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:maps-creative" data-paper-title="MAPS: A Multi-Agent Personalized Script-Driven Video Advertising System Enhanced by Reinforcement Learning" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="MAPS: A Multi-Agent Personalized Script-Driven Video Advertising System Enhanced by Reinforcement Learning 搜广推与 LLM 应用 Beihang University 2026-10-19 从固定广告库存检索创意，无法及时适应个体偏好和反馈。MAPS以Profile提取画像、Scripter生成分镜、Director调用视频生成、Reflector归因反馈，区分画像问题与脚本问题并路由最小修改。画像不仅含兴趣，也包含呈现风格与决策倾向。脚本先SFT学习结构，再用结构正确性、个性化偏好和商品事实一致性构造混合奖励，以GRPO式组内标准化更新。它的关键是大模型/视频生成与私有反馈环境的组合，不是独立奖励公式。 成本过高，不复现（审查 DONE），不把通用GRPO或三个分数加权冒充视频广告生成系统。仅研究资料。成本过高，不复现（审查 DONE），不把通用GRPO或三个分数加权冒充视频广告生成系统。Profile/Reflector是Qwen3-VL-32B，Scripter是8B；SFT20epoch、最大8192tokens，随后RL5000步，原文在8张H100上实验。导演依赖Kling-Omni，反馈闭环依赖生产系统。单卡A100/A30与Mac不承担此完整矩阵，成本过高，不复现（审查 DONE）。没有本地模型、评测指标或GPU回执，不进入自动重试与Evolve。  展示层生成与个性化 个性化创意生成 搜广推 重排、展示与长期价值 MAPS 的混合 reward 与关键词计数替代，相比保留哪些语义要求？ 结构奖含场景角色与物理合理性，个性化和商品一致性由语义 judge 评估，关键词覆盖无法判断事实矛盾或用户契合。代理可单测接口却不是同一算法证据。奖励配比也不保证 judge 可靠，必须区分文字得分与真实创意效果。 示意：脚本写满“耐用、适合你”可命中关键词，却可能把普通鞋描述成防火鞋；语义一致性要检查商品事实，而非只数赞美词。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-78415cab72cfc051">MAPS 的混合 reward 与关键词计数替代，相比保留哪些语义要求？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amaps-creative">MAPS: A Multi-Agent Personalized Script-Driven Video Advertising System Enhanced by Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>结构奖含场景角色与物理合理性，个性化和商品一致性由语义 judge 评估，关键词覆盖无法判断事实矛盾或用户契合。代理可单测接口却不是同一算法证据。奖励配比也不保证 judge 可靠，必须区分文字得分与真实创意效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>脚本写满“耐用、适合你”可命中关键词，却可能把普通鞋描述成防火鞋；语义一致性要检查商品事实，而非只数赞美词。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.25748v1">原论文</a> · <a href="../../../../recommendation-components/2610.25748-maps-creative/">实现解读</a> · <a href="#qa-78415cab72cfc051">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:maps-creative" data-paper-title="MAPS: A Multi-Agent Personalized Script-Driven Video Advertising System Enhanced by Reinforcement Learning" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="MAPS: A Multi-Agent Personalized Script-Driven Video Advertising System Enhanced by Reinforcement Learning 搜广推与 LLM 应用 Beihang University 2026-10-19 从固定广告库存检索创意，无法及时适应个体偏好和反馈。MAPS以Profile提取画像、Scripter生成分镜、Director调用视频生成、Reflector归因反馈，区分画像问题与脚本问题并路由最小修改。画像不仅含兴趣，也包含呈现风格与决策倾向。脚本先SFT学习结构，再用结构正确性、个性化偏好和商品事实一致性构造混合奖励，以GRPO式组内标准化更新。它的关键是大模型/视频生成与私有反馈环境的组合，不是独立奖励公式。 成本过高，不复现（审查 DONE），不把通用GRPO或三个分数加权冒充视频广告生成系统。仅研究资料。成本过高，不复现（审查 DONE），不把通用GRPO或三个分数加权冒充视频广告生成系统。Profile/Reflector是Qwen3-VL-32B，Scripter是8B；SFT20epoch、最大8192tokens，随后RL5000步，原文在8张H100上实验。导演依赖Kling-Omni，反馈闭环依赖生产系统。单卡A100/A30与Mac不承担此完整矩阵，成本过高，不复现（审查 DONE）。没有本地模型、评测指标或GPU回执，不进入自动重试与Evolve。  展示层生成与个性化 个性化创意生成 搜广推 重排、展示与长期价值 MAPS 的 group advantage 为什么在没有反馈差异时不能声称做了有效 RL？ 同上下文脚本奖励需形成相对差异，全部相同则中心化后优势为零，没有方向教策略更偏哪条；judge 和视频执行链也必须真实存在。来源明确不提供关键词 proxy 来替代整篇，公式可计算不意味着训练与环境已经复现。 示意：四个脚本都被简陋规则打满分，策略无从学习哪份更个性化；跑一次优化器不能当作四 agent 视频创作能力已提升。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-04085df67bb7bfc8">MAPS 的 group advantage 为什么在没有反馈差异时不能声称做了有效 RL？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amaps-creative">MAPS: A Multi-Agent Personalized Script-Driven Video Advertising System Enhanced by Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同上下文脚本奖励需形成相对差异，全部相同则中心化后优势为零，没有方向教策略更偏哪条；judge 和视频执行链也必须真实存在。来源明确不提供关键词 proxy 来替代整篇，公式可计算不意味着训练与环境已经复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>四个脚本都被简陋规则打满分，策略无从学习哪份更个性化；跑一次优化器不能当作四 agent 视频创作能力已提升。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.25748v1">原论文</a> · <a href="../../../../recommendation-components/2610.25748-maps-creative/">实现解读</a> · <a href="#qa-04085df67bb7bfc8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cohortmix-ts" data-paper-title="Challenges and Solutions for Bandits in the Wild: Warm-Started Mixture Bandits for Cross-Cohort Slate Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Challenges and Solutions for Bandits in the Wild: Warm-Started Mixture Bandits for Cross-Cohort Slate Recommendation 搜广推与 LLM 应用 DFKI / RPTU Kaiserslautern-Landau 2026-09-29 从历史 cohort 学习用户群和 item arm，用元数据给新用户构造固定强度的混合 Beta 先验；每轮用 Thompson sampling 选择未曝光 slate，并按用户反馈独立更新后验。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行固定强度 mixture prior、Thompson slate 与 posterior update；未复刻历史矩阵分解和 25 天部署。执行固定强度 mixture prior、Thompson slate 与 posterior update；未复刻历史矩阵分解和 25 天部署。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  cold-start slate-bandit cross-cohort-transfer 搜广推 重排、展示与长期价值 CohortMix-TS 为什么为新用户构造群组混合先验，而不是等待个人数据充足？ 新用户反馈少，个人成功率极不稳定；元数据得到群组 membership，再混合历史各组对 item arm 的估计，为初始探索提供方向。固定先验强度控制借用多少信任，后续个体反馈可逐步改写。群组信息是起点，不代表同组用户偏好必然相同。 示意：新用户尚未点击，可按其元数据混合两个兴趣群组的电影成功率；获得几次个人反馈后，后验应开始偏离群体平均。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-cohortmix-ts-f84d0507" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-75004509b0ab288c">CohortMix-TS 为什么为新用户构造群组混合先验，而不是等待个人数据充足？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acohortmix-ts">Challenges and Solutions for Bandits in the Wild: Warm-Started Mixture Bandits for Cross-Cohort Slate Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · DFKI / RPTU Kaiserslautern-Landau</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>新用户反馈少，个人成功率极不稳定；元数据得到群组 membership，再混合历史各组对 item arm 的估计，为初始探索提供方向。固定先验强度控制借用多少信任，后续个体反馈可逐步改写。群组信息是起点，不代表同组用户偏好必然相同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新用户尚未点击，可按其元数据混合两个兴趣群组的电影成功率；获得几次个人反馈后，后验应开始偏离群体平均。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37800">原论文</a> · <a href="../../../../reproductions/2609.37800-cohortmix-ts/">实现解读</a> · <a href="#qa-75004509b0ab288c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cohortmix-ts" data-paper-title="Challenges and Solutions for Bandits in the Wild: Warm-Started Mixture Bandits for Cross-Cohort Slate Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Challenges and Solutions for Bandits in the Wild: Warm-Started Mixture Bandits for Cross-Cohort Slate Recommendation 搜广推与 LLM 应用 DFKI / RPTU Kaiserslautern-Landau 2026-09-29 从历史 cohort 学习用户群和 item arm，用元数据给新用户构造固定强度的混合 Beta 先验；每轮用 Thompson sampling 选择未曝光 slate，并按用户反馈独立更新后验。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行固定强度 mixture prior、Thompson slate 与 posterior update；未复刻历史矩阵分解和 25 天部署。执行固定强度 mixture prior、Thompson slate 与 posterior update；未复刻历史矩阵分解和 25 天部署。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  cold-start slate-bandit cross-cohort-transfer 搜广推 重排、展示与长期价值 CohortMix-TS为什么用固定强度的混合Beta先验，而不直接搬来历史群组的全部计数？ 新用户可借相似群组的经验热启动，但历史样本规模若直接变成先验强度，会让个人新反馈长期无法改变判断。方法先混合群组均值，再用受控伪计数形成先验，并按个人曝光反馈独立更新。Thompson采样保留探索，不是永久按群组平均值确定推荐；本地只检验后验机制。 示意：群组有十万次反馈，新用户只有三次；若全部继承，三次反馈几乎不起作用。用固定先验强度，群体经验能引路，也允许个人兴趣逐渐接管。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cohortmix-ts" data-paper-title="Challenges and Solutions for Bandits in the Wild: Warm-Started Mixture Bandits for Cross-Cohort Slate Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Challenges and Solutions for Bandits in the Wild: Warm-Started Mixture Bandits for Cross-Cohort Slate Recommendation 搜广推与 LLM 应用 DFKI / RPTU Kaiserslautern-Landau 2026-09-29 从历史 cohort 学习用户群和 item arm，用元数据给新用户构造固定强度的混合 Beta 先验；每轮用 Thompson sampling 选择未曝光 slate，并按用户反馈独立更新后验。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行固定强度 mixture prior、Thompson slate 与 posterior update；未复刻历史矩阵分解和 25 天部署。执行固定强度 mixture prior、Thompson slate 与 posterior update；未复刻历史矩阵分解和 25 天部署。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  cold-start slate-bandit cross-cohort-transfer 搜广推 重排、展示与长期价值 CohortMix-TS 的 Thompson sampling 与总选后验均值最高 arm，探索方式有何不同？ 均值贪心忽略估计不确定性，Thompson sampling 从每个后验抽样，反馈少但潜力高的 arm 有机会被选中。随着数据增加不确定性下降，探索自然收敛。它并不保证每轮结果更好，来源本地只核验状态转换，不可据三种子诊断宣称推荐能力。 示意：甲均值略高且很确定，乙均值略低但样本少。抽样偶尔会让乙胜出以收集证据，贪心则可能永远不再尝试乙。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ea291b7996f80080">CohortMix-TS 的 Thompson sampling 与总选后验均值最高 arm，探索方式有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acohortmix-ts">Challenges and Solutions for Bandits in the Wild: Warm-Started Mixture Bandits for Cross-Cohort Slate Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · DFKI / RPTU Kaiserslautern-Landau</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>均值贪心忽略估计不确定性，Thompson sampling 从每个后验抽样，反馈少但潜力高的 arm 有机会被选中。随着数据增加不确定性下降，探索自然收敛。它并不保证每轮结果更好，来源本地只核验状态转换，不可据三种子诊断宣称推荐能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>甲均值略高且很确定，乙均值略低但样本少。抽样偶尔会让乙胜出以收集证据，贪心则可能永远不再尝试乙。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37800">原论文</a> · <a href="../../../../reproductions/2609.37800-cohortmix-ts/">实现解读</a> · <a href="#qa-ea291b7996f80080">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cohortmix-ts" data-paper-title="Challenges and Solutions for Bandits in the Wild: Warm-Started Mixture Bandits for Cross-Cohort Slate Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Challenges and Solutions for Bandits in the Wild: Warm-Started Mixture Bandits for Cross-Cohort Slate Recommendation 搜广推与 LLM 应用 DFKI / RPTU Kaiserslautern-Landau 2026-09-29 从历史 cohort 学习用户群和 item arm，用元数据给新用户构造固定强度的混合 Beta 先验；每轮用 Thompson sampling 选择未曝光 slate，并按用户反馈独立更新后验。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行固定强度 mixture prior、Thompson slate 与 posterior update；未复刻历史矩阵分解和 25 天部署。执行固定强度 mixture prior、Thompson slate 与 posterior update；未复刻历史矩阵分解和 25 天部署。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  cold-start slate-bandit cross-cohort-transfer 搜广推 重排、展示与长期价值 CohortMix-TS 更新 Beta 后验时，为何每位新用户应有独立计数并排除已曝光 slate？ 群组先验只初始化个人状态，之后成功与失败应写入该用户对应 arm，避免一人反馈修改所有新用户。每轮在未曝光集合选 slate，才符合连续探索口径；没有曝光的 arm 不应凭空记失败。共享先验与共享后验是不同设计。 示意：甲点击喜剧只增加甲的成功计数，不能替乙也加一次；本轮未展示的动作片没有反馈，不应自动记成负例来压低它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-dc1bab4e714e15fa">CohortMix-TS 更新 Beta 后验时，为何每位新用户应有独立计数并排除已曝光 slate？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acohortmix-ts">Challenges and Solutions for Bandits in the Wild: Warm-Started Mixture Bandits for Cross-Cohort Slate Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · DFKI / RPTU Kaiserslautern-Landau</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>群组先验只初始化个人状态，之后成功与失败应写入该用户对应 arm，避免一人反馈修改所有新用户。每轮在未曝光集合选 slate，才符合连续探索口径；没有曝光的 arm 不应凭空记失败。共享先验与共享后验是不同设计。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>甲点击喜剧只增加甲的成功计数，不能替乙也加一次；本轮未展示的动作片没有反馈，不应自动记成负例来压低它。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37800">原论文</a> · <a href="../../../../reproductions/2609.37800-cohortmix-ts/">实现解读</a> · <a href="#qa-dc1bab4e714e15fa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gese" data-paper-title="Generate to Explore, Select to Exploit: Aligning LLM-based Headline Generation with Personalized Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Generate to Explore, Select to Exploit: Aligning LLM-based Headline Generation with Personalized Recommendation 搜广推与 LLM 应用 Baidu 2026-09-14 集合级多样性/忠实度探索后，再以当前上下文选择个性化标题；生产系统报告 CTR +2.57%、停留时长 +0.87%。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。私有日志、生产 checkpoint 与 serving 栈均未复刻。本地只验证公开数据上的核心状态转换；未复刻私有训练数据、大模型生成器、生产流量反馈或在线服务。当前不映射 evolve，避免 registry-only 标签。线上数字来自论文正文 A/B，不与本地 MovieLens 结果混写。本地 seeds 42/43/44 见 metrics/movielens-100k-seeds42-44.json。首个 seed 的统一 NDCG@10 基线为 0.05401，实验组为 0.04421，相对变化 -18.15%。  presentation-layer headline-generation gspo bandit-selection 搜广推 重排、展示与长期价值 GESE 为什么把标题探索与个性化选择分开？ 生成阶段提出一组相关、多样且忠于内容的标题，选择阶段再结合当前用户与上下文决定展示哪个，避免一次通用生成承担所有个性化。候选质量是前提，selector 无法修复集合里没有忠实标题的问题，也不应把吸睛等同于真实满意。 示意：同一文章可突出方法、场景或结论三种角度，用户不同选择不同标题；三种都不能把原文没有的效果写出来。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-gese-4a69cb3b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0293f9dc765bc20a">GESE 为什么把标题探索与个性化选择分开？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agese">Generate to Explore, Select to Exploit: Aligning LLM-based Headline Generation with Personalized Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Baidu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>生成阶段提出一组相关、多样且忠于内容的标题，选择阶段再结合当前用户与上下文决定展示哪个，避免一次通用生成承担所有个性化。候选质量是前提，selector 无法修复集合里没有忠实标题的问题，也不应把吸睛等同于真实满意。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一文章可突出方法、场景或结论三种角度，用户不同选择不同标题；三种都不能把原文没有的效果写出来。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.15094">原论文</a> · <a href="../../../../reproductions/2609.15094-gese/">实现解读</a> · <a href="#qa-0293f9dc765bc20a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gese" data-paper-title="Generate to Explore, Select to Exploit: Aligning LLM-based Headline Generation with Personalized Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Generate to Explore, Select to Exploit: Aligning LLM-based Headline Generation with Personalized Recommendation 搜广推与 LLM 应用 Baidu 2026-09-14 集合级多样性/忠实度探索后，再以当前上下文选择个性化标题；生产系统报告 CTR +2.57%、停留时长 +0.87%。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。私有日志、生产 checkpoint 与 serving 栈均未复刻。本地只验证公开数据上的核心状态转换；未复刻私有训练数据、大模型生成器、生产流量反馈或在线服务。当前不映射 evolve，避免 registry-only 标签。线上数字来自论文正文 A/B，不与本地 MovieLens 结果混写。本地 seeds 42/43/44 见 metrics/movielens-100k-seeds42-44.json。首个 seed 的统一 NDCG@10 基线为 0.05401，实验组为 0.04421，相对变化 -18.15%。  presentation-layer headline-generation gspo bandit-selection 搜广推 重排、展示与长期价值 GESE为什么先探索一组多样且忠实的标题，再按当前上下文选择一个？ 只有一个固定标题无法适应不同用户，逐请求自由生成又可能昂贵且产生失真。集合探索先准备相互有区别、仍忠于内容的候选，selector再利用上下文选择，分离可复用创作与实时个性化。多样性不能以捏造事实换取；本地固定候选打分只验证选择组件，不等于重现完整标题生成训练。 示意：同一纪录片可有摄影视角或自然知识视角的忠实标题，面对不同用户选择其一；不能为了提高点击把影片没有的惊险情节写进候选集合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gese" data-paper-title="Generate to Explore, Select to Exploit: Aligning LLM-based Headline Generation with Personalized Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Generate to Explore, Select to Exploit: Aligning LLM-based Headline Generation with Personalized Recommendation 搜广推与 LLM 应用 Baidu 2026-09-14 集合级多样性/忠实度探索后，再以当前上下文选择个性化标题；生产系统报告 CTR +2.57%、停留时长 +0.87%。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。私有日志、生产 checkpoint 与 serving 栈均未复刻。本地只验证公开数据上的核心状态转换；未复刻私有训练数据、大模型生成器、生产流量反馈或在线服务。当前不映射 evolve，避免 registry-only 标签。线上数字来自论文正文 A/B，不与本地 MovieLens 结果混写。本地 seeds 42/43/44 见 metrics/movielens-100k-seeds42-44.json。首个 seed 的统一 NDCG@10 基线为 0.05401，实验组为 0.04421，相对变化 -18.15%。  presentation-layer headline-generation gspo bandit-selection 搜广推 重排、展示与长期价值 GESE 与为每个用户实时调用 LLM 写标题，相比怎样分配计算？ 预先探索可复用候选，把昂贵生成摊到多次请求，轻选择器负责实时适配；逐用户生成更灵活却增加延迟、重复成本与一致性风险。预生成也限制候选覆盖，机制取舍不能由本地确定性打分推断生产系统速度与效果。 示意：先为文章生成五种合法角度，千位用户只运行选择；如果某新场景所需角度不在五个里，selector 也不能现场创造它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-068e2515ee4f87c1">GESE 与为每个用户实时调用 LLM 写标题，相比怎样分配计算？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agese">Generate to Explore, Select to Exploit: Aligning LLM-based Headline Generation with Personalized Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Baidu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>预先探索可复用候选，把昂贵生成摊到多次请求，轻选择器负责实时适配；逐用户生成更灵活却增加延迟、重复成本与一致性风险。预生成也限制候选覆盖，机制取舍不能由本地确定性打分推断生产系统速度与效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先为文章生成五种合法角度，千位用户只运行选择；如果某新场景所需角度不在五个里，selector 也不能现场创造它。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.15094">原论文</a> · <a href="../../../../reproductions/2609.15094-gese/">实现解读</a> · <a href="#qa-068e2515ee4f87c1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gese" data-paper-title="Generate to Explore, Select to Exploit: Aligning LLM-based Headline Generation with Personalized Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Generate to Explore, Select to Exploit: Aligning LLM-based Headline Generation with Personalized Recommendation 搜广推与 LLM 应用 Baidu 2026-09-14 集合级多样性/忠实度探索后，再以当前上下文选择个性化标题；生产系统报告 CTR +2.57%、停留时长 +0.87%。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。私有日志、生产 checkpoint 与 serving 栈均未复刻。本地只验证公开数据上的核心状态转换；未复刻私有训练数据、大模型生成器、生产流量反馈或在线服务。当前不映射 evolve，避免 registry-only 标签。线上数字来自论文正文 A/B，不与本地 MovieLens 结果混写。本地 seeds 42/43/44 见 metrics/movielens-100k-seeds42-44.json。首个 seed 的统一 NDCG@10 基线为 0.05401，实验组为 0.04421，相对变化 -18.15%。  presentation-layer headline-generation gspo bandit-selection 搜广推 重排、展示与长期价值 GESE 本地候选打分实现为什么不能当作完整 LLM 生成训练？ 来源明确用确定性 relevance、多样性、faithfulness 和上下文 selector 限定机制，验证候选选择逻辑，并未复刻大模型集合生成与生产后训练。应报告这些算子与负结果，论文线上数值只作为原文证据，不能填进本地指标。 示意：手工准备五个标题再选一个，可检验 selector，但不证明模型能生成这五个忠实标题；两阶段不能因共用论文名而合并成已完成链路。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-21b38b3c2ed12207">GESE 本地候选打分实现为什么不能当作完整 LLM 生成训练？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agese">Generate to Explore, Select to Exploit: Aligning LLM-based Headline Generation with Personalized Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Baidu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>来源明确用确定性 relevance、多样性、faithfulness 和上下文 selector 限定机制，验证候选选择逻辑，并未复刻大模型集合生成与生产后训练。应报告这些算子与负结果，论文线上数值只作为原文证据，不能填进本地指标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>手工准备五个标题再选一个，可检验 selector，但不证明模型能生成这五个忠实标题；两阶段不能因共用论文名而合并成已完成链路。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.15094">原论文</a> · <a href="../../../../reproductions/2609.15094-gese/">实现解读</a> · <a href="#qa-21b38b3c2ed12207">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ogr" data-paper-title="Once Generated, Ranked: End-to-End Generative Slate Recommendation with Unified Semantic-Collaborative IDs" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Once Generated, Ranked: End-to-End Generative Slate Recommendation with Unified Semantic-Collaborative IDs 搜广推与 LLM 应用 Kuaishou Technology 2026-08-18 TUSID 融合语义码与协同码，GL2P 直接规划整张 slate，SPA 再用保守策略优化对齐列表级反馈。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation slate-ranking semantic-id reinforcement-learning 搜广推 重排、展示与长期价值 OGR 为什么用 TUSID 同时承载语义与协同，而不只做内容量化？ 内容码方便共享与新物品泛化，协同码保留行为关系，联合编码为整页规划提供两种线索。GL2P 再面向列表行动，SPA 用反馈调整，三个环节不同。联合空间可能有冲突，编码更丰富不自动代表页面质量更高。 示意：两件商品外观不同却常被一起消费，协同可连接；新品没有反馈时又可借内容，整页规划据此组织而非只按外观相似凑满。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-ogr-bedfe7b4" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-14454e397408092b">OGR 为什么用 TUSID 同时承载语义与协同，而不只做内容量化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aogr">Once Generated, Ranked: End-to-End Generative Slate Recommendation with Unified Semantic-Collaborative IDs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>内容码方便共享与新物品泛化，协同码保留行为关系，联合编码为整页规划提供两种线索。GL2P 再面向列表行动，SPA 用反馈调整，三个环节不同。联合空间可能有冲突，编码更丰富不自动代表页面质量更高。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两件商品外观不同却常被一起消费，协同可连接；新品没有反馈时又可借内容，整页规划据此组织而非只按外观相似凑满。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.17613">原论文</a> · <a href="../../../../reproductions/2608.17613-ogr/">实现解读</a> · <a href="#qa-14454e397408092b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ogr" data-paper-title="Once Generated, Ranked: End-to-End Generative Slate Recommendation with Unified Semantic-Collaborative IDs" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Once Generated, Ranked: End-to-End Generative Slate Recommendation with Unified Semantic-Collaborative IDs 搜广推与 LLM 应用 Kuaishou Technology 2026-08-18 TUSID 融合语义码与协同码，GL2P 直接规划整张 slate，SPA 再用保守策略优化对齐列表级反馈。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation slate-ranking semantic-id reinforcement-learning 搜广推 重排、展示与长期价值 OGR 为什么先融合语义码与协同码，再对整张 slate 做保守策略优化？ 语义码帮助内容相近物品共享结构，协同码补充用户行为关系，联合编码先决定生成空间怎样组织物品。列表规划再把整张推荐列表作为行动，使训练能考虑项目之间的配合；保守优化利用列表反馈调整策略，同时约束偏离已有监督策略的幅度。编码、规划和反馈分别解决表示、联合决策与稳定更新。 示意：一屏四个商品若逐个选最高分，可能全是相似运动鞋。联合列表目标可以考虑鞋、袜、背包的互补性，策略约束则防止为追求一次反馈突然生成完全陌生组合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ogr" data-paper-title="Once Generated, Ranked: End-to-End Generative Slate Recommendation with Unified Semantic-Collaborative IDs" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Once Generated, Ranked: End-to-End Generative Slate Recommendation with Unified Semantic-Collaborative IDs 搜广推与 LLM 应用 Kuaishou Technology 2026-08-18 TUSID 融合语义码与协同码，GL2P 直接规划整张 slate，SPA 再用保守策略优化对齐列表级反馈。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation slate-ranking semantic-id reinforcement-learning 搜广推 重排、展示与长期价值 OGR 的保守 SPA 与无约束奖励最大化，为什么保留 SFT 锚点？ 奖励可能稀疏或偏离真实满意，KL 惩罚限制相对监督策略的偏移，减少为代理高分生成极端列表。它在改进自由与稳定间取舍，不能消除奖励错误。来源本地整体 NDCG 与 Hit 方向不同，也不支持宣称全部列表目标改善。 示意：新颖性奖励可能鼓励全冷门无关商品，SFT 参考保留已学兴趣；约束太强又可能难探索，系数需要合适验证。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d6bca16b182e0c0a">OGR 的保守 SPA 与无约束奖励最大化，为什么保留 SFT 锚点？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aogr">Once Generated, Ranked: End-to-End Generative Slate Recommendation with Unified Semantic-Collaborative IDs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>奖励可能稀疏或偏离真实满意，KL 惩罚限制相对监督策略的偏移，减少为代理高分生成极端列表。它在改进自由与稳定间取舍，不能消除奖励错误。来源本地整体 NDCG 与 Hit 方向不同，也不支持宣称全部列表目标改善。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新颖性奖励可能鼓励全冷门无关商品，SFT 参考保留已学兴趣；约束太强又可能难探索，系数需要合适验证。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.17613">原论文</a> · <a href="../../../../reproductions/2608.17613-ogr/">实现解读</a> · <a href="#qa-d6bca16b182e0c0a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ogr" data-paper-title="Once Generated, Ranked: End-to-End Generative Slate Recommendation with Unified Semantic-Collaborative IDs" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Once Generated, Ranked: End-to-End Generative Slate Recommendation with Unified Semantic-Collaborative IDs 搜广推与 LLM 应用 Kuaishou Technology 2026-08-18 TUSID 融合语义码与协同码，GL2P 直接规划整张 slate，SPA 再用保守策略优化对齐列表级反馈。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation slate-ranking semantic-id reinforcement-learning 搜广推 重排、展示与长期价值 OGR 的 R(Y) 与 KL 应比较什么完整对象，为什么不能只看单个 item？ Y 是整张 slate，奖励、生成概率与参考分布需针对同一列表或定义的 token 分解，候选身份与去重规则一致。单品奖励平均不一定等于列表效用，固定分数混合也不等于策略更新。本地代理实现范围需以实际更新路径为准。 示意：五条各自相关却重复的列表，单品平均分仍高，列表奖励应看到组合冗余；否则并没有检验 GL2P 所要优化的整页决策。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c51a2b6ad730034d">OGR 的 R(Y) 与 KL 应比较什么完整对象，为什么不能只看单个 item？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aogr">Once Generated, Ranked: End-to-End Generative Slate Recommendation with Unified Semantic-Collaborative IDs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Y 是整张 slate，奖励、生成概率与参考分布需针对同一列表或定义的 token 分解，候选身份与去重规则一致。单品奖励平均不一定等于列表效用，固定分数混合也不等于策略更新。本地代理实现范围需以实际更新路径为准。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>五条各自相关却重复的列表，单品平均分仍高，列表奖励应看到组合冗余；否则并没有检验 GL2P 所要优化的整页决策。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.17613">原论文</a> · <a href="../../../../reproductions/2608.17613-ogr/">实现解读</a> · <a href="#qa-c51a2b6ad730034d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:drem" data-paper-title="DrEM: Dual-Side Robust Ensemble Ranking from Noisy User Preference Predictions in Video Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DrEM: Dual-Side Robust Ensemble Ranking from Noisy User Preference Predictions in Video Recommendation 搜广推与 LLM 应用 Shenzhen University 2026-08-13 把多路 pxtr 先变换到 logit 空间，对预测噪声做偏好保持筛选，并利用 pair-label 翻转风险反演修正训练目标；最后用一致性融合减小输入扰动导致的排序漂移。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为朴素三路加权融合，实验组加入偏好保持筛选与风险修正；seed 42 的 NDCG@10 为 0.07726，基线为 0.07518。  ranking multi-objective robust-learning video-recommendation 搜广推 重排、展示与长期价值 DrEM 为什么围绕 pair 偏好翻转研究噪声？ 排序依赖相对次序，分数误差不大也可能颠倒接近候选。logit 扰动、偏好保持筛选与风险修正关注这种顺序脆弱性，再以一致性融合降低漂移。单品预测准确不保证 pair 稳定，翻转风险估计本身也可能出错。 示意：甲乙分数只差零点零一，轻微噪声就交换首位；各自平均误差很小仍无法说明这个排序可靠，简单平均多路分数也不显式检查翻转。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-drem-6dedd99f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-44786acb8838e31e">DrEM 为什么围绕 pair 偏好翻转研究噪声？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adrem">DrEM: Dual-Side Robust Ensemble Ranking from Noisy User Preference Predictions in Video Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shenzhen University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>排序依赖相对次序，分数误差不大也可能颠倒接近候选。logit 扰动、偏好保持筛选与风险修正关注这种顺序脆弱性，再以一致性融合降低漂移。单品预测准确不保证 pair 稳定，翻转风险估计本身也可能出错。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>甲乙分数只差零点零一，轻微噪声就交换首位；各自平均误差很小仍无法说明这个排序可靠，简单平均多路分数也不显式检查翻转。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.12778">原论文</a> · <a href="../../../../reproductions/2608.12778-drem/">实现解读</a> · <a href="#qa-44786acb8838e31e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:drem" data-paper-title="DrEM: Dual-Side Robust Ensemble Ranking from Noisy User Preference Predictions in Video Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DrEM: Dual-Side Robust Ensemble Ranking from Noisy User Preference Predictions in Video Recommendation 搜广推与 LLM 应用 Shenzhen University 2026-08-13 把多路 pxtr 先变换到 logit 空间，对预测噪声做偏好保持筛选，并利用 pair-label 翻转风险反演修正训练目标；最后用一致性融合减小输入扰动导致的排序漂移。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为朴素三路加权融合，实验组加入偏好保持筛选与风险修正；seed 42 的 NDCG@10 为 0.07726，基线为 0.07518。  ranking multi-objective robust-learning video-recommendation 搜广推 重排、展示与长期价值 DrEM为什么对偏好翻转风险修正损失，而不是只对多个预测分求平均？ 各路预测存在噪声时，组合得到的物品偏好可能被翻转，简单平均仍可能稳定地学到错误次序。DrEM先筛选扰动下保持偏好的样本，再根据翻转风险修正目标，并用一致性融合降低排序漂移。修正依赖对噪声机制的估计，翻转率接近不稳定边界时不能无条件套用公式。 示意：两件视频原本只差一点分，轻微CTR噪声就让正负对颠倒；与其把这种随机次序当可靠标签，更应识别其风险并约束融合结果对扰动的敏感度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:drem" data-paper-title="DrEM: Dual-Side Robust Ensemble Ranking from Noisy User Preference Predictions in Video Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DrEM: Dual-Side Robust Ensemble Ranking from Noisy User Preference Predictions in Video Recommendation 搜广推与 LLM 应用 Shenzhen University 2026-08-13 把多路 pxtr 先变换到 logit 空间，对预测噪声做偏好保持筛选，并利用 pair-label 翻转风险反演修正训练目标；最后用一致性融合减小输入扰动导致的排序漂移。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为朴素三路加权融合，实验组加入偏好保持筛选与风险修正；seed 42 的 NDCG@10 为 0.07726，基线为 0.07518。  ranking multi-objective robust-learning video-recommendation 搜广推 重排、展示与长期价值 DrEM 的风险反演与普通扰动增强，额外依赖什么假设？ 增强只要求模型见过噪声输入，反演则按估计翻转概率组合正反标签损失，试图校正噪声前目标。因此依赖风险模型和非奇异分母，错误概率会残留偏差或放大方差。不能把任意加噪训练都称为完成反演，更不能预设其必胜普通增强。 示意：真实四成标签会翻转却按两成校正，训练目标仍有偏；若不知道风险，仅加随机扰动并不能合理生成那项反演系数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4cae3e0c16f4d980">DrEM 的风险反演与普通扰动增强，额外依赖什么假设？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adrem">DrEM: Dual-Side Robust Ensemble Ranking from Noisy User Preference Predictions in Video Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shenzhen University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>增强只要求模型见过噪声输入，反演则按估计翻转概率组合正反标签损失，试图校正噪声前目标。因此依赖风险模型和非奇异分母，错误概率会残留偏差或放大方差。不能把任意加噪训练都称为完成反演，更不能预设其必胜普通增强。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>真实四成标签会翻转却按两成校正，训练目标仍有偏；若不知道风险，仅加随机扰动并不能合理生成那项反演系数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.12778">原论文</a> · <a href="../../../../reproductions/2608.12778-drem/">实现解读</a> · <a href="#qa-4cae3e0c16f4d980">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:drem" data-paper-title="DrEM: Dual-Side Robust Ensemble Ranking from Noisy User Preference Predictions in Video Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DrEM: Dual-Side Robust Ensemble Ranking from Noisy User Preference Predictions in Video Recommendation 搜广推与 LLM 应用 Shenzhen University 2026-08-13 把多路 pxtr 先变换到 logit 空间，对预测噪声做偏好保持筛选，并利用 pair-label 翻转风险反演修正训练目标；最后用一致性融合减小输入扰动导致的排序漂移。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为朴素三路加权融合，实验组加入偏好保持筛选与风险修正；seed 42 的 NDCG@10 为 0.07726，基线为 0.07518。  ranking multi-objective robust-learning video-recommendation 搜广推 重排、展示与长期价值 DrEM 实现为什么要分别检查概率转 logit 与 1−2ρ？ 零或一概率会产生无限 logit，ρ 接近二分之一又让反演分母趋零，二者是不同数值边界。处理方式需明确记录，不能静默输出巨大梯度。筛选、修正和一致性融合也需各自执行，只有一个噪声函数不构成完整方法。 示意：翻转像抛硬币一样随机时，除以极小分母不会创造偏好证据；应报告不适用边界，而不是把异常大 loss 当成强监督。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8670300d1dfc49e8">DrEM 实现为什么要分别检查概率转 logit 与 1−2ρ？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adrem">DrEM: Dual-Side Robust Ensemble Ranking from Noisy User Preference Predictions in Video Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shenzhen University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>零或一概率会产生无限 logit，ρ 接近二分之一又让反演分母趋零，二者是不同数值边界。处理方式需明确记录，不能静默输出巨大梯度。筛选、修正和一致性融合也需各自执行，只有一个噪声函数不构成完整方法。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>翻转像抛硬币一样随机时，除以极小分母不会创造偏好证据；应报告不适用边界，而不是把异常大 loss 当成强监督。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.12778">原论文</a> · <a href="../../../../reproductions/2608.12778-drem/">实现解读</a> · <a href="#qa-8670300d1dfc49e8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dream" data-paper-title="DREAM: A Dual-Loop Recommendation Evolution Framework Powered by Large Language Models" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DREAM: A Dual-Loop Recommendation Evolution Framework Powered by Large Language Models 搜广推与 LLM 应用 Taobao &amp; Tmall Group / Alibaba 2026-08-10 工业推荐长期依赖人工配置和逐层独立优化，LLM 若直接生成自由文本又难以满足稳定性与安全要求。DREAM 是覆盖现有召回、精排和重排之上的控制平面：Intent Engine 将端上信号、session 行为和实时上下文整理成 L0 物理、L1 需求、L2 偏好三层意图；Meta Engine 依次执行 M1 意图摘要、M2 结合 Strategy Memory 的策略规划和 M3 确定性参数翻译；Unified Outlet 只接受白名单、范围内的 typed 参数。 Fidelity：核心机制复现。保留原推荐 backbone，实际执行分层意图、策略记忆、typed 参数编译、安全护栏及离线/影子在线双环；不以普通重排器代替核心控制链路。没有复刻淘宝私有多源信号、Qwen3 Meta Engine、真实流量和线上结论回存；本地“在线环”是 validation 内独立影子组，test 从未参与策略选择。本地对照口径：基线为同一 MovieLens-1M 切分和候选上的原 retrieval/ranking backbone；实验组只增加 DREAM 控制层，相对 NDCG@10 +39.36%，同时 head share +94.37%，不能只报正向相关性指标。  llm-recommendation ranking reranking intent-understanding online-policy serving 搜广推 重排、展示与长期价值 DREAM 为什么被称作现有链路上的控制平面？ Intent 和 Meta Engine 提炼状态并规划策略，Unified Outlet 把有界 typed 参数施加到已有召回、精排与重排，原模型继续负责候选评分。它协调配置而不是逐物品自由生成分数。控制层能够执行仍不说明策略有效，必须由观测反馈约束。 示意：用户转向露营时控制层调节品类权重与打散数量，底层网络继续打分；这与重训一套从历史直接输出全部候选的新模型不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-dream-c0565aca" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-3eb08e15565860a7">DREAM 为什么被称作现有链路上的控制平面？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adream">DREAM: A Dual-Loop Recommendation Evolution Framework Powered by Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Intent 和 Meta Engine 提炼状态并规划策略，Unified Outlet 把有界 typed 参数施加到已有召回、精排与重排，原模型继续负责候选评分。它协调配置而不是逐物品自由生成分数。控制层能够执行仍不说明策略有效，必须由观测反馈约束。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户转向露营时控制层调节品类权重与打散数量，底层网络继续打分；这与重训一套从历史直接输出全部候选的新模型不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.09408">原论文</a> · <a href="../../../../reproductions/2608.09408-dream/">实现解读</a> · <a href="#qa-3eb08e15565860a7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dream" data-paper-title="DREAM: A Dual-Loop Recommendation Evolution Framework Powered by Large Language Models" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DREAM: A Dual-Loop Recommendation Evolution Framework Powered by Large Language Models 搜广推与 LLM 应用 Taobao &amp; Tmall Group / Alibaba 2026-08-10 工业推荐长期依赖人工配置和逐层独立优化，LLM 若直接生成自由文本又难以满足稳定性与安全要求。DREAM 是覆盖现有召回、精排和重排之上的控制平面：Intent Engine 将端上信号、session 行为和实时上下文整理成 L0 物理、L1 需求、L2 偏好三层意图；Meta Engine 依次执行 M1 意图摘要、M2 结合 Strategy Memory 的策略规划和 M3 确定性参数翻译；Unified Outlet 只接受白名单、范围内的 typed 参数。 Fidelity：核心机制复现。保留原推荐 backbone，实际执行分层意图、策略记忆、typed 参数编译、安全护栏及离线/影子在线双环；不以普通重排器代替核心控制链路。没有复刻淘宝私有多源信号、Qwen3 Meta Engine、真实流量和线上结论回存；本地“在线环”是 validation 内独立影子组，test 从未参与策略选择。本地对照口径：基线为同一 MovieLens-1M 切分和候选上的原 retrieval/ranking backbone；实验组只增加 DREAM 控制层，相对 NDCG@10 +39.36%，同时 head share +94.37%，不能只报正向相关性指标。  llm-recommendation ranking reranking intent-understanding online-policy serving 搜广推 重排、展示与长期价值 DREAM为什么让LLM输出有界语义级别，再由确定性模块翻译为参数？ 自由文本难以直接满足线上接口与取值约束，DREAM把意图理解、策略规划和参数编译分开。LLM只表达允许的调整方向与强度，统一出口再执行白名单与范围检查；离线和线上反馈验证后才写回策略记忆。这样语义推理可影响现有链路，却不能任意改写生产模型或无限放大权重。 示意：模型判断用户想多看新类目，只能提出规定级别的增加多样性；编译器把它转成有限的打散数量，而不会执行一句没有边界的“尽量推新内容”。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dream" data-paper-title="DREAM: A Dual-Loop Recommendation Evolution Framework Powered by Large Language Models" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DREAM: A Dual-Loop Recommendation Evolution Framework Powered by Large Language Models 搜广推与 LLM 应用 Taobao &amp; Tmall Group / Alibaba 2026-08-10 工业推荐长期依赖人工配置和逐层独立优化，LLM 若直接生成自由文本又难以满足稳定性与安全要求。DREAM 是覆盖现有召回、精排和重排之上的控制平面：Intent Engine 将端上信号、session 行为和实时上下文整理成 L0 物理、L1 需求、L2 偏好三层意图；Meta Engine 依次执行 M1 意图摘要、M2 结合 Strategy Memory 的策略规划和 M3 确定性参数翻译；Unified Outlet 只接受白名单、范围内的 typed 参数。 Fidelity：核心机制复现。保留原推荐 backbone，实际执行分层意图、策略记忆、typed 参数编译、安全护栏及离线/影子在线双环；不以普通重排器代替核心控制链路。没有复刻淘宝私有多源信号、Qwen3 Meta Engine、真实流量和线上结论回存；本地“在线环”是 validation 内独立影子组，test 从未参与策略选择。本地对照口径：基线为同一 MovieLens-1M 切分和候选上的原 retrieval/ranking backbone；实验组只增加 DREAM 控制层，相对 NDCG@10 +39.36%，同时 head share +94.37%，不能只报正向相关性指标。  llm-recommendation ranking reranking intent-understanding online-policy serving 搜广推 重排、展示与长期价值 DREAM 的影子线上门控为什么不能等同于真实生产 A/B？ 独立影子数据能减少离线选择过拟合，却仍处于公开数据代理和固定反应环境，没有完整真实用户反馈。生产双环需要实际实验支持。本地相关性改善同时头部集中、新内容下降，应分别报告，而不是把独立验证通过当成真实生态收益。 示意：两组验证用户分开能防止同组反复挑策略，但没有真正展示后用户的适应和流失，仍无法测得上线一周的长期活跃。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-6eacc5f563f85ba1">DREAM 的影子线上门控为什么不能等同于真实生产 A/B？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adream">DREAM: A Dual-Loop Recommendation Evolution Framework Powered by Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立影子数据能减少离线选择过拟合，却仍处于公开数据代理和固定反应环境，没有完整真实用户反馈。生产双环需要实际实验支持。本地相关性改善同时头部集中、新内容下降，应分别报告，而不是把独立验证通过当成真实生态收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两组验证用户分开能防止同组反复挑策略，但没有真正展示后用户的适应和流失，仍无法测得上线一周的长期活跃。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.09408">原论文</a> · <a href="../../../../reproductions/2608.09408-dream/">实现解读</a> · <a href="#qa-6eacc5f563f85ba1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dream" data-paper-title="DREAM: A Dual-Loop Recommendation Evolution Framework Powered by Large Language Models" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DREAM: A Dual-Loop Recommendation Evolution Framework Powered by Large Language Models 搜广推与 LLM 应用 Taobao &amp; Tmall Group / Alibaba 2026-08-10 工业推荐长期依赖人工配置和逐层独立优化，LLM 若直接生成自由文本又难以满足稳定性与安全要求。DREAM 是覆盖现有召回、精排和重排之上的控制平面：Intent Engine 将端上信号、session 行为和实时上下文整理成 L0 物理、L1 需求、L2 偏好三层意图；Meta Engine 依次执行 M1 意图摘要、M2 结合 Strategy Memory 的策略规划和 M3 确定性参数翻译；Unified Outlet 只接受白名单、范围内的 typed 参数。 Fidelity：核心机制复现。保留原推荐 backbone，实际执行分层意图、策略记忆、typed 参数编译、安全护栏及离线/影子在线双环；不以普通重排器代替核心控制链路。没有复刻淘宝私有多源信号、Qwen3 Meta Engine、真实流量和线上结论回存；本地“在线环”是 validation 内独立影子组，test 从未参与策略选择。本地对照口径：基线为同一 MovieLens-1M 切分和候选上的原 retrieval/ranking backbone；实验组只增加 DREAM 控制层，相对 NDCG@10 +39.36%，同时 head share +94.37%，不能只报正向相关性指标。  llm-recommendation ranking reranking intent-understanding online-policy serving 搜广推 重排、展示与长期价值 DREAM 的语义级别怎样编译成可执行且有界的参数？ 离散级别只能通过白名单与确定翻译进入服务：排序覆盖由原权重和级别得到，类目打散数使用 max(1,默认数+bc) 保留下界。LLM 不能绕过接口输出任意值；记录需绑定编译后的实际配置，否则反馈会对应从未执行的提案。 示意：默认打散数一、级别负二，编译后仍至少一；若直接传负数，即使策略文字合理，也不满足实际服务契约。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0ad1fc02983bed80">DREAM 的语义级别怎样编译成可执行且有界的参数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adream">DREAM: A Dual-Loop Recommendation Evolution Framework Powered by Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>离散级别只能通过白名单与确定翻译进入服务：排序覆盖由原权重和级别得到，类目打散数使用 max(1,默认数+bc) 保留下界。LLM 不能绕过接口输出任意值；记录需绑定编译后的实际配置，否则反馈会对应从未执行的提案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>默认打散数一、级别负二，编译后仍至少一；若直接传负数，即使策略文字合理，也不满足实际服务契约。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.09408">原论文</a> · <a href="../../../../reproductions/2608.09408-dream/">实现解读</a> · <a href="#qa-0ad1fc02983bed80">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:metastrategy" data-paper-title="MetaStrategy: Generative Ranking with Executable LLM Strategies" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="MetaStrategy: Generative Ranking with Executable LLM Strategies 搜广推与 LLM 应用 Alibaba / Taobao 2026-08-10 固定打分网络难以按用户当下意图动态改变目标。MetaStrategy 让 LLM 输出带类型的 JSON 排序策略，包括目标权重、内容/类目偏好、约束与位置规则；确定性 compiler 将策略执行在候选列表上，避免自由文本直接控制线上排序。生产训练还用 replay 环境、自竞争 curriculum、evaluator-routed reward-augmented OPD 将 4B teacher 蒸馏到 0.8B student。 Fidelity：核心机制复现。实际训练上下文条件策略生成器，并以确定性 compiler 执行 typed strategy；本地负结果如实保留。未复刻淘宝私有日志、生产 replay、4B→0.8B OPD 与 nearline serving；公开实验只验证“生成 typed bundle → 校验 → 确定性执行”的核心路径。本地对照口径：基线为同预算单目标排序器，实验组为 typed strategy generator + deterministic compiler；NDCG@10 相对变化 -8.51%。  ranking llm-recommendation executable-strategy online-policy 搜广推 重排、展示与长期价值 MetaStrategy 为什么将目标权重、偏好、约束和位置规则放在 typed JSON 中？ 固定打分网络难快速表达当下意图，自由文本又难直接可靠执行。typed 策略给 compiler 明确可检查参数，让语义规划与确定排序分离。输出合法 JSON 只是格式门槛，规则可能不合理，仍需 replay、反馈和范围校验。 示意：用户要新鲜内容，策略明确增加新内容权重并设位置限制，比生成一句“多推荐新品”更可执行；合法字段也不保证这个权重对用户好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-metastrategy-1088d4bd" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0cb0e2b1dcb6379f">MetaStrategy 为什么将目标权重、偏好、约束和位置规则放在 typed JSON 中？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ametastrategy">MetaStrategy: Generative Ranking with Executable LLM Strategies</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定打分网络难快速表达当下意图，自由文本又难直接可靠执行。typed 策略给 compiler 明确可检查参数，让语义规划与确定排序分离。输出合法 JSON 只是格式门槛，规则可能不合理，仍需 replay、反馈和范围校验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户要新鲜内容，策略明确增加新内容权重并设位置限制，比生成一句“多推荐新品”更可执行；合法字段也不保证这个权重对用户好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.09440">原论文</a> · <a href="../../../../reproductions/2608.09440-metastrategy/">实现解读</a> · <a href="#qa-0cb0e2b1dcb6379f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:metastrategy" data-paper-title="MetaStrategy: Generative Ranking with Executable LLM Strategies" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="MetaStrategy: Generative Ranking with Executable LLM Strategies 搜广推与 LLM 应用 Alibaba / Taobao 2026-08-10 固定打分网络难以按用户当下意图动态改变目标。MetaStrategy 让 LLM 输出带类型的 JSON 排序策略，包括目标权重、内容/类目偏好、约束与位置规则；确定性 compiler 将策略执行在候选列表上，避免自由文本直接控制线上排序。生产训练还用 replay 环境、自竞争 curriculum、evaluator-routed reward-augmented OPD 将 4B teacher 蒸馏到 0.8B student。 Fidelity：核心机制复现。实际训练上下文条件策略生成器，并以确定性 compiler 执行 typed strategy；本地负结果如实保留。未复刻淘宝私有日志、生产 replay、4B→0.8B OPD 与 nearline serving；公开实验只验证“生成 typed bundle → 校验 → 确定性执行”的核心路径。本地对照口径：基线为同预算单目标排序器，实验组为 typed strategy generator + deterministic compiler；NDCG@10 相对变化 -8.51%。  ranking llm-recommendation executable-strategy online-policy 搜广推 重排、展示与长期价值 MetaStrategy为什么让LLM生成typed策略而不是直接生成最终物品次序？ 结构化策略把目标权重、类目偏好和位置约束显式化，确定性compiler再对真实候选执行，便于限制范围与审计失败原因。LLM负责理解意图，排序逻辑负责保证可执行，二者可分别更新与评价。JSON格式正确只证明接口合法，不证明策略有用，更不能用模型自评分替代真实回放反馈。 示意：用户想少看重复内容，模型输出限定的类目打散与权重参数，compiler据现有候选排表；若没有相关候选，应暴露限制，而不是凭空生成不存在的商品。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:metastrategy" data-paper-title="MetaStrategy: Generative Ranking with Executable LLM Strategies" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="MetaStrategy: Generative Ranking with Executable LLM Strategies 搜广推与 LLM 应用 Alibaba / Taobao 2026-08-10 固定打分网络难以按用户当下意图动态改变目标。MetaStrategy 让 LLM 输出带类型的 JSON 排序策略，包括目标权重、内容/类目偏好、约束与位置规则；确定性 compiler 将策略执行在候选列表上，避免自由文本直接控制线上排序。生产训练还用 replay 环境、自竞争 curriculum、evaluator-routed reward-augmented OPD 将 4B teacher 蒸馏到 0.8B student。 Fidelity：核心机制复现。实际训练上下文条件策略生成器，并以确定性 compiler 执行 typed strategy；本地负结果如实保留。未复刻淘宝私有日志、生产 replay、4B→0.8B OPD 与 nearline serving；公开实验只验证“生成 typed bundle → 校验 → 确定性执行”的核心路径。本地对照口径：基线为同预算单目标排序器，实验组为 typed strategy generator + deterministic compiler；NDCG@10 相对变化 -8.51%。  ranking llm-recommendation executable-strategy online-policy 搜广推 重排、展示与长期价值 MetaStrategy 与直接生成物品清单，相比审计和复用单位有什么不同？ 清单绑定当次候选，策略可在更新候选上重复执行并检查规则，使控制意图更透明；但 compiler 能表达的空间有限，复杂偏好未必能写成参数。来源完整生产蒸馏与本地 typed bundle 代理范围不同，不能把控制可执行当作同等智能。 示意：一条“同作者最多一项”可用于多份候选表，具体十本书清单则过期就失效；但规则无法独自判断所有内容语义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4de5dd9640bbf81d">MetaStrategy 与直接生成物品清单，相比审计和复用单位有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ametastrategy">MetaStrategy: Generative Ranking with Executable LLM Strategies</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>清单绑定当次候选，策略可在更新候选上重复执行并检查规则，使控制意图更透明；但 compiler 能表达的空间有限，复杂偏好未必能写成参数。来源完整生产蒸馏与本地 typed bundle 代理范围不同，不能把控制可执行当作同等智能。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一条“同作者最多一项”可用于多份候选表，具体十本书清单则过期就失效；但规则无法独自判断所有内容语义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.09440">原论文</a> · <a href="../../../../reproductions/2608.09440-metastrategy/">实现解读</a> · <a href="#qa-4de5dd9640bbf81d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:metastrategy" data-paper-title="MetaStrategy: Generative Ranking with Executable LLM Strategies" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="MetaStrategy: Generative Ranking with Executable LLM Strategies 搜广推与 LLM 应用 Alibaba / Taobao 2026-08-10 固定打分网络难以按用户当下意图动态改变目标。MetaStrategy 让 LLM 输出带类型的 JSON 排序策略，包括目标权重、内容/类目偏好、约束与位置规则；确定性 compiler 将策略执行在候选列表上，避免自由文本直接控制线上排序。生产训练还用 replay 环境、自竞争 curriculum、evaluator-routed reward-augmented OPD 将 4B teacher 蒸馏到 0.8B student。 Fidelity：核心机制复现。实际训练上下文条件策略生成器，并以确定性 compiler 执行 typed strategy；本地负结果如实保留。未复刻淘宝私有日志、生产 replay、4B→0.8B OPD 与 nearline serving；公开实验只验证“生成 typed bundle → 校验 → 确定性执行”的核心路径。本地对照口径：基线为同预算单目标排序器，实验组为 typed strategy generator + deterministic compiler；NDCG@10 相对变化 -8.51%。  ranking llm-recommendation executable-strategy online-policy 搜广推 重排、展示与长期价值 MetaStrategy 的 compiler 为什么必须对未知字段和越界值显式拒绝？ 否则语言模型可绕过允许空间，让策略评估与服务行为不一致。应绑定 schema、默认值与执行后的实际列表，记录失败而不是猜测修复含义。线上奖励路由与 teacher-student OPD 也不是只写一个 JSON 文件便已实现。 示意：模型给“无限提高购买权重”或不存在的字段，compiler 不应静默执行任意表达式；必须在受控参数范围内才能审计结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ea5ce8c5c8505db2">MetaStrategy 的 compiler 为什么必须对未知字段和越界值显式拒绝？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ametastrategy">MetaStrategy: Generative Ranking with Executable LLM Strategies</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>否则语言模型可绕过允许空间，让策略评估与服务行为不一致。应绑定 schema、默认值与执行后的实际列表，记录失败而不是猜测修复含义。线上奖励路由与 teacher-student OPD 也不是只写一个 JSON 文件便已实现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型给“无限提高购买权重”或不存在的字段，compiler 不应静默执行任意表达式；必须在受控参数范围内才能审计结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.09440">原论文</a> · <a href="../../../../reproductions/2608.09440-metastrategy/">实现解读</a> · <a href="#qa-ea5ce8c5c8505db2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:degr" data-paper-title="DEGR: Dual Exploration-Driven Generative Re-Ranking for Adaptive Cross-Request Context Bridging" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DEGR: Dual Exploration-Driven Generative Re-Ranking for Adaptive Cross-Request Context Bridging 搜广推与 LLM 应用 JD.com 2026-08-05 逐请求优化容易反复暴露相似商品。DEGR 在生成目标外加入同 cohort item embedding 的平方余弦约束，并用探索反馈形成 reward-adaptive ORPO，使偏好强度随真实探索收益变化；推理时再执行 diversity-aware greedy selection。 Fidelity：核心机制复现。实现 next-item CE、cohort 内多样性约束、adaptive reward-weighted ORPO 和多样性感知 greedy 重排。公开 MovieLens 没有跨请求曝光与探索 reward；本地以逆流行度代理奖励，未复刻京东十亿请求 reward model。本地对照口径：基线为同预算 CE generator，实验组加入 diversity 与 adaptive reward ORPO；相对基线 NDCG@10 +0.00%。  reranking slate-optimization exploration preference-optimization 搜广推 重排、展示与长期价值 DEGR 为什么把探索反馈与生成模型训练连接，而不只在末端随机插入新商品？ 末端随机探索能收集反馈，却未必让生成器学会哪些新内容值得继续探索。奖励自适应偏好更新将探索收益写回策略，同 cohort 表示正则和推理多样性选择再减少重复。探索应同时保持相关性，不能仅以头部占比下降证明用户受益。 示意：尝试一件冷门户外商品后若得到好反馈，训练可提高相关探索；纯随机插入每次从头碰运气，不会主动记住这次成功线索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-degr-c402d30b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4515d3bc01040e10">DEGR 为什么把探索反馈与生成模型训练连接，而不只在末端随机插入新商品？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adegr">DEGR: Dual Exploration-Driven Generative Re-Ranking for Adaptive Cross-Request Context Bridging</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · JD.com</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>末端随机探索能收集反馈，却未必让生成器学会哪些新内容值得继续探索。奖励自适应偏好更新将探索收益写回策略，同 cohort 表示正则和推理多样性选择再减少重复。探索应同时保持相关性，不能仅以头部占比下降证明用户受益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>尝试一件冷门户外商品后若得到好反馈，训练可提高相关探索；纯随机插入每次从头碰运气，不会主动记住这次成功线索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04809">原论文</a> · <a href="../../../../reproductions/2608.04809-degr/">实现解读</a> · <a href="#qa-4515d3bc01040e10">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:degr" data-paper-title="DEGR: Dual Exploration-Driven Generative Re-Ranking for Adaptive Cross-Request Context Bridging" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DEGR: Dual Exploration-Driven Generative Re-Ranking for Adaptive Cross-Request Context Bridging 搜广推与 LLM 应用 JD.com 2026-08-05 逐请求优化容易反复暴露相似商品。DEGR 在生成目标外加入同 cohort item embedding 的平方余弦约束，并用探索反馈形成 reward-adaptive ORPO，使偏好强度随真实探索收益变化；推理时再执行 diversity-aware greedy selection。 Fidelity：核心机制复现。实现 next-item CE、cohort 内多样性约束、adaptive reward-weighted ORPO 和多样性感知 greedy 重排。公开 MovieLens 没有跨请求曝光与探索 reward；本地以逆流行度代理奖励，未复刻京东十亿请求 reward model。本地对照口径：基线为同预算 CE generator，实验组加入 diversity 与 adaptive reward ORPO；相对基线 NDCG@10 +0.00%。  reranking slate-optimization exploration preference-optimization 搜广推 重排、展示与长期价值 DEGR为什么同时约束同cohort物品表示，并按探索收益调整偏好优化强度？ 逐请求追求高分可能跨请求反复暴露同类物品，表示约束先减少候选间的方向重叠。探索反馈再决定偏好更新应多强，避免对没有实际收益的探索机械强化；推理时的多样性选择补上输出层决策。训练表示分散不必然等于用户感知多样性，仍需同时看相关性与探索反馈。 示意：一组用户连续收到相似鞋款，单次列表看似合理却长期单调；模型既需减少候选同向集中，也需验证换入新类目是否真的带来有价值的探索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:degr" data-paper-title="DEGR: Dual Exploration-Driven Generative Re-Ranking for Adaptive Cross-Request Context Bridging" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DEGR: Dual Exploration-Driven Generative Re-Ranking for Adaptive Cross-Request Context Bridging 搜广推与 LLM 应用 JD.com 2026-08-05 逐请求优化容易反复暴露相似商品。DEGR 在生成目标外加入同 cohort item embedding 的平方余弦约束，并用探索反馈形成 reward-adaptive ORPO，使偏好强度随真实探索收益变化；推理时再执行 diversity-aware greedy selection。 Fidelity：核心机制复现。实现 next-item CE、cohort 内多样性约束、adaptive reward-weighted ORPO 和多样性感知 greedy 重排。公开 MovieLens 没有跨请求曝光与探索 reward；本地以逆流行度代理奖励，未复刻京东十亿请求 reward model。本地对照口径：基线为同预算 CE generator，实验组加入 diversity 与 adaptive reward ORPO；相对基线 NDCG@10 +0.00%。  reranking slate-optimization exploration preference-optimization 搜广推 重排、展示与长期价值 DEGR 的训练多样性正则与推理 diversity-aware greedy，作用阶段有何不同？ 平方余弦约束改变物品表示，让同 cohort 更少坍缩；推理选择则依据已选项控制当前列表冗余。前者塑造长期空间，后者处理单次组合，两者不能互代。正则过强会推开真实相似品，推理过强也会牺牲相关性，需分别消融。 示意：把物品向量稍微拉开不能保证一屏不重复；反过来每屏强行换类别也不能修复训练表示全挤在热门方向，两个环节需单独检查。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ce7f25a54ba8e30c">DEGR 的训练多样性正则与推理 diversity-aware greedy，作用阶段有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adegr">DEGR: Dual Exploration-Driven Generative Re-Ranking for Adaptive Cross-Request Context Bridging</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · JD.com</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>平方余弦约束改变物品表示，让同 cohort 更少坍缩；推理选择则依据已选项控制当前列表冗余。前者塑造长期空间，后者处理单次组合，两者不能互代。正则过强会推开真实相似品，推理过强也会牺牲相关性，需分别消融。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把物品向量稍微拉开不能保证一屏不重复；反过来每屏强行换类别也不能修复训练表示全挤在热门方向，两个环节需单独检查。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04809">原论文</a> · <a href="../../../../reproductions/2608.04809-degr/">实现解读</a> · <a href="#qa-ce7f25a54ba8e30c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:degr" data-paper-title="DEGR: Dual Exploration-Driven Generative Re-Ranking for Adaptive Cross-Request Context Bridging" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DEGR: Dual Exploration-Driven Generative Re-Ranking for Adaptive Cross-Request Context Bridging 搜广推与 LLM 应用 JD.com 2026-08-05 逐请求优化容易反复暴露相似商品。DEGR 在生成目标外加入同 cohort item embedding 的平方余弦约束，并用探索反馈形成 reward-adaptive ORPO，使偏好强度随真实探索收益变化；推理时再执行 diversity-aware greedy selection。 Fidelity：核心机制复现。实现 next-item CE、cohort 内多样性约束、adaptive reward-weighted ORPO 和多样性感知 greedy 重排。公开 MovieLens 没有跨请求曝光与探索 reward；本地以逆流行度代理奖励，未复刻京东十亿请求 reward model。本地对照口径：基线为同预算 CE generator，实验组加入 diversity 与 adaptive reward ORPO；相对基线 NDCG@10 +0.00%。  reranking slate-optimization exploration preference-optimization 搜广推 重排、展示与长期价值 DEGR 本地 NDCG 持平但 head share 下降，应怎样验收机制而不夸大效果？ 来源确实执行偏好与 diversity pair 更新，可据日志检查算子与次数，再分别报告排序与分布变化。NDCG 零增量表示本协议未看到主质量改善，头部略降只说明曝光集中度变化。不能用更新次数或三项损失存在，替代用户价值证据。 示意：榜单少了一点热门片却没有提高相关项位置，可以说分布更分散，不能说用户一定更满意，也不能把持平改写为全面优化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e3a307970f00ddbf">DEGR 本地 NDCG 持平但 head share 下降，应怎样验收机制而不夸大效果？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adegr">DEGR: Dual Exploration-Driven Generative Re-Ranking for Adaptive Cross-Request Context Bridging</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · JD.com</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>来源确实执行偏好与 diversity pair 更新，可据日志检查算子与次数，再分别报告排序与分布变化。NDCG 零增量表示本协议未看到主质量改善，头部略降只说明曝光集中度变化。不能用更新次数或三项损失存在，替代用户价值证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>榜单少了一点热门片却没有提高相关项位置，可以说分布更分散，不能说用户一定更满意，也不能把持平改写为全面优化。</p>
<p class="ar-learning-sources">依据：本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04809">原论文</a> · <a href="../../../../reproductions/2608.04809-degr/">实现解读</a> · <a href="#qa-e3a307970f00ddbf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:steps" data-paper-title="A Self-Triggered Agentic Push Recommendation System" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="A Self-Triggered Agentic Push Recommendation System 搜广推与 LLM 应用 ByteDance / Douyin 2026-08-03 固定频控无法实时调整，周期轮询又在成本与时机间冲突。STEPS 把“是否推送”和“何时再次唤醒”合成闭环：planning agent 用 gated ordinal regression 规划间隔，execution agent 用轨迹回报决定发送，轻量 filter agent 控制算力并拦截异常计划。 Fidelity：核心机制复现。公开数据只验证论文机制，不模拟生产流量。MovieLens 没有真实 push permission、触达成本和 wall-clock 唤醒器，只验证决策分解。本地对照口径：基线为共享 transition + content scorer，实验组只加入 STEPS 核心机制；相对 NDCG@10 +66.05%。  push-recommendation agentic-recommendation decision-transformer serving 搜广推 重排、展示与长期价值 STEPS为什么同时决定发不发和何时再唤醒？ 固定频控不能跟踪用户状态，周期轮询又浪费或错时。规划间隔、执行动作和轻量过滤形成自触发闭环，把时机与计算成本一起纳入决策。 例如这次不推，也需决定多久后再评估，而不是无限等到固定轮询点。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-steps-e0be3966" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-dc79db1d208005a2">STEPS为什么同时决定发不发和何时再唤醒？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asteps">A Self-Triggered Agentic Push Recommendation System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定频控不能跟踪用户状态，周期轮询又浪费或错时。规划间隔、执行动作和轻量过滤形成自触发闭环，把时机与计算成本一起纳入决策。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如这次不推，也需决定多久后再评估，而不是无限等到固定轮询点。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01949">原论文</a> · <a href="../../../../reproductions/2608.01949-steps/">实现解读</a> · <a href="#qa-dc79db1d208005a2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:steps" data-paper-title="A Self-Triggered Agentic Push Recommendation System" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="A Self-Triggered Agentic Push Recommendation System 搜广推与 LLM 应用 ByteDance / Douyin 2026-08-03 固定频控无法实时调整，周期轮询又在成本与时机间冲突。STEPS 把“是否推送”和“何时再次唤醒”合成闭环：planning agent 用 gated ordinal regression 规划间隔，execution agent 用轨迹回报决定发送，轻量 filter agent 控制算力并拦截异常计划。 Fidelity：核心机制复现。公开数据只验证论文机制，不模拟生产流量。MovieLens 没有真实 push permission、触达成本和 wall-clock 唤醒器，只验证决策分解。本地对照口径：基线为共享 transition + content scorer，实验组只加入 STEPS 核心机制；相对 NDCG@10 +66.05%。  push-recommendation agentic-recommendation decision-transformer serving 搜广推 重排、展示与长期价值 STEPS 为什么把“下次何时唤醒”和“此刻是否推送”交给不同 agent，并加轻量过滤？ 固定频控不能适应用户状态，频繁轮询又浪费计算。规划 agent 用有序间隔预测决定何时再观察，执行 agent 根据轨迹回报选择发送，过滤器先拦截异常或低价值计划。分工把观察频率与发送决策联合成闭环，仍需区分等待收益与消息收益；本地代理排序结果不能替代真实推送留存实验。 示意：用户刚忽略一条通知，规划器可延长下次唤醒间隔；到时执行器发现没有值得发的内容，仍可选择不发。过滤器则避免异常计划让系统每秒反复唤醒。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:steps" data-paper-title="A Self-Triggered Agentic Push Recommendation System" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="A Self-Triggered Agentic Push Recommendation System 搜广推与 LLM 应用 ByteDance / Douyin 2026-08-03 固定频控无法实时调整，周期轮询又在成本与时机间冲突。STEPS 把“是否推送”和“何时再次唤醒”合成闭环：planning agent 用 gated ordinal regression 规划间隔，execution agent 用轨迹回报决定发送，轻量 filter agent 控制算力并拦截异常计划。 Fidelity：核心机制复现。公开数据只验证论文机制，不模拟生产流量。MovieLens 没有真实 push permission、触达成本和 wall-clock 唤醒器，只验证决策分解。本地对照口径：基线为共享 transition + content scorer，实验组只加入 STEPS 核心机制；相对 NDCG@10 +66.05%。  push-recommendation agentic-recommendation decision-transformer serving 搜广推 重排、展示与长期价值 planning、execution与filter三角色是否只是同一分数阈值？ planning预测唤醒间隔，execution评发送，filter限制成本与异常计划，职责不同。把三个都压成发送概率会丢掉调度与防护机制，不能宣称完整agentic push。 例如决定明早再醒与决定此刻是否推送，是两个不同输出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c53833bd32479dc4">planning、execution与filter三角色是否只是同一分数阈值？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asteps">A Self-Triggered Agentic Push Recommendation System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>planning预测唤醒间隔，execution评发送，filter限制成本与异常计划，职责不同。把三个都压成发送概率会丢掉调度与防护机制，不能宣称完整agentic push。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如决定明早再醒与决定此刻是否推送，是两个不同输出。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01949">原论文</a> · <a href="../../../../reproductions/2608.01949-steps/">实现解读</a> · <a href="#qa-c53833bd32479dc4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:steps" data-paper-title="A Self-Triggered Agentic Push Recommendation System" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="A Self-Triggered Agentic Push Recommendation System 搜广推与 LLM 应用 ByteDance / Douyin 2026-08-03 固定频控无法实时调整，周期轮询又在成本与时机间冲突。STEPS 把“是否推送”和“何时再次唤醒”合成闭环：planning agent 用 gated ordinal regression 规划间隔，execution agent 用轨迹回报决定发送，轻量 filter agent 控制算力并拦截异常计划。 Fidelity：核心机制复现。公开数据只验证论文机制，不模拟生产流量。MovieLens 没有真实 push permission、触达成本和 wall-clock 唤醒器，只验证决策分解。本地对照口径：基线为共享 transition + content scorer，实验组只加入 STEPS 核心机制；相对 NDCG@10 +66.05%。  push-recommendation agentic-recommendation decision-transformer serving 搜广推 重排、展示与长期价值 STEPS本地是否有真实permission和wall-clock唤醒器？ 没有，MovieLens只验证决策分解，缺少push授权、触达成本和实际时钟调度。模拟间隔不代表设备会真的唤醒，执行仍需服务契约和真实回报。 例如数组里的下一次时间更新，不等于用户手机实际收到一条通知。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-af395a3461d3e92d">STEPS本地是否有真实permission和wall-clock唤醒器？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asteps">A Self-Triggered Agentic Push Recommendation System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有，MovieLens只验证决策分解，缺少push授权、触达成本和实际时钟调度。模拟间隔不代表设备会真的唤醒，执行仍需服务契约和真实回报。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如数组里的下一次时间更新，不等于用户手机实际收到一条通知。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01949">原论文</a> · <a href="../../../../reproductions/2608.01949-steps/">实现解读</a> · <a href="#qa-af395a3461d3e92d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:director" data-paper-title="DIRECTOR: Dynamic Index-based Recommendation with Transport-Optimized Retrieval" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DIRECTOR: Dynamic Index-based Recommendation with Transport-Optimized Retrieval 搜广推与 LLM 应用 University of Science and Technology of China 2026-07-29 每个展示位置生成动态索引分布，以 Sinkhorn 最优运输联合约束所有位置；最终用全局匹配而非独立 argmax 解码，减少冲突并一次并行产生整张 slate。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为各位置独立动态索引，实验组加入 Sinkhorn transport 与硬全局匹配；seed 42 的 NDCG@10 为 0.05334，基线为 0.03857。  reranking dynamic-index optimal-transport non-autoregressive 搜广推 重排、展示与长期价值 DIRECTOR 的动态索引分布为什么要覆盖所有展示位置？ 每个位置都要从候选中选物品，独立分布会让多个位置争抢同一高分项。联合运输把位置供给与物品分配联系起来，随后硬匹配产生可用 slate。并行生成减少逐步解码依赖，但联合可行性和相关性仍需同时检查。 示意：五个位置都最喜欢电影甲，独立预测会重复五次；联合分配要求它只占合法数量位置，其余位置选择互补候选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-director-8aa08907" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2b387bec5d3f4c84">DIRECTOR 的动态索引分布为什么要覆盖所有展示位置？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adirector">DIRECTOR: Dynamic Index-based Recommendation with Transport-Optimized Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每个位置都要从候选中选物品，独立分布会让多个位置争抢同一高分项。联合运输把位置供给与物品分配联系起来，随后硬匹配产生可用 slate。并行生成减少逐步解码依赖，但联合可行性和相关性仍需同时检查。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>五个位置都最喜欢电影甲，独立预测会重复五次；联合分配要求它只占合法数量位置，其余位置选择互补候选。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26418">原论文</a> · <a href="../../../../reproductions/2607.26418-director/">实现解读</a> · <a href="#qa-2b387bec5d3f4c84">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:director" data-paper-title="DIRECTOR: Dynamic Index-based Recommendation with Transport-Optimized Retrieval" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DIRECTOR: Dynamic Index-based Recommendation with Transport-Optimized Retrieval 搜广推与 LLM 应用 University of Science and Technology of China 2026-07-29 每个展示位置生成动态索引分布，以 Sinkhorn 最优运输联合约束所有位置；最终用全局匹配而非独立 argmax 解码，减少冲突并一次并行产生整张 slate。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为各位置独立动态索引，实验组加入 Sinkhorn transport 与硬全局匹配；seed 42 的 NDCG@10 为 0.05334，基线为 0.03857。  reranking dynamic-index optimal-transport non-autoregressive 搜广推 重排、展示与长期价值 DIRECTOR为什么用Sinkhorn加全局匹配，而不让每个位置独立挑最高分物品？ 独立位置预测可能都选择同一个热门物品，忽略位置之间争夺候选的耦合。Sinkhorn将分数转成受行列边际约束的软运输计划，训练时联合分配所有位置；最终再以全局匹配得到不冲突的硬列表。软分布本身还不是可展示排列，不能用独立argmax替代最后的组合解码。 示意：三个位置都最喜欢A，独立取最大会重复三次；全局匹配会同时考虑把A给最需要的位置、把B和C分给其余位置，从而形成一张合法列表。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:director" data-paper-title="DIRECTOR: Dynamic Index-based Recommendation with Transport-Optimized Retrieval" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DIRECTOR: Dynamic Index-based Recommendation with Transport-Optimized Retrieval 搜广推与 LLM 应用 University of Science and Technology of China 2026-07-29 每个展示位置生成动态索引分布，以 Sinkhorn 最优运输联合约束所有位置；最终用全局匹配而非独立 argmax 解码，减少冲突并一次并行产生整张 slate。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为各位置独立动态索引，实验组加入 Sinkhorn transport 与硬全局匹配；seed 42 的 NDCG@10 为 0.05334，基线为 0.03857。  reranking dynamic-index optimal-transport non-autoregressive 搜广推 重排、展示与长期价值 DIRECTOR 的 Sinkhorn 软运输与最终全局硬匹配，为什么不能只保留前者后逐行 argmax？ 软矩阵满足的是连续约束，逐行取最大仍可能撞到同一列，破坏唯一分配。全局匹配在离散空间共同选择，考虑某位置让步换来的总分。温度与迭代影响软近似，但不能用近似双随机直接保证独立取最大合法。 示意：两行都把甲分到零点六、乙零点四，即使列约束经过近似处理，独立取甲仍冲突；硬匹配需让其中一行选乙。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-33ef213afb9625c2">DIRECTOR 的 Sinkhorn 软运输与最终全局硬匹配，为什么不能只保留前者后逐行 argmax？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adirector">DIRECTOR: Dynamic Index-based Recommendation with Transport-Optimized Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>软矩阵满足的是连续约束，逐行取最大仍可能撞到同一列，破坏唯一分配。全局匹配在离散空间共同选择，考虑某位置让步换来的总分。温度与迭代影响软近似，但不能用近似双随机直接保证独立取最大合法。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两行都把甲分到零点六、乙零点四，即使列约束经过近似处理，独立取甲仍冲突；硬匹配需让其中一行选乙。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26418">原论文</a> · <a href="../../../../reproductions/2607.26418-director/">实现解读</a> · <a href="#qa-33ef213afb9625c2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:director" data-paper-title="DIRECTOR: Dynamic Index-based Recommendation with Transport-Optimized Retrieval" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DIRECTOR: Dynamic Index-based Recommendation with Transport-Optimized Retrieval 搜广推与 LLM 应用 University of Science and Technology of China 2026-07-29 每个展示位置生成动态索引分布，以 Sinkhorn 最优运输联合约束所有位置；最终用全局匹配而非独立 argmax 解码，减少冲突并一次并行产生整张 slate。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为各位置独立动态索引，实验组加入 Sinkhorn transport 与硬全局匹配；seed 42 的 NDCG@10 为 0.05334，基线为 0.03857。  reranking dynamic-index optimal-transport non-autoregressive 搜广推 重排、展示与长期价值 DIRECTOR 的 score 矩阵与最终 permutation 应如何对齐候选索引？ 矩阵行代表位置、列代表候选，运输和硬匹配需使用同一列身份，取回物品时按全局匹配索引而不是各行排序索引。候选不足或重复身份需明确约束；来源本地比较独立索引与联合匹配，不能把电影代理结果外推生产 valid view。 示意：模型列二对应电影乙，匹配后若用已重排候选表的列二取值，会拿错电影；数值目标正确也无法保证实际展示列表合法。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-adf26f4d49897225">DIRECTOR 的 score 矩阵与最终 permutation 应如何对齐候选索引？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adirector">DIRECTOR: Dynamic Index-based Recommendation with Transport-Optimized Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>矩阵行代表位置、列代表候选，运输和硬匹配需使用同一列身份，取回物品时按全局匹配索引而不是各行排序索引。候选不足或重复身份需明确约束；来源本地比较独立索引与联合匹配，不能把电影代理结果外推生产 valid view。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型列二对应电影乙，匹配后若用已重排候选表的列二取值，会拿错电影；数值目标正确也无法保证实际展示列表合法。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26418">原论文</a> · <a href="../../../../reproductions/2607.26418-director/">实现解读</a> · <a href="#qa-adf26f4d49897225">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:psg" data-paper-title="PSG: Pair-Space Generation for Efficient Generative Reranking" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="PSG: Pair-Space Generation for Efficient Generative Reranking 搜广推与 LLM 应用 Kuaishou Technology 2026-07-29 把相邻两个 item 编成一个请求内 pair token，在 pair 空间生成半长度序列，再无损展开为 item slate；pair scorer 显式保留顺序，重复约束保证展开结果可用。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为六步 item-space 生成，实验组为三步 pair-space 生成与展开；seed 42 的 NDCG@10 为 0.04826，基线为 0.05401，负结果保留。  reranking generative-recommendation pair-token serving 搜广推 重排、展示与长期价值 PSG 为什么把请求内两个位置定义为有序 pair？ pair 同时覆盖两个展示位，减少自回归步数但保留谁先谁后，下一 pair 还依赖此前组合。有序打包能无损展开给定列表，却不意味着选择算法无损或配对空间无成本。奇数长度和重复也需要明确规则。 示意：基础教程在前、实操在后与反过来体验不同，两者应是不同 pair；把它们当无序集合会丢掉展示顺序信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-psg-c3e023ce" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-bd4316b465920770">PSG 为什么把请求内两个位置定义为有序 pair？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apsg">PSG: Pair-Space Generation for Efficient Generative Reranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>pair 同时覆盖两个展示位，减少自回归步数但保留谁先谁后，下一 pair 还依赖此前组合。有序打包能无损展开给定列表，却不意味着选择算法无损或配对空间无成本。奇数长度和重复也需要明确规则。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>基础教程在前、实操在后与反过来体验不同，两者应是不同 pair；把它们当无序集合会丢掉展示顺序信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26427">原论文</a> · <a href="../../../../reproductions/2607.26427-psg/">实现解读</a> · <a href="#qa-bd4316b465920770">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:psg" data-paper-title="PSG: Pair-Space Generation for Efficient Generative Reranking" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="PSG: Pair-Space Generation for Efficient Generative Reranking 搜广推与 LLM 应用 Kuaishou Technology 2026-07-29 把相邻两个 item 编成一个请求内 pair token，在 pair 空间生成半长度序列，再无损展开为 item slate；pair scorer 显式保留顺序，重复约束保证展开结果可用。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为六步 item-space 生成，实验组为三步 pair-space 生成与展开；seed 42 的 NDCG@10 为 0.04826，基线为 0.05401，负结果保留。  reranking generative-recommendation pair-token serving 搜广推 重排、展示与长期价值 PSG 把两个相邻物品打包为 pair token，为什么能减少生成步数又必须保留内部顺序？ pair token 把两个位置联合建模，生成半长的 pair 序列后可无损展开，因此自回归步数减少。但一个 pair 的两个物品顺序会影响展示与后续条件，不能当作无序集合；重复约束还要保证不同 pair 展开后没有不可用重复。减少步数把一部分复杂度转移到配对空间和评分上，并非免费加速。 示意：六个位置原本生成六次，改成三次分别生成有序二元组。二元组“咖啡机、咖啡豆”与反过来不同；若第二组再次含咖啡机，展开前还需要处理重复。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:psg" data-paper-title="PSG: Pair-Space Generation for Efficient Generative Reranking" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="PSG: Pair-Space Generation for Efficient Generative Reranking 搜广推与 LLM 应用 Kuaishou Technology 2026-07-29 把相邻两个 item 编成一个请求内 pair token，在 pair 空间生成半长度序列，再无损展开为 item slate；pair scorer 显式保留顺序，重复约束保证展开结果可用。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为六步 item-space 生成，实验组为三步 pair-space 生成与展开；seed 42 的 NDCG@10 为 0.04826，基线为 0.05401，负结果保留。  reranking generative-recommendation pair-token serving 搜广推 重排、展示与长期价值 PSG 与普通两步并行 item 预测，相比 pair scorer 学什么依赖？ 独立位置头可同时输出但未必显式评价组合，pair scorer 联合看两个物品及次序，使一对内部互补进入一次动作。候选 pair 数可能很大，缩短步数把压力转到动作空间；来源代理质量负向，不能只报半长度宣称无损加速。 示意：相机与镜头一对可能互补，两台近似相机单条分高却重复，联合评分可区分；但所有可能二元组数量比单品多。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-36598c3f06a42d49">PSG 与普通两步并行 item 预测，相比 pair scorer 学什么依赖？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apsg">PSG: Pair-Space Generation for Efficient Generative Reranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立位置头可同时输出但未必显式评价组合，pair scorer 联合看两个物品及次序，使一对内部互补进入一次动作。候选 pair 数可能很大，缩短步数把压力转到动作空间；来源代理质量负向，不能只报半长度宣称无损加速。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>相机与镜头一对可能互补，两台近似相机单条分高却重复，联合评分可区分；但所有可能二元组数量比单品多。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26427">原论文</a> · <a href="../../../../reproductions/2607.26427-psg/">实现解读</a> · <a href="#qa-36598c3f06a42d49">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:psg" data-paper-title="PSG: Pair-Space Generation for Efficient Generative Reranking" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="PSG: Pair-Space Generation for Efficient Generative Reranking 搜广推与 LLM 应用 Kuaishou Technology 2026-07-29 把相邻两个 item 编成一个请求内 pair token，在 pair 空间生成半长度序列，再无损展开为 item slate；pair scorer 显式保留顺序，重复约束保证展开结果可用。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为六步 item-space 生成，实验组为三步 pair-space 生成与展开；seed 42 的 NDCG@10 为 0.04826，基线为 0.05401，负结果保留。  reranking generative-recommendation pair-token serving 搜广推 重排、展示与长期价值 PSG 展开后为什么还要跨 pair 去重，而不只保证每个 pair 内不同？ 同一物品可出现在不同 pair，局部不重复不保证整页合法，选新 pair 时需考虑已选前缀。映射要保留 pair 内顺序，不能排序成 ID 升序。长度、余项与空合法集合需显式处理，不用重复填满掩盖失败。 示意：第一对相机镜头，第二对相机包，内部都不同却重复相机；展开前后都应检查全列表约束，而不是只看两两组合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e93e622c0c622dc8">PSG 展开后为什么还要跨 pair 去重，而不只保证每个 pair 内不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apsg">PSG: Pair-Space Generation for Efficient Generative Reranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一物品可出现在不同 pair，局部不重复不保证整页合法，选新 pair 时需考虑已选前缀。映射要保留 pair 内顺序，不能排序成 ID 升序。长度、余项与空合法集合需显式处理，不用重复填满掩盖失败。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第一对相机镜头，第二对相机包，内部都不同却重复相机；展开前后都应检查全列表约束，而不是只看两两组合。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26427">原论文</a> · <a href="../../../../reproductions/2607.26427-psg/">实现解读</a> · <a href="#qa-e93e622c0c622dc8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:swag-bid" data-paper-title="Beyond Single-Episode Optimization: Sliding-Window Aware Generative Auto-Bidding for Long-Term Advertising Effectiveness" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Beyond Single-Episode Optimization: Sliding-Window Aware Generative Auto-Bidding for Long-Term Advertising Effectiveness 搜广推与 LLM 应用 Alibaba International Digital Commerce / Dalian University of Technology 2026-07-28 用 masked future plan 建模跨 episode 的七日滑窗目标，并以 per-step gate 将长期 guidance 注入当前 bid 决策。 Fidelity: 核心机制复现。本地执行论文的窗口感知出价目标与约束代理，不把公开离线实验写成生产广告系统。不是生产 Decision Transformer checkpoint，且公开数据没有 bid、budget、GMV，结果仅是结构消融。本地对照口径：基线为 single-episode Decision Transformer proxy，实验组为 sliding-window planner；同一小数据候选排序下 Hit@10 与 NDCG@10 均为 +0.00%。  advertising generative-model decision-transformer long-horizon 搜广推 重排、展示与长期价值 SWAG为什么看跨episode七日滑窗而不只单次出价？ 广告目标常在滑动周期内结算，单步或单episode最优可能破坏窗口累计目标。masked future plan提供长期条件，再由当前state gate调节其对bid的作用。 例如今天节省过多预算可能错过窗口内机会，单日局部最优不等于七日最优。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-swag-bid-1ae52cbb" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e8e31735a2ad749a">SWAG为什么看跨episode七日滑窗而不只单次出价？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aswag-bid">Beyond Single-Episode Optimization: Sliding-Window Aware Generative Auto-Bidding for Long-Term Advertising Effectiveness</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce / Dalian University of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>广告目标常在滑动周期内结算，单步或单episode最优可能破坏窗口累计目标。masked future plan提供长期条件，再由当前state gate调节其对bid的作用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如今天节省过多预算可能错过窗口内机会，单日局部最优不等于七日最优。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25233">原论文</a> · <a href="../../../../reproductions/2607.25233-swag-bid/">实现解读</a> · <a href="#qa-e8e31735a2ad749a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:swag-bid" data-paper-title="Beyond Single-Episode Optimization: Sliding-Window Aware Generative Auto-Bidding for Long-Term Advertising Effectiveness" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Beyond Single-Episode Optimization: Sliding-Window Aware Generative Auto-Bidding for Long-Term Advertising Effectiveness 搜广推与 LLM 应用 Alibaba International Digital Commerce / Dalian University of Technology 2026-07-28 用 masked future plan 建模跨 episode 的七日滑窗目标，并以 per-step gate 将长期 guidance 注入当前 bid 决策。 Fidelity: 核心机制复现。本地执行论文的窗口感知出价目标与约束代理，不把公开离线实验写成生产广告系统。不是生产 Decision Transformer checkpoint，且公开数据没有 bid、budget、GMV，结果仅是结构消融。本地对照口径：基线为 single-episode Decision Transformer proxy，实验组为 sliding-window planner；同一小数据候选排序下 Hit@10 与 NDCG@10 均为 +0.00%。  advertising generative-model decision-transformer long-horizon 搜广推 重排、展示与长期价值 SWAG-Bid 为什么用跨 episode 的七日滑窗计划，还要逐步 gate 注入当前出价？ 单个 episode 的局部奖励可能忽视跨天预算与收益。滑窗状态承载更长目标，逐步 gate 再决定当前决策需要多少长期指导，避免固定强度压过即时市场信号。训练中的 masked future plan 提供监督，不意味着执行时可读取真实未来；本地小规模零变化也不能被解释成长期竞价收益已验证。 示意：今天竞争激烈但本周后面仍有机会，长期计划可能建议保留预算；当前遇到高价值请求时 gate 又允许即时信号更强。真实出价仍只能依据当时可得信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:swag-bid" data-paper-title="Beyond Single-Episode Optimization: Sliding-Window Aware Generative Auto-Bidding for Long-Term Advertising Effectiveness" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Beyond Single-Episode Optimization: Sliding-Window Aware Generative Auto-Bidding for Long-Term Advertising Effectiveness 搜广推与 LLM 应用 Alibaba International Digital Commerce / Dalian University of Technology 2026-07-28 用 masked future plan 建模跨 episode 的七日滑窗目标，并以 per-step gate 将长期 guidance 注入当前 bid 决策。 Fidelity: 核心机制复现。本地执行论文的窗口感知出价目标与约束代理，不把公开离线实验写成生产广告系统。不是生产 Decision Transformer checkpoint，且公开数据没有 bid、budget、GMV，结果仅是结构消融。本地对照口径：基线为 single-episode Decision Transformer proxy，实验组为 sliding-window planner；同一小数据候选排序下 Hit@10 与 NDCG@10 均为 +0.00%。  advertising generative-model decision-transformer long-horizon 搜广推 重排、展示与长期价值 每步gate与把同一长期计划强行喂给所有状态有什么差别？ gate允许当前市场和预算状态决定长期guidance使用程度，固定注入不作条件区分。长期计划仍是估计，不可把未来真实GMV或成本直接送进当前决策。 例如临近窗口末尾与刚开始时，对同一预算计划的依赖可不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-6f09b12303391e18">每步gate与把同一长期计划强行喂给所有状态有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aswag-bid">Beyond Single-Episode Optimization: Sliding-Window Aware Generative Auto-Bidding for Long-Term Advertising Effectiveness</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce / Dalian University of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>gate允许当前市场和预算状态决定长期guidance使用程度，固定注入不作条件区分。长期计划仍是估计，不可把未来真实GMV或成本直接送进当前决策。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如临近窗口末尾与刚开始时，对同一预算计划的依赖可不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25233">原论文</a> · <a href="../../../../reproductions/2607.25233-swag-bid/">实现解读</a> · <a href="#qa-6f09b12303391e18">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:swag-bid" data-paper-title="Beyond Single-Episode Optimization: Sliding-Window Aware Generative Auto-Bidding for Long-Term Advertising Effectiveness" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Beyond Single-Episode Optimization: Sliding-Window Aware Generative Auto-Bidding for Long-Term Advertising Effectiveness 搜广推与 LLM 应用 Alibaba International Digital Commerce / Dalian University of Technology 2026-07-28 用 masked future plan 建模跨 episode 的七日滑窗目标，并以 per-step gate 将长期 guidance 注入当前 bid 决策。 Fidelity: 核心机制复现。本地执行论文的窗口感知出价目标与约束代理，不把公开离线实验写成生产广告系统。不是生产 Decision Transformer checkpoint，且公开数据没有 bid、budget、GMV，结果仅是结构消融。本地对照口径：基线为 single-episode Decision Transformer proxy，实验组为 sliding-window planner；同一小数据候选排序下 Hit@10 与 NDCG@10 均为 +0.00%。  advertising generative-model decision-transformer long-horizon 搜广推 重排、展示与长期价值 SWAG本地公开数据是否有真实bid、budget和GMV？ 没有，当前是结构消融，非生产Decision Transformer检查点。计划mask和状态时间要严格因果，不能由未来观察补齐计划后再报告真实自动出价收益。 例如电影行为上的一个动作分数，不代表广告竞价价格。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-73cfdb7c6e857295">SWAG本地公开数据是否有真实bid、budget和GMV？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aswag-bid">Beyond Single-Episode Optimization: Sliding-Window Aware Generative Auto-Bidding for Long-Term Advertising Effectiveness</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce / Dalian University of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有，当前是结构消融，非生产Decision Transformer检查点。计划mask和状态时间要严格因果，不能由未来观察补齐计划后再报告真实自动出价收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如电影行为上的一个动作分数，不代表广告竞价价格。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25233">原论文</a> · <a href="../../../../reproductions/2607.25233-swag-bid/">实现解读</a> · <a href="#qa-73cfdb7c6e857295">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:youtube-freshness" data-paper-title="Breaking the Loop: An Empirical Comparison of Strategies for Novelty and Freshness in YouTube Music" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Breaking the Loop: An Empirical Comparison of Strategies for Novelty and Freshness in YouTube Music 搜广推与 LLM 应用 YouTube Music / Google 2026-07-26 系统比较 recency feature、IPS、可移除 bias tower 与 SNGP 不确定性探索，区分训练去偏和 serving 探索。 Fidelity: 核心机制复现。本地执行新鲜度感知的候选打分与公平对照；不复刻 YouTube 私有流量系统。没有 YouTube 连续训练基础设施和 SNGP 大模型；本地负结果不推翻论文各干预的在线结论。本地对照口径：基线为 popularity-biased continuous ranker，实验组为四机制组合；Hit@10 +0.00%、NDCG@10 -6.35%，head share -28.72%。  ranking feedback-loop freshness exploration 搜广推 重排、展示与长期价值 新鲜度研究为什么把训练去偏与serving探索分开？ 日志受既有曝光影响，新内容数据少；IPS或bias tower改训练信号，不确定性探索则改变实际曝光。两者干预位置不同，不能只靠加入发布时间消除反馈环。 例如旧歌更常被展示导致数据更多，新歌需获得真实尝试机会。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-youtube-freshness-c4f4face" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9d94c36948fa946f">新鲜度研究为什么把训练去偏与serving探索分开？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ayoutube-freshness">Breaking the Loop: An Empirical Comparison of Strategies for Novelty and Freshness in YouTube Music</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · YouTube Music / Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>日志受既有曝光影响，新内容数据少；IPS或bias tower改训练信号，不确定性探索则改变实际曝光。两者干预位置不同，不能只靠加入发布时间消除反馈环。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如旧歌更常被展示导致数据更多，新歌需获得真实尝试机会。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.23749">原论文</a> · <a href="../../../../reproductions/2607.23749-youtube-freshness/">实现解读</a> · <a href="#qa-9d94c36948fa946f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:youtube-freshness" data-paper-title="Breaking the Loop: An Empirical Comparison of Strategies for Novelty and Freshness in YouTube Music" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Breaking the Loop: An Empirical Comparison of Strategies for Novelty and Freshness in YouTube Music 搜广推与 LLM 应用 YouTube Music / Google 2026-07-26 系统比较 recency feature、IPS、可移除 bias tower 与 SNGP 不确定性探索，区分训练去偏和 serving 探索。 Fidelity: 核心机制复现。本地执行新鲜度感知的候选打分与公平对照；不复刻 YouTube 私有流量系统。没有 YouTube 连续训练基础设施和 SNGP 大模型；本地负结果不推翻论文各干预的在线结论。本地对照口径：基线为 popularity-biased continuous ranker，实验组为四机制组合；Hit@10 +0.00%、NDCG@10 -6.35%，head share -28.72%。  ranking feedback-loop freshness exploration 搜广推 重排、展示与长期价值 YouTube Freshness 为什么区分训练去偏与 serving 探索，而不把新鲜度特征当作完整解决方案？ 新鲜度特征告诉模型内容年龄，却不自动改变旧曝光造成的标签偏差。IPS 与可移除偏置塔在训练端处理数据选择，SNGP 不确定性奖励在服务端为未知内容分配探索，两者作用阶段不同。探索收集新反馈，去偏改善已有反馈利用；都依赖校准与假设，不能只因头部占比下降就认定用户满意度提高。 示意：新视频没有点击不一定质量差，可能从未曝光。训练端校正旧曝光偏差，服务端给高不确定候选少量机会，再根据真实反馈更新，而非仅给所有新视频固定加分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:youtube-freshness" data-paper-title="Breaking the Loop: An Empirical Comparison of Strategies for Novelty and Freshness in YouTube Music" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Breaking the Loop: An Empirical Comparison of Strategies for Novelty and Freshness in YouTube Music 搜广推与 LLM 应用 YouTube Music / Google 2026-07-26 系统比较 recency feature、IPS、可移除 bias tower 与 SNGP 不确定性探索，区分训练去偏和 serving 探索。 Fidelity: 核心机制复现。本地执行新鲜度感知的候选打分与公平对照；不复刻 YouTube 私有流量系统。没有 YouTube 连续训练基础设施和 SNGP 大模型；本地负结果不推翻论文各干预的在线结论。本地对照口径：基线为 popularity-biased continuous ranker，实验组为四机制组合；Hit@10 +0.00%、NDCG@10 -6.35%，head share -28.72%。  ranking feedback-loop freshness exploration 搜广推 重排、展示与长期价值 可移除bias tower与推理保留recency特征有什么区别？ bias tower可吸收训练曝光偏差后移除，recency仍直接影响服务分。移除与保留改变目标，不能把训练偏差模型当作线上质量因素继续叠分。 例如学习日志里旧内容优势，不代表部署应再次奖励旧内容。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-746a342e1a577d0e">可移除bias tower与推理保留recency特征有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ayoutube-freshness">Breaking the Loop: An Empirical Comparison of Strategies for Novelty and Freshness in YouTube Music</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · YouTube Music / Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>bias tower可吸收训练曝光偏差后移除，recency仍直接影响服务分。移除与保留改变目标，不能把训练偏差模型当作线上质量因素继续叠分。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学习日志里旧内容优势，不代表部署应再次奖励旧内容。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.23749">原论文</a> · <a href="../../../../reproductions/2607.23749-youtube-freshness/">实现解读</a> · <a href="#qa-746a342e1a577d0e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:youtube-freshness" data-paper-title="Breaking the Loop: An Empirical Comparison of Strategies for Novelty and Freshness in YouTube Music" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Breaking the Loop: An Empirical Comparison of Strategies for Novelty and Freshness in YouTube Music 搜广推与 LLM 应用 YouTube Music / Google 2026-07-26 系统比较 recency feature、IPS、可移除 bias tower 与 SNGP 不确定性探索，区分训练去偏和 serving 探索。 Fidelity: 核心机制复现。本地执行新鲜度感知的候选打分与公平对照；不复刻 YouTube 私有流量系统。没有 YouTube 连续训练基础设施和 SNGP 大模型；本地负结果不推翻论文各干预的在线结论。本地对照口径：基线为 popularity-biased continuous ranker，实验组为四机制组合；Hit@10 +0.00%、NDCG@10 -6.35%，head share -28.72%。  ranking feedback-loop freshness exploration 搜广推 重排、展示与长期价值 本地SNGP代理或负结果能解释原YouTube在线试验吗？ 不能，当前没有连续训练基础设施和真实SNGP大模型。需分别报告干预、日志倾向与探索预算，IPS概率必须有来源，不能用物品流行度随意代替真实propensity。 例如低流行并不等于当时被展示的概率低，两者统计对象不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1479c82e1a934ed5">本地SNGP代理或负结果能解释原YouTube在线试验吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ayoutube-freshness">Breaking the Loop: An Empirical Comparison of Strategies for Novelty and Freshness in YouTube Music</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · YouTube Music / Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，当前没有连续训练基础设施和真实SNGP大模型。需分别报告干预、日志倾向与探索预算，IPS概率必须有来源，不能用物品流行度随意代替真实propensity。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如低流行并不等于当时被展示的概率低，两者统计对象不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.23749">原论文</a> · <a href="../../../../reproductions/2607.23749-youtube-freshness/">实现解读</a> · <a href="#qa-1479c82e1a934ed5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pindco" data-paper-title="PinDCO: Whole-Page Aware Dynamic Creative Optimization at Scale" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="PinDCO: Whole-Page Aware Dynamic Creative Optimization at Scale 搜广推与 LLM 应用 Pinterest 2026-07-21 生成式创意使每个广告的候选图像、标题与版式迅速增多。PinDCO 用组件专属 tower 分别编码异构创意，再预测相对基础广告排序 logit 的增量；PAM 根据相对长宽比惩罚过度占用瀑布流像素的创意，前置轻量筛选、缓存和动态 batching 控制线上成本，ε-greedy 流量为新创意收集较少偏的反馈。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行组件专塔、基于广告分数的增量融合、像素惩罚公式与候选筛选；不把 MovieLens 内容特征冒充 Pinterest 创意或生产流量。未复刻 Pinterest 私有创意、用户/上下文特征、广告基线、在线 bandit 流量、缓存与服务集群。本实现不声明 CUDA 路径，也未接入 evolve，因为当前统一 evaluator 尚不能执行完整创意候选协议。MovieLens 100K、seeds 42/43/44 的固定公开口径见 metrics/movielens-100k-seeds42-44.json。  advertising creative-optimization whole-page-optimization multi-tower 搜广推 重排、展示与长期价值 PinDCO 为什么为图像、标题、版式使用组件专属 tower？ 创意各组件模态与统计不同，独立编码后再学习其对基础广告的增量，便于比较同一广告不同组合。全混合容易丢角色差别，但组件塔也需交互才能表达搭配。增量是预测分变化，不自动等于随机实验测得的创意因果收益。 示意：同一商品换标题与换长图影响不同，专属塔让模型知道改的是哪部分；图片漂亮也可能配错文案，需要组合判断。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-pindco-94511583" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b6d3443f9095014d">PinDCO 为什么为图像、标题、版式使用组件专属 tower？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apindco">PinDCO: Whole-Page Aware Dynamic Creative Optimization at Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>创意各组件模态与统计不同，独立编码后再学习其对基础广告的增量，便于比较同一广告不同组合。全混合容易丢角色差别，但组件塔也需交互才能表达搭配。增量是预测分变化，不自动等于随机实验测得的创意因果收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一商品换标题与换长图影响不同，专属塔让模型知道改的是哪部分；图片漂亮也可能配错文案，需要组合判断。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11943">原论文</a> · <a href="../../../../reproductions/2609.11943-pindco/">实现解读</a> · <a href="#qa-b6d3443f9095014d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pindco" data-paper-title="PinDCO: Whole-Page Aware Dynamic Creative Optimization at Scale" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="PinDCO: Whole-Page Aware Dynamic Creative Optimization at Scale 搜广推与 LLM 应用 Pinterest 2026-07-21 生成式创意使每个广告的候选图像、标题与版式迅速增多。PinDCO 用组件专属 tower 分别编码异构创意，再预测相对基础广告排序 logit 的增量；PAM 根据相对长宽比惩罚过度占用瀑布流像素的创意，前置轻量筛选、缓存和动态 batching 控制线上成本，ε-greedy 流量为新创意收集较少偏的反馈。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行组件专塔、基于广告分数的增量融合、像素惩罚公式与候选筛选；不把 MovieLens 内容特征冒充 Pinterest 创意或生产流量。未复刻 Pinterest 私有创意、用户/上下文特征、广告基线、在线 bandit 流量、缓存与服务集群。本实现不声明 CUDA 路径，也未接入 evolve，因为当前统一 evaluator 尚不能执行完整创意候选协议。MovieLens 100K、seeds 42/43/44 的固定公开口径见 metrics/movielens-100k-seeds42-44.json。  advertising creative-optimization whole-page-optimization multi-tower 搜广推 重排、展示与长期价值 PinDCO 为什么预测创意相对基础广告的增量，并额外惩罚长宽比带来的像素占用？ 基础广告分数包含商品和用户匹配信息，增量预测把学习重点放在图片、标题与版式改变了多少价值。较高创意还会占用更多瀑布流空间，像素调整乘子让收益与空间代价共同决定选择。探索流量为新创意补反馈；本地无真实像素实验，不能把代理特征结果解释为布局因果收益。 示意：同一广告有方图和长图，长图点击可能更高，却挤掉其他内容。只有增加的价值足以抵消像素惩罚时才选长图，而不是见到更高点击预测就直接占用更多版面。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pindco" data-paper-title="PinDCO: Whole-Page Aware Dynamic Creative Optimization at Scale" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="PinDCO: Whole-Page Aware Dynamic Creative Optimization at Scale 搜广推与 LLM 应用 Pinterest 2026-07-21 生成式创意使每个广告的候选图像、标题与版式迅速增多。PinDCO 用组件专属 tower 分别编码异构创意，再预测相对基础广告排序 logit 的增量；PAM 根据相对长宽比惩罚过度占用瀑布流像素的创意，前置轻量筛选、缓存和动态 batching 控制线上成本，ε-greedy 流量为新创意收集较少偏的反馈。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行组件专塔、基于广告分数的增量融合、像素惩罚公式与候选筛选；不把 MovieLens 内容特征冒充 Pinterest 创意或生产流量。未复刻 Pinterest 私有创意、用户/上下文特征、广告基线、在线 bandit 流量、缓存与服务集群。本实现不声明 CUDA 路径，也未接入 evolve，因为当前统一 evaluator 尚不能执行完整创意候选协议。MovieLens 100K、seeds 42/43/44 的固定公开口径见 metrics/movielens-100k-seeds42-44.json。  advertising creative-optimization whole-page-optimization multi-tower 搜广推 重排、展示与长期价值 PinDCO 的 ε-greedy 与只给历史最优创意流量，相比对新品反馈有什么作用？ 贪心持续曝光旧赢家，新创意缺机会便难估；少量随机探索提供较少选择偏差的反馈，再训练组件价值。探索也有成本且不消除全部混杂，像素调整另管页面占用，不应把两者合并成一个收益保证。 示意：新标题暂没点击并不代表差，分一点探索流量才有证据；但不能为了探索把明显误导创意强推，目录与事实约束仍需保留。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7ae9e5ad97be3805">PinDCO 的 ε-greedy 与只给历史最优创意流量，相比对新品反馈有什么作用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apindco">PinDCO: Whole-Page Aware Dynamic Creative Optimization at Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>贪心持续曝光旧赢家，新创意缺机会便难估；少量随机探索提供较少选择偏差的反馈，再训练组件价值。探索也有成本且不消除全部混杂，像素调整另管页面占用，不应把两者合并成一个收益保证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新标题暂没点击并不代表差，分一点探索流量才有证据；但不能为了探索把明显误导创意强推，目录与事实约束仍需保留。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11943">原论文</a> · <a href="../../../../reproductions/2609.11943-pindco/">实现解读</a> · <a href="#qa-7ae9e5ad97be3805">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pindco" data-paper-title="PinDCO: Whole-Page Aware Dynamic Creative Optimization at Scale" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="PinDCO: Whole-Page Aware Dynamic Creative Optimization at Scale 搜广推与 LLM 应用 Pinterest 2026-07-21 生成式创意使每个广告的候选图像、标题与版式迅速增多。PinDCO 用组件专属 tower 分别编码异构创意，再预测相对基础广告排序 logit 的增量；PAM 根据相对长宽比惩罚过度占用瀑布流像素的创意，前置轻量筛选、缓存和动态 batching 控制线上成本，ε-greedy 流量为新创意收集较少偏的反馈。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行组件专塔、基于广告分数的增量融合、像素惩罚公式与候选筛选；不把 MovieLens 内容特征冒充 Pinterest 创意或生产流量。未复刻 Pinterest 私有创意、用户/上下文特征、广告基线、在线 bandit 流量、缓存与服务集群。本实现不声明 CUDA 路径，也未接入 evolve，因为当前统一 evaluator 尚不能执行完整创意候选协议。MovieLens 100K、seeds 42/43/44 的固定公开口径见 metrics/movielens-100k-seeds42-44.json。  advertising creative-optimization whole-page-optimization multi-tower 搜广推 重排、展示与长期价值 PAM 的 clip 与相对长宽比 r，为什么需要精确保持？ P(r)=clip(1−tanh(k(r−1)),0,1) 使过高创意受惩罚并保持合法范围，乘在对应原目标 O 上。换成长宽比倒数或去掉 clip 会改变边界。本地 content norm 只是无像素替代，不能从该代理结果宣称真实版式效率。 示意：若 r 定义高宽比，误用宽高比就会惩罚宽图而非高图；公式都能算出有限数，却正好反转了屏幕空间代价方向。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-21c31e3b63c31f20">PAM 的 clip 与相对长宽比 r，为什么需要精确保持？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apindco">PinDCO: Whole-Page Aware Dynamic Creative Optimization at Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>P(r)=clip(1−tanh(k(r−1)),0,1) 使过高创意受惩罚并保持合法范围，乘在对应原目标 O 上。换成长宽比倒数或去掉 clip 会改变边界。本地 content norm 只是无像素替代，不能从该代理结果宣称真实版式效率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>若 r 定义高宽比，误用宽高比就会惩罚宽图而非高图；公式都能算出有限数，却正好反转了屏幕空间代价方向。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11943">原论文</a> · <a href="../../../../reproductions/2609.11943-pindco/">实现解读</a> · <a href="#qa-21c31e3b63c31f20">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:uame" data-paper-title="Uncertainty as Remedy: Mitigating Satisfaction Label Bias in Short Video Multi-Objective Ensemble Ranking" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Uncertainty as Remedy: Mitigating Satisfaction Label Bias in Short Video Multi-Objective Ensemble Ranking 搜广推与 LLM 应用 Kuaishou Technology 2026-07-19 点击、观看、点赞等 pxtr 只是不可观测“真实满意度”的冲突代理。UAME 在 EMER/EASQ 主干上增加共享表征的均值与方差双头，把分数视作 Gaussian 变量；用解析 pair probability 联合各 pxtr，令冲突更高的 pair 获得更大训练权重。线上只使用均值打分，因此不增加 serving 路径。 Fidelity: 核心机制复现。训练 Gaussian score 双头、概率 pairwise loss、冲突约束与不确定性加权；私有八路 pxtr 和生产 backbone 用公开 proxy 替代。未获得快手八路 pxtr、EMER/EASQ、问卷满意度和亿级流量；本地负结果说明这一公开 proxy 映射不能直接复现论文收益，不与线上 lift 混写。本地对照口径：基线是同 backbone 的 deterministic multi-objective pairwise ranker；实验组加入完整 UAME loss，NDCG@10 相对 -62.28%。  multi-objective-ranking uncertainty loss-design 搜广推 重排、展示与长期价值 UAME为什么同时预测均值与方差？ 多个pxtr是潜在满意度的冲突代理，方差描述预测不确定性，解析高斯pair概率联合学习。线上只用均值，因此训练不确定性建模与服务打分分开。 例如点击高但观看低的候选，其相对偏好可能比信号一致者更不确定。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-uame-b8cd46d0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-cbd00bc0c8913daa">UAME为什么同时预测均值与方差？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Auame">Uncertainty as Remedy: Mitigating Satisfaction Label Bias in Short Video Multi-Objective Ensemble Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多个pxtr是潜在满意度的冲突代理，方差描述预测不确定性，解析高斯pair概率联合学习。线上只用均值，因此训练不确定性建模与服务打分分开。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如点击高但观看低的候选，其相对偏好可能比信号一致者更不确定。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.17092">原论文</a> · <a href="../../../../reproductions/2607.17092-uame/">实现解读</a> · <a href="#qa-cbd00bc0c8913daa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:uame" data-paper-title="Uncertainty as Remedy: Mitigating Satisfaction Label Bias in Short Video Multi-Objective Ensemble Ranking" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Uncertainty as Remedy: Mitigating Satisfaction Label Bias in Short Video Multi-Objective Ensemble Ranking 搜广推与 LLM 应用 Kuaishou Technology 2026-07-19 点击、观看、点赞等 pxtr 只是不可观测“真实满意度”的冲突代理。UAME 在 EMER/EASQ 主干上增加共享表征的均值与方差双头，把分数视作 Gaussian 变量；用解析 pair probability 联合各 pxtr，令冲突更高的 pair 获得更大训练权重。线上只使用均值打分，因此不增加 serving 路径。 Fidelity: 核心机制复现。训练 Gaussian score 双头、概率 pairwise loss、冲突约束与不确定性加权；私有八路 pxtr 和生产 backbone 用公开 proxy 替代。未获得快手八路 pxtr、EMER/EASQ、问卷满意度和亿级流量；本地负结果说明这一公开 proxy 映射不能直接复现论文收益，不与线上 lift 混写。本地对照口径：基线是同 backbone 的 deterministic multi-objective pairwise ranker；实验组加入完整 UAME loss，NDCG@10 相对 -62.28%。  multi-objective-ranking uncertainty loss-design 搜广推 重排、展示与长期价值 UAME 为什么为排序分数学习均值和方差，训练时重点处理高冲突 pair，却线上只用均值？ 多个 pxtr 是满意度的冲突代理，确定性分数难表达其分歧。均值—方差双头把得分建成高斯变量，用解析胜出概率进行 pairwise 学习，再提高高不确定 pair 的权重并约束方差。方差在训练中组织困难关系，服务只读取均值以保持路径成本；它表示模型化的不确定性，不是已观测到的真实满意度方差。 示意：两个视频一个更易点击、一个更可能长看，模型对胜负不确定。训练重点处理这类冲突，并约束随意抬高方差；上线仍输出一个均值分数参与排序。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:uame" data-paper-title="Uncertainty as Remedy: Mitigating Satisfaction Label Bias in Short Video Multi-Objective Ensemble Ranking" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Uncertainty as Remedy: Mitigating Satisfaction Label Bias in Short Video Multi-Objective Ensemble Ranking 搜广推与 LLM 应用 Kuaishou Technology 2026-07-19 点击、观看、点赞等 pxtr 只是不可观测“真实满意度”的冲突代理。UAME 在 EMER/EASQ 主干上增加共享表征的均值与方差双头，把分数视作 Gaussian 变量；用解析 pair probability 联合各 pxtr，令冲突更高的 pair 获得更大训练权重。线上只使用均值打分，因此不增加 serving 路径。 Fidelity: 核心机制复现。训练 Gaussian score 双头、概率 pairwise loss、冲突约束与不确定性加权；私有八路 pxtr 和生产 backbone 用公开 proxy 替代。未获得快手八路 pxtr、EMER/EASQ、问卷满意度和亿级流量；本地负结果说明这一公开 proxy 映射不能直接复现论文收益，不与线上 lift 混写。本地对照口径：基线是同 backbone 的 deterministic multi-objective pairwise ranker；实验组加入完整 UAME loss，NDCG@10 相对 -62.28%。  multi-objective-ranking uncertainty loss-design 搜广推 重排、展示与长期价值 不确定性加权与直接平均各pxtr有什么不同？ 前者让高冲突pair获得更多训练关注，并建模比较概率；平均只固定合成代理。方差不是问卷真满意度，不能由高权重证明已解决所有目标冲突。 例如两个候选各擅长不同指标，不该把冲突隐藏成一个无解释平均数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-8588c89858fb0a5d">不确定性加权与直接平均各pxtr有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Auame">Uncertainty as Remedy: Mitigating Satisfaction Label Bias in Short Video Multi-Objective Ensemble Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者让高冲突pair获得更多训练关注，并建模比较概率；平均只固定合成代理。方差不是问卷真满意度，不能由高权重证明已解决所有目标冲突。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个候选各擅长不同指标，不该把冲突隐藏成一个无解释平均数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.17092">原论文</a> · <a href="../../../../reproductions/2607.17092-uame/">实现解读</a> · <a href="#qa-8588c89858fb0a5d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:uame" data-paper-title="Uncertainty as Remedy: Mitigating Satisfaction Label Bias in Short Video Multi-Objective Ensemble Ranking" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Uncertainty as Remedy: Mitigating Satisfaction Label Bias in Short Video Multi-Objective Ensemble Ranking 搜广推与 LLM 应用 Kuaishou Technology 2026-07-19 点击、观看、点赞等 pxtr 只是不可观测“真实满意度”的冲突代理。UAME 在 EMER/EASQ 主干上增加共享表征的均值与方差双头，把分数视作 Gaussian 变量；用解析 pair probability 联合各 pxtr，令冲突更高的 pair 获得更大训练权重。线上只使用均值打分，因此不增加 serving 路径。 Fidelity: 核心机制复现。训练 Gaussian score 双头、概率 pairwise loss、冲突约束与不确定性加权；私有八路 pxtr 和生产 backbone 用公开 proxy 替代。未获得快手八路 pxtr、EMER/EASQ、问卷满意度和亿级流量；本地负结果说明这一公开 proxy 映射不能直接复现论文收益，不与线上 lift 混写。本地对照口径：基线是同 backbone 的 deterministic multi-objective pairwise ranker；实验组加入完整 UAME loss，NDCG@10 相对 -62.28%。  multi-objective-ranking uncertainty loss-design 搜广推 重排、展示与长期价值 UAME线上是否必须采Gaussian噪声，既有负结果怎样解释？ 线上只读均值，不需训练用噪声或方差路径。当前公开proxy负结果说明映射未复现原收益，不应删除或外推否定原私有实验；方差和权重零范围边界要明示。 例如所有pair不确定性相同，min-max分母为零需合法处理，而非制造NaN。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d7048180b0074ee9">UAME线上是否必须采Gaussian噪声，既有负结果怎样解释？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Auame">Uncertainty as Remedy: Mitigating Satisfaction Label Bias in Short Video Multi-Objective Ensemble Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>线上只读均值，不需训练用噪声或方差路径。当前公开proxy负结果说明映射未复现原收益，不应删除或外推否定原私有实验；方差和权重零范围边界要明示。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如所有pair不确定性相同，min-max分母为零需合法处理，而非制造NaN。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.17092">原论文</a> · <a href="../../../../reproductions/2607.17092-uame/">实现解读</a> · <a href="#qa-d7048180b0074ee9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:real-estate-rerank" data-paper-title="LLM-Based Re-Ranking for Real Estate Search" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="LLM-Based Re-Ranking for Real Estate Search 搜广推与 LLM 应用 QuintoAndar 2026-07-16 把对话需求、结构化房源属性、文本描述和候选集合统计交给 LLM 重排，用候选间比较补足向量召回的局部相关性。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  search-ranking llm-reranking content-understanding 搜广推 重排、展示与长期价值 房产重排为什么要结合结构化属性与对话需求，而不只读文本描述？ 宣传文字可能含糊，价格、面积、通勤等字段提供明确约束，对话又包含用户逐步表达的取舍。联合读取使模型可比较多条件满足度，候选集统计补相对环境。语言理解不能替代真实属性校验，也不能凭生成理由改写事实。 示意：房源都写交通便利，一套到地铁二十分钟、另一套五分钟，用户要求十分钟内时应依据结构字段，而不是谁描述更吸引人。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-real-estate-rerank-2009ea9f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d6adce1daee6cd20">房产重排为什么要结合结构化属性与对话需求，而不只读文本描述？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Areal-estate-rerank">LLM-Based Re-Ranking for Real Estate Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · QuintoAndar</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>宣传文字可能含糊，价格、面积、通勤等字段提供明确约束，对话又包含用户逐步表达的取舍。联合读取使模型可比较多条件满足度，候选集统计补相对环境。语言理解不能替代真实属性校验，也不能凭生成理由改写事实。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>房源都写交通便利，一套到地铁二十分钟、另一套五分钟，用户要求十分钟内时应依据结构字段，而不是谁描述更吸引人。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14835">原论文</a> · <a href="../../../../reproductions/2607.14835-real-estate-rerank/">实现解读</a> · <a href="#qa-d6adce1daee6cd20">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:real-estate-rerank" data-paper-title="LLM-Based Re-Ranking for Real Estate Search" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="LLM-Based Re-Ranking for Real Estate Search 搜广推与 LLM 应用 QuintoAndar 2026-07-16 把对话需求、结构化房源属性、文本描述和候选集合统计交给 LLM 重排，用候选间比较补足向量召回的局部相关性。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  search-ranking llm-reranking content-understanding 搜广推 重排、展示与长期价值 房产 LLM 重排为什么要读取候选集合统计，而不只独立比较查询与每套房源？ 对话需求可能包含预算、通勤和空间等互相制约条件，房源描述与结构化字段也需要共同解释。候选集合统计提供当前可选范围，使模型进行相对取舍，补足向量相似度的局部匹配。列表变化会改变比较背景，所以分数未必可跨集合直接复用；重排也不能补回召回阶段漏掉的房源。 示意：用户想要地铁近且安静，候选都难两者兼得。读取整组后可说明哪套在通勤与噪声之间更平衡，而不是把每套宣传文本单独与查询做相似度比较。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:real-estate-rerank" data-paper-title="LLM-Based Re-Ranking for Real Estate Search" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="LLM-Based Re-Ranking for Real Estate Search 搜广推与 LLM 应用 QuintoAndar 2026-07-16 把对话需求、结构化房源属性、文本描述和候选集合统计交给 LLM 重排，用候选间比较补足向量召回的局部相关性。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  search-ranking llm-reranking content-understanding 搜广推 重排、展示与长期价值 LLM 相对重排与向量召回，为什么缺一方不能完成另一方任务？ 召回从大库低成本选池，向量难表达复杂条件；LLM 在小池细比较但无法重排未召回房源。候选集依赖也增加成本，不能把小集合改善称全库搜索完成。来源本地电影代理缺真实对话和房产限制，只检验部分打分思路。 示意：最符合学区和通勤的房源没进前百，LLM 在其中再聪明也选不到；提高重排解释质量不能补回候选覆盖。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-69f2be7b04684526">LLM 相对重排与向量召回，为什么缺一方不能完成另一方任务？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Areal-estate-rerank">LLM-Based Re-Ranking for Real Estate Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · QuintoAndar</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>召回从大库低成本选池，向量难表达复杂条件；LLM 在小池细比较但无法重排未召回房源。候选集依赖也增加成本，不能把小集合改善称全库搜索完成。来源本地电影代理缺真实对话和房产限制，只检验部分打分思路。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>最符合学区和通勤的房源没进前百，LLM 在其中再聪明也选不到；提高重排解释质量不能补回候选覆盖。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14835">原论文</a> · <a href="../../../../reproductions/2607.14835-real-estate-rerank/">实现解读</a> · <a href="#qa-69f2be7b04684526">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:real-estate-rerank" data-paper-title="LLM-Based Re-Ranking for Real Estate Search" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="LLM-Based Re-Ranking for Real Estate Search 搜广推与 LLM 应用 QuintoAndar 2026-07-16 把对话需求、结构化房源属性、文本描述和候选集合统计交给 LLM 重排，用候选间比较补足向量召回的局部相关性。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  search-ranking llm-reranking content-understanding 搜广推 重排、展示与长期价值 房产 LLM 评分的 Agg(X) 为什么必须随着候选集变化重算？ 它代表当前列表统计，删增房源会改变相对预算与可选范围，旧聚合不再对应同一条件。结构字段与文本身份也要对齐，不能按真实成交先挑候选给模型。本地单品 scorer 与完整对话重排需按实际依赖区分。 示意：原候选全高价时某房显便宜，加入多套低价后不再如此；若继续用旧均价，模型的相对性解释就与真实列表不符。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-bd070477da15b501">房产 LLM 评分的 Agg(X) 为什么必须随着候选集变化重算？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Areal-estate-rerank">LLM-Based Re-Ranking for Real Estate Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · QuintoAndar</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它代表当前列表统计，删增房源会改变相对预算与可选范围，旧聚合不再对应同一条件。结构字段与文本身份也要对齐，不能按真实成交先挑候选给模型。本地单品 scorer 与完整对话重排需按实际依赖区分。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>原候选全高价时某房显便宜，加入多套低价后不再如此；若继续用旧均价，模型的相对性解释就与真实列表不符。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14835">原论文</a> · <a href="../../../../reproductions/2607.14835-real-estate-rerank/">实现解读</a> · <a href="#qa-bd070477da15b501">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:adaptive-ad-load" data-paper-title="Adaptive Ad Load Design for Sponsored Search Markets: Evidence, Theory, and Deployment" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Adaptive Ad Load Design for Sponsored Search Markets: Evidence, Theory, and Deployment 搜广推与 LLM 应用 University of Washington 2026-07-15 在收入与转化约束下动态决定每次搜索展示多少广告，利用随机现场实验估计供给曲线，再由轻量策略选择 ad load。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  advertising constrained-optimization marketplace 搜广推 重排、展示与长期价值 Adaptive Ad Load 优化的决策变量为什么是每次请求的广告数量，而不只是广告排序？ 排序解决给定广告位里放什么，ad load 决定给请求多少广告位，直接影响用户体验、收入和后续转化。先估计不同数量下的供给与响应，再在约束内选择数量，才能处理广告供给的边际收益，而非默认所有请求都有相同容量。 示意：强购物意图搜索可能容纳更多相关广告，探索型搜索过量广告会挤压自然结果；两次请求即使候选广告相同，合理广告数也可能不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-adaptive-ad-load-26eb54c1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2da658a8eef28309">Adaptive Ad Load 优化的决策变量为什么是每次请求的广告数量，而不只是广告排序？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aadaptive-ad-load">Adaptive Ad Load Design for Sponsored Search Markets: Evidence, Theory, and Deployment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>排序解决给定广告位里放什么，ad load 决定给请求多少广告位，直接影响用户体验、收入和后续转化。先估计不同数量下的供给与响应，再在约束内选择数量，才能处理广告供给的边际收益，而非默认所有请求都有相同容量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>强购物意图搜索可能容纳更多相关广告，探索型搜索过量广告会挤压自然结果；两次请求即使候选广告相同，合理广告数也可能不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14418">原论文</a> · <a href="../../../../reproductions/2607.14418-adaptive-ad-load/">实现解读</a> · <a href="#qa-2da658a8eef28309">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:adaptive-ad-load" data-paper-title="Adaptive Ad Load Design for Sponsored Search Markets: Evidence, Theory, and Deployment" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Adaptive Ad Load Design for Sponsored Search Markets: Evidence, Theory, and Deployment 搜广推与 LLM 应用 University of Washington 2026-07-15 在收入与转化约束下动态决定每次搜索展示多少广告，利用随机现场实验估计供给曲线，再由轻量策略选择 ad load。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  advertising constrained-optimization marketplace 搜广推 重排、展示与长期价值 为什么搜索广告数量不能始终取使当前广告收入最大的那个值？ 广告数量同时影响收入、自然结果体验和转化，最优供给随请求而变。方法先借随机现场实验估计不同广告量的响应曲线，再在业务约束下选择请求级策略；拉格朗日权重表达目标之间的取舍。不能把相关性日志直接当增加一个广告位的因果收益，本地代理排序也未验证真实市场均衡。 示意：购物意图强的查询可容纳多个广告，导航型查询多塞广告反而妨碍用户；同样增加一格，两个请求的收入与体验变化可能相反。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:adaptive-ad-load" data-paper-title="Adaptive Ad Load Design for Sponsored Search Markets: Evidence, Theory, and Deployment" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Adaptive Ad Load Design for Sponsored Search Markets: Evidence, Theory, and Deployment 搜广推与 LLM 应用 University of Washington 2026-07-15 在收入与转化约束下动态决定每次搜索展示多少广告，利用随机现场实验估计供给曲线，再由轻量策略选择 ad load。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  advertising constrained-optimization marketplace 搜广推 重排、展示与长期价值 用随机现场实验估计 ad load，和只回看既有日志中的高收入请求相比有什么识别差别？ 既有广告数量往往已由旧策略选择，收入差异可能来自用户意图而非广告数。随机变化数量更有机会区分供给变化的效果与请求本身差异。轻量策略再使用估计曲线作选择；公开排序代理没有真实供给干预，不能据其命中率推断数量的因果收益。 示意：原日志里高意图用户广告多且收入高，不能因此给所有人加广告；在相近请求中随机分配广告数，才能更接近观察增加一位的实际影响。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d8fa5c26341b14ab">用随机现场实验估计 ad load，和只回看既有日志中的高收入请求相比有什么识别差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aadaptive-ad-load">Adaptive Ad Load Design for Sponsored Search Markets: Evidence, Theory, and Deployment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>既有广告数量往往已由旧策略选择，收入差异可能来自用户意图而非广告数。随机变化数量更有机会区分供给变化的效果与请求本身差异。轻量策略再使用估计曲线作选择；公开排序代理没有真实供给干预，不能据其命中率推断数量的因果收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>原日志里高意图用户广告多且收入高，不能因此给所有人加广告；在相近请求中随机分配广告数，才能更接近观察增加一位的实际影响。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14418">原论文</a> · <a href="../../../../reproductions/2607.14418-adaptive-ad-load/">实现解读</a> · <a href="#qa-d8fa5c26341b14ab">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:adaptive-ad-load" data-paper-title="Adaptive Ad Load Design for Sponsored Search Markets: Evidence, Theory, and Deployment" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Adaptive Ad Load Design for Sponsored Search Markets: Evidence, Theory, and Deployment 搜广推与 LLM 应用 University of Washington 2026-07-15 在收入与转化约束下动态决定每次搜索展示多少广告，利用随机现场实验估计供给曲线，再由轻量策略选择 ad load。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  advertising constrained-optimization marketplace 搜广推 重排、展示与长期价值 实现 ad load 选择时，为什么必须遍历可行数量并明确收入与转化项的口径？ 选择式在各可行 k 上比较收入与加权转化，候选数量、库存和业务限制决定合法集合，系数决定目标取舍。若不同 k 的估计来自不同口径，最大值没有可比意义。本地混合权重只在验证集选择，测试不能用于调出看似更好的数量策略。 示意：只允许零到三条广告时不能输出五条；若一项用每请求收入、另一项却用每广告转化率，也应先统一定义再比较不同数量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8f2658cd2009f4e6">实现 ad load 选择时，为什么必须遍历可行数量并明确收入与转化项的口径？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aadaptive-ad-load">Adaptive Ad Load Design for Sponsored Search Markets: Evidence, Theory, and Deployment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>选择式在各可行 k 上比较收入与加权转化，候选数量、库存和业务限制决定合法集合，系数决定目标取舍。若不同 k 的估计来自不同口径，最大值没有可比意义。本地混合权重只在验证集选择，测试不能用于调出看似更好的数量策略。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>只允许零到三条广告时不能输出五条；若一项用每请求收入、另一项却用每广告转化率，也应先统一定义再比较不同数量。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14418">原论文</a> · <a href="../../../../reproductions/2607.14418-adaptive-ad-load/">实现解读</a> · <a href="#qa-8f2658cd2009f4e6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:downstream-rewards" data-paper-title="Long-term User Engagement Optimization through Model-agnostic Downstream Rewards Learning" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Long-term User Engagement Optimization through Model-agnostic Downstream Rewards Learning 搜广推与 LLM 应用 Pinterest 2026-07-15 只优化当前点击或保存可能牺牲用户后续活跃。Pinterest 的方法先离线提出并筛选能预测未来参与度的 downstream rewards，再把通过筛选的 reward head 作为模型无关附加目标接入 Homefeed、Search、Related Pins 和 Notifications 等不同系统，无需替换原有主排序器。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实执行 reward 筛选与附加头；Pinterest 私有跨 surface 长期标签未复刻。本地从 deeper transition、content depth、new use-case exploration 和 shallow closeup 四类 session 信号出发，以未来类型覆盖代理长期参与度做离线筛选，训练独立 reward head，再在 validation 上选择与即时排序分数的融合强度。  long-term-value reward-design multi-surface retention 搜广推 重排、展示与长期价值 Downstream Rewards 为什么用未来参与度筛选即时行为信号？ 即时点击或保存可能只是短暂吸引，未必对应后续活跃。筛选先找出能预测未来参与的行为，再训练可在线预测的附加头，让排序考虑更长价值。相关性只是候选证据，不证明该行为有因果促进；不同产品仍要独立验证。 示意：误触大图带来点击却很快离开，深入探索收藏可能更关联后续使用；先比较长期预测关系，再决定哪种行为值得成为附加目标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-downstream-rewards-21cba3a1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-455bebe20e3ceb57">Downstream Rewards 为什么用未来参与度筛选即时行为信号？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adownstream-rewards">Long-term User Engagement Optimization through Model-agnostic Downstream Rewards Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>即时点击或保存可能只是短暂吸引，未必对应后续活跃。筛选先找出能预测未来参与的行为，再训练可在线预测的附加头，让排序考虑更长价值。相关性只是候选证据，不证明该行为有因果促进；不同产品仍要独立验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>误触大图带来点击却很快离开，深入探索收藏可能更关联后续使用；先比较长期预测关系，再决定哪种行为值得成为附加目标。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14192">原论文</a> · <a href="../../../../reproductions/2607.14192-downstream-rewards/">实现解读</a> · <a href="#qa-455bebe20e3ceb57">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:downstream-rewards" data-paper-title="Long-term User Engagement Optimization through Model-agnostic Downstream Rewards Learning" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Long-term User Engagement Optimization through Model-agnostic Downstream Rewards Learning 搜广推与 LLM 应用 Pinterest 2026-07-15 只优化当前点击或保存可能牺牲用户后续活跃。Pinterest 的方法先离线提出并筛选能预测未来参与度的 downstream rewards，再把通过筛选的 reward head 作为模型无关附加目标接入 Homefeed、Search、Related Pins 和 Notifications 等不同系统，无需替换原有主排序器。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实执行 reward 筛选与附加头；Pinterest 私有跨 surface 长期标签未复刻。本地从 deeper transition、content depth、new use-case exploration 和 shallow closeup 四类 session 信号出发，以未来类型覆盖代理长期参与度做离线筛选，训练独立 reward head，再在 validation 上选择与即时排序分数的融合强度。  long-term-value reward-design multi-surface retention 搜广推 重排、展示与长期价值 下游reward为什么要先筛选对未来参与度的预测能力，而不是把所有即时行为都加进排序？ 即时行为和长期满意度可能相反，盲目增加目标会放大浅层互动或噪声。方法先提出多种下游信号并检验其与未来参与度的关系，只把通过筛选的reward head接入原有系统。预测关联仍不等于因果改善，因此跨产品接入后还需相应评价，不能把所有短期指标上涨相加当留存收益。 示意：一次点开大图可能只是误触，随后深入浏览相关收藏却更可能表示有价值的探索；先比较它们与未来活跃的关系，再决定哪种反馈值得成为附加目标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:downstream-rewards" data-paper-title="Long-term User Engagement Optimization through Model-agnostic Downstream Rewards Learning" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Long-term User Engagement Optimization through Model-agnostic Downstream Rewards Learning 搜广推与 LLM 应用 Pinterest 2026-07-15 只优化当前点击或保存可能牺牲用户后续活跃。Pinterest 的方法先离线提出并筛选能预测未来参与度的 downstream rewards，再把通过筛选的 reward head 作为模型无关附加目标接入 Homefeed、Search、Related Pins 和 Notifications 等不同系统，无需替换原有主排序器。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实执行 reward 筛选与附加头；Pinterest 私有跨 surface 长期标签未复刻。本地从 deeper transition、content depth、new use-case exploration 和 shallow closeup 四类 session 信号出发，以未来类型覆盖代理长期参与度做离线筛选，训练独立 reward head，再在 validation 上选择与即时排序分数的融合强度。  long-term-value reward-design multi-surface retention 搜广推 重排、展示与长期价值 附加 downstream reward head 与替换整个主排序器，接入方式有什么不同？ 附加头保留现有主干，以筛选后的长期代理预测作为额外目标或融合项，便于在多个 surface 使用。替换主模型涉及更多特征和部署变化。模型无关接入不代表标签含义通用，首页有效信号不一定适合通知，也不保证所有子指标提高。 示意：首页继续用原相关性模型，只额外预测深度消费；通知系统可以另定权重，但不能把保存和下载直接解释成通知留存。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1cf29444b410a58e">附加 downstream reward head 与替换整个主排序器，接入方式有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adownstream-rewards">Long-term User Engagement Optimization through Model-agnostic Downstream Rewards Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>附加头保留现有主干，以筛选后的长期代理预测作为额外目标或融合项，便于在多个 surface 使用。替换主模型涉及更多特征和部署变化。模型无关接入不代表标签含义通用，首页有效信号不一定适合通知，也不保证所有子指标提高。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>首页继续用原相关性模型，只额外预测深度消费；通知系统可以另定权重，但不能把保存和下载直接解释成通知留存。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14192">原论文</a> · <a href="../../../../reproductions/2607.14192-downstream-rewards/">实现解读</a> · <a href="#qa-1cf29444b410a58e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:downstream-rewards" data-paper-title="Long-term User Engagement Optimization through Model-agnostic Downstream Rewards Learning" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Long-term User Engagement Optimization through Model-agnostic Downstream Rewards Learning 搜广推与 LLM 应用 Pinterest 2026-07-15 只优化当前点击或保存可能牺牲用户后续活跃。Pinterest 的方法先离线提出并筛选能预测未来参与度的 downstream rewards，再把通过筛选的 reward head 作为模型无关附加目标接入 Homefeed、Search、Related Pins 和 Notifications 等不同系统，无需替换原有主排序器。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实执行 reward 筛选与附加头；Pinterest 私有跨 surface 长期标签未复刻。本地从 deeper transition、content depth、new use-case exploration 和 shallow closeup 四类 session 信号出发，以未来类型覆盖代理长期参与度做离线筛选，训练独立 reward head，再在 validation 上选择与即时排序分数的融合强度。  long-term-value reward-design multi-surface retention 搜广推 重排、展示与长期价值 训练 downstream reward head 时，未来窗口信息应放在哪一侧？ 未来行为可用于构造监督和筛选 reward，在线输入必须截止当前请求，不能将未来轨迹直接当特征。融合强度按验证口径选择后冻结。来源本地用未来类别覆盖代理长期参与，既不能偷读测试未来，也不能当作平台留存标签复现。 示意：用明天是否探索新主题训练今天的预测合理；上线今天若直接输入明天浏览记录，模型是在读取答案，而非预测长期参与。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c0ff2adff3a1c3c8">训练 downstream reward head 时，未来窗口信息应放在哪一侧？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adownstream-rewards">Long-term User Engagement Optimization through Model-agnostic Downstream Rewards Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>未来行为可用于构造监督和筛选 reward，在线输入必须截止当前请求，不能将未来轨迹直接当特征。融合强度按验证口径选择后冻结。来源本地用未来类别覆盖代理长期参与，既不能偷读测试未来，也不能当作平台留存标签复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用明天是否探索新主题训练今天的预测合理；上线今天若直接输入明天浏览记录，模型是在读取答案，而非预测长期参与。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14192">原论文</a> · <a href="../../../../reproductions/2607.14192-downstream-rewards/">实现解读</a> · <a href="#qa-c0ff2adff3a1c3c8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:genpage" data-paper-title="GenPage: Towards End-to-End Generative Homepage Construction at Netflix" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="GenPage: Towards End-to-End Generative Homepage Construction at Netflix 搜广推与 LLM 应用 Netflix 2026-06-30 用一个生成模型直接输出整页而非逐阶段召回排序，并在 WBC/SFT 后以生产长期奖励进行 RL 后训练，同时处理业务规则和冷启动。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation page-generation reinforcement-learning 搜广推 重排、展示与长期价值 GenPage 的整页动作为什么比逐物品预测更接近首页目标？ 首页价值取决于内容类型、布局和项目之间的组合，单品各自高分仍可组成重复或不连贯页面。整页生成使上下文包含已选内容，长期奖励再评价页面整体。输出单位更大也带来更难的搜索与信用问题，不自动保证全局最优。 示意：一页全是同系列电影单条都相关，用户却缺少探索入口；整页目标可考虑同时放不同类型，让页面整体更有用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-genpage-e2b0c563" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-35e394cf0e16a8ef">GenPage 的整页动作为什么比逐物品预测更接近首页目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agenpage">GenPage: Towards End-to-End Generative Homepage Construction at Netflix</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Netflix</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>首页价值取决于内容类型、布局和项目之间的组合，单品各自高分仍可组成重复或不连贯页面。整页生成使上下文包含已选内容，长期奖励再评价页面整体。输出单位更大也带来更难的搜索与信用问题，不自动保证全局最优。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一页全是同系列电影单条都相关，用户却缺少探索入口；整页目标可考虑同时放不同类型，让页面整体更有用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.31031">原论文</a> · <a href="../../../../reproductions/2606.31031-genpage/">实现解读</a> · <a href="#qa-35e394cf0e16a8ef">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:genpage" data-paper-title="GenPage: Towards End-to-End Generative Homepage Construction at Netflix" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="GenPage: Towards End-to-End Generative Homepage Construction at Netflix 搜广推与 LLM 应用 Netflix 2026-06-30 用一个生成模型直接输出整页而非逐阶段召回排序，并在 WBC/SFT 后以生产长期奖励进行 RL 后训练，同时处理业务规则和冷启动。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation page-generation reinforcement-learning 搜广推 重排、展示与长期价值 GenPage直接生成整页，为什么还需要长期奖励后训练，而非只模仿已有页面？ 行为克隆或SFT主要重现日志中的展示分布，未必表达不同位置、内容组合对长期价值的共同影响。整页奖励把评价对象提升到页面决策，再通过后训练调整策略，同时保留业务可行性与冷启动处理。页面级建模不保证因果最优，尤其不能把公开代理列表收益当作生产长期留存。 示意：日志里每行都堆热门内容，模仿会复制这种布局；整页评价可能发现适量新内容有助持续探索，但需真实长期反馈，而不是只凭标题多样就假定收益。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:genpage" data-paper-title="GenPage: Towards End-to-End Generative Homepage Construction at Netflix" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="GenPage: Towards End-to-End Generative Homepage Construction at Netflix 搜广推与 LLM 应用 Netflix 2026-06-30 用一个生成模型直接输出整页而非逐阶段召回排序，并在 WBC/SFT 后以生产长期奖励进行 RL 后训练，同时处理业务规则和冷启动。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation page-generation reinforcement-learning 搜广推 重排、展示与长期价值 GenPage 的 WBC/SFT 与长期 RL 后训练，分别依赖什么证据？ 模仿阶段借已有页面和加权示范建立可用策略，RL 再按长期反馈调整超出日志模仿的取舍。后者依赖可靠环境与奖励，不能由离线电影代理直接恢复真实留存。业务规则和冷启动也需要独立约束，而非完全交给单个长期数值。 示意：旧首页偏熟悉内容，模仿可快速学会可用布局；若真实长期反馈支持适度探索，后训练才有依据改变，不能凭空假设探索一定增加留存。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-6cf9fc644ec1b04d">GenPage 的 WBC/SFT 与长期 RL 后训练，分别依赖什么证据？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agenpage">GenPage: Towards End-to-End Generative Homepage Construction at Netflix</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Netflix</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>模仿阶段借已有页面和加权示范建立可用策略，RL 再按长期反馈调整超出日志模仿的取舍。后者依赖可靠环境与奖励，不能由离线电影代理直接恢复真实留存。业务规则和冷启动也需要独立约束，而非完全交给单个长期数值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>旧首页偏熟悉内容，模仿可快速学会可用布局；若真实长期反馈支持适度探索，后训练才有依据改变，不能凭空假设探索一定增加留存。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.31031">原论文</a> · <a href="../../../../reproductions/2606.31031-genpage/">实现解读</a> · <a href="#qa-6cf9fc644ec1b04d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:genpage" data-paper-title="GenPage: Towards End-to-End Generative Homepage Construction at Netflix" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="GenPage: Towards End-to-End Generative Homepage Construction at Netflix 搜广推与 LLM 应用 Netflix 2026-06-30 用一个生成模型直接输出整页而非逐阶段召回排序，并在 WBC/SFT 后以生产长期奖励进行 RL 后训练，同时处理业务规则和冷启动。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation page-generation reinforcement-learning 搜广推 重排、展示与长期价值 GenPage 本地 MovieLens 核心路径为什么不能当作 Netflix 整页生产实现？ 公开数据没有真实首页布局、多形态内容与长期奖励，仅按固定候选协议检查代理机制。验收应明确哪些页面状态、约束与更新实际存在，不把一个排序列表改名为首页。来源本地也保留负结果，不能用原文线上收益填补缺失。 示意：十部电影排成列表没有轮播、文案与跨天反馈；它可以检验部分组合逻辑，却不能证明整页 UI 与留存策略都已上线可用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-4f31e6dc5dcbd000">GenPage 本地 MovieLens 核心路径为什么不能当作 Netflix 整页生产实现？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agenpage">GenPage: Towards End-to-End Generative Homepage Construction at Netflix</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Netflix</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>公开数据没有真实首页布局、多形态内容与长期奖励，仅按固定候选协议检查代理机制。验收应明确哪些页面状态、约束与更新实际存在，不把一个排序列表改名为首页。来源本地也保留负结果，不能用原文线上收益填补缺失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>十部电影排成列表没有轮播、文案与跨天反馈；它可以检验部分组合逻辑，却不能证明整页 UI 与留存策略都已上线可用。</p>
<p class="ar-learning-sources">依据：本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.31031">原论文</a> · <a href="../../../../reproductions/2606.31031-genpage/">实现解读</a> · <a href="#qa-4f31e6dc5dcbd000">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:piano" data-paper-title="PIANO: Personalized Reranking via Information Aggregation Node for Music Search Optimization" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="PIANO: Personalized Reranking via Information Aggregation Node for Music Search Optimization 搜广推与 LLM 应用 NetEase Cloud Music 2026-06-15 Query-Driven Interest Refiner 从历史中提取查询相关兴趣，Information Aggregation Node 汇总整张候选列表并反向条件化 item 级 CTR/CVR。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 PIANO 为 0.04988，相对变化 -7.65%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  search reranking listwise 搜广推 重排、展示与长期价值 PIANO 的 IAN 为什么读取整张候选列表？ 用户选择某项受同页替代与竞争影响，列表聚合为单品 CTR/CVR 提供当前可选环境；查询相关历史则提供用户需求。它把“谁和谁一起出现”纳入评分，和单品静态价值不同，列表变化后分数也可能变化。 示意：一双中价鞋在全是高价专业鞋的列表里显得实用，在入门低价列表里又不同；同一用户商品对的条件概率因此未必固定。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-piano-1fe78019" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-de9d8b1bc0e5a79f">PIANO 的 IAN 为什么读取整张候选列表？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apiano">PIANO: Personalized Reranking via Information Aggregation Node for Music Search Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NetEase Cloud Music</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用户选择某项受同页替代与竞争影响，列表聚合为单品 CTR/CVR 提供当前可选环境；查询相关历史则提供用户需求。它把“谁和谁一起出现”纳入评分，和单品静态价值不同，列表变化后分数也可能变化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一双中价鞋在全是高价专业鞋的列表里显得实用，在入门低价列表里又不同；同一用户商品对的条件概率因此未必固定。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.16641">原论文</a> · <a href="../../../../reproductions/2606.16641-piano/">实现解读</a> · <a href="#qa-de9d8b1bc0e5a79f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:piano" data-paper-title="PIANO: Personalized Reranking via Information Aggregation Node for Music Search Optimization" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="PIANO: Personalized Reranking via Information Aggregation Node for Music Search Optimization 搜广推与 LLM 应用 NetEase Cloud Music 2026-06-15 Query-Driven Interest Refiner 从历史中提取查询相关兴趣，Information Aggregation Node 汇总整张候选列表并反向条件化 item 级 CTR/CVR。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 PIANO 为 0.04988，相对变化 -7.65%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  search reranking listwise 搜广推 重排、展示与长期价值 PIANO 为什么同时提取查询相关历史兴趣，又用整张候选列表反向条件化单品预测？ 查询相关兴趣帮助模型从历史中选出当前搜索意图需要的部分；列表聚合节点则让单品 CTR/CVR 预测知道它处于怎样的候选集合中。前者解决用户历史与查询匹配，后者处理候选间的上下文关系。列表一变，条件化得分也可能变化，因此不能把它当作对每件商品独立、可任意跨列表复用的分数。 示意：用户平时买跑鞋，当前搜索登山鞋；先聚焦户外相关历史。同一双鞋放在全是高价专业鞋的列表中，与放在入门款列表中，选择概率也可能不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:piano" data-paper-title="PIANO: Personalized Reranking via Information Aggregation Node for Music Search Optimization" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="PIANO: Personalized Reranking via Information Aggregation Node for Music Search Optimization 搜广推与 LLM 应用 NetEase Cloud Music 2026-06-15 Query-Driven Interest Refiner 从历史中提取查询相关兴趣，Information Aggregation Node 汇总整张候选列表并反向条件化 item 级 CTR/CVR。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 PIANO 为 0.04988，相对变化 -7.65%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  search reranking listwise 搜广推 重排、展示与长期价值 PIANO 列表条件化与独立 pointwise CTR，相比缓存与评估单位有何变化？ 独立模型分数可在相同用户物品条件下复用，列表条件化还依赖整组候选，不能跨列表盲用缓存。更丰富上下文可能帮助竞争建模，也增加计算和候选分布敏感性。来源公开代理负结果不支持普遍优越结论。 示意：从十件候选删掉最便宜款后，其余预测可变；若复用删前分数，就没有让 IAN 反映新列表，和模型定义不一致。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4f6aa8a43da07d5d">PIANO 列表条件化与独立 pointwise CTR，相比缓存与评估单位有何变化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apiano">PIANO: Personalized Reranking via Information Aggregation Node for Music Search Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NetEase Cloud Music</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立模型分数可在相同用户物品条件下复用，列表条件化还依赖整组候选，不能跨列表盲用缓存。更丰富上下文可能帮助竞争建模，也增加计算和候选分布敏感性。来源公开代理负结果不支持普遍优越结论。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>从十件候选删掉最便宜款后，其余预测可变；若复用删前分数，就没有让 IAN 反映新列表，和模型定义不一致。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.16641">原论文</a> · <a href="../../../../reproductions/2606.16641-piano/">实现解读</a> · <a href="#qa-4f6aa8a43da07d5d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:piano" data-paper-title="PIANO: Personalized Reranking via Information Aggregation Node for Music Search Optimization" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="PIANO: Personalized Reranking via Information Aggregation Node for Music Search Optimization 搜广推与 LLM 应用 NetEase Cloud Music 2026-06-15 Query-Driven Interest Refiner 从历史中提取查询相关兴趣，Information Aggregation Node 汇总整张候选列表并反向条件化 item 级 CTR/CVR。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 PIANO 为 0.04988，相对变化 -7.65%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  search reranking listwise 搜广推 重排、展示与长期价值 PIANO 的列表 aggregation 在训练时如何避免 gold target 位置泄漏？ 候选集合可输入，但排序、特殊标识与聚合不能按真实点击把目标提前或标记；标签只进入损失。padding 与候选数量也需 mask，查询取历史只能用既往事件。否则 IAN 可能读目标位置捷径，而非学习真实竞争。 示意：每次把正确商品放第一列再算 attention，模型易记首列；测试若也照做会虚高，应保持与真实服务同义的无答案候选布局。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1e1faf71d3bafef6">PIANO 的列表 aggregation 在训练时如何避免 gold target 位置泄漏？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apiano">PIANO: Personalized Reranking via Information Aggregation Node for Music Search Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NetEase Cloud Music</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>候选集合可输入，但排序、特殊标识与聚合不能按真实点击把目标提前或标记；标签只进入损失。padding 与候选数量也需 mask，查询取历史只能用既往事件。否则 IAN 可能读目标位置捷径，而非学习真实竞争。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>每次把正确商品放第一列再算 attention，模型易记首列；测试若也照做会虚高，应保持与真实服务同义的无答案候选布局。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.16641">原论文</a> · <a href="../../../../reproductions/2606.16641-piano/">实现解读</a> · <a href="#qa-1e1faf71d3bafef6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:taiji" data-paper-title="Taiji: Pareto Optimal Policy Optimization with Semantics-IDs Trade-off for Industrial LLM-Enhanced Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Taiji: Pareto Optimal Policy Optimization with Semantics-IDs Trade-off for Industrial LLM-Enhanced Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-06-02 先用反向工程偏好推理与拒绝采样激活推荐 CoT，再由 POPO 动态平衡 LLM 语义奖励和推荐协同 ID 奖励，避免固定权重遗漏非凸 Pareto 前沿。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.06448，相对变化 +19.39%。本地代理目标与论文生产任务不同，不能外推线上 lift。  advertising reinforcement-alignment pareto-optimization 搜广推 重排、展示与长期价值 Taiji为什么同时用语义奖励和协同ID奖励？ 语言语义能解释内容，协同ID反映平台行为偏好，两者可能冲突。先激活推荐CoT，再动态平衡目标，避免单一语言偏好脱离真实交互。 例如描述相似物品不一定被同类用户共同喜欢。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-taiji-2fa562ab" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0f928cae1c771b93">Taiji为什么同时用语义奖励和协同ID奖励？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ataiji">Taiji: Pareto Optimal Policy Optimization with Semantics-IDs Trade-off for Industrial LLM-Enhanced Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语言语义能解释内容，协同ID反映平台行为偏好，两者可能冲突。先激活推荐CoT，再动态平衡目标，避免单一语言偏好脱离真实交互。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如描述相似物品不一定被同类用户共同喜欢。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.03866">原论文</a> · <a href="../../../../reproductions/2606.03866-taiji/">实现解读</a> · <a href="#qa-0f928cae1c771b93">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:taiji" data-paper-title="Taiji: Pareto Optimal Policy Optimization with Semantics-IDs Trade-off for Industrial LLM-Enhanced Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Taiji: Pareto Optimal Policy Optimization with Semantics-IDs Trade-off for Industrial LLM-Enhanced Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-06-02 先用反向工程偏好推理与拒绝采样激活推荐 CoT，再由 POPO 动态平衡 LLM 语义奖励和推荐协同 ID 奖励，避免固定权重遗漏非凸 Pareto 前沿。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.06448，相对变化 +19.39%。本地代理目标与论文生产任务不同，不能外推线上 lift。  advertising reinforcement-alignment pareto-optimization 搜广推 重排、展示与长期价值 TAIJI 为什么动态平衡语义奖励和协同 ID 奖励，而不使用一组固定权重？ 语义奖励衡量内容与解释的契合，协同奖励反映行为关系，不同样本可能需要不同取舍。固定加权只搜索有限方向，尤其可能遗漏非凸前沿上的有用方案；动态权重试图适配这些差异。反向偏好推理和拒绝采样先激活推荐推理，再做多目标对齐，但动态权重仍不能保证识别真实用户最优偏好。 示意：冷门新品缺乏行为反馈时多借语义，热门商品有充分交互时可更依赖协同信号。若所有样本都用七比三，可能同时不适合这两类物品。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:taiji" data-paper-title="Taiji: Pareto Optimal Policy Optimization with Semantics-IDs Trade-off for Industrial LLM-Enhanced Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Taiji: Pareto Optimal Policy Optimization with Semantics-IDs Trade-off for Industrial LLM-Enhanced Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-06-02 先用反向工程偏好推理与拒绝采样激活推荐 CoT，再由 POPO 动态平衡 LLM 语义奖励和推荐协同 ID 奖励，避免固定权重遗漏非凸 Pareto 前沿。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.06448，相对变化 +19.39%。本地代理目标与论文生产任务不同，不能外推线上 lift。  advertising reinforcement-alignment pareto-optimization 搜广推 重排、展示与长期价值 动态Pareto权重与固定线性加权有什么区别？ 固定权重只覆盖一定取舍，非凸前沿可能遗漏；动态权重试图适应样本或阶段。但没有真实多目标对照时，不能声称已找到全局Pareto最优。 例如某用户更看重语义新颖，另一用户更依赖稳定行为证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c3adb493a4a9fad7">动态Pareto权重与固定线性加权有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ataiji">Taiji: Pareto Optimal Policy Optimization with Semantics-IDs Trade-off for Industrial LLM-Enhanced Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定权重只覆盖一定取舍，非凸前沿可能遗漏；动态权重试图适应样本或阶段。但没有真实多目标对照时，不能声称已找到全局Pareto最优。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某用户更看重语义新颖，另一用户更依赖稳定行为证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.03866">原论文</a> · <a href="../../../../reproductions/2606.03866-taiji/">实现解读</a> · <a href="#qa-c3adb493a4a9fad7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:taiji" data-paper-title="Taiji: Pareto Optimal Policy Optimization with Semantics-IDs Trade-off for Industrial LLM-Enhanced Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Taiji: Pareto Optimal Policy Optimization with Semantics-IDs Trade-off for Industrial LLM-Enhanced Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-06-02 先用反向工程偏好推理与拒绝采样激活推荐 CoT，再由 POPO 动态平衡 LLM 语义奖励和推荐协同 ID 奖励，避免固定权重遗漏非凸 Pareto 前沿。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.06448，相对变化 +19.39%。本地代理目标与论文生产任务不同，不能外推线上 lift。  advertising reinforcement-alignment pareto-optimization 搜广推 重排、展示与长期价值 Taiji拒绝采样和权重学习需要怎样隔离数据？ 只用训练允许的偏好推理与验证信号筛候选，测试反馈不能选择CoT或目标权重。当前MovieLens代理未复刻真实LLM、私有协同码和生产服务。 例如看完测试点击再挑一条能解释它的CoT，会泄露目标行为。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-45ec1fbe6228d174">Taiji拒绝采样和权重学习需要怎样隔离数据？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ataiji">Taiji: Pareto Optimal Policy Optimization with Semantics-IDs Trade-off for Industrial LLM-Enhanced Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只用训练允许的偏好推理与验证信号筛候选，测试反馈不能选择CoT或目标权重。当前MovieLens代理未复刻真实LLM、私有协同码和生产服务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如看完测试点击再挑一条能解释它的CoT，会泄露目标行为。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.03866">原论文</a> · <a href="../../../../reproductions/2606.03866-taiji/">实现解读</a> · <a href="#qa-45ec1fbe6228d174">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:primal-dual-decoding" data-paper-title="Stochastic Primal-Dual Decoding for Multiobjective Generative Recommender Systems" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Stochastic Primal-Dual Decoding for Multiobjective Generative Recommender Systems 搜广推与 LLM 应用 Spotify 2026-05-26 不重训生成式推荐模型，在逐位置解码时把相关性 logits 与辅助目标贡献相加，并根据剩余约束松弛量以镜像下降动态更新拉格朗日乘子。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.02109，相对变化 -60.95%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation multiobjective constrained-decoding 搜广推 重排、展示与长期价值 原始—对偶解码为什么可以不重训生成器？ 它在服务搜索时将原相关性分和辅助目标贡献结合，再动态调整乘子，改变每步选项而不更新模型权重。收益依赖候选与分数质量，不创造生成器未提供的知识；运行策略变了，成本、相关性损失和约束达成仍需分别测。 示意：原模型分数不动，解码逐步提高缺少新作者时的奖励权重；这是一种搜索控制，不是模型经过新数据学会偏好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-primal-dual-decoding-161adf1d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-299e1034b7d7ddc7">原始—对偶解码为什么可以不重训生成器？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aprimal-dual-decoding">Stochastic Primal-Dual Decoding for Multiobjective Generative Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Spotify</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它在服务搜索时将原相关性分和辅助目标贡献结合，再动态调整乘子，改变每步选项而不更新模型权重。收益依赖候选与分数质量，不创造生成器未提供的知识；运行策略变了，成本、相关性损失和约束达成仍需分别测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>原模型分数不动，解码逐步提高缺少新作者时的奖励权重；这是一种搜索控制，不是模型经过新数据学会偏好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.19357">原论文</a> · <a href="../../../../reproductions/2607.19357-primal-dual-decoding/">实现解读</a> · <a href="#qa-299e1034b7d7ddc7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:primal-dual-decoding" data-paper-title="Stochastic Primal-Dual Decoding for Multiobjective Generative Recommender Systems" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Stochastic Primal-Dual Decoding for Multiobjective Generative Recommender Systems 搜广推与 LLM 应用 Spotify 2026-05-26 不重训生成式推荐模型，在逐位置解码时把相关性 logits 与辅助目标贡献相加，并根据剩余约束松弛量以镜像下降动态更新拉格朗日乘子。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.02109，相对变化 -60.95%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation multiobjective constrained-decoding 搜广推 重排、展示与长期价值 原始—对偶解码为什么要随剩余约束动态调整乘子，而不是固定加一个多样性分？ 固定权重无法根据已经生成的内容判断约束是否快要违约。原始—对偶解码在每个位置组合模型分数与辅助目标贡献，并按当前约束松弛量更新乘子，使后续选择补偿前面决策。不需要重训生成器，但只能在可选候选与局部解码范围内权衡，也可能牺牲相关性；并非所有硬约束都能自动满足。 示意：一张五条列表希望至少两条来自新作者。前四条只选到一条时，最后一步应提高新作者贡献权重；若早已满足，则无需继续用同样强度挤压相关性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:primal-dual-decoding" data-paper-title="Stochastic Primal-Dual Decoding for Multiobjective Generative Recommender Systems" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Stochastic Primal-Dual Decoding for Multiobjective Generative Recommender Systems 搜广推与 LLM 应用 Spotify 2026-05-26 不重训生成式推荐模型，在逐位置解码时把相关性 logits 与辅助目标贡献相加，并根据剩余约束松弛量以镜像下降动态更新拉格朗日乘子。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.02109，相对变化 -60.95%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation multiobjective constrained-decoding 搜广推 重排、展示与长期价值 动态对偶乘子与固定多样性权重，相比何时会放松或加紧约束？ 固定权重不看已选前缀是否达标，对偶更新依据当前贡献与目标进度改变强度，让余下位置补不足或减少过度补偿。它是局部在线取舍，未必满足不可行硬约束，也可能牺牲相关性，不能称无损改进。 示意：前四条已含足够新作者，最后一条可回归相关性；如果仍缺配额则继续加大辅助贡献，固定加分无法表达两种状态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0779bc4cfc3e4265">动态对偶乘子与固定多样性权重，相比何时会放松或加紧约束？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aprimal-dual-decoding">Stochastic Primal-Dual Decoding for Multiobjective Generative Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Spotify</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定权重不看已选前缀是否达标，对偶更新依据当前贡献与目标进度改变强度，让余下位置补不足或减少过度补偿。它是局部在线取舍，未必满足不可行硬约束，也可能牺牲相关性，不能称无损改进。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>前四条已含足够新作者，最后一条可回归相关性；如果仍缺配额则继续加大辅助贡献，固定加分无法表达两种状态。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.19357">原论文</a> · <a href="../../../../reproductions/2607.19357-primal-dual-decoding/">实现解读</a> · <a href="#qa-0779bc4cfc3e4265">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:primal-dual-decoding" data-paper-title="Stochastic Primal-Dual Decoding for Multiobjective Generative Recommender Systems" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Stochastic Primal-Dual Decoding for Multiobjective Generative Recommender Systems 搜广推与 LLM 应用 Spotify 2026-05-26 不重训生成式推荐模型，在逐位置解码时把相关性 logits 与辅助目标贡献相加，并根据剩余约束松弛量以镜像下降动态更新拉格朗日乘子。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.02109，相对变化 -60.95%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation multiobjective constrained-decoding 搜广推 重排、展示与长期价值 镜像下降更新为什么要求乘子非负，并注意指数数值范围？ 非负乘子对应约束惩罚方向，乘法指数更新在正初始化下保持符号，但过大步长可能溢出或迅速极端化。辅助贡献、目标 R/K 与分数单位也需一致。来源公式简写概率与 logit 时要遵循真实实现口径，不能任意互换。 示意：把观看秒数直接与概率混加可能让辅助项完全支配；指数连续放大后即使程序没报错，也可能只追配额而忽略用户相关性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6d3a9288628b2b06">镜像下降更新为什么要求乘子非负，并注意指数数值范围？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aprimal-dual-decoding">Stochastic Primal-Dual Decoding for Multiobjective Generative Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Spotify</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>非负乘子对应约束惩罚方向，乘法指数更新在正初始化下保持符号，但过大步长可能溢出或迅速极端化。辅助贡献、目标 R/K 与分数单位也需一致。来源公式简写概率与 logit 时要遵循真实实现口径，不能任意互换。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把观看秒数直接与概率混加可能让辅助项完全支配；指数连续放大后即使程序没报错，也可能只追配额而忽略用户相关性。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.19357">原论文</a> · <a href="../../../../reproductions/2607.19357-primal-dual-decoding/">实现解读</a> · <a href="#qa-6d3a9288628b2b06">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:degre" data-paper-title="DeGRe: Listwise Generative Reranking with Offline Lookahead Distillation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DeGRe: Listwise Generative Reranking with Offline Lookahead Distillation 搜广推与 LLM 应用 Alibaba Group / Zhejiang University 2026-05-25 逐点生成器只学习日志中的单一路径，难以直接优化整张列表的长期价值。DeGRe 离线训练累计回报 evaluator，用 beam search 探索高价值列表，再把每个前缀下所有剩余候选的前瞻价值蒸馏为 dense soft label；线上只保留一次 greedy generator。 Fidelity: 核心机制复现。累计价值评估器、lookahead beam mining、逐前缀 dense label、beam weighting 与单次在线生成路径均实际执行。未复刻私有交易标签与工业 Transformer 规模；本地结果仅验证离线 evaluator→beam mining→dense distillation 链路。本地对照口径：基线是相同候选与特征的 pointwise generator；实验组 DeGRe 加入离线前瞻蒸馏，相对基线 Hit@10 +0.00%、NDCG@10 +3.31%。  generative-recommendation reranking distillation 搜广推 重排、展示与长期价值 DeGRe 为什么用离线累计回报 evaluator，而不只把下一位置真实物品当标签？ 单点标签只说明日志路径，不能评价不同候选加入后整张列表的未来价值。evaluator 为多种前缀提供前瞻估计，离线 beam 探索后将这些价值传给生成器。目标因而从模仿单一路径扩展到列表结果，但 evaluator 的误差也会被蒸馏继承。 示意：先放一条基础教程可能引出后续进阶内容，单看当前点击未必高；累计评价尝试理解整段组合，再教生成器一次选得更好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-degre-898bafc1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-539fd601ea9cebcc">DeGRe 为什么用离线累计回报 evaluator，而不只把下一位置真实物品当标签？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adegre">DeGRe: Listwise Generative Reranking with Offline Lookahead Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group / Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单点标签只说明日志路径，不能评价不同候选加入后整张列表的未来价值。evaluator 为多种前缀提供前瞻估计，离线 beam 探索后将这些价值传给生成器。目标因而从模仿单一路径扩展到列表结果，但 evaluator 的误差也会被蒸馏继承。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先放一条基础教程可能引出后续进阶内容，单看当前点击未必高；累计评价尝试理解整段组合，再教生成器一次选得更好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.25749">原论文</a> · <a href="../../../../reproductions/2605.25749-degre/">实现解读</a> · <a href="#qa-539fd601ea9cebcc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:degre" data-paper-title="DeGRe: Listwise Generative Reranking with Offline Lookahead Distillation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DeGRe: Listwise Generative Reranking with Offline Lookahead Distillation 搜广推与 LLM 应用 Alibaba Group / Zhejiang University 2026-05-25 逐点生成器只学习日志中的单一路径，难以直接优化整张列表的长期价值。DeGRe 离线训练累计回报 evaluator，用 beam search 探索高价值列表，再把每个前缀下所有剩余候选的前瞻价值蒸馏为 dense soft label；线上只保留一次 greedy generator。 Fidelity: 核心机制复现。累计价值评估器、lookahead beam mining、逐前缀 dense label、beam weighting 与单次在线生成路径均实际执行。未复刻私有交易标签与工业 Transformer 规模；本地结果仅验证离线 evaluator→beam mining→dense distillation 链路。本地对照口径：基线是相同候选与特征的 pointwise generator；实验组 DeGRe 加入离线前瞻蒸馏，相对基线 Hit@10 +0.00%、NDCG@10 +3.31%。  generative-recommendation reranking distillation 搜广推 重排、展示与长期价值 DeGRe离线做beam前瞻，为什么上线却只保留greedy generator？ 前瞻evaluator能比较不同前缀及其后续列表价值，但在线逐步搜索成本高。DeGRe离线探索高价值列表，再把每个前缀下剩余候选的价值分布蒸馏为软标签，让生成器在单步选择中近似吸收未来影响。蒸馏的是估计价值而非真实最优策略，evaluator偏差也可能被一起固化。 示意：第一项点分最高的候选可能使后面只能选重复内容；离线搜索发现另一开头能组成更好整页，再教greedy模型优先选它，而非上线每次重搜所有排列。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:degre" data-paper-title="DeGRe: Listwise Generative Reranking with Offline Lookahead Distillation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DeGRe: Listwise Generative Reranking with Offline Lookahead Distillation 搜广推与 LLM 应用 Alibaba Group / Zhejiang University 2026-05-25 逐点生成器只学习日志中的单一路径，难以直接优化整张列表的长期价值。DeGRe 离线训练累计回报 evaluator，用 beam search 探索高价值列表，再把每个前缀下所有剩余候选的前瞻价值蒸馏为 dense soft label；线上只保留一次 greedy generator。 Fidelity: 核心机制复现。累计价值评估器、lookahead beam mining、逐前缀 dense label、beam weighting 与单次在线生成路径均实际执行。未复刻私有交易标签与工业 Transformer 规模；本地结果仅验证离线 evaluator→beam mining→dense distillation 链路。本地对照口径：基线是相同候选与特征的 pointwise generator；实验组 DeGRe 加入离线前瞻蒸馏，相对基线 Hit@10 +0.00%、NDCG@10 +3.31%。  generative-recommendation reranking distillation 搜广推 重排、展示与长期价值 DeGRe 的 dense soft label 与只蒸馏 beam 最佳列表，有什么反馈密度区别？ 最佳列表只为每个位置给一个目标，dense 标签则对该前缀下所有剩余候选按前瞻价值分配概率，传递“接近好答案”的关系。列表权重再强调更高价值轨迹。分布更密不意味着更准确，错误 evaluator 会给更多候选传播偏差。 示意：两本书都适合作为下一项，软标签可分别给较高概率，单赢家只奖励其中一本；若估值把热门度当价值，两者也都会被带偏。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a2565b25b45fc835">DeGRe 的 dense soft label 与只蒸馏 beam 最佳列表，有什么反馈密度区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adegre">DeGRe: Listwise Generative Reranking with Offline Lookahead Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group / Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最佳列表只为每个位置给一个目标，dense 标签则对该前缀下所有剩余候选按前瞻价值分配概率，传递“接近好答案”的关系。列表权重再强调更高价值轨迹。分布更密不意味着更准确，错误 evaluator 会给更多候选传播偏差。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两本书都适合作为下一项，软标签可分别给较高概率，单赢家只奖励其中一本；若估值把热门度当价值，两者也都会被带偏。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.25749">原论文</a> · <a href="../../../../reproductions/2605.25749-degre/">实现解读</a> · <a href="#qa-a2565b25b45fc835">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:degre" data-paper-title="DeGRe: Listwise Generative Reranking with Offline Lookahead Distillation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="DeGRe: Listwise Generative Reranking with Offline Lookahead Distillation 搜广推与 LLM 应用 Alibaba Group / Zhejiang University 2026-05-25 逐点生成器只学习日志中的单一路径，难以直接优化整张列表的长期价值。DeGRe 离线训练累计回报 evaluator，用 beam search 探索高价值列表，再把每个前缀下所有剩余候选的前瞻价值蒸馏为 dense soft label；线上只保留一次 greedy generator。 Fidelity: 核心机制复现。累计价值评估器、lookahead beam mining、逐前缀 dense label、beam weighting 与单次在线生成路径均实际执行。未复刻私有交易标签与工业 Transformer 规模；本地结果仅验证离线 evaluator→beam mining→dense distillation 链路。本地对照口径：基线是相同候选与特征的 pointwise generator；实验组 DeGRe 加入离线前瞻蒸馏，相对基线 Hit@10 +0.00%、NDCG@10 +3.31%。  generative-recommendation reranking distillation 搜广推 重排、展示与长期价值 DeGRe 构造 qt 时，为什么要屏蔽已选物品并对同一前缀的剩余集归一？ 目标定义是下一位置的合法延续，已选物品重复进入会训练出重复列表。所有候选价值应对应同一前缀，softmax 范围和学生输出 mask 一致；不同前缀的价值不能直接混用。线上 greedy 仍需逐步更新已选状态，即使不再运行 beam。 示意：前缀已含电影甲，第二步的标签只在其他电影间分配；若甲仍在分母并高分，会诱导学生重复推荐它，偏离列表任务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-64f10e3b26c58fd2">DeGRe 构造 qt 时，为什么要屏蔽已选物品并对同一前缀的剩余集归一？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adegre">DeGRe: Listwise Generative Reranking with Offline Lookahead Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group / Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标定义是下一位置的合法延续，已选物品重复进入会训练出重复列表。所有候选价值应对应同一前缀，softmax 范围和学生输出 mask 一致；不同前缀的价值不能直接混用。线上 greedy 仍需逐步更新已选状态，即使不再运行 beam。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>前缀已含电影甲，第二步的标签只在其他电影间分配；若甲仍在分母并高分，会诱导学生重复推荐它，偏离列表任务。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.25749">原论文</a> · <a href="../../../../reproductions/2605.25749-degre/">实现解读</a> · <a href="#qa-64f10e3b26c58fd2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:prl-puts" data-paper-title="A Production-Ready RL Framework for Personalized Utility Tuning with Pareto Sweeping in Pinterest Recommender Systems" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="A Production-Ready RL Framework for Personalized Utility Tuning with Pareto Sweeping in Pinterest Recommender Systems 搜广推与 LLM 应用 Pinterest 2026-05-08 双头 Q 网络分别估计 Repin 与 P2P utility，再通过 Pareto sweeping 离线筛选不劣策略；线上仅切换可治理的权重策略，不更换模型。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 prl-puts 核心机制，相对 NDCG@10 +39.64%。  reinforcement-learning multi-objective-ranking homefeed 搜广推 重排、展示与长期价值 PRL-PUTS 为什么分别估计 Repin 与 P2P 两个 Q 值？ 两个效用体现不同业务结果，分头估计让线上可以改变权重策略而不重新训练全部价值函数，再通过离线 Pareto 扫描选可治理取舍。Q 的估计误差会影响前沿，双头并不表示两个目标一定能同时提高。 示意：一个动作更易收藏，一个更易后续深度互动，双头保留各自价值；合成单奖励后若想调整取舍，就可能需要重训。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-prl-puts-9d4fc321" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-cfcea21c081d6ffb">PRL-PUTS 为什么分别估计 Repin 与 P2P 两个 Q 值？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aprl-puts">A Production-Ready RL Framework for Personalized Utility Tuning with Pareto Sweeping in Pinterest Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两个效用体现不同业务结果，分头估计让线上可以改变权重策略而不重新训练全部价值函数，再通过离线 Pareto 扫描选可治理取舍。Q 的估计误差会影响前沿，双头并不表示两个目标一定能同时提高。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个动作更易收藏，一个更易后续深度互动，双头保留各自价值；合成单奖励后若想调整取舍，就可能需要重训。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.16344">原论文</a> · <a href="../../../../reproductions/2605.16344-prl-puts/">实现解读</a> · <a href="#qa-cfcea21c081d6ffb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:prl-puts" data-paper-title="A Production-Ready RL Framework for Personalized Utility Tuning with Pareto Sweeping in Pinterest Recommender Systems" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="A Production-Ready RL Framework for Personalized Utility Tuning with Pareto Sweeping in Pinterest Recommender Systems 搜广推与 LLM 应用 Pinterest 2026-05-08 双头 Q 网络分别估计 Repin 与 P2P utility，再通过 Pareto sweeping 离线筛选不劣策略；线上仅切换可治理的权重策略，不更换模型。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 prl-puts 核心机制，相对 NDCG@10 +39.64%。  reinforcement-learning multi-objective-ranking homefeed 搜广推 重排、展示与长期价值 PRL-PUTS 为什么用双头 Q 值和 Pareto sweeping 预选权重，而不线上随意调单一奖励？ 两个 Q 头分别估计不同业务效用，权重组合对应不同策略取舍。离线扫描权重并筛掉被其他策略同时支配的选择，可形成可治理的候选前沿；线上切换权重即可改变目标平衡，无须替换整套模型。但 Q 值误差和分布变化仍影响前沿可靠性，离线不劣不能直接推出线上更优。 示意：一组权重带来更多收藏，另一组带来更多后续互动。若某组两项都更差就先淘汰；保留下来的取舍点再供业务选择，而不是在真实流量里盲目搜索所有权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:prl-puts" data-paper-title="A Production-Ready RL Framework for Personalized Utility Tuning with Pareto Sweeping in Pinterest Recommender Systems" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="A Production-Ready RL Framework for Personalized Utility Tuning with Pareto Sweeping in Pinterest Recommender Systems 搜广推与 LLM 应用 Pinterest 2026-05-08 双头 Q 网络分别估计 Repin 与 P2P utility，再通过 Pareto sweeping 离线筛选不劣策略；线上仅切换可治理的权重策略，不更换模型。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 prl-puts 核心机制，相对 NDCG@10 +39.64%。  reinforcement-learning multi-objective-ranking homefeed 搜广推 重排、展示与长期价值 Pareto sweeping 与只选单一加权最高点，相比保留了什么业务选择？ 单权重仅给一个折中，扫描不同权重并剔除被同时支配者，保留多种不劣策略供目标变化时选择。前沿依据离线估计，不是已测线上保证；同样值的误差也可能造成虚假不劣，需不确定性与实验验证。 示意：甲收藏更强、乙深度互动更强，两者都可留；丙两项都差应排除，而不是因为某个随意权重让它偶然得分高就上线。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5dfcbf1bdbb87b31">Pareto sweeping 与只选单一加权最高点，相比保留了什么业务选择？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aprl-puts">A Production-Ready RL Framework for Personalized Utility Tuning with Pareto Sweeping in Pinterest Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单权重仅给一个折中，扫描不同权重并剔除被同时支配者，保留多种不劣策略供目标变化时选择。前沿依据离线估计，不是已测线上保证；同样值的误差也可能造成虚假不劣，需不确定性与实验验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>甲收藏更强、乙深度互动更强，两者都可留；丙两项都差应排除，而不是因为某个随意权重让它偶然得分高就上线。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.16344">原论文</a> · <a href="../../../../reproductions/2605.16344-prl-puts/">实现解读</a> · <a href="#qa-5dfcbf1bdbb87b31">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:prl-puts" data-paper-title="A Production-Ready RL Framework for Personalized Utility Tuning with Pareto Sweeping in Pinterest Recommender Systems" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="A Production-Ready RL Framework for Personalized Utility Tuning with Pareto Sweeping in Pinterest Recommender Systems 搜广推与 LLM 应用 Pinterest 2026-05-08 双头 Q 网络分别估计 Repin 与 P2P utility，再通过 Pareto sweeping 离线筛选不劣策略；线上仅切换可治理的权重策略，不更换模型。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 prl-puts 核心机制，相对 NDCG@10 +39.64%。  reinforcement-learning multi-objective-ranking homefeed 搜广推 重排、展示与长期价值 PRL-PUTS 线上切换权重时，为什么仍要固定 Q 模型与动作空间版本？ 权重只在同一组可比较 Q 值上改变取舍，若同时换模型或候选动作，便无法把变化归给策略。α 应在合法范围，两个头的量纲与收益定义也需记录。本地固定 scorer 代理不能自动证明完整长期 Q 学习和线上策略治理完成。 示意：从七三切五五同时重训一个 Q 头，指标改变不能全归配比；要检验权重策略，应先保持其余估计和动作一致。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-bd0619af50c1211a">PRL-PUTS 线上切换权重时，为什么仍要固定 Q 模型与动作空间版本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aprl-puts">A Production-Ready RL Framework for Personalized Utility Tuning with Pareto Sweeping in Pinterest Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>权重只在同一组可比较 Q 值上改变取舍，若同时换模型或候选动作，便无法把变化归给策略。α 应在合法范围，两个头的量纲与收益定义也需记录。本地固定 scorer 代理不能自动证明完整长期 Q 学习和线上策略治理完成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>从七三切五五同时重训一个 Q 头，指标改变不能全归配比；要检验权重策略，应先保持其余估计和动作一致。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.16344">原论文</a> · <a href="../../../../reproductions/2605.16344-prl-puts/">实现解读</a> · <a href="#qa-bd0619af50c1211a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:glorank" data-paper-title="From Local Indices to Global Identifiers: Generative Reranking via Global Action Space" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="From Local Indices to Global Identifiers: Generative Reranking via Global Action Space 搜广推与 LLM 应用 City University of Hong Kong / Kuaishou / UC San Diego 2026-04-28 全局 Semantic ID 空间把局部候选重排改写为全库生成；先做 listwise SFT，再用组相对奖励优化列表效用与长尾覆盖。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 glorank 核心机制；相对 NDCG@10 -44.26%。  reranking generative-recommendation semantic-id reinforcement-learning 搜广推 重排、展示与长期价值 GloRank 使用全局 SID 后，为什么可以选出局部候选池之外的物品？ 局部索引只指向当前集合，生成全局标识则在整个物品空间定义动作，任务从重排扩展到重新提名。它可突破局部召回限制，也带来更大搜索空间、合法映射与列表目标难度，不能继续按固定候选重排的假设解释全部结果。 示意：局部列表只有五本热门书，编号排序永远选不到冷门专业书；全局 SID 可提名它，但必须确保目录合法且相关。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-glorank-9a7d512b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5adb644fca5330fb">GloRank 使用全局 SID 后，为什么可以选出局部候选池之外的物品？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aglorank">From Local Indices to Global Identifiers: Generative Reranking via Global Action Space</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · City University of Hong Kong / Kuaishou / UC San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>局部索引只指向当前集合，生成全局标识则在整个物品空间定义动作，任务从重排扩展到重新提名。它可突破局部召回限制，也带来更大搜索空间、合法映射与列表目标难度，不能继续按固定候选重排的假设解释全部结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>局部列表只有五本热门书，编号排序永远选不到冷门专业书；全局 SID 可提名它，但必须确保目录合法且相关。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.25291">原论文</a> · <a href="../../../../reproductions/2604.25291-glorank/">实现解读</a> · <a href="#qa-5adb644fca5330fb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:glorank" data-paper-title="From Local Indices to Global Identifiers: Generative Reranking via Global Action Space" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="From Local Indices to Global Identifiers: Generative Reranking via Global Action Space 搜广推与 LLM 应用 City University of Hong Kong / Kuaishou / UC San Diego 2026-04-28 全局 Semantic ID 空间把局部候选重排改写为全库生成；先做 listwise SFT，再用组相对奖励优化列表效用与长尾覆盖。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 glorank 核心机制；相对 NDCG@10 -44.26%。  reranking generative-recommendation semantic-id reinforcement-learning 搜广推 重排、展示与长期价值 GloRank把局部候选编号换成全局SID后，为什么任务已超出普通重排？ 局部编号只能指向上游给定的候选，生成这些编号仍受候选池上限限制。全局SID让模型在更大目录中表达选择，训练因而同时承担物品定位与列表效用对齐，不只是给既有项目换顺序。扩大动作空间也增加搜索与合法性难度，不能沿用封闭候选重排的简单评测口径。 示意：局部列表里只有十件商品，输出编号十一没有含义；全局码可指向原列表外的物品，但必须验证它在目录中可服务，而不是把新增搜索空间免费当成收益。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:glorank" data-paper-title="From Local Indices to Global Identifiers: Generative Reranking via Global Action Space" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="From Local Indices to Global Identifiers: Generative Reranking via Global Action Space 搜广推与 LLM 应用 City University of Hong Kong / Kuaishou / UC San Diego 2026-04-28 全局 Semantic ID 空间把局部候选重排改写为全库生成；先做 listwise SFT，再用组相对奖励优化列表效用与长尾覆盖。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 glorank 核心机制；相对 NDCG@10 -44.26%。  reranking generative-recommendation semantic-id reinforcement-learning 搜广推 重排、展示与长期价值 全局动作空间与局部重排，公平比较为什么需要说明候选权限？ 若一方只能重排给定列表，另一方能全库生成，收益包含候选覆盖变化而非纯排序改进。需要明确全库或局部评估、合法映射和奖励口径。机制对比不允许把两种权限下的数值直接当同一组件消融，来源本地负向也应保留。 示意：生成器找到池外正确书而局部模型没权限选，不能把差异全归给重排网络更强；候选权本身就是重要变量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-82506a319bcd80dd">全局动作空间与局部重排，公平比较为什么需要说明候选权限？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aglorank">From Local Indices to Global Identifiers: Generative Reranking via Global Action Space</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · City University of Hong Kong / Kuaishou / UC San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若一方只能重排给定列表，另一方能全库生成，收益包含候选覆盖变化而非纯排序改进。需要明确全库或局部评估、合法映射和奖励口径。机制对比不允许把两种权限下的数值直接当同一组件消融，来源本地负向也应保留。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>生成器找到池外正确书而局部模型没权限选，不能把差异全归给重排网络更强；候选权本身就是重要变量。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.25291">原论文</a> · <a href="../../../../reproductions/2604.25291-glorank/">实现解读</a> · <a href="#qa-82506a319bcd80dd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:glorank" data-paper-title="From Local Indices to Global Identifiers: Generative Reranking via Global Action Space" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="From Local Indices to Global Identifiers: Generative Reranking via Global Action Space 搜广推与 LLM 应用 City University of Hong Kong / Kuaishou / UC San Diego 2026-04-28 全局 Semantic ID 空间把局部候选重排改写为全库生成；先做 listwise SFT，再用组相对奖励优化列表效用与长尾覆盖。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 glorank 核心机制；相对 NDCG@10 -44.26%。  reranking generative-recommendation semantic-id reinforcement-learning 搜广推 重排、展示与长期价值 GloRank 实现 listwise SFT 与组奖励时，为什么全局 SID 不能只用请求内下标代替？ 请求内下标随候选排序变化，无法稳定表示全库物品，训练与解码必须使用可映射目录的全局路径。列表奖励也应针对实际生成身份，而非借测试答案修补非法码。本地代理不包含完整全局语言生成训练时，应按实际范围描述。 示意：本请求编号三是相机，下次编号三是帐篷；把三当全局 token 会让模型学到冲突含义，无法稳定生成池外物品。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-418c8e5487031517">GloRank 实现 listwise SFT 与组奖励时，为什么全局 SID 不能只用请求内下标代替？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aglorank">From Local Indices to Global Identifiers: Generative Reranking via Global Action Space</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · City University of Hong Kong / Kuaishou / UC San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>请求内下标随候选排序变化，无法稳定表示全库物品，训练与解码必须使用可映射目录的全局路径。列表奖励也应针对实际生成身份，而非借测试答案修补非法码。本地代理不包含完整全局语言生成训练时，应按实际范围描述。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>本请求编号三是相机，下次编号三是帐篷；把三当全局 token 会让模型学到冲突含义，无法稳定生成池外物品。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.25291">原论文</a> · <a href="../../../../reproductions/2604.25291-glorank/">实现解读</a> · <a href="#qa-418c8e5487031517">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dual-rerank" data-paper-title="Dual-Rerank: Fusing Sequential Dependencies and Utility for Generative Reranking" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Dual-Rerank: Fusing Sequential Dependencies and Utility for Generative Reranking 搜广推与 LLM 应用 Kuaishou Technology 2026-04-08 AR 教师学习物品间顺序依赖，NAR 学生并行估计名次；效用蒸馏把效果与延迟共同写入训练目标。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 dual-rerank 核心机制；相对 NDCG@10 +10.66%。  reranking knowledge-distillation listwise-rl serving 搜广推 重排、展示与长期价值 Dual-Rerank 为什么分别使用 AR 教师与 NAR 学生？ 教师逐项条件化，适合学习前缀与顺序依赖；学生并行估计名次，减轻实时解码成本。训练把教师分布与效用迁给学生，服务不重复运行完整教师。并行输出仍需检查去重与位置一致性，也不能假定蒸馏保存全部教师能力。 示意：教师先选基础教程再选进阶内容，学生学习这种偏好后一次给多个位置评分；它不需要在线再逐项复制教师搜索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-dual-rerank-e775c831" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-002570e2a9cfb086">Dual-Rerank 为什么分别使用 AR 教师与 NAR 学生？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adual-rerank">Dual-Rerank: Fusing Sequential Dependencies and Utility for Generative Reranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>教师逐项条件化，适合学习前缀与顺序依赖；学生并行估计名次，减轻实时解码成本。训练把教师分布与效用迁给学生，服务不重复运行完整教师。并行输出仍需检查去重与位置一致性，也不能假定蒸馏保存全部教师能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教师先选基础教程再选进阶内容，学生学习这种偏好后一次给多个位置评分；它不需要在线再逐项复制教师搜索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.07420">原论文</a> · <a href="../../../../reproductions/2604.07420-dual-rerank/">实现解读</a> · <a href="#qa-002570e2a9cfb086">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dual-rerank" data-paper-title="Dual-Rerank: Fusing Sequential Dependencies and Utility for Generative Reranking" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Dual-Rerank: Fusing Sequential Dependencies and Utility for Generative Reranking 搜广推与 LLM 应用 Kuaishou Technology 2026-04-08 AR 教师学习物品间顺序依赖，NAR 学生并行估计名次；效用蒸馏把效果与延迟共同写入训练目标。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 dual-rerank 核心机制；相对 NDCG@10 +10.66%。  reranking knowledge-distillation listwise-rl serving 搜广推 重排、展示与长期价值 Dual-Rerank的非自回归学生并行输出，怎样吸收自回归教师的顺序依赖？ 教师逐项条件化已有前缀，能学习列表中物品之间的作用，但服务成本随生成步骤增加。学生通过排序分布与utility蒸馏，把教师的顺序偏好压入可并行的名次估计，减少上线逐步调用。蒸馏只能近似教师依赖，并不使并行学生天然等价于每个前缀都重新计算的自回归模型。 示意：教师知道先展示教程会改变后面器材的价值，学生学习这种整体名次模式后一次给出列表；遇到新组合时仍可能无法完全复现教师的逐步判断。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dual-rerank" data-paper-title="Dual-Rerank: Fusing Sequential Dependencies and Utility for Generative Reranking" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Dual-Rerank: Fusing Sequential Dependencies and Utility for Generative Reranking 搜广推与 LLM 应用 Kuaishou Technology 2026-04-08 AR 教师学习物品间顺序依赖，NAR 学生并行估计名次；效用蒸馏把效果与延迟共同写入训练目标。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 dual-rerank 核心机制；相对 NDCG@10 +10.66%。  reranking knowledge-distillation listwise-rl serving 搜广推 重排、展示与长期价值 效用蒸馏与只拟合 AR 概率，相比允许怎样的学生取舍？ KL 关注分布接近，效用项让质量与服务约束共同参与学生目标，容许有限偏离教师以满足实际成本。效用代理若错误也会教坏学生，不能据目标里有延迟一词就认定真实服务更快；两种贡献应分别检验。 示意：学生可优先保留影响列表价值的关系，而不精确拟合所有尾部概率；若效用只奖励速度，也可能变成很快但无关的输出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-6793aecc3c187e00">效用蒸馏与只拟合 AR 概率，相比允许怎样的学生取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adual-rerank">Dual-Rerank: Fusing Sequential Dependencies and Utility for Generative Reranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>KL 关注分布接近，效用项让质量与服务约束共同参与学生目标，容许有限偏离教师以满足实际成本。效用代理若错误也会教坏学生，不能据目标里有延迟一词就认定真实服务更快；两种贡献应分别检验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>学生可优先保留影响列表价值的关系，而不精确拟合所有尾部概率；若效用只奖励速度，也可能变成很快但无关的输出。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.07420">原论文</a> · <a href="../../../../reproductions/2604.07420-dual-rerank/">实现解读</a> · <a href="#qa-6793aecc3c187e00">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dual-rerank" data-paper-title="Dual-Rerank: Fusing Sequential Dependencies and Utility for Generative Reranking" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Dual-Rerank: Fusing Sequential Dependencies and Utility for Generative Reranking 搜广推与 LLM 应用 Kuaishou Technology 2026-04-08 AR 教师学习物品间顺序依赖，NAR 学生并行估计名次；效用蒸馏把效果与延迟共同写入训练目标。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 dual-rerank 核心机制；相对 NDCG@10 +10.66%。  reranking knowledge-distillation listwise-rl serving 搜广推 重排、展示与长期价值 AR 与 NAR 做 KL 时，为什么候选、位置与 mask 需要同义对齐？ 教师每步受已选前缀约束，学生位置头可能并行看全部候选；蒸馏应明确比较同一事件空间，padding 和已选项处理一致。不能把最终教师分数复制给每个位置就声称学到顺序。候选列顺序错位时形状相同也不构成有效监督。 示意：教师第二位已排除第一位电影，学生若仍在全库归一，概率分母不同；必须定义映射，而非直接相减两个同长度数组。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-843d902d26c1e784">AR 与 NAR 做 KL 时，为什么候选、位置与 mask 需要同义对齐？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adual-rerank">Dual-Rerank: Fusing Sequential Dependencies and Utility for Generative Reranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>教师每步受已选前缀约束，学生位置头可能并行看全部候选；蒸馏应明确比较同一事件空间，padding 和已选项处理一致。不能把最终教师分数复制给每个位置就声称学到顺序。候选列顺序错位时形状相同也不构成有效监督。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教师第二位已排除第一位电影，学生若仍在全库归一，概率分母不同；必须定义映射，而非直接相减两个同长度数组。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.07420">原论文</a> · <a href="../../../../reproductions/2604.07420-dual-rerank/">实现解读</a> · <a href="#qa-843d902d26c1e784">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:safro" data-paper-title="SaFRO: Satisfaction-Aware Fusion via Dual-Relative Policy Optimization for Short-Video Search" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="SaFRO: Satisfaction-Aware Fusion via Dual-Relative Policy Optimization for Short-Video Search 搜广推与 LLM 应用 Kuaishou Technology 2026-03-20 满意度 reward 同时建模即时互动与长期留存，Dual-Relative PO 在组内和任务间归一化优势，关系门控融合多搜索目标。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 safro 核心机制，相对 NDCG@10 +81.86%。  search-ranking reinforcement-learning multi-task-learning 搜广推 重排、展示与长期价值 SaFRO为什么把满意度连接即时互动与长期留存？ 单次点击不代表后续满意，综合奖励希望让多目标搜索融合兼顾当下与长期。观测定义和延迟反馈很重要，代理奖励不能直接当真实留存因果效果。 例如视频引起点击却让用户马上离开，与看后持续回访的价值不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-safro-95b49eda" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-926f0f190e18ffa3">SaFRO为什么把满意度连接即时互动与长期留存？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asafro">SaFRO: Satisfaction-Aware Fusion via Dual-Relative Policy Optimization for Short-Video Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单次点击不代表后续满意，综合奖励希望让多目标搜索融合兼顾当下与长期。观测定义和延迟反馈很重要，代理奖励不能直接当真实留存因果效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如视频引起点击却让用户马上离开，与看后持续回访的价值不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.19585">原论文</a> · <a href="../../../../reproductions/2603.19585-safro/">实现解读</a> · <a href="#qa-926f0f190e18ffa3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:safro" data-paper-title="SaFRO: Satisfaction-Aware Fusion via Dual-Relative Policy Optimization for Short-Video Search" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="SaFRO: Satisfaction-Aware Fusion via Dual-Relative Policy Optimization for Short-Video Search 搜广推与 LLM 应用 Kuaishou Technology 2026-03-20 满意度 reward 同时建模即时互动与长期留存，Dual-Relative PO 在组内和任务间归一化优势，关系门控融合多搜索目标。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 safro 核心机制，相对 NDCG@10 +81.86%。  search-ranking reinforcement-learning multi-task-learning 搜广推 重排、展示与长期价值 SAFRO 为什么在组内和任务间都做相对 advantage 归一化？ 即时互动与长期留存的奖励尺度及难度可能不同，直接混合会让方差大或数值大的目标主导更新。组内归一化表达同一目标下哪些候选更好，任务间相对项再比较同一候选的多目标表现，关系门控组织搜索目标。归一化改善可比性，却不能自动决定长期价值权重，也不代表所有目标同时提升。 示意：点击分通常很密集，留存分稀疏且尺度更大。先在各自候选组里比较，再处理任务间差异，可减少模型只追逐数值最大的那一种奖励。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:safro" data-paper-title="SaFRO: Satisfaction-Aware Fusion via Dual-Relative Policy Optimization for Short-Video Search" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="SaFRO: Satisfaction-Aware Fusion via Dual-Relative Policy Optimization for Short-Video Search 搜广推与 LLM 应用 Kuaishou Technology 2026-03-20 满意度 reward 同时建模即时互动与长期留存，Dual-Relative PO 在组内和任务间归一化优势，关系门控融合多搜索目标。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 safro 核心机制，相对 NDCG@10 +81.86%。  search-ranking reinforcement-learning multi-task-learning 搜广推 重排、展示与长期价值 Dual-Relative优势与只在同题组标准化有何区别？ 它同时使用组内与任务间相对信息，关系门控再处理不同目标融合。两个统计轴不能混成单一全局均值，避免把任务难度与回答质量变化混淆。 例如某类任务整体奖励低，不能只因量纲差就被长期忽视。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-467e8fa083cd8a30">Dual-Relative优势与只在同题组标准化有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asafro">SaFRO: Satisfaction-Aware Fusion via Dual-Relative Policy Optimization for Short-Video Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它同时使用组内与任务间相对信息，关系门控再处理不同目标融合。两个统计轴不能混成单一全局均值，避免把任务难度与回答质量变化混淆。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某类任务整体奖励低，不能只因量纲差就被长期忽视。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.19585">原论文</a> · <a href="../../../../reproductions/2603.19585-safro/">实现解读</a> · <a href="#qa-467e8fa083cd8a30">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:safro" data-paper-title="SaFRO: Satisfaction-Aware Fusion via Dual-Relative Policy Optimization for Short-Video Search" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="SaFRO: Satisfaction-Aware Fusion via Dual-Relative Policy Optimization for Short-Video Search 搜广推与 LLM 应用 Kuaishou Technology 2026-03-20 满意度 reward 同时建模即时互动与长期留存，Dual-Relative PO 在组内和任务间归一化优势，关系门控融合多搜索目标。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 safro 核心机制，相对 NDCG@10 +81.86%。  search-ranking reinforcement-learning multi-task-learning 搜广推 重排、展示与长期价值 SaFRO本地MovieLens协议能复刻短视频留存信号吗？ 不能，公开全库排序只检验代理核心计算，没有私有搜索、留存和在线分桶。需明确奖励轴与样本任务身份，保留负结果，不把同seed差写成线上A/B提升。 例如电影离线命中率不是用户次日回访率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-bfe6bd5eec699a5c">SaFRO本地MovieLens协议能复刻短视频留存信号吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asafro">SaFRO: Satisfaction-Aware Fusion via Dual-Relative Policy Optimization for Short-Video Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，公开全库排序只检验代理核心计算，没有私有搜索、留存和在线分桶。需明确奖励轴与样本任务身份，保留负结果，不把同seed差写成线上A/B提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如电影离线命中率不是用户次日回访率。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.19585">原论文</a> · <a href="../../../../reproductions/2603.19585-safro/">实现解读</a> · <a href="#qa-bfe6bd5eec699a5c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cgr" data-paper-title="Constraint-Aware Generative Re-ranking for Multi-Objective Optimization in Advertising Feeds" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Constraint-Aware Generative Re-ranking for Multi-Objective Optimization in Advertising Feeds 搜广推与 LLM 应用 Bilibili 2026-03-04 CGR 用一个网络同时完成序列生成和奖励估计，将广告位、广告负载等业务规则直接写入自回归解码；约束感知奖励剪枝提前排除不可行分支，避免生成后的启发式修补。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05715，相对变化 +5.82%。本地代理目标与论文生产任务不同，不能外推线上 lift。  advertising generative-reranking constraint-optimization 搜广推 重排、展示与长期价值 CGR 把生成与奖励估计放在同一网络里，主要想统一哪两个决策？ 模型既提出下一项，也估计加入后的业务价值，使序列生成受已有前缀、广告位与负载规则共同影响。可行集合限制能选什么，奖励决定合法项之间怎样取舍。统一网络不是取消业务约束，更不是把奖励高视为自动合法。 示意：当前屏已达到广告上限，价值头再看好某广告也不能生成；在剩余自然内容里才继续按相关性与列表价值选择。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-cgr-09571847" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d186e3d75468b242">CGR 把生成与奖励估计放在同一网络里，主要想统一哪两个决策？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acgr">Constraint-Aware Generative Re-ranking for Multi-Objective Optimization in Advertising Feeds</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Bilibili</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>模型既提出下一项，也估计加入后的业务价值，使序列生成受已有前缀、广告位与负载规则共同影响。可行集合限制能选什么，奖励决定合法项之间怎样取舍。统一网络不是取消业务约束，更不是把奖励高视为自动合法。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>当前屏已达到广告上限，价值头再看好某广告也不能生成；在剩余自然内容里才继续按相关性与列表价值选择。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.04227">原论文</a> · <a href="../../../../reproductions/2603.04227-cgr/">实现解读</a> · <a href="#qa-d186e3d75468b242">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cgr" data-paper-title="Constraint-Aware Generative Re-ranking for Multi-Objective Optimization in Advertising Feeds" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Constraint-Aware Generative Re-ranking for Multi-Objective Optimization in Advertising Feeds 搜广推与 LLM 应用 Bilibili 2026-03-04 CGR 用一个网络同时完成序列生成和奖励估计，将广告位、广告负载等业务规则直接写入自回归解码；约束感知奖励剪枝提前排除不可行分支，避免生成后的启发式修补。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05715，相对变化 +5.82%。本地代理目标与论文生产任务不同，不能外推线上 lift。  advertising generative-reranking constraint-optimization 搜广推 重排、展示与长期价值 CGR把广告负载约束放进解码，和列表生成后再删掉多余广告有什么不同？ 事后删除会改变上下文和剩余配额，原来为某个前缀估计的价值可能不再成立。CGR在逐步生成时维护可行集合，并结合奖励估计提前剪去不可行分支，使搜索预算集中在满足业务规则的列表上。它优化的是受约束的整体选择，不能把高分但不可执行的列表当作有效输出。 示意：五个位置最多允许两个广告，前两步已用满配额时，后续直接屏蔽广告；若先生成四个广告再删，剩余位置和原预测列表已不是同一对象。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cgr" data-paper-title="Constraint-Aware Generative Re-ranking for Multi-Objective Optimization in Advertising Feeds" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Constraint-Aware Generative Re-ranking for Multi-Objective Optimization in Advertising Feeds 搜广推与 LLM 应用 Bilibili 2026-03-04 CGR 用一个网络同时完成序列生成和奖励估计，将广告位、广告负载等业务规则直接写入自回归解码；约束感知奖励剪枝提前排除不可行分支，避免生成后的启发式修补。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05715，相对变化 +5.82%。本地代理目标与论文生产任务不同，不能外推线上 lift。  advertising generative-reranking constraint-optimization 搜广推 重排、展示与长期价值 CGR 的约束感知剪枝与固定单品排序，有什么前缀依赖差别？ 固定排序认为候选价值不随已选项改变，CGR 每步根据前缀更新可行集合与奖励，因此位置和数量规则直接改变后续选择。它可减少事后修补，却需要可靠价值估计及搜索预算，不能据一次代理比较证明全局最优列表。 示意：第一位已经放广告，第二位因间隔规则只能选自然内容；普通单品分数不变，而前缀可行集合会立刻变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f174d05b9d0e95e6">CGR 的约束感知剪枝与固定单品排序，有什么前缀依赖差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acgr">Constraint-Aware Generative Re-ranking for Multi-Objective Optimization in Advertising Feeds</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Bilibili</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定排序认为候选价值不随已选项改变，CGR 每步根据前缀更新可行集合与奖励，因此位置和数量规则直接改变后续选择。它可减少事后修补，却需要可靠价值估计及搜索预算，不能据一次代理比较证明全局最优列表。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第一位已经放广告，第二位因间隔规则只能选自然内容；普通单品分数不变，而前缀可行集合会立刻变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.04227">原论文</a> · <a href="../../../../reproductions/2603.04227-cgr/">实现解读</a> · <a href="#qa-f174d05b9d0e95e6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cgr" data-paper-title="Constraint-Aware Generative Re-ranking for Multi-Objective Optimization in Advertising Feeds" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Constraint-Aware Generative Re-ranking for Multi-Objective Optimization in Advertising Feeds 搜广推与 LLM 应用 Bilibili 2026-03-04 CGR 用一个网络同时完成序列生成和奖励估计，将广告位、广告负载等业务规则直接写入自回归解码；约束感知奖励剪枝提前排除不可行分支，避免生成后的启发式修补。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05715，相对变化 +5.82%。本地代理目标与论文生产任务不同，不能外推线上 lift。  advertising generative-reranking constraint-optimization 搜广推 重排、展示与长期价值 CGR 的 F(y&lt;t) 在实现中应随着哪一步更新？ 每次选定新项后都要更新前缀、负载和位置状态，再构造下一步合法集合，保证剪枝与实际列表一致。不能先生成整条序列再假装每步满足约束。空可行集合也应有明确终止或合法回退，不能悄悄生成违规项填满长度。 示意：还剩一个位置但广告配额已用完，应从自然内容选；若自然内容也为空，就报告或按定义终止，而非无视配额补一条广告。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-5c0ea9ddfaee5e68">CGR 的 F(y&lt;t) 在实现中应随着哪一步更新？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acgr">Constraint-Aware Generative Re-ranking for Multi-Objective Optimization in Advertising Feeds</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Bilibili</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每次选定新项后都要更新前缀、负载和位置状态，再构造下一步合法集合，保证剪枝与实际列表一致。不能先生成整条序列再假装每步满足约束。空可行集合也应有明确终止或合法回退，不能悄悄生成违规项填满长度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>还剩一个位置但广告配额已用完，应从自然内容选；若自然内容也为空，就报告或按定义终止，而非无视配额补一条广告。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.04227">原论文</a> · <a href="../../../../reproductions/2603.04227-cgr/">实现解读</a> · <a href="#qa-5c0ea9ddfaee5e68">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ltv-video-ranking" data-paper-title="A Long-term Value Prediction Framework In Video Ranking" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="A Long-term Value Prediction Framework In Video Ranking 搜广推与 LLM 应用 Alibaba Group / Tsinghua University 2026-02-19 PDQ 消除位置偏差，归因模块分配会话内长期价值，作者周期任务再引入跨日优质创作者价值。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 ltv-video-ranking 核心机制，相对 NDCG@10 +9.73%。  ranking long-term-value debiasing 搜广推 重排、展示与长期价值 LTV Video Ranking 为什么先校正位置再分配会话长期价值？ 展示位置影响观看与互动，未校正时前位内容可能获得不应归于质量的信用。PDQ 将不同位置结果对齐，再汇总会话与跨日创作者价值，减少把位置机会误当长期贡献。分位校正仍依分布假设，不等于所有曝光混杂都被消除。 示意：第一位视频比第五位更易被看，不能把全部差值归于作者优质；先对齐位置条件，再比较它带来的后续消费。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-ltv-video-ranking-a90843c2" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ec0e6682983c183a">LTV Video Ranking 为什么先校正位置再分配会话长期价值？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Altv-video-ranking">A Long-term Value Prediction Framework In Video Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group / Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>展示位置影响观看与互动，未校正时前位内容可能获得不应归于质量的信用。PDQ 将不同位置结果对齐，再汇总会话与跨日创作者价值，减少把位置机会误当长期贡献。分位校正仍依分布假设，不等于所有曝光混杂都被消除。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第一位视频比第五位更易被看，不能把全部差值归于作者优质；先对齐位置条件，再比较它带来的后续消费。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.17058">原论文</a> · <a href="../../../../reproductions/2602.17058-ltv-video-ranking/">实现解读</a> · <a href="#qa-ec0e6682983c183a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ltv-video-ranking" data-paper-title="A Long-term Value Prediction Framework In Video Ranking" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="A Long-term Value Prediction Framework In Video Ranking 搜广推与 LLM 应用 Alibaba Group / Tsinghua University 2026-02-19 PDQ 消除位置偏差，归因模块分配会话内长期价值，作者周期任务再引入跨日优质创作者价值。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 ltv-video-ranking 核心机制，相对 NDCG@10 +9.73%。  ranking long-term-value debiasing 搜广推 重排、展示与长期价值 LTV视频排序为什么先处理位置偏差，再把会话与跨日创作者价值纳入目标？ 前排内容更容易被看到，直接把观测互动当长期价值可能奖励展示机会而非真正贡献。位置校正先尽量对齐可比反馈，再通过会话归因与作者周期任务表达更长时间范围的价值。位置分位映射和长期归因各有假设，不能把两者叠加后的分数直接解释成已识别的因果留存增量。 示意：一个创作者总被放首位因而互动高，另一个常在后排；先控制展示机会，再看谁带来后续持续消费，才不至于把排位优势误当长期内容价值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ltv-video-ranking" data-paper-title="A Long-term Value Prediction Framework In Video Ranking" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="A Long-term Value Prediction Framework In Video Ranking 搜广推与 LLM 应用 Alibaba Group / Tsinghua University 2026-02-19 PDQ 消除位置偏差，归因模块分配会话内长期价值，作者周期任务再引入跨日优质创作者价值。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 ltv-video-ranking 核心机制，相对 NDCG@10 +9.73%。  ranking long-term-value debiasing 搜广推 重排、展示与长期价值 长期创作者价值与只按单条观看秒数排序，相比奖励单位有何不同？ 单条秒数反映即时消费，作者周期任务看跨日持续价值，可能鼓励稳定内容供给而非一次吸睛。两种价值需要明确融合，长期代理也可能偏向既有头部作者。机制更长远不意味着已验证留存或生态改善，来源公开代理不含真实作者周期。 示意：一条夸张视频短期长看，但持续优质系列让用户多日返回；排序目标若只看当前秒数，就难奖励后一种贡献。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1c2041aa0f275a2e">长期创作者价值与只按单条观看秒数排序，相比奖励单位有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Altv-video-ranking">A Long-term Value Prediction Framework In Video Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group / Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单条秒数反映即时消费，作者周期任务看跨日持续价值，可能鼓励稳定内容供给而非一次吸睛。两种价值需要明确融合，长期代理也可能偏向既有头部作者。机制更长远不意味着已验证留存或生态改善，来源公开代理不含真实作者周期。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一条夸张视频短期长看，但持续优质系列让用户多日返回；排序目标若只看当前秒数，就难奖励后一种贡献。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.17058">原论文</a> · <a href="../../../../reproductions/2602.17058-ltv-video-ranking/">实现解读</a> · <a href="#qa-1c2041aa0f275a2e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ltv-video-ranking" data-paper-title="A Long-term Value Prediction Framework In Video Ranking" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="A Long-term Value Prediction Framework In Video Ranking 搜广推与 LLM 应用 Alibaba Group / Tsinghua University 2026-02-19 PDQ 消除位置偏差，归因模块分配会话内长期价值，作者周期任务再引入跨日优质创作者价值。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 ltv-video-ranking 核心机制，相对 NDCG@10 +9.73%。  ranking long-term-value debiasing 搜广推 重排、展示与长期价值 PDQ 的分布映射为何必须区分原位置分布与目标参考分布？ 先在候选原位置条件分布求分位，再经统一参考分布逆映射，才表达可比较尺度；若两步都用同一原分布会近似还原原值。经验分布应从允许数据拟合，不能用测试后行为调参。缺少真实位置日志时只能做明确代理。 示意：第五位观看在该位置属前百分之十，映到参考位置对应值；若直接把第五位分位再逆映回第五位，就没有完成跨位置对齐。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-284c94dfb453b29c">PDQ 的分布映射为何必须区分原位置分布与目标参考分布？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Altv-video-ranking">A Long-term Value Prediction Framework In Video Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group / Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>先在候选原位置条件分布求分位，再经统一参考分布逆映射，才表达可比较尺度；若两步都用同一原分布会近似还原原值。经验分布应从允许数据拟合，不能用测试后行为调参。缺少真实位置日志时只能做明确代理。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第五位观看在该位置属前百分之十，映到参考位置对应值；若直接把第五位分位再逆映回第五位，就没有完成跨位置对齐。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.17058">原论文</a> · <a href="../../../../reproductions/2602.17058-ltv-video-ranking/">实现解读</a> · <a href="#qa-284c94dfb453b29c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:spatial-ads" data-paper-title="Online Advertising with Spatial Interactions" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Online Advertising with Spatial Interactions 搜广推与 LLM 应用 Google Research 2026-02-12 传统逐位置竞价忽略屏幕上的空间干扰。论文将最近邻外部性问题约化到分组伪圆盘选择，再将LP解舍入为可行圆盘集合；同时研究可分解价值的简单拍卖、二维PTAS与乘积距离模型的困难性。实现范围为v1 §2.2 Algorithm1及Eq2。 论文没有完整训练实验，故full_experiment_status=not_applicable_theoretical_paper，不伪造“高成本不复现”理由。属于L1机制诊断，不是线上广告收益。自建3点度量、3个圆盘的数学测试；检查LP可行、所有采样满足约束II，并以独立种子检验边际保留概率接近。属于L1机制诊断，不是线上广告收益。CPU无需GPU；稳定记录见metrics/component-cpu-seed42.json。  空间外部性与广告分配 LP随机舍入 搜广推 重排、展示与长期价值 Spatial Ads为什么把屏幕位置之间的干扰建模？ 一个广告的价值可能受邻近广告影响，独立位置竞价忽略空间外部性。分组圆盘与覆盖约束描述可兼容选择，再通过LP和随机舍入得到可行集合。 例如两条相邻大广告互相遮抢注意，单个位置价值不能简单相加。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-spatial-ads-1dbea82c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5765da49c1050335">Spatial Ads为什么把屏幕位置之间的干扰建模？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aspatial-ads">Online Advertising with Spatial Interactions</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一个广告的价值可能受邻近广告影响，独立位置竞价忽略空间外部性。分组圆盘与覆盖约束描述可兼容选择，再通过LP和随机舍入得到可行集合。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两条相邻大广告互相遮抢注意，单个位置价值不能简单相加。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12481">原论文</a> · <a href="../../../../recommendation-components/2602.12481-spatial-ads/">实现解读</a> · <a href="#qa-5765da49c1050335">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:spatial-ads" data-paper-title="Online Advertising with Spatial Interactions" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Online Advertising with Spatial Interactions 搜广推与 LLM 应用 Google Research 2026-02-12 传统逐位置竞价忽略屏幕上的空间干扰。论文将最近邻外部性问题约化到分组伪圆盘选择，再将LP解舍入为可行圆盘集合；同时研究可分解价值的简单拍卖、二维PTAS与乘积距离模型的困难性。实现范围为v1 §2.2 Algorithm1及Eq2。 论文没有完整训练实验，故full_experiment_status=not_applicable_theoretical_paper，不伪造“高成本不复现”理由。属于L1机制诊断，不是线上广告收益。自建3点度量、3个圆盘的数学测试；检查LP可行、所有采样满足约束II，并以独立种子检验边际保留概率接近。属于L1机制诊断，不是线上广告收益。CPU无需GPU；稳定记录见metrics/component-cpu-seed42.json。  空间外部性与广告分配 LP随机舍入 搜广推 重排、展示与长期价值 Spatial Ads 的 LP 舍入为什么针对整个原始采样集合判冲突，而不是按贪心已选集合逐个接受？ 圆盘选择同时受空间冲突与同组约束，独立采样后的保留概率修正基于原始采样事件推导。若改成贪心逐个接受，后面的条件分布与冲突概率就变了，不能沿用原保证。真正求解 LP 并按规定舍入，是这里的算法核心；本地仅做小规模数学诊断，未验证线上广告收益。 示意：两个广告圆盘互相冲突，贪心先留下甲会改变乙面对的条件。原算法先固定整份随机采样，再据其中所有冲突决定保留，不能把二者当作同一个过程。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:spatial-ads" data-paper-title="Online Advertising with Spatial Interactions" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Online Advertising with Spatial Interactions 搜广推与 LLM 应用 Google Research 2026-02-12 传统逐位置竞价忽略屏幕上的空间干扰。论文将最近邻外部性问题约化到分组伪圆盘选择，再将LP解舍入为可行圆盘集合；同时研究可分解价值的简单拍卖、二维PTAS与乘积距离模型的困难性。实现范围为v1 §2.2 Algorithm1及Eq2。 论文没有完整训练实验，故full_experiment_status=not_applicable_theoretical_paper，不伪造“高成本不复现”理由。属于L1机制诊断，不是线上广告收益。自建3点度量、3个圆盘的数学测试；检查LP可行、所有采样满足约束II，并以独立种子检验边际保留概率接近。属于L1机制诊断，不是线上广告收益。CPU无需GPU；稳定记录见metrics/component-cpu-seed42.json。  空间外部性与广告分配 LP随机舍入 搜广推 重排、展示与长期价值 真实LP加两阶段舍入与贪心逐个放广告有什么不同？ LP处理分数可行域，采样后冲突针对原整个采样集，再二次稀释；贪心只看已保留集合会改变选择概率和保证条件。不能用启发式兜底冒充原算法。 例如某候选虽最终没留，若在原采样集里冲突仍影响规定事件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-85443f4bcd96a86e">真实LP加两阶段舍入与贪心逐个放广告有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aspatial-ads">Online Advertising with Spatial Interactions</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>LP处理分数可行域，采样后冲突针对原整个采样集，再二次稀释；贪心只看已保留集合会改变选择概率和保证条件。不能用启发式兜底冒充原算法。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某候选虽最终没留，若在原采样集里冲突仍影响规定事件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12481">原论文</a> · <a href="../../../../recommendation-components/2602.12481-spatial-ads/">实现解读</a> · <a href="#qa-85443f4bcd96a86e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:spatial-ads" data-paper-title="Online Advertising with Spatial Interactions" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Online Advertising with Spatial Interactions 搜广推与 LLM 应用 Google Research 2026-02-12 传统逐位置竞价忽略屏幕上的空间干扰。论文将最近邻外部性问题约化到分组伪圆盘选择，再将LP解舍入为可行圆盘集合；同时研究可分解价值的简单拍卖、二维PTAS与乘积距离模型的困难性。实现范围为v1 §2.2 Algorithm1及Eq2。 论文没有完整训练实验，故full_experiment_status=not_applicable_theoretical_paper，不伪造“高成本不复现”理由。属于L1机制诊断，不是线上广告收益。自建3点度量、3个圆盘的数学测试；检查LP可行、所有采样满足约束II，并以独立种子检验边际保留概率接近。属于L1机制诊断，不是线上广告收益。CPU无需GPU；稳定记录见metrics/component-cpu-seed42.json。  空间外部性与广告分配 LP随机舍入 搜广推 重排、展示与长期价值 圆盘边界与采样概率不合法时怎样处理？ 覆盖用严格距离小于半径，不含边界；距离需满足协议且稀释概率合法，不满足就失败。当前用真实HiGHS LP，未复现论文所有拍卖或二维PTAS结论。 例如概率算到大于一不能直接clip后继续声称相同舍入分布。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e4b1f33f48797fac">圆盘边界与采样概率不合法时怎样处理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aspatial-ads">Online Advertising with Spatial Interactions</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>覆盖用严格距离小于半径，不含边界；距离需满足协议且稀释概率合法，不满足就失败。当前用真实HiGHS LP，未复现论文所有拍卖或二维PTAS结论。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如概率算到大于一不能直接clip后继续声称相同舍入分布。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12481">原论文</a> · <a href="../../../../recommendation-components/2602.12481-spatial-ads/">实现解读</a> · <a href="#qa-e4b1f33f48797fac">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hcub" data-paper-title="Hierarchical Contextual Uplift Bandits for Catalog Personalization" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Hierarchical Contextual Uplift Bandits for Catalog Personalization 搜广推与 LLM 应用 Dream11 2026-01-20 在用户与系统上下文树上动态选择粒度，并让父节点奖励向稀疏子节点继承以改善冷启动；策略直接估计动作的增量收益，而不是只拟合观察到的绝对点击。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04886，相对变化 -9.53%。本地代理目标与论文生产任务不同，不能外推线上 lift。  bandit uplift-modeling catalog-personalization 搜广推 重排、展示与长期价值 HCUB 的上下文树为什么需要动态选择粗细粒度？ 细节点更贴近个体场景却样本稀少，父节点数据多但更粗。动态粒度与奖励继承在冷启动时借用较稳统计，数据积累后增加本地权重。它不是固定人群标签，树结构与混合系数也会影响偏差，不能把细分越多当越准确。 示意：新用户的细分节点只有两次反馈，先借上层群体估计；积累百次后再更多依赖本地，避免两次偶然点击决定长期策略。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-hcub-b171df10" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6d31f882b2fed638">HCUB 的上下文树为什么需要动态选择粗细粒度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahcub">Hierarchical Contextual Uplift Bandits for Catalog Personalization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dream11</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>细节点更贴近个体场景却样本稀少，父节点数据多但更粗。动态粒度与奖励继承在冷启动时借用较稳统计，数据积累后增加本地权重。它不是固定人群标签，树结构与混合系数也会影响偏差，不能把细分越多当越准确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新用户的细分节点只有两次反馈，先借上层群体估计；积累百次后再更多依赖本地，避免两次偶然点击决定长期策略。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.14333">原论文</a> · <a href="../../../../reproductions/2601.14333-hcub/">实现解读</a> · <a href="#qa-6d31f882b2fed638">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hcub" data-paper-title="Hierarchical Contextual Uplift Bandits for Catalog Personalization" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Hierarchical Contextual Uplift Bandits for Catalog Personalization 搜广推与 LLM 应用 Dream11 2026-01-20 在用户与系统上下文树上动态选择粒度，并让父节点奖励向稀疏子节点继承以改善冷启动；策略直接估计动作的增量收益，而不是只拟合观察到的绝对点击。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04886，相对变化 -9.53%。本地代理目标与论文生产任务不同，不能外推线上 lift。  bandit uplift-modeling catalog-personalization 搜广推 重排、展示与长期价值 HCUB为什么让稀疏上下文继承父节点奖励，同时仍保留探索项？ 细粒度用户群体数据少，完全独立估计会高方差；继承父节点提供较稳定起点，随着本地反馈增加再提高专属信息权重。动作选择依据增量收益并加入不确定性探索，避免永久锁定早期看似最好的动作。层级共享也可能掩盖少数群体差异，因此不能用父节点平均值替代所有局部证据。 示意：新出现的某设备用户群只有几次反馈，可先借更大地域群体经验；后续若本地偏好不同，估计应逐渐改写，而探索让这种差异有机会被发现。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hcub" data-paper-title="Hierarchical Contextual Uplift Bandits for Catalog Personalization" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Hierarchical Contextual Uplift Bandits for Catalog Personalization 搜广推与 LLM 应用 Dream11 2026-01-20 在用户与系统上下文树上动态选择粒度，并让父节点奖励向稀疏子节点继承以改善冷启动；策略直接估计动作的增量收益，而不是只拟合观察到的绝对点击。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04886，相对变化 -9.53%。本地代理目标与论文生产任务不同，不能外推线上 lift。  bandit uplift-modeling catalog-personalization 搜广推 重排、展示与长期价值 HCUB 的增量收益加 UCB 与按绝对点击率贪心，相比探索目标有什么不同？ 增量试图判断动作相对参考改变多少，探索项补偿不确定性，而点击贪心偏向本来就高响应的场景。两者回答不同问题；因果增量需要合适数据支持，置信 bonus 也不是因果识别工具。公开电影代理无法证明真实干预收益。 示意：某高活跃群体本来就点，增动作帮助很小；低活跃但可被有效动作改善的群体才可能值得探索，而非总选最高原始 CTR。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-31e5f1063f754e80">HCUB 的增量收益加 UCB 与按绝对点击率贪心，相比探索目标有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahcub">Hierarchical Contextual Uplift Bandits for Catalog Personalization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dream11</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>增量试图判断动作相对参考改变多少，探索项补偿不确定性，而点击贪心偏向本来就高响应的场景。两者回答不同问题；因果增量需要合适数据支持，置信 bonus 也不是因果识别工具。公开电影代理无法证明真实干预收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某高活跃群体本来就点，增动作帮助很小；低活跃但可被有效动作改善的群体才可能值得探索，而非总选最高原始 CTR。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.14333">原论文</a> · <a href="../../../../reproductions/2601.14333-hcub/">实现解读</a> · <a href="#qa-31e5f1063f754e80">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hcub" data-paper-title="Hierarchical Contextual Uplift Bandits for Catalog Personalization" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Hierarchical Contextual Uplift Bandits for Catalog Personalization 搜广推与 LLM 应用 Dream11 2026-01-20 在用户与系统上下文树上动态选择粒度，并让父节点奖励向稀疏子节点继承以改善冷启动；策略直接估计动作的增量收益，而不是只拟合观察到的绝对点击。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04886，相对变化 -9.53%。本地代理目标与论文生产任务不同，不能外推线上 lift。  bandit uplift-modeling catalog-personalization 搜广推 重排、展示与长期价值 HCUB 父子奖励混合时，怎样避免稀疏子节点反向污染全部父节点？ 应明确局部估计与父级先验的更新范围，混合读取不等于把一次子反馈复制到整棵树。η 和探索不确定性要随定义使用，动作身份保持一致；没有观测的动作不能随意记失败。否则共享机制会放大噪声而非缓解冷启动。 示意：一个新子群偶然点击某动作，可更新其统计并影响合法祖先汇总，但不能给所有兄弟节点都加一次成功，假装它们也获得同样反馈。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ba7a862fd90fa644">HCUB 父子奖励混合时，怎样避免稀疏子节点反向污染全部父节点？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahcub">Hierarchical Contextual Uplift Bandits for Catalog Personalization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dream11</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>应明确局部估计与父级先验的更新范围，混合读取不等于把一次子反馈复制到整棵树。η 和探索不确定性要随定义使用，动作身份保持一致；没有观测的动作不能随意记失败。否则共享机制会放大噪声而非缓解冷启动。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个新子群偶然点击某动作，可更新其统计并影响合法祖先汇总，但不能给所有兄弟节点都加一次成功，假装它们也获得同样反馈。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.14333">原论文</a> · <a href="../../../../reproductions/2601.14333-hcub/">实现解读</a> · <a href="#qa-ba7a862fd90fa644">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:harmonrank" data-paper-title="Rethinking Multi-objective Ranking Ensemble in Recommender System: From Score Fusion to Rank Consistency" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Rethinking Multi-objective Ranking Ensemble in Recommender System: From Score Fusion to Rank Consistency 搜广推与 LLM 应用 Kuaishou Technology 2026-01-06 第一阶段将 AUC 改写为可微 rank-sum 目标，使各任务从分类分数转向排序对齐；第二阶段用目标间 self-attention 学习购买、评论等目标的依赖，再输出统一序。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05203，相对变化 -3.65%。本地代理目标与论文生产任务不同，不能外推线上 lift。  multi-objective-ranking rank-consistency ensemble 搜广推 重排、展示与长期价值 HarmonRank 为什么把各任务从分类分数转到名次关系？ 不同目标概率尺度与基准率不同，直接相加容易让某项数值主导。可微 rank-sum/AUC 先强调任务内部相对次序，再学习目标之间依赖形成统一序。名次也会丢失绝对价值幅度，不能称为所有业务量纲都已被公平保留。 示意：点击率数值大、购买率很小，直接合并可能忽略购买；先比较各自谁更优可减少尺度支配，但无法单凭名次表达收益差多少。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-harmonrank-1abfcd00" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c91d11da9694e889">HarmonRank 为什么把各任务从分类分数转到名次关系？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aharmonrank">Rethinking Multi-objective Ranking Ensemble in Recommender System: From Score Fusion to Rank Consistency</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同目标概率尺度与基准率不同，直接相加容易让某项数值主导。可微 rank-sum/AUC 先强调任务内部相对次序，再学习目标之间依赖形成统一序。名次也会丢失绝对价值幅度，不能称为所有业务量纲都已被公平保留。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>点击率数值大、购买率很小，直接合并可能忽略购买；先比较各自谁更优可减少尺度支配，但无法单凭名次表达收益差多少。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.02955">原论文</a> · <a href="../../../../reproductions/2601.02955-harmonrank/">实现解读</a> · <a href="#qa-c91d11da9694e889">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:harmonrank" data-paper-title="Rethinking Multi-objective Ranking Ensemble in Recommender System: From Score Fusion to Rank Consistency" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Rethinking Multi-objective Ranking Ensemble in Recommender System: From Score Fusion to Rank Consistency 搜广推与 LLM 应用 Kuaishou Technology 2026-01-06 第一阶段将 AUC 改写为可微 rank-sum 目标，使各任务从分类分数转向排序对齐；第二阶段用目标间 self-attention 学习购买、评论等目标的依赖，再输出统一序。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05203，相对变化 -3.65%。本地代理目标与论文生产任务不同，不能外推线上 lift。  multi-objective-ranking rank-consistency ensemble 搜广推 重排、展示与长期价值 HarmonRank为什么先对齐各任务的名次，而不是直接融合未经处理的预测概率？ 不同目标的概率尺度与标签频率不一致，直接融合容易受校准或稀疏程度支配。可微rank-sum目标先让任务学习相对次序，再以任务间attention表示购买、评论等依赖并给出统一排序。名次对齐不保留全部绝对概率信息，适用目标和约束仍需单独检查，不能把它当通用概率校准器。 示意：购买率通常比点击率小很多，直接相加时点击可能压倒购买；先比较候选在各任务中的相对次序，再学习任务关系，可减少这种纯数值尺度支配。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:harmonrank" data-paper-title="Rethinking Multi-objective Ranking Ensemble in Recommender System: From Score Fusion to Rank Consistency" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Rethinking Multi-objective Ranking Ensemble in Recommender System: From Score Fusion to Rank Consistency 搜广推与 LLM 应用 Kuaishou Technology 2026-01-06 第一阶段将 AUC 改写为可微 rank-sum 目标，使各任务从分类分数转向排序对齐；第二阶段用目标间 self-attention 学习购买、评论等目标的依赖，再输出统一序。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05203，相对变化 -3.65%。本地代理目标与论文生产任务不同，不能外推线上 lift。  multi-objective-ranking rank-consistency ensemble 搜广推 重排、展示与长期价值 目标间 self-attention 与固定加权融合，相比如何处理冲突目标？ 固定权重预设全局取舍，attention 可依据目标表示学习依赖与条件组合，让一个目标影响另一个的使用方式。它增加适应性，也可能让高频目标主导，必须按任务与样本检查。来源本地负结果不支持把依赖建模直接等同于更高质量。 示意：高点击但低购买的商品需要不同于两项都高的处理，动态依赖可表达这种条件；简单七三加权则对两类始终使用同样系数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-2689dff0a475a4a9">目标间 self-attention 与固定加权融合，相比如何处理冲突目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aharmonrank">Rethinking Multi-objective Ranking Ensemble in Recommender System: From Score Fusion to Rank Consistency</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定权重预设全局取舍，attention 可依据目标表示学习依赖与条件组合，让一个目标影响另一个的使用方式。它增加适应性，也可能让高频目标主导，必须按任务与样本检查。来源本地负结果不支持把依赖建模直接等同于更高质量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>高点击但低购买的商品需要不同于两项都高的处理，动态依赖可表达这种条件；简单七三加权则对两类始终使用同样系数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.02955">原论文</a> · <a href="../../../../reproductions/2601.02955-harmonrank/">实现解读</a> · <a href="#qa-2689dff0a475a4a9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:harmonrank" data-paper-title="Rethinking Multi-objective Ranking Ensemble in Recommender System: From Score Fusion to Rank Consistency" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Rethinking Multi-objective Ranking Ensemble in Recommender System: From Score Fusion to Rank Consistency 搜广推与 LLM 应用 Kuaishou Technology 2026-01-06 第一阶段将 AUC 改写为可微 rank-sum 目标，使各任务从分类分数转向排序对齐；第二阶段用目标间 self-attention 学习购买、评论等目标的依赖，再输出统一序。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05203，相对变化 -3.65%。本地代理目标与论文生产任务不同，不能外推线上 lift。  multi-objective-ranking rank-consistency ensemble 搜广推 重排、展示与长期价值 实现 soft AUC 时，为什么 batch 内必须同时有正负样本并明确无效任务？ 排序目标依赖正负比较，只有一类标签的切片无法形成同义 AUC；需按约定 mask 或报告不可估，不能默认满分。目标间模块输入也应对应一致候选身份。可微近似的温度和采样影响梯度，不等于真实全数据 AUC。 示意：一批购买标签全零，不能把该任务“排序全对”记为一；应标记无可比较 pair，避免它误导第二阶段目标融合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-205f2c06bfda2ec2">实现 soft AUC 时，为什么 batch 内必须同时有正负样本并明确无效任务？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aharmonrank">Rethinking Multi-objective Ranking Ensemble in Recommender System: From Score Fusion to Rank Consistency</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>排序目标依赖正负比较，只有一类标签的切片无法形成同义 AUC；需按约定 mask 或报告不可估，不能默认满分。目标间模块输入也应对应一致候选身份。可微近似的温度和采样影响梯度，不等于真实全数据 AUC。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一批购买标签全零，不能把该任务“排序全对”记为一；应标记无可比较 pair，避免它误导第二阶段目标融合。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.02955">原论文</a> · <a href="../../../../reproductions/2601.02955-harmonrank/">实现解读</a> · <a href="#qa-205f2c06bfda2ec2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:higr" data-paper-title="HiGR: Industrial-Scale Hierarchical Generative Slate Recommendation Framework in Tencent" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="HiGR: Industrial-Scale Hierarchical Generative Slate Recommendation Framework in Tencent 搜广推与 LLM 应用 Tencent 2025-12-31 逐物品生成忽略 slate 内相互作用。HiGR 用 PCRQ-VAE 得到层级语义 ID，Hierarchical Slate Decoder 先选簇再选物品，并通过 ORPO 对齐整页偏好。 多样性更好但精度下降，未复现线上收益。Fidelity: 核心机制复现。实际学习两级 residual semantic ID，执行 coarse-to-fine slate 解码和 ORPO 风格偏好重排。MovieLens 单物品 next-item 目标并非视频 slate 反馈；本地 k-means residual ID 不等价于生产 PCRQ-VAE。本地对照口径：相对 flat item slate 基线，实验组 NDCG@10 -12.32%。  generative-recommendation slate-recommendation semantic-id preference-optimization 搜广推 重排、展示与长期价值 HiGR 为什么在整页生成中先选语义簇再选物品？ 层级结构把大物品空间拆成粗兴趣与具体身份，页面可先组织不同簇，再细化对象，有助表达组合。粗码错误会限制后续候选，簇间覆盖也不等于相关性好。整页目标与量化质量都需检验，不能只看列表看起来更多样。 示意：先安排教程、工具和案例三个方向，再选具体内容；若误把用户需求归到娱乐簇，后续选再多不同娱乐项目也可能无关。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-higr-d87ebf0f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-75d3a4b1b9164993">HiGR 为什么在整页生成中先选语义簇再选物品？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahigr">HiGR: Industrial-Scale Hierarchical Generative Slate Recommendation Framework in Tencent</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>层级结构把大物品空间拆成粗兴趣与具体身份，页面可先组织不同簇，再细化对象，有助表达组合。粗码错误会限制后续候选，簇间覆盖也不等于相关性好。整页目标与量化质量都需检验，不能只看列表看起来更多样。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先安排教程、工具和案例三个方向，再选具体内容；若误把用户需求归到娱乐簇，后续选再多不同娱乐项目也可能无关。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2512.24787">原论文</a> · <a href="../../../../reproductions/2512.24787-higr/">实现解读</a> · <a href="#qa-75d3a4b1b9164993">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:higr" data-paper-title="HiGR: Industrial-Scale Hierarchical Generative Slate Recommendation Framework in Tencent" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="HiGR: Industrial-Scale Hierarchical Generative Slate Recommendation Framework in Tencent 搜广推与 LLM 应用 Tencent 2025-12-31 逐物品生成忽略 slate 内相互作用。HiGR 用 PCRQ-VAE 得到层级语义 ID，Hierarchical Slate Decoder 先选簇再选物品，并通过 ORPO 对齐整页偏好。 多样性更好但精度下降，未复现线上收益。Fidelity: 核心机制复现。实际学习两级 residual semantic ID，执行 coarse-to-fine slate 解码和 ORPO 风格偏好重排。MovieLens 单物品 next-item 目标并非视频 slate 反馈；本地 k-means residual ID 不等价于生产 PCRQ-VAE。本地对照口径：相对 flat item slate 基线，实验组 NDCG@10 -12.32%。  generative-recommendation slate-recommendation semantic-id preference-optimization 搜广推 重排、展示与长期价值 HiGR先选语义簇再选物品，为什么还需要整页偏好对齐？ 层级ID降低了物品定位难度，但分别选中相关物品并不保证列表互补与顺序合理。Hierarchical Slate Decoder组织粗到细生成，ORPO再用好坏整页偏好调整组合分布。偏好反馈仍只覆盖已评估组合，不能因为有层级结构就声称长尾覆盖或页面效用必然提高。 示意：簇级选择都命中运动主题，生成结果却可能全是近似跑鞋；整页偏好可教模型换入袜子或训练内容，而不只是逐个奖励主题相关。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:higr" data-paper-title="HiGR: Industrial-Scale Hierarchical Generative Slate Recommendation Framework in Tencent" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="HiGR: Industrial-Scale Hierarchical Generative Slate Recommendation Framework in Tencent 搜广推与 LLM 应用 Tencent 2025-12-31 逐物品生成忽略 slate 内相互作用。HiGR 用 PCRQ-VAE 得到层级语义 ID，Hierarchical Slate Decoder 先选簇再选物品，并通过 ORPO 对齐整页偏好。 多样性更好但精度下降，未复现线上收益。Fidelity: 核心机制复现。实际学习两级 residual semantic ID，执行 coarse-to-fine slate 解码和 ORPO 风格偏好重排。MovieLens 单物品 next-item 目标并非视频 slate 反馈；本地 k-means residual ID 不等价于生产 PCRQ-VAE。本地对照口径：相对 flat item slate 基线，实验组 NDCG@10 -12.32%。  generative-recommendation slate-recommendation semantic-id preference-optimization 搜广推 重排、展示与长期价值 HiGR 的 ORPO 与单纯页级 SFT，偏好证据怎样不同？ SFT 模仿正页面，ORPO 还用胜负页的相对 odds 调整，让模型知道哪些组合更好而非仅复制一种。偏好标签与量化结构可能有偏，不能因多样性提高就宣称总体改善。来源本地 NDCG 下降，应连同头部变化一并报告。 示意：两页单条都相关，一页重复一页互补，偏好对给出组合差别；只学其中正页未必明确惩罚另一页，ORPO 增加了相对监督。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d13d7f938c1fcfbc">HiGR 的 ORPO 与单纯页级 SFT，偏好证据怎样不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahigr">HiGR: Industrial-Scale Hierarchical Generative Slate Recommendation Framework in Tencent</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>SFT 模仿正页面，ORPO 还用胜负页的相对 odds 调整，让模型知道哪些组合更好而非仅复制一种。偏好标签与量化结构可能有偏，不能因多样性提高就宣称总体改善。来源本地 NDCG 下降，应连同头部变化一并报告。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两页单条都相关，一页重复一页互补，偏好对给出组合差别；只学其中正页未必明确惩罚另一页，ORPO 增加了相对监督。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2512.24787">原论文</a> · <a href="../../../../reproductions/2512.24787-higr/">实现解读</a> · <a href="#qa-d13d7f938c1fcfbc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:higr" data-paper-title="HiGR: Industrial-Scale Hierarchical Generative Slate Recommendation Framework in Tencent" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="HiGR: Industrial-Scale Hierarchical Generative Slate Recommendation Framework in Tencent 搜广推与 LLM 应用 Tencent 2025-12-31 逐物品生成忽略 slate 内相互作用。HiGR 用 PCRQ-VAE 得到层级语义 ID，Hierarchical Slate Decoder 先选簇再选物品，并通过 ORPO 对齐整页偏好。 多样性更好但精度下降，未复现线上收益。Fidelity: 核心机制复现。实际学习两级 residual semantic ID，执行 coarse-to-fine slate 解码和 ORPO 风格偏好重排。MovieLens 单物品 next-item 目标并非视频 slate 反馈；本地 k-means residual ID 不等价于生产 PCRQ-VAE。本地对照口径：相对 flat item slate 基线，实验组 NDCG@10 -12.32%。  generative-recommendation slate-recommendation semantic-id preference-optimization 搜广推 重排、展示与长期价值 HiGR 的概率进入 logit odds 时，为什么要明确序列概率与数值边界？ 页面概率是条件 token 概率的联合，直接连乘易下溢，应在 log 空间按定义计算；odds 又涉及一减概率，需稳定边界处理。不能拿任意未归一分数当概率。层级码映射和重复约束也要与页身份一致。 示意：长页面联合概率极小，浮点乘成零后再取 log 会无穷；用稳定 log 概率保留差异，但不能随意换成长度均值而不说明目标变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-29d8f706697c4551">HiGR 的概率进入 logit odds 时，为什么要明确序列概率与数值边界？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahigr">HiGR: Industrial-Scale Hierarchical Generative Slate Recommendation Framework in Tencent</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>页面概率是条件 token 概率的联合，直接连乘易下溢，应在 log 空间按定义计算；odds 又涉及一减概率，需稳定边界处理。不能拿任意未归一分数当概率。层级码映射和重复约束也要与页身份一致。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>长页面联合概率极小，浮点乘成零后再取 log 会无穷；用稳定 log 概率保留差异，但不能随意换成长度均值而不说明目标变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2512.24787">原论文</a> · <a href="../../../../reproductions/2512.24787-higr/">实现解读</a> · <a href="#qa-29d8f706697c4551">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:drl-put" data-paper-title="Deep Reinforcement Learning for Ranking Utility Tuning in the Ad Recommender System at Pinterest" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Deep Reinforcement Learning for Ranking Utility Tuning in the Ad Recommender System at Pinterest 搜广推与 LLM 应用 Pinterest 2025-09-05 广告排序的相关性、CTR、CVR 和收益权重通常靠人工调节。DRL-PUT 把权重组合视为动作，依据用户/请求状态选择动作，并从 logged behavior 和组合 reward 学习策略。 Fidelity: 核心机制复现。从公开交互构造带 propensity 的日志策略，并用 REINFORCE 学习效用权重动作。公开评分代理点击和收益，无法重建 Pinterest 拍卖、真实 counterfactual reward 与广告主约束。本地对照口径：相对固定 utility 权重基线，实验组 NDCG@10 +19.13%。  ads-ranking reinforcement-learning utility-tuning off-policy 搜广推 重排、展示与长期价值 DRL-PUT 为什么把 utility 权重当动作，而非直接生成物品？ 已有 CTR、CVR、相关性和收益模型继续提供候选分数，策略只决定当前请求如何组合，动作更受控也便于接入。反馈评价权重诱导出的列表结果，不能直接解释成每个物品的独立因果贡献。该方法改变配置策略，不是重建所有评分器。 示意：相同候选三份分数可由七二一或四三三权重产生不同排序，策略选择配比；商品表示和底层点击网络可以保持不变。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-drl-put-ba6d0f54" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4769e145ec181242">DRL-PUT 为什么把 utility 权重当动作，而非直接生成物品？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adrl-put">Deep Reinforcement Learning for Ranking Utility Tuning in the Ad Recommender System at Pinterest</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>已有 CTR、CVR、相关性和收益模型继续提供候选分数，策略只决定当前请求如何组合，动作更受控也便于接入。反馈评价权重诱导出的列表结果，不能直接解释成每个物品的独立因果贡献。该方法改变配置策略，不是重建所有评分器。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>相同候选三份分数可由七二一或四三三权重产生不同排序，策略选择配比；商品表示和底层点击网络可以保持不变。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2509.05292">原论文</a> · <a href="../../../../reproductions/2509.05292-drl-put/">实现解读</a> · <a href="#qa-4769e145ec181242">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:drl-put" data-paper-title="Deep Reinforcement Learning for Ranking Utility Tuning in the Ad Recommender System at Pinterest" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Deep Reinforcement Learning for Ranking Utility Tuning in the Ad Recommender System at Pinterest 搜广推与 LLM 应用 Pinterest 2025-09-05 广告排序的相关性、CTR、CVR 和收益权重通常靠人工调节。DRL-PUT 把权重组合视为动作，依据用户/请求状态选择动作，并从 logged behavior 和组合 reward 学习策略。 Fidelity: 核心机制复现。从公开交互构造带 propensity 的日志策略，并用 REINFORCE 学习效用权重动作。公开评分代理点击和收益，无法重建 Pinterest 拍卖、真实 counterfactual reward 与广告主约束。本地对照口径：相对固定 utility 权重基线，实验组 NDCG@10 +19.13%。  ads-ranking reinforcement-learning utility-tuning off-policy 搜广推 重排、展示与长期价值 DRL-PUT学习的是推荐物品本身，还是多个utility分数的组合方式？ 动作是相关性、CTR、CVR等分数的权重配置，策略依据请求状态决定如何组合已有预测器。这样可以在不替换所有底层模型的情况下适配业务取舍；离线利用日志策略概率校正动作分布差异。若某些权重在历史中几乎没被采用，就缺少可靠反馈支持，不能凭离线大权重宣称线上最优。 示意：同一批广告已有点击与转化分，策略可对探索型请求更重相关性，对明确购买请求更重转化；变化的是决策组合，而非重新生成所有广告表示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:drl-put" data-paper-title="Deep Reinforcement Learning for Ranking Utility Tuning in the Ad Recommender System at Pinterest" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Deep Reinforcement Learning for Ranking Utility Tuning in the Ad Recommender System at Pinterest 搜广推与 LLM 应用 Pinterest 2025-09-05 广告排序的相关性、CTR、CVR 和收益权重通常靠人工调节。DRL-PUT 把权重组合视为动作，依据用户/请求状态选择动作，并从 logged behavior 和组合 reward 学习策略。 Fidelity: 核心机制复现。从公开交互构造带 propensity 的日志策略，并用 REINFORCE 学习效用权重动作。公开评分代理点击和收益，无法重建 Pinterest 拍卖、真实 counterfactual reward 与广告主约束。本地对照口径：相对固定 utility 权重基线，实验组 NDCG@10 +19.13%。  ads-ranking reinforcement-learning utility-tuning off-policy 搜广推 重排、展示与长期价值 DRL-PUT 的离策略更新与直接拟合日志中最高 reward，有何分布区别？ 日志动作来自 μ，目标策略 π 的选择频率不同，概率比试图校正这种差别。忽略它会偏爱旧策略常试的动作。校正要求动作支持与可靠记录，极端比值也增加方差，并非对所有混杂自动免疫；本地公开代理不等于真实广告随机日志。 示意：旧系统几乎总用高 CTR 权重，多数高 reward 自然也来自它；这不证明其他配比无效，还需要知道各动作实际获得多少机会。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d5788a31ee9ff996">DRL-PUT 的离策略更新与直接拟合日志中最高 reward，有何分布区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adrl-put">Deep Reinforcement Learning for Ranking Utility Tuning in the Ad Recommender System at Pinterest</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>日志动作来自 μ，目标策略 π 的选择频率不同，概率比试图校正这种差别。忽略它会偏爱旧策略常试的动作。校正要求动作支持与可靠记录，极端比值也增加方差，并非对所有混杂自动免疫；本地公开代理不等于真实广告随机日志。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>旧系统几乎总用高 CTR 权重，多数高 reward 自然也来自它；这不证明其他配比无效，还需要知道各动作实际获得多少机会。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2509.05292">原论文</a> · <a href="../../../../reproductions/2509.05292-drl-put/">实现解读</a> · <a href="#qa-d5788a31ee9ff996">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:drl-put" data-paper-title="Deep Reinforcement Learning for Ranking Utility Tuning in the Ad Recommender System at Pinterest" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Deep Reinforcement Learning for Ranking Utility Tuning in the Ad Recommender System at Pinterest 搜广推与 LLM 应用 Pinterest 2025-09-05 广告排序的相关性、CTR、CVR 和收益权重通常靠人工调节。DRL-PUT 把权重组合视为动作，依据用户/请求状态选择动作，并从 logged behavior 和组合 reward 学习策略。 Fidelity: 核心机制复现。从公开交互构造带 propensity 的日志策略，并用 REINFORCE 学习效用权重动作。公开评分代理点击和收益，无法重建 Pinterest 拍卖、真实 counterfactual reward 与广告主约束。本地对照口径：相对固定 utility 权重基线，实验组 NDCG@10 +19.13%。  ads-ranking reinforcement-learning utility-tuning off-policy 搜广推 重排、展示与长期价值 计算 DRL-PUT 的 π/μ 时，日志中的动作身份为何必须和概率一一对应？ 实际执行配比、行为概率、上下文与 reward 要保持同一事件配对，否则重要性权重失去含义。μ 为零时没有支持，不能以任意小常数假装可无偏外推；基线 b 也不能读取测试结果。只存最终列表不足以还原完整离策略更新。 示意：执行七三配比却记录四六配比的概率，会给错误梯度倍数；即使 reward 和列表都真实，也无法修复这一动作日志错位。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-96e89b6778bf510d">计算 DRL-PUT 的 π/μ 时，日志中的动作身份为何必须和概率一一对应？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adrl-put">Deep Reinforcement Learning for Ranking Utility Tuning in the Ad Recommender System at Pinterest</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>实际执行配比、行为概率、上下文与 reward 要保持同一事件配对，否则重要性权重失去含义。μ 为零时没有支持，不能以任意小常数假装可无偏外推；基线 b 也不能读取测试结果。只存最终列表不足以还原完整离策略更新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>执行七三配比却记录四六配比的概率，会给错误梯度倍数；即使 reward 和列表都真实，也无法修复这一动作日志错位。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2509.05292">原论文</a> · <a href="../../../../reproductions/2509.05292-drl-put/">实现解读</a> · <a href="#qa-96e89b6778bf510d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sort-gen" data-paper-title="A Generative Re-ranking Model for List-level Multi-objective Optimization at Taobao" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="A Generative Re-ranking Model for List-level Multi-objective Optimization at Taobao 搜广推与 LLM 应用 Alibaba / Taobao &amp; Tmall 2025-05-12 传统公式或 LTR 在 item level 优化 CTR、CVR、GMV，无法建模已选前缀对后续 item 的影响。SORT-Gen 用 causal Transformer 输入 item、user、position 和上游 CTR/CVR score，在每个前缀位置预测“累计行为数是否至少达到第档”的 ordered-regression 概率，从而估计加入 item 后的列表边际价值。推理先建立 CLICK、PAY、GMV 等目标队列，把搜索空间从全部候选降到队首。 Fidelity: 核心机制复现。实际训练 causal Transformer ordered regression，并执行多目标队列、mask-driven 单次批量评分和 MMR；私有曝光与线上 kernel 缩小。MovieLens rating/genre/popularity 分别代理点击、交易、商品内容和上游 score；没有淘宝真实曝光、CVR/GMV、用户商业特征和多模态 embedding。单次调用是 PyTorch 批量路径，不等价于论文生产 19 ms kernel；本地 proxy 指标不能和线上百分比直接比较。  reranking multi-objective ordered-regression diversity 搜广推 重排、展示与长期价值 SORT-Gen为什么把列表前缀价值而非独立item分优化？ 已选内容影响下一项边际收益，独立CTR无法表达列表相互作用。模型在前缀上预测累计行为档位，选择能增加当前列表价值的候选。 例如前面已有两条相似商品，再加第三条可能不如补充另一需求。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-sort-gen-b1c957ea" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0ae30452731af4a0">SORT-Gen为什么把列表前缀价值而非独立item分优化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asort-gen">A Generative Re-ranking Model for List-level Multi-objective Optimization at Taobao</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao &amp; Tmall</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>已选内容影响下一项边际收益，独立CTR无法表达列表相互作用。模型在前缀上预测累计行为档位，选择能增加当前列表价值的候选。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如前面已有两条相似商品，再加第三条可能不如补充另一需求。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.07197">原论文</a> · <a href="../../../../reproductions/2505.07197-sort-gen/">实现解读</a> · <a href="#qa-0ae30452731af4a0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sort-gen" data-paper-title="A Generative Re-ranking Model for List-level Multi-objective Optimization at Taobao" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="A Generative Re-ranking Model for List-level Multi-objective Optimization at Taobao 搜广推与 LLM 应用 Alibaba / Taobao &amp; Tmall 2025-05-12 传统公式或 LTR 在 item level 优化 CTR、CVR、GMV，无法建模已选前缀对后续 item 的影响。SORT-Gen 用 causal Transformer 输入 item、user、position 和上游 CTR/CVR score，在每个前缀位置预测“累计行为数是否至少达到第档”的 ordered-regression 概率，从而估计加入 item 后的列表边际价值。推理先建立 CLICK、PAY、GMV 等目标队列，把搜索空间从全部候选降到队首。 Fidelity: 核心机制复现。实际训练 causal Transformer ordered regression，并执行多目标队列、mask-driven 单次批量评分和 MMR；私有曝光与线上 kernel 缩小。MovieLens rating/genre/popularity 分别代理点击、交易、商品内容和上游 score；没有淘宝真实曝光、CVR/GMV、用户商业特征和多模态 embedding。单次调用是 PyTorch 批量路径，不等价于论文生产 19 ms kernel；本地 proxy 指标不能和线上百分比直接比较。  reranking multi-objective ordered-regression diversity 搜广推 重排、展示与长期价值 SORT-Gen 为什么用累计行为数的 ordered regression 估计前缀价值，而不把单品 CTR 相加？ 单品分数忽略已选列表对下一物品的影响。ordered regression 在每个前缀预测累计行为是否达到各档，从分布估计加入候选后的边际价值；目标队列减少搜索候选，张量掩码加速批量评估，MMR 直接参与选择。它建模的是列表条件价值，仍依赖代理标签和搜索范围，不能把加速队列当作全局最优搜索。 示意：前两条已经是相似手机，再放第三条手机未必增加多少互动。模型比较加入耳机后的累计行为分布，而不是只看第三条手机独立 CTR 是否略高。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sort-gen" data-paper-title="A Generative Re-ranking Model for List-level Multi-objective Optimization at Taobao" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="A Generative Re-ranking Model for List-level Multi-objective Optimization at Taobao 搜广推与 LLM 应用 Alibaba / Taobao &amp; Tmall 2025-05-12 传统公式或 LTR 在 item level 优化 CTR、CVR、GMV，无法建模已选前缀对后续 item 的影响。SORT-Gen 用 causal Transformer 输入 item、user、position 和上游 CTR/CVR score，在每个前缀位置预测“累计行为数是否至少达到第档”的 ordered-regression 概率，从而估计加入 item 后的列表边际价值。推理先建立 CLICK、PAY、GMV 等目标队列，把搜索空间从全部候选降到队首。 Fidelity: 核心机制复现。实际训练 causal Transformer ordered regression，并执行多目标队列、mask-driven 单次批量评分和 MMR；私有曝光与线上 kernel 缩小。MovieLens rating/genre/popularity 分别代理点击、交易、商品内容和上游 score；没有淘宝真实曝光、CVR/GMV、用户商业特征和多模态 embedding。单次调用是 PyTorch 批量路径，不等价于论文生产 19 ms kernel；本地 proxy 指标不能和线上百分比直接比较。  reranking multi-objective ordered-regression diversity 搜广推 重排、展示与长期价值 MMR进入生成选择与生成后再去重有什么区别？ 选择时就权衡边际价值与相似性，会影响后续前缀；事后删除只修最后列表，可能留下空位或错过早期更优组合。两者并不等价。 例如第一步选了高重复内容，后处理删掉它也不能完全重现另一条生成路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-fb168cb5f84dbd00">MMR进入生成选择与生成后再去重有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asort-gen">A Generative Re-ranking Model for List-level Multi-objective Optimization at Taobao</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao &amp; Tmall</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>选择时就权衡边际价值与相似性，会影响后续前缀；事后删除只修最后列表，可能留下空位或错过早期更优组合。两者并不等价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如第一步选了高重复内容，后处理删掉它也不能完全重现另一条生成路径。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.07197">原论文</a> · <a href="../../../../reproductions/2505.07197-sort-gen/">实现解读</a> · <a href="#qa-fb168cb5f84dbd00">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sort-gen" data-paper-title="A Generative Re-ranking Model for List-level Multi-objective Optimization at Taobao" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="A Generative Re-ranking Model for List-level Multi-objective Optimization at Taobao 搜广推与 LLM 应用 Alibaba / Taobao &amp; Tmall 2025-05-12 传统公式或 LTR 在 item level 优化 CTR、CVR、GMV，无法建模已选前缀对后续 item 的影响。SORT-Gen 用 causal Transformer 输入 item、user、position 和上游 CTR/CVR score，在每个前缀位置预测“累计行为数是否至少达到第档”的 ordered-regression 概率，从而估计加入 item 后的列表边际价值。推理先建立 CLICK、PAY、GMV 等目标队列，把搜索空间从全部候选降到队首。 Fidelity: 核心机制复现。实际训练 causal Transformer ordered regression，并执行多目标队列、mask-driven 单次批量评分和 MMR；私有曝光与线上 kernel 缩小。MovieLens rating/genre/popularity 分别代理点击、交易、商品内容和上游 score；没有淘宝真实曝光、CVR/GMV、用户商业特征和多模态 embedding。单次调用是 PyTorch 批量路径，不等价于论文生产 19 ms kernel；本地 proxy 指标不能和线上百分比直接比较。  reranking multi-objective ordered-regression diversity 搜广推 重排、展示与长期价值 SORT-Gen本地单批模型调用等于原文19ms kernel吗？ 不等于，只是PyTorch批量mask计算路径，未包含生产优化。MovieLens评分与流行度代理点击交易及上游分，不是真GMV；prefix累计目标和候选mask须正确对齐。 例如一个批次函数只调用一次，不表示设备内部执行成本与专用kernel相同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-aecda01f5daf23a9">SORT-Gen本地单批模型调用等于原文19ms kernel吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asort-gen">A Generative Re-ranking Model for List-level Multi-objective Optimization at Taobao</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao &amp; Tmall</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不等于，只是PyTorch批量mask计算路径，未包含生产优化。MovieLens评分与流行度代理点击交易及上游分，不是真GMV；prefix累计目标和候选mask须正确对齐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个批次函数只调用一次，不表示设备内部执行成本与专用kernel相同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.07197">原论文</a> · <a href="../../../../reproductions/2505.07197-sort-gen/">实现解读</a> · <a href="#qa-aecda01f5daf23a9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cdm" data-paper-title="Contextual Distillation Model for Diversified Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Contextual Distillation Model for Diversified Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2024-06-13 先用可控 MMR 教师产生兼顾相关性与多样性的列表，再把上下文边际收益蒸馏到可低延迟服务的学生。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 cdm 核心机制；相对 NDCG@10 +1.25%。  reranking diversity knowledge-distillation 搜广推 重排、展示与长期价值 CDM 为什么把多样性理解为当前已选前缀下的边际收益？ 同一物品是否有增量价值取决于列表已有内容：第一条科幻片可能丰富，第四条相似科幻片则冗余。MMR 教师显式结合相关性与重复惩罚，学生学习该上下文收益以便低延迟服务。多样性不是给某个物品永久增加固定分数。 示意：列表已有两部同导演作品，再放第三部的边际价值可能低；若列表尚无该导演，同一影片则可能是很好的补充。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<span id="paper-recommendation-cdm-24f0cce6" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-93a791dccea8c9a7">CDM 为什么把多样性理解为当前已选前缀下的边际收益？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acdm">Contextual Distillation Model for Diversified Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一物品是否有增量价值取决于列表已有内容：第一条科幻片可能丰富，第四条相似科幻片则冗余。MMR 教师显式结合相关性与重复惩罚，学生学习该上下文收益以便低延迟服务。多样性不是给某个物品永久增加固定分数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>列表已有两部同导演作品，再放第三部的边际价值可能低；若列表尚无该导演，同一影片则可能是很好的补充。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2406.09021">原论文</a> · <a href="../../../../reproductions/2406.09021-cdm/">实现解读</a> · <a href="#qa-93a791dccea8c9a7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cdm" data-paper-title="Contextual Distillation Model for Diversified Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Contextual Distillation Model for Diversified Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2024-06-13 先用可控 MMR 教师产生兼顾相关性与多样性的列表，再把上下文边际收益蒸馏到可低延迟服务的学生。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 cdm 核心机制；相对 NDCG@10 +1.25%。  reranking diversity knowledge-distillation 搜广推 重排、展示与长期价值 CDM把MMR教师蒸馏给学生，学生为什么必须看同请求候选的上下文？ 一个物品是否被MMR选中取决于其他候选及其重复程度，单看物品本身无法恢复这种集合关系。CDM学习目标物品相对上下文的入选倾向，再与原推荐分结合，把昂贵的逐步去冗余知识转成可服务的评分。学生近似不保证完全复刻教师列表，本地缩小实验也不能推出生产多样性收益。 示意：同一段旅行视频，在十段近似视频里可能被淘汰，在全是做饭视频的列表中却很独特；不输入候选上下文，学生无法区分这两种情况。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cdm" data-paper-title="Contextual Distillation Model for Diversified Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Contextual Distillation Model for Diversified Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2024-06-13 先用可控 MMR 教师产生兼顾相关性与多样性的列表，再把上下文边际收益蒸馏到可低延迟服务的学生。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 cdm 核心机制；相对 NDCG@10 +1.25%。  reranking diversity knowledge-distillation 搜广推 重排、展示与长期价值 CDM 蒸馏与每次在线直接运行 MMR，相比节省了什么又引入什么误差？ 直接 MMR 每步根据已选集合重新计算惩罚，蒸馏学生将这种规则近似写入可快速预测的模型，减少在线迭代成本。近似可能在新候选分布或长列表下失真，需要核验精度与多样性，而非只看延迟；来源代理改进不证明教师规则已被无误复现。 示意：教师反复比较候选和已选项，学生一次近似给出边际分；若遇到训练没见过的高度重复候选，学生可能低估冗余，仍需检查。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-8bc42bf8da4f58b1">CDM 蒸馏与每次在线直接运行 MMR，相比节省了什么又引入什么误差？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acdm">Contextual Distillation Model for Diversified Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直接 MMR 每步根据已选集合重新计算惩罚，蒸馏学生将这种规则近似写入可快速预测的模型，减少在线迭代成本。近似可能在新候选分布或长列表下失真，需要核验精度与多样性，而非只看延迟；来源代理改进不证明教师规则已被无误复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教师反复比较候选和已选项，学生一次近似给出边际分；若遇到训练没见过的高度重复候选，学生可能低估冗余，仍需检查。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2406.09021">原论文</a> · <a href="../../../../reproductions/2406.09021-cdm/">实现解读</a> · <a href="#qa-8bc42bf8da4f58b1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cdm" data-paper-title="Contextual Distillation Model for Diversified Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/slates-business-value" data-search="Contextual Distillation Model for Diversified Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2024-06-13 先用可控 MMR 教师产生兼顾相关性与多样性的列表，再把上下文边际收益蒸馏到可低延迟服务的学生。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 cdm 核心机制；相对 NDCG@10 +1.25%。  reranking diversity knowledge-distillation 搜广推 重排、展示与长期价值 CDM 教师生成序列时，为什么选出一项后要更新相似度惩罚？ MMR 惩罚相对当前已选前缀的最大相似度，每次加入新项都会改变剩余候选的边际分。若一次算完固定分再排序，就不是同一上下文决策。学生训练标签也应对齐相应前缀，不能把不同阶段的收益混成一个静态单品目标。 示意：选中第一条露营教程后，另一条近重复教程应被重新降权；若仍使用空列表时的得分，两条可能相邻出现，失去教师的去冗余作用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 重排、展示与长期价值</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-491caed66cdd9445">CDM 教师生成序列时，为什么选出一项后要更新相似度惩罚？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acdm">Contextual Distillation Model for Diversified Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>MMR 惩罚相对当前已选前缀的最大相似度，每次加入新项都会改变剩余候选的边际分。若一次算完固定分再排序，就不是同一上下文决策。学生训练标签也应对齐相应前缀，不能把不同阶段的收益混成一个静态单品目标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>选中第一条露营教程后，另一条近重复教程应被重新降权；若仍使用空列表时的得分，两条可能相邻出现，失去教师的去冗余作用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2406.09021">原论文</a> · <a href="../../../../reproductions/2406.09021-cdm/">实现解读</a> · <a href="#qa-491caed66cdd9445">问题链接</a></p>
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
