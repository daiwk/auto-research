---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 学习信号、多任务与反馈偏差

[搜广推](index.md) / 35 个问题 · 35 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">35 个问题 · 35 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hge" data-paper-title="Hierarchical GTV Estimation: Bridging the Gap between Container-Level Ranking and Item-Level Conversion" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Hierarchical GTV Estimation: Bridging the Gap between Container-Level Ranking and Item-Level Conversion 搜广推与 LLM 应用 Meituan 2026-10-23 搜索广告排序的是门店、直播间等“容器”，成交却发生在内部商品上。单条成交金额既稀疏又高方差，简单把门店当成一个商品，容易忽略低价高频与高价低频商品的组合。HGE 先用 Hybrid Set-Aware Encoder 编码 top-K 商品的竞争关系，再在自注意力之后拼入用户、门店、上下文与查询。Proxy-Label Learning 分开预测门店是否成交、成交后每个商品的购买概率和数量； 论文私有日志训练和线上实验成本过高，不复现（审查 DONE）；实现范围为 HSAE、PLL、RCEF 的可微 L1 组件，不是完整广告模型。论文私有日志训练和线上实验成本过高，不复现（审查 DONE）；不据此宣称本地获得线上收益或接入 Evolve。HierarchicalGTV 接受外部商品 embedding、位置向量、上下文、价格和通用回归输出，不收答案/成交标签。以小尺寸可微模块验证：独立逐商品 Eq.5 参考、上下文不影响前置 MHSA、位置/价格/残差移除负控、融合两端点、商品概率之和可大于1、所有参数和输入的有限非零梯度。种子为42/43/44；指标只是合成机制误差和梯度，不是推荐准确率、收入或校准效果。  广告价值预估 层次化多任务学习 搜广推 学习信号、多任务与反馈偏差 HGE为什么分别预测容器成交、内部商品购买概率和数量，而不只回归一个门店GMV？ 容器价值来自内部商品组合，单一金额标签稀疏且波动大。分解让模型先表达是否成交，再累加不同商品的条件购买与数量，并以残差补偿top-K遗漏；商品不是互斥选择，不能把独立购买概率改成总和为一的softmax。融合门必须读取上下文，不能按真实成交标签事后选支路。 示意：用户可能在同一店同时买两件低价商品，或只买一件高价商品；把内部商品视作互斥类别会漏掉多件购买，单一门店回归又难解释这些来源差异。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-hge-0554c3a1" class="ar-learning-paper-anchor"></span>
<h2 id="qa-5741411042653d97">HGE为什么分别预测容器成交、内部商品购买概率和数量，而不只回归一个门店GMV？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahge">Hierarchical GTV Estimation: Bridging the Gap between Container-Level Ranking and Item-Level Conversion</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>容器价值来自内部商品组合，单一金额标签稀疏且波动大。分解让模型先表达是否成交，再累加不同商品的条件购买与数量，并以残差补偿top-K遗漏；商品不是互斥选择，不能把独立购买概率改成总和为一的softmax。融合门必须读取上下文，不能按真实成交标签事后选支路。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户可能在同一店同时买两件低价商品，或只买一件高价商品；把内部商品视作互斥类别会漏掉多件购买，单一门店回归又难解释这些来源差异。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32420v1">原论文</a> · <a href="../../../../recommendation-components/2610.32420-hge/">实现解读</a> · <a href="#qa-5741411042653d97">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:baseline-incremental" data-paper-title="Baseline and Incremental: User, Item, and Request Debiasing in Instagram Feed Ranking" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Baseline and Incremental: User, Item, and Request Debiasing in Instagram Feed Ranking 搜广推与 LLM 应用 Meta 2026-10-20 参与度预测同时包含用户习惯、商品受欢迎程度、当前候选池水平和候选自身的相对优势。直接去掉基线可能丢失有用的绝对水平。论文保留原始预测，同时对相对基线的非线性增量单独加权；这是评分配置变化，不是因果uplift估计。用户、商品基线来自历史特征，请求基线来自当前候选池。概率使用log-odds差，回归量使用同单位差；正向门和降权门的幅度不同，不能把乘预测值的正向门直接改符号用于降权，否则预测接近零时惩罚也消失。 完整私有日志、排名系统及线上消融成本过高，不复现（审查 DONE）。仅为L1机制诊断，不是线上收益复现；已实现评分算子，不新增或训练排名网络。仅为L1机制诊断，不是线上收益复现；完整私有日志、排名系统及线上消融成本过高，不复现（审查 DONE）。运行独立有理式参考、hinge与sigmoid区别、预测地板降权和移除增量项的排序负对照，seed42/43/44。输入为合成分数，不读取生产数据，不拟合或选择线上权重，不将数组排序改变解释为推荐提升。request_baseline只计算调用方指定的池内统计，不自行学会选择基线。  排序与决策优化 基线与增量去偏 搜广推 学习信号、多任务与反馈偏差 已经减去用户或商品基线，为什么还要保留原始预测项？ 相对基线表示候选超出常态的程度，原始预测保留真实业务量级，两者提供不同信息。方法为非线性增量单独设权重，概率在log-odds空间比较，回归量用同单位差；它是评分配置，不是因果uplift。若只按相对改善排，低基线上的小绝对收益可能压过高价值候选。 示意：候选A从低基线略升，候选B本来就有较高购买概率；只看相对变化会偏向A，保留绝对预测才能同时表达高基线的真实价值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-baseline-incremental-a452c157" class="ar-learning-paper-anchor"></span>
<h2 id="qa-047a61e14691f63d">已经减去用户或商品基线，为什么还要保留原始预测项？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Abaseline-incremental">Baseline and Incremental: User, Item, and Request Debiasing in Instagram Feed Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相对基线表示候选超出常态的程度，原始预测保留真实业务量级，两者提供不同信息。方法为非线性增量单独设权重，概率在log-odds空间比较，回归量用同单位差；它是评分配置，不是因果uplift。若只按相对改善排，低基线上的小绝对收益可能压过高价值候选。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>候选A从低基线略升，候选B本来就有较高购买概率；只看相对变化会偏向A，保留绝对预测才能同时表达高基线的真实价值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.27423v1">原论文</a> · <a href="../../../../recommendation-components/2610.27423-baseline-incremental/">实现解读</a> · <a href="#qa-047a61e14691f63d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:casi" data-paper-title="CASI: Credit Assignment via Set Intervention for Agentic Retrieval" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="CASI: Credit Assignment via Set Intervention for Agentic Retrieval 搜广推与 LLM 应用 Xiaohongshu 2026-10-14 一次检索请求可能联合产生多个改写动作，线上却只返回整个结果集合的奖励。CASI 不把这个奖励简单均分：每个动作只检索一次，冻结候选快照，再重组子集、评估候选之间的协同与替代关系，以 Shapley 边际贡献分配信用。随后用共享尺度归一化与有界零和投影，将集合信用转为 action/token 优势。集合奖励广播仍可给出原集合目标的有效 score-function 估计；CASI 的内部优势塑形不能额外宣称保持同一无偏梯度。论文也指出：加性集合无需额外干预； 完整的私有拍卖重放、LLM 五次训练及生产 A/B：成本过高，不复现（审查 DONE）。默认诊断后端按固定分数对每个子集重新取 top-2，属于显式的 pr_rerun 敏感性示例，不是论文的私有 pr_filter 训练后端；本地对照口径：基线为相同冻结集合函数上的 Singleton 和 LOO，实验组为精确/置换 Shapley 与零和优势组件；没有策略训练，相对能力提升不适用。  agentic-retrieval credit-assignment policy-optimization 搜广推 学习信号、多任务与反馈偏差 CASI为什么冻结检索快照后重组子集，而不把集合奖励平均分给各动作？ 多个改写动作的候选可能互相补充或替代，均分奖励会掩盖这种作用。CASI固定每个动作一次检索的结果，比较它加入不同子集时的边际价值，再用Shapley信用塑形优势。冻结快照避免重复检索噪声污染归因，但这种内部塑形不能额外声称保留原集合目标的同一无偏梯度。 示意：改写A与B返回相同商品，C补出新类目；三者平分奖励会高估重复动作。固定结果后移除或加入不同组合，才能看出C的互补贡献。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-casi-2c2b2f1b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-26fe8a4e5a7b2ef3">CASI为什么冻结检索快照后重组子集，而不把集合奖励平均分给各动作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acasi">CASI: Credit Assignment via Set Intervention for Agentic Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多个改写动作的候选可能互相补充或替代，均分奖励会掩盖这种作用。CASI固定每个动作一次检索的结果，比较它加入不同子集时的边际价值，再用Shapley信用塑形优势。冻结快照避免重复检索噪声污染归因，但这种内部塑形不能额外声称保留原集合目标的同一无偏梯度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>改写A与B返回相同商品，C补出新类目；三者平分奖励会高估重复动作。固定结果后移除或加入不同组合，才能看出C的互补贡献。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20293">原论文</a> · <a href="../../../../reproductions/2610.20293-casi/">实现解读</a> · <a href="#qa-26fe8a4e5a7b2ef3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:promptshift" data-paper-title="Measuring and Mitigating Identity-Cue Preference Drift in LLM-based Recommender Systems" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Measuring and Mitigating Identity-Cue Preference Drift in LLM-based Recommender Systems 搜广推与 LLM 应用 University of Electronic Science and Technology of China 2026-09-28 在行为历史不变时比较身份提示与无身份参考列表，用 Drift 与 SliceShift 量化身份线索偏移，再依据用户主流度自适应混合原分与逆群体流行度。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行列表指标与后处理 reranker；身份 slice 和相关性由公开 fixture 给出，不生成真实用户画像。执行列表指标与后处理 reranker；身份 slice 和相关性由公开 fixture 给出，不生成真实用户画像。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  llm-recommendation identity-cue-drift fairness 搜广推 学习信号、多任务与反馈偏差 PromptShift 为什么固定行为历史，只改变身份提示，再分别测量 Drift 与 SliceShift？ 同时更改历史和身份无法区分列表变化来自真实偏好还是身份线索。固定历史后，Drift 描述列表重叠与位次变化，SliceShift 描述群体流行度方向的变化，再按主流度调整相关性和逆流行度混合。它提供受控敏感性诊断，不足以单独证明社会因果歧视；本地也明确只做诊断。 示意：同一段电影观看历史分别附上与不附上身份描述，比较推荐是否系统性偏向某群体热门片。保持历史不变，才便于观察额外身份线索带来的列表移动。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-promptshift-7e539145" class="ar-learning-paper-anchor"></span>
<h2 id="qa-27ec4d2dd288c79e">PromptShift 为什么固定行为历史，只改变身份提示，再分别测量 Drift 与 SliceShift？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apromptshift">Measuring and Mitigating Identity-Cue Preference Drift in LLM-based Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Electronic Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同时更改历史和身份无法区分列表变化来自真实偏好还是身份线索。固定历史后，Drift 描述列表重叠与位次变化，SliceShift 描述群体流行度方向的变化，再按主流度调整相关性和逆流行度混合。它提供受控敏感性诊断，不足以单独证明社会因果歧视；本地也明确只做诊断。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一段电影观看历史分别附上与不附上身份描述，比较推荐是否系统性偏向某群体热门片。保持历史不变，才便于观察额外身份线索带来的列表移动。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34229">原论文</a> · <a href="../../../../reproductions/2609.34229-promptshift/">实现解读</a> · <a href="#qa-27ec4d2dd288c79e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:flvm" data-paper-title="Mend the Measurement Gap: Latent User Preference Modeling for Short-Form Video Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Mend the Measurement Gap: Latent User Preference Modeling for Short-Form Video Recommendation 搜广推与 LLM 应用 Google / YouTube 2026-09-26 短视频的观看时长会被视频长度、用户习惯和时段影响，同样的观看行为不一定代表喜欢。Google/YouTube 的 FLVM 不直接把各种行为当成单一偏好分数，而是用三维潜变量分别表示消费、主动参与、参与方向（正负）。时长等测量混杂因素只进入受限基线；完整的用户—视频信息进入潜变量编码器。每个反馈头只读取与其语义相符的因子，然后在 logit 空间叠加到停止梯度的基线上。 复现级别：公开数据概念验证。复现级别：公开数据概念验证。本地执行了三因子高斯潜变量、受限基线、稀疏路由、停止梯度与 KL 损失；没有 YouTube 的满意度调查、生产特征和线上实验，不能据此声称复现 +2.67% 收益。本地对照口径：实验组为 FLVM 缩比结构；基线为独立初始化和训练、读取相同曝光前特征、使用相同四种反馈与更新步数的共享塔多任务模型。两者不是 YouTube 生产模型，相对论文线上收益不适用。  ranking multi-task feedback-debiasing 搜广推 学习信号、多任务与反馈偏差 FLVM为什么把测量混杂放进受限基线，再用受路由约束的潜变量修正反馈头？ 观看时长等反馈受视频长度和用户习惯影响，不是纯偏好。受限基线先解释测量条件，潜变量分别承担消费、主动参与和正负方向，反馈头只读取语义相关因子；基线停止梯度避免残差目标反过来任意改写参照。结构限制帮助分工，但不构成潜变量已被完全因果识别的保证。 示意：完整看完短片与中途划走长片可能秒数接近；基线解释长度机会，潜变量再区分主动喜欢与被动消费，不能让所有反馈都变成同一个时长偏好分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-flvm-33286ec7" class="ar-learning-paper-anchor"></span>
<h2 id="qa-63ac9135b7c263d4">FLVM为什么把测量混杂放进受限基线，再用受路由约束的潜变量修正反馈头？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aflvm">Mend the Measurement Gap: Latent User Preference Modeling for Short-Form Video Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>观看时长等反馈受视频长度和用户习惯影响，不是纯偏好。受限基线先解释测量条件，潜变量分别承担消费、主动参与和正负方向，反馈头只读取语义相关因子；基线停止梯度避免残差目标反过来任意改写参照。结构限制帮助分工，但不构成潜变量已被完全因果识别的保证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>完整看完短片与中途划走长片可能秒数接近；基线解释长度机会，潜变量再区分主动喜欢与被动消费，不能让所有反馈都变成同一个时长偏好分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.32839">原论文</a> · <a href="../../../../reproductions/2609.32839-flvm/">实现解读</a> · <a href="#qa-63ac9135b7c263d4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cross-task-relationships" data-paper-title="Learned Cross-Task Relationships in Multi-Task Models" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Learned Cross-Task Relationships in Multi-Task Models 搜广推与 LLM 应用 Google 2026-09-23 多任务网络只预测各反馈的边际概率，可能丢掉任务之间的联合信息。该方法加入成对联合标签或缺失的无条件辅助头，既给共享表示提供额外梯度，也能把联合预测作为下游策略的新输入；论文将这两种收益分阶段隔离测试。 成本过高，不复现（审查 DONE）：原文每日数十亿样本、多周训练与线上实验不在单卡预算内；小切片稀疏且有前缀选择偏差，三种子仍只是诊断，不是稳定能力提升。使用官方 KuaiRand-Pure 固定 4,096 行曝光前缀，时间排序后按 70/15/15 划分 train/validation/test。特征仅含曝光前的用户/视频 ID、时段和视频时长；is_click / long_view 只进入损失与评分。训练集检查四种联合标签均存在，排除互斥、嵌套、常量或当前切片无法支持的任务对。  多目标与多任务学习 联合标签与辅助头 搜广推 学习信号、多任务与反馈偏差 已经分别预测点赞率和点击率，为什么还需要预测两者的联合标签？ 边际概率无法确定两个反馈是否集中在同一批样本上。联合头补充依赖信息，既能给共享表示额外监督，也能成为下游决策信号；这两种收益应分开验证。由边际与联合值恢复完整分布时，还要检查概率是否可行，不能把负概率裁掉后就声称模型已经校准。 示意：两个模型都预测点击率和点赞率各为20%，一种情况完全发生在同一群人，另一种彼此分离；只看两个边际，无法区分应如何组合业务目标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-cross-task-relationships-c0c2f1d1" class="ar-learning-paper-anchor"></span>
<h2 id="qa-3a67c9b61c5a23fb">已经分别预测点赞率和点击率，为什么还需要预测两者的联合标签？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Across-task-relationships">Learned Cross-Task Relationships in Multi-Task Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>边际概率无法确定两个反馈是否集中在同一批样本上。联合头补充依赖信息，既能给共享表示额外监督，也能成为下游决策信号；这两种收益应分开验证。由边际与联合值恢复完整分布时，还要检查概率是否可行，不能把负概率裁掉后就声称模型已经校准。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个模型都预测点击率和点赞率各为20%，一种情况完全发生在同一群人，另一种彼此分离；只看两个边际，无法区分应如何组合业务目标。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.28776">原论文</a> · <a href="../../../../recommendation-components/2609.28776-cross-task-relationships/">实现解读</a> · <a href="#qa-3a67c9b61c5a23fb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:light-heads" data-paper-title="Lightweight Ranking Heads: Accelerating Multi-Task Experimentation in Production Recommender Systems" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Lightweight Ranking Heads: Accelerating Multi-Task Experimentation in Production Recommender Systems 搜广推与 LLM 应用 Google 2026-09-21 工业多任务 ranker 要添加新目标时，直接改动共享塔可能导致旧目标负迁移，还会让并行实验模型与下游模型输出空间不一致。论文把新增目标声明为中央配置，训练时在共享表示上动态挂一个浅头；轻头输入执行 stop_gradient，因此新目标不会回传到共享塔。每个持续训练窗口可以重置轻头参数，使不同上游模型的轻头训练年龄可比较。论文也报告了“不重置”和“去掉 stop-gradient”的消融，前者可能给数据稀疏的目标更好的拟合，后者可能损伤原任务。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地确实执行了动态注入、stop-gradient、训练窗口重置以及两个对应消融；没有 Google 私有流量、持续训练平台或线上下游模型。公开数据结果与论文线上结果严格分开。执行了论文定义性的“共享塔 + 动态轻头 + 梯度隔离 + 可选重置”；不是同名的后处理打分函数。本地对照口径：同预算不重置轻头为新任务基线，test AUC 0.6267；标准重置实验组 0.5109，相对 -18.48%。这是公开数据短训练窗口的负结果。  ranking multi-task-learning lightweight-heads 搜广推 学习信号、多任务与反馈偏差 Light Heads对共享表示做stop-gradient后，新目标还能改善主干吗？ 单独的新目标损失不能通过这条路径更新共享主干，只能训练浅头，因此可以降低新增目标对旧任务的干扰。窗口重置又让并行模型的轻头训练年龄可比较，但会损失稀疏目标的长期拟合。隔离梯度与重置是两种不同控制，不能把新头AUC提高解释为主干能力已经因此增强。 示意：给成熟点击模型临时加一个新反馈头，梯度隔离可避免它伤害旧塔；每周重置便于公平比较不同上游，但新任务样本很少时也可能重新学不够。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-light-heads-bf390928" class="ar-learning-paper-anchor"></span>
<h2 id="qa-52edfaf206e2bd93">Light Heads对共享表示做stop-gradient后，新目标还能改善主干吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alight-heads">Lightweight Ranking Heads: Accelerating Multi-Task Experimentation in Production Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单独的新目标损失不能通过这条路径更新共享主干，只能训练浅头，因此可以降低新增目标对旧任务的干扰。窗口重置又让并行模型的轻头训练年龄可比较，但会损失稀疏目标的长期拟合。隔离梯度与重置是两种不同控制，不能把新头AUC提高解释为主干能力已经因此增强。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>给成熟点击模型临时加一个新反馈头，梯度隔离可避免它伤害旧塔；每周重置便于公平比较不同上游，但新任务样本很少时也可能重新学不够。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.25433">原论文</a> · <a href="../../../../reproductions/2609.25433-light-heads/">实现解读</a> · <a href="#qa-52edfaf206e2bd93">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:baff" data-paper-title="BAFF: Bid-Aware Filter Family for Mitigating Training Data Interference in RTB A/B Tests" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="BAFF: Bid-Aware Filter Family for Mitigating Training Data Interference in RTB A/B Tests 搜广推与 LLM 应用 Dable 2026-09-08 RTB 实验中 A/B 两个策略看到的竞价机会会互相影响；直接混用日志训练 B 模型会引入 treatment interference。BAFF 同时检查 A 广告在 B 排序中的位置差和 bid-price 差，只保留对 B 决策近似无干扰的 A 日志。 复现级别：受控仿真核心机制。复现级别：受控仿真核心机制。精确执行论文过滤判据，以 B-only 训练作参照测量共享日志参数偏差；不把仿真结果称为线上提升。2,400 次受控拍卖、三种子结果见 metrics/controlled-rtb-seeds42-44.json。仿真真实执行严格双轴过滤及 ridge 参数偏差诊断，但没有 Dable 私有 DSP 日志、生产 CTR 模型或市场侧 reference 实验。  advertising rtb ab-testing training-data-interference 搜广推 学习信号、多任务与反馈偏差 BAFF为什么同时比较排序位置差和竞价价格差，只过滤其中一项不够吗？ 两个实验策略即使给出相近名次，也可能因价格差改变赢标机会；价格接近时，排序差又可能改变曝光分布。BAFF以双轴条件筛掉会显著影响B策略决策的A日志，减少训练中的处理干扰。保留下来只表示在给定条件下较可迁移，不等于恢复了真实无干扰市场。 示意：A广告在B榜单位置相近，却有大幅更高报价，仍可能抢走机会；反之价格相同但名次跨过展示边界，也不能直接混用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-baff-e8ac8fd9" class="ar-learning-paper-anchor"></span>
<h2 id="qa-14b2794811c5695a">BAFF为什么同时比较排序位置差和竞价价格差，只过滤其中一项不够吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Abaff">BAFF: Bid-Aware Filter Family for Mitigating Training Data Interference in RTB A/B Tests</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dable</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两个实验策略即使给出相近名次，也可能因价格差改变赢标机会；价格接近时，排序差又可能改变曝光分布。BAFF以双轴条件筛掉会显著影响B策略决策的A日志，减少训练中的处理干扰。保留下来只表示在给定条件下较可迁移，不等于恢复了真实无干扰市场。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>A广告在B榜单位置相近，却有大幅更高报价，仍可能抢走机会；反之价格相同但名次跨过展示边界，也不能直接混用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08725">原论文</a> · <a href="../../../../reproductions/2609.08725-baff/">实现解读</a> · <a href="#qa-14b2794811c5695a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dceo" data-paper-title="DCEO: Direct Causal Effect Optimization for Long-Term User Value Modeling in E-commerce Search" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="DCEO: Direct Causal Effect Optimization for Long-Term User Value Modeling in E-commerce Search 搜广推与 LLM 应用 Taobao &amp; Tmall Group, Alibaba 2026-08-26 固定加权的点击、转化和 GMV 目标不能随用户状态改变，也无法直接刻画一次排序动作的长期因果价值。DCEO 用 actor 输出上下文相关 simplex 权重，用用户级 critic 估计相对干预效果；线上只保留轻量 actor。 本地负相关诊断明确阻止把 Hit 改善解读为长期价值提升。Fidelity：核心机制复现。本地执行上下文条件目标权重、用户级 proxy 聚合和相对因果干预；生产 critic 与在线 actor serving 未复刻。proxy outcome 与真实长期 GMV 不等价；本地负相关诊断明确阻止把 Hit 改善解读为长期价值提升。本地实现现在把 causal_gain × temperature 纳入 evolve 搜索空间：20 个候选只在 validation 上按 NDCG@10 + 0.15 × Hit@10 选择，随后仅对冠军运行一次 held-out test。  search-ranking long-term-value causal-optimization multi-objective-ranking 搜广推 学习信号、多任务与反馈偏差 DCEO为什么让actor按上下文输出目标权重，而不是全站固定一组CTR、CVR、GMV系数？ 固定系数假设所有用户状态具有相同取舍，难以体现一次动作对长期价值的不同影响。actor输出和为一的动态权重，critic在训练中评估相对干预效果，服务侧只保留轻量权重决策。动态权重本身不等于因果识别，若critic缺少可信对照，仍可能只学到相关性代理。 示意：新用户更需要探索合适内容，成熟购物用户可能更重转化；同一组分数可按状态采用不同组合，但要用相应长期反馈验证，而不是仅看即时点击。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-dceo-b39ed1b8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-58453392f6b5bfe3">DCEO为什么让actor按上下文输出目标权重，而不是全站固定一组CTR、CVR、GMV系数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adceo">DCEO: Direct Causal Effect Optimization for Long-Term User Value Modeling in E-commerce Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group, Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定系数假设所有用户状态具有相同取舍，难以体现一次动作对长期价值的不同影响。actor输出和为一的动态权重，critic在训练中评估相对干预效果，服务侧只保留轻量权重决策。动态权重本身不等于因果识别，若critic缺少可信对照，仍可能只学到相关性代理。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新用户更需要探索合适内容，成熟购物用户可能更重转化；同一组分数可按状态采用不同组合，但要用相应长期反馈验证，而不是仅看即时点击。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25635">原论文</a> · <a href="../../../../reproductions/2608.25635-dceo/">实现解读</a> · <a href="#qa-58453392f6b5bfe3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:incrementality" data-paper-title="From Prediction to Incrementality: Causal Optimization for Large-Scale Targeting and Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="From Prediction to Incrementality: Causal Optimization for Large-Scale Targeting and Recommendation 搜广推与 LLM 应用 LinkedIn 2026-08-10 分别估计处理与不处理时的潜在结果，以 uplift 及其不确定度代替点击概率排序，再在固定触达预算下完成因果分配。这样优化的是动作带来的增量价值，而不是本来就会发生的结果。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线按 treated outcome 排序，实验组按 uplift 与不确定度分配；同为 30% 预算，seed 42 的 policy value 为 0.10408，基线为 0.09537。  causal-recommendation uplift bandit constrained-allocation 搜广推 学习信号、多任务与反馈偏差 为什么高购买概率用户未必是有限触达预算下的最佳对象？ 触达策略关心动作改变了多少结果，而高购买概率可能表示用户不干预也会购买。方法分别估计处理和不处理结局，以uplift扣除不确定度后分配预算，避免把资源都花在本来就会发生的结果上。差值是否可信取决于实验支持与识别条件，不能由两个预测头存在就保证因果正确。 示意：甲无论是否触达都常买，乙只有看到合适推荐才可能买；同样一个触达名额，乙的原始购买率虽低，增量收益却可能更高。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-incrementality-26b16fde" class="ar-learning-paper-anchor"></span>
<h2 id="qa-e4b37a9687331955">为什么高购买概率用户未必是有限触达预算下的最佳对象？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aincrementality">From Prediction to Incrementality: Causal Optimization for Large-Scale Targeting and Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>触达策略关心动作改变了多少结果，而高购买概率可能表示用户不干预也会购买。方法分别估计处理和不处理结局，以uplift扣除不确定度后分配预算，避免把资源都花在本来就会发生的结果上。差值是否可信取决于实验支持与识别条件，不能由两个预测头存在就保证因果正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>甲无论是否触达都常买，乙只有看到合适推荐才可能买；同样一个触达名额，乙的原始购买率虽低，增量收益却可能更高。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.10182">原论文</a> · <a href="../../../../reproductions/2608.10182-incrementality/">实现解读</a> · <a href="#qa-e4b37a9687331955">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:twitch-mor" data-paper-title="Multi-Objective Ranking for Live-Streaming: Balancing Fresh and Delayed Signals with Segment-Aware Targeting" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Multi-Objective Ranking for Live-Streaming: Balancing Fresh and Delayed Signals with Segment-Aware Targeting 搜广推与 LLM 应用 Twitch 2026-08-05 主题：直播多目标排序。直播观看、互动、关注和付费的反馈延迟不同，且生命周期分群差异明显。论文组合即时/延迟模型、分群目标权重与 MMoE，在共享专家的同时保留目标专属 gate。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。MovieLens-1M 构造五个即时/延迟目标，比较单目标 DNN 与三专家生命周期 MMoE。  ranking multi-task-learning mmoe live-streaming 搜广推 学习信号、多任务与反馈偏差 Twitch 多目标排序为什么同时处理反馈延迟、用户生命周期权重和 MMoE gate？ 观看、互动、关注与付费在观测时点和用户阶段上含义不同，直接混成一个目标会偏向容易立即得到的信号。即时与延迟模型处理成熟度差异，分群权重表达不同生命周期目标，MMoE 则共享有用专家并保留任务选择。三者针对标签、业务取舍和表示冲突，不能只用一个总体指标证明所有阶段受益。 示意：新用户先建立观看习惯，老用户可能更看重深度互动；付费还比点击晚发生。模型分别处理时间与阶段，再通过任务 gate 组合专家，而不是让点击数量压过全部目标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-twitch-mor-68bc3da8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-9a6f243fe269c1c1">Twitch 多目标排序为什么同时处理反馈延迟、用户生命周期权重和 MMoE gate？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atwitch-mor">Multi-Objective Ranking for Live-Streaming: Balancing Fresh and Delayed Signals with Segment-Aware Targeting</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Twitch</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>观看、互动、关注与付费在观测时点和用户阶段上含义不同，直接混成一个目标会偏向容易立即得到的信号。即时与延迟模型处理成熟度差异，分群权重表达不同生命周期目标，MMoE 则共享有用专家并保留任务选择。三者针对标签、业务取舍和表示冲突，不能只用一个总体指标证明所有阶段受益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新用户先建立观看习惯，老用户可能更看重深度互动；付费还比点击晚发生。模型分别处理时间与阶段，再通过任务 gate 组合专家，而不是让点击数量压过全部目标。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04455">原论文</a> · <a href="../../../../reproductions/2608.04455-twitch-mor/">实现解读</a> · <a href="#qa-9a6f243fe269c1c1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:llm-ts-prior" data-paper-title="LLM-Derived Priors for Thompson Sampling in Cold-Start Comment Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="LLM-Derived Priors for Thompson Sampling in Cold-Start Comment Recommendation 搜广推与 LLM 应用 NAVER WEBTOON 2026-08-04 主题：LLM 语义先验与冷启动 bandit。新评论缺少交互反馈，但文本已含性别/内容偏好线索。论文把 LLM 语义判断转为 Beta 伪计数，并按性别年龄分群维护 Thompson posterior。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。以 MovieLens genre 代理文本语义，运行分群 Beta prior 与 40 轮 Thompson 在线更新；明确保留负向及不显著结果。  llm-recommendation bandit cold-start comment-ranking 搜广推 学习信号、多任务与反馈偏差 把LLM判断转成Beta伪计数时，为什么先验强度κ和预测概率p一样重要？ 概率决定初始偏好方向，伪计数强度决定新反馈需要多少次才能改变它。κ过大时，错误语义判断可能长期压过真实反馈；过小时又几乎不能缓解冷启动。Thompson采样在后验上探索并持续更新，因此LLM只提供起点而非永久答案；本地分群代理实验不能证明文本先验普遍有效。 示意：两个新内容都得到80%语义先验，一个只相当于几次观察，另一个相当于上千次；出现连续负反馈后，前者很快改变，后者仍可能固执地被推荐。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-llm-ts-prior-97482120" class="ar-learning-paper-anchor"></span>
<h2 id="qa-ff3deba117656c28">把LLM判断转成Beta伪计数时，为什么先验强度κ和预测概率p一样重要？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Allm-ts-prior">LLM-Derived Priors for Thompson Sampling in Cold-Start Comment Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NAVER WEBTOON</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>概率决定初始偏好方向，伪计数强度决定新反馈需要多少次才能改变它。κ过大时，错误语义判断可能长期压过真实反馈；过小时又几乎不能缓解冷启动。Thompson采样在后验上探索并持续更新，因此LLM只提供起点而非永久答案；本地分群代理实验不能证明文本先验普遍有效。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个新内容都得到80%语义先验，一个只相当于几次观察，另一个相当于上千次；出现连续负反馈后，前者很快改变，后者仍可能固执地被推荐。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03382">原论文</a> · <a href="../../../../reproductions/2608.03382-llm-ts-prior/">实现解读</a> · <a href="#qa-ff3deba117656c28">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:twice" data-paper-title="TWICE: Two-Clock, Two-Window Learning for Long-Horizon Conversion Prediction in Online Advertising" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="TWICE: Two-Clock, Two-Window Learning for Long-Horizon Conversion Prediction in Online Advertising 搜广推与 LLM 应用 Kuaishou 2026-07-28 把点击时钟的 current-status 标签与转化时钟的 delay CDF 分开学习，再用曝光窗口权重校正长期未成熟标签。 Fidelity: 核心机制复现。本地执行双时钟、双窗口校正路径和统一评测，私有工业特征与服务未复刻。公开交互代理广告延迟，未包含生产聚合记录和真实 revenue；线上数字只引用论文。本地对照口径：基线为 mature-label next-item CVR，实验组为双时钟 current-status；Hit@10 +8.00%、NDCG@10 +14.31%。  advertising cvr delayed-feedback full-traffic 搜广推 学习信号、多任务与反馈偏差 TWICE 为什么把最终转化概率与 delay CDF 分开学习，而不把未转化样本立刻记为负例？ 观察时尚未转化的样本，可能只是还没等到转化发生。最终概率描述是否会转化，延迟分布描述在给定等待时间内已发生的比例，两者相乘对应当前可观测状态。双时钟与曝光窗口校正减轻标签成熟度差异，但需要合理的延迟建模；公开时间戳代理不能证明真实广告转化延迟被恢复。 示意：刚点击五分钟未买不应与等待一周仍未买等同。模型分别估计最终购买机会与五分钟内完成的比例，让“还没发生”不被直接当作“永远不会发生”。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-twice-bd9f2dd2" class="ar-learning-paper-anchor"></span>
<h2 id="qa-90f01d7ee97d595c">TWICE 为什么把最终转化概率与 delay CDF 分开学习，而不把未转化样本立刻记为负例？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atwice">TWICE: Two-Clock, Two-Window Learning for Long-Horizon Conversion Prediction in Online Advertising</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>观察时尚未转化的样本，可能只是还没等到转化发生。最终概率描述是否会转化，延迟分布描述在给定等待时间内已发生的比例，两者相乘对应当前可观测状态。双时钟与曝光窗口校正减轻标签成熟度差异，但需要合理的延迟建模；公开时间戳代理不能证明真实广告转化延迟被恢复。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>刚点击五分钟未买不应与等待一周仍未买等同。模型分别估计最终购买机会与五分钟内完成的比例，让“还没发生”不被直接当作“永远不会发生”。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25404">原论文</a> · <a href="../../../../reproductions/2607.25404-twice/">实现解读</a> · <a href="#qa-90f01d7ee97d595c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pinequalizer" data-paper-title="PinEqualizer: Full Funnel Content Exploration and Debiasing System at Pinterest" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="PinEqualizer: Full Funnel Content Exploration and Debiasing System at Pinterest 搜广推与 LLM 应用 Pinterest 2026-07-23 新内容缺少协同图和历史互动，生产模型又会依赖已有曝光形成反馈回路。PinEqualizer 不把问题限制在一个排序模型，而是在 corpus selection、召回、精排和 utility 每一级检查 fresh 内容的输入占比与存活率。模型侧加入纯内容/VLM/SID 特征、逐 engagement 特征 dropout、内容—年龄—互动显式交叉、分内容类型 calibration 和 fresh/old 分数正则； Fidelity: 核心机制复现。真实执行 engagement dropout、内容交叉、分 cohort calibration、探索 corpus 与 relevance-scaled UCB；私有多阶段系统由公开代理缩小。MovieLens 的物品首见时间只是新内容代理：fresh 定义为首见时间最新 20%，underexplored 再限制为低于 fresh popularity 中位数。实现没有 Pinterest 的 PinCLIP、SID、商家数据、三大 surface、长期内容 holdout 和实时 Flink 特征；  cold-start exploration debiasing ranking retrieval 搜广推 学习信号、多任务与反馈偏差 PinEqualizer 为什么沿整条分发链检查新内容存活率，而不只在精排里提高新内容分数？ 新内容可能在语料选择或召回阶段已经消失，精排再加分也看不到它。逐级检查输入占比和存活率能定位瓶颈；内容特征、互动特征 dropout 和校准减少模型依赖旧曝光，独立探索与不确定性奖励再补采反馈。探索仍要受相关性约束，否则只奖励低曝光会把不合适内容推给用户。 示意：一篇新食谱在召回前就被过滤，精排加分无济于事。先为新内容保留进入机会，再按相关性和不确定性分配少量探索流量，才能收集判断质量所需的反馈。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-pinequalizer-1595745d" class="ar-learning-paper-anchor"></span>
<h2 id="qa-8ad2cb9fa87f3c82">PinEqualizer 为什么沿整条分发链检查新内容存活率，而不只在精排里提高新内容分数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apinequalizer">PinEqualizer: Full Funnel Content Exploration and Debiasing System at Pinterest</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>新内容可能在语料选择或召回阶段已经消失，精排再加分也看不到它。逐级检查输入占比和存活率能定位瓶颈；内容特征、互动特征 dropout 和校准减少模型依赖旧曝光，独立探索与不确定性奖励再补采反馈。探索仍要受相关性约束，否则只奖励低曝光会把不合适内容推给用户。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一篇新食谱在召回前就被过滤，精排加分无济于事。先为新内容保留进入机会，再按相关性和不确定性分配少量探索流量，才能收集判断质量所需的反馈。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.22518">原论文</a> · <a href="../../../../reproductions/2607.22518-pinequalizer/">实现解读</a> · <a href="#qa-8ad2cb9fa87f3c82">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ramp" data-paper-title="RAMP: Robust Ad Recommendation Under Limited Personalized-Feature Availability via Masking and Alignment Pathways" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="RAMP: Robust Ad Recommendation Under Limited Personalized-Feature Availability via Masking and Alignment Pathways 搜广推与 LLM 应用 Huawei Ireland Research Center / University College Dublin 2026-07-20 隐私选择、权限或平台限制会让同一广告模型在部分流量上拿不到个性化字段。RAMP 不把缺失值简单填零，而是显式维护 personalized 与 non-personalized 两条路径，用可用性 mask 控制输出，并通过 prediction alignment 把富特征路径的知识蒸馏给受限路径。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练 masked 双路径与 prediction alignment；私有工业 CVR 数据未复刻。MovieLens 行为向量代理受限个性化字段、类型特征代理公共广告字段；训练中实际执行双路径、输出 masking 和富特征 teacher 到受限路径的 KL 对齐，测试专门评估无个性化字段流量。  advertising privacy distillation missing-features 搜广推 学习信号、多任务与反馈偏差 RAMP 为什么为缺少个性化字段的流量保留独立路径，而不是统一填零？ 填零会把“字段不可用”与真实零值混为一谈，还要求同一表示同时适应差异很大的输入分布。RAMP 用可用性掩码选择个性化或公共路径，并在训练期把富特征预测对齐给受限路径，让后者学习可迁移知识。受限路径推理仍只用获准字段，蒸馏不能让它恢复原本不可见的个人信息。 示意：用户未授权行为特征时，只走内容与上下文路径；训练时可从有授权样本的丰富预测获得软监督。上线不能为了复制教师分数再偷偷读取缺失的历史字段。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-ramp-9687450e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-228f5bd4932e7220">RAMP 为什么为缺少个性化字段的流量保留独立路径，而不是统一填零？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aramp">RAMP: Robust Ad Recommendation Under Limited Personalized-Feature Availability via Masking and Alignment Pathways</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Ireland Research Center / University College Dublin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>填零会把“字段不可用”与真实零值混为一谈，还要求同一表示同时适应差异很大的输入分布。RAMP 用可用性掩码选择个性化或公共路径，并在训练期把富特征预测对齐给受限路径，让后者学习可迁移知识。受限路径推理仍只用获准字段，蒸馏不能让它恢复原本不可见的个人信息。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户未授权行为特征时，只走内容与上下文路径；训练时可从有授权样本的丰富预测获得软监督。上线不能为了复制教师分数再偷偷读取缺失的历史字段。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.17473">原论文</a> · <a href="../../../../reproductions/2607.17473-ramp/">实现解读</a> · <a href="#qa-228f5bd4932e7220">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:causal-retrieval" data-paper-title="Deep-learning Causal Retrieval Optimization for Efficient e-commerce Distribution in Pinterest" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Deep-learning Causal Retrieval Optimization for Efficient e-commerce Distribution in Pinterest 搜广推与 LLM 应用 Pinterest 2026-07-14 始终触发 shopping candidate generator 浪费资源，也会向无购物意图用户过度分发。论文用随机日志学习多事件 outcome 和 doubly-robust uplift，离线线性 replay 选阈值，线上与远程召回并行执行。 Fidelity: 核心机制复现。执行 propensity、双 outcome、DR pseudo-outcome 和触发阈值。没有 Pinterest randomized logs、购物 session 或 RPC 成本；本地 pseudo-treatment 仅用于可辨识的机制实验。本地对照口径：基线是固定的非因果 transition/content/popularity retrieval ensemble；实验组以 DR uplift 选择约 30% shopping trigger，NDCG@10 0.03540→0.06399，相对 +80.77%。  causal-retrieval uplift candidate-generation 搜广推 学习信号、多任务与反馈偏差 因果召回为什么按触发召回带来的uplift决策，而不是按用户本来的购物概率？ 高购物概率用户可能无需额外召回也会购买，资源应关注触发动作所改变的结果。方法用随机日志学习处理与对照结局，并以doubly-robust校正构造增量估计，再通过replay选择触发阈值。估计仍依赖合适的实验支持与重叠条件，不能把普通预测分换个名字就叫因果收益。 示意：甲本来就会购买，额外召回几乎不改变结局；乙购买概率较低但对合适候选敏感。预算紧张时应比较干预增量，而非只把召回给甲。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-causal-retrieval-c13802af" class="ar-learning-paper-anchor"></span>
<h2 id="qa-188923aec4e8da1a">因果召回为什么按触发召回带来的uplift决策，而不是按用户本来的购物概率？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acausal-retrieval">Deep-learning Causal Retrieval Optimization for Efficient e-commerce Distribution in Pinterest</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>高购物概率用户可能无需额外召回也会购买，资源应关注触发动作所改变的结果。方法用随机日志学习处理与对照结局，并以doubly-robust校正构造增量估计，再通过replay选择触发阈值。估计仍依赖合适的实验支持与重叠条件，不能把普通预测分换个名字就叫因果收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>甲本来就会购买，额外召回几乎不改变结局；乙购买概率较低但对合适候选敏感。预算紧张时应比较干预增量，而非只把召回给甲。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14161">原论文</a> · <a href="../../../../reproductions/2607.14161-causal-retrieval/">实现解读</a> · <a href="#qa-188923aec4e8da1a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:danet" data-paper-title="Cheaper is Better: A Discount-Aware Network for Conversion Rate Prediction in E-commerce Recommendation System" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Cheaper is Better: A Discount-Aware Network for Conversion Rate Prediction in E-commerce Recommendation System 搜广推与 LLM 应用 Alibaba Group / Tmall 2026-07-14 只建模兴趣无法解释“便宜多少”对购买的影响。DANet 的 IPN 捕获一般兴趣；DPN 对 400 天 discount-rate 序列做 FFT 滤波和高低频分解，DCM-User 从相似购买中抽取折扣偏好，DCM-Context 用促销周期 gate 修正分布，并以购买样本的真实折扣做辅助回归。 Fidelity: 核心机制复现。参照作者开源代码执行 IPN、FFT/IFFT、DCM-User、DCM-Context 与折扣回归辅助任务。未使用 Tmall 私有 400 天折扣和促销特征；明确区分作者 TensorFlow 代码与本地 NumPy 复现。本地对照口径：基线是 IPN interest score；实验组 DANet 加入折扣代理的 TFTM/DCM，Hit@10 +0.00%、NDCG@10 -1.46%，fresh Hit@10 +50.00%。  ranking cvr discount 搜广推 学习信号、多任务与反馈偏差 DANet为什么把折扣历史分成高低频，而不只给模型一个当前折扣率？ 相同折扣对不同用户的吸引力不同，当前数值无法表达长期价格敏感度及短期促销反应。DPN从折扣序列中分离较稳定模式与快速波动，再结合相似购买和促销上下文调节偏好；兴趣网络负责另一路需求。购买样本的折扣辅助监督补充信息，但不能由关联直接推出降价因果效应。 示意：有人只在年度大促采购，有人日常也追逐小幅优惠；今天同为八折，两人的历史周期和近期反应不同，模型不应给出完全相同的折扣增益。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-danet-112ada17" class="ar-learning-paper-anchor"></span>
<h2 id="qa-10d7141209c02687">DANet为什么把折扣历史分成高低频，而不只给模型一个当前折扣率？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adanet">Cheaper is Better: A Discount-Aware Network for Conversion Rate Prediction in E-commerce Recommendation System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group / Tmall</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相同折扣对不同用户的吸引力不同，当前数值无法表达长期价格敏感度及短期促销反应。DPN从折扣序列中分离较稳定模式与快速波动，再结合相似购买和促销上下文调节偏好；兴趣网络负责另一路需求。购买样本的折扣辅助监督补充信息，但不能由关联直接推出降价因果效应。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>有人只在年度大促采购，有人日常也追逐小幅优惠；今天同为八折，两人的历史周期和近期反应不同，模型不应给出完全相同的折扣增益。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12578">原论文</a> · <a href="../../../../reproductions/2607.12578-danet/">实现解读</a> · <a href="#qa-10d7141209c02687">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:scalr" data-paper-title="Synthetic Data from Cross-Domain Events for Large-Scale Recommendation Systems" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Synthetic Data from Cross-Domain Events for Large-Scale Recommendation Systems 搜广推与 LLM 应用 Meta 2026-05-29 目标域 conversion 极稀疏，而同一用户在其他产品 surface 上有丰富行为。传统 cross-domain recommendation 把迁移逻辑耦合进模型参数；SCALR 先把 source event 翻译成目标域格式的 synthetic user-item event，再让任何下游模型像读取普通目标域数据一样训练。随机采样保留概率分布和 catalog 多样性，避免 top-k 反复生成少数头部 item。 Fidelity: 核心机制复现。本地从重叠用户估计跨域 item translation distribution，真实生成随机采样与 deterministic top-k 两套 synthetic events，再用相同下游协议比较。本地 genre 不是 Meta 的跨产品 surface，也没有 conversion label、隐私管线或多源生产生成服务。结果只验证概率翻译、随机生成和分布覆盖机制，不能外推论文线上 CVR。本地对照口径：基线为相同 source events、相同每事件生成预算的 deterministic top-k translation，实验组改为 SCALR 概率采样；  cross-domain synthetic-data sampling conversion data-augmentation 搜广推 学习信号、多任务与反馈偏差 SCALR 为什么把跨域迁移变成合成事件，并随机采样目标物品而不是总取 top-k？ 迁移逻辑若写进特定网络，换模型就要重做。SCALR 根据重叠用户估计源事件到目标物品的条件分布，再采样合成目标域事件，供不同下游模型像普通数据一样训练。随机采样保留分布中的长尾机会，避免确定性 top-k 反复复制头部；但合成事件仍是统计迁移，不能冒充实际发生的用户行为。 示意：源域一次旅行浏览对应多个可能的目标域商品。总取最高概率会反复生成行李箱；按分布采样还可能生成转接头或旅行收纳，使训练数据保留更多可能需求。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-scalr-f567c58a" class="ar-learning-paper-anchor"></span>
<h2 id="qa-9e2a137aa9d4e7ec">SCALR 为什么把跨域迁移变成合成事件，并随机采样目标物品而不是总取 top-k？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ascalr">Synthetic Data from Cross-Domain Events for Large-Scale Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>迁移逻辑若写进特定网络，换模型就要重做。SCALR 根据重叠用户估计源事件到目标物品的条件分布，再采样合成目标域事件，供不同下游模型像普通数据一样训练。随机采样保留分布中的长尾机会，避免确定性 top-k 反复复制头部；但合成事件仍是统计迁移，不能冒充实际发生的用户行为。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>源域一次旅行浏览对应多个可能的目标域商品。总取最高概率会反复生成行李箱；按分布采样还可能生成转接头或旅行收纳，使训练数据保留更多可能需求。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.00282">原论文</a> · <a href="../../../../reproductions/2606.00282-scalr/">实现解读</a> · <a href="#qa-9e2a137aa9d4e7ec">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:causal-representation" data-paper-title="Causal Representation Learning for Generalisable Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Causal Representation Learning for Generalisable Recommendation 搜广推与 LLM 应用 University of Warwick 2026-05-26 通过信息论去混杂约束，让候选表征保留与结果有关的因果成分、丢弃由曝光策略带来的非因果成分；训练后不增加线上推理开销。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05220，相对变化 -3.35%。本地代理目标与论文生产任务不同，不能外推线上 lift。  causal-recommendation distribution-shift representation-learning 搜广推 学习信号、多任务与反馈偏差 去掉所有与曝光策略相关的信息，为什么不一定能得到好的因果推荐表征？ 有些信息同时关联曝光与真实结果，完全删除可能连有用信号一起丢掉。方法以信息论目标平衡给定混杂条件后的结果信息和对曝光机制的依赖，争取保留可迁移成分。这里的因果解释依赖混杂变量与识别假设；只看到分布迁移下指标变化，并不足以证明所有非因果成分已被清除。 示意：地域既影响内容曝光，也影响配送可达性，不能因为它关联曝光就一刀切删除；要区分仅反映投放偏好的部分和确实影响结果的部分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-causal-representation-dd23e0e4" class="ar-learning-paper-anchor"></span>
<h2 id="qa-ad3fba55e7e132de">去掉所有与曝光策略相关的信息，为什么不一定能得到好的因果推荐表征？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acausal-representation">Causal Representation Learning for Generalisable Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Warwick</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>有些信息同时关联曝光与真实结果，完全删除可能连有用信号一起丢掉。方法以信息论目标平衡给定混杂条件后的结果信息和对曝光机制的依赖，争取保留可迁移成分。这里的因果解释依赖混杂变量与识别假设；只看到分布迁移下指标变化，并不足以证明所有非因果成分已被清除。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>地域既影响内容曝光，也影响配送可达性，不能因为它关联曝光就一刀切删除；要区分仅反映投放偏好的部分和确实影响结果的部分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.27043">原论文</a> · <a href="../../../../reproductions/2605.27043-causal-representation/">实现解读</a> · <a href="#qa-ad3fba55e7e132de">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pearl-percentile" data-paper-title="PEARL: Unbiased Percentile Estimation via Contrastive Learning for Industrial-Scale Livestream Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="PEARL: Unbiased Percentile Estimation via Contrastive Learning for Industrial-Scale Livestream Recommendation 搜广推与 LLM 应用 TikTok 2026-05-20 用多次对比而不是单个偏置标签估计行为 percentile，并按价值加权、bootstrap 和长期共训练扩展到多个排序目标。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  ranking contrastive-learning debiasing 搜广推 学习信号、多任务与反馈偏差 PEARL 为什么用多次行为对比估计 percentile，而不直接回归原始行为值？ 原始行为值受尺度和偏置影响，不同目标或样本未必可直接比较。把一个行为与多次参考行为比较，可估计它在参考分布中的相对位置；比较次数增加时估计方差下降。价值加权与长期共训练再连接业务目标，但 percentile 仍依赖参考分布，不能把相对排名误当作去除了所有因果偏差的价值。 示意：同样观看三十秒，对十五秒视频和十分钟视频含义不同。与合适参考行为反复比较后，可分别得到在各自分布中的位置；参考群体选错，相对位置仍会误导。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-pearl-percentile-dbf6d244" class="ar-learning-paper-anchor"></span>
<h2 id="qa-4447b64d4565cd98">PEARL 为什么用多次行为对比估计 percentile，而不直接回归原始行为值？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apearl-percentile">PEARL: Unbiased Percentile Estimation via Contrastive Learning for Industrial-Scale Livestream Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · TikTok</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原始行为值受尺度和偏置影响，不同目标或样本未必可直接比较。把一个行为与多次参考行为比较，可估计它在参考分布中的相对位置；比较次数增加时估计方差下降。价值加权与长期共训练再连接业务目标，但 percentile 仍依赖参考分布，不能把相对排名误当作去除了所有因果偏差的价值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同样观看三十秒，对十五秒视频和十分钟视频含义不同。与合适参考行为反复比较后，可分别得到在各自分布中的位置；参考群体选错，相对位置仍会误导。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.21752">原论文</a> · <a href="../../../../reproductions/2605.21752-pearl-percentile/">实现解读</a> · <a href="#qa-4447b64d4565cd98">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dadf" data-paper-title="DADF: A Distribution-Aware Debiasing Framework for Watch-Time Regression in Recommender Systems" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="DADF: A Distribution-Aware Debiasing Framework for Watch-Time Regression in Recommender Systems 搜广推与 LLM 应用 Kuaishou Technology 2026-05-18 冻结成熟的第一阶段 watch-time 模型，按条件分布学习乘性残差校正，并保持线上标量接口不变。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  ranking watch-time debiasing 搜广推 学习信号、多任务与反馈偏差 DADF为什么冻结成熟第一阶段模型，只学习乘性校正因子？ 已有模型包含稳定预测能力，全部重训既可能损坏旧知识，又会改变线上接口。DADF用条件分布信息学习残差比例，让校正随输入及初始预测变化，而仍输出同一种标量。乘性修正适合相对误差，但极小初始预测会使比例不稳定，因此分母保护与条件分布校正不可忽略。 示意：两类用户都被预测看10秒，一类长期被低估、另一类高估；校正器可分别乘上不同系数，而不是给所有用户统一加五秒或重建整套模型。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-dadf-696311de" class="ar-learning-paper-anchor"></span>
<h2 id="qa-3c6b5e2b06c5bf58">DADF为什么冻结成熟第一阶段模型，只学习乘性校正因子？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adadf">DADF: A Distribution-Aware Debiasing Framework for Watch-Time Regression in Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>已有模型包含稳定预测能力，全部重训既可能损坏旧知识，又会改变线上接口。DADF用条件分布信息学习残差比例，让校正随输入及初始预测变化，而仍输出同一种标量。乘性修正适合相对误差，但极小初始预测会使比例不稳定，因此分母保护与条件分布校正不可忽略。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两类用户都被预测看10秒，一类长期被低估、另一类高估；校正器可分别乘上不同系数，而不是给所有用户统一加五秒或重建整套模型。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.17863">原论文</a> · <a href="../../../../reproductions/2605.17863-dadf/">实现解读</a> · <a href="#qa-3c6b5e2b06c5bf58">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ektm" data-paper-title="Effective Knowledge Transfer for Multi-Task Recommendation Models" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Effective Knowledge Transfer for Multi-Task Recommendation Models 搜广推与 LLM 应用 Huawei Technologies 2026-05-07 让 CTR 表示按 CVR 任务相似度向多个转化塔迁移，并以难例感知损失抑制负迁移，保持多任务部署成本可控。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 ektm 核心机制，相对 NDCG@10 +10.98%。  multi-task-learning knowledge-transfer conversion 搜广推 学习信号、多任务与反馈偏差 EKTM为什么按任务相似度迁移CTR表示，而不是让所有转化任务平等共享？ 点击监督较丰富，但不同转化目标与点击的关系不相同，平均共享可能把无关模式灌入稀疏任务。EKTM依据任务关系选择迁移强度，再关注难例以抑制负迁移；共性可被借用，各转化塔仍保留专门目标。相似度是需要学习和验证的信号，不能只因数据量大就把CTR当所有任务的可靠teacher。 示意：加购与点击关系较近，长期续费可能更依赖其他因素；同一份点击表示向两者迁移的力度不应相同，否则容易提高前者却损伤后者。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-ektm-e47d7330" class="ar-learning-paper-anchor"></span>
<h2 id="qa-4e3e011f83fa003d">EKTM为什么按任务相似度迁移CTR表示，而不是让所有转化任务平等共享？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aektm">Effective Knowledge Transfer for Multi-Task Recommendation Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Technologies</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>点击监督较丰富，但不同转化目标与点击的关系不相同，平均共享可能把无关模式灌入稀疏任务。EKTM依据任务关系选择迁移强度，再关注难例以抑制负迁移；共性可被借用，各转化塔仍保留专门目标。相似度是需要学习和验证的信号，不能只因数据量大就把CTR当所有任务的可靠teacher。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>加购与点击关系较近，长期续费可能更依赖其他因素；同一份点击表示向两者迁移的力度不应相同，否则容易提高前者却损伤后者。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.05730">原论文</a> · <a href="../../../../reproductions/2605.05730-ektm/">实现解读</a> · <a href="#qa-4e3e011f83fa003d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pa-bridge" data-paper-title="Bridging Passive and Active: Enhancing Conversation Starter Recommendation via Active Expression Modeling" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Bridging Passive and Active: Enhancing Conversation Starter Recommendation via Active Expression Modeling 搜广推与 LLM 应用 ByteDance 2026-05-07 用分布对齐器把被动浏览行为迁移到主动查询空间，再通过语义离散化和重加权削弱曝光反馈回路，改善 conversation starter 的覆盖与多样性。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04938，相对变化 -8.57%。本地代理目标与论文生产任务不同，不能外推线上 lift。  conversation-starter distribution-alignment debiasing 搜广推 学习信号、多任务与反馈偏差 PA-Bridge 为什么先把被动浏览对齐到主动查询空间，再做语义离散化和重加权？ 被动浏览反映“看过什么”，主动查询更接近“此刻想问什么”，直接复用浏览表示可能推荐熟悉却不适合发起对话的话题。分布对齐连接两种意图空间，离散语义单元和重加权再降低热门曝光反复主导训练的程度。目标是让起始问题更可探索，而不是把高曝光浏览内容原样改写成问题。 示意：用户常被动看到健身短视频，但真正想问的是“膝盖不适怎样调整训练”。对齐到查询空间后，再平衡热门话题权重，有机会提出更贴近行动需求的对话起点。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-pa-bridge-6df7bc67" class="ar-learning-paper-anchor"></span>
<h2 id="qa-a9bfad439e3d5eb0">PA-Bridge 为什么先把被动浏览对齐到主动查询空间，再做语义离散化和重加权？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apa-bridge">Bridging Passive and Active: Enhancing Conversation Starter Recommendation via Active Expression Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>被动浏览反映“看过什么”，主动查询更接近“此刻想问什么”，直接复用浏览表示可能推荐熟悉却不适合发起对话的话题。分布对齐连接两种意图空间，离散语义单元和重加权再降低热门曝光反复主导训练的程度。目标是让起始问题更可探索，而不是把高曝光浏览内容原样改写成问题。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户常被动看到健身短视频，但真正想问的是“膝盖不适怎样调整训练”。对齐到查询空间后，再平衡热门话题权重，有机会提出更贴近行动需求的对话起点。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.05855">原论文</a> · <a href="../../../../reproductions/2605.05855-pa-bridge/">实现解读</a> · <a href="#qa-a9bfad439e3d5eb0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gpl-prerank" data-paper-title="Generative Pseudo-Labeling for Pre-Ranking with LLMs" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Generative Pseudo-Labeling for Pre-Ranking with LLMs 搜广推与 LLM 应用 Alibaba Group / Renmin University 2026-02-24 LLM 从用户行为生成兴趣锚点，为未曝光召回候选产生伪标签；预排序器联合真实与伪监督，且线上不调用 LLM。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 gpl-prerank 核心机制，相对 NDCG@10 +12.84%。  pre-ranking pseudo-labeling llm-recommendation 搜广推 学习信号、多任务与反馈偏差 GPL预排序为什么给未曝光候选补伪标签，而不只对已曝光点击做监督？ 已曝光样本由旧系统筛选，预排器很少看见被早期淘汰候选的有效监督。LLM借用户兴趣锚点对这些候选产生补充标签，帮助模型覆盖旧日志的盲区，服务时仍使用轻量预排器。伪标签是带误差的外部判断，不是反事实真值，需要控制权重并检查它是否放大已有语义偏差。 示意：旧系统从未展示某类相关新品，因此没有点击记录；LLM可提供初步相关性判断来训练预排，但不能把这个判断写成用户已经喜欢或购买的事实。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-gpl-prerank-737de503" class="ar-learning-paper-anchor"></span>
<h2 id="qa-6b23a16668d0204b">GPL预排序为什么给未曝光候选补伪标签，而不只对已曝光点击做监督？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agpl-prerank">Generative Pseudo-Labeling for Pre-Ranking with LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group / Renmin University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>已曝光样本由旧系统筛选，预排器很少看见被早期淘汰候选的有效监督。LLM借用户兴趣锚点对这些候选产生补充标签，帮助模型覆盖旧日志的盲区，服务时仍使用轻量预排器。伪标签是带误差的外部判断，不是反事实真值，需要控制权重并检查它是否放大已有语义偏差。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>旧系统从未展示某类相关新品，因此没有点击记录；LLM可提供初步相关性判断来训练预排，但不能把这个判断写成用户已经喜欢或购买的事实。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.20995">原论文</a> · <a href="../../../../reproductions/2602.20995-gpl-prerank/">实现解读</a> · <a href="#qa-6b23a16668d0204b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unimvt" data-paper-title="Jointly Optimizing Debiased CTR and Uplift for Coupons Marketing: A Unified Causal Framework" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Jointly Optimizing Debiased CTR and Uplift for Coupons Marketing: A Unified Causal Framework 搜广推与 LLM 应用 Kuaishou Technology 2026-02-13 用去混杂表示把基础点击倾向与券强度敏感性分开，再由双预测塔和反事实 X-Network 约束事实/反事实结果；单元 uplift 将不同券档的增量统一到可比较尺度。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.03955，相对变化 -26.76%。本地代理目标与论文生产任务不同，不能外推线上 lift。  causal-recommendation uplift-modeling coupon-marketing 搜广推 学习信号、多任务与反馈偏差 UniMVT 为什么把基础点击倾向与券强度敏感性分开，再比较有券和无券预测？ 高点击用户即使没有券也可能购买，直接用有券转化率排序会把自然倾向误当券增益。分离表示与双塔先建模基础结果和处理结果，反事实约束连接未观测情形，单元 uplift 再统一不同券档的增量尺度。模型结构不能单独建立因果识别，仍依赖处理分配、混杂控制与反事实假设。 示意：甲不用券也有八成购买机会，乙从两成升到五成。按转化率会选甲，按增量更可能选乙；但若发券对象本来就不同，还需控制选择偏差才可解释差值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-unimvt-218d40bb" class="ar-learning-paper-anchor"></span>
<h2 id="qa-5c56d597faaf6232">UniMVT 为什么把基础点击倾向与券强度敏感性分开，再比较有券和无券预测？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunimvt">Jointly Optimizing Debiased CTR and Uplift for Coupons Marketing: A Unified Causal Framework</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>高点击用户即使没有券也可能购买，直接用有券转化率排序会把自然倾向误当券增益。分离表示与双塔先建模基础结果和处理结果，反事实约束连接未观测情形，单元 uplift 再统一不同券档的增量尺度。模型结构不能单独建立因果识别，仍依赖处理分配、混杂控制与反事实假设。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>甲不用券也有八成购买机会，乙从两成升到五成。按转化率会选甲，按增量更可能选乙；但若发券对象本来就不同，还需控制选择偏差才可解释差值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12972">原论文</a> · <a href="../../../../reproductions/2602.12972-unimvt/">实现解读</a> · <a href="#qa-5c56d597faaf6232">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:smes" data-paper-title="SMES: Towards Scalable Multi-Task Recommendation via Expert Sparsity" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="SMES: Towards Scalable Multi-Task Recommendation via Expert Sparsity 搜广推与 LLM 应用 Kuaishou Technology 2026-02-10 把每个任务的激活专家拆为所有任务共享的稳定子集和任务自适应私有子集，并用跨任务全局负载均衡约束路由，控制激活量与专家倾斜。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05359，相对变化 -0.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。  multi-task-learning sparse-moe expert-routing 搜广推 学习信号、多任务与反馈偏差 SMES 为什么既固定共享激活专家，又保留任务自适应私有专家，并做全局负载均衡？ 稳定共享子集承接各任务共性，任务私有选择提供差异化容量，使激活预算不必全花在同一类信息上。跨任务全局平衡防止路由整体拥向少数专家，仅在单任务内部均匀并不能解决总负载倾斜。共享与私有分工是结构约束，专家实际学到什么仍需检查，也要平衡路由自由和均衡惩罚。 示意：点击和购买每次都使用基础兴趣专家，各自再选择新颖性或价格专家。若所有任务私有路由最后都挤向同一台专家，全局均衡会暴露这种跨任务热点。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-smes-9171fefe" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1ed4c7004f28e1f0">SMES 为什么既固定共享激活专家，又保留任务自适应私有专家，并做全局负载均衡？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asmes">SMES: Towards Scalable Multi-Task Recommendation via Expert Sparsity</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>稳定共享子集承接各任务共性，任务私有选择提供差异化容量，使激活预算不必全花在同一类信息上。跨任务全局平衡防止路由整体拥向少数专家，仅在单任务内部均匀并不能解决总负载倾斜。共享与私有分工是结构约束，专家实际学到什么仍需检查，也要平衡路由自由和均衡惩罚。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>点击和购买每次都使用基础兴趣专家，各自再选择新颖性或价格专家。若所有任务私有路由最后都挤向同一台专家，全局均衡会暴露这种跨任务热点。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.09386">原论文</a> · <a href="../../../../reproductions/2602.09386-smes/">实现解读</a> · <a href="#qa-1ed4c7004f28e1f0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:attribution-sets" data-paper-title="Statistical Learning from Attribution Sets" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Statistical Learning from Attribution Sets 搜广推与 LLM 应用 Google Research 2026-02-06 隐私归因场景不提供点击到转化的真实配对，候选集合还可能重叠。方法不采用随机或最大先验伪标签，而将二元损失拆为与标签无关的部分及标签相关矩，再由归因集合统计估计风险。主源定位：v1 §3 Theorem 1、§4.1 Eq6–7。 完整约7,800次、100–200epoch网格成本过高，不复现（审查DONE）。仅使用自建小规模数学夹具。单元素集合在穷举隐藏二元流时匹配真实风险；多元素集合的v1印刷系数未通过常数函数检查。令，原式给出  广告归因与弱监督 风险估计 搜广推 学习信号、多任务与反馈偏差 不知道哪次点击对应转化时，为什么不从归因集合随机选一个点击当正例？ 随机选配对会制造不存在的精确标签，且重叠集合会使同一事件被重复影响。方法转而把二元损失拆成标签无关项与标签相关矩，由集合统计估计风险，不先伪造个体归因。本地发现多元素情形的原文印刷系数未通过常数检查，因此保留反例，不能声称该估计器已被完整验证。 示意：一次购买可能关联三个曝光，其中两个还出现在另一归因集合。随便指定一个获胜者会改变监督含义；用集合统计也需先检查估计式的一致性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-attribution-sets-5c9ffe92" class="ar-learning-paper-anchor"></span>
<h2 id="qa-ae6528b34b9ff368">不知道哪次点击对应转化时，为什么不从归因集合随机选一个点击当正例？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aattribution-sets">Statistical Learning from Attribution Sets</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>随机选配对会制造不存在的精确标签，且重叠集合会使同一事件被重复影响。方法转而把二元损失拆成标签无关项与标签相关矩，由集合统计估计风险，不先伪造个体归因。本地发现多元素情形的原文印刷系数未通过常数检查，因此保留反例，不能声称该估计器已被完整验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次购买可能关联三个曝光，其中两个还出现在另一归因集合。随便指定一个获胜者会改变监督含义；用集合统计也需先检查估计式的一致性。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.06276">原论文</a> · <a href="../../../../recommendation-components/2602.06276-attribution-sets/">实现解读</a> · <a href="#qa-ae6528b34b9ff368">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:easq" data-paper-title="Towards End-to-End Alignment of User Satisfaction via Questionnaire in Video Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Towards End-to-End Alignment of User Satisfaction via Questionnaire in Video Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-01-28 把稀疏问卷满意度监督放入独立 LoRA 参数路径，避免被海量行为标签淹没；在线 DPO 以问卷专家作为动态 reference，持续更新满意度偏好而尽量不扰动主排序干线。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05160，相对变化 -4.46%。本地代理目标与论文生产任务不同，不能外推线上 lift。  satisfaction-alignment preference-learning online-learning 搜广推 学习信号、多任务与反馈偏差 问卷满意度样本很少，EASQ为什么为它保留独立LoRA路径和动态reference？ 海量行为标签容易支配共享更新，使稀疏但直接的满意度监督被淹没。独立低秩路径为问卷知识保留可调空间，在线偏好优化再以问卷专家作动态参照，让更新持续围绕满意度而非只追点击。它降低干扰却不消除问卷抽样偏差，不能把少数答卷直接当全体用户的完整偏好。 示意：许多点击来自猎奇内容，少量问卷却显示用户不满意；独立专家保留这类信号，再引导线上偏好更新，避免点击数量把它全部冲掉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-easq-454991cc" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1f5d8831db260b0a">问卷满意度样本很少，EASQ为什么为它保留独立LoRA路径和动态reference？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aeasq">Towards End-to-End Alignment of User Satisfaction via Questionnaire in Video Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>海量行为标签容易支配共享更新，使稀疏但直接的满意度监督被淹没。独立低秩路径为问卷知识保留可调空间，在线偏好优化再以问卷专家作动态参照，让更新持续围绕满意度而非只追点击。它降低干扰却不消除问卷抽样偏差，不能把少数答卷直接当全体用户的完整偏好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>许多点击来自猎奇内容，少量问卷却显示用户不满意；独立专家保留这类信号，再引导线上偏好更新，避免点击数量把它全部冲掉。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.20215">原论文</a> · <a href="../../../../reproductions/2601.20215-easq/">实现解读</a> · <a href="#qa-1f5d8831db260b0a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:podcast-mtl" data-paper-title="Cold-Starting Podcast Ads and Promotions with Multi-Task Learning on Spotify" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Cold-Starting Podcast Ads and Promotions with Multi-Task Learning on Spotify 搜广推与 LLM 应用 Spotify 2026-01-05 新 podcast 缺少广告点击与播放数据。论文联合训练 ads 和 organic promotions，共享 user/content/context 表征，从数据丰富任务迁移到冷启动任务，并以不平衡处理和梯度平衡抑制 negative transfer。 Fidelity: 核心机制复现。执行 shared low-rank multi-task representation 和冷物品分桶。MovieLens 电影与 genre 代理 podcast/ad 特征，没有 Spotify impression、bid 和曝光校准日志。本地对照口径：基线是 single-task popularity/content ranker；实验组联合 organic/promotion 两任务，NDCG@10 0.03540→0.02810，相对 -20.63%，本地出现 negative transfer。  cold-start multi-task ads 搜广推 学习信号、多任务与反馈偏差 Podcast 多任务学习怎样借自然推广数据帮助缺少广告反馈的新播客，又为什么需要梯度平衡？ 广告与自然推广任务共享用户、内容和上下文表示，使数据较丰富任务提供基础语义与偏好信号；各任务头保留不同的预测目标。样本不平衡和目标冲突可能让强任务压过冷启动任务，因此要调整采样或梯度贡献。共享带来迁移机会，但相关性不足时也会负迁移，不能因共享数据就预设新播客必然受益。 示意：新播客还没有广告点击，却有少量自然推荐播放。共享编码器可先学到它适合哪些听众，再由广告任务头适配广告行为，同时限制大流量任务的梯度压制。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-podcast-mtl-fc67da12" class="ar-learning-paper-anchor"></span>
<h2 id="qa-bf5d9b50db60650a">Podcast 多任务学习怎样借自然推广数据帮助缺少广告反馈的新播客，又为什么需要梯度平衡？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apodcast-mtl">Cold-Starting Podcast Ads and Promotions with Multi-Task Learning on Spotify</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Spotify</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>广告与自然推广任务共享用户、内容和上下文表示，使数据较丰富任务提供基础语义与偏好信号；各任务头保留不同的预测目标。样本不平衡和目标冲突可能让强任务压过冷启动任务，因此要调整采样或梯度贡献。共享带来迁移机会，但相关性不足时也会负迁移，不能因共享数据就预设新播客必然受益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新播客还没有广告点击，却有少量自然推荐播放。共享编码器可先学到它适合哪些听众，再由广告任务头适配广告行为，同时限制大流量任务的梯度压制。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.02306">原论文</a> · <a href="../../../../reproductions/2601.02306-podcast-mtl/">实现解读</a> · <a href="#qa-bf5d9b50db60650a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:click-a-buy-b" data-paper-title="Click A, Buy B: Rethinking Conversion Attribution in E-Commerce Recommendations" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Click A, Buy B: Rethinking Conversion Attribution in E-Commerce Recommendations 搜广推与 LLM 应用 Pinterest 2025-07-20 Last-click attribution 默认点击和购买属于同一商品，忽略用户点 A 后买 B。论文将 Click-A-Buy-A 与 Click-A-Buy-B 分成多任务，并用商品 taxonomy 建模 A/B 的协同归因。 Fidelity: 核心机制复现。实际构造 CABA/CABB 双分支，并按公开 genre taxonomy 学习跨物品协同权重。连续观影不等价于购买；没有真实曝光、归因窗口、广告竞价和 Pinterest taxonomy。本地对照口径：相对 last-click 单物品归因基线，实验组 NDCG@10 +33.70%。  conversion-attribution multi-task-learning taxonomy ads-ranking 搜广推 学习信号、多任务与反馈偏差 用户点击商品A后购买B，为什么不能把购买收益全部当成A自身转化？ 点击对象和购买对象可能不同，last-click同商品归因会漏掉跨商品的影响。论文把Click-A-Buy-A与Click-A-Buy-B分成任务，并借taxonomy表示A与B的类别关系，让模型学习从入口到最终商品的不同路径。这是在改进观测归因与预测，并不自动识别A导致B购买的因果效应。 示意：用户先看入门相机，比较后买了更高型号；若只统计同商品成交，入口相机被当作无价值，实际上它参与了一条跨商品决策路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-click-a-buy-b-aac757e9" class="ar-learning-paper-anchor"></span>
<h2 id="qa-fb5e3facbeeba7ab">用户点击商品A后购买B，为什么不能把购买收益全部当成A自身转化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aclick-a-buy-b">Click A, Buy B: Rethinking Conversion Attribution in E-Commerce Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>点击对象和购买对象可能不同，last-click同商品归因会漏掉跨商品的影响。论文把Click-A-Buy-A与Click-A-Buy-B分成任务，并借taxonomy表示A与B的类别关系，让模型学习从入口到最终商品的不同路径。这是在改进观测归因与预测，并不自动识别A导致B购买的因果效应。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户先看入门相机，比较后买了更高型号；若只统计同商品成交，入口相机被当作无价值，实际上它参与了一条跨商品决策路径。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.15113">原论文</a> · <a href="../../../../reproductions/2507.15113-click-a-buy-b/">实现解读</a> · <a href="#qa-fb5e3facbeeba7ab">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mgoe" data-paper-title="Macro Graph of Experts for Billion-Scale Multi-Task Recommendation" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Macro Graph of Experts for Billion-Scale Multi-Task Recommendation 搜广推与 LLM 应用 Alibaba 2025-06-12 MMoE 只在样本级通过 gate 隐式共享，难表达任务间稳定结构。MGOE 先构建 Macro Task Merging Graph，再由 Macro Graph Bottom/Experts 传播跨任务信息，最后进入任务塔。 Fidelity: 核心机制复现。实际估计多任务相关图，执行宏观图传播 experts 和任务门控预测。公开 proxy 任务远小于工业多目标；没有十亿级 sparse embedding、分布式图构建和阿里线上特征。本地对照口径：相对 MMoE 独立 gate 基线，实验组 NDCG@10 +7.03%。  multi-task-learning mixture-of-experts graph-neural-network ranking 搜广推 学习信号、多任务与反馈偏差 MGOE显式建立任务关系图，相比MMoE的样本级gate增加了什么信息？ MMoE可按样本组合专家，却未必直接表达任务之间较稳定的结构。任务图让相关目标在图底座和专家层传播信息，再由各自任务塔预测，把宏观关系与局部路由分开。图边如果估计错误也会传播负迁移，因此显式关系不等于天然正确，需要检查相邻任务及不相关任务的表现。 示意：点击、加购、购买有较强联系，举报可能关注另一套因素；任务图可控制长期共享路径，而不是要求每个样本的gate从零重学所有任务关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-mgoe-e3468d6f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-7af4301a11225bf7">MGOE显式建立任务关系图，相比MMoE的样本级gate增加了什么信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amgoe">Macro Graph of Experts for Billion-Scale Multi-Task Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>MMoE可按样本组合专家，却未必直接表达任务之间较稳定的结构。任务图让相关目标在图底座和专家层传播信息，再由各自任务塔预测，把宏观关系与局部路由分开。图边如果估计错误也会传播负迁移，因此显式关系不等于天然正确，需要检查相邻任务及不相关任务的表现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>点击、加购、购买有较强联系，举报可能关注另一套因素；任务图可控制长期共享路径，而不是要求每个样本的gate从零重学所有任务关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2506.10520">原论文</a> · <a href="../../../../reproductions/2506.10520-mgoe/">实现解读</a> · <a href="#qa-7af4301a11225bf7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cwm" data-paper-title="Counteracting Duration Bias in Video Recommendation via Counterfactual Watch Time" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Counteracting Duration Bias in Video Recommendation via Counterfactual Watch Time 搜广推与 LLM 应用 Kuaishou Technology / Renmin University of China 2024-06-12 以反事实观看时长估计消除视频时长偏置：区分观察到的 watch time 与在统一时长干预下的潜在收益。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 cwm 核心机制；相对 NDCG@10 -17.89%。  ranking counterfactual-learning watch-time bias 搜广推 学习信号、多任务与反馈偏差 用反事实观看时长打分，为什么比直接比较实际观看秒数更贴近偏好？ 实际观看秒数同时受内容吸引力和视频长度限制，长视频天然有更多累积空间。CWM尝试在统一时长干预下比较潜在观看收益，将机会差异与偏好信号分开。这个估计依赖反事实建模假设，并非简单用秒数除以时长；本地代理机制不能证明已消除真实曝光与时长混杂。 示意：一个短视频被完整看完20秒，另一个长视频看了30秒就划走，直接按秒数会偏向后者；统一观看机会后，二者的偏好排序未必相同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-cwm-65e93cb4" class="ar-learning-paper-anchor"></span>
<h2 id="qa-08cd76fbd0f6979a">用反事实观看时长打分，为什么比直接比较实际观看秒数更贴近偏好？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acwm">Counteracting Duration Bias in Video Recommendation via Counterfactual Watch Time</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology / Renmin University of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>实际观看秒数同时受内容吸引力和视频长度限制，长视频天然有更多累积空间。CWM尝试在统一时长干预下比较潜在观看收益，将机会差异与偏好信号分开。这个估计依赖反事实建模假设，并非简单用秒数除以时长；本地代理机制不能证明已消除真实曝光与时长混杂。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个短视频被完整看完20秒，另一个长视频看了30秒就划走，直接按秒数会偏向后者；统一观看机会后，二者的偏好排序未必相同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2406.07932">原论文</a> · <a href="../../../../reproductions/2406.07932-cwm/">实现解读</a> · <a href="#qa-08cd76fbd0f6979a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ple" data-paper-title="Progressive Layered Extraction (PLE): A Novel Multi-Task Learning Model for Personalized Recommendations" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Progressive Layered Extraction (PLE): A Novel Multi-Task Learning Model for Personalized Recommendations 搜广推与 LLM 应用 Tencent 2020-09-22 MMoE 仍让所有 experts 在所有任务间共享，任务冲突强时难以同时保留共性与个性。PLE 将 experts 分成共享组和任务专属组，通过 CGC 门控逐层提取共享与特定信息，减少跷跷板现象。 复现级别：核心机制复现。复现级别：核心机制复现。实际训练共享/任务专属 experts、CGC gates 和独立 heads；腾讯视频生产规模未复刻。本地对照口径：基线为 MMoE，实验组为共享与任务专属 experts 的 CGC/PLE；平均任务 AUC 相对 +1.34%，见 metrics/movielens-100k-seeds42-44.json。  ranking classic multi-task mixture-of-experts 搜广推 学习信号、多任务与反馈偏差 PLE 相比 MMoE 的独立任务 gate，为什么还显式区分共享专家与任务专属专家？ MMoE 虽可为任务选择不同专家比例，但专家本身仍共同承受各任务梯度。PLE 给任务保留专属专家，同时保留共享专家，再通过逐层门控提取共性与差异，让冲突更强的知识有明确存放位置。它扩展了信息与梯度的隔离结构，代价是更多容量和路由选择；仍需验证是否减少此消彼长的任务退化。 示意：点击和购买可共享品类兴趣专家，购买专属专家学习价格承受能力，点击专属专家学习标题吸引力。门控逐层组合，而不要求全部专家都被两个任务共同改写。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-ple-a2bf42a4" class="ar-learning-paper-anchor"></span>
<h2 id="qa-3abbb3ea731757ca">PLE 相比 MMoE 的独立任务 gate，为什么还显式区分共享专家与任务专属专家？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aple">Progressive Layered Extraction (PLE): A Novel Multi-Task Learning Model for Personalized Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>MMoE 虽可为任务选择不同专家比例，但专家本身仍共同承受各任务梯度。PLE 给任务保留专属专家，同时保留共享专家，再通过逐层门控提取共性与差异，让冲突更强的知识有明确存放位置。它扩展了信息与梯度的隔离结构，代价是更多容量和路由选择；仍需验证是否减少此消彼长的任务退化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>点击和购买可共享品类兴趣专家，购买专属专家学习价格承受能力，点击专属专家学习标题吸引力。门控逐层组合，而不要求全部专家都被两个任务共同改写。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://doi.org/10.1145/3383313.3412236">原论文</a> · <a href="../../../../reproductions/recsys2020-ple-ple/">实现解读</a> · <a href="#qa-3abbb3ea731757ca">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mmoe" data-paper-title="Modeling Task Relationships in Multi-task Learning with Multi-gate Mixture-of-Experts" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Modeling Task Relationships in Multi-task Learning with Multi-gate Mixture-of-Experts 搜广推与 LLM 应用 Google 2018-08-19 共享底座的多任务模型会在任务相关性较低时产生负迁移。完全独立的模型又无法利用共性。MMoE 建立一组共享专家，但为每个任务学习独立 softmax gate，让任务以不同权重组合专家。 复现级别：核心机制复现。复现级别：核心机制复现。实际训练共享 experts、任务专属 gates 与任务 heads；Google 私有业务特征未复刻。本地对照口径：基线为 shared-bottom 双任务网络，实验组为每任务独立 gate 的共享 experts；平均任务 AUC 相对 +1.30%，见 metrics/movielens-100k-seeds42-44.json。  ranking classic multi-task mixture-of-experts 搜广推 学习信号、多任务与反馈偏差 MMoE 共享专家却为每个任务单独设 gate，为什么能缓解共享底座的负迁移？ 共享底座要求任务使用同一份中间表示，目标冲突时梯度会相互拉扯。MMoE 保留一组可共同训练的专家，但每个任务用自己的 gate 按输入组合专家，使相关任务共享有用部分，不相关任务走不同组合。它提供软分工的自由度，并不保证专家天然对应可解释语义或完全消除冲突。 示意：点击与购买都可使用“品类偏好”专家，但购买任务可更重视价格专家，点击任务更重视新鲜感专家。两个任务共享知识，同时避免只能接受同一种混合比例。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-mmoe-a1bda9df" class="ar-learning-paper-anchor"></span>
<h2 id="qa-ad97f0b0fdf40ae7">MMoE 共享专家却为每个任务单独设 gate，为什么能缓解共享底座的负迁移？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ammoe">Modeling Task Relationships in Multi-task Learning with Multi-gate Mixture-of-Experts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共享底座要求任务使用同一份中间表示，目标冲突时梯度会相互拉扯。MMoE 保留一组可共同训练的专家，但每个任务用自己的 gate 按输入组合专家，使相关任务共享有用部分，不相关任务走不同组合。它提供软分工的自由度，并不保证专家天然对应可解释语义或完全消除冲突。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>点击与购买都可使用“品类偏好”专家，但购买任务可更重视价格专家，点击任务更重视新鲜感专家。两个任务共享知识，同时避免只能接受同一种混合比例。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://research.google/pubs/modeling-task-relationships-in-multi-task-learning-with-multi-gate-mixture-of-experts/">原论文</a> · <a href="../../../../reproductions/kdd2018-mmoe-mmoe/">实现解读</a> · <a href="#qa-ad97f0b0fdf40ae7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:esmm" data-paper-title="Entire Space Multi-Task Model: An Effective Approach for Estimating Post-Click Conversion Rate" data-learning-pending="false" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Entire Space Multi-Task Model: An Effective Approach for Estimating Post-Click Conversion Rate 搜广推与 LLM 应用 Alibaba 2018-04-21 CVR 只在点击样本上可观测，直接训练会遭遇 sample-selection bias；转化又远比点击稀疏。ESMM 在全曝光空间同时学习 CTR 与 CVR，并用概率链式分解得到 CTCVR。CTR 的稠密监督帮助 CVR tower 学到更稳定的表示。 复现级别：核心机制复现。复现级别：核心机制复现。实际执行 CTR/CVR 双塔、概率乘积与 entire-space loss；淘宝私有漏斗数据由公开数据构造替代。本地对照口径：基线只在 clicked space 训练 CVR，实验组在 entire space 联合 CTR 与 CTCVR；平均任务 AUC 相对 +1.69%，见 metrics/movielens-100k-seeds42-44.json。  ranking classic multi-task conversion 搜广推 学习信号、多任务与反馈偏差 ESMM为什么训练CTR和CTCVR，却不把未点击样本直接当作CVR负例？ CVR是点击条件下的转化概率，未点击并不能告诉我们点击后会不会买。ESMM用CTR与CVR的乘积表示曝光后点击且转化概率，在全曝光空间监督CTR和联合事件，借漏斗关系缓解稀疏与选择偏差。链式分解是概率关系，不意味着模型自动解决所有归因、延迟反馈或因果识别问题。 示意：点击率10%、点击后购买率20%对应联合率2%；某次未点击只提供点击和联合事件的零标签，不能因此断言这位用户点击后一定不会购买。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-esmm-4cd7f113" class="ar-learning-paper-anchor"></span>
<h2 id="qa-bb787df90c5dc8be">ESMM为什么训练CTR和CTCVR，却不把未点击样本直接当作CVR负例？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aesmm">Entire Space Multi-Task Model: An Effective Approach for Estimating Post-Click Conversion Rate</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>CVR是点击条件下的转化概率，未点击并不能告诉我们点击后会不会买。ESMM用CTR与CVR的乘积表示曝光后点击且转化概率，在全曝光空间监督CTR和联合事件，借漏斗关系缓解稀疏与选择偏差。链式分解是概率关系，不意味着模型自动解决所有归因、延迟反馈或因果识别问题。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>点击率10%、点击后购买率20%对应联合率2%；某次未点击只提供点击和联合事件的零标签，不能因此断言这位用户点击后一定不会购买。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1804.07931">原论文</a> · <a href="../../../../reproductions/1804.07931-esmm/">实现解读</a> · <a href="#qa-bb787df90c5dc8be">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

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

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
