---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 候选生成与搜索匹配

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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pair" data-paper-title="PAIR: Preference-Aligned Intent Retrieval for Premium People Recommendation at LinkedIn" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="PAIR: Preference-Aligned Intent Retrieval for Premium People Recommendation at LinkedIn 搜广推与 LLM 应用 LinkedIn 2026-10-22 职业社交中的相关性往往是互补而非相似：求职者可能需要招聘者，不是与自己背景最相近的人。PAIR 从被点击候选、同次曝光未点击候选和随机会员构造偏好，训练共享的 profile/document 编码器，并用历史塔刻画短期意图。论文明确说它不是 token 级 DPO，也没有显式参考模型或 KL 项；损失在计算形式上就是多负例对比学习，差别在曝光条件下的监督语义。 成本过高，不复现（审查 DONE）；这些是公式与接口诊断，不是模型准确率、完整推荐能力或线上提升。固定三种子证据见组件指标，真实CUDA回执为 docs/gpu-validations/pair-a100-20261023.json。验证比较独立标量余弦/交叉熵公式与梯度，执行三次真实更新，检查掩码历史无影响、位置顺序有效、曝光负例不混入点击正例。这些是公式与接口诊断，不是模型准确率、完整推荐能力或线上提升。  召回与匹配 曝光偏好与历史意图 搜广推 候选生成与搜索匹配 PAIR 为什么将职业社交相关性理解为互补，而不只相似？ 求职者可能需要招聘者、客户或不同技能伙伴，资料最像的人未必最有帮助。共享资料编码加历史塔，利用同次曝光的点击与未点击构造偏好，让空间反映这种需求。互补关系仍依场景，不能一律推荐背景不同者。 示意：工程师找招聘者时另一工程师更相似却不合任务；若在找技术同伴，工程师又可能合适，当前历史意图决定相关性含义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-pair-40d29d93" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5a6b8f1b86d82b97">PAIR 为什么将职业社交相关性理解为互补，而不只相似？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apair">PAIR: Preference-Aligned Intent Retrieval for Premium People Recommendation at LinkedIn</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>求职者可能需要招聘者、客户或不同技能伙伴，资料最像的人未必最有帮助。共享资料编码加历史塔，利用同次曝光的点击与未点击构造偏好，让空间反映这种需求。互补关系仍依场景，不能一律推荐背景不同者。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>工程师找招聘者时另一工程师更相似却不合任务；若在找技术同伴，工程师又可能合适，当前历史意图决定相关性含义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与服务边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30941v1">原论文</a> · <a href="../../../../recommendation-components/2610.30941-pair/">实现解读</a> · <a href="#qa-5a6b8f1b86d82b97">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pair" data-paper-title="PAIR: Preference-Aligned Intent Retrieval for Premium People Recommendation at LinkedIn" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="PAIR: Preference-Aligned Intent Retrieval for Premium People Recommendation at LinkedIn 搜广推与 LLM 应用 LinkedIn 2026-10-22 职业社交中的相关性往往是互补而非相似：求职者可能需要招聘者，不是与自己背景最相近的人。PAIR 从被点击候选、同次曝光未点击候选和随机会员构造偏好，训练共享的 profile/document 编码器，并用历史塔刻画短期意图。论文明确说它不是 token 级 DPO，也没有显式参考模型或 KL 项；损失在计算形式上就是多负例对比学习，差别在曝光条件下的监督语义。 成本过高，不复现（审查 DONE）；这些是公式与接口诊断，不是模型准确率、完整推荐能力或线上提升。固定三种子证据见组件指标，真实CUDA回执为 docs/gpu-validations/pair-a100-20261023.json。验证比较独立标量余弦/交叉熵公式与梯度，执行三次真实更新，检查掩码历史无影响、位置顺序有效、曝光负例不混入点击正例。这些是公式与接口诊断，不是模型准确率、完整推荐能力或线上提升。  召回与匹配 曝光偏好与历史意图 搜广推 候选生成与搜索匹配 PAIR 的偏好损失形式像多负例对比学习，为什么不能把它称作 token 级 DPO？ PAIR 用点击候选、同次曝光未点击候选和随机会员构造偏好，训练资料编码器与历史塔，使相关性表达互补需求而非只看相似。其计算形式是多负例对比目标，没有逐 token 概率比、显式参考策略或 KL 项。定义性差别在曝光条件下的监督语义，不能因使用“偏好”一词就等同于语言模型 DPO。 示意：求职者点击了招聘者而略过另一位求职者。两位求职者资料可能更相似，但这种曝光偏好要求编码器学会互补关系；训练比较的是候选表示得分，不是回答文本的 token 概率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pair" data-paper-title="PAIR: Preference-Aligned Intent Retrieval for Premium People Recommendation at LinkedIn" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="PAIR: Preference-Aligned Intent Retrieval for Premium People Recommendation at LinkedIn 搜广推与 LLM 应用 LinkedIn 2026-10-22 职业社交中的相关性往往是互补而非相似：求职者可能需要招聘者，不是与自己背景最相近的人。PAIR 从被点击候选、同次曝光未点击候选和随机会员构造偏好，训练共享的 profile/document 编码器，并用历史塔刻画短期意图。论文明确说它不是 token 级 DPO，也没有显式参考模型或 KL 项；损失在计算形式上就是多负例对比学习，差别在曝光条件下的监督语义。 成本过高，不复现（审查 DONE）；这些是公式与接口诊断，不是模型准确率、完整推荐能力或线上提升。固定三种子证据见组件指标，真实CUDA回执为 docs/gpu-validations/pair-a100-20261023.json。验证比较独立标量余弦/交叉熵公式与梯度，执行三次真实更新，检查掩码历史无影响、位置顺序有效、曝光负例不混入点击正例。这些是公式与接口诊断，不是模型准确率、完整推荐能力或线上提升。  召回与匹配 曝光偏好与历史意图 搜广推 候选生成与搜索匹配 PAIR 的同次曝光未点击与随机会员负例，分别提供什么区分难度？ 曝光未点击更接近用户实际面对的竞争对象，随机会员提供较广但常更容易的背景；混合帮助区分细粒度选择与全局空间。未点击不一定真负，位置与机会也影响反馈。来源称偏好不代表有 token DPO 或已消除曝光偏差。 示意：用户在两位同地区招聘者中点了一位，是细比较；从全国随机抽一个无关学生更易区分，却不能替代这次真实选择关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f86c93423be74324">PAIR 的同次曝光未点击与随机会员负例，分别提供什么区分难度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apair">PAIR: Preference-Aligned Intent Retrieval for Premium People Recommendation at LinkedIn</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>曝光未点击更接近用户实际面对的竞争对象，随机会员提供较广但常更容易的背景；混合帮助区分细粒度选择与全局空间。未点击不一定真负，位置与机会也影响反馈。来源称偏好不代表有 token DPO 或已消除曝光偏差。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户在两位同地区招聘者中点了一位，是细比较；从全国随机抽一个无关学生更易区分，却不能替代这次真实选择关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与服务边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30941v1">原论文</a> · <a href="../../../../recommendation-components/2610.30941-pair/">实现解读</a> · <a href="#qa-f86c93423be74324">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pair" data-paper-title="PAIR: Preference-Aligned Intent Retrieval for Premium People Recommendation at LinkedIn" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="PAIR: Preference-Aligned Intent Retrieval for Premium People Recommendation at LinkedIn 搜广推与 LLM 应用 LinkedIn 2026-10-22 职业社交中的相关性往往是互补而非相似：求职者可能需要招聘者，不是与自己背景最相近的人。PAIR 从被点击候选、同次曝光未点击候选和随机会员构造偏好，训练共享的 profile/document 编码器，并用历史塔刻画短期意图。论文明确说它不是 token 级 DPO，也没有显式参考模型或 KL 项；损失在计算形式上就是多负例对比学习，差别在曝光条件下的监督语义。 成本过高，不复现（审查 DONE）；这些是公式与接口诊断，不是模型准确率、完整推荐能力或线上提升。固定三种子证据见组件指标，真实CUDA回执为 docs/gpu-validations/pair-a100-20261023.json。验证比较独立标量余弦/交叉熵公式与梯度，执行三次真实更新，检查掩码历史无影响、位置顺序有效、曝光负例不混入点击正例。这些是公式与接口诊断，不是模型准确率、完整推荐能力或线上提升。  召回与匹配 曝光偏好与历史意图 搜广推 候选生成与搜索匹配 PAIR 的历史塔如何检查 position、padding 与候选身份，而不读取未来点击？ 历史只能含请求前事件，mask 应使 padding 内容变化不影响输出，位置变化可按结构影响序列，候选资料与标签保持配对。真实更新与梯度诊断能核验算子，不把少量 CUDA smoke 当正式职业推荐收益。原文损失是多负例对比，不可擅加参考 KL。 示意：改动被 mask 的历史 token 不应改变分数；若改了未来被点击候选才变准，那不是合法历史建模，而是把答案漏进输入。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f03a7c6d20c75741">PAIR 的历史塔如何检查 position、padding 与候选身份，而不读取未来点击？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apair">PAIR: Preference-Aligned Intent Retrieval for Premium People Recommendation at LinkedIn</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>历史只能含请求前事件，mask 应使 padding 内容变化不影响输出，位置变化可按结构影响序列，候选资料与标签保持配对。真实更新与梯度诊断能核验算子，不把少量 CUDA smoke 当正式职业推荐收益。原文损失是多负例对比，不可擅加参考 KL。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>改动被 mask 的历史 token 不应改变分数；若改了未来被点击候选才变准，那不是合法历史建模，而是把答案漏进输入。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与服务边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30941v1">原论文</a> · <a href="../../../../recommendation-components/2610.30941-pair/">实现解读</a> · <a href="#qa-f03a7c6d20c75741">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:snap-dpa-relevance" data-paper-title="LLM-based User-Product Relevance Evaluation for Dynamic Product Advertising" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="LLM-based User-Product Relevance Evaluation for Dynamic Product Advertising 搜广推与 LLM 应用 Snap Inc. 2026-10-10 广告召回的点击信号稀疏且有偏，单纯离线命中率难以代表用户真实需求。该方法按语义ID与事件类型压缩历史意图，通过自动发现且人工业务对齐的相关性准则训练学生判别器，再聚合为用户与流量组的相关性指标。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文§4–5依赖10K私有日志经GPT-5、Gemini-2.5-Pro与多轮人工审定；生产student为Gemini-2.5-Flash微调并经Vertex AI调用。商业API、人工标注和私有数据不是当前单卡可直接复现的资源；未测量本地或API总成本，不启动付费教师调用或替换为启发式judge。  ads-retrieval llm-judge evaluation 搜广推 候选生成与搜索匹配 Snap DPA相关性为何先压缩历史意图而不直接看点击？ 点击稀疏且受曝光影响，按SID与事件类型分组提取最新意图，再由业务对齐准则判候选相关，形成另一种用户需求评价轴。不是把点击率重新命名为相关性。 例如近期多次加购某类物品比一次偶然曝光更能表达当前需求。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-snap-dpa-relevance-9f0c9ccb" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9395ea2a026ef61e">Snap DPA相关性为何先压缩历史意图而不直接看点击？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asnap-dpa-relevance">LLM-based User-Product Relevance Evaluation for Dynamic Product Advertising</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Snap Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>点击稀疏且受曝光影响，按SID与事件类型分组提取最新意图，再由业务对齐准则判候选相关，形成另一种用户需求评价轴。不是把点击率重新命名为相关性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如近期多次加购某类物品比一次偶然曝光更能表达当前需求。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14550">原论文</a> · <a href="../../../../reproductions/2610.14550-snap-dpa-relevance/">实现解读</a> · <a href="#qa-9395ea2a026ef61e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:snap-dpa-relevance" data-paper-title="LLM-based User-Product Relevance Evaluation for Dynamic Product Advertising" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="LLM-based User-Product Relevance Evaluation for Dynamic Product Advertising 搜广推与 LLM 应用 Snap Inc. 2026-10-10 广告召回的点击信号稀疏且有偏，单纯离线命中率难以代表用户真实需求。该方法按语义ID与事件类型压缩历史意图，通过自动发现且人工业务对齐的相关性准则训练学生判别器，再聚合为用户与流量组的相关性指标。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文§4–5依赖10K私有日志经GPT-5、Gemini-2.5-Pro与多轮人工审定；生产student为Gemini-2.5-Flash微调并经Vertex AI调用。商业API、人工标注和私有数据不是当前单卡可直接复现的资源；未测量本地或API总成本，不启动付费教师调用或替换为启发式judge。  ads-retrieval llm-judge evaluation 搜广推 候选生成与搜索匹配 Snap DPA 相关性指标为什么区分 MicroRel 与 MacroRel，还要先审定判别准则？ 历史按语义与事件压缩成意图组，再由经准则训练的判别器评价候选相关性。MicroRel 对用户—候选对等权，容易受候选多的用户影响；MacroRel 对用户等权，观察的是另一种群体平均。准则发现与人工业务对齐决定“相关”含义，聚合公式不能补救错误判别；本地没有复现私有评审数据和商业模型流程。 示意：一个用户有一百条候选，另一个只有十条。按候选对平均时前者权重大十倍，按用户平均时两者相同；两种结果都应先建立在可靠的相关性判断上。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:snap-dpa-relevance" data-paper-title="LLM-based User-Product Relevance Evaluation for Dynamic Product Advertising" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="LLM-based User-Product Relevance Evaluation for Dynamic Product Advertising 搜广推与 LLM 应用 Snap Inc. 2026-10-10 广告召回的点击信号稀疏且有偏，单纯离线命中率难以代表用户真实需求。该方法按语义ID与事件类型压缩历史意图，通过自动发现且人工业务对齐的相关性准则训练学生判别器，再聚合为用户与流量组的相关性指标。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文§4–5依赖10K私有日志经GPT-5、Gemini-2.5-Pro与多轮人工审定；生产student为Gemini-2.5-Flash微调并经Vertex AI调用。商业API、人工标注和私有数据不是当前单卡可直接复现的资源；未测量本地或API总成本，不启动付费教师调用或替换为启发式judge。  ads-retrieval llm-judge evaluation 搜广推 候选生成与搜索匹配 MicroRel与MacroRel为什么可能给出不同结论？ 前者每用户候选对等权，后者每用户等权；候选多的用户在micro占更多份量。两者统计单位不同，不可选更好看的一个代表全部流量。 例如活跃用户候选很多，其分数会更影响micro而非同程度影响macro。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-59a1b674f56a0a46">MicroRel与MacroRel为什么可能给出不同结论？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asnap-dpa-relevance">LLM-based User-Product Relevance Evaluation for Dynamic Product Advertising</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Snap Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者每用户候选对等权，后者每用户等权；候选多的用户在micro占更多份量。两者统计单位不同，不可选更好看的一个代表全部流量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如活跃用户候选很多，其分数会更影响micro而非同程度影响macro。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14550">原论文</a> · <a href="../../../../reproductions/2610.14550-snap-dpa-relevance/">实现解读</a> · <a href="#qa-59a1b674f56a0a46">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:snap-dpa-relevance" data-paper-title="LLM-based User-Product Relevance Evaluation for Dynamic Product Advertising" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="LLM-based User-Product Relevance Evaluation for Dynamic Product Advertising 搜广推与 LLM 应用 Snap Inc. 2026-10-10 广告召回的点击信号稀疏且有偏，单纯离线命中率难以代表用户真实需求。该方法按语义ID与事件类型压缩历史意图，通过自动发现且人工业务对齐的相关性准则训练学生判别器，再聚合为用户与流量组的相关性指标。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文§4–5依赖10K私有日志经GPT-5、Gemini-2.5-Pro与多轮人工审定；生产student为Gemini-2.5-Flash微调并经Vertex AI调用。商业API、人工标注和私有数据不是当前单卡可直接复现的资源；未测量本地或API总成本，不启动付费教师调用或替换为启发式judge。  ads-retrieval llm-judge evaluation 搜广推 候选生成与搜索匹配 相关性判别器能用真实标签直接回填代替吗？ 不能，需按发现且经人工业务审查的准则实际训练判别模型，再在独立数据验证。规则发现还有bootstrap和各类F1边界，不能省人工覆盖审查后声称整套完成。 例如把金标当预测可算指标，但不证明模型学会判断用户商品相关。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ec1c2b80c0f2fa30">相关性判别器能用真实标签直接回填代替吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asnap-dpa-relevance">LLM-based User-Product Relevance Evaluation for Dynamic Product Advertising</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Snap Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，需按发现且经人工业务审查的准则实际训练判别模型，再在独立数据验证。规则发现还有bootstrap和各类F1边界，不能省人工覆盖审查后声称整套完成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把金标当预测可算指标，但不证明模型学会判断用户商品相关。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14550">原论文</a> · <a href="../../../../reproductions/2610.14550-snap-dpa-relevance/">实现解读</a> · <a href="#qa-ec1c2b80c0f2fa30">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rptune" data-paper-title="RPTune: Learned Context Curation for LLM Catalog Search" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="RPTune: Learned Context Curation for LLM Catalog Search 搜广推与 LLM 应用 Google 2026-10-01 用查询-商品编码器、可学习调整项和下游 LLM 反馈共同决定商品保留与摆放顺序；高优商品靠近提示词末端，再对编排后的目录做选择后训练。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。只执行 rank/prune/position 核心编排，不调用 Gemini/Gemma、商家目录或论文训练。只执行 rank/prune/position 核心编排，不调用 Gemini/Gemma、商家目录或论文训练。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  search llm-recommendation context-curation 搜广推 候选生成与搜索匹配 RPTune的prune与position分别决定商品是否出现，还是出现在哪里？ prune决定哪些目录商品保留进提示，position决定保留商品的摆放顺序。前者改变可供下游选择的集合，后者改变模型读取同一集合的上下文条件；两者是独立可观察的编排动作。没进入上下文的商品不能靠调整位置重新获得曝光。 教学例子：先从一千件中保留十件，再把这十件按规定重排；第二步不会把第一步删掉的商品重新找回。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-rptune-1e6a74b6" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-cfc59a331b753a91">RPTune的prune与position分别决定商品是否出现，还是出现在哪里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arptune">RPTune: Learned Context Curation for LLM Catalog Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>prune决定哪些目录商品保留进提示，position决定保留商品的摆放顺序。前者改变可供下游选择的集合，后者改变模型读取同一集合的上下文条件；两者是独立可观察的编排动作。没进入上下文的商品不能靠调整位置重新获得曝光。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先从一千件中保留十件，再把这十件按规定重排；第二步不会把第一步删掉的商品重新找回。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00964">原论文</a> · <a href="../../../../reproductions/2610.00964-rptune/">实现解读</a> · <a href="#qa-cfc59a331b753a91">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rptune" data-paper-title="RPTune: Learned Context Curation for LLM Catalog Search" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="RPTune: Learned Context Curation for LLM Catalog Search 搜广推与 LLM 应用 Google 2026-10-01 用查询-商品编码器、可学习调整项和下游 LLM 反馈共同决定商品保留与摆放顺序；高优商品靠近提示词末端，再对编排后的目录做选择后训练。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。只执行 rank/prune/position 核心编排，不调用 Gemini/Gemma、商家目录或论文训练。只执行 rank/prune/position 核心编排，不调用 Gemini/Gemma、商家目录或论文训练。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  search llm-recommendation context-curation 搜广推 候选生成与搜索匹配 RPTune 为什么把高优商品按升序放到提示末端，而不是简单按相关性降序塞满上下文？ 目录选择与提示位置都会影响下游语言模型利用信息的方式。查询—商品得分加可学习调整项先决定保留谁，再把高优项靠近末端，让编排本身成为可优化变量；后训练适配这种目录输入。它不只是换排序展示顺序，本地只检验定义性编排算子，不能据此声称所有模型都必然有相同位置偏好。 示意：提示只能容纳三件商品，先删掉低相关候选，再把最符合预算的商品放在靠近回答的位置。模型看到的内容与位置同时变化，需要分别检查各自贡献。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rptune" data-paper-title="RPTune: Learned Context Curation for LLM Catalog Search" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="RPTune: Learned Context Curation for LLM Catalog Search 搜广推与 LLM 应用 Google 2026-10-01 用查询-商品编码器、可学习调整项和下游 LLM 反馈共同决定商品保留与摆放顺序；高优商品靠近提示词末端，再对编排后的目录做选择后训练。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。只执行 rank/prune/position 核心编排，不调用 Gemini/Gemma、商家目录或论文训练。只执行 rank/prune/position 核心编排，不调用 Gemini/Gemma、商家目录或论文训练。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  search llm-recommendation context-curation 搜广推 候选生成与搜索匹配 RPTune的商品打分与后续提示排序，是否都等同于普通向量top-k？ 不等同。打分除语义点积外还有查询与商品的可学习调整项；保留top-k后还要执行规定的位置编排。纯向量top-k既不包含该调整项，也不规定输入LLM的顺序。应分别对照集合选择和位置策略，不能把二者的作用合并解释。 教学例子：两个方案可保留相同十件商品却顺序不同；也可顺序规则相同但因调整项选出不同集合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-51d8e0ae47576123">RPTune的商品打分与后续提示排序，是否都等同于普通向量top-k？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arptune">RPTune: Learned Context Curation for LLM Catalog Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不等同。打分除语义点积外还有查询与商品的可学习调整项；保留top-k后还要执行规定的位置编排。纯向量top-k既不包含该调整项，也不规定输入LLM的顺序。应分别对照集合选择和位置策略，不能把二者的作用合并解释。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个方案可保留相同十件商品却顺序不同；也可顺序规则相同但因调整项选出不同集合。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00964">原论文</a> · <a href="../../../../reproductions/2610.00964-rptune/">实现解读</a> · <a href="#qa-51d8e0ae47576123">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rptune" data-paper-title="RPTune: Learned Context Curation for LLM Catalog Search" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="RPTune: Learned Context Curation for LLM Catalog Search 搜广推与 LLM 应用 Google 2026-10-01 用查询-商品编码器、可学习调整项和下游 LLM 反馈共同决定商品保留与摆放顺序；高优商品靠近提示词末端，再对编排后的目录做选择后训练。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。只执行 rank/prune/position 核心编排，不调用 Gemini/Gemma、商家目录或论文训练。只执行 rank/prune/position 核心编排，不调用 Gemini/Gemma、商家目录或论文训练。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  search llm-recommendation context-curation 搜广推 候选生成与搜索匹配 RPTune选出top-k后为什么按分数升序摆放？ 规定高分靠末端，所以保留集合后再升序排列，不能习惯性降序。当前只执行rank/prune/position核，未调用原LLM或完成后训练，不能报告完整目录搜索收益。 例如最高分被排在最前，会反转设计的末端优先位置。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-825fb1cf921dcc1c">RPTune选出top-k后为什么按分数升序摆放？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arptune">RPTune: Learned Context Curation for LLM Catalog Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>规定高分靠末端，所以保留集合后再升序排列，不能习惯性降序。当前只执行rank/prune/position核，未调用原LLM或完成后训练，不能报告完整目录搜索收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如最高分被排在最前，会反转设计的末端优先位置。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00964">原论文</a> · <a href="../../../../reproductions/2610.00964-rptune/">实现解读</a> · <a href="#qa-825fb1cf921dcc1c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:muser" data-paper-title="MuSeR: Scalable Long-sequence Recommendation with Multi-interest Modeling" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="MuSeR: Scalable Long-sequence Recommendation with Multi-interest Modeling 搜广推与 LLM 应用 Baidu 2026-09-20 工业用户长期行为可达十万级，直接截断丢掉稳定偏好，直接 Transformer 编码又超预算。MuSeR 将最近行为原样保留，中期与远期行为分别用更大步幅汇聚；压缩后的序列由轻量 Transformer 编码。多组可学习 query 从序列状态提取不同兴趣，候选物品再通过相似度 softmax 选择兴趣。论文还把 ERNIE 生成的内容摘要蒸馏后用 BGE 编码，与 ID embedding 对齐并融合；训练使用 next-K 对比目标和兴趣正交正则。 复现级别：概念验证（非论文完整复现）。复现级别：概念验证（非论文完整复现）。本地训练了分层时间压缩、Transformer 编码、可学习多查询兴趣、候选自适应兴趣融合与正交约束；但论文的 ERNIE→BGE 多模态语义链路被公开商品标签替代，因此不能把本地结果称为 MuSeR 论文效果。公开数据只有视频标签作为内容特征，没有论文使用的 ERNIE 摘要、ERNIE-Speed 蒸馏、BGE 文本/视频向量；这决定了本实验只能列为概念验证。本地对照口径：最近序列单兴趣 ID 为基线，三 seed test Recall@10 均值 0.0100；完整本地实验组 0.0257，相对 +156.7%、绝对 +0.0157。  retrieval long-sequence multi-interest 搜广推 候选生成与搜索匹配 MuSeR 的多组可学习 query 为什么要加兴趣正交正则？ 多 query 可能全部读取同一热门模式，形式上多兴趣却缺少分工。正交项限制兴趣向量相似，鼓励不同方向供候选选择。几何不同不等于语义互补，也可能把真实相关兴趣推开，效果需用消融和任务指标检查。 示意：摄影与露营 query 若都只抓热门短视频，候选没有真正选择；分开方向可改善覆盖，但随机正交的两个向量也未必有用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-muser-f887e208" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8ffaaf0436b17c9f">MuSeR 的多组可学习 query 为什么要加兴趣正交正则？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amuser">MuSeR: Scalable Long-sequence Recommendation with Multi-interest Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Baidu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多 query 可能全部读取同一热门模式，形式上多兴趣却缺少分工。正交项限制兴趣向量相似，鼓励不同方向供候选选择。几何不同不等于语义互补，也可能把真实相关兴趣推开，效果需用消融和任务指标检查。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>摄影与露营 query 若都只抓热门短视频，候选没有真正选择；分开方向可改善覆盖，但随机正交的两个向量也未必有用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.23677">原论文</a> · <a href="../../../../reproductions/2609.23677-muser/">实现解读</a> · <a href="#qa-8ffaaf0436b17c9f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:muser" data-paper-title="MuSeR: Scalable Long-sequence Recommendation with Multi-interest Modeling" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="MuSeR: Scalable Long-sequence Recommendation with Multi-interest Modeling 搜广推与 LLM 应用 Baidu 2026-09-20 工业用户长期行为可达十万级，直接截断丢掉稳定偏好，直接 Transformer 编码又超预算。MuSeR 将最近行为原样保留，中期与远期行为分别用更大步幅汇聚；压缩后的序列由轻量 Transformer 编码。多组可学习 query 从序列状态提取不同兴趣，候选物品再通过相似度 softmax 选择兴趣。论文还把 ERNIE 生成的内容摘要蒸馏后用 BGE 编码，与 ID embedding 对齐并融合；训练使用 next-K 对比目标和兴趣正交正则。 复现级别：概念验证（非论文完整复现）。复现级别：概念验证（非论文完整复现）。本地训练了分层时间压缩、Transformer 编码、可学习多查询兴趣、候选自适应兴趣融合与正交约束；但论文的 ERNIE→BGE 多模态语义链路被公开商品标签替代，因此不能把本地结果称为 MuSeR 论文效果。公开数据只有视频标签作为内容特征，没有论文使用的 ERNIE 摘要、ERNIE-Speed 蒸馏、BGE 文本/视频向量；这决定了本实验只能列为概念验证。本地对照口径：最近序列单兴趣 ID 为基线，三 seed test Recall@10 均值 0.0100；完整本地实验组 0.0257，相对 +156.7%、绝对 +0.0157。  retrieval long-sequence multi-interest 搜广推 候选生成与搜索匹配 MuSeR 为什么近、中、远期历史用不同压缩步幅，还要让候选选择不同兴趣？ 近期行为保留细节以捕捉即时意图，较远历史用更大步幅汇聚以控制长序列成本。多个可学习查询再从压缩序列提取不同兴趣，候选依据相似度选择合适的兴趣组合。时间压缩解决“读多少历史”，多兴趣选择解决“读完后用哪部分”；二者互补，但汇聚仍可能损失远期稀有事件。 示意：用户长期爱摄影，近期在准备露营。远期摄影行为可合并保留稳定偏好，最近露营浏览逐条保留；相机候选与帐篷候选再分别激活不同兴趣向量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:muser" data-paper-title="MuSeR: Scalable Long-sequence Recommendation with Multi-interest Modeling" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="MuSeR: Scalable Long-sequence Recommendation with Multi-interest Modeling 搜广推与 LLM 应用 Baidu 2026-09-20 工业用户长期行为可达十万级，直接截断丢掉稳定偏好，直接 Transformer 编码又超预算。MuSeR 将最近行为原样保留，中期与远期行为分别用更大步幅汇聚；压缩后的序列由轻量 Transformer 编码。多组可学习 query 从序列状态提取不同兴趣，候选物品再通过相似度 softmax 选择兴趣。论文还把 ERNIE 生成的内容摘要蒸馏后用 BGE 编码，与 ID embedding 对齐并融合；训练使用 next-K 对比目标和兴趣正交正则。 复现级别：概念验证（非论文完整复现）。复现级别：概念验证（非论文完整复现）。本地训练了分层时间压缩、Transformer 编码、可学习多查询兴趣、候选自适应兴趣融合与正交约束；但论文的 ERNIE→BGE 多模态语义链路被公开商品标签替代，因此不能把本地结果称为 MuSeR 论文效果。公开数据只有视频标签作为内容特征，没有论文使用的 ERNIE 摘要、ERNIE-Speed 蒸馏、BGE 文本/视频向量；这决定了本实验只能列为概念验证。本地对照口径：最近序列单兴趣 ID 为基线，三 seed test Recall@10 均值 0.0100；完整本地实验组 0.0257，相对 +156.7%、绝对 +0.0157。  retrieval long-sequence multi-interest 搜广推 候选生成与搜索匹配 MuSeR 的候选选择兴趣与统一平均多个兴趣，相比保留什么条件性？ 平均给所有候选同一汇总，候选 softmax 按相似度激活不同兴趣，让相机与帐篷读取不同用户侧知识。需要计算候选相关权重，不能把该结果全部当公共缓存。来源标签融合并不等于原 ERNIE/BGE 多模态链路已完整复刻。 示意：同一用户相机候选更重摄影向量，帐篷更重露营向量；若先平均，两个候选都只看到折中表示，可能稀释各自证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-da9523e9a8606b73">MuSeR 的候选选择兴趣与统一平均多个兴趣，相比保留什么条件性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amuser">MuSeR: Scalable Long-sequence Recommendation with Multi-interest Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Baidu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>平均给所有候选同一汇总，候选 softmax 按相似度激活不同兴趣，让相机与帐篷读取不同用户侧知识。需要计算候选相关权重，不能把该结果全部当公共缓存。来源标签融合并不等于原 ERNIE/BGE 多模态链路已完整复刻。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一用户相机候选更重摄影向量，帐篷更重露营向量；若先平均，两个候选都只看到折中表示，可能稀释各自证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.23677">原论文</a> · <a href="../../../../reproductions/2609.23677-muser/">实现解读</a> · <a href="#qa-da9523e9a8606b73">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:muser" data-paper-title="MuSeR: Scalable Long-sequence Recommendation with Multi-interest Modeling" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="MuSeR: Scalable Long-sequence Recommendation with Multi-interest Modeling 搜广推与 LLM 应用 Baidu 2026-09-20 工业用户长期行为可达十万级，直接截断丢掉稳定偏好，直接 Transformer 编码又超预算。MuSeR 将最近行为原样保留，中期与远期行为分别用更大步幅汇聚；压缩后的序列由轻量 Transformer 编码。多组可学习 query 从序列状态提取不同兴趣，候选物品再通过相似度 softmax 选择兴趣。论文还把 ERNIE 生成的内容摘要蒸馏后用 BGE 编码，与 ID embedding 对齐并融合；训练使用 next-K 对比目标和兴趣正交正则。 复现级别：概念验证（非论文完整复现）。复现级别：概念验证（非论文完整复现）。本地训练了分层时间压缩、Transformer 编码、可学习多查询兴趣、候选自适应兴趣融合与正交约束；但论文的 ERNIE→BGE 多模态语义链路被公开商品标签替代，因此不能把本地结果称为 MuSeR 论文效果。公开数据只有视频标签作为内容特征，没有论文使用的 ERNIE 摘要、ERNIE-Speed 蒸馏、BGE 文本/视频向量；这决定了本实验只能列为概念验证。本地对照口径：最近序列单兴趣 ID 为基线，三 seed test Recall@10 均值 0.0100；完整本地实验组 0.0257，相对 +156.7%、绝对 +0.0157。  retrieval long-sequence multi-interest 搜广推 候选生成与搜索匹配 MuSeR 本地大相对 Recall 增益为什么仍需报告低绝对值与分模块结果？ 基线很低时小绝对变化也形成大百分比，不能遮掉整体仍难命中的事实；分层压缩本地消融差距小，联合改善不能全部归给它。测试抽样用户和全目录范围也应明确，标签代理不能称为原大模型摘要收益。 示意：Recall 从百分之一到约百分之二点六相对增幅很大，仍有绝大多数目标没进前十；只报一百多百分点会误导读者以为任务已解决。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-68f338a526b6f67a">MuSeR 本地大相对 Recall 增益为什么仍需报告低绝对值与分模块结果？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amuser">MuSeR: Scalable Long-sequence Recommendation with Multi-interest Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Baidu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>基线很低时小绝对变化也形成大百分比，不能遮掉整体仍难命中的事实；分层压缩本地消融差距小，联合改善不能全部归给它。测试抽样用户和全目录范围也应明确，标签代理不能称为原大模型摘要收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>Recall 从百分之一到约百分之二点六相对增幅很大，仍有绝大多数目标没进前十；只报一百多百分点会误导读者以为任务已解决。</p>
<p class="ar-learning-sources">依据：本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.23677">原论文</a> · <a href="../../../../reproductions/2609.23677-muser/">实现解读</a> · <a href="#qa-68f338a526b6f67a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mima" data-paper-title="MIMA: Multi-Interest Recommendation via Multi-Positive Exclusive Assignment" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="MIMA: Multi-Interest Recommendation via Multi-Positive Exclusive Assignment 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-09-11 传统多兴趣召回每个训练样本只有一个正例，容易反复更新同一个最相似兴趣并造成 interest collapse。MIMA 把同一请求共同出现的物品视为多正例集合，用 causal decoder 生成多个兴趣，再用 Hungarian matching 强制正例与兴趣一对一监督；routing 模块估计每个兴趣的激活概率，使不同通道的分数可比较。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行多正例分组、一对一最小成本分配、互补兴趣更新和兴趣激活校准；生产 causal Transformer 由公开序列特征替代。公开数据没有生产“同请求多成交”日志，本地以相邻行为组替代；未复刻阿里私有 catalog、生产 causal Transformer checkpoint 和在线召回系统。当前不映射 evolve，避免只有 registry 标签而无可执行候选协议。MovieLens 100K、seeds 42/43/44 的统一结果见 metrics/movielens-100k-seeds42-44.json。  retrieval multi-interest exclusive-assignment industrial-recommendation 搜广推 候选生成与搜索匹配 MIMA 为什么把同一请求正例当成集合，而不是强制固定先后序列？ 请求内多个正例可代表并存兴趣，固定顺序会人为指定哪条兴趣先解释哪个物品。集合匹配让多个兴趣分工而对排列不敏感，routing 再估实际激活。集合不表示无任何时序信息，历史编码仍可因果，改变的是正例监督对应。 示意：同次请求跑鞋与登山包都被喜欢，不必规定先学鞋再学包；两条兴趣各解释一项，比总由最强运动通道独占更有分工。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-mima-5191fe9f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-1132beb05c6cad64">MIMA 为什么把同一请求正例当成集合，而不是强制固定先后序列？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amima">MIMA: Multi-Interest Recommendation via Multi-Positive Exclusive Assignment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>请求内多个正例可代表并存兴趣，固定顺序会人为指定哪条兴趣先解释哪个物品。集合匹配让多个兴趣分工而对排列不敏感，routing 再估实际激活。集合不表示无任何时序信息，历史编码仍可因果，改变的是正例监督对应。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同次请求跑鞋与登山包都被喜欢，不必规定先学鞋再学包；两条兴趣各解释一项，比总由最强运动通道独占更有分工。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.12842">原论文</a> · <a href="../../../../reproductions/2609.12842-mima/">实现解读</a> · <a href="#qa-1132beb05c6cad64">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mima" data-paper-title="MIMA: Multi-Interest Recommendation via Multi-Positive Exclusive Assignment" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="MIMA: Multi-Interest Recommendation via Multi-Positive Exclusive Assignment 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-09-11 传统多兴趣召回每个训练样本只有一个正例，容易反复更新同一个最相似兴趣并造成 interest collapse。MIMA 把同一请求共同出现的物品视为多正例集合，用 causal decoder 生成多个兴趣，再用 Hungarian matching 强制正例与兴趣一对一监督；routing 模块估计每个兴趣的激活概率，使不同通道的分数可比较。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行多正例分组、一对一最小成本分配、互补兴趣更新和兴趣激活校准；生产 causal Transformer 由公开序列特征替代。公开数据没有生产“同请求多成交”日志，本地以相邻行为组替代；未复刻阿里私有 catalog、生产 causal Transformer checkpoint 和在线召回系统。当前不映射 evolve，避免只有 registry 标签而无可执行候选协议。MovieLens 100K、seeds 42/43/44 的统一结果见 metrics/movielens-100k-seeds42-44.json。  retrieval multi-interest exclusive-assignment industrial-recommendation 搜广推 候选生成与搜索匹配 为什么 MIMA 要把同一请求的多个正例一对一分配给兴趣，而不是让每个正例选择最相似的兴趣？ 独立选择最相似兴趣会让多个正例持续更新同一个通道，其余兴趣得不到监督。MIMA 先构造兴趣与正例的相似度代价矩阵，再求全局最优的一对一匹配，让不同兴趣分别承担正例。激活概率进一步校准通道得分；分工由集合监督产生，不只是增加向量数量。 示意：同一请求有跑鞋、登山包两个正例。若都更新“运动”通道，另一个兴趣闲置；一对一匹配迫使两个通道各解释一个正例，再按激活概率参与召回。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mima" data-paper-title="MIMA: Multi-Interest Recommendation via Multi-Positive Exclusive Assignment" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="MIMA: Multi-Interest Recommendation via Multi-Positive Exclusive Assignment 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-09-11 传统多兴趣召回每个训练样本只有一个正例，容易反复更新同一个最相似兴趣并造成 interest collapse。MIMA 把同一请求共同出现的物品视为多正例集合，用 causal decoder 生成多个兴趣，再用 Hungarian matching 强制正例与兴趣一对一监督；routing 模块估计每个兴趣的激活概率，使不同通道的分数可比较。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行多正例分组、一对一最小成本分配、互补兴趣更新和兴趣激活校准；生产 causal Transformer 由公开序列特征替代。公开数据没有生产“同请求多成交”日志，本地以相邻行为组替代；未复刻阿里私有 catalog、生产 causal Transformer checkpoint 和在线召回系统。当前不映射 evolve，避免只有 registry 标签而无可执行候选协议。MovieLens 100K、seeds 42/43/44 的统一结果见 metrics/movielens-100k-seeds42-44.json。  retrieval multi-interest exclusive-assignment industrial-recommendation 搜广推 候选生成与搜索匹配 MIMA 的一对一匹配与每个正例独立选最近兴趣，相比怎样避免同通道拥挤？ 独立选择可让全部正例落同一兴趣，其他通道没有梯度；全局匹配要求在总成本下分配不同位置，形成竞争与分工。若兴趣数和正例数不等，未匹配处理仍需定义；分工强制也可能让噪声正例影响某通道，不保证天然语义独立。 示意：两件商品都略偏兴趣一，独立 argmax 全选一；一对一会比较把其中一件交给兴趣二的总成本，而不是单项贪心。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-34e97c32a3372408">MIMA 的一对一匹配与每个正例独立选最近兴趣，相比怎样避免同通道拥挤？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amima">MIMA: Multi-Interest Recommendation via Multi-Positive Exclusive Assignment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立选择可让全部正例落同一兴趣，其他通道没有梯度；全局匹配要求在总成本下分配不同位置，形成竞争与分工。若兴趣数和正例数不等，未匹配处理仍需定义；分工强制也可能让噪声正例影响某通道，不保证天然语义独立。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两件商品都略偏兴趣一，独立 argmax 全选一；一对一会比较把其中一件交给兴趣二的总成本，而不是单项贪心。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.12842">原论文</a> · <a href="../../../../reproductions/2609.12842-mima/">实现解读</a> · <a href="#qa-34e97c32a3372408">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mima" data-paper-title="MIMA: Multi-Interest Recommendation via Multi-Positive Exclusive Assignment" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="MIMA: Multi-Interest Recommendation via Multi-Positive Exclusive Assignment 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-09-11 传统多兴趣召回每个训练样本只有一个正例，容易反复更新同一个最相似兴趣并造成 interest collapse。MIMA 把同一请求共同出现的物品视为多正例集合，用 causal decoder 生成多个兴趣，再用 Hungarian matching 强制正例与兴趣一对一监督；routing 模块估计每个兴趣的激活概率，使不同通道的分数可比较。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行多正例分组、一对一最小成本分配、互补兴趣更新和兴趣激活校准；生产 causal Transformer 由公开序列特征替代。公开数据没有生产“同请求多成交”日志，本地以相邻行为组替代；未复刻阿里私有 catalog、生产 causal Transformer checkpoint 和在线召回系统。当前不映射 evolve，避免只有 registry 标签而无可执行候选协议。MovieLens 100K、seeds 42/43/44 的统一结果见 metrics/movielens-100k-seeds42-44.json。  retrieval multi-interest exclusive-assignment industrial-recommendation 搜广推 候选生成与搜索匹配 MIMA 小规模穷举与 Hungarian 何时在目标上等价，什么不能随意替换？ 二者都求同一代价矩阵的最优一对一分配，小矩阵可穷举核验最优值；贪心逐项匹配一般不等价。代价应使用对应兴趣与正例相似度，routing 的 log 激活概率另用于通道校准。只比较配对是否看起来合理不够。 示意：第一个正例抢走唯一适合第二个的兴趣，贪心可能总损失更高；穷举所有合法配对能发现另一分配才是全局最优。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8833e9be64e7f356">MIMA 小规模穷举与 Hungarian 何时在目标上等价，什么不能随意替换？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amima">MIMA: Multi-Interest Recommendation via Multi-Positive Exclusive Assignment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>二者都求同一代价矩阵的最优一对一分配，小矩阵可穷举核验最优值；贪心逐项匹配一般不等价。代价应使用对应兴趣与正例相似度，routing 的 log 激活概率另用于通道校准。只比较配对是否看起来合理不够。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第一个正例抢走唯一适合第二个的兴趣，贪心可能总损失更高；穷举所有合法配对能发现另一分配才是全局最优。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.12842">原论文</a> · <a href="../../../../reproductions/2609.12842-mima/">实现解读</a> · <a href="#qa-8833e9be64e7f356">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:allecompanion" data-paper-title="Beyond Co-purchase Relation: Evolution of Complementary Recommendations at Allegro" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Beyond Co-purchase Relation: Evolution of Complementary Recommendations at Allegro 搜广推与 LLM 应用 Allegro.com 2026-09-04 共购不等于互补：相机与另一台相机可能经常一起浏览，却不如镜头真正互补。AlleCompanion 先用 ComCat 融合专家规则、人工反馈、LLM 推理和统计挖掘形成类别关系，再用类别约束双塔和 Category Adapter 把候选限制在合理的互补空间。 复现级别：CPU 可训练检索核心。复现级别：CPU 可训练检索核心。共享内容/类别编码器、Category Adapter、混合负样本检索损失和类别重建损失均参与反向传播。MovieLens 邻接关系不是商品互补性，不声称复现 ComCat 或线上效果。ComCat 原始映射、Allegro 行为数据和生产服务未公开；本地实现的是可审计核心机制，不是生产系统复刻。2026-09-08 更正：旧版固定加权打分结果作废。  complementary-recommendation two-tower category-adapter e-commerce 搜广推 候选生成与搜索匹配 AlleCompanion 的 ComCat 为什么先维护类别互补关系，再训练类别约束双塔？ 互补是一种用途关系，普通共购或语义邻近不可靠地代表它。ComCat 汇合规则、人工、语言推理和统计证据，把合理类别关系先显式化，双塔与适配器再在这些空间里学习匹配。类别先验提供约束，但不能代替具体商品是否兼容的判断。 示意：相机与镜头类别互补，但具体卡口仍需匹配；两台相机虽可能被共同浏览，也不应仅凭共现当作彼此配件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-allecompanion-f53aba66" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-db05219008dd977e">AlleCompanion 的 ComCat 为什么先维护类别互补关系，再训练类别约束双塔？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aallecompanion">Beyond Co-purchase Relation: Evolution of Complementary Recommendations at Allegro</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Allegro.com</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>互补是一种用途关系，普通共购或语义邻近不可靠地代表它。ComCat 汇合规则、人工、语言推理和统计证据，把合理类别关系先显式化，双塔与适配器再在这些空间里学习匹配。类别先验提供约束，但不能代替具体商品是否兼容的判断。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>相机与镜头类别互补，但具体卡口仍需匹配；两台相机虽可能被共同浏览，也不应仅凭共现当作彼此配件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.05063">原论文</a> · <a href="../../../../reproductions/2609.05063-allecompanion/">实现解读</a> · <a href="#qa-db05219008dd977e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:allecompanion" data-paper-title="Beyond Co-purchase Relation: Evolution of Complementary Recommendations at Allegro" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Beyond Co-purchase Relation: Evolution of Complementary Recommendations at Allegro 搜广推与 LLM 应用 Allegro.com 2026-09-04 共购不等于互补：相机与另一台相机可能经常一起浏览，却不如镜头真正互补。AlleCompanion 先用 ComCat 融合专家规则、人工反馈、LLM 推理和统计挖掘形成类别关系，再用类别约束双塔和 Category Adapter 把候选限制在合理的互补空间。 复现级别：CPU 可训练检索核心。复现级别：CPU 可训练检索核心。共享内容/类别编码器、Category Adapter、混合负样本检索损失和类别重建损失均参与反向传播。MovieLens 邻接关系不是商品互补性，不声称复现 ComCat 或线上效果。ComCat 原始映射、Allegro 行为数据和生产服务未公开；本地实现的是可审计核心机制，不是生产系统复刻。2026-09-08 更正：旧版固定加权打分结果作废。  complementary-recommendation two-tower category-adapter e-commerce 搜广推 候选生成与搜索匹配 为什么有强共现关系的两件商品，仍可能不适合作为互补推荐？ 共现可以来自替代比较或流行度，互补却要求两件商品能共同完成需求。AlleCompanion先用多来源证据建立类别互补关系，再以类别约束双塔与Category Adapter学习具体匹配，避免只按相似或共购打分。推理必须对候选类别进行合法计算，不能提前读取待预测商品类别来选路。 示意：用户比较过两台相机，不代表需要一起买；镜头可能才与相机互补。类别先限定可用配件，再比较具体接口和用途是否匹配。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:allecompanion" data-paper-title="Beyond Co-purchase Relation: Evolution of Complementary Recommendations at Allegro" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Beyond Co-purchase Relation: Evolution of Complementary Recommendations at Allegro 搜广推与 LLM 应用 Allegro.com 2026-09-04 共购不等于互补：相机与另一台相机可能经常一起浏览，却不如镜头真正互补。AlleCompanion 先用 ComCat 融合专家规则、人工反馈、LLM 推理和统计挖掘形成类别关系，再用类别约束双塔和 Category Adapter 把候选限制在合理的互补空间。 复现级别：CPU 可训练检索核心。复现级别：CPU 可训练检索核心。共享内容/类别编码器、Category Adapter、混合负样本检索损失和类别重建损失均参与反向传播。MovieLens 邻接关系不是商品互补性，不声称复现 ComCat 或线上效果。ComCat 原始映射、Allegro 行为数据和生产服务未公开；本地实现的是可审计核心机制，不是生产系统复刻。2026-09-08 更正：旧版固定加权打分结果作废。  complementary-recommendation two-tower category-adapter e-commerce 搜广推 候选生成与搜索匹配 AlleCompanion 与普通同类相似召回，适用的推荐意图有何不同？ 同类召回常用于替代选择，强调功能与内容相近；互补召回寻找一起使用能满足需求的不同功能物品。两者正例定义不同，直接用 next-product 命中代替互补标签会改变任务，因此本地 Amazon 负结果不能单独证伪 ComCat 的类别知识。 示意：买帐篷后想替换型号时推荐另一顶帐篷，准备露营套装时则可能需要睡袋与防潮垫；同一候选在两种意图下的价值不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5a2ad12c1c72b9db">AlleCompanion 与普通同类相似召回，适用的推荐意图有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aallecompanion">Beyond Co-purchase Relation: Evolution of Complementary Recommendations at Allegro</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Allegro.com</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同类召回常用于替代选择，强调功能与内容相近；互补召回寻找一起使用能满足需求的不同功能物品。两者正例定义不同，直接用 next-product 命中代替互补标签会改变任务，因此本地 Amazon 负结果不能单独证伪 ComCat 的类别知识。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>买帐篷后想替换型号时推荐另一顶帐篷，准备露营套装时则可能需要睡袋与防潮垫；同一候选在两种意图下的价值不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.05063">原论文</a> · <a href="../../../../reproductions/2609.05063-allecompanion/">实现解读</a> · <a href="#qa-5a2ad12c1c72b9db">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:allecompanion" data-paper-title="Beyond Co-purchase Relation: Evolution of Complementary Recommendations at Allegro" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Beyond Co-purchase Relation: Evolution of Complementary Recommendations at Allegro 搜广推与 LLM 应用 Allegro.com 2026-09-04 共购不等于互补：相机与另一台相机可能经常一起浏览，却不如镜头真正互补。AlleCompanion 先用 ComCat 融合专家规则、人工反馈、LLM 推理和统计挖掘形成类别关系，再用类别约束双塔和 Category Adapter 把候选限制在合理的互补空间。 复现级别：CPU 可训练检索核心。复现级别：CPU 可训练检索核心。共享内容/类别编码器、Category Adapter、混合负样本检索损失和类别重建损失均参与反向传播。MovieLens 邻接关系不是商品互补性，不声称复现 ComCat 或线上效果。ComCat 原始映射、Allegro 行为数据和生产服务未公开；本地实现的是可审计核心机制，不是生产系统复刻。2026-09-08 更正：旧版固定加权打分结果作废。  complementary-recommendation two-tower category-adapter e-commerce 搜广推 候选生成与搜索匹配 AlleCompanion 本地 Category Adapter 推理时能否读取测试目标的类别？ 不能。来源明确对所有候选类别分别计算，训练只使用 train 邻接对，测试目标类别不能作为正确答案提示。公开替代任务也没有真实 ComCat 互补标签，应该保留诊断性质与负结果，不能把类别提示泄漏包装成互补推荐能力。 示意：全库评估必须让每个候选按自身类别进入模型；若先告诉模型“正确答案是镜头类”再只评镜头，就绕过了它本该完成的类别选择。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-26fc233a12d9d993">AlleCompanion 本地 Category Adapter 推理时能否读取测试目标的类别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aallecompanion">Beyond Co-purchase Relation: Evolution of Complementary Recommendations at Allegro</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Allegro.com</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。来源明确对所有候选类别分别计算，训练只使用 train 邻接对，测试目标类别不能作为正确答案提示。公开替代任务也没有真实 ComCat 互补标签，应该保留诊断性质与负结果，不能把类别提示泄漏包装成互补推荐能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>全库评估必须让每个候选按自身类别进入模型；若先告诉模型“正确答案是镜头类”再只评镜头，就绕过了它本该完成的类别选择。</p>
<p class="ar-learning-sources">依据：本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.05063">原论文</a> · <a href="../../../../reproductions/2609.05063-allecompanion/">实现解读</a> · <a href="#qa-26fc233a12d9d993">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:setmir" data-paper-title="SetMIR: Multi-Interest Retrieval as Set Prediction" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="SetMIR: Multi-Interest Retrieval as Set Prediction 搜广推与 LLM 应用 Snap Inc. 2026-08-31 SetMIR 用 K 个可学习 query 解码无序兴趣集合，Hungarian matching 强制一对一分工以抑制兴趣坍缩；presence head 判断本次请求实际需要哪些兴趣，服务时再用 query-level NMS 删除重复 ANN 请求。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现兴趣集合、presence 门控和 query-level NMS。未复刻私有 DPA 历史、生产 Transformer checkpoint 与 ANN dispatch；仅声明 CPU 公共数据路径。用公开类型簇代理兴趣 query，执行 presence 与相关性 NMS；NDCG@10 从 0.05401 到 0.05665。三 seed 产物见 metrics/public-seeds42-44.json。  multi-interest-retrieval set-prediction dynamic-dispatch 搜广推 候选生成与搜索匹配 SetMIR的query是用户手动输入的搜索词吗？ 不是。这里的query是模型产生的兴趣检索向量或槽位，用于向物品库发出ANN请求，不要求用户写出文本搜索词。多个槽位表达不同潜在兴趣，实际激活数还需由服务规则决定；向量名称相同不代表它与搜索业务中的自然语言query同义。 教学例子：用户只打开推荐页，模型仍可生成运动与摄影两个兴趣向量；这不表示用户刚输入过两个搜索词。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-setmir-231692c0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-1dbb7554298c2ace">SetMIR的query是用户手动输入的搜索词吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asetmir">SetMIR: Multi-Interest Retrieval as Set Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Snap Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。这里的query是模型产生的兴趣检索向量或槽位，用于向物品库发出ANN请求，不要求用户写出文本搜索词。多个槽位表达不同潜在兴趣，实际激活数还需由服务规则决定；向量名称相同不代表它与搜索业务中的自然语言query同义。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户只打开推荐页，模型仍可生成运动与摄影两个兴趣向量；这不表示用户刚输入过两个搜索词。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.30251">原论文</a> · <a href="../../../../reproductions/2608.30251-setmir/">实现解读</a> · <a href="#qa-1dbb7554298c2ace">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:setmir" data-paper-title="SetMIR: Multi-Interest Retrieval as Set Prediction" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="SetMIR: Multi-Interest Retrieval as Set Prediction 搜广推与 LLM 应用 Snap Inc. 2026-08-31 SetMIR 用 K 个可学习 query 解码无序兴趣集合，Hungarian matching 强制一对一分工以抑制兴趣坍缩；presence head 判断本次请求实际需要哪些兴趣，服务时再用 query-level NMS 删除重复 ANN 请求。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现兴趣集合、presence 门控和 query-level NMS。未复刻私有 DPA 历史、生产 Transformer checkpoint 与 ANN dispatch；仅声明 CPU 公共数据路径。用公开类型簇代理兴趣 query，执行 presence 与相关性 NMS；NDCG@10 从 0.05401 到 0.05665。三 seed 产物见 metrics/public-seeds42-44.json。  multi-interest-retrieval set-prediction dynamic-dispatch 搜广推 候选生成与搜索匹配 SetMIR 为什么训练时用一对一集合匹配，服务时仍要 presence head 和 query NMS？ 匹配监督让多个兴趣查询分工，减少它们都解释同一正例的坍缩，但固定查询数不代表每次请求都有同样多的真实兴趣。presence head 决定哪些查询应激活，NMS 再删除高度重复的检索请求，分别处理训练分工与服务冗余。多兴趣表达丰富并不意味着把所有查询都发出去最有效。 示意：模型最多有八个兴趣，但某次请求只明显有摄影和露营。presence 只启用相关查询，若两个都指向同一种相机，再用 NMS 合并，避免浪费两次近邻检索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:setmir" data-paper-title="SetMIR: Multi-Interest Retrieval as Set Prediction" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="SetMIR: Multi-Interest Retrieval as Set Prediction 搜广推与 LLM 应用 Snap Inc. 2026-08-31 SetMIR 用 K 个可学习 query 解码无序兴趣集合，Hungarian matching 强制一对一分工以抑制兴趣坍缩；presence head 判断本次请求实际需要哪些兴趣，服务时再用 query-level NMS 删除重复 ANN 请求。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现兴趣集合、presence 门控和 query-level NMS。未复刻私有 DPA 历史、生产 Transformer checkpoint 与 ANN dispatch；仅声明 CPU 公共数据路径。用公开类型簇代理兴趣 query，执行 presence 与相关性 NMS；NDCG@10 从 0.05401 到 0.05665。三 seed 产物见 metrics/public-seeds42-44.json。  multi-interest-retrieval set-prediction dynamic-dispatch 搜广推 候选生成与搜索匹配 SetMIR的一对一集合匹配，与让每个兴趣槽独立挑同一个正例有什么不同？ 一对一匹配在整组槽位与目标之间分配对应关系，限制多个槽反复解释同一目标；独立挑选则可能所有槽都被同一容易正例吸引。它处理训练分工，仍需可靠目标集合，不能仅因匹配唯一就认定全部用户兴趣都已被发现。 教学例子：两个槽与运动、摄影两项目标应分配不同对应；若各自贪选最容易的运动项，摄影目标可能无人负责。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-37ab5a0653ba7420">SetMIR的一对一集合匹配，与让每个兴趣槽独立挑同一个正例有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asetmir">SetMIR: Multi-Interest Retrieval as Set Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Snap Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一对一匹配在整组槽位与目标之间分配对应关系，限制多个槽反复解释同一目标；独立挑选则可能所有槽都被同一容易正例吸引。它处理训练分工，仍需可靠目标集合，不能仅因匹配唯一就认定全部用户兴趣都已被发现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个槽与运动、摄影两项目标应分配不同对应；若各自贪选最容易的运动项，摄影目标可能无人负责。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.30251">原论文</a> · <a href="../../../../reproductions/2608.30251-setmir/">实现解读</a> · <a href="#qa-37ab5a0653ba7420">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:setmir" data-paper-title="SetMIR: Multi-Interest Retrieval as Set Prediction" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="SetMIR: Multi-Interest Retrieval as Set Prediction 搜广推与 LLM 应用 Snap Inc. 2026-08-31 SetMIR 用 K 个可学习 query 解码无序兴趣集合，Hungarian matching 强制一对一分工以抑制兴趣坍缩；presence head 判断本次请求实际需要哪些兴趣，服务时再用 query-level NMS 删除重复 ANN 请求。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现兴趣集合、presence 门控和 query-level NMS。未复刻私有 DPA 历史、生产 Transformer checkpoint 与 ANN dispatch；仅声明 CPU 公共数据路径。用公开类型簇代理兴趣 query，执行 presence 与相关性 NMS；NDCG@10 从 0.05401 到 0.05665。三 seed 产物见 metrics/public-seeds42-44.json。  multi-interest-retrieval set-prediction dynamic-dispatch 搜广推 候选生成与搜索匹配 SetMIR服务时哪些query实际派发ANN？ 同时通过presence且未被query-level NMS抑制的query，不能固定全部K条都发。当前只声明公开CPU路径，未复刻私有历史、生产Transformer和ANN dispatch。 例如模型预留十个槽，不代表每个用户请求都必须做十次召回。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-9c478711239026dd">SetMIR服务时哪些query实际派发ANN？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asetmir">SetMIR: Multi-Interest Retrieval as Set Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Snap Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同时通过presence且未被query-level NMS抑制的query，不能固定全部K条都发。当前只声明公开CPU路径，未复刻私有历史、生产Transformer和ANN dispatch。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型预留十个槽，不代表每个用户请求都必须做十次召回。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.30251">原论文</a> · <a href="../../../../reproductions/2608.30251-setmir/">实现解读</a> · <a href="#qa-9c478711239026dd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:friend-gnn" data-paper-title="Scaling Graph Neural Networks for Friend Recommendation: Multi-Hash User Embeddings and Temporal Neighbor Sampling" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Scaling Graph Neural Networks for Friend Recommendation: Multi-Hash User Embeddings and Temporal Neighbor Sampling 搜广推与 LLM 应用 AI VK 2026-08-27 超大社交图既放不下完整用户 ID 表，又必须防止采到未来好友边。论文用三个独立 hash 查共享表并拼接投影，以 timestamp-sorted CSR + binary search 得到历史邻居前缀，再由 GATv2 和 query/candidate 双头打分。 Fidelity：核心机制复现。本地执行多哈希共享表、按时间排序邻接与二分 cutoff，并在公开数据上与同候选集基线比较。MovieLens 物品转移图不是好友图；未复刻 VK 私有日志、194M 用户图、分布式 GATv2 和生产 ranker。本地对照口径：基线为相同全候选目录上的 popularity ranker，实验组为 Friend-GNN 时序图 proxy；Hit@10 相对提升 247.62%，仅用于本地机制对照。  friend-recommendation graph-ranking multi-hash-embedding temporal-sampling 搜广推 候选生成与搜索匹配 Friend-GNN 为什么要同时解决用户 ID 存储和好友边时间可见性？ 超大图的逐用户表内存昂贵，多哈希共享表压缩身份表示；好友边若包含预测时点之后的新增关系，会泄漏结果。两项分别管理容量与时序正确性，GNN 传播再提取邻域信息。压缩与时间合法都不自动证明好友推荐更准。 示意：十亿用户难各存大向量，可用多个哈希组合；但预测昨天好友时仍不能采今天新增边，否则压缩再高效也只是在读未来答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-friend-gnn-0f3bf9e0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-608c9a7e5fd4b8a6">Friend-GNN 为什么要同时解决用户 ID 存储和好友边时间可见性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Afriend-gnn">Scaling Graph Neural Networks for Friend Recommendation: Multi-Hash User Embeddings and Temporal Neighbor Sampling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AI VK</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>超大图的逐用户表内存昂贵，多哈希共享表压缩身份表示；好友边若包含预测时点之后的新增关系，会泄漏结果。两项分别管理容量与时序正确性，GNN 传播再提取邻域信息。压缩与时间合法都不自动证明好友推荐更准。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>十亿用户难各存大向量，可用多个哈希组合；但预测昨天好友时仍不能采今天新增边，否则压缩再高效也只是在读未来答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27413">原论文</a> · <a href="../../../../reproductions/2608.27413-friend-gnn/">实现解读</a> · <a href="#qa-608c9a7e5fd4b8a6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:friend-gnn" data-paper-title="Scaling Graph Neural Networks for Friend Recommendation: Multi-Hash User Embeddings and Temporal Neighbor Sampling" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Scaling Graph Neural Networks for Friend Recommendation: Multi-Hash User Embeddings and Temporal Neighbor Sampling 搜广推与 LLM 应用 AI VK 2026-08-27 超大社交图既放不下完整用户 ID 表，又必须防止采到未来好友边。论文用三个独立 hash 查共享表并拼接投影，以 timestamp-sorted CSR + binary search 得到历史邻居前缀，再由 GATv2 和 query/candidate 双头打分。 Fidelity：核心机制复现。本地执行多哈希共享表、按时间排序邻接与二分 cutoff，并在公开数据上与同候选集基线比较。MovieLens 物品转移图不是好友图；未复刻 VK 私有日志、194M 用户图、分布式 GATv2 和生产 ranker。本地对照口径：基线为相同全候选目录上的 popularity ranker，实验组为 Friend-GNN 时序图 proxy；Hit@10 相对提升 247.62%，仅用于本地机制对照。  friend-recommendation graph-ranking multi-hash-embedding temporal-sampling 搜广推 候选生成与搜索匹配 Friend-GNN为什么既使用多哈希用户表示，又按时间前缀采邻居？ 多哈希共享表减少超大用户词表的存储，但哈希压缩并不解决时间泄漏。时序CSR把邻居按时间排序，查询只允许访问截止点之前的边，再由图网络聚合；否则模型可能通过未来已成好友关系猜中当前推荐。两部分分别控制内存与观测合法性，不能用图分数提高代替这两项检查。 示意：周二推荐好友时不能使用周五才新增的连接；即使用户embedding压缩得很省，采到这条未来边仍会让离线结果失真，因此必须按请求时刻截断邻居。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:friend-gnn" data-paper-title="Scaling Graph Neural Networks for Friend Recommendation: Multi-Hash User Embeddings and Temporal Neighbor Sampling" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Scaling Graph Neural Networks for Friend Recommendation: Multi-Hash User Embeddings and Temporal Neighbor Sampling 搜广推与 LLM 应用 AI VK 2026-08-27 超大社交图既放不下完整用户 ID 表，又必须防止采到未来好友边。论文用三个独立 hash 查共享表并拼接投影，以 timestamp-sorted CSR + binary search 得到历史邻居前缀，再由 GATv2 和 query/candidate 双头打分。 Fidelity：核心机制复现。本地执行多哈希共享表、按时间排序邻接与二分 cutoff，并在公开数据上与同候选集基线比较。MovieLens 物品转移图不是好友图；未复刻 VK 私有日志、194M 用户图、分布式 GATv2 和生产 ranker。本地对照口径：基线为相同全候选目录上的 popularity ranker，实验组为 Friend-GNN 时序图 proxy；Hit@10 相对提升 247.62%，仅用于本地机制对照。  friend-recommendation graph-ranking multi-hash-embedding temporal-sampling 搜广推 候选生成与搜索匹配 三个独立 hash 拼接与单 hash embedding，相比为何能缓解碰撞而非消除碰撞？ 单哈希把同桶用户压成同表示，多哈希让身份由多组地址组合，两个用户全部地址相同的机会更低，投影再融合。共享表仍会产生部分冲突，存储与精度存在取舍。它不是完整独立 ID 表，不能声称每个用户唯一可辨。 示意：甲乙第一桶相同但另两桶不同，组合仍可区分；若三个桶都撞上，模型也不能靠这个编码恢复两人的独立身份。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1d0825584eb05ffd">三个独立 hash 拼接与单 hash embedding，相比为何能缓解碰撞而非消除碰撞？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Afriend-gnn">Scaling Graph Neural Networks for Friend Recommendation: Multi-Hash User Embeddings and Temporal Neighbor Sampling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AI VK</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单哈希把同桶用户压成同表示，多哈希让身份由多组地址组合，两个用户全部地址相同的机会更低，投影再融合。共享表仍会产生部分冲突，存储与精度存在取舍。它不是完整独立 ID 表，不能声称每个用户唯一可辨。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>甲乙第一桶相同但另两桶不同，组合仍可区分；若三个桶都撞上，模型也不能靠这个编码恢复两人的独立身份。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27413">原论文</a> · <a href="../../../../reproductions/2608.27413-friend-gnn/">实现解读</a> · <a href="#qa-1d0825584eb05ffd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:friend-gnn" data-paper-title="Scaling Graph Neural Networks for Friend Recommendation: Multi-Hash User Embeddings and Temporal Neighbor Sampling" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Scaling Graph Neural Networks for Friend Recommendation: Multi-Hash User Embeddings and Temporal Neighbor Sampling 搜广推与 LLM 应用 AI VK 2026-08-27 超大社交图既放不下完整用户 ID 表，又必须防止采到未来好友边。论文用三个独立 hash 查共享表并拼接投影，以 timestamp-sorted CSR + binary search 得到历史邻居前缀，再由 GATv2 和 query/candidate 双头打分。 Fidelity：核心机制复现。本地执行多哈希共享表、按时间排序邻接与二分 cutoff，并在公开数据上与同候选集基线比较。MovieLens 物品转移图不是好友图；未复刻 VK 私有日志、194M 用户图、分布式 GATv2 和生产 ranker。本地对照口径：基线为相同全候选目录上的 popularity ranker，实验组为 Friend-GNN 时序图 proxy；Hit@10 相对提升 247.62%，仅用于本地机制对照。  friend-recommendation graph-ranking multi-hash-embedding temporal-sampling 搜广推 候选生成与搜索匹配 时序 CSR 采样为什么要对每个用户邻居时间排序后取历史前缀？ 二分查找只能在有序时间数组中定位 τ−Δ 截止，随后仅从合法前缀采邻居，避免未来边进入消息传播。边界是严格前缀还是包含截止需遵循 lower_bound 定义，不能用当前全图过滤的口头声明代替实际索引。 示意：邻居边按一月、二月、三月排列，预测二月前只取早于截止的部分；若数组未排序，二分结果可能把三月未来边藏进采样集合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f8d5d303c99adcd3">时序 CSR 采样为什么要对每个用户邻居时间排序后取历史前缀？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Afriend-gnn">Scaling Graph Neural Networks for Friend Recommendation: Multi-Hash User Embeddings and Temporal Neighbor Sampling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AI VK</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>二分查找只能在有序时间数组中定位 τ−Δ 截止，随后仅从合法前缀采邻居，避免未来边进入消息传播。边界是严格前缀还是包含截止需遵循 lower_bound 定义，不能用当前全图过滤的口头声明代替实际索引。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>邻居边按一月、二月、三月排列，预测二月前只取早于截止的部分；若数组未排序，二分结果可能把三月未来边藏进采样集合。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27413">原论文</a> · <a href="../../../../reproductions/2608.27413-friend-gnn/">实现解读</a> · <a href="#qa-f8d5d303c99adcd3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:transretrieval" data-paper-title="TransRetrieval: Scaling Up Transformer-Based Retrieval for Industrial Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="TransRetrieval: Scaling Up Transformer-Based Retrieval for Industrial Recommendation 搜广推与 LLM 应用 Renmin University of China / Taobao &amp; Tmall Group, Alibaba 2026-08-26 跨域广告召回同时受源域噪声、目标域 token 成本和域信息混淆影响。论文按 token norm 聚合源历史，把多个 target tokens 压为一个，并以位置形式注入 domain embedding，减少 target attention 开销。 85% target FLOPs reduction 是结构诊断，不是端到端延迟实测。Fidelity：核心机制复现。本地执行 norm-aware 聚合、target-token 压缩和位置化 domain embedding。未使用论文的 400 亿交互、5200 万广告和生产 ANN；85% target FLOPs reduction 是结构诊断，不是端到端延迟实测。本地对照口径：基线为 Transformer two-tower；实验组加入三项核心机制。MovieLens-1M Hit@10 0.1063 → 0.1187（+11.76%），NDCG@10 0.05429 → 0.05473（+0.81%）。  retrieval transformer-scaling target-token-compression multi-domain 搜广推 候选生成与搜索匹配 TransRetrieval为什么同时压源历史与目标tokens？ 跨域源域噪声和目标多token都会抬高attention成本，norm-aware聚合与目标压缩分别处理两端，域embedding再减少信息混淆。压缩不保证无信息损失。 例如许多源行为先汇总，目标侧多字段合一后再交互。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-transretrieval-4252b15a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-74ee6b5fb450fd19">TransRetrieval为什么同时压源历史与目标tokens？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atransretrieval">TransRetrieval: Scaling Up Transformer-Based Retrieval for Industrial Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Renmin University of China / Taobao &amp; Tmall Group, Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>跨域源域噪声和目标多token都会抬高attention成本，norm-aware聚合与目标压缩分别处理两端，域embedding再减少信息混淆。压缩不保证无信息损失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如许多源行为先汇总，目标侧多字段合一后再交互。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25528">原论文</a> · <a href="../../../../reproductions/2608.25528-transretrieval/">实现解读</a> · <a href="#qa-74ee6b5fb450fd19">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:transretrieval" data-paper-title="TransRetrieval: Scaling Up Transformer-Based Retrieval for Industrial Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="TransRetrieval: Scaling Up Transformer-Based Retrieval for Industrial Recommendation 搜广推与 LLM 应用 Renmin University of China / Taobao &amp; Tmall Group, Alibaba 2026-08-26 跨域广告召回同时受源域噪声、目标域 token 成本和域信息混淆影响。论文按 token norm 聚合源历史，把多个 target tokens 压为一个，并以位置形式注入 domain embedding，减少 target attention 开销。 85% target FLOPs reduction 是结构诊断，不是端到端延迟实测。Fidelity：核心机制复现。本地执行 norm-aware 聚合、target-token 压缩和位置化 domain embedding。未使用论文的 400 亿交互、5200 万广告和生产 ANN；85% target FLOPs reduction 是结构诊断，不是端到端延迟实测。本地对照口径：基线为 Transformer two-tower；实验组加入三项核心机制。MovieLens-1M Hit@10 0.1063 → 0.1187（+11.76%），NDCG@10 0.05429 → 0.05473（+0.81%）。  retrieval transformer-scaling target-token-compression multi-domain 搜广推 候选生成与搜索匹配 TransRetrieval 为什么按 token norm 聚合源域历史，并压缩目标域 token、注入域位置信息？ 源域行为多却可能带噪声，范数加权聚合提供不同于等权平均的信号选择；目标 token 压缩减少跨域注意力成本，域位置信息帮助模型区分相同表示在不同业务中的含义。三项分别控制源噪声、目标计算和域混淆，但高范数不必然等于高相关，压缩也可能损失目标域细节。 示意：阅读域历史迁移到广告召回时，先聚合行为，再把目标侧多种字段压成紧凑表示，同时标明来自哪个域，避免把“收藏文章”和“购买商品”误作相同动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:transretrieval" data-paper-title="TransRetrieval: Scaling Up Transformer-Based Retrieval for Industrial Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="TransRetrieval: Scaling Up Transformer-Based Retrieval for Industrial Recommendation 搜广推与 LLM 应用 Renmin University of China / Taobao &amp; Tmall Group, Alibaba 2026-08-26 跨域广告召回同时受源域噪声、目标域 token 成本和域信息混淆影响。论文按 token norm 聚合源历史，把多个 target tokens 压为一个，并以位置形式注入 domain embedding，减少 target attention 开销。 85% target FLOPs reduction 是结构诊断，不是端到端延迟实测。Fidelity：核心机制复现。本地执行 norm-aware 聚合、target-token 压缩和位置化 domain embedding。未使用论文的 400 亿交互、5200 万广告和生产 ANN；85% target FLOPs reduction 是结构诊断，不是端到端延迟实测。本地对照口径：基线为 Transformer two-tower；实验组加入三项核心机制。MovieLens-1M Hit@10 0.1063 → 0.1187（+11.76%），NDCG@10 0.05429 → 0.05473（+0.81%）。  retrieval transformer-scaling target-token-compression multi-domain 搜广推 候选生成与搜索匹配 按norm加权与直接平均源token有什么不同？ 大norm表示获得更大权重，平均则各项同权；norm是否代表有用性依模型和校准，不能当真实因果重要度。域位置编码也不能仅用一个共享常数替代。 例如某噪声特征幅度很大时，norm策略可能需要额外审查。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0be0037018c4d9ac">按norm加权与直接平均源token有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atransretrieval">TransRetrieval: Scaling Up Transformer-Based Retrieval for Industrial Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Renmin University of China / Taobao &amp; Tmall Group, Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>大norm表示获得更大权重，平均则各项同权；norm是否代表有用性依模型和校准，不能当真实因果重要度。域位置编码也不能仅用一个共享常数替代。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某噪声特征幅度很大时，norm策略可能需要额外审查。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25528">原论文</a> · <a href="../../../../reproductions/2608.25528-transretrieval/">实现解读</a> · <a href="#qa-0be0037018c4d9ac">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:transretrieval" data-paper-title="TransRetrieval: Scaling Up Transformer-Based Retrieval for Industrial Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="TransRetrieval: Scaling Up Transformer-Based Retrieval for Industrial Recommendation 搜广推与 LLM 应用 Renmin University of China / Taobao &amp; Tmall Group, Alibaba 2026-08-26 跨域广告召回同时受源域噪声、目标域 token 成本和域信息混淆影响。论文按 token norm 聚合源历史，把多个 target tokens 压为一个，并以位置形式注入 domain embedding，减少 target attention 开销。 85% target FLOPs reduction 是结构诊断，不是端到端延迟实测。Fidelity：核心机制复现。本地执行 norm-aware 聚合、target-token 压缩和位置化 domain embedding。未使用论文的 400 亿交互、5200 万广告和生产 ANN；85% target FLOPs reduction 是结构诊断，不是端到端延迟实测。本地对照口径：基线为 Transformer two-tower；实验组加入三项核心机制。MovieLens-1M Hit@10 0.1063 → 0.1187（+11.76%），NDCG@10 0.05429 → 0.05473（+0.81%）。  retrieval transformer-scaling target-token-compression multi-domain 搜广推 候选生成与搜索匹配 85% target FLOPs reduction可直接写成端到端时延降低吗？ 不可以，结构计数不包含访存、其他层和服务开销。当前没有原40B交互、千万广告和ANN，需区分目标分支解析节约与实测整体速度。 例如attention少很多算式，若预处理或检索占主要时间，延迟不会同倍下降。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-21beb67cd46b2b17">85% target FLOPs reduction可直接写成端到端时延降低吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atransretrieval">TransRetrieval: Scaling Up Transformer-Based Retrieval for Industrial Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Renmin University of China / Taobao &amp; Tmall Group, Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不可以，结构计数不包含访存、其他层和服务开销。当前没有原40B交互、千万广告和ANN，需区分目标分支解析节约与实测整体速度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如attention少很多算式，若预处理或检索占主要时间，延迟不会同倍下降。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25528">原论文</a> · <a href="../../../../reproductions/2608.25528-transretrieval/">实现解读</a> · <a href="#qa-21beb67cd46b2b17">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:spear" data-paper-title="SPEAR: Selection-aware Personalized End-to-end Adaptive Rewriting and Retrieval for Community Search" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="SPEAR: Selection-aware Personalized End-to-end Adaptive Rewriting and Retrieval for Community Search 搜广推与 LLM 应用 Dewu 2026-08-03 端到端改写—检索容易让通用词凭高 path score 胜出、偏离原 query。SPEAR 用双 embedding 和梯度隔离保护 recall 语义，以 rewrite confidence × item relevance 的乘法门消除捷径，再由动态 selector 产生 request-specific 权重、scale 和 bias。 Fidelity：核心机制复现。公开数据只验证论文机制，不模拟生产流量。MovieLens item 内容代理商品/帖子，未复刻得物 query rewrite generator、私有 session 与线上排序链路。本地对照口径：基线为共享 transition + content scorer，实验组只加入 SPEAR 核心机制；相对 NDCG@10 +26.95%。  search query-rewriting retrieval personalization 搜广推 候选生成与搜索匹配 推荐SPEAR为什么保护原query召回语义？ 通用改写词可能凭高路径分走捷径，偏离用户原意。双embedding与梯度隔离保留原召回结构，再用改写置信乘物品相关性门控，让个性化不任意放大。 例如想搜跑鞋，宽泛运动改写不能仅靠流行度把无关内容推上来。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-spear-7c6c6f8e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d1837bff0f6de91d">推荐SPEAR为什么保护原query召回语义？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aspear">SPEAR: Selection-aware Personalized End-to-end Adaptive Rewriting and Retrieval for Community Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dewu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>通用改写词可能凭高路径分走捷径，偏离用户原意。双embedding与梯度隔离保留原召回结构，再用改写置信乘物品相关性门控，让个性化不任意放大。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如想搜跑鞋，宽泛运动改写不能仅靠流行度把无关内容推上来。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01738">原论文</a> · <a href="../../../../reproductions/2608.01738-spear/">实现解读</a> · <a href="#qa-d1837bff0f6de91d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:spear" data-paper-title="SPEAR: Selection-aware Personalized End-to-end Adaptive Rewriting and Retrieval for Community Search" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="SPEAR: Selection-aware Personalized End-to-end Adaptive Rewriting and Retrieval for Community Search 搜广推与 LLM 应用 Dewu 2026-08-03 端到端改写—检索容易让通用词凭高 path score 胜出、偏离原 query。SPEAR 用双 embedding 和梯度隔离保护 recall 语义，以 rewrite confidence × item relevance 的乘法门消除捷径，再由动态 selector 产生 request-specific 权重、scale 和 bias。 Fidelity：核心机制复现。公开数据只验证论文机制，不模拟生产流量。MovieLens item 内容代理商品/帖子，未复刻得物 query rewrite generator、私有 session 与线上排序链路。本地对照口径：基线为共享 transition + content scorer，实验组只加入 SPEAR 核心机制；相对 NDCG@10 +26.95%。  search query-rewriting retrieval personalization 搜广推 候选生成与搜索匹配 SPEAR 为什么将改写置信度与物品相关性相乘，并隔离召回与排序 embedding 的梯度？ 端到端训练可能让泛化词靠高路径分数取胜，即使它偏离原查询。乘法门要求改写可信且对应物品相关，单项再高也不能轻易走捷径；双表示与梯度隔离保护召回语义不被排序目标任意扭曲。动态 selector 再做请求级校准，仍需检查置信度是否可靠，不能只用一个高总分证明改写正确。 示意：把“防水登山鞋”改成“热门商品”可能得到高点击路径，但改写置信度应低；乘法门压低这条捷径，让真正保留防水需求的改写更有机会。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:spear" data-paper-title="SPEAR: Selection-aware Personalized End-to-end Adaptive Rewriting and Retrieval for Community Search" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="SPEAR: Selection-aware Personalized End-to-end Adaptive Rewriting and Retrieval for Community Search 搜广推与 LLM 应用 Dewu 2026-08-03 端到端改写—检索容易让通用词凭高 path score 胜出、偏离原 query。SPEAR 用双 embedding 和梯度隔离保护 recall 语义，以 rewrite confidence × item relevance 的乘法门消除捷径，再由动态 selector 产生 request-specific 权重、scale 和 bias。 Fidelity：核心机制复现。公开数据只验证论文机制，不模拟生产流量。MovieLens item 内容代理商品/帖子，未复刻得物 query rewrite generator、私有 session 与线上排序链路。本地对照口径：基线为共享 transition + content scorer，实验组只加入 SPEAR 核心机制；相对 NDCG@10 +26.95%。  search query-rewriting retrieval personalization 搜广推 候选生成与搜索匹配 乘法门与改写置信加相关分有什么不同？ 乘法需要两者共同支持，一项低就限制贡献；加法可能由极高另一项补偿无关改写。动态selector还调request级scale和bias，不能只加两个静态分冒充。 例如改写很自信但商品不相关时，不该凭置信单独拿高分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a7ebe4a3068ccbd8">乘法门与改写置信加相关分有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aspear">SPEAR: Selection-aware Personalized End-to-end Adaptive Rewriting and Retrieval for Community Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dewu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>乘法需要两者共同支持，一项低就限制贡献；加法可能由极高另一项补偿无关改写。动态selector还调request级scale和bias，不能只加两个静态分冒充。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如改写很自信但商品不相关时，不该凭置信单独拿高分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01738">原论文</a> · <a href="../../../../reproductions/2608.01738-spear/">实现解读</a> · <a href="#qa-a7ebe4a3068ccbd8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:spear" data-paper-title="SPEAR: Selection-aware Personalized End-to-end Adaptive Rewriting and Retrieval for Community Search" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="SPEAR: Selection-aware Personalized End-to-end Adaptive Rewriting and Retrieval for Community Search 搜广推与 LLM 应用 Dewu 2026-08-03 端到端改写—检索容易让通用词凭高 path score 胜出、偏离原 query。SPEAR 用双 embedding 和梯度隔离保护 recall 语义，以 rewrite confidence × item relevance 的乘法门消除捷径，再由动态 selector 产生 request-specific 权重、scale 和 bias。 Fidelity：核心机制复现。公开数据只验证论文机制，不模拟生产流量。MovieLens item 内容代理商品/帖子，未复刻得物 query rewrite generator、私有 session 与线上排序链路。本地对照口径：基线为共享 transition + content scorer，实验组只加入 SPEAR 核心机制；相对 NDCG@10 +26.95%。  search query-rewriting retrieval personalization 搜广推 候选生成与搜索匹配 本地SPEAR双路代理是否等于真实query rewrite generator？ 不是，MovieLens内容代理商品帖子，没有私有query会话和生产生成器。梯度隔离应保护相应embedding路径，原query分仍保留，不能用测试行为挑改写。 例如提供一条手写改写后打分，未测模型是否会生成它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-38144047487ed4ce">本地SPEAR双路代理是否等于真实query rewrite generator？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aspear">SPEAR: Selection-aware Personalized End-to-end Adaptive Rewriting and Retrieval for Community Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dewu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是，MovieLens内容代理商品帖子，没有私有query会话和生产生成器。梯度隔离应保护相应embedding路径，原query分仍保留，不能用测试行为挑改写。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如提供一条手写改写后打分，未测模型是否会生成它。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01738">原论文</a> · <a href="../../../../reproductions/2608.01738-spear/">实现解读</a> · <a href="#qa-38144047487ed4ce">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:asarl" data-paper-title="ASARL: Autonomous Social-Aware Relevance Learning for QQ Search" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="ASARL: Autonomous Social-Aware Relevance Learning for QQ Search 搜广推与 LLM 应用 Tencent PCG 2026-07-29 QQ 群与频道搜索面对口语化标题、长尾数据和行为漂移。ASARL 用 ReasonAgent 产出 intent–attribute reasoning 与三级相关性标签，CriticAgent 反复校验并检测分布缺口，GenAgent 为长尾区域补样本；随后执行 Social Context Training、基于交互信号的 Preference-Guided Optimization，最后蒸馏到可在线服务的小模型。 Fidelity: 核心机制复现。实际执行多 Agent 数据整理、SCT、偏好优化与 social distillation；闭源 LLM 和 QQ 私有日志未复刻。没有 QQ 私有 query-title 日志、生产 LLM 标注 Agent 或线上 RoBERTa。这里验证的是闭环数据整理、偏好阶段和蒸馏路径；MovieLens genre 代理造成的负迁移被原样保留。本地对照口径：基线与实验组使用同一 MovieLens relevance proxy、student 参数量、训练划分和 seed；实验组增加 Reason/Critic/Gen、PGO 与蒸馏，相对 NDCG@10 为 -72.72%。  search-relevance multi-agent-data-curation knowledge-distillation 搜广推 候选生成与搜索匹配 ASARL 为什么先学习三级社交相关性，再将 teacher 蒸馏为线上 student？ 社交标题常口语化且长尾，先用上下文推理与三级标签形成较细监督，训练教师理解意图与属性，再把标签分布迁移给较小模型。昂贵数据整理和推理位于训练侧，在线保留轻量判别。标签层次帮助区分相关程度，却仍需验证与真实搜索需求一致。 示意：“周末组队”在游戏频道与徒步群语境不同，教师先结合社交属性判断强相关、弱相关或无关，再教小模型做快速在线预测。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-asarl-181d0e5f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5c546964529a7273">ASARL 为什么先学习三级社交相关性，再将 teacher 蒸馏为线上 student？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aasarl">ASARL: Autonomous Social-Aware Relevance Learning for QQ Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent PCG</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>社交标题常口语化且长尾，先用上下文推理与三级标签形成较细监督，训练教师理解意图与属性，再把标签分布迁移给较小模型。昂贵数据整理和推理位于训练侧，在线保留轻量判别。标签层次帮助区分相关程度，却仍需验证与真实搜索需求一致。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>“周末组队”在游戏频道与徒步群语境不同，教师先结合社交属性判断强相关、弱相关或无关，再教小模型做快速在线预测。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26593">原论文</a> · <a href="../../../../reproductions/2607.26593-asarl/">实现解读</a> · <a href="#qa-5c546964529a7273">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:asarl" data-paper-title="ASARL: Autonomous Social-Aware Relevance Learning for QQ Search" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="ASARL: Autonomous Social-Aware Relevance Learning for QQ Search 搜广推与 LLM 应用 Tencent PCG 2026-07-29 QQ 群与频道搜索面对口语化标题、长尾数据和行为漂移。ASARL 用 ReasonAgent 产出 intent–attribute reasoning 与三级相关性标签，CriticAgent 反复校验并检测分布缺口，GenAgent 为长尾区域补样本；随后执行 Social Context Training、基于交互信号的 Preference-Guided Optimization，最后蒸馏到可在线服务的小模型。 Fidelity: 核心机制复现。实际执行多 Agent 数据整理、SCT、偏好优化与 social distillation；闭源 LLM 和 QQ 私有日志未复刻。没有 QQ 私有 query-title 日志、生产 LLM 标注 Agent 或线上 RoBERTa。这里验证的是闭环数据整理、偏好阶段和蒸馏路径；MovieLens genre 代理造成的负迁移被原样保留。本地对照口径：基线与实验组使用同一 MovieLens relevance proxy、student 参数量、训练划分和 seed；实验组增加 Reason/Critic/Gen、PGO 与蒸馏，相对 NDCG@10 为 -72.72%。  search-relevance multi-agent-data-curation knowledge-distillation 搜广推 候选生成与搜索匹配 ASARL中的Critic与GenAgent为什么不能被一次LLM标注替代？ 一次标注可能沿用原数据的偏差并漏掉长尾意图。ReasonAgent提出推理与等级，Critic反复校验并定位分布缺口，GenAgent再补对应样本；随后用交互反馈优化偏好并蒸馏给低延迟学生。补样本必须服务已识别的缺口，不能把未经行为校验的生成理由直接视作真标签。 示意：群名中的口语缩写被误判后，Critic发现某类校园查询持续出错，生成模块补这类对照，而不是均匀增加一批与缺口无关的样本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:asarl" data-paper-title="ASARL: Autonomous Social-Aware Relevance Learning for QQ Search" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="ASARL: Autonomous Social-Aware Relevance Learning for QQ Search 搜广推与 LLM 应用 Tencent PCG 2026-07-29 QQ 群与频道搜索面对口语化标题、长尾数据和行为漂移。ASARL 用 ReasonAgent 产出 intent–attribute reasoning 与三级相关性标签，CriticAgent 反复校验并检测分布缺口，GenAgent 为长尾区域补样本；随后执行 Social Context Training、基于交互信号的 Preference-Guided Optimization，最后蒸馏到可在线服务的小模型。 Fidelity: 核心机制复现。实际执行多 Agent 数据整理、SCT、偏好优化与 social distillation；闭源 LLM 和 QQ 私有日志未复刻。没有 QQ 私有 query-title 日志、生产 LLM 标注 Agent 或线上 RoBERTa。这里验证的是闭环数据整理、偏好阶段和蒸馏路径；MovieLens genre 代理造成的负迁移被原样保留。本地对照口径：基线与实验组使用同一 MovieLens relevance proxy、student 参数量、训练划分和 seed；实验组增加 Reason/Critic/Gen、PGO 与蒸馏，相对 NDCG@10 为 -72.72%。  search-relevance multi-agent-data-curation knowledge-distillation 搜广推 候选生成与搜索匹配 ASARL 的 PGO 与仅用合成三级标签做监督，差别在哪里？ 合成标签主要来自模型解释和审查，PGO 进一步使用交互信号验证的正负推理—标签序列，以相对偏好约束教师。两者证据来源不同，后者意在校准合成判断，但仍可能受行为偏差影响。不能把分类 loss 下降直接视为下游检索效果提升。 示意：模型觉得“摄影交流群”很相关，用户实际更偏好特定机型群；经过行为验证的胜负序列可纠正一般相关性，却不能只靠更好拟合合成标签做到。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-36bcca6a95183b32">ASARL 的 PGO 与仅用合成三级标签做监督，差别在哪里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aasarl">ASARL: Autonomous Social-Aware Relevance Learning for QQ Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent PCG</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>合成标签主要来自模型解释和审查，PGO 进一步使用交互信号验证的正负推理—标签序列，以相对偏好约束教师。两者证据来源不同，后者意在校准合成判断，但仍可能受行为偏差影响。不能把分类 loss 下降直接视为下游检索效果提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型觉得“摄影交流群”很相关，用户实际更偏好特定机型群；经过行为验证的胜负序列可纠正一般相关性，却不能只靠更好拟合合成标签做到。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26593">原论文</a> · <a href="../../../../reproductions/2607.26593-asarl/">实现解读</a> · <a href="#qa-36bcca6a95183b32">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:asarl" data-paper-title="ASARL: Autonomous Social-Aware Relevance Learning for QQ Search" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="ASARL: Autonomous Social-Aware Relevance Learning for QQ Search 搜广推与 LLM 应用 Tencent PCG 2026-07-29 QQ 群与频道搜索面对口语化标题、长尾数据和行为漂移。ASARL 用 ReasonAgent 产出 intent–attribute reasoning 与三级相关性标签，CriticAgent 反复校验并检测分布缺口，GenAgent 为长尾区域补样本；随后执行 Social Context Training、基于交互信号的 Preference-Guided Optimization，最后蒸馏到可在线服务的小模型。 Fidelity: 核心机制复现。实际执行多 Agent 数据整理、SCT、偏好优化与 social distillation；闭源 LLM 和 QQ 私有日志未复刻。没有 QQ 私有 query-title 日志、生产 LLM 标注 Agent 或线上 RoBERTa。这里验证的是闭环数据整理、偏好阶段和蒸馏路径；MovieLens genre 代理造成的负迁移被原样保留。本地对照口径：基线与实验组使用同一 MovieLens relevance proxy、student 参数量、训练划分和 seed；实验组增加 Reason/Critic/Gen、PGO 与蒸馏，相对 NDCG@10 为 -72.72%。  search-relevance multi-agent-data-curation knowledge-distillation 搜广推 候选生成与搜索匹配 ASARL 蒸馏时 KL 的对象是自然语言理由还是标签分布？ 来源的在线 student 最小化教师与学生的标签分布 KL，理由主要支持数据与教师训练，不要求小模型在线复述完整推理。本地 MovieLens 使用 genre 交集代理社交属性，分类改善却未迁移到排序，不能把这个替代标签当作真实社交搜索评估。 示意：教师给强、弱、无关三个概率，小模型学习这组三元分布即可快速服务；让它逐字生成长理由会变成另一条在线成本路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f737fc745ada373a">ASARL 蒸馏时 KL 的对象是自然语言理由还是标签分布？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aasarl">ASARL: Autonomous Social-Aware Relevance Learning for QQ Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent PCG</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>来源的在线 student 最小化教师与学生的标签分布 KL，理由主要支持数据与教师训练，不要求小模型在线复述完整推理。本地 MovieLens 使用 genre 交集代理社交属性，分类改善却未迁移到排序，不能把这个替代标签当作真实社交搜索评估。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教师给强、弱、无关三个概率，小模型学习这组三元分布即可快速服务；让它逐字生成长理由会变成另一条在线成本路径。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26593">原论文</a> · <a href="../../../../reproductions/2607.26593-asarl/">实现解读</a> · <a href="#qa-f737fc745ada373a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:oneshot-index" data-paper-title="OneShot: Index-in-Ranking with Neural Scoring for Large-Scale Retrieval" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="OneShot: Index-in-Ranking with Neural Scoring for Large-Scale Retrieval 搜广推与 LLM 应用 Meta / Instagram 2026-07-29 传统 ANN 索引按 embedding 几何邻近性组织物品，而排序目标直接优化用户行为，两者不一致。OneShot 在模型内共同学习层级索引和排序：前向使用离散路径，反向用 straight-through estimator；全局路径平衡避免热门桶拥塞；候选进入路径后再使用比点积更强的 neural scoring。 Fidelity: 核心机制复现。本地执行 ranking-shaped 分层索引、路径探测和非点积 neural scoring；确定性 assignment 代理生产训练中的 STE 与全局平衡优化。未复刻 Instagram 私有数据、十亿物品多机索引、STE 训练 kernel、SCO 全局平衡与线上检索服务；本地结果不等同论文复现指标。本地对照口径：基线为同数据、同全库评测的 two-tower 点积检索；实验组加入 ranking-shaped 分层索引和 neural scoring，NDCG@10 相对 -7.70%。  retrieval learnable-index neural-scoring serving 搜广推 候选生成与搜索匹配 OneShot 为什么把索引路径当模型的一部分，而非训练后再聚类？ 训练后索引只按既有向量几何组织，可能和神经排序目标不一致。联合索引让行为损失影响分桶，候选进入路径后再用强评分器区分。离散路由与平衡约束仍可能降低覆盖，学习式索引不能保证所有规模都获益。 示意：文本相似但受众不同商品可因排序监督分开；若先固定几何桶，强评分器再好也只能在被召回桶里工作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-oneshot-index-d86efe4f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-09ee1ff47d178754">OneShot 为什么把索引路径当模型的一部分，而非训练后再聚类？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aoneshot-index">OneShot: Index-in-Ranking with Neural Scoring for Large-Scale Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta / Instagram</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>训练后索引只按既有向量几何组织，可能和神经排序目标不一致。联合索引让行为损失影响分桶，候选进入路径后再用强评分器区分。离散路由与平衡约束仍可能降低覆盖，学习式索引不能保证所有规模都获益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>文本相似但受众不同商品可因排序监督分开；若先固定几何桶，强评分器再好也只能在被召回桶里工作。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27475">原论文</a> · <a href="../../../../reproductions/2607.27475-oneshot-index/">实现解读</a> · <a href="#qa-09ee1ff47d178754">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:oneshot-index" data-paper-title="OneShot: Index-in-Ranking with Neural Scoring for Large-Scale Retrieval" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="OneShot: Index-in-Ranking with Neural Scoring for Large-Scale Retrieval 搜广推与 LLM 应用 Meta / Instagram 2026-07-29 传统 ANN 索引按 embedding 几何邻近性组织物品，而排序目标直接优化用户行为，两者不一致。OneShot 在模型内共同学习层级索引和排序：前向使用离散路径，反向用 straight-through estimator；全局路径平衡避免热门桶拥塞；候选进入路径后再使用比点积更强的 neural scoring。 Fidelity: 核心机制复现。本地执行 ranking-shaped 分层索引、路径探测和非点积 neural scoring；确定性 assignment 代理生产训练中的 STE 与全局平衡优化。未复刻 Instagram 私有数据、十亿物品多机索引、STE 训练 kernel、SCO 全局平衡与线上检索服务；本地结果不等同论文复现指标。本地对照口径：基线为同数据、同全库评测的 two-tower 点积检索；实验组加入 ranking-shaped 分层索引和 neural scoring，NDCG@10 相对 -7.70%。  retrieval learnable-index neural-scoring serving 搜广推 候选生成与搜索匹配 OneShot 如何让离散层级索引受到排序目标训练，而不只按 embedding 距离分桶？ 前向时物品走离散索引路径，反向用 straight-through 近似把排序损失传回路径分配参数，因此“分到哪个桶”能受到行为目标影响。全局平衡抑制热门路径拥塞，入桶候选再用更强的神经评分。索引与排序共同学习减少目标割裂，但梯度是近似的，桶平衡也不能代替真实相关性。 示意：两个商品文本相似，却面向不同购买人群。几何索引可能把它们放在一起，排序监督则可推动路径分开；同时平衡约束避免所有热门商品挤进同一个桶。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:oneshot-index" data-paper-title="OneShot: Index-in-Ranking with Neural Scoring for Large-Scale Retrieval" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="OneShot: Index-in-Ranking with Neural Scoring for Large-Scale Retrieval 搜广推与 LLM 应用 Meta / Instagram 2026-07-29 传统 ANN 索引按 embedding 几何邻近性组织物品，而排序目标直接优化用户行为，两者不一致。OneShot 在模型内共同学习层级索引和排序：前向使用离散路径，反向用 straight-through estimator；全局路径平衡避免热门桶拥塞；候选进入路径后再使用比点积更强的 neural scoring。 Fidelity: 核心机制复现。本地执行 ranking-shaped 分层索引、路径探测和非点积 neural scoring；确定性 assignment 代理生产训练中的 STE 与全局平衡优化。未复刻 Instagram 私有数据、十亿物品多机索引、STE 训练 kernel、SCO 全局平衡与线上检索服务；本地结果不等同论文复现指标。本地对照口径：基线为同数据、同全库评测的 two-tower 点积检索；实验组加入 ranking-shaped 分层索引和 neural scoring，NDCG@10 相对 -7.70%。  retrieval learnable-index neural-scoring serving 搜广推 候选生成与搜索匹配 OneShot 的全局路径平衡与热门度惩罚，作用对象为何不同？ 路径平衡控制桶的资源与负载，避免索引拥塞；热门度惩罚直接改变物品推荐偏好。平衡桶不等于减少头部曝光，可能只是把热门项分散到多个桶。机制与业务分布应分别测量，不能用均匀索引占用代替推荐公平性。 示意：十件热门商品被平均放入十桶，最终仍可全被推荐；桶不拥挤了，但曝光依然头部，两个现象不能混称。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ae072d6a59aa6979">OneShot 的全局路径平衡与热门度惩罚，作用对象为何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aoneshot-index">OneShot: Index-in-Ranking with Neural Scoring for Large-Scale Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta / Instagram</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>路径平衡控制桶的资源与负载，避免索引拥塞；热门度惩罚直接改变物品推荐偏好。平衡桶不等于减少头部曝光，可能只是把热门项分散到多个桶。机制与业务分布应分别测量，不能用均匀索引占用代替推荐公平性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>十件热门商品被平均放入十桶，最终仍可全被推荐；桶不拥挤了，但曝光依然头部，两个现象不能混称。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27475">原论文</a> · <a href="../../../../reproductions/2607.27475-oneshot-index/">实现解读</a> · <a href="#qa-ae072d6a59aa6979">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:oneshot-index" data-paper-title="OneShot: Index-in-Ranking with Neural Scoring for Large-Scale Retrieval" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="OneShot: Index-in-Ranking with Neural Scoring for Large-Scale Retrieval 搜广推与 LLM 应用 Meta / Instagram 2026-07-29 传统 ANN 索引按 embedding 几何邻近性组织物品，而排序目标直接优化用户行为，两者不一致。OneShot 在模型内共同学习层级索引和排序：前向使用离散路径，反向用 straight-through estimator；全局路径平衡避免热门桶拥塞；候选进入路径后再使用比点积更强的 neural scoring。 Fidelity: 核心机制复现。本地执行 ranking-shaped 分层索引、路径探测和非点积 neural scoring；确定性 assignment 代理生产训练中的 STE 与全局平衡优化。未复刻 Instagram 私有数据、十亿物品多机索引、STE 训练 kernel、SCO 全局平衡与线上检索服务；本地结果不等同论文复现指标。本地对照口径：基线为同数据、同全库评测的 two-tower 点积检索；实验组加入 ranking-shaped 分层索引和 neural scoring，NDCG@10 相对 -7.70%。  retrieval learnable-index neural-scoring serving 搜广推 候选生成与搜索匹配 OneShot 的 STE 前向与反向为什么应分别检查？ 前向必须走实际离散 one-hot 路径，反向才用 softmax 梯度近似。全程 soft assignment 不测试离散服务，彻底硬 argmax 又可能无梯度。路径、候选映射与神经评分要保持同一索引版本，才能验收排序损失真正在训练地址。 示意：训练一步后路由参数应得到梯度，但单样本前向仍只选规定路径；若同时混所有桶，loss 可降却不对应线上离散树搜索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-713862f67a90446c">OneShot 的 STE 前向与反向为什么应分别检查？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aoneshot-index">OneShot: Index-in-Ranking with Neural Scoring for Large-Scale Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta / Instagram</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前向必须走实际离散 one-hot 路径，反向才用 softmax 梯度近似。全程 soft assignment 不测试离散服务，彻底硬 argmax 又可能无梯度。路径、候选映射与神经评分要保持同一索引版本，才能验收排序损失真正在训练地址。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练一步后路由参数应得到梯度，但单样本前向仍只选规定路径；若同时混所有桶，loss 可降却不对应线上离散树搜索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27475">原论文</a> · <a href="../../../../reproductions/2607.27475-oneshot-index/">实现解读</a> · <a href="#qa-713862f67a90446c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:core-relevance" data-paper-title="CORE: A Unified Cascaded Ordinal Relevance Estimation Framework for E-commerce Search" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="CORE: A Unified Cascaded Ordinal Relevance Estimation Framework for E-commerce Search 搜广推与 LLM 应用 Meituan / Beijing Institute of Technology 2026-07-27 电商相关性是有序的 High/Mid/Low，但 flat 三分类把三个边界视为对称。CORE 先判断 High vs. Non-High；只有第一步为 Non-High 时才判断 Mid vs. Low，使两个 head 分别专注严格实体/意图匹配和较软的替代性边界。 Fidelity: 核心机制复现。实际执行 flat/cascade 分类、条件 step reward、group-normalized clipped GRPO 和 PostCoT logit 聚合蒸馏；缩小 encoder、数据和 LLM。MovieLens 用户 genre 画像与候选 genre overlap 构造可审计的三级序数标签，替代美团私有 query-item 标注；小型 MLP 替代 Qwen3-14B 与生产 BERT。结果只验证级联、step credit 和 PostCoT 蒸馏链路，不能外推到搜索语义或线上阈值。  search-ranking ordinal-relevance step-grpo llm-distillation 搜广推 候选生成与搜索匹配 CORE 中 High、Mid、Low 为什么不能简单当作无顺序的三个类别？ High 侧重严格实体与意图匹配，Mid 和 Low 的分界允许更软的替代关系。它们的错误代价与判别依据不同，级联拆分使两个头各自集中于相应边界。类别有序不意味着数值间隔相等，也不能把三类随意编码后当连续回归目标。 示意：搜索某型号手机时，同型号是 High，其他可替代型号可能是 Mid，无关配件可能是 Low；把 High 误判 Low 与相邻等级混淆含义不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-core-relevance-f3a9a752" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ff961451ea4c9ef2">CORE 中 High、Mid、Low 为什么不能简单当作无顺序的三个类别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acore-relevance">CORE: A Unified Cascaded Ordinal Relevance Estimation Framework for E-commerce Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan / Beijing Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>High 侧重严格实体与意图匹配，Mid 和 Low 的分界允许更软的替代关系。它们的错误代价与判别依据不同，级联拆分使两个头各自集中于相应边界。类别有序不意味着数值间隔相等，也不能把三类随意编码后当连续回归目标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>搜索某型号手机时，同型号是 High，其他可替代型号可能是 Mid，无关配件可能是 Low；把 High 误判 Low 与相邻等级混淆含义不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24417">原论文</a> · <a href="../../../../reproductions/2607.24417-core-relevance/">实现解读</a> · <a href="#qa-ff961451ea4c9ef2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:core-relevance" data-paper-title="CORE: A Unified Cascaded Ordinal Relevance Estimation Framework for E-commerce Search" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="CORE: A Unified Cascaded Ordinal Relevance Estimation Framework for E-commerce Search 搜广推与 LLM 应用 Meituan / Beijing Institute of Technology 2026-07-27 电商相关性是有序的 High/Mid/Low，但 flat 三分类把三个边界视为对称。CORE 先判断 High vs. Non-High；只有第一步为 Non-High 时才判断 Mid vs. Low，使两个 head 分别专注严格实体/意图匹配和较软的替代性边界。 Fidelity: 核心机制复现。实际执行 flat/cascade 分类、条件 step reward、group-normalized clipped GRPO 和 PostCoT logit 聚合蒸馏；缩小 encoder、数据和 LLM。MovieLens 用户 genre 画像与候选 genre overlap 构造可审计的三级序数标签，替代美团私有 query-item 标注；小型 MLP 替代 Qwen3-14B 与生产 BERT。结果只验证级联、step credit 和 PostCoT 蒸馏链路，不能外推到搜索语义或线上阈值。  search-ranking ordinal-relevance step-grpo llm-distillation 搜广推 候选生成与搜索匹配 CORE为什么先判High与Non-High，再只对Non-High判Mid与Low？ 三档相关性有顺序且边界含义不同，平面三分类会混合严格匹配与宽松替代判断。级联让两个条件头分别专注边界，训练中的逐步奖励也只作用于实际经过的步骤；若已判High，就不应为未执行的Mid/Low步骤制造梯度。蒸馏时须把三类教师概率正确汇总成条件分布。 示意：搜索特定型号时先核对是否精确命中；未命中才区分可替代型号与完全无关商品。不能因为第一步已通过，还要求模型回答一个没必要执行的第二步。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:core-relevance" data-paper-title="CORE: A Unified Cascaded Ordinal Relevance Estimation Framework for E-commerce Search" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="CORE: A Unified Cascaded Ordinal Relevance Estimation Framework for E-commerce Search 搜广推与 LLM 应用 Meituan / Beijing Institute of Technology 2026-07-27 电商相关性是有序的 High/Mid/Low，但 flat 三分类把三个边界视为对称。CORE 先判断 High vs. Non-High；只有第一步为 Non-High 时才判断 Mid vs. Low，使两个 head 分别专注严格实体/意图匹配和较软的替代性边界。 Fidelity: 核心机制复现。实际执行 flat/cascade 分类、条件 step reward、group-normalized clipped GRPO 和 PostCoT logit 聚合蒸馏；缩小 encoder、数据和 LLM。MovieLens 用户 genre 画像与候选 genre overlap 构造可审计的三级序数标签，替代美团私有 query-item 标注；小型 MLP 替代 Qwen3-14B 与生产 BERT。结果只验证级联、step credit 和 PostCoT 蒸馏链路，不能外推到搜索语义或线上阈值。  search-ranking ordinal-relevance step-grpo llm-distillation 搜广推 候选生成与搜索匹配 CORE 的 step-GRPO 与只给最终三分类答案一个奖励，有什么信用分配区别？ 最终奖励无法区分是第一层判断、第二层条件判断还是格式出了错。分步奖励分别组内归一，把反馈送到有效步骤；若已判 High，未执行的 Mid/Low 不产生奖励和梯度。更细信用依赖可验证步骤定义，不是推理文字越长奖励就越充分。 示意：正确判为 High 后不应强迫模型继续回答 Mid 还是 Low；只惩罚最终答案则可能让未被执行的步骤也受到含混更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-16957d65af880b23">CORE 的 step-GRPO 与只给最终三分类答案一个奖励，有什么信用分配区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acore-relevance">CORE: A Unified Cascaded Ordinal Relevance Estimation Framework for E-commerce Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan / Beijing Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最终奖励无法区分是第一层判断、第二层条件判断还是格式出了错。分步奖励分别组内归一，把反馈送到有效步骤；若已判 High，未执行的 Mid/Low 不产生奖励和梯度。更细信用依赖可验证步骤定义，不是推理文字越长奖励就越充分。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>正确判为 High 后不应强迫模型继续回答 Mid 还是 Low；只惩罚最终答案则可能让未被执行的步骤也受到含混更新。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24417">原论文</a> · <a href="../../../../reproductions/2607.24417-core-relevance/">实现解读</a> · <a href="#qa-16957d65af880b23">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:core-relevance" data-paper-title="CORE: A Unified Cascaded Ordinal Relevance Estimation Framework for E-commerce Search" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="CORE: A Unified Cascaded Ordinal Relevance Estimation Framework for E-commerce Search 搜广推与 LLM 应用 Meituan / Beijing Institute of Technology 2026-07-27 电商相关性是有序的 High/Mid/Low，但 flat 三分类把三个边界视为对称。CORE 先判断 High vs. Non-High；只有第一步为 Non-High 时才判断 Mid vs. Low，使两个 head 分别专注严格实体/意图匹配和较软的替代性边界。 Fidelity: 核心机制复现。实际执行 flat/cascade 分类、条件 step reward、group-normalized clipped GRPO 和 PostCoT logit 聚合蒸馏；缩小 encoder、数据和 LLM。MovieLens 用户 genre 画像与候选 genre overlap 构造可审计的三级序数标签，替代美团私有 query-item 标注；小型 MLP 替代 Qwen3-14B 与生产 BERT。结果只验证级联、step credit 和 PostCoT 蒸馏链路，不能外推到搜索语义或线上阈值。  search-ranking ordinal-relevance step-grpo llm-distillation 搜广推 候选生成与搜索匹配 CORE 将三类 teacher logits 蒸馏给双头 student 时，Non-High 的 logit 为什么要用 logsumexp？ Non-High 对应 Mid 与 Low 的概率总和，在 logit 空间应以 log(exp zM+exp zL) 合并，而不是取均值。第二头只比较 Low 与 Mid，条件标签与有效 mask 要对齐。直接复制三类 logits 到两个头会改变条件概率含义。 示意：Mid 与 Low 各有较大质量时，它们合计可能超过 High；取两者 logit 平均会漏掉“两个分支合并”的概率，导致第一头判断失真。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-008971e4da77f9dd">CORE 将三类 teacher logits 蒸馏给双头 student 时，Non-High 的 logit 为什么要用 logsumexp？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acore-relevance">CORE: A Unified Cascaded Ordinal Relevance Estimation Framework for E-commerce Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan / Beijing Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Non-High 对应 Mid 与 Low 的概率总和，在 logit 空间应以 log(exp zM+exp zL) 合并，而不是取均值。第二头只比较 Low 与 Mid，条件标签与有效 mask 要对齐。直接复制三类 logits 到两个头会改变条件概率含义。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>Mid 与 Low 各有较大质量时，它们合计可能超过 High；取两者 logit 平均会漏掉“两个分支合并”的概率，导致第一头判断失真。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24417">原论文</a> · <a href="../../../../reproductions/2607.24417-core-relevance/">实现解读</a> · <a href="#qa-008971e4da77f9dd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:melo" data-paper-title="Melo: A Production LLM-Powered Music Recommendation Agent" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Melo: A Production LLM-Powered Music Recommendation Agent 搜广推与 LLM 应用 NetEase Cloud Music / Zhejiang University of Technology 2026-07-26 用多节点 Agent 编排意图、检索、推荐与解释，以实体目录 grounding 阻止幻觉，并在失败时触发反思重试。 Fidelity: 核心机制复现。本地执行意图路由、grounded 检索与失败反思重试；不把公开代理环境冒充网易云音乐生产系统。无法隔离论文系统 A/B 中模型、产品面和 UI 的贡献，论文也未给置信区间；本站明确保留该归因限制。本地对照口径：基线为无运行时修复的 catalog recommender，实验组为 grounding + retry；Hit@10 -20.00%、NDCG@10 -8.16%，fresh Hit@10 +50.00%。  llm-recommendation agent entity-grounding reflection 搜广推 候选生成与搜索匹配 Melo 为什么将意图、检索、推荐、解释分成多个执行节点？ 每步有不同输入与失败条件，目录 grounding 让生成实体落到真实可用对象，反馈再决定是否反思重试。分节点便于定位与修复，而非让自由语言一次包办。合法实体也不保证相关，解释流畅也不能弥补候选错误。 示意：模型说出不存在的电影时，应先修实体映射而非继续解释；若实体真实却不合用户需求，则应回到意图或检索节点找原因。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-melo-f661791b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d38970c261e7939e">Melo 为什么将意图、检索、推荐、解释分成多个执行节点？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amelo">Melo: A Production LLM-Powered Music Recommendation Agent</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NetEase Cloud Music / Zhejiang University of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每步有不同输入与失败条件，目录 grounding 让生成实体落到真实可用对象，反馈再决定是否反思重试。分节点便于定位与修复，而非让自由语言一次包办。合法实体也不保证相关，解释流畅也不能弥补候选错误。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型说出不存在的电影时，应先修实体映射而非继续解释；若实体真实却不合用户需求，则应回到意图或检索节点找原因。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.23718">原论文</a> · <a href="../../../../reproductions/2607.23718-melo/">实现解读</a> · <a href="#qa-d38970c261e7939e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:melo" data-paper-title="Melo: A Production LLM-Powered Music Recommendation Agent" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Melo: A Production LLM-Powered Music Recommendation Agent 搜广推与 LLM 应用 NetEase Cloud Music / Zhejiang University of Technology 2026-07-26 用多节点 Agent 编排意图、检索、推荐与解释，以实体目录 grounding 阻止幻觉，并在失败时触发反思重试。 Fidelity: 核心机制复现。本地执行意图路由、grounded 检索与失败反思重试；不把公开代理环境冒充网易云音乐生产系统。无法隔离论文系统 A/B 中模型、产品面和 UI 的贡献，论文也未给置信区间；本站明确保留该归因限制。本地对照口径：基线为无运行时修复的 catalog recommender，实验组为 grounding + retry；Hit@10 -20.00%、NDCG@10 -8.16%，fresh Hit@10 +50.00%。  llm-recommendation agent entity-grounding reflection 搜广推 候选生成与搜索匹配 Melo为什么必须在推荐后做实体grounding，并在失败时反思重试？ 语言模型能生成合理的音乐描述，却可能给出不存在或名称不一致的实体。grounding把输出映射到真实目录，验证后才进入推荐结果；反思重试利用失败原因修正意图或检索，而非任意换一份列表。合法实体也未必符合偏好，修复成功率和推荐质量需要分别观察。 示意：模型写出一首听起来像真的歌，目录却找不到；系统应回到意图和检索节点修正，而不是把相似名称强行当成成功，也不能因歌名合法就认定用户会喜欢。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:melo" data-paper-title="Melo: A Production LLM-Powered Music Recommendation Agent" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Melo: A Production LLM-Powered Music Recommendation Agent 搜广推与 LLM 应用 NetEase Cloud Music / Zhejiang University of Technology 2026-07-26 用多节点 Agent 编排意图、检索、推荐与解释，以实体目录 grounding 阻止幻觉，并在失败时触发反思重试。 Fidelity: 核心机制复现。本地执行意图路由、grounded 检索与失败反思重试；不把公开代理环境冒充网易云音乐生产系统。无法隔离论文系统 A/B 中模型、产品面和 UI 的贡献，论文也未给置信区间；本站明确保留该归因限制。本地对照口径：基线为无运行时修复的 catalog recommender，实验组为 grounding + retry；Hit@10 -20.00%、NDCG@10 -8.16%，fresh Hit@10 +50.00%。  llm-recommendation agent entity-grounding reflection 搜广推 候选生成与搜索匹配 Melo 的一次 reflective retry 与无边界反复生成，相比可靠性取舍是什么？ 受控重试可修明显 grounding 错误并限制成本，无限重试可能反复幻觉或把随机碰中当能力。触发需基于目录合法性与置信条件，修复后仍独立评质量。来源本地 fresh 增加但总体退化，不能用修复次数证明更好。 示意：第一次输出错电影名，可查目录再试一次；若越试越换主题，继续循环直到碰到答案会夸大系统成功率并浪费延迟。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b4aaf679737868f4">Melo 的一次 reflective retry 与无边界反复生成，相比可靠性取舍是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amelo">Melo: A Production LLM-Powered Music Recommendation Agent</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NetEase Cloud Music / Zhejiang University of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>受控重试可修明显 grounding 错误并限制成本，无限重试可能反复幻觉或把随机碰中当能力。触发需基于目录合法性与置信条件，修复后仍独立评质量。来源本地 fresh 增加但总体退化，不能用修复次数证明更好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第一次输出错电影名，可查目录再试一次；若越试越换主题，继续循环直到碰到答案会夸大系统成功率并浪费延迟。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.23718">原论文</a> · <a href="../../../../reproductions/2607.23718-melo/">实现解读</a> · <a href="#qa-b4aaf679737868f4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:melo" data-paper-title="Melo: A Production LLM-Powered Music Recommendation Agent" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Melo: A Production LLM-Powered Music Recommendation Agent 搜广推与 LLM 应用 NetEase Cloud Music / Zhejiang University of Technology 2026-07-26 用多节点 Agent 编排意图、检索、推荐与解释，以实体目录 grounding 阻止幻觉，并在失败时触发反思重试。 Fidelity: 核心机制复现。本地执行意图路由、grounded 检索与失败反思重试；不把公开代理环境冒充网易云音乐生产系统。无法隔离论文系统 A/B 中模型、产品面和 UI 的贡献，论文也未给置信区间；本站明确保留该归因限制。本地对照口径：基线为无运行时修复的 catalog recommender，实验组为 grounding + retry；Hit@10 -20.00%、NDCG@10 -8.16%，fresh Hit@10 +50.00%。  llm-recommendation agent entity-grounding reflection 搜广推 候选生成与搜索匹配 Melo 的 grounding 后 argmax 返回合法实体，为什么仍需要阈值和失败状态？ 在目录内强选最高分总会得到一个合法 ID，但全部分数都低时可能是硬凑。阈值识别证据不足，原始生成实体是否存在也要在映射前记录；不能映射后再用“在目录内”条件假装发现了全部错误。本地只允许定义的一次重试。 示意：不存在的片名被硬映到最近真片，ID 虽合法但语义可能错；若只检查映射结果存在，就会漏报原始幻觉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a7d0077c574dea15">Melo 的 grounding 后 argmax 返回合法实体，为什么仍需要阈值和失败状态？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amelo">Melo: A Production LLM-Powered Music Recommendation Agent</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NetEase Cloud Music / Zhejiang University of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>在目录内强选最高分总会得到一个合法 ID，但全部分数都低时可能是硬凑。阈值识别证据不足，原始生成实体是否存在也要在映射前记录；不能映射后再用“在目录内”条件假装发现了全部错误。本地只允许定义的一次重试。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>不存在的片名被硬映到最近真片，ID 虽合法但语义可能错；若只检查映射结果存在，就会漏报原始幻觉。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.23718">原论文</a> · <a href="../../../../reproductions/2607.23718-melo/">实现解读</a> · <a href="#qa-a7d0077c574dea15">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mesh" data-paper-title="MESH: Scaling Up Retrieval with Heterogeneous Content Unification" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="MESH: Scaling Up Retrieval with Heterogeneous Content Unification 搜广推与 LLM 应用 Pinterest 2026-07-14 统一放大 flat retrieval 容易让高频 evergreen 梯度淹没 fresh/tail 信号。MESH 先把 user/item/context 分到独立 sub-tower，各自在全局交互前用 residual crossing 放大；RGBC 再用 context gate 调节纯 user-item affinity，服务端可并行各塔并异步缓存 item tower。 Fidelity: 核心机制复现。分组 manifold、独立 residual signal amplifier、全局 crossing 与 RGBC 均实际执行。未复刻 DHEN 全算子与生产 GPU inter-op；不引用本地微基准支持论文吞吐结论。本地对照口径：基线是 flat retrieval；实验组 MESH 使用三塔放大与 RGBC，验证集选 blend 0.1，相对基线 Hit@10 +0.00%、NDCG@10 -3.54%。  retrieval fresh-content serving 搜广推 候选生成与搜索匹配 MESH 为什么先在 user、item、context 子塔内部放大？ 全量 flat 交互容易让高频 evergreen 信号支配共享梯度，分子塔先独立交叉可保留各类结构，再由 context gate 调节 user-item 亲和。它试图让新增容量更均衡使用，不保证 fresh/tail 真正受益，仍需分组和整体质量证据。 示意：用户长期偏好、商品新鲜度和请求场景分别建模，再决定当前两者怎样匹配；不能让大量热门商品统计先淹没场景细节。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-mesh-881b1237" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7c782c1ba17874b8">MESH 为什么先在 user、item、context 子塔内部放大？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amesh">MESH: Scaling Up Retrieval with Heterogeneous Content Unification</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全量 flat 交互容易让高频 evergreen 信号支配共享梯度，分子塔先独立交叉可保留各类结构，再由 context gate 调节 user-item 亲和。它试图让新增容量更均衡使用，不保证 fresh/tail 真正受益，仍需分组和整体质量证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户长期偏好、商品新鲜度和请求场景分别建模，再决定当前两者怎样匹配；不能让大量热门商品统计先淹没场景细节。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12392">原论文</a> · <a href="../../../../reproductions/2607.12392-mesh/">实现解读</a> · <a href="#qa-7c782c1ba17874b8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mesh" data-paper-title="MESH: Scaling Up Retrieval with Heterogeneous Content Unification" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="MESH: Scaling Up Retrieval with Heterogeneous Content Unification 搜广推与 LLM 应用 Pinterest 2026-07-14 统一放大 flat retrieval 容易让高频 evergreen 梯度淹没 fresh/tail 信号。MESH 先把 user/item/context 分到独立 sub-tower，各自在全局交互前用 residual crossing 放大；RGBC 再用 context gate 调节纯 user-item affinity，服务端可并行各塔并异步缓存 item tower。 Fidelity: 核心机制复现。分组 manifold、独立 residual signal amplifier、全局 crossing 与 RGBC 均实际执行。未复刻 DHEN 全算子与生产 GPU inter-op；不引用本地微基准支持论文吞吐结论。本地对照口径：基线是 flat retrieval；实验组 MESH 使用三塔放大与 RGBC，验证集选 blend 0.1，相对基线 Hit@10 +0.00%、NDCG@10 -3.54%。  retrieval fresh-content serving 搜广推 候选生成与搜索匹配 MESH为什么先分别放大user、item、context子塔，再做全局交互？ 过早平铺所有输入，常见内容的强梯度可能掩盖新鲜和长尾信号。独立子塔先在各自空间做残差交叉，保留专门容量，再用context gate调节用户—物品亲和力，使交互受请求语境影响。可缓存item子塔并不代表最终打分完全解耦，后续候选相关计算仍需按实际服务路径核算。 示意：长尾商品的内容特征先有独立建模空间，不必一开始就与热门曝光统计竞争同一层；随后在当前场景中再判断用户与该商品的匹配程度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mesh" data-paper-title="MESH: Scaling Up Retrieval with Heterogeneous Content Unification" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="MESH: Scaling Up Retrieval with Heterogeneous Content Unification 搜广推与 LLM 应用 Pinterest 2026-07-14 统一放大 flat retrieval 容易让高频 evergreen 梯度淹没 fresh/tail 信号。MESH 先把 user/item/context 分到独立 sub-tower，各自在全局交互前用 residual crossing 放大；RGBC 再用 context gate 调节纯 user-item affinity，服务端可并行各塔并异步缓存 item tower。 Fidelity: 核心机制复现。分组 manifold、独立 residual signal amplifier、全局 crossing 与 RGBC 均实际执行。未复刻 DHEN 全算子与生产 GPU inter-op；不引用本地微基准支持论文吞吐结论。本地对照口径：基线是 flat retrieval；实验组 MESH 使用三塔放大与 RGBC，验证集选 blend 0.1，相对基线 Hit@10 +0.00%、NDCG@10 -3.54%。  retrieval fresh-content serving 搜广推 候选生成与搜索匹配 MESH 的塔并行与 flat 模型串行，相比何时才可能带来速度收益？ 独立塔允许并发、item 可异步缓存，但真实收益依赖执行框架、设备、批量和同步开销。模型图可并行不等于 Python 小批实际并行，来源测到更慢也是有效反例。质量与算力更需分别比较，不能按理论分支数推算吞吐。 示意：三条塔在同一 CPU 循环逐一执行，没有 GPU 并发，反而多了调度成本；设计可并行并不能让这种运行自动提速三倍。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-323fdf049a2e98cf">MESH 的塔并行与 flat 模型串行，相比何时才可能带来速度收益？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amesh">MESH: Scaling Up Retrieval with Heterogeneous Content Unification</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立塔允许并发、item 可异步缓存，但真实收益依赖执行框架、设备、批量和同步开销。模型图可并行不等于 Python 小批实际并行，来源测到更慢也是有效反例。质量与算力更需分别比较，不能按理论分支数推算吞吐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三条塔在同一 CPU 循环逐一执行，没有 GPU 并发，反而多了调度成本；设计可并行并不能让这种运行自动提速三倍。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12392">原论文</a> · <a href="../../../../reproductions/2607.12392-mesh/">实现解读</a> · <a href="#qa-323fdf049a2e98cf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mesh" data-paper-title="MESH: Scaling Up Retrieval with Heterogeneous Content Unification" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="MESH: Scaling Up Retrieval with Heterogeneous Content Unification 搜广推与 LLM 应用 Pinterest 2026-07-14 统一放大 flat retrieval 容易让高频 evergreen 梯度淹没 fresh/tail 信号。MESH 先把 user/item/context 分到独立 sub-tower，各自在全局交互前用 residual crossing 放大；RGBC 再用 context gate 调节纯 user-item affinity，服务端可并行各塔并异步缓存 item tower。 Fidelity: 核心机制复现。分组 manifold、独立 residual signal amplifier、全局 crossing 与 RGBC 均实际执行。未复刻 DHEN 全算子与生产 GPU inter-op；不引用本地微基准支持论文吞吐结论。本地对照口径：基线是 flat retrieval；实验组 MESH 使用三塔放大与 RGBC，验证集选 blend 0.1，相对基线 Hit@10 +0.00%、NDCG@10 -3.54%。  retrieval fresh-content serving 搜广推 候选生成与搜索匹配 RGBC 为什么在 user-item 逐元素亲和上施加 context gate，再加 context 残差？ 乘积形成两侧对应维关系，context 的 sigmoid gate 调节哪些关系适合当前场景，残差保留上下文本身。三塔向量需同维且身份对应，不能先平均上下文再宣称逐样本调节；LN 和残差位置也会改变作用。 示意：相同用户商品在通勤与周末场景可使用不同亲和维度，context 还可提供独立时段线索；把场景只当最终常数偏置不是同一机制。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-296affeb40c412ba">RGBC 为什么在 user-item 逐元素亲和上施加 context gate，再加 context 残差？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amesh">MESH: Scaling Up Retrieval with Heterogeneous Content Unification</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>乘积形成两侧对应维关系，context 的 sigmoid gate 调节哪些关系适合当前场景，残差保留上下文本身。三塔向量需同维且身份对应，不能先平均上下文再宣称逐样本调节；LN 和残差位置也会改变作用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>相同用户商品在通勤与周末场景可使用不同亲和维度，context 还可提供独立时段线索；把场景只当最终常数偏置不是同一机制。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12392">原论文</a> · <a href="../../../../reproductions/2607.12392-mesh/">实现解读</a> · <a href="#qa-296affeb40c412ba">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:zorro" data-paper-title="ZoRRO: A Zero-Weight Personalized Recommender System for Scalable News Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="ZoRRO: A Zero-Weight Personalized Recommender System for Scalable News Recommendation 搜广推与 LLM 应用 Technical University of Denmark 2026-07-12 不用模型训练，直接融合历史文章的时间衰减、语义相似度和类别关系，面向高吞吐新闻候选排序。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 ZoRRO 为 0.05201，相对变化 -3.70%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  news-recommendation training-free recency 搜广推 候选生成与搜索匹配 ZoRRO零训练参数是否表示完全不需要表示模型？ 不表示，方法可使用已有文章embedding及类别，排序阶段不再训练参数，通过时间衰减和相似关系融合个性化。已有表示和固定超参仍是先验与成本来源。 例如直接用外部语义向量算近邻，没有再对新闻日志反传训练。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-zorro-2da90bec" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-94f65e23b4aab23a">ZoRRO零训练参数是否表示完全不需要表示模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Azorro">ZoRRO: A Zero-Weight Personalized Recommender System for Scalable News Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Technical University of Denmark</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不表示，方法可使用已有文章embedding及类别，排序阶段不再训练参数，通过时间衰减和相似关系融合个性化。已有表示和固定超参仍是先验与成本来源。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如直接用外部语义向量算近邻，没有再对新闻日志反传训练。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.10910">原论文</a> · <a href="../../../../reproductions/2607.10910-zorro/">实现解读</a> · <a href="#qa-94f65e23b4aab23a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:zorro" data-paper-title="ZoRRO: A Zero-Weight Personalized Recommender System for Scalable News Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="ZoRRO: A Zero-Weight Personalized Recommender System for Scalable News Recommendation 搜广推与 LLM 应用 Technical University of Denmark 2026-07-12 不用模型训练，直接融合历史文章的时间衰减、语义相似度和类别关系，面向高吞吐新闻候选排序。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 ZoRRO 为 0.05201，相对变化 -3.70%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  news-recommendation training-free recency 搜广推 候选生成与搜索匹配 ZoRRO 为什么无需模型训练也能做候选排序，又在哪些信息上受限？ 它直接用历史的时间衰减、语义相似与类别关系组合候选得分，偏好规则与内容向量足以构成可运行排序器，省去参数拟合和训练更新。新历史可立即改变权重，但组合关系由设计固定，难自动学习复杂协同与用户差异。适合检验轻量规则价值，不能把无训练误解为没有特征、超参数或数据依赖。 示意：用户刚读多篇科技新闻，最近文章权重更高，语义相近且同类候选得分上升。系统能立刻响应，但无法自行学出“某用户周末更想看文化内容”的复杂规律。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:zorro" data-paper-title="ZoRRO: A Zero-Weight Personalized Recommender System for Scalable News Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="ZoRRO: A Zero-Weight Personalized Recommender System for Scalable News Recommendation 搜广推与 LLM 应用 Technical University of Denmark 2026-07-12 不用模型训练，直接融合历史文章的时间衰减、语义相似度和类别关系，面向高吞吐新闻候选排序。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 ZoRRO 为 0.05201，相对变化 -3.70%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  news-recommendation training-free recency 搜广推 候选生成与搜索匹配 时间衰减语义打分与只按热门新闻排序有什么不同？ 前者随用户历史内容及时间变化，热门基线主要共享全局热度；类别项另提供结构。但相似历史可能形成重复推荐，也不保证新闻新鲜度目标自动满足。 例如两用户同一时刻可因旧阅读兴趣得到不同顺序。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-763fa02b8a81b827">时间衰减语义打分与只按热门新闻排序有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Azorro">ZoRRO: A Zero-Weight Personalized Recommender System for Scalable News Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Technical University of Denmark</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者随用户历史内容及时间变化，热门基线主要共享全局热度；类别项另提供结构。但相似历史可能形成重复推荐，也不保证新闻新鲜度目标自动满足。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两用户同一时刻可因旧阅读兴趣得到不同顺序。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.10910">原论文</a> · <a href="../../../../reproductions/2607.10910-zorro/">实现解读</a> · <a href="#qa-763fa02b8a81b827">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:zorro" data-paper-title="ZoRRO: A Zero-Weight Personalized Recommender System for Scalable News Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="ZoRRO: A Zero-Weight Personalized Recommender System for Scalable News Recommendation 搜广推与 LLM 应用 Technical University of Denmark 2026-07-12 不用模型训练，直接融合历史文章的时间衰减、语义相似度和类别关系，面向高吞吐新闻候选排序。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 ZoRRO 为 0.05201，相对变化 -3.70%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  news-recommendation training-free recency 搜广推 候选生成与搜索匹配 ZoRRO本地电影代理能证明高吞吐新闻线上表现吗？ 不能，MovieLens缺少真实新闻时效、私有流量与serving。时间权重、历史截止和类别来源需明确，固定系数不能用测试结果逐题挑选后称零训练泛化。 例如把发布很久的电影时间当新闻新鲜度，只是机制代理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-eb697fa410518ed9">ZoRRO本地电影代理能证明高吞吐新闻线上表现吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Azorro">ZoRRO: A Zero-Weight Personalized Recommender System for Scalable News Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Technical University of Denmark</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，MovieLens缺少真实新闻时效、私有流量与serving。时间权重、历史截止和类别来源需明确，固定系数不能用测试结果逐题挑选后称零训练泛化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把发布很久的电影时间当新闻新鲜度，只是机制代理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.10910">原论文</a> · <a href="../../../../reproductions/2607.10910-zorro/">实现解读</a> · <a href="#qa-eb697fa410518ed9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:elise" data-paper-title="Multilingual Semantic Retrieval for Apple Music Search" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Multilingual Semantic Retrieval for Apple Music Search 搜广推与 LLM 应用 Apple 2026-07-11 Siamese bi-encoder 补充词法倒排，再用分位数分布匹配把 dense 与 token score 校准到同一尺度并限制语义结果数量。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 ELISE 为 0.04739，相对变化 -12.24%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  search multilingual-retrieval score-calibration 搜广推 候选生成与搜索匹配 ELISE 为什么保留词法与语义两条检索路径？ 词法匹配擅长型号、实体与精确条件，双编码器擅长表达变化和语义联想。混合补充不同盲点，再校准分数并限制语义数量，避免泛化吞掉明确要求。两路都可能出错，语义相似不等于符合全部商品条件。 示意：查具体相机型号依靠精确词项，查“适合雨天徒步”可借语义找到防水装备；仅保留一条路径会漏掉另一种需求。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-elise-a73bc968" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e99e6ece1c058781">ELISE 为什么保留词法与语义两条检索路径？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aelise">Multilingual Semantic Retrieval for Apple Music Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Apple</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>词法匹配擅长型号、实体与精确条件，双编码器擅长表达变化和语义联想。混合补充不同盲点，再校准分数并限制语义数量，避免泛化吞掉明确要求。两路都可能出错，语义相似不等于符合全部商品条件。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>查具体相机型号依靠精确词项，查“适合雨天徒步”可借语义找到防水装备；仅保留一条路径会漏掉另一种需求。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.10239">原论文</a> · <a href="../../../../reproductions/2607.10239-elise/">实现解读</a> · <a href="#qa-e99e6ece1c058781">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:elise" data-paper-title="Multilingual Semantic Retrieval for Apple Music Search" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Multilingual Semantic Retrieval for Apple Music Search 搜广推与 LLM 应用 Apple 2026-07-11 Siamese bi-encoder 补充词法倒排，再用分位数分布匹配把 dense 与 token score 校准到同一尺度并限制语义结果数量。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 ELISE 为 0.04739，相对变化 -12.24%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  search multilingual-retrieval score-calibration 搜广推 候选生成与搜索匹配 ELISE为什么先做分位数匹配，再融合语义召回和词法检索分数？ 两种模型的原始分数尺度和分布不同，直接加权可能让数值范围较大的一路支配结果。分位数映射先表达各自分布中的相对位置，再进行受控融合并限制语义结果数量。百分位不是校准点击概率，也不能替代对精确实体匹配的检查；跨语言分布变化后映射同样可能需要更新。 示意：词法分常在几十，向量相似度在零到一，直接相加几乎只看词法；映射到各自百分位后才可公平组合，同时保留精确歌名匹配的控制。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:elise" data-paper-title="Multilingual Semantic Retrieval for Apple Music Search" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Multilingual Semantic Retrieval for Apple Music Search 搜广推与 LLM 应用 Apple 2026-07-11 Siamese bi-encoder 补充词法倒排，再用分位数分布匹配把 dense 与 token score 校准到同一尺度并限制语义结果数量。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 ELISE 为 0.04739，相对变化 -12.24%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  search multilingual-retrieval score-calibration 搜广推 候选生成与搜索匹配 分位数匹配与线性 min-max 缩放，处理分数分布的方式有何不同？ 线性缩放主要调整范围，分位数依据经验分布映射相对位置，能应对两路形状差异。它提升可比性却不保证同分位等于同相关概率，分布漂移还会改变含义。不能只因融合后数值同范围就声称概率校准完成。 示意：词法分长尾很重、语义分挤在窄区间，乘常数未必对齐尾部；百分位可表达各自位置，但新品查询仍可能不服从旧分布。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-cb8bb8bb0fe59c3a">分位数匹配与线性 min-max 缩放，处理分数分布的方式有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aelise">Multilingual Semantic Retrieval for Apple Music Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Apple</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>线性缩放主要调整范围，分位数依据经验分布映射相对位置，能应对两路形状差异。它提升可比性却不保证同分位等于同相关概率，分布漂移还会改变含义。不能只因融合后数值同范围就声称概率校准完成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>词法分长尾很重、语义分挤在窄区间，乘常数未必对齐尾部；百分位可表达各自位置，但新品查询仍可能不服从旧分布。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.10239">原论文</a> · <a href="../../../../reproductions/2607.10239-elise/">实现解读</a> · <a href="#qa-cb8bb8bb0fe59c3a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:elise" data-paper-title="Multilingual Semantic Retrieval for Apple Music Search" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Multilingual Semantic Retrieval for Apple Music Search 搜广推与 LLM 应用 Apple 2026-07-11 Siamese bi-encoder 补充词法倒排，再用分位数分布匹配把 dense 与 token score 校准到同一尺度并限制语义结果数量。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 ELISE 为 0.04739，相对变化 -12.24%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  search multilingual-retrieval score-calibration 搜广推 候选生成与搜索匹配 ELISE 的映射、融合权重与语义配额为什么要在 test 前锁定？ 三者都决定最终候选及次序，按测试结果反复调整会把评估集用成验证。应在训练或验证口径拟合并固定，服务执行相同配额。本地公开代理出现负结果时不能再挑测试最佳组合隐藏退化。 示意：看到 test 后发现语义比例七成最好，再只报这一组会乐观；先锁定比例和分位映射，才能诚实测它对新请求的表现。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-96f620f321725996">ELISE 的映射、融合权重与语义配额为什么要在 test 前锁定？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aelise">Multilingual Semantic Retrieval for Apple Music Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Apple</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>三者都决定最终候选及次序，按测试结果反复调整会把评估集用成验证。应在训练或验证口径拟合并固定，服务执行相同配额。本地公开代理出现负结果时不能再挑测试最佳组合隐藏退化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>看到 test 后发现语义比例七成最好，再只报这一组会乐观；先锁定比例和分位映射，才能诚实测它对新请求的表现。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.10239">原论文</a> · <a href="../../../../reproductions/2607.10239-elise/">实现解读</a> · <a href="#qa-96f620f321725996">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cluster-goobs" data-paper-title="Real-Time Hard Negative Sampling via LLM-based Clustering for Large-Scale Two-Tower Retrieval" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Real-Time Hard Negative Sampling via LLM-based Clustering for Large-Scale Two-Tower Retrieval 搜广推与 LLM 应用 Meta 2026-07-01 大规模双塔召回常从 out-of-batch（OOB）池随机抽负例。绝大多数负例过于容易，梯度弱；同时热门物品更常进入池，形成曝光反馈循环。论文先用 LLM/多模态 embedding 把物品划入语义 cluster，再让 GOOBS 的 update engine 按 cluster 分段写入实时 OOB 池，sample engine 大概率从正例所在 cluster 抽 hard negative。这样不增加在线模型结构，采样仍是 O(1)。 Fidelity: 核心机制复现。cluster-conditioned online hard-negative sampler 实际执行；MovieLens genre 替换私有 LLM 多模态 cluster，分布式 GOOBS serving 未复刻。本地对照口径：基线是 Random OOB negative sampler；实验组是 Cluster GOOBS sampler；NDCG@10 +0.98%、head share -1.81%。这是负采样策略消融，不是完整双塔相对 DIN 的比较。   搜广推 候选生成与搜索匹配 Cluster GOOBS 为什么修改负采样池，而不用增加线上模型结构？ 双塔仍计算同样相似度，难度提升发生在训练分母中的负例选择：实时池按语义簇组织，更常给出与正例接近的竞争项。服务不需要额外簇模型参与打分。训练采样改变了学习分布，因此评估应看全库，而非只在同样采样的小集合上报好成绩。 示意：模型结构不变，但训练相机正例时更多面对相似镜头或相机负例；上线仍是一份双塔向量索引，不需再跑新网络。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-cluster-goobs-3f572e40" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-96b235575e77219f">Cluster GOOBS 为什么修改负采样池，而不用增加线上模型结构？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acluster-goobs">Real-Time Hard Negative Sampling via LLM-based Clustering for Large-Scale Two-Tower Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>双塔仍计算同样相似度，难度提升发生在训练分母中的负例选择：实时池按语义簇组织，更常给出与正例接近的竞争项。服务不需要额外簇模型参与打分。训练采样改变了学习分布，因此评估应看全库，而非只在同样采样的小集合上报好成绩。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型结构不变，但训练相机正例时更多面对相似镜头或相机负例；上线仍是一份双塔向量索引，不需再跑新网络。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.00448">原论文</a> · <a href="../../../../reproductions/2607.00448-cluster-goobs/">实现解读</a> · <a href="#qa-96b235575e77219f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cluster-goobs" data-paper-title="Real-Time Hard Negative Sampling via LLM-based Clustering for Large-Scale Two-Tower Retrieval" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Real-Time Hard Negative Sampling via LLM-based Clustering for Large-Scale Two-Tower Retrieval 搜广推与 LLM 应用 Meta 2026-07-01 大规模双塔召回常从 out-of-batch（OOB）池随机抽负例。绝大多数负例过于容易，梯度弱；同时热门物品更常进入池，形成曝光反馈循环。论文先用 LLM/多模态 embedding 把物品划入语义 cluster，再让 GOOBS 的 update engine 按 cluster 分段写入实时 OOB 池，sample engine 大概率从正例所在 cluster 抽 hard negative。这样不增加在线模型结构，采样仍是 O(1)。 Fidelity: 核心机制复现。cluster-conditioned online hard-negative sampler 实际执行；MovieLens genre 替换私有 LLM 多模态 cluster，分布式 GOOBS serving 未复刻。本地对照口径：基线是 Random OOB negative sampler；实验组是 Cluster GOOBS sampler；NDCG@10 +0.98%、head share -1.81%。这是负采样策略消融，不是完整双塔相对 DIN 的比较。   搜广推 候选生成与搜索匹配 Cluster GOOBS为什么大概率在正例所在语义簇里抽负例，又保留随机负例？ 同簇物品在内容上接近，更可能落在模型真实选择边界，能避免大部分随机负例太容易。保留少量随机采样则提供全局覆盖，减轻只学簇内区分的局限。核心变化在实时OOB池的分段更新与采样分布，而非给线上双塔再加一个LLM；同簇物品也可能是假负例，比例需验证。 示意：正例是跑鞋时，与另一款跑鞋比较比与冰箱比较更难；偶尔仍抽跨类物品，避免模型只会区分鞋款，却不知道鞋和家电的整体差异。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cluster-goobs" data-paper-title="Real-Time Hard Negative Sampling via LLM-based Clustering for Large-Scale Two-Tower Retrieval" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Real-Time Hard Negative Sampling via LLM-based Clustering for Large-Scale Two-Tower Retrieval 搜广推与 LLM 应用 Meta 2026-07-01 大规模双塔召回常从 out-of-batch（OOB）池随机抽负例。绝大多数负例过于容易，梯度弱；同时热门物品更常进入池，形成曝光反馈循环。论文先用 LLM/多模态 embedding 把物品划入语义 cluster，再让 GOOBS 的 update engine 按 cluster 分段写入实时 OOB 池，sample engine 大概率从正例所在 cluster 抽 hard negative。这样不增加在线模型结构，采样仍是 O(1)。 Fidelity: 核心机制复现。cluster-conditioned online hard-negative sampler 实际执行；MovieLens genre 替换私有 LLM 多模态 cluster，分布式 GOOBS serving 未复刻。本地对照口径：基线是 Random OOB negative sampler；实验组是 Cluster GOOBS sampler；NDCG@10 +0.98%、head share -1.81%。这是负采样策略消融，不是完整双塔相对 DIN 的比较。   搜广推 候选生成与搜索匹配 Cluster GOOBS 与只在当前 batch 内找 hard negatives，相比多了什么覆盖？ 当前 batch 受批大小与抽样偶然性限制，out-of-batch 池提供更大、持续更新的负例来源，语义分段让取难例成本可控。池也可能有陈旧向量或假负例，需要与随机成分平衡；不能把常数采样开销误说成整个训练常数复杂度。 示意：当前批次没有同类电影，批内负例都很容易；跨批池中已有同题材候选，能提供更细的区分，但真实也喜欢的片可能成为假负例。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1c2cb8a9fc3232c5">Cluster GOOBS 与只在当前 batch 内找 hard negatives，相比多了什么覆盖？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acluster-goobs">Real-Time Hard Negative Sampling via LLM-based Clustering for Large-Scale Two-Tower Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>当前 batch 受批大小与抽样偶然性限制，out-of-batch 池提供更大、持续更新的负例来源，语义分段让取难例成本可控。池也可能有陈旧向量或假负例，需要与随机成分平衡；不能把常数采样开销误说成整个训练常数复杂度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>当前批次没有同类电影，批内负例都很容易；跨批池中已有同题材候选，能提供更细的区分，但真实也喜欢的片可能成为假负例。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.00448">原论文</a> · <a href="../../../../reproductions/2607.00448-cluster-goobs/">实现解读</a> · <a href="#qa-1c2cb8a9fc3232c5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cluster-goobs" data-paper-title="Real-Time Hard Negative Sampling via LLM-based Clustering for Large-Scale Two-Tower Retrieval" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Real-Time Hard Negative Sampling via LLM-based Clustering for Large-Scale Two-Tower Retrieval 搜广推与 LLM 应用 Meta 2026-07-01 大规模双塔召回常从 out-of-batch（OOB）池随机抽负例。绝大多数负例过于容易，梯度弱；同时热门物品更常进入池，形成曝光反馈循环。论文先用 LLM/多模态 embedding 把物品划入语义 cluster，再让 GOOBS 的 update engine 按 cluster 分段写入实时 OOB 池，sample engine 大概率从正例所在 cluster 抽 hard negative。这样不增加在线模型结构，采样仍是 O(1)。 Fidelity: 核心机制复现。cluster-conditioned online hard-negative sampler 实际执行；MovieLens genre 替换私有 LLM 多模态 cluster，分布式 GOOBS serving 未复刻。本地对照口径：基线是 Random OOB negative sampler；实验组是 Cluster GOOBS sampler；NDCG@10 +0.98%、head share -1.81%。这是负采样策略消融，不是完整双塔相对 DIN 的比较。   搜广推 候选生成与搜索匹配 Cluster GOOBS 的 random:cluster 比例与实时池更新应怎样避免测试泄漏？ 簇与池应由训练可用内容和交互构造，采样混合比例按设定或验证口径固定，不能根据 test 命中反复调整。本地 MovieLens 用 genre 代理语义簇且限制训练转移量，不等同于原文多模态簇；全库评估与采样池是两个不同集合。 示意：一比十五表示每份随机负例配更多簇负例，并非只测试这十六件物品；测试目标也不能提前进入池更新来改变训练难度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-cdff540d8f7eb8cc">Cluster GOOBS 的 random:cluster 比例与实时池更新应怎样避免测试泄漏？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acluster-goobs">Real-Time Hard Negative Sampling via LLM-based Clustering for Large-Scale Two-Tower Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>簇与池应由训练可用内容和交互构造，采样混合比例按设定或验证口径固定，不能根据 test 命中反复调整。本地 MovieLens 用 genre 代理语义簇且限制训练转移量，不等同于原文多模态簇；全库评估与采样池是两个不同集合。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一比十五表示每份随机负例配更多簇负例，并非只测试这十六件物品；测试目标也不能提前进入池更新来改变训练难度。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.00448">原论文</a> · <a href="../../../../reproductions/2607.00448-cluster-goobs/">实现解读</a> · <a href="#qa-cdff540d8f7eb8cc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:next-vlm" data-paper-title="NEXT: Reasoning-Driven Video Recommendation via a Vision-Language Model" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="NEXT: Reasoning-Driven Video Recommendation via a Vision-Language Model 搜广推与 LLM 应用 Meta 2026-06-27 共现和语义相似只能回答“哪些视频相近”，难以推断用户看完当前视频后下一步想做什么。NEXT 先识别显式续集；对隐式关系让 NEXT-8B VLM 生成 next-intent query，再检索并验证候选，形成 directed Next Knowledge Graph。推理放在离线，线上只在用户正反馈后注入高置信边，避免把 8B VLM 放进请求链路。 这是公开代理任务的单 seed 诊断结果，不是 Meta 线上收益复现。Fidelity: 核心机制复现。本地执行 item→intent→item、离线 directed edge 生成/验证和线上加性注入；没有把规则或 embedding 代理写成“训练了 NEXT-8B”。本地用电影标题/genre 和协同转移代理视觉语义与 VLM 验证；未训练 8B VLM、GRPO/SFT 偏好阶段，也没有短视频画面、私有安全模型和实时 serving。本地对照口径：基线为同数据的 transition+semantic 多路径 ranker；  multimodal reasoning retrieval knowledge-graph vlm 搜广推 候选生成与搜索匹配 NEXT 的 directed graph 为什么不能把所有边自动反向使用？ 下一意图有顺序，A 看完后需要 B 不代表 B 后需要 A。显式续集与隐式推理都生成方向关系，在线再按正反馈触发高置信连接。无方向相似图无法表达同样转移，也不能把推断边当真实观测消费。 示意：咖啡机开箱后常需萃取教程，教程后再看开箱未必自然；把边反向会改变需求阶段，而不是仅多一点图覆盖。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-next-vlm-e4f6498d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f372a46478cadf88">NEXT 的 directed graph 为什么不能把所有边自动反向使用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Anext-vlm">NEXT: Reasoning-Driven Video Recommendation via a Vision-Language Model</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>下一意图有顺序，A 看完后需要 B 不代表 B 后需要 A。显式续集与隐式推理都生成方向关系，在线再按正反馈触发高置信连接。无方向相似图无法表达同样转移，也不能把推断边当真实观测消费。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>咖啡机开箱后常需萃取教程，教程后再看开箱未必自然；把边反向会改变需求阶段，而不是仅多一点图覆盖。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24789">原论文</a> · <a href="../../../../reproductions/2607.24789-next-vlm/">实现解读</a> · <a href="#qa-f372a46478cadf88">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:next-vlm" data-paper-title="NEXT: Reasoning-Driven Video Recommendation via a Vision-Language Model" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="NEXT: Reasoning-Driven Video Recommendation via a Vision-Language Model 搜广推与 LLM 应用 Meta 2026-06-27 共现和语义相似只能回答“哪些视频相近”，难以推断用户看完当前视频后下一步想做什么。NEXT 先识别显式续集；对隐式关系让 NEXT-8B VLM 生成 next-intent query，再检索并验证候选，形成 directed Next Knowledge Graph。推理放在离线，线上只在用户正反馈后注入高置信边，避免把 8B VLM 放进请求链路。 这是公开代理任务的单 seed 诊断结果，不是 Meta 线上收益复现。Fidelity: 核心机制复现。本地执行 item→intent→item、离线 directed edge 生成/验证和线上加性注入；没有把规则或 embedding 代理写成“训练了 NEXT-8B”。本地用电影标题/genre 和协同转移代理视觉语义与 VLM 验证；未训练 8B VLM、GRPO/SFT 偏好阶段，也没有短视频画面、私有安全模型和实时 serving。本地对照口径：基线为同数据的 transition+semantic 多路径 ranker；  multimodal reasoning retrieval knowledge-graph vlm 搜广推 候选生成与搜索匹配 NEXT 为什么先生成 next-intent 再检索和验证，而不直接连接语义最相似的视频？ 语义相似描述内容接近，未必描述用户看完后的下一步需求。NEXT 用视觉语言模型从当前视频推断后续意图，再检索满足该意图的候选并验证，形成有方向的边。昂贵推理离线执行，在线在正反馈后注入高置信连接；因此图表达的是可能的后续关系，而非无方向的内容相似网络。 示意：看完“咖啡机开箱”后，下一需求可能是“如何萃取”，未必是另一条开箱。先生成这个后续意图，再检索教学视频，便能产生开箱到使用教程的有向边。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:next-vlm" data-paper-title="NEXT: Reasoning-Driven Video Recommendation via a Vision-Language Model" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="NEXT: Reasoning-Driven Video Recommendation via a Vision-Language Model 搜广推与 LLM 应用 Meta 2026-06-27 共现和语义相似只能回答“哪些视频相近”，难以推断用户看完当前视频后下一步想做什么。NEXT 先识别显式续集；对隐式关系让 NEXT-8B VLM 生成 next-intent query，再检索并验证候选，形成 directed Next Knowledge Graph。推理放在离线，线上只在用户正反馈后注入高置信边，避免把 8B VLM 放进请求链路。 这是公开代理任务的单 seed 诊断结果，不是 Meta 线上收益复现。Fidelity: 核心机制复现。本地执行 item→intent→item、离线 directed edge 生成/验证和线上加性注入；没有把规则或 embedding 代理写成“训练了 NEXT-8B”。本地用电影标题/genre 和协同转移代理视觉语义与 VLM 验证；未训练 8B VLM、GRPO/SFT 偏好阶段，也没有短视频画面、私有安全模型和实时 serving。本地对照口径：基线为同数据的 transition+semantic 多路径 ranker；  multimodal reasoning retrieval knowledge-graph vlm 搜广推 候选生成与搜索匹配 NEXT 的 intent→retrieve→verify 与直接让 VLM 点名下一视频，可靠性有什么差别？ 意图先表达后续需求，检索落到真实目录，验证再检查候选是否满足该方向，减少自由点名幻觉。多阶段仍可能误推意图或继承检索漏召，不保证推理正确；来源本地是代理图增量，不能称 NEXT-8B 全训练已重建。 示意：先问“接下来想学怎么用”，再找教程并核对，比直接编出某视频标题更可落地；若意图起初理解错，验证也可能沿错方向工作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7dcbd227aeffe137">NEXT 的 intent→retrieve→verify 与直接让 VLM 点名下一视频，可靠性有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Anext-vlm">NEXT: Reasoning-Driven Video Recommendation via a Vision-Language Model</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>意图先表达后续需求，检索落到真实目录，验证再检查候选是否满足该方向，减少自由点名幻觉。多阶段仍可能误推意图或继承检索漏召，不保证推理正确；来源本地是代理图增量，不能称 NEXT-8B 全训练已重建。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先问“接下来想学怎么用”，再找教程并核对，比直接编出某视频标题更可落地；若意图起初理解错，验证也可能沿错方向工作。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24789">原论文</a> · <a href="../../../../reproductions/2607.24789-next-vlm/">实现解读</a> · <a href="#qa-7dcbd227aeffe137">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:next-vlm" data-paper-title="NEXT: Reasoning-Driven Video Recommendation via a Vision-Language Model" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="NEXT: Reasoning-Driven Video Recommendation via a Vision-Language Model 搜广推与 LLM 应用 Meta 2026-06-27 共现和语义相似只能回答“哪些视频相近”，难以推断用户看完当前视频后下一步想做什么。NEXT 先识别显式续集；对隐式关系让 NEXT-8B VLM 生成 next-intent query，再检索并验证候选，形成 directed Next Knowledge Graph。推理放在离线，线上只在用户正反馈后注入高置信边，避免把 8B VLM 放进请求链路。 这是公开代理任务的单 seed 诊断结果，不是 Meta 线上收益复现。Fidelity: 核心机制复现。本地执行 item→intent→item、离线 directed edge 生成/验证和线上加性注入；没有把规则或 embedding 代理写成“训练了 NEXT-8B”。本地用电影标题/genre 和协同转移代理视觉语义与 VLM 验证；未训练 8B VLM、GRPO/SFT 偏好阶段，也没有短视频画面、私有安全模型和实时 serving。本地对照口径：基线为同数据的 transition+semantic 多路径 ranker；  multimodal reasoning retrieval knowledge-graph vlm 搜广推 候选生成与搜索匹配 NEXT 在线为何仅在 positive engagement 后加性注入 NKG 候选？ 正反馈作为继续同类需求的触发，图路径补充现有生产候选而非完全替换，减少低置信边的影响。触发标签需当时已发生，不能用未来目标反馈；重复候选与资格仍要处理。本地单 seed 大幅变化只解释固定代理协议。 示意：用户跳过开箱不应立即强推使用教程，明确喜欢后再加图候选；原召回继续提供其他选项，避免一条推断边接管全部列表。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f9e4c0fc5abbe8b3">NEXT 在线为何仅在 positive engagement 后加性注入 NKG 候选？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Anext-vlm">NEXT: Reasoning-Driven Video Recommendation via a Vision-Language Model</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>正反馈作为继续同类需求的触发，图路径补充现有生产候选而非完全替换，减少低置信边的影响。触发标签需当时已发生，不能用未来目标反馈；重复候选与资格仍要处理。本地单 seed 大幅变化只解释固定代理协议。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户跳过开箱不应立即强推使用教程，明确喜欢后再加图候选；原召回继续提供其他选项，避免一条推断边接管全部列表。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24789">原论文</a> · <a href="../../../../reproductions/2607.24789-next-vlm/">实现解读</a> · <a href="#qa-f9e4c0fc5abbe8b3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rankgraph2" data-paper-title="RankGraph-2: Lifecycle Co-Design for Billion-Node Graph Learning in Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="RankGraph-2: Lifecycle Co-Design for Billion-Node Graph Learning in Recommendation 搜广推与 LLM 应用 Meta 2026-06-16 直接在线跑多层 GNN 成本高且易受热门边支配。RankGraph-2 对边做 popularity correction，离线预计算多跳 PPR，再用共同学习的 residual/cluster index 压缩服务。 复现保真度：核心机制复现。复现保真度：核心机制复现。流行度校正、离线 PPR 和 cluster index 均实际执行。MovieLens item graph 上真实执行去偏转移、多跳 PPR 与 PPR 表征聚类索引。  graph-retrieval ppr residual-quantization 搜广推 候选生成与搜索匹配 RankGraph-2 的 PPR 为什么结合回到起点与多跳传播？ 回跳保留查询种子个性化，多跳沿校正图扩展间接关系，避免仅一跳覆盖不足。热门边修正减少概率被大节点吸走。传播稳定不等于关系无偏，离线图还会过时，索引压缩也可能丢长尾路径。 示意：从一条摄影内容出发，经镜头与技巧节点找到教程，回跳让结果仍围绕原兴趣，而非走很多步后全跑到全站热门视频。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-rankgraph2-ef314ec2" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-bbf469a8879df2f5">RankGraph-2 的 PPR 为什么结合回到起点与多跳传播？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arankgraph2">RankGraph-2: Lifecycle Co-Design for Billion-Node Graph Learning in Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>回跳保留查询种子个性化，多跳沿校正图扩展间接关系，避免仅一跳覆盖不足。热门边修正减少概率被大节点吸走。传播稳定不等于关系无偏，离线图还会过时，索引压缩也可能丢长尾路径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>从一条摄影内容出发，经镜头与技巧节点找到教程，回跳让结果仍围绕原兴趣，而非走很多步后全跑到全站热门视频。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.18379">原论文</a> · <a href="../../../../reproductions/2606.18379-rankgraph2/">实现解读</a> · <a href="#qa-bbf469a8879df2f5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rankgraph2" data-paper-title="RankGraph-2: Lifecycle Co-Design for Billion-Node Graph Learning in Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="RankGraph-2: Lifecycle Co-Design for Billion-Node Graph Learning in Recommendation 搜广推与 LLM 应用 Meta 2026-06-16 直接在线跑多层 GNN 成本高且易受热门边支配。RankGraph-2 对边做 popularity correction，离线预计算多跳 PPR，再用共同学习的 residual/cluster index 压缩服务。 复现保真度：核心机制复现。复现保真度：核心机制复现。流行度校正、离线 PPR 和 cluster index 均实际执行。MovieLens item graph 上真实执行去偏转移、多跳 PPR 与 PPR 表征聚类索引。  graph-retrieval ppr residual-quantization 搜广推 候选生成与搜索匹配 RankGraph-2 为什么先校正热门边再离线计算多跳 PPR，而不在线堆更深 GNN？ 多跳传播能发现间接关系，但热门节点容易吸走大量概率，在线逐层图计算也昂贵。先按流行度校正转移，再离线求个性化 PageRank，可把去偏多跳关系预先写入表示；残差与聚类索引进一步压缩服务。校正改变传播偏好，并不保证消除全部曝光偏差，离线图也需随数据更新。 示意：所有用户都看过一部大片时，它可能把很多无关电影连在一起。降低通向热门节点的传播权重后，再计算多跳邻近，更有机会保留小众但相关的关联。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rankgraph2" data-paper-title="RankGraph-2: Lifecycle Co-Design for Billion-Node Graph Learning in Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="RankGraph-2: Lifecycle Co-Design for Billion-Node Graph Learning in Recommendation 搜广推与 LLM 应用 Meta 2026-06-16 直接在线跑多层 GNN 成本高且易受热门边支配。RankGraph-2 对边做 popularity correction，离线预计算多跳 PPR，再用共同学习的 residual/cluster index 压缩服务。 复现保真度：核心机制复现。复现保真度：核心机制复现。流行度校正、离线 PPR 和 cluster index 均实际执行。MovieLens item graph 上真实执行去偏转移、多跳 PPR 与 PPR 表征聚类索引。  graph-retrieval ppr residual-quantization 搜广推 候选生成与搜索匹配 离线 PPR 加压缩索引与在线深 GNN，相比成本与新鲜度如何交换？ 离线将多跳计算摊到更新周期，服务查表或索引更轻，但对新增边和近期意图反应可能滞后；在线图模型更及时却每次付传播成本。不能把 PPR 迭代收敛速度直接当端到端吞吐，来源代理比较也非完整生产架构消融。 示意：昨天图上热门教程已预算好，今天新发布内容尚无连接；在线模型也许更快利用新边，离线方案则要等刷新，两者预算不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-8de9c180a87e7923">离线 PPR 加压缩索引与在线深 GNN，相比成本与新鲜度如何交换？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arankgraph2">RankGraph-2: Lifecycle Co-Design for Billion-Node Graph Learning in Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>离线将多跳计算摊到更新周期，服务查表或索引更轻，但对新增边和近期意图反应可能滞后；在线图模型更及时却每次付传播成本。不能把 PPR 迭代收敛速度直接当端到端吞吐，来源代理比较也非完整生产架构消融。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>昨天图上热门教程已预算好，今天新发布内容尚无连接；在线模型也许更快利用新边，离线方案则要等刷新，两者预算不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.18379">原论文</a> · <a href="../../../../reproductions/2606.18379-rankgraph2/">实现解读</a> · <a href="#qa-8de9c180a87e7923">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rankgraph2" data-paper-title="RankGraph-2: Lifecycle Co-Design for Billion-Node Graph Learning in Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="RankGraph-2: Lifecycle Co-Design for Billion-Node Graph Learning in Recommendation 搜广推与 LLM 应用 Meta 2026-06-16 直接在线跑多层 GNN 成本高且易受热门边支配。RankGraph-2 对边做 popularity correction，离线预计算多跳 PPR，再用共同学习的 residual/cluster index 压缩服务。 复现保真度：核心机制复现。复现保真度：核心机制复现。流行度校正、离线 PPR 和 cluster index 均实际执行。MovieLens item graph 上真实执行去偏转移、多跳 PPR 与 PPR 表征聚类索引。  graph-retrieval ppr residual-quantization 搜广推 候选生成与搜索匹配 流行度校正后为什么必须重新归一转移行再求 PPR？ 除以热门度因子改变边权，若不归一为合法转移，概率质量会错误衰减或放大，PPR 方程意义改变。需检查孤立节点与回跳处理，残差/聚类索引再单独验收。校正是设计的去偏路径，不自动证明消除全部曝光偏差。 示意：一行原来和一，压热门边后只剩零点四，不归一便让每跳丢六成质量；这不是想要的“重新分配邻居偏好”。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e362d9fc430e281c">流行度校正后为什么必须重新归一转移行再求 PPR？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arankgraph2">RankGraph-2: Lifecycle Co-Design for Billion-Node Graph Learning in Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>除以热门度因子改变边权，若不归一为合法转移，概率质量会错误衰减或放大，PPR 方程意义改变。需检查孤立节点与回跳处理，残差/聚类索引再单独验收。校正是设计的去偏路径，不自动证明消除全部曝光偏差。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一行原来和一，压热门边后只剩零点四，不归一便让每跳丢六成质量；这不是想要的“重新分配邻居偏好”。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.18379">原论文</a> · <a href="../../../../reproductions/2606.18379-rankgraph2/">实现解读</a> · <a href="#qa-e362d9fc430e281c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:toolrec" data-paper-title="ToolRec: Calibrated Preference Alignment for Query Recommendation in On-Device Assistants" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="ToolRec: Calibrated Preference Alignment for Query Recommendation in On-Device Assistants 搜广推与 LLM 应用 Huazhong University of Science and Technology 2026-06-07 在 KTO 式偏好目标上同时加入用户侧校准与工具频率驱动的动态系统侧校准，提升会触发工具的查询，同时约束上下文相关性下降。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04819，相对变化 -10.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。  query-recommendation preference-alignment tool-use 搜广推 候选生成与搜索匹配 ToolRec的工具频率信号，表示工具调用越多就越好吗？ 不是。频率是系统侧校准信息，与用户请求是否适合触发某工具是不同轴。它用于调节供需或使用分布，不能替代上下文相关性，也不是每次调用成功的质量标签。先区分频率与效用，才能读懂双侧目标为什么不能只报触发率。 教学例子：某工具调用很少，增加频率也不能使无关问题适合它；调用率上升应与用户相关性一起检查。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-toolrec-2caef440" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-25a7db10326f0f87">ToolRec的工具频率信号，表示工具调用越多就越好吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atoolrec">ToolRec: Calibrated Preference Alignment for Query Recommendation in On-Device Assistants</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huazhong University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。频率是系统侧校准信息，与用户请求是否适合触发某工具是不同轴。它用于调节供需或使用分布，不能替代上下文相关性，也不是每次调用成功的质量标签。先区分频率与效用，才能读懂双侧目标为什么不能只报触发率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某工具调用很少，增加频率也不能使无关问题适合它；调用率上升应与用户相关性一起检查。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.08466">原论文</a> · <a href="../../../../reproductions/2606.08466-toolrec/">实现解读</a> · <a href="#qa-25a7db10326f0f87">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:toolrec" data-paper-title="ToolRec: Calibrated Preference Alignment for Query Recommendation in On-Device Assistants" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="ToolRec: Calibrated Preference Alignment for Query Recommendation in On-Device Assistants 搜广推与 LLM 应用 Huazhong University of Science and Technology 2026-06-07 在 KTO 式偏好目标上同时加入用户侧校准与工具频率驱动的动态系统侧校准，提升会触发工具的查询，同时约束上下文相关性下降。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04819，相对变化 -10.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。  query-recommendation preference-alignment tool-use 搜广推 候选生成与搜索匹配 ToolRec 为什么同时校准用户偏好与系统工具频率，而不只奖励触发工具？ 只奖励工具调用容易让模型对不相关请求也强行调用，单看用户侧偏好又可能忽略工具在系统中的供需失衡。双侧校准分别约束用户相关性与工具频率，动态系统权重调节偏好目标，让适合的查询更易触发工具。频率是治理信号而非质量本身，必须同时检查上下文相关性是否下降。 示意：用户问实时航班时适合查工具，问概念定义时未必需要。即使某工具使用率偏低，也不能为了拉高频次让所有问题都调用它，用户侧校准应约束这种倾向。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:toolrec" data-paper-title="ToolRec: Calibrated Preference Alignment for Query Recommendation in On-Device Assistants" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="ToolRec: Calibrated Preference Alignment for Query Recommendation in On-Device Assistants 搜广推与 LLM 应用 Huazhong University of Science and Technology 2026-06-07 在 KTO 式偏好目标上同时加入用户侧校准与工具频率驱动的动态系统侧校准，提升会触发工具的查询，同时约束上下文相关性下降。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04819，相对变化 -10.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。  query-recommendation preference-alignment tool-use 搜广推 候选生成与搜索匹配 工具频率动态权重与固定正负样本比例有什么差别？ 动态权重随系统使用统计变化，固定比例不感知当前分布。频率也不是用户效用，不能为多调用工具牺牲上下文相关性后仍只报触发率提升。 例如低频工具被增加机会，仍须判断它是否适合这次用户请求。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b00694e9f0f66520">工具频率动态权重与固定正负样本比例有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atoolrec">ToolRec: Calibrated Preference Alignment for Query Recommendation in On-Device Assistants</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huazhong University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>动态权重随系统使用统计变化，固定比例不感知当前分布。频率也不是用户效用，不能为多调用工具牺牲上下文相关性后仍只报触发率提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如低频工具被增加机会，仍须判断它是否适合这次用户请求。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.08466">原论文</a> · <a href="../../../../reproductions/2606.08466-toolrec/">实现解读</a> · <a href="#qa-b00694e9f0f66520">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:toolrec" data-paper-title="ToolRec: Calibrated Preference Alignment for Query Recommendation in On-Device Assistants" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="ToolRec: Calibrated Preference Alignment for Query Recommendation in On-Device Assistants 搜广推与 LLM 应用 Huazhong University of Science and Technology 2026-06-07 在 KTO 式偏好目标上同时加入用户侧校准与工具频率驱动的动态系统侧校准，提升会触发工具的查询，同时约束上下文相关性下降。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04819，相对变化 -10.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。  query-recommendation preference-alignment tool-use 搜广推 候选生成与搜索匹配 ToolRec本地MovieLens代理是否真实执行工具？ 没有真实工具query或私有session，仅验证校准目标和打分路径。频率统计需来自训练允许窗口并固定版本，不能用测试未来调用率调权重。 例如电影类别频率不是实际API成本或工具服务负载。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6d1486b37d004bc3">ToolRec本地MovieLens代理是否真实执行工具？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atoolrec">ToolRec: Calibrated Preference Alignment for Query Recommendation in On-Device Assistants</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huazhong University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有真实工具query或私有session，仅验证校准目标和打分路径。频率统计需来自训练允许窗口并固定版本，不能用测试未来调用率调权重。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如电影类别频率不是实际API成本或工具服务负载。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.08466">原论文</a> · <a href="../../../../reproductions/2606.08466-toolrec/">实现解读</a> · <a href="#qa-6d1486b37d004bc3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:harness-lm" data-paper-title="HARNESS-LM: A Three-Phase Training Recipe for Harnessing SLMs in Sponsored Search Retrieval" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="HARNESS-LM: A Three-Phase Training Recipe for Harnessing SLMs in Sponsored Search Retrieval 搜广推与 LLM 应用 Microsoft AI / Bing Ads 2026-05-22 Sponsored Search 可以离线使用昂贵文档编码器，却要求在线 query encoder 足够小。HARNESS-LM 先训练强 teacher，再让小 query encoder 直接对齐 teacher query 空间，最后冻结 teacher 文档塔做监督对比精修，避免重建索引。 Fidelity: 核心机制复现。Teacher、L2 embedding alignment、冻结 teacher document index 的 contrastive refinement 三阶段均实际执行。协同 SVD+内容代理 Qwen3-Embedding teacher；未复刻 4B/0.6B 规模、GPT expansion 与 CPU pruning frontier。本地对照口径：基线是小型对称内容 retriever；实验组 HARNESS-LM 使用强协同文档空间、L2 对齐与对比精修，相对基线 Hit@10 -23.08%、NDCG@10 -28.05%。  llm-recommendation retrieval distillation 搜广推 候选生成与搜索匹配 HARNESS-LM 为什么容许离线 document encoder 很大、在线 query encoder 很小？ 文档可提前编码并重复使用，查询到来才产生、延迟敏感，因此非对称计算预算更符合服务成本。小 query 先对齐强空间，再在冻结文档塔下对比精修。两侧规模不同不保证质量无损，学生仍可能无法表达教师复杂意图。 示意：百万广告向量夜间预算好，用户一句查询需几毫秒处理；把重模型放文档侧能摊销成本，而非每个请求都运行两份大网络。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-harness-lm-9919eb79" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-71f6c9ca8eea9645">HARNESS-LM 为什么容许离线 document encoder 很大、在线 query encoder 很小？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aharness-lm">HARNESS-LM: A Three-Phase Training Recipe for Harnessing SLMs in Sponsored Search Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft AI / Bing Ads</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档可提前编码并重复使用，查询到来才产生、延迟敏感，因此非对称计算预算更符合服务成本。小 query 先对齐强空间，再在冻结文档塔下对比精修。两侧规模不同不保证质量无损，学生仍可能无法表达教师复杂意图。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>百万广告向量夜间预算好，用户一句查询需几毫秒处理；把重模型放文档侧能摊销成本，而非每个请求都运行两份大网络。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.23572">原论文</a> · <a href="../../../../reproductions/2605.23572-harness-lm/">实现解读</a> · <a href="#qa-71f6c9ca8eea9645">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:harness-lm" data-paper-title="HARNESS-LM: A Three-Phase Training Recipe for Harnessing SLMs in Sponsored Search Retrieval" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="HARNESS-LM: A Three-Phase Training Recipe for Harnessing SLMs in Sponsored Search Retrieval 搜广推与 LLM 应用 Microsoft AI / Bing Ads 2026-05-22 Sponsored Search 可以离线使用昂贵文档编码器，却要求在线 query encoder 足够小。HARNESS-LM 先训练强 teacher，再让小 query encoder 直接对齐 teacher query 空间，最后冻结 teacher 文档塔做监督对比精修，避免重建索引。 Fidelity: 核心机制复现。Teacher、L2 embedding alignment、冻结 teacher document index 的 contrastive refinement 三阶段均实际执行。协同 SVD+内容代理 Qwen3-Embedding teacher；未复刻 4B/0.6B 规模、GPT expansion 与 CPU pruning frontier。本地对照口径：基线是小型对称内容 retriever；实验组 HARNESS-LM 使用强协同文档空间、L2 对齐与对比精修，相对基线 Hit@10 -23.08%、NDCG@10 -28.05%。  llm-recommendation retrieval distillation 搜广推 候选生成与搜索匹配 HARNESS-LM精修时为什么冻结强文档塔，只训练小query encoder？ 文档向量可以提前离线计算，在线请求侧却需要轻量且低延迟。小查询塔先对齐teacher查询空间，再在固定文档空间里用对比监督精修，避免一边训练一边让索引坐标漂移、反复重建全库。冻结减少部署变化，也限制目标域适应能力，不能默认小模型必然达到teacher质量。 示意：已有百万广告向量由强文档塔建好，小查询塔只需学会在这套坐标里找对象；若同时更新文档塔，旧索引可能失效，部署成本远不止查询模型变小。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:harness-lm" data-paper-title="HARNESS-LM: A Three-Phase Training Recipe for Harnessing SLMs in Sponsored Search Retrieval" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="HARNESS-LM: A Three-Phase Training Recipe for Harnessing SLMs in Sponsored Search Retrieval 搜广推与 LLM 应用 Microsoft AI / Bing Ads 2026-05-22 Sponsored Search 可以离线使用昂贵文档编码器，却要求在线 query encoder 足够小。HARNESS-LM 先训练强 teacher，再让小 query encoder 直接对齐 teacher query 空间，最后冻结 teacher 文档塔做监督对比精修，避免重建索引。 Fidelity: 核心机制复现。Teacher、L2 embedding alignment、冻结 teacher document index 的 contrastive refinement 三阶段均实际执行。协同 SVD+内容代理 Qwen3-Embedding teacher；未复刻 4B/0.6B 规模、GPT expansion 与 CPU pruning frontier。本地对照口径：基线是小型对称内容 retriever；实验组 HARNESS-LM 使用强协同文档空间、L2 对齐与对比精修，相对基线 Hit@10 -23.08%、NDCG@10 -28.05%。  llm-recommendation retrieval distillation 搜广推 候选生成与搜索匹配 HARNESS-LM 的 L2 对齐与后续 InfoNCE 精修，为什么不是重复目标？ L2 让学生坐标接近教师 query，提供空间初始化；InfoNCE 再直接优化对固定文档的区分，关注检索关系而非逐维误差。对齐误差下降不保证排名提升，来源本地损失收敛但检索退化正说明这两类证据不同。 示意：向量更接近教师平均位置仍可能在两个相似广告间排错；对比精修专门比较正确广告与竞争广告，需要另外检验。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c7582077c51c0e0b">HARNESS-LM 的 L2 对齐与后续 InfoNCE 精修，为什么不是重复目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aharness-lm">HARNESS-LM: A Three-Phase Training Recipe for Harnessing SLMs in Sponsored Search Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft AI / Bing Ads</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>L2 让学生坐标接近教师 query，提供空间初始化；InfoNCE 再直接优化对固定文档的区分，关注检索关系而非逐维误差。对齐误差下降不保证排名提升，来源本地损失收敛但检索退化正说明这两类证据不同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>向量更接近教师平均位置仍可能在两个相似广告间排错；对比精修专门比较正确广告与竞争广告，需要另外检验。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.23572">原论文</a> · <a href="../../../../reproductions/2605.23572-harness-lm/">实现解读</a> · <a href="#qa-c7582077c51c0e0b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:harness-lm" data-paper-title="HARNESS-LM: A Three-Phase Training Recipe for Harnessing SLMs in Sponsored Search Retrieval" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="HARNESS-LM: A Three-Phase Training Recipe for Harnessing SLMs in Sponsored Search Retrieval 搜广推与 LLM 应用 Microsoft AI / Bing Ads 2026-05-22 Sponsored Search 可以离线使用昂贵文档编码器，却要求在线 query encoder 足够小。HARNESS-LM 先训练强 teacher，再让小 query encoder 直接对齐 teacher query 空间，最后冻结 teacher 文档塔做监督对比精修，避免重建索引。 Fidelity: 核心机制复现。Teacher、L2 embedding alignment、冻结 teacher document index 的 contrastive refinement 三阶段均实际执行。协同 SVD+内容代理 Qwen3-Embedding teacher；未复刻 4B/0.6B 规模、GPT expansion 与 CPU pruning frontier。本地对照口径：基线是小型对称内容 retriever；实验组 HARNESS-LM 使用强协同文档空间、L2 对齐与对比精修，相对基线 Hit@10 -23.08%、NDCG@10 -28.05%。  llm-recommendation retrieval distillation 搜广推 候选生成与搜索匹配 HARNESS-LM 精修为什么必须确认 teacher document 参数没有梯度？ 冻结文档塔让既有索引保持一致，只有学生 query 改变以适应该空间；若文档也更新，原无需重建索引的部署条件就失效。可检查参数摘要或梯度范围，不能只看优化器名。小模型对齐成功也不能由此推断线上索引已更新。 示意：训练一步后 query 参数变化而文档不变符合契约；若文档向量也移动，继续用旧索引就会和新评分空间错位。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-2614230fc91437a1">HARNESS-LM 精修为什么必须确认 teacher document 参数没有梯度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aharness-lm">HARNESS-LM: A Three-Phase Training Recipe for Harnessing SLMs in Sponsored Search Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft AI / Bing Ads</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冻结文档塔让既有索引保持一致，只有学生 query 改变以适应该空间；若文档也更新，原无需重建索引的部署条件就失效。可检查参数摘要或梯度范围，不能只看优化器名。小模型对齐成功也不能由此推断线上索引已更新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练一步后 query 参数变化而文档不变符合契约；若文档向量也移动，继续用旧索引就会和新评分空间错位。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.23572">原论文</a> · <a href="../../../../reproductions/2605.23572-harness-lm/">实现解读</a> · <a href="#qa-2614230fc91437a1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:llm-ad-retrieval" data-paper-title="LLM Retrieval for Stable and Predictable Ad Recommendations" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="LLM Retrieval for Stable and Predictable Ad Recommendations 搜广推与 LLM 应用 Meta 2026-05-21 广告候选生成通常只优化点击/转化预测与 Recall，轻微修改 creative 后却可能因为 ID 或稀疏特征变化而得到完全不同的投放结果。论文新增 A/A&#x27; predictability 框架：复制 primary ad 为 shadow ad，只做不改变语义的输入扰动，再衡量两者转换和曝光差异。模型侧用经过广告检索任务适配的 LLM 从标题、描述等 creative 中抽取层级 category、brand、product 和 context 属性； Fidelity: 核心机制复现。本地实际执行成对 creative 的领域 SFT、LLM hidden-state 属性头、层级离散语义表示、phrase→token 两级 Jaccard 建图、协同图融合、validation 选权重，以及扰动稳定性评估；未复刻 Meta 私有广告语料、Llama-3-8B、分布式推理、线上转换与 shadow-ad 流量系统。本地对照口径：基线是 Collaborative Item Graph；实验组是在固定候选预算下加入 LLM Semantic Graph；Recall@20 +11.90%、NDCG@20 +3.03%，边分数漂移 -77.36%。  llm-recommendation retrieval stability 搜广推 候选生成与搜索匹配 A/A′ shadow ad 为什么要求扰动不改变广告语义？ 目标检验检索对无关输入变化的稳定性，若内容意图本就改变，分发差异可能合理。primary 与 shadow 只改格式或等义表达，才更接近测模型是否过度依赖 ID 与稀疏外观。稳定不等于相关，始终输出同样错误候选也可稳定。 示意：只改标点和年份表达应大体保持受众；把“儿童鞋”改成“登山鞋”却期待一样分发，是把真实语义变化误当噪声。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-llm-ad-retrieval-68e38a71" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ec68ff836f180cae">A/A′ shadow ad 为什么要求扰动不改变广告语义？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Allm-ad-retrieval">LLM Retrieval for Stable and Predictable Ad Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标检验检索对无关输入变化的稳定性，若内容意图本就改变，分发差异可能合理。primary 与 shadow 只改格式或等义表达，才更接近测模型是否过度依赖 ID 与稀疏外观。稳定不等于相关，始终输出同样错误候选也可稳定。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>只改标点和年份表达应大体保持受众；把“儿童鞋”改成“登山鞋”却期待一样分发，是把真实语义变化误当噪声。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.21969">原论文</a> · <a href="../../../../reproductions/2605.21969-llm-ad-retrieval/">实现解读</a> · <a href="#qa-ec68ff836f180cae">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:llm-ad-retrieval" data-paper-title="LLM Retrieval for Stable and Predictable Ad Recommendations" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="LLM Retrieval for Stable and Predictable Ad Recommendations 搜广推与 LLM 应用 Meta 2026-05-21 广告候选生成通常只优化点击/转化预测与 Recall，轻微修改 creative 后却可能因为 ID 或稀疏特征变化而得到完全不同的投放结果。论文新增 A/A&#x27; predictability 框架：复制 primary ad 为 shadow ad，只做不改变语义的输入扰动，再衡量两者转换和曝光差异。模型侧用经过广告检索任务适配的 LLM 从标题、描述等 creative 中抽取层级 category、brand、product 和 context 属性； Fidelity: 核心机制复现。本地实际执行成对 creative 的领域 SFT、LLM hidden-state 属性头、层级离散语义表示、phrase→token 两级 Jaccard 建图、协同图融合、validation 选权重，以及扰动稳定性评估；未复刻 Meta 私有广告语料、Llama-3-8B、分布式推理、线上转换与 shadow-ad 流量系统。本地对照口径：基线是 Collaborative Item Graph；实验组是在固定候选预算下加入 LLM Semantic Graph；Recall@20 +11.90%、NDCG@20 +3.03%，边分数漂移 -77.36%。  llm-recommendation retrieval stability 搜广推 候选生成与搜索匹配 LLM广告召回为什么增加A/A′可预测性检查，而不只看Recall？ 语义几乎不变的创意轻微改动可能因ID与稀疏信号导致投放剧烈变化，Recall却未必暴露这种不稳定。primary与shadow对照衡量扰动后的转换和曝光差异；层级语义属性与广告图提供较可迁移的召回关系。稳定性评价仍需控制统计噪声，不能把任何小样本差异都判为模型失效。 示意：广告只换了不改变产品含义的措辞，却几乎失去曝光，普通命中率可能仍很好；复制对照能专门检查系统是否对这种语义等价变化过度敏感。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:llm-ad-retrieval" data-paper-title="LLM Retrieval for Stable and Predictable Ad Recommendations" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="LLM Retrieval for Stable and Predictable Ad Recommendations 搜广推与 LLM 应用 Meta 2026-05-21 广告候选生成通常只优化点击/转化预测与 Recall，轻微修改 creative 后却可能因为 ID 或稀疏特征变化而得到完全不同的投放结果。论文新增 A/A&#x27; predictability 框架：复制 primary ad 为 shadow ad，只做不改变语义的输入扰动，再衡量两者转换和曝光差异。模型侧用经过广告检索任务适配的 LLM 从标题、描述等 creative 中抽取层级 category、brand、product 和 context 属性； Fidelity: 核心机制复现。本地实际执行成对 creative 的领域 SFT、LLM hidden-state 属性头、层级离散语义表示、phrase→token 两级 Jaccard 建图、协同图融合、validation 选权重，以及扰动稳定性评估；未复刻 Meta 私有广告语料、Llama-3-8B、分布式推理、线上转换与 shadow-ad 流量系统。本地对照口径：基线是 Collaborative Item Graph；实验组是在固定候选预算下加入 LLM Semantic Graph；Recall@20 +11.90%、NDCG@20 +3.03%，边分数漂移 -77.36%。  llm-recommendation retrieval stability 搜广推 候选生成与搜索匹配 LLM 语义图与协同 item graph，相比为新品与稳定性提供什么不同来源？ 协同图来自历史共同消费，语义图从创意属性连接广告，可在行为少时补边并减少无义改写造成的漂移。语义提取也会幻觉，图扩展需置信度与预算控制。来源本地是固定预算路由增量，不是端到端广告效果或强随机训练方差证明。 示意：新广告没有共点边，品牌与用途属性仍可连到用户种子广告；若模型错认品牌，也会扩到错误候选，不能只看边数量更多。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-14f5757cdd50ff78">LLM 语义图与协同 item graph，相比为新品与稳定性提供什么不同来源？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Allm-ad-retrieval">LLM Retrieval for Stable and Predictable Ad Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>协同图来自历史共同消费，语义图从创意属性连接广告，可在行为少时补边并减少无义改写造成的漂移。语义提取也会幻觉，图扩展需置信度与预算控制。来源本地是固定预算路由增量，不是端到端广告效果或强随机训练方差证明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新广告没有共点边，品牌与用途属性仍可连到用户种子广告；若模型错认品牌，也会扩到错误候选，不能只看边数量更多。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.21969">原论文</a> · <a href="../../../../reproductions/2605.21969-llm-ad-retrieval/">实现解读</a> · <a href="#qa-14f5757cdd50ff78">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:llm-ad-retrieval" data-paper-title="LLM Retrieval for Stable and Predictable Ad Recommendations" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="LLM Retrieval for Stable and Predictable Ad Recommendations 搜广推与 LLM 应用 Meta 2026-05-21 广告候选生成通常只优化点击/转化预测与 Recall，轻微修改 creative 后却可能因为 ID 或稀疏特征变化而得到完全不同的投放结果。论文新增 A/A&#x27; predictability 框架：复制 primary ad 为 shadow ad，只做不改变语义的输入扰动，再衡量两者转换和曝光差异。模型侧用经过广告检索任务适配的 LLM 从标题、描述等 creative 中抽取层级 category、brand、product 和 context 属性； Fidelity: 核心机制复现。本地实际执行成对 creative 的领域 SFT、LLM hidden-state 属性头、层级离散语义表示、phrase→token 两级 Jaccard 建图、协同图融合、validation 选权重，以及扰动稳定性评估；未复刻 Meta 私有广告语料、Llama-3-8B、分布式推理、线上转换与 shadow-ad 流量系统。本地对照口径：基线是 Collaborative Item Graph；实验组是在固定候选预算下加入 LLM Semantic Graph；Recall@20 +11.90%、NDCG@20 +3.03%，边分数漂移 -77.36%。  llm-recommendation retrieval stability 搜广推 候选生成与搜索匹配 本地 LLM 广告召回为什么不能把三次 tie-breaking seed 的相同结果写成训练方差为零？ 训练链路本身并未在三种子下独立重训，且实际没有分数 tie，改变 tie-breaking 不会改变候选。它只能说明该后处理确定性，不能估计模型训练不确定度。A/A′ 属性和分数漂移、Recall 与 NDCG 也要分别报告。 示意：同一 checkpoint 对同分不存在的列表改随机排序种子，输出三次一致很自然；不能据此声称模型三次训练都得到稳定同样收益。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3159eea7b4ec5c7a">本地 LLM 广告召回为什么不能把三次 tie-breaking seed 的相同结果写成训练方差为零？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Allm-ad-retrieval">LLM Retrieval for Stable and Predictable Ad Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>训练链路本身并未在三种子下独立重训，且实际没有分数 tie，改变 tie-breaking 不会改变候选。它只能说明该后处理确定性，不能估计模型训练不确定度。A/A′ 属性和分数漂移、Recall 与 NDCG 也要分别报告。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一 checkpoint 对同分不存在的列表改随机排序种子，输出三次一致很自然；不能据此声称模型三次训练都得到稳定同样收益。</p>
<p class="ar-learning-sources">依据：本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.21969">原论文</a> · <a href="../../../../reproductions/2605.21969-llm-ad-retrieval/">实现解读</a> · <a href="#qa-3159eea7b4ec5c7a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mdcns" data-paper-title="Divergence Meets Consensus: A Multi-Source Negative Sampling Framework for Sequential Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Divergence Meets Consensus: A Multi-Source Negative Sampling Framework for Sequential Recommendation 搜广推与 LLM 应用 论文作者团队（原文未标注公司） 2026-05-19 随机负采样太容易，DNS 只追逐单模型高分负例又容易产生 false negative、低多样性和模型偏置。MDCNS 受“最近发展区”启发，引入 Self、Peer、Teacher 三个视角：Self 与异构 Peer 分别评分，Teacher 聚合两者；再用两模型分歧提升“困难且有信息量”的候选，最后把 Teacher 在完整候选池上的分布蒸馏回 Self，避免候选打分只利用一个负例。 Fidelity: 核心机制复现。三源负采样、双模型分歧/共识选择与更新实际执行；推荐 backbone 缩小为本地可训练模型。本地对照口径：主基线是 Uniform negative sampling，辅助基线是 DNS；实验组是 MDCNS；NDCG@10 相对 Uniform 从 0.003016 升至 0.006175（+104.75%）。这是采样策略消融；DIN 不适用于该采样器级比较。   搜广推 候选生成与搜索匹配 MDCNS 为什么用 Self、Peer 和 Teacher 三个视角看负例？ 单模型高分可能是偏置或真实未标正例，异构 Peer 提供另一判断，Teacher 聚合两者，再利用分歧找困难且可能有信息的候选。分歧并不天然等于正确困难度，假负例仍可能存在；完整候选池蒸馏补充单次选负例丢掉的信息。 示意：Self 很确信一件相机是负例而 Peer 认为相近，这份分歧值得学习；但用户也许真喜欢它，不能将未交互直接视作确定不喜欢。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-mdcns-8e8ced60" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7c4b021a66342a05">MDCNS 为什么用 Self、Peer 和 Teacher 三个视角看负例？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amdcns">Divergence Meets Consensus: A Multi-Source Negative Sampling Framework for Sequential Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文作者团队（原文未标注公司）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单模型高分可能是偏置或真实未标正例，异构 Peer 提供另一判断，Teacher 聚合两者，再利用分歧找困难且可能有信息的候选。分歧并不天然等于正确困难度，假负例仍可能存在；完整候选池蒸馏补充单次选负例丢掉的信息。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>Self 很确信一件相机是负例而 Peer 认为相近，这份分歧值得学习；但用户也许真喜欢它，不能将未交互直接视作确定不喜欢。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.19651">原论文</a> · <a href="../../../../reproductions/2605.19651-mdcns/">实现解读</a> · <a href="#qa-7c4b021a66342a05">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mdcns" data-paper-title="Divergence Meets Consensus: A Multi-Source Negative Sampling Framework for Sequential Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Divergence Meets Consensus: A Multi-Source Negative Sampling Framework for Sequential Recommendation 搜广推与 LLM 应用 论文作者团队（原文未标注公司） 2026-05-19 随机负采样太容易，DNS 只追逐单模型高分负例又容易产生 false negative、低多样性和模型偏置。MDCNS 受“最近发展区”启发，引入 Self、Peer、Teacher 三个视角：Self 与异构 Peer 分别评分，Teacher 聚合两者；再用两模型分歧提升“困难且有信息量”的候选，最后把 Teacher 在完整候选池上的分布蒸馏回 Self，避免候选打分只利用一个负例。 Fidelity: 核心机制复现。三源负采样、双模型分歧/共识选择与更新实际执行；推荐 backbone 缩小为本地可训练模型。本地对照口径：主基线是 Uniform negative sampling，辅助基线是 DNS；实验组是 MDCNS；NDCG@10 相对 Uniform 从 0.003016 升至 0.006175（+104.75%）。这是采样策略消融；DIN 不适用于该采样器级比较。   搜广推 候选生成与搜索匹配 MDCNS为什么同时看Self与Peer分歧，而不是永远选择Self分最高的负例？ 单模型高分可能只是自身偏置或潜在正例，始终追它会降低多样性。异构Peer提供另一视角，分歧帮助识别值得学习的候选，Teacher再把完整候选池关系蒸馏回Self，避免只利用一个负例。分歧不等于标签为负的证据，采样仍需控制假负例风险与训练稳定性。 示意：Self把某类热门商品都打高，Peer并不认同；只按Self挖负例会重复其偏见，多视角可暴露这种不确定性，但不能断言所有分歧商品都不相关。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mdcns" data-paper-title="Divergence Meets Consensus: A Multi-Source Negative Sampling Framework for Sequential Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Divergence Meets Consensus: A Multi-Source Negative Sampling Framework for Sequential Recommendation 搜广推与 LLM 应用 论文作者团队（原文未标注公司） 2026-05-19 随机负采样太容易，DNS 只追逐单模型高分负例又容易产生 false negative、低多样性和模型偏置。MDCNS 受“最近发展区”启发，引入 Self、Peer、Teacher 三个视角：Self 与异构 Peer 分别评分，Teacher 聚合两者；再用两模型分歧提升“困难且有信息量”的候选，最后把 Teacher 在完整候选池上的分布蒸馏回 Self，避免候选打分只利用一个负例。 Fidelity: 核心机制复现。三源负采样、双模型分歧/共识选择与更新实际执行；推荐 backbone 缩小为本地可训练模型。本地对照口径：主基线是 Uniform negative sampling，辅助基线是 DNS；实验组是 MDCNS；NDCG@10 相对 Uniform 从 0.003016 升至 0.006175（+104.75%）。这是采样策略消融；DIN 不适用于该采样器级比较。   搜广推 候选生成与搜索匹配 MDCNS 的 Top-M 随机选与 DNS 固定选最高分，相比为何保留随机性？ 永远最难容易反复追同一异常或假负例，Top-M 内随机选择扩大困难区域的覆盖。分歧重排和多源损失再减少单模型主导，仍受候选池质量影响。来源轻 Markov backbone 的增益只支持采样路径，不等于复现大型序列模型水平。 示意：最高分总是同一热门电影，固定 DNS 每步都选它；在前五困难项中随机抽，可避免所有更新围绕一个疑似假负例。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1cc07ab0f592c36a">MDCNS 的 Top-M 随机选与 DNS 固定选最高分，相比为何保留随机性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amdcns">Divergence Meets Consensus: A Multi-Source Negative Sampling Framework for Sequential Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文作者团队（原文未标注公司）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>永远最难容易反复追同一异常或假负例，Top-M 内随机选择扩大困难区域的覆盖。分歧重排和多源损失再减少单模型主导，仍受候选池质量影响。来源轻 Markov backbone 的增益只支持采样路径，不等于复现大型序列模型水平。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>最高分总是同一热门电影，固定 DNS 每步都选它；在前五困难项中随机抽，可避免所有更新围绕一个疑似假负例。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.19651">原论文</a> · <a href="../../../../reproductions/2605.19651-mdcns/">实现解读</a> · <a href="#qa-1cc07ab0f592c36a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mdcns" data-paper-title="Divergence Meets Consensus: A Multi-Source Negative Sampling Framework for Sequential Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Divergence Meets Consensus: A Multi-Source Negative Sampling Framework for Sequential Recommendation 搜广推与 LLM 应用 论文作者团队（原文未标注公司） 2026-05-19 随机负采样太容易，DNS 只追逐单模型高分负例又容易产生 false negative、低多样性和模型偏置。MDCNS 受“最近发展区”启发，引入 Self、Peer、Teacher 三个视角：Self 与异构 Peer 分别评分，Teacher 聚合两者；再用两模型分歧提升“困难且有信息量”的候选，最后把 Teacher 在完整候选池上的分布蒸馏回 Self，避免候选打分只利用一个负例。 Fidelity: 核心机制复现。三源负采样、双模型分歧/共识选择与更新实际执行；推荐 backbone 缩小为本地可训练模型。本地对照口径：主基线是 Uniform negative sampling，辅助基线是 DNS；实验组是 MDCNS；NDCG@10 相对 Uniform 从 0.003016 升至 0.006175（+104.75%）。这是采样策略消融；DIN 不适用于该采样器级比较。   搜广推 候选生成与搜索匹配 MDCNS 的 Teacher KL 为什么在完整候选池计算，而非仅选中的一个负例？ 单负例只有局部比较，Teacher 分布覆盖全部候选，传递其他难易关系；Self 与 Peer 分数及列身份须对齐，温度和 τ² 保持定义尺度。未交互集合也只能按训练截止构造，不能用测试答案决定哪些负例可保留。 示意：三十个候选只抽一个训练 pair，KL 仍能告诉 Self 其余哪些更接近；若只对单个标量归一为一，就没有这份分布知识。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-55b0814cd9fac24b">MDCNS 的 Teacher KL 为什么在完整候选池计算，而非仅选中的一个负例？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amdcns">Divergence Meets Consensus: A Multi-Source Negative Sampling Framework for Sequential Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文作者团队（原文未标注公司）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单负例只有局部比较，Teacher 分布覆盖全部候选，传递其他难易关系；Self 与 Peer 分数及列身份须对齐，温度和 τ² 保持定义尺度。未交互集合也只能按训练截止构造，不能用测试答案决定哪些负例可保留。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三十个候选只抽一个训练 pair，KL 仍能告诉 Self 其余哪些更接近；若只对单个标量归一为一，就没有这份分布知识。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.19651">原论文</a> · <a href="../../../../reproductions/2605.19651-mdcns/">实现解读</a> · <a href="#qa-55b0814cd9fac24b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:policy-facet" data-paper-title="Policy-Grounded Dynamic Facet Suggestions for Job Search" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Policy-Grounded Dynamic Facet Suggestions for Job Search 搜广推与 LLM 应用 LinkedIn 2026-05-15 先由人工与 LLM 维护符合产品策略的 facet taxonomy，再用 embedding SLM 召回候选，以生成式 SLM 做单 token 点式评分；前缀缓存和批处理满足实时延迟。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04713，相对变化 -12.73%。本地代理目标与论文生产任务不同，不能外推线上 lift。  job-search facet-retrieval policy-ranking 搜广推 候选生成与搜索匹配 Policy Facet 的 facet 与最终商品或文档结果，是同一种候选吗？ 不是。facet 是帮助用户细化搜索的主题或属性选项，选中后可改变接下来的查询或浏览范围；item 是实际检索对象。分面先要符合 taxonomy 和当前需求，再判断它是否提供有用细化。不能因某商品得分高，就直接把商品标题当作合适分面。 示意：旅行搜索里的“亲子活动”是细化方向，具体博物馆门票是结果；前者帮助选择需求，后者满足需求，两者不应共用无说明的标签。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-policy-facet-10555aa9" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-1d64a12b7237f3f1">Policy Facet 的 facet 与最终商品或文档结果，是同一种候选吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apolicy-facet">Policy-Grounded Dynamic Facet Suggestions for Job Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。facet 是帮助用户细化搜索的主题或属性选项，选中后可改变接下来的查询或浏览范围；item 是实际检索对象。分面先要符合 taxonomy 和当前需求，再判断它是否提供有用细化。不能因某商品得分高，就直接把商品标题当作合适分面。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>旅行搜索里的“亲子活动”是细化方向，具体博物馆门票是结果；前者帮助选择需求，后者满足需求，两者不应共用无说明的标签。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.16479">原论文</a> · <a href="../../../../reproductions/2605.16479-policy-facet/">实现解读</a> · <a href="#qa-1d64a12b7237f3f1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:policy-facet" data-paper-title="Policy-Grounded Dynamic Facet Suggestions for Job Search" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Policy-Grounded Dynamic Facet Suggestions for Job Search 搜广推与 LLM 应用 LinkedIn 2026-05-15 先由人工与 LLM 维护符合产品策略的 facet taxonomy，再用 embedding SLM 召回候选，以生成式 SLM 做单 token 点式评分；前缀缓存和批处理满足实时延迟。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04713，相对变化 -12.73%。本地代理目标与论文生产任务不同，不能外推线上 lift。  job-search facet-retrieval policy-ranking 搜广推 候选生成与搜索匹配 Policy Facet 为什么先维护受产品策略约束的分类，再用小模型召回和单 token 评分？ 受维护的 facet 集合先限定可推荐的主题边界，避免生成器随意提出不符合策略的选项。嵌入模型在集合内低成本召回，生成式小模型再根据用户与查询输出“Okay”等单 token 的概率评分。它把开放生成转为受控候选判断，并用缓存和批处理降延迟；概率高仍不等于策略已经自动完备。 示意：搜索亲子旅行时，系统只从经过维护的目的地与活动主题里选候选，再判断哪些最适合当前查询。模型不需要现场编造新的分类名称，也更便于检查推荐范围。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:policy-facet" data-paper-title="Policy-Grounded Dynamic Facet Suggestions for Job Search" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Policy-Grounded Dynamic Facet Suggestions for Job Search 搜广推与 LLM 应用 LinkedIn 2026-05-15 先由人工与 LLM 维护符合产品策略的 facet taxonomy，再用 embedding SLM 召回候选，以生成式 SLM 做单 token 点式评分；前缀缓存和批处理满足实时延迟。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04713，相对变化 -12.73%。本地代理目标与论文生产任务不同，不能外推线上 lift。  job-search facet-retrieval policy-ranking 搜广推 候选生成与搜索匹配 单 token Okay 概率与生成完整评语，为什么更适合低延迟候选打分？ 固定输出将评价转成受控点式概率，避免每个候选长解码，前缀缓存和批处理可进一步复用。它丢掉在线详细理由，概率也需校准；不是输出单词就天然更准确。候选召回遗漏无法靠评分弥补。 示意：十个分面各问一次是否适合并读 Okay 概率，比让模型逐项写百字分析便宜；但遗漏的合适分面从未被评，就仍选不到。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4f7b6dbe5963d4ef">单 token Okay 概率与生成完整评语，为什么更适合低延迟候选打分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apolicy-facet">Policy-Grounded Dynamic Facet Suggestions for Job Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定输出将评价转成受控点式概率，避免每个候选长解码，前缀缓存和批处理可进一步复用。它丢掉在线详细理由，概率也需校准；不是输出单词就天然更准确。候选召回遗漏无法靠评分弥补。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>十个分面各问一次是否适合并读 Okay 概率，比让模型逐项写百字分析便宜；但遗漏的合适分面从未被评，就仍选不到。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.16479">原论文</a> · <a href="../../../../reproductions/2605.16479-policy-facet/">实现解读</a> · <a href="#qa-4f7b6dbe5963d4ef">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:policy-facet" data-paper-title="Policy-Grounded Dynamic Facet Suggestions for Job Search" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Policy-Grounded Dynamic Facet Suggestions for Job Search 搜广推与 LLM 应用 LinkedIn 2026-05-15 先由人工与 LLM 维护符合产品策略的 facet taxonomy，再用 embedding SLM 召回候选，以生成式 SLM 做单 token 点式评分；前缀缓存和批处理满足实时延迟。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04713，相对变化 -12.73%。本地代理目标与论文生产任务不同，不能外推线上 lift。  job-search facet-retrieval policy-ranking 搜广推 候选生成与搜索匹配 Policy Facet 读取 Okay 的分数时，为什么要核验 tokenizer 与完整条件前缀？ 目标词可能不是任意模型的一枚同义 token，分数需对应约定输出与同一用户、查询、候选条件。只读某个固定词表索引会在模型更换后错位；候选前缀缓存也不能混入另一分面。来源本地代理不证明完整小模型服务延迟。 示意：换模型后 Okay 拆成两片，仍取旧单 token 索引就测了别的词；分数有限也不能说明点式判断正确。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-eaf1989efcddb804">Policy Facet 读取 Okay 的分数时，为什么要核验 tokenizer 与完整条件前缀？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apolicy-facet">Policy-Grounded Dynamic Facet Suggestions for Job Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标词可能不是任意模型的一枚同义 token，分数需对应约定输出与同一用户、查询、候选条件。只读某个固定词表索引会在模型更换后错位；候选前缀缓存也不能混入另一分面。来源本地代理不证明完整小模型服务延迟。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>换模型后 Okay 拆成两片，仍取旧单 token 索引就测了别的词；分数有限也不能说明点式判断正确。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.16479">原论文</a> · <a href="../../../../reproductions/2605.16479-policy-facet/">实现解读</a> · <a href="#qa-eaf1989efcddb804">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cs3" data-paper-title="CS3: Efficient Online Capability Synergy for Two-Tower Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="CS3: Efficient Online Capability Synergy for Two-Tower Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-04-21 传统双塔为 ANN 解耦 user/item 表征，牺牲交叉能力。CS3 通过离线/在线可部署的循环修正和知识协同增强塔间交互。 三 seed NDCG@10 相对 -16.06%，当前小数据未复现线上收益。Fidelity: 核心机制复现。实现双塔间的循环自修正、显式交叉同步与级联教师辅助目标。没有 4 亿 DAU 的在线缓存、EMA 跨塔向量和生产 QPS 链路。本地对照口径：基线是 matched two-tower；实验组加入 cycle、cross sync 与 teacher loss；三 seed NDCG@10 相对 -16.06%，当前小数据未复现线上收益。  retrieval two-tower online-learning 搜广推 候选生成与搜索匹配 CS3 为什么称双塔交互是召回效率与表达力之间的冲突？ 独立塔让物品向量可预计算、用户向量可一次计算，适合近邻检索；深度用户—物品交互则通常依赖具体配对，难直接缓存。循环修正与知识协同尝试在可部署边界内增加联系，不能简单把全交叉模型原封不动当成 ANN 双塔。 示意：商品向量若每换用户都改变，就不能只存一份通用索引；双塔高效正来自这种解耦，增强交互时必须保留清晰的服务路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-cs3-e2cd1a82" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2c2970df359ab633">CS3 为什么称双塔交互是召回效率与表达力之间的冲突？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acs3">CS3: Efficient Online Capability Synergy for Two-Tower Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立塔让物品向量可预计算、用户向量可一次计算，适合近邻检索；深度用户—物品交互则通常依赖具体配对，难直接缓存。循环修正与知识协同尝试在可部署边界内增加联系，不能简单把全交叉模型原封不动当成 ANN 双塔。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>商品向量若每换用户都改变，就不能只存一份通用索引；双塔高效正来自这种解耦，增强交互时必须保留清晰的服务路径。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.19269">原论文</a> · <a href="../../../../reproductions/2604.19269-cs3/">实现解读</a> · <a href="#qa-2c2970df359ab633">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cs3" data-paper-title="CS3: Efficient Online Capability Synergy for Two-Tower Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="CS3: Efficient Online Capability Synergy for Two-Tower Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-04-21 传统双塔为 ANN 解耦 user/item 表征，牺牲交叉能力。CS3 通过离线/在线可部署的循环修正和知识协同增强塔间交互。 三 seed NDCG@10 相对 -16.06%，当前小数据未复现线上收益。Fidelity: 核心机制复现。实现双塔间的循环自修正、显式交叉同步与级联教师辅助目标。没有 4 亿 DAU 的在线缓存、EMA 跨塔向量和生产 QPS 链路。本地对照口径：基线是 matched two-tower；实验组加入 cycle、cross sync 与 teacher loss；三 seed NDCG@10 相对 -16.06%，当前小数据未复现线上收益。  retrieval two-tower online-learning 搜广推 候选生成与搜索匹配 CS3想增强双塔交互，为什么不能直接把候选向量写回所有共享用户表示？ 双塔高效检索依赖用户与物品表征可分别计算，一旦用户表示依赖具体候选，就不能直接用同一向量检索全库。CS3以可部署的循环修正和知识协同增强交互，需要明确哪些更新可离线物化、哪些仍随候选变化。不能把训练时可用的强交互路径直接当成免费ANN服务能力。 示意：给用户向量加入商品A的细节后，它可能更擅长评A，却不再是检索商品B、C的同一查询；修正必须有清楚的缓存和在线执行边界。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cs3" data-paper-title="CS3: Efficient Online Capability Synergy for Two-Tower Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="CS3: Efficient Online Capability Synergy for Two-Tower Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-04-21 传统双塔为 ANN 解耦 user/item 表征，牺牲交叉能力。CS3 通过离线/在线可部署的循环修正和知识协同增强塔间交互。 三 seed NDCG@10 相对 -16.06%，当前小数据未复现线上收益。Fidelity: 核心机制复现。实现双塔间的循环自修正、显式交叉同步与级联教师辅助目标。没有 4 亿 DAU 的在线缓存、EMA 跨塔向量和生产 QPS 链路。本地对照口径：基线是 matched two-tower；实验组加入 cycle、cross sync 与 teacher loss；三 seed NDCG@10 相对 -16.06%，当前小数据未复现线上收益。  retrieval two-tower online-learning 搜广推 候选生成与搜索匹配 CS3 的门控残差修正与用 cross-encoder 直接替代双塔，区别是什么？ 残差沿原双塔表示作受控更新，并结合协同损失保持部署接口；cross-encoder 通常对每对输入完整联合编码。两者计算依赖与索引条件不同，交互更强也可能更贵。来源本地 matched 对照为负，不能把设计目标写成已证实效果无损。 示意：先有可检索基础向量，再对候选做有限修正，像在初稿上补充；把每件商品与用户从头联合编码，则是另一种成本更高的评分过程。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-310a5a6284b81045">CS3 的门控残差修正与用 cross-encoder 直接替代双塔，区别是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acs3">CS3: Efficient Online Capability Synergy for Two-Tower Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>残差沿原双塔表示作受控更新，并结合协同损失保持部署接口；cross-encoder 通常对每对输入完整联合编码。两者计算依赖与索引条件不同，交互更强也可能更贵。来源本地 matched 对照为负，不能把设计目标写成已证实效果无损。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先有可检索基础向量，再对候选做有限修正，像在初稿上补充；把每件商品与用户从头联合编码，则是另一种成本更高的评分过程。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.19269">原论文</a> · <a href="../../../../reproductions/2604.19269-cs3/">实现解读</a> · <a href="#qa-310a5a6284b81045">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cs3" data-paper-title="CS3: Efficient Online Capability Synergy for Two-Tower Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="CS3: Efficient Online Capability Synergy for Two-Tower Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-04-21 传统双塔为 ANN 解耦 user/item 表征，牺牲交叉能力。CS3 通过离线/在线可部署的循环修正和知识协同增强塔间交互。 三 seed NDCG@10 相对 -16.06%，当前小数据未复现线上收益。Fidelity: 核心机制复现。实现双塔间的循环自修正、显式交叉同步与级联教师辅助目标。没有 4 亿 DAU 的在线缓存、EMA 跨塔向量和生产 QPS 链路。本地对照口径：基线是 matched two-tower；实验组加入 cycle、cross sync 与 teacher loss；三 seed NDCG@10 相对 -16.06%，当前小数据未复现线上收益。  retrieval two-tower online-learning 搜广推 候选生成与搜索匹配 CS3 实现循环修正时，如何区分可离线物品状态与在线候选相关状态？ 应跟踪每步更新是否读取当前用户或候选，读取之后的张量不能再冒充全局缓存。gate 与残差维度要一致，循环也需明确使用上一轮还是当前轮状态，防止原地更新改变算法。来源只支持其实际 cycle、cross-sync 和损失路径，不是任意相互写回。 示意：物品 i 经过用户甲修正后不能覆盖索引里的通用 i，再给用户乙读取；应另存配对状态，并保留原可缓存表示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a29682928ab8d584">CS3 实现循环修正时，如何区分可离线物品状态与在线候选相关状态？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acs3">CS3: Efficient Online Capability Synergy for Two-Tower Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>应跟踪每步更新是否读取当前用户或候选，读取之后的张量不能再冒充全局缓存。gate 与残差维度要一致，循环也需明确使用上一轮还是当前轮状态，防止原地更新改变算法。来源只支持其实际 cycle、cross-sync 和损失路径，不是任意相互写回。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>物品 i 经过用户甲修正后不能覆盖索引里的通用 i，再给用户乙读取；应另存配对状态，并保留原可缓存表示。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.19269">原论文</a> · <a href="../../../../reproductions/2604.19269-cs3/">实现解读</a> · <a href="#qa-a29682928ab8d584">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hill-index" data-paper-title="Efficient Retrieval Scaling with Hierarchical Indexing for Large Scale Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Efficient Retrieval Scaling with Hierarchical Indexing for Large Scale Recommendation 搜广推与 LLM 应用 Meta / Facebook and Instagram Ads 2026-04-14 大型 retrieval foundation model 若对全部 user-item pair 执行复杂 interaction tower，线上成本不可接受。HILL 不再独立地按 item embedding 建 ANN，而是让 MoNN 的用户、item 与交互信号参与 index-node 学习；第一层用 attention-style soft assignment，下一层量化上一层未解释的 residual。 Fidelity: 核心机制复现。本地执行 soft assignment、跨层 residual quantization、层级 beam retrieval 与固定公开切分评测；不是把离线 k-means 树直接命名为 HILL。本地没有 MoNN 的千级特征、多任务半监督训练、Meta Ads 十亿级索引、FAISS EM 和真实 QPS；中间节点数量只作为公开的 TTT-data proxy，未宣称完成线上 test-time training。  retrieval hierarchical-index residual-quantization test-time-training serving 搜广推 候选生成与搜索匹配 HILL 为什么让 user 和交互信号参与索引节点学习？ 普通 ANN 只组织 item 几何近邻，可能与复杂交互塔的相关性不一致。节点伪 item 与用户一起经模型评分，把检索决策需要的关系纳入索引，再按层缩小候选。索引不再只是静态聚类，训练、树结构与服务路径需共同维护。 示意：两个向量近的商品对不同用户价值不同，交互监督可让树按推荐需求组织，而不只按内容距离把它们放在一起。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-hill-index-46d50ccf" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b6cf5a4612015d03">HILL 为什么让 user 和交互信号参与索引节点学习？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahill-index">Efficient Retrieval Scaling with Hierarchical Indexing for Large Scale Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta / Facebook and Instagram Ads</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>普通 ANN 只组织 item 几何近邻，可能与复杂交互塔的相关性不一致。节点伪 item 与用户一起经模型评分，把检索决策需要的关系纳入索引，再按层缩小候选。索引不再只是静态聚类，训练、树结构与服务路径需共同维护。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个向量近的商品对不同用户价值不同，交互监督可让树按推荐需求组织，而不只按内容距离把它们放在一起。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.12965">原论文</a> · <a href="../../../../reproductions/2604.12965-hill-index/">实现解读</a> · <a href="#qa-b6cf5a4612015d03">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hill-index" data-paper-title="Efficient Retrieval Scaling with Hierarchical Indexing for Large Scale Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Efficient Retrieval Scaling with Hierarchical Indexing for Large Scale Recommendation 搜广推与 LLM 应用 Meta / Facebook and Instagram Ads 2026-04-14 大型 retrieval foundation model 若对全部 user-item pair 执行复杂 interaction tower，线上成本不可接受。HILL 不再独立地按 item embedding 建 ANN，而是让 MoNN 的用户、item 与交互信号参与 index-node 学习；第一层用 attention-style soft assignment，下一层量化上一层未解释的 residual。 Fidelity: 核心机制复现。本地执行 soft assignment、跨层 residual quantization、层级 beam retrieval 与固定公开切分评测；不是把离线 k-means 树直接命名为 HILL。本地没有 MoNN 的千级特征、多任务半监督训练、Meta Ads 十亿级索引、FAISS EM 和真实 QPS；中间节点数量只作为公开的 TTT-data proxy，未宣称完成线上 test-time training。  retrieval hierarchical-index residual-quantization test-time-training serving 搜广推 候选生成与搜索匹配 HILL为什么学习索引节点时也让用户与交互塔参与，而不只对item向量聚类？ 普通索引主要保持item几何近邻，未必与复杂交互模型的选择目标一致。HILL让节点作为可训练替代表示进入用户—物品交互，再用下一层残差补足上层未表达信息，使粗细索引共同服务检索。层级beam仍可能漏掉路径，少量test-time样本也不能用隔离测试答案来挑选或更新。 示意：两个商品内容向量很近，却被不同人群偏好；只按item距离可能分到同桶，交互驱动的节点学习可让索引更贴近实际用户选择，再逐层缩小候选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hill-index" data-paper-title="Efficient Retrieval Scaling with Hierarchical Indexing for Large Scale Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Efficient Retrieval Scaling with Hierarchical Indexing for Large Scale Recommendation 搜广推与 LLM 应用 Meta / Facebook and Instagram Ads 2026-04-14 大型 retrieval foundation model 若对全部 user-item pair 执行复杂 interaction tower，线上成本不可接受。HILL 不再独立地按 item embedding 建 ANN，而是让 MoNN 的用户、item 与交互信号参与 index-node 学习；第一层用 attention-style soft assignment，下一层量化上一层未解释的 residual。 Fidelity: 核心机制复现。本地执行 soft assignment、跨层 residual quantization、层级 beam retrieval 与固定公开切分评测；不是把离线 k-means 树直接命名为 HILL。本地没有 MoNN 的千级特征、多任务半监督训练、Meta Ads 十亿级索引、FAISS EM 和真实 QPS；中间节点数量只作为公开的 TTT-data proxy，未宣称完成线上 test-time training。  retrieval hierarchical-index residual-quantization test-time-training serving 搜广推 候选生成与搜索匹配 HILL 的残差子层与重复对原向量聚类，相比为何能提供互补层次？ 下一层量化前层未解释的残差，专注补充已有节点不足；反复聚原向量容易重复最强方向。互补只是设计目标，树搜索预算与路由误差仍会漏候选。来源本地压缩有效但质量负向，不能将候选比例下降直接当系统更好。 示意：首层已表达电子产品主题，残差再区分用途与价格；若每层都主要重学主题，增加树深却没有增加有用区分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5406f6bb678f4cbe">HILL 的残差子层与重复对原向量聚类，相比为何能提供互补层次？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahill-index">Efficient Retrieval Scaling with Hierarchical Indexing for Large Scale Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta / Facebook and Instagram Ads</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>下一层量化前层未解释的残差，专注补充已有节点不足；反复聚原向量容易重复最强方向。互补只是设计目标，树搜索预算与路由误差仍会漏候选。来源本地压缩有效但质量负向，不能将候选比例下降直接当系统更好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>首层已表达电子产品主题，残差再区分用途与价格；若每层都主要重学主题，增加树深却没有增加有用区分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.12965">原论文</a> · <a href="../../../../reproductions/2604.12965-hill-index/">实现解读</a> · <a href="#qa-5406f6bb678f4cbe">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hill-index" data-paper-title="Efficient Retrieval Scaling with Hierarchical Indexing for Large Scale Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Efficient Retrieval Scaling with Hierarchical Indexing for Large Scale Recommendation 搜广推与 LLM 应用 Meta / Facebook and Instagram Ads 2026-04-14 大型 retrieval foundation model 若对全部 user-item pair 执行复杂 interaction tower，线上成本不可接受。HILL 不再独立地按 item embedding 建 ANN，而是让 MoNN 的用户、item 与交互信号参与 index-node 学习；第一层用 attention-style soft assignment，下一层量化上一层未解释的 residual。 Fidelity: 核心机制复现。本地执行 soft assignment、跨层 residual quantization、层级 beam retrieval 与固定公开切分评测；不是把离线 k-means 树直接命名为 HILL。本地没有 MoNN 的千级特征、多任务半监督训练、Meta Ads 十亿级索引、FAISS EM 和真实 QPS；中间节点数量只作为公开的 TTT-data proxy，未宣称完成线上 test-time training。  retrieval hierarchical-index residual-quantization test-time-training serving 搜广推 候选生成与搜索匹配 HILL 的 soft assignment 与层级 beam，为什么需要分别验收？ 训练用连续分配构造伪 item 并传梯度，服务沿离散层级搜索有限分支，两条路径可能有差距。应检查归一、残差更新、父子映射与实际候选预算，不能用 soft 重构好证明 beam 覆盖好；小目录结构波动也需记录。 示意：目标商品在软分配中获若干节点少量质量，硬 beam 却可能一个都不保留；因此训练 loss 好看仍可能服务漏召。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-cbced8f5719b2196">HILL 的 soft assignment 与层级 beam，为什么需要分别验收？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahill-index">Efficient Retrieval Scaling with Hierarchical Indexing for Large Scale Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta / Facebook and Instagram Ads</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>训练用连续分配构造伪 item 并传梯度，服务沿离散层级搜索有限分支，两条路径可能有差距。应检查归一、残差更新、父子映射与实际候选预算，不能用 soft 重构好证明 beam 覆盖好；小目录结构波动也需记录。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>目标商品在软分配中获若干节点少量质量，硬 beam 却可能一个都不保留；因此训练 loss 好看仍可能服务漏召。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.12965">原论文</a> · <a href="../../../../reproductions/2604.12965-hill-index/">实现解读</a> · <a href="#qa-cbced8f5719b2196">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:genfacet" data-paper-title="GenFacet: End-to-End Generative Faceted Search via Multi-Task Preference Alignment in E-Commerce" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="GenFacet: End-to-End Generative Faceted Search via Multi-Task Preference Alignment in E-Commerce 搜广推与 LLM 应用 JD.com 2026-03-20 GenFacet 把电商分面搜索统一为上下文分面生成与意图驱动 query 改写两个生成任务，并以教师蒸馏加 GRPO 的多任务偏好对齐直接优化下游搜索满意度，闭合“分面选择—检索”链路。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05171，相对变化 -4.26%。本地代理目标与论文生产任务不同，不能外推线上 lift。  e-commerce-search facet-generation preference-alignment 搜广推 候选生成与搜索匹配 GenFacet 为什么把分面选择和 query 改写视为同一搜索链路？ 分面决定用户选择哪种细化方向，改写把该方向转成检索可用查询，二者共同影响最终结果。分开优化容易出现分面好看但搜不到、或改写偏离意图。联合反馈以检索满意度连接，但仍依赖目录与奖励可靠性。 示意：选“适合通勤”后，改写应落到轻便、防水等相关条件；若分面说通勤却改成专业越野，单独看两段文字都流畅也不构成正确链路。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-genfacet-00b00c8d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6e2cea1f051265fa">GenFacet 为什么把分面选择和 query 改写视为同一搜索链路？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agenfacet">GenFacet: End-to-End Generative Faceted Search via Multi-Task Preference Alignment in E-Commerce</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · JD.com</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分面决定用户选择哪种细化方向，改写把该方向转成检索可用查询，二者共同影响最终结果。分开优化容易出现分面好看但搜不到、或改写偏离意图。联合反馈以检索满意度连接，但仍依赖目录与奖励可靠性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>选“适合通勤”后，改写应落到轻便、防水等相关条件；若分面说通勤却改成专业越野，单独看两段文字都流畅也不构成正确链路。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.19665">原论文</a> · <a href="../../../../reproductions/2603.19665-genfacet/">实现解读</a> · <a href="#qa-6e2cea1f051265fa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:genfacet" data-paper-title="GenFacet: End-to-End Generative Faceted Search via Multi-Task Preference Alignment in E-Commerce" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="GenFacet: End-to-End Generative Faceted Search via Multi-Task Preference Alignment in E-Commerce 搜广推与 LLM 应用 JD.com 2026-03-20 GenFacet 把电商分面搜索统一为上下文分面生成与意图驱动 query 改写两个生成任务，并以教师蒸馏加 GRPO 的多任务偏好对齐直接优化下游搜索满意度，闭合“分面选择—检索”链路。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05171，相对变化 -4.26%。本地代理目标与论文生产任务不同，不能外推线上 lift。  e-commerce-search facet-generation preference-alignment 搜广推 候选生成与搜索匹配 GenFacet为什么把分面生成和query改写一起按下游检索反馈优化？ 分面文本看起来合理，不一定能带来可用搜索结果；选定分面后的改写也必须保持用户意图。多任务偏好对齐把这两步放进同一检索链路，用分面质量与实际结果共同约束策略，减少局部生成目标错位。反馈仍可能偏向热门分面，因此不能只用生成流畅度或单项命中率评价整体。 示意：用户搜轻便电脑，生成重量分面后应形成可检索的重量条件；若分面漂亮却改写成性能排名，局部文本都通顺，最终结果仍偏离需求。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:genfacet" data-paper-title="GenFacet: End-to-End Generative Faceted Search via Multi-Task Preference Alignment in E-Commerce" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="GenFacet: End-to-End Generative Faceted Search via Multi-Task Preference Alignment in E-Commerce 搜广推与 LLM 应用 JD.com 2026-03-20 GenFacet 把电商分面搜索统一为上下文分面生成与意图驱动 query 改写两个生成任务，并以教师蒸馏加 GRPO 的多任务偏好对齐直接优化下游搜索满意度，闭合“分面选择—检索”链路。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05171，相对变化 -4.26%。本地代理目标与论文生产任务不同，不能外推线上 lift。  e-commerce-search facet-generation preference-alignment 搜广推 候选生成与搜索匹配 GenFacet 的多任务偏好对齐与仅蒸馏教师分面文本，监督目标有什么区别？ 文本蒸馏主要复制教师表达，多任务奖励同时评价分面与改写后的检索结果，把行为价值带回生成器。它可纠正语言流畅却无效的选择，也可能为奖励牺牲未覆盖条件。来源公开代理负结果不能被原文生产目标描述代替。 示意：教师写出很漂亮的“精致生活”分面，目录却难检索；下游反馈可更支持具体的“可机洗”条件，但也需防止只迎合容易命中的词。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-3692d7096617bcd7">GenFacet 的多任务偏好对齐与仅蒸馏教师分面文本，监督目标有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agenfacet">GenFacet: End-to-End Generative Faceted Search via Multi-Task Preference Alignment in E-Commerce</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · JD.com</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文本蒸馏主要复制教师表达，多任务奖励同时评价分面与改写后的检索结果，把行为价值带回生成器。它可纠正语言流畅却无效的选择，也可能为奖励牺牲未覆盖条件。来源公开代理负结果不能被原文生产目标描述代替。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教师写出很漂亮的“精致生活”分面，目录却难检索；下游反馈可更支持具体的“可机洗”条件，但也需防止只迎合容易命中的词。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.19665">原论文</a> · <a href="../../../../reproductions/2603.19665-genfacet/">实现解读</a> · <a href="#qa-3692d7096617bcd7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:genfacet" data-paper-title="GenFacet: End-to-End Generative Faceted Search via Multi-Task Preference Alignment in E-Commerce" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="GenFacet: End-to-End Generative Faceted Search via Multi-Task Preference Alignment in E-Commerce 搜广推与 LLM 应用 JD.com 2026-03-20 GenFacet 把电商分面搜索统一为上下文分面生成与意图驱动 query 改写两个生成任务，并以教师蒸馏加 GRPO 的多任务偏好对齐直接优化下游搜索满意度，闭合“分面选择—检索”链路。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05171，相对变化 -4.26%。本地代理目标与论文生产任务不同，不能外推线上 lift。  e-commerce-search facet-generation preference-alignment 搜广推 候选生成与搜索匹配 GenFacet 实现两任务训练时，为什么必须保存分面到改写的对应关系？ 检索 reward 只能回到产生该查询的上下文与分面，错配会把另一个任务结果当信用。多任务权重、参考策略与有效输出 mask 也要明确。若只有确定性候选分数，没有实际生成和更新，不能称完成教师蒸馏加 GRPO 链路。 示意：防水分面生成的查询拿到好结果，应奖励这条对应动作；若回写给轻便分面，模型会学到错误关系，即使总 reward 没变。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1b7f66fb276b673f">GenFacet 实现两任务训练时，为什么必须保存分面到改写的对应关系？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agenfacet">GenFacet: End-to-End Generative Faceted Search via Multi-Task Preference Alignment in E-Commerce</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · JD.com</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>检索 reward 只能回到产生该查询的上下文与分面，错配会把另一个任务结果当信用。多任务权重、参考策略与有效输出 mask 也要明确。若只有确定性候选分数，没有实际生成和更新，不能称完成教师蒸馏加 GRPO 链路。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>防水分面生成的查询拿到好结果，应奖励这条对应动作；若回写给轻便分面，模型会学到错误关系，即使总 reward 没变。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.19665">原论文</a> · <a href="../../../../reproductions/2603.19665-genfacet/">实现解读</a> · <a href="#qa-1b7f66fb276b673f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hap" data-paper-title="Not All Candidates are Created Equal: Heterogeneity-Aware Pre-ranking" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Not All Candidates are Created Equal: Heterogeneity-Aware Pre-ranking 搜广推与 LLM 应用 ByteDance / Toutiao 2026-03-04 按候选难度把样本路由到轻量或强预排分支，再以跨分支 harmonization 约束不同计算预算下的排序尺度。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 hap 核心机制；相对 NDCG@10 +4.90%。  pre-ranking contrastive-learning dynamic-routing 搜广推 候选生成与搜索匹配 HAP 为什么按候选难度分配轻、强两种预排计算？ 大部分候选容易区分，全用强模型浪费预算；困难候选需要更多交互容量，路由让算力随需求分配。难度判断也有成本且会出错，误把关键候选送轻分支可能丢质量。动态预算不是简单按热门度给更多计算。 示意：明显不相关商品可由轻分支快速筛掉，两件高度相近且都符合条件的商品交给强分支细判，避免所有人都走同样重路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-hap-86607d9e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8556d538b0f73ee2">HAP 为什么按候选难度分配轻、强两种预排计算？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahap">Not All Candidates are Created Equal: Heterogeneity-Aware Pre-ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Toutiao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>大部分候选容易区分，全用强模型浪费预算；困难候选需要更多交互容量，路由让算力随需求分配。难度判断也有成本且会出错，误把关键候选送轻分支可能丢质量。动态预算不是简单按热门度给更多计算。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>明显不相关商品可由轻分支快速筛掉，两件高度相近且都符合条件的商品交给强分支细判，避免所有人都走同样重路径。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.03770">原论文</a> · <a href="../../../../reproductions/2603.03770-hap/">实现解读</a> · <a href="#qa-8556d538b0f73ee2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hap" data-paper-title="Not All Candidates are Created Equal: Heterogeneity-Aware Pre-ranking" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Not All Candidates are Created Equal: Heterogeneity-Aware Pre-ranking 搜广推与 LLM 应用 ByteDance / Toutiao 2026-03-04 按候选难度把样本路由到轻量或强预排分支，再以跨分支 harmonization 约束不同计算预算下的排序尺度。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 hap 核心机制；相对 NDCG@10 +4.90%。  pre-ranking contrastive-learning dynamic-routing 搜广推 候选生成与搜索匹配 HAP把困难候选送到强分支，为什么还要harmonization对齐分支分数？ 分支计算量不同，输出分布可能具有不同尺度；直接混排会把模型尺度误当物品价值。HAP先按候选难度分配轻重计算，再用跨分支协调约束，让有限预算下的结果仍能比较。路由错误也会把真正难例送入弱路径，因此不能只报告省下多少算力，而忽略统一排序质量。 示意：轻分支输出常在0.8附近，强分支输出常在0.4附近，二者直接比较会系统偏向前者；对齐尺度后，才能判断不同分支评分的候选谁应排前。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hap" data-paper-title="Not All Candidates are Created Equal: Heterogeneity-Aware Pre-ranking" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Not All Candidates are Created Equal: Heterogeneity-Aware Pre-ranking 搜广推与 LLM 应用 ByteDance / Toutiao 2026-03-04 按候选难度把样本路由到轻量或强预排分支，再以跨分支 harmonization 约束不同计算预算下的排序尺度。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 hap 核心机制；相对 NDCG@10 +4.90%。  pre-ranking contrastive-learning dynamic-routing 搜广推 候选生成与搜索匹配 HAP 的 harmonization 与单独校准强分支，相比要协调什么跨路径关系？ 最终候选来自不同分支，排序必须可跨分支比较，只让各自内部准确不足。harmonization 约束两种预算下尺度与偏好一致，避免路由身份成为优势。它可能限制专长表达，需检验质量—成本，不保证对齐后强分支毫无损失。 示意：轻分支普遍输出零点八、强分支零点四，不代表前者更好；若直接混排，简单候选可无端压过真正困难的高价值候选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-26201eaaf777f09a">HAP 的 harmonization 与单独校准强分支，相比要协调什么跨路径关系？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahap">Not All Candidates are Created Equal: Heterogeneity-Aware Pre-ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Toutiao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最终候选来自不同分支，排序必须可跨分支比较，只让各自内部准确不足。harmonization 约束两种预算下尺度与偏好一致，避免路由身份成为优势。它可能限制专长表达，需检验质量—成本，不保证对齐后强分支毫无损失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>轻分支普遍输出零点八、强分支零点四，不代表前者更好；若直接混排，简单候选可无端压过真正困难的高价值候选。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.03770">原论文</a> · <a href="../../../../reproductions/2603.03770-hap/">实现解读</a> · <a href="#qa-26201eaaf777f09a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hap" data-paper-title="Not All Candidates are Created Equal: Heterogeneity-Aware Pre-ranking" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Not All Candidates are Created Equal: Heterogeneity-Aware Pre-ranking 搜广推与 LLM 应用 ByteDance / Toutiao 2026-03-04 按候选难度把样本路由到轻量或强预排分支，再以跨分支 harmonization 约束不同计算预算下的排序尺度。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 hap 核心机制；相对 NDCG@10 +4.90%。  pre-ranking contrastive-learning dynamic-routing 搜广推 候选生成与搜索匹配 HAP 的 gate 与两路输出相乘时，为什么要区分软训练和实际执行预算？ 软融合可能同时算两分支，即使 gate 接近零或一也未必节省真实 FLOPs；服务若采用硬路由需明确阈值和回退。不能仅从公式宣称实际只算轻路径。本地代理排序结果也不包含完整生产延迟证据。 示意：程序先跑完轻强网络再按零一 gate 相加，数值是路由，计算却没省；要测服务成本应确认未选分支实际没有执行。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-db25c552897fed6f">HAP 的 gate 与两路输出相乘时，为什么要区分软训练和实际执行预算？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahap">Not All Candidates are Created Equal: Heterogeneity-Aware Pre-ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Toutiao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>软融合可能同时算两分支，即使 gate 接近零或一也未必节省真实 FLOPs；服务若采用硬路由需明确阈值和回退。不能仅从公式宣称实际只算轻路径。本地代理排序结果也不包含完整生产延迟证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>程序先跑完轻强网络再按零一 gate 相加，数值是路由，计算却没省；要测服务成本应确认未选分支实际没有执行。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.03770">原论文</a> · <a href="../../../../reproductions/2603.03770-hap/">实现解读</a> · <a href="#qa-db25c552897fed6f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mfli" data-paper-title="Rethinking ANN-based Retrieval: Multifaceted Learnable Index for Large-scale Recommendation System" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Rethinking ANN-based Retrieval: Multifaceted Learnable Index for Large-scale Recommendation System 搜广推与 LLM 应用 Meta 2026-02-18 ANN 把所有召回目标压进一个几何空间，离线建索引导致新内容滞后，在线近邻搜索又随候选规模变贵。MFLI 将 index 作为模型参数联合学习，并用多个 facet 表达语义、受欢迎度和时效性；请求侧直接分配各 facet 的检索预算。 Fidelity: 核心机制复现。本地构建并学习 genre、两层 semantic code、freshness 四个 facet，而非用单一 ANN 空间代替论文方法。全目录打分用于公平实验，不测 Meta 的十亿级实时索引、GPU QPS 或私有新鲜度标签。本地对照口径：基线为同切分的 single-space ANN proxy，实验组加入四 facet MFLI；NDCG@10 相对 -10.01%。  retrieval learnable-index fresh-content diversity serving 搜广推 候选生成与搜索匹配 MFLI 为什么把检索索引也纳入模型学习，而非只为既有向量建 ANN？ 独立 ANN 组织几何近邻，多个业务目标被压进单空间，更新也可能滞后。学习式多 facet 索引让语义、流行与时效有不同组织，并按请求分预算。它连接任务与索引，却仍需处理节点更新和覆盖，不能把参数化索引视为自动实时无成本。 示意：同一物品可在语义与新鲜度两套 facet 中有位置，请求决定更多查哪路，而不是一个距离同时承担所有目标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-mfli-7f2af977" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c0622b3380a540c5">MFLI 为什么把检索索引也纳入模型学习，而非只为既有向量建 ANN？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amfli">Rethinking ANN-based Retrieval: Multifaceted Learnable Index for Large-scale Recommendation System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立 ANN 组织几何近邻，多个业务目标被压进单空间，更新也可能滞后。学习式多 facet 索引让语义、流行与时效有不同组织，并按请求分预算。它连接任务与索引，却仍需处理节点更新和覆盖，不能把参数化索引视为自动实时无成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一物品可在语义与新鲜度两套 facet 中有位置，请求决定更多查哪路，而不是一个距离同时承担所有目标。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.16124">原论文</a> · <a href="../../../../reproductions/2602.16124-mfli/">实现解读</a> · <a href="#qa-c0622b3380a540c5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mfli" data-paper-title="Rethinking ANN-based Retrieval: Multifaceted Learnable Index for Large-scale Recommendation System" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Rethinking ANN-based Retrieval: Multifaceted Learnable Index for Large-scale Recommendation System 搜广推与 LLM 应用 Meta 2026-02-18 ANN 把所有召回目标压进一个几何空间，离线建索引导致新内容滞后，在线近邻搜索又随候选规模变贵。MFLI 将 index 作为模型参数联合学习，并用多个 facet 表达语义、受欢迎度和时效性；请求侧直接分配各 facet 的检索预算。 Fidelity: 核心机制复现。本地构建并学习 genre、两层 semantic code、freshness 四个 facet，而非用单一 ANN 空间代替论文方法。全目录打分用于公平实验，不测 Meta 的十亿级实时索引、GPU QPS 或私有新鲜度标签。本地对照口径：基线为同切分的 single-space ANN proxy，实验组加入四 facet MFLI；NDCG@10 相对 -10.01%。  retrieval learnable-index fresh-content diversity serving 搜广推 候选生成与搜索匹配 MFLI为什么把索引作为模型参数，并让请求按facet分配检索预算？ 一个几何空间难同时表达语义、热度和时效性，独立离线索引也可能落后于模型。多facet学习式索引为不同目标保留不同组织方式，请求再决定各路投入多少候选配额，避免统一搜索策略。可学习索引仍需维护新内容与路径一致性，不能只凭省去传统ANN就宣称质量与更新成本都更好。 示意：探索请求可多给新鲜内容facet预算，明确品类请求多给语义facet；如果所有请求固定平均分配，即使有多个索引，也未真正利用上下文需求。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mfli" data-paper-title="Rethinking ANN-based Retrieval: Multifaceted Learnable Index for Large-scale Recommendation System" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Rethinking ANN-based Retrieval: Multifaceted Learnable Index for Large-scale Recommendation System 搜广推与 LLM 应用 Meta 2026-02-18 ANN 把所有召回目标压进一个几何空间，离线建索引导致新内容滞后，在线近邻搜索又随候选规模变贵。MFLI 将 index 作为模型参数联合学习，并用多个 facet 表达语义、受欢迎度和时效性；请求侧直接分配各 facet 的检索预算。 Fidelity: 核心机制复现。本地构建并学习 genre、两层 semantic code、freshness 四个 facet，而非用单一 ANN 空间代替论文方法。全目录打分用于公平实验，不测 Meta 的十亿级实时索引、GPU QPS 或私有新鲜度标签。本地对照口径：基线为同切分的 single-space ANN proxy，实验组加入四 facet MFLI；NDCG@10 相对 -10.01%。  retrieval learnable-index fresh-content diversity serving 搜广推 候选生成与搜索匹配 MFLI 多 facet 与简单把多路召回结果拼接，相比预算分配有何区别？ 多 facet 在学习索引和请求权重上共同设计，a(q) 影响各目标的检索资源；简单拼接可能使用固定配额且目标空间独立。学习并不保证少热门，来源本地 head share 反而升，需检验实际候选分布，不能只相信 facet 名称。 示意：寻找新品时可增加时效 facet 预算，明确型号时多查语义；固定每路十个则对所有请求一样，也可能重复浪费在热门候选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-33f382dac78ac62b">MFLI 多 facet 与简单把多路召回结果拼接，相比预算分配有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amfli">Rethinking ANN-based Retrieval: Multifaceted Learnable Index for Large-scale Recommendation System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多 facet 在学习索引和请求权重上共同设计，a(q) 影响各目标的检索资源；简单拼接可能使用固定配额且目标空间独立。学习并不保证少热门，来源本地 head share 反而升，需检验实际候选分布，不能只相信 facet 名称。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>寻找新品时可增加时效 facet 预算，明确型号时多查语义；固定每路十个则对所有请求一样，也可能重复浪费在热门候选。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.16124">原论文</a> · <a href="../../../../reproductions/2602.16124-mfli/">实现解读</a> · <a href="#qa-33f382dac78ac62b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mfli" data-paper-title="Rethinking ANN-based Retrieval: Multifaceted Learnable Index for Large-scale Recommendation System" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Rethinking ANN-based Retrieval: Multifaceted Learnable Index for Large-scale Recommendation System 搜广推与 LLM 应用 Meta 2026-02-18 ANN 把所有召回目标压进一个几何空间，离线建索引导致新内容滞后，在线近邻搜索又随候选规模变贵。MFLI 将 index 作为模型参数联合学习，并用多个 facet 表达语义、受欢迎度和时效性；请求侧直接分配各 facet 的检索预算。 Fidelity: 核心机制复现。本地构建并学习 genre、两层 semantic code、freshness 四个 facet，而非用单一 ANN 空间代替论文方法。全目录打分用于公平实验，不测 Meta 的十亿级实时索引、GPU QPS 或私有新鲜度标签。本地对照口径：基线为同切分的 single-space ANN proxy，实验组加入四 facet MFLI；NDCG@10 相对 -10.01%。  retrieval learnable-index fresh-content diversity serving 搜广推 候选生成与搜索匹配 MFLI 的 facet 权重 softmax 与实际检索配额，为什么要分开核验？ 连续权重和为一只是学习输出，转成整数预算还涉及取整、总额与空分支处理，执行数量可能偏离预期。各 facet 的 code 身份也需正确映回 item，再去重。来源本地四 facet proxy 不能直接推出工业索引刷新与吞吐性能。 示意：预算十、权重三路各三分之一，简单四舍五入只得到九；需有明确余量分配，否则数学权重正确而实际召回预算并不守恒。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-305b55efe709b3f3">MFLI 的 facet 权重 softmax 与实际检索配额，为什么要分开核验？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amfli">Rethinking ANN-based Retrieval: Multifaceted Learnable Index for Large-scale Recommendation System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>连续权重和为一只是学习输出，转成整数预算还涉及取整、总额与空分支处理，执行数量可能偏离预期。各 facet 的 code 身份也需正确映回 item，再去重。来源本地四 facet proxy 不能直接推出工业索引刷新与吞吐性能。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>预算十、权重三路各三分之一，简单四舍五入只得到九；需有明确余量分配，否则数学权重正确而实际召回预算并不守恒。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.16124">原论文</a> · <a href="../../../../reproductions/2602.16124-mfli/">实现解读</a> · <a href="#qa-305b55efe709b3f3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:capts" data-paper-title="CAPTS: Channel-Aware, Preference-Aligned Trigger Selection for Multi-Channel Item-to-Item Retrieval" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="CAPTS: Channel-Aware, Preference-Aligned Trigger Selection for Multi-Channel Item-to-Item Retrieval 搜广推与 LLM 应用 Kuaishou Technology 2026-02-13 VAM 不只看触发物品本身的反馈，而把两跳召回物品的下游消费价值归因回 trigger；CATR 再联合决定 trigger 到各 I2I 通道的路由，减少通道重叠并提升互补覆盖。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05500，相对变化 +1.84%。本地代理目标与论文生产任务不同，不能外推线上 lift。  retrieval trigger-selection multi-channel-routing 搜广推 候选生成与搜索匹配 CAPTS 为什么把 trigger 的价值定义在两跳召回链路之后？ trigger 是召回其他内容的入口，其本身点击高不一定能带来有价值候选。VAM 将下游消费归回入口，评价它在当前 I2I 通道中能带出什么；CATR 再分配路由，让多个通道提供互补覆盖。入口价值依赖后端链路，不能脱离通道单独理解。 示意：用户看过一个热门视频，但它带出的候选很重复；另一条较冷历史能召回用户喜欢的新主题，后者可能是更好的 trigger。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-capts-e4a04e24" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a2ae5faa63b3569c">CAPTS 为什么把 trigger 的价值定义在两跳召回链路之后？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acapts">CAPTS: Channel-Aware, Preference-Aligned Trigger Selection for Multi-Channel Item-to-Item Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>trigger 是召回其他内容的入口，其本身点击高不一定能带来有价值候选。VAM 将下游消费归回入口，评价它在当前 I2I 通道中能带出什么；CATR 再分配路由，让多个通道提供互补覆盖。入口价值依赖后端链路，不能脱离通道单独理解。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户看过一个热门视频，但它带出的候选很重复；另一条较冷历史能召回用户喜欢的新主题，后者可能是更好的 trigger。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12564">原论文</a> · <a href="../../../../reproductions/2602.12564-capts/">实现解读</a> · <a href="#qa-a2ae5faa63b3569c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:capts" data-paper-title="CAPTS: Channel-Aware, Preference-Aligned Trigger Selection for Multi-Channel Item-to-Item Retrieval" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="CAPTS: Channel-Aware, Preference-Aligned Trigger Selection for Multi-Channel Item-to-Item Retrieval 搜广推与 LLM 应用 Kuaishou Technology 2026-02-13 VAM 不只看触发物品本身的反馈，而把两跳召回物品的下游消费价值归因回 trigger；CATR 再联合决定 trigger 到各 I2I 通道的路由，减少通道重叠并提升互补覆盖。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05500，相对变化 +1.84%。本地代理目标与论文生产任务不同，不能外推线上 lift。  retrieval trigger-selection multi-channel-routing 搜广推 候选生成与搜索匹配 CAPTS为什么用trigger召回出的内容消费价值评价trigger，而不只看trigger自身点击？ 触发物品是召回入口，其直接反馈未必反映后续能带来什么候选。VAM把两跳内容的下游消费归因回入口，再由CATR联合分配trigger与I2I通道，既考虑价值又惩罚重叠。单独挑最热门入口可能让多个通道召回相同内容，浪费有限候选配额。 示意：两个热门视频都导向同一批搞笑片，第三个较冷入口却能召回高价值科普；按下游价值和通道互补分配，可能比全选热门入口覆盖更好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:capts" data-paper-title="CAPTS: Channel-Aware, Preference-Aligned Trigger Selection for Multi-Channel Item-to-Item Retrieval" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="CAPTS: Channel-Aware, Preference-Aligned Trigger Selection for Multi-Channel Item-to-Item Retrieval 搜广推与 LLM 应用 Kuaishou Technology 2026-02-13 VAM 不只看触发物品本身的反馈，而把两跳召回物品的下游消费价值归因回 trigger；CATR 再联合决定 trigger 到各 I2I 通道的路由，减少通道重叠并提升互补覆盖。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05500，相对变化 +1.84%。本地代理目标与论文生产任务不同，不能外推线上 lift。  retrieval trigger-selection multi-channel-routing 搜广推 候选生成与搜索匹配 CAPTS 的联合通道路由与每个 I2I 通道独立选最强 trigger，有何区别？ 独立选择容易让各通道都围绕同一入口工作，局部最优叠加出高度重叠集合。联合目标同时考虑下游价值和重叠惩罚，让入口与通道之间分工。覆盖增加仍可能牺牲部分精度，来源只支持特定任务的测量，不能视为全通道无代价改进。 示意：三个通道都从同一部电影出发，返回同批热门续集；联合路由可让一个通道保留续集，另一个从导演兴趣入口探索不同内容。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-2d510fa145843a7c">CAPTS 的联合通道路由与每个 I2I 通道独立选最强 trigger，有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acapts">CAPTS: Channel-Aware, Preference-Aligned Trigger Selection for Multi-Channel Item-to-Item Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立选择容易让各通道都围绕同一入口工作，局部最优叠加出高度重叠集合。联合目标同时考虑下游价值和重叠惩罚，让入口与通道之间分工。覆盖增加仍可能牺牲部分精度，来源只支持特定任务的测量，不能视为全通道无代价改进。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三个通道都从同一部电影出发，返回同批热门续集；联合路由可让一个通道保留续集，另一个从导演兴趣入口探索不同内容。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12564">原论文</a> · <a href="../../../../reproductions/2602.12564-capts/">实现解读</a> · <a href="#qa-2d510fa145843a7c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:capts" data-paper-title="CAPTS: Channel-Aware, Preference-Aligned Trigger Selection for Multi-Channel Item-to-Item Retrieval" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="CAPTS: Channel-Aware, Preference-Aligned Trigger Selection for Multi-Channel Item-to-Item Retrieval 搜广推与 LLM 应用 Kuaishou Technology 2026-02-13 VAM 不只看触发物品本身的反馈，而把两跳召回物品的下游消费价值归因回 trigger；CATR 再联合决定 trigger 到各 I2I 通道的路由，减少通道重叠并提升互补覆盖。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05500，相对变化 +1.84%。本地代理目标与论文生产任务不同，不能外推线上 lift。  retrieval trigger-selection multi-channel-routing 搜广推 候选生成与搜索匹配 CAPTS 的价值汇总为什么需要保留 trigger、通道与下游物品三层索引？ 同一 trigger 在不同通道会产生不同候选及贡献，权重与反馈必须回到正确路径，再在联合选择时计算通道重叠。若先把所有结果压成一个全局物品分数，就丢掉入口信用。公开代理的消费标签与真实生产价值也应明确区分。 示意：候选甲由两个 trigger 召回，不能把同一次消费不加区分地各算全额收益；保留路径与权重，才知道哪个入口真正补充了候选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-2f638ca3d8dc3d29">CAPTS 的价值汇总为什么需要保留 trigger、通道与下游物品三层索引？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acapts">CAPTS: Channel-Aware, Preference-Aligned Trigger Selection for Multi-Channel Item-to-Item Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一 trigger 在不同通道会产生不同候选及贡献，权重与反馈必须回到正确路径，再在联合选择时计算通道重叠。若先把所有结果压成一个全局物品分数，就丢掉入口信用。公开代理的消费标签与真实生产价值也应明确区分。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>候选甲由两个 trigger 召回，不能把同一次消费不加区分地各算全额收益；保留路径与权重，才知道哪个入口真正补充了候选。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12564">原论文</a> · <a href="../../../../reproductions/2602.12564-capts/">实现解读</a> · <a href="#qa-2f638ca3d8dc3d29">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:airbnb-ebr" data-paper-title="Applying Embedding-Based Retrieval to Airbnb Search" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Applying Embedding-Based Retrieval to Airbnb Search 搜广推与 LLM 应用 Airbnb 2026-01-11 按搜索—浏览—预订的多阶段旅程构造正例和 hard negatives，以流量 replay 对齐第一阶段召回口径；线上结合 HNSW/IVF、地理过滤与高频库存更新。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04943，相对变化 -8.48%。本地代理目标与论文生产任务不同，不能外推线上 lift。  search-retrieval embedding-retrieval hard-negative-mining 搜广推 候选生成与搜索匹配 Airbnb EBR 为什么同时需要查询塔、房源塔与地理库存过滤？ 双塔把请求与房源映到可检索空间，点积负责相关性，但相似房源可能不在目的地、不可入住或库存已变。索引提供快速候选，地理与库存约束保证候选在当前请求可服务；这两类条件不能仅靠语义模型记住。 示意：模型判断一套海边公寓很符合用户，但它在另一座城市且日期已满。相关性高不代表可订，过滤仍应在当前库存口径下执行。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-airbnb-ebr-a90e62e0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f7de56d9be73fcab">Airbnb EBR 为什么同时需要查询塔、房源塔与地理库存过滤？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aairbnb-ebr">Applying Embedding-Based Retrieval to Airbnb Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Airbnb</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>双塔把请求与房源映到可检索空间，点积负责相关性，但相似房源可能不在目的地、不可入住或库存已变。索引提供快速候选，地理与库存约束保证候选在当前请求可服务；这两类条件不能仅靠语义模型记住。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型判断一套海边公寓很符合用户，但它在另一座城市且日期已满。相关性高不代表可订，过滤仍应在当前库存口径下执行。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.06873">原论文</a> · <a href="../../../../reproductions/2601.06873-airbnb-ebr/">实现解读</a> · <a href="#qa-f7de56d9be73fcab">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:airbnb-ebr" data-paper-title="Applying Embedding-Based Retrieval to Airbnb Search" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Applying Embedding-Based Retrieval to Airbnb Search 搜广推与 LLM 应用 Airbnb 2026-01-11 按搜索—浏览—预订的多阶段旅程构造正例和 hard negatives，以流量 replay 对齐第一阶段召回口径；线上结合 HNSW/IVF、地理过滤与高频库存更新。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04943，相对变化 -8.48%。本地代理目标与论文生产任务不同，不能外推线上 lift。  search-retrieval embedding-retrieval hard-negative-mining 搜广推 候选生成与搜索匹配 Airbnb EBR为什么要沿搜索—浏览—预订旅程构造难负例，而不只用随机房源？ 随机房源往往地域或条件明显不符，模型容易只学到粗差别。旅程内浏览过但未预订的房源提供更接近实际选择边界的对照，训练因此更贴合第一阶段召回；服务时还需结合地理、库存和索引更新。未预订不必然是不喜欢，所以难负例与采样口径必须一起解释。 示意：巴黎行程中用东京房源作负例太容易；同区域、相近价格但未预订的房源更能检验细粒度需求，同时要避免把已订满当作不相关。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:airbnb-ebr" data-paper-title="Applying Embedding-Based Retrieval to Airbnb Search" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Applying Embedding-Based Retrieval to Airbnb Search 搜广推与 LLM 应用 Airbnb 2026-01-11 按搜索—浏览—预订的多阶段旅程构造正例和 hard negatives，以流量 replay 对齐第一阶段召回口径；线上结合 HNSW/IVF、地理过滤与高频库存更新。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04943，相对变化 -8.48%。本地代理目标与论文生产任务不同，不能外推线上 lift。  search-retrieval embedding-retrieval hard-negative-mining 搜广推 候选生成与搜索匹配 Airbnb EBR 的流量 replay 与只在静态负例集上评估，有何候选分布差别？ 静态负例可能过易或不反映第一阶段真实候选，离线高命中便未必迁移。replay 按真实请求与旅程重放候选和过滤口径，更接近召回器实际面对的决策范围；它仍不能替代真实线上用户反应，尤其库存与行为会继续变化。 示意：在随机全国房源中找对纽约房源很容易，但纽约同日期可订房源之间才是真实竞争。按请求重放能暴露后者的检索难度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-03cce997a8ff19b3">Airbnb EBR 的流量 replay 与只在静态负例集上评估，有何候选分布差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aairbnb-ebr">Applying Embedding-Based Retrieval to Airbnb Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Airbnb</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>静态负例可能过易或不反映第一阶段真实候选，离线高命中便未必迁移。replay 按真实请求与旅程重放候选和过滤口径，更接近召回器实际面对的决策范围；它仍不能替代真实线上用户反应，尤其库存与行为会继续变化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>在随机全国房源中找对纽约房源很容易，但纽约同日期可订房源之间才是真实竞争。按请求重放能暴露后者的检索难度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.06873">原论文</a> · <a href="../../../../reproductions/2601.06873-airbnb-ebr/">实现解读</a> · <a href="#qa-03cce997a8ff19b3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:airbnb-ebr" data-paper-title="Applying Embedding-Based Retrieval to Airbnb Search" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Applying Embedding-Based Retrieval to Airbnb Search 搜广推与 LLM 应用 Airbnb 2026-01-11 按搜索—浏览—预订的多阶段旅程构造正例和 hard negatives，以流量 replay 对齐第一阶段召回口径；线上结合 HNSW/IVF、地理过滤与高频库存更新。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04943，相对变化 -8.48%。本地代理目标与论文生产任务不同，不能外推线上 lift。  search-retrieval embedding-retrieval hard-negative-mining 搜广推 候选生成与搜索匹配 Airbnb EBR 的对比损失中，难负例和合法候选应如何与目标匹配？ 同一查询的正房源与旅程中未选的合理房源共同进入分母，使训练学会细粒度区分；目标房源必须来自该请求的正旅程，不能把别人的预订错配进来。服务索引与过滤需使用一致特征版本，本地电影代理不包含真实地理库存。 示意：用户看过三套同区公寓最后预订一套，另外两套可构成难负例；另一城市不可订房源即使容易区分，也不能代替全部真实竞争候选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b7ceaa141a992d9f">Airbnb EBR 的对比损失中，难负例和合法候选应如何与目标匹配？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aairbnb-ebr">Applying Embedding-Based Retrieval to Airbnb Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Airbnb</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一查询的正房源与旅程中未选的合理房源共同进入分母，使训练学会细粒度区分；目标房源必须来自该请求的正旅程，不能把别人的预订错配进来。服务索引与过滤需使用一致特征版本，本地电影代理不包含真实地理库存。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户看过三套同区公寓最后预订一套，另外两套可构成难负例；另一城市不可订房源即使容易区分，也不能代替全部真实竞争候选。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.06873">原论文</a> · <a href="../../../../reproductions/2601.06873-airbnb-ebr/">实现解读</a> · <a href="#qa-b7ceaa141a992d9f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:crsd" data-paper-title="From Reasoning LLMs to BERT: A Two-Stage Distillation Framework for Search Relevance" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="From Reasoning LLMs to BERT: A Two-Stage Distillation Framework for Search Relevance 搜广推与 LLM 应用 Meituan 2025-10-13 先以 CPT、SFT 和多维偏好优化构建领域 reasoning LLM，再让同一轻量学生的普通输入与 reasoning-augmented 输入做对比式自蒸馏，线上无需推理链。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上执行论文的候选相关检索、层级压缩或蒸馏目标；未使用公司私有日志与线上 serving，线上 A/B 只引用原文。本地相对变化不得与原文指标混写。本地对照口径：基线为 shared transition + content baseline，实验组为 CRSD，只改变论文核心机制；ndcg_at_10 0.0354 → 0.0346，相对基线 -2.14%。  search content-understanding llm-distillation 搜广推 候选生成与搜索匹配 CRSD 为什么让 reasoning 作为训练期增强视图，而不是永久服务依赖？ 推理文本能提供更丰富监督，但实时生成成本高。学生同时面对普通输入与带推理输入，自蒸馏将增强视图的分布知识迁到普通路径；线上只用后者。推理的价值通过训练留下，不能保证学生保存了完整推理过程或解释忠实性。 示意：训练时用“用户要轻便通勤”解释辅助判断商品，服务只输入当前特征快速打分；无需每次先写一段长理由再选候选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-crsd-bbd3991b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-94dea0d87b1d446e">CRSD 为什么让 reasoning 作为训练期增强视图，而不是永久服务依赖？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acrsd">From Reasoning LLMs to BERT: A Two-Stage Distillation Framework for Search Relevance</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>推理文本能提供更丰富监督，但实时生成成本高。学生同时面对普通输入与带推理输入，自蒸馏将增强视图的分布知识迁到普通路径；线上只用后者。推理的价值通过训练留下，不能保证学生保存了完整推理过程或解释忠实性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练时用“用户要轻便通勤”解释辅助判断商品，服务只输入当前特征快速打分；无需每次先写一段长理由再选候选。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.11056">原论文</a> · <a href="../../../../reproductions/2510.11056-crsd/">实现解读</a> · <a href="#qa-94dea0d87b1d446e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:crsd" data-paper-title="From Reasoning LLMs to BERT: A Two-Stage Distillation Framework for Search Relevance" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="From Reasoning LLMs to BERT: A Two-Stage Distillation Framework for Search Relevance 搜广推与 LLM 应用 Meituan 2025-10-13 先以 CPT、SFT 和多维偏好优化构建领域 reasoning LLM，再让同一轻量学生的普通输入与 reasoning-augmented 输入做对比式自蒸馏，线上无需推理链。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上执行论文的候选相关检索、层级压缩或蒸馏目标；未使用公司私有日志与线上 serving，线上 A/B 只引用原文。本地相对变化不得与原文指标混写。本地对照口径：基线为 shared transition + content baseline，实验组为 CRSD，只改变论文核心机制；ndcg_at_10 0.0354 → 0.0346，相对基线 -2.14%。  search content-understanding llm-distillation 搜广推 候选生成与搜索匹配 CRSD为何让同一学生比较有reasoning和无reasoning的输入，而不是上线时始终携带推理链？ reasoning视图提供更丰富的关系线索，普通视图对应实际低延迟服务输入。自蒸馏与对比目标把丰富视图的判断压入学生，使其不依赖每次生成推理文本；标签监督继续约束任务正确性。若教师理由含答案泄漏或两种视图在服务时分布不一致，蒸馏损失下降也未必意味着有效迁移。 示意：训练时给商品相关性学生看一段属性比较理由，再要求无理由输入也作出相近判断；上线只给查询和商品，不必为每个候选额外生成一段解释。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:crsd" data-paper-title="From Reasoning LLMs to BERT: A Two-Stage Distillation Framework for Search Relevance" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="From Reasoning LLMs to BERT: A Two-Stage Distillation Framework for Search Relevance 搜广推与 LLM 应用 Meituan 2025-10-13 先以 CPT、SFT 和多维偏好优化构建领域 reasoning LLM，再让同一轻量学生的普通输入与 reasoning-augmented 输入做对比式自蒸馏，线上无需推理链。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上执行论文的候选相关检索、层级压缩或蒸馏目标；未使用公司私有日志与线上 serving，线上 A/B 只引用原文。本地相对变化不得与原文指标混写。本地对照口径：基线为 shared transition + content baseline，实验组为 CRSD，只改变论文核心机制；ndcg_at_10 0.0354 → 0.0346，相对基线 -2.14%。  search content-understanding llm-distillation 搜广推 候选生成与搜索匹配 CRSD 的对比式自蒸馏与单纯从外部 teacher 拟合 logits，有什么学生共享关系？ 这里同一轻量学生在两种输入视图下形成分布，对比目标还约束表示关系，减少单靠外部教师尺度不匹配的影响。共享不等于没有教师噪声，推理增强数据仍可能错误。两视图的梯度与停止路径需按实现核验，不能只称“自蒸馏”便推断无偏。 示意：同一小模型读普通商品信息和附加理由各算一次，学习两者保持一致；这不同于另一个大模型直接给固定分数，后者没有共享学生参数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-16dedeae125cf8d6">CRSD 的对比式自蒸馏与单纯从外部 teacher 拟合 logits，有什么学生共享关系？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acrsd">From Reasoning LLMs to BERT: A Two-Stage Distillation Framework for Search Relevance</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这里同一轻量学生在两种输入视图下形成分布，对比目标还约束表示关系，减少单靠外部教师尺度不匹配的影响。共享不等于没有教师噪声，推理增强数据仍可能错误。两视图的梯度与停止路径需按实现核验，不能只称“自蒸馏”便推断无偏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一小模型读普通商品信息和附加理由各算一次，学习两者保持一致；这不同于另一个大模型直接给固定分数，后者没有共享学生参数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.11056">原论文</a> · <a href="../../../../reproductions/2510.11056-crsd/">实现解读</a> · <a href="#qa-16dedeae125cf8d6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:crsd" data-paper-title="From Reasoning LLMs to BERT: A Two-Stage Distillation Framework for Search Relevance" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="From Reasoning LLMs to BERT: A Two-Stage Distillation Framework for Search Relevance 搜广推与 LLM 应用 Meituan 2025-10-13 先以 CPT、SFT 和多维偏好优化构建领域 reasoning LLM，再让同一轻量学生的普通输入与 reasoning-augmented 输入做对比式自蒸馏，线上无需推理链。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上执行论文的候选相关检索、层级压缩或蒸馏目标；未使用公司私有日志与线上 serving，线上 A/B 只引用原文。本地相对变化不得与原文指标混写。本地对照口径：基线为 shared transition + content baseline，实验组为 CRSD，只改变论文核心机制；ndcg_at_10 0.0354 → 0.0346，相对基线 -2.14%。  search content-understanding llm-distillation 搜广推 候选生成与搜索匹配 CRSD 上线时若仍把 reasoning r 拼进输入，为什么偏离了蒸馏目标？ 来源让普通路径 pS(·|x) 学习增强路径 pS(·|x,r)，目标正是移除在线推理依赖。服务再要求 r 会恢复额外成本，也无法说明普通路径已学会。验收需分别检查训练增强损失与无理由推理输出，本地代理结果不能证明完整领域 LLM 训练。 示意：把测试样本先送大模型生成理由，再给学生评分，测到的是增强链路；只给原始 x 的结果才对应预期的轻量服务路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6c70d8635c52695c">CRSD 上线时若仍把 reasoning r 拼进输入，为什么偏离了蒸馏目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acrsd">From Reasoning LLMs to BERT: A Two-Stage Distillation Framework for Search Relevance</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>来源让普通路径 pS(·|x) 学习增强路径 pS(·|x,r)，目标正是移除在线推理依赖。服务再要求 r 会恢复额外成本，也无法说明普通路径已学会。验收需分别检查训练增强损失与无理由推理输出，本地代理结果不能证明完整领域 LLM 训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把测试样本先送大模型生成理由，再给学生评分，测到的是增强链路；只给原始 x 的结果才对应预期的轻量服务路径。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.11056">原论文</a> · <a href="../../../../reproductions/2510.11056-crsd/">实现解读</a> · <a href="#qa-6c70d8635c52695c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mpformer" data-paper-title="MPFormer: Adaptive Framework for Industrial Multi-Task Personalized Sequential Retriever" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="MPFormer: Adaptive Framework for Industrial Multi-Task Personalized Sequential Retriever 搜广推与 LLM 应用 Kuaishou Technology 2025-08-28 以 objective token 驱动同一序列检索器完成多种行为目标，并按任务难度动态分配容量和候选配额。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 mpformer 核心机制；相对 NDCG@10 -7.15%。  retrieval multi-task sequence serving 搜广推 候选生成与搜索匹配 MPFormer 为什么用 objective token 区分召回目标？ 不同反馈需要同一历史的不同切面，objective token 在编码时声明当前任务，使主干共享而输出有条件差异。任务难度进一步影响容量和候选预算。token 只是接口，不能把任务名称与真实标签含义混同，缺少监督时也无法凭空学会目标。 示意：同一用户点击喜欢新鲜、购买偏可靠，两种 objective 可形成不同表示；若训练只有观看标签，就不能仅换 token 宣称学会购买。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-mpformer-268b1045" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-3da58df8da20b61e">MPFormer 为什么用 objective token 区分召回目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ampformer">MPFormer: Adaptive Framework for Industrial Multi-Task Personalized Sequential Retriever</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同反馈需要同一历史的不同切面，objective token 在编码时声明当前任务，使主干共享而输出有条件差异。任务难度进一步影响容量和候选预算。token 只是接口，不能把任务名称与真实标签含义混同，缺少监督时也无法凭空学会目标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一用户点击喜欢新鲜、购买偏可靠，两种 objective 可形成不同表示；若训练只有观看标签，就不能仅换 token 宣称学会购买。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.20400">原论文</a> · <a href="../../../../reproductions/2508.20400-mpformer/">实现解读</a> · <a href="#qa-3da58df8da20b61e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mpformer" data-paper-title="MPFormer: Adaptive Framework for Industrial Multi-Task Personalized Sequential Retriever" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="MPFormer: Adaptive Framework for Industrial Multi-Task Personalized Sequential Retriever 搜广推与 LLM 应用 Kuaishou Technology 2025-08-28 以 objective token 驱动同一序列检索器完成多种行为目标，并按任务难度动态分配容量和候选配额。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 mpformer 核心机制；相对 NDCG@10 -7.15%。  retrieval multi-task sequence serving 搜广推 候选生成与搜索匹配 MPFormer 的 objective token 如何让同一段历史产生面向不同目标的召回表示？ 目标 token 与历史一起进入序列模型，为编码过程提供当前任务条件，所以同一用户可以形成面向不同行为目标的表示。动态权重和候选配额再根据任务难度调整训练与检索资源。它共享主干却保留目标差异，代价是各目标的权重和配额需要校准，不能把多个目标当作完全相同的下一物品预测。 示意：同一段浏览历史，点击目标更关注新奇内容，购买目标更关注近期反复比较的商品。切换目标 token 后，模型可以从同一历史中提取不同信号并分配候选数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mpformer" data-paper-title="MPFormer: Adaptive Framework for Industrial Multi-Task Personalized Sequential Retriever" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="MPFormer: Adaptive Framework for Industrial Multi-Task Personalized Sequential Retriever 搜广推与 LLM 应用 Kuaishou Technology 2025-08-28 以 objective token 驱动同一序列检索器完成多种行为目标，并按任务难度动态分配容量和候选配额。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 mpformer 核心机制；相对 NDCG@10 -7.15%。  retrieval multi-task sequence serving 搜广推 候选生成与搜索匹配 MPFormer 动态配额与每任务固定 K，相比服务预算怎样变化？ 固定 K 对所有任务投入相同候选数，动态配额依难度或上下文分资源，可能让困难任务有更多覆盖，也可能挤占其他目标。权重归一不自动保证实际整数预算守恒。来源公开代理不能证明工业多行为目标均受益。 示意：点击目标候选易找可少分一点，稀疏购买多给检索机会；若任务难度估错，额外预算也可能浪费而非带来价值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-3e14785dbbaeabdb">MPFormer 动态配额与每任务固定 K，相比服务预算怎样变化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ampformer">MPFormer: Adaptive Framework for Industrial Multi-Task Personalized Sequential Retriever</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定 K 对所有任务投入相同候选数，动态配额依难度或上下文分资源，可能让困难任务有更多覆盖，也可能挤占其他目标。权重归一不自动保证实际整数预算守恒。来源公开代理不能证明工业多行为目标均受益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>点击目标候选易找可少分一点，稀疏购买多给检索机会；若任务难度估错，额外预算也可能浪费而非带来价值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.20400">原论文</a> · <a href="../../../../reproductions/2508.20400-mpformer/">实现解读</a> · <a href="#qa-3e14785dbbaeabdb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mpformer" data-paper-title="MPFormer: Adaptive Framework for Industrial Multi-Task Personalized Sequential Retriever" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="MPFormer: Adaptive Framework for Industrial Multi-Task Personalized Sequential Retriever 搜广推与 LLM 应用 Kuaishou Technology 2025-08-28 以 objective token 驱动同一序列检索器完成多种行为目标，并按任务难度动态分配容量和候选配额。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 mpformer 核心机制；相对 NDCG@10 -7.15%。  retrieval multi-task sequence serving 搜广推 候选生成与搜索匹配 MPFormer 的 qm(h) 在训练加权与候选配额中，为什么要记录具体使用方式？ 连续训练权重和推理候选数是不同对象，前者归一后乘 loss，后者需转换成合法整数并满足总预算。任务空标签应 mask，不能用默认零伪造监督。仅在分数上混合几路代理不等于 objective-conditioned 共享模型实际训练。 示意：训练权重零点三不自动对应三十个候选；总预算十时还要定义取整与余量，否则任务集合变多就可能超支。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-fab82113a426caac">MPFormer 的 qm(h) 在训练加权与候选配额中，为什么要记录具体使用方式？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ampformer">MPFormer: Adaptive Framework for Industrial Multi-Task Personalized Sequential Retriever</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>连续训练权重和推理候选数是不同对象，前者归一后乘 loss，后者需转换成合法整数并满足总预算。任务空标签应 mask，不能用默认零伪造监督。仅在分数上混合几路代理不等于 objective-conditioned 共享模型实际训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练权重零点三不自动对应三十个候选；总预算十时还要定义取整与余量，否则任务集合变多就可能超支。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.20400">原论文</a> · <a href="../../../../reproductions/2508.20400-mpformer/">实现解读</a> · <a href="#qa-fab82113a426caac">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:beque" data-paper-title="Large Language Model based Long-tail Query Rewriting in Taobao Search" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Large Language Model based Long-tail Query Rewriting in Taobao Search 搜广推与 LLM 应用 Alibaba 2023-11-07 长尾电商 query 存在语义缺口，单纯 SFT 只模仿人工 rewrite，未直接对齐召回质量。BEQUE 先用拒绝采样和多指令数据 SFT，再让模型为每个 query 自采样多个 rewrite；淘宝离线搜索系统从 relevance、retrieval increment、hit rate 打分并形成偏序，最后用 Preference Ranking Optimization（PRO）把排序反馈对齐回 LLM。生产 serving 采用离线刷库 + 在线 KV，不把 7B 自回归模型放进请求链路。 Fidelity: 完整核心链路复现。真实执行 seq2seq SFT、beam self-sampling、离线检索反馈、partial order 构造和 rank-aware PRO；Qwen-7B/淘宝搜索替换为 T5-small/MovieLens 公开目录。本地对照口径：基线是 T5 SFT；实验组是同一模型继续做 PRO；主组合反馈从 0.62102 升至 0.80750（+30.03%），但 increment -66.02%。这是对齐阶段消融；DIN 不适用于 query rewriting 任务。  llm-recommendation query-rewriting preference-optimization search 搜广推 候选生成与搜索匹配 BEQUE 的 query rewrite 为什么不能只按与人工改写文字相似来评价？ 不同表达可能召回不同商品集合，文字接近不保证相关性、覆盖和命中都好。BEQUE 用真实搜索系统对模型自采样改写评分，再把偏序反馈训练回生成器，使目标连接检索行为。搜索反馈也只是所选组合目标，不代表所有子指标必然同时改善。 示意：把“露营防潮”改成更流畅的“户外生活”可能更像通用文案，却丢掉防潮垫检索；应看实际召回，而不只比较词面是否漂亮。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-beque-26cd2487" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-3063f4740daf0113">BEQUE 的 query rewrite 为什么不能只按与人工改写文字相似来评价？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Abeque">Large Language Model based Long-tail Query Rewriting in Taobao Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同表达可能召回不同商品集合，文字接近不保证相关性、覆盖和命中都好。BEQUE 用真实搜索系统对模型自采样改写评分，再把偏序反馈训练回生成器，使目标连接检索行为。搜索反馈也只是所选组合目标，不代表所有子指标必然同时改善。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把“露营防潮”改成更流畅的“户外生活”可能更像通用文案，却丢掉防潮垫检索；应看实际召回，而不只比较词面是否漂亮。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2311.03758">原论文</a> · <a href="../../../../reproductions/2311.03758-beque/">实现解读</a> · <a href="#qa-3063f4740daf0113">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:beque" data-paper-title="Large Language Model based Long-tail Query Rewriting in Taobao Search" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Large Language Model based Long-tail Query Rewriting in Taobao Search 搜广推与 LLM 应用 Alibaba 2023-11-07 长尾电商 query 存在语义缺口，单纯 SFT 只模仿人工 rewrite，未直接对齐召回质量。BEQUE 先用拒绝采样和多指令数据 SFT，再让模型为每个 query 自采样多个 rewrite；淘宝离线搜索系统从 relevance、retrieval increment、hit rate 打分并形成偏序，最后用 Preference Ranking Optimization（PRO）把排序反馈对齐回 LLM。生产 serving 采用离线刷库 + 在线 KV，不把 7B 自回归模型放进请求链路。 Fidelity: 完整核心链路复现。真实执行 seq2seq SFT、beam self-sampling、离线检索反馈、partial order 构造和 rank-aware PRO；Qwen-7B/淘宝搜索替换为 T5-small/MovieLens 公开目录。本地对照口径：基线是 T5 SFT；实验组是同一模型继续做 PRO；主组合反馈从 0.62102 升至 0.80750（+30.03%），但 increment -66.02%。这是对齐阶段消融；DIN 不适用于 query rewriting 任务。  llm-recommendation query-rewriting preference-optimization search 搜广推 候选生成与搜索匹配 BEQUE完成SFT后为什么还要对多个自采样rewrite做PRO？ SFT学习示范怎么改写，却未必优化改写后的检索结果。BEQUE让同一查询生成多个候选，由离线搜索反馈形成偏序，再用长度归一化序列分数学习更好的相对选择。反馈同时含相关性与新增召回等目标，因此组合分上涨仍可能牺牲某一子项，不能把流畅改写当检索成功。 示意：两种改写都很通顺，一种只召回原有热门商品，另一种补到相关长尾；搜索反馈可提供文字示范里没有的区别，但需同时看新增覆盖是否退化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:beque" data-paper-title="Large Language Model based Long-tail Query Rewriting in Taobao Search" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Large Language Model based Long-tail Query Rewriting in Taobao Search 搜广推与 LLM 应用 Alibaba 2023-11-07 长尾电商 query 存在语义缺口，单纯 SFT 只模仿人工 rewrite，未直接对齐召回质量。BEQUE 先用拒绝采样和多指令数据 SFT，再让模型为每个 query 自采样多个 rewrite；淘宝离线搜索系统从 relevance、retrieval increment、hit rate 打分并形成偏序，最后用 Preference Ranking Optimization（PRO）把排序反馈对齐回 LLM。生产 serving 采用离线刷库 + 在线 KV，不把 7B 自回归模型放进请求链路。 Fidelity: 完整核心链路复现。真实执行 seq2seq SFT、beam self-sampling、离线检索反馈、partial order 构造和 rank-aware PRO；Qwen-7B/淘宝搜索替换为 T5-small/MovieLens 公开目录。本地对照口径：基线是 T5 SFT；实验组是同一模型继续做 PRO；主组合反馈从 0.62102 升至 0.80750（+30.03%），但 increment -66.02%。这是对齐阶段消融；DIN 不适用于 query rewriting 任务。  llm-recommendation query-rewriting preference-optimization search 搜广推 候选生成与搜索匹配 BEQUE 的 PRO 与只取最佳改写继续 SFT，有什么监督区别？ 只保留最佳结果会丢掉同一 query 下其余候选的相对关系；PRO 对有序候选逐级对比，使模型学习不同质量间的概率排序，并结合 SFT 稳定。长度归一与温度影响比较，排序依据仍受反馈设计约束，不能把组合分提高写成每种召回指标都提高。 示意：四个改写有明确好坏，单赢家 SFT 只说第一条值得模仿；PRO 还表达第二优于第三、第三优于第四，提供更细的候选相对监督。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-9b2761f870e80195">BEQUE 的 PRO 与只取最佳改写继续 SFT，有什么监督区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Abeque">Large Language Model based Long-tail Query Rewriting in Taobao Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只保留最佳结果会丢掉同一 query 下其余候选的相对关系；PRO 对有序候选逐级对比，使模型学习不同质量间的概率排序，并结合 SFT 稳定。长度归一与温度影响比较，排序依据仍受反馈设计约束，不能把组合分提高写成每种召回指标都提高。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>四个改写有明确好坏，单赢家 SFT 只说第一条值得模仿；PRO 还表达第二优于第三、第三优于第四，提供更细的候选相对监督。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2311.03758">原论文</a> · <a href="../../../../reproductions/2311.03758-beque/">实现解读</a> · <a href="#qa-9b2761f870e80195">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:beque" data-paper-title="Large Language Model based Long-tail Query Rewriting in Taobao Search" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Large Language Model based Long-tail Query Rewriting in Taobao Search 搜广推与 LLM 应用 Alibaba 2023-11-07 长尾电商 query 存在语义缺口，单纯 SFT 只模仿人工 rewrite，未直接对齐召回质量。BEQUE 先用拒绝采样和多指令数据 SFT，再让模型为每个 query 自采样多个 rewrite；淘宝离线搜索系统从 relevance、retrieval increment、hit rate 打分并形成偏序，最后用 Preference Ranking Optimization（PRO）把排序反馈对齐回 LLM。生产 serving 采用离线刷库 + 在线 KV，不把 7B 自回归模型放进请求链路。 Fidelity: 完整核心链路复现。真实执行 seq2seq SFT、beam self-sampling、离线检索反馈、partial order 构造和 rank-aware PRO；Qwen-7B/淘宝搜索替换为 T5-small/MovieLens 公开目录。本地对照口径：基线是 T5 SFT；实验组是同一模型继续做 PRO；主组合反馈从 0.62102 升至 0.80750（+30.03%），但 increment -66.02%。这是对齐阶段消融；DIN 不适用于 query rewriting 任务。  llm-recommendation query-rewriting preference-optimization search 搜广推 候选生成与搜索匹配 BEQUE 本地构造 PRO 偏序时，为什么不能把人工 SFT target 插入候选列表？ 对齐阶段要评价模型真实生成的改写，插入 gold target 会把生成器当时无法产生的答案混入搜索，改变实验含义。来源只使用模型候选与无标签 fallback，按目录反馈排序；测试和训练偏序也要隔离，避免把目标答案泄漏成候选优势。 示意：模型四个 beam 都没覆盖正确类别时，应如实计算反馈；额外塞入正确改写再展示胜者，会把“没生成出来”的失败伪装成成功选中了答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8125c6476f377c2e">BEQUE 本地构造 PRO 偏序时，为什么不能把人工 SFT target 插入候选列表？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Abeque">Large Language Model based Long-tail Query Rewriting in Taobao Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>对齐阶段要评价模型真实生成的改写，插入 gold target 会把生成器当时无法产生的答案混入搜索，改变实验含义。来源只使用模型候选与无标签 fallback，按目录反馈排序；测试和训练偏序也要隔离，避免把目标答案泄漏成候选优势。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型四个 beam 都没覆盖正确类别时，应如实计算反馈；额外塞入正确改写再展示胜者，会把“没生成出来”的失败伪装成成功选中了答案。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2311.03758">原论文</a> · <a href="../../../../reproductions/2311.03758-beque/">实现解读</a> · <a href="#qa-8125c6476f377c2e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:youtube-dnn" data-paper-title="Deep Neural Networks for YouTube Recommendations" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Deep Neural Networks for YouTube Recommendations 搜广推与 LLM 应用 Google / YouTube 2016-09-15 YouTube 将推荐拆成候选生成与精排。候选阶段要从百万量级视频中快速召回，传统矩阵分解难以吸收异构历史和上下文。观看历史 embedding 经过聚合和多层网络形成用户向量，训练目标把下一次观看建模为大规模多分类；服务时用近邻检索取候选。 三 seed 下 NDCG@10 为 0.02854→0.02666，该缩放设置未复现论文方向性收益，作为负结果保留。复现级别：核心机制复现。复现级别：核心机制复现。实际训练历史聚合、非线性用户塔和 item embedding 打分；YouTube 私有日志及生产 sampled softmax 未复刻。本地对照口径：基线为历史均值 two-tower，实验组增加 YouTube DNN 非线性用户塔；NDCG@10 相对 -6.61%，见 metrics/movielens-100k-seeds42-44.json。  retrieval ranking classic two-stage 搜广推 候选生成与搜索匹配 YouTube DNN候选生成为什么用深用户塔？ 历史与上下文异构，聚合embedding后深网络形成用户向量，把下一观看作大规模分类，再以近邻快速召回；精排是另一阶段，不由该召回向量独自完成。 例如先从百万视频找少量候选，再由精排考虑更多特征。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<span id="paper-recommendation-youtube-dnn-d653b9f6" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-26a9aedb5d40afbd">YouTube DNN候选生成为什么用深用户塔？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ayoutube-dnn">Deep Neural Networks for YouTube Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>历史与上下文异构，聚合embedding后深网络形成用户向量，把下一观看作大规模分类，再以近邻快速召回；精排是另一阶段，不由该召回向量独自完成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先从百万视频找少量候选，再由精排考虑更多特征。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://research.google/pubs/deep-neural-networks-for-youtube-recommendations/">原论文</a> · <a href="../../../../reproductions/recsys2016-youtube-dnn-youtube-dnn/">实现解读</a> · <a href="#qa-26a9aedb5d40afbd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:youtube-dnn" data-paper-title="Deep Neural Networks for YouTube Recommendations" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Deep Neural Networks for YouTube Recommendations 搜广推与 LLM 应用 Google / YouTube 2016-09-15 YouTube 将推荐拆成候选生成与精排。候选阶段要从百万量级视频中快速召回，传统矩阵分解难以吸收异构历史和上下文。观看历史 embedding 经过聚合和多层网络形成用户向量，训练目标把下一次观看建模为大规模多分类；服务时用近邻检索取候选。 三 seed 下 NDCG@10 为 0.02854→0.02666，该缩放设置未复现论文方向性收益，作为负结果保留。复现级别：核心机制复现。复现级别：核心机制复现。实际训练历史聚合、非线性用户塔和 item embedding 打分；YouTube 私有日志及生产 sampled softmax 未复刻。本地对照口径：基线为历史均值 two-tower，实验组增加 YouTube DNN 非线性用户塔；NDCG@10 相对 -6.61%，见 metrics/movielens-100k-seeds42-44.json。  retrieval ranking classic two-stage 搜广推 候选生成与搜索匹配 YouTube DNN 为什么把下一观看训练为大规模分类，却在服务时只做向量近邻检索？ 用户历史与上下文经非线性网络形成向量，训练用物品向量点积的多分类目标，使观看过的目标比负例更匹配。相同点积结构允许服务端预建物品索引，快速寻找高分候选，避免逐视频运行复杂网络。它是候选生成器的效率设计，不能把召回分数直接等同于精排最终效用。 示意：训练时让用户向量更靠近真实下一视频，远离采样负例；请求时只算一次用户向量，再从百万视频索引取近邻，后续精排继续处理更复杂的候选特征。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:youtube-dnn" data-paper-title="Deep Neural Networks for YouTube Recommendations" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Deep Neural Networks for YouTube Recommendations 搜广推与 LLM 应用 Google / YouTube 2016-09-15 YouTube 将推荐拆成候选生成与精排。候选阶段要从百万量级视频中快速召回，传统矩阵分解难以吸收异构历史和上下文。观看历史 embedding 经过聚合和多层网络形成用户向量，训练目标把下一次观看建模为大规模多分类；服务时用近邻检索取候选。 三 seed 下 NDCG@10 为 0.02854→0.02666，该缩放设置未复现论文方向性收益，作为负结果保留。复现级别：核心机制复现。复现级别：核心机制复现。实际训练历史聚合、非线性用户塔和 item embedding 打分；YouTube 私有日志及生产 sampled softmax 未复刻。本地对照口径：基线为历史均值 two-tower，实验组增加 YouTube DNN 非线性用户塔；NDCG@10 相对 -6.61%，见 metrics/movielens-100k-seeds42-44.json。  retrieval ranking classic two-stage 搜广推 候选生成与搜索匹配 深用户塔与传统矩阵分解主要多了什么？ 矩阵分解常学习固定用户item因子，深塔可用历史和上下文动态组合用户状态。它仍有向量压缩瓶颈，不能因为加MLP就假定覆盖所有多兴趣。 例如同一用户近期兴趣变动可进入塔输入，而不只查一个固定用户ID向量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0e36e5eadec2c06c">深用户塔与传统矩阵分解主要多了什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ayoutube-dnn">Deep Neural Networks for YouTube Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>矩阵分解常学习固定用户item因子，深塔可用历史和上下文动态组合用户状态。它仍有向量压缩瓶颈，不能因为加MLP就假定覆盖所有多兴趣。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一用户近期兴趣变动可进入塔输入，而不只查一个固定用户ID向量。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://research.google/pubs/deep-neural-networks-for-youtube-recommendations/">原论文</a> · <a href="../../../../reproductions/recsys2016-youtube-dnn-youtube-dnn/">实现解读</a> · <a href="#qa-0e36e5eadec2c06c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:youtube-dnn" data-paper-title="Deep Neural Networks for YouTube Recommendations" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/retrieval-matching" data-search="Deep Neural Networks for YouTube Recommendations 搜广推与 LLM 应用 Google / YouTube 2016-09-15 YouTube 将推荐拆成候选生成与精排。候选阶段要从百万量级视频中快速召回，传统矩阵分解难以吸收异构历史和上下文。观看历史 embedding 经过聚合和多层网络形成用户向量，训练目标把下一次观看建模为大规模多分类；服务时用近邻检索取候选。 三 seed 下 NDCG@10 为 0.02854→0.02666，该缩放设置未复现论文方向性收益，作为负结果保留。复现级别：核心机制复现。复现级别：核心机制复现。实际训练历史聚合、非线性用户塔和 item embedding 打分；YouTube 私有日志及生产 sampled softmax 未复刻。本地对照口径：基线为历史均值 two-tower，实验组增加 YouTube DNN 非线性用户塔；NDCG@10 相对 -6.61%，见 metrics/movielens-100k-seeds42-44.json。  retrieval ranking classic two-stage 搜广推 候选生成与搜索匹配 下一观看softmax训练与服务近邻如何保持一致？ 用户与视频向量采用对应打分空间，训练只见截止前历史，服务检索同版本item向量；负采样近似与全库概率不能混报。当前公开实现不含原百万库存和私有训练服务。 例如模型升级用户空间后，旧item索引未刷新可能让近邻含义错位。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 候选生成与搜索匹配</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0f7c96d8cf079da2">下一观看softmax训练与服务近邻如何保持一致？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ayoutube-dnn">Deep Neural Networks for YouTube Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用户与视频向量采用对应打分空间，训练只见截止前历史，服务检索同版本item向量；负采样近似与全库概率不能混报。当前公开实现不含原百万库存和私有训练服务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型升级用户空间后，旧item索引未刷新可能让近邻含义错位。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://research.google/pubs/deep-neural-networks-for-youtube-recommendations/">原论文</a> · <a href="../../../../reproductions/recsys2016-youtube-dnn-youtube-dnn/">实现解读</a> · <a href="#qa-0f7c96d8cf079da2">问题链接</a></p>
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
