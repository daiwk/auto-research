---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 视觉世界建模：状态、生成与动作条件

[多模态](index.md) / 88 个问题 · 22 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

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
<p class="ar-learning-status" data-learning-status role="status">88 个问题 · 22 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:dt-jepa" data-paper-title="DT-JEPA: Learning to Predict Future Representations for Decision-Making" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="DT-JEPA: Learning to Predict Future Representations for Decision-Making 基础模型 Southeast University 2026-10-23 传统DT用单个return-to-go条件，无法区分回报相同但未来动力学不同的轨迹。本方法将条件改成由历史预测的未来latent分布：历史encoder生成Gaussian参数，EMA target encoder只在训练期编码真实未来；重参数采样的预测未来通过独立gamma/beta MLP调制DT hidden。离线目标为BC加Gaussian NLL；在线通过双target critic的较小值构建多步target，并优化Q1指导的actor目标。 成本过高，不复现（审查 DONE）。D4RL共19个locomotion/navigation数据配置、主表5种子、多个未见reward的在线适配及基线/消融；附录DT4层/4头/512hidden、batch256/context20。原文未给总GPU小时，不臆测。完整offline+online矩阵超单卡短时预算，不安装MuJoCo、不下载轨迹、不启动环境试跑。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  JEPA与世界模型 未来表征与离线决策 多模态 视觉世界建模：状态、生成与动作条件 DT-JEPA 的未来 latent 条件与 return-to-go 表达的信息有何不同？ return-to-go 是一个累计回报量，相同数值可对应不同未来动力学；预测未来 latent 则用历史生成分布，尝试描述可能到达的未来状态。部署只从可观察历史预测，并非读取真实未来；latent 也不保证天然包含任务所需全部信息。 例如绕障碍左走和右走可能回报相同，但未来位置不同；分布式未来条件可表达这种差别，而单个回报数难以区分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-dt-jepa-898e3cdc" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-656e6bff07c6b2fa">DT-JEPA 的未来 latent 条件与 return-to-go 表达的信息有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adt-jepa">DT-JEPA: Learning to Predict Future Representations for Decision-Making</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Southeast University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>return-to-go 是一个累计回报量，相同数值可对应不同未来动力学；预测未来 latent 则用历史生成分布，尝试描述可能到达的未来状态。部署只从可观察历史预测，并非读取真实未来；latent 也不保证天然包含任务所需全部信息。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如绕障碍左走和右走可能回报相同，但未来位置不同；分布式未来条件可表达这种差别，而单个回报数难以区分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32657v1">原论文</a> · <a href="../../../../foundation-models/2610.32657-dt-jepa/">实现解读</a> · <a href="#qa-656e6bff07c6b2fa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:dt-jepa" data-paper-title="DT-JEPA: Learning to Predict Future Representations for Decision-Making" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="DT-JEPA: Learning to Predict Future Representations for Decision-Making 基础模型 Southeast University 2026-10-23 传统DT用单个return-to-go条件，无法区分回报相同但未来动力学不同的轨迹。本方法将条件改成由历史预测的未来latent分布：历史encoder生成Gaussian参数，EMA target encoder只在训练期编码真实未来；重参数采样的预测未来通过独立gamma/beta MLP调制DT hidden。离线目标为BC加Gaussian NLL；在线通过双target critic的较小值构建多步target，并优化Q1指导的actor目标。 成本过高，不复现（审查 DONE）。D4RL共19个locomotion/navigation数据配置、主表5种子、多个未见reward的在线适配及基线/消融；附录DT4层/4头/512hidden、batch256/context20。原文未给总GPU小时，不臆测。完整offline+online矩阵超单卡短时预算，不安装MuJoCo、不下载轨迹、不启动环境试跑。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  JEPA与世界模型 未来表征与离线决策 多模态 视觉世界建模：状态、生成与动作条件 为什么未来 latent 要由历史预测，而真实未来只交给训练期的目标编码器？ 决策时真实未来尚未发生，直接用它作条件会造成泄漏。历史编码器预测未来分布，并通过重参数采样得到决策条件；EMA 目标只提供训练对齐信号。相同回报可能对应不同动力学，未来表征尝试补足单一 return-to-go 无法区分的信息。 例如两条轨迹都得十分，但一条将撞到障碍、另一条可通行；预测未来状态比仅给“目标十分”更能区分后续选择。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-07079ed5e9b5243c">为什么未来 latent 要由历史预测，而真实未来只交给训练期的目标编码器？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adt-jepa">DT-JEPA: Learning to Predict Future Representations for Decision-Making</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Southeast University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>决策时真实未来尚未发生，直接用它作条件会造成泄漏。历史编码器预测未来分布，并通过重参数采样得到决策条件；EMA 目标只提供训练对齐信号。相同回报可能对应不同动力学，未来表征尝试补足单一 return-to-go 无法区分的信息。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两条轨迹都得十分，但一条将撞到障碍、另一条可通行；预测未来状态比仅给“目标十分”更能区分后续选择。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32657v1">原论文</a> · <a href="../../../../foundation-models/2610.32657-dt-jepa/">实现解读</a> · <a href="#qa-07079ed5e9b5243c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:dt-jepa" data-paper-title="DT-JEPA: Learning to Predict Future Representations for Decision-Making" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="DT-JEPA: Learning to Predict Future Representations for Decision-Making 基础模型 Southeast University 2026-10-23 传统DT用单个return-to-go条件，无法区分回报相同但未来动力学不同的轨迹。本方法将条件改成由历史预测的未来latent分布：历史encoder生成Gaussian参数，EMA target encoder只在训练期编码真实未来；重参数采样的预测未来通过独立gamma/beta MLP调制DT hidden。离线目标为BC加Gaussian NLL；在线通过双target critic的较小值构建多步target，并优化Q1指导的actor目标。 成本过高，不复现（审查 DONE）。D4RL共19个locomotion/navigation数据配置、主表5种子、多个未见reward的在线适配及基线/消融；附录DT4层/4头/512hidden、batch256/context20。原文未给总GPU小时，不臆测。完整offline+online矩阵超单卡短时预算，不安装MuJoCo、不下载轨迹、不启动环境试跑。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  JEPA与世界模型 未来表征与离线决策 多模态 视觉世界建模：状态、生成与动作条件 预测高斯分布与直接用一个确定未来向量，有何建模取舍？ 高斯均值与方差允许表示不确定性，再经重参数采样调制 DT；确定向量只提供一个点条件。分布形式增加可训练的不确定性表达，但受对角高斯假设限制，不能因此声称可完整覆盖多峰未来，也不能把训练真实未来输入部署前向。 例如两条路都可能成功时，方差可反映预测不确定；但两个相距很远的离散目标未必能被单一高斯精确表达。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4edbb4e720f6808c">预测高斯分布与直接用一个确定未来向量，有何建模取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adt-jepa">DT-JEPA: Learning to Predict Future Representations for Decision-Making</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Southeast University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>高斯均值与方差允许表示不确定性，再经重参数采样调制 DT；确定向量只提供一个点条件。分布形式增加可训练的不确定性表达，但受对角高斯假设限制，不能因此声称可完整覆盖多峰未来，也不能把训练真实未来输入部署前向。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两条路都可能成功时，方差可反映预测不确定；但两个相距很远的离散目标未必能被单一高斯精确表达。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32657v1">原论文</a> · <a href="../../../../foundation-models/2610.32657-dt-jepa/">实现解读</a> · <a href="#qa-4edbb4e720f6808c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:dt-jepa" data-paper-title="DT-JEPA: Learning to Predict Future Representations for Decision-Making" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="DT-JEPA: Learning to Predict Future Representations for Decision-Making 基础模型 Southeast University 2026-10-23 传统DT用单个return-to-go条件，无法区分回报相同但未来动力学不同的轨迹。本方法将条件改成由历史预测的未来latent分布：历史encoder生成Gaussian参数，EMA target encoder只在训练期编码真实未来；重参数采样的预测未来通过独立gamma/beta MLP调制DT hidden。离线目标为BC加Gaussian NLL；在线通过双target critic的较小值构建多步target，并优化Q1指导的actor目标。 成本过高，不复现（审查 DONE）。D4RL共19个locomotion/navigation数据配置、主表5种子、多个未见reward的在线适配及基线/消融；附录DT4层/4头/512hidden、batch256/context20。原文未给总GPU小时，不臆测。完整offline+online矩阵超单卡短时预算，不安装MuJoCo、不下载轨迹、不启动环境试跑。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  JEPA与世界模型 未来表征与离线决策 多模态 视觉世界建模：状态、生成与动作条件 NLL、BC 与 critic 的归约能都改成通用 MSE.mean 吗？ 不能。NLL 对 latent 维求和后批平均，BC 与 critic 对时间和动作维求和后批平均；归约改变会隐式改变损失相对权重。target 与 TD bootstrap 停止梯度，但 actor 的 Q 对动作梯度需保留，本地仅验证这些组件，不包含完整在线环境收集。 例如动作维翻倍时，全元素均值会缩小单样本总贡献；若其他项仍按维求和，原有权重关系就发生变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-92f993e968b93b89">NLL、BC 与 critic 的归约能都改成通用 MSE.mean 吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adt-jepa">DT-JEPA: Learning to Predict Future Representations for Decision-Making</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Southeast University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。NLL 对 latent 维求和后批平均，BC 与 critic 对时间和动作维求和后批平均；归约改变会隐式改变损失相对权重。target 与 TD bootstrap 停止梯度，但 actor 的 Q 对动作梯度需保留，本地仅验证这些组件，不包含完整在线环境收集。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如动作维翻倍时，全元素均值会缩小单样本总贡献；若其他项仍按维求和，原有权重关系就发生变化。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32657v1">原论文</a> · <a href="../../../../foundation-models/2610.32657-dt-jepa/">实现解读</a> · <a href="#qa-92f993e968b93b89">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:uniaction" data-paper-title="UniAction: Unified Action Conditioning for World Models" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="UniAction: Unified Action Conditioning for World Models 多模态大模型 Stanford University 2026-10-23 异质动作以不同粒度编码，token较多的动作在同一softmax中会仅因数量而占据更大attention mass。UniAction以共享semantic codebook编码元素身份，将(t,y,x)送入既有视频模型的native positional mechanism，再对action部分统一加一个基数bias，保持action内部相对logits不变，同时移除总mass对Na的线性依赖。 成本过高，不复现（审查 DONE）。诊断回调仅证明参数传递，不能当成真实视频backbone位置实现。Wan2.2-I2V-A14B high-noise expert LoRA，GoalForce/SolarWM/EgoDex/DROID各10K clips，共40K段81帧480×832；410反事实生成、多个motion/pose估计器、4个专家和100人评测。完整视频训练/生成显著超过单A100/A30短时资源，不下载14B权重或40K视频，不试跑成本。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  世界模型与动作条件 统一动作表示 多模态 视觉世界建模：状态、生成与动作条件 动作 token 数量为何会影响联合注意力，即使每个 token 相似度没变？ softmax 对所有视觉与动作 logits 一起归一化，同类动作 token 更多会增加它们的总指数权重，仅靠数量就改变总注意力。UniAction 给动作部分加入基数校正，试图去除这种线性数量效应，同时保留动作内部相对分数，而不是把所有动作平均成一个 token。 例如同一动作表示复制四次，未经校正时总权重会变大，模型可能因此比只放一次更偏向动作信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-multimodal-models-uniaction-704ab058" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-22a1c4fa397b7c64">动作 token 数量为何会影响联合注意力，即使每个 token 相似度没变？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Auniaction">UniAction: Unified Action Conditioning for World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>softmax 对所有视觉与动作 logits 一起归一化，同类动作 token 更多会增加它们的总指数权重，仅靠数量就改变总注意力。UniAction 给动作部分加入基数校正，试图去除这种线性数量效应，同时保留动作内部相对分数，而不是把所有动作平均成一个 token。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一动作表示复制四次，未经校正时总权重会变大，模型可能因此比只放一次更偏向动作信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32977v1">原论文</a> · <a href="../../../../multimodal-models/2610.32977-uniaction/">实现解读</a> · <a href="#qa-22a1c4fa397b7c64">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:uniaction" data-paper-title="UniAction: Unified Action Conditioning for World Models" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="UniAction: Unified Action Conditioning for World Models 多模态大模型 Stanford University 2026-10-23 异质动作以不同粒度编码，token较多的动作在同一softmax中会仅因数量而占据更大attention mass。UniAction以共享semantic codebook编码元素身份，将(t,y,x)送入既有视频模型的native positional mechanism，再对action部分统一加一个基数bias，保持action内部相对logits不变，同时移除总mass对Na的线性依赖。 成本过高，不复现（审查 DONE）。诊断回调仅证明参数传递，不能当成真实视频backbone位置实现。Wan2.2-I2V-A14B high-noise expert LoRA，GoalForce/SolarWM/EgoDex/DROID各10K clips，共40K段81帧480×832；410反事实生成、多个motion/pose估计器、4个专家和100人评测。完整视频训练/生成显著超过单A100/A30短时资源，不下载14B权重或40K视频，不试跑成本。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  世界模型与动作条件 统一动作表示 多模态 视觉世界建模：状态、生成与动作条件 为什么给 action logits 加 log(Nref/Na)，能抵消完全复制动作 Token 带来的注意力总权重变化？ 同一联合 softmax 中，复制相同 key/value 且位置编码相同，会增加重复项的指数和，使 action 总权重仅因数量变大。数量对应的对数偏置抵消这种重复，同时保留 action 内相对 logits；加入不同内容或不同位置的动作仍可合理改变输出。 例如把每个动作 token 连位置表示一起复制两份，未经校正动作会更占权重；校正后不应仅凭重复份数改变结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-32b91700ff0ec00d">为什么给 action logits 加 log(Nref/Na)，能抵消完全复制动作 Token 带来的注意力总权重变化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Auniaction">UniAction: Unified Action Conditioning for World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一联合 softmax 中，复制相同 key/value 且位置编码相同，会增加重复项的指数和，使 action 总权重仅因数量变大。数量对应的对数偏置抵消这种重复，同时保留 action 内相对 logits；加入不同内容或不同位置的动作仍可合理改变输出。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把每个动作 token 连位置表示一起复制两份，未经校正动作会更占权重；校正后不应仅凭重复份数改变结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32977v1">原论文</a> · <a href="../../../../multimodal-models/2610.32977-uniaction/">实现解读</a> · <a href="#qa-32b91700ff0ec00d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:uniaction" data-paper-title="UniAction: Unified Action Conditioning for World Models" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="UniAction: Unified Action Conditioning for World Models 多模态大模型 Stanford University 2026-10-23 异质动作以不同粒度编码，token较多的动作在同一softmax中会仅因数量而占据更大attention mass。UniAction以共享semantic codebook编码元素身份，将(t,y,x)送入既有视频模型的native positional mechanism，再对action部分统一加一个基数bias，保持action内部相对logits不变，同时移除总mass对Na的线性依赖。 成本过高，不复现（审查 DONE）。诊断回调仅证明参数传递，不能当成真实视频backbone位置实现。Wan2.2-I2V-A14B high-noise expert LoRA，GoalForce/SolarWM/EgoDex/DROID各10K clips，共40K段81帧480×832；410反事实生成、多个motion/pose估计器、4个专家和100人评测。完整视频训练/生成显著超过单A100/A30短时资源，不下载14B权重或40K视频，不试跑成本。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  世界模型与动作条件 统一动作表示 多模态 视觉世界建模：状态、生成与动作条件 联合 softmax 校正与把视频、动作分别 softmax 后相加有何不同？ 联合 softmax 让两种信息在同一个归一化分母竞争，动作 logits 统一加 log(Nref/Na) 调节总量；分别归一化会各自总和为一，再相加形成另一种融合规则。两者即使动作内部排序相同，也不具有相同的跨模态权重。 例如视频证据很强、动作证据弱时，联合归一化可使动作总权重较小；分别归一化仍强行分配一整份动作权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-867e752facaab6ed">联合 softmax 校正与把视频、动作分别 softmax 后相加有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Auniaction">UniAction: Unified Action Conditioning for World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>联合 softmax 让两种信息在同一个归一化分母竞争，动作 logits 统一加 log(Nref/Na) 调节总量；分别归一化会各自总和为一，再相加形成另一种融合规则。两者即使动作内部排序相同，也不具有相同的跨模态权重。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如视频证据很强、动作证据弱时，联合归一化可使动作总权重较小；分别归一化仍强行分配一整份动作权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32977v1">原论文</a> · <a href="../../../../multimodal-models/2610.32977-uniaction/">实现解读</a> · <a href="#qa-867e752facaab6ed">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:uniaction" data-paper-title="UniAction: Unified Action Conditioning for World Models" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="UniAction: Unified Action Conditioning for World Models 多模态大模型 Stanford University 2026-10-23 异质动作以不同粒度编码，token较多的动作在同一softmax中会仅因数量而占据更大attention mass。UniAction以共享semantic codebook编码元素身份，将(t,y,x)送入既有视频模型的native positional mechanism，再对action部分统一加一个基数bias，保持action内部相对logits不变，同时移除总mass对Na的线性依赖。 成本过高，不复现（审查 DONE）。诊断回调仅证明参数传递，不能当成真实视频backbone位置实现。Wan2.2-I2V-A14B high-noise expert LoRA，GoalForce/SolarWM/EgoDex/DROID各10K clips，共40K段81帧480×832；410反事实生成、多个motion/pose估计器、4个专家和100人评测。完整视频训练/生成显著超过单A100/A30短时资源，不下载14B权重或40K视频，不试跑成本。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  世界模型与动作条件 统一动作表示 多模态 视觉世界建模：状态、生成与动作条件 复制不变性是否允许新增任意动作或改变位置编码？ 不允许。精确不变性要求复制的 key、value 及位置表示完全相同；不同新动作或不同位置可改变输出。Na 按每个请求的有效动作计数，padding 不计且 softmax 权重为零；native 位置回调必须显式提供，本地诊断回调不冒充 Wan 原生位置机制。 例如把同一动作复制到另一个时间点，位置表示变了就不再是完全复制，输出发生变化并不违反该不变性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0438a167c0dd745e">复制不变性是否允许新增任意动作或改变位置编码？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Auniaction">UniAction: Unified Action Conditioning for World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不允许。精确不变性要求复制的 key、value 及位置表示完全相同；不同新动作或不同位置可改变输出。Na 按每个请求的有效动作计数，padding 不计且 softmax 权重为零；native 位置回调必须显式提供，本地诊断回调不冒充 Wan 原生位置机制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把同一动作复制到另一个时间点，位置表示变了就不再是完全复制，输出发生变化并不违反该不变性。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32977v1">原论文</a> · <a href="../../../../multimodal-models/2610.32977-uniaction/">实现解读</a> · <a href="#qa-0438a167c0dd745e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:inside-jepa" data-paper-title="Inside-JEPA: From Prediction to Relational Grounding in Latent World Models" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Inside-JEPA: From Prediction to Relational Grounding in Latent World Models 基础模型 Australian Institute for Machine Learning, Adelaide University 2026-10-22 普通 JEPA 能预测潜在状态，但潜变量未必对应可解释关系。本文把每个有序实体对的关系通道直接拼入动态状态，并要求逆动态头根据前后关系通道恢复动作；预测损失的未来目标仍由 EMA 编码器提供，而逆动态的未来状态必须来自可反传的 online 编码器。仅预测、读全部状态、只读实体和打乱动作标签的对照用于区分信号来自哪里。原文 §3 该完整矩阵超出单 A100/A30/Mac 短时预算，成本过高，不复现（审查 DONE）；真实 crop、ResNet18、检测跟踪均由外部提供，当前未运行它们。RelationalStateEncoder 接收 [B,4,512] 冻结特征、[B,4,4] 归一化框、实体类型和共享实体 mask，本地组件每次调用最多64对帧；真实 crop、ResNet18、检测跟踪均由外部提供，当前未运行它们。InsideJEPA 实现预测器、可选离散/连续动作条件、五臂损失与显式 EMA 更新。  世界模型 JEPA 关系表示与逆动态 多模态 视觉世界建模：状态、生成与动作条件 为什么 Inside-JEPA 把有序实体对关系直接拼进动态状态？ 普通 latent 可能可预测却不易读出关系，显式关系通道让预测器与逆动态头能直接使用实体间结构。有序对区分 i 到 j 与 j 到 i，例如左于和右于不同；它提供关系归纳偏置，但二维框关系仍是几何代理，不等于理解三维接触或因果。 例如红块在蓝块左边与蓝块在红块左边不能共用同一方向关系值；有序对允许分别表示这两个命题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-inside-jepa-840eadf0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c81bf3ff739be368">为什么 Inside-JEPA 把有序实体对关系直接拼进动态状态？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ainside-jepa">Inside-JEPA: From Prediction to Relational Grounding in Latent World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Australian Institute for Machine Learning, Adelaide University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>普通 latent 可能可预测却不易读出关系，显式关系通道让预测器与逆动态头能直接使用实体间结构。有序对区分 i 到 j 与 j 到 i，例如左于和右于不同；它提供关系归纳偏置，但二维框关系仍是几何代理，不等于理解三维接触或因果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如红块在蓝块左边与蓝块在红块左边不能共用同一方向关系值；有序对允许分别表示这两个命题。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与五臂；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31194v1">原论文</a> · <a href="../../../../foundation-models/2610.31194-inside-jepa/">实现解读</a> · <a href="#qa-c81bf3ff739be368">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:inside-jepa" data-paper-title="Inside-JEPA: From Prediction to Relational Grounding in Latent World Models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Inside-JEPA: From Prediction to Relational Grounding in Latent World Models 基础模型 Australian Institute for Machine Learning, Adelaide University 2026-10-22 普通 JEPA 能预测潜在状态，但潜变量未必对应可解释关系。本文把每个有序实体对的关系通道直接拼入动态状态，并要求逆动态头根据前后关系通道恢复动作；预测损失的未来目标仍由 EMA 编码器提供，而逆动态的未来状态必须来自可反传的 online 编码器。仅预测、读全部状态、只读实体和打乱动作标签的对照用于区分信号来自哪里。原文 §3 该完整矩阵超出单 A100/A30/Mac 短时预算，成本过高，不复现（审查 DONE）；真实 crop、ResNet18、检测跟踪均由外部提供，当前未运行它们。RelationalStateEncoder 接收 [B,4,512] 冻结特征、[B,4,4] 归一化框、实体类型和共享实体 mask，本地组件每次调用最多64对帧；真实 crop、ResNet18、检测跟踪均由外部提供，当前未运行它们。InsideJEPA 实现预测器、可选离散/连续动作条件、五臂损失与显式 EMA 更新。  世界模型 JEPA 关系表示与逆动态 多模态 视觉世界建模：状态、生成与动作条件 为什么逆动态头的未来状态要来自可反传的 online 编码器，而非 EMA target？ 逆动态目标要把“哪些关系能解释动作”的信号传回表示层，若未来关系全停梯度，该侧就失去相应学习压力。JEPA 预测目标仍可使用稳定 EMA，但逆动态路径有不同梯度职责；还需通过只读实体、打乱动作等对照确认关系通道真正提供作用信息。 例如模型需根据移动前后的“杯子在盒子左侧”关系恢复动作；未来关系分支可反传，才能学会保留这种变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-098a3adf3f209998">为什么逆动态头的未来状态要来自可反传的 online 编码器，而非 EMA target？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ainside-jepa">Inside-JEPA: From Prediction to Relational Grounding in Latent World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Australian Institute for Machine Learning, Adelaide University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>逆动态目标要把“哪些关系能解释动作”的信号传回表示层，若未来关系全停梯度，该侧就失去相应学习压力。JEPA 预测目标仍可使用稳定 EMA，但逆动态路径有不同梯度职责；还需通过只读实体、打乱动作等对照确认关系通道真正提供作用信息。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型需根据移动前后的“杯子在盒子左侧”关系恢复动作；未来关系分支可反传，才能学会保留这种变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与五臂；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31194v1">原论文</a> · <a href="../../../../foundation-models/2610.31194-inside-jepa/">实现解读</a> · <a href="#qa-098a3adf3f209998">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:inside-jepa" data-paper-title="Inside-JEPA: From Prediction to Relational Grounding in Latent World Models" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Inside-JEPA: From Prediction to Relational Grounding in Latent World Models 基础模型 Australian Institute for Machine Learning, Adelaide University 2026-10-22 普通 JEPA 能预测潜在状态，但潜变量未必对应可解释关系。本文把每个有序实体对的关系通道直接拼入动态状态，并要求逆动态头根据前后关系通道恢复动作；预测损失的未来目标仍由 EMA 编码器提供，而逆动态的未来状态必须来自可反传的 online 编码器。仅预测、读全部状态、只读实体和打乱动作标签的对照用于区分信号来自哪里。原文 §3 该完整矩阵超出单 A100/A30/Mac 短时预算，成本过高，不复现（审查 DONE）；真实 crop、ResNet18、检测跟踪均由外部提供，当前未运行它们。RelationalStateEncoder 接收 [B,4,512] 冻结特征、[B,4,4] 归一化框、实体类型和共享实体 mask，本地组件每次调用最多64对帧；真实 crop、ResNet18、检测跟踪均由外部提供，当前未运行它们。InsideJEPA 实现预测器、可选离散/连续动作条件、五臂损失与显式 EMA 更新。  世界模型 JEPA 关系表示与逆动态 多模态 视觉世界建模：状态、生成与动作条件 INV-S、INV-R 与打乱标签控制分别用来区分什么信号？ INV-S 让逆动态只读关系通道，INV-R 只读实体 latent，可检查动作监督是否直接塑造关系；打乱标签臂只打乱 inverse 目标，而预测器仍读真实动作。它们是监督来源控制，不能简单将任意辅助头增益都解释为关系 grounding。 例如随机动作标签也能带来相似变化时，就需警惕收益来自一般正则而非正确动作与关系变化的对应。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-eec426b4717383d2">INV-S、INV-R 与打乱标签控制分别用来区分什么信号？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ainside-jepa">Inside-JEPA: From Prediction to Relational Grounding in Latent World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Australian Institute for Machine Learning, Adelaide University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>INV-S 让逆动态只读关系通道，INV-R 只读实体 latent，可检查动作监督是否直接塑造关系；打乱标签臂只打乱 inverse 目标，而预测器仍读真实动作。它们是监督来源控制，不能简单将任意辅助头增益都解释为关系 grounding。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如随机动作标签也能带来相似变化时，就需警惕收益来自一般正则而非正确动作与关系变化的对应。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与五臂；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31194v1">原论文</a> · <a href="../../../../foundation-models/2610.31194-inside-jepa/">实现解读</a> · <a href="#qa-eec426b4717383d2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:inside-jepa" data-paper-title="Inside-JEPA: From Prediction to Relational Grounding in Latent World Models" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Inside-JEPA: From Prediction to Relational Grounding in Latent World Models 基础模型 Australian Institute for Machine Learning, Adelaide University 2026-10-22 普通 JEPA 能预测潜在状态，但潜变量未必对应可解释关系。本文把每个有序实体对的关系通道直接拼入动态状态，并要求逆动态头根据前后关系通道恢复动作；预测损失的未来目标仍由 EMA 编码器提供，而逆动态的未来状态必须来自可反传的 online 编码器。仅预测、读全部状态、只读实体和打乱动作标签的对照用于区分信号来自哪里。原文 §3 该完整矩阵超出单 A100/A30/Mac 短时预算，成本过高，不复现（审查 DONE）；真实 crop、ResNet18、检测跟踪均由外部提供，当前未运行它们。RelationalStateEncoder 接收 [B,4,512] 冻结特征、[B,4,4] 归一化框、实体类型和共享实体 mask，本地组件每次调用最多64对帧；真实 crop、ResNet18、检测跟踪均由外部提供，当前未运行它们。InsideJEPA 实现预测器、可选离散/连续动作条件、五臂损失与显式 EMA 更新。  世界模型 JEPA 关系表示与逆动态 多模态 视觉世界建模：状态、生成与动作条件 四实体 K=8 的状态为什么是 256 维，而不是删对角后的 224 维？ 实体 latent 为 4×32，有序对槽为 4×4×8，合计 256；padding 和对角槽固定零但仍保留形状。JEPA 未来目标来自 EMA 并停止梯度，inverse 的未来状态必须来自可反传 online 编码器；将二者混用会切断定义性训练信号。 例如把对角关系值设零不会删除那三十二个槽；若顺手移除它们，预测器输入维度与论文合同就不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-37cda28a2170cf1f">四实体 K=8 的状态为什么是 256 维，而不是删对角后的 224 维？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ainside-jepa">Inside-JEPA: From Prediction to Relational Grounding in Latent World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Australian Institute for Machine Learning, Adelaide University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>实体 latent 为 4×32，有序对槽为 4×4×8，合计 256；padding 和对角槽固定零但仍保留形状。JEPA 未来目标来自 EMA 并停止梯度，inverse 的未来状态必须来自可反传 online 编码器；将二者混用会切断定义性训练信号。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把对角关系值设零不会删除那三十二个槽；若顺手移除它们，预测器输入维度与论文合同就不同。</p>
<p class="ar-learning-sources">依据：核心公式与五臂、本地复现与操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31194v1">原论文</a> · <a href="../../../../foundation-models/2610.31194-inside-jepa/">实现解读</a> · <a href="#qa-37cda28a2170cf1f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:alps" data-paper-title="ALPS: Visual State Encoders for World Models" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="ALPS: Visual State Encoders for World Models 基础模型 University of California, Santa Cruz 2026-10-21 世界模型以视觉 token 为状态进行预测和规划，但一个编码器通常只擅长物理状态、语言对齐或像素重建中的一部分。ALPS 尝试让同一组 patch token 同时承担三种接口：机器人状态探针能读出位置，文字指令能对应图像，而未来 token 能被解码成图像以便检查。第一阶段从零训练 ViT-B/16：同一组未做最终 LayerNorm 的 patch token接受图文对比、caption、自重建和密集跨裁剪对应四种监督。第二阶段将第一阶段 encoder 同时用作学生初始化和固定教师； 完整预训练和实验成本过高，不复现（审查 DONE），not_reproduced_high_cost 为终态，不下载大模型/训练数据、不试探性跑完整训练、不自动重试。诊断使用两组裁剪、patch、8 维 query 和 6 维随机 token。输入会检查 shape、有限值、正尺度、裁剪范围和标准差；不静默修正无效数据。模块导入不要求 torch，执行时才加载；不联网、不自动安装依赖、不执行上游脚本或下载 checkpoint。正式评测必须将训练统计与测试轨迹隔离，验证集选参，测试集只用于最终报告。  视觉表征与世界模型 联合嵌入与自监督学习 多模态 视觉世界建模：状态、生成与动作条件 ALPS 为什么要求同一组 patch token 同时服务状态、语言和像素接口？ 世界模型既需从视觉状态预测物理变化，也需对应文字指令并能检查预测图像。若三种用途使用互不关联的表示，规划接口可能难以协调；ALPS 通过多任务监督训练同一组未做最终 LayerNorm 的 patch token，但这不自动赋予时序动作理解。 例如一个物体的位置要能被状态探针读出，同时对应“把红块推过去”的文字，并支持把未来表示解码成画面检查。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-alps-4489dea8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-3824083e7eb834df">ALPS 为什么要求同一组 patch token 同时服务状态、语言和像素接口？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aalps">ALPS: Visual State Encoders for World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Santa Cruz</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>世界模型既需从视觉状态预测物理变化，也需对应文字指令并能检查预测图像。若三种用途使用互不关联的表示，规划接口可能难以协调；ALPS 通过多任务监督训练同一组未做最终 LayerNorm 的 patch token，但这不自动赋予时序动作理解。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个物体的位置要能被状态探针读出，同时对应“把红块推过去”的文字，并支持把未来表示解码成画面检查。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30120v1">原论文</a> · <a href="../../../../foundation-models/2610.30120-alps/">实现解读</a> · <a href="#qa-3824083e7eb834df">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:alps" data-paper-title="ALPS: Visual State Encoders for World Models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="ALPS: Visual State Encoders for World Models 基础模型 University of California, Santa Cruz 2026-10-21 世界模型以视觉 token 为状态进行预测和规划，但一个编码器通常只擅长物理状态、语言对齐或像素重建中的一部分。ALPS 尝试让同一组 patch token 同时承担三种接口：机器人状态探针能读出位置，文字指令能对应图像，而未来 token 能被解码成图像以便检查。第一阶段从零训练 ViT-B/16：同一组未做最终 LayerNorm 的 patch token接受图文对比、caption、自重建和密集跨裁剪对应四种监督。第二阶段将第一阶段 encoder 同时用作学生初始化和固定教师； 完整预训练和实验成本过高，不复现（审查 DONE），not_reproduced_high_cost 为终态，不下载大模型/训练数据、不试探性跑完整训练、不自动重试。诊断使用两组裁剪、patch、8 维 query 和 6 维随机 token。输入会检查 shape、有限值、正尺度、裁剪范围和标准差；不静默修正无效数据。模块导入不要求 torch，执行时才加载；不联网、不自动安装依赖、不执行上游脚本或下载 checkpoint。正式评测必须将训练统计与测试轨迹隔离，验证集选参，测试集只用于最终报告。  视觉表征与世界模型 联合嵌入与自监督学习 多模态 视觉世界建模：状态、生成与动作条件 第二阶段为什么只监督教师裁剪 B 中落在学生裁剪 A 内的 patch？ 学生只看得到 A，要求它逐点预测完全不在视野内的 B 区域会把不可见内容也当成确定监督。几何映射先找可对应位置，再预测固定教师的目标，外观增强则训练鲁棒表示；教师固定与学生初始化相同，不意味着训练中两者会一起更新。 例如学生只看到图片左半边，教师裁剪横跨左右；应只监督二者重叠部分，而不能要求学生精确读出右侧从未见到的小字。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8d4c87309e5eec26">第二阶段为什么只监督教师裁剪 B 中落在学生裁剪 A 内的 patch？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aalps">ALPS: Visual State Encoders for World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Santa Cruz</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>学生只看得到 A，要求它逐点预测完全不在视野内的 B 区域会把不可见内容也当成确定监督。几何映射先找可对应位置，再预测固定教师的目标，外观增强则训练鲁棒表示；教师固定与学生初始化相同，不意味着训练中两者会一起更新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生只看到图片左半边，教师裁剪横跨左右；应只监督二者重叠部分，而不能要求学生精确读出右侧从未见到的小字。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30120v1">原论文</a> · <a href="../../../../foundation-models/2610.30120-alps/">实现解读</a> · <a href="#qa-8d4c87309e5eec26">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:alps" data-paper-title="ALPS: Visual State Encoders for World Models" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="ALPS: Visual State Encoders for World Models 基础模型 University of California, Santa Cruz 2026-10-21 世界模型以视觉 token 为状态进行预测和规划，但一个编码器通常只擅长物理状态、语言对齐或像素重建中的一部分。ALPS 尝试让同一组 patch token 同时承担三种接口：机器人状态探针能读出位置，文字指令能对应图像，而未来 token 能被解码成图像以便检查。第一阶段从零训练 ViT-B/16：同一组未做最终 LayerNorm 的 patch token接受图文对比、caption、自重建和密集跨裁剪对应四种监督。第二阶段将第一阶段 encoder 同时用作学生初始化和固定教师； 完整预训练和实验成本过高，不复现（审查 DONE），not_reproduced_high_cost 为终态，不下载大模型/训练数据、不试探性跑完整训练、不自动重试。诊断使用两组裁剪、patch、8 维 query 和 6 维随机 token。输入会检查 shape、有限值、正尺度、裁剪范围和标准差；不静默修正无效数据。模块导入不要求 torch，执行时才加载；不联网、不自动安装依赖、不执行上游脚本或下载 checkpoint。正式评测必须将训练统计与测试轨迹隔离，验证集选参，测试集只用于最终报告。  视觉表征与世界模型 联合嵌入与自监督学习 多模态 视觉世界建模：状态、生成与动作条件 固定 Stage1 教师与 EMA 教师在第二阶段各意味着什么？ ALPS 用 Stage1 模型作为学生初始化和固定教师，教师在第二阶段不随学生更新。EMA 教师则会按学生参数持续移动，目标分布不同；不能把常见 JEPA 的 EMA 习惯套进 ALPS。训练后丢弃跨视图预测器，部署保留学生 encoder 和语言接口。 例如学生为增强鲁棒性发生变化时，固定教师仍提供同一干净裁剪目标；EMA 设置会让这些目标随训练一起漂移。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-9f22083ac5b1aebb">固定 Stage1 教师与 EMA 教师在第二阶段各意味着什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aalps">ALPS: Visual State Encoders for World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Santa Cruz</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>ALPS 用 Stage1 模型作为学生初始化和固定教师，教师在第二阶段不随学生更新。EMA 教师则会按学生参数持续移动，目标分布不同；不能把常见 JEPA 的 EMA 习惯套进 ALPS。训练后丢弃跨视图预测器，部署保留学生 encoder 和语言接口。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生为增强鲁棒性发生变化时，固定教师仍提供同一干净裁剪目标；EMA 设置会让这些目标随训练一起漂移。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30120v1">原论文</a> · <a href="../../../../foundation-models/2610.30120-alps/">实现解读</a> · <a href="#qa-9f22083ac5b1aebb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:alps" data-paper-title="ALPS: Visual State Encoders for World Models" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="ALPS: Visual State Encoders for World Models 基础模型 University of California, Santa Cruz 2026-10-21 世界模型以视觉 token 为状态进行预测和规划，但一个编码器通常只擅长物理状态、语言对齐或像素重建中的一部分。ALPS 尝试让同一组 patch token 同时承担三种接口：机器人状态探针能读出位置，文字指令能对应图像，而未来 token 能被解码成图像以便检查。第一阶段从零训练 ViT-B/16：同一组未做最终 LayerNorm 的 patch token接受图文对比、caption、自重建和密集跨裁剪对应四种监督。第二阶段将第一阶段 encoder 同时用作学生初始化和固定教师； 完整预训练和实验成本过高，不复现（审查 DONE），not_reproduced_high_cost 为终态，不下载大模型/训练数据、不试探性跑完整训练、不自动重试。诊断使用两组裁剪、patch、8 维 query 和 6 维随机 token。输入会检查 shape、有限值、正尺度、裁剪范围和标准差；不静默修正无效数据。模块导入不要求 torch，执行时才加载；不联网、不自动安装依赖、不执行上游脚本或下载 checkpoint。正式评测必须将训练统计与测试轨迹隔离，验证集选参，测试集只用于最终报告。  视觉表征与世界模型 联合嵌入与自监督学习 多模态 视觉世界建模：状态、生成与动作条件 跨裁剪损失为什么先按图平均有效 patch，再对 batch 平均？ 每图重叠区域大小不同，先做图内均值可避免重叠更多的图自动占更大权重。有效性由 B 的 patch 中心是否落入 A 的半开区间决定；无重叠时损失安全贡献零，训练采样器另有最小有效数要求，不能把安全分母当完整采样策略。 例如甲图重叠一百格、乙图十格，整体 token 平均会让甲权重十倍；逐图平均让两张图各贡献一个样本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8f9c95b863618d1a">跨裁剪损失为什么先按图平均有效 patch，再对 batch 平均？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aalps">ALPS: Visual State Encoders for World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Santa Cruz</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每图重叠区域大小不同，先做图内均值可避免重叠更多的图自动占更大权重。有效性由 B 的 patch 中心是否落入 A 的半开区间决定；无重叠时损失安全贡献零，训练采样器另有最小有效数要求，不能把安全分母当完整采样策略。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如甲图重叠一百格、乙图十格，整体 token 平均会让甲权重十倍；逐图平均让两张图各贡献一个样本。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、验证与结果边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30120v1">原论文</a> · <a href="../../../../foundation-models/2610.30120-alps/">实现解读</a> · <a href="#qa-8f9c95b863618d1a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:aw0" data-paper-title="Agentic World Action Models" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Agentic World Action Models 多模态大模型 UC Berkeley 2026-10-21 世界动作模型能预测未来视觉和控制轨迹，但通常缺少可组合的技能结构；代码型机器人 Agent 能重用程序，却未必把计划与物理动态预测统一起来。AW-0 在 Mixture-of-Transformers 中组合三个专家：代码专家产生参数化程序片段，视频专家预测未来场景，动作专家产生连续控制。程序既能约束预测，也可在可选执行模式中调用技能库。每个专家有独立投影、归一化与 FFN，通过每层联合注意力交换信息；专家内部双向、专家之间按代码→视频→动作分块因果。 原始训练与完整对照矩阵明显超出低成本预算，且真实硬件和未随 release 提供的语料无法由合成 fixture 替代，因此成本过高，不复现（审查 DONE）。本地未验证、未生成预测，也没有生产搜广推线上 A/B 证据。本页、原论文 Figure 2、完整作者/代码元数据、成本依据和终态 catalog 已收录。没有运行 adapter、低成本 proxy、benchmark 指标或 GPU 验证收据；也不把“找到开源代码”当作复现完成。promotion_eligible=false、evolve_integrated=false，不进入 Evolve 训练或自动选参。  视频理解与世界模型 具身技能与联合动作生成 多模态 视觉世界建模：状态、生成与动作条件 AW-0 默认生成代码后一定直接执行程序吗？ 不是。默认代码作为计划参与联合去噪，最终由动作 chunk 控制机器人；只有可选 hybrid 模式在代码通过有效性、前提和进展检查时才执行技能，否则回退动作。程序输出、预测视频与实际控制是相关但不同的接口，不能描述成任意 Python 自动执行。 例如模型生成“抓取后放置”的技能片段可帮助动作专家规划，但默认模式仍输出连续控制，而不直接运行该片段。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-multimodal-models-aw0-c41ecc38" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-63a711c06d27630b">AW-0 默认生成代码后一定直接执行程序吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Aaw0">Agentic World Action Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。默认代码作为计划参与联合去噪，最终由动作 chunk 控制机器人；只有可选 hybrid 模式在代码通过有效性、前提和进展检查时才执行技能，否则回退动作。程序输出、预测视频与实际控制是相关但不同的接口，不能描述成任意 Python 自动执行。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型生成“抓取后放置”的技能片段可帮助动作专家规划，但默认模式仍输出连续控制，而不直接运行该片段。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30136v1">原论文</a> · <a href="../../../../multimodal-models/2610.30136-aw0/">实现解读</a> · <a href="#qa-63a711c06d27630b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:aw0" data-paper-title="Agentic World Action Models" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Agentic World Action Models 多模态大模型 UC Berkeley 2026-10-21 世界动作模型能预测未来视觉和控制轨迹，但通常缺少可组合的技能结构；代码型机器人 Agent 能重用程序，却未必把计划与物理动态预测统一起来。AW-0 在 Mixture-of-Transformers 中组合三个专家：代码专家产生参数化程序片段，视频专家预测未来场景，动作专家产生连续控制。程序既能约束预测，也可在可选执行模式中调用技能库。每个专家有独立投影、归一化与 FFN，通过每层联合注意力交换信息；专家内部双向、专家之间按代码→视频→动作分块因果。 原始训练与完整对照矩阵明显超出低成本预算，且真实硬件和未随 release 提供的语料无法由合成 fixture 替代，因此成本过高，不复现（审查 DONE）。本地未验证、未生成预测，也没有生产搜广推线上 A/B 证据。本页、原论文 Figure 2、完整作者/代码元数据、成本依据和终态 catalog 已收录。没有运行 adapter、低成本 proxy、benchmark 指标或 GPU 验证收据；也不把“找到开源代码”当作复现完成。promotion_eligible=false、evolve_integrated=false，不进入 Evolve 训练或自动选参。  视频理解与世界模型 具身技能与联合动作生成 多模态 视觉世界建模：状态、生成与动作条件 AW-0 为什么允许专家内部双向交互，却把专家之间限制为代码→视频→动作？ 内部双向交互有利于同一模态组织完整表示，跨专家分块因果则保持计划、场景预测与动作的条件方向。代码不应提前读取后续视频或动作来伪装规划，动作却可利用代码与预测场景；完全互读会改变信息可用性及推理时的执行顺序。 例如先生成“抓取杯子”的程序，视频专家据此预测场景，动作专家再产出控制；不能让程序先偷看真实未来动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-b0c5a8e2785d041b">AW-0 为什么允许专家内部双向交互，却把专家之间限制为代码→视频→动作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Aaw0">Agentic World Action Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>内部双向交互有利于同一模态组织完整表示，跨专家分块因果则保持计划、场景预测与动作的条件方向。代码不应提前读取后续视频或动作来伪装规划，动作却可利用代码与预测场景；完全互读会改变信息可用性及推理时的执行顺序。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先生成“抓取杯子”的程序，视频专家据此预测场景，动作专家再产出控制；不能让程序先偷看真实未来动作。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30136v1">原论文</a> · <a href="../../../../multimodal-models/2610.30136-aw0/">实现解读</a> · <a href="#qa-b0c5a8e2785d041b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:aw0" data-paper-title="Agentic World Action Models" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Agentic World Action Models 多模态大模型 UC Berkeley 2026-10-21 世界动作模型能预测未来视觉和控制轨迹，但通常缺少可组合的技能结构；代码型机器人 Agent 能重用程序，却未必把计划与物理动态预测统一起来。AW-0 在 Mixture-of-Transformers 中组合三个专家：代码专家产生参数化程序片段，视频专家预测未来场景，动作专家产生连续控制。程序既能约束预测，也可在可选执行模式中调用技能库。每个专家有独立投影、归一化与 FFN，通过每层联合注意力交换信息；专家内部双向、专家之间按代码→视频→动作分块因果。 原始训练与完整对照矩阵明显超出低成本预算，且真实硬件和未随 release 提供的语料无法由合成 fixture 替代，因此成本过高，不复现（审查 DONE）。本地未验证、未生成预测，也没有生产搜广推线上 A/B 证据。本页、原论文 Figure 2、完整作者/代码元数据、成本依据和终态 catalog 已收录。没有运行 adapter、低成本 proxy、benchmark 指标或 GPU 验证收据；也不把“找到开源代码”当作复现完成。promotion_eligible=false、evolve_integrated=false，不进入 Evolve 训练或自动选参。  视频理解与世界模型 具身技能与联合动作生成 多模态 视觉世界建模：状态、生成与动作条件 代码、视频与动作专家完全互相注意，与论文分块因果有何不同？ 论文允许专家内部双向交互，跨专家按代码到视频到动作分块因果：视频读代码，动作读二者，代码不反读未来视频或动作。完全互读会改变条件依赖甚至泄露训练目标信息；独立投影、norm 与 FFN 也不能简化为同一个共享专家。 例如代码计划应基于当前观察和指令，而不能提前读取干净动作答案再生成计划；这条边界由跨块 mask 保证。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-80ec646f7634554a">代码、视频与动作专家完全互相注意，与论文分块因果有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Aaw0">Agentic World Action Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>论文允许专家内部双向交互，跨专家按代码到视频到动作分块因果：视频读代码，动作读二者，代码不反读未来视频或动作。完全互读会改变条件依赖甚至泄露训练目标信息；独立投影、norm 与 FFN 也不能简化为同一个共享专家。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如代码计划应基于当前观察和指令，而不能提前读取干净动作答案再生成计划；这条边界由跨块 mask 保证。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30136v1">原论文</a> · <a href="../../../../multimodal-models/2610.30136-aw0/">实现解读</a> · <a href="#qa-80ec646f7634554a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:aw0" data-paper-title="Agentic World Action Models" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Agentic World Action Models 多模态大模型 UC Berkeley 2026-10-21 世界动作模型能预测未来视觉和控制轨迹，但通常缺少可组合的技能结构；代码型机器人 Agent 能重用程序，却未必把计划与物理动态预测统一起来。AW-0 在 Mixture-of-Transformers 中组合三个专家：代码专家产生参数化程序片段，视频专家预测未来场景，动作专家产生连续控制。程序既能约束预测，也可在可选执行模式中调用技能库。每个专家有独立投影、归一化与 FFN，通过每层联合注意力交换信息；专家内部双向、专家之间按代码→视频→动作分块因果。 原始训练与完整对照矩阵明显超出低成本预算，且真实硬件和未随 release 提供的语料无法由合成 fixture 替代，因此成本过高，不复现（审查 DONE）。本地未验证、未生成预测，也没有生产搜广推线上 A/B 证据。本页、原论文 Figure 2、完整作者/代码元数据、成本依据和终态 catalog 已收录。没有运行 adapter、低成本 proxy、benchmark 指标或 GPU 验证收据；也不把“找到开源代码”当作复现完成。promotion_eligible=false、evolve_integrated=false，不进入 Evolve 训练或自动选参。  视频理解与世界模型 具身技能与联合动作生成 多模态 视觉世界建模：状态、生成与动作条件 连续 flow 目标与代码 masked diffusion 能使用同一噪声和监督 mask 吗？ 不能。视频与动作采用连续加噪及速度回归，代码采用独立 Bernoulli mask，只监督被遮挡程序 token；动作噪声与代码 mask 也不由视频噪声统一决定。视频混合采样还需不同重要性权重并截断归一化，单个 flow loss 不能代表完整训练。 例如视频噪声较低不意味着程序也只能遮少量 token；若三者共用一个随机 mask，就改变了论文规定的独立采样关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-09ecab1ee5f08245">连续 flow 目标与代码 masked diffusion 能使用同一噪声和监督 mask 吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Aaw0">Agentic World Action Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。视频与动作采用连续加噪及速度回归，代码采用独立 Bernoulli mask，只监督被遮挡程序 token；动作噪声与代码 mask 也不由视频噪声统一决定。视频混合采样还需不同重要性权重并截断归一化，单个 flow loss 不能代表完整训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如视频噪声较低不意味着程序也只能遮少量 token；若三者共用一个随机 mask，就改变了论文规定的独立采样关系。</p>
<p class="ar-learning-sources">依据：本地收录与复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30136v1">原论文</a> · <a href="../../../../multimodal-models/2610.30136-aw0/">实现解读</a> · <a href="#qa-09ecab1ee5f08245">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:locale-jepa" data-paper-title="LocaLeJEPA: Maximum Entropy Representations under Geometric Priors" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="LocaLeJEPA: Maximum Entropy Representations under Geometric Priors 基础模型 University of Pennsylvania 2026-10-20 LeJEPA 将整体表示推向各向同性高斯；当表示本身具有局部流形、双曲或等变几何时，单一全局分布不一定合适。LocaLeJEPA 不改写为另一种高斯损失，而是将每个 batch 的多视图平均表示分簇，在各簇内分别匹配均匀球分布。各簇位置不被拉向共同原点，局部形状通过重中心后的残差约束。 完整实验标注成本过高，不复现（审查 DONE），不下载、不试跑、不进入自动训练队列。3 seed 不改变 L1 诊断资格，无正式 capability comparison、无 Evolve 晋级。已实现 uniform_ball_cf、ballreg_loss、torch_kmeans_labels、local_ballreg_loss 和 locale_jepa_loss。前向真实计算局部均匀球统计并反向传播至投影；仅分簇赋值 detached，预测均值和重中心残差没有 stop-gradient。采用作者官方 pure-torch k-means 路径，不额外引入聚类依赖。  JEPA与世界模型 局部均匀球分布匹配 多模态 视觉世界建模：状态、生成与动作条件 局部均匀球约束为什么先对每簇表示重中心？ 局部分布正则约束簇内残差的形状，而不把所有簇中心拉到同一个原点，因此可以保留不同局部结构之间的位置关系。分簇使用 detached 多视图均值，各视图共享分组；重中心后的残差仍参与梯度，不能把整个局部目标都 detach。 例如两类物体表示位于相距很远的中心，正则可分别展开各自局部残差，而不要求两类中心重合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-locale-jepa-ba12e8f4" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-3d704fc3d2d42061">局部均匀球约束为什么先对每簇表示重中心？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alocale-jepa">LocaLeJEPA: Maximum Entropy Representations under Geometric Priors</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pennsylvania</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>局部分布正则约束簇内残差的形状，而不把所有簇中心拉到同一个原点，因此可以保留不同局部结构之间的位置关系。分簇使用 detached 多视图均值，各视图共享分组；重中心后的残差仍参与梯度，不能把整个局部目标都 detach。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两类物体表示位于相距很远的中心，正则可分别展开各自局部残差，而不要求两类中心重合。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28458v1">原论文</a> · <a href="../../../../foundation-models/2610.28458-locale-jepa/">实现解读</a> · <a href="#qa-3d704fc3d2d42061">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:locale-jepa" data-paper-title="LocaLeJEPA: Maximum Entropy Representations under Geometric Priors" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="LocaLeJEPA: Maximum Entropy Representations under Geometric Priors 基础模型 University of Pennsylvania 2026-10-20 LeJEPA 将整体表示推向各向同性高斯；当表示本身具有局部流形、双曲或等变几何时，单一全局分布不一定合适。LocaLeJEPA 不改写为另一种高斯损失，而是将每个 batch 的多视图平均表示分簇，在各簇内分别匹配均匀球分布。各簇位置不被拉向共同原点，局部形状通过重中心后的残差约束。 完整实验标注成本过高，不复现（审查 DONE），不下载、不试跑、不进入自动训练队列。3 seed 不改变 L1 诊断资格，无正式 capability comparison、无 Evolve 晋级。已实现 uniform_ball_cf、ballreg_loss、torch_kmeans_labels、local_ballreg_loss 和 locale_jepa_loss。前向真实计算局部均匀球统计并反向传播至投影；仅分簇赋值 detached，预测均值和重中心残差没有 stop-gradient。采用作者官方 pure-torch k-means 路径，不额外引入聚类依赖。  JEPA与世界模型 局部均匀球分布匹配 多模态 视觉世界建模：状态、生成与动作条件 为什么 LocaLeJEPA 不把所有簇都直接拉向同一个高斯分布？ 不同局部簇可能对应具有自身几何的状态，把它们统一拉向原点会破坏簇间位置和局部结构。方法先固定分组，再对各簇重中心残差匹配均匀球体分布，保留整体布局；簇太小时还要明确回退，不能把目标偷换为普通全局高斯正则。 例如两团表示分别对应两种运动模式，各自分散但位置不同；约束局部形状无需把两团的中心都拉到同一点。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-039c7085ea195e93">为什么 LocaLeJEPA 不把所有簇都直接拉向同一个高斯分布？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alocale-jepa">LocaLeJEPA: Maximum Entropy Representations under Geometric Priors</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pennsylvania</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同局部簇可能对应具有自身几何的状态，把它们统一拉向原点会破坏簇间位置和局部结构。方法先固定分组，再对各簇重中心残差匹配均匀球体分布，保留整体布局；簇太小时还要明确回退，不能把目标偷换为普通全局高斯正则。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两团表示分别对应两种运动模式，各自分散但位置不同；约束局部形状无需把两团的中心都拉到同一点。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28458v1">原论文</a> · <a href="../../../../foundation-models/2610.28458-locale-jepa/">实现解读</a> · <a href="#qa-039c7085ea195e93">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:locale-jepa" data-paper-title="LocaLeJEPA: Maximum Entropy Representations under Geometric Priors" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="LocaLeJEPA: Maximum Entropy Representations under Geometric Priors 基础模型 University of Pennsylvania 2026-10-20 LeJEPA 将整体表示推向各向同性高斯；当表示本身具有局部流形、双曲或等变几何时，单一全局分布不一定合适。LocaLeJEPA 不改写为另一种高斯损失，而是将每个 batch 的多视图平均表示分簇，在各簇内分别匹配均匀球分布。各簇位置不被拉向共同原点，局部形状通过重中心后的残差约束。 完整实验标注成本过高，不复现（审查 DONE），不下载、不试跑、不进入自动训练队列。3 seed 不改变 L1 诊断资格，无正式 capability comparison、无 Evolve 晋级。已实现 uniform_ball_cf、ballreg_loss、torch_kmeans_labels、local_ballreg_loss 和 locale_jepa_loss。前向真实计算局部均匀球统计并反向传播至投影；仅分簇赋值 detached，预测均值和重中心残差没有 stop-gradient。采用作者官方 pure-torch k-means 路径，不额外引入聚类依赖。  JEPA与世界模型 局部均匀球分布匹配 多模态 视觉世界建模：状态、生成与动作条件 均匀实心球目标与高斯或单位球面目标有什么区别？ 均匀实心球把概率分布在球体内部，半径取根号 d+2 使协方差为单位阵；高斯无界，球面则只在固定半径上有质量。三者特征函数不同，LocaLeJEPA 的目标不能由高斯公式或向量单位化代替。 例如二维均匀圆盘含中心附近样本，圆周分布没有内部质量，高斯还会在任意大半径出现样本；它们并非同一正则。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-cfaad9a651dc6033">均匀实心球目标与高斯或单位球面目标有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alocale-jepa">LocaLeJEPA: Maximum Entropy Representations under Geometric Priors</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pennsylvania</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>均匀实心球把概率分布在球体内部，半径取根号 d+2 使协方差为单位阵；高斯无界，球面则只在固定半径上有质量。三者特征函数不同，LocaLeJEPA 的目标不能由高斯公式或向量单位化代替。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如二维均匀圆盘含中心附近样本，圆周分布没有内部质量，高斯还会在任意大半径出现样本；它们并非同一正则。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28458v1">原论文</a> · <a href="../../../../foundation-models/2610.28458-locale-jepa/">实现解读</a> · <a href="#qa-cfaad9a651dc6033">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:locale-jepa" data-paper-title="LocaLeJEPA: Maximum Entropy Representations under Geometric Priors" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="LocaLeJEPA: Maximum Entropy Representations under Geometric Priors 基础模型 University of Pennsylvania 2026-10-20 LeJEPA 将整体表示推向各向同性高斯；当表示本身具有局部流形、双曲或等变几何时，单一全局分布不一定合适。LocaLeJEPA 不改写为另一种高斯损失，而是将每个 batch 的多视图平均表示分簇，在各簇内分别匹配均匀球分布。各簇位置不被拉向共同原点，局部形状通过重中心后的残差约束。 完整实验标注成本过高，不复现（审查 DONE），不下载、不试跑、不进入自动训练队列。3 seed 不改变 L1 诊断资格，无正式 capability comparison、无 Evolve 晋级。已实现 uniform_ball_cf、ballreg_loss、torch_kmeans_labels、local_ballreg_loss 和 locale_jepa_loss。前向真实计算局部均匀球统计并反向传播至投影；仅分簇赋值 detached，预测均值和重中心残差没有 stop-gradient。采用作者官方 pure-torch k-means 路径，不额外引入聚类依赖。  JEPA与世界模型 局部均匀球分布匹配 多模态 视觉世界建模：状态、生成与动作条件 小簇过滤与簇数变化为什么影响有效正则强度？ 只保留至少四样本的簇，无有效簇时回退全 batch 并记录。各簇统计先乘其样本数，再对有效簇和视图等权平均，因此改变簇数不只是改变局部粒度，也改变损失尺度；积分采用球特征函数，不能把高斯窗口误作目标分布。 例如拆成更多有效小簇后，等权平均与样本数因子共同改变数值；沿用同一 λ 也不保证正则力度相同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-5c22e52ed3c5a5bb">小簇过滤与簇数变化为什么影响有效正则强度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alocale-jepa">LocaLeJEPA: Maximum Entropy Representations under Geometric Priors</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pennsylvania</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只保留至少四样本的簇，无有效簇时回退全 batch 并记录。各簇统计先乘其样本数，再对有效簇和视图等权平均，因此改变簇数不只是改变局部粒度，也改变损失尺度；积分采用球特征函数，不能把高斯窗口误作目标分布。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如拆成更多有效小簇后，等权平均与样本数因子共同改变数值；沿用同一 λ 也不保证正则力度相同。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、验证与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28458v1">原论文</a> · <a href="../../../../foundation-models/2610.28458-locale-jepa/">实现解读</a> · <a href="#qa-5c22e52ed3c5a5bb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ppmem" data-paper-title="Persistent Planar Memory for Video World Models" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Persistent Planar Memory for Video World Models 基础模型 Tsinghua University 2026-10-16 长视频生成若只保存少量历史帧，跨视角回访容易遗忘场景；持续保存全部像素点云又非常大。PPMem把场景记忆压成可光栅化的平面primitive，在视频生成过程中由同一骨干联合预测，再通过持久pool向后续chunk反馈深度。每个局部平面用中心深度、两个矩形尺度和四元数共7个参数表示，变换到世界坐标后合并。pool按遮挡投票删除错误旧面，按观察质量去重，并依据已给定的下一段相机轨迹提前淘汰即将被更好观测替换的面；它不是读取未来真实视频。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。没有本地世界模型、训练结果或Evolve能力算子。本轮只核原文方法、元数据、结果归属及成本，不下载模型或视频，不制造小张量“世界模型能力”分数。没有GPU回执要求，因为没有接受执行CUDA实现。  多模态基础模型 世界模型与持久三维记忆 多模态 视觉世界建模：状态、生成与动作条件 PPMem 保存平面 primitive 而不是所有历史帧，保留了哪类信息？ 平面 pool 保存可渲染深度的持久几何状态，每个局部平面以中心深度、两个尺度和四元数共七参数表示，再变换到世界坐标。它主要支持跨视角几何记忆，不等于无损保存历史纹理、动态事件或所有像素，紧凑 pool 大小也不是整个模型显存。 例如再次转向先前墙面时，可从世界坐标平面渲染深度帮助一致生成，但不能仅靠七参数恢复墙上所有文字纹理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-ppmem-5417d641" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4111c1cac44a1ce5">PPMem 保存平面 primitive 而不是所有历史帧，保留了哪类信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Appmem">Persistent Planar Memory for Video World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>平面 pool 保存可渲染深度的持久几何状态，每个局部平面以中心深度、两个尺度和四元数共七参数表示，再变换到世界坐标。它主要支持跨视角几何记忆，不等于无损保存历史纹理、动态事件或所有像素，紧凑 pool 大小也不是整个模型显存。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如再次转向先前墙面时，可从世界坐标平面渲染深度帮助一致生成，但不能仅靠七参数恢复墙上所有文字纹理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与流程；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23795">原论文</a> · <a href="../../../../foundation-models/2610.23795-ppmem/">实现解读</a> · <a href="#qa-4111c1cac44a1ce5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ppmem" data-paper-title="Persistent Planar Memory for Video World Models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Persistent Planar Memory for Video World Models 基础模型 Tsinghua University 2026-10-16 长视频生成若只保存少量历史帧，跨视角回访容易遗忘场景；持续保存全部像素点云又非常大。PPMem把场景记忆压成可光栅化的平面primitive，在视频生成过程中由同一骨干联合预测，再通过持久pool向后续chunk反馈深度。每个局部平面用中心深度、两个矩形尺度和四元数共7个参数表示，变换到世界坐标后合并。pool按遮挡投票删除错误旧面，按观察质量去重，并依据已给定的下一段相机轨迹提前淘汰即将被更好观测替换的面；它不是读取未来真实视频。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。没有本地世界模型、训练结果或Evolve能力算子。本轮只核原文方法、元数据、结果归属及成本，不下载模型或视频，不制造小张量“世界模型能力”分数。没有GPU回执要求，因为没有接受执行CUDA实现。  多模态基础模型 世界模型与持久三维记忆 多模态 视觉世界建模：状态、生成与动作条件 依据下一段相机轨迹淘汰平面，为什么不等于读取未来真实视频？ 相机轨迹可以是生成任务已给定的控制条件，它说明之后将朝哪里看，并不提供那里的真实图像。平面池据此管理将被更好观测替换的几何，后续视频仍需模型生成；只有把未知未来观测或真值几何提前送入记忆，才构成另一种信息泄漏。 例如用户预先指定镜头绕桌子一圈，系统可据轨迹安排记忆；它仍不知道桌子背面的真实纹理，不能当成已经看到。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-1ffec7e05ce43b92">依据下一段相机轨迹淘汰平面，为什么不等于读取未来真实视频？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Appmem">Persistent Planar Memory for Video World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相机轨迹可以是生成任务已给定的控制条件，它说明之后将朝哪里看，并不提供那里的真实图像。平面池据此管理将被更好观测替换的几何，后续视频仍需模型生成；只有把未知未来观测或真值几何提前送入记忆，才构成另一种信息泄漏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户预先指定镜头绕桌子一圈，系统可据轨迹安排记忆；它仍不知道桌子背面的真实纹理，不能当成已经看到。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与流程；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23795">原论文</a> · <a href="../../../../foundation-models/2610.23795-ppmem/">实现解读</a> · <a href="#qa-1ffec7e05ce43b92">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ppmem" data-paper-title="Persistent Planar Memory for Video World Models" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Persistent Planar Memory for Video World Models 基础模型 Tsinghua University 2026-10-16 长视频生成若只保存少量历史帧，跨视角回访容易遗忘场景；持续保存全部像素点云又非常大。PPMem把场景记忆压成可光栅化的平面primitive，在视频生成过程中由同一骨干联合预测，再通过持久pool向后续chunk反馈深度。每个局部平面用中心深度、两个矩形尺度和四元数共7个参数表示，变换到世界坐标后合并。pool按遮挡投票删除错误旧面，按观察质量去重，并依据已给定的下一段相机轨迹提前淘汰即将被更好观测替换的面；它不是读取未来真实视频。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。没有本地世界模型、训练结果或Evolve能力算子。本轮只核原文方法、元数据、结果归属及成本，不下载模型或视频，不制造小张量“世界模型能力”分数。没有GPU回执要求，因为没有接受执行CUDA实现。  多模态基础模型 世界模型与持久三维记忆 多模态 视觉世界建模：状态、生成与动作条件 持久平面池与仅保留近期帧作为生成条件有什么差别？ 近期帧记忆容易在长时间离开某区域后忘记场景，世界坐标 pool 可在相机回访时继续提供几何条件。它还需遮挡投票、质量去重及淘汰维护，不能把不断追加平面当完整机制；已知未来相机轨迹也不等于读取未来真实视频。 例如镜头绕房间一圈后回到起点，旧墙面可仍在 pool 中；淘汰决策可知道下一段相机位置，却不知道未来真实像素。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e1ace68dd5ef5979">持久平面池与仅保留近期帧作为生成条件有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Appmem">Persistent Planar Memory for Video World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>近期帧记忆容易在长时间离开某区域后忘记场景，世界坐标 pool 可在相机回访时继续提供几何条件。它还需遮挡投票、质量去重及淘汰维护，不能把不断追加平面当完整机制；已知未来相机轨迹也不等于读取未来真实视频。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如镜头绕房间一圈后回到起点，旧墙面可仍在 pool 中；淘汰决策可知道下一段相机位置，却不知道未来真实像素。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与流程；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23795">原论文</a> · <a href="../../../../foundation-models/2610.23795-ppmem/">实现解读</a> · <a href="#qa-e1ace68dd5ef5979">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ppmem" data-paper-title="Persistent Planar Memory for Video World Models" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Persistent Planar Memory for Video World Models 基础模型 Tsinghua University 2026-10-16 长视频生成若只保存少量历史帧，跨视角回访容易遗忘场景；持续保存全部像素点云又非常大。PPMem把场景记忆压成可光栅化的平面primitive，在视频生成过程中由同一骨干联合预测，再通过持久pool向后续chunk反馈深度。每个局部平面用中心深度、两个矩形尺度和四元数共7个参数表示，变换到世界坐标后合并。pool按遮挡投票删除错误旧面，按观察质量去重，并依据已给定的下一段相机轨迹提前淘汰即将被更好观测替换的面；它不是读取未来真实视频。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。没有本地世界模型、训练结果或Evolve能力算子。本轮只核原文方法、元数据、结果归属及成本，不下载模型或视频，不制造小张量“世界模型能力”分数。没有GPU回执要求，因为没有接受执行CUDA实现。  多模态基础模型 世界模型与持久三维记忆 多模态 视觉世界建模：状态、生成与动作条件 几何 LoRA 是在每个视频去噪步都开启吗？ 不是。视频去噪使用 Stage1 冻结骨干并关闭几何 LoRA，视频生成完成后额外开启一次几何前向提取平面。两阶段训练还有深度、法线、光栅化与平滑目标，前千步不启用光栅化损失；当前本地仅资料收录，没有执行世界模型。 例如生成二十五帧 chunk 的多个去噪步不逐步更新平面；结束后一次几何提取再合并 pool，流程不同于每步联训几何。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-873512f352f628c0">几何 LoRA 是在每个视频去噪步都开启吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Appmem">Persistent Planar Memory for Video World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。视频去噪使用 Stage1 冻结骨干并关闭几何 LoRA，视频生成完成后额外开启一次几何前向提取平面。两阶段训练还有深度、法线、光栅化与平滑目标，前千步不启用光栅化损失；当前本地仅资料收录，没有执行世界模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如生成二十五帧 chunk 的多个去噪步不逐步更新平面；结束后一次几何提取再合并 pool，流程不同于每步联训几何。</p>
<p class="ar-learning-sources">依据：核心公式与流程、本地复现与成本判断；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23795">原论文</a> · <a href="../../../../foundation-models/2610.23795-ppmem/">实现解读</a> · <a href="#qa-873512f352f628c0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ego-p2c" data-paper-title="EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video 基础模型 Arizona State University 2026-10-15 第一视角视频空间推理既要提问、采集证据，也要保证感知回答可靠。固定外部视觉工具无法随推理策略一起改进；把规划与感知压到同一组参数中又可能引入梯度冲突。EgoP²C先在冻结VLM上分别训练规划/组合（PC）与感知（V）的LoRA教师，再复制选定FFN形成PC、V、通用直接回答（G）专家。学生自己生成交互片段，由相应冻结教师实时评价同一批学生tokens，而非模仿教师另行生成的答案。公共视频前缀始终走冻结基础路径；角色私有文字、选项和历史不混入公共KV。 完整实验成本过高，不复现（审查 DONE）。本地保留真实角色FFN复制、q/k/v/o低秩残差、因果attention、公共前缀冻结、严格参数冻结、完整词表打分及上述损失。使用12维单层小型decoder和人工token ids，没有视觉编码器或真实视频。预设PLAN和DIRECT骨架，仅各片段内部由学生当前分布实时采样；没有训练过的空间教师、自由工具调用或学习到的路由器。  多模态基础模型 空间推理与分段多教师蒸馏 多模态 视觉世界建模：状态、生成与动作条件 PC、V、G 三种角色为什么需要不同可见信息？ PC 负责规划组合，V 负责自包含感知子问题，G 负责直接回答原问题。隔离私有上下文可避免感知教师被选项或规划文字诱导，并保持角色训练与推理一致；公共视频可共享基础前缀，但各角色的文字历史不能混进公共 KV。 例如 V 只应看视频与“左边物体是什么”的子问题，不应看到原题某选项被 PC 提前标成正确。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-ego-p2c-b2c2eae5" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-47077d41b441deb0">PC、V、G 三种角色为什么需要不同可见信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aego-p2c">EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Arizona State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>PC 负责规划组合，V 负责自包含感知子问题，G 负责直接回答原问题。隔离私有上下文可避免感知教师被选项或规划文字诱导，并保持角色训练与推理一致；公共视频可共享基础前缀，但各角色的文字历史不能混进公共 KV。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 V 只应看视频与“左边物体是什么”的子问题，不应看到原题某选项被 PC 提前标成正确。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与信息边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22681">原论文</a> · <a href="../../../../foundation-models/2610.22681-ego-p2c/">实现解读</a> · <a href="#qa-47077d41b441deb0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ego-p2c" data-paper-title="EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video 基础模型 Arizona State University 2026-10-15 第一视角视频空间推理既要提问、采集证据，也要保证感知回答可靠。固定外部视觉工具无法随推理策略一起改进；把规划与感知压到同一组参数中又可能引入梯度冲突。EgoP²C先在冻结VLM上分别训练规划/组合（PC）与感知（V）的LoRA教师，再复制选定FFN形成PC、V、通用直接回答（G）专家。学生自己生成交互片段，由相应冻结教师实时评价同一批学生tokens，而非模仿教师另行生成的答案。公共视频前缀始终走冻结基础路径；角色私有文字、选项和历史不混入公共KV。 完整实验成本过高，不复现（审查 DONE）。本地保留真实角色FFN复制、q/k/v/o低秩残差、因果attention、公共前缀冻结、严格参数冻结、完整词表打分及上述损失。使用12维单层小型decoder和人工token ids，没有视觉编码器或真实视频。预设PLAN和DIRECT骨架，仅各片段内部由学生当前分布实时采样；没有训练过的空间教师、自由工具调用或学习到的路由器。  多模态基础模型 空间推理与分段多教师蒸馏 多模态 视觉世界建模：状态、生成与动作条件 为什么分段蒸馏必须让各教师评价同一批学生 tokens？ 学生实际生成的交互决定了它访问的前缀，各角色教师在这些前缀上评分，才能分别指出规划、感知或直接回答的偏差。若改成模仿教师另写的一条答案，就丢失在策略监督；共享视频 KV 还不能混入角色私有历史，以免破坏信息隔离。 例如学生先提出一个视角问题，再给出空间判断；规划教师评前段、感知教师评相关片段，二者都评学生真正走过的文本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c60c2b24dcf80f55">为什么分段蒸馏必须让各教师评价同一批学生 tokens？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aego-p2c">EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Arizona State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>学生实际生成的交互决定了它访问的前缀，各角色教师在这些前缀上评分，才能分别指出规划、感知或直接回答的偏差。若改成模仿教师另写的一条答案，就丢失在策略监督；共享视频 KV 还不能混入角色私有历史，以免破坏信息隔离。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生先提出一个视角问题，再给出空间判断；规划教师评前段、感知教师评相关片段，二者都评学生真正走过的文本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与信息边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22681">原论文</a> · <a href="../../../../foundation-models/2610.22681-ego-p2c/">实现解读</a> · <a href="#qa-c60c2b24dcf80f55">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ego-p2c" data-paper-title="EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video 基础模型 Arizona State University 2026-10-15 第一视角视频空间推理既要提问、采集证据，也要保证感知回答可靠。固定外部视觉工具无法随推理策略一起改进；把规划与感知压到同一组参数中又可能引入梯度冲突。EgoP²C先在冻结VLM上分别训练规划/组合（PC）与感知（V）的LoRA教师，再复制选定FFN形成PC、V、通用直接回答（G）专家。学生自己生成交互片段，由相应冻结教师实时评价同一批学生tokens，而非模仿教师另行生成的答案。公共视频前缀始终走冻结基础路径；角色私有文字、选项和历史不混入公共KV。 完整实验成本过高，不复现（审查 DONE）。本地保留真实角色FFN复制、q/k/v/o低秩残差、因果attention、公共前缀冻结、严格参数冻结、完整词表打分及上述损失。使用12维单层小型decoder和人工token ids，没有视觉编码器或真实视频。预设PLAN和DIRECT骨架，仅各片段内部由学生当前分布实时采样；没有训练过的空间教师、自由工具调用或学习到的路由器。  多模态基础模型 空间推理与分段多教师蒸馏 多模态 视觉世界建模：状态、生成与动作条件 学生前缀上的多教师 OPD 与模仿教师各自生成答案有什么区别？ OPD 对学生自己采样的同一批 token，由对应角色教师在同一可见前缀下评分，优化学生实际访问状态。模仿教师另生成的答案会换轨迹与上下文，不能直接代表相同 on-policy 信号；教师优势也应只作为训练监督而非部署 oracle。 例如学生先写出一个错误假设，教师需要评价该实际前缀上的下一 token，而不是另起一条完美推理覆盖它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d2509c24f0c7580c">学生前缀上的多教师 OPD 与模仿教师各自生成答案有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aego-p2c">EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Arizona State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>OPD 对学生自己采样的同一批 token，由对应角色教师在同一可见前缀下评分，优化学生实际访问状态。模仿教师另生成的答案会换轨迹与上下文，不能直接代表相同 on-policy 信号；教师优势也应只作为训练监督而非部署 oracle。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生先写出一个错误假设，教师需要评价该实际前缀上的下一 token，而不是另起一条完美推理覆盖它。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与信息边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22681">原论文</a> · <a href="../../../../foundation-models/2610.22681-ego-p2c/">实现解读</a> · <a href="#qa-d2509c24f0c7580c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ego-p2c" data-paper-title="EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video 基础模型 Arizona State University 2026-10-15 第一视角视频空间推理既要提问、采集证据，也要保证感知回答可靠。固定外部视觉工具无法随推理策略一起改进；把规划与感知压到同一组参数中又可能引入梯度冲突。EgoP²C先在冻结VLM上分别训练规划/组合（PC）与感知（V）的LoRA教师，再复制选定FFN形成PC、V、通用直接回答（G）专家。学生自己生成交互片段，由相应冻结教师实时评价同一批学生tokens，而非模仿教师另行生成的答案。公共视频前缀始终走冻结基础路径；角色私有文字、选项和历史不混入公共KV。 完整实验成本过高，不复现（审查 DONE）。本地保留真实角色FFN复制、q/k/v/o低秩残差、因果attention、公共前缀冻结、严格参数冻结、完整词表打分及上述损失。使用12维单层小型decoder和人工token ids，没有视觉编码器或真实视频。预设PLAN和DIRECT骨架，仅各片段内部由学生当前分布实时采样；没有训练过的空间教师、自由工具调用或学习到的路由器。  多模态基础模型 空间推理与分段多教师蒸馏 多模态 视觉世界建模：状态、生成与动作条件 角色长度归一化的分母为何必须覆盖整条轨迹？ 同角色可出现多个片段，分母是该轨迹中该角色所有监督 token 总数，而非每段各平均一次。否则拆成更多短片段就会获得更大角色权重。教师与旧学生 logp 停止梯度，私有 decoder KV 不跨角色复用，本地随机教师诊断不等于空间推理能力。 例如 PC 总共十个 token，拆成两段各五个后总权重应不变；若每段独立平均，拆段会把 PC 贡献翻倍。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a6f0616beea54a27">角色长度归一化的分母为何必须覆盖整条轨迹？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aego-p2c">EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Arizona State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同角色可出现多个片段，分母是该轨迹中该角色所有监督 token 总数，而非每段各平均一次。否则拆成更多短片段就会获得更大角色权重。教师与旧学生 logp 停止梯度，私有 decoder KV 不跨角色复用，本地随机教师诊断不等于空间推理能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 PC 总共十个 token，拆成两段各五个后总权重应不变；若每段独立平均，拆段会把 PC 贡献翻倍。</p>
<p class="ar-learning-sources">依据：核心公式与信息边界、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22681">原论文</a> · <a href="../../../../foundation-models/2610.22681-ego-p2c/">实现解读</a> · <a href="#qa-a6f0616beea54a27">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gen4p" data-paper-title="Gen4P: Video Generators are 4D Perceivers" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Gen4P: Video Generators are 4D Perceivers 基础模型 Nanyang Technological University 2026-10-15 视频生成预训练包含运动与几何先验。Gen4P不通过多次去噪恢复几何，而是在干净视频潜变量上运行一次DiT编码，用按需cross-attention查询输出3D轨迹、点云、深度和相机参数。连续时间查询适配不同视频长度，冻结depth-LoRA提供额外几何先验，独立4D-LoRA学习新任务。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地训练、能力指标或Evolve算子。无本地adapter、GPU验收、训练指标或可执行Evolve映射。上游repo存在不等同代码已开源；未来若作者真正发布实现，只有出现新的独立证据或用户明确需求时再审查。本轮只完成方法、代码发布状态与资源配置核验；没有下载视频、checkpoint、运行训练或制造小模型“4D能力”分数。  多模态基础模型 视频生成与四维感知 多模态 视觉世界建模：状态、生成与动作条件 Gen4P 将视频生成器用于感知时，为什么不需要反复去噪？ 它把干净视频经 VAE 得到的潜变量送入一次 DiT 前向，提取共享场景 token，再用查询解码几何属性。这里使用的是生成预训练获得的表示先验，而非先生成一段视频再估计几何；输入也不需要人为加噪后运行多步采样。 例如给一段已拍摄视频，单次编码后查询某像素的三维轨迹，不必先执行五十轮扩散生成另一段视频。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-gen4p-e9a640f8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e01e783591ec19da">Gen4P 将视频生成器用于感知时，为什么不需要反复去噪？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agen4p">Gen4P: Video Generators are 4D Perceivers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它把干净视频经 VAE 得到的潜变量送入一次 DiT 前向，提取共享场景 token，再用查询解码几何属性。这里使用的是生成预训练获得的表示先验，而非先生成一段视频再估计几何；输入也不需要人为加噪后运行多步采样。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如给一段已拍摄视频，单次编码后查询某像素的三维轨迹，不必先执行五十轮扩散生成另一段视频。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22371">原论文</a> · <a href="../../../../foundation-models/2610.22371-gen4p/">实现解读</a> · <a href="#qa-e01e783591ec19da">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gen4p" data-paper-title="Gen4P: Video Generators are 4D Perceivers" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Gen4P: Video Generators are 4D Perceivers 基础模型 Nanyang Technological University 2026-10-15 视频生成预训练包含运动与几何先验。Gen4P不通过多次去噪恢复几何，而是在干净视频潜变量上运行一次DiT编码，用按需cross-attention查询输出3D轨迹、点云、深度和相机参数。连续时间查询适配不同视频长度，冻结depth-LoRA提供额外几何先验，独立4D-LoRA学习新任务。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地训练、能力指标或Evolve算子。无本地adapter、GPU验收、训练指标或可执行Evolve映射。上游repo存在不等同代码已开源；未来若作者真正发布实现，只有出现新的独立证据或用户明确需求时再审查。本轮只完成方法、代码发布状态与资源配置核验；没有下载视频、checkpoint、运行训练或制造小模型“4D能力”分数。  多模态基础模型 视频生成与四维感知 多模态 视觉世界建模：状态、生成与动作条件 使用视频生成器做四维感知时，为什么不必执行完整多步去噪？ Gen4P 利用预训练 DiT 内部的运动与几何表示，而不是要求它重新生成视频。干净视频潜变量经过一次规定条件的编码，查询再读出轨迹或深度；冻结几何适配与新任务 LoRA 承担不同职责。少一次生成过程并不意味着感知任务无需监督或解码器。 例如输入现有视频后查询某点三秒后的三维位置，读取一次场景表示即可训练预测头，不需要先生成另一段完整视频。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-e6914c7043932711">使用视频生成器做四维感知时，为什么不必执行完整多步去噪？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agen4p">Gen4P: Video Generators are 4D Perceivers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Gen4P 利用预训练 DiT 内部的运动与几何表示，而不是要求它重新生成视频。干净视频潜变量经过一次规定条件的编码，查询再读出轨迹或深度；冻结几何适配与新任务 LoRA 承担不同职责。少一次生成过程并不意味着感知任务无需监督或解码器。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如输入现有视频后查询某点三秒后的三维位置，读取一次场景表示即可训练预测头，不需要先生成另一段完整视频。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22371">原论文</a> · <a href="../../../../foundation-models/2610.22371-gen4p/">实现解读</a> · <a href="#qa-e6914c7043932711">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gen4p" data-paper-title="Gen4P: Video Generators are 4D Perceivers" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Gen4P: Video Generators are 4D Perceivers 基础模型 Nanyang Technological University 2026-10-15 视频生成预训练包含运动与几何先验。Gen4P不通过多次去噪恢复几何，而是在干净视频潜变量上运行一次DiT编码，用按需cross-attention查询输出3D轨迹、点云、深度和相机参数。连续时间查询适配不同视频长度，冻结depth-LoRA提供额外几何先验，独立4D-LoRA学习新任务。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地训练、能力指标或Evolve算子。无本地adapter、GPU验收、训练指标或可执行Evolve映射。上游repo存在不等同代码已开源；未来若作者真正发布实现，只有出现新的独立证据或用户明确需求时再审查。本轮只完成方法、代码发布状态与资源配置核验；没有下载视频、checkpoint、运行训练或制造小模型“4D能力”分数。  多模态基础模型 视频生成与四维感知 多模态 视觉世界建模：状态、生成与动作条件 冻结 depth-LoRA 与训练 4D-LoRA 的分工，为什么不同于全参数微调？ 基础 DiT 和深度 LoRA 保持冻结，新增 4D-LoRA、查询与输出解码器承担感知任务适配，分别保留生成和深度先验。全参数微调会允许更广泛改变这些表示；双 LoRA 也并非每项指标必然改善，原文保留了深度结果下降的例子。 例如新任务需要追踪点的时间轨迹，可更新 4D 适配而不改已有深度更新，但仍要检查是否改善实际深度与追踪。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f62c7e64e5b82850">冻结 depth-LoRA 与训练 4D-LoRA 的分工，为什么不同于全参数微调？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agen4p">Gen4P: Video Generators are 4D Perceivers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>基础 DiT 和深度 LoRA 保持冻结，新增 4D-LoRA、查询与输出解码器承担感知任务适配，分别保留生成和深度先验。全参数微调会允许更广泛改变这些表示；双 LoRA 也并非每项指标必然改善，原文保留了深度结果下降的例子。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如新任务需要追踪点的时间轨迹，可更新 4D 适配而不改已有深度更新，但仍要检查是否改善实际深度与追踪。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22371">原论文</a> · <a href="../../../../foundation-models/2610.22371-gen4p/">实现解读</a> · <a href="#qa-f62c7e64e5b82850">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gen4p" data-paper-title="Gen4P: Video Generators are 4D Perceivers" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Gen4P: Video Generators are 4D Perceivers 基础模型 Nanyang Technological University 2026-10-15 视频生成预训练包含运动与几何先验。Gen4P不通过多次去噪恢复几何，而是在干净视频潜变量上运行一次DiT编码，用按需cross-attention查询输出3D轨迹、点云、深度和相机参数。连续时间查询适配不同视频长度，冻结depth-LoRA提供额外几何先验，独立4D-LoRA学习新任务。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地训练、能力指标或Evolve算子。无本地adapter、GPU验收、训练指标或可执行Evolve映射。上游repo存在不等同代码已开源；未来若作者真正发布实现，只有出现新的独立证据或用户明确需求时再审查。本轮只完成方法、代码发布状态与资源配置核验；没有下载视频、checkpoint、运行训练或制造小模型“4D能力”分数。  多模态基础模型 视频生成与四维感知 多模态 视觉世界建模：状态、生成与动作条件 连续时间查询与 DiT 输入条件有哪些容易混淆的细节？ 时间查询用起终点 embedding 按 t/(T-1) 连续插值，DiT 则读取干净 z0，使用最终 scheduler 时间条件和空文本条件。不能把查询时间当作扩散加噪时刻，也不能改成迭代去噪。当前只有资料收录，无本地 adapter 或 4D 能力验证。 例如查询视频中间时刻使用两个时间端点的插值，并不是给该帧加一半噪声再让生成器恢复。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-15ae281ad1d75986">连续时间查询与 DiT 输入条件有哪些容易混淆的细节？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agen4p">Gen4P: Video Generators are 4D Perceivers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>时间查询用起终点 embedding 按 t/(T-1) 连续插值，DiT 则读取干净 z0，使用最终 scheduler 时间条件和空文本条件。不能把查询时间当作扩散加噪时刻，也不能改成迭代去噪。当前只有资料收录，无本地 adapter 或 4D 能力验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如查询视频中间时刻使用两个时间端点的插值，并不是给该帧加一半噪声再让生成器恢复。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22371">原论文</a> · <a href="../../../../foundation-models/2610.22371-gen4p/">实现解读</a> · <a href="#qa-15ae281ad1d75986">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:egojepa" data-paper-title="EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos 基础模型 Mohamed bin Zayed University of Artificial Intelligence 2026-10-14 人类第一视角视频中的手运动不需要经规则映射为每种机器人的动作。EgoJEPA先用手部运动差分条件JEPA预测未来视觉表示，再联合建模视觉与潜动作，最后仅适配目标机器人的输入输出动作接口。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地能力指标、训练结果或可执行 Evolve 算子。无本地adapter、指标文件或GPU回执，也不登记可执行Evolve算子。原论文结果仅作为阅读资料。范围见本轮实现与审查合同。本轮只完成方法、资源需求、公开代码状态及原图收录，没有运行完整实验、下载checkpoint或制造模拟能力分数。  JEPA与世界模型 具身多模态 多模态 视觉世界建模：状态、生成与动作条件 EgoJEPA 为什么用人手运动差分，而不是先把人手轨迹硬映射成机器人关节？ 手部差分作为动作条件帮助预测未来视觉表示，把可迁移的变化规律与具体机器人执行接口分开。后续再适配目标机器人的输入输出，因此不需要先为每种具身设计完整关节映射；这并不表示无需机器人数据或无需控制适配。 例如人类捏起物体的运动可提供状态变化线索，但五指机器人与双指夹爪仍须各自学习如何输出可执行控制。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-egojepa-867ae28c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-eace4b99f19a0163">EgoJEPA 为什么用人手运动差分，而不是先把人手轨迹硬映射成机器人关节？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aegojepa">EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Mohamed bin Zayed University of Artificial Intelligence</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>手部差分作为动作条件帮助预测未来视觉表示，把可迁移的变化规律与具体机器人执行接口分开。后续再适配目标机器人的输入输出，因此不需要先为每种具身设计完整关节映射；这并不表示无需机器人数据或无需控制适配。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如人类捏起物体的运动可提供状态变化线索，但五指机器人与双指夹爪仍须各自学习如何输出可执行控制。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20904">原论文</a> · <a href="../../../../foundation-models/2610.20904-egojepa/">实现解读</a> · <a href="#qa-eace4b99f19a0163">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:egojepa" data-paper-title="EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos 基础模型 Mohamed bin Zayed University of Artificial Intelligence 2026-10-14 人类第一视角视频中的手运动不需要经规则映射为每种机器人的动作。EgoJEPA先用手部运动差分条件JEPA预测未来视觉表示，再联合建模视觉与潜动作，最后仅适配目标机器人的输入输出动作接口。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地能力指标、训练结果或可执行 Evolve 算子。无本地adapter、指标文件或GPU回执，也不登记可执行Evolve算子。原论文结果仅作为阅读资料。范围见本轮实现与审查合同。本轮只完成方法、资源需求、公开代码状态及原图收录，没有运行完整实验、下载checkpoint或制造模拟能力分数。  JEPA与世界模型 具身多模态 多模态 视觉世界建模：状态、生成与动作条件 EgoJEPA 为什么先学习潜动作，而不把人的手部轨迹直接规则映射成机器人关节？ 人的手与机器人的执行器形态不同，硬映射容易把特定身体结构当成通用动作。方法先用运动差分条件学习与视觉变化相关的潜动作，再联合视觉建模，最后适配目标机器人的动作接口；可迁移的是作用关系，而不是假设两种关节坐标天然等价。 例如人的捏取动作和夹爪闭合角度不同，但都能导致杯子被拿起；先学这一状态变化，再适配夹爪的输入输出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-245e1f402013e420">EgoJEPA 为什么先学习潜动作，而不把人的手部轨迹直接规则映射成机器人关节？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aegojepa">EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Mohamed bin Zayed University of Artificial Intelligence</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>人的手与机器人的执行器形态不同，硬映射容易把特定身体结构当成通用动作。方法先用运动差分条件学习与视觉变化相关的潜动作，再联合视觉建模，最后适配目标机器人的动作接口；可迁移的是作用关系，而不是假设两种关节坐标天然等价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如人的捏取动作和夹爪闭合角度不同，但都能导致杯子被拿起；先学这一状态变化，再适配夹爪的输入输出。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20904">原论文</a> · <a href="../../../../foundation-models/2610.20904-egojepa/">实现解读</a> · <a href="#qa-245e1f402013e420">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:egojepa" data-paper-title="EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos 基础模型 Mohamed bin Zayed University of Artificial Intelligence 2026-10-14 人类第一视角视频中的手运动不需要经规则映射为每种机器人的动作。EgoJEPA先用手部运动差分条件JEPA预测未来视觉表示，再联合建模视觉与潜动作，最后仅适配目标机器人的输入输出动作接口。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地能力指标、训练结果或可执行 Evolve 算子。无本地adapter、指标文件或GPU回执，也不登记可执行Evolve算子。原论文结果仅作为阅读资料。范围见本轮实现与审查合同。本轮只完成方法、资源需求、公开代码状态及原图收录，没有运行完整实验、下载checkpoint或制造模拟能力分数。  JEPA与世界模型 具身多模态 多模态 视觉世界建模：状态、生成与动作条件 潜动作迁移与规则 retargeting 的假设差别是什么？ retargeting 显式规定人类动作如何对应机器人动作，依赖几何或关节关系；潜动作路线从视觉变化学习较抽象的行为表示，再由机器人接口解码。它减少硬映射依赖，也将难点转到表示学习与适配质量，不能据此断言任意新机器人都能零样本控制。 例如同一个“抓取”视觉变化可对应夹爪闭合或多指协同，潜动作不必提前指定每个关节的一一关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-9a0417ac0042303b">潜动作迁移与规则 retargeting 的假设差别是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aegojepa">EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Mohamed bin Zayed University of Artificial Intelligence</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>retargeting 显式规定人类动作如何对应机器人动作，依赖几何或关节关系；潜动作路线从视觉变化学习较抽象的行为表示，再由机器人接口解码。它减少硬映射依赖，也将难点转到表示学习与适配质量，不能据此断言任意新机器人都能零样本控制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一个“抓取”视觉变化可对应夹爪闭合或多指协同，潜动作不必提前指定每个关节的一一关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20904">原论文</a> · <a href="../../../../foundation-models/2610.20904-egojepa/">实现解读</a> · <a href="#qa-9a0417ac0042303b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:egojepa" data-paper-title="EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos 基础模型 Mohamed bin Zayed University of Artificial Intelligence 2026-10-14 人类第一视角视频中的手运动不需要经规则映射为每种机器人的动作。EgoJEPA先用手部运动差分条件JEPA预测未来视觉表示，再联合建模视觉与潜动作，最后仅适配目标机器人的输入输出动作接口。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地能力指标、训练结果或可执行 Evolve 算子。无本地adapter、指标文件或GPU回执，也不登记可执行Evolve算子。原论文结果仅作为阅读资料。范围见本轮实现与审查合同。本轮只完成方法、资源需求、公开代码状态及原图收录，没有运行完整实验、下载checkpoint或制造模拟能力分数。  JEPA与世界模型 具身多模态 多模态 视觉世界建模：状态、生成与动作条件 未来视觉目标在 JEPA 训练和实际控制时的可见性有什么区别？ 训练时真实未来帧经目标编码器提供停止梯度的表征，用于监督历史和手部差分条件预测；实际控制不能读取尚未发生的未来。当前本地只有方法和成本收录，无 adapter、指标或 GPU 回执，不能把公式说明当作真实机器人链路已实现。 例如给定前几帧预测拿起后的物体位置，目标帧只用于训练核对；部署时若直接输入该帧，就已提前泄露未来。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d9385b48d4f63672">未来视觉目标在 JEPA 训练和实际控制时的可见性有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aegojepa">EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Mohamed bin Zayed University of Artificial Intelligence</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>训练时真实未来帧经目标编码器提供停止梯度的表征，用于监督历史和手部差分条件预测；实际控制不能读取尚未发生的未来。当前本地只有方法和成本收录，无 adapter、指标或 GPU 回执，不能把公式说明当作真实机器人链路已实现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如给定前几帧预测拿起后的物体位置，目标帧只用于训练核对；部署时若直接输入该帧，就已提前泄露未来。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20904">原论文</a> · <a href="../../../../foundation-models/2610.20904-egojepa/">实现解读</a> · <a href="#qa-d9385b48d4f63672">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:esc" data-paper-title="ESC: Escaping 2D Diffusion Ambiguity with Geometric Constraints for Consistent Novel View Synthesis" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="ESC: Escaping 2D Diffusion Ambiguity with Geometric Constraints for Consistent Novel View Synthesis 基础模型 FAIR at Meta / Mila - Québec AI Institute / Université de Montréal 2026-10-14 单幅图像经扩散模型生成新视角时，2D视觉质量或相机姿态对齐不保证3D几何一致。ESC 联合生成 RGB 与逆深度，用 Plücker ray maps 条件化 Qwen MM-DiT，并以双向深度重投影约束 PCC 识别“物体消失”与“凭空出现”。推理时按 PCC 在多次随机生成中选优。 完整实验成本过高，不复现（审查 DONE）。未实现、未训练、未 GPU 验证。历史补发现，不是10月18日至21日的新首发。完整实验成本过高，不复现（审查 DONE）。本页没有可运行 adapter、没有本地效果指标，不进入自动训练或 Evolve 晋级队列。未实现、未训练、未 GPU 验证。本轮只有资料与算法边界收录，不提供伪 adapter、占位效果 JSON 或假 CUDA 回执。已核验固定 v1 正文、方法、架构图及 Appendix E.1 成本。  多模态基础模型 几何一致新视角生成 多模态 视觉世界建模：状态、生成与动作条件 新视角图像看起来真实，为什么仍可能不满足 ESC 关注的几何一致性？ 单张图像的视觉质量不保证它与源图共享同一三维场景，物体可能消失、重复或改变深度。ESC 联合生成 RGB 与逆深度，再用双向重投影检查几何，目的是把外观合理与跨视角一致分开；相机姿态对齐也不足以消除所有几何歧义。 例如新视角中的椅子纹理很逼真，却在应当可见的位置消失；只看图像美观或文本相似度可能察觉不到该问题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-esc-e793a8c8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9fcdef57f9d4db58">新视角图像看起来真实，为什么仍可能不满足 ESC 关注的几何一致性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aesc">ESC: Escaping 2D Diffusion Ambiguity with Geometric Constraints for Consistent Novel View Synthesis</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta / Mila - Québec AI Institute / Université de Montréal</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单张图像的视觉质量不保证它与源图共享同一三维场景，物体可能消失、重复或改变深度。ESC 联合生成 RGB 与逆深度，再用双向重投影检查几何，目的是把外观合理与跨视角一致分开；相机姿态对齐也不足以消除所有几何歧义。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如新视角中的椅子纹理很逼真，却在应当可见的位置消失；只看图像美观或文本相似度可能察觉不到该问题。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23732v1">原论文</a> · <a href="../../../../foundation-models/2610.23732-esc/">实现解读</a> · <a href="#qa-9fcdef57f9d4db58">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:esc" data-paper-title="ESC: Escaping 2D Diffusion Ambiguity with Geometric Constraints for Consistent Novel View Synthesis" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="ESC: Escaping 2D Diffusion Ambiguity with Geometric Constraints for Consistent Novel View Synthesis 基础模型 FAIR at Meta / Mila - Québec AI Institute / Université de Montréal 2026-10-14 单幅图像经扩散模型生成新视角时，2D视觉质量或相机姿态对齐不保证3D几何一致。ESC 联合生成 RGB 与逆深度，用 Plücker ray maps 条件化 Qwen MM-DiT，并以双向深度重投影约束 PCC 识别“物体消失”与“凭空出现”。推理时按 PCC 在多次随机生成中选优。 完整实验成本过高，不复现（审查 DONE）。未实现、未训练、未 GPU 验证。历史补发现，不是10月18日至21日的新首发。完整实验成本过高，不复现（审查 DONE）。本页没有可运行 adapter、没有本地效果指标，不进入自动训练或 Evolve 晋级队列。未实现、未训练、未 GPU 验证。本轮只有资料与算法边界收录，不提供伪 adapter、占位效果 JSON 或假 CUDA 回执。已核验固定 v1 正文、方法、架构图及 Appendix E.1 成本。  多模态基础模型 几何一致新视角生成 多模态 视觉世界建模：状态、生成与动作条件 为什么新视角图像看起来清晰、相机姿态也正确，仍可能不满足 PCC？ 外观逼真不约束两视角是否描述同一个三维场景。PCC 用深度重投影及可见性检查双向几何差，区分物体消失与凭空出现；遮挡和无效像素必须处理，不能用普通 RGB 差代替。Best-of-N 选优比较的是几何一致性，而非直接选择最漂亮的图片。 例如转动镜头后桌上的杯子消失，新图依旧自然清晰；双向深度重投影却会暴露这处不一致。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-fdc0872eefd4d85b">为什么新视角图像看起来清晰、相机姿态也正确，仍可能不满足 PCC？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aesc">ESC: Escaping 2D Diffusion Ambiguity with Geometric Constraints for Consistent Novel View Synthesis</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta / Mila - Québec AI Institute / Université de Montréal</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>外观逼真不约束两视角是否描述同一个三维场景。PCC 用深度重投影及可见性检查双向几何差，区分物体消失与凭空出现；遮挡和无效像素必须处理，不能用普通 RGB 差代替。Best-of-N 选优比较的是几何一致性，而非直接选择最漂亮的图片。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如转动镜头后桌上的杯子消失，新图依旧自然清晰；双向深度重投影却会暴露这处不一致。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23732v1">原论文</a> · <a href="../../../../foundation-models/2610.23732-esc/">实现解读</a> · <a href="#qa-fdc0872eefd4d85b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:esc" data-paper-title="ESC: Escaping 2D Diffusion Ambiguity with Geometric Constraints for Consistent Novel View Synthesis" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="ESC: Escaping 2D Diffusion Ambiguity with Geometric Constraints for Consistent Novel View Synthesis 基础模型 FAIR at Meta / Mila - Québec AI Institute / Université de Montréal 2026-10-14 单幅图像经扩散模型生成新视角时，2D视觉质量或相机姿态对齐不保证3D几何一致。ESC 联合生成 RGB 与逆深度，用 Plücker ray maps 条件化 Qwen MM-DiT，并以双向深度重投影约束 PCC 识别“物体消失”与“凭空出现”。推理时按 PCC 在多次随机生成中选优。 完整实验成本过高，不复现（审查 DONE）。未实现、未训练、未 GPU 验证。历史补发现，不是10月18日至21日的新首发。完整实验成本过高，不复现（审查 DONE）。本页没有可运行 adapter、没有本地效果指标，不进入自动训练或 Evolve 晋级队列。未实现、未训练、未 GPU 验证。本轮只有资料与算法边界收录，不提供伪 adapter、占位效果 JSON 或假 CUDA 回执。已核验固定 v1 正文、方法、架构图及 Appendix E.1 成本。  多模态基础模型 几何一致新视角生成 多模态 视觉世界建模：状态、生成与动作条件 PCC Best-of-N 与按 RGB 相似度选最像源图的候选有什么不同？ 新视角本来就应改变像素外观，RGB 相似不能直接代表几何正确。PCC 使用源与目标深度的双向投影、遮挡和有效覆盖判断缺失与幻觉几何，并选择分数最小的候选；它衡量特定几何约束，不保证所有图像质量指标同时最优。 例如相机转到桌子另一侧，正确图像与源图像素差很大；重复源图可能 RGB 更近，却不符合目标视角。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-da2aafe8b40641a0">PCC Best-of-N 与按 RGB 相似度选最像源图的候选有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aesc">ESC: Escaping 2D Diffusion Ambiguity with Geometric Constraints for Consistent Novel View Synthesis</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta / Mila - Québec AI Institute / Université de Montréal</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>新视角本来就应改变像素外观，RGB 相似不能直接代表几何正确。PCC 使用源与目标深度的双向投影、遮挡和有效覆盖判断缺失与幻觉几何，并选择分数最小的候选；它衡量特定几何约束，不保证所有图像质量指标同时最优。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如相机转到桌子另一侧，正确图像与源图像素差很大；重复源图可能 RGB 更近，却不符合目标视角。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23732v1">原论文</a> · <a href="../../../../foundation-models/2610.23732-esc/">实现解读</a> · <a href="#qa-da2aafe8b40641a0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:esc" data-paper-title="ESC: Escaping 2D Diffusion Ambiguity with Geometric Constraints for Consistent Novel View Synthesis" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="ESC: Escaping 2D Diffusion Ambiguity with Geometric Constraints for Consistent Novel View Synthesis 基础模型 FAIR at Meta / Mila - Québec AI Institute / Université de Montréal 2026-10-14 单幅图像经扩散模型生成新视角时，2D视觉质量或相机姿态对齐不保证3D几何一致。ESC 联合生成 RGB 与逆深度，用 Plücker ray maps 条件化 Qwen MM-DiT，并以双向深度重投影约束 PCC 识别“物体消失”与“凭空出现”。推理时按 PCC 在多次随机生成中选优。 完整实验成本过高，不复现（审查 DONE）。未实现、未训练、未 GPU 验证。历史补发现，不是10月18日至21日的新首发。完整实验成本过高，不复现（审查 DONE）。本页没有可运行 adapter、没有本地效果指标，不进入自动训练或 Evolve 晋级队列。未实现、未训练、未 GPU 验证。本轮只有资料与算法边界收录，不提供伪 adapter、占位效果 JSON 或假 CUDA 回执。已核验固定 v1 正文、方法、架构图及 Appendix E.1 成本。  多模态基础模型 几何一致新视角生成 多模态 视觉世界建模：状态、生成与动作条件 重投影计算为什么必须包含 z-buffer 和有效像素 mask？ 多个源点投到同一目标像素时要处理遮挡，负深度、越界或无源深度点也不能当有效误差。PCC 还含阈值、对数压缩、裁剪与覆盖归一化，不是简单绝对深度差。当前未实现或训练 ESC，本地没有可用能力指标。 例如墙后物体在目标视角被遮住，不应因缺少可见对应就算作消失；忽略遮挡会把正确几何当成失败。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-80733d2366c21114">重投影计算为什么必须包含 z-buffer 和有效像素 mask？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aesc">ESC: Escaping 2D Diffusion Ambiguity with Geometric Constraints for Consistent Novel View Synthesis</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta / Mila - Québec AI Institute / Université de Montréal</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多个源点投到同一目标像素时要处理遮挡，负深度、越界或无源深度点也不能当有效误差。PCC 还含阈值、对数压缩、裁剪与覆盖归一化，不是简单绝对深度差。当前未实现或训练 ESC，本地没有可用能力指标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如墙后物体在目标视角被遮住，不应因缺少可见对应就算作消失；忽略遮挡会把正确几何当成失败。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23732v1">原论文</a> · <a href="../../../../foundation-models/2610.23732-esc/">实现解读</a> · <a href="#qa-80733d2366c21114">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jepa-prediction-planning" data-paper-title="One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models 基础模型 论文未列机构 2026-10-14 JEPA 在自己的潜空间预测下一观察，较小的一步 loss 不一定表示更好的长程行动。论文固定一个只在真实观察编码上拟合的物理状态解码器，分别解码真实下一表征与预测下一表征，把编码器本身的可读性和预测器新增的误差拆开。规划仍用相同 checkpoint、相同任务和配对种子单独执行，不能由预测指标推导成功率。 原文三个环境的世界模型重训、每环境多训练/解码/规划种子和完整 MPC：成本过高，不复现（审查 DONE）。CPU 接口实测保存真实解码器拟合与受控输入的诊断指标，不代表世界模型能力。本地对照口径：共享状态规范与归一化、同一冻结解码器；输入必须来自相同 transition。世界模型预测与外部规划分别评价，不自动接入 Evolve 选择。  世界模型评测 冻结物理状态解码器 预测与规划配对比较 多模态 视觉世界建模：状态、生成与动作条件 为什么要先检查真实下一表征本身能否解码物理状态？ 预测 latent 的物理误差既包含编码器信息损失，也包含预测器新增偏差。用同一个只在真实观察表征上训练的冻结解码器，分别评真实与预测下一表征，才能拆开这两部分；否则编码器可读性变化可能被误认为动力学预测改善。 例如真实 latent 已经丢掉物体角度，即使预测器完全复制真实 latent，解码角度仍会错，不能把这全算预测器失败。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-jepa-prediction-planning-96c625cf" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c84d7475eab03391">为什么要先检查真实下一表征本身能否解码物理状态？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ajepa-prediction-planning">One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>预测 latent 的物理误差既包含编码器信息损失，也包含预测器新增偏差。用同一个只在真实观察表征上训练的冻结解码器，分别评真实与预测下一表征，才能拆开这两部分；否则编码器可读性变化可能被误认为动力学预测改善。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如真实 latent 已经丢掉物体角度，即使预测器完全复制真实 latent，解码角度仍会错，不能把这全算预测器失败。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19375v1">原论文</a> · <a href="../../../../foundation-models/2610.19375-jepa-prediction-planning/">实现解读</a> · <a href="#qa-c84d7475eab03391">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jepa-prediction-planning" data-paper-title="One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models 基础模型 论文未列机构 2026-10-14 JEPA 在自己的潜空间预测下一观察，较小的一步 loss 不一定表示更好的长程行动。论文固定一个只在真实观察编码上拟合的物理状态解码器，分别解码真实下一表征与预测下一表征，把编码器本身的可读性和预测器新增的误差拆开。规划仍用相同 checkpoint、相同任务和配对种子单独执行，不能由预测指标推导成功率。 原文三个环境的世界模型重训、每环境多训练/解码/规划种子和完整 MPC：成本过高，不复现（审查 DONE）。CPU 接口实测保存真实解码器拟合与受控输入的诊断指标，不代表世界模型能力。本地对照口径：共享状态规范与归一化、同一冻结解码器；输入必须来自相同 transition。世界模型预测与外部规划分别评价，不自动接入 Evolve 选择。  世界模型评测 冻结物理状态解码器 预测与规划配对比较 多模态 视觉世界建模：状态、生成与动作条件 为什么要从预测状态误差中减去真实表征经同一解码器得到的误差？ 解码误差同时混合编码器可读性、解码器不足和预测器偏差。固定同一解码器，先测真实下一表征，再测预测下一表征，差值更接近预测环节新增的影响；它可能为负，不能截零。即便差值小，长程规划成功率仍需独立配对验证。 例如解码器本来就把位置估错两格，预测表征又错三格；不能把全部三格都归因预测器，应先扣除真实表征的基础误差。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c221d8dad06e5450">为什么要从预测状态误差中减去真实表征经同一解码器得到的误差？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ajepa-prediction-planning">One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>解码误差同时混合编码器可读性、解码器不足和预测器偏差。固定同一解码器，先测真实下一表征，再测预测下一表征，差值更接近预测环节新增的影响；它可能为负，不能截零。即便差值小，长程规划成功率仍需独立配对验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如解码器本来就把位置估错两格，预测表征又错三格；不能把全部三格都归因预测器，应先扣除真实表征的基础误差。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19375v1">原论文</a> · <a href="../../../../foundation-models/2610.19375-jepa-prediction-planning/">实现解读</a> · <a href="#qa-c221d8dad06e5450">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jepa-prediction-planning" data-paper-title="One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models 基础模型 论文未列机构 2026-10-14 JEPA 在自己的潜空间预测下一观察，较小的一步 loss 不一定表示更好的长程行动。论文固定一个只在真实观察编码上拟合的物理状态解码器，分别解码真实下一表征与预测下一表征，把编码器本身的可读性和预测器新增的误差拆开。规划仍用相同 checkpoint、相同任务和配对种子单独执行，不能由预测指标推导成功率。 原文三个环境的世界模型重训、每环境多训练/解码/规划种子和完整 MPC：成本过高，不复现（审查 DONE）。CPU 接口实测保存真实解码器拟合与受控输入的诊断指标，不代表世界模型能力。本地对照口径：共享状态规范与归一化、同一冻结解码器；输入必须来自相同 transition。世界模型预测与外部规划分别评价，不自动接入 Evolve 选择。  世界模型评测 冻结物理状态解码器 预测与规划配对比较 多模态 视觉世界建模：状态、生成与动作条件 一步物理预测误差下降与规划成功率提升为什么需要分开测？ 规划反复调用模型，误差可能累积、偏向关键动作或改变搜索路径；一步平均误差无法表达这些闭环影响。应在同一 checkpoint、任务和配对种子上实际运行规划，再比较成功率，不能由一个预测指标自动推导行动能力。 例如模型在常见静止状态更准，却在碰撞附近稍错，整体一步误差下降仍可能让规划频繁撞墙。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-dedb423059826135">一步物理预测误差下降与规划成功率提升为什么需要分开测？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ajepa-prediction-planning">One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>规划反复调用模型，误差可能累积、偏向关键动作或改变搜索路径；一步平均误差无法表达这些闭环影响。应在同一 checkpoint、任务和配对种子上实际运行规划，再比较成功率，不能由一个预测指标自动推导行动能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型在常见静止状态更准，却在碰撞附近稍错，整体一步误差下降仍可能让规划频繁撞墙。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19375v1">原论文</a> · <a href="../../../../foundation-models/2610.19375-jepa-prediction-planning/">实现解读</a> · <a href="#qa-dedb423059826135">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jepa-prediction-planning" data-paper-title="One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models 基础模型 论文未列机构 2026-10-14 JEPA 在自己的潜空间预测下一观察，较小的一步 loss 不一定表示更好的长程行动。论文固定一个只在真实观察编码上拟合的物理状态解码器，分别解码真实下一表征与预测下一表征，把编码器本身的可读性和预测器新增的误差拆开。规划仍用相同 checkpoint、相同任务和配对种子单独执行，不能由预测指标推导成功率。 原文三个环境的世界模型重训、每环境多训练/解码/规划种子和完整 MPC：成本过高，不复现（审查 DONE）。CPU 接口实测保存真实解码器拟合与受控输入的诊断指标，不代表世界模型能力。本地对照口径：共享状态规范与归一化、同一冻结解码器；输入必须来自相同 transition。世界模型预测与外部规划分别评价，不自动接入 Evolve 选择。  世界模型评测 冻结物理状态解码器 预测与规划配对比较 多模态 视觉世界建模：状态、生成与动作条件 E_excess 为负时应截成零吗？ 不应。它定义为预测表征解码误差减真实表征解码误差，预测表示偶然更适合冻结解码器时差值可为负。两种表示完全相同则差值必须为零；状态归一化方差只由共享训练数据确定，解码器不能用预测 test 表征重新拟合。 例如真实表征误差为三、预测为二，差值应为负一；截零会改变定义并掩盖解码器外推现象。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-cd7787052f6ef35f">E_excess 为负时应截成零吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ajepa-prediction-planning">One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不应。它定义为预测表征解码误差减真实表征解码误差，预测表示偶然更适合冻结解码器时差值可为负。两种表示完全相同则差值必须为零；状态归一化方差只由共享训练数据确定，解码器不能用预测 test 表征重新拟合。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如真实表征误差为三、预测为二，差值应为负一；截零会改变定义并掩盖解码器外推现象。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、聚合、结果与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19375v1">原论文</a> · <a href="../../../../foundation-models/2610.19375-jepa-prediction-planning/">实现解读</a> · <a href="#qa-cd7787052f6ef35f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:oob-regularization" data-paper-title="Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning 基础模型 European Molecular Biology Laboratory (EMBL) 2026-10-14 联合嵌入自监督学习一方面拉近同一图像的不同增强视图，另一方面用抗坍塌正则保持表示多样性。小 batch 对整个表示分布的估计可能很差；单纯增大 GPU batch 又受显存限制。OOB 把“统计范围”与“本次优化 batch”解耦：定期编码整个训练集，按全数据分布构建每个样本的固定目标，再存入 CPU。在线训练只读取当前样本对应的锚点，不在每一步重新估计全数据正则。Gaussian 变体沿随机单位方向投影，把每列样本排序后匹配标准正态分位数； 完整原研究为成本过高，不复现（审查 DONE）。先核验 MD5 c99cafc152244af753f735de768cd75f，再解析官方 pickle，拒绝任意未验证 pickle。本地实现两种真实锚点算法，并在有限的官方 CIFAR 图像上执行有对照的训练。它不是原论文多数据集、100 epochs 的完整研究；短预算的负结果照实保留，不进入 Evolve 自动晋级。完整原研究为成本过高，不复现（审查 DONE）。本地对照口径：基线为同投影 / 分位数口径的 in-batch Gaussian 及 SimCLR；  self-supervised-learning joint-embedding small-batch representation-learning 多模态 视觉世界建模：状态、生成与动作条件 OOB 中“全数据统计”和“当前优化 batch”为什么可以分开？ 周期性编码整个训练集后，按稳定样本索引构建并缓存固定锚点；每次梯度更新只读取当前样本的锚点。统计覆盖因此可以大于 GPU batch，但锚点会随编码器变化而陈旧，需要按刷新规则重建；训练集以外的标签或表示不能混入构建。 例如 GPU 一次只能处理八张图，仍可每隔一段训练遍历五百张训练图建锚点，再为每个八张 batch 查对应目标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-oob-regularization-98328dd1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-24c359d6bb05f722">OOB 中“全数据统计”和“当前优化 batch”为什么可以分开？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aoob-regularization">Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · European Molecular Biology Laboratory (EMBL)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>周期性编码整个训练集后，按稳定样本索引构建并缓存固定锚点；每次梯度更新只读取当前样本的锚点。统计覆盖因此可以大于 GPU batch，但锚点会随编码器变化而陈旧，需要按刷新规则重建；训练集以外的标签或表示不能混入构建。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 GPU 一次只能处理八张图，仍可每隔一段训练遍历五百张训练图建锚点，再为每个八张 batch 查对应目标。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20158">原论文</a> · <a href="../../../../reproductions/2610.20158-oob-regularization/">实现解读</a> · <a href="#qa-24c359d6bb05f722">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:oob-regularization" data-paper-title="Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning 基础模型 European Molecular Biology Laboratory (EMBL) 2026-10-14 联合嵌入自监督学习一方面拉近同一图像的不同增强视图，另一方面用抗坍塌正则保持表示多样性。小 batch 对整个表示分布的估计可能很差；单纯增大 GPU batch 又受显存限制。OOB 把“统计范围”与“本次优化 batch”解耦：定期编码整个训练集，按全数据分布构建每个样本的固定目标，再存入 CPU。在线训练只读取当前样本对应的锚点，不在每一步重新估计全数据正则。Gaussian 变体沿随机单位方向投影，把每列样本排序后匹配标准正态分位数； 完整原研究为成本过高，不复现（审查 DONE）。先核验 MD5 c99cafc152244af753f735de768cd75f，再解析官方 pickle，拒绝任意未验证 pickle。本地实现两种真实锚点算法，并在有限的官方 CIFAR 图像上执行有对照的训练。它不是原论文多数据集、100 epochs 的完整研究；短预算的负结果照实保留，不进入 Evolve 自动晋级。完整原研究为成本过高，不复现（审查 DONE）。本地对照口径：基线为同投影 / 分位数口径的 in-batch Gaussian 及 SimCLR；  self-supervised-learning joint-embedding small-batch representation-learning 多模态 视觉世界建模：状态、生成与动作条件 OOB 为什么能让小 batch 使用接近全数据范围的抗坍塌监督？ 它把全数据统计与在线优化分开：定期编码训练集并建立每样本锚点，随后小 batch 读取对应固定目标。这样在线更新无需每步重新估计完整分布，但锚点会随模型变化而陈旧，需要刷新；这不同于直接在小 batch 上计算普通方差或协方差损失。 例如显存一次只能放八张图，仍可事先用全训练集生成排序分位数目标，再让这八张各自匹配自己的缓存锚点。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-39f15ae4c6df1bd0">OOB 为什么能让小 batch 使用接近全数据范围的抗坍塌监督？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aoob-regularization">Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · European Molecular Biology Laboratory (EMBL)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它把全数据统计与在线优化分开：定期编码训练集并建立每样本锚点，随后小 batch 读取对应固定目标。这样在线更新无需每步重新估计完整分布，但锚点会随模型变化而陈旧，需要刷新；这不同于直接在小 batch 上计算普通方差或协方差损失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如显存一次只能放八张图，仍可事先用全训练集生成排序分位数目标，再让这八张各自匹配自己的缓存锚点。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20158">原论文</a> · <a href="../../../../reproductions/2610.20158-oob-regularization/">实现解读</a> · <a href="#qa-39f15ae4c6df1bd0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:oob-regularization" data-paper-title="Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning 基础模型 European Molecular Biology Laboratory (EMBL) 2026-10-14 联合嵌入自监督学习一方面拉近同一图像的不同增强视图，另一方面用抗坍塌正则保持表示多样性。小 batch 对整个表示分布的估计可能很差；单纯增大 GPU batch 又受显存限制。OOB 把“统计范围”与“本次优化 batch”解耦：定期编码整个训练集，按全数据分布构建每个样本的固定目标，再存入 CPU。在线训练只读取当前样本对应的锚点，不在每一步重新估计全数据正则。Gaussian 变体沿随机单位方向投影，把每列样本排序后匹配标准正态分位数； 完整原研究为成本过高，不复现（审查 DONE）。先核验 MD5 c99cafc152244af753f735de768cd75f，再解析官方 pickle，拒绝任意未验证 pickle。本地实现两种真实锚点算法，并在有限的官方 CIFAR 图像上执行有对照的训练。它不是原论文多数据集、100 epochs 的完整研究；短预算的负结果照实保留，不进入 Evolve 自动晋级。完整原研究为成本过高，不复现（审查 DONE）。本地对照口径：基线为同投影 / 分位数口径的 in-batch Gaussian 及 SimCLR；  self-supervised-learning joint-embedding small-batch representation-learning 多模态 视觉世界建模：状态、生成与动作条件 Gaussian sorted-quantile 目标与只约束均值零、方差一有何不同？ 排序分位数为每个样本沿随机方向分配正态目标，约束投影分布及样本对应；均值方差只约束少数矩，许多不同分布都满足。该目标也不是原始 Epps–Pulley 统计量，配对基线应使用同一分位数口径，避免把损失差异误作范围收益。 例如一半样本在负一、一半在正一也可均值零方差一，却不是正态分位数排列；锚点目标会区分两种分布。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-62e96fc660a402dc">Gaussian sorted-quantile 目标与只约束均值零、方差一有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aoob-regularization">Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · European Molecular Biology Laboratory (EMBL)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>排序分位数为每个样本沿随机方向分配正态目标，约束投影分布及样本对应；均值方差只约束少数矩，许多不同分布都满足。该目标也不是原始 Epps–Pulley 统计量，配对基线应使用同一分位数口径，避免把损失差异误作范围收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一半样本在负一、一半在正一也可均值零方差一，却不是正态分位数排列；锚点目标会区分两种分布。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20158">原论文</a> · <a href="../../../../reproductions/2610.20158-oob-regularization/">实现解读</a> · <a href="#qa-62e96fc660a402dc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:oob-regularization" data-paper-title="Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning 基础模型 European Molecular Biology Laboratory (EMBL) 2026-10-14 联合嵌入自监督学习一方面拉近同一图像的不同增强视图，另一方面用抗坍塌正则保持表示多样性。小 batch 对整个表示分布的估计可能很差；单纯增大 GPU batch 又受显存限制。OOB 把“统计范围”与“本次优化 batch”解耦：定期编码整个训练集，按全数据分布构建每个样本的固定目标，再存入 CPU。在线训练只读取当前样本对应的锚点，不在每一步重新估计全数据正则。Gaussian 变体沿随机单位方向投影，把每列样本排序后匹配标准正态分位数； 完整原研究为成本过高，不复现（审查 DONE）。先核验 MD5 c99cafc152244af753f735de768cd75f，再解析官方 pickle，拒绝任意未验证 pickle。本地实现两种真实锚点算法，并在有限的官方 CIFAR 图像上执行有对照的训练。它不是原论文多数据集、100 epochs 的完整研究；短预算的负结果照实保留，不进入 Evolve 自动晋级。完整原研究为成本过高，不复现（审查 DONE）。本地对照口径：基线为同投影 / 分位数口径的 in-batch Gaussian 及 SimCLR；  self-supervised-learning joint-embedding small-batch representation-learning 多模态 视觉世界建模：状态、生成与动作条件 锚点刷新的方向、目标和梯度应怎样隔离？ 刷新后投影方向和按样本分配的目标固定，detach 后存 CPU，在线损失对 B、视图数 V、方向数 M 归一化，不通过锚点反传到刷新阶段。球面变体另优化单位锚点，不能替换为 Gaussian 目标；稳定索引丢失会把样本配到错误锚点。 例如数据加载器打乱顺序后仍需按原样本 ID 查锚点，不能把缓存第一个目标直接给当前 batch 的第一张图。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-5fcebfd43f84ed2a">锚点刷新的方向、目标和梯度应怎样隔离？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aoob-regularization">Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · European Molecular Biology Laboratory (EMBL)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>刷新后投影方向和按样本分配的目标固定，detach 后存 CPU，在线损失对 B、视图数 V、方向数 M 归一化，不通过锚点反传到刷新阶段。球面变体另优化单位锚点，不能替换为 Gaussian 目标；稳定索引丢失会把样本配到错误锚点。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如数据加载器打乱顺序后仍需按原样本 ID 查锚点，不能把缓存第一个目标直接给当前 batch 的第一张图。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界与成本结论；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20158">原论文</a> · <a href="../../../../reproductions/2610.20158-oob-regularization/">实现解读</a> · <a href="#qa-5fcebfd43f84ed2a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:time-jepa" data-paper-title="Time-JEPA: Grounding Video World Models with Physical Time Series" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Time-JEPA: Grounding Video World Models with Physical Time Series 基础模型 Harbin Institute of Technology 2026-10-14 视频自监督目标不必保留精确的速度、关节角等物理状态。Time-JEPA 用同步传感器或标注作辅助目标，但它们不是编码器输入：训练时同一个 online encoder 分别处理 masked 上下文和 unmasked 视频，评测移除物理态 head，仍只输入视频。 完整实验成本过高，不复现（审查 DONE）。CPU与真实单张A100的42/43/44三seed诊断已完成。实现不只封装 loss：包含时间戳 nearest 对齐、逐变量 valid tubelet 池化、训练独占统计、真正的上下文 self-attention encoder、masked latent predictor、unmasked 两层物理 head、冻结 target 和显式 EMA 更新。nearest 的距离阈值由调用方传入、平局取较早测量，是本地明确的对齐策略，不冒充所有原始数据集的具体解码流程。  JEPA与世界模型 物理时序监督 多模态 视觉世界建模：状态、生成与动作条件 Time-JEPA 在评测时为什么仍可只输入视频？ 传感器或物理时序是训练辅助目标，不是编码器输入。共享 online encoder 从 unmasked 视频特征预测物理变量，masked 分支同时做 JEPA；评测移除物理 head 后只保留视频路径，因此不能把方法描述为推理时额外获得真实速度或关节角。 例如训练用同步速度计监督车辆视频表示，部署看视频估计状态时不能再把速度计真值作为输入，否则已改变协议。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-time-jepa-c002ea0d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4391c33e37078638">Time-JEPA 在评测时为什么仍可只输入视频？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atime-jepa">Time-JEPA: Grounding Video World Models with Physical Time Series</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>传感器或物理时序是训练辅助目标，不是编码器输入。共享 online encoder 从 unmasked 视频特征预测物理变量，masked 分支同时做 JEPA；评测移除物理 head 后只保留视频路径，因此不能把方法描述为推理时额外获得真实速度或关节角。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如训练用同步速度计监督车辆视频表示，部署看视频估计状态时不能再把速度计真值作为输入，否则已改变协议。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与隔离要求；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23982">原论文</a> · <a href="../../../../foundation-models/2610.23982-time-jepa/">实现解读</a> · <a href="#qa-4391c33e37078638">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:time-jepa" data-paper-title="Time-JEPA: Grounding Video World Models with Physical Time Series" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Time-JEPA: Grounding Video World Models with Physical Time Series 基础模型 Harbin Institute of Technology 2026-10-14 视频自监督目标不必保留精确的速度、关节角等物理状态。Time-JEPA 用同步传感器或标注作辅助目标，但它们不是编码器输入：训练时同一个 online encoder 分别处理 masked 上下文和 unmasked 视频，评测移除物理态 head，仍只输入视频。 完整实验成本过高，不复现（审查 DONE）。CPU与真实单张A100的42/43/44三seed诊断已完成。实现不只封装 loss：包含时间戳 nearest 对齐、逐变量 valid tubelet 池化、训练独占统计、真正的上下文 self-attention encoder、masked latent predictor、unmasked 两层物理 head、冻结 target 和显式 EMA 更新。nearest 的距离阈值由调用方传入、平局取较早测量，是本地明确的对齐策略，不冒充所有原始数据集的具体解码流程。  JEPA与世界模型 物理时序监督 多模态 视觉世界建模：状态、生成与动作条件 物理时间序列只作训练标签，为何还能改善仅输入视频的编码器？ 辅助头把视频表示映射到速度或关节角，误差反向推动编码器保留这些物理信息，部署时可以删除该头。传感器不进入输入，因此评测仍是视频任务；无效帧要保持掩码，归一化统计也只能来自训练集，避免伪造零标签或测试泄漏。 例如训练时用同步速度监督视频表示，测试只给运动画面；若把速度数值直接拼进测试输入，就变成不同任务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-045efa8d388d00cd">物理时间序列只作训练标签，为何还能改善仅输入视频的编码器？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atime-jepa">Time-JEPA: Grounding Video World Models with Physical Time Series</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>辅助头把视频表示映射到速度或关节角，误差反向推动编码器保留这些物理信息，部署时可以删除该头。传感器不进入输入，因此评测仍是视频任务；无效帧要保持掩码，归一化统计也只能来自训练集，避免伪造零标签或测试泄漏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如训练时用同步速度监督视频表示，测试只给运动画面；若把速度数值直接拼进测试输入，就变成不同任务。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与隔离要求；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23982">原论文</a> · <a href="../../../../foundation-models/2610.23982-time-jepa/">实现解读</a> · <a href="#qa-045efa8d388d00cd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:time-jepa" data-paper-title="Time-JEPA: Grounding Video World Models with Physical Time Series" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Time-JEPA: Grounding Video World Models with Physical Time Series 基础模型 Harbin Institute of Technology 2026-10-14 视频自监督目标不必保留精确的速度、关节角等物理状态。Time-JEPA 用同步传感器或标注作辅助目标，但它们不是编码器输入：训练时同一个 online encoder 分别处理 masked 上下文和 unmasked 视频，评测移除物理态 head，仍只输入视频。 完整实验成本过高，不复现（审查 DONE）。CPU与真实单张A100的42/43/44三seed诊断已完成。实现不只封装 loss：包含时间戳 nearest 对齐、逐变量 valid tubelet 池化、训练独占统计、真正的上下文 self-attention encoder、masked latent predictor、unmasked 两层物理 head、冻结 target 和显式 EMA 更新。nearest 的距离阈值由调用方传入、平局取较早测量，是本地明确的对齐策略，不冒充所有原始数据集的具体解码流程。  JEPA与世界模型 物理时序监督 多模态 视觉世界建模：状态、生成与动作条件 辅助物理目标与只做 masked latent prediction 约束什么不同信息？ masked latent 预测鼓励表征可预测，却未必保留精确物理量；同步物理监督直接推动同一 encoder 保留这些变量。它可能改善物理可读性，但仍受变量覆盖与跨域分布影响，不能将一个域的探针结果推广为所有物理任务或控制能力。 例如视频模型能补全道路纹理，却忽略速度微差；训练专用速度目标会直接要求表示区分这类差异。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-bfed14e3e777d72b">辅助物理目标与只做 masked latent prediction 约束什么不同信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atime-jepa">Time-JEPA: Grounding Video World Models with Physical Time Series</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>masked latent 预测鼓励表征可预测，却未必保留精确物理量；同步物理监督直接推动同一 encoder 保留这些变量。它可能改善物理可读性，但仍受变量覆盖与跨域分布影响，不能将一个域的探针结果推广为所有物理任务或控制能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如视频模型能补全道路纹理，却忽略速度微差；训练专用速度目标会直接要求表示区分这类差异。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与隔离要求；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23982">原论文</a> · <a href="../../../../foundation-models/2610.23982-time-jepa/">实现解读</a> · <a href="#qa-bfed14e3e777d72b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:time-jepa" data-paper-title="Time-JEPA: Grounding Video World Models with Physical Time Series" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Time-JEPA: Grounding Video World Models with Physical Time Series 基础模型 Harbin Institute of Technology 2026-10-14 视频自监督目标不必保留精确的速度、关节角等物理状态。Time-JEPA 用同步传感器或标注作辅助目标，但它们不是编码器输入：训练时同一个 online encoder 分别处理 masked 上下文和 unmasked 视频，评测移除物理态 head，仍只输入视频。 完整实验成本过高，不复现（审查 DONE）。CPU与真实单张A100的42/43/44三seed诊断已完成。实现不只封装 loss：包含时间戳 nearest 对齐、逐变量 valid tubelet 池化、训练独占统计、真正的上下文 self-attention encoder、masked latent predictor、unmasked 两层物理 head、冻结 target 和显式 EMA 更新。nearest 的距离阈值由调用方传入、平局取较早测量，是本地明确的对齐策略，不冒充所有原始数据集的具体解码流程。  JEPA与世界模型 物理时序监督 多模态 视觉世界建模：状态、生成与动作条件 tubelet 内某变量完全缺测时，能否补成有效零标签？ 不能。每个变量独立按 valid 帧求均值，空 tubelet 仍无效；归一化均值方差仅在训练集拟合并冻结。物理损失只在有效项上求 SmoothL1，β 为 0.5；不同域还各有 head、统计和权重，不能混成同一无条件标签空间。 例如两帧都没测到关节角，填零会把未知误当真实零角度；正确做法是让该变量该 tubelet 不贡献监督。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-4693c64708e6cbb5">tubelet 内某变量完全缺测时，能否补成有效零标签？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atime-jepa">Time-JEPA: Grounding Video World Models with Physical Time Series</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。每个变量独立按 valid 帧求均值，空 tubelet 仍无效；归一化均值方差仅在训练集拟合并冻结。物理损失只在有效项上求 SmoothL1，β 为 0.5；不同域还各有 head、统计和权重，不能混成同一无条件标签空间。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两帧都没测到关节角，填零会把未知误当真实零角度；正确做法是让该变量该 tubelet 不贡献监督。</p>
<p class="ar-learning-sources">依据：核心公式与隔离要求、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23982">原论文</a> · <a href="../../../../foundation-models/2610.23982-time-jepa/">实现解读</a> · <a href="#qa-4693c64708e6cbb5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ev-jepa" data-paper-title="EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference 基础模型 Meta Reality Labs Research 2026-10-09 固定容量的视频模型难以同时适配端侧预算和跨设备协作，独立训练不同宽度也不保证中间表示兼容。EV-JEPA共享嵌套宽度参数，每步联合训练窄、宽与窄转宽三条路径，以冻结视频教师约束共同表示空间，并增加可调token压缩。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文§4.1：128 GPU、300epochs，Kinetics-710/SSv2/HowTo100M视频，冻结V-JEPA2 ViT-G教师；每步同时训练窄、宽、混合三路径。压缩器另需100epochs×300iterations、全局batch4096。不是本地测速，原预算显著超出单卡A100/A30或Mac；不下载全视频或尝试多臂训练。  jepa video-representation elastic-inference 多模态 视觉世界建模：状态、生成与动作条件 嵌套宽度共享参数与分别训练多个尺寸模型有什么不同？ 窄路径使用宽模型通道的嵌套切片，多个宽度在同一训练中共享参数，可适配不同设备预算。独立训练模型没有天然的中间表示兼容性；共享本身也不保证兼容，因此 EV-JEPA 还显式训练窄转宽混合路径并对齐固定教师。 例如端侧先用窄通道计算，再把中间状态交给较宽服务器继续，接口需要在训练中见过这种切换。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-ev-jepa-12c252ce" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-fd62dd8be67749b5">嵌套宽度共享参数与分别训练多个尺寸模型有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aev-jepa">EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Reality Labs Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>窄路径使用宽模型通道的嵌套切片，多个宽度在同一训练中共享参数，可适配不同设备预算。独立训练模型没有天然的中间表示兼容性；共享本身也不保证兼容，因此 EV-JEPA 还显式训练窄转宽混合路径并对齐固定教师。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如端侧先用窄通道计算，再把中间状态交给较宽服务器继续，接口需要在训练中见过这种切换。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14324">原论文</a> · <a href="../../../../reproductions/2610.14324-ev-jepa/">实现解读</a> · <a href="#qa-fd62dd8be67749b5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ev-jepa" data-paper-title="EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference 基础模型 Meta Reality Labs Research 2026-10-09 固定容量的视频模型难以同时适配端侧预算和跨设备协作，独立训练不同宽度也不保证中间表示兼容。EV-JEPA共享嵌套宽度参数，每步联合训练窄、宽与窄转宽三条路径，以冻结视频教师约束共同表示空间，并增加可调token压缩。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文§4.1：128 GPU、300epochs，Kinetics-710/SSv2/HowTo100M视频，冻结V-JEPA2 ViT-G教师；每步同时训练窄、宽、混合三路径。压缩器另需100epochs×300iterations、全局batch4096。不是本地测速，原预算显著超出单卡A100/A30或Mac；不下载全视频或尝试多臂训练。  jepa video-representation elastic-inference 多模态 视觉世界建模：状态、生成与动作条件 为何训练窄模型和宽模型之外，还要专门训练“窄转宽”路径？ 两种宽度各自表现好，不保证窄模型中间状态可直接交给宽模型。混合路径显式训练切分层的升宽接口，并以共同冻结教师约束表示，使跨设备接力有训练依据；这与随意裁剪通道或在运行时硬接两个独立模型不同，也不能省掉接力通信成本。 例如手机先跑窄层再把状态交给服务器宽层；若从未训练这种交接，服务器接到的表示可能不在其熟悉的分布中。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-339f1d60618048c6">为何训练窄模型和宽模型之外，还要专门训练“窄转宽”路径？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aev-jepa">EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Reality Labs Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两种宽度各自表现好，不保证窄模型中间状态可直接交给宽模型。混合路径显式训练切分层的升宽接口，并以共同冻结教师约束表示，使跨设备接力有训练依据；这与随意裁剪通道或在运行时硬接两个独立模型不同，也不能省掉接力通信成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如手机先跑窄层再把状态交给服务器宽层；若从未训练这种交接，服务器接到的表示可能不在其熟悉的分布中。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14324">原论文</a> · <a href="../../../../reproductions/2610.14324-ev-jepa/">实现解读</a> · <a href="#qa-339f1d60618048c6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ev-jepa" data-paper-title="EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference 基础模型 Meta Reality Labs Research 2026-10-09 固定容量的视频模型难以同时适配端侧预算和跨设备协作，独立训练不同宽度也不保证中间表示兼容。EV-JEPA共享嵌套宽度参数，每步联合训练窄、宽与窄转宽三条路径，以冻结视频教师约束共同表示空间，并增加可调token压缩。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文§4.1：128 GPU、300epochs，Kinetics-710/SSv2/HowTo100M视频，冻结V-JEPA2 ViT-G教师；每步同时训练窄、宽、混合三路径。压缩器另需100epochs×300iterations、全局batch4096。不是本地测速，原预算显著超出单卡A100/A30或Mac；不下载全视频或尝试多臂训练。  jepa video-representation elastic-inference 多模态 视觉世界建模：状态、生成与动作条件 T3 的窄转宽路径与只同时训练窄、宽两条路径相比，多约束了什么？ 只训练两端可让各自完成任务，却未要求窄网络中间输出能接入宽网络后半段。混合路径在切分层通过可学习投影升宽，并接受同一教师监督，直接约束跨宽度衔接；这种路径兼容性不能靠裁剪参数或插零自动获得。 例如窄模型第三层状态经投影交给宽模型第四层，要有相应训练；两个完整模型各自分数高并不证明这样拼接有效。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a740fcbaa2cbbe9d">T3 的窄转宽路径与只同时训练窄、宽两条路径相比，多约束了什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aev-jepa">EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Reality Labs Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只训练两端可让各自完成任务，却未要求窄网络中间输出能接入宽网络后半段。混合路径在切分层通过可学习投影升宽，并接受同一教师监督，直接约束跨宽度衔接；这种路径兼容性不能靠裁剪参数或插零自动获得。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如窄模型第三层状态经投影交给宽模型第四层，要有相应训练；两个完整模型各自分数高并不证明这样拼接有效。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14324">原论文</a> · <a href="../../../../reproductions/2610.14324-ev-jepa/">实现解读</a> · <a href="#qa-a740fcbaa2cbbe9d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ev-jepa" data-paper-title="EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference 基础模型 Meta Reality Labs Research 2026-10-09 固定容量的视频模型难以同时适配端侧预算和跨设备协作，独立训练不同宽度也不保证中间表示兼容。EV-JEPA共享嵌套宽度参数，每步联合训练窄、宽与窄转宽三条路径，以冻结视频教师约束共同表示空间，并增加可调token压缩。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文§4.1：128 GPU、300epochs，Kinetics-710/SSv2/HowTo100M视频，冻结V-JEPA2 ViT-G教师；每步同时训练窄、宽、混合三路径。压缩器另需100epochs×300iterations、全局batch4096。不是本地测速，原预算显著超出单卡A100/A30或Mac；不下载全视频或尝试多臂训练。  jepa video-representation elastic-inference 多模态 视觉世界建模：状态、生成与动作条件 EV-JEPA 的教师是否跟随学生做 EMA，压缩器是否就是 token 裁剪？ 两者都不是。教师是冻结 V-JEPA2，T3 将窄、混合、宽三条 masked-token L1 相加；压缩器另在后训练阶段增加切分层重建目标。当前本地没有运行算法或 GPU 通过记录，不能将规格文档或普通裁剪标为完整弹性模型实现。 例如修改学生宽路径参数后，教师目标仍应不变；若教师随之指数更新，就改变了论文固定目标训练。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-5a736aec4cf8931e">EV-JEPA 的教师是否跟随学生做 EMA，压缩器是否就是 token 裁剪？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aev-jepa">EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Reality Labs Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两者都不是。教师是冻结 V-JEPA2，T3 将窄、混合、宽三条 masked-token L1 相加；压缩器另在后训练阶段增加切分层重建目标。当前本地没有运行算法或 GPU 通过记录，不能将规格文档或普通裁剪标为完整弹性模型实现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如修改学生宽路径参数后，教师目标仍应不变；若教师随之指数更新，就改变了论文固定目标训练。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、边界与后续触发条件；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14324">原论文</a> · <a href="../../../../reproductions/2610.14324-ev-jepa/">实现解读</a> · <a href="#qa-5a736aec4cf8931e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:smolwam" data-paper-title="SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices 基础模型 ML Collective 2026-10-09 Cosmos Policy 将机器人状态、两路相机、动作和未来状态编码为九个 latent frame，沿用视频生成接口：33 帧 VAE、T5-XXL、28-block 2B DiT、1764 tokens 和五步去噪。SmolWAM 并非只换一个轻量 action head，而是在保留预训练 trunk、token 原位置与 rectified-flow readout 的同时，逐项恢复接口改变造成的分布偏移。单帧 Wan VAE 配合 0.5M adapter，映射回原 clip latent 空间； 8 步仅是缩小训练机制诊断，不代表原68,830row/5000step效果。当前为 core_mechanism：真实 A100 已完成三 seed 缩放 teacher 蒸馏、两阶段布局课程与新 student LIBERO 闭环，不用 VQA/随机小网络替代。新 student 与 no-op 均无任务成功；原5000步蒸馏未重训，不能称 full_pipeline 或能力提升。本地对照口径：基线为同固定 LIBERO 初始状态实际执行的 no-op 策略，实验组为各 seed 新训练、validation-selected SmolWAM student；完整 teacher 保持率与相对提速不适用。  world-action-model robotics efficient-inference 多模态 视觉世界建模：状态、生成与动作条件 SmolWAM 为什么保留未来 latent 输出，而不只做轻量动作头？ 它希望压缩 Cosmos Policy 同时保留世界预测接口，单次 trunk 前向同时输出动作 chunk 与两路未来 latent。若只保留动作头，就失去论文的重要训练和读出对象；紧凑设计还要恢复 VAE、文本和布局改变造成的分布偏移，不能只删层后直接宣称等价。 例如机器人输出接下来十六步动作时，也预测执行后的相机 latent，用同一骨干承接动作与视觉未来，而非单独回归关节。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-smolwam-cc2de315" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0aa7cf4f31b523e5">SmolWAM 为什么保留未来 latent 输出，而不只做轻量动作头？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asmolwam">SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ML Collective</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它希望压缩 Cosmos Policy 同时保留世界预测接口，单次 trunk 前向同时输出动作 chunk 与两路未来 latent。若只保留动作头，就失去论文的重要训练和读出对象；紧凑设计还要恢复 VAE、文本和布局改变造成的分布偏移，不能只删层后直接宣称等价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如机器人输出接下来十六步动作时，也预测执行后的相机 latent，用同一骨干承接动作与视觉未来，而非单独回归关节。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13740">原论文</a> · <a href="../../../../reproductions/2610.13740-smolwam/">实现解读</a> · <a href="#qa-0aa7cf4f31b523e5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:smolwam" data-paper-title="SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices 基础模型 ML Collective 2026-10-09 Cosmos Policy 将机器人状态、两路相机、动作和未来状态编码为九个 latent frame，沿用视频生成接口：33 帧 VAE、T5-XXL、28-block 2B DiT、1764 tokens 和五步去噪。SmolWAM 并非只换一个轻量 action head，而是在保留预训练 trunk、token 原位置与 rectified-flow readout 的同时，逐项恢复接口改变造成的分布偏移。单帧 Wan VAE 配合 0.5M adapter，映射回原 clip latent 空间； 8 步仅是缩小训练机制诊断，不代表原68,830row/5000step效果。当前为 core_mechanism：真实 A100 已完成三 seed 缩放 teacher 蒸馏、两阶段布局课程与新 student LIBERO 闭环，不用 VQA/随机小网络替代。新 student 与 no-op 均无任务成功；原5000步蒸馏未重训，不能称 full_pipeline 或能力提升。本地对照口径：基线为同固定 LIBERO 初始状态实际执行的 no-op 策略，实验组为各 seed 新训练、validation-selected SmolWAM student；完整 teacher 保持率与相对提速不适用。  world-action-model robotics efficient-inference 多模态 视觉世界建模：状态、生成与动作条件 为什么缩小动作查询接口时，还要保留原 token 位置与 rectified-flow 方向？ 预训练 trunk 已适应特定位置语义和从数据到噪声的速度定义，换轻量接口若同时改掉这些约定，会产生额外分布偏移。SmolWAM 逐项恢复适配而非只缩小动作头；载入权重成功也不能证明错误的噪声方向或位置设置下仍等价运行。 例如教师学的是噪声减数据的速度，若学生默认反向定义却仍套用原读出公式，动作恢复就可能朝错误方向变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-6d581a20417b2084">为什么缩小动作查询接口时，还要保留原 token 位置与 rectified-flow 方向？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asmolwam">SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ML Collective</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>预训练 trunk 已适应特定位置语义和从数据到噪声的速度定义，换轻量接口若同时改掉这些约定，会产生额外分布偏移。SmolWAM 逐项恢复适配而非只缩小动作头；载入权重成功也不能证明错误的噪声方向或位置设置下仍等价运行。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如教师学的是噪声减数据的速度，若学生默认反向定义却仍套用原读出公式，动作恢复就可能朝错误方向变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13740">原论文</a> · <a href="../../../../reproductions/2610.13740-smolwam/">实现解读</a> · <a href="#qa-6d581a20417b2084">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:smolwam" data-paper-title="SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices 基础模型 ML Collective 2026-10-09 Cosmos Policy 将机器人状态、两路相机、动作和未来状态编码为九个 latent frame，沿用视频生成接口：33 帧 VAE、T5-XXL、28-block 2B DiT、1764 tokens 和五步去噪。SmolWAM 并非只换一个轻量 action head，而是在保留预训练 trunk、token 原位置与 rectified-flow readout 的同时，逐项恢复接口改变造成的分布偏移。单帧 Wan VAE 配合 0.5M adapter，映射回原 clip latent 空间； 8 步仅是缩小训练机制诊断，不代表原68,830row/5000step效果。当前为 core_mechanism：真实 A100 已完成三 seed 缩放 teacher 蒸馏、两阶段布局课程与新 student LIBERO 闭环，不用 VQA/随机小网络替代。新 student 与 no-op 均无任务成功；原5000步蒸馏未重训，不能称 full_pipeline 或能力提升。本地对照口径：基线为同固定 LIBERO 初始状态实际执行的 no-op 策略，实验组为各 seed 新训练、validation-selected SmolWAM student；完整 teacher 保持率与相对提速不适用。  world-action-model robotics efficient-inference 多模态 视觉世界建模：状态、生成与动作条件 单帧 VAE 加 adapter 与直接换成单帧 VAE 有何不同？ 原 teacher 以视频 clip latent 接口训练，单帧编码的分布可能不同；adapter 将单帧结果映回原 clip latent 空间，以保留预训练 trunk 可用的输入结构。直接更换编码器省略这个恢复步骤，不能假定 token 位置相同就代表数值分布一致。 例如两个编码器都输出相同形状，数值尺度和时空语义仍可能不同；adapter 学的是让新单帧输入适应旧骨干。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-9f6b8f26a0b0653d">单帧 VAE 加 adapter 与直接换成单帧 VAE 有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asmolwam">SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ML Collective</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原 teacher 以视频 clip latent 接口训练，单帧编码的分布可能不同；adapter 将单帧结果映回原 clip latent 空间，以保留预训练 trunk 可用的输入结构。直接更换编码器省略这个恢复步骤，不能假定 token 位置相同就代表数值分布一致。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个编码器都输出相同形状，数值尺度和时空语义仍可能不同；adapter 学的是让新单帧输入适应旧骨干。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13740">原论文</a> · <a href="../../../../reproductions/2610.13740-smolwam/">实现解读</a> · <a href="#qa-9f6b8f26a0b0653d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:smolwam" data-paper-title="SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices 基础模型 ML Collective 2026-10-09 Cosmos Policy 将机器人状态、两路相机、动作和未来状态编码为九个 latent frame，沿用视频生成接口：33 帧 VAE、T5-XXL、28-block 2B DiT、1764 tokens 和五步去噪。SmolWAM 并非只换一个轻量 action head，而是在保留预训练 trunk、token 原位置与 rectified-flow readout 的同时，逐项恢复接口改变造成的分布偏移。单帧 Wan VAE 配合 0.5M adapter，映射回原 clip latent 空间； 8 步仅是缩小训练机制诊断，不代表原68,830row/5000step效果。当前为 core_mechanism：真实 A100 已完成三 seed 缩放 teacher 蒸馏、两阶段布局课程与新 student LIBERO 闭环，不用 VQA/随机小网络替代。新 student 与 no-op 均无任务成功；原5000步蒸馏未重训，不能称 full_pipeline 或能力提升。本地对照口径：基线为同固定 LIBERO 初始状态实际执行的 no-op 策略，实验组为各 seed 新训练、validation-selected SmolWAM student；完整 teacher 保持率与相对提速不适用。  world-action-model robotics efficient-inference 多模态 视觉世界建模：状态、生成与动作条件 这里的 rectified-flow 速度方向与 LeWAM 相同吗？ 不同。SmolWAM 沿 teacher 的数据到噪声方向，插值 xτ=(1-τ)x0+τε，速度为 ε-x0，干净估计应与此符号一致；LeWAM 使用相反方向。还需保留十二个指定 block、原位置及零偏置 sink，不能只照抄另一篇 flow 公式。 例如从噪声端反推干净动作时若把速度符号颠倒，会朝错误方向更新；损失数值可运行并不说明读取方向正确。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b896fba15c6b0841">这里的 rectified-flow 速度方向与 LeWAM 相同吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asmolwam">SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ML Collective</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同。SmolWAM 沿 teacher 的数据到噪声方向，插值 xτ=(1-τ)x0+τε，速度为 ε-x0，干净估计应与此符号一致；LeWAM 使用相反方向。还需保留十二个指定 block、原位置及零偏置 sink，不能只照抄另一篇 flow 公式。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如从噪声端反推干净动作时若把速度符号颠倒，会朝错误方向更新；损失数值可运行并不说明读取方向正确。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、数据协议、结果与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13740">原论文</a> · <a href="../../../../reproductions/2610.13740-smolwam/">实现解读</a> · <a href="#qa-b896fba15c6b0841">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:lewam" data-paper-title="LeWAM: End-to-End World and Action Modeling with JEPAs" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="LeWAM: End-to-End World and Action Modeling with JEPAs 基础模型 UC San Diego 2026-10-08 传统 JEPA 学习“给定动作会到什么状态”，之后另训逆动力学或在线搜索动作。两阶段会使控制监督无法塑造视觉表征，宽高斯动作搜索也较昂贵。LeWAM 在同一训练阶段更新视觉编码器、潜在动力学和随机策略：既预测动作导致的未来 latent，又通过 flow matching 学习如何行动。视觉编码器由从零训练的 ResNet-18、空间 softmax 和两层投影 MLP 组成。模拟版本约 16.9M 参数，latent/MoT 宽度 192，4 层、4 头。 当前为 core_mechanism：真实 A100 已完成三 seed 缩放联合训练→新候选三臂闭环，证据绑定实际源码与权重哈希。目标来自训练轨迹，仍是非 holdout 诊断；未观测到规划相对 reactive 的优势，不宣称完整论文效果复现。本地对照口径：本轮真实测量用各 seed 的新训练、validation-selected checkpoint；基线为同一候选的 reactive policy，实验组为 best-of-K 与梯度规划。原目标来自训练轨迹，稳定能力相对提升不适用。发布模型入口仍保留，但未将其成绩冒充新候选成绩。  world-action-model jepa latent-planning 多模态 视觉世界建模：状态、生成与动作条件 LeWAM 为什么让视觉编码器同时接受世界预测与动作监督？ 两阶段路线先学给定动作的未来表示，再另学控制，动作目标难以反向塑造前期视觉表示。LeWAM 联合更新视觉编码器、潜在动力学和随机策略，使表示同时服务未来预测与行动；联合目标也需要防塌缩约束，不能只训练动作头便称端到端联合。 例如视觉表示若忽略可抓取边缘，动作损失可以在联合训练中推动编码器保留它，而冻结两阶段编码器做不到同样更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-lewam-7895d3a3" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-1a6959f95b4f9227">LeWAM 为什么让视觉编码器同时接受世界预测与动作监督？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alewam">LeWAM: End-to-End World and Action Modeling with JEPAs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两阶段路线先学给定动作的未来表示，再另学控制，动作目标难以反向塑造前期视觉表示。LeWAM 联合更新视觉编码器、潜在动力学和随机策略，使表示同时服务未来预测与行动；联合目标也需要防塌缩约束，不能只训练动作头便称端到端联合。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如视觉表示若忽略可抓取边缘，动作损失可以在联合训练中推动编码器保留它，而冻结两阶段编码器做不到同样更新。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12818">原论文</a> · <a href="../../../../reproductions/2610.12818-lewam/">实现解读</a> · <a href="#qa-1a6959f95b4f9227">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:lewam" data-paper-title="LeWAM: End-to-End World and Action Modeling with JEPAs" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="LeWAM: End-to-End World and Action Modeling with JEPAs 基础模型 UC San Diego 2026-10-08 传统 JEPA 学习“给定动作会到什么状态”，之后另训逆动力学或在线搜索动作。两阶段会使控制监督无法塑造视觉表征，宽高斯动作搜索也较昂贵。LeWAM 在同一训练阶段更新视觉编码器、潜在动力学和随机策略：既预测动作导致的未来 latent，又通过 flow matching 学习如何行动。视觉编码器由从零训练的 ResNet-18、空间 softmax 和两层投影 MLP 组成。模拟版本约 16.9M 参数，latent/MoT 宽度 192，4 层、4 头。 当前为 core_mechanism：真实 A100 已完成三 seed 缩放联合训练→新候选三臂闭环，证据绑定实际源码与权重哈希。目标来自训练轨迹，仍是非 holdout 诊断；未观测到规划相对 reactive 的优势，不宣称完整论文效果复现。本地对照口径：本轮真实测量用各 seed 的新训练、validation-selected checkpoint；基线为同一候选的 reactive policy，实验组为 best-of-K 与梯度规划。原目标来自训练轨迹，稳定能力相对提升不适用。发布模型入口仍保留，但未将其成绩冒充新候选成绩。  world-action-model jepa latent-planning 多模态 视觉世界建模：状态、生成与动作条件 为什么 LeWAM 的噪声动作分支不能经中间层读取干净动作？ 干净动作作为未来动力学监督，在训练中可供状态查询使用，却不是部署时策略已知的信息。如果噪声动作通过共享注意力偷读它，就可能复制目标而不学从观察和目标生成动作。分支独立参数不够，必须同时约束跨层可见性以堵住间接泄漏。 例如训练给出真实“向左推”的动作供预测未来；生成动作的噪声分支不能先看见这个答案，再把恢复结果算成决策能力。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-64e4dca51fbd2f0a">为什么 LeWAM 的噪声动作分支不能经中间层读取干净动作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alewam">LeWAM: End-to-End World and Action Modeling with JEPAs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>干净动作作为未来动力学监督，在训练中可供状态查询使用，却不是部署时策略已知的信息。如果噪声动作通过共享注意力偷读它，就可能复制目标而不学从观察和目标生成动作。分支独立参数不够，必须同时约束跨层可见性以堵住间接泄漏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如训练给出真实“向左推”的动作供预测未来；生成动作的噪声分支不能先看见这个答案，再把恢复结果算成决策能力。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12818">原论文</a> · <a href="../../../../reproductions/2610.12818-lewam/">实现解读</a> · <a href="#qa-64e4dca51fbd2f0a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:lewam" data-paper-title="LeWAM: End-to-End World and Action Modeling with JEPAs" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="LeWAM: End-to-End World and Action Modeling with JEPAs 基础模型 UC San Diego 2026-10-08 传统 JEPA 学习“给定动作会到什么状态”，之后另训逆动力学或在线搜索动作。两阶段会使控制监督无法塑造视觉表征，宽高斯动作搜索也较昂贵。LeWAM 在同一训练阶段更新视觉编码器、潜在动力学和随机策略：既预测动作导致的未来 latent，又通过 flow matching 学习如何行动。视觉编码器由从零训练的 ResNet-18、空间 softmax 和两层投影 MLP 组成。模拟版本约 16.9M 参数，latent/MoT 宽度 192，4 层、4 头。 当前为 core_mechanism：真实 A100 已完成三 seed 缩放联合训练→新候选三臂闭环，证据绑定实际源码与权重哈希。目标来自训练轨迹，仍是非 holdout 诊断；未观测到规划相对 reactive 的优势，不宣称完整论文效果复现。本地对照口径：本轮真实测量用各 seed 的新训练、validation-selected checkpoint；基线为同一候选的 reactive policy，实验组为 best-of-K 与梯度规划。原目标来自训练轨迹，稳定能力相对提升不适用。发布模型入口仍保留，但未将其成绩冒充新候选成绩。  world-action-model jepa latent-planning 多模态 视觉世界建模：状态、生成与动作条件 LeWAM 的动作 flow 策略与宽高斯随机搜索的区别是什么？ flow matching 学习从噪声到动作数据的速度场，提供更接近训练动作分布的候选，再在潜在动力学中规划。宽高斯搜索主要靠无结构采样覆盖动作；学得的候选可能更集中，但真实优势仍需独立控制任务验证，不能靠训练损失推断。 例如推物体时，学得策略可优先给出贴近桌面的推法，而不是大量采样穿过桌面的无效动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7d7c630753bca65d">LeWAM 的动作 flow 策略与宽高斯随机搜索的区别是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alewam">LeWAM: End-to-End World and Action Modeling with JEPAs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>flow matching 学习从噪声到动作数据的速度场，提供更接近训练动作分布的候选，再在潜在动力学中规划。宽高斯搜索主要靠无结构采样覆盖动作；学得的候选可能更集中，但真实优势仍需独立控制任务验证，不能靠训练损失推断。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如推物体时，学得策略可优先给出贴近桌面的推法，而不是大量采样穿过桌面的无效动作。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12818">原论文</a> · <a href="../../../../reproductions/2610.12818-lewam/">实现解读</a> · <a href="#qa-7d7c630753bca65d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:lewam" data-paper-title="LeWAM: End-to-End World and Action Modeling with JEPAs" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="LeWAM: End-to-End World and Action Modeling with JEPAs 基础模型 UC San Diego 2026-10-08 传统 JEPA 学习“给定动作会到什么状态”，之后另训逆动力学或在线搜索动作。两阶段会使控制监督无法塑造视觉表征，宽高斯动作搜索也较昂贵。LeWAM 在同一训练阶段更新视觉编码器、潜在动力学和随机策略：既预测动作导致的未来 latent，又通过 flow matching 学习如何行动。视觉编码器由从零训练的 ResNet-18、空间 softmax 和两层投影 MLP 组成。模拟版本约 16.9M 参数，latent/MoT 宽度 192，4 层、4 头。 当前为 core_mechanism：真实 A100 已完成三 seed 缩放联合训练→新候选三臂闭环，证据绑定实际源码与权重哈希。目标来自训练轨迹，仍是非 holdout 诊断；未观测到规划相对 reactive 的优势，不宣称完整论文效果复现。本地对照口径：本轮真实测量用各 seed 的新训练、validation-selected checkpoint；基线为同一候选的 reactive policy，实验组为 best-of-K 与梯度规划。原目标来自训练轨迹，稳定能力相对提升不适用。发布模型入口仍保留，但未将其成绩冒充新候选成绩。  world-action-model jepa latent-planning 多模态 视觉世界建模：状态、生成与动作条件 噪声动作能通过状态 query 间接读取干净动作吗？ 不能。历史只读历史，状态 query 可读干净动作，但噪声动作不能读干净动作或携带其信息的 query。动作插值从噪声到数据，速度为 A-ε；视觉编码器在线联合训练而非 EMA，SIGReg 也不是只匹配均值方差的替代项。 例如第一层 query 看见正确动作后，第二层若噪声动作再读 query，就发生间接答案泄露，即使直接边已遮住。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c23e22f887512a09">噪声动作能通过状态 query 间接读取干净动作吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alewam">LeWAM: End-to-End World and Action Modeling with JEPAs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。历史只读历史，状态 query 可读干净动作，但噪声动作不能读干净动作或携带其信息的 query。动作插值从噪声到数据，速度为 A-ε；视觉编码器在线联合训练而非 EMA，SIGReg 也不是只匹配均值方差的替代项。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如第一层 query 看见正确动作后，第二层若噪声动作再读 query，就发生间接答案泄露，即使直接边已遮住。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、数据协议、结果与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12818">原论文</a> · <a href="../../../../reproductions/2610.12818-lewam/">实现解读</a> · <a href="#qa-c23e22f887512a09">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:raw-video-midtraining" data-paper-title="Mid-Training Language Models on Raw Video" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Mid-Training Language Models on Raw Video 多模态大模型 Meta AI / Massachusetts Institute of Technology 2026-10-08 将有序帧的patch编码为连续视觉token并按空间顺序序列化；因果LM预测下一视觉token，目标侧stop-gradient。中期训练没有字幕或文本损失；随后与对照使用相同图文指令调优，隔离视频阶段贡献。原文§3–4 成本过高，不复现（审查 DONE）；Google/Meta优先补漏。成本过高，不复现（审查 DONE）；不以MSE演示冒充视频中期训练。原文§4.1.4使用128张H100训练27300步，batch256、16K上下文，之后还有指令调优。原始资源配置  视频理解与世界模型 无字幕视频中期训练 多模态 视觉世界建模：状态、生成与动作条件 无字幕的视频中期训练，语言模型究竟预测什么？ 有序视频帧经视觉 tokenizer 转成连续 patch token，并按空间顺序序列化；因果语言模型和预测头回归下一个连续视觉 token。这个阶段没有字幕或文本损失，目标是从视觉序列学习结构，而不是将视频先自动写成描述再做文本续写。 例如当前输入某帧左上到右下的视觉 token，模型预测后继视觉向量，而不是输出“有人开门”这段字幕。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-multimodal-models-raw-video-midtraining-db4472b0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-176304cc6cc0aa4d">无字幕的视频中期训练，语言模型究竟预测什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Araw-video-midtraining">Mid-Training Language Models on Raw Video</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI / Massachusetts Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>有序视频帧经视觉 tokenizer 转成连续 patch token，并按空间顺序序列化；因果语言模型和预测头回归下一个连续视觉 token。这个阶段没有字幕或文本损失，目标是从视觉序列学习结构，而不是将视频先自动写成描述再做文本续写。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如当前输入某帧左上到右下的视觉 token，模型预测后继视觉向量，而不是输出“有人开门”这段字幕。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与原文效果；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11019">原论文</a> · <a href="../../../../multimodal-models/2610.11019-raw-video-midtraining/">实现解读</a> · <a href="#qa-176304cc6cc0aa4d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:raw-video-midtraining" data-paper-title="Mid-Training Language Models on Raw Video" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Mid-Training Language Models on Raw Video 多模态大模型 Meta AI / Massachusetts Institute of Technology 2026-10-08 将有序帧的patch编码为连续视觉token并按空间顺序序列化；因果LM预测下一视觉token，目标侧stop-gradient。中期训练没有字幕或文本损失；随后与对照使用相同图文指令调优，隔离视频阶段贡献。原文§3–4 成本过高，不复现（审查 DONE）；Google/Meta优先补漏。成本过高，不复现（审查 DONE）；不以MSE演示冒充视频中期训练。原文§4.1.4使用128张H100训练27300步，batch256、16K上下文，之后还有指令调优。原始资源配置  视频理解与世界模型 无字幕视频中期训练 多模态 视觉世界建模：状态、生成与动作条件 目标侧 stop-gradient 为什么不意味着视觉 tokenizer 完全冻结？ 目标路径停止梯度是防止预测目标跟随预测一起塌缩或移动，输入侧视觉 tokenizer 仍可通过 LM 与预测头接收梯度。模型在无字幕中期训练中学习视觉序列关系，之后需匹配的指令调优对照；不能把没有文字损失误解为整个视觉前端不训练。 例如用前一帧 patch 预测下一 patch，下一目标不反传，但前一输入经过的视觉参数仍可被预测误差更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-cca299426ddfa506">目标侧 stop-gradient 为什么不意味着视觉 tokenizer 完全冻结？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Araw-video-midtraining">Mid-Training Language Models on Raw Video</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI / Massachusetts Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标路径停止梯度是防止预测目标跟随预测一起塌缩或移动，输入侧视觉 tokenizer 仍可通过 LM 与预测头接收梯度。模型在无字幕中期训练中学习视觉序列关系，之后需匹配的指令调优对照；不能把没有文字损失误解为整个视觉前端不训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用前一帧 patch 预测下一 patch，下一目标不反传，但前一输入经过的视觉参数仍可被预测误差更新。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与原文效果；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11019">原论文</a> · <a href="../../../../multimodal-models/2610.11019-raw-video-midtraining/">实现解读</a> · <a href="#qa-cca299426ddfa506">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:raw-video-midtraining" data-paper-title="Mid-Training Language Models on Raw Video" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Mid-Training Language Models on Raw Video 多模态大模型 Meta AI / Massachusetts Institute of Technology 2026-10-08 将有序帧的patch编码为连续视觉token并按空间顺序序列化；因果LM预测下一视觉token，目标侧stop-gradient。中期训练没有字幕或文本损失；随后与对照使用相同图文指令调优，隔离视频阶段贡献。原文§3–4 成本过高，不复现（审查 DONE）；Google/Meta优先补漏。成本过高，不复现（审查 DONE）；不以MSE演示冒充视频中期训练。原文§4.1.4使用128张H100训练27300步，batch256、16K上下文，之后还有指令调优。原始资源配置  视频理解与世界模型 无字幕视频中期训练 多模态 视觉世界建模：状态、生成与动作条件 与视频 caption 训练相比，raw video 路线避免了什么监督瓶颈？ caption 只保留文字描述覆盖的视觉内容，可能省略连续运动和细节；连续 token 预测直接利用原始视频顺序。它也引入更长序列与视觉回归训练成本，不能因为没有字幕就推断语义必然更好，后续还需匹配的图文指令调优比较。 例如字幕只写“球移动”，原始连续表示仍含路径与速度变化；但模型能否利用这些信息需要实际下游评测。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1aa77b19c09a3bc6">与视频 caption 训练相比，raw video 路线避免了什么监督瓶颈？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Araw-video-midtraining">Mid-Training Language Models on Raw Video</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI / Massachusetts Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>caption 只保留文字描述覆盖的视觉内容，可能省略连续运动和细节；连续 token 预测直接利用原始视频顺序。它也引入更长序列与视觉回归训练成本，不能因为没有字幕就推断语义必然更好，后续还需匹配的图文指令调优比较。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如字幕只写“球移动”，原始连续表示仍含路径与速度变化；但模型能否利用这些信息需要实际下游评测。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与原文效果；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11019">原论文</a> · <a href="../../../../multimodal-models/2610.11019-raw-video-midtraining/">实现解读</a> · <a href="#qa-1aa77b19c09a3bc6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:raw-video-midtraining" data-paper-title="Mid-Training Language Models on Raw Video" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Mid-Training Language Models on Raw Video 多模态大模型 Meta AI / Massachusetts Institute of Technology 2026-10-08 将有序帧的patch编码为连续视觉token并按空间顺序序列化；因果LM预测下一视觉token，目标侧stop-gradient。中期训练没有字幕或文本损失；随后与对照使用相同图文指令调优，隔离视频阶段贡献。原文§3–4 成本过高，不复现（审查 DONE）；Google/Meta优先补漏。成本过高，不复现（审查 DONE）；不以MSE演示冒充视频中期训练。原文§4.1.4使用128张H100训练27300步，batch256、16K上下文，之后还有指令调优。原始资源配置  视频理解与世界模型 无字幕视频中期训练 多模态 视觉世界建模：状态、生成与动作条件 目标 token stop-gradient 是否意味着视觉 tokenizer 冻结？ 不意味着。目标侧停止梯度避免预测目标被直接拉动，但同一 tokenizer 的输入路径仍接收预测损失，和语言模型、预测头一起端到端更新。当前本地没有运行该大规模训练；不能把 detach 目标的小张量测试称为视频中期训练已完成。 例如 v_(i+1) 作为标签不反传，但 v_1 到 v_i 作为上下文仍可把梯度传回视觉 tokenizer；两条路径要区分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-9a155f198062cb83">目标 token stop-gradient 是否意味着视觉 tokenizer 冻结？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Araw-video-midtraining">Mid-Training Language Models on Raw Video</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI / Massachusetts Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不意味着。目标侧停止梯度避免预测目标被直接拉动，但同一 tokenizer 的输入路径仍接收预测损失，和语言模型、预测头一起端到端更新。当前本地没有运行该大规模训练；不能把 detach 目标的小张量测试称为视频中期训练已完成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 v_(i+1) 作为标签不反传，但 v_1 到 v_i 作为上下文仍可把梯度传回视觉 tokenizer；两条路径要区分。</p>
<p class="ar-learning-sources">依据：核心公式与原文效果、本地复现与成本决策；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11019">原论文</a> · <a href="../../../../multimodal-models/2610.11019-raw-video-midtraining/">实现解读</a> · <a href="#qa-9a155f198062cb83">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:woven" data-paper-title="WOVEN: Weaving Visual World Modeling into Multimodal LLMs" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="WOVEN: Weaving Visual World Modeling into Multimodal LLMs 多模态大模型 Northwestern University 2026-10-08 静态识别不等于理解状态变化。WOVEN以为共同对象，用视频生成模型rollout提供结果/中间状态，而非在prompt里预写结果。相同初始状态在不同动作下的rollout提供counterfactual候选；按scene、action、reasoning三个轴形成可控监督，用error-typed distractors区分错误机制。该paper的核心是真实视觉转移监督进入MLLM训练，不是训练图片class scorer。 相对原论文benchmark不适用，source_id分组小样本accuracy只用于L1诊断。本地对照口径：同一冻结公共VLM零LoRA残差为基线，真实transition response SFT为实验组；相对原论文benchmark不适用，source_id分组小样本accuracy只用于L1诊断。  multimodal-foundation-model visual-transition-reasoning world-model-supervision 多模态 视觉世界建模：状态、生成与动作条件 WOVEN 的状态转移监督为什么不是普通静态图片分类？ 共同对象是初始状态、动作与结果状态的关系，可要求前向预测、反推动作或反事实结果。视频生成 rollout 提供实际视觉转移及中间帧，而非在 prompt 里直接写结果；仅辨认物体类别无法覆盖这些操作，也不能替代模型对转移关系的学习。 例如同一初始球位，左推与右推得到不同结果，问题可要求选动作或选后果，不是只回答画面里有没有球。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-multimodal-models-woven-63239e78" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7a31f3fc9074b0c6">WOVEN 的状态转移监督为什么不是普通静态图片分类？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Awoven">WOVEN: Weaving Visual World Modeling into Multimodal LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Northwestern University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共同对象是初始状态、动作与结果状态的关系，可要求前向预测、反推动作或反事实结果。视频生成 rollout 提供实际视觉转移及中间帧，而非在 prompt 里直接写结果；仅辨认物体类别无法覆盖这些操作，也不能替代模型对转移关系的学习。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一初始球位，左推与右推得到不同结果，问题可要求选动作或选后果，不是只回答画面里有没有球。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12417">原论文</a> · <a href="../../../../reproductions/2610.12417-woven/">实现解读</a> · <a href="#qa-7a31f3fc9074b0c6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:woven" data-paper-title="WOVEN: Weaving Visual World Modeling into Multimodal LLMs" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="WOVEN: Weaving Visual World Modeling into Multimodal LLMs 多模态大模型 Northwestern University 2026-10-08 静态识别不等于理解状态变化。WOVEN以为共同对象，用视频生成模型rollout提供结果/中间状态，而非在prompt里预写结果。相同初始状态在不同动作下的rollout提供counterfactual候选；按scene、action、reasoning三个轴形成可控监督，用error-typed distractors区分错误机制。该paper的核心是真实视觉转移监督进入MLLM训练，不是训练图片class scorer。 相对原论文benchmark不适用，source_id分组小样本accuracy只用于L1诊断。本地对照口径：同一冻结公共VLM零LoRA残差为基线，真实transition response SFT为实验组；相对原论文benchmark不适用，source_id分组小样本accuracy只用于L1诊断。  multimodal-foundation-model visual-transition-reasoning world-model-supervision 多模态 视觉世界建模：状态、生成与动作条件 为什么要按初始场景或 source 分组切分，而不能随机拆散视觉转移问答？ 同一初始图像可以衍生多个动作、问题与反事实选项，随机按题切分可能把几乎相同的视觉状态放进训练和测试。分组隔离减少这种捷径，再区分场景、动作与推理操作的迁移；高同源问答分数不能自动说明理解了未知场景的状态变化。 例如同一桌面分别问“向左推会怎样”和“什么动作导致杯子移动”，两题共享底图，应作为一组切分而非分居训练测试。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-507c29cd3a03e147">为什么要按初始场景或 source 分组切分，而不能随机拆散视觉转移问答？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Awoven">WOVEN: Weaving Visual World Modeling into Multimodal LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Northwestern University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一初始图像可以衍生多个动作、问题与反事实选项，随机按题切分可能把几乎相同的视觉状态放进训练和测试。分组隔离减少这种捷径，再区分场景、动作与推理操作的迁移；高同源问答分数不能自动说明理解了未知场景的状态变化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一桌面分别问“向左推会怎样”和“什么动作导致杯子移动”，两题共享底图，应作为一组切分而非分居训练测试。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12417">原论文</a> · <a href="../../../../reproductions/2610.12417-woven/">实现解读</a> · <a href="#qa-507c29cd3a03e147">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:woven" data-paper-title="WOVEN: Weaving Visual World Modeling into Multimodal LLMs" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="WOVEN: Weaving Visual World Modeling into Multimodal LLMs 多模态大模型 Northwestern University 2026-10-08 静态识别不等于理解状态变化。WOVEN以为共同对象，用视频生成模型rollout提供结果/中间状态，而非在prompt里预写结果。相同初始状态在不同动作下的rollout提供counterfactual候选；按scene、action、reasoning三个轴形成可控监督，用error-typed distractors区分错误机制。该paper的核心是真实视觉转移监督进入MLLM训练，不是训练图片class scorer。 相对原论文benchmark不适用，source_id分组小样本accuracy只用于L1诊断。本地对照口径：同一冻结公共VLM零LoRA残差为基线，真实transition response SFT为实验组；相对原论文benchmark不适用，source_id分组小样本accuracy只用于L1诊断。  multimodal-foundation-model visual-transition-reasoning world-model-supervision 多模态 视觉世界建模：状态、生成与动作条件 scene-OOD 与 state-perturbation 测试区分什么泛化问题？ scene-OOD 改变场景分布，state-perturbation 检查状态变化下的鲁棒性，两者不能因 ID 准确率高就视为解决。原文受控轴还含 action 与 reasoning，不同监督操作对迁移的贡献需分别比较，不能把按不同 benchmark 选 subset 的覆盖当成单模型全面提升。 例如模型在新餐厅场景表现好，仍可能对同一场景里物体位置的小变化敏感；两种测试关注不同失效模式。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-9f43b6abf0908831">scene-OOD 与 state-perturbation 测试区分什么泛化问题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Awoven">WOVEN: Weaving Visual World Modeling into Multimodal LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Northwestern University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>scene-OOD 改变场景分布，state-perturbation 检查状态变化下的鲁棒性，两者不能因 ID 准确率高就视为解决。原文受控轴还含 action 与 reasoning，不同监督操作对迁移的贡献需分别比较，不能把按不同 benchmark 选 subset 的覆盖当成单模型全面提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型在新餐厅场景表现好，仍可能对同一场景里物体位置的小变化敏感；两种测试关注不同失效模式。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12417">原论文</a> · <a href="../../../../reproductions/2610.12417-woven/">实现解读</a> · <a href="#qa-9f43b6abf0908831">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:woven" data-paper-title="WOVEN: Weaving Visual World Modeling into Multimodal LLMs" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="WOVEN: Weaving Visual World Modeling into Multimodal LLMs 多模态大模型 Northwestern University 2026-10-08 静态识别不等于理解状态变化。WOVEN以为共同对象，用视频生成模型rollout提供结果/中间状态，而非在prompt里预写结果。相同初始状态在不同动作下的rollout提供counterfactual候选；按scene、action、reasoning三个轴形成可控监督，用error-typed distractors区分错误机制。该paper的核心是真实视觉转移监督进入MLLM训练，不是训练图片class scorer。 相对原论文benchmark不适用，source_id分组小样本accuracy只用于L1诊断。本地对照口径：同一冻结公共VLM零LoRA残差为基线，真实transition response SFT为实验组；相对原论文benchmark不适用，source_id分组小样本accuracy只用于L1诊断。  multimodal-foundation-model visual-transition-reasoning world-model-supervision 多模态 视觉世界建模：状态、生成与动作条件 四种 option permutation 与 source_id 分组分别防什么问题？ 排列选项时要同步搬迁目标字母而保持内容和图像对应，避免固定字母捷径；划分按初始来源分组，防同源状态的不同问法跨集合泄露。prompt 只投影问题、选项和真实图像，distractor_type 等答案相关字段不能进入模型，本地也只运行 SFT 未运行 GRPO。 例如同一初始帧生成三道题，应一起划到训练或留出；否则模型可记住来源，再在所谓 test 回答变体问题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-def30335d1ff6136">四种 option permutation 与 source_id 分组分别防什么问题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Awoven">WOVEN: Weaving Visual World Modeling into Multimodal LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Northwestern University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>排列选项时要同步搬迁目标字母而保持内容和图像对应，避免固定字母捷径；划分按初始来源分组，防同源状态的不同问法跨集合泄露。prompt 只投影问题、选项和真实图像，distractor_type 等答案相关字段不能进入模型，本地也只运行 SFT 未运行 GRPO。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一初始帧生成三道题，应一起划到训练或留出；否则模型可记住来源，再在所谓 test 回答变体问题。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、代码映射与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12417">原论文</a> · <a href="../../../../reproductions/2610.12417-woven/">实现解读</a> · <a href="#qa-def30335d1ff6136">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:vjepa-policy" data-paper-title="V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents 基础模型 Tsinghua University 2026-09-29 冻结 V-JEPA 2.1 视觉编码器，在预测视觉潜空间中联合训练 instruction-conditioned future-latent predictor 和 flow-matching action expert；动作生成读取 predictor 的未来信息上下文。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 future-latent stop-gradient 与 action flow matching；未加载 V-JEPA 2.1 或机器人数据。执行 future-latent stop-gradient 与 action flow matching；未加载 V-JEPA 2.1 或机器人数据。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  世界动作模型 预测视觉潜变量 机器人 多模态 视觉世界建模：状态、生成与动作条件 future-latent predictor 为什么要接收文字指令？ 同一当前视觉状态在不同指令下应通向不同未来，指令条件让预测未来与任务目标联系起来。动作专家读取这个预测上下文来生成控制；训练真实未来提供目标，部署使用预测未来，不能将目标 latent 直接当作可观察状态。 例如同一桌面上“推红块”和“推蓝块”需要不同未来布局，指令条件应改变预测并进一步影响动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-vjepa-policy-d720eedd" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5edd75f877906c0b">future-latent predictor 为什么要接收文字指令？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Avjepa-policy">V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一当前视觉状态在不同指令下应通向不同未来，指令条件让预测未来与任务目标联系起来。动作专家读取这个预测上下文来生成控制；训练真实未来提供目标，部署使用预测未来，不能将目标 latent 直接当作可观察状态。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一桌面上“推红块”和“推蓝块”需要不同未来布局，指令条件应改变预测并进一步影响动作。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37250">原论文</a> · <a href="../../../../foundation-models/2609.37250-vjepa-policy/">实现解读</a> · <a href="#qa-5edd75f877906c0b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:vjepa-policy" data-paper-title="V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents 基础模型 Tsinghua University 2026-09-29 冻结 V-JEPA 2.1 视觉编码器，在预测视觉潜空间中联合训练 instruction-conditioned future-latent predictor 和 flow-matching action expert；动作生成读取 predictor 的未来信息上下文。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 future-latent stop-gradient 与 action flow matching；未加载 V-JEPA 2.1 或机器人数据。执行 future-latent stop-gradient 与 action flow matching；未加载 V-JEPA 2.1 或机器人数据。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  世界动作模型 预测视觉潜变量 机器人 多模态 视觉世界建模：状态、生成与动作条件 动作专家读取预测未来潜变量，与直接读取训练视频未来帧有何区别？ 预测未来由当前观察与指令生成，部署时也能获得；真实未来仅作为训练目标，用于塑造预测器。动作 flow expert 因而使用可计算的前瞻上下文，而非提前观察结果。冻结视觉编码器稳定表示，却不保证预测误差不会在控制过程中累积。 例如根据当前桌面预测抓取后的杯子位置，再产生动作；不能把实际抓取结束后的照片先传给策略再评价成功率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-b1dc62a377da6fe6">动作专家读取预测未来潜变量，与直接读取训练视频未来帧有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Avjepa-policy">V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>预测未来由当前观察与指令生成，部署时也能获得；真实未来仅作为训练目标，用于塑造预测器。动作 flow expert 因而使用可计算的前瞻上下文，而非提前观察结果。冻结视觉编码器稳定表示，却不保证预测误差不会在控制过程中累积。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如根据当前桌面预测抓取后的杯子位置，再产生动作；不能把实际抓取结束后的照片先传给策略再评价成功率。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37250">原论文</a> · <a href="../../../../foundation-models/2609.37250-vjepa-policy/">实现解读</a> · <a href="#qa-b1dc62a377da6fe6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:vjepa-policy" data-paper-title="V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents 基础模型 Tsinghua University 2026-09-29 冻结 V-JEPA 2.1 视觉编码器，在预测视觉潜空间中联合训练 instruction-conditioned future-latent predictor 和 flow-matching action expert；动作生成读取 predictor 的未来信息上下文。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 future-latent stop-gradient 与 action flow matching；未加载 V-JEPA 2.1 或机器人数据。执行 future-latent stop-gradient 与 action flow matching；未加载 V-JEPA 2.1 或机器人数据。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  世界动作模型 预测视觉潜变量 机器人 多模态 视觉世界建模：状态、生成与动作条件 联合世界与动作训练与先训预测器再独立训动作头有什么区别？ 联合训练让未来预测与动作 flow 在同一训练框架中协调，动作专家使用 predictor 提供的未来信息；两阶段独立训练则可能让预测表征未适配控制需要。这里视觉 encoder 仍冻结，不能将联合 predictor/action 训练扩大为所有视觉参数都端到端更新。 例如动作头需要未来抓取位置，联合训练可协调预测上下文；但冻结 V-JEPA 编码器的权重依然不会因动作损失而变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-eae201df1d76d128">联合世界与动作训练与先训预测器再独立训动作头有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Avjepa-policy">V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>联合训练让未来预测与动作 flow 在同一训练框架中协调，动作专家使用 predictor 提供的未来信息；两阶段独立训练则可能让预测表征未适配控制需要。这里视觉 encoder 仍冻结，不能将联合 predictor/action 训练扩大为所有视觉参数都端到端更新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如动作头需要未来抓取位置，联合训练可协调预测上下文；但冻结 V-JEPA 编码器的权重依然不会因动作损失而变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37250">原论文</a> · <a href="../../../../foundation-models/2609.37250-vjepa-policy/">实现解读</a> · <a href="#qa-eae201df1d76d128">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:vjepa-policy" data-paper-title="V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents 基础模型 Tsinghua University 2026-09-29 冻结 V-JEPA 2.1 视觉编码器，在预测视觉潜空间中联合训练 instruction-conditioned future-latent predictor 和 flow-matching action expert；动作生成读取 predictor 的未来信息上下文。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 future-latent stop-gradient 与 action flow matching；未加载 V-JEPA 2.1 或机器人数据。执行 future-latent stop-gradient 与 action flow matching；未加载 V-JEPA 2.1 或机器人数据。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  世界动作模型 预测视觉潜变量 机器人 多模态 视觉世界建模：状态、生成与动作条件 future target 的梯度隔离与本地实现边界应怎样表述？ 真实未来经冻结视觉编码器产生目标并 stop-gradient，masked 位置上做 L1，同时训练动作速度损失。本地只执行 future-latent 隔离和 flow 机制诊断，没有加载 V-JEPA 2.1 或机器人数据，不能将三 seed 小张量更新说成 LIBERO 策略已验证。 例如检查目标张量没有梯度可确认监督边界，但没有任何机器人 rollout，就不能计算实际动作成功率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-44f9ff0a4f6450b9">future target 的梯度隔离与本地实现边界应怎样表述？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Avjepa-policy">V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>真实未来经冻结视觉编码器产生目标并 stop-gradient，masked 位置上做 L1，同时训练动作速度损失。本地只执行 future-latent 隔离和 flow 机制诊断，没有加载 V-JEPA 2.1 或机器人数据，不能将三 seed 小张量更新说成 LIBERO 策略已验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如检查目标张量没有梯度可确认监督边界，但没有任何机器人 rollout，就不能计算实际动作成功率。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37250">原论文</a> · <a href="../../../../foundation-models/2609.37250-vjepa-policy/">实现解读</a> · <a href="#qa-44f9ff0a4f6450b9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:vbvr-pro" data-paper-title="VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning 基础模型 Nanyang Technological University / VBVR Community 2026-08-26 通用 VLM judge 容易被流畅输出误导，难以逐实例核对时空状态。VBVR-Pro 为每种任务定义可执行 scorer，把中间状态、约束和最终状态都变成可验证奖励，并据此训练多模态生成模型。 Fidelity：核心机制的程序化验证。本地复刻 task-specific deterministic scorer 与标量 judge 对照，不训练视频生成大模型。该结果只验证 scorer 的确定性和可解释失败归因，不等同于论文七个外部 benchmark 或 14B/19B checkpoint 训练。本地对照口径：基线为带噪标量 VLM-judge analogue；实验组为三个确定性 task-specific verifier。300 个程序化任务 reward mean 0.5942 → 1.0000（+68.30%）。  multimodal-foundation-model native-visual-reasoning verifiable-reward benchmark 多模态 视觉世界建模：状态、生成与动作条件 可执行视觉 scorer 为什么要检查中间状态和约束，而不只看终图？ 终图可能看似合理却违反过程规则，例如物体穿越障碍或顺序错误。任务专属 scorer 把状态与约束变成可核验奖励，提供更可解释的失败定位；它依赖任务的可执行定义，不能把任意开放视觉推理都变成自动可验证。 例如最终球到了目标区，但轨迹穿过禁止墙面；只看终点会判成功，中间约束检查可以识别这条无效路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-vbvr-pro-eb931970" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a689a1bd0391b575">可执行视觉 scorer 为什么要检查中间状态和约束，而不只看终图？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Avbvr-pro">VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University / VBVR Community</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>终图可能看似合理却违反过程规则，例如物体穿越障碍或顺序错误。任务专属 scorer 把状态与约束变成可核验奖励，提供更可解释的失败定位；它依赖任务的可执行定义，不能把任意开放视觉推理都变成自动可验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如最终球到了目标区，但轨迹穿过禁止墙面；只看终点会判成功，中间约束检查可以识别这条无效路径。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26105">原论文</a> · <a href="../../../../reproductions/2608.26105-vbvr-pro/">实现解读</a> · <a href="#qa-a689a1bd0391b575">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:vbvr-pro" data-paper-title="VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning 基础模型 Nanyang Technological University / VBVR Community 2026-08-26 通用 VLM judge 容易被流畅输出误导，难以逐实例核对时空状态。VBVR-Pro 为每种任务定义可执行 scorer，把中间状态、约束和最终状态都变成可验证奖励，并据此训练多模态生成模型。 Fidelity：核心机制的程序化验证。本地复刻 task-specific deterministic scorer 与标量 judge 对照，不训练视频生成大模型。该结果只验证 scorer 的确定性和可解释失败归因，不等同于论文七个外部 benchmark 或 14B/19B checkpoint 训练。本地对照口径：基线为带噪标量 VLM-judge analogue；实验组为三个确定性 task-specific verifier。300 个程序化任务 reward mean 0.5942 → 1.0000（+68.30%）。  multimodal-foundation-model native-visual-reasoning verifiable-reward benchmark 多模态 视觉世界建模：状态、生成与动作条件 可执行 scorer 为什么比通用 VLM judge 更适合某些时空约束任务？ 任务若能明确列出中间状态、约束和最终条件，就可逐实例检查，而不只凭答案是否流畅判断。这样的奖励把可验证条件接入训练，但只覆盖已定义的规则；scorer 自身正确、被评模型不读 gold 与生成任务真正执行，仍是不同的验证要求。 例如移动方块不能穿墙且最终到达目标格，可逐步检查轨迹；一段听起来合理却实际穿墙的解释不应获得成功奖励。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-3c05a2d2ce10e7f4">可执行 scorer 为什么比通用 VLM judge 更适合某些时空约束任务？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Avbvr-pro">VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University / VBVR Community</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>任务若能明确列出中间状态、约束和最终条件，就可逐实例检查，而不只凭答案是否流畅判断。这样的奖励把可验证条件接入训练，但只覆盖已定义的规则；scorer 自身正确、被评模型不读 gold 与生成任务真正执行，仍是不同的验证要求。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如移动方块不能穿墙且最终到达目标格，可逐步检查轨迹；一段听起来合理却实际穿墙的解释不应获得成功奖励。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26105">原论文</a> · <a href="../../../../reproductions/2608.26105-vbvr-pro/">实现解读</a> · <a href="#qa-3c05a2d2ce10e7f4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:vbvr-pro" data-paper-title="VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning 基础模型 Nanyang Technological University / VBVR Community 2026-08-26 通用 VLM judge 容易被流畅输出误导，难以逐实例核对时空状态。VBVR-Pro 为每种任务定义可执行 scorer，把中间状态、约束和最终状态都变成可验证奖励，并据此训练多模态生成模型。 Fidelity：核心机制的程序化验证。本地复刻 task-specific deterministic scorer 与标量 judge 对照，不训练视频生成大模型。该结果只验证 scorer 的确定性和可解释失败归因，不等同于论文七个外部 benchmark 或 14B/19B checkpoint 训练。本地对照口径：基线为带噪标量 VLM-judge analogue；实验组为三个确定性 task-specific verifier。300 个程序化任务 reward mean 0.5942 → 1.0000（+68.30%）。  multimodal-foundation-model native-visual-reasoning verifiable-reward benchmark 多模态 视觉世界建模：状态、生成与动作条件 专属 verifier 与通用 VLM judge 在判断依据上有何不同？ verifier 根据明确状态和程序约束执行判断，通用 judge 以语义模型评价输出，可能受流畅叙述或视觉表面影响。前者更可复查但覆盖范围受限，后者较灵活却可能不稳定；不能用一个确定性 fixture 的满分推断模型视觉能力已提升。 例如几何任务可精确检查是否越界，但开放创意图的美感没有同样明确的布尔合同，不能照搬一个 scorer。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f61addb2d17becd9">专属 verifier 与通用 VLM judge 在判断依据上有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Avbvr-pro">VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University / VBVR Community</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>verifier 根据明确状态和程序约束执行判断，通用 judge 以语义模型评价输出，可能受流畅叙述或视觉表面影响。前者更可复查但覆盖范围受限，后者较灵活却可能不稳定；不能用一个确定性 fixture 的满分推断模型视觉能力已提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如几何任务可精确检查是否越界，但开放创意图的美感没有同样明确的布尔合同，不能照搬一个 scorer。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26105">原论文</a> · <a href="../../../../reproductions/2608.26105-vbvr-pro/">实现解读</a> · <a href="#qa-f61addb2d17becd9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:vbvr-pro" data-paper-title="VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning 基础模型 Nanyang Technological University / VBVR Community 2026-08-26 通用 VLM judge 容易被流畅输出误导，难以逐实例核对时空状态。VBVR-Pro 为每种任务定义可执行 scorer，把中间状态、约束和最终状态都变成可验证奖励，并据此训练多模态生成模型。 Fidelity：核心机制的程序化验证。本地复刻 task-specific deterministic scorer 与标量 judge 对照，不训练视频生成大模型。该结果只验证 scorer 的确定性和可解释失败归因，不等同于论文七个外部 benchmark 或 14B/19B checkpoint 训练。本地对照口径：基线为带噪标量 VLM-judge analogue；实验组为三个确定性 task-specific verifier。300 个程序化任务 reward mean 0.5942 → 1.0000（+68.30%）。  multimodal-foundation-model native-visual-reasoning verifiable-reward benchmark 多模态 视觉世界建模：状态、生成与动作条件 本地程序化 reward 从带噪基线到满分说明什么？ 只说明当前确定性 task-specific scorer 在给定程序化任务上的执行与失败归因，比带噪 judge analogue 稳定；不是多模态生成模型完成 RLVR 后的能力收益。原论文训练与外部 benchmark 需要真实轨迹、模型更新和独立评价，当前机制结果不能替代。 例如已知轨迹满足所有布尔条件时 scorer 返回一，验证的是评分器，不是证明生成模型能自己找到这样的轨迹。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8bddbd7e921c7fde">本地程序化 reward 从带噪基线到满分说明什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Avbvr-pro">VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University / VBVR Community</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只说明当前确定性 task-specific scorer 在给定程序化任务上的执行与失败归因，比带噪 judge analogue 稳定；不是多模态生成模型完成 RLVR 后的能力收益。原论文训练与外部 benchmark 需要真实轨迹、模型更新和独立评价，当前机制结果不能替代。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如已知轨迹满足所有布尔条件时 scorer 返回一，验证的是评分器，不是证明生成模型能自己找到这样的轨迹。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26105">原论文</a> · <a href="../../../../reproductions/2608.26105-vbvr-pro/">实现解读</a> · <a href="#qa-8bddbd7e921c7fde">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:mice" data-paper-title="Editing Everything Everywhere All at Once" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Editing Everything Everywhere All at Once 多模态大模型 University of Modena and Reggio Emilia 2026-06-30 多区域同时编辑容易把一处指令的属性传到另一处。MICE 在联合注意力中隔离不同文字组，并用实例掩码的平滑空间偏置控制视觉交互，以兼顾局部绑定与周围区域融合。方法不训练新的编辑模型。 以单张 A100/A30 或 Mac 的资源限制评估，完整矩阵需要大权重、长时间生成和外部服务，标注成本过高，不复现（审查 DONE）。诊断使用 2 个生成掩码、6×8 raster 和随机 Q/K/V，真实执行 attention 与反向传播。实现 instance_aware_masks、instance_log_bias、mice_joint_bias、mice_joint_attention 和统一 diagnostic(seed, device)。模块导入不加载 PyTorch，实际调用时才需要。输入必须是已经在同一网格上的、非空、互不重叠的二值 mask；  视觉生成与编辑 多实例编辑与注意力隔离 多模态 视觉世界建模：状态、生成与动作条件 MICE 的文字组隔离为什么对多实例编辑重要？ 多区域指令若完全互读，某实例的属性可能传播到另一实例。MICE 用组间隔离与实例空间偏置，把局部文字绑定到对应视觉区域，同时保留必要背景交互；这改变既有模型注意力，不需要训练新编辑模型，但仍依赖正确实例掩码。 例如“左杯变红、右杯变蓝”需要分别绑定两组文字；完全混合可能把两个杯子都涂成同一种颜色。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-multimodal-models-mice-b52a199b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7fbd2b03fd6b9570">MICE 的文字组隔离为什么对多实例编辑重要？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Amice">Editing Everything Everywhere All at Once</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Modena and Reggio Emilia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多区域指令若完全互读，某实例的属性可能传播到另一实例。MICE 用组间隔离与实例空间偏置，把局部文字绑定到对应视觉区域，同时保留必要背景交互；这改变既有模型注意力，不需要训练新编辑模型，但仍依赖正确实例掩码。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如“左杯变红、右杯变蓝”需要分别绑定两组文字；完全混合可能把两个杯子都涂成同一种颜色。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.31278v1">原论文</a> · <a href="../../../../multimodal-models/2606.31278-mice/">实现解读</a> · <a href="#qa-7fbd2b03fd6b9570">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:mice" data-paper-title="Editing Everything Everywhere All at Once" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Editing Everything Everywhere All at Once 多模态大模型 University of Modena and Reggio Emilia 2026-06-30 多区域同时编辑容易把一处指令的属性传到另一处。MICE 在联合注意力中隔离不同文字组，并用实例掩码的平滑空间偏置控制视觉交互，以兼顾局部绑定与周围区域融合。方法不训练新的编辑模型。 以单张 A100/A30 或 Mac 的资源限制评估，完整矩阵需要大权重、长时间生成和外部服务，标注成本过高，不复现（审查 DONE）。诊断使用 2 个生成掩码、6×8 raster 和随机 Q/K/V，真实执行 attention 与反向传播。实现 instance_aware_masks、instance_log_bias、mice_joint_bias、mice_joint_attention 和统一 diagnostic(seed, device)。模块导入不加载 PyTorch，实际调用时才需要。输入必须是已经在同一网格上的、非空、互不重叠的二值 mask；  视觉生成与编辑 多实例编辑与注意力隔离 多模态 视觉世界建模：状态、生成与动作条件 多实例编辑为什么同时需要文字组隔离与平滑空间偏置？ 文字组隔离减少一条编辑指令直接影响另一组语义，空间偏置则把该指令绑定到相应实例并允许边界附近融合。只有硬切区域可能产生接缝，只有全局文字约束又可能串色；偏置在注意力里控制可见性，并不等于训练了一个新的编辑模型。 例如要求左鞋变红、右鞋变蓝，文字组不应互相传播颜色，而平滑实例区域帮助各自颜色与周围图像自然衔接。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-17c3380975ca6c68">多实例编辑为什么同时需要文字组隔离与平滑空间偏置？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Amice">Editing Everything Everywhere All at Once</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Modena and Reggio Emilia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文字组隔离减少一条编辑指令直接影响另一组语义，空间偏置则把该指令绑定到相应实例并允许边界附近融合。只有硬切区域可能产生接缝，只有全局文字约束又可能串色；偏置在注意力里控制可见性，并不等于训练了一个新的编辑模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如要求左鞋变红、右鞋变蓝，文字组不应互相传播颜色，而平滑实例区域帮助各自颜色与周围图像自然衔接。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.31278v1">原论文</a> · <a href="../../../../multimodal-models/2606.31278-mice/">实现解读</a> · <a href="#qa-17c3380975ca6c68">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:mice" data-paper-title="Editing Everything Everywhere All at Once" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Editing Everything Everywhere All at Once 多模态大模型 University of Modena and Reggio Emilia 2026-06-30 多区域同时编辑容易把一处指令的属性传到另一处。MICE 在联合注意力中隔离不同文字组，并用实例掩码的平滑空间偏置控制视觉交互，以兼顾局部绑定与周围区域融合。方法不训练新的编辑模型。 以单张 A100/A30 或 Mac 的资源限制评估，完整矩阵需要大权重、长时间生成和外部服务，标注成本过高，不复现（审查 DONE）。诊断使用 2 个生成掩码、6×8 raster 和随机 Q/K/V，真实执行 attention 与反向传播。实现 instance_aware_masks、instance_log_bias、mice_joint_bias、mice_joint_attention 和统一 diagnostic(seed, device)。模块导入不加载 PyTorch，实际调用时才需要。输入必须是已经在同一网格上的、非空、互不重叠的二值 mask；  视觉生成与编辑 多实例编辑与注意力隔离 多模态 视觉世界建模：状态、生成与动作条件 软空间偏置与对区域外 token 全部 hard mask 有何区别？ 平滑掩码取对数后给区域外有限负偏置，让边缘有逐渐衰减的交互以融合周围内容；hard mask 则彻底禁止。无关文字组仍用负无穷隔离，不能把所有边都统一软化；正文与作者默认代码还存在版本差异，本地明确遵循 paper_v1。 例如物体边缘附近的阴影可获得较弱联系帮助融合，但另一实例专属像素被清零，避免把局部编辑扩散过去。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5967ac30be26b54d">软空间偏置与对区域外 token 全部 hard mask 有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Amice">Editing Everything Everywhere All at Once</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Modena and Reggio Emilia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>平滑掩码取对数后给区域外有限负偏置，让边缘有逐渐衰减的交互以融合周围内容；hard mask 则彻底禁止。无关文字组仍用负无穷隔离，不能把所有边都统一软化；正文与作者默认代码还存在版本差异，本地明确遵循 paper_v1。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如物体边缘附近的阴影可获得较弱联系帮助融合，但另一实例专属像素被清零，避免把局部编辑扩散过去。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.31278v1">原论文</a> · <a href="../../../../multimodal-models/2606.31278-mice/">实现解读</a> · <a href="#qa-5967ac30be26b54d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:mice" data-paper-title="Editing Everything Everywhere All at Once" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Editing Everything Everywhere All at Once 多模态大模型 University of Modena and Reggio Emilia 2026-06-30 多区域同时编辑容易把一处指令的属性传到另一处。MICE 在联合注意力中隔离不同文字组，并用实例掩码的平滑空间偏置控制视觉交互，以兼顾局部绑定与周围区域融合。方法不训练新的编辑模型。 以单张 A100/A30 或 Mac 的资源限制评估，完整矩阵需要大权重、长时间生成和外部服务，标注成本过高，不复现（审查 DONE）。诊断使用 2 个生成掩码、6×8 raster 和随机 Q/K/V，真实执行 attention 与反向传播。实现 instance_aware_masks、instance_log_bias、mice_joint_bias、mice_joint_attention 和统一 diagnostic(seed, device)。模块导入不加载 PyTorch，实际调用时才需要。输入必须是已经在同一网格上的、非空、互不重叠的二值 mask；  视觉生成与编辑 多实例编辑与注意力隔离 多模态 视觉世界建模：状态、生成与动作条件 为什么 ε=10^-30 的偏置至少用 float32，且 context 到视觉域不能随意加空间 mask？ float16 可能使极小 ε 下溢，改变有限 log 偏置的语义；softmax 与累加需至少 float32。本地采用正文 Case 5 的 context 到整个视觉域无偏置，不能混入示意图或默认 processor 的不同规则，再声称各版本完全等价。 例如区域外 log(ε) 本应是有限大负数，若下溢成零再取对数就变成负无穷，软衰减被意外改为硬禁止。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-9dcf4741dcb5f179">为什么 ε=10^-30 的偏置至少用 float32，且 context 到视觉域不能随意加空间 mask？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Amice">Editing Everything Everywhere All at Once</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Modena and Reggio Emilia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>float16 可能使极小 ε 下溢，改变有限 log 偏置的语义；softmax 与累加需至少 float32。本地采用正文 Case 5 的 context 到整个视觉域无偏置，不能混入示意图或默认 processor 的不同规则，再声称各版本完全等价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如区域外 log(ε) 本应是有限大负数，若下溢成零再取对数就变成负无穷，软衰减被意外改为硬禁止。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、原文与代码版本边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.31278v1">原论文</a> · <a href="../../../../multimodal-models/2606.31278-mice/">实现解读</a> · <a href="#qa-9dcf4741dcb5f179">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

