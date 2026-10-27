---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 偏好与对齐：先看反馈长什么样

[LLM 后训练](index.md) / 100 个问题 · 25 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

[阅读本主题精读卡片：多篇论文对比、分析与问答](../../deep-dives/post-training/preference-and-alignment.md)

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
<p class="ar-learning-status" data-learning-status role="status">100 个问题 · 25 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:clean-rm" data-paper-title="CleanRM: Reward Modeling from Noisy Feedback with a Few Clean Feedback for RLHF" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="CleanRM: Reward Modeling from Noisy Feedback with a Few Clean Feedback for RLHF LLM 后训练 Zhejiang University 2026-10-15 不同偏好样本的标注噪声不一定相同。CleanRM 用少量干净反馈校准两个方向的样本级噪声率；以语义与恢复偏好的联合分布作最优传输，而不是只匹配偏好直方图。随后固定估计器，用去偏 surrogate 训练 RM。 完整 RM/RLHF 实验成本过高，不复现（审查 DONE）。L1 小特征、真实 joint OT 与 signed corrected loss 组件。不用预知噪声率代替核心估计器；不把合成机制结果称为真实 RLHF 安全能力。完整 RM/RLHF 实验成本过高，不复现（审查 DONE）。NoiseEstimator 通过三路 softmax 保证两向噪声率非负、总和至多 .95。noise_estimation_loss 只读取 noisy features/观察反馈以及独立 clean calibration 子集，不接收已知真实噪声率。编码特征在组件中视为固定，未下载原文 LLM backbone。  二元反馈对齐 后训练算法组件 CleanRM LLM 后训练 偏好与对齐：先看反馈长什么样 CleanRM为什么区分两种偏好翻转噪声，而不只估一个总体错误率？ 真实正偏好被标成负例，与真实负偏好被标成正例，可能由不同原因产生。分开估计两种条件噪声率，才能对观察标签对应的风险分别校正；总体错误率会掩盖这种不对称。 例如标注者偏爱长回答，正确短答被误拒与错误长答被误选的频率可以不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<span id="paper-post-training-clean-rm-81560dec" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4ff1ba1637aad6e3">CleanRM为什么区分两种偏好翻转噪声，而不只估一个总体错误率？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aclean-rm">CleanRM: Reward Modeling from Noisy Feedback with a Few Clean Feedback for RLHF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>真实正偏好被标成负例，与真实负偏好被标成正例，可能由不同原因产生。分开估计两种条件噪声率，才能对观察标签对应的风险分别校正；总体错误率会掩盖这种不对称。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如标注者偏爱长回答，正确短答被误拒与错误长答被误选的频率可以不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21138v1">原论文</a> · <a href="../../../../post-training/2610.21138-clean-rm/">实现解读</a> · <a href="#qa-4ff1ba1637aad6e3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:clean-rm" data-paper-title="CleanRM: Reward Modeling from Noisy Feedback with a Few Clean Feedback for RLHF" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="CleanRM: Reward Modeling from Noisy Feedback with a Few Clean Feedback for RLHF LLM 后训练 Zhejiang University 2026-10-15 不同偏好样本的标注噪声不一定相同。CleanRM 用少量干净反馈校准两个方向的样本级噪声率；以语义与恢复偏好的联合分布作最优传输，而不是只匹配偏好直方图。随后固定估计器，用去偏 surrogate 训练 RM。 完整 RM/RLHF 实验成本过高，不复现（审查 DONE）。L1 小特征、真实 joint OT 与 signed corrected loss 组件。不用预知噪声率代替核心估计器；不把合成机制结果称为真实 RLHF 安全能力。完整 RM/RLHF 实验成本过高，不复现（审查 DONE）。NoiseEstimator 通过三路 softmax 保证两向噪声率非负、总和至多 .95。noise_estimation_loss 只读取 noisy features/观察反馈以及独立 clean calibration 子集，不接收已知真实噪声率。编码特征在组件中视为固定，未下载原文 LLM backbone。  二元反馈对齐 后训练算法组件 CleanRM LLM 后训练 偏好与对齐：先看反馈长什么样 CleanRM为什么同时匹配语义与恢复偏好，校正损失为负时能截成零吗？ 只匹配偏好比例会把语义不同的样本错误对齐，联合最优传输同时利用表示距离和恢复偏好来估计双向噪声。随后固定估计器校正风险，带符号损失可以合法为负；截断会改变期望，不能再沿用无偏解释，而噪声率估错也会破坏保证。 教学例子：两类问题都有一半赞同标签，但一类经常被误标。仅对齐标签比例看不出差别，需要结合问题表示识别噪声。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-5aea70a8fd94cd32">CleanRM为什么同时匹配语义与恢复偏好，校正损失为负时能截成零吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aclean-rm">CleanRM: Reward Modeling from Noisy Feedback with a Few Clean Feedback for RLHF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只匹配偏好比例会把语义不同的样本错误对齐，联合最优传输同时利用表示距离和恢复偏好来估计双向噪声。随后固定估计器校正风险，带符号损失可以合法为负；截断会改变期望，不能再沿用无偏解释，而噪声率估错也会破坏保证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两类问题都有一半赞同标签，但一类经常被误标。仅对齐标签比例看不出差别，需要结合问题表示识别噪声。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21138v1">原论文</a> · <a href="../../../../post-training/2610.21138-clean-rm/">实现解读</a> · <a href="#qa-5aea70a8fd94cd32">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:clean-rm" data-paper-title="CleanRM: Reward Modeling from Noisy Feedback with a Few Clean Feedback for RLHF" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="CleanRM: Reward Modeling from Noisy Feedback with a Few Clean Feedback for RLHF LLM 后训练 Zhejiang University 2026-10-15 不同偏好样本的标注噪声不一定相同。CleanRM 用少量干净反馈校准两个方向的样本级噪声率；以语义与恢复偏好的联合分布作最优传输，而不是只匹配偏好直方图。随后固定估计器，用去偏 surrogate 训练 RM。 完整 RM/RLHF 实验成本过高，不复现（审查 DONE）。L1 小特征、真实 joint OT 与 signed corrected loss 组件。不用预知噪声率代替核心估计器；不把合成机制结果称为真实 RLHF 安全能力。完整 RM/RLHF 实验成本过高，不复现（审查 DONE）。NoiseEstimator 通过三路 softmax 保证两向噪声率非负、总和至多 .95。noise_estimation_loss 只读取 noisy features/观察反馈以及独立 clean calibration 子集，不接收已知真实噪声率。编码特征在组件中视为固定，未下载原文 LLM backbone。  二元反馈对齐 后训练算法组件 CleanRM LLM 后训练 偏好与对齐：先看反馈长什么样 CleanRM把噪声估计器冻结后训练RM，与两者一起追着当前损失更新有何区别？ 冻结后，奖励模型优化的是由一套既定噪声率定义的校正风险；若估计器同时随RM损失变化，校正系数也会移动，RM可能通过改变噪声解释降低损失。联合训练属于另一个优化问题，不能直接继承固定噪声估计下的风险校正解释。 教学例子：先估某类标签翻转率再训练RM；不能因为RM暂时分错，就把这条样本重新解释成更高噪声。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b0ba45f5b5fa7573">CleanRM把噪声估计器冻结后训练RM，与两者一起追着当前损失更新有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aclean-rm">CleanRM: Reward Modeling from Noisy Feedback with a Few Clean Feedback for RLHF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冻结后，奖励模型优化的是由一套既定噪声率定义的校正风险；若估计器同时随RM损失变化，校正系数也会移动，RM可能通过改变噪声解释降低损失。联合训练属于另一个优化问题，不能直接继承固定噪声估计下的风险校正解释。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先估某类标签翻转率再训练RM；不能因为RM暂时分错，就把这条样本重新解释成更高噪声。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21138v1">原论文</a> · <a href="../../../../post-training/2610.21138-clean-rm/">实现解读</a> · <a href="#qa-b0ba45f5b5fa7573">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:clean-rm" data-paper-title="CleanRM: Reward Modeling from Noisy Feedback with a Few Clean Feedback for RLHF" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="CleanRM: Reward Modeling from Noisy Feedback with a Few Clean Feedback for RLHF LLM 后训练 Zhejiang University 2026-10-15 不同偏好样本的标注噪声不一定相同。CleanRM 用少量干净反馈校准两个方向的样本级噪声率；以语义与恢复偏好的联合分布作最优传输，而不是只匹配偏好直方图。随后固定估计器，用去偏 surrogate 训练 RM。 完整 RM/RLHF 实验成本过高，不复现（审查 DONE）。L1 小特征、真实 joint OT 与 signed corrected loss 组件。不用预知噪声率代替核心估计器；不把合成机制结果称为真实 RLHF 安全能力。完整 RM/RLHF 实验成本过高，不复现（审查 DONE）。NoiseEstimator 通过三路 softmax 保证两向噪声率非负、总和至多 .95。noise_estimation_loss 只读取 noisy features/观察反馈以及独立 clean calibration 子集，不接收已知真实噪声率。编码特征在组件中视为固定，未下载原文 LLM backbone。  二元反馈对齐 后训练算法组件 CleanRM LLM 后训练 偏好与对齐：先看反馈长什么样 CleanRM的恢复标签或校正损失越出常见范围时应直接裁剪吗？ 不能。恢复偏好可能超出零到一，校正风险也是可为负的带符号量；强行裁剪会改变去偏目标。还需保证两噪声率之和小于一，并在奖励模型更新时冻结估计器。 例如一次校正得到负损失，只要公式条件成立，就不能为让曲线好看而改成零。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-4642fc40ad22ddae">CleanRM的恢复标签或校正损失越出常见范围时应直接裁剪吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aclean-rm">CleanRM: Reward Modeling from Noisy Feedback with a Few Clean Feedback for RLHF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。恢复偏好可能超出零到一，校正风险也是可为负的带符号量；强行裁剪会改变去偏目标。还需保证两噪声率之和小于一，并在奖励模型更新时冻结估计器。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一次校正得到负损失，只要公式条件成立，就不能为让曲线好看而改成零。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21138v1">原论文</a> · <a href="../../../../post-training/2610.21138-clean-rm/">实现解读</a> · <a href="#qa-4642fc40ad22ddae">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gaw-po" data-paper-title="GAW-PO: Preference Optimization with Gradient-Aligned Token Weights" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="GAW-PO: Preference Optimization with Gradient-Aligned Token Weights LLM 后训练 National University of Science and Technology POLITEHNICA Bucharest 2026-10-01 用拒绝 token 梯度与 preferred update direction 的对齐度调节负权重；越支持优选行为的 token 越少受罚。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行梯度对齐权重；未进行 LoRA/DPO 训练。执行梯度对齐权重；未进行 LoRA/DPO 训练。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  偏好优化 token credit DPO LLM 后训练 偏好与对齐：先看反馈长什么样 GAW-PO里的preferred与rejected是整条回答标签，还是每个词元的好坏标注？ 它们是同一提示下两条回答的相对偏好标签，并没有逐词标注。被拒回答仍可能含有正确步骤或共享措辞。因此输入的监督粒度与实际调整的词元粒度不同；梯度对齐是补充的信用分配信号，不能被解释成新增的人类逐词真值。 教学例子：两份解答都先写出正确公式，只在最后计算不同；整条拒绝标签并未把公共公式标成错误。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<span id="paper-post-training-gaw-po-bf9dde22" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7bb97a727465c23f">GAW-PO里的preferred与rejected是整条回答标签，还是每个词元的好坏标注？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agaw-po">GAW-PO: Preference Optimization with Gradient-Aligned Token Weights</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Science and Technology POLITEHNICA Bucharest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它们是同一提示下两条回答的相对偏好标签，并没有逐词标注。被拒回答仍可能含有正确步骤或共享措辞。因此输入的监督粒度与实际调整的词元粒度不同；梯度对齐是补充的信用分配信号，不能被解释成新增的人类逐词真值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两份解答都先写出正确公式，只在最后计算不同；整条拒绝标签并未把公共公式标成错误。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01511">原论文</a> · <a href="../../../../post-training/2610.01511-gaw-po/">实现解读</a> · <a href="#qa-7bb97a727465c23f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gaw-po" data-paper-title="GAW-PO: Preference Optimization with Gradient-Aligned Token Weights" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="GAW-PO: Preference Optimization with Gradient-Aligned Token Weights LLM 后训练 National University of Science and Technology POLITEHNICA Bucharest 2026-10-01 用拒绝 token 梯度与 preferred update direction 的对齐度调节负权重；越支持优选行为的 token 越少受罚。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行梯度对齐权重；未进行 LoRA/DPO 训练。执行梯度对齐权重；未进行 LoRA/DPO 训练。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  偏好优化 token credit DPO LLM 后训练 偏好与对齐：先看反馈长什么样 被拒回答中的token如果支持优选方向，GAW-PO为什么反而少罚它？ 拒绝整条回答不代表其中每个token都坏。GAW-PO比较该token梯度与优选更新方向的夹角，对齐越强，负权重越小，从而减少把共享有用成分一并压低的冲突。它调整的是拒绝项信用，不把梯度相似度当成token事实正确性的证明。 教学例子：两份回答开头都正确，拒绝回答只在结论出错。若正确开头支持优选方向，就不应与错误结论同样强地受罚。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-0307c820f34c8286">被拒回答中的token如果支持优选方向，GAW-PO为什么反而少罚它？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agaw-po">GAW-PO: Preference Optimization with Gradient-Aligned Token Weights</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Science and Technology POLITEHNICA Bucharest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>拒绝整条回答不代表其中每个token都坏。GAW-PO比较该token梯度与优选更新方向的夹角，对齐越强，负权重越小，从而减少把共享有用成分一并压低的冲突。它调整的是拒绝项信用，不把梯度相似度当成token事实正确性的证明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两份回答开头都正确，拒绝回答只在结论出错。若正确开头支持优选方向，就不应与错误结论同样强地受罚。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01511">原论文</a> · <a href="../../../../post-training/2610.01511-gaw-po/">实现解读</a> · <a href="#qa-0307c820f34c8286">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gaw-po" data-paper-title="GAW-PO: Preference Optimization with Gradient-Aligned Token Weights" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="GAW-PO: Preference Optimization with Gradient-Aligned Token Weights LLM 后训练 National University of Science and Technology POLITEHNICA Bucharest 2026-10-01 用拒绝 token 梯度与 preferred update direction 的对齐度调节负权重；越支持优选行为的 token 越少受罚。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行梯度对齐权重；未进行 LoRA/DPO 训练。执行梯度对齐权重；未进行 LoRA/DPO 训练。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  偏好优化 token credit DPO LLM 后训练 偏好与对齐：先看反馈长什么样 GAW-PO的梯度对齐与按词元概率高低加权有何不同？ 概率描述当前模型有多常生成某词，对齐度描述惩罚它会否妨碍优选方向。二者不等价：常见词可能无关，罕见词也可能支持优选更新；这里只比较机制，不推断效果胜负。 例如一个低频术语恰好支撑正确解释，不能只因概率低就加重负向惩罚。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-013be2268305c60d">GAW-PO的梯度对齐与按词元概率高低加权有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agaw-po">GAW-PO: Preference Optimization with Gradient-Aligned Token Weights</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Science and Technology POLITEHNICA Bucharest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>概率描述当前模型有多常生成某词，对齐度描述惩罚它会否妨碍优选方向。二者不等价：常见词可能无关，罕见词也可能支持优选更新；这里只比较机制，不推断效果胜负。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个低频术语恰好支撑正确解释，不能只因概率低就加重负向惩罚。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01511">原论文</a> · <a href="../../../../post-training/2610.01511-gaw-po/">实现解读</a> · <a href="#qa-013be2268305c60d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gaw-po" data-paper-title="GAW-PO: Preference Optimization with Gradient-Aligned Token Weights" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="GAW-PO: Preference Optimization with Gradient-Aligned Token Weights LLM 后训练 National University of Science and Technology POLITEHNICA Bucharest 2026-10-01 用拒绝 token 梯度与 preferred update direction 的对齐度调节负权重；越支持优选行为的 token 越少受罚。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行梯度对齐权重；未进行 LoRA/DPO 训练。执行梯度对齐权重；未进行 LoRA/DPO 训练。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  偏好优化 token credit DPO LLM 后训练 偏好与对齐：先看反馈长什么样 GAW-PO权重中正部余弦会怎样处理同向、正交与反向梯度？ 权重是一减正部余弦：完全同向时趋于零，正交或反向时保持一，中间正对齐则部分减罚。需要真实梯度方向；本地只验证该权重核，未完成语言模型偏好训练。 例如余弦为负并不会得到大于一的惩罚权重，正部操作先把它变成零。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-92390bc26a92b79e">GAW-PO权重中正部余弦会怎样处理同向、正交与反向梯度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agaw-po">GAW-PO: Preference Optimization with Gradient-Aligned Token Weights</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Science and Technology POLITEHNICA Bucharest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>权重是一减正部余弦：完全同向时趋于零，正交或反向时保持一，中间正对齐则部分减罚。需要真实梯度方向；本地只验证该权重核，未完成语言模型偏好训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如余弦为负并不会得到大于一的惩罚权重，正部操作先把它变成零。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01511">原论文</a> · <a href="../../../../post-training/2610.01511-gaw-po/">实现解读</a> · <a href="#qa-92390bc26a92b79e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:compo" data-paper-title="A Zeroth-Order Paradigm for LLM Preference Alignment" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="A Zeroth-Order Paradigm for LLM Preference Alignment LLM 后训练 University of California, Berkeley 2026-09-16 不求偏好目标梯度，只比较正负参数扰动的结果得到一比特方向，再以逐坐标阈值抑制噪声。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行一比特比较 oracle 与阈值化更新；mini-suite 不是大模型对齐结果。本地执行一比特比较 oracle 与阈值化更新；mini-suite 不是大模型对齐结果。  偏好优化 零阶优化 LLM 后训练 偏好与对齐：先看反馈长什么样 COMPO所说的黑盒优化，是只改提示词而不改模型参数吗？ 不是。黑盒指优化器不需要取得偏好目标的反向梯度，更新对象仍是模型参数。它能在参数附近提出扰动、调用目标比较接口，再产生下一参数点。只有一个只能接收提示词、不能部署参数扰动的远程接口，并不自动满足这个访问条件。 教学例子：能装载两份轻微改动的权重并比较结果，才有参数扰动接口；只修改聊天提示是另一种搜索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<span id="paper-post-training-compo-257a1fd8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-65f82773739e80be">COMPO所说的黑盒优化，是只改提示词而不改模型参数吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acompo">A Zeroth-Order Paradigm for LLM Preference Alignment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。黑盒指优化器不需要取得偏好目标的反向梯度，更新对象仍是模型参数。它能在参数附近提出扰动、调用目标比较接口，再产生下一参数点。只有一个只能接收提示词、不能部署参数扰动的远程接口，并不自动满足这个访问条件。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>能装载两份轻微改动的权重并比较结果，才有参数扰动接口；只修改聊天提示是另一种搜索。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.19144">原论文</a> · <a href="../../../../post-training/2609.19144-compo/">实现解读</a> · <a href="#qa-65f82773739e80be">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:compo" data-paper-title="A Zeroth-Order Paradigm for LLM Preference Alignment" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="A Zeroth-Order Paradigm for LLM Preference Alignment LLM 后训练 University of California, Berkeley 2026-09-16 不求偏好目标梯度，只比较正负参数扰动的结果得到一比特方向，再以逐坐标阈值抑制噪声。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行一比特比较 oracle 与阈值化更新；mini-suite 不是大模型对齐结果。本地执行一比特比较 oracle 与阈值化更新；mini-suite 不是大模型对齐结果。  偏好优化 零阶优化 LLM 后训练 偏好与对齐：先看反馈长什么样 COMPO只比较正负参数扰动，怎样得到更新方向，为什么还需要坐标阈值？ 正负扰动在同一偏好目标上的优劣提供方向符号，无需显式反向求导也能提出参数更新。一比特比较的信息较粗，噪声可能让少数坐标被误更新，因此逐坐标阈值用来抑制不可靠分量。这仍需要目标评估，不等于没有采样或评估成本。 教学例子：沿某个随机方向分别轻推和回退参数，比较哪边更符合固定偏好；差异不可靠的坐标先保持原样，而非全部跟随。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8e824d210b2c1f79">COMPO只比较正负参数扰动，怎样得到更新方向，为什么还需要坐标阈值？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acompo">A Zeroth-Order Paradigm for LLM Preference Alignment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>正负扰动在同一偏好目标上的优劣提供方向符号，无需显式反向求导也能提出参数更新。一比特比较的信息较粗，噪声可能让少数坐标被误更新，因此逐坐标阈值用来抑制不可靠分量。这仍需要目标评估，不等于没有采样或评估成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>沿某个随机方向分别轻推和回退参数，比较哪边更符合固定偏好；差异不可靠的坐标先保持原样，而非全部跟随。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.19144">原论文</a> · <a href="../../../../post-training/2609.19144-compo/">实现解读</a> · <a href="#qa-8e824d210b2c1f79">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:compo" data-paper-title="A Zeroth-Order Paradigm for LLM Preference Alignment" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="A Zeroth-Order Paradigm for LLM Preference Alignment LLM 后训练 University of California, Berkeley 2026-09-16 不求偏好目标梯度，只比较正负参数扰动的结果得到一比特方向，再以逐坐标阈值抑制噪声。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行一比特比较 oracle 与阈值化更新；mini-suite 不是大模型对齐结果。本地执行一比特比较 oracle 与阈值化更新；mini-suite 不是大模型对齐结果。  偏好优化 零阶优化 LLM 后训练 偏好与对齐：先看反馈长什么样 COMPO的零阶比较与一阶反向传播分别需要什么信息？ 一阶方法需要目标对参数可微并可反传，零阶比较只需能评估扰动后的优劣。后者仍要付出多次目标评估，而且比较噪声会影响方向，不能把免反传等同免费或更准确。 例如外部偏好裁判只能给两模型排序，也可提供比较信号，却不能直接返回每层梯度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-76db661a1119217d">COMPO的零阶比较与一阶反向传播分别需要什么信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acompo">A Zeroth-Order Paradigm for LLM Preference Alignment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一阶方法需要目标对参数可微并可反传，零阶比较只需能评估扰动后的优劣。后者仍要付出多次目标评估，而且比较噪声会影响方向，不能把免反传等同免费或更准确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如外部偏好裁判只能给两模型排序，也可提供比较信号，却不能直接返回每层梯度。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.19144">原论文</a> · <a href="../../../../post-training/2609.19144-compo/">实现解读</a> · <a href="#qa-76db661a1119217d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:compo" data-paper-title="A Zeroth-Order Paradigm for LLM Preference Alignment" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="A Zeroth-Order Paradigm for LLM Preference Alignment LLM 后训练 University of California, Berkeley 2026-09-16 不求偏好目标梯度，只比较正负参数扰动的结果得到一比特方向，再以逐坐标阈值抑制噪声。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行一比特比较 oracle 与阈值化更新；mini-suite 不是大模型对齐结果。本地执行一比特比较 oracle 与阈值化更新；mini-suite 不是大模型对齐结果。  偏好优化 零阶优化 LLM 后训练 偏好与对齐：先看反馈长什么样 COMPO为什么在一比特更新后还要逐坐标阈值化？ 单次比较信息粗糙，方向估计中的弱坐标可能主要反映噪声。阈值用于抑制这些分量，代价是也可能丢掉小而真实的信号；本地只执行比较oracle和阈值核，未证明大模型对齐收益。 例如某坐标多次估计都接近零，可先抑制；不能把所有小值都解释为无用参数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-318c54c96ba1d744">COMPO为什么在一比特更新后还要逐坐标阈值化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acompo">A Zeroth-Order Paradigm for LLM Preference Alignment</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单次比较信息粗糙，方向估计中的弱坐标可能主要反映噪声。阈值用于抑制这些分量，代价是也可能丢掉小而真实的信号；本地只执行比较oracle和阈值核，未证明大模型对齐收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某坐标多次估计都接近零，可先抑制；不能把所有小值都解释为无用参数。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.19144">原论文</a> · <a href="../../../../post-training/2609.19144-compo/">实现解读</a> · <a href="#qa-318c54c96ba1d744">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sd-dpo" data-paper-title="Style-Debiased DPO: Updating LLM Knowledge with Factuality-Aware Synthetic Preference Data" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Style-Debiased DPO: Updating LLM Knowledge with Factuality-Aware Synthetic Preference Data LLM 后训练 Waseda University 2026-09-15 识别事实正确但风格不同的 rejected response，反转其偏好方向并按组比例加权以抵消风格梯度。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行偏好反转和组平衡损失；事实分数由 fixture 提供，不冒充 judge LLM。本地执行偏好反转和组平衡损失；事实分数由 fixture 提供，不冒充 judge LLM。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  偏好优化 知识更新 LLM 后训练 偏好与对齐：先看反馈长什么样 Style-Debiased DPO想更新的是知识，还是让模型统一采用某种文风？ 它的任务是利用合成偏好更新知识，风格差异是需要排除的混杂因素。喜欢简洁或华丽表达，不能直接充当事实对错标签。先把知识正确性与表达形式分清，才能理解后续为何需要事实判断和组平衡，而不是把它当成风格个性化训练。 教学例子：同一新知识可以用短句或长段表达；目标是两种表达都保留正确知识，而非强制只输出短句。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<span id="paper-post-training-sd-dpo-8723680d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4cc0854feb5b0998">Style-Debiased DPO想更新的是知识，还是让模型统一采用某种文风？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asd-dpo">Style-Debiased DPO: Updating LLM Knowledge with Factuality-Aware Synthetic Preference Data</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Waseda University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它的任务是利用合成偏好更新知识，风格差异是需要排除的混杂因素。喜欢简洁或华丽表达，不能直接充当事实对错标签。先把知识正确性与表达形式分清，才能理解后续为何需要事实判断和组平衡，而不是把它当成风格个性化训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一新知识可以用短句或长段表达；目标是两种表达都保留正确知识，而非强制只输出短句。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现对应；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16532">原论文</a> · <a href="../../../../post-training/2609.16532-sd-dpo/">实现解读</a> · <a href="#qa-4cc0854feb5b0998">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sd-dpo" data-paper-title="Style-Debiased DPO: Updating LLM Knowledge with Factuality-Aware Synthetic Preference Data" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Style-Debiased DPO: Updating LLM Knowledge with Factuality-Aware Synthetic Preference Data LLM 后训练 Waseda University 2026-09-15 识别事实正确但风格不同的 rejected response，反转其偏好方向并按组比例加权以抵消风格梯度。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行偏好反转和组平衡损失；事实分数由 fixture 提供，不冒充 judge LLM。本地执行偏好反转和组平衡损失；事实分数由 fixture 提供，不冒充 judge LLM。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  偏好优化 知识更新 LLM 后训练 偏好与对齐：先看反馈长什么样 被标为rejected的回答事实正确时，SD-DPO为何会反转偏好方向？ 合成偏好可能把风格差异误当成知识错误，普通DPO会随之压低事实正确的表达。SD-DPO识别这类回答，反转对应偏好并按组比例加权，让两组风格梯度相互抵消。关键是事实判断与组构造可靠，不能把任何不同写法都自动改成正例。 教学例子：两份回答给出同一事实，一份简短、一份带客套话。若标签只偏爱客套话，直接训练可能学到风格而非知识。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-dc95882a3e62042c">被标为rejected的回答事实正确时，SD-DPO为何会反转偏好方向？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asd-dpo">Style-Debiased DPO: Updating LLM Knowledge with Factuality-Aware Synthetic Preference Data</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Waseda University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>合成偏好可能把风格差异误当成知识错误，普通DPO会随之压低事实正确的表达。SD-DPO识别这类回答，反转对应偏好并按组比例加权，让两组风格梯度相互抵消。关键是事实判断与组构造可靠，不能把任何不同写法都自动改成正例。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两份回答给出同一事实，一份简短、一份带客套话。若标签只偏爱客套话，直接训练可能学到风格而非知识。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现对应；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16532">原论文</a> · <a href="../../../../post-training/2609.16532-sd-dpo/">实现解读</a> · <a href="#qa-dc95882a3e62042c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sd-dpo" data-paper-title="Style-Debiased DPO: Updating LLM Knowledge with Factuality-Aware Synthetic Preference Data" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Style-Debiased DPO: Updating LLM Knowledge with Factuality-Aware Synthetic Preference Data LLM 后训练 Waseda University 2026-09-15 识别事实正确但风格不同的 rejected response，反转其偏好方向并按组比例加权以抵消风格梯度。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行偏好反转和组平衡损失；事实分数由 fixture 提供，不冒充 judge LLM。本地执行偏好反转和组平衡损失；事实分数由 fixture 提供，不冒充 judge LLM。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  偏好优化 知识更新 LLM 后训练 偏好与对齐：先看反馈长什么样 SD-DPO的反转与简单删除风格样本有何不同？ 删除只去掉这类样本的作用，反转再按组比例加权则试图抵消原有风格方向。能否正确区分事实与风格是前提，不能把错误回答也反转成正例。 例如同一事实有正式与口语两种表达，应先确认内容正确，再讨论如何平衡风格监督。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d1ee0ad22878bbd9">SD-DPO的反转与简单删除风格样本有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asd-dpo">Style-Debiased DPO: Updating LLM Knowledge with Factuality-Aware Synthetic Preference Data</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Waseda University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>删除只去掉这类样本的作用，反转再按组比例加权则试图抵消原有风格方向。能否正确区分事实与风格是前提，不能把错误回答也反转成正例。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一事实有正式与口语两种表达，应先确认内容正确，再讨论如何平衡风格监督。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现对应；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16532">原论文</a> · <a href="../../../../post-training/2609.16532-sd-dpo/">实现解读</a> · <a href="#qa-d1ee0ad22878bbd9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sd-dpo" data-paper-title="Style-Debiased DPO: Updating LLM Knowledge with Factuality-Aware Synthetic Preference Data" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Style-Debiased DPO: Updating LLM Knowledge with Factuality-Aware Synthetic Preference Data LLM 后训练 Waseda University 2026-09-15 识别事实正确但风格不同的 rejected response，反转其偏好方向并按组比例加权以抵消风格梯度。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行偏好反转和组平衡损失；事实分数由 fixture 提供，不冒充 judge LLM。本地执行偏好反转和组平衡损失；事实分数由 fixture 提供，不冒充 judge LLM。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  偏好优化 知识更新 LLM 后训练 偏好与对齐：先看反馈长什么样 SD-DPO本地事实分数来自哪里，能代表真实裁判识别能力吗？ 本地事实分数由固定测试输入提供，执行的是偏好反转和组平衡损失。它能验证给定标签下的数据流与计算，不能证明自动事实裁判已实现，也不能据此宣称知识更新成功。 例如测试指定某回答事实正确，程序按规则反转，只说明规则执行对，未说明它自己识别出事实。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b16448413bb6fd49">SD-DPO本地事实分数来自哪里，能代表真实裁判识别能力吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asd-dpo">Style-Debiased DPO: Updating LLM Knowledge with Factuality-Aware Synthetic Preference Data</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Waseda University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>本地事实分数由固定测试输入提供，执行的是偏好反转和组平衡损失。它能验证给定标签下的数据流与计算，不能证明自动事实裁判已实现，也不能据此宣称知识更新成功。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如测试指定某回答事实正确，程序按规则反转，只说明规则执行对，未说明它自己识别出事实。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现对应；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16532">原论文</a> · <a href="../../../../post-training/2609.16532-sd-dpo/">实现解读</a> · <a href="#qa-b16448413bb6fd49">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:normalized-dpo" data-paper-title="Disentangling Optimization Scale from Preference Scale in DPO" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Disentangling Optimization Scale from Preference Scale in DPO LLM 后训练 Affiliation not listed in the paper 2026-08-27 标准 DPO 的同时改变偏好噪声尺度与梯度幅度，导致有效学习率被隐式重缩放。论文用除以的 centered-softplus 保持相同 argmin，同时让梯度尺度在时不消失。 复现级别：核心公式 mini-suite。复现级别：核心公式 mini-suite。实现 centered-softplus 归一化目标及连续的极限。本地为候选策略机制验证，不是语言模型偏好数据全量训练。arithmetic-smoke、100 steps：accuracy 0.1953 → 0.4766，并记录 preference margin、normalized loss 与梯度力。指标见 metrics/arithmetic-smoke-seed42.json。  DPO 偏好/优化尺度解耦 LLM 后训练 偏好与对齐：先看反馈长什么样 Normalized DPO里的margin是人的评分差，还是模型对一对回答的相对偏好量？ 这里的margin是进入偏好损失的模型侧相对量，而不是直接读取两个人工分数相减。数据告诉模型哪条回答更受偏好，当前策略和参考策略的概率决定模型侧间隔；β再控制它进入偏好曲线的尺度。先区分标签与模型分数，才不会把归一化误读成改写标注。 教学例子：标注只给出回答甲胜过乙，没有说胜出三分；训练仍可从两条回答的概率算出当前间隔。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<span id="paper-post-training-normalized-dpo-59718764" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d8f5f2448d0d1fc9">Normalized DPO里的margin是人的评分差，还是模型对一对回答的相对偏好量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Anormalized-dpo">Disentangling Optimization Scale from Preference Scale in DPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Affiliation not listed in the paper</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这里的margin是进入偏好损失的模型侧相对量，而不是直接读取两个人工分数相减。数据告诉模型哪条回答更受偏好，当前策略和参考策略的概率决定模型侧间隔；β再控制它进入偏好曲线的尺度。先区分标签与模型分数，才不会把归一化误读成改写标注。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>标注只给出回答甲胜过乙，没有说胜出三分；训练仍可从两条回答的概率算出当前间隔。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27032">原论文</a> · <a href="../../../../post-training/2608.27032-normalized-dpo/">实现解读</a> · <a href="#qa-d8f5f2448d0d1fc9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:normalized-dpo" data-paper-title="Disentangling Optimization Scale from Preference Scale in DPO" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Disentangling Optimization Scale from Preference Scale in DPO LLM 后训练 Affiliation not listed in the paper 2026-08-27 标准 DPO 的同时改变偏好噪声尺度与梯度幅度，导致有效学习率被隐式重缩放。论文用除以的 centered-softplus 保持相同 argmin，同时让梯度尺度在时不消失。 复现级别：核心公式 mini-suite。复现级别：核心公式 mini-suite。实现 centered-softplus 归一化目标及连续的极限。本地为候选策略机制验证，不是语言模型偏好数据全量训练。arithmetic-smoke、100 steps：accuracy 0.1953 → 0.4766，并记录 preference margin、normalized loss 与梯度力。指标见 metrics/arithmetic-smoke-seed42.json。  DPO 偏好/优化尺度解耦 LLM 后训练 偏好与对齐：先看反馈长什么样 Normalized DPO除以beta后，为什么还能保持目标最优点却改变梯度尺度？ 对固定正beta，损失减常数再乘正数不会改变最优点，但会重标度梯度。标准DPO的beta同时控制偏好曲线与更新幅度；中心化softplus再除beta后，margin梯度不再额外乘beta，因而可以把偏好尺度和有效学习率分开讨论。 教学例子：保持同一组偏好，只调小beta。普通目标的更新可能同步变弱；归一化目标让曲线设置与步长不再被同一个因子绑定。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-6f9a407550fa6eb6">Normalized DPO除以beta后，为什么还能保持目标最优点却改变梯度尺度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Anormalized-dpo">Disentangling Optimization Scale from Preference Scale in DPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Affiliation not listed in the paper</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>对固定正beta，损失减常数再乘正数不会改变最优点，但会重标度梯度。标准DPO的beta同时控制偏好曲线与更新幅度；中心化softplus再除beta后，margin梯度不再额外乘beta，因而可以把偏好尺度和有效学习率分开讨论。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>保持同一组偏好，只调小beta。普通目标的更新可能同步变弱；归一化目标让曲线设置与步长不再被同一个因子绑定。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27032">原论文</a> · <a href="../../../../post-training/2608.27032-normalized-dpo/">实现解读</a> · <a href="#qa-6f9a407550fa6eb6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:normalized-dpo" data-paper-title="Disentangling Optimization Scale from Preference Scale in DPO" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Disentangling Optimization Scale from Preference Scale in DPO LLM 后训练 Affiliation not listed in the paper 2026-08-27 标准 DPO 的同时改变偏好噪声尺度与梯度幅度，导致有效学习率被隐式重缩放。论文用除以的 centered-softplus 保持相同 argmin，同时让梯度尺度在时不消失。 复现级别：核心公式 mini-suite。复现级别：核心公式 mini-suite。实现 centered-softplus 归一化目标及连续的极限。本地为候选策略机制验证，不是语言模型偏好数据全量训练。arithmetic-smoke、100 steps：accuracy 0.1953 → 0.4766，并记录 preference margin、normalized loss 与梯度力。指标见 metrics/arithmetic-smoke-seed42.json。  DPO 偏好/优化尺度解耦 LLM 后训练 偏好与对齐：先看反馈长什么样 Normalized DPO与单纯重新调学习率在机制上完全相同吗？ 它通过目标的中心化和除β显式改变梯度尺度，单纯调学习率则在优化器外缩放更新。简单条件下可有联系，但动量、自适应统计等可能使训练路径不同，不能直接声称全面等价。 例如自适应优化器还维护历史二阶量，外部步长与损失缩放不必产生完全相同的状态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0e56aa9d911938bb">Normalized DPO与单纯重新调学习率在机制上完全相同吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Anormalized-dpo">Disentangling Optimization Scale from Preference Scale in DPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Affiliation not listed in the paper</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它通过目标的中心化和除β显式改变梯度尺度，单纯调学习率则在优化器外缩放更新。简单条件下可有联系，但动量、自适应统计等可能使训练路径不同，不能直接声称全面等价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如自适应优化器还维护历史二阶量，外部步长与损失缩放不必产生完全相同的状态。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27032">原论文</a> · <a href="../../../../post-training/2608.27032-normalized-dpo/">实现解读</a> · <a href="#qa-0e56aa9d911938bb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:normalized-dpo" data-paper-title="Disentangling Optimization Scale from Preference Scale in DPO" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Disentangling Optimization Scale from Preference Scale in DPO LLM 后训练 Affiliation not listed in the paper 2026-08-27 标准 DPO 的同时改变偏好噪声尺度与梯度幅度，导致有效学习率被隐式重缩放。论文用除以的 centered-softplus 保持相同 argmin，同时让梯度尺度在时不消失。 复现级别：核心公式 mini-suite。复现级别：核心公式 mini-suite。实现 centered-softplus 归一化目标及连续的极限。本地为候选策略机制验证，不是语言模型偏好数据全量训练。arithmetic-smoke、100 steps：accuracy 0.1953 → 0.4766，并记录 preference margin、normalized loss 与梯度力。指标见 metrics/arithmetic-smoke-seed42.json。  DPO 偏好/优化尺度解耦 LLM 后训练 偏好与对齐：先看反馈长什么样 归一化DPO在β很小时如何避免把公式误算成零除零？ 中心化softplus与log2之差需要稳定计算或使用小β极限，梯度为负的sigmoid而不随β直接消失。实现应检查数值极限，不能只把β置零代入分式；本地候选诊断不代表全量偏好训练。 例如β极小时应检验损失和梯度趋近有限值，而不是用异常捕获后统一返回零。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c8ea679e776c4425">归一化DPO在β很小时如何避免把公式误算成零除零？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Anormalized-dpo">Disentangling Optimization Scale from Preference Scale in DPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Affiliation not listed in the paper</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>中心化softplus与log2之差需要稳定计算或使用小β极限，梯度为负的sigmoid而不随β直接消失。实现应检查数值极限，不能只把β置零代入分式；本地候选诊断不代表全量偏好训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如β极小时应检验损失和梯度趋近有限值，而不是用异常捕获后统一返回零。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27032">原论文</a> · <a href="../../../../post-training/2608.27032-normalized-dpo/">实现解读</a> · <a href="#qa-c8ea679e776c4425">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:grip" data-paper-title="GRIP: Granular Reward-Guided Parameter Interpolation for Efficient Reasoning" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="GRIP: Granular Reward-Guided Parameter Interpolation for Efficient Reasoning LLM 后训练 Peking University 2026-08-26 在 thinking 与 instruct 权重间，不使用单一全局系数，而由细粒度 reward 学习分层/参数插值，使模型保留推理准确率同时缩短输出。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。本地对照口径：arithmetic-smoke 100 steps，accuracy 0.1250 → 0.2344（+87.50%）；本地在策略概率而非大模型权重上验证 reward-guided interpolation。  奖励引导参数插值 LLM 后训练 偏好与对齐：先看反馈长什么样 GRIP得到的是一个合并模型，还是每个请求都先运行thinking和instruct两套模型？ 原文操作对象是两套对齐权重之间的参数插值，产物是一套组合参数，再用它执行模型。它不是根据每次回答质量在线选择两位专家，也不需要先生成两份答案再投票。能否合理插值还取决于权重结构是否对应，不能把任意架构直接相加。 教学例子：先把同形状层的两份权重按系数组合，再做一次前向；并非先各生成一篇答案再挑短的一篇。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<span id="paper-post-training-grip-70305ebb" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-3564cca28d3e1319">GRIP得到的是一个合并模型，还是每个请求都先运行thinking和instruct两套模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agrip">GRIP: Granular Reward-Guided Parameter Interpolation for Efficient Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原文操作对象是两套对齐权重之间的参数插值，产物是一套组合参数，再用它执行模型。它不是根据每次回答质量在线选择两位专家，也不需要先生成两份答案再投票。能否合理插值还取决于权重结构是否对应，不能把任意架构直接相加。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先把同形状层的两份权重按系数组合，再做一次前向；并非先各生成一篇答案再挑短的一篇。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25583">原论文</a> · <a href="../../../../post-training/2608.25583-grip/">实现解读</a> · <a href="#qa-3564cca28d3e1319">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:grip" data-paper-title="GRIP: Granular Reward-Guided Parameter Interpolation for Efficient Reasoning" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="GRIP: Granular Reward-Guided Parameter Interpolation for Efficient Reasoning LLM 后训练 Peking University 2026-08-26 在 thinking 与 instruct 权重间，不使用单一全局系数，而由细粒度 reward 学习分层/参数插值，使模型保留推理准确率同时缩短输出。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。本地对照口径：arithmetic-smoke 100 steps，accuracy 0.1250 → 0.2344（+87.50%）；本地在策略概率而非大模型权重上验证 reward-guided interpolation。  奖励引导参数插值 LLM 后训练 偏好与对齐：先看反馈长什么样 GRIP为什么学习细粒度参数插值，而不是给thinking和instruct模型一个统一比例？ 不同层或参数承担的能力不同，统一系数可能同时削弱推理与简洁表达。GRIP用奖励指导细粒度插值，使不同位置有不同混合程度。原文讨论权重组合，本地策略概率插值只是缩小诊断，两者不能因公式外形相似就视为同规模模型验证。 教学例子：希望保留解题模型的计算习惯，又减少重复解释，可以让不同参数区域承担不同混合比例，而非所有层一律各取一半。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-043e5c5450e52cbc">GRIP为什么学习细粒度参数插值，而不是给thinking和instruct模型一个统一比例？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agrip">GRIP: Granular Reward-Guided Parameter Interpolation for Efficient Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同层或参数承担的能力不同，统一系数可能同时削弱推理与简洁表达。GRIP用奖励指导细粒度插值，使不同位置有不同混合程度。原文讨论权重组合，本地策略概率插值只是缩小诊断，两者不能因公式外形相似就视为同规模模型验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>希望保留解题模型的计算习惯，又减少重复解释，可以让不同参数区域承担不同混合比例，而非所有层一律各取一半。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25583">原论文</a> · <a href="../../../../post-training/2608.25583-grip/">实现解读</a> · <a href="#qa-043e5c5450e52cbc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:grip" data-paper-title="GRIP: Granular Reward-Guided Parameter Interpolation for Efficient Reasoning" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="GRIP: Granular Reward-Guided Parameter Interpolation for Efficient Reasoning LLM 后训练 Peking University 2026-08-26 在 thinking 与 instruct 权重间，不使用单一全局系数，而由细粒度 reward 学习分层/参数插值，使模型保留推理准确率同时缩短输出。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。本地对照口径：arithmetic-smoke 100 steps，accuracy 0.1250 → 0.2344（+87.50%）；本地在策略概率而非大模型权重上验证 reward-guided interpolation。  奖励引导参数插值 LLM 后训练 偏好与对齐：先看反馈长什么样 GRIP改变参数与推理时降低采样温度，都能影响输出长度，作用位置相同吗？ 不同。参数插值改变各上下文下的模型分布；温度则对某次前向已有的logits重新缩放。较低温度可能改变采样多样性，却不等于学到thinking与instruct能力的参数组合。即使两者都让某例变短，也不能用长度相同证明机制等价。 教学例子：合并模型可能改变首选推理步骤；同一模型降温通常仍围绕原来更高的logit进行选择。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b9c01e1412413fd6">GRIP改变参数与推理时降低采样温度，都能影响输出长度，作用位置相同吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agrip">GRIP: Granular Reward-Guided Parameter Interpolation for Efficient Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同。参数插值改变各上下文下的模型分布；温度则对某次前向已有的logits重新缩放。较低温度可能改变采样多样性，却不等于学到thinking与instruct能力的参数组合。即使两者都让某例变短，也不能用长度相同证明机制等价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>合并模型可能改变首选推理步骤；同一模型降温通常仍围绕原来更高的logit进行选择。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25583">原论文</a> · <a href="../../../../post-training/2608.25583-grip/">实现解读</a> · <a href="#qa-b9c01e1412413fd6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:grip" data-paper-title="GRIP: Granular Reward-Guided Parameter Interpolation for Efficient Reasoning" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="GRIP: Granular Reward-Guided Parameter Interpolation for Efficient Reasoning LLM 后训练 Peking University 2026-08-26 在 thinking 与 instruct 权重间，不使用单一全局系数，而由细粒度 reward 学习分层/参数插值，使模型保留推理准确率同时缩短输出。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。本地对照口径：arithmetic-smoke 100 steps，accuracy 0.1250 → 0.2344（+87.50%）；本地在策略概率而非大模型权重上验证 reward-guided interpolation。  奖励引导参数插值 LLM 后训练 偏好与对齐：先看反馈长什么样 GRIP的逐元素插值需要哪些形状与评估边界？ 两套权重及插值系数必须可按目标粒度对齐，系数广播也要符合层或参数定义。奖励应来自允许的数据协议；本地确定性候选任务只隔离插值机制，不证明论文检查点的推理和长度收益。 例如按层系数不能错广播成按词表列系数，否则即使张量能相乘也改变了粒度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1dad8a09f9c6a8fb">GRIP的逐元素插值需要哪些形状与评估边界？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agrip">GRIP: Granular Reward-Guided Parameter Interpolation for Efficient Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两套权重及插值系数必须可按目标粒度对齐，系数广播也要符合层或参数定义。奖励应来自允许的数据协议；本地确定性候选任务只隔离插值机制，不证明论文检查点的推理和长度收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如按层系数不能错广播成按词表列系数，否则即使张量能相乘也改变了粒度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25583">原论文</a> · <a href="../../../../post-training/2608.25583-grip/">实现解读</a> · <a href="#qa-1dad8a09f9c6a8fb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:c2-dpo" data-paper-title="Context Blindness in DPO: Mitigating Object Hallucination in MLLMs via Context-Calibrated Preference Optimization" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Context Blindness in DPO: Mitigating Object Hallucination in MLLMs via Context-Calibrated Preference Optimization LLM 后训练 Korea University 2026-08-12 普通 DPO 即使输入相关图像上下文，也可能主要依赖语言先验。论文先定义 CPG，度量加入上下文后 chosen/rejected preference margin 增加多少；C²-DPO 直接扩大该增益，同时保留原偏好顺序。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实际计算 full/degraded context 的 Contextual Preference Gain 并参与偏好更新；不把候选策略模型写成完整 MLLM 微调。尚未下载 Qwen2-VL、SENTINEL 与 Object HalBench 做完整微调；MR7 同时提供 checkpoint matrix / lmms-eval 基础设施，后续可把该目标接入真实 MLLM 训练。120 steps arithmetic mini-suite：accuracy 0.1953→0.6719；  多模态上下文偏好校准 LLM 后训练 偏好与对齐：先看反馈长什么样 C²-DPO的一条训练样本为何同时需要回答对和两种上下文？ 回答对给出同一问题下chosen与rejected的相对偏好；完整与退化上下文则提供两种证据条件。这是两个不同维度，不能把退化上下文误当另一条被拒回答。先固定回答内容、只改变证据，后续比较才是在观察上下文带来的偏好变化。 教学例子：仍比较“红车”和“蓝车”两条回答，分别让模型看原图与退化图，而不是换成另一道问题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<span id="paper-post-training-c2-dpo-2993ea41" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-24a30e0257152972">C²-DPO的一条训练样本为何同时需要回答对和两种上下文？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Ac2-dpo">Context Blindness in DPO: Mitigating Object Hallucination in MLLMs via Context-Calibrated Preference Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Korea University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>回答对给出同一问题下chosen与rejected的相对偏好；完整与退化上下文则提供两种证据条件。这是两个不同维度，不能把退化上下文误当另一条被拒回答。先固定回答内容、只改变证据，后续比较才是在观察上下文带来的偏好变化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>仍比较“红车”和“蓝车”两条回答，分别让模型看原图与退化图，而不是换成另一道问题。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.12158">原论文</a> · <a href="../../../../post-training/2608.12158-c2-dpo/">实现解读</a> · <a href="#qa-24a30e0257152972">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:c2-dpo" data-paper-title="Context Blindness in DPO: Mitigating Object Hallucination in MLLMs via Context-Calibrated Preference Optimization" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Context Blindness in DPO: Mitigating Object Hallucination in MLLMs via Context-Calibrated Preference Optimization LLM 后训练 Korea University 2026-08-12 普通 DPO 即使输入相关图像上下文，也可能主要依赖语言先验。论文先定义 CPG，度量加入上下文后 chosen/rejected preference margin 增加多少；C²-DPO 直接扩大该增益，同时保留原偏好顺序。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实际计算 full/degraded context 的 Contextual Preference Gain 并参与偏好更新；不把候选策略模型写成完整 MLLM 微调。尚未下载 Qwen2-VL、SENTINEL 与 Object HalBench 做完整微调；MR7 同时提供 checkpoint matrix / lmms-eval 基础设施，后续可把该目标接入真实 MLLM 训练。120 steps arithmetic mini-suite：accuracy 0.1953→0.6719；  多模态上下文偏好校准 LLM 后训练 偏好与对齐：先看反馈长什么样 C²-DPO为什么比较完整与退化上下文中的偏好margin，而不只训练chosen更高？ 仅提高chosen概率时，模型可能依靠语言惯性忽略图像。上下文偏好增益比较同一回答对在完整和退化证据下的margin差，鼓励偏好真正随证据改变，同时保留原偏好顺序。增益依赖退化方式是否有效，不能直接解释为视觉理解已经正确。 教学例子：同一对图表答案在有图和遮图时都被同样偏爱，说明语言先验可能主导；希望有图后正确答案得到额外支持。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-35469067fe68386f">C²-DPO为什么比较完整与退化上下文中的偏好margin，而不只训练chosen更高？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Ac2-dpo">Context Blindness in DPO: Mitigating Object Hallucination in MLLMs via Context-Calibrated Preference Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Korea University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>仅提高chosen概率时，模型可能依靠语言惯性忽略图像。上下文偏好增益比较同一回答对在完整和退化证据下的margin差，鼓励偏好真正随证据改变，同时保留原偏好顺序。增益依赖退化方式是否有效，不能直接解释为视觉理解已经正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一对图表答案在有图和遮图时都被同样偏爱，说明语言先验可能主导；希望有图后正确答案得到额外支持。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.12158">原论文</a> · <a href="../../../../post-training/2608.12158-c2-dpo/">实现解读</a> · <a href="#qa-35469067fe68386f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:c2-dpo" data-paper-title="Context Blindness in DPO: Mitigating Object Hallucination in MLLMs via Context-Calibrated Preference Optimization" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Context Blindness in DPO: Mitigating Object Hallucination in MLLMs via Context-Calibrated Preference Optimization LLM 后训练 Korea University 2026-08-12 普通 DPO 即使输入相关图像上下文，也可能主要依赖语言先验。论文先定义 CPG，度量加入上下文后 chosen/rejected preference margin 增加多少；C²-DPO 直接扩大该增益，同时保留原偏好顺序。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实际计算 full/degraded context 的 Contextual Preference Gain 并参与偏好更新；不把候选策略模型写成完整 MLLM 微调。尚未下载 Qwen2-VL、SENTINEL 与 Object HalBench 做完整微调；MR7 同时提供 checkpoint matrix / lmms-eval 基础设施，后续可把该目标接入真实 MLLM 训练。120 steps arithmetic mini-suite：accuracy 0.1953→0.6719；  多模态上下文偏好校准 LLM 后训练 偏好与对齐：先看反馈长什么样 CPG为正与chosen在完整上下文中胜出，是同一条件吗？ 不是。CPG比较两个上下文中的margin差，而chosen胜出要求完整上下文的margin本身为正。差值变好时，完整条件仍可能偏好错误回答。因此增加上下文增益与保持原偏好顺序是不同约束，不能只凭正CPG就宣布回答已正确。 教学例子：教学用margin从−3变成−1，增益为正但chosen仍未胜出；这些数字只说明两个判断条件不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-bb62ba4316cf25a3">CPG为正与chosen在完整上下文中胜出，是同一条件吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Ac2-dpo">Context Blindness in DPO: Mitigating Object Hallucination in MLLMs via Context-Calibrated Preference Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Korea University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。CPG比较两个上下文中的margin差，而chosen胜出要求完整上下文的margin本身为正。差值变好时，完整条件仍可能偏好错误回答。因此增加上下文增益与保持原偏好顺序是不同约束，不能只凭正CPG就宣布回答已正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学用margin从−3变成−1，增益为正但chosen仍未胜出；这些数字只说明两个判断条件不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.12158">原论文</a> · <a href="../../../../post-training/2608.12158-c2-dpo/">实现解读</a> · <a href="#qa-bb62ba4316cf25a3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:c2-dpo" data-paper-title="Context Blindness in DPO: Mitigating Object Hallucination in MLLMs via Context-Calibrated Preference Optimization" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Context Blindness in DPO: Mitigating Object Hallucination in MLLMs via Context-Calibrated Preference Optimization LLM 后训练 Korea University 2026-08-12 普通 DPO 即使输入相关图像上下文，也可能主要依赖语言先验。论文先定义 CPG，度量加入上下文后 chosen/rejected preference margin 增加多少；C²-DPO 直接扩大该增益，同时保留原偏好顺序。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。实际计算 full/degraded context 的 Contextual Preference Gain 并参与偏好更新；不把候选策略模型写成完整 MLLM 微调。尚未下载 Qwen2-VL、SENTINEL 与 Object HalBench 做完整微调；MR7 同时提供 checkpoint matrix / lmms-eval 基础设施，后续可把该目标接入真实 MLLM 训练。120 steps arithmetic mini-suite：accuracy 0.1953→0.6719；  多模态上下文偏好校准 LLM 后训练 偏好与对齐：先看反馈长什么样 C²-DPO里两个margin必须使用什么一致性协议？ 应对同一问题、同一chosen/rejected对比较两种上下文，避免把回答变化混入上下文效应。退化上下文也不能携带答案。本地尚未完成指定多模态模型和数据的完整微调。 例如完整图评A/B、退化图却评C/D，两个间隔相减就不再只测图像贡献。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-86d4bee16225c912">C²-DPO里两个margin必须使用什么一致性协议？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Ac2-dpo">Context Blindness in DPO: Mitigating Object Hallucination in MLLMs via Context-Calibrated Preference Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Korea University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>应对同一问题、同一chosen/rejected对比较两种上下文，避免把回答变化混入上下文效应。退化上下文也不能携带答案。本地尚未完成指定多模态模型和数据的完整微调。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如完整图评A/B、退化图却评C/D，两个间隔相减就不再只测图像贡献。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.12158">原论文</a> · <a href="../../../../post-training/2608.12158-c2-dpo/">实现解读</a> · <a href="#qa-86d4bee16225c912">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:pto" data-paper-title="Preference Tree Optimization: Enhancing Goal-Oriented Dialogue with Look-Ahead Simulations" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Preference Tree Optimization: Enhancing Goal-Oriented Dialogue with Look-Ahead Simulations LLM 后训练 Reichman University 2026-08-12 逐轮偏好只判断当前回答，难以优化目标导向对话的长期结果。PTO 让 agent 和虚拟用户展开候选对话树，oracle 评价当前回答及未来延续，以偏好对迭代执行 DPO；更深 look-ahead 带来更稳定的长期策略。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实际构造 preference tree、oracle 排序与 look-ahead advantage；不冒充论文的心理咨询模型实验。未运行 Llama-2-7B、虚拟心理咨询患者或 LLM oracle；本地 deterministic reward 仅替代昂贵 evaluator，偏好树与前瞻信用路径实际执行。120 steps 的 arithmetic mini-suite 中，初始 accuracy 0.1953，PTO 路径为 0.4453；  前瞻偏好树 LLM 后训练 偏好与对齐：先看反馈长什么样 PTO里的对话策略、虚拟用户和oracle分别负责什么，最终更新谁？ 策略产生当前候选回复，虚拟用户负责续接可能的后续交互，oracle评价展开分支的结果。由这些比较构造当前状态的偏好对，再更新对话策略。模拟用户和评价器提供训练信号，并不因此等同真实用户，也不意味着三者都由同一损失更新。 教学例子：咨询策略提出两个问题，虚拟用户各自回答，评价器比较进展；被学习的是咨询策略的当前回复选择。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<span id="paper-post-training-pto-55a5beae" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ab711475e2acf5fb">PTO里的对话策略、虚拟用户和oracle分别负责什么，最终更新谁？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Apto">Preference Tree Optimization: Enhancing Goal-Oriented Dialogue with Look-Ahead Simulations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Reichman University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>策略产生当前候选回复，虚拟用户负责续接可能的后续交互，oracle评价展开分支的结果。由这些比较构造当前状态的偏好对，再更新对话策略。模拟用户和评价器提供训练信号，并不因此等同真实用户，也不意味着三者都由同一损失更新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>咨询策略提出两个问题，虚拟用户各自回答，评价器比较进展；被学习的是咨询策略的当前回复选择。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.12062">原论文</a> · <a href="../../../../post-training/2608.12062-pto/">实现解读</a> · <a href="#qa-ab711475e2acf5fb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:pto" data-paper-title="Preference Tree Optimization: Enhancing Goal-Oriented Dialogue with Look-Ahead Simulations" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Preference Tree Optimization: Enhancing Goal-Oriented Dialogue with Look-Ahead Simulations LLM 后训练 Reichman University 2026-08-12 逐轮偏好只判断当前回答，难以优化目标导向对话的长期结果。PTO 让 agent 和虚拟用户展开候选对话树，oracle 评价当前回答及未来延续，以偏好对迭代执行 DPO；更深 look-ahead 带来更稳定的长期策略。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实际构造 preference tree、oracle 排序与 look-ahead advantage；不冒充论文的心理咨询模型实验。未运行 Llama-2-7B、虚拟心理咨询患者或 LLM oracle；本地 deterministic reward 仅替代昂贵 evaluator，偏好树与前瞻信用路径实际执行。120 steps 的 arithmetic mini-suite 中，初始 accuracy 0.1953，PTO 路径为 0.4453；  前瞻偏好树 LLM 后训练 偏好与对齐：先看反馈长什么样 PTO给当前回答打偏好时，为什么还模拟后续对话？ 当前说得讨喜不一定有利于长期目标。PTO扩展候选回答的后续用户交互，由评价器比较整条分支，再把长期差异转为当前回答的偏好对供DPO使用。模拟深度改变成本和估计范围，模拟器或oracle的偏差也会进入训练，不能当真人反馈。 教学例子：助手立即猜测需求与先问一个澄清问题，第一轮可能前者更顺畅；模拟下一轮后，才可能看出澄清能避免后续走错方向。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-ba4418ae346a8ba2">PTO给当前回答打偏好时，为什么还模拟后续对话？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Apto">Preference Tree Optimization: Enhancing Goal-Oriented Dialogue with Look-Ahead Simulations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Reichman University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>当前说得讨喜不一定有利于长期目标。PTO扩展候选回答的后续用户交互，由评价器比较整条分支，再把长期差异转为当前回答的偏好对供DPO使用。模拟深度改变成本和估计范围，模拟器或oracle的偏差也会进入训练，不能当真人反馈。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>助手立即猜测需求与先问一个澄清问题，第一轮可能前者更顺畅；模拟下一轮后，才可能看出澄清能避免后续走错方向。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.12062">原论文</a> · <a href="../../../../post-training/2608.12062-pto/">实现解读</a> · <a href="#qa-ba4418ae346a8ba2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:pto" data-paper-title="Preference Tree Optimization: Enhancing Goal-Oriented Dialogue with Look-Ahead Simulations" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Preference Tree Optimization: Enhancing Goal-Oriented Dialogue with Look-Ahead Simulations LLM 后训练 Reichman University 2026-08-12 逐轮偏好只判断当前回答，难以优化目标导向对话的长期结果。PTO 让 agent 和虚拟用户展开候选对话树，oracle 评价当前回答及未来延续，以偏好对迭代执行 DPO；更深 look-ahead 带来更稳定的长期策略。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实际构造 preference tree、oracle 排序与 look-ahead advantage；不冒充论文的心理咨询模型实验。未运行 Llama-2-7B、虚拟心理咨询患者或 LLM oracle；本地 deterministic reward 仅替代昂贵 evaluator，偏好树与前瞻信用路径实际执行。120 steps 的 arithmetic mini-suite 中，初始 accuracy 0.1953，PTO 路径为 0.4453；  前瞻偏好树 LLM 后训练 偏好与对齐：先看反馈长什么样 PTO增加候选分支数与增加前瞻深度，分别扩展了哪种搜索范围？ 更多候选主要扩大同一状态可比较的动作范围，更深前瞻主要延长对动作后果的观察范围。两者都会增加模拟与评价成本，却不能互相替代：许多短分支可能漏掉迟发后果，一条深分支也可能错过更好的起始动作。这里是搜索结构对比，不是效果排名。 教学例子：五种开场各模拟一轮，是增加宽度；只试一种开场但续聊多轮，是增加深度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ade76e34fb07aaaa">PTO增加候选分支数与增加前瞻深度，分别扩展了哪种搜索范围？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Apto">Preference Tree Optimization: Enhancing Goal-Oriented Dialogue with Look-Ahead Simulations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Reichman University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>更多候选主要扩大同一状态可比较的动作范围，更深前瞻主要延长对动作后果的观察范围。两者都会增加模拟与评价成本，却不能互相替代：许多短分支可能漏掉迟发后果，一条深分支也可能错过更好的起始动作。这里是搜索结构对比，不是效果排名。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>五种开场各模拟一轮，是增加宽度；只试一种开场但续聊多轮，是增加深度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.12062">原论文</a> · <a href="../../../../post-training/2608.12062-pto/">实现解读</a> · <a href="#qa-ade76e34fb07aaaa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:pto" data-paper-title="Preference Tree Optimization: Enhancing Goal-Oriented Dialogue with Look-Ahead Simulations" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Preference Tree Optimization: Enhancing Goal-Oriented Dialogue with Look-Ahead Simulations LLM 后训练 Reichman University 2026-08-12 逐轮偏好只判断当前回答，难以优化目标导向对话的长期结果。PTO 让 agent 和虚拟用户展开候选对话树，oracle 评价当前回答及未来延续，以偏好对迭代执行 DPO；更深 look-ahead 带来更稳定的长期策略。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实际构造 preference tree、oracle 排序与 look-ahead advantage；不冒充论文的心理咨询模型实验。未运行 Llama-2-7B、虚拟心理咨询患者或 LLM oracle；本地 deterministic reward 仅替代昂贵 evaluator，偏好树与前瞻信用路径实际执行。120 steps 的 arithmetic mini-suite 中，初始 accuracy 0.1953，PTO 路径为 0.4453；  前瞻偏好树 LLM 后训练 偏好与对齐：先看反馈长什么样 PTO实现时为什么要保留当前历史与各未来分支的对应关系？ 偏好对属于同一个当前状态，未来续写必须从各自候选动作展开，不能错接其他分支或把未来结果直接放进当前策略输入。本地确定性评价器替代昂贵oracle，仅验证树与信用路径。 例如候选A引出澄清、候选B引出误解，若把A的成功结局接到B上，偏好就反了。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1a3b00a1932c6dec">PTO实现时为什么要保留当前历史与各未来分支的对应关系？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Apto">Preference Tree Optimization: Enhancing Goal-Oriented Dialogue with Look-Ahead Simulations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Reichman University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>偏好对属于同一个当前状态，未来续写必须从各自候选动作展开，不能错接其他分支或把未来结果直接放进当前策略输入。本地确定性评价器替代昂贵oracle，仅验证树与信用路径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如候选A引出澄清、候选B引出误解，若把A的成功结局接到B上，偏好就反了。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.12062">原论文</a> · <a href="../../../../post-training/2608.12062-pto/">实现解读</a> · <a href="#qa-1a3b00a1932c6dec">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rm-memorization-protocol" data-paper-title="What do Reward Models Memorize?" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="What do Reward Models Memorize? LLM 后训练 ILLC, University of Amsterdam 2026-07-27 Sec.3 Eq.1–2：对每个真实run的reward差先sigmoid，再分别对训练内20次和留出5次求均值，CM=TM−TG。必须按用户划分，不能同用户不同偏好对跨train/test。组件只聚合调用方提供的真实run分数/manifest并检验用户一致；不制造25个RM、不实现描述不充分的cooccurrence搜索、不把sigmoid(mean margin)冒充mean(sigmoid margin)。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。seed42/43/44并不把合成诊断变成真实能力评测。状态：独立 L1 数值/协议组件，diagnostic only；不代表真实LLM能力、训练收益或完整论文复现。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本地仅执行 counterfactual_memorization 及配套数值协议。外部真实模型/数据观测是调用方前提，不由fixture伪造。  奖励建模与评估协议 Counterfactual memorization LLM 后训练 偏好与对齐：先看反馈长什么样 奖励模型记忆研究为什么把训练内表现与留出表现分开？ 某偏好对在被训练时得分高，不足以区分一般规律学习与对该样本的记忆。通过多次真实划分比较同一样本训练内外的偏好概率，差值才描述其条件记忆效应。 例如同一偏好对在包含它的模型与没见过它的模型中表现不同，才有可比的记忆线索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<span id="paper-post-training-rm-memorization-protocol-fc530cbb" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-18ac1f819b98e581">奖励模型记忆研究为什么把训练内表现与留出表现分开？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arm-memorization-protocol">What do Reward Models Memorize?</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ILLC, University of Amsterdam</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>某偏好对在被训练时得分高，不足以区分一般规律学习与对该样本的记忆。通过多次真实划分比较同一样本训练内外的偏好概率，差值才描述其条件记忆效应。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一偏好对在包含它的模型与没见过它的模型中表现不同，才有可比的记忆线索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24484v1">原论文</a> · <a href="../../../../post-training/2607.24484-rm-memorization-protocol/">实现解读</a> · <a href="#qa-18ac1f819b98e581">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rm-memorization-protocol" data-paper-title="What do Reward Models Memorize?" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="What do Reward Models Memorize? LLM 后训练 ILLC, University of Amsterdam 2026-07-27 Sec.3 Eq.1–2：对每个真实run的reward差先sigmoid，再分别对训练内20次和留出5次求均值，CM=TM−TG。必须按用户划分，不能同用户不同偏好对跨train/test。组件只聚合调用方提供的真实run分数/manifest并检验用户一致；不制造25个RM、不实现描述不充分的cooccurrence搜索、不把sigmoid(mean margin)冒充mean(sigmoid margin)。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。seed42/43/44并不把合成诊断变成真实能力评测。状态：独立 L1 数值/协议组件，diagnostic only；不代表真实LLM能力、训练收益或完整论文复现。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本地仅执行 counterfactual_memorization 及配套数值协议。外部真实模型/数据观测是调用方前提，不由fixture伪造。  奖励建模与评估协议 Counterfactual memorization LLM 后训练 偏好与对齐：先看反馈长什么样 计算奖励模型记忆量时，为什么必须先逐run做sigmoid，再按训练内外平均？ sigmoid是非线性的，先平均margin再变换会改变统计量。协议先把每个真实run的优劣奖励差转为概率，再分别条件平均得到训练内记忆与留出泛化，二者差可为负。训练包含关系来自真实划分记录，不能从高分反推，也不能让同用户跨边界泄漏。 教学例子：同一偏好对在两个run的margin差异很大，先压成一个均值会掩盖概率饱和；应保留每次训练是否包含它的记录。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-13c11fab85e1d0ae">计算奖励模型记忆量时，为什么必须先逐run做sigmoid，再按训练内外平均？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arm-memorization-protocol">What do Reward Models Memorize?</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ILLC, University of Amsterdam</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>sigmoid是非线性的，先平均margin再变换会改变统计量。协议先把每个真实run的优劣奖励差转为概率，再分别条件平均得到训练内记忆与留出泛化，二者差可为负。训练包含关系来自真实划分记录，不能从高分反推，也不能让同用户跨边界泄漏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一偏好对在两个run的margin差异很大，先压成一个均值会掩盖概率饱和；应保留每次训练是否包含它的记录。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24484v1">原论文</a> · <a href="../../../../post-training/2607.24484-rm-memorization-protocol/">实现解读</a> · <a href="#qa-13c11fab85e1d0ae">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rm-memorization-protocol" data-paper-title="What do Reward Models Memorize?" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="What do Reward Models Memorize? LLM 后训练 ILLC, University of Amsterdam 2026-07-27 Sec.3 Eq.1–2：对每个真实run的reward差先sigmoid，再分别对训练内20次和留出5次求均值，CM=TM−TG。必须按用户划分，不能同用户不同偏好对跨train/test。组件只聚合调用方提供的真实run分数/manifest并检验用户一致；不制造25个RM、不实现描述不充分的cooccurrence搜索、不把sigmoid(mean margin)冒充mean(sigmoid margin)。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。seed42/43/44并不把合成诊断变成真实能力评测。状态：独立 L1 数值/协议组件，diagnostic only；不代表真实LLM能力、训练收益或完整论文复现。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本地仅执行 counterfactual_memorization 及配套数值协议。外部真实模型/数据观测是调用方前提，不由fixture伪造。  奖励建模与评估协议 Counterfactual memorization LLM 后训练 偏好与对齐：先看反馈长什么样 CM与直接训练集准确率减测试集准确率有何区别？ CM围绕同一偏好样本跨运行比较，并要求按用户划分，避免用户特征泄漏。普通两个集合均值还混合样本难度差异。该指标仍依赖划分与运行质量，不是逐条证明模型背诵。 例如两个不同用户群难度不同，训练测试差可能来自群体差异，而非同一条偏好记忆。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-cb91206f6cb57754">CM与直接训练集准确率减测试集准确率有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arm-memorization-protocol">What do Reward Models Memorize?</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ILLC, University of Amsterdam</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>CM围绕同一偏好样本跨运行比较，并要求按用户划分，避免用户特征泄漏。普通两个集合均值还混合样本难度差异。该指标仍依赖划分与运行质量，不是逐条证明模型背诵。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个不同用户群难度不同，训练测试差可能来自群体差异，而非同一条偏好记忆。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24484v1">原论文</a> · <a href="../../../../post-training/2607.24484-rm-memorization-protocol/">实现解读</a> · <a href="#qa-cb91206f6cb57754">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rm-memorization-protocol" data-paper-title="What do Reward Models Memorize?" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="What do Reward Models Memorize? LLM 后训练 ILLC, University of Amsterdam 2026-07-27 Sec.3 Eq.1–2：对每个真实run的reward差先sigmoid，再分别对训练内20次和留出5次求均值，CM=TM−TG。必须按用户划分，不能同用户不同偏好对跨train/test。组件只聚合调用方提供的真实run分数/manifest并检验用户一致；不制造25个RM、不实现描述不充分的cooccurrence搜索、不把sigmoid(mean margin)冒充mean(sigmoid margin)。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。seed42/43/44并不把合成诊断变成真实能力评测。状态：独立 L1 数值/协议组件，diagnostic only；不代表真实LLM能力、训练收益或完整论文复现。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本地仅执行 counterfactual_memorization 及配套数值协议。外部真实模型/数据观测是调用方前提，不由fixture伪造。  奖励建模与评估协议 Counterfactual memorization LLM 后训练 偏好与对齐：先看反馈长什么样 同一偏好对跨run的训练包含关系，能根据奖励模型得分高低推断吗？ 不能。训练内或留出身份必须由每次真实划分的manifest给出，得分只是被统计的结果。用高分反推“训练见过”会把结论写进分组条件，制造循环解释。还需核对用户级隔离；本地聚合组件不生成论文所需的多次RM训练运行。 教学例子：某条留出回答得分很高，仍应归入该run的留出组；不能为了符合记忆假设把它移动到训练组。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b6cbf37a01cc1dc1">同一偏好对跨run的训练包含关系，能根据奖励模型得分高低推断吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arm-memorization-protocol">What do Reward Models Memorize?</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ILLC, University of Amsterdam</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。训练内或留出身份必须由每次真实划分的manifest给出，得分只是被统计的结果。用高分反推“训练见过”会把结论写进分组条件，制造循环解释。还需核对用户级隔离；本地聚合组件不生成论文所需的多次RM训练运行。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某条留出回答得分很高，仍应归入该run的留出组；不能为了符合记忆假设把它移动到训练组。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24484v1">原论文</a> · <a href="../../../../post-training/2607.24484-rm-memorization-protocol/">实现解读</a> · <a href="#qa-b6cbf37a01cc1dc1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sa-dpo" data-paper-title="Mind the Gap: Structure-Aware Consistency in Preference Learning" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Mind the Gap: Structure-Aware Consistency in Preference Learning LLM 后训练 Google Research / Courant Institute of Mathematical Sciences 2026-04-30 对语义几乎相同的回答强求固定偏好间隔，会制造难以满足的约束。SA-DPO 将间隔改为回答距离的函数，保留相对参考策略的隐式奖励差；同时研究 margin、模型容量与 surrogate 尾部的一致性关系，而非单纯调整 DPO 的学习率。图依据原文 §5.3 重绘。原文 Figure 1 与目标函数。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。§7、附录 M 使用 Llama-3-8B LoRA；真实数据实验为 UltraFeedback 20k、1,200 步、batch 16，另需语义编码器、多基线和多次运行。完整比较估计为多小时级，成本过高，不复现（审查 DONE）；不是本地耗时实测。  直接偏好优化 语义距离自适应间隔 LLM 后训练 偏好与对齐：先看反馈长什么样 SA-DPO中的语义距离量的是两条回答，还是两个提示之间的差异？ 距离作用于同一提示下的优选与非优选回答，描述两种候选内容有多接近。它不是按题目难度或提示长度分配margin。原文实验用冻结语义表示计算回答距离，因此距离编码器的判断与偏好标签是两种来源，不能把距离直接当正确性分数。 教学例子：同题的两条同义答复可距离很小；换了两个题目，即使提示文字很像，也不是这条margin的比较对象。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<span id="paper-post-training-sa-dpo-319b4acc" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5b5098de671ca213">SA-DPO中的语义距离量的是两条回答，还是两个提示之间的差异？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asa-dpo">Mind the Gap: Structure-Aware Consistency in Preference Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research / Courant Institute of Mathematical Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>距离作用于同一提示下的优选与非优选回答，描述两种候选内容有多接近。它不是按题目难度或提示长度分配margin。原文实验用冻结语义表示计算回答距离，因此距离编码器的判断与偏好标签是两种来源，不能把距离直接当正确性分数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同题的两条同义答复可距离很小；换了两个题目，即使提示文字很像，也不是这条margin的比较对象。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.27733v1">原论文</a> · <a href="../../../../post-training/2604.27733-sa-dpo/">实现解读</a> · <a href="#qa-5b5098de671ca213">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sa-dpo" data-paper-title="Mind the Gap: Structure-Aware Consistency in Preference Learning" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Mind the Gap: Structure-Aware Consistency in Preference Learning LLM 后训练 Google Research / Courant Institute of Mathematical Sciences 2026-04-30 对语义几乎相同的回答强求固定偏好间隔，会制造难以满足的约束。SA-DPO 将间隔改为回答距离的函数，保留相对参考策略的隐式奖励差；同时研究 margin、模型容量与 surrogate 尾部的一致性关系，而非单纯调整 DPO 的学习率。图依据原文 §5.3 重绘。原文 Figure 1 与目标函数。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。§7、附录 M 使用 Llama-3-8B LoRA；真实数据实验为 UltraFeedback 20k、1,200 步、batch 16，另需语义编码器、多基线和多次运行。完整比较估计为多小时级，成本过高，不复现（审查 DONE）；不是本地耗时实测。  直接偏好优化 语义距离自适应间隔 LLM 后训练 偏好与对齐：先看反馈长什么样 两份回答语义几乎一样时，SA-DPO为什么要求更小的偏好间隔？ 固定大间隔会强迫模型区分几乎同义的表达，消耗容量并放大标注噪声。SA-DPO让额外margin随冻结表示中的语义距离变化，零距离时不额外要求分离。它仍优化相对参考策略的偏好差，语义距离的质量和平均约束强度都需要单独控制。 教学例子：“答案为三”和“结果是3”表达接近，应避免像区分正确与错误答案那样强拉开它们；距离估计也可能受表述影响。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-006c8557a58ba088">两份回答语义几乎一样时，SA-DPO为什么要求更小的偏好间隔？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asa-dpo">Mind the Gap: Structure-Aware Consistency in Preference Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research / Courant Institute of Mathematical Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定大间隔会强迫模型区分几乎同义的表达，消耗容量并放大标注噪声。SA-DPO让额外margin随冻结表示中的语义距离变化，零距离时不额外要求分离。它仍优化相对参考策略的偏好差，语义距离的质量和平均约束强度都需要单独控制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>“答案为三”和“结果是3”表达接近，应避免像区分正确与错误答案那样强拉开它们；距离估计也可能受表述影响。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.27733v1">原论文</a> · <a href="../../../../post-training/2604.27733-sa-dpo/">实现解读</a> · <a href="#qa-006c8557a58ba088">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sa-dpo" data-paper-title="Mind the Gap: Structure-Aware Consistency in Preference Learning" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Mind the Gap: Structure-Aware Consistency in Preference Learning LLM 后训练 Google Research / Courant Institute of Mathematical Sciences 2026-04-30 对语义几乎相同的回答强求固定偏好间隔，会制造难以满足的约束。SA-DPO 将间隔改为回答距离的函数，保留相对参考策略的隐式奖励差；同时研究 margin、模型容量与 surrogate 尾部的一致性关系，而非单纯调整 DPO 的学习率。图依据原文 §5.3 重绘。原文 Figure 1 与目标函数。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。§7、附录 M 使用 Llama-3-8B LoRA；真实数据实验为 UltraFeedback 20k、1,200 步、batch 16，另需语义编码器、多基线和多次运行。完整比较估计为多小时级，成本过高，不复现（审查 DONE）；不是本地耗时实测。  直接偏好优化 语义距离自适应间隔 LLM 后训练 偏好与对齐：先看反馈长什么样 SA-DPO与固定margin方法比较时，为什么要对齐平均margin？ 若平均约束强度不同，效果差可能只是整体训练压力变化。对齐平均margin后，才更接近检验按语义距离分配约束这一机制；这仍不是证明语义编码器永远判断正确。 例如一种方法平均间隔更小，训练更容易，不能把全部改善归因于它懂语义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b5ab87cfeaf71fbf">SA-DPO与固定margin方法比较时，为什么要对齐平均margin？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asa-dpo">Mind the Gap: Structure-Aware Consistency in Preference Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research / Courant Institute of Mathematical Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若平均约束强度不同，效果差可能只是整体训练压力变化。对齐平均margin后，才更接近检验按语义距离分配约束这一机制；这仍不是证明语义编码器永远判断正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一种方法平均间隔更小，训练更容易，不能把全部改善归因于它懂语义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.27733v1">原论文</a> · <a href="../../../../post-training/2604.27733-sa-dpo/">实现解读</a> · <a href="#qa-b5ab87cfeaf71fbf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sa-dpo" data-paper-title="Mind the Gap: Structure-Aware Consistency in Preference Learning" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Mind the Gap: Structure-Aware Consistency in Preference Learning LLM 后训练 Google Research / Courant Institute of Mathematical Sciences 2026-04-30 对语义几乎相同的回答强求固定偏好间隔，会制造难以满足的约束。SA-DPO 将间隔改为回答距离的函数，保留相对参考策略的隐式奖励差；同时研究 margin、模型容量与 surrogate 尾部的一致性关系，而非单纯调整 DPO 的学习率。图依据原文 §5.3 重绘。原文 Figure 1 与目标函数。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。§7、附录 M 使用 Llama-3-8B LoRA；真实数据实验为 UltraFeedback 20k、1,200 步、batch 16，另需语义编码器、多基线和多次运行。完整比较估计为多小时级，成本过高，不复现（审查 DONE）；不是本地耗时实测。  直接偏好优化 语义距离自适应间隔 LLM 后训练 偏好与对齐：先看反馈长什么样 SA-DPO在回答距离为零时应保留怎样的目标？ 额外距离margin应为零，但策略与参考的对数概率比差仍参与偏好损失。距离来自冻结表示，不可用固定常数替换后仍沿用方法名，也不应把测试标签用于校准距离系数。 例如完全相同表达的额外分离项消失，不表示整个偏好损失都直接返回零。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b5a27901e7c2d8b2">SA-DPO在回答距离为零时应保留怎样的目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asa-dpo">Mind the Gap: Structure-Aware Consistency in Preference Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research / Courant Institute of Mathematical Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>额外距离margin应为零，但策略与参考的对数概率比差仍参与偏好损失。距离来自冻结表示，不可用固定常数替换后仍沿用方法名，也不应把测试标签用于校准距离系数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如完全相同表达的额外分离项消失，不表示整个偏好损失都直接返回零。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.27733v1">原论文</a> · <a href="../../../../post-training/2604.27733-sa-dpo/">实现解读</a> · <a href="#qa-b5a27901e7c2d8b2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:group-dpo" data-paper-title="GroupDPO: Memory-Efficient Group-Wise Direct Preference Optimization" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="GroupDPO: Memory-Efficient Group-Wise Direct Preference Optimization LLM 后训练 Carnegie Mellon University 2026-04-17 GroupDPO 先无梯度计算所有响应在当前参数点的全组导数，再固定这些系数逐响应微批次反传，保留完整组目标的一阶梯度。它支持一条提示的多个正负响应，避免为计算组目标而同时保留整组模型激活；不保证替身损失值或二阶导数等价。本地核对 v1 / v2 的 §4、Algorithm 1 和 Table 1；所实现的四类目标及一阶替身机制未见实质变化。本实现以固定 v2 为准，包括对共享响应累计贡献、损失值不相等以及不保留二阶结构的边界。 完整实验：成本过高，不复现（审查 DONE）。诊断用小型真实线性神经模型，4 个组目标 × SGD / AdamW × 3 次参数更新，对照整组联合反传；L1 精确机制组件，diagnostic only，不是完整大模型能力复现，未接入 Evolve、不可晋级。完整实验：成本过高，不复现（审查 DONE）。本篇是 Google 官方会议页带出的历史补漏，不是 10 月 25 日新发表论文。backward_microbatched 先分块执行 no-grad 策略前向，将少量标量组成完整响应向量；全组系数和正样本 NLL 权重都在这一步固定。  偏好优化 组级目标与梯度等价微批次 LLM 后训练 偏好与对齐：先看反馈长什么样 GroupDPO的一组正负响应是多条独立候选，还是要拼成一条长回答？ 一组属于同一提示，内部是非空的正响应集合与负响应集合，各响应保留独立概率和身份。集合关系进入组目标，不需要把文本接成长序列。理解这个单位后，才能区分“整组目标”与“同时把整组激活放进显存”这两个问题。 教学例子：同一问题有甲乙两条正例、丙丁两条负例；四条回答各自编码，目标比较两个集合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<span id="paper-post-training-group-dpo-93d61191" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b8740cc2992f39de">GroupDPO的一组正负响应是多条独立候选，还是要拼成一条长回答？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agroup-dpo">GroupDPO: Memory-Efficient Group-Wise Direct Preference Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Carnegie Mellon University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一组属于同一提示，内部是非空的正响应集合与负响应集合，各响应保留独立概率和身份。集合关系进入组目标，不需要把文本接成长序列。理解这个单位后，才能区分“整组目标”与“同时把整组激活放进显存”这两个问题。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一问题有甲乙两条正例、丙丁两条负例；四条回答各自编码，目标比较两个集合。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.15602v1">原论文</a> · <a href="../../../../post-training/2604.15602-group-dpo/">实现解读</a> · <a href="#qa-b8740cc2992f39de">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:group-dpo" data-paper-title="GroupDPO: Memory-Efficient Group-Wise Direct Preference Optimization" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="GroupDPO: Memory-Efficient Group-Wise Direct Preference Optimization LLM 后训练 Carnegie Mellon University 2026-04-17 GroupDPO 先无梯度计算所有响应在当前参数点的全组导数，再固定这些系数逐响应微批次反传，保留完整组目标的一阶梯度。它支持一条提示的多个正负响应，避免为计算组目标而同时保留整组模型激活；不保证替身损失值或二阶导数等价。本地核对 v1 / v2 的 §4、Algorithm 1 和 Table 1；所实现的四类目标及一阶替身机制未见实质变化。本实现以固定 v2 为准，包括对共享响应累计贡献、损失值不相等以及不保留二阶结构的边界。 完整实验：成本过高，不复现（审查 DONE）。诊断用小型真实线性神经模型，4 个组目标 × SGD / AdamW × 3 次参数更新，对照整组联合反传；L1 精确机制组件，diagnostic only，不是完整大模型能力复现，未接入 Evolve、不可晋级。完整实验：成本过高，不复现（审查 DONE）。本篇是 Google 官方会议页带出的历史补漏，不是 10 月 25 日新发表论文。backward_microbatched 先分块执行 no-grad 策略前向，将少量标量组成完整响应向量；全组系数和正样本 NLL 权重都在这一步固定。  偏好优化 组级目标与梯度等价微批次 LLM 后训练 偏好与对齐：先看反馈长什么样 GroupDPO逐响应反传，为什么不能在每个微批次重新计算局部组系数？ 系数必须由同一参数点上的完整组目标导数得到，并在逐响应反传时冻结，才能恢复全组一阶梯度。只用局部响应重算会改变正负集合和归一化，得到另一个目标。参数更新后还要重新预计算；等价仅指一阶梯度，不包括损失值或Hessian。 教学例子：一题有多个正负回答，为省显存轮流送入模型；每个回答携带全组计算的固定信用，而非在自己的小批次里重新排名。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-31c1d45cb19d9504">GroupDPO逐响应反传，为什么不能在每个微批次重新计算局部组系数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agroup-dpo">GroupDPO: Memory-Efficient Group-Wise Direct Preference Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Carnegie Mellon University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>系数必须由同一参数点上的完整组目标导数得到，并在逐响应反传时冻结，才能恢复全组一阶梯度。只用局部响应重算会改变正负集合和归一化，得到另一个目标。参数更新后还要重新预计算；等价仅指一阶梯度，不包括损失值或Hessian。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一题有多个正负回答，为省显存轮流送入模型；每个回答携带全组计算的固定信用，而非在自己的小批次里重新排名。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.15602v1">原论文</a> · <a href="../../../../post-training/2604.15602-group-dpo/">实现解读</a> · <a href="#qa-31c1d45cb19d9504">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:group-dpo" data-paper-title="GroupDPO: Memory-Efficient Group-Wise Direct Preference Optimization" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="GroupDPO: Memory-Efficient Group-Wise Direct Preference Optimization LLM 后训练 Carnegie Mellon University 2026-04-17 GroupDPO 先无梯度计算所有响应在当前参数点的全组导数，再固定这些系数逐响应微批次反传，保留完整组目标的一阶梯度。它支持一条提示的多个正负响应，避免为计算组目标而同时保留整组模型激活；不保证替身损失值或二阶导数等价。本地核对 v1 / v2 的 §4、Algorithm 1 和 Table 1；所实现的四类目标及一阶替身机制未见实质变化。本实现以固定 v2 为准，包括对共享响应累计贡献、损失值不相等以及不保留二阶结构的边界。 完整实验：成本过高，不复现（审查 DONE）。诊断用小型真实线性神经模型，4 个组目标 × SGD / AdamW × 3 次参数更新，对照整组联合反传；L1 精确机制组件，diagnostic only，不是完整大模型能力复现，未接入 Evolve、不可晋级。完整实验：成本过高，不复现（审查 DONE）。本篇是 Google 官方会议页带出的历史补漏，不是 10 月 25 日新发表论文。backward_microbatched 先分块执行 no-grad 策略前向，将少量标量组成完整响应向量；全组系数和正样本 NLL 权重都在这一步固定。  偏好优化 组级目标与梯度等价微批次 LLM 后训练 偏好与对齐：先看反馈长什么样 GroupDPO支持Margin、MPO、Softmax、All-Pairs，意味着这四种组目标彼此等价吗？ 不意味着。它们定义不同的正负集合比较方式；共享的是从选定全组目标提取导数，再分开反传的内存处理办法。更换组目标会改变优化问题，而改变响应计算批次可在规定条件下保留该目标的一阶梯度，两种改动不能混称等价。 教学例子：比较所有正负配对与先汇总正集合再比较，可能给同一响应不同系数；省显存方法可分别服务二者。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ee0899295d4a06f6">GroupDPO支持Margin、MPO、Softmax、All-Pairs，意味着这四种组目标彼此等价吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agroup-dpo">GroupDPO: Memory-Efficient Group-Wise Direct Preference Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Carnegie Mellon University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不意味着。它们定义不同的正负集合比较方式；共享的是从选定全组目标提取导数，再分开反传的内存处理办法。更换组目标会改变优化问题，而改变响应计算批次可在规定条件下保留该目标的一阶梯度，两种改动不能混称等价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>比较所有正负配对与先汇总正集合再比较，可能给同一响应不同系数；省显存方法可分别服务二者。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.15602v1">原论文</a> · <a href="../../../../post-training/2604.15602-group-dpo/">实现解读</a> · <a href="#qa-ee0899295d4a06f6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:group-dpo" data-paper-title="GroupDPO: Memory-Efficient Group-Wise Direct Preference Optimization" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="GroupDPO: Memory-Efficient Group-Wise Direct Preference Optimization LLM 后训练 Carnegie Mellon University 2026-04-17 GroupDPO 先无梯度计算所有响应在当前参数点的全组导数，再固定这些系数逐响应微批次反传，保留完整组目标的一阶梯度。它支持一条提示的多个正负响应，避免为计算组目标而同时保留整组模型激活；不保证替身损失值或二阶导数等价。本地核对 v1 / v2 的 §4、Algorithm 1 和 Table 1；所实现的四类目标及一阶替身机制未见实质变化。本实现以固定 v2 为准，包括对共享响应累计贡献、损失值不相等以及不保留二阶结构的边界。 完整实验：成本过高，不复现（审查 DONE）。诊断用小型真实线性神经模型，4 个组目标 × SGD / AdamW × 3 次参数更新，对照整组联合反传；L1 精确机制组件，diagnostic only，不是完整大模型能力复现，未接入 Evolve、不可晋级。完整实验：成本过高，不复现（审查 DONE）。本篇是 Google 官方会议页带出的历史补漏，不是 10 月 25 日新发表论文。backward_microbatched 先分块执行 no-grad 策略前向，将少量标量组成完整响应向量；全组系数和正样本 NLL 权重都在这一步固定。  偏好优化 组级目标与梯度等价微批次 LLM 后训练 偏好与对齐：先看反馈长什么样 GroupDPO的预计算系数能在下一次optimizer更新后继续复用吗？ 不能。参数变化后全组导数也变，必须重新计算。逐响应反传不再额外除以微批次数或局部组数；额外正样本NLL也应按全批次组定义归一，避免隐性缩放。 例如为省一次前向沿用上步系数，会变成陈旧近似，不能再声称当前梯度精确等价。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c09b70ec0aa149ab">GroupDPO的预计算系数能在下一次optimizer更新后继续复用吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agroup-dpo">GroupDPO: Memory-Efficient Group-Wise Direct Preference Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Carnegie Mellon University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。参数变化后全组导数也变，必须重新计算。逐响应反传不再额外除以微批次数或局部组数；额外正样本NLL也应按全批次组定义归一，避免隐性缩放。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如为省一次前向沿用上步系数，会变成陈旧近似，不能再声称当前梯度精确等价。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.15602v1">原论文</a> · <a href="../../../../post-training/2604.15602-group-dpo/">实现解读</a> · <a href="#qa-c09b70ec0aa149ab">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:benchmark-self-bias" data-paper-title="When LLMs Benchmark Themselves: Deconstructing Self-Bias in Automated Evaluation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="When LLMs Benchmark Themselves: Deconstructing Self-Bias in Automated Evaluation LLM 后训练 Google 2025-09-30 Sec.2 Eq.1使用[segment,target,benchmark-role]的逐segment排名，先按segment平均，再diag−leave-self-out peers。原始分数方向必须明确，MetricX-QE越低越好。论文未公开ties细节，本地平均tie是显式约定；不把peer consensus当绝对真值，不在合成表上宣称真实模型有偏。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。seed42/43/44并不把合成诊断变成真实能力评测。状态：独立 L1 数值/协议组件，diagnostic only；不代表真实LLM能力、训练收益或完整论文复现。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本地仅执行 self_bias 及配套数值协议。外部真实模型/数据观测是调用方前提，不由fixture伪造。  LLM评估与校准 自偏好与生成式benchmark LLM 后训练 偏好与对齐：先看反馈长什么样 自评偏差表中的target与benchmark-role分别是谁，哪一格才算自评？ target是被评价的模型，benchmark-role是用于评价它的模型角色；两轴相同时才是自评的对角格。固定同一个target，再比较自身角色与其他角色，才是在观察评价者变化，不能把不同target的成绩差直接叫自评偏差。 教学例子：模型甲回答、模型乙评价是非对角格；甲回答并由甲评价才是对角格，二者的被测对象应保持甲。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<span id="paper-post-training-benchmark-self-bias-143e8f64" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7ea7ef39b1edfe7d">自评偏差表中的target与benchmark-role分别是谁，哪一格才算自评？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Abenchmark-self-bias">When LLMs Benchmark Themselves: Deconstructing Self-Bias in Automated Evaluation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>target是被评价的模型，benchmark-role是用于评价它的模型角色；两轴相同时才是自评的对角格。固定同一个target，再比较自身角色与其他角色，才是在观察评价者变化，不能把不同target的成绩差直接叫自评偏差。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型甲回答、模型乙评价是非对角格；甲回答并由甲评价才是对角格，二者的被测对象应保持甲。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2509.26600v1">原论文</a> · <a href="../../../../post-training/2509.26600-benchmark-self-bias/">实现解读</a> · <a href="#qa-7ea7ef39b1edfe7d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:benchmark-self-bias" data-paper-title="When LLMs Benchmark Themselves: Deconstructing Self-Bias in Automated Evaluation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="When LLMs Benchmark Themselves: Deconstructing Self-Bias in Automated Evaluation LLM 后训练 Google 2025-09-30 Sec.2 Eq.1使用[segment,target,benchmark-role]的逐segment排名，先按segment平均，再diag−leave-self-out peers。原始分数方向必须明确，MetricX-QE越低越好。论文未公开ties细节，本地平均tie是显式约定；不把peer consensus当绝对真值，不在合成表上宣称真实模型有偏。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。seed42/43/44并不把合成诊断变成真实能力评测。状态：独立 L1 数值/协议组件，diagnostic only；不代表真实LLM能力、训练收益或完整论文复现。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本地仅执行 self_bias 及配套数值协议。外部真实模型/数据观测是调用方前提，不由fixture伪造。  LLM评估与校准 自偏好与生成式benchmark LLM 后训练 偏好与对齐：先看反馈长什么样 衡量模型自评偏差时，为什么先逐segment排名，并把自身从peer均值排除？ 不同segment的原始分数尺度可能不同，先各自排名再平均，才能保持协议定义的比较。自评位置减去不含自身的peer结果，避免把同一个自评分混回对照。分数方向、轴顺序和并列约定都影响符号；peer共识也不是外部真值。 教学例子：某指标越低越好，另一个越高越好，若不先统一排名方向，会把优势读成劣势；自评对照中也不应再次加入自身。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-bae0503700524a2d">衡量模型自评偏差时，为什么先逐segment排名，并把自身从peer均值排除？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Abenchmark-self-bias">When LLMs Benchmark Themselves: Deconstructing Self-Bias in Automated Evaluation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同segment的原始分数尺度可能不同，先各自排名再平均，才能保持协议定义的比较。自评位置减去不含自身的peer结果，避免把同一个自评分混回对照。分数方向、轴顺序和并列约定都影响符号；peer共识也不是外部真值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某指标越低越好，另一个越高越好，若不先统一排名方向，会把优势读成劣势；自评对照中也不应再次加入自身。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2509.26600v1">原论文</a> · <a href="../../../../post-training/2509.26600-benchmark-self-bias/">实现解读</a> · <a href="#qa-bae0503700524a2d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:benchmark-self-bias" data-paper-title="When LLMs Benchmark Themselves: Deconstructing Self-Bias in Automated Evaluation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="When LLMs Benchmark Themselves: Deconstructing Self-Bias in Automated Evaluation LLM 后训练 Google 2025-09-30 Sec.2 Eq.1使用[segment,target,benchmark-role]的逐segment排名，先按segment平均，再diag−leave-self-out peers。原始分数方向必须明确，MetricX-QE越低越好。论文未公开ties细节，本地平均tie是显式约定；不把peer consensus当绝对真值，不在合成表上宣称真实模型有偏。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。seed42/43/44并不把合成诊断变成真实能力评测。状态：独立 L1 数值/协议组件，diagnostic only；不代表真实LLM能力、训练收益或完整论文复现。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本地仅执行 self_bias 及配套数值协议。外部真实模型/数据观测是调用方前提，不由fixture伪造。  LLM评估与校准 自偏好与生成式benchmark LLM 后训练 偏好与对齐：先看反馈长什么样 自评优势与模型真实更强，如何在这个协议中区分？ 协议比较同一目标在自身benchmark角色和其他角色下的排名差，尝试分离目标质量与自角色偏好。其他裁判也可能共享偏差，因此该差值是相对审计证据，并非完整能力判决。 例如某模型在所有裁判下都靠前，与只在自己评分下突然领先，是不同观察模式。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b2350803a5a27539">自评优势与模型真实更强，如何在这个协议中区分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Abenchmark-self-bias">When LLMs Benchmark Themselves: Deconstructing Self-Bias in Automated Evaluation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>协议比较同一目标在自身benchmark角色和其他角色下的排名差，尝试分离目标质量与自角色偏好。其他裁判也可能共享偏差，因此该差值是相对审计证据，并非完整能力判决。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某模型在所有裁判下都靠前，与只在自己评分下突然领先，是不同观察模式。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2509.26600v1">原论文</a> · <a href="../../../../post-training/2509.26600-benchmark-self-bias/">实现解读</a> · <a href="#qa-b2350803a5a27539">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:benchmark-self-bias" data-paper-title="When LLMs Benchmark Themselves: Deconstructing Self-Bias in Automated Evaluation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="When LLMs Benchmark Themselves: Deconstructing Self-Bias in Automated Evaluation LLM 后训练 Google 2025-09-30 Sec.2 Eq.1使用[segment,target,benchmark-role]的逐segment排名，先按segment平均，再diag−leave-self-out peers。原始分数方向必须明确，MetricX-QE越低越好。论文未公开ties细节，本地平均tie是显式约定；不把peer consensus当绝对真值，不在合成表上宣称真实模型有偏。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。seed42/43/44并不把合成诊断变成真实能力评测。状态：独立 L1 数值/协议组件，diagnostic only；不代表真实LLM能力、训练收益或完整论文复现。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本地仅执行 self_bias 及配套数值协议。外部真实模型/数据观测是调用方前提，不由fixture伪造。  LLM评估与校准 自偏好与生成式benchmark LLM 后训练 偏好与对齐：先看反馈长什么样 计算自评bias时，轴顺序与leave-self-out为什么不能弄错？ 先按每个片段排序，再沿片段平均，最后以对角自身减去排除自身的同伴均值。需声明分数越高或越低越好；负bias表示更有利自排名，不能因习惯把负值解释成更差。 例如MetricX-QE越低越好，若直接按降序排，偏差方向会被整个翻转。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0b238a5ebb648838">计算自评bias时，轴顺序与leave-self-out为什么不能弄错？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Abenchmark-self-bias">When LLMs Benchmark Themselves: Deconstructing Self-Bias in Automated Evaluation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>先按每个片段排序，再沿片段平均，最后以对角自身减去排除自身的同伴均值。需声明分数越高或越低越好；负bias表示更有利自排名，不能因习惯把负值解释成更差。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如MetricX-QE越低越好，若直接按降序排，偏差方向会被整个翻转。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2509.26600v1">原论文</a> · <a href="../../../../post-training/2509.26600-benchmark-self-bias/">实现解读</a> · <a href="#qa-0b238a5ebb648838">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:probabilistic-autorater" data-paper-title="Judging with Confidence: Calibrating Autoraters to Preference Distributions" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Judging with Confidence: Calibrating Autoraters to Preference Distributions LLM 后训练 Google 2025-09-30 Sec.3 Eq.1–2 piecewise奖励和实验用epsilon=.001可精确实现。解析成功必须在[0,1]；失败Brier=0、Log=log(epsilon)。本地严格tag parser是明确的本地约定，不是作者未公开parser；数学梯度诊断不代表可以对生成文本float解析反传，更不等于GRPO训练。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。seed42/43/44并不把合成诊断变成真实能力评测。状态：独立 L1 数值/协议组件，diagnostic only；不代表真实LLM能力、训练收益或完整论文复现。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本地仅执行 proper_rewards 及配套数值协议。外部真实模型/数据观测是调用方前提，不由fixture伪造。  奖励建模与校准 概率偏好与proper scoring rules LLM 后训练 偏好与对齐：先看反馈长什么样 概率裁判为什么输出偏好概率，而不只输出胜者？ 不同样本可存在真实偏好分歧，概率允许表达不确定程度。Brier或对数奖励鼓励预测匹配偏好频率，而非只压向零一；这依赖监督分布可靠，不意味着任意自信数字都校准。 例如评审意见接近均分时，报告中等概率比武断宣布绝对胜者更能表达分歧。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<span id="paper-post-training-probabilistic-autorater-421e42ad" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-86cdf4efbe8d3fa3">概率裁判为什么输出偏好概率，而不只输出胜者？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aprobabilistic-autorater">Judging with Confidence: Calibrating Autoraters to Preference Distributions</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同样本可存在真实偏好分歧，概率允许表达不确定程度。Brier或对数奖励鼓励预测匹配偏好频率，而非只压向零一；这依赖监督分布可靠，不意味着任意自信数字都校准。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如评审意见接近均分时，报告中等概率比武断宣布绝对胜者更能表达分歧。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.00263v1">原论文</a> · <a href="../../../../post-training/2510.00263-probabilistic-autorater/">实现解读</a> · <a href="#qa-86cdf4efbe8d3fa3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:probabilistic-autorater" data-paper-title="Judging with Confidence: Calibrating Autoraters to Preference Distributions" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Judging with Confidence: Calibrating Autoraters to Preference Distributions LLM 后训练 Google 2025-09-30 Sec.3 Eq.1–2 piecewise奖励和实验用epsilon=.001可精确实现。解析成功必须在[0,1]；失败Brier=0、Log=log(epsilon)。本地严格tag parser是明确的本地约定，不是作者未公开parser；数学梯度诊断不代表可以对生成文本float解析反传，更不等于GRPO训练。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。seed42/43/44并不把合成诊断变成真实能力评测。状态：独立 L1 数值/协议组件，diagnostic only；不代表真实LLM能力、训练收益或完整论文复现。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本地仅执行 proper_rewards 及配套数值协议。外部真实模型/数据观测是调用方前提，不由fixture伪造。  奖励建模与校准 概率偏好与proper scoring rules LLM 后训练 偏好与对齐：先看反馈长什么样 Autorater输出一个置信概率后，为什么不能把奖励梯度直接穿过文本解析器？ 实际策略先生成概率文本，解析后得到冻结奖励，再用策略梯度更新；文本到浮点的解析没有普通连续反传路径。Brier和对数奖励鼓励校准预测，非法输出走独立惩罚分支。对数值概率求导只检验评分规则，不能据此宣称已完成GRPO训练。 教学例子：模型输出“可信度很高”而非约定格式的概率，应按解析失败处理；不能偷偷改成一个合理数值再把它算作有效预测。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f08ba902f4cd5432">Autorater输出一个置信概率后，为什么不能把奖励梯度直接穿过文本解析器？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aprobabilistic-autorater">Judging with Confidence: Calibrating Autoraters to Preference Distributions</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>实际策略先生成概率文本，解析后得到冻结奖励，再用策略梯度更新；文本到浮点的解析没有普通连续反传路径。Brier和对数奖励鼓励校准预测，非法输出走独立惩罚分支。对数值概率求导只检验评分规则，不能据此宣称已完成GRPO训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型输出“可信度很高”而非约定格式的概率，应按解析失败处理；不能偷偷改成一个合理数值再把它算作有效预测。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.00263v1">原论文</a> · <a href="../../../../post-training/2510.00263-probabilistic-autorater/">实现解读</a> · <a href="#qa-f08ba902f4cd5432">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:probabilistic-autorater" data-paper-title="Judging with Confidence: Calibrating Autoraters to Preference Distributions" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Judging with Confidence: Calibrating Autoraters to Preference Distributions LLM 后训练 Google 2025-09-30 Sec.3 Eq.1–2 piecewise奖励和实验用epsilon=.001可精确实现。解析成功必须在[0,1]；失败Brier=0、Log=log(epsilon)。本地严格tag parser是明确的本地约定，不是作者未公开parser；数学梯度诊断不代表可以对生成文本float解析反传，更不等于GRPO训练。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。seed42/43/44并不把合成诊断变成真实能力评测。状态：独立 L1 数值/协议组件，diagnostic only；不代表真实LLM能力、训练收益或完整论文复现。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本地仅执行 proper_rewards 及配套数值协议。外部真实模型/数据观测是调用方前提，不由fixture伪造。  奖励建模与校准 概率偏好与proper scoring rules LLM 后训练 偏好与对齐：先看反馈长什么样 Brier与对数奖励处理置信错误的方式有何不同？ 两者都可用于概率校准，但平方误差与对数惩罚的尾部形状不同，极自信错误在对数规则下尤其敏感。原方法还为解析失败定义单独奖励，不能只比较合法数字的数学梯度。 例如预测几乎必胜却实际落败，两种规则均惩罚，但幅度随概率变化的曲线不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-87f7465105cb6097">Brier与对数奖励处理置信错误的方式有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aprobabilistic-autorater">Judging with Confidence: Calibrating Autoraters to Preference Distributions</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两者都可用于概率校准，但平方误差与对数惩罚的尾部形状不同，极自信错误在对数规则下尤其敏感。原方法还为解析失败定义单独奖励，不能只比较合法数字的数学梯度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如预测几乎必胜却实际落败，两种规则均惩罚，但幅度随概率变化的曲线不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.00263v1">原论文</a> · <a href="../../../../post-training/2510.00263-probabilistic-autorater/">实现解读</a> · <a href="#qa-87f7465105cb6097">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:probabilistic-autorater" data-paper-title="Judging with Confidence: Calibrating Autoraters to Preference Distributions" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Judging with Confidence: Calibrating Autoraters to Preference Distributions LLM 后训练 Google 2025-09-30 Sec.3 Eq.1–2 piecewise奖励和实验用epsilon=.001可精确实现。解析成功必须在[0,1]；失败Brier=0、Log=log(epsilon)。本地严格tag parser是明确的本地约定，不是作者未公开parser；数学梯度诊断不代表可以对生成文本float解析反传，更不等于GRPO训练。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。seed42/43/44并不把合成诊断变成真实能力评测。状态：独立 L1 数值/协议组件，diagnostic only；不代表真实LLM能力、训练收益或完整论文复现。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本地仅执行 proper_rewards 及配套数值协议。外部真实模型/数据观测是调用方前提，不由fixture伪造。  奖励建模与校准 概率偏好与proper scoring rules LLM 后训练 偏好与对齐：先看反馈长什么样 概率裁判生成NaN或区间外数字时，为什么不能先套评分公式再乘零掩码？ 非法值必须先分流，合法概率才进入平方或对数计算。NaN经过非线性后再乘零仍可污染损失，区间外数字也不具有偏好概率含义。原方法为解析失败单独规定奖励；本地严格标签解析器只是接口约定，不代表作者解析器或完整RL训练。 教学例子：文本解析成NaN时直接走invalid奖励分支，不能先算log(NaN)，再希望有效性mask把它擦掉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-37c219be1787c9bd">概率裁判生成NaN或区间外数字时，为什么不能先套评分公式再乘零掩码？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aprobabilistic-autorater">Judging with Confidence: Calibrating Autoraters to Preference Distributions</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>非法值必须先分流，合法概率才进入平方或对数计算。NaN经过非线性后再乘零仍可污染损失，区间外数字也不具有偏好概率含义。原方法为解析失败单独规定奖励；本地严格标签解析器只是接口约定，不代表作者解析器或完整RL训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>文本解析成NaN时直接走invalid奖励分支，不能先算log(NaN)，再希望有效性mask把它擦掉。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.00263v1">原论文</a> · <a href="../../../../post-training/2510.00263-probabilistic-autorater/">实现解读</a> · <a href="#qa-37c219be1787c9bd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:simpo" data-paper-title="SimPO" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="SimPO LLM 后训练 Princeton University 2024-05-23 DPO 训练需要常驻 reference model，而且 sequence 概率天然偏向短响应。SimPO 用平均 token log-probability 作为隐式 reward，去掉 reference model，并在 Bradley–Terry 目标中加入固定 margin。 用长度归一化的 policy log-probability 直接作 reward，并用目标 margin 拉开偏好。核心 sequence normalization、reference-free reward 和 margin 已落到真实 token loss；未复刻 Mistral/Llama/Gemma 规模训练及 AlpacaEval judge。本地在自由生成 causal LM 上实现平均 token log-probability 和 margin，训练时不创建 reference model；用相同 warmup、数据、步数与 seed 和其他自由生成方法比较。  Reference-free 偏好 LLM 后训练 偏好与对齐：先看反馈长什么样 SimPO的reference-free指没有训练反馈吗？ 不是。它仍需要chosen与rejected偏好对，只是不常驻参考模型，而用长度平均的策略对数概率作为隐式奖励，再加入固定偏好间隔。反馈来源与是否使用参考模型是不同维度。 例如两篇回答仍需知道哪篇更好，只是训练时不用再计算冻结参考模型的分数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<span id="paper-post-training-simpo-d55ff0e4" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-19268f541c6ed5d9">SimPO的reference-free指没有训练反馈吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asimpo">SimPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。它仍需要chosen与rejected偏好对，只是不常驻参考模型，而用长度平均的策略对数概率作为隐式奖励，再加入固定偏好间隔。反馈来源与是否使用参考模型是不同维度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两篇回答仍需知道哪篇更好，只是训练时不用再计算冻结参考模型的分数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2405.14734">原论文</a> · <a href="../../../../post-training/2405.14734-simpo/">实现解读</a> · <a href="#qa-19268f541c6ed5d9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:simpo" data-paper-title="SimPO" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="SimPO LLM 后训练 Princeton University 2024-05-23 DPO 训练需要常驻 reference model，而且 sequence 概率天然偏向短响应。SimPO 用平均 token log-probability 作为隐式 reward，去掉 reference model，并在 Bradley–Terry 目标中加入固定 margin。 用长度归一化的 policy log-probability 直接作 reward，并用目标 margin 拉开偏好。核心 sequence normalization、reference-free reward 和 margin 已落到真实 token loss；未复刻 Mistral/Llama/Gemma 规模训练及 AlpacaEval judge。本地在自由生成 causal LM 上实现平均 token log-probability 和 margin，训练时不创建 reference model；用相同 warmup、数据、步数与 seed 和其他自由生成方法比较。  Reference-free 偏好 LLM 后训练 偏好与对齐：先看反馈长什么样 SimPO去掉reference model后，怎样避免直接用整句概率偏爱短回答？ 整句对数概率随token累加，长度本身就会改变奖励尺度。SimPO用平均token对数概率构造隐式奖励，再要求优选回答超过拒绝回答一个margin，因此不需要额外reference前向。长度归一化减少特定偏置，但并不自动保证长短回答质量公平。 教学例子：简短错误答案与较长正确解释，直接比较累积log-prob可能偏向前者；平均token分数让长度不再直接作为求和惩罚。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-864ca18fd75dda04">SimPO去掉reference model后，怎样避免直接用整句概率偏爱短回答？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asimpo">SimPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>整句对数概率随token累加，长度本身就会改变奖励尺度。SimPO用平均token对数概率构造隐式奖励，再要求优选回答超过拒绝回答一个margin，因此不需要额外reference前向。长度归一化减少特定偏置，但并不自动保证长短回答质量公平。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>简短错误答案与较长正确解释，直接比较累积log-prob可能偏向前者；平均token分数让长度不再直接作为求和惩罚。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2405.14734">原论文</a> · <a href="../../../../post-training/2405.14734-simpo/">实现解读</a> · <a href="#qa-864ca18fd75dda04">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:simpo" data-paper-title="SimPO" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="SimPO LLM 后训练 Princeton University 2024-05-23 DPO 训练需要常驻 reference model，而且 sequence 概率天然偏向短响应。SimPO 用平均 token log-probability 作为隐式 reward，去掉 reference model，并在 Bradley–Terry 目标中加入固定 margin。 用长度归一化的 policy log-probability 直接作 reward，并用目标 margin 拉开偏好。核心 sequence normalization、reference-free reward 和 margin 已落到真实 token loss；未复刻 Mistral/Llama/Gemma 规模训练及 AlpacaEval judge。本地在自由生成 causal LM 上实现平均 token log-probability 和 margin，训练时不创建 reference model；用相同 warmup、数据、步数与 seed 和其他自由生成方法比较。  Reference-free 偏好 LLM 后训练 偏好与对齐：先看反馈长什么样 SimPO训练时的目标margin，与推理时降低温度是一种调节吗？ 不是。margin在偏好训练中规定两条回答的长度平均隐式奖励应拉开多少，直接影响参数梯度；温度在推理时重新缩放给定前缀的logits。二者可共同使用，却不等价，也不能把某个温度下回答更短当作目标margin有效的证据。 教学例子：训练比较完整回答甲乙的平均logp差；推理温度只作用于当前下一词分布，不读取这对训练回答。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-85c5fbdd0f8ee884">SimPO训练时的目标margin，与推理时降低温度是一种调节吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asimpo">SimPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。margin在偏好训练中规定两条回答的长度平均隐式奖励应拉开多少，直接影响参数梯度；温度在推理时重新缩放给定前缀的logits。二者可共同使用，却不等价，也不能把某个温度下回答更短当作目标margin有效的证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练比较完整回答甲乙的平均logp差；推理温度只作用于当前下一词分布，不读取这对训练回答。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2405.14734">原论文</a> · <a href="../../../../post-training/2405.14734-simpo/">实现解读</a> · <a href="#qa-85c5fbdd0f8ee884">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:simpo" data-paper-title="SimPO" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="SimPO LLM 后训练 Princeton University 2024-05-23 DPO 训练需要常驻 reference model，而且 sequence 概率天然偏向短响应。SimPO 用平均 token log-probability 作为隐式 reward，去掉 reference model，并在 Bradley–Terry 目标中加入固定 margin。 用长度归一化的 policy log-probability 直接作 reward，并用目标 margin 拉开偏好。核心 sequence normalization、reference-free reward 和 margin 已落到真实 token loss；未复刻 Mistral/Llama/Gemma 规模训练及 AlpacaEval judge。本地在自由生成 causal LM 上实现平均 token log-probability 和 margin，训练时不创建 reference model；用相同 warmup、数据、步数与 seed 和其他自由生成方法比较。  Reference-free 偏好 LLM 后训练 偏好与对齐：先看反馈长什么样 SimPO实现时哪些词元应该进入长度与log-prob求和？ 应使用对应响应的有效词元，求和与长度掩码需一致，不能把padding计入长度或把提示混入响应奖励。偏好损失只更新策略；本地token目标存在不代表原文大模型评审矩阵完成。 例如一个短答案补了许多padding，若也进分母，会人为改变平均奖励。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-cb729e6cab9ed41b">SimPO实现时哪些词元应该进入长度与log-prob求和？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asimpo">SimPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>应使用对应响应的有效词元，求和与长度掩码需一致，不能把padding计入长度或把提示混入响应奖励。偏好损失只更新策略；本地token目标存在不代表原文大模型评审矩阵完成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个短答案补了许多padding，若也进分母，会人为改变平均奖励。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2405.14734">原论文</a> · <a href="../../../../post-training/2405.14734-simpo/">实现解读</a> · <a href="#qa-cb729e6cab9ed41b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:orpo" data-paper-title="ORPO" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="ORPO LLM 后训练 KAIST 2024-03-12 常见对齐流程先 SFT、再用 reference-relative 偏好目标训练。ORPO 把 chosen response 的 NLL 与 chosen/rejected 的 odds-ratio penalty 合成一个目标；概率接近 0 或 1 时，odds 会提供比普通概率差更敏感的对比信号。 本地把完整候选视为 response action，未训练论文中的 Mistral/Llama 模型，KL 只用于统一报告而不参与目标。ORPO 用一个模型同时完成监督学习与偏好拉开，不需要冻结 reference model。实现了 chosen SFT 与 odds-ratio preference penalty 的单阶段更新；本地把完整候选视为 response action，未训练论文中的 Mistral/Llama 模型，KL 只用于统一报告而不参与目标。最后一步 SFT NLL 为 0.0715、chosen/rejected log-odds margin 为 6.3502；  单阶段偏好 LLM 后训练 偏好与对齐：先看反馈长什么样 ORPO里的odds和概率有什么直观区别？ 概率p表示事件占全部可能结果的份额，odds=p/(1−p)则比较发生与不发生的相对量。odds不是另一个仍在零到一之间的概率；ORPO比较的是优选和拒绝回答的赔率关系，阅读目标前先分清这两个量，才能避免把数值大小直接当置信百分比。 教学例子：教学用p=1/2时odds为1，p=3/4时odds为3；odds为3并不是概率300%。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<span id="paper-post-training-orpo-e4a32db7" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-898ddc81df5c3d9b">ORPO里的odds和概率有什么直观区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aorpo">ORPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>概率p表示事件占全部可能结果的份额，odds=p/(1−p)则比较发生与不发生的相对量。odds不是另一个仍在零到一之间的概率；ORPO比较的是优选和拒绝回答的赔率关系，阅读目标前先分清这两个量，才能避免把数值大小直接当置信百分比。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学用p=1/2时odds为1，p=3/4时odds为3；odds为3并不是概率300%。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2403.07691">原论文</a> · <a href="../../../../post-training/2403.07691-orpo/">实现解读</a> · <a href="#qa-898ddc81df5c3d9b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:orpo" data-paper-title="ORPO" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="ORPO LLM 后训练 KAIST 2024-03-12 常见对齐流程先 SFT、再用 reference-relative 偏好目标训练。ORPO 把 chosen response 的 NLL 与 chosen/rejected 的 odds-ratio penalty 合成一个目标；概率接近 0 或 1 时，odds 会提供比普通概率差更敏感的对比信号。 本地把完整候选视为 response action，未训练论文中的 Mistral/Llama 模型，KL 只用于统一报告而不参与目标。ORPO 用一个模型同时完成监督学习与偏好拉开，不需要冻结 reference model。实现了 chosen SFT 与 odds-ratio preference penalty 的单阶段更新；本地把完整候选视为 response action，未训练论文中的 Mistral/Llama 模型，KL 只用于统一报告而不参与目标。最后一步 SFT NLL 为 0.0715、chosen/rejected log-odds margin 为 6.3502；  单阶段偏好 LLM 后训练 偏好与对齐：先看反馈长什么样 ORPO把SFT与odds-ratio放在同一目标里，两部分分别约束什么？ SFT项提高优选回答的似然，odds-ratio项扩大它相对拒绝回答的赔率差，两者一起训练同一个策略，不需要独立reference模型。赔率对接近边界的概率更敏感，因此数值处理很重要；附带计算reference KL作诊断，不意味着训练目标使用了reference。 教学例子：只提升优选答案也可能顺便提升相似的坏答案；额外的赔率比较要求两者拉开，而不是只把所有候选概率一起推高。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-713377bce48ffbf5">ORPO把SFT与odds-ratio放在同一目标里，两部分分别约束什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aorpo">ORPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>SFT项提高优选回答的似然，odds-ratio项扩大它相对拒绝回答的赔率差，两者一起训练同一个策略，不需要独立reference模型。赔率对接近边界的概率更敏感，因此数值处理很重要；附带计算reference KL作诊断，不意味着训练目标使用了reference。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>只提升优选答案也可能顺便提升相似的坏答案；额外的赔率比较要求两者拉开，而不是只把所有候选概率一起推高。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2403.07691">原论文</a> · <a href="../../../../post-training/2403.07691-orpo/">实现解读</a> · <a href="#qa-713377bce48ffbf5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:orpo" data-paper-title="ORPO" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="ORPO LLM 后训练 KAIST 2024-03-12 常见对齐流程先 SFT、再用 reference-relative 偏好目标训练。ORPO 把 chosen response 的 NLL 与 chosen/rejected 的 odds-ratio penalty 合成一个目标；概率接近 0 或 1 时，odds 会提供比普通概率差更敏感的对比信号。 本地把完整候选视为 response action，未训练论文中的 Mistral/Llama 模型，KL 只用于统一报告而不参与目标。ORPO 用一个模型同时完成监督学习与偏好拉开，不需要冻结 reference model。实现了 chosen SFT 与 odds-ratio preference penalty 的单阶段更新；本地把完整候选视为 response action，未训练论文中的 Mistral/Llama 模型，KL 只用于统一报告而不参与目标。最后一步 SFT NLL 为 0.0715、chosen/rejected log-odds margin 为 6.3502；  单阶段偏好 LLM 后训练 偏好与对齐：先看反馈长什么样 ORPO的单阶段训练，与先SFT再开启独立偏好阶段在流程上有何不同？ ORPO在同一次策略训练中同时使用优选回答NLL和偏好赔率项，不需要为独立偏好阶段常驻冻结reference。两阶段流程则先得到SFT策略，再切换偏好目标与参照。阶段合并是训练组织方式的区别，不能据此推断任意初始化和数据下都更优。 教学例子：一批偏好数据同时产生NLL和赔率梯度，而不是先完成一轮只学chosen，再另开reference-relative训练。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-8b37223053c895c4">ORPO的单阶段训练，与先SFT再开启独立偏好阶段在流程上有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aorpo">ORPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>ORPO在同一次策略训练中同时使用优选回答NLL和偏好赔率项，不需要为独立偏好阶段常驻冻结reference。两阶段流程则先得到SFT策略，再切换偏好目标与参照。阶段合并是训练组织方式的区别，不能据此推断任意初始化和数据下都更优。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一批偏好数据同时产生NLL和赔率梯度，而不是先完成一轮只学chosen，再另开reference-relative训练。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2403.07691">原论文</a> · <a href="../../../../post-training/2403.07691-orpo/">实现解读</a> · <a href="#qa-8b37223053c895c4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:orpo" data-paper-title="ORPO" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="ORPO LLM 后训练 KAIST 2024-03-12 常见对齐流程先 SFT、再用 reference-relative 偏好目标训练。ORPO 把 chosen response 的 NLL 与 chosen/rejected 的 odds-ratio penalty 合成一个目标；概率接近 0 或 1 时，odds 会提供比普通概率差更敏感的对比信号。 本地把完整候选视为 response action，未训练论文中的 Mistral/Llama 模型，KL 只用于统一报告而不参与目标。ORPO 用一个模型同时完成监督学习与偏好拉开，不需要冻结 reference model。实现了 chosen SFT 与 odds-ratio preference penalty 的单阶段更新；本地把完整候选视为 response action，未训练论文中的 Mistral/Llama 模型，KL 只用于统一报告而不参与目标。最后一步 SFT NLL 为 0.0715、chosen/rejected log-odds margin 为 6.3502；  单阶段偏好 LLM 后训练 偏好与对齐：先看反馈长什么样 ORPO 实现 log-odds margin 时，为什么要处理概率靠近 0 或 1 的数值边界？ 单个log-odds是log(p)减log(1−p)，两响应再相减。边界会触发log零或极大比值；本地候选内核给p与1−p项加1e−12，并用logaddexp计算偏好损失。这是本地数值保护，不能用普通概率差替换原目标，也不能把候选概率等同逐token响应概率。 示意：p从0.9升到0.99，概率只增0.09，odds却从9升到99；直接相减概率不是同一个训练信号。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-533c71e635c7676c">ORPO 实现 log-odds margin 时，为什么要处理概率靠近 0 或 1 的数值边界？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aorpo">ORPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单个log-odds是log(p)减log(1−p)，两响应再相减。边界会触发log零或极大比值；本地候选内核给p与1−p项加1e−12，并用logaddexp计算偏好损失。这是本地数值保护，不能用普通概率差替换原目标，也不能把候选概率等同逐token响应概率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>p从0.9升到0.99，概率只增0.09，odds却从9升到99；直接相减概率不是同一个训练信号。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2403.07691">原论文</a> · <a href="../../../../post-training/2403.07691-orpo/">实现解读</a> · <a href="#qa-533c71e635c7676c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:kto" data-paper-title="KTO" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="KTO LLM 后训练 Contextual AI 2024-02-02 DPO 需要成对偏好，而生产反馈常只有点赞、点踩或是否接受。KTO 将单样本反馈映射为 desirable / undesirable utility，并用 policy 与 reference 的 KL 期望作为“参照点”；两类样本可独立采集，也允许类别不平衡。 KTO 只需要单条回答的“满意 / 不满意”标签，以 reference KL 为参照构造前景理论效用，不要求同一 prompt 的 chosen/rejected 偏好对。实现了单样本二元反馈、reference log-ratio、KL 移动参照点与两类 utility；本地 policy 是六候选线性策略，不是论文中的 1B–30B 自由生成 LLM，也未复刻人类偏好数据规模。最后一步 desirable / undesirable utility 为 0.5030 / 0.4972，KL EMA 为 0.0074。  二元反馈对齐 LLM 后训练 偏好与对齐：先看反馈长什么样 KTO里的满意类权重与不满意类权重，是反馈出现的概率吗？ 不是。两类标签描述单条回答被接受或拒绝，λ权重控制两类样本对训练效用的贡献。允许类别数量不平衡，并不表示频繁出现的标签自动更重要；样本数量与显式权重需要分开记录，不能把λ误读成模型预测的满意概率。 教学例子：点赞记录多、点踩少时，可以调整两类贡献；这没有把少量点踩伪造成与每条点赞同题的偏好对。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<span id="paper-post-training-kto-edf0a49a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ea3586d73fba657b">KTO里的满意类权重与不满意类权重，是反馈出现的概率吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Akto">KTO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Contextual AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。两类标签描述单条回答被接受或拒绝，λ权重控制两类样本对训练效用的贡献。允许类别数量不平衡，并不表示频繁出现的标签自动更重要；样本数量与显式权重需要分开记录，不能把λ误读成模型预测的满意概率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>点赞记录多、点踩少时，可以调整两类贡献；这没有把少量点踩伪造成与每条点赞同题的偏好对。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2402.01306">原论文</a> · <a href="../../../../post-training/2402.01306-kto/">实现解读</a> · <a href="#qa-ea3586d73fba657b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:kto" data-paper-title="KTO" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="KTO LLM 后训练 Contextual AI 2024-02-02 DPO 需要成对偏好，而生产反馈常只有点赞、点踩或是否接受。KTO 将单样本反馈映射为 desirable / undesirable utility，并用 policy 与 reference 的 KL 期望作为“参照点”；两类样本可独立采集，也允许类别不平衡。 KTO 只需要单条回答的“满意 / 不满意”标签，以 reference KL 为参照构造前景理论效用，不要求同一 prompt 的 chosen/rejected 偏好对。实现了单样本二元反馈、reference log-ratio、KL 移动参照点与两类 utility；本地 policy 是六候选线性策略，不是论文中的 1B–30B 自由生成 LLM，也未复刻人类偏好数据规模。最后一步 desirable / undesirable utility 为 0.5030 / 0.4972，KL EMA 为 0.0074。  二元反馈对齐 LLM 后训练 偏好与对齐：先看反馈长什么样 KTO没有同题chosen/rejected对，如何判断单条满意反馈应该往哪边更新？ 它用策略相对reference的log-ratio描述回答价值，再以KL期望提供动态参照点，分别构造满意与不满意样本的效用。两类样本可独立采集并调权，无需虚构跨题偏好对。但参照分布与类别不平衡仍影响目标，单条标签不等于绝对奖励。 教学例子：用户分别给两次不同咨询点赞和点踩，可作为单条反馈进入相应分支；不必假装这两个问题的回答构成直接比较。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-2aa2521a67232958">KTO没有同题chosen/rejected对，如何判断单条满意反馈应该往哪边更新？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Akto">KTO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Contextual AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它用策略相对reference的log-ratio描述回答价值，再以KL期望提供动态参照点，分别构造满意与不满意样本的效用。两类样本可独立采集并调权，无需虚构跨题偏好对。但参照分布与类别不平衡仍影响目标，单条标签不等于绝对奖励。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户分别给两次不同咨询点赞和点踩，可作为单条反馈进入相应分支；不必假装这两个问题的回答构成直接比较。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2402.01306">原论文</a> · <a href="../../../../post-training/2402.01306-kto/">实现解读</a> · <a href="#qa-2aa2521a67232958">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:kto" data-paper-title="KTO" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="KTO LLM 后训练 Contextual AI 2024-02-02 DPO 需要成对偏好，而生产反馈常只有点赞、点踩或是否接受。KTO 将单样本反馈映射为 desirable / undesirable utility，并用 policy 与 reference 的 KL 期望作为“参照点”；两类样本可独立采集，也允许类别不平衡。 KTO 只需要单条回答的“满意 / 不满意”标签，以 reference KL 为参照构造前景理论效用，不要求同一 prompt 的 chosen/rejected 偏好对。实现了单样本二元反馈、reference log-ratio、KL 移动参照点与两类 utility；本地 policy 是六候选线性策略，不是论文中的 1B–30B 自由生成 LLM，也未复刻人类偏好数据规模。最后一步 desirable / undesirable utility 为 0.5030 / 0.4972，KL EMA 为 0.0074。  二元反馈对齐 LLM 后训练 偏好与对齐：先看反馈长什么样 KTO与DPO的差别只在把偏好对拆开吗？ 还包括效用与参照点的定义：KTO围绕KL参照处理得失，DPO比较同提示下两回答的相对间隔。单样本反馈不能任意配成不存在的偏好关系，两类权重也影响训练取舍。 例如不同用户分别点赞和点踩，不能直接认定前者回答在后者同一问题上更优。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b7b11de358098425">KTO与DPO的差别只在把偏好对拆开吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Akto">KTO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Contextual AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>还包括效用与参照点的定义：KTO围绕KL参照处理得失，DPO比较同提示下两回答的相对间隔。单样本反馈不能任意配成不存在的偏好关系，两类权重也影响训练取舍。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如不同用户分别点赞和点踩，不能直接认定前者回答在后者同一问题上更优。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2402.01306">原论文</a> · <a href="../../../../post-training/2402.01306-kto/">实现解读</a> · <a href="#qa-b7b11de358098425">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:kto" data-paper-title="KTO" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="KTO LLM 后训练 Contextual AI 2024-02-02 DPO 需要成对偏好，而生产反馈常只有点赞、点踩或是否接受。KTO 将单样本反馈映射为 desirable / undesirable utility，并用 policy 与 reference 的 KL 期望作为“参照点”；两类样本可独立采集，也允许类别不平衡。 KTO 只需要单条回答的“满意 / 不满意”标签，以 reference KL 为参照构造前景理论效用，不要求同一 prompt 的 chosen/rejected 偏好对。实现了单样本二元反馈、reference log-ratio、KL 移动参照点与两类 utility；本地 policy 是六候选线性策略，不是论文中的 1B–30B 自由生成 LLM，也未复刻人类偏好数据规模。最后一步 desirable / undesirable utility 为 0.5030 / 0.4972，KL EMA 为 0.0074。  二元反馈对齐 LLM 后训练 偏好与对齐：先看反馈长什么样 KTO的参照点和本地候选策略应怎样解释？ 参照点来自策略到参考的KL期望，与某条回答的log-ratio不是同一个量。实现需区分总体基准与样本信号；本地六候选线性策略只验证这条计算关系，未训练原文自由生成模型。 例如一条回答的高log-ratio要相对移动基准判断，不能把它自己又当作全部KL期望。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-51338639a8b4c3b6">KTO的参照点和本地候选策略应怎样解释？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Akto">KTO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Contextual AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>参照点来自策略到参考的KL期望，与某条回答的log-ratio不是同一个量。实现需区分总体基准与样本信号；本地六候选线性策略只验证这条计算关系，未训练原文自由生成模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一条回答的高log-ratio要相对移动基准判断，不能把它自己又当作全部KL期望。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2402.01306">原论文</a> · <a href="../../../../post-training/2402.01306-kto/">实现解读</a> · <a href="#qa-51338639a8b4c3b6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:self-rewarding" data-paper-title="Self-Rewarding LM" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Self-Rewarding LM LLM 后训练 Meta AI 2024-01-18 每轮由当前模型生成候选并以 LLM-as-a-Judge 打分，形成新的偏好对继续 DPO，构成自举闭环。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.6250（+166.67%）；奖励、KL、长度和候选预算一致。  自奖励 LLM 后训练 偏好与对齐：先看反馈长什么样 Self-Rewarding裁判给两条候选相同分数时，能据此断言哪条更受偏好吗？ 不能。同分没有提供严格的优劣关系，不能仅按展示顺序制造一对有方向的偏好。该循环依靠评分差选择优选与拒绝候选，因而生成候选数量和可区分的评价是不同条件。即便得分不同，也只是当前模型裁判的判断，不是新人工真值。 教学例子：两条候选均获同一评分时，不能把先显示的那条写成winner；需要有区分的比较信号才形成该胜负对。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<span id="paper-post-training-self-rewarding-38dd38b1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b295099775e750b6">Self-Rewarding裁判给两条候选相同分数时，能据此断言哪条更受偏好吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aself-rewarding">Self-Rewarding LM</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。同分没有提供严格的优劣关系，不能仅按展示顺序制造一对有方向的偏好。该循环依靠评分差选择优选与拒绝候选，因而生成候选数量和可区分的评价是不同条件。即便得分不同，也只是当前模型裁判的判断，不是新人工真值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两条候选均获同一评分时，不能把先显示的那条写成winner；需要有区分的比较信号才形成该胜负对。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2401.10020">原论文</a> · <a href="../../../../post-training/2401.10020-self-rewarding/">实现解读</a> · <a href="#qa-b295099775e750b6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:self-rewarding" data-paper-title="Self-Rewarding LM" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Self-Rewarding LM LLM 后训练 Meta AI 2024-01-18 每轮由当前模型生成候选并以 LLM-as-a-Judge 打分，形成新的偏好对继续 DPO，构成自举闭环。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.6250（+166.67%）；奖励、KL、长度和候选预算一致。  自奖励 LLM 后训练 偏好与对齐：先看反馈长什么样 Self-Rewarding LM既写答案又当裁判，新增偏好来自哪里，为什么仍可能自我强化错误？ 每轮模型生成候选并以自己的评审能力排序，新偏好再用于下一轮DPO，形成生成与评价共同演化的闭环。新增的是当前模型给出的判断，不是独立人工真值；如果它持续偏爱某种错误风格，迭代可能放大偏差，必须保留外部留出评估。 教学例子：模型总给长解释更高分，即使算术结论错误，也可能把冗长错误答案反复选成优例；外部验证应能打破这种循环。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-154b2587d78b6046">Self-Rewarding LM既写答案又当裁判，新增偏好来自哪里，为什么仍可能自我强化错误？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aself-rewarding">Self-Rewarding LM</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每轮模型生成候选并以自己的评审能力排序，新偏好再用于下一轮DPO，形成生成与评价共同演化的闭环。新增的是当前模型给出的判断，不是独立人工真值；如果它持续偏爱某种错误风格，迭代可能放大偏差，必须保留外部留出评估。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型总给长解释更高分，即使算术结论错误，也可能把冗长错误答案反复选成优例；外部验证应能打破这种循环。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2401.10020">原论文</a> · <a href="../../../../post-training/2401.10020-self-rewarding/">实现解读</a> · <a href="#qa-154b2587d78b6046">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:self-rewarding" data-paper-title="Self-Rewarding LM" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Self-Rewarding LM LLM 后训练 Meta AI 2024-01-18 每轮由当前模型生成候选并以 LLM-as-a-Judge 打分，形成新的偏好对继续 DPO，构成自举闭环。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.6250（+166.67%）；奖励、KL、长度和候选预算一致。  自奖励 LLM 后训练 偏好与对齐：先看反馈长什么样 Self-Rewarding与固定外部奖励模型的关键假设差在哪里？ 固定奖励模型不随策略共同进化，自奖励希望生成与评价能力都能自举改善，但也让错误更可能相互强化。两者比较需独立评估与相同预算，不能以自评分越来越高证明能力越来越好。 例如模型学会讨自己评分规则喜欢，得分可升高，但外部用户未必觉得答案更有用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-64e85cc5effd028f">Self-Rewarding与固定外部奖励模型的关键假设差在哪里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aself-rewarding">Self-Rewarding LM</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定奖励模型不随策略共同进化，自奖励希望生成与评价能力都能自举改善，但也让错误更可能相互强化。两者比较需独立评估与相同预算，不能以自评分越来越高证明能力越来越好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型学会讨自己评分规则喜欢，得分可升高，但外部用户未必觉得答案更有用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2401.10020">原论文</a> · <a href="../../../../post-training/2401.10020-self-rewarding/">实现解读</a> · <a href="#qa-64e85cc5effd028f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:self-rewarding" data-paper-title="Self-Rewarding LM" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Self-Rewarding LM LLM 后训练 Meta AI 2024-01-18 每轮由当前模型生成候选并以 LLM-as-a-Judge 打分，形成新的偏好对继续 DPO，构成自举闭环。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.6250（+166.67%）；奖励、KL、长度和候选预算一致。  自奖励 LLM 后训练 偏好与对齐：先看反馈长什么样 自奖励迭代中的教师轮次与偏好数据应如何留痕？ 记录哪轮策略生成、哪轮裁判评分及选对规则，才能避免把更新后分数倒填旧批次。评估应使用隔离标准；本地只验证循环状态与目标，不包含论文规模裁判质量实验。 例如上一轮模型给候选排序，训练下一轮后不能重算高分再假装它是当初的监督。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7824f1f8ceec3d9a">自奖励迭代中的教师轮次与偏好数据应如何留痕？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aself-rewarding">Self-Rewarding LM</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>记录哪轮策略生成、哪轮裁判评分及选对规则，才能避免把更新后分数倒填旧批次。评估应使用隔离标准；本地只验证循环状态与目标，不包含论文规模裁判质量实验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如上一轮模型给候选排序，训练下一轮后不能重算高分再假装它是当初的监督。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2401.10020">原论文</a> · <a href="../../../../post-training/2401.10020-self-rewarding/">实现解读</a> · <a href="#qa-7824f1f8ceec3d9a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:spin" data-paper-title="SPIN" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="SPIN LLM 后训练 University of California, Los Angeles 2024-01-02 额外偏好标注昂贵。SPIN 从 SFT 模型出发，用上一轮模型为训练 prompt 生成回答，把人类示范视作正例、自生成回答视作负例，通过自博弈判别目标得到下一轮模型，循环提升而不引入新的人工偏好数据。 本页复现“上一轮策略生成负例、人与自生成回答对比、定期刷新对手”的迭代状态，不把 candidate sampling 写成完整 LLM rollout。实现冻结对手、self-play sampling、reference-relative 偏好损失与轮次刷新；没有真实文本生成、分布式训练或论文模型规模。上一轮 candidate policy 负责采样负例，每 16 次更新刷新一次对手。  自博弈微调 LLM 后训练 偏好与对齐：先看反馈长什么样 SPIN没有新增人工偏好数据，正例仍从哪里来？ 它保留既有人类SFT示范为正例，让上一轮模型对同样训练提示生成负例。自博弈改变的是负例分布和参照策略，并非完全不需要人工示范或自动知道所有生成都错。 例如原训练集中已有标准答，模型生成的新答作为对照，未要求人再给这两条排序。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<span id="paper-post-training-spin-6b40abc1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2d79d9ecff10c497">SPIN没有新增人工偏好数据，正例仍从哪里来？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aspin">SPIN</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Los Angeles</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它保留既有人类SFT示范为正例，让上一轮模型对同样训练提示生成负例。自博弈改变的是负例分布和参照策略，并非完全不需要人工示范或自动知道所有生成都错。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如原训练集中已有标准答，模型生成的新答作为对照，未要求人再给这两条排序。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2401.01335">原论文</a> · <a href="../../../../post-training/2401.01335-spin/">实现解读</a> · <a href="#qa-2d79d9ecff10c497">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:spin" data-paper-title="SPIN" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="SPIN LLM 后训练 University of California, Los Angeles 2024-01-02 额外偏好标注昂贵。SPIN 从 SFT 模型出发，用上一轮模型为训练 prompt 生成回答，把人类示范视作正例、自生成回答视作负例，通过自博弈判别目标得到下一轮模型，循环提升而不引入新的人工偏好数据。 本页复现“上一轮策略生成负例、人与自生成回答对比、定期刷新对手”的迭代状态，不把 candidate sampling 写成完整 LLM rollout。实现冻结对手、self-play sampling、reference-relative 偏好损失与轮次刷新；没有真实文本生成、分布式训练或论文模型规模。上一轮 candidate policy 负责采样负例，每 16 次更新刷新一次对手。  自博弈微调 LLM 后训练 偏好与对齐：先看反馈长什么样 SPIN把上一轮模型回答当负例，和让模型自己评出优劣有什么不同？ SPIN的正例来自已有人工示范，负例由上一轮策略生成，通过相对上一轮策略的判别目标训练下一轮。它不依赖同一模型再给候选打出偏好分，更新后还要刷新对手。人工示范仍是监督前提，生成回答也不因此被断言为事实错误。 教学例子：固定一批专家示范，让当前模型为相同问题作答并与示范区分；下一轮重新生成对手回答，而非一直训练同一批旧负例。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c0b13386310cfbca">SPIN把上一轮模型回答当负例，和让模型自己评出优劣有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aspin">SPIN</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Los Angeles</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>SPIN的正例来自已有人工示范，负例由上一轮策略生成，通过相对上一轮策略的判别目标训练下一轮。它不依赖同一模型再给候选打出偏好分，更新后还要刷新对手。人工示范仍是监督前提，生成回答也不因此被断言为事实错误。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>固定一批专家示范，让当前模型为相同问题作答并与示范区分；下一轮重新生成对手回答，而非一直训练同一批旧负例。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2401.01335">原论文</a> · <a href="../../../../post-training/2401.01335-spin/">实现解读</a> · <a href="#qa-c0b13386310cfbca">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:spin" data-paper-title="SPIN" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="SPIN LLM 后训练 University of California, Los Angeles 2024-01-02 额外偏好标注昂贵。SPIN 从 SFT 模型出发，用上一轮模型为训练 prompt 生成回答，把人类示范视作正例、自生成回答视作负例，通过自博弈判别目标得到下一轮模型，循环提升而不引入新的人工偏好数据。 本页复现“上一轮策略生成负例、人与自生成回答对比、定期刷新对手”的迭代状态，不把 candidate sampling 写成完整 LLM rollout。实现冻结对手、self-play sampling、reference-relative 偏好损失与轮次刷新；没有真实文本生成、分布式训练或论文模型规模。上一轮 candidate policy 负责采样负例，每 16 次更新刷新一次对手。  自博弈微调 LLM 后训练 偏好与对齐：先看反馈长什么样 SPIN每轮刷新生成负例，与在同一批人工示范上反复做SFT有什么不同？ 重复SFT主要继续提高固定示范的似然；SPIN让上一轮模型在相同提示下生成新的对照分布，再学习区分示范与当前对手行为。变化的不只是训练轮数，还有负例来源和相对参照，因此不能用多跑几轮SFT代替自博弈迭代。 教学例子：第一轮常见的错误被修正后，下一轮对手会产生不同回答；固定SFT数据本身不会刷新这些对照。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-de51d109d380cea3">SPIN每轮刷新生成负例，与在同一批人工示范上反复做SFT有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aspin">SPIN</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Los Angeles</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>重复SFT主要继续提高固定示范的似然；SPIN让上一轮模型在相同提示下生成新的对照分布，再学习区分示范与当前对手行为。变化的不只是训练轮数，还有负例来源和相对参照，因此不能用多跑几轮SFT代替自博弈迭代。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第一轮常见的错误被修正后，下一轮对手会产生不同回答；固定SFT数据本身不会刷新这些对照。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2401.01335">原论文</a> · <a href="../../../../post-training/2401.01335-spin/">实现解读</a> · <a href="#qa-de51d109d380cea3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:spin" data-paper-title="SPIN" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="SPIN LLM 后训练 University of California, Los Angeles 2024-01-02 额外偏好标注昂贵。SPIN 从 SFT 模型出发，用上一轮模型为训练 prompt 生成回答，把人类示范视作正例、自生成回答视作负例，通过自博弈判别目标得到下一轮模型，循环提升而不引入新的人工偏好数据。 本页复现“上一轮策略生成负例、人与自生成回答对比、定期刷新对手”的迭代状态，不把 candidate sampling 写成完整 LLM rollout。实现冻结对手、self-play sampling、reference-relative 偏好损失与轮次刷新；没有真实文本生成、分布式训练或论文模型规模。上一轮 candidate policy 负责采样负例，每 16 次更新刷新一次对手。  自博弈微调 LLM 后训练 偏好与对齐：先看反馈长什么样 SPIN为什么必须冻结本轮对手并在下一轮刷新？ 损失用上一轮策略作相对参照，采样也来自该对手；本轮训练中随意更新参照会改变目标含义。完成一轮后再刷新，保持生成、评分与更新的轮次一致，本地未做真实文本规模实验。 例如一半批次用旧参照、一半偷偷换新参照，便不是同一轮定义清楚的自博弈更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-68b65f63205056ef">SPIN为什么必须冻结本轮对手并在下一轮刷新？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aspin">SPIN</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Los Angeles</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>损失用上一轮策略作相对参照，采样也来自该对手；本轮训练中随意更新参照会改变目标含义。完成一轮后再刷新，保持生成、评分与更新的轮次一致，本地未做真实文本规模实验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一半批次用旧参照、一半偷偷换新参照，便不是同一轮定义清楚的自博弈更新。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2401.01335">原论文</a> · <a href="../../../../post-training/2401.01335-spin/">实现解读</a> · <a href="#qa-68b65f63205056ef">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ipo" data-paper-title="IPO" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="IPO LLM 后训练 Google DeepMind 2023-10-18 论文指出 RLHF 与 DPO 都依赖将成对偏好转成标量 reward 的假设，并提出直接在偏好概率上优化的 PO 框架。取恒等映射得到 IPO：拟合一个有限的目标间隔，而不是像 logistic loss 一样在训练集可分时持续放大 chosen/rejected 间隔。 用平方回归约束偏好 log-ratio，避免 DPO 在可分数据上把策略推向确定性极端。保留了 tokenizer 级序列概率、自由生成、reference policy 与 IPO 平方目标；本地模型和算术数据用于验证训练机制，不等同于论文的大模型偏好评测。本地用字符 tokenizer、GRU causal LM 和自由生成 numeric verifier。SFT warmup 后，正确 completion 为 chosen，当前 policy rollout 中最低 reward 响应为 rejected，按 token log-probability 实现 reference-relative IPO。  偏好正则 LLM 后训练 偏好与对齐：先看反馈长什么样 IPO目标中的τ变大时，期望偏好间隔会变大还是变小？ 有限目标是1/(2τ)，所以正τ增大时，期望的相对间隔反而缩小。τ不是“优选程度越大”的标注分数，也不能与目标间隔同向理解。这里只说明公式中的控制关系，具体训练效果还取决于数据、策略与优化过程。 教学例子：教学用τ从1变成2，目标由1/2变成1/4；这是目标值演算，不是论文实验指标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<span id="paper-post-training-ipo-127b83ec" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-3ab275343c2f6b76">IPO目标中的τ变大时，期望偏好间隔会变大还是变小？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aipo">IPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>有限目标是1/(2τ)，所以正τ增大时，期望的相对间隔反而缩小。τ不是“优选程度越大”的标注分数，也不能与目标间隔同向理解。这里只说明公式中的控制关系，具体训练效果还取决于数据、策略与优化过程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学用τ从1变成2，目标由1/2变成1/4；这是目标值演算，不是论文实验指标。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2310.12036">原论文</a> · <a href="../../../../post-training/2310.12036-ipo/">实现解读</a> · <a href="#qa-3ab275343c2f6b76">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ipo" data-paper-title="IPO" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="IPO LLM 后训练 Google DeepMind 2023-10-18 论文指出 RLHF 与 DPO 都依赖将成对偏好转成标量 reward 的假设，并提出直接在偏好概率上优化的 PO 框架。取恒等映射得到 IPO：拟合一个有限的目标间隔，而不是像 logistic loss 一样在训练集可分时持续放大 chosen/rejected 间隔。 用平方回归约束偏好 log-ratio，避免 DPO 在可分数据上把策略推向确定性极端。保留了 tokenizer 级序列概率、自由生成、reference policy 与 IPO 平方目标；本地模型和算术数据用于验证训练机制，不等同于论文的大模型偏好评测。本地用字符 tokenizer、GRU causal LM 和自由生成 numeric verifier。SFT warmup 后，正确 completion 为 chosen，当前 policy rollout 中最低 reward 响应为 rejected，按 token log-probability 实现 reference-relative IPO。  偏好正则 LLM 后训练 偏好与对齐：先看反馈长什么样 IPO为什么让偏好gap贴近有限目标，而不是只要chosen越压过rejected越好？ 在可分数据上，logistic式偏好目标可能持续扩大间隔，增加过拟合风险。IPO对相对reference的log-ratio gap做平方拟合，目标由正则参数给出有限值。超过目标后梯度会拉回，因此它改变的是偏好目标形状，不是简单减小学习率。 教学例子：两份回答已被明确区分，继续无限压低拒绝回答未必有益；有限目标会在分离充分时减弱更新，过头时甚至反向校正。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-27d91eff39b627ea">IPO为什么让偏好gap贴近有限目标，而不是只要chosen越压过rejected越好？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aipo">IPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>在可分数据上，logistic式偏好目标可能持续扩大间隔，增加过拟合风险。IPO对相对reference的log-ratio gap做平方拟合，目标由正则参数给出有限值。超过目标后梯度会拉回，因此它改变的是偏好目标形状，不是简单减小学习率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两份回答已被明确区分，继续无限压低拒绝回答未必有益；有限目标会在分离充分时减弱更新，过头时甚至反向校正。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2310.12036">原论文</a> · <a href="../../../../post-training/2310.12036-ipo/">实现解读</a> · <a href="#qa-27d91eff39b627ea">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ipo" data-paper-title="IPO" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="IPO LLM 后训练 Google DeepMind 2023-10-18 论文指出 RLHF 与 DPO 都依赖将成对偏好转成标量 reward 的假设，并提出直接在偏好概率上优化的 PO 框架。取恒等映射得到 IPO：拟合一个有限的目标间隔，而不是像 logistic loss 一样在训练集可分时持续放大 chosen/rejected 间隔。 用平方回归约束偏好 log-ratio，避免 DPO 在可分数据上把策略推向确定性极端。保留了 tokenizer 级序列概率、自由生成、reference policy 与 IPO 平方目标；本地模型和算术数据用于验证训练机制，不等同于论文的大模型偏好评测。本地用字符 tokenizer、GRU causal LM 和自由生成 numeric verifier。SFT warmup 后，正确 completion 为 chosen，当前 policy rollout 中最低 reward 响应为 rejected，按 token log-probability 实现 reference-relative IPO。  偏好正则 LLM 后训练 偏好与对齐：先看反馈长什么样 IPO拟合相对间隔，是否等于要求chosen自身的绝对概率一定上升？ 不等于。间隔比较的是chosen与rejected的策略相对reference对数比之差，可以通过提高chosen、降低rejected或二者共同变化来接近目标。单看chosen绝对概率无法判断目标改善，且完整分布的归一化也会影响其他回答。 教学例子：chosen概率不变而rejected下降，也可能扩大相对间隔；不能仅凭chosen未上升判定本次目标没有变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c593b9604bc999a9">IPO拟合相对间隔，是否等于要求chosen自身的绝对概率一定上升？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aipo">IPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不等于。间隔比较的是chosen与rejected的策略相对reference对数比之差，可以通过提高chosen、降低rejected或二者共同变化来接近目标。单看chosen绝对概率无法判断目标改善，且完整分布的归一化也会影响其他回答。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>chosen概率不变而rejected下降，也可能扩大相对间隔；不能仅凭chosen未上升判定本次目标没有变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2310.12036">原论文</a> · <a href="../../../../post-training/2310.12036-ipo/">实现解读</a> · <a href="#qa-c593b9604bc999a9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ipo" data-paper-title="IPO" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="IPO LLM 后训练 Google DeepMind 2023-10-18 论文指出 RLHF 与 DPO 都依赖将成对偏好转成标量 reward 的假设，并提出直接在偏好概率上优化的 PO 框架。取恒等映射得到 IPO：拟合一个有限的目标间隔，而不是像 logistic loss 一样在训练集可分时持续放大 chosen/rejected 间隔。 用平方回归约束偏好 log-ratio，避免 DPO 在可分数据上把策略推向确定性极端。保留了 tokenizer 级序列概率、自由生成、reference policy 与 IPO 平方目标；本地模型和算术数据用于验证训练机制，不等同于论文的大模型偏好评测。本地用字符 tokenizer、GRU causal LM 和自由生成 numeric verifier。SFT warmup 后，正确 completion 为 chosen，当前 policy rollout 中最低 reward 响应为 rejected，按 token log-probability 实现 reference-relative IPO。  偏好正则 LLM 后训练 偏好与对齐：先看反馈长什么样 IPO的间隔为什么要计算策略与reference的交叉概率比？ 它衡量优选相对拒绝的变化相对参考有多大，而非只看策略两概率差；目标为一除二τ，τ需为正并与协议固定。真实实现还需正确聚合响应词元，不能把参考项漏掉。 例如参考本来就偏爱某种措辞，交叉比能区分继承的偏好与新训练额外引入的变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-90a4386f929b6180">IPO的间隔为什么要计算策略与reference的交叉概率比？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aipo">IPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它衡量优选相对拒绝的变化相对参考有多大，而非只看策略两概率差；目标为一除二τ，τ需为正并与协议固定。真实实现还需正确聚合响应词元，不能把参考项漏掉。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如参考本来就偏爱某种措辞，交叉比能区分继承的偏好与新训练额外引入的变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2310.12036">原论文</a> · <a href="../../../../post-training/2310.12036-ipo/">实现解读</a> · <a href="#qa-90a4386f929b6180">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:steerlm" data-paper-title="SteerLM" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="SteerLM LLM 后训练 NVIDIA 2023-10-09 传统 RLHF 把多维偏好压成一个 reward，用户推理时也不能改变目标。SteerLM 先用 attribute prediction model 为回答标注 helpfulness、quality 等属性，再把属性和值拼入条件做普通 SFT，推理时由用户指定目标属性。 本页复现显式属性标注、目标属性条件选择与 SFT 更新，不把四维本地属性冒充 NVIDIA 43B 模型。保留多维 annotation 与条件 SFT；本地属性来自公开候选数据的确定性 reward axes，没有训练大属性预测器，也未实现真实文本 token 级条件生成。四个 reward axis 作为可审计属性标注，目标属性向量参与响应选择，再执行条件 SFT。  多属性可控 SFT LLM 后训练 偏好与对齐：先看反馈长什么样 SteerLM的属性预测模型与属性条件生成模型，是同一个角色吗？ 两者职责不同：属性预测给已有回答标注helpfulness、quality等维度，生成模型学习在指定属性条件下输出回答。推理时用户提供目标属性，而不是先拿到一份未来答案让属性模型评分后再生成。区分标注器与条件策略，才能看清监督如何进入训练。 教学例子：先给训练回答标“较简洁、较有帮助”，再训练按这些条件生成；上线时输入目标条件并请求新回答。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<span id="paper-post-training-steerlm-863fe2af" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8618eab53654c787">SteerLM的属性预测模型与属性条件生成模型，是同一个角色吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asteerlm">SteerLM</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NVIDIA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两者职责不同：属性预测给已有回答标注helpfulness、quality等维度，生成模型学习在指定属性条件下输出回答。推理时用户提供目标属性，而不是先拿到一份未来答案让属性模型评分后再生成。区分标注器与条件策略，才能看清监督如何进入训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先给训练回答标“较简洁、较有帮助”，再训练按这些条件生成；上线时输入目标条件并请求新回答。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2310.05344">原论文</a> · <a href="../../../../post-training/2310.05344-steerlm/">实现解读</a> · <a href="#qa-8618eab53654c787">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:steerlm" data-paper-title="SteerLM" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="SteerLM LLM 后训练 NVIDIA 2023-10-09 传统 RLHF 把多维偏好压成一个 reward，用户推理时也不能改变目标。SteerLM 先用 attribute prediction model 为回答标注 helpfulness、quality 等属性，再把属性和值拼入条件做普通 SFT，推理时由用户指定目标属性。 本页复现显式属性标注、目标属性条件选择与 SFT 更新，不把四维本地属性冒充 NVIDIA 43B 模型。保留多维 annotation 与条件 SFT；本地属性来自公开候选数据的确定性 reward axes，没有训练大属性预测器，也未实现真实文本 token 级条件生成。四个 reward axis 作为可审计属性标注，目标属性向量参与响应选择，再执行条件 SFT。  多属性可控 SFT LLM 后训练 偏好与对齐：先看反馈长什么样 SteerLM为什么把目标属性作为生成条件，而不只把多个偏好分数合成奖励？ 把属性压成一个标量后，推理时很难重新选择偏好组合。SteerLM先预测回答属性，再做属性条件SFT，使策略学习给定属性下的表达方式，用户可在推理时指定目标。属性标注是否可靠仍是前提，条件可控不代表每项属性都能独立精确满足。 教学例子：同一问题想要“详细但语气克制”或“简短且友好”，可改变条件属性；无需为每种组合都重新训练一个独立奖励策略。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-4a8ee45efddccf43">SteerLM为什么把目标属性作为生成条件，而不只把多个偏好分数合成奖励？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asteerlm">SteerLM</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NVIDIA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>把属性压成一个标量后，推理时很难重新选择偏好组合。SteerLM先预测回答属性，再做属性条件SFT，使策略学习给定属性下的表达方式，用户可在推理时指定目标。属性标注是否可靠仍是前提，条件可控不代表每项属性都能独立精确满足。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一问题想要“详细但语气克制”或“简短且友好”，可改变条件属性；无需为每种组合都重新训练一个独立奖励策略。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2310.05344">原论文</a> · <a href="../../../../post-training/2310.05344-steerlm/">实现解读</a> · <a href="#qa-4a8ee45efddccf43">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:steerlm" data-paper-title="SteerLM" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="SteerLM LLM 后训练 NVIDIA 2023-10-09 传统 RLHF 把多维偏好压成一个 reward，用户推理时也不能改变目标。SteerLM 先用 attribute prediction model 为回答标注 helpfulness、quality 等属性，再把属性和值拼入条件做普通 SFT，推理时由用户指定目标属性。 本页复现显式属性标注、目标属性条件选择与 SFT 更新，不把四维本地属性冒充 NVIDIA 43B 模型。保留多维 annotation 与条件 SFT；本地属性来自公开候选数据的确定性 reward axes，没有训练大属性预测器，也未实现真实文本 token 级条件生成。四个 reward axis 作为可审计属性标注，目标属性向量参与响应选择，再执行条件 SFT。  多属性可控 SFT LLM 后训练 偏好与对齐：先看反馈长什么样 SteerLM与推理时只在提示里说更简洁有什么机制差别？ 属性条件SFT用带标注数据把属性值与回答模式系统关联，临时自然语言要求未必对应同样训练信号。两者可并用，但不能仅因加了属性文本就声称完成属性条件训练。 例如训练时多个简洁等级都有示范，部署指定等级才有明确学习依据，不只是换一句措辞。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-6818c23101e01b24">SteerLM与推理时只在提示里说更简洁有什么机制差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asteerlm">SteerLM</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NVIDIA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>属性条件SFT用带标注数据把属性值与回答模式系统关联，临时自然语言要求未必对应同样训练信号。两者可并用，但不能仅因加了属性文本就声称完成属性条件训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如训练时多个简洁等级都有示范，部署指定等级才有明确学习依据，不只是换一句措辞。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2310.05344">原论文</a> · <a href="../../../../post-training/2310.05344-steerlm/">实现解读</a> · <a href="#qa-6818c23101e01b24">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:steerlm" data-paper-title="SteerLM" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="SteerLM LLM 后训练 NVIDIA 2023-10-09 传统 RLHF 把多维偏好压成一个 reward，用户推理时也不能改变目标。SteerLM 先用 attribute prediction model 为回答标注 helpfulness、quality 等属性，再把属性和值拼入条件做普通 SFT，推理时由用户指定目标属性。 本页复现显式属性标注、目标属性条件选择与 SFT 更新，不把四维本地属性冒充 NVIDIA 43B 模型。保留多维 annotation 与条件 SFT；本地属性来自公开候选数据的确定性 reward axes，没有训练大属性预测器，也未实现真实文本 token 级条件生成。四个 reward axis 作为可审计属性标注，目标属性向量参与响应选择，再执行条件 SFT。  多属性可控 SFT LLM 后训练 偏好与对齐：先看反馈长什么样 SteerLM本地属性标签与原文属性预测模型能混为一谈吗？ 不能。本地用公开候选上的确定性奖励轴形成多维标签，验证条件接口；未训练大型属性预测器，也未实现完整自由文本条件生成。属性向量顺序和值域还需与训练协议一致。 例如把质量与长度两列调换仍可能运行，却会让用户指定的属性含义整个交换。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d29a44f99cbc4fc3">SteerLM本地属性标签与原文属性预测模型能混为一谈吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asteerlm">SteerLM</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NVIDIA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。本地用公开候选上的确定性奖励轴形成多维标签，验证条件接口；未训练大型属性预测器，也未实现完整自由文本条件生成。属性向量顺序和值域还需与训练协议一致。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把质量与长度两列调换仍可能运行，却会让用户指定的属性含义整个交换。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2310.05344">原论文</a> · <a href="../../../../post-training/2310.05344-steerlm/">实现解读</a> · <a href="#qa-d29a44f99cbc4fc3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rlaif" data-paper-title="RLAIF" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="RLAIF LLM 后训练 Google Research 2023-09-01 AI labeler 对候选做顺序交换评判，去除位置偏差后训练 preference policy；本地落实双顺序标签与成对更新。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.6406（+173.33%）；奖励、KL、长度和候选预算一致。  AI 反馈 LLM 后训练 偏好与对齐：先看反馈长什么样 RLAIF替代的是哪部分人工工作？ 主要用AI判断候选偏好，减少逐对人工标注，再据偏好信号训练策略；它不取消评价标准或独立能力评测。AI标签仍可能带位置、风格和知识偏差。 例如人工制定标准后，AI批量比较两篇摘要，而非把AI高分视作客观真理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<span id="paper-post-training-rlaif-a542b4bc" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-04d1061c5a5f15e4">RLAIF替代的是哪部分人工工作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arlaif">RLAIF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>主要用AI判断候选偏好，减少逐对人工标注，再据偏好信号训练策略；它不取消评价标准或独立能力评测。AI标签仍可能带位置、风格和知识偏差。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如人工制定标准后，AI批量比较两篇摘要，而非把AI高分视作客观真理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2309.00267">原论文</a> · <a href="../../../../post-training/2309.00267-rlaif/">实现解读</a> · <a href="#qa-04d1061c5a5f15e4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rlaif" data-paper-title="RLAIF" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="RLAIF LLM 后训练 Google Research 2023-09-01 AI labeler 对候选做顺序交换评判，去除位置偏差后训练 preference policy；本地落实双顺序标签与成对更新。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.6406（+173.33%）；奖励、KL、长度和候选预算一致。  AI 反馈 LLM 后训练 偏好与对齐：先看反馈长什么样 RLAIF为什么把候选交换顺序再判断，交换后的分数能直接平均吗？ AI裁判可能偏爱先出现的候选，因此要交换展示顺序再评价，并把结果映射回同一个候选身份后合并。直接平均不同含义的胜率会抵消真实偏好。这样主要校正位置偏差，不能证明裁判没有风格、事实或价值判断偏差，仍需独立评估。 教学例子：答案甲无论内容都在首位时更易获胜；交换甲乙后，应把第二次的选择还原成“甲胜率”，再比较合并。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-dfd8d3776378be1d">RLAIF为什么把候选交换顺序再判断，交换后的分数能直接平均吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arlaif">RLAIF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>AI裁判可能偏爱先出现的候选，因此要交换展示顺序再评价，并把结果映射回同一个候选身份后合并。直接平均不同含义的胜率会抵消真实偏好。这样主要校正位置偏差，不能证明裁判没有风格、事实或价值判断偏差，仍需独立评估。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>答案甲无论内容都在首位时更易获胜；交换甲乙后，应把第二次的选择还原成“甲胜率”，再比较合并。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2309.00267">原论文</a> · <a href="../../../../post-training/2309.00267-rlaif/">实现解读</a> · <a href="#qa-dfd8d3776378be1d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rlaif" data-paper-title="RLAIF" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="RLAIF LLM 后训练 Google Research 2023-09-01 AI labeler 对候选做顺序交换评判，去除位置偏差后训练 preference policy；本地落实双顺序标签与成对更新。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.6406（+173.33%）；奖励、KL、长度和候选预算一致。  AI 反馈 LLM 后训练 偏好与对齐：先看反馈长什么样 RLAIF用AI偏好训练策略，与推理时让AI从候选中挑一个有什么不同？ 前者把AI判断转成训练数据并更新策略参数，后者只在当前请求上选择，未必产生任何参数学习。两者可能复用类似裁判，但成本发生位置和对后续请求的影响不同；一次候选选择成功不能证明策略已通过RLAIF学会该行为。 教学例子：今天用AI挑中一条回答，只改变今天的展示；将这对偏好用于训练，才可能改变明天的策略分布。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0cc21caa8f68e6b2">RLAIF用AI偏好训练策略，与推理时让AI从候选中挑一个有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arlaif">RLAIF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者把AI判断转成训练数据并更新策略参数，后者只在当前请求上选择，未必产生任何参数学习。两者可能复用类似裁判，但成本发生位置和对后续请求的影响不同；一次候选选择成功不能证明策略已通过RLAIF学会该行为。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>今天用AI挑中一条回答，只改变今天的展示；将这对偏好用于训练，才可能改变明天的策略分布。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2309.00267">原论文</a> · <a href="../../../../post-training/2309.00267-rlaif/">实现解读</a> · <a href="#qa-0cc21caa8f68e6b2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rlaif" data-paper-title="RLAIF" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="RLAIF LLM 后训练 Google Research 2023-09-01 AI labeler 对候选做顺序交换评判，去除位置偏差后训练 preference policy；本地落实双顺序标签与成对更新。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.6406（+173.33%）；奖励、KL、长度和候选预算一致。  AI 反馈 LLM 后训练 偏好与对齐：先看反馈长什么样 本地RLAIF双顺序标签如何避免身份弄反？ 交换输入后应把输出解释回原始候选身份，再组成成对监督。固定标签核只验证这一映射和更新，不包含完整AI裁判与大模型RL训练。 例如第二次说左边更好，此时左边是B，不能仍把分数记到A。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e9950599cb9a6017">本地RLAIF双顺序标签如何避免身份弄反？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arlaif">RLAIF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>交换输入后应把输出解释回原始候选身份，再组成成对监督。固定标签核只验证这一映射和更新，不包含完整AI裁判与大模型RL训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如第二次说左边更好，此时左边是B，不能仍把分数记到A。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2309.00267">原论文</a> · <a href="../../../../post-training/2309.00267-rlaif/">实现解读</a> · <a href="#qa-e9950599cb9a6017">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dpo" data-paper-title="DPO" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="DPO LLM 后训练 Stanford University 2023-05-29 传统 RLHF 先拟合 reward model，再用 PPO 优化策略，链路复杂且不稳定。DPO 从 KL-regularized RLHF 的最优策略形式出发，把隐式 reward 写成 policy 与 reference log-ratio，最终只需在偏好对上做二分类。 本页实现 chosen/rejected 相对 reference policy 的闭式偏好分类目标，不训练显式 reward model，也不进行在线 rollout。实现 DPO 的 reference-relative pairwise loss 与偏好 margin；候选策略可以精确计算整项概率，但没有训练自回归 LLM，也没有复刻 Anthropic HH 或 TL;DR 偏好数据。统一 GSM8K candidate 协议下，每题以 gold candidate 为 chosen、当前最高分错误项为 rejected，并记录 reference-corrected preference margin。  直接偏好优化 LLM 后训练 偏好与对齐：先看反馈长什么样 DPO为什么不必先单独拟合奖励模型？ 它把KL正则下的隐式奖励写成策略相对参考的对数比，再直接用优选拒绝回答对构造分类目标。奖励信息来自偏好数据，并非模型无需监督。 例如已有两答案谁更好的标签，就可计算成对损失，不需额外先训练打分器。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<span id="paper-post-training-dpo-0073c0b6" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5b1bca6549e89038">DPO为什么不必先单独拟合奖励模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adpo">DPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它把KL正则下的隐式奖励写成策略相对参考的对数比，再直接用优选拒绝回答对构造分类目标。奖励信息来自偏好数据，并非模型无需监督。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如已有两答案谁更好的标签，就可计算成对损失，不需额外先训练打分器。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.18290">原论文</a> · <a href="../../../../post-training/2305.18290-dpo/">实现解读</a> · <a href="#qa-5b1bca6549e89038">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dpo" data-paper-title="DPO" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="DPO LLM 后训练 Stanford University 2023-05-29 传统 RLHF 先拟合 reward model，再用 PPO 优化策略，链路复杂且不稳定。DPO 从 KL-regularized RLHF 的最优策略形式出发，把隐式 reward 写成 policy 与 reference log-ratio，最终只需在偏好对上做二分类。 本页实现 chosen/rejected 相对 reference policy 的闭式偏好分类目标，不训练显式 reward model，也不进行在线 rollout。实现 DPO 的 reference-relative pairwise loss 与偏好 margin；候选策略可以精确计算整项概率，但没有训练自回归 LLM，也没有复刻 Anthropic HH 或 TL;DR 偏好数据。统一 GSM8K candidate 协议下，每题以 gold candidate 为 chosen、当前最高分错误项为 rejected，并记录 reference-corrected preference margin。  直接偏好优化 LLM 后训练 偏好与对齐：先看反馈长什么样 DPO为什么比较policy相对reference的变化，而不只比较chosen与rejected的原始概率？ 原始概率差混入了模型训练前的偏好，reference-relative比值关注当前策略相对基准如何重新分配概率。优选与拒绝两项共同进入分类margin，从KL正则化最优策略关系得到可训练目标；无需显式奖励模型，但仍依赖同题偏好数据和固定reference口径。 教学例子：基座原本就极偏爱一句套话。训练时需要区分“原来就高概率”与“偏好监督使其进一步升高”，不能仅看当前分数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f795703a61b6c34c">DPO为什么比较policy相对reference的变化，而不只比较chosen与rejected的原始概率？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adpo">DPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原始概率差混入了模型训练前的偏好，reference-relative比值关注当前策略相对基准如何重新分配概率。优选与拒绝两项共同进入分类margin，从KL正则化最优策略关系得到可训练目标；无需显式奖励模型，但仍依赖同题偏好数据和固定reference口径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>基座原本就极偏爱一句套话。训练时需要区分“原来就高概率”与“偏好监督使其进一步升高”，不能仅看当前分数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.18290">原论文</a> · <a href="../../../../post-training/2305.18290-dpo/">实现解读</a> · <a href="#qa-f795703a61b6c34c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dpo" data-paper-title="DPO" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="DPO LLM 后训练 Stanford University 2023-05-29 传统 RLHF 先拟合 reward model，再用 PPO 优化策略，链路复杂且不稳定。DPO 从 KL-regularized RLHF 的最优策略形式出发，把隐式 reward 写成 policy 与 reference log-ratio，最终只需在偏好对上做二分类。 本页实现 chosen/rejected 相对 reference policy 的闭式偏好分类目标，不训练显式 reward model，也不进行在线 rollout。实现 DPO 的 reference-relative pairwise loss 与偏好 margin；候选策略可以精确计算整项概率，但没有训练自回归 LLM，也没有复刻 Anthropic HH 或 TL;DR 偏好数据。统一 GSM8K candidate 协议下，每题以 gold candidate 为 chosen、当前最高分错误项为 rejected，并记录 reference-corrected preference margin。  直接偏好优化 LLM 后训练 偏好与对齐：先看反馈长什么样 DPO与传统奖励模型加PPO在训练数据流上有何差别？ 经典DPO可直接消费固定偏好对，不需每步在线采样并由奖励模型打分；PPO链路通常包含这些环节。少了环节不代表任何离线偏好都覆盖策略未来访问状态。 例如偏好库没包含某类错误前缀，直接优化固定对不会自动补出它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-fb674fbd601d1a3d">DPO与传统奖励模型加PPO在训练数据流上有何差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adpo">DPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>经典DPO可直接消费固定偏好对，不需每步在线采样并由奖励模型打分；PPO链路通常包含这些环节。少了环节不代表任何离线偏好都覆盖策略未来访问状态。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如偏好库没包含某类错误前缀，直接优化固定对不会自动补出它。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.18290">原论文</a> · <a href="../../../../post-training/2305.18290-dpo/">实现解读</a> · <a href="#qa-fb674fbd601d1a3d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dpo" data-paper-title="DPO" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="DPO LLM 后训练 Stanford University 2023-05-29 传统 RLHF 先拟合 reward model，再用 PPO 优化策略，链路复杂且不稳定。DPO 从 KL-regularized RLHF 的最优策略形式出发，把隐式 reward 写成 policy 与 reference log-ratio，最终只需在偏好对上做二分类。 本页实现 chosen/rejected 相对 reference policy 的闭式偏好分类目标，不训练显式 reward model，也不进行在线 rollout。实现 DPO 的 reference-relative pairwise loss 与偏好 margin；候选策略可以精确计算整项概率，但没有训练自回归 LLM，也没有复刻 Anthropic HH 或 TL;DR 偏好数据。统一 GSM8K candidate 协议下，每题以 gold candidate 为 chosen、当前最高分错误项为 rejected，并记录 reference-corrected preference margin。  直接偏好优化 LLM 后训练 偏好与对齐：先看反馈长什么样 DPO参考模型为什么需要冻结且与响应mask一致？ 参考分布定义相对变化的锚点，若同时更新会改变目标。策略和参考须评价同一响应词元，不能一边含提示或padding、另一边不含，否则margin混入协议差异。 例如只在参考端把题干概率加进来，会把无关输入长度带进偏好间隔。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d9471cd43ba2d2a4">DPO参考模型为什么需要冻结且与响应mask一致？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adpo">DPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>参考分布定义相对变化的锚点，若同时更新会改变目标。策略和参考须评价同一响应词元，不能一边含提示或padding、另一边不含，否则margin混入协议差异。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只在参考端把题干概率加进来，会把无关输入长度带进偏好间隔。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.18290">原论文</a> · <a href="../../../../post-training/2305.18290-dpo/">实现解读</a> · <a href="#qa-d9471cd43ba2d2a4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:slic-hf" data-paper-title="SLiC-HF" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="SLiC-HF LLM 后训练 Google DeepMind 2023-05-17 PPO-RLHF 需要策略、reward 和 value 等多套模型。SLiC-HF 直接要求偏好回答的序列 log-likelihood 高于拒绝回答，并用监督目标限制策略漂移；也能消费为其他模型采集的 off-policy 偏好数据。 GSM8K candidate 512/128、300 steps、seed 42，共享同一未训练策略基线。本页复现“偏好序列 margin 校准 + SFT 正则”目标，不把 candidate policy 写成原论文的 T5-XXL 实验。实现 sequence margin、off-policy preference 标记和参考分布正则；候选项代表完整回答，未训练 T5、独立 ranker，也未复刻 TL;DR 人评。  序列概率校准 LLM 后训练 偏好与对齐：先看反馈长什么样 SLiC-HF为什么把序列校准与监督损失放在一起？ 排序项要求优选响应似然领先拒绝响应，监督项则保留对可信回答的学习，限制只靠压低坏答完成目标。它直接训练生成策略，而非先训练独立奖励模型。 例如既拉开好坏摘要差距，也继续学习可信摘要的实际内容。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<span id="paper-post-training-slic-hf-5def3201" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7c231dcb6386ca8e">SLiC-HF为什么把序列校准与监督损失放在一起？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aslic-hf">SLiC-HF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>排序项要求优选响应似然领先拒绝响应，监督项则保留对可信回答的学习，限制只靠压低坏答完成目标。它直接训练生成策略，而非先训练独立奖励模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如既拉开好坏摘要差距，也继续学习可信摘要的实际内容。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.10425">原论文</a> · <a href="../../../../post-training/2305.10425-slic-hf/">实现解读</a> · <a href="#qa-7c231dcb6386ca8e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:slic-hf" data-paper-title="SLiC-HF" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="SLiC-HF LLM 后训练 Google DeepMind 2023-05-17 PPO-RLHF 需要策略、reward 和 value 等多套模型。SLiC-HF 直接要求偏好回答的序列 log-likelihood 高于拒绝回答，并用监督目标限制策略漂移；也能消费为其他模型采集的 off-policy 偏好数据。 GSM8K candidate 512/128、300 steps、seed 42，共享同一未训练策略基线。本页复现“偏好序列 margin 校准 + SFT 正则”目标，不把 candidate policy 写成原论文的 T5-XXL 实验。实现 sequence margin、off-policy preference 标记和参考分布正则；候选项代表完整回答，未训练 T5、独立 ranker，也未复刻 TL;DR 人评。  序列概率校准 LLM 后训练 偏好与对齐：先看反馈长什么样 SLiC-HF已有偏好margin，为什么还保留监督交叉熵项？ margin约束只要求优选回答比拒绝回答更高，不能单独阻止整体语言分布漂移。监督项继续约束参考回答似然，形成序列概率校准与生成质量的双重约束。它可以使用离策略偏好，但这不意味着采样来源、回答长度和数据覆盖差异都已被消除。 教学例子：把坏答案概率压得更低就能满足排序，却可能连好答案也一起变差；监督项要求策略仍能生成合理的参考回答。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-fc913597b1af1378">SLiC-HF已有偏好margin，为什么还保留监督交叉熵项？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aslic-hf">SLiC-HF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>margin约束只要求优选回答比拒绝回答更高，不能单独阻止整体语言分布漂移。监督项继续约束参考回答似然，形成序列概率校准与生成质量的双重约束。它可以使用离策略偏好，但这不意味着采样来源、回答长度和数据覆盖差异都已被消除。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把坏答案概率压得更低就能满足排序，却可能连好答案也一起变差；监督项要求策略仍能生成合理的参考回答。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.10425">原论文</a> · <a href="../../../../post-training/2305.10425-slic-hf/">实现解读</a> · <a href="#qa-fc913597b1af1378">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:slic-hf" data-paper-title="SLiC-HF" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="SLiC-HF LLM 后训练 Google DeepMind 2023-05-17 PPO-RLHF 需要策略、reward 和 value 等多套模型。SLiC-HF 直接要求偏好回答的序列 log-likelihood 高于拒绝回答，并用监督目标限制策略漂移；也能消费为其他模型采集的 off-policy 偏好数据。 GSM8K candidate 512/128、300 steps、seed 42，共享同一未训练策略基线。本页复现“偏好序列 margin 校准 + SFT 正则”目标，不把 candidate policy 写成原论文的 T5-XXL 实验。实现 sequence margin、off-policy preference 标记和参考分布正则；候选项代表完整回答，未训练 T5、独立 ranker，也未复刻 TL;DR 人评。  序列概率校准 LLM 后训练 偏好与对齐：先看反馈长什么样 SLiC-HF的hinge间隔与DPO相对参考间隔有何差异？ 前者直接约束策略的序列似然差并配监督项，DPO比较策略相对冻结参考的对数比差。约束基准与损失形状不同，不能把两者仅当相同公式换名字。 例如hinge满足所需间隔后可不再增加排序惩罚，而相对基准另有含义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-da985f94e4904b1e">SLiC-HF的hinge间隔与DPO相对参考间隔有何差异？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aslic-hf">SLiC-HF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者直接约束策略的序列似然差并配监督项，DPO比较策略相对冻结参考的对数比差。约束基准与损失形状不同，不能把两者仅当相同公式换名字。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如hinge满足所需间隔后可不再增加排序惩罚，而相对基准另有含义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.10425">原论文</a> · <a href="../../../../post-training/2305.10425-slic-hf/">实现解读</a> · <a href="#qa-da985f94e4904b1e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:slic-hf" data-paper-title="SLiC-HF" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="SLiC-HF LLM 后训练 Google DeepMind 2023-05-17 PPO-RLHF 需要策略、reward 和 value 等多套模型。SLiC-HF 直接要求偏好回答的序列 log-likelihood 高于拒绝回答，并用监督目标限制策略漂移；也能消费为其他模型采集的 off-policy 偏好数据。 GSM8K candidate 512/128、300 steps、seed 42，共享同一未训练策略基线。本页复现“偏好序列 margin 校准 + SFT 正则”目标，不把 candidate policy 写成原论文的 T5-XXL 实验。实现 sequence margin、off-policy preference 标记和参考分布正则；候选项代表完整回答，未训练 T5、独立 ranker，也未复刻 TL;DR 人评。  序列概率校准 LLM 后训练 偏好与对齐：先看反馈长什么样 SLiC-HF为何允许使用其他模型采集的偏好对？ 目标可直接评价固定响应，不要求这些响应由当前策略生成，因此可消费off-policy数据。但须保留来源与同提示配对，本地完整候选核没有复刻T5和人评流程。 例如旧模型生成的两篇摘要也可被当前模型评分，前提是偏好标签仍对应这两篇。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1991e69bbbffe205">SLiC-HF为何允许使用其他模型采集的偏好对？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aslic-hf">SLiC-HF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标可直接评价固定响应，不要求这些响应由当前策略生成，因此可消费off-policy数据。但须保留来源与同提示配对，本地完整候选核没有复刻T5和人评流程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如旧模型生成的两篇摘要也可被当前模型评分，前提是偏好标签仍对应这两篇。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.10425">原论文</a> · <a href="../../../../post-training/2305.10425-slic-hf/">实现解读</a> · <a href="#qa-1991e69bbbffe205">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rrhf" data-paper-title="RRHF" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="RRHF LLM 后训练 Alibaba DAMO Academy 2023-04-11 PPO-RLHF 需要 policy、old policy、reward 和 value 等多模型协同，训练和调参复杂。RRHF 从多个模型或人工答案中采样响应，以 reward 给出完整排序，让模型自身的平均 log-likelihood 顺序与 reward 顺序一致，并对最高质量响应继续做 SFT。 本页实现全候选 reward ordering、response log-probability ranking loss 与 best-response SFT，不把它简化成单个 chosen/rejected 的 DPO。保留全排序 hinge 与 best-response SFT；候选 log-probability 是可审计策略概率，没有训练 7B LLaMA，也没有复刻 HH 数据生成、外部 reward model 或人工评价。公开 GSM8K candidate 512/128、300 steps、seed 42；每组 6 个响应均进入 reward 排序和违序 pair 统计。  全排序偏好 LLM 后训练 偏好与对齐：先看反馈长什么样 RRHF为什么利用同题多个响应的完整排序？ 多来源回答提供比单个优选对更丰富的相对关系，模型平均对数似然应与奖励顺序一致，同时对最好回答做监督学习。排序质量仍受奖励或人工标注限制。 例如好、中、差三条解答包含多组顺序，不只是一对胜负。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<span id="paper-post-training-rrhf-c28f5ad3" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-25f8a4e90ddf8a40">RRHF为什么利用同题多个响应的完整排序？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arrhf">RRHF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba DAMO Academy</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多来源回答提供比单个优选对更丰富的相对关系，模型平均对数似然应与奖励顺序一致，同时对最好回答做监督学习。排序质量仍受奖励或人工标注限制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如好、中、差三条解答包含多组顺序，不只是一对胜负。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2304.05302">原论文</a> · <a href="../../../../post-training/2304.05302-rrhf/">实现解读</a> · <a href="#qa-25f8a4e90ddf8a40">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rrhf" data-paper-title="RRHF" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="RRHF LLM 后训练 Alibaba DAMO Academy 2023-04-11 PPO-RLHF 需要 policy、old policy、reward 和 value 等多模型协同，训练和调参复杂。RRHF 从多个模型或人工答案中采样响应，以 reward 给出完整排序，让模型自身的平均 log-likelihood 顺序与 reward 顺序一致，并对最高质量响应继续做 SFT。 本页实现全候选 reward ordering、response log-probability ranking loss 与 best-response SFT，不把它简化成单个 chosen/rejected 的 DPO。保留全排序 hinge 与 best-response SFT；候选 log-probability 是可审计策略概率，没有训练 7B LLaMA，也没有复刻 HH 数据生成、外部 reward model 或人工评价。公开 GSM8K candidate 512/128、300 steps、seed 42；每组 6 个响应均进入 reward 排序和违序 pair 统计。  全排序偏好 LLM 后训练 偏好与对齐：先看反馈长什么样 RRHF已经按奖励给多个回答排序，为什么仍对最佳回答做SFT？ 排序hinge只修正概率顺序冲突，顺序正确后可能不给强的生成学习信号。最佳回答SFT继续提高高质量内容的似然，两者分别承担相对排序与具体模仿。奖励排序来自外部评价，长度归一化也只是分数口径，不能保证最高奖励必然事实正确。 教学例子：三个答案已按优劣排对，但优质答案生成概率仍很低；排序项可能停下，最佳答案的监督项仍可继续提升它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c84c0f92798e6391">RRHF已经按奖励给多个回答排序，为什么仍对最佳回答做SFT？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arrhf">RRHF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba DAMO Academy</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>排序hinge只修正概率顺序冲突，顺序正确后可能不给强的生成学习信号。最佳回答SFT继续提高高质量内容的似然，两者分别承担相对排序与具体模仿。奖励排序来自外部评价，长度归一化也只是分数口径，不能保证最高奖励必然事实正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三个答案已按优劣排对，但优质答案生成概率仍很低；排序项可能停下，最佳答案的监督项仍可继续提升它。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2304.05302">原论文</a> · <a href="../../../../post-training/2304.05302-rrhf/">实现解读</a> · <a href="#qa-c84c0f92798e6391">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rrhf" data-paper-title="RRHF" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="RRHF LLM 后训练 Alibaba DAMO Academy 2023-04-11 PPO-RLHF 需要 policy、old policy、reward 和 value 等多模型协同，训练和调参复杂。RRHF 从多个模型或人工答案中采样响应，以 reward 给出完整排序，让模型自身的平均 log-likelihood 顺序与 reward 顺序一致，并对最高质量响应继续做 SFT。 本页实现全候选 reward ordering、response log-probability ranking loss 与 best-response SFT，不把它简化成单个 chosen/rejected 的 DPO。保留全排序 hinge 与 best-response SFT；候选 log-probability 是可审计策略概率，没有训练 7B LLaMA，也没有复刻 HH 数据生成、外部 reward model 或人工评价。公开 GSM8K candidate 512/128、300 steps、seed 42；每组 6 个响应均进入 reward 排序和违序 pair 统计。  全排序偏好 LLM 后训练 偏好与对齐：先看反馈长什么样 RRHF的best-response SFT与只做排序损失分别贡献什么？ 排序损失纠正响应相对次序，SFT直接提升最好响应的似然。只排序可能通过压低其他响应完成要求，二者组合兼顾相对关系与正向学习，不据此宣称通用最优。 例如好答比坏答高还不够，还希望好答本身被模型学会。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5870e025a2c47fef">RRHF的best-response SFT与只做排序损失分别贡献什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arrhf">RRHF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba DAMO Academy</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>排序损失纠正响应相对次序，SFT直接提升最好响应的似然。只排序可能通过压低其他响应完成要求，二者组合兼顾相对关系与正向学习，不据此宣称通用最优。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如好答比坏答高还不够，还希望好答本身被模型学会。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2304.05302">原论文</a> · <a href="../../../../post-training/2304.05302-rrhf/">实现解读</a> · <a href="#qa-5870e025a2c47fef">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rrhf" data-paper-title="RRHF" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="RRHF LLM 后训练 Alibaba DAMO Academy 2023-04-11 PPO-RLHF 需要 policy、old policy、reward 和 value 等多模型协同，训练和调参复杂。RRHF 从多个模型或人工答案中采样响应，以 reward 给出完整排序，让模型自身的平均 log-likelihood 顺序与 reward 顺序一致，并对最高质量响应继续做 SFT。 本页实现全候选 reward ordering、response log-probability ranking loss 与 best-response SFT，不把它简化成单个 chosen/rejected 的 DPO。保留全排序 hinge 与 best-response SFT；候选 log-probability 是可审计策略概率，没有训练 7B LLaMA，也没有复刻 HH 数据生成、外部 reward model 或人工评价。公开 GSM8K candidate 512/128、300 steps、seed 42；每组 6 个响应均进入 reward 排序和违序 pair 统计。  全排序偏好 LLM 后训练 偏好与对齐：先看反馈长什么样 RRHF里的p_i为什么不能误当原始概率？ 这里是响应长度归一后的log-probability，hinge比较它们的次序。实现需按同一提示组成关系集合并保持reward方向一致，本地候选概率不是完整7B训练。 例如把小数概率直接替代平均logp，会改变间隔大小及更新形状。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-5bdec3da01bf0a15">RRHF里的p_i为什么不能误当原始概率？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arrhf">RRHF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba DAMO Academy</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这里是响应长度归一后的log-probability，hinge比较它们的次序。实现需按同一提示组成关系集合并保持reward方向一致，本地候选概率不是完整7B训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把小数概率直接替代平均logp，会改变间隔大小及更新形状。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2304.05302">原论文</a> · <a href="../../../../post-training/2304.05302-rrhf/">实现解读</a> · <a href="#qa-5bdec3da01bf0a15">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:constitutional-ai" data-paper-title="Constitutional AI" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Constitutional AI LLM 后训练 Anthropic 2022-12-15 人工逐条标注有害回答成本高，而且价值规范不透明。论文把人类监督压缩成一组自然语言原则：第一阶段让模型依据原则批评并重写自己的回答，再对修订回答做 SFT；第二阶段让 AI 比较回答、训练 preference model，并以该奖励执行 RLAIF。 GSM8K 的原则维度是正确性、格式、过程和简洁性，不是安全红队数据，也未训练独立 preference model 或执行大模型 PPO。本页复现“自我批评与修订 → 修订样本 SFT → AI 偏好 RLAIF”两阶段机制；本地 candidate policy 不冒充 Anthropic 原始大模型安全训练。实现显式原则打分、自我修订 SFT 和 AI preference ranking 的状态更新；GSM8K 的原则维度是正确性、格式、过程和简洁性，不是安全红队数据，也未训练独立 preference model 或执行大模型 PPO。  AI 反馈安全对齐 LLM 后训练 偏好与对齐：先看反馈长什么样 Constitutional AI中的constitution承担什么角色？ 它把人类规范显式写成自然语言原则，指导批评、重写与AI偏好判断；原则是监督来源，不是模型自行发现的绝对价值标准。 例如用明确原则解释为何重写回答，而非仅给一个没有依据的好坏分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<span id="paper-post-training-constitutional-ai-8d3916b0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-3a349cd4a2fb2d2f">Constitutional AI中的constitution承担什么角色？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aconstitutional-ai">Constitutional AI</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Anthropic</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它把人类规范显式写成自然语言原则，指导批评、重写与AI偏好判断；原则是监督来源，不是模型自行发现的绝对价值标准。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用明确原则解释为何重写回答，而非仅给一个没有依据的好坏分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2212.08073">原论文</a> · <a href="../../../../post-training/2212.08073-constitutional-ai/">实现解读</a> · <a href="#qa-3a349cd4a2fb2d2f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:constitutional-ai" data-paper-title="Constitutional AI" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Constitutional AI LLM 后训练 Anthropic 2022-12-15 人工逐条标注有害回答成本高，而且价值规范不透明。论文把人类监督压缩成一组自然语言原则：第一阶段让模型依据原则批评并重写自己的回答，再对修订回答做 SFT；第二阶段让 AI 比较回答、训练 preference model，并以该奖励执行 RLAIF。 GSM8K 的原则维度是正确性、格式、过程和简洁性，不是安全红队数据，也未训练独立 preference model 或执行大模型 PPO。本页复现“自我批评与修订 → 修订样本 SFT → AI 偏好 RLAIF”两阶段机制；本地 candidate policy 不冒充 Anthropic 原始大模型安全训练。实现显式原则打分、自我修订 SFT 和 AI preference ranking 的状态更新；GSM8K 的原则维度是正确性、格式、过程和简洁性，不是安全红队数据，也未训练独立 preference model 或执行大模型 PPO。  AI 反馈安全对齐 LLM 后训练 偏好与对齐：先看反馈长什么样 Constitutional AI的原则批评与AI偏好训练，为什么是两个不同阶段？ 第一阶段依据原则批评并修订回答，再用修订文本做监督训练；第二阶段用原则指导回答间比较，学习偏好并用于强化学习。前者提供改写示范，后者提供选择信号。原则文本并不自动保证无害性，本地原则打分或状态更新也不等于完整安全红队训练。 教学例子：先按“不泄露隐私”原则改写一份回答，再比较两种改写哪个更合适；改写文本与二选一标签不是同一种训练输入。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c8b07171181a7608">Constitutional AI的原则批评与AI偏好训练，为什么是两个不同阶段？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aconstitutional-ai">Constitutional AI</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Anthropic</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>第一阶段依据原则批评并修订回答，再用修订文本做监督训练；第二阶段用原则指导回答间比较，学习偏好并用于强化学习。前者提供改写示范，后者提供选择信号。原则文本并不自动保证无害性，本地原则打分或状态更新也不等于完整安全红队训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先按“不泄露隐私”原则改写一份回答，再比较两种改写哪个更合适；改写文本与二选一标签不是同一种训练输入。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2212.08073">原论文</a> · <a href="../../../../post-training/2212.08073-constitutional-ai/">实现解读</a> · <a href="#qa-c8b07171181a7608">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:constitutional-ai" data-paper-title="Constitutional AI" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Constitutional AI LLM 后训练 Anthropic 2022-12-15 人工逐条标注有害回答成本高，而且价值规范不透明。论文把人类监督压缩成一组自然语言原则：第一阶段让模型依据原则批评并重写自己的回答，再对修订回答做 SFT；第二阶段让 AI 比较回答、训练 preference model，并以该奖励执行 RLAIF。 GSM8K 的原则维度是正确性、格式、过程和简洁性，不是安全红队数据，也未训练独立 preference model 或执行大模型 PPO。本页复现“自我批评与修订 → 修订样本 SFT → AI 偏好 RLAIF”两阶段机制；本地 candidate policy 不冒充 Anthropic 原始大模型安全训练。实现显式原则打分、自我修订 SFT 和 AI preference ranking 的状态更新；GSM8K 的原则维度是正确性、格式、过程和简洁性，不是安全红队数据，也未训练独立 preference model 或执行大模型 PPO。  AI 反馈安全对齐 LLM 后训练 偏好与对齐：先看反馈长什么样 按原则自我修订SFT与RLAIF阶段为何不能混为一个目标？ 前者学习修订文本，后者利用AI偏好训练奖励并优化策略，数据和执行环节不同。本地简化组合不能证明独立偏好模型及PPO已执行，也不能把算术原则当安全红队证据。 例如修好一条回答只构成监督样本，不自动等于完成奖励驱动强化学习。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0d13ae16bfabf670">按原则自我修订SFT与RLAIF阶段为何不能混为一个目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aconstitutional-ai">Constitutional AI</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Anthropic</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者学习修订文本，后者利用AI偏好训练奖励并优化策略，数据和执行环节不同。本地简化组合不能证明独立偏好模型及PPO已执行，也不能把算术原则当安全红队证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如修好一条回答只构成监督样本，不自动等于完成奖励驱动强化学习。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2212.08073">原论文</a> · <a href="../../../../post-training/2212.08073-constitutional-ai/">实现解读</a> · <a href="#qa-0d13ae16bfabf670">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:constitutional-ai" data-paper-title="Constitutional AI" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/preference-and-alignment" data-search="Constitutional AI LLM 后训练 Anthropic 2022-12-15 人工逐条标注有害回答成本高，而且价值规范不透明。论文把人类监督压缩成一组自然语言原则：第一阶段让模型依据原则批评并重写自己的回答，再对修订回答做 SFT；第二阶段让 AI 比较回答、训练 preference model，并以该奖励执行 RLAIF。 GSM8K 的原则维度是正确性、格式、过程和简洁性，不是安全红队数据，也未训练独立 preference model 或执行大模型 PPO。本页复现“自我批评与修订 → 修订样本 SFT → AI 偏好 RLAIF”两阶段机制；本地 candidate policy 不冒充 Anthropic 原始大模型安全训练。实现显式原则打分、自我修订 SFT 和 AI preference ranking 的状态更新；GSM8K 的原则维度是正确性、格式、过程和简洁性，不是安全红队数据，也未训练独立 preference model 或执行大模型 PPO。  AI 反馈安全对齐 LLM 后训练 偏好与对齐：先看反馈长什么样 本地Constitutional AI的原则维度与安全能力有什么边界？ 本地使用正确性、格式、过程和简洁性等确定性轴，验证原则评分与状态更新。它们不覆盖真实有害请求，也未训练完整安全奖励模型，不能报告为无害性提升。 例如格式规范通过，只能说明输出格式，不能推出危险建议已被可靠拒绝。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 偏好与对齐：先看反馈长什么样</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-2199338594cbccc3">本地Constitutional AI的原则维度与安全能力有什么边界？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aconstitutional-ai">Constitutional AI</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Anthropic</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>本地使用正确性、格式、过程和简洁性等确定性轴，验证原则评分与状态更新。它们不覆盖真实有害请求，也未训练完整安全奖励模型，不能报告为无害性提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如格式规范通过，只能说明输出格式，不能推出危险建议已被可靠拒绝。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2212.08073">原论文</a> · <a href="../../../../post-training/2212.08073-constitutional-ai/">实现解读</a> · <a href="#qa-2199338594cbccc3">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

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

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
