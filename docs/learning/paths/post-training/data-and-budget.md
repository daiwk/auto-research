---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 数据与预算：下一份算力花在哪里

[LLM 后训练](index.md) / 152 个问题 · 38 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

[阅读本主题精读卡片：多篇论文对比、分析与问答](../../deep-dives/post-training/data-and-budget.md)

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
<p class="ar-learning-status" data-learning-status role="status">152 个问题 · 38 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ask-to-distill" data-paper-title="Ask to Distill: Learning to Synthesize Data for On-Policy Distillation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Ask to Distill: Learning to Synthesize Data for On-Policy Distillation LLM 后训练 University of Illinois Urbana-Champaign 2026-10-20 问题决定学生会走到哪些前缀，因而决定教师能提供什么监督。A2D 冻结评分用的师生，训练独立的问题合成器；奖励同时要求“有差异”和“教师偏好的候选仍落在学生可达支持集”，然后筛选问题库，再从原始学生初始化执行 OPD。不是给每道问题做一次学生微调来估价。 完整实验成本过高，不复现（审查 DONE）。三 seed 仍只是机制诊断。仅实现 L1 奖励与更新公式组件，不是完整合成数据系统或能力复现。diagnostic_only=true；不可晋级、未接入 Evolve。完整实验成本过高，不复现（审查 DONE）。本页属于 10 月 21 日同一公告的补审，不是上一批之后的新首发。无下载、无预训练模型调用。随机生成的 logits、显式 mask 和外部 cluster share 只检查公式，不生成自然语言问题。CPU/CUDA 都运行同一算子；CUDA 不可用报错，不回退。输出不可覆盖，最多三个 seed；三 seed 仍只是机制诊断。  On-policy distillation 蒸馏数据合成与筛选 LLM 后训练 数据与预算：下一份算力花在哪里 A2D为什么训练问题合成器而非先直接训练学生？ 问题决定学生访问哪些前缀，也决定教师能提供什么帮助。先冻结评分师生、优化提问分布，再筛库并从原学生开始蒸馏，分开课程学习与学生更新。 例如先寻找学生有差距又能学的练习题，而非边改题边偷偷累计学生收益。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-ask-to-distill-6c38407f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-037eb7aa83d997b6">A2D为什么训练问题合成器而非先直接训练学生？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aask-to-distill">Ask to Distill: Learning to Synthesize Data for On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>问题决定学生访问哪些前缀，也决定教师能提供什么帮助。先冻结评分师生、优化提问分布，再筛库并从原学生开始蒸馏，分开课程学习与学生更新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先寻找学生有差距又能学的练习题，而非边改题边偷偷累计学生收益。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.27450v1">原论文</a> · <a href="../../../../post-training/2610.27450-ask-to-distill/">实现解读</a> · <a href="#qa-037eb7aa83d997b6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ask-to-distill" data-paper-title="Ask to Distill: Learning to Synthesize Data for On-Policy Distillation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Ask to Distill: Learning to Synthesize Data for On-Policy Distillation LLM 后训练 University of Illinois Urbana-Champaign 2026-10-20 问题决定学生会走到哪些前缀，因而决定教师能提供什么监督。A2D 冻结评分用的师生，训练独立的问题合成器；奖励同时要求“有差异”和“教师偏好的候选仍落在学生可达支持集”，然后筛选问题库，再从原始学生初始化执行 OPD。不是给每道问题做一次学生微调来估价。 完整实验成本过高，不复现（审查 DONE）。三 seed 仍只是机制诊断。仅实现 L1 奖励与更新公式组件，不是完整合成数据系统或能力复现。diagnostic_only=true；不可晋级、未接入 Evolve。完整实验成本过高，不复现（审查 DONE）。本页属于 10 月 21 日同一公告的补审，不是上一批之后的新首发。无下载、无预训练模型调用。随机生成的 logits、显式 mask 和外部 cluster share 只检查公式，不生成自然语言问题。CPU/CUDA 都运行同一算子；CUDA 不可用报错，不回退。输出不可覆盖，最多三个 seed；三 seed 仍只是机制诊断。  On-policy distillation 蒸馏数据合成与筛选 LLM 后训练 数据与预算：下一份算力花在哪里 A2D为什么既要求师生分歧大，又要求教师偏好落在学生可达支持集？ 只有分歧可能选到学生完全学不动的问题，只有兼容性又可能选到已掌握的问题。A2D用差异与兼容性的乘积奖励问题合成器；兼容性取教师在学生候选上的原始概率质量，不能重新归一化抹掉不可达部分。评分师生冻结，下游再从原始学生开始蒸馏。 例如学生会两种基本解法，教师还知道一种相近改进，问题有学习空间；若教师几乎只支持学生完全采不到的路线，兼容性应低。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ask-to-distill" data-paper-title="Ask to Distill: Learning to Synthesize Data for On-Policy Distillation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Ask to Distill: Learning to Synthesize Data for On-Policy Distillation LLM 后训练 University of Illinois Urbana-Champaign 2026-10-20 问题决定学生会走到哪些前缀，因而决定教师能提供什么监督。A2D 冻结评分用的师生，训练独立的问题合成器；奖励同时要求“有差异”和“教师偏好的候选仍落在学生可达支持集”，然后筛选问题库，再从原始学生初始化执行 OPD。不是给每道问题做一次学生微调来估价。 完整实验成本过高，不复现（审查 DONE）。三 seed 仍只是机制诊断。仅实现 L1 奖励与更新公式组件，不是完整合成数据系统或能力复现。diagnostic_only=true；不可晋级、未接入 Evolve。完整实验成本过高，不复现（审查 DONE）。本页属于 10 月 21 日同一公告的补审，不是上一批之后的新首发。无下载、无预训练模型调用。随机生成的 logits、显式 mask 和外部 cluster share 只检查公式，不生成自然语言问题。CPU/CUDA 都运行同一算子；CUDA 不可用报错，不回退。输出不可覆盖，最多三个 seed；三 seed 仍只是机制诊断。  On-policy distillation 蒸馏数据合成与筛选 LLM 后训练 数据与预算：下一份算力花在哪里 A2D的兼容性与纯师生分歧奖励有什么差别？ 分歧大可能表示任务完全不可达，兼容性看教师质量落在学生支持多少。乘积平衡学习空间与可达性，不把越难越远直接当越有价值。 例如教师只会学生从不支持的路线，分歧虽大仍可能低教学回报。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-694dff9b34d8b000">A2D的兼容性与纯师生分歧奖励有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aask-to-distill">Ask to Distill: Learning to Synthesize Data for On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分歧大可能表示任务完全不可达，兼容性看教师质量落在学生支持多少。乘积平衡学习空间与可达性，不把越难越远直接当越有价值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如教师只会学生从不支持的路线，分歧虽大仍可能低教学回报。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.27450v1">原论文</a> · <a href="../../../../post-training/2610.27450-ask-to-distill/">实现解读</a> · <a href="#qa-694dff9b34d8b000">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ask-to-distill" data-paper-title="Ask to Distill: Learning to Synthesize Data for On-Policy Distillation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Ask to Distill: Learning to Synthesize Data for On-Policy Distillation LLM 后训练 University of Illinois Urbana-Champaign 2026-10-20 问题决定学生会走到哪些前缀，因而决定教师能提供什么监督。A2D 冻结评分用的师生，训练独立的问题合成器；奖励同时要求“有差异”和“教师偏好的候选仍落在学生可达支持集”，然后筛选问题库，再从原始学生初始化执行 OPD。不是给每道问题做一次学生微调来估价。 完整实验成本过高，不复现（审查 DONE）。三 seed 仍只是机制诊断。仅实现 L1 奖励与更新公式组件，不是完整合成数据系统或能力复现。diagnostic_only=true；不可晋级、未接入 Evolve。完整实验成本过高，不复现（审查 DONE）。本页属于 10 月 21 日同一公告的补审，不是上一批之后的新首发。无下载、无预训练模型调用。随机生成的 logits、显式 mask 和外部 cluster share 只检查公式，不生成自然语言问题。CPU/CUDA 都运行同一算子；CUDA 不可用报错，不回退。输出不可覆盖，最多三个 seed；三 seed 仍只是机制诊断。  On-policy distillation 蒸馏数据合成与筛选 LLM 后训练 数据与预算：下一份算力花在哪里 A2D兼容概率为什么不能在并集内重新归一后再算？ 它需教师全词表在学生候选上的原始质量，重归一会隐藏并集外质量。重复惩罚按完整评分批聚类，非单GRPO组；下游候选优势也不再任意组标准化。 例如教师绝大部分质量在学生候选外，局部归一会把不可达程度夸成很兼容。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-403dedcf6fb8e94d">A2D兼容概率为什么不能在并集内重新归一后再算？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aask-to-distill">Ask to Distill: Learning to Synthesize Data for On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它需教师全词表在学生候选上的原始质量，重归一会隐藏并集外质量。重复惩罚按完整评分批聚类，非单GRPO组；下游候选优势也不再任意组标准化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如教师绝大部分质量在学生候选外，局部归一会把不可达程度夸成很兼容。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.27450v1">原论文</a> · <a href="../../../../post-training/2610.27450-ask-to-distill/">实现解读</a> · <a href="#qa-403dedcf6fb8e94d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tar-adaptive-replay" data-paper-title="Preserving Reasoning Diversity in Reinforcement Learning with Verifiable Rewards via Adaptive Replay" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Preserving Reasoning Diversity in Reinforcement Learning with Verifiable Rewards via Adaptive Replay LLM 后训练 Cornell University 2026-10-16 有限on-policy采样可能逐步压低同样正确但较少出现的推理模式；仅在当前rollout上重加权，难以恢复已经采不到的模式。TAR先从基础策略大量生成，过滤正确回答，再保留分散的原型轨迹。训练时只重放相对base已经被压制的轨迹，并将梯度集中到其中被压制的token，避免始终模仿有限bank限制策略适应。原文§3–4 原图建议：Figure 3压制比例与gated replay loss的机制分析图；原文未提供完整架构图，以上Mermaid是方法重绘，不冒充原图。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是数学推理或语义多样性复现。L1 定义性组件／梯度诊断，不是数学推理或语义多样性复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接Evolve。随机初始化16词表、8维GRU，base为当前初始策略的冻结副本。每个公开prompt实际采8个回答，外部合成verifier检查后，在base真实隐状态上做FPS并保留至多3条；未用gold、模板答案或手写候选填充bank。该随机初始隐状态不是语义encoder，只能验证FPS的定义，不能说明语义推理模式覆盖。  RLVR 多样性与经验重放 后训练算法组件 LLM 后训练 数据与预算：下一份算力花在哪里 TAR为什么先从base实际采到正确记忆？ 目标是保住基座已有但后训练压制的模式，必须真实生成并经训练verifier通过，再选分散原型；手写标准解无法证明原来可达，没正确候选就不建bank。 例如基座从未采出的解法，不能被包装成被遗忘的旧能力。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-tar-adaptive-replay-2e44ae67" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-58ca00fbe8a70481">TAR为什么先从base实际采到正确记忆？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atar-adaptive-replay">Preserving Reasoning Diversity in Reinforcement Learning with Verifiable Rewards via Adaptive Replay</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Cornell University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标是保住基座已有但后训练压制的模式，必须真实生成并经训练verifier通过，再选分散原型；手写标准解无法证明原来可达，没正确候选就不建bank。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如基座从未采出的解法，不能被包装成被遗忘的旧能力。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24236v1">原论文</a> · <a href="../../../../post-training/2610.24236-tar-adaptive-replay/">实现解读</a> · <a href="#qa-58ca00fbe8a70481">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tar-adaptive-replay" data-paper-title="Preserving Reasoning Diversity in Reinforcement Learning with Verifiable Rewards via Adaptive Replay" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Preserving Reasoning Diversity in Reinforcement Learning with Verifiable Rewards via Adaptive Replay LLM 后训练 Cornell University 2026-10-16 有限on-policy采样可能逐步压低同样正确但较少出现的推理模式；仅在当前rollout上重加权，难以恢复已经采不到的模式。TAR先从基础策略大量生成，过滤正确回答，再保留分散的原型轨迹。训练时只重放相对base已经被压制的轨迹，并将梯度集中到其中被压制的token，避免始终模仿有限bank限制策略适应。原文§3–4 原图建议：Figure 3压制比例与gated replay loss的机制分析图；原文未提供完整架构图，以上Mermaid是方法重绘，不冒充原图。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是数学推理或语义多样性复现。L1 定义性组件／梯度诊断，不是数学推理或语义多样性复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接Evolve。随机初始化16词表、8维GRU，base为当前初始策略的冻结副本。每个公开prompt实际采8个回答，外部合成verifier检查后，在base真实隐状态上做FPS并保留至多3条；未用gold、模板答案或手写候选填充bank。该随机初始隐状态不是语义encoder，只能验证FPS的定义，不能说明语义推理模式覆盖。  RLVR 多样性与经验重放 后训练算法组件 LLM 后训练 数据与预算：下一份算力花在哪里 TAR为什么只重放相对基础策略被压制的正确轨迹，而不是固定模仿整个记忆库？ 基础策略实际采样并经训练验证器筛出的正确轨迹用于保存多样解法。当前策略若未压低某条轨迹，其门控可以为零；若发生压制，再把损失集中到被压低的词元。轨迹门与词元权重都停止梯度，避免优化器通过改变门控取巧，测试答案不参与建库。 例如旧策略的代数解法逐渐采不到时才补学其中受压步骤；仍常见的图解轨迹无需重复强制模仿，也不能手编答案冒充旧采样。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tar-adaptive-replay" data-paper-title="Preserving Reasoning Diversity in Reinforcement Learning with Verifiable Rewards via Adaptive Replay" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Preserving Reasoning Diversity in Reinforcement Learning with Verifiable Rewards via Adaptive Replay LLM 后训练 Cornell University 2026-10-16 有限on-policy采样可能逐步压低同样正确但较少出现的推理模式；仅在当前rollout上重加权，难以恢复已经采不到的模式。TAR先从基础策略大量生成，过滤正确回答，再保留分散的原型轨迹。训练时只重放相对base已经被压制的轨迹，并将梯度集中到其中被压制的token，避免始终模仿有限bank限制策略适应。原文§3–4 原图建议：Figure 3压制比例与gated replay loss的机制分析图；原文未提供完整架构图，以上Mermaid是方法重绘，不冒充原图。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是数学推理或语义多样性复现。L1 定义性组件／梯度诊断，不是数学推理或语义多样性复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接Evolve。随机初始化16词表、8维GRU，base为当前初始策略的冻结副本。每个公开prompt实际采8个回答，外部合成verifier检查后，在base真实隐状态上做FPS并保留至多3条；未用gold、模板答案或手写候选填充bank。该随机初始隐状态不是语义encoder，只能验证FPS的定义，不能说明语义推理模式覆盖。  RLVR 多样性与经验重放 后训练算法组件 LLM 后训练 数据与预算：下一份算力花在哪里 TAR自适应重放与固定archive反复SFT有什么差别？ 只有相对base被压制时才开轨迹门，并聚焦受压词元，避免已掌握部分持续限制新适应。固定回放始终提供监督，不具这种按当前压制变化的选择。 例如某旧解法仍常见时可不额外回放，后来下降再补。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-267997e69aa769dd">TAR自适应重放与固定archive反复SFT有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atar-adaptive-replay">Preserving Reasoning Diversity in Reinforcement Learning with Verifiable Rewards via Adaptive Replay</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Cornell University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只有相对base被压制时才开轨迹门，并聚焦受压词元，避免已掌握部分持续限制新适应。固定回放始终提供监督，不具这种按当前压制变化的选择。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某旧解法仍常见时可不额外回放，后来下降再补。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24236v1">原论文</a> · <a href="../../../../post-training/2610.24236-tar-adaptive-replay/">实现解读</a> · <a href="#qa-267997e69aa769dd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:tar-adaptive-replay" data-paper-title="Preserving Reasoning Diversity in Reinforcement Learning with Verifiable Rewards via Adaptive Replay" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Preserving Reasoning Diversity in Reinforcement Learning with Verifiable Rewards via Adaptive Replay LLM 后训练 Cornell University 2026-10-16 有限on-policy采样可能逐步压低同样正确但较少出现的推理模式；仅在当前rollout上重加权，难以恢复已经采不到的模式。TAR先从基础策略大量生成，过滤正确回答，再保留分散的原型轨迹。训练时只重放相对base已经被压制的轨迹，并将梯度集中到其中被压制的token，避免始终模仿有限bank限制策略适应。原文§3–4 原图建议：Figure 3压制比例与gated replay loss的机制分析图；原文未提供完整架构图，以上Mermaid是方法重绘，不冒充原图。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是数学推理或语义多样性复现。L1 定义性组件／梯度诊断，不是数学推理或语义多样性复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接Evolve。随机初始化16词表、8维GRU，base为当前初始策略的冻结副本。每个公开prompt实际采8个回答，外部合成verifier检查后，在base真实隐状态上做FPS并保留至多3条；未用gold、模板答案或手写候选填充bank。该随机初始隐状态不是语义encoder，只能验证FPS的定义，不能说明语义推理模式覆盖。  RLVR 多样性与经验重放 后训练算法组件 LLM 后训练 数据与预算：下一份算力花在哪里 TAR能仅对活跃门的轨迹平均loss吗？ 不能，按全部bank轨迹平均，零gate也在分母；门与token权重都detach，半精度内部需稳定计算。只除活跃数会随激活比例额外放大回放。 例如只一条被压制时，改活跃分母会让它比规定全bank均值强很多。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c32e3a7b26d024e5">TAR能仅对活跃门的轨迹平均loss吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atar-adaptive-replay">Preserving Reasoning Diversity in Reinforcement Learning with Verifiable Rewards via Adaptive Replay</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Cornell University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，按全部bank轨迹平均，零gate也在分母；门与token权重都detach，半精度内部需稳定计算。只除活跃数会随激活比例额外放大回放。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只一条被压制时，改活跃分母会让它比规定全bank均值强很多。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24236v1">原论文</a> · <a href="../../../../post-training/2610.24236-tar-adaptive-replay/">实现解读</a> · <a href="#qa-c32e3a7b26d024e5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:stopd" data-paper-title="Does On-Policy Distillation Need to Complete Every Rollout?" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Does On-Policy Distillation Need to Complete Every Rollout? LLM 后训练 Cornell University 2026-10-15 每条响应在生成之前独立采样 anchor，向上取整到 block 末尾，学生只生成到该 cutoff 或自然 EOS。保留的每个 token 都接收教师监督，并按其精确 inclusion probability 加权；自然 EOS 也是普通有效 token。若把截断结果直接除以本批随机 token 数，不能沿用无偏 gradient-sum 的论证，所以实现使用前一批加权 token count。 完整长 rollout 训练成本过高，不复现（审查 DONE）；L1 cutoff / IPW / lagged normalizer 组件，真实短策略更新。完整长 rollout 训练成本过高，不复现（审查 DONE）；不是固定前缀截断的改名。固定公开 Hamlet 1524，revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784；byte 范围 80%/10%/10% 隔离。微型教师 next-token 训练后冻结，学生真实在线生成；  On-policy distillation 后训练算法组件 STOPD LLM 后训练 数据与预算：下一份算力花在哪里 STOPD为什么在生成前随机选cutoff？ 预先独立抽取可明确每个位置被保留的概率，并实际节省后续生成；生成完再截只能省监督且可能引入选择偏差。自然EOS仍是有效词元。 例如先决定最多走到某块末尾，而不是看完答案再挑最有利长度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-stopd-818867f2" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0ade71d0b770864e">STOPD为什么在生成前随机选cutoff？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Astopd">Does On-Policy Distillation Need to Complete Every Rollout?</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Cornell University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>预先独立抽取可明确每个位置被保留的概率，并实际节省后续生成；生成完再截只能省监督且可能引入选择偏差。自然EOS仍是有效词元。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先决定最多走到某块末尾，而不是看完答案再挑最有利长度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21337v1">原论文</a> · <a href="../../../../post-training/2610.21337-stopd/">实现解读</a> · <a href="#qa-0ade71d0b770864e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:stopd" data-paper-title="Does On-Policy Distillation Need to Complete Every Rollout?" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Does On-Policy Distillation Need to Complete Every Rollout? LLM 后训练 Cornell University 2026-10-15 每条响应在生成之前独立采样 anchor，向上取整到 block 末尾，学生只生成到该 cutoff 或自然 EOS。保留的每个 token 都接收教师监督，并按其精确 inclusion probability 加权；自然 EOS 也是普通有效 token。若把截断结果直接除以本批随机 token 数，不能沿用无偏 gradient-sum 的论证，所以实现使用前一批加权 token count。 完整长 rollout 训练成本过高，不复现（审查 DONE）；L1 cutoff / IPW / lagged normalizer 组件，真实短策略更新。完整长 rollout 训练成本过高，不复现（审查 DONE）；不是固定前缀截断的改名。固定公开 Hamlet 1524，revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784；byte 范围 80%/10%/10% 隔离。微型教师 next-token 训练后冻结，学生真实在线生成；  On-policy distillation 后训练算法组件 STOPD LLM 后训练 数据与预算：下一份算力花在哪里 STOPD按截断位置的逆概率加权，为什么还不能用本批随机词元数直接归一化？ 预先随机截断使后面词元更少被观测，精确纳入概率的倒数可校正梯度和。但随机分子再除以同批随机分母，并不自动保持无偏。方法使用前批的加权计数作当前归一量，权重和分母不参与微分；结论也不是每次优化器更新都等于完整生成。 例如后段步骤只有部分截断计划能保留，应增加其权重；但不能因此宣称一次短生成的平均损失必定与完整长回答相同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:stopd" data-paper-title="Does On-Policy Distillation Need to Complete Every Rollout?" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Does On-Policy Distillation Need to Complete Every Rollout? LLM 后训练 Cornell University 2026-10-15 每条响应在生成之前独立采样 anchor，向上取整到 block 末尾，学生只生成到该 cutoff 或自然 EOS。保留的每个 token 都接收教师监督，并按其精确 inclusion probability 加权；自然 EOS 也是普通有效 token。若把截断结果直接除以本批随机 token 数，不能沿用无偏 gradient-sum 的论证，所以实现使用前一批加权 token count。 完整长 rollout 训练成本过高，不复现（审查 DONE）；L1 cutoff / IPW / lagged normalizer 组件，真实短策略更新。完整长 rollout 训练成本过高，不复现（审查 DONE）；不是固定前缀截断的改名。固定公开 Hamlet 1524，revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784；byte 范围 80%/10%/10% 隔离。微型教师 next-token 训练后冻结，学生真实在线生成；  On-policy distillation 后训练算法组件 STOPD LLM 后训练 数据与预算：下一份算力花在哪里 逆纳入概率保证梯度和无偏，等于每次Adam更新相同吗？ 不等于。随机和的期望可匹配完整和，但归一和非线性优化器还有额外状态。不能把无偏性直接扩大到每批参数更新或训练结果完全一样。 例如两次短采样平均接近全和，不代表每次自适应步长都与完整批一致。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ba0afc9a512a246e">逆纳入概率保证梯度和无偏，等于每次Adam更新相同吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Astopd">Does On-Policy Distillation Need to Complete Every Rollout?</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Cornell University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不等于。随机和的期望可匹配完整和，但归一和非线性优化器还有额外状态。不能把无偏性直接扩大到每批参数更新或训练结果完全一样。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两次短采样平均接近全和，不代表每次自适应步长都与完整批一致。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21337v1">原论文</a> · <a href="../../../../post-training/2610.21337-stopd/">实现解读</a> · <a href="#qa-ba0afc9a512a246e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:stopd" data-paper-title="Does On-Policy Distillation Need to Complete Every Rollout?" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Does On-Policy Distillation Need to Complete Every Rollout? LLM 后训练 Cornell University 2026-10-15 每条响应在生成之前独立采样 anchor，向上取整到 block 末尾，学生只生成到该 cutoff 或自然 EOS。保留的每个 token 都接收教师监督，并按其精确 inclusion probability 加权；自然 EOS 也是普通有效 token。若把截断结果直接除以本批随机 token 数，不能沿用无偏 gradient-sum 的论证，所以实现使用前一批加权 token count。 完整长 rollout 训练成本过高，不复现（审查 DONE）；L1 cutoff / IPW / lagged normalizer 组件，真实短策略更新。完整长 rollout 训练成本过高，不复现（审查 DONE）；不是固定前缀截断的改名。固定公开 Hamlet 1524，revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784；byte 范围 80%/10%/10% 隔离。微型教师 next-token 训练后冻结，学生真实在线生成；  On-policy distillation 后训练算法组件 STOPD LLM 后训练 数据与预算：下一份算力花在哪里 STOPD最后不足整块的位置如何算权重与normalizer？ 按精确覆盖概率处理短尾块，不能假定所有块等宽；使用前批加权计数作当前normalizer。计划分begin、loss、finish防复用，不能拿当前随机计数替代。 例如最大长度不是块宽整数倍时，尾部位置仍需正确纳入概率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-eb36605b4b19c6d7">STOPD最后不足整块的位置如何算权重与normalizer？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Astopd">Does On-Policy Distillation Need to Complete Every Rollout?</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Cornell University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>按精确覆盖概率处理短尾块，不能假定所有块等宽；使用前批加权计数作当前normalizer。计划分begin、loss、finish防复用，不能拿当前随机计数替代。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如最大长度不是块宽整数倍时，尾部位置仍需正确纳入概率。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21337v1">原论文</a> · <a href="../../../../post-training/2610.21337-stopd/">实现解读</a> · <a href="#qa-eb36605b4b19c6d7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:boundary-evo" data-paper-title="BoundaryEvo: Data-Model Co-Evolution at the Capability Boundary for Long-Chain Reasoning Distillation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="BoundaryEvo: Data-Model Co-Evolution at the Capability Boundary for Long-Chain Reasoning Distillation LLM 后训练 Shanghai Artificial Intelligence Laboratory 2026-10-09 长推理监督的价值随学生能力变化。BoundaryEvo 先不按 correctness 过滤地蒸馏少量教师行为做 capability priming，然后每轮用当前学生、固定 expert 和 analyzer 重估边界，保留仍未掌握的 replay 并补充新问题；选好问题后再生成并验证 fresh teacher trajectories。 短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：正式对照设计尚未执行；计划以相同学生的 teacher-primed checkpoint 为基线，边界筛选后 fresh teacher 轨迹 SFT 为实验组。本次只有短预算机制诊断，本短跑稳定相对提升不适用，不报告能力收益；空边界或无 Stage 2 更新保留失败。  Capability boundary Data-model co-evolution Reasoning distillation LLM 后训练 数据与预算：下一份算力花在哪里 BoundaryEvo为什么每轮重新评估旧问题？ 学生能力变化，原本有价值的边界题可能已掌握，旧replay需重新过筛并补新问题。课程与模型共同演化，而不是固定难题集永久回放。 例如原来不会的证明学会后，应转向新的能力缺口。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-boundary-evo-60ecea39" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f4d4c905d8f2b6ca">BoundaryEvo为什么每轮重新评估旧问题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aboundary-evo">BoundaryEvo: Data-Model Co-Evolution at the Capability Boundary for Long-Chain Reasoning Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Artificial Intelligence Laboratory</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>学生能力变化，原本有价值的边界题可能已掌握，旧replay需重新过筛并补新问题。课程与模型共同演化，而不是固定难题集永久回放。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如原来不会的证明学会后，应转向新的能力缺口。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13285">原论文</a> · <a href="../../../../reproductions/2610.13285-boundary-evo/">实现解读</a> · <a href="#qa-f4d4c905d8f2b6ca">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:boundary-evo" data-paper-title="BoundaryEvo: Data-Model Co-Evolution at the Capability Boundary for Long-Chain Reasoning Distillation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="BoundaryEvo: Data-Model Co-Evolution at the Capability Boundary for Long-Chain Reasoning Distillation LLM 后训练 Shanghai Artificial Intelligence Laboratory 2026-10-09 长推理监督的价值随学生能力变化。BoundaryEvo 先不按 correctness 过滤地蒸馏少量教师行为做 capability priming，然后每轮用当前学生、固定 expert 和 analyzer 重估边界，保留仍未掌握的 replay 并补充新问题；选好问题后再生成并验证 fresh teacher trajectories。 短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：正式对照设计尚未执行；计划以相同学生的 teacher-primed checkpoint 为基线，边界筛选后 fresh teacher 轨迹 SFT 为实验组。本次只有短预算机制诊断，本短跑稳定相对提升不适用，不报告能力收益；空边界或无 Stage 2 更新保留失败。  Capability boundary Data-model co-evolution Reasoning distillation LLM 后训练 数据与预算：下一份算力花在哪里 BoundaryEvo为什么先选能力边界问题，再重新生成并验证教师轨迹？ 问题是否值得学取决于当前学生与专家的差距，旧问题也需重新检查；确定问题后生成新教师轨迹并独立验证，可避免把旧错误答案跟随问题一起重用。初始行为预热与后续验证监督具有不同过滤规则，不能把预热未验答案宣传成正确标签。 例如学生已经学会某个分解题，就不必永久重放；新边界题即使问题合理，也要重新核验教师解法，不能沿用未经检查的旧稿。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:boundary-evo" data-paper-title="BoundaryEvo: Data-Model Co-Evolution at the Capability Boundary for Long-Chain Reasoning Distillation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="BoundaryEvo: Data-Model Co-Evolution at the Capability Boundary for Long-Chain Reasoning Distillation LLM 后训练 Shanghai Artificial Intelligence Laboratory 2026-10-09 长推理监督的价值随学生能力变化。BoundaryEvo 先不按 correctness 过滤地蒸馏少量教师行为做 capability priming，然后每轮用当前学生、固定 expert 和 analyzer 重估边界，保留仍未掌握的 replay 并补充新问题；选好问题后再生成并验证 fresh teacher trajectories。 短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：正式对照设计尚未执行；计划以相同学生的 teacher-primed checkpoint 为基线，边界筛选后 fresh teacher 轨迹 SFT 为实验组。本次只有短预算机制诊断，本短跑稳定相对提升不适用，不报告能力收益；空边界或无 Stage 2 更新保留失败。  Capability boundary Data-model co-evolution Reasoning distillation LLM 后训练 数据与预算：下一份算力花在哪里 capability priming与正式验证教师监督的区别是什么？ 初期少量行为预热不按正确性过滤，后阶段选题后生成fresh教师轨迹并独立验证。不能把前者未验数据描述成正确示范，也不能省去后者验收。 例如学习教师表达习惯与确认某题解法正确，是两个阶段标准。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-835c2c91ce077e66">capability priming与正式验证教师监督的区别是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aboundary-evo">BoundaryEvo: Data-Model Co-Evolution at the Capability Boundary for Long-Chain Reasoning Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Artificial Intelligence Laboratory</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>初期少量行为预热不按正确性过滤，后阶段选题后生成fresh教师轨迹并独立验证。不能把前者未验数据描述成正确示范，也不能省去后者验收。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学习教师表达习惯与确认某题解法正确，是两个阶段标准。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13285">原论文</a> · <a href="../../../../reproductions/2610.13285-boundary-evo/">实现解读</a> · <a href="#qa-835c2c91ce077e66">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:boundary-evo" data-paper-title="BoundaryEvo: Data-Model Co-Evolution at the Capability Boundary for Long-Chain Reasoning Distillation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="BoundaryEvo: Data-Model Co-Evolution at the Capability Boundary for Long-Chain Reasoning Distillation LLM 后训练 Shanghai Artificial Intelligence Laboratory 2026-10-09 长推理监督的价值随学生能力变化。BoundaryEvo 先不按 correctness 过滤地蒸馏少量教师行为做 capability priming，然后每轮用当前学生、固定 expert 和 analyzer 重估边界，保留仍未掌握的 replay 并补充新问题；选好问题后再生成并验证 fresh teacher trajectories。 短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：正式对照设计尚未执行；计划以相同学生的 teacher-primed checkpoint 为基线，边界筛选后 fresh teacher 轨迹 SFT 为实验组。本次只有短预算机制诊断，本短跑稳定相对提升不适用，不报告能力收益；空边界或无 Stage 2 更新保留失败。  Capability boundary Data-model co-evolution Reasoning distillation LLM 后训练 数据与预算：下一份算力花在哪里 BoundaryEvo在SFT前应固定哪些生成与验证记录？ 选题依据当前学生、固定expert和analyzer的差距及质量条件；新teacher轨迹验证后只监督响应token。测试参考不能参与选题，旧答案也不能直接冒充fresh生成。 例如换了新问题却复用另一题旧解，失去选题与监督的一致性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e98dde6a3c689662">BoundaryEvo在SFT前应固定哪些生成与验证记录？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aboundary-evo">BoundaryEvo: Data-Model Co-Evolution at the Capability Boundary for Long-Chain Reasoning Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Artificial Intelligence Laboratory</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>选题依据当前学生、固定expert和analyzer的差距及质量条件；新teacher轨迹验证后只监督响应token。测试参考不能参与选题，旧答案也不能直接冒充fresh生成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如换了新问题却复用另一题旧解，失去选题与监督的一致性。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13285">原论文</a> · <a href="../../../../reproductions/2610.13285-boundary-evo/">实现解读</a> · <a href="#qa-e98dde6a3c689662">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:branch-opd" data-paper-title="Branching On-Policy Distillation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Branching On-Policy Distillation LLM 后训练 Tsinghua University / SenseTime Research 2026-10-09 普通 OPD 每个前缀只看到一次后续。BranchOPD 用学生不确定性和师生分歧定位 fork，从同一冻结学生策略独立采样 suffix，前缀只计入一次；并用协议事件监督结束行为。分枝不是教师强制 token，也不按答案正确性筛选。 短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：计划基线为相同学生的单轨 OPD，实验组执行 student 分枝采样、teacher 计分与 PBR；本次没有实跑同预算基线，稳定相对提升不适用。  On-policy distillation Student-policy branching Protocol-boundary repair LLM 后训练 数据与预算：下一份算力花在哪里 BranchOPD为什么在不确定分叉处多采suffix？ 单条轨迹只展示一次后续，额外学生分枝可覆盖同一状态的多种选择，让教师指导更集中在有分歧的位置。分枝仍来自冻结学生而非教师直接指定。 例如一道证明转折有两种延续，可从相同前文独立尝试两条。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-branch-opd-974c9738" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-18b4958bb5fa31a4">BranchOPD为什么在不确定分叉处多采suffix？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Abranch-opd">Branching On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University / SenseTime Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单条轨迹只展示一次后续，额外学生分枝可覆盖同一状态的多种选择，让教师指导更集中在有分歧的位置。分枝仍来自冻结学生而非教师直接指定。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一道证明转折有两种延续，可从相同前文独立尝试两条。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13481">原论文</a> · <a href="../../../../reproductions/2610.13481-branch-opd/">实现解读</a> · <a href="#qa-18b4958bb5fa31a4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:branch-opd" data-paper-title="Branching On-Policy Distillation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Branching On-Policy Distillation LLM 后训练 Tsinghua University / SenseTime Research 2026-10-09 普通 OPD 每个前缀只看到一次后续。BranchOPD 用学生不确定性和师生分歧定位 fork，从同一冻结学生策略独立采样 suffix，前缀只计入一次；并用协议事件监督结束行为。分枝不是教师强制 token，也不按答案正确性筛选。 短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：计划基线为相同学生的单轨 OPD，实验组执行 student 分枝采样、teacher 计分与 PBR；本次没有实跑同预算基线，稳定相对提升不适用。  On-policy distillation Student-policy branching Protocol-boundary repair LLM 后训练 数据与预算：下一份算力花在哪里 BranchOPD从同一前缀分枝时，为什么前缀只应计算一次损失？ 分枝增加的是同一学生状态下的多种后续，若每条分枝都重复计算共享前缀，会无意放大早期词元权重。方法按不确定性与师生分歧选分叉，从冻结学生独立采样续写，再由教师评分；它不是教师强制续写，也不按答案正确性预筛分枝。 例如共享三步推理后生成两种续解，共享三步只记一次，两条后续各自受监督；否则增加分枝会顺带加重无关前文。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:branch-opd" data-paper-title="Branching On-Policy Distillation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Branching On-Policy Distillation LLM 后训练 Tsinghua University / SenseTime Research 2026-10-09 普通 OPD 每个前缀只看到一次后续。BranchOPD 用学生不确定性和师生分歧定位 fork，从同一冻结学生策略独立采样 suffix，前缀只计入一次；并用协议事件监督结束行为。分枝不是教师强制 token，也不按答案正确性筛选。 短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：计划基线为相同学生的单轨 OPD，实验组执行 student 分枝采样、teacher 计分与 PBR；本次没有实跑同预算基线，稳定相对提升不适用。  On-policy distillation Student-policy branching Protocol-boundary repair LLM 后训练 数据与预算：下一份算力花在哪里 按分歧分枝与只保留正确分枝有什么假设差别？ 前者不靠答案筛选，后者事后条件化结果，会改变采样分布。教师评分与协议结束监督也不能被成功过滤替代，否则预算与来源不再相同。 例如失败分枝仍提供怎样继续的状态，不能为了曲线好看全部删除。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-773ea46ef6380052">按分歧分枝与只保留正确分枝有什么假设差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Abranch-opd">Branching On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University / SenseTime Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者不靠答案筛选，后者事后条件化结果，会改变采样分布。教师评分与协议结束监督也不能被成功过滤替代，否则预算与来源不再相同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如失败分枝仍提供怎样继续的状态，不能为了曲线好看全部删除。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13481">原论文</a> · <a href="../../../../reproductions/2610.13481-branch-opd/">实现解读</a> · <a href="#qa-773ea46ef6380052">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:branch-opd" data-paper-title="Branching On-Policy Distillation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Branching On-Policy Distillation LLM 后训练 Tsinghua University / SenseTime Research 2026-10-09 普通 OPD 每个前缀只看到一次后续。BranchOPD 用学生不确定性和师生分歧定位 fork，从同一冻结学生策略独立采样 suffix，前缀只计入一次；并用协议事件监督结束行为。分枝不是教师强制 token，也不按答案正确性筛选。 短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：计划基线为相同学生的单轨 OPD，实验组执行 student 分枝采样、teacher 计分与 PBR；本次没有实跑同预算基线，稳定相对提升不适用。  On-policy distillation Student-policy branching Protocol-boundary repair LLM 后训练 数据与预算：下一份算力花在哪里 BranchOPD为什么共享前缀不能按分枝数重复计loss？ 新增的是后缀覆盖，重复前缀会无意提高其权重。需去重、对齐有效位置，PBR监督规定结束事件；不能把完整boxed后EOS规则泛化成任意早停。 例如一个前缀长出五枝，不应让前面无关词也自动学五次。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-9191245083f7512a">BranchOPD为什么共享前缀不能按分枝数重复计loss？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Abranch-opd">Branching On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University / SenseTime Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>新增的是后缀覆盖，重复前缀会无意提高其权重。需去重、对齐有效位置，PBR监督规定结束事件；不能把完整boxed后EOS规则泛化成任意早停。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个前缀长出五枝，不应让前面无关词也自动学五次。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13481">原论文</a> · <a href="../../../../reproductions/2610.13481-branch-opd/">实现解读</a> · <a href="#qa-9191245083f7512a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:grpo-difficulty-curriculum" data-paper-title="A Step Harder, Not a Step Too Far: The Benefits and Limits of Curriculum Difficulty Progression in GRPO" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="A Step Harder, Not a Step Too Far: The Benefits and Limits of Curriculum Difficulty Progression in GRPO LLM 后训练 Dalian Maritime University 2026-10-09 difficulty随当前policy变化，样本可能反复进出难度带。论文比较静态easy-to-hard、在线fixed-medium和B1→B5课程，进一步升到B5会退化。实现每步真实rollout重新估难、保留B5控制，不按problem长度或旧评分替代。 本次不复现原文完整B1→B5课程或B5退化。staged缩放成每步validation诊断，保持噪声容忍/恢复best checkpoint；本地对照口径：基线为相同checkpoint与配置的unfiltered、fixed-medium、static、staged、B5-too-hard；按实际effective-update/rollout预算解释；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  GRPO difficulty curriculum Current-policy recalibration Overly-hard degradation control LLM 后训练 数据与预算：下一份算力花在哪里 GRPO课程中的难度为什么随策略更新？ 以当前多次rollout成功率定义难度，学会后同题会变容易，遗忘后可重新变难。课程是动态状态选择，题面长度或旧固定分数都不是同一量。 例如昨日全错的短题今天常对，应该离开原来的困难带。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-grpo-difficulty-curriculum-3b9ce14e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d3963a5ac4b91e90">GRPO课程中的难度为什么随策略更新？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agrpo-difficulty-curriculum">A Step Harder, Not a Step Too Far: The Benefits and Limits of Curriculum Difficulty Progression in GRPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dalian Maritime University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>以当前多次rollout成功率定义难度，学会后同题会变容易，遗忘后可重新变难。课程是动态状态选择，题面长度或旧固定分数都不是同一量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如昨日全错的短题今天常对，应该离开原来的困难带。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13669">原论文</a> · <a href="../../../../reproductions/2610.13669-grpo-difficulty-curriculum/">实现解读</a> · <a href="#qa-d3963a5ac4b91e90">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:grpo-difficulty-curriculum" data-paper-title="A Step Harder, Not a Step Too Far: The Benefits and Limits of Curriculum Difficulty Progression in GRPO" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="A Step Harder, Not a Step Too Far: The Benefits and Limits of Curriculum Difficulty Progression in GRPO LLM 后训练 Dalian Maritime University 2026-10-09 difficulty随当前policy变化，样本可能反复进出难度带。论文比较静态easy-to-hard、在线fixed-medium和B1→B5课程，进一步升到B5会退化。实现每步真实rollout重新估难、保留B5控制，不按problem长度或旧评分替代。 本次不复现原文完整B1→B5课程或B5退化。staged缩放成每步validation诊断，保持噪声容忍/恢复best checkpoint；本地对照口径：基线为相同checkpoint与配置的unfiltered、fixed-medium、static、staged、B5-too-hard；按实际effective-update/rollout预算解释；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  GRPO difficulty curriculum Current-policy recalibration Overly-hard degradation control LLM 后训练 数据与预算：下一份算力花在哪里 GRPO难度课程为什么要随当前策略重测成功率，而不能按题目长度固定分级？ 难度取决于当前策略和采样预算，同一道题会随学习进出目标成功率区间。课程用真实生成的成功率分带，阶段选择依赖验证集；越往难处推进并不保证更好，因此还需要最难阶段对照。长度奖励是辅助目标，不能代替难度估计或用测试表现决定推进。 例如短算术题可能恰好是当前模型弱项，长题反而熟练；课程应依据当前多次解答是否成功，而不是字符串长短。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:grpo-difficulty-curriculum" data-paper-title="A Step Harder, Not a Step Too Far: The Benefits and Limits of Curriculum Difficulty Progression in GRPO" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="A Step Harder, Not a Step Too Far: The Benefits and Limits of Curriculum Difficulty Progression in GRPO LLM 后训练 Dalian Maritime University 2026-10-09 difficulty随当前policy变化，样本可能反复进出难度带。论文比较静态easy-to-hard、在线fixed-medium和B1→B5课程，进一步升到B5会退化。实现每步真实rollout重新估难、保留B5控制，不按problem长度或旧评分替代。 本次不复现原文完整B1→B5课程或B5退化。staged缩放成每步validation诊断，保持噪声容忍/恢复best checkpoint；本地对照口径：基线为相同checkpoint与配置的unfiltered、fixed-medium、static、staged、B5-too-hard；按实际effective-update/rollout预算解释；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  GRPO difficulty curriculum Current-policy recalibration Overly-hard degradation control LLM 后训练 数据与预算：下一份算力花在哪里 在线fixed-medium与不断升到最难带为何不等价？ 前者持续保持可学的中等成功区间，后者逐段推进可能进入几乎无信号区；原研究也保留最难阶段退化边界，不能把越难越好当通则。 例如课程越过能力边界后全组失败，难度更高却可能学不到。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d0bcbab33c779c96">在线fixed-medium与不断升到最难带为何不等价？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agrpo-difficulty-curriculum">A Step Harder, Not a Step Too Far: The Benefits and Limits of Curriculum Difficulty Progression in GRPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dalian Maritime University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者持续保持可学的中等成功区间，后者逐段推进可能进入几乎无信号区；原研究也保留最难阶段退化边界，不能把越难越好当通则。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如课程越过能力边界后全组失败，难度更高却可能学不到。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13669">原论文</a> · <a href="../../../../reproductions/2610.13669-grpo-difficulty-curriculum/">实现解读</a> · <a href="#qa-d0bcbab33c779c96">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:grpo-difficulty-curriculum" data-paper-title="A Step Harder, Not a Step Too Far: The Benefits and Limits of Curriculum Difficulty Progression in GRPO" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="A Step Harder, Not a Step Too Far: The Benefits and Limits of Curriculum Difficulty Progression in GRPO LLM 后训练 Dalian Maritime University 2026-10-09 difficulty随当前policy变化，样本可能反复进出难度带。论文比较静态easy-to-hard、在线fixed-medium和B1→B5课程，进一步升到B5会退化。实现每步真实rollout重新估难、保留B5控制，不按problem长度或旧评分替代。 本次不复现原文完整B1→B5课程或B5退化。staged缩放成每步validation诊断，保持噪声容忍/恢复best checkpoint；本地对照口径：基线为相同checkpoint与配置的unfiltered、fixed-medium、static、staged、B5-too-hard；按实际effective-update/rollout预算解释；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  GRPO difficulty curriculum Current-policy recalibration Overly-hard degradation control LLM 后训练 数据与预算：下一份算力花在哪里 课程阶段选择能看测试分或使用长度奖励定难度吗？ 不能，阶段只看验证并恢复所选checkpoint；长度奖励是辅助目标，不用于成功率难度gate。每步需真实rollout重估，不能把静态mock概率充当在线机制。 例如长回答不一定难，不能根据长度奖励高低直接决定进入哪个阶段。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-bf468dcf604fdc63">课程阶段选择能看测试分或使用长度奖励定难度吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agrpo-difficulty-curriculum">A Step Harder, Not a Step Too Far: The Benefits and Limits of Curriculum Difficulty Progression in GRPO</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dalian Maritime University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，阶段只看验证并恢复所选checkpoint；长度奖励是辅助目标，不用于成功率难度gate。每步需真实rollout重估，不能把静态mock概率充当在线机制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如长回答不一定难，不能根据长度奖励高低直接决定进入哪个阶段。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13669">原论文</a> · <a href="../../../../reproductions/2610.13669-grpo-difficulty-curriculum/">实现解读</a> · <a href="#qa-bf468dcf604fdc63">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:progressive-contraction" data-paper-title="Learning More by Training Less: Uncertainty-Guided Progressive Contraction for Efficient Reasoning Post-Training" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Learning More by Training Less: Uncertainty-Guided Progressive Contraction for Efficient Reasoning Post-Training LLM 后训练 National University of Singapore / Nanjing University 2026-10-09 正确teacher CoT也可能经过多种正确/错误后续的reasoning fork。论文对真实prefix做Monte Carlo continuation，按branch不确定性先收缩teacher pool，再经真实student probing epoch按当前NLL选top-M并重路由。teacher profiling与student训练曝光必须分开核算。 本页不声明未执行实验已经完成。本地对照口径：基线为同一真实verified teacher全集的full-SFT；相同epochs，teacher profiling成本不并入student exposure比率；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Monte Carlo reasoning tree Teacher-side uncertainty contraction Learner-aware SFT routing LLM 后训练 数据与预算：下一份算力花在哪里 渐进收缩为什么从正确轨迹中再挑高分支不确定性？ 正确结尾仍可能经过后续易错分叉，Monte Carlo续写估计可识别有教学价值状态。只看原轨迹正确与否会遗漏这些关键分叉。 例如一条正确推导在中途有多个易混公式，值得针对性学习。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-progressive-contraction-16120d48" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d7b2e9d5c5821ab1">渐进收缩为什么从正确轨迹中再挑高分支不确定性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aprogressive-contraction">Learning More by Training Less: Uncertainty-Guided Progressive Contraction for Efficient Reasoning Post-Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore / Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>正确结尾仍可能经过后续易错分叉，Monte Carlo续写估计可识别有教学价值状态。只看原轨迹正确与否会遗漏这些关键分叉。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一条正确推导在中途有多个易混公式，值得针对性学习。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12933">原论文</a> · <a href="../../../../reproductions/2610.12933-progressive-contraction/">实现解读</a> · <a href="#qa-d7b2e9d5c5821ab1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:progressive-contraction" data-paper-title="Learning More by Training Less: Uncertainty-Guided Progressive Contraction for Efficient Reasoning Post-Training" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Learning More by Training Less: Uncertainty-Guided Progressive Contraction for Efficient Reasoning Post-Training LLM 后训练 National University of Singapore / Nanjing University 2026-10-09 正确teacher CoT也可能经过多种正确/错误后续的reasoning fork。论文对真实prefix做Monte Carlo continuation，按branch不确定性先收缩teacher pool，再经真实student probing epoch按当前NLL选top-M并重路由。teacher profiling与student训练曝光必须分开核算。 本页不声明未执行实验已经完成。本地对照口径：基线为同一真实verified teacher全集的full-SFT；相同epochs，teacher profiling成本不并入student exposure比率；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Monte Carlo reasoning tree Teacher-side uncertainty contraction Learner-aware SFT routing LLM 后训练 数据与预算：下一份算力花在哪里 渐进收缩为什么先测教师轨迹的分支不确定性，再按学生损失选训练子集？ 正确教师轨迹也可能经过后续容易分叉的位置，蒙特卡洛续写可识别这种学习价值。先按教师分支不确定性收缩池，再经真实学生探测，选当前损失较高的轨迹并重新路由。减少学生曝光量不等于相同倍数的总加速，教师探测成本必须另计。 例如两条都正确的证明，一条中间选择容易走错，先保留它；学生掌握后再换别的难点，不能只按答案是否正确筛选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:progressive-contraction" data-paper-title="Learning More by Training Less: Uncertainty-Guided Progressive Contraction for Efficient Reasoning Post-Training" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Learning More by Training Less: Uncertainty-Guided Progressive Contraction for Efficient Reasoning Post-Training LLM 后训练 National University of Singapore / Nanjing University 2026-10-09 正确teacher CoT也可能经过多种正确/错误后续的reasoning fork。论文对真实prefix做Monte Carlo continuation，按branch不确定性先收缩teacher pool，再经真实student probing epoch按当前NLL选top-M并重路由。teacher profiling与student训练曝光必须分开核算。 本页不声明未执行实验已经完成。本地对照口径：基线为同一真实verified teacher全集的full-SFT；相同epochs，teacher profiling成本不并入student exposure比率；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Monte Carlo reasoning tree Teacher-side uncertainty contraction Learner-aware SFT routing LLM 后训练 数据与预算：下一份算力花在哪里 教师profiling与学生NLL重路由分别解决什么？ 教师阶段找潜在推理难点，学生探测阶段判断当前学生尚未掌握什么。两层依据不同，不能把teacher难度分永久当作学生难度，也不能用静态长度代替。 例如教师认为难的步骤学生已会，学生路由可把预算转给别处。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a24601f33c222bf6">教师profiling与学生NLL重路由分别解决什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aprogressive-contraction">Learning More by Training Less: Uncertainty-Guided Progressive Contraction for Efficient Reasoning Post-Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore / Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>教师阶段找潜在推理难点，学生探测阶段判断当前学生尚未掌握什么。两层依据不同，不能把teacher难度分永久当作学生难度，也不能用静态长度代替。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如教师认为难的步骤学生已会，学生路由可把预算转给别处。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12933">原论文</a> · <a href="../../../../reproductions/2610.12933-progressive-contraction/">实现解读</a> · <a href="#qa-a24601f33c222bf6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:progressive-contraction" data-paper-title="Learning More by Training Less: Uncertainty-Guided Progressive Contraction for Efficient Reasoning Post-Training" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Learning More by Training Less: Uncertainty-Guided Progressive Contraction for Efficient Reasoning Post-Training LLM 后训练 National University of Singapore / Nanjing University 2026-10-09 正确teacher CoT也可能经过多种正确/错误后续的reasoning fork。论文对真实prefix做Monte Carlo continuation，按branch不确定性先收缩teacher pool，再经真实student probing epoch按当前NLL选top-M并重路由。teacher profiling与student训练曝光必须分开核算。 本页不声明未执行实验已经完成。本地对照口径：基线为同一真实verified teacher全集的full-SFT；相同epochs，teacher profiling成本不并入student exposure比率；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Monte Carlo reasoning tree Teacher-side uncertainty contraction Learner-aware SFT routing LLM 后训练 数据与预算：下一份算力花在哪里 曝光量减少为何不能直接写成总GPU加速倍数？ 公式只统计学生训练曝光，不包括教师真实续写profiling、学生探测和其他开销。需分别记账并保留真实生成证据，不能由少训练样本推算端到端速度。 例如前期花很多教师计算筛题，少两个epoch未必按比例省总时间。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b729b9b90aee1d77">曝光量减少为何不能直接写成总GPU加速倍数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aprogressive-contraction">Learning More by Training Less: Uncertainty-Guided Progressive Contraction for Efficient Reasoning Post-Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore / Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>公式只统计学生训练曝光，不包括教师真实续写profiling、学生探测和其他开销。需分别记账并保留真实生成证据，不能由少训练样本推算端到端速度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如前期花很多教师计算筛题，少两个epoch未必按比例省总时间。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12933">原论文</a> · <a href="../../../../reproductions/2610.12933-progressive-contraction/">实现解读</a> · <a href="#qa-b729b9b90aee1d77">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:synthself" data-paper-title="Continually Post-training Small Models via Synthetic Self-distillation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Continually Post-training Small Models via Synthetic Self-distillation LLM 后训练 KAIST AI / LG AI Research 2026-10-09 小模型self-rewrite可能失真，直接SFT又可能偏离base分布。SynthSelf用更大的同家族aligner把train demonstration贪心离线改写，通过答案拒绝采样后SFT。不允许student读评测答案，也不以文本过滤替代真实训练。 默认GSM validation预先拆不重叠两片，只是同域acquisition/retention诊断。本地对照口径：基线为同初始学生与epochs的gold-SFT；另可unfiltered-rewrite消融，真实token预算不相同则明确记录；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Synthetic self-distillation Same-family aligner Offline rejection-sampled SFT LLM 后训练 数据与预算：下一份算力花在哪里 SynthSelf为什么让更大同家族模型改写训练示范？ 小模型自改写容易失真，而原示范风格未必适合学生；更大同家族aligner生成候选改写，经答案检查才监督学生。它不是改写越短越好。 例如把跳步证明改成学生可学的步骤，同时保持训练题结论正确。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-synthself-6e723ecb" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a53b09934bf1fdde">SynthSelf为什么让更大同家族模型改写训练示范？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asynthself">Continually Post-training Small Models via Synthetic Self-distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST AI / LG AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>小模型自改写容易失真，而原示范风格未必适合学生；更大同家族aligner生成候选改写，经答案检查才监督学生。它不是改写越短越好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把跳步证明改成学生可学的步骤，同时保持训练题结论正确。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13113">原论文</a> · <a href="../../../../reproductions/2610.13113-synthself/">实现解读</a> · <a href="#qa-a53b09934bf1fdde">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:synthself" data-paper-title="Continually Post-training Small Models via Synthetic Self-distillation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Continually Post-training Small Models via Synthetic Self-distillation LLM 后训练 KAIST AI / LG AI Research 2026-10-09 小模型self-rewrite可能失真，直接SFT又可能偏离base分布。SynthSelf用更大的同家族aligner把train demonstration贪心离线改写，通过答案拒绝采样后SFT。不允许student读评测答案，也不以文本过滤替代真实训练。 默认GSM validation预先拆不重叠两片，只是同域acquisition/retention诊断。本地对照口径：基线为同初始学生与epochs的gold-SFT；另可unfiltered-rewrite消融，真实token预算不相同则明确记录；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Synthetic self-distillation Same-family aligner Offline rejection-sampled SFT LLM 后训练 数据与预算：下一份算力花在哪里 SynthSelf为什么用较大的同家族改写器，并在改写后再次核对训练答案？ 小学生直接自改写可能引入错误，较大同家族模型用于把训练示范改成更适合学生学习的表达。改写经答案拒绝采样后才用于响应监督，且需实测分布与保真约束是否成立。改写器并不天然满足约束，评测答案也不能进入改写或学生输入。 例如把训练题的冗长正确解改成清晰步骤后，仍要检查结论一致；不能用测试题标准答案指导改写，再把得分称为泛化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:synthself" data-paper-title="Continually Post-training Small Models via Synthetic Self-distillation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Continually Post-training Small Models via Synthetic Self-distillation LLM 后训练 KAIST AI / LG AI Research 2026-10-09 小模型self-rewrite可能失真，直接SFT又可能偏离base分布。SynthSelf用更大的同家族aligner把train demonstration贪心离线改写，通过答案拒绝采样后SFT。不允许student读评测答案，也不以文本过滤替代真实训练。 默认GSM validation预先拆不重叠两片，只是同域acquisition/retention诊断。本地对照口径：基线为同初始学生与epochs的gold-SFT；另可unfiltered-rewrite消融，真实token预算不相同则明确记录；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Synthetic self-distillation Same-family aligner Offline rejection-sampled SFT LLM 后训练 数据与预算：下一份算力花在哪里 答案拒绝采样与仅检查文本格式有什么区别？ 格式合法不保证内容正确，拒绝采样要核对改写答案；原约束还需实际测改写分布与保真关系，不能因同家族就宣布必满足。 例如JSON完整但最后算错，仍不该进入有效训练改写。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-8a15e41148b5baa0">答案拒绝采样与仅检查文本格式有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asynthself">Continually Post-training Small Models via Synthetic Self-distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST AI / LG AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>格式合法不保证内容正确，拒绝采样要核对改写答案；原约束还需实际测改写分布与保真关系，不能因同家族就宣布必满足。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如JSON完整但最后算错，仍不该进入有效训练改写。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13113">原论文</a> · <a href="../../../../reproductions/2610.13113-synthself/">实现解读</a> · <a href="#qa-8a15e41148b5baa0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:synthself" data-paper-title="Continually Post-training Small Models via Synthetic Self-distillation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Continually Post-training Small Models via Synthetic Self-distillation LLM 后训练 KAIST AI / LG AI Research 2026-10-09 小模型self-rewrite可能失真，直接SFT又可能偏离base分布。SynthSelf用更大的同家族aligner把train demonstration贪心离线改写，通过答案拒绝采样后SFT。不允许student读评测答案，也不以文本过滤替代真实训练。 默认GSM validation预先拆不重叠两片，只是同域acquisition/retention诊断。本地对照口径：基线为同初始学生与epochs的gold-SFT；另可unfiltered-rewrite消融，真实token预算不相同则明确记录；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Synthetic self-distillation Same-family aligner Offline rejection-sampled SFT LLM 后训练 数据与预算：下一份算力花在哪里 SynthSelf的gold允许在哪些阶段出现？ 训练示范可供离线aligner改写与验收，学生输入不包含评测答案，测试标签不能筛选课程。真实学生SFT不可由文本过滤代替，既有失败和修后证据分别保留。 例如筛出正确文本但没做任何参数更新，尚不是完整训练实现。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-dd88b8babcbee15a">SynthSelf的gold允许在哪些阶段出现？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asynthself">Continually Post-training Small Models via Synthetic Self-distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST AI / LG AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>训练示范可供离线aligner改写与验收，学生输入不包含评测答案，测试标签不能筛选课程。真实学生SFT不可由文本过滤代替，既有失败和修后证据分别保留。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如筛出正确文本但没做任何参数更新，尚不是完整训练实现。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13113">原论文</a> · <a href="../../../../reproductions/2610.13113-synthself/">实现解读</a> · <a href="#qa-dd88b8babcbee15a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dial-opd" data-paper-title="DIAL-OPD: Learning More from Fewer Tokens in On-Policy Distillation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="DIAL-OPD: Learning More from Fewer Tokens in On-Policy Distillation LLM 后训练 Eastern Institute of Technology, Ningbo / The Hong Kong Polytechnic University 2026-10-08 用概率的对数均值调节教师—学生对数差异，降低两者都不认可的低概率 token 的监督优先级。按每条响应选取高分位置，未选位置仍保留为上下文。 核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式、可直接改路径运行的命令见checkpoint 运行说明。  On-policy distillation Token supervision LLM 后训练 数据与预算：下一份算力花在哪里 DIAL-OPD为什么在大log差之外乘概率对数均值？ 两模型都极低概率的词也可出现大log差，尺度因子降低这类噪声位置优先级，突出有较实际支持的分歧。选中并不等于已被verifier认定错误。 例如一个怪词两边都不想要，差十倍也未必比关键数字的小差更有价值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-dial-opd-c9cdfa1a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5413860493b450f1">DIAL-OPD为什么在大log差之外乘概率对数均值？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adial-opd">DIAL-OPD: Learning More from Fewer Tokens in On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Eastern Institute of Technology, Ningbo / The Hong Kong Polytechnic University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两模型都极低概率的词也可出现大log差，尺度因子降低这类噪声位置优先级，突出有较实际支持的分歧。选中并不等于已被verifier认定错误。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个怪词两边都不想要，差十倍也未必比关键数字的小差更有价值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11659">原论文</a> · <a href="../../../../post-training/2610.11659-dial-opd/">实现解读</a> · <a href="#qa-5413860493b450f1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dial-opd" data-paper-title="DIAL-OPD: Learning More from Fewer Tokens in On-Policy Distillation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="DIAL-OPD: Learning More from Fewer Tokens in On-Policy Distillation LLM 后训练 Eastern Institute of Technology, Ningbo / The Hong Kong Polytechnic University 2026-10-08 用概率的对数均值调节教师—学生对数差异，降低两者都不认可的低概率 token 的监督优先级。按每条响应选取高分位置，未选位置仍保留为上下文。 核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式、可直接改路径运行的命令见checkpoint 运行说明。  On-policy distillation Token supervision LLM 后训练 数据与预算：下一份算力花在哪里 DIAL-OPD为什么不直接按师生对数概率差最大的词元选择监督？ 两者都认为极不可能的词元也可能有很大对数差，单看差值会高估其训练价值。概率对数均值提供尺度调节，再结合差异选位置；未选位置仍保留在上下文，只是不计对应损失。选择监督位置不会自动减少生成成本，也不保证每个大分歧都是知识错误。 例如教师和学生都几乎不支持一个怪词，它们的对数差仍很大；尺度调节让正常关键步骤的分歧有机会优先受监督。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dial-opd" data-paper-title="DIAL-OPD: Learning More from Fewer Tokens in On-Policy Distillation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="DIAL-OPD: Learning More from Fewer Tokens in On-Policy Distillation LLM 后训练 Eastern Institute of Technology, Ningbo / The Hong Kong Polytechnic University 2026-10-08 用概率的对数均值调节教师—学生对数差异，降低两者都不认可的低概率 token 的监督优先级。按每条响应选取高分位置，未选位置仍保留为上下文。 核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式、可直接改路径运行的命令见checkpoint 运行说明。  On-policy distillation Token supervision LLM 后训练 数据与预算：下一份算力花在哪里 DIAL只监督部分位置与删除未选文本有何区别？ 未选位置仍作为条件上下文保留，只屏蔽对应loss。删除文本会改变后续前缀和教师分布，已不再是相同学生轨迹上的稀疏监督。 例如不学习中间连接词，后续数字仍需读到它之前的完整算式。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-6ea92af295c46f6f">DIAL只监督部分位置与删除未选文本有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adial-opd">DIAL-OPD: Learning More from Fewer Tokens in On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Eastern Institute of Technology, Ningbo / The Hong Kong Polytechnic University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>未选位置仍作为条件上下文保留，只屏蔽对应loss。删除文本会改变后续前缀和教师分布，已不再是相同学生轨迹上的稀疏监督。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如不学习中间连接词，后续数字仍需读到它之前的完整算式。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11659">原论文</a> · <a href="../../../../post-training/2610.11659-dial-opd/">实现解读</a> · <a href="#qa-6ea92af295c46f6f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dial-opd" data-paper-title="DIAL-OPD: Learning More from Fewer Tokens in On-Policy Distillation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="DIAL-OPD: Learning More from Fewer Tokens in On-Policy Distillation LLM 后训练 Eastern Institute of Technology, Ningbo / The Hong Kong Polytechnic University 2026-10-08 用概率的对数均值调节教师—学生对数差异，降低两者都不认可的低概率 token 的监督优先级。按每条响应选取高分位置，未选位置仍保留为上下文。 核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式、可直接改路径运行的命令见checkpoint 运行说明。  On-policy distillation Token supervision LLM 后训练 数据与预算：下一份算力花在哪里 DIAL对p=q的对数均值怎么处理？ 用连续极限避免零除零；有效响应内按每条规定配额选择，优势停止梯度，只沿末学生logp更新。不能先全batch统一排名导致长回答独占配额。 例如两概率相等时数学上有有限极限，不应返回NaN或任意大分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d5031e3253e24536">DIAL对p=q的对数均值怎么处理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adial-opd">DIAL-OPD: Learning More from Fewer Tokens in On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Eastern Institute of Technology, Ningbo / The Hong Kong Polytechnic University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用连续极限避免零除零；有效响应内按每条规定配额选择，优势停止梯度，只沿末学生logp更新。不能先全batch统一排名导致长回答独占配额。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两概率相等时数学上有有限极限，不应返回NaN或任意大分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11659">原论文</a> · <a href="../../../../post-training/2610.11659-dial-opd/">实现解读</a> · <a href="#qa-d5031e3253e24536">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:grpo-dropout" data-paper-title="GRPODropout: Less is More for Online Reinforcement Learning Rollouts" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="GRPODropout: Less is More for Online Reinforcement Learning Rollouts LLM 后训练 Harbin Institute of Technology (Shenzhen) 2026-10-08 从同一 prompt 的 GRPO 响应组中筛除部分高概率、正优势响应，并用旧策略概率重新中心化保留响应的优势。不是随机 dropout，也不改变生成预算。 核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式和命令见checkpoint 运行说明。  RLVR Rollout selection LLM 后训练 数据与预算：下一份算力花在哪里 GRPODropout为什么删部分高概率正优势回答？ 这些样本可能继续集中已占优模式，按熵贡献选择性减少其更新，并保留失败负反馈。它不是随机丢神经元，也没有减少已付出的rollout生成预算。 例如同一常见正确模板反复出现，可少强化其中一些重复优势。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-grpo-dropout-a03001b8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-94cea1800fc90264">GRPODropout为什么删部分高概率正优势回答？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agrpo-dropout">GRPODropout: Less is More for Online Reinforcement Learning Rollouts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Institute of Technology (Shenzhen)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这些样本可能继续集中已占优模式，按熵贡献选择性减少其更新，并保留失败负反馈。它不是随机丢神经元，也没有减少已付出的rollout生成预算。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一常见正确模板反复出现，可少强化其中一些重复优势。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11854">原论文</a> · <a href="../../../../post-training/2610.11854-grpo-dropout/">实现解读</a> · <a href="#qa-94cea1800fc90264">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:grpo-dropout" data-paper-title="GRPODropout: Less is More for Online Reinforcement Learning Rollouts" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="GRPODropout: Less is More for Online Reinforcement Learning Rollouts LLM 后训练 Harbin Institute of Technology (Shenzhen) 2026-10-08 从同一 prompt 的 GRPO 响应组中筛除部分高概率、正优势响应，并用旧策略概率重新中心化保留响应的优势。不是随机 dropout，也不改变生成预算。 核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式和命令见checkpoint 运行说明。  RLVR Rollout selection LLM 后训练 数据与预算：下一份算力花在哪里 GRPODropout为何筛掉部分高概率正优势响应，却恢复所有非正优势响应？ 高概率且正优势的响应可能进一步强化已占优势的模式，筛选依据是它们对熵变化的贡献，而非随机丢弃。保留负向反馈后，再按旧策略概率重新中心化优势，避免筛选改变基线。生成预算并未因此减少，节约更新样本不等于少生成。 例如一组里常见正确模板过度主导，可少学其中部分重复回答；失败回答仍用于惩罚，不能删掉后把剩余样本都视为正例。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:grpo-dropout" data-paper-title="GRPODropout: Less is More for Online Reinforcement Learning Rollouts" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="GRPODropout: Less is More for Online Reinforcement Learning Rollouts LLM 后训练 Harbin Institute of Technology (Shenzhen) 2026-10-08 从同一 prompt 的 GRPO 响应组中筛除部分高概率、正优势响应，并用旧策略概率重新中心化保留响应的优势。不是随机 dropout，也不改变生成预算。 核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式和命令见checkpoint 运行说明。  RLVR Rollout selection LLM 后训练 数据与预算：下一份算力花在哪里 响应dropout与生成前少采几条有什么成本差异？ 前者先生成再筛训练，仍支付全组生成；后者减少数据覆盖和生成成本，改变估计条件。不能把少反传响应自动写成同等比例的端到端采样加速。 例如八条都生成后只用六条，不等于只花六条生成的时间。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4ca549af2d7ba6d5">响应dropout与生成前少采几条有什么成本差异？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agrpo-dropout">GRPODropout: Less is More for Online Reinforcement Learning Rollouts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Institute of Technology (Shenzhen)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者先生成再筛训练，仍支付全组生成；后者减少数据覆盖和生成成本，改变估计条件。不能把少反传响应自动写成同等比例的端到端采样加速。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如八条都生成后只用六条，不等于只花六条生成的时间。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11854">原论文</a> · <a href="../../../../post-training/2610.11854-grpo-dropout/">实现解读</a> · <a href="#qa-4ca549af2d7ba6d5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:grpo-dropout" data-paper-title="GRPODropout: Less is More for Online Reinforcement Learning Rollouts" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="GRPODropout: Less is More for Online Reinforcement Learning Rollouts LLM 后训练 Harbin Institute of Technology (Shenzhen) 2026-10-08 从同一 prompt 的 GRPO 响应组中筛除部分高概率、正优势响应，并用旧策略概率重新中心化保留响应的优势。不是随机 dropout，也不改变生成预算。 核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式和命令见checkpoint 运行说明。  RLVR Rollout selection LLM 后训练 数据与预算：下一份算力花在哪里 GRPODropout删除后能用原组优势不再中心化吗？ 需要按保留项旧策略概率重新中心化，且所有非正优势响应恢复。忽略任一会改变均值和负反馈结构，不能把简单随机去两条称原算法。 例如删掉强正样本后组基准已变化，原优势并不自动仍满足规定中心。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ddbbf23888330984">GRPODropout删除后能用原组优势不再中心化吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agrpo-dropout">GRPODropout: Less is More for Online Reinforcement Learning Rollouts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Institute of Technology (Shenzhen)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>需要按保留项旧策略概率重新中心化，且所有非正优势响应恢复。忽略任一会改变均值和负反馈结构，不能把简单随机去两条称原算法。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如删掉强正样本后组基准已变化，原优势并不自动仍满足规定中心。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11854">原论文</a> · <a href="../../../../post-training/2610.11854-grpo-dropout/">实现解读</a> · <a href="#qa-ddbbf23888330984">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:magicbeanstalk" data-paper-title="MagicBeanStalk: Escaping the RLVR Zero Advantage Trap with Recursive Data Synthesis" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="MagicBeanStalk: Escaping the RLVR Zero Advantage Trap with Recursive Data Synthesis LLM 后训练 University of Washington 2026-10-08 RLVR有效性取决于problem、当前policy、rollout预算。MBS从verified hard seed提炼reasoning蓝图，自顶向下分解并实测child worked examples是否提高parent正确率，再合成更难新leaf、自底向上按原依赖组合。最终独立验证、保蓝图和实质新颖性，并满足目标policy Goldilocks及预算内完整正确解。 当前状态（2026-10-14）：成本过高，暂不复现／完整方法待验收。本轮新路径固定在 4c4710cd，仅依据 train/validation 教师短诊断提出，尚须新源码完整 GPU 验证。当前状态（2026-10-14）：成本过高，暂不复现／完整方法待验收。用户要求先交付其余成果，不再扩大候选池、更换教师或启动后续种子。本页保留论文解读、实验源码和所有失败证据；magicbeanstalk 只是历史计划键，已从可执行 registry、批量 reproduce 和公开训练 runner 中移出，不是已完成实现，也未接入 evolve。  RLVR data synthesis Effectivity-validated decomposition Policy-calibrated Goldilocks LLM 后训练 数据与预算：下一份算力花在哪里 MagicBeanStalk为什么递归分解再组合难题？ 硬题全错缺少优势，子题示例可揭示有效蓝图，再合成新叶并沿依赖组合，寻求当前策略既有对又有错的可学任务。合成合法不等于任务有效。 例如将复杂推导拆成可练的小环节，再组合成保留关键依赖的新题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-magicbeanstalk-9678e8db" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-32dc90312231b7d8">MagicBeanStalk为什么递归分解再组合难题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amagicbeanstalk">MagicBeanStalk: Escaping the RLVR Zero Advantage Trap with Recursive Data Synthesis</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>硬题全错缺少优势，子题示例可揭示有效蓝图，再合成新叶并沿依赖组合，寻求当前策略既有对又有错的可学任务。合成合法不等于任务有效。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如将复杂推导拆成可练的小环节，再组合成保留关键依赖的新题。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12659">原论文</a> · <a href="../../../../reproductions/2610.12659-magicbeanstalk/">实现解读</a> · <a href="#qa-32dc90312231b7d8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:magicbeanstalk" data-paper-title="MagicBeanStalk: Escaping the RLVR Zero Advantage Trap with Recursive Data Synthesis" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="MagicBeanStalk: Escaping the RLVR Zero Advantage Trap with Recursive Data Synthesis LLM 后训练 University of Washington 2026-10-08 RLVR有效性取决于problem、当前policy、rollout预算。MBS从verified hard seed提炼reasoning蓝图，自顶向下分解并实测child worked examples是否提高parent正确率，再合成更难新leaf、自底向上按原依赖组合。最终独立验证、保蓝图和实质新颖性，并满足目标policy Goldilocks及预算内完整正确解。 当前状态（2026-10-14）：成本过高，暂不复现／完整方法待验收。本轮新路径固定在 4c4710cd，仅依据 train/validation 教师短诊断提出，尚须新源码完整 GPU 验证。当前状态（2026-10-14）：成本过高，暂不复现／完整方法待验收。用户要求先交付其余成果，不再扩大候选池、更换教师或启动后续种子。本页保留论文解读、实验源码和所有失败证据；magicbeanstalk 只是历史计划键，已从可执行 registry、批量 reproduce 和公开训练 runner 中移出，不是已完成实现，也未接入 evolve。  RLVR data synthesis Effectivity-validated decomposition Policy-calibrated Goldilocks LLM 后训练 数据与预算：下一份算力花在哪里 MagicBeanStalk的子题有效性和最终Goldilocks筛选，为什么不能互相替代？ 子题示范是否提高父题成功率，检验依赖分解是否有效；最终任务还需对目标策略在给定预算下既非全对也非全错，并存在正常结束的正确解。两条件针对不同对象与阶段。局部教师诊断通过不代表递归构造成功，本地多次构造失败也须保留。 例如两个子题确实帮助另一个学生解父题，但目标模型仍一次都解不出合成题；这种任务仍未通过最终可学习性筛选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:magicbeanstalk" data-paper-title="MagicBeanStalk: Escaping the RLVR Zero Advantage Trap with Recursive Data Synthesis" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="MagicBeanStalk: Escaping the RLVR Zero Advantage Trap with Recursive Data Synthesis LLM 后训练 University of Washington 2026-10-08 RLVR有效性取决于problem、当前policy、rollout预算。MBS从verified hard seed提炼reasoning蓝图，自顶向下分解并实测child worked examples是否提高parent正确率，再合成更难新leaf、自底向上按原依赖组合。最终独立验证、保蓝图和实质新颖性，并满足目标policy Goldilocks及预算内完整正确解。 当前状态（2026-10-14）：成本过高，暂不复现／完整方法待验收。本轮新路径固定在 4c4710cd，仅依据 train/validation 教师短诊断提出，尚须新源码完整 GPU 验证。当前状态（2026-10-14）：成本过高，暂不复现／完整方法待验收。用户要求先交付其余成果，不再扩大候选池、更换教师或启动后续种子。本页保留论文解读、实验源码和所有失败证据；magicbeanstalk 只是历史计划键，已从可执行 registry、批量 reproduce 和公开训练 runner 中移出，不是已完成实现，也未接入 evolve。  RLVR data synthesis Effectivity-validated decomposition Policy-calibrated Goldilocks LLM 后训练 数据与预算：下一份算力花在哪里 子题effectivity与目标policy Goldilocks各验证什么？ 前者看子例是否提高某学生父题成功，后者看最终目标策略在规定预算是否有部分成功且至少正常结束正确。两阶段对象不同，前者不能替代后者。 例如辅助学生学得好，但目标模型仍全错，最终题仍不适合本轮训练。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-3edb9a183c7f314b">子题effectivity与目标policy Goldilocks各验证什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amagicbeanstalk">MagicBeanStalk: Escaping the RLVR Zero Advantage Trap with Recursive Data Synthesis</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者看子例是否提高某学生父题成功，后者看最终目标策略在规定预算是否有部分成功且至少正常结束正确。两阶段对象不同，前者不能替代后者。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如辅助学生学得好，但目标模型仍全错，最终题仍不适合本轮训练。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12659">原论文</a> · <a href="../../../../reproductions/2610.12659-magicbeanstalk/">实现解读</a> · <a href="#qa-3edb9a183c7f314b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:magicbeanstalk" data-paper-title="MagicBeanStalk: Escaping the RLVR Zero Advantage Trap with Recursive Data Synthesis" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="MagicBeanStalk: Escaping the RLVR Zero Advantage Trap with Recursive Data Synthesis LLM 后训练 University of Washington 2026-10-08 RLVR有效性取决于problem、当前policy、rollout预算。MBS从verified hard seed提炼reasoning蓝图，自顶向下分解并实测child worked examples是否提高parent正确率，再合成更难新leaf、自底向上按原依赖组合。最终独立验证、保蓝图和实质新颖性，并满足目标policy Goldilocks及预算内完整正确解。 当前状态（2026-10-14）：成本过高，暂不复现／完整方法待验收。本轮新路径固定在 4c4710cd，仅依据 train/validation 教师短诊断提出，尚须新源码完整 GPU 验证。当前状态（2026-10-14）：成本过高，暂不复现／完整方法待验收。用户要求先交付其余成果，不再扩大候选池、更换教师或启动后续种子。本页保留论文解读、实验源码和所有失败证据；magicbeanstalk 只是历史计划键，已从可执行 registry、批量 reproduce 和公开训练 runner 中移出，不是已完成实现，也未接入 evolve。  RLVR data synthesis Effectivity-validated decomposition Policy-calibrated Goldilocks LLM 后训练 数据与预算：下一份算力花在哪里 本地MBS格式合法的新题能直接进入实现通过状态吗？ 不能，还需完整正确解、独立验证、蓝图与新颖性以及有效性和Goldilocks检查。既有多次真实构造失败需保留，单次教师质量诊断不是整方法通过。 例如JSON与依赖图都合法，内容却无法解出，仍应记构造失败。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-41efd4ef1614f2c5">本地MBS格式合法的新题能直接进入实现通过状态吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Amagicbeanstalk">MagicBeanStalk: Escaping the RLVR Zero Advantage Trap with Recursive Data Synthesis</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，还需完整正确解、独立验证、蓝图与新颖性以及有效性和Goldilocks检查。既有多次真实构造失败需保留，单次教师质量诊断不是整方法通过。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如JSON与依赖图都合法，内容却无法解出，仍应记构造失败。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12659">原论文</a> · <a href="../../../../reproductions/2610.12659-magicbeanstalk/">实现解读</a> · <a href="#qa-41efd4ef1614f2c5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:pivot" data-paper-title="PIVOT: Perplexity-Informed KD-to-RL Transition Scheduling for Vertical-Domain Few-Shot Distillation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="PIVOT: Perplexity-Informed KD-to-RL Transition Scheduling for Vertical-Domain Few-Shot Distillation LLM 后训练 Ping An Technology / University of Science and Technology of China 2026-10-08 垂直领域的小模型既需要教师传授知识，也需要任务奖励改善最终判断；所有样本同时从蒸馏切换到 RL，可能使困难样本过早失去教师监督。PIVOT 在学生自己的响应上计算教师困惑度，先把低困惑度问题切换到 GRPO，高困惑度问题继续 OPD。 有界少样本、单 seed、LoRA 与短训练只验证机制，不复现原始 480 步/全参数/HWU64 能力收益。共享热身、样本级路由和三配方重置已在 A100 实跑；8 题诊断无准确率提升，不等于原论文能力复现。真实 Qwen2.5-0.5B-Instruct 学生、7B-Instruct 教师，q/v LoRA 而非原文全参数微调。所有配方共享教师响应两轮 SFT、初始 OPD 热身和相同初始 adapter；随后重置 optimizer 与随机种子，分别执行持续 OPD、固定半预算切换及样本级 PIVOT。  On-policy 蒸馏 组相对策略优化 LLM 后训练 数据与预算：下一份算力花在哪里 PIVOT为什么按问题而不是全训练同时从OPD切到RL？ 不同题学生准备程度不同，统一切换会让困难题过早失去教师。按教师对学生响应的困惑度排序，逐渐增加低困惑度题的RL比例，其他仍蒸馏。 例如已熟悉的题先自主探索，尚偏离教师的题继续有人指导。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-pivot-65855e82" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-184154fc1deeefdf">PIVOT为什么按问题而不是全训练同时从OPD切到RL？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Apivot">PIVOT: Perplexity-Informed KD-to-RL Transition Scheduling for Vertical-Domain Few-Shot Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ping An Technology / University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同题学生准备程度不同，统一切换会让困难题过早失去教师。按教师对学生响应的困惑度排序，逐渐增加低困惑度题的RL比例，其他仍蒸馏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如已熟悉的题先自主探索，尚偏离教师的题继续有人指导。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11167">原论文</a> · <a href="../../../../post-training/2610.11167-pivot/">实现解读</a> · <a href="#qa-184154fc1deeefdf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:pivot" data-paper-title="PIVOT: Perplexity-Informed KD-to-RL Transition Scheduling for Vertical-Domain Few-Shot Distillation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="PIVOT: Perplexity-Informed KD-to-RL Transition Scheduling for Vertical-Domain Few-Shot Distillation LLM 后训练 Ping An Technology / University of Science and Technology of China 2026-10-08 垂直领域的小模型既需要教师传授知识，也需要任务奖励改善最终判断；所有样本同时从蒸馏切换到 RL，可能使困难样本过早失去教师监督。PIVOT 在学生自己的响应上计算教师困惑度，先把低困惑度问题切换到 GRPO，高困惑度问题继续 OPD。 有界少样本、单 seed、LoRA 与短训练只验证机制，不复现原始 480 步/全参数/HWU64 能力收益。共享热身、样本级路由和三配方重置已在 A100 实跑；8 题诊断无准确率提升，不等于原论文能力复现。真实 Qwen2.5-0.5B-Instruct 学生、7B-Instruct 教师，q/v LoRA 而非原文全参数微调。所有配方共享教师响应两轮 SFT、初始 OPD 热身和相同初始 adapter；随后重置 optimizer 与随机种子，分别执行持续 OPD、固定半预算切换及样本级 PIVOT。  On-policy 蒸馏 组相对策略优化 LLM 后训练 数据与预算：下一份算力花在哪里 PIVOT为什么让低教师困惑度的问题先转RL，而高困惑度问题继续蒸馏？ 困惑度在学生自己的响应上计算，表示教师对学生当前行为的支持程度。较低时可较早依靠任务奖励探索，较高时继续获得教师监督；按问题组汇总后随训练逐步增加RL比例。它是路由依据，不是正确性判定，也不表示低困惑度问题必然简单。 例如教师已认可学生的一类解题步骤，这类题先转奖励训练；另一类仍频繁偏离教师分布，暂时保留蒸馏而非统一切换。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:pivot" data-paper-title="PIVOT: Perplexity-Informed KD-to-RL Transition Scheduling for Vertical-Domain Few-Shot Distillation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="PIVOT: Perplexity-Informed KD-to-RL Transition Scheduling for Vertical-Domain Few-Shot Distillation LLM 后训练 Ping An Technology / University of Science and Technology of China 2026-10-08 垂直领域的小模型既需要教师传授知识，也需要任务奖励改善最终判断；所有样本同时从蒸馏切换到 RL，可能使困难样本过早失去教师监督。PIVOT 在学生自己的响应上计算教师困惑度，先把低困惑度问题切换到 GRPO，高困惑度问题继续 OPD。 有界少样本、单 seed、LoRA 与短训练只验证机制，不复现原始 480 步/全参数/HWU64 能力收益。共享热身、样本级路由和三配方重置已在 A100 实跑；8 题诊断无准确率提升，不等于原论文能力复现。真实 Qwen2.5-0.5B-Instruct 学生、7B-Instruct 教师，q/v LoRA 而非原文全参数微调。所有配方共享教师响应两轮 SFT、初始 OPD 热身和相同初始 adapter；随后重置 optimizer 与随机种子，分别执行持续 OPD、固定半预算切换及样本级 PIVOT。  On-policy 蒸馏 组相对策略优化 LLM 后训练 数据与预算：下一份算力花在哪里 教师困惑度与verifier正确率为什么不能互换？ 困惑度衡量教师对学生文本的支持，正确率衡量任务结果。高支持可能仍错，低支持也可能是新有效解法；它是路由代理，不是独立答案验证。 例如教师不习惯学生新表达，并不证明该表达的结论错误。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-02788785d8815ca5">教师困惑度与verifier正确率为什么不能互换？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Apivot">PIVOT: Perplexity-Informed KD-to-RL Transition Scheduling for Vertical-Domain Few-Shot Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ping An Technology / University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>困惑度衡量教师对学生文本的支持，正确率衡量任务结果。高支持可能仍错，低支持也可能是新有效解法；它是路由代理，不是独立答案验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如教师不习惯学生新表达，并不证明该表达的结论错误。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11167">原论文</a> · <a href="../../../../post-training/2610.11167-pivot/">实现解读</a> · <a href="#qa-02788785d8815ca5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:pivot" data-paper-title="PIVOT: Perplexity-Informed KD-to-RL Transition Scheduling for Vertical-Domain Few-Shot Distillation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="PIVOT: Perplexity-Informed KD-to-RL Transition Scheduling for Vertical-Domain Few-Shot Distillation LLM 后训练 Ping An Technology / University of Science and Technology of China 2026-10-08 垂直领域的小模型既需要教师传授知识，也需要任务奖励改善最终判断；所有样本同时从蒸馏切换到 RL，可能使困难样本过早失去教师监督。PIVOT 在学生自己的响应上计算教师困惑度，先把低困惑度问题切换到 GRPO，高困惑度问题继续 OPD。 有界少样本、单 seed、LoRA 与短训练只验证机制，不复现原始 480 步/全参数/HWU64 能力收益。共享热身、样本级路由和三配方重置已在 A100 实跑；8 题诊断无准确率提升，不等于原论文能力复现。真实 Qwen2.5-0.5B-Instruct 学生、7B-Instruct 教师，q/v LoRA 而非原文全参数微调。所有配方共享教师响应两轮 SFT、初始 OPD 热身和相同初始 adapter；随后重置 optimizer 与随机种子，分别执行持续 OPD、固定半预算切换及样本级 PIVOT。  On-policy 蒸馏 组相对策略优化 LLM 后训练 数据与预算：下一份算力花在哪里 PIVOT怎样从响应分数形成问题路由？ 先算每响应教师平均负logp的指数，再同题组平均、批内标准化，按余弦比例选最低问题。GRPO与OPD各保留规定归一，不能按单token直接分成两个目标。 例如同题几条回答先汇总，不能只取最容易一条就判整题可转RL。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-17707b628c0a119d">PIVOT怎样从响应分数形成问题路由？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Apivot">PIVOT: Perplexity-Informed KD-to-RL Transition Scheduling for Vertical-Domain Few-Shot Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Ping An Technology / University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>先算每响应教师平均负logp的指数，再同题组平均、批内标准化，按余弦比例选最低问题。GRPO与OPD各保留规定归一，不能按单token直接分成两个目标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同题几条回答先汇总，不能只取最容易一条就判整题可转RL。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11167">原论文</a> · <a href="../../../../post-training/2610.11167-pivot/">实现解读</a> · <a href="#qa-17707b628c0a119d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:recal" data-paper-title="ReCal: Calibrating Structured Pruning for On-Policy Distillation Recovery" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="ReCal: Calibrating Structured Pruning for On-Policy Distillation Recovery LLM 后训练 Zhongguancun Academy / Tencent / University of Science and Technology of China 2026-10-08 先剪枝再蒸馏并不保证可恢复：损坏的学生轨迹会限制 OPD 教师信号。ReCal 先用剪枝 probe 测量教师轨迹上损伤，再用损伤重加权原始未剪枝模型的校准统计，重新选择通道；目标宽度和恢复流程保持一致。 恢复使用 q/v LoRA，未复现原文全参数 FSDP、四领域数据或多 seed。已实现真实 FFN 通道删除、教师 SFT 和学生轨迹 OPD；当前四题诊断包含负结果，不代表论文 benchmark 收益。Qwen3-4B/A100，FFN 宽度从 9728 真正减到 7296。对照与 ReCal 使用相同目标宽度和教师 SFT 响应，2 轮 SFT、4 步 OPD；SFT/OPD 问题分开，验证 4 题。见运行说明。  On-policy distillation 剪枝恢复 LLM 后训练 数据与预算：下一份算力花在哪里 ReCal为什么剪枝前就考虑后续OPD可恢复性？ 严重剪枝会让学生只访问劣质状态，教师在这些状态的监督也受限。探针损伤帮助校准重新挑通道，意在保留更可恢复的结构，不是仅事后补训。 例如关键运算路径删坏后，单靠更长蒸馏未必能恢复。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-recal-386ad741" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-84a60a24fbdb3407">ReCal为什么剪枝前就考虑后续OPD可恢复性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arecal">ReCal: Calibrating Structured Pruning for On-Policy Distillation Recovery</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhongguancun Academy / Tencent / University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>严重剪枝会让学生只访问劣质状态，教师在这些状态的监督也受限。探针损伤帮助校准重新挑通道，意在保留更可恢复的结构，不是仅事后补训。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如关键运算路径删坏后，单靠更长蒸馏未必能恢复。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11332">原论文</a> · <a href="../../../../post-training/2610.11332-recal/">实现解读</a> · <a href="#qa-84a60a24fbdb3407">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:recal" data-paper-title="ReCal: Calibrating Structured Pruning for On-Policy Distillation Recovery" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="ReCal: Calibrating Structured Pruning for On-Policy Distillation Recovery LLM 后训练 Zhongguancun Academy / Tencent / University of Science and Technology of China 2026-10-08 先剪枝再蒸馏并不保证可恢复：损坏的学生轨迹会限制 OPD 教师信号。ReCal 先用剪枝 probe 测量教师轨迹上损伤，再用损伤重加权原始未剪枝模型的校准统计，重新选择通道；目标宽度和恢复流程保持一致。 恢复使用 q/v LoRA，未复现原文全参数 FSDP、四领域数据或多 seed。已实现真实 FFN 通道删除、教师 SFT 和学生轨迹 OPD；当前四题诊断包含负结果，不代表论文 benchmark 收益。Qwen3-4B/A100，FFN 宽度从 9728 真正减到 7296。对照与 ReCal 使用相同目标宽度和教师 SFT 响应，2 轮 SFT、4 步 OPD；SFT/OPD 问题分开，验证 4 题。见运行说明。  On-policy distillation 剪枝恢复 LLM 后训练 数据与预算：下一份算力花在哪里 ReCal为什么用剪枝探针测损伤，却回到未剪枝模型重新计算通道选择？ 第一次剪枝暴露哪些教师状态受损，这些损伤用于重加权原模型的校准激活，再重新选择通道。它试图避免损坏学生只能产生贫乏轨迹、后续蒸馏难以修复的循环。损伤估计需保留词表剩余概率质量，单独归一化少数候选会改变KL含义。 例如探针发现处理进位的状态受损较大，重新校准时提高这些状态的重要性；不是在已经删掉的通道上继续随意打补丁。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:recal" data-paper-title="ReCal: Calibrating Structured Pruning for On-Policy Distillation Recovery" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="ReCal: Calibrating Structured Pruning for On-Policy Distillation Recovery LLM 后训练 Zhongguancun Academy / Tencent / University of Science and Technology of China 2026-10-08 先剪枝再蒸馏并不保证可恢复：损坏的学生轨迹会限制 OPD 教师信号。ReCal 先用剪枝 probe 测量教师轨迹上损伤，再用损伤重加权原始未剪枝模型的校准统计，重新选择通道；目标宽度和恢复流程保持一致。 恢复使用 q/v LoRA，未复现原文全参数 FSDP、四领域数据或多 seed。已实现真实 FFN 通道删除、教师 SFT 和学生轨迹 OPD；当前四题诊断包含负结果，不代表论文 benchmark 收益。Qwen3-4B/A100，FFN 宽度从 9728 真正减到 7296。对照与 ReCal 使用相同目标宽度和教师 SFT 响应，2 轮 SFT、4 步 OPD；SFT/OPD 问题分开，验证 4 题。见运行说明。  On-policy distillation 剪枝恢复 LLM 后训练 数据与预算：下一份算力花在哪里 损伤加权校准与按普通激活大小直接剪有何不同？ 前者关注教师轨迹哪些状态被probe损坏，再重权原模型统计；普通激活重要性不直接看恢复需求。目标宽度与恢复流程需相同才能公平比较。 例如某状态不常见但损伤很大，可在校准中获更多权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a3fb80191720e2b7">损伤加权校准与按普通激活大小直接剪有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arecal">ReCal: Calibrating Structured Pruning for On-Policy Distillation Recovery</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhongguancun Academy / Tencent / University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者关注教师轨迹哪些状态被probe损坏，再重权原模型统计；普通激活重要性不直接看恢复需求。目标宽度与恢复流程需相同才能公平比较。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某状态不常见但损伤很大，可在校准中获更多权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11332">原论文</a> · <a href="../../../../post-training/2610.11332-recal/">实现解读</a> · <a href="#qa-a3fb80191720e2b7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:recal" data-paper-title="ReCal: Calibrating Structured Pruning for On-Policy Distillation Recovery" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="ReCal: Calibrating Structured Pruning for On-Policy Distillation Recovery LLM 后训练 Zhongguancun Academy / Tencent / University of Science and Technology of China 2026-10-08 先剪枝再蒸馏并不保证可恢复：损坏的学生轨迹会限制 OPD 教师信号。ReCal 先用剪枝 probe 测量教师轨迹上损伤，再用损伤重加权原始未剪枝模型的校准统计，重新选择通道；目标宽度和恢复流程保持一致。 恢复使用 q/v LoRA，未复现原文全参数 FSDP、四领域数据或多 seed。已实现真实 FFN 通道删除、教师 SFT 和学生轨迹 OPD；当前四题诊断包含负结果，不代表论文 benchmark 收益。Qwen3-4B/A100，FFN 宽度从 9728 真正减到 7296。对照与 ReCal 使用相同目标宽度和教师 SFT 响应，2 轮 SFT、4 步 OPD；SFT/OPD 问题分开，验证 4 题。见运行说明。  On-policy distillation 剪枝恢复 LLM 后训练 数据与预算：下一份算力花在哪里 ReCal top教师候选外的概率可以丢掉再归一吗？ 不能，保留top及其余总质量桶来估损伤，避免隐藏词表外误差。每响应损伤权重归一到单位，零损伤退化均匀；通道重选回到未剪原模型统计。 例如probe把质量移到top外，局部重归一会看不见这类损伤。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3aa5afe4d1764d68">ReCal top教师候选外的概率可以丢掉再归一吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arecal">ReCal: Calibrating Structured Pruning for On-Policy Distillation Recovery</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhongguancun Academy / Tencent / University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，保留top及其余总质量桶来估损伤，避免隐藏词表外误差。每响应损伤权重归一到单位，零损伤退化均匀；通道重选回到未剪原模型统计。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如probe把质量移到top外，局部重归一会看不见这类损伤。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11332">原论文</a> · <a href="../../../../post-training/2610.11332-recal/">实现解读</a> · <a href="#qa-3aa5afe4d1764d68">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:follow-the-winners" data-paper-title="Follow the Winners: Conservative Policy Improvement with the Cross-Entropy Method for Critic-Free RFT" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Follow the Winners: Conservative Policy Improvement with the Cross-Entropy Method for Critic-Free RFT LLM 后训练 Trent AI Limited 2026-10-02 在有状态工具环境里，为同一提示重复生成一组等价 rollout 往往很贵；而 PPO 的 critic 又占用额外模型资源。FTW 不计算 value，也不要求 GRPO 式同题多轨迹。它保留近期策略产生的真实轨迹，从 FIFO 池中反复抽取小批量、仅模仿每批回报最高的条，并用 KL 约束更新幅度。过去轨迹被再次选中的次数自然形成训练权重，而不是对整池只做一次硬截断。 L1 核心机制诊断。L1 核心机制诊断。实现了论文 Algorithm 2 的 FIFO 轨迹池、重复小批量 top- 筛选和带 KL 正则的交叉熵策略投影；目前只在合成双臂 bandit 上执行，不等同于论文的 LLM Agent 训练。没有训练 Qwen、运行 Sokoban/Search-R1，也没有与同预算 PPO/GRPO 比较；bandit 的已知均值只用于诊断，不构成验证集/测试集上的调参或能力评测。该产物标记 diagnostic_only=true、formal_comparison=false，不参与公开能力提升或 Evolve 晋级。  Agentic RL 无 critic 策略改进 精英轨迹筛选 LLM 后训练 数据与预算：下一份算力花在哪里 FTW为什么不用同题多轨迹或value critic？ 有状态工具轨迹采集贵，方法从近期FIFO真实轨迹池反复抽批，模仿批内精英并用KL约束。它以回放排名替代一部分同题组与价值估计需求。 例如每个工具任务只做一条，也可把近期不同任务轨迹放进池中选批精英。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-follow-the-winners-b5a02f54" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d44fcdf056fedcaa">FTW为什么不用同题多轨迹或value critic？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Afollow-the-winners">Follow the Winners: Conservative Policy Improvement with the Cross-Entropy Method for Critic-Free RFT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Trent AI Limited</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>有状态工具轨迹采集贵，方法从近期FIFO真实轨迹池反复抽批，模仿批内精英并用KL约束。它以回放排名替代一部分同题组与价值估计需求。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如每个工具任务只做一条，也可把近期不同任务轨迹放进池中选批精英。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03361">原论文</a> · <a href="../../../../post-training/2610.03361-follow-the-winners/">实现解读</a> · <a href="#qa-d44fcdf056fedcaa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:follow-the-winners" data-paper-title="Follow the Winners: Conservative Policy Improvement with the Cross-Entropy Method for Critic-Free RFT" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Follow the Winners: Conservative Policy Improvement with the Cross-Entropy Method for Critic-Free RFT LLM 后训练 Trent AI Limited 2026-10-02 在有状态工具环境里，为同一提示重复生成一组等价 rollout 往往很贵；而 PPO 的 critic 又占用额外模型资源。FTW 不计算 value，也不要求 GRPO 式同题多轨迹。它保留近期策略产生的真实轨迹，从 FIFO 池中反复抽取小批量、仅模仿每批回报最高的条，并用 KL 约束更新幅度。过去轨迹被再次选中的次数自然形成训练权重，而不是对整池只做一次硬截断。 L1 核心机制诊断。L1 核心机制诊断。实现了论文 Algorithm 2 的 FIFO 轨迹池、重复小批量 top- 筛选和带 KL 正则的交叉熵策略投影；目前只在合成双臂 bandit 上执行，不等同于论文的 LLM Agent 训练。没有训练 Qwen、运行 Sokoban/Search-R1，也没有与同预算 PPO/GRPO 比较；bandit 的已知均值只用于诊断，不构成验证集/测试集上的调参或能力评测。该产物标记 diagnostic_only=true、formal_comparison=false，不参与公开能力提升或 Evolve 晋级。  Agentic RL 无 critic 策略改进 精英轨迹筛选 LLM 后训练 数据与预算：下一份算力花在哪里 Follow the Winners为什么反复抽小批精英，而不只取整个回放池的前K条？ 每次先从近期轨迹池随机抽批，再取批内高回报轨迹，重复入选次数形成平滑的排名权重。整池硬截断是特例，通常会丢掉更多次优但有用的轨迹。方法不要求同题多条轨迹或价值模型，仍需KL控制更新；本地小环境诊断不证明工具任务收益。 例如池中最好路线经常入选，次好路线也可能在某批成为精英；不是永久只训练全池最前几条，更不是给重复轨迹去重后等权。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:follow-the-winners" data-paper-title="Follow the Winners: Conservative Policy Improvement with the Cross-Entropy Method for Critic-Free RFT" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Follow the Winners: Conservative Policy Improvement with the Cross-Entropy Method for Critic-Free RFT LLM 后训练 Trent AI Limited 2026-10-02 在有状态工具环境里，为同一提示重复生成一组等价 rollout 往往很贵；而 PPO 的 critic 又占用额外模型资源。FTW 不计算 value，也不要求 GRPO 式同题多轨迹。它保留近期策略产生的真实轨迹，从 FIFO 池中反复抽取小批量、仅模仿每批回报最高的条，并用 KL 约束更新幅度。过去轨迹被再次选中的次数自然形成训练权重，而不是对整池只做一次硬截断。 L1 核心机制诊断。L1 核心机制诊断。实现了论文 Algorithm 2 的 FIFO 轨迹池、重复小批量 top- 筛选和带 KL 正则的交叉熵策略投影；目前只在合成双臂 bandit 上执行，不等同于论文的 LLM Agent 训练。没有训练 Qwen、运行 Sokoban/Search-R1，也没有与同预算 PPO/GRPO 比较；bandit 的已知均值只用于诊断，不构成验证集/测试集上的调参或能力评测。该产物标记 diagnostic_only=true、formal_comparison=false，不参与公开能力提升或 Evolve 晋级。  Agentic RL 无 critic 策略改进 精英轨迹筛选 LLM 后训练 数据与预算：下一份算力花在哪里 FTW小批精英与整池一次top-K为何不等价？ 反复抽批形成按排名的软占用率，次优轨迹也可能入选；整池硬截断只保留绝对前列。重复入选次数是权重的一部分，去重会改目标。 例如全池第二梯队在一批中没有最强对手时仍可成为精英。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1d5e36608da4db56">FTW小批精英与整池一次top-K为何不等价？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Afollow-the-winners">Follow the Winners: Conservative Policy Improvement with the Cross-Entropy Method for Critic-Free RFT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Trent AI Limited</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>反复抽批形成按排名的软占用率，次优轨迹也可能入选；整池硬截断只保留绝对前列。重复入选次数是权重的一部分，去重会改目标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如全池第二梯队在一批中没有最强对手时仍可成为精英。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03361">原论文</a> · <a href="../../../../post-training/2610.03361-follow-the-winners/">实现解读</a> · <a href="#qa-1d5e36608da4db56">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:follow-the-winners" data-paper-title="Follow the Winners: Conservative Policy Improvement with the Cross-Entropy Method for Critic-Free RFT" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Follow the Winners: Conservative Policy Improvement with the Cross-Entropy Method for Critic-Free RFT LLM 后训练 Trent AI Limited 2026-10-02 在有状态工具环境里，为同一提示重复生成一组等价 rollout 往往很贵；而 PPO 的 critic 又占用额外模型资源。FTW 不计算 value，也不要求 GRPO 式同题多轨迹。它保留近期策略产生的真实轨迹，从 FIFO 池中反复抽取小批量、仅模仿每批回报最高的条，并用 KL 约束更新幅度。过去轨迹被再次选中的次数自然形成训练权重，而不是对整池只做一次硬截断。 L1 核心机制诊断。L1 核心机制诊断。实现了论文 Algorithm 2 的 FIFO 轨迹池、重复小批量 top- 筛选和带 KL 正则的交叉熵策略投影；目前只在合成双臂 bandit 上执行，不等同于论文的 LLM Agent 训练。没有训练 Qwen、运行 Sokoban/Search-R1，也没有与同预算 PPO/GRPO 比较；bandit 的已知均值只用于诊断，不构成验证集/测试集上的调参或能力评测。该产物标记 diagnostic_only=true、formal_comparison=false，不参与公开能力提升或 Evolve 晋级。  Agentic RL 无 critic 策略改进 精英轨迹筛选 LLM 后训练 数据与预算：下一份算力花在哪里 FTW的K=C与C=N分别应退化成什么？ 前者保留整批，成为均匀抽样；后者每次取全池，对应整池精英选择。应验证分布和为一并保留跨批重复，本地bandit诊断不等于真实工具环境收益。 例如把K设成C还偏爱最高排名，就说明实现未正确退化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0d6b4047412aaba8">FTW的K=C与C=N分别应退化成什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Afollow-the-winners">Follow the Winners: Conservative Policy Improvement with the Cross-Entropy Method for Critic-Free RFT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Trent AI Limited</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者保留整批，成为均匀抽样；后者每次取全池，对应整池精英选择。应验证分布和为一并保留跨批重复，本地bandit诊断不等于真实工具环境收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把K设成C还偏爱最高排名，就说明实现未正确退化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03361">原论文</a> · <a href="../../../../post-training/2610.03361-follow-the-winners/">实现解读</a> · <a href="#qa-0d6b4047412aaba8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:lesser" data-paper-title="LESSER: Post-Training Data Selection with Output-Layer Gradients" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="LESSER: Post-Training Data Selection with Output-Layer Gradients LLM 后训练 University of Pennsylvania 2026-10-02 现有面向目标任务的数据选择常计算每个候选样本和少量目标任务 query 的全参数梯度，再按相似性选取训练子集；对大模型逐样本反传代价很高。LESSER 只替换特征：从一次前向得到的最后隐藏状态和词表概率解析地计算输出层梯度。SFT、RL 问题选择或教师选择原有的选择规则不需要改变。 L1 前向特征与筛选协议诊断。L1 前向特征与筛选协议诊断。已实现论文的输出层梯度、双侧随机投影及保持不变的 round-robin 选择；没有宣称复现大模型微调、RL、教师选择或论文速度收益。这里的隐藏状态和 logits 来自固定随机张量，用于公式与选择器的确定性验证；没有在公开 Tulu V2、GSM8K 等数据上运行真实 LLM，也没有比较训练后的任务效果或 A100 吞吐。因此标记 diagnostic_only=true，不进入正式能力看板或 Evolve 增益候选。若要升级为 L2，需固定公开 checkpoint/数据修订、query/test 切分、同预算 LESS/随机对照和多 seed 下游训练；  后训练数据选择 梯度特征 计算效率 LLM 后训练 数据与预算：下一份算力花在哪里 LESSER为什么用输出层梯度作为数据选择特征？ 全参数逐样本反传昂贵，独立readout梯度可由一次前向的概率残差与末隐藏态解析得到，再压缩成特征供原选择器使用。改变的是表示，不是另造选样准则。 例如仍按与目标查询相似度选题，只把代价高的梯度特征换成输出层形式。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-lesser-18cdf418" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c5e873d09446feea">LESSER为什么用输出层梯度作为数据选择特征？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Alesser">LESSER: Post-Training Data Selection with Output-Layer Gradients</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pennsylvania</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全参数逐样本反传昂贵，独立readout梯度可由一次前向的概率残差与末隐藏态解析得到，再压缩成特征供原选择器使用。改变的是表示，不是另造选样准则。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如仍按与目标查询相似度选题，只把代价高的梯度特征换成输出层形式。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03702">原论文</a> · <a href="../../../../post-training/2610.03702-lesser/">实现解读</a> · <a href="#qa-c5e873d09446feea">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:lesser" data-paper-title="LESSER: Post-Training Data Selection with Output-Layer Gradients" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="LESSER: Post-Training Data Selection with Output-Layer Gradients LLM 后训练 University of Pennsylvania 2026-10-02 现有面向目标任务的数据选择常计算每个候选样本和少量目标任务 query 的全参数梯度，再按相似性选取训练子集；对大模型逐样本反传代价很高。LESSER 只替换特征：从一次前向得到的最后隐藏状态和词表概率解析地计算输出层梯度。SFT、RL 问题选择或教师选择原有的选择规则不需要改变。 L1 前向特征与筛选协议诊断。L1 前向特征与筛选协议诊断。已实现论文的输出层梯度、双侧随机投影及保持不变的 round-robin 选择；没有宣称复现大模型微调、RL、教师选择或论文速度收益。这里的隐藏状态和 logits 来自固定随机张量，用于公式与选择器的确定性验证；没有在公开 Tulu V2、GSM8K 等数据上运行真实 LLM，也没有比较训练后的任务效果或 A100 吞吐。因此标记 diagnostic_only=true，不进入正式能力看板或 Evolve 增益候选。若要升级为 L2，需固定公开 checkpoint/数据修订、query/test 切分、同预算 LESS/随机对照和多 seed 下游训练；  后训练数据选择 梯度特征 计算效率 LLM 后训练 数据与预算：下一份算力花在哪里 LESSER从一次前向解析输出层梯度，为什么不能称为全参数梯度的精确替代？ 解析式利用隐藏状态与输出概率残差的外积，精确针对独立输出读出层；双侧共享投影再压缩这些特征，原数据选择规则可以继续使用。它不是所有层梯度，嵌入权重绑定时还需区分间接依赖。选择用验证代理查询，隔离测试集不能参与选样。 例如用少量验证题的输出层梯度方向挑相关训练题；不能先看测试题方向来选数据，也不能把最后一层相似等同全模型更新相同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:lesser" data-paper-title="LESSER: Post-Training Data Selection with Output-Layer Gradients" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="LESSER: Post-Training Data Selection with Output-Layer Gradients LLM 后训练 University of Pennsylvania 2026-10-02 现有面向目标任务的数据选择常计算每个候选样本和少量目标任务 query 的全参数梯度，再按相似性选取训练子集；对大模型逐样本反传代价很高。LESSER 只替换特征：从一次前向得到的最后隐藏状态和词表概率解析地计算输出层梯度。SFT、RL 问题选择或教师选择原有的选择规则不需要改变。 L1 前向特征与筛选协议诊断。L1 前向特征与筛选协议诊断。已实现论文的输出层梯度、双侧随机投影及保持不变的 round-robin 选择；没有宣称复现大模型微调、RL、教师选择或论文速度收益。这里的隐藏状态和 logits 来自固定随机张量，用于公式与选择器的确定性验证；没有在公开 Tulu V2、GSM8K 等数据上运行真实 LLM，也没有比较训练后的任务效果或 A100 吞吐。因此标记 diagnostic_only=true，不进入正式能力看板或 Evolve 增益候选。若要升级为 L2，需固定公开 checkpoint/数据修订、query/test 切分、同预算 LESS/随机对照和多 seed 下游训练；  后训练数据选择 梯度特征 计算效率 LLM 后训练 数据与预算：下一份算力花在哪里 LESSER与完整模型梯度相似度能声称完全等价吗？ 不能，解析精确性针对独立输出层；隐藏态若经绑定embedding依赖同一参数，还有额外路径。压缩也近似几何，不能从公式核通过推断同样下游性能。 例如最后一层方向相近，不代表所有中层参数更新都相近。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f265bae522721287">LESSER与完整模型梯度相似度能声称完全等价吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Alesser">LESSER: Post-Training Data Selection with Output-Layer Gradients</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pennsylvania</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，解析精确性针对独立输出层；隐藏态若经绑定embedding依赖同一参数，还有额外路径。压缩也近似几何，不能从公式核通过推断同样下游性能。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如最后一层方向相近，不代表所有中层参数更新都相近。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03702">原论文</a> · <a href="../../../../post-training/2610.03702-lesser/">实现解读</a> · <a href="#qa-f265bae522721287">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:lesser" data-paper-title="LESSER: Post-Training Data Selection with Output-Layer Gradients" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="LESSER: Post-Training Data Selection with Output-Layer Gradients LLM 后训练 University of Pennsylvania 2026-10-02 现有面向目标任务的数据选择常计算每个候选样本和少量目标任务 query 的全参数梯度，再按相似性选取训练子集；对大模型逐样本反传代价很高。LESSER 只替换特征：从一次前向得到的最后隐藏状态和词表概率解析地计算输出层梯度。SFT、RL 问题选择或教师选择原有的选择规则不需要改变。 L1 前向特征与筛选协议诊断。L1 前向特征与筛选协议诊断。已实现论文的输出层梯度、双侧随机投影及保持不变的 round-robin 选择；没有宣称复现大模型微调、RL、教师选择或论文速度收益。这里的隐藏状态和 logits 来自固定随机张量，用于公式与选择器的确定性验证；没有在公开 Tulu V2、GSM8K 等数据上运行真实 LLM，也没有比较训练后的任务效果或 A100 吞吐。因此标记 diagnostic_only=true，不进入正式能力看板或 Evolve 增益候选。若要升级为 L2，需固定公开 checkpoint/数据修订、query/test 切分、同预算 LESS/随机对照和多 seed 下游训练；  后训练数据选择 梯度特征 计算效率 LLM 后训练 数据与预算：下一份算力花在哪里 LESSER为什么候选与query共享同一随机投影？ 只有共同坐标才能比较特征相似度，应先在token残差和hidden两侧投影，避免物化大矩阵。query来自验证代理，测试不可选样；本地输入随机张量仅诊断。 例如每样本各抽一套投影，向量夹角就不再比较同一特征空间。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d424b130e8a7aebb">LESSER为什么候选与query共享同一随机投影？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Alesser">LESSER: Post-Training Data Selection with Output-Layer Gradients</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pennsylvania</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只有共同坐标才能比较特征相似度，应先在token残差和hidden两侧投影，避免物化大矩阵。query来自验证代理，测试不可选样；本地输入随机张量仅诊断。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如每样本各抽一套投影，向量夹角就不再比较同一特征空间。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03702">原论文</a> · <a href="../../../../post-training/2610.03702-lesser/">实现解读</a> · <a href="#qa-d424b130e8a7aebb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dars" data-paper-title="Dependency-Aware Reward Shaping for Agentic Reinforcement Learning" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Dependency-Aware Reward Shaping for Agentic Reinforcement Learning LLM 后训练 University of Illinois Urbana-Champaign 2026-10-01 把任务进度表示为带先决条件的 predicate 图；验证、失效和修复事件更新图状态，最近破损依赖按图距离衰减已完成工作的 credit，独立分支不受牵连。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行依赖衰减、失效/修复与 potential 差分；未训练 1.5B–8B 模型，官方仓库当前仅发布接口说明、代码仍在准备。执行依赖衰减、失效/修复与 potential 差分；未训练 1.5B–8B 模型，官方仓库当前仅发布接口说明、代码仍在准备。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Agentic RL 依赖图 步级奖励 LLM 后训练 数据与预算：下一份算力花在哪里 DARS为什么把进度写成依赖predicate图？ 已完成步骤可能依赖后来失效的条件，单纯累计进度无法反映破损。图状态让验证、失效和修复影响相关信用，同时保持独立分支，不一律清零。 例如预订取消会影响依赖行程，却不必抹去独立完成的材料准备。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-dars-eb9dd187" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f737fb5a8ac8ba71">DARS为什么把进度写成依赖predicate图？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adars">Dependency-Aware Reward Shaping for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>已完成步骤可能依赖后来失效的条件，单纯累计进度无法反映破损。图状态让验证、失效和修复影响相关信用，同时保持独立分支，不一律清零。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如预订取消会影响依赖行程，却不必抹去独立完成的材料准备。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01207">原论文</a> · <a href="../../../../post-training/2610.01207-dars/">实现解读</a> · <a href="#qa-f737fb5a8ac8ba71">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dars" data-paper-title="Dependency-Aware Reward Shaping for Agentic Reinforcement Learning" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Dependency-Aware Reward Shaping for Agentic Reinforcement Learning LLM 后训练 University of Illinois Urbana-Champaign 2026-10-01 把任务进度表示为带先决条件的 predicate 图；验证、失效和修复事件更新图状态，最近破损依赖按图距离衰减已完成工作的 credit，独立分支不受牵连。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行依赖衰减、失效/修复与 potential 差分；未训练 1.5B–8B 模型，官方仓库当前仅发布接口说明、代码仍在准备。执行依赖衰减、失效/修复与 potential 差分；未训练 1.5B–8B 模型，官方仓库当前仅发布接口说明、代码仍在准备。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Agentic RL 依赖图 步级奖励 LLM 后训练 数据与预算：下一份算力花在哪里 依赖感知奖励塑形为什么只衰减破损依赖附近的信用，而不清空所有已完成进度？ 任务以先决条件图表示，某个条件失效会影响依赖它的后续工作，却不必影响独立分支。按图距离衰减信用，再由势函数差分形成奖励，可反映破损与修复。它依赖谓词状态和依赖图是否正确，本地状态转移核没有证明真实智能体训练收益。 例如订票失效会削弱依赖该行程的酒店安排信用，但不应抹掉独立完成的报销材料；修复后相关进度再按状态恢复。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dars" data-paper-title="Dependency-Aware Reward Shaping for Agentic Reinforcement Learning" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Dependency-Aware Reward Shaping for Agentic Reinforcement Learning LLM 后训练 University of Illinois Urbana-Champaign 2026-10-01 把任务进度表示为带先决条件的 predicate 图；验证、失效和修复事件更新图状态，最近破损依赖按图距离衰减已完成工作的 credit，独立分支不受牵连。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行依赖衰减、失效/修复与 potential 差分；未训练 1.5B–8B 模型，官方仓库当前仅发布接口说明、代码仍在准备。执行依赖衰减、失效/修复与 potential 差分；未训练 1.5B–8B 模型，官方仓库当前仅发布接口说明、代码仍在准备。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Agentic RL 依赖图 步级奖励 LLM 后训练 数据与预算：下一份算力花在哪里 依赖距离衰减与全局失败扣分有何差别？ 衰减针对离破损依赖不同距离的工作，全局扣分不分关联。图错也会误分信用，因此结构化不自动保证准确，仍需验证predicate和依赖。 例如酒店安排依赖航班，另一分支的账户验证不该同受惩罚。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-680896d0dd51adf2">依赖距离衰减与全局失败扣分有何差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adars">Dependency-Aware Reward Shaping for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>衰减针对离破损依赖不同距离的工作，全局扣分不分关联。图错也会误分信用，因此结构化不自动保证准确，仍需验证predicate和依赖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如酒店安排依赖航班，另一分支的账户验证不该同受惩罚。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01207">原论文</a> · <a href="../../../../post-training/2610.01207-dars/">实现解读</a> · <a href="#qa-680896d0dd51adf2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dars" data-paper-title="Dependency-Aware Reward Shaping for Agentic Reinforcement Learning" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Dependency-Aware Reward Shaping for Agentic Reinforcement Learning LLM 后训练 University of Illinois Urbana-Champaign 2026-10-01 把任务进度表示为带先决条件的 predicate 图；验证、失效和修复事件更新图状态，最近破损依赖按图距离衰减已完成工作的 credit，独立分支不受牵连。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行依赖衰减、失效/修复与 potential 差分；未训练 1.5B–8B 模型，官方仓库当前仅发布接口说明、代码仍在准备。执行依赖衰减、失效/修复与 potential 差分；未训练 1.5B–8B 模型，官方仓库当前仅发布接口说明、代码仍在准备。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Agentic RL 依赖图 步级奖励 LLM 后训练 数据与预算：下一份算力花在哪里 DARS修复事件是否只改当前reward不改状态？ 应更新依赖状态与势函数，再由相邻势差得奖，否则后续仍基于旧破损记录。当前只执行状态核，未训练原文模型；上游接口说明不等于作者训练代码已发布。 例如航班修复后关联信用应按新状态恢复，而不只是额外加一次奖金。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-985f17937ae96c42">DARS修复事件是否只改当前reward不改状态？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adars">Dependency-Aware Reward Shaping for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>应更新依赖状态与势函数，再由相邻势差得奖，否则后续仍基于旧破损记录。当前只执行状态核，未训练原文模型；上游接口说明不等于作者训练代码已发布。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如航班修复后关联信用应按新状态恢复，而不只是额外加一次奖金。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01207">原论文</a> · <a href="../../../../post-training/2610.01207-dars/">实现解读</a> · <a href="#qa-985f17937ae96c42">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gats" data-paper-title="Guide, Then Let Go: Gap-Adaptive Teacher Scheduling for Sparse-Reward Agentic RL" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Guide, Then Let Go: Gap-Adaptive Teacher Scheduling for Sparse-Reward Agentic RL LLM 后训练 Dalian University of Technology / Kuaishou 2026-09-29 用教师训练尾部成功率作为固定参考，以学生滞后一拍的移动平均估计能力差距；OPD 权重随差距线性下降，学生达到教师参考后永久关闭教师分支，继续只做 GRPO。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行滞后一拍移动平均、gap weight 和永久 withdrawal；未做 Qwen Agent RL。执行滞后一拍移动平均、gap weight 和永久 withdrawal；未做 Qwen Agent RL。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Agentic RL On-policy distillation 课程调度 LLM 后训练 数据与预算：下一份算力花在哪里 GATS为什么让教师权重随学生差距下降？ 教师在稀疏奖励初期提供方向，学生接近固定教师参考后减少模仿，避免继续限制自身探索；达到参考后永久撤出，后续只做奖励训练。 例如学生已掌握教师水平，继续每步跟随可能妨碍自主改进。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-gats-23ea5c63" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-1dae826119dc52c7">GATS为什么让教师权重随学生差距下降？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agats">Guide, Then Let Go: Gap-Adaptive Teacher Scheduling for Sparse-Reward Agentic RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dalian University of Technology / Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>教师在稀疏奖励初期提供方向，学生接近固定教师参考后减少模仿，避免继续限制自身探索；达到参考后永久撤出，后续只做奖励训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生已掌握教师水平，继续每步跟随可能妨碍自主改进。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37898">原论文</a> · <a href="../../../../post-training/2609.37898-gats/">实现解读</a> · <a href="#qa-1dae826119dc52c7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gats" data-paper-title="Guide, Then Let Go: Gap-Adaptive Teacher Scheduling for Sparse-Reward Agentic RL" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Guide, Then Let Go: Gap-Adaptive Teacher Scheduling for Sparse-Reward Agentic RL LLM 后训练 Dalian University of Technology / Kuaishou 2026-09-29 用教师训练尾部成功率作为固定参考，以学生滞后一拍的移动平均估计能力差距；OPD 权重随差距线性下降，学生达到教师参考后永久关闭教师分支，继续只做 GRPO。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行滞后一拍移动平均、gap weight 和永久 withdrawal；未做 Qwen Agent RL。执行滞后一拍移动平均、gap weight 和永久 withdrawal；未做 Qwen Agent RL。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Agentic RL On-policy distillation 课程调度 LLM 后训练 数据与预算：下一份算力花在哪里 GATS为什么使用滞后一拍的学生成功率，并在赶上教师后永久撤出教师？ 滞后移动平均避免当前批次结果立即改变同批教师权重，固定教师参考使差距有稳定基准。差距缩小时蒸馏线性减弱，达到参考后永久关闭教师而继续奖励训练，避免短期波动反复开关。成功率受估计噪声影响，本地只验证调度状态机。 例如本轮表现改善，下轮才减少指导；一旦达到设定教师参考，即使随后小幅波动也不重新叫回教师，这与逐批动态开关不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gats" data-paper-title="Guide, Then Let Go: Gap-Adaptive Teacher Scheduling for Sparse-Reward Agentic RL" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Guide, Then Let Go: Gap-Adaptive Teacher Scheduling for Sparse-Reward Agentic RL LLM 后训练 Dalian University of Technology / Kuaishou 2026-09-29 用教师训练尾部成功率作为固定参考，以学生滞后一拍的移动平均估计能力差距；OPD 权重随差距线性下降，学生达到教师参考后永久关闭教师分支，继续只做 GRPO。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行滞后一拍移动平均、gap weight 和永久 withdrawal；未做 Qwen Agent RL。执行滞后一拍移动平均、gap weight 和永久 withdrawal；未做 Qwen Agent RL。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Agentic RL On-policy distillation 课程调度 LLM 后训练 数据与预算：下一份算力花在哪里 GATS永久withdrawal与每批按成功率重新开关有什么区别？ 永久状态避免短期波动反复调用教师，动态开关可在下降后恢复指导，二者政策不同。成功率有估计噪声，不能把一次达到就解释成所有能力超过教师。 例如下一批稍降也不会重启教师，这是状态机规定而非忘记调用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7be6d244589f428f">GATS永久withdrawal与每批按成功率重新开关有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agats">Guide, Then Let Go: Gap-Adaptive Teacher Scheduling for Sparse-Reward Agentic RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dalian University of Technology / Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>永久状态避免短期波动反复调用教师，动态开关可在下降后恢复指导，二者政策不同。成功率有估计噪声，不能把一次达到就解释成所有能力超过教师。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如下一批稍降也不会重启教师，这是状态机规定而非忘记调用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37898">原论文</a> · <a href="../../../../post-training/2609.37898-gats/">实现解读</a> · <a href="#qa-7be6d244589f428f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gats" data-paper-title="Guide, Then Let Go: Gap-Adaptive Teacher Scheduling for Sparse-Reward Agentic RL" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Guide, Then Let Go: Gap-Adaptive Teacher Scheduling for Sparse-Reward Agentic RL LLM 后训练 Dalian University of Technology / Kuaishou 2026-09-29 用教师训练尾部成功率作为固定参考，以学生滞后一拍的移动平均估计能力差距；OPD 权重随差距线性下降，学生达到教师参考后永久关闭教师分支，继续只做 GRPO。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行滞后一拍移动平均、gap weight 和永久 withdrawal；未做 Qwen Agent RL。执行滞后一拍移动平均、gap weight 和永久 withdrawal；未做 Qwen Agent RL。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Agentic RL On-policy distillation 课程调度 LLM 后训练 数据与预算：下一份算力花在哪里 GATS为什么用滞后一拍学生EMA与固定教师尾部成功率？ 当前批奖励不能即时反向改变同批调度，固定参照使差距可解释。需处理教师基准为零等边界，当前仅验证调度核，未执行Qwen Agent RL。 例如先完成本批记录，下一批权重再读更新后EMA，避免数据时序混乱。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3efcce80c343cefb">GATS为什么用滞后一拍学生EMA与固定教师尾部成功率？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agats">Guide, Then Let Go: Gap-Adaptive Teacher Scheduling for Sparse-Reward Agentic RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Dalian University of Technology / Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>当前批奖励不能即时反向改变同批调度，固定参照使差距可解释。需处理教师基准为零等边界，当前仅验证调度核，未执行Qwen Agent RL。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先完成本批记录，下一批权重再读更新后EMA，避免数据时序混乱。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37898">原论文</a> · <a href="../../../../post-training/2609.37898-gats/">实现解读</a> · <a href="#qa-3efcce80c343cefb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:roft" data-paper-title="Shockingly Simple Self-retrospection Improves Agentic Models Without RL" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Shockingly Simple Self-retrospection Improves Agentic Models Without RL LLM 后训练 Rensselaer Polytechnic Institute 2026-09-28 ROFT 不直接用环境奖励更新动作策略，而是让模型在完整轨迹与反馈之后生成一段自我回顾，再只监督回顾 token。回顾成为后续行为可复用的训练信号，同时避免把环境文本或历史动作误当监督标签。 复现级别：L1 核心机制 + 真实 checkpoint CUDA 路径。复现级别：L1 核心机制 + 真实 checkpoint CUDA 路径。本地实现全局 retrospection-token 交叉熵；不声称复现论文规模训练收益。当前没有论文规模 Agent rollout 数据，也没有把 ROFT 注册进 Evolve；在统一控制器能够实际构造回顾数据、训练并用隔离验证集评价前，不把 registry 标签当成已接入。roft_retrospection_loss 是可训练的 PyTorch 目标；通用后训练 CLI 中的 roft 只提供小型候选策略诊断。  自我回顾 监督微调 Agent 后训练 LLM 后训练 数据与预算：下一份算力花在哪里 ROFT为什么把环境反馈转成自我回顾再学习？ 直接终局奖励难表达可复用经验，模型事后写回顾将失败或成功转成文字监督。学习对象是回顾，不是把全部历史动作当作正确行为重放。 例如执行错误后归纳应先检查文件权限，可成为下次任务的经验。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-roft-6e694561" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7af0302d79d9d6da">ROFT为什么把环境反馈转成自我回顾再学习？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aroft">Shockingly Simple Self-retrospection Improves Agentic Models Without RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Rensselaer Polytechnic Institute</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直接终局奖励难表达可复用经验，模型事后写回顾将失败或成功转成文字监督。学习对象是回顾，不是把全部历史动作当作正确行为重放。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如执行错误后归纳应先检查文件权限，可成为下次任务的经验。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35741">原论文</a> · <a href="../../../../post-training/2609.35741-roft/">实现解读</a> · <a href="#qa-7af0302d79d9d6da">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:roft" data-paper-title="Shockingly Simple Self-retrospection Improves Agentic Models Without RL" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Shockingly Simple Self-retrospection Improves Agentic Models Without RL LLM 后训练 Rensselaer Polytechnic Institute 2026-09-28 ROFT 不直接用环境奖励更新动作策略，而是让模型在完整轨迹与反馈之后生成一段自我回顾，再只监督回顾 token。回顾成为后续行为可复用的训练信号，同时避免把环境文本或历史动作误当监督标签。 复现级别：L1 核心机制 + 真实 checkpoint CUDA 路径。复现级别：L1 核心机制 + 真实 checkpoint CUDA 路径。本地实现全局 retrospection-token 交叉熵；不声称复现论文规模训练收益。当前没有论文规模 Agent rollout 数据，也没有把 ROFT 注册进 Evolve；在统一控制器能够实际构造回顾数据、训练并用隔离验证集评价前，不把 registry 标签当成已接入。roft_retrospection_loss 是可训练的 PyTorch 目标；通用后训练 CLI 中的 roft 只提供小型候选策略诊断。  自我回顾 监督微调 Agent 后训练 LLM 后训练 数据与预算：下一份算力花在哪里 ROFT为什么只监督自我回顾词元，而不把轨迹里的动作和环境反馈一起训练？ 完整轨迹与反馈是回顾所需的条件，监督对象则是模型事后归纳的经验。分开上下文掩码与目标掩码，可避免把环境文本或历史错误动作当成应模仿标签；损失按所有回顾词元统一平均。本地没有完整智能体数据闭环，注册名称也不代表已接入演化控制器。 例如一次工具调用失败后，模型回顾应先检查参数；训练读取错误调用和报错，却只学习这段回顾，不模仿报错内容或错误动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:roft" data-paper-title="Shockingly Simple Self-retrospection Improves Agentic Models Without RL" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Shockingly Simple Self-retrospection Improves Agentic Models Without RL LLM 后训练 Rensselaer Polytechnic Institute 2026-09-28 ROFT 不直接用环境奖励更新动作策略，而是让模型在完整轨迹与反馈之后生成一段自我回顾，再只监督回顾 token。回顾成为后续行为可复用的训练信号，同时避免把环境文本或历史动作误当监督标签。 复现级别：L1 核心机制 + 真实 checkpoint CUDA 路径。复现级别：L1 核心机制 + 真实 checkpoint CUDA 路径。本地实现全局 retrospection-token 交叉熵；不声称复现论文规模训练收益。当前没有论文规模 Agent rollout 数据，也没有把 ROFT 注册进 Evolve；在统一控制器能够实际构造回顾数据、训练并用隔离验证集评价前，不把 registry 标签当成已接入。roft_retrospection_loss 是可训练的 PyTorch 目标；通用后训练 CLI 中的 roft 只提供小型候选策略诊断。  自我回顾 监督微调 Agent 后训练 LLM 后训练 数据与预算：下一份算力花在哪里 ROFT与用原轨迹动作做行为克隆有何不同？ 行为克隆模仿曾经采取的动作，回顾监督可学习避免这些动作的经验，两者标签对象不同。回顾若错误仍会误导，并非自我解释就天然可靠。 例如失败动作是删错文件，回顾可教检查路径，而不是再模仿删除。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-dd724cac5d5c8bf5">ROFT与用原轨迹动作做行为克隆有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aroft">Shockingly Simple Self-retrospection Improves Agentic Models Without RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Rensselaer Polytechnic Institute</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>行为克隆模仿曾经采取的动作，回顾监督可学习避免这些动作的经验，两者标签对象不同。回顾若错误仍会误导，并非自我解释就天然可靠。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如失败动作是删错文件，回顾可教检查路径，而不是再模仿删除。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35741">原论文</a> · <a href="../../../../post-training/2609.35741-roft/">实现解读</a> · <a href="#qa-dd724cac5d5c8bf5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:roft" data-paper-title="Shockingly Simple Self-retrospection Improves Agentic Models Without RL" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Shockingly Simple Self-retrospection Improves Agentic Models Without RL LLM 后训练 Rensselaer Polytechnic Institute 2026-09-28 ROFT 不直接用环境奖励更新动作策略，而是让模型在完整轨迹与反馈之后生成一段自我回顾，再只监督回顾 token。回顾成为后续行为可复用的训练信号，同时避免把环境文本或历史动作误当监督标签。 复现级别：L1 核心机制 + 真实 checkpoint CUDA 路径。复现级别：L1 核心机制 + 真实 checkpoint CUDA 路径。本地实现全局 retrospection-token 交叉熵；不声称复现论文规模训练收益。当前没有论文规模 Agent rollout 数据，也没有把 ROFT 注册进 Evolve；在统一控制器能够实际构造回顾数据、训练并用隔离验证集评价前，不把 registry 标签当成已接入。roft_retrospection_loss 是可训练的 PyTorch 目标；通用后训练 CLI 中的 roft 只提供小型候选策略诊断。  自我回顾 监督微调 Agent 后训练 LLM 后训练 数据与预算：下一份算力花在哪里 ROFT多个长短回顾的loss如何归一？ 按全部有效回顾词元全局平均，任务、动作、观察、反馈mask为零但保留输入。若先各回顾平均再等权，会改变长度权重；当前没有完整Agent数据或Evolve闭环。 例如一条很短和一条很长回顾，两个平均方案赋予的词元总贡献不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d3fe3fffdba6ba97">ROFT多个长短回顾的loss如何归一？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aroft">Shockingly Simple Self-retrospection Improves Agentic Models Without RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Rensselaer Polytechnic Institute</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>按全部有效回顾词元全局平均，任务、动作、观察、反馈mask为零但保留输入。若先各回顾平均再等权，会改变长度权重；当前没有完整Agent数据或Evolve闭环。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一条很短和一条很长回顾，两个平均方案赋予的词元总贡献不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35741">原论文</a> · <a href="../../../../post-training/2609.35741-roft/">实现解读</a> · <a href="#qa-d3fe3fffdba6ba97">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ross" data-paper-title="ROSS: Relearning from Self-Generated Rollouts through Selective Supervision" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="ROSS: Relearning from Self-Generated Rollouts through Selective Supervision LLM 后训练 AllSpark Team（原文以团队署名，未列机构） 2026-09-28 保留历史 self-rollout 的完整上下文，但只对筛选出的模型 continuation 计算损失，避免模仿其中错误或冗余步骤。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 full-context/selective-loss 边界；选择 mask 是 fixture，不冒充论文 selector。执行 full-context/selective-loss 边界；选择 mask 是 fixture，不冒充论文 selector。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  离线 SFT 选择性监督 LLM 后训练 数据与预算：下一份算力花在哪里 ROSS为什么重用历史self-rollout却不整段模仿？ 旧轨迹包含错误与冗余，完整上下文仍决定后续状态，选择性续写监督只吸收有价值部分。可见文字与应学标签应分开，不能把历史存在就当正确。 例如保留一次失败经过作背景，只学习后来被选中的纠正。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-ross-56261390" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-53158c924443c142">ROSS为什么重用历史self-rollout却不整段模仿？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aross">ROSS: Relearning from Self-Generated Rollouts through Selective Supervision</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AllSpark Team（原文以团队署名，未列机构）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>旧轨迹包含错误与冗余，完整上下文仍决定后续状态，选择性续写监督只吸收有价值部分。可见文字与应学标签应分开，不能把历史存在就当正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如保留一次失败经过作背景，只学习后来被选中的纠正。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35954">原论文</a> · <a href="../../../../post-training/2609.35954-ross/">实现解读</a> · <a href="#qa-53158c924443c142">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ross" data-paper-title="ROSS: Relearning from Self-Generated Rollouts through Selective Supervision" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="ROSS: Relearning from Self-Generated Rollouts through Selective Supervision LLM 后训练 AllSpark Team（原文以团队署名，未列机构） 2026-09-28 保留历史 self-rollout 的完整上下文，但只对筛选出的模型 continuation 计算损失，避免模仿其中错误或冗余步骤。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 full-context/selective-loss 边界；选择 mask 是 fixture，不冒充论文 selector。执行 full-context/selective-loss 边界；选择 mask 是 fixture，不冒充论文 selector。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  离线 SFT 选择性监督 LLM 后训练 数据与预算：下一份算力花在哪里 ROSS为什么保留历史轨迹的完整上下文，却只监督筛出的续写片段？ 历史上下文说明续写发生在什么状态，删掉它会改变条件分布；只对选中续写计算损失，则避免把旧轨迹中的错误或冗余步骤都当标签。上下文可见与梯度监督需要独立掩码。本地选择掩码是固定诊断输入，没有实现论文选择器，不能据此宣称自动筛选能力。 例如早期有一步错误但后续成功纠正，训练可读到整段经过，只学习被选的纠正续写；不能把可见上下文全部纳入模仿损失。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ross" data-paper-title="ROSS: Relearning from Self-Generated Rollouts through Selective Supervision" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="ROSS: Relearning from Self-Generated Rollouts through Selective Supervision LLM 后训练 AllSpark Team（原文以团队署名，未列机构） 2026-09-28 保留历史 self-rollout 的完整上下文，但只对筛选出的模型 continuation 计算损失，避免模仿其中错误或冗余步骤。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 full-context/selective-loss 边界；选择 mask 是 fixture，不冒充论文 selector。执行 full-context/selective-loss 边界；选择 mask 是 fixture，不冒充论文 selector。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  离线 SFT 选择性监督 LLM 后训练 数据与预算：下一份算力花在哪里 ROSS与直接删掉未选span再SFT有什么差别？ 删span改变后续条件，完整上下文加选择loss则保留真实轨迹状态。选择器质量仍决定监督可靠性，mask准确不等于选择算法已经实现。 例如移除错误前缀后，纠错句的含义和生成概率都可能改变。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-138dd71554ebd473">ROSS与直接删掉未选span再SFT有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aross">ROSS: Relearning from Self-Generated Rollouts through Selective Supervision</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AllSpark Team（原文以团队署名，未列机构）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>删span改变后续条件，完整上下文加选择loss则保留真实轨迹状态。选择器质量仍决定监督可靠性，mask准确不等于选择算法已经实现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如移除错误前缀后，纠错句的含义和生成概率都可能改变。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35954">原论文</a> · <a href="../../../../post-training/2609.35954-ross/">实现解读</a> · <a href="#qa-138dd71554ebd473">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ross" data-paper-title="ROSS: Relearning from Self-Generated Rollouts through Selective Supervision" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="ROSS: Relearning from Self-Generated Rollouts through Selective Supervision LLM 后训练 AllSpark Team（原文以团队署名，未列机构） 2026-09-28 保留历史 self-rollout 的完整上下文，但只对筛选出的模型 continuation 计算损失，避免模仿其中错误或冗余步骤。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 full-context/selective-loss 边界；选择 mask 是 fixture，不冒充论文 selector。执行 full-context/selective-loss 边界；选择 mask 是 fixture，不冒充论文 selector。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  离线 SFT 选择性监督 LLM 后训练 数据与预算：下一份算力花在哪里 ROSS当前本地selector是真实学习出来的吗？ 不是，选择mask是fixture，只验证full-context与selective-loss边界。不得把固定mask的梯度隔离通过，写成自动筛选历史有效步骤的模型能力。 例如测试明确指定学最后两句，只说明程序遵从mask，不说明会自己挑句。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-18dbcba85610e737">ROSS当前本地selector是真实学习出来的吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aross">ROSS: Relearning from Self-Generated Rollouts through Selective Supervision</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AllSpark Team（原文以团队署名，未列机构）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是，选择mask是fixture，只验证full-context与selective-loss边界。不得把固定mask的梯度隔离通过，写成自动筛选历史有效步骤的模型能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如测试明确指定学最后两句，只说明程序遵从mask，不说明会自己挑句。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35954">原论文</a> · <a href="../../../../post-training/2609.35954-ross/">实现解读</a> · <a href="#qa-18dbcba85610e737">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:retire-opd" data-paper-title="RetireOPD: Self-Retiring On-Policy Distillation for Agentic Reinforcement Learning" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="RetireOPD: Self-Retiring On-Policy Distillation for Agentic Reinforcement Learning LLM 后训练 Zhejiang University 2026-09-17 给不同技能配置解耦教师；学生同时执行 RL 与 on-policy distillation，当成功率接近教师且分布差距不再收缩时自动退休教师。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行退休判据与学生更新；未训练论文规模 Agent 教师。本地执行退休判据与学生更新；未训练论文规模 Agent 教师。  On-policy distillation Agent RL LLM 后训练 数据与预算：下一份算力花在哪里 RetireOPD为什么为不同技能设置可退休教师？ 各技能掌握程度不同，教师可在学生接近其水平且分布进步停滞时退出，继续RL探索。统一固定教师预算可能对熟练技能过多、对薄弱技能不足。 例如搜索已熟而格式仍弱，可分别决定是否保留指导。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-retire-opd-e8a79255" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4c0fd08faf333c24">RetireOPD为什么为不同技能设置可退休教师？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aretire-opd">RetireOPD: Self-Retiring On-Policy Distillation for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>各技能掌握程度不同，教师可在学生接近其水平且分布进步停滞时退出，继续RL探索。统一固定教师预算可能对熟练技能过多、对薄弱技能不足。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如搜索已熟而格式仍弱，可分别决定是否保留指导。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.20784">原论文</a> · <a href="../../../../post-training/2609.20784-retire-opd/">实现解读</a> · <a href="#qa-4c0fd08faf333c24">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:retire-opd" data-paper-title="RetireOPD: Self-Retiring On-Policy Distillation for Agentic Reinforcement Learning" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="RetireOPD: Self-Retiring On-Policy Distillation for Agentic Reinforcement Learning LLM 后训练 Zhejiang University 2026-09-17 给不同技能配置解耦教师；学生同时执行 RL 与 on-policy distillation，当成功率接近教师且分布差距不再收缩时自动退休教师。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行退休判据与学生更新；未训练论文规模 Agent 教师。本地执行退休判据与学生更新；未训练论文规模 Agent 教师。  On-policy distillation Agent RL LLM 后训练 数据与预算：下一份算力花在哪里 RetireOPD为什么不能仅凭学生成功率接近教师就立即退休所有教师？ 方法给不同技能配置解耦教师，退休同时考虑成功率接近和分布差距不再收缩。前者反映任务结果，后者提示继续蒸馏的边际空间；只看其中一项可能过早撤走有用指导。退休应针对相应技能判断，本地仅验证判据和更新，不代表论文规模多教师训练。 例如学生搜索技能已接近搜索教师，但工具格式仍落后，前者可以考虑退休，不能据一个总成功率就把格式教师一并撤掉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:retire-opd" data-paper-title="RetireOPD: Self-Retiring On-Policy Distillation for Agentic Reinforcement Learning" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="RetireOPD: Self-Retiring On-Policy Distillation for Agentic Reinforcement Learning LLM 后训练 Zhejiang University 2026-09-17 给不同技能配置解耦教师；学生同时执行 RL 与 on-policy distillation，当成功率接近教师且分布差距不再收缩时自动退休教师。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行退休判据与学生更新；未训练论文规模 Agent 教师。本地执行退休判据与学生更新；未训练论文规模 Agent 教师。  On-policy distillation Agent RL LLM 后训练 数据与预算：下一份算力花在哪里 退休看成功率和分布gap，为什么不只看其一？ 成功率相近仍可能有可学行为差异，gap停滞也可能表示学生仍失败；联合条件用于判断继续蒸馏的价值。它是调度判据，不是所有能力超过教师的证明。 例如任务得分接近但工具选择还不同，仍需核对差距是否真正收缩完。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-da2dbe2a3dc8b6d6">退休看成功率和分布gap，为什么不只看其一？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aretire-opd">RetireOPD: Self-Retiring On-Policy Distillation for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>成功率相近仍可能有可学行为差异，gap停滞也可能表示学生仍失败；联合条件用于判断继续蒸馏的价值。它是调度判据，不是所有能力超过教师的证明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如任务得分接近但工具选择还不同，仍需核对差距是否真正收缩完。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.20784">原论文</a> · <a href="../../../../post-training/2609.20784-retire-opd/">实现解读</a> · <a href="#qa-da2dbe2a3dc8b6d6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:retire-opd" data-paper-title="RetireOPD: Self-Retiring On-Policy Distillation for Agentic Reinforcement Learning" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="RetireOPD: Self-Retiring On-Policy Distillation for Agentic Reinforcement Learning LLM 后训练 Zhejiang University 2026-09-17 给不同技能配置解耦教师；学生同时执行 RL 与 on-policy distillation，当成功率接近教师且分布差距不再收缩时自动退休教师。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行退休判据与学生更新；未训练论文规模 Agent 教师。本地执行退休判据与学生更新；未训练论文规模 Agent 教师。  On-policy distillation Agent RL LLM 后训练 数据与预算：下一份算力花在哪里 RetireOPD本地判据通过是否代表已训练解耦Agent教师？ 没有，只执行退休状态与学生更新核。成功率、gap趋势、技能身份和退役状态需可追踪，不能只有一个registry标签就称完整多教师闭环。 例如模拟统计触发retired，只验证条件分支，不证明真实教师已被替代。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-bfc0702f7f16fe11">RetireOPD本地判据通过是否代表已训练解耦Agent教师？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aretire-opd">RetireOPD: Self-Retiring On-Policy Distillation for Agentic Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有，只执行退休状态与学生更新核。成功率、gap趋势、技能身份和退役状态需可追踪，不能只有一个registry标签就称完整多教师闭环。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模拟统计触发retired，只验证条件分支，不证明真实教师已被替代。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.20784">原论文</a> · <a href="../../../../post-training/2609.20784-retire-opd/">实现解读</a> · <a href="#qa-bfc0702f7f16fe11">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:trajectory-learnability" data-paper-title="Trajectory Learnability for Offline On-Policy Distillation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Trajectory Learnability for Offline On-Policy Distillation LLM 后训练 National University of Singapore 2026-09-16 用成功轨迹训练参考模型，以参考与当前策略逐 token 对数似然变化衡量可学性，并据此重加权离线 OPD 轨迹。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行逐 token 可学性聚合和轨迹加权；未复刻论文 GPU 训练预算。本地执行逐 token 可学性聚合和轨迹加权；未复刻论文 GPU 训练预算。  On-policy distillation 轨迹加权 LLM 后训练 数据与预算：下一份算力花在哪里 轨迹可学性为什么不等同成功奖励？ 成功说明结果，学习价值还取决于当前学生是否已掌握。成功参考与当前策略的逐词元似然变化帮助区分已有知识与潜在可吸收部分，再重权离线轨迹。 例如两条都对，一条学生会了，另一条尚缺关键转折。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-trajectory-learnability-8d70d16c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-44335d5c4b2a60d2">轨迹可学性为什么不等同成功奖励？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atrajectory-learnability">Trajectory Learnability for Offline On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>成功说明结果，学习价值还取决于当前学生是否已掌握。成功参考与当前策略的逐词元似然变化帮助区分已有知识与潜在可吸收部分，再重权离线轨迹。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两条都对，一条学生会了，另一条尚缺关键转折。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.18321">原论文</a> · <a href="../../../../post-training/2609.18321-trajectory-learnability/">实现解读</a> · <a href="#qa-44335d5c4b2a60d2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:trajectory-learnability" data-paper-title="Trajectory Learnability for Offline On-Policy Distillation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Trajectory Learnability for Offline On-Policy Distillation LLM 后训练 National University of Singapore 2026-09-16 用成功轨迹训练参考模型，以参考与当前策略逐 token 对数似然变化衡量可学性，并据此重加权离线 OPD 轨迹。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行逐 token 可学性聚合和轨迹加权；未复刻论文 GPU 训练预算。本地执行逐 token 可学性聚合和轨迹加权；未复刻论文 GPU 训练预算。  On-policy distillation 轨迹加权 LLM 后训练 数据与预算：下一份算力花在哪里 离线OPD为什么比较成功参考模型与当前策略的逐词元似然，而不只按轨迹奖励排序？ 终局成功只能说明轨迹结果，不能说明当前学生在哪些位置还可学习。用成功轨迹训练参考模型，再比较其与当前策略的词元似然变化，可形成轨迹可学性权重。该信号仍依赖参考模型和离线覆盖，不能恢复数据中从未出现的状态，本地只是权重核验证。 例如两条都答对的解法，一条学生已熟练，另一条关键转折尚未掌握；可学性重加权试图区分它们，而非给相同成功标签就等权。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:trajectory-learnability" data-paper-title="Trajectory Learnability for Offline On-Policy Distillation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Trajectory Learnability for Offline On-Policy Distillation LLM 后训练 National University of Singapore 2026-09-16 用成功轨迹训练参考模型，以参考与当前策略逐 token 对数似然变化衡量可学性，并据此重加权离线 OPD 轨迹。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行逐 token 可学性聚合和轨迹加权；未复刻论文 GPU 训练预算。本地执行逐 token 可学性聚合和轨迹加权；未复刻论文 GPU 训练预算。  On-policy distillation 轨迹加权 LLM 后训练 数据与预算：下一份算力花在哪里 离线可学性重权与重新采当前on-policy数据有什么差别？ 重权只在既有轨迹覆盖中分配预算，采新数据可发现新状态。前者不能凭权重恢复库里不存在的路径，不能因为名字含OPD就声称持续实时学生采样。 例如缓存没有新解法，再怎么重权也不会自动生成它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-72e52209edf16fe9">离线可学性重权与重新采当前on-policy数据有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atrajectory-learnability">Trajectory Learnability for Offline On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>重权只在既有轨迹覆盖中分配预算，采新数据可发现新状态。前者不能凭权重恢复库里不存在的路径，不能因为名字含OPD就声称持续实时学生采样。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如缓存没有新解法，再怎么重权也不会自动生成它。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.18321">原论文</a> · <a href="../../../../post-training/2609.18321-trajectory-learnability/">实现解读</a> · <a href="#qa-72e52209edf16fe9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:trajectory-learnability" data-paper-title="Trajectory Learnability for Offline On-Policy Distillation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Trajectory Learnability for Offline On-Policy Distillation LLM 后训练 National University of Singapore 2026-09-16 用成功轨迹训练参考模型，以参考与当前策略逐 token 对数似然变化衡量可学性，并据此重加权离线 OPD 轨迹。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行逐 token 可学性聚合和轨迹加权；未复刻论文 GPU 训练预算。本地执行逐 token 可学性聚合和轨迹加权；未复刻论文 GPU 训练预算。  On-policy distillation 轨迹加权 LLM 后训练 数据与预算：下一份算力花在哪里 本地可学性聚合是否包括论文完整GPU训练？ 不包括，只执行逐词元聚合与轨迹权重。参考和当前概率应评价同一文本前缀并保留版本，不能把不同响应的似然变化相减当可学性。 例如旧模型评A解法、新模型评B解法，差值混入内容改变。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-67fb24ffbb9c3b16">本地可学性聚合是否包括论文完整GPU训练？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Atrajectory-learnability">Trajectory Learnability for Offline On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不包括，只执行逐词元聚合与轨迹权重。参考和当前概率应评价同一文本前缀并保留版本，不能把不同响应的似然变化相减当可学性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如旧模型评A解法、新模型评B解法，差值混入内容改变。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.18321">原论文</a> · <a href="../../../../post-training/2609.18321-trajectory-learnability/">实现解读</a> · <a href="#qa-67fb24ffbb9c3b16">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:growmtp" data-paper-title="GrowMTP: Can RL Grow Its Own Draft Head?" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="GrowMTP: Can RL Grow Its Own Draft Head? LLM 后训练 WeChat AI, Tencent / Peking University 2026-09-15 在 RL rollout 内按被接受的草稿深度训练 MTP head，并与主干梯度解耦。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 depth-coupled acceptance loss；未报告 GPU 加速。本地执行 depth-coupled acceptance loss；未报告 GPU 加速。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  RL 训练加速 推测解码 LLM 后训练 数据与预算：下一份算力花在哪里 GrowMTP为什么在RL过程中同时生长草稿头？ 主策略持续变化会让静态draft过时，利用rollout接受反馈训练MTP头，使加速模块跟随策略。提升草稿效率与提升任务能力是不同目标。 例如策略学会新表达后，草稿头也需学会提议它，才容易被接受。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-growmtp-d690b374" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-43adec038dd6f353">GrowMTP为什么在RL过程中同时生长草稿头？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agrowmtp">GrowMTP: Can RL Grow Its Own Draft Head?</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · WeChat AI, Tencent / Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>主策略持续变化会让静态draft过时，利用rollout接受反馈训练MTP头，使加速模块跟随策略。提升草稿效率与提升任务能力是不同目标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如策略学会新表达后，草稿头也需学会提议它，才容易被接受。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16648">原论文</a> · <a href="../../../../post-training/2609.16648-growmtp/">实现解读</a> · <a href="#qa-43adec038dd6f353">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:growmtp" data-paper-title="GrowMTP: Can RL Grow Its Own Draft Head?" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="GrowMTP: Can RL Grow Its Own Draft Head? LLM 后训练 WeChat AI, Tencent / Peking University 2026-09-15 在 RL rollout 内按被接受的草稿深度训练 MTP head，并与主干梯度解耦。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 depth-coupled acceptance loss；未报告 GPU 加速。本地执行 depth-coupled acceptance loss；未报告 GPU 加速。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  RL 训练加速 推测解码 LLM 后训练 数据与预算：下一份算力花在哪里 GrowMTP为什么按实际接受深度训练草稿头，并把它与主干梯度解耦？ 草稿越深，前面的提议必须先被接受才会真正影响生成，实际接受深度能提供与使用情形相关的训练信号。梯度解耦限制草稿加速目标干扰主策略的奖励学习。接受率与端到端速度还取决于硬件及验证成本，本地深度损失诊断没有测得GPU加速。 例如第三个草稿词元只有前两个通过验证才有用，训练不能假定每个深度都同样可达；改善草稿头也不能自动算作主策略能力提升。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:growmtp" data-paper-title="GrowMTP: Can RL Grow Its Own Draft Head?" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="GrowMTP: Can RL Grow Its Own Draft Head? LLM 后训练 WeChat AI, Tencent / Peking University 2026-09-15 在 RL rollout 内按被接受的草稿深度训练 MTP head，并与主干梯度解耦。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 depth-coupled acceptance loss；未报告 GPU 加速。本地执行 depth-coupled acceptance loss；未报告 GPU 加速。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  RL 训练加速 推测解码 LLM 后训练 数据与预算：下一份算力花在哪里 按接受深度学习与每个future head等权监督有何不同？ 实际可用深度受前面接受事件约束，深度耦合反映这种使用条件；等权假定各头贡献相似。它仍需精确验证，不能因head训练好就跳过target。 例如第三头只有前两步被接受后才可能真正节省生成步骤。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e14ddb8dfe5131f8">按接受深度学习与每个future head等权监督有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agrowmtp">GrowMTP: Can RL Grow Its Own Draft Head?</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · WeChat AI, Tencent / Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>实际可用深度受前面接受事件约束，深度耦合反映这种使用条件；等权假定各头贡献相似。它仍需精确验证，不能因head训练好就跳过target。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如第三头只有前两步被接受后才可能真正节省生成步骤。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16648">原论文</a> · <a href="../../../../post-training/2609.16648-growmtp/">实现解读</a> · <a href="#qa-e14ddb8dfe5131f8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:growmtp" data-paper-title="GrowMTP: Can RL Grow Its Own Draft Head?" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="GrowMTP: Can RL Grow Its Own Draft Head? LLM 后训练 WeChat AI, Tencent / Peking University 2026-09-15 在 RL rollout 内按被接受的草稿深度训练 MTP head，并与主干梯度解耦。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 depth-coupled acceptance loss；未报告 GPU 加速。本地执行 depth-coupled acceptance loss；未报告 GPU 加速。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  RL 训练加速 推测解码 LLM 后训练 数据与预算：下一份算力花在哪里 GrowMTP为何要与主干梯度解耦，本地测了加速吗？ 加速损失不应未经控制改变主RL目标，解耦限定其作用路径。当前只执行深度接受损失，未报告GPU吞吐，不能由接受率公式推算实际加速。 例如草稿变准也可能增加计算，端到端速度还需真实计时。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-16c4706125d30fb6">GrowMTP为何要与主干梯度解耦，本地测了加速吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agrowmtp">GrowMTP: Can RL Grow Its Own Draft Head?</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · WeChat AI, Tencent / Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>加速损失不应未经控制改变主RL目标，解耦限定其作用路径。当前只执行深度接受损失，未报告GPU吞吐，不能由接受率公式推算实际加速。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如草稿变准也可能增加计算，端到端速度还需真实计时。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16648">原论文</a> · <a href="../../../../post-training/2609.16648-growmtp/">实现解读</a> · <a href="#qa-16c4706125d30fb6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:stride-opd" data-paper-title="Know When to Stop, Where to Restart: Accelerating Multi-Turn Agentic On-Policy Distillation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Know When to Stop, Where to Restart: Accelerating Multi-Turn Agentic On-Policy Distillation LLM 后训练 University of Science and Technology of China / Ant Group 2026-09-13 teacher 累积置信度越界时早停，并从最弱正确 turn 的缓存前缀重新开始。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 未复现大模型 rollout 吞吐。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行早停和前缀重启；未复现大模型 rollout 吞吐。本地执行早停和前缀重启；未复现大模型 rollout 吞吐。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  On-policy distillation 多轮加速 LLM 后训练 数据与预算：下一份算力花在哪里 STRIDE-OPD为什么从最弱正确turn重新开始？ 重启已缓存的可学状态，可把预算放在勉强掌握的轮次，而非反复生成熟悉前段；正确资格提供安全起点，弱表示仍有指导空间。 例如第一轮已稳定，第二轮刚能做对，下次可从第二轮前缀重试。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-stride-opd-55204229" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8ab8a5185b1e6dcf">STRIDE-OPD为什么从最弱正确turn重新开始？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Astride-opd">Know When to Stop, Where to Restart: Accelerating Multi-Turn Agentic On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China / Ant Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>重启已缓存的可学状态，可把预算放在勉强掌握的轮次，而非反复生成熟悉前段；正确资格提供安全起点，弱表示仍有指导空间。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如第一轮已稳定，第二轮刚能做对，下次可从第二轮前缀重试。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.14636">原论文</a> · <a href="../../../../post-training/2609.14636-stride-opd/">实现解读</a> · <a href="#qa-8ab8a5185b1e6dcf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:stride-opd" data-paper-title="Know When to Stop, Where to Restart: Accelerating Multi-Turn Agentic On-Policy Distillation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Know When to Stop, Where to Restart: Accelerating Multi-Turn Agentic On-Policy Distillation LLM 后训练 University of Science and Technology of China / Ant Group 2026-09-13 teacher 累积置信度越界时早停，并从最弱正确 turn 的缓存前缀重新开始。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 未复现大模型 rollout 吞吐。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行早停和前缀重启；未复现大模型 rollout 吞吐。本地执行早停和前缀重启；未复现大模型 rollout 吞吐。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  On-policy distillation 多轮加速 LLM 后训练 数据与预算：下一份算力花在哪里 STRIDE-OPD为什么把早停与最弱正确轮次的前缀重启配在一起？ 教师累积置信度触发停止，可避免在低价值后续上继续花费；缓存中较弱但正确的轮次则提供可学习的重启状态，把预算回投到仍需加强的位置。停止和重启是不同决策，不能等同直接跳到标准答案。本地状态核未验证大模型多轮生成吞吐。 例如一段工具交互后续已无新增指导，可停止；下一次从此前勉强完成的正确轮次重试，而不是总从任务开头重复熟悉步骤。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:stride-opd" data-paper-title="Know When to Stop, Where to Restart: Accelerating Multi-Turn Agentic On-Policy Distillation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Know When to Stop, Where to Restart: Accelerating Multi-Turn Agentic On-Policy Distillation LLM 后训练 University of Science and Technology of China / Ant Group 2026-09-13 teacher 累积置信度越界时早停，并从最弱正确 turn 的缓存前缀重新开始。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 未复现大模型 rollout 吞吐。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行早停和前缀重启；未复现大模型 rollout 吞吐。本地执行早停和前缀重启；未复现大模型 rollout 吞吐。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  On-policy distillation 多轮加速 LLM 后训练 数据与预算：下一份算力花在哪里 早停与统一缩短所有轨迹有何不同？ 早停由教师累积置信度触发，并与前缀重启配合；统一长度上限不依状态。两者数据覆盖不同，缩短轨迹也不自动保证任务完整或节省同等计算。 例如一条早已充分、一条仍需探索，不必在同一token数截断。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d5cd1beecf336df0">早停与统一缩短所有轨迹有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Astride-opd">Know When to Stop, Where to Restart: Accelerating Multi-Turn Agentic On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China / Ant Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>早停由教师累积置信度触发，并与前缀重启配合；统一长度上限不依状态。两者数据覆盖不同，缩短轨迹也不自动保证任务完整或节省同等计算。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一条早已充分、一条仍需探索，不必在同一token数截断。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.14636">原论文</a> · <a href="../../../../post-training/2609.14636-stride-opd/">实现解读</a> · <a href="#qa-d5cd1beecf336df0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:stride-opd" data-paper-title="Know When to Stop, Where to Restart: Accelerating Multi-Turn Agentic On-Policy Distillation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Know When to Stop, Where to Restart: Accelerating Multi-Turn Agentic On-Policy Distillation LLM 后训练 University of Science and Technology of China / Ant Group 2026-09-13 teacher 累积置信度越界时早停，并从最弱正确 turn 的缓存前缀重新开始。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 未复现大模型 rollout 吞吐。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行早停和前缀重启；未复现大模型 rollout 吞吐。本地执行早停和前缀重启；未复现大模型 rollout 吞吐。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  On-policy distillation 多轮加速 LLM 后训练 数据与预算：下一份算力花在哪里 STRIDE缓存前缀能在任意环境状态直接恢复吗？ 需保证前缀与实际动作观察状态对应，不能只拷文本却丢环境状态。当前本地验证早停重启核，未复现大模型rollout吞吐，不能把状态机通过当生产速度证据。 例如工具已执行一次，恢复时不能重复副作用而假装同一状态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-857ce14c8b27797d">STRIDE缓存前缀能在任意环境状态直接恢复吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Astride-opd">Know When to Stop, Where to Restart: Accelerating Multi-Turn Agentic On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China / Ant Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>需保证前缀与实际动作观察状态对应，不能只拷文本却丢环境状态。当前本地验证早停重启核，未复现大模型rollout吞吐，不能把状态机通过当生产速度证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如工具已执行一次，恢复时不能重复副作用而假装同一状态。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.14636">原论文</a> · <a href="../../../../post-training/2609.14636-stride-opd/">实现解读</a> · <a href="#qa-857ce14c8b27797d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:df-opd" data-paper-title="Data-free On-policy Distillation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Data-free On-policy Distillation LLM 后训练 Institute of Automation, Chinese Academy of Sciences / Tencent 2026-09-12 由教师在自身策略空间生成问题，减少对外部后训练语料的依赖。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行自生成问题的策略特征诊断；未生成自然语言训练集。本地执行自生成问题的策略特征诊断；未生成自然语言训练集。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  On-policy distillation 数据合成 LLM 后训练 数据与预算：下一份算力花在哪里 Data-free OPD说data-free具体减少什么依赖？ 教师自行生成训练问题，减少额外收集后训练题库的需求；教师预训练知识和生成偏好仍是信息来源，不意味着从零无数据学习。 例如老师出练习题无需人工题库，但其出题能力来自已有训练。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-df-opd-48f2c181" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-152303e6ac1faa65">Data-free OPD说data-free具体减少什么依赖？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adf-opd">Data-free On-policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Automation, Chinese Academy of Sciences / Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>教师自行生成训练问题，减少额外收集后训练题库的需求；教师预训练知识和生成偏好仍是信息来源，不意味着从零无数据学习。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如老师出练习题无需人工题库，但其出题能力来自已有训练。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.14193">原论文</a> · <a href="../../../../post-training/2609.14193-df-opd/">实现解读</a> · <a href="#qa-152303e6ac1faa65">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:df-opd" data-paper-title="Data-free On-policy Distillation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Data-free On-policy Distillation LLM 后训练 Institute of Automation, Chinese Academy of Sciences / Tencent 2026-09-12 由教师在自身策略空间生成问题，减少对外部后训练语料的依赖。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行自生成问题的策略特征诊断；未生成自然语言训练集。本地执行自生成问题的策略特征诊断；未生成自然语言训练集。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  On-policy distillation 数据合成 LLM 后训练 数据与预算：下一份算力花在哪里 Data-free OPD自己生成问题，为什么仍不能说训练不依赖任何先验知识？ 问题来自教师自身策略而非外部后训练题库，减少的是额外数据收集依赖；教师参数、生成分布和筛选条件仍决定课程覆盖。自生成也可能重复已有模式或产生不可靠任务，需要验证质量。本地只做问题生成的策略特征诊断，尚未生成自然语言训练集。 例如教师围绕已知代码技能提出练习，可减少人工题库；但如果它一直生成同一类循环题，学生不会因此自动学到未覆盖的并发问题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:df-opd" data-paper-title="Data-free On-policy Distillation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Data-free On-policy Distillation LLM 后训练 Institute of Automation, Chinese Academy of Sciences / Tencent 2026-09-12 由教师在自身策略空间生成问题，减少对外部后训练语料的依赖。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行自生成问题的策略特征诊断；未生成自然语言训练集。本地执行自生成问题的策略特征诊断；未生成自然语言训练集。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  On-policy distillation 数据合成 LLM 后训练 数据与预算：下一份算力花在哪里 教师自生成课程与固定公开题库在覆盖上有什么取舍？ 自生成可围绕教师能力定制，也可能重复或遗漏；固定题库覆盖可审计但收集成本高。两者需独立验证质量，不能把自然语言格式合法当有效任务。 例如教师反复只出线性方程题，不会自动覆盖几何推理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5d4419882e5e88b9">教师自生成课程与固定公开题库在覆盖上有什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adf-opd">Data-free On-policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Automation, Chinese Academy of Sciences / Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>自生成可围绕教师能力定制，也可能重复或遗漏；固定题库覆盖可审计但收集成本高。两者需独立验证质量，不能把自然语言格式合法当有效任务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如教师反复只出线性方程题，不会自动覆盖几何推理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.14193">原论文</a> · <a href="../../../../post-training/2609.14193-df-opd/">实现解读</a> · <a href="#qa-5d4419882e5e88b9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:df-opd" data-paper-title="Data-free On-policy Distillation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Data-free On-policy Distillation LLM 后训练 Institute of Automation, Chinese Academy of Sciences / Tencent 2026-09-12 由教师在自身策略空间生成问题，减少对外部后训练语料的依赖。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行自生成问题的策略特征诊断；未生成自然语言训练集。本地执行自生成问题的策略特征诊断；未生成自然语言训练集。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  On-policy distillation 数据合成 LLM 后训练 数据与预算：下一份算力花在哪里 DF-OPD本地生成过真实自然语言训练集吗？ 尚未，只做自生成问题的策略特征诊断。完整流程还需实际问题生成、质量筛选与学生蒸馏记录，不能用候选索引变化冒充真实教师出题。 例如抽到一个特征编号不是一条已验证的数学题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-75cbfa58aed85ace">DF-OPD本地生成过真实自然语言训练集吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adf-opd">Data-free On-policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Automation, Chinese Academy of Sciences / Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>尚未，只做自生成问题的策略特征诊断。完整流程还需实际问题生成、质量筛选与学生蒸馏记录，不能用候选索引变化冒充真实教师出题。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如抽到一个特征编号不是一条已验证的数学题。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.14193">原论文</a> · <a href="../../../../post-training/2609.14193-df-opd/">实现解读</a> · <a href="#qa-75cbfa58aed85ace">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:adaptive-opd-gate" data-paper-title="A Unified Per-Token Gating Family for On-Policy Distillation: FKL/RKL Mixing with Multi-Channel and Bias Coefficients" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="A Unified Per-Token Gating Family for On-Policy Distillation: FKL/RKL Mixing with Multi-Channel and Bias Coefficients LLM 后训练 Xiaohongshu 2026-09-10 把熵、不确定性、reference 偏移和教师—学生差距组合成逐 token gate，在 FKL/RKL 蒸馏方向间自适应分配。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行四信号 gate；结果仅是机制诊断，不把探索性结果写成稳定胜出。本地执行四信号 gate；结果仅是机制诊断，不把探索性结果写成稳定胜出。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  On-policy distillation 逐 token 自适应门控 LLM 后训练 数据与预算：下一份算力花在哪里 自适应OPD gate为什么组合多路信号？ 熵、不确定性、参考偏移与师生gap各描述不同状态，单一信号可能不足。组合门控在每位置分配正反KL指导，仍依赖这些代理与目标的关系。 例如教师确定但偏离参考很大，与教师不确定却接近学生，是不同情况。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-adaptive-opd-gate-493b3a1b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0835105825885790">自适应OPD gate为什么组合多路信号？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aadaptive-opd-gate">A Unified Per-Token Gating Family for On-Policy Distillation: FKL/RKL Mixing with Multi-Channel and Bias Coefficients</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>熵、不确定性、参考偏移与师生gap各描述不同状态，单一信号可能不足。组合门控在每位置分配正反KL指导，仍依赖这些代理与目标的关系。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如教师确定但偏离参考很大，与教师不确定却接近学生，是不同情况。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11768">原论文</a> · <a href="../../../../post-training/2609.11768-adaptive-opd-gate/">实现解读</a> · <a href="#qa-0835105825885790">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:adaptive-opd-gate" data-paper-title="A Unified Per-Token Gating Family for On-Policy Distillation: FKL/RKL Mixing with Multi-Channel and Bias Coefficients" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="A Unified Per-Token Gating Family for On-Policy Distillation: FKL/RKL Mixing with Multi-Channel and Bias Coefficients LLM 后训练 Xiaohongshu 2026-09-10 把熵、不确定性、reference 偏移和教师—学生差距组合成逐 token gate，在 FKL/RKL 蒸馏方向间自适应分配。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行四信号 gate；结果仅是机制诊断，不把探索性结果写成稳定胜出。本地执行四信号 gate；结果仅是机制诊断，不把探索性结果写成稳定胜出。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  On-policy distillation 逐 token 自适应门控 LLM 后训练 数据与预算：下一份算力花在哪里 逐词元门控为何混合FKL与RKL，而不是对整条回答只选一个散度方向？ 不同位置的教师不确定性、师生差距与参考偏移不同，统一散度方向可能把覆盖与集中之间的取舍强加给所有词元。门控组合多路信号，在位置层分配正向和反向蒸馏权重。门控是启发监督分配，不是正确性证明，本地四信号实验也没有稳定胜出结论。 例如关键分叉处需保留教师多种选择，已收敛的格式位置可更集中；不能因为一句话整体可靠，就认为每个词元都应使用相同权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:adaptive-opd-gate" data-paper-title="A Unified Per-Token Gating Family for On-Policy Distillation: FKL/RKL Mixing with Multi-Channel and Bias Coefficients" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="A Unified Per-Token Gating Family for On-Policy Distillation: FKL/RKL Mixing with Multi-Channel and Bias Coefficients LLM 后训练 Xiaohongshu 2026-09-10 把熵、不确定性、reference 偏移和教师—学生差距组合成逐 token gate，在 FKL/RKL 蒸馏方向间自适应分配。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行四信号 gate；结果仅是机制诊断，不把探索性结果写成稳定胜出。本地执行四信号 gate；结果仅是机制诊断，不把探索性结果写成稳定胜出。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  On-policy distillation 逐 token 自适应门控 LLM 后训练 数据与预算：下一份算力花在哪里 逐token混合FKL/RKL与固定整句比例有何区别？ 前者可按位置分配覆盖和集中压力，后者给所有词同一取舍。更灵活也增加调参和过拟合风险，机制诊断不能写成稳定全面胜出。 例如关键分叉与确定格式词不必承担相同散度混合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ae53784d12de3186">逐token混合FKL/RKL与固定整句比例有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aadaptive-opd-gate">A Unified Per-Token Gating Family for On-Policy Distillation: FKL/RKL Mixing with Multi-Channel and Bias Coefficients</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者可按位置分配覆盖和集中压力，后者给所有词同一取舍。更灵活也增加调参和过拟合风险，机制诊断不能写成稳定全面胜出。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如关键分叉与确定格式词不必承担相同散度混合。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11768">原论文</a> · <a href="../../../../post-training/2609.11768-adaptive-opd-gate/">实现解读</a> · <a href="#qa-ae53784d12de3186">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:adaptive-opd-gate" data-paper-title="A Unified Per-Token Gating Family for On-Policy Distillation: FKL/RKL Mixing with Multi-Channel and Bias Coefficients" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="A Unified Per-Token Gating Family for On-Policy Distillation: FKL/RKL Mixing with Multi-Channel and Bias Coefficients LLM 后训练 Xiaohongshu 2026-09-10 把熵、不确定性、reference 偏移和教师—学生差距组合成逐 token gate，在 FKL/RKL 蒸馏方向间自适应分配。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行四信号 gate；结果仅是机制诊断，不把探索性结果写成稳定胜出。本地执行四信号 gate；结果仅是机制诊断，不把探索性结果写成稳定胜出。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  On-policy distillation 逐 token 自适应门控 LLM 后训练 数据与预算：下一份算力花在哪里 四信号gate本地探索结果能直接用于能力晋级吗？ 不能，当前是确定性机制诊断，完整模型效果与公平预算尚未确立。实现要明确方向、信号版本和gate梯度，不可只改注册名就声称新训练已接入。 例如某小候选任务一次更高分，仍不足以推广到开放式语言能力。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e4d08eed3b9a498f">四信号gate本地探索结果能直接用于能力晋级吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aadaptive-opd-gate">A Unified Per-Token Gating Family for On-Policy Distillation: FKL/RKL Mixing with Multi-Channel and Bias Coefficients</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，当前是确定性机制诊断，完整模型效果与公平预算尚未确立。实现要明确方向、信号版本和gate梯度，不可只改注册名就声称新训练已接入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某小候选任务一次更高分，仍不足以推广到开放式语言能力。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11768">原论文</a> · <a href="../../../../post-training/2609.11768-adaptive-opd-gate/">实现解读</a> · <a href="#qa-e4d08eed3b9a498f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:locus" data-paper-title="LOCUS: Task-Aware Low-Rank Post-Training for Token-Efficient Language Generation" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="LOCUS: Task-Aware Low-Rank Post-Training for Token-Efficient Language Generation LLM 后训练 University of Washington 2026-09-10 学习任务相关低秩后训练子空间，只在紧凑方向上更新以缩短回答，同时保留任务能力。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地用样本特征 SVD 投影策略梯度；未训练论文规模语言模型。本地用样本特征 SVD 投影策略梯度；未训练论文规模语言模型。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  低秩后训练 Token 效率 LLM 后训练 数据与预算：下一份算力花在哪里 LOCUS为什么把任务更新压到低秩方向？ 目标是用紧凑任务相关变化改善token效率，限制无关漂移，同时保留任务能力。低秩只是可行空间限制，子空间若漏关键方向也会损害表现。 例如删重复表述所需变化不必任意重写全部模型参数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-locus-5c47d1f6" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-27a97fe3f318d1e5">LOCUS为什么把任务更新压到低秩方向？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Alocus">LOCUS: Task-Aware Low-Rank Post-Training for Token-Efficient Language Generation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标是用紧凑任务相关变化改善token效率，限制无关漂移，同时保留任务能力。低秩只是可行空间限制，子空间若漏关键方向也会损害表现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如删重复表述所需变化不必任意重写全部模型参数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11739">原论文</a> · <a href="../../../../post-training/2609.11739-locus/">实现解读</a> · <a href="#qa-27a97fe3f318d1e5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:locus" data-paper-title="LOCUS: Task-Aware Low-Rank Post-Training for Token-Efficient Language Generation" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="LOCUS: Task-Aware Low-Rank Post-Training for Token-Efficient Language Generation LLM 后训练 University of Washington 2026-09-10 学习任务相关低秩后训练子空间，只在紧凑方向上更新以缩短回答，同时保留任务能力。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地用样本特征 SVD 投影策略梯度；未训练论文规模语言模型。本地用样本特征 SVD 投影策略梯度；未训练论文规模语言模型。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  低秩后训练 Token 效率 LLM 后训练 数据与预算：下一份算力花在哪里 LOCUS把更新限制在任务相关低秩子空间，为什么有机会缩短回答却不等于直接截断？ 低秩约束作用于参数更新方向，试图保留任务相关的有效变化、限制无关漂移，简洁性通过后训练目标学习。直接截断则在生成后强行删掉内容，可能损失必要步骤。子空间是否覆盖目标能力仍需检验，本地特征SVD投影不能证明大模型长度与能力兼得。 例如让模型学会少写重复检查，与把每条证明的后半段删除不同；若所选子空间不包含关键推理方向，即使回答变短也可能失去正确性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:locus" data-paper-title="LOCUS: Task-Aware Low-Rank Post-Training for Token-Efficient Language Generation" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="LOCUS: Task-Aware Low-Rank Post-Training for Token-Efficient Language Generation LLM 后训练 University of Washington 2026-09-10 学习任务相关低秩后训练子空间，只在紧凑方向上更新以缩短回答，同时保留任务能力。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地用样本特征 SVD 投影策略梯度；未训练论文规模语言模型。本地用样本特征 SVD 投影策略梯度；未训练论文规模语言模型。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  低秩后训练 Token 效率 LLM 后训练 数据与预算：下一份算力花在哪里 任务低秩更新与生成后截断回答有什么区别？ 前者训练模型选择更简洁的行为，后者强行删输出并可能丢关键步骤。简洁性应与正确性共同评估，不能只看到词数下降就认定效率改善。 例如少写重复检查与把证明最后结论切掉，长度都变短但质量不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-00d679c76eed8a3e">任务低秩更新与生成后截断回答有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Alocus">LOCUS: Task-Aware Low-Rank Post-Training for Token-Efficient Language Generation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者训练模型选择更简洁的行为，后者强行删输出并可能丢关键步骤。简洁性应与正确性共同评估，不能只看到词数下降就认定效率改善。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如少写重复检查与把证明最后结论切掉，长度都变短但质量不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11739">原论文</a> · <a href="../../../../post-training/2609.11739-locus/">实现解读</a> · <a href="#qa-00d679c76eed8a3e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:locus" data-paper-title="LOCUS: Task-Aware Low-Rank Post-Training for Token-Efficient Language Generation" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="LOCUS: Task-Aware Low-Rank Post-Training for Token-Efficient Language Generation LLM 后训练 University of Washington 2026-09-10 学习任务相关低秩后训练子空间，只在紧凑方向上更新以缩短回答，同时保留任务能力。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地用样本特征 SVD 投影策略梯度；未训练论文规模语言模型。本地用样本特征 SVD 投影策略梯度；未训练论文规模语言模型。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  低秩后训练 Token 效率 LLM 后训练 数据与预算：下一份算力花在哪里 LOCUS本地SVD投影代表训练了真实语言模型吗？ 没有，只在样本特征子空间投影策略梯度。需审查rank、基正交和投影前后梯度边界，不能把随机低秩矩阵叫已学到任务语义子空间。 例如数值上投影成功，不表示该基覆盖真实推理关键能力。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a1961e19bf470995">LOCUS本地SVD投影代表训练了真实语言模型吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Alocus">LOCUS: Task-Aware Low-Rank Post-Training for Token-Efficient Language Generation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有，只在样本特征子空间投影策略梯度。需审查rank、基正交和投影前后梯度边界，不能把随机低秩矩阵叫已学到任务语义子空间。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如数值上投影成功，不表示该基覆盖真实推理关键能力。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11739">原论文</a> · <a href="../../../../post-training/2609.11739-locus/">实现解读</a> · <a href="#qa-a1961e19bf470995">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sparse-opd" data-paper-title="Extremely Sparse Supervision Incentivizes Reasoning Ability" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Extremely Sparse Supervision Incentivizes Reasoning Ability LLM 后训练 Amazon / Duke University 2026-09-03 常规 on-policy distillation 对生成轨迹的每个 token 使用教师分布。论文发现只挑一到两个关键位置、约占全部 token 的 0.05%，也能达到或超过全 token 训练。最大正差异 token 尤其有效，说明有效后训练可能更接近“反思关键步骤”而非逐字纠错。 复现级别：核心目标函数 mini-suite。复现级别：核心目标函数 mini-suite。在统一 OPD runner 中实现最大差异、最小差异和随机稀疏 token 选择。未执行 Qwen/Llama 全参数 OPD 或 PPO；当前方法不宣传 CUDA 路径，因此无需 GPU receipt。arithmetic-smoke、seeds 42/43/44 的监督位置数、监督比例、选择差异和目标值见 metrics/arithmetic-smoke-seeds42-44.json。  极稀疏 On-policy distillation LLM 后训练 数据与预算：下一份算力花在哪里 Sparse OPD为什么研究一两个关键位置也能否提供学习？ 全词元监督可能大量冗余，选教师与学生重要正差异处检验信息是否集中。特定实验少量有效不表示所有任务都可固定只教一词。 例如一个关键运算符改正可能比整段连接词模仿更影响结论。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-sparse-opd-2b68a2ae" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c4e9c98cacdbf422">Sparse OPD为什么研究一两个关键位置也能否提供学习？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asparse-opd">Extremely Sparse Supervision Incentivizes Reasoning Ability</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Amazon / Duke University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全词元监督可能大量冗余，选教师与学生重要正差异处检验信息是否集中。特定实验少量有效不表示所有任务都可固定只教一词。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个关键运算符改正可能比整段连接词模仿更影响结论。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04565">原论文</a> · <a href="../../../../post-training/2609.04565-sparse-opd/">实现解读</a> · <a href="#qa-c4e9c98cacdbf422">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sparse-opd" data-paper-title="Extremely Sparse Supervision Incentivizes Reasoning Ability" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Extremely Sparse Supervision Incentivizes Reasoning Ability LLM 后训练 Amazon / Duke University 2026-09-03 常规 on-policy distillation 对生成轨迹的每个 token 使用教师分布。论文发现只挑一到两个关键位置、约占全部 token 的 0.05%，也能达到或超过全 token 训练。最大正差异 token 尤其有效，说明有效后训练可能更接近“反思关键步骤”而非逐字纠错。 复现级别：核心目标函数 mini-suite。复现级别：核心目标函数 mini-suite。在统一 OPD runner 中实现最大差异、最小差异和随机稀疏 token 选择。未执行 Qwen/Llama 全参数 OPD 或 PPO；当前方法不宣传 CUDA 路径，因此无需 GPU receipt。arithmetic-smoke、seeds 42/43/44 的监督位置数、监督比例、选择差异和目标值见 metrics/arithmetic-smoke-seeds42-44.json。  极稀疏 On-policy distillation LLM 后训练 数据与预算：下一份算力花在哪里 Sparse OPD只监督少数最大正差异位置，为什么仍要保留完整学生轨迹上下文？ 关键位置的教师分布依赖前面实际生成的推理，去掉未监督部分会改变该状态。稀疏化改变的是哪些位置产生梯度，而不是把其余词元从条件输入删除。少量位置有效是实验条件下的发现，不能推断任何任务都只需一两个词元，本地也未做全参数蒸馏。 例如只学习一次关键纠错词元，教师仍需看到之前的计算才能判断它；把整段前文删掉后监督同一个字，已经变成不同任务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sparse-opd" data-paper-title="Extremely Sparse Supervision Incentivizes Reasoning Ability" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Extremely Sparse Supervision Incentivizes Reasoning Ability LLM 后训练 Amazon / Duke University 2026-09-03 常规 on-policy distillation 对生成轨迹的每个 token 使用教师分布。论文发现只挑一到两个关键位置、约占全部 token 的 0.05%，也能达到或超过全 token 训练。最大正差异 token 尤其有效，说明有效后训练可能更接近“反思关键步骤”而非逐字纠错。 复现级别：核心目标函数 mini-suite。复现级别：核心目标函数 mini-suite。在统一 OPD runner 中实现最大差异、最小差异和随机稀疏 token 选择。未执行 Qwen/Llama 全参数 OPD 或 PPO；当前方法不宣传 CUDA 路径，因此无需 GPU receipt。arithmetic-smoke、seeds 42/43/44 的监督位置数、监督比例、选择差异和目标值见 metrics/arithmetic-smoke-seeds42-44.json。  极稀疏 On-policy distillation LLM 后训练 数据与预算：下一份算力花在哪里 稀疏监督与更短生成为什么不是同一效率优化？ 稀疏化减少被监督位置，仍需保留学生轨迹并可能评分全段寻找关键点；短生成直接改变采样成本和状态覆盖。不能把少loss token数等同总推理成本下降。 例如先生成千词再选一词，仍已支付千词生成费用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-464fbb3a8d32673d">稀疏监督与更短生成为什么不是同一效率优化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asparse-opd">Extremely Sparse Supervision Incentivizes Reasoning Ability</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Amazon / Duke University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>稀疏化减少被监督位置，仍需保留学生轨迹并可能评分全段寻找关键点；短生成直接改变采样成本和状态覆盖。不能把少loss token数等同总推理成本下降。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先生成千词再选一词，仍已支付千词生成费用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04565">原论文</a> · <a href="../../../../post-training/2609.04565-sparse-opd/">实现解读</a> · <a href="#qa-464fbb3a8d32673d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sparse-opd" data-paper-title="Extremely Sparse Supervision Incentivizes Reasoning Ability" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Extremely Sparse Supervision Incentivizes Reasoning Ability LLM 后训练 Amazon / Duke University 2026-09-03 常规 on-policy distillation 对生成轨迹的每个 token 使用教师分布。论文发现只挑一到两个关键位置、约占全部 token 的 0.05%，也能达到或超过全 token 训练。最大正差异 token 尤其有效，说明有效后训练可能更接近“反思关键步骤”而非逐字纠错。 复现级别：核心目标函数 mini-suite。复现级别：核心目标函数 mini-suite。在统一 OPD runner 中实现最大差异、最小差异和随机稀疏 token 选择。未执行 Qwen/Llama 全参数 OPD 或 PPO；当前方法不宣传 CUDA 路径，因此无需 GPU receipt。arithmetic-smoke、seeds 42/43/44 的监督位置数、监督比例、选择差异和目标值见 metrics/arithmetic-smoke-seeds42-44.json。  极稀疏 On-policy distillation LLM 后训练 数据与预算：下一份算力花在哪里 Sparse OPD未选位置的梯度与上下文如何区分？ 未选token不产生对应直接损失，但保留为后续条件，模型共享参数仍可能间接受影响。本地未执行真实Qwen或Llama全参数训练，不能据候选核复述原表成绩。 例如不监督第二步，并不表示第三步评分时可以删掉第二步。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-efb25fd7e2942129">Sparse OPD未选位置的梯度与上下文如何区分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asparse-opd">Extremely Sparse Supervision Incentivizes Reasoning Ability</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Amazon / Duke University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>未选token不产生对应直接损失，但保留为后续条件，模型共享参数仍可能间接受影响。本地未执行真实Qwen或Llama全参数训练，不能据候选核复述原表成绩。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如不监督第二步，并不表示第三步评分时可以删掉第二步。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04565">原论文</a> · <a href="../../../../post-training/2609.04565-sparse-opd/">实现解读</a> · <a href="#qa-efb25fd7e2942129">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rail" data-paper-title="Optimizing What Policies Learn From: Recoverability-Aware Rollout Intervention Learning" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Optimizing What Policies Learn From: Recoverability-Aware Rollout Intervention Learning LLM 后训练 University of Notre Dame / Amazon 2026-08-05 主题：rollout 预算分配。均匀 rollout 浪费预算，静态启发式又跟不上策略变化。RAIL 把干预位置与方式视为 contextual bandit，并通过 shadow-to-live 轨迹学习 recoverability controller。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的 rollout 预算分配算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/arithmetic-smoke-seed42.json，不提交 checkpoint 或原始运行目录。  rollout 预算分配 LLM 后训练 数据与预算：下一份算力花在哪里 RAIL为什么学习recoverability而不是只看不确定性？ 不确定状态未必可修复，干预应带来预期恢复收益并考虑成本。控制器把位置和方式作为条件决策，避免均匀追加预算或长期固定启发式。 例如缺一次工具重试与前提完全错的轨迹，值得投入的程度不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-rail-7f7d9ac0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c263ba6e6c66676d">RAIL为什么学习recoverability而不是只看不确定性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arail">Optimizing What Policies Learn From: Recoverability-Aware Rollout Intervention Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Notre Dame / Amazon</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不确定状态未必可修复，干预应带来预期恢复收益并考虑成本。控制器把位置和方式作为条件决策，避免均匀追加预算或长期固定启发式。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如缺一次工具重试与前提完全错的轨迹，值得投入的程度不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05080">原论文</a> · <a href="../../../../post-training/2608.05080-rail/">实现解读</a> · <a href="#qa-c263ba6e6c66676d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rail" data-paper-title="Optimizing What Policies Learn From: Recoverability-Aware Rollout Intervention Learning" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Optimizing What Policies Learn From: Recoverability-Aware Rollout Intervention Learning LLM 后训练 University of Notre Dame / Amazon 2026-08-05 主题：rollout 预算分配。均匀 rollout 浪费预算，静态启发式又跟不上策略变化。RAIL 把干预位置与方式视为 contextual bandit，并通过 shadow-to-live 轨迹学习 recoverability controller。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的 rollout 预算分配算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/arithmetic-smoke-seed42.json，不提交 checkpoint 或原始运行目录。  rollout 预算分配 LLM 后训练 数据与预算：下一份算力花在哪里 RAIL为什么把干预位置与方式当作带成本的决策，而不总在最不确定处多采样？ 不确定不代表能够恢复，一些状态追加预算也难以改变结果。控制器根据状态学习不同干预的可恢复收益，并扣除成本；从影子评估到实际执行，使调度随策略变化调整。恢复信号需要真实可审计反馈，不能读取标准答案来选动作，本地未运行原文大规模环境。 例如一条轨迹只差一次工具重试，另一条已因前提错误无从修复，相同追加预算可能收益不同；单按熵高低无法区分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rail" data-paper-title="Optimizing What Policies Learn From: Recoverability-Aware Rollout Intervention Learning" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Optimizing What Policies Learn From: Recoverability-Aware Rollout Intervention Learning LLM 后训练 University of Notre Dame / Amazon 2026-08-05 主题：rollout 预算分配。均匀 rollout 浪费预算，静态启发式又跟不上策略变化。RAIL 把干预位置与方式视为 contextual bandit，并通过 shadow-to-live 轨迹学习 recoverability controller。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的 rollout 预算分配算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/arithmetic-smoke-seed42.json，不提交 checkpoint 或原始运行目录。  rollout 预算分配 LLM 后训练 数据与预算：下一份算力花在哪里 shadow-to-live评估与直接拿gold选择干预有何不同？ 前者通过允许的试探和实际反馈学习恢复价值，gold选择是不可用的oracle。控制器部署输入必须保持公开，不能把训练诊断标注直接作为可见状态。 例如知道标准计划后精准重启，只能算oracle诊断而非智能控制。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-fc3188e5d5410b22">shadow-to-live评估与直接拿gold选择干预有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arail">Optimizing What Policies Learn From: Recoverability-Aware Rollout Intervention Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Notre Dame / Amazon</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者通过允许的试探和实际反馈学习恢复价值，gold选择是不可用的oracle。控制器部署输入必须保持公开，不能把训练诊断标注直接作为可见状态。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如知道标准计划后精准重启，只能算oracle诊断而非智能控制。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05080">原论文</a> · <a href="../../../../post-training/2608.05080-rail/">实现解读</a> · <a href="#qa-fc3188e5d5410b22">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rail" data-paper-title="Optimizing What Policies Learn From: Recoverability-Aware Rollout Intervention Learning" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Optimizing What Policies Learn From: Recoverability-Aware Rollout Intervention Learning LLM 后训练 University of Notre Dame / Amazon 2026-08-05 主题：rollout 预算分配。均匀 rollout 浪费预算，静态启发式又跟不上策略变化。RAIL 把干预位置与方式视为 contextual bandit，并通过 shadow-to-live 轨迹学习 recoverability controller。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的 rollout 预算分配算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/arithmetic-smoke-seed42.json，不提交 checkpoint 或原始运行目录。  rollout 预算分配 LLM 后训练 数据与预算：下一份算力花在哪里 RAIL当前本地路径能支持哪些声明？ 可验证干预选择与成本目标的参考机制，不含原文大模型、专有环境或昂贵judge。需实际执行并评价后才称能力集成，不能只凭argmax公式报告预算收益。 例如随机生成一组恢复分数后选最大值，尚未测真实轨迹能否恢复。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e56f84403d3fc865">RAIL当前本地路径能支持哪些声明？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arail">Optimizing What Policies Learn From: Recoverability-Aware Rollout Intervention Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Notre Dame / Amazon</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>可验证干预选择与成本目标的参考机制，不含原文大模型、专有环境或昂贵judge。需实际执行并评价后才称能力集成，不能只凭argmax公式报告预算收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如随机生成一组恢复分数后选最大值，尚未测真实轨迹能否恢复。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05080">原论文</a> · <a href="../../../../post-training/2608.05080-rail/">实现解读</a> · <a href="#qa-e56f84403d3fc865">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:specroll" data-paper-title="SpecRoll: Fast-Slow Verifier-Feedback Adaptation for Speculative Reinforcement Learning Rollouts" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="SpecRoll: Fast-Slow Verifier-Feedback Adaptation for Speculative Reinforcement Learning Rollouts LLM 后训练 VNU University of Engineering and Technology / Viettel AI 2026-08-05 主题：RL rollout 加速。RL 中 target policy 持续变化，静态 drafter 很快过时。SpecRoll 用 future-token heads 提议、Reflex 做无反传的快速隐状态纠偏，并只在持续退化时启动慢速 head 更新；exact verifier 保持采样分布不变。 新版完整 GRPO 多模型实验不复现，审查已完成，现有 mini-suite 的证据等级不变。复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的 RL rollout 加速算子；不把确定性小型评测写成论文完整复现。版本边界（2026-10-15 复核）：本页与 specroll 保留原 v1 的 fast/slow 机制，不代表已经实现 v2 SPARK。v2 改为同一 prompt group 内共享、每轮重置的低秩 logit correction，并由 verifier 反馈更新、跨 rollout 学习投影；不能把旧 adapter 改名就算新版已接入。  RL rollout 加速 LLM 后训练 数据与预算：下一份算力花在哪里 SpecRoll为什么需要快速与慢速两种draft适配？ RL目标策略不断变化，轻量隐状态纠偏应对短期漂移，持续退化才训练future head，避免每次波动都付完整更新成本。两者优化提议而非替换目标策略。 例如一批接受率暂降先快速调整，持续跟不上再更新head。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-specroll-077f92f9" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a2b6bdaeac9dff6c">SpecRoll为什么需要快速与慢速两种draft适配？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aspecroll">SpecRoll: Fast-Slow Verifier-Feedback Adaptation for Speculative Reinforcement Learning Rollouts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · VNU University of Engineering and Technology / Viettel AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>RL目标策略不断变化，轻量隐状态纠偏应对短期漂移，持续退化才训练future head，避免每次波动都付完整更新成本。两者优化提议而非替换目标策略。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一批接受率暂降先快速调整，持续跟不上再更新head。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04962">原论文</a> · <a href="../../../../post-training/2608.04962-specroll/">实现解读</a> · <a href="#qa-a2b6bdaeac9dff6c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:specroll" data-paper-title="SpecRoll: Fast-Slow Verifier-Feedback Adaptation for Speculative Reinforcement Learning Rollouts" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="SpecRoll: Fast-Slow Verifier-Feedback Adaptation for Speculative Reinforcement Learning Rollouts LLM 后训练 VNU University of Engineering and Technology / Viettel AI 2026-08-05 主题：RL rollout 加速。RL 中 target policy 持续变化，静态 drafter 很快过时。SpecRoll 用 future-token heads 提议、Reflex 做无反传的快速隐状态纠偏，并只在持续退化时启动慢速 head 更新；exact verifier 保持采样分布不变。 新版完整 GRPO 多模型实验不复现，审查已完成，现有 mini-suite 的证据等级不变。复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的 RL rollout 加速算子；不把确定性小型评测写成论文完整复现。版本边界（2026-10-15 复核）：本页与 specroll 保留原 v1 的 fast/slow 机制，不代表已经实现 v2 SPARK。v2 改为同一 prompt group 内共享、每轮重置的低秩 logit correction，并由 verifier 反馈更新、跨 rollout 学习投影；不能把旧 adapter 改名就算新版已接入。  RL rollout 加速 LLM 后训练 数据与预算：下一份算力花在哪里 SpecRoll中快速纠偏和慢速草稿头更新，为什么都不能替代精确验证器？ 策略在RL中持续变化，快速隐藏状态纠偏用于及时适应，持续退化时再触发较慢的草稿头训练。二者提高提议质量，精确接受拒绝验证才负责保持目标采样分布。若省略验证，即使草稿看似更准也可能改变RL数据分布；本地没有大模型吞吐结论。 例如草稿头突然跟不上新策略，先修正隐状态再考虑训练；每次提议仍须验证，不能因连续几次猜对就直接当目标策略输出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:specroll" data-paper-title="SpecRoll: Fast-Slow Verifier-Feedback Adaptation for Speculative Reinforcement Learning Rollouts" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="SpecRoll: Fast-Slow Verifier-Feedback Adaptation for Speculative Reinforcement Learning Rollouts LLM 后训练 VNU University of Engineering and Technology / Viettel AI 2026-08-05 主题：RL rollout 加速。RL 中 target policy 持续变化，静态 drafter 很快过时。SpecRoll 用 future-token heads 提议、Reflex 做无反传的快速隐状态纠偏，并只在持续退化时启动慢速 head 更新；exact verifier 保持采样分布不变。 新版完整 GRPO 多模型实验不复现，审查已完成，现有 mini-suite 的证据等级不变。复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的 RL rollout 加速算子；不把确定性小型评测写成论文完整复现。版本边界（2026-10-15 复核）：本页与 specroll 保留原 v1 的 fast/slow 机制，不代表已经实现 v2 SPARK。v2 改为同一 prompt group 内共享、每轮重置的低秩 logit correction，并由 verifier 反馈更新、跨 rollout 学习投影；不能把旧 adapter 改名就算新版已接入。  RL rollout 加速 LLM 后训练 数据与预算：下一份算力花在哪里 SpecRoll改变draft后，GRPO目标也要改成draft目标吗？ 不需要，精确target验证保持采样分布，GRPO本身不变。若省验证直接用草稿，就改变训练数据政策，无法沿用原分布不变说明。 例如草稿常猜对也不能直接把其概率当当前策略概率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7efb0aba37ca861e">SpecRoll改变draft后，GRPO目标也要改成draft目标吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aspecroll">SpecRoll: Fast-Slow Verifier-Feedback Adaptation for Speculative Reinforcement Learning Rollouts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · VNU University of Engineering and Technology / Viettel AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不需要，精确target验证保持采样分布，GRPO本身不变。若省验证直接用草稿，就改变训练数据政策，无法沿用原分布不变说明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如草稿常猜对也不能直接把其概率当当前策略概率。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04962">原论文</a> · <a href="../../../../post-training/2608.04962-specroll/">实现解读</a> · <a href="#qa-7efb0aba37ca861e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:specroll" data-paper-title="SpecRoll: Fast-Slow Verifier-Feedback Adaptation for Speculative Reinforcement Learning Rollouts" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="SpecRoll: Fast-Slow Verifier-Feedback Adaptation for Speculative Reinforcement Learning Rollouts LLM 后训练 VNU University of Engineering and Technology / Viettel AI 2026-08-05 主题：RL rollout 加速。RL 中 target policy 持续变化，静态 drafter 很快过时。SpecRoll 用 future-token heads 提议、Reflex 做无反传的快速隐状态纠偏，并只在持续退化时启动慢速 head 更新；exact verifier 保持采样分布不变。 新版完整 GRPO 多模型实验不复现，审查已完成，现有 mini-suite 的证据等级不变。复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的 RL rollout 加速算子；不把确定性小型评测写成论文完整复现。版本边界（2026-10-15 复核）：本页与 specroll 保留原 v1 的 fast/slow 机制，不代表已经实现 v2 SPARK。v2 改为同一 prompt group 内共享、每轮重置的低秩 logit correction，并由 verifier 反馈更新、跨 rollout 学习投影；不能把旧 adapter 改名就算新版已接入。  RL rollout 加速 LLM 后训练 数据与预算：下一份算力花在哪里 本地SpecRoll注册候选意味着已测大模型RL吞吐吗？ 没有，当前验证状态与选择路径，未运行原文模型和完整环境。实际需核对接受拒绝残差、更新调度及成本，注册发现仅表示可被列出。 例如候选列表出现方法名，不等于控制器已执行其完整GPU训练。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1e3ea16b91f9a1ba">本地SpecRoll注册候选意味着已测大模型RL吞吐吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aspecroll">SpecRoll: Fast-Slow Verifier-Feedback Adaptation for Speculative Reinforcement Learning Rollouts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · VNU University of Engineering and Technology / Viettel AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有，当前验证状态与选择路径，未运行原文模型和完整环境。实际需核对接受拒绝残差、更新调度及成本，注册发现仅表示可被列出。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如候选列表出现方法名，不等于控制器已执行其完整GPU训练。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04962">原论文</a> · <a href="../../../../post-training/2608.04962-specroll/">实现解读</a> · <a href="#qa-1e3ea16b91f9a1ba">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:coba-rl" data-paper-title="CoBA-RL" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="CoBA-RL LLM 后训练 Zhejiang University 2026-06-21 普通 RLVR 可能只重新分配 base model 已有轨迹的概率，提升 pass@1 却不扩展高采样 pass@k 所反映的能力边界。该方法先用多次采样估计边界，在边界附近/之外注入教师推理，再用 RL 巩固。 定位当前能力边界，对边界附近样本提供教师引导，再用 RL 固化新增推理模式。实现了边界状态、难度课程、真实教师触发、自由生成 RL、pass@k/教师缓存与成本曲线；本地 teacher 只有 0.5B，且最高只统计 pass@8，没有运行论文规模 pass@256 或同规模学生，因此不能宣称复现论文中的能力边界增量。本地算术 suite 带可复现难度；训练器维护动态 curriculum boundary、采样边界样本，无正确 rollout 时调用固定 revision 的真实 causal-LM teacher，并把教师 completion 以小权重 SFT 项注入 sequence RL。  能力边界课程 LLM 后训练 数据与预算：下一份算力花在哪里 CoBA-RL为什么用pass@k探测边界再注入教师？ pass@1提高可能只是已有正确路径更常见，高采样覆盖帮助识别尚难达到的题。边界附近教师引导提供新路线，再用RL巩固，目标是兼顾利用与扩展。 例如原来偶尔会的题更稳定，与原来反复采样都不会的题学会，是不同变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-coba-rl-1893eb3e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2bebe79393c05758">CoBA-RL为什么用pass@k探测边界再注入教师？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acoba-rl">CoBA-RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>pass@1提高可能只是已有正确路径更常见，高采样覆盖帮助识别尚难达到的题。边界附近教师引导提供新路线，再用RL巩固，目标是兼顾利用与扩展。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如原来偶尔会的题更稳定，与原来反复采样都不会的题学会，是不同变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.22317">原论文</a> · <a href="../../../../post-training/2606.22317-coba-rl/">实现解读</a> · <a href="#qa-2bebe79393c05758">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:coba-rl" data-paper-title="CoBA-RL" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="CoBA-RL LLM 后训练 Zhejiang University 2026-06-21 普通 RLVR 可能只重新分配 base model 已有轨迹的概率，提升 pass@1 却不扩展高采样 pass@k 所反映的能力边界。该方法先用多次采样估计边界，在边界附近/之外注入教师推理，再用 RL 巩固。 定位当前能力边界，对边界附近样本提供教师引导，再用 RL 固化新增推理模式。实现了边界状态、难度课程、真实教师触发、自由生成 RL、pass@k/教师缓存与成本曲线；本地 teacher 只有 0.5B，且最高只统计 pass@8，没有运行论文规模 pass@256 或同规模学生，因此不能宣称复现论文中的能力边界增量。本地算术 suite 带可复现难度；训练器维护动态 curriculum boundary、采样边界样本，无正确 rollout 时调用固定 revision 的真实 causal-LM teacher，并把教师 completion 以小权重 SFT 项注入 sequence RL。  能力边界课程 LLM 后训练 数据与预算：下一份算力花在哪里 CoBA-RL为什么同时看pass@1与较大采样预算的pass@k来定位能力边界？ 单次成功率提高可能只是把已有正确轨迹变得常见，不一定获得原先完全采不到的新解法。多次采样用于探测边界，再在边界附近引入教师并用RL巩固。有限预算仍可能漏掉稀有解，本地仅到较小的采样规模，不能宣称复现原文高采样边界增量。 例如原来偶尔能解的题变成经常解对，说明利用更好；若想判断是否学会原先从未解出的题，还需更广采样并计入教师成本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:coba-rl" data-paper-title="CoBA-RL" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="CoBA-RL LLM 后训练 Zhejiang University 2026-06-21 普通 RLVR 可能只重新分配 base model 已有轨迹的概率，提升 pass@1 却不扩展高采样 pass@k 所反映的能力边界。该方法先用多次采样估计边界，在边界附近/之外注入教师推理，再用 RL 巩固。 定位当前能力边界，对边界附近样本提供教师引导，再用 RL 固化新增推理模式。实现了边界状态、难度课程、真实教师触发、自由生成 RL、pass@k/教师缓存与成本曲线；本地 teacher 只有 0.5B，且最高只统计 pass@8，没有运行论文规模 pass@256 或同规模学生，因此不能宣称复现论文中的能力边界增量。本地算术 suite 带可复现难度；训练器维护动态 curriculum boundary、采样边界样本，无正确 rollout 时调用固定 revision 的真实 causal-LM teacher，并把教师 completion 以小权重 SFT 项注入 sequence RL。  能力边界课程 LLM 后训练 数据与预算：下一份算力花在哪里 边界课程与按固定题面难度排队有什么区别？ 课程依据当前策略多次采样能力更新，固定题面不随掌握变化。有限k仍可能漏稀有正确路径，所以边界是预算条件估计，不能当绝对不可解证明。 例如模型学会新技巧后，一道长题也可能不再位于边界。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-03ea6cc76d47837a">边界课程与按固定题面难度排队有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acoba-rl">CoBA-RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>课程依据当前策略多次采样能力更新，固定题面不随掌握变化。有限k仍可能漏稀有正确路径，所以边界是预算条件估计，不能当绝对不可解证明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型学会新技巧后，一道长题也可能不再位于边界。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.22317">原论文</a> · <a href="../../../../post-training/2606.22317-coba-rl/">实现解读</a> · <a href="#qa-03ea6cc76d47837a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:coba-rl" data-paper-title="CoBA-RL" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="CoBA-RL LLM 后训练 Zhejiang University 2026-06-21 普通 RLVR 可能只重新分配 base model 已有轨迹的概率，提升 pass@1 却不扩展高采样 pass@k 所反映的能力边界。该方法先用多次采样估计边界，在边界附近/之外注入教师推理，再用 RL 巩固。 定位当前能力边界，对边界附近样本提供教师引导，再用 RL 固化新增推理模式。实现了边界状态、难度课程、真实教师触发、自由生成 RL、pass@k/教师缓存与成本曲线；本地 teacher 只有 0.5B，且最高只统计 pass@8，没有运行论文规模 pass@256 或同规模学生，因此不能宣称复现论文中的能力边界增量。本地算术 suite 带可复现难度；训练器维护动态 curriculum boundary、采样边界样本，无正确 rollout 时调用固定 revision 的真实 causal-LM teacher，并把教师 completion 以小权重 SFT 项注入 sequence RL。  能力边界课程 LLM 后训练 数据与预算：下一份算力花在哪里 CoBA本地pass@8能否证明论文pass@256边界增量？ 不能，教师规模、学生规模与采样预算不同。当前有真实生成、触发与成本曲线，但只支持缩小配置的机制证据，不能把较小k直接换标签当原规模。 例如八次未成功不等于二百多次也不会成功，统计覆盖不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-9daf279970f9b21e">CoBA本地pass@8能否证明论文pass@256边界增量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acoba-rl">CoBA-RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，教师规模、学生规模与采样预算不同。当前有真实生成、触发与成本曲线，但只支持缩小配置的机制证据，不能把较小k直接换标签当原规模。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如八次未成功不等于二百多次也不会成功，统计覆盖不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.22317">原论文</a> · <a href="../../../../post-training/2606.22317-coba-rl/">实现解读</a> · <a href="#qa-9daf279970f9b21e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sparse-to-dense-reward-principle" data-paper-title="Beyond GRPO and On-Policy Distillation: An Empirical Sparse-to-Dense Reward Principle for Language-Model Post-Training" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Beyond GRPO and On-Policy Distillation: An Empirical Sparse-to-Dense Reward Principle for Language-Model Post-Training LLM 后训练 LinkedIn 2026-05-12 Sec.2–3四阶段工作流和等标签预算经验对照是本论文核心；FKL在teacher occupancy、OPD在student occupancy，教师冻结且需共享tokenizer。库中已有GRPO/OPD/KL算子不等于本文完整流程；不重复包装通用KL或把四个状态标签称为复现。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。状态：仅文献与成本收录，没有可执行能力adapter，不以heuristic冒充核心模型。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本轮不提供可运行模型、loss包装或伪测试。库里已有通用KL/RL/统计工具并不构成本文核心流程；原文语义模型、API多轮生成或大规模训练不能用手工规则替换。仅保存经过核验的方法、资源、源码状态与原图，终态为 not_reproduced_high_cost。后续不得自动移回待训练队列。  训练流程与资源分配 Teacher RL与FKL-to-OPD LLM 后训练 数据与预算：下一份算力花在哪里 稀疏到稠密原则论文为何重视等标签预算的阶段实验？ 稠密教师信号通常花费不同监督成本，只有把标签预算与阶段流程对齐，才能理解哪些顺序有效。论文贡献不是另一个通用KL函数，而是四阶段经验比较。 例如额外调用更多教师得到提高，不能都归因于目标从稀疏变稠密。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-sparse-to-dense-reward-principle-66732323" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-dbea5a3e23945c93">稀疏到稠密原则论文为何重视等标签预算的阶段实验？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asparse-to-dense-reward-principle">Beyond GRPO and On-Policy Distillation: An Empirical Sparse-to-Dense Reward Principle for Language-Model Post-Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>稠密教师信号通常花费不同监督成本，只有把标签预算与阶段流程对齐，才能理解哪些顺序有效。论文贡献不是另一个通用KL函数，而是四阶段经验比较。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如额外调用更多教师得到提高，不能都归因于目标从稀疏变稠密。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.12483v1">原论文</a> · <a href="../../../../post-training/2605.12483-sparse-to-dense-reward-principle/">实现解读</a> · <a href="#qa-dbea5a3e23945c93">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sparse-to-dense-reward-principle" data-paper-title="Beyond GRPO and On-Policy Distillation: An Empirical Sparse-to-Dense Reward Principle for Language-Model Post-Training" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Beyond GRPO and On-Policy Distillation: An Empirical Sparse-to-Dense Reward Principle for Language-Model Post-Training LLM 后训练 LinkedIn 2026-05-12 Sec.2–3四阶段工作流和等标签预算经验对照是本论文核心；FKL在teacher occupancy、OPD在student occupancy，教师冻结且需共享tokenizer。库中已有GRPO/OPD/KL算子不等于本文完整流程；不重复包装通用KL或把四个状态标签称为复现。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。状态：仅文献与成本收录，没有可执行能力adapter，不以heuristic冒充核心模型。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本轮不提供可运行模型、loss包装或伪测试。库里已有通用KL/RL/统计工具并不构成本文核心流程；原文语义模型、API多轮生成或大规模训练不能用手工规则替换。仅保存经过核验的方法、资源、源码状态与原图，终态为 not_reproduced_high_cost。后续不得自动移回待训练队列。  训练流程与资源分配 Teacher RL与FKL-to-OPD LLM 后训练 数据与预算：下一份算力花在哪里 稀疏到稠密奖励原则为什么不仅是把GRPO与KL算子按顺序调用？ 论文核心是四阶段流程及相同标签预算下的经验对照，还区分教师访问状态上的正向KL与学生访问状态上的逆向KL。散度方向和状态来源共同决定训练信号，只有几个通用算子或阶段标签不能构成复现。本地目前文献收录，未执行完整训练流程。 例如同样写着KL损失，在教师标准解的前缀计算与在学生错误前缀计算，监督对象不同；不能仅因公式名字相同就合并成一个阶段。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sparse-to-dense-reward-principle" data-paper-title="Beyond GRPO and On-Policy Distillation: An Empirical Sparse-to-Dense Reward Principle for Language-Model Post-Training" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Beyond GRPO and On-Policy Distillation: An Empirical Sparse-to-Dense Reward Principle for Language-Model Post-Training LLM 后训练 LinkedIn 2026-05-12 Sec.2–3四阶段工作流和等标签预算经验对照是本论文核心；FKL在teacher occupancy、OPD在student occupancy，教师冻结且需共享tokenizer。库中已有GRPO/OPD/KL算子不等于本文完整流程；不重复包装通用KL或把四个状态标签称为复现。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。状态：仅文献与成本收录，没有可执行能力adapter，不以heuristic冒充核心模型。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本轮不提供可运行模型、loss包装或伪测试。库里已有通用KL/RL/统计工具并不构成本文核心流程；原文语义模型、API多轮生成或大规模训练不能用手工规则替换。仅保存经过核验的方法、资源、源码状态与原图，终态为 not_reproduced_high_cost。后续不得自动移回待训练队列。  训练流程与资源分配 Teacher RL与FKL-to-OPD LLM 后训练 数据与预算：下一份算力花在哪里 相同KL方向在teacher occupancy与student occupancy上等价吗？ 不等价，状态访问决定监督覆盖；教师理想前缀与学生实际前缀包含不同错误。方向与occupancy必须一起说明，不能只列KL符号便判同一训练。 例如同一损失在正确证明与错误中间式上，教会的修复行为不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d26c9a44ab00a9cf">相同KL方向在teacher occupancy与student occupancy上等价吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asparse-to-dense-reward-principle">Beyond GRPO and On-Policy Distillation: An Empirical Sparse-to-Dense Reward Principle for Language-Model Post-Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不等价，状态访问决定监督覆盖；教师理想前缀与学生实际前缀包含不同错误。方向与occupancy必须一起说明，不能只列KL符号便判同一训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一损失在正确证明与错误中间式上，教会的修复行为不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.12483v1">原论文</a> · <a href="../../../../post-training/2605.12483-sparse-to-dense-reward-principle/">实现解读</a> · <a href="#qa-d26c9a44ab00a9cf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sparse-to-dense-reward-principle" data-paper-title="Beyond GRPO and On-Policy Distillation: An Empirical Sparse-to-Dense Reward Principle for Language-Model Post-Training" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Beyond GRPO and On-Policy Distillation: An Empirical Sparse-to-Dense Reward Principle for Language-Model Post-Training LLM 后训练 LinkedIn 2026-05-12 Sec.2–3四阶段工作流和等标签预算经验对照是本论文核心；FKL在teacher occupancy、OPD在student occupancy，教师冻结且需共享tokenizer。库中已有GRPO/OPD/KL算子不等于本文完整流程；不重复包装通用KL或把四个状态标签称为复现。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。状态：仅文献与成本收录，没有可执行能力adapter，不以heuristic冒充核心模型。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本轮不提供可运行模型、loss包装或伪测试。库里已有通用KL/RL/统计工具并不构成本文核心流程；原文语义模型、API多轮生成或大规模训练不能用手工规则替换。仅保存经过核验的方法、资源、源码状态与原图，终态为 not_reproduced_high_cost。后续不得自动移回待训练队列。  训练流程与资源分配 Teacher RL与FKL-to-OPD LLM 后训练 数据与预算：下一份算力花在哪里 库里已有GRPO和OPD算子是否算完整四阶段复现？ 不算，当前仅文献收录，没有完整阶段调度、真实冻结教师及等预算实验。共享tokenizer等前提也需满足，四个状态标签不代表实际训练链路。 例如把配置阶段写齐但未运行数据流，不能报告流程已验证。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8d9196ac9cfedb73">库里已有GRPO和OPD算子是否算完整四阶段复现？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asparse-to-dense-reward-principle">Beyond GRPO and On-Policy Distillation: An Empirical Sparse-to-Dense Reward Principle for Language-Model Post-Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不算，当前仅文献收录，没有完整阶段调度、真实冻结教师及等预算实验。共享tokenizer等前提也需满足，四个状态标签不代表实际训练链路。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把配置阶段写齐但未运行数据流，不能报告流程已验证。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.12483v1">原论文</a> · <a href="../../../../post-training/2605.12483-sparse-to-dense-reward-principle/">实现解读</a> · <a href="#qa-8d9196ac9cfedb73">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:lightning-opd" data-paper-title="Lightning OPD" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Lightning OPD LLM 后训练 MIT HAN Lab 2026-04-14 传统在线蒸馏在每一步训练都调用教师，吞吐和成本受教师推理限制。Lightning OPD 先让学生在 SFT 数据上产生 on-policy rollout，再由同一个教师一次性计算 token 分布并缓存。训练只读取缓存，因此保留学生分布上的蒸馏信号，又不需要训练期在线教师。 保真度：本地实现复现教师预填充、teacher consistency 和训练期零在线教师调用；保真度：本地实现复现教师预填充、teacher consistency 和训练期零在线教师调用；当前使用候选策略验证机制，不等同于论文的 Qwen3 全参数训练。当前没有训练真实 Qwen3、token-level vocabulary distribution 或复跑 AIME；因此只能证明缓存式 OPD 数据流和教师调用约束成立，不能把本地 accuracy 与论文 AIME 数字比较。实现先为全部训练候选缓存教师概率，保存 teacher_prefill_calls 和 teacher_cache_entries；  On-policy distillation LLM 后训练 数据与预算：下一份算力花在哪里 Lightning OPD为什么把教师打分移到训练前缓存？ 教师在线推理可能成为瓶颈，先对学生生成轨迹一次评分，训练反复读标签，减少持续教师调用。成本被前置，不代表初次打分或学生生成免费。 例如先备好每个前缀的教师分数，再在多次更新时重复使用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-lightning-opd-b1670874" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a0e66c15fe51a1fd">Lightning OPD为什么把教师打分移到训练前缓存？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Alightning-opd">Lightning OPD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · MIT HAN Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>教师在线推理可能成为瓶颈，先对学生生成轨迹一次评分，训练反复读标签，减少持续教师调用。成本被前置，不代表初次打分或学生生成免费。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先备好每个前缀的教师分数，再在多次更新时重复使用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.13010">原论文</a> · <a href="../../../../post-training/2604.13010-lightning-opd/">实现解读</a> · <a href="#qa-a0e66c15fe51a1fd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:lightning-opd" data-paper-title="Lightning OPD" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Lightning OPD LLM 后训练 MIT HAN Lab 2026-04-14 传统在线蒸馏在每一步训练都调用教师，吞吐和成本受教师推理限制。Lightning OPD 先让学生在 SFT 数据上产生 on-policy rollout，再由同一个教师一次性计算 token 分布并缓存。训练只读取缓存，因此保留学生分布上的蒸馏信号，又不需要训练期在线教师。 保真度：本地实现复现教师预填充、teacher consistency 和训练期零在线教师调用；保真度：本地实现复现教师预填充、teacher consistency 和训练期零在线教师调用；当前使用候选策略验证机制，不等同于论文的 Qwen3 全参数训练。当前没有训练真实 Qwen3、token-level vocabulary distribution 或复跑 AIME；因此只能证明缓存式 OPD 数据流和教师调用约束成立，不能把本地 accuracy 与论文 AIME 数字比较。实现先为全部训练候选缓存教师概率，保存 teacher_prefill_calls 和 teacher_cache_entries；  On-policy distillation LLM 后训练 数据与预算：下一份算力花在哪里 Lightning OPD缓存的是学生轨迹上的教师评分，为什么不能等同持续更新的在线教师蒸馏？ 先由学生采样、再用一致教师配置打分，可一次付出教师成本，后续训练读取缓存。标签最初位于学生分布，但学生更新后访问状态会变化，旧缓存不会自动覆盖新状态。因而成本收益与缓存覆盖、教师一致性有关，本地只验证数据流，没有真实词表蒸馏成绩。 例如学生初期常犯某类错误，缓存能教这些前缀；当学生后来走出新解法，旧缓存不会自动补上新前缀，需要另行定义刷新协议。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:lightning-opd" data-paper-title="Lightning OPD" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Lightning OPD LLM 后训练 MIT HAN Lab 2026-04-14 传统在线蒸馏在每一步训练都调用教师，吞吐和成本受教师推理限制。Lightning OPD 先让学生在 SFT 数据上产生 on-policy rollout，再由同一个教师一次性计算 token 分布并缓存。训练只读取缓存，因此保留学生分布上的蒸馏信号，又不需要训练期在线教师。 保真度：本地实现复现教师预填充、teacher consistency 和训练期零在线教师调用；保真度：本地实现复现教师预填充、teacher consistency 和训练期零在线教师调用；当前使用候选策略验证机制，不等同于论文的 Qwen3 全参数训练。当前没有训练真实 Qwen3、token-level vocabulary distribution 或复跑 AIME；因此只能证明缓存式 OPD 数据流和教师调用约束成立，不能把本地 accuracy 与论文 AIME 数字比较。实现先为全部训练候选缓存教师概率，保存 teacher_prefill_calls 和 teacher_cache_entries；  On-policy distillation LLM 后训练 数据与预算：下一份算力花在哪里 离线教师缓存与每步刷新学生轨迹的OPD有何覆盖差？ 缓存保留初始学生访问状态，当前学生更新后可能走新状态，在线刷新能覆盖这些变化但更贵。两者是覆盖和成本取舍，不可称缓存永远保持当前on-policy。 例如学生新学到另一解法，旧缓存并没有自动获得其前缀标签。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4833bd93af00c6b0">离线教师缓存与每步刷新学生轨迹的OPD有何覆盖差？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Alightning-opd">Lightning OPD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · MIT HAN Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>缓存保留初始学生访问状态，当前学生更新后可能走新状态，在线刷新能覆盖这些变化但更贵。两者是覆盖和成本取舍，不可称缓存永远保持当前on-policy。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生新学到另一解法，旧缓存并没有自动获得其前缀标签。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.13010">原论文</a> · <a href="../../../../post-training/2604.13010-lightning-opd/">实现解读</a> · <a href="#qa-4833bd93af00c6b0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:lightning-opd" data-paper-title="Lightning OPD" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Lightning OPD LLM 后训练 MIT HAN Lab 2026-04-14 传统在线蒸馏在每一步训练都调用教师，吞吐和成本受教师推理限制。Lightning OPD 先让学生在 SFT 数据上产生 on-policy rollout，再由同一个教师一次性计算 token 分布并缓存。训练只读取缓存，因此保留学生分布上的蒸馏信号，又不需要训练期在线教师。 保真度：本地实现复现教师预填充、teacher consistency 和训练期零在线教师调用；保真度：本地实现复现教师预填充、teacher consistency 和训练期零在线教师调用；当前使用候选策略验证机制，不等同于论文的 Qwen3 全参数训练。当前没有训练真实 Qwen3、token-level vocabulary distribution 或复跑 AIME；因此只能证明缓存式 OPD 数据流和教师调用约束成立，不能把本地 accuracy 与论文 AIME 数字比较。实现先为全部训练候选缓存教师概率，保存 teacher_prefill_calls 和 teacher_cache_entries；  On-policy distillation LLM 后训练 数据与预算：下一份算力花在哪里 Lightning缓存应核对哪些身份以避免teacher mismatch？ 教师检查点、提示、tokenizer、响应内容与位置mask需一致，修改文本或教师配置后不能沿用旧标签。当前本地只有缓存数据流，未跑真实Qwen词表蒸馏和AIME。 例如分词器升级后旧位置logp可能错位，不能仅因文件名相同继续读。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8dddd41106ab3d2b">Lightning缓存应核对哪些身份以避免teacher mismatch？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Alightning-opd">Lightning OPD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · MIT HAN Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>教师检查点、提示、tokenizer、响应内容与位置mask需一致，修改文本或教师配置后不能沿用旧标签。当前本地只有缓存数据流，未跑真实Qwen词表蒸馏和AIME。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如分词器升级后旧位置logp可能错位，不能仅因文件名相同继续读。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.13010">原论文</a> · <a href="../../../../post-training/2604.13010-lightning-opd/">实现解读</a> · <a href="#qa-8dddd41106ab3d2b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cross-script-knowledge-transfer" data-paper-title="Large Reasoning Models Struggle to Transfer Parametric Knowledge Across Scripts" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Large Reasoning Models Struggle to Transfer Parametric Knowledge Across Scripts LLM 后训练 Google Research 2026-03-17 Sec.4–6与Appendix A/H：观察性回归、训练专用entity提示干预和真实LoRA是定义性路径。不能把正则音译、手工插提示或小分类器当成其LLM知识检索机制。本文不是新闭式RL loss；本轮仅文献收录，不强造operator。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。状态：仅文献与成本收录，没有可执行能力adapter，不以heuristic冒充核心模型。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本轮不提供可运行模型、loss包装或伪测试。库里已有通用KL/RL/统计工具并不构成本文核心流程；原文语义模型、API多轮生成或大规模训练不能用手工规则替换。仅保存经过核验的方法、资源、源码状态与原图，终态为 not_reproduced_high_cost。后续不得自动移回待训练队列。  多语言后训练 跨文字系统知识迁移 LLM 后训练 数据与预算：下一份算力花在哪里 跨文字系统知识研究为什么不只考查翻译质量？ 同一事实用另一套文字表示时，失败可能来自实体识别、参数知识检索或推理表达，翻译只是其中一环。研究用回归和干预拆分因素，不能直接当新RL算法。 例如一个人名转成另一文字后答错，不一定是从未学过这个人的事实。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-cross-script-knowledge-transfer-cff708b0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-21884a7e420cd1b2">跨文字系统知识研究为什么不只考查翻译质量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Across-script-knowledge-transfer">Large Reasoning Models Struggle to Transfer Parametric Knowledge Across Scripts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一事实用另一套文字表示时，失败可能来自实体识别、参数知识检索或推理表达，翻译只是其中一环。研究用回归和干预拆分因素，不能直接当新RL算法。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个人名转成另一文字后答错，不一定是从未学过这个人的事实。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.17070v1">原论文</a> · <a href="../../../../post-training/2603.17070-cross-script-knowledge-transfer/">实现解读</a> · <a href="#qa-21884a7e420cd1b2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cross-script-knowledge-transfer" data-paper-title="Large Reasoning Models Struggle to Transfer Parametric Knowledge Across Scripts" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Large Reasoning Models Struggle to Transfer Parametric Knowledge Across Scripts LLM 后训练 Google Research 2026-03-17 Sec.4–6与Appendix A/H：观察性回归、训练专用entity提示干预和真实LoRA是定义性路径。不能把正则音译、手工插提示或小分类器当成其LLM知识检索机制。本文不是新闭式RL loss；本轮仅文献收录，不强造operator。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。状态：仅文献与成本收录，没有可执行能力adapter，不以heuristic冒充核心模型。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本轮不提供可运行模型、loss包装或伪测试。库里已有通用KL/RL/统计工具并不构成本文核心流程；原文语义模型、API多轮生成或大规模训练不能用手工规则替换。仅保存经过核验的方法、资源、源码状态与原图，终态为 not_reproduced_high_cost。后续不得自动移回待训练队列。  多语言后训练 跨文字系统知识迁移 LLM 后训练 数据与预算：下一份算力花在哪里 跨文字系统知识迁移为何不能只靠把问题机械音译来判断模型是否拥有知识？ 文字系统变化会同时影响实体识别、参数知识检索与推理表达，仅比较音译前后答案难以定位原因。论文结合观察回归、训练期实体提示干预和真实LoRA来拆分这些因素。提示或正则替换只是条件改变，本地文献收录没有实现语言模型知识检索能力。 例如同一地名改用另一种文字后回答失败，可能是实体没对齐而非事实从未学过；加提示能帮助诊断，却不能当成迁移训练已经完成。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cross-script-knowledge-transfer" data-paper-title="Large Reasoning Models Struggle to Transfer Parametric Knowledge Across Scripts" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Large Reasoning Models Struggle to Transfer Parametric Knowledge Across Scripts LLM 后训练 Google Research 2026-03-17 Sec.4–6与Appendix A/H：观察性回归、训练专用entity提示干预和真实LoRA是定义性路径。不能把正则音译、手工插提示或小分类器当成其LLM知识检索机制。本文不是新闭式RL loss；本轮仅文献收录，不强造operator。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。状态：仅文献与成本收录，没有可执行能力adapter，不以heuristic冒充核心模型。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本轮不提供可运行模型、loss包装或伪测试。库里已有通用KL/RL/统计工具并不构成本文核心流程；原文语义模型、API多轮生成或大规模训练不能用手工规则替换。仅保存经过核验的方法、资源、源码状态与原图，终态为 not_reproduced_high_cost。后续不得自动移回待训练队列。  多语言后训练 跨文字系统知识迁移 LLM 后训练 数据与预算：下一份算力花在哪里 训练期entity提示干预与推理时手工音译能相互替代吗？ 不能，前者用于研究检索与学习路径，后者只改当前输入，可能绕过困难。真实LoRA与语义风格迁移也不能由正则替换或小分类器冒充。 例如把名字统一转回熟悉写法能帮助答题，却未证明模型学会跨文字迁移。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e434884eee2a2d72">训练期entity提示干预与推理时手工音译能相互替代吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Across-script-knowledge-transfer">Large Reasoning Models Struggle to Transfer Parametric Knowledge Across Scripts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，前者用于研究检索与学习路径，后者只改当前输入，可能绕过困难。真实LoRA与语义风格迁移也不能由正则替换或小分类器冒充。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把名字统一转回熟悉写法能帮助答题，却未证明模型学会跨文字迁移。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.17070v1">原论文</a> · <a href="../../../../post-training/2603.17070-cross-script-knowledge-transfer/">实现解读</a> · <a href="#qa-e434884eee2a2d72">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:cross-script-knowledge-transfer" data-paper-title="Large Reasoning Models Struggle to Transfer Parametric Knowledge Across Scripts" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Large Reasoning Models Struggle to Transfer Parametric Knowledge Across Scripts LLM 后训练 Google Research 2026-03-17 Sec.4–6与Appendix A/H：观察性回归、训练专用entity提示干预和真实LoRA是定义性路径。不能把正则音译、手工插提示或小分类器当成其LLM知识检索机制。本文不是新闭式RL loss；本轮仅文献收录，不强造operator。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。状态：仅文献与成本收录，没有可执行能力adapter，不以heuristic冒充核心模型。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本轮不提供可运行模型、loss包装或伪测试。库里已有通用KL/RL/统计工具并不构成本文核心流程；原文语义模型、API多轮生成或大规模训练不能用手工规则替换。仅保存经过核验的方法、资源、源码状态与原图，终态为 not_reproduced_high_cost。后续不得自动移回待训练队列。  多语言后训练 跨文字系统知识迁移 LLM 后训练 数据与预算：下一份算力花在哪里 本地这篇是否存在可执行知识迁移operator？ 当前仅收录文献，未实现所需真实语言模型语义模块及LoRA训练。公式是方法解释，不能借通用SFT接口就声明已复现，也不以测试答案构造训练提示。 例如一个音译函数能运行，不意味着论文的参数知识检索机制已接入。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0480a7b8e8e475bc">本地这篇是否存在可执行知识迁移operator？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Across-script-knowledge-transfer">Large Reasoning Models Struggle to Transfer Parametric Knowledge Across Scripts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>当前仅收录文献，未实现所需真实语言模型语义模块及LoRA训练。公式是方法解释，不能借通用SFT接口就声明已复现，也不以测试答案构造训练提示。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个音译函数能运行，不意味着论文的参数知识检索机制已接入。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.17070v1">原论文</a> · <a href="../../../../post-training/2603.17070-cross-script-knowledge-transfer/">实现解读</a> · <a href="#qa-0480a7b8e8e475bc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:prompt-level-distillation" data-paper-title="Prompt-Level Distillation: A Non-Parametric Alternative to Model Fine-Tuning for Efficient Reasoning" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Prompt-Level Distillation: A Non-Parametric Alternative to Model Fine-Tuning for Efficient Reasoning LLM 后训练 Google 2026-02-24 PLD 不微调学生参数，而把教师推理抽象为可审查的系统指令：先用带标签训练样本提取微规则，经语义向量 DBSCAN 去掉噪声、合成规则，再根据训练错误修订冲突。学生最终使用整理后的规则，不读取每个测试样本的答案。图按原文 Figure 1 重绘。原始流程图。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。§4.1 使用 Gemini 3 Flash thinking 提取、Gemini 3 Pro thinking 合成和修复、Gemini Embedding 聚类，学生含 Gemma-3 4B / Gemini 2 Flash。多阶段闭源调用与完整多任务评测成本无法廉价固定，成本过高，不复现（审查 DONE），不下载模型探成本。  Context distillation 提示级非参数蒸馏 LLM 后训练 数据与预算：下一份算力花在哪里 PLD不微调参数，知识最终存在哪里？ 存于教师抽象、聚类和修订得到的可读系统规则，学生推理时读取冻结指令。规则是学习产物，参数不变不表示没有训练数据依赖。 例如把常见日期处理经验编成几条指令，部署时作为学生系统提示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-prompt-level-distillation-91a64214" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e2a7d297d28d0a8c">PLD不微调参数，知识最终存在哪里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aprompt-level-distillation">Prompt-Level Distillation: A Non-Parametric Alternative to Model Fine-Tuning for Efficient Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>存于教师抽象、聚类和修订得到的可读系统规则，学生推理时读取冻结指令。规则是学习产物，参数不变不表示没有训练数据依赖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把常见日期处理经验编成几条指令，部署时作为学生系统提示。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与数据协议；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.21103v1">原论文</a> · <a href="../../../../post-training/2602.21103-prompt-level-distillation/">实现解读</a> · <a href="#qa-e2a7d297d28d0a8c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:prompt-level-distillation" data-paper-title="Prompt-Level Distillation: A Non-Parametric Alternative to Model Fine-Tuning for Efficient Reasoning" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Prompt-Level Distillation: A Non-Parametric Alternative to Model Fine-Tuning for Efficient Reasoning LLM 后训练 Google 2026-02-24 PLD 不微调学生参数，而把教师推理抽象为可审查的系统指令：先用带标签训练样本提取微规则，经语义向量 DBSCAN 去掉噪声、合成规则，再根据训练错误修订冲突。学生最终使用整理后的规则，不读取每个测试样本的答案。图按原文 Figure 1 重绘。原始流程图。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。§4.1 使用 Gemini 3 Flash thinking 提取、Gemini 3 Pro thinking 合成和修复、Gemini Embedding 聚类，学生含 Gemma-3 4B / Gemini 2 Flash。多阶段闭源调用与完整多任务评测成本无法廉价固定，成本过高，不复现（审查 DONE），不下载模型探成本。  Context distillation 提示级非参数蒸馏 LLM 后训练 数据与预算：下一份算力花在哪里 PLD不更新学生参数，为什么还要训练、验证与测试严格分离？ 教师从带标签训练样本提取规则，经语义聚类与错误对照修订后，规则本身就承载了学习结果。验证集可判断规则是否收敛，测试时必须冻结规则，不能依据测试答案继续修补。参数不变并不消除泄漏风险；它把教师推理编译为可读指令而非微调权重。 例如训练中提炼日期归一化规则，验证后固定为系统指令；看到测试标准日期再添加特例，即使没有梯度更新也已使用测试标签。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:prompt-level-distillation" data-paper-title="Prompt-Level Distillation: A Non-Parametric Alternative to Model Fine-Tuning for Efficient Reasoning" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Prompt-Level Distillation: A Non-Parametric Alternative to Model Fine-Tuning for Efficient Reasoning LLM 后训练 Google 2026-02-24 PLD 不微调学生参数，而把教师推理抽象为可审查的系统指令：先用带标签训练样本提取微规则，经语义向量 DBSCAN 去掉噪声、合成规则，再根据训练错误修订冲突。学生最终使用整理后的规则，不读取每个测试样本的答案。图按原文 Figure 1 重绘。原始流程图。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。§4.1 使用 Gemini 3 Flash thinking 提取、Gemini 3 Pro thinking 合成和修复、Gemini Embedding 聚类，学生含 Gemma-3 4B / Gemini 2 Flash。多阶段闭源调用与完整多任务评测成本无法廉价固定，成本过高，不复现（审查 DONE），不下载模型探成本。  Context distillation 提示级非参数蒸馏 LLM 后训练 数据与预算：下一份算力花在哪里 PLD语义DBSCAN与简单把相同句子去重有什么不同？ 语义聚类可把不同措辞的同类微规则聚合并去噪，字符去重只识别字面相同。规则冲突还要根据训练错误修订，不能由字符串列表自动保证一致。 例如两条不同表达的单位换算规则应可能属于同一语义簇。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d97c7cd044405c08">PLD语义DBSCAN与简单把相同句子去重有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aprompt-level-distillation">Prompt-Level Distillation: A Non-Parametric Alternative to Model Fine-Tuning for Efficient Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语义聚类可把不同措辞的同类微规则聚合并去噪，字符去重只识别字面相同。规则冲突还要根据训练错误修订，不能由字符串列表自动保证一致。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两条不同表达的单位换算规则应可能属于同一语义簇。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与数据协议；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.21103v1">原论文</a> · <a href="../../../../post-training/2602.21103-prompt-level-distillation/">实现解读</a> · <a href="#qa-d97c7cd044405c08">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:prompt-level-distillation" data-paper-title="Prompt-Level Distillation: A Non-Parametric Alternative to Model Fine-Tuning for Efficient Reasoning" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Prompt-Level Distillation: A Non-Parametric Alternative to Model Fine-Tuning for Efficient Reasoning LLM 后训练 Google 2026-02-24 PLD 不微调学生参数，而把教师推理抽象为可审查的系统指令：先用带标签训练样本提取微规则，经语义向量 DBSCAN 去掉噪声、合成规则，再根据训练错误修订冲突。学生最终使用整理后的规则，不读取每个测试样本的答案。图按原文 Figure 1 重绘。原始流程图。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。§4.1 使用 Gemini 3 Flash thinking 提取、Gemini 3 Pro thinking 合成和修复、Gemini Embedding 聚类，学生含 Gemma-3 4B / Gemini 2 Flash。多阶段闭源调用与完整多任务评测成本无法廉价固定，成本过高，不复现（审查 DONE），不下载模型探成本。  Context distillation 提示级非参数蒸馏 LLM 后训练 数据与预算：下一份算力花在哪里 PLD的规则什么时候冻结，测试反馈能继续修订吗？ 用训练样本提规则和纠错，验证判断收敛后冻结，测试不再依据标准答案改规则。未更新权重仍可能泄漏，因此提示版本与来源应可追踪。 例如看完测试日期错例后加特例，再重报测试分，就不再是独立评估。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-fa6ed62dc42efca1">PLD的规则什么时候冻结，测试反馈能继续修订吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aprompt-level-distillation">Prompt-Level Distillation: A Non-Parametric Alternative to Model Fine-Tuning for Efficient Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用训练样本提规则和纠错，验证判断收敛后冻结，测试不再依据标准答案改规则。未更新权重仍可能泄漏，因此提示版本与来源应可追踪。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如看完测试日期错例后加特例，再重报测试分，就不再是独立评估。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与数据协议；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.21103v1">原论文</a> · <a href="../../../../post-training/2602.21103-prompt-level-distillation/">实现解读</a> · <a href="#qa-fa6ed62dc42efca1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:chord" data-paper-title="CHORD" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="CHORD LLM 后训练 Alibaba Group 2025-08-15 将 SFT 与 RL 串成两个独立阶段会造成 expert data 的过拟合或过早遗忘。CHORD 把专家 SFT 作为 on-policy RL 中动态退火的辅助目标，并以 token 级不确定性权重平滑从模仿过渡到探索。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地不训练 LLM token-level uncertainty model，gold candidate 仅是确定性 expert 代理。把 verified gold candidate 作为 expert trace，真实按训练进度退火 SFT 项并与 on-policy group-RL 梯度相加。  SFT-RL 动态混合 LLM 后训练 数据与预算：下一份算力花在哪里 CHORD为什么让SFT辅助项在RL中逐渐退火？ 早期专家示范提供稳定方向，后期过强模仿可能限制探索。动态权重和词元不确定性使两种信号平滑交接，避免阶段突然切换带来的过拟合或遗忘。 例如一开始多学标准步骤，熟练后让任务奖励有更多决定权。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-chord-f1e12f5e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-69baa45da687fd7d">CHORD为什么让SFT辅助项在RL中逐渐退火？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Achord">CHORD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>早期专家示范提供稳定方向，后期过强模仿可能限制探索。动态权重和词元不确定性使两种信号平滑交接，避免阶段突然切换带来的过拟合或遗忘。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一开始多学标准步骤，熟练后让任务奖励有更多决定权。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.11408">原论文</a> · <a href="../../../../post-training/2508.11408-chord/">实现解读</a> · <a href="#qa-69baa45da687fd7d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:chord" data-paper-title="CHORD" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="CHORD LLM 后训练 Alibaba Group 2025-08-15 将 SFT 与 RL 串成两个独立阶段会造成 expert data 的过拟合或过早遗忘。CHORD 把专家 SFT 作为 on-policy RL 中动态退火的辅助目标，并以 token 级不确定性权重平滑从模仿过渡到探索。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地不训练 LLM token-level uncertainty model，gold candidate 仅是确定性 expert 代理。把 verified gold candidate 作为 expert trace，真实按训练进度退火 SFT 项并与 on-policy group-RL 梯度相加。  SFT-RL 动态混合 LLM 后训练 数据与预算：下一份算力花在哪里 CHORD为什么在RL过程中逐渐减小专家监督，而不一次性切掉SFT？ 专家数据可在探索初期提供稳定方向，但长期过强模仿会限制新策略；动态退火结合词元不确定性权重，让监督与探索平滑交接。它仍需控制专家与当前策略的分布差异，不保证混合必然优于分阶段。本地专家候选只是代理，未训练词元不确定性模型。 例如学生开始解题时保留教师步骤指导，逐渐熟练后更多依靠任务奖励；不是到某一步突然完全忘掉专家，也不是始终固定等权。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:chord" data-paper-title="CHORD" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="CHORD LLM 后训练 Alibaba Group 2025-08-15 将 SFT 与 RL 串成两个独立阶段会造成 expert data 的过拟合或过早遗忘。CHORD 把专家 SFT 作为 on-policy RL 中动态退火的辅助目标，并以 token 级不确定性权重平滑从模仿过渡到探索。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地不训练 LLM token-level uncertainty model，gold candidate 仅是确定性 expert 代理。把 verified gold candidate 作为 expert trace，真实按训练进度退火 SFT 项并与 on-policy group-RL 梯度相加。  SFT-RL 动态混合 LLM 后训练 数据与预算：下一份算力花在哪里 CHORD与PIVOT按问题切换是否同一机制？ CHORD混合目标并退火辅助监督，PIVOT按教师困惑度把问题路由到不同目标。作用粒度和调度依据不同，不能只因都从模仿走向RL就视为等价。 例如一法同题可同时承受两项，一法按规则选择该题走哪条分支。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-de0dc149fb4ad21f">CHORD与PIVOT按问题切换是否同一机制？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Achord">CHORD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>CHORD混合目标并退火辅助监督，PIVOT按教师困惑度把问题路由到不同目标。作用粒度和调度依据不同，不能只因都从模仿走向RL就视为等价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一法同题可同时承受两项，一法按规则选择该题走哪条分支。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.11408">原论文</a> · <a href="../../../../post-training/2508.11408-chord/">实现解读</a> · <a href="#qa-de0dc149fb4ad21f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:chord" data-paper-title="CHORD" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="CHORD LLM 后训练 Alibaba Group 2025-08-15 将 SFT 与 RL 串成两个独立阶段会造成 expert data 的过拟合或过早遗忘。CHORD 把专家 SFT 作为 on-policy RL 中动态退火的辅助目标，并以 token 级不确定性权重平滑从模仿过渡到探索。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地不训练 LLM token-level uncertainty model，gold candidate 仅是确定性 expert 代理。把 verified gold candidate 作为 expert trace，真实按训练进度退火 SFT 项并与 on-policy group-RL 梯度相加。  SFT-RL 动态混合 LLM 后训练 数据与预算：下一份算力花在哪里 CHORD本地gold candidate能代表真实token不确定性模型吗？ 不能，只是确定性专家代理，未训练LLM词元不确定性。实现需分别记录专家off-policy数据与学生rollout，按规定退火，不能把专家答案泄露到学生评估输入。 例如固定候选标签没有提供真实长文本每个位置的不确定估计。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f4af7a15d2745480">CHORD本地gold candidate能代表真实token不确定性模型吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Achord">CHORD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，只是确定性专家代理，未训练LLM词元不确定性。实现需分别记录专家off-policy数据与学生rollout，按规定退火，不能把专家答案泄露到学生评估输入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如固定候选标签没有提供真实长文本每个位置的不确定估计。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.11408">原论文</a> · <a href="../../../../post-training/2508.11408-chord/">实现解读</a> · <a href="#qa-f4af7a15d2745480">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:spiral" data-paper-title="SPIRAL" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="SPIRAL LLM 后训练 Apple 2025-06-30 同一模型扮演出题者和解题者，在可自动判定的零和多轮语言游戏中形成逐步变难的课程。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.3438（+46.67%）；奖励、KL、长度和候选预算一致。  自博弈课程 LLM 后训练 数据与预算：下一份算力花在哪里 SPIRAL为何让同模型扮演出题与解题两方？ 零和可判定游戏让对手变化形成动态课程，不必人工逐题增加难度。同模型角色不同仍需明确奖励与合法规则，不能让出题者自行宣布胜负。 例如一个角色设计局面，另一个尝试破解，程序按同一规则裁决。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-spiral-8df7f07c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c95c0c1a16fcba51">SPIRAL为何让同模型扮演出题与解题两方？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aspiral">SPIRAL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Apple</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>零和可判定游戏让对手变化形成动态课程，不必人工逐题增加难度。同模型角色不同仍需明确奖励与合法规则，不能让出题者自行宣布胜负。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个角色设计局面，另一个尝试破解，程序按同一规则裁决。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2506.24119">原论文</a> · <a href="../../../../post-training/2506.24119-spiral/">实现解读</a> · <a href="#qa-c95c0c1a16fcba51">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:spiral" data-paper-title="SPIRAL" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="SPIRAL LLM 后训练 Apple 2025-06-30 同一模型扮演出题者和解题者，在可自动判定的零和多轮语言游戏中形成逐步变难的课程。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.3438（+46.67%）；奖励、KL、长度和候选预算一致。  自博弈课程 LLM 后训练 数据与预算：下一份算力花在哪里 SPIRAL的出题者与解题者零和对抗，为什么仍需要可自动判定的游戏规则？ 对抗让双方随着对手变强而调整策略，可形成动态课程；但输赢必须由独立、明确的游戏规则决定，不能让出题者自己宣称解题者失败。零和奖励定义激励关系，不保证课程一定覆盖通用推理。本地只验证状态与目标，没有复刻大模型多轮自博弈训练。 例如出题者设计一个规则明确的文字博弈局面，解题者尝试获胜，程序裁定结果；不能允许出题者临时改规则把任何回答判输。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:spiral" data-paper-title="SPIRAL" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="SPIRAL LLM 后训练 Apple 2025-06-30 同一模型扮演出题者和解题者，在可自动判定的零和多轮语言游戏中形成逐步变难的课程。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.3438（+46.67%）；奖励、KL、长度和候选预算一致。  自博弈课程 LLM 后训练 数据与预算：下一份算力花在哪里 自博弈课程与固定难题库各有什么边界？ 自博弈随对手变化可适应，但也可能陷入局部游戏套路；固定题库覆盖清楚却缺少动态对抗。游戏中进步不能直接外推全部开放推理能力。 例如赢了某种文字博弈，不代表数学、检索和工具任务都同步提升。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a8712f25147d80f3">自博弈课程与固定难题库各有什么边界？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aspiral">SPIRAL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Apple</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>自博弈随对手变化可适应，但也可能陷入局部游戏套路；固定题库覆盖清楚却缺少动态对抗。游戏中进步不能直接外推全部开放推理能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如赢了某种文字博弈，不代表数学、检索和工具任务都同步提升。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2506.24119">原论文</a> · <a href="../../../../post-training/2506.24119-spiral/">实现解读</a> · <a href="#qa-a8712f25147d80f3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:spiral" data-paper-title="SPIRAL" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="SPIRAL LLM 后训练 Apple 2025-06-30 同一模型扮演出题者和解题者，在可自动判定的零和多轮语言游戏中形成逐步变难的课程。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.3438（+46.67%）；奖励、KL、长度和候选预算一致。  自博弈课程 LLM 后训练 数据与预算：下一份算力花在哪里 SPIRAL实现为什么必须保持两方零和奖励对应？ 同一结果的双方优势方向应相反，规则与角色状态需对齐；若两方都因同一获胜得正奖，就改了博弈。当前本地核未复刻大模型多轮自博弈训练。 例如出题方获胜时，解题方不能同时被记录成同样成功。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-aa88b77e42aae8aa">SPIRAL实现为什么必须保持两方零和奖励对应？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aspiral">SPIRAL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Apple</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一结果的双方优势方向应相反，规则与角色状态需对齐；若两方都因同一获胜得正奖，就改了博弈。当前本地核未复刻大模型多轮自博弈训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如出题方获胜时，解题方不能同时被记录成同样成功。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2506.24119">原论文</a> · <a href="../../../../post-training/2506.24119-spiral/">实现解读</a> · <a href="#qa-aa88b77e42aae8aa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:absolute-zero" data-paper-title="Absolute Zero" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Absolute Zero LLM 后训练 Tsinghua University 2025-05-06 proposer 自己生成可验证任务，solver 求解，程序 verifier 提供奖励；按当前能力边界组织课程。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.5938（+153.33%）；奖励、KL、长度和候选预算一致。  零数据自博弈 LLM 后训练 数据与预算：下一份算力花在哪里 Absolute Zero为什么还需要程序verifier？ 模型自生成任务与解答不代表自带真值，程序执行提供独立可验证反馈。零人工逐题数据与零监督不同，课程仍受可执行任务范围和验证器质量限制。 例如生成代码再实际运行核对结果，而不是相信模型自己写的输出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-absolute-zero-7e819456" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-756d0db2f64d583b">Absolute Zero为什么还需要程序verifier？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aabsolute-zero">Absolute Zero</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>模型自生成任务与解答不代表自带真值，程序执行提供独立可验证反馈。零人工逐题数据与零监督不同，课程仍受可执行任务范围和验证器质量限制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如生成代码再实际运行核对结果，而不是相信模型自己写的输出。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.03335">原论文</a> · <a href="../../../../post-training/2505.03335-absolute-zero/">实现解读</a> · <a href="#qa-756d0db2f64d583b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:absolute-zero" data-paper-title="Absolute Zero" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Absolute Zero LLM 后训练 Tsinghua University 2025-05-06 proposer 自己生成可验证任务，solver 求解，程序 verifier 提供奖励；按当前能力边界组织课程。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.5938（+153.33%）；奖励、KL、长度和候选预算一致。  零数据自博弈 LLM 后训练 数据与预算：下一份算力花在哪里 Absolute Zero的自生成课程为什么仍离不开程序验证器？ 提议者产生任务，求解者给出解答，程序执行提供独立奖励，从而无需人工逐题标注。没有人工数据不表示没有监督来源，验证器与任务可执行性构成信号基础。若用任务自带答案直接馈给求解者，就破坏了闭环；本地机制诊断未复现完整大模型课程。 例如模型生成可执行代码任务并预测输出，实际运行程序核对；答案应由执行结果验证，不能把生成任务时保存的标准输出塞进求解提示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:absolute-zero" data-paper-title="Absolute Zero" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Absolute Zero LLM 后训练 Tsinghua University 2025-05-06 proposer 自己生成可验证任务，solver 求解，程序 verifier 提供奖励；按当前能力边界组织课程。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.5938（+153.33%）；奖励、KL、长度和候选预算一致。  零数据自博弈 LLM 后训练 数据与预算：下一份算力花在哪里 proposer生成更难题与有效能力边界课程有什么区别？ 单纯更难可能使solver全失败，没有学习信号；课程需围绕当前能力形成可验证挑战。任务形式合法也不等于有教学价值，不能只优化新颖复杂。 例如一题复杂到预算内无人能解，未必比适度挑战更适合训练。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d1c625299ded1b0f">proposer生成更难题与有效能力边界课程有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aabsolute-zero">Absolute Zero</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单纯更难可能使solver全失败，没有学习信号；课程需围绕当前能力形成可验证挑战。任务形式合法也不等于有教学价值，不能只优化新颖复杂。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一题复杂到预算内无人能解，未必比适度挑战更适合训练。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.03335">原论文</a> · <a href="../../../../post-training/2505.03335-absolute-zero/">实现解读</a> · <a href="#qa-d1c625299ded1b0f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:absolute-zero" data-paper-title="Absolute Zero" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Absolute Zero LLM 后训练 Tsinghua University 2025-05-06 proposer 自己生成可验证任务，solver 求解，程序 verifier 提供奖励；按当前能力边界组织课程。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.5938（+153.33%）；奖励、KL、长度和候选预算一致。  零数据自博弈 LLM 后训练 数据与预算：下一份算力花在哪里 Absolute Zero评估时可把生成时保存的答案给solver吗？ 不能，答案或执行结果应留在验证端，solver只读公开任务。当前本地只验证课程与状态核，没有原规模大模型闭环，不能以内部求解器成绩充当模型能力。 例如模型需预测程序输出，不能先将真实执行输出拼回提示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-9cba8bebbfe55e0e">Absolute Zero评估时可把生成时保存的答案给solver吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aabsolute-zero">Absolute Zero</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，答案或执行结果应留在验证端，solver只读公开任务。当前本地只验证课程与状态核，没有原规模大模型闭环，不能以内部求解器成绩充当模型能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型需预测程序输出，不能先将真实执行输出拼回提示。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.03335">原论文</a> · <a href="../../../../post-training/2505.03335-absolute-zero/">实现解读</a> · <a href="#qa-9cba8bebbfe55e0e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:raft" data-paper-title="RAFT" data-learning-pending="false" data-level="basics" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="RAFT LLM 后训练 HKUST 2023-04-13 PPO 的在线更新不稳定，而在固定 SFT 数据上训练又无法持续利用变好的策略。RAFT 每轮从当前模型生成多个响应，用 reward model 排序并丢弃低质量样本，只对选中的高质量响应执行普通 maximum-likelihood fine-tuning，然后用新策略进入下一轮。 未训练真实生成式 LLM/reward model，也未复刻扩散模型实验。本页实现“当前策略采样 → reward 选优 → 只在保留响应上 SFT → 再采样”的迭代 rejection-sampling 路径，和 RRHF 的全排序 loss 分开。实现在线采样、reward ranking、top-response filtering 和迭代 SFT；未训练真实生成式 LLM/reward model，也未复刻扩散模型实验。候选策略结果只验证算法状态转移。公开 GSM8K candidate 512/128、300 steps、seed 42；  Reward 选优微调 LLM 后训练 数据与预算：下一份算力花在哪里 RAFT为什么用当前模型持续产生新训练候选？ 固定SFT库无法随策略改善提供新数据，迭代采样、奖励排序和选优监督把较好行为加入下一轮。它仍受候选覆盖限制，没生成的优秀答案无法被选。 例如第一轮学好后可生成更好的摘要，再以新候选继续训练。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<span id="paper-post-training-raft-fe9d648c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4b34e16004065fe4">RAFT为什么用当前模型持续产生新训练候选？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Araft">RAFT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · HKUST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定SFT库无法随策略改善提供新数据，迭代采样、奖励排序和选优监督把较好行为加入下一轮。它仍受候选覆盖限制，没生成的优秀答案无法被选。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如第一轮学好后可生成更好的摘要，再以新候选继续训练。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2304.06767">原论文</a> · <a href="../../../../post-training/2304.06767-raft/">实现解读</a> · <a href="#qa-4b34e16004065fe4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:raft" data-paper-title="RAFT" data-learning-pending="false" data-level="mechanism" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="RAFT LLM 后训练 HKUST 2023-04-13 PPO 的在线更新不稳定，而在固定 SFT 数据上训练又无法持续利用变好的策略。RAFT 每轮从当前模型生成多个响应，用 reward model 排序并丢弃低质量样本，只对选中的高质量响应执行普通 maximum-likelihood fine-tuning，然后用新策略进入下一轮。 未训练真实生成式 LLM/reward model，也未复刻扩散模型实验。本页实现“当前策略采样 → reward 选优 → 只在保留响应上 SFT → 再采样”的迭代 rejection-sampling 路径，和 RRHF 的全排序 loss 分开。实现在线采样、reward ranking、top-response filtering 和迭代 SFT；未训练真实生成式 LLM/reward model，也未复刻扩散模型实验。候选策略结果只验证算法状态转移。公开 GSM8K candidate 512/128、300 steps、seed 42；  Reward 选优微调 LLM 后训练 数据与预算：下一份算力花在哪里 RAFT按奖励选优后做最大似然训练，和直接把奖励当策略梯度有何不同？ RAFT用奖励模型排序当前策略的多个回答，筛选高质量样本后执行普通监督微调；奖励决定样本选择，而非直接作为每个动作的梯度权重。新策略再生成下一轮数据，仍受奖励模型偏差与候选覆盖限制。本地候选策略只验证迭代采样和筛选状态转移。 例如从几篇候选摘要中选评分最高的一篇再学习其文字；没有出现的好摘要无法被选中，评分错误也可能被下一轮模仿放大。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:raft" data-paper-title="RAFT" data-learning-pending="false" data-level="comparison" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="RAFT LLM 后训练 HKUST 2023-04-13 PPO 的在线更新不稳定，而在固定 SFT 数据上训练又无法持续利用变好的策略。RAFT 每轮从当前模型生成多个响应，用 reward model 排序并丢弃低质量样本，只对选中的高质量响应执行普通 maximum-likelihood fine-tuning，然后用新策略进入下一轮。 未训练真实生成式 LLM/reward model，也未复刻扩散模型实验。本页实现“当前策略采样 → reward 选优 → 只在保留响应上 SFT → 再采样”的迭代 rejection-sampling 路径，和 RRHF 的全排序 loss 分开。实现在线采样、reward ranking、top-response filtering 和迭代 SFT；未训练真实生成式 LLM/reward model，也未复刻扩散模型实验。候选策略结果只验证算法状态转移。公开 GSM8K candidate 512/128、300 steps、seed 42；  Reward 选优微调 LLM 后训练 数据与预算：下一份算力花在哪里 RAFT与PPO在奖励进入梯度的方式上有何不同？ RAFT奖励决定筛哪些文本，然后用最大似然学习；PPO把优势与概率比直接进入策略目标。筛选监督与加权策略梯度不是同一估计，即便都循环采样。 例如高奖只影响一条回答是否入库，不一定按分数大小连续放大其CE。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-fc21318c02d86430">RAFT与PPO在奖励进入梯度的方式上有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Araft">RAFT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · HKUST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>RAFT奖励决定筛哪些文本，然后用最大似然学习；PPO把优势与概率比直接进入策略目标。筛选监督与加权策略梯度不是同一估计，即便都循环采样。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如高奖只影响一条回答是否入库，不一定按分数大小连续放大其CE。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2304.06767">原论文</a> · <a href="../../../../post-training/2304.06767-raft/">实现解读</a> · <a href="#qa-fc21318c02d86430">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:raft" data-paper-title="RAFT" data-learning-pending="false" data-level="implementation" data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="RAFT LLM 后训练 HKUST 2023-04-13 PPO 的在线更新不稳定，而在固定 SFT 数据上训练又无法持续利用变好的策略。RAFT 每轮从当前模型生成多个响应，用 reward model 排序并丢弃低质量样本，只对选中的高质量响应执行普通 maximum-likelihood fine-tuning，然后用新策略进入下一轮。 未训练真实生成式 LLM/reward model，也未复刻扩散模型实验。本页实现“当前策略采样 → reward 选优 → 只在保留响应上 SFT → 再采样”的迭代 rejection-sampling 路径，和 RRHF 的全排序 loss 分开。实现在线采样、reward ranking、top-response filtering 和迭代 SFT；未训练真实生成式 LLM/reward model，也未复刻扩散模型实验。候选策略结果只验证算法状态转移。公开 GSM8K candidate 512/128、300 steps、seed 42；  Reward 选优微调 LLM 后训练 数据与预算：下一份算力花在哪里 RAFT选优与评估数据隔离应怎样维护？ 奖励模型和采样版本需记录，同提示候选内选优后更新新策略，测试答案不能参与排序。当前候选策略验证状态转移，未训练真实生成式LLM或奖励模型。 例如拿测试正确性直接挑样本再训练，不能称未见测试上的泛化改进。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-cd03d4197adb8876">RAFT选优与评估数据隔离应怎样维护？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Araft">RAFT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · HKUST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>奖励模型和采样版本需记录，同提示候选内选优后更新新策略，测试答案不能参与排序。当前候选策略验证状态转移，未训练真实生成式LLM或奖励模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如拿测试正确性直接挑样本再训练，不能称未见测试上的泛化改进。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2304.06767">原论文</a> · <a href="../../../../post-training/2304.06767-raft/">实现解读</a> · <a href="#qa-cd03d4197adb8876">问题链接</a></p>
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
