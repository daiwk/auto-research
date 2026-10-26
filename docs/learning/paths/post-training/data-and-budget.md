---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 数据与预算：下一份算力花在哪里

[LLM 后训练](index.md) / 38 个问题 · 38 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">38 个问题 · 38 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ask-to-distill" data-paper-title="Ask to Distill: Learning to Synthesize Data for On-Policy Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Ask to Distill: Learning to Synthesize Data for On-Policy Distillation LLM 后训练 University of Illinois Urbana-Champaign 2026-10-20 问题决定学生会走到哪些前缀，因而决定教师能提供什么监督。A2D 冻结评分用的师生，训练独立的问题合成器；奖励同时要求“有差异”和“教师偏好的候选仍落在学生可达支持集”，然后筛选问题库，再从原始学生初始化执行 OPD。不是给每道问题做一次学生微调来估价。 完整实验成本过高，不复现（审查 DONE）。三 seed 仍只是机制诊断。仅实现 L1 奖励与更新公式组件，不是完整合成数据系统或能力复现。diagnostic_only=true；不可晋级、未接入 Evolve。完整实验成本过高，不复现（审查 DONE）。本页属于 10 月 21 日同一公告的补审，不是上一批之后的新首发。无下载、无预训练模型调用。随机生成的 logits、显式 mask 和外部 cluster share 只检查公式，不生成自然语言问题。CPU/CUDA 都运行同一算子；CUDA 不可用报错，不回退。输出不可覆盖，最多三个 seed；三 seed 仍只是机制诊断。  On-policy distillation 蒸馏数据合成与筛选 LLM 后训练 数据与预算：下一份算力花在哪里 A2D为什么既要求师生分歧大，又要求教师偏好落在学生可达支持集？ 只有分歧可能选到学生完全学不动的问题，只有兼容性又可能选到已掌握的问题。A2D用差异与兼容性的乘积奖励问题合成器；兼容性取教师在学生候选上的原始概率质量，不能重新归一化抹掉不可达部分。评分师生冻结，下游再从原始学生开始蒸馏。 例如学生会两种基本解法，教师还知道一种相近改进，问题有学习空间；若教师几乎只支持学生完全采不到的路线，兼容性应低。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-ask-to-distill-6c38407f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-fdbf7cacadf7e6e0">A2D为什么既要求师生分歧大，又要求教师偏好落在学生可达支持集？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aask-to-distill">Ask to Distill: Learning to Synthesize Data for On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只有分歧可能选到学生完全学不动的问题，只有兼容性又可能选到已掌握的问题。A2D用差异与兼容性的乘积奖励问题合成器；兼容性取教师在学生候选上的原始概率质量，不能重新归一化抹掉不可达部分。评分师生冻结，下游再从原始学生开始蒸馏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生会两种基本解法，教师还知道一种相近改进，问题有学习空间；若教师几乎只支持学生完全采不到的路线，兼容性应低。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.27450v1">原论文</a> · <a href="../../../../post-training/2610.27450-ask-to-distill/">实现解读</a> · <a href="#qa-fdbf7cacadf7e6e0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tar-adaptive-replay" data-paper-title="Preserving Reasoning Diversity in Reinforcement Learning with Verifiable Rewards via Adaptive Replay" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Preserving Reasoning Diversity in Reinforcement Learning with Verifiable Rewards via Adaptive Replay LLM 后训练 Cornell University 2026-10-16 有限on-policy采样可能逐步压低同样正确但较少出现的推理模式；仅在当前rollout上重加权，难以恢复已经采不到的模式。TAR先从基础策略大量生成，过滤正确回答，再保留分散的原型轨迹。训练时只重放相对base已经被压制的轨迹，并将梯度集中到其中被压制的token，避免始终模仿有限bank限制策略适应。原文§3–4 原图建议：Figure 3压制比例与gated replay loss的机制分析图；原文未提供完整架构图，以上Mermaid是方法重绘，不冒充原图。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是数学推理或语义多样性复现。L1 定义性组件／梯度诊断，不是数学推理或语义多样性复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接Evolve。随机初始化16词表、8维GRU，base为当前初始策略的冻结副本。每个公开prompt实际采8个回答，外部合成verifier检查后，在base真实隐状态上做FPS并保留至多3条；未用gold、模板答案或手写候选填充bank。该随机初始隐状态不是语义encoder，只能验证FPS的定义，不能说明语义推理模式覆盖。  RLVR 多样性与经验重放 后训练算法组件 LLM 后训练 数据与预算：下一份算力花在哪里 TAR为什么只重放相对基础策略被压制的正确轨迹，而不是固定模仿整个记忆库？ 基础策略实际采样并经训练验证器筛出的正确轨迹用于保存多样解法。当前策略若未压低某条轨迹，其门控可以为零；若发生压制，再把损失集中到被压低的词元。轨迹门与词元权重都停止梯度，避免优化器通过改变门控取巧，测试答案不参与建库。 例如旧策略的代数解法逐渐采不到时才补学其中受压步骤；仍常见的图解轨迹无需重复强制模仿，也不能手编答案冒充旧采样。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-tar-adaptive-replay-2e44ae67" class="ar-learning-paper-anchor"></span>
<h2 id="qa-ebca3f0a5ff34c64">TAR为什么只重放相对基础策略被压制的正确轨迹，而不是固定模仿整个记忆库？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atar-adaptive-replay">Preserving Reasoning Diversity in Reinforcement Learning with Verifiable Rewards via Adaptive Replay</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Cornell University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>基础策略实际采样并经训练验证器筛出的正确轨迹用于保存多样解法。当前策略若未压低某条轨迹，其门控可以为零；若发生压制，再把损失集中到被压低的词元。轨迹门与词元权重都停止梯度，避免优化器通过改变门控取巧，测试答案不参与建库。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如旧策略的代数解法逐渐采不到时才补学其中受压步骤；仍常见的图解轨迹无需重复强制模仿，也不能手编答案冒充旧采样。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24236v1">原论文</a> · <a href="../../../../post-training/2610.24236-tar-adaptive-replay/">实现解读</a> · <a href="#qa-ebca3f0a5ff34c64">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:stopd" data-paper-title="Does On-Policy Distillation Need to Complete Every Rollout?" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Does On-Policy Distillation Need to Complete Every Rollout? LLM 后训练 Cornell University 2026-10-15 每条响应在生成之前独立采样 anchor，向上取整到 block 末尾，学生只生成到该 cutoff 或自然 EOS。保留的每个 token 都接收教师监督，并按其精确 inclusion probability 加权；自然 EOS 也是普通有效 token。若把截断结果直接除以本批随机 token 数，不能沿用无偏 gradient-sum 的论证，所以实现使用前一批加权 token count。 完整长 rollout 训练成本过高，不复现（审查 DONE）；L1 cutoff / IPW / lagged normalizer 组件，真实短策略更新。完整长 rollout 训练成本过高，不复现（审查 DONE）；不是固定前缀截断的改名。固定公开 Hamlet 1524，revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784；byte 范围 80%/10%/10% 隔离。微型教师 next-token 训练后冻结，学生真实在线生成；  On-policy distillation 后训练算法组件 STOPD LLM 后训练 数据与预算：下一份算力花在哪里 STOPD按截断位置的逆概率加权，为什么还不能用本批随机词元数直接归一化？ 预先随机截断使后面词元更少被观测，精确纳入概率的倒数可校正梯度和。但随机分子再除以同批随机分母，并不自动保持无偏。方法使用前批的加权计数作当前归一量，权重和分母不参与微分；结论也不是每次优化器更新都等于完整生成。 例如后段步骤只有部分截断计划能保留，应增加其权重；但不能因此宣称一次短生成的平均损失必定与完整长回答相同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-stopd-818867f2" class="ar-learning-paper-anchor"></span>
<h2 id="qa-986fe23827dbb58a">STOPD按截断位置的逆概率加权，为什么还不能用本批随机词元数直接归一化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Astopd">Does On-Policy Distillation Need to Complete Every Rollout?</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Cornell University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>预先随机截断使后面词元更少被观测，精确纳入概率的倒数可校正梯度和。但随机分子再除以同批随机分母，并不自动保持无偏。方法使用前批的加权计数作当前归一量，权重和分母不参与微分；结论也不是每次优化器更新都等于完整生成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如后段步骤只有部分截断计划能保留，应增加其权重；但不能因此宣称一次短生成的平均损失必定与完整长回答相同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21337v1">原论文</a> · <a href="../../../../post-training/2610.21337-stopd/">实现解读</a> · <a href="#qa-986fe23827dbb58a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:boundary-evo" data-paper-title="BoundaryEvo: Data-Model Co-Evolution at the Capability Boundary for Long-Chain Reasoning Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="BoundaryEvo: Data-Model Co-Evolution at the Capability Boundary for Long-Chain Reasoning Distillation LLM 后训练 Shanghai Artificial Intelligence Laboratory 2026-10-09 长推理监督的价值随学生能力变化。BoundaryEvo 先不按 correctness 过滤地蒸馏少量教师行为做 capability priming，然后每轮用当前学生、固定 expert 和 analyzer 重估边界，保留仍未掌握的 replay 并补充新问题；选好问题后再生成并验证 fresh teacher trajectories。 短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：正式对照设计尚未执行；计划以相同学生的 teacher-primed checkpoint 为基线，边界筛选后 fresh teacher 轨迹 SFT 为实验组。本次只有短预算机制诊断，本短跑稳定相对提升不适用，不报告能力收益；空边界或无 Stage 2 更新保留失败。  Capability boundary Data-model co-evolution Reasoning distillation LLM 后训练 数据与预算：下一份算力花在哪里 BoundaryEvo为什么先选能力边界问题，再重新生成并验证教师轨迹？ 问题是否值得学取决于当前学生与专家的差距，旧问题也需重新检查；确定问题后生成新教师轨迹并独立验证，可避免把旧错误答案跟随问题一起重用。初始行为预热与后续验证监督具有不同过滤规则，不能把预热未验答案宣传成正确标签。 例如学生已经学会某个分解题，就不必永久重放；新边界题即使问题合理，也要重新核验教师解法，不能沿用未经检查的旧稿。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-boundary-evo-60ecea39" class="ar-learning-paper-anchor"></span>
<h2 id="qa-e7fd17e9fc0128f5">BoundaryEvo为什么先选能力边界问题，再重新生成并验证教师轨迹？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aboundary-evo">BoundaryEvo: Data-Model Co-Evolution at the Capability Boundary for Long-Chain Reasoning Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Artificial Intelligence Laboratory</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>问题是否值得学取决于当前学生与专家的差距，旧问题也需重新检查；确定问题后生成新教师轨迹并独立验证，可避免把旧错误答案跟随问题一起重用。初始行为预热与后续验证监督具有不同过滤规则，不能把预热未验答案宣传成正确标签。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生已经学会某个分解题，就不必永久重放；新边界题即使问题合理，也要重新核验教师解法，不能沿用未经检查的旧稿。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13285">原论文</a> · <a href="../../../../reproductions/2610.13285-boundary-evo/">实现解读</a> · <a href="#qa-e7fd17e9fc0128f5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:branch-opd" data-paper-title="Branching On-Policy Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Branching On-Policy Distillation LLM 后训练 Tsinghua University / SenseTime Research 2026-10-09 普通 OPD 每个前缀只看到一次后续。BranchOPD 用学生不确定性和师生分歧定位 fork，从同一冻结学生策略独立采样 suffix，前缀只计入一次；并用协议事件监督结束行为。分枝不是教师强制 token，也不按答案正确性筛选。 短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：计划基线为相同学生的单轨 OPD，实验组执行 student 分枝采样、teacher 计分与 PBR；本次没有实跑同预算基线，稳定相对提升不适用。  On-policy distillation Student-policy branching Protocol-boundary repair LLM 后训练 数据与预算：下一份算力花在哪里 BranchOPD从同一前缀分枝时，为什么前缀只应计算一次损失？ 分枝增加的是同一学生状态下的多种后续，若每条分枝都重复计算共享前缀，会无意放大早期词元权重。方法按不确定性与师生分歧选分叉，从冻结学生独立采样续写，再由教师评分；它不是教师强制续写，也不按答案正确性预筛分枝。 例如共享三步推理后生成两种续解，共享三步只记一次，两条后续各自受监督；否则增加分枝会顺带加重无关前文。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-branch-opd-974c9738" class="ar-learning-paper-anchor"></span>
<h2 id="qa-6570a1154693895c">BranchOPD从同一前缀分枝时，为什么前缀只应计算一次损失？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Abranch-opd">Branching On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University / SenseTime Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分枝增加的是同一学生状态下的多种后续，若每条分枝都重复计算共享前缀，会无意放大早期词元权重。方法按不确定性与师生分歧选分叉，从冻结学生独立采样续写，再由教师评分；它不是教师强制续写，也不按答案正确性预筛分枝。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如共享三步推理后生成两种续解，共享三步只记一次，两条后续各自受监督；否则增加分枝会顺带加重无关前文。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13481">原论文</a> · <a href="../../../../reproductions/2610.13481-branch-opd/">实现解读</a> · <a href="#qa-6570a1154693895c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:grpo-difficulty-curriculum" data-paper-title="A Step Harder, Not a Step Too Far: The Benefits and Limits of Curriculum Difficulty Progression in GRPO" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="A Step Harder, Not a Step Too Far: The Benefits and Limits of Curriculum Difficulty Progression in GRPO LLM 后训练 Dalian Maritime University 2026-10-09 difficulty随当前policy变化，样本可能反复进出难度带。论文比较静态easy-to-hard、在线fixed-medium和B1→B5课程，进一步升到B5会退化。实现每步真实rollout重新估难、保留B5控制，不按problem长度或旧评分替代。 本次不复现原文完整B1→B5课程或B5退化。staged缩放成每步validation诊断，保持噪声容忍/恢复best checkpoint；本地对照口径：基线为相同checkpoint与配置的unfiltered、fixed-medium、static、staged、B5-too-hard；按实际effective-update/rollout预算解释；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  GRPO difficulty curriculum Current-policy recalibration Overly-hard degradation control LLM 后训练 数据与预算：下一份算力花在哪里 GRPO难度课程为什么要随当前策略重测成功率，而不能按题目长度固定分级？ 难度取决于当前策略和采样预算，同一道题会随学习进出目标成功率区间。课程用真实生成的成功率分带，阶段选择依赖验证集；越往难处推进并不保证更好，因此还需要最难阶段对照。长度奖励是辅助目标，不能代替难度估计或用测试表现决定推进。 例如短算术题可能恰好是当前模型弱项，长题反而熟练；课程应依据当前多次解答是否成功，而不是字符串长短。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-grpo-difficulty-curriculum-3b9ce14e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-ff387fdac665f742">GRPO难度课程为什么要随当前策略重测成功率，而不能按题目长度固定分级？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agrpo-difficulty-curriculum">A Step Harder, Not a Step Too Far: The Benefits and Limits of Curriculum Difficulty Progression in GRPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dalian Maritime University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>难度取决于当前策略和采样预算，同一道题会随学习进出目标成功率区间。课程用真实生成的成功率分带，阶段选择依赖验证集；越往难处推进并不保证更好，因此还需要最难阶段对照。长度奖励是辅助目标，不能代替难度估计或用测试表现决定推进。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如短算术题可能恰好是当前模型弱项，长题反而熟练；课程应依据当前多次解答是否成功，而不是字符串长短。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13669">原论文</a> · <a href="../../../../reproductions/2610.13669-grpo-difficulty-curriculum/">实现解读</a> · <a href="#qa-ff387fdac665f742">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:progressive-contraction" data-paper-title="Learning More by Training Less: Uncertainty-Guided Progressive Contraction for Efficient Reasoning Post-Training" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Learning More by Training Less: Uncertainty-Guided Progressive Contraction for Efficient Reasoning Post-Training LLM 后训练 National University of Singapore / Nanjing University 2026-10-09 正确teacher CoT也可能经过多种正确/错误后续的reasoning fork。论文对真实prefix做Monte Carlo continuation，按branch不确定性先收缩teacher pool，再经真实student probing epoch按当前NLL选top-M并重路由。teacher profiling与student训练曝光必须分开核算。 本页不声明未执行实验已经完成。本地对照口径：基线为同一真实verified teacher全集的full-SFT；相同epochs，teacher profiling成本不并入student exposure比率；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Monte Carlo reasoning tree Teacher-side uncertainty contraction Learner-aware SFT routing LLM 后训练 数据与预算：下一份算力花在哪里 渐进收缩为什么先测教师轨迹的分支不确定性，再按学生损失选训练子集？ 正确教师轨迹也可能经过后续容易分叉的位置，蒙特卡洛续写可识别这种学习价值。先按教师分支不确定性收缩池，再经真实学生探测，选当前损失较高的轨迹并重新路由。减少学生曝光量不等于相同倍数的总加速，教师探测成本必须另计。 例如两条都正确的证明，一条中间选择容易走错，先保留它；学生掌握后再换别的难点，不能只按答案是否正确筛选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-progressive-contraction-16120d48" class="ar-learning-paper-anchor"></span>
<h2 id="qa-99594692ebd73c81">渐进收缩为什么先测教师轨迹的分支不确定性，再按学生损失选训练子集？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aprogressive-contraction">Learning More by Training Less: Uncertainty-Guided Progressive Contraction for Efficient Reasoning Post-Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore / Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>正确教师轨迹也可能经过后续容易分叉的位置，蒙特卡洛续写可识别这种学习价值。先按教师分支不确定性收缩池，再经真实学生探测，选当前损失较高的轨迹并重新路由。减少学生曝光量不等于相同倍数的总加速，教师探测成本必须另计。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两条都正确的证明，一条中间选择容易走错，先保留它；学生掌握后再换别的难点，不能只按答案是否正确筛选。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12933">原论文</a> · <a href="../../../../reproductions/2610.12933-progressive-contraction/">实现解读</a> · <a href="#qa-99594692ebd73c81">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:synthself" data-paper-title="Continually Post-training Small Models via Synthetic Self-distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Continually Post-training Small Models via Synthetic Self-distillation LLM 后训练 KAIST AI / LG AI Research 2026-10-09 小模型self-rewrite可能失真，直接SFT又可能偏离base分布。SynthSelf用更大的同家族aligner把train demonstration贪心离线改写，通过答案拒绝采样后SFT。不允许student读评测答案，也不以文本过滤替代真实训练。 默认GSM validation预先拆不重叠两片，只是同域acquisition/retention诊断。本地对照口径：基线为同初始学生与epochs的gold-SFT；另可unfiltered-rewrite消融，真实token预算不相同则明确记录；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Synthetic self-distillation Same-family aligner Offline rejection-sampled SFT LLM 后训练 数据与预算：下一份算力花在哪里 SynthSelf为什么用较大的同家族改写器，并在改写后再次核对训练答案？ 小学生直接自改写可能引入错误，较大同家族模型用于把训练示范改成更适合学生学习的表达。改写经答案拒绝采样后才用于响应监督，且需实测分布与保真约束是否成立。改写器并不天然满足约束，评测答案也不能进入改写或学生输入。 例如把训练题的冗长正确解改成清晰步骤后，仍要检查结论一致；不能用测试题标准答案指导改写，再把得分称为泛化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-synthself-6e723ecb" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b2403206d644220f">SynthSelf为什么用较大的同家族改写器，并在改写后再次核对训练答案？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asynthself">Continually Post-training Small Models via Synthetic Self-distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST AI / LG AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>小学生直接自改写可能引入错误，较大同家族模型用于把训练示范改成更适合学生学习的表达。改写经答案拒绝采样后才用于响应监督，且需实测分布与保真约束是否成立。改写器并不天然满足约束，评测答案也不能进入改写或学生输入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把训练题的冗长正确解改成清晰步骤后，仍要检查结论一致；不能用测试题标准答案指导改写，再把得分称为泛化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13113">原论文</a> · <a href="../../../../reproductions/2610.13113-synthself/">实现解读</a> · <a href="#qa-b2403206d644220f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dial-opd" data-paper-title="DIAL-OPD: Learning More from Fewer Tokens in On-Policy Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="DIAL-OPD: Learning More from Fewer Tokens in On-Policy Distillation LLM 后训练 Eastern Institute of Technology, Ningbo / The Hong Kong Polytechnic University 2026-10-08 用概率的对数均值调节教师—学生对数差异，降低两者都不认可的低概率 token 的监督优先级。按每条响应选取高分位置，未选位置仍保留为上下文。 核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式、可直接改路径运行的命令见checkpoint 运行说明。  On-policy distillation Token supervision LLM 后训练 数据与预算：下一份算力花在哪里 DIAL-OPD为什么不直接按师生对数概率差最大的词元选择监督？ 两者都认为极不可能的词元也可能有很大对数差，单看差值会高估其训练价值。概率对数均值提供尺度调节，再结合差异选位置；未选位置仍保留在上下文，只是不计对应损失。选择监督位置不会自动减少生成成本，也不保证每个大分歧都是知识错误。 例如教师和学生都几乎不支持一个怪词，它们的对数差仍很大；尺度调节让正常关键步骤的分歧有机会优先受监督。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-dial-opd-c9cdfa1a" class="ar-learning-paper-anchor"></span>
<h2 id="qa-c592ae65b12af48c">DIAL-OPD为什么不直接按师生对数概率差最大的词元选择监督？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adial-opd">DIAL-OPD: Learning More from Fewer Tokens in On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Eastern Institute of Technology, Ningbo / The Hong Kong Polytechnic University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两者都认为极不可能的词元也可能有很大对数差，单看差值会高估其训练价值。概率对数均值提供尺度调节，再结合差异选位置；未选位置仍保留在上下文，只是不计对应损失。选择监督位置不会自动减少生成成本，也不保证每个大分歧都是知识错误。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如教师和学生都几乎不支持一个怪词，它们的对数差仍很大；尺度调节让正常关键步骤的分歧有机会优先受监督。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11659">原论文</a> · <a href="../../../../post-training/2610.11659-dial-opd/">实现解读</a> · <a href="#qa-c592ae65b12af48c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:grpo-dropout" data-paper-title="GRPODropout: Less is More for Online Reinforcement Learning Rollouts" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="GRPODropout: Less is More for Online Reinforcement Learning Rollouts LLM 后训练 Harbin Institute of Technology (Shenzhen) 2026-10-08 从同一 prompt 的 GRPO 响应组中筛除部分高概率、正优势响应，并用旧策略概率重新中心化保留响应的优势。不是随机 dropout，也不改变生成预算。 核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式和命令见checkpoint 运行说明。  RLVR Rollout selection LLM 后训练 数据与预算：下一份算力花在哪里 GRPODropout为何筛掉部分高概率正优势响应，却恢复所有非正优势响应？ 高概率且正优势的响应可能进一步强化已占优势的模式，筛选依据是它们对熵变化的贡献，而非随机丢弃。保留负向反馈后，再按旧策略概率重新中心化优势，避免筛选改变基线。生成预算并未因此减少，节约更新样本不等于少生成。 例如一组里常见正确模板过度主导，可少学其中部分重复回答；失败回答仍用于惩罚，不能删掉后把剩余样本都视为正例。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-grpo-dropout-a03001b8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-880cfa0b36ab4eb7">GRPODropout为何筛掉部分高概率正优势响应，却恢复所有非正优势响应？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agrpo-dropout">GRPODropout: Less is More for Online Reinforcement Learning Rollouts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Institute of Technology (Shenzhen)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>高概率且正优势的响应可能进一步强化已占优势的模式，筛选依据是它们对熵变化的贡献，而非随机丢弃。保留负向反馈后，再按旧策略概率重新中心化优势，避免筛选改变基线。生成预算并未因此减少，节约更新样本不等于少生成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一组里常见正确模板过度主导，可少学其中部分重复回答；失败回答仍用于惩罚，不能删掉后把剩余样本都视为正例。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11854">原论文</a> · <a href="../../../../post-training/2610.11854-grpo-dropout/">实现解读</a> · <a href="#qa-880cfa0b36ab4eb7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:magicbeanstalk" data-paper-title="MagicBeanStalk: Escaping the RLVR Zero Advantage Trap with Recursive Data Synthesis" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="MagicBeanStalk: Escaping the RLVR Zero Advantage Trap with Recursive Data Synthesis LLM 后训练 University of Washington 2026-10-08 RLVR有效性取决于problem、当前policy、rollout预算。MBS从verified hard seed提炼reasoning蓝图，自顶向下分解并实测child worked examples是否提高parent正确率，再合成更难新leaf、自底向上按原依赖组合。最终独立验证、保蓝图和实质新颖性，并满足目标policy Goldilocks及预算内完整正确解。 当前状态（2026-10-14）：成本过高，暂不复现／完整方法待验收。本轮新路径固定在 4c4710cd，仅依据 train/validation 教师短诊断提出，尚须新源码完整 GPU 验证。当前状态（2026-10-14）：成本过高，暂不复现／完整方法待验收。用户要求先交付其余成果，不再扩大候选池、更换教师或启动后续种子。本页保留论文解读、实验源码和所有失败证据；magicbeanstalk 只是历史计划键，已从可执行 registry、批量 reproduce 和公开训练 runner 中移出，不是已完成实现，也未接入 evolve。  RLVR data synthesis Effectivity-validated decomposition Policy-calibrated Goldilocks LLM 后训练 数据与预算：下一份算力花在哪里 MagicBeanStalk的子题有效性和最终Goldilocks筛选，为什么不能互相替代？ 子题示范是否提高父题成功率，检验依赖分解是否有效；最终任务还需对目标策略在给定预算下既非全对也非全错，并存在正常结束的正确解。两条件针对不同对象与阶段。局部教师诊断通过不代表递归构造成功，本地多次构造失败也须保留。 例如两个子题确实帮助另一个学生解父题，但目标模型仍一次都解不出合成题；这种任务仍未通过最终可学习性筛选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-magicbeanstalk-9678e8db" class="ar-learning-paper-anchor"></span>
<h2 id="qa-3c26137f6ce5272c">MagicBeanStalk的子题有效性和最终Goldilocks筛选，为什么不能互相替代？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amagicbeanstalk">MagicBeanStalk: Escaping the RLVR Zero Advantage Trap with Recursive Data Synthesis</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>子题示范是否提高父题成功率，检验依赖分解是否有效；最终任务还需对目标策略在给定预算下既非全对也非全错，并存在正常结束的正确解。两条件针对不同对象与阶段。局部教师诊断通过不代表递归构造成功，本地多次构造失败也须保留。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个子题确实帮助另一个学生解父题，但目标模型仍一次都解不出合成题；这种任务仍未通过最终可学习性筛选。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12659">原论文</a> · <a href="../../../../reproductions/2610.12659-magicbeanstalk/">实现解读</a> · <a href="#qa-3c26137f6ce5272c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:pivot" data-paper-title="PIVOT: Perplexity-Informed KD-to-RL Transition Scheduling for Vertical-Domain Few-Shot Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="PIVOT: Perplexity-Informed KD-to-RL Transition Scheduling for Vertical-Domain Few-Shot Distillation LLM 后训练 Ping An Technology / University of Science and Technology of China 2026-10-08 垂直领域的小模型既需要教师传授知识，也需要任务奖励改善最终判断；所有样本同时从蒸馏切换到 RL，可能使困难样本过早失去教师监督。PIVOT 在学生自己的响应上计算教师困惑度，先把低困惑度问题切换到 GRPO，高困惑度问题继续 OPD。 有界少样本、单 seed、LoRA 与短训练只验证机制，不复现原始 480 步/全参数/HWU64 能力收益。共享热身、样本级路由和三配方重置已在 A100 实跑；8 题诊断无准确率提升，不等于原论文能力复现。真实 Qwen2.5-0.5B-Instruct 学生、7B-Instruct 教师，q/v LoRA 而非原文全参数微调。所有配方共享教师响应两轮 SFT、初始 OPD 热身和相同初始 adapter；随后重置 optimizer 与随机种子，分别执行持续 OPD、固定半预算切换及样本级 PIVOT。  On-policy 蒸馏 组相对策略优化 LLM 后训练 数据与预算：下一份算力花在哪里 PIVOT为什么让低教师困惑度的问题先转RL，而高困惑度问题继续蒸馏？ 困惑度在学生自己的响应上计算，表示教师对学生当前行为的支持程度。较低时可较早依靠任务奖励探索，较高时继续获得教师监督；按问题组汇总后随训练逐步增加RL比例。它是路由依据，不是正确性判定，也不表示低困惑度问题必然简单。 例如教师已认可学生的一类解题步骤，这类题先转奖励训练；另一类仍频繁偏离教师分布，暂时保留蒸馏而非统一切换。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-pivot-65855e82" class="ar-learning-paper-anchor"></span>
<h2 id="qa-4001ca700052909f">PIVOT为什么让低教师困惑度的问题先转RL，而高困惑度问题继续蒸馏？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Apivot">PIVOT: Perplexity-Informed KD-to-RL Transition Scheduling for Vertical-Domain Few-Shot Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ping An Technology / University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>困惑度在学生自己的响应上计算，表示教师对学生当前行为的支持程度。较低时可较早依靠任务奖励探索，较高时继续获得教师监督；按问题组汇总后随训练逐步增加RL比例。它是路由依据，不是正确性判定，也不表示低困惑度问题必然简单。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如教师已认可学生的一类解题步骤，这类题先转奖励训练；另一类仍频繁偏离教师分布，暂时保留蒸馏而非统一切换。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11167">原论文</a> · <a href="../../../../post-training/2610.11167-pivot/">实现解读</a> · <a href="#qa-4001ca700052909f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:recal" data-paper-title="ReCal: Calibrating Structured Pruning for On-Policy Distillation Recovery" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="ReCal: Calibrating Structured Pruning for On-Policy Distillation Recovery LLM 后训练 Zhongguancun Academy / Tencent / University of Science and Technology of China 2026-10-08 先剪枝再蒸馏并不保证可恢复：损坏的学生轨迹会限制 OPD 教师信号。ReCal 先用剪枝 probe 测量教师轨迹上损伤，再用损伤重加权原始未剪枝模型的校准统计，重新选择通道；目标宽度和恢复流程保持一致。 恢复使用 q/v LoRA，未复现原文全参数 FSDP、四领域数据或多 seed。已实现真实 FFN 通道删除、教师 SFT 和学生轨迹 OPD；当前四题诊断包含负结果，不代表论文 benchmark 收益。Qwen3-4B/A100，FFN 宽度从 9728 真正减到 7296。对照与 ReCal 使用相同目标宽度和教师 SFT 响应，2 轮 SFT、4 步 OPD；SFT/OPD 问题分开，验证 4 题。见运行说明。  On-policy distillation 剪枝恢复 LLM 后训练 数据与预算：下一份算力花在哪里 ReCal为什么用剪枝探针测损伤，却回到未剪枝模型重新计算通道选择？ 第一次剪枝暴露哪些教师状态受损，这些损伤用于重加权原模型的校准激活，再重新选择通道。它试图避免损坏学生只能产生贫乏轨迹、后续蒸馏难以修复的循环。损伤估计需保留词表剩余概率质量，单独归一化少数候选会改变KL含义。 例如探针发现处理进位的状态受损较大，重新校准时提高这些状态的重要性；不是在已经删掉的通道上继续随意打补丁。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-recal-386ad741" class="ar-learning-paper-anchor"></span>
<h2 id="qa-8cc63e77f549c436">ReCal为什么用剪枝探针测损伤，却回到未剪枝模型重新计算通道选择？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arecal">ReCal: Calibrating Structured Pruning for On-Policy Distillation Recovery</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhongguancun Academy / Tencent / University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>第一次剪枝暴露哪些教师状态受损，这些损伤用于重加权原模型的校准激活，再重新选择通道。它试图避免损坏学生只能产生贫乏轨迹、后续蒸馏难以修复的循环。损伤估计需保留词表剩余概率质量，单独归一化少数候选会改变KL含义。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如探针发现处理进位的状态受损较大，重新校准时提高这些状态的重要性；不是在已经删掉的通道上继续随意打补丁。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11332">原论文</a> · <a href="../../../../post-training/2610.11332-recal/">实现解读</a> · <a href="#qa-8cc63e77f549c436">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:follow-the-winners" data-paper-title="Follow the Winners: Conservative Policy Improvement with the Cross-Entropy Method for Critic-Free RFT" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Follow the Winners: Conservative Policy Improvement with the Cross-Entropy Method for Critic-Free RFT LLM 后训练 Trent AI Limited 2026-10-02 在有状态工具环境里，为同一提示重复生成一组等价 rollout 往往很贵；而 PPO 的 critic 又占用额外模型资源。FTW 不计算 value，也不要求 GRPO 式同题多轨迹。它保留近期策略产生的真实轨迹，从 FIFO 池中反复抽取小批量、仅模仿每批回报最高的条，并用 KL 约束更新幅度。过去轨迹被再次选中的次数自然形成训练权重，而不是对整池只做一次硬截断。 L1 核心机制诊断。L1 核心机制诊断。实现了论文 Algorithm 2 的 FIFO 轨迹池、重复小批量 top- 筛选和带 KL 正则的交叉熵策略投影；目前只在合成双臂 bandit 上执行，不等同于论文的 LLM Agent 训练。没有训练 Qwen、运行 Sokoban/Search-R1，也没有与同预算 PPO/GRPO 比较；bandit 的已知均值只用于诊断，不构成验证集/测试集上的调参或能力评测。该产物标记 diagnostic_only=true、formal_comparison=false，不参与公开能力提升或 Evolve 晋级。  Agentic RL 无 critic 策略改进 精英轨迹筛选 LLM 后训练 数据与预算：下一份算力花在哪里 Follow the Winners为什么反复抽小批精英，而不只取整个回放池的前K条？ 每次先从近期轨迹池随机抽批，再取批内高回报轨迹，重复入选次数形成平滑的排名权重。整池硬截断是特例，通常会丢掉更多次优但有用的轨迹。方法不要求同题多条轨迹或价值模型，仍需KL控制更新；本地小环境诊断不证明工具任务收益。 例如池中最好路线经常入选，次好路线也可能在某批成为精英；不是永久只训练全池最前几条，更不是给重复轨迹去重后等权。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-follow-the-winners-b5a02f54" class="ar-learning-paper-anchor"></span>
<h2 id="qa-410d39abbd09bc56">Follow the Winners为什么反复抽小批精英，而不只取整个回放池的前K条？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Afollow-the-winners">Follow the Winners: Conservative Policy Improvement with the Cross-Entropy Method for Critic-Free RFT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Trent AI Limited</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每次先从近期轨迹池随机抽批，再取批内高回报轨迹，重复入选次数形成平滑的排名权重。整池硬截断是特例，通常会丢掉更多次优但有用的轨迹。方法不要求同题多条轨迹或价值模型，仍需KL控制更新；本地小环境诊断不证明工具任务收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如池中最好路线经常入选，次好路线也可能在某批成为精英；不是永久只训练全池最前几条，更不是给重复轨迹去重后等权。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03361">原论文</a> · <a href="../../../../post-training/2610.03361-follow-the-winners/">实现解读</a> · <a href="#qa-410d39abbd09bc56">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:lesser" data-paper-title="LESSER: Post-Training Data Selection with Output-Layer Gradients" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="LESSER: Post-Training Data Selection with Output-Layer Gradients LLM 后训练 University of Pennsylvania 2026-10-02 现有面向目标任务的数据选择常计算每个候选样本和少量目标任务 query 的全参数梯度，再按相似性选取训练子集；对大模型逐样本反传代价很高。LESSER 只替换特征：从一次前向得到的最后隐藏状态和词表概率解析地计算输出层梯度。SFT、RL 问题选择或教师选择原有的选择规则不需要改变。 L1 前向特征与筛选协议诊断。L1 前向特征与筛选协议诊断。已实现论文的输出层梯度、双侧随机投影及保持不变的 round-robin 选择；没有宣称复现大模型微调、RL、教师选择或论文速度收益。这里的隐藏状态和 logits 来自固定随机张量，用于公式与选择器的确定性验证；没有在公开 Tulu V2、GSM8K 等数据上运行真实 LLM，也没有比较训练后的任务效果或 A100 吞吐。因此标记 diagnostic_only=true，不进入正式能力看板或 Evolve 增益候选。若要升级为 L2，需固定公开 checkpoint/数据修订、query/test 切分、同预算 LESS/随机对照和多 seed 下游训练；  后训练数据选择 梯度特征 计算效率 LLM 后训练 数据与预算：下一份算力花在哪里 LESSER从一次前向解析输出层梯度，为什么不能称为全参数梯度的精确替代？ 解析式利用隐藏状态与输出概率残差的外积，精确针对独立输出读出层；双侧共享投影再压缩这些特征，原数据选择规则可以继续使用。它不是所有层梯度，嵌入权重绑定时还需区分间接依赖。选择用验证代理查询，隔离测试集不能参与选样。 例如用少量验证题的输出层梯度方向挑相关训练题；不能先看测试题方向来选数据，也不能把最后一层相似等同全模型更新相同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-lesser-18cdf418" class="ar-learning-paper-anchor"></span>
<h2 id="qa-23f6b957f56de63e">LESSER从一次前向解析输出层梯度，为什么不能称为全参数梯度的精确替代？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Alesser">LESSER: Post-Training Data Selection with Output-Layer Gradients</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pennsylvania</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>解析式利用隐藏状态与输出概率残差的外积，精确针对独立输出读出层；双侧共享投影再压缩这些特征，原数据选择规则可以继续使用。它不是所有层梯度，嵌入权重绑定时还需区分间接依赖。选择用验证代理查询，隔离测试集不能参与选样。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用少量验证题的输出层梯度方向挑相关训练题；不能先看测试题方向来选数据，也不能把最后一层相似等同全模型更新相同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03702">原论文</a> · <a href="../../../../post-training/2610.03702-lesser/">实现解读</a> · <a href="#qa-23f6b957f56de63e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dars" data-paper-title="Dependency-Aware Reward Shaping for Agentic Reinforcement Learning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Dependency-Aware Reward Shaping for Agentic Reinforcement Learning LLM 后训练 University of Illinois Urbana-Champaign 2026-10-01 把任务进度表示为带先决条件的 predicate 图；验证、失效和修复事件更新图状态，最近破损依赖按图距离衰减已完成工作的 credit，独立分支不受牵连。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行依赖衰减、失效/修复与 potential 差分；未训练 1.5B–8B 模型，官方仓库当前仅发布接口说明、代码仍在准备。执行依赖衰减、失效/修复与 potential 差分；未训练 1.5B–8B 模型，官方仓库当前仅发布接口说明、代码仍在准备。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Agentic RL 依赖图 步级奖励 LLM 后训练 数据与预算：下一份算力花在哪里 依赖感知奖励塑形为什么只衰减破损依赖附近的信用，而不清空所有已完成进度？ 任务以先决条件图表示，某个条件失效会影响依赖它的后续工作，却不必影响独立分支。按图距离衰减信用，再由势函数差分形成奖励，可反映破损与修复。它依赖谓词状态和依赖图是否正确，本地状态转移核没有证明真实智能体训练收益。 例如订票失效会削弱依赖该行程的酒店安排信用，但不应抹掉独立完成的报销材料；修复后相关进度再按状态恢复。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-dars-eb9dd187" class="ar-learning-paper-anchor"></span>
<h2 id="qa-644835722eac59bb">依赖感知奖励塑形为什么只衰减破损依赖附近的信用，而不清空所有已完成进度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adars">Dependency-Aware Reward Shaping for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>任务以先决条件图表示，某个条件失效会影响依赖它的后续工作，却不必影响独立分支。按图距离衰减信用，再由势函数差分形成奖励，可反映破损与修复。它依赖谓词状态和依赖图是否正确，本地状态转移核没有证明真实智能体训练收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如订票失效会削弱依赖该行程的酒店安排信用，但不应抹掉独立完成的报销材料；修复后相关进度再按状态恢复。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01207">原论文</a> · <a href="../../../../post-training/2610.01207-dars/">实现解读</a> · <a href="#qa-644835722eac59bb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gats" data-paper-title="Guide, Then Let Go: Gap-Adaptive Teacher Scheduling for Sparse-Reward Agentic RL" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Guide, Then Let Go: Gap-Adaptive Teacher Scheduling for Sparse-Reward Agentic RL LLM 后训练 Dalian University of Technology / Kuaishou 2026-09-29 用教师训练尾部成功率作为固定参考，以学生滞后一拍的移动平均估计能力差距；OPD 权重随差距线性下降，学生达到教师参考后永久关闭教师分支，继续只做 GRPO。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行滞后一拍移动平均、gap weight 和永久 withdrawal；未做 Qwen Agent RL。执行滞后一拍移动平均、gap weight 和永久 withdrawal；未做 Qwen Agent RL。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Agentic RL On-policy distillation 课程调度 LLM 后训练 数据与预算：下一份算力花在哪里 GATS为什么使用滞后一拍的学生成功率，并在赶上教师后永久撤出教师？ 滞后移动平均避免当前批次结果立即改变同批教师权重，固定教师参考使差距有稳定基准。差距缩小时蒸馏线性减弱，达到参考后永久关闭教师而继续奖励训练，避免短期波动反复开关。成功率受估计噪声影响，本地只验证调度状态机。 例如本轮表现改善，下轮才减少指导；一旦达到设定教师参考，即使随后小幅波动也不重新叫回教师，这与逐批动态开关不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-gats-23ea5c63" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f584461fdb668a3b">GATS为什么使用滞后一拍的学生成功率，并在赶上教师后永久撤出教师？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agats">Guide, Then Let Go: Gap-Adaptive Teacher Scheduling for Sparse-Reward Agentic RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dalian University of Technology / Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>滞后移动平均避免当前批次结果立即改变同批教师权重，固定教师参考使差距有稳定基准。差距缩小时蒸馏线性减弱，达到参考后永久关闭教师而继续奖励训练，避免短期波动反复开关。成功率受估计噪声影响，本地只验证调度状态机。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如本轮表现改善，下轮才减少指导；一旦达到设定教师参考，即使随后小幅波动也不重新叫回教师，这与逐批动态开关不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37898">原论文</a> · <a href="../../../../post-training/2609.37898-gats/">实现解读</a> · <a href="#qa-f584461fdb668a3b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:roft" data-paper-title="Shockingly Simple Self-retrospection Improves Agentic Models Without RL" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Shockingly Simple Self-retrospection Improves Agentic Models Without RL LLM 后训练 Rensselaer Polytechnic Institute 2026-09-28 ROFT 不直接用环境奖励更新动作策略，而是让模型在完整轨迹与反馈之后生成一段自我回顾，再只监督回顾 token。回顾成为后续行为可复用的训练信号，同时避免把环境文本或历史动作误当监督标签。 复现级别：L1 核心机制 + 真实 checkpoint CUDA 路径。复现级别：L1 核心机制 + 真实 checkpoint CUDA 路径。本地实现全局 retrospection-token 交叉熵；不声称复现论文规模训练收益。当前没有论文规模 Agent rollout 数据，也没有把 ROFT 注册进 Evolve；在统一控制器能够实际构造回顾数据、训练并用隔离验证集评价前，不把 registry 标签当成已接入。roft_retrospection_loss 是可训练的 PyTorch 目标；通用后训练 CLI 中的 roft 只提供小型候选策略诊断。  自我回顾 监督微调 Agent 后训练 LLM 后训练 数据与预算：下一份算力花在哪里 ROFT为什么只监督自我回顾词元，而不把轨迹里的动作和环境反馈一起训练？ 完整轨迹与反馈是回顾所需的条件，监督对象则是模型事后归纳的经验。分开上下文掩码与目标掩码，可避免把环境文本或历史错误动作当成应模仿标签；损失按所有回顾词元统一平均。本地没有完整智能体数据闭环，注册名称也不代表已接入演化控制器。 例如一次工具调用失败后，模型回顾应先检查参数；训练读取错误调用和报错，却只学习这段回顾，不模仿报错内容或错误动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-roft-6e694561" class="ar-learning-paper-anchor"></span>
<h2 id="qa-fa5d3a606524d353">ROFT为什么只监督自我回顾词元，而不把轨迹里的动作和环境反馈一起训练？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aroft">Shockingly Simple Self-retrospection Improves Agentic Models Without RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Rensselaer Polytechnic Institute</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>完整轨迹与反馈是回顾所需的条件，监督对象则是模型事后归纳的经验。分开上下文掩码与目标掩码，可避免把环境文本或历史错误动作当成应模仿标签；损失按所有回顾词元统一平均。本地没有完整智能体数据闭环，注册名称也不代表已接入演化控制器。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一次工具调用失败后，模型回顾应先检查参数；训练读取错误调用和报错，却只学习这段回顾，不模仿报错内容或错误动作。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35741">原论文</a> · <a href="../../../../post-training/2609.35741-roft/">实现解读</a> · <a href="#qa-fa5d3a606524d353">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ross" data-paper-title="ROSS: Relearning from Self-Generated Rollouts through Selective Supervision" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="ROSS: Relearning from Self-Generated Rollouts through Selective Supervision LLM 后训练 AllSpark Team（原文以团队署名，未列机构） 2026-09-28 保留历史 self-rollout 的完整上下文，但只对筛选出的模型 continuation 计算损失，避免模仿其中错误或冗余步骤。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 full-context/selective-loss 边界；选择 mask 是 fixture，不冒充论文 selector。执行 full-context/selective-loss 边界；选择 mask 是 fixture，不冒充论文 selector。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  离线 SFT 选择性监督 LLM 后训练 数据与预算：下一份算力花在哪里 ROSS为什么保留历史轨迹的完整上下文，却只监督筛出的续写片段？ 历史上下文说明续写发生在什么状态，删掉它会改变条件分布；只对选中续写计算损失，则避免把旧轨迹中的错误或冗余步骤都当标签。上下文可见与梯度监督需要独立掩码。本地选择掩码是固定诊断输入，没有实现论文选择器，不能据此宣称自动筛选能力。 例如早期有一步错误但后续成功纠正，训练可读到整段经过，只学习被选的纠正续写；不能把可见上下文全部纳入模仿损失。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-ross-56261390" class="ar-learning-paper-anchor"></span>
<h2 id="qa-9faad04c9357c685">ROSS为什么保留历史轨迹的完整上下文，却只监督筛出的续写片段？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aross">ROSS: Relearning from Self-Generated Rollouts through Selective Supervision</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AllSpark Team（原文以团队署名，未列机构）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>历史上下文说明续写发生在什么状态，删掉它会改变条件分布；只对选中续写计算损失，则避免把旧轨迹中的错误或冗余步骤都当标签。上下文可见与梯度监督需要独立掩码。本地选择掩码是固定诊断输入，没有实现论文选择器，不能据此宣称自动筛选能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如早期有一步错误但后续成功纠正，训练可读到整段经过，只学习被选的纠正续写；不能把可见上下文全部纳入模仿损失。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35954">原论文</a> · <a href="../../../../post-training/2609.35954-ross/">实现解读</a> · <a href="#qa-9faad04c9357c685">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:retire-opd" data-paper-title="RetireOPD: Self-Retiring On-Policy Distillation for Agentic Reinforcement Learning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="RetireOPD: Self-Retiring On-Policy Distillation for Agentic Reinforcement Learning LLM 后训练 Zhejiang University 2026-09-17 给不同技能配置解耦教师；学生同时执行 RL 与 on-policy distillation，当成功率接近教师且分布差距不再收缩时自动退休教师。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行退休判据与学生更新；未训练论文规模 Agent 教师。本地执行退休判据与学生更新；未训练论文规模 Agent 教师。  On-policy distillation Agent RL LLM 后训练 数据与预算：下一份算力花在哪里 RetireOPD为什么不能仅凭学生成功率接近教师就立即退休所有教师？ 方法给不同技能配置解耦教师，退休同时考虑成功率接近和分布差距不再收缩。前者反映任务结果，后者提示继续蒸馏的边际空间；只看其中一项可能过早撤走有用指导。退休应针对相应技能判断，本地仅验证判据和更新，不代表论文规模多教师训练。 例如学生搜索技能已接近搜索教师，但工具格式仍落后，前者可以考虑退休，不能据一个总成功率就把格式教师一并撤掉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-retire-opd-e8a79255" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1ad55afe94098476">RetireOPD为什么不能仅凭学生成功率接近教师就立即退休所有教师？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aretire-opd">RetireOPD: Self-Retiring On-Policy Distillation for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>方法给不同技能配置解耦教师，退休同时考虑成功率接近和分布差距不再收缩。前者反映任务结果，后者提示继续蒸馏的边际空间；只看其中一项可能过早撤走有用指导。退休应针对相应技能判断，本地仅验证判据和更新，不代表论文规模多教师训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生搜索技能已接近搜索教师，但工具格式仍落后，前者可以考虑退休，不能据一个总成功率就把格式教师一并撤掉。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.20784">原论文</a> · <a href="../../../../post-training/2609.20784-retire-opd/">实现解读</a> · <a href="#qa-1ad55afe94098476">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:trajectory-learnability" data-paper-title="Trajectory Learnability for Offline On-Policy Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Trajectory Learnability for Offline On-Policy Distillation LLM 后训练 National University of Singapore 2026-09-16 用成功轨迹训练参考模型，以参考与当前策略逐 token 对数似然变化衡量可学性，并据此重加权离线 OPD 轨迹。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行逐 token 可学性聚合和轨迹加权；未复刻论文 GPU 训练预算。本地执行逐 token 可学性聚合和轨迹加权；未复刻论文 GPU 训练预算。  On-policy distillation 轨迹加权 LLM 后训练 数据与预算：下一份算力花在哪里 离线OPD为什么比较成功参考模型与当前策略的逐词元似然，而不只按轨迹奖励排序？ 终局成功只能说明轨迹结果，不能说明当前学生在哪些位置还可学习。用成功轨迹训练参考模型，再比较其与当前策略的词元似然变化，可形成轨迹可学性权重。该信号仍依赖参考模型和离线覆盖，不能恢复数据中从未出现的状态，本地只是权重核验证。 例如两条都答对的解法，一条学生已熟练，另一条关键转折尚未掌握；可学性重加权试图区分它们，而非给相同成功标签就等权。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-trajectory-learnability-8d70d16c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-16034fc631f8fda0">离线OPD为什么比较成功参考模型与当前策略的逐词元似然，而不只按轨迹奖励排序？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atrajectory-learnability">Trajectory Learnability for Offline On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>终局成功只能说明轨迹结果，不能说明当前学生在哪些位置还可学习。用成功轨迹训练参考模型，再比较其与当前策略的词元似然变化，可形成轨迹可学性权重。该信号仍依赖参考模型和离线覆盖，不能恢复数据中从未出现的状态，本地只是权重核验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两条都答对的解法，一条学生已熟练，另一条关键转折尚未掌握；可学性重加权试图区分它们，而非给相同成功标签就等权。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.18321">原论文</a> · <a href="../../../../post-training/2609.18321-trajectory-learnability/">实现解读</a> · <a href="#qa-16034fc631f8fda0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:growmtp" data-paper-title="GrowMTP: Can RL Grow Its Own Draft Head?" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="GrowMTP: Can RL Grow Its Own Draft Head? LLM 后训练 WeChat AI, Tencent / Peking University 2026-09-15 在 RL rollout 内按被接受的草稿深度训练 MTP head，并与主干梯度解耦。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 depth-coupled acceptance loss；未报告 GPU 加速。本地执行 depth-coupled acceptance loss；未报告 GPU 加速。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  RL 训练加速 推测解码 LLM 后训练 数据与预算：下一份算力花在哪里 GrowMTP为什么按实际接受深度训练草稿头，并把它与主干梯度解耦？ 草稿越深，前面的提议必须先被接受才会真正影响生成，实际接受深度能提供与使用情形相关的训练信号。梯度解耦限制草稿加速目标干扰主策略的奖励学习。接受率与端到端速度还取决于硬件及验证成本，本地深度损失诊断没有测得GPU加速。 例如第三个草稿词元只有前两个通过验证才有用，训练不能假定每个深度都同样可达；改善草稿头也不能自动算作主策略能力提升。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-growmtp-d690b374" class="ar-learning-paper-anchor"></span>
<h2 id="qa-49cc4453c625bc11">GrowMTP为什么按实际接受深度训练草稿头，并把它与主干梯度解耦？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agrowmtp">GrowMTP: Can RL Grow Its Own Draft Head?</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · WeChat AI, Tencent / Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>草稿越深，前面的提议必须先被接受才会真正影响生成，实际接受深度能提供与使用情形相关的训练信号。梯度解耦限制草稿加速目标干扰主策略的奖励学习。接受率与端到端速度还取决于硬件及验证成本，本地深度损失诊断没有测得GPU加速。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如第三个草稿词元只有前两个通过验证才有用，训练不能假定每个深度都同样可达；改善草稿头也不能自动算作主策略能力提升。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16648">原论文</a> · <a href="../../../../post-training/2609.16648-growmtp/">实现解读</a> · <a href="#qa-49cc4453c625bc11">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:stride-opd" data-paper-title="Know When to Stop, Where to Restart: Accelerating Multi-Turn Agentic On-Policy Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Know When to Stop, Where to Restart: Accelerating Multi-Turn Agentic On-Policy Distillation LLM 后训练 University of Science and Technology of China / Ant Group 2026-09-13 teacher 累积置信度越界时早停，并从最弱正确 turn 的缓存前缀重新开始。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 未复现大模型 rollout 吞吐。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行早停和前缀重启；未复现大模型 rollout 吞吐。本地执行早停和前缀重启；未复现大模型 rollout 吞吐。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  On-policy distillation 多轮加速 LLM 后训练 数据与预算：下一份算力花在哪里 STRIDE-OPD为什么把早停与最弱正确轮次的前缀重启配在一起？ 教师累积置信度触发停止，可避免在低价值后续上继续花费；缓存中较弱但正确的轮次则提供可学习的重启状态，把预算回投到仍需加强的位置。停止和重启是不同决策，不能等同直接跳到标准答案。本地状态核未验证大模型多轮生成吞吐。 例如一段工具交互后续已无新增指导，可停止；下一次从此前勉强完成的正确轮次重试，而不是总从任务开头重复熟悉步骤。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-stride-opd-55204229" class="ar-learning-paper-anchor"></span>
<h2 id="qa-dfb066e0ae31243d">STRIDE-OPD为什么把早停与最弱正确轮次的前缀重启配在一起？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Astride-opd">Know When to Stop, Where to Restart: Accelerating Multi-Turn Agentic On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China / Ant Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>教师累积置信度触发停止，可避免在低价值后续上继续花费；缓存中较弱但正确的轮次则提供可学习的重启状态，把预算回投到仍需加强的位置。停止和重启是不同决策，不能等同直接跳到标准答案。本地状态核未验证大模型多轮生成吞吐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一段工具交互后续已无新增指导，可停止；下一次从此前勉强完成的正确轮次重试，而不是总从任务开头重复熟悉步骤。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.14636">原论文</a> · <a href="../../../../post-training/2609.14636-stride-opd/">实现解读</a> · <a href="#qa-dfb066e0ae31243d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:df-opd" data-paper-title="Data-free On-policy Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Data-free On-policy Distillation LLM 后训练 Institute of Automation, Chinese Academy of Sciences / Tencent 2026-09-12 由教师在自身策略空间生成问题，减少对外部后训练语料的依赖。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行自生成问题的策略特征诊断；未生成自然语言训练集。本地执行自生成问题的策略特征诊断；未生成自然语言训练集。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  On-policy distillation 数据合成 LLM 后训练 数据与预算：下一份算力花在哪里 Data-free OPD自己生成问题，为什么仍不能说训练不依赖任何先验知识？ 问题来自教师自身策略而非外部后训练题库，减少的是额外数据收集依赖；教师参数、生成分布和筛选条件仍决定课程覆盖。自生成也可能重复已有模式或产生不可靠任务，需要验证质量。本地只做问题生成的策略特征诊断，尚未生成自然语言训练集。 例如教师围绕已知代码技能提出练习，可减少人工题库；但如果它一直生成同一类循环题，学生不会因此自动学到未覆盖的并发问题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-df-opd-48f2c181" class="ar-learning-paper-anchor"></span>
<h2 id="qa-cad6ac56bf666ca8">Data-free OPD自己生成问题，为什么仍不能说训练不依赖任何先验知识？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adf-opd">Data-free On-policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Automation, Chinese Academy of Sciences / Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>问题来自教师自身策略而非外部后训练题库，减少的是额外数据收集依赖；教师参数、生成分布和筛选条件仍决定课程覆盖。自生成也可能重复已有模式或产生不可靠任务，需要验证质量。本地只做问题生成的策略特征诊断，尚未生成自然语言训练集。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如教师围绕已知代码技能提出练习，可减少人工题库；但如果它一直生成同一类循环题，学生不会因此自动学到未覆盖的并发问题。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.14193">原论文</a> · <a href="../../../../post-training/2609.14193-df-opd/">实现解读</a> · <a href="#qa-cad6ac56bf666ca8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:adaptive-opd-gate" data-paper-title="A Unified Per-Token Gating Family for On-Policy Distillation: FKL/RKL Mixing with Multi-Channel and Bias Coefficients" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="A Unified Per-Token Gating Family for On-Policy Distillation: FKL/RKL Mixing with Multi-Channel and Bias Coefficients LLM 后训练 Xiaohongshu 2026-09-10 把熵、不确定性、reference 偏移和教师—学生差距组合成逐 token gate，在 FKL/RKL 蒸馏方向间自适应分配。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行四信号 gate；结果仅是机制诊断，不把探索性结果写成稳定胜出。本地执行四信号 gate；结果仅是机制诊断，不把探索性结果写成稳定胜出。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  On-policy distillation 逐 token 自适应门控 LLM 后训练 数据与预算：下一份算力花在哪里 逐词元门控为何混合FKL与RKL，而不是对整条回答只选一个散度方向？ 不同位置的教师不确定性、师生差距与参考偏移不同，统一散度方向可能把覆盖与集中之间的取舍强加给所有词元。门控组合多路信号，在位置层分配正向和反向蒸馏权重。门控是启发监督分配，不是正确性证明，本地四信号实验也没有稳定胜出结论。 例如关键分叉处需保留教师多种选择，已收敛的格式位置可更集中；不能因为一句话整体可靠，就认为每个词元都应使用相同权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-adaptive-opd-gate-493b3a1b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-57b792891db90d75">逐词元门控为何混合FKL与RKL，而不是对整条回答只选一个散度方向？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aadaptive-opd-gate">A Unified Per-Token Gating Family for On-Policy Distillation: FKL/RKL Mixing with Multi-Channel and Bias Coefficients</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同位置的教师不确定性、师生差距与参考偏移不同，统一散度方向可能把覆盖与集中之间的取舍强加给所有词元。门控组合多路信号，在位置层分配正向和反向蒸馏权重。门控是启发监督分配，不是正确性证明，本地四信号实验也没有稳定胜出结论。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如关键分叉处需保留教师多种选择，已收敛的格式位置可更集中；不能因为一句话整体可靠，就认为每个词元都应使用相同权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11768">原论文</a> · <a href="../../../../post-training/2609.11768-adaptive-opd-gate/">实现解读</a> · <a href="#qa-57b792891db90d75">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:locus" data-paper-title="LOCUS: Task-Aware Low-Rank Post-Training for Token-Efficient Language Generation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="LOCUS: Task-Aware Low-Rank Post-Training for Token-Efficient Language Generation LLM 后训练 University of Washington 2026-09-10 学习任务相关低秩后训练子空间，只在紧凑方向上更新以缩短回答，同时保留任务能力。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地用样本特征 SVD 投影策略梯度；未训练论文规模语言模型。本地用样本特征 SVD 投影策略梯度；未训练论文规模语言模型。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  低秩后训练 Token 效率 LLM 后训练 数据与预算：下一份算力花在哪里 LOCUS把更新限制在任务相关低秩子空间，为什么有机会缩短回答却不等于直接截断？ 低秩约束作用于参数更新方向，试图保留任务相关的有效变化、限制无关漂移，简洁性通过后训练目标学习。直接截断则在生成后强行删掉内容，可能损失必要步骤。子空间是否覆盖目标能力仍需检验，本地特征SVD投影不能证明大模型长度与能力兼得。 例如让模型学会少写重复检查，与把每条证明的后半段删除不同；若所选子空间不包含关键推理方向，即使回答变短也可能失去正确性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-locus-5c47d1f6" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f1bbb645213174e0">LOCUS把更新限制在任务相关低秩子空间，为什么有机会缩短回答却不等于直接截断？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Alocus">LOCUS: Task-Aware Low-Rank Post-Training for Token-Efficient Language Generation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>低秩约束作用于参数更新方向，试图保留任务相关的有效变化、限制无关漂移，简洁性通过后训练目标学习。直接截断则在生成后强行删掉内容，可能损失必要步骤。子空间是否覆盖目标能力仍需检验，本地特征SVD投影不能证明大模型长度与能力兼得。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如让模型学会少写重复检查，与把每条证明的后半段删除不同；若所选子空间不包含关键推理方向，即使回答变短也可能失去正确性。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11739">原论文</a> · <a href="../../../../post-training/2609.11739-locus/">实现解读</a> · <a href="#qa-f1bbb645213174e0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sparse-opd" data-paper-title="Extremely Sparse Supervision Incentivizes Reasoning Ability" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Extremely Sparse Supervision Incentivizes Reasoning Ability LLM 后训练 Amazon / Duke University 2026-09-03 常规 on-policy distillation 对生成轨迹的每个 token 使用教师分布。论文发现只挑一到两个关键位置、约占全部 token 的 0.05%，也能达到或超过全 token 训练。最大正差异 token 尤其有效，说明有效后训练可能更接近“反思关键步骤”而非逐字纠错。 复现级别：核心目标函数 mini-suite。复现级别：核心目标函数 mini-suite。在统一 OPD runner 中实现最大差异、最小差异和随机稀疏 token 选择。未执行 Qwen/Llama 全参数 OPD 或 PPO；当前方法不宣传 CUDA 路径，因此无需 GPU receipt。arithmetic-smoke、seeds 42/43/44 的监督位置数、监督比例、选择差异和目标值见 metrics/arithmetic-smoke-seeds42-44.json。  极稀疏 On-policy distillation LLM 后训练 数据与预算：下一份算力花在哪里 Sparse OPD只监督少数最大正差异位置，为什么仍要保留完整学生轨迹上下文？ 关键位置的教师分布依赖前面实际生成的推理，去掉未监督部分会改变该状态。稀疏化改变的是哪些位置产生梯度，而不是把其余词元从条件输入删除。少量位置有效是实验条件下的发现，不能推断任何任务都只需一两个词元，本地也未做全参数蒸馏。 例如只学习一次关键纠错词元，教师仍需看到之前的计算才能判断它；把整段前文删掉后监督同一个字，已经变成不同任务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-sparse-opd-2b68a2ae" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d6859f74d2d04207">Sparse OPD只监督少数最大正差异位置，为什么仍要保留完整学生轨迹上下文？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asparse-opd">Extremely Sparse Supervision Incentivizes Reasoning Ability</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Amazon / Duke University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>关键位置的教师分布依赖前面实际生成的推理，去掉未监督部分会改变该状态。稀疏化改变的是哪些位置产生梯度，而不是把其余词元从条件输入删除。少量位置有效是实验条件下的发现，不能推断任何任务都只需一两个词元，本地也未做全参数蒸馏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只学习一次关键纠错词元，教师仍需看到之前的计算才能判断它；把整段前文删掉后监督同一个字，已经变成不同任务。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04565">原论文</a> · <a href="../../../../post-training/2609.04565-sparse-opd/">实现解读</a> · <a href="#qa-d6859f74d2d04207">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rail" data-paper-title="Optimizing What Policies Learn From: Recoverability-Aware Rollout Intervention Learning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Optimizing What Policies Learn From: Recoverability-Aware Rollout Intervention Learning LLM 后训练 University of Notre Dame / Amazon 2026-08-05 主题：rollout 预算分配。均匀 rollout 浪费预算，静态启发式又跟不上策略变化。RAIL 把干预位置与方式视为 contextual bandit，并通过 shadow-to-live 轨迹学习 recoverability controller。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的 rollout 预算分配算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/arithmetic-smoke-seed42.json，不提交 checkpoint 或原始运行目录。  rollout 预算分配 LLM 后训练 数据与预算：下一份算力花在哪里 RAIL为什么把干预位置与方式当作带成本的决策，而不总在最不确定处多采样？ 不确定不代表能够恢复，一些状态追加预算也难以改变结果。控制器根据状态学习不同干预的可恢复收益，并扣除成本；从影子评估到实际执行，使调度随策略变化调整。恢复信号需要真实可审计反馈，不能读取标准答案来选动作，本地未运行原文大规模环境。 例如一条轨迹只差一次工具重试，另一条已因前提错误无从修复，相同追加预算可能收益不同；单按熵高低无法区分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-rail-7f7d9ac0" class="ar-learning-paper-anchor"></span>
<h2 id="qa-6b91768c570d659e">RAIL为什么把干预位置与方式当作带成本的决策，而不总在最不确定处多采样？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arail">Optimizing What Policies Learn From: Recoverability-Aware Rollout Intervention Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Notre Dame / Amazon</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不确定不代表能够恢复，一些状态追加预算也难以改变结果。控制器根据状态学习不同干预的可恢复收益，并扣除成本；从影子评估到实际执行，使调度随策略变化调整。恢复信号需要真实可审计反馈，不能读取标准答案来选动作，本地未运行原文大规模环境。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一条轨迹只差一次工具重试，另一条已因前提错误无从修复，相同追加预算可能收益不同；单按熵高低无法区分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05080">原论文</a> · <a href="../../../../post-training/2608.05080-rail/">实现解读</a> · <a href="#qa-6b91768c570d659e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:specroll" data-paper-title="SpecRoll: Fast-Slow Verifier-Feedback Adaptation for Speculative Reinforcement Learning Rollouts" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="SpecRoll: Fast-Slow Verifier-Feedback Adaptation for Speculative Reinforcement Learning Rollouts LLM 后训练 VNU University of Engineering and Technology / Viettel AI 2026-08-05 主题：RL rollout 加速。RL 中 target policy 持续变化，静态 drafter 很快过时。SpecRoll 用 future-token heads 提议、Reflex 做无反传的快速隐状态纠偏，并只在持续退化时启动慢速 head 更新；exact verifier 保持采样分布不变。 新版完整 GRPO 多模型实验不复现，审查已完成，现有 mini-suite 的证据等级不变。复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的 RL rollout 加速算子；不把确定性小型评测写成论文完整复现。版本边界（2026-10-15 复核）：本页与 specroll 保留原 v1 的 fast/slow 机制，不代表已经实现 v2 SPARK。v2 改为同一 prompt group 内共享、每轮重置的低秩 logit correction，并由 verifier 反馈更新、跨 rollout 学习投影；不能把旧 adapter 改名就算新版已接入。  RL rollout 加速 LLM 后训练 数据与预算：下一份算力花在哪里 SpecRoll中快速纠偏和慢速草稿头更新，为什么都不能替代精确验证器？ 策略在RL中持续变化，快速隐藏状态纠偏用于及时适应，持续退化时再触发较慢的草稿头训练。二者提高提议质量，精确接受拒绝验证才负责保持目标采样分布。若省略验证，即使草稿看似更准也可能改变RL数据分布；本地没有大模型吞吐结论。 例如草稿头突然跟不上新策略，先修正隐状态再考虑训练；每次提议仍须验证，不能因连续几次猜对就直接当目标策略输出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-specroll-077f92f9" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1d1234935a356567">SpecRoll中快速纠偏和慢速草稿头更新，为什么都不能替代精确验证器？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aspecroll">SpecRoll: Fast-Slow Verifier-Feedback Adaptation for Speculative Reinforcement Learning Rollouts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · VNU University of Engineering and Technology / Viettel AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>策略在RL中持续变化，快速隐藏状态纠偏用于及时适应，持续退化时再触发较慢的草稿头训练。二者提高提议质量，精确接受拒绝验证才负责保持目标采样分布。若省略验证，即使草稿看似更准也可能改变RL数据分布；本地没有大模型吞吐结论。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如草稿头突然跟不上新策略，先修正隐状态再考虑训练；每次提议仍须验证，不能因连续几次猜对就直接当目标策略输出。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04962">原论文</a> · <a href="../../../../post-training/2608.04962-specroll/">实现解读</a> · <a href="#qa-1d1234935a356567">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:coba-rl" data-paper-title="CoBA-RL" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="CoBA-RL LLM 后训练 Zhejiang University 2026-06-21 普通 RLVR 可能只重新分配 base model 已有轨迹的概率，提升 pass@1 却不扩展高采样 pass@k 所反映的能力边界。该方法先用多次采样估计边界，在边界附近/之外注入教师推理，再用 RL 巩固。 定位当前能力边界，对边界附近样本提供教师引导，再用 RL 固化新增推理模式。实现了边界状态、难度课程、真实教师触发、自由生成 RL、pass@k/教师缓存与成本曲线；本地 teacher 只有 0.5B，且最高只统计 pass@8，没有运行论文规模 pass@256 或同规模学生，因此不能宣称复现论文中的能力边界增量。本地算术 suite 带可复现难度；训练器维护动态 curriculum boundary、采样边界样本，无正确 rollout 时调用固定 revision 的真实 causal-LM teacher，并把教师 completion 以小权重 SFT 项注入 sequence RL。  能力边界课程 LLM 后训练 数据与预算：下一份算力花在哪里 CoBA-RL为什么同时看pass@1与较大采样预算的pass@k来定位能力边界？ 单次成功率提高可能只是把已有正确轨迹变得常见，不一定获得原先完全采不到的新解法。多次采样用于探测边界，再在边界附近引入教师并用RL巩固。有限预算仍可能漏掉稀有解，本地仅到较小的采样规模，不能宣称复现原文高采样边界增量。 例如原来偶尔能解的题变成经常解对，说明利用更好；若想判断是否学会原先从未解出的题，还需更广采样并计入教师成本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-coba-rl-1893eb3e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f5709b23a4b1224c">CoBA-RL为什么同时看pass@1与较大采样预算的pass@k来定位能力边界？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acoba-rl">CoBA-RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单次成功率提高可能只是把已有正确轨迹变得常见，不一定获得原先完全采不到的新解法。多次采样用于探测边界，再在边界附近引入教师并用RL巩固。有限预算仍可能漏掉稀有解，本地仅到较小的采样规模，不能宣称复现原文高采样边界增量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如原来偶尔能解的题变成经常解对，说明利用更好；若想判断是否学会原先从未解出的题，还需更广采样并计入教师成本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.22317">原论文</a> · <a href="../../../../post-training/2606.22317-coba-rl/">实现解读</a> · <a href="#qa-f5709b23a4b1224c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sparse-to-dense-reward-principle" data-paper-title="Beyond GRPO and On-Policy Distillation: An Empirical Sparse-to-Dense Reward Principle for Language-Model Post-Training" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Beyond GRPO and On-Policy Distillation: An Empirical Sparse-to-Dense Reward Principle for Language-Model Post-Training LLM 后训练 LinkedIn 2026-05-12 Sec.2–3四阶段工作流和等标签预算经验对照是本论文核心；FKL在teacher occupancy、OPD在student occupancy，教师冻结且需共享tokenizer。库中已有GRPO/OPD/KL算子不等于本文完整流程；不重复包装通用KL或把四个状态标签称为复现。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。状态：仅文献与成本收录，没有可执行能力adapter，不以heuristic冒充核心模型。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本轮不提供可运行模型、loss包装或伪测试。库里已有通用KL/RL/统计工具并不构成本文核心流程；原文语义模型、API多轮生成或大规模训练不能用手工规则替换。仅保存经过核验的方法、资源、源码状态与原图，终态为 not_reproduced_high_cost。后续不得自动移回待训练队列。  训练流程与资源分配 Teacher RL与FKL-to-OPD LLM 后训练 数据与预算：下一份算力花在哪里 稀疏到稠密奖励原则为什么不仅是把GRPO与KL算子按顺序调用？ 论文核心是四阶段流程及相同标签预算下的经验对照，还区分教师访问状态上的正向KL与学生访问状态上的逆向KL。散度方向和状态来源共同决定训练信号，只有几个通用算子或阶段标签不能构成复现。本地目前文献收录，未执行完整训练流程。 例如同样写着KL损失，在教师标准解的前缀计算与在学生错误前缀计算，监督对象不同；不能仅因公式名字相同就合并成一个阶段。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-sparse-to-dense-reward-principle-66732323" class="ar-learning-paper-anchor"></span>
<h2 id="qa-a171a8da19e34101">稀疏到稠密奖励原则为什么不仅是把GRPO与KL算子按顺序调用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asparse-to-dense-reward-principle">Beyond GRPO and On-Policy Distillation: An Empirical Sparse-to-Dense Reward Principle for Language-Model Post-Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>论文核心是四阶段流程及相同标签预算下的经验对照，还区分教师访问状态上的正向KL与学生访问状态上的逆向KL。散度方向和状态来源共同决定训练信号，只有几个通用算子或阶段标签不能构成复现。本地目前文献收录，未执行完整训练流程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同样写着KL损失，在教师标准解的前缀计算与在学生错误前缀计算，监督对象不同；不能仅因公式名字相同就合并成一个阶段。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.12483v1">原论文</a> · <a href="../../../../post-training/2605.12483-sparse-to-dense-reward-principle/">实现解读</a> · <a href="#qa-a171a8da19e34101">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:lightning-opd" data-paper-title="Lightning OPD" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Lightning OPD LLM 后训练 MIT HAN Lab 2026-04-14 传统在线蒸馏在每一步训练都调用教师，吞吐和成本受教师推理限制。Lightning OPD 先让学生在 SFT 数据上产生 on-policy rollout，再由同一个教师一次性计算 token 分布并缓存。训练只读取缓存，因此保留学生分布上的蒸馏信号，又不需要训练期在线教师。 保真度：本地实现复现教师预填充、teacher consistency 和训练期零在线教师调用；保真度：本地实现复现教师预填充、teacher consistency 和训练期零在线教师调用；当前使用候选策略验证机制，不等同于论文的 Qwen3 全参数训练。当前没有训练真实 Qwen3、token-level vocabulary distribution 或复跑 AIME；因此只能证明缓存式 OPD 数据流和教师调用约束成立，不能把本地 accuracy 与论文 AIME 数字比较。实现先为全部训练候选缓存教师概率，保存 teacher_prefill_calls 和 teacher_cache_entries；  On-policy distillation LLM 后训练 数据与预算：下一份算力花在哪里 Lightning OPD缓存的是学生轨迹上的教师评分，为什么不能等同持续更新的在线教师蒸馏？ 先由学生采样、再用一致教师配置打分，可一次付出教师成本，后续训练读取缓存。标签最初位于学生分布，但学生更新后访问状态会变化，旧缓存不会自动覆盖新状态。因而成本收益与缓存覆盖、教师一致性有关，本地只验证数据流，没有真实词表蒸馏成绩。 例如学生初期常犯某类错误，缓存能教这些前缀；当学生后来走出新解法，旧缓存不会自动补上新前缀，需要另行定义刷新协议。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-lightning-opd-b1670874" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d662b69ce7015b40">Lightning OPD缓存的是学生轨迹上的教师评分，为什么不能等同持续更新的在线教师蒸馏？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Alightning-opd">Lightning OPD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · MIT HAN Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>先由学生采样、再用一致教师配置打分，可一次付出教师成本，后续训练读取缓存。标签最初位于学生分布，但学生更新后访问状态会变化，旧缓存不会自动覆盖新状态。因而成本收益与缓存覆盖、教师一致性有关，本地只验证数据流，没有真实词表蒸馏成绩。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生初期常犯某类错误，缓存能教这些前缀；当学生后来走出新解法，旧缓存不会自动补上新前缀，需要另行定义刷新协议。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.13010">原论文</a> · <a href="../../../../post-training/2604.13010-lightning-opd/">实现解读</a> · <a href="#qa-d662b69ce7015b40">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cross-script-knowledge-transfer" data-paper-title="Large Reasoning Models Struggle to Transfer Parametric Knowledge Across Scripts" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Large Reasoning Models Struggle to Transfer Parametric Knowledge Across Scripts LLM 后训练 Google Research 2026-03-17 Sec.4–6与Appendix A/H：观察性回归、训练专用entity提示干预和真实LoRA是定义性路径。不能把正则音译、手工插提示或小分类器当成其LLM知识检索机制。本文不是新闭式RL loss；本轮仅文献收录，不强造operator。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。状态：仅文献与成本收录，没有可执行能力adapter，不以heuristic冒充核心模型。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本轮不提供可运行模型、loss包装或伪测试。库里已有通用KL/RL/统计工具并不构成本文核心流程；原文语义模型、API多轮生成或大规模训练不能用手工规则替换。仅保存经过核验的方法、资源、源码状态与原图，终态为 not_reproduced_high_cost。后续不得自动移回待训练队列。  多语言后训练 跨文字系统知识迁移 LLM 后训练 数据与预算：下一份算力花在哪里 跨文字系统知识迁移为何不能只靠把问题机械音译来判断模型是否拥有知识？ 文字系统变化会同时影响实体识别、参数知识检索与推理表达，仅比较音译前后答案难以定位原因。论文结合观察回归、训练期实体提示干预和真实LoRA来拆分这些因素。提示或正则替换只是条件改变，本地文献收录没有实现语言模型知识检索能力。 例如同一地名改用另一种文字后回答失败，可能是实体没对齐而非事实从未学过；加提示能帮助诊断，却不能当成迁移训练已经完成。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-cross-script-knowledge-transfer-cff708b0" class="ar-learning-paper-anchor"></span>
<h2 id="qa-2ca85a2d8b44437e">跨文字系统知识迁移为何不能只靠把问题机械音译来判断模型是否拥有知识？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Across-script-knowledge-transfer">Large Reasoning Models Struggle to Transfer Parametric Knowledge Across Scripts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文字系统变化会同时影响实体识别、参数知识检索与推理表达，仅比较音译前后答案难以定位原因。论文结合观察回归、训练期实体提示干预和真实LoRA来拆分这些因素。提示或正则替换只是条件改变，本地文献收录没有实现语言模型知识检索能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一地名改用另一种文字后回答失败，可能是实体没对齐而非事实从未学过；加提示能帮助诊断，却不能当成迁移训练已经完成。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.17070v1">原论文</a> · <a href="../../../../post-training/2603.17070-cross-script-knowledge-transfer/">实现解读</a> · <a href="#qa-2ca85a2d8b44437e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:prompt-level-distillation" data-paper-title="Prompt-Level Distillation: A Non-Parametric Alternative to Model Fine-Tuning for Efficient Reasoning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Prompt-Level Distillation: A Non-Parametric Alternative to Model Fine-Tuning for Efficient Reasoning LLM 后训练 Google 2026-02-24 PLD 不微调学生参数，而把教师推理抽象为可审查的系统指令：先用带标签训练样本提取微规则，经语义向量 DBSCAN 去掉噪声、合成规则，再根据训练错误修订冲突。学生最终使用整理后的规则，不读取每个测试样本的答案。图按原文 Figure 1 重绘。原始流程图。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。§4.1 使用 Gemini 3 Flash thinking 提取、Gemini 3 Pro thinking 合成和修复、Gemini Embedding 聚类，学生含 Gemma-3 4B / Gemini 2 Flash。多阶段闭源调用与完整多任务评测成本无法廉价固定，成本过高，不复现（审查 DONE），不下载模型探成本。  Context distillation 提示级非参数蒸馏 LLM 后训练 数据与预算：下一份算力花在哪里 PLD不更新学生参数，为什么还要训练、验证与测试严格分离？ 教师从带标签训练样本提取规则，经语义聚类与错误对照修订后，规则本身就承载了学习结果。验证集可判断规则是否收敛，测试时必须冻结规则，不能依据测试答案继续修补。参数不变并不消除泄漏风险；它把教师推理编译为可读指令而非微调权重。 例如训练中提炼日期归一化规则，验证后固定为系统指令；看到测试标准日期再添加特例，即使没有梯度更新也已使用测试标签。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-prompt-level-distillation-91a64214" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f8e39103d977724f">PLD不更新学生参数，为什么还要训练、验证与测试严格分离？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aprompt-level-distillation">Prompt-Level Distillation: A Non-Parametric Alternative to Model Fine-Tuning for Efficient Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>教师从带标签训练样本提取规则，经语义聚类与错误对照修订后，规则本身就承载了学习结果。验证集可判断规则是否收敛，测试时必须冻结规则，不能依据测试答案继续修补。参数不变并不消除泄漏风险；它把教师推理编译为可读指令而非微调权重。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如训练中提炼日期归一化规则，验证后固定为系统指令；看到测试标准日期再添加特例，即使没有梯度更新也已使用测试标签。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与数据协议；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.21103v1">原论文</a> · <a href="../../../../post-training/2602.21103-prompt-level-distillation/">实现解读</a> · <a href="#qa-f8e39103d977724f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:chord" data-paper-title="CHORD" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="CHORD LLM 后训练 Alibaba Group 2025-08-15 将 SFT 与 RL 串成两个独立阶段会造成 expert data 的过拟合或过早遗忘。CHORD 把专家 SFT 作为 on-policy RL 中动态退火的辅助目标，并以 token 级不确定性权重平滑从模仿过渡到探索。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地不训练 LLM token-level uncertainty model，gold candidate 仅是确定性 expert 代理。把 verified gold candidate 作为 expert trace，真实按训练进度退火 SFT 项并与 on-policy group-RL 梯度相加。  SFT-RL 动态混合 LLM 后训练 数据与预算：下一份算力花在哪里 CHORD为什么在RL过程中逐渐减小专家监督，而不一次性切掉SFT？ 专家数据可在探索初期提供稳定方向，但长期过强模仿会限制新策略；动态退火结合词元不确定性权重，让监督与探索平滑交接。它仍需控制专家与当前策略的分布差异，不保证混合必然优于分阶段。本地专家候选只是代理，未训练词元不确定性模型。 例如学生开始解题时保留教师步骤指导，逐渐熟练后更多依靠任务奖励；不是到某一步突然完全忘掉专家，也不是始终固定等权。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-chord-f1e12f5e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-751d193dd884b093">CHORD为什么在RL过程中逐渐减小专家监督，而不一次性切掉SFT？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Achord">CHORD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>专家数据可在探索初期提供稳定方向，但长期过强模仿会限制新策略；动态退火结合词元不确定性权重，让监督与探索平滑交接。它仍需控制专家与当前策略的分布差异，不保证混合必然优于分阶段。本地专家候选只是代理，未训练词元不确定性模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生开始解题时保留教师步骤指导，逐渐熟练后更多依靠任务奖励；不是到某一步突然完全忘掉专家，也不是始终固定等权。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.11408">原论文</a> · <a href="../../../../post-training/2508.11408-chord/">实现解读</a> · <a href="#qa-751d193dd884b093">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:spiral" data-paper-title="SPIRAL" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="SPIRAL LLM 后训练 Apple 2025-06-30 同一模型扮演出题者和解题者，在可自动判定的零和多轮语言游戏中形成逐步变难的课程。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.3438（+46.67%）；奖励、KL、长度和候选预算一致。  自博弈课程 LLM 后训练 数据与预算：下一份算力花在哪里 SPIRAL的出题者与解题者零和对抗，为什么仍需要可自动判定的游戏规则？ 对抗让双方随着对手变强而调整策略，可形成动态课程；但输赢必须由独立、明确的游戏规则决定，不能让出题者自己宣称解题者失败。零和奖励定义激励关系，不保证课程一定覆盖通用推理。本地只验证状态与目标，没有复刻大模型多轮自博弈训练。 例如出题者设计一个规则明确的文字博弈局面，解题者尝试获胜，程序裁定结果；不能允许出题者临时改规则把任何回答判输。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-spiral-8df7f07c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-7816033509093ce3">SPIRAL的出题者与解题者零和对抗，为什么仍需要可自动判定的游戏规则？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aspiral">SPIRAL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Apple</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>对抗让双方随着对手变强而调整策略，可形成动态课程；但输赢必须由独立、明确的游戏规则决定，不能让出题者自己宣称解题者失败。零和奖励定义激励关系，不保证课程一定覆盖通用推理。本地只验证状态与目标，没有复刻大模型多轮自博弈训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如出题者设计一个规则明确的文字博弈局面，解题者尝试获胜，程序裁定结果；不能允许出题者临时改规则把任何回答判输。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2506.24119">原论文</a> · <a href="../../../../post-training/2506.24119-spiral/">实现解读</a> · <a href="#qa-7816033509093ce3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:absolute-zero" data-paper-title="Absolute Zero" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Absolute Zero LLM 后训练 Tsinghua University 2025-05-06 proposer 自己生成可验证任务，solver 求解，程序 verifier 提供奖励；按当前能力边界组织课程。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.5938（+153.33%）；奖励、KL、长度和候选预算一致。  零数据自博弈 LLM 后训练 数据与预算：下一份算力花在哪里 Absolute Zero的自生成课程为什么仍离不开程序验证器？ 提议者产生任务，求解者给出解答，程序执行提供独立奖励，从而无需人工逐题标注。没有人工数据不表示没有监督来源，验证器与任务可执行性构成信号基础。若用任务自带答案直接馈给求解者，就破坏了闭环；本地机制诊断未复现完整大模型课程。 例如模型生成可执行代码任务并预测输出，实际运行程序核对；答案应由执行结果验证，不能把生成任务时保存的标准输出塞进求解提示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-absolute-zero-7e819456" class="ar-learning-paper-anchor"></span>
<h2 id="qa-97e862263943075f">Absolute Zero的自生成课程为什么仍离不开程序验证器？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aabsolute-zero">Absolute Zero</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>提议者产生任务，求解者给出解答，程序执行提供独立奖励，从而无需人工逐题标注。没有人工数据不表示没有监督来源，验证器与任务可执行性构成信号基础。若用任务自带答案直接馈给求解者，就破坏了闭环；本地机制诊断未复现完整大模型课程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型生成可执行代码任务并预测输出，实际运行程序核对；答案应由执行结果验证，不能把生成任务时保存的标准输出塞进求解提示。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.03335">原论文</a> · <a href="../../../../post-training/2505.03335-absolute-zero/">实现解读</a> · <a href="#qa-97e862263943075f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:raft" data-paper-title="RAFT" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="RAFT LLM 后训练 HKUST 2023-04-13 PPO 的在线更新不稳定，而在固定 SFT 数据上训练又无法持续利用变好的策略。RAFT 每轮从当前模型生成多个响应，用 reward model 排序并丢弃低质量样本，只对选中的高质量响应执行普通 maximum-likelihood fine-tuning，然后用新策略进入下一轮。 未训练真实生成式 LLM/reward model，也未复刻扩散模型实验。本页实现“当前策略采样 → reward 选优 → 只在保留响应上 SFT → 再采样”的迭代 rejection-sampling 路径，和 RRHF 的全排序 loss 分开。实现在线采样、reward ranking、top-response filtering 和迭代 SFT；未训练真实生成式 LLM/reward model，也未复刻扩散模型实验。候选策略结果只验证算法状态转移。公开 GSM8K candidate 512/128、300 steps、seed 42；  Reward 选优微调 LLM 后训练 数据与预算：下一份算力花在哪里 RAFT按奖励选优后做最大似然训练，和直接把奖励当策略梯度有何不同？ RAFT用奖励模型排序当前策略的多个回答，筛选高质量样本后执行普通监督微调；奖励决定样本选择，而非直接作为每个动作的梯度权重。新策略再生成下一轮数据，仍受奖励模型偏差与候选覆盖限制。本地候选策略只验证迭代采样和筛选状态转移。 例如从几篇候选摘要中选评分最高的一篇再学习其文字；没有出现的好摘要无法被选中，评分错误也可能被下一轮模仿放大。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-raft-fe9d648c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-e3b8808917c40363">RAFT按奖励选优后做最大似然训练，和直接把奖励当策略梯度有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Araft">RAFT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · HKUST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>RAFT用奖励模型排序当前策略的多个回答，筛选高质量样本后执行普通监督微调；奖励决定样本选择，而非直接作为每个动作的梯度权重。新策略再生成下一轮数据，仍受奖励模型偏差与候选覆盖限制。本地候选策略只验证迭代采样和筛选状态转移。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如从几篇候选摘要中选评分最高的一篇再学习其文字；没有出现的好摘要无法被选中，评分错误也可能被下一轮模仿放大。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2304.06767">原论文</a> · <a href="../../../../post-training/2304.06767-raft/">实现解读</a> · <a href="#qa-e3b8808917c40363">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

