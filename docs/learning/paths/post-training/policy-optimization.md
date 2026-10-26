---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 策略优化：谁在采样，谁在被更新

[LLM 后训练](index.md) / 54 个问题 · 54 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">54 个问题 · 54 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:moer" data-paper-title="MOER: Mix-Policy Optimization under Expert Prefix Guidance with Selective Rollback" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="MOER: Mix-Policy Optimization under Expert Prefix Guidance with Selective Rollback LLM 后训练 City University of Hong Kong 2026-10-22 既有混合策略训练直接加入完整专家解法，可能削弱探索；专家前缀引导虽允许学生续写，却可能把错误续写继续作为监督。MOER 逐步缩短专家 CoT 前缀：成功则保留前缀加续写，失败则回滚到已有的完整、已验证专家轨迹。它把整个引导轨迹都视为 off-policy，包括学生续写部分，并为两类轨迹采用不同目标。 完整实验：成本过高，不复现（审查 DONE），不自动重试。不得用三 seed 将诊断升级为能力复现。本地状态：L1 精确数值组件，diagnostic only。保留 Eq. 1、3–6 与单候选回滚，不是 LLM 训练器、验证器或能力复现。完整实验：成本过高，不复现（审查 DONE），不自动重试。moer.py 独立实现论文公式与单候选回滚。每个 prompt 限定一个已验证 off-policy 行、至少一个 on-policy 行，对应作者主配置 n_prefix=1；调用方提供完整响应 token mask。guided 行的前缀与续写必须都有效，prompt/padding 不参与损失。  后训练算法组件 Mix-policy RL CoT prefix guidance and selective rollback LLM 后训练 策略优化：谁在采样，谁在被更新 MOER里续写由学生生成，为什么整条专家前缀引导轨迹仍按off-policy处理？ 学生是在外部专家前缀条件下续写，整条轨迹并非从无引导学生策略完整采样，因此不能仅按作者身份把后半段归为普通on-policy。MOER成功时保留引导轨迹，失败时回滚到已验证专家轨迹，并使用两类目标；专家信息仅能处于训练边界。 教学例子：老师先写出关键推导，学生接着完成；即使后半段亲自写出，也不能假装学生从空白独立走到了同一状态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-moer-39449a72" class="ar-learning-paper-anchor"></span>
<h2 id="qa-8338e49fb024a4f2">MOER里续写由学生生成，为什么整条专家前缀引导轨迹仍按off-policy处理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amoer">MOER: Mix-Policy Optimization under Expert Prefix Guidance with Selective Rollback</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · City University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>学生是在外部专家前缀条件下续写，整条轨迹并非从无引导学生策略完整采样，因此不能仅按作者身份把后半段归为普通on-policy。MOER成功时保留引导轨迹，失败时回滚到已验证专家轨迹，并使用两类目标；专家信息仅能处于训练边界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>老师先写出关键推导，学生接着完成；即使后半段亲自写出，也不能假装学生从空白独立走到了同一状态。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30873v1">原论文</a> · <a href="../../../../post-training/2610.30873-moer/">实现解读</a> · <a href="#qa-8338e49fb024a4f2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cord" data-paper-title="CORD: Conflict-Aware Optimization for Joint RL and Distillation in Agents" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="CORD: Conflict-Aware Optimization for Joint RL and Distillation in Agents LLM 后训练 The Chinese University of Hong Kong 2026-10-21 任务奖励和教师指导提供不同信号，直接相加会让相反的梯度互相抵消。CORD 不替换 GRPO 或 OPD 的目标，而是明确选择一个 protected objective，最小修改另一个梯度。是否修改由独立的投影 gate 决定：只在冲突时投影，或始终去掉平行分量。两种保护方向、两种 gate 不能混为同一个算法配置。 完整实验成本过高，不复现（审查 DONE）。诊断用两个冲突的交叉熵目标对一个极小 MLP 做三次真实 SGD 更新，验证一般双目标组合公式。L1 梯度组合组件，不是 Agent 能力复现。不可晋级、未接入 Evolve。完整实验成本过高，不复现（审查 DONE）。本篇属于 2026-10-22 新公告，不是将旧候选重记为新论文。combine_gradients 对已汇总向量执行公式；accumulate_gradients 先应用调用方固定的损失聚合权重，再执行一次投影；objective_gradients 从真实 scalar loss 提取参数梯度。  Agentic RL 联合RL与蒸馏梯度优化 LLM 后训练 策略优化：谁在采样，谁在被更新 CORD为什么要先选protected梯度，再对另一个梯度投影？ 投影的含义是尽量保留被保护目标的方向，只最小修改冲突的另一方向；交换保护对象会得到不同更新。还要区分只在冲突时投影与始终投影，并在完整优化批次汇总后操作。得到的是优化器转换前的一阶性质，不保证有限AdamW步后目标必降。 教学例子：任务奖励与教师模仿希望把同一参数往相反方向推。保护任务目标与保护模仿目标，保留下来的方向不会相同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-cord-0b4a5d25" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1ebcba12aeca3711">CORD为什么要先选protected梯度，再对另一个梯度投影？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acord">CORD: Conflict-Aware Optimization for Joint RL and Distillation in Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>投影的含义是尽量保留被保护目标的方向，只最小修改冲突的另一方向；交换保护对象会得到不同更新。还要区分只在冲突时投影与始终投影，并在完整优化批次汇总后操作。得到的是优化器转换前的一阶性质，不保证有限AdamW步后目标必降。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>任务奖励与教师模仿希望把同一参数往相反方向推。保护任务目标与保护模仿目标，保留下来的方向不会相同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.29965v1">原论文</a> · <a href="../../../../post-training/2610.29965-cord/">实现解读</a> · <a href="#qa-1ebcba12aeca3711">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ggpo" data-paper-title="Gibbs-Gap Policy Optimization for Off-Policy RL with Verifiable Rewards" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Gibbs-Gap Policy Optimization for Off-Policy RL with Verifiable Rewards LLM 后训练 University of Illinois Urbana-Champaign 2026-10-14 behavior policy 负责产生样本，reference policy 负责 KL anchor，两者不是同一角色。组内 adjusted reward 全相同时，策略满足该 reference 的 Gibbs 目标。GGPO 用 log-mean-exp 与算术平均的差量度偏离，不给更新乘 learner/behavior importance weight，并周期刷新 reference 以改变后续目标。 完整多 GPU 训练成本过高，不复现（审查 DONE）；L1 objective / refresh 组件及微型策略更新诊断。L1 objective / refresh 组件及微型策略更新诊断。完整多 GPU 训练成本过高，不复现（审查 DONE）；不把规则 verifier 当数学能力证据。公开 Hamlet 1524 固定内容 revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784；  离策略推理 RL 后训练算法组件 GGPO LLM 后训练 策略优化：谁在采样，谁在被更新 GGPO的behavior policy与reference policy为什么不能混为同一个角色？ behavior决定固定样本从哪里来，reference决定KL锚定后的Gibbs目标。GGPO根据调整奖励的log-mean-exp与均值差直接优化，不额外套learner/behavior重要性权重。刷新reference改变后续目标，而不是改写过去采样来源；过滤和归一化后的日志也不能直接套原始理论界。 教学例子：旧模型提供一组回答，新模型相对另一个锚点更新；更换锚点并不会让这批旧回答变成由新模型采样。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-ggpo-409d30ac" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1f2cbda8035e076d">GGPO的behavior policy与reference policy为什么不能混为同一个角色？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aggpo">Gibbs-Gap Policy Optimization for Off-Policy RL with Verifiable Rewards</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>behavior决定固定样本从哪里来，reference决定KL锚定后的Gibbs目标。GGPO根据调整奖励的log-mean-exp与均值差直接优化，不额外套learner/behavior重要性权重。刷新reference改变后续目标，而不是改写过去采样来源；过滤和归一化后的日志也不能直接套原始理论界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>旧模型提供一组回答，新模型相对另一个锚点更新；更换锚点并不会让这批旧回答变成由新模型采样。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20814v1">原论文</a> · <a href="../../../../post-training/2610.20814-ggpo/">实现解读</a> · <a href="#qa-1f2cbda8035e076d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:orl-diffusion" data-paper-title="On-Policy Residual Learning for Diffusion Language Models" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="On-Policy Residual Learning for Diffusion Language Models LLM 后训练 Together AI / University of Illinois Urbana-Champaign 2026-10-14 将上一步预测分布作为残差上下文不是简单后处理：训练时必须看到模型自己诱导的残差轨迹。ORL联合在线采集、状态传输、精确重放及熵收缩，减少训练与推理残差状态分布差异。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地能力指标、训练结果或可执行 Evolve 算子。无本地adapter、指标文件或GPU回执，也不登记可执行Evolve算子。原论文结果仅作为阅读资料。范围见本轮实现与审查合同。本轮只完成方法、资源需求、公开代码状态及原图收录，没有运行完整实验、下载checkpoint或制造模拟能力分数。  扩散语言模型后训练 On-policy学习与蒸馏 LLM 后训练 策略优化：谁在采样，谁在被更新 ORL为什么要求重放模型自己产生的残差状态，而不只训练固定残差输入？ 扩散模型上一步预测会成为下一步残差上下文，误差也沿这条状态路径传播。固定或理想残差训练可能避开推理时真实遇到的状态；在线采集与精确重放让训练面对自身诱导的分布，再结合熵收缩。该机制不是输出后的简单修补，本地尚无完整训练证据。 教学例子：第一轮预测已偏向错误词，第二轮会在这个偏差上继续更新；只用完美残差做训练，可能从未见过这种纠偏情形。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-orl-diffusion-21689257" class="ar-learning-paper-anchor"></span>
<h2 id="qa-fd0685fda98823c0">ORL为什么要求重放模型自己产生的残差状态，而不只训练固定残差输入？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aorl-diffusion">On-Policy Residual Learning for Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Together AI / University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>扩散模型上一步预测会成为下一步残差上下文，误差也沿这条状态路径传播。固定或理想残差训练可能避开推理时真实遇到的状态；在线采集与精确重放让训练面对自身诱导的分布，再结合熵收缩。该机制不是输出后的简单修补，本地尚无完整训练证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第一轮预测已偏向错误词，第二轮会在这个偏差上继续更新；只用完美残差做训练，可能从未见过这种纠偏情形。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20687">原论文</a> · <a href="../../../../post-training/2610.20687-orl-diffusion/">实现解读</a> · <a href="#qa-fd0685fda98823c0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gppo-framework" data-paper-title="Generalized Proximal Policy Optimization: Unifying LLM RL Algorithms from the Perspective of Divergence" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Generalized Proximal Policy Optimization: Unifying LLM RL Algorithms from the Perspective of Divergence LLM 后训练 Tsinghua University AIR 2026-10-09 GPPO把近端优化拆成f-divergence几何和估计拓扑。MC、atomic、binary对采样动作概率/补集的处理不同，诱导实际不同信任域。所有组合参与真实rollout token优化，不是给GRPO换registry名；新key不覆盖已有2508.07629的gppo。 本页不声明未执行实验已经完成。本地对照口径：基线为同checkpoint与配置的GRPO-control；零优势重采样成本显式记录；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Proximal policy optimization f-divergence geometry Probability-aware estimator LLM 后训练 策略优化：谁在采样，谁在被更新 同一个f-divergence换成MC、atomic或binary估计，为何可能得到不同信任域？ 估计方式决定采样动作概率及其补集怎样进入散度，因而相同函数和半径也不必给出相同可行比率区间。GPPO把几何与估计拓扑分开描述，再由实际区间约束策略更新。不能只给GRPO换名称；某些KL写法间的差异也应显式保留而非暗改。 教学例子：一个动作本来极罕见，只约束它自己的比率与同时考虑“其余动作”概率，可能允许不同幅度的概率变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-gppo-framework-a99015aa" class="ar-learning-paper-anchor"></span>
<h2 id="qa-9f37ce2c9a7ea94c">同一个f-divergence换成MC、atomic或binary估计，为何可能得到不同信任域？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agppo-framework">Generalized Proximal Policy Optimization: Unifying LLM RL Algorithms from the Perspective of Divergence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University AIR</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>估计方式决定采样动作概率及其补集怎样进入散度，因而相同函数和半径也不必给出相同可行比率区间。GPPO把几何与估计拓扑分开描述，再由实际区间约束策略更新。不能只给GRPO换名称；某些KL写法间的差异也应显式保留而非暗改。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个动作本来极罕见，只约束它自己的比率与同时考虑“其余动作”概率，可能允许不同幅度的概率变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13015">原论文</a> · <a href="../../../../reproductions/2610.13015-gppo-framework/">实现解读</a> · <a href="#qa-9f37ce2c9a7ea94c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tapo-trajectory" data-paper-title="Trajectory-Aware Policy Optimization: Closing the State Distribution Gap in Long-Horizon LLM RL" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Trajectory-Aware Policy Optimization: Closing the State Distribution Gap in Long-Horizon LLM RL LLM 后训练 Tsinghua University AIR 2026-10-09 autoregressive轨迹的前序policy变化累积state distribution gap。TAPO对token前缀likelihood ratio取几何均值、按长度收紧clipping，并stop-gradient避免前序token反传进当前动作。新key不覆盖已有2607.27973的tapo。 本页不声明未执行实验已经完成。本地对照口径：基线为同checkpoint、采样与优化上限的GRPO-control；不是原Qwen3-8B Avg@8结果；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Trajectory-aware policy optimization Geometric prefix correction Length-aware clipping LLM 后训练 策略优化：谁在采样，谁在被更新 TAPO用前缀几何平均比率后，为什么还要stop-gradient避免跨token反传？ 前缀比率用于衡量累计状态偏移，但当前动作的信用不应经这一权重再回传到所有早期token。TAPO冻结几何平均权重，并让当前动作保留自己的log-prob梯度，避免额外的跨位置梯度和按前缀长度稀释。权重与梯度路径是两个需要分别实现的部分。 教学例子：第十步的前缀已偏离旧策略，需要调整这一动作的权重；不等于这一次损失应该同时重写前九步的信用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-tapo-trajectory-36082418" class="ar-learning-paper-anchor"></span>
<h2 id="qa-dbfc5a17598c40cf">TAPO用前缀几何平均比率后，为什么还要stop-gradient避免跨token反传？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atapo-trajectory">Trajectory-Aware Policy Optimization: Closing the State Distribution Gap in Long-Horizon LLM RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University AIR</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前缀比率用于衡量累计状态偏移，但当前动作的信用不应经这一权重再回传到所有早期token。TAPO冻结几何平均权重，并让当前动作保留自己的log-prob梯度，避免额外的跨位置梯度和按前缀长度稀释。权重与梯度路径是两个需要分别实现的部分。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第十步的前缀已偏离旧策略，需要调整这一动作的权重；不等于这一次损失应该同时重写前九步的信用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13020">原论文</a> · <a href="../../../../reproductions/2610.13020-tapo-trajectory/">实现解读</a> · <a href="#qa-dbfc5a17598c40cf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:zcpo" data-paper-title="When KL Regularization Misfires in Group Policy Optimization" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="When KL Regularization Misfires in Group Policy Optimization LLM 后训练 Alibaba Group 2026-10-08 独立 KL 惩罚可能在奖励相同或奖励梯度取消时继续更新策略。ZCPO 用响应平均的条件 KL 相对漂移，校准组内奖励系数；再将该系数放进原策略 surrogate，不另加独立 KL loss。 实际训练链路和边界检查已实现；24 步单 seed 诊断不是 AIME 收益复现。固定 Qwen3-4B 基础参考，训练 q/v LoRA；group=4、24 步、每响应最多 256 token，8 个独立验证问题。完整词表条件 KL、有效响应 mask、长度平均和 stop-gradient 均实际执行。见运行说明。  组相对策略优化 KL 校准 LLM 后训练 策略优化：谁在采样，谁在被更新 ZCPO为什么把KL放进组内零和系数，而不另外加一项KL loss？ 独立KL项在奖励没有区分或奖励梯度抵消时仍可能推动策略。ZCPO把响应平均条件KL的相对漂移与组内奖励一起中心化，再放入原策略surrogate。奖励尺度为零或组不合格时跳过整组，还需避免优化器权重衰减造成无信号更新，不能只返回零损失。 教学例子：一组回答全得相同奖励，本来没有相对学习方向；额外KL仍可能改模型，所以要明确整组是否真正跳过优化步骤。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-zcpo-1bf32735" class="ar-learning-paper-anchor"></span>
<h2 id="qa-16d59c38f113dc65">ZCPO为什么把KL放进组内零和系数，而不另外加一项KL loss？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Azcpo">When KL Regularization Misfires in Group Policy Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立KL项在奖励没有区分或奖励梯度抵消时仍可能推动策略。ZCPO把响应平均条件KL的相对漂移与组内奖励一起中心化，再放入原策略surrogate。奖励尺度为零或组不合格时跳过整组，还需避免优化器权重衰减造成无信号更新，不能只返回零损失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一组回答全得相同奖励，本来没有相对学习方向；额外KL仍可能改模型，所以要明确整组是否真正跳过优化步骤。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12161">原论文</a> · <a href="../../../../post-training/2610.12161-zcpo/">实现解读</a> · <a href="#qa-16d59c38f113dc65">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gmc-grpo" data-paper-title="Asynchronous LLM Post-Training: Group-Mass Capping and Convergence Analysis" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Asynchronous LLM Post-Training: Group-Mass Capping and Convergence Analysis LLM 后训练 The Ohio State University 2026-10-01 异步 rollout 的重要性比在 group 级统一缩放，使总质量受帽约束；在共同二阶矩保证下减少 trajectory-wise clipping 的持续偏差。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 group mass capping；未搭建异步 RL 集群。执行 group mass capping；未搭建异步 RL 集群。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  异步 RL GRPO 重要性采样 LLM 后训练 策略优化：谁在采样，谁在被更新 GMC-GRPO为什么统一缩放整组重要性比，而不把每条轨迹各自截断？ 逐条截断会不均匀改变组内样本之间的比例。组质量封顶在总比率过大时用同一个因子缩放，保持相对比例而限制总权重。它控制的是组层面质量，仍依赖采样和矩条件；在公式上计算这一步，不代表已经搭建并验证异步训练系统。 教学例子：一组旧轨迹的比率总量过大，统一缩小可保留彼此相对贡献；分别裁平可能让原本不同的重要性看起来一样。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-gmc-grpo-1030f809" class="ar-learning-paper-anchor"></span>
<h2 id="qa-c6f729f6a888dc53">GMC-GRPO为什么统一缩放整组重要性比，而不把每条轨迹各自截断？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agmc-grpo">Asynchronous LLM Post-Training: Group-Mass Capping and Convergence Analysis</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Ohio State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>逐条截断会不均匀改变组内样本之间的比例。组质量封顶在总比率过大时用同一个因子缩放，保持相对比例而限制总权重。它控制的是组层面质量，仍依赖采样和矩条件；在公式上计算这一步，不代表已经搭建并验证异步训练系统。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一组旧轨迹的比率总量过大，统一缩小可保留彼此相对贡献；分别裁平可能让原本不同的重要性看起来一样。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01896">原论文</a> · <a href="../../../../post-training/2610.01896-gmc-grpo/">实现解读</a> · <a href="#qa-c6f729f6a888dc53">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:range-grpo" data-paper-title="Range-GRPO: Policy Optimization via Pairwise Relations among Reward Intervals" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Range-GRPO: Policy Optimization via Pairwise Relations among Reward Intervals LLM 后训练 Yonsei University 2026-10-01 用 conformal reward interval 代替单点 judge 分数；组内只对可确定排序的区间产生方向信号，区间重叠时不制造虚假偏好。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行成对区间关系与 point-limit；不拟合 conformal judge，也不做大模型 GRPO。执行成对区间关系与 point-limit；不拟合 conformal judge，也不做大模型 GRPO。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  GRPO 奖励区间 半监督后训练 LLM 后训练 策略优化：谁在采样，谁在被更新 奖励区间重叠时，Range-GRPO为什么不强行给两条回答排出先后？ 点估计的微小差别可能只是裁判不确定性。Range-GRPO比较校准区间的可确定关系，重叠时不制造方向信号，再在组内聚合相对优势；区间退化为点时回到对应点奖励情形。区间可信性依赖校准协议，只有区间关系算子并不等于已训练可靠judge。 教学例子：两个回答的质量估计范围大幅重叠，不能因一个中心值略高就当作明确优例；先保留无法确定的关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-range-grpo-b66c385f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-58d186d40a148b8d">奖励区间重叠时，Range-GRPO为什么不强行给两条回答排出先后？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arange-grpo">Range-GRPO: Policy Optimization via Pairwise Relations among Reward Intervals</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Yonsei University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>点估计的微小差别可能只是裁判不确定性。Range-GRPO比较校准区间的可确定关系，重叠时不制造方向信号，再在组内聚合相对优势；区间退化为点时回到对应点奖励情形。区间可信性依赖校准协议，只有区间关系算子并不等于已训练可靠judge。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个回答的质量估计范围大幅重叠，不能因一个中心值略高就当作明确优例；先保留无法确定的关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01548">原论文</a> · <a href="../../../../post-training/2610.01548-range-grpo/">实现解读</a> · <a href="#qa-58d186d40a148b8d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rlcpr" data-paper-title="RLCPR: Rethinking Probability-Based Reinforcement Learning From Posterior Concentration" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="RLCPR: Rethinking Probability-Based Reinforcement Learning From Posterior Concentration LLM 后训练 National University of Singapore 2026-10-01 概率奖励在同组推理后验接近时难以区分冗长推理；RLCPR 只对“全组都长、答案后验又集中”的组施加相对长度惩罚。另用直接作答时的 token 平均熵把数据分层，让保留分布偏向低不确定样本。 L1 奖励与课程分布诊断：实现论文集中度门控、长度惩罚和低熵数据分布；L1 奖励与课程分布诊断：实现论文集中度门控、长度惩罚和低熵数据分布；未运行完整语言模型 RL。调用方必须提供真实模型 token 熵、答案后验、长度及策略更新；本地手工输入是公式诊断，不是推理正确率或模型 RL 收益。没有 GPU/Evolve 正式能力集成。PYTHONPATH=src python scripts/run_oct04_seven_papers.py：短且后验分散的组不受惩罚；长且集中的组最长 rollout 惩罚为 -1，最短不罚。低熵样本保留概率约 0.333，高熵约 0.100。见产物。  后验集中与长度约束 强化学习 LLM 后训练 策略优化：谁在采样，谁在被更新 RLCPR为什么只有全组都长且答案后验集中时才加相对长度惩罚？ 后验接近说明这些推理给答案提供的区分有限，全组都长时才有理由压缩相对冗余。门控同时满足后，惩罚依据组内相对长度而非统一固定阈值；等号边界和分位数口径都重要。输入后验与熵须来自真实模型，手工数值只验证公式。 教学例子：同题几条回答都很长且答案概率近似，可尝试偏向较短者；若长回答明显提高答案支持，就不应照样惩罚。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-rlcpr-dde5901c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-524181a96eb45723">RLCPR为什么只有全组都长且答案后验集中时才加相对长度惩罚？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arlcpr">RLCPR: Rethinking Probability-Based Reinforcement Learning From Posterior Concentration</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>后验接近说明这些推理给答案提供的区分有限，全组都长时才有理由压缩相对冗余。门控同时满足后，惩罚依据组内相对长度而非统一固定阈值；等号边界和分位数口径都重要。输入后验与熵须来自真实模型，手工数值只验证公式。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同题几条回答都很长且答案概率近似，可尝试偏向较短者；若长回答明显提高答案支持，就不应照样惩罚。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01458">原论文</a> · <a href="../../../../post-training/2610.01458-rlcpr/">实现解读</a> · <a href="#qa-524181a96eb45723">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sharpening-tax" data-paper-title="Sharpening Tax in Post-Training" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Sharpening Tax in Post-Training LLM 后训练 Meta Superintelligence Labs / University of Wisconsin–Madison 2026-10-01 比较 base 与后训练策略在固定采样预算下的任务覆盖；再用 posterior-tempered group sampling 按估计难度调温，兼顾 pass@1 与覆盖率。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行固定预算覆盖差指标；不运行 Meta 模型或 Agent 环境。执行固定预算覆盖差指标；不运行 Meta 模型或 Agent 环境。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  RL 后训练 覆盖率 Agentic RL LLM 后训练 策略优化：谁在采样，谁在被更新 pass@1提高时，Sharpening Tax为什么仍要比较固定预算下的任务覆盖？ 后训练可能把概率集中到熟悉解法，让一次命中更高，却失去某些只有多次采样才能找到的解。覆盖差比较基座与后训练策略在同一预算能解决哪些任务，再据难度调温。单次准确率、token熵和任务覆盖不是同一指标，不能用一个替代另一个。 教学例子：模型对常见题更确定，但再也采不到一类罕见正确解；只看首个答案的表现，可能完全看不见这部分覆盖损失。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-sharpening-tax-09653801" class="ar-learning-paper-anchor"></span>
<h2 id="qa-7fe59e1e2e6de973">pass@1提高时，Sharpening Tax为什么仍要比较固定预算下的任务覆盖？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asharpening-tax">Sharpening Tax in Post-Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs / University of Wisconsin–Madison</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>后训练可能把概率集中到熟悉解法，让一次命中更高，却失去某些只有多次采样才能找到的解。覆盖差比较基座与后训练策略在同一预算能解决哪些任务，再据难度调温。单次准确率、token熵和任务覆盖不是同一指标，不能用一个替代另一个。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型对常见题更确定，但再也采不到一类罕见正确解；只看首个答案的表现，可能完全看不见这部分覆盖损失。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01509">原论文</a> · <a href="../../../../post-training/2610.01509-sharpening-tax/">实现解读</a> · <a href="#qa-7fe59e1e2e6de973">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:graft" data-paper-title="Learning Beyond What You Sample: Off-Policy-Aware Cross-Model Trajectory Exchange for RLVR" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Learning Beyond What You Sample: Off-Policy-Aware Cross-Model Trajectory Exchange for RLVR LLM 后训练 KAIST 2026-09-29 当 receiver 的 rollout group 全错、peer 在同题同时有成功和失败轨迹时，GRAFT 用完整 peer group 替换无信号组并保留 peer 内部 advantage。跨 tokenizer 的策略错配通过序列平均 log-likelihood compatibility 加权，再用 token importance ratio clipping 限制更新。 复现级别：L1 目标机制。复现级别：L1 目标机制。实现 peer compatibility gate、source advantage 保留与 token ratio clipping。本地目标检查低兼容 peer 被降权、ratio 越界被截断且 advantage 不回传；三种子机制结果见 metrics/mechanism-seeds42-44.json。未进行双模型 GRPO 联训或五个数学 benchmark，故不宣称论文平均 +2.1 分收益。  RLVR 跨模型轨迹交换 离策略校正 LLM 后训练 策略优化：谁在采样，谁在被更新 GRAFT为什么交换同题完整peer组，而不只挑peer的一条成功回答？ receiver全错组缺少区分信号，完整peer组同时保留成功与失败及其内部相对优势。只取成功例会改变组结构和信用。跨模型尤其跨tokenizer时，还需序列兼容性与token比率裁剪处理错配；交换来的数据不能被标成receiver自己的在策略采样。 教学例子：模型甲同题全错，模型乙有对有错。把乙的整组连同组内信用交给甲学习，与单独塞入一份标准答案不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-graft-20b4d98a" class="ar-learning-paper-anchor"></span>
<h2 id="qa-4a8a72e7c33e77d4">GRAFT为什么交换同题完整peer组，而不只挑peer的一条成功回答？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agraft">Learning Beyond What You Sample: Off-Policy-Aware Cross-Model Trajectory Exchange for RLVR</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>receiver全错组缺少区分信号，完整peer组同时保留成功与失败及其内部相对优势。只取成功例会改变组结构和信用。跨模型尤其跨tokenizer时，还需序列兼容性与token比率裁剪处理错配；交换来的数据不能被标成receiver自己的在策略采样。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型甲同题全错，模型乙有对有错。把乙的整组连同组内信用交给甲学习，与单独塞入一份标准答案不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37868">原论文</a> · <a href="../../../../post-training/2609.37868-graft/">实现解读</a> · <a href="#qa-4a8a72e7c33e77d4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rfpo" data-paper-title="Unlocking the Critic: Reward-Free Policy Optimization for LLM Post-Training" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Unlocking the Critic: Reward-Free Policy Optimization for LLM Post-Training LLM 后训练 University of Luxembourg 2026-09-29 冻结已校准 critic，把前缀成功概率同时作为 rollout reward、GAE baseline 和未完成轨迹预报，并在去长度偏置后二值化，降低策略利用 critic 偏差的风险。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行冻结 critic 的去偏、二值奖励与 GAE；未训练长链思维模型。执行冻结 critic 的去偏、二值奖励与 GAE；未训练长链思维模型。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  RL 冻结 Critic 无标签奖励 LLM 后训练 策略优化：谁在采样，谁在被更新 RFPO冻结critic后，为什么还需要去长度偏置和二值化，不能直接最大化它的连续分数？ 冻结只阻止critic参数继续变化，不能消除其评分偏差。策略仍可能通过冗长或其他捷径提高分数，因此方法对前缀成功估计去偏并二值化，同时把critic用于基线和未完成轨迹预报。reward-free不等于无监督来源，而是复用已校准critic提供信号。 教学例子：critic偏爱长推理，学生即使不更正确也可靠加长拿高分；固定critic之后，这个可利用的偏差仍然存在。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-rfpo-964b9a42" class="ar-learning-paper-anchor"></span>
<h2 id="qa-cfcc645e9e1f5910">RFPO冻结critic后，为什么还需要去长度偏置和二值化，不能直接最大化它的连续分数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arfpo">Unlocking the Critic: Reward-Free Policy Optimization for LLM Post-Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Luxembourg</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冻结只阻止critic参数继续变化，不能消除其评分偏差。策略仍可能通过冗长或其他捷径提高分数，因此方法对前缀成功估计去偏并二值化，同时把critic用于基线和未完成轨迹预报。reward-free不等于无监督来源，而是复用已校准critic提供信号。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>critic偏爱长推理，学生即使不更正确也可靠加长拿高分；固定critic之后，这个可利用的偏差仍然存在。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37119">原论文</a> · <a href="../../../../post-training/2609.37119-rfpo/">实现解读</a> · <a href="#qa-cfcc645e9e1f5910">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tlm-dre" data-paper-title="Turn-level Multiscale Density Ratio Estimation for LLM Agents" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Turn-level Multiscale Density Ratio Estimation for LLM Agents LLM 后训练 Alibaba Group 2026-09-15 按 turn 分配多尺度权重，并对正负 token 密度比采用非对称更新。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 turn 权重与非对称 token 更新；未运行真实多轮 Agent 环境。本地执行 turn 权重与非对称 token 更新；未运行真实多轮 Agent 环境。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  多轮 Agent 对齐 密度比估计 LLM 后训练 策略优化：谁在采样，谁在被更新 tlm-DRE为什么提高低置信轮次的权重，而不是给每轮相同惩罚？ 参考策略的长度平均对数概率被用作训练充分程度的估计，低置信轮次获得更高尺度，改变多轮密度比及正负轨迹的不对称训练压力。它依赖置信与学习需求的关系，不声称低概率动作必错；本地仅执行权重与更新诊断，未验证真实Agent泛化。 教学例子：工具选择轮次犹豫、最后复述轮次很确定，可把更多校正压力放在前者；但低置信可能也来自合法的罕见动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-tlm-dre-7ebc851d" class="ar-learning-paper-anchor"></span>
<h2 id="qa-8bf40a276febca62">tlm-DRE为什么提高低置信轮次的权重，而不是给每轮相同惩罚？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atlm-dre">Turn-level Multiscale Density Ratio Estimation for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>参考策略的长度平均对数概率被用作训练充分程度的估计，低置信轮次获得更高尺度，改变多轮密度比及正负轨迹的不对称训练压力。它依赖置信与学习需求的关系，不声称低概率动作必错；本地仅执行权重与更新诊断，未验证真实Agent泛化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>工具选择轮次犹豫、最后复述轮次很确定，可把更多校正压力放在前者；但低置信可能也来自合法的罕见动作。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16760">原论文</a> · <a href="../../../../post-training/2609.16760-tlm-dre/">实现解读</a> · <a href="#qa-8bf40a276febca62">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:mad-rl" data-paper-title="MaD-RL: Matching Distributions for Calibrating LLMs with Reinforcement Learning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="MaD-RL: Matching Distributions for Calibrating LLMs with Reinforcement Learning LLM 后训练 Meta Superintelligence Labs 2026-09-12 逐条最大化正确性奖励可能令输出类别坍缩；MaD-RL为输出的类别频率拟合指定分布，而非仅提高token熵。它将组内频率与目标类别分布构造的L2、forward-KL、reverse-KL或JSD奖励，与任务正确性结合后用于GRPO。完整分布约束与正确性须分别测量。原文§2 完整实验成本过高，不复现（审查 DONE）；既有机制诊断保留，不能升级为原文数学/代码能力复现。Google/Meta优先资料与实验关联。完整实验成本过高，不复现（审查 DONE）；既有机制诊断保留，不能升级为原文数学/代码能力复现。既有实验、三种子结果与负结果仍是事实来源。字符GRU与Qwen3-4B五选项诊断不是原文自由数学/代码任务；Qwen三臂验证完全打平，未观察到分布奖励差异。已有A100回执绑定mad-rl-qwen-choice，不改键、不重新绑定到本资料条目；本轮没有新增CUDA路径或GPU交付。  在线强化学习 类别分布匹配奖励 LLM 后训练 策略优化：谁在采样，谁在被更新 MaD-RL为什么约束输出类别频率，而不是只提高每个token的熵？ token更随机不保证最终类别更均衡。MaD-RL先把输出映射为类别，用经验频率与指定目标分布的差异构造奖励，再与任务正确性结合。频率在该次更新中视为固定，未采到的类别也不会凭空获得on-policy样本；类别判定与无效输出分母必须明确。 教学例子：模型可以用很多不同措辞反复给出同一类别，token多样但决策仍坍缩；应直接检查最终类别分布。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-mad-rl-6dafc52d" class="ar-learning-paper-anchor"></span>
<h2 id="qa-83efe3e396c5af87">MaD-RL为什么约束输出类别频率，而不是只提高每个token的熵？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amad-rl">MaD-RL: Matching Distributions for Calibrating LLMs with Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>token更随机不保证最终类别更均衡。MaD-RL先把输出映射为类别，用经验频率与指定目标分布的差异构造奖励，再与任务正确性结合。频率在该次更新中视为固定，未采到的类别也不会凭空获得on-policy样本；类别判定与无效输出分母必须明确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型可以用很多不同措辞反复给出同一类别，token多样但决策仍坍缩；应直接检查最终类别分布。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.31644">原论文</a> · <a href="../../../../post-training/2609.31644-mad-rl/">实现解读</a> · <a href="#qa-83efe3e396c5af87">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tasco" data-paper-title="Beyond Confidence: Stability-Aware Test-Time Adaptation for LLM Reasoning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Beyond Confidence: Stability-Aware Test-Time Adaptation for LLM Reasoning LLM 后训练 Chongqing University 2026-09-10 冻结主模型，优化轻量 prefix；除置信度外还惩罚邻域扰动下的不稳定，从而避免自信但错误的轨迹。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行随机邻域扰动和稳定性惩罚；没有加载冻结 LLM prefix。本地执行随机邻域扰动和稳定性惩罚；没有加载冻结 LLM prefix。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  测试时适配 稳定性优化 LLM 后训练 策略优化：谁在采样，谁在被更新 TASCO只提高测试题置信度为什么不够，还要检查邻域扰动的稳定性？ 错误答案也可能被模型反复自信确认，仅优化置信会强化这种错误。TASCO冻结主模型，只调轻量前缀，并把邻域扰动下预测不稳定作为额外惩罚。它利用的是无标签稳定性线索，不是正确性oracle；本地扰动诊断没有加载真实LLM前缀。 教学例子：题目换一种等价说法，模型就从一个答案跳到另一个；即使原答案概率很高，这种不稳定也提示不能只按置信强化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-tasco-a3638c7c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-3bf3e360a7863e6c">TASCO只提高测试题置信度为什么不够，还要检查邻域扰动的稳定性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atasco">Beyond Confidence: Stability-Aware Test-Time Adaptation for LLM Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Chongqing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>错误答案也可能被模型反复自信确认，仅优化置信会强化这种错误。TASCO冻结主模型，只调轻量前缀，并把邻域扰动下预测不稳定作为额外惩罚。它利用的是无标签稳定性线索，不是正确性oracle；本地扰动诊断没有加载真实LLM前缀。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>题目换一种等价说法，模型就从一个答案跳到另一个；即使原答案概率很高，这种不稳定也提示不能只按置信强化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11393">原论文</a> · <a href="../../../../post-training/2609.11393-tasco/">实现解读</a> · <a href="#qa-3bf3e360a7863e6c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:probe-erpo" data-paper-title="Entropy-Regularized Rank-Masked Policy Optimization for Test-Time Reinforcement Learning in Code Generation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Entropy-Regularized Rank-Masked Policy Optimization for Test-Time Reinforcement Learning in Code Generation LLM 后训练 Nanyang Technological University 2026-09-08 论文用不依赖最终答案的 probe consistency ratio（PCR）估计当前题目的可信度：高一致样本可强化，低一致样本对排名靠后的候选施加负向约束，同时用熵项控制探索。 复现级别：PCR 已知条件下的策略更新诊断。复现级别：PCR 已知条件下的策略更新诊断。本地不执行论文的代码探针，只验证 PCR 分组后的负排名掩码与熵方向。三种子结果见 metrics/arithmetic-smoke-seeds42-44.json。诊断 fixture 提供 PCR 轴，本地实现低共识候选的负排名 mask 和 entropy direction；没有运行代码执行探针，所以不可把该结果称为完整 TTRL/ERPO。  代码测试时 RL LLM 后训练 策略优化：谁在采样，谁在被更新 Probe-ERPO为什么用不依赖最终答案的探针一致性，低一致时又不直接强化多数答案？ 直接用模型自己的输出当标签可能循环确认错误。输出自由探针提供另一种一致性估计，高一致与低一致分支采用不同更新；低一致时限制排名靠后的候选，并配合熵控制探索。一致性仍不是答案真值，所以不能把探针分数当作有监督正确率。 教学例子：多个相关探针互相矛盾，主答案即使票数最多也不宜盲目强化；可先抑制明显落后的候选，保留进一步探索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-probe-erpo-6a0c336f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-974ed0304580b614">Probe-ERPO为什么用不依赖最终答案的探针一致性，低一致时又不直接强化多数答案？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aprobe-erpo">Entropy-Regularized Rank-Masked Policy Optimization for Test-Time Reinforcement Learning in Code Generation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直接用模型自己的输出当标签可能循环确认错误。输出自由探针提供另一种一致性估计，高一致与低一致分支采用不同更新；低一致时限制排名靠后的候选，并配合熵控制探索。一致性仍不是答案真值，所以不能把探针分数当作有监督正确率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>多个相关探针互相矛盾，主答案即使票数最多也不宜盲目强化；可先抑制明显落后的候选，保留进一步探索。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.09135">原论文</a> · <a href="../../../../post-training/2609.09135-probe-erpo/">实现解读</a> · <a href="#qa-974ed0304580b614">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rlvr-fusion" data-paper-title="Consolidating RLVR Capabilities Across Domains: A Deep Dive into Fusion Paradigms" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Consolidating RLVR Capabilities Across Domains: A Deep Dive into Fusion Paradigms LLM 后训练 Fudan University 2026-08-27 论文统一比较三种复用产物不同的跨域能力融合：Merge 合并专家 task vector，Mix RL 合并训练数据，MOPD 同时复用专家和数据。平均差距不超过 1.4 points，但单项可达 8.6 points，因此选择取决于专家、数据和成本条件。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。公平实现论文三种范式的可审计诊断；本地已有领域专家时执行论文建议的 task-vector Merge，不把三者混成论文没有提出的新目标。本地候选策略不是大模型 checkpoint；只执行“已有 experts”条件下的 Merge，Mix RL/MOPD 作为等预算可审计诊断，不声称复刻论文多模型规模结果。arithmetic-smoke、100 steps：accuracy 0.1953 → 0.2812；同时记录 task-vector cosine、Mix RL advantage 和 MOPD teacher-gap 诊断。  跨领域 RLVR 能力融合 LLM 后训练 策略优化：谁在采样，谁在被更新 RLVR Fusion里的Merge、Mix RL和MOPD为什么不能当作同一种融合操作？ 三者复用的产物不同：Merge组合已有专家的参数增量，Mix RL混合领域数据再训练，MOPD同时利用专家指导与数据。可用专家、数据和预算因此决定可选路线。平均接近不代表各领域相同，也不能用概率向量合并的小实验证明真实checkpoint融合无损。 教学例子：只有两个领域专家权重、没有训练数据时，可讨论参数合并；若只有数据而无专家，则不能假装可以运行同样的蒸馏。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-rlvr-fusion-9745b358" class="ar-learning-paper-anchor"></span>
<h2 id="qa-7a1eadf46dc7ae5e">RLVR Fusion里的Merge、Mix RL和MOPD为什么不能当作同一种融合操作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arlvr-fusion">Consolidating RLVR Capabilities Across Domains: A Deep Dive into Fusion Paradigms</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Fudan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>三者复用的产物不同：Merge组合已有专家的参数增量，Mix RL混合领域数据再训练，MOPD同时利用专家指导与数据。可用专家、数据和预算因此决定可选路线。平均接近不代表各领域相同，也不能用概率向量合并的小实验证明真实checkpoint融合无损。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>只有两个领域专家权重、没有训练数据时，可讨论参数合并；若只有数据而无专家，则不能假装可以运行同样的蒸馏。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27409">原论文</a> · <a href="../../../../post-training/2608.27409-rlvr-fusion/">实现解读</a> · <a href="#qa-7a1eadf46dc7ae5e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ttpo" data-paper-title="TTPO: Test-Time Policy Optimization" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="TTPO: Test-Time Policy Optimization LLM 后训练 Zhejiang University 2026-08-27 多数票伪标签可能错误，但与多数票分歧的 rollout 通常仍是错的。TTPO 因而对同意分支做 OPSD，对分歧分支做 grouped RL，并分别过滤已收敛 token 与高置信错误。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实现多数票路由、同意样本 OPSD、分歧样本 grouped RL 与置信错误筛选。未加载 Qwen checkpoint、未执行真实 test-time rollout；只验证非对称目标和 token 选择路径。arithmetic-smoke 100 steps：accuracy 0.1953 → 0.6328。这是候选策略上的机制隔离，不等同论文数学 benchmark。  测试时强化学习 LLM 后训练 策略优化：谁在采样，谁在被更新 TTPO为什么对同意多数票与反对多数票的回答采用不同目标？ 多数票可能正确也可能错，完全照抄会把误差扩散。TTPO对同意分支使用自蒸馏，对分歧分支采用组式RL，并通过token选择过滤已收敛位置和高置信错误。两条路径利用不同信号，并不把多数票升级为真值，也不允许读取测试金标。 教学例子：几条回答都选同一答案，其中一条反对；不能简单把反对者整段删掉，而要按各分支的目标与可靠性过滤处理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-ttpo-67dfbe79" class="ar-learning-paper-anchor"></span>
<h2 id="qa-69b2a4247c96ba4a">TTPO为什么对同意多数票与反对多数票的回答采用不同目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Attpo">TTPO: Test-Time Policy Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多数票可能正确也可能错，完全照抄会把误差扩散。TTPO对同意分支使用自蒸馏，对分歧分支采用组式RL，并通过token选择过滤已收敛位置和高置信错误。两条路径利用不同信号，并不把多数票升级为真值，也不允许读取测试金标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>几条回答都选同一答案，其中一条反对；不能简单把反对者整段删掉，而要按各分支的目标与可靠性过滤处理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27448">原论文</a> · <a href="../../../../post-training/2608.27448-ttpo/">实现解读</a> · <a href="#qa-69b2a4247c96ba4a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:grin" data-paper-title="From Memorization to Absorption: Mixed-Policy RL for Continual Knowledge Injection" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="From Memorization to Absorption: Mixed-Policy RL for Continual Knowledge Injection LLM 后训练 University of California, Merced 2026-08-26 纯 on-policy RL 在新知识尚未掌握时几乎采不到正确答案。GRIN 在失败组注入 golden response，再以 mixed-policy importance correction 训练；能力提高后自动回到 on-policy 探索。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。本地对照口径：arithmetic-smoke 100 steps，accuracy 0.1250 → 0.3438（+175.00%）；golden answer 是本地候选 oracle。  混合策略知识注入 RL LLM 后训练 策略优化：谁在采样，谁在被更新 GRIN给失败组注入golden response时，为什么必须按混合采样分布校正？ 注入的专家回答并非由无提示当前策略采到，组内数据来自策略与外部来源的混合。以混合分布作分母的校正用于处理这种变化，能力提高后再减少注入、回到探索。gold只属于训练监督，不能让被评估Agent在部署输入中直接读取。 教学例子：学生整组都答错，训练时加入一份已验证解法；可以利用它学习，但不能把这份外部解法记成学生自己探索成功。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-grin-1eaeb543" class="ar-learning-paper-anchor"></span>
<h2 id="qa-3f5bf75743d70577">GRIN给失败组注入golden response时，为什么必须按混合采样分布校正？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agrin">From Memorization to Absorption: Mixed-Policy RL for Continual Knowledge Injection</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Merced</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>注入的专家回答并非由无提示当前策略采到，组内数据来自策略与外部来源的混合。以混合分布作分母的校正用于处理这种变化，能力提高后再减少注入、回到探索。gold只属于训练监督，不能让被评估Agent在部署输入中直接读取。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>学生整组都答错，训练时加入一份已验证解法；可以利用它学习，但不能把这份外部解法记成学生自己探索成功。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25243">原论文</a> · <a href="../../../../post-training/2608.25243-grin/">实现解读</a> · <a href="#qa-3f5bf75743d70577">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:erpo" data-paper-title="Beyond the Stability-Exploration Dilemma: Environmental Regularization for LLM Policy Optimization" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Beyond the Stability-Exploration Dilemma: Environmental Regularization for LLM Policy Optimization LLM 后训练 AMAP, Alibaba Group 2026-08-24 传统 Policy-KL 直接压回答分布，稳定训练的同时消耗探索预算。ERPO 观察到 RL 过程中模型诱导的问题分布也会漂移，于是把正则放到输入侧：用冻结 reference 的问题似然给 query 静态加权，再以 Query-KL 控制环境分布漂移，不直接对 response score function 施压。 复现级别：核心机制 candidate-policy。复现级别：核心机制 candidate-policy。实际执行 reference typicality weight 与 Query-KL，且响应侧 Policy-KL 系数固定为零。本地将 candidate typicality 作为 query-likelihood 代理，验证梯度边界和稳定性控制流；没有训练真实 LLM 或复跑六个论文 benchmark。同一初始 candidate policy、arithmetic-smoke、100 steps、seed 42。基线 accuracy 0.1953，ERPO 0.6094（+212.0%）；  输入侧 Query-KL LLM 后训练 策略优化：谁在采样，谁在被更新 ERPO把正则移到问题分布一侧，和直接限制回答分布有什么区别？ 回答侧KL会直接压制输出变化，稳定训练的同时也限制探索。ERPO用reference的问题似然对query加权，并约束模型诱导的问题分布漂移，改变的是哪些输入获得多少更新压力。它不是把回答KL换个变量名；本地typicality代理也没有验证真实query分布建模。 教学例子：训练持续偏向某类熟题时，可调整问题侧权重；这与要求每个回答都紧贴原模型，是两种不同的约束。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-erpo-0cf15e52" class="ar-learning-paper-anchor"></span>
<h2 id="qa-474029342d1961bb">ERPO把正则移到问题分布一侧，和直接限制回答分布有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aerpo">Beyond the Stability-Exploration Dilemma: Environmental Regularization for LLM Policy Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AMAP, Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>回答侧KL会直接压制输出变化，稳定训练的同时也限制探索。ERPO用reference的问题似然对query加权，并约束模型诱导的问题分布漂移，改变的是哪些输入获得多少更新压力。它不是把回答KL换个变量名；本地typicality代理也没有验证真实query分布建模。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练持续偏向某类熟题时，可调整问题侧权重；这与要求每个回答都紧贴原模型，是两种不同的约束。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.23311">原论文</a> · <a href="../../../../post-training/2608.23311-erpo/">实现解读</a> · <a href="#qa-474029342d1961bb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gcpo" data-paper-title="GCPO: Diagnosing and Constraining Subspace Geometry in Rollout RL for LLMs" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="GCPO: Diagnosing and Constraining Subspace Geometry in Rollout RL for LLMs LLM 后训练 Shanghai AI Laboratory 2026-08-12 GRPO 等 on-policy rollout RL 会偶发进入预训练权重的主奇异子空间，论文观察到这些 spike 常先于验证性能下降。GCPO 固定预训练矩阵两侧的 top-k 奇异空间，只允许低秩更新存在于输入、输出两侧的正交补中；这是硬可行域，不是依赖系数的软 penalty。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实际计算 rollout update 的主子空间重合，并把 policy update 投影到互补子空间；线性策略不是论文矩阵层的完整双侧 LoRA。本地 policy 参数是向量，因此以 empirical update covariance 的主右奇异空间实现等价正交限制；未声称复刻 Qwen3-8B/GLM4-9B 的逐层矩阵双侧 LoRA、三 seed 或论文 benchmark。本地对照口径：基线为同一随机初始化 candidate policy 训练前；  几何约束 RL LLM 后训练 策略优化：谁在采样，谁在被更新 GCPO为什么把低秩更新投影到左右奇异空间的正交补，而不只惩罚投影大小？ 软惩罚允许优化用足够大收益换取主子空间漂移，双侧投影则把这类更新从可行域中直接排除。固定预训练主奇异空间后，输入和输出两侧都受约束，目标是减少覆盖已有主映射。向量级诊断并不等同真实逐层矩阵LoRA训练。 教学例子：若某个权重矩阵的主要输入输出方向需要保护，只在损失里罚它仍可被突破；双侧投影要求每次有效更新都避开这些方向。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-gcpo-c679efe1" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b228873198b3173b">GCPO为什么把低秩更新投影到左右奇异空间的正交补，而不只惩罚投影大小？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agcpo">GCPO: Diagnosing and Constraining Subspace Geometry in Rollout RL for LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai AI Laboratory</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>软惩罚允许优化用足够大收益换取主子空间漂移，双侧投影则把这类更新从可行域中直接排除。固定预训练主奇异空间后，输入和输出两侧都受约束，目标是减少覆盖已有主映射。向量级诊断并不等同真实逐层矩阵LoRA训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>若某个权重矩阵的主要输入输出方向需要保护，只在损失里罚它仍可被突破；双侧投影要求每次有效更新都避开这些方向。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.11674">原论文</a> · <a href="../../../../post-training/2608.11674-gcpo/">实现解读</a> · <a href="#qa-b228873198b3173b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:erils" data-paper-title="Beyond On-Policy Exploration: Integrating External Policy Rollouts for Reinforcement Learning in Diffusion Language Models" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Beyond On-Policy Exploration: Integrating External Policy Rollouts for Reinforcement Learning in Diffusion Language Models LLM 后训练 Seoul National University 2026-08-03 约束外部策略 rollout 长度，并对 on-policy/external 来源分别处理奖励以防联合归一化崩溃。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  外部 rollout Diffusion LM RL LLM 后训练 策略优化：谁在采样，谁在被更新 ERILS为什么分别处理自身与外部rollout的奖励，而不把它们直接拼组归一化？ 不同来源的长度与奖励分布可能不同，联合归一化会把来源差异混成优势，使一类样本支配或失去信号。ERILS限制外部轨迹长度并分来源处理奖励，保留外部探索价值。来源分组不自动消除所有离策略误差，仍需按实际目标解释采样口径。 教学例子：外部策略总写更长、更高分的回答，直接与学生短回答混组，可能让所有学生样本都变负；应先识别来源差异。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-erils-07f1d788" class="ar-learning-paper-anchor"></span>
<h2 id="qa-671320bb53b7dd5a">ERILS为什么分别处理自身与外部rollout的奖励，而不把它们直接拼组归一化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aerils">Beyond On-Policy Exploration: Integrating External Policy Rollouts for Reinforcement Learning in Diffusion Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Seoul National University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同来源的长度与奖励分布可能不同，联合归一化会把来源差异混成优势，使一类样本支配或失去信号。ERILS限制外部轨迹长度并分来源处理奖励，保留外部探索价值。来源分组不自动消除所有离策略误差，仍需按实际目标解释采样口径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>外部策略总写更长、更高分的回答，直接与学生短回答混组，可能让所有学生样本都变负；应先识别来源差异。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01717">原论文</a> · <a href="../../../../post-training/2608.01717-erils/">实现解读</a> · <a href="#qa-671320bb53b7dd5a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:reco-grpo" data-paper-title="ReCo" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="ReCo LLM 后训练 Seoul National University 2026-07-29 GRPO 容易重复采到高概率回答，并继续放大已经占优的 token，导致大下推理路径覆盖率下降。ReCo 同时修正 response 和 token：按 rollout 组中的期望出现次数抑制高频回答，再用 Bernoulli 方差比把更新集中到尚未饱和的决策点。 这是 objective-level 机制复现，不是 Qwen/Llama 全参数 RLVR；本地候选动作代理完整 response，无法等价报告 Pass@64 或自然语言 Self-BLEU。candidate-policy mini-suite 中同时执行期望出现次数权重、方差比、PPO clip、KL 和每 16 步 rollout-policy refresh。  分布保持 RL LLM 后训练 策略优化：谁在采样，谁在被更新 ReCo为什么既抑制高频回答，又按token的Bernoulli方差调整更新？ 响应级重复会让热门解法反复占据样本，token级饱和又会继续放大已占优决策。两项分别校正组内期望出现次数和局部决策的可塑性，不能相互替代。保持覆盖的目标也不等于追求任意随机性，本地候选概率不能代表真实长文本路径覆盖。 教学例子：多次采样都得到同一句模板，末尾选择也几乎确定；只减少重复回答权重，未必能避免饱和token继续主导更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-reco-grpo-97f782ad" class="ar-learning-paper-anchor"></span>
<h2 id="qa-24eff40b49e92f55">ReCo为什么既抑制高频回答，又按token的Bernoulli方差调整更新？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Areco-grpo">ReCo</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Seoul National University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>响应级重复会让热门解法反复占据样本，token级饱和又会继续放大已占优决策。两项分别校正组内期望出现次数和局部决策的可塑性，不能相互替代。保持覆盖的目标也不等于追求任意随机性，本地候选概率不能代表真实长文本路径覆盖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>多次采样都得到同一句模板，末尾选择也几乎确定；只减少重复回答权重，未必能避免饱和token继续主导更新。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26862">原论文</a> · <a href="../../../../post-training/2607.26862-reco/">实现解读</a> · <a href="#qa-24eff40b49e92f55">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:code-optimization-rl" data-paper-title="Reinforcement Learning for Code Optimization" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Reinforcement Learning for Code Optimization LLM 后训练 FAIR at Meta / Inria 2026-07-28 代码正确不等于运行快；直接加入耗时奖励会被小测试、共享worker负载和稀疏优势淹没。作者构造DMC-Optim，用独立服务校准时长，再组合正确性、优化测试和人类参考百分位。先离线回放筛选奖励与环境，在线GRPO另处理稀疏奖励与过旧批次。原文§3–5、附录C–F 成本过高，不复现（审查 DONE）；Google/Meta优先补漏资料。成本过高，不复现（审查 DONE）；没有新增训练、CUDA路径或evolve接入。原文每次在线RL运行使用8至32个GPU节点、数小时至数天，且依赖独立代码执行服务，显著超出单A100/A30或Mac预算。成本过高，不复现（审查 DONE）；不下载checkpoint、不训练，不用CPU计时fixture替代完整算法。  在线强化学习 代码效率奖励与执行校准 LLM 后训练 策略优化：谁在采样，谁在被更新 代码优化RL为什么先校准计时环境，再把耗时加入奖励？ 共享worker负载和小测试波动会让同一程序测得不同速度，策略可能学会利用计时噪声而非优化程序。独立沙箱计时、正确性门控与优化测试共同界定速度奖励，再处理稀疏优势和旧批次。通过语法或小夹具不能证明生产代码更快。 教学例子：一份程序恰好在空闲机器上跑得快，不应因此压过真正更高效的版本；先做同条件重复计时，再比较合法程序。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-code-optimization-rl-602974e9" class="ar-learning-paper-anchor"></span>
<h2 id="qa-2d56a2f3fb13d993">代码优化RL为什么先校准计时环境，再把耗时加入奖励？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acode-optimization-rl">Reinforcement Learning for Code Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta / Inria</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共享worker负载和小测试波动会让同一程序测得不同速度，策略可能学会利用计时噪声而非优化程序。独立沙箱计时、正确性门控与优化测试共同界定速度奖励，再处理稀疏优势和旧批次。通过语法或小夹具不能证明生产代码更快。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一份程序恰好在空闲机器上跑得快，不应因此压过真正更高效的版本；先做同条件重复计时，再比较合法程序。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25970">原论文</a> · <a href="../../../../post-training/2607.25970-code-optimization-rl/">实现解读</a> · <a href="#qa-2d56a2f3fb13d993">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:iso-rlvr" data-paper-title="ISO: An RLVR-Native Optimization Stack" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="ISO: An RLVR-Native Optimization Stack LLM 后训练 The University of Texas at Austin 2026-07-21 固定预训练权重奇异值，仅优化输入/输出 singular frames；同时提供无数据 specialist merger。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  RLVR 优化器 LLM 后训练 策略优化：谁在采样，谁在被更新 ISO固定奇异值只优化singular frames，和普通低秩增量训练有什么不同？ 固定谱把参数变化限制为输入与输出奇异方向的调整，而非自由改变所有幅度或任意加一个低秩矩阵。这个约束影响可达权重集合，也为专家合并提供结构。只验证小矩阵或候选策略上的保持性质，不能据此声称完整模型优化栈已被复现。 教学例子：同一组奇异值对应的矩阵仍可因方向旋转而改变映射；因此“谱不变”不意味着模型行为不变，也不等于参数被冻结。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-iso-rlvr-42a6dc22" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d6e53e6e465caeee">ISO固定奇异值只优化singular frames，和普通低秩增量训练有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aiso-rlvr">ISO: An RLVR-Native Optimization Stack</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The University of Texas at Austin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定谱把参数变化限制为输入与输出奇异方向的调整，而非自由改变所有幅度或任意加一个低秩矩阵。这个约束影响可达权重集合，也为专家合并提供结构。只验证小矩阵或候选策略上的保持性质，不能据此声称完整模型优化栈已被复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一组奇异值对应的矩阵仍可因方向旋转而改变映射；因此“谱不变”不意味着模型行为不变，也不等于参数被冻结。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.19331">原论文</a> · <a href="../../../../post-training/2607.19331-iso-rlvr/">实现解读</a> · <a href="#qa-d6e53e6e465caeee">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:off-context-grpo" data-paper-title="Off-Context GRPO: Learning to Reason on Hard Problems using Privileged Information" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Off-Context GRPO: Learning to Reason on Hard Problems using Privileged Information LLM 后训练 Meta AI 2026-07-21 困难题上 vanilla GRPO 常因整组 rollout 都失败而没有有效优势信号。Off-Context GRPO 只在采样时向 behavior policy 提供解题草稿或提示等 privileged information，提高成功轨迹出现率；优化目标仍是原始无提示 policy，并用 importance ratio 校正两种采样分布的偏差，因此推理时不需要特权上下文。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实执行 privileged rollout 和 importance correction；Qwen2.5 大模型规模未复刻。脚本下载并使用官方 GSM8K。vanilla GRPO 从原问题采样；OC-GRPO 从包含官方解题过程的 behavior distribution 采样，计算 exact-answer reward、group-relative advantage 和 target/behavior importance correction。  rlvr grpo reasoning privileged-information LLM 后训练 策略优化：谁在采样，谁在被更新 Off-Context GRPO采样时给提示，为什么优化与推理却仍使用无提示策略？ 提示用于提高困难题成功轨迹的出现率，采样行为分布因此不同于目标策略。训练用无提示策略概率与带特权行为概率的比值校正，而不是训练一个依赖提示才能运行的模型。忽略分母或把提示留在评测输入中，都会改变方法所声称的任务。 教学例子：训练教师给出一段草稿帮助采到正确续写；更新时学生仍只条件于原题，测试时也不能把那段草稿偷偷保留。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-off-context-grpo-ccd1608e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-5a3ebe3e47f8ed51">Off-Context GRPO采样时给提示，为什么优化与推理却仍使用无提示策略？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aoff-context-grpo">Off-Context GRPO: Learning to Reason on Hard Problems using Privileged Information</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>提示用于提高困难题成功轨迹的出现率，采样行为分布因此不同于目标策略。训练用无提示策略概率与带特权行为概率的比值校正，而不是训练一个依赖提示才能运行的模型。忽略分母或把提示留在评测输入中，都会改变方法所声称的任务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练教师给出一段草稿帮助采到正确续写；更新时学生仍只条件于原题，测试时也不能把那段草稿偷偷保留。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.19313">原论文</a> · <a href="../../../../reproductions/2607.19313-off-context-grpo/">实现解读</a> · <a href="#qa-5a3ebe3e47f8ed51">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ripo" data-paper-title="RIPO" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="RIPO LLM 后训练 Tsinghua University 2026-07-11 固定 PPO ratio 区间在低概率区域过于保守、在高概率区域又可能过大。RIPO 以 Fisher–Rao 几何定义策略距离，并按旧策略概率设置等距 clip 半径，使不同概率区域获得更均衡的局部 KL 预算。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。候选动作概率替代 token 分布，验证动态 clip 与梯度路径，不复刻论文的全参数长 CoT 训练。在 GSM8K candidate-policy 上实际执行依旧概率相关的 Fisher–Rao clip、组内优势和旧 rollout policy 刷新，并记录各样本动态半径。  几何信任域 LLM 后训练 策略优化：谁在采样，谁在被更新 相同PPO ratio区间在不同旧概率处，为什么不代表相同的策略距离？ 概率空间的几何随旧概率位置改变，罕见动作与高概率动作的相同比率变化会消耗不同局部KL预算。RIPO依据Fisher–Rao距离设置概率相关半径，试图让约束更可比。它改变裁剪边界而非优势标签，仍需用实际更新验证稳定性。 教学例子：把一个极少见动作的概率翻倍与把常见动作概率翻倍，对其余分布的影响不同；统一比率上限并不几何等距。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-ripo-458e77e0" class="ar-learning-paper-anchor"></span>
<h2 id="qa-925d5b7d5f114e23">相同PPO ratio区间在不同旧概率处，为什么不代表相同的策略距离？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aripo">RIPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>概率空间的几何随旧概率位置改变，罕见动作与高概率动作的相同比率变化会消耗不同局部KL预算。RIPO依据Fisher–Rao距离设置概率相关半径，试图让约束更可比。它改变裁剪边界而非优势标签，仍需用实际更新验证稳定性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把一个极少见动作的概率翻倍与把常见动作概率翻倍，对其余分布的影响不同；统一比率上限并不几何等距。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.10169">原论文</a> · <a href="../../../../post-training/2607.10169-ripo/">实现解读</a> · <a href="#qa-925d5b7d5f114e23">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sis" data-paper-title="Turning Off-Policy Tokens On-Policy: A Plug-in Approach for Improving LLM Alignment" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Turning Off-Policy Tokens On-Policy: A Plug-in Approach for Improving LLM Alignment LLM 后训练 Renmin University of China 2026-07-06 异步 rollout、样本复用和 stale policy 会让 LLM 强化学习变成 off-policy 更新。标准 importance sampling（IS）在长序列上连乘后方差很大，直接 clipping 又会丢失有效梯度。SIS 将 token 级 rejection sampling 插入 GRPO、DAPO、GSPO：被接受的旧策略 token 可视为来自当前策略，其 IS ratio 直接置 1；未接受 token 仍交给原算法处理。 Fidelity: 核心机制复现。SIS 的 off-policy token 变换按论文公式实际执行；Qwen3 上的完整 RL 后训练不在本地实验中。本地对照口径：基线是标准 token-level Importance Sampling；实验组是 SIS ratio transformation；importance-weight variance 平均 -6.62%。这是 off-policy estimator 比较，DIN 与推荐排序指标均不适用。  post-training off-policy-correction importance-sampling LLM 后训练 策略优化：谁在采样，谁在被更新 SIS接受旧token后为什么把ratio置1，这是否意味着整条旧轨迹都变成on-policy？ 拒绝采样在给定前缀下校正被接受动作的条件分布，理想条件下这部分无需再乘原重要性比；未接受token仍由宿主算法处理。它不把整条旧轨迹自动改成当前策略轨迹，且top-K envelope是工程近似，必须与精确采样保证区分。 教学例子：一条旧回答只有部分位置通过接受检验，不能因为其中一个token被接受，就把整段历史的全部比率都改成一。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-sis-7add6071" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1196d9cfe453f499">SIS接受旧token后为什么把ratio置1，这是否意味着整条旧轨迹都变成on-policy？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asis">Turning Off-Policy Tokens On-Policy: A Plug-in Approach for Improving LLM Alignment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Renmin University of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>拒绝采样在给定前缀下校正被接受动作的条件分布，理想条件下这部分无需再乘原重要性比；未接受token仍由宿主算法处理。它不把整条旧轨迹自动改成当前策略轨迹，且top-K envelope是工程近似，必须与精确采样保证区分。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一条旧回答只有部分位置通过接受检验，不能因为其中一个token被接受，就把整段历史的全部比率都改成一。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.04728">原论文</a> · <a href="../../../../reproductions/2607.04728-sis/">实现解读</a> · <a href="#qa-1196d9cfe453f499">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:stare" data-paper-title="STARE" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="STARE LLM 后训练 Tsinghua University 2026-06-17 按 batch surprisal 分位数识别 entropy-critical token，重加权其 advantage，并以目标 entropy 闭环 gate 调节方向。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。Arithmetic candidate suite、120 steps、seed 42：accuracy 0.2344 → 0.5312（+126.67%）。  Entropy 稳定 LLM 后训练 策略优化：谁在采样，谁在被更新 STARE为什么同时看token surprisal和整体熵目标，而不一律强化意外token？ 高surprisal位置可能对熵变化更敏感，但持续放大它们也可能让策略过度发散。STARE先按batch分位识别关键位置，再依据当前熵与目标熵的差异调节优势权重。意外程度不是正确性，门控旨在控制训练动态，不是把罕见词都标成好动作。 教学例子：同样一个低概率token，在策略过度确定时与已经过度随机时，可能需要不同调节方向；不能永远给它额外正权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-stare-ca64b168" class="ar-learning-paper-anchor"></span>
<h2 id="qa-faaef258a6b76c26">STARE为什么同时看token surprisal和整体熵目标，而不一律强化意外token？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Astare">STARE</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>高surprisal位置可能对熵变化更敏感，但持续放大它们也可能让策略过度发散。STARE先按batch分位识别关键位置，再依据当前熵与目标熵的差异调节优势权重。意外程度不是正确性，门控旨在控制训练动态，不是把罕见词都标成好动作。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同样一个低概率token，在策略过度确定时与已经过度随机时，可能需要不同调节方向；不能永远给它额外正权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.19236">原论文</a> · <a href="../../../../post-training/2606.19236-stare/">实现解读</a> · <a href="#qa-faaef258a6b76c26">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:kpop" data-paper-title="KPop" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="KPop LLM 后训练 Ling / Ring Team 2026-06-13 异步 rollout 中的 serving 概率与训练侧概率失配，固定 ratio mask 会误删正常探索或保留错误梯度。KPop 将当前 token 与“其余词表”压缩为二元分布，只有正反两个方向的 binary KL 都低于阈值时才保留该 token 的更新。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。没有真实训推引擎、MoE routing 或万亿参数异步集群；本地只验证 binary-KL mask 的可审计更新语义。在候选策略的 rollout/训练双分布上计算双向 binary KL，并让 mask 真正决定每个采样动作是否产生 policy gradient。  异步训推失配 LLM 后训练 策略优化：谁在采样，谁在被更新 KPop为什么比较token与其余词表的双向binary KL，而不只判断ratio是否过大？ 相同比率在不同基础概率下含义不同，二元分布同时考虑当前token及其补集，更能反映局部概率变化。正反KL还具有不对称性，因此两边都过关才保留更新。这个掩码检验训推概率一致性，不证明留下的动作正确或整个异步系统无偏。 教学例子：一个罕见词与一个常见词都出现相同比率偏移，仅看ratio会同等处理；加入其余词表概率后，几何差异才显现。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-kpop-03b1bc3e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d03b1e6d172879e3">KPop为什么比较token与其余词表的双向binary KL，而不只判断ratio是否过大？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Akpop">KPop</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ling / Ring Team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相同比率在不同基础概率下含义不同，二元分布同时考虑当前token及其补集，更能反映局部概率变化。正反KL还具有不对称性，因此两边都过关才保留更新。这个掩码检验训推概率一致性，不证明留下的动作正确或整个异步系统无偏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个罕见词与一个常见词都出现相同比率偏移，仅看ratio会同等处理；加入其余词表概率后，几何差异才显现。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.15079">原论文</a> · <a href="../../../../post-training/2606.15079-kpop/">实现解读</a> · <a href="#qa-d03b1e6d172879e3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gprl" data-paper-title="GPRL" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="GPRL LLM 后训练 Stanford University 2026-05-18 单一标量 reward 容易掩盖 helpfulness、格式、推理和简洁度之间的冲突。GPRL 先在每个偏好维度内部计算 group-relative advantage，再根据上下文聚合；漂移控制器检测某个维度是否主导训练并调整权重。 保真度：本地实现逐维 group normalization、动态聚合和漂移监控；保真度：本地实现逐维 group normalization、动态聚合和漂移监控；候选式 GSM8K 主要验证算法状态，不覆盖论文的开放式多维 judge。当前没有接入 AlpacaEval judge、开放式生成或真实人类多维偏好。GPRL 低于 DPO/OPD 的 exact-answer accuracy 是已记录的负结果，不代表论文的多维开放式结论已被否定。本地 reward 轴为 outcome、format、reasoning、brevity；每轴独立标准化并记录漂移事件。  多目标 RL LLM 后训练 策略优化：谁在采样，谁在被更新 GPRL为什么逐偏好维度算组内优势，再按上下文聚合？ 直接相加原始奖励会让量纲大或方差大的维度支配训练，掩盖帮助性、格式与简洁性的冲突。逐维标准化先获得可比信号，再用上下文权重表达任务取舍，并监测漂移。标准化不决定价值优先级，也不能把单一答案准确率当作多维偏好的完整评估。 教学例子：一个评分维度取百分制，另一个只取少数档位，直接求和容易由前者主导；需先区分尺度与用户真正想要的权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-gprl-3009fd16" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d36e96fff938a5a3">GPRL为什么逐偏好维度算组内优势，再按上下文聚合？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agprl">GPRL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直接相加原始奖励会让量纲大或方差大的维度支配训练，掩盖帮助性、格式与简洁性的冲突。逐维标准化先获得可比信号，再用上下文权重表达任务取舍，并监测漂移。标准化不决定价值优先级，也不能把单一答案准确率当作多维偏好的完整评估。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个评分维度取百分制，另一个只取少数档位，直接求和容易由前者主导；需先区分尺度与用户真正想要的权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.18721">原论文</a> · <a href="../../../../post-training/2605.18721-gprl/">实现解读</a> · <a href="#qa-d36e96fff938a5a3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:conspo" data-paper-title="ConSPO" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="ConSPO LLM 后训练 Beijing Institute of Technology 2026-05-13 将同组序列的优劣关系写成长度归一化 InfoNCE，避免 token 求和造成长度和组内尺度偏差。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.6406（+173.33%）；奖励、KL、长度和候选预算一致。  对比序列 RL LLM 后训练 策略优化：谁在采样，谁在被更新 ConSPO为什么用长度归一化序列分数做组内InfoNCE，而不直接累计token奖励？ 累积对数概率会随长度改变分数尺度，可能把长短差异误当优劣。ConSPO先用平均token分数表示整条响应，再在同题组内做对比，使优选响应相对其他候选得到更高概率。归一化与温度仍影响梯度，组内相对好不保证答案绝对正确。 教学例子：同题一份短回答和一份长解释都正确，直接求和可能惩罚后者；先归一化，再比较组内相对质量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-conspo-ff3e363d" class="ar-learning-paper-anchor"></span>
<h2 id="qa-dcba0d92e323eff2">ConSPO为什么用长度归一化序列分数做组内InfoNCE，而不直接累计token奖励？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aconspo">ConSPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beijing Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>累积对数概率会随长度改变分数尺度，可能把长短差异误当优劣。ConSPO先用平均token分数表示整条响应，再在同题组内做对比，使优选响应相对其他候选得到更高概率。归一化与温度仍影响梯度，组内相对好不保证答案绝对正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同题一份短回答和一份长解释都正确，直接求和可能惩罚后者；先归一化，再比较组内相对质量。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.12969">原论文</a> · <a href="../../../../post-training/2605.12969-conspo/">实现解读</a> · <a href="#qa-dcba0d92e323eff2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:missing-old-logits" data-paper-title="Missing Old Logits" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Missing Old Logits LLM 后训练 Tianjin University 2026-05-12 指出异步 RL 丢失历史训练侧 logits 后，训推校正与策略陈旧校正发生语义混叠；给出快照、old-logit model、中断同步和 PPO-EWMA 修复。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。Arithmetic candidate suite、120 steps、seed 42：accuracy 0.2344 → 0.5000（+113.33%）。  异步 off-policy LLM 后训练 策略优化：谁在采样，谁在被更新 丢掉历史训练侧logits后，为什么无法分清训推失配与策略陈旧？ 当前训练概率到旧推理概率的总比率可拆成历史训推差异和后续策略变化，两者需要历史训练侧概率作中间量。缺失它时，只看总比率无法判断偏移来自引擎还是权重更新。快照或old-logit模型是在恢复这个参照，不是给缺失值随便补零。 教学例子：同一旧样本现在概率变了，可能是推理引擎当时就有差，也可能训练后模型改变；没有旧训练快照，两种原因会混在一起。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-missing-old-logits-37bc553d" class="ar-learning-paper-anchor"></span>
<h2 id="qa-460fc794c3daf6c8">丢掉历史训练侧logits后，为什么无法分清训推失配与策略陈旧？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amissing-old-logits">Missing Old Logits</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tianjin University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>当前训练概率到旧推理概率的总比率可拆成历史训推差异和后续策略变化，两者需要历史训练侧概率作中间量。缺失它时，只看总比率无法判断偏移来自引擎还是权重更新。快照或old-logit模型是在恢复这个参照，不是给缺失值随便补零。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一旧样本现在概率变了，可能是推理引擎当时就有差，也可能训练后模型改变；没有旧训练快照，两种原因会混在一起。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.12070">原论文</a> · <a href="../../../../post-training/2605.12070-missing-old-logits/">实现解读</a> · <a href="#qa-460fc794c3daf6c8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:luspo" data-paper-title="LUSPO" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="LUSPO LLM 后训练 Meituan 2026-02-05 论文从目标函数分解解释不同 RLVR 算法为何产生不同的响应长度轨迹，并指出 GSPO 的 sequence ratio 仍含长度偏置。LUSPO 对 sequence log-probability 作长度无偏归一化，避免训练中的长度坍塌。 Length-Unbiased Sequence Policy Optimization：校正 sequence policy objective 的响应长度偏差。已实现真实自由生成、sequence-level ratio 和长度无偏归一化；本地短算术响应无法覆盖论文长 CoT 的长度动力学，结论仅用于代码路径与指标口径验证。本地从 policy 自由采样完整响应，用 exact-answer verifier 评分，以长度归一化的 sequence ratio 和 group advantage 更新；同时记录 response length 与 reward 相关性。  长度无偏 RL LLM 后训练 策略优化：谁在采样，谁在被更新 LUSPO为什么认为sequence ratio仍需检查长度偏置，序列级更新不就已经公平了吗？ 把更新聚合到序列级并不会自动消除累积log-prob与长度的耦合。LUSPO从目标分解关注这种差异，用长度无偏口径组织序列分数，避免更新系统性推着响应变长或变短。短算术任务上跑通归一化，并不能验证长CoT训练的长度动力学。 教学例子：两条回答每步变化相近，但一条长很多，累积比率仍可能不同；称为“序列级目标”本身不能消除这种长度效应。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-luspo-8b4b98a1" class="ar-learning-paper-anchor"></span>
<h2 id="qa-335bdae0fb18cc4d">LUSPO为什么认为sequence ratio仍需检查长度偏置，序列级更新不就已经公平了吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aluspo">LUSPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>把更新聚合到序列级并不会自动消除累积log-prob与长度的耦合。LUSPO从目标分解关注这种差异，用长度无偏口径组织序列分数，避免更新系统性推着响应变长或变短。短算术任务上跑通归一化，并不能验证长CoT训练的长度动力学。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两条回答每步变化相近，但一条长很多，累积比率仍可能不同；称为“序列级目标”本身不能消除这种长度效应。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.05261">原论文</a> · <a href="../../../../post-training/2602.05261-luspo/">实现解读</a> · <a href="#qa-335bdae0fb18cc4d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:calibration-aware-rl" data-paper-title="Balancing Classification and Calibration Performance in Decision-Making LLMs via Calibration Aware Reinforcement Learning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Balancing Classification and Calibration Performance in Decision-Making LLMs via Calibration Aware Reinforcement Learning LLM 后训练 University of Southern California 2026-01-19 论文指出 RLVR 虽能提高决策正确率，却可能让 decision token 极度过度自信；其方法直接调整决策 token 的概率，在保留准确率的同时降低 ECE。本仓库对应地把 accuracy 与 Brier/ECE 同时纳入报告，并只用 validation 拟合温度，禁止用 test 调参。本地实现不复刻论文的完整 RLVR 流程，属于决策概率校准机制与评测协议实现。 未复现完整 RLVR 训练，只实现决策概率校准轴、数据隔离与统一报告。  校准强化学习 决策 token LLM 后训练 策略优化：谁在采样，谁在被更新 准确率提高而ECE变差，为什么Calibration-Aware RL还要单独约束决策概率？ 正确决策只要求最大概率类别对，校准还要求置信与真实命中频率相符。RLVR可能把已正确的选择推得过度自信，因此两项应分开测量。本地温度只由validation选择，test用于最终报告；事后校准机制并不等于原论文完整RL训练被复现。 教学例子：两模型总选同一类别，但一个每次声称几乎必对，另一个承认不确定；准确率相同不代表概率质量相同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-calibration-aware-rl-6e3cb1f1" class="ar-learning-paper-anchor"></span>
<h2 id="qa-4c73529324e3dd75">准确率提高而ECE变差，为什么Calibration-Aware RL还要单独约束决策概率？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acalibration-aware-rl">Balancing Classification and Calibration Performance in Decision-Making LLMs via Calibration Aware Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>正确决策只要求最大概率类别对，校准还要求置信与真实命中频率相符。RLVR可能把已正确的选择推得过度自信，因此两项应分开测量。本地温度只由validation选择，test用于最终报告；事后校准机制并不等于原论文完整RL训练被复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两模型总选同一类别，但一个每次声称几乎必对，另一个承认不确定；准确率相同不代表概率质量相同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.13284">原论文</a> · <a href="../../../../post-training/2601.13284-calibration-aware-rl/">实现解读</a> · <a href="#qa-4c73529324e3dd75">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:online-icepop" data-paper-title="Online IcePop" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Online IcePop LLM 后训练 Ant Group 2025-12-16 普通 IcePop 同时面对训练/rollout 引擎差异和一次 rollout 被多次更新造成的策略陈旧。Online IcePop 强制每个 rollout batch 只更新一次，使 stale-policy ratio 恒为 1，从目标中移除 PPO ratio 与 clip；训练侧仍用 IcePop 双侧 mask 和区间内原始 ratio 校正引擎失配。 每个训练 step 后立即把当前权重刷新为下一批 rollout 权重，诊断中强制 policy_staleness_ratio_mean=1、关闭 PPO clip，同时沿用 IcePop [0.5, 5.0] 双侧 mask。本页在公开候选策略上复现网页资料中的可隔离 RL 更新机制；不把轻量实验写成来源材料中的大模型效果。本地一个 candidate group 对应一个 rollout batch，不包含真实并行采样和通信；验证的是单次更新调度、stale ratio 消除和训推 mask 的组合语义。  纯在线训推校正 LLM 后训练 策略优化：谁在采样，谁在被更新 Online IcePop每批只更新一次后，为什么仍不能删掉训推引擎校正？ 单次使用新鲜rollout消除了跨更新复用造成的策略陈旧，所以对应policy ratio在采样点为一，不再需要那条PPO裁剪路径。但同一权重在推理和训练引擎中仍可能给出不同概率，双侧IcePop掩码及区间内原始比率仍负责这一差异。 教学例子：刚采样的回答虽然没有过期，推理端与训练端精度仍不同；“新鲜数据”不意味着两个引擎算出的概率完全一致。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-online-icepop-2e9d86d8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-7d8fc111dd88f837">Online IcePop每批只更新一次后，为什么仍不能删掉训推引擎校正？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aonline-icepop">Online IcePop</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ant Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单次使用新鲜rollout消除了跨更新复用造成的策略陈旧，所以对应policy ratio在采样点为一，不再需要那条PPO裁剪路径。但同一权重在推理和训练引擎中仍可能给出不同概率，双侧IcePop掩码及区间内原始比率仍负责这一差异。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>刚采样的回答虽然没有过期，推理端与训练端精度仍不同；“新鲜数据”不意味着两个引擎算出的概率完全一致。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://zhuanlan.zhihu.com/p/1984379979035850499">原始资料</a> · <a href="../../../../post-training/web-2025-online-icepop/">实现解读</a> · <a href="#qa-7d8fc111dd88f837">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:minirl" data-paper-title="Stabilizing RL with LLMs" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Stabilizing RL with LLMs LLM 后训练 Alibaba Qwen Team 2025-12-01 分解训推差异与 policy staleness，on-policy 使用 importance correction，off-policy 结合 clipping 与 MoE Routing Replay。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。Arithmetic candidate suite、120 steps、seed 42：accuracy 0.2344 → 0.5000（+113.33%）。  稳定 MoE RL LLM 后训练 策略优化：谁在采样，谁在被更新 MiniRL为什么把训推差异与policy staleness拆开，MoE Routing Replay又处理哪层不一致？ 引擎数值差异与参数更新造成的陈旧是不同来源，不能用同一个未说明的比率混过去。方法对在策略部分做概率校正，对离策略更新结合裁剪，并重放rollout时的MoE路由以减少执行路径变化。概率权重和专家路径都需核对，小核诊断不代表集群验证。 教学例子：相同token在采样时走专家甲，训练重算时走专家乙，即使权重刚同步也会产生差异；仅调陈旧比率未必解决。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-minirl-5767c2fc" class="ar-learning-paper-anchor"></span>
<h2 id="qa-a451194042251330">MiniRL为什么把训推差异与policy staleness拆开，MoE Routing Replay又处理哪层不一致？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aminirl">Stabilizing RL with LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Qwen Team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>引擎数值差异与参数更新造成的陈旧是不同来源，不能用同一个未说明的比率混过去。方法对在策略部分做概率校正，对离策略更新结合裁剪，并重放rollout时的MoE路由以减少执行路径变化。概率权重和专家路径都需核对，小核诊断不代表集群验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>相同token在采样时走专家甲，训练重算时走专家乙，即使权重刚同步也会产生差异；仅调陈旧比率未必解决。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2512.01374">原论文</a> · <a href="../../../../post-training/2512.01374-minirl/">实现解读</a> · <a href="#qa-a451194042251330">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:icepop" data-paper-title="IcePop" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="IcePop LLM 后训练 Ant Group 2025-10-21 MoE router 会放大训练引擎与 rollout 引擎的微小数值差异，单侧 TIS 仍可能保留严重偏小的失配 ratio。IcePop 对训练侧与 rollout 引擎的 token 概率比设置固定双侧区间；区间内保留原始校正权重，区间外 token 的本次策略梯度直接归零。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。没有真实 MoE expert routing、万亿参数模型或异步集群；本地只隔离复现固定双侧 mask 与原始区间内校正权重。在与 TIS 相同的候选策略和引擎失配模拟中采用公开实现常用的 [0.5, 5.0] 区间，区间外动作真正不产生梯度，同时保留旧 rollout policy 的 PPO ratio/clip。  MoE 训推失配 LLM 后训练 策略优化：谁在采样，谁在被更新 IcePop区间外token的更新归零，和把ratio裁到最近边界有什么不同？ 裁剪会保留边界权重下的贡献，掩码则直接放弃该token本次策略梯度。IcePop用固定双侧区间排除过大和过小的训推比，区间内仍使用原始校正权重，避免把它们全部改成一。它过滤的是失配程度，不是在判断token内容好坏。 教学例子：某token的训推比极小，单侧上截断几乎不处理它；双侧掩码会排除，而非给它补上一个最小边界权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-icepop-96432a79" class="ar-learning-paper-anchor"></span>
<h2 id="qa-6dd13d3913684d0d">IcePop区间外token的更新归零，和把ratio裁到最近边界有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aicepop">IcePop</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ant Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>裁剪会保留边界权重下的贡献，掩码则直接放弃该token本次策略梯度。IcePop用固定双侧区间排除过大和过小的训推比，区间内仍使用原始校正权重，避免把它们全部改成一。它过滤的是失配程度，不是在判断token内容好坏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某token的训推比极小，单侧上截断几乎不处理它；双侧掩码会排除，而非给它补上一个最小边界权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.18855">原论文</a> · <a href="../../../../post-training/2510.18855-icepop/">实现解读</a> · <a href="#qa-6dd13d3913684d0d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gppo" data-paper-title="GPPO" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="GPPO LLM 后训练 Alibaba Group 2025-08-11 普通 PPO 在正优势高 ratio、负优势低 ratio 的越界象限直接令梯度为零，可能同时压制探索和从负样本学习。GPPO 保持 PPO 的前向 clipped objective，但通过 stop-gradient 边界权重恢复这些越界位置的反向信号。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地不训练 Klear-Reasoner 或长 CoT SFT，只复现 GPPO 的前向/反向分离机制。在 GSM8K candidate-policy 中区分 PPO 正常和越界样本，前向仍计算 clipped surrogate，反向以 clip 边界权重保留越界梯度。  梯度保留 clip LLM 后训练 策略优化：谁在采样，谁在被更新 GPPO前向仍像PPO，为什么越界token却能保留反向信号？ 前向裁剪值和反向导数可以通过stop-gradient构造分别指定。GPPO保留PPO形式的数值目标，同时用边界权重恢复原本被截平象限的更新，避免正样本探索和负样本学习同时中断。仅比较loss数值看不出差异，必须检查梯度路径。 教学例子：两个算子打印同一个裁剪后分数，但一个越界时梯度为零，另一个仍有边界加权梯度；训练行为会不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-gppo-ce7f50e5" class="ar-learning-paper-anchor"></span>
<h2 id="qa-7ded4f2a343eef5f">GPPO前向仍像PPO，为什么越界token却能保留反向信号？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agppo">GPPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前向裁剪值和反向导数可以通过stop-gradient构造分别指定。GPPO保留PPO形式的数值目标，同时用边界权重恢复原本被截平象限的更新，避免正样本探索和负样本学习同时中断。仅比较loss数值看不出差异，必须检查梯度路径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个算子打印同一个裁剪后分数，但一个越界时梯度为零，另一个仍有边界加权梯度；训练行为会不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.07629">原论文</a> · <a href="../../../../post-training/2508.07629-gppo/">实现解读</a> · <a href="#qa-7ded4f2a343eef5f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tis" data-paper-title="TIS" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="TIS LLM 后训练 University of California, San Diego 2025-08-05 混合训练框架由 rollout 引擎采样、训练引擎重算 log-prob；即使权重相同，数值精度和 kernel 差异也会让行为分布与训练分布偏离。TIS 将训练侧与 rollout 引擎概率比乘入策略梯度，并只对过大的校正权重做单侧上截断，保留小权重样本而控制重尾方差。 本页在公开候选策略上复现网页资料中的可隔离 RL 更新机制；不把轻量实验写成来源材料中的大模型效果。候选动作分布替代逐 token LLM 概率，确定性引擎扰动替代真实 vLLM/FSDP 数值差异；这里只验证 TIS 权重与梯度路径，不复刻网页中的大模型训练。本地显式维护旧训练策略和带确定性数值/router 扰动的 rollout 引擎分布，以 c=2 单侧截断训推 ratio；TIS 不丢弃区间外样本，并继续保留 PPO stale-policy ratio。  训推失配校正 LLM 后训练 策略优化：谁在采样，谁在被更新 TIS为什么只上截断训练与推理概率比，而保留小权重样本？ 比率用于把rollout引擎采样校正到训练侧分布，特别大的权重会带来重尾方差，上截断限制其支配程度。小比率表示该样本在目标侧贡献较小，仍可保留相应权重。它不是PPO的新旧策略比，也不等于双侧丢弃失配token。 教学例子：一个旧引擎常采到、训练侧罕见的词应少贡献，而不是自动删除；极大的反向失配则需限制其单个样本影响。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-tis-834fa80d" class="ar-learning-paper-anchor"></span>
<h2 id="qa-741f3036cd257055">TIS为什么只上截断训练与推理概率比，而保留小权重样本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atis">TIS</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>比率用于把rollout引擎采样校正到训练侧分布，特别大的权重会带来重尾方差，上截断限制其支配程度。小比率表示该样本在目标侧贡献较小，仍可保留相应权重。它不是PPO的新旧策略比，也不等于双侧丢弃失配token。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个旧引擎常采到、训练侧罕见的词应少贡献，而不是自动删除；极大的反向失配则需限制其单个样本影响。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://fengyao.notion.site/off-policy-rl">原始资料</a> · <a href="../../../../post-training/web-2025-tis/">实现解读</a> · <a href="#qa-741f3036cd257055">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gspo" data-paper-title="GSPO" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="GSPO LLM 后训练 Alibaba Qwen Team 2025-07-24 GRPO/PPO 常逐 token 裁剪 ratio，但 reward 在完整序列级给出；长序列中单个异常 token 会造成大量裁剪，MoE routing 变化还会放大不稳定。GSPO 对每条 response 取平均 log-ratio，再指数化为单一 sequence ratio，整条序列共享 clip 权重。 GSPO 把 token-level importance ratio 改为 response 的序列级 ratio，使优化单元与序列 reward 对齐，并降低长回答和 MoE 训练中的方差。实现了长度归一化 sequence ratio、group advantage、序列级 clip 与 reference KL；本地候选没有真实 token trajectory，也未复刻 Qwen3 MoE 的 expert routing 与集群规模。300 steps 刷新 old policy 18 次；最后一组 sequence ratio 均值/标准差为 1.0131/0.0117。  稳定序列 RL LLM 后训练 策略优化：谁在采样，谁在被更新 GSPO为何先平均token log-ratio再指数化，而不逐token各裁一次？ 完整回答接收一个结果奖励，逐token异常可能引发不一致裁剪。GSPO把平均log-ratio变成单个序列权重，让整条回答共享相对优势与裁剪决定。它缓和局部噪声，但改变了信用聚合粒度，也不能因此推断所有长度偏置或MoE路径差异已经消失。 教学例子：一段正确回答只有一个词的ratio异常，逐词裁剪与整段共享一个几何平均权重，会给出不同的更新分配。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-gspo-8ccc0734" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b968145af51dfe73">GSPO为何先平均token log-ratio再指数化，而不逐token各裁一次？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agspo">GSPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Qwen Team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>完整回答接收一个结果奖励，逐token异常可能引发不一致裁剪。GSPO把平均log-ratio变成单个序列权重，让整条回答共享相对优势与裁剪决定。它缓和局部噪声，但改变了信用聚合粒度，也不能因此推断所有长度偏置或MoE路径差异已经消失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一段正确回答只有一个词的ratio异常，逐词裁剪与整段共享一个几何平均权重，会给出不同的更新分配。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.18071">原论文</a> · <a href="../../../../post-training/2507.18071-gspo/">实现解读</a> · <a href="#qa-b968145af51dfe73">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rlcr" data-paper-title="Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty LLM 后训练 Massachusetts Institute of Technology 2025-07-22 普通 binary reward 只奖励答对，容易鼓励模型无差别地自信。RLCR 让模型同时输出预测与置信度，并把 bounded proper scoring rule 加入奖励，使诚实概率具有最优激励。本地基线对完整候选分布最小化多类 Brier：这里复现的是 scoring-rule 机制，不是论文的 LLM rollout、RL 训练栈或 confidence-weighted scaling；因此以机制实验而非论文结果复刻报告。 未运行论文的 LLM checkpoint 与 RL rollout，当前为 proper-scoring 机制实现。  校准奖励 Proper scoring rule LLM 后训练 策略优化：谁在采样，谁在被更新 RLCR输出答案再报置信，为什么需要proper scoring rule而不是只奖励答对？ 二元正确奖励不区分恰当谨慎与盲目自信，模型即使经常出错也可能报高置信。proper评分规则把预测概率与结果共同计分，在其假设下激励诚实概率。训练与报告应分开准确性和校准；本地Brier梯度实验不是论文完整rollout强化学习。 教学例子：一个答题器对不熟悉的问题总说“完全确定”，仅按对错奖励未必纠正这句话；概率评分会让无根据自信付出代价。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-rlcr-9a05e032" class="ar-learning-paper-anchor"></span>
<h2 id="qa-e491a49ab4ec08e3">RLCR输出答案再报置信，为什么需要proper scoring rule而不是只奖励答对？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arlcr">Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Massachusetts Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>二元正确奖励不区分恰当谨慎与盲目自信，模型即使经常出错也可能报高置信。proper评分规则把预测概率与结果共同计分，在其假设下激励诚实概率。训练与报告应分开准确性和校准；本地Brier梯度实验不是论文完整rollout强化学习。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个答题器对不熟悉的问题总说“完全确定”，仅按对错奖励未必纠正这句话；概率评分会让无根据自信付出代价。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.16806">原论文</a> · <a href="../../../../post-training/2507.16806-rlcr/">实现解读</a> · <a href="#qa-e491a49ab4ec08e3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cispo" data-paper-title="CISPO / MiniMax-M1" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="CISPO / MiniMax-M1 LLM 后训练 MiniMax 2025-06-16 固定 rollout policy 采样，token 级计算 importance ratio，只裁剪比率以保留优势方向和有效梯度。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.5000（+113.33%）；奖励、KL、长度和候选预算一致。  长上下文 RL LLM 后训练 策略优化：谁在采样，谁在被更新 CISPO裁剪的是importance weight，为什么不像PPO那样让部分越界token直接没有梯度？ 它把裁剪后的比率当作策略梯度的权重，优势方向和log-prob更新仍被保留；PPO的min-surrogate则会在某些越界象限形成平坦区。两者即使采用相似裁剪区间，反向路径也不同。测试需要检查梯度，不能只比前向目标或把优势本身截断。 教学例子：一个负优势token已经很少出现，PPO可能不再继续压低；权重式裁剪仍可给它受限的负向学习信号。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-cispo-73dd09ad" class="ar-learning-paper-anchor"></span>
<h2 id="qa-ce326a3ad19568a3">CISPO裁剪的是importance weight，为什么不像PPO那样让部分越界token直接没有梯度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acispo">CISPO / MiniMax-M1</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · MiniMax</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它把裁剪后的比率当作策略梯度的权重，优势方向和log-prob更新仍被保留；PPO的min-surrogate则会在某些越界象限形成平坦区。两者即使采用相似裁剪区间，反向路径也不同。测试需要检查梯度，不能只比前向目标或把优势本身截断。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个负优势token已经很少出现，PPO可能不再继续压低；权重式裁剪仍可给它受限的负向学习信号。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2506.13585">原论文</a> · <a href="../../../../post-training/2506.13585-cispo/">实现解读</a> · <a href="#qa-ce326a3ad19568a3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ttrl" data-paper-title="TTRL" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="TTRL LLM 后训练 PRIME-RL author team 2025-04-22 同一测试题多次采样，以多数一致答案作为伪标签并即时更新模型，不访问 gold label。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.2344（+0.00%）；奖励、KL、长度和候选预算一致。  测试时强化学习 LLM 后训练 策略优化：谁在采样，谁在被更新 TTRL用测试题多数票作奖励，为什么必须明确它是无标签适配而非普通固定模型评测？ 测试输入被用于采样并即时更新参数，评测对象因此随过程变化。多数票提供伪标签而非gold，可能自我强化错误，所以必须报告采样与适配预算，并把隐藏答案留在独立评分侧。无标签不等于没有测试时学习，更不能与零适配结果混写。 教学例子：模型对一道新题采样多次，再按共识更新后作答；这与直接调用原模型一次不同，即使全过程没有读取标准答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-ttrl-f1272098" class="ar-learning-paper-anchor"></span>
<h2 id="qa-c6d9c41a8ac4de24">TTRL用测试题多数票作奖励，为什么必须明确它是无标签适配而非普通固定模型评测？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Attrl">TTRL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · PRIME-RL author team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>测试输入被用于采样并即时更新参数，评测对象因此随过程变化。多数票提供伪标签而非gold，可能自我强化错误，所以必须报告采样与适配预算，并把隐藏答案留在独立评分侧。无标签不等于没有测试时学习，更不能与零适配结果混写。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型对一道新题采样多次，再按共识更新后作答；这与直接调用原模型一次不同，即使全过程没有读取标准答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.16084">原论文</a> · <a href="../../../../post-training/2504.16084-ttrl/">实现解读</a> · <a href="#qa-c6d9c41a8ac4de24">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:luffy" data-paper-title="LUFFY" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="LUFFY LLM 后训练 University of Washington 2025-04-21 把离线高质量推理与在线 rollout 放进同一 support，通过正则化 importance ratio 保留 on-policy 行为。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.5312（+126.67%）；奖励、KL、长度和候选预算一致。  离策略推理 RL LLM 后训练 策略优化：谁在采样，谁在被更新 LUFFY把离线示范和在线rollout放在一起时，为什么还要关心行为分布mu？ 示范与当前策略样本来自不同分布，不能仅因共用一个batch就当成同一种on-policy数据。重要性比及正则化用于控制这种来源错配，同时保留在线探索。示范覆盖不到的状态仍需学生自己访问，且训练示范不能泄漏到最终被评估策略的输入。 教学例子：专家有一条成功推导，学生自己采到几条失败推导；混合使用时要记录每条来源，而非把专家成功记作学生采样。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-luffy-8fd3aff1" class="ar-learning-paper-anchor"></span>
<h2 id="qa-3e37406dcb0a268f">LUFFY把离线示范和在线rollout放在一起时，为什么还要关心行为分布mu？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aluffy">LUFFY</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>示范与当前策略样本来自不同分布，不能仅因共用一个batch就当成同一种on-policy数据。重要性比及正则化用于控制这种来源错配，同时保留在线探索。示范覆盖不到的状态仍需学生自己访问，且训练示范不能泄漏到最终被评估策略的输入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>专家有一条成功推导，学生自己采到几条失败推导；混合使用时要记录每条来源，而非把专家成功记作学生采样。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.14945">原论文</a> · <a href="../../../../post-training/2504.14945-luffy/">实现解读</a> · <a href="#qa-3e37406dcb0a268f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:vapo" data-paper-title="VAPO" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="VAPO LLM 后训练 ByteDance Seed 2025-04-07 长 CoT 的 value-based PPO 易受 critic bias、异质 response 长度和稀疏奖励影响。VAPO 预训练 value model，并依 response 长度调节 actor 的 GAE/更新策略，以更稳定地进行 value-based 推理 RL。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地 critic 不是预训练 value model，候选动作与伪长度替代自由生成长 CoT。复用可训练线性 critic，按候选伪长度调节 GAE 系数，并真实更新 actor、old policy 和 critic。  Critic PPO LLM 后训练 策略优化：谁在采样，谁在被更新 VAPO为什么先改善critic，并让GAE与响应长度相关，而不是直接换成无critic算法？ 长推理中稀疏奖励和长度差异会放大价值估计偏差，VAPO选择修复value-based路径：预训练critic，再让优势估计与actor策略适配长度。它没有声称critic可以省略；本地小价值估计和伪长度也不能代替真实长CoT的训练与稳定性证据。 教学例子：短回答很快看到结果，长回答要延迟很久才获奖；同一优势估计参数可能给它们不同的偏差与方差。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-vapo-b94393ac" class="ar-learning-paper-anchor"></span>
<h2 id="qa-0e539b78de945446">VAPO为什么先改善critic，并让GAE与响应长度相关，而不是直接换成无critic算法？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Avapo">VAPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance Seed</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长推理中稀疏奖励和长度差异会放大价值估计偏差，VAPO选择修复value-based路径：预训练critic，再让优势估计与actor策略适配长度。它没有声称critic可以省略；本地小价值估计和伪长度也不能代替真实长CoT的训练与稳定性证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>短回答很快看到结果，长回答要延迟很久才获奖；同一优势估计参数可能给它们不同的偏差与方差。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.05118">原论文</a> · <a href="../../../../post-training/2504.05118-vapo/">实现解读</a> · <a href="#qa-0e539b78de945446">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dr-grpo" data-paper-title="Dr. GRPO" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="Dr. GRPO LLM 后训练 SAIL 研究团队 2025-03-26 原始 GRPO 的 response 内长度平均和组内标准差会引入长度与题目难度偏置。Dr. GRPO 移除这两个归一化项，保留中心化的组相对奖励，让每条轨迹以原始尺度参与更新。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。候选策略没有自由生成 response 长度，伪长度只用于暴露归一化差异，不等同于论文的 token-level 长 CoT 训练。在相同 GSM8K candidate-policy、步数和 seed 下真实移除组 std 与伪长度归一化，并与 GRPO 的更新统计对比。  GRPO 聚合偏置 LLM 后训练 策略优化：谁在采样，谁在被更新 Dr. GRPO为什么同时移除组标准差和响应内长度平均？ 按组标准差会让不同难度问题因局部方差被重新加权，响应内长度平均又改变长短轨迹的相对贡献。移除两项后，保留中心化奖励并按固定口径汇总，从目标层面减少这些偏置。它不是删除所有归一化，也不保证任何任务都自动更好。 教学例子：两个问题的平均奖励差相近，但其中一个组方差极小，标准化后可能被放大；再除响应长度会叠加另一层权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-dr-grpo-c17c40d0" class="ar-learning-paper-anchor"></span>
<h2 id="qa-72916d57d18ee4c3">Dr. GRPO为什么同时移除组标准差和响应内长度平均？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adr-grpo">Dr. GRPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · SAIL 研究团队</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>按组标准差会让不同难度问题因局部方差被重新加权，响应内长度平均又改变长短轨迹的相对贡献。移除两项后，保留中心化奖励并按固定口径汇总，从目标层面减少这些偏置。它不是删除所有归一化，也不保证任何任务都自动更好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个问题的平均奖励差相近，但其中一个组方差极小，标准化后可能被放大；再除响应长度会叠加另一层权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2503.20783">原论文</a> · <a href="../../../../post-training/2503.20783-dr-grpo/">实现解读</a> · <a href="#qa-72916d57d18ee4c3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dapo" data-paper-title="DAPO" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="DAPO LLM 后训练 ByteDance Seed 2025-03-18 长 CoT 的在线 RL 容易被标准对称 clip 限制探索，且全对/全错的组没有学习信号。DAPO 用 Clip-Higher 放宽概率上升、Dynamic Sampling 丢弃零方差组、token-level loss 公平处理不同长度，并对过长回答分段惩罚。 DAPO 在 GRPO 类在线训练上加入非对称裁剪、动态采样、token-level loss 与 overlong reward shaping，解决熵坍缩和无效 batch。实现四个核心训练机制和 old-policy rollout；候选长度由确定性伪 token 长度模拟，没有复刻 32B 长 CoT、分布式训练、真实 token mask 或 AIME verifier。300 steps 刷新 old policy 18 次；最后一步 low/high clip 为 0.20/0.28，clip fraction 0.25，平均伪 token 数 2.25，overlong penalty 0.0125。  长推理 RL LLM 后训练 策略优化：谁在采样，谁在被更新 DAPO的Dynamic Sampling为什么丢弃全对组，难道正确回答不值得继续学习？ 同组全对或全错时，中心化奖励没有相对差异，继续消耗该组预算难以提供所需优势。动态采样挑选仍有区分的组；Clip-Higher、token级汇总与过长惩罚分别处理探索和长度问题。丢弃无方差组不等于判定这些回答无价值，也不允许用test挑题。 教学例子：同题所有回答奖励完全相同，再算组内相对优势仍无方向；换一组尚有成败差异的训练样本，可能更有学习信号。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-dapo-b7495c1f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-ebd8d3555febbac3">DAPO的Dynamic Sampling为什么丢弃全对组，难道正确回答不值得继续学习？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adapo">DAPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance Seed</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同组全对或全错时，中心化奖励没有相对差异，继续消耗该组预算难以提供所需优势。动态采样挑选仍有区分的组；Clip-Higher、token级汇总与过长惩罚分别处理探索和长度问题。丢弃无方差组不等于判定这些回答无价值，也不允许用test挑题。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同题所有回答奖励完全相同，再算组内相对优势仍无方向；换一组尚有成败差异的训练样本，可能更有学习信号。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2503.14476">原论文</a> · <a href="../../../../post-training/2503.14476-dapo/">实现解读</a> · <a href="#qa-ebd8d3555febbac3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:reinforce-plus" data-paper-title="REINFORCE++" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="REINFORCE++ LLM 后训练 Independent researchers 2025-01-04 GRPO/RLOO 的 prompt-local 标准差会让不同难度组被随机方差重新加权。REINFORCE++ 保留组内中心化，但使用跨 batch 的全局优势尺度归一化，从而在不引入 critic 的前提下降低方差与局部偏置。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地 EMA 是小批候选轨迹统计，不代表论文的大 batch 分布或人类偏好奖励。维护跨训练步的 reward 二阶矩，真实以它而非当前组 std 缩放 group-centered advantage。  全局优势估计 LLM 后训练 策略优化：谁在采样，谁在被更新 REINFORCE++为什么保留组内中心化，却把尺度归一化放到全局？ 组内中心化消除同题共同难度，但局部标准差可能把偶然小方差组放大。跨batch的全局尺度提供更一致的更新量纲，在不增加critic的情况下减少局部重新加权。全局统计的窗口与分布也有影响，小batch EMA诊断不能当作大规模稳定性证明。 教学例子：两道题都出现一点奖励差，只有一道题的组方差特别小；统一全局尺度可避免它因偶然方差而获得异常大权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-reinforce-plus-c6bb06c9" class="ar-learning-paper-anchor"></span>
<h2 id="qa-939c465a1c7db3eb">REINFORCE++为什么保留组内中心化，却把尺度归一化放到全局？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Areinforce-plus">REINFORCE++</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Independent researchers</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>组内中心化消除同题共同难度，但局部标准差可能把偶然小方差组放大。跨batch的全局尺度提供更一致的更新量纲，在不增加critic的情况下减少局部重新加权。全局统计的窗口与分布也有影响，小batch EMA诊断不能当作大规模稳定性证明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两道题都出现一点奖励差，只有一道题的组方差特别小；统一全局尺度可避免它因偶然方差而获得异常大权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2501.03262">原论文</a> · <a href="../../../../post-training/2501.03262-reinforce-plus/">实现解读</a> · <a href="#qa-939c465a1c7db3eb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rloo" data-paper-title="RLOO" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="RLOO LLM 后训练 Cohere For AI 2024-02-22 PPO 为一般长时域 RL 设计，价值网络、GAE 和多轮 clipping 给 LLM RLHF 带来较大显存与调参开销。RLOO 把一整段 response 视作一个 action；同一 prompt 采样多个 response，用其余样本的平均 reward 作为当前样本 baseline。 本页实现完整响应级 REINFORCE、leave-one-out baseline 与 KL-shaped reward，不引入 PPO critic。实现了 K=4 的 leave-one-out advantage、完整候选 action 和 KL shaping，且明确不创建 value model；未复刻 6.9B/7B 模型、学习到的 reward model 与论文数据规模。与 PPO-RLHF 使用完全相同的 GSM8K candidate 数据、特征、reward、steps 与 seed。  经典 RLHF LLM 后训练 策略优化：谁在采样，谁在被更新 RLOO为什么用同题其余样本的平均奖励作baseline，而把当前样本排除？ baseline用来降低方差，应避免把当前动作自己的随机奖励混入其参照。leave-one-out使用同prompt其他独立样本，整段回答当一个动作，省去value网络。仍需足够组大小与一致奖励口径；无需critic不意味着无需采样、reference约束或外部评价。 教学例子：四份独立回答中评价第一份时，用另外三份的平均表现作参照；若把自己也算入，参照会随自身奖励一起移动。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-rloo-064c4d91" class="ar-learning-paper-anchor"></span>
<h2 id="qa-8f08c5af1cc0c720">RLOO为什么用同题其余样本的平均奖励作baseline，而把当前样本排除？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arloo">RLOO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Cohere For AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>baseline用来降低方差，应避免把当前动作自己的随机奖励混入其参照。leave-one-out使用同prompt其他独立样本，整段回答当一个动作，省去value网络。仍需足够组大小与一致奖励口径；无需critic不意味着无需采样、reference约束或外部评价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>四份独立回答中评价第一份时，用另外三份的平均表现作参照；若把自己也算入，参照会随自身奖励一起移动。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2402.14740">原论文</a> · <a href="../../../../post-training/2402.14740-rloo/">实现解读</a> · <a href="#qa-8f08c5af1cc0c720">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:grpo" data-paper-title="DeepSeekMath / GRPO" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="DeepSeekMath / GRPO LLM 后训练 DeepSeek-AI 2024-02-05 PPO 的 value model 与 policy 同规模，数学推理 RL 训练显存昂贵。GRPO 对同一问题采样一组 response，以组内 reward 均值和标准差构造 advantage，删除 critic；策略部分仍使用 old policy ratio、clipping 与 reference KL。 最后一步诊断包含 4 个 group samples、importance ratio、clip fraction；本页实现 group-relative advantage、old-policy ratio、clipped surrogate 与 reference KL，并验证无需 critic 的在线策略更新。保留 GRPO 的在线 group sampling、critic-free advantage、ratio clipping 和 KL；本地 response 是六候选完整 action，未训练 DeepSeekMath 7B，也未复刻 120B token 预训练和自由生成数学 verifier。  在线推理 RL LLM 后训练 策略优化：谁在采样，谁在被更新 GRPO省掉critic后，同一问题的回答组怎样提供优势，old policy与reference还各做什么？ 组内奖励的中心化与尺度化提供相对优势，代替单独训练的价值估计；old policy记录采样时分布，用于比率和裁剪，reference则提供KL锚点。三者角色不能互换，全同奖励组也不会凭空产生区分信号。本地候选动作更新不等于完整数学模型训练。 教学例子：同题几份回答有对有错，可比较彼此奖励；更换reference只改变锚定目标，不能改写这些回答当时由谁采样。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-grpo-679757d4" class="ar-learning-paper-anchor"></span>
<h2 id="qa-62e639b015b8e33e">GRPO省掉critic后，同一问题的回答组怎样提供优势，old policy与reference还各做什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agrpo">DeepSeekMath / GRPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · DeepSeek-AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>组内奖励的中心化与尺度化提供相对优势，代替单独训练的价值估计；old policy记录采样时分布，用于比率和裁剪，reference则提供KL锚点。三者角色不能互换，全同奖励组也不会凭空产生区分信号。本地候选动作更新不等于完整数学模型训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同题几份回答有对有错，可比较彼此奖励；更换reference只改变锚定目标，不能改写这些回答当时由谁采样。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2402.03300">原论文</a> · <a href="../../../../post-training/2402.03300-grpo/">实现解读</a> · <a href="#qa-62e639b015b8e33e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:remax" data-paper-title="ReMax" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="ReMax LLM 后训练 香港中文大学（深圳）/ 深圳市大数据研究院 2023-10-16 ReMax 利用 LLM RLHF 的三项特征：模拟快、token 转移确定、reward 通常只在轨迹末端给出。它删除 PPO 的 value model，以当前策略 greedy decoding 的 reward 作 prompt-dependent baseline，降低 REINFORCE 方差。 本页实现 ReMax 的 sampled rollout 减 greedy rollout baseline，验证无需价值网络的低状态 RLHF 更新。实现 sampled/greedy 双 rollout 与 value-free 更新；候选策略中的 greedy baseline 与自回归 greedy decoding 同构，但没有复刻 Mistral-7B、分布式训练或显存基准，本地结果不能与 AlpacaEval 横向比较。稳定指标：classic-post-training-gsm8k-seed42.json。  经典 RLHF LLM 后训练 策略优化：谁在采样，谁在被更新 ReMax用greedy回答奖励作baseline，会不会要求greedy答案一定正确？ 不需要。baseline只是同prompt的参照，用来降低采样更新的方差；随机回答比greedy好或差，决定相对信号。greedy也可能错，且baseline不作为独立真值标签。方法省去value模型，但仍要实际生成并评价greedy与采样两条路径的成本。 教学例子：贪心解法答错，随机解法答对时仍有正信号；如果两者都错，不能因为贪心是baseline就把它称作标准答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-remax-79f8bb09" class="ar-learning-paper-anchor"></span>
<h2 id="qa-4c70be2bb992c727">ReMax用greedy回答奖励作baseline，会不会要求greedy答案一定正确？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aremax">ReMax</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 香港中文大学（深圳）/ 深圳市大数据研究院</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不需要。baseline只是同prompt的参照，用来降低采样更新的方差；随机回答比greedy好或差，决定相对信号。greedy也可能错，且baseline不作为独立真值标签。方法省去value模型，但仍要实际生成并评价greedy与采样两条路径的成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>贪心解法答错，随机解法答对时仍有正信号；如果两者都错，不能因为贪心是baseline就把它称作标准答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2310.10505">原论文</a> · <a href="../../../../post-training/2310.10505-remax/">实现解读</a> · <a href="#qa-4c70be2bb992c727">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ppo-rlhf" data-paper-title="InstructGPT / PPO-RLHF" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/policy-optimization" data-search="InstructGPT / PPO-RLHF LLM 后训练 OpenAI 2022-03-04 只扩大语言模型不能保证更符合用户意图。InstructGPT 建立了经典三阶段流程：先用标注员示范做 SFT，再用成对排序训练 reward model，最后用 PPO 优化策略，同时以 KL 惩罚限制策略偏离 SFT/reference model。 未训练 GPT-3、reward model，也未使用 OpenAI 私有 prompt 和人工标注数据。本页实现 PPO-RLHF 的旧策略采样、clipped surrogate、独立 critic 与 KL 约束；不把候选策略实验写成 175B InstructGPT 复刻。保留 PPO 的 actor/old-policy/critic/clip/KL 更新结构，但策略是可解释的候选线性 policy，reward 来自确定性结果与过程轴；未训练 GPT-3、reward model，也未使用 OpenAI 私有 prompt 和人工标注数据。  经典 RLHF LLM 后训练 策略优化：谁在采样，谁在被更新 InstructGPT流程中的reward model、critic、old policy与reference为什么不能合成一个概念？ reward model把偏好转成评分，critic估计回报以构造优势，old policy标识采样分布，reference约束相对SFT策略的漂移。它们可能有共享初始化，但训练目的与使用时点不同。只跑候选策略的actor/critic更新，并未复现人工排序、奖励模型训练或大模型RLHF。 教学例子：一份回答可被奖励模型评高分，但critic只是预测它未来能获多少回报；reference又只负责比较策略偏离程度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 策略优化：谁在采样，谁在被更新</a></p>
<span id="paper-post-training-ppo-rlhf-a0e573a8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-5003585127af1af3">InstructGPT流程中的reward model、critic、old policy与reference为什么不能合成一个概念？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Appo-rlhf">InstructGPT / PPO-RLHF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · OpenAI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>reward model把偏好转成评分，critic估计回报以构造优势，old policy标识采样分布，reference约束相对SFT策略的漂移。它们可能有共享初始化，但训练目的与使用时点不同。只跑候选策略的actor/critic更新，并未复现人工排序、奖励模型训练或大模型RLHF。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一份回答可被奖励模型评高分，但critic只是预测它未来能获多少回报；reference又只负责比较策略偏离程度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2203.02155">原论文</a> · <a href="../../../../post-training/2203.02155-ppo-rlhf/">实现解读</a> · <a href="#qa-5003585127af1af3">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

