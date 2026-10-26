---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 偏好与对齐：先看反馈长什么样

[LLM 后训练](index.md) / 子主题导学 · 约 3 分钟 · 25 张论文卡

## 先想一个问题

只有“更喜欢哪个回答”或单条点赞时，怎样把反馈变成可学习目标？

## 记住这一点

先辨认监督的形状。DPO 使用同一提示下的优劣回答对，并通过当前策略相对参考策略的概率比建立偏好分类目标；KTO 面向单条满意或不满意反馈，不要求成对。奖励模型、AI评审和可控SFT则改变反馈来源或目标组织。反馈格式、参考分布和标注可靠性共同决定可用方法，不能只凭算法名字替换损失。

## 一个例子

例如一个客服系统有两批数据：一批是同题两答案的人工排序，另一批只有用户是否接受单条回答。前一批可组织为DPO偏好对；后一批不能随意把不同问题的回答拼成优劣对。若不同风格的人群意见相反，还需要记录偏好分布与标注来源，避免把评审模型的文风喜好误作事实正确性。

## 什么时候要小心

偏好提高不保证知识正确、安全或生产收益。比较需固定数据、参考模型和评估口径，并检查长度、风格等混杂。库中的闭式损失、候选策略或偏好夹具只验证相应机制；评分器协议检查和未复现实验不能被写成模型已经完成对齐。

## 先读这几篇

先读DPO，理解偏好对与参考log-ratio；再读KTO，对比单条二元反馈；最后读概率Autorater，理解评审置信分布与单一胜负标签的差别。

