---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 从列表边际价值到出价控制：策略权重与约束

[搜广推](../index.md) · 更新 2026-10-30 · 37 篇主题资料 / 5 篇重点对照

CDM把相关性与去冗余的教师选择蒸馏给学生，SORT-Gen直接估计前缀条件下的列表边际价值，PRL-PUTS扫描多目标权重策略，Primal-Dual Decoding则在解码中根据约束松弛量更新乘子。它们分别改变列表上下文、效用模型、策略选择和约束控制，不能把多样性更高或某一目标更好当成全面胜出。 RLBP把相同的多目标治理问题带到日级PID参数选择，但其BU/CPC奖励和控制动作不能当成列表逐项效用。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/recommendation/slates-business-value.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：价值属于单物品、已选前缀还是整套策略 · 训练期蒸馏与推理期搜索的分工 · 固定权重、Pareto筛选与动态乘子 · 软目标与硬可行性及代理收入边界

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [Contextual Distillation Model for Diversified Recommendation](../../../reproductions/2406.09021-cdm/README.md) · [原始来源](https://arxiv.org/abs/2406.09021)<br>章节：背景与主要改动、核心公式、复现边界 | 用MMR教师在相关性分数上减已选物品的最大相似度，生成上下文边际监督，再训练学生低延迟模仿。 | 把列表去冗余压入可服务模型，但学生继承教师目标与相似度定义；更不相似不保证更满意，公开数据结果也非生产收益。 |
| [A Generative Re-ranking Model for List-level Multi-objective Optimization at Taobao](../../../reproductions/2505.07197-sort-gen/README.md) · [原始来源](https://arxiv.org/abs/2505.07197)<br>章节：背景与主要改动、核心公式、复现边界 | causal Transformer按前缀预测CLICK/PAY累计计数的ordered-regression概率，估计追加物品的边际价值；多目标队列与mask缩小搜索。 | 显式处理前缀效应，也引入队列候选范围和批量搜索近似；本地点击/交易/GMV是公开数据代理，单次PyTorch调用不等价生产kernel延迟。 |
| [A Production-Ready RL Framework for Personalized Utility Tuning with Pareto Sweeping in Pinterest Recommender Systems](../../../reproductions/2605.16344-prl-puts/README.md) · [原始来源](https://arxiv.org/abs/2605.16344)<br>章节：背景与主要改动、核心公式、复现边界 | 双头Q分别估计Repin和P2P utility，对不同权重策略作Pareto sweeping，再在线选择可治理策略。 | Pareto不劣只表示没有另一候选同时不差且至少一项更好，并不保证两项都超过原策略；策略权重选择与列表内逐项边际估计不同。 |
| [Stochastic Primal-Dual Decoding for Multiobjective Generative Recommender Systems](../../../reproductions/2607.19357-primal-dual-decoding/README.md) · [原始来源](https://arxiv.org/abs/2607.19357)<br>章节：背景与主要改动、核心公式、复现边界 | 不重训生成器，在逐位置选择中加入辅助贡献，并用剩余约束松弛量以镜像下降更新乘子。 | 乘子可随已选前缀改变压力，但软惩罚不是硬可行性证明；若剩余候选无法满足约束，权重再大也不能制造可行解。本地只验证代理机制。 |
| [Reinforcement Learning for Controller Parameters in the Auto-Bidding System at Pinterest](../../../recommendation-components/2610.33248-pinterest-rlbp/README.md) · [原始来源](https://arxiv.org/abs/2610.33248v1)<br>章节：背景与主要改动、核心公式、高成本完整实验 | 日级选择九种P/I倍率且D固定，生产gamma0回归BU/CPC相对lift，推理用Qbu−betaQcpc再topK softmax，服务保留PID。 | 不同于PRL-PUTS的Repin/P2P策略扫描；CPC改善的reward仍是负值，多步max/min是扩展，生产beta幅度与数值预处理外置。 |

</div>

## 取舍分析 {#analysis}

### 同一个分数需要回答不同层级的问题

CDM的MMR教师认为与已选内容重复会降低新增价值；SORT-Gen把列表前缀放进预测器，让点击和交易预期随前缀变化。PRL-PUTS则在Q估计之上挑不同目标权重的策略，不等于每个物品有一个永远正确的固定分。应分别比较效用估计、候选搜索和策略治理，不把预测器变化与权重调节混为一谈。

对照来源：[cdm](../../../reproductions/2406.09021-cdm/README.md) · [sort-gen](../../../reproductions/2505.07197-sort-gen/README.md) · [prl-puts](../../../reproductions/2605.16344-prl-puts/README.md)

### 多目标偏好不能替代合法性检查

PRL-PUTS用Pareto扫描保留值得权衡的策略，Primal-Dual Decoding用动态乘子调整解码压力；二者都在表达目标取舍。SORT-Gen里的已选mask则阻止重复选择，属于另一种可行性条件。有限权重允许目标相互补偿，所以广告量、库存或去重的硬要求仍应独立验证，不能仅看总reward达标。

对照来源：[prl-puts](../../../reproductions/2605.16344-prl-puts/README.md) · [primal-dual-decoding](../../../reproductions/2607.19357-primal-dual-decoding/README.md) · [sort-gen](../../../reproductions/2505.07197-sort-gen/README.md)

### 相同双头形式，不是相同控制问题

PRL-PUTS分别估计Repin/P2P效用，再扫描权重策略；RLBP的两个头则预测日级BU和CPC相对生产基线的变化，选择的是PID系数而非推荐物品。因为CPC越低越好，负lift不能先翻成正奖励再在融合时再次取负。部署gamma=0也意味着并未用跨日bootstrap学长期Q；生命周期取舍由外部beta表达。两头各自max/min的多步扩展不保证融合后就是组合目标的最优Q，七天A/B与两月非均衡holdout也应分开解释。

对照来源：[pinterest-rlbp](../../../recommendation-components/2610.33248-pinterest-rlbp/README.md) · [prl-puts](../../../reproductions/2605.16344-prl-puts/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### CDM和SORT-Gen为什么都不应把物品的独立CTR当成列表里永远不变的价值？ {#cross-prefix-changes-marginal-value}

??? note "展开答案与例子"

    **答案：** 已选前缀会改变新增物品的贡献。CDM用与前缀的最大相似度扣除重复性，SORT-Gen则条件于前缀预测累计行为并估计边际价值；两者建模方式不同，但都否定固定点分数足以描述整页收益。是否值得牺牲即时分数仍需按目标评估。

    **教学例子：** 示意：前三个高分视频是同一段滑雪镜头，露营视频独立分略低；当前缀已含滑雪时，露营的新增信息可能更大，但这不是未经测量的CTR提升结论。

    对照来源：[cdm](../../../reproductions/2406.09021-cdm/README.md) · [sort-gen](../../../reproductions/2505.07197-sort-gen/README.md)

### PRL-PUTS保留一条Pareto策略，是否表示它在Repin、P2P和列表质量上都更好？ {#cross-pareto-is-not-universal-win}

??? note "展开答案与例子"

    **答案：** 不表示。Pareto筛选相对给定候选策略和估计目标定义，只排除被同时支配的点；一个策略可以提高Repin却降低P2P。SORT-Gen或CDM的列表上下文目标又是不同层级，不能把双目标不劣直接推广成所有列表指标改善。

    **教学例子：** 示意：策略A的两项效用为(10,6)，B为(8,9)，二者互不支配；保留B不是证明它全面优于A，更没有说明两者的重复曝光率。

    对照来源：[prl-puts](../../../reproductions/2605.16344-prl-puts/README.md) · [sort-gen](../../../reproductions/2505.07197-sort-gen/README.md) · [cdm](../../../reproductions/2406.09021-cdm/README.md)

### Primal-Dual Decoding动态增大约束乘子后，为什么仍要单独检查列表可行性？ {#cross-adaptive-weights-not-hard-guarantees}

??? note "展开答案与例子"

    **答案：** 乘子调整的是软选择压力，不改变剩余候选是否存在可行组合。若必须覆盖的类别已被早期选择排除，后续加权无法补回。SORT-Gen的去重mask体现硬排除与价值评分的区别，PRL-PUTS的权重扫描也不能自动承担所有业务硬规则。

    **教学例子：** 示意：最后只剩一个位置，却还要求覆盖两个互斥类别，任何乘子都无法满足；系统应报告不可行或采用预先约定的回退，而非只显示更高总分。

    对照来源：[primal-dual-decoding](../../../reproductions/2607.19357-primal-dual-decoding/README.md) · [sort-gen](../../../reproductions/2505.07197-sort-gen/README.md) · [prl-puts](../../../reproductions/2605.16344-prl-puts/README.md)

### RLBP与PRL-PUTS都有双头Q和可调权重，为什么不能直接共享动作/奖励解释？ {#cross-rlbp-two-heads-not-listwise-q}

??? note "展开答案与例子"

    **答案：** PRL-PUTS围绕Repin/P2P的推荐策略取舍，RLBP按日选PID倍率以平衡预算利用率和CPC。RLBP保留负CPC lift，在Qbu−betaQcpc中让低成本更受偏好；部署gamma0是单步daily目标，不能套用一个通用长期列表Q解释两者。

    **教学例子：** 教学示意：CPC从1降到0.9得到reward -0.1；减beta乘该值会提高融合分数。若先把它改为+0.1再照公式相减，就反而惩罚了成本下降。

    对照来源：[pinterest-rlbp](../../../recommendation-components/2610.33248-pinterest-rlbp/README.md) · [prl-puts](../../../reproductions/2605.16344-prl-puts/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-30** · 精读RLBP日级九动作、部署gamma0、负CPC lift、Q融合与外部预处理；相对PRL-PUTS双目标策略扫描区分状态/动作/回报，扩宽专题标题但保留稳定id和原阅读路径。

涉及：[pinterest-rlbp](../../../recommendation-components/2610.33248-pinterest-rlbp/README.md) · [prl-puts](../../../reproductions/2605.16344-prl-puts/README.md)

**2026-10-27** · 首版：比较cdm、sort-gen、prl-puts、primal-dual-decoding，围绕价值属于单物品、已选前缀还是整套策略与训练期蒸馏与推理期搜索的分工建立分析和跨论文问答。

覆盖 36 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 37 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [Adaptive Ad Load Design for Sponsored Search Markets: Evidence, Theory, and Deployment](../../../reproductions/2607.14418-adaptive-ad-load/README.md)
- [Contextual Distillation Model for Diversified Recommendation](../../../reproductions/2406.09021-cdm/README.md)
- [Constraint-Aware Generative Re-ranking for Multi-Objective Optimization in Advertising Feeds](../../../reproductions/2603.04227-cgr/README.md)
- [Challenges and Solutions for Bandits in the Wild: Warm-Started Mixture Bandits for Cross-Cohort Slate Recommendation](../../../reproductions/2609.37800-cohortmix-ts/README.md)
- [DEGR: Dual Exploration-Driven Generative Re-Ranking for Adaptive Cross-Request Context Bridging](../../../reproductions/2608.04809-degr/README.md)
- [DeGRe: Listwise Generative Reranking with Offline Lookahead Distillation](../../../reproductions/2605.25749-degre/README.md)
- [DIRECTOR: Dynamic Index-based Recommendation with Transport-Optimized Retrieval](../../../reproductions/2607.26418-director/README.md)
- [Long-term User Engagement Optimization through Model-agnostic Downstream Rewards Learning](../../../reproductions/2607.14192-downstream-rewards/README.md)
- [DREAM: A Dual-Loop Recommendation Evolution Framework Powered by Large Language Models](../../../reproductions/2608.09408-dream/README.md)
- [DrEM: Dual-Side Robust Ensemble Ranking from Noisy User Preference Predictions in Video Recommendation](../../../reproductions/2608.12778-drem/README.md)
- [Deep Reinforcement Learning for Ranking Utility Tuning in the Ad Recommender System at Pinterest](../../../reproductions/2509.05292-drl-put/README.md)
- [Dual-Rerank: Fusing Sequential Dependencies and Utility for Generative Reranking](../../../reproductions/2604.07420-dual-rerank/README.md)
- [GenPage: Towards End-to-End Generative Homepage Construction at Netflix](../../../reproductions/2606.31031-genpage/README.md)
- [Generate to Explore, Select to Exploit: Aligning LLM-based Headline Generation with Personalized Recommendation](../../../reproductions/2609.15094-gese/README.md)
- [From Local Indices to Global Identifiers: Generative Reranking via Global Action Space](../../../reproductions/2604.25291-glorank/README.md)
- [Rethinking Multi-objective Ranking Ensemble in Recommender System: From Score Fusion to Rank Consistency](../../../reproductions/2601.02955-harmonrank/README.md)
- [Hierarchical Contextual Uplift Bandits for Catalog Personalization](../../../reproductions/2601.14333-hcub/README.md)
- [HiGR: Industrial-Scale Hierarchical Generative Slate Recommendation Framework in Tencent](../../../reproductions/2512.24787-higr/README.md)
- [A Long-term Value Prediction Framework In Video Ranking](../../../reproductions/2602.17058-ltv-video-ranking/README.md)
- [MAPS: A Multi-Agent Personalized Script-Driven Video Advertising System Enhanced by Reinforcement Learning](../../../recommendation-components/2610.25748-maps-creative/README.md)
- [MetaStrategy: Generative Ranking with Executable LLM Strategies](../../../reproductions/2608.09440-metastrategy/README.md)
- [Once Generated, Ranked: End-to-End Generative Slate Recommendation with Unified Semantic-Collaborative IDs](../../../reproductions/2608.17613-ogr/README.md)
- [PIANO: Personalized Reranking via Information Aggregation Node for Music Search Optimization](../../../reproductions/2606.16641-piano/README.md)
- [PinDCO: Whole-Page Aware Dynamic Creative Optimization at Scale](../../../reproductions/2609.11943-pindco/README.md)
- [Stochastic Primal-Dual Decoding for Multiobjective Generative Recommender Systems](../../../reproductions/2607.19357-primal-dual-decoding/README.md)
- [A Production-Ready RL Framework for Personalized Utility Tuning with Pareto Sweeping in Pinterest Recommender Systems](../../../reproductions/2605.16344-prl-puts/README.md)
- [PSG: Pair-Space Generation for Efficient Generative Reranking](../../../reproductions/2607.26427-psg/README.md)
- [LLM-Based Re-Ranking for Real Estate Search](../../../reproductions/2607.14835-real-estate-rerank/README.md)
- [SaFRO: Satisfaction-Aware Fusion via Dual-Relative Policy Optimization for Short-Video Search](../../../reproductions/2603.19585-safro/README.md)
- [A Generative Re-ranking Model for List-level Multi-objective Optimization at Taobao](../../../reproductions/2505.07197-sort-gen/README.md)
- [Online Advertising with Spatial Interactions](../../../recommendation-components/2602.12481-spatial-ads/README.md)
- [A Self-Triggered Agentic Push Recommendation System](../../../reproductions/2608.01949-steps/README.md)
- [Beyond Single-Episode Optimization: Sliding-Window Aware Generative Auto-Bidding for Long-Term Advertising Effectiveness](../../../reproductions/2607.25233-swag-bid/README.md)
- [Taiji: Pareto Optimal Policy Optimization with Semantics-IDs Trade-off for Industrial LLM-Enhanced Recommendation](../../../reproductions/2606.03866-taiji/README.md)
- [Uncertainty as Remedy: Mitigating Satisfaction Label Bias in Short Video Multi-Objective Ensemble Ranking](../../../reproductions/2607.17092-uame/README.md)
- [Breaking the Loop: An Empirical Comparison of Strategies for Novelty and Freshness in YouTube Music](../../../reproductions/2607.23749-youtube-freshness/README.md)
- [Reinforcement Learning for Controller Parameters in the Auto-Bidding System at Pinterest](../../../recommendation-components/2610.33248-pinterest-rlbp/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/recommendation/slates-business-value.md) · [返回全部精读卡片](../index.md)
