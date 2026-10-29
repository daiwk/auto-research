---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 长上下文：注意力、递归状态与记忆

[基础模型](index.md) / 132 个问题 · 33 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

[阅读本主题精读卡片：多篇论文对比、分析与问答](../../deep-dives/foundation-models/context-and-state.md)

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
<p class="ar-learning-status" data-learning-status role="status">132 个问题 · 33 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:select-ttt" data-paper-title="Select-TTT: Query-Conditioned Selective Fast Weight Updates for In-Place Test-Time Training" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Select-TTT: Query-Conditioned Selective Fast Weight Updates for In-Place Test-Time Training 基础模型 University of Science and Technology of China 2026-10-27 In-Place TTT 把 MLP 下投影作为 fast weights，边读上下文边写入；对所有 chunk 使用相同学习率会把无关内容也等强写进去。Select-TTT 不新增检索编码器或可学习门控，而从冻结输出头读取上下文 hidden 对用户问题 token的预测程度，为每个 chunk 生成连续写入倍率。它不是先找到 gold answer chunk 再加强写入。论文的 answer-chunk 实验只是动机分析；部署规则只用问题，不允许答案标记进入评分接口。 完整实验：成本过高，不复现（审查 DONE）；本地状态：L1 查询评分与 fast-weight 写入组件、diagnostic only，没有加载 LLM 或接入 LongMemEval。完整实验：成本过高，不复现（审查 DONE）；不是可执行 evolve 能力算子。实现词表分块 log-sum-exp 与直接问题 token logits、最低 CE top-k、温度 / clip 倍率及顺序 apply-then-write 参考。调用者必须提供真实模型的 RMSNorm 参数和 epsilon，以及原 In-Place TTT 的 NTP 对齐 keys / values；  注意力与长上下文 测试时训练与fast weights 基础模型 长上下文：注意力、递归状态与记忆 Select-TTT改变的是上下文检索，还是写入fast weights的力度？ 它保留In-Place TTT的分chunk写入，只按问题相关性缩放每个chunk的学习率。相关性来自冻结LM输出头对问题token的负对数概率，不另训检索器，也不直接丢弃所有低分chunk。问题不同，写入倍率也可能不同。 教学例子：同一长对话中，问搬家日期和问饮食偏好时，应强化的片段不同；这不表示模型拿到了哪一段包含标准答案的标签。 2026-10-29">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-select-ttt-1dc0ac0a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-99cdb22b8325ac12">Select-TTT改变的是上下文检索，还是写入fast weights的力度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aselect-ttt">Select-TTT: Query-Conditioned Selective Fast Weight Updates for In-Place Test-Time Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-29 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它保留In-Place TTT的分chunk写入，只按问题相关性缩放每个chunk的学习率。相关性来自冻结LM输出头对问题token的负对数概率，不另训检索器，也不直接丢弃所有低分chunk。问题不同，写入倍率也可能不同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一长对话中，问搬家日期和问饮食偏好时，应强化的片段不同；这不表示模型拿到了哪一段包含标准答案的标签。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.36794v1">原论文</a> · <a href="../../../../foundation-models/2610.36794-select-ttt/">实现解读</a> · <a href="#qa-99cdb22b8325ac12">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:select-ttt" data-paper-title="Select-TTT: Query-Conditioned Selective Fast Weight Updates for In-Place Test-Time Training" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Select-TTT: Query-Conditioned Selective Fast Weight Updates for In-Place Test-Time Training 基础模型 University of Science and Technology of China 2026-10-27 In-Place TTT 把 MLP 下投影作为 fast weights，边读上下文边写入；对所有 chunk 使用相同学习率会把无关内容也等强写进去。Select-TTT 不新增检索编码器或可学习门控，而从冻结输出头读取上下文 hidden 对用户问题 token的预测程度，为每个 chunk 生成连续写入倍率。它不是先找到 gold answer chunk 再加强写入。论文的 answer-chunk 实验只是动机分析；部署规则只用问题，不允许答案标记进入评分接口。 完整实验：成本过高，不复现（审查 DONE）；本地状态：L1 查询评分与 fast-weight 写入组件、diagnostic only，没有加载 LLM 或接入 LongMemEval。完整实验：成本过高，不复现（审查 DONE）；不是可执行 evolve 能力算子。实现词表分块 log-sum-exp 与直接问题 token logits、最低 CE top-k、温度 / clip 倍率及顺序 apply-then-write 参考。调用者必须提供真实模型的 RMSNorm 参数和 epsilon，以及原 In-Place TTT 的 NTP 对齐 keys / values；  注意力与长上下文 测试时训练与fast weights 基础模型 长上下文：注意力、递归状态与记忆 为什么chunk相关性取最低CE位置的top-k均值，而不是最高CE？ 这里CE是问题token在当前hidden诱导的词表分布下的平均负对数概率；越低，说明该位置越能预测问题词汇。取最低CE的若干位置可保留局部相关证据，同时比只取单个最小值更稳健。把方向反过来会强化最不相关的位置。 教学例子：两位置的查询CE为1和6，取最相关的一项应选1；选6相当于把低概率误作高相关。问题序列中重复的token仍按出现次数计入平均。 2026-10-29">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-0936a469597e97bb">为什么chunk相关性取最低CE位置的top-k均值，而不是最高CE？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aselect-ttt">Select-TTT: Query-Conditioned Selective Fast Weight Updates for In-Place Test-Time Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-29 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这里CE是问题token在当前hidden诱导的词表分布下的平均负对数概率；越低，说明该位置越能预测问题词汇。取最低CE的若干位置可保留局部相关证据，同时比只取单个最小值更稳健。把方向反过来会强化最不相关的位置。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两位置的查询CE为1和6，取最相关的一项应选1；选6相当于把低概率误作高相关。问题序列中重复的token仍按出现次数计入平均。</p>
<p class="ar-learning-sources">依据：核心公式、检查与负控；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.36794v1">原论文</a> · <a href="../../../../foundation-models/2610.36794-select-ttt/">实现解读</a> · <a href="#qa-0936a469597e97bb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:select-ttt" data-paper-title="Select-TTT: Query-Conditioned Selective Fast Weight Updates for In-Place Test-Time Training" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Select-TTT: Query-Conditioned Selective Fast Weight Updates for In-Place Test-Time Training 基础模型 University of Science and Technology of China 2026-10-27 In-Place TTT 把 MLP 下投影作为 fast weights，边读上下文边写入；对所有 chunk 使用相同学习率会把无关内容也等强写进去。Select-TTT 不新增检索编码器或可学习门控，而从冻结输出头读取上下文 hidden 对用户问题 token的预测程度，为每个 chunk 生成连续写入倍率。它不是先找到 gold answer chunk 再加强写入。论文的 answer-chunk 实验只是动机分析；部署规则只用问题，不允许答案标记进入评分接口。 完整实验：成本过高，不复现（审查 DONE）；本地状态：L1 查询评分与 fast-weight 写入组件、diagnostic only，没有加载 LLM 或接入 LongMemEval。完整实验：成本过高，不复现（审查 DONE）；不是可执行 evolve 能力算子。实现词表分块 log-sum-exp 与直接问题 token logits、最低 CE top-k、温度 / clip 倍率及顺序 apply-then-write 参考。调用者必须提供真实模型的 RMSNorm 参数和 epsilon，以及原 In-Place TTT 的 NTP 对齐 keys / values；  注意力与长上下文 测试时训练与fast weights 基础模型 长上下文：注意力、递归状态与记忆 为什么不能把Select-TTT描述成“严格守恒的写入预算分配”？ 乘chunk数后的softmax在没有clip时和为chunk数；随后上限截断可能降低总和。论文描述近似保持平均学习率，不等于截断后严格守恒。再归一化会改变Eq.10，还可能重新超过单chunk上限，不能悄悄替换。 教学例子：三个chunk的softmax几乎全压到第一个，乘3后约为[3,0,0]；上限1.2后总和约1.2，不是3。这是公式例子，不是QA实验。 2026-10-29">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-aa77181e9a488912">为什么不能把Select-TTT描述成“严格守恒的写入预算分配”？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aselect-ttt">Select-TTT: Query-Conditioned Selective Fast Weight Updates for In-Place Test-Time Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-29 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>乘chunk数后的softmax在没有clip时和为chunk数；随后上限截断可能降低总和。论文描述近似保持平均学习率，不等于截断后严格守恒。再归一化会改变Eq.10，还可能重新超过单chunk上限，不能悄悄替换。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三个chunk的softmax几乎全压到第一个，乘3后约为[3,0,0]；上限1.2后总和约1.2，不是3。这是公式例子，不是QA实验。</p>
<p class="ar-learning-sources">依据：核心公式、检查与负控；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.36794v1">原论文</a> · <a href="../../../../foundation-models/2610.36794-select-ttt/">实现解读</a> · <a href="#qa-aa77181e9a488912">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:select-ttt" data-paper-title="Select-TTT: Query-Conditioned Selective Fast Weight Updates for In-Place Test-Time Training" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Select-TTT: Query-Conditioned Selective Fast Weight Updates for In-Place Test-Time Training 基础模型 University of Science and Technology of China 2026-10-27 In-Place TTT 把 MLP 下投影作为 fast weights，边读上下文边写入；对所有 chunk 使用相同学习率会把无关内容也等强写进去。Select-TTT 不新增检索编码器或可学习门控，而从冻结输出头读取上下文 hidden 对用户问题 token的预测程度，为每个 chunk 生成连续写入倍率。它不是先找到 gold answer chunk 再加强写入。论文的 answer-chunk 实验只是动机分析；部署规则只用问题，不允许答案标记进入评分接口。 完整实验：成本过高，不复现（审查 DONE）；本地状态：L1 查询评分与 fast-weight 写入组件、diagnostic only，没有加载 LLM 或接入 LongMemEval。完整实验：成本过高，不复现（审查 DONE）；不是可执行 evolve 能力算子。实现词表分块 log-sum-exp 与直接问题 token logits、最低 CE top-k、温度 / clip 倍率及顺序 apply-then-write 参考。调用者必须提供真实模型的 RMSNorm 参数和 epsilon，以及原 In-Place TTT 的 NTP 对齐 keys / values；  注意力与长上下文 测试时训练与fast weights 基础模型 长上下文：注意力、递归状态与记忆 fast-weight参考实现为何必须先输出当前chunk，再写入它的keys与values？ 当前chunk输出使用更新前的状态，随后才把该chunk信息写入供后续使用。若先写后读，当前输出就利用了本应更新后才存在的value，改变因果顺序。本地只验证这种张量状态变化；真实NTP对齐特征、backbone和长对话评测尚未接入。 教学例子：初始W为0，第一个chunk先输出0，再写成W=1，第二个才能读到1；若第一个就输出1，已把当前写入提前使用。 2026-10-29">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f70c34eaf358e479">fast-weight参考实现为何必须先输出当前chunk，再写入它的keys与values？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aselect-ttt">Select-TTT: Query-Conditioned Selective Fast Weight Updates for In-Place Test-Time Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-29 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>当前chunk输出使用更新前的状态，随后才把该chunk信息写入供后续使用。若先写后读，当前输出就利用了本应更新后才存在的value，改变因果顺序。本地只验证这种张量状态变化；真实NTP对齐特征、backbone和长对话评测尚未接入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>初始W为0，第一个chunk先输出0，再写成W=1，第二个才能读到1；若第一个就输出1，已把当前写入提前使用。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、检查与负控；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.36794v1">原论文</a> · <a href="../../../../foundation-models/2610.36794-select-ttt/">实现解读</a> · <a href="#qa-f70c34eaf358e479">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:openattention" data-paper-title="OpenAttention: One Percent Is Enough with Tail Proxies" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="OpenAttention: One Percent Is Enough with Tail Proxies 基础模型 Sogang University 2026-10-22 低读取率稀疏注意力不只需要选出少量重要 KV，还需要处理未读取的尾部。OpenAttention 在 query 二阶矩定义的几何空间内聚类，以 ErrorGate 估计簇内代理误差并分配精确读取预算；每个簇的未读部分成为一个带计数的均值代理。它不是单纯的 top-k 截断或均值池化。 完整实验成本过高，不复现（审查 DONE）。该小规模诊断仅核对公式与可执行性，不是语言模型能力比较。fit_cache、qgs_scores、errorgate、waterfill、residual_proxy_attention、attend 真实执行完整单头算子链。为便于独立核对，残余均值直接从未读行重算，而不是移植 Triton 的缓存和减法实现。全零误差按等权 water filling 处理；排序并列按原位置，空簇保持无代理，均为显式确定性边界。  高效注意力 KV缓存与稀疏推理 基础模型 长上下文：注意力、递归状态与记忆 OpenAttention 为什么不满足于“只读少量重要 KV”？ 低读取率下，未读尾部仍可能携带大量总权重。OpenAttention把精确读取与带计数的残余簇均值代理结合，尝试保留尾部质量，而非把所有未读token当作没有贡献。 示意：很多单项不突出的历史词，合起来的注意力质量也可能影响输出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-openattention-57f03e45" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6de51fcd1292a9c7">OpenAttention 为什么不满足于“只读少量重要 KV”？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aopenattention">OpenAttention: One Percent Is Enough with Tail Proxies</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Sogang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>低读取率下，未读尾部仍可能携带大量总权重。OpenAttention把精确读取与带计数的残余簇均值代理结合，尝试保留尾部质量，而非把所有未读token当作没有贡献。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>很多单项不突出的历史词，合起来的注意力质量也可能影响输出。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30951v1">原论文</a> · <a href="../../../../foundation-models/2610.30951-openattention/">实现解读</a> · <a href="#qa-6de51fcd1292a9c7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:openattention" data-paper-title="OpenAttention: One Percent Is Enough with Tail Proxies" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="OpenAttention: One Percent Is Enough with Tail Proxies 基础模型 Sogang University 2026-10-22 低读取率稀疏注意力不只需要选出少量重要 KV，还需要处理未读取的尾部。OpenAttention 在 query 二阶矩定义的几何空间内聚类，以 ErrorGate 估计簇内代理误差并分配精确读取预算；每个簇的未读部分成为一个带计数的均值代理。它不是单纯的 top-k 截断或均值池化。 完整实验成本过高，不复现（审查 DONE）。该小规模诊断仅核对公式与可执行性，不是语言模型能力比较。fit_cache、qgs_scores、errorgate、waterfill、residual_proxy_attention、attend 真实执行完整单头算子链。为便于独立核对，残余均值直接从未读行重算，而不是移植 Triton 的缓存和减法实现。全零误差按等权 water filling 处理；排序并列按原位置，空簇保持无代理，均为显式确定性边界。  高效注意力 KV缓存与稀疏推理 基础模型 长上下文：注意力、递归状态与记忆 OpenAttention只精读少量KV，为什么还要给未读尾部留一个带计数的代理？ 直接top-k会把未读token的softmax质量全部丢掉。OpenAttention按查询相关几何聚类，给高估计误差的簇更多精读预算；剩余token以均值key/value代理参与归一化，并在logit中加入对数数量。这样保留尾部的总质量近似，但簇内分布与误差估计仍有假设，不能视为精确attention。 教学例子：100个相似尾部token各自权重不大，合起来却很可观；一个无计数的均值代理只算一次，会低估它们，加入数量修正才能近似这100项的总贡献。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-deccca2f42b3b93c">OpenAttention只精读少量KV，为什么还要给未读尾部留一个带计数的代理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aopenattention">OpenAttention: One Percent Is Enough with Tail Proxies</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Sogang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直接top-k会把未读token的softmax质量全部丢掉。OpenAttention按查询相关几何聚类，给高估计误差的簇更多精读预算；剩余token以均值key/value代理参与归一化，并在logit中加入对数数量。这样保留尾部的总质量近似，但簇内分布与误差估计仍有假设，不能视为精确attention。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>100个相似尾部token各自权重不大，合起来却很可观；一个无计数的均值代理只算一次，会低估它们，加入数量修正才能近似这100项的总贡献。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30951v1">原论文</a> · <a href="../../../../foundation-models/2610.30951-openattention/">实现解读</a> · <a href="#qa-deccca2f42b3b93c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:openattention" data-paper-title="OpenAttention: One Percent Is Enough with Tail Proxies" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="OpenAttention: One Percent Is Enough with Tail Proxies 基础模型 Sogang University 2026-10-22 低读取率稀疏注意力不只需要选出少量重要 KV，还需要处理未读取的尾部。OpenAttention 在 query 二阶矩定义的几何空间内聚类，以 ErrorGate 估计簇内代理误差并分配精确读取预算；每个簇的未读部分成为一个带计数的均值代理。它不是单纯的 top-k 截断或均值池化。 完整实验成本过高，不复现（审查 DONE）。该小规模诊断仅核对公式与可执行性，不是语言模型能力比较。fit_cache、qgs_scores、errorgate、waterfill、residual_proxy_attention、attend 真实执行完整单头算子链。为便于独立核对，残余均值直接从未读行重算，而不是移植 Triton 的缓存和减法实现。全零误差按等权 water filling 处理；排序并列按原位置，空簇保持无代理，均为显式确定性边界。  高效注意力 KV缓存与稀疏推理 基础模型 长上下文：注意力、递归状态与记忆 OpenAttention 的残余代理，相对普通 top-k 截断多保留了什么？ top-k以外的内容被直接忽略；残余代理以剩余均值和数量近似未读集合的贡献，并与精确token联合softmax。它仍是近似，不是把代理均值当成尾部的精确恢复。 示意：一个簇剩下100个相近token，代理不应仅以“一项”的权重参与归一化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b733e66f95bcc284">OpenAttention 的残余代理，相对普通 top-k 截断多保留了什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aopenattention">OpenAttention: One Percent Is Enough with Tail Proxies</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Sogang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>top-k以外的内容被直接忽略；残余代理以剩余均值和数量近似未读集合的贡献，并与精确token联合softmax。它仍是近似，不是把代理均值当成尾部的精确恢复。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个簇剩下100个相近token，代理不应仅以“一项”的权重参与归一化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30951v1">原论文</a> · <a href="../../../../foundation-models/2610.30951-openattention/">实现解读</a> · <a href="#qa-b733e66f95bcc284">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:openattention" data-paper-title="OpenAttention: One Percent Is Enough with Tail Proxies" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="OpenAttention: One Percent Is Enough with Tail Proxies 基础模型 Sogang University 2026-10-22 低读取率稀疏注意力不只需要选出少量重要 KV，还需要处理未读取的尾部。OpenAttention 在 query 二阶矩定义的几何空间内聚类，以 ErrorGate 估计簇内代理误差并分配精确读取预算；每个簇的未读部分成为一个带计数的均值代理。它不是单纯的 top-k 截断或均值池化。 完整实验成本过高，不复现（审查 DONE）。该小规模诊断仅核对公式与可执行性，不是语言模型能力比较。fit_cache、qgs_scores、errorgate、waterfill、residual_proxy_attention、attend 真实执行完整单头算子链。为便于独立核对，残余均值直接从未读行重算，而不是移植 Triton 的缓存和减法实现。全零误差按等权 water filling 处理；排序并列按原位置，空簇保持无代理，均为显式确定性边界。  高效注意力 KV缓存与稀疏推理 基础模型 长上下文：注意力、递归状态与记忆 精确 token 选出后，为什么必须从簇代理里扣除这些行并重算计数？ 否则选中的token会同时以精确项和代理成分被重复计算。残余簇需重算均值与数量，并在logit加入log计数；空簇不再产生代理。文档的确定性边界不能偷偷用经验补丁替代。 示意：簇原有10项、精确读取3项，剩余代理代表7项，而不是继续代表10项。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-72235cc045539e99">精确 token 选出后，为什么必须从簇代理里扣除这些行并重算计数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aopenattention">OpenAttention: One Percent Is Enough with Tail Proxies</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Sogang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>否则选中的token会同时以精确项和代理成分被重复计算。残余簇需重算均值与数量，并在logit加入log计数；空簇不再产生代理。文档的确定性边界不能偷偷用经验补丁替代。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>簇原有10项、精确读取3项，剩余代理代表7项，而不是继续代表10项。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30951v1">原论文</a> · <a href="../../../../foundation-models/2610.30951-openattention/">实现解读</a> · <a href="#qa-72235cc045539e99">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ttr-compressor" data-paper-title="Rethinking Sequence Compression with Test-time Regression" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Rethinking Sequence Compression with Test-time Regression 基础模型 The Chinese University of Hong Kong 2026-10-22 固定池化或投影分别聚合 token，难以按当前输入的相关结构调整压缩。TTR 把一组 token 视作回归观测：由 token 方向构造 key，由保留模长的原始 token 生成可学习标量 target；每次前向精确求解 ridge 系数，直接把系数作为压缩表示。外层任务 loss 通过闭式求解训练 target 投影与正则。“test-time”指输入相关的回归系数在前向内重新拟合，不表示推理时更新模型参数。基础版本只有个可训练参数，不是另建一个 agent 或训练时读取正确压缩答案。 完整模型训练和多基准评估成本过高，不复现（审查 DONE），不下载、不试跑、不进入自动重试或实现队列。三个 seed 不会把机制诊断升级成能力复现。ttr_compress 独立实现正对角 generalized ridge 与 dual Cholesky；TTRCompressor 将注册成可训练参数。diagnostic(seed, device=&#x27;cpu&#x27;) 生成4组、每组7个12维 token，执行外层反传和一次真实 SGD 更新，返回严格的 seed/metrics/checks。既不下载数据或权重，也不调用 pretrained 模型。  序列压缩 可微测试时回归 基础模型 长上下文：注意力、递归状态与记忆 TTR-Compressor 的“test-time”是否表示推理时再训练模型参数？ 这里指每次前向按当前token组重新拟合回归系数，把系数作为压缩表示。可训练target投影和正则由外层loss学习；输入相关的闭式拟合不等同于推理时更新这些模型参数。 示意：两组输入使用同一套a和ρ，却各自解出不同的压缩系数h。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-ttr-compressor-1230f560" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-453f6b16d07755e9">TTR-Compressor 的“test-time”是否表示推理时再训练模型参数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Attr-compressor">Rethinking Sequence Compression with Test-time Regression</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这里指每次前向按当前token组重新拟合回归系数，把系数作为压缩表示。可训练target投影和正则由外层loss学习；输入相关的闭式拟合不等同于推理时更新这些模型参数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两组输入使用同一套a和ρ，却各自解出不同的压缩系数h。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31574v1">原论文</a> · <a href="../../../../foundation-models/2610.31574-ttr-compressor/">实现解读</a> · <a href="#qa-453f6b16d07755e9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ttr-compressor" data-paper-title="Rethinking Sequence Compression with Test-time Regression" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Rethinking Sequence Compression with Test-time Regression 基础模型 The Chinese University of Hong Kong 2026-10-22 固定池化或投影分别聚合 token，难以按当前输入的相关结构调整压缩。TTR 把一组 token 视作回归观测：由 token 方向构造 key，由保留模长的原始 token 生成可学习标量 target；每次前向精确求解 ridge 系数，直接把系数作为压缩表示。外层任务 loss 通过闭式求解训练 target 投影与正则。“test-time”指输入相关的回归系数在前向内重新拟合，不表示推理时更新模型参数。基础版本只有个可训练参数，不是另建一个 agent 或训练时读取正确压缩答案。 完整模型训练和多基准评估成本过高，不复现（审查 DONE），不下载、不试跑、不进入自动重试或实现队列。三个 seed 不会把机制诊断升级成能力复现。ttr_compress 独立实现正对角 generalized ridge 与 dual Cholesky；TTRCompressor 将注册成可训练参数。diagnostic(seed, device=&#x27;cpu&#x27;) 生成4组、每组7个12维 token，执行外层反传和一次真实 SGD 更新，返回严格的 seed/metrics/checks。既不下载数据或权重，也不调用 pretrained 模型。  序列压缩 可微测试时回归 基础模型 长上下文：注意力、递归状态与记忆 TTR为什么只归一化key，却让回归target保留原始token的模长？ key的单位化让回归按方向组织观测，target仍保留输入强度；二者的这种不对称使系数反映当前token集合。若target也由归一化key的同一个静态投影产生，固定向量就能平凡拟合，失去输入相关压缩意义。每次前向求回归系数，不等于推理时更新模型的持久参数。 教学例子：两个token方向相同、模长分别1和3；key相同但target不同，回归必须权衡两次观测。若两边都归一化，它们会变成同一个监督点，强度差异随之消失。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-0f87d6fafc5bcc63">TTR为什么只归一化key，却让回归target保留原始token的模长？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Attr-compressor">Rethinking Sequence Compression with Test-time Regression</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>key的单位化让回归按方向组织观测，target仍保留输入强度；二者的这种不对称使系数反映当前token集合。若target也由归一化key的同一个静态投影产生，固定向量就能平凡拟合，失去输入相关压缩意义。每次前向求回归系数，不等于推理时更新模型的持久参数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个token方向相同、模长分别1和3；key相同但target不同，回归必须权衡两次观测。若两边都归一化，它们会变成同一个监督点，强度差异随之消失。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31574v1">原论文</a> · <a href="../../../../foundation-models/2610.31574-ttr-compressor/">实现解读</a> · <a href="#qa-0f87d6fafc5bcc63">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ttr-compressor" data-paper-title="Rethinking Sequence Compression with Test-time Regression" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Rethinking Sequence Compression with Test-time Regression 基础模型 The Chinese University of Hong Kong 2026-10-22 固定池化或投影分别聚合 token，难以按当前输入的相关结构调整压缩。TTR 把一组 token 视作回归观测：由 token 方向构造 key，由保留模长的原始 token 生成可学习标量 target；每次前向精确求解 ridge 系数，直接把系数作为压缩表示。外层任务 loss 通过闭式求解训练 target 投影与正则。“test-time”指输入相关的回归系数在前向内重新拟合，不表示推理时更新模型参数。基础版本只有个可训练参数，不是另建一个 agent 或训练时读取正确压缩答案。 完整模型训练和多基准评估成本过高，不复现（审查 DONE），不下载、不试跑、不进入自动重试或实现队列。三个 seed 不会把机制诊断升级成能力复现。ttr_compress 独立实现正对角 generalized ridge 与 dual Cholesky；TTRCompressor 将注册成可训练参数。diagnostic(seed, device=&#x27;cpu&#x27;) 生成4组、每组7个12维 token，执行外层反传和一次真实 SGD 更新，返回严格的 seed/metrics/checks。既不下载数据或权重，也不调用 pretrained 模型。  序列压缩 可微测试时回归 基础模型 长上下文：注意力、递归状态与记忆 TTR 与固定平均池化的主要区别，为什么不只是换一组权重？ 平均池化按固定聚合规则输出；TTR将当前组构造成ridge回归问题，精确求解与这组相关结构有关的系数，并通过求解反传训练外层参数。它改变了压缩问题的定义。 示意：两组token均值相同，但方向相关性不同，回归压缩仍可能产生不同表示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-9ee87e3a06c2bbc4">TTR 与固定平均池化的主要区别，为什么不只是换一组权重？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Attr-compressor">Rethinking Sequence Compression with Test-time Regression</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>平均池化按固定聚合规则输出；TTR将当前组构造成ridge回归问题，精确求解与这组相关结构有关的系数，并通过求解反传训练外层参数。它改变了压缩问题的定义。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两组token均值相同，但方向相关性不同，回归压缩仍可能产生不同表示。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31574v1">原论文</a> · <a href="../../../../foundation-models/2610.31574-ttr-compressor/">实现解读</a> · <a href="#qa-9ee87e3a06c2bbc4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ttr-compressor" data-paper-title="Rethinking Sequence Compression with Test-time Regression" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Rethinking Sequence Compression with Test-time Regression 基础模型 The Chinese University of Hong Kong 2026-10-22 固定池化或投影分别聚合 token，难以按当前输入的相关结构调整压缩。TTR 把一组 token 视作回归观测：由 token 方向构造 key，由保留模长的原始 token 生成可学习标量 target；每次前向精确求解 ridge 系数，直接把系数作为压缩表示。外层任务 loss 通过闭式求解训练 target 投影与正则。“test-time”指输入相关的回归系数在前向内重新拟合，不表示推理时更新模型参数。基础版本只有个可训练参数，不是另建一个 agent 或训练时读取正确压缩答案。 完整模型训练和多基准评估成本过高，不复现（审查 DONE），不下载、不试跑、不进入自动重试或实现队列。三个 seed 不会把机制诊断升级成能力复现。ttr_compress 独立实现正对角 generalized ridge 与 dual Cholesky；TTRCompressor 将注册成可训练参数。diagnostic(seed, device=&#x27;cpu&#x27;) 生成4组、每组7个12维 token，执行外层反传和一次真实 SGD 更新，返回严格的 seed/metrics/checks。既不下载数据或权重，也不调用 pretrained 模型。  序列压缩 可微测试时回归 基础模型 长上下文：注意力、递归状态与记忆 TTR 的 dual solve 为什么在 token 轴形成 T×T 矩阵，且不能 detach？ 用K按D的逆平方根缩放后，解I_T加K_tilde K_tilde转置的Cholesky方程，再映射回d维系数。外层loss需要通过solve训练target投影和正则，detach会切断定义中的学习路径；复杂度也保留T的三次项。 示意：T远小于d时解token轴方程较合适，但不能据此把任意T规模都宣称为只需O(T²d)。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-70dfe34e2a284c5f">TTR 的 dual solve 为什么在 token 轴形成 T×T 矩阵，且不能 detach？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Attr-compressor">Rethinking Sequence Compression with Test-time Regression</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用K按D的逆平方根缩放后，解I_T加K_tilde K_tilde转置的Cholesky方程，再映射回d维系数。外层loss需要通过solve训练target投影和正则，detach会切断定义中的学习路径；复杂度也保留T的三次项。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>T远小于d时解token轴方程较合适，但不能据此把任意T规模都宣称为只需O(T²d)。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31574v1">原论文</a> · <a href="../../../../foundation-models/2610.31574-ttr-compressor/">实现解读</a> · <a href="#qa-70dfe34e2a284c5f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:stratified-sparse-attention" data-paper-title="Stratified Sparse Attention: Reducing the Sparse-to-Dense Gap at Extreme Sparsity" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Stratified Sparse Attention: Reducing the Sparse-to-Dense Gap at Extreme Sparsity 基础模型 Rice University 2026-10-20 只保留 top-k 会丢掉尾部质量；均匀抽样又浪费预算。SSA先确定保留高概率项，再按残差代理分布抽样。关键不是“top-k加采样”的外形，而是有放回抽样后去重，按每个token至少出现一次的包含概率修正。论文的自适应 Algorithm 1 与实际优化内核的固定 heavy fraction 版本不同；本地实现前者，不冒充后者的速度。 完整实验标注成本过高，不复现（审查 DONE），不下载、不试跑、不自动重试。L1诊断不是正式能力比较，不参与Evolve晋级。stratified_sparse_attention 接受单query、keys、values和外部代理分数，真实执行water-filling、离散采样和精确选中项打分。梯度只通过实际选中Q/K/V；代理分配是detached离散步骤。没有声称实现PQCache代理、层级采样或paged KV runtime。  注意力与长上下文 稀疏注意力 基础模型 长上下文：注意力、递归状态与记忆 SSA 为什么既确定保留 heavy 项，又随机覆盖剩余尾部？ 只留top-k会丢掉尾部，均匀采样又可能浪费预算。SSA按代理分数分配确定保留和残差抽样预算，再用包含概率修正被选token，兼顾重要项与尾部覆盖。 示意：强证据稳定保留，较弱证据仍有被抽到的机会，而非全部被硬截断。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-stratified-sparse-attention-869759f6" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4e03b2497b28be11">SSA 为什么既确定保留 heavy 项，又随机覆盖剩余尾部？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Astratified-sparse-attention">Stratified Sparse Attention: Reducing the Sparse-to-Dense Gap at Extreme Sparsity</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Rice University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只留top-k会丢掉尾部，均匀采样又可能浪费预算。SSA按代理分数分配确定保留和残差抽样预算，再用包含概率修正被选token，兼顾重要项与尾部覆盖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>强证据稳定保留，较弱证据仍有被抽到的机会，而非全部被硬截断。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28441v1">原论文</a> · <a href="../../../../foundation-models/2610.28441-stratified-sparse-attention/">实现解读</a> · <a href="#qa-4e03b2497b28be11">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:stratified-sparse-attention" data-paper-title="Stratified Sparse Attention: Reducing the Sparse-to-Dense Gap at Extreme Sparsity" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Stratified Sparse Attention: Reducing the Sparse-to-Dense Gap at Extreme Sparsity 基础模型 Rice University 2026-10-20 只保留 top-k 会丢掉尾部质量；均匀抽样又浪费预算。SSA先确定保留高概率项，再按残差代理分布抽样。关键不是“top-k加采样”的外形，而是有放回抽样后去重，按每个token至少出现一次的包含概率修正。论文的自适应 Algorithm 1 与实际优化内核的固定 heavy fraction 版本不同；本地实现前者，不冒充后者的速度。 完整实验标注成本过高，不复现（审查 DONE），不下载、不试跑、不自动重试。L1诊断不是正式能力比较，不参与Evolve晋级。stratified_sparse_attention 接受单query、keys、values和外部代理分数，真实执行water-filling、离散采样和精确选中项打分。梯度只通过实际选中Q/K/V；代理分配是detached离散步骤。没有声称实现PQCache代理、层级采样或paged KV runtime。  注意力与长上下文 稀疏注意力 基础模型 长上下文：注意力、递归状态与记忆 SSA有放回采样后先去重，为什么还要按“至少抽中一次”的概率修正？ 一个token可能在多次抽样中重复出现；去重后，它是否进入最终集合的概率不再等于单次抽样概率。SSA用包含概率一减一减p的m次方作修正，并让确定保留的重项概率为1。最终是自归一化比值估计，不能把这种修正继续夸成输出严格无偏。 教学例子：某token每次被抽中的概率为0.2，抽两次时至少出现一次的概率是0.36；去重只算一行时，应按0.36而不是0.2修正它的贡献。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-80e8ff6ac2401e91">SSA有放回采样后先去重，为什么还要按“至少抽中一次”的概率修正？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Astratified-sparse-attention">Stratified Sparse Attention: Reducing the Sparse-to-Dense Gap at Extreme Sparsity</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Rice University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一个token可能在多次抽样中重复出现；去重后，它是否进入最终集合的概率不再等于单次抽样概率。SSA用包含概率一减一减p的m次方作修正，并让确定保留的重项概率为1。最终是自归一化比值估计，不能把这种修正继续夸成输出严格无偏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某token每次被抽中的概率为0.2，抽两次时至少出现一次的概率是0.36；去重只算一行时，应按0.36而不是0.2修正它的贡献。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28441v1">原论文</a> · <a href="../../../../foundation-models/2610.28441-stratified-sparse-attention/">实现解读</a> · <a href="#qa-80e8ff6ac2401e91">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:stratified-sparse-attention" data-paper-title="Stratified Sparse Attention: Reducing the Sparse-to-Dense Gap at Extreme Sparsity" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Stratified Sparse Attention: Reducing the Sparse-to-Dense Gap at Extreme Sparsity 基础模型 Rice University 2026-10-20 只保留 top-k 会丢掉尾部质量；均匀抽样又浪费预算。SSA先确定保留高概率项，再按残差代理分布抽样。关键不是“top-k加采样”的外形，而是有放回抽样后去重，按每个token至少出现一次的包含概率修正。论文的自适应 Algorithm 1 与实际优化内核的固定 heavy fraction 版本不同；本地实现前者，不冒充后者的速度。 完整实验标注成本过高，不复现（审查 DONE），不下载、不试跑、不自动重试。L1诊断不是正式能力比较，不参与Evolve晋级。stratified_sparse_attention 接受单query、keys、values和外部代理分数，真实执行water-filling、离散采样和精确选中项打分。梯度只通过实际选中Q/K/V；代理分配是detached离散步骤。没有声称实现PQCache代理、层级采样或paged KV runtime。  注意力与长上下文 稀疏注意力 基础模型 长上下文：注意力、递归状态与记忆 有放回抽样后去重，为什么不能再直接用 1/p_i 修正？ 去重后每个token最多参与一次，相关概率是至少被抽到一次的π_i=1-(1-p_i)^m，而不是单次抽样概率p_i。分子分母再取比值仍是self-normalized估计，不能宣称严格无偏。 示意：同一token抽中三次后只保留一行，不能既去重又按三次独立样本的口径计权。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-53b2ad3285caf307">有放回抽样后去重，为什么不能再直接用 1/p_i 修正？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Astratified-sparse-attention">Stratified Sparse Attention: Reducing the Sparse-to-Dense Gap at Extreme Sparsity</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Rice University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>去重后每个token最多参与一次，相关概率是至少被抽到一次的π_i=1-(1-p_i)^m，而不是单次抽样概率p_i。分子分母再取比值仍是self-normalized估计，不能宣称严格无偏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一token抽中三次后只保留一行，不能既去重又按三次独立样本的口径计权。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28441v1">原论文</a> · <a href="../../../../foundation-models/2610.28441-stratified-sparse-attention/">实现解读</a> · <a href="#qa-53b2ad3285caf307">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:stratified-sparse-attention" data-paper-title="Stratified Sparse Attention: Reducing the Sparse-to-Dense Gap at Extreme Sparsity" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Stratified Sparse Attention: Reducing the Sparse-to-Dense Gap at Extreme Sparsity 基础模型 Rice University 2026-10-20 只保留 top-k 会丢掉尾部质量；均匀抽样又浪费预算。SSA先确定保留高概率项，再按残差代理分布抽样。关键不是“top-k加采样”的外形，而是有放回抽样后去重，按每个token至少出现一次的包含概率修正。论文的自适应 Algorithm 1 与实际优化内核的固定 heavy fraction 版本不同；本地实现前者，不冒充后者的速度。 完整实验标注成本过高，不复现（审查 DONE），不下载、不试跑、不自动重试。L1诊断不是正式能力比较，不参与Evolve晋级。stratified_sparse_attention 接受单query、keys、values和外部代理分数，真实执行water-filling、离散采样和精确选中项打分。梯度只通过实际选中Q/K/V；代理分配是detached离散步骤。没有声称实现PQCache代理、层级采样或paged KV runtime。  注意力与长上下文 稀疏注意力 基础模型 长上下文：注意力、递归状态与记忆 SSA 怎样稳定计算很小的包含概率，并验证 full-budget 边界？ 文档使用-expm1(m·log1p(-p))避免直接相减的精度损失，再在log空间归一化；k=N时显式返回dense attention。代理分配是离散detached步骤，不能声称该处已获梯度。 示意：把预算设为全部key时，应与dense结果一致，而不再随机遗漏某个尾部token。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-04c938ddcf6c6174">SSA 怎样稳定计算很小的包含概率，并验证 full-budget 边界？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Astratified-sparse-attention">Stratified Sparse Attention: Reducing the Sparse-to-Dense Gap at Extreme Sparsity</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Rice University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档使用-expm1(m·log1p(-p))避免直接相减的精度损失，再在log空间归一化；k=N时显式返回dense attention。代理分配是离散detached步骤，不能声称该处已获梯度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把预算设为全部key时，应与dense结果一致，而不再随机遗漏某个尾部token。</p>
<p class="ar-learning-sources">依据：核心公式、验证与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28441v1">原论文</a> · <a href="../../../../foundation-models/2610.28441-stratified-sparse-attention/">实现解读</a> · <a href="#qa-04c938ddcf6c6174">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:kronlstm" data-paper-title="Kronecker Delta Rule for Long Context Linear Attention" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Kronecker Delta Rule for Long Context Linear Attention 基础模型 Johannes Kepler University Linz 2026-10-19 标准 DeltaNet 用向量误差更新矩阵记忆，会干扰与当前 key 重叠的其他关联。Kronecker Delta Rule 修正的是一个 key-value 对的标量关联；记忆修订沿的单一矩阵方向进行。KronLSTM 再加入 key 轴逐通道遗忘和分离 erase/write 门。 完整实验显著超出单张 A100/A30 或本地 Mac 的日常预算，成本过高，不复现（审查 DONE）。kronecker_update 保存标量关联擦除与 key 轴忘记；TinyKronLSTM 包含真实投影、短卷积、归一化、四类输入相关门、循环记忆和输出投影。它不是把普通 DeltaNet 换个名字，也不是仅记录配置。当前是 PyTorch 循环版，未实现论文 Appendix A8 的融合 chunkwise 前后向内核，不宣称相同吞吐量。  注意力与长上下文 线性注意力与递归记忆 基础模型 长上下文：注意力、递归状态与记忆 KronLSTM 把记忆中的哪个对象看成要修正的目标？ 它针对一个key-value对的标量关联vᵀSk进行修订，而不是直接要求整条预测向量都等于目标value。更新沿vkᵀ这一矩阵方向发生，再结合遗忘及擦写门。 示意：修正“某个key与某个value之间的关联强度”，不必把这一key下的所有value方向一并重写。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-kronlstm-ae88fcaa" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f0cf180efd09886f">KronLSTM 把记忆中的哪个对象看成要修正的目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Akronlstm">Kronecker Delta Rule for Long Context Linear Attention</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Johannes Kepler University Linz</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它针对一个key-value对的标量关联vᵀSk进行修订，而不是直接要求整条预测向量都等于目标value。更新沿vkᵀ这一矩阵方向发生，再结合遗忘及擦写门。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>修正“某个key与某个value之间的关联强度”，不必把这一key下的所有value方向一并重写。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.26834">原论文</a> · <a href="../../../../foundation-models/2610.26834-kronlstm/">实现解读</a> · <a href="#qa-f0cf180efd09886f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:kronlstm" data-paper-title="Kronecker Delta Rule for Long Context Linear Attention" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Kronecker Delta Rule for Long Context Linear Attention 基础模型 Johannes Kepler University Linz 2026-10-19 标准 DeltaNet 用向量误差更新矩阵记忆，会干扰与当前 key 重叠的其他关联。Kronecker Delta Rule 修正的是一个 key-value 对的标量关联；记忆修订沿的单一矩阵方向进行。KronLSTM 再加入 key 轴逐通道遗忘和分离 erase/write 门。 完整实验显著超出单张 A100/A30 或本地 Mac 的日常预算，成本过高，不复现（审查 DONE）。kronecker_update 保存标量关联擦除与 key 轴忘记；TinyKronLSTM 包含真实投影、短卷积、归一化、四类输入相关门、循环记忆和输出投影。它不是把普通 DeltaNet 换个名字，也不是仅记录配置。当前是 PyTorch 循环版，未实现论文 Appendix A8 的融合 chunkwise 前后向内核，不宣称相同吞吐量。  注意力与长上下文 线性注意力与递归记忆 基础模型 长上下文：注意力、递归状态与记忆 KronLSTM擦写的是整个value向量，还是一个key–value的标量关联？ Kronecker Delta Rule用v转置Sk衡量一个key与value方向的标量关联，沿vk转置这一矩阵方向擦写；它不同于直接用整段向量误差修改记忆。对另一个关联的干扰同时取决于key和value的重叠，任一方向正交都能阻断这次干扰。KronLSTM还分开遗忘、擦除与写入门，不能把写入系数误乘擦除门。 教学例子：两条关联使用相近的key，但value方向正交。沿第一条的vk转置更新时，第二条的标量关联不会因此被同样擦掉；这仍不保证所有后续写入都无干扰。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-a233b49ed9960b21">KronLSTM擦写的是整个value向量，还是一个key–value的标量关联？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Akronlstm">Kronecker Delta Rule for Long Context Linear Attention</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Johannes Kepler University Linz</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Kronecker Delta Rule用v转置Sk衡量一个key与value方向的标量关联，沿vk转置这一矩阵方向擦写；它不同于直接用整段向量误差修改记忆。对另一个关联的干扰同时取决于key和value的重叠，任一方向正交都能阻断这次干扰。KronLSTM还分开遗忘、擦除与写入门，不能把写入系数误乘擦除门。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两条关联使用相近的key，但value方向正交。沿第一条的vk转置更新时，第二条的标量关联不会因此被同样擦掉；这仍不保证所有后续写入都无干扰。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.26834">原论文</a> · <a href="../../../../foundation-models/2610.26834-kronlstm/">实现解读</a> · <a href="#qa-a233b49ed9960b21">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:kronlstm" data-paper-title="Kronecker Delta Rule for Long Context Linear Attention" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Kronecker Delta Rule for Long Context Linear Attention 基础模型 Johannes Kepler University Linz 2026-10-19 标准 DeltaNet 用向量误差更新矩阵记忆，会干扰与当前 key 重叠的其他关联。Kronecker Delta Rule 修正的是一个 key-value 对的标量关联；记忆修订沿的单一矩阵方向进行。KronLSTM 再加入 key 轴逐通道遗忘和分离 erase/write 门。 完整实验显著超出单张 A100/A30 或本地 Mac 的日常预算，成本过高，不复现（审查 DONE）。kronecker_update 保存标量关联擦除与 key 轴忘记；TinyKronLSTM 包含真实投影、短卷积、归一化、四类输入相关门、循环记忆和输出投影。它不是把普通 DeltaNet 换个名字，也不是仅记录配置。当前是 PyTorch 循环版，未实现论文 Appendix A8 的融合 chunkwise 前后向内核，不宣称相同吞吐量。  注意力与长上下文 线性注意力与递归记忆 基础模型 长上下文：注意力、递归状态与记忆 KronLSTM 与普通 DeltaNet 的误差对象不同，会怎样影响干扰分析？ 普通DeltaNet使用向量误差Sk-v；Kronecker规则使用标量误差vᵀSk-c。文档说明其他关联的扰动同时取决于key与value内积，其中一侧正交即可消除当前擦写干扰，但不保证任意长历史永不遗忘。 示意：两个key相似但value正交时，标量关联更新的干扰判断与只看key重叠不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-949d6d4b470021a6">KronLSTM 与普通 DeltaNet 的误差对象不同，会怎样影响干扰分析？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Akronlstm">Kronecker Delta Rule for Long Context Linear Attention</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Johannes Kepler University Linz</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>普通DeltaNet使用向量误差Sk-v；Kronecker规则使用标量误差vᵀSk-c。文档说明其他关联的扰动同时取决于key与value内积，其中一侧正交即可消除当前擦写干扰，但不保证任意长历史永不遗忘。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个key相似但value正交时，标量关联更新的干扰判断与只看key重叠不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.26834">原论文</a> · <a href="../../../../foundation-models/2610.26834-kronlstm/">实现解读</a> · <a href="#qa-949d6d4b470021a6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:kronlstm" data-paper-title="Kronecker Delta Rule for Long Context Linear Attention" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Kronecker Delta Rule for Long Context Linear Attention 基础模型 Johannes Kepler University Linz 2026-10-19 标准 DeltaNet 用向量误差更新矩阵记忆，会干扰与当前 key 重叠的其他关联。Kronecker Delta Rule 修正的是一个 key-value 对的标量关联；记忆修订沿的单一矩阵方向进行。KronLSTM 再加入 key 轴逐通道遗忘和分离 erase/write 门。 完整实验显著超出单张 A100/A30 或本地 Mac 的日常预算，成本过高，不复现（审查 DONE）。kronecker_update 保存标量关联擦除与 key 轴忘记；TinyKronLSTM 包含真实投影、短卷积、归一化、四类输入相关门、循环记忆和输出投影。它不是把普通 DeltaNet 换个名字，也不是仅记录配置。当前是 PyTorch 循环版，未实现论文 Appendix A8 的融合 chunkwise 前后向内核，不宣称相同吞吐量。  注意力与长上下文 线性注意力与递归记忆 基础模型 长上下文：注意力、递归状态与记忆 KronLSTM 的遗忘乘法方向和 write 系数，为什么不能照搬普通 delta update？ 文档中的遗忘在右侧作用于key轴，解耦写入项是c·vkᵀ，而非βc·vkᵀ；擦除项才使用β。改错任何一项都会改变更新式，应对照独立vec参考，而非只检查loss是否下降。 示意：把β设得很小并不应顺带把独立write门c的写入也压小。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b32ff25fb71361e2">KronLSTM 的遗忘乘法方向和 write 系数，为什么不能照搬普通 delta update？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Akronlstm">Kronecker Delta Rule for Long Context Linear Attention</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Johannes Kepler University Linz</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档中的遗忘在右侧作用于key轴，解耦写入项是c·vkᵀ，而非βc·vkᵀ；擦除项才使用β。改错任何一项都会改变更新式，应对照独立vec参考，而非只检查loss是否下降。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把β设得很小并不应顺带把独立write门c的写入也压小。</p>
<p class="ar-learning-sources">依据：核心公式、实现与运行；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.26834">原论文</a> · <a href="../../../../foundation-models/2610.26834-kronlstm/">实现解读</a> · <a href="#qa-b32ff25fb71361e2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:memory-mosaics-plus" data-paper-title="Open-world AI: a Tale of Three Requirements" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Open-world AI: a Tale of Three Requirements 基础模型 FAIR, Meta 2026-10-14 固定任务的 IID 泛化不等于在开放世界中学习新任务。论文提出推理时学习、丰富表示和预测性解耦三个要求。§3.2 的 Mosaics+ 用短期模块先处理近期依赖，再以 Gaussian-kernel 长期记忆检索预测关联；two-stage 版本分别估计当前任务与相关任务，避免一锅混池让不相关历史越多越有害。 单张 A100/A30 不适合完整多臂训练，成本过高，不复现（审查 DONE）。完整逐 seed 数据见诊断指标和GPU 回执。不下载公开语料或 checkpoint。固定程序化 revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1，seeds42/43/44；每个 seed 使用2条8-token、16维随机输入和明确文档边界。短窗2、skip1 是缩小的算子配置，不等于原文256/64设定。随机目标只用于确认训练路径，不是任务测试答案。  网络架构 关联记忆与推理时学习 基础模型 长上下文：注意力、递归状态与记忆 Memory Mosaics+ 为什么强调推理时学习新任务，而不只看 IID 测试？ 固定训练分布上的测试无法充分说明模型怎样利用新出现的任务经验。Mosaics+把近期依赖和长期关联检索结合，使推理过程能从已有上下文中的预测关联组织新任务证据。 示意：模型面对一个新的输入输出规则时，可利用刚观察到的关联，而不只重复旧任务统计。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-memory-mosaics-plus-a2cfe6c3" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6ed9deb0553b2192">Memory Mosaics+ 为什么强调推理时学习新任务，而不只看 IID 测试？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amemory-mosaics-plus">Open-world AI: a Tale of Three Requirements</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR, Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定训练分布上的测试无法充分说明模型怎样利用新出现的任务经验。Mosaics+把近期依赖和长期关联检索结合，使推理过程能从已有上下文中的预测关联组织新任务证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型面对一个新的输入输出规则时，可利用刚观察到的关联，而不只重复旧任务统计。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20782">原论文</a> · <a href="../../../../foundation-models/2610.20782-memory-mosaics-plus/">实现解读</a> · <a href="#qa-6ed9deb0553b2192">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:memory-mosaics-plus" data-paper-title="Open-world AI: a Tale of Three Requirements" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Open-world AI: a Tale of Three Requirements 基础模型 FAIR, Meta 2026-10-14 固定任务的 IID 泛化不等于在开放世界中学习新任务。论文提出推理时学习、丰富表示和预测性解耦三个要求。§3.2 的 Mosaics+ 用短期模块先处理近期依赖，再以 Gaussian-kernel 长期记忆检索预测关联；two-stage 版本分别估计当前任务与相关任务，避免一锅混池让不相关历史越多越有害。 单张 A100/A30 不适合完整多臂训练，成本过高，不复现（审查 DONE）。完整逐 seed 数据见诊断指标和GPU 回执。不下载公开语料或 checkpoint。固定程序化 revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1，seeds42/43/44；每个 seed 使用2条8-token、16维随机输入和明确文档边界。短窗2、skip1 是缩小的算子配置，不等于原文256/64设定。随机目标只用于确认训练路径，不是任务测试答案。  网络架构 关联记忆与推理时学习 基础模型 长上下文：注意力、递归状态与记忆 Mosaics+为何分别归一化当前任务和相关任务记忆，不能直接混成一个softmax？ 把两类记忆混池后，它们会在同一个分母中竞争；数量很多但无关的旧任务可能稀释当前任务证据。two-stage路径分别求两类记忆的归一化预测，再合并结果，使证据来源保持可分。短期模块负责近期依赖，长期记忆保存预测关联；读取也要跳过不合法的未来位置。 教学例子：当前文档只有3条有用关联，历史库却有1000条其他任务记录。混池可能让后者挤占权重；分开归一化后，当前文档的预测不会仅因旧记录数量增长而被同样稀释。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-b087fe5457f11f79">Mosaics+为何分别归一化当前任务和相关任务记忆，不能直接混成一个softmax？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amemory-mosaics-plus">Open-world AI: a Tale of Three Requirements</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR, Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>把两类记忆混池后，它们会在同一个分母中竞争；数量很多但无关的旧任务可能稀释当前任务证据。two-stage路径分别求两类记忆的归一化预测，再合并结果，使证据来源保持可分。短期模块负责近期依赖，长期记忆保存预测关联；读取也要跳过不合法的未来位置。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>当前文档只有3条有用关联，历史库却有1000条其他任务记录。混池可能让后者挤占权重；分开归一化后，当前文档的预测不会仅因旧记录数量增长而被同样稀释。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20782">原论文</a> · <a href="../../../../foundation-models/2610.20782-memory-mosaics-plus/">实现解读</a> · <a href="#qa-b087fe5457f11f79">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:memory-mosaics-plus" data-paper-title="Open-world AI: a Tale of Three Requirements" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Open-world AI: a Tale of Three Requirements 基础模型 FAIR, Meta 2026-10-14 固定任务的 IID 泛化不等于在开放世界中学习新任务。论文提出推理时学习、丰富表示和预测性解耦三个要求。§3.2 的 Mosaics+ 用短期模块先处理近期依赖，再以 Gaussian-kernel 长期记忆检索预测关联；two-stage 版本分别估计当前任务与相关任务，避免一锅混池让不相关历史越多越有害。 单张 A100/A30 不适合完整多臂训练，成本过高，不复现（审查 DONE）。完整逐 seed 数据见诊断指标和GPU 回执。不下载公开语料或 checkpoint。固定程序化 revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1，seeds42/43/44；每个 seed 使用2条8-token、16维随机输入和明确文档边界。短窗2、skip1 是缩小的算子配置，不等于原文256/64设定。随机目标只用于确认训练路径，不是任务测试答案。  网络架构 关联记忆与推理时学习 基础模型 长上下文：注意力、递归状态与记忆 Mosaics+ 的 two-stage 检索，与把当前任务和历史任务放进一个 softmax 池有什么区别？ two-stage分别归一化当前任务与相关历史任务，再合并估计。单一混池中，历史条数增多会改变当前任务的相对权重，即使新历史并不相关；两个计算并不等价。 示意：加入很多旧任务样本，不应仅凭数量就淹没当前文档里少量但关键的关联。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-68e8c0c69a84e1cc">Mosaics+ 的 two-stage 检索，与把当前任务和历史任务放进一个 softmax 池有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amemory-mosaics-plus">Open-world AI: a Tale of Three Requirements</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR, Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>two-stage分别归一化当前任务与相关历史任务，再合并估计。单一混池中，历史条数增多会改变当前任务的相对权重，即使新历史并不相关；两个计算并不等价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>加入很多旧任务样本，不应仅凭数量就淹没当前文档里少量但关键的关联。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20782">原论文</a> · <a href="../../../../foundation-models/2610.20782-memory-mosaics-plus/">实现解读</a> · <a href="#qa-68e8c0c69a84e1cc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:memory-mosaics-plus" data-paper-title="Open-world AI: a Tale of Three Requirements" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Open-world AI: a Tale of Three Requirements 基础模型 FAIR, Meta 2026-10-14 固定任务的 IID 泛化不等于在开放世界中学习新任务。论文提出推理时学习、丰富表示和预测性解耦三个要求。§3.2 的 Mosaics+ 用短期模块先处理近期依赖，再以 Gaussian-kernel 长期记忆检索预测关联；two-stage 版本分别估计当前任务与相关任务，避免一锅混池让不相关历史越多越有害。 单张 A100/A30 不适合完整多臂训练，成本过高，不复现（审查 DONE）。完整逐 seed 数据见诊断指标和GPU 回执。不下载公开语料或 checkpoint。固定程序化 revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1，seeds42/43/44；每个 seed 使用2条8-token、16维随机输入和明确文档边界。短窗2、skip1 是缩小的算子配置，不等于原文256/64设定。随机目标只用于确认训练路径，不是任务测试答案。  网络架构 关联记忆与推理时学习 基础模型 长上下文：注意力、递归状态与记忆 预测 value 用到 i+1 的信息时，怎样避免当前查询读取未来？ 读取范围限制为i≤t-s且s≥1，因而value涉及的i+1不超过当前可见边界。还需按文档边界拆开两次归一化，并处理空记忆；文档中的独立循环与未来扰动是重要负对照。 示意：skip=1时最多读取i=t-1的关联，其预测value可涉及t，但不能读取t+1。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-eff87d4df2d3102d">预测 value 用到 i+1 的信息时，怎样避免当前查询读取未来？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amemory-mosaics-plus">Open-world AI: a Tale of Three Requirements</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR, Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>读取范围限制为i≤t-s且s≥1，因而value涉及的i+1不超过当前可见边界。还需按文档边界拆开两次归一化，并处理空记忆；文档中的独立循环与未来扰动是重要负对照。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>skip=1时最多读取i=t-1的关联，其预测value可涉及t，但不能读取t+1。</p>
<p class="ar-learning-sources">依据：核心公式、结果与独立对照；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20782">原论文</a> · <a href="../../../../foundation-models/2610.20782-memory-mosaics-plus/">实现解读</a> · <a href="#qa-eff87d4df2d3102d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:oal" data-paper-title="Not All Dimensions Are Equal: Outlier-Aware Attention Linearization with Grouped Quadratic Kernels" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Not All Dimensions Are Equal: Outlier-Aware Attention Linearization with Grouped Quadratic Kernels 基础模型 The Chinese University of Hong Kong, Shenzhen 2026-10-09 预训练 attention 的 QK 各维度贡献不均匀，少量高贡献坐标包含较多 softmax 近似误差。OAL 先在 post-RoPE QK 上计算因果贡献，以 prompt bootstrap 识别高贡献尾部的稳定边界；随后学习共享组和组对系数的二次核。正半定参数化保证分母严格正，并用真实 attention 输出 MSE 校准，而不是仅拟合 attention 权重。校准之后保留前后 softmax 层，对中间层进行转换，并在所有层的 q/k/v/o 上做 LoRA，联合训练核系数。 小规模诊断不作稳定提升声明，相对原文效果百分比不适用。cpu-contracts.json记录已重跑的 5 个测试：因果贡献公式、bootstrap/无人工组数上限、正核与 dense/HD 等价、输出校准梯度、实际 Qwen 模块转换与 LoRA 梯度。每项先固定 seed 42，递推等价/校准专用用例内部使用 seed 11/2；不是独立多 seed 能力实验。没有 CPU 单测到 A100 完成的自动晋级。core_mechanism / L1：保留 QK 分组、正核、真实输出校准和真实 Base checkpoint 的 LoRA 联合更新。小 batch 训练使用精确 dense kernel；  推理与系统效率 注意力线性化 基础模型 长上下文：注意力、递归状态与记忆 OAL 为什么专门关注 post-RoPE QK 中贡献较大的坐标？ 不同坐标对匹配分数的贡献不均匀，高贡献尾部可能主导softmax近似误差。OAL据此分组并学习正二次核，用更有针对性的表示替代统一处理全部坐标。 示意：少数坐标贡献了大部分匹配变化，分组近似不应把它们与低贡献坐标一视同仁。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-oal-9fb61fc3" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e990ea924ac5ed7a">OAL 为什么专门关注 post-RoPE QK 中贡献较大的坐标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aoal">Not All Dimensions Are Equal: Outlier-Aware Attention Linearization with Grouped Quadratic Kernels</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong, Shenzhen</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同坐标对匹配分数的贡献不均匀，高贡献尾部可能主导softmax近似误差。OAL据此分组并学习正二次核，用更有针对性的表示替代统一处理全部坐标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>少数坐标贡献了大部分匹配变化，分组近似不应把它们与低贡献坐标一视同仁。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13674">原论文</a> · <a href="../../../../reproductions/2610.13674-oal/">实现解读</a> · <a href="#qa-e990ea924ac5ed7a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:oal" data-paper-title="Not All Dimensions Are Equal: Outlier-Aware Attention Linearization with Grouped Quadratic Kernels" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Not All Dimensions Are Equal: Outlier-Aware Attention Linearization with Grouped Quadratic Kernels 基础模型 The Chinese University of Hong Kong, Shenzhen 2026-10-09 预训练 attention 的 QK 各维度贡献不均匀，少量高贡献坐标包含较多 softmax 近似误差。OAL 先在 post-RoPE QK 上计算因果贡献，以 prompt bootstrap 识别高贡献尾部的稳定边界；随后学习共享组和组对系数的二次核。正半定参数化保证分母严格正，并用真实 attention 输出 MSE 校准，而不是仅拟合 attention 权重。校准之后保留前后 softmax 层，对中间层进行转换，并在所有层的 q/k/v/o 上做 LoRA，联合训练核系数。 小规模诊断不作稳定提升声明，相对原文效果百分比不适用。cpu-contracts.json记录已重跑的 5 个测试：因果贡献公式、bootstrap/无人工组数上限、正核与 dense/HD 等价、输出校准梯度、实际 Qwen 模块转换与 LoRA 梯度。每项先固定 seed 42，递推等价/校准专用用例内部使用 seed 11/2；不是独立多 seed 能力实验。没有 CPU 单测到 A100 完成的自动晋级。core_mechanism / L1：保留 QK 分组、正核、真实输出校准和真实 Base checkpoint 的 LoRA 联合更新。小 batch 训练使用精确 dense kernel；  推理与系统效率 注意力线性化 基础模型 长上下文：注意力、递归状态与记忆 OAL为什么按QK维度贡献分组，还要用attention输出误差校准二次核？ 少数坐标可能主导softmax近似误差，统一处理所有维度会浪费近似能力。OAL先在post-RoPE空间识别稳定贡献分组，再学习共享组与组对的正定二次核。校准对齐最终聚合输出，而不只是权重，因为相同权重误差乘上不同value会产生不同后果；正定约束也保护归一化分母。 教学例子：两个注意力近似都错了相同权重，但一处value很大、另一处value几乎相同，输出影响不同。应比较最终读出的向量，而不只看权重图接近程度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-5ef7344fcef7af22">OAL为什么按QK维度贡献分组，还要用attention输出误差校准二次核？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aoal">Not All Dimensions Are Equal: Outlier-Aware Attention Linearization with Grouped Quadratic Kernels</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong, Shenzhen</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>少数坐标可能主导softmax近似误差，统一处理所有维度会浪费近似能力。OAL先在post-RoPE空间识别稳定贡献分组，再学习共享组与组对的正定二次核。校准对齐最终聚合输出，而不只是权重，因为相同权重误差乘上不同value会产生不同后果；正定约束也保护归一化分母。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个注意力近似都错了相同权重，但一处value很大、另一处value几乎相同，输出影响不同。应比较最终读出的向量，而不只看权重图接近程度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13674">原论文</a> · <a href="../../../../reproductions/2610.13674-oal/">实现解读</a> · <a href="#qa-5ef7344fcef7af22">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:oal" data-paper-title="Not All Dimensions Are Equal: Outlier-Aware Attention Linearization with Grouped Quadratic Kernels" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Not All Dimensions Are Equal: Outlier-Aware Attention Linearization with Grouped Quadratic Kernels 基础模型 The Chinese University of Hong Kong, Shenzhen 2026-10-09 预训练 attention 的 QK 各维度贡献不均匀，少量高贡献坐标包含较多 softmax 近似误差。OAL 先在 post-RoPE QK 上计算因果贡献，以 prompt bootstrap 识别高贡献尾部的稳定边界；随后学习共享组和组对系数的二次核。正半定参数化保证分母严格正，并用真实 attention 输出 MSE 校准，而不是仅拟合 attention 权重。校准之后保留前后 softmax 层，对中间层进行转换，并在所有层的 q/k/v/o 上做 LoRA，联合训练核系数。 小规模诊断不作稳定提升声明，相对原文效果百分比不适用。cpu-contracts.json记录已重跑的 5 个测试：因果贡献公式、bootstrap/无人工组数上限、正核与 dense/HD 等价、输出校准梯度、实际 Qwen 模块转换与 LoRA 梯度。每项先固定 seed 42，递推等价/校准专用用例内部使用 seed 11/2；不是独立多 seed 能力实验。没有 CPU 单测到 A100 完成的自动晋级。core_mechanism / L1：保留 QK 分组、正核、真实输出校准和真实 Base checkpoint 的 LoRA 联合更新。小 batch 训练使用精确 dense kernel；  推理与系统效率 注意力线性化 基础模型 长上下文：注意力、递归状态与记忆 OAL 校准 attention 输出 MSE，与只拟合 attention 权重有什么区别？ 输出还取决于V以及归一化后的加权和；权重误差相同，造成的输出误差可能不同。OAL用真实输出MSE校准核，优化的是读出行为，而非单独复制一张权重矩阵。 示意：两处权重交换若对应相同value，输出可能不变；对应相反value时影响就很大。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b02978e4ca43559d">OAL 校准 attention 输出 MSE，与只拟合 attention 权重有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aoal">Not All Dimensions Are Equal: Outlier-Aware Attention Linearization with Grouped Quadratic Kernels</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong, Shenzhen</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>输出还取决于V以及归一化后的加权和；权重误差相同，造成的输出误差可能不同。OAL用真实输出MSE校准核，优化的是读出行为，而非单独复制一张权重矩阵。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两处权重交换若对应相同value，输出可能不变；对应相反value时影响就很大。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13674">原论文</a> · <a href="../../../../reproductions/2610.13674-oal/">实现解读</a> · <a href="#qa-b02978e4ca43559d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:oal" data-paper-title="Not All Dimensions Are Equal: Outlier-Aware Attention Linearization with Grouped Quadratic Kernels" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Not All Dimensions Are Equal: Outlier-Aware Attention Linearization with Grouped Quadratic Kernels 基础模型 The Chinese University of Hong Kong, Shenzhen 2026-10-09 预训练 attention 的 QK 各维度贡献不均匀，少量高贡献坐标包含较多 softmax 近似误差。OAL 先在 post-RoPE QK 上计算因果贡献，以 prompt bootstrap 识别高贡献尾部的稳定边界；随后学习共享组和组对系数的二次核。正半定参数化保证分母严格正，并用真实 attention 输出 MSE 校准，而不是仅拟合 attention 权重。校准之后保留前后 softmax 层，对中间层进行转换，并在所有层的 q/k/v/o 上做 LoRA，联合训练核系数。 小规模诊断不作稳定提升声明，相对原文效果百分比不适用。cpu-contracts.json记录已重跑的 5 个测试：因果贡献公式、bootstrap/无人工组数上限、正核与 dense/HD 等价、输出校准梯度、实际 Qwen 模块转换与 LoRA 梯度。每项先固定 seed 42，递推等价/校准专用用例内部使用 seed 11/2；不是独立多 seed 能力实验。没有 CPU 单测到 A100 完成的自动晋级。core_mechanism / L1：保留 QK 分组、正核、真实输出校准和真实 Base checkpoint 的 LoRA 联合更新。小 batch 训练使用精确 dense kernel；  推理与系统效率 注意力线性化 基础模型 长上下文：注意力、递归状态与记忆 OAL 的分组、校准与初始化选择，哪些可以使用 test 数据？ 都不应使用test来选。文档把train分块用于分组、输出校准及LoRA，validation选择核初始化和checkpoint，最后才读取test。正核参数化中的ε也需保留，保证归一化分母为正。 示意：某个核在test上最好，不能回头用它替换validation选出的核再报告同一test成绩。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-eb26be760a2e1b53">OAL 的分组、校准与初始化选择，哪些可以使用 test 数据？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aoal">Not All Dimensions Are Equal: Outlier-Aware Attention Linearization with Grouped Quadratic Kernels</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong, Shenzhen</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>都不应使用test来选。文档把train分块用于分组、输出校准及LoRA，validation选择核初始化和checkpoint，最后才读取test。正核参数化中的ε也需保留，保证归一化分母为正。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某个核在test上最好，不能回头用它替换validation选出的核再报告同一test成绩。</p>
<p class="ar-learning-sources">依据：核心公式、数据协议；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13674">原论文</a> · <a href="../../../../reproductions/2610.13674-oal/">实现解读</a> · <a href="#qa-eb26be760a2e1b53">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:orthros" data-paper-title="Orthros: Phase-Aware Heterogeneous Attention for Efficient Transformers" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Orthros: Phase-Aware Heterogeneous Attention for Efficient Transformers 基础模型 The Hong Kong Polytechnic University 2026-10-09 长 prompt、短回答的推理中，prefill 与 decode 的计算角色不同。Orthros 保留两个 token 流：base tokens 对所有位置执行固定窗口 SWA，并构建完整的逐层 KV；output-specific tokens 只在需预测输出的位置出现，用共享 KV 做全历史 causal cross-attention。FFN、norm 和主要 Q/K/V/O 权重共享，但两种 query 各有可学习 affine 变换。 单seed/短序列结果仅L1，不复现论文21.9×、长上下文能力或生产吞吐。本地对照口径：共享小型预训练起点继续训练的Transformer为基线，转换并真实适配的Orthros为实验组；论文吞吐相对收益不适用，本地只报告固定预算NLL与cached/batch一致性。  llm-architecture efficient-attention long-context 基础模型 长上下文：注意力、递归状态与记忆 Orthros 为什么区分 base tokens 和 output-specific tokens？ prefill中的大多数位置只需构建缓存，真正产生输出的位置才需要全局检索。base流做固定窗口计算并维护完整KV，输出流在需要预测的位置读取这些共享KV。 示意：输入一篇长文时，不必让每个prompt位置都走输出流的全历史检索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-orthros-ce7b4e60" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7c10d95f900154d7">Orthros 为什么区分 base tokens 和 output-specific tokens？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aorthros">Orthros: Phase-Aware Heterogeneous Attention for Efficient Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hong Kong Polytechnic University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>prefill中的大多数位置只需构建缓存，真正产生输出的位置才需要全局检索。base流做固定窗口计算并维护完整KV，输出流在需要预测的位置读取这些共享KV。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>输入一篇长文时，不必让每个prompt位置都走输出流的全历史检索。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13735">原论文</a> · <a href="../../../../reproductions/2610.13735-orthros/">实现解读</a> · <a href="#qa-7c10d95f900154d7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:orthros" data-paper-title="Orthros: Phase-Aware Heterogeneous Attention for Efficient Transformers" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Orthros: Phase-Aware Heterogeneous Attention for Efficient Transformers 基础模型 The Hong Kong Polytechnic University 2026-10-09 长 prompt、短回答的推理中，prefill 与 decode 的计算角色不同。Orthros 保留两个 token 流：base tokens 对所有位置执行固定窗口 SWA，并构建完整的逐层 KV；output-specific tokens 只在需预测输出的位置出现，用共享 KV 做全历史 causal cross-attention。FFN、norm 和主要 Q/K/V/O 权重共享，但两种 query 各有可学习 affine 变换。 单seed/短序列结果仅L1，不复现论文21.9×、长上下文能力或生产吞吐。本地对照口径：共享小型预训练起点继续训练的Transformer为基线，转换并真实适配的Orthros为实验组；论文吞吐相对收益不适用，本地只报告固定预算NLL与cached/batch一致性。  llm-architecture efficient-attention long-context 基础模型 长上下文：注意力、递归状态与记忆 Orthros的prefill使用局部窗口，为什么decode还能够检索完整历史？ base流在每个位置执行滑窗注意力，但仍构建并保留全部逐层KV；只有需要预测输出的位置另开output-specific流，读取共享的全历史KV。输出流不写入KV。这里线性prefill指固定窗口下的计算规模，不是把历史换成线性attention状态，也不意味着完整缓存成本消失。 教学例子：长文档prefill时每个base位置只读邻近词，最后一个提示位置复制出输出查询去全局取证；开始回答后，每个新输出位置都可再次检索已保存的历史。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-d753314406f18da1">Orthros的prefill使用局部窗口，为什么decode还能够检索完整历史？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aorthros">Orthros: Phase-Aware Heterogeneous Attention for Efficient Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hong Kong Polytechnic University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>base流在每个位置执行滑窗注意力，但仍构建并保留全部逐层KV；只有需要预测输出的位置另开output-specific流，读取共享的全历史KV。输出流不写入KV。这里线性prefill指固定窗口下的计算规模，不是把历史换成线性attention状态，也不意味着完整缓存成本消失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>长文档prefill时每个base位置只读邻近词，最后一个提示位置复制出输出查询去全局取证；开始回答后，每个新输出位置都可再次检索已保存的历史。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13735">原论文</a> · <a href="../../../../reproductions/2610.13735-orthros/">实现解读</a> · <a href="#qa-d753314406f18da1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:orthros" data-paper-title="Orthros: Phase-Aware Heterogeneous Attention for Efficient Transformers" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Orthros: Phase-Aware Heterogeneous Attention for Efficient Transformers 基础模型 The Hong Kong Polytechnic University 2026-10-09 长 prompt、短回答的推理中，prefill 与 decode 的计算角色不同。Orthros 保留两个 token 流：base tokens 对所有位置执行固定窗口 SWA，并构建完整的逐层 KV；output-specific tokens 只在需预测输出的位置出现，用共享 KV 做全历史 causal cross-attention。FFN、norm 和主要 Q/K/V/O 权重共享，但两种 query 各有可学习 affine 变换。 单seed/短序列结果仅L1，不复现论文21.9×、长上下文能力或生产吞吐。本地对照口径：共享小型预训练起点继续训练的Transformer为基线，转换并真实适配的Orthros为实验组；论文吞吐相对收益不适用，本地只报告固定预算NLL与cached/batch一致性。  llm-architecture efficient-attention long-context 基础模型 长上下文：注意力、递归状态与记忆 Orthros 的“线性 prefill”与 kernelized linear attention 是一回事吗？ 不是。这里base流使用固定窗口SWA形成O(Tw)计算，输出流仍可对完整KV做普通causal cross-attention；它没有把全历史压成核化递归状态，也没有因局部读取而删除旧KV。 示意：文首KV仍保留，只是大多数prefill位置不执行全历史读取。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e8cd696712fa94f4">Orthros 的“线性 prefill”与 kernelized linear attention 是一回事吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aorthros">Orthros: Phase-Aware Heterogeneous Attention for Efficient Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hong Kong Polytechnic University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。这里base流使用固定窗口SWA形成O(Tw)计算，输出流仍可对完整KV做普通causal cross-attention；它没有把全历史压成核化递归状态，也没有因局部读取而删除旧KV。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>文首KV仍保留，只是大多数prefill位置不执行全历史读取。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13735">原论文</a> · <a href="../../../../reproductions/2610.13735-orthros/">实现解读</a> · <a href="#qa-e8cd696712fa94f4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:orthros" data-paper-title="Orthros: Phase-Aware Heterogeneous Attention for Efficient Transformers" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Orthros: Phase-Aware Heterogeneous Attention for Efficient Transformers 基础模型 The Hong Kong Polytechnic University 2026-10-09 长 prompt、短回答的推理中，prefill 与 decode 的计算角色不同。Orthros 保留两个 token 流：base tokens 对所有位置执行固定窗口 SWA，并构建完整的逐层 KV；output-specific tokens 只在需预测输出的位置出现，用共享 KV 做全历史 causal cross-attention。FFN、norm 和主要 Q/K/V/O 权重共享，但两种 query 各有可学习 affine 变换。 单seed/短序列结果仅L1，不复现论文21.9×、长上下文能力或生产吞吐。本地对照口径：共享小型预训练起点继续训练的Transformer为基线，转换并真实适配的Orthros为实验组；论文吞吐相对收益不适用，本地只报告固定预算NLL与cached/batch一致性。  llm-architecture efficient-attention long-context 基础模型 长上下文：注意力、递归状态与记忆 Orthros 的 output stream 也应把自己的 K/V 追加进共享缓存吗？ 不应。文档明确同层KV只来自base流，output流负责查询；两种query使用共享投影及各自affine。让输出流写KV会改变缓存含义，并可能破坏batch与cached decode的一致性。 示意：每个decode步只追加一份base KV，而不是把同一个token的两条流都存进去。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7da10ef89316529a">Orthros 的 output stream 也应把自己的 K/V 追加进共享缓存吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aorthros">Orthros: Phase-Aware Heterogeneous Attention for Efficient Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hong Kong Polytechnic University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不应。文档明确同层KV只来自base流，output流负责查询；两种query使用共享投影及各自affine。让输出流写KV会改变缓存含义，并可能破坏batch与cached decode的一致性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>每个decode步只追加一份base KV，而不是把同一个token的两条流都存进去。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13735">原论文</a> · <a href="../../../../reproductions/2610.13735-orthros/">实现解读</a> · <a href="#qa-7da10ef89316529a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:rea" data-paper-title="Role-aware Heuristic Episodic Attention for Conversational LLMs" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Role-aware Heuristic Episodic Attention for Conversational LLMs 基础模型 原文首页未列第一作者机构 2026-10-01 把全局指令放入持久前缀，把多轮交互放入 episodic memory；检索时按角色决定保留原文、压缩表示或省略。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行角色分离与 episodic top-k；不调用压缩 LLM。执行角色分离与 episodic top-k；不调用压缩 LLM。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  长上下文 会话记忆 注意力 基础模型 长上下文：注意力、递归状态与记忆 REA 为什么不把系统指令与所有聊天历史一起做 top-k？ 全局指令需要持续约束后续交互，而普通历史可按相关性检索。REA把指令放在持久前缀，交互放在episodic memory，再按角色决定保留、压缩或省略方式。 示意：一条长期格式要求不应仅因与当前关键词不相似就被历史检索淘汰。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-rea-ef53c923" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5d6cddee4d267173">REA 为什么不把系统指令与所有聊天历史一起做 top-k？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Area">Role-aware Heuristic Episodic Attention for Conversational LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全局指令需要持续约束后续交互，而普通历史可按相关性检索。REA把指令放在持久前缀，交互放在episodic memory，再按角色决定保留、压缩或省略方式。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一条长期格式要求不应仅因与当前关键词不相似就被历史检索淘汰。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00958">原论文</a> · <a href="../../../../foundation-models/2610.00958-rea/">实现解读</a> · <a href="#qa-5d6cddee4d267173">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:rea" data-paper-title="Role-aware Heuristic Episodic Attention for Conversational LLMs" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Role-aware Heuristic Episodic Attention for Conversational LLMs 基础模型 原文首页未列第一作者机构 2026-10-01 把全局指令放入持久前缀，把多轮交互放入 episodic memory；检索时按角色决定保留原文、压缩表示或省略。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行角色分离与 episodic top-k；不调用压缩 LLM。执行角色分离与 episodic top-k；不调用压缩 LLM。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  长上下文 会话记忆 注意力 基础模型 长上下文：注意力、递归状态与记忆 REA为何把全局指令保留为持久前缀，而不让它与聊天片段一起按相关性竞争？ 聊天记忆的某次相关性排序不应顺便删除持续有效的全局约束。REA把持久指令和情节记忆分开，对后者检索，并按角色决定保留原文、压缩或省略。它控制的是构成当前上下文的材料，而不是保证压缩后所有信息都可恢复；角色和检索规则仍需核验。 教学例子：用户早先规定输出必须用中文，最近谈论电影；电影片段可按问题相关性选择，而中文约束不应只因和电影关键词无关就被挤出上下文。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-958b8fd9fb9bf5ff">REA为何把全局指令保留为持久前缀，而不让它与聊天片段一起按相关性竞争？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Area">Role-aware Heuristic Episodic Attention for Conversational LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>聊天记忆的某次相关性排序不应顺便删除持续有效的全局约束。REA把持久指令和情节记忆分开，对后者检索，并按角色决定保留原文、压缩或省略。它控制的是构成当前上下文的材料，而不是保证压缩后所有信息都可恢复；角色和检索规则仍需核验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户早先规定输出必须用中文，最近谈论电影；电影片段可按问题相关性选择，而中文约束不应只因和电影关键词无关就被挤出上下文。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00958">原论文</a> · <a href="../../../../foundation-models/2610.00958-rea/">实现解读</a> · <a href="#qa-958b8fd9fb9bf5ff">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:rea" data-paper-title="Role-aware Heuristic Episodic Attention for Conversational LLMs" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Role-aware Heuristic Episodic Attention for Conversational LLMs 基础模型 原文首页未列第一作者机构 2026-10-01 把全局指令放入持久前缀，把多轮交互放入 episodic memory；检索时按角色决定保留原文、压缩表示或省略。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行角色分离与 episodic top-k；不调用压缩 LLM。执行角色分离与 episodic top-k；不调用压缩 LLM。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  长上下文 会话记忆 注意力 基础模型 长上下文：注意力、递归状态与记忆 角色感知的 episodic 检索，相对只保留最近聊天窗口改变了什么？ 最近窗口只看时间距离；episodic检索可取回更远但相关的交互，并保留独立持久指令。角色策略还区分不同来源内容的处理方式，但不保证压缩后一定无信息损失。 示意：较早的用户偏好可被取回，而很多刚发生但无关的工具日志可以省略。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d014abe718e687fc">角色感知的 episodic 检索，相对只保留最近聊天窗口改变了什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Area">Role-aware Heuristic Episodic Attention for Conversational LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最近窗口只看时间距离；episodic检索可取回更远但相关的交互，并保留独立持久指令。角色策略还区分不同来源内容的处理方式，但不保证压缩后一定无信息损失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>较早的用户偏好可被取回，而很多刚发生但无关的工具日志可以省略。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00958">原论文</a> · <a href="../../../../foundation-models/2610.00958-rea/">实现解读</a> · <a href="#qa-d014abe718e687fc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:rea" data-paper-title="Role-aware Heuristic Episodic Attention for Conversational LLMs" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Role-aware Heuristic Episodic Attention for Conversational LLMs 基础模型 原文首页未列第一作者机构 2026-10-01 把全局指令放入持久前缀，把多轮交互放入 episodic memory；检索时按角色决定保留原文、压缩表示或省略。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行角色分离与 episodic top-k；不调用压缩 LLM。执行角色分离与 episodic top-k；不调用压缩 LLM。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  长上下文 会话记忆 注意力 基础模型 长上下文：注意力、递归状态与记忆 本地 REA 的 top-k 与角色分离已经包含真实 LLM 压缩吗？ 没有。文档只记录角色分离和episodic top-k执行，不调用压缩LLM。集成时应区分已执行的记忆选择与尚未提供的生成式压缩，不能把压缩占位当成模型能力。 示意：选中了三段历史，不等于已经让一个语言模型把三段压成忠实摘要。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-155fe90c15fcfee8">本地 REA 的 top-k 与角色分离已经包含真实 LLM 压缩吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Area">Role-aware Heuristic Episodic Attention for Conversational LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。文档只记录角色分离和episodic top-k执行，不调用压缩LLM。集成时应区分已执行的记忆选择与尚未提供的生成式压缩，不能把压缩占位当成模型能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>选中了三段历史，不等于已经让一个语言模型把三段压成忠实摘要。</p>
<p class="ar-learning-sources">依据：复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00958">原论文</a> · <a href="../../../../foundation-models/2610.00958-rea/">实现解读</a> · <a href="#qa-155fe90c15fcfee8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:triadic-linear-attention" data-paper-title="Triadic Linear Attention: Three-Dimensional Recurrent States for Long-Context Sequence Modeling" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Triadic Linear Attention: Three-Dimensional Recurrent States for Long-Context Sequence Modeling 基础模型 MIT / MIT-IBM Watson AI Lab 2026-09-29 普通线性注意力写入的二维状态；Triadic 再加入第二 key，写入，读取时用收缩两个 key 轴。第二 key 维度为时，状态容量乘以，只新增两组 projection；严格退化为普通线性注意力。 复现级别：L1 递推机制。复现级别：L1 递推机制。实现论文 Eq. (2)–(3) 的写入、双 query 收缩和按第二 key 轴衰减。triadic_linear_attention 是透明的 recurrent reference，测试对照显式求和、检查因果性、退化与梯度；三种子机制结果见 metrics/mechanism-seeds42-44.json。未实现论文 Triton chunkwise kernel、Gated DeltaNet upcycling 或长书语言建模，不能把小张量一致性当成论文效果复现。  网络架构 线性注意力 长上下文 基础模型 长上下文：注意力、递归状态与记忆 线性注意力的“状态”是逐条历史列表，还是累积的关联记忆？ 普通线性注意力把key与value的外积写入累积二维状态，读取用query收缩，而不是逐条保留原始KV列表。Triadic在此基础上增加一个key轴，讨论的是关联状态容量与寻址条件。 示意：状态像把多次写入叠加到一张关联表；新增key轴相当于增加一种联合寻址条件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-triadic-linear-attention-debbb585" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c44e1dc920136d0b">线性注意力的“状态”是逐条历史列表，还是累积的关联记忆？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atriadic-linear-attention">Triadic Linear Attention: Three-Dimensional Recurrent States for Long-Context Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · MIT / MIT-IBM Watson AI Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>普通线性注意力把key与value的外积写入累积二维状态，读取用query收缩，而不是逐条保留原始KV列表。Triadic在此基础上增加一个key轴，讨论的是关联状态容量与寻址条件。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>状态像把多次写入叠加到一张关联表；新增key轴相当于增加一种联合寻址条件。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36529">原论文</a> · <a href="../../../../foundation-models/2609.36529-triadic-linear-attention/">实现解读</a> · <a href="#qa-c44e1dc920136d0b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:triadic-linear-attention" data-paper-title="Triadic Linear Attention: Three-Dimensional Recurrent States for Long-Context Sequence Modeling" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Triadic Linear Attention: Three-Dimensional Recurrent States for Long-Context Sequence Modeling 基础模型 MIT / MIT-IBM Watson AI Lab 2026-09-29 普通线性注意力写入的二维状态；Triadic 再加入第二 key，写入，读取时用收缩两个 key 轴。第二 key 维度为时，状态容量乘以，只新增两组 projection；严格退化为普通线性注意力。 复现级别：L1 递推机制。复现级别：L1 递推机制。实现论文 Eq. (2)–(3) 的写入、双 query 收缩和按第二 key 轴衰减。triadic_linear_attention 是透明的 recurrent reference，测试对照显式求和、检查因果性、退化与梯度；三种子机制结果见 metrics/mechanism-seeds42-44.json。未实现论文 Triton chunkwise kernel、Gated DeltaNet upcycling 或长书语言建模，不能把小张量一致性当成论文效果复现。  网络架构 线性注意力 长上下文 基础模型 长上下文：注意力、递归状态与记忆 Triadic Linear Attention增加第二个key，容量和检索条件如何改变？ 普通线性attention把key与value写入二维状态；Triadic再加入第二个key轴，查询时用两组query共同收缩。这样关联同时受两种地址条件约束，状态容量随第二key维度增大，而不是免费扩容。第二维退化为1时应回到普通线性attention，是检查实现是否保留核心机制的边界。 教学例子：用人物和场景作为两种地址，同一个人物在不同场景对应不同value；第二key可帮助区分，但也需要保存更大的联合状态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-6d8ba49e4e0aa0df">Triadic Linear Attention增加第二个key，容量和检索条件如何改变？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atriadic-linear-attention">Triadic Linear Attention: Three-Dimensional Recurrent States for Long-Context Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · MIT / MIT-IBM Watson AI Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>普通线性attention把key与value写入二维状态；Triadic再加入第二个key轴，查询时用两组query共同收缩。这样关联同时受两种地址条件约束，状态容量随第二key维度增大，而不是免费扩容。第二维退化为1时应回到普通线性attention，是检查实现是否保留核心机制的边界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用人物和场景作为两种地址，同一个人物在不同场景对应不同value；第二key可帮助区分，但也需要保存更大的联合状态。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36529">原论文</a> · <a href="../../../../foundation-models/2609.36529-triadic-linear-attention/">实现解读</a> · <a href="#qa-6d8ba49e4e0aa0df">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:triadic-linear-attention" data-paper-title="Triadic Linear Attention: Three-Dimensional Recurrent States for Long-Context Sequence Modeling" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Triadic Linear Attention: Three-Dimensional Recurrent States for Long-Context Sequence Modeling 基础模型 MIT / MIT-IBM Watson AI Lab 2026-09-29 普通线性注意力写入的二维状态；Triadic 再加入第二 key，写入，读取时用收缩两个 key 轴。第二 key 维度为时，状态容量乘以，只新增两组 projection；严格退化为普通线性注意力。 复现级别：L1 递推机制。复现级别：L1 递推机制。实现论文 Eq. (2)–(3) 的写入、双 query 收缩和按第二 key 轴衰减。triadic_linear_attention 是透明的 recurrent reference，测试对照显式求和、检查因果性、退化与梯度；三种子机制结果见 metrics/mechanism-seeds42-44.json。未实现论文 Triton chunkwise kernel、Gated DeltaNet upcycling 或长书语言建模，不能把小张量一致性当成论文效果复现。  网络架构 线性注意力 长上下文 基础模型 长上下文：注意力、递归状态与记忆 三阶状态增加的容量，与只增大普通线性注意力的 value 维度有什么不同？ 第二key维度E新增一个可被独立查询收缩的轴，状态容量乘E；只增大value维度扩充的是输出内容维度，不提供相同的双key寻址结构。 示意：给每条记录增加更多内容，与给记录再加一个独立检索条件，是不同的扩展。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d494a0dcffab28cd">三阶状态增加的容量，与只增大普通线性注意力的 value 维度有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atriadic-linear-attention">Triadic Linear Attention: Three-Dimensional Recurrent States for Long-Context Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · MIT / MIT-IBM Watson AI Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>第二key维度E新增一个可被独立查询收缩的轴，状态容量乘E；只增大value维度扩充的是输出内容维度，不提供相同的双key寻址结构。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>给每条记录增加更多内容，与给记录再加一个独立检索条件，是不同的扩展。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36529">原论文</a> · <a href="../../../../foundation-models/2609.36529-triadic-linear-attention/">实现解读</a> · <a href="#qa-d494a0dcffab28cd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:triadic-linear-attention" data-paper-title="Triadic Linear Attention: Three-Dimensional Recurrent States for Long-Context Sequence Modeling" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Triadic Linear Attention: Three-Dimensional Recurrent States for Long-Context Sequence Modeling 基础模型 MIT / MIT-IBM Watson AI Lab 2026-09-29 普通线性注意力写入的二维状态；Triadic 再加入第二 key，写入，读取时用收缩两个 key 轴。第二 key 维度为时，状态容量乘以，只新增两组 projection；严格退化为普通线性注意力。 复现级别：L1 递推机制。复现级别：L1 递推机制。实现论文 Eq. (2)–(3) 的写入、双 query 收缩和按第二 key 轴衰减。triadic_linear_attention 是透明的 recurrent reference，测试对照显式求和、检查因果性、退化与梯度；三种子机制结果见 metrics/mechanism-seeds42-44.json。未实现论文 Triton chunkwise kernel、Gated DeltaNet upcycling 或长书语言建模，不能把小张量一致性当成论文效果复现。  网络架构 线性注意力 长上下文 基础模型 长上下文：注意力、递归状态与记忆 Triadic 的 E=1 退化测试为什么比“前向没有报错”更有用？ 该边界应严格还原普通线性注意力，可检查第二key轴的构造与收缩是否正确。还应对照显式历史求和、因果性和梯度；这些算子测试不证明长书语言建模效果。 示意：移除第二key的实际自由度后，输出应与同输入的二维记忆参考一致。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a38956b9ce3cc27d">Triadic 的 E=1 退化测试为什么比“前向没有报错”更有用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atriadic-linear-attention">Triadic Linear Attention: Three-Dimensional Recurrent States for Long-Context Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · MIT / MIT-IBM Watson AI Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>该边界应严格还原普通线性注意力，可检查第二key轴的构造与收缩是否正确。还应对照显式历史求和、因果性和梯度；这些算子测试不证明长书语言建模效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>移除第二key的实际自由度后，输出应与同输入的二维记忆参考一致。</p>
<p class="ar-learning-sources">依据：背景与主要改动、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36529">原论文</a> · <a href="../../../../foundation-models/2609.36529-triadic-linear-attention/">实现解读</a> · <a href="#qa-a38956b9ce3cc27d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:frac-ssm" data-paper-title="Fractional State Space Transition for Long Sequence Modeling" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Fractional State Space Transition for Long Sequence Modeling 基础模型 Huawei Noah&#x27;s Ark Lab, Montreal Research Center 2026-09-28 以对数间隔的有限指数模态逼近分数阶动力学的幂律记忆，在有界递归状态下兼顾长尾记忆和并行训练。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行有限模态递归与长尾记忆不变量；不是 1.3B 参数语言模型结果。执行有限模态递归与长尾记忆不变量；不是 1.3B 参数语言模型结果。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  状态空间模型 长上下文 基础模型 长上下文：注意力、递归状态与记忆 Frac-SSM 所说的幂律记忆，与只记住最近窗口有何区别？ 幂律尾部表示旧事件的影响衰减较慢，不在固定窗口边界突然消失。Frac-SSM用有限指数模态近似这类长尾，在有界递归状态中保留多个时间尺度。 示意：很久前的一次事件仍可能有较弱影响，而不是离开最近100步后立即归零。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-frac-ssm-9d35422b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-88fb5b322da73fee">Frac-SSM 所说的幂律记忆，与只记住最近窗口有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Afrac-ssm">Fractional State Space Transition for Long Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Noah&#x27;s Ark Lab, Montreal Research Center</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>幂律尾部表示旧事件的影响衰减较慢，不在固定窗口边界突然消失。Frac-SSM用有限指数模态近似这类长尾，在有界递归状态中保留多个时间尺度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>很久前的一次事件仍可能有较弱影响，而不是离开最近100步后立即归零。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36314">原论文</a> · <a href="../../../../foundation-models/2609.36314-frac-ssm/">实现解读</a> · <a href="#qa-88fb5b322da73fee">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:frac-ssm" data-paper-title="Fractional State Space Transition for Long Sequence Modeling" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Fractional State Space Transition for Long Sequence Modeling 基础模型 Huawei Noah&#x27;s Ark Lab, Montreal Research Center 2026-09-28 以对数间隔的有限指数模态逼近分数阶动力学的幂律记忆，在有界递归状态下兼顾长尾记忆和并行训练。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行有限模态递归与长尾记忆不变量；不是 1.3B 参数语言模型结果。执行有限模态递归与长尾记忆不变量；不是 1.3B 参数语言模型结果。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  状态空间模型 长上下文 基础模型 长上下文：注意力、递归状态与记忆 有限个递归状态，怎样近似分数阶系统很长的幂律记忆？ 单个指数模式只有一种衰减时间尺度；方法用对数间隔的多个指数模式共同逼近幂律尾部。快速模式追踪近期变化，慢速模式保留更远历史，组合后获得更宽的有效记忆范围。它仍是有限模式近似，因此状态容量和近似区间有限，不能据此宣称无限精确记忆。 教学例子：用快、中、慢三条衰减通道同时记录一次事件；短期主要由快通道贡献，过很久后由慢通道贡献。三者相加能比单一衰减更接近长尾影响。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-70c0b6310e5e85f1">有限个递归状态，怎样近似分数阶系统很长的幂律记忆？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Afrac-ssm">Fractional State Space Transition for Long Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Noah&#x27;s Ark Lab, Montreal Research Center</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单个指数模式只有一种衰减时间尺度；方法用对数间隔的多个指数模式共同逼近幂律尾部。快速模式追踪近期变化，慢速模式保留更远历史，组合后获得更宽的有效记忆范围。它仍是有限模式近似，因此状态容量和近似区间有限，不能据此宣称无限精确记忆。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用快、中、慢三条衰减通道同时记录一次事件；短期主要由快通道贡献，过很久后由慢通道贡献。三者相加能比单一衰减更接近长尾影响。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36314">原论文</a> · <a href="../../../../foundation-models/2609.36314-frac-ssm/">实现解读</a> · <a href="#qa-70c0b6310e5e85f1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:frac-ssm" data-paper-title="Fractional State Space Transition for Long Sequence Modeling" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Fractional State Space Transition for Long Sequence Modeling 基础模型 Huawei Noah&#x27;s Ark Lab, Montreal Research Center 2026-09-28 以对数间隔的有限指数模态逼近分数阶动力学的幂律记忆，在有界递归状态下兼顾长尾记忆和并行训练。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行有限模态递归与长尾记忆不变量；不是 1.3B 参数语言模型结果。执行有限模态递归与长尾记忆不变量；不是 1.3B 参数语言模型结果。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  状态空间模型 长上下文 基础模型 长上下文：注意力、递归状态与记忆 为什么多个不同衰减速度的状态，比单个指数衰减更适合近似长尾？ 单个指数状态只有一种时间尺度；多个对数间隔的模态可分别覆盖近期与远期，组合后更接近幂律。有限模态仍只在一定范围内近似，不等于精确实现无限历史。 示意：快状态记短期波动，慢状态记长期趋势，两者相加而非强迫一个衰减率兼顾全部。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4881d67379b8f1c5">为什么多个不同衰减速度的状态，比单个指数衰减更适合近似长尾？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Afrac-ssm">Fractional State Space Transition for Long Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Noah&#x27;s Ark Lab, Montreal Research Center</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单个指数状态只有一种时间尺度；多个对数间隔的模态可分别覆盖近期与远期，组合后更接近幂律。有限模态仍只在一定范围内近似，不等于精确实现无限历史。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>快状态记短期波动，慢状态记长期趋势，两者相加而非强迫一个衰减率兼顾全部。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36314">原论文</a> · <a href="../../../../foundation-models/2609.36314-frac-ssm/">实现解读</a> · <a href="#qa-4881d67379b8f1c5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:frac-ssm" data-paper-title="Fractional State Space Transition for Long Sequence Modeling" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Fractional State Space Transition for Long Sequence Modeling 基础模型 Huawei Noah&#x27;s Ark Lab, Montreal Research Center 2026-09-28 以对数间隔的有限指数模态逼近分数阶动力学的幂律记忆，在有界递归状态下兼顾长尾记忆和并行训练。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行有限模态递归与长尾记忆不变量；不是 1.3B 参数语言模型结果。执行有限模态递归与长尾记忆不变量；不是 1.3B 参数语言模型结果。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  状态空间模型 长上下文 基础模型 长上下文：注意力、递归状态与记忆 测试有限模态递归时，应该检查哪些内容而不是只看输出形状？ 应检验递归更新与对应有限模态计算一致、长尾记忆不变量以及状态跨步传递。当前记录属于这类算子诊断，不能把它标成1.3B语言模型效果或完整训练复现。 示意：向序列早期注入一次脉冲，检查多个状态随时间衰减后的合成贡献是否符合所定义的近似。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ea7bf61d830b801b">测试有限模态递归时，应该检查哪些内容而不是只看输出形状？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Afrac-ssm">Fractional State Space Transition for Long Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Noah&#x27;s Ark Lab, Montreal Research Center</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>应检验递归更新与对应有限模态计算一致、长尾记忆不变量以及状态跨步传递。当前记录属于这类算子诊断，不能把它标成1.3B语言模型效果或完整训练复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>向序列早期注入一次脉冲，检查多个状态随时间衰减后的合成贡献是否符合所定义的近似。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36314">原论文</a> · <a href="../../../../foundation-models/2609.36314-frac-ssm/">实现解读</a> · <a href="#qa-ea7bf61d830b801b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ms-gla" data-paper-title="MS-GLA: Multi-Scale Gated Linear Attention for Addressing Representational Bottlenecks via Multi-Temporal Resolution" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="MS-GLA: Multi-Scale Gated Linear Attention for Addressing Representational Bottlenecks via Multi-Temporal Resolution 基础模型 International Institute of Information Technology Hyderabad 2026-09-28 单一时间分辨率的线性注意力容易形成表征瓶颈。MS-GLA 把 head budget 分配给多个尺度：先做无重叠 masked average pooling，再分别执行 GLA，最后以因果 hold 方式恢复到 token 分辨率，并由输入相关 softmax 路由融合。 未复现论文的 Flash kernel 和等参数训练。复现级别：L1 架构机制 + 真实 A100 前后向。复现级别：L1 架构机制 + 真实 A100 前后向。保留多尺度分解、因果 hold 对齐与输入相关融合；未复现论文的 Flash kernel 和等参数训练。当前 recurrent kernel 面向正确性而非吞吐，没有复刻 Triton/Flash 实现或论文参数规模。尚未接入 Evolve，避免把结构名登记误称为已可搜索与公平评价。MultiScaleGLA 是可前后向的紧凑 PyTorch 层；A100 receipt 只证明 CUDA 路径可运行。  网络架构 线性注意力 长上下文 基础模型 长上下文：注意力、递归状态与记忆 MS-GLA 为什么让不同 head 处理不同时间尺度？ 单一时间分辨率可能成为表征瓶颈。MS-GLA把头预算分配到多个尺度，让一部分保留逐token变化，另一部分处理池化后的较粗历史，再融合这些信息。 示意：短语内部细节与跨多个短语的趋势，不必都由同一种更新频率承担。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-ms-gla-a1875a93" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-95933f677c9061f9">MS-GLA 为什么让不同 head 处理不同时间尺度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ams-gla">MS-GLA: Multi-Scale Gated Linear Attention for Addressing Representational Bottlenecks via Multi-Temporal Resolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · International Institute of Information Technology Hyderabad</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单一时间分辨率可能成为表征瓶颈。MS-GLA把头预算分配到多个尺度，让一部分保留逐token变化，另一部分处理池化后的较粗历史，再融合这些信息。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>短语内部细节与跨多个短语的趋势，不必都由同一种更新频率承担。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35664">原论文</a> · <a href="../../../../foundation-models/2609.35664-ms-gla/">实现解读</a> · <a href="#qa-95933f677c9061f9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ms-gla" data-paper-title="MS-GLA: Multi-Scale Gated Linear Attention for Addressing Representational Bottlenecks via Multi-Temporal Resolution" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="MS-GLA: Multi-Scale Gated Linear Attention for Addressing Representational Bottlenecks via Multi-Temporal Resolution 基础模型 International Institute of Information Technology Hyderabad 2026-09-28 单一时间分辨率的线性注意力容易形成表征瓶颈。MS-GLA 把 head budget 分配给多个尺度：先做无重叠 masked average pooling，再分别执行 GLA，最后以因果 hold 方式恢复到 token 分辨率，并由输入相关 softmax 路由融合。 未复现论文的 Flash kernel 和等参数训练。复现级别：L1 架构机制 + 真实 A100 前后向。复现级别：L1 架构机制 + 真实 A100 前后向。保留多尺度分解、因果 hold 对齐与输入相关融合；未复现论文的 Flash kernel 和等参数训练。当前 recurrent kernel 面向正确性而非吞吐，没有复刻 Triton/Flash 实现或论文参数规模。尚未接入 Evolve，避免把结构名登记误称为已可搜索与公平评价。MultiScaleGLA 是可前后向的紧凑 PyTorch 层；A100 receipt 只证明 CUDA 路径可运行。  网络架构 线性注意力 长上下文 基础模型 长上下文：注意力、递归状态与记忆 MS-GLA把几个token池化到一起后，怎样避免把未来信息漏给块前部？ 粗尺度分支先对不重叠块做masked平均，再运行GLA；一个块的汇总只有在块末token到达后才能对外可见。恢复token分辨率时使用因果hold，而不是把整块结果提前填回每个位置。多个时间尺度最后由输入相关权重融合，从而兼顾细粒度变化和更长时间范围。 教学例子：尺度4的块包含位置1到4；位置2不能读取由位置3、4共同形成的平均值。必须等到位置4结束后，后续位置才能使用这块的粗尺度状态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-ea64391758996402">MS-GLA把几个token池化到一起后，怎样避免把未来信息漏给块前部？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ams-gla">MS-GLA: Multi-Scale Gated Linear Attention for Addressing Representational Bottlenecks via Multi-Temporal Resolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · International Institute of Information Technology Hyderabad</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>粗尺度分支先对不重叠块做masked平均，再运行GLA；一个块的汇总只有在块末token到达后才能对外可见。恢复token分辨率时使用因果hold，而不是把整块结果提前填回每个位置。多个时间尺度最后由输入相关权重融合，从而兼顾细粒度变化和更长时间范围。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>尺度4的块包含位置1到4；位置2不能读取由位置3、4共同形成的平均值。必须等到位置4结束后，后续位置才能使用这块的粗尺度状态。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35664">原论文</a> · <a href="../../../../foundation-models/2609.35664-ms-gla/">实现解读</a> · <a href="#qa-ea64391758996402">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ms-gla" data-paper-title="MS-GLA: Multi-Scale Gated Linear Attention for Addressing Representational Bottlenecks via Multi-Temporal Resolution" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="MS-GLA: Multi-Scale Gated Linear Attention for Addressing Representational Bottlenecks via Multi-Temporal Resolution 基础模型 International Institute of Information Technology Hyderabad 2026-09-28 单一时间分辨率的线性注意力容易形成表征瓶颈。MS-GLA 把 head budget 分配给多个尺度：先做无重叠 masked average pooling，再分别执行 GLA，最后以因果 hold 方式恢复到 token 分辨率，并由输入相关 softmax 路由融合。 未复现论文的 Flash kernel 和等参数训练。复现级别：L1 架构机制 + 真实 A100 前后向。复现级别：L1 架构机制 + 真实 A100 前后向。保留多尺度分解、因果 hold 对齐与输入相关融合；未复现论文的 Flash kernel 和等参数训练。当前 recurrent kernel 面向正确性而非吞吐，没有复刻 Triton/Flash 实现或论文参数规模。尚未接入 Evolve，避免把结构名登记误称为已可搜索与公平评价。MultiScaleGLA 是可前后向的紧凑 PyTorch 层；A100 receipt 只证明 CUDA 路径可运行。  网络架构 线性注意力 长上下文 基础模型 长上下文：注意力、递归状态与记忆 多尺度 GLA 相对单一尺度，多出的并不只是更大的窗口，为什么？ 各尺度先对输入做不同粒度的无重叠池化，再分别执行GLA；这改变了状态更新的时间分辨率。只扩窗口仍按同样的token粒度更新，不能等价替代这条多尺度路径。 示意：每四词形成一次粗更新，与每词更新但多看四词，是不同的信息组织方式。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-8d3d6b392df03331">多尺度 GLA 相对单一尺度，多出的并不只是更大的窗口，为什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ams-gla">MS-GLA: Multi-Scale Gated Linear Attention for Addressing Representational Bottlenecks via Multi-Temporal Resolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · International Institute of Information Technology Hyderabad</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>各尺度先对输入做不同粒度的无重叠池化，再分别执行GLA；这改变了状态更新的时间分辨率。只扩窗口仍按同样的token粒度更新，不能等价替代这条多尺度路径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>每四词形成一次粗更新，与每词更新但多看四词，是不同的信息组织方式。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35664">原论文</a> · <a href="../../../../foundation-models/2609.35664-ms-gla/">实现解读</a> · <a href="#qa-8d3d6b392df03331">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ms-gla" data-paper-title="MS-GLA: Multi-Scale Gated Linear Attention for Addressing Representational Bottlenecks via Multi-Temporal Resolution" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="MS-GLA: Multi-Scale Gated Linear Attention for Addressing Representational Bottlenecks via Multi-Temporal Resolution 基础模型 International Institute of Information Technology Hyderabad 2026-09-28 单一时间分辨率的线性注意力容易形成表征瓶颈。MS-GLA 把 head budget 分配给多个尺度：先做无重叠 masked average pooling，再分别执行 GLA，最后以因果 hold 方式恢复到 token 分辨率，并由输入相关 softmax 路由融合。 未复现论文的 Flash kernel 和等参数训练。复现级别：L1 架构机制 + 真实 A100 前后向。复现级别：L1 架构机制 + 真实 A100 前后向。保留多尺度分解、因果 hold 对齐与输入相关融合；未复现论文的 Flash kernel 和等参数训练。当前 recurrent kernel 面向正确性而非吞吐，没有复刻 Triton/Flash 实现或论文参数规模。尚未接入 Evolve，避免把结构名登记误称为已可搜索与公平评价。MultiScaleGLA 是可前后向的紧凑 PyTorch 层；A100 receipt 只证明 CUDA 路径可运行。  网络架构 线性注意力 长上下文 基础模型 长上下文：注意力、递归状态与记忆 尺度为4的 pooled 表示何时才能供第一个块里的 token 使用？ 只有块末token到达后才可见，否则池化会泄漏块内未来。恢复token分辨率需使用因果hold，再按当前输入的softmax权重融合；不能直接把完整块均值广播给块内每个位置。 示意：第1词预测时不能使用第1到4词的平均值；第4词到达后才允许读取该块表示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-97483a5c9b1dce32">尺度为4的 pooled 表示何时才能供第一个块里的 token 使用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ams-gla">MS-GLA: Multi-Scale Gated Linear Attention for Addressing Representational Bottlenecks via Multi-Temporal Resolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · International Institute of Information Technology Hyderabad</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只有块末token到达后才可见，否则池化会泄漏块内未来。恢复token分辨率需使用因果hold，再按当前输入的softmax权重融合；不能直接把完整块均值广播给块内每个位置。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第1词预测时不能使用第1到4词的平均值；第4词到达后才允许读取该块表示。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35664">原论文</a> · <a href="../../../../foundation-models/2609.35664-ms-gla/">实现解读</a> · <a href="#qa-97483a5c9b1dce32">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:oda" data-paper-title="On-Demand Attention: Efficient Long-Context Decoding with Learned Recall" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="On-Demand Attention: Efficient Long-Context Decoding with Learned Recall 基础模型 Southern University of Science and Technology 2026-09-17 默认只读局部 KV，由轻量 recall head 在全局注意力发生前预测其收益；仅高收益 token 触发全局读取，完整 KV 仍保留。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 recall gate 和条件全局注意力；真实 A100 receipt 只证明 CUDA 路径，不外推 vLLM 吞吐。本地执行 recall gate 和条件全局注意力；真实 A100 receipt 只证明 CUDA 路径，不外推 vLLM 吞吐。  注意力与长上下文 推理效率 基础模型 长上下文：注意力、递归状态与记忆 ODA 所说的局部历史与远程历史，是按信息重要性划分的吗？ 局部与远程首先是相对当前token的可读位置范围，不是重要与不重要的标签。重要证据可能在很久以前，近邻也可能无关；理解这一点，才能明白为什么局部读取之外仍需要按需全局访问。 示意：刚出现的几个词属于局部窗口，文章开头的人名可能已经在窗口外，却仍对当前问题很重要。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-oda-5fd8c6ed" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-edf84b3436ce3886">ODA 所说的局部历史与远程历史，是按信息重要性划分的吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aoda">On-Demand Attention: Efficient Long-Context Decoding with Learned Recall</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Southern University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>局部与远程首先是相对当前token的可读位置范围，不是重要与不重要的标签。重要证据可能在很久以前，近邻也可能无关；理解这一点，才能明白为什么局部读取之外仍需要按需全局访问。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>刚出现的几个词属于局部窗口，文章开头的人名可能已经在窗口外，却仍对当前问题很重要。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.20734">原论文</a> · <a href="../../../../foundation-models/2609.20734-oda/">实现解读</a> · <a href="#qa-edf84b3436ce3886">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:oda" data-paper-title="On-Demand Attention: Efficient Long-Context Decoding with Learned Recall" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="On-Demand Attention: Efficient Long-Context Decoding with Learned Recall 基础模型 Southern University of Science and Technology 2026-09-17 默认只读局部 KV，由轻量 recall head 在全局注意力发生前预测其收益；仅高收益 token 触发全局读取，完整 KV 仍保留。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 recall gate 和条件全局注意力；真实 A100 receipt 只证明 CUDA 路径，不外推 vLLM 吞吐。本地执行 recall gate 和条件全局注意力；真实 A100 receipt 只证明 CUDA 路径，不外推 vLLM 吞吐。  注意力与长上下文 推理效率 基础模型 长上下文：注意力、递归状态与记忆 On-Demand Attention默认只读局部KV，什么时候才调用全局检索？ 轻量recall head先预测一次全局注意力的预期收益，在真正执行昂贵全局读取前作决定；只有值得的token才触发。完整KV仍被保存，所以省掉的是部分解码位置的读取计算，不能据此声称缓存已经被删除或压缩。判断器漏判时，也可能失去本应使用的远程证据。 教学例子：连续生成固定格式标点时可能仅靠局部状态；到了需要引用开头编号的位置，再触发全局读取。这个触发决定必须先作，不能先花全局成本再宣称省掉了它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-63a2a877c0ad9062">On-Demand Attention默认只读局部KV，什么时候才调用全局检索？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aoda">On-Demand Attention: Efficient Long-Context Decoding with Learned Recall</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Southern University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>轻量recall head先预测一次全局注意力的预期收益，在真正执行昂贵全局读取前作决定；只有值得的token才触发。完整KV仍被保存，所以省掉的是部分解码位置的读取计算，不能据此声称缓存已经被删除或压缩。判断器漏判时，也可能失去本应使用的远程证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>连续生成固定格式标点时可能仅靠局部状态；到了需要引用开头编号的位置，再触发全局读取。这个触发决定必须先作，不能先花全局成本再宣称省掉了它。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.20734">原论文</a> · <a href="../../../../foundation-models/2609.20734-oda/">实现解读</a> · <a href="#qa-63a2a877c0ad9062">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:oda" data-paper-title="On-Demand Attention: Efficient Long-Context Decoding with Learned Recall" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="On-Demand Attention: Efficient Long-Context Decoding with Learned Recall 基础模型 Southern University of Science and Technology 2026-09-17 默认只读局部 KV，由轻量 recall head 在全局注意力发生前预测其收益；仅高收益 token 触发全局读取，完整 KV 仍保留。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 recall gate 和条件全局注意力；真实 A100 receipt 只证明 CUDA 路径，不外推 vLLM 吞吐。本地执行 recall gate 和条件全局注意力；真实 A100 receipt 只证明 CUDA 路径，不外推 vLLM 吞吐。  注意力与长上下文 推理效率 基础模型 长上下文：注意力、递归状态与记忆 ODA 的按需读取，与直接驱逐旧 KV 的方法有什么不同？ ODA保留完整KV，只动态决定何时读取全局；驱逐会让部分历史缓存永久离开可访问集合。前者主要改变访问计算，后者还改变缓存容量，不能把两者的节省口径混在一起。 示意：某条旧信息本轮没有被读，不代表下一轮就无法从保留的KV中取回。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-88cec963475ac414">ODA 的按需读取，与直接驱逐旧 KV 的方法有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aoda">On-Demand Attention: Efficient Long-Context Decoding with Learned Recall</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Southern University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>ODA保留完整KV，只动态决定何时读取全局；驱逐会让部分历史缓存永久离开可访问集合。前者主要改变访问计算，后者还改变缓存容量，不能把两者的节省口径混在一起。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某条旧信息本轮没有被读，不代表下一轮就无法从保留的KV中取回。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.20734">原论文</a> · <a href="../../../../foundation-models/2609.20734-oda/">实现解读</a> · <a href="#qa-88cec963475ac414">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:oda" data-paper-title="On-Demand Attention: Efficient Long-Context Decoding with Learned Recall" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="On-Demand Attention: Efficient Long-Context Decoding with Learned Recall 基础模型 Southern University of Science and Technology 2026-09-17 默认只读局部 KV，由轻量 recall head 在全局注意力发生前预测其收益；仅高收益 token 触发全局读取，完整 KV 仍保留。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 recall gate 和条件全局注意力；真实 A100 receipt 只证明 CUDA 路径，不外推 vLLM 吞吐。本地执行 recall gate 和条件全局注意力；真实 A100 receipt 只证明 CUDA 路径，不外推 vLLM 吞吐。  注意力与长上下文 推理效率 基础模型 长上下文：注意力、递归状态与记忆 为什么 ODA 的 recall 判断必须发生在全局 attention 之前？ 若先计算完整全局attention再决定是否需要它，就已经支付了要节省的成本。门控应控制条件执行；本地A100回执只证明路径可运行，不能由此外推vLLM端到端吞吐。 示意：先翻完整本书再决定只看目录，并没有省下翻书工作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3f3461a49801c34b">为什么 ODA 的 recall 判断必须发生在全局 attention 之前？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aoda">On-Demand Attention: Efficient Long-Context Decoding with Learned Recall</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Southern University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若先计算完整全局attention再决定是否需要它，就已经支付了要节省的成本。门控应控制条件执行；本地A100回执只证明路径可运行，不能由此外推vLLM端到端吞吐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先翻完整本书再决定只看目录，并没有省下翻书工作。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.20734">原论文</a> · <a href="../../../../foundation-models/2609.20734-oda/">实现解读</a> · <a href="#qa-3f3461a49801c34b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:sas-attention" data-paper-title="SAS: Simple Attention Sparsification via End-to-End Optimization of Context Ranking" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="SAS: Simple Attention Sparsification via End-to-End Optimization of Context Ranking 基础模型 Tencent HY LLM Frontier / HKUST (Guangzhou) / HKUST 2026-09-11 硬 Top-K 只能改变被选中的索引，语言模型损失无法沿离散索引直接训练 selector。SAS 不再蒸馏 dense attention：selector 先给历史块连续打分，训练时保留 Top-K 块的连续 gate，并把 log(gate) 加到注意力 logits 内。这样最终 token prediction loss 可直接优化“哪些上下文真正影响预测”。历史块 gate 共同 softmax 归一化，当前块始终使用单位 gate，避免历史上下文整体权重漂移。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地真实训练冻结主干后的 selector，执行 softmax 归一化 gate、历史块 Top-K、当前块常驻和 attention softmax 内的 log-gate；不把 PyTorch 参考实现宣称为 Triton 加速实现。本地实现物化稠密注意力矩阵，仅用于验证论文的选择与梯度机制；没有复刻 Qwen3-4B/8B/14B、OLMo3-7B、OpenR1-Math-220k、LongBench、BFCL、VitaBench，也没有接入原文 Triton/FlashAttention kernel 和 SGLang benchmark。  sparse-attention long-context post-training context-ranking 基础模型 长上下文：注意力、递归状态与记忆 SAS 为什么要保留连续 gate，而不只保存 top-k 的块索引？ 索引决定选谁，却不能直接让语言模型损失通过离散选择训练selector。连续gate进入所选attention的计算后，提供可微的反馈路径，使selector能学到哪些历史帮助预测。 示意：选中同样两块，0.8/0.2与0.5/0.5仍能产生不同读出和训练梯度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-sas-attention-90d42e99" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8e073aa1cf873934">SAS 为什么要保留连续 gate，而不只保存 top-k 的块索引？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asas-attention">SAS: Simple Attention Sparsification via End-to-End Optimization of Context Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent HY LLM Frontier / HKUST (Guangzhou) / HKUST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>索引决定选谁，却不能直接让语言模型损失通过离散选择训练selector。连续gate进入所选attention的计算后，提供可微的反馈路径，使selector能学到哪些历史帮助预测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>选中同样两块，0.8/0.2与0.5/0.5仍能产生不同读出和训练梯度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.13141">原论文</a> · <a href="../../../../reproductions/2609.13141-sas-attention/">实现解读</a> · <a href="#qa-8e073aa1cf873934">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:sas-attention" data-paper-title="SAS: Simple Attention Sparsification via End-to-End Optimization of Context Ranking" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="SAS: Simple Attention Sparsification via End-to-End Optimization of Context Ranking 基础模型 Tencent HY LLM Frontier / HKUST (Guangzhou) / HKUST 2026-09-11 硬 Top-K 只能改变被选中的索引，语言模型损失无法沿离散索引直接训练 selector。SAS 不再蒸馏 dense attention：selector 先给历史块连续打分，训练时保留 Top-K 块的连续 gate，并把 log(gate) 加到注意力 logits 内。这样最终 token prediction loss 可直接优化“哪些上下文真正影响预测”。历史块 gate 共同 softmax 归一化，当前块始终使用单位 gate，避免历史上下文整体权重漂移。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地真实训练冻结主干后的 selector，执行 softmax 归一化 gate、历史块 Top-K、当前块常驻和 attention softmax 内的 log-gate；不把 PyTorch 参考实现宣称为 Triton 加速实现。本地实现物化稠密注意力矩阵，仅用于验证论文的选择与梯度机制；没有复刻 Qwen3-4B/8B/14B、OLMo3-7B、OpenR1-Math-220k、LongBench、BFCL、VitaBench，也没有接入原文 Triton/FlashAttention kernel 和 SGLang benchmark。  sparse-attention long-context post-training context-ranking 基础模型 长上下文：注意力、递归状态与记忆 Top-K索引不可导，SAS怎样仍让语言模型损失训练上下文selector？ 它没有声称让离散索引本身变得可导，而是在选中历史块后保留连续gate，并把log gate加进attention的softmax内部。最终预测损失可以沿这些连续数值更新selector。历史gate共同归一化，当前块固定单位gate，避免整体历史权重无约束漂移。 教学例子：两个选中块都进入attention，但gate从0.8、0.2变为0.6、0.4会改变最终输出；损失可据此学习。只留下两个整数索引而丢掉gate，就没有这条梯度通路。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-d6b2dc7c35d29a0f">Top-K索引不可导，SAS怎样仍让语言模型损失训练上下文selector？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asas-attention">SAS: Simple Attention Sparsification via End-to-End Optimization of Context Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent HY LLM Frontier / HKUST (Guangzhou) / HKUST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它没有声称让离散索引本身变得可导，而是在选中历史块后保留连续gate，并把log gate加进attention的softmax内部。最终预测损失可以沿这些连续数值更新selector。历史gate共同归一化，当前块固定单位gate，避免整体历史权重无约束漂移。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个选中块都进入attention，但gate从0.8、0.2变为0.6、0.4会改变最终输出；损失可据此学习。只留下两个整数索引而丢掉gate，就没有这条梯度通路。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.13141">原论文</a> · <a href="../../../../reproductions/2609.13141-sas-attention/">实现解读</a> · <a href="#qa-d6b2dc7c35d29a0f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:sas-attention" data-paper-title="SAS: Simple Attention Sparsification via End-to-End Optimization of Context Ranking" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="SAS: Simple Attention Sparsification via End-to-End Optimization of Context Ranking 基础模型 Tencent HY LLM Frontier / HKUST (Guangzhou) / HKUST 2026-09-11 硬 Top-K 只能改变被选中的索引，语言模型损失无法沿离散索引直接训练 selector。SAS 不再蒸馏 dense attention：selector 先给历史块连续打分，训练时保留 Top-K 块的连续 gate，并把 log(gate) 加到注意力 logits 内。这样最终 token prediction loss 可直接优化“哪些上下文真正影响预测”。历史块 gate 共同 softmax 归一化，当前块始终使用单位 gate，避免历史上下文整体权重漂移。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地真实训练冻结主干后的 selector，执行 softmax 归一化 gate、历史块 Top-K、当前块常驻和 attention softmax 内的 log-gate；不把 PyTorch 参考实现宣称为 Triton 加速实现。本地实现物化稠密注意力矩阵，仅用于验证论文的选择与梯度机制；没有复刻 Qwen3-4B/8B/14B、OLMo3-7B、OpenR1-Math-220k、LongBench、BFCL、VitaBench，也没有接入原文 Triton/FlashAttention kernel 和 SGLang benchmark。  sparse-attention long-context post-training context-ranking 基础模型 长上下文：注意力、递归状态与记忆 SAS 用最终 LM loss 训练 selector，与蒸馏 dense attention 排名有什么不同？ 前者依据token预测目标反馈所选上下文的作用，后者学习模仿dense模型的注意力行为。SAS不要求把dense attention排名当监督；但它仍需正确的连续门控路径，硬top-k本身没有因此变成可导。 示意：某块对复制dense权重很重要，未必对当前预测loss带来相同的训练信号。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-9fdfbe025d1dba3e">SAS 用最终 LM loss 训练 selector，与蒸馏 dense attention 排名有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asas-attention">SAS: Simple Attention Sparsification via End-to-End Optimization of Context Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent HY LLM Frontier / HKUST (Guangzhou) / HKUST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者依据token预测目标反馈所选上下文的作用，后者学习模仿dense模型的注意力行为。SAS不要求把dense attention排名当监督；但它仍需正确的连续门控路径，硬top-k本身没有因此变成可导。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某块对复制dense权重很重要，未必对当前预测loss带来相同的训练信号。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.13141">原论文</a> · <a href="../../../../reproductions/2609.13141-sas-attention/">实现解读</a> · <a href="#qa-9fdfbe025d1dba3e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:sas-attention" data-paper-title="SAS: Simple Attention Sparsification via End-to-End Optimization of Context Ranking" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="SAS: Simple Attention Sparsification via End-to-End Optimization of Context Ranking 基础模型 Tencent HY LLM Frontier / HKUST (Guangzhou) / HKUST 2026-09-11 硬 Top-K 只能改变被选中的索引，语言模型损失无法沿离散索引直接训练 selector。SAS 不再蒸馏 dense attention：selector 先给历史块连续打分，训练时保留 Top-K 块的连续 gate，并把 log(gate) 加到注意力 logits 内。这样最终 token prediction loss 可直接优化“哪些上下文真正影响预测”。历史块 gate 共同 softmax 归一化，当前块始终使用单位 gate，避免历史上下文整体权重漂移。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地真实训练冻结主干后的 selector，执行 softmax 归一化 gate、历史块 Top-K、当前块常驻和 attention softmax 内的 log-gate；不把 PyTorch 参考实现宣称为 Triton 加速实现。本地实现物化稠密注意力矩阵，仅用于验证论文的选择与梯度机制；没有复刻 Qwen3-4B/8B/14B、OLMo3-7B、OpenR1-Math-220k、LongBench、BFCL、VitaBench，也没有接入原文 Triton/FlashAttention kernel 和 SGLang benchmark。  sparse-attention long-context post-training context-ranking 基础模型 长上下文：注意力、递归状态与记忆 SAS 的 log-gate 应加在 softmax 内，还是在输出之后相乘？ 文档要求把选中历史gate的对数加到attention logits，再统一softmax；历史gate共同归一化，当前块固定为1。输出后再乘改变不了同样的相对归一化关系，不是等价替代。 示意：当前块gate=1意味着加0，历史块则携带各自log-gate共同竞争attention质量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-5d9c14bab0803e99">SAS 的 log-gate 应加在 softmax 内，还是在输出之后相乘？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asas-attention">SAS: Simple Attention Sparsification via End-to-End Optimization of Context Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent HY LLM Frontier / HKUST (Guangzhou) / HKUST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档要求把选中历史gate的对数加到attention logits，再统一softmax；历史gate共同归一化，当前块固定为1。输出后再乘改变不了同样的相对归一化关系，不是等价替代。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>当前块gate=1意味着加0，历史块则携带各自log-gate共同竞争attention质量。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.13141">原论文</a> · <a href="../../../../reproductions/2609.13141-sas-attention/">实现解读</a> · <a href="#qa-5d9c14bab0803e99">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:olmpool-long-context" data-paper-title="Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension 基础模型 Ai2 2026-08-10 以受控 7B 模型池隔离 normalization、GQA、预训练长度和滑窗注意力对长上下文扩展的复合影响。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 olmpool-long-context；单 seed 变化为 +92.19% 个百分点。  注意力与长上下文 网络架构 基础模型 长上下文：注意力、递归状态与记忆 OLMpool 长上下文研究为什么使用受控模型池？ 不同模型的归一化、GQA、预训练长度和滑窗设置常同时变化，容易混淆原因。受控模型池用于隔离这些较小架构选择及其组合对长上下文扩展的影响。 示意：两个模型长文本能力不同，不能在训练长度和结构都变了时只归因于其中一个开关。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-olmpool-long-context-26415a28" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c86c25ddeee07a58">OLMpool 长上下文研究为什么使用受控模型池？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aolmpool-long-context">Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ai2</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同模型的归一化、GQA、预训练长度和滑窗设置常同时变化，容易混淆原因。受控模型池用于隔离这些较小架构选择及其组合对长上下文扩展的影响。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个模型长文本能力不同，不能在训练长度和结构都变了时只归因于其中一个开关。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.10296">原论文</a> · <a href="../../../../reproductions/2608.10296-olmpool-long-context/">实现解读</a> · <a href="#qa-c86c25ddeee07a58">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:olmpool-long-context" data-paper-title="Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension 基础模型 Ai2 2026-08-10 以受控 7B 模型池隔离 normalization、GQA、预训练长度和滑窗注意力对长上下文扩展的复合影响。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 olmpool-long-context；单 seed 变化为 +92.19% 个百分点。  注意力与长上下文 网络架构 基础模型 长上下文：注意力、递归状态与记忆 比较两种长上下文扩展方法时，为什么只对齐模型参数量仍然不够？ 相同参数规模的模型也可能采用不同归一化、GQA、预训练窗口和滑窗结构；这些选择会共同改变长上下文行为。受控模型池把这些因素分开比较，防止把底座差异误归因于扩展方法。一个模型在某个长度上成功，不等于某种位置或注意力改动在所有底座上都有效。 教学例子：A模型训练时已见更长窗口，B模型只见短窗口；扩展后A更强，不能直接归功于其扩展算法。应先固定底座条件，再改变待研究的因素。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-43e1a94b62bc3646">比较两种长上下文扩展方法时，为什么只对齐模型参数量仍然不够？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aolmpool-long-context">Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ai2</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相同参数规模的模型也可能采用不同归一化、GQA、预训练窗口和滑窗结构；这些选择会共同改变长上下文行为。受控模型池把这些因素分开比较，防止把底座差异误归因于扩展方法。一个模型在某个长度上成功，不等于某种位置或注意力改动在所有底座上都有效。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>A模型训练时已见更长窗口，B模型只见短窗口；扩展后A更强，不能直接归功于其扩展算法。应先固定底座条件，再改变待研究的因素。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.10296">原论文</a> · <a href="../../../../reproductions/2608.10296-olmpool-long-context/">实现解读</a> · <a href="#qa-43e1a94b62bc3646">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:olmpool-long-context" data-paper-title="Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension 基础模型 Ai2 2026-08-10 以受控 7B 模型池隔离 normalization、GQA、预训练长度和滑窗注意力对长上下文扩展的复合影响。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 olmpool-long-context；单 seed 变化为 +92.19% 个百分点。  注意力与长上下文 网络架构 基础模型 长上下文：注意力、递归状态与记忆 对比两个现成模型，与在受控池里改变 normalization，有什么证据差别？ 现成模型可能还在数据、规模和训练日程上不同；受控变更才能更清楚分析某项结构因素。文档中的复合函数也提醒多因素可能交互，单因素趋势不能自动相加。 示意：先固定其它设置只换归一化，再检查它与GQA组合时是否保持同样方向。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-fa900f1f7e8c421c">对比两个现成模型，与在受控池里改变 normalization，有什么证据差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aolmpool-long-context">Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ai2</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>现成模型可能还在数据、规模和训练日程上不同；受控变更才能更清楚分析某项结构因素。文档中的复合函数也提醒多因素可能交互，单因素趋势不能自动相加。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先固定其它设置只换归一化，再检查它与GQA组合时是否保持同样方向。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.10296">原论文</a> · <a href="../../../../reproductions/2608.10296-olmpool-long-context/">实现解读</a> · <a href="#qa-fa900f1f7e8c421c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:olmpool-long-context" data-paper-title="Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension 基础模型 Ai2 2026-08-10 以受控 7B 模型池隔离 normalization、GQA、预训练长度和滑窗注意力对长上下文扩展的复合影响。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 olmpool-long-context；单 seed 变化为 +92.19% 个百分点。  注意力与长上下文 网络架构 基础模型 长上下文：注意力、递归状态与记忆 本地 mini-suite 通过，是否已经验证 7B 模型池的长上下文结论？ 没有。当前记录只确认相应核心数据流与计算路径可执行，未训练论文规模checkpoint或复跑完整benchmark。真正复核因果影响还需受控训练配置、相同扩展协议及任务评测。 示意：64条诊断样本上的准确率不能替代一组7B模型在长文本任务上的受控实验。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-31598daf655929d5">本地 mini-suite 通过，是否已经验证 7B 模型池的长上下文结论？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aolmpool-long-context">Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ai2</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。当前记录只确认相应核心数据流与计算路径可执行，未训练论文规模checkpoint或复跑完整benchmark。真正复核因果影响还需受控训练配置、相同扩展协议及任务评测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>64条诊断样本上的准确率不能替代一组7B模型在长文本任务上的受控实验。</p>
<p class="ar-learning-sources">依据：本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.10296">原论文</a> · <a href="../../../../reproductions/2608.10296-olmpool-long-context/">实现解读</a> · <a href="#qa-31598daf655929d5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:autonomy-heads" data-paper-title="Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry 基础模型 Institute of Computing Technology, Chinese Academy of Sciences 2026-08-07 直接从冻结 QK 投影的谱有效秩区分 retrieval 与 streaming heads，无需校准数据或运行时门控。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 autonomy-heads；单 seed 变化为 +92.19% 个百分点。  注意力与长上下文 稀疏注意力 基础模型 长上下文：注意力、递归状态与记忆 Autonomy-of-Heads 的“data-free”具体省掉了什么？ 它从冻结的Q/K投影分析头的几何结构，而不先准备校准样本来决定稀疏模式。省掉的是这一步校准和运行时门控，不代表原模型无需训练，也不代表稀疏后不必测效果。 示意：部署者可先检查权重分配头类型，但上线前仍需用实际任务核验答案是否受损。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-autonomy-heads-2d7238b5" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-460838ff2d888e65">Autonomy-of-Heads 的“data-free”具体省掉了什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aautonomy-heads">Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Computing Technology, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它从冻结的Q/K投影分析头的几何结构，而不先准备校准样本来决定稀疏模式。省掉的是这一步校准和运行时门控，不代表原模型无需训练，也不代表稀疏后不必测效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>部署者可先检查权重分配头类型，但上线前仍需用实际任务核验答案是否受损。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06849">原论文</a> · <a href="../../../../reproductions/2608.06849-autonomy-heads/">实现解读</a> · <a href="#qa-460838ff2d888e65">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:autonomy-heads" data-paper-title="Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry 基础模型 Institute of Computing Technology, Chinese Academy of Sciences 2026-08-07 直接从冻结 QK 投影的谱有效秩区分 retrieval 与 streaming heads，无需校准数据或运行时门控。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 autonomy-heads；单 seed 变化为 +92.19% 个百分点。  注意力与长上下文 稀疏注意力 基础模型 长上下文：注意力、递归状态与记忆 没有校准样本，Autonomy-of-Heads凭什么给不同head分配不同稀疏模式？ 它检查冻结的Q/K投影所形成的几何结构，用奇异值分布的谱有效秩描述头的潜在匹配能力，再区分偏检索和偏流式处理的头。选择依据来自模型参数，而非额外样本上运行一个门控器。因此省掉校准与运行时选择成本，但参数几何不能替代真实任务上的效果验证。 教学例子：两个头拥有相同窗口预算，但一个投影只突出很少方向，另一个能区分更多方向；方法先据此分配注意力方式，再检查任务是否真的保留所需证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-6d644b6b25fc1e45">没有校准样本，Autonomy-of-Heads凭什么给不同head分配不同稀疏模式？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aautonomy-heads">Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Computing Technology, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它检查冻结的Q/K投影所形成的几何结构，用奇异值分布的谱有效秩描述头的潜在匹配能力，再区分偏检索和偏流式处理的头。选择依据来自模型参数，而非额外样本上运行一个门控器。因此省掉校准与运行时选择成本，但参数几何不能替代真实任务上的效果验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个头拥有相同窗口预算，但一个投影只突出很少方向，另一个能区分更多方向；方法先据此分配注意力方式，再检查任务是否真的保留所需证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06849">原论文</a> · <a href="../../../../reproductions/2608.06849-autonomy-heads/">实现解读</a> · <a href="#qa-6d644b6b25fc1e45">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:autonomy-heads" data-paper-title="Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry 基础模型 Institute of Computing Technology, Chinese Academy of Sciences 2026-08-07 直接从冻结 QK 投影的谱有效秩区分 retrieval 与 streaming heads，无需校准数据或运行时门控。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 autonomy-heads；单 seed 变化为 +92.19% 个百分点。  注意力与长上下文 稀疏注意力 基础模型 长上下文：注意力、递归状态与记忆 根据冻结权重分头，与根据当前输入动态选择注意力范围有什么区别？ 权重几何给出较稳定的head分工，避免每个输入额外运行选择器；动态方法能随内容改变计算范围，却需要承担选择开销。两者适应对象不同，不能仅凭省校准就断言准确率更高。 示意：一个固定检索头始终承担远程访问；动态门控则可能对短文和长文分配不同范围。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4985c216e974937b">根据冻结权重分头，与根据当前输入动态选择注意力范围有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aautonomy-heads">Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Computing Technology, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>权重几何给出较稳定的head分工，避免每个输入额外运行选择器；动态方法能随内容改变计算范围，却需要承担选择开销。两者适应对象不同，不能仅凭省校准就断言准确率更高。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个固定检索头始终承担远程访问；动态门控则可能对短文和长文分配不同范围。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06849">原论文</a> · <a href="../../../../reproductions/2608.06849-autonomy-heads/">实现解读</a> · <a href="#qa-4985c216e974937b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:autonomy-heads" data-paper-title="Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry 基础模型 Institute of Computing Technology, Chinese Academy of Sciences 2026-08-07 直接从冻结 QK 投影的谱有效秩区分 retrieval 与 streaming heads，无需校准数据或运行时门控。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 autonomy-heads；单 seed 变化为 +92.19% 个百分点。  注意力与长上下文 稀疏注意力 基础模型 长上下文：注意力、递归状态与记忆 谱有效秩中的奇异值能直接当作概率计算熵吗？ 计算谱熵前要把奇异值变成归一化的谱分布，否则矩阵整体缩放会改变“熵”的含义。也要处理退化矩阵的数值边界；本地mini-suite只验证数据流，不能替代真实checkpoint评测。 示意：[2,2]和[20,20]归一化后都是[0.5,0.5]，应反映相同的谱分散程度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3f4c233f05443042">谱有效秩中的奇异值能直接当作概率计算熵吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aautonomy-heads">Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Computing Technology, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>计算谱熵前要把奇异值变成归一化的谱分布，否则矩阵整体缩放会改变“熵”的含义。也要处理退化矩阵的数值边界；本地mini-suite只验证数据流，不能替代真实checkpoint评测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>[2,2]和[20,20]归一化后都是[0.5,0.5]，应反映相同的谱分散程度。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06849">原论文</a> · <a href="../../../../reproductions/2608.06849-autonomy-heads/">实现解读</a> · <a href="#qa-3f4c233f05443042">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:dart" data-paper-title="DART: Decoded Attention over Recurrent States for Efficient Long-Context Sequence Modeling" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="DART: Decoded Attention over Recurrent States for Efficient Long-Context Sequence Modeling 基础模型 Zhejiang University 2026-08-03 保留 Mamba-2 chunk state contributions，解码 token-conditioned K/V 并执行 state-memory attention。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 dart；单 seed 变化为 +3.12% 个百分点。  网络架构 注意力与长上下文 基础模型 长上下文：注意力、递归状态与记忆 DART 为什么把递归状态当成可查询记忆，而不只当作最终摘要？ 固定容量递归状态可能在连续更新中丢掉旧信息。DART保留分块的状态贡献，让当前查询能再次选择相关的历史状态，为长期依赖增加可寻址入口。 示意：读完很多章节后要问第一章的人名，可以检索相应分块状态，而非只读最后摘要。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-dart-ebf1e36e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-322681ae4ecfb82c">DART 为什么把递归状态当成可查询记忆，而不只当作最终摘要？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adart">DART: Decoded Attention over Recurrent States for Efficient Long-Context Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定容量递归状态可能在连续更新中丢掉旧信息。DART保留分块的状态贡献，让当前查询能再次选择相关的历史状态，为长期依赖增加可寻址入口。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>读完很多章节后要问第一章的人名，可以检索相应分块状态，而非只读最后摘要。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.02032">原论文</a> · <a href="../../../../reproductions/2608.02032-dart/">实现解读</a> · <a href="#qa-322681ae4ecfb82c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:dart" data-paper-title="DART: Decoded Attention over Recurrent States for Efficient Long-Context Sequence Modeling" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="DART: Decoded Attention over Recurrent States for Efficient Long-Context Sequence Modeling 基础模型 Zhejiang University 2026-08-03 保留 Mamba-2 chunk state contributions，解码 token-conditioned K/V 并执行 state-memory attention。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 dart；单 seed 变化为 +3.12% 个百分点。  网络架构 注意力与长上下文 基础模型 长上下文：注意力、递归状态与记忆 DART为何保留多个chunk的递归状态，而不是只用最后一个状态回答问题？ 单个递归状态把很多历史合并到固定容量，某条旧信息可能被之后的更新覆盖。DART保留分块产生的状态贡献，把它们解码成可查询的K/V，再让当前token通过attention选择相关状态，并与Mamba路径融合。它为递归摘要增加了可寻址的记忆入口，代价是额外保存和检索状态。 教学例子：一章记作者、一章记年份；最终状态可能偏重后一章。查询作者时，可回到前一块的状态贡献，而不必指望最后状态仍完整携带两项信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c3968b3b16484d2a">DART为何保留多个chunk的递归状态，而不是只用最后一个状态回答问题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adart">DART: Decoded Attention over Recurrent States for Efficient Long-Context Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单个递归状态把很多历史合并到固定容量，某条旧信息可能被之后的更新覆盖。DART保留分块产生的状态贡献，把它们解码成可查询的K/V，再让当前token通过attention选择相关状态，并与Mamba路径融合。它为递归摘要增加了可寻址的记忆入口，代价是额外保存和检索状态。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一章记作者、一章记年份；最终状态可能偏重后一章。查询作者时，可回到前一块的状态贡献，而不必指望最后状态仍完整携带两项信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.02032">原论文</a> · <a href="../../../../reproductions/2608.02032-dart/">实现解读</a> · <a href="#qa-c3968b3b16484d2a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:dart" data-paper-title="DART: Decoded Attention over Recurrent States for Efficient Long-Context Sequence Modeling" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="DART: Decoded Attention over Recurrent States for Efficient Long-Context Sequence Modeling 基础模型 Zhejiang University 2026-08-03 保留 Mamba-2 chunk state contributions，解码 token-conditioned K/V 并执行 state-memory attention。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 dart；单 seed 变化为 +3.12% 个百分点。  网络架构 注意力与长上下文 基础模型 长上下文：注意力、递归状态与记忆 DART 的状态记忆与保存所有原始 token 的 KV cache，保存对象有何不同？ DART检索的是分块递归状态解码出的K/V，不是逐token原样保存的全部历史K/V。它通过状态压缩与额外attention平衡记忆容量和访问方式，压缩损失不会因此消失。 示意：查询会访问“某一块的状态表示”，不能默认其中每个旧词都能被逐字还原。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-339f62d5ba0a3b95">DART 的状态记忆与保存所有原始 token 的 KV cache，保存对象有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adart">DART: Decoded Attention over Recurrent States for Efficient Long-Context Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>DART检索的是分块递归状态解码出的K/V，不是逐token原样保存的全部历史K/V。它通过状态压缩与额外attention平衡记忆容量和访问方式，压缩损失不会因此消失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>查询会访问“某一块的状态表示”，不能默认其中每个旧词都能被逐字还原。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.02032">原论文</a> · <a href="../../../../reproductions/2608.02032-dart/">实现解读</a> · <a href="#qa-339f62d5ba0a3b95">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:dart" data-paper-title="DART: Decoded Attention over Recurrent States for Efficient Long-Context Sequence Modeling" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="DART: Decoded Attention over Recurrent States for Efficient Long-Context Sequence Modeling 基础模型 Zhejiang University 2026-08-03 保留 Mamba-2 chunk state contributions，解码 token-conditioned K/V 并执行 state-memory attention。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 dart；单 seed 变化为 +3.12% 个百分点。  网络架构 注意力与长上下文 基础模型 长上下文：注意力、递归状态与记忆 DART 融合式里的门 g_t 应作用在哪条路径上？ 文档表达式把Mamba输出作为主路径，再加上门控后的state-memory attention。实现需区分递归状态更新、状态到K/V的解码和查询读取，不能把门误用成对整个输出统一缩放。 示意：g_t接近0时，额外记忆读取贡献变小，但Mamba主路径仍保留。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d8a5db2ce8d1be02">DART 融合式里的门 g_t 应作用在哪条路径上？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adart">DART: Decoded Attention over Recurrent States for Efficient Long-Context Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档表达式把Mamba输出作为主路径，再加上门控后的state-memory attention。实现需区分递归状态更新、状态到K/V的解码和查询读取，不能把门误用成对整个输出统一缩放。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>g_t接近0时，额外记忆读取贡献变小，但Mamba主路径仍保留。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.02032">原论文</a> · <a href="../../../../reproductions/2608.02032-dart/">实现解读</a> · <a href="#qa-d8a5db2ce8d1be02">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ttcd" data-paper-title="Learning What to Remember: Test-Time Training via Context Distillation" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Learning What to Remember: Test-Time Training via Context Distillation 基础模型 Princeton University 2026-08-03 长窗口教师以隐藏状态差异监督短窗口学生的 fast weights，使有限记忆优先保留未来有用信息。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 ttcd；单 seed 变化为 +78.12% 个百分点。  注意力与长上下文 测试时训练 基础模型 长上下文：注意力、递归状态与记忆 TTCD 的长窗口教师与短窗口学生，最直接的信息条件差别是什么？ 教师能看到更长历史，学生受有限窗口或fast-weight记忆约束。教师hidden-state监督提供保留信息的目标，但不能据此假设部署学生也直接访问完整长历史。 示意：教师读过整段背景后给学习信号，学生运行时仍需依靠自己的有限记忆保留相关信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-ttcd-fe56ef12" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9888956d6e16b230">TTCD 的长窗口教师与短窗口学生，最直接的信息条件差别是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Attcd">Learning What to Remember: Test-Time Training via Context Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>教师能看到更长历史，学生受有限窗口或fast-weight记忆约束。教师hidden-state监督提供保留信息的目标，但不能据此假设部署学生也直接访问完整长历史。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教师读过整段背景后给学习信号，学生运行时仍需依靠自己的有限记忆保留相关信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01672">原论文</a> · <a href="../../../../reproductions/2608.01672-ttcd/">实现解读</a> · <a href="#qa-9888956d6e16b230">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ttcd" data-paper-title="Learning What to Remember: Test-Time Training via Context Distillation" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Learning What to Remember: Test-Time Training via Context Distillation 基础模型 Princeton University 2026-08-03 长窗口教师以隐藏状态差异监督短窗口学生的 fast weights，使有限记忆优先保留未来有用信息。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 ttcd；单 seed 变化为 +78.12% 个百分点。  注意力与长上下文 测试时训练 基础模型 长上下文：注意力、递归状态与记忆 TTCD让短窗口学生学习长窗口教师的什么，而不只是模仿最终答案？ 长窗口教师提供隐藏状态层面的目标，监督学生的fast weights保留对后续预测有用的上下文信息。学生有限记忆需要学会筛选，而不是平均压缩每个历史token。隐藏状态蒸馏能表达中间信息差距，但仍不保证压缩记忆完整保存教师看到的所有细节。 教学例子：长文开头定义了一个变量，教师到结尾仍能直接读取；短窗口学生需把该定义写进fast weights，使后续状态接近教师，而不仅背下某一次结尾答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-62897b0d29fdf49d">TTCD让短窗口学生学习长窗口教师的什么，而不只是模仿最终答案？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Attcd">Learning What to Remember: Test-Time Training via Context Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长窗口教师提供隐藏状态层面的目标，监督学生的fast weights保留对后续预测有用的上下文信息。学生有限记忆需要学会筛选，而不是平均压缩每个历史token。隐藏状态蒸馏能表达中间信息差距，但仍不保证压缩记忆完整保存教师看到的所有细节。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>长文开头定义了一个变量，教师到结尾仍能直接读取；短窗口学生需把该定义写进fast weights，使后续状态接近教师，而不仅背下某一次结尾答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01672">原论文</a> · <a href="../../../../reproductions/2608.01672-ttcd/">实现解读</a> · <a href="#qa-62897b0d29fdf49d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ttcd" data-paper-title="Learning What to Remember: Test-Time Training via Context Distillation" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Learning What to Remember: Test-Time Training via Context Distillation 基础模型 Princeton University 2026-08-03 长窗口教师以隐藏状态差异监督短窗口学生的 fast weights，使有限记忆优先保留未来有用信息。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 ttcd；单 seed 变化为 +78.12% 个百分点。  注意力与长上下文 测试时训练 基础模型 长上下文：注意力、递归状态与记忆 TTCD 的状态蒸馏，相对只匹配最终 token 输出多约束了什么？ 隐藏状态损失直接对齐教师与fast-weight学生的中间表征，而不只是最后预测概率。监督位置和表示空间不同，不可把它简写成普通输出蒸馏而忽略记忆学习路径。 示意：两个学生给出同一个下一词，但内部保留的历史信息仍可能不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5e538a1608b476d1">TTCD 的状态蒸馏，相对只匹配最终 token 输出多约束了什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Attcd">Learning What to Remember: Test-Time Training via Context Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>隐藏状态损失直接对齐教师与fast-weight学生的中间表征，而不只是最后预测概率。监督位置和表示空间不同，不可把它简写成普通输出蒸馏而忽略记忆学习路径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个学生给出同一个下一词，但内部保留的历史信息仍可能不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01672">原论文</a> · <a href="../../../../reproductions/2608.01672-ttcd/">实现解读</a> · <a href="#qa-5e538a1608b476d1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ttcd" data-paper-title="Learning What to Remember: Test-Time Training via Context Distillation" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Learning What to Remember: Test-Time Training via Context Distillation 基础模型 Princeton University 2026-08-03 长窗口教师以隐藏状态差异监督短窗口学生的 fast weights，使有限记忆优先保留未来有用信息。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 ttcd；单 seed 变化为 +78.12% 个百分点。  注意力与长上下文 测试时训练 基础模型 长上下文：注意力、递归状态与记忆 计算长窗口教师与 fast-weight 学生的差异时，为什么需要对齐位置和表示？ 文档损失逐t比较两条路径的hidden，要求比较同一位置且维度可对应；错位或广播会优化错误对象。当前mini-suite未训练论文规模checkpoint，不能据其分数宣称长文本能力复现。 示意：第20步学生状态应对齐教师第20步，而不是教师整篇最后一步的表示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7295b9f8ace3f89d">计算长窗口教师与 fast-weight 学生的差异时，为什么需要对齐位置和表示？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Attcd">Learning What to Remember: Test-Time Training via Context Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档损失逐t比较两条路径的hidden，要求比较同一位置且维度可对应；错位或广播会优化错误对象。当前mini-suite未训练论文规模checkpoint，不能据其分数宣称长文本能力复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第20步学生状态应对齐教师第20步，而不是教师整篇最后一步的表示。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01672">原论文</a> · <a href="../../../../reproductions/2608.01672-ttcd/">实现解读</a> · <a href="#qa-7295b9f8ace3f89d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:transmem" data-paper-title="TransMem: Transforming Hidden States into Memory for Large Language Models" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="TransMem: Transforming Hidden States into Memory for Large Language Models 基础模型 Authors did not disclose affiliation 2026-07-31 将冻结骨干的稀疏历史 hidden states 变换成可复用参数记忆，并用 evidence-conditioned self-distillation 学门控。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 transmem；单 seed 变化为 +12.50% 个百分点。  注意力与长上下文 Agent 记忆 基础模型 长上下文：注意力、递归状态与记忆 TransMem 的 frozen backbone 与可学习记忆门控，是否表示所有参数都不更新？ 冻结指骨干保持不变，记忆门控仍需学习。evidence-conditioned self-distillation用于学习怎样使用历史记忆，不能把冻结骨干写成整个系统没有学习，也不能把记忆状态变化误认成骨干权重更新。 示意：主模型不变，新增记忆支路仍可学习何时把历史信息加回当前状态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-transmem-2625c67f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-27cc9d050984c6eb">TransMem 的 frozen backbone 与可学习记忆门控，是否表示所有参数都不更新？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atransmem">TransMem: Transforming Hidden States into Memory for Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冻结指骨干保持不变，记忆门控仍需学习。evidence-conditioned self-distillation用于学习怎样使用历史记忆，不能把冻结骨干写成整个系统没有学习，也不能把记忆状态变化误认成骨干权重更新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>主模型不变，新增记忆支路仍可学习何时把历史信息加回当前状态。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.29032">原论文</a> · <a href="../../../../reproductions/2607.29032-transmem/">实现解读</a> · <a href="#qa-27cc9d050984c6eb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:transmem" data-paper-title="TransMem: Transforming Hidden States into Memory for Large Language Models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="TransMem: Transforming Hidden States into Memory for Large Language Models 基础模型 Authors did not disclose affiliation 2026-07-31 将冻结骨干的稀疏历史 hidden states 变换成可复用参数记忆，并用 evidence-conditioned self-distillation 学门控。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 transmem；单 seed 变化为 +12.50% 个百分点。  注意力与长上下文 Agent 记忆 基础模型 长上下文：注意力、递归状态与记忆 TransMem把历史hidden states转成参数记忆，与一直保留原始历史有什么区别？ 它抽取冻结骨干的稀疏历史状态，再变换成可复用的记忆增量，并通过门控制其对当前状态的影响。原始上下文不再每次逐token参与同样的检索，信息经过变换与压缩，因此可复用性与细节保真之间有取舍。学习门控也不代表骨干本体已随每段历史重新训练。 教学例子：把一段已读说明压成可调用的记忆增量，后续问题可利用这份信息；如果压缩时丢了一个精确编号，记忆模块不能仅凭复用就保证把编号还原出来。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-322b52536e46b91b">TransMem把历史hidden states转成参数记忆，与一直保留原始历史有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atransmem">TransMem: Transforming Hidden States into Memory for Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它抽取冻结骨干的稀疏历史状态，再变换成可复用的记忆增量，并通过门控制其对当前状态的影响。原始上下文不再每次逐token参与同样的检索，信息经过变换与压缩，因此可复用性与细节保真之间有取舍。学习门控也不代表骨干本体已随每段历史重新训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把一段已读说明压成可调用的记忆增量，后续问题可利用这份信息；如果压缩时丢了一个精确编号，记忆模块不能仅凭复用就保证把编号还原出来。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.29032">原论文</a> · <a href="../../../../reproductions/2607.29032-transmem/">实现解读</a> · <a href="#qa-322b52536e46b91b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:transmem" data-paper-title="TransMem: Transforming Hidden States into Memory for Large Language Models" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="TransMem: Transforming Hidden States into Memory for Large Language Models 基础模型 Authors did not disclose affiliation 2026-07-31 将冻结骨干的稀疏历史 hidden states 变换成可复用参数记忆，并用 evidence-conditioned self-distillation 学门控。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 transmem；单 seed 变化为 +12.50% 个百分点。  注意力与长上下文 Agent 记忆 基础模型 长上下文：注意力、递归状态与记忆 TransMem 的参数记忆，与直接把旧文本拼到上下文里有什么取舍？ 参数记忆通过T(H_sparse)把稀疏历史变换后注入hidden；文本拼接让模型重新读取原始token。前者改变了存储和融合方式，也可能丢失未被选中的细节，不能视为逐字缓存。 示意：记忆可保留一项事实的表示，但不保证能原样找回被省略段落的每一个词。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-eb5007a2cbb3c70f">TransMem 的参数记忆，与直接把旧文本拼到上下文里有什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atransmem">TransMem: Transforming Hidden States into Memory for Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>参数记忆通过T(H_sparse)把稀疏历史变换后注入hidden；文本拼接让模型重新读取原始token。前者改变了存储和融合方式，也可能丢失未被选中的细节，不能视为逐字缓存。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>记忆可保留一项事实的表示，但不保证能原样找回被省略段落的每一个词。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.29032">原论文</a> · <a href="../../../../reproductions/2607.29032-transmem/">实现解读</a> · <a href="#qa-eb5007a2cbb3c70f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:transmem" data-paper-title="TransMem: Transforming Hidden States into Memory for Large Language Models" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="TransMem: Transforming Hidden States into Memory for Large Language Models 基础模型 Authors did not disclose affiliation 2026-07-31 将冻结骨干的稀疏历史 hidden states 变换成可复用参数记忆，并用 evidence-conditioned self-distillation 学门控。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 transmem；单 seed 变化为 +12.50% 个百分点。  注意力与长上下文 Agent 记忆 基础模型 长上下文：注意力、递归状态与记忆 TransMem 的门控残差应该替换原 hidden，还是加在原 hidden 上？ 文档写作h′=h+g⊙T(H_sparse)，原hidden是保留的主路径。实现需区分稀疏历史选择、变换与门控注入；当前mini-suite未训练论文规模checkpoint，不能由式子可执行宣称完整复现。 示意：g为0时输出回到原hidden，而不是变成全零表示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-219e33d6432ab044">TransMem 的门控残差应该替换原 hidden，还是加在原 hidden 上？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atransmem">TransMem: Transforming Hidden States into Memory for Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档写作h′=h+g⊙T(H_sparse)，原hidden是保留的主路径。实现需区分稀疏历史选择、变换与门控注入；当前mini-suite未训练论文规模checkpoint，不能由式子可执行宣称完整复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>g为0时输出回到原hidden，而不是变成全零表示。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.29032">原论文</a> · <a href="../../../../reproductions/2607.29032-transmem/">实现解读</a> · <a href="#qa-219e33d6432ab044">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gzip-sparse-attention" data-paper-title="Parameter-free Adaptive Sparse Attention via Compression-Based Content Selection" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Parameter-free Adaptive Sparse Attention via Compression-Based Content Selection 基础模型 Pennsylvania State University 2026-07-23 固定 BigBird/Longformer mask 不理解内容，learned mask 又需要额外参数、梯度估计或专用 kernel。论文把字节序列切成固定 block，用 gzip 压缩率作为无需训练的信息密度信号：高于样本均值的 literal blocks 互相建立长程连接，所有 block 保留局部窗口，不设置固定 global token。50% heads 只看 local、25% 只看 literal long-range、25% 使用两者并集。 Fidelity: 核心机制复现。真实逐块执行 gzip、生成样本自适应 mask 并训练同参数 ByteLM；缩小 context、模型和训练步数。本地实现确实逐样本调用 gzip 并执行三类 head mask，但 PyTorch 仍计算 dense score matrix 后 masking，所以 edge 数下降不等于 wall-clock 加速。没有下载 28,602 本 PG-19、训练 92M 模型或使用 8K context；小预算负结果不能反驳论文的长上下文训练结论。  llm sparse-attention long-context compression 基础模型 长上下文：注意力、递归状态与记忆 Gzip-guided Sparse Attention 为什么先把原始 bytes 分块压缩？ 它用压缩率作为无需训练的内容密度信号，识别可能携带较多独特字节的块，再决定长程连接。这个信号是启发式代理，不是语义重要性标签。 示意：重复模板与独特编号的压缩率可能不同，但难压缩的乱码也未必对答案有用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-gzip-sparse-attention-4236c23c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b01cb35887c2065a">Gzip-guided Sparse Attention 为什么先把原始 bytes 分块压缩？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agzip-sparse-attention">Parameter-free Adaptive Sparse Attention via Compression-Based Content Selection</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pennsylvania State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它用压缩率作为无需训练的内容密度信号，识别可能携带较多独特字节的块，再决定长程连接。这个信号是启发式代理，不是语义重要性标签。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>重复模板与独特编号的压缩率可能不同，但难压缩的乱码也未必对答案有用。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21752">原论文</a> · <a href="../../../../reproductions/2607.21752-gzip-sparse-attention/">实现解读</a> · <a href="#qa-b01cb35887c2065a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gzip-sparse-attention" data-paper-title="Parameter-free Adaptive Sparse Attention via Compression-Based Content Selection" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Parameter-free Adaptive Sparse Attention via Compression-Based Content Selection 基础模型 Pennsylvania State University 2026-07-23 固定 BigBird/Longformer mask 不理解内容，learned mask 又需要额外参数、梯度估计或专用 kernel。论文把字节序列切成固定 block，用 gzip 压缩率作为无需训练的信息密度信号：高于样本均值的 literal blocks 互相建立长程连接，所有 block 保留局部窗口，不设置固定 global token。50% heads 只看 local、25% 只看 literal long-range、25% 使用两者并集。 Fidelity: 核心机制复现。真实逐块执行 gzip、生成样本自适应 mask 并训练同参数 ByteLM；缩小 context、模型和训练步数。本地实现确实逐样本调用 gzip 并执行三类 head mask，但 PyTorch 仍计算 dense score matrix 后 masking，所以 edge 数下降不等于 wall-clock 加速。没有下载 28,602 本 PG-19、训练 92M 模型或使用 8K context；小预算负结果不能反驳论文的长上下文训练结论。  llm sparse-attention long-context compression 基础模型 长上下文：注意力、递归状态与记忆 gzip压不动的block为什么获得长程连接，这是否等于找到了重要内容？ 方法把较难压缩的字节块视为literal信息较丰富，以样本平均压缩率为阈值，让这些块之间建立长程边，同时保留局部窗口与因果约束。压缩率是无需训练的内容选择信号，并非语义重要性的真值；随机噪声也可能难压缩，而且literal块过多时长程边仍会变贵。 教学例子：重复模板容易压缩，独特编号往往更难压缩，后者可能需要跨段读取；但一段随机乱码也难压缩，所以还得验证这种连接是否服务于实际问题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-ff5a539f7aa258a3">gzip压不动的block为什么获得长程连接，这是否等于找到了重要内容？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agzip-sparse-attention">Parameter-free Adaptive Sparse Attention via Compression-Based Content Selection</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pennsylvania State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>方法把较难压缩的字节块视为literal信息较丰富，以样本平均压缩率为阈值，让这些块之间建立长程边，同时保留局部窗口与因果约束。压缩率是无需训练的内容选择信号，并非语义重要性的真值；随机噪声也可能难压缩，而且literal块过多时长程边仍会变贵。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>重复模板容易压缩，独特编号往往更难压缩，后者可能需要跨段读取；但一段随机乱码也难压缩，所以还得验证这种连接是否服务于实际问题。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21752">原论文</a> · <a href="../../../../reproductions/2607.21752-gzip-sparse-attention/">实现解读</a> · <a href="#qa-ff5a539f7aa258a3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gzip-sparse-attention" data-paper-title="Parameter-free Adaptive Sparse Attention via Compression-Based Content Selection" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Parameter-free Adaptive Sparse Attention via Compression-Based Content Selection 基础模型 Pennsylvania State University 2026-07-23 固定 BigBird/Longformer mask 不理解内容，learned mask 又需要额外参数、梯度估计或专用 kernel。论文把字节序列切成固定 block，用 gzip 压缩率作为无需训练的信息密度信号：高于样本均值的 literal blocks 互相建立长程连接，所有 block 保留局部窗口，不设置固定 global token。50% heads 只看 local、25% 只看 literal long-range、25% 使用两者并集。 Fidelity: 核心机制复现。真实逐块执行 gzip、生成样本自适应 mask 并训练同参数 ByteLM；缩小 context、模型和训练步数。本地实现确实逐样本调用 gzip 并执行三类 head mask，但 PyTorch 仍计算 dense score matrix 后 masking，所以 edge 数下降不等于 wall-clock 加速。没有下载 28,602 本 PG-19、训练 92M 模型或使用 8K context；小预算负结果不能反驳论文的长上下文训练结论。  llm sparse-attention long-context compression 基础模型 长上下文：注意力、递归状态与记忆 相对固定 BigBird/Longformer mask，gzip mask 的变化来自哪里？ 固定mask按预设位置建立边；gzip方案按每个样本的块压缩率改变literal长程边，同时保留局部窗口。它无需学习mask参数，但引入逐样本压缩与建mask工作，不能只比较边数就断言更快。 示意：把独特段落从文首移到文末，内容驱动的长程连接可随它改变，而固定位置模式不因此改变。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-95f4b53dbe2b61f2">相对固定 BigBird/Longformer mask，gzip mask 的变化来自哪里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agzip-sparse-attention">Parameter-free Adaptive Sparse Attention via Compression-Based Content Selection</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pennsylvania State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定mask按预设位置建立边；gzip方案按每个样本的块压缩率改变literal长程边，同时保留局部窗口。它无需学习mask参数，但引入逐样本压缩与建mask工作，不能只比较边数就断言更快。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把独特段落从文首移到文末，内容驱动的长程连接可随它改变，而固定位置模式不因此改变。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21752">原论文</a> · <a href="../../../../reproductions/2607.21752-gzip-sparse-attention/">实现解读</a> · <a href="#qa-95f4b53dbe2b61f2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gzip-sparse-attention" data-paper-title="Parameter-free Adaptive Sparse Attention via Compression-Based Content Selection" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Parameter-free Adaptive Sparse Attention via Compression-Based Content Selection 基础模型 Pennsylvania State University 2026-07-23 固定 BigBird/Longformer mask 不理解内容，learned mask 又需要额外参数、梯度估计或专用 kernel。论文把字节序列切成固定 block，用 gzip 压缩率作为无需训练的信息密度信号：高于样本均值的 literal blocks 互相建立长程连接，所有 block 保留局部窗口，不设置固定 global token。50% heads 只看 local、25% 只看 literal long-range、25% 使用两者并集。 Fidelity: 核心机制复现。真实逐块执行 gzip、生成样本自适应 mask 并训练同参数 ByteLM；缩小 context、模型和训练步数。本地实现确实逐样本调用 gzip 并执行三类 head mask，但 PyTorch 仍计算 dense score matrix 后 masking，所以 edge 数下降不等于 wall-clock 加速。没有下载 28,602 本 PG-19、训练 92M 模型或使用 8K context；小预算负结果不能反驳论文的长上下文训练结论。  llm sparse-attention long-context compression 基础模型 长上下文：注意力、递归状态与记忆 为什么合并 literal/local/self 边后，还必须与 causal mask 相交？ 这些连接规则只说明哪些块相关，并不保证时间顺序；若直接使用并集，当前token可能读到未来。还需按三类head分配相应mask；本地dense score后masking并不实现稀疏kernel加速。 示意：两个literal块位于前后章节，早期token不能因为两块都被选中就读取后面章节。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-33a4f2c162cacc0b">为什么合并 literal/local/self 边后，还必须与 causal mask 相交？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agzip-sparse-attention">Parameter-free Adaptive Sparse Attention via Compression-Based Content Selection</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pennsylvania State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这些连接规则只说明哪些块相关，并不保证时间顺序；若直接使用并集，当前token可能读到未来。还需按三类head分配相应mask；本地dense score后masking并不实现稀疏kernel加速。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个literal块位于前后章节，早期token不能因为两块都被选中就读取后面章节。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21752">原论文</a> · <a href="../../../../reproductions/2607.21752-gzip-sparse-attention/">实现解读</a> · <a href="#qa-33a4f2c162cacc0b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mobius-rope" data-paper-title="Anti-Periodic Positional Encoding: Möbius Boundary Conditions Make In-Context Retrieval Reliable" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Anti-Periodic Positional Encoding: Möbius Boundary Conditions Make In-Context Retrieval Reliable 基础模型 Independent researcher 2026-07-23 标准 RoPE 的随机种子会显著影响长距离 needle retrieval。论文为部分 attention heads 使用反周期频率梯度，使跨完整训练窗口的旋转恒为；其余 heads 保留标准 RoPE，以维持语言建模能力。 未运行 48 个大模型、2B tokens/run 和六 seed 方差检验；Fidelity: 核心机制复现。真实训练 standard RoPE 与 25% heads Möbius RoPE；缩小模型、语料和随机种子规模。未运行 48 个大模型、2B tokens/run 和六 seed 方差检验；本地 needle task 是可审计的机制验证，且两组都接受相同 retrieval curriculum。本地对照口径：基线为 standard RoPE；  llm-architecture positional-encoding long-context 基础模型 长上下文：注意力、递归状态与记忆 Möbius RoPE 想改善的是哪种长距离检索不稳定？ 文档指出标准RoPE在长距离needle retrieval上可能受随机种子显著影响。Möbius为部分头加入反周期频率边界，尝试稳定跨训练窗口的相位关系，同时让其余头保留标准RoPE。 示意：同一长文本里插入同一个needle，不同训练seed的检索表现可能差异很大。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-mobius-rope-d829e106" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a35ee6b0b63900fc">Möbius RoPE 想改善的是哪种长距离检索不稳定？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amobius-rope">Anti-Periodic Positional Encoding: Möbius Boundary Conditions Make In-Context Retrieval Reliable</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Independent researcher</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档指出标准RoPE在长距离needle retrieval上可能受随机种子显著影响。Möbius为部分头加入反周期频率边界，尝试稳定跨训练窗口的相位关系，同时让其余头保留标准RoPE。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一长文本里插入同一个needle，不同训练seed的检索表现可能差异很大。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21405">原论文</a> · <a href="../../../../reproductions/2607.21405-mobius-rope/">实现解读</a> · <a href="#qa-a35ee6b0b63900fc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mobius-rope" data-paper-title="Anti-Periodic Positional Encoding: Möbius Boundary Conditions Make In-Context Retrieval Reliable" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Anti-Periodic Positional Encoding: Möbius Boundary Conditions Make In-Context Retrieval Reliable 基础模型 Independent researcher 2026-07-23 标准 RoPE 的随机种子会显著影响长距离 needle retrieval。论文为部分 attention heads 使用反周期频率梯度，使跨完整训练窗口的旋转恒为；其余 heads 保留标准 RoPE，以维持语言建模能力。 未运行 48 个大模型、2B tokens/run 和六 seed 方差检验；Fidelity: 核心机制复现。真实训练 standard RoPE 与 25% heads Möbius RoPE；缩小模型、语料和随机种子规模。未运行 48 个大模型、2B tokens/run 和六 seed 方差检验；本地 needle task 是可审计的机制验证，且两组都接受相同 retrieval curriculum。本地对照口径：基线为 standard RoPE；  llm-architecture positional-encoding long-context 基础模型 长上下文：注意力、递归状态与记忆 Möbius位置编码跨训练窗口旋转成负单位阵，和标准RoPE有何不同？ 它为部分头使用反周期频率，使相隔一个训练窗口的旋转为负单位阵、两个窗口后回到单位阵。这样显式约束长距离位置关系；其余头保留标准RoPE以兼顾语言建模。它是改变某些头的位置几何，不是增加可访问的历史内容，也不自动保证所有长度上的检索。 教学例子：窗口长度为N时，相隔N的位置在这些头上受到统一反向旋转，而相隔2N回到同向；内容是否被正确检索，仍需由查询、键和训练共同决定。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-9cea57bf909d2052">Möbius位置编码跨训练窗口旋转成负单位阵，和标准RoPE有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amobius-rope">Anti-Periodic Positional Encoding: Möbius Boundary Conditions Make In-Context Retrieval Reliable</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Independent researcher</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它为部分头使用反周期频率，使相隔一个训练窗口的旋转为负单位阵、两个窗口后回到单位阵。这样显式约束长距离位置关系；其余头保留标准RoPE以兼顾语言建模。它是改变某些头的位置几何，不是增加可访问的历史内容，也不自动保证所有长度上的检索。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>窗口长度为N时，相隔N的位置在这些头上受到统一反向旋转，而相隔2N回到同向；内容是否被正确检索，仍需由查询、键和训练共同决定。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21405">原论文</a> · <a href="../../../../reproductions/2607.21405-mobius-rope/">实现解读</a> · <a href="#qa-9cea57bf909d2052">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mobius-rope" data-paper-title="Anti-Periodic Positional Encoding: Möbius Boundary Conditions Make In-Context Retrieval Reliable" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Anti-Periodic Positional Encoding: Möbius Boundary Conditions Make In-Context Retrieval Reliable 基础模型 Independent researcher 2026-07-23 标准 RoPE 的随机种子会显著影响长距离 needle retrieval。论文为部分 attention heads 使用反周期频率梯度，使跨完整训练窗口的旋转恒为；其余 heads 保留标准 RoPE，以维持语言建模能力。 未运行 48 个大模型、2B tokens/run 和六 seed 方差检验；Fidelity: 核心机制复现。真实训练 standard RoPE 与 25% heads Möbius RoPE；缩小模型、语料和随机种子规模。未运行 48 个大模型、2B tokens/run 和六 seed 方差检验；本地 needle task 是可审计的机制验证，且两组都接受相同 retrieval curriculum。本地对照口径：基线为 standard RoPE；  llm-architecture positional-encoding long-context 基础模型 长上下文：注意力、递归状态与记忆 Möbius 频率相对标准 RoPE，多出了什么明确的边界条件？ 它把部分头的二维频率设为π(2i+1)/N，使跨N位置的旋转为-I、跨2N为I；标准RoPE头继续保留。差异在相位结构，不能把这项结构约束等同于已经测得检索提升。 示意：相隔一个训练窗口时相位反转，两个窗口后复原，而非任意缩放全部头的频率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7909d719708669df">Möbius 频率相对标准 RoPE，多出了什么明确的边界条件？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amobius-rope">Anti-Periodic Positional Encoding: Möbius Boundary Conditions Make In-Context Retrieval Reliable</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Independent researcher</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它把部分头的二维频率设为π(2i+1)/N，使跨N位置的旋转为-I、跨2N为I；标准RoPE头继续保留。差异在相位结构，不能把这项结构约束等同于已经测得检索提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>相隔一个训练窗口时相位反转，两个窗口后复原，而非任意缩放全部头的频率。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21405">原论文</a> · <a href="../../../../reproductions/2607.21405-mobius-rope/">实现解读</a> · <a href="#qa-7909d719708669df">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mobius-rope" data-paper-title="Anti-Periodic Positional Encoding: Möbius Boundary Conditions Make In-Context Retrieval Reliable" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Anti-Periodic Positional Encoding: Möbius Boundary Conditions Make In-Context Retrieval Reliable 基础模型 Independent researcher 2026-07-23 标准 RoPE 的随机种子会显著影响长距离 needle retrieval。论文为部分 attention heads 使用反周期频率梯度，使跨完整训练窗口的旋转恒为；其余 heads 保留标准 RoPE，以维持语言建模能力。 未运行 48 个大模型、2B tokens/run 和六 seed 方差检验；Fidelity: 核心机制复现。真实训练 standard RoPE 与 25% heads Möbius RoPE；缩小模型、语料和随机种子规模。未运行 48 个大模型、2B tokens/run 和六 seed 方差检验；本地 needle task 是可审计的机制验证，且两组都接受相同 retrieval curriculum。本地对照口径：基线为 standard RoPE；  llm-architecture positional-encoding long-context 基础模型 长上下文：注意力、递归状态与记忆 实现 Möbius RoPE 时，N 应随当前推理长度动态改写吗？ 文档把N定义为固定训练上下文，本地固定N=64并仅替换四头中的一头。若每次随输入长度改N，相同位置就可能使用不同频率，改变原本的边界定义。小模型负结果仍需如实保留。 示意：长度32与80的输入都应使用同一训练N，而非分别按32和80重建这张频率表。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c8f3ab0c1ff95aa5">实现 Möbius RoPE 时，N 应随当前推理长度动态改写吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amobius-rope">Anti-Periodic Positional Encoding: Möbius Boundary Conditions Make In-Context Retrieval Reliable</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Independent researcher</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档把N定义为固定训练上下文，本地固定N=64并仅替换四头中的一头。若每次随输入长度改N，相同位置就可能使用不同频率，改变原本的边界定义。小模型负结果仍需如实保留。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>长度32与80的输入都应使用同一训练N，而非分别按32和80重建这张频率表。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21405">原论文</a> · <a href="../../../../reproductions/2607.21405-mobius-rope/">实现解读</a> · <a href="#qa-c8f3ab0c1ff95aa5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:naju" data-paper-title="Naju: A Native Discrete State-Space Model with Independent Retention and Writing for Long-Sequence Memory" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Naju: A Native Discrete State-Space Model with Independent Retention and Writing for Long-Sequence Memory 基础模型 Independent researchers 2026-07-23 Mamba 从连续时间系统离散化得到转移，单一耦合门也容易形成“强保留就难写入”的约束。Naju 直接参数化离散 pole，将 retain gate 和 write gate 分开，并保留 token-dependent 方向、短程因果卷积、直接 feedthrough 与输出调制。 Fidelity: 核心机制复现。真实执行 native-discrete selective recurrence 的完整 block；缩小模型与预训练预算。Python sequential recurrence 与论文 affine scan 数学等价，但没有作者 fused parallel kernel。未复跑 1.2B-token WikiText-103、Mamba/Mamba-2/xLSTM 和完整 LRA/MQAR；本地负结果只适用于当前规模。本地对照口径：基线为同 token、optimizer、70 steps 的 96-d、3-layer Transformer；  llm-architecture state-space-model long-context 基础模型 长上下文：注意力、递归状态与记忆 Naju 为什么把“保留旧状态”和“写入新信息”分开控制？ 若两个动作被同一门耦合，强保留可能限制新信息写入。Naju分别参数化retain与write门，并直接使用离散状态转移，使两种需求能独立调节。 示意：读到关键补充事实时，可以既保留旧事实，又写入新事实，而非必须二选一。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-naju-616fb3d6" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5585d4a9b7fbb306">Naju 为什么把“保留旧状态”和“写入新信息”分开控制？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Anaju">Naju: A Native Discrete State-Space Model with Independent Retention and Writing for Long-Sequence Memory</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Independent researchers</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若两个动作被同一门耦合，强保留可能限制新信息写入。Naju分别参数化retain与write门，并直接使用离散状态转移，使两种需求能独立调节。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>读到关键补充事实时，可以既保留旧事实，又写入新事实，而非必须二选一。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21000">原论文</a> · <a href="../../../../reproductions/2607.21000-naju/">实现解读</a> · <a href="#qa-5585d4a9b7fbb306">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:naju" data-paper-title="Naju: A Native Discrete State-Space Model with Independent Retention and Writing for Long-Sequence Memory" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Naju: A Native Discrete State-Space Model with Independent Retention and Writing for Long-Sequence Memory 基础模型 Independent researchers 2026-07-23 Mamba 从连续时间系统离散化得到转移，单一耦合门也容易形成“强保留就难写入”的约束。Naju 直接参数化离散 pole，将 retain gate 和 write gate 分开，并保留 token-dependent 方向、短程因果卷积、直接 feedthrough 与输出调制。 Fidelity: 核心机制复现。真实执行 native-discrete selective recurrence 的完整 block；缩小模型与预训练预算。Python sequential recurrence 与论文 affine scan 数学等价，但没有作者 fused parallel kernel。未复跑 1.2B-token WikiText-103、Mamba/Mamba-2/xLSTM 和完整 LRA/MQAR；本地负结果只适用于当前规模。本地对照口径：基线为同 token、optimizer、70 steps 的 96-d、3-layer Transformer；  llm-architecture state-space-model long-context 基础模型 长上下文：注意力、递归状态与记忆 Naju为什么把保留门和写入门分开，不能只用一个互补门？ 若写入量固定等于一减保留量，强保留旧信息就会同时压低新信息写入。Naju直接参数化离散转移，并独立控制retain和write，所以可以同时较强地保留旧状态并接收新线索。token相关读写方向、局部卷积和直通路径仍各有作用，不应把它简化为一个固定指数滑动平均。 教学例子：已有状态记录人物名字，当前token补充其年龄；独立门允许保留名字并写入年龄，而不是为了增加年龄信息就被迫按同一比例擦掉旧状态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-2e4296cda59e007b">Naju为什么把保留门和写入门分开，不能只用一个互补门？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Anaju">Naju: A Native Discrete State-Space Model with Independent Retention and Writing for Long-Sequence Memory</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Independent researchers</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若写入量固定等于一减保留量，强保留旧信息就会同时压低新信息写入。Naju直接参数化离散转移，并独立控制retain和write，所以可以同时较强地保留旧状态并接收新线索。token相关读写方向、局部卷积和直通路径仍各有作用，不应把它简化为一个固定指数滑动平均。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>已有状态记录人物名字，当前token补充其年龄；独立门允许保留名字并写入年龄，而不是为了增加年龄信息就被迫按同一比例擦掉旧状态。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21000">原论文</a> · <a href="../../../../reproductions/2607.21000-naju/">实现解读</a> · <a href="#qa-2e4296cda59e007b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:naju" data-paper-title="Naju: A Native Discrete State-Space Model with Independent Retention and Writing for Long-Sequence Memory" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Naju: A Native Discrete State-Space Model with Independent Retention and Writing for Long-Sequence Memory 基础模型 Independent researchers 2026-07-23 Mamba 从连续时间系统离散化得到转移，单一耦合门也容易形成“强保留就难写入”的约束。Naju 直接参数化离散 pole，将 retain gate 和 write gate 分开，并保留 token-dependent 方向、短程因果卷积、直接 feedthrough 与输出调制。 Fidelity: 核心机制复现。真实执行 native-discrete selective recurrence 的完整 block；缩小模型与预训练预算。Python sequential recurrence 与论文 affine scan 数学等价，但没有作者 fused parallel kernel。未复跑 1.2B-token WikiText-103、Mamba/Mamba-2/xLSTM 和完整 LRA/MQAR；本地负结果只适用于当前规模。本地对照口径：基线为同 token、optimizer、70 steps 的 96-d、3-layer Transformer；  llm-architecture state-space-model long-context 基础模型 长上下文：注意力、递归状态与记忆 Naju 的原生离散 pole 与 Mamba 的连续系统离散化，出发点有什么不同？ Naju直接参数化离散保留系数，Mamba路径从连续动力学及输入相关步长得到转移。两者都可递归，但参数化和门的耦合关系不同，不能只因都叫SSM就替换公式。 示意：一个模型直接学习每步保留比例，另一个经时间步长和连续系统矩阵得到该比例。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e36079e843449dc1">Naju 的原生离散 pole 与 Mamba 的连续系统离散化，出发点有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Anaju">Naju: A Native Discrete State-Space Model with Independent Retention and Writing for Long-Sequence Memory</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Independent researchers</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Naju直接参数化离散保留系数，Mamba路径从连续动力学及输入相关步长得到转移。两者都可递归，但参数化和门的耦合关系不同，不能只因都叫SSM就替换公式。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个模型直接学习每步保留比例，另一个经时间步长和连续系统矩阵得到该比例。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21000">原论文</a> · <a href="../../../../reproductions/2607.21000-naju/">实现解读</a> · <a href="#qa-e36079e843449dc1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:naju" data-paper-title="Naju: A Native Discrete State-Space Model with Independent Retention and Writing for Long-Sequence Memory" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Naju: A Native Discrete State-Space Model with Independent Retention and Writing for Long-Sequence Memory 基础模型 Independent researchers 2026-07-23 Mamba 从连续时间系统离散化得到转移，单一耦合门也容易形成“强保留就难写入”的约束。Naju 直接参数化离散 pole，将 retain gate 和 write gate 分开，并保留 token-dependent 方向、短程因果卷积、直接 feedthrough 与输出调制。 Fidelity: 核心机制复现。真实执行 native-discrete selective recurrence 的完整 block；缩小模型与预训练预算。Python sequential recurrence 与论文 affine scan 数学等价，但没有作者 fused parallel kernel。未复跑 1.2B-token WikiText-103、Mamba/Mamba-2/xLSTM 和完整 LRA/MQAR；本地负结果只适用于当前规模。本地对照口径：基线为同 token、optimizer、70 steps 的 96-d、3-layer Transformer；  llm-architecture state-space-model long-context 基础模型 长上下文：注意力、递归状态与记忆 preserve-first 初始化应该怎样反映在 Naju 的两个 sigmoid 门上？ 文档给出forget_bias=5、write_bias=-2，使初始保留接近1、写入较小；它不是把两个门设为同一个值。还需保留token相关B/C与直接feedthrough，才能对应记录的完整本地路径。 示意：sigmoid(5)约0.993、sigmoid(-2)约0.119，分别表达强保留与弱初始写入。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e5b9b10c234e61db">preserve-first 初始化应该怎样反映在 Naju 的两个 sigmoid 门上？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Anaju">Naju: A Native Discrete State-Space Model with Independent Retention and Writing for Long-Sequence Memory</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Independent researchers</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档给出forget_bias=5、write_bias=-2，使初始保留接近1、写入较小；它不是把两个门设为同一个值。还需保留token相关B/C与直接feedthrough，才能对应记录的完整本地路径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>sigmoid(5)约0.993、sigmoid(-2)约0.119，分别表达强保留与弱初始写入。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21000">原论文</a> · <a href="../../../../reproductions/2607.21000-naju/">实现解读</a> · <a href="#qa-e5b9b10c234e61db">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:conv-llm" data-paper-title="Convolution for Large Language Models" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Convolution for Large Language Models 基础模型 Huawei / Peking University / Tsinghua University 2026-07-20 自注意力擅长全局依赖，却没有显式的短程归纳偏置。论文固定 Qwen3 主干，系统比较 17 个卷积插入位置，最终选择在 Q/K/V 线性投影后、attention 聚合前加入 kernel=3 的逐通道一维卷积；残差旁路保留原投影，不加归一化或激活，额外参数低于 0.01%。 未运行 Qwen3-0.6B/1.7B/4B、论文大规模预训练语料和七项下游任务；Fidelity: 核心机制复现。真实预训练同预算 Transformer 与 post-QKV residual depthwise Conv1D；缩小模型和语料规模。未运行 Qwen3-0.6B/1.7B/4B、论文大规模预训练语料和七项下游任务；本地结论只支持小模型短预算下的方向性收益。本地对照口径：基线是相同 96-d、3-layer、60-step Transformer；实验组仅增加 QKV 后残差 depthwise Conv1D，test perplexity 相对降低 0.29%。  llm-architecture attention depthwise-convolution 基础模型 长上下文：注意力、递归状态与记忆 Conv-LLM 试图补足 attention 的哪类信息偏好？ 全局attention能按内容访问远处位置，却不天然强调相邻词的局部组合。论文用轻量短卷积先增强Q/K/V附近的顺序模式，再保留attention做全局交互。 示意：“不太好”中的相邻否定关系可先被局部聚合，再参与对整段上下文的读取。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-conv-llm-13d560f4" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0cd712f5033c9b5c">Conv-LLM 试图补足 attention 的哪类信息偏好？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aconv-llm">Convolution for Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei / Peking University / Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全局attention能按内容访问远处位置，却不天然强调相邻词的局部组合。论文用轻量短卷积先增强Q/K/V附近的顺序模式，再保留attention做全局交互。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>“不太好”中的相邻否定关系可先被局部聚合，再参与对整段上下文的读取。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.18413">原论文</a> · <a href="../../../../reproductions/2607.18413-conv-llm/">实现解读</a> · <a href="#qa-0cd712f5033c9b5c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:conv-llm" data-paper-title="Convolution for Large Language Models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Convolution for Large Language Models 基础模型 Huawei / Peking University / Tsinghua University 2026-07-20 自注意力擅长全局依赖，却没有显式的短程归纳偏置。论文固定 Qwen3 主干，系统比较 17 个卷积插入位置，最终选择在 Q/K/V 线性投影后、attention 聚合前加入 kernel=3 的逐通道一维卷积；残差旁路保留原投影，不加归一化或激活，额外参数低于 0.01%。 未运行 Qwen3-0.6B/1.7B/4B、论文大规模预训练语料和七项下游任务；Fidelity: 核心机制复现。真实预训练同预算 Transformer 与 post-QKV residual depthwise Conv1D；缩小模型和语料规模。未运行 Qwen3-0.6B/1.7B/4B、论文大规模预训练语料和七项下游任务；本地结论只支持小模型短预算下的方向性收益。本地对照口径：基线是相同 96-d、3-layer、60-step Transformer；实验组仅增加 QKV 后残差 depthwise Conv1D，test perplexity 相对降低 0.29%。  llm-architecture attention depthwise-convolution 基础模型 长上下文：注意力、递归状态与记忆 Conv-LLM已经有attention，为什么还在Q/K/V投影后加三点卷积？ attention按内容在历史中选择位置，短卷积先给每个位置注入附近顺序模式。这里卷积作用于投影后的Q/K/V，并通过残差保留原值，再进入attention；它不是把整个全局交互替换为卷积。逐通道卷积控制额外参数，因果左填充避免提前读到后面的词。 教学例子：读取“不是很好”时，局部卷积可先把否定词与相邻词结合，再让增强后的查询去匹配远处上下文；卷积不能读取尚未出现的“好”。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-ca1d3cdc7932365e">Conv-LLM已经有attention，为什么还在Q/K/V投影后加三点卷积？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aconv-llm">Convolution for Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei / Peking University / Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>attention按内容在历史中选择位置，短卷积先给每个位置注入附近顺序模式。这里卷积作用于投影后的Q/K/V，并通过残差保留原值，再进入attention；它不是把整个全局交互替换为卷积。逐通道卷积控制额外参数，因果左填充避免提前读到后面的词。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>读取“不是很好”时，局部卷积可先把否定词与相邻词结合，再让增强后的查询去匹配远处上下文；卷积不能读取尚未出现的“好”。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.18413">原论文</a> · <a href="../../../../reproductions/2607.18413-conv-llm/">实现解读</a> · <a href="#qa-ca1d3cdc7932365e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:conv-llm" data-paper-title="Convolution for Large Language Models" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Convolution for Large Language Models 基础模型 Huawei / Peking University / Tsinghua University 2026-07-20 自注意力擅长全局依赖，却没有显式的短程归纳偏置。论文固定 Qwen3 主干，系统比较 17 个卷积插入位置，最终选择在 Q/K/V 线性投影后、attention 聚合前加入 kernel=3 的逐通道一维卷积；残差旁路保留原投影，不加归一化或激活，额外参数低于 0.01%。 未运行 Qwen3-0.6B/1.7B/4B、论文大规模预训练语料和七项下游任务；Fidelity: 核心机制复现。真实预训练同预算 Transformer 与 post-QKV residual depthwise Conv1D；缩小模型和语料规模。未运行 Qwen3-0.6B/1.7B/4B、论文大规模预训练语料和七项下游任务；本地结论只支持小模型短预算下的方向性收益。本地对照口径：基线是相同 96-d、3-layer、60-step Transformer；实验组仅增加 QKV 后残差 depthwise Conv1D，test perplexity 相对降低 0.29%。  llm-architecture attention depthwise-convolution 基础模型 长上下文：注意力、递归状态与记忆 QKV 后的逐通道短卷积，与直接把 attention 换成卷积有什么区别？ 前者只增强投影表示，保留原attention的全局匹配与聚合；后者会改变主要交互路径。逐通道卷积也不在不同通道间做完整混合，额外参数因此较小，但长程访问仍由attention负责。 示意：卷积先组合邻近三个位置，当前词之后仍能通过attention读取几百词前的名字。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-30e7fcb1185be4fa">QKV 后的逐通道短卷积，与直接把 attention 换成卷积有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aconv-llm">Convolution for Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei / Peking University / Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者只增强投影表示，保留原attention的全局匹配与聚合；后者会改变主要交互路径。逐通道卷积也不在不同通道间做完整混合，额外参数因此较小，但长程访问仍由attention负责。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>卷积先组合邻近三个位置，当前词之后仍能通过attention读取几百词前的名字。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.18413">原论文</a> · <a href="../../../../reproductions/2607.18413-conv-llm/">实现解读</a> · <a href="#qa-30e7fcb1185be4fa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:conv-llm" data-paper-title="Convolution for Large Language Models" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Convolution for Large Language Models 基础模型 Huawei / Peking University / Tsinghua University 2026-07-20 自注意力擅长全局依赖，却没有显式的短程归纳偏置。论文固定 Qwen3 主干，系统比较 17 个卷积插入位置，最终选择在 Q/K/V 线性投影后、attention 聚合前加入 kernel=3 的逐通道一维卷积；残差旁路保留原投影，不加归一化或激活，额外参数低于 0.01%。 未运行 Qwen3-0.6B/1.7B/4B、论文大规模预训练语料和七项下游任务；Fidelity: 核心机制复现。真实预训练同预算 Transformer 与 post-QKV residual depthwise Conv1D；缩小模型和语料规模。未运行 Qwen3-0.6B/1.7B/4B、论文大规模预训练语料和七项下游任务；本地结论只支持小模型短预算下的方向性收益。本地对照口径：基线是相同 96-d、3-layer、60-step Transformer；实验组仅增加 QKV 后残差 depthwise Conv1D，test perplexity 相对降低 0.29%。  llm-architecture attention depthwise-convolution 基础模型 长上下文：注意力、递归状态与记忆 QKV 残差卷积的 padding、激活和旁路该怎样对应文档？ 本地实现使用左侧padding，避免卷积读取未来；卷积结果加回原QKV投影，再进入attention。文档指定该旁路不另加归一化或激活，随手增加层会改变被比较的配置。 示意：核宽3时，第t位只能组合t、t-1、t-2，不能为了保持长度而使用对称未来填充。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-779d00242b977804">QKV 残差卷积的 padding、激活和旁路该怎样对应文档？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aconv-llm">Convolution for Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei / Peking University / Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>本地实现使用左侧padding，避免卷积读取未来；卷积结果加回原QKV投影，再进入attention。文档指定该旁路不另加归一化或激活，随手增加层会改变被比较的配置。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>核宽3时，第t位只能组合t、t-1、t-2，不能为了保持长度而使用对称未来填充。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.18413">原论文</a> · <a href="../../../../reproductions/2607.18413-conv-llm/">实现解读</a> · <a href="#qa-779d00242b977804">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:minimax-sparse-attention" data-paper-title="MiniMax Sparse Attention" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="MiniMax Sparse Attention 基础模型 MiniMax 2026-06-11 长上下文 dense attention 的二次复杂度成为主要瓶颈。MSA 为每个 GQA 组增加轻量 index branch，先选择少数历史 block，主分支再对命中 token 做精确 attention；训练和推理使用同一路径。 复现保真度：核心机制复现。复现保真度：核心机制复现。Index branch、每 GQA 组 top-k block 和精确 sparse attention 均真实训练；109B 预训练与 fused kernel 未复刻。WikiText-2 上训练同初始化/同预算的 tiny dense GQA 与 blockwise MSA，报告 PPL、训练时间和实际 attention pair ratio。  llm sparse-attention gqa long-context 基础模型 长上下文：注意力、递归状态与记忆 MSA 中的历史 block 是新的模型层，还是沿 token 轴组织的候选单元？ block用于把历史token组织成索引候选，轻量分支先选block，主分支再读取其中token；它不是额外Transformer层。理解两个粒度才能区分块选择成本与精确attention成本。 示意：先在目录选章节，再精读该章句子，章节与句子是不同读取粒度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-minimax-sparse-attention-fdb70645" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7404b15170e7203f">MSA 中的历史 block 是新的模型层，还是沿 token 轴组织的候选单元？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aminimax-sparse-attention">MiniMax Sparse Attention</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · MiniMax</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>block用于把历史token组织成索引候选，轻量分支先选block，主分支再读取其中token；它不是额外Transformer层。理解两个粒度才能区分块选择成本与精确attention成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先在目录选章节，再精读该章句子，章节与句子是不同读取粒度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.13392">原论文</a> · <a href="../../../../reproductions/2606.13392-minimax-sparse-attention/">实现解读</a> · <a href="#qa-7404b15170e7203f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:minimax-sparse-attention" data-paper-title="MiniMax Sparse Attention" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="MiniMax Sparse Attention 基础模型 MiniMax 2026-06-11 长上下文 dense attention 的二次复杂度成为主要瓶颈。MSA 为每个 GQA 组增加轻量 index branch，先选择少数历史 block，主分支再对命中 token 做精确 attention；训练和推理使用同一路径。 复现保真度：核心机制复现。复现保真度：核心机制复现。Index branch、每 GQA 组 top-k block 和精确 sparse attention 均真实训练；109B 预训练与 fused kernel 未复刻。WikiText-2 上训练同初始化/同预算的 tiny dense GQA 与 blockwise MSA，报告 PPL、训练时间和实际 attention pair ratio。  llm sparse-attention gqa long-context 基础模型 长上下文：注意力、递归状态与记忆 MSA先选block再做精确attention，省掉的是哪一步，保留的又是什么？ 轻量索引分支先用较便宜的块级匹配缩小历史范围，主注意力仅对命中块内的token计算精确权重。因此不是把所有token都换成一个块均值；块摘要用于筛选，细粒度交互仍在被选区域发生。若索引漏掉答案所在块，后续精确attention也无法弥补。 教学例子：十页文档先选两页，再逐字寻找日期。省下的是其他八页的主注意力计算；若索引先删掉唯一包含日期的一页，细读剩余页面也找不到答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-be7681bf09e68302">MSA先选block再做精确attention，省掉的是哪一步，保留的又是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aminimax-sparse-attention">MiniMax Sparse Attention</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · MiniMax</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>轻量索引分支先用较便宜的块级匹配缩小历史范围，主注意力仅对命中块内的token计算精确权重。因此不是把所有token都换成一个块均值；块摘要用于筛选，细粒度交互仍在被选区域发生。若索引漏掉答案所在块，后续精确attention也无法弥补。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>十页文档先选两页，再逐字寻找日期。省下的是其他八页的主注意力计算；若索引先删掉唯一包含日期的一页，细读剩余页面也找不到答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.13392">原论文</a> · <a href="../../../../reproductions/2606.13392-minimax-sparse-attention/">实现解读</a> · <a href="#qa-be7681bf09e68302">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:minimax-sparse-attention" data-paper-title="MiniMax Sparse Attention" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="MiniMax Sparse Attention 基础模型 MiniMax 2026-06-11 长上下文 dense attention 的二次复杂度成为主要瓶颈。MSA 为每个 GQA 组增加轻量 index branch，先选择少数历史 block，主分支再对命中 token 做精确 attention；训练和推理使用同一路径。 复现保真度：核心机制复现。复现保真度：核心机制复现。Index branch、每 GQA 组 top-k block 和精确 sparse attention 均真实训练；109B 预训练与 fused kernel 未复刻。WikiText-2 上训练同初始化/同预算的 tiny dense GQA 与 blockwise MSA，报告 PPL、训练时间和实际 attention pair ratio。  llm sparse-attention gqa long-context 基础模型 长上下文：注意力、递归状态与记忆 MSA 的索引分支与直接缩小主 attention 的 KV，承担的是同一种任务吗？ 索引分支负责决定哪些历史块值得读取，主分支仍以自身Q/K/V进行精确attention。直接压缩KV会改变被聚合的内容表示；预选与内容压缩是不同的近似位置。 示意：选择原文的两段来读，和把全文先压成两段摘要再读，保留的证据可能不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b463a148aea8bf76">MSA 的索引分支与直接缩小主 attention 的 KV，承担的是同一种任务吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aminimax-sparse-attention">MiniMax Sparse Attention</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · MiniMax</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>索引分支负责决定哪些历史块值得读取，主分支仍以自身Q/K/V进行精确attention。直接压缩KV会改变被聚合的内容表示；预选与内容压缩是不同的近似位置。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>选择原文的两段来读，和把全文先压成两段摘要再读，保留的证据可能不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.13392">原论文</a> · <a href="../../../../reproductions/2606.13392-minimax-sparse-attention/">实现解读</a> · <a href="#qa-b463a148aea8bf76">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:minimax-sparse-attention" data-paper-title="MiniMax Sparse Attention" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="MiniMax Sparse Attention 基础模型 MiniMax 2026-06-11 长上下文 dense attention 的二次复杂度成为主要瓶颈。MSA 为每个 GQA 组增加轻量 index branch，先选择少数历史 block，主分支再对命中 token 做精确 attention；训练和推理使用同一路径。 复现保真度：核心机制复现。复现保真度：核心机制复现。Index branch、每 GQA 组 top-k block 和精确 sparse attention 均真实训练；109B 预训练与 fused kernel 未复刻。WikiText-2 上训练同初始化/同预算的 tiny dense GQA 与 blockwise MSA，报告 PPL、训练时间和实际 attention pair ratio。  llm sparse-attention gqa long-context 基础模型 长上下文：注意力、递归状态与记忆 MSA 的 attention pair ratio 降低，为什么不能直接报告同幅度的加速？ 实际时间还包括索引、块选择、数据搬运以及所用kernel。文档中的未融合PyTorch/MPS路径虽然减少pair，耗时却更高；应分别报告pair比例、PPL与实测时间。 示意：理论上少读八成配对，但额外索引和执行方式可能让一次训练反而更慢。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0ce248cccdc3b3a1">MSA 的 attention pair ratio 降低，为什么不能直接报告同幅度的加速？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aminimax-sparse-attention">MiniMax Sparse Attention</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · MiniMax</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>实际时间还包括索引、块选择、数据搬运以及所用kernel。文档中的未融合PyTorch/MPS路径虽然减少pair，耗时却更高；应分别报告pair比例、PPL与实测时间。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>理论上少读八成配对，但额外索引和执行方式可能让一次训练反而更慢。</p>
<p class="ar-learning-sources">依据：本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.13392">原论文</a> · <a href="../../../../reproductions/2606.13392-minimax-sparse-attention/">实现解读</a> · <a href="#qa-0ce248cccdc3b3a1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:sleep-lti" data-paper-title="Language Models Need Sleep: Learning to Self-Modify and Consolidate Memories" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Language Models Need Sleep: Learning to Self-Modify and Consolidate Memories 基础模型 Google Research 2026-06-02 上下文结束会丢失短期知识，直接更新基础权重又可能覆盖旧知识。Sleep在活跃学习之外增加离线巩固：多频率记忆模块间先计算未来基础更新但不应用，再扩展低秩专家、用更新前教师巩固到拟更新学生，最后应用更新并清理发送层专家。知识播种结合教师数据和学生自生成前缀上的蒸馏；LTI再让学生补全教师梦境，以冻结语义评审和阈值化token编辑相似度提供奖励。本地只实现后一个奖励公式，不能因为奖励可计算，就声称自修改、抗遗忘或知识巩固已完成。 完整Sleep实验成本过高，不复现（审查 DONE）；本地仅实现 LTI奖励的纯CPU L1组件，没有CMS、扩容、梦境生成、语义评审模型或LLM训练。完整Sleep实验成本过高，不复现（审查 DONE）；不接入Evolve。用已分词整数序列检查插入、删除、替换、阈值包含等号、按最大长度归一，以及语义分支独立性。42/43/44是合成机制种子，不是LLM模型比较。语义标签只在奖励侧输入，不参与被评测Agent的行动生成。  持续学习 离线记忆巩固 知识播种 基础模型 长上下文：注意力、递归状态与记忆 Sleep中的睡眠只是暂停训练，还是另一套学习阶段？ 是离线巩固阶段。方法在应用预计算基础更新前扩展慢模块，用更新前教师把快记忆巩固到拟更新学生，然后应用更新并清理发送层专家。它不是简单暂停或重放几条样本，本地也没有实现这一完整链路。 教学例：临时笔记要整理进长期知识库，先核对整理后的内容再清空临时笔记；只计算笔记相似度并不等于完成整理。 2026-10-29">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-sleep-lti-911eb3e3" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d2752590c7dbcbcf">Sleep中的睡眠只是暂停训练，还是另一套学习阶段？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asleep-lti">Language Models Need Sleep: Learning to Self-Modify and Consolidate Memories</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-29 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>是离线巩固阶段。方法在应用预计算基础更新前扩展慢模块，用更新前教师把快记忆巩固到拟更新学生，然后应用更新并清理发送层专家。它不是简单暂停或重放几条样本，本地也没有实现这一完整链路。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：临时笔记要整理进长期知识库，先核对整理后的内容再清空临时笔记；只计算笔记相似度并不等于完成整理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.03979v2">原论文</a> · <a href="../../../../foundation-models/2606.03979-sleep-lti/">实现解读</a> · <a href="#qa-d2752590c7dbcbcf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:sleep-lti" data-paper-title="Language Models Need Sleep: Learning to Self-Modify and Consolidate Memories" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Language Models Need Sleep: Learning to Self-Modify and Consolidate Memories 基础模型 Google Research 2026-06-02 上下文结束会丢失短期知识，直接更新基础权重又可能覆盖旧知识。Sleep在活跃学习之外增加离线巩固：多频率记忆模块间先计算未来基础更新但不应用，再扩展低秩专家、用更新前教师巩固到拟更新学生，最后应用更新并清理发送层专家。知识播种结合教师数据和学生自生成前缀上的蒸馏；LTI再让学生补全教师梦境，以冻结语义评审和阈值化token编辑相似度提供奖励。本地只实现后一个奖励公式，不能因为奖励可计算，就声称自修改、抗遗忘或知识巩固已完成。 完整Sleep实验成本过高，不复现（审查 DONE）；本地仅实现 LTI奖励的纯CPU L1组件，没有CMS、扩容、梦境生成、语义评审模型或LLM训练。完整Sleep实验成本过高，不复现（审查 DONE）；不接入Evolve。用已分词整数序列检查插入、删除、替换、阈值包含等号、按最大长度归一，以及语义分支独立性。42/43/44是合成机制种子，不是LLM模型比较。语义标签只在奖励侧输入，不参与被评测Agent的行动生成。  持续学习 离线记忆巩固 知识播种 基础模型 长上下文：注意力、递归状态与记忆 LTI的编辑距离门槛限制的是编辑次数还是相似度比例？ 门槛限制绝对token编辑次数；通过门槛后，字面奖励才用一减距离除以两段续写最大长度。阈值包含等号，不能把它换成固定相似度比例。 教学例：阈值为1时，一次替换无论发生在6token还是60token续写都通过，但归一化奖励分别为5/6和59/60。 2026-10-29">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-357fc7df50a38180">LTI的编辑距离门槛限制的是编辑次数还是相似度比例？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asleep-lti">Language Models Need Sleep: Learning to Self-Modify and Consolidate Memories</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-29 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>门槛限制绝对token编辑次数；通过门槛后，字面奖励才用一减距离除以两段续写最大长度。阈值包含等号，不能把它换成固定相似度比例。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：阈值为1时，一次替换无论发生在6token还是60token续写都通过，但归一化奖励分别为5/6和59/60。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.03979v2">原论文</a> · <a href="../../../../foundation-models/2606.03979-sleep-lti/">实现解读</a> · <a href="#qa-357fc7df50a38180">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:sleep-lti" data-paper-title="Language Models Need Sleep: Learning to Self-Modify and Consolidate Memories" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Language Models Need Sleep: Learning to Self-Modify and Consolidate Memories 基础模型 Google Research 2026-06-02 上下文结束会丢失短期知识，直接更新基础权重又可能覆盖旧知识。Sleep在活跃学习之外增加离线巩固：多频率记忆模块间先计算未来基础更新但不应用，再扩展低秩专家、用更新前教师巩固到拟更新学生，最后应用更新并清理发送层专家。知识播种结合教师数据和学生自生成前缀上的蒸馏；LTI再让学生补全教师梦境，以冻结语义评审和阈值化token编辑相似度提供奖励。本地只实现后一个奖励公式，不能因为奖励可计算，就声称自修改、抗遗忘或知识巩固已完成。 完整Sleep实验成本过高，不复现（审查 DONE）；本地仅实现 LTI奖励的纯CPU L1组件，没有CMS、扩容、梦境生成、语义评审模型或LLM训练。完整Sleep实验成本过高，不复现（审查 DONE）；不接入Evolve。用已分词整数序列检查插入、删除、替换、阈值包含等号、按最大长度归一，以及语义分支独立性。42/43/44是合成机制种子，不是LLM模型比较。语义标签只在奖励侧输入，不参与被评测Agent的行动生成。  持续学习 离线记忆巩固 知识播种 基础模型 长上下文：注意力、递归状态与记忆 字面距离超阈值，是否意味着语义奖励也要清零？ 不是。语义0/1由外部冻结评审独立给出，阈值只作用于字面分支。词面差很多也可能语义相同；仅用编辑距离替代语义模型会改变算法。 教学例：gamma为0.4、语义评审判同义，字面分支为零时总奖励仍为0.4，而不是零。 2026-10-29">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7ed013edbf092629">字面距离超阈值，是否意味着语义奖励也要清零？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asleep-lti">Language Models Need Sleep: Learning to Self-Modify and Consolidate Memories</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-29 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。语义0/1由外部冻结评审独立给出，阈值只作用于字面分支。词面差很多也可能语义相同；仅用编辑距离替代语义模型会改变算法。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：gamma为0.4、语义评审判同义，字面分支为零时总奖励仍为0.4，而不是零。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.03979v2">原论文</a> · <a href="../../../../foundation-models/2606.03979-sleep-lti/">实现解读</a> · <a href="#qa-7ed013edbf092629">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:sleep-lti" data-paper-title="Language Models Need Sleep: Learning to Self-Modify and Consolidate Memories" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Language Models Need Sleep: Learning to Self-Modify and Consolidate Memories 基础模型 Google Research 2026-06-02 上下文结束会丢失短期知识，直接更新基础权重又可能覆盖旧知识。Sleep在活跃学习之外增加离线巩固：多频率记忆模块间先计算未来基础更新但不应用，再扩展低秩专家、用更新前教师巩固到拟更新学生，最后应用更新并清理发送层专家。知识播种结合教师数据和学生自生成前缀上的蒸馏；LTI再让学生补全教师梦境，以冻结语义评审和阈值化token编辑相似度提供奖励。本地只实现后一个奖励公式，不能因为奖励可计算，就声称自修改、抗遗忘或知识巩固已完成。 完整Sleep实验成本过高，不复现（审查 DONE）；本地仅实现 LTI奖励的纯CPU L1组件，没有CMS、扩容、梦境生成、语义评审模型或LLM训练。完整Sleep实验成本过高，不复现（审查 DONE）；不接入Evolve。用已分词整数序列检查插入、删除、替换、阈值包含等号、按最大长度归一，以及语义分支独立性。42/43/44是合成机制种子，不是LLM模型比较。语义标签只在奖励侧输入，不参与被评测Agent的行动生成。  持续学习 离线记忆巩固 知识播种 基础模型 长上下文：注意力、递归状态与记忆 本地Sleep奖励组件能证明模型已学会长期保留知识吗？ 不能。它只接收已分词续写与外部语义标签，验证奖励数值边界；没有梦境采样、CMS、参数扩展、LoRA训练、筛选或遗忘评测。完整高成本实验已明确不复现，不把奖励核注册为Evolve能力算子。 教学例：两段整数token得到0.9奖励，只说明该输入满足奖励公式，不说明任何语言模型权重发生了变化。 2026-10-29">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-da8dd16e738119ab">本地Sleep奖励组件能证明模型已学会长期保留知识吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asleep-lti">Language Models Need Sleep: Learning to Self-Modify and Consolidate Memories</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-29 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。它只接收已分词续写与外部语义标签，验证奖励数值边界；没有梦境采样、CMS、参数扩展、LoRA训练、筛选或遗忘评测。完整高成本实验已明确不复现，不把奖励核注册为Evolve能力算子。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：两段整数token得到0.9奖励，只说明该输入满足奖励公式，不说明任何语言模型权重发生了变化。</p>
<p class="ar-learning-sources">依据：本地复现与边界、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.03979v2">原论文</a> · <a href="../../../../foundation-models/2606.03979-sleep-lti/">实现解读</a> · <a href="#qa-da8dd16e738119ab">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:switch-attention" data-paper-title="Switch Attention: Towards Dynamic and Fine-grained Hybrid Transformers" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Switch Attention: Towards Dynamic and Fine-grained Hybrid Transformers 基础模型 Peking University / Huawei Technologies 2026-03-27 静态 hybrid attention 对所有 token 使用固定模式。Switch Attention 学习细粒度 router，只让需要全局信息的 token 走 full attention。 Fidelity: 核心机制复现。实现逐 token 动态选择 full/local attention 的可学习 router。本地使用可微 soft router，未复刻论文 STE 硬路由、32K continual pretraining 和 branch-selective fused kernel。本地对照口径：基线是 full-attention tiny Transformer；实验组动态混合 full 与 16-token local attention；30-step perplexity 相对 +0.19%（近似持平但略差）。  llm-architecture efficient-attention long-context 基础模型 长上下文：注意力、递归状态与记忆 Switch Attention 的 local 与 full 两条路径，分别能读到哪些历史？ local只看限定窗口内的可见位置，full可读完整因果历史。二者首先是证据范围与读取成本的差别；router根据token决定路径，不是让full路径访问未来token。 示意：回答刚出现的局部词组可能只需近邻，关联很久以前的信息才可能需要更广历史。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-switch-attention-753b5e50" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-3235ac51ae30aba8">Switch Attention 的 local 与 full 两条路径，分别能读到哪些历史？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aswitch-attention">Switch Attention: Towards Dynamic and Fine-grained Hybrid Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University / Huawei Technologies</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>local只看限定窗口内的可见位置，full可读完整因果历史。二者首先是证据范围与读取成本的差别；router根据token决定路径，不是让full路径访问未来token。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>回答刚出现的局部词组可能只需近邻，关联很久以前的信息才可能需要更广历史。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.26380">原论文</a> · <a href="../../../../reproductions/2603.26380-switch-attention/">实现解读</a> · <a href="#qa-3235ac51ae30aba8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:switch-attention" data-paper-title="Switch Attention: Towards Dynamic and Fine-grained Hybrid Transformers" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Switch Attention: Towards Dynamic and Fine-grained Hybrid Transformers 基础模型 Peking University / Huawei Technologies 2026-03-27 静态 hybrid attention 对所有 token 使用固定模式。Switch Attention 学习细粒度 router，只让需要全局信息的 token 走 full attention。 Fidelity: 核心机制复现。实现逐 token 动态选择 full/local attention 的可学习 router。本地使用可微 soft router，未复刻论文 STE 硬路由、32K continual pretraining 和 branch-selective fused kernel。本地对照口径：基线是 full-attention tiny Transformer；实验组动态混合 full 与 16-token local attention；30-step perplexity 相对 +0.19%（近似持平但略差）。  llm-architecture efficient-attention long-context 基础模型 长上下文：注意力、递归状态与记忆 Switch Attention是给每层固定一种模式，还是逐token决定是否需要全局attention？ 它用细粒度router决定当前token走全局还是局部注意力，因此同一层里不同位置可以使用不同读取范围。训练需处理这种选择的离散性，不能把硬路由当作普通可微操作。计算收益取决于实际全局调用比例和实现开销，选择更稀疏本身不保证质量保持。 教学例子：一句话中多数连接词只需局部上下文，引用开头人名的位置则可能需要全局检索；固定整层都走全局，会把两类位置支付的成本混在一起。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-145fabe3734e92b3">Switch Attention是给每层固定一种模式，还是逐token决定是否需要全局attention？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aswitch-attention">Switch Attention: Towards Dynamic and Fine-grained Hybrid Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University / Huawei Technologies</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它用细粒度router决定当前token走全局还是局部注意力，因此同一层里不同位置可以使用不同读取范围。训练需处理这种选择的离散性，不能把硬路由当作普通可微操作。计算收益取决于实际全局调用比例和实现开销，选择更稀疏本身不保证质量保持。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一句话中多数连接词只需局部上下文，引用开头人名的位置则可能需要全局检索；固定整层都走全局，会把两类位置支付的成本混在一起。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.26380">原论文</a> · <a href="../../../../reproductions/2603.26380-switch-attention/">实现解读</a> · <a href="#qa-145fabe3734e92b3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:switch-attention" data-paper-title="Switch Attention: Towards Dynamic and Fine-grained Hybrid Transformers" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Switch Attention: Towards Dynamic and Fine-grained Hybrid Transformers 基础模型 Peking University / Huawei Technologies 2026-03-27 静态 hybrid attention 对所有 token 使用固定模式。Switch Attention 学习细粒度 router，只让需要全局信息的 token 走 full attention。 Fidelity: 核心机制复现。实现逐 token 动态选择 full/local attention 的可学习 router。本地使用可微 soft router，未复刻论文 STE 硬路由、32K continual pretraining 和 branch-selective fused kernel。本地对照口径：基线是 full-attention tiny Transformer；实验组动态混合 full 与 16-token local attention；30-step perplexity 相对 +0.19%（近似持平但略差）。  llm-architecture efficient-attention long-context 基础模型 长上下文：注意力、递归状态与记忆 动态切换 full/local，与对两条分支始终做连续加权有什么区别？ 硬切换可选择实际执行分支，连续加权通常仍需两条输出再混合。两者在梯度近似与计算节省上不同；文档明确本地soft router尚未复刻论文STE硬路由。 示意：计算两次attention再各乘权重，并不因某权重接近0就自动省掉对应计算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-31c3a79c4cb08720">动态切换 full/local，与对两条分支始终做连续加权有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aswitch-attention">Switch Attention: Towards Dynamic and Fine-grained Hybrid Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University / Huawei Technologies</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>硬切换可选择实际执行分支，连续加权通常仍需两条输出再混合。两者在梯度近似与计算节省上不同；文档明确本地soft router尚未复刻论文STE硬路由。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>计算两次attention再各乘权重，并不因某权重接近0就自动省掉对应计算。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.26380">原论文</a> · <a href="../../../../reproductions/2603.26380-switch-attention/">实现解读</a> · <a href="#qa-31c3a79c4cb08720">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:switch-attention" data-paper-title="Switch Attention: Towards Dynamic and Fine-grained Hybrid Transformers" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Switch Attention: Towards Dynamic and Fine-grained Hybrid Transformers 基础模型 Peking University / Huawei Technologies 2026-03-27 静态 hybrid attention 对所有 token 使用固定模式。Switch Attention 学习细粒度 router，只让需要全局信息的 token 走 full attention。 Fidelity: 核心机制复现。实现逐 token 动态选择 full/local attention 的可学习 router。本地使用可微 soft router，未复刻论文 STE 硬路由、32K continual pretraining 和 branch-selective fused kernel。本地对照口径：基线是 full-attention tiny Transformer；实验组动态混合 full 与 16-token local attention；30-step perplexity 相对 +0.19%（近似持平但略差）。  llm-architecture efficient-attention long-context 基础模型 长上下文：注意力、递归状态与记忆 本地 Switch Attention 的 soft router 能用来证明 branch-selective kernel 加速吗？ 不能。当前实现验证连续混合路径，未提供论文硬路由、32K继续预训练或分支选择fused kernel。核对时要分别检查路由选择、执行分支及实际耗时，不能只看门值。 示意：日志显示90%权重给local，也不证明90%的global调用被跳过。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1652841be38828b4">本地 Switch Attention 的 soft router 能用来证明 branch-selective kernel 加速吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aswitch-attention">Switch Attention: Towards Dynamic and Fine-grained Hybrid Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University / Huawei Technologies</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。当前实现验证连续混合路径，未提供论文硬路由、32K继续预训练或分支选择fused kernel。核对时要分别检查路由选择、执行分支及实际耗时，不能只看门值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>日志显示90%权重给local，也不证明90%的global调用被跳过。</p>
<p class="ar-learning-sources">依据：复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.26380">原论文</a> · <a href="../../../../reproductions/2603.26380-switch-attention/">实现解读</a> · <a href="#qa-1652841be38828b4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gated-attention" data-paper-title="Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free 基础模型 Qwen / Alibaba 2025-05-10 softmax attention 的 value aggregation 到 output projection 之间基本是线性映射。论文系统比较 30 种门控变体，发现最简单稳定的方案是在每个 attention head 的 SDPA 输出后施加 query-dependent sigmoid gate：既增加非线性，也能稀疏抑制无用 head 输出。 未执行 3.5T-token、1.7B/15B scaling、完整学习率 sweep 与长上下文矩阵；Fidelity: 核心机制复现。真实训练论文最优的 head-specific sigmoid gate，并记录门控分布。未执行 3.5T-token、1.7B/15B scaling、完整学习率 sweep 与长上下文矩阵；本地只验证论文最优门控位置的实际训练路径。本地对照口径：基线是同预算 llama_modern；实验组只增加 post-SDPA 逐头 sigmoid gate，WikiText-2 LM loss 5.7471→5.7398，相对 -0.13%，PPL 相对 -0.72%。  llm-architecture attention-gating long-context 基础模型 长上下文：注意力、递归状态与记忆 Gated Attention 的门在决定“读哪里”，还是“读出多少”？ 这里的门作用于每头SDPA已经聚合出的结果，由当前输入控制信息送出多少。历史位置的匹配仍先由attention完成，门再抑制或保留整条读出路径。 示意：一个头已读到格式符号，但当前问题不需要它，门可以减小该头输出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-gated-attention-0685e39f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ec17b654ab0c8a26">Gated Attention 的门在决定“读哪里”，还是“读出多少”？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agated-attention">Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Qwen / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这里的门作用于每头SDPA已经聚合出的结果，由当前输入控制信息送出多少。历史位置的匹配仍先由attention完成，门再抑制或保留整条读出路径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个头已读到格式符号，但当前问题不需要它，门可以减小该头输出。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.06708">原论文</a> · <a href="../../../../reproductions/2505.06708-gated-attention/">实现解读</a> · <a href="#qa-ec17b654ab0c8a26">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gated-attention" data-paper-title="Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free 基础模型 Qwen / Alibaba 2025-05-10 softmax attention 的 value aggregation 到 output projection 之间基本是线性映射。论文系统比较 30 种门控变体，发现最简单稳定的方案是在每个 attention head 的 SDPA 输出后施加 query-dependent sigmoid gate：既增加非线性，也能稀疏抑制无用 head 输出。 未执行 3.5T-token、1.7B/15B scaling、完整学习率 sweep 与长上下文矩阵；Fidelity: 核心机制复现。真实训练论文最优的 head-specific sigmoid gate，并记录门控分布。未执行 3.5T-token、1.7B/15B scaling、完整学习率 sweep 与长上下文矩阵；本地只验证论文最优门控位置的实际训练路径。本地对照口径：基线是同预算 llama_modern；实验组只增加 post-SDPA 逐头 sigmoid gate，WikiText-2 LM loss 5.7471→5.7398，相对 -0.13%，PPL 相对 -0.72%。  llm-architecture attention-gating long-context 基础模型 长上下文：注意力、递归状态与记忆 Gated Attention的门为何放在SDPA输出之后，而不是先改attention分数？ 先完成每个头的注意力聚合，再用由当前输入产生的sigmoid门调制聚合结果，最后进入输出投影。这样门控制的是“当前头已经读出的信息该送出多少”，并在原本较线性的聚合到投影之间引入非线性。它与改变某个历史位置的softmax权重是不同控制对象。 教学例子：一个头读出了格式标记，另一个头读出了答案证据；当前查询的门可以抑制前者的整段输出，而不是重新指定每个历史token的注意力概率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-6609c4e775bab9c1">Gated Attention的门为何放在SDPA输出之后，而不是先改attention分数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agated-attention">Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Qwen / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>先完成每个头的注意力聚合，再用由当前输入产生的sigmoid门调制聚合结果，最后进入输出投影。这样门控制的是“当前头已经读出的信息该送出多少”，并在原本较线性的聚合到投影之间引入非线性。它与改变某个历史位置的softmax权重是不同控制对象。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个头读出了格式标记，另一个头读出了答案证据；当前查询的门可以抑制前者的整段输出，而不是重新指定每个历史token的注意力概率。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.06708">原论文</a> · <a href="../../../../reproductions/2505.06708-gated-attention/">实现解读</a> · <a href="#qa-6609c4e775bab9c1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gated-attention" data-paper-title="Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free 基础模型 Qwen / Alibaba 2025-05-10 softmax attention 的 value aggregation 到 output projection 之间基本是线性映射。论文系统比较 30 种门控变体，发现最简单稳定的方案是在每个 attention head 的 SDPA 输出后施加 query-dependent sigmoid gate：既增加非线性，也能稀疏抑制无用 head 输出。 未执行 3.5T-token、1.7B/15B scaling、完整学习率 sweep 与长上下文矩阵；Fidelity: 核心机制复现。真实训练论文最优的 head-specific sigmoid gate，并记录门控分布。未执行 3.5T-token、1.7B/15B scaling、完整学习率 sweep 与长上下文矩阵；本地只验证论文最优门控位置的实际训练路径。本地对照口径：基线是同预算 llama_modern；实验组只增加 post-SDPA 逐头 sigmoid gate，WikiText-2 LM loss 5.7471→5.7398，相对 -0.13%，PPL 相对 -0.72%。  llm-architecture attention-gating long-context 基础模型 长上下文：注意力、递归状态与记忆 把 sigmoid 门放在 SDPA 前后，为什么不是同一件事？ 在score或value处门控，会改变参与聚合的权重或内容；post-SDPA门控调制的是聚合完成后的输出。文档把这一位置列为消融选出的关键配置，不能随意挪动却仍称为同一实现。 示意：先把两条证据合并再整体缩小，通常不同于先分别缩小其中一条再重新聚合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-85ed640a6af63395">把 sigmoid 门放在 SDPA 前后，为什么不是同一件事？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agated-attention">Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Qwen / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>在score或value处门控，会改变参与聚合的权重或内容；post-SDPA门控调制的是聚合完成后的输出。文档把这一位置列为消融选出的关键配置，不能随意挪动却仍称为同一实现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先把两条证据合并再整体缩小，通常不同于先分别缩小其中一条再重新聚合。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.06708">原论文</a> · <a href="../../../../reproductions/2505.06708-gated-attention/">实现解读</a> · <a href="#qa-85ed640a6af63395">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gated-attention" data-paper-title="Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free 基础模型 Qwen / Alibaba 2025-05-10 softmax attention 的 value aggregation 到 output projection 之间基本是线性映射。论文系统比较 30 种门控变体，发现最简单稳定的方案是在每个 attention head 的 SDPA 输出后施加 query-dependent sigmoid gate：既增加非线性，也能稀疏抑制无用 head 输出。 未执行 3.5T-token、1.7B/15B scaling、完整学习率 sweep 与长上下文矩阵；Fidelity: 核心机制复现。真实训练论文最优的 head-specific sigmoid gate，并记录门控分布。未执行 3.5T-token、1.7B/15B scaling、完整学习率 sweep 与长上下文矩阵；本地只验证论文最优门控位置的实际训练路径。本地对照口径：基线是同预算 llama_modern；实验组只增加 post-SDPA 逐头 sigmoid gate，WikiText-2 LM loss 5.7471→5.7398，相对 -0.13%，PPL 相对 -0.72%。  llm-architecture attention-gating long-context 基础模型 长上下文：注意力、递归状态与记忆 逐头 query-dependent gate 能直接复用一个固定常数吗？ 固定常数没有当前输入依赖，也失去按头选择性调制。应由当前hidden产生对应头的sigmoid门，在输出投影前乘到SDPA结果上；本地门值统计只能说明实际路径没有退化为恒等旁路。 示意：两个问题即使读同一篇文章，也可对同一个头给出不同gate，而非始终乘0.5。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-5e263c96ab746d7a">逐头 query-dependent gate 能直接复用一个固定常数吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agated-attention">Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Qwen / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定常数没有当前输入依赖，也失去按头选择性调制。应由当前hidden产生对应头的sigmoid门，在输出投影前乘到SDPA结果上；本地门值统计只能说明实际路径没有退化为恒等旁路。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个问题即使读同一篇文章，也可对同一个头给出不同gate，而非始终乘0.5。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.06708">原论文</a> · <a href="../../../../reproductions/2505.06708-gated-attention/">实现解读</a> · <a href="#qa-5e263c96ab746d7a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:moba" data-paper-title="MoBA: Mixture of Block Attention for Long-Context LLMs" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="MoBA: Mixture of Block Attention for Long-Context LLMs 基础模型 Moonshot AI 2025-02-18 把序列切成 block，以可微 router 为每个 query 选择少量相关块，同时保留当前因果块。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际将历史划分为 8-token blocks，以 query 对 block key centroid 的相似度选择 top-2 causal blocks，再在命中块内执行精确 attention；PyTorch reference 未复刻百万上下文 fused kernel。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 moba；相对 PPL +0.49%。  sparse-attention long-context block-routing 基础模型 长上下文：注意力、递归状态与记忆 MoBA 为什么把历史划成 block，而不是给每个 query 都读完整历史？ 它把块作为路由单元，先为query挑少量相关历史，再在命中的块内做精确attention。这样减少候选配对范围，同时保留块内的细粒度读取。 示意：当前问题只需要两段相关材料时，不必对整篇每一个词都建立attention配对。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-moba-f8997c1b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-90411b0ae7184500">MoBA 为什么把历史划成 block，而不是给每个 query 都读完整历史？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amoba">MoBA: Mixture of Block Attention for Long-Context LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Moonshot AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它把块作为路由单元，先为query挑少量相关历史，再在命中的块内做精确attention。这样减少候选配对范围，同时保留块内的细粒度读取。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>当前问题只需要两段相关材料时，不必对整篇每一个词都建立attention配对。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.13189">原论文</a> · <a href="../../../../reproductions/2502.13189-moba/">实现解读</a> · <a href="#qa-90411b0ae7184500">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:moba" data-paper-title="MoBA: Mixture of Block Attention for Long-Context LLMs" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="MoBA: Mixture of Block Attention for Long-Context LLMs 基础模型 Moonshot AI 2025-02-18 把序列切成 block，以可微 router 为每个 query 选择少量相关块，同时保留当前因果块。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际将历史划分为 8-token blocks，以 query 对 block key centroid 的相似度选择 top-2 causal blocks，再在命中块内执行精确 attention；PyTorch reference 未复刻百万上下文 fused kernel。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 moba；相对 PPL +0.49%。  sparse-attention long-context block-routing 基础模型 长上下文：注意力、递归状态与记忆 MoBA选择少数远程block时，为什么还要保留当前的因果block？ 块级路由负责寻找远处相关区域，当前块则承载尚未完成的近邻上下文。保留当前因果块可避免路由遗漏局部连续信息，并通过因果掩码限制可见位置；命中块内部仍执行token级attention。稀疏收益来自少读一些块，不意味着任意删块都能保持相同分布。 教学例子：当前句子的主语刚出现在本块，而远处章节包含背景知识。即便路由更偏爱远程章节，也不能把刚出现的主语一起排除，更不能读取当前块尚未生成的后缀。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-627cf3d7c1d91b13">MoBA选择少数远程block时，为什么还要保留当前的因果block？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amoba">MoBA: Mixture of Block Attention for Long-Context LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Moonshot AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>块级路由负责寻找远处相关区域，当前块则承载尚未完成的近邻上下文。保留当前因果块可避免路由遗漏局部连续信息，并通过因果掩码限制可见位置；命中块内部仍执行token级attention。稀疏收益来自少读一些块，不意味着任意删块都能保持相同分布。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>当前句子的主语刚出现在本块，而远处章节包含背景知识。即便路由更偏爱远程章节，也不能把刚出现的主语一起排除，更不能读取当前块尚未生成的后缀。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.13189">原论文</a> · <a href="../../../../reproductions/2502.13189-moba/">实现解读</a> · <a href="#qa-627cf3d7c1d91b13">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:moba" data-paper-title="MoBA: Mixture of Block Attention for Long-Context LLMs" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="MoBA: Mixture of Block Attention for Long-Context LLMs 基础模型 Moonshot AI 2025-02-18 把序列切成 block，以可微 router 为每个 query 选择少量相关块，同时保留当前因果块。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际将历史划分为 8-token blocks，以 query 对 block key centroid 的相似度选择 top-2 causal blocks，再在命中块内执行精确 attention；PyTorch reference 未复刻百万上下文 fused kernel。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 moba；相对 PPL +0.49%。  sparse-attention long-context block-routing 基础模型 长上下文：注意力、递归状态与记忆 MoBA 的按内容选块，相对固定最近窗口保留了什么可能性？ 固定窗口按位置截断，窗口外再相关也不可读；内容路由有机会选回远处相关块，但可能遗漏没被选中的证据。代价由块大小和选块预算共同决定，不能理解为无损裁剪。 示意：开头出现的人名可以因内容匹配被选回，而不是因太旧必然被丢掉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d037963927322859">MoBA 的按内容选块，相对固定最近窗口保留了什么可能性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amoba">MoBA: Mixture of Block Attention for Long-Context LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Moonshot AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定窗口按位置截断，窗口外再相关也不可读；内容路由有机会选回远处相关块，但可能遗漏没被选中的证据。代价由块大小和选块预算共同决定，不能理解为无损裁剪。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>开头出现的人名可以因内容匹配被选回，而不是因太旧必然被丢掉。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.13189">原论文</a> · <a href="../../../../reproductions/2502.13189-moba/">实现解读</a> · <a href="#qa-d037963927322859">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:moba" data-paper-title="MoBA: Mixture of Block Attention for Long-Context LLMs" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="MoBA: Mixture of Block Attention for Long-Context LLMs 基础模型 Moonshot AI 2025-02-18 把序列切成 block，以可微 router 为每个 query 选择少量相关块，同时保留当前因果块。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际将历史划分为 8-token blocks，以 query 对 block key centroid 的相似度选择 top-2 causal blocks，再在命中块内执行精确 attention；PyTorch reference 未复刻百万上下文 fused kernel。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 moba；相对 PPL +0.49%。  sparse-attention long-context block-routing 基础模型 长上下文：注意力、递归状态与记忆 实现 MoBA 时，选中当前块是否就可以忽略块内因果约束？ 不能。当前块里仍包含查询之后的位置，必须保留token级因果屏蔽。文档的本地参考用8-token块和top-2选择，属于具体缩小配置，不能直接当成百万上下文fused kernel。 示意：同在第一个8词块，第3词依然不能读取第7词。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-5f47a19dd639778f">实现 MoBA 时，选中当前块是否就可以忽略块内因果约束？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amoba">MoBA: Mixture of Block Attention for Long-Context LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Moonshot AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。当前块里仍包含查询之后的位置，必须保留token级因果屏蔽。文档的本地参考用8-token块和top-2选择，属于具体缩小配置，不能直接当成百万上下文fused kernel。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同在第一个8词块，第3词依然不能读取第7词。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.13189">原论文</a> · <a href="../../../../reproductions/2502.13189-moba/">实现解读</a> · <a href="#qa-5f47a19dd639778f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:native-sparse-attention" data-paper-title="Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention 基础模型 DeepSeek 2025-02-16 全注意力的计算和 KV 读取随上下文长度平方增长。NSA 不是在训练后裁剪 attention，而是从预训练开始并行学习三条路径：压缩历史块负责全局轮廓，query 相关的 block selection 恢复重要细节，滑窗保留近期精确信息；三路输出再由可学习门控融合。 未执行 27B continued pretraining、64K benchmark 和定制 Triton kernel；Fidelity: 核心机制复现。真实训练压缩、选择和滑窗三条注意力分支；未复刻论文的 Triton kernel 与 27B 训练。未执行 27B continued pretraining、64K benchmark 和定制 Triton kernel；结果只支持“核心三路算子可训练且在当前短预算有效”，不能外推论文的规模或速度结论。本地对照口径：基线是同维度、层数、token、AdamW 和 30-step 预算的 llama_modern；  llm-architecture sparse-attention long-context 基础模型 长上下文：注意力、递归状态与记忆 NSA 为什么同时保留压缩、选择和滑窗三条注意力路径？ 压缩块提供全局轮廓，按query选中的细块补回细节，滑窗保留近期精确信息。三路承担不同信息职责，再由可学习门融合，避免仅靠一种稀疏方式覆盖全部需求。 示意：主题摘要、远处关键句和当前短语细节可以分别来自三条路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-native-sparse-attention-6720d24e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-564f44b322bba736">NSA 为什么同时保留压缩、选择和滑窗三条注意力路径？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Anative-sparse-attention">Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · DeepSeek</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>压缩块提供全局轮廓，按query选中的细块补回细节，滑窗保留近期精确信息。三路承担不同信息职责，再由可学习门融合，避免仅靠一种稀疏方式覆盖全部需求。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>主题摘要、远处关键句和当前短语细节可以分别来自三条路径。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.11089">原论文</a> · <a href="../../../../reproductions/2502.11089-native-sparse-attention/">实现解读</a> · <a href="#qa-564f44b322bba736">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:native-sparse-attention" data-paper-title="Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention 基础模型 DeepSeek 2025-02-16 全注意力的计算和 KV 读取随上下文长度平方增长。NSA 不是在训练后裁剪 attention，而是从预训练开始并行学习三条路径：压缩历史块负责全局轮廓，query 相关的 block selection 恢复重要细节，滑窗保留近期精确信息；三路输出再由可学习门控融合。 未执行 27B continued pretraining、64K benchmark 和定制 Triton kernel；Fidelity: 核心机制复现。真实训练压缩、选择和滑窗三条注意力分支；未复刻论文的 Triton kernel 与 27B 训练。未执行 27B continued pretraining、64K benchmark 和定制 Triton kernel；结果只支持“核心三路算子可训练且在当前短预算有效”，不能外推论文的规模或速度结论。本地对照口径：基线是同维度、层数、token、AdamW 和 30-step 预算的 llama_modern；  llm-architecture sparse-attention long-context 基础模型 长上下文：注意力、递归状态与记忆 NSA已经有压缩历史，为什么还要选择原始块和保留滑动窗口？ 压缩块提供便宜的全局轮廓，却可能抹掉关键token细节；选择分支再根据当前查询读取重要原始块，滑窗保留近期精确信息。三条路径承担不同信息粒度，从预训练起一起学习并融合，不是训练结束后临时删掉部分attention。三路都必须保持因果性。 教学例子：压缩摘要能告诉模型某章讲日期，却可能分不清两个年份；选中该章后读取原始token来区分，同时从滑窗保留当前句子的限定条件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f731030c47e87c33">NSA已经有压缩历史，为什么还要选择原始块和保留滑动窗口？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Anative-sparse-attention">Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · DeepSeek</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>压缩块提供便宜的全局轮廓，却可能抹掉关键token细节；选择分支再根据当前查询读取重要原始块，滑窗保留近期精确信息。三条路径承担不同信息粒度，从预训练起一起学习并融合，不是训练结束后临时删掉部分attention。三路都必须保持因果性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>压缩摘要能告诉模型某章讲日期，却可能分不清两个年份；选中该章后读取原始token来区分，同时从滑窗保留当前句子的限定条件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.11089">原论文</a> · <a href="../../../../reproductions/2502.11089-native-sparse-attention/">实现解读</a> · <a href="#qa-f731030c47e87c33">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:native-sparse-attention" data-paper-title="Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention 基础模型 DeepSeek 2025-02-16 全注意力的计算和 KV 读取随上下文长度平方增长。NSA 不是在训练后裁剪 attention，而是从预训练开始并行学习三条路径：压缩历史块负责全局轮廓，query 相关的 block selection 恢复重要细节，滑窗保留近期精确信息；三路输出再由可学习门控融合。 未执行 27B continued pretraining、64K benchmark 和定制 Triton kernel；Fidelity: 核心机制复现。真实训练压缩、选择和滑窗三条注意力分支；未复刻论文的 Triton kernel 与 27B 训练。未执行 27B continued pretraining、64K benchmark 和定制 Triton kernel；结果只支持“核心三路算子可训练且在当前短预算有效”，不能外推论文的规模或速度结论。本地对照口径：基线是同维度、层数、token、AdamW 和 30-step 预算的 llama_modern；  llm-architecture sparse-attention long-context 基础模型 长上下文：注意力、递归状态与记忆 NSA 与训练完成后简单裁掉低 attention 权重，有什么关键差别？ NSA从预训练起联合学习三路算子及其门控，而非只在已训练的dense模型上删除连接。它改变了训练时的信息通路；后处理裁剪不能自动获得同样的适应过程。 示意：模型从一开始就学会在摘要与细块之间取舍，区别于训练后突然拿走一部分历史。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a405b8a8da3af38e">NSA 与训练完成后简单裁掉低 attention 权重，有什么关键差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Anative-sparse-attention">Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · DeepSeek</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>NSA从预训练起联合学习三路算子及其门控，而非只在已训练的dense模型上删除连接。它改变了训练时的信息通路；后处理裁剪不能自动获得同样的适应过程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型从一开始就学会在摘要与细块之间取舍，区别于训练后突然拿走一部分历史。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.11089">原论文</a> · <a href="../../../../reproductions/2502.11089-native-sparse-attention/">实现解读</a> · <a href="#qa-a405b8a8da3af38e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:native-sparse-attention" data-paper-title="Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention 基础模型 DeepSeek 2025-02-16 全注意力的计算和 KV 读取随上下文长度平方增长。NSA 不是在训练后裁剪 attention，而是从预训练开始并行学习三条路径：压缩历史块负责全局轮廓，query 相关的 block selection 恢复重要细节，滑窗保留近期精确信息；三路输出再由可学习门控融合。 未执行 27B continued pretraining、64K benchmark 和定制 Triton kernel；Fidelity: 核心机制复现。真实训练压缩、选择和滑窗三条注意力分支；未复刻论文的 Triton kernel 与 27B 训练。未执行 27B continued pretraining、64K benchmark 和定制 Triton kernel；结果只支持“核心三路算子可训练且在当前短预算有效”，不能外推论文的规模或速度结论。本地对照口径：基线是同维度、层数、token、AdamW 和 30-step 预算的 llama_modern；  llm-architecture sparse-attention long-context 基础模型 长上下文：注意力、递归状态与记忆 NSA 三条分支都需要遵守因果边界吗？ 需要。压缩块、选中的细块和局部滑窗都不能包含当前查询的未来信息；各分支输出还需对齐维度再门控融合。本地edge proxy只计连接数量，不代表已经实现论文Triton吞吐。 示意：被选中的块若跨过当前位置，仍要屏蔽块内尚未出现的词。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f9175d8e49ec4071">NSA 三条分支都需要遵守因果边界吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Anative-sparse-attention">Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · DeepSeek</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>需要。压缩块、选中的细块和局部滑窗都不能包含当前查询的未来信息；各分支输出还需对齐维度再门控融合。本地edge proxy只计连接数量，不代表已经实现论文Triton吞吐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>被选中的块若跨过当前位置，仍要屏蔽块内尚未出现的词。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.11089">原论文</a> · <a href="../../../../reproductions/2502.11089-native-sparse-attention/">实现解读</a> · <a href="#qa-f9175d8e49ec4071">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:hymba" data-paper-title="Hymba: A Hybrid-head Architecture for Small Language Models" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Hymba: A Hybrid-head Architecture for Small Language Models 基础模型 NVIDIA 2024-11-20 同一层并行执行 attention 与状态空间分支，再用输入相关 gate 融合局部精确检索和线性长程状态。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际在每层并行执行 causal attention 与深度卷积状态分支，并以输入相关 gate 融合；未复刻 1.5B 参数、meta tokens 和 fused kernel。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 hymba；相对 PPL +8.53%。  hybrid-attention-ssm small-language-model architecture 基础模型 长上下文：注意力、递归状态与记忆 Hymba 为什么同时需要显式历史读取和递归摘要？ 显式attention适合直接找回某些位置的信息，状态空间分支把历史压缩为递归状态。混合架构希望在同层结合这两种访问方式，而不是要求其中一种承担所有依赖。 示意：找回上文姓名与维护持续语法状态，可以分别受益于具体位置读取和递归累积。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-hymba-2cf1482a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0efbea46861fa34b">Hymba 为什么同时需要显式历史读取和递归摘要？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ahymba">Hymba: A Hybrid-head Architecture for Small Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NVIDIA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>显式attention适合直接找回某些位置的信息，状态空间分支把历史压缩为递归状态。混合架构希望在同层结合这两种访问方式，而不是要求其中一种承担所有依赖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>找回上文姓名与维护持续语法状态，可以分别受益于具体位置读取和递归累积。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2411.13676">原论文</a> · <a href="../../../../reproductions/2411.13676-hymba/">实现解读</a> · <a href="#qa-0efbea46861fa34b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:hymba" data-paper-title="Hymba: A Hybrid-head Architecture for Small Language Models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Hymba: A Hybrid-head Architecture for Small Language Models 基础模型 NVIDIA 2024-11-20 同一层并行执行 attention 与状态空间分支，再用输入相关 gate 融合局部精确检索和线性长程状态。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际在每层并行执行 causal attention 与深度卷积状态分支，并以输入相关 gate 融合；未复刻 1.5B 参数、meta tokens 和 fused kernel。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 hymba；相对 PPL +8.53%。  hybrid-attention-ssm small-language-model architecture 基础模型 长上下文：注意力、递归状态与记忆 Hymba为什么在同一层并行放attention和SSM，而不简单轮流堆两种层？ 并行分支让同一份当前输入同时获得显式历史读取和递归状态摘要，再融合两种输出。attention可补充直接检索，SSM提供另一种历史压缩路径；两者在一次层更新中协作。这样安排并不意味着两个分支免费运行，融合方式、KV缓存与状态预算仍共同影响成本。 教学例子：当前词既需要找回前文的一个名字，又依赖持续累积的语法状态；同层可分别读取具体位置与递归摘要，再把两种信号交给下一层。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-957edc876261c0c0">Hymba为什么在同一层并行放attention和SSM，而不简单轮流堆两种层？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ahymba">Hymba: A Hybrid-head Architecture for Small Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NVIDIA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>并行分支让同一份当前输入同时获得显式历史读取和递归状态摘要，再融合两种输出。attention可补充直接检索，SSM提供另一种历史压缩路径；两者在一次层更新中协作。这样安排并不意味着两个分支免费运行，融合方式、KV缓存与状态预算仍共同影响成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>当前词既需要找回前文的一个名字，又依赖持续累积的语法状态；同层可分别读取具体位置与递归摘要，再把两种信号交给下一层。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2411.13676">原论文</a> · <a href="../../../../reproductions/2411.13676-hymba/">实现解读</a> · <a href="#qa-957edc876261c0c0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:hymba" data-paper-title="Hymba: A Hybrid-head Architecture for Small Language Models" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Hymba: A Hybrid-head Architecture for Small Language Models 基础模型 NVIDIA 2024-11-20 同一层并行执行 attention 与状态空间分支，再用输入相关 gate 融合局部精确检索和线性长程状态。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际在每层并行执行 causal attention 与深度卷积状态分支，并以输入相关 gate 融合；未复刻 1.5B 参数、meta tokens 和 fused kernel。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 hymba；相对 PPL +8.53%。  hybrid-attention-ssm small-language-model architecture 基础模型 长上下文：注意力、递归状态与记忆 同层并行的 Hymba，与交替堆 attention 层和 SSM 层有什么结构差异？ 并行结构让同一输入在一次层更新中进入两条分支，再融合输出；交替堆叠则让后一类层读取前一层已经变换的结果。两者的计算图和信息融合时机不同，不能仅按层数视为等价。 示意：并行时两位读者同时看原输入再合议，交替时第二位只先接到第一位整理后的表示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c2fee06492c5f6c0">同层并行的 Hymba，与交替堆 attention 层和 SSM 层有什么结构差异？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ahymba">Hymba: A Hybrid-head Architecture for Small Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NVIDIA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>并行结构让同一输入在一次层更新中进入两条分支，再融合输出；交替堆叠则让后一类层读取前一层已经变换的结果。两者的计算图和信息融合时机不同，不能仅按层数视为等价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>并行时两位读者同时看原输入再合议，交替时第二位只先接到第一位整理后的表示。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2411.13676">原论文</a> · <a href="../../../../reproductions/2411.13676-hymba/">实现解读</a> · <a href="#qa-c2fee06492c5f6c0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:hymba" data-paper-title="Hymba: A Hybrid-head Architecture for Small Language Models" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Hymba: A Hybrid-head Architecture for Small Language Models 基础模型 NVIDIA 2024-11-20 同一层并行执行 attention 与状态空间分支，再用输入相关 gate 融合局部精确检索和线性长程状态。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际在每层并行执行 causal attention 与深度卷积状态分支，并以输入相关 gate 融合；未复刻 1.5B 参数、meta tokens 和 fused kernel。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 hymba；相对 PPL +8.53%。  hybrid-attention-ssm small-language-model architecture 基础模型 长上下文：注意力、递归状态与记忆 本地 Hymba 路径已经覆盖原论文所有结构与吞吐优化了吗？ 没有。当前文档记录的是causal attention与深度卷积状态分支的并行融合，未复刻meta tokens、1.5B规模与fused kernel。实现或复用时应明确这些边界，不能由分支可执行推导论文吞吐。 示意：小模型里门控融合能前向通过，只证明这条本地路径可运行，不证明完整Hymba部署速度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c7d03a30101239fb">本地 Hymba 路径已经覆盖原论文所有结构与吞吐优化了吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ahymba">Hymba: A Hybrid-head Architecture for Small Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NVIDIA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。当前文档记录的是causal attention与深度卷积状态分支的并行融合，未复刻meta tokens、1.5B规模与fused kernel。实现或复用时应明确这些边界，不能由分支可执行推导论文吞吐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>小模型里门控融合能前向通过，只证明这条本地路径可运行，不证明完整Hymba部署速度。</p>
<p class="ar-learning-sources">依据：复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2411.13676">原论文</a> · <a href="../../../../reproductions/2411.13676-hymba/">实现解读</a> · <a href="#qa-c7d03a30101239fb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mamba" data-paper-title="Mamba: Linear-Time Sequence Modeling with Selective State Spaces" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Mamba: Linear-Time Sequence Modeling with Selective State Spaces 基础模型 Carnegie Mellon University / Princeton University 2023-12-01 Mamba 让 SSM 的步长、读写向量依赖当前 token，从而选择性保留信息，同时保持序列长度线性复杂度。 Fidelity: 核心机制复现。实现输入相关的 selective SSM、因果 depthwise convolution 与门控输出。未使用 fused parallel scan CUDA kernel，也没有 2.8B 规模预训练；短预算结果不代表论文规模结论。本地对照口径：基线是 tiny Transformer；实验组是原生 PyTorch selective scan；WikiText-2 30-step perplexity 相对 +48.82%（变差）。  llm-architecture state-space-model classic 基础模型 长上下文：注意力、递归状态与记忆 Mamba 的“选择性”为什么与当前 token 有关？ 它让SSM步长和读写向量依赖当前输入，从而按内容决定哪些信息保留、更新和读出。递归状态仍然存在，但状态转移不再对所有token使用完全相同的选择规则。 示意：分隔符与包含答案的词可以触发不同的状态更新，而非一律按同一强度写入。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-mamba-0b65990c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7a505778b7bd7571">Mamba 的“选择性”为什么与当前 token 有关？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amamba">Mamba: Linear-Time Sequence Modeling with Selective State Spaces</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Carnegie Mellon University / Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它让SSM步长和读写向量依赖当前输入，从而按内容决定哪些信息保留、更新和读出。递归状态仍然存在，但状态转移不再对所有token使用完全相同的选择规则。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>分隔符与包含答案的词可以触发不同的状态更新，而非一律按同一强度写入。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2312.00752">原论文</a> · <a href="../../../../reproductions/2312.00752-mamba/">实现解读</a> · <a href="#qa-7a505778b7bd7571">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mamba" data-paper-title="Mamba: Linear-Time Sequence Modeling with Selective State Spaces" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Mamba: Linear-Time Sequence Modeling with Selective State Spaces 基础模型 Carnegie Mellon University / Princeton University 2023-12-01 Mamba 让 SSM 的步长、读写向量依赖当前 token，从而选择性保留信息，同时保持序列长度线性复杂度。 Fidelity: 核心机制复现。实现输入相关的 selective SSM、因果 depthwise convolution 与门控输出。未使用 fused parallel scan CUDA kernel，也没有 2.8B 规模预训练；短预算结果不代表论文规模结论。本地对照口径：基线是 tiny Transformer；实验组是原生 PyTorch selective scan；WikiText-2 30-step perplexity 相对 +48.82%（变差）。  llm-architecture state-space-model classic 基础模型 长上下文：注意力、递归状态与记忆 Mamba的“选择性”具体改变了SSM的什么，而不只是给输出加一个门？ 它让步长及读写方向随当前token变化，从而改变旧状态保留多久、当前输入写入哪里，以及状态怎样被读出。选择发生在递归更新内部，不只是最后对固定SSM结果做缩放。历史通过有限状态传播，长序列计算可保持线性，但精确找回任意旧token仍受状态容量影响。 教学例子：连续读到无关填充词时可以尽量保留已有状态，遇到关键编号时改变写入方向；之后回答编号仍取决于那部分信息是否被状态保留下来。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-53597ba087ad9762">Mamba的“选择性”具体改变了SSM的什么，而不只是给输出加一个门？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amamba">Mamba: Linear-Time Sequence Modeling with Selective State Spaces</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Carnegie Mellon University / Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它让步长及读写方向随当前token变化，从而改变旧状态保留多久、当前输入写入哪里，以及状态怎样被读出。选择发生在递归更新内部，不只是最后对固定SSM结果做缩放。历史通过有限状态传播，长序列计算可保持线性，但精确找回任意旧token仍受状态容量影响。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>连续读到无关填充词时可以尽量保留已有状态，遇到关键编号时改变写入方向；之后回答编号仍取决于那部分信息是否被状态保留下来。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2312.00752">原论文</a> · <a href="../../../../reproductions/2312.00752-mamba/">实现解读</a> · <a href="#qa-53597ba087ad9762">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mamba" data-paper-title="Mamba: Linear-Time Sequence Modeling with Selective State Spaces" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Mamba: Linear-Time Sequence Modeling with Selective State Spaces 基础模型 Carnegie Mellon University / Princeton University 2023-12-01 Mamba 让 SSM 的步长、读写向量依赖当前 token，从而选择性保留信息，同时保持序列长度线性复杂度。 Fidelity: 核心机制复现。实现输入相关的 selective SSM、因果 depthwise convolution 与门控输出。未使用 fused parallel scan CUDA kernel，也没有 2.8B 规模预训练；短预算结果不代表论文规模结论。本地对照口径：基线是 tiny Transformer；实验组是原生 PyTorch selective scan；WikiText-2 30-step perplexity 相对 +48.82%（变差）。  llm-architecture state-space-model classic 基础模型 长上下文：注意力、递归状态与记忆 Mamba 的状态更新，与 Transformer 从全部历史 KV 重新加权有什么差别？ Mamba把历史影响累积到递归状态，再由当前token相关的读出产生输出；attention可对保留的历史位置直接分配权重。前者改变了记忆与访问方式，不能把线性复杂度理解为逐词历史毫无损失。 示意：递归摘要可能保留一个事实的影响，却不等于保留每个历史词都可单独检索的槽位。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7b1c8ad148c1bce8">Mamba 的状态更新，与 Transformer 从全部历史 KV 重新加权有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amamba">Mamba: Linear-Time Sequence Modeling with Selective State Spaces</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Carnegie Mellon University / Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Mamba把历史影响累积到递归状态，再由当前token相关的读出产生输出；attention可对保留的历史位置直接分配权重。前者改变了记忆与访问方式，不能把线性复杂度理解为逐词历史毫无损失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>递归摘要可能保留一个事实的影响，却不等于保留每个历史词都可单独检索的槽位。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2312.00752">原论文</a> · <a href="../../../../reproductions/2312.00752-mamba/">实现解读</a> · <a href="#qa-7b1c8ad148c1bce8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mamba" data-paper-title="Mamba: Linear-Time Sequence Modeling with Selective State Spaces" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Mamba: Linear-Time Sequence Modeling with Selective State Spaces 基础模型 Carnegie Mellon University / Princeton University 2023-12-01 Mamba 让 SSM 的步长、读写向量依赖当前 token，从而选择性保留信息，同时保持序列长度线性复杂度。 Fidelity: 核心机制复现。实现输入相关的 selective SSM、因果 depthwise convolution 与门控输出。未使用 fused parallel scan CUDA kernel，也没有 2.8B 规模预训练；短预算结果不代表论文规模结论。本地对照口径：基线是 tiny Transformer；实验组是原生 PyTorch selective scan；WikiText-2 30-step perplexity 相对 +48.82%（变差）。  llm-architecture state-space-model classic 基础模型 长上下文：注意力、递归状态与记忆 用 Python/PyTorch 循环执行 selective scan，就能宣称复现 Mamba 的 kernel 吞吐吗？ 不能。循环版可检查输入依赖参数和逐步状态递推，但并不包含fused parallel scan CUDA kernel。文档还未运行2.8B预训练；需把算子正确性、端到端语言效果和系统吞吐分别验证。 示意：七步递推与参考式一致，是机制证据；每秒生成多少token则需要真实优化实现的单独测量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-275f57141b520ee1">用 Python/PyTorch 循环执行 selective scan，就能宣称复现 Mamba 的 kernel 吞吐吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amamba">Mamba: Linear-Time Sequence Modeling with Selective State Spaces</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Carnegie Mellon University / Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。循环版可检查输入依赖参数和逐步状态递推，但并不包含fused parallel scan CUDA kernel。文档还未运行2.8B预训练；需把算子正确性、端到端语言效果和系统吞吐分别验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>七步递推与参考式一致，是机制证据；每秒生成多少token则需要真实优化实现的单独测量。</p>
<p class="ar-learning-sources">依据：本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2312.00752">原论文</a> · <a href="../../../../reproductions/2312.00752-mamba/">实现解读</a> · <a href="#qa-275f57141b520ee1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:alibi" data-paper-title="Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation 基础模型 University of Washington / Meta AI 2021-08-27 不学习位置向量，而是在每个 head 的注意力 logits 上加入线性距离惩罚，实现 train-short/test-long 外推。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际移除位置 embedding，并对各 attention head 加不同斜率的因果距离线性 bias；WikiText-2 小模型未复跑论文 WikiText-103 1.3B 参数实验。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 alibi；相对 PPL +0.06%。  position-encoding length-extrapolation attention 基础模型 长上下文：注意力、递归状态与记忆 为什么 ALiBi 关心“训练看短文本、推理读长文本”？ 位置表示若只适配训练长度，推理遇到更远距离就可能失效。ALiBi用可继续计算的距离惩罚表达顺序，把位置偏好直接放进注意力分数；外推的是位置规则，长文本任务是否有效仍需评测。 示意：训练最长512词，推理出现第800词时仍能计算它与前文的距离，不需要查第800项位置表。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-alibi-69e595a8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-accc8fac0a859481">为什么 ALiBi 关心“训练看短文本、推理读长文本”？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aalibi">Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington / Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>位置表示若只适配训练长度，推理遇到更远距离就可能失效。ALiBi用可继续计算的距离惩罚表达顺序，把位置偏好直接放进注意力分数；外推的是位置规则，长文本任务是否有效仍需评测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练最长512词，推理出现第800词时仍能计算它与前文的距离，不需要查第800项位置表。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2108.12409">原论文</a> · <a href="../../../../reproductions/2108.12409-alibi/">实现解读</a> · <a href="#qa-accc8fac0a859481">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:alibi" data-paper-title="Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation 基础模型 University of Washington / Meta AI 2021-08-27 不学习位置向量，而是在每个 head 的注意力 logits 上加入线性距离惩罚，实现 train-short/test-long 外推。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际移除位置 embedding，并对各 attention head 加不同斜率的因果距离线性 bias；WikiText-2 小模型未复跑论文 WikiText-103 1.3B 参数实验。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 alibi；相对 PPL +0.06%。  position-encoding length-extrapolation attention 基础模型 长上下文：注意力、递归状态与记忆 ALiBi不加位置向量，模型怎样知道两个token离得有多远？ 它直接在每个注意力头的匹配分数上减去与距离成正比的偏置。距离越远，读到该位置需要更强的内容匹配来抵消惩罚；不同头的斜率提供不同距离偏好。偏置可以在更长位置上计算，不依赖一张只训练到固定长度的位置表，但这不保证任意长上下文都能正确检索。 教学例子：两个历史词的内容分数相同，一个距离2、一个距离20；距离惩罚让较近者得到更高权重。若远处包含独特答案，它仍需凭更强内容匹配胜出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-d919373883619f72">ALiBi不加位置向量，模型怎样知道两个token离得有多远？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aalibi">Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington / Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它直接在每个注意力头的匹配分数上减去与距离成正比的偏置。距离越远，读到该位置需要更强的内容匹配来抵消惩罚；不同头的斜率提供不同距离偏好。偏置可以在更长位置上计算，不依赖一张只训练到固定长度的位置表，但这不保证任意长上下文都能正确检索。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个历史词的内容分数相同，一个距离2、一个距离20；距离惩罚让较近者得到更高权重。若远处包含独特答案，它仍需凭更强内容匹配胜出。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2108.12409">原论文</a> · <a href="../../../../reproductions/2108.12409-alibi/">实现解读</a> · <a href="#qa-d919373883619f72">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:alibi" data-paper-title="Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation 基础模型 University of Washington / Meta AI 2021-08-27 不学习位置向量，而是在每个 head 的注意力 logits 上加入线性距离惩罚，实现 train-short/test-long 外推。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际移除位置 embedding，并对各 attention head 加不同斜率的因果距离线性 bias；WikiText-2 小模型未复跑论文 WikiText-103 1.3B 参数实验。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 alibi；相对 PPL +0.06%。  position-encoding length-extrapolation attention 基础模型 长上下文：注意力、递归状态与记忆 ALiBi 的线性偏置与给 token 加位置 embedding，分别改动哪里？ 位置embedding先修改token表示，再由投影产生Q/K/V；ALiBi不学习位置向量，而直接给各头的匹配分数加距离偏置。这是信息进入模型的位置不同，不能只把两者都叫“加一个位置数值”。 示意：同一对内容向量可以保持不变，但在不同距离下获得不同logit惩罚。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e857b141de1beae3">ALiBi 的线性偏置与给 token 加位置 embedding，分别改动哪里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aalibi">Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington / Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>位置embedding先修改token表示，再由投影产生Q/K/V；ALiBi不学习位置向量，而直接给各头的匹配分数加距离偏置。这是信息进入模型的位置不同，不能只把两者都叫“加一个位置数值”。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一对内容向量可以保持不变，但在不同距离下获得不同logit惩罚。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2108.12409">原论文</a> · <a href="../../../../reproductions/2108.12409-alibi/">实现解读</a> · <a href="#qa-e857b141de1beae3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:alibi" data-paper-title="Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation 基础模型 University of Washington / Meta AI 2021-08-27 不学习位置向量，而是在每个 head 的注意力 logits 上加入线性距离惩罚，实现 train-short/test-long 外推。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际移除位置 embedding，并对各 attention head 加不同斜率的因果距离线性 bias；WikiText-2 小模型未复跑论文 WikiText-103 1.3B 参数实验。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 alibi；相对 PPL +0.06%。  position-encoding length-extrapolation attention 基础模型 长上下文：注意力、递归状态与记忆 实现 ALiBi 时，只减距离就能替代因果 mask 吗？ 不能。距离偏置改变可见位置之间的偏好，因果mask决定未来位置是否可见。需要按head广播各自斜率，并继续屏蔽未来；本地小模型结果也不能证明论文大规模长上下文收益。 示意：第3词对第4词虽只有距离1，仍必须被因果mask排除。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e0295b696e351666">实现 ALiBi 时，只减距离就能替代因果 mask 吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aalibi">Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington / Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。距离偏置改变可见位置之间的偏好，因果mask决定未来位置是否可见。需要按head广播各自斜率，并继续屏蔽未来；本地小模型结果也不能证明论文大规模长上下文收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第3词对第4词虽只有距离1，仍必须被因果mask排除。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2108.12409">原论文</a> · <a href="../../../../reproductions/2108.12409-alibi/">实现解读</a> · <a href="#qa-e0295b696e351666">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:rope" data-paper-title="RoFormer: Enhanced Transformer with Rotary Position Embedding" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="RoFormer: Enhanced Transformer with Rotary Position Embedding 基础模型 Zhuiyi Technology 2021-04-20 对每个 attention head 的 Q/K 二维子空间施加随位置旋转，使点积天然只依赖相对位移。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际对每个注意力 head 的 Q/K 执行复数平面旋转并由相对相位进入 dot product；WikiText-2 64d 小模型替代论文中文 RoFormer 预训练。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 rope；相对 PPL +0.00%。  position-encoding long-context architecture 基础模型 长上下文：注意力、递归状态与记忆 RoPE 为什么把位置作用在 Q/K 的二维子空间里？ 位置控制二维旋转角度，Q与K的点积便带上相对位移的相位关系。它让匹配分数同时依赖内容和相对位置，不必给每个位置单独学习一项向量。 示意：相同内容相隔2词和20词，可因相对旋转不同而获得不同匹配分数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<span id="paper-foundation-models-rope-baa4b020" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-821e31f5f271e6be">RoPE 为什么把位置作用在 Q/K 的二维子空间里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Arope">RoFormer: Enhanced Transformer with Rotary Position Embedding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhuiyi Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>位置控制二维旋转角度，Q与K的点积便带上相对位移的相位关系。它让匹配分数同时依赖内容和相对位置，不必给每个位置单独学习一项向量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>相同内容相隔2词和20词，可因相对旋转不同而获得不同匹配分数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2104.09864">原论文</a> · <a href="../../../../reproductions/2104.09864-rope/">实现解读</a> · <a href="#qa-821e31f5f271e6be">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:rope" data-paper-title="RoFormer: Enhanced Transformer with Rotary Position Embedding" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="RoFormer: Enhanced Transformer with Rotary Position Embedding 基础模型 Zhuiyi Technology 2021-04-20 对每个 attention head 的 Q/K 二维子空间施加随位置旋转，使点积天然只依赖相对位移。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际对每个注意力 head 的 Q/K 执行复数平面旋转并由相对相位进入 dot product；WikiText-2 64d 小模型替代论文中文 RoFormer 预训练。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 rope；相对 PPL +0.00%。  position-encoding long-context architecture 基础模型 长上下文：注意力、递归状态与记忆 RoPE给Q和K分别加了绝对位置旋转，为什么点积却能表达相对位置？ 位置m、n对应的旋转在点积中组合，前一个旋转的转置抵消共同的绝对部分，留下与n减m相关的旋转。因此内容匹配中自然带上相对位移。被旋转的是Q/K子空间，不是把value直接标成位置；能计算更远位置也不等于经过训练的检索能力无限外推。 教学例子：把两个词同时从位置3、8平移到13、18，二者距离仍是5；位置旋转在点积中的相对关系保持一致，而内容本身仍由投影决定。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-9430b8ac22a0b9f9">RoPE给Q和K分别加了绝对位置旋转，为什么点积却能表达相对位置？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Arope">RoFormer: Enhanced Transformer with Rotary Position Embedding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhuiyi Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>位置m、n对应的旋转在点积中组合，前一个旋转的转置抵消共同的绝对部分，留下与n减m相关的旋转。因此内容匹配中自然带上相对位移。被旋转的是Q/K子空间，不是把value直接标成位置；能计算更远位置也不等于经过训练的检索能力无限外推。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把两个词同时从位置3、8平移到13、18，二者距离仍是5；位置旋转在点积中的相对关系保持一致，而内容本身仍由投影决定。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2104.09864">原论文</a> · <a href="../../../../reproductions/2104.09864-rope/">实现解读</a> · <a href="#qa-9430b8ac22a0b9f9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:rope" data-paper-title="RoFormer: Enhanced Transformer with Rotary Position Embedding" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="RoFormer: Enhanced Transformer with Rotary Position Embedding 基础模型 Zhuiyi Technology 2021-04-20 对每个 attention head 的 Q/K 二维子空间施加随位置旋转，使点积天然只依赖相对位移。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际对每个注意力 head 的 Q/K 执行复数平面旋转并由相对相位进入 dot product；WikiText-2 64d 小模型替代论文中文 RoFormer 预训练。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 rope；相对 PPL +0.00%。  position-encoding long-context architecture 基础模型 长上下文：注意力、递归状态与记忆 RoPE 的旋转位置表示，与直接加绝对位置向量有什么计算差异？ 绝对位置向量先加到表示里；RoPE旋转Q/K，使两者内积中的位置部分可写成相对旋转。两者注入位置的运算不同，不能只因都用位置编号就按同一公式实现。 示意：两段内容整体平移后，相对位移不变，RoPE的相对相位关系也保持对应。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-22c3fb74dae17ab4">RoPE 的旋转位置表示，与直接加绝对位置向量有什么计算差异？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Arope">RoFormer: Enhanced Transformer with Rotary Position Embedding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhuiyi Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>绝对位置向量先加到表示里；RoPE旋转Q/K，使两者内积中的位置部分可写成相对旋转。两者注入位置的运算不同，不能只因都用位置编号就按同一公式实现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两段内容整体平移后，相对位移不变，RoPE的相对相位关系也保持对应。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2104.09864">原论文</a> · <a href="../../../../reproductions/2104.09864-rope/">实现解读</a> · <a href="#qa-22c3fb74dae17ab4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:rope" data-paper-title="RoFormer: Enhanced Transformer with Rotary Position Embedding" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/context-and-state" data-search="RoFormer: Enhanced Transformer with Rotary Position Embedding 基础模型 Zhuiyi Technology 2021-04-20 对每个 attention head 的 Q/K 二维子空间施加随位置旋转，使点积天然只依赖相对位移。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际对每个注意力 head 的 Q/K 执行复数平面旋转并由相对相位进入 dot product；WikiText-2 64d 小模型替代论文中文 RoFormer 预训练。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 rope；相对 PPL +0.00%。  position-encoding long-context architecture 基础模型 长上下文：注意力、递归状态与记忆 实现 RoPE 时，Q 与 K 只旋转其中一个可以吗？ 不可以按此替代文档公式。相对位移来自R_m与R_n共同进入点积；要正确配对二维通道，并让增量解码的位置编号延续历史，而非每一步重置为0。 示意：生成第100个位置时仍需使用位置100的旋转，不能因当前只输入一个token就当作位置0。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 长上下文：注意力、递归状态与记忆</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-fcc3c0bb705d3c12">实现 RoPE 时，Q 与 K 只旋转其中一个可以吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Arope">RoFormer: Enhanced Transformer with Rotary Position Embedding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhuiyi Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不可以按此替代文档公式。相对位移来自R_m与R_n共同进入点积；要正确配对二维通道，并让增量解码的位置编号延续历史，而非每一步重置为0。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>生成第100个位置时仍需使用位置100的旋转，不能因当前只输入一个token就当作位置0。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2104.09864">原论文</a> · <a href="../../../../reproductions/2104.09864-rope/">实现解读</a> · <a href="#qa-fcc3c0bb705d3c12">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

