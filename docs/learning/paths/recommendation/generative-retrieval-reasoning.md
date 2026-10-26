---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 生成式召回与推理推荐

[搜广推](index.md) / 60 个问题 · 60 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">60 个问题 · 60 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onelatent" data-paper-title="OneLatent: Latent Reasoning for Efficient Foundation Recommendation Models" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneLatent: Latent Reasoning for Efficient Foundation Recommendation Models 搜广推与 LLM 应用 Kuaishou Technology 2026-10-22 推荐FRM的显式CoT会增加生成时延，也可能过度思考或被固定推理模板带偏。OneLatent先用探索、评价、归因三视角生成自适应教师监督，再学习三个潜在token接口，最后只生成三层语义ID，避免在线输出长推理文本。 成本过高，不复现（审查 DONE），不下载235B教师、不做56卡训练的缩小替身、不自动重试因此本项是资料与成本审查完成，没有本地模型、诊断proxy、benchmark指标、GPU回执或evolve映射。Appendix A.1原配置为7节点×每节点8GPU，即56GPU、全参数BF16、4096tokens、两有效epochs；监督涉及Qwen3-235B-A22B教师及工业数据。单张A100/A30或Mac不适合照搬完整矩阵，本轮不先下载/试跑来验证它昂贵。  大模型能力与推荐融合 潜在推理与生成式推荐 搜广推 生成式召回与推理推荐 OneLatent 的潜在 token 为什么能省掉在线长推理，又不能被称为严格的推理信息瓶颈？ 训练用探索、评价、归因理由重建教学生通过潜在 token 组织推荐信息，随后只预测语义 ID，省去输出长理由的解码成本。但普通因果掩码仍允许输出读取原始画像和历史，且更新全部学生参数，所以效果不能归因于潜在 token 单独存储了全部推理。本地仅完成资料与成本审查，没有运行复现。 示意：训练时教模型用几个内部标记支持“为何适合这位用户”的回答，上线只输出物品编码。即使推荐更快，也不能据此断言这些标记完整保存了每一步推理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-onelatent-08691361" class="ar-learning-paper-anchor"></span>
<h2 id="qa-edb5f88714252428">OneLatent 的潜在 token 为什么能省掉在线长推理，又不能被称为严格的推理信息瓶颈？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonelatent">OneLatent: Latent Reasoning for Efficient Foundation Recommendation Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>训练用探索、评价、归因理由重建教学生通过潜在 token 组织推荐信息，随后只预测语义 ID，省去输出长理由的解码成本。但普通因果掩码仍允许输出读取原始画像和历史，且更新全部学生参数，所以效果不能归因于潜在 token 单独存储了全部推理。本地仅完成资料与成本审查，没有运行复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练时教模型用几个内部标记支持“为何适合这位用户”的回答，上线只输出物品编码。即使推荐更快，也不能据此断言这些标记完整保存了每一步推理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、成本判断与本地边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30675v1">原论文</a> · <a href="../../../../recommendation-components/2610.30675-onelatent/">实现解读</a> · <a href="#qa-edb5f88714252428">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:spar-prefix-balance" data-paper-title="SPAR: Stepwise Personalized Autoregressive Recommendation with Prefix-Balanced Semantic IDs" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="SPAR: Stepwise Personalized Autoregressive Recommendation with Prefix-Balanced Semantic IDs 搜广推与 LLM 应用 University of Electronic Science and Technology of China 2026-10-20 同一用户长历史中，有用证据随已生成SID前缀而变；热门前缀的交互负载还会压倒其他分支。SPAR由三部分组成：按前缀检索粗到细记忆的PATH、冻结残差码本后的RQ-PIB负载修复，以及SFT+DPO偏好对齐。本地只实现第二部分的修复子程序，不拿字典或K-means冒充整个推荐模型。 完整生产训练与A/B成本过高，不复现（审查 DONE）。已实现RQ-PIB的冻结码本修复阶段，仅L1机制诊断；已实现RQ-PIB的冻结码本修复阶段，仅L1机制诊断；没有实现PATH Decoder、RQ训练或偏好训练。完整生产训练与A/B成本过高，不复现（审查 DONE）。输入必须提供冻结码中心、残差、分配、训练期权重和父前缀。算法实现Eq13–15/Algorithm1的分支修复，以独立构造验证最小可行移动、空分支目的地、重商品上界、总负载守恒、至多一次移动和“不修复则超载”的负对照。合成权重不是推荐指标，也不能说明未来曝光更公平。  生成式推荐 前缀负载平衡 搜广推 生成式召回与推理推荐 SPAR 的 RQ-PIB 为什么只移动商品分支、不更新码中心，并用包含最重商品的负载上界？ 冻结码中心与父前缀可限制修复对语义路径的扰动，算法只在可行目的分支中选择距离代价最小的当前移动。商品不可分且权重不同，平均负载不一定可达，因此上界需考虑最重商品，不能强求严格等分。每件至多移动一次也限定修复范围；本地只实现这段子程序，没有整个记忆检索与偏好对齐模型。 示意：三个分支总负载十二，但某个商品单独重六，要求每支恰好四不可能。上界容纳不可分重商品，再从过载支选代价最小的可行移动，而非重训所有码中心。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-spar-prefix-balance-335a990d" class="ar-learning-paper-anchor"></span>
<h2 id="qa-e5b3653237f86b16">SPAR 的 RQ-PIB 为什么只移动商品分支、不更新码中心，并用包含最重商品的负载上界？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aspar-prefix-balance">SPAR: Stepwise Personalized Autoregressive Recommendation with Prefix-Balanced Semantic IDs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Electronic Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冻结码中心与父前缀可限制修复对语义路径的扰动，算法只在可行目的分支中选择距离代价最小的当前移动。商品不可分且权重不同，平均负载不一定可达，因此上界需考虑最重商品，不能强求严格等分。每件至多移动一次也限定修复范围；本地只实现这段子程序，没有整个记忆检索与偏好对齐模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三个分支总负载十二，但某个商品单独重六，要求每支恰好四不可能。上界容纳不可分重商品，再从过载支选代价最小的可行移动，而非重训所有码中心。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.27898v1">原论文</a> · <a href="../../../../recommendation-components/2610.27898-spar-prefix-balance/">实现解读</a> · <a href="#qa-e5b3653237f86b16">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unisgr-v2" data-paper-title="UniSGR-V2: Stepwise Target-Side Feature Anticipation and Crossing for Generative Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="UniSGR-V2: Stepwise Target-Side Feature Anticipation and Crossing for Generative Recommendation 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-10-12 生成式推荐尚未生成目标商品时无法读取其侧信息，导致逐级生成与最终排序同时缺少商品属性。TacGR在每级语义码之前预测连续侧信息并做解码器内交叉，同时用辅助排序塔防止回归目标坍塌、单向掩码隔离预测噪声。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文§4.1：24.2亿私有样本、646万用户、753万商品；8层512维GQA/SwiGLU-MoE解码器，64专家top-2、序列长度1024。数据不可用，原规模训练超出单卡A100/A30或Mac预算；没有实测本地耗时，不用昂贵试跑估算。  generative-recommendation target-side-feature multitask-ranking 搜广推 生成式召回与推理推荐 TacGR 为什么先预测目标侧信息，又用单向掩码阻止语义 token 在注意力中读取预测 token？ 生成目标尚未确定时拿不到真实商品属性，先预测连续侧信息可为每级码提供条件。预测噪声若反复写回语义历史会累积，因此掩码限制这条注意力传播；预测特征仍通过输出条件进入生成，并非被禁用。辅助排序塔给可学习回归目标语义锚定，避免共同坍塌；本地因数据与预算没有完整复现。 示意：生成商品码前先估计价格与风格，输出头可利用这些估计；但不让估计 token 任意污染此前语义状态。若只把预测特征全部关掉，就失去了论文要补充的目标侧信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-unisgr-v2-08304e35" class="ar-learning-paper-anchor"></span>
<h2 id="qa-0d266de6aee71fa6">TacGR 为什么先预测目标侧信息，又用单向掩码阻止语义 token 在注意力中读取预测 token？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunisgr-v2">UniSGR-V2: Stepwise Target-Side Feature Anticipation and Crossing for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>生成目标尚未确定时拿不到真实商品属性，先预测连续侧信息可为每级码提供条件。预测噪声若反复写回语义历史会累积，因此掩码限制这条注意力传播；预测特征仍通过输出条件进入生成，并非被禁用。辅助排序塔给可学习回归目标语义锚定，避免共同坍塌；本地因数据与预算没有完整复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>生成商品码前先估计价格与风格，输出头可利用这些估计；但不让估计 token 任意污染此前语义状态。若只把预测特征全部关掉，就失去了论文要补充的目标侧信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.16132">原论文</a> · <a href="../../../../reproductions/2610.16132-unisgr-v2/">实现解读</a> · <a href="#qa-0d266de6aee71fa6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:wegr" data-paper-title="WeGR: Unified Generative Retrieval for Industrial Search Systems in WeChat" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="WeGR: Unified Generative Retrieval for Industrial Search Systems in WeChat 搜广推与 LLM 应用 WeChat E-commerce Search team（正文未单列作者机构） 2026-10-12 WeGR 联合优化协同语义编码和生成检索偏好：CoCo-VAE 让连续表示学习查询—商品与商品—商品共现，刷新低使用率码字，并用残差保真和跨样本碰撞损失改善码本利用率。DHPO 从短 SID 前缀逐步扩展到完整 SID，同时扩展奖励匹配和策略梯度范围，以多正例 SFT 稳定稀疏奖励下的训练。 三种子只是有界机制诊断，稳定相对提升不适用。本地对照口径：基线为 SFT 和完整 SID GRPO+MSFT，实验组为动态 horizon DHPO+MSFT；共用同一 CoCo-VAE 和 SFT 初始化。三种子只是有界机制诊断，稳定相对提升不适用。  generative-recommendation semantic-id preference-optimization 搜广推 生成式召回与推理推荐 WeGR 的 DHPO 为什么从短 SID 前缀逐渐扩展奖励匹配与策略梯度范围？ 一开始要求完整长 SID 命中会让奖励极稀疏，模型难区分部分正确路径。动态 horizon 先奖励较短前缀，并只更新对应 token 范围，再随训练逐步扩到完整路径，使奖励粒度与优化范围一致。多正例 SFT 稳定更新，CoCo-VAE 另行改善编码；本地是有界机制诊断，不能据此宣称大规模稳定提升。 示意：先学对“户外”粗码就能获得反馈，之后要求“户外—露营”，最终才要求具体帐篷完整码。若只放宽奖励却仍强更新全部后缀，可能把未被评价的错误路径一起强化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-wegr-8c03ebb0" class="ar-learning-paper-anchor"></span>
<h2 id="qa-560f97a3aa5441bb">WeGR 的 DHPO 为什么从短 SID 前缀逐渐扩展奖励匹配与策略梯度范围？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Awegr">WeGR: Unified Generative Retrieval for Industrial Search Systems in WeChat</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · WeChat E-commerce Search team（正文未单列作者机构）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一开始要求完整长 SID 命中会让奖励极稀疏，模型难区分部分正确路径。动态 horizon 先奖励较短前缀，并只更新对应 token 范围，再随训练逐步扩到完整路径，使奖励粒度与优化范围一致。多正例 SFT 稳定更新，CoCo-VAE 另行改善编码；本地是有界机制诊断，不能据此宣称大规模稳定提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先学对“户外”粗码就能获得反馈，之后要求“户外—露营”，最终才要求具体帐篷完整码。若只放宽奖励却仍强更新全部后缀，可能把未被评价的错误路径一起强化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.16979">原论文</a> · <a href="../../../../reproductions/2610.16979-wegr/">实现解读</a> · <a href="#qa-560f97a3aa5441bb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gear" data-paper-title="Generative End-to-end Ad Retrieval at Douyin" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Generative End-to-end Ad Retrieval at Douyin 搜广推与 LLM 应用 ByteDance 2026-09-30 GEAR 用正交基参数化 BasisVQ/BasisRQ，使码本更新具有全局共享和稳定旋转；生成器输出层级 token，碰撞 item 再由上下文条件 reranker 精排。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 BasisVQ、前缀残差量化接口与碰撞 rerank；不复刻流式 PS、分钟级索引和线上流量，不把本地随机张量作为广告效果。执行 BasisVQ、前缀残差量化接口与碰撞 rerank；不复刻流式 PS、分钟级索引和线上流量，不把本地随机张量作为广告效果。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  ad-retrieval generative-retrieval semantic-id 搜广推 生成式召回与推理推荐 GEAR为什么把码本写成共享正交基，而不是任意更新每个码向量？ 共享基使码本变化受到整体几何结构约束，便于在更新中保留较稳定的表示关系；层级生成仍负责粗到细选择，碰撞组再交给上下文重排区分。结构化码本不自动消除碰撞，也不能代替推荐目标训练。本地只验证量化、状态与梯度组件，不支持将其说成完整广告检索收益。 示意：多个码共享一套坐标基，更新更像有组织地调整坐标而非各自乱漂；两件广告若仍落在同一码，必须根据当前用户再排，不能只返回一个固定热门广告。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-gear-42599d59" class="ar-learning-paper-anchor"></span>
<h2 id="qa-97a87993f2fd04a0">GEAR为什么把码本写成共享正交基，而不是任意更新每个码向量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agear">Generative End-to-end Ad Retrieval at Douyin</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共享基使码本变化受到整体几何结构约束，便于在更新中保留较稳定的表示关系；层级生成仍负责粗到细选择，碰撞组再交给上下文重排区分。结构化码本不自动消除碰撞，也不能代替推荐目标训练。本地只验证量化、状态与梯度组件，不支持将其说成完整广告检索收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>多个码共享一套坐标基，更新更像有组织地调整坐标而非各自乱漂；两件广告若仍落在同一码，必须根据当前用户再排，不能只返回一个固定热门广告。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.39327">原论文</a> · <a href="../../../../reproductions/2609.39327-gear/">实现解读</a> · <a href="#qa-97a87993f2fd04a0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:grp" data-paper-title="GRP v0.1 Technical Report" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="GRP v0.1 Technical Report 搜广推与 LLM 应用 Snap Inc. 2026-09-29 GRP 不是一次性替换成熟推荐漏斗，而是逐步把统一生成模型作为召回源接入，再替换弱源、增加配额并逐步绕过排序器。模型用 encoder-decoder 生成多模态 Semantic ID；MHP 通过 stop-gradient 路径联合学习排序，之后冻结为 RL reward。mGRPO 在 GRPO 上增加以 logged target 为锚点的单边 margin，只在策略开始牺牲原目标召回时惩罚。 复现级别：L1 架构与目标机制。复现级别：L1 架构与目标机制。本地实现独立 SID block mask、生成/排序梯度隔离和 mGRPO 单边召回保护；不宣称复现 Snap 线上效果。未包含 Snap 私有数据、Qwen3-VL SID tokenizer、生产尺度训练、CUDA graph serving、反向目录和在线流量，因此标记 concept_demo / l1_mechanism，不进入 Evolve 的效果提升证据池。本地对照口径：基线为不触发 logged-target 单边保护的同一 GRPO surrogate，实验组启用保护项；  generative-recommendation ranking rl-alignment 搜广推 生成式召回与推理推荐 GRP的logged-target单边margin为什么只在原目标召回被牺牲时激活？ 奖励优化可能把策略推向少数高分输出，同时降低原日志目标的概率。单边保护只惩罚超过容忍区间的下降，给新偏好改进留空间，又避免任意损伤基础召回；排序reward头停止梯度并冻结，也减少奖励与生成器相互追逐。本地仅验证目标与梯度组件，不能据此证明生产漏斗已被替换。 示意：新策略发现更有价值的候选且未明显损伤原目标时无需额外束缚；若只是把概率全部挪给一类高奖励物品，margin才对这种基础能力退化施加保护。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-grp-12c5e416" class="ar-learning-paper-anchor"></span>
<h2 id="qa-7c1a13612a425df6">GRP的logged-target单边margin为什么只在原目标召回被牺牲时激活？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agrp">GRP v0.1 Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Snap Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>奖励优化可能把策略推向少数高分输出，同时降低原日志目标的概率。单边保护只惩罚超过容忍区间的下降，给新偏好改进留空间，又避免任意损伤基础召回；排序reward头停止梯度并冻结，也减少奖励与生成器相互追逐。本地仅验证目标与梯度组件，不能据此证明生产漏斗已被替换。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新策略发现更有价值的候选且未明显损伤原目标时无需额外束缚；若只是把概率全部挪给一类高奖励物品，margin才对这种基础能力退化施加保护。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36688">原论文</a> · <a href="../../../../reproductions/2609.36688-grp/">实现解读</a> · <a href="#qa-7c1a13612a425df6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:xrec" data-paper-title="X-Rec Technical Report" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="X-Rec Technical Report 搜广推与 LLM 应用 TikTok (ByteDance) 2026-09-24 传统 U2I 召回将用户兴趣压缩为一个或少量向量，生成式语义 ID 方法则要逐 token 解码。X-Rec 直接在归一化 item embedding 球面上生成多个召回触发向量：先预测 item 所在的粗粒度聚类（anchor），再以该 anchor 为条件把球面噪声沿测地线流向目标 item。生成的向量与全量 item embedding 做近邻检索，可覆盖多个兴趣区域而无需语义 ID 量化。论文的另一个重点是计算结构：历史行为先经过前 L-1 层 Transformer； 未执行：TikTok 私有多属性日志与 streaming benchmark、工业 item encoder、ANN/在线 KV 服务、真实线上 A/B。Fidelity：核心机制复现；证据等级：L2 公开数据集。公开 MovieLens 任务只检验算法链路，不代表 TikTok 流量或论文绝对结果。当前是低预算机制实验；在 MovieLens-1M 上，X-Rec 的三种子均值低于 U2I，不能宣称收益。实际执行：item 对比学习、球面 anchor 聚类与 CE、测地线 RFM 监督、末层历史 K/V 复用、时间/anchor 调制、切空间速度、球面 Euler 和多 trigger 全目录检索。  retrieval generative-recommendation flow-matching 搜广推 生成式召回与推理推荐 X-Rec 为什么在归一化 embedding 球面上做条件流生成，而不是逐 token 生成 SID？ 连续 trigger 可直接对接近邻检索，避免离散量化与逐码路径的误差。先预测粗 anchor，再让球面噪声沿测地线流向目标向量，切空间投影和球面积分维持归一化几何；历史前层只算一次，去噪仅更新末层生成 token。它仍有多步采样与检索成本，本地低预算结果为负，不能据结构声称优于 SID。 示意：先定位摄影兴趣区域，再从球面噪声生成多个检索向量，分别覆盖相机与镜头。向量始终留在物品归一化空间，最后交给 ANN，而不是先生成一串整数码再查表。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-xrec-d9eceda3" class="ar-learning-paper-anchor"></span>
<h2 id="qa-4756ebc069854072">X-Rec 为什么在归一化 embedding 球面上做条件流生成，而不是逐 token 生成 SID？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Axrec">X-Rec Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · TikTok (ByteDance)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>连续 trigger 可直接对接近邻检索，避免离散量化与逐码路径的误差。先预测粗 anchor，再让球面噪声沿测地线流向目标向量，切空间投影和球面积分维持归一化几何；历史前层只算一次，去噪仅更新末层生成 token。它仍有多步采样与检索成本，本地低预算结果为负，不能据结构声称优于 SID。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先定位摄影兴趣区域，再从球面噪声生成多个检索向量，分别覆盖相机与镜头。向量始终留在物品归一化空间，最后交给 ANN，而不是先生成一串整数码再查表。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.29180">原论文</a> · <a href="../../../../reproductions/2609.29180-xrec/">实现解读</a> · <a href="#qa-4756ebc069854072">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unique" data-paper-title="UNIQUE: A Unified Retrieval and Ranking System for Large-Scale Feed Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="UNIQUE: A Unified Retrieval and Ranking System for Large-Scale Feed Recommendation 搜广推与 LLM 应用 Beihang University 2026-09-20 传统召回与排序分开优化，召回侧较难利用排序反馈；多层残差量化又可能逐层积累误差。UNIQUE 将物品先映射到一个扁平 code：物品向量由用户反馈监督的双塔编码，最近邻分配经使用频率校正，并用 EMA 更新码本。用户静态特征、近期行为、中期行为及兴趣摘要构成前缀；候选 item/code 各自只关注这一前缀，而不读取其他候选。共享的编码结果同时训练 code 分布和多个排序目标，推理时先按 code 提名，再对对应物品排序。 复现级别：公开数据缩比机制实验（概念验证）。复现级别：公开数据缩比机制实验（概念验证）。执行了反馈感知单层扁平量化、EMA 与频率平衡、用户多粒度前缀、目标注意力分离、code 生成与曝光排序联合训练；缺少百度生产特征、多目标头和在线基础设施，不能称为完整论文复现。仅用公开 item ID、标签、点击/长播与播放时长；没有百度的文本、发布者、细粒度反馈和多场景目标头。本地对照口径：同一早融合排序器、同数据和训练预算下，去掉联合 code 生成是基线，三 seed test CTR-AUC 均值约 0.5282；完整缩比实验组约 0.5270，相对 -0.23%。本地没有观察到稳定提升。  retrieval ranking generative-recommendation 搜广推 生成式召回与推理推荐 UNIQUE 为什么采用扁平 code，并让候选 item/code 只读取公共前缀而不互读？ 扁平码避免多层残差量化逐层积累误差，反馈双塔、频率校正与 EMA 让分配兼顾行为和码使用。候选各自只读取公共用户前缀，既共享编码又保持候选隔离，联合训练 code 分布与排序目标连接召回和判别。它用较大单层空间换取路径简化，码利用与碰撞问题仍需监测。 示意：同一用户有十个候选，各自读一份共同历史，不读取邻居候选信息。物品先分到单层 code 提名，再对桶内商品排序，避免多层早期量化错误逐级传递。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-unique-d194acb1" class="ar-learning-paper-anchor"></span>
<h2 id="qa-340940bae7589d13">UNIQUE 为什么采用扁平 code，并让候选 item/code 只读取公共前缀而不互读？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunique">UNIQUE: A Unified Retrieval and Ranking System for Large-Scale Feed Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>扁平码避免多层残差量化逐层积累误差，反馈双塔、频率校正与 EMA 让分配兼顾行为和码使用。候选各自只读取公共用户前缀，既共享编码又保持候选隔离，联合训练 code 分布与排序目标连接召回和判别。它用较大单层空间换取路径简化，码利用与碰撞问题仍需监测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一用户有十个候选，各自读一份共同历史，不读取邻居候选信息。物品先分到单层 code 提名，再对桶内商品排序，避免多层早期量化错误逐级传递。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.23718">原论文</a> · <a href="../../../../reproductions/2609.23718-unique/">实现解读</a> · <a href="#qa-340940bae7589d13">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:angle" data-paper-title="One-Step Retrieval Framework for Real-Time Sponsored Search Ads Using Hierarchical Text Representations" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="One-Step Retrieval Framework for Real-Time Sponsored Search Ads Using Hierarchical Text Representations 搜广推与 LLM 应用 Tencent 2026-09-16 以意图标识×摘要标识组织广告语义层次，用生成、判别和排序联合目标训练，并在请求侧动态约束 beam 只产生合法标识。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地在 MovieLens 100K 执行层次标识、联合打分和受约束检索；不使用腾讯私有广告日志或生产索引。本地在 MovieLens 100K 执行层次标识、联合打分和受约束检索；不使用腾讯私有广告日志或生产索引。本地 seeds 42/43/44 见 metrics/movielens-100k-seeds42-44.json。  sponsored-search generative-retrieval hierarchical-identifiers 搜广推 生成式召回与推理推荐 ANGLE有了层次广告标识，为什么解码时还要施加请求侧动态约束？ 标识层次只描述广告的组织方式，不保证每个请求都能投放所有合法组合。请求侧约束将库存、资格等条件落实到beam搜索，使不可服务标识在生成过程中被排除；生成、判别和排序目标再共同训练相关性。先任意生成再事后删掉无效项，可能浪费搜索预算且漏掉可用候选。 示意：同一意图下有多个广告摘要码，其中一项当前不可投；若等生成完再过滤，beam可能已被它占满，动态约束则把预算留给可服务广告。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-angle-c3d4b151" class="ar-learning-paper-anchor"></span>
<h2 id="qa-c4c49ab8f4fbbd8c">ANGLE有了层次广告标识，为什么解码时还要施加请求侧动态约束？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aangle">One-Step Retrieval Framework for Real-Time Sponsored Search Ads Using Hierarchical Text Representations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>标识层次只描述广告的组织方式，不保证每个请求都能投放所有合法组合。请求侧约束将库存、资格等条件落实到beam搜索，使不可服务标识在生成过程中被排除；生成、判别和排序目标再共同训练相关性。先任意生成再事后删掉无效项，可能浪费搜索预算且漏掉可用候选。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一意图下有多个广告摘要码，其中一项当前不可投；若等生成完再过滤，beam可能已被它占满，动态约束则把预算留给可服务广告。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.18296">原论文</a> · <a href="../../../../reproductions/2609.18296-angle/">实现解读</a> · <a href="#qa-c4c49ab8f4fbbd8c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tgr" data-paper-title="TGR: Advancing Industrial Recommendation from Generative-Paradigm Ranking toward Unified Generation and Reasoning" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="TGR: Advancing Industrial Recommendation from Generative-Paradigm Ranking toward Unified Generation and Reasoning 搜广推与 LLM 应用 Tencent 2026-09-01 TGR 把工业推荐的三个方向纳入同一框架：CCFormer 承担可扩展排序，BARGE/HiGR 用分层语义 ID 生成单物品或整页列表，TGR-Reason 把离线生成的 reason token 注入在线解码，避免请求时再做昂贵 rollout。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现分层语义 ID 路径、列表目标和 reason-token 注入的组合。未复刻私有 semantic-ID catalog、生产 CCFormer checkpoint 与在线生成服务；仅实现公开数据可审计核心机制。MovieLens 100K 三 seed 固定协议下 NDCG@10 从 0.05401 提升到 0.05953。完整产物见 metrics/public-seeds42-44.json。  generative-recommendation ranking-network reason-token 搜广推 生成式召回与推理推荐 TGR 为什么把可扩展排序、分层 SID 生成和离线 reason token 放在同一技术框架？ 排序负责细粒度判别，层级 SID 支持从单物品到整页生成，离线 reason token 则把昂贵推理准备成在线可消费条件。框架连接的是不同阶段的信息与计算，而非用一个新公式取代全部模块。理解时应分别检查生成路径、列表目标和推理接口；本地路径分数实现不能代表所有生产子系统都已重建。 示意：先离线整理用户可能的兴趣理由，生成器据此产生一页候选，再由扩展排序模型判断价值。请求时直接读取准备好的理由 token，不必重新运行长推理搜索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-tgr-d333ba35" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d75ea81538d30e34">TGR 为什么把可扩展排序、分层 SID 生成和离线 reason token 放在同一技术框架？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atgr">TGR: Advancing Industrial Recommendation from Generative-Paradigm Ranking toward Unified Generation and Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>排序负责细粒度判别，层级 SID 支持从单物品到整页生成，离线 reason token 则把昂贵推理准备成在线可消费条件。框架连接的是不同阶段的信息与计算，而非用一个新公式取代全部模块。理解时应分别检查生成路径、列表目标和推理接口；本地路径分数实现不能代表所有生产子系统都已重建。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先离线整理用户可能的兴趣理由，生成器据此产生一页候选，再由扩展排序模型判断价值。请求时直接读取准备好的理由 token，不必重新运行长推理搜索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.00986">原论文</a> · <a href="../../../../reproductions/2609.00986-tgr/">实现解读</a> · <a href="#qa-d75ea81538d30e34">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tagr" data-paper-title="TAGR: Temporally Adaptive Generative Recommendation for Industrial Live-Streaming Advertising" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="TAGR: Temporally Adaptive Generative Recommendation for Industrial Live-Streaming Advertising 搜广推与 LLM 应用 Kuaishou Technology 2026-08-25 直播间内容、商品和反馈高速变化，静态 semantic ID、单一时间尺度历史和离策略偏好优化都会过时。TAGR 在三层适配：LSID 周期刷新语义/协同分配但保持 token 词表稳定；IAG 融合短、中、长期意图；IOPO 间歇执行 on-policy GRPO，并在两次 burst 之间继续 NTP 维护，防止在线 RL 覆盖行为分布。 Fidelity：核心机制复现。本地执行稳定词表的可刷新 LSID、多尺度 intent 与行为/价值双分支；生产在线训练与广告系统未复刻。未使用快手私有日志、在线 reward model、真实 GRPO burst、广告价值标签和实时 serving；本地只验证三个核心适配结构及其在非时变公开数据上的失败边界。本地对照口径：基线为一阶转移与热度融合；实验组加入两级 LSID、三尺度 intent 和有界行为/价值门控。MovieLens-1M 上 NDCG@10 从 0.1123 降至 0.0821（-26.86%），但 head share 从 0.7275 降至 0.1303。  generative-recommendation live-streaming-advertising semantic-id online-rl 搜广推 生成式召回与推理推荐 TAGR 为什么把直播适应拆成码分配、兴趣时间尺度和间歇式策略更新三层？ 直播内容、用户意图和反馈分布以不同速度变化，只更新一处容易仍受其他过时环节限制。LSID 刷新分配但保持词表接口，IAG 融合短中长期兴趣，IOPO 在 on-policy 更新之间继续 NTP 维护行为分布。三层分别处理物品、用户和策略变化；本地有界门控不等同于完整在线 GRPO 闭环。 示意：直播间突然换商品，用户刚转向新兴趣，旧偏好策略也需校准。只改商品码无法解决后两者；间歇强化学习又配合常规序列训练，避免一次更新忘掉基础分布。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-tagr-4f20f91f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-2515cfaf4e666dc8">TAGR 为什么把直播适应拆成码分配、兴趣时间尺度和间歇式策略更新三层？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atagr">TAGR: Temporally Adaptive Generative Recommendation for Industrial Live-Streaming Advertising</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直播内容、用户意图和反馈分布以不同速度变化，只更新一处容易仍受其他过时环节限制。LSID 刷新分配但保持词表接口，IAG 融合短中长期兴趣，IOPO 在 on-policy 更新之间继续 NTP 维护行为分布。三层分别处理物品、用户和策略变化；本地有界门控不等同于完整在线 GRPO 闭环。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>直播间突然换商品，用户刚转向新兴趣，旧偏好策略也需校准。只改商品码无法解决后两者；间歇强化学习又配合常规序列训练，避免一次更新忘掉基础分布。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24034">原论文</a> · <a href="../../../../reproductions/2608.24034-tagr/">实现解读</a> · <a href="#qa-2515cfaf4e666dc8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sona" data-paper-title="Sona Technical Report" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Sona Technical Report 搜广推与 LLM 应用 Yandex 2026-08-11 Yandex Music 原链路有 15 个以上候选生成器与独立预排、精排。Sona 用 chronology event encoder 表示用户，以历史压缩控制长序列成本，自回归生成 Semantic ID，并用同一状态的 Ranking Module 对物品排序；高容量 teacher 只在训练期提供蒸馏监督。 Fidelity：核心机制复现。实际训练压缩历史编码器、三层自回归 Semantic ID 头与 item ranker；本地负迁移如实保留。未复刻私有音乐语义 tokenizer、完整 teacher、15+ 生产候选源和智能音箱 serving；本地仅验证核心训练与推理数据流。本地对照口径：基线为同预算共享 encoder 排序器，实验组为 history compression + SID decoder + item ranker；NDCG@10 相对变化 -92.05%。  generative-recommendation semantic-id ranking history-compression 搜广推 生成式召回与推理推荐 Sona 为什么让 SID 生成与排序模块共享用户状态，并只在训练期使用高容量 teacher？ 独立候选生成器与排序器会重复理解历史，也容易优化不同表示。Sona 用按时间编码并压缩的同一状态支持生成与物品排序，联合目标连接两条路径；教师只在训练期提供额外监督，服务保持较轻结构。共享状态不消除生成漏召问题，历史压缩也有损失，本地负结果不能用生产统一架构的描述覆盖。 示意：用户最近转听古典乐，生成器和排序头都读取同一更新后的状态，避免一边还按旧摇滚偏好召回。大教师训练时指导表示，上线无需为每次请求调用它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-sona-74c5ab5b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d656f31a07458ede">Sona 为什么让 SID 生成与排序模块共享用户状态，并只在训练期使用高容量 teacher？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asona">Sona Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Yandex</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立候选生成器与排序器会重复理解历史，也容易优化不同表示。Sona 用按时间编码并压缩的同一状态支持生成与物品排序，联合目标连接两条路径；教师只在训练期提供额外监督，服务保持较轻结构。共享状态不消除生成漏召问题，历史压缩也有损失，本地负结果不能用生产统一架构的描述覆盖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户最近转听古典乐，生成器和排序头都读取同一更新后的状态，避免一边还按旧摇滚偏好召回。大教师训练时指导表示，上线无需为每次请求调用它。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.11015">原论文</a> · <a href="../../../../reproductions/2608.11015-sona/">实现解读</a> · <a href="#qa-d656f31a07458ede">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pushdualgen" data-paper-title="PushDualGen: Enabling LLMs to Generate Semantic IDs with Interpretable Copy for Industrial Push Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="PushDualGen: Enabling LLMs to Generate Semantic IDs with Interpretable Copy for Industrial Push Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-08-08 先生成可服务的 Semantic ID，再按需生成可跳过的解释 copy；在线侧融合 SID 与 copy 表示，同时保留解释一致性。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation semantic-id llm-recommendation push 搜广推 生成式召回与推理推荐 PushDualGen 为什么先生成可服务 SID，再按门控决定是否继续生成解释文案？ SID 是实际推荐对象的稳定接口，先生成它可让候选即刻进入服务链路；解释以 SID 和历史为条件，只在需要时额外生成，避免所有请求都承担长文本成本。融合两侧表示并约束一致性，意在让文案围绕已选对象，而不是文案和商品各说各话；跳过文案时推荐路径仍需独立可用。 示意：用户只需要普通推荐时，生成商品码便返回；推送通知需要一句理由时，再围绕同一码生成文案。这样不能把“推荐跑鞋”配上“这本小说适合你”的解释。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-pushdualgen-379bfcda" class="ar-learning-paper-anchor"></span>
<h2 id="qa-2ef9c408f3412728">PushDualGen 为什么先生成可服务 SID，再按门控决定是否继续生成解释文案？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apushdualgen">PushDualGen: Enabling LLMs to Generate Semantic IDs with Interpretable Copy for Industrial Push Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>SID 是实际推荐对象的稳定接口，先生成它可让候选即刻进入服务链路；解释以 SID 和历史为条件，只在需要时额外生成，避免所有请求都承担长文本成本。融合两侧表示并约束一致性，意在让文案围绕已选对象，而不是文案和商品各说各话；跳过文案时推荐路径仍需独立可用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户只需要普通推荐时，生成商品码便返回；推送通知需要一句理由时，再围绕同一码生成文案。这样不能把“推荐跑鞋”配上“这本小说适合你”的解释。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.07989">原论文</a> · <a href="../../../../reproductions/2608.07989-pushdualgen/">实现解读</a> · <a href="#qa-2ef9c408f3412728">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gryphon-v2" data-paper-title="Gryphon-v2: One Model in Place of a Cascade — Generate-and-Rank Recommender with Rollout Distillation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Gryphon-v2: One Model in Place of a Cascade — Generate-and-Rank Recommender with Rollout Distillation 搜广推与 LLM 应用 Yandex 2026-08-06 Yandex 原系统包含 15 个以上召回器和独立预排/排序。Gryphon-v2 复用生成式推荐的共享 history encoder：生成头预测 Semantic ID，item-level ranking head 对生成候选直接排序；离线高容量 teacher 同时监督当前模型 rollout 和 logged impressions，从而让排序器见到 serving 分布与真实曝光分布。 Fidelity：核心机制复现。实现共享历史编码器、生成头、训练期 teacher、双来源 rollout 蒸馏与 item-level ranker；本地负结果如实保留。未复刻 Yandex 私有音乐/多模态 SID、8,000 长历史、十分钟在线更新和 Triton serving；公开数据只验证核心训练数据流。本地对照口径：基线为同预算生成式召回，实验组加入双来源蒸馏与 ranker；相对基线 NDCG@10 -26.84%。  generative-recommendation retrieval ranking rollout-distillation 搜广推 生成式召回与推理推荐 Gryphon-v2为什么同时蒸馏当前rollout候选和真实曝光候选？ 生成器改变后会产生日志中少见的候选，排序器若只学习旧曝光分布，就可能无法评价实际服务输出；只学当前rollout又会丢掉真实系统的成熟覆盖。双来源蒸馏让同一teacher同时校准两类候选，再通过共享encoder连接生成与排序。teacher偏差仍会传递，双数据源不等于自动消除分布错位。 示意：新生成器开始提出冷门电影，旧曝光日志只含热门片；rollout提供新候选判断，真实曝光保留既有经验，避免排序头只认识其中一种。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-gryphon-v2-65508cc1" class="ar-learning-paper-anchor"></span>
<h2 id="qa-68390dcde3890556">Gryphon-v2为什么同时蒸馏当前rollout候选和真实曝光候选？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agryphon-v2">Gryphon-v2: One Model in Place of a Cascade — Generate-and-Rank Recommender with Rollout Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Yandex</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>生成器改变后会产生日志中少见的候选，排序器若只学习旧曝光分布，就可能无法评价实际服务输出；只学当前rollout又会丢掉真实系统的成熟覆盖。双来源蒸馏让同一teacher同时校准两类候选，再通过共享encoder连接生成与排序。teacher偏差仍会传递，双数据源不等于自动消除分布错位。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新生成器开始提出冷门电影，旧曝光日志只含热门片；rollout提供新候选判断，真实曝光保留既有经验，避免排序头只认识其中一种。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06213">原论文</a> · <a href="../../../../reproductions/2608.06213-gryphon-v2/">实现解读</a> · <a href="#qa-68390dcde3890556">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hrpo" data-paper-title="Hierarchical Residual Policy Optimization for Generative Recommendations" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Hierarchical Residual Policy Optimization for Generative Recommendations 搜广推与 LLM 应用 City University of Hong Kong / Kuaishou 2026-08-01 主题：生成式推荐后训练。最终物品回报直接广播给所有 SID token 会造成稀疏且高方差的信用。HRPO 在用户簇内平滑 prefix utility，再分解 residual token credit 并累积 credit-to-go，最后用 RRPO 做保守更新。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。MovieLens-1M 上构造二进制层级 SID，实际计算 prefix smoothing、residual credit 与 credit-to-go。  generative-recommendation reinforcement-learning semantic-id credit-assignment 搜广推 生成式召回与推理推荐 HRPO为什么把最终回报拆成prefix residual credit和credit-to-go？ 整件物品的奖励广播到每枚SID token，会让不同决策承担相同责任并增加方差。HRPO先在用户簇内平滑前缀效用，再用相邻前缀的增量形成局部信用，累积后续影响帮助早期决策学习长期贡献。前缀价值是估计量，分解并不自动消除偏差，也不能在推理时读取真实目标路径。 示意：第一层选错品类可能决定整条路径失败，末层只是在类内微调；把相同奖励平分给所有码，难以区分这两种作用，前缀信用尝试定位差异。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-hrpo-d54751e8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d24dff680526ea54">HRPO为什么把最终回报拆成prefix residual credit和credit-to-go？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahrpo">Hierarchical Residual Policy Optimization for Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · City University of Hong Kong / Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>整件物品的奖励广播到每枚SID token，会让不同决策承担相同责任并增加方差。HRPO先在用户簇内平滑前缀效用，再用相邻前缀的增量形成局部信用，累积后续影响帮助早期决策学习长期贡献。前缀价值是估计量，分解并不自动消除偏差，也不能在推理时读取真实目标路径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第一层选错品类可能决定整条路径失败，末层只是在类内微调；把相同奖励平分给所有码，难以区分这两种作用，前缀信用尝试定位差异。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.00750">原论文</a> · <a href="../../../../reproductions/2608.00750-hrpo/">实现解读</a> · <a href="#qa-d24dff680526ea54">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:feedback-policy" data-paper-title="From Understanding to Action: Feedback-Grounded Policy Discovery for Generative Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="From Understanding to Action: Feedback-Grounded Policy Discovery for Generative Recommendation 搜广推与 LLM 应用 Huazhong Agricultural University (Kuaishou internship) 2026-07-30 从用户反馈发现生成策略，以双空间关系蒸馏把策略压入轻量排序器，从而避免线上调用 LLM。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation policy-optimization distillation 搜广推 生成式召回与推理推荐 Feedback Policy为什么蒸馏教师的关系矩阵，而不只模仿每个物品的独立分数？ 策略知识不仅在单项分数里，也在候选之间的相对关系中。关系蒸馏要求学生保留教师在对应空间内的相似或偏好结构，使轻量排序器吸收反馈发现的模式，而不在服务时运行LLM。若教师关系本身受偏置影响，学生也会继承；匹配矩阵误差下降并不等于用户反馈必然改善。 示意：两个商品单独分数相近，但教师知道它们在当前意图下互为替代；学生保留这种关系后可更好选择组合，而不仅逐个复制一个静态高分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-feedback-policy-7fbe9a73" class="ar-learning-paper-anchor"></span>
<h2 id="qa-3d327498079e2bb6">Feedback Policy为什么蒸馏教师的关系矩阵，而不只模仿每个物品的独立分数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Afeedback-policy">From Understanding to Action: Feedback-Grounded Policy Discovery for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huazhong Agricultural University (Kuaishou internship)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>策略知识不仅在单项分数里，也在候选之间的相对关系中。关系蒸馏要求学生保留教师在对应空间内的相似或偏好结构，使轻量排序器吸收反馈发现的模式，而不在服务时运行LLM。若教师关系本身受偏置影响，学生也会继承；匹配矩阵误差下降并不等于用户反馈必然改善。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个商品单独分数相近，但教师知道它们在当前意图下互为替代；学生保留这种关系后可更好选择组合，而不仅逐个复制一个静态高分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27789">原论文</a> · <a href="../../../../reproductions/2607.27789-feedback-policy/">实现解读</a> · <a href="#qa-3d327498079e2bb6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:snaplgr" data-paper-title="LLM-Based Generative Retrieval for Snapchat Content Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="LLM-Based Generative Retrieval for Snapchat Content Recommendation 搜广推与 LLM 应用 Snap Inc. 2026-07-30 先从共参与图传播内容相关性，再用分层残差量化形成 semantic ID；训练时把 SID token 与真实内容表征对齐，并学习用户序列到下一 SID 的生成转移。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为普通 residual SID，实验组加入共参与传播、grounding 与 SID transition；  retrieval generative-recommendation semantic-id llm multimodal 搜广推 生成式召回与推理推荐 SnapLGR 为什么先在共参与图传播，再量化为 SID，并对 token 做内容 grounding？ 原始内容向量未必包含平台上的协同行为，图传播先把共参与关系融入表示，再量化使这些关系进入离散路径。grounding 约束生成 token 仍对应实际内容，序列到下一 SID 的目标再学习用户转移。图信号、离散化与生成分别承担不同环节，热门共现偏差也可能沿传播进入码本。 示意：两类内容视觉不同却常被同一兴趣群体消费，传播后可在表示上关联；量化得到路径后仍需对齐原内容，避免用户生成某个码却无法稳定映回相关物品。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-snaplgr-28d916e6" class="ar-learning-paper-anchor"></span>
<h2 id="qa-e972912a0c70610f">SnapLGR 为什么先在共参与图传播，再量化为 SID，并对 token 做内容 grounding？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asnaplgr">LLM-Based Generative Retrieval for Snapchat Content Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Snap Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原始内容向量未必包含平台上的协同行为，图传播先把共参与关系融入表示，再量化使这些关系进入离散路径。grounding 约束生成 token 仍对应实际内容，序列到下一 SID 的目标再学习用户转移。图信号、离散化与生成分别承担不同环节，热门共现偏差也可能沿传播进入码本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两类内容视觉不同却常被同一兴趣群体消费，传播后可在表示上关联；量化得到路径后仍需对齐原内容，避免用户生成某个码却无法稳定映回相关物品。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28895">原论文</a> · <a href="../../../../reproductions/2607.28895-snaplgr/">实现解读</a> · <a href="#qa-e972912a0c70610f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:reward-guided-decoding" data-paper-title="Reward Guided Decoding for Generative Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Reward Guided Decoding for Generative Recommendation 搜广推与 LLM 应用 Institute of Information Engineering, Chinese Academy of Sciences 2026-07-28 保持生成器概率作为先验，在解码时用独立 reward 进行指数倾斜；闭式策略在提升期望 reward 的同时用 KL 温度限制偏离，无需重新训练生成器。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线按生成器似然解码，实验组用内容/新颖度 reward 做 KL 正则倾斜；seed 42 的 NDCG@10 为 0.02249，基线为 0.05401，负结果保留。  generative-recommendation decoding reward business-alignment 搜广推 生成式召回与推理推荐 奖励引导解码中的指数倾斜，为什么既保留生成器先验又受 KL 温度控制？ 最优受约束分布在原模型概率上乘以奖励的指数项，奖励较高的结果被提升，但原先极不可能的结果不会完全忽略先验地涌入。温度控制偏离代价，越小越强追逐奖励，越大越接近原分布。无需重训不代表无代价：奖励误差会改变解码方向，归一化与候选搜索也影响近似质量。 示意：原模型偏好熟悉影片，奖励鼓励新颖。适中温度可适度提升相关冷门片；温度过小则可能为新颖性挑出不合兴趣的片，因而不能只看奖励升高就说推荐更好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-reward-guided-decoding-a3100a32" class="ar-learning-paper-anchor"></span>
<h2 id="qa-0710a847a39d981a">奖励引导解码中的指数倾斜，为什么既保留生成器先验又受 KL 温度控制？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Areward-guided-decoding">Reward Guided Decoding for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Information Engineering, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最优受约束分布在原模型概率上乘以奖励的指数项，奖励较高的结果被提升，但原先极不可能的结果不会完全忽略先验地涌入。温度控制偏离代价，越小越强追逐奖励，越大越接近原分布。无需重训不代表无代价：奖励误差会改变解码方向，归一化与候选搜索也影响近似质量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>原模型偏好熟悉影片，奖励鼓励新颖。适中温度可适度提升相关冷门片；温度过小则可能为新颖性挑出不合兴趣的片，因而不能只看奖励升高就说推荐更好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25344">原论文</a> · <a href="../../../../reproductions/2607.25344-reward-guided-decoding/">实现解读</a> · <a href="#qa-0710a847a39d981a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:oxygenrec-v2" data-paper-title="OxygenREC-v2: Internalizing Discrimination into Generative Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OxygenREC-v2: Internalizing Discrimination into Generative Recommendation 搜广推与 LLM 应用 JD.COM 2026-07-27 工业生成式推荐通常先生成候选，再外挂判别器或 reward model 重排；重排只能改变顺序，不能补回生成阶段漏掉的商品。OxygenREC-v2 把 click/cart/order 行为作为 decoder instruction，从第一枚 SID token 起控制候选生成；后训练再使用仅训练期可见的未来交互，联合可验证轨迹优化、自蒸馏和高熵位置的 forward-KL。 Fidelity: 核心机制复现。实际训练行为 instruction、行为加权目标、未来交互 privileged view 与熵路由蒸馏；生产模型和私有漏斗数据未复刻。这是核心机制的小规模复现，不含京东私有多行为日志、三层生产 SID、3B-A1B MoE 和线上服务。负结果主要说明“流行度分位”不是购买意图的可靠替代，不否定论文的私有数据结论。本地对照口径：基线与实验组使用同一 MovieLens 切片、full-catalog 候选、训练步数和 seed；实验组只增加论文机制，相对 NDCG@10 为 -54.09%。  generative-recommendation privileged-distillation behavior-instruction 搜广推 生成式召回与推理推荐 OxygenREC-v2 为什么从第一枚 SID 就注入行为指令，并按不确定性选择不同的后训练约束？ 只在生成后重排不能补回已经漏掉的商品，行为指令因此直接进入解码前缀，让点击、加购或下单目标影响整条生成路径。后训练借助仅训练时可见的未来交互，低熵位置接受较确定的教师信号，高熵位置用 forward-KL 保留多种可能。未来信息用于监督而不进入线上输入，是机制成立的关键边界。 示意：要优化下单时，模型从首个语义码就偏向可购买候选。若某一分支有多种合理商品，训练不把它硬压成唯一答案；请求时仍只能依据当前已知历史生成。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-oxygenrec-v2-987866fe" class="ar-learning-paper-anchor"></span>
<h2 id="qa-707ccd2ae0c3750c">OxygenREC-v2 为什么从第一枚 SID 就注入行为指令，并按不确定性选择不同的后训练约束？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aoxygenrec-v2">OxygenREC-v2: Internalizing Discrimination into Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · JD.COM</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只在生成后重排不能补回已经漏掉的商品，行为指令因此直接进入解码前缀，让点击、加购或下单目标影响整条生成路径。后训练借助仅训练时可见的未来交互，低熵位置接受较确定的教师信号，高熵位置用 forward-KL 保留多种可能。未来信息用于监督而不进入线上输入，是机制成立的关键边界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>要优化下单时，模型从首个语义码就偏向可购买候选。若某一分支有多种合理商品，训练不把它硬压成唯一答案；请求时仍只能依据当前已知历史生成。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24255">原论文</a> · <a href="../../../../reproductions/2607.24255-oxygenrec-v2/">实现解读</a> · <a href="#qa-707ccd2ae0c3750c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unir2" data-paper-title="Unifying Generative Recall and Multi-Objective Ranking in a Single Decoder-Only Sequence" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Unifying Generative Recall and Multi-Objective Ranking in a Single Decoder-Only Sequence 搜广推与 LLM 应用 Kuaishou / IIE, CAS / UCAS 2026-07-27 传统工业 cascade 分别训练 recall 和 ranking：两边重复编码用户历史，生成轨迹在候选交接时丢失，训练目标也可能冲突。UniR² 把用户上下文、目标物品 SID 轨迹和 item ranking features 拼成一个 decoder-only 异构序列，让生成轨迹成为召回与排序之间的表示桥。DQ-PCA 为同一层提供两种 query：generation query 只能读取完整用户 prefix 和此前 SID； 本地使用两级 16-way SID，而非三层 8129 codebook，也未运行 beam search、3×640 服务模型和流水线并行。Fidelity: 核心机制复现。实际训练层级 SID、Dual-Query Prefix-Causal Attention、ranking-only LoRA 和生成/排序联合目标；缩小 codebook、模型和业务标签。MovieLens next-item 与 genre-affinity 代理快手 click/long-view/gift；  generative-recommendation unified-recall-ranking multi-objective-ranking lora 搜广推 生成式召回与推理推荐 UniR² 为什么让排序分支读取 SID 轨迹，却对共享输出 stop-gradient 并只学习 LoRA？ SID 轨迹包含召回时逐级选择的中间信息，保留它可作为生成与排序的表示桥。两类 query 用不同掩码读取所需上下文，排序分支再对共享输出停止梯度，只通过低秩增量学习专有交互，防止排序目标破坏生成主干。它共享前向知识但控制反向干扰，并非所有任务梯度都无约束混合。 示意：生成器先走“户外—露营—帐篷”路径，排序器可利用整条轨迹判断具体商品。若排序偏好变化，先调整排序 LoRA，而不直接把生成器原本学好的路径语义改乱。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-unir2-b2b6f557" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d829ee3c55f372e7">UniR² 为什么让排序分支读取 SID 轨迹，却对共享输出 stop-gradient 并只学习 LoRA？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunir2">Unifying Generative Recall and Multi-Objective Ranking in a Single Decoder-Only Sequence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou / IIE, CAS / UCAS</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>SID 轨迹包含召回时逐级选择的中间信息，保留它可作为生成与排序的表示桥。两类 query 用不同掩码读取所需上下文，排序分支再对共享输出停止梯度，只通过低秩增量学习专有交互，防止排序目标破坏生成主干。它共享前向知识但控制反向干扰，并非所有任务梯度都无约束混合。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>生成器先走“户外—露营—帐篷”路径，排序器可利用整条轨迹判断具体商品。若排序偏好变化，先调整排序 LoRA，而不直接把生成器原本学好的路径语义改乱。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24439">原论文</a> · <a href="../../../../reproductions/2607.24439-unir2/">实现解读</a> · <a href="#qa-d829ee3c55f372e7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:egr" data-paper-title="EGR: Embedding-Native Generative Retrieval with a Shared LLM" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="EGR: Embedding-Native Generative Retrieval with a Shared LLM 搜广推与 LLM 应用 Snap Inc. 2026-07-25 同一编码骨干产生 item 索引向量和 user query 向量，并让 item representation learning 与 next-item prediction 全程联合训练。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 EGR 为 0.05025，相对变化 -6.95%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  retrieval generative-retrieval shared-encoder 搜广推 生成式召回与推理推荐 EGR让item索引与user查询共用骨干，为什么仍要联合训练两个任务？ 共享参数只提供计算与表示联系，不保证两侧在检索空间中自然匹配。item表示学习维护可索引内容，next-item目标让用户查询朝实际消费关系调整，两种监督共同决定空间几何。若独立冻结一侧而另一侧持续变化，索引可能陈旧；联合训练后的向量仍需以一致版本建库和评估。 示意：商品编码因新训练发生旋转，用户查询却沿旧方向打分，会破坏近邻关系；两个目标共同训练有助对齐，但服务索引也要按对应版本更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-egr-a66d7f0c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-72f235af74f628cc">EGR让item索引与user查询共用骨干，为什么仍要联合训练两个任务？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aegr">EGR: Embedding-Native Generative Retrieval with a Shared LLM</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Snap Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共享参数只提供计算与表示联系，不保证两侧在检索空间中自然匹配。item表示学习维护可索引内容，next-item目标让用户查询朝实际消费关系调整，两种监督共同决定空间几何。若独立冻结一侧而另一侧持续变化，索引可能陈旧；联合训练后的向量仍需以一致版本建库和评估。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>商品编码因新训练发生旋转，用户查询却沿旧方向打分，会破坏近邻关系；两个目标共同训练有助对齐，但服务索引也要按对应版本更新。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.23038">原论文</a> · <a href="../../../../reproductions/2607.23038-egr/">实现解读</a> · <a href="#qa-72f235af74f628cc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:barge" data-paper-title="Bridging the Structural Gap: Adapting Autoregressive Generation for Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Bridging the Structural Gap: Adapting Autoregressive Generation for Recommendation 搜广推与 LLM 应用 Tencent 2026-07-23 RQ-VAE 把一个 item 展成多个 Semantic-ID token 后，普通 Transformer 会丢失 item 边界；单量化路径还会让早期 beam 偏差逐层放大。BARGE 用 ICA 将同一 item 的 token 聚合后门控回写，用 HPR 对累计语义路径做逐层对比重排，并通过正交切分产生两条互补解码路径。 Fidelity: 核心机制复现。实际训练 OSQ 双语义路径、ICA、HPR、双 decoder 与 item-space OR-fusion；缩小公开数据与服务规模。MovieLens genre 替代腾讯 item embedding；全库 teacher-forced path scoring 替代生产 beam kernel，未使用私有曝光负例和线上 serving。OSQ、ICA、HPR、DPD 均真实训练，但本地百分比不对应论文线上 lift。本地对照口径：基线是同 width、层数、训练行、optimizer 和 140 steps 的 single-path RQ-VAE/TIGER；  generative-recommendation semantic-id reranking 搜广推 生成式召回与推理推荐 BARGE为什么既修复同一物品的token边界，又对累计语义路径重排？ 一个物品被展开为多层SID后，普通序列注意力可能把局部码当独立事件，ICA先聚合物品上下文再门控回写。HPR则对已经生成的累计路径判断相关性，缓解早期beam偏差向深层扩散；互补量化路径进一步提供不同分解视角。三者分别处理表示边界、搜索误差和路径多样性。 示意：商品的三层码像同一地址的省、市、街道，不能当三次独立购买；若省级候选已选偏，后面只细分街道也难补救，因此要逐层检查路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-barge-1cfb2666" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1164e6c8c83dd97c">BARGE为什么既修复同一物品的token边界，又对累计语义路径重排？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Abarge">Bridging the Structural Gap: Adapting Autoregressive Generation for Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一个物品被展开为多层SID后，普通序列注意力可能把局部码当独立事件，ICA先聚合物品上下文再门控回写。HPR则对已经生成的累计路径判断相关性，缓解早期beam偏差向深层扩散；互补量化路径进一步提供不同分解视角。三者分别处理表示边界、搜索误差和路径多样性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>商品的三层码像同一地址的省、市、街道，不能当三次独立购买；若省级候选已选偏，后面只细分街道也难补救，因此要逐层检查路径。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21028">原论文</a> · <a href="../../../../reproductions/2607.21028-barge/">实现解读</a> · <a href="#qa-1164e6c8c83dd97c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tsgr" data-paper-title="TSGR: Taobao Search Generative Retrieval" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="TSGR: Taobao Search Generative Retrieval 搜广推与 LLM 应用 Taobao &amp; Tmall Group of Alibaba / Zhejiang University 2026-07-21 淘宝搜索的生成式召回不仅要找到相关商品，还要把商业价值直接带进生成路径。TSGR 先用 residual quantization 生成语义前缀，再为同一前缀下的商品并行分配全局价值码和 query-conditioned 价值码；最后用与生成 backbone 联合训练的 Value-aware Ranking Module（VRM）完成精细排序，避免把独立预排器硬接在生成器后面。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实执行并行价值 Semantic ID 和联合 VRM；私有淘宝日志与生产 serving 未复刻。本地在 MovieLens 100K 上真实构建两级 residual semantic prefix、全局/条件价值码，并用 23,027 个加权正例和 115,135 个负例拟合联合 VRM；融合权重只在 validation 上选择。  generative-retrieval semantic-id search pre-ranking 搜广推 生成式召回与推理推荐 TSGR 为什么在同一语义前缀下同时分配全局和 query-conditioned 价值码？ 语义前缀先组织商品相关性，但同一主题下的商业价值既有全局差异，也随查询而变。两套并行价值码把这两种信号带入生成路径，联合训练的 VRM 再结合生成状态与商品信息精细评分，避免完全独立的预排器割裂目标。价值代理与真实业务标签需区分，本地公开评分构造不能代表真实交易价值。 示意：同一款相机配件整体销量一般，但在“微距摄影”查询下很有价值。全局码表达总体表现，条件码表达该查询的特殊价值，精细模块再综合判断。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-tsgr-1abc60bc" class="ar-learning-paper-anchor"></span>
<h2 id="qa-3a964a889b237327">TSGR 为什么在同一语义前缀下同时分配全局和 query-conditioned 价值码？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atsgr">TSGR: Taobao Search Generative Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group of Alibaba / Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语义前缀先组织商品相关性，但同一主题下的商业价值既有全局差异，也随查询而变。两套并行价值码把这两种信号带入生成路径，联合训练的 VRM 再结合生成状态与商品信息精细评分，避免完全独立的预排器割裂目标。价值代理与真实业务标签需区分，本地公开评分构造不能代表真实交易价值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一款相机配件整体销量一般，但在“微距摄影”查询下很有价值。全局码表达总体表现，条件码表达该查询的特殊价值，精细模块再综合判断。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.18796">原论文</a> · <a href="../../../../reproductions/2607.18796-tsgr/">实现解读</a> · <a href="#qa-3a964a889b237327">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recgpt-v3" data-paper-title="RecGPT-V3 Technical Report" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="RecGPT-V3 Technical Report 搜广推与 LLM 应用 Alibaba / Taobao 2026-07-17 RecGPT-V1 把用户意图引入推荐链路，V2 用多智能体扩展推理，但每次请求仍重复读取最长约 55K token 的完整历史；自然语言 tag 到商品又形成有损瓶颈，显式 CoT 的数千 token 也无法承受高 QPS。V3 同时改造三处：Memory Hub 将完整行为压成带行为模式、偏好摘要、原始行为索引和时间信息的可追溯 memory unit；新行为只更新相关 unit 或创建新 unit。 Fidelity: 核心机制复现。实际训练两级 Semantic ID、结构化 Memory Hub、显式教师到 latent token 的重建蒸馏和 ranking-feedback；基础模型、数据与线上系统缩小。本地真实训练了两级 RQ-VAE、SID/text item tower、显式教师、memory attention、latent 多段重建和 dense ranking-feedback KL；MovieLens genre 替代淘宝文本/图像/属性，520 items 替代工业商品池，公开 teacher+popularity reward 替代生产 CTR ranker。  generative-recommendation semantic-id user-memory latent-reasoning 搜广推 生成式召回与推理推荐 RecGPT-V3 为什么同时改记忆、商品接口和推理表示，而不是只压缩显式 CoT？ 仅压缩 CoT 仍会反复读取长历史，也保留自然语言标签映射商品的损失。Memory Hub 增量更新可追溯记忆单元，SID 连接模型与实际商品，潜在 token 再减少输出推理文本的成本。三者分别针对输入重算、输出落地与解码开销；生产排序反馈还参与对齐，不能把总体收益归因于单个压缩步骤。 示意：新增一次相机浏览时，只更新相关摄影记忆，而非重读所有历史；生成器直接输出商品码，内部短推理提供支持。三处节省来自不同环节，不能只统计少写了多少字。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-recgpt-v3-d1c7b19e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-7fce71e69a1528f4">RecGPT-V3 为什么同时改记忆、商品接口和推理表示，而不是只压缩显式 CoT？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecgpt-v3">RecGPT-V3 Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>仅压缩 CoT 仍会反复读取长历史，也保留自然语言标签映射商品的损失。Memory Hub 增量更新可追溯记忆单元，SID 连接模型与实际商品，潜在 token 再减少输出推理文本的成本。三者分别针对输入重算、输出落地与解码开销；生产排序反馈还参与对齐，不能把总体收益归因于单个压缩步骤。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新增一次相机浏览时，只更新相关摄影记忆，而非重读所有历史；生成器直接输出商品码，内部短推理提供支持。三处节省来自不同环节，不能只统计少写了多少字。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.15591">原论文</a> · <a href="../../../../reproductions/2607.15591-recgpt-v3/">实现解读</a> · <a href="#qa-7fce71e69a1528f4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:guess-where-you-go" data-paper-title="Guess Where You Go: Generative Next Point-of-Interest Recommendation in Amap" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Guess Where You Go: Generative Next Point-of-Interest Recommendation in Amap 搜广推与 LLM 应用 Amap / Alibaba 2026-07-13 把下一 POI 编成 Semantic ID 序列，并用时空特征、课程式预训练/SFT 与 EAKTO 强化优化长周期用户反馈。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation next-poi semantic-id reinforcement-learning 搜广推 生成式召回与推理推荐 下一POI生成为什么需要时空上下文，不能只把地点名当普通商品ID？ 地点选择受距离、时间与出行状态限制，相同兴趣在不同位置未必可执行。语义ID提供层次表示，时空特征限定当前需求，课程式训练再逐步适应更复杂反馈。长期奖励优化仍需要对应观测，不能把静态地点共现或一次命中直接当真实路线规划与长期出行收益。 示意：用户喜欢咖啡馆，但早晨上班途中和周末远游时可去的店不同；模型要结合当前时间与位置，而不能只重复历史里最常访问的店名。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-guess-where-you-go-0a00ce9c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-51385eee77e0ff0e">下一POI生成为什么需要时空上下文，不能只把地点名当普通商品ID？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aguess-where-you-go">Guess Where You Go: Generative Next Point-of-Interest Recommendation in Amap</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Amap / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>地点选择受距离、时间与出行状态限制，相同兴趣在不同位置未必可执行。语义ID提供层次表示，时空特征限定当前需求，课程式训练再逐步适应更复杂反馈。长期奖励优化仍需要对应观测，不能把静态地点共现或一次命中直接当真实路线规划与长期出行收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户喜欢咖啡馆，但早晨上班途中和周末远游时可去的店不同；模型要结合当前时间与位置，而不能只重复历史里最常访问的店名。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26073">原论文</a> · <a href="../../../../reproductions/2607.26073-guess-where-you-go/">实现解读</a> · <a href="#qa-51385eee77e0ff0e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rag-generation" data-paper-title="Recommendation as Generation: Unifying Personalized Video Generation and Recommendation at Industrial Scale" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Recommendation as Generation: Unifying Personalized Video Generation and Recommendation at Industrial Scale 搜广推与 LLM 应用 Kuaishou / Beihang University 2026-06-24 用解耦语义 ID 连接生成式推荐与兴趣条件视频生成，并以跨域 reward 协调候选选择和内容创建。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 RaG 为 0.04235，相对变化 -21.59%。仅验证 D-SID 接口，视频生成器未复刻；生产线上 lift 的外推不适用。  generative-recommendation semantic-id video-generation 搜广推 生成式召回与推理推荐 RaG 为什么用解耦 SID 连接推荐选择和内容生成，而不是把两者当成同一个输出任务？ 推荐需要在既有内容中找到合适对象，内容生成还要控制创作属性，两类信息若混在单一编码里会互相牵制。解耦 SID 为内容与创意因素提供接口，再以跨域奖励协调“推荐什么”和“怎样生成”。接口一致不代表已实现完整生成器；本地只验证离散接口，不能据此宣称视频生成质量或端到端业务收益。 示意：用户偏好露营教学，内容码表达露营主题，创意码控制镜头或呈现方式。推荐侧先判断主题是否合适，生成侧再按创意条件制作，二者共享接口而职责不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-rag-generation-6f1ef070" class="ar-learning-paper-anchor"></span>
<h2 id="qa-151971fc5f0ff942">RaG 为什么用解耦 SID 连接推荐选择和内容生成，而不是把两者当成同一个输出任务？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arag-generation">Recommendation as Generation: Unifying Personalized Video Generation and Recommendation at Industrial Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou / Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>推荐需要在既有内容中找到合适对象，内容生成还要控制创作属性，两类信息若混在单一编码里会互相牵制。解耦 SID 为内容与创意因素提供接口，再以跨域奖励协调“推荐什么”和“怎样生成”。接口一致不代表已实现完整生成器；本地只验证离散接口，不能据此宣称视频生成质量或端到端业务收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户偏好露营教学，内容码表达露营主题，创意码控制镜头或呈现方式。推荐侧先判断主题是否合适，生成侧再按创意条件制作，二者共享接口而职责不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.25496">原论文</a> · <a href="../../../../reproductions/2606.25496-rag-generation/">实现解读</a> · <a href="#qa-151971fc5f0ff942">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:qgs" data-paper-title="From Item-Only to Query-Item: Query-Conditioned Generative Search with QGS in Quark" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="From Item-Only to Query-Item: Query-Conditioned Generative Search with QGS in Quark 搜广推与 LLM 应用 University of Science and Technology of China / Alibaba 2026-05-25 将 query 与 item 共同序列化做生成式搜索，Linear HSTU 以线性复杂度编码历史，HFG-Attention 再融合稀疏交叉特征。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-search search-ranking long-sequence 搜广推 生成式召回与推理推荐 QGS 为什么将 query 与 item 共同序列化，还要用特征交互模块补充历史编码？ 共同序列化使生成概率直接以当前查询和历史为条件，模型在生成物品路径时就处理搜索意图，而非先给出通用用户向量。历史编码控制长上下文开销，HFG-Attention 再融合稀疏字段交叉，补足仅靠序列表示难覆盖的异构关系。这里的效率设计属于该具体结构，不能推广成所有 HSTU 注意力都线性。 示意：同一用户搜索“旅行相机”和“室内灯具”应走不同生成路径。查询进入序列后，历史被按当前意图解释；设备、地区等稀疏字段再通过交互模块影响候选选择。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-qgs-de75c3ea" class="ar-learning-paper-anchor"></span>
<h2 id="qa-9c44591d27ec4e42">QGS 为什么将 query 与 item 共同序列化，还要用特征交互模块补充历史编码？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aqgs">From Item-Only to Query-Item: Query-Conditioned Generative Search with QGS in Quark</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共同序列化使生成概率直接以当前查询和历史为条件，模型在生成物品路径时就处理搜索意图，而非先给出通用用户向量。历史编码控制长上下文开销，HFG-Attention 再融合稀疏字段交叉，补足仅靠序列表示难覆盖的异构关系。这里的效率设计属于该具体结构，不能推广成所有 HSTU 注意力都线性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一用户搜索“旅行相机”和“室内灯具”应走不同生成路径。查询进入序列后，历史被按当前意图解释；设备、地区等稀疏字段再通过交互模块影响候选选择。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.25514">原论文</a> · <a href="../../../../reproductions/2605.25514-qgs/">实现解读</a> · <a href="#qa-9c44591d27ec4e42">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:growthgr" data-paper-title="Towards Sustainable Growth: A Multi-Value-Aware Retrieval Framework for E-Commerce Search" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Towards Sustainable Growth: A Multi-Value-Aware Retrieval Framework for E-Commerce Search 搜广推与 LLM 应用 Alibaba Group / Taobao &amp; Tmall 2026-05-18 新品只按即时成交优化会持续缺曝光。GrowthGR 用 counterfactual ItemLTV 估计点击带来的长期订单增量，再以 RQ-VAE SID 和 decoder-only generator 召回；MoPO 联合购买、点击、曝光、排序和高 uplift 标签，并用 clipped inverse propensity 强化稀有高价值物品。 Fidelity: 核心机制复现。ItemLTV、三层 Semantic ID、NTP、MoPO/GRPO clipped update 与有效 SID 约束均实际执行。未来正反馈频次代理 7 日订单，公开数据不支持还原真实搜索漏斗和多模态商品 foundation embedding。本地对照口径：基线是同一 transition policy 的 NTP retrieval；实验组 GrowthGR 加入 ItemLTV 与 8 轮 MoPO，相对基线 Hit@10 +0.00%、NDCG@10 +2.05%。  generative-recommendation reinforcement-learning new-items 搜广推 生成式召回与推理推荐 GrowthGR为什么用ItemLTV增量价值和多目标后训练，而不是只提高新品的即时曝光？ 给新品曝光本身不是最终目标，重要的是这次机会能否带来未来订单或其他长期价值。ItemLTV尝试区分原本会发生的结果与干预增量，多目标优化再协调点击、购买和覆盖；对稀有高价值动作的强化需要截断以防权重失控。反事实估计与奖励设计都需验证，不能把新品量增加直接当增长。 示意：两件新品同样少曝光，一件能打开持续消费场景，另一件只得到一次误触；均匀加流量无法区分，长期价值估计试图把机会分给更有增量的一件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-growthgr-aa9df061" class="ar-learning-paper-anchor"></span>
<h2 id="qa-fcd351b4112088fb">GrowthGR为什么用ItemLTV增量价值和多目标后训练，而不是只提高新品的即时曝光？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agrowthgr">Towards Sustainable Growth: A Multi-Value-Aware Retrieval Framework for E-Commerce Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group / Taobao &amp; Tmall</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>给新品曝光本身不是最终目标，重要的是这次机会能否带来未来订单或其他长期价值。ItemLTV尝试区分原本会发生的结果与干预增量，多目标优化再协调点击、购买和覆盖；对稀有高价值动作的强化需要截断以防权重失控。反事实估计与奖励设计都需验证，不能把新品量增加直接当增长。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两件新品同样少曝光，一件能打开持续消费场景，另一件只得到一次误触；均匀加流量无法区分，长期价值估计试图把机会分给更有增量的一件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.17994">原论文</a> · <a href="../../../../reproductions/2605.17994-growthgr/">实现解读</a> · <a href="#qa-fcd351b4112088fb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cq-sid" data-paper-title="Efficient Generative Retrieval for E-commerce Search with Semantic Cluster IDs and Expert-Guided RL" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Efficient Generative Retrieval for E-commerce Search with Semantic Cluster IDs and Expert-Guided RL 搜广推与 LLM 应用 Alibaba Taobao &amp; Tmall Group 2026-05-14 论文让首级 SID 服从商品类目，再用残差码表达类目内差异；Expert-Guided RL 组合点击、购买、语义与约束信号优化生成检索。 Fidelity: 核心机制复现。实现类目约束 Semantic ID、残差量化、多信号奖励和 EG-GRPO 更新。没有复刻 64-GPU 渐进训练、Tmall 私有 query log 和生产 beam service；EG-GRPO 更新本身真实执行。本地对照口径：基线是协同 item-ID 检索；实验组执行 CQ-SID 与 240 次 group-relative policy update；NDCG@10 相对 +1.66%。  generative-retrieval semantic-id reinforcement-learning 搜广推 生成式召回与推理推荐 CQ-SID把商品类目固定在首级码，会给生成式召回带来什么好处与代价？ 首级类目为生成路径提供明确的粗层组织，使后续残差码只需表达类内差异，也方便加入业务与语义约束。代价是类目错误会在很早阶段限制可达候选，跨类替代关系也不能被默认当成同一路径。专家引导奖励用于协调点击、购买和约束，不能只靠类目结构保证相关性。 示意：先选鞋类再生成鞋款细码，搜索更有组织；若多功能商品被错误归为箱包，首层约束可能阻止模型在鞋类请求中找到它，需要单独处理分类和跨类需求。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-cq-sid-a55bb5d1" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b4f87d7ed4915a2b">CQ-SID把商品类目固定在首级码，会给生成式召回带来什么好处与代价？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acq-sid">Efficient Generative Retrieval for E-commerce Search with Semantic Cluster IDs and Expert-Guided RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Taobao &amp; Tmall Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>首级类目为生成路径提供明确的粗层组织，使后续残差码只需表达类内差异，也方便加入业务与语义约束。代价是类目错误会在很早阶段限制可达候选，跨类替代关系也不能被默认当成同一路径。专家引导奖励用于协调点击、购买和约束，不能只靠类目结构保证相关性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先选鞋类再生成鞋款细码，搜索更有组织；若多功能商品被错误归为箱包，首层约束可能阻止模型在鞋类请求中找到它，需要单独处理分类和跨类需求。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.14434">原论文</a> · <a href="../../../../reproductions/2605.14434-cq-sid/">实现解读</a> · <a href="#qa-b4f87d7ed4915a2b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:univa" data-paper-title="Unified Value Alignment for Generative Recommendation in Industrial Advertising" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Unified Value Alignment for Generative Recommendation in Industrial Advertising 搜广推与 LLM 应用 Tencent / WeChat Channels 2026-05-07 传统生成式推荐主要优化用户行为匹配，却没有直接表示广告主的出价、ROI、优化目标等商业价值；工业广告还要求生成路径合法、满足请求级库存约束。UniVA 将“用户偏好、商业价值、可投放性”放进同一套生成式模型：Commercial SID 在语义 token 后编码商业属性；Generation-as-Ranking 用生成头和价值头联合给路径打分；eCPM-aware RL 让策略直接偏向请求内相对高价值广告；个性化 trie 则保证 beam 只沿当前请求可投放的广告路径展开。论文的三项关键改动是： Commercial token 的机制诊断是正向的：以相同前两级语义前缀分组，组内 bid proxy 的平均标准差由 0.34956 降至 0.09773（-72.04%）。Fidelity: 完整核心链路。本地实际执行 Commercial SID、HSTU 用户编码、cross-attention → causal self-attention 解码、MoR、共享专家 + top-k Sparse MoE、generation/value 双头、监督学习与 PPO/value 交替训练，以及 value-guided 个性化 trie beam search。  generative-advertising commercial-sid ppo value-aware-serving 搜广推 生成式召回与推理推荐 UniVA 为什么同时需要 Commercial SID、生成价值头和请求级个性化 trie？ 商业码把出价等属性带入输出路径，生成与价值 logit 相加让解码同时考虑相关性和商业价值，eCPM 奖励再调整策略。请求级 trie 则解决另一件事：只有当前可投放广告才可沿路径生成。价值高不意味着合法可投放，合法也不意味着用户相关，三类信号缺一不可；本地价值是公开数据代理。 示意：某广告出价高，但当前地区无库存，必须由请求 trie 禁止生成；另一条合法广告再由相关性和价值联合评分，不能只凭商业码就绕过投放约束。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-univa-ad679aba" class="ar-learning-paper-anchor"></span>
<h2 id="qa-9b382078c2f77bfb">UniVA 为什么同时需要 Commercial SID、生成价值头和请求级个性化 trie？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Auniva">Unified Value Alignment for Generative Recommendation in Industrial Advertising</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent / WeChat Channels</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>商业码把出价等属性带入输出路径，生成与价值 logit 相加让解码同时考虑相关性和商业价值，eCPM 奖励再调整策略。请求级 trie 则解决另一件事：只有当前可投放广告才可沿路径生成。价值高不意味着合法可投放，合法也不意味着用户相关，三类信号缺一不可；本地价值是公开数据代理。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某广告出价高，但当前地区无库存，必须由请求 trie 禁止生成；另一条合法广告再由相关性和价值联合评分，不能只凭商业码就绕过投放约束。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.05803">原论文</a> · <a href="../../../../reproductions/2605.05803-univa/">实现解读</a> · <a href="#qa-9b382078c2f77bfb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:genrec" data-paper-title="GenRec: A Preference-Oriented Generative Framework for Large-Scale Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="GenRec: A Preference-Oriented Generative Framework for Large-Scale Recommendation 搜广推与 LLM 应用 JD.com 2026-04-16 逐 item 生成忽略同一页面内的互补和顺序。GenRec 将下一页作为序列目标，用非对称 Token Merger 压缩输入，并以 GRPO-SR 的组内 reward 优化整页，同时保留 NLL 正则抑制策略漂移。 复现保真度：核心机制复现。复现保真度：核心机制复现。Page-wise NTP、非对称 Token Merger 与 GRPO-SR/NLL 约束实际执行。把连续三个正反馈组成一页，联合估计 page policy，并用序位 reward advantage 更新、NLL policy 约束。  generative-recommendation grpo page-wise 搜广推 生成式召回与推理推荐 GenRec为什么把下一页作为序列目标，并在GRPO旁保留NLL约束？ 单item监督只告诉模型下一件是什么，不能直接学同页顺序与互补。页面序列目标表达组合关系，组内reward优势推动整页效果；NLL继续约束日志支持的行为，减少只追奖励造成的策略漂移。若页面奖励遗漏相关性或可行性，生成整页也可能放大偏差，不能把reward上升直接当用户满意。 示意：三件内容分别高分却高度重复，页面目标可以学到替换其中一件；但若只奖励新颖，可能生成不相关内容，NLL帮助限制这种偏离。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-genrec-e5f875fa" class="ar-learning-paper-anchor"></span>
<h2 id="qa-e1b9b517b34000d1">GenRec为什么把下一页作为序列目标，并在GRPO旁保留NLL约束？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agenrec">GenRec: A Preference-Oriented Generative Framework for Large-Scale Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · JD.com</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单item监督只告诉模型下一件是什么，不能直接学同页顺序与互补。页面序列目标表达组合关系，组内reward优势推动整页效果；NLL继续约束日志支持的行为，减少只追奖励造成的策略漂移。若页面奖励遗漏相关性或可行性，生成整页也可能放大偏差，不能把reward上升直接当用户满意。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三件内容分别高分却高度重复，页面目标可以学到替换其中一件；但若只奖励新颖，可能生成不相关内容，NLL帮助限制这种偏离。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.14878">原论文</a> · <a href="../../../../reproductions/2604.14878-genrec/">实现解读</a> · <a href="#qa-e1b9b517b34000d1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unirec-coa" data-paper-title="UniRec: Bridging the Expressive Gap between Generative and Discriminative Recommendation via Chain-of-Attribute" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="UniRec: Bridging the Expressive Gap between Generative and Discriminative Recommendation via Chain-of-Attribute 搜广推与 LLM 应用 Authors did not disclose affiliation / large-scale e-commerce platform 2026-04-14 在 SID 前生成品类、卖家和品牌等属性链，用容量受限量化抑制热点 token 塌缩，并以任务上下文稳定多场景生成。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 unirec-coa 核心机制，相对 NDCG@10 -4.93%。  generative-recommendation semantic-id preference-alignment 搜广推 生成式召回与推理推荐 UniRec-CoA 为什么在 SID 前生成属性链，并对量化容量加约束？ 属性链先把品类、卖家、品牌等结构化条件显式带入生成，使后续 SID 依赖更具体的上下文；容量约束限制热门 token 挤占码空间，任务上下文再区分不同场景需求。链式分解提高条件组织能力，也会传播早期属性错误，不能把可解释链条的存在等同于最终生成必然正确。 示意：先确定运动鞋、目标品牌和卖家范围，再生成具体商品码。若第一步把品类选成皮鞋，后续再精细也容易偏离；容量约束则防止所有商品都挤向热门品牌路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-unirec-coa-7ee11184" class="ar-learning-paper-anchor"></span>
<h2 id="qa-5ec2902153dfbf8c">UniRec-CoA 为什么在 SID 前生成属性链，并对量化容量加约束？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunirec-coa">UniRec: Bridging the Expressive Gap between Generative and Discriminative Recommendation via Chain-of-Attribute</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation / large-scale e-commerce platform</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>属性链先把品类、卖家、品牌等结构化条件显式带入生成，使后续 SID 依赖更具体的上下文；容量约束限制热门 token 挤占码空间，任务上下文再区分不同场景需求。链式分解提高条件组织能力，也会传播早期属性错误，不能把可解释链条的存在等同于最终生成必然正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先确定运动鞋、目标品牌和卖家范围，再生成具体商品码。若第一步把品类选成皮鞋，后续再精细也容易偏离；容量约束则防止所有商品都挤向热门品牌路径。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.12234">原论文</a> · <a href="../../../../reproductions/2604.12234-unirec-coa/">实现解读</a> · <a href="#qa-5ec2902153dfbf8c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mbgr" data-paper-title="MBGR: Multi-Business Generative Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="MBGR: Multi-Business Generative Recommendation 搜广推与 LLM 应用 Meituan 2026-04-03 多业务日志交错时，普通 next-item 监督只覆盖实际下一条业务。MBGR 用 business-conditioned autoencoder 保留 SID 语义，以共享 MoE 生成业务特定表示；LDR 在每个时刻为每个业务寻找最近未来交互，无标签业务被 mask。 Fidelity: 核心机制复现。Business-aware SID、共享 experts、逐业务预测与 Label Dynamic Routing 均实际执行。genre 是公开业务域代理，不能替代 Meituan 多业务私有日志与线上生成器规模。本地对照口径：基线是共享 next-item 模型；实验组 MBGR 用 genre 作为 19 个业务域并执行 BID/MBP/LDR，相对基线 Hit@10 -4.17%、NDCG@10 -5.92%。  generative-recommendation multi-domain semantic-id 搜广推 生成式召回与推理推荐 MBGR为什么为每个业务寻找最近未来交互，而不只监督日志中的下一条事件？ 多业务事件交错时，实际下一条可能属于高频业务，稀疏业务长期得不到直接监督。LDR在当前时刻为各业务寻找最近未来目标，结合业务条件表示，让同一上下文学习多条发展方向；没有对应未来事件时必须mask。构造这些标签仅限训练，评估策略不能把它们当作当前已知输入。 示意：用户先刷视频再搜索商品，下一条总是视频会淹没购物监督；按业务寻找未来目标能保留购物分支，但不能把未来购买ID直接喂给当前推荐器。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-mbgr-3a21e1da" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f28720ce81a7ef92">MBGR为什么为每个业务寻找最近未来交互，而不只监督日志中的下一条事件？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ambgr">MBGR: Multi-Business Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多业务事件交错时，实际下一条可能属于高频业务，稀疏业务长期得不到直接监督。LDR在当前时刻为各业务寻找最近未来目标，结合业务条件表示，让同一上下文学习多条发展方向；没有对应未来事件时必须mask。构造这些标签仅限训练，评估策略不能把它们当作当前已知输入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户先刷视频再搜索商品，下一条总是视频会淹没购物监督；按业务寻找未来目标能保留购物分支，但不能把未来购买ID直接喂给当前推荐器。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.02684">原论文</a> · <a href="../../../../reproductions/2604.02684-mbgr/">实现解读</a> · <a href="#qa-f28720ce81a7ef92">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rclrec" data-paper-title="RCLRec: Reverse Curriculum Learning for Modeling Sparse Conversions in Generative Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="RCLRec: Reverse Curriculum Learning for Modeling Sparse Conversions in Generative Recommendation 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-03-30 RCLRec 从行为历史里选择与转化相关的短子序列，并按逆时间顺序作为 decoder 前缀。联合生成目标提供逐样本的中间监督，质量感知损失抑制无信息课程，缓解转化标签稀疏。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04768，相对变化 -11.71%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation conversion-modeling curriculum-learning 搜广推 生成式召回与推理推荐 RCLRec 为什么把转化相关历史逆序放到 decoder 前缀，并按课程质量加权？ 转化标签稀疏时，最终目标难给长历史中的每一步充分监督。选择相关短子序列并逆序组织，使靠近转化的行为优先成为生成条件，联合目标提供中间学习信号。质量权重降低无信息课程的影响；但课程选择若只依赖错误相关性，也会强化偏差，因此不能把任意历史重排都称为有效课程。 示意：购买前先搜索、比较、加购，课程从更接近购买的加购行为向前组织，帮助模型学习关键链条；无关的偶然浏览被降低权重，而不是同等参与解释转化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-rclrec-bd92f42c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-db3a9db18dacde46">RCLRec 为什么把转化相关历史逆序放到 decoder 前缀，并按课程质量加权？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arclrec">RCLRec: Reverse Curriculum Learning for Modeling Sparse Conversions in Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>转化标签稀疏时，最终目标难给长历史中的每一步充分监督。选择相关短子序列并逆序组织，使靠近转化的行为优先成为生成条件，联合目标提供中间学习信号。质量权重降低无信息课程的影响；但课程选择若只依赖错误相关性，也会强化偏差，因此不能把任意历史重排都称为有效课程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>购买前先搜索、比较、加购，课程从更接近购买的加购行为向前组织，帮助模型学习关键链条；无关的偶然浏览被降低权重，而不是同等参与解释转化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.28124">原论文</a> · <a href="../../../../reproductions/2603.28124-rclrec/">实现解读</a> · <a href="#qa-db3a9db18dacde46">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:aigq" data-paper-title="AIGQ: An End-to-End Hybrid Generative Architecture for E-commerce Query Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="AIGQ: An End-to-End Hybrid Generative Architecture for E-commerce Query Recommendation 搜广推与 LLM 应用 Taobao &amp; Tmall Group / Alibaba 2026-03-20 Direct 路径负责低时延，Reasoning 路径补足复杂意图；IL-GRPO 用线上 CTR 奖励优化整组 query，并采用离线/在线混合服务。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 aigq 核心机制，相对 NDCG@10 +8.09%。  query-recommendation generative-recommendation reinforcement-learning 搜广推 生成式召回与推理推荐 AIGQ为什么同时保留Direct与Reasoning两条查询推荐路径？ 简单意图需要低延迟直接生成，复杂意图则可能受益于更充分的推理，两路承担不同成本与质量需求。IL-GRPO用整组query的反馈对齐组合效果，并通过离线与在线混合服务减少请求时负担；它不是把单条查询得分独立最大化。本地代理实验不能证明完整线上CTR奖励和双路服务已复现。 示意：输入品牌名时直接补全即可；含糊的送礼需求可能先推断对象和用途，再提出互补查询，避免多条结果只是同一句话的改写。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-aigq-4359f5f2" class="ar-learning-paper-anchor"></span>
<h2 id="qa-49d1587cf0ff9fec">AIGQ为什么同时保留Direct与Reasoning两条查询推荐路径？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aaigq">AIGQ: An End-to-End Hybrid Generative Architecture for E-commerce Query Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>简单意图需要低延迟直接生成，复杂意图则可能受益于更充分的推理，两路承担不同成本与质量需求。IL-GRPO用整组query的反馈对齐组合效果，并通过离线与在线混合服务减少请求时负担；它不是把单条查询得分独立最大化。本地代理实验不能证明完整线上CTR奖励和双路服务已复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>输入品牌名时直接补全即可；含糊的送礼需求可能先推断对象和用途，再提出互补查询，避免多条结果只是同一句话的改写。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.19710">原论文</a> · <a href="../../../../reproductions/2603.19710-aigq/">实现解读</a> · <a href="#qa-49d1587cf0ff9fec">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:glide" data-paper-title="Deploying Semantic ID-based Generative Retrieval for Large-Scale Podcast Discovery at Spotify" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Deploying Semantic ID-based Generative Retrieval for Large-Scale Podcast Discovery at Spotify 搜广推与 LLM 应用 Spotify 2026-03-18 纯近期序列容易只召回习惯内容。GLIDE 用 Semantic ID 自回归生成候选，同时把近期行为和长期用户 embedding 作为两类 prompt，兼顾即时意图与探索。 复现保真度：核心机制复现。复现保真度：核心机制复现。Residual Semantic ID、code 生成和双时间尺度 prompt 均实际执行。公开 item feature 做三级 residual quantization，以 code transition 生成并融合短期历史/长期内容画像。  generative-retrieval semantic-id soft-prompt 搜广推 生成式召回与推理推荐 GLIDE为什么把近期行为和长期用户embedding分别作为prompt？ 近期序列能响应刚发生的意图，却容易反复推荐熟悉内容；长期表示补充更稳定、可能被短窗口遗漏的偏好。两类prompt共同条件化SID生成，让模型在即时需求与探索之间选择。长期向量不是永远正确的背景，兴趣漂移时仍需检查其影响，不能简单拼长历史后就声称具有探索能力。 示意：用户最近只听通勤播客，但长期喜欢科学主题；两路提示可让模型在满足当前场景时发现新的科学节目，而不是只复述刚听过的系列。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-glide-1ae86d8e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-0b2de1129245e709">GLIDE为什么把近期行为和长期用户embedding分别作为prompt？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aglide">Deploying Semantic ID-based Generative Retrieval for Large-Scale Podcast Discovery at Spotify</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Spotify</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>近期序列能响应刚发生的意图，却容易反复推荐熟悉内容；长期表示补充更稳定、可能被短窗口遗漏的偏好。两类prompt共同条件化SID生成，让模型在即时需求与探索之间选择。长期向量不是永远正确的背景，兴趣漂移时仍需检查其影响，不能简单拼长历史后就声称具有探索能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户最近只听通勤播客，但长期喜欢科学主题；两路提示可让模型在满足当前场景时发现新的科学节目，而不是只复述刚听过的系列。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.17540">原论文</a> · <a href="../../../../reproductions/2603.17540-glide/">实现解读</a> · <a href="#qa-0b2de1129245e709">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:oneranker" data-paper-title="OneRanker: Unified Generation and Ranking with One Model in Industrial Advertising Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneRanker: Unified Generation and Ranking with One Model in Industrial Advertising Recommendation 搜广推与 LLM 应用 Tencent 2026-03-03 用 fake item token 统一生成、点击价值估计和广告排序，并通过分布一致性约束让生成概率与 value head 保持同一偏好。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 oneranker 核心机制；相对 NDCG@10 -7.65%。  advertising generative-recommendation ranking multi-task 搜广推 生成式召回与推理推荐 OneRanker 为什么要约束生成分布和 value head 的偏好一致？ 生成头决定哪些候选容易出现，价值头决定出现后怎样排序。若两者偏好不一致，生成器可能持续漏掉价值头最看重的物品，末端重排也无法补回。共享 fake item token 提供统一接口，分布一致性损失进一步连接两条学习信号；代价是需要平衡生成拟合、价值预测和一致性约束，避免互相压制。 示意：生成器总给便宜配件高概率，价值头却更看好适合用户的耐用工具。只重排现有配件无法展示工具；一致性训练试图让工具在生成阶段也得到机会。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-oneranker-399e9549" class="ar-learning-paper-anchor"></span>
<h2 id="qa-7e52b4a05d3de442">OneRanker 为什么要约束生成分布和 value head 的偏好一致？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aoneranker">OneRanker: Unified Generation and Ranking with One Model in Industrial Advertising Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>生成头决定哪些候选容易出现，价值头决定出现后怎样排序。若两者偏好不一致，生成器可能持续漏掉价值头最看重的物品，末端重排也无法补回。共享 fake item token 提供统一接口，分布一致性损失进一步连接两条学习信号；代价是需要平衡生成拟合、价值预测和一致性约束，避免互相压制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>生成器总给便宜配件高概率，价值头却更看好适合用户的耐用工具。只重排现有配件无法展示工具；一致性训练试图让工具在生成阶段也得到机会。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.02999">原论文</a> · <a href="../../../../reproductions/2603.02999-oneranker/">实现解读</a> · <a href="#qa-7e52b4a05d3de442">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:grc" data-paper-title="Learning to Reflect and Correct: Towards Better Decoding Trajectories for Large-Scale Generative Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Learning to Reflect and Correct: Towards Better Decoding Trajectories for Large-Scale Generative Recommendation 搜广推与 LLM 应用 Alibaba International / Wuhan University 2026-02-27 Semantic ID 自回归生成的早期错误会向后传播。GRC 把 draft SID、首错位置/属性一致性反思、corrected SID 串成结构化模板；再对完整轨迹做 GRPO，并用反思 token 熵把固定纠错预算分配给最不确定的 beam。 Fidelity: 核心机制复现。结构化 SFT、完整轨迹 GRPO 与 entropy-guided reflection scheduling 均实际执行。MovieLens genre 代理 category/seller/brand 属性；未复刻工业 LLM 参数量。本地对照口径：基线是同一 SID 的 GR backbone；实验组 GRC 加入 1,320 条结构化轨迹、10 轮 GRPO 与 EGRS，相对基线 Hit@10 -12.50%、NDCG@10 -11.12%。  generative-recommendation reinforcement-learning self-correction 搜广推 生成式召回与推理推荐 GRC训练时标注首个错误SID位置，为什么评估时不能直接把这个位置交给纠错器？ 真实目标码只在训练监督中用于构造draft—反思—纠正轨迹。部署时模型必须从当前候选、属性一致性和自身不确定性判断哪里可能错，否则就是把答案泄漏给被评估策略。熵引导把有限纠错预算分给不确定beam，但高不确定也可能只是难例，不保证一定能修正或提高召回。 示意：训练可指出草稿城市码与目标不同；实际推荐时系统不知道用户最终会选哪件商品，只能检查语义与当前证据，不能预先读目标码来定位错误。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-grc-7f75523b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-34cb5a2e2828c895">GRC训练时标注首个错误SID位置，为什么评估时不能直接把这个位置交给纠错器？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agrc">Learning to Reflect and Correct: Towards Better Decoding Trajectories for Large-Scale Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International / Wuhan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>真实目标码只在训练监督中用于构造draft—反思—纠正轨迹。部署时模型必须从当前候选、属性一致性和自身不确定性判断哪里可能错，否则就是把答案泄漏给被评估策略。熵引导把有限纠错预算分给不确定beam，但高不确定也可能只是难例，不保证一定能修正或提高召回。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练可指出草稿城市码与目标不同；实际推荐时系统不知道用户最终会选哪件商品，只能检查语义与当前证据，不能预先读目标码来定位错误。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.23639">原论文</a> · <a href="../../../../reproductions/2602.23639-grc/">实现解读</a> · <a href="#qa-34cb5a2e2828c895">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gr4ad" data-paper-title="Generative Recommendation for Large-Scale Advertising" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Generative Recommendation for Large-Scale Advertising 搜广推与 LLM 应用 Kuaishou 2026-02-26 广告生成式推荐同时受商业语义、实时更新和延迟约束。GR4AD 用多粒度 UA-SID 编码广告，LazyAR 放松层间自回归依赖，VSL 按商业价值加权监督，RSPO 直接优化列表排序，Dynamic Beam Serving 随负载调整 beam。 Fidelity: 核心机制复现。UA-SID、并行 LazyAR、VSL、list-wise RSPO 均训练；私有多模态广告、eCPM、在线持续学习和动态 beam 服务未复刻。本地对照口径：统一跨模型基线是 DIN，GR4AD NDCG@10 相对 DIN +69.67%；内部 DLRM 基线加入 UA-SID/LazyAR/VSL/RSPO 后 +49.88%。两项都伴随 head share 0.505 的偏置风险。60 steps、180 users/280 items、seeds 42–44。统一 DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；  generative-retrieval advertising reinforcement-learning serving 搜广推 生成式召回与推理推荐 GR4AD为什么既按商业价值加权监督，又用列表排序优化，而不只学习下一个广告码？ 单纯next-token学习曝光频率，可能让常见却价值较低的广告主导训练。价值加权改变不同样本的贡献，列表优化再关心候选之间的相对业务收益；多粒度SID和依赖放松则处理表示与计算问题。这些目标未必一致，必须检查是否牺牲相关性或过度集中头部，不能只报告收入代理的单项变化。 示意：一个广告出现很多却很少带来有效转化，另一个较少曝光但有较高业务价值；频率模仿会偏前者，价值监督与列表对齐允许表达这一区别。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-gr4ad-4d146b97" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1aaa4f6709186ebb">GR4AD为什么既按商业价值加权监督，又用列表排序优化，而不只学习下一个广告码？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agr4ad">Generative Recommendation for Large-Scale Advertising</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单纯next-token学习曝光频率，可能让常见却价值较低的广告主导训练。价值加权改变不同样本的贡献，列表优化再关心候选之间的相对业务收益；多粒度SID和依赖放松则处理表示与计算问题。这些目标未必一致，必须检查是否牺牲相关性或过度集中头部，不能只报告收入代理的单项变化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个广告出现很多却很少带来有效转化，另一个较少曝光但有较高业务价值；频率模仿会偏前者，价值监督与列表对齐允许表达这一区别。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.22732">原论文</a> · <a href="../../../../reproductions/2602.22732-gr4ad/">实现解读</a> · <a href="#qa-1aaa4f6709186ebb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sigma" data-paper-title="SIGMA: A Semantic-Grounded Instruction-Driven Generative Multi-Task Recommender at AliExpress" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="SIGMA: A Semantic-Grounded Instruction-Driven Generative Multi-Task Recommender at AliExpress 搜广推与 LLM 应用 Alibaba / AliExpress 2026-02-26 普通生成推荐只做 next-item，难以即时响应 Query、Category、Longtail、Discover、Season、Holiday 等业务任务。SIGMA 先通过搜索语义、视觉、世界知识和协同行为四类 relevance pair，把 LLM 语义与在线 ID embedding 对齐；随后用“短 SID prefix + unique item ID”同时保留生成效率和商品精度；七任务 instruction SFT 统一训练； 七任务分桶样本只有约 18/任务，逐任务数字只作诊断，不作结论。Fidelity: 完整核心链路。本地实际执行 causal-LM LoRA 多视角 InfoNCE+KD、RQ-SID prefix 与 unique ID 混合 token、七类 instruction SFT、SID-prefix NTP、同-prefix hard-negative InfoNCE、prefix beam→子目录 item retrieval→APF。不是用最终分数规则模拟 SIGMA。使用真实 SmolLM LoRA 编码与反向，不是固定 embedding 直接代替 multi-view grounding；  generative-recommendation multi-task-sft hybrid-token semantic-grounding 搜广推 生成式召回与推理推荐 SIGMA 为什么用“短 SID 前缀加唯一物品 ID”，而不完全生成 SID 或只做全库 ANN？ 短前缀让模型先按任务指令定位语义子目录，唯一 ID 再保留物品精度并避免同码混淆。检索只在对应子目录做近邻搜索，折中完整多级解码与全库检索成本；多视角对齐让语义与行为空间更相容。APF 根据前缀置信度调节精确性和多样性，但早期前缀漏掉的目录仍可能限制候选覆盖。 示意：先生成“户外装备”子目录，再在其中选具体帐篷 ID。置信度高时集中搜索，模糊时扩展多个前缀；若第一步只选家居目录，再强的目录内 ANN 也找不到帐篷。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-sigma-3e17a33a" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1ed6d59e347fea5a">SIGMA 为什么用“短 SID 前缀加唯一物品 ID”，而不完全生成 SID 或只做全库 ANN？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asigma">SIGMA: A Semantic-Grounded Instruction-Driven Generative Multi-Task Recommender at AliExpress</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / AliExpress</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>短前缀让模型先按任务指令定位语义子目录，唯一 ID 再保留物品精度并避免同码混淆。检索只在对应子目录做近邻搜索，折中完整多级解码与全库检索成本；多视角对齐让语义与行为空间更相容。APF 根据前缀置信度调节精确性和多样性，但早期前缀漏掉的目录仍可能限制候选覆盖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先生成“户外装备”子目录，再在其中选具体帐篷 ID。置信度高时集中搜索，模糊时扩展多个前缀；若第一步只选家居目录，再强的目录内 ANN 也找不到帐篷。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.22913">原论文</a> · <a href="../../../../reproductions/2602.22913-sigma/">实现解读</a> · <a href="#qa-1ed6d59e347fea5a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:static-constraint-decoding" data-paper-title="Vectorizing the Trie: Efficient Constrained Decoding for LLM-based Generative Retrieval on Accelerators" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Vectorizing the Trie: Efficient Constrained Decoding for LLM-based Generative Retrieval on Accelerators 搜广推与 LLM 应用 Google 2026-02-26 生成式推荐常需要将解码限制在新鲜内容、库存或地域等合法 item 子集中。STATIC 将前缀树离线压成 CSR 迁移矩阵，浅层可用 dense lookup；每步在 GPU/TPU 上抽取合法候选，消除 CPU 指针追踪和设备往返。 成本过高，不复现（审查 DONE）：完整实验需要 TPU v6e、1B 模型及生产环境；本次实现 Algorithms 1/2 的独立 PyTorch 算子：CSR 离线构建、固定最大分支宽度的向量化 speculative gather、浅层 dense lookup、log-space 掩码、beam 父状态重排和显式 EOS。使用变长 ID 时必须保留 EOS，调用方需收集已结束 beam；不提供完整语言模型。  生成式推荐 约束解码与服务效率 搜广推 生成式召回与推理推荐 STATIC 为什么先做全词表 log-softmax 再屏蔽非法 token，而不在合法集合重新归一化？ 约束只限制可走路径，不应悄悄改变模型原本的条件概率尺度。在各前缀的合法集合上重归一化，会让候选少的前缀获得人为优势，改变跨 beam 的比较。CSR 把合法转移压成设备友好数组，加速查表；选择 beam 后还必须同步重排前缀与树状态，否则约束会套到错误路径上。 示意：两个前缀分别只剩一个和十个合法后继。若各自重归一化，前者唯一后继概率变成一，可能无端击败原模型更支持的另一条路径；保持原概率再掩码可避免这种偏移。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-static-constraint-decoding-c02cbeaf" class="ar-learning-paper-anchor"></span>
<h2 id="qa-9de99ca7ecd033e3">STATIC 为什么先做全词表 log-softmax 再屏蔽非法 token，而不在合法集合重新归一化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Astatic-constraint-decoding">Vectorizing the Trie: Efficient Constrained Decoding for LLM-based Generative Retrieval on Accelerators</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>约束只限制可走路径，不应悄悄改变模型原本的条件概率尺度。在各前缀的合法集合上重归一化，会让候选少的前缀获得人为优势，改变跨 beam 的比较。CSR 把合法转移压成设备友好数组，加速查表；选择 beam 后还必须同步重排前缀与树状态，否则约束会套到错误路径上。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个前缀分别只剩一个和十个合法后继。若各自重归一化，前者唯一后继概率变成一，可能无端击败原模型更支持的另一条路径；保持原概率再掩码可避免这种偏移。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.22647">原论文</a> · <a href="../../../../recommendation-components/2602.22647-static-constraint-decoding/">实现解读</a> · <a href="#qa-9de99ca7ecd033e3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:climber-pilot" data-paper-title="Climber-Pilot: A Non-Myopic Generative Recommendation Model Towards Better Instruction-Following" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Climber-Pilot: A Non-Myopic Generative Recommendation Model Towards Better Instruction-Following 搜广推与 LLM 应用 NetEase Cloud Music 2026-02-14 Climber-Pilot 用时间感知多物品预测把长周期、多物品消费前瞻蒸馏进单步生成模型；条件引导稀疏注意力在 attention 内注入类目和业务约束，无需额外过滤或多步推理。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.09251，相对变化 +71.29%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-retrieval long-horizon instruction-following 搜广推 生成式召回与推理推荐 Climber-Pilot怎样让单步生成考虑更远消费，而不在服务时展开整条未来轨迹？ 时间感知多物品预测在训练中要求当前状态解释多个未来目标，把长周期前瞻压进参数；服务时仍可只生成当前结果。条件引导的注意力再把类目与业务限制纳入计算，而不是额外多步推理。未来监督只能来自训练轨迹，不能在评估请求中读取真实未来物品来决定当前推荐。 示意：训练时知道某次兴趣最终延伸到相机配件，可让当前表示学习这类后续需求；真正上线只看已有历史，不能把这位用户尚未发生的购买塞进输入。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-climber-pilot-a97c0a4c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-93eb6feb5d5e3d8d">Climber-Pilot怎样让单步生成考虑更远消费，而不在服务时展开整条未来轨迹？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aclimber-pilot">Climber-Pilot: A Non-Myopic Generative Recommendation Model Towards Better Instruction-Following</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NetEase Cloud Music</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>时间感知多物品预测在训练中要求当前状态解释多个未来目标，把长周期前瞻压进参数；服务时仍可只生成当前结果。条件引导的注意力再把类目与业务限制纳入计算，而不是额外多步推理。未来监督只能来自训练轨迹，不能在评估请求中读取真实未来物品来决定当前推荐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练时知道某次兴趣最终延伸到相机配件，可让当前表示学习这类后续需求；真正上线只看已有历史，不能把这位用户尚未发生的购买塞进输入。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.13581">原论文</a> · <a href="../../../../reproductions/2602.13581-climber-pilot/">实现解读</a> · <a href="#qa-93eb6feb5d5e3d8d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rgalign-rec" data-paper-title="RGAlign-Rec: Ranking-Guided Alignment for Latent Query Reasoning in Recommendation Systems" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="RGAlign-Rec: Ranking-Guided Alignment for Latent Query Reasoning in Recommendation Systems 搜广推与 LLM 应用 Forth AI / Shopee / Singapore University of Technology and Design 2026-02-13 先让 LLM 从上下文生成潜在 query，再用真实排序模型的 item 偏好构建正负 query，通过 RG-SFT 与 DPO 对齐 top-rank 意图。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 rgalign-rec 核心机制，相对 NDCG@10 -14.03%。  llm-recommendation query-reasoning preference-alignment 搜广推 生成式召回与推理推荐 RGAlign 为什么用排序模型对物品的偏好反过来选择 query 的胜负？ 语言上流畅的潜在 query 未必能召回排序器真正看重的物品。先生成多种 query，再依据它们对应物品的排序偏好构造监督与胜负对，可把意图生成目标对齐到下游 top-rank 需求。RG-SFT 建立基本映射，DPO 强化相对偏好；它仍继承排序器的判断，不能被当成独立用户满意度标签。 示意：历史可解释为“入门摄影”或“专业镜头”。若下游对该用户更看好轻便入门相机，就优先训练前一 query，而不是仅按哪句表达更自然来选胜者。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-rgalign-rec-56b59d1c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-6398abbf95278d4e">RGAlign 为什么用排序模型对物品的偏好反过来选择 query 的胜负？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Argalign-rec">RGAlign-Rec: Ranking-Guided Alignment for Latent Query Reasoning in Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Forth AI / Shopee / Singapore University of Technology and Design</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语言上流畅的潜在 query 未必能召回排序器真正看重的物品。先生成多种 query，再依据它们对应物品的排序偏好构造监督与胜负对，可把意图生成目标对齐到下游 top-rank 需求。RG-SFT 建立基本映射，DPO 强化相对偏好；它仍继承排序器的判断，不能被当成独立用户满意度标签。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>历史可解释为“入门摄影”或“专业镜头”。若下游对该用户更看好轻便入门相机，就优先训练前一 query，而不是仅按哪句表达更自然来选胜者。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12968">原论文</a> · <a href="../../../../reproductions/2602.12968-rgalign-rec/">实现解读</a> · <a href="#qa-6398abbf95278d4e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rolegen" data-paper-title="Awakening Dormant Users: Generative Recommendation with Counterfactual Functional Role Reasoning" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Awakening Dormant Users: Generative Recommendation with Counterfactual Functional Role Reasoning 搜广推与 LLM 应用 Beihang University 2026-02-13 RoleGen 让 LLM Reasoner 判断物品在转化轨迹中的功能角色，并通过反事实路径估计其工具性作用；候选再进入 SID 生成骨干，通过推理—执行—反馈—反思闭环迭代，降低休眠用户兴趣坍缩。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05605，相对变化 +3.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation counterfactual-reasoning dormant-users 搜广推 生成式召回与推理推荐 RoleGen 为什么要识别转化路径中的功能角色，而不只按物品相似度唤醒休眠用户？ 长期无活跃时，重复旧相似物品容易把兴趣收窄。功能角色把物品理解为探索、比较或促成转化等路径环节，再用反事实路径估计其工具性贡献，反馈给 SID 生成骨干并迭代反思。这里的作用估计依赖模型与数据假设，不能仅凭观测轨迹就把分数差解释成已识别的真实因果效应。 示意：用户买相机前看过评测和摄影教程，教程虽不似相机商品，却可能是重新激活兴趣的入口。按角色理解路径可考虑这个入口，而不只继续推荐相似相机。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-rolegen-9ce78677" class="ar-learning-paper-anchor"></span>
<h2 id="qa-c0450005c9756e63">RoleGen 为什么要识别转化路径中的功能角色，而不只按物品相似度唤醒休眠用户？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arolegen">Awakening Dormant Users: Generative Recommendation with Counterfactual Functional Role Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长期无活跃时，重复旧相似物品容易把兴趣收窄。功能角色把物品理解为探索、比较或促成转化等路径环节，再用反事实路径估计其工具性贡献，反馈给 SID 生成骨干并迭代反思。这里的作用估计依赖模型与数据假设，不能仅凭观测轨迹就把分数差解释成已识别的真实因果效应。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户买相机前看过评测和摄影教程，教程虽不似相机商品，却可能是重新激活兴趣的入口。按角色理解路径可考虑这个入口，而不只继续推荐相似相机。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.13134">原论文</a> · <a href="../../../../reproductions/2602.13134-rolegen/">实现解读</a> · <a href="#qa-c0450005c9756e63">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:s-grec" data-paper-title="S-GRec: Personalized Semantic-Aware Generative Recommendation with Asymmetric Advantage" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="S-GRec: Personalized Semantic-Aware Generative Recommendation with Asymmetric Advantage 搜广推与 LLM 应用 Tencent / WeChat Channels 2026-02-11 生成式推荐通常只从行为日志学习 next-item likelihood，难以理解用户为何偏好某个内容；直接把 LLM 放到在线链路又无法满足工业延迟。S-GRec 将 LLM 仅作为离线语义 judge：两阶段 Personalized Semantic Judge（PSJ）先输出可解释的方面证据，再学习每个用户的方面权重；轻量生成器线上只生成 Semantic ID，不依赖 LLM。论文的第二个问题是语义目标可能与收入目标冲突。 这是最大的数据保真度差异。Fidelity: 完整核心链路。本地实际执行 causal LLM LoRA judge、方面打分 SFT+GRPO、用户条件权重 pairwise GRPO、SID 自回归生成器、5% 稀疏 semantic sampling，以及从相同 SFT checkpoint 初始化的 Reward-Sum、Adv-Sum、A2PO。模型规模与数据规模缩小，腾讯私有人工广告标注和 eCPM 模型由公开 Office 行为与 Qwen embedding 构造的监督替代。Qwen3-4B PSJ 缩小为 SmolLM2-135M；  generative-recommendation llm-as-judge grpo a2po 搜广推 生成式召回与推理推荐 S-GRec 的 A2PO 为什么只在语义与业务 advantage 同向时加入受限语义贡献？ 语义 judge 的分数与收入反馈量纲不同，直接相加可能让语义目标压倒业务。A2PO 先在各 rollout 组内分别标准化，以业务 advantage 为锚；仅同向时引入语义项，并把有效贡献限在业务幅度内。这样语义奖励提供辅助方向而非任意改写目标，但业务和 judge 本身仍可能有偏差。 示意：候选理由听来很贴合兴趣，但业务反馈为负时，不让高语义分把它翻成强正样本；两者都支持时才适度加分，避免模型为讨好评审牺牲业务目标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-s-grec-c5ba1bc0" class="ar-learning-paper-anchor"></span>
<h2 id="qa-ef678d9523c7b0d4">S-GRec 的 A2PO 为什么只在语义与业务 advantage 同向时加入受限语义贡献？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3As-grec">S-GRec: Personalized Semantic-Aware Generative Recommendation with Asymmetric Advantage</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent / WeChat Channels</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语义 judge 的分数与收入反馈量纲不同，直接相加可能让语义目标压倒业务。A2PO 先在各 rollout 组内分别标准化，以业务 advantage 为锚；仅同向时引入语义项，并把有效贡献限在业务幅度内。这样语义奖励提供辅助方向而非任意改写目标，但业务和 judge 本身仍可能有偏差。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>候选理由听来很贴合兴趣，但业务反馈为负时，不让高语义分把它翻成强正样本；两者都支持时才适度加分，避免模型为讨好评审牺牲业务目标。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.10606">原论文</a> · <a href="../../../../reproductions/2602.10606-s-grec/">实现解读</a> · <a href="#qa-ef678d9523c7b0d4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:diffureason" data-paper-title="DiffuReason: Bridging Latent Reasoning and Generative Refinement for Sequential Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="DiffuReason: Bridging Latent Reasoning and Generative Refinement for Sequential Recommendation 搜广推与 LLM 应用 Tencent 2026-02-10 Thinking Tokens 形成连续潜在意图，扩散去噪逐步修正冲突兴趣，GRPO 再把连续生成与离散排序奖励端到端对齐。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 diffureason 核心机制，相对 NDCG@10 -6.50%。  generative-recommendation diffusion reinforcement-learning 搜广推 生成式召回与推理推荐 DiffuReason为什么在潜在意图上做多步扩散修正，而不是一次生成最终推荐表示？ 一次预测可能将多个冲突兴趣压成不稳定方向，潜在Thinking Tokens先承载意图，再由逐步去噪反复修正表示，使不同线索有机会重新协调。GRPO随后用离散排序反馈对齐连续生成路径。多步过程增加计算且可能累积模型偏差，本地代理不能单独证明完整潜在推理能力。 示意：用户既搜健身器材又看甜品视频，一次融合可能摇摆；去噪过程可逐步形成更适合当前请求的意图，但不能把中间向量自动解释为真实的人类思考。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-diffureason-5f379d3c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-fc1bd647de874fa4">DiffuReason为什么在潜在意图上做多步扩散修正，而不是一次生成最终推荐表示？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adiffureason">DiffuReason: Bridging Latent Reasoning and Generative Refinement for Sequential Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一次预测可能将多个冲突兴趣压成不稳定方向，潜在Thinking Tokens先承载意图，再由逐步去噪反复修正表示，使不同线索有机会重新协调。GRPO随后用离散排序反馈对齐连续生成路径。多步过程增加计算且可能累积模型偏差，本地代理不能单独证明完整潜在推理能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户既搜健身器材又看甜品视频，一次融合可能摇摆；去噪过程可逐步形成更适合当前请求的意图，但不能把中间向量自动解释为真实的人类思考。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.09744">原论文</a> · <a href="../../../../reproductions/2602.09744-diffureason/">实现解读</a> · <a href="#qa-fc1bd647de874fa4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rag-qac" data-paper-title="Unifying Ranking and Generation in Query Auto-Completion via Retrieval-Augmented Generation and Multi-Objective Alignment" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Unifying Ranking and Generation in Query Auto-Completion via Retrieval-Augmented Generation and Multi-Objective Alignment 搜广推与 LLM 应用 Apple 2026-02-01 先从可搜索目录检索补全证据，再以 SFT 和 DPO 同时对齐相关性、安全、参与度、目录/上下文 groundedness 与多样性。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 rag-qac 核心机制，相对 NDCG@10 -4.48%。  query-auto-completion retrieval-augmented-generation preference-alignment 搜广推 生成式召回与推理推荐 RAG-QAC 为什么先检索可搜索目录，再对补全建议做多目标偏好对齐？ 自由生成的查询补全可能语言合理却找不到商品或文档。目录检索先提供可追溯候选与证据，使建议有机会落到可服务对象；SFT 与 DPO 再联合权衡相关性、安全、参与度、上下文依据和多样性。多目标对齐不能弥补目录里本就不存在的内容，也需避免为参与度牺牲真实性。 示意：用户输入“轻便露营”，先从目录取得帐篷、炊具等真实类别再补全，避免生成商店根本没有的型号；两个都能搜到的补全再比较相关性与多样性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-rag-qac-5e006d24" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d935bc68ea027e7f">RAG-QAC 为什么先检索可搜索目录，再对补全建议做多目标偏好对齐？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arag-qac">Unifying Ranking and Generation in Query Auto-Completion via Retrieval-Augmented Generation and Multi-Objective Alignment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Apple</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>自由生成的查询补全可能语言合理却找不到商品或文档。目录检索先提供可追溯候选与证据，使建议有机会落到可服务对象；SFT 与 DPO 再联合权衡相关性、安全、参与度、上下文依据和多样性。多目标对齐不能弥补目录里本就不存在的内容，也需避免为参与度牺牲真实性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户输入“轻便露营”，先从目录取得帐篷、炊具等真实类别再补全，避免生成商店根本没有的型号；两个都能搜到的补全再比较相关性与多样性。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.01023">原论文</a> · <a href="../../../../reproductions/2602.01023-rag-qac/">实现解读</a> · <a href="#qa-d935bc68ea027e7f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onemall" data-paper-title="OneMall: One Model, More Scenarios -- End-to-End Generative Recommender Family at Kuaishou E-Commerce" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneMall: One Model, More Scenarios -- End-to-End Generative Recommender Family at Kuaishou E-Commerce 搜广推与 LLM 应用 Kuaishou 2026-01-29 快手电商的商品卡、短视频和直播分发原本由不同链路维护。OneMall 用统一商品 Semantic ID、Query-Former 压缩、多行为 cross-attention、Sparse MoE 生成器及 RL 对齐，把多个场景收进一个生成推荐家族。 Fidelity: 核心机制复现。执行场景 prompt、三层 Semantic ID 和跨行为融合；缩小数据与模型规模。MovieLens genre 仅代理场景；未复刻快手私有商品特征、Sparse MoE、生产 RL 和线上 serving。本地对照口径：基线是共享 transition/content ensemble；实验组只增加场景 prompt、三层 residual SID 和跨行为融合，MovieLens-100K NDCG@10 0.03540→0.03693，相对 +4.33%，Hit@10 相对 -4.35%。  generative-recommendation multi-scenario semantic-id 搜广推 生成式召回与推理推荐 OneMall 用统一 Semantic ID 之后，为什么还要场景条件和多行为 cross-attention？ 统一编码只让商品在多个场景使用同一套输出词表，不能消除商品卡、短视频与直播的行为差异。场景条件告诉生成器当前目标，多行为交互再提取与该目标相关的历史信息；Query-Former 压缩和稀疏专家控制上下文与容量成本。因此统一的是模型家族和表示接口，场景特性仍需显式建模。 示意：同一件夹克在商品卡里对应点击，在直播里可能对应停留与下单。共用商品编码后，模型仍需知道当前是直播推荐，才能从用户多种行为中选择相关信号。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-onemall-15aa9dcd" class="ar-learning-paper-anchor"></span>
<h2 id="qa-361175a32963e5b8">OneMall 用统一 Semantic ID 之后，为什么还要场景条件和多行为 cross-attention？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonemall">OneMall: One Model, More Scenarios -- End-to-End Generative Recommender Family at Kuaishou E-Commerce</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>统一编码只让商品在多个场景使用同一套输出词表，不能消除商品卡、短视频与直播的行为差异。场景条件告诉生成器当前目标，多行为交互再提取与该目标相关的历史信息；Query-Former 压缩和稀疏专家控制上下文与容量成本。因此统一的是模型家族和表示接口，场景特性仍需显式建模。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一件夹克在商品卡里对应点击，在直播里可能对应停留与下单。共用商品编码后，模型仍需知道当前是直播推荐，才能从用户多种行为中选择相关信号。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.21770">原论文</a> · <a href="../../../../reproductions/2601.21770-onemall/">实现解读</a> · <a href="#qa-361175a32963e5b8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:s2gr" data-paper-title="S2GR: Stepwise Semantic-Guided Reasoning in Latent Space for Generative Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="S2GR: Stepwise Semantic-Guided Reasoning in Latent Space for Generative Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-01-26 在每一级 SID 生成前插入可解释 thinking token，并让它与真实 codebook 分布对比学习；协同共现图和负载均衡共同改善由粗到细的语义层级。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05463，相对变化 +1.15%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation latent-reasoning semantic-id 搜广推 生成式召回与推理推荐 S2GR 为什么在每一级 SID 前插入 thinking token，并把它与 codebook 分布对齐？ 粗到细 SID 的早期选择会限定后续路径，单独最大化码概率可能缺少明确的语义过渡。逐级 thinking token 提供中间状态，再用与真实码本分布的对比监督把它连接到合法语义空间，协同图与负载均衡补充行为关系和码使用。中间 token 可辅助解释，但不能仅凭名字就证明它进行了忠实的自然语言推理。 示意：先确定户外大类，再细分露营装备。每级中间状态都需贴近对应码本语义，避免出现解释像在谈露营，实际却跳到无关家居编码的脱节。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-s2gr-c72e2aca" class="ar-learning-paper-anchor"></span>
<h2 id="qa-833b7b1f56656208">S2GR 为什么在每一级 SID 前插入 thinking token，并把它与 codebook 分布对齐？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3As2gr">S2GR: Stepwise Semantic-Guided Reasoning in Latent Space for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>粗到细 SID 的早期选择会限定后续路径，单独最大化码概率可能缺少明确的语义过渡。逐级 thinking token 提供中间状态，再用与真实码本分布的对比监督把它连接到合法语义空间，协同图与负载均衡补充行为关系和码使用。中间 token 可辅助解释，但不能仅凭名字就证明它进行了忠实的自然语言推理。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先确定户外大类，再细分露营装备。每级中间状态都需贴近对应码本语义，避免出现解释像在谈露营，实际却跳到无关家居编码的脱节。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.18664">原论文</a> · <a href="../../../../reproductions/2601.18664-s2gr/">实现解读</a> · <a href="#qa-833b7b1f56656208">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:promise" data-paper-title="PROMISE: Process Reward Models Unlock Test-Time Scaling Laws in Generative Recommendations" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="PROMISE: Process Reward Models Unlock Test-Time Scaling Laws in Generative Recommendations 搜广推与 LLM 应用 Kuaishou Technology 2026-01-08 轻量 path-level PRM 在每个 SID 层级评价中间路径，训练时提供稠密反馈、推理时提前剪除已发生语义漂移的 beam；因此增加 beam width 能形成可控的 test-time scaling。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05929，相对变化 +9.79%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation process-reward test-time-scaling 搜广推 生成式召回与推理推荐 PROMISE 为什么在 SID 中间路径就给奖励，而不等生成完整物品后才评分？ 层级生成一旦在早期走错语义分支，后续计算很可能继续细化错误方向。轻量过程奖励模型逐层评价路径，既给训练更稠密的反馈，也在推理中及早剪掉漂移 beam。增加束宽因此有机会探索更多有希望路径，但收益受过程评分可靠性与额外计算制约，束越宽并不保证越好。 示意：用户要登山装备，首层路径却进入家居装饰。等生成到具体抱枕才打低分会浪费后续步骤；路径评分可在粗层就淘汰它，把预算留给户外相关分支。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-promise-c348f413" class="ar-learning-paper-anchor"></span>
<h2 id="qa-bd05a70bed64223d">PROMISE 为什么在 SID 中间路径就给奖励，而不等生成完整物品后才评分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apromise">PROMISE: Process Reward Models Unlock Test-Time Scaling Laws in Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>层级生成一旦在早期走错语义分支，后续计算很可能继续细化错误方向。轻量过程奖励模型逐层评价路径，既给训练更稠密的反馈，也在推理中及早剪掉漂移 beam。增加束宽因此有机会探索更多有希望路径，但收益受过程评分可靠性与额外计算制约，束越宽并不保证越好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户要登山装备，首层路径却进入家居装饰。等生成到具体抱枕才打低分会浪费后续步骤；路径评分可在粗层就淘汰它，把预算留给户外相关分支。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.04674">原论文</a> · <a href="../../../../reproductions/2601.04674-promise/">实现解读</a> · <a href="#qa-bd05a70bed64223d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dualgr" data-paper-title="DualGR: Generative Retrieval with Long and Short-Term Interests Modeling" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="DualGR: Generative Retrieval with Long and Short-Term Interests Modeling 搜广推与 LLM 应用 USTC / Kuaishou Technology 2025-11-16 短期兴趣与长期兴趣使用双路由器，约束 Semantic ID 前缀有效性，并以曝光感知项抑制头部坍缩。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 dualgr 核心机制；相对 NDCG@10 +6.73%。  retrieval generative-recommendation semantic-id long-short-interest 搜广推 生成式召回与推理推荐 DualGR为什么分别路由长短期兴趣，而不是把全部历史拼成一条序列？ 短期兴趣反映当前意图，长期兴趣提供稳定偏好，两者可能在不同请求中权重相反。双路由器让模型按状态融合两种生成分布，前缀约束保证输出可对应物品，曝光感知项再抑制热门码垄断。分成两路本身不能保证分工，仍需检查路由是否坍缩以及两路是否学到不同信息。 示意：用户平时爱旅行，今天集中购买厨房用品；短期路应响应当下需求，长期路则保留旅行兴趣，不能让漫长旧历史把最近明显变化完全淹没。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-dualgr-b1420088" class="ar-learning-paper-anchor"></span>
<h2 id="qa-24d3da30a1a5d844">DualGR为什么分别路由长短期兴趣，而不是把全部历史拼成一条序列？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adualgr">DualGR: Generative Retrieval with Long and Short-Term Interests Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · USTC / Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>短期兴趣反映当前意图，长期兴趣提供稳定偏好，两者可能在不同请求中权重相反。双路由器让模型按状态融合两种生成分布，前缀约束保证输出可对应物品，曝光感知项再抑制热门码垄断。分成两路本身不能保证分工，仍需检查路由是否坍缩以及两路是否学到不同信息。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户平时爱旅行，今天集中购买厨房用品；短期路应响应当下需求，长期路则保留旅行兴趣，不能让漫长旧历史把最近明显变化完全淹没。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2511.12518">原论文</a> · <a href="../../../../reproductions/2511.12518-dualgr/">实现解读</a> · <a href="#qa-24d3da30a1a5d844">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:plum" data-paper-title="PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations 搜广推与 LLM 应用 Google DeepMind / YouTube 2025-10-09 传统 large embedding model（LEM）把绝大多数参数放在千万级 ID embedding 表，神经网络容量反而很小，难以获得 LLM 式 scaling。PLUM 从 Gemini-1.5 MoE 初始化，把视频量化成 Semantic ID（SID），先用用户行为与视频文本/ASR/频道元数据做 continued pre-training（CPT），再以 next-SID generation 做生成式召回。线上用 beam search 直接生成候选 SID，不再维护点积检索索引。 LLM 初始化组在有无 CPT 时 Recall@10 都为 0，未复现论文中 LLM initialization 的增益。Fidelity: 完整核心链路复现。本地实际执行多层 RQ Semantic ID、预训练 decoder-only LM 的 CPT、next-SID SFT 和 token-level constrained beam search；只缩小模型/数据规模并替换私有模态。本地对照口径：基线是随机初始化无 CPT（R1），实验组是随机初始化有 CPT（CR1）；Recall@10 都是 0.0050（0.00%），但 SFT final loss 从 3.5023 降至 2.5933；   搜广推 生成式召回与推理推荐 PLUM 为什么把视频变成层级 SID 并继续预训练语言模型，而不是继续扩大 ID embedding 表？ 巨型 ID 表把参数花在逐物品记忆上，新物品难共享知识，也不能充分利用大语言模型的网络容量。层级 SID 把输出分解为可组合的码，CPT 再把行为与文本、ASR 和元数据接入语言模型，随后学习 next-SID。线上直接束搜索生成候选，但 SID 的语义与协同质量仍决定路径是否适合推荐。 示意：新增一条烘焙视频时，独立 ID 只能从少量点击起步；若它拥有与已有烘焙内容共享的粗粒度码，生成器可先复用主题知识，再在细码上区分具体视频。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-plum-515f2ca7" class="ar-learning-paper-anchor"></span>
<h2 id="qa-0d1840f495739871">PLUM 为什么把视频变成层级 SID 并继续预训练语言模型，而不是继续扩大 ID embedding 表？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aplum">PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>巨型 ID 表把参数花在逐物品记忆上，新物品难共享知识，也不能充分利用大语言模型的网络容量。层级 SID 把输出分解为可组合的码，CPT 再把行为与文本、ASR 和元数据接入语言模型，随后学习 next-SID。线上直接束搜索生成候选，但 SID 的语义与协同质量仍决定路径是否适合推荐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新增一条烘焙视频时，独立 ID 只能从少量点击起步；若它拥有与已有烘焙内容共享的粗粒度码，生成器可先复用主题知识，再在细码上区分具体视频。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.07784">原论文</a> · <a href="../../../../reproductions/2510.07784-plum/">实现解读</a> · <a href="#qa-0d1840f495739871">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:intsr" data-paper-title="IntSR: An Integrated Generative Framework for Search and Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="IntSR: An Integrated Generative Framework for Search and Recommendation 搜广推与 LLM 应用 Alibaba / Amap 2025-09-25 用显式查询和隐式会话意图共同生成 POI/物品，统一搜索与推荐词表，并加入时间上下文刻画意图漂移。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 intsr 核心机制；相对 NDCG@10 +33.56%。  search recommendation generative-retrieval content-understanding 搜广推 生成式召回与推理推荐 IntSR怎样同时处理显式搜索词和没有搜索词的推荐意图？ 显式查询给出当前表达，隐式会话历史补充未说出的需求，两者共同推断潜在意图，再以统一物品或POI词表生成结果。时间上下文帮助区分需求是否仍有效，减少搜索与推荐之间的语义割裂。统一词表不意味着可以忽略查询约束，也不能把旧会话中的兴趣当成用户现在明确提出的要求。 示意：用户搜附近咖啡，历史显示偏好安静环境，模型可同时利用二者；若只是浏览推荐，则从会话推断需求，但不能把昨日地点当成今日仍然有效的位置。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-intsr-9d48eca1" class="ar-learning-paper-anchor"></span>
<h2 id="qa-fb387442d699fb31">IntSR怎样同时处理显式搜索词和没有搜索词的推荐意图？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aintsr">IntSR: An Integrated Generative Framework for Search and Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Amap</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>显式查询给出当前表达，隐式会话历史补充未说出的需求，两者共同推断潜在意图，再以统一物品或POI词表生成结果。时间上下文帮助区分需求是否仍有效，减少搜索与推荐之间的语义割裂。统一词表不意味着可以忽略查询约束，也不能把旧会话中的兴趣当成用户现在明确提出的要求。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户搜附近咖啡，历史显示偏好安静环境，模型可同时利用二者；若只是浏览推荐，则从会话推断需求，但不能把昨日地点当成今日仍然有效的位置。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2509.21179">原论文</a> · <a href="../../../../reproductions/2509.21179-intsr/">实现解读</a> · <a href="#qa-fb387442d699fb31">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onerec-v2" data-paper-title="OneRec-V2 Technical Report" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneRec-V2 Technical Report 搜广推与 LLM 应用 Kuaishou 2025-08-28 OneRec-V1 用 encoder-decoder 生成推荐 session，但长历史 encoder 重复计算，偏好对齐又依赖额外 reward model。V2 只把最新曝光作为监督目标；Context Processor 一次生成所有 decoder 层共享的 K/V，目标侧只解码 [BOS,s1,s2]→[s1,s2,s3]。Lazy block 依次执行 cross-attention、causal self-attention 和 FFN，并结合 GQA、K=V、跨层 KV sharing。 Fidelity: 完整核心链路复现。实际训练三层 residual-quantized Semantic ID、newest-impression SFT、layer-shared K/V Lazy Decoder、Duration-Aware Reward Shaping 和 GBPO；仅缩小模型/数据，省略私有异构特征与分布式 serving。本地对照口径：效率基线是 Encoder-Decoder，实验组 Lazy SFT 的延迟 -54.78%、validation loss -0.34%；对齐基线是 Lazy SFT，加入 GBPO 后反馈加权概率 +21.66%。  llm-recommendation generative-retrieval reinforcement-learning 搜广推 生成式召回与推理推荐 OneRec-V2 为什么只监督最新曝光，并让所有 decoder 层共享一次生成的上下文 K/V？ 最新曝光监督把训练目标集中到请求末端，避免为每个历史位置重复做完整目标解码。Context Processor 一次产生可被多个解码层复用的上下文 K/V，Lazy block 再按需交互并生成短 SID。它减少的是历史编码与逐层缓存的重复成本；后训练的真实反馈对齐是另一条改动，不能把全部效果归给共享 K/V。 示意：用户有很长历史，当前只需要预测最新请求的三层物品码。先把历史处理成一份共享记忆，解码各层重复读取它，比每层各自重新构造整段历史缓存更节省。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-onerec-v2-8a1036e5" class="ar-learning-paper-anchor"></span>
<h2 id="qa-6a8c770978f6160d">OneRec-V2 为什么只监督最新曝光，并让所有 decoder 层共享一次生成的上下文 K/V？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonerec-v2">OneRec-V2 Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最新曝光监督把训练目标集中到请求末端，避免为每个历史位置重复做完整目标解码。Context Processor 一次产生可被多个解码层复用的上下文 K/V，Lazy block 再按需交互并生成短 SID。它减少的是历史编码与逐层缓存的重复成本；后训练的真实反馈对齐是另一条改动，不能把全部效果归给共享 K/V。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户有很长历史，当前只需要预测最新请求的三层物品码。先把历史处理成一份共享记忆，解码各层重复读取它，比每层各自重新构造整段历史缓存更节省。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.20900">原论文</a> · <a href="../../../../reproductions/2508.20900-onerec-v2/">实现解读</a> · <a href="#qa-6a8c770978f6160d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pinrec" data-paper-title="PinRec: Outcome-Conditioned, Multi-Token Generative Retrieval for Industry-Scale Recommendation Systems" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="PinRec: Outcome-Conditioned, Multi-Token Generative Retrieval for Industry-Scale Recommendation Systems 搜广推与 LLM 应用 Pinterest 2025-04-09 普通 next-item 只会延续用户最常见行为，且严格顺序不适合 feed session。PinRec 把期望 outcome 注入输出头，并在同一未来窗口一次生成多个 ANN-compatible item vectors。 Fidelity: 完整核心链路复现。真实执行因果 decoder、outcome embedding、归一化 ANN 输出、无序未来窗口 multi-token 对比学习；MovieLens 评分档位替代 Pinterest 多 surface action。本地对照口径：基线是 unconditioned next-token 模型；实验组是 outcome-conditioned 三 token window；Unordered Recall@10 -27.78%、NDCG@10 -34.82%。这是 outcome/multi-token 模块消融，不是相对 DIN。  generative-retrieval outcome-conditioning multi-token 搜广推 生成式召回与推理推荐 PinRec 为什么把期望 outcome 注入输出头，并在未来窗口预测多个物品向量？ 单一 next-item 目标容易重复用户最常见行为，也把同一窗口的消费强加为固定顺序。期望 outcome 提供行为条件，多输出头预测窗口内多个 ANN 兼容向量，使检索能覆盖并存兴趣。向量可接现有近邻系统，但训练需要处理预测与窗口正例的对应，不能把多个头仅当成重复采样同一个最热门物品。 示意：希望用户收藏而非随手浏览时，输出条件切换为收藏。一个未来窗口同时有园艺和烘焙内容，多向量可以覆盖两类兴趣，不必认为先看园艺才是唯一正确顺序。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-pinrec-66bf0193" class="ar-learning-paper-anchor"></span>
<h2 id="qa-2ea183949a2f6b44">PinRec 为什么把期望 outcome 注入输出头，并在未来窗口预测多个物品向量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apinrec">PinRec: Outcome-Conditioned, Multi-Token Generative Retrieval for Industry-Scale Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单一 next-item 目标容易重复用户最常见行为，也把同一窗口的消费强加为固定顺序。期望 outcome 提供行为条件，多输出头预测窗口内多个 ANN 兼容向量，使检索能覆盖并存兴趣。向量可接现有近邻系统，但训练需要处理预测与窗口正例的对应，不能把多个头仅当成重复采样同一个最热门物品。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>希望用户收藏而非随手浏览时，输出条件切换为收藏。一个未来窗口同时有园艺和烘焙内容，多向量可以覆盖两类兴趣，不必认为先看园艺才是唯一正确顺序。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.10507">原论文</a> · <a href="../../../../reproductions/2504.10507-pinrec/">实现解读</a> · <a href="#qa-2ea183949a2f6b44">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cobra" data-paper-title="Sparse Meets Dense: Unified Generative Recommendations with Cascaded Sparse-Dense Representations" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Sparse Meets Dense: Unified Generative Recommendations with Cascaded Sparse-Dense Representations 搜广推与 LLM 应用 Baidu 2025-03-04 纯 Semantic ID 在量化阶段丢失细粒度信息。COBRA 先生成稀疏 code，再以 code 条件生成可端到端更新的 dense vector；推理先 beam 搜索 code，再用 dense 最近邻细排。 Fidelity: 完整核心链路复现。稀疏 S-ID、以 S-ID 为条件的稠密向量、联合训练和 coarse-to-fine BeamFusion 均执行；生产 ANN 服务未复刻。本地对照口径：统一跨模型基线是 DIN，COBRA NDCG@10 相对 DIN +25.75%；内部 sparse-only 基线加入 dense cascade 后 +45.83%。两项提升不能相互替代。180 users/280 items、seeds 42–44。统一 DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；  generative-retrieval semantic-id dense-retrieval 搜广推 生成式召回与推理推荐 COBRA已经生成了稀疏SID，为什么还要按SID条件生成稠密向量？ 语义量化保留粗结构，却会丢失码内的细节。COBRA先用离散路径缩小搜索范围，再让用户上下文与该路径共同产生稠密查询，区分共享粗码的物品；稀疏与稠密目标联合训练以减少接口错位。后级细排只能区分前级保留的候选，无法保证找回已被beam排除的正确路径。 示意：粗码先选中运动鞋，条件稠密向量再区分越野鞋与公路鞋；若第一步误去了家电分支，第二步再精细也难把正确鞋款补回来。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-cobra-75daff60" class="ar-learning-paper-anchor"></span>
<h2 id="qa-fc61d6dcbcc97925">COBRA已经生成了稀疏SID，为什么还要按SID条件生成稠密向量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acobra">Sparse Meets Dense: Unified Generative Recommendations with Cascaded Sparse-Dense Representations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Baidu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语义量化保留粗结构，却会丢失码内的细节。COBRA先用离散路径缩小搜索范围，再让用户上下文与该路径共同产生稠密查询，区分共享粗码的物品；稀疏与稠密目标联合训练以减少接口错位。后级细排只能区分前级保留的候选，无法保证找回已被beam排除的正确路径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>粗码先选中运动鞋，条件稠密向量再区分越野鞋与公路鞋；若第一步误去了家电分支，第二步再精细也难把正确鞋款补回来。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2503.02453">原论文</a> · <a href="../../../../reproductions/2503.02453-cobra/">实现解读</a> · <a href="#qa-fc61d6dcbcc97925">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onerec" data-paper-title="OneRec: Unifying Retrieve and Rank with Generative Recommender and Iterative Preference Alignment" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneRec: Unifying Retrieve and Rank with Generative Recommender and Iterative Preference Alignment 搜广推与 LLM 应用 Kuaishou 2025-02-26 传统 retrieve→rank 多阶段系统目标割裂；已有生成式召回又多为 point-wise next-item generation，难以保证一个推荐 session 内的连贯性与多样性。OneRec 用三层 RQ Semantic ID 表示物品，以 MoE 模型一次生成 5 个目标物品的完整 session，并训练个性化 reward model 预测 watch/interaction 指标。 Fidelity: 完整核心链路复现。当前代码实际训练 RQ Semantic IDs、session-wise encoder-decoder、稀疏 MoE、个性化 reward model 和 self-hard DPO；仅缩小模型、session 长度和公开数据规模。本地对照口径：基线是 Session Generator SFT；实验组是 reward model+self-hard DPO 后的 OneRec；NDCG@10 从 0.01565 降至 0（-100%）。这是 preference alignment 阶段消融，不是 OneRec 相对 DIN 的结果。   搜广推 生成式召回与推理推荐 OneRec 为什么从当前模型生成的完整 session 中选 self-hard 胜负对，而不是逐个物品做偏好训练？ 完整 session 把项目之间的连贯性与多样性纳入同一生成对象，奖励模型也据此评价整段推荐。当前模型产生的较难区分胜负对，能把偏好更新集中到模型实际容易混淆的方案上；DPO 比较胜负 session 相对参考模型的概率变化。奖励误差仍会影响方向，本地小规模结果也没有验证线上收益。 示意：两组五条视频都单条相关，但一组内容重复，另一组节奏更连贯。把整组作为胜负对象，模型才有机会学到“这几条放在一起更合适”，而非只提升某条视频概率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-onerec-bec96f9e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-4d76f811142e31ca">OneRec 为什么从当前模型生成的完整 session 中选 self-hard 胜负对，而不是逐个物品做偏好训练？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonerec">OneRec: Unifying Retrieve and Rank with Generative Recommender and Iterative Preference Alignment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>完整 session 把项目之间的连贯性与多样性纳入同一生成对象，奖励模型也据此评价整段推荐。当前模型产生的较难区分胜负对，能把偏好更新集中到模型实际容易混淆的方案上；DPO 比较胜负 session 相对参考模型的概率变化。奖励误差仍会影响方向，本地小规模结果也没有验证线上收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两组五条视频都单条相关，但一组内容重复，另一组节奏更连贯。把整组作为胜负对象，模型才有机会学到“这几条放在一起更合适”，而非只提升某条视频概率。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.18965">原论文</a> · <a href="../../../../reproductions/2502.18965-onerec/">实现解读</a> · <a href="#qa-4d76f811142e31ca">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sessionrec" data-paper-title="SessionRec: Next Session Prediction Paradigm For Generative Sequential Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="SessionRec: Next Session Prediction Paradigm For Generative Sequential Recommendation 搜广推与 LLM 应用 Meituan 2025-02-14 逐物品 next-item 训练把同一消费意图中的多个物品硬排成先后标签，也无法把“下一次访问会同时消费的一组物品”作为多正例。SessionRec 先由 Item-based Session Encoder（ISE）把一次访问中的物品聚合为 session token，再由 Session-based Sequence Encoder（SSE）建模跨 session 兴趣迁移，最终让一个 query 同时召回下一 session 的所有正例。 Fidelity: 核心机制复现。真实执行 session 内聚合、session 间 Transformer、多正例 next-session retrieval，以及 session 内曝光负例排序损失；私有特征与 ANN 服务未复刻。本地对照口径：基线是等预算的扁平 Item Transformer；实验组是 SessionRec Transformer；NDCG@20 从 0.004718 降至 0.003678（-22.05%）。这是 session 建模消融；DIN 未在 KuaiRand session 任务中参与比较。  session recommendation generative retrieval 搜广推 生成式召回与推理推荐 SessionRec 为什么先把一次访问聚成 session token，再预测下一 session 的多正例？ 同次访问的多个物品常共享一个意图，逐物品训练会把它们硬排成唯一先后关系。ISE 先聚合会话内部内容，SSE 再学习会话之间的兴趣迁移，目标将下一会话全部正反馈作为正例，并利用真实未点击曝光区分难负例。它改变了监督单位，不是单纯缩短序列；会话划分错误也可能混合不同意图。 示意：一次访问同时看帐篷、睡袋和防潮垫，下一次访问关注徒步鞋。先用一个会话 token 表达露营采购，再预测下一组需求，比认定“睡袋后唯一应看防潮垫”更贴近组消费。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-sessionrec-2fd19641" class="ar-learning-paper-anchor"></span>
<h2 id="qa-9400ea46fb6842b9">SessionRec 为什么先把一次访问聚成 session token，再预测下一 session 的多正例？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asessionrec">SessionRec: Next Session Prediction Paradigm For Generative Sequential Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同次访问的多个物品常共享一个意图，逐物品训练会把它们硬排成唯一先后关系。ISE 先聚合会话内部内容，SSE 再学习会话之间的兴趣迁移，目标将下一会话全部正反馈作为正例，并利用真实未点击曝光区分难负例。它改变了监督单位，不是单纯缩短序列；会话划分错误也可能混合不同意图。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次访问同时看帐篷、睡袋和防潮垫，下一次访问关注徒步鞋。先用一个会话 token 表达露营采购，再预测下一组需求，比认定“睡袋后唯一应看防潮垫”更贴近组消费。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.10157">原论文</a> · <a href="../../../../reproductions/2502.10157-sessionrec/">实现解读</a> · <a href="#qa-9400ea46fb6842b9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:leadre" data-paper-title="LEADRE: Multi-Faceted Knowledge Enhanced LLM Empowered Display Advertisement Recommender System" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="LEADRE: Multi-Faceted Knowledge Enhanced LLM Empowered Display Advertisement Recommender System 搜广推与 LLM 应用 Tencent / WeChat 2024-11-21 ID 召回难利用广告内容。LEADRE 以跨域行为、长期总结和实时行为构造 intent-aware prompt，将广告量化为 S-ID，并用广告语义/商业价值辅助任务和 DPO 对齐，线上把长期生成缓存与实时服务组合。 Fidelity: 完整核心链路复现。Semantic ID、长短期/商业意图、语义与价值辅助任务、SFT→DPO 和可缓存/实时双路径均执行；私有广告与生产服务未复刻。本地对照口径：统一跨模型基线是 DIN，LEADRE NDCG@10 相对 DIN +12.94%；内部基线是 S-ID 多任务 SFT，继续 DPO 后 -4.53%。主结论与对齐阶段消融分开报告。MovieLens-100K，180 users/280 items，seeds 42–44。统一 DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；  llm-recommendation generative-retrieval advertising preference-alignment 搜广推 生成式召回与推理推荐 LEADRE为什么用意图prompt、语义辅助任务和DPO共同训练广告SID生成？ 单独预测离散码可能只记住曝光ID，难利用广告内容与跨域需求。意图prompt整理长期与实时信号，语义和商业价值目标赋予码更明确的推荐含义，DPO再调整偏好取舍。偏好优化不保证每项检索指标都提高，内部SFT到DPO的变化应单独报告，而非借整体模型对另一基线的提升遮盖。 示意：同属家电类的两个广告可能一个符合当前装修意图、另一个只是高频曝光；语义与价值监督帮助区分，但DPO过度偏商业反馈也可能损害新增相关候选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-leadre-72cfaef2" class="ar-learning-paper-anchor"></span>
<h2 id="qa-cbbfe12497e2d087">LEADRE为什么用意图prompt、语义辅助任务和DPO共同训练广告SID生成？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aleadre">LEADRE: Multi-Faceted Knowledge Enhanced LLM Empowered Display Advertisement Recommender System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent / WeChat</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单独预测离散码可能只记住曝光ID，难利用广告内容与跨域需求。意图prompt整理长期与实时信号，语义和商业价值目标赋予码更明确的推荐含义，DPO再调整偏好取舍。偏好优化不保证每项检索指标都提高，内部SFT到DPO的变化应单独报告，而非借整体模型对另一基线的提升遮盖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同属家电类的两个广告可能一个符合当前装修意图、另一个只是高频曝光；语义与价值监督帮助区分，但DPO过度偏商业反馈也可能损害新增相关候选。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2411.13789">原论文</a> · <a href="../../../../reproductions/2411.13789-leadre/">实现解读</a> · <a href="#qa-cbbfe12497e2d087">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tiger" data-paper-title="Recommender Systems with Generative Retrieval" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Recommender Systems with Generative Retrieval 搜广推与 LLM 应用 Google / Google DeepMind 2023-05-08 传统召回为每个物品维护独立 ID embedding，难以共享语义，也无法自然生成新物品。TIGER 先把内容向量量化成分层 Semantic ID，再让 encoder-decoder 像生成 token 一样生成下一个物品；同一语义前缀的冲突由额外 token 消解。 保真度：核心机制复现。保真度：核心机制复现。RQ-VAE、残差语义 ID、collision token 和自回归 Transformer 检索链路均实际训练；MovieLens genre 替代 Sentence-T5 商品文本，省略 hashed user token 与 cold-start epsilon mixing。本地对照口径：基线是词表容量和参数量匹配的随机分层 ID 生成器；实验组是 TIGER Semantic ID；NDCG@10 从 0.01043 降至 0.00635（-39.16%）。这是 ID 方案消融，不是相对 DIN 的比较。   搜广推 生成式召回与推理推荐 TIGER 的残差量化 SID 为什么比随机分层 ID 更有语义共享能力，还需要碰撞 token？ 残差量化先用粗层中心解释内容向量，再逐层编码剩余误差，因此相近内容有机会共享前缀，生成器可复用粗到细的决策。有限码本仍可能把不同物品映成同一路径，额外碰撞 token 才提供唯一地址。语义共享不保证推荐一定更好，随机分层对照能帮助隔离“有层级”和“层级有语义”的区别。 示意：两本园艺书先共享园艺前缀，后层区分室内种植与户外栽培；若细码仍相同，最后用碰撞码分开，避免生成同一条路径时不知道究竟服务哪本书。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<span id="paper-recommendation-tiger-7436853d" class="ar-learning-paper-anchor"></span>
<h2 id="qa-41bf45ff5bebea3c">TIGER 的残差量化 SID 为什么比随机分层 ID 更有语义共享能力，还需要碰撞 token？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atiger">Recommender Systems with Generative Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>残差量化先用粗层中心解释内容向量，再逐层编码剩余误差，因此相近内容有机会共享前缀，生成器可复用粗到细的决策。有限码本仍可能把不同物品映成同一路径，额外碰撞 token 才提供唯一地址。语义共享不保证推荐一定更好，随机分层对照能帮助隔离“有层级”和“层级有语义”的区别。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两本园艺书先共享园艺前缀，后层区分室内种植与户外栽培；若细码仍相同，最后用碰撞码分开，避免生成同一条路径时不知道究竟服务哪本书。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.05065">原论文</a> · <a href="../../../../reproductions/2305.05065-tiger/">实现解读</a> · <a href="#qa-41bf45ff5bebea3c">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

