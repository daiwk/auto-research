---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 自动研究与高效上线

[搜广推](index.md) / 76 个问题 · 19 篇论文

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
<p class="ar-learning-status" data-learning-status role="status">76 个问题 · 19 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:forte" data-paper-title="FORTE: A Production Framework for Feature Evaluation and Deprecation in Industrial Recommender Systems" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="FORTE: A Production Framework for Feature Evaluation and Deprecation in Industrial Recommender Systems 搜广推与 LLM 应用 Pinterest 2026-10-09 添加一个特征只需在某项指标上有收益，删除却不能损伤任何业务指标，而且同一个特征可能有多个模型消费者。FORTE 将退役流程拆成逐渐昂贵的门槛：先每天衡量冻结模型的特征依赖，检查长期稳定性，再联合扰动候选集合并真实重训，最后做线上实验和所有消费者的血缘审计。它不是单次 feature selection，也不能把单特征收益相加当成联合删除效果。一个特征单独看没有价值，可能与另一个冗余特征共同承载重要信号；不同输出头也可能给出相反方向。 结果仍是诊断，不能宣称复现 Pinterest 能力或吞吐收益。L2 公开数据训练，核心机制实现；结果仍是诊断，不能宣称复现 Pinterest 能力或吞吐收益。未复刻私有多模态特征、DCNv2/MMoE 大型 Pin Ranker、分布式 actor、每日生产 checkpoint sensors、线上 A/B 和实际基础设施移除。没有通过任一门槛也是有效结果，保留而不伪造通过。加载经过固定 archive SHA-256 校验的公开 MovieLens-100K。按 timestamp、user、item 排序，chronological 80/10/10；  features efficiency feature-deprecation 搜广推 自动研究与高效上线 FORTÉ 为什么把特征退役看成全生命周期任务，而非一次重要性排序？ 模型弱依赖只是开始，同一特征可被多个头和下游系统消费，训练适应后还可能重新依赖它。流程逐级检查时间稳定、联合删除、重训、线上及血缘，直到全部消费者允许退役。删除决策的证据比增加特征更全面，低重要性本身不是删除许可。 示意：某字段对主点击头无用，却仍被反欺诈模型读取；从一个模型移除不代表可停日志与数据生产，必须查完所有消费路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-forte-d5b8210d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-40320b35fc4a7114">FORTÉ 为什么把特征退役看成全生命周期任务，而非一次重要性排序？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aforte">FORTE: A Production Framework for Feature Evaluation and Deprecation in Industrial Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>模型弱依赖只是开始，同一特征可被多个头和下游系统消费，训练适应后还可能重新依赖它。流程逐级检查时间稳定、联合删除、重训、线上及血缘，直到全部消费者允许退役。删除决策的证据比增加特征更全面，低重要性本身不是删除许可。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某字段对主点击头无用，却仍被反欺诈模型读取；从一个模型移除不代表可停日志与数据生产，必须查完所有消费路径。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13806">原论文</a> · <a href="../../../../reproductions/2610.13806-forte/">实现解读</a> · <a href="#qa-40320b35fc4a7114">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:forte" data-paper-title="FORTE: A Production Framework for Feature Evaluation and Deprecation in Industrial Recommender Systems" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="FORTE: A Production Framework for Feature Evaluation and Deprecation in Industrial Recommender Systems 搜广推与 LLM 应用 Pinterest 2026-10-09 添加一个特征只需在某项指标上有收益，删除却不能损伤任何业务指标，而且同一个特征可能有多个模型消费者。FORTE 将退役流程拆成逐渐昂贵的门槛：先每天衡量冻结模型的特征依赖，检查长期稳定性，再联合扰动候选集合并真实重训，最后做线上实验和所有消费者的血缘审计。它不是单次 feature selection，也不能把单特征收益相加当成联合删除效果。一个特征单独看没有价值，可能与另一个冗余特征共同承载重要信号；不同输出头也可能给出相反方向。 结果仍是诊断，不能宣称复现 Pinterest 能力或吞吐收益。L2 公开数据训练，核心机制实现；结果仍是诊断，不能宣称复现 Pinterest 能力或吞吐收益。未复刻私有多模态特征、DCNv2/MMoE 大型 Pin Ranker、分布式 actor、每日生产 checkpoint sensors、线上 A/B 和实际基础设施移除。没有通过任一门槛也是有效结果，保留而不伪造通过。加载经过固定 archive SHA-256 校验的公开 MovieLens-100K。按 timestamp、user、item 排序，chronological 80/10/10；  features efficiency feature-deprecation 搜广推 自动研究与高效上线 两个特征各自删除都几乎不掉分，FORTE为什么仍要求联合扰动、重训和消费者审计？ 单特征扰动衡量的是其余信号仍存在时的依赖，两个冗余特征可能互相补偿，同时删除才暴露损失。FORTE先检查跨时间、跨输出头的稳定弱依赖，再逐级做联合扰动和真实重训；最终还要确认所有下游消费者均可退役，不能把某个模型的一次零损失当全链路删除许可。 示意：用户年龄和年龄分桶互相替代，单删一个不掉分；同时删除可能伤害新用户任务，因此还需检查其他输出头与消费它的模型。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-6ba8284366c5569d">两个特征各自删除都几乎不掉分，FORTE为什么仍要求联合扰动、重训和消费者审计？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aforte">FORTE: A Production Framework for Feature Evaluation and Deprecation in Industrial Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单特征扰动衡量的是其余信号仍存在时的依赖，两个冗余特征可能互相补偿，同时删除才暴露损失。FORTE先检查跨时间、跨输出头的稳定弱依赖，再逐级做联合扰动和真实重训；最终还要确认所有下游消费者均可退役，不能把某个模型的一次零损失当全链路删除许可。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户年龄和年龄分桶互相替代，单删一个不掉分；同时删除可能伤害新用户任务，因此还需检查其他输出头与消费它的模型。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13806">原论文</a> · <a href="../../../../reproductions/2610.13806-forte/">实现解读</a> · <a href="#qa-6ba8284366c5569d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:forte" data-paper-title="FORTE: A Production Framework for Feature Evaluation and Deprecation in Industrial Recommender Systems" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="FORTE: A Production Framework for Feature Evaluation and Deprecation in Industrial Recommender Systems 搜广推与 LLM 应用 Pinterest 2026-10-09 添加一个特征只需在某项指标上有收益，删除却不能损伤任何业务指标，而且同一个特征可能有多个模型消费者。FORTE 将退役流程拆成逐渐昂贵的门槛：先每天衡量冻结模型的特征依赖，检查长期稳定性，再联合扰动候选集合并真实重训，最后做线上实验和所有消费者的血缘审计。它不是单次 feature selection，也不能把单特征收益相加当成联合删除效果。一个特征单独看没有价值，可能与另一个冗余特征共同承载重要信号；不同输出头也可能给出相反方向。 结果仍是诊断，不能宣称复现 Pinterest 能力或吞吐收益。L2 公开数据训练，核心机制实现；结果仍是诊断，不能宣称复现 Pinterest 能力或吞吐收益。未复刻私有多模态特征、DCNv2/MMoE 大型 Pin Ranker、分布式 actor、每日生产 checkpoint sensors、线上 A/B 和实际基础设施移除。没有通过任一门槛也是有效结果，保留而不伪造通过。加载经过固定 archive SHA-256 校验的公开 MovieLens-100K。按 timestamp、user、item 排序，chronological 80/10/10；  features efficiency feature-deprecation 搜广推 自动研究与高效上线 冻结扰动与真实删特征重训分别回答什么问题，为什么不能只保留一个？ 冻结扰动测当前模型立即依赖，重训测网络是否能在缺失后重新适应，二者都不涵盖所有线上影响。单次弱依赖可能靠冗余补偿，重训成功也不能覆盖之前时间门槛失败。来源本地三种子保留基线，是流程有效负结果而非删特征成功。 示意：拔掉年龄字段当前模型变差，但重训可用其他信号补回；反过来单删没影响，两字段联合删除却可能受损，两个阶段各有用途。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f74a47ab0fc224b5">冻结扰动与真实删特征重训分别回答什么问题，为什么不能只保留一个？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aforte">FORTE: A Production Framework for Feature Evaluation and Deprecation in Industrial Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冻结扰动测当前模型立即依赖，重训测网络是否能在缺失后重新适应，二者都不涵盖所有线上影响。单次弱依赖可能靠冗余补偿，重训成功也不能覆盖之前时间门槛失败。来源本地三种子保留基线，是流程有效负结果而非删特征成功。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>拔掉年龄字段当前模型变差，但重训可用其他信号补回；反过来单删没影响，两字段联合删除却可能受损，两个阶段各有用途。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13806">原论文</a> · <a href="../../../../reproductions/2610.13806-forte/">实现解读</a> · <a href="#qa-f74a47ab0fc224b5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:forte" data-paper-title="FORTE: A Production Framework for Feature Evaluation and Deprecation in Industrial Recommender Systems" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="FORTE: A Production Framework for Feature Evaluation and Deprecation in Industrial Recommender Systems 搜广推与 LLM 应用 Pinterest 2026-10-09 添加一个特征只需在某项指标上有收益，删除却不能损伤任何业务指标，而且同一个特征可能有多个模型消费者。FORTE 将退役流程拆成逐渐昂贵的门槛：先每天衡量冻结模型的特征依赖，检查长期稳定性，再联合扰动候选集合并真实重训，最后做线上实验和所有消费者的血缘审计。它不是单次 feature selection，也不能把单特征收益相加当成联合删除效果。一个特征单独看没有价值，可能与另一个冗余特征共同承载重要信号；不同输出头也可能给出相反方向。 结果仍是诊断，不能宣称复现 Pinterest 能力或吞吐收益。L2 公开数据训练，核心机制实现；结果仍是诊断，不能宣称复现 Pinterest 能力或吞吐收益。未复刻私有多模态特征、DCNv2/MMoE 大型 Pin Ranker、分布式 actor、每日生产 checkpoint sensors、线上 A/B 和实际基础设施移除。没有通过任一门槛也是有效结果，保留而不伪造通过。加载经过固定 archive SHA-256 校验的公开 MovieLens-100K。按 timestamp、user、item 排序，chronological 80/10/10；  features efficiency feature-deprecation 搜广推 自动研究与高效上线 FORTÉ 的 signed_change 为什么可能为负，VirtualBatch 又如何保证测的是冻结依赖？ 高优指标按扰动减基线计算，负值表示损害，不应翻成“重要性越大越好”。VirtualBatch 复用同一 dense、sparse、ragged 原值与扰动字典，各组只切引用；前后参数摘要核对防止前向期间更新。联合边际也不能用单特征变化相加替代。 示意：AUC 从零点八降到零点七九得到负变化，说明依赖而非收益；若评估时悄悄训练了几步补回，就不再测冻结模型的特征依赖。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-de0c178c54f394ff">FORTÉ 的 signed_change 为什么可能为负，VirtualBatch 又如何保证测的是冻结依赖？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aforte">FORTE: A Production Framework for Feature Evaluation and Deprecation in Industrial Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>高优指标按扰动减基线计算，负值表示损害，不应翻成“重要性越大越好”。VirtualBatch 复用同一 dense、sparse、ragged 原值与扰动字典，各组只切引用；前后参数摘要核对防止前向期间更新。联合边际也不能用单特征变化相加替代。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>AUC 从零点八降到零点七九得到负变化，说明依赖而非收益；若评估时悄悄训练了几步补回，就不再测冻结模型的特征依赖。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13806">原论文</a> · <a href="../../../../reproductions/2610.13806-forte/">实现解读</a> · <a href="#qa-de0c178c54f394ff">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:effective-training-time" data-paper-title="Optimizing Effective Training Time for Large-Scale Recommendation Systems" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Optimizing Effective Training Time for Large-Scale Recommendation Systems 搜广推与 LLM 应用 Meta Platforms, Inc. 2026-10-01 把端到端 wall time 分为真正消费新数据的训练时间与初始化、编译、checkpoint、发布和恢复等生命周期损耗，再按 owner 定位和优化。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 ETT 分解与 owner loss 归因；这是用户批准的生产基础设施例外，不声称推荐模型效果或线上 A/B 收益。收录例外：用户于 2026-10-02 明确批准的生产训练基础设施例外；部署指标是 ETT，不作为推荐模型效果或线上 A/B 收益。执行 ETT 分解与 owner loss 归因；这是用户批准的生产基础设施例外，不声称推荐模型效果或线上 A/B 收益。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  training-systems effective-training-time gpu-fleet 搜广推 自动研究与高效上线 GPU已经满负荷运行，为什么Effective Training Time仍可能很低？ ETT关注总生命周期里真正用于消费新数据的训练时间占比，初始化、编译、保存、发布和故障恢复都会拉长分母。提高单步算子效率只优化其中一段，不能自动消除其他停顿；应先按阶段和负责方定位时间损耗。本地只有生命周期状态诊断，不能据此推算生产集群收益。 示意：一小时中20分钟训练新数据，40分钟反复编译和恢复，即使训练时GPU很忙，ETT仍只有约三分之一；应先减少生命周期损耗。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-effective-training-time-8fded34e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2a1f5892e23650ba">GPU已经满负荷运行，为什么Effective Training Time仍可能很低？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aeffective-training-time">Optimizing Effective Training Time for Large-Scale Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Platforms, Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>ETT关注总生命周期里真正用于消费新数据的训练时间占比，初始化、编译、保存、发布和故障恢复都会拉长分母。提高单步算子效率只优化其中一段，不能自动消除其他停顿；应先按阶段和负责方定位时间损耗。本地只有生命周期状态诊断，不能据此推算生产集群收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一小时中20分钟训练新数据，40分钟反复编译和恢复，即使训练时GPU很忙，ETT仍只有约三分之一；应先减少生命周期损耗。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02057">原论文</a> · <a href="../../../../reproductions/2610.02057-effective-training-time/">实现解读</a> · <a href="#qa-2a1f5892e23650ba">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:effective-training-time" data-paper-title="Optimizing Effective Training Time for Large-Scale Recommendation Systems" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Optimizing Effective Training Time for Large-Scale Recommendation Systems 搜广推与 LLM 应用 Meta Platforms, Inc. 2026-10-01 把端到端 wall time 分为真正消费新数据的训练时间与初始化、编译、checkpoint、发布和恢复等生命周期损耗，再按 owner 定位和优化。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 ETT 分解与 owner loss 归因；这是用户批准的生产基础设施例外，不声称推荐模型效果或线上 A/B 收益。收录例外：用户于 2026-10-02 明确批准的生产训练基础设施例外；部署指标是 ETT，不作为推荐模型效果或线上 A/B 收益。执行 ETT 分解与 owner loss 归因；这是用户批准的生产基础设施例外，不声称推荐模型效果或线上 A/B 收益。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  training-systems effective-training-time gpu-fleet 搜广推 自动研究与高效上线 ETT 如何利用阶段分解决定先优化编译、恢复还是训练算子？ 先把总时长分为新数据训练及各项生命周期损耗，再按可减少规模与负责方定位。若训练只占少数，继续优化算子未必最有价值；若生命周期开销已低，训练效率才是主要瓶颈。分解服务于实际进展，不把所有 GPU 活动都视为有效训练。 示意：一小时训练十分钟、恢复三十分钟，提速算子一成只能省少量时间；少一次恢复反而可能显著增加消费新数据的时间。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-aef5009086049e42">ETT 如何利用阶段分解决定先优化编译、恢复还是训练算子？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aeffective-training-time">Optimizing Effective Training Time for Large-Scale Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Platforms, Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>先把总时长分为新数据训练及各项生命周期损耗，再按可减少规模与负责方定位。若训练只占少数，继续优化算子未必最有价值；若生命周期开销已低，训练效率才是主要瓶颈。分解服务于实际进展，不把所有 GPU 活动都视为有效训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一小时训练十分钟、恢复三十分钟，提速算子一成只能省少量时间；少一次恢复反而可能显著增加消费新数据的时间。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02057">原论文</a> · <a href="../../../../reproductions/2610.02057-effective-training-time/">实现解读</a> · <a href="#qa-aef5009086049e42">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:effective-training-time" data-paper-title="Optimizing Effective Training Time for Large-Scale Recommendation Systems" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Optimizing Effective Training Time for Large-Scale Recommendation Systems 搜广推与 LLM 应用 Meta Platforms, Inc. 2026-10-01 把端到端 wall time 分为真正消费新数据的训练时间与初始化、编译、checkpoint、发布和恢复等生命周期损耗，再按 owner 定位和优化。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 ETT 分解与 owner loss 归因；这是用户批准的生产基础设施例外，不声称推荐模型效果或线上 A/B 收益。收录例外：用户于 2026-10-02 明确批准的生产训练基础设施例外；部署指标是 ETT，不作为推荐模型效果或线上 A/B 收益。执行 ETT 分解与 owner loss 归因；这是用户批准的生产基础设施例外，不声称推荐模型效果或线上 A/B 收益。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  training-systems effective-training-time gpu-fleet 搜广推 自动研究与高效上线 ETT 与稳定训练段 samples/s 或 MFU，为什么可能导出不同优化优先级？ 吞吐衡量单位训练时间速度，MFU 衡量算力使用，ETT 关注端到端生命周期的新数据训练占比。更快 kernel 若带来更多编译或重启，前两者可上升而整日新数据进展变差。三个指标互补，不能拿任一个自动推断另外两个。 示意：新内核每步快两成，却每天多次故障恢复；测稳定段吞吐很好看，总处理新数据反而减少，ETT 才能暴露损耗位置。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d25e0706c7f774fb">ETT 与稳定训练段 samples/s 或 MFU，为什么可能导出不同优化优先级？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aeffective-training-time">Optimizing Effective Training Time for Large-Scale Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Platforms, Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>吞吐衡量单位训练时间速度，MFU 衡量算力使用，ETT 关注端到端生命周期的新数据训练占比。更快 kernel 若带来更多编译或重启，前两者可上升而整日新数据进展变差。三个指标互补，不能拿任一个自动推断另外两个。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新内核每步快两成，却每天多次故障恢复；测稳定段吞吐很好看，总处理新数据反而减少，ETT 才能暴露损耗位置。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02057">原论文</a> · <a href="../../../../reproductions/2610.02057-effective-training-time/">实现解读</a> · <a href="#qa-d25e0706c7f774fb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:effective-training-time" data-paper-title="Optimizing Effective Training Time for Large-Scale Recommendation Systems" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Optimizing Effective Training Time for Large-Scale Recommendation Systems 搜广推与 LLM 应用 Meta Platforms, Inc. 2026-10-01 把端到端 wall time 分为真正消费新数据的训练时间与初始化、编译、checkpoint、发布和恢复等生命周期损耗，再按 owner 定位和优化。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 ETT 分解与 owner loss 归因；这是用户批准的生产基础设施例外，不声称推荐模型效果或线上 A/B 收益。收录例外：用户于 2026-10-02 明确批准的生产训练基础设施例外；部署指标是 ETT，不作为推荐模型效果或线上 A/B 收益。执行 ETT 分解与 owner loss 归因；这是用户批准的生产基础设施例外，不声称推荐模型效果或线上 A/B 收益。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  training-systems effective-training-time gpu-fleet 搜广推 自动研究与高效上线 ETT 计时为什么要明确重叠阶段与恢复重放的口径？ 分母是同一任务实际 wall time，分子只算消费新数据的训练区间；异步保存与训练重叠不能重复累加，恢复重放旧 batch 也不等于新进展。阶段归因可以重叠，但比例计算需一致。本地状态诊断不构成生产吞吐实测。 示意：保存与训练重叠五分钟，不能把一小时机械加成六十五分钟；恢复中重复旧数据也不能记为额外五分钟新数据训练。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7f33374785e1c483">ETT 计时为什么要明确重叠阶段与恢复重放的口径？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aeffective-training-time">Optimizing Effective Training Time for Large-Scale Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Platforms, Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分母是同一任务实际 wall time，分子只算消费新数据的训练区间；异步保存与训练重叠不能重复累加，恢复重放旧 batch 也不等于新进展。阶段归因可以重叠，但比例计算需一致。本地状态诊断不构成生产吞吐实测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>保存与训练重叠五分钟，不能把一小时机械加成六十五分钟；恢复中重复旧数据也不能记为额外五分钟新数据训练。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02057">原论文</a> · <a href="../../../../reproductions/2610.02057-effective-training-time/">实现解读</a> · <a href="#qa-7f33374785e1c483">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:evoskillrec" data-paper-title="EvoSkillRec: Skill-Genome Evolution for Recommender Architecture Discovery" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="EvoSkillRec: Skill-Genome Evolution for Recommender Architecture Discovery 搜广推与 LLM 应用 City University of Hong Kong 2026-09-28 把推荐网络拆成带输入输出类型的可执行 skill genome；控制器在约束空间组合技能，只有通过 validation 的创新才晋级并进入后续复用库。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 typed genome、validation evaluator、promotion 与 reuse；未调用外部 LLM 发明任意代码，也不复述论文大规模搜索收益。执行 typed genome、validation evaluator、promotion 与 reuse；未调用外部 LLM 发明任意代码，也不复述论文大规模搜索收益。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  recommendation-auto-evolution architecture-search skill-genome 搜广推 自动研究与高效上线 EvoSkillRec 为什么要求 skill 具有可执行的输入输出契约？ 自然语言技能名无法保证模块可组合，类型约束把基因组变成能运行并被统一评估的程序。兼容只是第一道检查，不说明信息语义或推荐效果正确，还需独立验证和晋级。结构合法与能力证据应始终分开。 示意：序列编码器输出向量后可接向量评分头；若下一模块要求候选集合，名称看似相关也不能直接拼，必须有明确转换。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-evoskillrec-7ef949da" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-3735285efdd844ab">EvoSkillRec 为什么要求 skill 具有可执行的输入输出契约？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aevoskillrec">EvoSkillRec: Skill-Genome Evolution for Recommender Architecture Discovery</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · City University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>自然语言技能名无法保证模块可组合，类型约束把基因组变成能运行并被统一评估的程序。兼容只是第一道检查，不说明信息语义或推荐效果正确，还需独立验证和晋级。结构合法与能力证据应始终分开。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>序列编码器输出向量后可接向量评分头；若下一模块要求候选集合，名称看似相关也不能直接拼，必须有明确转换。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34552">原论文</a> · <a href="../../../../reproductions/2609.34552-evoskillrec/">实现解读</a> · <a href="#qa-3735285efdd844ab">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:evoskillrec" data-paper-title="EvoSkillRec: Skill-Genome Evolution for Recommender Architecture Discovery" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="EvoSkillRec: Skill-Genome Evolution for Recommender Architecture Discovery 搜广推与 LLM 应用 City University of Hong Kong 2026-09-28 把推荐网络拆成带输入输出类型的可执行 skill genome；控制器在约束空间组合技能，只有通过 validation 的创新才晋级并进入后续复用库。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 typed genome、validation evaluator、promotion 与 reuse；未调用外部 LLM 发明任意代码，也不复述论文大规模搜索收益。执行 typed genome、validation evaluator、promotion 与 reuse；未调用外部 LLM 发明任意代码，也不复述论文大规模搜索收益。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  recommendation-auto-evolution architecture-search skill-genome 搜广推 自动研究与高效上线 Skill genome为什么必须检查相邻技能输入输出类型，而不能任意拼接高分模块？ 单个模块有效不代表组合后语义与形状兼容，类型合同先排除无法执行的技能链。控制器随后实际构造候选、评估validation，并只把超过晋级门槛的组合写入复用库。注册一个名称或通过类型检查都不等于完成集成；本地三种子只检查组合与状态转换，不是正式能力排名。 示意：输出item向量的技能不能直接接一个要求完整行为序列的技能；即使两者各自得分高，也要先有正确适配，再验证组合是否保留预期语义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-11fbd5c6574e563d">Skill genome为什么必须检查相邻技能输入输出类型，而不能任意拼接高分模块？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aevoskillrec">EvoSkillRec: Skill-Genome Evolution for Recommender Architecture Discovery</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · City University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单个模块有效不代表组合后语义与形状兼容，类型合同先排除无法执行的技能链。控制器随后实际构造候选、评估validation，并只把超过晋级门槛的组合写入复用库。注册一个名称或通过类型检查都不等于完成集成；本地三种子只检查组合与状态转换，不是正式能力排名。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>输出item向量的技能不能直接接一个要求完整行为序列的技能；即使两者各自得分高，也要先有正确适配，再验证组合是否保留预期语义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34552">原论文</a> · <a href="../../../../reproductions/2609.34552-evoskillrec/">实现解读</a> · <a href="#qa-11fbd5c6574e563d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:evoskillrec" data-paper-title="EvoSkillRec: Skill-Genome Evolution for Recommender Architecture Discovery" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="EvoSkillRec: Skill-Genome Evolution for Recommender Architecture Discovery 搜广推与 LLM 应用 City University of Hong Kong 2026-09-28 把推荐网络拆成带输入输出类型的可执行 skill genome；控制器在约束空间组合技能，只有通过 validation 的创新才晋级并进入后续复用库。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 typed genome、validation evaluator、promotion 与 reuse；未调用外部 LLM 发明任意代码，也不复述论文大规模搜索收益。执行 typed genome、validation evaluator、promotion 与 reuse；未调用外部 LLM 发明任意代码，也不复述论文大规模搜索收益。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  recommendation-auto-evolution architecture-search skill-genome 搜广推 自动研究与高效上线 验证晋级与立即保存所有新 skill，相比如何控制复用库质量？ 未经验证模块可能无效或有害，只有达到相对基准门槛的创新才能进入可复用库，减少噪声经验误导后续。验证门槛仍受预算与数据限制，类型通过不代表提升，也不能反复用 test 决定晋级。失败可以记录，但不该冒充已证实技能。 示意：一个形状正确模块让验证分下降，应保留失败经验而非作为默认推荐技能；否则下一代会把坏结果当成功知识继续扩散。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b51a0203ac02a2fe">验证晋级与立即保存所有新 skill，相比如何控制复用库质量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aevoskillrec">EvoSkillRec: Skill-Genome Evolution for Recommender Architecture Discovery</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · City University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>未经验证模块可能无效或有害，只有达到相对基准门槛的创新才能进入可复用库，减少噪声经验误导后续。验证门槛仍受预算与数据限制，类型通过不代表提升，也不能反复用 test 决定晋级。失败可以记录，但不该冒充已证实技能。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个形状正确模块让验证分下降，应保留失败经验而非作为默认推荐技能；否则下一代会把坏结果当成功知识继续扩散。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34552">原论文</a> · <a href="../../../../reproductions/2609.34552-evoskillrec/">实现解读</a> · <a href="#qa-b51a0203ac02a2fe">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:evoskillrec" data-paper-title="EvoSkillRec: Skill-Genome Evolution for Recommender Architecture Discovery" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="EvoSkillRec: Skill-Genome Evolution for Recommender Architecture Discovery 搜广推与 LLM 应用 City University of Hong Kong 2026-09-28 把推荐网络拆成带输入输出类型的可执行 skill genome；控制器在约束空间组合技能，只有通过 validation 的创新才晋级并进入后续复用库。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 typed genome、validation evaluator、promotion 与 reuse；未调用外部 LLM 发明任意代码，也不复述论文大规模搜索收益。执行 typed genome、validation evaluator、promotion 与 reuse；未调用外部 LLM 发明任意代码，也不复述论文大规模搜索收益。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  recommendation-auto-evolution architecture-search skill-genome 搜广推 自动研究与高效上线 技能类型检查为什么不能只比较最后一维大小？ B×d 用户向量、B×C×d 候选向量与 B×T×d 序列状态有不同角色，即使末维相同也不等价。契约要覆盖批、候选与时间语义，实际执行组合再评估。本地只验证状态转换，不能将诊断标签升级为正式能力排名。 示意：把用户向量广播成所有候选表示可能不报错，却没有候选差异；程序能跑不能证明技能组合完成了预期的用户—物品交互。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-aaaed1d71fd23064">技能类型检查为什么不能只比较最后一维大小？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aevoskillrec">EvoSkillRec: Skill-Genome Evolution for Recommender Architecture Discovery</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · City University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>B×d 用户向量、B×C×d 候选向量与 B×T×d 序列状态有不同角色，即使末维相同也不等价。契约要覆盖批、候选与时间语义，实际执行组合再评估。本地只验证状态转换，不能将诊断标签升级为正式能力排名。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把用户向量广播成所有候选表示可能不报错，却没有候选差异；程序能跑不能证明技能组合完成了预期的用户—物品交互。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34552">原论文</a> · <a href="../../../../reproductions/2609.34552-evoskillrec/">实现解读</a> · <a href="#qa-aaaed1d71fd23064">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:evopilot" data-paper-title="Verify, Don&#x27;t Trust: Agentic Model Development for Video Discovery Retrieval at Scale" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Verify, Don&#x27;t Trust: Agentic Model Development for Video Discovery Retrieval at Scale 搜广推与 LLM 应用 Meta Platforms 2026-09-18 EvoPilot 不把“某个训练任务完成”直接当成研究证据，而把控制组与实验组的匹配比较作为证据单元。协议固定 shared base、数据版本、评测器、有效输出深度和唯一允许变化的 treatment；执行结束后，从产物读取实际状态并 fail closed，最后仍需人工审核才能接纳结论。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地复现的是 EvoPilot 的比较协议与 fail-closed 验证器，并在同一 MovieLens 切分上运行匹配的交互头对照；不是 Meta VDD 生产系统复刻。公开 MovieLens 上执行比较协议、artifact attestation、fail-closed pair verifier 与 validation-only 交互头对照；不复刻 Meta VDD 私有视频日志、百亿级索引、远程工作流或线上流量。  autoresearch experiment-verification video-retrieval 搜广推 自动研究与高效上线 EvoPilot 为什么让负结果也可能通过 Verify？ Verify 检查比较协议与产物是否可靠，效果方向则是实验结论，二者不同。两臂匹配且产物完整的下降结果仍是有效证据；人工 Review 再审查解释与后续接纳。不能把成功验收误写成性能提升，也不能因负向就删掉真实结果。 示意：交互头降低命中但仅它发生变化，可接纳为有效负证据；另一实验数字上升却同时换数据，应先拒绝其归因比较。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-evopilot-795a30ed" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9c17b6bb0d1f9105">EvoPilot 为什么让负结果也可能通过 Verify？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aevopilot">Verify, Don&#x27;t Trust: Agentic Model Development for Video Discovery Retrieval at Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Platforms</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Verify 检查比较协议与产物是否可靠，效果方向则是实验结论，二者不同。两臂匹配且产物完整的下降结果仍是有效证据；人工 Review 再审查解释与后续接纳。不能把成功验收误写成性能提升，也不能因负向就删掉真实结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>交互头降低命中但仅它发生变化，可接纳为有效负证据；另一实验数字上升却同时换数据，应先拒绝其归因比较。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.21257">原论文</a> · <a href="../../../../reproductions/2609.21257-evopilot/">实现解读</a> · <a href="#qa-9c17b6bb0d1f9105">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:evopilot" data-paper-title="Verify, Don&#x27;t Trust: Agentic Model Development for Video Discovery Retrieval at Scale" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Verify, Don&#x27;t Trust: Agentic Model Development for Video Discovery Retrieval at Scale 搜广推与 LLM 应用 Meta Platforms 2026-09-18 EvoPilot 不把“某个训练任务完成”直接当成研究证据，而把控制组与实验组的匹配比较作为证据单元。协议固定 shared base、数据版本、评测器、有效输出深度和唯一允许变化的 treatment；执行结束后，从产物读取实际状态并 fail closed，最后仍需人工审核才能接纳结论。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地复现的是 EvoPilot 的比较协议与 fail-closed 验证器，并在同一 MovieLens 切分上运行匹配的交互头对照；不是 Meta VDD 生产系统复刻。公开 MovieLens 上执行比较协议、artifact attestation、fail-closed pair verifier 与 validation-only 交互头对照；不复刻 Meta VDD 私有视频日志、百亿级索引、远程工作流或线上流量。  autoresearch experiment-verification video-retrieval 搜广推 自动研究与高效上线 EvoPilot为什么把匹配的两臂比较，而不是一个成功训练任务，作为证据单元？ 单臂任务完成只能证明产物出现，无法说明提升来自哪项改动。EvoPilot固定共同基座、数据、评测器和输出深度，只允许批准的treatment不同，再从实际产物核对终态与来源；任一额外差异都会拒收。协议校验通过也可能得到负结果，它不是质量收益或上线许可的替代品。 示意：实验组换了交互层，同时多训一倍步数，即使分数更高也不能只归功于交互层；需要先恢复匹配预算，再接纳这对比较作为证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-e00f149074d02130">EvoPilot为什么把匹配的两臂比较，而不是一个成功训练任务，作为证据单元？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aevopilot">Verify, Don&#x27;t Trust: Agentic Model Development for Video Discovery Retrieval at Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Platforms</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单臂任务完成只能证明产物出现，无法说明提升来自哪项改动。EvoPilot固定共同基座、数据、评测器和输出深度，只允许批准的treatment不同，再从实际产物核对终态与来源；任一额外差异都会拒收。协议校验通过也可能得到负结果，它不是质量收益或上线许可的替代品。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>实验组换了交互层，同时多训一倍步数，即使分数更高也不能只归功于交互层；需要先恢复匹配预算，再接纳这对比较作为证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.21257">原论文</a> · <a href="../../../../reproductions/2609.21257-evopilot/">实现解读</a> · <a href="#qa-e00f149074d02130">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:evopilot" data-paper-title="Verify, Don&#x27;t Trust: Agentic Model Development for Video Discovery Retrieval at Scale" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Verify, Don&#x27;t Trust: Agentic Model Development for Video Discovery Retrieval at Scale 搜广推与 LLM 应用 Meta Platforms 2026-09-18 EvoPilot 不把“某个训练任务完成”直接当成研究证据，而把控制组与实验组的匹配比较作为证据单元。协议固定 shared base、数据版本、评测器、有效输出深度和唯一允许变化的 treatment；执行结束后，从产物读取实际状态并 fail closed，最后仍需人工审核才能接纳结论。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地复现的是 EvoPilot 的比较协议与 fail-closed 验证器，并在同一 MovieLens 切分上运行匹配的交互头对照；不是 Meta VDD 生产系统复刻。公开 MovieLens 上执行比较协议、artifact attestation、fail-closed pair verifier 与 validation-only 交互头对照；不复刻 Meta VDD 私有视频日志、百亿级索引、远程工作流或线上流量。  autoresearch experiment-verification video-retrieval 搜广推 自动研究与高效上线 匹配 treatment 与复用历史高质量 baseline，为什么不总是同一比较？ 历史 baseline 的 base、数据、评测器或输出深度可能已不同，多项变化会混淆差值。协议要求唯一批准 treatment 是实际差异，先建立同义两臂再讨论指标。更多种子只能估计波动，不能修复比较基础不匹配。 示意：新模型输出十层、历史基线只输出五层，就不再是“只换交互头”；即使训练都成功，差值也无法归给单一改动。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-482826e1007f31c0">匹配 treatment 与复用历史高质量 baseline，为什么不总是同一比较？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aevopilot">Verify, Don&#x27;t Trust: Agentic Model Development for Video Discovery Retrieval at Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Platforms</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>历史 baseline 的 base、数据、评测器或输出深度可能已不同，多项变化会混淆差值。协议要求唯一批准 treatment 是实际差异，先建立同义两臂再讨论指标。更多种子只能估计波动，不能修复比较基础不匹配。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新模型输出十层、历史基线只输出五层，就不再是“只换交互头”；即使训练都成功，差值也无法归给单一改动。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.21257">原论文</a> · <a href="../../../../reproductions/2609.21257-evopilot/">实现解读</a> · <a href="#qa-482826e1007f31c0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:evopilot" data-paper-title="Verify, Don&#x27;t Trust: Agentic Model Development for Video Discovery Retrieval at Scale" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Verify, Don&#x27;t Trust: Agentic Model Development for Video Discovery Retrieval at Scale 搜广推与 LLM 应用 Meta Platforms 2026-09-18 EvoPilot 不把“某个训练任务完成”直接当成研究证据，而把控制组与实验组的匹配比较作为证据单元。协议固定 shared base、数据版本、评测器、有效输出深度和唯一允许变化的 treatment；执行结束后，从产物读取实际状态并 fail closed，最后仍需人工审核才能接纳结论。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地复现的是 EvoPilot 的比较协议与 fail-closed 验证器，并在同一 MovieLens 切分上运行匹配的交互头对照；不是 Meta VDD 生产系统复刻。公开 MovieLens 上执行比较协议、artifact attestation、fail-closed pair verifier 与 validation-only 交互头对照；不复刻 Meta VDD 私有视频日志、百亿级索引、远程工作流或线上流量。  autoresearch experiment-verification video-retrieval 搜广推 自动研究与高效上线 EvoPilot 为什么从实际产物读终态与 provenance，而不只信调度器 success？ 任务可能部分失败、运行错配置或留下旧文件，调度状态不能证明两臂证据存在。缺终态、版本或实际差异时 fail closed，不能默认为通过。来源本地还检验输出深度不匹配会被拒绝，显示协议应检查真实执行而非声明。 示意：任务结束但指标缺失时，不能沿用上轮 JSON 来完成比较；那会把未执行的结果误当作当前证据，哪怕分数看起来合理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8d1d591c91723507">EvoPilot 为什么从实际产物读终态与 provenance，而不只信调度器 success？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aevopilot">Verify, Don&#x27;t Trust: Agentic Model Development for Video Discovery Retrieval at Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Platforms</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>任务可能部分失败、运行错配置或留下旧文件，调度状态不能证明两臂证据存在。缺终态、版本或实际差异时 fail closed，不能默认为通过。来源本地还检验输出深度不匹配会被拒绝，显示协议应检查真实执行而非声明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>任务结束但指标缺失时，不能沿用上轮 JSON 来完成比较；那会把未执行的结果误当作当前证据，哪怕分数看起来合理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.21257">原论文</a> · <a href="../../../../reproductions/2609.21257-evopilot/">实现解读</a> · <a href="#qa-8d1d591c91723507">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:autolr" data-paper-title="AutoLR: Automating the Path from Research to Launch Review in Industrial Recommender Systems" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="AutoLR: Automating the Path from Research to Launch Review in Industrial Recommender Systems 搜广推与 LLM 应用 NetEase, Inc. 2026-09-04 AutoLR 将论文调研、方案辩论、代码实验、离线评估、A/B 测试与 Launch Review 串成长期状态机。LLM 负责语义推理和代码生成，确定性控制器保留预算分配、指标抽取、护栏和状态迁移权，防止噪声结果在 KEEP 链中被不断放大。 复现级别：离线控制器核心。复现级别：离线控制器核心。对输入候选与评审执行预算排序、独立指标门槛、持久化账本和人工评审打包；不包含实时 LLM 调研、自动代码生成或线上发布。论文生产代码与 DASHEN 数据未公开；模型只能选择白名单参数，不能注入命令或任意代码。当前实现是受控的离线自动研究闭环，不声称自主创新架构或具备自动发布权限。真实 Qwen checkpoint 已在公开 Amazon Beauty 2014 5-core 上完成三轮有界研究：每轮动态生成参数提案，分别调用两个 reviewer，再执行一轮真实反向传播验证和完整 validation 训练。  auto-research experiment-controller launch-review industrial-recommendation 搜广推 自动研究与高效上线 AutoLR 的长期研究状态机为什么要区分离线评估、真实 A/B 与 Launch Review？ 离线结果只说明特定数据协议下的表现，真实用户影响与上线资源约束需要另外验证。状态机将提案、实验、审查和晋级分开，让证据逐级增加，并把失败与预算写入长期状态。LLM 可以推理和写代码，不能用一句“有提升”跳过后续权限与证据。 示意：一个优化器在验证集更好但内存超预算，应停在离线阶段；另一个经过真实实验才有资格进入发布审查，而不是自动成为线上冠军。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-autolr-f0e06ba6" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-44f52b6cb732a632">AutoLR 的长期研究状态机为什么要区分离线评估、真实 A/B 与 Launch Review？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aautolr">AutoLR: Automating the Path from Research to Launch Review in Industrial Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NetEase, Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>离线结果只说明特定数据协议下的表现，真实用户影响与上线资源约束需要另外验证。状态机将提案、实验、审查和晋级分开，让证据逐级增加，并把失败与预算写入长期状态。LLM 可以推理和写代码，不能用一句“有提升”跳过后续权限与证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个优化器在验证集更好但内存超预算，应停在离线阶段；另一个经过真实实验才有资格进入发布审查，而不是自动成为线上冠军。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04871">原论文</a> · <a href="../../../../reproductions/2609.04871-autolr/">实现解读</a> · <a href="#qa-44f52b6cb732a632">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:autolr" data-paper-title="AutoLR: Automating the Path from Research to Launch Review in Industrial Recommender Systems" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="AutoLR: Automating the Path from Research to Launch Review in Industrial Recommender Systems 搜广推与 LLM 应用 NetEase, Inc. 2026-09-04 AutoLR 将论文调研、方案辩论、代码实验、离线评估、A/B 测试与 Launch Review 串成长期状态机。LLM 负责语义推理和代码生成，确定性控制器保留预算分配、指标抽取、护栏和状态迁移权，防止噪声结果在 KEEP 链中被不断放大。 复现级别：离线控制器核心。复现级别：离线控制器核心。对输入候选与评审执行预算排序、独立指标门槛、持久化账本和人工评审打包；不包含实时 LLM 调研、自动代码生成或线上发布。论文生产代码与 DASHEN 数据未公开；模型只能选择白名单参数，不能注入命令或任意代码。当前实现是受控的离线自动研究闭环，不声称自主创新架构或具备自动发布权限。真实 Qwen checkpoint 已在公开 Amazon Beauty 2014 5-core 上完成三轮有界研究：每轮动态生成参数提案，分别调用两个 reviewer，再执行一轮真实反向传播验证和完整 validation 训练。  auto-research experiment-controller launch-review industrial-recommendation 搜广推 自动研究与高效上线 AutoLR为什么不让LLM直接把自认为最好的方案写成长期冠军？ 提案和讨论含有噪声，若每轮凭语言判断KEEP，错误会沿持久状态累积。AutoLR把语义推理交给LLM，却把预算、指标提取、护栏与状态迁移留给确定性控制器；只有通过对应实验门槛的证据才能更新冠军。一次代理指标胜出也不能绕过后续A/B与Launch Review。 示意：模型建议一种新优化器，但离线收益不稳定；控制器记录提案和失败而保留旧冠军，避免下轮把未验证方案当成已经成立的基线。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-366e4daee96ef43b">AutoLR为什么不让LLM直接把自认为最好的方案写成长期冠军？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aautolr">AutoLR: Automating the Path from Research to Launch Review in Industrial Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NetEase, Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>提案和讨论含有噪声，若每轮凭语言判断KEEP，错误会沿持久状态累积。AutoLR把语义推理交给LLM，却把预算、指标提取、护栏与状态迁移留给确定性控制器；只有通过对应实验门槛的证据才能更新冠军。一次代理指标胜出也不能绕过后续A/B与Launch Review。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型建议一种新优化器，但离线收益不稳定；控制器记录提案和失败而保留旧冠军，避免下轮把未验证方案当成已经成立的基线。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04871">原论文</a> · <a href="../../../../reproductions/2609.04871-autolr/">实现解读</a> · <a href="#qa-366e4daee96ef43b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:autolr" data-paper-title="AutoLR: Automating the Path from Research to Launch Review in Industrial Recommender Systems" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="AutoLR: Automating the Path from Research to Launch Review in Industrial Recommender Systems 搜广推与 LLM 应用 NetEase, Inc. 2026-09-04 AutoLR 将论文调研、方案辩论、代码实验、离线评估、A/B 测试与 Launch Review 串成长期状态机。LLM 负责语义推理和代码生成，确定性控制器保留预算分配、指标抽取、护栏和状态迁移权，防止噪声结果在 KEEP 链中被不断放大。 复现级别：离线控制器核心。复现级别：离线控制器核心。对输入候选与评审执行预算排序、独立指标门槛、持久化账本和人工评审打包；不包含实时 LLM 调研、自动代码生成或线上发布。论文生产代码与 DASHEN 数据未公开；模型只能选择白名单参数，不能注入命令或任意代码。当前实现是受控的离线自动研究闭环，不声称自主创新架构或具备自动发布权限。真实 Qwen checkpoint 已在公开 Amazon Beauty 2014 5-core 上完成三轮有界研究：每轮动态生成参数提案，分别调用两个 reviewer，再执行一轮真实反向传播验证和完整 validation 训练。  auto-research experiment-controller launch-review industrial-recommendation 搜广推 自动研究与高效上线 AutoLR 的分歧惩罚与总选最有探索价值的候选相比，改变了什么预算取舍？ 仅按探索价值选会偏向未知且高风险的想法，已有证据、探索不确定性和专家分歧同时入分，给风险冲突明确代价。分歧不等于错误，但要求更多证据或较低预算优先级。本地三轮没有胜过基线，也允许保持原冠军，避免把持续研究误解为必须持续报正增益。 示意：两个候选同样新颖，一个审查者均认可，另一个对保真存在严重争议；预算有限时可先测前者，后者先补证据而不是仅因未知就优先。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-abf2dd6ec5a95be2">AutoLR 的分歧惩罚与总选最有探索价值的候选相比，改变了什么预算取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aautolr">AutoLR: Automating the Path from Research to Launch Review in Industrial Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NetEase, Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>仅按探索价值选会偏向未知且高风险的想法，已有证据、探索不确定性和专家分歧同时入分，给风险冲突明确代价。分歧不等于错误，但要求更多证据或较低预算优先级。本地三轮没有胜过基线，也允许保持原冠军，避免把持续研究误解为必须持续报正增益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个候选同样新颖，一个审查者均认可，另一个对保真存在严重争议；预算有限时可先测前者，后者先补证据而不是仅因未知就优先。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04871">原论文</a> · <a href="../../../../reproductions/2609.04871-autolr/">实现解读</a> · <a href="#qa-abf2dd6ec5a95be2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:autolr" data-paper-title="AutoLR: Automating the Path from Research to Launch Review in Industrial Recommender Systems" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="AutoLR: Automating the Path from Research to Launch Review in Industrial Recommender Systems 搜广推与 LLM 应用 NetEase, Inc. 2026-09-04 AutoLR 将论文调研、方案辩论、代码实验、离线评估、A/B 测试与 Launch Review 串成长期状态机。LLM 负责语义推理和代码生成，确定性控制器保留预算分配、指标抽取、护栏和状态迁移权，防止噪声结果在 KEEP 链中被不断放大。 复现级别：离线控制器核心。复现级别：离线控制器核心。对输入候选与评审执行预算排序、独立指标门槛、持久化账本和人工评审打包；不包含实时 LLM 调研、自动代码生成或线上发布。论文生产代码与 DASHEN 数据未公开；模型只能选择白名单参数，不能注入命令或任意代码。当前实现是受控的离线自动研究闭环，不声称自主创新架构或具备自动发布权限。真实 Qwen checkpoint 已在公开 Amazon Beauty 2014 5-core 上完成三轮有界研究：每轮动态生成参数提案，分别调用两个 reviewer，再执行一轮真实反向传播验证和完整 validation 训练。  auto-research experiment-controller launch-review industrial-recommendation 搜广推 自动研究与高效上线 本地 AutoLR 在恢复磁盘账本后，怎样防止历史 test 结果影响下一轮晋级？ 来源让提案读取研究证据与已执行 validation 账本，先做一步真实反向传播检查，再用固定预算训练，最终 test 只在选择后运行一次。恢复应保留候选、审查与验证状态，且 online_authorized 始终为 false；不能从账本中把测试表现变成选择奖励。 示意：程序中断后继续读取前两轮验证记录，第三轮无需重跑；最终测试即使发现退化，也只如实报告，而不把测试分写回提案提示再重选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-47ac2230b7116bba">本地 AutoLR 在恢复磁盘账本后，怎样防止历史 test 结果影响下一轮晋级？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aautolr">AutoLR: Automating the Path from Research to Launch Review in Industrial Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NetEase, Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>来源让提案读取研究证据与已执行 validation 账本，先做一步真实反向传播检查，再用固定预算训练，最终 test 只在选择后运行一次。恢复应保留候选、审查与验证状态，且 online_authorized 始终为 false；不能从账本中把测试表现变成选择奖励。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>程序中断后继续读取前两轮验证记录，第三轮无需重跑；最终测试即使发现退化，也只如实报告，而不把测试分写回提案提示再重选。</p>
<p class="ar-learning-sources">依据：本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04871">原论文</a> · <a href="../../../../reproductions/2609.04871-autolr/">实现解读</a> · <a href="#qa-47ac2230b7116bba">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:coral" data-paper-title="CORAL: An LLM-Native Harness for Production Recommender Systems" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="CORAL: An LLM-Native Harness for Production Recommender Systems 搜广推与 LLM 应用 Meta AI 2026-09-02 CORAL 把推荐优化建模为连续闭环：LLM 根据目标、预算和最近实验记忆生成结构化配置，执行系统验证约束并运行实验，再把观测结果写回下一轮上下文。与一次性自动调参相比，它强调可执行约束、短记忆和生产反馈。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。实现有预算约束的配置提案、短期实验记忆、效果反馈与下一轮更新。未接入 Meta 私有遥测、生产 LLM、实验平台或线上流量；实现可作为推荐 Evolve 的控制器算子组合使用。在 MovieLens 100K 上执行五轮预算分配、三轮记忆和 validation-only blend；三 seed 产物见 metrics/public-seeds42-44.json。该结果只验证控制器闭环和约束可执行性，不把公开小数据效果等同于 Meta 线上因果增益。  auto-research agent retrieval-budget constrained-optimization 搜广推 自动研究与高效上线 CORAL 的结构化配置为什么必须带目标和预算，而不是让 LLM 自由写优化建议？ 可执行配置要能交给系统验证、运行和比较，预算定义允许哪些资源分配，目标定义观测如何反馈。自由建议可能无法执行或超出服务限制，结构化接口把推理接到真实实验闭环。控制器成功运行仍不意味着获得生产因果收益。 示意：建议“多给召回算力”不够，配置需明确给哪个通道多少预算；总预算不足时系统应调整或拒绝，而不是把文字建议当作已完成优化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-coral-3b3ed34a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c6fbfac3347e3e68">CORAL 的结构化配置为什么必须带目标和预算，而不是让 LLM 自由写优化建议？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acoral">CORAL: An LLM-Native Harness for Production Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>可执行配置要能交给系统验证、运行和比较，预算定义允许哪些资源分配，目标定义观测如何反馈。自由建议可能无法执行或超出服务限制，结构化接口把推理接到真实实验闭环。控制器成功运行仍不意味着获得生产因果收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>建议“多给召回算力”不够，配置需明确给哪个通道多少预算；总预算不足时系统应调整或拒绝，而不是把文字建议当作已完成优化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.02730">原论文</a> · <a href="../../../../reproductions/2609.02730-coral/">实现解读</a> · <a href="#qa-c6fbfac3347e3e68">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:coral" data-paper-title="CORAL: An LLM-Native Harness for Production Recommender Systems" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="CORAL: An LLM-Native Harness for Production Recommender Systems 搜广推与 LLM 应用 Meta AI 2026-09-02 CORAL 把推荐优化建模为连续闭环：LLM 根据目标、预算和最近实验记忆生成结构化配置，执行系统验证约束并运行实验，再把观测结果写回下一轮上下文。与一次性自动调参相比，它强调可执行约束、短记忆和生产反馈。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。实现有预算约束的配置提案、短期实验记忆、效果反馈与下一轮更新。未接入 Meta 私有遥测、生产 LLM、实验平台或线上流量；实现可作为推荐 Evolve 的控制器算子组合使用。在 MovieLens 100K 上执行五轮预算分配、三轮记忆和 validation-only blend；三 seed 产物见 metrics/public-seeds42-44.json。该结果只验证控制器闭环和约束可执行性，不把公开小数据效果等同于 Meta 线上因果增益。  auto-research agent retrieval-budget constrained-optimization 搜广推 自动研究与高效上线 CORAL为什么把配置投影到预算可行域，并只保留最近几轮实验记忆？ 语言模型可能提出超配额或负数预算，投影先让配置成为可执行候选，再用真实实验反馈修正下一轮。有限近期记忆帮助适应系统变化，避免旧结论无限堆积干扰决策。记忆短不代表可以丢掉可审计历史，且提案经预算修正后仍需验证，不能把可行性误当成质量提升。 示意：模型把三路召回预算都加大，合计超过请求上限；先重新分配到允许总量，再运行实验。若近期流量分布变了，旧的最优配方也不应自动占优。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-89bd6b73ca40a757">CORAL为什么把配置投影到预算可行域，并只保留最近几轮实验记忆？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acoral">CORAL: An LLM-Native Harness for Production Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语言模型可能提出超配额或负数预算，投影先让配置成为可执行候选，再用真实实验反馈修正下一轮。有限近期记忆帮助适应系统变化，避免旧结论无限堆积干扰决策。记忆短不代表可以丢掉可审计历史，且提案经预算修正后仍需验证，不能把可行性误当成质量提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型把三路召回预算都加大，合计超过请求上限；先重新分配到允许总量，再运行实验。若近期流量分布变了，旧的最优配方也不应自动占优。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.02730">原论文</a> · <a href="../../../../reproductions/2609.02730-coral/">实现解读</a> · <a href="#qa-89bd6b73ca40a757">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:coral" data-paper-title="CORAL: An LLM-Native Harness for Production Recommender Systems" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="CORAL: An LLM-Native Harness for Production Recommender Systems 搜广推与 LLM 应用 Meta AI 2026-09-02 CORAL 把推荐优化建模为连续闭环：LLM 根据目标、预算和最近实验记忆生成结构化配置，执行系统验证约束并运行实验，再把观测结果写回下一轮上下文。与一次性自动调参相比，它强调可执行约束、短记忆和生产反馈。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。实现有预算约束的配置提案、短期实验记忆、效果反馈与下一轮更新。未接入 Meta 私有遥测、生产 LLM、实验平台或线上流量；实现可作为推荐 Evolve 的控制器算子组合使用。在 MovieLens 100K 上执行五轮预算分配、三轮记忆和 validation-only blend；三 seed 产物见 metrics/public-seeds42-44.json。该结果只验证控制器闭环和约束可执行性，不把公开小数据效果等同于 Meta 线上因果增益。  auto-research agent retrieval-budget constrained-optimization 搜广推 自动研究与高效上线 CORAL 的短记忆闭环与保留全部历史最佳配置，分别适合什么变化假设？ 短记忆更重视近期反馈，减少陈旧实验主导当前决策；全历史最佳依赖环境相对稳定，可能对过去高分过度执着。CORAL 通过最近观测持续更新并投影约束，代价是可能遗忘有用长期经验。两者机制取舍不能由来源小数据的单次分数判定普遍优劣。 示意：节日期间最佳广告配比未必适合节后，近期反馈应有更大影响；但过短记忆也可能忘掉之前发现的安全边界，仍需独立规则保留。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b9b80dc33e148828">CORAL 的短记忆闭环与保留全部历史最佳配置，分别适合什么变化假设？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acoral">CORAL: An LLM-Native Harness for Production Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>短记忆更重视近期反馈，减少陈旧实验主导当前决策；全历史最佳依赖环境相对稳定，可能对过去高分过度执着。CORAL 通过最近观测持续更新并投影约束，代价是可能遗忘有用长期经验。两者机制取舍不能由来源小数据的单次分数判定普遍优劣。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>节日期间最佳广告配比未必适合节后，近期反馈应有更大影响；但过短记忆也可能忘掉之前发现的安全边界，仍需独立规则保留。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.02730">原论文</a> · <a href="../../../../reproductions/2609.02730-coral/">实现解读</a> · <a href="#qa-b9b80dc33e148828">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:coral" data-paper-title="CORAL: An LLM-Native Harness for Production Recommender Systems" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="CORAL: An LLM-Native Harness for Production Recommender Systems 搜广推与 LLM 应用 Meta AI 2026-09-02 CORAL 把推荐优化建模为连续闭环：LLM 根据目标、预算和最近实验记忆生成结构化配置，执行系统验证约束并运行实验，再把观测结果写回下一轮上下文。与一次性自动调参相比，它强调可执行约束、短记忆和生产反馈。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。实现有预算约束的配置提案、短期实验记忆、效果反馈与下一轮更新。未接入 Meta 私有遥测、生产 LLM、实验平台或线上流量；实现可作为推荐 Evolve 的控制器算子组合使用。在 MovieLens 100K 上执行五轮预算分配、三轮记忆和 validation-only blend；三 seed 产物见 metrics/public-seeds42-44.json。该结果只验证控制器闭环和约束可执行性，不把公开小数据效果等同于 Meta 线上因果增益。  auto-research agent retrieval-budget constrained-optimization 搜广推 自动研究与高效上线 CORAL 将配置投影到非负且总和不超预算的集合，为什么不只逐项裁剪？ 逐项非负仅修复负值，不能保证总和满足 B，联合投影同时处理耦合预算条件。执行后的实际配置与观测应成对写回，而不是把原始超预算提案记为已运行。来源本地五轮流程只支持约束和反馈循环的可执行性。 示意：三个通道各提议六份资源，单项都合法但总和十八超过十；需要整体调整并记录真实分配，否则下一轮会基于从未执行的方案推理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-80652d133f4a6d24">CORAL 将配置投影到非负且总和不超预算的集合，为什么不只逐项裁剪？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acoral">CORAL: An LLM-Native Harness for Production Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>逐项非负仅修复负值，不能保证总和满足 B，联合投影同时处理耦合预算条件。执行后的实际配置与观测应成对写回，而不是把原始超预算提案记为已运行。来源本地五轮流程只支持约束和反馈循环的可执行性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三个通道各提议六份资源，单项都合法但总和十八超过十；需要整体调整并记录真实分配，否则下一轮会基于从未执行的方案推理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.02730">原论文</a> · <a href="../../../../reproductions/2609.02730-coral/">实现解读</a> · <a href="#qa-80652d133f4a6d24">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recharness" data-paper-title="RecHarness: A Bandit-Routed Agentic Harness for Self-Evolving Recommender Systems" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="RecHarness: A Bandit-Routed Agentic Harness for Self-Evolving Recommender Systems 搜广推与 LLM 应用 Huazhong Agricultural University (Kuaishou internship) 2026-07-31 将结构改造定义为有限 arm，用 bandit 根据历史收益和不确定性分配试验预算，再把胜者反馈写回下一轮候选。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  auto-research bandit ranking 搜广推 自动研究与高效上线 RecHarness 为什么将架构修改离散为有限 arm？ 明确候选动作便于统计每类改造的收益与不确定性，在有限预算内安排下一次实验，反馈再影响后续候选。它管理实验资源而非直接推荐物品。预设 arm 也限制创新范围，不能因为用了 bandit 就宣称自动探索任意网络。 示意：加宽、换门控、增加内容分支各为一类 arm，系统根据已有验证安排试验；它并没有从零生成无限种未知代码结构。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-recharness-7341e5ce" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-51f56bee15d21b4e">RecHarness 为什么将架构修改离散为有限 arm？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecharness">RecHarness: A Bandit-Routed Agentic Harness for Self-Evolving Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huazhong Agricultural University (Kuaishou internship)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>明确候选动作便于统计每类改造的收益与不确定性，在有限预算内安排下一次实验，反馈再影响后续候选。它管理实验资源而非直接推荐物品。预设 arm 也限制创新范围，不能因为用了 bandit 就宣称自动探索任意网络。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>加宽、换门控、增加内容分支各为一类 arm，系统根据已有验证安排试验；它并没有从零生成无限种未知代码结构。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.29241">原论文</a> · <a href="../../../../reproductions/2607.29241-recharness/">实现解读</a> · <a href="#qa-51f56bee15d21b4e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recharness" data-paper-title="RecHarness: A Bandit-Routed Agentic Harness for Self-Evolving Recommender Systems" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="RecHarness: A Bandit-Routed Agentic Harness for Self-Evolving Recommender Systems 搜广推与 LLM 应用 Huazhong Agricultural University (Kuaishou internship) 2026-07-31 将结构改造定义为有限 arm，用 bandit 根据历史收益和不确定性分配试验预算，再把胜者反馈写回下一轮候选。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  auto-research bandit ranking 搜广推 自动研究与高效上线 RecHarness 的 bandit 为什么同时看历史收益与不确定性分配实验，而不总选当前最好结构？ 总选当前平均收益最高的结构会过早放弃样本少但可能更好的方向。置信上界在估计收益上加入与试验次数有关的探索项，让不确定 arm 获得预算，再把胜者反馈用于后续候选。它优化的是有限实验资源分配，不保证找到全局最优架构；收益估计也必须遵守相同验证协议。 示意：结构甲已测十次、均值略高，结构乙只测一次。bandit 可给乙额外机会确认潜力，而不是永远重复甲；但最后仍应在独立测试集评估选中的结构。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-1259497038b725b8">RecHarness 的 bandit 为什么同时看历史收益与不确定性分配实验，而不总选当前最好结构？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecharness">RecHarness: A Bandit-Routed Agentic Harness for Self-Evolving Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huazhong Agricultural University (Kuaishou internship)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>总选当前平均收益最高的结构会过早放弃样本少但可能更好的方向。置信上界在估计收益上加入与试验次数有关的探索项，让不确定 arm 获得预算，再把胜者反馈用于后续候选。它优化的是有限实验资源分配，不保证找到全局最优架构；收益估计也必须遵守相同验证协议。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>结构甲已测十次、均值略高，结构乙只测一次。bandit 可给乙额外机会确认潜力，而不是永远重复甲；但最后仍应在独立测试集评估选中的结构。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.29241">原论文</a> · <a href="../../../../reproductions/2607.29241-recharness/">实现解读</a> · <a href="#qa-1259497038b725b8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recharness" data-paper-title="RecHarness: A Bandit-Routed Agentic Harness for Self-Evolving Recommender Systems" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="RecHarness: A Bandit-Routed Agentic Harness for Self-Evolving Recommender Systems 搜广推与 LLM 应用 Huazhong Agricultural University (Kuaishou internship) 2026-07-31 将结构改造定义为有限 arm，用 bandit 根据历史收益和不确定性分配试验预算，再把胜者反馈写回下一轮候选。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  auto-research bandit ranking 搜广推 自动研究与高效上线 UCB 选择与轮询每个结构同样次数，相比适合哪种收益分布？ 轮询均匀投入，UCB 将更多预算给高均值或尚不确定方向，减少反复测明显差项。收益非平稳或评估噪声不一致会影响估计，不能把一次偶然高分当长期最优。探索项也不修复不公平基线和数据泄漏。 示意：某结构连续五次退化，均匀轮询仍继续花预算；UCB 可少测它，多给潜力结构，但需要保留足够探索避免早早错杀。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d0deb0712d9b51f7">UCB 选择与轮询每个结构同样次数，相比适合哪种收益分布？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecharness">RecHarness: A Bandit-Routed Agentic Harness for Self-Evolving Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huazhong Agricultural University (Kuaishou internship)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>轮询均匀投入，UCB 将更多预算给高均值或尚不确定方向，减少反复测明显差项。收益非平稳或评估噪声不一致会影响估计，不能把一次偶然高分当长期最优。探索项也不修复不公平基线和数据泄漏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某结构连续五次退化，均匀轮询仍继续花预算；UCB 可少测它，多给潜力结构，但需要保留足够探索避免早早错杀。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.29241">原论文</a> · <a href="../../../../reproductions/2607.29241-recharness/">实现解读</a> · <a href="#qa-d0deb0712d9b51f7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recharness" data-paper-title="RecHarness: A Bandit-Routed Agentic Harness for Self-Evolving Recommender Systems" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="RecHarness: A Bandit-Routed Agentic Harness for Self-Evolving Recommender Systems 搜广推与 LLM 应用 Huazhong Agricultural University (Kuaishou internship) 2026-07-31 将结构改造定义为有限 arm，用 bandit 根据历史收益和不确定性分配试验预算，再把胜者反馈写回下一轮候选。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  auto-research bandit ranking 搜广推 自动研究与高效上线 RecHarness 的 na=0 与多轮账本，应如何避免除零和虚构已试次数？ 未试 arm 应按约定优先初始化或使用明确无限探索值，不能直接代入零分母；次数只在真实实验完成后增加，收益来自固定验证协议。中断恢复需保留真实状态，不能提交任务就算拿到反馈。来源小代理不证明生产研究吞吐。 示意：训练任务失败没产生验证结果，应记录失败而非给该 arm 加一个零收益或成功次数，否则后续不确定性估计会被伪数据影响。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-853a202b59350215">RecHarness 的 na=0 与多轮账本，应如何避免除零和虚构已试次数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecharness">RecHarness: A Bandit-Routed Agentic Harness for Self-Evolving Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huazhong Agricultural University (Kuaishou internship)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>未试 arm 应按约定优先初始化或使用明确无限探索值，不能直接代入零分母；次数只在真实实验完成后增加，收益来自固定验证协议。中断恢复需保留真实状态，不能提交任务就算拿到反馈。来源小代理不证明生产研究吞吐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练任务失败没产生验证结果，应记录失败而非给该 arm 加一个零收益或成功次数，否则后续不确定性估计会被伪数据影响。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.29241">原论文</a> · <a href="../../../../reproductions/2607.29241-recharness/">实现解读</a> · <a href="#qa-853a202b59350215">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rocs" data-paper-title="ROCS: Request-Oriented Compute Sharing for Efficient Large-Scale Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="ROCS: Request-Oriented Compute Sharing for Efficient Large-Scale Recommendation 搜广推与 LLM 应用 Meta AI 2026-07-30 一次推荐请求会评分大量候选，而用户侧特征完全相同。ROCS 通过 Generalized Layer Masking 保持候选隔离，用 Deep Cross Attention 延迟交互，再由 IKBO 在 GPU kernel 内广播 request 表示。 Fidelity: 核心机制复现。实现一次 request encoding、延迟 candidate interaction 和批量候选评分。未复刻生产 GLM、IKBO CUDA kernel、Meta 私有模型与集群。本地对照口径：基线为逐候选重复编码；实验组为 ROCS core，相对基线 NDCG@10 +8.19%。  retrieval ranking serving compute-sharing 搜广推 自动研究与高效上线 ROCS为什么把request侧表示共享一次？ 同一推荐请求会评大量候选，用户侧输入重复，提前共享编码可减少冗余计算；候选通过延迟交互获得各自分数。共享不是取消所有用户物品交互。 例如同一用户给上千视频打分，不必重复算上千遍完全一样的请求特征。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-rocs-28113d9d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-90441741441e8286">ROCS为什么把request侧表示共享一次？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arocs">ROCS: Request-Oriented Compute Sharing for Efficient Large-Scale Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一推荐请求会评大量候选，用户侧输入重复，提前共享编码可减少冗余计算；候选通过延迟交互获得各自分数。共享不是取消所有用户物品交互。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一用户给上千视频打分，不必重复算上千遍完全一样的请求特征。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27744">原论文</a> · <a href="../../../../reproductions/2607.27744-rocs/">实现解读</a> · <a href="#qa-90441741441e8286">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rocs" data-paper-title="ROCS: Request-Oriented Compute Sharing for Efficient Large-Scale Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="ROCS: Request-Oriented Compute Sharing for Efficient Large-Scale Recommendation 搜广推与 LLM 应用 Meta AI 2026-07-30 一次推荐请求会评分大量候选，而用户侧特征完全相同。ROCS 通过 Generalized Layer Masking 保持候选隔离，用 Deep Cross Attention 延迟交互，再由 IKBO 在 GPU kernel 内广播 request 表示。 Fidelity: 核心机制复现。实现一次 request encoding、延迟 candidate interaction 和批量候选评分。未复刻生产 GLM、IKBO CUDA kernel、Meta 私有模型与集群。本地对照口径：基线为逐候选重复编码；实验组为 ROCS core，相对基线 NDCG@10 +8.19%。  retrieval ranking serving compute-sharing 搜广推 自动研究与高效上线 ROCS 为什么需要候选隔离掩码，才能安全地把用户侧计算从逐候选重复中拿出来？ 若用户状态在某层已读取某个候选，就不能作为其他候选通用的缓存。Generalized Layer Masking 约束信息流保持隔离，Deep Cross Attention 延后候选交互，才允许请求表示只算一次。内核广播进一步减少复制成本；本地进程内微基准只反映重复编码与共享的路径差异，不能冒充完整生产吞吐提升。 示意：同一用户评一百件商品，用户主干先保持候选无关，再广播给各商品分支。若商品甲先写进用户表示，商品乙再复用它，得分就会被不该看到的候选污染。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-a037f568e876e729">ROCS 为什么需要候选隔离掩码，才能安全地把用户侧计算从逐候选重复中拿出来？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arocs">ROCS: Request-Oriented Compute Sharing for Efficient Large-Scale Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若用户状态在某层已读取某个候选，就不能作为其他候选通用的缓存。Generalized Layer Masking 约束信息流保持隔离，Deep Cross Attention 延后候选交互，才允许请求表示只算一次。内核广播进一步减少复制成本；本地进程内微基准只反映重复编码与共享的路径差异，不能冒充完整生产吞吐提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一用户评一百件商品，用户主干先保持候选无关，再广播给各商品分支。若商品甲先写进用户表示，商品乙再复用它，得分就会被不该看到的候选污染。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27744">原论文</a> · <a href="../../../../reproductions/2607.27744-rocs/">实现解读</a> · <a href="#qa-a037f568e876e729">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rocs" data-paper-title="ROCS: Request-Oriented Compute Sharing for Efficient Large-Scale Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="ROCS: Request-Oriented Compute Sharing for Efficient Large-Scale Recommendation 搜广推与 LLM 应用 Meta AI 2026-07-30 一次推荐请求会评分大量候选，而用户侧特征完全相同。ROCS 通过 Generalized Layer Masking 保持候选隔离，用 Deep Cross Attention 延迟交互，再由 IKBO 在 GPU kernel 内广播 request 表示。 Fidelity: 核心机制复现。实现一次 request encoding、延迟 candidate interaction 和批量候选评分。未复刻生产 GLM、IKBO CUDA kernel、Meta 私有模型与集群。本地对照口径：基线为逐候选重复编码；实验组为 ROCS core，相对基线 NDCG@10 +8.19%。  retrieval ranking serving compute-sharing 搜广推 自动研究与高效上线 ROCS候选隔离与把所有候选放同一自注意力有何不同？ 隔离防止一个候选读到其他候选导致分数互相依赖，同时允许读取共享请求。任意全交互会改变模型语义，不能只靠缓存用户向量声称实现原mask机制。 例如新增视频不应无意改掉原候选的内部表示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a7629b435887d373">ROCS候选隔离与把所有候选放同一自注意力有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arocs">ROCS: Request-Oriented Compute Sharing for Efficient Large-Scale Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>隔离防止一个候选读到其他候选导致分数互相依赖，同时允许读取共享请求。任意全交互会改变模型语义，不能只靠缓存用户向量声称实现原mask机制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如新增视频不应无意改掉原候选的内部表示。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27744">原论文</a> · <a href="../../../../reproductions/2607.27744-rocs/">实现解读</a> · <a href="#qa-a7629b435887d373">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rocs" data-paper-title="ROCS: Request-Oriented Compute Sharing for Efficient Large-Scale Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="ROCS: Request-Oriented Compute Sharing for Efficient Large-Scale Recommendation 搜广推与 LLM 应用 Meta AI 2026-07-30 一次推荐请求会评分大量候选，而用户侧特征完全相同。ROCS 通过 Generalized Layer Masking 保持候选隔离，用 Deep Cross Attention 延迟交互，再由 IKBO 在 GPU kernel 内广播 request 表示。 Fidelity: 核心机制复现。实现一次 request encoding、延迟 candidate interaction 和批量候选评分。未复刻生产 GLM、IKBO CUDA kernel、Meta 私有模型与集群。本地对照口径：基线为逐候选重复编码；实验组为 ROCS core，相对基线 NDCG@10 +8.19%。  retrieval ranking serving compute-sharing 搜广推 自动研究与高效上线 本地ROCS是否实现生产GLM mask和IKBO CUDA广播？ 没有，当前仅覆盖共享表示与打分分工，未复刻专用kernel或Meta集群。需要区分模型结构的计算复用与真正设备内广播，后者需实测才能声称吞吐收益。 例如Python循环复用一个向量，不等于GPU kernel已经共享加载。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c3d495c5df8a7b41">本地ROCS是否实现生产GLM mask和IKBO CUDA广播？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arocs">ROCS: Request-Oriented Compute Sharing for Efficient Large-Scale Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有，当前仅覆盖共享表示与打分分工，未复刻专用kernel或Meta集群。需要区分模型结构的计算复用与真正设备内广播，后者需实测才能声称吞吐收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如Python循环复用一个向量，不等于GPU kernel已经共享加载。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27744">原论文</a> · <a href="../../../../reproductions/2607.27744-rocs/">实现解读</a> · <a href="#qa-c3d495c5df8a7b41">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:memory-layer" data-paper-title="Memory Layer: Train the In-Model Cache for Recommendation Models" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Memory Layer: Train the In-Model Cache for Recommendation Models 搜广推与 LLM 应用 Meta / Instagram Reels 2026-07-27 传统 early-stage ranker 在训练时用 item tower 的新鲜输出，服务时却读另一个流程预计算并发布的 item cache；cache miss 还会绕过正常模型。这造成训练、离线评测和线上服务看到三套不同表征。Memory Layer 把 cache 变成模型自身的稀疏参数表：item tower 在训练中写入，后续网络和服务共同读取；作者、topic 等 always-on 属性则保证新内容或 cache miss 仍可评分。 seed 42 的 NDCG@10 相对基线约 +4.36%，结构诊断而非公开小数据 lift 是本复现重点。Fidelity: 核心机制复现。本地实现训练内 item-tower 写回、共享 cache 读取、冻结外部快照对照和 always-on cache-miss fallback；不把普通 embedding lookup 冒充 Meta 的 MPZCH 基础设施。MovieLens 没有媒体创建时间、Instagram 冷启动曝光与线上 NE，因此不能验证论文业务 lift。  ranking training-serving-consistency cold-start cache serving 搜广推 自动研究与高效上线 Memory Layer 为什么要求训练、评测和服务都读取同一份表征？ 训练用新鲜 tower 输出、服务用外部旧 cache 会产生表征错位，cache miss 另走旁路又增加分布差异。内置 Memory 表由训练写回，评分始终读表，always-on 属性支持未命中。统一读取不等于缓存永远新鲜，仍需记录更新时间和缺失。 示意：训练以最新电影向量学好，线上却查上周版本，分数会漂；让两侧消费同一内存表能减少这种接口不一致，但不消除所有刷新滞后。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-memory-layer-0d31a0b7" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0d309a881f527fd6">Memory Layer 为什么要求训练、评测和服务都读取同一份表征？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amemory-layer">Memory Layer: Train the In-Model Cache for Recommendation Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta / Instagram Reels</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>训练用新鲜 tower 输出、服务用外部旧 cache 会产生表征错位，cache miss 另走旁路又增加分布差异。内置 Memory 表由训练写回，评分始终读表，always-on 属性支持未命中。统一读取不等于缓存永远新鲜，仍需记录更新时间和缺失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练以最新电影向量学好，线上却查上周版本，分数会漂；让两侧消费同一内存表能减少这种接口不一致，但不消除所有刷新滞后。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25110">原论文</a> · <a href="../../../../reproductions/2607.25110-memory-layer/">实现解读</a> · <a href="#qa-0d309a881f527fd6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:memory-layer" data-paper-title="Memory Layer: Train the In-Model Cache for Recommendation Models" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Memory Layer: Train the In-Model Cache for Recommendation Models 搜广推与 LLM 应用 Meta / Instagram Reels 2026-07-27 传统 early-stage ranker 在训练时用 item tower 的新鲜输出，服务时却读另一个流程预计算并发布的 item cache；cache miss 还会绕过正常模型。这造成训练、离线评测和线上服务看到三套不同表征。Memory Layer 把 cache 变成模型自身的稀疏参数表：item tower 在训练中写入，后续网络和服务共同读取；作者、topic 等 always-on 属性则保证新内容或 cache miss 仍可评分。 seed 42 的 NDCG@10 相对基线约 +4.36%，结构诊断而非公开小数据 lift 是本复现重点。Fidelity: 核心机制复现。本地实现训练内 item-tower 写回、共享 cache 读取、冻结外部快照对照和 always-on cache-miss fallback；不把普通 embedding lookup 冒充 Meta 的 MPZCH 基础设施。MovieLens 没有媒体创建时间、Instagram 冷启动曝光与线上 NE，因此不能验证论文业务 lift。  ranking training-serving-consistency cold-start cache serving 搜广推 自动研究与高效上线 Memory Layer为什么把item cache做成模型内稀疏参数表，而不继续用独立发布的外部缓存？ 训练用新鲜item塔输出、服务读旧缓存会造成表征错位，miss时走旁路又产生第三种分布。模型内写回与读取让后续网络在训练中就适应缓存语义，always-on属性还保证未命中项可评分。它改变的是数据依赖与训练服务一致性，不意味着缓存永远最新或外部读取完全没有开销。 示意：某商品训练时有新向量，上线却读到昨日旧值；把缓存纳入模型读取路径可让训练见到相同机制，缺失时仍用作者或主题等通用属性打分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-af7939892d02952f">Memory Layer为什么把item cache做成模型内稀疏参数表，而不继续用独立发布的外部缓存？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amemory-layer">Memory Layer: Train the In-Model Cache for Recommendation Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta / Instagram Reels</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>训练用新鲜item塔输出、服务读旧缓存会造成表征错位，miss时走旁路又产生第三种分布。模型内写回与读取让后续网络在训练中就适应缓存语义，always-on属性还保证未命中项可评分。它改变的是数据依赖与训练服务一致性，不意味着缓存永远最新或外部读取完全没有开销。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某商品训练时有新向量，上线却读到昨日旧值；把缓存纳入模型读取路径可让训练见到相同机制，缺失时仍用作者或主题等通用属性打分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25110">原论文</a> · <a href="../../../../reproductions/2607.25110-memory-layer/">实现解读</a> · <a href="#qa-af7939892d02952f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:memory-layer" data-paper-title="Memory Layer: Train the In-Model Cache for Recommendation Models" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Memory Layer: Train the In-Model Cache for Recommendation Models 搜广推与 LLM 应用 Meta / Instagram Reels 2026-07-27 传统 early-stage ranker 在训练时用 item tower 的新鲜输出，服务时却读另一个流程预计算并发布的 item cache；cache miss 还会绕过正常模型。这造成训练、离线评测和线上服务看到三套不同表征。Memory Layer 把 cache 变成模型自身的稀疏参数表：item tower 在训练中写入，后续网络和服务共同读取；作者、topic 等 always-on 属性则保证新内容或 cache miss 仍可评分。 seed 42 的 NDCG@10 相对基线约 +4.36%，结构诊断而非公开小数据 lift 是本复现重点。Fidelity: 核心机制复现。本地实现训练内 item-tower 写回、共享 cache 读取、冻结外部快照对照和 always-on cache-miss fallback；不把普通 embedding lookup 冒充 Meta 的 MPZCH 基础设施。MovieLens 没有媒体创建时间、Instagram 冷启动曝光与线上 NE，因此不能验证论文业务 lift。  ranking training-serving-consistency cold-start cache serving 搜广推 自动研究与高效上线 模型内 writeback 与定期全量发布外部 cache，相比一致性和维护成本如何变化？ writeback 把更新与训练事件耦合，减少独立发布管线带来的错位；外部发布可集中控制但可能落后和覆盖不齐。内存表仍有容量、并发和版本问题，always-on 也只是缺失 fallback。来源本地结构诊断不能外推 Meta 生产吞吐。 示意：训练到商品甲就写它的新向量，未出现商品仍旧；定期发布则全表一起换，两种更新节奏不同，不能只按命中率判断谁更好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-827dab223ef80fd9">模型内 writeback 与定期全量发布外部 cache，相比一致性和维护成本如何变化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amemory-layer">Memory Layer: Train the In-Model Cache for Recommendation Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta / Instagram Reels</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>writeback 把更新与训练事件耦合，减少独立发布管线带来的错位；外部发布可集中控制但可能落后和覆盖不齐。内存表仍有容量、并发和版本问题，always-on 也只是缺失 fallback。来源本地结构诊断不能外推 Meta 生产吞吐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练到商品甲就写它的新向量，未出现商品仍旧；定期发布则全表一起换，两种更新节奏不同，不能只按命中率判断谁更好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25110">原论文</a> · <a href="../../../../reproductions/2607.25110-memory-layer/">实现解读</a> · <a href="#qa-827dab223ef80fd9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:memory-layer" data-paper-title="Memory Layer: Train the In-Model Cache for Recommendation Models" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Memory Layer: Train the In-Model Cache for Recommendation Models 搜广推与 LLM 应用 Meta / Instagram Reels 2026-07-27 传统 early-stage ranker 在训练时用 item tower 的新鲜输出，服务时却读另一个流程预计算并发布的 item cache；cache miss 还会绕过正常模型。这造成训练、离线评测和线上服务看到三套不同表征。Memory Layer 把 cache 变成模型自身的稀疏参数表：item tower 在训练中写入，后续网络和服务共同读取；作者、topic 等 always-on 属性则保证新内容或 cache miss 仍可评分。 seed 42 的 NDCG@10 相对基线约 +4.36%，结构诊断而非公开小数据 lift 是本复现重点。Fidelity: 核心机制复现。本地实现训练内 item-tower 写回、共享 cache 读取、冻结外部快照对照和 always-on cache-miss fallback；不把普通 embedding lookup 冒充 Meta 的 MPZCH 基础设施。MovieLens 没有媒体创建时间、Instagram 冷启动曝光与线上 NE，因此不能验证论文业务 lift。  ranking training-serving-consistency cold-start cache serving 搜广推 自动研究与高效上线 Memory Layer 的 η=1 writeback 为什么不同于对 M[i] 做普通小学习率 SGD？ 这里把 item tower 输出直接覆盖对应表项，而非让旧表值缓慢沿任意梯度走。读出始终来自表，miss 分量置零但保留通用属性。应核验写回误差、覆盖与陈旧度，不能因表可训练就忽略来源定义的实际赋值行为。 示意：新 tower 输出一二三，写回后表项应就是一二三；若变成旧向量与新向量的十分之一混合，已不是 η=1 的覆盖语义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e90d4036e6663eba">Memory Layer 的 η=1 writeback 为什么不同于对 M[i] 做普通小学习率 SGD？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amemory-layer">Memory Layer: Train the In-Model Cache for Recommendation Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta / Instagram Reels</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这里把 item tower 输出直接覆盖对应表项，而非让旧表值缓慢沿任意梯度走。读出始终来自表，miss 分量置零但保留通用属性。应核验写回误差、覆盖与陈旧度，不能因表可训练就忽略来源定义的实际赋值行为。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新 tower 输出一二三，写回后表项应就是一二三；若变成旧向量与新向量的十分之一混合，已不是 η=1 的覆盖语义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25110">原论文</a> · <a href="../../../../reproductions/2607.25110-memory-layer/">实现解读</a> · <a href="#qa-e90d4036e6663eba">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recevolve" data-paper-title="RecEvolve: A Knowledge-Driven Autonomous Agent System for Recommender Systems" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="RecEvolve: A Knowledge-Driven Autonomous Agent System for Recommender Systems 搜广推与 LLM 应用 Google 2026-07-20 RecEvolve 让研究 Agent 从实验知识库提出模型变体，以独立验证集选择冠军，并用版本化状态支持失败回滚。系统显式防止通过极端温度等方式“刷指标”，让上一轮结论成为下一轮可审计的研究知识。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。实现提案、critic gate、隔离试验、冠军继承、回滚与 reward-hack 拒绝。未复刻 Google 私有日志、TPU 集群、生产 coding-agent 工具链和线上实验归因；该 adapter 作为推荐 Evolve 的统一多轮控制器算子。MovieLens 100K 上用固定候选空间执行完整研究控制流；三 seed 结果见 metrics/public-seeds42-44.json。本地指标用于比较同一公开协议下的控制策略，不复刻 Google 私有 Two-Tower 数值。  auto-research agent two-tower reward-hacking 搜广推 自动研究与高效上线 RecEvolve 为什么将研究知识库与冠军状态版本化？ 下一轮提案要知道过去真实试过什么，版本记录将候选、验证结果与约束绑定，失败可回滚而不污染长期冠军。知识不是随意摘要，缺配置与数据口径就难复用。固定候选流程成功也不证明开放式科研或真实生产晋级。 示意：上一轮修改门控失败，回滚旧冠军同时保留失败条件，下一轮避免重复；只保留最后目录而不记版本，会失去因果对照线索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-recevolve-55072983" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5016e08e383200b4">RecEvolve 为什么将研究知识库与冠军状态版本化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecevolve">RecEvolve: A Knowledge-Driven Autonomous Agent System for Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>下一轮提案要知道过去真实试过什么，版本记录将候选、验证结果与约束绑定，失败可回滚而不污染长期冠军。知识不是随意摘要，缺配置与数据口径就难复用。固定候选流程成功也不证明开放式科研或真实生产晋级。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>上一轮修改门控失败，回滚旧冠军同时保留失败条件，下一轮避免重复；只保留最后目录而不记版本，会失去因果对照线索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.01622">原论文</a> · <a href="../../../../reproductions/2609.01622-recevolve/">实现解读</a> · <a href="#qa-5016e08e383200b4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recevolve" data-paper-title="RecEvolve: A Knowledge-Driven Autonomous Agent System for Recommender Systems" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="RecEvolve: A Knowledge-Driven Autonomous Agent System for Recommender Systems 搜广推与 LLM 应用 Google 2026-07-20 RecEvolve 让研究 Agent 从实验知识库提出模型变体，以独立验证集选择冠军，并用版本化状态支持失败回滚。系统显式防止通过极端温度等方式“刷指标”，让上一轮结论成为下一轮可审计的研究知识。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。实现提案、critic gate、隔离试验、冠军继承、回滚与 reward-hack 拒绝。未复刻 Google 私有日志、TPU 集群、生产 coding-agent 工具链和线上实验归因；该 adapter 作为推荐 Evolve 的统一多轮控制器算子。MovieLens 100K 上用固定候选空间执行完整研究控制流；三 seed 结果见 metrics/public-seeds42-44.json。本地指标用于比较同一公开协议下的控制策略，不复刻 Google 私有 Two-Tower 数值。  auto-research agent two-tower reward-hacking 搜广推 自动研究与高效上线 RecEvolve 为什么把候选门控、独立验证集选择和版本回滚放在研究 agent 外围？ 研究 agent 能生成结构改动，也可能提出只对某个指标投机的配置。外部门控先拒绝违规候选，再用独立验证效用与当前冠军比较，只有真实改善才原子更新版本，失败则回滚并记录知识。它把“提出想法”与“接受证据”分开；测试集不能参与冠军选择，否则循环会逐步过拟合最终评估。 示意：agent 提议极低温度让分布异常尖锐，门控先检查是否合法；另一个结构能运行但验证集更差，就保留旧冠军，并把失败原因记入下轮实验知识。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-372bb80dd4440915">RecEvolve 为什么把候选门控、独立验证集选择和版本回滚放在研究 agent 外围？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecevolve">RecEvolve: A Knowledge-Driven Autonomous Agent System for Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>研究 agent 能生成结构改动，也可能提出只对某个指标投机的配置。外部门控先拒绝违规候选，再用独立验证效用与当前冠军比较，只有真实改善才原子更新版本，失败则回滚并记录知识。它把“提出想法”与“接受证据”分开；测试集不能参与冠军选择，否则循环会逐步过拟合最终评估。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>agent 提议极低温度让分布异常尖锐，门控先检查是否合法；另一个结构能运行但验证集更差，就保留旧冠军，并把失败原因记入下轮实验知识。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.01622">原论文</a> · <a href="../../../../reproductions/2609.01622-recevolve/">实现解读</a> · <a href="#qa-372bb80dd4440915">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recevolve" data-paper-title="RecEvolve: A Knowledge-Driven Autonomous Agent System for Recommender Systems" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="RecEvolve: A Knowledge-Driven Autonomous Agent System for Recommender Systems 搜广推与 LLM 应用 Google 2026-07-20 RecEvolve 让研究 Agent 从实验知识库提出模型变体，以独立验证集选择冠军，并用版本化状态支持失败回滚。系统显式防止通过极端温度等方式“刷指标”，让上一轮结论成为下一轮可审计的研究知识。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。实现提案、critic gate、隔离试验、冠军继承、回滚与 reward-hack 拒绝。未复刻 Google 私有日志、TPU 集群、生产 coding-agent 工具链和线上实验归因；该 adapter 作为推荐 Evolve 的统一多轮控制器算子。MovieLens 100K 上用固定候选空间执行完整研究控制流；三 seed 结果见 metrics/public-seeds42-44.json。本地指标用于比较同一公开协议下的控制策略，不复刻 Google 私有 Two-Tower 数值。  auto-research agent two-tower reward-hacking 搜广推 自动研究与高效上线 外部 critic gate 与让 agent 自评好坏，相比为什么能减少刷指标？ agent 可能偏向自己提案或利用温度等捷径，外部门控固定允许空间，独立验证效用决定是否晋级。它管理证据而非保证创新，门控规则也需可执行不能仅写提示。test 不得成为 critic 的常规搜索反馈。 示意：极低温度让输出异常尖锐，即使某代理分好看也先按约束拒绝；不是让 agent 自己说一句“没有作弊”就算审查通过。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c025052f0584af9e">外部 critic gate 与让 agent 自评好坏，相比为什么能减少刷指标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecevolve">RecEvolve: A Knowledge-Driven Autonomous Agent System for Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>agent 可能偏向自己提案或利用温度等捷径，外部门控固定允许空间，独立验证效用决定是否晋级。它管理证据而非保证创新，门控规则也需可执行不能仅写提示。test 不得成为 critic 的常规搜索反馈。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>极低温度让输出异常尖锐，即使某代理分好看也先按约束拒绝；不是让 agent 自己说一句“没有作弊”就算审查通过。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.01622">原论文</a> · <a href="../../../../reproductions/2609.01622-recevolve/">实现解读</a> · <a href="#qa-c025052f0584af9e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recevolve" data-paper-title="RecEvolve: A Knowledge-Driven Autonomous Agent System for Recommender Systems" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="RecEvolve: A Knowledge-Driven Autonomous Agent System for Recommender Systems 搜广推与 LLM 应用 Google 2026-07-20 RecEvolve 让研究 Agent 从实验知识库提出模型变体，以独立验证集选择冠军，并用版本化状态支持失败回滚。系统显式防止通过极端温度等方式“刷指标”，让上一轮结论成为下一轮可审计的研究知识。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。实现提案、critic gate、隔离试验、冠军继承、回滚与 reward-hack 拒绝。未复刻 Google 私有日志、TPU 集群、生产 coding-agent 工具链和线上实验归因；该 adapter 作为推荐 Evolve 的统一多轮控制器算子。MovieLens 100K 上用固定候选空间执行完整研究控制流；三 seed 结果见 metrics/public-seeds42-44.json。本地指标用于比较同一公开协议下的控制策略，不复刻 Google 私有 Two-Tower 数值。  auto-research agent two-tower reward-hacking 搜广推 自动研究与高效上线 RecEvolve 的原子冠军更新，为什么需要先完成验证产物再替换指针？ 部分训练、缺指标或写入中断不应覆盖可用基线，先核验候选终态与 J，再原子切换版本，否则失败难恢复。未胜出时保留旧冠军是有效结果，不强制每轮有改进。来源本地小幅差值不能外推线上长期收益。 示意：新 checkpoint 写到一半崩溃，冠军仍应指向旧完整版本；先改指针再写文件会让下一轮读取一个不存在或不完整的模型。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8790c407791febbd">RecEvolve 的原子冠军更新，为什么需要先完成验证产物再替换指针？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecevolve">RecEvolve: A Knowledge-Driven Autonomous Agent System for Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>部分训练、缺指标或写入中断不应覆盖可用基线，先核验候选终态与 J，再原子切换版本，否则失败难恢复。未胜出时保留旧冠军是有效结果，不强制每轮有改进。来源本地小幅差值不能外推线上长期收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新 checkpoint 写到一半崩溃，冠军仍应指向旧完整版本；先改指针再写文件会让下一轮读取一个不存在或不完整的模型。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.01622">原论文</a> · <a href="../../../../reproductions/2609.01622-recevolve/">实现解读</a> · <a href="#qa-8790c407791febbd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:prompt-generation" data-paper-title="Prompt Generation Technical Report" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Prompt Generation Technical Report 搜广推与 LLM 应用 Alibaba / Taobao Search 2026-07-13 生成式检索把 query、用户行为和异构特征输入 LLM，再直接生成商品或文档 SID。工业系统的问题不只是模型效果：每次加特征都要同步修改数据、训练和 serving，容易产生 training-serving skew；长文本和行为序列又会迅速放大 token 数与延迟。PG 用 prompt_template.json 与 prompt_feature.json 把特征工程从模型代码中解耦。 Fidelity: 核心机制复现。本地实际执行论文同款 Qwen2.5-0.5B、MiniOneRec Amazon Office 数据与官方三段式 SID、双 JSON 单一事实源、text/embedding/combo/sequence 四类特征、preprocessor/projector/merger 组件协议、embedding-space mean merger、LoRA SFT、validation 配置选择和 held-out 候选评分。未复刻淘宝全量训练、C++ batched kernels、线上 event replay 和生产 serving。  llm-recommendation generative-retrieval autoresearch serving 搜广推 自动研究与高效上线 Prompt Generation 为什么把特征类型与处理组件分成两个正交维度？ text、embedding、combo、sequence 描述输入是什么，preprocessor、projector、merger 描述如何处理；拆开可组合而不为每种特征改模型代码。配置是可执行协议，不是单纯提示文案，错误配置仍会丢信息或制造训练服务偏差。 示意：标题是 text，可先清洗再投影后池化；行为是 sequence，也可用同类组件不同配置，不能把“文本”直接等同某一种固定处理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-prompt-generation-d1640558" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-cc9e170b1b09019e">Prompt Generation 为什么把特征类型与处理组件分成两个正交维度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aprompt-generation">Prompt Generation Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao Search</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>text、embedding、combo、sequence 描述输入是什么，preprocessor、projector、merger 描述如何处理；拆开可组合而不为每种特征改模型代码。配置是可执行协议，不是单纯提示文案，错误配置仍会丢信息或制造训练服务偏差。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>标题是 text，可先清洗再投影后池化；行为是 sequence，也可用同类组件不同配置，不能把“文本”直接等同某一种固定处理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.11326">原论文</a> · <a href="../../../../reproductions/2607.11326-prompt-generation/">实现解读</a> · <a href="#qa-cc9e170b1b09019e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:prompt-generation" data-paper-title="Prompt Generation Technical Report" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Prompt Generation Technical Report 搜广推与 LLM 应用 Alibaba / Taobao Search 2026-07-13 生成式检索把 query、用户行为和异构特征输入 LLM，再直接生成商品或文档 SID。工业系统的问题不只是模型效果：每次加特征都要同步修改数据、训练和 serving，容易产生 training-serving skew；长文本和行为序列又会迅速放大 token 数与延迟。PG 用 prompt_template.json 与 prompt_feature.json 把特征工程从模型代码中解耦。 Fidelity: 核心机制复现。本地实际执行论文同款 Qwen2.5-0.5B、MiniOneRec Amazon Office 数据与官方三段式 SID、双 JSON 单一事实源、text/embedding/combo/sequence 四类特征、preprocessor/projector/merger 组件协议、embedding-space mean merger、LoRA SFT、validation 配置选择和 held-out 候选评分。未复刻淘宝全量训练、C++ batched kernels、线上 event replay 和生产 serving。  llm-recommendation generative-retrieval autoresearch serving 搜广推 自动研究与高效上线 Prompt Generation 的 preprocessor、projector、merger 为什么要与模板一起配置化？ 新增特征往往同时涉及离线数据处理和在线输入组装，分别写代码容易产生训练服务偏差。统一协议把清洗、空间投影与融合压缩拆为可组合部件，让训练和服务解释同一份配置。merger 还控制 token 数，因此它影响延迟与信息损失，不只是文本拼接工具；均值压缩的强基线也不意味着所有顺序信息都可丢弃。 示意：给检索器新增商品标题，配置声明文本清洗、向量投影和均值压缩后，训练与服务都产出同样的一个 token。若两边各自实现，一边截十词另一边读全文就会偏离。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8d412e12f27fcb01">Prompt Generation 的 preprocessor、projector、merger 为什么要与模板一起配置化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aprompt-generation">Prompt Generation Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao Search</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>新增特征往往同时涉及离线数据处理和在线输入组装，分别写代码容易产生训练服务偏差。统一协议把清洗、空间投影与融合压缩拆为可组合部件，让训练和服务解释同一份配置。merger 还控制 token 数，因此它影响延迟与信息损失，不只是文本拼接工具；均值压缩的强基线也不意味着所有顺序信息都可丢弃。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>给检索器新增商品标题，配置声明文本清洗、向量投影和均值压缩后，训练与服务都产出同样的一个 token。若两边各自实现，一边截十词另一边读全文就会偏离。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.11326">原论文</a> · <a href="../../../../reproductions/2607.11326-prompt-generation/">实现解读</a> · <a href="#qa-8d412e12f27fcb01">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:prompt-generation" data-paper-title="Prompt Generation Technical Report" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Prompt Generation Technical Report 搜广推与 LLM 应用 Alibaba / Taobao Search 2026-07-13 生成式检索把 query、用户行为和异构特征输入 LLM，再直接生成商品或文档 SID。工业系统的问题不只是模型效果：每次加特征都要同步修改数据、训练和 serving，容易产生 training-serving skew；长文本和行为序列又会迅速放大 token 数与延迟。PG 用 prompt_template.json 与 prompt_feature.json 把特征工程从模型代码中解耦。 Fidelity: 核心机制复现。本地实际执行论文同款 Qwen2.5-0.5B、MiniOneRec Amazon Office 数据与官方三段式 SID、双 JSON 单一事实源、text/embedding/combo/sequence 四类特征、preprocessor/projector/merger 组件协议、embedding-space mean merger、LoRA SFT、validation 配置选择和 held-out 候选评分。未复刻淘宝全量训练、C++ batched kernels、线上 event replay 和生产 serving。  llm-recommendation generative-retrieval autoresearch serving 搜广推 自动研究与高效上线 无参数 mean merger 与可学习压缩，相比默认优点与信息代价是什么？ 均值简单、无额外训练参数且易保持服务一致，可降低 token 成本；它忽略顺序和部分细节，学习压缩更灵活也增加开销与过拟合。来源称强默认不意味着所有字段都应均值，更不能用压缩率替代相关性验证。 示意：几条同义商品属性均值可够用，带否定和先后关系的长行为直接平均可能丢“不要”或顺序，需按特征任务选择。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-bc543930148110c9">无参数 mean merger 与可学习压缩，相比默认优点与信息代价是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aprompt-generation">Prompt Generation Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao Search</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>均值简单、无额外训练参数且易保持服务一致，可降低 token 成本；它忽略顺序和部分细节，学习压缩更灵活也增加开销与过拟合。来源称强默认不意味着所有字段都应均值，更不能用压缩率替代相关性验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>几条同义商品属性均值可够用，带否定和先后关系的长行为直接平均可能丢“不要”或顺序，需按特征任务选择。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.11326">原论文</a> · <a href="../../../../reproductions/2607.11326-prompt-generation/">实现解读</a> · <a href="#qa-bc543930148110c9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:prompt-generation" data-paper-title="Prompt Generation Technical Report" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Prompt Generation Technical Report 搜广推与 LLM 应用 Alibaba / Taobao Search 2026-07-13 生成式检索把 query、用户行为和异构特征输入 LLM，再直接生成商品或文档 SID。工业系统的问题不只是模型效果：每次加特征都要同步修改数据、训练和 serving，容易产生 training-serving skew；长文本和行为序列又会迅速放大 token 数与延迟。PG 用 prompt_template.json 与 prompt_feature.json 把特征工程从模型代码中解耦。 Fidelity: 核心机制复现。本地实际执行论文同款 Qwen2.5-0.5B、MiniOneRec Amazon Office 数据与官方三段式 SID、双 JSON 单一事实源、text/embedding/combo/sequence 四类特征、preprocessor/projector/merger 组件协议、embedding-space mean merger、LoRA SFT、validation 配置选择和 held-out 候选评分。未复刻淘宝全量训练、C++ batched kernels、线上 event replay 和生产 serving。  llm-recommendation generative-retrieval autoresearch serving 搜广推 自动研究与高效上线 PG_train(x,c)=PG_serve(x,c) 为什么需要用线上原始特征 replay 检查？ 同一 JSON 不保证两端依赖、截断、缺失值和 tokenizer 实现一致，重放实际源特征才能比较最终输入张量。配置版本与解释器都需绑定。来源本地按验证选 Title 后 test 下降，应保留而不以压缩更短宣布效果成功。 示意：训练标题清洗保留数字、服务删型号，两边配置名相同却输入不同；replay 对比能暴露这种隐藏 skew。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-64a9ffca7a083428">PG_train(x,c)=PG_serve(x,c) 为什么需要用线上原始特征 replay 检查？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aprompt-generation">Prompt Generation Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao Search</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一 JSON 不保证两端依赖、截断、缺失值和 tokenizer 实现一致，重放实际源特征才能比较最终输入张量。配置版本与解释器都需绑定。来源本地按验证选 Title 后 test 下降，应保留而不以压缩更短宣布效果成功。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练标题清洗保留数字、服务删型号，两边配置名相同却输入不同；replay 对比能暴露这种隐藏 skew。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.11326">原论文</a> · <a href="../../../../reproductions/2607.11326-prompt-generation/">实现解读</a> · <a href="#qa-64a9ffca7a083428">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:nova" data-paper-title="NOVA: A Verification-Aware Agent Harness for Architecture Evolution in Industrial Recommender Systems" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="NOVA: A Verification-Aware Agent Harness for Architecture Evolution in Industrial Recommender Systems 搜广推与 LLM 应用 Tencent 2026-06-25 普通代码 agent 只能证明代码“能跑”，无法阻止结构语义错误和静默负向。NOVA 用 architecture gradient 汇总历史修改、验证诊断和指标反馈，再通过 L1 结构语义、L2 可执行、L3 离线有效、L4 在线影响的级联验证逐级放行，高风险任务交给人工。 复现保真度：核心机制复现。复现保真度：核心机制复现。四级验证、失败方向记忆和 architecture gradient 均实际执行；腾讯生产 agent 与线上灰度未复刻。在 MovieLens 100K 上生成 transition、content、popularity 和故意错误的 shape 候选，真实执行四级验证并只用 validation 选候选；通用 evolve 还会把验证记录、成功技能和禁止方向写入 result.json。  auto-research architecture-evolution verification 搜广推 自动研究与高效上线 NOVA 的 architecture gradient 为什么不是普通反向传播梯度？ 它汇总历史架构修改、诊断与指标，作为 agent 下一轮结构选择的反馈，属于研究控制信号，而非某个参数可微损失的导数。名称强调方向性，不能据此假设可以端到端对代码求梯度或保证每次修改提升。 示意：记录“上次加宽超预算、改门控验证退化”可影响下一提案，这像研究经验方向；它不是给 Python 源码每个字符计算一个真实导数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-nova-6f1301b9" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-65efab2b17892552">NOVA 的 architecture gradient 为什么不是普通反向传播梯度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Anova">NOVA: A Verification-Aware Agent Harness for Architecture Evolution in Industrial Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它汇总历史架构修改、诊断与指标，作为 agent 下一轮结构选择的反馈，属于研究控制信号，而非某个参数可微损失的导数。名称强调方向性，不能据此假设可以端到端对代码求梯度或保证每次修改提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>记录“上次加宽超预算、改门控验证退化”可影响下一提案，这像研究经验方向；它不是给 Python 源码每个字符计算一个真实导数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.27243">原论文</a> · <a href="../../../../reproductions/2606.27243-nova/">实现解读</a> · <a href="#qa-65efab2b17892552">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:nova" data-paper-title="NOVA: A Verification-Aware Agent Harness for Architecture Evolution in Industrial Recommender Systems" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="NOVA: A Verification-Aware Agent Harness for Architecture Evolution in Industrial Recommender Systems 搜广推与 LLM 应用 Tencent 2026-06-25 普通代码 agent 只能证明代码“能跑”，无法阻止结构语义错误和静默负向。NOVA 用 architecture gradient 汇总历史修改、验证诊断和指标反馈，再通过 L1 结构语义、L2 可执行、L3 离线有效、L4 在线影响的级联验证逐级放行，高风险任务交给人工。 复现保真度：核心机制复现。复现保真度：核心机制复现。四级验证、失败方向记忆和 architecture gradient 均实际执行；腾讯生产 agent 与线上灰度未复刻。在 MovieLens 100K 上生成 transition、content、popularity 和故意错误的 shape 候选，真实执行四级验证并只用 validation 选候选；通用 evolve 还会把验证记录、成功技能和禁止方向写入 result.json。  auto-research architecture-evolution verification 搜广推 自动研究与高效上线 NOVA 为什么把架构修改验证拆成结构语义、可执行、离线有效和在线影响四层？ 代码能运行只排除了部分执行错误，不能说明架构仍符合设计，也不能说明指标或线上效果变好。NOVA 将历史修改与诊断反馈汇总为架构更新依据，再按成本递增的验证层级放行，让明显错误尽早退出。离线通过仍需独立的在线证据；本地可执行级联属于诊断流程，不能充当真实上线结果。 示意：一次改动把多任务分支接错，张量维度却仍兼容。运行测试可能通过，结构语义检查先拦住它；另一次结构正确但验证集退化，则在离线有效层退出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-1fd1d6f99b8afe4f">NOVA 为什么把架构修改验证拆成结构语义、可执行、离线有效和在线影响四层？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Anova">NOVA: A Verification-Aware Agent Harness for Architecture Evolution in Industrial Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>代码能运行只排除了部分执行错误，不能说明架构仍符合设计，也不能说明指标或线上效果变好。NOVA 将历史修改与诊断反馈汇总为架构更新依据，再按成本递增的验证层级放行，让明显错误尽早退出。离线通过仍需独立的在线证据；本地可执行级联属于诊断流程，不能充当真实上线结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次改动把多任务分支接错，张量维度却仍兼容。运行测试可能通过，结构语义检查先拦住它；另一次结构正确但验证集退化，则在离线有效层退出。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.27243">原论文</a> · <a href="../../../../reproductions/2606.27243-nova/">实现解读</a> · <a href="#qa-1fd1d6f99b8afe4f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:nova" data-paper-title="NOVA: A Verification-Aware Agent Harness for Architecture Evolution in Industrial Recommender Systems" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="NOVA: A Verification-Aware Agent Harness for Architecture Evolution in Industrial Recommender Systems 搜广推与 LLM 应用 Tencent 2026-06-25 普通代码 agent 只能证明代码“能跑”，无法阻止结构语义错误和静默负向。NOVA 用 architecture gradient 汇总历史修改、验证诊断和指标反馈，再通过 L1 结构语义、L2 可执行、L3 离线有效、L4 在线影响的级联验证逐级放行，高风险任务交给人工。 复现保真度：核心机制复现。复现保真度：核心机制复现。四级验证、失败方向记忆和 architecture gradient 均实际执行；腾讯生产 agent 与线上灰度未复刻。在 MovieLens 100K 上生成 transition、content、popularity 和故意错误的 shape 候选，真实执行四级验证并只用 validation 选候选；通用 evolve 还会把验证记录、成功技能和禁止方向写入 result.json。  auto-research architecture-evolution verification 搜广推 自动研究与高效上线 NOVA 的结构语义检查与普通运行测试，为什么一个通过不能替代另一个？ 形状兼容代码也可能把任务头接错或取消定义性信息流，语义层检查设计；可执行层确认实际运行，再由离线与在线证据判断价值。四层问题不同，不能靠训练 loss 下降跳过结构。来源公开候选流程不包含真实生产 A/B。 示意：购买头误接点击标签仍可训练并降低 loss，运行测试通过；语义检查应发现任务关系错，不能等线上效果坏了才判断。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-3c68b7b618e25f7c">NOVA 的结构语义检查与普通运行测试，为什么一个通过不能替代另一个？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Anova">NOVA: A Verification-Aware Agent Harness for Architecture Evolution in Industrial Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>形状兼容代码也可能把任务头接错或取消定义性信息流，语义层检查设计；可执行层确认实际运行，再由离线与在线证据判断价值。四层问题不同，不能靠训练 loss 下降跳过结构。来源公开候选流程不包含真实生产 A/B。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>购买头误接点击标签仍可训练并降低 loss，运行测试通过；语义检查应发现任务关系错，不能等线上效果坏了才判断。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.27243">原论文</a> · <a href="../../../../reproductions/2606.27243-nova/">实现解读</a> · <a href="#qa-3c68b7b618e25f7c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:nova" data-paper-title="NOVA: A Verification-Aware Agent Harness for Architecture Evolution in Industrial Recommender Systems" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="NOVA: A Verification-Aware Agent Harness for Architecture Evolution in Industrial Recommender Systems 搜广推与 LLM 应用 Tencent 2026-06-25 普通代码 agent 只能证明代码“能跑”，无法阻止结构语义错误和静默负向。NOVA 用 architecture gradient 汇总历史修改、验证诊断和指标反馈，再通过 L1 结构语义、L2 可执行、L3 离线有效、L4 在线影响的级联验证逐级放行，高风险任务交给人工。 复现保真度：核心机制复现。复现保真度：核心机制复现。四级验证、失败方向记忆和 architecture gradient 均实际执行；腾讯生产 agent 与线上灰度未复刻。在 MovieLens 100K 上生成 transition、content、popularity 和故意错误的 shape 候选，真实执行四级验证并只用 validation 选候选；通用 evolve 还会把验证记录、成功技能和禁止方向写入 result.json。  auto-research architecture-evolution verification 搜广推 自动研究与高效上线 NOVA 本地选择 candidate 后，哪些产物需区分真实验证与模拟 online？ 候选、形状失败、validation 指标和晋级记录可真实执行；线上影响若无真实流量只能标诊断或模拟，不应把第四层存在于控制流就称上线完成。test 应只评最终选型，成功技能和禁止方向需写可审计结果。 示意：故意错误 shape 被拦证明执行 gate 有用，模拟分数通过不代表用户实验；两种“通过”必须在记录中保留不同证据等级。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f549c47146369669">NOVA 本地选择 candidate 后，哪些产物需区分真实验证与模拟 online？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Anova">NOVA: A Verification-Aware Agent Harness for Architecture Evolution in Industrial Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>候选、形状失败、validation 指标和晋级记录可真实执行；线上影响若无真实流量只能标诊断或模拟，不应把第四层存在于控制流就称上线完成。test 应只评最终选型，成功技能和禁止方向需写可审计结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>故意错误 shape 被拦证明执行 gate 有用，模拟分数通过不代表用户实验；两种“通过”必须在记录中保留不同证据等级。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.27243">原论文</a> · <a href="../../../../reproductions/2606.27243-nova/">实现解读</a> · <a href="#qa-f549c47146369669">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:evorec" data-paper-title="EvoRec: Self-Evolving Agentic Recommender Systems" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="EvoRec: Self-Evolving Agentic Recommender Systems 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-06-15 既有 LLM agent 每轮只翻译代码，不会积累优化方法。EvoRec 让 Research/Code Agent 迭代模型，Skill Evolver 从持久 Memory 中提炼可复用方法，使“模型”和“怎么优化模型”同时进化。 复现保真度：核心机制复现。复现保真度：核心机制复现。模型候选与优化方法双轨迭代、跨代 skill memory 均实际执行；生产多 agent 工具链未复刻。本地让 transition、content、popularity 三类技能竞争，连续三代根据固定 validation 选择并把胜出技能写入 memory；该记忆还接入通用 evolve 的下一代候选排序。  auto-research agent skill-evolution 搜广推 自动研究与高效上线 EvoRec 为什么不仅进化模型，还提炼优化 skill？ 最终代码没有保留哪些尝试有效、在哪些条件下有效，后续容易重复失败。Skill Evolver 从持久实验记忆总结方法，指导 Research/Code Agent 下一轮提案。技能是带证据的经验，不能当新数据上免验证的规则，历史成功也有范围。 示意：除了保存一套双塔，还记下“短历史时加强内容分支”的验证条件，下一轮据此思考，而不是盲抄所有旧参数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-evorec-ed228584" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b33ffe7f74179c8b">EvoRec 为什么不仅进化模型，还提炼优化 skill？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aevorec">EvoRec: Self-Evolving Agentic Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最终代码没有保留哪些尝试有效、在哪些条件下有效，后续容易重复失败。Skill Evolver 从持久实验记忆总结方法，指导 Research/Code Agent 下一轮提案。技能是带证据的经验，不能当新数据上免验证的规则，历史成功也有范围。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>除了保存一套双塔，还记下“短历史时加强内容分支”的验证条件，下一轮据此思考，而不是盲抄所有旧参数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.28368">原论文</a> · <a href="../../../../reproductions/2606.28368-evorec/">实现解读</a> · <a href="#qa-b33ffe7f74179c8b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:evorec" data-paper-title="EvoRec: Self-Evolving Agentic Recommender Systems" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="EvoRec: Self-Evolving Agentic Recommender Systems 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-06-15 既有 LLM agent 每轮只翻译代码，不会积累优化方法。EvoRec 让 Research/Code Agent 迭代模型，Skill Evolver 从持久 Memory 中提炼可复用方法，使“模型”和“怎么优化模型”同时进化。 复现保真度：核心机制复现。复现保真度：核心机制复现。模型候选与优化方法双轨迭代、跨代 skill memory 均实际执行；生产多 agent 工具链未复刻。本地让 transition、content、popularity 三类技能竞争，连续三代根据固定 validation 选择并把胜出技能写入 memory；该记忆还接入通用 evolve 的下一代候选排序。  auto-research agent skill-evolution 搜广推 自动研究与高效上线 EvoRec让Skill Evolver进化什么，为什么不只保存最终模型代码？ 模型参数和代码记录了本轮结果，却未必保留发现有效改动的条件与方法。Skill Evolver从持久实验记忆中总结可复用优化技能，供下一轮Research与Code Agent调用，使搜索过程本身也能改进。技能仍须经实际执行与验证，不能把事后写出的漂亮经验当成已经证明可泛化的优化规律。 示意：一次负采样改动只在长尾切片有效，保存技能时应记住适用条件与失败切片；下轮遇到不同数据时先验证，而不是直接照搬冠军代码。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-d7f3d1db570aa7ca">EvoRec让Skill Evolver进化什么，为什么不只保存最终模型代码？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aevorec">EvoRec: Self-Evolving Agentic Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>模型参数和代码记录了本轮结果，却未必保留发现有效改动的条件与方法。Skill Evolver从持久实验记忆中总结可复用优化技能，供下一轮Research与Code Agent调用，使搜索过程本身也能改进。技能仍须经实际执行与验证，不能把事后写出的漂亮经验当成已经证明可泛化的优化规律。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次负采样改动只在长尾切片有效，保存技能时应记住适用条件与失败切片；下轮遇到不同数据时先验证，而不是直接照搬冠军代码。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.28368">原论文</a> · <a href="../../../../reproductions/2606.28368-evorec/">实现解读</a> · <a href="#qa-d7f3d1db570aa7ca">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:evorec" data-paper-title="EvoRec: Self-Evolving Agentic Recommender Systems" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="EvoRec: Self-Evolving Agentic Recommender Systems 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-06-15 既有 LLM agent 每轮只翻译代码，不会积累优化方法。EvoRec 让 Research/Code Agent 迭代模型，Skill Evolver 从持久 Memory 中提炼可复用方法，使“模型”和“怎么优化模型”同时进化。 复现保真度：核心机制复现。复现保真度：核心机制复现。模型候选与优化方法双轨迭代、跨代 skill memory 均实际执行；生产多 agent 工具链未复刻。本地让 transition、content、popularity 三类技能竞争，连续三代根据固定 validation 选择并把胜出技能写入 memory；该记忆还接入通用 evolve 的下一代候选排序。  auto-research agent skill-evolution 搜广推 自动研究与高效上线 EvoRec 的技能记忆与固定 grid search，怎样改变后续探索？ 固定网格反复比较预列配置，技能记忆可调整优化方法、候选顺序和组合方向，复用过去反馈。若本地只在少数预设技能竞争，结论需限定有界控制流，不能称开放式发明算法。验证负责选择，test 不能参与迭代。 示意：网格每次照跑十组，技能库可先尝试前轮已发现有用的表示变换；但只有三个技能的实验不能证明能自动发现任意新网络。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-47950852691d04f6">EvoRec 的技能记忆与固定 grid search，怎样改变后续探索？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aevorec">EvoRec: Self-Evolving Agentic Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定网格反复比较预列配置，技能记忆可调整优化方法、候选顺序和组合方向，复用过去反馈。若本地只在少数预设技能竞争，结论需限定有界控制流，不能称开放式发明算法。验证负责选择，test 不能参与迭代。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>网格每次照跑十组，技能库可先尝试前轮已发现有用的表示变换；但只有三个技能的实验不能证明能自动发现任意新网络。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.28368">原论文</a> · <a href="../../../../reproductions/2606.28368-evorec/">实现解读</a> · <a href="#qa-47950852691d04f6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:evorec" data-paper-title="EvoRec: Self-Evolving Agentic Recommender Systems" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="EvoRec: Self-Evolving Agentic Recommender Systems 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-06-15 既有 LLM agent 每轮只翻译代码，不会积累优化方法。EvoRec 让 Research/Code Agent 迭代模型，Skill Evolver 从持久 Memory 中提炼可复用方法，使“模型”和“怎么优化模型”同时进化。 复现保真度：核心机制复现。复现保真度：核心机制复现。模型候选与优化方法双轨迭代、跨代 skill memory 均实际执行；生产多 agent 工具链未复刻。本地让 transition、content、popularity 三类技能竞争，连续三代根据固定 validation 选择并把胜出技能写入 memory；该记忆还接入通用 evolve 的下一代候选排序。  auto-research agent skill-evolution 搜广推 自动研究与高效上线 EvoRec 写入 memory 为什么需要保留数据协议和失败条件？ 赢家名称不能解释是否适用，记忆需绑定候选、验证口径、观察指标与约束，失败也帮助避免重复。下一代复用应调用真实算子，注册一个 skill 标签不等于执行集成。本地三代结果只支持其具体候选空间。 示意：只写“内容塔更好”会误导所有场景；写清“同预算、稀疏历史验证下更好，长历史未验证”，才能有条件地指导下一轮。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c437ad23d283a87d">EvoRec 写入 memory 为什么需要保留数据协议和失败条件？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aevorec">EvoRec: Self-Evolving Agentic Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>赢家名称不能解释是否适用，记忆需绑定候选、验证口径、观察指标与约束，失败也帮助避免重复。下一代复用应调用真实算子，注册一个 skill 标签不等于执行集成。本地三代结果只支持其具体候选空间。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>只写“内容塔更好”会误导所有场景；写清“同预算、稀疏历史验证下更好，长历史未验证”，才能有条件地指导下一轮。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.28368">原论文</a> · <a href="../../../../reproductions/2606.28368-evorec/">实现解读</a> · <a href="#qa-c437ad23d283a87d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rec-distill" data-paper-title="Rec-Distill: An Industrial Distillation Pipeline for Large-Scale Recommendation Models" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Rec-Distill: An Industrial Distillation Pipeline for Large-Scale Recommendation Models 搜广推与 LLM 应用 ByteDance / Douyin / TikTok 2026-05-28 工业大推荐 teacher 无法直接 serving，且 teacher/student 数据采样与实时分布不同。Rec-Distill 让 teacher 在自身 forward 阶段写出黑盒 logits，一份信号可异步服务多个 student。Student 的 main tower 只收真实标签并用于线上；aux tower 同时收 task 与 distillation loss，两者共享 backbone。 Fidelity: 完整核心链路复现。本地实际训练大 teacher 与轻 student，物化 black-box logits，执行 student-side sampling correction、main/aux decoupled towers、batch→streaming 两阶段蒸馏，并在 validation 搜索 loss ratio。本地对照口径：迁移基线是相同日程训练的 Raw Student；实验组是 Rec-Distill Student；NDCG@10 从 0.0039 降至 0.0036，transferability -4.11%。   搜广推 自动研究与高效上线 Rec-Distill 为什么让 teacher 写黑盒 logits 异步服务多个 student？ 大教师不适合每个学生请求实时运行，训练前向顺带产出信号可复用，学生按自己时间表消费。数据采样与时效不同仍会造成概率错位，需校正而非直接拷贝。黑盒接口减少耦合，也限制学生取得教师中间表示。 示意：教师一次给一批候选输出分数，两种小模型可各自训练；它们无需同进程跑大教师，但必须知道这些分数来自什么样本与版本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-rec-distill-367afce1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6ffcb019fb96fa25">Rec-Distill 为什么让 teacher 写黑盒 logits 异步服务多个 student？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arec-distill">Rec-Distill: An Industrial Distillation Pipeline for Large-Scale Recommendation Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin / TikTok</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>大教师不适合每个学生请求实时运行，训练前向顺带产出信号可复用，学生按自己时间表消费。数据采样与时效不同仍会造成概率错位，需校正而非直接拷贝。黑盒接口减少耦合，也限制学生取得教师中间表示。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教师一次给一批候选输出分数，两种小模型可各自训练；它们无需同进程跑大教师，但必须知道这些分数来自什么样本与版本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.29755">原论文</a> · <a href="../../../../reproductions/2605.29755-rec-distill/">实现解读</a> · <a href="#qa-6ffcb019fb96fa25">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rec-distill" data-paper-title="Rec-Distill: An Industrial Distillation Pipeline for Large-Scale Recommendation Models" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Rec-Distill: An Industrial Distillation Pipeline for Large-Scale Recommendation Models 搜广推与 LLM 应用 ByteDance / Douyin / TikTok 2026-05-28 工业大推荐 teacher 无法直接 serving，且 teacher/student 数据采样与实时分布不同。Rec-Distill 让 teacher 在自身 forward 阶段写出黑盒 logits，一份信号可异步服务多个 student。Student 的 main tower 只收真实标签并用于线上；aux tower 同时收 task 与 distillation loss，两者共享 backbone。 Fidelity: 完整核心链路复现。本地实际训练大 teacher 与轻 student，物化 black-box logits，执行 student-side sampling correction、main/aux decoupled towers、batch→streaming 两阶段蒸馏，并在 validation 搜索 loss ratio。本地对照口径：迁移基线是相同日程训练的 Raw Student；实验组是 Rec-Distill Student；NDCG@10 从 0.0039 降至 0.0036，transferability -4.11%。   搜广推 自动研究与高效上线 Rec-Distill 为什么先校正 teacher 的采样概率空间，还把蒸馏放在 aux tower 而非线上 main tower？ teacher 与 student 的采样方式不同，原始 logit 对应的概率含义可能不一致，直接拟合会把采样偏差也传过去。先按 student 口径校正，再让辅助塔接收任务与蒸馏损失，共享主干迁移知识；主塔只接真实标签并负责服务。这样控制蒸馏对输出校准的干扰，但教师质量与时效仍限制迁移收益。 示意：教师训练时更强地下采样负例，其分数不能直接当学生的真实点击概率。校正后让辅助头学习软信号，线上主头继续由真实标签约束，避免照搬错误的概率尺度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-995da271649e534d">Rec-Distill 为什么先校正 teacher 的采样概率空间，还把蒸馏放在 aux tower 而非线上 main tower？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arec-distill">Rec-Distill: An Industrial Distillation Pipeline for Large-Scale Recommendation Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin / TikTok</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>teacher 与 student 的采样方式不同，原始 logit 对应的概率含义可能不一致，直接拟合会把采样偏差也传过去。先按 student 口径校正，再让辅助塔接收任务与蒸馏损失，共享主干迁移知识；主塔只接真实标签并负责服务。这样控制蒸馏对输出校准的干扰，但教师质量与时效仍限制迁移收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教师训练时更强地下采样负例，其分数不能直接当学生的真实点击概率。校正后让辅助头学习软信号，线上主头继续由真实标签约束，避免照搬错误的概率尺度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.29755">原论文</a> · <a href="../../../../reproductions/2605.29755-rec-distill/">实现解读</a> · <a href="#qa-995da271649e534d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rec-distill" data-paper-title="Rec-Distill: An Industrial Distillation Pipeline for Large-Scale Recommendation Models" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Rec-Distill: An Industrial Distillation Pipeline for Large-Scale Recommendation Models 搜广推与 LLM 应用 ByteDance / Douyin / TikTok 2026-05-28 工业大推荐 teacher 无法直接 serving，且 teacher/student 数据采样与实时分布不同。Rec-Distill 让 teacher 在自身 forward 阶段写出黑盒 logits，一份信号可异步服务多个 student。Student 的 main tower 只收真实标签并用于线上；aux tower 同时收 task 与 distillation loss，两者共享 backbone。 Fidelity: 完整核心链路复现。本地实际训练大 teacher 与轻 student，物化 black-box logits，执行 student-side sampling correction、main/aux decoupled towers、batch→streaming 两阶段蒸馏，并在 validation 搜索 loss ratio。本地对照口径：迁移基线是相同日程训练的 Raw Student；实验组是 Rec-Distill Student；NDCG@10 从 0.0039 降至 0.0036，transferability -4.11%。   搜广推 自动研究与高效上线 main/aux 双塔蒸馏与直接让线上 main 拟合教师，相比保护哪类输出？ main 只受真实标签约束保持服务目标，aux 同时接任务与蒸馏，两者经共享 backbone 间接迁知识，减少教师采样偏差直接改输出校准。共享仍有间接影响，不是彻底隔离。来源 teacher 强而 student 迁移为负，不能以大教师存在保证成功。 示意：教师因采样分数偏高，aux 可学相对知识，main 继续看真实点击；直接让 main 硬拟合未校正概率更可能复制错误基准。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-480b099c9b0f77c3">main/aux 双塔蒸馏与直接让线上 main 拟合教师，相比保护哪类输出？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arec-distill">Rec-Distill: An Industrial Distillation Pipeline for Large-Scale Recommendation Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin / TikTok</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>main 只受真实标签约束保持服务目标，aux 同时接任务与蒸馏，两者经共享 backbone 间接迁知识，减少教师采样偏差直接改输出校准。共享仍有间接影响，不是彻底隔离。来源 teacher 强而 student 迁移为负，不能以大教师存在保证成功。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教师因采样分数偏高，aux 可学相对知识，main 继续看真实点击；直接让 main 硬拟合未校正概率更可能复制错误基准。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.29755">原论文</a> · <a href="../../../../reproductions/2605.29755-rec-distill/">实现解读</a> · <a href="#qa-480b099c9b0f77c3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rec-distill" data-paper-title="Rec-Distill: An Industrial Distillation Pipeline for Large-Scale Recommendation Models" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Rec-Distill: An Industrial Distillation Pipeline for Large-Scale Recommendation Models 搜广推与 LLM 应用 ByteDance / Douyin / TikTok 2026-05-28 工业大推荐 teacher 无法直接 serving，且 teacher/student 数据采样与实时分布不同。Rec-Distill 让 teacher 在自身 forward 阶段写出黑盒 logits，一份信号可异步服务多个 student。Student 的 main tower 只收真实标签并用于线上；aux tower 同时收 task 与 distillation loss，两者共享 backbone。 Fidelity: 完整核心链路复现。本地实际训练大 teacher 与轻 student，物化 black-box logits，执行 student-side sampling correction、main/aux decoupled towers、batch→streaming 两阶段蒸馏，并在 validation 搜索 loss ratio。本地对照口径：迁移基线是相同日程训练的 Raw Student；实验组是 Rec-Distill Student；NDCG@10 从 0.0039 降至 0.0036，transferability -4.11%。   搜广推 自动研究与高效上线 Rec-Distill 的 transferability 分母很小时，为什么应连 raw student 与 teacher 一起报告？ η 比较学生蒸馏增量占教师可提供增益比例，分母接近零时极不稳定，单比率会夸大波动。teacher 不是线上基线，所有臂训练日程与候选需匹配。来源负 transferability 应如实保留，不能用较低 head share 改称有效迁移。 示意：教师只比学生高极小量，学生微小变化就给很大比率；同时展示三个原始指标，才能看清这不是大量知识成功传递。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ed85a422881b5223">Rec-Distill 的 transferability 分母很小时，为什么应连 raw student 与 teacher 一起报告？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arec-distill">Rec-Distill: An Industrial Distillation Pipeline for Large-Scale Recommendation Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin / TikTok</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>η 比较学生蒸馏增量占教师可提供增益比例，分母接近零时极不稳定，单比率会夸大波动。teacher 不是线上基线，所有臂训练日程与候选需匹配。来源负 transferability 应如实保留，不能用较低 head share 改称有效迁移。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教师只比学生高极小量，学生微小变化就给很大比率；同时展示三个原始指标，才能看清这不是大量知识成功传递。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.29755">原论文</a> · <a href="../../../../reproductions/2605.29755-rec-distill/">实现解读</a> · <a href="#qa-ed85a422881b5223">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:agentic-rec-tune" data-paper-title="AgenticRecTune: Multi-Agent with Self-Evolving Skillhub for Recommendation System Optimization" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="AgenticRecTune: Multi-Agent with Self-Evolving Skillhub for Recommendation System Optimization 搜广推与 LLM 应用 Google / Discover 2026-04-21 推荐系统配置跨召回、融合和重排，人工调节反馈慢且知识难复用。AgenticRecTune 将工作拆成 Actor、Critic、Insight、Skill、Online 五类 agent：生成方案、审查风险、总结洞见、沉淀技能，并从真实实验平台取回反馈形成闭环。 Fidelity: 核心机制复现。本地真正运行三轮 Actor 提案、Critic 评价和 SkillHub 继承，可直接观察每轮候选与冠军。动作空间是本地可执行排序权重，不接 Google 实验排期 API，也不把确定性 validation 评价冒充线上 Agent。本地对照口径：基线为固定手调排序配方，实验组运行三轮 Actor–Critic–SkillHub；NDCG@10 相对 +17.34%。  agent auto-research retrieval ranking reranking 搜广推 自动研究与高效上线 AgenticRecTune 为什么把配置搜索视为跨召回、融合、重排的配方，而非只调一个模型学习率？ 最终推荐由多环节共同决定，一个环节改动可能改变下游候选分布。把配方作为搜索对象才能联合考虑质量、多样性与风险，再由不同职责的 agent 提案、审查和沉淀经验。单个指标上升仍需要对应环节与完整链路的证据。 示意：提高多样性权重会改变最终列表，也可能需要召回补充更多品类；只调精排学习率无法解决候选池根本缺少这些品类的问题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-agentic-rec-tune-8a853675" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9076fec29b4dc03f">AgenticRecTune 为什么把配置搜索视为跨召回、融合、重排的配方，而非只调一个模型学习率？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aagentic-rec-tune">AgenticRecTune: Multi-Agent with Self-Evolving Skillhub for Recommendation System Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / Discover</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最终推荐由多环节共同决定，一个环节改动可能改变下游候选分布。把配方作为搜索对象才能联合考虑质量、多样性与风险，再由不同职责的 agent 提案、审查和沉淀经验。单个指标上升仍需要对应环节与完整链路的证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>提高多样性权重会改变最终列表，也可能需要召回补充更多品类；只调精排学习率无法解决候选池根本缺少这些品类的问题。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.26969">原论文</a> · <a href="../../../../reproductions/2604.26969-agentic-rec-tune/">实现解读</a> · <a href="#qa-9076fec29b4dc03f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:agentic-rec-tune" data-paper-title="AgenticRecTune: Multi-Agent with Self-Evolving Skillhub for Recommendation System Optimization" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="AgenticRecTune: Multi-Agent with Self-Evolving Skillhub for Recommendation System Optimization 搜广推与 LLM 应用 Google / Discover 2026-04-21 推荐系统配置跨召回、融合和重排，人工调节反馈慢且知识难复用。AgenticRecTune 将工作拆成 Actor、Critic、Insight、Skill、Online 五类 agent：生成方案、审查风险、总结洞见、沉淀技能，并从真实实验平台取回反馈形成闭环。 Fidelity: 核心机制复现。本地真正运行三轮 Actor 提案、Critic 评价和 SkillHub 继承，可直接观察每轮候选与冠军。动作空间是本地可执行排序权重，不接 Google 实验排期 API，也不把确定性 validation 评价冒充线上 Agent。本地对照口径：基线为固定手调排序配方，实验组运行三轮 Actor–Critic–SkillHub；NDCG@10 相对 +17.34%。  agent auto-research retrieval ranking reranking 搜广推 自动研究与高效上线 Actor提出了更高分的配置，为什么还需要Critic、SkillHub和真实实验反馈？ 提案只是待执行假设，Critic负责检查候选可行性与风险，真实实验才提供效果证据；Insight与Skill模块把可复用的成功条件和失败原因写回记忆。这样后续搜索能避免重复踩坑，而不是把语言模型的自评分当研究结果。本地配置搜索只支持缩小闭环，晋级必须遵守验证与测试隔离。 示意：Actor建议增加多样性权重，Critic发现延迟预算可能超标；真实运行失败后把失败条件存成技能，下轮便不再无条件复用同一方案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-bf6384e67bb84496">Actor提出了更高分的配置，为什么还需要Critic、SkillHub和真实实验反馈？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aagentic-rec-tune">AgenticRecTune: Multi-Agent with Self-Evolving Skillhub for Recommendation System Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / Discover</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>提案只是待执行假设，Critic负责检查候选可行性与风险，真实实验才提供效果证据；Insight与Skill模块把可复用的成功条件和失败原因写回记忆。这样后续搜索能避免重复踩坑，而不是把语言模型的自评分当研究结果。本地配置搜索只支持缩小闭环，晋级必须遵守验证与测试隔离。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>Actor建议增加多样性权重，Critic发现延迟预算可能超标；真实运行失败后把失败条件存成技能，下轮便不再无条件复用同一方案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.26969">原论文</a> · <a href="../../../../reproductions/2604.26969-agentic-rec-tune/">实现解读</a> · <a href="#qa-bf6384e67bb84496">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:agentic-rec-tune" data-paper-title="AgenticRecTune: Multi-Agent with Self-Evolving Skillhub for Recommendation System Optimization" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="AgenticRecTune: Multi-Agent with Self-Evolving Skillhub for Recommendation System Optimization 搜广推与 LLM 应用 Google / Discover 2026-04-21 推荐系统配置跨召回、融合和重排，人工调节反馈慢且知识难复用。AgenticRecTune 将工作拆成 Actor、Critic、Insight、Skill、Online 五类 agent：生成方案、审查风险、总结洞见、沉淀技能，并从真实实验平台取回反馈形成闭环。 Fidelity: 核心机制复现。本地真正运行三轮 Actor 提案、Critic 评价和 SkillHub 继承，可直接观察每轮候选与冠军。动作空间是本地可执行排序权重，不接 Google 实验排期 API，也不把确定性 validation 评价冒充线上 Agent。本地对照口径：基线为固定手调排序配方，实验组运行三轮 Actor–Critic–SkillHub；NDCG@10 相对 +17.34%。  agent auto-research retrieval ranking reranking 搜广推 自动研究与高效上线 AgenticRecTune 的 SkillHub 与每轮从零调用同一提示词相比，有什么持续学习差别？ 每轮从零容易重复无效尝试，SkillHub 将经过反馈的策略与约束保留为可复用知识，使后续提案基于已有实验。它保存的是可审计经验，并非把任何一次高分都当真；经验能否迁移仍取决于数据与场景相容性。 示意：前轮发现某多样性配置损害新用户相关性，后轮提案可带上这个条件限制；若只是重复旧提示词，agent 可能再次提出同一已失败配置。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-288104c3ee63595c">AgenticRecTune 的 SkillHub 与每轮从零调用同一提示词相比，有什么持续学习差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aagentic-rec-tune">AgenticRecTune: Multi-Agent with Self-Evolving Skillhub for Recommendation System Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / Discover</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每轮从零容易重复无效尝试，SkillHub 将经过反馈的策略与约束保留为可复用知识，使后续提案基于已有实验。它保存的是可审计经验，并非把任何一次高分都当真；经验能否迁移仍取决于数据与场景相容性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>前轮发现某多样性配置损害新用户相关性，后轮提案可带上这个条件限制；若只是重复旧提示词，agent 可能再次提出同一已失败配置。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.26969">原论文</a> · <a href="../../../../reproductions/2604.26969-agentic-rec-tune/">实现解读</a> · <a href="#qa-288104c3ee63595c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:agentic-rec-tune" data-paper-title="AgenticRecTune: Multi-Agent with Self-Evolving Skillhub for Recommendation System Optimization" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="AgenticRecTune: Multi-Agent with Self-Evolving Skillhub for Recommendation System Optimization 搜广推与 LLM 应用 Google / Discover 2026-04-21 推荐系统配置跨召回、融合和重排，人工调节反馈慢且知识难复用。AgenticRecTune 将工作拆成 Actor、Critic、Insight、Skill、Online 五类 agent：生成方案、审查风险、总结洞见、沉淀技能，并从真实实验平台取回反馈形成闭环。 Fidelity: 核心机制复现。本地真正运行三轮 Actor 提案、Critic 评价和 SkillHub 继承，可直接观察每轮候选与冠军。动作空间是本地可执行排序权重，不接 Google 实验排期 API，也不把确定性 validation 评价冒充线上 Agent。本地对照口径：基线为固定手调排序配方，实验组运行三轮 Actor–Critic–SkillHub；NDCG@10 相对 +17.34%。  agent auto-research retrieval ranking reranking 搜广推 自动研究与高效上线 本地 AgenticRecTune 怎样避免让测试集成为三轮配置搜索的调参工具？ 每轮 Actor 产生有限 genome，Critic 仅使用 validation 比较与选择，再把已选结果写入技能或状态。test 留到最终选择完成后评估，不能反复查看再决定下一轮配方。本地只执行有界公开数据搜索，不具备真实实验平台的线上权限。 示意：三轮分别试不同融合权重，都只看验证分；最后确定冠军后才揭开测试结果，即使测试较差，也不能回头用它再挑另一个冠军。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-66fce010d5e556b6">本地 AgenticRecTune 怎样避免让测试集成为三轮配置搜索的调参工具？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aagentic-rec-tune">AgenticRecTune: Multi-Agent with Self-Evolving Skillhub for Recommendation System Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / Discover</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每轮 Actor 产生有限 genome，Critic 仅使用 validation 比较与选择，再把已选结果写入技能或状态。test 留到最终选择完成后评估，不能反复查看再决定下一轮配方。本地只执行有界公开数据搜索，不具备真实实验平台的线上权限。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三轮分别试不同融合权重，都只看验证分；最后确定冠军后才揭开测试结果，即使测试较差，也不能回头用它再挑另一个冠军。</p>
<p class="ar-learning-sources">依据：背景与主要改动、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.26969">原论文</a> · <a href="../../../../reproductions/2604.26969-agentic-rec-tune/">实现解读</a> · <a href="#qa-66fce010d5e556b6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:solaris" data-paper-title="SOLARIS: Speculative Offloading of Latent-bAsed Representation for Inference Scaling" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="SOLARIS: Speculative Offloading of Latent-bAsed Representation for Inference Scaling 搜广推与 LLM 应用 Meta 2026-04-13 大推荐模型在请求时为全部 user-item 对计算 latent 不现实。SOLARIS 先预测未来会访问的 pair，异步用 foundation model 预计算并缓存 latent；请求命中 cache 直接消费，未命中走 fallback。 复现保真度：核心机制复现。复现保真度：核心机制复现。Future-pair predictor、异步 cache 与 fallback 均实际执行。用未来三步交互训练 pair predictor，只缓存高置信 pair，并测量 cache 覆盖与 fallback 路径。  foundation-model serving latent-cache 搜广推 自动研究与高效上线 SOLARIS为什么预测未来user-item pair再算latent？ 请求时全配对大模型计算太贵，先预测可能访问的pair，异步预计算，使在线命中只需轻量消费。预测不准会浪费预算，未命中仍需fallback。 例如提前准备用户可能看的几条内容表示，而不对全目录每项都算大模型。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-solaris-6dc852c5" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-91c05cfa4ac73637">SOLARIS为什么预测未来user-item pair再算latent？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asolaris">SOLARIS: Speculative Offloading of Latent-bAsed Representation for Inference Scaling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>请求时全配对大模型计算太贵，先预测可能访问的pair，异步预计算，使在线命中只需轻量消费。预测不准会浪费预算，未命中仍需fallback。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如提前准备用户可能看的几条内容表示，而不对全目录每项都算大模型。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.12110">原论文</a> · <a href="../../../../reproductions/2604.12110-solaris/">实现解读</a> · <a href="#qa-91c05cfa4ac73637">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:solaris" data-paper-title="SOLARIS: Speculative Offloading of Latent-bAsed Representation for Inference Scaling" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="SOLARIS: Speculative Offloading of Latent-bAsed Representation for Inference Scaling 搜广推与 LLM 应用 Meta 2026-04-13 大推荐模型在请求时为全部 user-item 对计算 latent 不现实。SOLARIS 先预测未来会访问的 pair，异步用 foundation model 预计算并缓存 latent；请求命中 cache 直接消费，未命中走 fallback。 复现保真度：核心机制复现。复现保真度：核心机制复现。Future-pair predictor、异步 cache 与 fallback 均实际执行。用未来三步交互训练 pair predictor，只缓存高置信 pair，并测量 cache 覆盖与 fallback 路径。  foundation-model serving latent-cache 搜广推 自动研究与高效上线 SOLARIS 为什么预测未来 user-item pair 后预计算 latent，而不只缓存一个通用用户向量？ 强模型的交互 latent 依赖具体用户与物品，单一用户向量未必保留这种深度配对信息。预测器提前挑可能访问的 pair，异步计算并缓存，再在请求命中时消费，未命中走 fallback。收益取决于覆盖率、时效和预算；未来交互可用于训练预测器，但在线缓存选择不能偷读真实未来答案。 示意：后台预测用户近期可能看到十件商品，先计算这十组深交互。请求出现其中一件时直接用缓存；出现意外商品就走常规路径，而不是假设所有未来候选都已准确知道。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-2fe75d5f35fcadd4">SOLARIS 为什么预测未来 user-item pair 后预计算 latent，而不只缓存一个通用用户向量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asolaris">SOLARIS: Speculative Offloading of Latent-bAsed Representation for Inference Scaling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>强模型的交互 latent 依赖具体用户与物品，单一用户向量未必保留这种深度配对信息。预测器提前挑可能访问的 pair，异步计算并缓存，再在请求命中时消费，未命中走 fallback。收益取决于覆盖率、时效和预算；未来交互可用于训练预测器，但在线缓存选择不能偷读真实未来答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>后台预测用户近期可能看到十件商品，先计算这十组深交互。请求出现其中一件时直接用缓存；出现意外商品就走常规路径，而不是假设所有未来候选都已准确知道。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.12110">原论文</a> · <a href="../../../../reproductions/2604.12110-solaris/">实现解读</a> · <a href="#qa-2fe75d5f35fcadd4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:solaris" data-paper-title="SOLARIS: Speculative Offloading of Latent-bAsed Representation for Inference Scaling" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="SOLARIS: Speculative Offloading of Latent-bAsed Representation for Inference Scaling 搜广推与 LLM 应用 Meta 2026-04-13 大推荐模型在请求时为全部 user-item 对计算 latent 不现实。SOLARIS 先预测未来会访问的 pair，异步用 foundation model 预计算并缓存 latent；请求命中 cache 直接消费，未命中走 fallback。 复现保真度：核心机制复现。复现保真度：核心机制复现。Future-pair predictor、异步 cache 与 fallback 均实际执行。用未来三步交互训练 pair predictor，只缓存高置信 pair，并测量 cache 覆盖与 fallback 路径。  foundation-model serving latent-cache 搜广推 自动研究与高效上线 latent cache与缓存最终排序列表有什么不同？ latent是可供轻量ranker使用的中间特征，可结合当前信息重评分；最终列表缓存固定排序更直接。中间缓存仍有陈旧与版本一致性问题，不是永远有效。 例如同一缓存latent加上当前价格，可得到与昨天不同的最终顺序。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-6b7fcf1178ba1fc0">latent cache与缓存最终排序列表有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asolaris">SOLARIS: Speculative Offloading of Latent-bAsed Representation for Inference Scaling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>latent是可供轻量ranker使用的中间特征，可结合当前信息重评分；最终列表缓存固定排序更直接。中间缓存仍有陈旧与版本一致性问题，不是永远有效。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一缓存latent加上当前价格，可得到与昨天不同的最终顺序。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.12110">原论文</a> · <a href="../../../../reproductions/2604.12110-solaris/">实现解读</a> · <a href="#qa-6b7fcf1178ba1fc0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:solaris" data-paper-title="SOLARIS: Speculative Offloading of Latent-bAsed Representation for Inference Scaling" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="SOLARIS: Speculative Offloading of Latent-bAsed Representation for Inference Scaling 搜广推与 LLM 应用 Meta 2026-04-13 大推荐模型在请求时为全部 user-item 对计算 latent 不现实。SOLARIS 先预测未来会访问的 pair，异步用 foundation model 预计算并缓存 latent；请求命中 cache 直接消费，未命中走 fallback。 复现保真度：核心机制复现。复现保真度：核心机制复现。Future-pair predictor、异步 cache 与 fallback 均实际执行。用未来三步交互训练 pair predictor，只缓存高置信 pair，并测量 cache 覆盖与 fallback 路径。  foundation-model serving latent-cache 搜广推 自动研究与高效上线 SOLARIS cache key需要包含哪些更新语义？ 至少能识别用户物品对、模型与特征版本及有效时间，命中读取与未命中fallback明确。当前抽象路径不证明真实异步服务延迟，不能仅用命中率推断收益。 例如同一pair模型升级后旧latent不应无标记继续当新结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-29504be389624dcd">SOLARIS cache key需要包含哪些更新语义？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asolaris">SOLARIS: Speculative Offloading of Latent-bAsed Representation for Inference Scaling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>至少能识别用户物品对、模型与特征版本及有效时间，命中读取与未命中fallback明确。当前抽象路径不证明真实异步服务延迟，不能仅用命中率推断收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一pair模型升级后旧latent不应无标记继续当新结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.12110">原论文</a> · <a href="../../../../reproductions/2604.12110-solaris/">实现解读</a> · <a href="#qa-29504be389624dcd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ug-sep" data-paper-title="Compute Only Once: UG-Separation for Efficient Large Recommendation Models" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Compute Only Once: UG-Separation for Efficient Large Recommendation Models 搜广推与 LLM 应用 ByteDance AML 2026-02-11 通过注意力/TokenMixer mask 阻断候选向用户 token 的反向信息流，使用户侧表示能在同一请求的多个候选间复用；Information Compensation 额外恢复被 mask 抑制的用户—候选交互。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04934，相对变化 -8.65%。本地代理目标与论文生产任务不同，不能外推线上 lift。  ranking-network inference-efficiency token-mixing 搜广推 自动研究与高效上线 UG-Sep为什么阻断候选回流到用户tokens？ 候选一旦影响用户状态，每个候选就需重算一份用户编码。单向信息流使同请求用户侧可共享，再以Information Compensation补回被隔离的交互，保持计算与表达取舍。 例如同一用户评千个商品，共享的历史状态不应因当前商品不同而变。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-ug-sep-25948e1e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f7cb92de7c9f342c">UG-Sep为什么阻断候选回流到用户tokens？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aug-sep">Compute Only Once: UG-Separation for Efficient Large Recommendation Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance AML</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>候选一旦影响用户状态，每个候选就需重算一份用户编码。单向信息流使同请求用户侧可共享，再以Information Compensation补回被隔离的交互，保持计算与表达取舍。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一用户评千个商品，共享的历史状态不应因当前商品不同而变。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.10455">原论文</a> · <a href="../../../../reproductions/2602.10455-ug-sep/">实现解读</a> · <a href="#qa-f7cb92de7c9f342c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ug-sep" data-paper-title="Compute Only Once: UG-Separation for Efficient Large Recommendation Models" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Compute Only Once: UG-Separation for Efficient Large Recommendation Models 搜广推与 LLM 应用 ByteDance AML 2026-02-11 通过注意力/TokenMixer mask 阻断候选向用户 token 的反向信息流，使用户侧表示能在同一请求的多个候选间复用；Information Compensation 额外恢复被 mask 抑制的用户—候选交互。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04934，相对变化 -8.65%。本地代理目标与论文生产任务不同，不能外推线上 lift。  ranking-network inference-efficiency token-mixing 搜广推 自动研究与高效上线 UG-Sep 为什么先屏蔽候选到用户 token 的反向信息流，再加 Information Compensation？ 用户状态若读过候选就失去跨候选复用资格，掩码先保证用户侧独立计算，从而减少重复开销。但阻断双向交互也可能削弱原模型表达，补偿模块在评分路径恢复必要的用户—候选关系。它保留的是可共享编码与候选专属交互的分工，不能把补偿后的候选状态再次当成公共用户缓存。 示意：先算一份不含商品信息的用户表示供一百个候选共用，再让每件商品单独与它交互补偿。若把商品甲的补偿结果缓存给商品乙，就破坏了最初的隔离条件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8145189206c730cf">UG-Sep 为什么先屏蔽候选到用户 token 的反向信息流，再加 Information Compensation？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aug-sep">Compute Only Once: UG-Separation for Efficient Large Recommendation Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance AML</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用户状态若读过候选就失去跨候选复用资格，掩码先保证用户侧独立计算，从而减少重复开销。但阻断双向交互也可能削弱原模型表达，补偿模块在评分路径恢复必要的用户—候选关系。它保留的是可共享编码与候选专属交互的分工，不能把补偿后的候选状态再次当成公共用户缓存。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先算一份不含商品信息的用户表示供一百个候选共用，再让每件商品单独与它交互补偿。若把商品甲的补偿结果缓存给商品乙，就破坏了最初的隔离条件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.10455">原论文</a> · <a href="../../../../reproductions/2602.10455-ug-sep/">实现解读</a> · <a href="#qa-8145189206c730cf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ug-sep" data-paper-title="Compute Only Once: UG-Separation for Efficient Large Recommendation Models" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Compute Only Once: UG-Separation for Efficient Large Recommendation Models 搜广推与 LLM 应用 ByteDance AML 2026-02-11 通过注意力/TokenMixer mask 阻断候选向用户 token 的反向信息流，使用户侧表示能在同一请求的多个候选间复用；Information Compensation 额外恢复被 mask 抑制的用户—候选交互。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04934，相对变化 -8.65%。本地代理目标与论文生产任务不同，不能外推线上 lift。  ranking-network inference-efficiency token-mixing 搜广推 自动研究与高效上线 用户计算共享与完全取消用户候选交互有什么区别？ 共享只限制用户端被候选改写，候选侧仍能读用户，补偿模块也建模相关交互。若直接双塔独立点积，可能丢掉原本保留的条件交互。 例如不让商品改用户缓存，不表示商品打分不能依用户偏好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ada9a9a1316edf1c">用户计算共享与完全取消用户候选交互有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aug-sep">Compute Only Once: UG-Separation for Efficient Large Recommendation Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance AML</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共享只限制用户端被候选改写，候选侧仍能读用户，补偿模块也建模相关交互。若直接双塔独立点积，可能丢掉原本保留的条件交互。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如不让商品改用户缓存，不表示商品打分不能依用户偏好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.10455">原论文</a> · <a href="../../../../reproductions/2602.10455-ug-sep/">实现解读</a> · <a href="#qa-ada9a9a1316edf1c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ug-sep" data-paper-title="Compute Only Once: UG-Separation for Efficient Large Recommendation Models" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Compute Only Once: UG-Separation for Efficient Large Recommendation Models 搜广推与 LLM 应用 ByteDance AML 2026-02-11 通过注意力/TokenMixer mask 阻断候选向用户 token 的反向信息流，使用户侧表示能在同一请求的多个候选间复用；Information Compensation 额外恢复被 mask 抑制的用户—候选交互。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04934，相对变化 -8.65%。本地代理目标与论文生产任务不同，不能外推线上 lift。  ranking-network inference-efficiency token-mixing 搜广推 自动研究与高效上线 UG-Sep mask如何验证共享是否合法？ 固定用户输入改变候选时，受保护用户表示应保持不变，候选输出可变；attention和TokenMixer路径都要检查。当前公开代理未复刻生产kernel及真实QPS。 例如只对attention加mask而mixer仍回流候选，就不能安全共享用户计算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-da3bf12463f029c9">UG-Sep mask如何验证共享是否合法？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aug-sep">Compute Only Once: UG-Separation for Efficient Large Recommendation Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance AML</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定用户输入改变候选时，受保护用户表示应保持不变，候选输出可变；attention和TokenMixer路径都要检查。当前公开代理未复刻生产kernel及真实QPS。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只对attention加mask而mixer仍回流候选，就不能安全共享用户计算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.10455">原论文</a> · <a href="../../../../reproductions/2602.10455-ug-sep/">实现解读</a> · <a href="#qa-da3bf12463f029c9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:self-evolving-rec" data-paper-title="Self-Evolving Recommendation System: End-To-End Autonomous Model Optimization With LLM Agents" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Self-Evolving Recommendation System: End-To-End Autonomous Model Optimization With LLM Agents 搜广推与 LLM 应用 Google / YouTube 2026-02-10 推荐研发通常依赖人工提出假设、改代码、跑离线实验、申请线上 A/B，再把经验散落在文档里。论文将 Gemini 2.5 放入双层闭环：内层 agent 以 researcher personas、实验 journal、代码/训练工具探索 optimizer、网络结构和 reward；外层状态机负责安全检查、资源约束和真实 A/B promotion，再把线上结论写回记忆，驱动下一轮搜索。 Fidelity: 核心机制复现。本地 SmolLM2-135M-Instruct 实际读取 journal、给可执行配置打分、逐轮提出未尝试方案并接收 validation 反馈；未复刻 Google 生产 A/B 基础设施。本地对照口径：基线是 Human/Adagrad 配置；实验组是本地 LLM agent 经过四代 journal→提案→训练→validation 反馈后晋级的配置，NDCG@10 +2.57%。test 只在晋级完成后运行，不是单一模型相对 DIN。   搜广推 自动研究与高效上线 自演化推荐系统的贡献为什么不只是一个新网络？ 内层agent提出并执行结构、优化器或reward实验，外层状态机管理预算、安全与真实A/B，再把结果写回journal，形成持续学习研发闭环。 例如一次离线失败也记录原因，下一轮研究者据此避免重复尝试。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-self-evolving-rec-3809fcbe" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4b4c2af3f199e061">自演化推荐系统的贡献为什么不只是一个新网络？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aself-evolving-rec">Self-Evolving Recommendation System: End-To-End Autonomous Model Optimization With LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>内层agent提出并执行结构、优化器或reward实验，外层状态机管理预算、安全与真实A/B，再把结果写回journal，形成持续学习研发闭环。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一次离线失败也记录原因，下一轮研究者据此避免重复尝试。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.10226">原论文</a> · <a href="../../../../reproductions/2602.10226-self-evolving-rec/">实现解读</a> · <a href="#qa-4b4c2af3f199e061">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:self-evolving-rec" data-paper-title="Self-Evolving Recommendation System: End-To-End Autonomous Model Optimization With LLM Agents" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Self-Evolving Recommendation System: End-To-End Autonomous Model Optimization With LLM Agents 搜广推与 LLM 应用 Google / YouTube 2026-02-10 推荐研发通常依赖人工提出假设、改代码、跑离线实验、申请线上 A/B，再把经验散落在文档里。论文将 Gemini 2.5 放入双层闭环：内层 agent 以 researcher personas、实验 journal、代码/训练工具探索 optimizer、网络结构和 reward；外层状态机负责安全检查、资源约束和真实 A/B promotion，再把线上结论写回记忆，驱动下一轮搜索。 Fidelity: 核心机制复现。本地 SmolLM2-135M-Instruct 实际读取 journal、给可执行配置打分、逐轮提出未尝试方案并接收 validation 反馈；未复刻 Google 生产 A/B 基础设施。本地对照口径：基线是 Human/Adagrad 配置；实验组是本地 LLM agent 经过四代 journal→提案→训练→validation 反馈后晋级的配置，NDCG@10 +2.57%。test 只在晋级完成后运行，不是单一模型相对 DIN。   搜广推 自动研究与高效上线 Self-Evolving Rec 为什么让内层 agent 探索离线方案，外层状态机才决定真实 A/B 晋级？ 离线代理能便宜筛选优化器、架构与奖励想法，却不完整代表线上用户和服务约束。外层独立管理安全、资源与真实实验晋级，再把结论写回长期 journal，让内层下一轮有证据可用。闭环的价值在实验治理与知识累积，不是 agent 提出方案就自动上线；本地验证循环不能替代真实生产 A/B。 示意：agent 提议一个离线更优但延迟超标的结构，外层先拒绝晋级；另一个通过资源检查再进入真实实验，其结果被记录，避免下一轮重复犯同样错误。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-a0ff42610abe6dfe">Self-Evolving Rec 为什么让内层 agent 探索离线方案，外层状态机才决定真实 A/B 晋级？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aself-evolving-rec">Self-Evolving Recommendation System: End-To-End Autonomous Model Optimization With LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>离线代理能便宜筛选优化器、架构与奖励想法，却不完整代表线上用户和服务约束。外层独立管理安全、资源与真实实验晋级，再把结论写回长期 journal，让内层下一轮有证据可用。闭环的价值在实验治理与知识累积，不是 agent 提出方案就自动上线；本地验证循环不能替代真实生产 A/B。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>agent 提议一个离线更优但延迟超标的结构，外层先拒绝晋级；另一个通过资源检查再进入真实实验，其结果被记录，避免下一轮重复犯同样错误。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.10226">原论文</a> · <a href="../../../../reproductions/2602.10226-self-evolving-rec/">实现解读</a> · <a href="#qa-a0ff42610abe6dfe">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:self-evolving-rec" data-paper-title="Self-Evolving Recommendation System: End-To-End Autonomous Model Optimization With LLM Agents" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Self-Evolving Recommendation System: End-To-End Autonomous Model Optimization With LLM Agents 搜广推与 LLM 应用 Google / YouTube 2026-02-10 推荐研发通常依赖人工提出假设、改代码、跑离线实验、申请线上 A/B，再把经验散落在文档里。论文将 Gemini 2.5 放入双层闭环：内层 agent 以 researcher personas、实验 journal、代码/训练工具探索 optimizer、网络结构和 reward；外层状态机负责安全检查、资源约束和真实 A/B promotion，再把线上结论写回记忆，驱动下一轮搜索。 Fidelity: 核心机制复现。本地 SmolLM2-135M-Instruct 实际读取 journal、给可执行配置打分、逐轮提出未尝试方案并接收 validation 反馈；未复刻 Google 生产 A/B 基础设施。本地对照口径：基线是 Human/Adagrad 配置；实验组是本地 LLM agent 经过四代 journal→提案→训练→validation 反馈后晋级的配置，NDCG@10 +2.57%。test 只在晋级完成后运行，不是单一模型相对 DIN。   搜广推 自动研究与高效上线 离线proxy通过与真实online promotion有什么区别？ 离线表现只是候选门，外层还要求线上实验、统计和guardrails。模型自己判断成功不能替代生产证据，结构登记也不等于工具能真实训练和评估。 例如离线命中提高，线上时延超预算仍不应自动发布。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-937788d1136b4b7b">离线proxy通过与真实online promotion有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aself-evolving-rec">Self-Evolving Recommendation System: End-To-End Autonomous Model Optimization With LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>离线表现只是候选门，外层还要求线上实验、统计和guardrails。模型自己判断成功不能替代生产证据，结构登记也不等于工具能真实训练和评估。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如离线命中提高，线上时延超预算仍不应自动发布。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.10226">原论文</a> · <a href="../../../../reproductions/2602.10226-self-evolving-rec/">实现解读</a> · <a href="#qa-937788d1136b4b7b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:self-evolving-rec" data-paper-title="Self-Evolving Recommendation System: End-To-End Autonomous Model Optimization With LLM Agents" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Self-Evolving Recommendation System: End-To-End Autonomous Model Optimization With LLM Agents 搜广推与 LLM 应用 Google / YouTube 2026-02-10 推荐研发通常依赖人工提出假设、改代码、跑离线实验、申请线上 A/B，再把经验散落在文档里。论文将 Gemini 2.5 放入双层闭环：内层 agent 以 researcher personas、实验 journal、代码/训练工具探索 optimizer、网络结构和 reward；外层状态机负责安全检查、资源约束和真实 A/B promotion，再把线上结论写回记忆，驱动下一轮搜索。 Fidelity: 核心机制复现。本地 SmolLM2-135M-Instruct 实际读取 journal、给可执行配置打分、逐轮提出未尝试方案并接收 validation 反馈；未复刻 Google 生产 A/B 基础设施。本地对照口径：基线是 Human/Adagrad 配置；实验组是本地 LLM agent 经过四代 journal→提案→训练→validation 反馈后晋级的配置，NDCG@10 +2.57%。test 只在晋级完成后运行，不是单一模型相对 DIN。   搜广推 自动研究与高效上线 本地要怎样才可称演化算子真正接入？ 控制器必须实际调用生成的改动、训练并在隔离验证上评价，状态和journal可追溯。仅registry名称或模拟计划不算执行，更不能伪称已跑真实A/B。 例如agent写好优化器建议但工具不能运行，就仍是提案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6726a7bb82861a54">本地要怎样才可称演化算子真正接入？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aself-evolving-rec">Self-Evolving Recommendation System: End-To-End Autonomous Model Optimization With LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>控制器必须实际调用生成的改动、训练并在隔离验证上评价，状态和journal可追溯。仅registry名称或模拟计划不算执行，更不能伪称已跑真实A/B。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如agent写好优化器建议但工具不能运行，就仍是提案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.10226">原论文</a> · <a href="../../../../reproductions/2602.10226-self-evolving-rec/">实现解读</a> · <a href="#qa-6726a7bb82861a54">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:radar" data-paper-title="RADAR: Recall Augmentation through Deferred Asynchronous Retrieval" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="RADAR: Recall Augmentation through Deferred Asynchronous Retrieval 搜广推与 LLM 应用 Meta 2025-06-08 将完整排序模型在本次请求后异步运行，把高价值结果缓存为下一次请求的召回补充，再与实时召回合并。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 radar 核心机制；相对 NDCG@10 -2.78%。  retrieval asynchronous-serving ranking 搜广推 自动研究与高效上线 RADAR 为什么将强排序器输出作为召回候选，而不是只用于最终重排？ 强排序器可在请求后异步看更大目录，找到普通实时召回漏掉的高价值项，下次作为补充候选，提前提升覆盖。末端重排只能处理已有项。缓存依据旧历史会陈旧，实时通道仍负责新需求，不能当当前全库最优。 示意：后台发现一部用户可能爱看的冷门片，下次加入召回池；若只在最终排序使用强模型，该片从未召回就永远无机会。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-radar-206d8edd" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-bfe5d1773a5c7047">RADAR 为什么将强排序器输出作为召回候选，而不是只用于最终重排？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aradar">RADAR: Recall Augmentation through Deferred Asynchronous Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>强排序器可在请求后异步看更大目录，找到普通实时召回漏掉的高价值项，下次作为补充候选，提前提升覆盖。末端重排只能处理已有项。缓存依据旧历史会陈旧，实时通道仍负责新需求，不能当当前全库最优。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>后台发现一部用户可能爱看的冷门片，下次加入召回池；若只在最终排序使用强模型，该片从未召回就永远无机会。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2506.07261">原论文</a> · <a href="../../../../reproductions/2506.07261-radar/">实现解读</a> · <a href="#qa-bfe5d1773a5c7047">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:radar" data-paper-title="RADAR: Recall Augmentation through Deferred Asynchronous Retrieval" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="RADAR: Recall Augmentation through Deferred Asynchronous Retrieval 搜广推与 LLM 应用 Meta 2025-06-08 将完整排序模型在本次请求后异步运行，把高价值结果缓存为下一次请求的召回补充，再与实时召回合并。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 radar 核心机制；相对 NDCG@10 -2.78%。  retrieval asynchronous-serving ranking 搜广推 自动研究与高效上线 RADAR 为什么把本次请求后异步运行的排序结果，用作下一次请求的召回补充？ 完整排序器通常比召回器表达更强，却无法在实时请求中遍历全部物品。RADAR 把昂贵全库计算移到请求后，缓存高价值结果，下次与实时召回合并，使排序知识提前影响候选覆盖。代价是缓存依据上一时刻历史，可能变旧，因此需要实时通道补充新意图，不能把异步结果当作当前请求的完整最优答案。 示意：用户看完一次推荐后，后台用完整模型筛出一批可能喜欢的电影。下次打开时直接把这批加入候选，同时实时召回根据刚发生的新点击补充变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f22b0db4a797c31d">RADAR 为什么把本次请求后异步运行的排序结果，用作下一次请求的召回补充？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aradar">RADAR: Recall Augmentation through Deferred Asynchronous Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>完整排序器通常比召回器表达更强，却无法在实时请求中遍历全部物品。RADAR 把昂贵全库计算移到请求后，缓存高价值结果，下次与实时召回合并，使排序知识提前影响候选覆盖。代价是缓存依据上一时刻历史，可能变旧，因此需要实时通道补充新意图，不能把异步结果当作当前请求的完整最优答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户看完一次推荐后，后台用完整模型筛出一批可能喜欢的电影。下次打开时直接把这批加入候选，同时实时召回根据刚发生的新点击补充变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2506.07261">原论文</a> · <a href="../../../../reproductions/2506.07261-radar/">实现解读</a> · <a href="#qa-f22b0db4a797c31d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:radar" data-paper-title="RADAR: Recall Augmentation through Deferred Asynchronous Retrieval" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="RADAR: Recall Augmentation through Deferred Asynchronous Retrieval 搜广推与 LLM 应用 Meta 2025-06-08 将完整排序模型在本次请求后异步运行，把高价值结果缓存为下一次请求的召回补充，再与实时召回合并。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 radar 核心机制；相对 NDCG@10 -2.78%。  retrieval asynchronous-serving ranking 搜广推 自动研究与高效上线 RADAR 的上一请求缓存与预测未来 pair latent 的缓存，复用对象有何不同？ RADAR 保存上一历史条件下筛出的候选结果，pair latent 方法预计算特定用户物品的深交互状态。两者都异步但对象、命中与失效条件不同，不能用一个缓存命中率替代另一方案成本。机制差别本身不支持效果排名。 示意：缓存一张电影名单与缓存用户对每部电影的中间向量不同；新请求可复用名单提名，但仍可能需要重新评分当前价值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f162747603870018">RADAR 的上一请求缓存与预测未来 pair latent 的缓存，复用对象有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aradar">RADAR: Recall Augmentation through Deferred Asynchronous Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>RADAR 保存上一历史条件下筛出的候选结果，pair latent 方法预计算特定用户物品的深交互状态。两者都异步但对象、命中与失效条件不同，不能用一个缓存命中率替代另一方案成本。机制差别本身不支持效果排名。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>缓存一张电影名单与缓存用户对每部电影的中间向量不同；新请求可复用名单提名，但仍可能需要重新评分当前价值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2506.07261">原论文</a> · <a href="../../../../reproductions/2506.07261-radar/">实现解读</a> · <a href="#qa-f162747603870018">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:radar" data-paper-title="RADAR: Recall Augmentation through Deferred Asynchronous Retrieval" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="RADAR: Recall Augmentation through Deferred Asynchronous Retrieval 搜广推与 LLM 应用 Meta 2025-06-08 将完整排序模型在本次请求后异步运行，把高价值结果缓存为下一次请求的召回补充，再与实时召回合并。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 radar 核心机制；相对 NDCG@10 -2.78%。  retrieval asynchronous-serving ranking 搜广推 自动研究与高效上线 RADAR 合并 live 与 cached Top-K 时，为什么必须去重并检查当前资格？ 缓存中物品可能已下架、被消费或资格变化，旧高分不能绕过当前规则；合并要按身份去重，保留来源便于测补充贡献。缓存生成时间与历史截止也需记录，不能让下一次真实目标提前进入异步任务。 示意：昨天预选的房源今天已满，仍应过滤；同一电影被两路召回也只算一个候选，不能靠重复项虚增覆盖与命中。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-10c293e7dee1f7e0">RADAR 合并 live 与 cached Top-K 时，为什么必须去重并检查当前资格？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aradar">RADAR: Recall Augmentation through Deferred Asynchronous Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>缓存中物品可能已下架、被消费或资格变化，旧高分不能绕过当前规则；合并要按身份去重，保留来源便于测补充贡献。缓存生成时间与历史截止也需记录，不能让下一次真实目标提前进入异步任务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>昨天预选的房源今天已满，仍应过滤；同一电影被两路召回也只算一个候选，不能靠重复项虚增覆盖与命中。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2506.07261">原论文</a> · <a href="../../../../reproductions/2506.07261-radar/">实现解读</a> · <a href="#qa-10c293e7dee1f7e0">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

