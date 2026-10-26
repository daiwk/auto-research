---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 自动研究与高效上线

[搜广推](index.md) / 19 个问题 · 19 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">19 个问题 · 19 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:forte" data-paper-title="FORTE: A Production Framework for Feature Evaluation and Deprecation in Industrial Recommender Systems" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="FORTE: A Production Framework for Feature Evaluation and Deprecation in Industrial Recommender Systems 搜广推与 LLM 应用 Pinterest 2026-10-09 添加一个特征只需在某项指标上有收益，删除却不能损伤任何业务指标，而且同一个特征可能有多个模型消费者。FORTE 将退役流程拆成逐渐昂贵的门槛：先每天衡量冻结模型的特征依赖，检查长期稳定性，再联合扰动候选集合并真实重训，最后做线上实验和所有消费者的血缘审计。它不是单次 feature selection，也不能把单特征收益相加当成联合删除效果。一个特征单独看没有价值，可能与另一个冗余特征共同承载重要信号；不同输出头也可能给出相反方向。 结果仍是诊断，不能宣称复现 Pinterest 能力或吞吐收益。L2 公开数据训练，核心机制实现；结果仍是诊断，不能宣称复现 Pinterest 能力或吞吐收益。未复刻私有多模态特征、DCNv2/MMoE 大型 Pin Ranker、分布式 actor、每日生产 checkpoint sensors、线上 A/B 和实际基础设施移除。没有通过任一门槛也是有效结果，保留而不伪造通过。加载经过固定 archive SHA-256 校验的公开 MovieLens-100K。按 timestamp、user、item 排序，chronological 80/10/10；  features efficiency feature-deprecation 搜广推 自动研究与高效上线 两个特征各自删除都几乎不掉分，FORTE为什么仍要求联合扰动、重训和消费者审计？ 单特征扰动衡量的是其余信号仍存在时的依赖，两个冗余特征可能互相补偿，同时删除才暴露损失。FORTE先检查跨时间、跨输出头的稳定弱依赖，再逐级做联合扰动和真实重训；最终还要确认所有下游消费者均可退役，不能把某个模型的一次零损失当全链路删除许可。 示意：用户年龄和年龄分桶互相替代，单删一个不掉分；同时删除可能伤害新用户任务，因此还需检查其他输出头与消费它的模型。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-forte-d5b8210d" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:effective-training-time" data-paper-title="Optimizing Effective Training Time for Large-Scale Recommendation Systems" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Optimizing Effective Training Time for Large-Scale Recommendation Systems 搜广推与 LLM 应用 Meta Platforms, Inc. 2026-10-01 把端到端 wall time 分为真正消费新数据的训练时间与初始化、编译、checkpoint、发布和恢复等生命周期损耗，再按 owner 定位和优化。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 ETT 分解与 owner loss 归因；这是用户批准的生产基础设施例外，不声称推荐模型效果或线上 A/B 收益。收录例外：用户于 2026-10-02 明确批准的生产训练基础设施例外；部署指标是 ETT，不作为推荐模型效果或线上 A/B 收益。执行 ETT 分解与 owner loss 归因；这是用户批准的生产基础设施例外，不声称推荐模型效果或线上 A/B 收益。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  training-systems effective-training-time gpu-fleet 搜广推 自动研究与高效上线 GPU已经满负荷运行，为什么Effective Training Time仍可能很低？ ETT关注总生命周期里真正用于消费新数据的训练时间占比，初始化、编译、保存、发布和故障恢复都会拉长分母。提高单步算子效率只优化其中一段，不能自动消除其他停顿；应先按阶段和负责方定位时间损耗。本地只有生命周期状态诊断，不能据此推算生产集群收益。 示意：一小时中20分钟训练新数据，40分钟反复编译和恢复，即使训练时GPU很忙，ETT仍只有约三分之一；应先减少生命周期损耗。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-effective-training-time-8fded34e" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:evoskillrec" data-paper-title="EvoSkillRec: Skill-Genome Evolution for Recommender Architecture Discovery" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="EvoSkillRec: Skill-Genome Evolution for Recommender Architecture Discovery 搜广推与 LLM 应用 City University of Hong Kong 2026-09-28 把推荐网络拆成带输入输出类型的可执行 skill genome；控制器在约束空间组合技能，只有通过 validation 的创新才晋级并进入后续复用库。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 typed genome、validation evaluator、promotion 与 reuse；未调用外部 LLM 发明任意代码，也不复述论文大规模搜索收益。执行 typed genome、validation evaluator、promotion 与 reuse；未调用外部 LLM 发明任意代码，也不复述论文大规模搜索收益。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  recommendation-auto-evolution architecture-search skill-genome 搜广推 自动研究与高效上线 Skill genome为什么必须检查相邻技能输入输出类型，而不能任意拼接高分模块？ 单个模块有效不代表组合后语义与形状兼容，类型合同先排除无法执行的技能链。控制器随后实际构造候选、评估validation，并只把超过晋级门槛的组合写入复用库。注册一个名称或通过类型检查都不等于完成集成；本地三种子只检查组合与状态转换，不是正式能力排名。 示意：输出item向量的技能不能直接接一个要求完整行为序列的技能；即使两者各自得分高，也要先有正确适配，再验证组合是否保留预期语义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-evoskillrec-7ef949da" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:evopilot" data-paper-title="Verify, Don&#x27;t Trust: Agentic Model Development for Video Discovery Retrieval at Scale" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Verify, Don&#x27;t Trust: Agentic Model Development for Video Discovery Retrieval at Scale 搜广推与 LLM 应用 Meta Platforms 2026-09-18 EvoPilot 不把“某个训练任务完成”直接当成研究证据，而把控制组与实验组的匹配比较作为证据单元。协议固定 shared base、数据版本、评测器、有效输出深度和唯一允许变化的 treatment；执行结束后，从产物读取实际状态并 fail closed，最后仍需人工审核才能接纳结论。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地复现的是 EvoPilot 的比较协议与 fail-closed 验证器，并在同一 MovieLens 切分上运行匹配的交互头对照；不是 Meta VDD 生产系统复刻。公开 MovieLens 上执行比较协议、artifact attestation、fail-closed pair verifier 与 validation-only 交互头对照；不复刻 Meta VDD 私有视频日志、百亿级索引、远程工作流或线上流量。  autoresearch experiment-verification video-retrieval 搜广推 自动研究与高效上线 EvoPilot为什么把匹配的两臂比较，而不是一个成功训练任务，作为证据单元？ 单臂任务完成只能证明产物出现，无法说明提升来自哪项改动。EvoPilot固定共同基座、数据、评测器和输出深度，只允许批准的treatment不同，再从实际产物核对终态与来源；任一额外差异都会拒收。协议校验通过也可能得到负结果，它不是质量收益或上线许可的替代品。 示意：实验组换了交互层，同时多训一倍步数，即使分数更高也不能只归功于交互层；需要先恢复匹配预算，再接纳这对比较作为证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-evopilot-795a30ed" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:autolr" data-paper-title="AutoLR: Automating the Path from Research to Launch Review in Industrial Recommender Systems" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="AutoLR: Automating the Path from Research to Launch Review in Industrial Recommender Systems 搜广推与 LLM 应用 NetEase, Inc. 2026-09-04 AutoLR 将论文调研、方案辩论、代码实验、离线评估、A/B 测试与 Launch Review 串成长期状态机。LLM 负责语义推理和代码生成，确定性控制器保留预算分配、指标抽取、护栏和状态迁移权，防止噪声结果在 KEEP 链中被不断放大。 复现级别：离线控制器核心。复现级别：离线控制器核心。对输入候选与评审执行预算排序、独立指标门槛、持久化账本和人工评审打包；不包含实时 LLM 调研、自动代码生成或线上发布。论文生产代码与 DASHEN 数据未公开；模型只能选择白名单参数，不能注入命令或任意代码。当前实现是受控的离线自动研究闭环，不声称自主创新架构或具备自动发布权限。真实 Qwen checkpoint 已在公开 Amazon Beauty 2014 5-core 上完成三轮有界研究：每轮动态生成参数提案，分别调用两个 reviewer，再执行一轮真实反向传播验证和完整 validation 训练。  auto-research experiment-controller launch-review industrial-recommendation 搜广推 自动研究与高效上线 AutoLR为什么不让LLM直接把自认为最好的方案写成长期冠军？ 提案和讨论含有噪声，若每轮凭语言判断KEEP，错误会沿持久状态累积。AutoLR把语义推理交给LLM，却把预算、指标提取、护栏与状态迁移留给确定性控制器；只有通过对应实验门槛的证据才能更新冠军。一次代理指标胜出也不能绕过后续A/B与Launch Review。 示意：模型建议一种新优化器，但离线收益不稳定；控制器记录提案和失败而保留旧冠军，避免下轮把未验证方案当成已经成立的基线。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-autolr-f0e06ba6" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:coral" data-paper-title="CORAL: An LLM-Native Harness for Production Recommender Systems" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="CORAL: An LLM-Native Harness for Production Recommender Systems 搜广推与 LLM 应用 Meta AI 2026-09-02 CORAL 把推荐优化建模为连续闭环：LLM 根据目标、预算和最近实验记忆生成结构化配置，执行系统验证约束并运行实验，再把观测结果写回下一轮上下文。与一次性自动调参相比，它强调可执行约束、短记忆和生产反馈。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。实现有预算约束的配置提案、短期实验记忆、效果反馈与下一轮更新。未接入 Meta 私有遥测、生产 LLM、实验平台或线上流量；实现可作为推荐 Evolve 的控制器算子组合使用。在 MovieLens 100K 上执行五轮预算分配、三轮记忆和 validation-only blend；三 seed 产物见 metrics/public-seeds42-44.json。该结果只验证控制器闭环和约束可执行性，不把公开小数据效果等同于 Meta 线上因果增益。  auto-research agent retrieval-budget constrained-optimization 搜广推 自动研究与高效上线 CORAL为什么把配置投影到预算可行域，并只保留最近几轮实验记忆？ 语言模型可能提出超配额或负数预算，投影先让配置成为可执行候选，再用真实实验反馈修正下一轮。有限近期记忆帮助适应系统变化，避免旧结论无限堆积干扰决策。记忆短不代表可以丢掉可审计历史，且提案经预算修正后仍需验证，不能把可行性误当成质量提升。 示意：模型把三路召回预算都加大，合计超过请求上限；先重新分配到允许总量，再运行实验。若近期流量分布变了，旧的最优配方也不应自动占优。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-coral-3b3ed34a" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recharness" data-paper-title="RecHarness: A Bandit-Routed Agentic Harness for Self-Evolving Recommender Systems" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="RecHarness: A Bandit-Routed Agentic Harness for Self-Evolving Recommender Systems 搜广推与 LLM 应用 Huazhong Agricultural University (Kuaishou internship) 2026-07-31 将结构改造定义为有限 arm，用 bandit 根据历史收益和不确定性分配试验预算，再把胜者反馈写回下一轮候选。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  auto-research bandit ranking 搜广推 自动研究与高效上线 RecHarness 的 bandit 为什么同时看历史收益与不确定性分配实验，而不总选当前最好结构？ 总选当前平均收益最高的结构会过早放弃样本少但可能更好的方向。置信上界在估计收益上加入与试验次数有关的探索项，让不确定 arm 获得预算，再把胜者反馈用于后续候选。它优化的是有限实验资源分配，不保证找到全局最优架构；收益估计也必须遵守相同验证协议。 示意：结构甲已测十次、均值略高，结构乙只测一次。bandit 可给乙额外机会确认潜力，而不是永远重复甲；但最后仍应在独立测试集评估选中的结构。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-recharness-7341e5ce" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rocs" data-paper-title="ROCS: Request-Oriented Compute Sharing for Efficient Large-Scale Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="ROCS: Request-Oriented Compute Sharing for Efficient Large-Scale Recommendation 搜广推与 LLM 应用 Meta AI 2026-07-30 一次推荐请求会评分大量候选，而用户侧特征完全相同。ROCS 通过 Generalized Layer Masking 保持候选隔离，用 Deep Cross Attention 延迟交互，再由 IKBO 在 GPU kernel 内广播 request 表示。 Fidelity: 核心机制复现。实现一次 request encoding、延迟 candidate interaction 和批量候选评分。未复刻生产 GLM、IKBO CUDA kernel、Meta 私有模型与集群。本地对照口径：基线为逐候选重复编码；实验组为 ROCS core，相对基线 NDCG@10 +8.19%。  retrieval ranking serving compute-sharing 搜广推 自动研究与高效上线 ROCS 为什么需要候选隔离掩码，才能安全地把用户侧计算从逐候选重复中拿出来？ 若用户状态在某层已读取某个候选，就不能作为其他候选通用的缓存。Generalized Layer Masking 约束信息流保持隔离，Deep Cross Attention 延后候选交互，才允许请求表示只算一次。内核广播进一步减少复制成本；本地进程内微基准只反映重复编码与共享的路径差异，不能冒充完整生产吞吐提升。 示意：同一用户评一百件商品，用户主干先保持候选无关，再广播给各商品分支。若商品甲先写进用户表示，商品乙再复用它，得分就会被不该看到的候选污染。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-rocs-28113d9d" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:memory-layer" data-paper-title="Memory Layer: Train the In-Model Cache for Recommendation Models" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Memory Layer: Train the In-Model Cache for Recommendation Models 搜广推与 LLM 应用 Meta / Instagram Reels 2026-07-27 传统 early-stage ranker 在训练时用 item tower 的新鲜输出，服务时却读另一个流程预计算并发布的 item cache；cache miss 还会绕过正常模型。这造成训练、离线评测和线上服务看到三套不同表征。Memory Layer 把 cache 变成模型自身的稀疏参数表：item tower 在训练中写入，后续网络和服务共同读取；作者、topic 等 always-on 属性则保证新内容或 cache miss 仍可评分。 seed 42 的 NDCG@10 相对基线约 +4.36%，结构诊断而非公开小数据 lift 是本复现重点。Fidelity: 核心机制复现。本地实现训练内 item-tower 写回、共享 cache 读取、冻结外部快照对照和 always-on cache-miss fallback；不把普通 embedding lookup 冒充 Meta 的 MPZCH 基础设施。MovieLens 没有媒体创建时间、Instagram 冷启动曝光与线上 NE，因此不能验证论文业务 lift。  ranking training-serving-consistency cold-start cache serving 搜广推 自动研究与高效上线 Memory Layer为什么把item cache做成模型内稀疏参数表，而不继续用独立发布的外部缓存？ 训练用新鲜item塔输出、服务读旧缓存会造成表征错位，miss时走旁路又产生第三种分布。模型内写回与读取让后续网络在训练中就适应缓存语义，always-on属性还保证未命中项可评分。它改变的是数据依赖与训练服务一致性，不意味着缓存永远最新或外部读取完全没有开销。 示意：某商品训练时有新向量，上线却读到昨日旧值；把缓存纳入模型读取路径可让训练见到相同机制，缺失时仍用作者或主题等通用属性打分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-memory-layer-0d31a0b7" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recevolve" data-paper-title="RecEvolve: A Knowledge-Driven Autonomous Agent System for Recommender Systems" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="RecEvolve: A Knowledge-Driven Autonomous Agent System for Recommender Systems 搜广推与 LLM 应用 Google 2026-07-20 RecEvolve 让研究 Agent 从实验知识库提出模型变体，以独立验证集选择冠军，并用版本化状态支持失败回滚。系统显式防止通过极端温度等方式“刷指标”，让上一轮结论成为下一轮可审计的研究知识。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。实现提案、critic gate、隔离试验、冠军继承、回滚与 reward-hack 拒绝。未复刻 Google 私有日志、TPU 集群、生产 coding-agent 工具链和线上实验归因；该 adapter 作为推荐 Evolve 的统一多轮控制器算子。MovieLens 100K 上用固定候选空间执行完整研究控制流；三 seed 结果见 metrics/public-seeds42-44.json。本地指标用于比较同一公开协议下的控制策略，不复刻 Google 私有 Two-Tower 数值。  auto-research agent two-tower reward-hacking 搜广推 自动研究与高效上线 RecEvolve 为什么把候选门控、独立验证集选择和版本回滚放在研究 agent 外围？ 研究 agent 能生成结构改动，也可能提出只对某个指标投机的配置。外部门控先拒绝违规候选，再用独立验证效用与当前冠军比较，只有真实改善才原子更新版本，失败则回滚并记录知识。它把“提出想法”与“接受证据”分开；测试集不能参与冠军选择，否则循环会逐步过拟合最终评估。 示意：agent 提议极低温度让分布异常尖锐，门控先检查是否合法；另一个结构能运行但验证集更差，就保留旧冠军，并把失败原因记入下轮实验知识。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-recevolve-55072983" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:prompt-generation" data-paper-title="Prompt Generation Technical Report" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Prompt Generation Technical Report 搜广推与 LLM 应用 Alibaba / Taobao Search 2026-07-13 生成式检索把 query、用户行为和异构特征输入 LLM，再直接生成商品或文档 SID。工业系统的问题不只是模型效果：每次加特征都要同步修改数据、训练和 serving，容易产生 training-serving skew；长文本和行为序列又会迅速放大 token 数与延迟。PG 用 prompt_template.json 与 prompt_feature.json 把特征工程从模型代码中解耦。 Fidelity: 核心机制复现。本地实际执行论文同款 Qwen2.5-0.5B、MiniOneRec Amazon Office 数据与官方三段式 SID、双 JSON 单一事实源、text/embedding/combo/sequence 四类特征、preprocessor/projector/merger 组件协议、embedding-space mean merger、LoRA SFT、validation 配置选择和 held-out 候选评分。未复刻淘宝全量训练、C++ batched kernels、线上 event replay 和生产 serving。  llm-recommendation generative-retrieval autoresearch serving 搜广推 自动研究与高效上线 Prompt Generation 的 preprocessor、projector、merger 为什么要与模板一起配置化？ 新增特征往往同时涉及离线数据处理和在线输入组装，分别写代码容易产生训练服务偏差。统一协议把清洗、空间投影与融合压缩拆为可组合部件，让训练和服务解释同一份配置。merger 还控制 token 数，因此它影响延迟与信息损失，不只是文本拼接工具；均值压缩的强基线也不意味着所有顺序信息都可丢弃。 示意：给检索器新增商品标题，配置声明文本清洗、向量投影和均值压缩后，训练与服务都产出同样的一个 token。若两边各自实现，一边截十词另一边读全文就会偏离。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-prompt-generation-d1640558" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:nova" data-paper-title="NOVA: A Verification-Aware Agent Harness for Architecture Evolution in Industrial Recommender Systems" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="NOVA: A Verification-Aware Agent Harness for Architecture Evolution in Industrial Recommender Systems 搜广推与 LLM 应用 Tencent 2026-06-25 普通代码 agent 只能证明代码“能跑”，无法阻止结构语义错误和静默负向。NOVA 用 architecture gradient 汇总历史修改、验证诊断和指标反馈，再通过 L1 结构语义、L2 可执行、L3 离线有效、L4 在线影响的级联验证逐级放行，高风险任务交给人工。 复现保真度：核心机制复现。复现保真度：核心机制复现。四级验证、失败方向记忆和 architecture gradient 均实际执行；腾讯生产 agent 与线上灰度未复刻。在 MovieLens 100K 上生成 transition、content、popularity 和故意错误的 shape 候选，真实执行四级验证并只用 validation 选候选；通用 evolve 还会把验证记录、成功技能和禁止方向写入 result.json。  auto-research architecture-evolution verification 搜广推 自动研究与高效上线 NOVA 为什么把架构修改验证拆成结构语义、可执行、离线有效和在线影响四层？ 代码能运行只排除了部分执行错误，不能说明架构仍符合设计，也不能说明指标或线上效果变好。NOVA 将历史修改与诊断反馈汇总为架构更新依据，再按成本递增的验证层级放行，让明显错误尽早退出。离线通过仍需独立的在线证据；本地可执行级联属于诊断流程，不能充当真实上线结果。 示意：一次改动把多任务分支接错，张量维度却仍兼容。运行测试可能通过，结构语义检查先拦住它；另一次结构正确但验证集退化，则在离线有效层退出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-nova-6f1301b9" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:evorec" data-paper-title="EvoRec: Self-Evolving Agentic Recommender Systems" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="EvoRec: Self-Evolving Agentic Recommender Systems 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-06-15 既有 LLM agent 每轮只翻译代码，不会积累优化方法。EvoRec 让 Research/Code Agent 迭代模型，Skill Evolver 从持久 Memory 中提炼可复用方法，使“模型”和“怎么优化模型”同时进化。 复现保真度：核心机制复现。复现保真度：核心机制复现。模型候选与优化方法双轨迭代、跨代 skill memory 均实际执行；生产多 agent 工具链未复刻。本地让 transition、content、popularity 三类技能竞争，连续三代根据固定 validation 选择并把胜出技能写入 memory；该记忆还接入通用 evolve 的下一代候选排序。  auto-research agent skill-evolution 搜广推 自动研究与高效上线 EvoRec让Skill Evolver进化什么，为什么不只保存最终模型代码？ 模型参数和代码记录了本轮结果，却未必保留发现有效改动的条件与方法。Skill Evolver从持久实验记忆中总结可复用优化技能，供下一轮Research与Code Agent调用，使搜索过程本身也能改进。技能仍须经实际执行与验证，不能把事后写出的漂亮经验当成已经证明可泛化的优化规律。 示意：一次负采样改动只在长尾切片有效，保存技能时应记住适用条件与失败切片；下轮遇到不同数据时先验证，而不是直接照搬冠军代码。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-evorec-ed228584" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rec-distill" data-paper-title="Rec-Distill: An Industrial Distillation Pipeline for Large-Scale Recommendation Models" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Rec-Distill: An Industrial Distillation Pipeline for Large-Scale Recommendation Models 搜广推与 LLM 应用 ByteDance / Douyin / TikTok 2026-05-28 工业大推荐 teacher 无法直接 serving，且 teacher/student 数据采样与实时分布不同。Rec-Distill 让 teacher 在自身 forward 阶段写出黑盒 logits，一份信号可异步服务多个 student。Student 的 main tower 只收真实标签并用于线上；aux tower 同时收 task 与 distillation loss，两者共享 backbone。 Fidelity: 完整核心链路复现。本地实际训练大 teacher 与轻 student，物化 black-box logits，执行 student-side sampling correction、main/aux decoupled towers、batch→streaming 两阶段蒸馏，并在 validation 搜索 loss ratio。本地对照口径：迁移基线是相同日程训练的 Raw Student；实验组是 Rec-Distill Student；NDCG@10 从 0.0039 降至 0.0036，transferability -4.11%。   搜广推 自动研究与高效上线 Rec-Distill 为什么先校正 teacher 的采样概率空间，还把蒸馏放在 aux tower 而非线上 main tower？ teacher 与 student 的采样方式不同，原始 logit 对应的概率含义可能不一致，直接拟合会把采样偏差也传过去。先按 student 口径校正，再让辅助塔接收任务与蒸馏损失，共享主干迁移知识；主塔只接真实标签并负责服务。这样控制蒸馏对输出校准的干扰，但教师质量与时效仍限制迁移收益。 示意：教师训练时更强地下采样负例，其分数不能直接当学生的真实点击概率。校正后让辅助头学习软信号，线上主头继续由真实标签约束，避免照搬错误的概率尺度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-rec-distill-367afce1" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:agentic-rec-tune" data-paper-title="AgenticRecTune: Multi-Agent with Self-Evolving Skillhub for Recommendation System Optimization" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="AgenticRecTune: Multi-Agent with Self-Evolving Skillhub for Recommendation System Optimization 搜广推与 LLM 应用 Google / Discover 2026-04-21 推荐系统配置跨召回、融合和重排，人工调节反馈慢且知识难复用。AgenticRecTune 将工作拆成 Actor、Critic、Insight、Skill、Online 五类 agent：生成方案、审查风险、总结洞见、沉淀技能，并从真实实验平台取回反馈形成闭环。 Fidelity: 核心机制复现。本地真正运行三轮 Actor 提案、Critic 评价和 SkillHub 继承，可直接观察每轮候选与冠军。动作空间是本地可执行排序权重，不接 Google 实验排期 API，也不把确定性 validation 评价冒充线上 Agent。本地对照口径：基线为固定手调排序配方，实验组运行三轮 Actor–Critic–SkillHub；NDCG@10 相对 +17.34%。  agent auto-research retrieval ranking reranking 搜广推 自动研究与高效上线 Actor提出了更高分的配置，为什么还需要Critic、SkillHub和真实实验反馈？ 提案只是待执行假设，Critic负责检查候选可行性与风险，真实实验才提供效果证据；Insight与Skill模块把可复用的成功条件和失败原因写回记忆。这样后续搜索能避免重复踩坑，而不是把语言模型的自评分当研究结果。本地配置搜索只支持缩小闭环，晋级必须遵守验证与测试隔离。 示意：Actor建议增加多样性权重，Critic发现延迟预算可能超标；真实运行失败后把失败条件存成技能，下轮便不再无条件复用同一方案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-agentic-rec-tune-8a853675" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:solaris" data-paper-title="SOLARIS: Speculative Offloading of Latent-bAsed Representation for Inference Scaling" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="SOLARIS: Speculative Offloading of Latent-bAsed Representation for Inference Scaling 搜广推与 LLM 应用 Meta 2026-04-13 大推荐模型在请求时为全部 user-item 对计算 latent 不现实。SOLARIS 先预测未来会访问的 pair，异步用 foundation model 预计算并缓存 latent；请求命中 cache 直接消费，未命中走 fallback。 复现保真度：核心机制复现。复现保真度：核心机制复现。Future-pair predictor、异步 cache 与 fallback 均实际执行。用未来三步交互训练 pair predictor，只缓存高置信 pair，并测量 cache 覆盖与 fallback 路径。  foundation-model serving latent-cache 搜广推 自动研究与高效上线 SOLARIS 为什么预测未来 user-item pair 后预计算 latent，而不只缓存一个通用用户向量？ 强模型的交互 latent 依赖具体用户与物品，单一用户向量未必保留这种深度配对信息。预测器提前挑可能访问的 pair，异步计算并缓存，再在请求命中时消费，未命中走 fallback。收益取决于覆盖率、时效和预算；未来交互可用于训练预测器，但在线缓存选择不能偷读真实未来答案。 示意：后台预测用户近期可能看到十件商品，先计算这十组深交互。请求出现其中一件时直接用缓存；出现意外商品就走常规路径，而不是假设所有未来候选都已准确知道。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-solaris-6dc852c5" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ug-sep" data-paper-title="Compute Only Once: UG-Separation for Efficient Large Recommendation Models" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Compute Only Once: UG-Separation for Efficient Large Recommendation Models 搜广推与 LLM 应用 ByteDance AML 2026-02-11 通过注意力/TokenMixer mask 阻断候选向用户 token 的反向信息流，使用户侧表示能在同一请求的多个候选间复用；Information Compensation 额外恢复被 mask 抑制的用户—候选交互。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04934，相对变化 -8.65%。本地代理目标与论文生产任务不同，不能外推线上 lift。  ranking-network inference-efficiency token-mixing 搜广推 自动研究与高效上线 UG-Sep 为什么先屏蔽候选到用户 token 的反向信息流，再加 Information Compensation？ 用户状态若读过候选就失去跨候选复用资格，掩码先保证用户侧独立计算，从而减少重复开销。但阻断双向交互也可能削弱原模型表达，补偿模块在评分路径恢复必要的用户—候选关系。它保留的是可共享编码与候选专属交互的分工，不能把补偿后的候选状态再次当成公共用户缓存。 示意：先算一份不含商品信息的用户表示供一百个候选共用，再让每件商品单独与它交互补偿。若把商品甲的补偿结果缓存给商品乙，就破坏了最初的隔离条件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-ug-sep-25948e1e" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:self-evolving-rec" data-paper-title="Self-Evolving Recommendation System: End-To-End Autonomous Model Optimization With LLM Agents" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Self-Evolving Recommendation System: End-To-End Autonomous Model Optimization With LLM Agents 搜广推与 LLM 应用 Google / YouTube 2026-02-10 推荐研发通常依赖人工提出假设、改代码、跑离线实验、申请线上 A/B，再把经验散落在文档里。论文将 Gemini 2.5 放入双层闭环：内层 agent 以 researcher personas、实验 journal、代码/训练工具探索 optimizer、网络结构和 reward；外层状态机负责安全检查、资源约束和真实 A/B promotion，再把线上结论写回记忆，驱动下一轮搜索。 Fidelity: 核心机制复现。本地 SmolLM2-135M-Instruct 实际读取 journal、给可执行配置打分、逐轮提出未尝试方案并接收 validation 反馈；未复刻 Google 生产 A/B 基础设施。本地对照口径：基线是 Human/Adagrad 配置；实验组是本地 LLM agent 经过四代 journal→提案→训练→validation 反馈后晋级的配置，NDCG@10 +2.57%。test 只在晋级完成后运行，不是单一模型相对 DIN。   搜广推 自动研究与高效上线 Self-Evolving Rec 为什么让内层 agent 探索离线方案，外层状态机才决定真实 A/B 晋级？ 离线代理能便宜筛选优化器、架构与奖励想法，却不完整代表线上用户和服务约束。外层独立管理安全、资源与真实实验晋级，再把结论写回长期 journal，让内层下一轮有证据可用。闭环的价值在实验治理与知识累积，不是 agent 提出方案就自动上线；本地验证循环不能替代真实生产 A/B。 示意：agent 提议一个离线更优但延迟超标的结构，外层先拒绝晋级；另一个通过资源检查再进入真实实验，其结果被记录，避免下一轮重复犯同样错误。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-self-evolving-rec-3809fcbe" class="ar-learning-paper-anchor"></span>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:radar" data-paper-title="RADAR: Recall Augmentation through Deferred Asynchronous Retrieval" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="RADAR: Recall Augmentation through Deferred Asynchronous Retrieval 搜广推与 LLM 应用 Meta 2025-06-08 将完整排序模型在本次请求后异步运行，把高价值结果缓存为下一次请求的召回补充，再与实时召回合并。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 radar 核心机制；相对 NDCG@10 -2.78%。  retrieval asynchronous-serving ranking 搜广推 自动研究与高效上线 RADAR 为什么把本次请求后异步运行的排序结果，用作下一次请求的召回补充？ 完整排序器通常比召回器表达更强，却无法在实时请求中遍历全部物品。RADAR 把昂贵全库计算移到请求后，缓存高价值结果，下次与实时召回合并，使排序知识提前影响候选覆盖。代价是缓存依据上一时刻历史，可能变旧，因此需要实时通道补充新意图，不能把异步结果当作当前请求的完整最优答案。 示意：用户看完一次推荐后，后台用完整模型筛出一批可能喜欢的电影。下次打开时直接把这批加入候选，同时实时召回根据刚发生的新点击补充变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<span id="paper-recommendation-radar-206d8edd" class="ar-learning-paper-anchor"></span>
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
