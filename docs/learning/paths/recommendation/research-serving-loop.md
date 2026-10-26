---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 自动研究与高效上线

[搜广推](index.md) / 子主题导学 · 约 3 分钟 · 19 张论文卡

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

## 这个子主题的论文卡片

导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">
<div class="ar-learning-controls">
<label for="learning-search">搜索卡片
<input id="learning-search" type="search" data-learning-search placeholder="搜索论文、机制、机构或本地边界"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">共 19 张卡片</p>
<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="FORTE: A Production Framework for Feature Evaluation and Deprecation in Industrial Recommender Systems 搜广推与 LLM 应用 Pinterest 2026-10-09 添加一个特征只需在某项指标上有收益，删除却不能损伤任何业务指标，而且同一个特征可能有多个模型消费者。FORTE 将退役流程拆成逐渐昂贵的门槛：先每天衡量冻结模型的特征依赖，检查长期稳定性，再联合扰动候选集合并真实重训，最后做线上实验和所有消费者的血缘审计。它不是单次 feature selection，也不能把单特征收益相加当成联合删除效果。一个特征单独看没有价值，可能与另一个冗余特征共同承载重要信号；不同输出头也可能给出相反方向。 结果仍是诊断，不能宣称复现 Pinterest 能力或吞吐收益。L2 公开数据训练，核心机制实现；结果仍是诊断，不能宣称复现 Pinterest 能力或吞吐收益。未复刻私有多模态特征、DCNv2/MMoE 大型 Pin Ranker、分布式 actor、每日生产 checkpoint sensors、线上 A/B 和实际基础设施移除。没有通过任一门槛也是有效结果，保留而不伪造通过。加载经过固定 archive SHA-256 校验的公开 MovieLens-100K。按 timestamp、user、item 排序，chronological 80/10/10；  features efficiency feature-deprecation 搜广推 自动研究与高效上线">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<h2 id="paper-recommendation-forte-d5b8210d">FORTE: A Production Framework for Feature Evaluation and Deprecation in Industrial Recommender Systems</h2>
<p class="ar-learning-card__meta">Pinterest · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>添加一个特征只需在某项指标上有收益，删除却不能损伤任何业务指标，而且同一个特征可能有多个模型消费者。FORTE 将退役流程拆成逐渐昂贵的门槛：先每天衡量冻结模型的特征依赖，检查长期稳定性，再联合扰动候选集合并真实重训，最后做线上实验和所有消费者的血缘审计。它不是单次 feature selection，也不能把单特征收益相加当成联合删除效果。一个特征单独看没有价值，可能与另一个冗余特征共同承载重要信号；不同输出头也可能给出相反方向。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>结果仍是诊断，不能宣称复现 Pinterest 能力或吞吐收益。L2 公开数据训练，核心机制实现；结果仍是诊断，不能宣称复现 Pinterest 能力或吞吐收益。未复刻私有多模态特征、DCNv2/MMoE 大型 Pin Ranker、分布式 actor、每日生产 checkpoint sensors、线上 A/B 和实际基础设施移除。没有通过任一门槛也是有效结果，保留而不伪造通过。加载经过固定 archive SHA-256 校验的公开 MovieLens-100K。按 timestamp、user、item 排序，chronological 80/10/10；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13806">原论文</a> · <a href="../../../../reproductions/2610.13806-forte/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Optimizing Effective Training Time for Large-Scale Recommendation Systems 搜广推与 LLM 应用 Meta Platforms, Inc. 2026-10-01 把端到端 wall time 分为真正消费新数据的训练时间与初始化、编译、checkpoint、发布和恢复等生命周期损耗，再按 owner 定位和优化。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 ETT 分解与 owner loss 归因；这是用户批准的生产基础设施例外，不声称推荐模型效果或线上 A/B 收益。收录例外：用户于 2026-10-02 明确批准的生产训练基础设施例外；部署指标是 ETT，不作为推荐模型效果或线上 A/B 收益。执行 ETT 分解与 owner loss 归因；这是用户批准的生产基础设施例外，不声称推荐模型效果或线上 A/B 收益。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  training-systems effective-training-time gpu-fleet 搜广推 自动研究与高效上线">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<h2 id="paper-recommendation-effective-training-time-8fded34e">Optimizing Effective Training Time for Large-Scale Recommendation Systems</h2>
<p class="ar-learning-card__meta">Meta Platforms, Inc. · 论文公开：2026-10-01</p>
<p><strong>方法要点：</strong>把端到端 wall time 分为真正消费新数据的训练时间与初始化、编译、checkpoint、发布和恢复等生命周期损耗，再按 owner 定位和优化。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 ETT 分解与 owner loss 归因；这是用户批准的生产基础设施例外，不声称推荐模型效果或线上 A/B 收益。收录例外：用户于 2026-10-02 明确批准的生产训练基础设施例外；部署指标是 ETT，不作为推荐模型效果或线上 A/B 收益。执行 ETT 分解与 owner loss 归因；这是用户批准的生产基础设施例外，不声称推荐模型效果或线上 A/B 收益。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02057">原论文</a> · <a href="../../../../reproductions/2610.02057-effective-training-time/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="EvoSkillRec: Skill-Genome Evolution for Recommender Architecture Discovery 搜广推与 LLM 应用 City University of Hong Kong 2026-09-28 把推荐网络拆成带输入输出类型的可执行 skill genome；控制器在约束空间组合技能，只有通过 validation 的创新才晋级并进入后续复用库。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 typed genome、validation evaluator、promotion 与 reuse；未调用外部 LLM 发明任意代码，也不复述论文大规模搜索收益。执行 typed genome、validation evaluator、promotion 与 reuse；未调用外部 LLM 发明任意代码，也不复述论文大规模搜索收益。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  recommendation-auto-evolution architecture-search skill-genome 搜广推 自动研究与高效上线">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<h2 id="paper-recommendation-evoskillrec-7ef949da">EvoSkillRec: Skill-Genome Evolution for Recommender Architecture Discovery</h2>
<p class="ar-learning-card__meta">City University of Hong Kong · 论文公开：2026-09-28</p>
<p><strong>方法要点：</strong>把推荐网络拆成带输入输出类型的可执行 skill genome；控制器在约束空间组合技能，只有通过 validation 的创新才晋级并进入后续复用库。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 typed genome、validation evaluator、promotion 与 reuse；未调用外部 LLM 发明任意代码，也不复述论文大规模搜索收益。执行 typed genome、validation evaluator、promotion 与 reuse；未调用外部 LLM 发明任意代码，也不复述论文大规模搜索收益。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34552">原论文</a> · <a href="../../../../reproductions/2609.34552-evoskillrec/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Verify, Don&#x27;t Trust: Agentic Model Development for Video Discovery Retrieval at Scale 搜广推与 LLM 应用 Meta Platforms 2026-09-18 EvoPilot 不把“某个训练任务完成”直接当成研究证据，而把控制组与实验组的匹配比较作为证据单元。协议固定 shared base、数据版本、评测器、有效输出深度和唯一允许变化的 treatment；执行结束后，从产物读取实际状态并 fail closed，最后仍需人工审核才能接纳结论。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地复现的是 EvoPilot 的比较协议与 fail-closed 验证器，并在同一 MovieLens 切分上运行匹配的交互头对照；不是 Meta VDD 生产系统复刻。公开 MovieLens 上执行比较协议、artifact attestation、fail-closed pair verifier 与 validation-only 交互头对照；不复刻 Meta VDD 私有视频日志、百亿级索引、远程工作流或线上流量。  autoresearch experiment-verification video-retrieval 搜广推 自动研究与高效上线">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<h2 id="paper-recommendation-evopilot-795a30ed">Verify, Don&#x27;t Trust: Agentic Model Development for Video Discovery Retrieval at Scale</h2>
<p class="ar-learning-card__meta">Meta Platforms · 论文公开：2026-09-18</p>
<p><strong>方法要点：</strong>EvoPilot 不把“某个训练任务完成”直接当成研究证据，而把控制组与实验组的匹配比较作为证据单元。协议固定 shared base、数据版本、评测器、有效输出深度和唯一允许变化的 treatment；执行结束后，从产物读取实际状态并 fail closed，最后仍需人工审核才能接纳结论。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地复现的是 EvoPilot 的比较协议与 fail-closed 验证器，并在同一 MovieLens 切分上运行匹配的交互头对照；不是 Meta VDD 生产系统复刻。公开 MovieLens 上执行比较协议、artifact attestation、fail-closed pair verifier 与 validation-only 交互头对照；不复刻 Meta VDD 私有视频日志、百亿级索引、远程工作流或线上流量。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.21257">原论文</a> · <a href="../../../../reproductions/2609.21257-evopilot/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="AutoLR: Automating the Path from Research to Launch Review in Industrial Recommender Systems 搜广推与 LLM 应用 NetEase, Inc. 2026-09-04 AutoLR 将论文调研、方案辩论、代码实验、离线评估、A/B 测试与 Launch Review 串成长期状态机。LLM 负责语义推理和代码生成，确定性控制器保留预算分配、指标抽取、护栏和状态迁移权，防止噪声结果在 KEEP 链中被不断放大。 复现级别：离线控制器核心。复现级别：离线控制器核心。对输入候选与评审执行预算排序、独立指标门槛、持久化账本和人工评审打包；不包含实时 LLM 调研、自动代码生成或线上发布。论文生产代码与 DASHEN 数据未公开；模型只能选择白名单参数，不能注入命令或任意代码。当前实现是受控的离线自动研究闭环，不声称自主创新架构或具备自动发布权限。真实 Qwen checkpoint 已在公开 Amazon Beauty 2014 5-core 上完成三轮有界研究：每轮动态生成参数提案，分别调用两个 reviewer，再执行一轮真实反向传播验证和完整 validation 训练。  auto-research experiment-controller launch-review industrial-recommendation 搜广推 自动研究与高效上线">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<h2 id="paper-recommendation-autolr-f0e06ba6">AutoLR: Automating the Path from Research to Launch Review in Industrial Recommender Systems</h2>
<p class="ar-learning-card__meta">NetEase, Inc. · 论文公开：2026-09-04</p>
<p><strong>方法要点：</strong>AutoLR 将论文调研、方案辩论、代码实验、离线评估、A/B 测试与 Launch Review 串成长期状态机。LLM 负责语义推理和代码生成，确定性控制器保留预算分配、指标抽取、护栏和状态迁移权，防止噪声结果在 KEEP 链中被不断放大。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：离线控制器核心。复现级别：离线控制器核心。对输入候选与评审执行预算排序、独立指标门槛、持久化账本和人工评审打包；不包含实时 LLM 调研、自动代码生成或线上发布。论文生产代码与 DASHEN 数据未公开；模型只能选择白名单参数，不能注入命令或任意代码。当前实现是受控的离线自动研究闭环，不声称自主创新架构或具备自动发布权限。真实 Qwen checkpoint 已在公开 Amazon Beauty 2014 5-core 上完成三轮有界研究：每轮动态生成参数提案，分别调用两个 reviewer，再执行一轮真实反向传播验证和完整 validation 训练。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04871">原论文</a> · <a href="../../../../reproductions/2609.04871-autolr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="CORAL: An LLM-Native Harness for Production Recommender Systems 搜广推与 LLM 应用 Meta AI 2026-09-02 CORAL 把推荐优化建模为连续闭环：LLM 根据目标、预算和最近实验记忆生成结构化配置，执行系统验证约束并运行实验，再把观测结果写回下一轮上下文。与一次性自动调参相比，它强调可执行约束、短记忆和生产反馈。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。实现有预算约束的配置提案、短期实验记忆、效果反馈与下一轮更新。未接入 Meta 私有遥测、生产 LLM、实验平台或线上流量；实现可作为推荐 Evolve 的控制器算子组合使用。在 MovieLens 100K 上执行五轮预算分配、三轮记忆和 validation-only blend；三 seed 产物见 metrics/public-seeds42-44.json。该结果只验证控制器闭环和约束可执行性，不把公开小数据效果等同于 Meta 线上因果增益。  auto-research agent retrieval-budget constrained-optimization 搜广推 自动研究与高效上线">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<h2 id="paper-recommendation-coral-3b3ed34a">CORAL: An LLM-Native Harness for Production Recommender Systems</h2>
<p class="ar-learning-card__meta">Meta AI · 论文公开：2026-09-02</p>
<p><strong>方法要点：</strong>CORAL 把推荐优化建模为连续闭环：LLM 根据目标、预算和最近实验记忆生成结构化配置，执行系统验证约束并运行实验，再把观测结果写回下一轮上下文。与一次性自动调参相比，它强调可执行约束、短记忆和生产反馈。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。实现有预算约束的配置提案、短期实验记忆、效果反馈与下一轮更新。未接入 Meta 私有遥测、生产 LLM、实验平台或线上流量；实现可作为推荐 Evolve 的控制器算子组合使用。在 MovieLens 100K 上执行五轮预算分配、三轮记忆和 validation-only blend；三 seed 产物见 metrics/public-seeds42-44.json。该结果只验证控制器闭环和约束可执行性，不把公开小数据效果等同于 Meta 线上因果增益。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.02730">原论文</a> · <a href="../../../../reproductions/2609.02730-coral/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="RecHarness: A Bandit-Routed Agentic Harness for Self-Evolving Recommender Systems 搜广推与 LLM 应用 Huazhong Agricultural University (Kuaishou internship) 2026-07-31 将结构改造定义为有限 arm，用 bandit 根据历史收益和不确定性分配试验预算，再把胜者反馈写回下一轮候选。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  auto-research bandit ranking 搜广推 自动研究与高效上线">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<h2 id="paper-recommendation-recharness-7341e5ce">RecHarness: A Bandit-Routed Agentic Harness for Self-Evolving Recommender Systems</h2>
<p class="ar-learning-card__meta">Huazhong Agricultural University (Kuaishou internship) · 论文公开：2026-07-31</p>
<p><strong>方法要点：</strong>将结构改造定义为有限 arm，用 bandit 根据历史收益和不确定性分配试验预算，再把胜者反馈写回下一轮候选。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.29241">原论文</a> · <a href="../../../../reproductions/2607.29241-recharness/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="ROCS: Request-Oriented Compute Sharing for Efficient Large-Scale Recommendation 搜广推与 LLM 应用 Meta AI 2026-07-30 一次推荐请求会评分大量候选，而用户侧特征完全相同。ROCS 通过 Generalized Layer Masking 保持候选隔离，用 Deep Cross Attention 延迟交互，再由 IKBO 在 GPU kernel 内广播 request 表示。 Fidelity: 核心机制复现。实现一次 request encoding、延迟 candidate interaction 和批量候选评分。未复刻生产 GLM、IKBO CUDA kernel、Meta 私有模型与集群。本地对照口径：基线为逐候选重复编码；实验组为 ROCS core，相对基线 NDCG@10 +8.19%。  retrieval ranking serving compute-sharing 搜广推 自动研究与高效上线">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<h2 id="paper-recommendation-rocs-28113d9d">ROCS: Request-Oriented Compute Sharing for Efficient Large-Scale Recommendation</h2>
<p class="ar-learning-card__meta">Meta AI · 论文公开：2026-07-30</p>
<p><strong>方法要点：</strong>一次推荐请求会评分大量候选，而用户侧特征完全相同。ROCS 通过 Generalized Layer Masking 保持候选隔离，用 Deep Cross Attention 延迟交互，再由 IKBO 在 GPU kernel 内广播 request 表示。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。实现一次 request encoding、延迟 candidate interaction 和批量候选评分。未复刻生产 GLM、IKBO CUDA kernel、Meta 私有模型与集群。本地对照口径：基线为逐候选重复编码；实验组为 ROCS core，相对基线 NDCG@10 +8.19%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27744">原论文</a> · <a href="../../../../reproductions/2607.27744-rocs/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Memory Layer: Train the In-Model Cache for Recommendation Models 搜广推与 LLM 应用 Meta / Instagram Reels 2026-07-27 传统 early-stage ranker 在训练时用 item tower 的新鲜输出，服务时却读另一个流程预计算并发布的 item cache；cache miss 还会绕过正常模型。这造成训练、离线评测和线上服务看到三套不同表征。Memory Layer 把 cache 变成模型自身的稀疏参数表：item tower 在训练中写入，后续网络和服务共同读取；作者、topic 等 always-on 属性则保证新内容或 cache miss 仍可评分。 seed 42 的 NDCG@10 相对基线约 +4.36%，结构诊断而非公开小数据 lift 是本复现重点。Fidelity: 核心机制复现。本地实现训练内 item-tower 写回、共享 cache 读取、冻结外部快照对照和 always-on cache-miss fallback；不把普通 embedding lookup 冒充 Meta 的 MPZCH 基础设施。MovieLens 没有媒体创建时间、Instagram 冷启动曝光与线上 NE，因此不能验证论文业务 lift。  ranking training-serving-consistency cold-start cache serving 搜广推 自动研究与高效上线">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<h2 id="paper-recommendation-memory-layer-0d31a0b7">Memory Layer: Train the In-Model Cache for Recommendation Models</h2>
<p class="ar-learning-card__meta">Meta / Instagram Reels · 论文公开：2026-07-27</p>
<p><strong>方法要点：</strong>传统 early-stage ranker 在训练时用 item tower 的新鲜输出，服务时却读另一个流程预计算并发布的 item cache；cache miss 还会绕过正常模型。这造成训练、离线评测和线上服务看到三套不同表征。Memory Layer 把 cache 变成模型自身的稀疏参数表：item tower 在训练中写入，后续网络和服务共同读取；作者、topic 等 always-on 属性则保证新内容或 cache miss 仍可评分。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>seed 42 的 NDCG@10 相对基线约 +4.36%，结构诊断而非公开小数据 lift 是本复现重点。Fidelity: 核心机制复现。本地实现训练内 item-tower 写回、共享 cache 读取、冻结外部快照对照和 always-on cache-miss fallback；不把普通 embedding lookup 冒充 Meta 的 MPZCH 基础设施。MovieLens 没有媒体创建时间、Instagram 冷启动曝光与线上 NE，因此不能验证论文业务 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25110">原论文</a> · <a href="../../../../reproductions/2607.25110-memory-layer/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="RecEvolve: A Knowledge-Driven Autonomous Agent System for Recommender Systems 搜广推与 LLM 应用 Google 2026-07-20 RecEvolve 让研究 Agent 从实验知识库提出模型变体，以独立验证集选择冠军，并用版本化状态支持失败回滚。系统显式防止通过极端温度等方式“刷指标”，让上一轮结论成为下一轮可审计的研究知识。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。实现提案、critic gate、隔离试验、冠军继承、回滚与 reward-hack 拒绝。未复刻 Google 私有日志、TPU 集群、生产 coding-agent 工具链和线上实验归因；该 adapter 作为推荐 Evolve 的统一多轮控制器算子。MovieLens 100K 上用固定候选空间执行完整研究控制流；三 seed 结果见 metrics/public-seeds42-44.json。本地指标用于比较同一公开协议下的控制策略，不复刻 Google 私有 Two-Tower 数值。  auto-research agent two-tower reward-hacking 搜广推 自动研究与高效上线">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<h2 id="paper-recommendation-recevolve-55072983">RecEvolve: A Knowledge-Driven Autonomous Agent System for Recommender Systems</h2>
<p class="ar-learning-card__meta">Google · 论文公开：2026-07-20</p>
<p><strong>方法要点：</strong>RecEvolve 让研究 Agent 从实验知识库提出模型变体，以独立验证集选择冠军，并用版本化状态支持失败回滚。系统显式防止通过极端温度等方式“刷指标”，让上一轮结论成为下一轮可审计的研究知识。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。实现提案、critic gate、隔离试验、冠军继承、回滚与 reward-hack 拒绝。未复刻 Google 私有日志、TPU 集群、生产 coding-agent 工具链和线上实验归因；该 adapter 作为推荐 Evolve 的统一多轮控制器算子。MovieLens 100K 上用固定候选空间执行完整研究控制流；三 seed 结果见 metrics/public-seeds42-44.json。本地指标用于比较同一公开协议下的控制策略，不复刻 Google 私有 Two-Tower 数值。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.01622">原论文</a> · <a href="../../../../reproductions/2609.01622-recevolve/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Prompt Generation Technical Report 搜广推与 LLM 应用 Alibaba / Taobao Search 2026-07-13 生成式检索把 query、用户行为和异构特征输入 LLM，再直接生成商品或文档 SID。工业系统的问题不只是模型效果：每次加特征都要同步修改数据、训练和 serving，容易产生 training-serving skew；长文本和行为序列又会迅速放大 token 数与延迟。PG 用 prompt_template.json 与 prompt_feature.json 把特征工程从模型代码中解耦。 Fidelity: 核心机制复现。本地实际执行论文同款 Qwen2.5-0.5B、MiniOneRec Amazon Office 数据与官方三段式 SID、双 JSON 单一事实源、text/embedding/combo/sequence 四类特征、preprocessor/projector/merger 组件协议、embedding-space mean merger、LoRA SFT、validation 配置选择和 held-out 候选评分。未复刻淘宝全量训练、C++ batched kernels、线上 event replay 和生产 serving。  llm-recommendation generative-retrieval autoresearch serving 搜广推 自动研究与高效上线">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<h2 id="paper-recommendation-prompt-generation-d1640558">Prompt Generation Technical Report</h2>
<p class="ar-learning-card__meta">Alibaba / Taobao Search · 论文公开：2026-07-13</p>
<p><strong>方法要点：</strong>生成式检索把 query、用户行为和异构特征输入 LLM，再直接生成商品或文档 SID。工业系统的问题不只是模型效果：每次加特征都要同步修改数据、训练和 serving，容易产生 training-serving skew；长文本和行为序列又会迅速放大 token 数与延迟。PG 用 prompt_template.json 与 prompt_feature.json 把特征工程从模型代码中解耦。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地实际执行论文同款 Qwen2.5-0.5B、MiniOneRec Amazon Office 数据与官方三段式 SID、双 JSON 单一事实源、text/embedding/combo/sequence 四类特征、preprocessor/projector/merger 组件协议、embedding-space mean merger、LoRA SFT、validation 配置选择和 held-out 候选评分。未复刻淘宝全量训练、C++ batched kernels、线上 event replay 和生产 serving。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.11326">原论文</a> · <a href="../../../../reproductions/2607.11326-prompt-generation/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="NOVA: A Verification-Aware Agent Harness for Architecture Evolution in Industrial Recommender Systems 搜广推与 LLM 应用 Tencent 2026-06-25 普通代码 agent 只能证明代码“能跑”，无法阻止结构语义错误和静默负向。NOVA 用 architecture gradient 汇总历史修改、验证诊断和指标反馈，再通过 L1 结构语义、L2 可执行、L3 离线有效、L4 在线影响的级联验证逐级放行，高风险任务交给人工。 复现保真度：核心机制复现。复现保真度：核心机制复现。四级验证、失败方向记忆和 architecture gradient 均实际执行；腾讯生产 agent 与线上灰度未复刻。在 MovieLens 100K 上生成 transition、content、popularity 和故意错误的 shape 候选，真实执行四级验证并只用 validation 选候选；通用 evolve 还会把验证记录、成功技能和禁止方向写入 result.json。  auto-research architecture-evolution verification 搜广推 自动研究与高效上线">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<h2 id="paper-recommendation-nova-6f1301b9">NOVA: A Verification-Aware Agent Harness for Architecture Evolution in Industrial Recommender Systems</h2>
<p class="ar-learning-card__meta">Tencent · 论文公开：2026-06-25</p>
<p><strong>方法要点：</strong>普通代码 agent 只能证明代码“能跑”，无法阻止结构语义错误和静默负向。NOVA 用 architecture gradient 汇总历史修改、验证诊断和指标反馈，再通过 L1 结构语义、L2 可执行、L3 离线有效、L4 在线影响的级联验证逐级放行，高风险任务交给人工。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现保真度：核心机制复现。复现保真度：核心机制复现。四级验证、失败方向记忆和 architecture gradient 均实际执行；腾讯生产 agent 与线上灰度未复刻。在 MovieLens 100K 上生成 transition、content、popularity 和故意错误的 shape 候选，真实执行四级验证并只用 validation 选候选；通用 evolve 还会把验证记录、成功技能和禁止方向写入 result.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.27243">原论文</a> · <a href="../../../../reproductions/2606.27243-nova/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="EvoRec: Self-Evolving Agentic Recommender Systems 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-06-15 既有 LLM agent 每轮只翻译代码，不会积累优化方法。EvoRec 让 Research/Code Agent 迭代模型，Skill Evolver 从持久 Memory 中提炼可复用方法，使“模型”和“怎么优化模型”同时进化。 复现保真度：核心机制复现。复现保真度：核心机制复现。模型候选与优化方法双轨迭代、跨代 skill memory 均实际执行；生产多 agent 工具链未复刻。本地让 transition、content、popularity 三类技能竞争，连续三代根据固定 validation 选择并把胜出技能写入 memory；该记忆还接入通用 evolve 的下一代候选排序。  auto-research agent skill-evolution 搜广推 自动研究与高效上线">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<h2 id="paper-recommendation-evorec-ed228584">EvoRec: Self-Evolving Agentic Recommender Systems</h2>
<p class="ar-learning-card__meta">Alibaba International Digital Commerce Group · 论文公开：2026-06-15</p>
<p><strong>方法要点：</strong>既有 LLM agent 每轮只翻译代码，不会积累优化方法。EvoRec 让 Research/Code Agent 迭代模型，Skill Evolver 从持久 Memory 中提炼可复用方法，使“模型”和“怎么优化模型”同时进化。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现保真度：核心机制复现。复现保真度：核心机制复现。模型候选与优化方法双轨迭代、跨代 skill memory 均实际执行；生产多 agent 工具链未复刻。本地让 transition、content、popularity 三类技能竞争，连续三代根据固定 validation 选择并把胜出技能写入 memory；该记忆还接入通用 evolve 的下一代候选排序。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.28368">原论文</a> · <a href="../../../../reproductions/2606.28368-evorec/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Rec-Distill: An Industrial Distillation Pipeline for Large-Scale Recommendation Models 搜广推与 LLM 应用 ByteDance / Douyin / TikTok 2026-05-28 工业大推荐 teacher 无法直接 serving，且 teacher/student 数据采样与实时分布不同。Rec-Distill 让 teacher 在自身 forward 阶段写出黑盒 logits，一份信号可异步服务多个 student。Student 的 main tower 只收真实标签并用于线上；aux tower 同时收 task 与 distillation loss，两者共享 backbone。 Fidelity: 完整核心链路复现。本地实际训练大 teacher 与轻 student，物化 black-box logits，执行 student-side sampling correction、main/aux decoupled towers、batch→streaming 两阶段蒸馏，并在 validation 搜索 loss ratio。本地对照口径：迁移基线是相同日程训练的 Raw Student；实验组是 Rec-Distill Student；NDCG@10 从 0.0039 降至 0.0036，transferability -4.11%。   搜广推 自动研究与高效上线">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<h2 id="paper-recommendation-rec-distill-367afce1">Rec-Distill: An Industrial Distillation Pipeline for Large-Scale Recommendation Models</h2>
<p class="ar-learning-card__meta">ByteDance / Douyin / TikTok · 论文公开：2026-05-28</p>
<p><strong>方法要点：</strong>工业大推荐 teacher 无法直接 serving，且 teacher/student 数据采样与实时分布不同。Rec-Distill 让 teacher 在自身 forward 阶段写出黑盒 logits，一份信号可异步服务多个 student。Student 的 main tower 只收真实标签并用于线上；aux tower 同时收 task 与 distillation loss，两者共享 backbone。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 完整核心链路复现。本地实际训练大 teacher 与轻 student，物化 black-box logits，执行 student-side sampling correction、main/aux decoupled towers、batch→streaming 两阶段蒸馏，并在 validation 搜索 loss ratio。本地对照口径：迁移基线是相同日程训练的 Raw Student；实验组是 Rec-Distill Student；NDCG@10 从 0.0039 降至 0.0036，transferability -4.11%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.29755">原论文</a> · <a href="../../../../reproductions/2605.29755-rec-distill/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="AgenticRecTune: Multi-Agent with Self-Evolving Skillhub for Recommendation System Optimization 搜广推与 LLM 应用 Google / Discover 2026-04-21 推荐系统配置跨召回、融合和重排，人工调节反馈慢且知识难复用。AgenticRecTune 将工作拆成 Actor、Critic、Insight、Skill、Online 五类 agent：生成方案、审查风险、总结洞见、沉淀技能，并从真实实验平台取回反馈形成闭环。 Fidelity: 核心机制复现。本地真正运行三轮 Actor 提案、Critic 评价和 SkillHub 继承，可直接观察每轮候选与冠军。动作空间是本地可执行排序权重，不接 Google 实验排期 API，也不把确定性 validation 评价冒充线上 Agent。本地对照口径：基线为固定手调排序配方，实验组运行三轮 Actor–Critic–SkillHub；NDCG@10 相对 +17.34%。  agent auto-research retrieval ranking reranking 搜广推 自动研究与高效上线">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<h2 id="paper-recommendation-agentic-rec-tune-8a853675">AgenticRecTune: Multi-Agent with Self-Evolving Skillhub for Recommendation System Optimization</h2>
<p class="ar-learning-card__meta">Google / Discover · 论文公开：2026-04-21</p>
<p><strong>方法要点：</strong>推荐系统配置跨召回、融合和重排，人工调节反馈慢且知识难复用。AgenticRecTune 将工作拆成 Actor、Critic、Insight、Skill、Online 五类 agent：生成方案、审查风险、总结洞见、沉淀技能，并从真实实验平台取回反馈形成闭环。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地真正运行三轮 Actor 提案、Critic 评价和 SkillHub 继承，可直接观察每轮候选与冠军。动作空间是本地可执行排序权重，不接 Google 实验排期 API，也不把确定性 validation 评价冒充线上 Agent。本地对照口径：基线为固定手调排序配方，实验组运行三轮 Actor–Critic–SkillHub；NDCG@10 相对 +17.34%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.26969">原论文</a> · <a href="../../../../reproductions/2604.26969-agentic-rec-tune/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="SOLARIS: Speculative Offloading of Latent-bAsed Representation for Inference Scaling 搜广推与 LLM 应用 Meta 2026-04-13 大推荐模型在请求时为全部 user-item 对计算 latent 不现实。SOLARIS 先预测未来会访问的 pair，异步用 foundation model 预计算并缓存 latent；请求命中 cache 直接消费，未命中走 fallback。 复现保真度：核心机制复现。复现保真度：核心机制复现。Future-pair predictor、异步 cache 与 fallback 均实际执行。用未来三步交互训练 pair predictor，只缓存高置信 pair，并测量 cache 覆盖与 fallback 路径。  foundation-model serving latent-cache 搜广推 自动研究与高效上线">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<h2 id="paper-recommendation-solaris-6dc852c5">SOLARIS: Speculative Offloading of Latent-bAsed Representation for Inference Scaling</h2>
<p class="ar-learning-card__meta">Meta · 论文公开：2026-04-13</p>
<p><strong>方法要点：</strong>大推荐模型在请求时为全部 user-item 对计算 latent 不现实。SOLARIS 先预测未来会访问的 pair，异步用 foundation model 预计算并缓存 latent；请求命中 cache 直接消费，未命中走 fallback。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现保真度：核心机制复现。复现保真度：核心机制复现。Future-pair predictor、异步 cache 与 fallback 均实际执行。用未来三步交互训练 pair predictor，只缓存高置信 pair，并测量 cache 覆盖与 fallback 路径。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.12110">原论文</a> · <a href="../../../../reproductions/2604.12110-solaris/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Compute Only Once: UG-Separation for Efficient Large Recommendation Models 搜广推与 LLM 应用 ByteDance AML 2026-02-11 通过注意力/TokenMixer mask 阻断候选向用户 token 的反向信息流，使用户侧表示能在同一请求的多个候选间复用；Information Compensation 额外恢复被 mask 抑制的用户—候选交互。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04934，相对变化 -8.65%。本地代理目标与论文生产任务不同，不能外推线上 lift。  ranking-network inference-efficiency token-mixing 搜广推 自动研究与高效上线">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<h2 id="paper-recommendation-ug-sep-25948e1e">Compute Only Once: UG-Separation for Efficient Large Recommendation Models</h2>
<p class="ar-learning-card__meta">ByteDance AML · 论文公开：2026-02-11</p>
<p><strong>方法要点：</strong>通过注意力/TokenMixer mask 阻断候选向用户 token 的反向信息流，使用户侧表示能在同一请求的多个候选间复用；Information Compensation 额外恢复被 mask 抑制的用户—候选交互。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04934，相对变化 -8.65%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.10455">原论文</a> · <a href="../../../../reproductions/2602.10455-ug-sep/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="Self-Evolving Recommendation System: End-To-End Autonomous Model Optimization With LLM Agents 搜广推与 LLM 应用 Google / YouTube 2026-02-10 推荐研发通常依赖人工提出假设、改代码、跑离线实验、申请线上 A/B，再把经验散落在文档里。论文将 Gemini 2.5 放入双层闭环：内层 agent 以 researcher personas、实验 journal、代码/训练工具探索 optimizer、网络结构和 reward；外层状态机负责安全检查、资源约束和真实 A/B promotion，再把线上结论写回记忆，驱动下一轮搜索。 Fidelity: 核心机制复现。本地 SmolLM2-135M-Instruct 实际读取 journal、给可执行配置打分、逐轮提出未尝试方案并接收 validation 反馈；未复刻 Google 生产 A/B 基础设施。本地对照口径：基线是 Human/Adagrad 配置；实验组是本地 LLM agent 经过四代 journal→提案→训练→validation 反馈后晋级的配置，NDCG@10 +2.57%。test 只在晋级完成后运行，不是单一模型相对 DIN。   搜广推 自动研究与高效上线">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<h2 id="paper-recommendation-self-evolving-rec-3809fcbe">Self-Evolving Recommendation System: End-To-End Autonomous Model Optimization With LLM Agents</h2>
<p class="ar-learning-card__meta">Google / YouTube · 论文公开：2026-02-10</p>
<p><strong>方法要点：</strong>推荐研发通常依赖人工提出假设、改代码、跑离线实验、申请线上 A/B，再把经验散落在文档里。论文将 Gemini 2.5 放入双层闭环：内层 agent 以 researcher personas、实验 journal、代码/训练工具探索 optimizer、网络结构和 reward；外层状态机负责安全检查、资源约束和真实 A/B promotion，再把线上结论写回记忆，驱动下一轮搜索。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地 SmolLM2-135M-Instruct 实际读取 journal、给可执行配置打分、逐轮提出未尝试方案并接收 validation 反馈；未复刻 Google 生产 A/B 基础设施。本地对照口径：基线是 Human/Adagrad 配置；实验组是本地 LLM agent 经过四代 journal→提案→训练→validation 反馈后晋级的配置，NDCG@10 +2.57%。test 只在晋级完成后运行，不是单一模型相对 DIN。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.10226">原论文</a> · <a href="../../../../reproductions/2602.10226-self-evolving-rec/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/research-serving-loop" data-search="RADAR: Recall Augmentation through Deferred Asynchronous Retrieval 搜广推与 LLM 应用 Meta 2025-06-08 将完整排序模型在本次请求后异步运行，把高价值结果缓存为下一次请求的召回补充，再与实时召回合并。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 radar 核心机制；相对 NDCG@10 -2.78%。  retrieval asynchronous-serving ranking 搜广推 自动研究与高效上线">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 自动研究与高效上线</a></p>
<h2 id="paper-recommendation-radar-206d8edd">RADAR: Recall Augmentation through Deferred Asynchronous Retrieval</h2>
<p class="ar-learning-card__meta">Meta · 论文公开：2025-06-08</p>
<p><strong>方法要点：</strong>将完整排序模型在本次请求后异步运行，把高价值结果缓存为下一次请求的召回补充，再与实时召回合并。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 radar 核心机制；相对 NDCG@10 -2.78%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2506.07261">原论文</a> · <a href="../../../../reproductions/2506.07261-radar/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
