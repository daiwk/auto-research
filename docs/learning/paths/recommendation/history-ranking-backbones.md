---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 用户历史与排序骨干

[搜广推](index.md) / 子主题导学 · 约 3 分钟 · 73 张论文卡

## 先想一个问题

计算预算应该花在历史内部、候选与历史，还是异构字段之间？

## 记住这一点

先分清交互对象：DIN按候选激活相关历史；HSTU让输入窗口中的历史状态逐层交互；RankMixer用固定TokenMix和独立FFN处理异构特征。长历史压缩、统一序列与字段、稀疏注意力以及预训练迁移，都在选择保留什么状态、何时交换信息。不同骨干可互补，不能仅凭都有Transformer就视为同一路线。

## 一个例子

用户长期喜欢园艺，最近连续看猫视频。推荐猫粮时，候选条件化读历史可以关注近期养猫线索；推荐园艺工具时则要找回远期兴趣。随后还要把价格、场景和用户字段一起交叉，历史建模与字段交互各自承担不同工作。

## 什么时候要小心

字段token数与历史长度不是同一变量，不能直接比较两张复杂度表。缓存只有在状态不依赖当前候选时才可共享。短历史公开数据上的正负结果，都不能单独证明工业长序列效果或生产吞吐。

## 先读这几篇

先读DIN辨认候选条件化兴趣，再读HSTU理解历史状态如何逐层变化，最后读RankMixer区分字段交互；再看[长历史对比](../../001-hstu-longer-slimper.md)和[RankMixer四行例子](../../002-rankmixer-tokenmix.md)比较信息流，本地结果以各自数据与保真度为限。