模型是在识别画面，还是能判断动作将怎样改变状态？

## 记住这一点

把观察、动作和后续状态放在一起，才能学习可用于预测或控制的表示。LeWAM 联合学习未来潜状态预测与动作 flow matching，让视觉表征和策略相互塑造；规划时再用潜动力学评价动作候选。WOVEN 则把视频生成的视觉转移组织成场景、动作、推理类型受控的监督，训练模型理解结果、原因与反事实。

## 一个例子

同一桌面，把杯子向左推和向右推应产生不同结果；只认出“桌上有杯子”不足以控制机器人。表征预测可避免逐像素重建，但仍要检验动作条件是否有效、rollout 多步后是否漂移，以及选出的动作能否在闭环环境到达目标。

## 什么时候要小心

生成视频逼真、一步预测误差小或训练集问答分数高，都不自动证明规划有效。源场景与轨迹要分组隔离，反事实不能泄漏未来结果。本地 LeWAM 尚是非 holdout 闭环诊断，WOVEN 是小规模公开训练源实验；都不能替代原文完整泛化或机器人结论。

## 先读这几篇

先读 LeWAM 的潜状态/动作联合目标，理解预测怎样进入控制；再读 WOVEN 的视觉转移与受控监督，区分表征学习、生成数据、问答推理和闭环规划。之后按视觉几何、视频记忆或具身动作细分。

1. [LeWAM: End-to-End World and Action Modeling with JEPAs](../../../reproductions/2610.12818-lewam/README.md) · [原论文](https://arxiv.org/abs/2610.12818)
2. [WOVEN: Weaving Visual World Modeling into Multimodal LLMs](../../../reproductions/2610.12417-woven/README.md) · [原论文](https://arxiv.org/abs/2610.12417)

## 自测一下

世界模型的一步 latent MSE 更低，是否必然能带来更高的长程控制成功率？

??? note "展开参考答案"

    不必然。误差可能集中在与动作选择无关的方向，多步 rollout 还会累积偏差，策略搜索也可能利用模型漏洞。需要相同环境、目标和预算下的闭环控制对照，且不能用训练目标轨迹冒充 holdout。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