1. [DPO](../../../post-training/2305.18290-dpo/README.md) · [原论文](https://arxiv.org/abs/2305.18290)
2. [KTO](../../../post-training/2402.01306-kto/README.md) · [原论文](https://arxiv.org/abs/2402.01306)
3. [Judging with Confidence: Calibrating Autoraters to Preference Distributions](../../../post-training/2510.00263-probabilistic-autorater/README.md) · [原论文](https://arxiv.org/abs/2510.00263v1)

## 自测一下

有一条回答获赞，另一问题的回答被点踩，可以直接组成DPO训练对吗？

??? note "展开参考答案"

    通常不能。DPO的标准偏好对要求共享同一条件；跨问题配对会混入难度与内容差异。可收集同题备选形成真实偏好，或选择面向单条反馈的目标，并明确类别分布、参考策略与独立评估。

## 这个子主题的论文卡片

导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">
<div class="ar-learning-controls">
<label for="learning-search">搜索卡片
<input id="learning-search" type="search" data-learning-search placeholder="搜索论文、机制、机构或本地边界"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">共 25 张卡片</p>
<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="CleanRM: Reward Modeling from Noisy Feedback with a Few Clean Feedback for RLHF LLM 后训练 Zhejiang University 2026-10-15 不同偏好样本的标注噪声不一定相同。CleanRM 用少量干净反馈校准两个方向的样本级噪声率；以语义与恢复偏好的联合分布作最优传输，而不是只匹配偏好直方图。随后固定估计器，用去偏 surrogate 训练 RM。 完整 RM/RLHF 实验成本过高，不复现（审查 DONE）。L1 小特征、真实 joint OT 与 signed corrected loss 组件。不用预知噪声率代替核心估计器；不把合成机制结果称为真实 RLHF 安全能力。完整 RM/RLHF 实验成本过高，不复现（审查 DONE）。NoiseEstimator 通过三路 softmax 保证两向噪声率非负、总和至多 .95。noise_estimation_loss 只读取 noisy features/观察反馈以及独立 clean calibration 子集，不接收已知真实噪声率。编码特征在组件中视为固定，未下载原文 LLM backbone。  二元反馈对齐 后训练算法组件 CleanRM LLM 后训练 偏好与对齐：先看反馈长什么样">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<h2 id="paper-post-training-clean-rm-81560dec">CleanRM: Reward Modeling from Noisy Feedback with a Few Clean Feedback for RLHF</h2>
<p class="ar-learning-card__meta">Zhejiang University · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>不同偏好样本的标注噪声不一定相同。CleanRM 用少量干净反馈校准两个方向的样本级噪声率；以语义与恢复偏好的联合分布作最优传输，而不是只匹配偏好直方图。随后固定估计器，用去偏 surrogate 训练 RM。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整 RM/RLHF 实验成本过高，不复现（审查 DONE）。L1 小特征、真实 joint OT 与 signed corrected loss 组件。不用预知噪声率代替核心估计器；不把合成机制结果称为真实 RLHF 安全能力。完整 RM/RLHF 实验成本过高，不复现（审查 DONE）。NoiseEstimator 通过三路 softmax 保证两向噪声率非负、总和至多 .95。noise_estimation_loss 只读取 noisy features/观察反馈以及独立 clean calibration 子集，不接收已知真实噪声率。编码特征在组件中视为固定，未下载原文 LLM backbone。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21138v1">原论文</a> · <a href="../../../../post-training/2610.21138-clean-rm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="GAW-PO: Preference Optimization with Gradient-Aligned Token Weights LLM 后训练 National University of Science and Technology POLITEHNICA Bucharest 2026-10-01 用拒绝 token 梯度与 preferred update direction 的对齐度调节负权重；越支持优选行为的 token 越少受罚。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行梯度对齐权重；未进行 LoRA/DPO 训练。执行梯度对齐权重；未进行 LoRA/DPO 训练。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  偏好优化 token credit DPO LLM 后训练 偏好与对齐：先看反馈长什么样">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<h2 id="paper-post-training-gaw-po-bf9dde22">GAW-PO: Preference Optimization with Gradient-Aligned Token Weights</h2>
<p class="ar-learning-card__meta">National University of Science and Technology POLITEHNICA Bucharest · 论文公开：2026-10-01</p>
<p><strong>方法要点：</strong>用拒绝 token 梯度与 preferred update direction 的对齐度调节负权重；越支持优选行为的 token 越少受罚。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行梯度对齐权重；未进行 LoRA/DPO 训练。执行梯度对齐权重；未进行 LoRA/DPO 训练。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01511">原论文</a> · <a href="../../../../post-training/2610.01511-gaw-po/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="A Zeroth-Order Paradigm for LLM Preference Alignment LLM 后训练 University of California, Berkeley 2026-09-16 不求偏好目标梯度，只比较正负参数扰动的结果得到一比特方向，再以逐坐标阈值抑制噪声。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行一比特比较 oracle 与阈值化更新；mini-suite 不是大模型对齐结果。本地执行一比特比较 oracle 与阈值化更新；mini-suite 不是大模型对齐结果。  偏好优化 零阶优化 LLM 后训练 偏好与对齐：先看反馈长什么样">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<h2 id="paper-post-training-compo-257a1fd8">A Zeroth-Order Paradigm for LLM Preference Alignment</h2>
<p class="ar-learning-card__meta">University of California, Berkeley · 论文公开：2026-09-16</p>
<p><strong>方法要点：</strong>不求偏好目标梯度，只比较正负参数扰动的结果得到一比特方向，再以逐坐标阈值抑制噪声。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行一比特比较 oracle 与阈值化更新；mini-suite 不是大模型对齐结果。本地执行一比特比较 oracle 与阈值化更新；mini-suite 不是大模型对齐结果。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.19144">原论文</a> · <a href="../../../../post-training/2609.19144-compo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Style-Debiased DPO: Updating LLM Knowledge with Factuality-Aware Synthetic Preference Data LLM 后训练 Waseda University 2026-09-15 识别事实正确但风格不同的 rejected response，反转其偏好方向并按组比例加权以抵消风格梯度。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行偏好反转和组平衡损失；事实分数由 fixture 提供，不冒充 judge LLM。本地执行偏好反转和组平衡损失；事实分数由 fixture 提供，不冒充 judge LLM。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  偏好优化 知识更新 LLM 后训练 偏好与对齐：先看反馈长什么样">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<h2 id="paper-post-training-sd-dpo-8723680d">Style-Debiased DPO: Updating LLM Knowledge with Factuality-Aware Synthetic Preference Data</h2>
<p class="ar-learning-card__meta">Waseda University · 论文公开：2026-09-15</p>
<p><strong>方法要点：</strong>识别事实正确但风格不同的 rejected response，反转其偏好方向并按组比例加权以抵消风格梯度。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行偏好反转和组平衡损失；事实分数由 fixture 提供，不冒充 judge LLM。本地执行偏好反转和组平衡损失；事实分数由 fixture 提供，不冒充 judge LLM。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16532">原论文</a> · <a href="../../../../post-training/2609.16532-sd-dpo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Disentangling Optimization Scale from Preference Scale in DPO LLM 后训练 Affiliation not listed in the paper 2026-08-27 标准 DPO 的同时改变偏好噪声尺度与梯度幅度，导致有效学习率被隐式重缩放。论文用除以的 centered-softplus 保持相同 argmin，同时让梯度尺度在时不消失。 复现级别：核心公式 mini-suite。复现级别：核心公式 mini-suite。实现 centered-softplus 归一化目标及连续的极限。本地为候选策略机制验证，不是语言模型偏好数据全量训练。arithmetic-smoke、100 steps：accuracy 0.1953 → 0.4766，并记录 preference margin、normalized loss 与梯度力。指标见 metrics/arithmetic-smoke-seed42.json。  DPO 偏好/优化尺度解耦 LLM 后训练 偏好与对齐：先看反馈长什么样">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<h2 id="paper-post-training-normalized-dpo-59718764">Disentangling Optimization Scale from Preference Scale in DPO</h2>
<p class="ar-learning-card__meta">Affiliation not listed in the paper · 论文公开：2026-08-27</p>
<p><strong>方法要点：</strong>标准 DPO 的同时改变偏好噪声尺度与梯度幅度，导致有效学习率被隐式重缩放。论文用除以的 centered-softplus 保持相同 argmin，同时让梯度尺度在时不消失。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心公式 mini-suite。复现级别：核心公式 mini-suite。实现 centered-softplus 归一化目标及连续的极限。本地为候选策略机制验证，不是语言模型偏好数据全量训练。arithmetic-smoke、100 steps：accuracy 0.1953 → 0.4766，并记录 preference margin、normalized loss 与梯度力。指标见 metrics/arithmetic-smoke-seed42.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27032">原论文</a> · <a href="../../../../post-training/2608.27032-normalized-dpo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="GRIP: Granular Reward-Guided Parameter Interpolation for Efficient Reasoning LLM 后训练 Peking University 2026-08-26 在 thinking 与 instruct 权重间，不使用单一全局系数，而由细粒度 reward 学习分层/参数插值，使模型保留推理准确率同时缩短输出。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。本地对照口径：arithmetic-smoke 100 steps，accuracy 0.1250 → 0.2344（+87.50%）；本地在策略概率而非大模型权重上验证 reward-guided interpolation。  奖励引导参数插值 LLM 后训练 偏好与对齐：先看反馈长什么样">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<h2 id="paper-post-training-grip-70305ebb">GRIP: Granular Reward-Guided Parameter Interpolation for Efficient Reasoning</h2>
<p class="ar-learning-card__meta">Peking University · 论文公开：2026-08-26</p>
<p><strong>方法要点：</strong>在 thinking 与 instruct 权重间，不使用单一全局系数，而由细粒度 reward 学习分层/参数插值，使模型保留推理准确率同时缩短输出。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。本地对照口径：arithmetic-smoke 100 steps，accuracy 0.1250 → 0.2344（+87.50%）；本地在策略概率而非大模型权重上验证 reward-guided interpolation。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25583">原论文</a> · <a href="../../../../post-training/2608.25583-grip/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Context Blindness in DPO: Mitigating Object Hallucination in MLLMs via Context-Calibrated Preference Optimization LLM 后训练 Korea University 2026-08-12 普通 DPO 即使输入相关图像上下文，也可能主要依赖语言先验。论文先定义 CPG，度量加入上下文后 chosen/rejected preference margin 增加多少；C²-DPO 直接扩大该增益，同时保留原偏好顺序。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实际计算 full/degraded context 的 Contextual Preference Gain 并参与偏好更新；不把候选策略模型写成完整 MLLM 微调。尚未下载 Qwen2-VL、SENTINEL 与 Object HalBench 做完整微调；MR7 同时提供 checkpoint matrix / lmms-eval 基础设施，后续可把该目标接入真实 MLLM 训练。120 steps arithmetic mini-suite：accuracy 0.1953→0.6719；  多模态上下文偏好校准 LLM 后训练 偏好与对齐：先看反馈长什么样">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<h2 id="paper-post-training-c2-dpo-2993ea41">Context Blindness in DPO: Mitigating Object Hallucination in MLLMs via Context-Calibrated Preference Optimization</h2>
<p class="ar-learning-card__meta">Korea University · 论文公开：2026-08-12</p>
<p><strong>方法要点：</strong>普通 DPO 即使输入相关图像上下文，也可能主要依赖语言先验。论文先定义 CPG，度量加入上下文后 chosen/rejected preference margin 增加多少；C²-DPO 直接扩大该增益，同时保留原偏好顺序。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实际计算 full/degraded context 的 Contextual Preference Gain 并参与偏好更新；不把候选策略模型写成完整 MLLM 微调。尚未下载 Qwen2-VL、SENTINEL 与 Object HalBench 做完整微调；MR7 同时提供 checkpoint matrix / lmms-eval 基础设施，后续可把该目标接入真实 MLLM 训练。120 steps arithmetic mini-suite：accuracy 0.1953→0.6719；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.12158">原论文</a> · <a href="../../../../post-training/2608.12158-c2-dpo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Preference Tree Optimization: Enhancing Goal-Oriented Dialogue with Look-Ahead Simulations LLM 后训练 Reichman University 2026-08-12 逐轮偏好只判断当前回答，难以优化目标导向对话的长期结果。PTO 让 agent 和虚拟用户展开候选对话树，oracle 评价当前回答及未来延续，以偏好对迭代执行 DPO；更深 look-ahead 带来更稳定的长期策略。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实际构造 preference tree、oracle 排序与 look-ahead advantage；不冒充论文的心理咨询模型实验。未运行 Llama-2-7B、虚拟心理咨询患者或 LLM oracle；本地 deterministic reward 仅替代昂贵 evaluator，偏好树与前瞻信用路径实际执行。120 steps 的 arithmetic mini-suite 中，初始 accuracy 0.1953，PTO 路径为 0.4453；  前瞻偏好树 LLM 后训练 偏好与对齐：先看反馈长什么样">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<h2 id="paper-post-training-pto-55a5beae">Preference Tree Optimization: Enhancing Goal-Oriented Dialogue with Look-Ahead Simulations</h2>
<p class="ar-learning-card__meta">Reichman University · 论文公开：2026-08-12</p>
<p><strong>方法要点：</strong>逐轮偏好只判断当前回答，难以优化目标导向对话的长期结果。PTO 让 agent 和虚拟用户展开候选对话树，oracle 评价当前回答及未来延续，以偏好对迭代执行 DPO；更深 look-ahead 带来更稳定的长期策略。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实际构造 preference tree、oracle 排序与 look-ahead advantage；不冒充论文的心理咨询模型实验。未运行 Llama-2-7B、虚拟心理咨询患者或 LLM oracle；本地 deterministic reward 仅替代昂贵 evaluator，偏好树与前瞻信用路径实际执行。120 steps 的 arithmetic mini-suite 中，初始 accuracy 0.1953，PTO 路径为 0.4453；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.12062">原论文</a> · <a href="../../../../post-training/2608.12062-pto/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="What do Reward Models Memorize? LLM 后训练 ILLC, University of Amsterdam 2026-07-27 Sec.3 Eq.1–2：对每个真实run的reward差先sigmoid，再分别对训练内20次和留出5次求均值，CM=TM−TG。必须按用户划分，不能同用户不同偏好对跨train/test。组件只聚合调用方提供的真实run分数/manifest并检验用户一致；不制造25个RM、不实现描述不充分的cooccurrence搜索、不把sigmoid(mean margin)冒充mean(sigmoid margin)。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。seed42/43/44并不把合成诊断变成真实能力评测。状态：独立 L1 数值/协议组件，diagnostic only；不代表真实LLM能力、训练收益或完整论文复现。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本地仅执行 counterfactual_memorization 及配套数值协议。外部真实模型/数据观测是调用方前提，不由fixture伪造。  奖励建模与评估协议 Counterfactual memorization LLM 后训练 偏好与对齐：先看反馈长什么样">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<h2 id="paper-post-training-rm-memorization-protocol-fc530cbb">What do Reward Models Memorize?</h2>
<p class="ar-learning-card__meta">ILLC, University of Amsterdam · 论文公开：2026-07-27</p>
<p><strong>方法要点：</strong>Sec.3 Eq.1–2：对每个真实run的reward差先sigmoid，再分别对训练内20次和留出5次求均值，CM=TM−TG。必须按用户划分，不能同用户不同偏好对跨train/test。组件只聚合调用方提供的真实run分数/manifest并检验用户一致；不制造25个RM、不实现描述不充分的cooccurrence搜索、不把sigmoid(mean margin)冒充mean(sigmoid margin)。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。seed42/43/44并不把合成诊断变成真实能力评测。状态：独立 L1 数值/协议组件，diagnostic only；不代表真实LLM能力、训练收益或完整论文复现。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本地仅执行 counterfactual_memorization 及配套数值协议。外部真实模型/数据观测是调用方前提，不由fixture伪造。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24484v1">原论文</a> · <a href="../../../../post-training/2607.24484-rm-memorization-protocol/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Mind the Gap: Structure-Aware Consistency in Preference Learning LLM 后训练 Google Research / Courant Institute of Mathematical Sciences 2026-04-30 对语义几乎相同的回答强求固定偏好间隔，会制造难以满足的约束。SA-DPO 将间隔改为回答距离的函数，保留相对参考策略的隐式奖励差；同时研究 margin、模型容量与 surrogate 尾部的一致性关系，而非单纯调整 DPO 的学习率。图依据原文 §5.3 重绘。原文 Figure 1 与目标函数。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。§7、附录 M 使用 Llama-3-8B LoRA；真实数据实验为 UltraFeedback 20k、1,200 步、batch 16，另需语义编码器、多基线和多次运行。完整比较估计为多小时级，成本过高，不复现（审查 DONE）；不是本地耗时实测。  直接偏好优化 语义距离自适应间隔 LLM 后训练 偏好与对齐：先看反馈长什么样">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<h2 id="paper-post-training-sa-dpo-319b4acc">Mind the Gap: Structure-Aware Consistency in Preference Learning</h2>
<p class="ar-learning-card__meta">Google Research / Courant Institute of Mathematical Sciences · 论文公开：2026-04-30</p>
<p><strong>方法要点：</strong>对语义几乎相同的回答强求固定偏好间隔，会制造难以满足的约束。SA-DPO 将间隔改为回答距离的函数，保留相对参考策略的隐式奖励差；同时研究 margin、模型容量与 surrogate 尾部的一致性关系，而非单纯调整 DPO 的学习率。图依据原文 §5.3 重绘。原文 Figure 1 与目标函数。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。§7、附录 M 使用 Llama-3-8B LoRA；真实数据实验为 UltraFeedback 20k、1,200 步、batch 16，另需语义编码器、多基线和多次运行。完整比较估计为多小时级，成本过高，不复现（审查 DONE）；不是本地耗时实测。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.27733v1">原论文</a> · <a href="../../../../post-training/2604.27733-sa-dpo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="GroupDPO: Memory-Efficient Group-Wise Direct Preference Optimization LLM 后训练 Carnegie Mellon University 2026-04-17 GroupDPO 先无梯度计算所有响应在当前参数点的全组导数，再固定这些系数逐响应微批次反传，保留完整组目标的一阶梯度。它支持一条提示的多个正负响应，避免为计算组目标而同时保留整组模型激活；不保证替身损失值或二阶导数等价。本地核对 v1 / v2 的 §4、Algorithm 1 和 Table 1；所实现的四类目标及一阶替身机制未见实质变化。本实现以固定 v2 为准，包括对共享响应累计贡献、损失值不相等以及不保留二阶结构的边界。 完整实验：成本过高，不复现（审查 DONE）。诊断用小型真实线性神经模型，4 个组目标 × SGD / AdamW × 3 次参数更新，对照整组联合反传；L1 精确机制组件，diagnostic only，不是完整大模型能力复现，未接入 Evolve、不可晋级。完整实验：成本过高，不复现（审查 DONE）。本篇是 Google 官方会议页带出的历史补漏，不是 10 月 25 日新发表论文。backward_microbatched 先分块执行 no-grad 策略前向，将少量标量组成完整响应向量；全组系数和正样本 NLL 权重都在这一步固定。  偏好优化 组级目标与梯度等价微批次 LLM 后训练 偏好与对齐：先看反馈长什么样">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<h2 id="paper-post-training-group-dpo-93d61191">GroupDPO: Memory-Efficient Group-Wise Direct Preference Optimization</h2>
<p class="ar-learning-card__meta">Carnegie Mellon University · 论文公开：2026-04-17</p>
<p><strong>方法要点：</strong>GroupDPO 先无梯度计算所有响应在当前参数点的全组导数，再固定这些系数逐响应微批次反传，保留完整组目标的一阶梯度。它支持一条提示的多个正负响应，避免为计算组目标而同时保留整组模型激活；不保证替身损失值或二阶导数等价。本地核对 v1 / v2 的 §4、Algorithm 1 和 Table 1；所实现的四类目标及一阶替身机制未见实质变化。本实现以固定 v2 为准，包括对共享响应累计贡献、损失值不相等以及不保留二阶结构的边界。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验：成本过高，不复现（审查 DONE）。诊断用小型真实线性神经模型，4 个组目标 × SGD / AdamW × 3 次参数更新，对照整组联合反传；L1 精确机制组件，diagnostic only，不是完整大模型能力复现，未接入 Evolve、不可晋级。完整实验：成本过高，不复现（审查 DONE）。本篇是 Google 官方会议页带出的历史补漏，不是 10 月 25 日新发表论文。backward_microbatched 先分块执行 no-grad 策略前向，将少量标量组成完整响应向量；全组系数和正样本 NLL 权重都在这一步固定。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.15602v1">原论文</a> · <a href="../../../../post-training/2604.15602-group-dpo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="When LLMs Benchmark Themselves: Deconstructing Self-Bias in Automated Evaluation LLM 后训练 Google 2025-09-30 Sec.2 Eq.1使用[segment,target,benchmark-role]的逐segment排名，先按segment平均，再diag−leave-self-out peers。原始分数方向必须明确，MetricX-QE越低越好。论文未公开ties细节，本地平均tie是显式约定；不把peer consensus当绝对真值，不在合成表上宣称真实模型有偏。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。seed42/43/44并不把合成诊断变成真实能力评测。状态：独立 L1 数值/协议组件，diagnostic only；不代表真实LLM能力、训练收益或完整论文复现。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本地仅执行 self_bias 及配套数值协议。外部真实模型/数据观测是调用方前提，不由fixture伪造。  LLM评估与校准 自偏好与生成式benchmark LLM 后训练 偏好与对齐：先看反馈长什么样">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<h2 id="paper-post-training-benchmark-self-bias-143e8f64">When LLMs Benchmark Themselves: Deconstructing Self-Bias in Automated Evaluation</h2>
<p class="ar-learning-card__meta">Google · 论文公开：2025-09-30</p>
<p><strong>方法要点：</strong>Sec.2 Eq.1使用[segment,target,benchmark-role]的逐segment排名，先按segment平均，再diag−leave-self-out peers。原始分数方向必须明确，MetricX-QE越低越好。论文未公开ties细节，本地平均tie是显式约定；不把peer consensus当绝对真值，不在合成表上宣称真实模型有偏。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。seed42/43/44并不把合成诊断变成真实能力评测。状态：独立 L1 数值/协议组件，diagnostic only；不代表真实LLM能力、训练收益或完整论文复现。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本地仅执行 self_bias 及配套数值协议。外部真实模型/数据观测是调用方前提，不由fixture伪造。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2509.26600v1">原论文</a> · <a href="../../../../post-training/2509.26600-benchmark-self-bias/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Judging with Confidence: Calibrating Autoraters to Preference Distributions LLM 后训练 Google 2025-09-30 Sec.3 Eq.1–2 piecewise奖励和实验用epsilon=.001可精确实现。解析成功必须在[0,1]；失败Brier=0、Log=log(epsilon)。本地严格tag parser是明确的本地约定，不是作者未公开parser；数学梯度诊断不代表可以对生成文本float解析反传，更不等于GRPO训练。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。seed42/43/44并不把合成诊断变成真实能力评测。状态：独立 L1 数值/协议组件，diagnostic only；不代表真实LLM能力、训练收益或完整论文复现。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本地仅执行 proper_rewards 及配套数值协议。外部真实模型/数据观测是调用方前提，不由fixture伪造。  奖励建模与校准 概率偏好与proper scoring rules LLM 后训练 偏好与对齐：先看反馈长什么样">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<h2 id="paper-post-training-probabilistic-autorater-421e42ad">Judging with Confidence: Calibrating Autoraters to Preference Distributions</h2>
<p class="ar-learning-card__meta">Google · 论文公开：2025-09-30</p>
<p><strong>方法要点：</strong>Sec.3 Eq.1–2 piecewise奖励和实验用epsilon=.001可精确实现。解析成功必须在[0,1]；失败Brier=0、Log=log(epsilon)。本地严格tag parser是明确的本地约定，不是作者未公开parser；数学梯度诊断不代表可以对生成文本float解析反传，更不等于GRPO训练。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。seed42/43/44并不把合成诊断变成真实能力评测。状态：独立 L1 数值/协议组件，diagnostic only；不代表真实LLM能力、训练收益或完整论文复现。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本地仅执行 proper_rewards 及配套数值协议。外部真实模型/数据观测是调用方前提，不由fixture伪造。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.00263v1">原论文</a> · <a href="../../../../post-training/2510.00263-probabilistic-autorater/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="SimPO LLM 后训练 Princeton University 2024-05-23 DPO 训练需要常驻 reference model，而且 sequence 概率天然偏向短响应。SimPO 用平均 token log-probability 作为隐式 reward，去掉 reference model，并在 Bradley–Terry 目标中加入固定 margin。 用长度归一化的 policy log-probability 直接作 reward，并用目标 margin 拉开偏好。核心 sequence normalization、reference-free reward 和 margin 已落到真实 token loss；未复刻 Mistral/Llama/Gemma 规模训练及 AlpacaEval judge。本地在自由生成 causal LM 上实现平均 token log-probability 和 margin，训练时不创建 reference model；用相同 warmup、数据、步数与 seed 和其他自由生成方法比较。  Reference-free 偏好 LLM 后训练 偏好与对齐：先看反馈长什么样">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<h2 id="paper-post-training-simpo-d55ff0e4">SimPO</h2>
<p class="ar-learning-card__meta">Princeton University · 论文公开：2024-05-23</p>
<p><strong>方法要点：</strong>DPO 训练需要常驻 reference model，而且 sequence 概率天然偏向短响应。SimPO 用平均 token log-probability 作为隐式 reward，去掉 reference model，并在 Bradley–Terry 目标中加入固定 margin。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>用长度归一化的 policy log-probability 直接作 reward，并用目标 margin 拉开偏好。核心 sequence normalization、reference-free reward 和 margin 已落到真实 token loss；未复刻 Mistral/Llama/Gemma 规模训练及 AlpacaEval judge。本地在自由生成 causal LM 上实现平均 token log-probability 和 margin，训练时不创建 reference model；用相同 warmup、数据、步数与 seed 和其他自由生成方法比较。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2405.14734">原论文</a> · <a href="../../../../post-training/2405.14734-simpo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="ORPO LLM 后训练 KAIST 2024-03-12 常见对齐流程先 SFT、再用 reference-relative 偏好目标训练。ORPO 把 chosen response 的 NLL 与 chosen/rejected 的 odds-ratio penalty 合成一个目标；概率接近 0 或 1 时，odds 会提供比普通概率差更敏感的对比信号。 本地把完整候选视为 response action，未训练论文中的 Mistral/Llama 模型，KL 只用于统一报告而不参与目标。ORPO 用一个模型同时完成监督学习与偏好拉开，不需要冻结 reference model。实现了 chosen SFT 与 odds-ratio preference penalty 的单阶段更新；本地把完整候选视为 response action，未训练论文中的 Mistral/Llama 模型，KL 只用于统一报告而不参与目标。最后一步 SFT NLL 为 0.0715、chosen/rejected log-odds margin 为 6.3502；  单阶段偏好 LLM 后训练 偏好与对齐：先看反馈长什么样">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<h2 id="paper-post-training-orpo-e4a32db7">ORPO</h2>
<p class="ar-learning-card__meta">KAIST · 论文公开：2024-03-12</p>
<p><strong>方法要点：</strong>常见对齐流程先 SFT、再用 reference-relative 偏好目标训练。ORPO 把 chosen response 的 NLL 与 chosen/rejected 的 odds-ratio penalty 合成一个目标；概率接近 0 或 1 时，odds 会提供比普通概率差更敏感的对比信号。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本地把完整候选视为 response action，未训练论文中的 Mistral/Llama 模型，KL 只用于统一报告而不参与目标。ORPO 用一个模型同时完成监督学习与偏好拉开，不需要冻结 reference model。实现了 chosen SFT 与 odds-ratio preference penalty 的单阶段更新；本地把完整候选视为 response action，未训练论文中的 Mistral/Llama 模型，KL 只用于统一报告而不参与目标。最后一步 SFT NLL 为 0.0715、chosen/rejected log-odds margin 为 6.3502；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2403.07691">原论文</a> · <a href="../../../../post-training/2403.07691-orpo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="KTO LLM 后训练 Contextual AI 2024-02-02 DPO 需要成对偏好，而生产反馈常只有点赞、点踩或是否接受。KTO 将单样本反馈映射为 desirable / undesirable utility，并用 policy 与 reference 的 KL 期望作为“参照点”；两类样本可独立采集，也允许类别不平衡。 KTO 只需要单条回答的“满意 / 不满意”标签，以 reference KL 为参照构造前景理论效用，不要求同一 prompt 的 chosen/rejected 偏好对。实现了单样本二元反馈、reference log-ratio、KL 移动参照点与两类 utility；本地 policy 是六候选线性策略，不是论文中的 1B–30B 自由生成 LLM，也未复刻人类偏好数据规模。最后一步 desirable / undesirable utility 为 0.5030 / 0.4972，KL EMA 为 0.0074。  二元反馈对齐 LLM 后训练 偏好与对齐：先看反馈长什么样">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<h2 id="paper-post-training-kto-edf0a49a">KTO</h2>
<p class="ar-learning-card__meta">Contextual AI · 论文公开：2024-02-02</p>
<p><strong>方法要点：</strong>DPO 需要成对偏好，而生产反馈常只有点赞、点踩或是否接受。KTO 将单样本反馈映射为 desirable / undesirable utility，并用 policy 与 reference 的 KL 期望作为“参照点”；两类样本可独立采集，也允许类别不平衡。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>KTO 只需要单条回答的“满意 / 不满意”标签，以 reference KL 为参照构造前景理论效用，不要求同一 prompt 的 chosen/rejected 偏好对。实现了单样本二元反馈、reference log-ratio、KL 移动参照点与两类 utility；本地 policy 是六候选线性策略，不是论文中的 1B–30B 自由生成 LLM，也未复刻人类偏好数据规模。最后一步 desirable / undesirable utility 为 0.5030 / 0.4972，KL EMA 为 0.0074。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2402.01306">原论文</a> · <a href="../../../../post-training/2402.01306-kto/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Self-Rewarding LM LLM 后训练 Meta AI 2024-01-18 每轮由当前模型生成候选并以 LLM-as-a-Judge 打分，形成新的偏好对继续 DPO，构成自举闭环。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.6250（+166.67%）；奖励、KL、长度和候选预算一致。  自奖励 LLM 后训练 偏好与对齐：先看反馈长什么样">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<h2 id="paper-post-training-self-rewarding-38dd38b1">Self-Rewarding LM</h2>
<p class="ar-learning-card__meta">Meta AI · 论文公开：2024-01-18</p>
<p><strong>方法要点：</strong>每轮由当前模型生成候选并以 LLM-as-a-Judge 打分，形成新的偏好对继续 DPO，构成自举闭环。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.6250（+166.67%）；奖励、KL、长度和候选预算一致。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2401.10020">原论文</a> · <a href="../../../../post-training/2401.10020-self-rewarding/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="SPIN LLM 后训练 University of California, Los Angeles 2024-01-02 额外偏好标注昂贵。SPIN 从 SFT 模型出发，用上一轮模型为训练 prompt 生成回答，把人类示范视作正例、自生成回答视作负例，通过自博弈判别目标得到下一轮模型，循环提升而不引入新的人工偏好数据。 本页复现“上一轮策略生成负例、人与自生成回答对比、定期刷新对手”的迭代状态，不把 candidate sampling 写成完整 LLM rollout。实现冻结对手、self-play sampling、reference-relative 偏好损失与轮次刷新；没有真实文本生成、分布式训练或论文模型规模。上一轮 candidate policy 负责采样负例，每 16 次更新刷新一次对手。  自博弈微调 LLM 后训练 偏好与对齐：先看反馈长什么样">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<h2 id="paper-post-training-spin-6b40abc1">SPIN</h2>
<p class="ar-learning-card__meta">University of California, Los Angeles · 论文公开：2024-01-02</p>
<p><strong>方法要点：</strong>额外偏好标注昂贵。SPIN 从 SFT 模型出发，用上一轮模型为训练 prompt 生成回答，把人类示范视作正例、自生成回答视作负例，通过自博弈判别目标得到下一轮模型，循环提升而不引入新的人工偏好数据。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本页复现“上一轮策略生成负例、人与自生成回答对比、定期刷新对手”的迭代状态，不把 candidate sampling 写成完整 LLM rollout。实现冻结对手、self-play sampling、reference-relative 偏好损失与轮次刷新；没有真实文本生成、分布式训练或论文模型规模。上一轮 candidate policy 负责采样负例，每 16 次更新刷新一次对手。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2401.01335">原论文</a> · <a href="../../../../post-training/2401.01335-spin/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="IPO LLM 后训练 Google DeepMind 2023-10-18 论文指出 RLHF 与 DPO 都依赖将成对偏好转成标量 reward 的假设，并提出直接在偏好概率上优化的 PO 框架。取恒等映射得到 IPO：拟合一个有限的目标间隔，而不是像 logistic loss 一样在训练集可分时持续放大 chosen/rejected 间隔。 用平方回归约束偏好 log-ratio，避免 DPO 在可分数据上把策略推向确定性极端。保留了 tokenizer 级序列概率、自由生成、reference policy 与 IPO 平方目标；本地模型和算术数据用于验证训练机制，不等同于论文的大模型偏好评测。本地用字符 tokenizer、GRU causal LM 和自由生成 numeric verifier。SFT warmup 后，正确 completion 为 chosen，当前 policy rollout 中最低 reward 响应为 rejected，按 token log-probability 实现 reference-relative IPO。  偏好正则 LLM 后训练 偏好与对齐：先看反馈长什么样">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<h2 id="paper-post-training-ipo-127b83ec">IPO</h2>
<p class="ar-learning-card__meta">Google DeepMind · 论文公开：2023-10-18</p>
<p><strong>方法要点：</strong>论文指出 RLHF 与 DPO 都依赖将成对偏好转成标量 reward 的假设，并提出直接在偏好概率上优化的 PO 框架。取恒等映射得到 IPO：拟合一个有限的目标间隔，而不是像 logistic loss 一样在训练集可分时持续放大 chosen/rejected 间隔。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>用平方回归约束偏好 log-ratio，避免 DPO 在可分数据上把策略推向确定性极端。保留了 tokenizer 级序列概率、自由生成、reference policy 与 IPO 平方目标；本地模型和算术数据用于验证训练机制，不等同于论文的大模型偏好评测。本地用字符 tokenizer、GRU causal LM 和自由生成 numeric verifier。SFT warmup 后，正确 completion 为 chosen，当前 policy rollout 中最低 reward 响应为 rejected，按 token log-probability 实现 reference-relative IPO。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2310.12036">原论文</a> · <a href="../../../../post-training/2310.12036-ipo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="SteerLM LLM 后训练 NVIDIA 2023-10-09 传统 RLHF 把多维偏好压成一个 reward，用户推理时也不能改变目标。SteerLM 先用 attribute prediction model 为回答标注 helpfulness、quality 等属性，再把属性和值拼入条件做普通 SFT，推理时由用户指定目标属性。 本页复现显式属性标注、目标属性条件选择与 SFT 更新，不把四维本地属性冒充 NVIDIA 43B 模型。保留多维 annotation 与条件 SFT；本地属性来自公开候选数据的确定性 reward axes，没有训练大属性预测器，也未实现真实文本 token 级条件生成。四个 reward axis 作为可审计属性标注，目标属性向量参与响应选择，再执行条件 SFT。  多属性可控 SFT LLM 后训练 偏好与对齐：先看反馈长什么样">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<h2 id="paper-post-training-steerlm-863fe2af">SteerLM</h2>
<p class="ar-learning-card__meta">NVIDIA · 论文公开：2023-10-09</p>
<p><strong>方法要点：</strong>传统 RLHF 把多维偏好压成一个 reward，用户推理时也不能改变目标。SteerLM 先用 attribute prediction model 为回答标注 helpfulness、quality 等属性，再把属性和值拼入条件做普通 SFT，推理时由用户指定目标属性。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本页复现显式属性标注、目标属性条件选择与 SFT 更新，不把四维本地属性冒充 NVIDIA 43B 模型。保留多维 annotation 与条件 SFT；本地属性来自公开候选数据的确定性 reward axes，没有训练大属性预测器，也未实现真实文本 token 级条件生成。四个 reward axis 作为可审计属性标注，目标属性向量参与响应选择，再执行条件 SFT。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2310.05344">原论文</a> · <a href="../../../../post-training/2310.05344-steerlm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="RLAIF LLM 后训练 Google Research 2023-09-01 AI labeler 对候选做顺序交换评判，去除位置偏差后训练 preference policy；本地落实双顺序标签与成对更新。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.6406（+173.33%）；奖励、KL、长度和候选预算一致。  AI 反馈 LLM 后训练 偏好与对齐：先看反馈长什么样">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<h2 id="paper-post-training-rlaif-a542b4bc">RLAIF</h2>
<p class="ar-learning-card__meta">Google Research · 论文公开：2023-09-01</p>
<p><strong>方法要点：</strong>AI labeler 对候选做顺序交换评判，去除位置偏差后训练 preference policy；本地落实双顺序标签与成对更新。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.6406（+173.33%）；奖励、KL、长度和候选预算一致。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2309.00267">原论文</a> · <a href="../../../../post-training/2309.00267-rlaif/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="DPO LLM 后训练 Stanford University 2023-05-29 传统 RLHF 先拟合 reward model，再用 PPO 优化策略，链路复杂且不稳定。DPO 从 KL-regularized RLHF 的最优策略形式出发，把隐式 reward 写成 policy 与 reference log-ratio，最终只需在偏好对上做二分类。 本页实现 chosen/rejected 相对 reference policy 的闭式偏好分类目标，不训练显式 reward model，也不进行在线 rollout。实现 DPO 的 reference-relative pairwise loss 与偏好 margin；候选策略可以精确计算整项概率，但没有训练自回归 LLM，也没有复刻 Anthropic HH 或 TL;DR 偏好数据。统一 GSM8K candidate 协议下，每题以 gold candidate 为 chosen、当前最高分错误项为 rejected，并记录 reference-corrected preference margin。  直接偏好优化 LLM 后训练 偏好与对齐：先看反馈长什么样">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<h2 id="paper-post-training-dpo-0073c0b6">DPO</h2>
<p class="ar-learning-card__meta">Stanford University · 论文公开：2023-05-29</p>
<p><strong>方法要点：</strong>传统 RLHF 先拟合 reward model，再用 PPO 优化策略，链路复杂且不稳定。DPO 从 KL-regularized RLHF 的最优策略形式出发，把隐式 reward 写成 policy 与 reference log-ratio，最终只需在偏好对上做二分类。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本页实现 chosen/rejected 相对 reference policy 的闭式偏好分类目标，不训练显式 reward model，也不进行在线 rollout。实现 DPO 的 reference-relative pairwise loss 与偏好 margin；候选策略可以精确计算整项概率，但没有训练自回归 LLM，也没有复刻 Anthropic HH 或 TL;DR 偏好数据。统一 GSM8K candidate 协议下，每题以 gold candidate 为 chosen、当前最高分错误项为 rejected，并记录 reference-corrected preference margin。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.18290">原论文</a> · <a href="../../../../post-training/2305.18290-dpo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="SLiC-HF LLM 后训练 Google DeepMind 2023-05-17 PPO-RLHF 需要策略、reward 和 value 等多套模型。SLiC-HF 直接要求偏好回答的序列 log-likelihood 高于拒绝回答，并用监督目标限制策略漂移；也能消费为其他模型采集的 off-policy 偏好数据。 GSM8K candidate 512/128、300 steps、seed 42，共享同一未训练策略基线。本页复现“偏好序列 margin 校准 + SFT 正则”目标，不把 candidate policy 写成原论文的 T5-XXL 实验。实现 sequence margin、off-policy preference 标记和参考分布正则；候选项代表完整回答，未训练 T5、独立 ranker，也未复刻 TL;DR 人评。  序列概率校准 LLM 后训练 偏好与对齐：先看反馈长什么样">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<h2 id="paper-post-training-slic-hf-5def3201">SLiC-HF</h2>
<p class="ar-learning-card__meta">Google DeepMind · 论文公开：2023-05-17</p>
<p><strong>方法要点：</strong>PPO-RLHF 需要策略、reward 和 value 等多套模型。SLiC-HF 直接要求偏好回答的序列 log-likelihood 高于拒绝回答，并用监督目标限制策略漂移；也能消费为其他模型采集的 off-policy 偏好数据。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>GSM8K candidate 512/128、300 steps、seed 42，共享同一未训练策略基线。本页复现“偏好序列 margin 校准 + SFT 正则”目标，不把 candidate policy 写成原论文的 T5-XXL 实验。实现 sequence margin、off-policy preference 标记和参考分布正则；候选项代表完整回答，未训练 T5、独立 ranker，也未复刻 TL;DR 人评。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.10425">原论文</a> · <a href="../../../../post-training/2305.10425-slic-hf/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="RRHF LLM 后训练 Alibaba DAMO Academy 2023-04-11 PPO-RLHF 需要 policy、old policy、reward 和 value 等多模型协同，训练和调参复杂。RRHF 从多个模型或人工答案中采样响应，以 reward 给出完整排序，让模型自身的平均 log-likelihood 顺序与 reward 顺序一致，并对最高质量响应继续做 SFT。 本页实现全候选 reward ordering、response log-probability ranking loss 与 best-response SFT，不把它简化成单个 chosen/rejected 的 DPO。保留全排序 hinge 与 best-response SFT；候选 log-probability 是可审计策略概率，没有训练 7B LLaMA，也没有复刻 HH 数据生成、外部 reward model 或人工评价。公开 GSM8K candidate 512/128、300 steps、seed 42；每组 6 个响应均进入 reward 排序和违序 pair 统计。  全排序偏好 LLM 后训练 偏好与对齐：先看反馈长什么样">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<h2 id="paper-post-training-rrhf-c28f5ad3">RRHF</h2>
<p class="ar-learning-card__meta">Alibaba DAMO Academy · 论文公开：2023-04-11</p>
<p><strong>方法要点：</strong>PPO-RLHF 需要 policy、old policy、reward 和 value 等多模型协同，训练和调参复杂。RRHF 从多个模型或人工答案中采样响应，以 reward 给出完整排序，让模型自身的平均 log-likelihood 顺序与 reward 顺序一致，并对最高质量响应继续做 SFT。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本页实现全候选 reward ordering、response log-probability ranking loss 与 best-response SFT，不把它简化成单个 chosen/rejected 的 DPO。保留全排序 hinge 与 best-response SFT；候选 log-probability 是可审计策略概率，没有训练 7B LLaMA，也没有复刻 HH 数据生成、外部 reward model 或人工评价。公开 GSM8K candidate 512/128、300 steps、seed 42；每组 6 个响应均进入 reward 排序和违序 pair 统计。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2304.05302">原论文</a> · <a href="../../../../post-training/2304.05302-rrhf/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Constitutional AI LLM 后训练 Anthropic 2022-12-15 人工逐条标注有害回答成本高，而且价值规范不透明。论文把人类监督压缩成一组自然语言原则：第一阶段让模型依据原则批评并重写自己的回答，再对修订回答做 SFT；第二阶段让 AI 比较回答、训练 preference model，并以该奖励执行 RLAIF。 GSM8K 的原则维度是正确性、格式、过程和简洁性，不是安全红队数据，也未训练独立 preference model 或执行大模型 PPO。本页复现“自我批评与修订 → 修订样本 SFT → AI 偏好 RLAIF”两阶段机制；本地 candidate policy 不冒充 Anthropic 原始大模型安全训练。实现显式原则打分、自我修订 SFT 和 AI preference ranking 的状态更新；GSM8K 的原则维度是正确性、格式、过程和简洁性，不是安全红队数据，也未训练独立 preference model 或执行大模型 PPO。  AI 反馈安全对齐 LLM 后训练 偏好与对齐：先看反馈长什么样">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<h2 id="paper-post-training-constitutional-ai-8d3916b0">Constitutional AI</h2>
<p class="ar-learning-card__meta">Anthropic · 论文公开：2022-12-15</p>
<p><strong>方法要点：</strong>人工逐条标注有害回答成本高，而且价值规范不透明。论文把人类监督压缩成一组自然语言原则：第一阶段让模型依据原则批评并重写自己的回答，再对修订回答做 SFT；第二阶段让 AI 比较回答、训练 preference model，并以该奖励执行 RLAIF。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>GSM8K 的原则维度是正确性、格式、过程和简洁性，不是安全红队数据，也未训练独立 preference model 或执行大模型 PPO。本页复现“自我批评与修订 → 修订样本 SFT → AI 偏好 RLAIF”两阶段机制；本地 candidate policy 不冒充 Anthropic 原始大模型安全训练。实现显式原则打分、自我修订 SFT 和 AI preference ranking 的状态更新；GSM8K 的原则维度是正确性、格式、过程和简洁性，不是安全红队数据，也未训练独立 preference model 或执行大模型 PPO。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2212.08073">原论文</a> · <a href="../../../../post-training/2212.08073-constitutional-ai/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
