---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 用户历史与排序骨干

[搜广推](index.md) / 81 个问题 · 73 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">81 个问题 · 73 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:echo-selector-loss" data-paper-title="ECHO: Efficient Cascade with Homogeneous Operators for Distillation-Guided 100K-Sequence Modeling" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="ECHO: Efficient Cascade with Homogeneous Operators for Distillation-Guided 100K-Sequence Modeling 搜广推与 LLM 应用 Kuaishou Technology 2026-10-20 将100K历史压成少量潜向量会丢失记录地址；逐候选扫描全部历史又过贵。ECHO让用户侧DS保留原始记录，再由目标侧TFR选更小子集。训练侧候选感知教师通过完整软分布和选择边界监督DS，教师相关性参数还导出到检索和聚合。线上不运行DS，也不扫描完整历史。 原文完整实验成本过高，不复现（审查 DONE）。仅L1诊断，不是完整ECHO/TWIN或推荐能力；已实现选择器蒸馏损失，在真实A100上验证公式、梯度和短时更新。仅L1诊断，不是完整ECHO/TWIN或推荐能力；原文完整实验成本过高，不复现（审查 DONE）。固定合成logit、seed42/43/44，在A100执行逐标量CE参考、实际学生参数更新、教师无梯度、padding零梯度及同排序无有效边界配对的负对照。未加载预训练checkpoint，无推荐准确率或正式比较资格。  长序列推荐 蒸馏选择与边界监督 搜广推 用户历史与排序骨干 ECHO为什么既蒸馏完整教师分布，又特别惩罚选择边界上的漏选？ 完整软分布传递教师对各历史项的相对相关性，但学生仍可能在有限选择预算下漏掉关键记录。边界监督比较高质量漏选项与低质量已选项，直接推动二者交换次序；权重来自停止梯度的教师差异。该组件保留记录地址而非只压成潜向量，本地仅验证损失与梯度，并未验证100K推荐效果。 示意：学生只选两条历史，却漏掉教师最看重的一条、保留一条低相关记录；软标签教整体偏好，边界配对则明确要求把这两条的选择顺序调换。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-echo-selector-loss-59466a02" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1e00f3b69701b501">ECHO为什么既蒸馏完整教师分布，又特别惩罚选择边界上的漏选？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aecho-selector-loss">ECHO: Efficient Cascade with Homogeneous Operators for Distillation-Guided 100K-Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>完整软分布传递教师对各历史项的相对相关性，但学生仍可能在有限选择预算下漏掉关键记录。边界监督比较高质量漏选项与低质量已选项，直接推动二者交换次序；权重来自停止梯度的教师差异。该组件保留记录地址而非只压成潜向量，本地仅验证损失与梯度，并未验证100K推荐效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>学生只选两条历史，却漏掉教师最看重的一条、保留一条低相关记录；软标签教整体偏好，边界配对则明确要求把这两条的选择顺序调换。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28569v1">原论文</a> · <a href="../../../../recommendation-components/2610.28569-echo-selector-loss/">实现解读</a> · <a href="#qa-1e00f3b69701b501">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:repair-state" data-paper-title="Not All Is Lost: Repairing Lossy User Preference States of Personalization Encoders" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Not All Is Lost: Repairing Lossy User Preference States of Personalization Encoders 搜广推与 LLM 应用 原文首页未列第一作者机构 2026-10-01 冻结 encoder 与原 task head，从已有 forward cache 中比较各 timestep 表征和当前 preference state，选择长程、近期或局部 burst 的纠正证据并做 residual repair。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 frozen-cache evidence selection 与 residual correction；用户批准为学术/Evolve 例外，无线上 A/B。收录例外：用户于 2026-10-02 明确批准的学术/Evolve 机制例外；论文没有量化线上 A/B，不进入工业证据结论。执行 frozen-cache evidence selection 与 residual correction；用户批准为学术/Evolve 例外，无线上 A/B。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。  personalization state-repair sequential-recommendation 搜广推 用户历史与排序骨干 Repair-State 为什么在冻结编码器和任务头的情况下，用历史状态差分修补当前 preference state？ 冻结模型避免重新训练整条链路，已有前向缓存则提供不同时间位置的证据。方法比较历史状态与当前偏好，选择长程、近期或突发片段，用加权残差把被压缩丢失的相关方向补回来。它纠正的是当前表示，不会创造缓存中不存在的信息；选择错误证据也可能把过时兴趣重新注入。 示意：当前汇总偏好被长期电影兴趣主导，但最近连续看育儿内容。无需重训编码器，可从缓存挑出这段突发证据，以差分残差补入当前状态，再交给原任务头。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-repair-state-eec04848" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d799684e7cf1cfcc">Repair-State 为什么在冻结编码器和任务头的情况下，用历史状态差分修补当前 preference state？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arepair-state">Not All Is Lost: Repairing Lossy User Preference States of Personalization Encoders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冻结模型避免重新训练整条链路，已有前向缓存则提供不同时间位置的证据。方法比较历史状态与当前偏好，选择长程、近期或突发片段，用加权残差把被压缩丢失的相关方向补回来。它纠正的是当前表示，不会创造缓存中不存在的信息；选择错误证据也可能把过时兴趣重新注入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>当前汇总偏好被长期电影兴趣主导，但最近连续看育儿内容。无需重训编码器，可从缓存挑出这段突发证据，以差分残差补入当前状态，再交给原任务头。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01270">原论文</a> · <a href="../../../../reproductions/2610.01270-repair-state/">实现解读</a> · <a href="#qa-d799684e7cf1cfcc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:helix" data-paper-title="HELIX: Purified and Unified - Rethinking Feature Interaction and Sequence Modeling for Large-Scale Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="HELIX: Purified and Unified - Rethinking Feature Interaction and Sequence Modeling for Large-Scale Recommendation 搜广推与 LLM 应用 TikTok / ByteDance 2026-09-29 工业排序通常分别扩大异构特征交互与长行为序列，两条轴单独扩展都会遇到上限。HELIX 交错 SeqFormer 与 MixFormer，但强制信息只从可复用的 user-only sequence state 流向 candidate-conditioned mix tokens，使用户侧序列计算能跨候选复用，同时保持两轴的跨深度通信。 复现级别：L1 架构机制。复现级别：L1 架构机制。实现三流 token、单向 U-only 缓存、跨深度 MixFormer/SeqFormer 交互与多任务头；没有 TikTok 私有数据和线上流量。本地使用合成张量，不含私有训练数据、线上 A/B 或论文规模系统优化，因此 reproduction_level=concept_demo。只有接入公开公平数据、基线和多种子 validation/test 隔离后，才能讨论效果复现或进入 Evolve 搜索空间。本地对照口径：基线为同一 user cache 下的候选 A，实验组为候选 B；只检查候选敏感性与 cache 不变量，没有公开效果指标，相对变化不适用。  ranking feature-interaction sequence-modeling 搜广推 用户历史与排序骨干 HELIX让序列状态流向候选混合token，为什么禁止候选反向写回共享序列？ 单向依赖使昂贵的用户历史编码保持候选无关，从而一次请求内可复用于多候选；候选侧仍能在多层读取用户信息，保留深交互。若允许反向写回，序列状态就随候选变化，复用前提被破坏。本地只验证候选敏感性和缓存不变量，不代表已获得生产吞吐或推荐提升。 示意：评相机和鞋时共用同一份历史状态，各候选分别读取；若相机信息先改写了历史，再把该缓存用于鞋，就混入了另一候选，已不再是共享用户证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-helix-94ed43e6" class="ar-learning-paper-anchor"></span>
<h2 id="qa-fdc7e424eea56b8a">HELIX让序列状态流向候选混合token，为什么禁止候选反向写回共享序列？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahelix">HELIX: Purified and Unified - Rethinking Feature Interaction and Sequence Modeling for Large-Scale Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · TikTok / ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单向依赖使昂贵的用户历史编码保持候选无关，从而一次请求内可复用于多候选；候选侧仍能在多层读取用户信息，保留深交互。若允许反向写回，序列状态就随候选变化，复用前提被破坏。本地只验证候选敏感性和缓存不变量，不代表已获得生产吞吐或推荐提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>评相机和鞋时共用同一份历史状态，各候选分别读取；若相机信息先改写了历史，再把该缓存用于鞋，就混入了另一候选，已不再是共享用户证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37183">原论文</a> · <a href="../../../../reproductions/2609.37183-helix/">实现解读</a> · <a href="#qa-fdc7e424eea56b8a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recap-ctr" data-paper-title="Beyond Interaction Capacity: Estimator Scaling with Recursive Models for CTR Prediction" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Beyond Interaction Capacity: Estimator Scaling with Recursive Models for CTR Prediction 搜广推与 LLM 应用 Georgia Institute of Technology / Google Research 2026-09-29 不再只增加单个 CTR predictor 的交互容量，而是扩展相关 estimator；RECAP 在共享参数的递归 backbone 上形成多条 route，并结合独立模型蒸馏、训练轨迹 EMA 与推理 route 平均。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行共享递归、route 平均、trajectory EMA 和可运行 RankMixer Evolve block；未做 benchmark 训练或独立模型蒸馏。执行共享递归、route 平均、trajectory EMA 和可运行 RankMixer Evolve block；未做 benchmark 训练或独立模型蒸馏。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  ctr estimator-scaling recursive-network 搜广推 用户历史与排序骨干 RECAP-CTR 为什么共享递归 block 却平均多个 route 的预测，还保留训练轨迹 EMA？ 单个大预测器可能仍缺少互补估计。共享递归结构用不同路径产生多个 logit，在控制参数开销的同时增加估计差异，推理平均降低单一路径波动；轨迹 EMA 则沿训练时间平滑参数。路径平均和时间平均作用于不同变化来源，但相关路径的收益有限，本地仅验证状态与算子不变量，不能冒充规模效果。 示意：同一共享 block 经两条递归路径得到略不同点击预测，平均可减小某一路径偶然偏高。EMA 另行平滑相邻训练步的模型，它不是又增加一个完全独立的模型。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-recap-ctr-8a9efe0a" class="ar-learning-paper-anchor"></span>
<h2 id="qa-6d48a3ea0b094184">RECAP-CTR 为什么共享递归 block 却平均多个 route 的预测，还保留训练轨迹 EMA？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecap-ctr">Beyond Interaction Capacity: Estimator Scaling with Recursive Models for CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Georgia Institute of Technology / Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单个大预测器可能仍缺少互补估计。共享递归结构用不同路径产生多个 logit，在控制参数开销的同时增加估计差异，推理平均降低单一路径波动；轨迹 EMA 则沿训练时间平滑参数。路径平均和时间平均作用于不同变化来源，但相关路径的收益有限，本地仅验证状态与算子不变量，不能冒充规模效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一共享 block 经两条递归路径得到略不同点击预测，平均可减小某一路径偶然偏高。EMA 另行平滑相邻训练步的模型，它不是又增加一个完全独立的模型。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37905">原论文</a> · <a href="../../../../reproductions/2609.37905-recap-ctr/">实现解读</a> · <a href="#qa-6d48a3ea0b094184">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onetrans-v2" data-paper-title="OneTrans-V2: Unifying Retrieval, Pre-rank, and Fine-rank with One Transformer in Industrial Recommender" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OneTrans-V2: Unifying Retrieval, Pre-rank, and Fine-rank with One Transformer in Industrial Recommender 搜广推与 LLM 应用 ByteDance 2026-09-23 工业推荐先检索海量候选，再预排缩小集合，最后精排。三套独立模型会反复编码同一用户历史，也难以让精排经验稳定反馈给上游。OneTrans-V2 保留三个阶段各自的输入与目标，却让它们共享一个因果 Transformer 用户上下文。行为序列不读阶段 token；每个阶段 token 只读请求时刻前的行为，不在阶段之间交叉读取。这既复用昂贵的用户编码，也防止未来信息泄漏。 故 adapter 标记为 concept_demo，不声称复刻 GMV、QPS 或完整 DCGR 业务控制。Fidelity：概念验证（非论文完整复现）；证据等级：L1 机制验证，使用完整 MovieLens-1M。三阶段核心计算与损失已执行，但公开 MovieLens 没有交易、广告供给和真实曝光漏斗，不能把代理指标解释为论文的业务提升。已执行共享因果用户编码、阶段隔离、三级 SID 自回归、可观测代理决策、双阶段多目标 BCE 与精排向预排蒸馏。未执行真实购买/金额/广告决策、工业物品编码、稀疏 MoE、Sequence-Native Training 的跨曝光摊销、线上服务与 A/B。  multi-stage-ranking generative-retrieval cross-stage-distillation 搜广推 用户历史与排序骨干 OneTrans-V2 三个阶段共享用户上下文，为什么又禁止阶段 token 彼此交叉读取？ 用户行为编码是三个阶段反复使用的昂贵公共部分，共享它可以减少重复计算。各阶段保留自己的输入和目标，并只读取请求时刻之前的行为，防止下游信息或未来行为通过注意力路径泄漏到上游。精排知识通过受控蒸馏损失反馈给预排，而非开放任意读取；本地没有独立三级基线，不能声称级联效果改善。 示意：召回、预排、精排都读同一份已发生的浏览历史，但召回 token 不直接看精排标签或未来点击。预排学习精排判断时走停止梯度的教师信号，而不是偷看答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-onetrans-v2-65020d24" class="ar-learning-paper-anchor"></span>
<h2 id="qa-e6a597373c4b5370">OneTrans-V2 三个阶段共享用户上下文，为什么又禁止阶段 token 彼此交叉读取？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonetrans-v2">OneTrans-V2: Unifying Retrieval, Pre-rank, and Fine-rank with One Transformer in Industrial Recommender</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用户行为编码是三个阶段反复使用的昂贵公共部分，共享它可以减少重复计算。各阶段保留自己的输入和目标，并只读取请求时刻之前的行为，防止下游信息或未来行为通过注意力路径泄漏到上游。精排知识通过受控蒸馏损失反馈给预排，而非开放任意读取；本地没有独立三级基线，不能声称级联效果改善。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>召回、预排、精排都读同一份已发生的浏览历史，但召回 token 不直接看精排标签或未来点击。预排学习精排判断时走停止梯度的教师信号，而不是偷看答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.28589">原论文</a> · <a href="../../../../reproductions/2609.28589-onetrans-v2/">实现解读</a> · <a href="#qa-e6a597373c4b5370">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:lazformer" data-paper-title="LazFormer: Scaling Transformers for Industrial Recommendation via Transferable Generative Pre-training" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="LazFormer: Scaling Transformers for Industrial Recommendation via Transferable Generative Pre-training 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-09-14 先做可迁移生成式预训练，再用 ranking residual adapter、近密远疏 token 与 hybrid sparse attention 适配排序；两周 A/B 报告 IPV +5.21%、GMV +9.85%。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。私有日志、生产 checkpoint 与 serving 栈均未复刻。本地只验证公开数据上的核心状态转换；未复刻私有训练数据、大模型生成器、生产流量反馈或在线服务。当前不映射 evolve，避免 registry-only 标签。线上数字来自论文正文 A/B，不与本地 MovieLens 结果混写。本地 seeds 42/43/44 见 metrics/movielens-100k-seeds42-44.json。首个 seed 的统一 NDCG@10 基线为 0.05401，实验组为 0.05048，相对变化 -6.53%。  ranking generative-pretraining residual-adapter hybrid-sparse-attention 搜广推 用户历史与排序骨干 LazFormer为什么在可迁移预训练骨干之外保留ranking residual adapter？ 生成式预训练学习通用序列规律，工业排序还需要候选交互与高频更新，直接全量覆盖可能破坏可迁移知识。残差适配为排序新增专门路径，近密远疏token和稀疏attention再控制长历史成本。本地仅保留确定性映射与适配组合组件，不能把其打分结果包装成完整生成式预训练已复现。 示意：预训骨干已掌握长期消费模式，新促销任务需要额外价格交互；残差路径可补这种任务信息，但用一个固定加权器不能证明原论文训练链路已经跑通。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-lazformer-e00dc3de" class="ar-learning-paper-anchor"></span>
<h2 id="qa-2a1ae90a18185961">LazFormer为什么在可迁移预训练骨干之外保留ranking residual adapter？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alazformer">LazFormer: Scaling Transformers for Industrial Recommendation via Transferable Generative Pre-training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>生成式预训练学习通用序列规律，工业排序还需要候选交互与高频更新，直接全量覆盖可能破坏可迁移知识。残差适配为排序新增专门路径，近密远疏token和稀疏attention再控制长历史成本。本地仅保留确定性映射与适配组合组件，不能把其打分结果包装成完整生成式预训练已复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>预训骨干已掌握长期消费模式，新促销任务需要额外价格交互；残差路径可补这种任务信息，但用一个固定加权器不能证明原论文训练链路已经跑通。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.14978">原论文</a> · <a href="../../../../reproductions/2609.14978-lazformer/">实现解读</a> · <a href="#qa-2a1ae90a18185961">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:chronicle-rec" data-paper-title="ChronicleRec: Pre-training Temporally Anchored Tokens for Lifelong User Modeling" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="ChronicleRec: Pre-training Temporally Anchored Tokens for Lifelong User Modeling 搜广推与 LLM 应用 Tencent 2026-09-11 逐候选检索超长历史会重复计算，统一压成无序 token 又容易丢失时间结构。ChronicleRec 对近、中、远历史采用逐渐增大的合并步幅，把 query token 插入时间轴并使用 causal encoder，使每个 token 只概括其锚点之前的历史；多分支分别遮掉不同长度的近期行为，alignment 预训练再用压缩过去预测近期意图。生成的 Chronicle Tokens 与候选无关，可缓存并复用于多个候选。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行近密远疏合并、因果 query 锚点、多 horizon 分支与面向近期目标的 alignment；不复刻腾讯私有 MixFormer 与缓存系统。公开短序列不能代表 2K–4K 乃至更长的生产历史；本地用线性 alignment 替代四层 causal Transformer，未复刻 AdLive、MixFormer 和异步 KV cache。实现只声明 CPU 公开数据核心机制。MovieLens 100K、seeds 42/43/44 的固定协议见 metrics/movielens-100k-seeds42-44.json。  ranking long-sequence sequence-compression pretraining 搜广推 用户历史与排序骨干 Chronicle Token为什么必须带时间锚点并只概括锚点之前的历史？ 没有时间边界的摘要容易把未来行为混入较早时刻的表示，既破坏训练因果性，也让跨请求缓存语义不清。ChronicleRec以不同粒度压缩远近历史，在时间轴上放置query，只允许它读取此前事件，再用多种近期遮蔽对齐短期意图。候选无关的锚定摘要才具备跨候选复用的基础。 示意：周三的摘要不能包含周五才购买的相机，否则周四推荐镜头时已偷看未来；固定时间锚点后，可让同一摘要服务当时的多个候选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-chronicle-rec-efcf1d9a" class="ar-learning-paper-anchor"></span>
<h2 id="qa-fe7e940e49d3f624">Chronicle Token为什么必须带时间锚点并只概括锚点之前的历史？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Achronicle-rec">ChronicleRec: Pre-training Temporally Anchored Tokens for Lifelong User Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有时间边界的摘要容易把未来行为混入较早时刻的表示，既破坏训练因果性，也让跨请求缓存语义不清。ChronicleRec以不同粒度压缩远近历史，在时间轴上放置query，只允许它读取此前事件，再用多种近期遮蔽对齐短期意图。候选无关的锚定摘要才具备跨候选复用的基础。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>周三的摘要不能包含周五才购买的相机，否则周四推荐镜头时已偷看未来；固定时间锚点后，可让同一摘要服务当时的多个候选。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.12375">原论文</a> · <a href="../../../../reproductions/2609.12375-chronicle-rec/">实现解读</a> · <a href="#qa-fe7e940e49d3f624">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unirec" data-paper-title="UniRec: Cross-Stage Multi-Task Fusion with Preference Optimization for Cascaded Recommender Systems" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="UniRec: Cross-Stage Multi-Task Fusion with Preference Optimization for Cascaded Recommender Systems 搜广推与 LLM 应用 Kuaishou 2026-09-10 预排和精排的候选范围、输入质量和延迟约束不同，直接复制精排的融合权重不能保证上游排序一致。UniRec 以部分共享 embedding、独立 DCN/Mixer 与 AutoInt-Lite 塔联合训练两阶段融合模块；下游偏好只作为上游训练监督，不作为预排线上输入。v3 明确保留多目标冲突的 CPPA、置信剪枝 CAPP，以及以组内 KL 抑制视频时长等属性引起的分布漂移。 成本过高，不复现（审查 DONE）。复现级别：组件诊断，非完整论文复现。复现级别：组件诊断，非完整论文复现。新增 v3 的 CPPA/CAPP、AGRR 组内 KL 与跨阶段偏好目标，验证前向、梯度和负对照。旧 unirec NumPy adapter 是固定权重启发式，现明确降为 concept_demo；历史测量与负结果完整保留。旧 MovieLens 100K、seeds 42/43/44 结果见 metrics/movielens-100k-seeds42-44.json。  pre-ranking ranking cross-stage-alignment industrial-recommendation 搜广推 用户历史与排序骨干 UniRec 的 CPPA 为什么保留同一 pair 的正反目标证据，而不先多数表决成单一胜负？ 点击、购买等目标可能对同一候选对给出相反偏好，多数表决会抹去冲突强度和少数目标。CPPA 分别累积正反证据，两种方向的 softplus 惩罚同时存在；CAPP 再选置信差距大的有向 pair，属性组 KL 控制分布漂移。下游偏好用于训练上游，不能作为预排服务时偷读的输入。 示意：甲比乙更易点击，乙比甲更易购买。保留两方向损失可表达这份取舍；若直接三票对两票判甲胜，购买侧反对证据就会被丢掉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-unirec-cd2efe22" class="ar-learning-paper-anchor"></span>
<h2 id="qa-0c25f39de037db51">UniRec 的 CPPA 为什么保留同一 pair 的正反目标证据，而不先多数表决成单一胜负？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunirec">UniRec: Cross-Stage Multi-Task Fusion with Preference Optimization for Cascaded Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>点击、购买等目标可能对同一候选对给出相反偏好，多数表决会抹去冲突强度和少数目标。CPPA 分别累积正反证据，两种方向的 softplus 惩罚同时存在；CAPP 再选置信差距大的有向 pair，属性组 KL 控制分布漂移。下游偏好用于训练上游，不能作为预排服务时偷读的输入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>甲比乙更易点击，乙比甲更易购买。保留两方向损失可表达这份取舍；若直接三票对两票判甲胜，购买侧反对证据就会被丢掉。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11052">原论文</a> · <a href="../../../../reproductions/2609.11052-unirec/">实现解读</a> · <a href="#qa-0c25f39de037db51">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sequenceo1" data-paper-title="SequenceO1: End-to-End Ultra-Long (100K) Sequence Modeling in Recommendation with Low-Rank Caching" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="SequenceO1: End-to-End Ultra-Long (100K) Sequence Modeling in Recommendation with Low-Rank Caching 搜广推与 LLM 应用 ByteDance / Douyin 2026-09-08 直接注意全部历史难以服务 100K 级用户行为。SequenceO1 用 Sketch Attention 把远期历史压缩为固定数量原型，并保留近期行为分支；STCA 让 sketch 与 recent 信息并行交互，控制成本同时保留长期兴趣。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行固定预算 prototype sketch 与 recent 双分支；MovieLens 不具备论文的 100K 事件历史。MovieLens 100K 三种子结果见 metrics/movielens-100k-seeds42-44.json。原型由训练历史 farthest-first 初始化并做一次 assignment/update，固定为 4 个；未实现 MRLB、FlashSA 或线上 cache，且暂不登记不可执行的 evolve 标签。  long-sequence sketch-attention prototype-compression industrial-recommendation 搜广推 用户历史与排序骨干 SequenceO1 把远期历史压成固定 sketch 后，哪些成本变得可控，哪些仍会随历史变化？ 固定预算原型让后续候选匹配与 sketch 交互的规模不再随远期事件数直接增长，近期分支保留即时行为，STCA 再连接两种时间尺度。但读取历史、构造或更新 sketch 仍有成本，不能把端到端处理十万行为都称为常数时间。本地原型近似只验证预算化远期分支，不是完整工业注意力路径。 示意：十万条旧行为先压成几十个兴趣原型，每个候选只与这些原型匹配；新行为到来仍需更新摘要。像查一份定长索引很快，但建立与维护索引不是免费的。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-sequenceo1-53b97674" class="ar-learning-paper-anchor"></span>
<h2 id="qa-8c0f466df9e7082f">SequenceO1 把远期历史压成固定 sketch 后，哪些成本变得可控，哪些仍会随历史变化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asequenceo1">SequenceO1: End-to-End Ultra-Long (100K) Sequence Modeling in Recommendation with Low-Rank Caching</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定预算原型让后续候选匹配与 sketch 交互的规模不再随远期事件数直接增长，近期分支保留即时行为，STCA 再连接两种时间尺度。但读取历史、构造或更新 sketch 仍有成本，不能把端到端处理十万行为都称为常数时间。本地原型近似只验证预算化远期分支，不是完整工业注意力路径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>十万条旧行为先压成几十个兴趣原型，每个候选只与这些原型匹配；新行为到来仍需更新摘要。像查一份定长索引很快，但建立与维护索引不是免费的。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08443">原论文</a> · <a href="../../../../reproductions/2609.08443-sequenceo1/">实现解读</a> · <a href="#qa-8c0f466df9e7082f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rest" data-paper-title="From Language to Behavior: Scaling Sequence Transformers for Industrial Recommendation Ranking with Rec-Native Designs" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="From Language to Behavior: Scaling Sequence Transformers for Industrial Recommendation Ranking with Rec-Native Designs 搜广推与 LLM 应用 ByteDance 2026-09-01 ReST 不直接照搬语言 Transformer：双门控注意力抑制行为噪声，RoPE 与相对时间编码同时表达顺序和时间间隔；系统侧把一次请求拆成可复用的重型用户 encoder 与轻型候选 cross decoder，实现 compute-once、decode-many。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现双门控时序编码、重用户编码/轻候选交叉的计算路径。未复刻私有行为日志、生产 checkpoint 和 shared-prefix serving kernel；本实现仅声明 CPU 公共数据核心机制，不宣传 CUDA 路径。在 MovieLens 100K 固定 220 用户/360 物品协议上执行时序衰减、信号门控与候选交叉路径；三 seed 结果见 metrics/public-seeds42-44.json。  ranking-network long-sequence shared-prefix-serving 搜广推 用户历史与排序骨干 ReST 的 compute-once、decode-many 为什么需要区分重型用户编码和轻型候选交互？ 长历史的门控注意力与顺序、时间间隔建模是用户侧公共成本，先算一次可供同请求多个候选使用。候选 cross decoder 再按物品读取相关用户信息，保留候选相关交互而避免重复完整编码。双门控减少噪声，但共享只适用于不依赖候选的状态；历史改变或缓存版本变化时仍要更新。 示意：对同一用户评估两百部电影，先统一编码其观看历史与间隔，再让每部电影做轻量查询。不能把为某个候选专门计算的交互结果直接当成所有电影通用用户表示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-rest-5ed56a69" class="ar-learning-paper-anchor"></span>
<h2 id="qa-ffc3ae495ed6b99c">ReST 的 compute-once、decode-many 为什么需要区分重型用户编码和轻型候选交互？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arest">From Language to Behavior: Scaling Sequence Transformers for Industrial Recommendation Ranking with Rec-Native Designs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长历史的门控注意力与顺序、时间间隔建模是用户侧公共成本，先算一次可供同请求多个候选使用。候选 cross decoder 再按物品读取相关用户信息，保留候选相关交互而避免重复完整编码。双门控减少噪声，但共享只适用于不依赖候选的状态；历史改变或缓存版本变化时仍要更新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>对同一用户评估两百部电影，先统一编码其观看历史与间隔，再让每部电影做轻量查询。不能把为某个候选专门计算的交互结果直接当成所有电影通用用户表示。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.01240">原论文</a> · <a href="../../../../reproductions/2609.01240-rest/">实现解读</a> · <a href="#qa-ffc3ae495ed6b99c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onemodel" data-paper-title="OneModel: A Unified Foundation for Platform-Scale Multi-Scenario Ranking" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OneModel: A Unified Foundation for Platform-Scale Multi-Scenario Ranking 搜广推与 LLM 应用 Xiaohongshu 2026-08-19 推荐、广告和商家推荐通常各训一套排序模型，既重复消耗资源，也无法充分共享跨场景行为。OneModel 将异构特征先投影到统一 event token，再以共享 causal decoder 建模混合长历史；SAIM 用场景条件 gate 调制 FFN，分层表征同时保留全局 attentive pooling 与最近局部状态，从而兼顾迁移与专门化。 Fidelity: 核心机制复现。本地真实执行多场景统计、场景投影、SAIM 式门控和全局/局部分层表征；生产 Transformer 与私有特征未复刻。使用本地 MovieLens-1M 公开数据；没有小红书私有多流日志、action token、统一 Transformer decoder、训练早期梯度隔离、选择性反向传播和在线 serving。核心场景门控路径已执行，但本地指标只验证机制与失败边界。本地对照口径：基线为共享全局转移排序器；实验组加入由 MovieLens genre 派生的三个场景、场景转移、sigmoid 门控和 global/local 融合。  ranking multi-scenario foundation-model long-sequence 搜广推 用户历史与排序骨干 OneModel 已共享因果主干，SAIM 的场景 gate 还保留了什么专门化能力？ 异构事件先投影到统一空间，使不同业务能共享历史建模；但完全共用 FFN 容易把场景差异压平。SAIM 依据场景嵌入调制共享 FFN 的激活，让同一中间表示在不同任务里使用不同通道。全局聚合与最近局部状态再分别保留稳定偏好和即时变化，避免统一表示只剩一种时间尺度。 示意：用户既看旅游内容也买旅行用品。共享主干能理解这些行为相关，但广告场景和内容推荐场景用不同门控组合特征，近期订机票的信号也可通过局部状态保留。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-onemodel-224b06a8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-56f6b3788fa8c230">OneModel 已共享因果主干，SAIM 的场景 gate 还保留了什么专门化能力？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonemodel">OneModel: A Unified Foundation for Platform-Scale Multi-Scenario Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>异构事件先投影到统一空间，使不同业务能共享历史建模；但完全共用 FFN 容易把场景差异压平。SAIM 依据场景嵌入调制共享 FFN 的激活，让同一中间表示在不同任务里使用不同通道。全局聚合与最近局部状态再分别保留稳定偏好和即时变化，避免统一表示只剩一种时间尺度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户既看旅游内容也买旅行用品。共享主干能理解这些行为相关，但广告场景和内容推荐场景用不同门控组合特征，近期订机票的信号也可通过局部状态保留。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.18606">原论文</a> · <a href="../../../../reproductions/2608.18606-onemodel/">实现解读</a> · <a href="#qa-56f6b3788fa8c230">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:genrec-netflix" data-paper-title="GenRec: An LLM-Backed Recommendation Ranker at Netflix" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="GenRec: An LLM-Backed Recommendation Ranker at Netflix 搜广推与 LLM 应用 Netflix 2026-08-10 传统 Netflix 排序系统依赖大量人工特征、特征交互和场景专用网络。新增内容形态或推荐场景时，往往要重新设计特征、模型和基础设施。GenRec 把问题从“特征工程”转成“上下文工程”：把用户历史、内容元数据、设备和时间等信号表达成文本，让共享 LLM 主干学习语义与高阶交互。论文采用两阶段训练：Phase 1 在开源 LLM 上继续训练 Netflix 内容和用户数据，获得内部 foundation LLM； Fidelity：核心机制复现。本地真实加载 causal LLM、执行 LoRA Phase-2 后训练、文本化用户历史、全目录 catalog-aware ranking head、联合语言/排序目标和 reward-weighted loss；Netflix 私有 Phase-1 基座与线上 reward model 不可公开，未用固定规则冒充。Netflix 内部 Phase-1 foundation LLM、数千生产特征和数千亿交互事件不可获得；本地使用公开 SmolLM2 和 MovieLens 文本/反馈。  ranking llm-recommendation post-training reward-weighting context-engineering training-serving 搜广推 用户历史与排序骨干 Netflix GenRec使用decoder-only LLM，为什么线上却不逐token生成推荐清单？ 文本上下文经LLM前向得到用户表示后，catalog-aware head直接对目录物品评分，服务可以只做prefill，不必自回归写出商品名。这样既利用语义与高阶交互，又避免目录外生成和多步解码成本。联合语言目标服务表示学习，并不改变最终是目录排序；本地单种子路径不证明Netflix规模收益。 示意：模型读完用户历史和场景后，一次输出目录里每部电影的分数；它无需先写第一部片名，再把片名回填生成第二部，因此不会凭空推荐目录外作品。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-genrec-netflix-691b65fa" class="ar-learning-paper-anchor"></span>
<h2 id="qa-7c9e2f93989e3d7b">Netflix GenRec使用decoder-only LLM，为什么线上却不逐token生成推荐清单？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agenrec-netflix">GenRec: An LLM-Backed Recommendation Ranker at Netflix</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Netflix</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文本上下文经LLM前向得到用户表示后，catalog-aware head直接对目录物品评分，服务可以只做prefill，不必自回归写出商品名。这样既利用语义与高阶交互，又避免目录外生成和多步解码成本。联合语言目标服务表示学习，并不改变最终是目录排序；本地单种子路径不证明Netflix规模收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型读完用户历史和场景后，一次输出目录里每部电影的分数；它无需先写第一部片名，再把片名回填生成第二部，因此不会凭空推荐目录外作品。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.10257">原论文</a> · <a href="../../../../reproductions/2608.10257-genrec-netflix/">实现解读</a> · <a href="#qa-7c9e2f93989e3d7b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:inthq" data-paper-title="IntHQ: Task-Interactive Hierarchical Query on Dual-Stream Representations for Generative Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="IntHQ: Task-Interactive Hierarchical Query on Dual-Stream Representations for Generative Recommendation 搜广推与 LLM 应用 Amap / Alibaba 2026-08-10 双流分别保留行为与上下文表示，when/where/how/via 四个任务查询在多个层级交互检索，使任务信号进入编码器而非只留在任务头。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  multi-task-learning generative-recommendation long-sequence 搜广推 用户历史与排序骨干 IntHQ让when、where、how、via查询进入多层编码，而不只加四个输出头，有何作用？ 仅在末端分头预测，早期编码仍可能按同一种方式压缩所有信息。任务查询在不同层级读取行为与上下文双流，让任务需求参与选择证据，例如时间问题关注周期、渠道问题关注入口。共享底层仍可保留共性，但这种互动不意味着任务冲突自动消失，需要检查各查询是否产生真实分工。 示意：同一条午间搜索记录，时间查询关心午休周期，渠道查询关心搜索入口；让两种问题在编码中取证，比最后对同一摘要各接一层分类头更灵活。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-inthq-fbf3d84e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-787bc07ff99b39ff">IntHQ让when、where、how、via查询进入多层编码，而不只加四个输出头，有何作用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ainthq">IntHQ: Task-Interactive Hierarchical Query on Dual-Stream Representations for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Amap / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>仅在末端分头预测，早期编码仍可能按同一种方式压缩所有信息。任务查询在不同层级读取行为与上下文双流，让任务需求参与选择证据，例如时间问题关注周期、渠道问题关注入口。共享底层仍可保留共性，但这种互动不意味着任务冲突自动消失，需要检查各查询是否产生真实分工。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一条午间搜索记录，时间查询关心午休周期，渠道查询关心搜索入口；让两种问题在编码中取证，比最后对同一摘要各接一层分类头更灵活。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.09634">原论文</a> · <a href="../../../../reproductions/2608.09634-inthq/">实现解读</a> · <a href="#qa-787bc07ff99b39ff">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tm20k" data-paper-title="Teacher Retains Full Tokens, Student Merges Efficiently: TM20K for E-Commerce Sequence Modeling in Ad Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Teacher Retains Full Tokens, Student Merges Efficiently: TM20K for E-Commerce Sequence Modeling in Ad Recommendation 搜广推与 LLM 应用 ByteDance 2026-08-07 教师网络保留完整行为 token 提供细粒度监督，学生把连续行为按组以 sum/√n 合并到固定 token 预算，再蒸馏教师注意力与排序分布，兼顾长序列信息和线上成本。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为无蒸馏的合并 token student，实验组从 full-token teacher 蒸馏；seed 42 的 NDCG@10 为 0.04022，基线为 0.03446。  advertising long-sequence token-merging distillation 搜广推 用户历史与排序骨干 TM20K 为什么把一组行为按 sum/√n 合并，并蒸馏完整 token teacher？ 分组合并把序列压到固定 token 预算，除以组大小平方根可缓和求和随组长增长的尺度变化，相较均值保留另一种组规模信息。完整教师仍能看到细粒度行为，注意力与排序蒸馏帮助压缩学生补回仅靠聚合易丢的关系。聚合不可逆，蒸馏只能学习有用近似，不能保证还原组内每次行为。 示意：四次相关浏览合为一个 token，按平方根缩放避免数值随组长直接翻倍。教师能区分四次内部关系，再把软信号传给压缩学生，但学生不再拥有原始四个位置。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-tm20k-e967dab7" class="ar-learning-paper-anchor"></span>
<h2 id="qa-74a2478da4c70ed5">TM20K 为什么把一组行为按 sum/√n 合并，并蒸馏完整 token teacher？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atm20k">Teacher Retains Full Tokens, Student Merges Efficiently: TM20K for E-Commerce Sequence Modeling in Ad Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分组合并把序列压到固定 token 预算，除以组大小平方根可缓和求和随组长增长的尺度变化，相较均值保留另一种组规模信息。完整教师仍能看到细粒度行为，注意力与排序蒸馏帮助压缩学生补回仅靠聚合易丢的关系。聚合不可逆，蒸馏只能学习有用近似，不能保证还原组内每次行为。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>四次相关浏览合为一个 token，按平方根缩放避免数值随组长直接翻倍。教师能区分四次内部关系，再把软信号传给压缩学生，但学生不再拥有原始四个位置。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.07055">原论文</a> · <a href="../../../../reproductions/2608.07055-tm20k/">实现解读</a> · <a href="#qa-74a2478da4c70ed5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:transx" data-paper-title="TransX: Scaling Transformer-based Recommendation via Behavioral and Serving Stream Crossings" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TransX: Scaling Transformer-based Recommendation via Behavioral and Serving Stream Crossings 搜广推与 LLM 应用 LinkedIn 2026-07-31 将可离线缓存的长行为流与请求时产生的短服务流解耦；行为端形成 global/local 缓存，候选端只对缓存做 cross-attention，从而避免每个请求重算完整 self-attention。 成本过高，不复现（审查 DONE）：报告的 32 H200、约 13 小时收敛、生产 Kafka/KV/多租户服务和完整多基准实验不在本批预算内。它们是公式/梯度诊断，不是新的推荐得分；历史 adapter：concept demo。model.py 的 NumPy 路径使用固定权重与既有特征，没有训练论文网络；历史结果原样保留，但不再标成核心模型训练或正式能力比较。下文另列本次技术报告的真实可微组件及独立验收证据。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；  ranking long-sequence cross-attention serving 搜广推 用户历史与排序骨干 TransX 为什么把行为流缓存为 global/local 两种状态，而让短服务流只做 cross-attention？ 长行为流在多个请求间变化较慢，离线或异步形成缓存能摊销自注意力成本；global 保存整体偏好，local 保留近期细节，服务流再用当前候选查询它们。每次请求省掉的是重复行为编码，缓存构建与更新仍有成本，也必须避免把候选相关状态误缓存成公共用户信息。 示意：用户一天内多次打开推荐，长期兴趣缓存可复用，局部缓存随新行为刷新。某次候选只读取需要的片段，不必为了这一件商品把整段多年历史重新自注意力一次。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-transx-58683026" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f63260b88299146b">TransX 为什么把行为流缓存为 global/local 两种状态，而让短服务流只做 cross-attention？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atransx">TransX: Scaling Transformer-based Recommendation via Behavioral and Serving Stream Crossings</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长行为流在多个请求间变化较慢，离线或异步形成缓存能摊销自注意力成本；global 保存整体偏好，local 保留近期细节，服务流再用当前候选查询它们。每次请求省掉的是重复行为编码，缓存构建与更新仍有成本，也必须避免把候选相关状态误缓存成公共用户信息。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户一天内多次打开推荐，长期兴趣缓存可复用，局部缓存随新行为刷新。某次候选只读取需要的片段，不必为了这一件商品把整段多年历史重新自注意力一次。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28940">原论文</a> · <a href="../../../../reproductions/2607.28940-transx/">实现解读</a> · <a href="#qa-f63260b88299146b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ccformer" data-paper-title="CCFormer: Efficient Cross-Field Interaction and Hierarchical Sequence Compression for Industrial Recommendation at Tencent" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="CCFormer: Efficient Cross-Field Interaction and Hierarchical Sequence Compression for Industrial Recommendation at Tencent 搜广推与 LLM 应用 Tencent Platform and Content Group 2026-07-30 工业排序既要细粒度字段交互，又要吃进千长度行为序列。CCFormer 让 ID、内容等字段先分离投影再 cross attention，并用逐层扩大感受野的 token mixing 压缩旧历史，近期行为保持细粒度。 Fidelity: 核心机制复现。实现跨字段门控、分层旧序列压缩和 recent-token 保留；不复刻腾讯私有数据与 kernel。未包含 40 亿私有样本、千长度线上序列、并行多 target kernel；本地结果只验证机制方向。本地对照口径：基线为同预算 GRU；实验组为 CCFormer core，相对基线 NDCG@10 +22.44%。  ranking long-sequence sequence-compression token-mixing 搜广推 用户历史与排序骨干 CCFormer为什么让远期历史逐层扩大压缩感受野，却保留近期行为细节？ 远期行为数量大，逐条高成本交互会挤占排序预算；近期行为更可能包含当前意图变化，过早合并容易损失精细差异。CCFormer用层次token mixing压缩旧历史，同时对不同字段保留分离投影与cross-attention。压缩和字段交互各解决不同瓶颈，不能只用更短序列长度评价模型是否有效。 示意：上个月反复浏览的同类商品可逐步合并，刚刚连续查看的两个不同尺码则应保留；候选相关字段还能从压缩历史中读到长期偏好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-ccformer-b04b720c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-16b5de07814be92e">CCFormer为什么让远期历史逐层扩大压缩感受野，却保留近期行为细节？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Accformer">CCFormer: Efficient Cross-Field Interaction and Hierarchical Sequence Compression for Industrial Recommendation at Tencent</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent Platform and Content Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>远期行为数量大，逐条高成本交互会挤占排序预算；近期行为更可能包含当前意图变化，过早合并容易损失精细差异。CCFormer用层次token mixing压缩旧历史，同时对不同字段保留分离投影与cross-attention。压缩和字段交互各解决不同瓶颈，不能只用更短序列长度评价模型是否有效。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>上个月反复浏览的同类商品可逐步合并，刚刚连续查看的两个不同尺码则应保留；候选相关字段还能从压缩历史中读到长期偏好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28070">原论文</a> · <a href="../../../../reproductions/2607.28070-ccformer/">实现解读</a> · <a href="#qa-16b5de07814be92e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ha-moe" data-paper-title="Heterogeneous Ranking in Industrial-Scale Recommender Systems: A Case Study" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Heterogeneous Ranking in Industrial-Scale Recommender Systems: A Case Study 搜广推与 LLM 应用 Google / Discover 2026-07-30 Discover 要在同一 feed 中比较新闻、视频、体育等开放网页内容，单一共享塔会让高频内容支配梯度。HA-MoE 用内容异构性特征控制 multi-gate MoE，把通用信号与领域专长分开；LENS 则追踪 expert 使用率和分领域 DL-AUC，避免总体指标掩盖局部退化。 Fidelity: 核心机制复现。本地执行异构性度量、专长 expert 与多门控融合，不把 MovieLens 代理实验写成 Google Discover 生产复刻。MovieLens genre 代理开放网页内容类型；未复刻 Discover 私有样本、LENS 生产观测系统和 DL-AUC 服务。本地对照口径：基线为同切分的 homogeneous transition-content ranker，实验组加入 HA-MoE；NDCG@10 相对 -1.77%。  ranking mixture-of-experts heterogeneity diversity 搜广推 用户历史与排序骨干 HA-MoE为什么用内容异构性控制专家，还要按领域监测DL-AUC？ 同一feed混合新闻、视频与体育时，高频领域可能支配共享梯度。异构性门控让不同样本借用不同专家组合，保留通用能力与领域专长；分领域监测检查专家利用率和局部质量，防止总体平均掩盖小领域退化。专家多不代表真正分工，必须同时看路由和切片结果。 示意：新闻流量占多数时，总体分数上涨可能盖住体育视频下降；领域感知路由可分配专长，但只有分领域评价才能发现这种被平均数隐藏的损伤。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-ha-moe-beffade8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-dda89f7194e99a78">HA-MoE为什么用内容异构性控制专家，还要按领域监测DL-AUC？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aha-moe">Heterogeneous Ranking in Industrial-Scale Recommender Systems: A Case Study</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / Discover</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一feed混合新闻、视频与体育时，高频领域可能支配共享梯度。异构性门控让不同样本借用不同专家组合，保留通用能力与领域专长；分领域监测检查专家利用率和局部质量，防止总体平均掩盖小领域退化。专家多不代表真正分工，必须同时看路由和切片结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新闻流量占多数时，总体分数上涨可能盖住体育视频下降；领域感知路由可分配专长，但只有分领域评价才能发现这种被平均数隐藏的损伤。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27577">原论文</a> · <a href="../../../../reproductions/2607.27577-ha-moe/">实现解读</a> · <a href="#qa-dda89f7194e99a78">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:clockrope" data-paper-title="ClockRoPE: Random Fourier Rotations for Temporal Routine Modeling" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="ClockRoPE: Random Fourier Rotations for Temporal Routine Modeling 搜广推与 LLM 应用 YouTube / Google DeepMind 2026-07-29 普通 RoPE 的对数线性频率偏向“距离越远相关性越弱”，但推荐行为常有日周期和周周期。ClockRoPE 从目标周期 kernel 的 Fourier 变换中采样旋转频率，使 query-key 点积在相同小时或星期附近重新增强，并可与标准 RoPE 各占一半通道。 Fidelity: 核心机制复现。本地执行周期 Gaussian Fourier kernel 对序列注意力的调制；公开数据缺少 YouTube 的小时级行为语境，因此结果只验证机制和边界。公开 MovieLens 只提供稀疏评分时间，本地用确定性事件间隔构造周期位置；未复刻 YouTube 私有日志、生成式检索模型、TPU kernel 和线上 serving。本地对照口径：基线为不使用周期调制的 RoPE-style recency ranker；实验组加入日/周 ClockRoPE kernel，NDCG@10 相对 -2.30%。  generative-retrieval temporal-modeling rope long-sequence 搜广推 用户历史与排序骨干 为什么ClockRoPE会让相隔一周的行为，比相隔两天的行为更相关？ 许多消费习惯具有周期，相关性并不随时间距离单调减弱。ClockRoPE按目标周期kernel的频谱采样旋转频率，使query-key点积在相同小时或星期附近重新增强；还可与普通RoPE分担通道，保留近期信号。周期编码提供归纳偏置，不意味着每位用户都存在同样稳定的周规律。 示意：周一早晨的通勤新闻可能与上周一早晨更接近，而非周六深夜的娱乐视频；周期旋转允许表达这种回归，同时仍可保留普通近期偏好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-clockrope-0d0da402" class="ar-learning-paper-anchor"></span>
<h2 id="qa-4dacd6aabb5cf7c7">为什么ClockRoPE会让相隔一周的行为，比相隔两天的行为更相关？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aclockrope">ClockRoPE: Random Fourier Rotations for Temporal Routine Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · YouTube / Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>许多消费习惯具有周期，相关性并不随时间距离单调减弱。ClockRoPE按目标周期kernel的频谱采样旋转频率，使query-key点积在相同小时或星期附近重新增强；还可与普通RoPE分担通道，保留近期信号。周期编码提供归纳偏置，不意味着每位用户都存在同样稳定的周规律。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>周一早晨的通勤新闻可能与上周一早晨更接近，而非周六深夜的娱乐视频；周期旋转允许表达这种回归，同时仍可保留普通近期偏好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26369">原论文</a> · <a href="../../../../reproductions/2607.26369-clockrope/">实现解读</a> · <a href="#qa-4dacd6aabb5cf7c7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:specformer" data-paper-title="SpecFormer: Mitigating Embedding and Attention Collapse via Spectral-Aware Transformer for Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="SpecFormer: Mitigating Embedding and Attention Collapse via Spectral-Aware Transformer for Recommendation 搜广推与 LLM 应用 Zhejiang University 2026-07-27 以奇异值谱软化和谱残差位置编码，抑制推荐 Transformer 的 embedding/attention collapse。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 SpecFormer 为 0.04999，相对变化 -7.44%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  ranking transformer spectral-softening 搜广推 用户历史与排序骨干 SpecFormer 的奇异值谱软化为什么有助于对抗表示坍缩？ 表示若被少数巨大奇异值主导，很多 token 会挤在近似同一低维方向，深层交互难增加信息。对谱做软化缩小强弱方向差距，谱残差位置编码再给注意力额外结构信号，意在保留更丰富的方向。它不是让所有方向等权的无损变换，弱方向可能也含噪声，效果仍需任务证据。 示意：一组向量几乎全沿“热门程度”方向变化，主题差别被淹没。压低最强方向的相对支配后，题材等较弱方向更可能被模型利用，但也要防止放大随机噪声。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-specformer-bc626a07" class="ar-learning-paper-anchor"></span>
<h2 id="qa-2c07d9b7ab232c29">SpecFormer 的奇异值谱软化为什么有助于对抗表示坍缩？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aspecformer">SpecFormer: Mitigating Embedding and Attention Collapse via Spectral-Aware Transformer for Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>表示若被少数巨大奇异值主导，很多 token 会挤在近似同一低维方向，深层交互难增加信息。对谱做软化缩小强弱方向差距，谱残差位置编码再给注意力额外结构信号，意在保留更丰富的方向。它不是让所有方向等权的无损变换，弱方向可能也含噪声，效果仍需任务证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一组向量几乎全沿“热门程度”方向变化，主题差别被淹没。压低最强方向的相对支配后，题材等较弱方向更可能被模型利用，但也要防止放大随机噪声。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24025">原论文</a> · <a href="../../../../reproductions/2607.24025-specformer/">实现解读</a> · <a href="#qa-2c07d9b7ab232c29">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:whale" data-paper-title="WHALE: A Scalable Unified Model for Recommendation with Wukong-HSTU Architecture" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="WHALE: A Scalable Unified Model for Recommendation with Wukong-HSTU Architecture 搜广推与 LLM 应用 Meta Platforms, Inc. 2026-07-19 工业推荐通常把稀疏特征交互和用户行为序列分成两个模型，扩展规模时容易形成表示与算力割裂。WHALE 用 Wukong 分支递归建模高阶特征交互，用 HSTU 分支建模行为序列，并在每层用 cross-attention 双向交换状态，形成可共同扩展的统一网络。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练 Wukong、HSTU 与逐层交换；Meta 私有特征规模和生产内核未复刻。本地实际训练 Wukong 乘性交互、门控因果 HSTU 和逐层 cross-branch attention，并以同维度、同层数的 late-fusion Transformer 为直接对照。  ranking hstu feature-interaction scaling 搜广推 用户历史与排序骨干 WHALE 为什么让 Wukong 与 HSTU 每层双向交换状态，而不是各自编码后只在末端融合？ 特征交互分支擅长高阶字段组合，序列分支擅长行为演化，末端融合只能组合两份已完成的表示。逐层 cross-attention 让字段关系影响后续历史解释，也让行为状态改变后续特征交互，从而联合扩容。双向交流增加计算与依赖，不同于纯用户缓存结构；本地比较也只支持公开缩比任务。 示意：场景字段显示周末出游，序列分支据此关注近期露营行为；更新后的兴趣再影响价格与品类交叉。若只末端拼接，两条分支在此前多层都无法互相调整。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-whale-9ea1c28b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-0dbf74a57516dd91">WHALE 为什么让 Wukong 与 HSTU 每层双向交换状态，而不是各自编码后只在末端融合？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Awhale">WHALE: A Scalable Unified Model for Recommendation with Wukong-HSTU Architecture</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Platforms, Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>特征交互分支擅长高阶字段组合，序列分支擅长行为演化，末端融合只能组合两份已完成的表示。逐层 cross-attention 让字段关系影响后续历史解释，也让行为状态改变后续特征交互，从而联合扩容。双向交流增加计算与依赖，不同于纯用户缓存结构；本地比较也只支持公开缩比任务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>场景字段显示周末出游，序列分支据此关注近期露营行为；更新后的兴趣再影响价格与品类交叉。若只末端拼接，两条分支在此前多层都无法互相调整。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.17017">原论文</a> · <a href="../../../../reproductions/2607.17017-whale/">实现解读</a> · <a href="#qa-0dbf74a57516dd91">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:long-history-transformer" data-paper-title="Long-History User Transformers for Real-Time Ad Ranking" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Long-History User Transformers for Real-Time Ad Ranking 搜广推与 LLM 应用 Yandex 2026-07-15 广告排序需要长历史，但请求时重算完整序列会增加延迟。论文把系统拆成异步 full-history Transformer 和在线 lightweight Transformer：离线部分周期性刷新固定维度用户状态，在线只编码最近事件并读取缓存；训练先用 next-event 与 feedback 辅助任务预训练，再针对目标广告 surface 微调。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练离线缓存与在线近期双 encoder；Yandex 生产特征系统未复刻。代码实际训练 24 步长的离线历史 encoder、32 维缓存、仅查看最近 4 个事件的在线 encoder，以及 next-item/feedback 辅助目标；基线只能在请求时查看最近 4 个事件。  advertising long-sequence cached-user-representation serving 搜广推 用户历史与排序骨干 异步长历史模型已有缓存，在线轻量Transformer为什么还要保留最近事件？ 长历史缓存覆盖稳定模式，但刷新有延迟，新发生的行为可能尚未进入。在线模型读取短窗口并结合缓存，补足实时变化，避免每个请求重算完整历史。训练辅助目标还让两部分学习可用表示；缓存尺寸小并不意味着没有压缩损失，也不能把离线新鲜状态与线上旧缓存混用评估。 示意：昨夜缓存记录用户爱摄影，今天突然连续搜索育儿用品；在线最近事件能反映新需求，不必等待下一轮长历史刷新，也不必重新编码全部旧记录。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-long-history-transformer-f4293ee0" class="ar-learning-paper-anchor"></span>
<h2 id="qa-269d7fd18f895962">异步长历史模型已有缓存，在线轻量Transformer为什么还要保留最近事件？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Along-history-transformer">Long-History User Transformers for Real-Time Ad Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Yandex</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长历史缓存覆盖稳定模式，但刷新有延迟，新发生的行为可能尚未进入。在线模型读取短窗口并结合缓存，补足实时变化，避免每个请求重算完整历史。训练辅助目标还让两部分学习可用表示；缓存尺寸小并不意味着没有压缩损失，也不能把离线新鲜状态与线上旧缓存混用评估。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>昨夜缓存记录用户爱摄影，今天突然连续搜索育儿用品；在线最近事件能反映新需求，不必等待下一轮长历史刷新，也不必重新编码全部旧记录。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14331">原论文</a> · <a href="../../../../reproductions/2607.14331-long-history-transformer/">实现解读</a> · <a href="#qa-269d7fd18f895962">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tmallgs" data-paper-title="TMallGS: Scaling Unified Feature and Sequence Modeling for Generative E-commerce Search" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TMallGS: Scaling Unified Feature and Sequence Modeling for Generative E-commerce Search 搜广推与 LLM 应用 Taobao &amp; Tmall Group of Alibaba 2026-07-15 电商搜索同时包含 query、短期/长期行为、用户和商品等异构字段，直接拼 token 会放大字段噪声。TMallGS 为不同字段学习独立 Q/K/V，用 distribution-calibrated saliency 和 noise-adaptive gate 控制交互；内容特征通过 FiLM 注入，context bias 修正最终分数，并用中间层误差自适应分配 progressive supervision。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练 field-adaptive 交互和 progressive loss；天猫私有字段与生产规模未复刻。本地把 MovieLens 类型和序列映射为异构字段，真实训练 field-wise QKV、噪声门控、显式内容 FiLM、context bias 和 error-aware progressive loss。  search-ranking transformer scaling feature-interaction 搜广推 用户历史与排序骨干 TMallGS 为什么为字段独立学习 Q/K/V，还要叠加噪声 gate 与逐层监督？ 查询、历史、用户和商品字段分布不同，共用一套投影可能混淆它们的含义。字段专属投影先建立适合的交互空间，显著性校准与噪声门控再控制哪些交互值得保留；FiLM 注入内容，逐层损失按中间误差分配训练信号。多个环节分别处理异构性、噪声和深层学习，不能只归因于增加注意力头数。 示意：一次偶然点击不应像明确搜索词一样强烈影响商品排序。字段投影区分两者，门控降低噪声历史贡献，中间层监督再帮助模型逐步学到更稳定的相关性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-tmallgs-f2b12094" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d7c6269d0941de88">TMallGS 为什么为字段独立学习 Q/K/V，还要叠加噪声 gate 与逐层监督？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atmallgs">TMallGS: Scaling Unified Feature and Sequence Modeling for Generative E-commerce Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group of Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>查询、历史、用户和商品字段分布不同，共用一套投影可能混淆它们的含义。字段专属投影先建立适合的交互空间，显著性校准与噪声门控再控制哪些交互值得保留；FiLM 注入内容，逐层损失按中间误差分配训练信号。多个环节分别处理异构性、噪声和深层学习，不能只归因于增加注意力头数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次偶然点击不应像明确搜索词一样强烈影响商品排序。字段投影区分两者，门控降低噪声历史贡献，中间层监督再帮助模型逐步学到更稳定的相关性。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.13398">原论文</a> · <a href="../../../../reproductions/2607.13398-tmallgs/">实现解读</a> · <a href="#qa-d7c6269d0941de88">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:nontp" data-paper-title="Not Only NTP: Extending Training Signal Coverage for Generative Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Not Only NTP: Extending Training Signal Coverage for Generative Recommendation 搜广推与 LLM 应用 Meituan 2026-07-14 标准 next-token prediction 只要求当前位置预测紧邻的下一个物品：它既没有监督 hidden state 理解更远的未来轨迹，也没有让跨业务上下文直接更新稀疏域目标物品。NONTP 将前者称为 temporal locality，后者称为 spatial locality。TCL 用在线 backbone 的第个状态预测 EMA teacher 的第个未来状态，并只把其他用户序列作为负例； Fidelity: 核心机制复现。本地真实执行 NTP、EMA teacher、三个未来步 predictor、跨序列 InfoNCE、跨域 hidden-state pooling 与共享预测头；训练辅助分支在推理时全部移除。保留论文、、和两个辅助损失权重 0.1。本地对照口径：基线是相同 causal backbone、相同初始化和训练预算的 ntp；实验组是同时加入 TCL 与 TDL 的 nontp。三随机种子下 Hit@10 从 0.05079 降到 0.04828（-4.93%），NDCG@10 从 0.02431 降到 0.02222（-8.62%）。  generative-recommendation contrastive-learning multi-domain 搜广推 用户历史与排序骨干 NONTP 的 TCL 与 TDL 分别补足 next-token prediction 的哪两种局部性？ TCL 让当前状态预测 EMA 教师的较远未来状态，补上只监督紧邻下一步的时间局部性；TDL 用目标之前的异域状态经共享物品头预测目标，让稀疏域获得跨域信号。两项只在训练时使用，推理仍走原主干。未来状态是训练监督而非上线输入，不能把这种训练方式理解为允许推理读取未来。 示意：用户先看家居内容再购买灯具。TCL 训练早期状态理解更远的轨迹，TDL 让购买前的异域浏览也参与预测灯具；真实请求时仍只能读取已经发生的行为。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-nontp-bd610948" class="ar-learning-paper-anchor"></span>
<h2 id="qa-0d443595c80ba49d">NONTP 的 TCL 与 TDL 分别补足 next-token prediction 的哪两种局部性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Anontp">Not Only NTP: Extending Training Signal Coverage for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>TCL 让当前状态预测 EMA 教师的较远未来状态，补上只监督紧邻下一步的时间局部性；TDL 用目标之前的异域状态经共享物品头预测目标，让稀疏域获得跨域信号。两项只在训练时使用，推理仍走原主干。未来状态是训练监督而非上线输入，不能把这种训练方式理解为允许推理读取未来。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户先看家居内容再购买灯具。TCL 训练早期状态理解更远的轨迹，TDL 让购买前的异域浏览也参与预测灯具；真实请求时仍只能读取已经发生的行为。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12277">原论文</a> · <a href="../../../../reproductions/2607.12277-nontp/">实现解读</a> · <a href="#qa-0d443595c80ba49d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sam" data-paper-title="Learning to Forget: Satiation-Aware Long-Sequence Transducers for Mitigating Post-Purchase Redundancy" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Learning to Forget: Satiation-Aware Long-Sequence Transducers for Mitigating Post-Purchase Redundancy 搜广推与 LLM 应用 Alibaba Group 2026-07-14 购买完成的是一簇意图，继续放大购买前点击会制造重复推荐。SAM 用 pointwise cross-attention 定位要压制的历史节点，并从长期购买序列预测补货节奏；ASGU 在刚购买时强抑制、接近周期时逐渐恢复，再以 log-mask 修改注意力 logits。 Fidelity: 核心机制复现。双路径 intent/rhythm、ASGU、log-mask intervention 与 TTNP 周期监督均实际执行。没有真实补货型商品和 censored purchase log；只验证机制和失败边界。本地对照口径：基线是 DIN-like interest score；实验组 SAM 加入按 genre 学习的周期与 ASGU，相对基线 Hit@10 -12.50%、NDCG@10 -6.60%。  ranking long-sequence satiation 搜广推 用户历史与排序骨干 SAM 为什么购买后先压制相关历史，再随补货周期逐渐恢复注意力？ 购买常意味着一个需求已经完成，继续照抄购买前点击会导致重复推荐。SAM 先定位属于同一已完成意图的历史节点，再依据长期购买节奏估计周期，用时间门控和 log-mask 压低注意力，接近补货时间时逐渐解除。它区分需求完成与永久厌恶；本地用评分代理购买事件，不能验证真实补货规律。 示意：刚买大包装洗衣液时减少同类推荐，几周后按个人使用节奏逐步恢复；若永久删掉这类兴趣会错过补货，完全不抑制又会立刻重复展示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-sam-b9df9dfc" class="ar-learning-paper-anchor"></span>
<h2 id="qa-90747e26d9c7c6ae">SAM 为什么购买后先压制相关历史，再随补货周期逐渐恢复注意力？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asam">Learning to Forget: Satiation-Aware Long-Sequence Transducers for Mitigating Post-Purchase Redundancy</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>购买常意味着一个需求已经完成，继续照抄购买前点击会导致重复推荐。SAM 先定位属于同一已完成意图的历史节点，再依据长期购买节奏估计周期，用时间门控和 log-mask 压低注意力，接近补货时间时逐渐解除。它区分需求完成与永久厌恶；本地用评分代理购买事件，不能验证真实补货规律。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>刚买大包装洗衣液时减少同类推荐，几周后按个人使用节奏逐步恢复；若永久删掉这类兴趣会错过补货，完全不抑制又会立刻重复展示。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12714">原论文</a> · <a href="../../../../reproductions/2607.12714-sam/">实现解读</a> · <a href="#qa-90747e26d9c7c6ae">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:slimper" data-paper-title="SlimPer: Make Personalization Model Slim and Smart" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="SlimPer: Make Personalization Model Slim and Smart 搜广推与 LLM 应用 Meta Platforms, Inc. 2026-07-14 SlimPer 每层用固定槽位的 user-item 知识库查询用户 token 池，执行 Select–Match–Refine。用户池保持可读，精炼层之间只传播小知识库；输入编码仍可带局部上下文。 本地只在短历史 MovieLens 上验证缩小机制；NDCG@10 +1.29% 仅为 seed 42 的 smoke，未实测生产 QPS 或显存。ROO 共享用户编码，候选相关知识库仍逐候选更新。 为什么用户 tokens 能共享，但 knowledge base 的更新结果不能全部共享？ ranking long-sequence serving-efficiency 搜广推 用户历史与排序骨干 SlimPer每层都读取长历史，为什么还能只保留固定大小的knowledge base？ 被反复更新的是少量候选相关知识槽，而原始用户token作为只读证据被重新访问。Select取出相关证据，Match与知识模板显式比较，Refine再更新槽位；层间无需传播全部历史隐藏状态。共享的是用户编码，候选相关knowledge base仍分别演化，并不是所有候选共用一个最终兴趣向量。 示意：同一份购买记录可供鞋和相机两个候选共读，但两组小知识槽分别整理尺寸需求和摄影兴趣，不能把鞋候选更新过的槽直接给相机。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-slimper-ce7fc963" class="ar-learning-paper-anchor"></span>
<h2 id="qa-4a13e5753d9c783b">SlimPer每层都读取长历史，为什么还能只保留固定大小的knowledge base？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aslimper">SlimPer: Make Personalization Model Slim and Smart</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Platforms, Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>被反复更新的是少量候选相关知识槽，而原始用户token作为只读证据被重新访问。Select取出相关证据，Match与知识模板显式比较，Refine再更新槽位；层间无需传播全部历史隐藏状态。共享的是用户编码，候选相关knowledge base仍分别演化，并不是所有候选共用一个最终兴趣向量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一份购买记录可供鞋和相机两个候选共读，但两组小知识槽分别整理尺寸需求和摄影兴趣，不能把鞋候选更新过的槽直接给相机。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12281">原论文</a> · <a href="../../../../reproductions/2607.12281-slimper/">实现解读</a> · <a href="../../../001-hstu-longer-slimper/">阅读精选对比</a> · <a href="#qa-4a13e5753d9c783b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:slimper" data-paper-title="SlimPer: Make Personalization Model Slim and Smart" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="SlimPer: Make Personalization Model Slim and Smart 搜广推与 LLM 应用 Meta Platforms, Inc. 2026-07-14 SlimPer 每层用固定槽位的 user-item 知识库查询用户 token 池，执行 Select–Match–Refine。用户池保持可读，精炼层之间只传播小知识库；输入编码仍可带局部上下文。 本地只在短历史 MovieLens 上验证缩小机制；NDCG@10 +1.29% 仅为 seed 42 的 smoke，未实测生产 QPS 或显存。ROO 共享用户编码，候选相关知识库仍逐候选更新。 为什么用户 tokens 能共享，但 knowledge base 的更新结果不能全部共享？ ranking long-sequence serving-efficiency 搜广推 用户历史与排序骨干 SlimPer 已经用 attention 选取证据，为什么还要与 knowledge templates 显式点积匹配？ Select 用当前知识库生成查询，得到少量被聚合的用户证据，回答“该取哪些信息”；Match 再把这些证据与同一知识库生成的多个模板比较，形成查询数乘模板数的相关性矩阵。Refine 利用这些显式关系更新知识，而非把聚合向量直接当最终兴趣。两步把证据检索与多方面相关性判断分开。 示意：面对跑鞋候选，Select 找到用户跑步距离与尺码相关行为；Match 再分别比较舒适度、用途等模板，更新知识槽。找到证据不等于已经判断它支持候选的哪个方面。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="qa-c8469615c85e200f">SlimPer 已经用 attention 选取证据，为什么还要与 knowledge templates 显式点积匹配？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aslimper">SlimPer: Make Personalization Model Slim and Smart</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Platforms, Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Select 用当前知识库生成查询，得到少量被聚合的用户证据，回答“该取哪些信息”；Match 再把这些证据与同一知识库生成的多个模板比较，形成查询数乘模板数的相关性矩阵。Refine 利用这些显式关系更新知识，而非把聚合向量直接当最终兴趣。两步把证据检索与多方面相关性判断分开。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>面对跑鞋候选，Select 找到用户跑步距离与尺码相关行为；Match 再分别比较舒适度、用途等模板，更新知识槽。找到证据不等于已经判断它支持候选的哪个方面。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12281">原论文</a> · <a href="../../../../reproductions/2607.12281-slimper/">实现解读</a> · <a href="../../../001-hstu-longer-slimper/">阅读精选对比</a> · <a href="#qa-c8469615c85e200f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:slimper" data-paper-title="SlimPer: Make Personalization Model Slim and Smart" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="SlimPer: Make Personalization Model Slim and Smart 搜广推与 LLM 应用 Meta Platforms, Inc. 2026-07-14 SlimPer 每层用固定槽位的 user-item 知识库查询用户 token 池，执行 Select–Match–Refine。用户池保持可读，精炼层之间只传播小知识库；输入编码仍可带局部上下文。 本地只在短历史 MovieLens 上验证缩小机制；NDCG@10 +1.29% 仅为 seed 42 的 smoke，未实测生产 QPS 或显存。ROO 共享用户编码，候选相关知识库仍逐候选更新。 为什么用户 tokens 能共享，但 knowledge base 的更新结果不能全部共享？ ranking long-sequence serving-efficiency 搜广推 用户历史与排序骨干 SlimPer 不逐层更新全历史，是否意味着它完全不建模相邻行为之间的关系？ 不是。原文§2.5在事件 token 化时加入局部上下文编码，可用卷积或滑窗注意力融合邻近行为；后续层才反复读取这些用户 token 并更新固定知识库。因此它减少的是深层全量两两历史交互，而非禁止任何历史关系。固定知识槽也只是中间状态预算，原始输入存储与每层读取仍随历史长度增长。 示意：连续搜索、比较、加购可先编码成带局部背景的事件，再由多层知识槽按候选读取。虽然每层不重写整条历史，这些事件也不必被当成彼此孤立的点击。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="qa-c31fdda2ede9afd6">SlimPer 不逐层更新全历史，是否意味着它完全不建模相邻行为之间的关系？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aslimper">SlimPer: Make Personalization Model Slim and Smart</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Platforms, Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。原文§2.5在事件 token 化时加入局部上下文编码，可用卷积或滑窗注意力融合邻近行为；后续层才反复读取这些用户 token 并更新固定知识库。因此它减少的是深层全量两两历史交互，而非禁止任何历史关系。固定知识槽也只是中间状态预算，原始输入存储与每层读取仍随历史长度增长。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>连续搜索、比较、加购可先编码成带局部背景的事件，再由多层知识槽按候选读取。虽然每层不重写整条历史，这些事件也不必被当成彼此孤立的点击。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12281">原论文</a> · <a href="../../../../reproductions/2607.12281-slimper/">实现解读</a> · <a href="../../../001-hstu-longer-slimper/">阅读精选对比</a> · <a href="#qa-c31fdda2ede9afd6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:poem" data-paper-title="POEM: Partial-Order Enhanced Real-Time Sequential Modeling for Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="POEM: Partial-Order Enhanced Real-Time Sequential Modeling for Recommendation 搜广推与 LLM 应用 Kuaishou 2026-06-29 把当前请求多个排序目标产生的相对次序转成偏序信号，动态构造比纯时间序更贴近实时兴趣的训练序列。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 POEM 为 0.05009，相对变化 -7.25%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  sequential-recommendation partial-order real-time 搜广推 用户历史与排序骨干 POEM 为什么把当前请求多个目标的相对次序变成偏序，而不只按历史时间排训练序列？ 时间顺序描述事件发生先后，不一定描述当前请求最在意的候选关系。POEM 汇总多个目标对候选的相对排序，构造反映请求偏好的偏序信号，再据此组织训练。多目标分歧可保留为不完全确定的关系；它借用的是已有目标的判断，不能被当作独立、无偏的真实用户偏好。 示意：两个商品先后被浏览，但当前点击和购买模型都更偏好后者。偏序信号可以表达“后者在本请求更优”，而不是强迫模型把浏览时间先后当成偏好强弱。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-poem-c8eda543" class="ar-learning-paper-anchor"></span>
<h2 id="qa-47020eb5235815f6">POEM 为什么把当前请求多个目标的相对次序变成偏序，而不只按历史时间排训练序列？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apoem">POEM: Partial-Order Enhanced Real-Time Sequential Modeling for Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>时间顺序描述事件发生先后，不一定描述当前请求最在意的候选关系。POEM 汇总多个目标对候选的相对排序，构造反映请求偏好的偏序信号，再据此组织训练。多目标分歧可保留为不完全确定的关系；它借用的是已有目标的判断，不能被当作独立、无偏的真实用户偏好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个商品先后被浏览，但当前点击和购买模型都更偏好后者。偏序信号可以表达“后者在本请求更优”，而不是强迫模型把浏览时间先后当成偏好强弱。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.29946">原论文</a> · <a href="../../../../reproductions/2606.29946-poem/">实现解读</a> · <a href="#qa-47020eb5235815f6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cmsl" data-paper-title="CMSL: Constructive Multi-Sequence Learning for Recommendation Systems" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="CMSL: Constructive Multi-Sequence Learning for Recommendation Systems 搜广推与 LLM 应用 Meta 2026-06-26 把点击、观看、互动等所有行为塞进单一长序列会混合多个意图，且 self-attention 成本随长度快速增长。CMSL 不依赖预定义业务 taxonomy，而是利用当前上下文特征学习多个 contextual lens，把原始历史动态构造成 K 条 latent semantic sequence；每条 strand 独立编码，再用当前非序列上下文作为 query 做 PMA 聚合。论文还给出 degree-2 polynomial feature map 的线性 HSTU 近似，以支持工业长序列。 Fidelity: 核心机制复现。当前实现让 contextual lenses、软序列构造和 HSTU-style gated attention 一起反向传播；未复刻 Meta 私有特征、规模和分布式 serving。本地对照口径：基线与实验组共享 embedding、HSTU block、优化器和训练预算；实验组仅增加 6 个 learned contextual lenses 和多 strand 聚合，NDCG@10 +29.42%，不是相对 DIN。   搜广推 用户历史与排序骨干 CMSL的contextual lens为什么不是预先按点击、购买等行为类型分桶？ 固定业务分桶未必对应用户当下的潜在意图。CMSL根据事件和当前上下文学习软分配，让同一历史形成多个语义strand，各自编码后再按非序列上下文聚合。它把兴趣拆分和场景选择都变成可学习过程；软分配不保证天然互补，仍需检查不同strand是否重复或失去有效历史。 示意：一次厨房用品点击既可能属于日常补货，也可能属于搬家准备；上下文不同，事件可被不同lens赋权，而不必永远留在同一个点击桶里。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-cmsl-b229ccb6" class="ar-learning-paper-anchor"></span>
<h2 id="qa-89f711951fa492ec">CMSL的contextual lens为什么不是预先按点击、购买等行为类型分桶？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acmsl">CMSL: Constructive Multi-Sequence Learning for Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定业务分桶未必对应用户当下的潜在意图。CMSL根据事件和当前上下文学习软分配，让同一历史形成多个语义strand，各自编码后再按非序列上下文聚合。它把兴趣拆分和场景选择都变成可学习过程；软分配不保证天然互补，仍需检查不同strand是否重复或失去有效历史。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次厨房用品点击既可能属于日常补货，也可能属于搬家准备；上下文不同，事件可被不同lens赋权，而不必永远留在同一个点击桶里。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.28533">原论文</a> · <a href="../../../../reproductions/2606.28533-cmsl/">实现解读</a> · <a href="#qa-89f711951fa492ec">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:uniformer" data-paper-title="UniFormer: Efficient and Unified Model-Centric Scaling for Industrial Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="UniFormer: Efficient and Unified Model-Centric Scaling for Industrial Recommendation 搜广推与 LLM 应用 Kuaishou 2026-06-25 把 item-independent/dependent 特征与不同任务拆成语义 token，通过统一交互模块共同扩展序列、特征和任务空间。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 UniFormer 为 0.04131，相对变化 -23.50%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  ranking feature-tokenization multi-task 搜广推 用户历史与排序骨干 UniFormer 为什么显式区分 item-independent、item-dependent 与 task token 后再统一交互？ 候选无关特征可表达用户公共状态，候选相关特征负责当前匹配，任务 token 指明预测目标。先明确语义角色再交互，有助统一序列、字段与任务的扩展接口，避免把所有输入视为同质字段。统一模块不等于这些状态都能跨候选缓存；一旦发生候选相关信息流，复用边界仍需由掩码和结构保证。 示意：用户年龄属于公共 token，候选价格属于商品相关 token，购买任务另有目标 token。三者可共同建模，但包含某件商品价格的交互状态不能直接复用给另一件商品。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-uniformer-655acc49" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b79ebda446d84c88">UniFormer 为什么显式区分 item-independent、item-dependent 与 task token 后再统一交互？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Auniformer">UniFormer: Efficient and Unified Model-Centric Scaling for Industrial Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>候选无关特征可表达用户公共状态，候选相关特征负责当前匹配，任务 token 指明预测目标。先明确语义角色再交互，有助统一序列、字段与任务的扩展接口，避免把所有输入视为同质字段。统一模块不等于这些状态都能跨候选缓存；一旦发生候选相关信息流，复用边界仍需由掩码和结构保证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户年龄属于公共 token，候选价格属于商品相关 token，购买任务另有目标 token。三者可共同建模，但包含某件商品价格的交互状态不能直接复用给另一件商品。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.27058">原论文</a> · <a href="../../../../reproductions/2606.27058-uniformer/">实现解读</a> · <a href="#qa-b79ebda446d84c88">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:journeyformer" data-paper-title="JourneyFormer: Encoding Airbnb Guest Journey with Sequence Modeling" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="JourneyFormer: Encoding Airbnb Guest Journey with Sequence Modeling 搜广推与 LLM 应用 Airbnb 2026-06-17 统一编码 Airbnb 长期和短期 guest journey，以事件类型、时间和 listing 表示构建序列，并通过缓存和稀疏计算满足线上时延。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  search-ranking sequence-modeling long-sequence 搜广推 用户历史与排序骨干 JourneyFormer为什么把事件类型与时间编码进guest journey，而不只记录浏览过的房源？ 相同房源出现在搜索、浏览、收藏或预订阶段，表达的决策进展不同；时间间隔又区分同次旅行与较早计划。统一旅程序列让模型学习阶段之间的关联，兼顾长期偏好和短期出行需求。缓存与稀疏计算只减少成本，不能因此忽略每个请求当时可见的事件边界。 示意：用户去年收藏海边房源，今天连续搜索市中心并查看商务公寓；房源ID列表不够区分两次旅行，事件类型和时间能帮助识别当前行程。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-journeyformer-09e3e4a3" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d64a894bfbe04f44">JourneyFormer为什么把事件类型与时间编码进guest journey，而不只记录浏览过的房源？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ajourneyformer">JourneyFormer: Encoding Airbnb Guest Journey with Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Airbnb</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相同房源出现在搜索、浏览、收藏或预订阶段，表达的决策进展不同；时间间隔又区分同次旅行与较早计划。统一旅程序列让模型学习阶段之间的关联，兼顾长期偏好和短期出行需求。缓存与稀疏计算只减少成本，不能因此忽略每个请求当时可见的事件边界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户去年收藏海边房源，今天连续搜索市中心并查看商务公寓；房源ID列表不够区分两次旅行，事件类型和时间能帮助识别当前行程。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.19108">原论文</a> · <a href="../../../../reproductions/2606.19108-journeyformer/">实现解读</a> · <a href="#qa-d64a894bfbe04f44">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onerank" data-paper-title="OneRank: Unified Transformer-Native Ranking Architecture for Multi-Task Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OneRank: Unified Transformer-Native Ranking Architecture for Multi-Task Recommendation 搜广推与 LLM 应用 Renmin University of China 2026-06-15 取消 encoder 与 task predictor 的割裂，把结构化特征和任务 token 放进统一序列，并用 task-private channel 与梯度隔离控制任务冲突。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 OneRank 为 0.09540，相对变化 +76.65%。这是公开代理任务上的机制结果，生产线上 lift 的外推不适用。  ranking multi-task transformer 搜广推 用户历史与排序骨干 OneRank 为什么在统一序列里保留 task-private channel，并隔离其他任务对它的梯度？ 任务 token 能让共享主干感知要预测什么，但所有参数仍共享时，冲突目标会争夺同一表示。私有通道为每个任务保留专属容量，梯度隔离保证其他任务损失不会直接改写该部分。统一输入负责共享信息，私有通道负责差异；它控制冲突的路径，而不是假设不同任务的最优表示完全一致。 示意：点击任务偏重新颖，购买任务偏重可靠。两者共用商品与用户序列，但点击损失不能直接更新购买私有通道，让购买相关的细分特征不被另一目标覆盖。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-onerank-a08d1448" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1cd8516d4afdddcd">OneRank 为什么在统一序列里保留 task-private channel，并隔离其他任务对它的梯度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonerank">OneRank: Unified Transformer-Native Ranking Architecture for Multi-Task Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Renmin University of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>任务 token 能让共享主干感知要预测什么，但所有参数仍共享时，冲突目标会争夺同一表示。私有通道为每个任务保留专属容量，梯度隔离保证其他任务损失不会直接改写该部分。统一输入负责共享信息，私有通道负责差异；它控制冲突的路径，而不是假设不同任务的最优表示完全一致。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>点击任务偏重新颖，购买任务偏重可靠。两者共用商品与用户序列，但点击损失不能直接更新购买私有通道，让购买相关的细分特征不被另一目标覆盖。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.16838">原论文</a> · <a href="../../../../reproductions/2606.16838-onerank/">实现解读</a> · <a href="#qa-1cd8516d4afdddcd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:memento" data-paper-title="Memento: Personalized RAG-Style Long-Retention Data Scaling for Online Ads Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Memento: Personalized RAG-Style Long-Retention Data Scaling for Online Ads Recommendation 搜广推与 LLM 应用 Meta 2026-05-22 工业推荐模型通常只保留有限长度历史，长期但相关的行为被截断；训练数据也会因一次 SGD 后被“忘记”。Memento 将 RAG 思想分成两条路径：Representation Memento 从最长 365 天用户历史 embedding 库检索与当前 query 相关且互不冗余的事件，再用 Ember 条件变换融入主模型；Data Memento 从历史训练样本库检索被当前模型遗忘、但与当前 batch 有关的样本做第二次 replay。 未复现 Ember、INT8 检索服务与 Data Memento replay。Fidelity: 核心机制复现。query-conditioned MMR 长历史检索实际执行；Meta 私有 Ember、replay 与 INT8 serving 未复刻。本地对照口径：基线是 LastN 历史截断；实验组是 query-conditioned Memento MMR；NDCG@10 从 0.0443 升至 0.0464（+4.78%）。这是历史检索策略消融，不是相对 DIN。   搜广推 用户历史与排序骨干 Memento的Representation路径和Data replay路径分别在挽救哪种遗忘？ 历史截断让推理时缺少远期兴趣，Representation路径检索相关且不冗余的事件并条件化融入模型。训练样本只用一次则可能被参数更新遗忘，Data路径回放与当前batch有关的旧样本。一个补输入证据，一个补训练经验，不能把只实现历史检索的本地结果说成两种记忆都已验证。 示意：一年前的摄影兴趣从输入窗口消失，可检索回来；模型曾学过但后来淡化的冷门类别，则需要训练回放。把旧向量塞进当前输入并不等于重新学过旧样本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-memento-1c9d9291" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b1cdd545af184e84">Memento的Representation路径和Data replay路径分别在挽救哪种遗忘？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amemento">Memento: Personalized RAG-Style Long-Retention Data Scaling for Online Ads Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>历史截断让推理时缺少远期兴趣，Representation路径检索相关且不冗余的事件并条件化融入模型。训练样本只用一次则可能被参数更新遗忘，Data路径回放与当前batch有关的旧样本。一个补输入证据，一个补训练经验，不能把只实现历史检索的本地结果说成两种记忆都已验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一年前的摄影兴趣从输入窗口消失，可检索回来；模型曾学过但后来淡化的冷门类别，则需要训练回放。把旧向量塞进当前输入并不等于重新学过旧样本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.24051">原论文</a> · <a href="../../../../reproductions/2605.24051-memento/">实现解读</a> · <a href="#qa-b1cdd545af184e84">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tubifm" data-paper-title="TubiFM: Unified Item, Carousel, and Search Ranking for Streaming Discovery" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TubiFM: Unified Item, Carousel, and Search Ranking for Streaming Discovery 搜广推与 LLM 应用 Tubi 2026-05-22 以统一 user story 序列描述跨页面旅程，同一个生成式 foundation model 通过任务提示完成 item、carousel 与 search 三种排序。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  foundation-model multi-task-learning search-ranking 搜广推 用户历史与排序骨干 TubiFM 为什么用统一 user story 描述跨页面旅程，再以任务提示区分 item、carousel 与 search？ 分散页面模型容易各自截取局部行为，难以连接用户旅程。统一序列把不同页面事件放入同一上下文，任务提示再告诉生成式模型当前评分对象和目标，让共享知识服务不同入口。统一输入格式并不意味着所有页面目标相同，也不自动解决不同候选类型的校准，本地核心代理只验证接口层面的机制。 示意：用户先搜索悬疑片，再在专题轮播中浏览，最后点进具体电影。用同一旅程序列建模后，任务提示决定此刻排序的是电影、专题栏还是搜索结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-tubifm-2a9a268d" class="ar-learning-paper-anchor"></span>
<h2 id="qa-23cac2c087366ab8">TubiFM 为什么用统一 user story 描述跨页面旅程，再以任务提示区分 item、carousel 与 search？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atubifm">TubiFM: Unified Item, Carousel, and Search Ranking for Streaming Discovery</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tubi</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分散页面模型容易各自截取局部行为，难以连接用户旅程。统一序列把不同页面事件放入同一上下文，任务提示再告诉生成式模型当前评分对象和目标，让共享知识服务不同入口。统一输入格式并不意味着所有页面目标相同，也不自动解决不同候选类型的校准，本地核心代理只验证接口层面的机制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户先搜索悬疑片，再在专题轮播中浏览，最后点进具体电影。用同一旅程序列建模后，任务提示决定此刻排序的是电影、专题栏还是搜索结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.23702">原论文</a> · <a href="../../../../reproductions/2605.23702-tubifm/">实现解读</a> · <a href="#qa-23cac2c087366ab8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:uxsid" data-paper-title="UxSID: Semantic-Aware User Interests Modeling for Ultra-Long Sequence" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="UxSID: Semantic-Aware User Interests Modeling for Ultra-Long Sequence 搜广推与 LLM 应用 Kuaishou 2026-05-09 UxSID 在逐候选检索和完全候选无关的历史压缩之间加入“目标语义组共享记忆”：用目标物品第一层 SID 查询全历史与可学习兴趣锚点，利用全局兴趣门控第二层语义探针。语义相近的候选共享用户兴趣表示，使离线端到端训练与线上按用户/SID 查表使用同一记忆。IAIC 先用可学习锚点对行为序列做交叉注意力，再为每个锚点配置独立 Sigmoid PFFN、残差及 LayerNorm；正交项抑制兴趣坍缩。目标 SID 对原序列取全局响应，并以该响应门控 SID 后查询压缩锚点，最后拼接两级兴趣表示进行监督训练。 一次早期 CPU/seed42/100 用户/1 epoch 诊断中，UxSID test AUC 0.5848，validation 选择的 agnostic 为 0.5916；默认 encoder 是固定版本 Qwen2.5-0.5B-Instruct 7ae557604adf67be50417f59c2c2f167def9a775；仅输入公开电影标题和 genre。所有 encoder 参数冻结，mask mean pooling 后归一化，不读取评分/验证/测试标签。公开文本语义不是私有视频/世界知识对齐 MLLM。  long-sequence ranking semantic-id compression 搜广推 用户历史与排序骨干 UxSID 为什么按目标第一层 SID 共享记忆，而不逐候选检索或完全候选无关地压缩历史？ 逐候选读全历史重复昂贵，完全公共摘要又容易丢掉目标相关细节。UxSID 让语义同组候选共享用户兴趣，第一层 SID 先响应原历史并门控后续语义探针，再读取可学习锚点；独立 PFFN 与正交约束减少兴趣坍缩。共享粒度介于用户与单物品之间，但同组候选仍可能存在被压平的差异。 示意：多件露营商品共享一份用户露营记忆，而相机组读取另一份。这样不用每顶帐篷都遍历全历史，又比所有商品只用一个通用用户向量更有针对性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-uxsid-c8fb3e15" class="ar-learning-paper-anchor"></span>
<h2 id="qa-79650491f8323060">UxSID 为什么按目标第一层 SID 共享记忆，而不逐候选检索或完全候选无关地压缩历史？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Auxsid">UxSID: Semantic-Aware User Interests Modeling for Ultra-Long Sequence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>逐候选读全历史重复昂贵，完全公共摘要又容易丢掉目标相关细节。UxSID 让语义同组候选共享用户兴趣，第一层 SID 先响应原历史并门控后续语义探针，再读取可学习锚点；独立 PFFN 与正交约束减少兴趣坍缩。共享粒度介于用户与单物品之间，但同组候选仍可能存在被压平的差异。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>多件露营商品共享一份用户露营记忆，而相机组读取另一份。这样不用每顶帐篷都遍历全历史，又比所有商品只用一个通用用户向量更有针对性。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.09040">原论文</a> · <a href="../../../../reproductions/2605.09040-uxsid/">实现解读</a> · <a href="#qa-79650491f8323060">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:semantic-native-longseq" data-paper-title="Beyond Item IDs: Scaling Short-Form-Video Recommendation via Semantic-Native Long Sequence Modeling" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Beyond Item IDs: Scaling Short-Form-Video Recommendation via Semantic-Native Long Sequence Modeling 搜广推与 LLM 应用 Google 2026-05-04 原子 Video ID 只能记忆内容，embedding table 随 corpus 无界增长，新视频也没有可迁移语义；完整 attention 又让千级历史成本呈平方增长。论文先用 RQ-VAE 产生 coarse-to-fine SID，并截断为 bounded bigram vocabulary；再把相邻个事件无参数折叠为 super-token，同时加入统一 global query，使模型在保留全局兴趣的情况下处理更长历史。 本地未训练 Google RQ-VAE，没有 billion-user 私有流量、2,000-event 服务序列、异步长历史模块或定制 HBM kernel。Fidelity: 核心机制复现。本地实际构建 residual-quantized Semantic ID，执行 depth-truncated bigram、parameter-free temporal folding、global query attention 和 global-local pooling。MovieLens feature 只代理多模态视频表征；  long-sequence semantic-id rq-vae efficient-transformer cold-start 搜广推 用户历史与排序骨干 Semantic-Native LongSeq 为什么同时压缩 SID 词表和时间序列，而不是只扩大历史窗口？ 原子 ID 表随内容增长，长序列全注意力又随长度平方增加。层级 SID 截断为有界词表处理表示规模，相邻事件折叠为 super-token 处理时间长度，全局 query 再收集跨窗口兴趣。两种压缩针对不同瓶颈，都会牺牲分辨率；本地用均值与近期组合代理折叠，不能当作原文通道重排的等价实现。 示意：四十八条历史每四条折成一个 token，只需处理十二个局部位置；同时用粗细语义码共享内容知识。被折在同一窗口的事件顺序仍可能损失，不能说完整细节都保留。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-semantic-native-longseq-dee361e1" class="ar-learning-paper-anchor"></span>
<h2 id="qa-63e5da9e21228955">Semantic-Native LongSeq 为什么同时压缩 SID 词表和时间序列，而不是只扩大历史窗口？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asemantic-native-longseq">Beyond Item IDs: Scaling Short-Form-Video Recommendation via Semantic-Native Long Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原子 ID 表随内容增长，长序列全注意力又随长度平方增加。层级 SID 截断为有界词表处理表示规模，相邻事件折叠为 super-token 处理时间长度，全局 query 再收集跨窗口兴趣。两种压缩针对不同瓶颈，都会牺牲分辨率；本地用均值与近期组合代理折叠，不能当作原文通道重排的等价实现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>四十八条历史每四条折成一个 token，只需处理十二个局部位置；同时用粗细语义码共享内容知识。被折在同一窗口的事件顺序仍可能损失，不能说完整细节都保留。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.07546">原论文</a> · <a href="../../../../reproductions/2606.07546-semantic-native-longseq/">实现解读</a> · <a href="#qa-63e5da9e21228955">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rankup" data-paper-title="RankUp: Towards High-rank Representations for Large Scale Advertising Recommender Systems" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="RankUp: Towards High-rank Representations for Large Scale Advertising Recommender Systems 搜广推与 LLM 应用 Tencent 2026-04-20 RankUp 针对深层推荐网络的表征坍缩，组合随机置换分组、多套 embedding、全局 token、交叉预训练 embedding 注入和任务 token 解耦，让随模型规模增长的参数真正转化为更高秩的表达空间。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04702，相对变化 -12.94%。本地代理目标与论文生产任务不同，不能外推线上 lift。  advertising representation-collapse feature-interaction 搜广推 用户历史与排序骨干 RankUp 为什么不仅增加 embedding 或层数，还用随机置换分组和全局 token 对抗低秩坍缩？ 参数增加并不保证表示包含更多独立方向，深层交互可能反复使用相同子空间。不同置换与多套 embedding 改变特征组合路径，全局 token 提供跨组交流，外部表征与任务解耦再补充不同信息。目标是让新增容量转成更丰富的表示秩；这些结构只是缓解手段，不能把参数变多等同于有效秩必然提高。 示意：四组特征若始终按同一种方式分组，层数再多也可能重复同样交叉。换不同分组并保留全局交流通道，可让原先从未同组的特征形成新的组合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-rankup-a9399758" class="ar-learning-paper-anchor"></span>
<h2 id="qa-0478859fae50a11a">RankUp 为什么不仅增加 embedding 或层数，还用随机置换分组和全局 token 对抗低秩坍缩？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arankup">RankUp: Towards High-rank Representations for Large Scale Advertising Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>参数增加并不保证表示包含更多独立方向，深层交互可能反复使用相同子空间。不同置换与多套 embedding 改变特征组合路径，全局 token 提供跨组交流，外部表征与任务解耦再补充不同信息。目标是让新增容量转成更丰富的表示秩；这些结构只是缓解手段，不能把参数变多等同于有效秩必然提高。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>四组特征若始终按同一种方式分组，层数再多也可能重复同样交叉。换不同分组并保留全局交流通道，可让原先从未同组的特征形成新的组合。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.17878">原论文</a> · <a href="../../../../reproductions/2604.17878-rankup/">实现解读</a> · <a href="#qa-0478859fae50a11a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:uniscale" data-paper-title="UniScale: Synergistic Entire Space Data and Model Scaling for Search Ranking" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="UniScale: Synergistic Entire Space Data and Model Scaling for Search Ranking 搜广推与 LLM 应用 Taobao &amp; Tmall Group / Alibaba 2026-03-25 ES³ 从曝光外全空间扩充数据，HHSFT 分层融合异构样本；数据规模和模型容量协同扩展，并配合低成本部署。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 uniscale 核心机制，相对 NDCG@10 -2.20%。  search-ranking model-scaling entire-space-learning 搜广推 用户历史与排序骨干 UniScale 为什么把曝光外数据扩充与分层异构训练一起做，而不只增加模型参数？ 仅扩大网络仍受现有曝光日志覆盖限制，新增容量可能继续拟合同样狭窄的样本。曝光外扩充增加学习范围，分层融合为不同来源和质量的数据安排合适路径，再协同扩大容量。关键是数据与模型共同扩展，合成或曝光外样本的可信度仍要控制；数据更多不自动意味着偏差更小。 示意：模型原来只见过首页曝光商品，即使参数翻倍也难学未曝光品类。扩充其他空间样本后，再按来源层次融合，可避免把高置信点击和弱监督样本完全等量对待。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-uniscale-5256c0f4" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f29a5b9c1c823d5f">UniScale 为什么把曝光外数据扩充与分层异构训练一起做，而不只增加模型参数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Auniscale">UniScale: Synergistic Entire Space Data and Model Scaling for Search Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>仅扩大网络仍受现有曝光日志覆盖限制，新增容量可能继续拟合同样狭窄的样本。曝光外扩充增加学习范围，分层融合为不同来源和质量的数据安排合适路径，再协同扩大容量。关键是数据与模型共同扩展，合成或曝光外样本的可信度仍要控制；数据更多不自动意味着偏差更小。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型原来只见过首页曝光商品，即使参数翻倍也难学未曝光品类。扩充其他空间样本后，再按来源层次融合，可避免把高置信点击和弱监督样本完全等量对待。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.24226">原论文</a> · <a href="../../../../reproductions/2603.24226-uniscale/">实现解读</a> · <a href="#qa-f29a5b9c1c823d5f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sort-ranking" data-paper-title="SORT: A Systematically Optimized Ranking Transformer for Industrial-scale Recommenders" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="SORT: A Systematically Optimized Ranking Transformer for Industrial-scale Recommenders 搜广推与 LLM 应用 Alibaba International Digital Commerce 2026-03-04 系统重做特征 token 化、注意力和 FFN，并以面向工业硬件的结构压缩长序列，使单一 Transformer 替代传统 DLRM。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 sort-ranking 核心机制，相对 NDCG@10 -13.11%。  ranking transformer serving-efficiency 搜广推 用户历史与排序骨干 SORT Ranking 为什么连特征 token 化、注意力与 FFN 都要一起改，而不直接把语言 Transformer 搬到排序？ 推荐输入包含语义各异的字段和长行为序列，token 组织决定哪些信息能交互，注意力决定信息流，FFN 决定逐 token 的变换容量。硬件约束下压缩长序列还会改变计算分配，因此几个环节需要协同设计。使用 Transformer 只是框架选择，本地简化机制不能证明完整工业 DLRM 替换方案的吞吐与精度。 示意：把年龄、商品类别和数百次行为都当同一种文本词直接堆入模型，可能浪费预算。先设计字段接口与历史压缩，再分配注意力和 FFN，才有机会匹配排序负载。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-sort-ranking-bed02966" class="ar-learning-paper-anchor"></span>
<h2 id="qa-a030a6e6a420cbd7">SORT Ranking 为什么连特征 token 化、注意力与 FFN 都要一起改，而不直接把语言 Transformer 搬到排序？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asort-ranking">SORT: A Systematically Optimized Ranking Transformer for Industrial-scale Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>推荐输入包含语义各异的字段和长行为序列，token 组织决定哪些信息能交互，注意力决定信息流，FFN 决定逐 token 的变换容量。硬件约束下压缩长序列还会改变计算分配，因此几个环节需要协同设计。使用 Transformer 只是框架选择，本地简化机制不能证明完整工业 DLRM 替换方案的吞吐与精度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把年龄、商品类别和数百次行为都当同一种文本词直接堆入模型，可能浪费预算。先设计字段接口与历史压缩，再分配注意力和 FFN，才有机会匹配排序负载。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.03988">原论文</a> · <a href="../../../../reproductions/2603.03988-sort-ranking/">实现解读</a> · <a href="#qa-a030a6e6a420cbd7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hpgr" data-paper-title="Beyond the Flat Sequence: Hierarchical and Preference-Aware Generative Recommendations" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Beyond the Flat Sequence: Hierarchical and Preference-Aware Generative Recommendations 搜广推与 LLM 应用 Harbin Institute of Technology 2026-03-01 HPGR 先通过基于 session 的掩码物品建模学习层级行为结构，再在微调阶段使用偏好引导稀疏注意力，只保留与当前意图最相关的历史事件，减少平铺长序列里的噪声和计算。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05467，相对变化 +1.23%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation hierarchical-sequence sparse-attention 搜广推 用户历史与排序骨干 HPGR为什么先做session掩码预训练，再用偏好引导的稀疏注意力选历史？ session结构描述一段行为内部的关联，先通过掩码任务学习它，可避免把长历史当作无差别平铺事件。微调时再依据当前偏好选择相关历史，把计算集中在有用证据上，而非只按时间截断。稀疏选择也可能丢掉罕见但关键的兴趣，因此选中项的覆盖与最终预测需要一起检验。 示意：用户上周的一组相机比较属于同一session，今天评镜头时可整组提取；最近一次无关购物不应只因更近就挤掉这段有组织的历史。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-hpgr-f17a7799" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f5ebe6d332af25ec">HPGR为什么先做session掩码预训练，再用偏好引导的稀疏注意力选历史？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahpgr">Beyond the Flat Sequence: Hierarchical and Preference-Aware Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>session结构描述一段行为内部的关联，先通过掩码任务学习它，可避免把长历史当作无差别平铺事件。微调时再依据当前偏好选择相关历史，把计算集中在有用证据上，而非只按时间截断。稀疏选择也可能丢掉罕见但关键的兴趣，因此选中项的覆盖与最终预测需要一起检验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户上周的一组相机比较属于同一session，今天评镜头时可整组提取；最近一次无关购物不应只因更近就挤掉这段有组织的历史。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.00980">原论文</a> · <a href="../../../../reproductions/2603.00980-hpgr/">实现解读</a> · <a href="#qa-f5ebe6d332af25ec">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hisac" data-paper-title="HiSAC: Hierarchical Sparse Activation Compression for Ultra-long Sequence Modeling in Recommenders" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="HiSAC: Hierarchical Sparse Activation Compression for Ultra-long Sequence Modeling in Recommenders 搜广推与 LLM 应用 Alibaba / Taobao 2026-02-24 超长行为全量 attention 成本高，固定压缩又损失长尾兴趣。HiSAC 用多模态 RQ-VAE 形成层级 code，逐层投票生成用户特定 interest agents，再让当前 query 只 soft-route 到少量相关 agent。 Fidelity: 核心机制复现。执行 residual codes、层级投票、兴趣 agent 与 soft routing。本地最多 64 行为，未复刻淘宝多模态 embedding、超长日志、稀疏 kernel 和线上服务。本地对照口径：基线是 recent-window dense proxy；实验组使用三层 codes、hierarchical voting 和 soft routing，NDCG@10 0.03540→0.03586，相对 +1.31%，Hit@10 相对 -4.35%。  long-sequence sparse-activation semantic-id 搜广推 用户历史与排序骨干 HiSAC为什么先形成层级interest agents，再让当前query只路由到少量agent？ 全历史attention昂贵，固定单摘要又易丢长尾兴趣。层级码与投票先把行为组织成用户特定兴趣表示，query再选择相关部分，减少逐请求需要读取的状态。兴趣agent不是能自由推理的独立LLM，而是结构化压缩单元；若层级划分或路由遗漏稀有兴趣，后续聚合也无法自动恢复。 示意：长历史里有摄影、烹饪和骑行三组兴趣，推荐镜头时主要读取摄影agent；若把少量天文摄影行为压掉，再精确的query路由也找不到那部分证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-hisac-bc7a3c37" class="ar-learning-paper-anchor"></span>
<h2 id="qa-4e26b8af5e5c89d6">HiSAC为什么先形成层级interest agents，再让当前query只路由到少量agent？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahisac">HiSAC: Hierarchical Sparse Activation Compression for Ultra-long Sequence Modeling in Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全历史attention昂贵，固定单摘要又易丢长尾兴趣。层级码与投票先把行为组织成用户特定兴趣表示，query再选择相关部分，减少逐请求需要读取的状态。兴趣agent不是能自由推理的独立LLM，而是结构化压缩单元；若层级划分或路由遗漏稀有兴趣，后续聚合也无法自动恢复。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>长历史里有摄影、烹饪和骑行三组兴趣，推荐镜头时主要读取摄影agent；若把少量天文摄影行为压掉，再精确的query路由也找不到那部分证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.21009">原论文</a> · <a href="../../../../reproductions/2602.21009-hisac/">实现解读</a> · <a href="#qa-4e26b8af5e5c89d6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ultra-hstu" data-paper-title="Bending the Scaling Law Curve in Large-Scale Recommendation Systems" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Bending the Scaling Law Curve in Large-Scale Recommendation Systems 搜广推与 LLM 应用 Meta 2026-02-19 原始 HSTU 扩展到 16k 行为和更深网络时，attention 与内存成本成为瓶颈。ULTRA-HSTU 用 semi-local attention 保留局部 token 和少量 landmark，LBSL 令越深层看到越宽范围，再以 Mixture of Transducers、attention truncation、混合精度和动态拓扑共同提升训练与推理斜率。 Fidelity: 核心机制复现。本地执行 semi-local attention、LBSL 逐层扩窗与 Mixture of Transducers。48-event 序列替代 16k 历史；不复刻 18 层生产模型、动态 topology、FP8 kernel 或 Meta 私有日志。本地对照口径：基线为 short-history transition-content ranker，实验组执行 ULTRA-HSTU compact core；NDCG@10 相对 -0.95%。  ranking long-sequence scaling-law attention serving 搜广推 用户历史与排序骨干 ULTRA-HSTU 为什么在局部窗口之外保留 landmark，并让更深层扩大可见范围？ 只看固定局部窗口会失去远期连接，全连接又难承受长序列成本。landmark 提供稀疏全局通道，随层加宽的局部范围让深层逐步整合更远信息，再配合混合 transducer 和系统优化扩展规模。稀疏模式改变可达路径，不是无损替代全注意力；端到端效率还受窗口、landmark 数和具体内核影响。 示意：浅层先理解最近几次点击，少量代表点连接过去兴趣，深层再扩大窗口组合更多上下文。像先看邻里再看城区，不能假设第一层已经读过所有历史细节。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-ultra-hstu-194b1e9b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-11dc09f7eb43dcda">ULTRA-HSTU 为什么在局部窗口之外保留 landmark，并让更深层扩大可见范围？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aultra-hstu">Bending the Scaling Law Curve in Large-Scale Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只看固定局部窗口会失去远期连接，全连接又难承受长序列成本。landmark 提供稀疏全局通道，随层加宽的局部范围让深层逐步整合更远信息，再配合混合 transducer 和系统优化扩展规模。稀疏模式改变可达路径，不是无损替代全注意力；端到端效率还受窗口、landmark 数和具体内核影响。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>浅层先理解最近几次点击，少量代表点连接过去兴趣，深层再扩大窗口组合更多上下文。像先看邻里再看城区，不能假设第一层已经读过所有历史细节。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.16986">原论文</a> · <a href="../../../../reproductions/2602.16986-ultra-hstu/">实现解读</a> · <a href="#qa-11dc09f7eb43dcda">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mixformer" data-paper-title="MixFormer: Co-Scaling Up Dense and Sequence in Industrial Recommenders" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="MixFormer: Co-Scaling Up Dense and Sequence in Industrial Recommenders 搜广推与 LLM 应用 ByteDance / Douyin 2026-02-15 现有推荐模型通常把 dense feature interaction 与 behavior-sequence Transformer 做成两个独立模块，模型预算必须在两边手工分配，且交互只发生在末端。MixFormer 将非序列字段和行为序列统一成同一 Transformer token space，共享参数、逐层发生高阶交互，从而联合扩大 dense capacity 与 sequence length。 Fidelity: 完整核心链路复现。当前代码在 matched local budget 下实际训练 stacked baseline 与 unified MixFormer blocks；proposed 将 dense feature-split tokens 和行为 tokens 放进共享 backbone，并复用 user encoding 对所有候选打分。本地对照口径：基线是参数量匹配的 Stacked Dense+Sequence；实验组是 Unified MixFormer；NDCG@10 从 0.0054 升至 0.0063（+17.41%）。   搜广推 用户历史与排序骨干 MixFormer 把稠密字段和行为序列放进同一 token 空间，和两个塔最后拼接有什么信息流区别？ 末端拼接时，字段交互与序列编码先各自完成，早期层无法根据对方的信息调整表示。MixFormer 让两类 token 在多层统一交互中共同更新，把预算和参数用于联合建模。服务时再解耦可共享的用户计算与候选相关计算；统一建模不等于每个候选都重算完整用户历史。 示意：用户刚连续浏览户外装备，当前场景是雨天。统一层可以在建模历史时利用场景字段，逐层强化防水需求；末端拼接只能拿已压缩的两份表示再组合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-mixformer-c586b532" class="ar-learning-paper-anchor"></span>
<h2 id="qa-7b0558ebad0e78da">MixFormer 把稠密字段和行为序列放进同一 token 空间，和两个塔最后拼接有什么信息流区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amixformer">MixFormer: Co-Scaling Up Dense and Sequence in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>末端拼接时，字段交互与序列编码先各自完成，早期层无法根据对方的信息调整表示。MixFormer 让两类 token 在多层统一交互中共同更新，把预算和参数用于联合建模。服务时再解耦可共享的用户计算与候选相关计算；统一建模不等于每个候选都重算完整用户历史。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户刚连续浏览户外装备，当前场景是雨天。统一层可以在建模历史时利用场景字段，逐层强化防水需求；末端拼接只能拿已压缩的两份表示再组合。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.14110">原论文</a> · <a href="../../../../reproductions/2602.14110-mixformer/">实现解读</a> · <a href="#qa-7b0558ebad0e78da">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:linkedin-feed-sr" data-paper-title="An Industrial-Scale Sequential Recommender for LinkedIn Feed Ranking" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="An Industrial-Scale Sequential Recommender for LinkedIn Feed Ranking 搜广推与 LLM 应用 LinkedIn 2026-02-12 将 Feed 候选、交互历史和上下文统一成超长序列，采用 HSTU 式目标注意力、负样本自由评估及增量服务优化。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 linkedin-feed-sr 核心机制，相对 NDCG@10 -0.12%。  ranking sequential-recommendation long-sequence 搜广推 用户历史与排序骨干 LinkedIn Feed序列模型为什么强调不依赖随机负采样的评价？ 随机抽少量容易负例会把排名任务变简单，掩盖大候选池中真正难区分的物品关系。统一候选、历史和上下文的序列模型需要在明确且一致的实际候选口径下评价，才能判断扩展与增量服务是否保留质量。本地代理排序不等于LinkedIn生产候选分布，更不能混用不同负例数量比较提升。 示意：在一个正例加九个明显无关内容中命中，和从数千相近Feed候选中找出同一内容不是同一难度；即使模型相同，两种指标也不能直接相减。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-linkedin-feed-sr-d07e7f6a" class="ar-learning-paper-anchor"></span>
<h2 id="qa-35861795e0c6722e">LinkedIn Feed序列模型为什么强调不依赖随机负采样的评价？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alinkedin-feed-sr">An Industrial-Scale Sequential Recommender for LinkedIn Feed Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>随机抽少量容易负例会把排名任务变简单，掩盖大候选池中真正难区分的物品关系。统一候选、历史和上下文的序列模型需要在明确且一致的实际候选口径下评价，才能判断扩展与增量服务是否保留质量。本地代理排序不等于LinkedIn生产候选分布，更不能混用不同负例数量比较提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>在一个正例加九个明显无关内容中命中，和从数千相近Feed候选中找出同一内容不是同一难度；即使模型相同，两种指标也不能直接相减。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12354">原论文</a> · <a href="../../../../reproductions/2602.12354-linkedin-feed-sr/">实现解读</a> · <a href="#qa-35861795e0c6722e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mlcc" data-paper-title="Compress, Cross and Scale: Multi-Level Compression Cross Networks for Efficient Scaling in Recommender Systems" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Compress, Cross and Scale: Multi-Level Compression Cross Networks for Efficient Scaling in Recommender Systems 搜广推与 LLM 应用 Bilibili 2026-02-12 在每一层先压缩高维特征，再在紧凑空间执行动态显式交叉并回注主干；MC-MLCC 使用多个并行子空间横向扩展表达力，使参数和 FLOPs 增长更可控。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05530，相对变化 +2.40%。本地代理目标与论文生产任务不同，不能外推线上 lift。  feature-interaction compression scaling-law 搜广推 用户历史与排序骨干 MLCC 为什么每层先压缩再做显式交叉，而不是只在输入端压缩一次？ 每层表示已经包含不同阶的交互，逐层压缩让后续交叉依赖当前状态，而不是始终围绕同一份输入投影。紧凑空间内的动态交叉再回注主干，控制高维运算的开销。多个并行子空间可覆盖不同关系，但表达力取决于压缩是否保留关键方向，不能把压缩视为无损操作。 示意：第一层先组合“地区与品类”，第二层可压缩这份新表示，再与价格偏好交叉；若只压缩最初字段，后续难以重新选择已形成的高阶关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-mlcc-9b40fb24" class="ar-learning-paper-anchor"></span>
<h2 id="qa-0f3168e9435168fe">MLCC 为什么每层先压缩再做显式交叉，而不是只在输入端压缩一次？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amlcc">Compress, Cross and Scale: Multi-Level Compression Cross Networks for Efficient Scaling in Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Bilibili</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每层表示已经包含不同阶的交互，逐层压缩让后续交叉依赖当前状态，而不是始终围绕同一份输入投影。紧凑空间内的动态交叉再回注主干，控制高维运算的开销。多个并行子空间可覆盖不同关系，但表达力取决于压缩是否保留关键方向，不能把压缩视为无损操作。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第一层先组合“地区与品类”，第二层可压缩这份新表示，再与价格偏好交叉；若只压缩最初字段，后续难以重新选择已形成的高阶关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12041">原论文</a> · <a href="../../../../reproductions/2602.12041-mlcc/">实现解读</a> · <a href="#qa-0f3168e9435168fe">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cadet" data-paper-title="CADET: Context-Conditioned Ads CTR Prediction With a Decoder-Only Transformer" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="CADET: Context-Conditioned Ads CTR Prediction With a Decoder-Only Transformer 搜广推与 LLM 应用 LinkedIn 2026-02-11 Decoder-only Transformer 先编码可缓存历史，候选打分后再注入 post-scoring context，避免训练与服务错位并统一广告 CTR 模型。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 cadet 核心机制，相对 NDCG@10 -6.20%。  advertising ctr-prediction decoder-only-transformer 搜广推 用户历史与排序骨干 CADET为什么要把可缓存历史和post-scoring context放在不同的信息流阶段？ 缓存历史必须在候选或后续上下文变化时仍保持语义有效。CADET先编码历史并进行候选打分，再在规定阶段注入post-scoring context，避免训练时借到服务打分点尚不可用的信号。若把所有信息一开始混入序列，即使离线分更高，也可能破坏复用条件并造成训练与服务错位。 示意：同一历史对应多个待评广告，不能把广告A打分后的上下文写进共享历史再给广告B；应保持共享前缀与后续条件化状态的明确边界。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-cadet-4647b60d" class="ar-learning-paper-anchor"></span>
<h2 id="qa-3572deb35e23e95e">CADET为什么要把可缓存历史和post-scoring context放在不同的信息流阶段？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acadet">CADET: Context-Conditioned Ads CTR Prediction With a Decoder-Only Transformer</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>缓存历史必须在候选或后续上下文变化时仍保持语义有效。CADET先编码历史并进行候选打分，再在规定阶段注入post-scoring context，避免训练时借到服务打分点尚不可用的信号。若把所有信息一开始混入序列，即使离线分更高，也可能破坏复用条件并造成训练与服务错位。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一历史对应多个待评广告，不能把广告A打分后的上下文写进共享历史再给广告B；应保持共享前缀与后续条件化状态的明确边界。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.11410">原论文</a> · <a href="../../../../reproductions/2602.11410-cadet/">实现解读</a> · <a href="#qa-3572deb35e23e95e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:kunlun" data-paper-title="Kunlun: Establishing Scaling Laws for Massive-Scale Recommendation Systems through Unified Architecture Design" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Kunlun: Establishing Scaling Laws for Massive-Scale Recommendation Systems through Unified Architecture Design 搜广推与 LLM 应用 Meta 2026-02-10 传统广告模型把序列塔、稠密交叉和系统并行分别优化，扩大规模后收益快速饱和。Kunlun 在每层同时放置 Transformer Block 与 Interaction Block：GDPA/PFFN 建模序列，HSP 汇总序列 seed，Global Interaction 交换序列与非序列信息；CompSkip 和 expert parallel 保持深层训练稳定与吞吐。 Fidelity: 核心机制复现。本地执行 GDPA、分层 seed pooling、expert routing 和 CompSkip；不声称复刻 Meta Ads 模型规模。本地仅验证网络算子和信息流；没有 Meta Ads 私有数据、万亿参数、expert parallel 或硬件 MFU 对照。本地对照口径：基线为 shallow transition-content ranker，实验组执行 Kunlun compact core；NDCG@10 相对 -5.25%。  ranking scaling-law long-sequence mixture-of-experts serving 搜广推 用户历史与排序骨干 Kunlun为什么交错序列块与交互块，而不只把其中一条塔扩得更大？ 序列模型负责历史依赖，异构交互负责字段关系，单独扩一侧可能受另一侧信息瓶颈限制。Kunlun在层间交换序列seed与非序列信息，并用门控和残差控制深层更新，再结合并行工程承载规模。结构联合扩展并非所有模块都可免费复用，必须区分候选依赖与实际服务开销。 示意：长历史提取了户外兴趣，但价格与场景交叉只在末端出现，可能无法影响更深的兴趣解释；交错结构让这两类信息在多层协同，而不只是concat一次。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-kunlun-7994f8f7" class="ar-learning-paper-anchor"></span>
<h2 id="qa-4031a3745258df11">Kunlun为什么交错序列块与交互块，而不只把其中一条塔扩得更大？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Akunlun">Kunlun: Establishing Scaling Laws for Massive-Scale Recommendation Systems through Unified Architecture Design</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>序列模型负责历史依赖，异构交互负责字段关系，单独扩一侧可能受另一侧信息瓶颈限制。Kunlun在层间交换序列seed与非序列信息，并用门控和残差控制深层更新，再结合并行工程承载规模。结构联合扩展并非所有模块都可免费复用，必须区分候选依赖与实际服务开销。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>长历史提取了户外兴趣，但价格与场景交叉只在末端出现，可能无法影响更深的兴趣解释；交错结构让这两类信息在多层协同，而不只是concat一次。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.10016">原论文</a> · <a href="../../../../reproductions/2602.10016-kunlun/">实现解读</a> · <a href="#qa-4031a3745258df11">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ml-dcn" data-paper-title="ML-DCN: Masked Low-Rank Deep Crossing Network Towards Scalable Ads Click-through Rate Prediction at Pinterest" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="ML-DCN: Masked Low-Rank Deep Crossing Network Towards Scalable Ads Click-through Rate Prediction at Pinterest 搜广推与 LLM 应用 Pinterest 2026-02-09 把 DCNv2 的全维交叉替换为可调内部维度的低秩交叉，并以可学习 mask 选择交叉通道，在相同 FLOPs 下扩大容量。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 ml-dcn 核心机制，相对 NDCG@10 -2.08%。  advertising feature-crossing serving-efficiency 搜广推 用户历史与排序骨干 ML-DCN 为什么在显式交叉前同时引入低秩投影和可学习 mask？ 全维交叉的容量与计算会一起增长。低秩投影把交叉压到可调内部维度，再映回原空间，减少昂贵的全维变换；mask 则调节哪些输入通道参与交叉。两者分别控制交叉的计算规模和信息选择，残差保留原表示，但低秩瓶颈也可能丢失不能被该子空间表达的关系。 示意：年龄、城市、设备等上千维特征不必全部两两充分交互。先保留与当前目标相关的通道，再用几十维子空间组合，省下的计算可用于增加层数或容量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-ml-dcn-5baa5b42" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b8e34d21c8c29d9b">ML-DCN 为什么在显式交叉前同时引入低秩投影和可学习 mask？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aml-dcn">ML-DCN: Masked Low-Rank Deep Crossing Network Towards Scalable Ads Click-through Rate Prediction at Pinterest</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全维交叉的容量与计算会一起增长。低秩投影把交叉压到可调内部维度，再映回原空间，减少昂贵的全维变换；mask 则调节哪些输入通道参与交叉。两者分别控制交叉的计算规模和信息选择，残差保留原表示，但低秩瓶颈也可能丢失不能被该子空间表达的关系。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>年龄、城市、设备等上千维特征不必全部两两充分交互。先保留与当前目标相关的通道，再用几十维子空间组合，省下的计算可用于增加层数或容量。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.09194">原论文</a> · <a href="../../../../reproductions/2602.09194-ml-dcn/">实现解读</a> · <a href="#qa-b8e34d21c8c29d9b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mdl" data-paper-title="MDL: A Unified Multi-Distribution Learner in Large-scale Industrial Recommendation through Tokenization" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="MDL: A Unified Multi-Distribution Learner in Large-scale Industrial Recommendation through Tokenization 搜广推与 LLM 应用 ByteDance / Douyin 2026-02-07 工业多场景、多任务模型常只在浅层做 gate，未充分共享大模型参数。MDL 把 feature、scenario 和 task 都表示成 token，经 feature self-attention、domain-feature attention 和 domain-fused aggregation 深层交互。 Fidelity: 核心机制复现。执行 feature/scenario/task tokens 与 domain-feature attention。MovieLens genre/next-item 代理抖音场景与任务，未复刻生产参数规模、私有标签和 serving。本地对照口径：基线是共享但非 tokenized ranker；实验组加入 19 feature tokens、19 scenario tokens 和 2 task tokens，NDCG@10 0.03540→0.04012，相对 +13.34%，但 head share +73.43%。  ranking multi-scenario multi-task tokenization 搜广推 用户历史与排序骨干 MDL为什么把scenario和task也做成token，而不只在输出端选不同head？ 末端分头无法让场景和任务需求持续影响特征选择。把它们作为token加入多层交互，domain query可读取相关字段，任务信息也能参与共享表示构造，增强深层复用。共享更深同时带来干扰可能，仍需检查低流量场景是否被大场景覆盖，不能用统一架构名称代替跨任务收益验证。 示意：相同商品字段用于首页点击和搜索转化时关注点不同；场景与任务token可在编码中改变取证方式，而不是所有信息压成同一向量后才分头判断。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-mdl-daad794f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f4f1ac6ba42c0ed1">MDL为什么把scenario和task也做成token，而不只在输出端选不同head？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amdl">MDL: A Unified Multi-Distribution Learner in Large-scale Industrial Recommendation through Tokenization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>末端分头无法让场景和任务需求持续影响特征选择。把它们作为token加入多层交互，domain query可读取相关字段，任务信息也能参与共享表示构造，增强深层复用。共享更深同时带来干扰可能，仍需检查低流量场景是否被大场景覆盖，不能用统一架构名称代替跨任务收益验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>相同商品字段用于首页点击和搜索转化时关注点不同；场景与任务token可在编码中改变取证方式，而不是所有信息压成同一向量后才分头判断。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.07520">原论文</a> · <a href="../../../../reproductions/2602.07520-mdl/">实现解读</a> · <a href="#qa-f4f1ac6ba42c0ed1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:msn" data-paper-title="MSN: A Memory-based Sparse Activation Scaling Framework for Large-scale Industrial Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="MSN: A Memory-based Sparse Activation Scaling Framework for Large-scale Industrial Recommendation 搜广推与 LLM 应用 ByteDance / Douyin Search 2026-02-07 工业排序希望扩大参数量但不同比例增加计算。MSN 将大容量知识放入两轴 Product-Key Memory，根据 query 只激活少量槽位，再用 gate 与 dense backbone 融合。 复现保真度：核心机制复现。复现保真度：核心机制复现。Product-Key Memory、top-k 稀疏读取和门控主干均实际执行。公开 genre 构造两轴 key，交互转移写入 memory value，每次只读取四个槽位。  search-ranking sparse-memory product-key-memory 搜广推 用户历史与排序骨干 MSN 的两轴 Product-Key Memory 如何增加参数容量而只读取少量知识？ 把键拆成两个轴后，一个槽位由两轴键的组合确定，组合空间可以很大。查询按两轴相似度的和寻找高分组合，只读取少量对应值，再通过 gate 与稠密主干融合。存储容量因此不必全部参与每次前向计算；效果仍依赖路由能否命中有用槽位，未激活的参数不会自动提供帮助。 示意：两组各一百个键可组合出一万个槽位，但一次请求只取最相关的四个。像从有两层索引的资料柜查少数文件，而不是把一万个文件全部读一遍。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-msn-56fd8b3f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-8c4d706cf2e88507">MSN 的两轴 Product-Key Memory 如何增加参数容量而只读取少量知识？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amsn">MSN: A Memory-based Sparse Activation Scaling Framework for Large-scale Industrial Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin Search</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>把键拆成两个轴后，一个槽位由两轴键的组合确定，组合空间可以很大。查询按两轴相似度的和寻找高分组合，只读取少量对应值，再通过 gate 与稠密主干融合。存储容量因此不必全部参与每次前向计算；效果仍依赖路由能否命中有用槽位，未激活的参数不会自动提供帮助。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两组各一百个键可组合出一万个槽位，但一次请求只取最相关的四个。像从有两层索引的资料柜查少数文件，而不是把一万个文件全部读一遍。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.07526">原论文</a> · <a href="../../../../reproductions/2602.07526-msn/">实现解读</a> · <a href="#qa-8c4d706cf2e88507">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tokenmixer-large" data-paper-title="TokenMixer-Large: Scaling Up Large Ranking Models in Industrial Recommenders" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TokenMixer-Large: Scaling Up Large Ranking Models in Industrial Recommenders 搜广推与 LLM 应用 ByteDance 2026-02-06 TokenMixer-Large 将候选与多域特征 token 先无参数 mixing，再分别做 head-wise SwiGLU，revert 后执行 token-wise SwiGLU；深层网络加入间隔残差和中间监督，使推荐精排能够稳定扩容。 复现保真度：完整核心链路复现。复现保真度：完整核心链路复现。主干、interval residual、中层辅助损失均真实训练，仅缩小规模。MovieLens 100K 上 TokenMixer-Large 与 rankmixer_dense 使用相同维度、层数、负采样和训练步数。  ranking token-mixing scaling 搜广推 用户历史与排序骨干 TokenMixer-Large 为什么在无参数 mixing 后做 head-wise SwiGLU，revert 后还要 token-wise SwiGLU？ mixing 重排特征通道，让 head 视角看到跨 token 的组合，head-wise 非线性先学习这些组合；revert 恢复 token 布局后，token-wise 变换再处理各位置内部表示。两种轴上的学习互补，间隔残差与中间监督支持深层训练。无参数混合只负责搬运信息，真正可学习交互来自其后的网络。 示意：把多个字段的通道重新分组，先学习“价格与消费偏好”等跨字段组合，再放回原布局做逐 token 处理。只有重排而没有后续非线性，不会凭空学会这些关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-tokenmixer-large-095f089c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-9a0857a64a43674f">TokenMixer-Large 为什么在无参数 mixing 后做 head-wise SwiGLU，revert 后还要 token-wise SwiGLU？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atokenmixer-large">TokenMixer-Large: Scaling Up Large Ranking Models in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>mixing 重排特征通道，让 head 视角看到跨 token 的组合，head-wise 非线性先学习这些组合；revert 恢复 token 布局后，token-wise 变换再处理各位置内部表示。两种轴上的学习互补，间隔残差与中间监督支持深层训练。无参数混合只负责搬运信息，真正可学习交互来自其后的网络。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把多个字段的通道重新分组，先学习“价格与消费偏好”等跨字段组合，再放回原布局做逐 token 处理。只有重排而没有后续非线性，不会凭空学会这些关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.06563">原论文</a> · <a href="../../../../reproductions/2602.06563-tokenmixer-large/">实现解读</a> · <a href="#qa-9a0857a64a43674f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:zenith" data-paper-title="Zenith: Scaling up Ranking Models for Billion-scale Livestreaming Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Zenith: Scaling up Ranking Models for Billion-scale Livestreaming Recommendation 搜广推与 LLM 应用 North Carolina State University 2026-01-29 Token Fusion 将大量异构稀疏特征压成少量高维 Prime Tokens，RSA/TMHSA 保持 token 差异；TSwiGLU/TSMoE 对每个 token 独立增强，改善模型规模与计算量的 scaling law。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04623，相对变化 -14.40%。本地代理目标与论文生产任务不同，不能外推线上 lift。  ranking-network scaling-law feature-interaction 搜广推 用户历史与排序骨干 Zenith 为什么先把异构稀疏特征融合成少量高维 Prime Tokens，再做 token 专属增强？ 大量短 token 会放大交互开销，Token Fusion 把特征压成少量更宽的表示，重新分配 token 数与通道容量。RSA/TMHSA 维持不同 token 的差异，专属 SwiGLU 或 MoE 再提供针对性非线性，避免压缩后都趋同。压缩可能损失细节，扩宽与专属参数是否值得需按同计算预算验证。 示意：原来一百个细字段逐对交互，先融合为少数宽 token 后可减少注意力位置数；但还要让用户与商品等角色保持差异，否则只得到几份相似的大向量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-zenith-6db3b2a2" class="ar-learning-paper-anchor"></span>
<h2 id="qa-cc81feea6d61f783">Zenith 为什么先把异构稀疏特征融合成少量高维 Prime Tokens，再做 token 专属增强？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Azenith">Zenith: Scaling up Ranking Models for Billion-scale Livestreaming Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · North Carolina State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>大量短 token 会放大交互开销，Token Fusion 把特征压成少量更宽的表示，重新分配 token 数与通道容量。RSA/TMHSA 维持不同 token 的差异，专属 SwiGLU 或 MoE 再提供针对性非线性，避免压缩后都趋同。压缩可能损失细节，扩宽与专属参数是否值得需按同计算预算验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>原来一百个细字段逐对交互，先融合为少数宽 token 后可减少注意力位置数；但还要让用户与商品等角色保持差异，否则只得到几份相似的大向量。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.21285">原论文</a> · <a href="../../../../reproductions/2601.21285-zenith/">实现解读</a> · <a href="#qa-cc81feea6d61f783">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:llatte" data-paper-title="LLaTTE: Scaling Laws for Multi-Stage Sequence Modeling in Large-Scale Ads Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="LLaTTE: Scaling Laws for Multi-Stage Sequence Modeling in Large-Scale Ads Recommendation 搜广推与 LLM 应用 Meta 2026-01-27 工业推荐序列模型同时受训练 FLOPs、在线延迟和跨阶段信息损失约束：直接把历史拉长会让在线 ranking 代价失控，只扩大下游模型又无法恢复上游丢掉的长期兴趣。LLaTTE 将 scaling 拆成两级：上游异步大序列模型读取超长、多源历史并缓存 2,048 维 user representation； Fidelity: 核心机制复现。当前实现实际运行 BERT-tiny semantic features、MLA 上游 latent、target-aware 在线 attention 与 DHEN 门控；未复刻 Meta 私有广告特征和异步生产 serving。本地对照口径：基线是相同 ID/语义 embedding 的 short online sequence；实验组增加 MLA upstream、候选感知 online attention 与 DHEN，NDCG@10 +49.81%。训练预算一致，不是相对 DIN。   搜广推 用户历史与排序骨干 LLaTTE已经缓存大模型用户表示，为什么下游仍要读取短历史并做候选感知attention？ 上游长历史编码能异步承载较大计算，却存在刷新间隔和压缩损失；在线短序列补充最新行为，候选query再选择对当前打分有用的证据。上下游因此各承担稳定知识与实时相关性，而不是把一个缓存向量当全部用户状态。上游指标改善是否有效迁移到下游，需要单独测量而非默认全额保留。 示意：昨夜缓存记录长期摄影兴趣，用户刚开始搜索旅行背包；在线近期序列应反映新意图，再结合当前候选读取相关知识，而不只复用昨夜的固定结论。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-llatte-05036174" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b35ec683629a5330">LLaTTE已经缓存大模型用户表示，为什么下游仍要读取短历史并做候选感知attention？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Allatte">LLaTTE: Scaling Laws for Multi-Stage Sequence Modeling in Large-Scale Ads Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>上游长历史编码能异步承载较大计算，却存在刷新间隔和压缩损失；在线短序列补充最新行为，候选query再选择对当前打分有用的证据。上下游因此各承担稳定知识与实时相关性，而不是把一个缓存向量当全部用户状态。上游指标改善是否有效迁移到下游，需要单独测量而非默认全额保留。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>昨夜缓存记录长期摄影兴趣，用户刚开始搜索旅行背包；在线近期序列应反映新意图，再结合当前候选读取相关知识，而不只复用昨夜的固定结论。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.20083">原论文</a> · <a href="../../../../reproductions/2601.20083-llatte/">实现解读</a> · <a href="#qa-b35ec683629a5330">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sparsectr" data-paper-title="Unleashing the Potential of Sparse Attention on Long-term Behaviors for CTR Prediction" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Unleashing the Potential of Sparse Attention on Long-term Behaviors for CTR Prediction 搜广推与 LLM 应用 Institute of Software, Chinese Academy of Sciences 2026-01-25 TimeChunking 按个体行为时间间隔自适应分块；EvoAttention 并联全局 chunk、兴趣转移和局部窗口三路注意力，RelTemporal 再注入时间间隔、小时和周末相对偏置。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05519，相对变化 +2.19%。本地代理目标与论文生产任务不同，不能外推线上 lift。  ctr-prediction long-sequence sparse-attention 搜广推 用户历史与排序骨干 SparseCTR 为什么按个体行为间隔自适应分块，还并联全局、转移和局部三路注意力？ 相同条数的行为可能跨几分钟也可能跨几个月，固定窗口会混淆会话边界。时间分块先组织个体节奏，三路分别提取长期概况、兴趣迁移和近邻细节，相对时间偏置再表达间隔与周期。它把时间结构写进信息流，而非只加一个绝对位置；分块与融合仍需避免压掉突发或稀疏兴趣。 示意：用户周末集中浏览十件家具，隔一个月又买耗材。按时间间隔可把两段分开，局部路保留同次采购细节，转移路学习从装修到补充用品的变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-sparsectr-7769ddba" class="ar-learning-paper-anchor"></span>
<h2 id="qa-132c0a2e3ff407c5">SparseCTR 为什么按个体行为间隔自适应分块，还并联全局、转移和局部三路注意力？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asparsectr">Unleashing the Potential of Sparse Attention on Long-term Behaviors for CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Software, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相同条数的行为可能跨几分钟也可能跨几个月，固定窗口会混淆会话边界。时间分块先组织个体节奏，三路分别提取长期概况、兴趣迁移和近邻细节，相对时间偏置再表达间隔与周期。它把时间结构写进信息流，而非只加一个绝对位置；分块与融合仍需避免压掉突发或稀疏兴趣。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户周末集中浏览十件家具，隔一个月又买耗材。按时间间隔可把两段分开，局部路保留同次采购细节，转移路学习从装修到补充用品的变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.17836">原论文</a> · <a href="../../../../reproductions/2601.17836-sparsectr/">实现解读</a> · <a href="#qa-132c0a2e3ff407c5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hyformer" data-paper-title="HyFormer: Revisiting the Roles of Sequence Modeling and Feature Interaction in CTR Prediction" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="HyFormer: Revisiting the Roles of Sequence Modeling and Feature Interaction in CTR Prediction 搜广推与 LLM 应用 ByteDance / Douyin Search 2026-01-19 LONGER→RankMixer 类串行架构先压缩长序列、再做异构字段交互，信息流晚且单向。HyFormer 从非序列字段和 sequence mean 生成 Global Queries，每层用 queries cross-attend 当前 sequence K/V，再把 decoded queries 与非序列 tokens 做 RankMixer-style boosting；boosted queries 进入下一层重新解码，实现双向、逐层共同演化。 Fidelity: 完整核心链路复现。本地逐层执行 Query Generation、Query Decoding 和 Query Boosting；私有多行为序列替换为 MovieLens 单序列。本地对照口径：基线是独立 sequence Transformer+dense MLP 的 Late Fusion；实验组是 HyFormer；NDCG@10 从 0.0048 升至 0.0116（+143.77%），head share 同时 +30.90pt。这是 query co-evolution 架构消融，不是相对 DIN。   搜广推 用户历史与排序骨干 HyFormer为什么每层读完历史后还要做Query Boosting，再返回下一层读取？ 若先把历史压成摘要再做字段交叉，字段信息无法改变下一次取证方向。HyFormer交替读取序列与混合非序列token，使刚得到的历史证据参与字段交互，再由增强query重新查询历史。这里共同演化的是紧凑query与字段表示，不应理解为每个候选都必须改写整段原始历史。 示意：第一层发现用户看过户外内容，结合雨天和商品材质后，下一层query可更关注防水装备；一次性摘要再接MLP就难把这条新问题反馈给历史读取。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-hyformer-d0fa9291" class="ar-learning-paper-anchor"></span>
<h2 id="qa-64a45769bae35220">HyFormer为什么每层读完历史后还要做Query Boosting，再返回下一层读取？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahyformer">HyFormer: Revisiting the Roles of Sequence Modeling and Feature Interaction in CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin Search</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若先把历史压成摘要再做字段交叉，字段信息无法改变下一次取证方向。HyFormer交替读取序列与混合非序列token，使刚得到的历史证据参与字段交互，再由增强query重新查询历史。这里共同演化的是紧凑query与字段表示，不应理解为每个候选都必须改写整段原始历史。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第一层发现用户看过户外内容，结合雨天和商品材质后，下一层query可更关注防水装备；一次性摘要再接MLP就难把这条新问题反馈给历史读取。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.12681">原论文</a> · <a href="../../../../reproductions/2601.12681-hyformer/">实现解读</a> · <a href="#qa-64a45769bae35220">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onetrans" data-paper-title="OneTrans: Unified Feature Interaction and Sequence Modeling with One Transformer in Industrial Recommender" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OneTrans: Unified Feature Interaction and Sequence Modeling with One Transformer in Industrial Recommender 搜广推与 LLM 应用 ByteDance 2025-10-30 OneTrans 把行为 S-tokens 放在异构 NS-tokens 前，使用一个 causal Transformer 同时完成序列建模和字段交互。语义同质的 S-token 共享 QKV/FFN；每个 NS-token 拥有独立参数。因果顺序使 NS-token 能读取完整历史，pyramid stack 逐层只保留近期 S queries。线上用 cross-candidate/cross-request KV cache 复用 S-side 计算。 Fidelity: 完整核心链路复现。本地执行 unified S/NS tokenization、mixed QKV、mixed FFN、causal attention 和 pyramid tail pruning；持久化跨请求 KV 服务系统未复刻。本地对照口径：基线是独立 sequence encoder 后与 candidate 交互的 Encode-then-Interact；实验组是 OneTrans；NDCG@10 从 0.0069 升至 0.0154（+123.58%），但 head share 达 92%。这是统一架构相对 stacked 架构的消融，不是相对 DIN。   搜广推 用户历史与排序骨干 OneTrans 为什么把行为 token 放在非序列字段之前，并让两类 token 使用不同参数共享方式？ 因果顺序允许后面的字段读取此前全部行为，同时行为状态不依赖后置候选字段，因此可复用用户侧计算。行为 token 语义同质，适合共享 QKV 与 FFN；异构字段含义不同，使用位置专属参数保留差异。金字塔逐层缩短行为查询降低后层开销，但缓存复用仍受时间窗口、参数版本和依赖关系约束。 示意：历史点击序列先编码，后面再放用户属性和候选商品字段。换一个候选时，之前的行为表示可复用；候选字段读取同一历史，却通过自己的参数解释价格与品类。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-onetrans-113b41b8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-3a6324bb9639c16d">OneTrans 为什么把行为 token 放在非序列字段之前，并让两类 token 使用不同参数共享方式？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonetrans">OneTrans: Unified Feature Interaction and Sequence Modeling with One Transformer in Industrial Recommender</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>因果顺序允许后面的字段读取此前全部行为，同时行为状态不依赖后置候选字段，因此可复用用户侧计算。行为 token 语义同质，适合共享 QKV 与 FFN；异构字段含义不同，使用位置专属参数保留差异。金字塔逐层缩短行为查询降低后层开销，但缓存复用仍受时间窗口、参数版本和依赖关系约束。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>历史点击序列先编码，后面再放用户属性和候选商品字段。换一个候选时，之前的行为表示可复用；候选字段读取同一历史，却通过自己的参数解释价格与品类。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.26104">原论文</a> · <a href="../../../../reproductions/2510.26104-onetrans/">实现解读</a> · <a href="#qa-3a6324bb9639c16d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onepiece" data-paper-title="OnePiece: Bringing Context Engineering and Reasoning to Industrial Cascade Ranking" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OnePiece: Bringing Context Engineering and Reasoning to Industrial Cascade Ranking 搜广推与 LLM 应用 Shopee 2025-09-22 把上下文 token、块级 latent reasoning 与递进多任务目标合并到级联排序器，让召回、点击和价值任务共享表示但分阶段收敛。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 onepiece 核心机制；相对 NDCG@10 +22.87%。  ranking retrieval latent-reasoning multi-task 搜广推 用户历史与排序骨干 OnePiece 的块级潜在推理与递进多任务权重，为什么比一次性相加所有任务损失更有区别？ 块级更新让上下文条件下的中间状态经过多步残差变换，而不是只在末端接多个头。递进权重再控制各训练阶段由哪些任务主导，使共享表示逐步适应召回、点击和价值目标。关键在更新路径与收敛顺序，不是仅增加任务数；本地代理机制不能证明潜在状态具有可验证的语言推理过程。 示意：先让表示学会区分相关与无关商品，再逐渐提高购买价值目标权重。相较从第一步就同时强推所有目标，这种安排意在减少早期难任务对基础相关性学习的干扰。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-onepiece-1b14efa1" class="ar-learning-paper-anchor"></span>
<h2 id="qa-10aa9ef73312afbd">OnePiece 的块级潜在推理与递进多任务权重，为什么比一次性相加所有任务损失更有区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonepiece">OnePiece: Bringing Context Engineering and Reasoning to Industrial Cascade Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shopee</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>块级更新让上下文条件下的中间状态经过多步残差变换，而不是只在末端接多个头。递进权重再控制各训练阶段由哪些任务主导，使共享表示逐步适应召回、点击和价值目标。关键在更新路径与收敛顺序，不是仅增加任务数；本地代理机制不能证明潜在状态具有可验证的语言推理过程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先让表示学会区分相关与无关商品，再逐渐提高购买价值目标权重。相较从第一步就同时强推所有目标，这种安排意在减少早期难任务对基础相关性学习的干扰。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2509.18091">原论文</a> · <a href="../../../../reproductions/2509.18091-onepiece/">实现解读</a> · <a href="#qa-10aa9ef73312afbd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:argus" data-paper-title="Scaling Recommender Transformers to One Billion Parameters" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Scaling Recommender Transformers to One Billion Parameters 搜广推与 LLM 应用 Yandex 2025-07-21 直接 next-item 预测把“用户会怎样反馈”和“会消费哪个 item”纠缠。ARGUS 先预测 feedback token，再以其条件化 next-item，使多种反馈共享序列主干并获得更好的 scaling。 两种口径均未验证收益。Fidelity: 核心机制复现。matched Transformer 中实际执行 feedback-first、next-item-second 分解；未复刻十亿参数规模与私有音乐反馈。本地对照口径：统一跨模型基线是 DIN，ARGUS NDCG@10 相对 DIN -4.12%；内部 next-item-only 基线加入 feedback decomposition 后 -20.95%。两种口径均未验证收益。统一为 180 users/280 items 后，DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；  long-sequence transformer multi-task 搜广推 用户历史与排序骨干 ARGUS先预测feedback token再预测物品，和直接预测下一个物品有何差别？ 直接next-item把消费对象与反馈类型混在一个目标里。ARGUS将联合概率拆为先判断用户会产生何种反馈，再在该条件下选择物品，使多种反馈共享主干却保留条件差异；推理时预测反馈不能偷读真实未来行为。本地对应消融出现负结果，因此不能把这种分解视为必然更优。 示意：同一历史既可能接着长看纪录片，也可能快速划走短视频；先区分预期反馈，再选对象，表达的是联合行为，而不是只猜物品名字。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-argus-3c7d662d" class="ar-learning-paper-anchor"></span>
<h2 id="qa-34e00691c873ae6a">ARGUS先预测feedback token再预测物品，和直接预测下一个物品有何差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aargus">Scaling Recommender Transformers to One Billion Parameters</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Yandex</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直接next-item把消费对象与反馈类型混在一个目标里。ARGUS将联合概率拆为先判断用户会产生何种反馈，再在该条件下选择物品，使多种反馈共享主干却保留条件差异；推理时预测反馈不能偷读真实未来行为。本地对应消融出现负结果，因此不能把这种分解视为必然更优。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一历史既可能接着长看纪录片，也可能快速划走短视频；先区分预期反馈，再选对象，表达的是联合行为，而不是只猜物品名字。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.15994">原论文</a> · <a href="../../../../reproductions/2507.15994-argus/">实现解读</a> · <a href="#qa-34e00691c873ae6a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rankmixer" data-paper-title="RankMixer: Scaling Up Ranking Models in Industrial Recommenders" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="RankMixer: Scaling Up Ranking Models in Industrial Recommenders 搜广推与 LLM 应用 ByteDance / Douyin 2025-07-21 RankMixer 用固定的多头 TokenMix 让不同 feature token 的分量相遇，再由各 token 独立的 FFN 学习组合。这里替换的是异构特征交互模块；上游长序列模块仍可使用 attention。 本地只有 seed 42 的 smoke。Shared FFN 与 Dense per-token 都含 TokenMix，且参数量不同，不能据此验证 TokenMix 优于 attention。Sparse 没有追平 Dense，当前路由与原文双 router DTSI 仍有差异。 TokenMix 没有可训练参数，整个模型为什么仍能学习特征关系？  搜广推 用户历史与排序骨干 固定TokenMix没有学习权重，为什么后面的独立FFN仍能学到跨字段交互？ TokenMix先按head切开每个输入token，再把各输入的同号片段拼成新token，让不同字段的信号进入同一个非线性FFN。学习发生在混合后的专属变换中，而非动态相似度权重；原文取head数等于token数并要求维度可整除。它替换字段交互，不意味着序列模块也应取消attention。 示意：用户、商品和场景各拆三块，同号块被送到一起；FFN可联合判断其中的年龄、品类和时段关系，固定搬运本身不需要先计算相似度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-rankmixer-298d1226" class="ar-learning-paper-anchor"></span>
<h2 id="qa-a18a983529fe37d7">固定TokenMix没有学习权重，为什么后面的独立FFN仍能学到跨字段交互？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arankmixer">RankMixer: Scaling Up Ranking Models in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>TokenMix先按head切开每个输入token，再把各输入的同号片段拼成新token，让不同字段的信号进入同一个非线性FFN。学习发生在混合后的专属变换中，而非动态相似度权重；原文取head数等于token数并要求维度可整除。它替换字段交互，不意味着序列模块也应取消attention。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户、商品和场景各拆三块，同号块被送到一起；FFN可联合判断其中的年龄、品类和时段关系，固定搬运本身不需要先计算相似度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.15551">原论文</a> · <a href="../../../../reproductions/2507.15551-rankmixer/">实现解读</a> · <a href="../../../002-rankmixer-tokenmix/">阅读精选对比</a> · <a href="#qa-a18a983529fe37d7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rankmixer" data-paper-title="RankMixer: Scaling Up Ranking Models in Industrial Recommenders" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="RankMixer: Scaling Up Ranking Models in Industrial Recommenders 搜广推与 LLM 应用 ByteDance / Douyin 2025-07-21 RankMixer 用固定的多头 TokenMix 让不同 feature token 的分量相遇，再由各 token 独立的 FFN 学习组合。这里替换的是异构特征交互模块；上游长序列模块仍可使用 attention。 本地只有 seed 42 的 smoke。Shared FFN 与 Dense per-token 都含 TokenMix，且参数量不同，不能据此验证 TokenMix 优于 attention。Sparse 没有追平 Dense，当前路由与原文双 router DTSI 仍有差异。 TokenMix 没有可训练参数，整个模型为什么仍能学习特征关系？  搜广推 用户历史与排序骨干 RankMixer 为什么设置 head 数 H 等于 token 数 T，并要求隐藏维度可整除？ 每个输入 token 被等分为 H 个长度 D/H 的片段，混合后得到 H 个长度 TD/H 的新 token。取 H=T 才恢复 T×D 形状，能与原输入直接做残差相加；D 也必须能被 H 整除。这里是张量布局条件，不是注意力头的语义约束，随意换 token 数却保留原 reshape 会改变或破坏结构。 示意：四个64维 token 各拆四份，每份16维；同号四份拼接后仍是四个64维 token。若改成三个 head，64无法等分，原样重排和残差就不成立。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="qa-67c000ac06ff074b">RankMixer 为什么设置 head 数 H 等于 token 数 T，并要求隐藏维度可整除？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arankmixer">RankMixer: Scaling Up Ranking Models in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每个输入 token 被等分为 H 个长度 D/H 的片段，混合后得到 H 个长度 TD/H 的新 token。取 H=T 才恢复 T×D 形状，能与原输入直接做残差相加；D 也必须能被 H 整除。这里是张量布局条件，不是注意力头的语义约束，随意换 token 数却保留原 reshape 会改变或破坏结构。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>四个64维 token 各拆四份，每份16维；同号四份拼接后仍是四个64维 token。若改成三个 head，64无法等分，原样重排和残差就不成立。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.15551">原论文</a> · <a href="../../../../reproductions/2507.15551-rankmixer/">实现解读</a> · <a href="../../../002-rankmixer-tokenmix/">阅读精选对比</a> · <a href="#qa-67c000ac06ff074b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rankmixer" data-paper-title="RankMixer: Scaling Up Ranking Models in Industrial Recommenders" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="RankMixer: Scaling Up Ranking Models in Industrial Recommenders 搜广推与 LLM 应用 ByteDance / Douyin 2025-07-21 RankMixer 用固定的多头 TokenMix 让不同 feature token 的分量相遇，再由各 token 独立的 FFN 学习组合。这里替换的是异构特征交互模块；上游长序列模块仍可使用 attention。 本地只有 seed 42 的 smoke。Shared FFN 与 Dense per-token 都含 TokenMix，且参数量不同，不能据此验证 TokenMix 优于 attention。Sparse 没有追平 Dense，当前路由与原文双 router DTSI 仍有差异。 TokenMix 没有可训练参数，整个模型为什么仍能学习特征关系？  搜广推 用户历史与排序骨干 RankMixer 的 ReLU 路由和双路由 DTSI 分别解决什么问题，为什么只做稀疏 top-k 不够？ ReLU 加稀疏正则允许不同 token 激活不同数量专家，处理固定 top-k 分配预算过于僵硬的问题。DTSI 另设训练与推理路由，稀疏正则只加在推理路由上，使专家训练不因稀疏选择长期饥饿。两者分别控制动态激活和专家训练覆盖；本地稀疏路径尚不能视作原文双路由方案的等价验证。 示意：信息复杂的 token 可用更多专家，简单 token 少用；训练时仍给较少被选专家足够学习机会。若从头只更新固定少数专家，其余专家即使参数很多也可能一直没有学好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="qa-473b102f64b8ecd6">RankMixer 的 ReLU 路由和双路由 DTSI 分别解决什么问题，为什么只做稀疏 top-k 不够？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arankmixer">RankMixer: Scaling Up Ranking Models in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>ReLU 加稀疏正则允许不同 token 激活不同数量专家，处理固定 top-k 分配预算过于僵硬的问题。DTSI 另设训练与推理路由，稀疏正则只加在推理路由上，使专家训练不因稀疏选择长期饥饿。两者分别控制动态激活和专家训练覆盖；本地稀疏路径尚不能视作原文双路由方案的等价验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>信息复杂的 token 可用更多专家，简单 token 少用；训练时仍给较少被选专家足够学习机会。若从头只更新固定少数专家，其余专家即使参数很多也可能一直没有学好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.15551">原论文</a> · <a href="../../../../reproductions/2507.15551-rankmixer/">实现解读</a> · <a href="../../../002-rankmixer-tokenmix/">阅读精选对比</a> · <a href="#qa-473b102f64b8ecd6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pinfm" data-paper-title="PinFM: Foundation Model for User Activity Sequences at a Billion-scale Visual Discovery Platform" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="PinFM: Foundation Model for User Activity Sequences at a Billion-scale Visual Discovery Platform 搜广推与 LLM 应用 Pinterest 2025-07-17 PinFM 把“先在跨场景用户行为上预训练，再接入各排序模型微调”的 Foundation Model 范式带到工业推荐。decoder-only backbone 学习 next/multi/future token；下游把候选追加到用户序列做 early fusion。DCAT 利用同一请求的候选共享用户历史，把 context self-attention 只算一次，然后让候选对缓存的 context KV 做 cross-attention。 保真度：核心机制复现。保真度：核心机制复现。NTL/MTL/FTL 对比预训练、预训练后下游微调、candidate early fusion、Candidate ID Randomization、backbone 低学习率和 DCAT 均实际执行；省略 Pinterest 多 action/surface 语料、fresh-item age dropout、分布式 20B embedding、int4 与 Triton kernel。本地对照口径：基线是 scratch DCAT；实验组是预训练后微调的 PinFM；   搜广推 用户历史与排序骨干 PinFM 的 DCAT 为什么能保留候选早融合，同时避免每个候选重算用户上下文？ 早融合让候选在模型内部与历史交互，但把同一用户历史为每个候选重复展开会浪费大量计算。DCAT 先对去重后的上下文做一次自注意力并缓存各层 K/V，再让候选侧查询读取这些状态。复用的前提是上下文计算不依赖被替换的候选；预训练收益与这种服务优化是不同问题，本地负结果也需保留。 示意：一位用户有五百条历史、待评一百个候选。先算一份历史记忆，再让每个候选读取相关部分，比复制一百份历史各算一次更省，而候选仍能在层内接触历史。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-pinfm-c653f7d8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-4eaf16c90d354ace">PinFM 的 DCAT 为什么能保留候选早融合，同时避免每个候选重算用户上下文？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apinfm">PinFM: Foundation Model for User Activity Sequences at a Billion-scale Visual Discovery Platform</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>早融合让候选在模型内部与历史交互，但把同一用户历史为每个候选重复展开会浪费大量计算。DCAT 先对去重后的上下文做一次自注意力并缓存各层 K/V，再让候选侧查询读取这些状态。复用的前提是上下文计算不依赖被替换的候选；预训练收益与这种服务优化是不同问题，本地负结果也需保留。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一位用户有五百条历史、待评一百个候选。先算一份历史记忆，再让每个候选读取相关部分，比复制一百份历史各算一次更省，而候选仍能在层内接触历史。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.12704">原论文</a> · <a href="../../../../reproductions/2507.12704-pinfm/">实现解读</a> · <a href="#qa-4eaf16c90d354ace">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:transact-v2" data-paper-title="TransAct V2: Lifelong User Action Sequence Modeling on Pinterest Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TransAct V2: Lifelong User Action Sequence Modeling on Pinterest Recommendation 搜广推与 LLM 应用 Pinterest 2025-06-02 TransAct 主要建模约百条实时行为，容易忽略用户多年的长期兴趣。TransAct V2 从约条 lifelong 序列中按候选相似度取回相关行为，同时保留最近行为，再通过共享 Transformer 做 CTR 排序；额外的 Next Action Loss 迫使序列表征预测下一次正向互动。论文也包含 SKUT、request deduplication 等 serving 优化，本地复现聚焦模型链路。 保真度：核心机制复现。保真度：核心机制复现。候选锚定的长/短序列近邻检索、最近行为保留、early-fusion causal Transformer 和 Next Action Loss 均实际训练；MovieLens genre 替代 PinSage embedding，省略 Pinterest action/surface 字段、曝光日志负例及生产 Triton kernel。本地对照口径：基线是参数量匹配的 TransAct；实验组是 TransAct V2；NDCG@10 从 0.01277 升至 0.02460（+92.65%），head share 同时 +14.70pt。   搜广推 用户历史与排序骨干 TransAct V2 为什么候选检索终身历史时仍保留一段原样近期行为，并增加 Next Action Loss？ 相似度检索擅长找到与当前候选相关的旧事件，却可能遗漏刚形成但尚未显式相似的新意图。保留近期分支保证即时信号可见，再用共享 Transformer 融合检索片段。Next Action Loss 让状态直接学习下一正向互动，补充 CTR 监督；检索选不中的远期事件仍不可见，服务优化也需单独验证。 示意：候选是帐篷，旧露营浏览被检回，同时保留最近突然关注亲子出游的行为。辅助下一动作目标促使状态理解需求变化，而不只判断当前这次曝光是否点击。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-transact-v2-c124d4cb" class="ar-learning-paper-anchor"></span>
<h2 id="qa-38858cbd67f8f10d">TransAct V2 为什么候选检索终身历史时仍保留一段原样近期行为，并增加 Next Action Loss？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atransact-v2">TransAct V2: Lifelong User Action Sequence Modeling on Pinterest Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相似度检索擅长找到与当前候选相关的旧事件，却可能遗漏刚形成但尚未显式相似的新意图。保留近期分支保证即时信号可见，再用共享 Transformer 融合检索片段。Next Action Loss 让状态直接学习下一正向互动，补充 CTR 监督；检索选不中的远期事件仍不可见，服务优化也需单独验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>候选是帐篷，旧露营浏览被检回，同时保留最近突然关注亲子出游的行为。辅助下一动作目标促使状态理解需求变化，而不只判断当前这次曝光是否点击。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2506.02267">原论文</a> · <a href="../../../../reproductions/2506.02267-transact-v2/">实现解读</a> · <a href="#qa-38858cbd67f8f10d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:genrank" data-paper-title="Towards Large-scale Generative Ranking" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Towards Large-scale Generative Ranking 搜广推与 LLM 应用 Xiaohongshu 2025-05-07 HSTU 式排序把 item 与 action 交错为两倍长序列。GenRank 将 action 作为同一 item token 的监督/特征，并加入 position 与 time bias，在不丢掉多行为生成目标的前提下降低排序成本。 Fidelity: 完整核心链路复现。真实执行 item/action 交错基线、action-oriented 组织、位置/时间偏置、因果 Transformer 和 action 生成；缩小为 MovieLens 显式反馈。本地对照口径：基线是 item/action 交错序列模型；实验组是 GenRank action-oriented 组织；延迟 -25.66%，但 AUC -0.46%。这是序列组织的效率—效果对照，不是准确率提升，也不是相对 DIN。  generative-ranking action-modeling efficiency 搜广推 用户历史与排序骨干 GenRank把action并入item token，为什么能改变HSTU式排序的计算成本？ 交错item与action会增加序列位置，二次交互成本随长度显著增长。GenRank把同一行为的action作为item位置的特征或监督，保留多行为目标却减少独立token，并用位置与时间偏置补充结构。序列更短并不保证信息完全等价，本地效率改善同时伴随质量变化，需联合报告。 示意：十次行为原来对应二十个交错位置，合并后只保留十个item位置及其反馈信息；注意力矩阵变小，但仍要检验是否损失了某些反馈依赖。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-genrank-a86f2304" class="ar-learning-paper-anchor"></span>
<h2 id="qa-9b301295110c48a6">GenRank把action并入item token，为什么能改变HSTU式排序的计算成本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agenrank">Towards Large-scale Generative Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>交错item与action会增加序列位置，二次交互成本随长度显著增长。GenRank把同一行为的action作为item位置的特征或监督，保留多行为目标却减少独立token，并用位置与时间偏置补充结构。序列更短并不保证信息完全等价，本地效率改善同时伴随质量变化，需联合报告。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>十次行为原来对应二十个交错位置，合并后只保留十个item位置及其反馈信息；注意力矩阵变小，但仍要检验是否损失了某些反馈依赖。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.04180">原论文</a> · <a href="../../../../reproductions/2505.04180-genrank/">实现解读</a> · <a href="#qa-9b301295110c48a6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:longer" data-paper-title="LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders 搜广推与 LLM 应用 ByteDance / Douyin 2025-05-07 LONGER 先以 Token Merge 合并相邻行为，首层用少量 Query 读取长 K/V，后续沿短序列继续 self-attention。学习重点是区分合并输入和压缩查询这两步。 当前本地 encode 拼接 global/merged/recent 后做单层 self-attention，尚缺论文的首层短 Q/长 K/V hybrid attention 路径和 causal mask。历史实验不作为该核心路径或生产缓存的验证。 首层之后，模型还能否直接重新读取完整长 K/V？  搜广推 用户历史与排序骨干 LONGER把长历史留给K/V后，后续层还要重复更新整段历史吗？ 论文首层用global与近期token组成较短Q，读取合并后的长历史K/V；输出长度跟Q走，后续层只在这组短状态上做self-attention。压缩因此发生在层间传播状态，而非先完全截掉远期证据。本地同名实现尚未完整保留这条首层路径，历史指标不能证明它已被验证。 示意：长历史像一本资料册，首层让几张近期问题卡查阅全册；后续只反复整理这些问题卡，而不是每层重新改写整本资料册。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-longer-50bd52b2" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b94e636f79ea884b">LONGER把长历史留给K/V后，后续层还要重复更新整段历史吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alonger">LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>论文首层用global与近期token组成较短Q，读取合并后的长历史K/V；输出长度跟Q走，后续层只在这组短状态上做self-attention。压缩因此发生在层间传播状态，而非先完全截掉远期证据。本地同名实现尚未完整保留这条首层路径，历史指标不能证明它已被验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>长历史像一本资料册，首层让几张近期问题卡查阅全册；后续只反复整理这些问题卡，而不是每层重新改写整本资料册。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.04421">原论文</a> · <a href="../../../../reproductions/2505.04421-longer/">实现解读</a> · <a href="../../../001-hstu-longer-slimper/">阅读精选对比</a> · <a href="#qa-b94e636f79ea884b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:longer" data-paper-title="LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders 搜广推与 LLM 应用 ByteDance / Douyin 2025-05-07 LONGER 先以 Token Merge 合并相邻行为，首层用少量 Query 读取长 K/V，后续沿短序列继续 self-attention。学习重点是区分合并输入和压缩查询这两步。 当前本地 encode 拼接 global/merged/recent 后做单层 self-attention，尚缺论文的首层短 Q/长 K/V hybrid attention 路径和 causal mask。历史实验不作为该核心路径或生产缓存的验证。 首层之后，模型还能否直接重新读取完整长 K/V？  搜广推 用户历史与排序骨干 LONGER 每 K 个 token 合并一次，为什么 K 更大不一定更省总 FLOPs？ 原文§3.4同时缩短序列并增宽合并表示：总 FLOPs 比例含随 K 增长的投影项和随 K 下降的注意力项。因此合并减少位置数，却会提高通道变换与参数成本，存在平衡点。InnerTrans 还用于补足组内交互；不能把这套设计等同于固定维度均值池化，也不能断言压缩越强效果越好。 示意：四条行为拼成一个更宽 token，位置更少但后续矩阵更大；再合并到八条可能让投影成本反弹。像减少箱子数量，却把每箱变得更大更难搬。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="qa-f90aa5aa39428720">LONGER 每 K 个 token 合并一次，为什么 K 更大不一定更省总 FLOPs？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alonger">LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原文§3.4同时缩短序列并增宽合并表示：总 FLOPs 比例含随 K 增长的投影项和随 K 下降的注意力项。因此合并减少位置数，却会提高通道变换与参数成本，存在平衡点。InnerTrans 还用于补足组内交互；不能把这套设计等同于固定维度均值池化，也不能断言压缩越强效果越好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>四条行为拼成一个更宽 token，位置更少但后续矩阵更大；再合并到八条可能让投影成本反弹。像减少箱子数量，却把每箱变得更大更难搬。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.04421">原论文</a> · <a href="../../../../reproductions/2505.04421-longer/">实现解读</a> · <a href="../../../001-hstu-longer-slimper/">阅读精选对比</a> · <a href="#qa-f90aa5aa39428720">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:longer" data-paper-title="LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders 搜广推与 LLM 应用 ByteDance / Douyin 2025-05-07 LONGER 先以 Token Merge 合并相邻行为，首层用少量 Query 读取长 K/V，后续沿短序列继续 self-attention。学习重点是区分合并输入和压缩查询这两步。 当前本地 encode 拼接 global/merged/recent 后做单层 self-attention，尚缺论文的首层短 Q/长 K/V hybrid attention 路径和 causal mask。历史实验不作为该核心路径或生产缓存的验证。 首层之后，模型还能否直接重新读取完整长 K/V？  搜广推 用户历史与排序骨干 LONGER 的 global token 可含候选信息，为什么仍能使用用户 KV cache？ 原文§3.5.2与§3.6.3用掩码确保用户序列不读取候选特有 global token，用户 K/V 才能先计算并跨候选复用。候选 global token 再与缓存历史交互，相关输出仍逐候选生成。global 代表可汇聚全局信息的角色，不代表所有 global token 都候选无关；缓存资格取决于实际依赖路径。 示意：两件商品共用用户浏览序列 K/V，但各有自己的候选 global token 查询历史。若先让用户序列吸收了商品甲信息，再给商品乙复用，就破坏了共享条件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="qa-906a6ef0a4addaf4">LONGER 的 global token 可含候选信息，为什么仍能使用用户 KV cache？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alonger">LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原文§3.5.2与§3.6.3用掩码确保用户序列不读取候选特有 global token，用户 K/V 才能先计算并跨候选复用。候选 global token 再与缓存历史交互，相关输出仍逐候选生成。global 代表可汇聚全局信息的角色，不代表所有 global token 都候选无关；缓存资格取决于实际依赖路径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两件商品共用用户浏览序列 K/V，但各有自己的候选 global token 查询历史。若先让用户序列吸收了商品甲信息，再给商品乙复用，就破坏了共享条件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.04421">原论文</a> · <a href="../../../../reproductions/2505.04421-longer/">实现解读</a> · <a href="../../../001-hstu-longer-slimper/">阅读精选对比</a> · <a href="#qa-906a6ef0a4addaf4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:fuxi-alpha" data-paper-title="FuXi-α: Scaling Recommendation Model with Feature Interaction Enhanced Transformer" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="FuXi-α: Scaling Recommendation Model with Feature Interaction Enhanced Transformer 搜广推与 LLM 应用 Huawei / USTC 2025-02-05 常规推荐 Transformer 扩参时容易受浅层特征交互限制。FuXi-α 用多个自适应交互通道建模不同关系，再以 multi-stage FFN 逐级融合。 Fidelity: 核心机制复现。实际执行时间、语义和流行度多通道注意力及分阶段交互门控。本地是小型数值通道实现，不包含论文十亿级 scaling、华为音乐私有连续特征与分布式训练。本地对照口径：相对单通道注意力基线，实验组 NDCG@10 -4.25%。  ranking transformer feature-interaction scaling 搜广推 用户历史与排序骨干 FuXi-α为什么用多个交互通道和逐级FFN，而不是只把单路attention堆得更宽？ 单一路径可能把不同字段关系挤进同一表示，增加宽度未必改善交互组织。多个自适应通道先表达不同关系，multi-stage FFN再逐级融合，使参数扩展与特征交叉相配合。但通道数量增加也可能重复建模，不能因参数更多就宣布更有效，需与单通道及同预算配置比较。 示意：用户—商品、场景—商品、行为—候选的关系可先由不同通道捕获，再逐步组合；若所有通道都学成相同注意力，扩大它们只会增加成本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-fuxi-alpha-d5540b18" class="ar-learning-paper-anchor"></span>
<h2 id="qa-034c54f6610a2785">FuXi-α为什么用多个交互通道和逐级FFN，而不是只把单路attention堆得更宽？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Afuxi-alpha">FuXi-α: Scaling Recommendation Model with Feature Interaction Enhanced Transformer</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei / USTC</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单一路径可能把不同字段关系挤进同一表示，增加宽度未必改善交互组织。多个自适应通道先表达不同关系，multi-stage FFN再逐级融合，使参数扩展与特征交叉相配合。但通道数量增加也可能重复建模，不能因参数更多就宣布更有效，需与单通道及同预算配置比较。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户—商品、场景—商品、行为—候选的关系可先由不同通道捕获，再逐步组合；若所有通道都学成相同注意力，扩大它们只会增加成本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.03036">原论文</a> · <a href="../../../../reproductions/2502.03036-fuxi-alpha/">实现解读</a> · <a href="#qa-034c54f6610a2785">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:adaf2m2" data-paper-title="AdaF²M²: Comprehensive Learning and Responsive Leveraging Features in Recommendation System" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="AdaF²M²: Comprehensive Learning and Responsive Leveraging Features in Recommendation System 搜广推与 LLM 应用 ByteDance / Douyin 2025-01-27 单次全特征前向容易过度依赖强特征，且不同用户/物品状态需要不同特征。AdaF²M² 通过多种 mask 重复前向学习互补表示，再以 state-aware adapter 动态融合。 Fidelity: 核心机制复现。实际执行三组 feature-mask 前向、共享聚合与用户/物品状态自适应 adapter。状态仅由历史长度和物品热度构造；没有抖音私有特征、全链路联合训练和线上资源成本。本地对照口径：相对单前向全特征基线，实验组 NDCG@10 +2.42%。  ranking feature-masking state-aware-adapter multi-forward 搜广推 用户历史与排序骨干 AdaF²M²的多种mask前向，和只随机丢一次特征有什么区别？ 多路mask让模型在不同信号缺席时分别学习互补表示，而非只拿一次受扰结果训练。state-aware adapter再根据当前用户或物品状态分配各路权重，使强特征可用时利用它、脆弱时依赖其他路径。收益来自条件化融合，不能把多路简单平均视为同一机制。 示意：老商品可重用行为路，新商品更依赖内容路；同一次请求分别计算遮掉行为、遮掉内容的表示，再由状态决定组合比例。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-adaf2m2-4b0f92a1" class="ar-learning-paper-anchor"></span>
<h2 id="qa-c63df32fe423b84d">AdaF²M²的多种mask前向，和只随机丢一次特征有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aadaf2m2">AdaF²M²: Comprehensive Learning and Responsive Leveraging Features in Recommendation System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多路mask让模型在不同信号缺席时分别学习互补表示，而非只拿一次受扰结果训练。state-aware adapter再根据当前用户或物品状态分配各路权重，使强特征可用时利用它、脆弱时依赖其他路径。收益来自条件化融合，不能把多路简单平均视为同一机制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>老商品可重用行为路，新商品更依赖内容路；同一次请求分别计算遮掉行为、遮掉内容的表示，再由状态决定组合比例。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2501.15816">原论文</a> · <a href="../../../../reproductions/2501.15816-adaf2m2/">实现解读</a> · <a href="#qa-c63df32fe423b84d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:twin-v2" data-paper-title="TWIN V2: Scaling Ultra-Long User Behavior Sequence Modeling for Enhanced CTR Prediction at Kuaishou" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TWIN V2: Scaling Ultra-Long User Behavior Sequence Modeling for Enhanced CTR Prediction at Kuaishou 搜广推与 LLM 应用 Kuaishou 2024-07-23 离线层次聚类将百万级生命周期行为压缩成带规模信息的虚拟物品；在线 GSU 检索相关簇，ESU 以 cluster-aware target attention 精排。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上执行论文的候选相关检索、层级压缩或蒸馏目标；未使用公司私有日志与线上 serving，线上 A/B 只引用原文。本地相对变化不得与原文指标混写。本地对照口径：基线为 shared transition + content baseline，实验组为 TWIN-V2，只改变论文核心机制；ndcg_at_10 0.0354 → 0.0433，相对基线 +22.45%。  ranking long-sequence training-serving 搜广推 用户历史与排序骨干 TWIN-V2 为什么把生命周期行为聚成带规模信息的虚拟物品，再做候选相关检索？ 极长历史无法逐事件在线精算，离线层级聚类先把重复或相似行为压成代表簇。在线 GSU 选择候选相关簇，ESU 再做 cluster-aware 交互，并考虑簇规模，避免把大簇仅因人数多而重复放大。压缩提高可服务性，却可能掩盖簇内稀有事件，不能把虚拟物品看作无损替代全部历史。 示意：用户多年里反复浏览相似跑鞋，可聚成一个带次数的虚拟物品。候选是越野鞋时检索相关簇，再利用规模信息，而不是把几千次近似浏览逐个计算注意力。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-twin-v2-72f26bc8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-646dc7ef8fc54339">TWIN-V2 为什么把生命周期行为聚成带规模信息的虚拟物品，再做候选相关检索？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atwin-v2">TWIN V2: Scaling Ultra-Long User Behavior Sequence Modeling for Enhanced CTR Prediction at Kuaishou</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>极长历史无法逐事件在线精算，离线层级聚类先把重复或相似行为压成代表簇。在线 GSU 选择候选相关簇，ESU 再做 cluster-aware 交互，并考虑簇规模，避免把大簇仅因人数多而重复放大。压缩提高可服务性，却可能掩盖簇内稀有事件，不能把虚拟物品看作无损替代全部历史。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户多年里反复浏览相似跑鞋，可聚成一个带次数的虚拟物品。候选是越野鞋时检索相关簇，再利用规模信息，而不是把几千次近似浏览逐个计算注意力。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2407.16357">原论文</a> · <a href="../../../../reproductions/2407.16357-twin-v2/">实现解读</a> · <a href="#qa-646dc7ef8fc54339">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hstu" data-paper-title="Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations 搜广推与 LLM 应用 Meta 2024-02-27 HSTU 在输入窗口内逐层更新历史 token，用因果交互建模行为之间的依赖。学习重点是把历史首算成本与 M-FALCON 缓存后的多候选增量成本分开。 保真度：核心机制复现。本地为核心层与 all-position 训练的缩小实现，未复刻异构 action/time、Stochastic Length 或 M-FALCON。MovieLens-100K 的三 seed 结果仅适用于匹配 SASRec 的本地协议，不能外推到工业系统。 有 M-FALCON 缓存后，哪些历史计算可以共享，哪些候选路径仍要重算？  搜广推 用户历史与排序骨干 HSTU为什么去掉softmax，却还要在聚合后归一化并加U-gate？ softmax把历史权重归一成总和固定的分布，容易弱化相关行为数量携带的偏好强度。HSTU用逐点SiLU聚合保留这种变化，再靠聚合后归一化稳定数值；U分支按当前token调制聚合结果。它仍在输入窗口内做因果历史交互，并没有因此变成线性复杂度模型。 示意：两位用户分别出现一次和十次同类行为，归一化平均可能看起来相似；逐点聚合允许区分强度，再由门控决定向下一层传多少信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-hstu-2703dd1e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d1b7f594100aaa20">HSTU为什么去掉softmax，却还要在聚合后归一化并加U-gate？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahstu">Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>softmax把历史权重归一成总和固定的分布，容易弱化相关行为数量携带的偏好强度。HSTU用逐点SiLU聚合保留这种变化，再靠聚合后归一化稳定数值；U分支按当前token调制聚合结果。它仍在输入窗口内做因果历史交互，并没有因此变成线性复杂度模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两位用户分别出现一次和十次同类行为，归一化平均可能看起来相似；逐点聚合允许区分强度，再由门控决定向下一层传多少信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2402.17152">原论文</a> · <a href="../../../../reproductions/2402.17152-hstu/">实现解读</a> · <a href="../../../001-hstu-longer-slimper/">阅读精选对比</a> · <a href="#qa-d1b7f594100aaa20">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hstu" data-paper-title="Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations 搜广推与 LLM 应用 Meta 2024-02-27 HSTU 在输入窗口内逐层更新历史 token，用因果交互建模行为之间的依赖。学习重点是把历史首算成本与 M-FALCON 缓存后的多候选增量成本分开。 保真度：核心机制复现。本地为核心层与 all-position 训练的缩小实现，未复刻异构 action/time、Stochastic Length 或 M-FALCON。MovieLens-100K 的三 seed 结果仅适用于匹配 SASRec 的本地协议，不能外推到工业系统。 有 M-FALCON 缓存后，哪些历史计算可以共享，哪些候选路径仍要重算？  搜广推 用户历史与排序骨干 HSTU 的历史 token 之间会不会交互，和只让候选读取一份静态历史向量有什么差别？ 会。HSTU 在有效输入窗口内逐层更新 token 状态，每个位置可聚合此前可见历史；较晚行为因而能结合更早上下文形成新表示。排序时目标 token 再读取这些状态，保留目标相关交互。因果掩码限制的是可见方向，不是禁止历史之间建模；窗口外未输入的事件也不会自动进入计算。 示意：先浏览相机再看镜头，镜头位置的状态可结合相机背景；候选三脚架读取的是这类已带上下文的历史状态，而不只是互不交流的原始物品向量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="qa-6d826e4c63d0f978">HSTU 的历史 token 之间会不会交互，和只让候选读取一份静态历史向量有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahstu">Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>会。HSTU 在有效输入窗口内逐层更新 token 状态，每个位置可聚合此前可见历史；较晚行为因而能结合更早上下文形成新表示。排序时目标 token 再读取这些状态，保留目标相关交互。因果掩码限制的是可见方向，不是禁止历史之间建模；窗口外未输入的事件也不会自动进入计算。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先浏览相机再看镜头，镜头位置的状态可结合相机背景；候选三脚架读取的是这类已带上下文的历史状态，而不只是互不交流的原始物品向量。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2402.17152">原论文</a> · <a href="../../../../reproductions/2402.17152-hstu/">实现解读</a> · <a href="../../../001-hstu-longer-slimper/">阅读精选对比</a> · <a href="#qa-6d826e4c63d0f978">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hstu" data-paper-title="Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations 搜广推与 LLM 应用 Meta 2024-02-27 HSTU 在输入窗口内逐层更新历史 token，用因果交互建模行为之间的依赖。学习重点是把历史首算成本与 M-FALCON 缓存后的多候选增量成本分开。 保真度：核心机制复现。本地为核心层与 all-position 训练的缩小实现，未复刻异构 action/time、Stochastic Length 或 M-FALCON。MovieLens-100K 的三 seed 结果仅适用于匹配 SASRec 的本地协议，不能外推到工业系统。 有 M-FALCON 缓存后，哪些历史计算可以共享，哪些候选路径仍要重算？  搜广推 用户历史与排序骨干 M-FALCON 缓存了哪些用户计算，为什么不能把整个 ranking 分数缓存给所有候选？ 原文§3.4与附录H把候选放入隔离的微批，复用各层候选无关历史 K/V；候选之间不互读，各自仍计算投影、目标到历史的交互和输出。缓存摊销历史编码，并未取消目标依赖。跨请求复用还要求历史、特征与模型版本等条件适用；本地 HSTU 没有实现该服务优化。 示意：一千个候选可分批读取同一份历史记忆，但相机和跑鞋各自的查询与分数仍不同。历史新增购买或模型更新后，也不能直接沿用旧缓存假装用户状态未变。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<h2 id="qa-a6dfb7484be36691">M-FALCON 缓存了哪些用户计算，为什么不能把整个 ranking 分数缓存给所有候选？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahstu">Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原文§3.4与附录H把候选放入隔离的微批，复用各层候选无关历史 K/V；候选之间不互读，各自仍计算投影、目标到历史的交互和输出。缓存摊销历史编码，并未取消目标依赖。跨请求复用还要求历史、特征与模型版本等条件适用；本地 HSTU 没有实现该服务优化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一千个候选可分批读取同一份历史记忆，但相机和跑鞋各自的查询与分数仍不同。历史新增购买或模型更新后，也不能直接沿用旧缓存假装用户状态未变。</p>
<p class="ar-learning-sources">依据：背景与主要改动、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2402.17152">原论文</a> · <a href="../../../../reproductions/2402.17152-hstu/">实现解读</a> · <a href="../../../001-hstu-longer-slimper/">阅读精选对比</a> · <a href="#qa-a6dfb7484be36691">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dcn-v2" data-paper-title="DCN V2: Improved Deep &amp; Cross Network and Practical Lessons for Web-scale Learning to Rank Systems" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="DCN V2: Improved Deep &amp; Cross Network and Practical Lessons for Web-scale Learning to Rank Systems 搜广推与 LLM 应用 Google 2020-08-19 DCN-V2 显式构造有界阶数的特征交互，并用低秩矩阵与专家混合降低 web-scale ranking 的参数和计算成本。 Fidelity: 核心机制复现。实现低秩 cross experts、输入相关 gate 与 deep tower。未使用 Google 私有数据和生产级专家规模；结果只验证显式交叉在公开数据上的作用。本地对照口径：基线是 deep-only；实验组是两层低秩 cross experts 与 gate；三 seed NDCG@10 相对 +22.87%。  ranking classic feature-interaction 搜广推 用户历史与排序骨干 DCN-V2为什么每一层都把原始输入x₀乘回当前交叉变换？ 原始输入作为锚点反复进入，使层数增加时产生可解释的更高阶特征组合，而非完全依赖普通MLP隐式拟合。矩阵形式能表达更丰富交叉，低秩分解与专家门控再控制参数与计算成本。低秩是容量约束和效率选择，不保证任意压缩都保持同样表达力，需与深层路径共同检验。 示意：第一层可组合用户与品类，下一层仍乘原始场景字段，就能形成用户—品类—时段交叉；低秩专家限制的是这些组合如何共享参数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-dcn-v2-7ac56e9e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-a5fba110bcfcd1e9">DCN-V2为什么每一层都把原始输入x₀乘回当前交叉变换？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adcn-v2">DCN V2: Improved Deep &amp; Cross Network and Practical Lessons for Web-scale Learning to Rank Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原始输入作为锚点反复进入，使层数增加时产生可解释的更高阶特征组合，而非完全依赖普通MLP隐式拟合。矩阵形式能表达更丰富交叉，低秩分解与专家门控再控制参数与计算成本。低秩是容量约束和效率选择，不保证任意压缩都保持同样表达力，需与深层路径共同检验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第一层可组合用户与品类，下一层仍乘原始场景字段，就能形成用户—品类—时段交叉；低秩专家限制的是这些组合如何共享参数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2008.13535">原论文</a> · <a href="../../../../reproductions/2008.13535-dcn-v2/">实现解读</a> · <a href="#qa-a5fba110bcfcd1e9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sim" data-paper-title="Search-based User Interest Modeling with Lifelong Sequential Behavior Data for CTR Prediction" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Search-based User Interest Modeling with Lifelong Sequential Behavior Data for CTR Prediction 搜广推与 LLM 应用 Alibaba 2020-06-10 以候选 item 为 query，GSU 从终身行为中快速搜索相关子序列，ESU 再计算候选与子序列的精确注意力。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上执行论文的候选相关检索、层级压缩或蒸馏目标；未使用公司私有日志与线上 serving，线上 A/B 只引用原文。本地相对变化不得与原文指标混写。本地对照口径：基线为 shared transition + content baseline，实验组为 SIM，只改变论文核心机制；ndcg_at_10 0.0354 → 0.0471，相对基线 +32.97%。  ranking long-sequence training-serving 搜广推 用户历史与排序骨干 SIM 为什么先用 GSU 搜相关历史，再由 ESU 做精细注意力，而不是对终身历史直接打分？ 候选相关的终身历史通常只占少数，对全部事件做精确交互成本高且噪声大。GSU 用较便宜的匹配选出子序列，ESU 再在这份候选相关证据上做精细注意力，把计算集中到可能有用的行为。两阶段的瓶颈是粗搜召回率：GSU 漏掉的关键事件，ESU 无法从不存在的输入中补回来。 示意：候选是相机时，先从多年历史中找摄影相关浏览，再比较具体品牌与用途。若粗搜只按错误类别过滤掉镜头历史，后面的精细注意力再强也读不到它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-sim-df73a28d" class="ar-learning-paper-anchor"></span>
<h2 id="qa-ff2b1a817c0aa800">SIM 为什么先用 GSU 搜相关历史，再由 ESU 做精细注意力，而不是对终身历史直接打分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asim">Search-based User Interest Modeling with Lifelong Sequential Behavior Data for CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>候选相关的终身历史通常只占少数，对全部事件做精确交互成本高且噪声大。GSU 用较便宜的匹配选出子序列，ESU 再在这份候选相关证据上做精细注意力，把计算集中到可能有用的行为。两阶段的瓶颈是粗搜召回率：GSU 漏掉的关键事件，ESU 无法从不存在的输入中补回来。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>候选是相机时，先从多年历史中找摄影相关浏览，再比较具体品牌与用途。若粗搜只按错误类别过滤掉镜头历史，后面的精细注意力再强也读不到它。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2006.05639">原论文</a> · <a href="../../../../reproductions/2006.05639-sim/">实现解读</a> · <a href="#qa-ff2b1a817c0aa800">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:bst" data-paper-title="Behavior Sequence Transformer for E-commerce Recommendation in Alibaba" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Behavior Sequence Transformer for E-commerce Recommendation in Alibaba 搜广推与 LLM 应用 Alibaba 2019-05-15 BST 用自注意力统一建模行为之间及行为与候选之间的关系，替代固定 pooling 或单一目标注意力。 Fidelity: 核心机制复现。实现候选 token、位置编码和行为序列 Transformer。公开数据替代淘宝日志；没有复刻用户画像、上下文特征和生产推理系统。本地对照口径：基线是 DIN；实验组是候选参与编码的 Transformer；三 seed NDCG@10 相对 +20.29%。  ranking classic sequence-modeling 搜广推 用户历史与排序骨干 BST把候选与行为一起做self-attention，和DIN只用候选给历史加权有什么不同？ DIN主要学习候选对各条行为的激活，BST还让行为之间交换信息，并让候选参与统一编码。这样某条历史的含义可以受其他行为影响，而不是始终作为固定键值独立出现；代价是更多序列计算，以及候选进入后部分状态不再能跨候选直接复用。是否值得要对齐预算与输入窗口比较。 示意：单独看一次相机点击可能是偶然，结合接连观看镜头和摄影教程后，行为间交互能强化摄影意图；换候选时共同编码的状态也可能随之改变。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-bst-730383cc" class="ar-learning-paper-anchor"></span>
<h2 id="qa-a856ffcdedab0d96">BST把候选与行为一起做self-attention，和DIN只用候选给历史加权有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Abst">Behavior Sequence Transformer for E-commerce Recommendation in Alibaba</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>DIN主要学习候选对各条行为的激活，BST还让行为之间交换信息，并让候选参与统一编码。这样某条历史的含义可以受其他行为影响，而不是始终作为固定键值独立出现；代价是更多序列计算，以及候选进入后部分状态不再能跨候选直接复用。是否值得要对齐预算与输入窗口比较。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>单独看一次相机点击可能是偶然，结合接连观看镜头和摄影教程后，行为间交互能强化摄影意图；换候选时共同编码的状态也可能随之改变。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1905.06874">原论文</a> · <a href="../../../../reproductions/1905.06874-bst/">实现解读</a> · <a href="#qa-a856ffcdedab0d96">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dien" data-paper-title="Deep Interest Evolution Network for Click-Through Rate Prediction" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Deep Interest Evolution Network for Click-Through Rate Prediction 搜广推与 LLM 应用 Alibaba 2018-09-11 DIN 直接激活历史兴趣，DIEN 则先用辅助监督抽取逐步兴趣，再让目标商品控制兴趣状态的演化速度。 Fidelity: 核心机制复现。实现兴趣抽取 GRU、下一行为辅助损失和候选相关兴趣演化。MovieLens 的短序列和稀疏信号不能替代 Taobao 广告特征；未使用生产 fused AUGRU kernel。本地对照口径：基线是同一训练协议的 DIN；实验组加入 GRU、辅助目标和候选相关演化；三 seed NDCG@10 相对 -1.98%，未迁移论文收益。  ranking classic sequence-modeling 搜广推 用户历史与排序骨干 DIEN把目标相关权重乘进GRU更新门，而不只在最后对历史池化，改变了什么？ 辅助目标先帮助抽取每一步的兴趣状态，候选相关注意力再调节状态更新速度。相关行为可以更强地改写当前兴趣，不相关行为则较少覆盖已有记忆，目标信息因此参与整条演化链。若仅在结尾加权，前面的状态已可能被无关事件改写；多一个循环模块也不保证在短历史数据上更好。 示意：用户连续看摄影内容后偶然点一次食品广告，推荐镜头时可减弱这次食品行为对兴趣状态的更新，而不是等最后才试图从被改写的状态中恢复摄影兴趣。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-dien-3d6c73b7" class="ar-learning-paper-anchor"></span>
<h2 id="qa-6b9b05c208996f59">DIEN把目标相关权重乘进GRU更新门，而不只在最后对历史池化，改变了什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adien">Deep Interest Evolution Network for Click-Through Rate Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>辅助目标先帮助抽取每一步的兴趣状态，候选相关注意力再调节状态更新速度。相关行为可以更强地改写当前兴趣，不相关行为则较少覆盖已有记忆，目标信息因此参与整条演化链。若仅在结尾加权，前面的状态已可能被无关事件改写；多一个循环模块也不保证在短历史数据上更好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户连续看摄影内容后偶然点一次食品广告，推荐镜头时可减弱这次食品行为对兴趣状态的更新，而不是等最后才试图从被改写的状态中恢复摄影兴趣。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1809.03672">原论文</a> · <a href="../../../../reproductions/1809.03672-dien/">实现解读</a> · <a href="#qa-6b9b05c208996f59">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sasrec" data-paper-title="Self-Attentive Sequential Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Self-Attentive Sequential Recommendation 搜广推与 LLM 应用 UC San Diego 2018-08-20 Markov Chain 偏重最近行为，RNN 又需要逐步计算。SASRec 用因果自注意力直接选择序列中与下一物品相关的行为，在稀疏与稠密数据之间取得更灵活的感受野，并成为序列推荐常用基线。 保真度：完整核心链路复现。保真度：完整核心链路复现。模型、原论文 pairwise BCE 训练目标与序列推理均实际执行；仅把公开数据从 MovieLens-1M 缩到 MovieLens-100K，并采用更严格的全库评估。本地对照口径：基线是 popularity 排序；实验组是 SASRec；主指标 NDCG@10 从 0.02969 降至 0.02933（-1.24%）。这是跨模型基线比较，不是 SASRec 模块消融。   搜广推 用户历史与排序骨干 SASRec 的因果自注意力如何兼顾短期与较远兴趣，又怎样避免训练时读取未来？ 每个位置可按内容对此前多个行为分配注意力，不像固定阶 Markov 只看近邻，也不必像 RNN 逐步递推全部历史。因果掩码禁止当前位置读取后续事件，下一物品仅作为监督目标。位置表示保留顺序，网络因数据稀疏程度可学不同感受野；自注意力本身不保证自动忽略所有无关历史。 示意：用户最近看喜剧，但较早看过多部科幻。预测下一片时可回看相关科幻行为，同时训练位置三不能看到位置四的电影，即使它正是要预测的标签。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-sasrec-6f67bc6e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-9e5caa204add37ff">SASRec 的因果自注意力如何兼顾短期与较远兴趣，又怎样避免训练时读取未来？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asasrec">Self-Attentive Sequential Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每个位置可按内容对此前多个行为分配注意力，不像固定阶 Markov 只看近邻，也不必像 RNN 逐步递推全部历史。因果掩码禁止当前位置读取后续事件，下一物品仅作为监督目标。位置表示保留顺序，网络因数据稀疏程度可学不同感受野；自注意力本身不保证自动忽略所有无关历史。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户最近看喜剧，但较早看过多部科幻。预测下一片时可回看相关科幻行为，同时训练位置三不能看到位置四的电影，即使它正是要预测的标签。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1808.09781">原论文</a> · <a href="../../../../reproductions/1808.09781-sasrec/">实现解读</a> · <a href="#qa-9e5caa204add37ff">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:din" data-paper-title="Deep Interest Network for Click-Through Rate Prediction" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Deep Interest Network for Click-Through Rate Prediction 搜广推与 LLM 应用 Alibaba 2017-06-21 传统 CTR 模型把用户全部行为压成固定向量，但用户与候选物品相关的兴趣只占历史的一部分。DIN 不再生成一个与候选无关的用户向量，而是用候选物品逐条激活历史行为，再把局部兴趣送入点击网络；Dice 根据当前特征分布自适应调整激活边界。 保真度：核心机制复现。保真度：核心机制复现。本实现实际训练候选物品条件化的 local activation、加权兴趣池化、Dice 与 CTR 网络；未复刻 Alibaba 私有稀疏特征、mini-batch-aware regularization 和生产 serving。本地对照口径：基线是移除 candidate-aware attention、改用 mean pooling 的同参数模型；实验组是 DIN；主指标 NDCG@10 从 0.01783 降至 0.01659（-6.97%）。这是 DIN 核心注意力的内部消融，不是相对其他推荐模型的提升。   搜广推 用户历史与排序骨干 DIN为什么对同一个用户也会得到不同的兴趣向量？ 用户历史包含多种兴趣，哪些行为重要取决于当前候选。DIN用候选和每条历史的组合特征学习激活，再加权聚合，因此用户表示随候选变化，而非始终是一个固定均值。候选感知提高表达力，却也意味着完整聚合状态通常不能跨所有候选直接复用；效果需与同预算池化对照判断。 示意：历史里既有跑鞋也有烤箱，评估运动袜时突出跑步行为，评估烘焙工具时突出厨房行为；两次使用同一份历史，却应得到不同的兴趣摘要。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-din-dfe7b0eb" class="ar-learning-paper-anchor"></span>
<h2 id="qa-13240dbf0db3f265">DIN为什么对同一个用户也会得到不同的兴趣向量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adin">Deep Interest Network for Click-Through Rate Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用户历史包含多种兴趣，哪些行为重要取决于当前候选。DIN用候选和每条历史的组合特征学习激活，再加权聚合，因此用户表示随候选变化，而非始终是一个固定均值。候选感知提高表达力，却也意味着完整聚合状态通常不能跨所有候选直接复用；效果需与同预算池化对照判断。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>历史里既有跑鞋也有烤箱，评估运动袜时突出跑步行为，评估烘焙工具时突出厨房行为；两次使用同一份历史，却应得到不同的兴趣摘要。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1706.06978">原论文</a> · <a href="../../../../reproductions/1706.06978-din/">实现解读</a> · <a href="#qa-13240dbf0db3f265">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:deepfm" data-paper-title="DeepFM: A Factorization-Machine based Neural Network for CTR Prediction" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="DeepFM: A Factorization-Machine based Neural Network for CTR Prediction 搜广推与 LLM 应用 Huawei Noah&#x27;s Ark Lab 2017-03-13 CTR 排序既依赖低阶组合特征，也依赖高阶非线性交互。传统 Wide &amp; Deep 需要人工构造 wide 特征，DeepFM 则让两条路径端到端共享 embedding。模型把 FM 的一阶/二阶项与 MLP 输出相加。相同 field embedding 同时进入两条路径，减少人工交叉和重复参数。 复现级别：核心机制复现。复现级别：核心机制复现。实际联合训练 FM 二阶交互与 deep 分支；私有工业特征和线上系统不在本地复现范围。本地对照口径：基线为 embedding MLP，实验组为共享 embedding 的 FM + deep 分支；NDCG@10 相对 +23.58%，见 metrics/movielens-100k-seeds42-44.json。  ranking classic feature-interaction 搜广推 用户历史与排序骨干 DeepFM为什么让FM与DNN共享同一份field embedding？ FM直接建模一阶和二阶组合，DNN学习更高阶非线性关系，两路需要的是同一组基础字段语义。共享embedding减少重复参数，并让低阶与高阶监督共同塑造底层表示，避免像手工wide交叉那样额外维护特征。但共享也会产生梯度耦合，不能把两路分数相加视为天然无冲突。 示意：用户职业与商品类目的一对组合可由FM学习，职业、类目、价格三者的复杂条件交给DNN；两路都更新同一字段向量，而不是各存一套互不沟通的词表。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-deepfm-65a63b7d" class="ar-learning-paper-anchor"></span>
<h2 id="qa-c7aa48572635a536">DeepFM为什么让FM与DNN共享同一份field embedding？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adeepfm">DeepFM: A Factorization-Machine based Neural Network for CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Noah&#x27;s Ark Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>FM直接建模一阶和二阶组合，DNN学习更高阶非线性关系，两路需要的是同一组基础字段语义。共享embedding减少重复参数，并让低阶与高阶监督共同塑造底层表示，避免像手工wide交叉那样额外维护特征。但共享也会产生梯度耦合，不能把两路分数相加视为天然无冲突。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户职业与商品类目的一对组合可由FM学习，职业、类目、价格三者的复杂条件交给DNN；两路都更新同一字段向量，而不是各存一套互不沟通的词表。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1703.04247">原论文</a> · <a href="../../../../reproductions/1703.04247-deepfm/">实现解读</a> · <a href="#qa-c7aa48572635a536">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:wide-deep" data-paper-title="Wide &amp; Deep Learning for Recommender Systems" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Wide &amp; Deep Learning for Recommender Systems 搜广推与 LLM 应用 Google 2016-06-24 纯线性模型善于记忆稀疏共现但泛化弱，纯 DNN 能泛化却可能推荐不相关组合。论文联合训练两路并共享最终 logit。 Fidelity: 核心机制复现。本地实现联合记忆型 wide 交叉与泛化型 deep tower。公开 MovieLens 替代 Google Play 私有日志；未复刻生产特征工程、分布式训练与 serving。本地对照口径：基线是参数匹配的 deep-only 模型；实验组加入 candidate 与 genre 交叉的 wide 路径；MovieLens-100K 三 seed 全库 NDCG@10 相对 +5.45%。  ranking classic feature-interaction 搜广推 用户历史与排序骨干 Wide &amp; Deep 为什么联合训练线性交叉与深网络，而不是只对两个独立模型做分数平均？ wide 路径可直接记忆已观察到的稀疏交叉，deep 路径通过嵌入与非线性共享知识，二者共同贡献一个 logit 并接受同一目标梯度。联合训练让各自学习补充尚未解释的部分，而非独立训练后固定融合。人工交叉覆盖有限，deep 泛化也可能产生不合理组合，因此两路能力互补但都需控制。 示意：wide 可记住“某用户群经常买某类商品”的明确交叉，deep 把相似品类经验迁移给新组合。共同训练时两者调整相对贡献，不是先各自最优再简单取平均。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-wide-deep-604050a0" class="ar-learning-paper-anchor"></span>
<h2 id="qa-bc8a20781ba57a95">Wide &amp; Deep 为什么联合训练线性交叉与深网络，而不是只对两个独立模型做分数平均？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Awide-deep">Wide &amp; Deep Learning for Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>wide 路径可直接记忆已观察到的稀疏交叉，deep 路径通过嵌入与非线性共享知识，二者共同贡献一个 logit 并接受同一目标梯度。联合训练让各自学习补充尚未解释的部分，而非独立训练后固定融合。人工交叉覆盖有限，deep 泛化也可能产生不合理组合，因此两路能力互补但都需控制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>wide 可记住“某用户群经常买某类商品”的明确交叉，deep 把相似品类经验迁移给新组合。共同训练时两者调整相对贡献，不是先各自最优再简单取平均。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1606.07792">原论文</a> · <a href="../../../../reproductions/1606.07792-wide-deep/">实现解读</a> · <a href="#qa-bc8a20781ba57a95">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

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

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