把物品改写成token后，推荐究竟改变了哪一步？

## 记住这一点

生成式召回把候选选择改为在用户上下文下生成物品码：先建立可还原到目录的标识，再学习码序列分布，最后用约束解码得到可服务物品。TIGER串起量化与自回归检索，COBRA进一步级联稀疏码和稠密表示，PLUM把推荐数据继续预训练接到已有语言模型。偏好优化与推理token是在这条链路上改变训练或搜索。

## 一个例子

目录里只有代码(3,7)和(3,9)，模型却给(3,5)很高概率。即使生成文本看起来合理，这也不是有效商品；解码必须服从目录约束。若两个商品共享同一码，还要处理碰撞或保留后续区分路径。

## 什么时候要小心

token loss下降不等于Recall提高，增加beam也不能恢复被错误码本或前缀约束排除的物品。部分论文同时生成列表，归组看主要生成机制，列表价值可接着读重排主题；本地缩小训练不等同于复现生产规模。

## 先读这几篇

按TIGER的离散ID生成→COBRA的稀疏—稠密级联→PLUM的已有LLM继续预训练阅读；这三篇有实际本地核心链路，但TIGER和PLUM的本地结果并未验证最终召回提升。

1. [Recommender Systems with Generative Retrieval](../../../reproductions/2305.05065-tiger/README.md) · [原论文](https://arxiv.org/abs/2305.05065)
2. [Sparse Meets Dense: Unified Generative Recommendations with Cascaded Sparse-Dense Representations](../../../reproductions/2503.02453-cobra/README.md) · [原论文](https://arxiv.org/abs/2503.02453)
3. [PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations](../../../reproductions/2510.07784-plum/README.md) · [原论文](https://arxiv.org/abs/2510.07784)

## 自测一下

模型能生成格式正确的三层SID，为什么仍可能没有有效召回？

??? note "展开参考答案"

    格式正确只保证长度和词表合法；组合可能不在目录中，也可能对应多个物品或错误兴趣。还需检查目录可达性、碰撞消解，以及隔离测试集上的候选覆盖和排序质量。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