预算有限时，应该多生成问题、多做rollout，还是把监督集中在更有价值的位置？

## 记住这一点

先确定优化对象：问题选择改变学生会访问哪些状态，课程改变训练难度，监督/rollout裁剪改变单个样本的成本。当前模型变强后，旧难度标签会过期；数据选择也需要与目标任务和固定评估集分开。LESSER用输出层梯度特征降低选择成本，但它没有替换具体选择目标。理解节省了哪一步，再比较总预算与最终质量。

## 一个例子

设一天只允许生成100条回答。给已全部答对的问题再采样，可能提供很少新信息；只选完全不会的问题，又可能没有正奖励。可以在训练数据上重新估计当前成功率，选择仍有学习信号的难度带，并保留过难对照。若只生成半条回答，token纳入概率发生变化，原来的未加权目标也不能直接照搬。

## 什么时候要小心

快不等于学得更好，少token不等于同质量。需要计入教师前向、问题合成、筛选与失败重试的总成本，在validation选择课程或预算，再用隔离test报告。解析梯度或裁剪合同的CPU检查不证明真实训练加速；跨文字体系等知识迁移研究也不能被包装成已可执行优化器。

## 先读这几篇

先读GRPO Difficulty Curriculum，理解难度随当前policy变化；再读LESSER，把便宜的梯度特征与选择规则分开；最后读STOPD，看提前结束rollout为何需要明确采样与加权协议。

1. [A Step Harder, Not a Step Too Far: The Benefits and Limits of Curriculum Difficulty Progression in GRPO](../../../reproductions/2610.13669-grpo-difficulty-curriculum/README.md) · [原论文](https://arxiv.org/abs/2610.13669)
2. [LESSER: Post-Training Data Selection with Output-Layer Gradients](../../../post-training/2610.03702-lesser/README.md) · [原论文](https://arxiv.org/abs/2610.03702)
3. [Does On-Policy Distillation Need to Complete Every Rollout?](../../../post-training/2610.21337-stopd/README.md) · [原论文](https://arxiv.org/abs/2610.21337v1)

## 自测一下

上一轮容易的问题，这一轮还能直接沿用同一个“中等难度”标签吗？

??? note "展开参考答案"

    不能默认沿用。难度依赖当前策略和采样预算，模型更新后应按所用课程定义重新估计。重估只能读取训练/validation允许的信息，最终test不能参与挑题。预算不够时，应明确使用旧估计的局限，而非把固定问题长度当作成功率难度。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
