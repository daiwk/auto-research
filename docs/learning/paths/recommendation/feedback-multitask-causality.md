---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 学习信号、多任务与反馈偏差

[搜广推](index.md) / 子主题导学 · 约 3 分钟 · 35 张论文卡

## 先想一个问题

观察到的点击和转化，究竟能监督哪一个概率或价值？

## 记住这一点

先定义标签再选网络：ESMM区分曝光后点击率、点击后转化率及二者联合事件；MMoE用任务独立门控共享专家，PLE再区分共享与任务专属信息。时长、延迟转化、曝光选择和归因会改变监督含义，伪标签与集合奖励分配也须说明依据。因果增量又多了一层反事实问题，不能由预测准确率自动推出。

## 一个例子

1000次曝光中，点击率为10%，点击后的转化率为20%，对应点击且转化概率为2%，约20次转化。这20次不能简单归因于一次新策略：其中一部分用户可能原本就会购买。

## 什么时候要小心

多任务共享不自动消除选择偏差；把未点击都标为CVR负例会混淆条件概率。延迟反馈、缺失特征和曝光策略也不是同一种噪声，需按各论文的观测假设验证；合成标签只支持相应机制检查。

## 先读这几篇

先用ESMM把漏斗概率说清，再用MMoE理解任务如何选择共享专家，最后用PLE看强冲突任务如何保留专属路径；三篇都有本地可训练机制，公开构造任务不冒充真实广告漏斗。