1. [Deep Interest Network for Click-Through Rate Prediction](../../../reproductions/1706.06978-din/README.md) · [原论文](https://arxiv.org/abs/1706.06978)
2. [Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations](../../../reproductions/2402.17152-hstu/README.md) · [原论文](https://arxiv.org/abs/2402.17152)
3. [RankMixer: Scaling Up Ranking Models in Industrial Recommenders](../../../reproductions/2507.15551-rankmixer/README.md) · [原论文](https://arxiv.org/abs/2507.15551)

## 自测一下

一个用户状态已经读过候选A的信息，还能原样作为候选B的共享用户缓存吗？

??? note "展开参考答案"

    通常不能。该状态已依赖A，会污染B的计算。需要保持候选无关的共享路径，或明确重新计算候选相关部分；只给模块起名为用户塔并不能保证可复用。

## 这个子主题的论文卡片

导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">
<div class="ar-learning-controls">
<label for="learning-search">搜索卡片
<input id="learning-search" type="search" data-learning-search placeholder="搜索论文、机制、机构或本地边界"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">共 73 张卡片</p>
<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="ECHO: Efficient Cascade with Homogeneous Operators for Distillation-Guided 100K-Sequence Modeling 搜广推与 LLM 应用 Kuaishou Technology 2026-10-20 将100K历史压成少量潜向量会丢失记录地址；逐候选扫描全部历史又过贵。ECHO让用户侧DS保留原始记录，再由目标侧TFR选更小子集。训练侧候选感知教师通过完整软分布和选择边界监督DS，教师相关性参数还导出到检索和聚合。线上不运行DS，也不扫描完整历史。 原文完整实验成本过高，不复现（审查 DONE）。仅L1诊断，不是完整ECHO/TWIN或推荐能力；已实现选择器蒸馏损失，在真实A100上验证公式、梯度和短时更新。仅L1诊断，不是完整ECHO/TWIN或推荐能力；原文完整实验成本过高，不复现（审查 DONE）。固定合成logit、seed42/43/44，在A100执行逐标量CE参考、实际学生参数更新、教师无梯度、padding零梯度及同排序无有效边界配对的负对照。未加载预训练checkpoint，无推荐准确率或正式比较资格。  长序列推荐 蒸馏选择与边界监督 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-echo-selector-loss-59466a02">ECHO: Efficient Cascade with Homogeneous Operators for Distillation-Guided 100K-Sequence Modeling</h2>
<p class="ar-learning-card__meta">Kuaishou Technology · 论文公开：2026-10-20</p>
<p><strong>方法要点：</strong>将100K历史压成少量潜向量会丢失记录地址；逐候选扫描全部历史又过贵。ECHO让用户侧DS保留原始记录，再由目标侧TFR选更小子集。训练侧候选感知教师通过完整软分布和选择边界监督DS，教师相关性参数还导出到检索和聚合。线上不运行DS，也不扫描完整历史。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>原文完整实验成本过高，不复现（审查 DONE）。仅L1诊断，不是完整ECHO/TWIN或推荐能力；已实现选择器蒸馏损失，在真实A100上验证公式、梯度和短时更新。仅L1诊断，不是完整ECHO/TWIN或推荐能力；原文完整实验成本过高，不复现（审查 DONE）。固定合成logit、seed42/43/44，在A100执行逐标量CE参考、实际学生参数更新、教师无梯度、padding零梯度及同排序无有效边界配对的负对照。未加载预训练checkpoint，无推荐准确率或正式比较资格。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28569v1">原论文</a> · <a href="../../../../recommendation-components/2610.28569-echo-selector-loss/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Not All Is Lost: Repairing Lossy User Preference States of Personalization Encoders 搜广推与 LLM 应用 原文首页未列第一作者机构 2026-10-01 冻结 encoder 与原 task head，从已有 forward cache 中比较各 timestep 表征和当前 preference state，选择长程、近期或局部 burst 的纠正证据并做 residual repair。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 frozen-cache evidence selection 与 residual correction；用户批准为学术/Evolve 例外，无线上 A/B。收录例外：用户于 2026-10-02 明确批准的学术/Evolve 机制例外；论文没有量化线上 A/B，不进入工业证据结论。执行 frozen-cache evidence selection 与 residual correction；用户批准为学术/Evolve 例外，无线上 A/B。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。  personalization state-repair sequential-recommendation 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-repair-state-eec04848">Not All Is Lost: Repairing Lossy User Preference States of Personalization Encoders</h2>
<p class="ar-learning-card__meta">原文首页未列第一作者机构 · 论文公开：2026-10-01</p>
<p><strong>方法要点：</strong>冻结 encoder 与原 task head，从已有 forward cache 中比较各 timestep 表征和当前 preference state，选择长程、近期或局部 burst 的纠正证据并做 residual repair。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 frozen-cache evidence selection 与 residual correction；用户批准为学术/Evolve 例外，无线上 A/B。收录例外：用户于 2026-10-02 明确批准的学术/Evolve 机制例外；论文没有量化线上 A/B，不进入工业证据结论。执行 frozen-cache evidence selection 与 residual correction；用户批准为学术/Evolve 例外，无线上 A/B。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01270">原论文</a> · <a href="../../../../reproductions/2610.01270-repair-state/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="HELIX: Purified and Unified - Rethinking Feature Interaction and Sequence Modeling for Large-Scale Recommendation 搜广推与 LLM 应用 TikTok / ByteDance 2026-09-29 工业排序通常分别扩大异构特征交互与长行为序列，两条轴单独扩展都会遇到上限。HELIX 交错 SeqFormer 与 MixFormer，但强制信息只从可复用的 user-only sequence state 流向 candidate-conditioned mix tokens，使用户侧序列计算能跨候选复用，同时保持两轴的跨深度通信。 复现级别：L1 架构机制。复现级别：L1 架构机制。实现三流 token、单向 U-only 缓存、跨深度 MixFormer/SeqFormer 交互与多任务头；没有 TikTok 私有数据和线上流量。本地使用合成张量，不含私有训练数据、线上 A/B 或论文规模系统优化，因此 reproduction_level=concept_demo。只有接入公开公平数据、基线和多种子 validation/test 隔离后，才能讨论效果复现或进入 Evolve 搜索空间。本地对照口径：基线为同一 user cache 下的候选 A，实验组为候选 B；只检查候选敏感性与 cache 不变量，没有公开效果指标，相对变化不适用。  ranking feature-interaction sequence-modeling 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-helix-94ed43e6">HELIX: Purified and Unified - Rethinking Feature Interaction and Sequence Modeling for Large-Scale Recommendation</h2>
<p class="ar-learning-card__meta">TikTok / ByteDance · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>工业排序通常分别扩大异构特征交互与长行为序列，两条轴单独扩展都会遇到上限。HELIX 交错 SeqFormer 与 MixFormer，但强制信息只从可复用的 user-only sequence state 流向 candidate-conditioned mix tokens，使用户侧序列计算能跨候选复用，同时保持两轴的跨深度通信。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 架构机制。复现级别：L1 架构机制。实现三流 token、单向 U-only 缓存、跨深度 MixFormer/SeqFormer 交互与多任务头；没有 TikTok 私有数据和线上流量。本地使用合成张量，不含私有训练数据、线上 A/B 或论文规模系统优化，因此 reproduction_level=concept_demo。只有接入公开公平数据、基线和多种子 validation/test 隔离后，才能讨论效果复现或进入 Evolve 搜索空间。本地对照口径：基线为同一 user cache 下的候选 A，实验组为候选 B；只检查候选敏感性与 cache 不变量，没有公开效果指标，相对变化不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37183">原论文</a> · <a href="../../../../reproductions/2609.37183-helix/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Beyond Interaction Capacity: Estimator Scaling with Recursive Models for CTR Prediction 搜广推与 LLM 应用 Georgia Institute of Technology / Google Research 2026-09-29 不再只增加单个 CTR predictor 的交互容量，而是扩展相关 estimator；RECAP 在共享参数的递归 backbone 上形成多条 route，并结合独立模型蒸馏、训练轨迹 EMA 与推理 route 平均。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行共享递归、route 平均、trajectory EMA 和可运行 RankMixer Evolve block；未做 benchmark 训练或独立模型蒸馏。执行共享递归、route 平均、trajectory EMA 和可运行 RankMixer Evolve block；未做 benchmark 训练或独立模型蒸馏。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  ctr estimator-scaling recursive-network 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-recap-ctr-8a9efe0a">Beyond Interaction Capacity: Estimator Scaling with Recursive Models for CTR Prediction</h2>
<p class="ar-learning-card__meta">Georgia Institute of Technology / Google Research · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>不再只增加单个 CTR predictor 的交互容量，而是扩展相关 estimator；RECAP 在共享参数的递归 backbone 上形成多条 route，并结合独立模型蒸馏、训练轨迹 EMA 与推理 route 平均。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行共享递归、route 平均、trajectory EMA 和可运行 RankMixer Evolve block；未做 benchmark 训练或独立模型蒸馏。执行共享递归、route 平均、trajectory EMA 和可运行 RankMixer Evolve block；未做 benchmark 训练或独立模型蒸馏。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37905">原论文</a> · <a href="../../../../reproductions/2609.37905-recap-ctr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OneTrans-V2: Unifying Retrieval, Pre-rank, and Fine-rank with One Transformer in Industrial Recommender 搜广推与 LLM 应用 ByteDance 2026-09-23 工业推荐先检索海量候选，再预排缩小集合，最后精排。三套独立模型会反复编码同一用户历史，也难以让精排经验稳定反馈给上游。OneTrans-V2 保留三个阶段各自的输入与目标，却让它们共享一个因果 Transformer 用户上下文。行为序列不读阶段 token；每个阶段 token 只读请求时刻前的行为，不在阶段之间交叉读取。这既复用昂贵的用户编码，也防止未来信息泄漏。 故 adapter 标记为 concept_demo，不声称复刻 GMV、QPS 或完整 DCGR 业务控制。Fidelity：概念验证（非论文完整复现）；证据等级：L1 机制验证，使用完整 MovieLens-1M。三阶段核心计算与损失已执行，但公开 MovieLens 没有交易、广告供给和真实曝光漏斗，不能把代理指标解释为论文的业务提升。已执行共享因果用户编码、阶段隔离、三级 SID 自回归、可观测代理决策、双阶段多目标 BCE 与精排向预排蒸馏。未执行真实购买/金额/广告决策、工业物品编码、稀疏 MoE、Sequence-Native Training 的跨曝光摊销、线上服务与 A/B。  multi-stage-ranking generative-retrieval cross-stage-distillation 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-onetrans-v2-65020d24">OneTrans-V2: Unifying Retrieval, Pre-rank, and Fine-rank with One Transformer in Industrial Recommender</h2>
<p class="ar-learning-card__meta">ByteDance · 论文公开：2026-09-23</p>
<p><strong>方法要点：</strong>工业推荐先检索海量候选，再预排缩小集合，最后精排。三套独立模型会反复编码同一用户历史，也难以让精排经验稳定反馈给上游。OneTrans-V2 保留三个阶段各自的输入与目标，却让它们共享一个因果 Transformer 用户上下文。行为序列不读阶段 token；每个阶段 token 只读请求时刻前的行为，不在阶段之间交叉读取。这既复用昂贵的用户编码，也防止未来信息泄漏。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>故 adapter 标记为 concept_demo，不声称复刻 GMV、QPS 或完整 DCGR 业务控制。Fidelity：概念验证（非论文完整复现）；证据等级：L1 机制验证，使用完整 MovieLens-1M。三阶段核心计算与损失已执行，但公开 MovieLens 没有交易、广告供给和真实曝光漏斗，不能把代理指标解释为论文的业务提升。已执行共享因果用户编码、阶段隔离、三级 SID 自回归、可观测代理决策、双阶段多目标 BCE 与精排向预排蒸馏。未执行真实购买/金额/广告决策、工业物品编码、稀疏 MoE、Sequence-Native Training 的跨曝光摊销、线上服务与 A/B。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.28589">原论文</a> · <a href="../../../../reproductions/2609.28589-onetrans-v2/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="LazFormer: Scaling Transformers for Industrial Recommendation via Transferable Generative Pre-training 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-09-14 先做可迁移生成式预训练，再用 ranking residual adapter、近密远疏 token 与 hybrid sparse attention 适配排序；两周 A/B 报告 IPV +5.21%、GMV +9.85%。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。私有日志、生产 checkpoint 与 serving 栈均未复刻。本地只验证公开数据上的核心状态转换；未复刻私有训练数据、大模型生成器、生产流量反馈或在线服务。当前不映射 evolve，避免 registry-only 标签。线上数字来自论文正文 A/B，不与本地 MovieLens 结果混写。本地 seeds 42/43/44 见 metrics/movielens-100k-seeds42-44.json。首个 seed 的统一 NDCG@10 基线为 0.05401，实验组为 0.05048，相对变化 -6.53%。  ranking generative-pretraining residual-adapter hybrid-sparse-attention 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-lazformer-e00dc3de">LazFormer: Scaling Transformers for Industrial Recommendation via Transferable Generative Pre-training</h2>
<p class="ar-learning-card__meta">Alibaba International Digital Commerce Group · 论文公开：2026-09-14</p>
<p><strong>方法要点：</strong>先做可迁移生成式预训练，再用 ranking residual adapter、近密远疏 token 与 hybrid sparse attention 适配排序；两周 A/B 报告 IPV +5.21%、GMV +9.85%。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：公开数据核心机制。复现级别：公开数据核心机制。私有日志、生产 checkpoint 与 serving 栈均未复刻。本地只验证公开数据上的核心状态转换；未复刻私有训练数据、大模型生成器、生产流量反馈或在线服务。当前不映射 evolve，避免 registry-only 标签。线上数字来自论文正文 A/B，不与本地 MovieLens 结果混写。本地 seeds 42/43/44 见 metrics/movielens-100k-seeds42-44.json。首个 seed 的统一 NDCG@10 基线为 0.05401，实验组为 0.05048，相对变化 -6.53%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.14978">原论文</a> · <a href="../../../../reproductions/2609.14978-lazformer/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="ChronicleRec: Pre-training Temporally Anchored Tokens for Lifelong User Modeling 搜广推与 LLM 应用 Tencent 2026-09-11 逐候选检索超长历史会重复计算，统一压成无序 token 又容易丢失时间结构。ChronicleRec 对近、中、远历史采用逐渐增大的合并步幅，把 query token 插入时间轴并使用 causal encoder，使每个 token 只概括其锚点之前的历史；多分支分别遮掉不同长度的近期行为，alignment 预训练再用压缩过去预测近期意图。生成的 Chronicle Tokens 与候选无关，可缓存并复用于多个候选。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行近密远疏合并、因果 query 锚点、多 horizon 分支与面向近期目标的 alignment；不复刻腾讯私有 MixFormer 与缓存系统。公开短序列不能代表 2K–4K 乃至更长的生产历史；本地用线性 alignment 替代四层 causal Transformer，未复刻 AdLive、MixFormer 和异步 KV cache。实现只声明 CPU 公开数据核心机制。MovieLens 100K、seeds 42/43/44 的固定协议见 metrics/movielens-100k-seeds42-44.json。  ranking long-sequence sequence-compression pretraining 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-chronicle-rec-efcf1d9a">ChronicleRec: Pre-training Temporally Anchored Tokens for Lifelong User Modeling</h2>
<p class="ar-learning-card__meta">Tencent · 论文公开：2026-09-11</p>
<p><strong>方法要点：</strong>逐候选检索超长历史会重复计算，统一压成无序 token 又容易丢失时间结构。ChronicleRec 对近、中、远历史采用逐渐增大的合并步幅，把 query token 插入时间轴并使用 causal encoder，使每个 token 只概括其锚点之前的历史；多分支分别遮掉不同长度的近期行为，alignment 预训练再用压缩过去预测近期意图。生成的 Chronicle Tokens 与候选无关，可缓存并复用于多个候选。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行近密远疏合并、因果 query 锚点、多 horizon 分支与面向近期目标的 alignment；不复刻腾讯私有 MixFormer 与缓存系统。公开短序列不能代表 2K–4K 乃至更长的生产历史；本地用线性 alignment 替代四层 causal Transformer，未复刻 AdLive、MixFormer 和异步 KV cache。实现只声明 CPU 公开数据核心机制。MovieLens 100K、seeds 42/43/44 的固定协议见 metrics/movielens-100k-seeds42-44.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.12375">原论文</a> · <a href="../../../../reproductions/2609.12375-chronicle-rec/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="UniRec: Cross-Stage Multi-Task Fusion with Preference Optimization for Cascaded Recommender Systems 搜广推与 LLM 应用 Kuaishou 2026-09-10 预排和精排的候选范围、输入质量和延迟约束不同，直接复制精排的融合权重不能保证上游排序一致。UniRec 以部分共享 embedding、独立 DCN/Mixer 与 AutoInt-Lite 塔联合训练两阶段融合模块；下游偏好只作为上游训练监督，不作为预排线上输入。v3 明确保留多目标冲突的 CPPA、置信剪枝 CAPP，以及以组内 KL 抑制视频时长等属性引起的分布漂移。 成本过高，不复现（审查 DONE）。复现级别：组件诊断，非完整论文复现。复现级别：组件诊断，非完整论文复现。新增 v3 的 CPPA/CAPP、AGRR 组内 KL 与跨阶段偏好目标，验证前向、梯度和负对照。旧 unirec NumPy adapter 是固定权重启发式，现明确降为 concept_demo；历史测量与负结果完整保留。旧 MovieLens 100K、seeds 42/43/44 结果见 metrics/movielens-100k-seeds42-44.json。  pre-ranking ranking cross-stage-alignment industrial-recommendation 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-unirec-cd2efe22">UniRec: Cross-Stage Multi-Task Fusion with Preference Optimization for Cascaded Recommender Systems</h2>
<p class="ar-learning-card__meta">Kuaishou · 论文公开：2026-09-10</p>
<p><strong>方法要点：</strong>预排和精排的候选范围、输入质量和延迟约束不同，直接复制精排的融合权重不能保证上游排序一致。UniRec 以部分共享 embedding、独立 DCN/Mixer 与 AutoInt-Lite 塔联合训练两阶段融合模块；下游偏好只作为上游训练监督，不作为预排线上输入。v3 明确保留多目标冲突的 CPPA、置信剪枝 CAPP，以及以组内 KL 抑制视频时长等属性引起的分布漂移。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。复现级别：组件诊断，非完整论文复现。复现级别：组件诊断，非完整论文复现。新增 v3 的 CPPA/CAPP、AGRR 组内 KL 与跨阶段偏好目标，验证前向、梯度和负对照。旧 unirec NumPy adapter 是固定权重启发式，现明确降为 concept_demo；历史测量与负结果完整保留。旧 MovieLens 100K、seeds 42/43/44 结果见 metrics/movielens-100k-seeds42-44.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11052">原论文</a> · <a href="../../../../reproductions/2609.11052-unirec/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="SequenceO1: End-to-End Ultra-Long (100K) Sequence Modeling in Recommendation with Low-Rank Caching 搜广推与 LLM 应用 ByteDance / Douyin 2026-09-08 直接注意全部历史难以服务 100K 级用户行为。SequenceO1 用 Sketch Attention 把远期历史压缩为固定数量原型，并保留近期行为分支；STCA 让 sketch 与 recent 信息并行交互，控制成本同时保留长期兴趣。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行固定预算 prototype sketch 与 recent 双分支；MovieLens 不具备论文的 100K 事件历史。MovieLens 100K 三种子结果见 metrics/movielens-100k-seeds42-44.json。原型由训练历史 farthest-first 初始化并做一次 assignment/update，固定为 4 个；未实现 MRLB、FlashSA 或线上 cache，且暂不登记不可执行的 evolve 标签。  long-sequence sketch-attention prototype-compression industrial-recommendation 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-sequenceo1-53b97674">SequenceO1: End-to-End Ultra-Long (100K) Sequence Modeling in Recommendation with Low-Rank Caching</h2>
<p class="ar-learning-card__meta">ByteDance / Douyin · 论文公开：2026-09-08</p>
<p><strong>方法要点：</strong>直接注意全部历史难以服务 100K 级用户行为。SequenceO1 用 Sketch Attention 把远期历史压缩为固定数量原型，并保留近期行为分支；STCA 让 sketch 与 recent 信息并行交互，控制成本同时保留长期兴趣。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行固定预算 prototype sketch 与 recent 双分支；MovieLens 不具备论文的 100K 事件历史。MovieLens 100K 三种子结果见 metrics/movielens-100k-seeds42-44.json。原型由训练历史 farthest-first 初始化并做一次 assignment/update，固定为 4 个；未实现 MRLB、FlashSA 或线上 cache，且暂不登记不可执行的 evolve 标签。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08443">原论文</a> · <a href="../../../../reproductions/2609.08443-sequenceo1/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="From Language to Behavior: Scaling Sequence Transformers for Industrial Recommendation Ranking with Rec-Native Designs 搜广推与 LLM 应用 ByteDance 2026-09-01 ReST 不直接照搬语言 Transformer：双门控注意力抑制行为噪声，RoPE 与相对时间编码同时表达顺序和时间间隔；系统侧把一次请求拆成可复用的重型用户 encoder 与轻型候选 cross decoder，实现 compute-once、decode-many。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现双门控时序编码、重用户编码/轻候选交叉的计算路径。未复刻私有行为日志、生产 checkpoint 和 shared-prefix serving kernel；本实现仅声明 CPU 公共数据核心机制，不宣传 CUDA 路径。在 MovieLens 100K 固定 220 用户/360 物品协议上执行时序衰减、信号门控与候选交叉路径；三 seed 结果见 metrics/public-seeds42-44.json。  ranking-network long-sequence shared-prefix-serving 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-rest-5ed56a69">From Language to Behavior: Scaling Sequence Transformers for Industrial Recommendation Ranking with Rec-Native Designs</h2>
<p class="ar-learning-card__meta">ByteDance · 论文公开：2026-09-01</p>
<p><strong>方法要点：</strong>ReST 不直接照搬语言 Transformer：双门控注意力抑制行为噪声，RoPE 与相对时间编码同时表达顺序和时间间隔；系统侧把一次请求拆成可复用的重型用户 encoder 与轻型候选 cross decoder，实现 compute-once、decode-many。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现双门控时序编码、重用户编码/轻候选交叉的计算路径。未复刻私有行为日志、生产 checkpoint 和 shared-prefix serving kernel；本实现仅声明 CPU 公共数据核心机制，不宣传 CUDA 路径。在 MovieLens 100K 固定 220 用户/360 物品协议上执行时序衰减、信号门控与候选交叉路径；三 seed 结果见 metrics/public-seeds42-44.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.01240">原论文</a> · <a href="../../../../reproductions/2609.01240-rest/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OneModel: A Unified Foundation for Platform-Scale Multi-Scenario Ranking 搜广推与 LLM 应用 Xiaohongshu 2026-08-19 推荐、广告和商家推荐通常各训一套排序模型，既重复消耗资源，也无法充分共享跨场景行为。OneModel 将异构特征先投影到统一 event token，再以共享 causal decoder 建模混合长历史；SAIM 用场景条件 gate 调制 FFN，分层表征同时保留全局 attentive pooling 与最近局部状态，从而兼顾迁移与专门化。 Fidelity: 核心机制复现。本地真实执行多场景统计、场景投影、SAIM 式门控和全局/局部分层表征；生产 Transformer 与私有特征未复刻。使用本地 MovieLens-1M 公开数据；没有小红书私有多流日志、action token、统一 Transformer decoder、训练早期梯度隔离、选择性反向传播和在线 serving。核心场景门控路径已执行，但本地指标只验证机制与失败边界。本地对照口径：基线为共享全局转移排序器；实验组加入由 MovieLens genre 派生的三个场景、场景转移、sigmoid 门控和 global/local 融合。  ranking multi-scenario foundation-model long-sequence 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-onemodel-224b06a8">OneModel: A Unified Foundation for Platform-Scale Multi-Scenario Ranking</h2>
<p class="ar-learning-card__meta">Xiaohongshu · 论文公开：2026-08-19</p>
<p><strong>方法要点：</strong>推荐、广告和商家推荐通常各训一套排序模型，既重复消耗资源，也无法充分共享跨场景行为。OneModel 将异构特征先投影到统一 event token，再以共享 causal decoder 建模混合长历史；SAIM 用场景条件 gate 调制 FFN，分层表征同时保留全局 attentive pooling 与最近局部状态，从而兼顾迁移与专门化。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地真实执行多场景统计、场景投影、SAIM 式门控和全局/局部分层表征；生产 Transformer 与私有特征未复刻。使用本地 MovieLens-1M 公开数据；没有小红书私有多流日志、action token、统一 Transformer decoder、训练早期梯度隔离、选择性反向传播和在线 serving。核心场景门控路径已执行，但本地指标只验证机制与失败边界。本地对照口径：基线为共享全局转移排序器；实验组加入由 MovieLens genre 派生的三个场景、场景转移、sigmoid 门控和 global/local 融合。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.18606">原论文</a> · <a href="../../../../reproductions/2608.18606-onemodel/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="GenRec: An LLM-Backed Recommendation Ranker at Netflix 搜广推与 LLM 应用 Netflix 2026-08-10 传统 Netflix 排序系统依赖大量人工特征、特征交互和场景专用网络。新增内容形态或推荐场景时，往往要重新设计特征、模型和基础设施。GenRec 把问题从“特征工程”转成“上下文工程”：把用户历史、内容元数据、设备和时间等信号表达成文本，让共享 LLM 主干学习语义与高阶交互。论文采用两阶段训练：Phase 1 在开源 LLM 上继续训练 Netflix 内容和用户数据，获得内部 foundation LLM； Fidelity：核心机制复现。本地真实加载 causal LLM、执行 LoRA Phase-2 后训练、文本化用户历史、全目录 catalog-aware ranking head、联合语言/排序目标和 reward-weighted loss；Netflix 私有 Phase-1 基座与线上 reward model 不可公开，未用固定规则冒充。Netflix 内部 Phase-1 foundation LLM、数千生产特征和数千亿交互事件不可获得；本地使用公开 SmolLM2 和 MovieLens 文本/反馈。  ranking llm-recommendation post-training reward-weighting context-engineering training-serving 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-genrec-netflix-691b65fa">GenRec: An LLM-Backed Recommendation Ranker at Netflix</h2>
<p class="ar-learning-card__meta">Netflix · 论文公开：2026-08-10</p>
<p><strong>方法要点：</strong>传统 Netflix 排序系统依赖大量人工特征、特征交互和场景专用网络。新增内容形态或推荐场景时，往往要重新设计特征、模型和基础设施。GenRec 把问题从“特征工程”转成“上下文工程”：把用户历史、内容元数据、设备和时间等信号表达成文本，让共享 LLM 主干学习语义与高阶交互。论文采用两阶段训练：Phase 1 在开源 LLM 上继续训练 Netflix 内容和用户数据，获得内部 foundation LLM；</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity：核心机制复现。本地真实加载 causal LLM、执行 LoRA Phase-2 后训练、文本化用户历史、全目录 catalog-aware ranking head、联合语言/排序目标和 reward-weighted loss；Netflix 私有 Phase-1 基座与线上 reward model 不可公开，未用固定规则冒充。Netflix 内部 Phase-1 foundation LLM、数千生产特征和数千亿交互事件不可获得；本地使用公开 SmolLM2 和 MovieLens 文本/反馈。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.10257">原论文</a> · <a href="../../../../reproductions/2608.10257-genrec-netflix/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="IntHQ: Task-Interactive Hierarchical Query on Dual-Stream Representations for Generative Recommendation 搜广推与 LLM 应用 Amap / Alibaba 2026-08-10 双流分别保留行为与上下文表示，when/where/how/via 四个任务查询在多个层级交互检索，使任务信号进入编码器而非只留在任务头。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  multi-task-learning generative-recommendation long-sequence 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-inthq-fbf3d84e">IntHQ: Task-Interactive Hierarchical Query on Dual-Stream Representations for Generative Recommendation</h2>
<p class="ar-learning-card__meta">Amap / Alibaba · 论文公开：2026-08-10</p>
<p><strong>方法要点：</strong>双流分别保留行为与上下文表示，when/where/how/via 四个任务查询在多个层级交互检索，使任务信号进入编码器而非只留在任务头。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.09634">原论文</a> · <a href="../../../../reproductions/2608.09634-inthq/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Teacher Retains Full Tokens, Student Merges Efficiently: TM20K for E-Commerce Sequence Modeling in Ad Recommendation 搜广推与 LLM 应用 ByteDance 2026-08-07 教师网络保留完整行为 token 提供细粒度监督，学生把连续行为按组以 sum/√n 合并到固定 token 预算，再蒸馏教师注意力与排序分布，兼顾长序列信息和线上成本。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为无蒸馏的合并 token student，实验组从 full-token teacher 蒸馏；seed 42 的 NDCG@10 为 0.04022，基线为 0.03446。  advertising long-sequence token-merging distillation 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-tm20k-e967dab7">Teacher Retains Full Tokens, Student Merges Efficiently: TM20K for E-Commerce Sequence Modeling in Ad Recommendation</h2>
<p class="ar-learning-card__meta">ByteDance · 论文公开：2026-08-07</p>
<p><strong>方法要点：</strong>教师网络保留完整行为 token 提供细粒度监督，学生把连续行为按组以 sum/√n 合并到固定 token 预算，再蒸馏教师注意力与排序分布，兼顾长序列信息和线上成本。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为无蒸馏的合并 token student，实验组从 full-token teacher 蒸馏；seed 42 的 NDCG@10 为 0.04022，基线为 0.03446。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.07055">原论文</a> · <a href="../../../../reproductions/2608.07055-tm20k/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TransX: Scaling Transformer-based Recommendation via Behavioral and Serving Stream Crossings 搜广推与 LLM 应用 LinkedIn 2026-07-31 将可离线缓存的长行为流与请求时产生的短服务流解耦；行为端形成 global/local 缓存，候选端只对缓存做 cross-attention，从而避免每个请求重算完整 self-attention。 成本过高，不复现（审查 DONE）：报告的 32 H200、约 13 小时收敛、生产 Kafka/KV/多租户服务和完整多基准实验不在本批预算内。它们是公式/梯度诊断，不是新的推荐得分；历史 adapter：concept demo。model.py 的 NumPy 路径使用固定权重与既有特征，没有训练论文网络；历史结果原样保留，但不再标成核心模型训练或正式能力比较。下文另列本次技术报告的真实可微组件及独立验收证据。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；  ranking long-sequence cross-attention serving 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-transx-58683026">TransX: Scaling Transformer-based Recommendation via Behavioral and Serving Stream Crossings</h2>
<p class="ar-learning-card__meta">LinkedIn · 论文公开：2026-07-31</p>
<p><strong>方法要点：</strong>将可离线缓存的长行为流与请求时产生的短服务流解耦；行为端形成 global/local 缓存，候选端只对缓存做 cross-attention，从而避免每个请求重算完整 self-attention。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）：报告的 32 H200、约 13 小时收敛、生产 Kafka/KV/多租户服务和完整多基准实验不在本批预算内。它们是公式/梯度诊断，不是新的推荐得分；历史 adapter：concept demo。model.py 的 NumPy 路径使用固定权重与既有特征，没有训练论文网络；历史结果原样保留，但不再标成核心模型训练或正式能力比较。下文另列本次技术报告的真实可微组件及独立验收证据。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28940">原论文</a> · <a href="../../../../reproductions/2607.28940-transx/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="CCFormer: Efficient Cross-Field Interaction and Hierarchical Sequence Compression for Industrial Recommendation at Tencent 搜广推与 LLM 应用 Tencent Platform and Content Group 2026-07-30 工业排序既要细粒度字段交互，又要吃进千长度行为序列。CCFormer 让 ID、内容等字段先分离投影再 cross attention，并用逐层扩大感受野的 token mixing 压缩旧历史，近期行为保持细粒度。 Fidelity: 核心机制复现。实现跨字段门控、分层旧序列压缩和 recent-token 保留；不复刻腾讯私有数据与 kernel。未包含 40 亿私有样本、千长度线上序列、并行多 target kernel；本地结果只验证机制方向。本地对照口径：基线为同预算 GRU；实验组为 CCFormer core，相对基线 NDCG@10 +22.44%。  ranking long-sequence sequence-compression token-mixing 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-ccformer-b04b720c">CCFormer: Efficient Cross-Field Interaction and Hierarchical Sequence Compression for Industrial Recommendation at Tencent</h2>
<p class="ar-learning-card__meta">Tencent Platform and Content Group · 论文公开：2026-07-30</p>
<p><strong>方法要点：</strong>工业排序既要细粒度字段交互，又要吃进千长度行为序列。CCFormer 让 ID、内容等字段先分离投影再 cross attention，并用逐层扩大感受野的 token mixing 压缩旧历史，近期行为保持细粒度。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。实现跨字段门控、分层旧序列压缩和 recent-token 保留；不复刻腾讯私有数据与 kernel。未包含 40 亿私有样本、千长度线上序列、并行多 target kernel；本地结果只验证机制方向。本地对照口径：基线为同预算 GRU；实验组为 CCFormer core，相对基线 NDCG@10 +22.44%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28070">原论文</a> · <a href="../../../../reproductions/2607.28070-ccformer/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Heterogeneous Ranking in Industrial-Scale Recommender Systems: A Case Study 搜广推与 LLM 应用 Google / Discover 2026-07-30 Discover 要在同一 feed 中比较新闻、视频、体育等开放网页内容，单一共享塔会让高频内容支配梯度。HA-MoE 用内容异构性特征控制 multi-gate MoE，把通用信号与领域专长分开；LENS 则追踪 expert 使用率和分领域 DL-AUC，避免总体指标掩盖局部退化。 Fidelity: 核心机制复现。本地执行异构性度量、专长 expert 与多门控融合，不把 MovieLens 代理实验写成 Google Discover 生产复刻。MovieLens genre 代理开放网页内容类型；未复刻 Discover 私有样本、LENS 生产观测系统和 DL-AUC 服务。本地对照口径：基线为同切分的 homogeneous transition-content ranker，实验组加入 HA-MoE；NDCG@10 相对 -1.77%。  ranking mixture-of-experts heterogeneity diversity 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-ha-moe-beffade8">Heterogeneous Ranking in Industrial-Scale Recommender Systems: A Case Study</h2>
<p class="ar-learning-card__meta">Google / Discover · 论文公开：2026-07-30</p>
<p><strong>方法要点：</strong>Discover 要在同一 feed 中比较新闻、视频、体育等开放网页内容，单一共享塔会让高频内容支配梯度。HA-MoE 用内容异构性特征控制 multi-gate MoE，把通用信号与领域专长分开；LENS 则追踪 expert 使用率和分领域 DL-AUC，避免总体指标掩盖局部退化。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地执行异构性度量、专长 expert 与多门控融合，不把 MovieLens 代理实验写成 Google Discover 生产复刻。MovieLens genre 代理开放网页内容类型；未复刻 Discover 私有样本、LENS 生产观测系统和 DL-AUC 服务。本地对照口径：基线为同切分的 homogeneous transition-content ranker，实验组加入 HA-MoE；NDCG@10 相对 -1.77%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27577">原论文</a> · <a href="../../../../reproductions/2607.27577-ha-moe/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="ClockRoPE: Random Fourier Rotations for Temporal Routine Modeling 搜广推与 LLM 应用 YouTube / Google DeepMind 2026-07-29 普通 RoPE 的对数线性频率偏向“距离越远相关性越弱”，但推荐行为常有日周期和周周期。ClockRoPE 从目标周期 kernel 的 Fourier 变换中采样旋转频率，使 query-key 点积在相同小时或星期附近重新增强，并可与标准 RoPE 各占一半通道。 Fidelity: 核心机制复现。本地执行周期 Gaussian Fourier kernel 对序列注意力的调制；公开数据缺少 YouTube 的小时级行为语境，因此结果只验证机制和边界。公开 MovieLens 只提供稀疏评分时间，本地用确定性事件间隔构造周期位置；未复刻 YouTube 私有日志、生成式检索模型、TPU kernel 和线上 serving。本地对照口径：基线为不使用周期调制的 RoPE-style recency ranker；实验组加入日/周 ClockRoPE kernel，NDCG@10 相对 -2.30%。  generative-retrieval temporal-modeling rope long-sequence 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-clockrope-0d0da402">ClockRoPE: Random Fourier Rotations for Temporal Routine Modeling</h2>
<p class="ar-learning-card__meta">YouTube / Google DeepMind · 论文公开：2026-07-29</p>
<p><strong>方法要点：</strong>普通 RoPE 的对数线性频率偏向“距离越远相关性越弱”，但推荐行为常有日周期和周周期。ClockRoPE 从目标周期 kernel 的 Fourier 变换中采样旋转频率，使 query-key 点积在相同小时或星期附近重新增强，并可与标准 RoPE 各占一半通道。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地执行周期 Gaussian Fourier kernel 对序列注意力的调制；公开数据缺少 YouTube 的小时级行为语境，因此结果只验证机制和边界。公开 MovieLens 只提供稀疏评分时间，本地用确定性事件间隔构造周期位置；未复刻 YouTube 私有日志、生成式检索模型、TPU kernel 和线上 serving。本地对照口径：基线为不使用周期调制的 RoPE-style recency ranker；实验组加入日/周 ClockRoPE kernel，NDCG@10 相对 -2.30%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26369">原论文</a> · <a href="../../../../reproductions/2607.26369-clockrope/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="SpecFormer: Mitigating Embedding and Attention Collapse via Spectral-Aware Transformer for Recommendation 搜广推与 LLM 应用 Zhejiang University 2026-07-27 以奇异值谱软化和谱残差位置编码，抑制推荐 Transformer 的 embedding/attention collapse。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 SpecFormer 为 0.04999，相对变化 -7.44%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  ranking transformer spectral-softening 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-specformer-bc626a07">SpecFormer: Mitigating Embedding and Attention Collapse via Spectral-Aware Transformer for Recommendation</h2>
<p class="ar-learning-card__meta">Zhejiang University · 论文公开：2026-07-27</p>
<p><strong>方法要点：</strong>以奇异值谱软化和谱残差位置编码，抑制推荐 Transformer 的 embedding/attention collapse。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 SpecFormer 为 0.04999，相对变化 -7.44%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24025">原论文</a> · <a href="../../../../reproductions/2607.24025-specformer/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="WHALE: A Scalable Unified Model for Recommendation with Wukong-HSTU Architecture 搜广推与 LLM 应用 Meta Platforms, Inc. 2026-07-19 工业推荐通常把稀疏特征交互和用户行为序列分成两个模型，扩展规模时容易形成表示与算力割裂。WHALE 用 Wukong 分支递归建模高阶特征交互，用 HSTU 分支建模行为序列，并在每层用 cross-attention 双向交换状态，形成可共同扩展的统一网络。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练 Wukong、HSTU 与逐层交换；Meta 私有特征规模和生产内核未复刻。本地实际训练 Wukong 乘性交互、门控因果 HSTU 和逐层 cross-branch attention，并以同维度、同层数的 late-fusion Transformer 为直接对照。  ranking hstu feature-interaction scaling 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-whale-9ea1c28b">WHALE: A Scalable Unified Model for Recommendation with Wukong-HSTU Architecture</h2>
<p class="ar-learning-card__meta">Meta Platforms, Inc. · 论文公开：2026-07-19</p>
<p><strong>方法要点：</strong>工业推荐通常把稀疏特征交互和用户行为序列分成两个模型，扩展规模时容易形成表示与算力割裂。WHALE 用 Wukong 分支递归建模高阶特征交互，用 HSTU 分支建模行为序列，并在每层用 cross-attention 双向交换状态，形成可共同扩展的统一网络。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练 Wukong、HSTU 与逐层交换；Meta 私有特征规模和生产内核未复刻。本地实际训练 Wukong 乘性交互、门控因果 HSTU 和逐层 cross-branch attention，并以同维度、同层数的 late-fusion Transformer 为直接对照。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.17017">原论文</a> · <a href="../../../../reproductions/2607.17017-whale/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Long-History User Transformers for Real-Time Ad Ranking 搜广推与 LLM 应用 Yandex 2026-07-15 广告排序需要长历史，但请求时重算完整序列会增加延迟。论文把系统拆成异步 full-history Transformer 和在线 lightweight Transformer：离线部分周期性刷新固定维度用户状态，在线只编码最近事件并读取缓存；训练先用 next-event 与 feedback 辅助任务预训练，再针对目标广告 surface 微调。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练离线缓存与在线近期双 encoder；Yandex 生产特征系统未复刻。代码实际训练 24 步长的离线历史 encoder、32 维缓存、仅查看最近 4 个事件的在线 encoder，以及 next-item/feedback 辅助目标；基线只能在请求时查看最近 4 个事件。  advertising long-sequence cached-user-representation serving 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-long-history-transformer-f4293ee0">Long-History User Transformers for Real-Time Ad Ranking</h2>
<p class="ar-learning-card__meta">Yandex · 论文公开：2026-07-15</p>
<p><strong>方法要点：</strong>广告排序需要长历史，但请求时重算完整序列会增加延迟。论文把系统拆成异步 full-history Transformer 和在线 lightweight Transformer：离线部分周期性刷新固定维度用户状态，在线只编码最近事件并读取缓存；训练先用 next-event 与 feedback 辅助任务预训练，再针对目标广告 surface 微调。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练离线缓存与在线近期双 encoder；Yandex 生产特征系统未复刻。代码实际训练 24 步长的离线历史 encoder、32 维缓存、仅查看最近 4 个事件的在线 encoder，以及 next-item/feedback 辅助目标；基线只能在请求时查看最近 4 个事件。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14331">原论文</a> · <a href="../../../../reproductions/2607.14331-long-history-transformer/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TMallGS: Scaling Unified Feature and Sequence Modeling for Generative E-commerce Search 搜广推与 LLM 应用 Taobao &amp; Tmall Group of Alibaba 2026-07-15 电商搜索同时包含 query、短期/长期行为、用户和商品等异构字段，直接拼 token 会放大字段噪声。TMallGS 为不同字段学习独立 Q/K/V，用 distribution-calibrated saliency 和 noise-adaptive gate 控制交互；内容特征通过 FiLM 注入，context bias 修正最终分数，并用中间层误差自适应分配 progressive supervision。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练 field-adaptive 交互和 progressive loss；天猫私有字段与生产规模未复刻。本地把 MovieLens 类型和序列映射为异构字段，真实训练 field-wise QKV、噪声门控、显式内容 FiLM、context bias 和 error-aware progressive loss。  search-ranking transformer scaling feature-interaction 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-tmallgs-f2b12094">TMallGS: Scaling Unified Feature and Sequence Modeling for Generative E-commerce Search</h2>
<p class="ar-learning-card__meta">Taobao &amp; Tmall Group of Alibaba · 论文公开：2026-07-15</p>
<p><strong>方法要点：</strong>电商搜索同时包含 query、短期/长期行为、用户和商品等异构字段，直接拼 token 会放大字段噪声。TMallGS 为不同字段学习独立 Q/K/V，用 distribution-calibrated saliency 和 noise-adaptive gate 控制交互；内容特征通过 FiLM 注入，context bias 修正最终分数，并用中间层误差自适应分配 progressive supervision。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练 field-adaptive 交互和 progressive loss；天猫私有字段与生产规模未复刻。本地把 MovieLens 类型和序列映射为异构字段，真实训练 field-wise QKV、噪声门控、显式内容 FiLM、context bias 和 error-aware progressive loss。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.13398">原论文</a> · <a href="../../../../reproductions/2607.13398-tmallgs/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Not Only NTP: Extending Training Signal Coverage for Generative Recommendation 搜广推与 LLM 应用 Meituan 2026-07-14 标准 next-token prediction 只要求当前位置预测紧邻的下一个物品：它既没有监督 hidden state 理解更远的未来轨迹，也没有让跨业务上下文直接更新稀疏域目标物品。NONTP 将前者称为 temporal locality，后者称为 spatial locality。TCL 用在线 backbone 的第个状态预测 EMA teacher 的第个未来状态，并只把其他用户序列作为负例； Fidelity: 核心机制复现。本地真实执行 NTP、EMA teacher、三个未来步 predictor、跨序列 InfoNCE、跨域 hidden-state pooling 与共享预测头；训练辅助分支在推理时全部移除。保留论文、、和两个辅助损失权重 0.1。本地对照口径：基线是相同 causal backbone、相同初始化和训练预算的 ntp；实验组是同时加入 TCL 与 TDL 的 nontp。三随机种子下 Hit@10 从 0.05079 降到 0.04828（-4.93%），NDCG@10 从 0.02431 降到 0.02222（-8.62%）。  generative-recommendation contrastive-learning multi-domain 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-nontp-bd610948">Not Only NTP: Extending Training Signal Coverage for Generative Recommendation</h2>
<p class="ar-learning-card__meta">Meituan · 论文公开：2026-07-14</p>
<p><strong>方法要点：</strong>标准 next-token prediction 只要求当前位置预测紧邻的下一个物品：它既没有监督 hidden state 理解更远的未来轨迹，也没有让跨业务上下文直接更新稀疏域目标物品。NONTP 将前者称为 temporal locality，后者称为 spatial locality。TCL 用在线 backbone 的第个状态预测 EMA teacher 的第个未来状态，并只把其他用户序列作为负例；</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地真实执行 NTP、EMA teacher、三个未来步 predictor、跨序列 InfoNCE、跨域 hidden-state pooling 与共享预测头；训练辅助分支在推理时全部移除。保留论文、、和两个辅助损失权重 0.1。本地对照口径：基线是相同 causal backbone、相同初始化和训练预算的 ntp；实验组是同时加入 TCL 与 TDL 的 nontp。三随机种子下 Hit@10 从 0.05079 降到 0.04828（-4.93%），NDCG@10 从 0.02431 降到 0.02222（-8.62%）。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12277">原论文</a> · <a href="../../../../reproductions/2607.12277-nontp/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Learning to Forget: Satiation-Aware Long-Sequence Transducers for Mitigating Post-Purchase Redundancy 搜广推与 LLM 应用 Alibaba Group 2026-07-14 购买完成的是一簇意图，继续放大购买前点击会制造重复推荐。SAM 用 pointwise cross-attention 定位要压制的历史节点，并从长期购买序列预测补货节奏；ASGU 在刚购买时强抑制、接近周期时逐渐恢复，再以 log-mask 修改注意力 logits。 Fidelity: 核心机制复现。双路径 intent/rhythm、ASGU、log-mask intervention 与 TTNP 周期监督均实际执行。没有真实补货型商品和 censored purchase log；只验证机制和失败边界。本地对照口径：基线是 DIN-like interest score；实验组 SAM 加入按 genre 学习的周期与 ASGU，相对基线 Hit@10 -12.50%、NDCG@10 -6.60%。  ranking long-sequence satiation 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-sam-b9df9dfc">Learning to Forget: Satiation-Aware Long-Sequence Transducers for Mitigating Post-Purchase Redundancy</h2>
<p class="ar-learning-card__meta">Alibaba Group · 论文公开：2026-07-14</p>
<p><strong>方法要点：</strong>购买完成的是一簇意图，继续放大购买前点击会制造重复推荐。SAM 用 pointwise cross-attention 定位要压制的历史节点，并从长期购买序列预测补货节奏；ASGU 在刚购买时强抑制、接近周期时逐渐恢复，再以 log-mask 修改注意力 logits。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。双路径 intent/rhythm、ASGU、log-mask intervention 与 TTNP 周期监督均实际执行。没有真实补货型商品和 censored purchase log；只验证机制和失败边界。本地对照口径：基线是 DIN-like interest score；实验组 SAM 加入按 genre 学习的周期与 ASGU，相对基线 Hit@10 -12.50%、NDCG@10 -6.60%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12714">原论文</a> · <a href="../../../../reproductions/2607.12714-sam/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="SlimPer: Make Personalization Model Slim and Smart 搜广推与 LLM 应用 Meta Platforms, Inc. 2026-07-14 SlimPer 每层用固定槽位的 user-item 知识库查询用户 token 池，执行 Select–Match–Refine。用户池保持可读，精炼层之间只传播小知识库；输入编码仍可带局部上下文。 本地只在短历史 MovieLens 上验证缩小机制；NDCG@10 +1.29% 仅为 seed 42 的 smoke，未实测生产 QPS 或显存。ROO 共享用户编码，候选相关知识库仍逐候选更新。 为什么用户 tokens 能共享，但 knowledge base 的更新结果不能全部共享？ ranking long-sequence serving-efficiency 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-slimper-ce7fc963">SlimPer: Make Personalization Model Slim and Smart</h2>
<p class="ar-learning-card__meta">Meta Platforms, Inc. · 论文公开：2026-07-14</p>
<p><strong>方法要点：</strong>SlimPer 每层用固定槽位的 user-item 知识库查询用户 token 池，执行 Select–Match–Refine。用户池保持可读，精炼层之间只传播小知识库；输入编码仍可带局部上下文。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本地只在短历史 MovieLens 上验证缩小机制；NDCG@10 +1.29% 仅为 seed 42 的 smoke，未实测生产 QPS 或显存。ROO 共享用户编码，候选相关知识库仍逐候选更新。</p></details>
<p class="ar-learning-question"><strong>想一想：</strong>为什么用户 tokens 能共享，但 knowledge base 的更新结果不能全部共享？</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12281">原论文</a> · <a href="../../../../reproductions/2607.12281-slimper/">实现解读</a> · <a href="../../../001-hstu-longer-slimper/">阅读精选对比</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="POEM: Partial-Order Enhanced Real-Time Sequential Modeling for Recommendation 搜广推与 LLM 应用 Kuaishou 2026-06-29 把当前请求多个排序目标产生的相对次序转成偏序信号，动态构造比纯时间序更贴近实时兴趣的训练序列。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 POEM 为 0.05009，相对变化 -7.25%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  sequential-recommendation partial-order real-time 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-poem-c8eda543">POEM: Partial-Order Enhanced Real-Time Sequential Modeling for Recommendation</h2>
<p class="ar-learning-card__meta">Kuaishou · 论文公开：2026-06-29</p>
<p><strong>方法要点：</strong>把当前请求多个排序目标产生的相对次序转成偏序信号，动态构造比纯时间序更贴近实时兴趣的训练序列。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 POEM 为 0.05009，相对变化 -7.25%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.29946">原论文</a> · <a href="../../../../reproductions/2606.29946-poem/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="CMSL: Constructive Multi-Sequence Learning for Recommendation Systems 搜广推与 LLM 应用 Meta 2026-06-26 把点击、观看、互动等所有行为塞进单一长序列会混合多个意图，且 self-attention 成本随长度快速增长。CMSL 不依赖预定义业务 taxonomy，而是利用当前上下文特征学习多个 contextual lens，把原始历史动态构造成 K 条 latent semantic sequence；每条 strand 独立编码，再用当前非序列上下文作为 query 做 PMA 聚合。论文还给出 degree-2 polynomial feature map 的线性 HSTU 近似，以支持工业长序列。 Fidelity: 核心机制复现。当前实现让 contextual lenses、软序列构造和 HSTU-style gated attention 一起反向传播；未复刻 Meta 私有特征、规模和分布式 serving。本地对照口径：基线与实验组共享 embedding、HSTU block、优化器和训练预算；实验组仅增加 6 个 learned contextual lenses 和多 strand 聚合，NDCG@10 +29.42%，不是相对 DIN。   搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-cmsl-b229ccb6">CMSL: Constructive Multi-Sequence Learning for Recommendation Systems</h2>
<p class="ar-learning-card__meta">Meta · 论文公开：2026-06-26</p>
<p><strong>方法要点：</strong>把点击、观看、互动等所有行为塞进单一长序列会混合多个意图，且 self-attention 成本随长度快速增长。CMSL 不依赖预定义业务 taxonomy，而是利用当前上下文特征学习多个 contextual lens，把原始历史动态构造成 K 条 latent semantic sequence；每条 strand 独立编码，再用当前非序列上下文作为 query 做 PMA 聚合。论文还给出 degree-2 polynomial feature map 的线性 HSTU 近似，以支持工业长序列。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。当前实现让 contextual lenses、软序列构造和 HSTU-style gated attention 一起反向传播；未复刻 Meta 私有特征、规模和分布式 serving。本地对照口径：基线与实验组共享 embedding、HSTU block、优化器和训练预算；实验组仅增加 6 个 learned contextual lenses 和多 strand 聚合，NDCG@10 +29.42%，不是相对 DIN。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.28533">原论文</a> · <a href="../../../../reproductions/2606.28533-cmsl/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="UniFormer: Efficient and Unified Model-Centric Scaling for Industrial Recommendation 搜广推与 LLM 应用 Kuaishou 2026-06-25 把 item-independent/dependent 特征与不同任务拆成语义 token，通过统一交互模块共同扩展序列、特征和任务空间。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 UniFormer 为 0.04131，相对变化 -23.50%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  ranking feature-tokenization multi-task 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-uniformer-655acc49">UniFormer: Efficient and Unified Model-Centric Scaling for Industrial Recommendation</h2>
<p class="ar-learning-card__meta">Kuaishou · 论文公开：2026-06-25</p>
<p><strong>方法要点：</strong>把 item-independent/dependent 特征与不同任务拆成语义 token，通过统一交互模块共同扩展序列、特征和任务空间。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 UniFormer 为 0.04131，相对变化 -23.50%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.27058">原论文</a> · <a href="../../../../reproductions/2606.27058-uniformer/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="JourneyFormer: Encoding Airbnb Guest Journey with Sequence Modeling 搜广推与 LLM 应用 Airbnb 2026-06-17 统一编码 Airbnb 长期和短期 guest journey，以事件类型、时间和 listing 表示构建序列，并通过缓存和稀疏计算满足线上时延。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  search-ranking sequence-modeling long-sequence 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-journeyformer-09e3e4a3">JourneyFormer: Encoding Airbnb Guest Journey with Sequence Modeling</h2>
<p class="ar-learning-card__meta">Airbnb · 论文公开：2026-06-17</p>
<p><strong>方法要点：</strong>统一编码 Airbnb 长期和短期 guest journey，以事件类型、时间和 listing 表示构建序列，并通过缓存和稀疏计算满足线上时延。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.19108">原论文</a> · <a href="../../../../reproductions/2606.19108-journeyformer/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OneRank: Unified Transformer-Native Ranking Architecture for Multi-Task Recommendation 搜广推与 LLM 应用 Renmin University of China 2026-06-15 取消 encoder 与 task predictor 的割裂，把结构化特征和任务 token 放进统一序列，并用 task-private channel 与梯度隔离控制任务冲突。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 OneRank 为 0.09540，相对变化 +76.65%。这是公开代理任务上的机制结果，生产线上 lift 的外推不适用。  ranking multi-task transformer 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-onerank-a08d1448">OneRank: Unified Transformer-Native Ranking Architecture for Multi-Task Recommendation</h2>
<p class="ar-learning-card__meta">Renmin University of China · 论文公开：2026-06-15</p>
<p><strong>方法要点：</strong>取消 encoder 与 task predictor 的割裂，把结构化特征和任务 token 放进统一序列，并用 task-private channel 与梯度隔离控制任务冲突。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 OneRank 为 0.09540，相对变化 +76.65%。这是公开代理任务上的机制结果，生产线上 lift 的外推不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.16838">原论文</a> · <a href="../../../../reproductions/2606.16838-onerank/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Memento: Personalized RAG-Style Long-Retention Data Scaling for Online Ads Recommendation 搜广推与 LLM 应用 Meta 2026-05-22 工业推荐模型通常只保留有限长度历史，长期但相关的行为被截断；训练数据也会因一次 SGD 后被“忘记”。Memento 将 RAG 思想分成两条路径：Representation Memento 从最长 365 天用户历史 embedding 库检索与当前 query 相关且互不冗余的事件，再用 Ember 条件变换融入主模型；Data Memento 从历史训练样本库检索被当前模型遗忘、但与当前 batch 有关的样本做第二次 replay。 未复现 Ember、INT8 检索服务与 Data Memento replay。Fidelity: 核心机制复现。query-conditioned MMR 长历史检索实际执行；Meta 私有 Ember、replay 与 INT8 serving 未复刻。本地对照口径：基线是 LastN 历史截断；实验组是 query-conditioned Memento MMR；NDCG@10 从 0.0443 升至 0.0464（+4.78%）。这是历史检索策略消融，不是相对 DIN。   搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-memento-1c9d9291">Memento: Personalized RAG-Style Long-Retention Data Scaling for Online Ads Recommendation</h2>
<p class="ar-learning-card__meta">Meta · 论文公开：2026-05-22</p>
<p><strong>方法要点：</strong>工业推荐模型通常只保留有限长度历史，长期但相关的行为被截断；训练数据也会因一次 SGD 后被“忘记”。Memento 将 RAG 思想分成两条路径：Representation Memento 从最长 365 天用户历史 embedding 库检索与当前 query 相关且互不冗余的事件，再用 Ember 条件变换融入主模型；Data Memento 从历史训练样本库检索被当前模型遗忘、但与当前 batch 有关的样本做第二次 replay。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>未复现 Ember、INT8 检索服务与 Data Memento replay。Fidelity: 核心机制复现。query-conditioned MMR 长历史检索实际执行；Meta 私有 Ember、replay 与 INT8 serving 未复刻。本地对照口径：基线是 LastN 历史截断；实验组是 query-conditioned Memento MMR；NDCG@10 从 0.0443 升至 0.0464（+4.78%）。这是历史检索策略消融，不是相对 DIN。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.24051">原论文</a> · <a href="../../../../reproductions/2605.24051-memento/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TubiFM: Unified Item, Carousel, and Search Ranking for Streaming Discovery 搜广推与 LLM 应用 Tubi 2026-05-22 以统一 user story 序列描述跨页面旅程，同一个生成式 foundation model 通过任务提示完成 item、carousel 与 search 三种排序。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  foundation-model multi-task-learning search-ranking 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-tubifm-2a9a268d">TubiFM: Unified Item, Carousel, and Search Ranking for Streaming Discovery</h2>
<p class="ar-learning-card__meta">Tubi · 论文公开：2026-05-22</p>
<p><strong>方法要点：</strong>以统一 user story 序列描述跨页面旅程，同一个生成式 foundation model 通过任务提示完成 item、carousel 与 search 三种排序。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.23702">原论文</a> · <a href="../../../../reproductions/2605.23702-tubifm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="UxSID: Semantic-Aware User Interests Modeling for Ultra-Long Sequence 搜广推与 LLM 应用 Kuaishou 2026-05-09 UxSID 在逐候选检索和完全候选无关的历史压缩之间加入“目标语义组共享记忆”：用目标物品第一层 SID 查询全历史与可学习兴趣锚点，利用全局兴趣门控第二层语义探针。语义相近的候选共享用户兴趣表示，使离线端到端训练与线上按用户/SID 查表使用同一记忆。IAIC 先用可学习锚点对行为序列做交叉注意力，再为每个锚点配置独立 Sigmoid PFFN、残差及 LayerNorm；正交项抑制兴趣坍缩。目标 SID 对原序列取全局响应，并以该响应门控 SID 后查询压缩锚点，最后拼接两级兴趣表示进行监督训练。 一次早期 CPU/seed42/100 用户/1 epoch 诊断中，UxSID test AUC 0.5848，validation 选择的 agnostic 为 0.5916；默认 encoder 是固定版本 Qwen2.5-0.5B-Instruct 7ae557604adf67be50417f59c2c2f167def9a775；仅输入公开电影标题和 genre。所有 encoder 参数冻结，mask mean pooling 后归一化，不读取评分/验证/测试标签。公开文本语义不是私有视频/世界知识对齐 MLLM。  long-sequence ranking semantic-id compression 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-uxsid-c8fb3e15">UxSID: Semantic-Aware User Interests Modeling for Ultra-Long Sequence</h2>
<p class="ar-learning-card__meta">Kuaishou · 论文公开：2026-05-09</p>
<p><strong>方法要点：</strong>UxSID 在逐候选检索和完全候选无关的历史压缩之间加入“目标语义组共享记忆”：用目标物品第一层 SID 查询全历史与可学习兴趣锚点，利用全局兴趣门控第二层语义探针。语义相近的候选共享用户兴趣表示，使离线端到端训练与线上按用户/SID 查表使用同一记忆。IAIC 先用可学习锚点对行为序列做交叉注意力，再为每个锚点配置独立 Sigmoid PFFN、残差及 LayerNorm；正交项抑制兴趣坍缩。目标 SID 对原序列取全局响应，并以该响应门控 SID 后查询压缩锚点，最后拼接两级兴趣表示进行监督训练。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>一次早期 CPU/seed42/100 用户/1 epoch 诊断中，UxSID test AUC 0.5848，validation 选择的 agnostic 为 0.5916；默认 encoder 是固定版本 Qwen2.5-0.5B-Instruct 7ae557604adf67be50417f59c2c2f167def9a775；仅输入公开电影标题和 genre。所有 encoder 参数冻结，mask mean pooling 后归一化，不读取评分/验证/测试标签。公开文本语义不是私有视频/世界知识对齐 MLLM。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.09040">原论文</a> · <a href="../../../../reproductions/2605.09040-uxsid/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Beyond Item IDs: Scaling Short-Form-Video Recommendation via Semantic-Native Long Sequence Modeling 搜广推与 LLM 应用 Google 2026-05-04 原子 Video ID 只能记忆内容，embedding table 随 corpus 无界增长，新视频也没有可迁移语义；完整 attention 又让千级历史成本呈平方增长。论文先用 RQ-VAE 产生 coarse-to-fine SID，并截断为 bounded bigram vocabulary；再把相邻个事件无参数折叠为 super-token，同时加入统一 global query，使模型在保留全局兴趣的情况下处理更长历史。 本地未训练 Google RQ-VAE，没有 billion-user 私有流量、2,000-event 服务序列、异步长历史模块或定制 HBM kernel。Fidelity: 核心机制复现。本地实际构建 residual-quantized Semantic ID，执行 depth-truncated bigram、parameter-free temporal folding、global query attention 和 global-local pooling。MovieLens feature 只代理多模态视频表征；  long-sequence semantic-id rq-vae efficient-transformer cold-start 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-semantic-native-longseq-dee361e1">Beyond Item IDs: Scaling Short-Form-Video Recommendation via Semantic-Native Long Sequence Modeling</h2>
<p class="ar-learning-card__meta">Google · 论文公开：2026-05-04</p>
<p><strong>方法要点：</strong>原子 Video ID 只能记忆内容，embedding table 随 corpus 无界增长，新视频也没有可迁移语义；完整 attention 又让千级历史成本呈平方增长。论文先用 RQ-VAE 产生 coarse-to-fine SID，并截断为 bounded bigram vocabulary；再把相邻个事件无参数折叠为 super-token，同时加入统一 global query，使模型在保留全局兴趣的情况下处理更长历史。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本地未训练 Google RQ-VAE，没有 billion-user 私有流量、2,000-event 服务序列、异步长历史模块或定制 HBM kernel。Fidelity: 核心机制复现。本地实际构建 residual-quantized Semantic ID，执行 depth-truncated bigram、parameter-free temporal folding、global query attention 和 global-local pooling。MovieLens feature 只代理多模态视频表征；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.07546">原论文</a> · <a href="../../../../reproductions/2606.07546-semantic-native-longseq/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="RankUp: Towards High-rank Representations for Large Scale Advertising Recommender Systems 搜广推与 LLM 应用 Tencent 2026-04-20 RankUp 针对深层推荐网络的表征坍缩，组合随机置换分组、多套 embedding、全局 token、交叉预训练 embedding 注入和任务 token 解耦，让随模型规模增长的参数真正转化为更高秩的表达空间。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04702，相对变化 -12.94%。本地代理目标与论文生产任务不同，不能外推线上 lift。  advertising representation-collapse feature-interaction 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-rankup-a9399758">RankUp: Towards High-rank Representations for Large Scale Advertising Recommender Systems</h2>
<p class="ar-learning-card__meta">Tencent · 论文公开：2026-04-20</p>
<p><strong>方法要点：</strong>RankUp 针对深层推荐网络的表征坍缩，组合随机置换分组、多套 embedding、全局 token、交叉预训练 embedding 注入和任务 token 解耦，让随模型规模增长的参数真正转化为更高秩的表达空间。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04702，相对变化 -12.94%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.17878">原论文</a> · <a href="../../../../reproductions/2604.17878-rankup/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="UniScale: Synergistic Entire Space Data and Model Scaling for Search Ranking 搜广推与 LLM 应用 Taobao &amp; Tmall Group / Alibaba 2026-03-25 ES³ 从曝光外全空间扩充数据，HHSFT 分层融合异构样本；数据规模和模型容量协同扩展，并配合低成本部署。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 uniscale 核心机制，相对 NDCG@10 -2.20%。  search-ranking model-scaling entire-space-learning 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-uniscale-5256c0f4">UniScale: Synergistic Entire Space Data and Model Scaling for Search Ranking</h2>
<p class="ar-learning-card__meta">Taobao &amp; Tmall Group / Alibaba · 论文公开：2026-03-25</p>
<p><strong>方法要点：</strong>ES³ 从曝光外全空间扩充数据，HHSFT 分层融合异构样本；数据规模和模型容量协同扩展，并配合低成本部署。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 uniscale 核心机制，相对 NDCG@10 -2.20%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.24226">原论文</a> · <a href="../../../../reproductions/2603.24226-uniscale/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="SORT: A Systematically Optimized Ranking Transformer for Industrial-scale Recommenders 搜广推与 LLM 应用 Alibaba International Digital Commerce 2026-03-04 系统重做特征 token 化、注意力和 FFN，并以面向工业硬件的结构压缩长序列，使单一 Transformer 替代传统 DLRM。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 sort-ranking 核心机制，相对 NDCG@10 -13.11%。  ranking transformer serving-efficiency 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-sort-ranking-bed02966">SORT: A Systematically Optimized Ranking Transformer for Industrial-scale Recommenders</h2>
<p class="ar-learning-card__meta">Alibaba International Digital Commerce · 论文公开：2026-03-04</p>
<p><strong>方法要点：</strong>系统重做特征 token 化、注意力和 FFN，并以面向工业硬件的结构压缩长序列，使单一 Transformer 替代传统 DLRM。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 sort-ranking 核心机制，相对 NDCG@10 -13.11%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.03988">原论文</a> · <a href="../../../../reproductions/2603.03988-sort-ranking/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Beyond the Flat Sequence: Hierarchical and Preference-Aware Generative Recommendations 搜广推与 LLM 应用 Harbin Institute of Technology 2026-03-01 HPGR 先通过基于 session 的掩码物品建模学习层级行为结构，再在微调阶段使用偏好引导稀疏注意力，只保留与当前意图最相关的历史事件，减少平铺长序列里的噪声和计算。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05467，相对变化 +1.23%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation hierarchical-sequence sparse-attention 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-hpgr-f17a7799">Beyond the Flat Sequence: Hierarchical and Preference-Aware Generative Recommendations</h2>
<p class="ar-learning-card__meta">Harbin Institute of Technology · 论文公开：2026-03-01</p>
<p><strong>方法要点：</strong>HPGR 先通过基于 session 的掩码物品建模学习层级行为结构，再在微调阶段使用偏好引导稀疏注意力，只保留与当前意图最相关的历史事件，减少平铺长序列里的噪声和计算。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05467，相对变化 +1.23%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.00980">原论文</a> · <a href="../../../../reproductions/2603.00980-hpgr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="HiSAC: Hierarchical Sparse Activation Compression for Ultra-long Sequence Modeling in Recommenders 搜广推与 LLM 应用 Alibaba / Taobao 2026-02-24 超长行为全量 attention 成本高，固定压缩又损失长尾兴趣。HiSAC 用多模态 RQ-VAE 形成层级 code，逐层投票生成用户特定 interest agents，再让当前 query 只 soft-route 到少量相关 agent。 Fidelity: 核心机制复现。执行 residual codes、层级投票、兴趣 agent 与 soft routing。本地最多 64 行为，未复刻淘宝多模态 embedding、超长日志、稀疏 kernel 和线上服务。本地对照口径：基线是 recent-window dense proxy；实验组使用三层 codes、hierarchical voting 和 soft routing，NDCG@10 0.03540→0.03586，相对 +1.31%，Hit@10 相对 -4.35%。  long-sequence sparse-activation semantic-id 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-hisac-bc7a3c37">HiSAC: Hierarchical Sparse Activation Compression for Ultra-long Sequence Modeling in Recommenders</h2>
<p class="ar-learning-card__meta">Alibaba / Taobao · 论文公开：2026-02-24</p>
<p><strong>方法要点：</strong>超长行为全量 attention 成本高，固定压缩又损失长尾兴趣。HiSAC 用多模态 RQ-VAE 形成层级 code，逐层投票生成用户特定 interest agents，再让当前 query 只 soft-route 到少量相关 agent。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。执行 residual codes、层级投票、兴趣 agent 与 soft routing。本地最多 64 行为，未复刻淘宝多模态 embedding、超长日志、稀疏 kernel 和线上服务。本地对照口径：基线是 recent-window dense proxy；实验组使用三层 codes、hierarchical voting 和 soft routing，NDCG@10 0.03540→0.03586，相对 +1.31%，Hit@10 相对 -4.35%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.21009">原论文</a> · <a href="../../../../reproductions/2602.21009-hisac/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Bending the Scaling Law Curve in Large-Scale Recommendation Systems 搜广推与 LLM 应用 Meta 2026-02-19 原始 HSTU 扩展到 16k 行为和更深网络时，attention 与内存成本成为瓶颈。ULTRA-HSTU 用 semi-local attention 保留局部 token 和少量 landmark，LBSL 令越深层看到越宽范围，再以 Mixture of Transducers、attention truncation、混合精度和动态拓扑共同提升训练与推理斜率。 Fidelity: 核心机制复现。本地执行 semi-local attention、LBSL 逐层扩窗与 Mixture of Transducers。48-event 序列替代 16k 历史；不复刻 18 层生产模型、动态 topology、FP8 kernel 或 Meta 私有日志。本地对照口径：基线为 short-history transition-content ranker，实验组执行 ULTRA-HSTU compact core；NDCG@10 相对 -0.95%。  ranking long-sequence scaling-law attention serving 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-ultra-hstu-194b1e9b">Bending the Scaling Law Curve in Large-Scale Recommendation Systems</h2>
<p class="ar-learning-card__meta">Meta · 论文公开：2026-02-19</p>
<p><strong>方法要点：</strong>原始 HSTU 扩展到 16k 行为和更深网络时，attention 与内存成本成为瓶颈。ULTRA-HSTU 用 semi-local attention 保留局部 token 和少量 landmark，LBSL 令越深层看到越宽范围，再以 Mixture of Transducers、attention truncation、混合精度和动态拓扑共同提升训练与推理斜率。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地执行 semi-local attention、LBSL 逐层扩窗与 Mixture of Transducers。48-event 序列替代 16k 历史；不复刻 18 层生产模型、动态 topology、FP8 kernel 或 Meta 私有日志。本地对照口径：基线为 short-history transition-content ranker，实验组执行 ULTRA-HSTU compact core；NDCG@10 相对 -0.95%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.16986">原论文</a> · <a href="../../../../reproductions/2602.16986-ultra-hstu/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="MixFormer: Co-Scaling Up Dense and Sequence in Industrial Recommenders 搜广推与 LLM 应用 ByteDance / Douyin 2026-02-15 现有推荐模型通常把 dense feature interaction 与 behavior-sequence Transformer 做成两个独立模块，模型预算必须在两边手工分配，且交互只发生在末端。MixFormer 将非序列字段和行为序列统一成同一 Transformer token space，共享参数、逐层发生高阶交互，从而联合扩大 dense capacity 与 sequence length。 Fidelity: 完整核心链路复现。当前代码在 matched local budget 下实际训练 stacked baseline 与 unified MixFormer blocks；proposed 将 dense feature-split tokens 和行为 tokens 放进共享 backbone，并复用 user encoding 对所有候选打分。本地对照口径：基线是参数量匹配的 Stacked Dense+Sequence；实验组是 Unified MixFormer；NDCG@10 从 0.0054 升至 0.0063（+17.41%）。   搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-mixformer-c586b532">MixFormer: Co-Scaling Up Dense and Sequence in Industrial Recommenders</h2>
<p class="ar-learning-card__meta">ByteDance / Douyin · 论文公开：2026-02-15</p>
<p><strong>方法要点：</strong>现有推荐模型通常把 dense feature interaction 与 behavior-sequence Transformer 做成两个独立模块，模型预算必须在两边手工分配，且交互只发生在末端。MixFormer 将非序列字段和行为序列统一成同一 Transformer token space，共享参数、逐层发生高阶交互，从而联合扩大 dense capacity 与 sequence length。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 完整核心链路复现。当前代码在 matched local budget 下实际训练 stacked baseline 与 unified MixFormer blocks；proposed 将 dense feature-split tokens 和行为 tokens 放进共享 backbone，并复用 user encoding 对所有候选打分。本地对照口径：基线是参数量匹配的 Stacked Dense+Sequence；实验组是 Unified MixFormer；NDCG@10 从 0.0054 升至 0.0063（+17.41%）。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.14110">原论文</a> · <a href="../../../../reproductions/2602.14110-mixformer/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="An Industrial-Scale Sequential Recommender for LinkedIn Feed Ranking 搜广推与 LLM 应用 LinkedIn 2026-02-12 将 Feed 候选、交互历史和上下文统一成超长序列，采用 HSTU 式目标注意力、负样本自由评估及增量服务优化。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 linkedin-feed-sr 核心机制，相对 NDCG@10 -0.12%。  ranking sequential-recommendation long-sequence 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-linkedin-feed-sr-d07e7f6a">An Industrial-Scale Sequential Recommender for LinkedIn Feed Ranking</h2>
<p class="ar-learning-card__meta">LinkedIn · 论文公开：2026-02-12</p>
<p><strong>方法要点：</strong>将 Feed 候选、交互历史和上下文统一成超长序列，采用 HSTU 式目标注意力、负样本自由评估及增量服务优化。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 linkedin-feed-sr 核心机制，相对 NDCG@10 -0.12%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12354">原论文</a> · <a href="../../../../reproductions/2602.12354-linkedin-feed-sr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Compress, Cross and Scale: Multi-Level Compression Cross Networks for Efficient Scaling in Recommender Systems 搜广推与 LLM 应用 Bilibili 2026-02-12 在每一层先压缩高维特征，再在紧凑空间执行动态显式交叉并回注主干；MC-MLCC 使用多个并行子空间横向扩展表达力，使参数和 FLOPs 增长更可控。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05530，相对变化 +2.40%。本地代理目标与论文生产任务不同，不能外推线上 lift。  feature-interaction compression scaling-law 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-mlcc-9b40fb24">Compress, Cross and Scale: Multi-Level Compression Cross Networks for Efficient Scaling in Recommender Systems</h2>
<p class="ar-learning-card__meta">Bilibili · 论文公开：2026-02-12</p>
<p><strong>方法要点：</strong>在每一层先压缩高维特征，再在紧凑空间执行动态显式交叉并回注主干；MC-MLCC 使用多个并行子空间横向扩展表达力，使参数和 FLOPs 增长更可控。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05530，相对变化 +2.40%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12041">原论文</a> · <a href="../../../../reproductions/2602.12041-mlcc/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="CADET: Context-Conditioned Ads CTR Prediction With a Decoder-Only Transformer 搜广推与 LLM 应用 LinkedIn 2026-02-11 Decoder-only Transformer 先编码可缓存历史，候选打分后再注入 post-scoring context，避免训练与服务错位并统一广告 CTR 模型。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 cadet 核心机制，相对 NDCG@10 -6.20%。  advertising ctr-prediction decoder-only-transformer 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-cadet-4647b60d">CADET: Context-Conditioned Ads CTR Prediction With a Decoder-Only Transformer</h2>
<p class="ar-learning-card__meta">LinkedIn · 论文公开：2026-02-11</p>
<p><strong>方法要点：</strong>Decoder-only Transformer 先编码可缓存历史，候选打分后再注入 post-scoring context，避免训练与服务错位并统一广告 CTR 模型。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 cadet 核心机制，相对 NDCG@10 -6.20%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.11410">原论文</a> · <a href="../../../../reproductions/2602.11410-cadet/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Kunlun: Establishing Scaling Laws for Massive-Scale Recommendation Systems through Unified Architecture Design 搜广推与 LLM 应用 Meta 2026-02-10 传统广告模型把序列塔、稠密交叉和系统并行分别优化，扩大规模后收益快速饱和。Kunlun 在每层同时放置 Transformer Block 与 Interaction Block：GDPA/PFFN 建模序列，HSP 汇总序列 seed，Global Interaction 交换序列与非序列信息；CompSkip 和 expert parallel 保持深层训练稳定与吞吐。 Fidelity: 核心机制复现。本地执行 GDPA、分层 seed pooling、expert routing 和 CompSkip；不声称复刻 Meta Ads 模型规模。本地仅验证网络算子和信息流；没有 Meta Ads 私有数据、万亿参数、expert parallel 或硬件 MFU 对照。本地对照口径：基线为 shallow transition-content ranker，实验组执行 Kunlun compact core；NDCG@10 相对 -5.25%。  ranking scaling-law long-sequence mixture-of-experts serving 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-kunlun-7994f8f7">Kunlun: Establishing Scaling Laws for Massive-Scale Recommendation Systems through Unified Architecture Design</h2>
<p class="ar-learning-card__meta">Meta · 论文公开：2026-02-10</p>
<p><strong>方法要点：</strong>传统广告模型把序列塔、稠密交叉和系统并行分别优化，扩大规模后收益快速饱和。Kunlun 在每层同时放置 Transformer Block 与 Interaction Block：GDPA/PFFN 建模序列，HSP 汇总序列 seed，Global Interaction 交换序列与非序列信息；CompSkip 和 expert parallel 保持深层训练稳定与吞吐。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地执行 GDPA、分层 seed pooling、expert routing 和 CompSkip；不声称复刻 Meta Ads 模型规模。本地仅验证网络算子和信息流；没有 Meta Ads 私有数据、万亿参数、expert parallel 或硬件 MFU 对照。本地对照口径：基线为 shallow transition-content ranker，实验组执行 Kunlun compact core；NDCG@10 相对 -5.25%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.10016">原论文</a> · <a href="../../../../reproductions/2602.10016-kunlun/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="ML-DCN: Masked Low-Rank Deep Crossing Network Towards Scalable Ads Click-through Rate Prediction at Pinterest 搜广推与 LLM 应用 Pinterest 2026-02-09 把 DCNv2 的全维交叉替换为可调内部维度的低秩交叉，并以可学习 mask 选择交叉通道，在相同 FLOPs 下扩大容量。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 ml-dcn 核心机制，相对 NDCG@10 -2.08%。  advertising feature-crossing serving-efficiency 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-ml-dcn-5baa5b42">ML-DCN: Masked Low-Rank Deep Crossing Network Towards Scalable Ads Click-through Rate Prediction at Pinterest</h2>
<p class="ar-learning-card__meta">Pinterest · 论文公开：2026-02-09</p>
<p><strong>方法要点：</strong>把 DCNv2 的全维交叉替换为可调内部维度的低秩交叉，并以可学习 mask 选择交叉通道，在相同 FLOPs 下扩大容量。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 ml-dcn 核心机制，相对 NDCG@10 -2.08%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.09194">原论文</a> · <a href="../../../../reproductions/2602.09194-ml-dcn/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="MDL: A Unified Multi-Distribution Learner in Large-scale Industrial Recommendation through Tokenization 搜广推与 LLM 应用 ByteDance / Douyin 2026-02-07 工业多场景、多任务模型常只在浅层做 gate，未充分共享大模型参数。MDL 把 feature、scenario 和 task 都表示成 token，经 feature self-attention、domain-feature attention 和 domain-fused aggregation 深层交互。 Fidelity: 核心机制复现。执行 feature/scenario/task tokens 与 domain-feature attention。MovieLens genre/next-item 代理抖音场景与任务，未复刻生产参数规模、私有标签和 serving。本地对照口径：基线是共享但非 tokenized ranker；实验组加入 19 feature tokens、19 scenario tokens 和 2 task tokens，NDCG@10 0.03540→0.04012，相对 +13.34%，但 head share +73.43%。  ranking multi-scenario multi-task tokenization 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-mdl-daad794f">MDL: A Unified Multi-Distribution Learner in Large-scale Industrial Recommendation through Tokenization</h2>
<p class="ar-learning-card__meta">ByteDance / Douyin · 论文公开：2026-02-07</p>
<p><strong>方法要点：</strong>工业多场景、多任务模型常只在浅层做 gate，未充分共享大模型参数。MDL 把 feature、scenario 和 task 都表示成 token，经 feature self-attention、domain-feature attention 和 domain-fused aggregation 深层交互。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。执行 feature/scenario/task tokens 与 domain-feature attention。MovieLens genre/next-item 代理抖音场景与任务，未复刻生产参数规模、私有标签和 serving。本地对照口径：基线是共享但非 tokenized ranker；实验组加入 19 feature tokens、19 scenario tokens 和 2 task tokens，NDCG@10 0.03540→0.04012，相对 +13.34%，但 head share +73.43%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.07520">原论文</a> · <a href="../../../../reproductions/2602.07520-mdl/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="MSN: A Memory-based Sparse Activation Scaling Framework for Large-scale Industrial Recommendation 搜广推与 LLM 应用 ByteDance / Douyin Search 2026-02-07 工业排序希望扩大参数量但不同比例增加计算。MSN 将大容量知识放入两轴 Product-Key Memory，根据 query 只激活少量槽位，再用 gate 与 dense backbone 融合。 复现保真度：核心机制复现。复现保真度：核心机制复现。Product-Key Memory、top-k 稀疏读取和门控主干均实际执行。公开 genre 构造两轴 key，交互转移写入 memory value，每次只读取四个槽位。  search-ranking sparse-memory product-key-memory 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-msn-56fd8b3f">MSN: A Memory-based Sparse Activation Scaling Framework for Large-scale Industrial Recommendation</h2>
<p class="ar-learning-card__meta">ByteDance / Douyin Search · 论文公开：2026-02-07</p>
<p><strong>方法要点：</strong>工业排序希望扩大参数量但不同比例增加计算。MSN 将大容量知识放入两轴 Product-Key Memory，根据 query 只激活少量槽位，再用 gate 与 dense backbone 融合。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现保真度：核心机制复现。复现保真度：核心机制复现。Product-Key Memory、top-k 稀疏读取和门控主干均实际执行。公开 genre 构造两轴 key，交互转移写入 memory value，每次只读取四个槽位。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.07526">原论文</a> · <a href="../../../../reproductions/2602.07526-msn/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TokenMixer-Large: Scaling Up Large Ranking Models in Industrial Recommenders 搜广推与 LLM 应用 ByteDance 2026-02-06 TokenMixer-Large 将候选与多域特征 token 先无参数 mixing，再分别做 head-wise SwiGLU，revert 后执行 token-wise SwiGLU；深层网络加入间隔残差和中间监督，使推荐精排能够稳定扩容。 复现保真度：完整核心链路复现。复现保真度：完整核心链路复现。主干、interval residual、中层辅助损失均真实训练，仅缩小规模。MovieLens 100K 上 TokenMixer-Large 与 rankmixer_dense 使用相同维度、层数、负采样和训练步数。  ranking token-mixing scaling 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-tokenmixer-large-095f089c">TokenMixer-Large: Scaling Up Large Ranking Models in Industrial Recommenders</h2>
<p class="ar-learning-card__meta">ByteDance · 论文公开：2026-02-06</p>
<p><strong>方法要点：</strong>TokenMixer-Large 将候选与多域特征 token 先无参数 mixing，再分别做 head-wise SwiGLU，revert 后执行 token-wise SwiGLU；深层网络加入间隔残差和中间监督，使推荐精排能够稳定扩容。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现保真度：完整核心链路复现。复现保真度：完整核心链路复现。主干、interval residual、中层辅助损失均真实训练，仅缩小规模。MovieLens 100K 上 TokenMixer-Large 与 rankmixer_dense 使用相同维度、层数、负采样和训练步数。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.06563">原论文</a> · <a href="../../../../reproductions/2602.06563-tokenmixer-large/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Zenith: Scaling up Ranking Models for Billion-scale Livestreaming Recommendation 搜广推与 LLM 应用 North Carolina State University 2026-01-29 Token Fusion 将大量异构稀疏特征压成少量高维 Prime Tokens，RSA/TMHSA 保持 token 差异；TSwiGLU/TSMoE 对每个 token 独立增强，改善模型规模与计算量的 scaling law。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04623，相对变化 -14.40%。本地代理目标与论文生产任务不同，不能外推线上 lift。  ranking-network scaling-law feature-interaction 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-zenith-6db3b2a2">Zenith: Scaling up Ranking Models for Billion-scale Livestreaming Recommendation</h2>
<p class="ar-learning-card__meta">North Carolina State University · 论文公开：2026-01-29</p>
<p><strong>方法要点：</strong>Token Fusion 将大量异构稀疏特征压成少量高维 Prime Tokens，RSA/TMHSA 保持 token 差异；TSwiGLU/TSMoE 对每个 token 独立增强，改善模型规模与计算量的 scaling law。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04623，相对变化 -14.40%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.21285">原论文</a> · <a href="../../../../reproductions/2601.21285-zenith/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="LLaTTE: Scaling Laws for Multi-Stage Sequence Modeling in Large-Scale Ads Recommendation 搜广推与 LLM 应用 Meta 2026-01-27 工业推荐序列模型同时受训练 FLOPs、在线延迟和跨阶段信息损失约束：直接把历史拉长会让在线 ranking 代价失控，只扩大下游模型又无法恢复上游丢掉的长期兴趣。LLaTTE 将 scaling 拆成两级：上游异步大序列模型读取超长、多源历史并缓存 2,048 维 user representation； Fidelity: 核心机制复现。当前实现实际运行 BERT-tiny semantic features、MLA 上游 latent、target-aware 在线 attention 与 DHEN 门控；未复刻 Meta 私有广告特征和异步生产 serving。本地对照口径：基线是相同 ID/语义 embedding 的 short online sequence；实验组增加 MLA upstream、候选感知 online attention 与 DHEN，NDCG@10 +49.81%。训练预算一致，不是相对 DIN。   搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-llatte-05036174">LLaTTE: Scaling Laws for Multi-Stage Sequence Modeling in Large-Scale Ads Recommendation</h2>
<p class="ar-learning-card__meta">Meta · 论文公开：2026-01-27</p>
<p><strong>方法要点：</strong>工业推荐序列模型同时受训练 FLOPs、在线延迟和跨阶段信息损失约束：直接把历史拉长会让在线 ranking 代价失控，只扩大下游模型又无法恢复上游丢掉的长期兴趣。LLaTTE 将 scaling 拆成两级：上游异步大序列模型读取超长、多源历史并缓存 2,048 维 user representation；</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。当前实现实际运行 BERT-tiny semantic features、MLA 上游 latent、target-aware 在线 attention 与 DHEN 门控；未复刻 Meta 私有广告特征和异步生产 serving。本地对照口径：基线是相同 ID/语义 embedding 的 short online sequence；实验组增加 MLA upstream、候选感知 online attention 与 DHEN，NDCG@10 +49.81%。训练预算一致，不是相对 DIN。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.20083">原论文</a> · <a href="../../../../reproductions/2601.20083-llatte/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Unleashing the Potential of Sparse Attention on Long-term Behaviors for CTR Prediction 搜广推与 LLM 应用 Institute of Software, Chinese Academy of Sciences 2026-01-25 TimeChunking 按个体行为时间间隔自适应分块；EvoAttention 并联全局 chunk、兴趣转移和局部窗口三路注意力，RelTemporal 再注入时间间隔、小时和周末相对偏置。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05519，相对变化 +2.19%。本地代理目标与论文生产任务不同，不能外推线上 lift。  ctr-prediction long-sequence sparse-attention 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-sparsectr-7769ddba">Unleashing the Potential of Sparse Attention on Long-term Behaviors for CTR Prediction</h2>
<p class="ar-learning-card__meta">Institute of Software, Chinese Academy of Sciences · 论文公开：2026-01-25</p>
<p><strong>方法要点：</strong>TimeChunking 按个体行为时间间隔自适应分块；EvoAttention 并联全局 chunk、兴趣转移和局部窗口三路注意力，RelTemporal 再注入时间间隔、小时和周末相对偏置。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05519，相对变化 +2.19%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.17836">原论文</a> · <a href="../../../../reproductions/2601.17836-sparsectr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="HyFormer: Revisiting the Roles of Sequence Modeling and Feature Interaction in CTR Prediction 搜广推与 LLM 应用 ByteDance / Douyin Search 2026-01-19 LONGER→RankMixer 类串行架构先压缩长序列、再做异构字段交互，信息流晚且单向。HyFormer 从非序列字段和 sequence mean 生成 Global Queries，每层用 queries cross-attend 当前 sequence K/V，再把 decoded queries 与非序列 tokens 做 RankMixer-style boosting；boosted queries 进入下一层重新解码，实现双向、逐层共同演化。 Fidelity: 完整核心链路复现。本地逐层执行 Query Generation、Query Decoding 和 Query Boosting；私有多行为序列替换为 MovieLens 单序列。本地对照口径：基线是独立 sequence Transformer+dense MLP 的 Late Fusion；实验组是 HyFormer；NDCG@10 从 0.0048 升至 0.0116（+143.77%），head share 同时 +30.90pt。这是 query co-evolution 架构消融，不是相对 DIN。   搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-hyformer-d0fa9291">HyFormer: Revisiting the Roles of Sequence Modeling and Feature Interaction in CTR Prediction</h2>
<p class="ar-learning-card__meta">ByteDance / Douyin Search · 论文公开：2026-01-19</p>
<p><strong>方法要点：</strong>LONGER→RankMixer 类串行架构先压缩长序列、再做异构字段交互，信息流晚且单向。HyFormer 从非序列字段和 sequence mean 生成 Global Queries，每层用 queries cross-attend 当前 sequence K/V，再把 decoded queries 与非序列 tokens 做 RankMixer-style boosting；boosted queries 进入下一层重新解码，实现双向、逐层共同演化。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 完整核心链路复现。本地逐层执行 Query Generation、Query Decoding 和 Query Boosting；私有多行为序列替换为 MovieLens 单序列。本地对照口径：基线是独立 sequence Transformer+dense MLP 的 Late Fusion；实验组是 HyFormer；NDCG@10 从 0.0048 升至 0.0116（+143.77%），head share 同时 +30.90pt。这是 query co-evolution 架构消融，不是相对 DIN。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.12681">原论文</a> · <a href="../../../../reproductions/2601.12681-hyformer/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OneTrans: Unified Feature Interaction and Sequence Modeling with One Transformer in Industrial Recommender 搜广推与 LLM 应用 ByteDance 2025-10-30 OneTrans 把行为 S-tokens 放在异构 NS-tokens 前，使用一个 causal Transformer 同时完成序列建模和字段交互。语义同质的 S-token 共享 QKV/FFN；每个 NS-token 拥有独立参数。因果顺序使 NS-token 能读取完整历史，pyramid stack 逐层只保留近期 S queries。线上用 cross-candidate/cross-request KV cache 复用 S-side 计算。 Fidelity: 完整核心链路复现。本地执行 unified S/NS tokenization、mixed QKV、mixed FFN、causal attention 和 pyramid tail pruning；持久化跨请求 KV 服务系统未复刻。本地对照口径：基线是独立 sequence encoder 后与 candidate 交互的 Encode-then-Interact；实验组是 OneTrans；NDCG@10 从 0.0069 升至 0.0154（+123.58%），但 head share 达 92%。这是统一架构相对 stacked 架构的消融，不是相对 DIN。   搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-onetrans-113b41b8">OneTrans: Unified Feature Interaction and Sequence Modeling with One Transformer in Industrial Recommender</h2>
<p class="ar-learning-card__meta">ByteDance · 论文公开：2025-10-30</p>
<p><strong>方法要点：</strong>OneTrans 把行为 S-tokens 放在异构 NS-tokens 前，使用一个 causal Transformer 同时完成序列建模和字段交互。语义同质的 S-token 共享 QKV/FFN；每个 NS-token 拥有独立参数。因果顺序使 NS-token 能读取完整历史，pyramid stack 逐层只保留近期 S queries。线上用 cross-candidate/cross-request KV cache 复用 S-side 计算。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 完整核心链路复现。本地执行 unified S/NS tokenization、mixed QKV、mixed FFN、causal attention 和 pyramid tail pruning；持久化跨请求 KV 服务系统未复刻。本地对照口径：基线是独立 sequence encoder 后与 candidate 交互的 Encode-then-Interact；实验组是 OneTrans；NDCG@10 从 0.0069 升至 0.0154（+123.58%），但 head share 达 92%。这是统一架构相对 stacked 架构的消融，不是相对 DIN。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.26104">原论文</a> · <a href="../../../../reproductions/2510.26104-onetrans/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OnePiece: Bringing Context Engineering and Reasoning to Industrial Cascade Ranking 搜广推与 LLM 应用 Shopee 2025-09-22 把上下文 token、块级 latent reasoning 与递进多任务目标合并到级联排序器，让召回、点击和价值任务共享表示但分阶段收敛。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 onepiece 核心机制；相对 NDCG@10 +22.87%。  ranking retrieval latent-reasoning multi-task 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-onepiece-1b14efa1">OnePiece: Bringing Context Engineering and Reasoning to Industrial Cascade Ranking</h2>
<p class="ar-learning-card__meta">Shopee · 论文公开：2025-09-22</p>
<p><strong>方法要点：</strong>把上下文 token、块级 latent reasoning 与递进多任务目标合并到级联排序器，让召回、点击和价值任务共享表示但分阶段收敛。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 onepiece 核心机制；相对 NDCG@10 +22.87%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2509.18091">原论文</a> · <a href="../../../../reproductions/2509.18091-onepiece/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Scaling Recommender Transformers to One Billion Parameters 搜广推与 LLM 应用 Yandex 2025-07-21 直接 next-item 预测把“用户会怎样反馈”和“会消费哪个 item”纠缠。ARGUS 先预测 feedback token，再以其条件化 next-item，使多种反馈共享序列主干并获得更好的 scaling。 两种口径均未验证收益。Fidelity: 核心机制复现。matched Transformer 中实际执行 feedback-first、next-item-second 分解；未复刻十亿参数规模与私有音乐反馈。本地对照口径：统一跨模型基线是 DIN，ARGUS NDCG@10 相对 DIN -4.12%；内部 next-item-only 基线加入 feedback decomposition 后 -20.95%。两种口径均未验证收益。统一为 180 users/280 items 后，DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；  long-sequence transformer multi-task 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-argus-3c7d662d">Scaling Recommender Transformers to One Billion Parameters</h2>
<p class="ar-learning-card__meta">Yandex · 论文公开：2025-07-21</p>
<p><strong>方法要点：</strong>直接 next-item 预测把“用户会怎样反馈”和“会消费哪个 item”纠缠。ARGUS 先预测 feedback token，再以其条件化 next-item，使多种反馈共享序列主干并获得更好的 scaling。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>两种口径均未验证收益。Fidelity: 核心机制复现。matched Transformer 中实际执行 feedback-first、next-item-second 分解；未复刻十亿参数规模与私有音乐反馈。本地对照口径：统一跨模型基线是 DIN，ARGUS NDCG@10 相对 DIN -4.12%；内部 next-item-only 基线加入 feedback decomposition 后 -20.95%。两种口径均未验证收益。统一为 180 users/280 items 后，DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.15994">原论文</a> · <a href="../../../../reproductions/2507.15994-argus/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="RankMixer: Scaling Up Ranking Models in Industrial Recommenders 搜广推与 LLM 应用 ByteDance / Douyin 2025-07-21 RankMixer 用固定的多头 TokenMix 让不同 feature token 的分量相遇，再由各 token 独立的 FFN 学习组合。这里替换的是异构特征交互模块；上游长序列模块仍可使用 attention。 本地只有 seed 42 的 smoke。Shared FFN 与 Dense per-token 都含 TokenMix，且参数量不同，不能据此验证 TokenMix 优于 attention。Sparse 没有追平 Dense，当前路由与原文双 router DTSI 仍有差异。 TokenMix 没有可训练参数，整个模型为什么仍能学习特征关系？  搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-rankmixer-298d1226">RankMixer: Scaling Up Ranking Models in Industrial Recommenders</h2>
<p class="ar-learning-card__meta">ByteDance / Douyin · 论文公开：2025-07-21</p>
<p><strong>方法要点：</strong>RankMixer 用固定的多头 TokenMix 让不同 feature token 的分量相遇，再由各 token 独立的 FFN 学习组合。这里替换的是异构特征交互模块；上游长序列模块仍可使用 attention。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本地只有 seed 42 的 smoke。Shared FFN 与 Dense per-token 都含 TokenMix，且参数量不同，不能据此验证 TokenMix 优于 attention。Sparse 没有追平 Dense，当前路由与原文双 router DTSI 仍有差异。</p></details>
<p class="ar-learning-question"><strong>想一想：</strong>TokenMix 没有可训练参数，整个模型为什么仍能学习特征关系？</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.15551">原论文</a> · <a href="../../../../reproductions/2507.15551-rankmixer/">实现解读</a> · <a href="../../../002-rankmixer-tokenmix/">阅读精选对比</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="PinFM: Foundation Model for User Activity Sequences at a Billion-scale Visual Discovery Platform 搜广推与 LLM 应用 Pinterest 2025-07-17 PinFM 把“先在跨场景用户行为上预训练，再接入各排序模型微调”的 Foundation Model 范式带到工业推荐。decoder-only backbone 学习 next/multi/future token；下游把候选追加到用户序列做 early fusion。DCAT 利用同一请求的候选共享用户历史，把 context self-attention 只算一次，然后让候选对缓存的 context KV 做 cross-attention。 保真度：核心机制复现。保真度：核心机制复现。NTL/MTL/FTL 对比预训练、预训练后下游微调、candidate early fusion、Candidate ID Randomization、backbone 低学习率和 DCAT 均实际执行；省略 Pinterest 多 action/surface 语料、fresh-item age dropout、分布式 20B embedding、int4 与 Triton kernel。本地对照口径：基线是 scratch DCAT；实验组是预训练后微调的 PinFM；   搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-pinfm-c653f7d8">PinFM: Foundation Model for User Activity Sequences at a Billion-scale Visual Discovery Platform</h2>
<p class="ar-learning-card__meta">Pinterest · 论文公开：2025-07-17</p>
<p><strong>方法要点：</strong>PinFM 把“先在跨场景用户行为上预训练，再接入各排序模型微调”的 Foundation Model 范式带到工业推荐。decoder-only backbone 学习 next/multi/future token；下游把候选追加到用户序列做 early fusion。DCAT 利用同一请求的候选共享用户历史，把 context self-attention 只算一次，然后让候选对缓存的 context KV 做 cross-attention。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。NTL/MTL/FTL 对比预训练、预训练后下游微调、candidate early fusion、Candidate ID Randomization、backbone 低学习率和 DCAT 均实际执行；省略 Pinterest 多 action/surface 语料、fresh-item age dropout、分布式 20B embedding、int4 与 Triton kernel。本地对照口径：基线是 scratch DCAT；实验组是预训练后微调的 PinFM；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.12704">原论文</a> · <a href="../../../../reproductions/2507.12704-pinfm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TransAct V2: Lifelong User Action Sequence Modeling on Pinterest Recommendation 搜广推与 LLM 应用 Pinterest 2025-06-02 TransAct 主要建模约百条实时行为，容易忽略用户多年的长期兴趣。TransAct V2 从约条 lifelong 序列中按候选相似度取回相关行为，同时保留最近行为，再通过共享 Transformer 做 CTR 排序；额外的 Next Action Loss 迫使序列表征预测下一次正向互动。论文也包含 SKUT、request deduplication 等 serving 优化，本地复现聚焦模型链路。 保真度：核心机制复现。保真度：核心机制复现。候选锚定的长/短序列近邻检索、最近行为保留、early-fusion causal Transformer 和 Next Action Loss 均实际训练；MovieLens genre 替代 PinSage embedding，省略 Pinterest action/surface 字段、曝光日志负例及生产 Triton kernel。本地对照口径：基线是参数量匹配的 TransAct；实验组是 TransAct V2；NDCG@10 从 0.01277 升至 0.02460（+92.65%），head share 同时 +14.70pt。   搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-transact-v2-c124d4cb">TransAct V2: Lifelong User Action Sequence Modeling on Pinterest Recommendation</h2>
<p class="ar-learning-card__meta">Pinterest · 论文公开：2025-06-02</p>
<p><strong>方法要点：</strong>TransAct 主要建模约百条实时行为，容易忽略用户多年的长期兴趣。TransAct V2 从约条 lifelong 序列中按候选相似度取回相关行为，同时保留最近行为，再通过共享 Transformer 做 CTR 排序；额外的 Next Action Loss 迫使序列表征预测下一次正向互动。论文也包含 SKUT、request deduplication 等 serving 优化，本地复现聚焦模型链路。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。候选锚定的长/短序列近邻检索、最近行为保留、early-fusion causal Transformer 和 Next Action Loss 均实际训练；MovieLens genre 替代 PinSage embedding，省略 Pinterest action/surface 字段、曝光日志负例及生产 Triton kernel。本地对照口径：基线是参数量匹配的 TransAct；实验组是 TransAct V2；NDCG@10 从 0.01277 升至 0.02460（+92.65%），head share 同时 +14.70pt。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2506.02267">原论文</a> · <a href="../../../../reproductions/2506.02267-transact-v2/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Towards Large-scale Generative Ranking 搜广推与 LLM 应用 Xiaohongshu 2025-05-07 HSTU 式排序把 item 与 action 交错为两倍长序列。GenRank 将 action 作为同一 item token 的监督/特征，并加入 position 与 time bias，在不丢掉多行为生成目标的前提下降低排序成本。 Fidelity: 完整核心链路复现。真实执行 item/action 交错基线、action-oriented 组织、位置/时间偏置、因果 Transformer 和 action 生成；缩小为 MovieLens 显式反馈。本地对照口径：基线是 item/action 交错序列模型；实验组是 GenRank action-oriented 组织；延迟 -25.66%，但 AUC -0.46%。这是序列组织的效率—效果对照，不是准确率提升，也不是相对 DIN。  generative-ranking action-modeling efficiency 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-genrank-a86f2304">Towards Large-scale Generative Ranking</h2>
<p class="ar-learning-card__meta">Xiaohongshu · 论文公开：2025-05-07</p>
<p><strong>方法要点：</strong>HSTU 式排序把 item 与 action 交错为两倍长序列。GenRank 将 action 作为同一 item token 的监督/特征，并加入 position 与 time bias，在不丢掉多行为生成目标的前提下降低排序成本。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 完整核心链路复现。真实执行 item/action 交错基线、action-oriented 组织、位置/时间偏置、因果 Transformer 和 action 生成；缩小为 MovieLens 显式反馈。本地对照口径：基线是 item/action 交错序列模型；实验组是 GenRank action-oriented 组织；延迟 -25.66%，但 AUC -0.46%。这是序列组织的效率—效果对照，不是准确率提升，也不是相对 DIN。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.04180">原论文</a> · <a href="../../../../reproductions/2505.04180-genrank/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders 搜广推与 LLM 应用 ByteDance / Douyin 2025-05-07 LONGER 先以 Token Merge 合并相邻行为，首层用少量 Query 读取长 K/V，后续沿短序列继续 self-attention。学习重点是区分合并输入和压缩查询这两步。 当前本地 encode 拼接 global/merged/recent 后做单层 self-attention，尚缺论文的首层短 Q/长 K/V hybrid attention 路径和 causal mask。历史实验不作为该核心路径或生产缓存的验证。 首层之后，模型还能否直接重新读取完整长 K/V？  搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-longer-50bd52b2">LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders</h2>
<p class="ar-learning-card__meta">ByteDance / Douyin · 论文公开：2025-05-07</p>
<p><strong>方法要点：</strong>LONGER 先以 Token Merge 合并相邻行为，首层用少量 Query 读取长 K/V，后续沿短序列继续 self-attention。学习重点是区分合并输入和压缩查询这两步。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>当前本地 encode 拼接 global/merged/recent 后做单层 self-attention，尚缺论文的首层短 Q/长 K/V hybrid attention 路径和 causal mask。历史实验不作为该核心路径或生产缓存的验证。</p></details>
<p class="ar-learning-question"><strong>想一想：</strong>首层之后，模型还能否直接重新读取完整长 K/V？</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.04421">原论文</a> · <a href="../../../../reproductions/2505.04421-longer/">实现解读</a> · <a href="../../../001-hstu-longer-slimper/">阅读精选对比</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="FuXi-α: Scaling Recommendation Model with Feature Interaction Enhanced Transformer 搜广推与 LLM 应用 Huawei / USTC 2025-02-05 常规推荐 Transformer 扩参时容易受浅层特征交互限制。FuXi-α 用多个自适应交互通道建模不同关系，再以 multi-stage FFN 逐级融合。 Fidelity: 核心机制复现。实际执行时间、语义和流行度多通道注意力及分阶段交互门控。本地是小型数值通道实现，不包含论文十亿级 scaling、华为音乐私有连续特征与分布式训练。本地对照口径：相对单通道注意力基线，实验组 NDCG@10 -4.25%。  ranking transformer feature-interaction scaling 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-fuxi-alpha-d5540b18">FuXi-α: Scaling Recommendation Model with Feature Interaction Enhanced Transformer</h2>
<p class="ar-learning-card__meta">Huawei / USTC · 论文公开：2025-02-05</p>
<p><strong>方法要点：</strong>常规推荐 Transformer 扩参时容易受浅层特征交互限制。FuXi-α 用多个自适应交互通道建模不同关系，再以 multi-stage FFN 逐级融合。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。实际执行时间、语义和流行度多通道注意力及分阶段交互门控。本地是小型数值通道实现，不包含论文十亿级 scaling、华为音乐私有连续特征与分布式训练。本地对照口径：相对单通道注意力基线，实验组 NDCG@10 -4.25%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.03036">原论文</a> · <a href="../../../../reproductions/2502.03036-fuxi-alpha/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="AdaF²M²: Comprehensive Learning and Responsive Leveraging Features in Recommendation System 搜广推与 LLM 应用 ByteDance / Douyin 2025-01-27 单次全特征前向容易过度依赖强特征，且不同用户/物品状态需要不同特征。AdaF²M² 通过多种 mask 重复前向学习互补表示，再以 state-aware adapter 动态融合。 Fidelity: 核心机制复现。实际执行三组 feature-mask 前向、共享聚合与用户/物品状态自适应 adapter。状态仅由历史长度和物品热度构造；没有抖音私有特征、全链路联合训练和线上资源成本。本地对照口径：相对单前向全特征基线，实验组 NDCG@10 +2.42%。  ranking feature-masking state-aware-adapter multi-forward 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-adaf2m2-4b0f92a1">AdaF²M²: Comprehensive Learning and Responsive Leveraging Features in Recommendation System</h2>
<p class="ar-learning-card__meta">ByteDance / Douyin · 论文公开：2025-01-27</p>
<p><strong>方法要点：</strong>单次全特征前向容易过度依赖强特征，且不同用户/物品状态需要不同特征。AdaF²M² 通过多种 mask 重复前向学习互补表示，再以 state-aware adapter 动态融合。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。实际执行三组 feature-mask 前向、共享聚合与用户/物品状态自适应 adapter。状态仅由历史长度和物品热度构造；没有抖音私有特征、全链路联合训练和线上资源成本。本地对照口径：相对单前向全特征基线，实验组 NDCG@10 +2.42%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2501.15816">原论文</a> · <a href="../../../../reproductions/2501.15816-adaf2m2/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TWIN V2: Scaling Ultra-Long User Behavior Sequence Modeling for Enhanced CTR Prediction at Kuaishou 搜广推与 LLM 应用 Kuaishou 2024-07-23 离线层次聚类将百万级生命周期行为压缩成带规模信息的虚拟物品；在线 GSU 检索相关簇，ESU 以 cluster-aware target attention 精排。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上执行论文的候选相关检索、层级压缩或蒸馏目标；未使用公司私有日志与线上 serving，线上 A/B 只引用原文。本地相对变化不得与原文指标混写。本地对照口径：基线为 shared transition + content baseline，实验组为 TWIN-V2，只改变论文核心机制；ndcg_at_10 0.0354 → 0.0433，相对基线 +22.45%。  ranking long-sequence training-serving 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-twin-v2-72f26bc8">TWIN V2: Scaling Ultra-Long User Behavior Sequence Modeling for Enhanced CTR Prediction at Kuaishou</h2>
<p class="ar-learning-card__meta">Kuaishou · 论文公开：2024-07-23</p>
<p><strong>方法要点：</strong>离线层次聚类将百万级生命周期行为压缩成带规模信息的虚拟物品；在线 GSU 检索相关簇，ESU 以 cluster-aware target attention 精排。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上执行论文的候选相关检索、层级压缩或蒸馏目标；未使用公司私有日志与线上 serving，线上 A/B 只引用原文。本地相对变化不得与原文指标混写。本地对照口径：基线为 shared transition + content baseline，实验组为 TWIN-V2，只改变论文核心机制；ndcg_at_10 0.0354 → 0.0433，相对基线 +22.45%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2407.16357">原论文</a> · <a href="../../../../reproductions/2407.16357-twin-v2/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations 搜广推与 LLM 应用 Meta 2024-02-27 HSTU 在输入窗口内逐层更新历史 token，用因果交互建模行为之间的依赖。学习重点是把历史首算成本与 M-FALCON 缓存后的多候选增量成本分开。 保真度：核心机制复现。本地为核心层与 all-position 训练的缩小实现，未复刻异构 action/time、Stochastic Length 或 M-FALCON。MovieLens-100K 的三 seed 结果仅适用于匹配 SASRec 的本地协议，不能外推到工业系统。 有 M-FALCON 缓存后，哪些历史计算可以共享，哪些候选路径仍要重算？  搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-hstu-2703dd1e">Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations</h2>
<p class="ar-learning-card__meta">Meta · 论文公开：2024-02-27</p>
<p><strong>方法要点：</strong>HSTU 在输入窗口内逐层更新历史 token，用因果交互建模行为之间的依赖。学习重点是把历史首算成本与 M-FALCON 缓存后的多候选增量成本分开。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。本地为核心层与 all-position 训练的缩小实现，未复刻异构 action/time、Stochastic Length 或 M-FALCON。MovieLens-100K 的三 seed 结果仅适用于匹配 SASRec 的本地协议，不能外推到工业系统。</p></details>
<p class="ar-learning-question"><strong>想一想：</strong>有 M-FALCON 缓存后，哪些历史计算可以共享，哪些候选路径仍要重算？</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2402.17152">原论文</a> · <a href="../../../../reproductions/2402.17152-hstu/">实现解读</a> · <a href="../../../001-hstu-longer-slimper/">阅读精选对比</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="DCN V2: Improved Deep &amp; Cross Network and Practical Lessons for Web-scale Learning to Rank Systems 搜广推与 LLM 应用 Google 2020-08-19 DCN-V2 显式构造有界阶数的特征交互，并用低秩矩阵与专家混合降低 web-scale ranking 的参数和计算成本。 Fidelity: 核心机制复现。实现低秩 cross experts、输入相关 gate 与 deep tower。未使用 Google 私有数据和生产级专家规模；结果只验证显式交叉在公开数据上的作用。本地对照口径：基线是 deep-only；实验组是两层低秩 cross experts 与 gate；三 seed NDCG@10 相对 +22.87%。  ranking classic feature-interaction 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-dcn-v2-7ac56e9e">DCN V2: Improved Deep &amp; Cross Network and Practical Lessons for Web-scale Learning to Rank Systems</h2>
<p class="ar-learning-card__meta">Google · 论文公开：2020-08-19</p>
<p><strong>方法要点：</strong>DCN-V2 显式构造有界阶数的特征交互，并用低秩矩阵与专家混合降低 web-scale ranking 的参数和计算成本。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。实现低秩 cross experts、输入相关 gate 与 deep tower。未使用 Google 私有数据和生产级专家规模；结果只验证显式交叉在公开数据上的作用。本地对照口径：基线是 deep-only；实验组是两层低秩 cross experts 与 gate；三 seed NDCG@10 相对 +22.87%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2008.13535">原论文</a> · <a href="../../../../reproductions/2008.13535-dcn-v2/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Search-based User Interest Modeling with Lifelong Sequential Behavior Data for CTR Prediction 搜广推与 LLM 应用 Alibaba 2020-06-10 以候选 item 为 query，GSU 从终身行为中快速搜索相关子序列，ESU 再计算候选与子序列的精确注意力。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上执行论文的候选相关检索、层级压缩或蒸馏目标；未使用公司私有日志与线上 serving，线上 A/B 只引用原文。本地相对变化不得与原文指标混写。本地对照口径：基线为 shared transition + content baseline，实验组为 SIM，只改变论文核心机制；ndcg_at_10 0.0354 → 0.0471，相对基线 +32.97%。  ranking long-sequence training-serving 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-sim-df73a28d">Search-based User Interest Modeling with Lifelong Sequential Behavior Data for CTR Prediction</h2>
<p class="ar-learning-card__meta">Alibaba · 论文公开：2020-06-10</p>
<p><strong>方法要点：</strong>以候选 item 为 query，GSU 从终身行为中快速搜索相关子序列，ESU 再计算候选与子序列的精确注意力。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上执行论文的候选相关检索、层级压缩或蒸馏目标；未使用公司私有日志与线上 serving，线上 A/B 只引用原文。本地相对变化不得与原文指标混写。本地对照口径：基线为 shared transition + content baseline，实验组为 SIM，只改变论文核心机制；ndcg_at_10 0.0354 → 0.0471，相对基线 +32.97%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2006.05639">原论文</a> · <a href="../../../../reproductions/2006.05639-sim/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Behavior Sequence Transformer for E-commerce Recommendation in Alibaba 搜广推与 LLM 应用 Alibaba 2019-05-15 BST 用自注意力统一建模行为之间及行为与候选之间的关系，替代固定 pooling 或单一目标注意力。 Fidelity: 核心机制复现。实现候选 token、位置编码和行为序列 Transformer。公开数据替代淘宝日志；没有复刻用户画像、上下文特征和生产推理系统。本地对照口径：基线是 DIN；实验组是候选参与编码的 Transformer；三 seed NDCG@10 相对 +20.29%。  ranking classic sequence-modeling 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-bst-730383cc">Behavior Sequence Transformer for E-commerce Recommendation in Alibaba</h2>
<p class="ar-learning-card__meta">Alibaba · 论文公开：2019-05-15</p>
<p><strong>方法要点：</strong>BST 用自注意力统一建模行为之间及行为与候选之间的关系，替代固定 pooling 或单一目标注意力。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。实现候选 token、位置编码和行为序列 Transformer。公开数据替代淘宝日志；没有复刻用户画像、上下文特征和生产推理系统。本地对照口径：基线是 DIN；实验组是候选参与编码的 Transformer；三 seed NDCG@10 相对 +20.29%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1905.06874">原论文</a> · <a href="../../../../reproductions/1905.06874-bst/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Deep Interest Evolution Network for Click-Through Rate Prediction 搜广推与 LLM 应用 Alibaba 2018-09-11 DIN 直接激活历史兴趣，DIEN 则先用辅助监督抽取逐步兴趣，再让目标商品控制兴趣状态的演化速度。 Fidelity: 核心机制复现。实现兴趣抽取 GRU、下一行为辅助损失和候选相关兴趣演化。MovieLens 的短序列和稀疏信号不能替代 Taobao 广告特征；未使用生产 fused AUGRU kernel。本地对照口径：基线是同一训练协议的 DIN；实验组加入 GRU、辅助目标和候选相关演化；三 seed NDCG@10 相对 -1.98%，未迁移论文收益。  ranking classic sequence-modeling 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-dien-3d6c73b7">Deep Interest Evolution Network for Click-Through Rate Prediction</h2>
<p class="ar-learning-card__meta">Alibaba · 论文公开：2018-09-11</p>
<p><strong>方法要点：</strong>DIN 直接激活历史兴趣，DIEN 则先用辅助监督抽取逐步兴趣，再让目标商品控制兴趣状态的演化速度。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。实现兴趣抽取 GRU、下一行为辅助损失和候选相关兴趣演化。MovieLens 的短序列和稀疏信号不能替代 Taobao 广告特征；未使用生产 fused AUGRU kernel。本地对照口径：基线是同一训练协议的 DIN；实验组加入 GRU、辅助目标和候选相关演化；三 seed NDCG@10 相对 -1.98%，未迁移论文收益。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1809.03672">原论文</a> · <a href="../../../../reproductions/1809.03672-dien/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Self-Attentive Sequential Recommendation 搜广推与 LLM 应用 UC San Diego 2018-08-20 Markov Chain 偏重最近行为，RNN 又需要逐步计算。SASRec 用因果自注意力直接选择序列中与下一物品相关的行为，在稀疏与稠密数据之间取得更灵活的感受野，并成为序列推荐常用基线。 保真度：完整核心链路复现。保真度：完整核心链路复现。模型、原论文 pairwise BCE 训练目标与序列推理均实际执行；仅把公开数据从 MovieLens-1M 缩到 MovieLens-100K，并采用更严格的全库评估。本地对照口径：基线是 popularity 排序；实验组是 SASRec；主指标 NDCG@10 从 0.02969 降至 0.02933（-1.24%）。这是跨模型基线比较，不是 SASRec 模块消融。   搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-sasrec-6f67bc6e">Self-Attentive Sequential Recommendation</h2>
<p class="ar-learning-card__meta">UC San Diego · 论文公开：2018-08-20</p>
<p><strong>方法要点：</strong>Markov Chain 偏重最近行为，RNN 又需要逐步计算。SASRec 用因果自注意力直接选择序列中与下一物品相关的行为，在稀疏与稠密数据之间取得更灵活的感受野，并成为序列推荐常用基线。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：完整核心链路复现。保真度：完整核心链路复现。模型、原论文 pairwise BCE 训练目标与序列推理均实际执行；仅把公开数据从 MovieLens-1M 缩到 MovieLens-100K，并采用更严格的全库评估。本地对照口径：基线是 popularity 排序；实验组是 SASRec；主指标 NDCG@10 从 0.02969 降至 0.02933（-1.24%）。这是跨模型基线比较，不是 SASRec 模块消融。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1808.09781">原论文</a> · <a href="../../../../reproductions/1808.09781-sasrec/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Deep Interest Network for Click-Through Rate Prediction 搜广推与 LLM 应用 Alibaba 2017-06-21 传统 CTR 模型把用户全部行为压成固定向量，但用户与候选物品相关的兴趣只占历史的一部分。DIN 不再生成一个与候选无关的用户向量，而是用候选物品逐条激活历史行为，再把局部兴趣送入点击网络；Dice 根据当前特征分布自适应调整激活边界。 保真度：核心机制复现。保真度：核心机制复现。本实现实际训练候选物品条件化的 local activation、加权兴趣池化、Dice 与 CTR 网络；未复刻 Alibaba 私有稀疏特征、mini-batch-aware regularization 和生产 serving。本地对照口径：基线是移除 candidate-aware attention、改用 mean pooling 的同参数模型；实验组是 DIN；主指标 NDCG@10 从 0.01783 降至 0.01659（-6.97%）。这是 DIN 核心注意力的内部消融，不是相对其他推荐模型的提升。   搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-din-dfe7b0eb">Deep Interest Network for Click-Through Rate Prediction</h2>
<p class="ar-learning-card__meta">Alibaba · 论文公开：2017-06-21</p>
<p><strong>方法要点：</strong>传统 CTR 模型把用户全部行为压成固定向量，但用户与候选物品相关的兴趣只占历史的一部分。DIN 不再生成一个与候选无关的用户向量，而是用候选物品逐条激活历史行为，再把局部兴趣送入点击网络；Dice 根据当前特征分布自适应调整激活边界。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。本实现实际训练候选物品条件化的 local activation、加权兴趣池化、Dice 与 CTR 网络；未复刻 Alibaba 私有稀疏特征、mini-batch-aware regularization 和生产 serving。本地对照口径：基线是移除 candidate-aware attention、改用 mean pooling 的同参数模型；实验组是 DIN；主指标 NDCG@10 从 0.01783 降至 0.01659（-6.97%）。这是 DIN 核心注意力的内部消融，不是相对其他推荐模型的提升。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1706.06978">原论文</a> · <a href="../../../../reproductions/1706.06978-din/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="DeepFM: A Factorization-Machine based Neural Network for CTR Prediction 搜广推与 LLM 应用 Huawei Noah&#x27;s Ark Lab 2017-03-13 CTR 排序既依赖低阶组合特征，也依赖高阶非线性交互。传统 Wide &amp; Deep 需要人工构造 wide 特征，DeepFM 则让两条路径端到端共享 embedding。模型把 FM 的一阶/二阶项与 MLP 输出相加。相同 field embedding 同时进入两条路径，减少人工交叉和重复参数。 复现级别：核心机制复现。复现级别：核心机制复现。实际联合训练 FM 二阶交互与 deep 分支；私有工业特征和线上系统不在本地复现范围。本地对照口径：基线为 embedding MLP，实验组为共享 embedding 的 FM + deep 分支；NDCG@10 相对 +23.58%，见 metrics/movielens-100k-seeds42-44.json。  ranking classic feature-interaction 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-deepfm-65a63b7d">DeepFM: A Factorization-Machine based Neural Network for CTR Prediction</h2>
<p class="ar-learning-card__meta">Huawei Noah&#x27;s Ark Lab · 论文公开：2017-03-13</p>
<p><strong>方法要点：</strong>CTR 排序既依赖低阶组合特征，也依赖高阶非线性交互。传统 Wide &amp; Deep 需要人工构造 wide 特征，DeepFM 则让两条路径端到端共享 embedding。模型把 FM 的一阶/二阶项与 MLP 输出相加。相同 field embedding 同时进入两条路径，减少人工交叉和重复参数。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制复现。复现级别：核心机制复现。实际联合训练 FM 二阶交互与 deep 分支；私有工业特征和线上系统不在本地复现范围。本地对照口径：基线为 embedding MLP，实验组为共享 embedding 的 FM + deep 分支；NDCG@10 相对 +23.58%，见 metrics/movielens-100k-seeds42-44.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1703.04247">原论文</a> · <a href="../../../../reproductions/1703.04247-deepfm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Wide &amp; Deep Learning for Recommender Systems 搜广推与 LLM 应用 Google 2016-06-24 纯线性模型善于记忆稀疏共现但泛化弱，纯 DNN 能泛化却可能推荐不相关组合。论文联合训练两路并共享最终 logit。 Fidelity: 核心机制复现。本地实现联合记忆型 wide 交叉与泛化型 deep tower。公开 MovieLens 替代 Google Play 私有日志；未复刻生产特征工程、分布式训练与 serving。本地对照口径：基线是参数匹配的 deep-only 模型；实验组加入 candidate 与 genre 交叉的 wide 路径；MovieLens-100K 三 seed 全库 NDCG@10 相对 +5.45%。  ranking classic feature-interaction 搜广推 用户历史与排序骨干">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="paper-recommendation-wide-deep-604050a0">Wide &amp; Deep Learning for Recommender Systems</h2>
<p class="ar-learning-card__meta">Google · 论文公开：2016-06-24</p>
<p><strong>方法要点：</strong>纯线性模型善于记忆稀疏共现但泛化弱，纯 DNN 能泛化却可能推荐不相关组合。论文联合训练两路并共享最终 logit。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地实现联合记忆型 wide 交叉与泛化型 deep tower。公开 MovieLens 替代 Google Play 私有日志；未复刻生产特征工程、分布式训练与 serving。本地对照口径：基线是参数匹配的 deep-only 模型；实验组加入 candidate 与 genre 交叉的 wide 路径；MovieLens-100K 三 seed 全库 NDCG@10 相对 +5.45%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1606.07792">原论文</a> · <a href="../../../../reproductions/1606.07792-wide-deep/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
