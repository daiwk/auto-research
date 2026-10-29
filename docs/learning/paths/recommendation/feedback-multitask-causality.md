---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 学习信号、多任务与反馈偏差

[搜广推](index.md) / 144 个问题 · 36 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

[阅读本主题精读卡片：多篇论文对比、分析与问答](../../deep-dives/recommendation/feedback-multitask-causality.md)

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
<p class="ar-learning-status" data-learning-status role="status">144 个问题 · 36 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:kl-mopd" data-paper-title="KL-MOPD: Discrepancy-Aware Multi-Objective On-Policy Distillation for Generative Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="KL-MOPD: Discrepancy-Aware Multi-Objective On-Policy Distillation for Generative Recommendation 搜广推与 LLM 应用 Zhejiang University 2026-10-27 生成式推荐必须连续生成一个商品的多个语义 token；某个位置没学到转化教师的偏好，就可能使整个商品无法召回。把点击教师和价值教师每一步都按一半融合，忽略了两者在不同位置的学习难度可能相反。KL-MOPD先在冻结的初始学生生成前缀上，按位置估计学生到两位教师的反向 KL。该差距只校准一次，归一化后作为固定教师权重；训练时在当前学生自己的前缀上计算加权反向 KL。不应改成逐步动态重算，也不是先平均教师概率再蒸馏。 完整训练与生产实验成本过高，不复现（审查 DONE）；本地为 L1 可微损失组件 / diagnostic only，不是完整推荐器或在线采样器。完整训练与生产实验成本过高，不复现（审查 DONE）；未接入 Evolve。calibrate_weights和kl_mopd_loss保留完整词表的KL方向、固定逐位置权重、教师冻结及两级聚合。独立概率域参考、反向/正向KL负控、动态重校准负控、padding零梯度与真实学生更新均可检查。  多目标蒸馏 生成式推荐 搜广推 学习信号、多任务与反馈偏差 KL-MOPD为什么在每个SID位置区分两位教师的学习难度？ 完整商品ID需要多个token都选对。点击教师在前几个位置容易模仿、价值教师在后几个位置容易模仿，不代表整条ID都学好了。固定一半权重忽略这种位置差异，方法用初始学生到各教师的KL差距为难学的一方加权。 教学例：三段商品码第一段区分类别、后两段区分属性。某教师只在类别段与学生差很远，不能把整条序列的同一个教师权重套到所有位置。 2026-10-29">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-kl-mopd-35d8ffea" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-225530c49babcf34">KL-MOPD为什么在每个SID位置区分两位教师的学习难度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Akl-mopd">KL-MOPD: Discrepancy-Aware Multi-Objective On-Policy Distillation for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-29 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>完整商品ID需要多个token都选对。点击教师在前几个位置容易模仿、价值教师在后几个位置容易模仿，不代表整条ID都学好了。固定一半权重忽略这种位置差异，方法用初始学生到各教师的KL差距为难学的一方加权。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：三段商品码第一段区分类别、后两段区分属性。某教师只在类别段与学生差很远，不能把整条序列的同一个教师权重套到所有位置。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.36973v1">原论文</a> · <a href="../../../../recommendation-components/2610.36973-kl-mopd/">实现解读</a> · <a href="#qa-225530c49babcf34">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:kl-mopd" data-paper-title="KL-MOPD: Discrepancy-Aware Multi-Objective On-Policy Distillation for Generative Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="KL-MOPD: Discrepancy-Aware Multi-Objective On-Policy Distillation for Generative Recommendation 搜广推与 LLM 应用 Zhejiang University 2026-10-27 生成式推荐必须连续生成一个商品的多个语义 token；某个位置没学到转化教师的偏好，就可能使整个商品无法召回。把点击教师和价值教师每一步都按一半融合，忽略了两者在不同位置的学习难度可能相反。KL-MOPD先在冻结的初始学生生成前缀上，按位置估计学生到两位教师的反向 KL。该差距只校准一次，归一化后作为固定教师权重；训练时在当前学生自己的前缀上计算加权反向 KL。不应改成逐步动态重算，也不是先平均教师概率再蒸馏。 完整训练与生产实验成本过高，不复现（审查 DONE）；本地为 L1 可微损失组件 / diagnostic only，不是完整推荐器或在线采样器。完整训练与生产实验成本过高，不复现（审查 DONE）；未接入 Evolve。calibrate_weights和kl_mopd_loss保留完整词表的KL方向、固定逐位置权重、教师冻结及两级聚合。独立概率域参考、反向/正向KL负控、动态重校准负控、padding零梯度与真实学生更新均可检查。  多目标蒸馏 生成式推荐 搜广推 学习信号、多任务与反馈偏差 KL-MOPD的alpha来自当前学生，还是冻结初始学生？ 来自冻结初始学生在自身采样前缀上的校准差距，只在训练前估计一次。后续损失使用当前学生的前缀，但不随当前模型重新计算alpha；动态权重属于另一个目标。 教学例：初始某位置KL为1和3，权重固定为1/4、3/4。训练后差距变成2和1，也不自动交换这两个权重。 2026-10-29">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-dd274eb36d8c0d0d">KL-MOPD的alpha来自当前学生，还是冻结初始学生？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Akl-mopd">KL-MOPD: Discrepancy-Aware Multi-Objective On-Policy Distillation for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-29 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>来自冻结初始学生在自身采样前缀上的校准差距，只在训练前估计一次。后续损失使用当前学生的前缀，但不随当前模型重新计算alpha；动态权重属于另一个目标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：初始某位置KL为1和3，权重固定为1/4、3/4。训练后差距变成2和1，也不自动交换这两个权重。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.36973v1">原论文</a> · <a href="../../../../recommendation-components/2610.36973-kl-mopd/">实现解读</a> · <a href="#qa-dd274eb36d8c0d0d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:kl-mopd" data-paper-title="KL-MOPD: Discrepancy-Aware Multi-Objective On-Policy Distillation for Generative Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="KL-MOPD: Discrepancy-Aware Multi-Objective On-Policy Distillation for Generative Recommendation 搜广推与 LLM 应用 Zhejiang University 2026-10-27 生成式推荐必须连续生成一个商品的多个语义 token；某个位置没学到转化教师的偏好，就可能使整个商品无法召回。把点击教师和价值教师每一步都按一半融合，忽略了两者在不同位置的学习难度可能相反。KL-MOPD先在冻结的初始学生生成前缀上，按位置估计学生到两位教师的反向 KL。该差距只校准一次，归一化后作为固定教师权重；训练时在当前学生自己的前缀上计算加权反向 KL。不应改成逐步动态重算，也不是先平均教师概率再蒸馏。 完整训练与生产实验成本过高，不复现（审查 DONE）；本地为 L1 可微损失组件 / diagnostic only，不是完整推荐器或在线采样器。完整训练与生产实验成本过高，不复现（审查 DONE）；未接入 Evolve。calibrate_weights和kl_mopd_loss保留完整词表的KL方向、固定逐位置权重、教师冻结及两级聚合。独立概率域参考、反向/正向KL负控、动态重校准负控、padding零梯度与真实学生更新均可检查。  多目标蒸馏 生成式推荐 搜广推 学习信号、多任务与反馈偏差 加权两项反向KL，等于把两位教师概率平均后算一次KL吗？ 一般不等价。加权的是学生到各教师的KL损失，而不是先做概率算术平均。方向还必须是KL(student||teacher)，不能换成教师到学生的正向KL。本地负控检查这两种计算不被混淆，不据此推出推荐收益。 教学例：两教师分别偏好不同token，算术混合会给两个峰都留质量；加权反向KL涉及对数教师分布，得到的梯度并不相同。 2026-10-29">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e1b61ee586eb6c08">加权两项反向KL，等于把两位教师概率平均后算一次KL吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Akl-mopd">KL-MOPD: Discrepancy-Aware Multi-Objective On-Policy Distillation for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-29 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一般不等价。加权的是学生到各教师的KL损失，而不是先做概率算术平均。方向还必须是KL(student||teacher)，不能换成教师到学生的正向KL。本地负控检查这两种计算不被混淆，不据此推出推荐收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：两教师分别偏好不同token，算术混合会给两个峰都留质量；加权反向KL涉及对数教师分布，得到的梯度并不相同。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.36973v1">原论文</a> · <a href="../../../../recommendation-components/2610.36973-kl-mopd/">实现解读</a> · <a href="#qa-e1b61ee586eb6c08">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:kl-mopd" data-paper-title="KL-MOPD: Discrepancy-Aware Multi-Objective On-Policy Distillation for Generative Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="KL-MOPD: Discrepancy-Aware Multi-Objective On-Policy Distillation for Generative Recommendation 搜广推与 LLM 应用 Zhejiang University 2026-10-27 生成式推荐必须连续生成一个商品的多个语义 token；某个位置没学到转化教师的偏好，就可能使整个商品无法召回。把点击教师和价值教师每一步都按一半融合，忽略了两者在不同位置的学习难度可能相反。KL-MOPD先在冻结的初始学生生成前缀上，按位置估计学生到两位教师的反向 KL。该差距只校准一次，归一化后作为固定教师权重；训练时在当前学生自己的前缀上计算加权反向 KL。不应改成逐步动态重算，也不是先平均教师概率再蒸馏。 完整训练与生产实验成本过高，不复现（审查 DONE）；本地为 L1 可微损失组件 / diagnostic only，不是完整推荐器或在线采样器。完整训练与生产实验成本过高，不复现（审查 DONE）；未接入 Evolve。calibrate_weights和kl_mopd_loss保留完整词表的KL方向、固定逐位置权重、教师冻结及两级聚合。独立概率域参考、反向/正向KL负控、动态重校准负控、padding零梯度与真实学生更新均可检查。  多目标蒸馏 生成式推荐 搜广推 学习信号、多任务与反馈偏差 张量损失通过梯度检查，为什么还不能称已实现on-policy推荐训练？ 内核只看输入logits，不知道前缀由谁采样。初始学生校准、当前学生在线生成、冻结教师评分、语义ID解码和真实数据切分都需要外部链路。当前只有损失组件与小张量CPU/CUDA机制证据，没有推荐器能力比较。 教学例：把一份缓存的旧模型前缀传进来，公式依然能计算，但调用者不能把它声明为当前学生的在线采样。 2026-10-29">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f943ef4c424b8aa8">张量损失通过梯度检查，为什么还不能称已实现on-policy推荐训练？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Akl-mopd">KL-MOPD: Discrepancy-Aware Multi-Objective On-Policy Distillation for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-29 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>内核只看输入logits，不知道前缀由谁采样。初始学生校准、当前学生在线生成、冻结教师评分、语义ID解码和真实数据切分都需要外部链路。当前只有损失组件与小张量CPU/CUDA机制证据，没有推荐器能力比较。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：把一份缓存的旧模型前缀传进来，公式依然能计算，但调用者不能把它声明为当前学生的在线采样。</p>
<p class="ar-learning-sources">依据：本地复现与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.36973v1">原论文</a> · <a href="../../../../recommendation-components/2610.36973-kl-mopd/">实现解读</a> · <a href="#qa-f943ef4c424b8aa8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hge" data-paper-title="Hierarchical GTV Estimation: Bridging the Gap between Container-Level Ranking and Item-Level Conversion" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Hierarchical GTV Estimation: Bridging the Gap between Container-Level Ranking and Item-Level Conversion 搜广推与 LLM 应用 Meituan 2026-10-23 搜索广告排序的是门店、直播间等“容器”，成交却发生在内部商品上。单条成交金额既稀疏又高方差，简单把门店当成一个商品，容易忽略低价高频与高价低频商品的组合。HGE 先用 Hybrid Set-Aware Encoder 编码 top-K 商品的竞争关系，再在自注意力之后拼入用户、门店、上下文与查询。Proxy-Label Learning 分开预测门店是否成交、成交后每个商品的购买概率和数量； 论文私有日志训练和线上实验成本过高，不复现（审查 DONE）；实现范围为 HSAE、PLL、RCEF 的可微 L1 组件，不是完整广告模型。论文私有日志训练和线上实验成本过高，不复现（审查 DONE）；不据此宣称本地获得线上收益或接入 Evolve。HierarchicalGTV 接受外部商品 embedding、位置向量、上下文、价格和通用回归输出，不收答案/成交标签。以小尺寸可微模块验证：独立逐商品 Eq.5 参考、上下文不影响前置 MHSA、位置/价格/残差移除负控、融合两端点、商品概率之和可大于1、所有参数和输入的有限非零梯度。种子为42/43/44；指标只是合成机制误差和梯度，不是推荐准确率、收入或校准效果。  广告价值预估 层次化多任务学习 搜广推 学习信号、多任务与反馈偏差 HGE 的 top-K 商品是要展示的 K 个推荐结果，还是同一容器内部的输入？ 是同一候选门店或直播间内部的商品输入，模型最终估计的是容器价值。不同容器各有自己的商品集合，集合注意力先描述内部关系，再拼接用户、查询等上下文。top-K 只覆盖部分库存，不等于整店全部商品，更不是一次直接输出 K 家门店。 示意：两家店各输入三件商品，总共六件内部商品参与编码，最终仍得到两家店的价值分数；不能把这六件商品误当最终推荐列表。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-hge-0554c3a1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c32f38715552fb0a">HGE 的 top-K 商品是要展示的 K 个推荐结果，还是同一容器内部的输入？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahge">Hierarchical GTV Estimation: Bridging the Gap between Container-Level Ranking and Item-Level Conversion</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>是同一候选门店或直播间内部的商品输入，模型最终估计的是容器价值。不同容器各有自己的商品集合，集合注意力先描述内部关系，再拼接用户、查询等上下文。top-K 只覆盖部分库存，不等于整店全部商品，更不是一次直接输出 K 家门店。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两家店各输入三件商品，总共六件内部商品参与编码，最终仍得到两家店的价值分数；不能把这六件商品误当最终推荐列表。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32420v1">原论文</a> · <a href="../../../../recommendation-components/2610.32420-hge/">实现解读</a> · <a href="#qa-c32f38715552fb0a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hge" data-paper-title="Hierarchical GTV Estimation: Bridging the Gap between Container-Level Ranking and Item-Level Conversion" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Hierarchical GTV Estimation: Bridging the Gap between Container-Level Ranking and Item-Level Conversion 搜广推与 LLM 应用 Meituan 2026-10-23 搜索广告排序的是门店、直播间等“容器”，成交却发生在内部商品上。单条成交金额既稀疏又高方差，简单把门店当成一个商品，容易忽略低价高频与高价低频商品的组合。HGE 先用 Hybrid Set-Aware Encoder 编码 top-K 商品的竞争关系，再在自注意力之后拼入用户、门店、上下文与查询。Proxy-Label Learning 分开预测门店是否成交、成交后每个商品的购买概率和数量； 论文私有日志训练和线上实验成本过高，不复现（审查 DONE）；实现范围为 HSAE、PLL、RCEF 的可微 L1 组件，不是完整广告模型。论文私有日志训练和线上实验成本过高，不复现（审查 DONE）；不据此宣称本地获得线上收益或接入 Evolve。HierarchicalGTV 接受外部商品 embedding、位置向量、上下文、价格和通用回归输出，不收答案/成交标签。以小尺寸可微模块验证：独立逐商品 Eq.5 参考、上下文不影响前置 MHSA、位置/价格/残差移除负控、融合两端点、商品概率之和可大于1、所有参数和输入的有限非零梯度。种子为42/43/44；指标只是合成机制误差和梯度，不是推荐准确率、收入或校准效果。  广告价值预估 层次化多任务学习 搜广推 学习信号、多任务与反馈偏差 HGE为什么分别预测容器成交、内部商品购买概率和数量，而不只回归一个门店GMV？ 容器价值来自内部商品组合，单一金额标签稀疏且波动大。分解让模型先表达是否成交，再累加不同商品的条件购买与数量，并以残差补偿top-K遗漏；商品不是互斥选择，不能把独立购买概率改成总和为一的softmax。融合门必须读取上下文，不能按真实成交标签事后选支路。 示意：用户可能在同一店同时买两件低价商品，或只买一件高价商品；把内部商品视作互斥类别会漏掉多件购买，单一门店回归又难解释这些来源差异。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hge" data-paper-title="Hierarchical GTV Estimation: Bridging the Gap between Container-Level Ranking and Item-Level Conversion" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Hierarchical GTV Estimation: Bridging the Gap between Container-Level Ranking and Item-Level Conversion 搜广推与 LLM 应用 Meituan 2026-10-23 搜索广告排序的是门店、直播间等“容器”，成交却发生在内部商品上。单条成交金额既稀疏又高方差，简单把门店当成一个商品，容易忽略低价高频与高价低频商品的组合。HGE 先用 Hybrid Set-Aware Encoder 编码 top-K 商品的竞争关系，再在自注意力之后拼入用户、门店、上下文与查询。Proxy-Label Learning 分开预测门店是否成交、成交后每个商品的购买概率和数量； 论文私有日志训练和线上实验成本过高，不复现（审查 DONE）；实现范围为 HSAE、PLL、RCEF 的可微 L1 组件，不是完整广告模型。论文私有日志训练和线上实验成本过高，不复现（审查 DONE）；不据此宣称本地获得线上收益或接入 Evolve。HierarchicalGTV 接受外部商品 embedding、位置向量、上下文、价格和通用回归输出，不收答案/成交标签。以小尺寸可微模块验证：独立逐商品 Eq.5 参考、上下文不影响前置 MHSA、位置/价格/残差移除负控、融合两端点、商品概率之和可大于1、所有参数和输入的有限非零梯度。种子为42/43/44；指标只是合成机制误差和梯度，不是推荐准确率、收入或校准效果。  广告价值预估 层次化多任务学习 搜广推 学习信号、多任务与反馈偏差 HGE 的商品购买 sigmoid 与互斥 softmax，为什么对应不同业务假设？ 用户成交后可能购买多件不同商品，sigmoid 允许各商品同时有高概率；softmax 强迫总和为一，等于只选一个，改变交易组合。数量头也不能被类别概率替代。原文定义在这里比常见分类代码习惯更重要，替换激活会改算法。 示意：用户在一家店同时买咖啡和面包，两项都可购买；softmax 会让提高咖啡概率压低面包，不符合多商品同单成交。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-96dc7e4b12d4bae4">HGE 的商品购买 sigmoid 与互斥 softmax，为什么对应不同业务假设？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahge">Hierarchical GTV Estimation: Bridging the Gap between Container-Level Ranking and Item-Level Conversion</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用户成交后可能购买多件不同商品，sigmoid 允许各商品同时有高概率；softmax 强迫总和为一，等于只选一个，改变交易组合。数量头也不能被类别概率替代。原文定义在这里比常见分类代码习惯更重要，替换激活会改算法。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户在一家店同时买咖啡和面包，两项都可购买；softmax 会让提高咖啡概率压低面包，不符合多商品同单成交。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32420v1">原论文</a> · <a href="../../../../recommendation-components/2610.32420-hge/">实现解读</a> · <a href="#qa-96dc7e4b12d4bae4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hge" data-paper-title="Hierarchical GTV Estimation: Bridging the Gap between Container-Level Ranking and Item-Level Conversion" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Hierarchical GTV Estimation: Bridging the Gap between Container-Level Ranking and Item-Level Conversion 搜广推与 LLM 应用 Meituan 2026-10-23 搜索广告排序的是门店、直播间等“容器”，成交却发生在内部商品上。单条成交金额既稀疏又高方差，简单把门店当成一个商品，容易忽略低价高频与高价低频商品的组合。HGE 先用 Hybrid Set-Aware Encoder 编码 top-K 商品的竞争关系，再在自注意力之后拼入用户、门店、上下文与查询。Proxy-Label Learning 分开预测门店是否成交、成交后每个商品的购买概率和数量； 论文私有日志训练和线上实验成本过高，不复现（审查 DONE）；实现范围为 HSAE、PLL、RCEF 的可微 L1 组件，不是完整广告模型。论文私有日志训练和线上实验成本过高，不复现（审查 DONE）；不据此宣称本地获得线上收益或接入 Evolve。HierarchicalGTV 接受外部商品 embedding、位置向量、上下文、价格和通用回归输出，不收答案/成交标签。以小尺寸可微模块验证：独立逐商品 Eq.5 参考、上下文不影响前置 MHSA、位置/价格/残差移除负控、融合两端点、商品概率之和可大于1、所有参数和输入的有限非零梯度。种子为42/43/44；指标只是合成机制误差和梯度，不是推荐准确率、收入或校准效果。  广告价值预估 层次化多任务学习 搜广推 学习信号、多任务与反馈偏差 HGE 残差与融合 gate 为什么不能按真实成交标签硬切路？ 残差可正可负，用于补偿 top-K 模型误差，不应擅自非负截断；融合权重只依曝光前上下文逐样本预测，不能利用事后真实成交挑更准分支。来源组件没有完整多任务训练配方，对输出平方求导只算梯度诊断。 示意：测试后知道门店成交才选商品分解分支，会让结果虚高；应由请求时已有上下文决定 gate，允许残差纠正高估也纠正低估。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-18f65c0f1ef11458">HGE 残差与融合 gate 为什么不能按真实成交标签硬切路？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahge">Hierarchical GTV Estimation: Bridging the Gap between Container-Level Ranking and Item-Level Conversion</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>残差可正可负，用于补偿 top-K 模型误差，不应擅自非负截断；融合权重只依曝光前上下文逐样本预测，不能利用事后真实成交挑更准分支。来源组件没有完整多任务训练配方，对输出平方求导只算梯度诊断。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>测试后知道门店成交才选商品分解分支，会让结果虚高；应由请求时已有上下文决定 gate，允许残差纠正高估也纠正低估。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32420v1">原论文</a> · <a href="../../../../recommendation-components/2610.32420-hge/">实现解读</a> · <a href="#qa-18f65c0f1ef11458">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:baseline-incremental" data-paper-title="Baseline and Incremental: User, Item, and Request Debiasing in Instagram Feed Ranking" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Baseline and Incremental: User, Item, and Request Debiasing in Instagram Feed Ranking 搜广推与 LLM 应用 Meta 2026-10-20 参与度预测同时包含用户习惯、商品受欢迎程度、当前候选池水平和候选自身的相对优势。直接去掉基线可能丢失有用的绝对水平。论文保留原始预测，同时对相对基线的非线性增量单独加权；这是评分配置变化，不是因果uplift估计。用户、商品基线来自历史特征，请求基线来自当前候选池。概率使用log-odds差，回归量使用同单位差；正向门和降权门的幅度不同，不能把乘预测值的正向门直接改符号用于降权，否则预测接近零时惩罚也消失。 完整私有日志、排名系统及线上消融成本过高，不复现（审查 DONE）。仅为L1机制诊断，不是线上收益复现；已实现评分算子，不新增或训练排名网络。仅为L1机制诊断，不是线上收益复现；完整私有日志、排名系统及线上消融成本过高，不复现（审查 DONE）。运行独立有理式参考、hinge与sigmoid区别、预测地板降权和移除增量项的排序负对照，seed42/43/44。输入为合成分数，不读取生产数据，不拟合或选择线上权重，不将数组排序改变解释为推荐提升。request_baseline只计算调用方指定的池内统计，不自行学会选择基线。  排序与决策优化 基线与增量去偏 搜广推 学习信号、多任务与反馈偏差 Baseline-Incremental 中的用户、商品和请求基线分别代表哪种相对参照？ 用户基线描述惯常响应，商品基线描述普遍吸引力，请求基线描述当前候选池水平。增量衡量候选相对某种参照的突出程度，原始预测保留绝对价值。它是评分配置，不是干预实验的因果 uplift，参照选错会改变排序含义。 示意：高活跃用户对所有视频都易点击，其中一条仅略高于个人习惯；低活跃用户的一次中等点击概率可能更突出，但两者绝对价值仍应保留。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-baseline-incremental-a452c157" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-92981c6733d15b6c">Baseline-Incremental 中的用户、商品和请求基线分别代表哪种相对参照？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Abaseline-incremental">Baseline and Incremental: User, Item, and Request Debiasing in Instagram Feed Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用户基线描述惯常响应，商品基线描述普遍吸引力，请求基线描述当前候选池水平。增量衡量候选相对某种参照的突出程度，原始预测保留绝对价值。它是评分配置，不是干预实验的因果 uplift，参照选错会改变排序含义。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>高活跃用户对所有视频都易点击，其中一条仅略高于个人习惯；低活跃用户的一次中等点击概率可能更突出，但两者绝对价值仍应保留。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.27423v1">原论文</a> · <a href="../../../../recommendation-components/2610.27423-baseline-incremental/">实现解读</a> · <a href="#qa-92981c6733d15b6c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:baseline-incremental" data-paper-title="Baseline and Incremental: User, Item, and Request Debiasing in Instagram Feed Ranking" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Baseline and Incremental: User, Item, and Request Debiasing in Instagram Feed Ranking 搜广推与 LLM 应用 Meta 2026-10-20 参与度预测同时包含用户习惯、商品受欢迎程度、当前候选池水平和候选自身的相对优势。直接去掉基线可能丢失有用的绝对水平。论文保留原始预测，同时对相对基线的非线性增量单独加权；这是评分配置变化，不是因果uplift估计。用户、商品基线来自历史特征，请求基线来自当前候选池。概率使用log-odds差，回归量使用同单位差；正向门和降权门的幅度不同，不能把乘预测值的正向门直接改符号用于降权，否则预测接近零时惩罚也消失。 完整私有日志、排名系统及线上消融成本过高，不复现（审查 DONE）。仅为L1机制诊断，不是线上收益复现；已实现评分算子，不新增或训练排名网络。仅为L1机制诊断，不是线上收益复现；完整私有日志、排名系统及线上消融成本过高，不复现（审查 DONE）。运行独立有理式参考、hinge与sigmoid区别、预测地板降权和移除增量项的排序负对照，seed42/43/44。输入为合成分数，不读取生产数据，不拟合或选择线上权重，不将数组排序改变解释为推荐提升。request_baseline只计算调用方指定的池内统计，不自行学会选择基线。  排序与决策优化 基线与增量去偏 搜广推 学习信号、多任务与反馈偏差 已经减去用户或商品基线，为什么还要保留原始预测项？ 相对基线表示候选超出常态的程度，原始预测保留真实业务量级，两者提供不同信息。方法为非线性增量单独设权重，概率在log-odds空间比较，回归量用同单位差；它是评分配置，不是因果uplift。若只按相对改善排，低基线上的小绝对收益可能压过高价值候选。 示意：候选A从低基线略升，候选B本来就有较高购买概率；只看相对变化会偏向A，保留绝对预测才能同时表达高基线的真实价值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:baseline-incremental" data-paper-title="Baseline and Incremental: User, Item, and Request Debiasing in Instagram Feed Ranking" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Baseline and Incremental: User, Item, and Request Debiasing in Instagram Feed Ranking 搜广推与 LLM 应用 Meta 2026-10-20 参与度预测同时包含用户习惯、商品受欢迎程度、当前候选池水平和候选自身的相对优势。直接去掉基线可能丢失有用的绝对水平。论文保留原始预测，同时对相对基线的非线性增量单独加权；这是评分配置变化，不是因果uplift估计。用户、商品基线来自历史特征，请求基线来自当前候选池。概率使用log-odds差，回归量使用同单位差；正向门和降权门的幅度不同，不能把乘预测值的正向门直接改符号用于降权，否则预测接近零时惩罚也消失。 完整私有日志、排名系统及线上消融成本过高，不复现（审查 DONE）。仅为L1机制诊断，不是线上收益复现；已实现评分算子，不新增或训练排名网络。仅为L1机制诊断，不是线上收益复现；完整私有日志、排名系统及线上消融成本过高，不复现（审查 DONE）。运行独立有理式参考、hinge与sigmoid区别、预测地板降权和移除增量项的排序负对照，seed42/43/44。输入为合成分数，不读取生产数据，不拟合或选择线上权重，不将数组排序改变解释为推荐提升。request_baseline只计算调用方指定的池内统计，不自行学会选择基线。  排序与决策优化 基线与增量去偏 搜广推 学习信号、多任务与反馈偏差 为什么概率预测用 log-odds 差，而回归量用原单位差，不能统一直接相减？ 概率在接近零或一时同样绝对差的含义不同，logit 差表达赔率尺度上的相对变化；回归目标已有自然单位，可用直接差。两种变换对应不同评分响应，不能为了代码统一而混用。本方法也未因此获得因果解释，仍是设计的价值函数。 示意：点击率从百分之一到百分之二与从百分之四十到四十一虽都增一点，赔率变化不同；观看秒数则可直接比较多出的时间。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ca6aded4d44a4977">为什么概率预测用 log-odds 差，而回归量用原单位差，不能统一直接相减？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Abaseline-incremental">Baseline and Incremental: User, Item, and Request Debiasing in Instagram Feed Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>概率在接近零或一时同样绝对差的含义不同，logit 差表达赔率尺度上的相对变化；回归目标已有自然单位，可用直接差。两种变换对应不同评分响应，不能为了代码统一而混用。本方法也未因此获得因果解释，仍是设计的价值函数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>点击率从百分之一到百分之二与从百分之四十到四十一虽都增一点，赔率变化不同；观看秒数则可直接比较多出的时间。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.27423v1">原论文</a> · <a href="../../../../recommendation-components/2610.27423-baseline-incremental/">实现解读</a> · <a href="#qa-ca6aded4d44a4977">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:baseline-incremental" data-paper-title="Baseline and Incremental: User, Item, and Request Debiasing in Instagram Feed Ranking" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Baseline and Incremental: User, Item, and Request Debiasing in Instagram Feed Ranking 搜广推与 LLM 应用 Meta 2026-10-20 参与度预测同时包含用户习惯、商品受欢迎程度、当前候选池水平和候选自身的相对优势。直接去掉基线可能丢失有用的绝对水平。论文保留原始预测，同时对相对基线的非线性增量单独加权；这是评分配置变化，不是因果uplift估计。用户、商品基线来自历史特征，请求基线来自当前候选池。概率使用log-odds差，回归量使用同单位差；正向门和降权门的幅度不同，不能把乘预测值的正向门直接改符号用于降权，否则预测接近零时惩罚也消失。 完整私有日志、排名系统及线上消融成本过高，不复现（审查 DONE）。仅为L1机制诊断，不是线上收益复现；已实现评分算子，不新增或训练排名网络。仅为L1机制诊断，不是线上收益复现；完整私有日志、排名系统及线上消融成本过高，不复现（审查 DONE）。运行独立有理式参考、hinge与sigmoid区别、预测地板降权和移除增量项的排序负对照，seed42/43/44。输入为合成分数，不读取生产数据，不拟合或选择线上权重，不将数组排序改变解释为推荐提升。request_baseline只计算调用方指定的池内统计，不自行学会选择基线。  排序与决策优化 基线与增量去偏 搜广推 学习信号、多任务与反馈偏差 Baseline-Incremental 的降权门为什么不能简单给正向门取负号？ 正向门若以预测 p 为幅度，p 接近零时会自然消失；降权若照搬它，最需压低的低预测候选反而几乎没有惩罚。来源保留常数、gap 等幅度与分段极限，并要求 logit 前显式裁剪概率边界。实现必须按门类型分别核验，不静默合并。 示意：某候选 p 接近零，负 p 门惩罚也近零；常数降权仍可压制它。把两个门写成仅符号相反的一行代码，会丢掉这一行为差异。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ed719753753ebfda">Baseline-Incremental 的降权门为什么不能简单给正向门取负号？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Abaseline-incremental">Baseline and Incremental: User, Item, and Request Debiasing in Instagram Feed Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>正向门若以预测 p 为幅度，p 接近零时会自然消失；降权若照搬它，最需压低的低预测候选反而几乎没有惩罚。来源保留常数、gap 等幅度与分段极限，并要求 logit 前显式裁剪概率边界。实现必须按门类型分别核验，不静默合并。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某候选 p 接近零，负 p 门惩罚也近零；常数降权仍可压制它。把两个门写成仅符号相反的一行代码，会丢掉这一行为差异。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.27423v1">原论文</a> · <a href="../../../../recommendation-components/2610.27423-baseline-incremental/">实现解读</a> · <a href="#qa-ed719753753ebfda">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:casi" data-paper-title="CASI: Credit Assignment via Set Intervention for Agentic Retrieval" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="CASI: Credit Assignment via Set Intervention for Agentic Retrieval 搜广推与 LLM 应用 Xiaohongshu 2026-10-14 一次检索请求可能联合产生多个改写动作，线上却只返回整个结果集合的奖励。CASI 不把这个奖励简单均分：每个动作只检索一次，冻结候选快照，再重组子集、评估候选之间的协同与替代关系，以 Shapley 边际贡献分配信用。随后用共享尺度归一化与有界零和投影，将集合信用转为 action/token 优势。集合奖励广播仍可给出原集合目标的有效 score-function 估计；CASI 的内部优势塑形不能额外宣称保持同一无偏梯度。论文也指出：加性集合无需额外干预； 完整的私有拍卖重放、LLM 五次训练及生产 A/B：成本过高，不复现（审查 DONE）。默认诊断后端按固定分数对每个子集重新取 top-2，属于显式的 pr_rerun 敏感性示例，不是论文的私有 pr_filter 训练后端；本地对照口径：基线为相同冻结集合函数上的 Singleton 和 LOO，实验组为精确/置换 Shapley 与零和优势组件；没有策略训练，相对能力提升不适用。  agentic-retrieval credit-assignment policy-optimization 搜广推 学习信号、多任务与反馈偏差 CASI 为什么把“动作检索一次”与“子集重新评价”分开？ 重新检索会让动作结果随子集变化，信用差异可能来自后端随机性而非协同关系。先冻结每个动作的候选快照，再重组集合，才能在相同证据上比较边际贡献。子集评价可以反映替代与协同，但仍需明确评价后端的敏感性假设。 示意：两条 query 都召回同一商品，移除一条后集合可能不变；若重新检索突然换了商品，就无法分清信用改变来自冗余还是检索波动。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-casi-2c2b2f1b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-807a571ed774579f">CASI 为什么把“动作检索一次”与“子集重新评价”分开？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acasi">CASI: Credit Assignment via Set Intervention for Agentic Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>重新检索会让动作结果随子集变化，信用差异可能来自后端随机性而非协同关系。先冻结每个动作的候选快照，再重组集合，才能在相同证据上比较边际贡献。子集评价可以反映替代与协同，但仍需明确评价后端的敏感性假设。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两条 query 都召回同一商品，移除一条后集合可能不变；若重新检索突然换了商品，就无法分清信用改变来自冗余还是检索波动。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20293">原论文</a> · <a href="../../../../reproductions/2610.20293-casi/">实现解读</a> · <a href="#qa-807a571ed774579f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:casi" data-paper-title="CASI: Credit Assignment via Set Intervention for Agentic Retrieval" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="CASI: Credit Assignment via Set Intervention for Agentic Retrieval 搜广推与 LLM 应用 Xiaohongshu 2026-10-14 一次检索请求可能联合产生多个改写动作，线上却只返回整个结果集合的奖励。CASI 不把这个奖励简单均分：每个动作只检索一次，冻结候选快照，再重组子集、评估候选之间的协同与替代关系，以 Shapley 边际贡献分配信用。随后用共享尺度归一化与有界零和投影，将集合信用转为 action/token 优势。集合奖励广播仍可给出原集合目标的有效 score-function 估计；CASI 的内部优势塑形不能额外宣称保持同一无偏梯度。论文也指出：加性集合无需额外干预； 完整的私有拍卖重放、LLM 五次训练及生产 A/B：成本过高，不复现（审查 DONE）。默认诊断后端按固定分数对每个子集重新取 top-2，属于显式的 pr_rerun 敏感性示例，不是论文的私有 pr_filter 训练后端；本地对照口径：基线为相同冻结集合函数上的 Singleton 和 LOO，实验组为精确/置换 Shapley 与零和优势组件；没有策略训练，相对能力提升不适用。  agentic-retrieval credit-assignment policy-optimization 搜广推 学习信号、多任务与反馈偏差 CASI为什么冻结检索快照后重组子集，而不把集合奖励平均分给各动作？ 多个改写动作的候选可能互相补充或替代，均分奖励会掩盖这种作用。CASI固定每个动作一次检索的结果，比较它加入不同子集时的边际价值，再用Shapley信用塑形优势。冻结快照避免重复检索噪声污染归因，但这种内部塑形不能额外声称保留原集合目标的同一无偏梯度。 示意：改写A与B返回相同商品，C补出新类目；三者平分奖励会高估重复动作。固定结果后移除或加入不同组合，才能看出C的互补贡献。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:casi" data-paper-title="CASI: Credit Assignment via Set Intervention for Agentic Retrieval" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="CASI: Credit Assignment via Set Intervention for Agentic Retrieval 搜广推与 LLM 应用 Xiaohongshu 2026-10-14 一次检索请求可能联合产生多个改写动作，线上却只返回整个结果集合的奖励。CASI 不把这个奖励简单均分：每个动作只检索一次，冻结候选快照，再重组子集、评估候选之间的协同与替代关系，以 Shapley 边际贡献分配信用。随后用共享尺度归一化与有界零和投影，将集合信用转为 action/token 优势。集合奖励广播仍可给出原集合目标的有效 score-function 估计；CASI 的内部优势塑形不能额外宣称保持同一无偏梯度。论文也指出：加性集合无需额外干预； 完整的私有拍卖重放、LLM 五次训练及生产 A/B：成本过高，不复现（审查 DONE）。默认诊断后端按固定分数对每个子集重新取 top-2，属于显式的 pr_rerun 敏感性示例，不是论文的私有 pr_filter 训练后端；本地对照口径：基线为相同冻结集合函数上的 Singleton 和 LOO，实验组为精确/置换 Shapley 与零和优势组件；没有策略训练，相对能力提升不适用。  agentic-retrieval credit-assignment policy-optimization 搜广推 学习信号、多任务与反馈偏差 CASI 的 Shapley 信用与 Singleton、LOO 在四个以上动作时为何不能一般互推？ Singleton 只看单动作价值，LOO 只看完整集合删除一个动作的端点；Shapley 平均所有联盟下的边际贡献，中间子集包含高阶协同。端点相同的集合函数仍可在中间联盟不同，因此两种端点不能通常恢复完整信用。加性情形则不需要额外干预。 示意：两个 query 单独无效但合起来覆盖需求，第三条可替代其中一条。只看单条或整组移除，可能漏掉这份依赖，需要比较不同联盟。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b413a4921e7951f0">CASI 的 Shapley 信用与 Singleton、LOO 在四个以上动作时为何不能一般互推？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acasi">CASI: Credit Assignment via Set Intervention for Agentic Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Singleton 只看单动作价值，LOO 只看完整集合删除一个动作的端点；Shapley 平均所有联盟下的边际贡献，中间子集包含高阶协同。端点相同的集合函数仍可在中间联盟不同，因此两种端点不能通常恢复完整信用。加性情形则不需要额外干预。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个 query 单独无效但合起来覆盖需求，第三条可替代其中一条。只看单条或整组移除，可能漏掉这份依赖，需要比较不同联盟。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20293">原论文</a> · <a href="../../../../reproductions/2610.20293-casi/">实现解读</a> · <a href="#qa-b413a4921e7951f0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:casi" data-paper-title="CASI: Credit Assignment via Set Intervention for Agentic Retrieval" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="CASI: Credit Assignment via Set Intervention for Agentic Retrieval 搜广推与 LLM 应用 Xiaohongshu 2026-10-14 一次检索请求可能联合产生多个改写动作，线上却只返回整个结果集合的奖励。CASI 不把这个奖励简单均分：每个动作只检索一次，冻结候选快照，再重组子集、评估候选之间的协同与替代关系，以 Shapley 边际贡献分配信用。随后用共享尺度归一化与有界零和投影，将集合信用转为 action/token 优势。集合奖励广播仍可给出原集合目标的有效 score-function 估计；CASI 的内部优势塑形不能额外宣称保持同一无偏梯度。论文也指出：加性集合无需额外干预； 完整的私有拍卖重放、LLM 五次训练及生产 A/B：成本过高，不复现（审查 DONE）。默认诊断后端按固定分数对每个子集重新取 top-2，属于显式的 pr_rerun 敏感性示例，不是论文的私有 pr_filter 训练后端；本地对照口径：基线为相同冻结集合函数上的 Singleton 和 LOO，实验组为精确/置换 Shapley 与零和优势组件；没有策略训练，相对能力提升不适用。  agentic-retrieval credit-assignment policy-optimization 搜广推 学习信号、多任务与反馈偏差 CASI 的有界零和优势为什么要联合投影，而不是逐维 clip 后直接使用？ 逐维裁剪会破坏总和为零，动作优势均值不再等于原 rollout 优势。联合投影求一个共享偏移 λ，再裁剪各维，使界限与零和同时成立。保持的是动作算术均值，非按 token 长度加权均值，也不保证塑形保持原目标无偏梯度。 示意：三个动作优势二、负一、负一，逐维限到一后总和变负；先求共同偏移再裁剪，才能保留总和为零而又不超过边界。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-beb70d44bd05caec">CASI 的有界零和优势为什么要联合投影，而不是逐维 clip 后直接使用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acasi">CASI: Credit Assignment via Set Intervention for Agentic Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>逐维裁剪会破坏总和为零，动作优势均值不再等于原 rollout 优势。联合投影求一个共享偏移 λ，再裁剪各维，使界限与零和同时成立。保持的是动作算术均值，非按 token 长度加权均值，也不保证塑形保持原目标无偏梯度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三个动作优势二、负一、负一，逐维限到一后总和变负；先求共同偏移再裁剪，才能保留总和为零而又不超过边界。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20293">原论文</a> · <a href="../../../../reproductions/2610.20293-casi/">实现解读</a> · <a href="#qa-beb70d44bd05caec">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:promptshift" data-paper-title="Measuring and Mitigating Identity-Cue Preference Drift in LLM-based Recommender Systems" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Measuring and Mitigating Identity-Cue Preference Drift in LLM-based Recommender Systems 搜广推与 LLM 应用 University of Electronic Science and Technology of China 2026-09-28 在行为历史不变时比较身份提示与无身份参考列表，用 Drift 与 SliceShift 量化身份线索偏移，再依据用户主流度自适应混合原分与逆群体流行度。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行列表指标与后处理 reranker；身份 slice 和相关性由公开 fixture 给出，不生成真实用户画像。执行列表指标与后处理 reranker；身份 slice 和相关性由公开 fixture 给出，不生成真实用户画像。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  llm-recommendation identity-cue-drift fairness 搜广推 学习信号、多任务与反馈偏差 PromptShift 发现列表 Drift 很大，能直接断定推荐准确率下降吗？ 不能。Drift 描述相对参考列表改变多少，不含每个新旧物品是否更相关的完整判断。新列表可能更好、更差或只是不同；SliceShift 也只补群体流行度方向。若要讨论质量，需要独立相关性或用户反馈证据，不能把敏感性指标直接改名为准确率损失。 示意：两部同样适合用户的电影互换会增加位次漂移，却未必伤体验；换成无关热门片也会漂移，但要靠相关性评价才能分清。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-promptshift-7e539145" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-12d0a4e2ffd1606c">PromptShift 发现列表 Drift 很大，能直接断定推荐准确率下降吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apromptshift">Measuring and Mitigating Identity-Cue Preference Drift in LLM-based Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Electronic Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。Drift 描述相对参考列表改变多少，不含每个新旧物品是否更相关的完整判断。新列表可能更好、更差或只是不同；SliceShift 也只补群体流行度方向。若要讨论质量，需要独立相关性或用户反馈证据，不能把敏感性指标直接改名为准确率损失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两部同样适合用户的电影互换会增加位次漂移，却未必伤体验；换成无关热门片也会漂移，但要靠相关性评价才能分清。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34229">原论文</a> · <a href="../../../../reproductions/2609.34229-promptshift/">实现解读</a> · <a href="#qa-12d0a4e2ffd1606c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:promptshift" data-paper-title="Measuring and Mitigating Identity-Cue Preference Drift in LLM-based Recommender Systems" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Measuring and Mitigating Identity-Cue Preference Drift in LLM-based Recommender Systems 搜广推与 LLM 应用 University of Electronic Science and Technology of China 2026-09-28 在行为历史不变时比较身份提示与无身份参考列表，用 Drift 与 SliceShift 量化身份线索偏移，再依据用户主流度自适应混合原分与逆群体流行度。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行列表指标与后处理 reranker；身份 slice 和相关性由公开 fixture 给出，不生成真实用户画像。执行列表指标与后处理 reranker；身份 slice 和相关性由公开 fixture 给出，不生成真实用户画像。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  llm-recommendation identity-cue-drift fairness 搜广推 学习信号、多任务与反馈偏差 PromptShift 为什么固定行为历史，只改变身份提示，再分别测量 Drift 与 SliceShift？ 同时更改历史和身份无法区分列表变化来自真实偏好还是身份线索。固定历史后，Drift 描述列表重叠与位次变化，SliceShift 描述群体流行度方向的变化，再按主流度调整相关性和逆流行度混合。它提供受控敏感性诊断，不足以单独证明社会因果歧视；本地也明确只做诊断。 示意：同一段电影观看历史分别附上与不附上身份描述，比较推荐是否系统性偏向某群体热门片。保持历史不变，才便于观察额外身份线索带来的列表移动。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:promptshift" data-paper-title="Measuring and Mitigating Identity-Cue Preference Drift in LLM-based Recommender Systems" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Measuring and Mitigating Identity-Cue Preference Drift in LLM-based Recommender Systems 搜广推与 LLM 应用 University of Electronic Science and Technology of China 2026-09-28 在行为历史不变时比较身份提示与无身份参考列表，用 Drift 与 SliceShift 量化身份线索偏移，再依据用户主流度自适应混合原分与逆群体流行度。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行列表指标与后处理 reranker；身份 slice 和相关性由公开 fixture 给出，不生成真实用户画像。执行列表指标与后处理 reranker；身份 slice 和相关性由公开 fixture 给出，不生成真实用户画像。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  llm-recommendation identity-cue-drift fairness 搜广推 学习信号、多任务与反馈偏差 自适应逆流行度混合与一律给冷门加分，相比用户条件在哪里？ 按主流度 m 决定原相关与逆流行贡献，意在让不同用户采取不同缓解强度；固定冷门奖对所有人同样操作。两者都可能牺牲相关性，诊断不等于真实公平或满意改善，来源本地不能进入正式能力排名。 示意：主流兴趣强用户可能需要不同校正，极小众用户再强推冷门可能没意义；先估用户状态而非统一给所有低流行内容同分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-2fd0165111d28e58">自适应逆流行度混合与一律给冷门加分，相比用户条件在哪里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apromptshift">Measuring and Mitigating Identity-Cue Preference Drift in LLM-based Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Electronic Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>按主流度 m 决定原相关与逆流行贡献，意在让不同用户采取不同缓解强度；固定冷门奖对所有人同样操作。两者都可能牺牲相关性，诊断不等于真实公平或满意改善，来源本地不能进入正式能力排名。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>主流兴趣强用户可能需要不同校正，极小众用户再强推冷门可能没意义；先估用户状态而非统一给所有低流行内容同分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34229">原论文</a> · <a href="../../../../reproductions/2609.34229-promptshift/">实现解读</a> · <a href="#qa-2fd0165111d28e58">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:promptshift" data-paper-title="Measuring and Mitigating Identity-Cue Preference Drift in LLM-based Recommender Systems" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Measuring and Mitigating Identity-Cue Preference Drift in LLM-based Recommender Systems 搜广推与 LLM 应用 University of Electronic Science and Technology of China 2026-09-28 在行为历史不变时比较身份提示与无身份参考列表，用 Drift 与 SliceShift 量化身份线索偏移，再依据用户主流度自适应混合原分与逆群体流行度。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行列表指标与后处理 reranker；身份 slice 和相关性由公开 fixture 给出，不生成真实用户画像。执行列表指标与后处理 reranker；身份 slice 和相关性由公开 fixture 给出，不生成真实用户画像。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  llm-recommendation identity-cue-drift fairness 搜广推 学习信号、多任务与反馈偏差 PromptShift 的 reference 列表与身份提示列表，哪些输入必须保持相同？ 历史、候选、模型与解码条件应尽量一致，只改变待检身份线索，否则差异无法归因。共同条目位次与集合变化要按定义处理，不能把不相交项强行配位置。缓解参数也不能看 test 最有利结果再选。 示意：一组还多给最近点击，另一组没有，那就不再只检身份；即使发现明显漂移，也可能来自额外行为而非提示线索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-cc6ed8a8ddc8268a">PromptShift 的 reference 列表与身份提示列表，哪些输入必须保持相同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apromptshift">Measuring and Mitigating Identity-Cue Preference Drift in LLM-based Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Electronic Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>历史、候选、模型与解码条件应尽量一致，只改变待检身份线索，否则差异无法归因。共同条目位次与集合变化要按定义处理，不能把不相交项强行配位置。缓解参数也不能看 test 最有利结果再选。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一组还多给最近点击，另一组没有，那就不再只检身份；即使发现明显漂移，也可能来自额外行为而非提示线索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34229">原论文</a> · <a href="../../../../reproductions/2609.34229-promptshift/">实现解读</a> · <a href="#qa-cc6ed8a8ddc8268a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:flvm" data-paper-title="Mend the Measurement Gap: Latent User Preference Modeling for Short-Form Video Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Mend the Measurement Gap: Latent User Preference Modeling for Short-Form Video Recommendation 搜广推与 LLM 应用 Google / YouTube 2026-09-26 短视频的观看时长会被视频长度、用户习惯和时段影响，同样的观看行为不一定代表喜欢。Google/YouTube 的 FLVM 不直接把各种行为当成单一偏好分数，而是用三维潜变量分别表示消费、主动参与、参与方向（正负）。时长等测量混杂因素只进入受限基线；完整的用户—视频信息进入潜变量编码器。每个反馈头只读取与其语义相符的因子，然后在 logit 空间叠加到停止梯度的基线上。 复现级别：公开数据概念验证。复现级别：公开数据概念验证。本地执行了三因子高斯潜变量、受限基线、稀疏路由、停止梯度与 KL 损失；没有 YouTube 的满意度调查、生产特征和线上实验，不能据此声称复现 +2.67% 收益。本地对照口径：实验组为 FLVM 缩比结构；基线为独立初始化和训练、读取相同曝光前特征、使用相同四种反馈与更新步数的共享塔多任务模型。两者不是 YouTube 生产模型，相对论文线上收益不适用。  ranking multi-task feedback-debiasing 搜广推 学习信号、多任务与反馈偏差 FLVM 为什么区分消费、主动参与和参与方向三个潜在因子？ 看得久、主动点击和喜欢不等价，负反馈也可能很主动。分因子让各反馈头只读取语义相关分量，避免把所有参与当正向价值。它是受约束的潜变量模型，不保证因子天然具有可识别的真实心理含义，仍需独立语义检查。 示意：用户长时间看完争议视频又点讨厌，消费与主动参与都高，正向方向却低；一个单一参与度分数容易误把它当喜欢。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-flvm-33286ec7" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-17e1de9e754f07eb">FLVM 为什么区分消费、主动参与和参与方向三个潜在因子？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aflvm">Mend the Measurement Gap: Latent User Preference Modeling for Short-Form Video Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>看得久、主动点击和喜欢不等价，负反馈也可能很主动。分因子让各反馈头只读取语义相关分量，避免把所有参与当正向价值。它是受约束的潜变量模型，不保证因子天然具有可识别的真实心理含义，仍需独立语义检查。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户长时间看完争议视频又点讨厌，消费与主动参与都高，正向方向却低；一个单一参与度分数容易误把它当喜欢。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.32839">原论文</a> · <a href="../../../../reproductions/2609.32839-flvm/">实现解读</a> · <a href="#qa-17e1de9e754f07eb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:flvm" data-paper-title="Mend the Measurement Gap: Latent User Preference Modeling for Short-Form Video Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Mend the Measurement Gap: Latent User Preference Modeling for Short-Form Video Recommendation 搜广推与 LLM 应用 Google / YouTube 2026-09-26 短视频的观看时长会被视频长度、用户习惯和时段影响，同样的观看行为不一定代表喜欢。Google/YouTube 的 FLVM 不直接把各种行为当成单一偏好分数，而是用三维潜变量分别表示消费、主动参与、参与方向（正负）。时长等测量混杂因素只进入受限基线；完整的用户—视频信息进入潜变量编码器。每个反馈头只读取与其语义相符的因子，然后在 logit 空间叠加到停止梯度的基线上。 复现级别：公开数据概念验证。复现级别：公开数据概念验证。本地执行了三因子高斯潜变量、受限基线、稀疏路由、停止梯度与 KL 损失；没有 YouTube 的满意度调查、生产特征和线上实验，不能据此声称复现 +2.67% 收益。本地对照口径：实验组为 FLVM 缩比结构；基线为独立初始化和训练、读取相同曝光前特征、使用相同四种反馈与更新步数的共享塔多任务模型。两者不是 YouTube 生产模型，相对论文线上收益不适用。  ranking multi-task feedback-debiasing 搜广推 学习信号、多任务与反馈偏差 FLVM为什么把测量混杂放进受限基线，再用受路由约束的潜变量修正反馈头？ 观看时长等反馈受视频长度和用户习惯影响，不是纯偏好。受限基线先解释测量条件，潜变量分别承担消费、主动参与和正负方向，反馈头只读取语义相关因子；基线停止梯度避免残差目标反过来任意改写参照。结构限制帮助分工，但不构成潜变量已被完全因果识别的保证。 示意：完整看完短片与中途划走长片可能秒数接近；基线解释长度机会，潜变量再区分主动喜欢与被动消费，不能让所有反馈都变成同一个时长偏好分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:flvm" data-paper-title="Mend the Measurement Gap: Latent User Preference Modeling for Short-Form Video Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Mend the Measurement Gap: Latent User Preference Modeling for Short-Form Video Recommendation 搜广推与 LLM 应用 Google / YouTube 2026-09-26 短视频的观看时长会被视频长度、用户习惯和时段影响，同样的观看行为不一定代表喜欢。Google/YouTube 的 FLVM 不直接把各种行为当成单一偏好分数，而是用三维潜变量分别表示消费、主动参与、参与方向（正负）。时长等测量混杂因素只进入受限基线；完整的用户—视频信息进入潜变量编码器。每个反馈头只读取与其语义相符的因子，然后在 logit 空间叠加到停止梯度的基线上。 复现级别：公开数据概念验证。复现级别：公开数据概念验证。本地执行了三因子高斯潜变量、受限基线、稀疏路由、停止梯度与 KL 损失；没有 YouTube 的满意度调查、生产特征和线上实验，不能据此声称复现 +2.67% 收益。本地对照口径：实验组为 FLVM 缩比结构；基线为独立初始化和训练、读取相同曝光前特征、使用相同四种反馈与更新步数的共享塔多任务模型。两者不是 YouTube 生产模型，相对论文线上收益不适用。  ranking multi-task feedback-debiasing 搜广推 学习信号、多任务与反馈偏差 FLVM 与普通多任务共享塔，相比受限 baseline 和 stop-gradient 限制了哪条捷径？ 时长与时段等因素先解释测量基线，完整用户物品信息通过潜变量修正，各头受固定语义路由约束，基线梯度另行训练。普通共享塔没有这类分工，容易混用所有信号。约束并不自动去掉混杂，本地潜变量分离也未获稳定证据。 示意：长视频更容易累积观看秒数，可先由基线解释长度；潜变量应学习额外偏好，而非把“长”直接当“喜欢”，但这种分工需要实测检查。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a996c425104773c4">FLVM 与普通多任务共享塔，相比受限 baseline 和 stop-gradient 限制了哪条捷径？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aflvm">Mend the Measurement Gap: Latent User Preference Modeling for Short-Form Video Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>时长与时段等因素先解释测量基线，完整用户物品信息通过潜变量修正，各头受固定语义路由约束，基线梯度另行训练。普通共享塔没有这类分工，容易混用所有信号。约束并不自动去掉混杂，本地潜变量分离也未获稳定证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>长视频更容易累积观看秒数，可先由基线解释长度；潜变量应学习额外偏好，而非把“长”直接当“喜欢”，但这种分工需要实测检查。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.32839">原论文</a> · <a href="../../../../reproductions/2609.32839-flvm/">实现解读</a> · <a href="#qa-a996c425104773c4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:flvm" data-paper-title="Mend the Measurement Gap: Latent User Preference Modeling for Short-Form Video Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Mend the Measurement Gap: Latent User Preference Modeling for Short-Form Video Recommendation 搜广推与 LLM 应用 Google / YouTube 2026-09-26 短视频的观看时长会被视频长度、用户习惯和时段影响，同样的观看行为不一定代表喜欢。Google/YouTube 的 FLVM 不直接把各种行为当成单一偏好分数，而是用三维潜变量分别表示消费、主动参与、参与方向（正负）。时长等测量混杂因素只进入受限基线；完整的用户—视频信息进入潜变量编码器。每个反馈头只读取与其语义相符的因子，然后在 logit 空间叠加到停止梯度的基线上。 复现级别：公开数据概念验证。复现级别：公开数据概念验证。本地执行了三因子高斯潜变量、受限基线、稀疏路由、停止梯度与 KL 损失；没有 YouTube 的满意度调查、生产特征和线上实验，不能据此声称复现 +2.67% 收益。本地对照口径：实验组为 FLVM 缩比结构；基线为独立初始化和训练、读取相同曝光前特征、使用相同四种反馈与更新步数的共享塔多任务模型。两者不是 YouTube 生产模型，相对论文线上收益不适用。  ranking multi-task feedback-debiasing 搜广推 学习信号、多任务与反馈偏差 FLVM 的反馈 mask 与固定潜因子路由为什么不能混为一项？ 观测 mask 决定该样本某标签是否存在，路由 mask 决定该反馈头允许读取哪些因子，作用轴不同。缺失标签不应置零，基线叠加需停止指定梯度；排序只用消费与正负方向的定义组合，不能直接把主动参与加作正奖励。 示意：没有 dislike 标签是未观测，不是明确喜欢；即使标签有效，讨厌头也不该读取与其语义无关的全部因子来绕过分工。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6c10ba9bb3d066ce">FLVM 的反馈 mask 与固定潜因子路由为什么不能混为一项？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aflvm">Mend the Measurement Gap: Latent User Preference Modeling for Short-Form Video Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / YouTube</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>观测 mask 决定该样本某标签是否存在，路由 mask 决定该反馈头允许读取哪些因子，作用轴不同。缺失标签不应置零，基线叠加需停止指定梯度；排序只用消费与正负方向的定义组合，不能直接把主动参与加作正奖励。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>没有 dislike 标签是未观测，不是明确喜欢；即使标签有效，讨厌头也不该读取与其语义无关的全部因子来绕过分工。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.32839">原论文</a> · <a href="../../../../reproductions/2609.32839-flvm/">实现解读</a> · <a href="#qa-6c10ba9bb3d066ce">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cross-task-relationships" data-paper-title="Learned Cross-Task Relationships in Multi-Task Models" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Learned Cross-Task Relationships in Multi-Task Models 搜广推与 LLM 应用 Google 2026-09-23 多任务网络只预测各反馈的边际概率，可能丢掉任务之间的联合信息。该方法加入成对联合标签或缺失的无条件辅助头，既给共享表示提供额外梯度，也能把联合预测作为下游策略的新输入；论文将这两种收益分阶段隔离测试。 成本过高，不复现（审查 DONE）：原文每日数十亿样本、多周训练与线上实验不在单卡预算内；小切片稀疏且有前缀选择偏差，三种子仍只是诊断，不是稳定能力提升。使用官方 KuaiRand-Pure 固定 4,096 行曝光前缀，时间排序后按 70/15/15 划分 train/validation/test。特征仅含曝光前的用户/视频 ID、时段和视频时长；is_click / long_view 只进入损失与评分。训练集检查四种联合标签均存在，排除互斥、嵌套、常量或当前切片无法支持的任务对。  多目标与多任务学习 联合标签与辅助头 搜广推 学习信号、多任务与反馈偏差 两个边际概率相同的多任务模型，为什么仍可能对联合行为作不同判断？ 边际只描述各事件发生频率，不决定它们是否一起发生。联合概率补充依赖结构，协方差由联合量减去边际乘积得到，可为共享表示及下游策略提供额外信息。前提是任务对在数据中有足够非退化组合，互斥或常量标签不能硬套同一解释。 示意：点击率和长看率都为一半时，两事件可总是一起，也可完全错开；仅看两个边际无法区分，联合头才能表达这种差别。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-cross-task-relationships-c0c2f1d1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-992bd51e3399c8a0">两个边际概率相同的多任务模型，为什么仍可能对联合行为作不同判断？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Across-task-relationships">Learned Cross-Task Relationships in Multi-Task Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>边际只描述各事件发生频率，不决定它们是否一起发生。联合概率补充依赖结构，协方差由联合量减去边际乘积得到，可为共享表示及下游策略提供额外信息。前提是任务对在数据中有足够非退化组合，互斥或常量标签不能硬套同一解释。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>点击率和长看率都为一半时，两事件可总是一起，也可完全错开；仅看两个边际无法区分，联合头才能表达这种差别。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.28776">原论文</a> · <a href="../../../../recommendation-components/2609.28776-cross-task-relationships/">实现解读</a> · <a href="#qa-992bd51e3399c8a0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cross-task-relationships" data-paper-title="Learned Cross-Task Relationships in Multi-Task Models" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Learned Cross-Task Relationships in Multi-Task Models 搜广推与 LLM 应用 Google 2026-09-23 多任务网络只预测各反馈的边际概率，可能丢掉任务之间的联合信息。该方法加入成对联合标签或缺失的无条件辅助头，既给共享表示提供额外梯度，也能把联合预测作为下游策略的新输入；论文将这两种收益分阶段隔离测试。 成本过高，不复现（审查 DONE）：原文每日数十亿样本、多周训练与线上实验不在单卡预算内；小切片稀疏且有前缀选择偏差，三种子仍只是诊断，不是稳定能力提升。使用官方 KuaiRand-Pure 固定 4,096 行曝光前缀，时间排序后按 70/15/15 划分 train/validation/test。特征仅含曝光前的用户/视频 ID、时段和视频时长；is_click / long_view 只进入损失与评分。训练集检查四种联合标签均存在，排除互斥、嵌套、常量或当前切片无法支持的任务对。  多目标与多任务学习 联合标签与辅助头 搜广推 学习信号、多任务与反馈偏差 已经分别预测点赞率和点击率，为什么还需要预测两者的联合标签？ 边际概率无法确定两个反馈是否集中在同一批样本上。联合头补充依赖信息，既能给共享表示额外监督，也能成为下游决策信号；这两种收益应分开验证。由边际与联合值恢复完整分布时，还要检查概率是否可行，不能把负概率裁掉后就声称模型已经校准。 示意：两个模型都预测点击率和点赞率各为20%，一种情况完全发生在同一群人，另一种彼此分离；只看两个边际，无法区分应如何组合业务目标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cross-task-relationships" data-paper-title="Learned Cross-Task Relationships in Multi-Task Models" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Learned Cross-Task Relationships in Multi-Task Models 搜广推与 LLM 应用 Google 2026-09-23 多任务网络只预测各反馈的边际概率，可能丢掉任务之间的联合信息。该方法加入成对联合标签或缺失的无条件辅助头，既给共享表示提供额外梯度，也能把联合预测作为下游策略的新输入；论文将这两种收益分阶段隔离测试。 成本过高，不复现（审查 DONE）：原文每日数十亿样本、多周训练与线上实验不在单卡预算内；小切片稀疏且有前缀选择偏差，三种子仍只是诊断，不是稳定能力提升。使用官方 KuaiRand-Pure 固定 4,096 行曝光前缀，时间排序后按 70/15/15 划分 train/validation/test。特征仅含曝光前的用户/视频 ID、时段和视频时长；is_click / long_view 只进入损失与评分。训练集检查四种联合标签均存在，排除互斥、嵌套、常量或当前切片无法支持的任务对。  多目标与多任务学习 联合标签与辅助头 搜广推 学习信号、多任务与反馈偏差 真实 cross-label 辅助头与打乱标签辅助头对照，为什么比只比较有无额外参数更有信息？ 新增头可能仅因多了梯度或正则而改变主干，打乱联合标签保留训练形式却破坏真实任务关系，可帮助区分关系信号与一般辅助训练效应。它仍是有限诊断，稀疏小切片不能支持稳定能力外推。 示意：真实点击且长看标签改善，而同样大小但乱序标签没有改善，更支持联合关系有用；若两者相似，就要考虑只是额外训练扰动。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-406fe847530f0af1">真实 cross-label 辅助头与打乱标签辅助头对照，为什么比只比较有无额外参数更有信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Across-task-relationships">Learned Cross-Task Relationships in Multi-Task Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>新增头可能仅因多了梯度或正则而改变主干，打乱联合标签保留训练形式却破坏真实任务关系，可帮助区分关系信号与一般辅助训练效应。它仍是有限诊断，稀疏小切片不能支持稳定能力外推。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>真实点击且长看标签改善，而同样大小但乱序标签没有改善，更支持联合关系有用；若两者相似，就要考虑只是额外训练扰动。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.28776">原论文</a> · <a href="../../../../recommendation-components/2609.28776-cross-task-relationships/">实现解读</a> · <a href="#qa-406fe847530f0af1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cross-task-relationships" data-paper-title="Learned Cross-Task Relationships in Multi-Task Models" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Learned Cross-Task Relationships in Multi-Task Models 搜广推与 LLM 应用 Google 2026-09-23 多任务网络只预测各反馈的边际概率，可能丢掉任务之间的联合信息。该方法加入成对联合标签或缺失的无条件辅助头，既给共享表示提供额外梯度，也能把联合预测作为下游策略的新输入；论文将这两种收益分阶段隔离测试。 成本过高，不复现（审查 DONE）：原文每日数十亿样本、多周训练与线上实验不在单卡预算内；小切片稀疏且有前缀选择偏差，三种子仍只是诊断，不是稳定能力提升。使用官方 KuaiRand-Pure 固定 4,096 行曝光前缀，时间排序后按 70/15/15 划分 train/validation/test。特征仅含曝光前的用户/视频 ID、时段和视频时长；is_click / long_view 只进入损失与评分。训练集检查四种联合标签均存在，排除互斥、嵌套、常量或当前切片无法支持的任务对。  多目标与多任务学习 联合标签与辅助头 搜广推 学习信号、多任务与反馈偏差 从 pX、pY、pXY 恢复四格联合分布时，为什么不能把负概率静默裁零？ 四格需满足非负与总和为一，pXY 还受边际界限约束。负值暴露模型估计不一致，裁零后再称校准正确会隐藏问题。来源保留不可行标记，标签只进损失与评分；点击或长看不能成为曝光前输入。 示意：pX 为零点二、pXY 为零点四会得到负的“仅点击”概率。应报告不一致，而不是剪到零后假装原模型输出了合法联合分布。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a3d34d2a90b174f4">从 pX、pY、pXY 恢复四格联合分布时，为什么不能把负概率静默裁零？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Across-task-relationships">Learned Cross-Task Relationships in Multi-Task Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>四格需满足非负与总和为一，pXY 还受边际界限约束。负值暴露模型估计不一致，裁零后再称校准正确会隐藏问题。来源保留不可行标记，标签只进损失与评分；点击或长看不能成为曝光前输入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>pX 为零点二、pXY 为零点四会得到负的“仅点击”概率。应报告不一致，而不是剪到零后假装原模型输出了合法联合分布。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.28776">原论文</a> · <a href="../../../../recommendation-components/2609.28776-cross-task-relationships/">实现解读</a> · <a href="#qa-a3d34d2a90b174f4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:light-heads" data-paper-title="Lightweight Ranking Heads: Accelerating Multi-Task Experimentation in Production Recommender Systems" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Lightweight Ranking Heads: Accelerating Multi-Task Experimentation in Production Recommender Systems 搜广推与 LLM 应用 Google 2026-09-21 工业多任务 ranker 要添加新目标时，直接改动共享塔可能导致旧目标负迁移，还会让并行实验模型与下游模型输出空间不一致。论文把新增目标声明为中央配置，训练时在共享表示上动态挂一个浅头；轻头输入执行 stop_gradient，因此新目标不会回传到共享塔。每个持续训练窗口可以重置轻头参数，使不同上游模型的轻头训练年龄可比较。论文也报告了“不重置”和“去掉 stop-gradient”的消融，前者可能给数据稀疏的目标更好的拟合，后者可能损伤原任务。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地确实执行了动态注入、stop-gradient、训练窗口重置以及两个对应消融；没有 Google 私有流量、持续训练平台或线上下游模型。公开数据结果与论文线上结果严格分开。执行了论文定义性的“共享塔 + 动态轻头 + 梯度隔离 + 可选重置”；不是同名的后处理打分函数。本地对照口径：同预算不重置轻头为新任务基线，test AUC 0.6267；标准重置实验组 0.5109，相对 -18.48%。这是公开数据短训练窗口的负结果。  ranking multi-task-learning lightweight-heads 搜广推 学习信号、多任务与反馈偏差 Light Heads 为什么把新增目标设计成浅头而非立即改共享主干？ 工业系统常要快速试新目标，同时保护已有任务与下游接口。浅头读取共享表示、只更新自身，让新监督成为低成本探针；它能利用主干已有知识却不能从该损失改善主干。新目标若需要缺失信息，轻头容量再大也难补。 示意：先在现有用户向量上试稀疏满意度目标，不必让少量标签改变全部点击网络；但向量没记录的细节不会因加头而自动出现。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-light-heads-bf390928" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-238d80dda721f3d5">Light Heads 为什么把新增目标设计成浅头而非立即改共享主干？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alight-heads">Lightweight Ranking Heads: Accelerating Multi-Task Experimentation in Production Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>工业系统常要快速试新目标，同时保护已有任务与下游接口。浅头读取共享表示、只更新自身，让新监督成为低成本探针；它能利用主干已有知识却不能从该损失改善主干。新目标若需要缺失信息，轻头容量再大也难补。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先在现有用户向量上试稀疏满意度目标，不必让少量标签改变全部点击网络；但向量没记录的细节不会因加头而自动出现。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.25433">原论文</a> · <a href="../../../../reproductions/2609.25433-light-heads/">实现解读</a> · <a href="#qa-238d80dda721f3d5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:light-heads" data-paper-title="Lightweight Ranking Heads: Accelerating Multi-Task Experimentation in Production Recommender Systems" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Lightweight Ranking Heads: Accelerating Multi-Task Experimentation in Production Recommender Systems 搜广推与 LLM 应用 Google 2026-09-21 工业多任务 ranker 要添加新目标时，直接改动共享塔可能导致旧目标负迁移，还会让并行实验模型与下游模型输出空间不一致。论文把新增目标声明为中央配置，训练时在共享表示上动态挂一个浅头；轻头输入执行 stop_gradient，因此新目标不会回传到共享塔。每个持续训练窗口可以重置轻头参数，使不同上游模型的轻头训练年龄可比较。论文也报告了“不重置”和“去掉 stop-gradient”的消融，前者可能给数据稀疏的目标更好的拟合，后者可能损伤原任务。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地确实执行了动态注入、stop-gradient、训练窗口重置以及两个对应消融；没有 Google 私有流量、持续训练平台或线上下游模型。公开数据结果与论文线上结果严格分开。执行了论文定义性的“共享塔 + 动态轻头 + 梯度隔离 + 可选重置”；不是同名的后处理打分函数。本地对照口径：同预算不重置轻头为新任务基线，test AUC 0.6267；标准重置实验组 0.5109，相对 -18.48%。这是公开数据短训练窗口的负结果。  ranking multi-task-learning lightweight-heads 搜广推 学习信号、多任务与反馈偏差 Light Heads对共享表示做stop-gradient后，新目标还能改善主干吗？ 单独的新目标损失不能通过这条路径更新共享主干，只能训练浅头，因此可以降低新增目标对旧任务的干扰。窗口重置又让并行模型的轻头训练年龄可比较，但会损失稀疏目标的长期拟合。隔离梯度与重置是两种不同控制，不能把新头AUC提高解释为主干能力已经因此增强。 示意：给成熟点击模型临时加一个新反馈头，梯度隔离可避免它伤害旧塔；每周重置便于公平比较不同上游，但新任务样本很少时也可能重新学不够。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:light-heads" data-paper-title="Lightweight Ranking Heads: Accelerating Multi-Task Experimentation in Production Recommender Systems" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Lightweight Ranking Heads: Accelerating Multi-Task Experimentation in Production Recommender Systems 搜广推与 LLM 应用 Google 2026-09-21 工业多任务 ranker 要添加新目标时，直接改动共享塔可能导致旧目标负迁移，还会让并行实验模型与下游模型输出空间不一致。论文把新增目标声明为中央配置，训练时在共享表示上动态挂一个浅头；轻头输入执行 stop_gradient，因此新目标不会回传到共享塔。每个持续训练窗口可以重置轻头参数，使不同上游模型的轻头训练年龄可比较。论文也报告了“不重置”和“去掉 stop-gradient”的消融，前者可能给数据稀疏的目标更好的拟合，后者可能损伤原任务。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地确实执行了动态注入、stop-gradient、训练窗口重置以及两个对应消融；没有 Google 私有流量、持续训练平台或线上下游模型。公开数据结果与论文线上结果严格分开。执行了论文定义性的“共享塔 + 动态轻头 + 梯度隔离 + 可选重置”；不是同名的后处理打分函数。本地对照口径：同预算不重置轻头为新任务基线，test AUC 0.6267；标准重置实验组 0.5109，相对 -18.48%。这是公开数据短训练窗口的负结果。  ranking multi-task-learning lightweight-heads 搜广推 学习信号、多任务与反馈偏差 重置与不重置 Light Head，为什么是训练年龄可比性和稀疏拟合的取舍？ 每窗口重置让不同上游模型的轻头学习年龄相同，减少历史累积差异；不重置保留更多稀疏标签经验，可能拟合更好。来源本地短窗口重置明显退化，因此不能宣称重置普遍最优。是否重置取决于实验目标与数据量。 示意：甲头已训练三周、乙刚挂一天，直接比会混入年龄差；都重置更可比，但极少样本目标可能来不及重新学好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-bfaadddfa74f0247">重置与不重置 Light Head，为什么是训练年龄可比性和稀疏拟合的取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alight-heads">Lightweight Ranking Heads: Accelerating Multi-Task Experimentation in Production Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每窗口重置让不同上游模型的轻头学习年龄相同，减少历史累积差异；不重置保留更多稀疏标签经验，可能拟合更好。来源本地短窗口重置明显退化，因此不能宣称重置普遍最优。是否重置取决于实验目标与数据量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>甲头已训练三周、乙刚挂一天，直接比会混入年龄差；都重置更可比，但极少样本目标可能来不及重新学好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.25433">原论文</a> · <a href="../../../../reproductions/2609.25433-light-heads/">实现解读</a> · <a href="#qa-bfaadddfa74f0247">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:light-heads" data-paper-title="Lightweight Ranking Heads: Accelerating Multi-Task Experimentation in Production Recommender Systems" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Lightweight Ranking Heads: Accelerating Multi-Task Experimentation in Production Recommender Systems 搜广推与 LLM 应用 Google 2026-09-21 工业多任务 ranker 要添加新目标时，直接改动共享塔可能导致旧目标负迁移，还会让并行实验模型与下游模型输出空间不一致。论文把新增目标声明为中央配置，训练时在共享表示上动态挂一个浅头；轻头输入执行 stop_gradient，因此新目标不会回传到共享塔。每个持续训练窗口可以重置轻头参数，使不同上游模型的轻头训练年龄可比较。论文也报告了“不重置”和“去掉 stop-gradient”的消融，前者可能给数据稀疏的目标更好的拟合，后者可能损伤原任务。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地确实执行了动态注入、stop-gradient、训练窗口重置以及两个对应消融；没有 Google 私有流量、持续训练平台或线上下游模型。公开数据结果与论文线上结果严格分开。执行了论文定义性的“共享塔 + 动态轻头 + 梯度隔离 + 可选重置”；不是同名的后处理打分函数。本地对照口径：同预算不重置轻头为新任务基线，test AUC 0.6267；标准重置实验组 0.5109，相对 -18.48%。这是公开数据短训练窗口的负结果。  ranking multi-task-learning lightweight-heads 搜广推 学习信号、多任务与反馈偏差 Light Head 梯度隔离与窗口重置，分别应检查哪些参数？ 仅新任务 loss 反传时共享 θ 梯度为零、轻头 ψ 非零；窗口切换只重新初始化 ψ，原主任务 φ 与 θ 保持约定。两项独立，不能因有重置就推断隔离成立，也不能重置优化器时误清主干状态。 示意：新目标一步更新后主干摘要若改变就隔离失败；窗口开始若把原点击头也重置，就不再是轻头实验，而是破坏了基线。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ceefd5e0f0b3dc9c">Light Head 梯度隔离与窗口重置，分别应检查哪些参数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alight-heads">Lightweight Ranking Heads: Accelerating Multi-Task Experimentation in Production Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>仅新任务 loss 反传时共享 θ 梯度为零、轻头 ψ 非零；窗口切换只重新初始化 ψ，原主任务 φ 与 θ 保持约定。两项独立，不能因有重置就推断隔离成立，也不能重置优化器时误清主干状态。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新目标一步更新后主干摘要若改变就隔离失败；窗口开始若把原点击头也重置，就不再是轻头实验，而是破坏了基线。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.25433">原论文</a> · <a href="../../../../reproductions/2609.25433-light-heads/">实现解读</a> · <a href="#qa-ceefd5e0f0b3dc9c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:baff" data-paper-title="BAFF: Bid-Aware Filter Family for Mitigating Training Data Interference in RTB A/B Tests" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="BAFF: Bid-Aware Filter Family for Mitigating Training Data Interference in RTB A/B Tests 搜广推与 LLM 应用 Dable 2026-09-08 RTB 实验中 A/B 两个策略看到的竞价机会会互相影响；直接混用日志训练 B 模型会引入 treatment interference。BAFF 同时检查 A 广告在 B 排序中的位置差和 bid-price 差，只保留对 B 决策近似无干扰的 A 日志。 复现级别：受控仿真核心机制。复现级别：受控仿真核心机制。精确执行论文过滤判据，以 B-only 训练作参照测量共享日志参数偏差；不把仿真结果称为线上提升。2,400 次受控拍卖、三种子结果见 metrics/controlled-rtb-seeds42-44.json。仿真真实执行严格双轴过滤及 ridge 参数偏差诊断，但没有 Dable 私有 DSP 日志、生产 CTR 模型或市场侧 reference 实验。  advertising rtb ab-testing training-data-interference 搜广推 学习信号、多任务与反馈偏差 BAFF 所说的 treatment interference 为什么会出现在 RTB 的 A/B 日志里？ 竞价机会与价格会被策略选择共同影响，一个实验组的广告决策可能改变另一策略实际面对的竞争环境。混用 A 日志训练 B 时，样本不再天然等同于 B 会看到的机会。过滤近似无干扰样本是在限制可迁移范围，而非认定实验标签可随意交换。 示意：A 抬高某广告出价后改变了竞争排序，B 本来不会以同样价格获得该机会；把这条日志直接当 B 的普通训练样本就混入策略影响。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-baff-e8ac8fd9" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-213d144919ea826f">BAFF 所说的 treatment interference 为什么会出现在 RTB 的 A/B 日志里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Abaff">BAFF: Bid-Aware Filter Family for Mitigating Training Data Interference in RTB A/B Tests</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dable</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>竞价机会与价格会被策略选择共同影响，一个实验组的广告决策可能改变另一策略实际面对的竞争环境。混用 A 日志训练 B 时，样本不再天然等同于 B 会看到的机会。过滤近似无干扰样本是在限制可迁移范围，而非认定实验标签可随意交换。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>A 抬高某广告出价后改变了竞争排序，B 本来不会以同样价格获得该机会；把这条日志直接当 B 的普通训练样本就混入策略影响。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08725">原论文</a> · <a href="../../../../reproductions/2609.08725-baff/">实现解读</a> · <a href="#qa-213d144919ea826f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:baff" data-paper-title="BAFF: Bid-Aware Filter Family for Mitigating Training Data Interference in RTB A/B Tests" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="BAFF: Bid-Aware Filter Family for Mitigating Training Data Interference in RTB A/B Tests 搜广推与 LLM 应用 Dable 2026-09-08 RTB 实验中 A/B 两个策略看到的竞价机会会互相影响；直接混用日志训练 B 模型会引入 treatment interference。BAFF 同时检查 A 广告在 B 排序中的位置差和 bid-price 差，只保留对 B 决策近似无干扰的 A 日志。 复现级别：受控仿真核心机制。复现级别：受控仿真核心机制。精确执行论文过滤判据，以 B-only 训练作参照测量共享日志参数偏差；不把仿真结果称为线上提升。2,400 次受控拍卖、三种子结果见 metrics/controlled-rtb-seeds42-44.json。仿真真实执行严格双轴过滤及 ridge 参数偏差诊断，但没有 Dable 私有 DSP 日志、生产 CTR 模型或市场侧 reference 实验。  advertising rtb ab-testing training-data-interference 搜广推 学习信号、多任务与反馈偏差 BAFF为什么同时比较排序位置差和竞价价格差，只过滤其中一项不够吗？ 两个实验策略即使给出相近名次，也可能因价格差改变赢标机会；价格接近时，排序差又可能改变曝光分布。BAFF以双轴条件筛掉会显著影响B策略决策的A日志，减少训练中的处理干扰。保留下来只表示在给定条件下较可迁移，不等于恢复了真实无干扰市场。 示意：A广告在B榜单位置相近，却有大幅更高报价，仍可能抢走机会；反之价格相同但名次跨过展示边界，也不能直接混用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:baff" data-paper-title="BAFF: Bid-Aware Filter Family for Mitigating Training Data Interference in RTB A/B Tests" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="BAFF: Bid-Aware Filter Family for Mitigating Training Data Interference in RTB A/B Tests 搜广推与 LLM 应用 Dable 2026-09-08 RTB 实验中 A/B 两个策略看到的竞价机会会互相影响；直接混用日志训练 B 模型会引入 treatment interference。BAFF 同时检查 A 广告在 B 排序中的位置差和 bid-price 差，只保留对 B 决策近似无干扰的 A 日志。 复现级别：受控仿真核心机制。复现级别：受控仿真核心机制。精确执行论文过滤判据，以 B-only 训练作参照测量共享日志参数偏差；不把仿真结果称为线上提升。2,400 次受控拍卖、三种子结果见 metrics/controlled-rtb-seeds42-44.json。仿真真实执行严格双轴过滤及 ridge 参数偏差诊断，但没有 Dable 私有 DSP 日志、生产 CTR 模型或市场侧 reference 实验。  advertising rtb ab-testing training-data-interference 搜广推 学习信号、多任务与反馈偏差 BAFF 的过滤与给全部 A 日志统一降权相比，有什么信息取舍？ 统一降权保留所有样本，却不区分哪些机会已严重受 A 策略影响；双条件过滤根据 B 排序位置和价格差，直接排除不相容日志。它减少干扰同时损失样本量，阈值越严不一定总更好，也不能保证留下样本已完全无偏。 示意：一条日志价格接近却排序差很大，统一乘半权仍会使用它；过滤可明确拒绝，但若门槛太严只剩极少样本，训练方差也会上升。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4ec25e619cf3dc9a">BAFF 的过滤与给全部 A 日志统一降权相比，有什么信息取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Abaff">BAFF: Bid-Aware Filter Family for Mitigating Training Data Interference in RTB A/B Tests</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dable</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>统一降权保留所有样本，却不区分哪些机会已严重受 A 策略影响；双条件过滤根据 B 排序位置和价格差，直接排除不相容日志。它减少干扰同时损失样本量，阈值越严不一定总更好，也不能保证留下样本已完全无偏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一条日志价格接近却排序差很大，统一乘半权仍会使用它；过滤可明确拒绝，但若门槛太严只剩极少样本，训练方差也会上升。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08725">原论文</a> · <a href="../../../../reproductions/2609.08725-baff/">实现解读</a> · <a href="#qa-4ec25e619cf3dc9a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:baff" data-paper-title="BAFF: Bid-Aware Filter Family for Mitigating Training Data Interference in RTB A/B Tests" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="BAFF: Bid-Aware Filter Family for Mitigating Training Data Interference in RTB A/B Tests 搜广推与 LLM 应用 Dable 2026-09-08 RTB 实验中 A/B 两个策略看到的竞价机会会互相影响；直接混用日志训练 B 模型会引入 treatment interference。BAFF 同时检查 A 广告在 B 排序中的位置差和 bid-price 差，只保留对 B 决策近似无干扰的 A 日志。 复现级别：受控仿真核心机制。复现级别：受控仿真核心机制。精确执行论文过滤判据，以 B-only 训练作参照测量共享日志参数偏差；不把仿真结果称为线上提升。2,400 次受控拍卖、三种子结果见 metrics/controlled-rtb-seeds42-44.json。仿真真实执行严格双轴过滤及 ridge 参数偏差诊断，但没有 Dable 私有 DSP 日志、生产 CTR 模型或市场侧 reference 实验。  advertising rtb ab-testing training-data-interference 搜广推 学习信号、多任务与反馈偏差 BAFF 的 bid-price 距离为什么只取 A 比 B 高出的正向部分？ 来源定义 max(bpA−bpB,0)/bpA，衡量的是这一方向上的价格抬升，而非对称绝对差；排序距离则按 B 中的位置除以 K。实现应保留方向、归一化与双阈值条件，不能随手换成绝对值或把两个阈值先加总。 示意：A 价十、B 价八时价格差为两成；A 价八、B 价十并不会得到相同正向惩罚。若改用绝对差，就悄悄变成另一个过滤规则。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1a6ce48b374de43a">BAFF 的 bid-price 距离为什么只取 A 比 B 高出的正向部分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Abaff">BAFF: Bid-Aware Filter Family for Mitigating Training Data Interference in RTB A/B Tests</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dable</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>来源定义 max(bpA−bpB,0)/bpA，衡量的是这一方向上的价格抬升，而非对称绝对差；排序距离则按 B 中的位置除以 K。实现应保留方向、归一化与双阈值条件，不能随手换成绝对值或把两个阈值先加总。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>A 价十、B 价八时价格差为两成；A 价八、B 价十并不会得到相同正向惩罚。若改用绝对差，就悄悄变成另一个过滤规则。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08725">原论文</a> · <a href="../../../../reproductions/2609.08725-baff/">实现解读</a> · <a href="#qa-1a6ce48b374de43a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dceo" data-paper-title="DCEO: Direct Causal Effect Optimization for Long-Term User Value Modeling in E-commerce Search" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="DCEO: Direct Causal Effect Optimization for Long-Term User Value Modeling in E-commerce Search 搜广推与 LLM 应用 Taobao &amp; Tmall Group, Alibaba 2026-08-26 固定加权的点击、转化和 GMV 目标不能随用户状态改变，也无法直接刻画一次排序动作的长期因果价值。DCEO 用 actor 输出上下文相关 simplex 权重，用用户级 critic 估计相对干预效果；线上只保留轻量 actor。 本地负相关诊断明确阻止把 Hit 改善解读为长期价值提升。Fidelity：核心机制复现。本地执行上下文条件目标权重、用户级 proxy 聚合和相对因果干预；生产 critic 与在线 actor serving 未复刻。proxy outcome 与真实长期 GMV 不等价；本地负相关诊断明确阻止把 Hit 改善解读为长期价值提升。本地实现现在把 causal_gain × temperature 纳入 evolve 搜索空间：20 个候选只在 validation 上按 NDCG@10 + 0.15 × Hit@10 选择，随后仅对冠军运行一次 held-out test。  search-ranking long-term-value causal-optimization multi-objective-ranking 搜广推 学习信号、多任务与反馈偏差 DCEO 中 actor 与用户级 critic 各自负责什么？ actor 输出上下文相关目标权重，用于即时融合点击、转化与价值分；critic 在训练评估排序动作相对参考的长期作用，给 actor 提供更有方向的信号。线上只保留轻 actor，并不代表 critic 的因果假设已被结构自动满足。 示意：新用户状态可能更重相关性，成熟用户更重交易价值；critic 检查这种改变是否带来长期增量，服务时无需再运行完整长期评估器。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-dceo-b39ed1b8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-1685d471a4a64785">DCEO 中 actor 与用户级 critic 各自负责什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adceo">DCEO: Direct Causal Effect Optimization for Long-Term User Value Modeling in E-commerce Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group, Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>actor 输出上下文相关目标权重，用于即时融合点击、转化与价值分；critic 在训练评估排序动作相对参考的长期作用，给 actor 提供更有方向的信号。线上只保留轻 actor，并不代表 critic 的因果假设已被结构自动满足。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新用户状态可能更重相关性，成熟用户更重交易价值；critic 检查这种改变是否带来长期增量，服务时无需再运行完整长期评估器。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25635">原论文</a> · <a href="../../../../reproductions/2608.25635-dceo/">实现解读</a> · <a href="#qa-1685d471a4a64785">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dceo" data-paper-title="DCEO: Direct Causal Effect Optimization for Long-Term User Value Modeling in E-commerce Search" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="DCEO: Direct Causal Effect Optimization for Long-Term User Value Modeling in E-commerce Search 搜广推与 LLM 应用 Taobao &amp; Tmall Group, Alibaba 2026-08-26 固定加权的点击、转化和 GMV 目标不能随用户状态改变，也无法直接刻画一次排序动作的长期因果价值。DCEO 用 actor 输出上下文相关 simplex 权重，用用户级 critic 估计相对干预效果；线上只保留轻量 actor。 本地负相关诊断明确阻止把 Hit 改善解读为长期价值提升。Fidelity：核心机制复现。本地执行上下文条件目标权重、用户级 proxy 聚合和相对因果干预；生产 critic 与在线 actor serving 未复刻。proxy outcome 与真实长期 GMV 不等价；本地负相关诊断明确阻止把 Hit 改善解读为长期价值提升。本地实现现在把 causal_gain × temperature 纳入 evolve 搜索空间：20 个候选只在 validation 上按 NDCG@10 + 0.15 × Hit@10 选择，随后仅对冠军运行一次 held-out test。  search-ranking long-term-value causal-optimization multi-objective-ranking 搜广推 学习信号、多任务与反馈偏差 DCEO为什么让actor按上下文输出目标权重，而不是全站固定一组CTR、CVR、GMV系数？ 固定系数假设所有用户状态具有相同取舍，难以体现一次动作对长期价值的不同影响。actor输出和为一的动态权重，critic在训练中评估相对干预效果，服务侧只保留轻量权重决策。动态权重本身不等于因果识别，若critic缺少可信对照，仍可能只学到相关性代理。 示意：新用户更需要探索合适内容，成熟购物用户可能更重转化；同一组分数可按状态采用不同组合，但要用相应长期反馈验证，而不是仅看即时点击。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dceo" data-paper-title="DCEO: Direct Causal Effect Optimization for Long-Term User Value Modeling in E-commerce Search" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="DCEO: Direct Causal Effect Optimization for Long-Term User Value Modeling in E-commerce Search 搜广推与 LLM 应用 Taobao &amp; Tmall Group, Alibaba 2026-08-26 固定加权的点击、转化和 GMV 目标不能随用户状态改变，也无法直接刻画一次排序动作的长期因果价值。DCEO 用 actor 输出上下文相关 simplex 权重，用用户级 critic 估计相对干预效果；线上只保留轻量 actor。 本地负相关诊断明确阻止把 Hit 改善解读为长期价值提升。Fidelity：核心机制复现。本地执行上下文条件目标权重、用户级 proxy 聚合和相对因果干预；生产 critic 与在线 actor serving 未复刻。proxy outcome 与真实长期 GMV 不等价；本地负相关诊断明确阻止把 Hit 改善解读为长期价值提升。本地实现现在把 causal_gain × temperature 纳入 evolve 搜索空间：20 个候选只在 validation 上按 NDCG@10 + 0.15 × Hit@10 选择，随后仅对冠军运行一次 held-out test。  search-ranking long-term-value causal-optimization multi-objective-ranking 搜广推 学习信号、多任务与反馈偏差 DCEO 的动态 simplex 权重与固定 log fusion，相比增加了什么自由度和风险？ 固定融合给所有请求相同取舍，simplex 权重随状态变化且非负和为一，能表达用户层面差异。自由度增加也可能利用代理奖励漏洞或过拟合，因此需要验证选择与分目标评估。本地 Hit 上升而 NDCG 略降，不能宣称全指标胜出。 示意：对两类用户使用不同点击与价值比例可能更合适，但某配置把热门商品推前提高命中，也可能让真正相关项位置变差，需要同时看两指标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-2e19239d99d64438">DCEO 的动态 simplex 权重与固定 log fusion，相比增加了什么自由度和风险？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adceo">DCEO: Direct Causal Effect Optimization for Long-Term User Value Modeling in E-commerce Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group, Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定融合给所有请求相同取舍，simplex 权重随状态变化且非负和为一，能表达用户层面差异。自由度增加也可能利用代理奖励漏洞或过拟合，因此需要验证选择与分目标评估。本地 Hit 上升而 NDCG 略降，不能宣称全指标胜出。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>对两类用户使用不同点击与价值比例可能更合适，但某配置把热门商品推前提高命中，也可能让真正相关项位置变差，需要同时看两指标。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25635">原论文</a> · <a href="../../../../reproductions/2608.25635-dceo/">实现解读</a> · <a href="#qa-2e19239d99d64438">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dceo" data-paper-title="DCEO: Direct Causal Effect Optimization for Long-Term User Value Modeling in E-commerce Search" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="DCEO: Direct Causal Effect Optimization for Long-Term User Value Modeling in E-commerce Search 搜广推与 LLM 应用 Taobao &amp; Tmall Group, Alibaba 2026-08-26 固定加权的点击、转化和 GMV 目标不能随用户状态改变，也无法直接刻画一次排序动作的长期因果价值。DCEO 用 actor 输出上下文相关 simplex 权重，用用户级 critic 估计相对干预效果；线上只保留轻量 actor。 本地负相关诊断明确阻止把 Hit 改善解读为长期价值提升。Fidelity：核心机制复现。本地执行上下文条件目标权重、用户级 proxy 聚合和相对因果干预；生产 critic 与在线 actor serving 未复刻。proxy outcome 与真实长期 GMV 不等价；本地负相关诊断明确阻止把 Hit 改善解读为长期价值提升。本地实现现在把 causal_gain × temperature 纳入 evolve 搜索空间：20 个候选只在 validation 上按 NDCG@10 + 0.15 × Hit@10 选择，随后仅对冠军运行一次 held-out test。  search-ranking long-term-value causal-optimization multi-objective-ranking 搜广推 学习信号、多任务与反馈偏差 本地 DCEO 为什么只对验证选出的冠军执行一次 held-out test？ causal_gain 与温度构成候选空间，二十个配置只按固定验证效用比较，最终冠军才进入 test。这样避免把测试波动当作下一轮搜索反馈。来源的公开代理评分不等同于真实用户干预效果，因果名称也不能替代实验设计。 示意：若测完二十组 test 再挑最高的一组，就把测试用成了验证；正确流程先锁定冠军，再如实报告它可能包含的 NDCG 退化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-5fcb3cc13628fc19">本地 DCEO 为什么只对验证选出的冠军执行一次 held-out test？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adceo">DCEO: Direct Causal Effect Optimization for Long-Term User Value Modeling in E-commerce Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group, Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>causal_gain 与温度构成候选空间，二十个配置只按固定验证效用比较，最终冠军才进入 test。这样避免把测试波动当作下一轮搜索反馈。来源的公开代理评分不等同于真实用户干预效果，因果名称也不能替代实验设计。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>若测完二十组 test 再挑最高的一组，就把测试用成了验证；正确流程先锁定冠军，再如实报告它可能包含的 NDCG 退化。</p>
<p class="ar-learning-sources">依据：本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25635">原论文</a> · <a href="../../../../reproductions/2608.25635-dceo/">实现解读</a> · <a href="#qa-5fcb3cc13628fc19">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:incrementality" data-paper-title="From Prediction to Incrementality: Causal Optimization for Large-Scale Targeting and Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="From Prediction to Incrementality: Causal Optimization for Large-Scale Targeting and Recommendation 搜广推与 LLM 应用 LinkedIn 2026-08-10 分别估计处理与不处理时的潜在结果，以 uplift 及其不确定度代替点击概率排序，再在固定触达预算下完成因果分配。这样优化的是动作带来的增量价值，而不是本来就会发生的结果。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线按 treated outcome 排序，实验组按 uplift 与不确定度分配；同为 30% 预算，seed 42 的 policy value 为 0.10408，基线为 0.09537。  causal-recommendation uplift bandit constrained-allocation 搜广推 学习信号、多任务与反馈偏差 Incrementality 为什么把触达动作的价值定义成 μ1−μ0？ μ1 估计处理后的结果，μ0 估计不处理的结果，两者差区分动作创造的增量和用户本来就会发生的行为。预算应优先分给可改变的人群，而非天然高响应者。潜在结果无法同时观测，估计需要支持与识别假设。 示意：甲不触达也会买，乙触达后才改变选择；甲购买率高不代表给甲发消息更有增量，不能只按处理组结果排序。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-incrementality-26b16fde" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a5953a5c0b25bb74">Incrementality 为什么把触达动作的价值定义成 μ1−μ0？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aincrementality">From Prediction to Incrementality: Causal Optimization for Large-Scale Targeting and Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>μ1 估计处理后的结果，μ0 估计不处理的结果，两者差区分动作创造的增量和用户本来就会发生的行为。预算应优先分给可改变的人群，而非天然高响应者。潜在结果无法同时观测，估计需要支持与识别假设。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>甲不触达也会买，乙触达后才改变选择；甲购买率高不代表给甲发消息更有增量，不能只按处理组结果排序。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.10182">原论文</a> · <a href="../../../../reproductions/2608.10182-incrementality/">实现解读</a> · <a href="#qa-a5953a5c0b25bb74">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:incrementality" data-paper-title="From Prediction to Incrementality: Causal Optimization for Large-Scale Targeting and Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="From Prediction to Incrementality: Causal Optimization for Large-Scale Targeting and Recommendation 搜广推与 LLM 应用 LinkedIn 2026-08-10 分别估计处理与不处理时的潜在结果，以 uplift 及其不确定度代替点击概率排序，再在固定触达预算下完成因果分配。这样优化的是动作带来的增量价值，而不是本来就会发生的结果。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线按 treated outcome 排序，实验组按 uplift 与不确定度分配；同为 30% 预算，seed 42 的 policy value 为 0.10408，基线为 0.09537。  causal-recommendation uplift bandit constrained-allocation 搜广推 学习信号、多任务与反馈偏差 为什么高购买概率用户未必是有限触达预算下的最佳对象？ 触达策略关心动作改变了多少结果，而高购买概率可能表示用户不干预也会购买。方法分别估计处理和不处理结局，以uplift扣除不确定度后分配预算，避免把资源都花在本来就会发生的结果上。差值是否可信取决于实验支持与识别条件，不能由两个预测头存在就保证因果正确。 示意：甲无论是否触达都常买，乙只有看到合适推荐才可能买；同样一个触达名额，乙的原始购买率虽低，增量收益却可能更高。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:incrementality" data-paper-title="From Prediction to Incrementality: Causal Optimization for Large-Scale Targeting and Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="From Prediction to Incrementality: Causal Optimization for Large-Scale Targeting and Recommendation 搜广推与 LLM 应用 LinkedIn 2026-08-10 分别估计处理与不处理时的潜在结果，以 uplift 及其不确定度代替点击概率排序，再在固定触达预算下完成因果分配。这样优化的是动作带来的增量价值，而不是本来就会发生的结果。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线按 treated outcome 排序，实验组按 uplift 与不确定度分配；同为 30% 预算，seed 42 的 policy value 为 0.10408，基线为 0.09537。  causal-recommendation uplift bandit constrained-allocation 搜广推 学习信号、多任务与反馈偏差 用 τ−λσ 分配与单纯按 uplift 均值，风险偏好如何不同？ 不确定度惩罚降低高估且证据不足对象的优先级，适合强调稳健预算价值；仅按均值可能追逐高方差极端值。惩罚也可能错过真正有潜力的新群体，不同于专门探索策略。机制取舍不能用一次代理 policy value 判定普遍最优。 示意：两个用户估计增量相同，一人数据丰富、一人只有一次反馈；保守分配偏向前者，但若要主动探索，可能需要另一套预算安排。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-fcfc9a80acae26bd">用 τ−λσ 分配与单纯按 uplift 均值，风险偏好如何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aincrementality">From Prediction to Incrementality: Causal Optimization for Large-Scale Targeting and Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不确定度惩罚降低高估且证据不足对象的优先级，适合强调稳健预算价值；仅按均值可能追逐高方差极端值。惩罚也可能错过真正有潜力的新群体，不同于专门探索策略。机制取舍不能用一次代理 policy value 判定普遍最优。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个用户估计增量相同，一人数据丰富、一人只有一次反馈；保守分配偏向前者，但若要主动探索，可能需要另一套预算安排。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.10182">原论文</a> · <a href="../../../../reproductions/2608.10182-incrementality/">实现解读</a> · <a href="#qa-fcfc9a80acae26bd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:incrementality" data-paper-title="From Prediction to Incrementality: Causal Optimization for Large-Scale Targeting and Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="From Prediction to Incrementality: Causal Optimization for Large-Scale Targeting and Recommendation 搜广推与 LLM 应用 LinkedIn 2026-08-10 分别估计处理与不处理时的潜在结果，以 uplift 及其不确定度代替点击概率排序，再在固定触达预算下完成因果分配。这样优化的是动作带来的增量价值，而不是本来就会发生的结果。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线按 treated outcome 排序，实验组按 uplift 与不确定度分配；同为 30% 预算，seed 42 的 policy value 为 0.10408，基线为 0.09537。  causal-recommendation uplift bandit constrained-allocation 搜广推 学习信号、多任务与反馈偏差 固定预算分配为什么既要检查 B，也要允许不花满？ 约束是总动作数不超过 B，风险调整价值可能全负，不应为填满预算而触达无益对象。排序与求解需使用同一对象身份及截止特征，不能看测试后结果挑用户。来源固定百分比代理不等于真实长期在线增量。 示意：预算可发十条但只三位用户风险调整后为正，硬发十条可能降低价值；除非业务明确要求花满，数学约束并没规定必须全部使用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3fa67cab9ff6ef8f">固定预算分配为什么既要检查 B，也要允许不花满？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aincrementality">From Prediction to Incrementality: Causal Optimization for Large-Scale Targeting and Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>约束是总动作数不超过 B，风险调整价值可能全负，不应为填满预算而触达无益对象。排序与求解需使用同一对象身份及截止特征，不能看测试后结果挑用户。来源固定百分比代理不等于真实长期在线增量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>预算可发十条但只三位用户风险调整后为正，硬发十条可能降低价值；除非业务明确要求花满，数学约束并没规定必须全部使用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.10182">原论文</a> · <a href="../../../../reproductions/2608.10182-incrementality/">实现解读</a> · <a href="#qa-3fa67cab9ff6ef8f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:twitch-mor" data-paper-title="Multi-Objective Ranking for Live-Streaming: Balancing Fresh and Delayed Signals with Segment-Aware Targeting" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Multi-Objective Ranking for Live-Streaming: Balancing Fresh and Delayed Signals with Segment-Aware Targeting 搜广推与 LLM 应用 Twitch 2026-08-05 主题：直播多目标排序。直播观看、互动、关注和付费的反馈延迟不同，且生命周期分群差异明显。论文组合即时/延迟模型、分群目标权重与 MMoE，在共享专家的同时保留目标专属 gate。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。MovieLens-1M 构造五个即时/延迟目标，比较单目标 DNN 与三专家生命周期 MMoE。  ranking multi-task-learning mmoe live-streaming 搜广推 学习信号、多任务与反馈偏差 Twitch多目标排序为什么区分即时与延迟反馈？ 观看互动很快可见，关注付费可能更晚，直接把未成熟目标当负会偏差；生命周期分群又有不同目标偏好，需结合时间与群体条件。 例如刚进入直播用户尚未付费，不该立即当作对该主播无价值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-twitch-mor-68bc3da8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-bf5fda6b62b7980b">Twitch多目标排序为什么区分即时与延迟反馈？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atwitch-mor">Multi-Objective Ranking for Live-Streaming: Balancing Fresh and Delayed Signals with Segment-Aware Targeting</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Twitch</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>观看互动很快可见，关注付费可能更晚，直接把未成熟目标当负会偏差；生命周期分群又有不同目标偏好，需结合时间与群体条件。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如刚进入直播用户尚未付费，不该立即当作对该主播无价值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04455">原论文</a> · <a href="../../../../reproductions/2608.04455-twitch-mor/">实现解读</a> · <a href="#qa-bf5fda6b62b7980b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:twitch-mor" data-paper-title="Multi-Objective Ranking for Live-Streaming: Balancing Fresh and Delayed Signals with Segment-Aware Targeting" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Multi-Objective Ranking for Live-Streaming: Balancing Fresh and Delayed Signals with Segment-Aware Targeting 搜广推与 LLM 应用 Twitch 2026-08-05 主题：直播多目标排序。直播观看、互动、关注和付费的反馈延迟不同，且生命周期分群差异明显。论文组合即时/延迟模型、分群目标权重与 MMoE，在共享专家的同时保留目标专属 gate。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。MovieLens-1M 构造五个即时/延迟目标，比较单目标 DNN 与三专家生命周期 MMoE。  ranking multi-task-learning mmoe live-streaming 搜广推 学习信号、多任务与反馈偏差 Twitch 多目标排序为什么同时处理反馈延迟、用户生命周期权重和 MMoE gate？ 观看、互动、关注与付费在观测时点和用户阶段上含义不同，直接混成一个目标会偏向容易立即得到的信号。即时与延迟模型处理成熟度差异，分群权重表达不同生命周期目标，MMoE 则共享有用专家并保留任务选择。三者针对标签、业务取舍和表示冲突，不能只用一个总体指标证明所有阶段受益。 示意：新用户先建立观看习惯，老用户可能更看重深度互动；付费还比点击晚发生。模型分别处理时间与阶段，再通过任务 gate 组合专家，而不是让点击数量压过全部目标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:twitch-mor" data-paper-title="Multi-Objective Ranking for Live-Streaming: Balancing Fresh and Delayed Signals with Segment-Aware Targeting" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Multi-Objective Ranking for Live-Streaming: Balancing Fresh and Delayed Signals with Segment-Aware Targeting 搜广推与 LLM 应用 Twitch 2026-08-05 主题：直播多目标排序。直播观看、互动、关注和付费的反馈延迟不同，且生命周期分群差异明显。论文组合即时/延迟模型、分群目标权重与 MMoE，在共享专家的同时保留目标专属 gate。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。MovieLens-1M 构造五个即时/延迟目标，比较单目标 DNN 与三专家生命周期 MMoE。  ranking multi-task-learning mmoe live-streaming 搜广推 学习信号、多任务与反馈偏差 MMoE任务gate与分群目标权重是不是同一层？ gate决定每任务用哪些共享专家，分群权重决定各任务损失或目标贡献，层次不同。只改变一个全局权重不能代表任务专属专家交互已完成。 例如新用户多重观看目标，同时各目标仍有不同专家混合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-8aaac58d9bd49b60">MMoE任务gate与分群目标权重是不是同一层？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atwitch-mor">Multi-Objective Ranking for Live-Streaming: Balancing Fresh and Delayed Signals with Segment-Aware Targeting</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Twitch</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>gate决定每任务用哪些共享专家，分群权重决定各任务损失或目标贡献，层次不同。只改变一个全局权重不能代表任务专属专家交互已完成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如新用户多重观看目标，同时各目标仍有不同专家混合。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04455">原论文</a> · <a href="../../../../reproductions/2608.04455-twitch-mor/">实现解读</a> · <a href="#qa-8aaac58d9bd49b60">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:twitch-mor" data-paper-title="Multi-Objective Ranking for Live-Streaming: Balancing Fresh and Delayed Signals with Segment-Aware Targeting" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Multi-Objective Ranking for Live-Streaming: Balancing Fresh and Delayed Signals with Segment-Aware Targeting 搜广推与 LLM 应用 Twitch 2026-08-05 主题：直播多目标排序。直播观看、互动、关注和付费的反馈延迟不同，且生命周期分群差异明显。论文组合即时/延迟模型、分群目标权重与 MMoE，在共享专家的同时保留目标专属 gate。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。MovieLens-1M 构造五个即时/延迟目标，比较单目标 DNN 与三专家生命周期 MMoE。  ranking multi-task-learning mmoe live-streaming 搜广推 学习信号、多任务与反馈偏差 本地Twitch-MOR能直接解释原文生产直播收益吗？ 不能，参考机制未包含真实延迟标签、私有特征和在线流量。分群定义与反馈成熟窗口需固定，不可用最终测试付费来反向定义当前用户segment。 例如测试后才知道谁会付费，再把他标成高价值群，会泄露结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-cb40c9610249d15e">本地Twitch-MOR能直接解释原文生产直播收益吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atwitch-mor">Multi-Objective Ranking for Live-Streaming: Balancing Fresh and Delayed Signals with Segment-Aware Targeting</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Twitch</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，参考机制未包含真实延迟标签、私有特征和在线流量。分群定义与反馈成熟窗口需固定，不可用最终测试付费来反向定义当前用户segment。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如测试后才知道谁会付费，再把他标成高价值群，会泄露结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04455">原论文</a> · <a href="../../../../reproductions/2608.04455-twitch-mor/">实现解读</a> · <a href="#qa-cb40c9610249d15e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:llm-ts-prior" data-paper-title="LLM-Derived Priors for Thompson Sampling in Cold-Start Comment Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="LLM-Derived Priors for Thompson Sampling in Cold-Start Comment Recommendation 搜广推与 LLM 应用 NAVER WEBTOON 2026-08-04 主题：LLM 语义先验与冷启动 bandit。新评论缺少交互反馈，但文本已含性别/内容偏好线索。论文把 LLM 语义判断转为 Beta 伪计数，并按性别年龄分群维护 Thompson posterior。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。以 MovieLens genre 代理文本语义，运行分群 Beta prior 与 40 轮 Thompson 在线更新；明确保留负向及不显著结果。  llm-recommendation bandit cold-start comment-ranking 搜广推 学习信号、多任务与反馈偏差 LLM-TS Prior 为什么把语义判断转成 Beta 伪计数，而非直接决定推荐？ 语言模型给新品一个初始成功概率，伪计数把它纳入可被反馈更新的贝叶斯状态，Thompson sampling 再平衡探索。这样先验只是起点，不应压过所有真实观察。文本可能含偏差，分群也不保证用户内部同质。 示意：新品评论被判断适合某群体，先得到温和先验，后续点击与忽略逐次修正；不能因模型一开始说适合就永久只推它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-llm-ts-prior-97482120" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d04d3e08bb42ff94">LLM-TS Prior 为什么把语义判断转成 Beta 伪计数，而非直接决定推荐？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Allm-ts-prior">LLM-Derived Priors for Thompson Sampling in Cold-Start Comment Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NAVER WEBTOON</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语言模型给新品一个初始成功概率，伪计数把它纳入可被反馈更新的贝叶斯状态，Thompson sampling 再平衡探索。这样先验只是起点，不应压过所有真实观察。文本可能含偏差，分群也不保证用户内部同质。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新品评论被判断适合某群体，先得到温和先验，后续点击与忽略逐次修正；不能因模型一开始说适合就永久只推它。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03382">原论文</a> · <a href="../../../../reproductions/2608.03382-llm-ts-prior/">实现解读</a> · <a href="#qa-d04d3e08bb42ff94">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:llm-ts-prior" data-paper-title="LLM-Derived Priors for Thompson Sampling in Cold-Start Comment Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="LLM-Derived Priors for Thompson Sampling in Cold-Start Comment Recommendation 搜广推与 LLM 应用 NAVER WEBTOON 2026-08-04 主题：LLM 语义先验与冷启动 bandit。新评论缺少交互反馈，但文本已含性别/内容偏好线索。论文把 LLM 语义判断转为 Beta 伪计数，并按性别年龄分群维护 Thompson posterior。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。以 MovieLens genre 代理文本语义，运行分群 Beta prior 与 40 轮 Thompson 在线更新；明确保留负向及不显著结果。  llm-recommendation bandit cold-start comment-ranking 搜广推 学习信号、多任务与反馈偏差 把LLM判断转成Beta伪计数时，为什么先验强度κ和预测概率p一样重要？ 概率决定初始偏好方向，伪计数强度决定新反馈需要多少次才能改变它。κ过大时，错误语义判断可能长期压过真实反馈；过小时又几乎不能缓解冷启动。Thompson采样在后验上探索并持续更新，因此LLM只提供起点而非永久答案；本地分群代理实验不能证明文本先验普遍有效。 示意：两个新内容都得到80%语义先验，一个只相当于几次观察，另一个相当于上千次；出现连续负反馈后，前者很快改变，后者仍可能固执地被推荐。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:llm-ts-prior" data-paper-title="LLM-Derived Priors for Thompson Sampling in Cold-Start Comment Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="LLM-Derived Priors for Thompson Sampling in Cold-Start Comment Recommendation 搜广推与 LLM 应用 NAVER WEBTOON 2026-08-04 主题：LLM 语义先验与冷启动 bandit。新评论缺少交互反馈，但文本已含性别/内容偏好线索。论文把 LLM 语义判断转为 Beta 伪计数，并按性别年龄分群维护 Thompson posterior。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。以 MovieLens genre 代理文本语义，运行分群 Beta prior 与 40 轮 Thompson 在线更新；明确保留负向及不显著结果。  llm-recommendation bandit cold-start comment-ranking 搜广推 学习信号、多任务与反馈偏差 相同 p 不同 κ 的先验，为什么在早期反馈下表现不同？ p 决定均值方向，κ 决定伪观察量和置信强度，强先验更难被少量真实反馈改变。概率相同不意味着同样探索；过强 κ 可锁住错误语义判断，过弱则几乎没借到知识。机制差异不等于某 κ 在所有人群更好。 示意：两份先验都估六成，一份相当两次观察、一份相当两百次；新增三次失败时，前者会明显调整，后者几乎仍坚持原判断。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-914728a81f5028cf">相同 p 不同 κ 的先验，为什么在早期反馈下表现不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Allm-ts-prior">LLM-Derived Priors for Thompson Sampling in Cold-Start Comment Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NAVER WEBTOON</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>p 决定均值方向，κ 决定伪观察量和置信强度，强先验更难被少量真实反馈改变。概率相同不意味着同样探索；过强 κ 可锁住错误语义判断，过弱则几乎没借到知识。机制差异不等于某 κ 在所有人群更好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两份先验都估六成，一份相当两次观察、一份相当两百次；新增三次失败时，前者会明显调整，后者几乎仍坚持原判断。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03382">原论文</a> · <a href="../../../../reproductions/2608.03382-llm-ts-prior/">实现解读</a> · <a href="#qa-914728a81f5028cf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:llm-ts-prior" data-paper-title="LLM-Derived Priors for Thompson Sampling in Cold-Start Comment Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="LLM-Derived Priors for Thompson Sampling in Cold-Start Comment Recommendation 搜广推与 LLM 应用 NAVER WEBTOON 2026-08-04 主题：LLM 语义先验与冷启动 bandit。新评论缺少交互反馈，但文本已含性别/内容偏好线索。论文把 LLM 语义判断转为 Beta 伪计数，并按性别年龄分群维护 Thompson posterior。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。以 MovieLens genre 代理文本语义，运行分群 Beta prior 与 40 轮 Thompson 在线更新；明确保留负向及不显著结果。  llm-recommendation bandit cold-start comment-ranking 搜广推 学习信号、多任务与反馈偏差 Beta prior 更新时，为何应区分先验伪计数与实际成功失败？ 初始化按 1+κp、1+κ(1−p) 形成参数，后续只给已展示并得到反馈的 arm 加真实计数，未曝光不应记失败。分群状态要按定义独立维护，测试未来反馈不得用于初始化。本地 genre 代理不是 LLM 语义调用的完整证明。 示意：一个 arm 没被选中就没有这轮反馈，不能因其他 arm 赢了给它加负例；否则探索迅速排斥未试选项，失去后验含义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-28b338121e35df01">Beta prior 更新时，为何应区分先验伪计数与实际成功失败？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Allm-ts-prior">LLM-Derived Priors for Thompson Sampling in Cold-Start Comment Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NAVER WEBTOON</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>初始化按 1+κp、1+κ(1−p) 形成参数，后续只给已展示并得到反馈的 arm 加真实计数，未曝光不应记失败。分群状态要按定义独立维护，测试未来反馈不得用于初始化。本地 genre 代理不是 LLM 语义调用的完整证明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个 arm 没被选中就没有这轮反馈，不能因其他 arm 赢了给它加负例；否则探索迅速排斥未试选项，失去后验含义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03382">原论文</a> · <a href="../../../../reproductions/2608.03382-llm-ts-prior/">实现解读</a> · <a href="#qa-28b338121e35df01">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:twice" data-paper-title="TWICE: Two-Clock, Two-Window Learning for Long-Horizon Conversion Prediction in Online Advertising" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="TWICE: Two-Clock, Two-Window Learning for Long-Horizon Conversion Prediction in Online Advertising 搜广推与 LLM 应用 Kuaishou 2026-07-28 把点击时钟的 current-status 标签与转化时钟的 delay CDF 分开学习，再用曝光窗口权重校正长期未成熟标签。 Fidelity: 核心机制复现。本地执行双时钟、双窗口校正路径和统一评测，私有工业特征与服务未复刻。公开交互代理广告延迟，未包含生产聚合记录和真实 revenue；线上数字只引用论文。本地对照口径：基线为 mature-label next-item CVR，实验组为双时钟 current-status；Hit@10 +8.00%、NDCG@10 +14.31%。  advertising cvr delayed-feedback full-traffic 搜广推 学习信号、多任务与反馈偏差 TWICE为什么把尚未转化与永不转化区分？ 点击后订单可能很晚才出现，当前负标签未成熟。最终CVR乘延迟CDF描述截至当前观察到的概率，避免把所有暂未转化当真负。 例如用户今天点击，明天才购买，今天不能直接判定永远不买。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-twice-bd9f2dd2" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-62772935573ba6cb">TWICE为什么把尚未转化与永不转化区分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atwice">TWICE: Two-Clock, Two-Window Learning for Long-Horizon Conversion Prediction in Online Advertising</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>点击后订单可能很晚才出现，当前负标签未成熟。最终CVR乘延迟CDF描述截至当前观察到的概率，避免把所有暂未转化当真负。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户今天点击，明天才购买，今天不能直接判定永远不买。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25404">原论文</a> · <a href="../../../../reproductions/2607.25404-twice/">实现解读</a> · <a href="#qa-62772935573ba6cb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:twice" data-paper-title="TWICE: Two-Clock, Two-Window Learning for Long-Horizon Conversion Prediction in Online Advertising" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="TWICE: Two-Clock, Two-Window Learning for Long-Horizon Conversion Prediction in Online Advertising 搜广推与 LLM 应用 Kuaishou 2026-07-28 把点击时钟的 current-status 标签与转化时钟的 delay CDF 分开学习，再用曝光窗口权重校正长期未成熟标签。 Fidelity: 核心机制复现。本地执行双时钟、双窗口校正路径和统一评测，私有工业特征与服务未复刻。公开交互代理广告延迟，未包含生产聚合记录和真实 revenue；线上数字只引用论文。本地对照口径：基线为 mature-label next-item CVR，实验组为双时钟 current-status；Hit@10 +8.00%、NDCG@10 +14.31%。  advertising cvr delayed-feedback full-traffic 搜广推 学习信号、多任务与反馈偏差 TWICE 为什么把最终转化概率与 delay CDF 分开学习，而不把未转化样本立刻记为负例？ 观察时尚未转化的样本，可能只是还没等到转化发生。最终概率描述是否会转化，延迟分布描述在给定等待时间内已发生的比例，两者相乘对应当前可观测状态。双时钟与曝光窗口校正减轻标签成熟度差异，但需要合理的延迟建模；公开时间戳代理不能证明真实广告转化延迟被恢复。 示意：刚点击五分钟未买不应与等待一周仍未买等同。模型分别估计最终购买机会与五分钟内完成的比例，让“还没发生”不被直接当作“永远不会发生”。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:twice" data-paper-title="TWICE: Two-Clock, Two-Window Learning for Long-Horizon Conversion Prediction in Online Advertising" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="TWICE: Two-Clock, Two-Window Learning for Long-Horizon Conversion Prediction in Online Advertising 搜广推与 LLM 应用 Kuaishou 2026-07-28 把点击时钟的 current-status 标签与转化时钟的 delay CDF 分开学习，再用曝光窗口权重校正长期未成熟标签。 Fidelity: 核心机制复现。本地执行双时钟、双窗口校正路径和统一评测，私有工业特征与服务未复刻。公开交互代理广告延迟，未包含生产聚合记录和真实 revenue；线上数字只引用论文。本地对照口径：基线为 mature-label next-item CVR，实验组为双时钟 current-status；Hit@10 +8.00%、NDCG@10 +14.31%。  advertising cvr delayed-feedback full-traffic 搜广推 学习信号、多任务与反馈偏差 点击时钟current-status与转化时钟delay各提供什么？ 前者看点击后当前成熟状态，后者建模延迟分布，两窗口联合校正观察偏差。只有单时钟容易混淆是否转化与何时可见，不是多加一个时间特征就相同。 例如相同等待时长在不同采样窗口会有不同标签成熟程度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-cb053d77c23dd08a">点击时钟current-status与转化时钟delay各提供什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atwice">TWICE: Two-Clock, Two-Window Learning for Long-Horizon Conversion Prediction in Online Advertising</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者看点击后当前成熟状态，后者建模延迟分布，两窗口联合校正观察偏差。只有单时钟容易混淆是否转化与何时可见，不是多加一个时间特征就相同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如相同等待时长在不同采样窗口会有不同标签成熟程度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25404">原论文</a> · <a href="../../../../reproductions/2607.25404-twice/">实现解读</a> · <a href="#qa-cb053d77c23dd08a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:twice" data-paper-title="TWICE: Two-Clock, Two-Window Learning for Long-Horizon Conversion Prediction in Online Advertising" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="TWICE: Two-Clock, Two-Window Learning for Long-Horizon Conversion Prediction in Online Advertising 搜广推与 LLM 应用 Kuaishou 2026-07-28 把点击时钟的 current-status 标签与转化时钟的 delay CDF 分开学习，再用曝光窗口权重校正长期未成熟标签。 Fidelity: 核心机制复现。本地执行双时钟、双窗口校正路径和统一评测，私有工业特征与服务未复刻。公开交互代理广告延迟，未包含生产聚合记录和真实 revenue；线上数字只引用论文。本地对照口径：基线为 mature-label next-item CVR，实验组为双时钟 current-status；Hit@10 +8.00%、NDCG@10 +14.31%。  advertising cvr delayed-feedback full-traffic 搜广推 学习信号、多任务与反馈偏差 TWICE的delay CDF需满足什么单调边界？ 时间越晚累计转化可见概率不能下降，数值需在零一范围，并与最终CVR角色分开。当前公开交互代理广告延迟，没有真实聚合记录或revenue，不能报生产收益。 例如等待从一天到两天，CDF不能从较高值反而下降。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1e0c01dbb4d8dde1">TWICE的delay CDF需满足什么单调边界？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atwice">TWICE: Two-Clock, Two-Window Learning for Long-Horizon Conversion Prediction in Online Advertising</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>时间越晚累计转化可见概率不能下降，数值需在零一范围，并与最终CVR角色分开。当前公开交互代理广告延迟，没有真实聚合记录或revenue，不能报生产收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如等待从一天到两天，CDF不能从较高值反而下降。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25404">原论文</a> · <a href="../../../../reproductions/2607.25404-twice/">实现解读</a> · <a href="#qa-1e0c01dbb4d8dde1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pinequalizer" data-paper-title="PinEqualizer: Full Funnel Content Exploration and Debiasing System at Pinterest" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="PinEqualizer: Full Funnel Content Exploration and Debiasing System at Pinterest 搜广推与 LLM 应用 Pinterest 2026-07-23 新内容缺少协同图和历史互动，生产模型又会依赖已有曝光形成反馈回路。PinEqualizer 不把问题限制在一个排序模型，而是在 corpus selection、召回、精排和 utility 每一级检查 fresh 内容的输入占比与存活率。模型侧加入纯内容/VLM/SID 特征、逐 engagement 特征 dropout、内容—年龄—互动显式交叉、分内容类型 calibration 和 fresh/old 分数正则； Fidelity: 核心机制复现。真实执行 engagement dropout、内容交叉、分 cohort calibration、探索 corpus 与 relevance-scaled UCB；私有多阶段系统由公开代理缩小。MovieLens 的物品首见时间只是新内容代理：fresh 定义为首见时间最新 20%，underexplored 再限制为低于 fresh popularity 中位数。实现没有 Pinterest 的 PinCLIP、SID、商家数据、三大 surface、长期内容 holdout 和实时 Flink 特征；  cold-start exploration debiasing ranking retrieval 搜广推 学习信号、多任务与反馈偏差 PinEqualizer 为什么把新内容探索看成供给与模型共同问题？ 新内容可在 corpus、召回、排序任何环节消失，单点加分不足；内容特征减少依赖旧互动，独立探索 corpus 提供入场机会，不确定性策略分流反馈。全链路存活率帮助定位瓶颈，但新内容配额高不代表整体相关性不受损。 示意：精排再愿意推荐新品，若召回从未包含它就无效；先检查候选入口，再决定模型去偏与探索该在哪层增加。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-pinequalizer-1595745d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c43ee2f671ca7474">PinEqualizer 为什么把新内容探索看成供给与模型共同问题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apinequalizer">PinEqualizer: Full Funnel Content Exploration and Debiasing System at Pinterest</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>新内容可在 corpus、召回、排序任何环节消失，单点加分不足；内容特征减少依赖旧互动，独立探索 corpus 提供入场机会，不确定性策略分流反馈。全链路存活率帮助定位瓶颈，但新内容配额高不代表整体相关性不受损。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>精排再愿意推荐新品，若召回从未包含它就无效；先检查候选入口，再决定模型去偏与探索该在哪层增加。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.22518">原论文</a> · <a href="../../../../reproductions/2607.22518-pinequalizer/">实现解读</a> · <a href="#qa-c43ee2f671ca7474">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pinequalizer" data-paper-title="PinEqualizer: Full Funnel Content Exploration and Debiasing System at Pinterest" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="PinEqualizer: Full Funnel Content Exploration and Debiasing System at Pinterest 搜广推与 LLM 应用 Pinterest 2026-07-23 新内容缺少协同图和历史互动，生产模型又会依赖已有曝光形成反馈回路。PinEqualizer 不把问题限制在一个排序模型，而是在 corpus selection、召回、精排和 utility 每一级检查 fresh 内容的输入占比与存活率。模型侧加入纯内容/VLM/SID 特征、逐 engagement 特征 dropout、内容—年龄—互动显式交叉、分内容类型 calibration 和 fresh/old 分数正则； Fidelity: 核心机制复现。真实执行 engagement dropout、内容交叉、分 cohort calibration、探索 corpus 与 relevance-scaled UCB；私有多阶段系统由公开代理缩小。MovieLens 的物品首见时间只是新内容代理：fresh 定义为首见时间最新 20%，underexplored 再限制为低于 fresh popularity 中位数。实现没有 Pinterest 的 PinCLIP、SID、商家数据、三大 surface、长期内容 holdout 和实时 Flink 特征；  cold-start exploration debiasing ranking retrieval 搜广推 学习信号、多任务与反馈偏差 PinEqualizer 为什么沿整条分发链检查新内容存活率，而不只在精排里提高新内容分数？ 新内容可能在语料选择或召回阶段已经消失，精排再加分也看不到它。逐级检查输入占比和存活率能定位瓶颈；内容特征、互动特征 dropout 和校准减少模型依赖旧曝光，独立探索与不确定性奖励再补采反馈。探索仍要受相关性约束，否则只奖励低曝光会把不合适内容推给用户。 示意：一篇新食谱在召回前就被过滤，精排加分无济于事。先为新内容保留进入机会，再按相关性和不确定性分配少量探索流量，才能收集判断质量所需的反馈。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pinequalizer" data-paper-title="PinEqualizer: Full Funnel Content Exploration and Debiasing System at Pinterest" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="PinEqualizer: Full Funnel Content Exploration and Debiasing System at Pinterest 搜广推与 LLM 应用 Pinterest 2026-07-23 新内容缺少协同图和历史互动，生产模型又会依赖已有曝光形成反馈回路。PinEqualizer 不把问题限制在一个排序模型，而是在 corpus selection、召回、精排和 utility 每一级检查 fresh 内容的输入占比与存活率。模型侧加入纯内容/VLM/SID 特征、逐 engagement 特征 dropout、内容—年龄—互动显式交叉、分内容类型 calibration 和 fresh/old 分数正则； Fidelity: 核心机制复现。真实执行 engagement dropout、内容交叉、分 cohort calibration、探索 corpus 与 relevance-scaled UCB；私有多阶段系统由公开代理缩小。MovieLens 的物品首见时间只是新内容代理：fresh 定义为首见时间最新 20%，underexplored 再限制为低于 fresh popularity 中位数。实现没有 Pinterest 的 PinCLIP、SID、商家数据、三大 surface、长期内容 holdout 和实时 Flink 特征；  cold-start exploration debiasing ranking retrieval 搜广推 学习信号、多任务与反馈偏差 PinEqualizer 的 UCB 与仅降低热门分，相比为何同时关注不确定性与相关性？ 降热门只是反向惩罚，不知道哪些冷内容值得试；UCB 给少曝光或高不确定对象机会，搜索再乘相关性限制无关探索。它仍有精度代价，来源本地整体 NDCG 下降而 fresh 大升，不能只报探索数字。 示意：低曝光的相关新食谱值得少量试探，不相关冷门新闻则不应仅因冷而上榜；相关性 gate 避免把探索变成随机打散。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a636a4fd426b06ff">PinEqualizer 的 UCB 与仅降低热门分，相比为何同时关注不确定性与相关性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apinequalizer">PinEqualizer: Full Funnel Content Exploration and Debiasing System at Pinterest</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>降热门只是反向惩罚，不知道哪些冷内容值得试；UCB 给少曝光或高不确定对象机会，搜索再乘相关性限制无关探索。它仍有精度代价，来源本地整体 NDCG 下降而 fresh 大升，不能只报探索数字。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>低曝光的相关新食谱值得少量试探，不相关冷门新闻则不应仅因冷而上榜；相关性 gate 避免把探索变成随机打散。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.22518">原论文</a> · <a href="../../../../reproductions/2607.22518-pinequalizer/">实现解读</a> · <a href="#qa-a636a4fd426b06ff">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pinequalizer" data-paper-title="PinEqualizer: Full Funnel Content Exploration and Debiasing System at Pinterest" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="PinEqualizer: Full Funnel Content Exploration and Debiasing System at Pinterest 搜广推与 LLM 应用 Pinterest 2026-07-23 新内容缺少协同图和历史互动，生产模型又会依赖已有曝光形成反馈回路。PinEqualizer 不把问题限制在一个排序模型，而是在 corpus selection、召回、精排和 utility 每一级检查 fresh 内容的输入占比与存活率。模型侧加入纯内容/VLM/SID 特征、逐 engagement 特征 dropout、内容—年龄—互动显式交叉、分内容类型 calibration 和 fresh/old 分数正则； Fidelity: 核心机制复现。真实执行 engagement dropout、内容交叉、分 cohort calibration、探索 corpus 与 relevance-scaled UCB；私有多阶段系统由公开代理缩小。MovieLens 的物品首见时间只是新内容代理：fresh 定义为首见时间最新 20%，underexplored 再限制为低于 fresh popularity 中位数。实现没有 Pinterest 的 PinCLIP、SID、商家数据、三大 surface、长期内容 holdout 和实时 Flink 特征；  cold-start exploration debiasing ranking retrieval 搜广推 学习信号、多任务与反馈偏差 PinEqualizer 验证全选 UCB α=0，为什么不能继续加大 α 调出好看的 fresh 指标？ 验证目标已表明额外探索损害当前取舍，应保留零选择，test 不用于重挑 α。去偏模型本身可已大幅增加 fresh 分发，探索项不是必须强开。fresh、小分母与整体指标要共同报告，不能更换目标隐去主质量退化。 示意：模型已让新品曝光翻几倍，继续 UCB 只让相关性更差；应报告这一边界，而非为了显得有 bandit 就强制启用正 α。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-429c749e92f0ed36">PinEqualizer 验证全选 UCB α=0，为什么不能继续加大 α 调出好看的 fresh 指标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apinequalizer">PinEqualizer: Full Funnel Content Exploration and Debiasing System at Pinterest</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>验证目标已表明额外探索损害当前取舍，应保留零选择，test 不用于重挑 α。去偏模型本身可已大幅增加 fresh 分发，探索项不是必须强开。fresh、小分母与整体指标要共同报告，不能更换目标隐去主质量退化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型已让新品曝光翻几倍，继续 UCB 只让相关性更差；应报告这一边界，而非为了显得有 bandit 就强制启用正 α。</p>
<p class="ar-learning-sources">依据：本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.22518">原论文</a> · <a href="../../../../reproductions/2607.22518-pinequalizer/">实现解读</a> · <a href="#qa-429c749e92f0ed36">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ramp" data-paper-title="RAMP: Robust Ad Recommendation Under Limited Personalized-Feature Availability via Masking and Alignment Pathways" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="RAMP: Robust Ad Recommendation Under Limited Personalized-Feature Availability via Masking and Alignment Pathways 搜广推与 LLM 应用 Huawei Ireland Research Center / University College Dublin 2026-07-20 隐私选择、权限或平台限制会让同一广告模型在部分流量上拿不到个性化字段。RAMP 不把缺失值简单填零，而是显式维护 personalized 与 non-personalized 两条路径，用可用性 mask 控制输出，并通过 prediction alignment 把富特征路径的知识蒸馏给受限路径。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练 masked 双路径与 prediction alignment；私有工业 CVR 数据未复刻。MovieLens 行为向量代理受限个性化字段、类型特征代理公共广告字段；训练中实际执行双路径、输出 masking 和富特征 teacher 到受限路径的 KL 对齐，测试专门评估无个性化字段流量。  advertising privacy distillation missing-features 搜广推 学习信号、多任务与反馈偏差 RAMP 的 non-personalized 路径是否意味着给所有请求同一个预测？ 不是。它不使用受限个性化字段，仍能依据广告内容、公共属性和请求上下文产生不同结果。无个人历史不等于没有任何输入，完全常数预测反而丢掉合法可用证据。具体公共字段应遵守来源与权限定义，不能以 public 名称包装个人标识。 示意：同一匿名用户在雨天看雨具广告与晴天看食品广告，公共内容和场景不同，预测可以不同；这无需读取他的私人浏览史。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-ramp-9687450e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-917b7d6f5d4a1bc0">RAMP 的 non-personalized 路径是否意味着给所有请求同一个预测？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aramp">RAMP: Robust Ad Recommendation Under Limited Personalized-Feature Availability via Masking and Alignment Pathways</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Ireland Research Center / University College Dublin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。它不使用受限个性化字段，仍能依据广告内容、公共属性和请求上下文产生不同结果。无个人历史不等于没有任何输入，完全常数预测反而丢掉合法可用证据。具体公共字段应遵守来源与权限定义，不能以 public 名称包装个人标识。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一匿名用户在雨天看雨具广告与晴天看食品广告，公共内容和场景不同，预测可以不同；这无需读取他的私人浏览史。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.17473">原论文</a> · <a href="../../../../reproductions/2607.17473-ramp/">实现解读</a> · <a href="#qa-917b7d6f5d4a1bc0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ramp" data-paper-title="RAMP: Robust Ad Recommendation Under Limited Personalized-Feature Availability via Masking and Alignment Pathways" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="RAMP: Robust Ad Recommendation Under Limited Personalized-Feature Availability via Masking and Alignment Pathways 搜广推与 LLM 应用 Huawei Ireland Research Center / University College Dublin 2026-07-20 隐私选择、权限或平台限制会让同一广告模型在部分流量上拿不到个性化字段。RAMP 不把缺失值简单填零，而是显式维护 personalized 与 non-personalized 两条路径，用可用性 mask 控制输出，并通过 prediction alignment 把富特征路径的知识蒸馏给受限路径。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练 masked 双路径与 prediction alignment；私有工业 CVR 数据未复刻。MovieLens 行为向量代理受限个性化字段、类型特征代理公共广告字段；训练中实际执行双路径、输出 masking 和富特征 teacher 到受限路径的 KL 对齐，测试专门评估无个性化字段流量。  advertising privacy distillation missing-features 搜广推 学习信号、多任务与反馈偏差 RAMP 为什么为缺少个性化字段的流量保留独立路径，而不是统一填零？ 填零会把“字段不可用”与真实零值混为一谈，还要求同一表示同时适应差异很大的输入分布。RAMP 用可用性掩码选择个性化或公共路径，并在训练期把富特征预测对齐给受限路径，让后者学习可迁移知识。受限路径推理仍只用获准字段，蒸馏不能让它恢复原本不可见的个人信息。 示意：用户未授权行为特征时，只走内容与上下文路径；训练时可从有授权样本的丰富预测获得软监督。上线不能为了复制教师分数再偷偷读取缺失的历史字段。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ramp" data-paper-title="RAMP: Robust Ad Recommendation Under Limited Personalized-Feature Availability via Masking and Alignment Pathways" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="RAMP: Robust Ad Recommendation Under Limited Personalized-Feature Availability via Masking and Alignment Pathways 搜广推与 LLM 应用 Huawei Ireland Research Center / University College Dublin 2026-07-20 隐私选择、权限或平台限制会让同一广告模型在部分流量上拿不到个性化字段。RAMP 不把缺失值简单填零，而是显式维护 personalized 与 non-personalized 两条路径，用可用性 mask 控制输出，并通过 prediction alignment 把富特征路径的知识蒸馏给受限路径。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练 masked 双路径与 prediction alignment；私有工业 CVR 数据未复刻。MovieLens 行为向量代理受限个性化字段、类型特征代理公共广告字段；训练中实际执行双路径、输出 masking 和富特征 teacher 到受限路径的 KL 对齐，测试专门评估无个性化字段流量。  advertising privacy distillation missing-features 搜广推 学习信号、多任务与反馈偏差 RAMP 的蒸馏对齐与单纯缺失特征训练，额外借用了哪类信号？ 缺失训练只用硬标签教模型适应受限输入，对齐还让富特征路径提供软判断，传递标签之外关系。受限学生不一定能恢复全部信息，教师偏差也会迁移。来源大相对增幅来自很低基线，不能只报百分比当工业鲁棒性定论。 示意：公共特征相近两广告，教师可用更多历史给软差别；学生学这份趋势，但没有足够公共线索时仍无法分清每个用户。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ee66fd4cfb400d2b">RAMP 的蒸馏对齐与单纯缺失特征训练，额外借用了哪类信号？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aramp">RAMP: Robust Ad Recommendation Under Limited Personalized-Feature Availability via Masking and Alignment Pathways</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Ireland Research Center / University College Dublin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>缺失训练只用硬标签教模型适应受限输入，对齐还让富特征路径提供软判断，传递标签之外关系。受限学生不一定能恢复全部信息，教师偏差也会迁移。来源大相对增幅来自很低基线，不能只报百分比当工业鲁棒性定论。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>公共特征相近两广告，教师可用更多历史给软差别；学生学这份趋势，但没有足够公共线索时仍无法分清每个用户。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.17473">原论文</a> · <a href="../../../../reproductions/2607.17473-ramp/">实现解读</a> · <a href="#qa-ee66fd4cfb400d2b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ramp" data-paper-title="RAMP: Robust Ad Recommendation Under Limited Personalized-Feature Availability via Masking and Alignment Pathways" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="RAMP: Robust Ad Recommendation Under Limited Personalized-Feature Availability via Masking and Alignment Pathways 搜广推与 LLM 应用 Huawei Ireland Research Center / University College Dublin 2026-07-20 隐私选择、权限或平台限制会让同一广告模型在部分流量上拿不到个性化字段。RAMP 不把缺失值简单填零，而是显式维护 personalized 与 non-personalized 两条路径，用可用性 mask 控制输出，并通过 prediction alignment 把富特征路径的知识蒸馏给受限路径。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练 masked 双路径与 prediction alignment；私有工业 CVR 数据未复刻。MovieLens 行为向量代理受限个性化字段、类型特征代理公共广告字段；训练中实际执行双路径、输出 masking 和富特征 teacher 到受限路径的 KL 对齐，测试专门评估无个性化字段流量。  advertising privacy distillation missing-features 搜广推 学习信号、多任务与反馈偏差 RAMP 可用性 mask 为什么必须由真实权限状态决定而非预测效果？ 输出选择代表字段是否可用，不应看标签或哪个分支事后更准来切换。训练蒸馏可在获准样本上进行，测试受限流量严格禁止个人字段，mask 与缺失值处理也需一致。若把零值当缺失，会混淆真实零特征和不可访问。 示意：某用户购买标签为正时选个人分支、为负选公共分支就是泄漏；正确 mask 只取决于请求时权限与字段存在性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d20381b7e2ac0bfd">RAMP 可用性 mask 为什么必须由真实权限状态决定而非预测效果？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aramp">RAMP: Robust Ad Recommendation Under Limited Personalized-Feature Availability via Masking and Alignment Pathways</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Ireland Research Center / University College Dublin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>输出选择代表字段是否可用，不应看标签或哪个分支事后更准来切换。训练蒸馏可在获准样本上进行，测试受限流量严格禁止个人字段，mask 与缺失值处理也需一致。若把零值当缺失，会混淆真实零特征和不可访问。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某用户购买标签为正时选个人分支、为负选公共分支就是泄漏；正确 mask 只取决于请求时权限与字段存在性。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.17473">原论文</a> · <a href="../../../../reproductions/2607.17473-ramp/">实现解读</a> · <a href="#qa-d20381b7e2ac0bfd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:causal-retrieval" data-paper-title="Deep-learning Causal Retrieval Optimization for Efficient e-commerce Distribution in Pinterest" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Deep-learning Causal Retrieval Optimization for Efficient e-commerce Distribution in Pinterest 搜广推与 LLM 应用 Pinterest 2026-07-14 始终触发 shopping candidate generator 浪费资源，也会向无购物意图用户过度分发。论文用随机日志学习多事件 outcome 和 doubly-robust uplift，离线线性 replay 选阈值，线上与远程召回并行执行。 Fidelity: 核心机制复现。执行 propensity、双 outcome、DR pseudo-outcome 和触发阈值。没有 Pinterest randomized logs、购物 session 或 RPC 成本；本地 pseudo-treatment 仅用于可辨识的机制实验。本地对照口径：基线是固定的非因果 transition/content/popularity retrieval ensemble；实验组以 DR uplift 选择约 30% shopping trigger，NDCG@10 0.03540→0.06399，相对 +80.77%。  causal-retrieval uplift candidate-generation 搜广推 学习信号、多任务与反馈偏差 因果召回中的 treatment 是触发哪种动作，outcome 又是什么？ 处理指是否运行购物候选生成器，结果是后续多事件业务响应，目标估计同类用户触发与不触发的差异。它评价的是资源动作的边际作用，不是购物模型单次预测准确度。只有两种决策在数据中有足够支持，才可能比较该增量。 示意：同样用户上下文下，运行购物召回是否改变购买或消费才是目标；用户本来就很爱购物，不足以证明这次额外运行有帮助。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-causal-retrieval-c13802af" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-dd18e3e23c61a9ea">因果召回中的 treatment 是触发哪种动作，outcome 又是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acausal-retrieval">Deep-learning Causal Retrieval Optimization for Efficient e-commerce Distribution in Pinterest</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>处理指是否运行购物候选生成器，结果是后续多事件业务响应，目标估计同类用户触发与不触发的差异。它评价的是资源动作的边际作用，不是购物模型单次预测准确度。只有两种决策在数据中有足够支持，才可能比较该增量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同样用户上下文下，运行购物召回是否改变购买或消费才是目标；用户本来就很爱购物，不足以证明这次额外运行有帮助。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14161">原论文</a> · <a href="../../../../reproductions/2607.14161-causal-retrieval/">实现解读</a> · <a href="#qa-dd18e3e23c61a9ea">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:causal-retrieval" data-paper-title="Deep-learning Causal Retrieval Optimization for Efficient e-commerce Distribution in Pinterest" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Deep-learning Causal Retrieval Optimization for Efficient e-commerce Distribution in Pinterest 搜广推与 LLM 应用 Pinterest 2026-07-14 始终触发 shopping candidate generator 浪费资源，也会向无购物意图用户过度分发。论文用随机日志学习多事件 outcome 和 doubly-robust uplift，离线线性 replay 选阈值，线上与远程召回并行执行。 Fidelity: 核心机制复现。执行 propensity、双 outcome、DR pseudo-outcome 和触发阈值。没有 Pinterest randomized logs、购物 session 或 RPC 成本；本地 pseudo-treatment 仅用于可辨识的机制实验。本地对照口径：基线是固定的非因果 transition/content/popularity retrieval ensemble；实验组以 DR uplift 选择约 30% shopping trigger，NDCG@10 0.03540→0.06399，相对 +80.77%。  causal-retrieval uplift candidate-generation 搜广推 学习信号、多任务与反馈偏差 因果召回为什么按触发召回带来的uplift决策，而不是按用户本来的购物概率？ 高购物概率用户可能无需额外召回也会购买，资源应关注触发动作所改变的结果。方法用随机日志学习处理与对照结局，并以doubly-robust校正构造增量估计，再通过replay选择触发阈值。估计仍依赖合适的实验支持与重叠条件，不能把普通预测分换个名字就叫因果收益。 示意：甲本来就会购买，额外召回几乎不改变结局；乙购买概率较低但对合适候选敏感。预算紧张时应比较干预增量，而非只把召回给甲。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:causal-retrieval" data-paper-title="Deep-learning Causal Retrieval Optimization for Efficient e-commerce Distribution in Pinterest" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Deep-learning Causal Retrieval Optimization for Efficient e-commerce Distribution in Pinterest 搜广推与 LLM 应用 Pinterest 2026-07-14 始终触发 shopping candidate generator 浪费资源，也会向无购物意图用户过度分发。论文用随机日志学习多事件 outcome 和 doubly-robust uplift，离线线性 replay 选阈值，线上与远程召回并行执行。 Fidelity: 核心机制复现。执行 propensity、双 outcome、DR pseudo-outcome 和触发阈值。没有 Pinterest randomized logs、购物 session 或 RPC 成本；本地 pseudo-treatment 仅用于可辨识的机制实验。本地对照口径：基线是固定的非因果 transition/content/popularity retrieval ensemble；实验组以 DR uplift 选择约 30% shopping trigger，NDCG@10 0.03540→0.06399，相对 +80.77%。  causal-retrieval uplift candidate-generation 搜广推 学习信号、多任务与反馈偏差 DR uplift 与只训练处理组、对照组两个 outcome 模型相比，多了什么校正？ 两模型差估计结局差异，DR 项再按倾向概率缩放观测残差，利用处理分配信息纠正拟合误差。双重稳健依赖其假设与至少适当的模型条件，不是对任意偏差都免疫。来源本地使用合成随机处理，不能直接外推真实平台增量。 示意：某类用户模型低估处理后购买，残差项可按其处理概率校正；若这一类用户从未接受处理，分母与缺乏支持的问题也无法凭公式解决。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-8b7a2a15a35fac28">DR uplift 与只训练处理组、对照组两个 outcome 模型相比，多了什么校正？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acausal-retrieval">Deep-learning Causal Retrieval Optimization for Efficient e-commerce Distribution in Pinterest</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两模型差估计结局差异，DR 项再按倾向概率缩放观测残差，利用处理分配信息纠正拟合误差。双重稳健依赖其假设与至少适当的模型条件，不是对任意偏差都免疫。来源本地使用合成随机处理，不能直接外推真实平台增量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某类用户模型低估处理后购买，残差项可按其处理概率校正；若这一类用户从未接受处理，分母与缺乏支持的问题也无法凭公式解决。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14161">原论文</a> · <a href="../../../../reproductions/2607.14161-causal-retrieval/">实现解读</a> · <a href="#qa-8b7a2a15a35fac28">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:causal-retrieval" data-paper-title="Deep-learning Causal Retrieval Optimization for Efficient e-commerce Distribution in Pinterest" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Deep-learning Causal Retrieval Optimization for Efficient e-commerce Distribution in Pinterest 搜广推与 LLM 应用 Pinterest 2026-07-14 始终触发 shopping candidate generator 浪费资源，也会向无购物意图用户过度分发。论文用随机日志学习多事件 outcome 和 doubly-robust uplift，离线线性 replay 选阈值，线上与远程召回并行执行。 Fidelity: 核心机制复现。执行 propensity、双 outcome、DR pseudo-outcome 和触发阈值。没有 Pinterest randomized logs、购物 session 或 RPC 成本；本地 pseudo-treatment 仅用于可辨识的机制实验。本地对照口径：基线是固定的非因果 transition/content/popularity retrieval ensemble；实验组以 DR uplift 选择约 30% shopping trigger，NDCG@10 0.03540→0.06399，相对 +80.77%。  causal-retrieval uplift candidate-generation 搜广推 学习信号、多任务与反馈偏差 因果召回实现中，为什么倾向概率接近零或一时必须特别检查？ DR 残差分别除以 e(x) 与 1−e(x)，极端概率会放大噪声，缺乏重叠时甚至无法估计对照差。阈值应由独立 replay 或验证口径选择，而非按 test 搜最好触发率；任何裁剪也需记录，因为它改变估计偏差与方差。 示意：某人群只有百分之一机会触发召回，一次结果会被大幅加权；不能把由小分母产生的巨大分数直接当成高置信增量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-edf0a7c6fee81043">因果召回实现中，为什么倾向概率接近零或一时必须特别检查？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acausal-retrieval">Deep-learning Causal Retrieval Optimization for Efficient e-commerce Distribution in Pinterest</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>DR 残差分别除以 e(x) 与 1−e(x)，极端概率会放大噪声，缺乏重叠时甚至无法估计对照差。阈值应由独立 replay 或验证口径选择，而非按 test 搜最好触发率；任何裁剪也需记录，因为它改变估计偏差与方差。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某人群只有百分之一机会触发召回，一次结果会被大幅加权；不能把由小分母产生的巨大分数直接当成高置信增量。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14161">原论文</a> · <a href="../../../../reproductions/2607.14161-causal-retrieval/">实现解读</a> · <a href="#qa-edf0a7c6fee81043">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:danet" data-paper-title="Cheaper is Better: A Discount-Aware Network for Conversion Rate Prediction in E-commerce Recommendation System" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Cheaper is Better: A Discount-Aware Network for Conversion Rate Prediction in E-commerce Recommendation System 搜广推与 LLM 应用 Alibaba Group / Tmall 2026-07-14 只建模兴趣无法解释“便宜多少”对购买的影响。DANet 的 IPN 捕获一般兴趣；DPN 对 400 天 discount-rate 序列做 FFT 滤波和高低频分解，DCM-User 从相似购买中抽取折扣偏好，DCM-Context 用促销周期 gate 修正分布，并以购买样本的真实折扣做辅助回归。 Fidelity: 核心机制复现。参照作者开源代码执行 IPN、FFT/IFFT、DCM-User、DCM-Context 与折扣回归辅助任务。未使用 Tmall 私有 400 天折扣和促销特征；明确区分作者 TensorFlow 代码与本地 NumPy 复现。本地对照口径：基线是 IPN interest score；实验组 DANet 加入折扣代理的 TFTM/DCM，Hit@10 +0.00%、NDCG@10 -1.46%，fresh Hit@10 +50.00%。  ranking cvr discount 搜广推 学习信号、多任务与反馈偏差 DANet 的一般兴趣与折扣偏好为什么分开建模？ 喜欢一个品类不代表只在大促时购买，折扣敏感度是另一种影响行为的维度。IPN 提取一般兴趣，DPN 从长期折扣序列分析节奏，用户与促销上下文模块再调节。两种信号可相互作用，但不能用“爱某商品”直接代替“愿为多大折扣等待”。 示意：两人都爱运动鞋，一人原价就买，另一人等季末促销；若只看同样的浏览兴趣，会错过价格时机上的差别。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-danet-112ada17" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5f4d3b95fcfb94c4">DANet 的一般兴趣与折扣偏好为什么分开建模？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adanet">Cheaper is Better: A Discount-Aware Network for Conversion Rate Prediction in E-commerce Recommendation System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group / Tmall</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>喜欢一个品类不代表只在大促时购买，折扣敏感度是另一种影响行为的维度。IPN 提取一般兴趣，DPN 从长期折扣序列分析节奏，用户与促销上下文模块再调节。两种信号可相互作用，但不能用“爱某商品”直接代替“愿为多大折扣等待”。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两人都爱运动鞋，一人原价就买，另一人等季末促销；若只看同样的浏览兴趣，会错过价格时机上的差别。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12578">原论文</a> · <a href="../../../../reproductions/2607.12578-danet/">实现解读</a> · <a href="#qa-5f4d3b95fcfb94c4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:danet" data-paper-title="Cheaper is Better: A Discount-Aware Network for Conversion Rate Prediction in E-commerce Recommendation System" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Cheaper is Better: A Discount-Aware Network for Conversion Rate Prediction in E-commerce Recommendation System 搜广推与 LLM 应用 Alibaba Group / Tmall 2026-07-14 只建模兴趣无法解释“便宜多少”对购买的影响。DANet 的 IPN 捕获一般兴趣；DPN 对 400 天 discount-rate 序列做 FFT 滤波和高低频分解，DCM-User 从相似购买中抽取折扣偏好，DCM-Context 用促销周期 gate 修正分布，并以购买样本的真实折扣做辅助回归。 Fidelity: 核心机制复现。参照作者开源代码执行 IPN、FFT/IFFT、DCM-User、DCM-Context 与折扣回归辅助任务。未使用 Tmall 私有 400 天折扣和促销特征；明确区分作者 TensorFlow 代码与本地 NumPy 复现。本地对照口径：基线是 IPN interest score；实验组 DANet 加入折扣代理的 TFTM/DCM，Hit@10 +0.00%、NDCG@10 -1.46%，fresh Hit@10 +50.00%。  ranking cvr discount 搜广推 学习信号、多任务与反馈偏差 DANet为什么把折扣历史分成高低频，而不只给模型一个当前折扣率？ 相同折扣对不同用户的吸引力不同，当前数值无法表达长期价格敏感度及短期促销反应。DPN从折扣序列中分离较稳定模式与快速波动，再结合相似购买和促销上下文调节偏好；兴趣网络负责另一路需求。购买样本的折扣辅助监督补充信息，但不能由关联直接推出降价因果效应。 示意：有人只在年度大促采购，有人日常也追逐小幅优惠；今天同为八折，两人的历史周期和近期反应不同，模型不应给出完全相同的折扣增益。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:danet" data-paper-title="Cheaper is Better: A Discount-Aware Network for Conversion Rate Prediction in E-commerce Recommendation System" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Cheaper is Better: A Discount-Aware Network for Conversion Rate Prediction in E-commerce Recommendation System 搜广推与 LLM 应用 Alibaba Group / Tmall 2026-07-14 只建模兴趣无法解释“便宜多少”对购买的影响。DANet 的 IPN 捕获一般兴趣；DPN 对 400 天 discount-rate 序列做 FFT 滤波和高低频分解，DCM-User 从相似购买中抽取折扣偏好，DCM-Context 用促销周期 gate 修正分布，并以购买样本的真实折扣做辅助回归。 Fidelity: 核心机制复现。参照作者开源代码执行 IPN、FFT/IFFT、DCM-User、DCM-Context 与折扣回归辅助任务。未使用 Tmall 私有 400 天折扣和促销特征；明确区分作者 TensorFlow 代码与本地 NumPy 复现。本地对照口径：基线是 IPN interest score；实验组 DANet 加入折扣代理的 TFTM/DCM，Hit@10 +0.00%、NDCG@10 -1.46%，fresh Hit@10 +50.00%。  ranking cvr discount 搜广推 学习信号、多任务与反馈偏差 DANet 的 FFT 高频、低频分解与简单最近折扣平均，相比多保留什么结构？ 均值把波动与周期压成一个数，频域分解将长期趋势和快速变化分开，让模型识别促销节奏。它也依赖时间采样与序列质量，不保证每种高频都是真实兴趣，噪声也会形成高频。公开数据无价格时，该机制只接受代理诊断。 示意：长期九折偶尔五折，与每周在八折十折间摆动，平均可能相近，频率结构却不同，用户对突发大促和规律折扣的反应也可能不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-9a3d1093600eb1bc">DANet 的 FFT 高频、低频分解与简单最近折扣平均，相比多保留什么结构？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adanet">Cheaper is Better: A Discount-Aware Network for Conversion Rate Prediction in E-commerce Recommendation System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group / Tmall</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>均值把波动与周期压成一个数，频域分解将长期趋势和快速变化分开，让模型识别促销节奏。它也依赖时间采样与序列质量，不保证每种高频都是真实兴趣，噪声也会形成高频。公开数据无价格时，该机制只接受代理诊断。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>长期九折偶尔五折，与每周在八折十折间摆动，平均可能相近，频率结构却不同，用户对突发大促和规律折扣的反应也可能不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12578">原论文</a> · <a href="../../../../reproductions/2607.12578-danet/">实现解读</a> · <a href="#qa-9a3d1093600eb1bc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:danet" data-paper-title="Cheaper is Better: A Discount-Aware Network for Conversion Rate Prediction in E-commerce Recommendation System" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Cheaper is Better: A Discount-Aware Network for Conversion Rate Prediction in E-commerce Recommendation System 搜广推与 LLM 应用 Alibaba Group / Tmall 2026-07-14 只建模兴趣无法解释“便宜多少”对购买的影响。DANet 的 IPN 捕获一般兴趣；DPN 对 400 天 discount-rate 序列做 FFT 滤波和高低频分解，DCM-User 从相似购买中抽取折扣偏好，DCM-Context 用促销周期 gate 修正分布，并以购买样本的真实折扣做辅助回归。 Fidelity: 核心机制复现。参照作者开源代码执行 IPN、FFT/IFFT、DCM-User、DCM-Context 与折扣回归辅助任务。未使用 Tmall 私有 400 天折扣和促销特征；明确区分作者 TensorFlow 代码与本地 NumPy 复现。本地对照口径：基线是 IPN interest score；实验组 DANet 加入折扣代理的 TFTM/DCM，Hit@10 +0.00%、NDCG@10 -1.46%，fresh Hit@10 +50.00%。  ranking cvr discount 搜广推 学习信号、多任务与反馈偏差 DANet 为什么只在购买样本上计算真实折扣辅助回归？ 该辅助目标对应已购买条件下观察到的折扣，未购买样本没有同义的成交折扣标签。按正样本指示 mask 避免编造监督；FFT 滤波后高频残差还应与低频重构相加回原序列。本地 popularity/rating intensity 只是代理，不得称真实券价回归。 示意：用户没买的鞋没有实际成交折扣，不能随手填零去训练；已买鞋的折扣才用于该目标，另用点击或排序损失学习总体行为。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-55f9897e4488e735">DANet 为什么只在购买样本上计算真实折扣辅助回归？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adanet">Cheaper is Better: A Discount-Aware Network for Conversion Rate Prediction in E-commerce Recommendation System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group / Tmall</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>该辅助目标对应已购买条件下观察到的折扣，未购买样本没有同义的成交折扣标签。按正样本指示 mask 避免编造监督；FFT 滤波后高频残差还应与低频重构相加回原序列。本地 popularity/rating intensity 只是代理，不得称真实券价回归。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户没买的鞋没有实际成交折扣，不能随手填零去训练；已买鞋的折扣才用于该目标，另用点击或排序损失学习总体行为。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12578">原论文</a> · <a href="../../../../reproductions/2607.12578-danet/">实现解读</a> · <a href="#qa-55f9897e4488e735">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:scalr" data-paper-title="Synthetic Data from Cross-Domain Events for Large-Scale Recommendation Systems" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Synthetic Data from Cross-Domain Events for Large-Scale Recommendation Systems 搜广推与 LLM 应用 Meta 2026-05-29 目标域 conversion 极稀疏，而同一用户在其他产品 surface 上有丰富行为。传统 cross-domain recommendation 把迁移逻辑耦合进模型参数；SCALR 先把 source event 翻译成目标域格式的 synthetic user-item event，再让任何下游模型像读取普通目标域数据一样训练。随机采样保留概率分布和 catalog 多样性，避免 top-k 反复生成少数头部 item。 Fidelity: 核心机制复现。本地从重叠用户估计跨域 item translation distribution，真实生成随机采样与 deterministic top-k 两套 synthetic events，再用相同下游协议比较。本地 genre 不是 Meta 的跨产品 surface，也没有 conversion label、隐私管线或多源生产生成服务。结果只验证概率翻译、随机生成和分布覆盖机制，不能外推论文线上 CVR。本地对照口径：基线为相同 source events、相同每事件生成预算的 deterministic top-k translation，实验组改为 SCALR 概率采样；  cross-domain synthetic-data sampling conversion data-augmentation 搜广推 学习信号、多任务与反馈偏差 SCALR翻译出的target事件，表示用户真的在目标域发生过该行为吗？ 不表示。它根据源域事件与条件分布采样出合成目标域训练记录，目的是让下游模型获得可使用的迁移数据。必须保留合成身份与权重，不能把这些记录混写成真实曝光、点击或转化日志；统计迁移不等于观测事实。 教学例子：源域看过甲后，系统合成目标域乙的训练事件；这不是在审计日志中声称该用户真的点击过乙。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-scalr-f567c58a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c660befc3863b6da">SCALR翻译出的target事件，表示用户真的在目标域发生过该行为吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ascalr">Synthetic Data from Cross-Domain Events for Large-Scale Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不表示。它根据源域事件与条件分布采样出合成目标域训练记录，目的是让下游模型获得可使用的迁移数据。必须保留合成身份与权重，不能把这些记录混写成真实曝光、点击或转化日志；统计迁移不等于观测事实。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>源域看过甲后，系统合成目标域乙的训练事件；这不是在审计日志中声称该用户真的点击过乙。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.00282">原论文</a> · <a href="../../../../reproductions/2606.00282-scalr/">实现解读</a> · <a href="#qa-c660befc3863b6da">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:scalr" data-paper-title="Synthetic Data from Cross-Domain Events for Large-Scale Recommendation Systems" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Synthetic Data from Cross-Domain Events for Large-Scale Recommendation Systems 搜广推与 LLM 应用 Meta 2026-05-29 目标域 conversion 极稀疏，而同一用户在其他产品 surface 上有丰富行为。传统 cross-domain recommendation 把迁移逻辑耦合进模型参数；SCALR 先把 source event 翻译成目标域格式的 synthetic user-item event，再让任何下游模型像读取普通目标域数据一样训练。随机采样保留概率分布和 catalog 多样性，避免 top-k 反复生成少数头部 item。 Fidelity: 核心机制复现。本地从重叠用户估计跨域 item translation distribution，真实生成随机采样与 deterministic top-k 两套 synthetic events，再用相同下游协议比较。本地 genre 不是 Meta 的跨产品 surface，也没有 conversion label、隐私管线或多源生产生成服务。结果只验证概率翻译、随机生成和分布覆盖机制，不能外推论文线上 CVR。本地对照口径：基线为相同 source events、相同每事件生成预算的 deterministic top-k translation，实验组改为 SCALR 概率采样；  cross-domain synthetic-data sampling conversion data-augmentation 搜广推 学习信号、多任务与反馈偏差 SCALR 为什么把跨域迁移变成合成事件，并随机采样目标物品而不是总取 top-k？ 迁移逻辑若写进特定网络，换模型就要重做。SCALR 根据重叠用户估计源事件到目标物品的条件分布，再采样合成目标域事件，供不同下游模型像普通数据一样训练。随机采样保留分布中的长尾机会，避免确定性 top-k 反复复制头部；但合成事件仍是统计迁移，不能冒充实际发生的用户行为。 示意：源域一次旅行浏览对应多个可能的目标域商品。总取最高概率会反复生成行李箱；按分布采样还可能生成转接头或旅行收纳，使训练数据保留更多可能需求。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:scalr" data-paper-title="Synthetic Data from Cross-Domain Events for Large-Scale Recommendation Systems" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Synthetic Data from Cross-Domain Events for Large-Scale Recommendation Systems 搜广推与 LLM 应用 Meta 2026-05-29 目标域 conversion 极稀疏，而同一用户在其他产品 surface 上有丰富行为。传统 cross-domain recommendation 把迁移逻辑耦合进模型参数；SCALR 先把 source event 翻译成目标域格式的 synthetic user-item event，再让任何下游模型像读取普通目标域数据一样训练。随机采样保留概率分布和 catalog 多样性，避免 top-k 反复生成少数头部 item。 Fidelity: 核心机制复现。本地从重叠用户估计跨域 item translation distribution，真实生成随机采样与 deterministic top-k 两套 synthetic events，再用相同下游协议比较。本地 genre 不是 Meta 的跨产品 surface，也没有 conversion label、隐私管线或多源生产生成服务。结果只验证概率翻译、随机生成和分布覆盖机制，不能外推论文线上 CVR。本地对照口径：基线为相同 source events、相同每事件生成预算的 deterministic top-k translation，实验组改为 SCALR 概率采样；  cross-domain synthetic-data sampling conversion data-augmentation 搜广推 学习信号、多任务与反馈偏差 SCALR的数据层迁移，与为每个下游模型分别加跨域网络模块有什么不同？ 数据层方案先把迁移结果写成目标格式事件，下游可沿普通数据接口训练；模型层方案把跨域逻辑绑定到特定结构。前者便于复用，却仍受合成分布质量限制，不能因接口统一就认定对所有排序器效果相同。 教学例子：同一批合成事件可交给不同目标模型；若迁移只存在于某种专用注意力层，换模型就需重新接入。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-87ad21447ca81b7c">SCALR的数据层迁移，与为每个下游模型分别加跨域网络模块有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ascalr">Synthetic Data from Cross-Domain Events for Large-Scale Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>数据层方案先把迁移结果写成目标格式事件，下游可沿普通数据接口训练；模型层方案把跨域逻辑绑定到特定结构。前者便于复用，却仍受合成分布质量限制，不能因接口统一就认定对所有排序器效果相同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一批合成事件可交给不同目标模型；若迁移只存在于某种专用注意力层，换模型就需重新接入。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.00282">原论文</a> · <a href="../../../../reproductions/2606.00282-scalr/">实现解读</a> · <a href="#qa-87ad21447ca81b7c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:scalr" data-paper-title="Synthetic Data from Cross-Domain Events for Large-Scale Recommendation Systems" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Synthetic Data from Cross-Domain Events for Large-Scale Recommendation Systems 搜广推与 LLM 应用 Meta 2026-05-29 目标域 conversion 极稀疏，而同一用户在其他产品 surface 上有丰富行为。传统 cross-domain recommendation 把迁移逻辑耦合进模型参数；SCALR 先把 source event 翻译成目标域格式的 synthetic user-item event，再让任何下游模型像读取普通目标域数据一样训练。随机采样保留概率分布和 catalog 多样性，避免 top-k 反复生成少数头部 item。 Fidelity: 核心机制复现。本地从重叠用户估计跨域 item translation distribution，真实生成随机采样与 deterministic top-k 两套 synthetic events，再用相同下游协议比较。本地 genre 不是 Meta 的跨产品 surface，也没有 conversion label、隐私管线或多源生产生成服务。结果只验证概率翻译、随机生成和分布覆盖机制，不能外推论文线上 CVR。本地对照口径：基线为相同 source events、相同每事件生成预算的 deterministic top-k translation，实验组改为 SCALR 概率采样；  cross-domain synthetic-data sampling conversion data-augmentation 搜广推 学习信号、多任务与反馈偏差 SCALR估计P(target|source)需要怎样的数据隔离？ 基于训练重叠用户共现，不用测试目标事件估转换表；零分母及无覆盖需处理。当前genre代理不是Meta跨产品或真实conversion，不能报告线上CVR。 例如先读测试购买再估翻译概率，会让合成事件暗含未来答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-757eb29377c39af1">SCALR估计P(target|source)需要怎样的数据隔离？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ascalr">Synthetic Data from Cross-Domain Events for Large-Scale Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>基于训练重叠用户共现，不用测试目标事件估转换表；零分母及无覆盖需处理。当前genre代理不是Meta跨产品或真实conversion，不能报告线上CVR。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先读测试购买再估翻译概率，会让合成事件暗含未来答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.00282">原论文</a> · <a href="../../../../reproductions/2606.00282-scalr/">实现解读</a> · <a href="#qa-757eb29377c39af1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:causal-representation" data-paper-title="Causal Representation Learning for Generalisable Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Causal Representation Learning for Generalisable Recommendation 搜广推与 LLM 应用 University of Warwick 2026-05-26 通过信息论去混杂约束，让候选表征保留与结果有关的因果成分、丢弃由曝光策略带来的非因果成分；训练后不增加线上推理开销。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05220，相对变化 -3.35%。本地代理目标与论文生产任务不同，不能外推线上 lift。  causal-recommendation distribution-shift representation-learning 搜广推 学习信号、多任务与反馈偏差 Causal Representation 为什么同时要求保留结果信息与抑制混杂信息？ 只抑制曝光策略相关信息可能连有用偏好一起删掉，表示便失去预测能力；只保留结果信息又可能走曝光捷径。条件结果信息与混杂惩罚形成双重目标，意在保留可泛化成分。信息论约束本身不建立因果识别，变量选择与数据假设仍决定解释。 示意：热门度既影响曝光也与点击相关，全部删掉可能损失需求信号，全部保留又会复制旧策略；训练需要在两者之间明确约束。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-causal-representation-dd23e0e4" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-003a7305ed9c5c96">Causal Representation 为什么同时要求保留结果信息与抑制混杂信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acausal-representation">Causal Representation Learning for Generalisable Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Warwick</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只抑制曝光策略相关信息可能连有用偏好一起删掉，表示便失去预测能力；只保留结果信息又可能走曝光捷径。条件结果信息与混杂惩罚形成双重目标，意在保留可泛化成分。信息论约束本身不建立因果识别，变量选择与数据假设仍决定解释。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>热门度既影响曝光也与点击相关，全部删掉可能损失需求信号，全部保留又会复制旧策略；训练需要在两者之间明确约束。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.27043">原论文</a> · <a href="../../../../reproductions/2605.27043-causal-representation/">实现解读</a> · <a href="#qa-003a7305ed9c5c96">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:causal-representation" data-paper-title="Causal Representation Learning for Generalisable Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Causal Representation Learning for Generalisable Recommendation 搜广推与 LLM 应用 University of Warwick 2026-05-26 通过信息论去混杂约束，让候选表征保留与结果有关的因果成分、丢弃由曝光策略带来的非因果成分；训练后不增加线上推理开销。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05220，相对变化 -3.35%。本地代理目标与论文生产任务不同，不能外推线上 lift。  causal-recommendation distribution-shift representation-learning 搜广推 学习信号、多任务与反馈偏差 去掉所有与曝光策略相关的信息，为什么不一定能得到好的因果推荐表征？ 有些信息同时关联曝光与真实结果，完全删除可能连有用信号一起丢掉。方法以信息论目标平衡给定混杂条件后的结果信息和对曝光机制的依赖，争取保留可迁移成分。这里的因果解释依赖混杂变量与识别假设；只看到分布迁移下指标变化，并不足以证明所有非因果成分已被清除。 示意：地域既影响内容曝光，也影响配送可达性，不能因为它关联曝光就一刀切删除；要区分仅反映投放偏好的部分和确实影响结果的部分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:causal-representation" data-paper-title="Causal Representation Learning for Generalisable Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Causal Representation Learning for Generalisable Recommendation 搜广推与 LLM 应用 University of Warwick 2026-05-26 通过信息论去混杂约束，让候选表征保留与结果有关的因果成分、丢弃由曝光策略带来的非因果成分；训练后不增加线上推理开销。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05220，相对变化 -3.35%。本地代理目标与论文生产任务不同，不能外推线上 lift。  causal-recommendation distribution-shift representation-learning 搜广推 学习信号、多任务与反馈偏差 因果表示约束与直接使用 IPS 权重，主要作用点有何不同？ 表示约束改变模型编码哪些信息，IPS 改变已有样本对损失的贡献，两者并非同一操作。前者依赖混杂表示与信息估计，后者依赖倾向概率与支持条件。机制对比只能说明偏差处理位置不同，不能从来源代理结果推断哪种方案普遍更优。 示意：给罕见曝光样本加权没有禁止网络读取热门度；相反，约束表示少记热门度也没有自动补上未曝光样本，两种方法解决不同层面。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4f562272774bfd8f">因果表示约束与直接使用 IPS 权重，主要作用点有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acausal-representation">Causal Representation Learning for Generalisable Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Warwick</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>表示约束改变模型编码哪些信息，IPS 改变已有样本对损失的贡献，两者并非同一操作。前者依赖混杂表示与信息估计，后者依赖倾向概率与支持条件。机制对比只能说明偏差处理位置不同，不能从来源代理结果推断哪种方案普遍更优。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>给罕见曝光样本加权没有禁止网络读取热门度；相反，约束表示少记热门度也没有自动补上未曝光样本，两种方法解决不同层面。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.27043">原论文</a> · <a href="../../../../reproductions/2605.27043-causal-representation/">实现解读</a> · <a href="#qa-4f562272774bfd8f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:causal-representation" data-paper-title="Causal Representation Learning for Generalisable Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Causal Representation Learning for Generalisable Recommendation 搜广推与 LLM 应用 University of Warwick 2026-05-26 通过信息论去混杂约束，让候选表征保留与结果有关的因果成分、丢弃由曝光策略带来的非因果成分；训练后不增加线上推理开销。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05220，相对变化 -3.35%。本地代理目标与论文生产任务不同，不能外推线上 lift。  causal-recommendation distribution-shift representation-learning 搜广推 学习信号、多任务与反馈偏差 实现 I(g(T);Y|Z)−λI(g(T);Z) 时，怎样避免把目标标签当成上线输入？ Y 与 Z 可参与训练目标和估计器，部署表示仍须只由预测时可用的 T 计算。条件信息用于约束学习，不意味着推理需要读取结果。来源称训练后不增加服务开销，本地公开代理也不能据此证明真实因果成分已分离。 示意：训练用点击标签教表示保留相关信息，上线未发生点击时仍能计算 g(T)；若把该次真实点击拼进输入，就变成答案泄漏。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-dcd516fbb0b0b066">实现 I(g(T);Y|Z)−λI(g(T);Z) 时，怎样避免把目标标签当成上线输入？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acausal-representation">Causal Representation Learning for Generalisable Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Warwick</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Y 与 Z 可参与训练目标和估计器，部署表示仍须只由预测时可用的 T 计算。条件信息用于约束学习，不意味着推理需要读取结果。来源称训练后不增加服务开销，本地公开代理也不能据此证明真实因果成分已分离。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练用点击标签教表示保留相关信息，上线未发生点击时仍能计算 g(T)；若把该次真实点击拼进输入，就变成答案泄漏。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.27043">原论文</a> · <a href="../../../../reproductions/2605.27043-causal-representation/">实现解读</a> · <a href="#qa-dcd516fbb0b0b066">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pearl-percentile" data-paper-title="PEARL: Unbiased Percentile Estimation via Contrastive Learning for Industrial-Scale Livestream Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="PEARL: Unbiased Percentile Estimation via Contrastive Learning for Industrial-Scale Livestream Recommendation 搜广推与 LLM 应用 TikTok 2026-05-20 用多次对比而不是单个偏置标签估计行为 percentile，并按价值加权、bootstrap 和长期共训练扩展到多个排序目标。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  ranking contrastive-learning debiasing 搜广推 学习信号、多任务与反馈偏差 PEARL 的 percentile 为什么必须说明相对于哪份参考分布？ percentile 是行为超过参考样本的比例，换参考用户、场景或窗口会改变其含义，不能当固定绝对价值。多比较可降低采样波动，价值权重再连接目标。相对排名不自动消除日志偏差，也不能凭分位高就解释为因果增量。 示意：三十秒观看在短视频群体很高、长教程群体很低；若参考集合混错，给同一个行为的分位会产生相反解释。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-pearl-percentile-dbf6d244" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-60a85dba32ab471e">PEARL 的 percentile 为什么必须说明相对于哪份参考分布？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apearl-percentile">PEARL: Unbiased Percentile Estimation via Contrastive Learning for Industrial-Scale Livestream Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · TikTok</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>percentile 是行为超过参考样本的比例，换参考用户、场景或窗口会改变其含义，不能当固定绝对价值。多比较可降低采样波动，价值权重再连接目标。相对排名不自动消除日志偏差，也不能凭分位高就解释为因果增量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三十秒观看在短视频群体很高、长教程群体很低；若参考集合混错，给同一个行为的分位会产生相反解释。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.21752">原论文</a> · <a href="../../../../reproductions/2605.21752-pearl-percentile/">实现解读</a> · <a href="#qa-60a85dba32ab471e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pearl-percentile" data-paper-title="PEARL: Unbiased Percentile Estimation via Contrastive Learning for Industrial-Scale Livestream Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="PEARL: Unbiased Percentile Estimation via Contrastive Learning for Industrial-Scale Livestream Recommendation 搜广推与 LLM 应用 TikTok 2026-05-20 用多次对比而不是单个偏置标签估计行为 percentile，并按价值加权、bootstrap 和长期共训练扩展到多个排序目标。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  ranking contrastive-learning debiasing 搜广推 学习信号、多任务与反馈偏差 PEARL 为什么用多次行为对比估计 percentile，而不直接回归原始行为值？ 原始行为值受尺度和偏置影响，不同目标或样本未必可直接比较。把一个行为与多次参考行为比较，可估计它在参考分布中的相对位置；比较次数增加时估计方差下降。价值加权与长期共训练再连接业务目标，但 percentile 仍依赖参考分布，不能把相对排名误当作去除了所有因果偏差的价值。 示意：同样观看三十秒，对十五秒视频和十分钟视频含义不同。与合适参考行为反复比较后，可分别得到在各自分布中的位置；参考群体选错，相对位置仍会误导。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pearl-percentile" data-paper-title="PEARL: Unbiased Percentile Estimation via Contrastive Learning for Industrial-Scale Livestream Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="PEARL: Unbiased Percentile Estimation via Contrastive Learning for Industrial-Scale Livestream Recommendation 搜广推与 LLM 应用 TikTok 2026-05-20 用多次对比而不是单个偏置标签估计行为 percentile，并按价值加权、bootstrap 和长期共训练扩展到多个排序目标。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  ranking contrastive-learning debiasing 搜广推 学习信号、多任务与反馈偏差 多次成对比较与一次原始标签回归，对尺度与方差的取舍是什么？ 原始回归保留量纲但受极值影响，比较估计相对位置更容易跨尺度组织，却会丢绝对差距并增加采样误差。N 增加时方差在相应独立假设下下降，bootstrap 也不修复系统偏差。机制对比不能证明分位必然胜过原标签。 示意：观看一百秒与一百零一秒可能排名不同但价值差很小，分位不直接表达这一秒幅度；反过来巨大异常时长也不再线性支配目标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e8375492d01fdaa2">多次成对比较与一次原始标签回归，对尺度与方差的取舍是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apearl-percentile">PEARL: Unbiased Percentile Estimation via Contrastive Learning for Industrial-Scale Livestream Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · TikTok</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原始回归保留量纲但受极值影响，比较估计相对位置更容易跨尺度组织，却会丢绝对差距并增加采样误差。N 增加时方差在相应独立假设下下降，bootstrap 也不修复系统偏差。机制对比不能证明分位必然胜过原标签。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>观看一百秒与一百零一秒可能排名不同但价值差很小，分位不直接表达这一秒幅度；反过来巨大异常时长也不再线性支配目标。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.21752">原论文</a> · <a href="../../../../reproductions/2605.21752-pearl-percentile/">实现解读</a> · <a href="#qa-e8375492d01fdaa2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pearl-percentile" data-paper-title="PEARL: Unbiased Percentile Estimation via Contrastive Learning for Industrial-Scale Livestream Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="PEARL: Unbiased Percentile Estimation via Contrastive Learning for Industrial-Scale Livestream Recommendation 搜广推与 LLM 应用 TikTok 2026-05-20 用多次对比而不是单个偏置标签估计行为 percentile，并按价值加权、bootstrap 和长期共训练扩展到多个排序目标。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  ranking contrastive-learning debiasing 搜广推 学习信号、多任务与反馈偏差 PEARL 用 p(1−p)/N 解释方差时，为什么要检查比较样本相关性？ 该形式依赖相应伯努利比较和采样条件，重复同一参考或强相关样本不会提供 N 份独立信息。权重、bootstrap 与长期共训的来源也应记录，不能把理论采样方差当模型训练方差。测试参考数据不得反向用于选目标。 示意：把同一视频重复比较一百次，不能当作一百个独立参考使不确定性缩小十倍；数据条数增加但信息并未同量增加。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b544a9feebc5aa13">PEARL 用 p(1−p)/N 解释方差时，为什么要检查比较样本相关性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apearl-percentile">PEARL: Unbiased Percentile Estimation via Contrastive Learning for Industrial-Scale Livestream Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · TikTok</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>该形式依赖相应伯努利比较和采样条件，重复同一参考或强相关样本不会提供 N 份独立信息。权重、bootstrap 与长期共训的来源也应记录，不能把理论采样方差当模型训练方差。测试参考数据不得反向用于选目标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把同一视频重复比较一百次，不能当作一百个独立参考使不确定性缩小十倍；数据条数增加但信息并未同量增加。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.21752">原论文</a> · <a href="../../../../reproductions/2605.21752-pearl-percentile/">实现解读</a> · <a href="#qa-b544a9feebc5aa13">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dadf" data-paper-title="DADF: A Distribution-Aware Debiasing Framework for Watch-Time Regression in Recommender Systems" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="DADF: A Distribution-Aware Debiasing Framework for Watch-Time Regression in Recommender Systems 搜广推与 LLM 应用 Kuaishou Technology 2026-05-18 冻结成熟的第一阶段 watch-time 模型，按条件分布学习乘性残差校正，并保持线上标量接口不变。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  ranking watch-time debiasing 搜广推 学习信号、多任务与反馈偏差 DADF 为什么把成熟预测器看作基准，再学习相对校正？ 成熟模型已经包含大量稳定关系，直接重训整套网络风险与成本更高。乘性校正让新模块专注基准在不同条件下的系统误差，并继续输出相同标量接口。它依赖基准可提供有用结构，若基础预测接近零或严重失效，校正也更困难。 示意：原模型对某类长视频总低估一成，可学条件因子修正；无需先推倒它已学好的所有用户与内容关系，但不能假设一个因子能补回缺失信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-dadf-696311de" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4ed21b3ed0463b49">DADF 为什么把成熟预测器看作基准，再学习相对校正？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adadf">DADF: A Distribution-Aware Debiasing Framework for Watch-Time Regression in Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>成熟模型已经包含大量稳定关系，直接重训整套网络风险与成本更高。乘性校正让新模块专注基准在不同条件下的系统误差，并继续输出相同标量接口。它依赖基准可提供有用结构，若基础预测接近零或严重失效，校正也更困难。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>原模型对某类长视频总低估一成，可学条件因子修正；无需先推倒它已学好的所有用户与内容关系，但不能假设一个因子能补回缺失信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.17863">原论文</a> · <a href="../../../../reproductions/2605.17863-dadf/">实现解读</a> · <a href="#qa-4ed21b3ed0463b49">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dadf" data-paper-title="DADF: A Distribution-Aware Debiasing Framework for Watch-Time Regression in Recommender Systems" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="DADF: A Distribution-Aware Debiasing Framework for Watch-Time Regression in Recommender Systems 搜广推与 LLM 应用 Kuaishou Technology 2026-05-18 冻结成熟的第一阶段 watch-time 模型，按条件分布学习乘性残差校正，并保持线上标量接口不变。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  ranking watch-time debiasing 搜广推 学习信号、多任务与反馈偏差 DADF为什么冻结成熟第一阶段模型，只学习乘性校正因子？ 已有模型包含稳定预测能力，全部重训既可能损坏旧知识，又会改变线上接口。DADF用条件分布信息学习残差比例，让校正随输入及初始预测变化，而仍输出同一种标量。乘性修正适合相对误差，但极小初始预测会使比例不稳定，因此分母保护与条件分布校正不可忽略。 示意：两类用户都被预测看10秒，一类长期被低估、另一类高估；校正器可分别乘上不同系数，而不是给所有用户统一加五秒或重建整套模型。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dadf" data-paper-title="DADF: A Distribution-Aware Debiasing Framework for Watch-Time Regression in Recommender Systems" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="DADF: A Distribution-Aware Debiasing Framework for Watch-Time Regression in Recommender Systems 搜广推与 LLM 应用 Kuaishou Technology 2026-05-18 冻结成熟的第一阶段 watch-time 模型，按条件分布学习乘性残差校正，并保持线上标量接口不变。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  ranking watch-time debiasing 搜广推 学习信号、多任务与反馈偏差 DADF 的乘性残差与加性残差，对预测尺度的作用有何不同？ 乘性校正表达相对比例误差，大预测可得到较大绝对调整，小预测调整较小；加性表达固定单位差。两者适合的误差形态不同，分布条件决定是否应使用比例。来源本地排序零变化，也说明数值校正不一定改变候选次序，不能自动写成推荐提升。 示意：十秒和一百秒预测都低估百分之十，乘性更自然；若都少了五秒则加性更贴切。只是整体乘同一常数时，排序可能完全不变。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-03765f3ee2f1d912">DADF 的乘性残差与加性残差，对预测尺度的作用有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adadf">DADF: A Distribution-Aware Debiasing Framework for Watch-Time Regression in Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>乘性校正表达相对比例误差，大预测可得到较大绝对调整，小预测调整较小；加性表达固定单位差。两者适合的误差形态不同，分布条件决定是否应使用比例。来源本地排序零变化，也说明数值校正不一定改变候选次序，不能自动写成推荐提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>十秒和一百秒预测都低估百分之十，乘性更自然；若都少了五秒则加性更贴切。只是整体乘同一常数时，排序可能完全不变。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.17863">原论文</a> · <a href="../../../../reproductions/2605.17863-dadf/">实现解读</a> · <a href="#qa-03765f3ee2f1d912">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dadf" data-paper-title="DADF: A Distribution-Aware Debiasing Framework for Watch-Time Regression in Recommender Systems" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="DADF: A Distribution-Aware Debiasing Framework for Watch-Time Regression in Recommender Systems 搜广推与 LLM 应用 Kuaishou Technology 2026-05-18 冻结成熟的第一阶段 watch-time 模型，按条件分布学习乘性残差校正，并保持线上标量接口不变。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  ranking watch-time debiasing 搜广推 学习信号、多任务与反馈偏差 DADF 学 y/max(y0,ε) 时，为什么冻结 y0 仍要检查小分母？ 冻结基准可稳定训练目标，但基准很小时比值仍可能巨大并放大噪声，epsilon 改变边界行为需明确记录。校正器输入、比值监督与输出乘法要使用同一基准版本；不能在训练中偷偷更新基础模型，再声称只学第二阶段。 示意：基准只预测零点零一秒而观察十秒，比值会非常大；应检查这类样本与数值设定，而不是把异常大因子理解为可靠学习到的偏好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ea006a6d3351f5f2">DADF 学 y/max(y0,ε) 时，为什么冻结 y0 仍要检查小分母？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adadf">DADF: A Distribution-Aware Debiasing Framework for Watch-Time Regression in Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冻结基准可稳定训练目标，但基准很小时比值仍可能巨大并放大噪声，epsilon 改变边界行为需明确记录。校正器输入、比值监督与输出乘法要使用同一基准版本；不能在训练中偷偷更新基础模型，再声称只学第二阶段。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>基准只预测零点零一秒而观察十秒，比值会非常大；应检查这类样本与数值设定，而不是把异常大因子理解为可靠学习到的偏好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.17863">原论文</a> · <a href="../../../../reproductions/2605.17863-dadf/">实现解读</a> · <a href="#qa-ea006a6d3351f5f2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ektm" data-paper-title="Effective Knowledge Transfer for Multi-Task Recommendation Models" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Effective Knowledge Transfer for Multi-Task Recommendation Models 搜广推与 LLM 应用 Huawei Technologies 2026-05-07 让 CTR 表示按 CVR 任务相似度向多个转化塔迁移，并以难例感知损失抑制负迁移，保持多任务部署成本可控。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 ektm 核心机制，相对 NDCG@10 +10.98%。  multi-task-learning knowledge-transfer conversion 搜广推 学习信号、多任务与反馈偏差 EKTM 为什么从 CTR 向多个 CVR 任务迁移，而不让它们从零学习？ 点击信号相对丰富，可为稀疏转化提供基本兴趣与相关性，但不同转化任务并不完全相同。任务相似度控制迁移量，难例感知损失限制负迁移。稠密数据是资源而非可靠教师的充分条件，仍需检查各目标是否受益。 示意：加购与购买可共享部分点击兴趣，退货目标则含不同含义；所有转化塔从零可能太稀疏，无差别接受 CTR 也可能带偏。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-ektm-e47d7330" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-37226c0f09f37dfc">EKTM 为什么从 CTR 向多个 CVR 任务迁移，而不让它们从零学习？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aektm">Effective Knowledge Transfer for Multi-Task Recommendation Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Technologies</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>点击信号相对丰富，可为稀疏转化提供基本兴趣与相关性，但不同转化任务并不完全相同。任务相似度控制迁移量，难例感知损失限制负迁移。稠密数据是资源而非可靠教师的充分条件，仍需检查各目标是否受益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>加购与购买可共享部分点击兴趣，退货目标则含不同含义；所有转化塔从零可能太稀疏，无差别接受 CTR 也可能带偏。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.05730">原论文</a> · <a href="../../../../reproductions/2605.05730-ektm/">实现解读</a> · <a href="#qa-37226c0f09f37dfc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ektm" data-paper-title="Effective Knowledge Transfer for Multi-Task Recommendation Models" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Effective Knowledge Transfer for Multi-Task Recommendation Models 搜广推与 LLM 应用 Huawei Technologies 2026-05-07 让 CTR 表示按 CVR 任务相似度向多个转化塔迁移，并以难例感知损失抑制负迁移，保持多任务部署成本可控。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 ektm 核心机制，相对 NDCG@10 +10.98%。  multi-task-learning knowledge-transfer conversion 搜广推 学习信号、多任务与反馈偏差 EKTM为什么按任务相似度迁移CTR表示，而不是让所有转化任务平等共享？ 点击监督较丰富，但不同转化目标与点击的关系不相同，平均共享可能把无关模式灌入稀疏任务。EKTM依据任务关系选择迁移强度，再关注难例以抑制负迁移；共性可被借用，各转化塔仍保留专门目标。相似度是需要学习和验证的信号，不能只因数据量大就把CTR当所有任务的可靠teacher。 示意：加购与点击关系较近，长期续费可能更依赖其他因素；同一份点击表示向两者迁移的力度不应相同，否则容易提高前者却损伤后者。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ektm" data-paper-title="Effective Knowledge Transfer for Multi-Task Recommendation Models" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Effective Knowledge Transfer for Multi-Task Recommendation Models 搜广推与 LLM 应用 Huawei Technologies 2026-05-07 让 CTR 表示按 CVR 任务相似度向多个转化塔迁移，并以难例感知损失抑制负迁移，保持多任务部署成本可控。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 ektm 核心机制，相对 NDCG@10 +10.98%。  multi-task-learning knowledge-transfer conversion 搜广推 学习信号、多任务与反馈偏差 EKTM 的相似度加权迁移与统一 shared-bottom，冲突控制发生在哪里？ shared-bottom 直接共享底座，EKTM 在转移表示时选择不同任务贡献，再用困难样本约束不合适共享。它增加有条件的分工，也依赖相似度估计和额外塔开销。机制差别并不保证普遍更优，电影代理排名也不能当真实转化率证明。 示意：购买塔可多吸收加购相关知识，另一个意图不同的塔少吸收；统一底座可能让它们都争同一表示，权重迁移则显式调节。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-2517233fca0a5f4d">EKTM 的相似度加权迁移与统一 shared-bottom，冲突控制发生在哪里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aektm">Effective Knowledge Transfer for Multi-Task Recommendation Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Technologies</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>shared-bottom 直接共享底座，EKTM 在转移表示时选择不同任务贡献，再用困难样本约束不合适共享。它增加有条件的分工，也依赖相似度估计和额外塔开销。机制差别并不保证普遍更优，电影代理排名也不能当真实转化率证明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>购买塔可多吸收加购相关知识，另一个意图不同的塔少吸收；统一底座可能让它们都争同一表示，权重迁移则显式调节。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.05730">原论文</a> · <a href="../../../../reproductions/2605.05730-ektm/">实现解读</a> · <a href="#qa-2517233fca0a5f4d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ektm" data-paper-title="Effective Knowledge Transfer for Multi-Task Recommendation Models" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Effective Knowledge Transfer for Multi-Task Recommendation Models 搜广推与 LLM 应用 Huawei Technologies 2026-05-07 让 CTR 表示按 CVR 任务相似度向多个转化塔迁移，并以难例感知损失抑制负迁移，保持多任务部署成本可控。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 ektm 核心机制，相对 NDCG@10 +10.98%。  multi-task-learning knowledge-transfer conversion 搜广推 学习信号、多任务与反馈偏差 EKTM 汇聚 fctr 与加权 CVR 表示时，为什么要检查任务身份而非仅形状？ 每个相似度权重对应特定源目标任务，向量须在可组合空间对齐后使用；任务顺序改变时映射也要一致。难例 mask 需要真实有效标签，不得从测试结果生成。本地公开代理不能把缺失的工业转化标签凭名义补全。 示意：表示“CTR 到购买”的权重若乘到收藏塔，张量仍能相加，学习语义却已错误；验收需核对每列具体代表哪个任务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a265bd597f40dca1">EKTM 汇聚 fctr 与加权 CVR 表示时，为什么要检查任务身份而非仅形状？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aektm">Effective Knowledge Transfer for Multi-Task Recommendation Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Technologies</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每个相似度权重对应特定源目标任务，向量须在可组合空间对齐后使用；任务顺序改变时映射也要一致。难例 mask 需要真实有效标签，不得从测试结果生成。本地公开代理不能把缺失的工业转化标签凭名义补全。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>表示“CTR 到购买”的权重若乘到收藏塔，张量仍能相加，学习语义却已错误；验收需核对每列具体代表哪个任务。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.05730">原论文</a> · <a href="../../../../reproductions/2605.05730-ektm/">实现解读</a> · <a href="#qa-a265bd597f40dca1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pa-bridge" data-paper-title="Bridging Passive and Active: Enhancing Conversation Starter Recommendation via Active Expression Modeling" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Bridging Passive and Active: Enhancing Conversation Starter Recommendation via Active Expression Modeling 搜广推与 LLM 应用 ByteDance 2026-05-07 用分布对齐器把被动浏览行为迁移到主动查询空间，再通过语义离散化和重加权削弱曝光反馈回路，改善 conversation starter 的覆盖与多样性。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04938，相对变化 -8.57%。本地代理目标与论文生产任务不同，不能外推线上 lift。  conversation-starter distribution-alignment debiasing 搜广推 学习信号、多任务与反馈偏差 PA-Bridge 的被动到主动迁移为什么不是简单将浏览标题改成问句？ 浏览反映看过的内容，主动 query 还包含行动与求解意图，两种分布不相同。对齐器先连接空间，再用离散语义和权重减弱曝光反馈回路。文字问号不能创造真正查询需求，模型推断也不等于用户明确表达。 示意：反复看健身视频可能只是娱乐，主动想问却是膝盖保护；把标题改成“如何健身？”不一定找到用户当前要解决的具体问题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-pa-bridge-6df7bc67" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9a068573604e1dba">PA-Bridge 的被动到主动迁移为什么不是简单将浏览标题改成问句？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apa-bridge">Bridging Passive and Active: Enhancing Conversation Starter Recommendation via Active Expression Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>浏览反映看过的内容，主动 query 还包含行动与求解意图，两种分布不相同。对齐器先连接空间，再用离散语义和权重减弱曝光反馈回路。文字问号不能创造真正查询需求，模型推断也不等于用户明确表达。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>反复看健身视频可能只是娱乐，主动想问却是膝盖保护；把标题改成“如何健身？”不一定找到用户当前要解决的具体问题。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.05855">原论文</a> · <a href="../../../../reproductions/2605.05855-pa-bridge/">实现解读</a> · <a href="#qa-9a068573604e1dba">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pa-bridge" data-paper-title="Bridging Passive and Active: Enhancing Conversation Starter Recommendation via Active Expression Modeling" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Bridging Passive and Active: Enhancing Conversation Starter Recommendation via Active Expression Modeling 搜广推与 LLM 应用 ByteDance 2026-05-07 用分布对齐器把被动浏览行为迁移到主动查询空间，再通过语义离散化和重加权削弱曝光反馈回路，改善 conversation starter 的覆盖与多样性。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04938，相对变化 -8.57%。本地代理目标与论文生产任务不同，不能外推线上 lift。  conversation-starter distribution-alignment debiasing 搜广推 学习信号、多任务与反馈偏差 PA-Bridge 为什么先把被动浏览对齐到主动查询空间，再做语义离散化和重加权？ 被动浏览反映“看过什么”，主动查询更接近“此刻想问什么”，直接复用浏览表示可能推荐熟悉却不适合发起对话的话题。分布对齐连接两种意图空间，离散语义单元和重加权再降低热门曝光反复主导训练的程度。目标是让起始问题更可探索，而不是把高曝光浏览内容原样改写成问题。 示意：用户常被动看到健身短视频，但真正想问的是“膝盖不适怎样调整训练”。对齐到查询空间后，再平衡热门话题权重，有机会提出更贴近行动需求的对话起点。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pa-bridge" data-paper-title="Bridging Passive and Active: Enhancing Conversation Starter Recommendation via Active Expression Modeling" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Bridging Passive and Active: Enhancing Conversation Starter Recommendation via Active Expression Modeling 搜广推与 LLM 应用 ByteDance 2026-05-07 用分布对齐器把被动浏览行为迁移到主动查询空间，再通过语义离散化和重加权削弱曝光反馈回路，改善 conversation starter 的覆盖与多样性。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04938，相对变化 -8.57%。本地代理目标与论文生产任务不同，不能外推线上 lift。  conversation-starter distribution-alignment debiasing 搜广推 学习信号、多任务与反馈偏差 PA-Bridge 重加权与直接取最高浏览频次话题，偏好覆盖如何不同？ 频次强受旧曝光影响，直接选最高会不断推荐已被系统推多的话题；重加权尝试减少热门语义单元支配，让主动入口更有覆盖。权重过强也会偏向无关冷门，不能将多样性自动当满意度或因果去偏。 示意：平台总曝光减脂内容，频次法继续只提减脂；权重可让同样相关但较少出现的力量训练进入，但不应随意推完全无关主题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-bb10a75c8320e802">PA-Bridge 重加权与直接取最高浏览频次话题，偏好覆盖如何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apa-bridge">Bridging Passive and Active: Enhancing Conversation Starter Recommendation via Active Expression Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>频次强受旧曝光影响，直接选最高会不断推荐已被系统推多的话题；重加权尝试减少热门语义单元支配，让主动入口更有覆盖。权重过强也会偏向无关冷门，不能将多样性自动当满意度或因果去偏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>平台总曝光减脂内容，频次法继续只提减脂；权重可让同样相关但较少出现的力量训练进入，但不应随意推完全无关主题。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.05855">原论文</a> · <a href="../../../../reproductions/2605.05855-pa-bridge/">实现解读</a> · <a href="#qa-bb10a75c8320e802">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pa-bridge" data-paper-title="Bridging Passive and Active: Enhancing Conversation Starter Recommendation via Active Expression Modeling" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Bridging Passive and Active: Enhancing Conversation Starter Recommendation via Active Expression Modeling 搜广推与 LLM 应用 ByteDance 2026-05-07 用分布对齐器把被动浏览行为迁移到主动查询空间，再通过语义离散化和重加权削弱曝光反馈回路，改善 conversation starter 的覆盖与多样性。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04938，相对变化 -8.57%。本地代理目标与论文生产任务不同，不能外推线上 lift。  conversation-starter distribution-alignment debiasing 搜广推 学习信号、多任务与反馈偏差 PA-Bridge 拟合 hpassive 到 hactive 对齐时，训练 pair 应有怎样的时间约束？ 主动查询可作为训练监督，预测当时的被动上下文必须截止查询前，不能包含查询后的点击来反推。离散码与样本权重也应来自允许历史。来源公开代理缺真实主动提问日志，不能仅凭一个 Align 函数就宣称完成跨行为迁移。 示意：用户提交膝盖保护问题后看的康复视频不能提前进入要预测该问题的浏览历史；否则对齐看似准确，其实使用了后续答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-4276e4fc92ccc22a">PA-Bridge 拟合 hpassive 到 hactive 对齐时，训练 pair 应有怎样的时间约束？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apa-bridge">Bridging Passive and Active: Enhancing Conversation Starter Recommendation via Active Expression Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>主动查询可作为训练监督，预测当时的被动上下文必须截止查询前，不能包含查询后的点击来反推。离散码与样本权重也应来自允许历史。来源公开代理缺真实主动提问日志，不能仅凭一个 Align 函数就宣称完成跨行为迁移。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户提交膝盖保护问题后看的康复视频不能提前进入要预测该问题的浏览历史；否则对齐看似准确，其实使用了后续答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.05855">原论文</a> · <a href="../../../../reproductions/2605.05855-pa-bridge/">实现解读</a> · <a href="#qa-4276e4fc92ccc22a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gpl-prerank" data-paper-title="Generative Pseudo-Labeling for Pre-Ranking with LLMs" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Generative Pseudo-Labeling for Pre-Ranking with LLMs 搜广推与 LLM 应用 Alibaba Group / Renmin University 2026-02-24 LLM 从用户行为生成兴趣锚点，为未曝光召回候选产生伪标签；预排序器联合真实与伪监督，且线上不调用 LLM。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 gpl-prerank 核心机制，相对 NDCG@10 +12.84%。  pre-ranking pseudo-labeling llm-recommendation 搜广推 学习信号、多任务与反馈偏差 GPL 为什么关注未曝光候选，而不是只扩大已曝光点击日志？ 预排面对的候选比最终曝光更广，只有曝光反馈会让训练覆盖偏窄。兴趣锚点与 LLM 为未曝光项提供弱监督，让模型学习更接近召回池的分布。伪标签是推断而非真实用户选择，不能取代全部观测反馈。 示意：召回一千件只展示十件，剩余没有点击标签却不必然差；伪标注可补一些相关性线索，但无法宣称这些商品实际得到过好反馈。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-gpl-prerank-737de503" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-3057b5a728b7bb76">GPL 为什么关注未曝光候选，而不是只扩大已曝光点击日志？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agpl-prerank">Generative Pseudo-Labeling for Pre-Ranking with LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group / Renmin University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>预排面对的候选比最终曝光更广，只有曝光反馈会让训练覆盖偏窄。兴趣锚点与 LLM 为未曝光项提供弱监督，让模型学习更接近召回池的分布。伪标签是推断而非真实用户选择，不能取代全部观测反馈。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>召回一千件只展示十件，剩余没有点击标签却不必然差；伪标注可补一些相关性线索，但无法宣称这些商品实际得到过好反馈。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.20995">原论文</a> · <a href="../../../../reproductions/2602.20995-gpl-prerank/">实现解读</a> · <a href="#qa-3057b5a728b7bb76">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gpl-prerank" data-paper-title="Generative Pseudo-Labeling for Pre-Ranking with LLMs" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Generative Pseudo-Labeling for Pre-Ranking with LLMs 搜广推与 LLM 应用 Alibaba Group / Renmin University 2026-02-24 LLM 从用户行为生成兴趣锚点，为未曝光召回候选产生伪标签；预排序器联合真实与伪监督，且线上不调用 LLM。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 gpl-prerank 核心机制，相对 NDCG@10 +12.84%。  pre-ranking pseudo-labeling llm-recommendation 搜广推 学习信号、多任务与反馈偏差 GPL预排序为什么给未曝光候选补伪标签，而不只对已曝光点击做监督？ 已曝光样本由旧系统筛选，预排器很少看见被早期淘汰候选的有效监督。LLM借用户兴趣锚点对这些候选产生补充标签，帮助模型覆盖旧日志的盲区，服务时仍使用轻量预排器。伪标签是带误差的外部判断，不是反事实真值，需要控制权重并检查它是否放大已有语义偏差。 示意：旧系统从未展示某类相关新品，因此没有点击记录；LLM可提供初步相关性判断来训练预排，但不能把这个判断写成用户已经喜欢或购买的事实。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gpl-prerank" data-paper-title="Generative Pseudo-Labeling for Pre-Ranking with LLMs" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Generative Pseudo-Labeling for Pre-Ranking with LLMs 搜广推与 LLM 应用 Alibaba Group / Renmin University 2026-02-24 LLM 从用户行为生成兴趣锚点，为未曝光召回候选产生伪标签；预排序器联合真实与伪监督，且线上不调用 LLM。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 gpl-prerank 核心机制，相对 NDCG@10 +12.84%。  pre-ranking pseudo-labeling llm-recommendation 搜广推 学习信号、多任务与反馈偏差 GPL 的伪标签与将未曝光一律当负例，相比纠正了什么假设？ 一律负例把没机会展示误当拒绝，伪标签依据用户意图估计可能相关性，减少这种过强假设。它也可能将语言模型偏见带入学生，需用权重控制并保留真实标签约束。线上无 LLM 是部署选择，不证明伪标签准确。 示意：用户没见过某防水鞋不代表不喜欢，锚点可给它弱正信号；若 LLM 只因广告文案漂亮就打高分，仍需真实反馈校准。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4251d480d33b6f86">GPL 的伪标签与将未曝光一律当负例，相比纠正了什么假设？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agpl-prerank">Generative Pseudo-Labeling for Pre-Ranking with LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group / Renmin University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一律负例把没机会展示误当拒绝，伪标签依据用户意图估计可能相关性，减少这种过强假设。它也可能将语言模型偏见带入学生，需用权重控制并保留真实标签约束。线上无 LLM 是部署选择，不证明伪标签准确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户没见过某防水鞋不代表不喜欢，锚点可给它弱正信号；若 LLM 只因广告文案漂亮就打高分，仍需真实反馈校准。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.20995">原论文</a> · <a href="../../../../reproductions/2602.20995-gpl-prerank/">实现解读</a> · <a href="#qa-4251d480d33b6f86">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:gpl-prerank" data-paper-title="Generative Pseudo-Labeling for Pre-Ranking with LLMs" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Generative Pseudo-Labeling for Pre-Ranking with LLMs 搜广推与 LLM 应用 Alibaba Group / Renmin University 2026-02-24 LLM 从用户行为生成兴趣锚点，为未曝光召回候选产生伪标签；预排序器联合真实与伪监督，且线上不调用 LLM。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 gpl-prerank 核心机制，相对 NDCG@10 +12.84%。  pre-ranking pseudo-labeling llm-recommendation 搜广推 学习信号、多任务与反馈偏差 GPL 的真实与伪监督为什么应分别记录来源和 λ？ 两个标签的可信度与覆盖不同，联合损失系数决定伪样本影响，不能无标记混成同一真实事件。训练只使用可得用户历史，测试目标不应用于构造兴趣锚点；本地公开代理也不能声称完成实际 LLM 标注生产流程。 示意：一百个真实点击和一万条伪标签若等权，弱监督可能压过事实；记录来源与权重，才可检查增益是否只是被某类伪标注主导。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e6c7b39eceaa12bb">GPL 的真实与伪监督为什么应分别记录来源和 λ？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agpl-prerank">Generative Pseudo-Labeling for Pre-Ranking with LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group / Renmin University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两个标签的可信度与覆盖不同，联合损失系数决定伪样本影响，不能无标记混成同一真实事件。训练只使用可得用户历史，测试目标不应用于构造兴趣锚点；本地公开代理也不能声称完成实际 LLM 标注生产流程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一百个真实点击和一万条伪标签若等权，弱监督可能压过事实；记录来源与权重，才可检查增益是否只是被某类伪标注主导。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.20995">原论文</a> · <a href="../../../../reproductions/2602.20995-gpl-prerank/">实现解读</a> · <a href="#qa-e6c7b39eceaa12bb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unimvt" data-paper-title="Jointly Optimizing Debiased CTR and Uplift for Coupons Marketing: A Unified Causal Framework" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Jointly Optimizing Debiased CTR and Uplift for Coupons Marketing: A Unified Causal Framework 搜广推与 LLM 应用 Kuaishou Technology 2026-02-13 用去混杂表示把基础点击倾向与券强度敏感性分开，再由双预测塔和反事实 X-Network 约束事实/反事实结果；单元 uplift 将不同券档的增量统一到可比较尺度。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.03955，相对变化 -26.76%。本地代理目标与论文生产任务不同，不能外推线上 lift。  causal-recommendation uplift-modeling coupon-marketing 搜广推 学习信号、多任务与反馈偏差 UniMVT为什么分基础点击与券强度敏感性？ 原本就会点击或购买的用户不应被全部归因于发券，分开基础倾向和处理响应，才能估增量而不是只预测接受券后的高概率。 例如本来必买的用户拿券购买，不一定是券带来的新增。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-unimvt-218d40bb" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-490ec6066f4cd35b">UniMVT为什么分基础点击与券强度敏感性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunimvt">Jointly Optimizing Debiased CTR and Uplift for Coupons Marketing: A Unified Causal Framework</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原本就会点击或购买的用户不应被全部归因于发券，分开基础倾向和处理响应，才能估增量而不是只预测接受券后的高概率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如本来必买的用户拿券购买，不一定是券带来的新增。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12972">原论文</a> · <a href="../../../../reproductions/2602.12972-unimvt/">实现解读</a> · <a href="#qa-490ec6066f4cd35b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unimvt" data-paper-title="Jointly Optimizing Debiased CTR and Uplift for Coupons Marketing: A Unified Causal Framework" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Jointly Optimizing Debiased CTR and Uplift for Coupons Marketing: A Unified Causal Framework 搜广推与 LLM 应用 Kuaishou Technology 2026-02-13 用去混杂表示把基础点击倾向与券强度敏感性分开，再由双预测塔和反事实 X-Network 约束事实/反事实结果；单元 uplift 将不同券档的增量统一到可比较尺度。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.03955，相对变化 -26.76%。本地代理目标与论文生产任务不同，不能外推线上 lift。  causal-recommendation uplift-modeling coupon-marketing 搜广推 学习信号、多任务与反馈偏差 UniMVT 为什么把基础点击倾向与券强度敏感性分开，再比较有券和无券预测？ 高点击用户即使没有券也可能购买，直接用有券转化率排序会把自然倾向误当券增益。分离表示与双塔先建模基础结果和处理结果，反事实约束连接未观测情形，单元 uplift 再统一不同券档的增量尺度。模型结构不能单独建立因果识别，仍依赖处理分配、混杂控制与反事实假设。 示意：甲不用券也有八成购买机会，乙从两成升到五成。按转化率会选甲，按增量更可能选乙；但若发券对象本来就不同，还需控制选择偏差才可解释差值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unimvt" data-paper-title="Jointly Optimizing Debiased CTR and Uplift for Coupons Marketing: A Unified Causal Framework" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Jointly Optimizing Debiased CTR and Uplift for Coupons Marketing: A Unified Causal Framework 搜广推与 LLM 应用 Kuaishou Technology 2026-02-13 用去混杂表示把基础点击倾向与券强度敏感性分开，再由双预测塔和反事实 X-Network 约束事实/反事实结果；单元 uplift 将不同券档的增量统一到可比较尺度。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.03955，相对变化 -26.76%。本地代理目标与论文生产任务不同，不能外推线上 lift。  causal-recommendation uplift-modeling coupon-marketing 搜广推 学习信号、多任务与反馈偏差 uplift与处理组CTR高低为什么不是同一指标？ uplift比较同条件下处理与不处理的潜在差，处理组高可能只是人群选择偏差。去混杂与反事实目标有假设，不能把预测塔差值自动称已识别因果效应。 例如优惠券专发高意向人群，他们高CTR也可能与券无关。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c31b90b9a26fcc65">uplift与处理组CTR高低为什么不是同一指标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunimvt">Jointly Optimizing Debiased CTR and Uplift for Coupons Marketing: A Unified Causal Framework</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>uplift比较同条件下处理与不处理的潜在差，处理组高可能只是人群选择偏差。去混杂与反事实目标有假设，不能把预测塔差值自动称已识别因果效应。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如优惠券专发高意向人群，他们高CTR也可能与券无关。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12972">原论文</a> · <a href="../../../../reproductions/2602.12972-unimvt/">实现解读</a> · <a href="#qa-c31b90b9a26fcc65">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unimvt" data-paper-title="Jointly Optimizing Debiased CTR and Uplift for Coupons Marketing: A Unified Causal Framework" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Jointly Optimizing Debiased CTR and Uplift for Coupons Marketing: A Unified Causal Framework 搜广推与 LLM 应用 Kuaishou Technology 2026-02-13 用去混杂表示把基础点击倾向与券强度敏感性分开，再由双预测塔和反事实 X-Network 约束事实/反事实结果；单元 uplift 将不同券档的增量统一到可比较尺度。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.03955，相对变化 -26.76%。本地代理目标与论文生产任务不同，不能外推线上 lift。  causal-recommendation uplift-modeling coupon-marketing 搜广推 学习信号、多任务与反馈偏差 本地UniMVT有没有真实随机券档和反事实结果？ 没有，MovieLens代理只验证双塔和反事实约束机制。估计需处理分配混杂与重叠，测试行为不得直接构造处理标签，不能报告真实优惠券增量收益。 例如人为按评分高低分券组，会把结果信息混入处理分配。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d47d70a6e230f86c">本地UniMVT有没有真实随机券档和反事实结果？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunimvt">Jointly Optimizing Debiased CTR and Uplift for Coupons Marketing: A Unified Causal Framework</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有，MovieLens代理只验证双塔和反事实约束机制。估计需处理分配混杂与重叠，测试行为不得直接构造处理标签，不能报告真实优惠券增量收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如人为按评分高低分券组，会把结果信息混入处理分配。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12972">原论文</a> · <a href="../../../../reproductions/2602.12972-unimvt/">实现解读</a> · <a href="#qa-d47d70a6e230f86c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:smes" data-paper-title="SMES: Towards Scalable Multi-Task Recommendation via Expert Sparsity" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="SMES: Towards Scalable Multi-Task Recommendation via Expert Sparsity 搜广推与 LLM 应用 Kuaishou Technology 2026-02-10 把每个任务的激活专家拆为所有任务共享的稳定子集和任务自适应私有子集，并用跨任务全局负载均衡约束路由，控制激活量与专家倾斜。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05359，相对变化 -0.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。  multi-task-learning sparse-moe expert-routing 搜广推 学习信号、多任务与反馈偏差 SMES为什么同时配置共享与任务私有专家？ 共享子集承载跨任务稳定知识，私有子集保留任务差异，避免所有任务争同一套激活路径。全局负载约束再处理专家倾斜，不只是每任务各自均衡。 例如观看与交易共用部分偏好特征，同时保留各自决策专家。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-smes-9171fefe" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6a1f6aeebf107665">SMES为什么同时配置共享与任务私有专家？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asmes">SMES: Towards Scalable Multi-Task Recommendation via Expert Sparsity</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共享子集承载跨任务稳定知识，私有子集保留任务差异，避免所有任务争同一套激活路径。全局负载约束再处理专家倾斜，不只是每任务各自均衡。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如观看与交易共用部分偏好特征，同时保留各自决策专家。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.09386">原论文</a> · <a href="../../../../reproductions/2602.09386-smes/">实现解读</a> · <a href="#qa-6a1f6aeebf107665">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:smes" data-paper-title="SMES: Towards Scalable Multi-Task Recommendation via Expert Sparsity" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="SMES: Towards Scalable Multi-Task Recommendation via Expert Sparsity 搜广推与 LLM 应用 Kuaishou Technology 2026-02-10 把每个任务的激活专家拆为所有任务共享的稳定子集和任务自适应私有子集，并用跨任务全局负载均衡约束路由，控制激活量与专家倾斜。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05359，相对变化 -0.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。  multi-task-learning sparse-moe expert-routing 搜广推 学习信号、多任务与反馈偏差 SMES 为什么既固定共享激活专家，又保留任务自适应私有专家，并做全局负载均衡？ 稳定共享子集承接各任务共性，任务私有选择提供差异化容量，使激活预算不必全花在同一类信息上。跨任务全局平衡防止路由整体拥向少数专家，仅在单任务内部均匀并不能解决总负载倾斜。共享与私有分工是结构约束，专家实际学到什么仍需检查，也要平衡路由自由和均衡惩罚。 示意：点击和购买每次都使用基础兴趣专家，各自再选择新颖性或价格专家。若所有任务私有路由最后都挤向同一台专家，全局均衡会暴露这种跨任务热点。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:smes" data-paper-title="SMES: Towards Scalable Multi-Task Recommendation via Expert Sparsity" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="SMES: Towards Scalable Multi-Task Recommendation via Expert Sparsity 搜广推与 LLM 应用 Kuaishou Technology 2026-02-10 把每个任务的激活专家拆为所有任务共享的稳定子集和任务自适应私有子集，并用跨任务全局负载均衡约束路由，控制激活量与专家倾斜。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05359，相对变化 -0.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。  multi-task-learning sparse-moe expert-routing 搜广推 学习信号、多任务与反馈偏差 共享私有拆分与普通单一路由MoE有什么差别？ 拆分显式限制哪些专家稳定共享、哪些可任务化选择，单一路由由一个候选池竞争。它也不保证天然减少负迁移，任务数据和容量仍决定结果。 例如交易任务不能把全部共享容量随意改成独占而不影响其他任务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b0beb83b4a61eb35">共享私有拆分与普通单一路由MoE有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asmes">SMES: Towards Scalable Multi-Task Recommendation via Expert Sparsity</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>拆分显式限制哪些专家稳定共享、哪些可任务化选择，单一路由由一个候选池竞争。它也不保证天然减少负迁移，任务数据和容量仍决定结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如交易任务不能把全部共享容量随意改成独占而不影响其他任务。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.09386">原论文</a> · <a href="../../../../reproductions/2602.09386-smes/">实现解读</a> · <a href="#qa-b0beb83b4a61eb35">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:smes" data-paper-title="SMES: Towards Scalable Multi-Task Recommendation via Expert Sparsity" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="SMES: Towards Scalable Multi-Task Recommendation via Expert Sparsity 搜广推与 LLM 应用 Kuaishou Technology 2026-02-10 把每个任务的激活专家拆为所有任务共享的稳定子集和任务自适应私有子集，并用跨任务全局负载均衡约束路由，控制激活量与专家倾斜。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05359，相对变化 -0.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。  multi-task-learning sparse-moe expert-routing 搜广推 学习信号、多任务与反馈偏差 SMES全局balance可以只对每个任务分别计算吗？ 只做局部可能看不见多个任务合起来过载同一专家，需按规定跨任务统计。当前MovieLens代理没有生产稀疏调度或集群，激活数与实际吞吐要分开。 例如每任务各用一半专家，但都集中同两位，全局仍高度倾斜。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-de54a8bdf45919c6">SMES全局balance可以只对每个任务分别计算吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asmes">SMES: Towards Scalable Multi-Task Recommendation via Expert Sparsity</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只做局部可能看不见多个任务合起来过载同一专家，需按规定跨任务统计。当前MovieLens代理没有生产稀疏调度或集群，激活数与实际吞吐要分开。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如每任务各用一半专家，但都集中同两位，全局仍高度倾斜。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.09386">原论文</a> · <a href="../../../../reproductions/2602.09386-smes/">实现解读</a> · <a href="#qa-de54a8bdf45919c6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:attribution-sets" data-paper-title="Statistical Learning from Attribution Sets" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Statistical Learning from Attribution Sets 搜广推与 LLM 应用 Google Research 2026-02-06 隐私归因场景不提供点击到转化的真实配对，候选集合还可能重叠。方法不采用随机或最大先验伪标签，而将二元损失拆为与标签无关的部分及标签相关矩，再由归因集合统计估计风险。主源定位：v1 §3 Theorem 1、§4.1 Eq6–7。 完整约7,800次、100–200epoch网格成本过高，不复现（审查DONE）。仅使用自建小规模数学夹具。单元素集合在穷举隐藏二元流时匹配真实风险；多元素集合的v1印刷系数未通过常数函数检查。令，原式给出  广告归因与弱监督 风险估计 搜广推 学习信号、多任务与反馈偏差 Attribution Sets 中的归因集合提供了什么信息，又刻意缺少什么信息？ 集合限制哪些点击可能关联转化，却不给出唯一真实配对，且不同集合还可能重叠。学习目标因此是利用集合统计估计风险，而不是补造每次点击的确定标签。理解这种观测粒度，才能分清集合可支持的估计与真实个体归因之间的差距。 示意：只知道一次购买可能来自前三次曝光，不知道是哪一次起作用；把三次都记为购买正例或随便选一次，都会加入原数据未提供的信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-attribution-sets-5c9ffe92" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-47a34e025140d9eb">Attribution Sets 中的归因集合提供了什么信息，又刻意缺少什么信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aattribution-sets">Statistical Learning from Attribution Sets</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>集合限制哪些点击可能关联转化，却不给出唯一真实配对，且不同集合还可能重叠。学习目标因此是利用集合统计估计风险，而不是补造每次点击的确定标签。理解这种观测粒度，才能分清集合可支持的估计与真实个体归因之间的差距。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>只知道一次购买可能来自前三次曝光，不知道是哪一次起作用；把三次都记为购买正例或随便选一次，都会加入原数据未提供的信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.06276">原论文</a> · <a href="../../../../recommendation-components/2602.06276-attribution-sets/">实现解读</a> · <a href="#qa-47a34e025140d9eb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:attribution-sets" data-paper-title="Statistical Learning from Attribution Sets" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Statistical Learning from Attribution Sets 搜广推与 LLM 应用 Google Research 2026-02-06 隐私归因场景不提供点击到转化的真实配对，候选集合还可能重叠。方法不采用随机或最大先验伪标签，而将二元损失拆为与标签无关的部分及标签相关矩，再由归因集合统计估计风险。主源定位：v1 §3 Theorem 1、§4.1 Eq6–7。 完整约7,800次、100–200epoch网格成本过高，不复现（审查DONE）。仅使用自建小规模数学夹具。单元素集合在穷举隐藏二元流时匹配真实风险；多元素集合的v1印刷系数未通过常数函数检查。令，原式给出  广告归因与弱监督 风险估计 搜广推 学习信号、多任务与反馈偏差 不知道哪次点击对应转化时，为什么不从归因集合随机选一个点击当正例？ 随机选配对会制造不存在的精确标签，且重叠集合会使同一事件被重复影响。方法转而把二元损失拆成标签无关项与标签相关矩，由集合统计估计风险，不先伪造个体归因。本地发现多元素情形的原文印刷系数未通过常数检查，因此保留反例，不能声称该估计器已被完整验证。 示意：一次购买可能关联三个曝光，其中两个还出现在另一归因集合。随便指定一个获胜者会改变监督含义；用集合统计也需先检查估计式的一致性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:attribution-sets" data-paper-title="Statistical Learning from Attribution Sets" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Statistical Learning from Attribution Sets 搜广推与 LLM 应用 Google Research 2026-02-06 隐私归因场景不提供点击到转化的真实配对，候选集合还可能重叠。方法不采用随机或最大先验伪标签，而将二元损失拆为与标签无关的部分及标签相关矩，再由归因集合统计估计风险。主源定位：v1 §3 Theorem 1、§4.1 Eq6–7。 完整约7,800次、100–200epoch网格成本过高，不复现（审查DONE）。仅使用自建小规模数学夹具。单元素集合在穷举隐藏二元流时匹配真实风险；多元素集合的v1印刷系数未通过常数函数检查。令，原式给出  广告归因与弱监督 风险估计 搜广推 学习信号、多任务与反馈偏差 Attribution Sets 的风险分解与最大先验伪标签相比，统计假设落在哪里？ 伪标签先决定隐藏配对，再像完整监督一样训练；风险分解保留不可辨识性，用人口矩和位置先验估计标签相关项。后者避免假装观测到个体真相，但仍依赖正确的统计式与输入假设。本地反例针对印刷系数的有限检查，不是发现了可直接替换的已校正理论。 示意：先验认为首个曝光最可能，也不能将它宣布为真标签；集合估计保留不确定性，但若常数函数检查失败，就必须停下审计而非继续报无偏效果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-32641f7c8cf39a07">Attribution Sets 的风险分解与最大先验伪标签相比，统计假设落在哪里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aattribution-sets">Statistical Learning from Attribution Sets</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>伪标签先决定隐藏配对，再像完整监督一样训练；风险分解保留不可辨识性，用人口矩和位置先验估计标签相关项。后者避免假装观测到个体真相，但仍依赖正确的统计式与输入假设。本地反例针对印刷系数的有限检查，不是发现了可直接替换的已校正理论。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先验认为首个曝光最可能，也不能将它宣布为真标签；集合估计保留不确定性，但若常数函数检查失败，就必须停下审计而非继续报无偏效果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.06276">原论文</a> · <a href="../../../../recommendation-components/2602.06276-attribution-sets/">实现解读</a> · <a href="#qa-32641f7c8cf39a07">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:attribution-sets" data-paper-title="Statistical Learning from Attribution Sets" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Statistical Learning from Attribution Sets 搜广推与 LLM 应用 Google Research 2026-02-06 隐私归因场景不提供点击到转化的真实配对，候选集合还可能重叠。方法不采用随机或最大先验伪标签，而将二元损失拆为与标签无关的部分及标签相关矩，再由归因集合统计估计风险。主源定位：v1 §3 Theorem 1、§4.1 Eq6–7。 完整约7,800次、100–200epoch网格成本过高，不复现（审查DONE）。仅使用自建小规模数学夹具。单元素集合在穷举隐藏二元流时匹配真实风险；多元素集合的v1印刷系数未通过常数函数检查。令，原式给出  广告归因与弱监督 风险估计 搜广推 学习信号、多任务与反馈偏差 实现归因集合估计式时，为什么不能在奇异边界偷偷裁剪分母或按窗口数重归一化？ 原式的二项尾概率、选择指标与固定分母共同决定估计器，裁剪或换分母会变成另一个统计对象。来源要求奇异边界显式失败，并区分已知人口矩与样本插入估计。多元素印刷式未通过检查时保留反例，不能借数值兜底掩盖理论不一致。 示意：分母为零时改成极小正数虽然能输出有限数，却不再是原文公式；应报告条件不成立，让读者看到为何该输入下估计不可用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c450c5f39527fd2b">实现归因集合估计式时，为什么不能在奇异边界偷偷裁剪分母或按窗口数重归一化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aattribution-sets">Statistical Learning from Attribution Sets</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原式的二项尾概率、选择指标与固定分母共同决定估计器，裁剪或换分母会变成另一个统计对象。来源要求奇异边界显式失败，并区分已知人口矩与样本插入估计。多元素印刷式未通过检查时保留反例，不能借数值兜底掩盖理论不一致。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>分母为零时改成极小正数虽然能输出有限数，却不再是原文公式；应报告条件不成立，让读者看到为何该输入下估计不可用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.06276">原论文</a> · <a href="../../../../recommendation-components/2602.06276-attribution-sets/">实现解读</a> · <a href="#qa-c450c5f39527fd2b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:easq" data-paper-title="Towards End-to-End Alignment of User Satisfaction via Questionnaire in Video Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Towards End-to-End Alignment of User Satisfaction via Questionnaire in Video Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-01-28 把稀疏问卷满意度监督放入独立 LoRA 参数路径，避免被海量行为标签淹没；在线 DPO 以问卷专家作为动态 reference，持续更新满意度偏好而尽量不扰动主排序干线。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05160，相对变化 -4.46%。本地代理目标与论文生产任务不同，不能外推线上 lift。  satisfaction-alignment preference-learning online-learning 搜广推 学习信号、多任务与反馈偏差 EASQ 为什么将问卷满意度与行为反馈分为不同参数路径？ 行为标签多但可能只反映短暂点击，问卷更直接却稀疏，合并时容易被数量压过。独立 LoRA 保留满意度学习空间，再作为偏好参考影响更新。问卷同样有响应选择偏差，不能视为全体用户的无偏真值。 示意：用户点击标题却在问卷表示后悔，少量反对信号若混入海量点击会被淹没；独立专家让它仍能影响偏好方向。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-easq-454991cc" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-23ddce3a069d0d93">EASQ 为什么将问卷满意度与行为反馈分为不同参数路径？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aeasq">Towards End-to-End Alignment of User Satisfaction via Questionnaire in Video Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>行为标签多但可能只反映短暂点击，问卷更直接却稀疏，合并时容易被数量压过。独立 LoRA 保留满意度学习空间，再作为偏好参考影响更新。问卷同样有响应选择偏差，不能视为全体用户的无偏真值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户点击标题却在问卷表示后悔，少量反对信号若混入海量点击会被淹没；独立专家让它仍能影响偏好方向。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.20215">原论文</a> · <a href="../../../../reproductions/2601.20215-easq/">实现解读</a> · <a href="#qa-23ddce3a069d0d93">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:easq" data-paper-title="Towards End-to-End Alignment of User Satisfaction via Questionnaire in Video Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Towards End-to-End Alignment of User Satisfaction via Questionnaire in Video Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-01-28 把稀疏问卷满意度监督放入独立 LoRA 参数路径，避免被海量行为标签淹没；在线 DPO 以问卷专家作为动态 reference，持续更新满意度偏好而尽量不扰动主排序干线。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05160，相对变化 -4.46%。本地代理目标与论文生产任务不同，不能外推线上 lift。  satisfaction-alignment preference-learning online-learning 搜广推 学习信号、多任务与反馈偏差 问卷满意度样本很少，EASQ为什么为它保留独立LoRA路径和动态reference？ 海量行为标签容易支配共享更新，使稀疏但直接的满意度监督被淹没。独立低秩路径为问卷知识保留可调空间，在线偏好优化再以问卷专家作动态参照，让更新持续围绕满意度而非只追点击。它降低干扰却不消除问卷抽样偏差，不能把少数答卷直接当全体用户的完整偏好。 示意：许多点击来自猎奇内容，少量问卷却显示用户不满意；独立专家保留这类信号，再引导线上偏好更新，避免点击数量把它全部冲掉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:easq" data-paper-title="Towards End-to-End Alignment of User Satisfaction via Questionnaire in Video Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Towards End-to-End Alignment of User Satisfaction via Questionnaire in Video Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-01-28 把稀疏问卷满意度监督放入独立 LoRA 参数路径，避免被海量行为标签淹没；在线 DPO 以问卷专家作为动态 reference，持续更新满意度偏好而尽量不扰动主排序干线。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05160，相对变化 -4.46%。本地代理目标与论文生产任务不同，不能外推线上 lift。  satisfaction-alignment preference-learning online-learning 搜广推 学习信号、多任务与反馈偏差 动态问卷 reference 与固定 SFT reference，偏好锚点有什么差别？ 固定参考持续锚定初始分布，动态专家随新满意度证据更新，使策略面对更当前的目标。代价是参考非平稳，需记录版本并限制扰动；不意味着参考每次变化都是改进，也不能由 LoRA 结构推断主干能力完全保持。 示意：用户近期更讨厌重复内容，专家更新后参考可反映这种变化；如果仍锚定早期习惯，策略可能继续奖励过去有效但现在过时的模式。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-120b292fc590341a">动态问卷 reference 与固定 SFT reference，偏好锚点有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aeasq">Towards End-to-End Alignment of User Satisfaction via Questionnaire in Video Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定参考持续锚定初始分布，动态专家随新满意度证据更新，使策略面对更当前的目标。代价是参考非平稳，需记录版本并限制扰动；不意味着参考每次变化都是改进，也不能由 LoRA 结构推断主干能力完全保持。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户近期更讨厌重复内容，专家更新后参考可反映这种变化；如果仍锚定早期习惯，策略可能继续奖励过去有效但现在过时的模式。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.20215">原论文</a> · <a href="../../../../reproductions/2601.20215-easq/">实现解读</a> · <a href="#qa-120b292fc590341a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:easq" data-paper-title="Towards End-to-End Alignment of User Satisfaction via Questionnaire in Video Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Towards End-to-End Alignment of User Satisfaction via Questionnaire in Video Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-01-28 把稀疏问卷满意度监督放入独立 LoRA 参数路径，避免被海量行为标签淹没；在线 DPO 以问卷专家作为动态 reference，持续更新满意度偏好而尽量不扰动主排序干线。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05160，相对变化 -4.46%。本地代理目标与论文生产任务不同，不能外推线上 lift。  satisfaction-alignment preference-learning online-learning 搜广推 学习信号、多任务与反馈偏差 验收 EASQ 时，为什么要检查实际可训练参数，而不只看配置写了 LoRA？ 若主干仍被优化器更新，实验就不是稀疏满意度的独立低秩路径；参考概率还须来自记录版本，避免比较对象无声变化。训练和服务依赖也需一致。来源公开代理没有真实问卷，不能把最终排序分当作满意度复现。 示意：主干全量更新可能更容易降低 loss，却无法证明低秩路径保护了原排序；查看梯度与优化器参数范围，比只看模块名可靠。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-09ba941e97be607b">验收 EASQ 时，为什么要检查实际可训练参数，而不只看配置写了 LoRA？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aeasq">Towards End-to-End Alignment of User Satisfaction via Questionnaire in Video Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若主干仍被优化器更新，实验就不是稀疏满意度的独立低秩路径；参考概率还须来自记录版本，避免比较对象无声变化。训练和服务依赖也需一致。来源公开代理没有真实问卷，不能把最终排序分当作满意度复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>主干全量更新可能更容易降低 loss，却无法证明低秩路径保护了原排序；查看梯度与优化器参数范围，比只看模块名可靠。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.20215">原论文</a> · <a href="../../../../reproductions/2601.20215-easq/">实现解读</a> · <a href="#qa-09ba941e97be607b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:podcast-mtl" data-paper-title="Cold-Starting Podcast Ads and Promotions with Multi-Task Learning on Spotify" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Cold-Starting Podcast Ads and Promotions with Multi-Task Learning on Spotify 搜广推与 LLM 应用 Spotify 2026-01-05 新 podcast 缺少广告点击与播放数据。论文联合训练 ads 和 organic promotions，共享 user/content/context 表征，从数据丰富任务迁移到冷启动任务，并以不平衡处理和梯度平衡抑制 negative transfer。 Fidelity: 核心机制复现。执行 shared low-rank multi-task representation 和冷物品分桶。MovieLens 电影与 genre 代理 podcast/ad 特征，没有 Spotify impression、bid 和曝光校准日志。本地对照口径：基线是 single-task popularity/content ranker；实验组联合 organic/promotion 两任务，NDCG@10 0.03540→0.02810，相对 -20.63%，本地出现 negative transfer。  cold-start multi-task ads 搜广推 学习信号、多任务与反馈偏差 Podcast MTL 中“冷启动”是完全没有内容信息，还是缺少目标任务反馈？ 这里关键是新播客缺少广告点击和播放反馈，不表示标题、主题等内容也为空。共享的 user、content、context 可提供已有线索，但不能把这些线索当成已观测广告效果。区分信息缺口，才能知道迁移补的是训练信号，而非凭空生成一份真实点击日志。 示意：新节目已有介绍和主持人信息，却还没有广告曝光；模型能使用内容判断相近受众，但不能说它已经验证了这批人会点击该广告。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-podcast-mtl-fc67da12" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ce83c5c320e4d33e">Podcast MTL 中“冷启动”是完全没有内容信息，还是缺少目标任务反馈？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apodcast-mtl">Cold-Starting Podcast Ads and Promotions with Multi-Task Learning on Spotify</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Spotify</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这里关键是新播客缺少广告点击和播放反馈，不表示标题、主题等内容也为空。共享的 user、content、context 可提供已有线索，但不能把这些线索当成已观测广告效果。区分信息缺口，才能知道迁移补的是训练信号，而非凭空生成一份真实点击日志。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新节目已有介绍和主持人信息，却还没有广告曝光；模型能使用内容判断相近受众，但不能说它已经验证了这批人会点击该广告。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.02306">原论文</a> · <a href="../../../../reproductions/2601.02306-podcast-mtl/">实现解读</a> · <a href="#qa-ce83c5c320e4d33e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:podcast-mtl" data-paper-title="Cold-Starting Podcast Ads and Promotions with Multi-Task Learning on Spotify" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Cold-Starting Podcast Ads and Promotions with Multi-Task Learning on Spotify 搜广推与 LLM 应用 Spotify 2026-01-05 新 podcast 缺少广告点击与播放数据。论文联合训练 ads 和 organic promotions，共享 user/content/context 表征，从数据丰富任务迁移到冷启动任务，并以不平衡处理和梯度平衡抑制 negative transfer。 Fidelity: 核心机制复现。执行 shared low-rank multi-task representation 和冷物品分桶。MovieLens 电影与 genre 代理 podcast/ad 特征，没有 Spotify impression、bid 和曝光校准日志。本地对照口径：基线是 single-task popularity/content ranker；实验组联合 organic/promotion 两任务，NDCG@10 0.03540→0.02810，相对 -20.63%，本地出现 negative transfer。  cold-start multi-task ads 搜广推 学习信号、多任务与反馈偏差 Podcast 多任务学习怎样借自然推广数据帮助缺少广告反馈的新播客，又为什么需要梯度平衡？ 广告与自然推广任务共享用户、内容和上下文表示，使数据较丰富任务提供基础语义与偏好信号；各任务头保留不同的预测目标。样本不平衡和目标冲突可能让强任务压过冷启动任务，因此要调整采样或梯度贡献。共享带来迁移机会，但相关性不足时也会负迁移，不能因共享数据就预设新播客必然受益。 示意：新播客还没有广告点击，却有少量自然推荐播放。共享编码器可先学到它适合哪些听众，再由广告任务头适配广告行为，同时限制大流量任务的梯度压制。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:podcast-mtl" data-paper-title="Cold-Starting Podcast Ads and Promotions with Multi-Task Learning on Spotify" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Cold-Starting Podcast Ads and Promotions with Multi-Task Learning on Spotify 搜广推与 LLM 应用 Spotify 2026-01-05 新 podcast 缺少广告点击与播放数据。论文联合训练 ads 和 organic promotions，共享 user/content/context 表征，从数据丰富任务迁移到冷启动任务，并以不平衡处理和梯度平衡抑制 negative transfer。 Fidelity: 核心机制复现。执行 shared low-rank multi-task representation 和冷物品分桶。MovieLens 电影与 genre 代理 podcast/ad 特征，没有 Spotify impression、bid 和曝光校准日志。本地对照口径：基线是 single-task popularity/content ranker；实验组联合 organic/promotion 两任务，NDCG@10 0.03540→0.02810，相对 -20.63%，本地出现 negative transfer。  cold-start multi-task ads 搜广推 学习信号、多任务与反馈偏差 梯度平衡与仅按样本数量混合，两种训练会怎样对待小任务？ 按数量混合容易让大任务主导共享参数，梯度或权重平衡调节实际训练贡献，让稀疏广告任务仍有学习空间。过度抬小任务又可能放大噪声，需按任务验证。不能通过把所有日志重复采样就保证冷启动改善。 示意：一百万自然推广和一千广告样本直接拼接，后者梯度可能被淹没；适当平衡保留它的方向，但不意味着一条广告标签应无限放大。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c78cd2c217eacbf6">梯度平衡与仅按样本数量混合，两种训练会怎样对待小任务？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apodcast-mtl">Cold-Starting Podcast Ads and Promotions with Multi-Task Learning on Spotify</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Spotify</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>按数量混合容易让大任务主导共享参数，梯度或权重平衡调节实际训练贡献，让稀疏广告任务仍有学习空间。过度抬小任务又可能放大噪声，需按任务验证。不能通过把所有日志重复采样就保证冷启动改善。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一百万自然推广和一千广告样本直接拼接，后者梯度可能被淹没；适当平衡保留它的方向，但不意味着一条广告标签应无限放大。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.02306">原论文</a> · <a href="../../../../reproductions/2601.02306-podcast-mtl/">实现解读</a> · <a href="#qa-c78cd2c217eacbf6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:podcast-mtl" data-paper-title="Cold-Starting Podcast Ads and Promotions with Multi-Task Learning on Spotify" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Cold-Starting Podcast Ads and Promotions with Multi-Task Learning on Spotify 搜广推与 LLM 应用 Spotify 2026-01-05 新 podcast 缺少广告点击与播放数据。论文联合训练 ads 和 organic promotions，共享 user/content/context 表征，从数据丰富任务迁移到冷启动任务，并以不平衡处理和梯度平衡抑制 negative transfer。 Fidelity: 核心机制复现。执行 shared low-rank multi-task representation 和冷物品分桶。MovieLens 电影与 genre 代理 podcast/ad 特征，没有 Spotify impression、bid 和曝光校准日志。本地对照口径：基线是 single-task popularity/content ranker；实验组联合 organic/promotion 两任务，NDCG@10 0.03540→0.02810，相对 -20.63%，本地出现 negative transfer。  cold-start multi-task ads 搜广推 学习信号、多任务与反馈偏差 Podcast 两任务标签缺失时，为什么不应给另一任务填零？ 自然推广样本未必观察广告结果，缺失只是没有同义反馈，mask 对应损失而不是制造负例。共享表示仍可由可观测任务更新。数据构造、头身份与 α 记录需清楚，本地电影替代不代表真实新播客广告点击。 示意：用户听了自然推荐播客，并没有看到其广告，不能因此写广告未点击负例；否则模型会把缺少广告机会误学成广告效果差。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6cb40b601772ffa9">Podcast 两任务标签缺失时，为什么不应给另一任务填零？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apodcast-mtl">Cold-Starting Podcast Ads and Promotions with Multi-Task Learning on Spotify</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Spotify</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>自然推广样本未必观察广告结果，缺失只是没有同义反馈，mask 对应损失而不是制造负例。共享表示仍可由可观测任务更新。数据构造、头身份与 α 记录需清楚，本地电影替代不代表真实新播客广告点击。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户听了自然推荐播客，并没有看到其广告，不能因此写广告未点击负例；否则模型会把缺少广告机会误学成广告效果差。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.02306">原论文</a> · <a href="../../../../reproductions/2601.02306-podcast-mtl/">实现解读</a> · <a href="#qa-6cb40b601772ffa9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:click-a-buy-b" data-paper-title="Click A, Buy B: Rethinking Conversion Attribution in E-Commerce Recommendations" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Click A, Buy B: Rethinking Conversion Attribution in E-Commerce Recommendations 搜广推与 LLM 应用 Pinterest 2025-07-20 Last-click attribution 默认点击和购买属于同一商品，忽略用户点 A 后买 B。论文将 Click-A-Buy-A 与 Click-A-Buy-B 分成多任务，并用商品 taxonomy 建模 A/B 的协同归因。 Fidelity: 核心机制复现。实际构造 CABA/CABB 双分支，并按公开 genre taxonomy 学习跨物品协同权重。连续观影不等价于购买；没有真实曝光、归因窗口、广告竞价和 Pinterest taxonomy。本地对照口径：相对 last-click 单物品归因基线，实验组 NDCG@10 +33.70%。  conversion-attribution multi-task-learning taxonomy ads-ranking 搜广推 学习信号、多任务与反馈偏差 Click-A-Buy-B 为什么把点击物品与购买物品视作可能不同的对象？ 用户可通过 A 发现需求，再因价格、规格等转向 B，购买与点击并不总是一对一同物品转化。分别学习 CABA 与 CABB 能保留自身成交和跨商品引导两种路径，taxonomy 提供它们的关系线索。观测协同仍不自动证明 A 对 B 有因果促进。 示意：点开一台相机后买了另一品牌，A 不是自身成交却可能参与决策；把购买只归为 A 的转化会学错商品结果，也丢失跨商品路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-click-a-buy-b-aac757e9" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-fba99f94af149fd0">Click-A-Buy-B 为什么把点击物品与购买物品视作可能不同的对象？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aclick-a-buy-b">Click A, Buy B: Rethinking Conversion Attribution in E-Commerce Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用户可通过 A 发现需求，再因价格、规格等转向 B，购买与点击并不总是一对一同物品转化。分别学习 CABA 与 CABB 能保留自身成交和跨商品引导两种路径，taxonomy 提供它们的关系线索。观测协同仍不自动证明 A 对 B 有因果促进。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>点开一台相机后买了另一品牌，A 不是自身成交却可能参与决策；把购买只归为 A 的转化会学错商品结果，也丢失跨商品路径。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.15113">原论文</a> · <a href="../../../../reproductions/2507.15113-click-a-buy-b/">实现解读</a> · <a href="#qa-fba99f94af149fd0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:click-a-buy-b" data-paper-title="Click A, Buy B: Rethinking Conversion Attribution in E-Commerce Recommendations" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Click A, Buy B: Rethinking Conversion Attribution in E-Commerce Recommendations 搜广推与 LLM 应用 Pinterest 2025-07-20 Last-click attribution 默认点击和购买属于同一商品，忽略用户点 A 后买 B。论文将 Click-A-Buy-A 与 Click-A-Buy-B 分成多任务，并用商品 taxonomy 建模 A/B 的协同归因。 Fidelity: 核心机制复现。实际构造 CABA/CABB 双分支，并按公开 genre taxonomy 学习跨物品协同权重。连续观影不等价于购买；没有真实曝光、归因窗口、广告竞价和 Pinterest taxonomy。本地对照口径：相对 last-click 单物品归因基线，实验组 NDCG@10 +33.70%。  conversion-attribution multi-task-learning taxonomy ads-ranking 搜广推 学习信号、多任务与反馈偏差 用户点击商品A后购买B，为什么不能把购买收益全部当成A自身转化？ 点击对象和购买对象可能不同，last-click同商品归因会漏掉跨商品的影响。论文把Click-A-Buy-A与Click-A-Buy-B分成任务，并借taxonomy表示A与B的类别关系，让模型学习从入口到最终商品的不同路径。这是在改进观测归因与预测，并不自动识别A导致B购买的因果效应。 示意：用户先看入门相机，比较后买了更高型号；若只统计同商品成交，入口相机被当作无价值，实际上它参与了一条跨商品决策路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:click-a-buy-b" data-paper-title="Click A, Buy B: Rethinking Conversion Attribution in E-Commerce Recommendations" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Click A, Buy B: Rethinking Conversion Attribution in E-Commerce Recommendations 搜广推与 LLM 应用 Pinterest 2025-07-20 Last-click attribution 默认点击和购买属于同一商品，忽略用户点 A 后买 B。论文将 Click-A-Buy-A 与 Click-A-Buy-B 分成多任务，并用商品 taxonomy 建模 A/B 的协同归因。 Fidelity: 核心机制复现。实际构造 CABA/CABB 双分支，并按公开 genre taxonomy 学习跨物品协同权重。连续观影不等价于购买；没有真实曝光、归因窗口、广告竞价和 Pinterest taxonomy。本地对照口径：相对 last-click 单物品归因基线，实验组 NDCG@10 +33.70%。  conversion-attribution multi-task-learning taxonomy ads-ranking 搜广推 学习信号、多任务与反馈偏差 CABB 与普通 next-item 预测相比，为什么还需要区分行为类型与商品层次？ 普通下一项只描述序列相邻，未必区分浏览、点击与购买，也未明确 A、B 的商品关系。CABB 的任务定义将跨商品购买路径单独监督，taxonomy 帮助组织可迁移关系。若用连续观影代理，只保留相邻关系，不等于验证真实购买归因。 示意：电影甲后看电影乙可模拟跨项转移，却没有广告点击和交易闭环；这能检查模型连接，不应直接称为电商归因效果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-006455c4de387e4b">CABB 与普通 next-item 预测相比，为什么还需要区分行为类型与商品层次？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aclick-a-buy-b">Click A, Buy B: Rethinking Conversion Attribution in E-Commerce Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>普通下一项只描述序列相邻，未必区分浏览、点击与购买，也未明确 A、B 的商品关系。CABB 的任务定义将跨商品购买路径单独监督，taxonomy 帮助组织可迁移关系。若用连续观影代理，只保留相邻关系，不等于验证真实购买归因。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>电影甲后看电影乙可模拟跨项转移，却没有广告点击和交易闭环；这能检查模型连接，不应直接称为电商归因效果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.15113">原论文</a> · <a href="../../../../reproductions/2507.15113-click-a-buy-b/">实现解读</a> · <a href="#qa-006455c4de387e4b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:click-a-buy-b" data-paper-title="Click A, Buy B: Rethinking Conversion Attribution in E-Commerce Recommendations" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Click A, Buy B: Rethinking Conversion Attribution in E-Commerce Recommendations 搜广推与 LLM 应用 Pinterest 2025-07-20 Last-click attribution 默认点击和购买属于同一商品，忽略用户点 A 后买 B。论文将 Click-A-Buy-A 与 Click-A-Buy-B 分成多任务，并用商品 taxonomy 建模 A/B 的协同归因。 Fidelity: 核心机制复现。实际构造 CABA/CABB 双分支，并按公开 genre taxonomy 学习跨物品协同权重。连续观影不等价于购买；没有真实曝光、归因窗口、广告竞价和 Pinterest taxonomy。本地对照口径：相对 last-click 单物品归因基线，实验组 NDCG@10 +33.70%。  conversion-attribution multi-task-learning taxonomy ads-ranking 搜广推 学习信号、多任务与反馈偏差 CABB 本地连续观影代理应怎样记录，才不把购买标签伪造出来？ 需要明确将先后观看映射为 Click-A/Buy-B 的替代任务，保留相同数据、候选与基线比较，并将结果限定在该代理。taxonomy 权重只连接对应 A、B，不能读取测试目标提前确定候选类别，也不能把公开评分解释成真实交易金额。 示意：报告可写“以连续观看模拟跨物品路径”，不能写“用户实际点击 A 并购买 B”；若正确答案类别只在测试后可知，它也不能进入推理输入。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-2cc0afb634ea21f7">CABB 本地连续观影代理应怎样记录，才不把购买标签伪造出来？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aclick-a-buy-b">Click A, Buy B: Rethinking Conversion Attribution in E-Commerce Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>需要明确将先后观看映射为 Click-A/Buy-B 的替代任务，保留相同数据、候选与基线比较，并将结果限定在该代理。taxonomy 权重只连接对应 A、B，不能读取测试目标提前确定候选类别，也不能把公开评分解释成真实交易金额。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>报告可写“以连续观看模拟跨物品路径”，不能写“用户实际点击 A 并购买 B”；若正确答案类别只在测试后可知，它也不能进入推理输入。</p>
<p class="ar-learning-sources">依据：背景与主要改动、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.15113">原论文</a> · <a href="../../../../reproductions/2507.15113-click-a-buy-b/">实现解读</a> · <a href="#qa-2cc0afb634ea21f7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mgoe" data-paper-title="Macro Graph of Experts for Billion-Scale Multi-Task Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Macro Graph of Experts for Billion-Scale Multi-Task Recommendation 搜广推与 LLM 应用 Alibaba 2025-06-12 MMoE 只在样本级通过 gate 隐式共享，难表达任务间稳定结构。MGOE 先构建 Macro Task Merging Graph，再由 Macro Graph Bottom/Experts 传播跨任务信息，最后进入任务塔。 Fidelity: 核心机制复现。实际估计多任务相关图，执行宏观图传播 experts 和任务门控预测。公开 proxy 任务远小于工业多目标；没有十亿级 sparse embedding、分布式图构建和阿里线上特征。本地对照口径：相对 MMoE 独立 gate 基线，实验组 NDCG@10 +7.03%。  multi-task-learning mixture-of-experts graph-neural-network ranking 搜广推 学习信号、多任务与反馈偏差 MGOE 为什么先建 Macro Task Merging Graph，再让专家传播？ 样本级 gate 不显式表达稳定任务结构，图把哪些目标可共享的信息关系写入传播路径，Macro Graph Bottom/Experts 再组合后接任务塔。任务相关性可能随场景变化，图先验不必永远正确，也不能把边连接解释为因果关系。 示意：点击、长看与购买有不同联系，图可让相关目标交换表征；但若用一条边就认定点击一定导致购买，则超出了任务共享含义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-mgoe-e3468d6f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f4ad32d70416c198">MGOE 为什么先建 Macro Task Merging Graph，再让专家传播？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amgoe">Macro Graph of Experts for Billion-Scale Multi-Task Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>样本级 gate 不显式表达稳定任务结构，图把哪些目标可共享的信息关系写入传播路径，Macro Graph Bottom/Experts 再组合后接任务塔。任务相关性可能随场景变化，图先验不必永远正确，也不能把边连接解释为因果关系。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>点击、长看与购买有不同联系，图可让相关目标交换表征；但若用一条边就认定点击一定导致购买，则超出了任务共享含义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2506.10520">原论文</a> · <a href="../../../../reproductions/2506.10520-mgoe/">实现解读</a> · <a href="#qa-f4ad32d70416c198">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mgoe" data-paper-title="Macro Graph of Experts for Billion-Scale Multi-Task Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Macro Graph of Experts for Billion-Scale Multi-Task Recommendation 搜广推与 LLM 应用 Alibaba 2025-06-12 MMoE 只在样本级通过 gate 隐式共享，难表达任务间稳定结构。MGOE 先构建 Macro Task Merging Graph，再由 Macro Graph Bottom/Experts 传播跨任务信息，最后进入任务塔。 Fidelity: 核心机制复现。实际估计多任务相关图，执行宏观图传播 experts 和任务门控预测。公开 proxy 任务远小于工业多目标；没有十亿级 sparse embedding、分布式图构建和阿里线上特征。本地对照口径：相对 MMoE 独立 gate 基线，实验组 NDCG@10 +7.03%。  multi-task-learning mixture-of-experts graph-neural-network ranking 搜广推 学习信号、多任务与反馈偏差 MGOE显式建立任务关系图，相比MMoE的样本级gate增加了什么信息？ MMoE可按样本组合专家，却未必直接表达任务之间较稳定的结构。任务图让相关目标在图底座和专家层传播信息，再由各自任务塔预测，把宏观关系与局部路由分开。图边如果估计错误也会传播负迁移，因此显式关系不等于天然正确，需要检查相邻任务及不相关任务的表现。 示意：点击、加购、购买有较强联系，举报可能关注另一套因素；任务图可控制长期共享路径，而不是要求每个样本的gate从零重学所有任务关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mgoe" data-paper-title="Macro Graph of Experts for Billion-Scale Multi-Task Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Macro Graph of Experts for Billion-Scale Multi-Task Recommendation 搜广推与 LLM 应用 Alibaba 2025-06-12 MMoE 只在样本级通过 gate 隐式共享，难表达任务间稳定结构。MGOE 先构建 Macro Task Merging Graph，再由 Macro Graph Bottom/Experts 传播跨任务信息，最后进入任务塔。 Fidelity: 核心机制复现。实际估计多任务相关图，执行宏观图传播 experts 和任务门控预测。公开 proxy 任务远小于工业多目标；没有十亿级 sparse embedding、分布式图构建和阿里线上特征。本地对照口径：相对 MMoE 独立 gate 基线，实验组 NDCG@10 +7.03%。  multi-task-learning mixture-of-experts graph-neural-network ranking 搜广推 学习信号、多任务与反馈偏差 MGOE 与 MMoE 独立 task gate，相比多了哪种共享归纳偏置？ MMoE 通过每样本选择专家隐式共享，MGOE 又用任务图约束跨任务信息如何传播，提供更稳定结构。该偏置可帮助稀疏任务，也会传错误关系造成负迁移。来源总体改善伴随头部变化，不能据图显式就称各任务都更好。 示意：稀疏购买任务可沿图借点击知识，若退货任务被错误强连，也可能继承不适合的方向；独立 gate 则没有同样固定传播路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d46d50e1c7231b58">MGOE 与 MMoE 独立 task gate，相比多了哪种共享归纳偏置？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amgoe">Macro Graph of Experts for Billion-Scale Multi-Task Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>MMoE 通过每样本选择专家隐式共享，MGOE 又用任务图约束跨任务信息如何传播，提供更稳定结构。该偏置可帮助稀疏任务，也会传错误关系造成负迁移。来源总体改善伴随头部变化，不能据图显式就称各任务都更好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>稀疏购买任务可沿图借点击知识，若退货任务被错误强连，也可能继承不适合的方向；独立 gate 则没有同样固定传播路径。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2506.10520">原论文</a> · <a href="../../../../reproductions/2506.10520-mgoe/">实现解读</a> · <a href="#qa-d46d50e1c7231b58">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mgoe" data-paper-title="Macro Graph of Experts for Billion-Scale Multi-Task Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Macro Graph of Experts for Billion-Scale Multi-Task Recommendation 搜广推与 LLM 应用 Alibaba 2025-06-12 MMoE 只在样本级通过 gate 隐式共享，难表达任务间稳定结构。MGOE 先构建 Macro Task Merging Graph，再由 Macro Graph Bottom/Experts 传播跨任务信息，最后进入任务塔。 Fidelity: 核心机制复现。实际估计多任务相关图，执行宏观图传播 experts 和任务门控预测。公开 proxy 任务远小于工业多目标；没有十亿级 sparse embedding、分布式图构建和阿里线上特征。本地对照口径：相对 MMoE 独立 gate 基线，实验组 NDCG@10 +7.03%。  multi-task-learning mixture-of-experts graph-neural-network ranking 搜广推 学习信号、多任务与反馈偏差 MGOE 的归一邻接与任务索引为什么要和 expert 张量保持一致？ A 的行列定义任务或图节点身份，传播 H 后的任务塔需读取正确位置；归一、自环与层数影响混合强度，不能任意换邻接仍称同算法。任务标签只用于训练，不能在测试用实际反馈重建图再评分。 示意：邻接第二行是购买，H 第二行却放长看表征，矩阵乘能运行但共享对象错了；检查维度不能代替节点身份对齐。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-9f0b168dfe442d78">MGOE 的归一邻接与任务索引为什么要和 expert 张量保持一致？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amgoe">Macro Graph of Experts for Billion-Scale Multi-Task Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>A 的行列定义任务或图节点身份，传播 H 后的任务塔需读取正确位置；归一、自环与层数影响混合强度，不能任意换邻接仍称同算法。任务标签只用于训练，不能在测试用实际反馈重建图再评分。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>邻接第二行是购买，H 第二行却放长看表征，矩阵乘能运行但共享对象错了；检查维度不能代替节点身份对齐。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2506.10520">原论文</a> · <a href="../../../../reproductions/2506.10520-mgoe/">实现解读</a> · <a href="#qa-9f0b168dfe442d78">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cwm" data-paper-title="Counteracting Duration Bias in Video Recommendation via Counterfactual Watch Time" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Counteracting Duration Bias in Video Recommendation via Counterfactual Watch Time 搜广推与 LLM 应用 Kuaishou Technology / Renmin University of China 2024-06-12 以反事实观看时长估计消除视频时长偏置：区分观察到的 watch time 与在统一时长干预下的潜在收益。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 cwm 核心机制；相对 NDCG@10 -17.89%。  ranking counterfactual-learning watch-time bias 搜广推 学习信号、多任务与反馈偏差 CWM 中“统一时长干预下的潜在观看收益”为什么不同于观察到的观看秒数？ 视频长度限制了可观看时间，也与内容类型有关，实际秒数混合偏好和时长机会。统一干预希望比较在相同曝光时长条件下的潜在结果，减少长视频天然占优。该潜在量不可直接观察，需要模型和识别假设，不能把简单除以时长就称为因果估计。 示意：看完十五秒短片和看两分钟长片，秒数更长不必然表示更喜欢；若在同一时长机会下比较，排名可能不同，但结果需要可信建模。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-cwm-65e93cb4" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-26b7e8adddd68f37">CWM 中“统一时长干预下的潜在观看收益”为什么不同于观察到的观看秒数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acwm">Counteracting Duration Bias in Video Recommendation via Counterfactual Watch Time</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology / Renmin University of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>视频长度限制了可观看时间，也与内容类型有关，实际秒数混合偏好和时长机会。统一干预希望比较在相同曝光时长条件下的潜在结果，减少长视频天然占优。该潜在量不可直接观察，需要模型和识别假设，不能把简单除以时长就称为因果估计。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>看完十五秒短片和看两分钟长片，秒数更长不必然表示更喜欢；若在同一时长机会下比较，排名可能不同，但结果需要可信建模。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2406.07932">原论文</a> · <a href="../../../../reproductions/2406.07932-cwm/">实现解读</a> · <a href="#qa-26b7e8adddd68f37">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cwm" data-paper-title="Counteracting Duration Bias in Video Recommendation via Counterfactual Watch Time" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Counteracting Duration Bias in Video Recommendation via Counterfactual Watch Time 搜广推与 LLM 应用 Kuaishou Technology / Renmin University of China 2024-06-12 以反事实观看时长估计消除视频时长偏置：区分观察到的 watch time 与在统一时长干预下的潜在收益。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 cwm 核心机制；相对 NDCG@10 -17.89%。  ranking counterfactual-learning watch-time bias 搜广推 学习信号、多任务与反馈偏差 用反事实观看时长打分，为什么比直接比较实际观看秒数更贴近偏好？ 实际观看秒数同时受内容吸引力和视频长度限制，长视频天然有更多累积空间。CWM尝试在统一时长干预下比较潜在观看收益，将机会差异与偏好信号分开。这个估计依赖反事实建模假设，并非简单用秒数除以时长；本地代理机制不能证明已消除真实曝光与时长混杂。 示意：一个短视频被完整看完20秒，另一个长视频看了30秒就划走，直接按秒数会偏向后者；统一观看机会后，二者的偏好排序未必相同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cwm" data-paper-title="Counteracting Duration Bias in Video Recommendation via Counterfactual Watch Time" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Counteracting Duration Bias in Video Recommendation via Counterfactual Watch Time 搜广推与 LLM 应用 Kuaishou Technology / Renmin University of China 2024-06-12 以反事实观看时长估计消除视频时长偏置：区分观察到的 watch time 与在统一时长干预下的潜在收益。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 cwm 核心机制；相对 NDCG@10 -17.89%。  ranking counterfactual-learning watch-time bias 搜广推 学习信号、多任务与反馈偏差 CWM 与按完播率排序相比，消除时长影响的假设有什么差别？ 完播率是观测比例，对短内容更容易达到高值，也没有显式反事实。CWM 目标是对统一时长干预估计潜在结果，试图区分偏好与长度机制。两者偏差来源不同，不能从数学目标直接断言因果方法总优于比例，也不能忽略模型误设。 示意：三秒广告轻易完播，长教程很难百分百看完；完播率可能偏向前者，反事实模型则尝试问相同时间条件下谁更有价值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5537f98a3b8a194f">CWM 与按完播率排序相比，消除时长影响的假设有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acwm">Counteracting Duration Bias in Video Recommendation via Counterfactual Watch Time</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology / Renmin University of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>完播率是观测比例，对短内容更容易达到高值，也没有显式反事实。CWM 目标是对统一时长干预估计潜在结果，试图区分偏好与长度机制。两者偏差来源不同，不能从数学目标直接断言因果方法总优于比例，也不能忽略模型误设。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三秒广告轻易完播，长教程很难百分百看完；完播率可能偏向前者，反事实模型则尝试问相同时间条件下谁更有价值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2406.07932">原论文</a> · <a href="../../../../reproductions/2406.07932-cwm/">实现解读</a> · <a href="#qa-5537f98a3b8a194f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cwm" data-paper-title="Counteracting Duration Bias in Video Recommendation via Counterfactual Watch Time" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Counteracting Duration Bias in Video Recommendation via Counterfactual Watch Time 搜广推与 LLM 应用 Kuaishou Technology / Renmin University of China 2024-06-12 以反事实观看时长估计消除视频时长偏置：区分观察到的 watch time 与在统一时长干预下的潜在收益。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 cwm 核心机制；相对 NDCG@10 -17.89%。  ranking counterfactual-learning watch-time bias 搜广推 学习信号、多任务与反馈偏差 实现 CWM 的 do(D=d0) 目标时，训练与预测的时长变量要如何区分？ 观测 D 可用于拟合时长机制，预测比较时应按约定固定 d0，再输出相应潜在量及定义的偏置项。若每个候选仍用自身长度却声称统一干预，就没有完成目标。来源本地电影代理缺少真实短视频观看数据，不能当作潜在观看收益实测。 示意：比较三十秒与五分钟候选时都设相同 d0；一个用三十、另一个用三百再称公平时长比较，会把原来的长度差重新带回。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1a473e83d1d8b5a0">实现 CWM 的 do(D=d0) 目标时，训练与预测的时长变量要如何区分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acwm">Counteracting Duration Bias in Video Recommendation via Counterfactual Watch Time</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology / Renmin University of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>观测 D 可用于拟合时长机制，预测比较时应按约定固定 d0，再输出相应潜在量及定义的偏置项。若每个候选仍用自身长度却声称统一干预，就没有完成目标。来源本地电影代理缺少真实短视频观看数据，不能当作潜在观看收益实测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>比较三十秒与五分钟候选时都设相同 d0；一个用三十、另一个用三百再称公平时长比较，会把原来的长度差重新带回。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2406.07932">原论文</a> · <a href="../../../../reproductions/2406.07932-cwm/">实现解读</a> · <a href="#qa-1a473e83d1d8b5a0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ple" data-paper-title="Progressive Layered Extraction (PLE): A Novel Multi-Task Learning Model for Personalized Recommendations" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Progressive Layered Extraction (PLE): A Novel Multi-Task Learning Model for Personalized Recommendations 搜广推与 LLM 应用 Tencent 2020-09-22 MMoE 仍让所有 experts 在所有任务间共享，任务冲突强时难以同时保留共性与个性。PLE 将 experts 分成共享组和任务专属组，通过 CGC 门控逐层提取共享与特定信息，减少跷跷板现象。 复现级别：核心机制复现。复现级别：核心机制复现。实际训练共享/任务专属 experts、CGC gates 和独立 heads；腾讯视频生产规模未复刻。本地对照口径：基线为 MMoE，实验组为共享与任务专属 experts 的 CGC/PLE；平均任务 AUC 相对 +1.34%，见 metrics/movielens-100k-seeds42-44.json。  ranking classic multi-task mixture-of-experts 搜广推 学习信号、多任务与反馈偏差 PLE 所说的“跷跷板现象”，为什么可能被平均任务 AUC 掩盖？ 它指多任务训练中一个目标改善、另一个退化的取舍，平均值会把两者抵消，看不出受损目标。应保留每任务指标及其共同训练条件，再判断共享是否合适。它与一次测量噪声不同，也不意味着所有目标必须取得完全相同的改善幅度。 示意：示意性地，点击 AUC 加两个点、购买减一个点，平均仍会上升；只看平均会遗漏购买目标退化，不能因此宣布两个任务都获益。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-ple-a2bf42a4" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0451f6496f52aa1f">PLE 所说的“跷跷板现象”，为什么可能被平均任务 AUC 掩盖？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aple">Progressive Layered Extraction (PLE): A Novel Multi-Task Learning Model for Personalized Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它指多任务训练中一个目标改善、另一个退化的取舍，平均值会把两者抵消，看不出受损目标。应保留每任务指标及其共同训练条件，再判断共享是否合适。它与一次测量噪声不同，也不意味着所有目标必须取得完全相同的改善幅度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>示意性地，点击 AUC 加两个点、购买减一个点，平均仍会上升；只看平均会遗漏购买目标退化，不能因此宣布两个任务都获益。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://doi.org/10.1145/3383313.3412236">原论文</a> · <a href="../../../../reproductions/recsys2020-ple-ple/">实现解读</a> · <a href="#qa-0451f6496f52aa1f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ple" data-paper-title="Progressive Layered Extraction (PLE): A Novel Multi-Task Learning Model for Personalized Recommendations" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Progressive Layered Extraction (PLE): A Novel Multi-Task Learning Model for Personalized Recommendations 搜广推与 LLM 应用 Tencent 2020-09-22 MMoE 仍让所有 experts 在所有任务间共享，任务冲突强时难以同时保留共性与个性。PLE 将 experts 分成共享组和任务专属组，通过 CGC 门控逐层提取共享与特定信息，减少跷跷板现象。 复现级别：核心机制复现。复现级别：核心机制复现。实际训练共享/任务专属 experts、CGC gates 和独立 heads；腾讯视频生产规模未复刻。本地对照口径：基线为 MMoE，实验组为共享与任务专属 experts 的 CGC/PLE；平均任务 AUC 相对 +1.34%，见 metrics/movielens-100k-seeds42-44.json。  ranking classic multi-task mixture-of-experts 搜广推 学习信号、多任务与反馈偏差 PLE 相比 MMoE 的独立任务 gate，为什么还显式区分共享专家与任务专属专家？ MMoE 虽可为任务选择不同专家比例，但专家本身仍共同承受各任务梯度。PLE 给任务保留专属专家，同时保留共享专家，再通过逐层门控提取共性与差异，让冲突更强的知识有明确存放位置。它扩展了信息与梯度的隔离结构，代价是更多容量和路由选择；仍需验证是否减少此消彼长的任务退化。 示意：点击和购买可共享品类兴趣专家，购买专属专家学习价格承受能力，点击专属专家学习标题吸引力。门控逐层组合，而不要求全部专家都被两个任务共同改写。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ple" data-paper-title="Progressive Layered Extraction (PLE): A Novel Multi-Task Learning Model for Personalized Recommendations" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Progressive Layered Extraction (PLE): A Novel Multi-Task Learning Model for Personalized Recommendations 搜广推与 LLM 应用 Tencent 2020-09-22 MMoE 仍让所有 experts 在所有任务间共享，任务冲突强时难以同时保留共性与个性。PLE 将 experts 分成共享组和任务专属组，通过 CGC 门控逐层提取共享与特定信息，减少跷跷板现象。 复现级别：核心机制复现。复现级别：核心机制复现。实际训练共享/任务专属 experts、CGC gates 和独立 heads；腾讯视频生产规模未复刻。本地对照口径：基线为 MMoE，实验组为共享与任务专属 experts 的 CGC/PLE；平均任务 AUC 相对 +1.34%，见 metrics/movielens-100k-seeds42-44.json。  ranking classic multi-task mixture-of-experts 搜广推 学习信号、多任务与反馈偏差 PLE 相比增加 MMoE 专家数量，为什么不是纯参数量扩大？ MMoE 更多专家仍可被所有任务共同更新，PLE 限制任务专属组的访问与梯度范围，再分层融合。改变的是共享拓扑而不仅数量，公平比较需匹配预算。来源本地对 MMoE 是具体两任务构造，不能外推所有冲突都消失。 示意：再加十个所有任务都用的专家，购买仍可能被点击梯度干扰；留出购买私有组则明确减少这条干扰路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4cfe1ebe206d5bfb">PLE 相比增加 MMoE 专家数量，为什么不是纯参数量扩大？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aple">Progressive Layered Extraction (PLE): A Novel Multi-Task Learning Model for Personalized Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>MMoE 更多专家仍可被所有任务共同更新，PLE 限制任务专属组的访问与梯度范围，再分层融合。改变的是共享拓扑而不仅数量，公平比较需匹配预算。来源本地对 MMoE 是具体两任务构造，不能外推所有冲突都消失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>再加十个所有任务都用的专家，购买仍可能被点击梯度干扰；留出购买私有组则明确减少这条干扰路径。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://doi.org/10.1145/3383313.3412236">原论文</a> · <a href="../../../../reproductions/recsys2020-ple-ple/">实现解读</a> · <a href="#qa-4cfe1ebe206d5bfb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ple" data-paper-title="Progressive Layered Extraction (PLE): A Novel Multi-Task Learning Model for Personalized Recommendations" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Progressive Layered Extraction (PLE): A Novel Multi-Task Learning Model for Personalized Recommendations 搜广推与 LLM 应用 Tencent 2020-09-22 MMoE 仍让所有 experts 在所有任务间共享，任务冲突强时难以同时保留共性与个性。PLE 将 experts 分成共享组和任务专属组，通过 CGC 门控逐层提取共享与特定信息，减少跷跷板现象。 复现级别：核心机制复现。复现级别：核心机制复现。实际训练共享/任务专属 experts、CGC gates 和独立 heads；腾讯视频生产规模未复刻。本地对照口径：基线为 MMoE，实验组为共享与任务专属 experts 的 CGC/PLE；平均任务 AUC 相对 +1.34%，见 metrics/movielens-100k-seeds42-44.json。  ranking classic multi-task mixture-of-experts 搜广推 学习信号、多任务与反馈偏差 PLE 各任务 gate 为什么只能看自己的专属组与共享组？ 这是 CGC 的分工约束，若 gate 混入其他任务私有专家，就改变隔离结构。需核对专家身份、路由 mask 和实际梯度，不能只靠对象名字 private。逐层输出到下一层的通道布局也应一致，避免隐式串错任务。 示意：点击 gate 不应直接使用购买私有专家；若代码把所有专家 concat 后无 mask，虽然输出维度对，却已退回更接近全共享混合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-433f6282251197a2">PLE 各任务 gate 为什么只能看自己的专属组与共享组？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aple">Progressive Layered Extraction (PLE): A Novel Multi-Task Learning Model for Personalized Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这是 CGC 的分工约束，若 gate 混入其他任务私有专家，就改变隔离结构。需核对专家身份、路由 mask 和实际梯度，不能只靠对象名字 private。逐层输出到下一层的通道布局也应一致，避免隐式串错任务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>点击 gate 不应直接使用购买私有专家；若代码把所有专家 concat 后无 mask，虽然输出维度对，却已退回更接近全共享混合。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://doi.org/10.1145/3383313.3412236">原论文</a> · <a href="../../../../reproductions/recsys2020-ple-ple/">实现解读</a> · <a href="#qa-433f6282251197a2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mmoe" data-paper-title="Modeling Task Relationships in Multi-task Learning with Multi-gate Mixture-of-Experts" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Modeling Task Relationships in Multi-task Learning with Multi-gate Mixture-of-Experts 搜广推与 LLM 应用 Google 2018-08-19 共享底座的多任务模型会在任务相关性较低时产生负迁移。完全独立的模型又无法利用共性。MMoE 建立一组共享专家，但为每个任务学习独立 softmax gate，让任务以不同权重组合专家。 复现级别：核心机制复现。复现级别：核心机制复现。实际训练共享 experts、任务专属 gates 与任务 heads；Google 私有业务特征未复刻。本地对照口径：基线为 shared-bottom 双任务网络，实验组为每任务独立 gate 的共享 experts；平均任务 AUC 相对 +1.30%，见 metrics/movielens-100k-seeds42-44.json。  ranking classic multi-task mixture-of-experts 搜广推 学习信号、多任务与反馈偏差 MMoE 的“专家共享、gate 私有”意味着每个任务能完全独立吗？ 任务共享专家参数，因此仍会通过专家梯度互相影响；私有 gate 只让使用比例不同，任务头再负责各自输出。它介于全共享和全独立之间，并不彻底隔离负迁移。专家分工应从实际路由与任务结果检查，不能按模块名字推断。 示意：点击和购买都用同一价格专家但比例不同，点击训练仍会更新这位专家，因此购买任务并非完全不受点击梯度影响。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-mmoe-a1bda9df" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7894d7d31049945b">MMoE 的“专家共享、gate 私有”意味着每个任务能完全独立吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ammoe">Modeling Task Relationships in Multi-task Learning with Multi-gate Mixture-of-Experts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>任务共享专家参数，因此仍会通过专家梯度互相影响；私有 gate 只让使用比例不同，任务头再负责各自输出。它介于全共享和全独立之间，并不彻底隔离负迁移。专家分工应从实际路由与任务结果检查，不能按模块名字推断。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>点击和购买都用同一价格专家但比例不同，点击训练仍会更新这位专家，因此购买任务并非完全不受点击梯度影响。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://research.google/pubs/modeling-task-relationships-in-multi-task-learning-with-multi-gate-mixture-of-experts/">原论文</a> · <a href="../../../../reproductions/kdd2018-mmoe-mmoe/">实现解读</a> · <a href="#qa-7894d7d31049945b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mmoe" data-paper-title="Modeling Task Relationships in Multi-task Learning with Multi-gate Mixture-of-Experts" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Modeling Task Relationships in Multi-task Learning with Multi-gate Mixture-of-Experts 搜广推与 LLM 应用 Google 2018-08-19 共享底座的多任务模型会在任务相关性较低时产生负迁移。完全独立的模型又无法利用共性。MMoE 建立一组共享专家，但为每个任务学习独立 softmax gate，让任务以不同权重组合专家。 复现级别：核心机制复现。复现级别：核心机制复现。实际训练共享 experts、任务专属 gates 与任务 heads；Google 私有业务特征未复刻。本地对照口径：基线为 shared-bottom 双任务网络，实验组为每任务独立 gate 的共享 experts；平均任务 AUC 相对 +1.30%，见 metrics/movielens-100k-seeds42-44.json。  ranking classic multi-task mixture-of-experts 搜广推 学习信号、多任务与反馈偏差 MMoE 共享专家却为每个任务单独设 gate，为什么能缓解共享底座的负迁移？ 共享底座要求任务使用同一份中间表示，目标冲突时梯度会相互拉扯。MMoE 保留一组可共同训练的专家，但每个任务用自己的 gate 按输入组合专家，使相关任务共享有用部分，不相关任务走不同组合。它提供软分工的自由度，并不保证专家天然对应可解释语义或完全消除冲突。 示意：点击与购买都可使用“品类偏好”专家，但购买任务可更重视价格专家，点击任务更重视新鲜感专家。两个任务共享知识，同时避免只能接受同一种混合比例。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mmoe" data-paper-title="Modeling Task Relationships in Multi-task Learning with Multi-gate Mixture-of-Experts" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Modeling Task Relationships in Multi-task Learning with Multi-gate Mixture-of-Experts 搜广推与 LLM 应用 Google 2018-08-19 共享底座的多任务模型会在任务相关性较低时产生负迁移。完全独立的模型又无法利用共性。MMoE 建立一组共享专家，但为每个任务学习独立 softmax gate，让任务以不同权重组合专家。 复现级别：核心机制复现。复现级别：核心机制复现。实际训练共享 experts、任务专属 gates 与任务 heads；Google 私有业务特征未复刻。本地对照口径：基线为 shared-bottom 双任务网络，实验组为每任务独立 gate 的共享 experts；平均任务 AUC 相对 +1.30%，见 metrics/movielens-100k-seeds42-44.json。  ranking classic multi-task mixture-of-experts 搜广推 学习信号、多任务与反馈偏差 MMoE 与单共享底座及每任务独立网络，分别在什么地方折中？ 单底座只提供一份共享表示，独立网络完全不交换参数，MMoE 给一组公共表征再让任务条件化组合。增加专家可提高共享灵活性，也增加计算与路由塌缩风险。任务相关性和数据量决定适合程度，不能保证比两端方案都好。 示意：两个任务可共用基础兴趣专家，各自重视另一专长；若目标毫不相关，仍强共用可能受损，若数据很少，完全独立又可能学不稳。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-08ebd1aca483e5d1">MMoE 与单共享底座及每任务独立网络，分别在什么地方折中？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ammoe">Modeling Task Relationships in Multi-task Learning with Multi-gate Mixture-of-Experts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单底座只提供一份共享表示，独立网络完全不交换参数，MMoE 给一组公共表征再让任务条件化组合。增加专家可提高共享灵活性，也增加计算与路由塌缩风险。任务相关性和数据量决定适合程度，不能保证比两端方案都好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个任务可共用基础兴趣专家，各自重视另一专长；若目标毫不相关，仍强共用可能受损，若数据很少，完全独立又可能学不稳。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://research.google/pubs/modeling-task-relationships-in-multi-task-learning-with-multi-gate-mixture-of-experts/">原论文</a> · <a href="../../../../reproductions/kdd2018-mmoe-mmoe/">实现解读</a> · <a href="#qa-08ebd1aca483e5d1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mmoe" data-paper-title="Modeling Task Relationships in Multi-task Learning with Multi-gate Mixture-of-Experts" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Modeling Task Relationships in Multi-task Learning with Multi-gate Mixture-of-Experts 搜广推与 LLM 应用 Google 2018-08-19 共享底座的多任务模型会在任务相关性较低时产生负迁移。完全独立的模型又无法利用共性。MMoE 建立一组共享专家，但为每个任务学习独立 softmax gate，让任务以不同权重组合专家。 复现级别：核心机制复现。复现级别：核心机制复现。实际训练共享 experts、任务专属 gates 与任务 heads；Google 私有业务特征未复刻。本地对照口径：基线为 shared-bottom 双任务网络，实验组为每任务独立 gate 的共享 experts；平均任务 AUC 相对 +1.30%，见 metrics/movielens-100k-seeds42-44.json。  ranking classic multi-task mixture-of-experts 搜广推 学习信号、多任务与反馈偏差 MMoE gate 的 softmax 为什么沿专家轴，四专家和两任务应产生几套权重？ 每个任务对每个样本生成四个专家权重并归一，两任务各有独立 gate，专家输出在同空间加权。若将任务轴一起归一，会强迫任务争夺总预算，改变模型。来源本地四专家两头的对照是 shared-bottom，而非任意跨论文模型。 示意：一名用户需要点击权重一组、购买权重另一组，各自和为一；把八个数合起来归一会让购买增加权重时无端降低点击表示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c6a76388ad05af8a">MMoE gate 的 softmax 为什么沿专家轴，四专家和两任务应产生几套权重？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ammoe">Modeling Task Relationships in Multi-task Learning with Multi-gate Mixture-of-Experts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每个任务对每个样本生成四个专家权重并归一，两任务各有独立 gate，专家输出在同空间加权。若将任务轴一起归一，会强迫任务争夺总预算，改变模型。来源本地四专家两头的对照是 shared-bottom，而非任意跨论文模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一名用户需要点击权重一组、购买权重另一组，各自和为一；把八个数合起来归一会让购买增加权重时无端降低点击表示。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://research.google/pubs/modeling-task-relationships-in-multi-task-learning-with-multi-gate-mixture-of-experts/">原论文</a> · <a href="../../../../reproductions/kdd2018-mmoe-mmoe/">实现解读</a> · <a href="#qa-c6a76388ad05af8a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:esmm" data-paper-title="Entire Space Multi-Task Model: An Effective Approach for Estimating Post-Click Conversion Rate" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Entire Space Multi-Task Model: An Effective Approach for Estimating Post-Click Conversion Rate 搜广推与 LLM 应用 Alibaba 2018-04-21 CVR 只在点击样本上可观测，直接训练会遭遇 sample-selection bias；转化又远比点击稀疏。ESMM 在全曝光空间同时学习 CTR 与 CVR，并用概率链式分解得到 CTCVR。CTR 的稠密监督帮助 CVR tower 学到更稳定的表示。 复现级别：核心机制复现。复现级别：核心机制复现。实际执行 CTR/CVR 双塔、概率乘积与 entire-space loss；淘宝私有漏斗数据由公开数据构造替代。本地对照口径：基线只在 clicked space 训练 CVR，实验组在 entire space 联合 CTR 与 CTCVR；平均任务 AUC 相对 +1.69%，见 metrics/movielens-100k-seeds42-44.json。  ranking classic multi-task conversion 搜广推 学习信号、多任务与反馈偏差 ESMM 的 CTCVR 标签为什么可对全曝光定义，条件 CVR 却不一样？ 未点击曝光不属于“点击且转化”，联合标签为零可知；但如果它被点击是否转化并未观察，所以不能直接给条件 CVR 置零。CTR 与 CVR 乘积连接两者，使用全空间联合监督。该链式关系依赖点击后转化定义，不能用于任意非嵌套反馈。 示意：用户没点广告，知道这次没有点击后购买，却不知道假如点击会不会买；两者条件不同，给 CVR 头直接负例会混淆它们。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<span id="paper-recommendation-esmm-4cd7f113" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-be460592e37829a5">ESMM 的 CTCVR 标签为什么可对全曝光定义，条件 CVR 却不一样？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aesmm">Entire Space Multi-Task Model: An Effective Approach for Estimating Post-Click Conversion Rate</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>未点击曝光不属于“点击且转化”，联合标签为零可知；但如果它被点击是否转化并未观察，所以不能直接给条件 CVR 置零。CTR 与 CVR 乘积连接两者，使用全空间联合监督。该链式关系依赖点击后转化定义，不能用于任意非嵌套反馈。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户没点广告，知道这次没有点击后购买，却不知道假如点击会不会买；两者条件不同，给 CVR 头直接负例会混淆它们。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1804.07931">原论文</a> · <a href="../../../../reproductions/1804.07931-esmm/">实现解读</a> · <a href="#qa-be460592e37829a5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:esmm" data-paper-title="Entire Space Multi-Task Model: An Effective Approach for Estimating Post-Click Conversion Rate" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Entire Space Multi-Task Model: An Effective Approach for Estimating Post-Click Conversion Rate 搜广推与 LLM 应用 Alibaba 2018-04-21 CVR 只在点击样本上可观测，直接训练会遭遇 sample-selection bias；转化又远比点击稀疏。ESMM 在全曝光空间同时学习 CTR 与 CVR，并用概率链式分解得到 CTCVR。CTR 的稠密监督帮助 CVR tower 学到更稳定的表示。 复现级别：核心机制复现。复现级别：核心机制复现。实际执行 CTR/CVR 双塔、概率乘积与 entire-space loss；淘宝私有漏斗数据由公开数据构造替代。本地对照口径：基线只在 clicked space 训练 CVR，实验组在 entire space 联合 CTR 与 CTCVR；平均任务 AUC 相对 +1.69%，见 metrics/movielens-100k-seeds42-44.json。  ranking classic multi-task conversion 搜广推 学习信号、多任务与反馈偏差 ESMM为什么训练CTR和CTCVR，却不把未点击样本直接当作CVR负例？ CVR是点击条件下的转化概率，未点击并不能告诉我们点击后会不会买。ESMM用CTR与CVR的乘积表示曝光后点击且转化概率，在全曝光空间监督CTR和联合事件，借漏斗关系缓解稀疏与选择偏差。链式分解是概率关系，不意味着模型自动解决所有归因、延迟反馈或因果识别问题。 示意：点击率10%、点击后购买率20%对应联合率2%；某次未点击只提供点击和联合事件的零标签，不能因此断言这位用户点击后一定不会购买。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:esmm" data-paper-title="Entire Space Multi-Task Model: An Effective Approach for Estimating Post-Click Conversion Rate" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Entire Space Multi-Task Model: An Effective Approach for Estimating Post-Click Conversion Rate 搜广推与 LLM 应用 Alibaba 2018-04-21 CVR 只在点击样本上可观测，直接训练会遭遇 sample-selection bias；转化又远比点击稀疏。ESMM 在全曝光空间同时学习 CTR 与 CVR，并用概率链式分解得到 CTCVR。CTR 的稠密监督帮助 CVR tower 学到更稳定的表示。 复现级别：核心机制复现。复现级别：核心机制复现。实际执行 CTR/CVR 双塔、概率乘积与 entire-space loss；淘宝私有漏斗数据由公开数据构造替代。本地对照口径：基线只在 clicked space 训练 CVR，实验组在 entire space 联合 CTR 与 CTCVR；平均任务 AUC 相对 +1.69%，见 metrics/movielens-100k-seeds42-44.json。  ranking classic multi-task conversion 搜广推 学习信号、多任务与反馈偏差 ESMM 相比只在 clicked space 学 CVR，补充了哪些曝光信息？ 点击子集受旧策略与用户选择影响，不能完整代表曝光分布。全空间 CTR 与 CTCVR 让未点击样本也约束联合行为，并用共享表示帮助稀疏转化。它不自动解决延迟反馈和全部未观测混杂，整体 AUC 也不证明因果 CVR 已识别。 示意：只从点击贵手机的人学购买，难泛化到所有曝光；全空间目标补充被略过商品信号，但仍没直接观察每件商品被点击后的反事实。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5d59e37d79697e99">ESMM 相比只在 clicked space 学 CVR，补充了哪些曝光信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aesmm">Entire Space Multi-Task Model: An Effective Approach for Estimating Post-Click Conversion Rate</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>点击子集受旧策略与用户选择影响，不能完整代表曝光分布。全空间 CTR 与 CTCVR 让未点击样本也约束联合行为，并用共享表示帮助稀疏转化。它不自动解决延迟反馈和全部未观测混杂，整体 AUC 也不证明因果 CVR 已识别。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>只从点击贵手机的人学购买，难泛化到所有曝光；全空间目标补充被略过商品信号，但仍没直接观察每件商品被点击后的反事实。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1804.07931">原论文</a> · <a href="../../../../reproductions/1804.07931-esmm/">实现解读</a> · <a href="#qa-5d59e37d79697e99">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:esmm" data-paper-title="Entire Space Multi-Task Model: An Effective Approach for Estimating Post-Click Conversion Rate" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/feedback-multitask-causality" data-search="Entire Space Multi-Task Model: An Effective Approach for Estimating Post-Click Conversion Rate 搜广推与 LLM 应用 Alibaba 2018-04-21 CVR 只在点击样本上可观测，直接训练会遭遇 sample-selection bias；转化又远比点击稀疏。ESMM 在全曝光空间同时学习 CTR 与 CVR，并用概率链式分解得到 CTCVR。CTR 的稠密监督帮助 CVR tower 学到更稳定的表示。 复现级别：核心机制复现。复现级别：核心机制复现。实际执行 CTR/CVR 双塔、概率乘积与 entire-space loss；淘宝私有漏斗数据由公开数据构造替代。本地对照口径：基线只在 clicked space 训练 CVR，实验组在 entire space 联合 CTR 与 CTCVR；平均任务 AUC 相对 +1.69%，见 metrics/movielens-100k-seeds42-44.json。  ranking classic multi-task conversion 搜广推 学习信号、多任务与反馈偏差 ESMM 实现时，未点击样本应进入哪个损失而不能直接监督哪个头？ CTR 头接受全曝光点击标签，CTR×CVR 的联合概率接受全曝光 CTCVR 标签；不能再把所有未点击样本当直接 CVR 负例。来源本地用评分阈值构造嵌套事件，只能验证这条训练连接，不等于真实广告转化场景复现。 示意：未点击样本可压低联合概率，模型也可通过低 CTR 解释；若强迫 CVR 同时为零，就额外添加了没有观察支持的条件标签。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 学习信号、多任务与反馈偏差</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-66950367b1602236">ESMM 实现时，未点击样本应进入哪个损失而不能直接监督哪个头？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aesmm">Entire Space Multi-Task Model: An Effective Approach for Estimating Post-Click Conversion Rate</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>CTR 头接受全曝光点击标签，CTR×CVR 的联合概率接受全曝光 CTCVR 标签；不能再把所有未点击样本当直接 CVR 负例。来源本地用评分阈值构造嵌套事件，只能验证这条训练连接，不等于真实广告转化场景复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>未点击样本可压低联合概率，模型也可通过低 CTR 解释；若强迫 CVR 同时为零，就额外添加了没有观察支持的条件标签。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1804.07931">原论文</a> · <a href="../../../../reproductions/1804.07931-esmm/">实现解读</a> · <a href="#qa-66950367b1602236">问题链接</a></p>
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