1. [Entire Space Multi-Task Model: An Effective Approach for Estimating Post-Click Conversion Rate](../../../reproductions/1804.07931-esmm/README.md) · [原论文](https://arxiv.org/abs/1804.07931)
2. [Modeling Task Relationships in Multi-task Learning with Multi-gate Mixture-of-Experts](../../../reproductions/kdd2018-mmoe-mmoe/README.md) · [原论文](https://research.google/pubs/modeling-task-relationships-in-multi-task-learning-with-multi-gate-mixture-of-experts/)
3. [Progressive Layered Extraction (PLE): A Novel Multi-Task Learning Model for Personalized Recommendations](../../../reproductions/recsys2020-ple-ple/README.md) · [原论文](https://doi.org/10.1145/3383313.3412236)

## 自测一下

点击率从10%涨到20%，点击后转化率仍为20%，联合转化率变成4%。这证明CVR模型变好或策略有因果增量了吗？

??? note "展开参考答案"

    两者都不能直接证明。联合转化率随CTR上升即可翻倍，条件CVR未变；因果增量还需可信对照或额外识别假设。

## 这个子主题的论文卡片

导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">
<div class="ar-learning-controls">
<label for="learning-search">搜索卡片
<input id="learning-search" type="search" data-learning-search placeholder="搜索论文、机制、机构或本地边界"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">共 35 张卡片</p>
<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Hierarchical GTV Estimation: Bridging the Gap between Container-Level Ranking and Item-Level Conversion 搜广推与 LLM 应用 Meituan 2026-10-23 搜索广告排序的是门店、直播间等“容器”，成交却发生在内部商品上。单条成交金额既稀疏又高方差，简单把门店当成一个商品，容易忽略低价高频与高价低频商品的组合。HGE 先用 Hybrid Set-Aware Encoder 编码 top-K 商品的竞争关系，再在自注意力之后拼入用户、门店、上下文与查询。Proxy-Label Learning 分开预测门店是否成交、成交后每个商品的购买概率和数量； 论文私有日志训练和线上实验成本过高，不复现（审查 DONE）；实现范围为 HSAE、PLL、RCEF 的可微 L1 组件，不是完整广告模型。论文私有日志训练和线上实验成本过高，不复现（审查 DONE）；不据此宣称本地获得线上收益或接入 Evolve。HierarchicalGTV 接受外部商品 embedding、位置向量、上下文、价格和通用回归输出，不收答案/成交标签。以小尺寸可微模块验证：独立逐商品 Eq.5 参考、上下文不影响前置 MHSA、位置/价格/残差移除负控、融合两端点、商品概率之和可大于1、所有参数和输入的有限非零梯度。种子为42/43/44；指标只是合成机制误差和梯度，不是推荐准确率、收入或校准效果。  广告价值预估 层次化多任务学习 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-hge-0554c3a1">Hierarchical GTV Estimation: Bridging the Gap between Container-Level Ranking and Item-Level Conversion</h2>
<p class="ar-learning-card__meta">Meituan · 论文公开：2026-10-23</p>
<p><strong>方法要点：</strong>搜索广告排序的是门店、直播间等“容器”，成交却发生在内部商品上。单条成交金额既稀疏又高方差，简单把门店当成一个商品，容易忽略低价高频与高价低频商品的组合。HGE 先用 Hybrid Set-Aware Encoder 编码 top-K 商品的竞争关系，再在自注意力之后拼入用户、门店、上下文与查询。Proxy-Label Learning 分开预测门店是否成交、成交后每个商品的购买概率和数量；</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>论文私有日志训练和线上实验成本过高，不复现（审查 DONE）；实现范围为 HSAE、PLL、RCEF 的可微 L1 组件，不是完整广告模型。论文私有日志训练和线上实验成本过高，不复现（审查 DONE）；不据此宣称本地获得线上收益或接入 Evolve。HierarchicalGTV 接受外部商品 embedding、位置向量、上下文、价格和通用回归输出，不收答案/成交标签。以小尺寸可微模块验证：独立逐商品 Eq.5 参考、上下文不影响前置 MHSA、位置/价格/残差移除负控、融合两端点、商品概率之和可大于1、所有参数和输入的有限非零梯度。种子为42/43/44；指标只是合成机制误差和梯度，不是推荐准确率、收入或校准效果。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32420v1">原论文</a> · <a href="../../../../recommendation-components/2610.32420-hge/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Baseline and Incremental: User, Item, and Request Debiasing in Instagram Feed Ranking 搜广推与 LLM 应用 Meta 2026-10-20 参与度预测同时包含用户习惯、商品受欢迎程度、当前候选池水平和候选自身的相对优势。直接去掉基线可能丢失有用的绝对水平。论文保留原始预测，同时对相对基线的非线性增量单独加权；这是评分配置变化，不是因果uplift估计。用户、商品基线来自历史特征，请求基线来自当前候选池。概率使用log-odds差，回归量使用同单位差；正向门和降权门的幅度不同，不能把乘预测值的正向门直接改符号用于降权，否则预测接近零时惩罚也消失。 完整私有日志、排名系统及线上消融成本过高，不复现（审查 DONE）。仅为L1机制诊断，不是线上收益复现；已实现评分算子，不新增或训练排名网络。仅为L1机制诊断，不是线上收益复现；完整私有日志、排名系统及线上消融成本过高，不复现（审查 DONE）。运行独立有理式参考、hinge与sigmoid区别、预测地板降权和移除增量项的排序负对照，seed42/43/44。输入为合成分数，不读取生产数据，不拟合或选择线上权重，不将数组排序改变解释为推荐提升。request_baseline只计算调用方指定的池内统计，不自行学会选择基线。  排序与决策优化 基线与增量去偏 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-baseline-incremental-a452c157">Baseline and Incremental: User, Item, and Request Debiasing in Instagram Feed Ranking</h2>
<p class="ar-learning-card__meta">Meta · 论文公开：2026-10-20</p>
<p><strong>方法要点：</strong>参与度预测同时包含用户习惯、商品受欢迎程度、当前候选池水平和候选自身的相对优势。直接去掉基线可能丢失有用的绝对水平。论文保留原始预测，同时对相对基线的非线性增量单独加权；这是评分配置变化，不是因果uplift估计。用户、商品基线来自历史特征，请求基线来自当前候选池。概率使用log-odds差，回归量使用同单位差；正向门和降权门的幅度不同，不能把乘预测值的正向门直接改符号用于降权，否则预测接近零时惩罚也消失。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整私有日志、排名系统及线上消融成本过高，不复现（审查 DONE）。仅为L1机制诊断，不是线上收益复现；已实现评分算子，不新增或训练排名网络。仅为L1机制诊断，不是线上收益复现；完整私有日志、排名系统及线上消融成本过高，不复现（审查 DONE）。运行独立有理式参考、hinge与sigmoid区别、预测地板降权和移除增量项的排序负对照，seed42/43/44。输入为合成分数，不读取生产数据，不拟合或选择线上权重，不将数组排序改变解释为推荐提升。request_baseline只计算调用方指定的池内统计，不自行学会选择基线。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.27423v1">原论文</a> · <a href="../../../../recommendation-components/2610.27423-baseline-incremental/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="CASI: Credit Assignment via Set Intervention for Agentic Retrieval 搜广推与 LLM 应用 Xiaohongshu 2026-10-14 一次检索请求可能联合产生多个改写动作，线上却只返回整个结果集合的奖励。CASI 不把这个奖励简单均分：每个动作只检索一次，冻结候选快照，再重组子集、评估候选之间的协同与替代关系，以 Shapley 边际贡献分配信用。随后用共享尺度归一化与有界零和投影，将集合信用转为 action/token 优势。集合奖励广播仍可给出原集合目标的有效 score-function 估计；CASI 的内部优势塑形不能额外宣称保持同一无偏梯度。论文也指出：加性集合无需额外干预； 完整的私有拍卖重放、LLM 五次训练及生产 A/B：成本过高，不复现（审查 DONE）。默认诊断后端按固定分数对每个子集重新取 top-2，属于显式的 pr_rerun 敏感性示例，不是论文的私有 pr_filter 训练后端；本地对照口径：基线为相同冻结集合函数上的 Singleton 和 LOO，实验组为精确/置换 Shapley 与零和优势组件；没有策略训练，相对能力提升不适用。  agentic-retrieval credit-assignment policy-optimization 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-casi-2c2b2f1b">CASI: Credit Assignment via Set Intervention for Agentic Retrieval</h2>
<p class="ar-learning-card__meta">Xiaohongshu · 论文公开：2026-10-14</p>
<p><strong>方法要点：</strong>一次检索请求可能联合产生多个改写动作，线上却只返回整个结果集合的奖励。CASI 不把这个奖励简单均分：每个动作只检索一次，冻结候选快照，再重组子集、评估候选之间的协同与替代关系，以 Shapley 边际贡献分配信用。随后用共享尺度归一化与有界零和投影，将集合信用转为 action/token 优势。集合奖励广播仍可给出原集合目标的有效 score-function 估计；CASI 的内部优势塑形不能额外宣称保持同一无偏梯度。论文也指出：加性集合无需额外干预；</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整的私有拍卖重放、LLM 五次训练及生产 A/B：成本过高，不复现（审查 DONE）。默认诊断后端按固定分数对每个子集重新取 top-2，属于显式的 pr_rerun 敏感性示例，不是论文的私有 pr_filter 训练后端；本地对照口径：基线为相同冻结集合函数上的 Singleton 和 LOO，实验组为精确/置换 Shapley 与零和优势组件；没有策略训练，相对能力提升不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20293">原论文</a> · <a href="../../../../reproductions/2610.20293-casi/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Measuring and Mitigating Identity-Cue Preference Drift in LLM-based Recommender Systems 搜广推与 LLM 应用 University of Electronic Science and Technology of China 2026-09-28 在行为历史不变时比较身份提示与无身份参考列表，用 Drift 与 SliceShift 量化身份线索偏移，再依据用户主流度自适应混合原分与逆群体流行度。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行列表指标与后处理 reranker；身份 slice 和相关性由公开 fixture 给出，不生成真实用户画像。执行列表指标与后处理 reranker；身份 slice 和相关性由公开 fixture 给出，不生成真实用户画像。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  llm-recommendation identity-cue-drift fairness 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-promptshift-7e539145">Measuring and Mitigating Identity-Cue Preference Drift in LLM-based Recommender Systems</h2>
<p class="ar-learning-card__meta">University of Electronic Science and Technology of China · 论文公开：2026-09-28</p>
<p><strong>方法要点：</strong>在行为历史不变时比较身份提示与无身份参考列表，用 Drift 与 SliceShift 量化身份线索偏移，再依据用户主流度自适应混合原分与逆群体流行度。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行列表指标与后处理 reranker；身份 slice 和相关性由公开 fixture 给出，不生成真实用户画像。执行列表指标与后处理 reranker；身份 slice 和相关性由公开 fixture 给出，不生成真实用户画像。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34229">原论文</a> · <a href="../../../../reproductions/2609.34229-promptshift/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Mend the Measurement Gap: Latent User Preference Modeling for Short-Form Video Recommendation 搜广推与 LLM 应用 Google / YouTube 2026-09-26 短视频的观看时长会被视频长度、用户习惯和时段影响，同样的观看行为不一定代表喜欢。Google/YouTube 的 FLVM 不直接把各种行为当成单一偏好分数，而是用三维潜变量分别表示消费、主动参与、参与方向（正负）。时长等测量混杂因素只进入受限基线；完整的用户—视频信息进入潜变量编码器。每个反馈头只读取与其语义相符的因子，然后在 logit 空间叠加到停止梯度的基线上。 复现级别：公开数据概念验证。复现级别：公开数据概念验证。本地执行了三因子高斯潜变量、受限基线、稀疏路由、停止梯度与 KL 损失；没有 YouTube 的满意度调查、生产特征和线上实验，不能据此声称复现 +2.67% 收益。本地对照口径：实验组为 FLVM 缩比结构；基线为独立初始化和训练、读取相同曝光前特征、使用相同四种反馈与更新步数的共享塔多任务模型。两者不是 YouTube 生产模型，相对论文线上收益不适用。  ranking multi-task feedback-debiasing 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-flvm-33286ec7">Mend the Measurement Gap: Latent User Preference Modeling for Short-Form Video Recommendation</h2>
<p class="ar-learning-card__meta">Google / YouTube · 论文公开：2026-09-26</p>
<p><strong>方法要点：</strong>短视频的观看时长会被视频长度、用户习惯和时段影响，同样的观看行为不一定代表喜欢。Google/YouTube 的 FLVM 不直接把各种行为当成单一偏好分数，而是用三维潜变量分别表示消费、主动参与、参与方向（正负）。时长等测量混杂因素只进入受限基线；完整的用户—视频信息进入潜变量编码器。每个反馈头只读取与其语义相符的因子，然后在 logit 空间叠加到停止梯度的基线上。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：公开数据概念验证。复现级别：公开数据概念验证。本地执行了三因子高斯潜变量、受限基线、稀疏路由、停止梯度与 KL 损失；没有 YouTube 的满意度调查、生产特征和线上实验，不能据此声称复现 +2.67% 收益。本地对照口径：实验组为 FLVM 缩比结构；基线为独立初始化和训练、读取相同曝光前特征、使用相同四种反馈与更新步数的共享塔多任务模型。两者不是 YouTube 生产模型，相对论文线上收益不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.32839">原论文</a> · <a href="../../../../reproductions/2609.32839-flvm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Learned Cross-Task Relationships in Multi-Task Models 搜广推与 LLM 应用 Google 2026-09-23 多任务网络只预测各反馈的边际概率，可能丢掉任务之间的联合信息。该方法加入成对联合标签或缺失的无条件辅助头，既给共享表示提供额外梯度，也能把联合预测作为下游策略的新输入；论文将这两种收益分阶段隔离测试。 成本过高，不复现（审查 DONE）：原文每日数十亿样本、多周训练与线上实验不在单卡预算内；小切片稀疏且有前缀选择偏差，三种子仍只是诊断，不是稳定能力提升。使用官方 KuaiRand-Pure 固定 4,096 行曝光前缀，时间排序后按 70/15/15 划分 train/validation/test。特征仅含曝光前的用户/视频 ID、时段和视频时长；is_click / long_view 只进入损失与评分。训练集检查四种联合标签均存在，排除互斥、嵌套、常量或当前切片无法支持的任务对。  多目标与多任务学习 联合标签与辅助头 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-cross-task-relationships-c0c2f1d1">Learned Cross-Task Relationships in Multi-Task Models</h2>
<p class="ar-learning-card__meta">Google · 论文公开：2026-09-23</p>
<p><strong>方法要点：</strong>多任务网络只预测各反馈的边际概率，可能丢掉任务之间的联合信息。该方法加入成对联合标签或缺失的无条件辅助头，既给共享表示提供额外梯度，也能把联合预测作为下游策略的新输入；论文将这两种收益分阶段隔离测试。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）：原文每日数十亿样本、多周训练与线上实验不在单卡预算内；小切片稀疏且有前缀选择偏差，三种子仍只是诊断，不是稳定能力提升。使用官方 KuaiRand-Pure 固定 4,096 行曝光前缀，时间排序后按 70/15/15 划分 train/validation/test。特征仅含曝光前的用户/视频 ID、时段和视频时长；is_click / long_view 只进入损失与评分。训练集检查四种联合标签均存在，排除互斥、嵌套、常量或当前切片无法支持的任务对。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.28776">原论文</a> · <a href="../../../../recommendation-components/2609.28776-cross-task-relationships/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Lightweight Ranking Heads: Accelerating Multi-Task Experimentation in Production Recommender Systems 搜广推与 LLM 应用 Google 2026-09-21 工业多任务 ranker 要添加新目标时，直接改动共享塔可能导致旧目标负迁移，还会让并行实验模型与下游模型输出空间不一致。论文把新增目标声明为中央配置，训练时在共享表示上动态挂一个浅头；轻头输入执行 stop_gradient，因此新目标不会回传到共享塔。每个持续训练窗口可以重置轻头参数，使不同上游模型的轻头训练年龄可比较。论文也报告了“不重置”和“去掉 stop-gradient”的消融，前者可能给数据稀疏的目标更好的拟合，后者可能损伤原任务。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地确实执行了动态注入、stop-gradient、训练窗口重置以及两个对应消融；没有 Google 私有流量、持续训练平台或线上下游模型。公开数据结果与论文线上结果严格分开。执行了论文定义性的“共享塔 + 动态轻头 + 梯度隔离 + 可选重置”；不是同名的后处理打分函数。本地对照口径：同预算不重置轻头为新任务基线，test AUC 0.6267；标准重置实验组 0.5109，相对 -18.48%。这是公开数据短训练窗口的负结果。  ranking multi-task-learning lightweight-heads 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-light-heads-bf390928">Lightweight Ranking Heads: Accelerating Multi-Task Experimentation in Production Recommender Systems</h2>
<p class="ar-learning-card__meta">Google · 论文公开：2026-09-21</p>
<p><strong>方法要点：</strong>工业多任务 ranker 要添加新目标时，直接改动共享塔可能导致旧目标负迁移，还会让并行实验模型与下游模型输出空间不一致。论文把新增目标声明为中央配置，训练时在共享表示上动态挂一个浅头；轻头输入执行 stop_gradient，因此新目标不会回传到共享塔。每个持续训练窗口可以重置轻头参数，使不同上游模型的轻头训练年龄可比较。论文也报告了“不重置”和“去掉 stop-gradient”的消融，前者可能给数据稀疏的目标更好的拟合，后者可能损伤原任务。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地确实执行了动态注入、stop-gradient、训练窗口重置以及两个对应消融；没有 Google 私有流量、持续训练平台或线上下游模型。公开数据结果与论文线上结果严格分开。执行了论文定义性的“共享塔 + 动态轻头 + 梯度隔离 + 可选重置”；不是同名的后处理打分函数。本地对照口径：同预算不重置轻头为新任务基线，test AUC 0.6267；标准重置实验组 0.5109，相对 -18.48%。这是公开数据短训练窗口的负结果。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.25433">原论文</a> · <a href="../../../../reproductions/2609.25433-light-heads/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="BAFF: Bid-Aware Filter Family for Mitigating Training Data Interference in RTB A/B Tests 搜广推与 LLM 应用 Dable 2026-09-08 RTB 实验中 A/B 两个策略看到的竞价机会会互相影响；直接混用日志训练 B 模型会引入 treatment interference。BAFF 同时检查 A 广告在 B 排序中的位置差和 bid-price 差，只保留对 B 决策近似无干扰的 A 日志。 复现级别：受控仿真核心机制。复现级别：受控仿真核心机制。精确执行论文过滤判据，以 B-only 训练作参照测量共享日志参数偏差；不把仿真结果称为线上提升。2,400 次受控拍卖、三种子结果见 metrics/controlled-rtb-seeds42-44.json。仿真真实执行严格双轴过滤及 ridge 参数偏差诊断，但没有 Dable 私有 DSP 日志、生产 CTR 模型或市场侧 reference 实验。  advertising rtb ab-testing training-data-interference 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-baff-e8ac8fd9">BAFF: Bid-Aware Filter Family for Mitigating Training Data Interference in RTB A/B Tests</h2>
<p class="ar-learning-card__meta">Dable · 论文公开：2026-09-08</p>
<p><strong>方法要点：</strong>RTB 实验中 A/B 两个策略看到的竞价机会会互相影响；直接混用日志训练 B 模型会引入 treatment interference。BAFF 同时检查 A 广告在 B 排序中的位置差和 bid-price 差，只保留对 B 决策近似无干扰的 A 日志。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：受控仿真核心机制。复现级别：受控仿真核心机制。精确执行论文过滤判据，以 B-only 训练作参照测量共享日志参数偏差；不把仿真结果称为线上提升。2,400 次受控拍卖、三种子结果见 metrics/controlled-rtb-seeds42-44.json。仿真真实执行严格双轴过滤及 ridge 参数偏差诊断，但没有 Dable 私有 DSP 日志、生产 CTR 模型或市场侧 reference 实验。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08725">原论文</a> · <a href="../../../../reproductions/2609.08725-baff/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="DCEO: Direct Causal Effect Optimization for Long-Term User Value Modeling in E-commerce Search 搜广推与 LLM 应用 Taobao &amp; Tmall Group, Alibaba 2026-08-26 固定加权的点击、转化和 GMV 目标不能随用户状态改变，也无法直接刻画一次排序动作的长期因果价值。DCEO 用 actor 输出上下文相关 simplex 权重，用用户级 critic 估计相对干预效果；线上只保留轻量 actor。 本地负相关诊断明确阻止把 Hit 改善解读为长期价值提升。Fidelity：核心机制复现。本地执行上下文条件目标权重、用户级 proxy 聚合和相对因果干预；生产 critic 与在线 actor serving 未复刻。proxy outcome 与真实长期 GMV 不等价；本地负相关诊断明确阻止把 Hit 改善解读为长期价值提升。本地实现现在把 causal_gain × temperature 纳入 evolve 搜索空间：20 个候选只在 validation 上按 NDCG@10 + 0.15 × Hit@10 选择，随后仅对冠军运行一次 held-out test。  search-ranking long-term-value causal-optimization multi-objective-ranking 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-dceo-b39ed1b8">DCEO: Direct Causal Effect Optimization for Long-Term User Value Modeling in E-commerce Search</h2>
<p class="ar-learning-card__meta">Taobao &amp; Tmall Group, Alibaba · 论文公开：2026-08-26</p>
<p><strong>方法要点：</strong>固定加权的点击、转化和 GMV 目标不能随用户状态改变，也无法直接刻画一次排序动作的长期因果价值。DCEO 用 actor 输出上下文相关 simplex 权重，用用户级 critic 估计相对干预效果；线上只保留轻量 actor。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本地负相关诊断明确阻止把 Hit 改善解读为长期价值提升。Fidelity：核心机制复现。本地执行上下文条件目标权重、用户级 proxy 聚合和相对因果干预；生产 critic 与在线 actor serving 未复刻。proxy outcome 与真实长期 GMV 不等价；本地负相关诊断明确阻止把 Hit 改善解读为长期价值提升。本地实现现在把 causal_gain × temperature 纳入 evolve 搜索空间：20 个候选只在 validation 上按 NDCG@10 + 0.15 × Hit@10 选择，随后仅对冠军运行一次 held-out test。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25635">原论文</a> · <a href="../../../../reproductions/2608.25635-dceo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="From Prediction to Incrementality: Causal Optimization for Large-Scale Targeting and Recommendation 搜广推与 LLM 应用 LinkedIn 2026-08-10 分别估计处理与不处理时的潜在结果，以 uplift 及其不确定度代替点击概率排序，再在固定触达预算下完成因果分配。这样优化的是动作带来的增量价值，而不是本来就会发生的结果。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线按 treated outcome 排序，实验组按 uplift 与不确定度分配；同为 30% 预算，seed 42 的 policy value 为 0.10408，基线为 0.09537。  causal-recommendation uplift bandit constrained-allocation 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-incrementality-26b16fde">From Prediction to Incrementality: Causal Optimization for Large-Scale Targeting and Recommendation</h2>
<p class="ar-learning-card__meta">LinkedIn · 论文公开：2026-08-10</p>
<p><strong>方法要点：</strong>分别估计处理与不处理时的潜在结果，以 uplift 及其不确定度代替点击概率排序，再在固定触达预算下完成因果分配。这样优化的是动作带来的增量价值，而不是本来就会发生的结果。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线按 treated outcome 排序，实验组按 uplift 与不确定度分配；同为 30% 预算，seed 42 的 policy value 为 0.10408，基线为 0.09537。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.10182">原论文</a> · <a href="../../../../reproductions/2608.10182-incrementality/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Multi-Objective Ranking for Live-Streaming: Balancing Fresh and Delayed Signals with Segment-Aware Targeting 搜广推与 LLM 应用 Twitch 2026-08-05 主题：直播多目标排序。直播观看、互动、关注和付费的反馈延迟不同，且生命周期分群差异明显。论文组合即时/延迟模型、分群目标权重与 MMoE，在共享专家的同时保留目标专属 gate。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。MovieLens-1M 构造五个即时/延迟目标，比较单目标 DNN 与三专家生命周期 MMoE。  ranking multi-task-learning mmoe live-streaming 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-twitch-mor-68bc3da8">Multi-Objective Ranking for Live-Streaming: Balancing Fresh and Delayed Signals with Segment-Aware Targeting</h2>
<p class="ar-learning-card__meta">Twitch · 论文公开：2026-08-05</p>
<p><strong>方法要点：</strong>主题：直播多目标排序。直播观看、互动、关注和付费的反馈延迟不同，且生命周期分群差异明显。论文组合即时/延迟模型、分群目标权重与 MMoE，在共享专家的同时保留目标专属 gate。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。MovieLens-1M 构造五个即时/延迟目标，比较单目标 DNN 与三专家生命周期 MMoE。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04455">原论文</a> · <a href="../../../../reproductions/2608.04455-twitch-mor/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="LLM-Derived Priors for Thompson Sampling in Cold-Start Comment Recommendation 搜广推与 LLM 应用 NAVER WEBTOON 2026-08-04 主题：LLM 语义先验与冷启动 bandit。新评论缺少交互反馈，但文本已含性别/内容偏好线索。论文把 LLM 语义判断转为 Beta 伪计数，并按性别年龄分群维护 Thompson posterior。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。以 MovieLens genre 代理文本语义，运行分群 Beta prior 与 40 轮 Thompson 在线更新；明确保留负向及不显著结果。  llm-recommendation bandit cold-start comment-ranking 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-llm-ts-prior-97482120">LLM-Derived Priors for Thompson Sampling in Cold-Start Comment Recommendation</h2>
<p class="ar-learning-card__meta">NAVER WEBTOON · 论文公开：2026-08-04</p>
<p><strong>方法要点：</strong>主题：LLM 语义先验与冷启动 bandit。新评论缺少交互反馈，但文本已含性别/内容偏好线索。论文把 LLM 语义判断转为 Beta 伪计数，并按性别年龄分群维护 Thompson posterior。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。以 MovieLens genre 代理文本语义，运行分群 Beta prior 与 40 轮 Thompson 在线更新；明确保留负向及不显著结果。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03382">原论文</a> · <a href="../../../../reproductions/2608.03382-llm-ts-prior/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="TWICE: Two-Clock, Two-Window Learning for Long-Horizon Conversion Prediction in Online Advertising 搜广推与 LLM 应用 Kuaishou 2026-07-28 把点击时钟的 current-status 标签与转化时钟的 delay CDF 分开学习，再用曝光窗口权重校正长期未成熟标签。 Fidelity: 核心机制复现。本地执行双时钟、双窗口校正路径和统一评测，私有工业特征与服务未复刻。公开交互代理广告延迟，未包含生产聚合记录和真实 revenue；线上数字只引用论文。本地对照口径：基线为 mature-label next-item CVR，实验组为双时钟 current-status；Hit@10 +8.00%、NDCG@10 +14.31%。  advertising cvr delayed-feedback full-traffic 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-twice-bd9f2dd2">TWICE: Two-Clock, Two-Window Learning for Long-Horizon Conversion Prediction in Online Advertising</h2>
<p class="ar-learning-card__meta">Kuaishou · 论文公开：2026-07-28</p>
<p><strong>方法要点：</strong>把点击时钟的 current-status 标签与转化时钟的 delay CDF 分开学习，再用曝光窗口权重校正长期未成熟标签。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地执行双时钟、双窗口校正路径和统一评测，私有工业特征与服务未复刻。公开交互代理广告延迟，未包含生产聚合记录和真实 revenue；线上数字只引用论文。本地对照口径：基线为 mature-label next-item CVR，实验组为双时钟 current-status；Hit@10 +8.00%、NDCG@10 +14.31%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25404">原论文</a> · <a href="../../../../reproductions/2607.25404-twice/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="PinEqualizer: Full Funnel Content Exploration and Debiasing System at Pinterest 搜广推与 LLM 应用 Pinterest 2026-07-23 新内容缺少协同图和历史互动，生产模型又会依赖已有曝光形成反馈回路。PinEqualizer 不把问题限制在一个排序模型，而是在 corpus selection、召回、精排和 utility 每一级检查 fresh 内容的输入占比与存活率。模型侧加入纯内容/VLM/SID 特征、逐 engagement 特征 dropout、内容—年龄—互动显式交叉、分内容类型 calibration 和 fresh/old 分数正则； Fidelity: 核心机制复现。真实执行 engagement dropout、内容交叉、分 cohort calibration、探索 corpus 与 relevance-scaled UCB；私有多阶段系统由公开代理缩小。MovieLens 的物品首见时间只是新内容代理：fresh 定义为首见时间最新 20%，underexplored 再限制为低于 fresh popularity 中位数。实现没有 Pinterest 的 PinCLIP、SID、商家数据、三大 surface、长期内容 holdout 和实时 Flink 特征；  cold-start exploration debiasing ranking retrieval 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-pinequalizer-1595745d">PinEqualizer: Full Funnel Content Exploration and Debiasing System at Pinterest</h2>
<p class="ar-learning-card__meta">Pinterest · 论文公开：2026-07-23</p>
<p><strong>方法要点：</strong>新内容缺少协同图和历史互动，生产模型又会依赖已有曝光形成反馈回路。PinEqualizer 不把问题限制在一个排序模型，而是在 corpus selection、召回、精排和 utility 每一级检查 fresh 内容的输入占比与存活率。模型侧加入纯内容/VLM/SID 特征、逐 engagement 特征 dropout、内容—年龄—互动显式交叉、分内容类型 calibration 和 fresh/old 分数正则；</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。真实执行 engagement dropout、内容交叉、分 cohort calibration、探索 corpus 与 relevance-scaled UCB；私有多阶段系统由公开代理缩小。MovieLens 的物品首见时间只是新内容代理：fresh 定义为首见时间最新 20%，underexplored 再限制为低于 fresh popularity 中位数。实现没有 Pinterest 的 PinCLIP、SID、商家数据、三大 surface、长期内容 holdout 和实时 Flink 特征；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.22518">原论文</a> · <a href="../../../../reproductions/2607.22518-pinequalizer/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="RAMP: Robust Ad Recommendation Under Limited Personalized-Feature Availability via Masking and Alignment Pathways 搜广推与 LLM 应用 Huawei Ireland Research Center / University College Dublin 2026-07-20 隐私选择、权限或平台限制会让同一广告模型在部分流量上拿不到个性化字段。RAMP 不把缺失值简单填零，而是显式维护 personalized 与 non-personalized 两条路径，用可用性 mask 控制输出，并通过 prediction alignment 把富特征路径的知识蒸馏给受限路径。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练 masked 双路径与 prediction alignment；私有工业 CVR 数据未复刻。MovieLens 行为向量代理受限个性化字段、类型特征代理公共广告字段；训练中实际执行双路径、输出 masking 和富特征 teacher 到受限路径的 KL 对齐，测试专门评估无个性化字段流量。  advertising privacy distillation missing-features 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-ramp-9687450e">RAMP: Robust Ad Recommendation Under Limited Personalized-Feature Availability via Masking and Alignment Pathways</h2>
<p class="ar-learning-card__meta">Huawei Ireland Research Center / University College Dublin · 论文公开：2026-07-20</p>
<p><strong>方法要点：</strong>隐私选择、权限或平台限制会让同一广告模型在部分流量上拿不到个性化字段。RAMP 不把缺失值简单填零，而是显式维护 personalized 与 non-personalized 两条路径，用可用性 mask 控制输出，并通过 prediction alignment 把富特征路径的知识蒸馏给受限路径。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练 masked 双路径与 prediction alignment；私有工业 CVR 数据未复刻。MovieLens 行为向量代理受限个性化字段、类型特征代理公共广告字段；训练中实际执行双路径、输出 masking 和富特征 teacher 到受限路径的 KL 对齐，测试专门评估无个性化字段流量。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.17473">原论文</a> · <a href="../../../../reproductions/2607.17473-ramp/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Deep-learning Causal Retrieval Optimization for Efficient e-commerce Distribution in Pinterest 搜广推与 LLM 应用 Pinterest 2026-07-14 始终触发 shopping candidate generator 浪费资源，也会向无购物意图用户过度分发。论文用随机日志学习多事件 outcome 和 doubly-robust uplift，离线线性 replay 选阈值，线上与远程召回并行执行。 Fidelity: 核心机制复现。执行 propensity、双 outcome、DR pseudo-outcome 和触发阈值。没有 Pinterest randomized logs、购物 session 或 RPC 成本；本地 pseudo-treatment 仅用于可辨识的机制实验。本地对照口径：基线是固定的非因果 transition/content/popularity retrieval ensemble；实验组以 DR uplift 选择约 30% shopping trigger，NDCG@10 0.03540→0.06399，相对 +80.77%。  causal-retrieval uplift candidate-generation 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-causal-retrieval-c13802af">Deep-learning Causal Retrieval Optimization for Efficient e-commerce Distribution in Pinterest</h2>
<p class="ar-learning-card__meta">Pinterest · 论文公开：2026-07-14</p>
<p><strong>方法要点：</strong>始终触发 shopping candidate generator 浪费资源，也会向无购物意图用户过度分发。论文用随机日志学习多事件 outcome 和 doubly-robust uplift，离线线性 replay 选阈值，线上与远程召回并行执行。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。执行 propensity、双 outcome、DR pseudo-outcome 和触发阈值。没有 Pinterest randomized logs、购物 session 或 RPC 成本；本地 pseudo-treatment 仅用于可辨识的机制实验。本地对照口径：基线是固定的非因果 transition/content/popularity retrieval ensemble；实验组以 DR uplift 选择约 30% shopping trigger，NDCG@10 0.03540→0.06399，相对 +80.77%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14161">原论文</a> · <a href="../../../../reproductions/2607.14161-causal-retrieval/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Cheaper is Better: A Discount-Aware Network for Conversion Rate Prediction in E-commerce Recommendation System 搜广推与 LLM 应用 Alibaba Group / Tmall 2026-07-14 只建模兴趣无法解释“便宜多少”对购买的影响。DANet 的 IPN 捕获一般兴趣；DPN 对 400 天 discount-rate 序列做 FFT 滤波和高低频分解，DCM-User 从相似购买中抽取折扣偏好，DCM-Context 用促销周期 gate 修正分布，并以购买样本的真实折扣做辅助回归。 Fidelity: 核心机制复现。参照作者开源代码执行 IPN、FFT/IFFT、DCM-User、DCM-Context 与折扣回归辅助任务。未使用 Tmall 私有 400 天折扣和促销特征；明确区分作者 TensorFlow 代码与本地 NumPy 复现。本地对照口径：基线是 IPN interest score；实验组 DANet 加入折扣代理的 TFTM/DCM，Hit@10 +0.00%、NDCG@10 -1.46%，fresh Hit@10 +50.00%。  ranking cvr discount 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-danet-112ada17">Cheaper is Better: A Discount-Aware Network for Conversion Rate Prediction in E-commerce Recommendation System</h2>
<p class="ar-learning-card__meta">Alibaba Group / Tmall · 论文公开：2026-07-14</p>
<p><strong>方法要点：</strong>只建模兴趣无法解释“便宜多少”对购买的影响。DANet 的 IPN 捕获一般兴趣；DPN 对 400 天 discount-rate 序列做 FFT 滤波和高低频分解，DCM-User 从相似购买中抽取折扣偏好，DCM-Context 用促销周期 gate 修正分布，并以购买样本的真实折扣做辅助回归。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。参照作者开源代码执行 IPN、FFT/IFFT、DCM-User、DCM-Context 与折扣回归辅助任务。未使用 Tmall 私有 400 天折扣和促销特征；明确区分作者 TensorFlow 代码与本地 NumPy 复现。本地对照口径：基线是 IPN interest score；实验组 DANet 加入折扣代理的 TFTM/DCM，Hit@10 +0.00%、NDCG@10 -1.46%，fresh Hit@10 +50.00%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12578">原论文</a> · <a href="../../../../reproductions/2607.12578-danet/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Synthetic Data from Cross-Domain Events for Large-Scale Recommendation Systems 搜广推与 LLM 应用 Meta 2026-05-29 目标域 conversion 极稀疏，而同一用户在其他产品 surface 上有丰富行为。传统 cross-domain recommendation 把迁移逻辑耦合进模型参数；SCALR 先把 source event 翻译成目标域格式的 synthetic user-item event，再让任何下游模型像读取普通目标域数据一样训练。随机采样保留概率分布和 catalog 多样性，避免 top-k 反复生成少数头部 item。 Fidelity: 核心机制复现。本地从重叠用户估计跨域 item translation distribution，真实生成随机采样与 deterministic top-k 两套 synthetic events，再用相同下游协议比较。本地 genre 不是 Meta 的跨产品 surface，也没有 conversion label、隐私管线或多源生产生成服务。结果只验证概率翻译、随机生成和分布覆盖机制，不能外推论文线上 CVR。本地对照口径：基线为相同 source events、相同每事件生成预算的 deterministic top-k translation，实验组改为 SCALR 概率采样；  cross-domain synthetic-data sampling conversion data-augmentation 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-scalr-f567c58a">Synthetic Data from Cross-Domain Events for Large-Scale Recommendation Systems</h2>
<p class="ar-learning-card__meta">Meta · 论文公开：2026-05-29</p>
<p><strong>方法要点：</strong>目标域 conversion 极稀疏，而同一用户在其他产品 surface 上有丰富行为。传统 cross-domain recommendation 把迁移逻辑耦合进模型参数；SCALR 先把 source event 翻译成目标域格式的 synthetic user-item event，再让任何下游模型像读取普通目标域数据一样训练。随机采样保留概率分布和 catalog 多样性，避免 top-k 反复生成少数头部 item。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地从重叠用户估计跨域 item translation distribution，真实生成随机采样与 deterministic top-k 两套 synthetic events，再用相同下游协议比较。本地 genre 不是 Meta 的跨产品 surface，也没有 conversion label、隐私管线或多源生产生成服务。结果只验证概率翻译、随机生成和分布覆盖机制，不能外推论文线上 CVR。本地对照口径：基线为相同 source events、相同每事件生成预算的 deterministic top-k translation，实验组改为 SCALR 概率采样；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.00282">原论文</a> · <a href="../../../../reproductions/2606.00282-scalr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Causal Representation Learning for Generalisable Recommendation 搜广推与 LLM 应用 University of Warwick 2026-05-26 通过信息论去混杂约束，让候选表征保留与结果有关的因果成分、丢弃由曝光策略带来的非因果成分；训练后不增加线上推理开销。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05220，相对变化 -3.35%。本地代理目标与论文生产任务不同，不能外推线上 lift。  causal-recommendation distribution-shift representation-learning 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-causal-representation-dd23e0e4">Causal Representation Learning for Generalisable Recommendation</h2>
<p class="ar-learning-card__meta">University of Warwick · 论文公开：2026-05-26</p>
<p><strong>方法要点：</strong>通过信息论去混杂约束，让候选表征保留与结果有关的因果成分、丢弃由曝光策略带来的非因果成分；训练后不增加线上推理开销。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05220，相对变化 -3.35%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.27043">原论文</a> · <a href="../../../../reproductions/2605.27043-causal-representation/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="PEARL: Unbiased Percentile Estimation via Contrastive Learning for Industrial-Scale Livestream Recommendation 搜广推与 LLM 应用 TikTok 2026-05-20 用多次对比而不是单个偏置标签估计行为 percentile，并按价值加权、bootstrap 和长期共训练扩展到多个排序目标。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  ranking contrastive-learning debiasing 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-pearl-percentile-dbf6d244">PEARL: Unbiased Percentile Estimation via Contrastive Learning for Industrial-Scale Livestream Recommendation</h2>
<p class="ar-learning-card__meta">TikTok · 论文公开：2026-05-20</p>
<p><strong>方法要点：</strong>用多次对比而不是单个偏置标签估计行为 percentile，并按价值加权、bootstrap 和长期共训练扩展到多个排序目标。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.21752">原论文</a> · <a href="../../../../reproductions/2605.21752-pearl-percentile/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="DADF: A Distribution-Aware Debiasing Framework for Watch-Time Regression in Recommender Systems 搜广推与 LLM 应用 Kuaishou Technology 2026-05-18 冻结成熟的第一阶段 watch-time 模型，按条件分布学习乘性残差校正，并保持线上标量接口不变。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  ranking watch-time debiasing 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-dadf-696311de">DADF: A Distribution-Aware Debiasing Framework for Watch-Time Regression in Recommender Systems</h2>
<p class="ar-learning-card__meta">Kuaishou Technology · 论文公开：2026-05-18</p>
<p><strong>方法要点：</strong>冻结成熟的第一阶段 watch-time 模型，按条件分布学习乘性残差校正，并保持线上标量接口不变。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.17863">原论文</a> · <a href="../../../../reproductions/2605.17863-dadf/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Effective Knowledge Transfer for Multi-Task Recommendation Models 搜广推与 LLM 应用 Huawei Technologies 2026-05-07 让 CTR 表示按 CVR 任务相似度向多个转化塔迁移，并以难例感知损失抑制负迁移，保持多任务部署成本可控。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 ektm 核心机制，相对 NDCG@10 +10.98%。  multi-task-learning knowledge-transfer conversion 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-ektm-e47d7330">Effective Knowledge Transfer for Multi-Task Recommendation Models</h2>
<p class="ar-learning-card__meta">Huawei Technologies · 论文公开：2026-05-07</p>
<p><strong>方法要点：</strong>让 CTR 表示按 CVR 任务相似度向多个转化塔迁移，并以难例感知损失抑制负迁移，保持多任务部署成本可控。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 ektm 核心机制，相对 NDCG@10 +10.98%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.05730">原论文</a> · <a href="../../../../reproductions/2605.05730-ektm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Bridging Passive and Active: Enhancing Conversation Starter Recommendation via Active Expression Modeling 搜广推与 LLM 应用 ByteDance 2026-05-07 用分布对齐器把被动浏览行为迁移到主动查询空间，再通过语义离散化和重加权削弱曝光反馈回路，改善 conversation starter 的覆盖与多样性。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04938，相对变化 -8.57%。本地代理目标与论文生产任务不同，不能外推线上 lift。  conversation-starter distribution-alignment debiasing 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-pa-bridge-6df7bc67">Bridging Passive and Active: Enhancing Conversation Starter Recommendation via Active Expression Modeling</h2>
<p class="ar-learning-card__meta">ByteDance · 论文公开：2026-05-07</p>
<p><strong>方法要点：</strong>用分布对齐器把被动浏览行为迁移到主动查询空间，再通过语义离散化和重加权削弱曝光反馈回路，改善 conversation starter 的覆盖与多样性。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04938，相对变化 -8.57%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.05855">原论文</a> · <a href="../../../../reproductions/2605.05855-pa-bridge/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Generative Pseudo-Labeling for Pre-Ranking with LLMs 搜广推与 LLM 应用 Alibaba Group / Renmin University 2026-02-24 LLM 从用户行为生成兴趣锚点，为未曝光召回候选产生伪标签；预排序器联合真实与伪监督，且线上不调用 LLM。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 gpl-prerank 核心机制，相对 NDCG@10 +12.84%。  pre-ranking pseudo-labeling llm-recommendation 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-gpl-prerank-737de503">Generative Pseudo-Labeling for Pre-Ranking with LLMs</h2>
<p class="ar-learning-card__meta">Alibaba Group / Renmin University · 论文公开：2026-02-24</p>
<p><strong>方法要点：</strong>LLM 从用户行为生成兴趣锚点，为未曝光召回候选产生伪标签；预排序器联合真实与伪监督，且线上不调用 LLM。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 gpl-prerank 核心机制，相对 NDCG@10 +12.84%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.20995">原论文</a> · <a href="../../../../reproductions/2602.20995-gpl-prerank/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Jointly Optimizing Debiased CTR and Uplift for Coupons Marketing: A Unified Causal Framework 搜广推与 LLM 应用 Kuaishou Technology 2026-02-13 用去混杂表示把基础点击倾向与券强度敏感性分开，再由双预测塔和反事实 X-Network 约束事实/反事实结果；单元 uplift 将不同券档的增量统一到可比较尺度。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.03955，相对变化 -26.76%。本地代理目标与论文生产任务不同，不能外推线上 lift。  causal-recommendation uplift-modeling coupon-marketing 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-unimvt-218d40bb">Jointly Optimizing Debiased CTR and Uplift for Coupons Marketing: A Unified Causal Framework</h2>
<p class="ar-learning-card__meta">Kuaishou Technology · 论文公开：2026-02-13</p>
<p><strong>方法要点：</strong>用去混杂表示把基础点击倾向与券强度敏感性分开，再由双预测塔和反事实 X-Network 约束事实/反事实结果；单元 uplift 将不同券档的增量统一到可比较尺度。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.03955，相对变化 -26.76%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12972">原论文</a> · <a href="../../../../reproductions/2602.12972-unimvt/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="SMES: Towards Scalable Multi-Task Recommendation via Expert Sparsity 搜广推与 LLM 应用 Kuaishou Technology 2026-02-10 把每个任务的激活专家拆为所有任务共享的稳定子集和任务自适应私有子集，并用跨任务全局负载均衡约束路由，控制激活量与专家倾斜。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05359，相对变化 -0.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。  multi-task-learning sparse-moe expert-routing 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-smes-9171fefe">SMES: Towards Scalable Multi-Task Recommendation via Expert Sparsity</h2>
<p class="ar-learning-card__meta">Kuaishou Technology · 论文公开：2026-02-10</p>
<p><strong>方法要点：</strong>把每个任务的激活专家拆为所有任务共享的稳定子集和任务自适应私有子集，并用跨任务全局负载均衡约束路由，控制激活量与专家倾斜。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05359，相对变化 -0.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.09386">原论文</a> · <a href="../../../../reproductions/2602.09386-smes/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Statistical Learning from Attribution Sets 搜广推与 LLM 应用 Google Research 2026-02-06 隐私归因场景不提供点击到转化的真实配对，候选集合还可能重叠。方法不采用随机或最大先验伪标签，而将二元损失拆为与标签无关的部分及标签相关矩，再由归因集合统计估计风险。主源定位：v1 §3 Theorem 1、§4.1 Eq6–7。 完整约7,800次、100–200epoch网格成本过高，不复现（审查DONE）。仅使用自建小规模数学夹具。单元素集合在穷举隐藏二元流时匹配真实风险；多元素集合的v1印刷系数未通过常数函数检查。令，原式给出  广告归因与弱监督 风险估计 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-attribution-sets-5c9ffe92">Statistical Learning from Attribution Sets</h2>
<p class="ar-learning-card__meta">Google Research · 论文公开：2026-02-06</p>
<p><strong>方法要点：</strong>隐私归因场景不提供点击到转化的真实配对，候选集合还可能重叠。方法不采用随机或最大先验伪标签，而将二元损失拆为与标签无关的部分及标签相关矩，再由归因集合统计估计风险。主源定位：v1 §3 Theorem 1、§4.1 Eq6–7。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整约7,800次、100–200epoch网格成本过高，不复现（审查DONE）。仅使用自建小规模数学夹具。单元素集合在穷举隐藏二元流时匹配真实风险；多元素集合的v1印刷系数未通过常数函数检查。令，原式给出</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.06276">原论文</a> · <a href="../../../../recommendation-components/2602.06276-attribution-sets/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Towards End-to-End Alignment of User Satisfaction via Questionnaire in Video Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-01-28 把稀疏问卷满意度监督放入独立 LoRA 参数路径，避免被海量行为标签淹没；在线 DPO 以问卷专家作为动态 reference，持续更新满意度偏好而尽量不扰动主排序干线。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05160，相对变化 -4.46%。本地代理目标与论文生产任务不同，不能外推线上 lift。  satisfaction-alignment preference-learning online-learning 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-easq-454991cc">Towards End-to-End Alignment of User Satisfaction via Questionnaire in Video Recommendation</h2>
<p class="ar-learning-card__meta">Kuaishou Technology · 论文公开：2026-01-28</p>
<p><strong>方法要点：</strong>把稀疏问卷满意度监督放入独立 LoRA 参数路径，避免被海量行为标签淹没；在线 DPO 以问卷专家作为动态 reference，持续更新满意度偏好而尽量不扰动主排序干线。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05160，相对变化 -4.46%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.20215">原论文</a> · <a href="../../../../reproductions/2601.20215-easq/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Cold-Starting Podcast Ads and Promotions with Multi-Task Learning on Spotify 搜广推与 LLM 应用 Spotify 2026-01-05 新 podcast 缺少广告点击与播放数据。论文联合训练 ads 和 organic promotions，共享 user/content/context 表征，从数据丰富任务迁移到冷启动任务，并以不平衡处理和梯度平衡抑制 negative transfer。 Fidelity: 核心机制复现。执行 shared low-rank multi-task representation 和冷物品分桶。MovieLens 电影与 genre 代理 podcast/ad 特征，没有 Spotify impression、bid 和曝光校准日志。本地对照口径：基线是 single-task popularity/content ranker；实验组联合 organic/promotion 两任务，NDCG@10 0.03540→0.02810，相对 -20.63%，本地出现 negative transfer。  cold-start multi-task ads 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-podcast-mtl-fc67da12">Cold-Starting Podcast Ads and Promotions with Multi-Task Learning on Spotify</h2>
<p class="ar-learning-card__meta">Spotify · 论文公开：2026-01-05</p>
<p><strong>方法要点：</strong>新 podcast 缺少广告点击与播放数据。论文联合训练 ads 和 organic promotions，共享 user/content/context 表征，从数据丰富任务迁移到冷启动任务，并以不平衡处理和梯度平衡抑制 negative transfer。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。执行 shared low-rank multi-task representation 和冷物品分桶。MovieLens 电影与 genre 代理 podcast/ad 特征，没有 Spotify impression、bid 和曝光校准日志。本地对照口径：基线是 single-task popularity/content ranker；实验组联合 organic/promotion 两任务，NDCG@10 0.03540→0.02810，相对 -20.63%，本地出现 negative transfer。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.02306">原论文</a> · <a href="../../../../reproductions/2601.02306-podcast-mtl/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Click A, Buy B: Rethinking Conversion Attribution in E-Commerce Recommendations 搜广推与 LLM 应用 Pinterest 2025-07-20 Last-click attribution 默认点击和购买属于同一商品，忽略用户点 A 后买 B。论文将 Click-A-Buy-A 与 Click-A-Buy-B 分成多任务，并用商品 taxonomy 建模 A/B 的协同归因。 Fidelity: 核心机制复现。实际构造 CABA/CABB 双分支，并按公开 genre taxonomy 学习跨物品协同权重。连续观影不等价于购买；没有真实曝光、归因窗口、广告竞价和 Pinterest taxonomy。本地对照口径：相对 last-click 单物品归因基线，实验组 NDCG@10 +33.70%。  conversion-attribution multi-task-learning taxonomy ads-ranking 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-click-a-buy-b-aac757e9">Click A, Buy B: Rethinking Conversion Attribution in E-Commerce Recommendations</h2>
<p class="ar-learning-card__meta">Pinterest · 论文公开：2025-07-20</p>
<p><strong>方法要点：</strong>Last-click attribution 默认点击和购买属于同一商品，忽略用户点 A 后买 B。论文将 Click-A-Buy-A 与 Click-A-Buy-B 分成多任务，并用商品 taxonomy 建模 A/B 的协同归因。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。实际构造 CABA/CABB 双分支，并按公开 genre taxonomy 学习跨物品协同权重。连续观影不等价于购买；没有真实曝光、归因窗口、广告竞价和 Pinterest taxonomy。本地对照口径：相对 last-click 单物品归因基线，实验组 NDCG@10 +33.70%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.15113">原论文</a> · <a href="../../../../reproductions/2507.15113-click-a-buy-b/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Macro Graph of Experts for Billion-Scale Multi-Task Recommendation 搜广推与 LLM 应用 Alibaba 2025-06-12 MMoE 只在样本级通过 gate 隐式共享，难表达任务间稳定结构。MGOE 先构建 Macro Task Merging Graph，再由 Macro Graph Bottom/Experts 传播跨任务信息，最后进入任务塔。 Fidelity: 核心机制复现。实际估计多任务相关图，执行宏观图传播 experts 和任务门控预测。公开 proxy 任务远小于工业多目标；没有十亿级 sparse embedding、分布式图构建和阿里线上特征。本地对照口径：相对 MMoE 独立 gate 基线，实验组 NDCG@10 +7.03%。  multi-task-learning mixture-of-experts graph-neural-network ranking 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-mgoe-e3468d6f">Macro Graph of Experts for Billion-Scale Multi-Task Recommendation</h2>
<p class="ar-learning-card__meta">Alibaba · 论文公开：2025-06-12</p>
<p><strong>方法要点：</strong>MMoE 只在样本级通过 gate 隐式共享，难表达任务间稳定结构。MGOE 先构建 Macro Task Merging Graph，再由 Macro Graph Bottom/Experts 传播跨任务信息，最后进入任务塔。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。实际估计多任务相关图，执行宏观图传播 experts 和任务门控预测。公开 proxy 任务远小于工业多目标；没有十亿级 sparse embedding、分布式图构建和阿里线上特征。本地对照口径：相对 MMoE 独立 gate 基线，实验组 NDCG@10 +7.03%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2506.10520">原论文</a> · <a href="../../../../reproductions/2506.10520-mgoe/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Counteracting Duration Bias in Video Recommendation via Counterfactual Watch Time 搜广推与 LLM 应用 Kuaishou Technology / Renmin University of China 2024-06-12 以反事实观看时长估计消除视频时长偏置：区分观察到的 watch time 与在统一时长干预下的潜在收益。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 cwm 核心机制；相对 NDCG@10 -17.89%。  ranking counterfactual-learning watch-time bias 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-cwm-65e93cb4">Counteracting Duration Bias in Video Recommendation via Counterfactual Watch Time</h2>
<p class="ar-learning-card__meta">Kuaishou Technology / Renmin University of China · 论文公开：2024-06-12</p>
<p><strong>方法要点：</strong>以反事实观看时长估计消除视频时长偏置：区分观察到的 watch time 与在统一时长干预下的潜在收益。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 cwm 核心机制；相对 NDCG@10 -17.89%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2406.07932">原论文</a> · <a href="../../../../reproductions/2406.07932-cwm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Progressive Layered Extraction (PLE): A Novel Multi-Task Learning Model for Personalized Recommendations 搜广推与 LLM 应用 Tencent 2020-09-22 MMoE 仍让所有 experts 在所有任务间共享，任务冲突强时难以同时保留共性与个性。PLE 将 experts 分成共享组和任务专属组，通过 CGC 门控逐层提取共享与特定信息，减少跷跷板现象。 复现级别：核心机制复现。复现级别：核心机制复现。实际训练共享/任务专属 experts、CGC gates 和独立 heads；腾讯视频生产规模未复刻。本地对照口径：基线为 MMoE，实验组为共享与任务专属 experts 的 CGC/PLE；平均任务 AUC 相对 +1.34%，见 metrics/movielens-100k-seeds42-44.json。  ranking classic multi-task mixture-of-experts 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-ple-a2bf42a4">Progressive Layered Extraction (PLE): A Novel Multi-Task Learning Model for Personalized Recommendations</h2>
<p class="ar-learning-card__meta">Tencent · 论文公开：2020-09-22</p>
<p><strong>方法要点：</strong>MMoE 仍让所有 experts 在所有任务间共享，任务冲突强时难以同时保留共性与个性。PLE 将 experts 分成共享组和任务专属组，通过 CGC 门控逐层提取共享与特定信息，减少跷跷板现象。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制复现。复现级别：核心机制复现。实际训练共享/任务专属 experts、CGC gates 和独立 heads；腾讯视频生产规模未复刻。本地对照口径：基线为 MMoE，实验组为共享与任务专属 experts 的 CGC/PLE；平均任务 AUC 相对 +1.34%，见 metrics/movielens-100k-seeds42-44.json。</p></details>
<p class="ar-learning-card__links"><a href="https://doi.org/10.1145/3383313.3412236">原论文</a> · <a href="../../../../reproductions/recsys2020-ple-ple/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Modeling Task Relationships in Multi-task Learning with Multi-gate Mixture-of-Experts 搜广推与 LLM 应用 Google 2018-08-19 共享底座的多任务模型会在任务相关性较低时产生负迁移。完全独立的模型又无法利用共性。MMoE 建立一组共享专家，但为每个任务学习独立 softmax gate，让任务以不同权重组合专家。 复现级别：核心机制复现。复现级别：核心机制复现。实际训练共享 experts、任务专属 gates 与任务 heads；Google 私有业务特征未复刻。本地对照口径：基线为 shared-bottom 双任务网络，实验组为每任务独立 gate 的共享 experts；平均任务 AUC 相对 +1.30%，见 metrics/movielens-100k-seeds42-44.json。  ranking classic multi-task mixture-of-experts 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-mmoe-a1bda9df">Modeling Task Relationships in Multi-task Learning with Multi-gate Mixture-of-Experts</h2>
<p class="ar-learning-card__meta">Google · 论文公开：2018-08-19</p>
<p><strong>方法要点：</strong>共享底座的多任务模型会在任务相关性较低时产生负迁移。完全独立的模型又无法利用共性。MMoE 建立一组共享专家，但为每个任务学习独立 softmax gate，让任务以不同权重组合专家。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制复现。复现级别：核心机制复现。实际训练共享 experts、任务专属 gates 与任务 heads；Google 私有业务特征未复刻。本地对照口径：基线为 shared-bottom 双任务网络，实验组为每任务独立 gate 的共享 experts；平均任务 AUC 相对 +1.30%，见 metrics/movielens-100k-seeds42-44.json。</p></details>
<p class="ar-learning-card__links"><a href="https://research.google/pubs/modeling-task-relationships-in-multi-task-learning-with-multi-gate-mixture-of-experts/">原论文</a> · <a href="../../../../reproductions/kdd2018-mmoe-mmoe/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Entire Space Multi-Task Model: An Effective Approach for Estimating Post-Click Conversion Rate 搜广推与 LLM 应用 Alibaba 2018-04-21 CVR 只在点击样本上可观测，直接训练会遭遇 sample-selection bias；转化又远比点击稀疏。ESMM 在全曝光空间同时学习 CTR 与 CVR，并用概率链式分解得到 CTCVR。CTR 的稠密监督帮助 CVR tower 学到更稳定的表示。 复现级别：核心机制复现。复现级别：核心机制复现。实际执行 CTR/CVR 双塔、概率乘积与 entire-space loss；淘宝私有漏斗数据由公开数据构造替代。本地对照口径：基线只在 clicked space 训练 CVR，实验组在 entire space 联合 CTR 与 CTCVR；平均任务 AUC 相对 +1.69%，见 metrics/movielens-100k-seeds42-44.json。  ranking classic multi-task conversion 搜广推 学习信号、多任务与反馈偏差">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<h2 id="paper-recommendation-esmm-4cd7f113">Entire Space Multi-Task Model: An Effective Approach for Estimating Post-Click Conversion Rate</h2>
<p class="ar-learning-card__meta">Alibaba · 论文公开：2018-04-21</p>
<p><strong>方法要点：</strong>CVR 只在点击样本上可观测，直接训练会遭遇 sample-selection bias；转化又远比点击稀疏。ESMM 在全曝光空间同时学习 CTR 与 CVR，并用概率链式分解得到 CTCVR。CTR 的稠密监督帮助 CVR tower 学到更稳定的表示。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制复现。复现级别：核心机制复现。实际执行 CTR/CVR 双塔、概率乘积与 entire-space loss；淘宝私有漏斗数据由公开数据构造替代。本地对照口径：基线只在 clicked space 训练 CVR，实验组在 entire space 联合 CTR 与 CTCVR；平均任务 AUC 相对 +1.69%，见 metrics/movielens-100k-seeds42-44.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1804.07931">原论文</a> · <a href="../../../../reproductions/1804.07931-esmm/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