在线采样、旧策略概率与当前策略更新之间，哪些量必须分开？

## 记住这一点

RL后训练先产生轨迹和奖励，再计算优势与更新目标。GRPO用同题一组回答的相对奖励替代独立critic；DAPO进一步处理裁剪、无效组和长度等训练问题。异步执行、离策略回放与训推引擎差异会改变采样分布，旧策略、当前策略和参考策略各有角色，不能把它们的概率混用。

## 一个例子

同一道题采样四个回答，奖励为0、0、1、1，组内相对优势能提供方向；若四个都错且奖励相同，仅靠标准组中心化得不到区分信号。把旧轨迹缓存下来继续训练时，当前概率仍在变化，不能连旧优势与密度比一起盲目复用。先核对目标是否需要重要性权重，以及权重对应哪个采样策略。

## 什么时候要小心

训练更稳定与任务能力更强需要不同证据。有限梯度、clip分支和概率比测试不能证明推理提升；离线样本上的低损失也不能替代真实rollout对照。涉及真实checkpoint和长轨迹的完整实验，继续服从成本与GPU证据边界，不因公式能执行而视为训练完成。

## 先读这几篇

先读GRPO，区分采样、优势、ratio和参考KL；再读DAPO，观察零方差组与训练稳定性的处理；最后读TIS，把实际采样引擎和训练引擎的概率口径纳入检查。

1. [DeepSeekMath / GRPO](../../../post-training/2402.03300-grpo/README.md) · [原论文](https://arxiv.org/abs/2402.03300)
2. [DAPO](../../../post-training/2503.14476-dapo/README.md) · [原论文](https://arxiv.org/abs/2503.14476)
3. [TIS](../../../post-training/web-2025-tis/README.md) · [原始资料](https://fengyao.notion.site/off-policy-rl)

## 自测一下

同一组回答奖励全相同，增大batch或多算几次相同的组内优势能产生新的学习方向吗？

??? note "展开参考答案"

    标准组中心化下不会自动产生区分。需要检查奖励是否过粗、问题难度是否合适、是否该重新采样或引入合规的额外信号；不能通过读取测试答案制造非零优势。任何改法都要重新核对目标和预算。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