上下文变长时，模型保留的是可寻址的历史 token，还是压缩后的递归状态？

## 记住这一点

先分清位置关系、信息访问和状态容量。RoPE 对 Q/K 的二维子空间作位置相关旋转，让点积表达相对位移；它仍允许注意力访问窗口内历史。Mamba 则让状态更新的步长和读写参数依赖当前输入，把历史汇入递归状态。稀疏注意力和混合结构在两端之间选择：只读部分历史，或让部分层保留完整访问。

## 一个例子

假设文档开头定义变量 x，三万 token 后要找回定义。完整注意力可以直接查询对应位置；递归模型必须把所需信息持续保存在状态里。若只保留局部窗口，就要检查有没有全局层或额外记忆，而不能只看宣传的上下文长度。

## 什么时候要小心

线性复杂度不保证长距离精确检索，也不保证真实硬件更快。RoPE 不是无限长度外推保证；状态、窗口、训练长度和位置缩放都要一起核对。当前本地小模型结果不代表论文规模的能力。

## 先读这几篇

先读 RoFormer 的 Q/K 旋转，理解位置与相对关系；再读 Mamba 的输入相关状态更新，比较“直接读取历史”和“把历史写入状态”。之后按需要进入稀疏注意力、混合结构或外部记忆。

1. [RoFormer: Enhanced Transformer with Rotary Position Embedding](../../../reproductions/2104.09864-rope/README.md) · [原论文](https://arxiv.org/abs/2104.09864)
2. [Mamba: Linear-Time Sequence Modeling with Selective State Spaces](../../../reproductions/2312.00752-mamba/README.md) · [原论文](https://arxiv.org/abs/2312.00752)

## 自测一下

两个模型都支持 32k 输入，是否说明它们能同样准确地找回首段的任意细节？

??? note "展开参考答案"

    不能。输入长度只说明接口或运行范围；直接寻址、窗口裁剪、状态容量和训练分布不同，可能造成不同遗忘。应在同预算下用位置与干扰长度受控的检索任务验证。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