一个离线更好的方案，怎样才算在真实请求和持续迭代中可用？

## 记住这一点

成本可以沿计算路径重新分配：蒸馏把大teacher知识交给轻student，共享请求状态减少多候选重复编码，异步缓存把计算移出实时链路。自动研究则把假设、执行、验证和结论记入闭环；提出一个方案与实际跑通并评估它是两件事。共同要求是用可核验的执行与独立评价连接研究和服务。

## 一个例子

理想化算例：一次用户编码耗2毫秒，每个候选交互0.02毫秒，100个候选若重复编码需约202毫秒，编码一次再逐候选交互约4毫秒。实际收益还受并行、缓存、带宽和算子开销影响，不能直接当生产加速比。

## 什么时候要小心

轻student必须与相同训练日程的student比较，不能用teacher更强来证明蒸馏成功。进程内计时不代表GPU集群吞吐；自动搜索只能用validation做选择，成本过高而终止复现的资料不能被重新当成可执行候选。

## 先读这几篇

先读Rec-Distill理解训练与服务之间的迁移，再读ROCS理解请求内复用条件，最后读Self-Evolving RecSys把候选执行、validation选择与日志反馈连成闭环；本地均有可执行机制，生产服务和A/B仍是各自边界。

1. [Rec-Distill: An Industrial Distillation Pipeline for Large-Scale Recommendation Models](../../../reproductions/2605.29755-rec-distill/README.md) · [原论文](https://arxiv.org/abs/2605.29755)
2. [ROCS: Request-Oriented Compute Sharing for Efficient Large-Scale Recommendation](../../../reproductions/2607.27744-rocs/README.md) · [原论文](https://arxiv.org/abs/2607.27744)
3. [Self-Evolving Recommendation System: End-To-End Autonomous Model Optimization With LLM Agents](../../../reproductions/2602.10226-self-evolving-rec/README.md) · [原论文](https://arxiv.org/abs/2602.10226)

## 自测一下

Agent给一个注册表写入新算子名，但控制器无法执行或评价它，是否已经完成研究闭环？

??? note "展开参考答案"

    没有。至少要能构造候选、实际执行对应路径、得到可比较的验证结果并记录失败与边界；只有名称或提案无法成为改进证据。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
