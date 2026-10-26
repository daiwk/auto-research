---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 数据与预算：下一份算力花在哪里

[LLM 后训练](index.md) / 子主题导学 · 约 3 分钟 · 38 张论文卡

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

## 这个子主题的论文卡片

导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">
<div class="ar-learning-controls">
<label for="learning-search">搜索卡片
<input id="learning-search" type="search" data-learning-search placeholder="搜索论文、机制、机构或本地边界"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">共 38 张卡片</p>
<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Ask to Distill: Learning to Synthesize Data for On-Policy Distillation LLM 后训练 University of Illinois Urbana-Champaign 2026-10-20 问题决定学生会走到哪些前缀，因而决定教师能提供什么监督。A2D 冻结评分用的师生，训练独立的问题合成器；奖励同时要求“有差异”和“教师偏好的候选仍落在学生可达支持集”，然后筛选问题库，再从原始学生初始化执行 OPD。不是给每道问题做一次学生微调来估价。 完整实验成本过高，不复现（审查 DONE）。三 seed 仍只是机制诊断。仅实现 L1 奖励与更新公式组件，不是完整合成数据系统或能力复现。diagnostic_only=true；不可晋级、未接入 Evolve。完整实验成本过高，不复现（审查 DONE）。本页属于 10 月 21 日同一公告的补审，不是上一批之后的新首发。无下载、无预训练模型调用。随机生成的 logits、显式 mask 和外部 cluster share 只检查公式，不生成自然语言问题。CPU/CUDA 都运行同一算子；CUDA 不可用报错，不回退。输出不可覆盖，最多三个 seed；三 seed 仍只是机制诊断。  On-policy distillation 蒸馏数据合成与筛选 LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-ask-to-distill-6c38407f">Ask to Distill: Learning to Synthesize Data for On-Policy Distillation</h2>
<p class="ar-learning-card__meta">University of Illinois Urbana-Champaign · 论文公开：2026-10-20</p>
<p><strong>方法要点：</strong>问题决定学生会走到哪些前缀，因而决定教师能提供什么监督。A2D 冻结评分用的师生，训练独立的问题合成器；奖励同时要求“有差异”和“教师偏好的候选仍落在学生可达支持集”，然后筛选问题库，再从原始学生初始化执行 OPD。不是给每道问题做一次学生微调来估价。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）。三 seed 仍只是机制诊断。仅实现 L1 奖励与更新公式组件，不是完整合成数据系统或能力复现。diagnostic_only=true；不可晋级、未接入 Evolve。完整实验成本过高，不复现（审查 DONE）。本页属于 10 月 21 日同一公告的补审，不是上一批之后的新首发。无下载、无预训练模型调用。随机生成的 logits、显式 mask 和外部 cluster share 只检查公式，不生成自然语言问题。CPU/CUDA 都运行同一算子；CUDA 不可用报错，不回退。输出不可覆盖，最多三个 seed；三 seed 仍只是机制诊断。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.27450v1">原论文</a> · <a href="../../../../post-training/2610.27450-ask-to-distill/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Preserving Reasoning Diversity in Reinforcement Learning with Verifiable Rewards via Adaptive Replay LLM 后训练 Cornell University 2026-10-16 有限on-policy采样可能逐步压低同样正确但较少出现的推理模式；仅在当前rollout上重加权，难以恢复已经采不到的模式。TAR先从基础策略大量生成，过滤正确回答，再保留分散的原型轨迹。训练时只重放相对base已经被压制的轨迹，并将梯度集中到其中被压制的token，避免始终模仿有限bank限制策略适应。原文§3–4 原图建议：Figure 3压制比例与gated replay loss的机制分析图；原文未提供完整架构图，以上Mermaid是方法重绘，不冒充原图。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是数学推理或语义多样性复现。L1 定义性组件／梯度诊断，不是数学推理或语义多样性复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接Evolve。随机初始化16词表、8维GRU，base为当前初始策略的冻结副本。每个公开prompt实际采8个回答，外部合成verifier检查后，在base真实隐状态上做FPS并保留至多3条；未用gold、模板答案或手写候选填充bank。该随机初始隐状态不是语义encoder，只能验证FPS的定义，不能说明语义推理模式覆盖。  RLVR 多样性与经验重放 后训练算法组件 LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-tar-adaptive-replay-2e44ae67">Preserving Reasoning Diversity in Reinforcement Learning with Verifiable Rewards via Adaptive Replay</h2>
<p class="ar-learning-card__meta">Cornell University · 论文公开：2026-10-16</p>
<p><strong>方法要点：</strong>有限on-policy采样可能逐步压低同样正确但较少出现的推理模式；仅在当前rollout上重加权，难以恢复已经采不到的模式。TAR先从基础策略大量生成，过滤正确回答，再保留分散的原型轨迹。训练时只重放相对base已经被压制的轨迹，并将梯度集中到其中被压制的token，避免始终模仿有限bank限制策略适应。原文§3–4 原图建议：Figure 3压制比例与gated replay loss的机制分析图；原文未提供完整架构图，以上Mermaid是方法重绘，不冒充原图。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是数学推理或语义多样性复现。L1 定义性组件／梯度诊断，不是数学推理或语义多样性复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接Evolve。随机初始化16词表、8维GRU，base为当前初始策略的冻结副本。每个公开prompt实际采8个回答，外部合成verifier检查后，在base真实隐状态上做FPS并保留至多3条；未用gold、模板答案或手写候选填充bank。该随机初始隐状态不是语义encoder，只能验证FPS的定义，不能说明语义推理模式覆盖。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24236v1">原论文</a> · <a href="../../../../post-training/2610.24236-tar-adaptive-replay/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Does On-Policy Distillation Need to Complete Every Rollout? LLM 后训练 Cornell University 2026-10-15 每条响应在生成之前独立采样 anchor，向上取整到 block 末尾，学生只生成到该 cutoff 或自然 EOS。保留的每个 token 都接收教师监督，并按其精确 inclusion probability 加权；自然 EOS 也是普通有效 token。若把截断结果直接除以本批随机 token 数，不能沿用无偏 gradient-sum 的论证，所以实现使用前一批加权 token count。 完整长 rollout 训练成本过高，不复现（审查 DONE）；L1 cutoff / IPW / lagged normalizer 组件，真实短策略更新。完整长 rollout 训练成本过高，不复现（审查 DONE）；不是固定前缀截断的改名。固定公开 Hamlet 1524，revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784；byte 范围 80%/10%/10% 隔离。微型教师 next-token 训练后冻结，学生真实在线生成；  On-policy distillation 后训练算法组件 STOPD LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-stopd-818867f2">Does On-Policy Distillation Need to Complete Every Rollout?</h2>
<p class="ar-learning-card__meta">Cornell University · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>每条响应在生成之前独立采样 anchor，向上取整到 block 末尾，学生只生成到该 cutoff 或自然 EOS。保留的每个 token 都接收教师监督，并按其精确 inclusion probability 加权；自然 EOS 也是普通有效 token。若把截断结果直接除以本批随机 token 数，不能沿用无偏 gradient-sum 的论证，所以实现使用前一批加权 token count。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整长 rollout 训练成本过高，不复现（审查 DONE）；L1 cutoff / IPW / lagged normalizer 组件，真实短策略更新。完整长 rollout 训练成本过高，不复现（审查 DONE）；不是固定前缀截断的改名。固定公开 Hamlet 1524，revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784；byte 范围 80%/10%/10% 隔离。微型教师 next-token 训练后冻结，学生真实在线生成；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21337v1">原论文</a> · <a href="../../../../post-training/2610.21337-stopd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="BoundaryEvo: Data-Model Co-Evolution at the Capability Boundary for Long-Chain Reasoning Distillation LLM 后训练 Shanghai Artificial Intelligence Laboratory 2026-10-09 长推理监督的价值随学生能力变化。BoundaryEvo 先不按 correctness 过滤地蒸馏少量教师行为做 capability priming，然后每轮用当前学生、固定 expert 和 analyzer 重估边界，保留仍未掌握的 replay 并补充新问题；选好问题后再生成并验证 fresh teacher trajectories。 短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：正式对照设计尚未执行；计划以相同学生的 teacher-primed checkpoint 为基线，边界筛选后 fresh teacher 轨迹 SFT 为实验组。本次只有短预算机制诊断，本短跑稳定相对提升不适用，不报告能力收益；空边界或无 Stage 2 更新保留失败。  Capability boundary Data-model co-evolution Reasoning distillation LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-boundary-evo-60ecea39">BoundaryEvo: Data-Model Co-Evolution at the Capability Boundary for Long-Chain Reasoning Distillation</h2>
<p class="ar-learning-card__meta">Shanghai Artificial Intelligence Laboratory · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>长推理监督的价值随学生能力变化。BoundaryEvo 先不按 correctness 过滤地蒸馏少量教师行为做 capability priming，然后每轮用当前学生、固定 expert 和 analyzer 重估边界，保留仍未掌握的 replay 并补充新问题；选好问题后再生成并验证 fresh teacher trajectories。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：正式对照设计尚未执行；计划以相同学生的 teacher-primed checkpoint 为基线，边界筛选后 fresh teacher 轨迹 SFT 为实验组。本次只有短预算机制诊断，本短跑稳定相对提升不适用，不报告能力收益；空边界或无 Stage 2 更新保留失败。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13285">原论文</a> · <a href="../../../../reproductions/2610.13285-boundary-evo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Branching On-Policy Distillation LLM 后训练 Tsinghua University / SenseTime Research 2026-10-09 普通 OPD 每个前缀只看到一次后续。BranchOPD 用学生不确定性和师生分歧定位 fork，从同一冻结学生策略独立采样 suffix，前缀只计入一次；并用协议事件监督结束行为。分枝不是教师强制 token，也不按答案正确性筛选。 短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：计划基线为相同学生的单轨 OPD，实验组执行 student 分枝采样、teacher 计分与 PBR；本次没有实跑同预算基线，稳定相对提升不适用。  On-policy distillation Student-policy branching Protocol-boundary repair LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-branch-opd-974c9738">Branching On-Policy Distillation</h2>
<p class="ar-learning-card__meta">Tsinghua University / SenseTime Research · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>普通 OPD 每个前缀只看到一次后续。BranchOPD 用学生不确定性和师生分歧定位 fork，从同一冻结学生策略独立采样 suffix，前缀只计入一次；并用协议事件监督结束行为。分枝不是教师强制 token，也不按答案正确性筛选。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。核心机制代码路径；短预算 checkpoint 结果只支持 runtime 诊断，不支持论文规模能力结论。本地对照口径：计划基线为相同学生的单轨 OPD，实验组执行 student 分枝采样、teacher 计分与 PBR；本次没有实跑同预算基线，稳定相对提升不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13481">原论文</a> · <a href="../../../../reproductions/2610.13481-branch-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="A Step Harder, Not a Step Too Far: The Benefits and Limits of Curriculum Difficulty Progression in GRPO LLM 后训练 Dalian Maritime University 2026-10-09 difficulty随当前policy变化，样本可能反复进出难度带。论文比较静态easy-to-hard、在线fixed-medium和B1→B5课程，进一步升到B5会退化。实现每步真实rollout重新估难、保留B5控制，不按problem长度或旧评分替代。 本次不复现原文完整B1→B5课程或B5退化。staged缩放成每步validation诊断，保持噪声容忍/恢复best checkpoint；本地对照口径：基线为相同checkpoint与配置的unfiltered、fixed-medium、static、staged、B5-too-hard；按实际effective-update/rollout预算解释；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  GRPO difficulty curriculum Current-policy recalibration Overly-hard degradation control LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-grpo-difficulty-curriculum-3b9ce14e">A Step Harder, Not a Step Too Far: The Benefits and Limits of Curriculum Difficulty Progression in GRPO</h2>
<p class="ar-learning-card__meta">Dalian Maritime University · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>difficulty随当前policy变化，样本可能反复进出难度带。论文比较静态easy-to-hard、在线fixed-medium和B1→B5课程，进一步升到B5会退化。实现每步真实rollout重新估难、保留B5控制，不按problem长度或旧评分替代。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本次不复现原文完整B1→B5课程或B5退化。staged缩放成每步validation诊断，保持噪声容忍/恢复best checkpoint；本地对照口径：基线为相同checkpoint与配置的unfiltered、fixed-medium、static、staged、B5-too-hard；按实际effective-update/rollout预算解释；实验组仅支持本页L0/L1机制，稳定相对提升不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13669">原论文</a> · <a href="../../../../reproductions/2610.13669-grpo-difficulty-curriculum/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Learning More by Training Less: Uncertainty-Guided Progressive Contraction for Efficient Reasoning Post-Training LLM 后训练 National University of Singapore / Nanjing University 2026-10-09 正确teacher CoT也可能经过多种正确/错误后续的reasoning fork。论文对真实prefix做Monte Carlo continuation，按branch不确定性先收缩teacher pool，再经真实student probing epoch按当前NLL选top-M并重路由。teacher profiling与student训练曝光必须分开核算。 本页不声明未执行实验已经完成。本地对照口径：基线为同一真实verified teacher全集的full-SFT；相同epochs，teacher profiling成本不并入student exposure比率；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Monte Carlo reasoning tree Teacher-side uncertainty contraction Learner-aware SFT routing LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-progressive-contraction-16120d48">Learning More by Training Less: Uncertainty-Guided Progressive Contraction for Efficient Reasoning Post-Training</h2>
<p class="ar-learning-card__meta">National University of Singapore / Nanjing University · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>正确teacher CoT也可能经过多种正确/错误后续的reasoning fork。论文对真实prefix做Monte Carlo continuation，按branch不确定性先收缩teacher pool，再经真实student probing epoch按当前NLL选top-M并重路由。teacher profiling与student训练曝光必须分开核算。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本页不声明未执行实验已经完成。本地对照口径：基线为同一真实verified teacher全集的full-SFT；相同epochs，teacher profiling成本不并入student exposure比率；实验组仅支持本页L0/L1机制，稳定相对提升不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12933">原论文</a> · <a href="../../../../reproductions/2610.12933-progressive-contraction/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Continually Post-training Small Models via Synthetic Self-distillation LLM 后训练 KAIST AI / LG AI Research 2026-10-09 小模型self-rewrite可能失真，直接SFT又可能偏离base分布。SynthSelf用更大的同家族aligner把train demonstration贪心离线改写，通过答案拒绝采样后SFT。不允许student读评测答案，也不以文本过滤替代真实训练。 默认GSM validation预先拆不重叠两片，只是同域acquisition/retention诊断。本地对照口径：基线为同初始学生与epochs的gold-SFT；另可unfiltered-rewrite消融，真实token预算不相同则明确记录；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  Synthetic self-distillation Same-family aligner Offline rejection-sampled SFT LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-synthself-6e723ecb">Continually Post-training Small Models via Synthetic Self-distillation</h2>
<p class="ar-learning-card__meta">KAIST AI / LG AI Research · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>小模型self-rewrite可能失真，直接SFT又可能偏离base分布。SynthSelf用更大的同家族aligner把train demonstration贪心离线改写，通过答案拒绝采样后SFT。不允许student读评测答案，也不以文本过滤替代真实训练。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>默认GSM validation预先拆不重叠两片，只是同域acquisition/retention诊断。本地对照口径：基线为同初始学生与epochs的gold-SFT；另可unfiltered-rewrite消融，真实token预算不相同则明确记录；实验组仅支持本页L0/L1机制，稳定相对提升不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13113">原论文</a> · <a href="../../../../reproductions/2610.13113-synthself/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="DIAL-OPD: Learning More from Fewer Tokens in On-Policy Distillation LLM 后训练 Eastern Institute of Technology, Ningbo / The Hong Kong Polytechnic University 2026-10-08 用概率的对数均值调节教师—学生对数差异，降低两者都不认可的低概率 token 的监督优先级。按每条响应选取高分位置，未选位置仍保留为上下文。 核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式、可直接改路径运行的命令见checkpoint 运行说明。  On-policy distillation Token supervision LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-dial-opd-c9cdfa1a">DIAL-OPD: Learning More from Fewer Tokens in On-Policy Distillation</h2>
<p class="ar-learning-card__meta">Eastern Institute of Technology, Ningbo / The Hong Kong Polytechnic University · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>用概率的对数均值调节教师—学生对数差异，降低两者都不认可的低概率 token 的监督优先级。按每条响应选取高分位置，未选位置仍保留为上下文。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式、可直接改路径运行的命令见checkpoint 运行说明。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11659">原论文</a> · <a href="../../../../post-training/2610.11659-dial-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="GRPODropout: Less is More for Online Reinforcement Learning Rollouts LLM 后训练 Harbin Institute of Technology (Shenzhen) 2026-10-08 从同一 prompt 的 GRPO 响应组中筛除部分高概率、正优势响应，并用旧策略概率重新中心化保留响应的优势。不是随机 dropout，也不改变生成预算。 核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式和命令见checkpoint 运行说明。  RLVR Rollout selection LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-grpo-dropout-a03001b8">GRPODropout: Less is More for Online Reinforcement Learning Rollouts</h2>
<p class="ar-learning-card__meta">Harbin Institute of Technology (Shenzhen) · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>从同一 prompt 的 GRPO 响应组中筛除部分高概率、正优势响应，并用旧策略概率重新中心化保留响应的优势。不是随机 dropout，也不改变生成预算。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式和命令见checkpoint 运行说明。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11854">原论文</a> · <a href="../../../../post-training/2610.11854-grpo-dropout/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="MagicBeanStalk: Escaping the RLVR Zero Advantage Trap with Recursive Data Synthesis LLM 后训练 University of Washington 2026-10-08 RLVR有效性取决于problem、当前policy、rollout预算。MBS从verified hard seed提炼reasoning蓝图，自顶向下分解并实测child worked examples是否提高parent正确率，再合成更难新leaf、自底向上按原依赖组合。最终独立验证、保蓝图和实质新颖性，并满足目标policy Goldilocks及预算内完整正确解。 当前状态（2026-10-14）：成本过高，暂不复现／完整方法待验收。本轮新路径固定在 4c4710cd，仅依据 train/validation 教师短诊断提出，尚须新源码完整 GPU 验证。当前状态（2026-10-14）：成本过高，暂不复现／完整方法待验收。用户要求先交付其余成果，不再扩大候选池、更换教师或启动后续种子。本页保留论文解读、实验源码和所有失败证据；magicbeanstalk 只是历史计划键，已从可执行 registry、批量 reproduce 和公开训练 runner 中移出，不是已完成实现，也未接入 evolve。  RLVR data synthesis Effectivity-validated decomposition Policy-calibrated Goldilocks LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-magicbeanstalk-9678e8db">MagicBeanStalk: Escaping the RLVR Zero Advantage Trap with Recursive Data Synthesis</h2>
<p class="ar-learning-card__meta">University of Washington · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>RLVR有效性取决于problem、当前policy、rollout预算。MBS从verified hard seed提炼reasoning蓝图，自顶向下分解并实测child worked examples是否提高parent正确率，再合成更难新leaf、自底向上按原依赖组合。最终独立验证、保蓝图和实质新颖性，并满足目标policy Goldilocks及预算内完整正确解。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>当前状态（2026-10-14）：成本过高，暂不复现／完整方法待验收。本轮新路径固定在 4c4710cd，仅依据 train/validation 教师短诊断提出，尚须新源码完整 GPU 验证。当前状态（2026-10-14）：成本过高，暂不复现／完整方法待验收。用户要求先交付其余成果，不再扩大候选池、更换教师或启动后续种子。本页保留论文解读、实验源码和所有失败证据；magicbeanstalk 只是历史计划键，已从可执行 registry、批量 reproduce 和公开训练 runner 中移出，不是已完成实现，也未接入 evolve。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12659">原论文</a> · <a href="../../../../reproductions/2610.12659-magicbeanstalk/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="PIVOT: Perplexity-Informed KD-to-RL Transition Scheduling for Vertical-Domain Few-Shot Distillation LLM 后训练 Ping An Technology / University of Science and Technology of China 2026-10-08 垂直领域的小模型既需要教师传授知识，也需要任务奖励改善最终判断；所有样本同时从蒸馏切换到 RL，可能使困难样本过早失去教师监督。PIVOT 在学生自己的响应上计算教师困惑度，先把低困惑度问题切换到 GRPO，高困惑度问题继续 OPD。 有界少样本、单 seed、LoRA 与短训练只验证机制，不复现原始 480 步/全参数/HWU64 能力收益。共享热身、样本级路由和三配方重置已在 A100 实跑；8 题诊断无准确率提升，不等于原论文能力复现。真实 Qwen2.5-0.5B-Instruct 学生、7B-Instruct 教师，q/v LoRA 而非原文全参数微调。所有配方共享教师响应两轮 SFT、初始 OPD 热身和相同初始 adapter；随后重置 optimizer 与随机种子，分别执行持续 OPD、固定半预算切换及样本级 PIVOT。  On-policy 蒸馏 组相对策略优化 LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-pivot-65855e82">PIVOT: Perplexity-Informed KD-to-RL Transition Scheduling for Vertical-Domain Few-Shot Distillation</h2>
<p class="ar-learning-card__meta">Ping An Technology / University of Science and Technology of China · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>垂直领域的小模型既需要教师传授知识，也需要任务奖励改善最终判断；所有样本同时从蒸馏切换到 RL，可能使困难样本过早失去教师监督。PIVOT 在学生自己的响应上计算教师困惑度，先把低困惑度问题切换到 GRPO，高困惑度问题继续 OPD。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>有界少样本、单 seed、LoRA 与短训练只验证机制，不复现原始 480 步/全参数/HWU64 能力收益。共享热身、样本级路由和三配方重置已在 A100 实跑；8 题诊断无准确率提升，不等于原论文能力复现。真实 Qwen2.5-0.5B-Instruct 学生、7B-Instruct 教师，q/v LoRA 而非原文全参数微调。所有配方共享教师响应两轮 SFT、初始 OPD 热身和相同初始 adapter；随后重置 optimizer 与随机种子，分别执行持续 OPD、固定半预算切换及样本级 PIVOT。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11167">原论文</a> · <a href="../../../../post-training/2610.11167-pivot/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="ReCal: Calibrating Structured Pruning for On-Policy Distillation Recovery LLM 后训练 Zhongguancun Academy / Tencent / University of Science and Technology of China 2026-10-08 先剪枝再蒸馏并不保证可恢复：损坏的学生轨迹会限制 OPD 教师信号。ReCal 先用剪枝 probe 测量教师轨迹上损伤，再用损伤重加权原始未剪枝模型的校准统计，重新选择通道；目标宽度和恢复流程保持一致。 恢复使用 q/v LoRA，未复现原文全参数 FSDP、四领域数据或多 seed。已实现真实 FFN 通道删除、教师 SFT 和学生轨迹 OPD；当前四题诊断包含负结果，不代表论文 benchmark 收益。Qwen3-4B/A100，FFN 宽度从 9728 真正减到 7296。对照与 ReCal 使用相同目标宽度和教师 SFT 响应，2 轮 SFT、4 步 OPD；SFT/OPD 问题分开，验证 4 题。见运行说明。  On-policy distillation 剪枝恢复 LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-recal-386ad741">ReCal: Calibrating Structured Pruning for On-Policy Distillation Recovery</h2>
<p class="ar-learning-card__meta">Zhongguancun Academy / Tencent / University of Science and Technology of China · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>先剪枝再蒸馏并不保证可恢复：损坏的学生轨迹会限制 OPD 教师信号。ReCal 先用剪枝 probe 测量教师轨迹上损伤，再用损伤重加权原始未剪枝模型的校准统计，重新选择通道；目标宽度和恢复流程保持一致。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>恢复使用 q/v LoRA，未复现原文全参数 FSDP、四领域数据或多 seed。已实现真实 FFN 通道删除、教师 SFT 和学生轨迹 OPD；当前四题诊断包含负结果，不代表论文 benchmark 收益。Qwen3-4B/A100，FFN 宽度从 9728 真正减到 7296。对照与 ReCal 使用相同目标宽度和教师 SFT 响应，2 轮 SFT、4 步 OPD；SFT/OPD 问题分开，验证 4 题。见运行说明。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11332">原论文</a> · <a href="../../../../post-training/2610.11332-recal/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Follow the Winners: Conservative Policy Improvement with the Cross-Entropy Method for Critic-Free RFT LLM 后训练 Trent AI Limited 2026-10-02 在有状态工具环境里，为同一提示重复生成一组等价 rollout 往往很贵；而 PPO 的 critic 又占用额外模型资源。FTW 不计算 value，也不要求 GRPO 式同题多轨迹。它保留近期策略产生的真实轨迹，从 FIFO 池中反复抽取小批量、仅模仿每批回报最高的条，并用 KL 约束更新幅度。过去轨迹被再次选中的次数自然形成训练权重，而不是对整池只做一次硬截断。 L1 核心机制诊断。L1 核心机制诊断。实现了论文 Algorithm 2 的 FIFO 轨迹池、重复小批量 top- 筛选和带 KL 正则的交叉熵策略投影；目前只在合成双臂 bandit 上执行，不等同于论文的 LLM Agent 训练。没有训练 Qwen、运行 Sokoban/Search-R1，也没有与同预算 PPO/GRPO 比较；bandit 的已知均值只用于诊断，不构成验证集/测试集上的调参或能力评测。该产物标记 diagnostic_only=true、formal_comparison=false，不参与公开能力提升或 Evolve 晋级。  Agentic RL 无 critic 策略改进 精英轨迹筛选 LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-follow-the-winners-b5a02f54">Follow the Winners: Conservative Policy Improvement with the Cross-Entropy Method for Critic-Free RFT</h2>
<p class="ar-learning-card__meta">Trent AI Limited · 论文公开：2026-10-02</p>
<p><strong>方法要点：</strong>在有状态工具环境里，为同一提示重复生成一组等价 rollout 往往很贵；而 PPO 的 critic 又占用额外模型资源。FTW 不计算 value，也不要求 GRPO 式同题多轨迹。它保留近期策略产生的真实轨迹，从 FIFO 池中反复抽取小批量、仅模仿每批回报最高的条，并用 KL 约束更新幅度。过去轨迹被再次选中的次数自然形成训练权重，而不是对整池只做一次硬截断。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>L1 核心机制诊断。L1 核心机制诊断。实现了论文 Algorithm 2 的 FIFO 轨迹池、重复小批量 top- 筛选和带 KL 正则的交叉熵策略投影；目前只在合成双臂 bandit 上执行，不等同于论文的 LLM Agent 训练。没有训练 Qwen、运行 Sokoban/Search-R1，也没有与同预算 PPO/GRPO 比较；bandit 的已知均值只用于诊断，不构成验证集/测试集上的调参或能力评测。该产物标记 diagnostic_only=true、formal_comparison=false，不参与公开能力提升或 Evolve 晋级。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03361">原论文</a> · <a href="../../../../post-training/2610.03361-follow-the-winners/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="LESSER: Post-Training Data Selection with Output-Layer Gradients LLM 后训练 University of Pennsylvania 2026-10-02 现有面向目标任务的数据选择常计算每个候选样本和少量目标任务 query 的全参数梯度，再按相似性选取训练子集；对大模型逐样本反传代价很高。LESSER 只替换特征：从一次前向得到的最后隐藏状态和词表概率解析地计算输出层梯度。SFT、RL 问题选择或教师选择原有的选择规则不需要改变。 L1 前向特征与筛选协议诊断。L1 前向特征与筛选协议诊断。已实现论文的输出层梯度、双侧随机投影及保持不变的 round-robin 选择；没有宣称复现大模型微调、RL、教师选择或论文速度收益。这里的隐藏状态和 logits 来自固定随机张量，用于公式与选择器的确定性验证；没有在公开 Tulu V2、GSM8K 等数据上运行真实 LLM，也没有比较训练后的任务效果或 A100 吞吐。因此标记 diagnostic_only=true，不进入正式能力看板或 Evolve 增益候选。若要升级为 L2，需固定公开 checkpoint/数据修订、query/test 切分、同预算 LESS/随机对照和多 seed 下游训练；  后训练数据选择 梯度特征 计算效率 LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-lesser-18cdf418">LESSER: Post-Training Data Selection with Output-Layer Gradients</h2>
<p class="ar-learning-card__meta">University of Pennsylvania · 论文公开：2026-10-02</p>
<p><strong>方法要点：</strong>现有面向目标任务的数据选择常计算每个候选样本和少量目标任务 query 的全参数梯度，再按相似性选取训练子集；对大模型逐样本反传代价很高。LESSER 只替换特征：从一次前向得到的最后隐藏状态和词表概率解析地计算输出层梯度。SFT、RL 问题选择或教师选择原有的选择规则不需要改变。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>L1 前向特征与筛选协议诊断。L1 前向特征与筛选协议诊断。已实现论文的输出层梯度、双侧随机投影及保持不变的 round-robin 选择；没有宣称复现大模型微调、RL、教师选择或论文速度收益。这里的隐藏状态和 logits 来自固定随机张量，用于公式与选择器的确定性验证；没有在公开 Tulu V2、GSM8K 等数据上运行真实 LLM，也没有比较训练后的任务效果或 A100 吞吐。因此标记 diagnostic_only=true，不进入正式能力看板或 Evolve 增益候选。若要升级为 L2，需固定公开 checkpoint/数据修订、query/test 切分、同预算 LESS/随机对照和多 seed 下游训练；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03702">原论文</a> · <a href="../../../../post-training/2610.03702-lesser/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Dependency-Aware Reward Shaping for Agentic Reinforcement Learning LLM 后训练 University of Illinois Urbana-Champaign 2026-10-01 把任务进度表示为带先决条件的 predicate 图；验证、失效和修复事件更新图状态，最近破损依赖按图距离衰减已完成工作的 credit，独立分支不受牵连。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行依赖衰减、失效/修复与 potential 差分；未训练 1.5B–8B 模型，官方仓库当前仅发布接口说明、代码仍在准备。执行依赖衰减、失效/修复与 potential 差分；未训练 1.5B–8B 模型，官方仓库当前仅发布接口说明、代码仍在准备。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Agentic RL 依赖图 步级奖励 LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-dars-eb9dd187">Dependency-Aware Reward Shaping for Agentic Reinforcement Learning</h2>
<p class="ar-learning-card__meta">University of Illinois Urbana-Champaign · 论文公开：2026-10-01</p>
<p><strong>方法要点：</strong>把任务进度表示为带先决条件的 predicate 图；验证、失效和修复事件更新图状态，最近破损依赖按图距离衰减已完成工作的 credit，独立分支不受牵连。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行依赖衰减、失效/修复与 potential 差分；未训练 1.5B–8B 模型，官方仓库当前仅发布接口说明、代码仍在准备。执行依赖衰减、失效/修复与 potential 差分；未训练 1.5B–8B 模型，官方仓库当前仅发布接口说明、代码仍在准备。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01207">原论文</a> · <a href="../../../../post-training/2610.01207-dars/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Guide, Then Let Go: Gap-Adaptive Teacher Scheduling for Sparse-Reward Agentic RL LLM 后训练 Dalian University of Technology / Kuaishou 2026-09-29 用教师训练尾部成功率作为固定参考，以学生滞后一拍的移动平均估计能力差距；OPD 权重随差距线性下降，学生达到教师参考后永久关闭教师分支，继续只做 GRPO。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行滞后一拍移动平均、gap weight 和永久 withdrawal；未做 Qwen Agent RL。执行滞后一拍移动平均、gap weight 和永久 withdrawal；未做 Qwen Agent RL。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  Agentic RL On-policy distillation 课程调度 LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-gats-23ea5c63">Guide, Then Let Go: Gap-Adaptive Teacher Scheduling for Sparse-Reward Agentic RL</h2>
<p class="ar-learning-card__meta">Dalian University of Technology / Kuaishou · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>用教师训练尾部成功率作为固定参考，以学生滞后一拍的移动平均估计能力差距；OPD 权重随差距线性下降，学生达到教师参考后永久关闭教师分支，继续只做 GRPO。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行滞后一拍移动平均、gap weight 和永久 withdrawal；未做 Qwen Agent RL。执行滞后一拍移动平均、gap weight 和永久 withdrawal；未做 Qwen Agent RL。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37898">原论文</a> · <a href="../../../../post-training/2609.37898-gats/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Shockingly Simple Self-retrospection Improves Agentic Models Without RL LLM 后训练 Rensselaer Polytechnic Institute 2026-09-28 ROFT 不直接用环境奖励更新动作策略，而是让模型在完整轨迹与反馈之后生成一段自我回顾，再只监督回顾 token。回顾成为后续行为可复用的训练信号，同时避免把环境文本或历史动作误当监督标签。 复现级别：L1 核心机制 + 真实 checkpoint CUDA 路径。复现级别：L1 核心机制 + 真实 checkpoint CUDA 路径。本地实现全局 retrospection-token 交叉熵；不声称复现论文规模训练收益。当前没有论文规模 Agent rollout 数据，也没有把 ROFT 注册进 Evolve；在统一控制器能够实际构造回顾数据、训练并用隔离验证集评价前，不把 registry 标签当成已接入。roft_retrospection_loss 是可训练的 PyTorch 目标；通用后训练 CLI 中的 roft 只提供小型候选策略诊断。  自我回顾 监督微调 Agent 后训练 LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-roft-6e694561">Shockingly Simple Self-retrospection Improves Agentic Models Without RL</h2>
<p class="ar-learning-card__meta">Rensselaer Polytechnic Institute · 论文公开：2026-09-28</p>
<p><strong>方法要点：</strong>ROFT 不直接用环境奖励更新动作策略，而是让模型在完整轨迹与反馈之后生成一段自我回顾，再只监督回顾 token。回顾成为后续行为可复用的训练信号，同时避免把环境文本或历史动作误当监督标签。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：L1 核心机制 + 真实 checkpoint CUDA 路径。复现级别：L1 核心机制 + 真实 checkpoint CUDA 路径。本地实现全局 retrospection-token 交叉熵；不声称复现论文规模训练收益。当前没有论文规模 Agent rollout 数据，也没有把 ROFT 注册进 Evolve；在统一控制器能够实际构造回顾数据、训练并用隔离验证集评价前，不把 registry 标签当成已接入。roft_retrospection_loss 是可训练的 PyTorch 目标；通用后训练 CLI 中的 roft 只提供小型候选策略诊断。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35741">原论文</a> · <a href="../../../../post-training/2609.35741-roft/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="ROSS: Relearning from Self-Generated Rollouts through Selective Supervision LLM 后训练 AllSpark Team（原文以团队署名，未列机构） 2026-09-28 保留历史 self-rollout 的完整上下文，但只对筛选出的模型 continuation 计算损失，避免模仿其中错误或冗余步骤。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 full-context/selective-loss 边界；选择 mask 是 fixture，不冒充论文 selector。执行 full-context/selective-loss 边界；选择 mask 是 fixture，不冒充论文 selector。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  离线 SFT 选择性监督 LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-ross-56261390">ROSS: Relearning from Self-Generated Rollouts through Selective Supervision</h2>
<p class="ar-learning-card__meta">AllSpark Team（原文以团队署名，未列机构） · 论文公开：2026-09-28</p>
<p><strong>方法要点：</strong>保留历史 self-rollout 的完整上下文，但只对筛选出的模型 continuation 计算损失，避免模仿其中错误或冗余步骤。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 full-context/selective-loss 边界；选择 mask 是 fixture，不冒充论文 selector。执行 full-context/selective-loss 边界；选择 mask 是 fixture，不冒充论文 selector。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35954">原论文</a> · <a href="../../../../post-training/2609.35954-ross/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="RetireOPD: Self-Retiring On-Policy Distillation for Agentic Reinforcement Learning LLM 后训练 Zhejiang University 2026-09-17 给不同技能配置解耦教师；学生同时执行 RL 与 on-policy distillation，当成功率接近教师且分布差距不再收缩时自动退休教师。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行退休判据与学生更新；未训练论文规模 Agent 教师。本地执行退休判据与学生更新；未训练论文规模 Agent 教师。  On-policy distillation Agent RL LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-retire-opd-e8a79255">RetireOPD: Self-Retiring On-Policy Distillation for Agentic Reinforcement Learning</h2>
<p class="ar-learning-card__meta">Zhejiang University · 论文公开：2026-09-17</p>
<p><strong>方法要点：</strong>给不同技能配置解耦教师；学生同时执行 RL 与 on-policy distillation，当成功率接近教师且分布差距不再收缩时自动退休教师。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行退休判据与学生更新；未训练论文规模 Agent 教师。本地执行退休判据与学生更新；未训练论文规模 Agent 教师。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.20784">原论文</a> · <a href="../../../../post-training/2609.20784-retire-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Trajectory Learnability for Offline On-Policy Distillation LLM 后训练 National University of Singapore 2026-09-16 用成功轨迹训练参考模型，以参考与当前策略逐 token 对数似然变化衡量可学性，并据此重加权离线 OPD 轨迹。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行逐 token 可学性聚合和轨迹加权；未复刻论文 GPU 训练预算。本地执行逐 token 可学性聚合和轨迹加权；未复刻论文 GPU 训练预算。  On-policy distillation 轨迹加权 LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-trajectory-learnability-8d70d16c">Trajectory Learnability for Offline On-Policy Distillation</h2>
<p class="ar-learning-card__meta">National University of Singapore · 论文公开：2026-09-16</p>
<p><strong>方法要点：</strong>用成功轨迹训练参考模型，以参考与当前策略逐 token 对数似然变化衡量可学性，并据此重加权离线 OPD 轨迹。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行逐 token 可学性聚合和轨迹加权；未复刻论文 GPU 训练预算。本地执行逐 token 可学性聚合和轨迹加权；未复刻论文 GPU 训练预算。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.18321">原论文</a> · <a href="../../../../post-training/2609.18321-trajectory-learnability/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="GrowMTP: Can RL Grow Its Own Draft Head? LLM 后训练 WeChat AI, Tencent / Peking University 2026-09-15 在 RL rollout 内按被接受的草稿深度训练 MTP head，并与主干梯度解耦。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 depth-coupled acceptance loss；未报告 GPU 加速。本地执行 depth-coupled acceptance loss；未报告 GPU 加速。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  RL 训练加速 推测解码 LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-growmtp-d690b374">GrowMTP: Can RL Grow Its Own Draft Head?</h2>
<p class="ar-learning-card__meta">WeChat AI, Tencent / Peking University · 论文公开：2026-09-15</p>
<p><strong>方法要点：</strong>在 RL rollout 内按被接受的草稿深度训练 MTP head，并与主干梯度解耦。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 depth-coupled acceptance loss；未报告 GPU 加速。本地执行 depth-coupled acceptance loss；未报告 GPU 加速。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16648">原论文</a> · <a href="../../../../post-training/2609.16648-growmtp/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Know When to Stop, Where to Restart: Accelerating Multi-Turn Agentic On-Policy Distillation LLM 后训练 University of Science and Technology of China / Ant Group 2026-09-13 teacher 累积置信度越界时早停，并从最弱正确 turn 的缓存前缀重新开始。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 未复现大模型 rollout 吞吐。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行早停和前缀重启；未复现大模型 rollout 吞吐。本地执行早停和前缀重启；未复现大模型 rollout 吞吐。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  On-policy distillation 多轮加速 LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-stride-opd-55204229">Know When to Stop, Where to Restart: Accelerating Multi-Turn Agentic On-Policy Distillation</h2>
<p class="ar-learning-card__meta">University of Science and Technology of China / Ant Group · 论文公开：2026-09-13</p>
<p><strong>方法要点：</strong>teacher 累积置信度越界时早停，并从最弱正确 turn 的缓存前缀重新开始。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>未复现大模型 rollout 吞吐。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行早停和前缀重启；未复现大模型 rollout 吞吐。本地执行早停和前缀重启；未复现大模型 rollout 吞吐。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.14636">原论文</a> · <a href="../../../../post-training/2609.14636-stride-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Data-free On-policy Distillation LLM 后训练 Institute of Automation, Chinese Academy of Sciences / Tencent 2026-09-12 由教师在自身策略空间生成问题，减少对外部后训练语料的依赖。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行自生成问题的策略特征诊断；未生成自然语言训练集。本地执行自生成问题的策略特征诊断；未生成自然语言训练集。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  On-policy distillation 数据合成 LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-df-opd-48f2c181">Data-free On-policy Distillation</h2>
<p class="ar-learning-card__meta">Institute of Automation, Chinese Academy of Sciences / Tencent · 论文公开：2026-09-12</p>
<p><strong>方法要点：</strong>由教师在自身策略空间生成问题，减少对外部后训练语料的依赖。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行自生成问题的策略特征诊断；未生成自然语言训练集。本地执行自生成问题的策略特征诊断；未生成自然语言训练集。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.14193">原论文</a> · <a href="../../../../post-training/2609.14193-df-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="A Unified Per-Token Gating Family for On-Policy Distillation: FKL/RKL Mixing with Multi-Channel and Bias Coefficients LLM 后训练 Xiaohongshu 2026-09-10 把熵、不确定性、reference 偏移和教师—学生差距组合成逐 token gate，在 FKL/RKL 蒸馏方向间自适应分配。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行四信号 gate；结果仅是机制诊断，不把探索性结果写成稳定胜出。本地执行四信号 gate；结果仅是机制诊断，不把探索性结果写成稳定胜出。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  On-policy distillation 逐 token 自适应门控 LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-adaptive-opd-gate-493b3a1b">A Unified Per-Token Gating Family for On-Policy Distillation: FKL/RKL Mixing with Multi-Channel and Bias Coefficients</h2>
<p class="ar-learning-card__meta">Xiaohongshu · 论文公开：2026-09-10</p>
<p><strong>方法要点：</strong>把熵、不确定性、reference 偏移和教师—学生差距组合成逐 token gate，在 FKL/RKL 蒸馏方向间自适应分配。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行四信号 gate；结果仅是机制诊断，不把探索性结果写成稳定胜出。本地执行四信号 gate；结果仅是机制诊断，不把探索性结果写成稳定胜出。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11768">原论文</a> · <a href="../../../../post-training/2609.11768-adaptive-opd-gate/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="LOCUS: Task-Aware Low-Rank Post-Training for Token-Efficient Language Generation LLM 后训练 University of Washington 2026-09-10 学习任务相关低秩后训练子空间，只在紧凑方向上更新以缩短回答，同时保留任务能力。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地用样本特征 SVD 投影策略梯度；未训练论文规模语言模型。本地用样本特征 SVD 投影策略梯度；未训练论文规模语言模型。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  低秩后训练 Token 效率 LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-locus-5c47d1f6">LOCUS: Task-Aware Low-Rank Post-Training for Token-Efficient Language Generation</h2>
<p class="ar-learning-card__meta">University of Washington · 论文公开：2026-09-10</p>
<p><strong>方法要点：</strong>学习任务相关低秩后训练子空间，只在紧凑方向上更新以缩短回答，同时保留任务能力。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地用样本特征 SVD 投影策略梯度；未训练论文规模语言模型。本地用样本特征 SVD 投影策略梯度；未训练论文规模语言模型。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11739">原论文</a> · <a href="../../../../post-training/2609.11739-locus/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Extremely Sparse Supervision Incentivizes Reasoning Ability LLM 后训练 Amazon / Duke University 2026-09-03 常规 on-policy distillation 对生成轨迹的每个 token 使用教师分布。论文发现只挑一到两个关键位置、约占全部 token 的 0.05%，也能达到或超过全 token 训练。最大正差异 token 尤其有效，说明有效后训练可能更接近“反思关键步骤”而非逐字纠错。 复现级别：核心目标函数 mini-suite。复现级别：核心目标函数 mini-suite。在统一 OPD runner 中实现最大差异、最小差异和随机稀疏 token 选择。未执行 Qwen/Llama 全参数 OPD 或 PPO；当前方法不宣传 CUDA 路径，因此无需 GPU receipt。arithmetic-smoke、seeds 42/43/44 的监督位置数、监督比例、选择差异和目标值见 metrics/arithmetic-smoke-seeds42-44.json。  极稀疏 On-policy distillation LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-sparse-opd-2b68a2ae">Extremely Sparse Supervision Incentivizes Reasoning Ability</h2>
<p class="ar-learning-card__meta">Amazon / Duke University · 论文公开：2026-09-03</p>
<p><strong>方法要点：</strong>常规 on-policy distillation 对生成轨迹的每个 token 使用教师分布。论文发现只挑一到两个关键位置、约占全部 token 的 0.05%，也能达到或超过全 token 训练。最大正差异 token 尤其有效，说明有效后训练可能更接近“反思关键步骤”而非逐字纠错。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心目标函数 mini-suite。复现级别：核心目标函数 mini-suite。在统一 OPD runner 中实现最大差异、最小差异和随机稀疏 token 选择。未执行 Qwen/Llama 全参数 OPD 或 PPO；当前方法不宣传 CUDA 路径，因此无需 GPU receipt。arithmetic-smoke、seeds 42/43/44 的监督位置数、监督比例、选择差异和目标值见 metrics/arithmetic-smoke-seeds42-44.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04565">原论文</a> · <a href="../../../../post-training/2609.04565-sparse-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Optimizing What Policies Learn From: Recoverability-Aware Rollout Intervention Learning LLM 后训练 University of Notre Dame / Amazon 2026-08-05 主题：rollout 预算分配。均匀 rollout 浪费预算，静态启发式又跟不上策略变化。RAIL 把干预位置与方式视为 contextual bandit，并通过 shadow-to-live 轨迹学习 recoverability controller。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的 rollout 预算分配算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/arithmetic-smoke-seed42.json，不提交 checkpoint 或原始运行目录。  rollout 预算分配 LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-rail-7f7d9ac0">Optimizing What Policies Learn From: Recoverability-Aware Rollout Intervention Learning</h2>
<p class="ar-learning-card__meta">University of Notre Dame / Amazon · 论文公开：2026-08-05</p>
<p><strong>方法要点：</strong>主题：rollout 预算分配。均匀 rollout 浪费预算，静态启发式又跟不上策略变化。RAIL 把干预位置与方式视为 contextual bandit，并通过 shadow-to-live 轨迹学习 recoverability controller。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的 rollout 预算分配算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/arithmetic-smoke-seed42.json，不提交 checkpoint 或原始运行目录。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05080">原论文</a> · <a href="../../../../post-training/2608.05080-rail/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="SpecRoll: Fast-Slow Verifier-Feedback Adaptation for Speculative Reinforcement Learning Rollouts LLM 后训练 VNU University of Engineering and Technology / Viettel AI 2026-08-05 主题：RL rollout 加速。RL 中 target policy 持续变化，静态 drafter 很快过时。SpecRoll 用 future-token heads 提议、Reflex 做无反传的快速隐状态纠偏，并只在持续退化时启动慢速 head 更新；exact verifier 保持采样分布不变。 新版完整 GRPO 多模型实验不复现，审查已完成，现有 mini-suite 的证据等级不变。复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的 RL rollout 加速算子；不把确定性小型评测写成论文完整复现。版本边界（2026-10-15 复核）：本页与 specroll 保留原 v1 的 fast/slow 机制，不代表已经实现 v2 SPARK。v2 改为同一 prompt group 内共享、每轮重置的低秩 logit correction，并由 verifier 反馈更新、跨 rollout 学习投影；不能把旧 adapter 改名就算新版已接入。  RL rollout 加速 LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-specroll-077f92f9">SpecRoll: Fast-Slow Verifier-Feedback Adaptation for Speculative Reinforcement Learning Rollouts</h2>
<p class="ar-learning-card__meta">VNU University of Engineering and Technology / Viettel AI · 论文公开：2026-08-05</p>
<p><strong>方法要点：</strong>主题：RL rollout 加速。RL 中 target policy 持续变化，静态 drafter 很快过时。SpecRoll 用 future-token heads 提议、Reflex 做无反传的快速隐状态纠偏，并只在持续退化时启动慢速 head 更新；exact verifier 保持采样分布不变。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>新版完整 GRPO 多模型实验不复现，审查已完成，现有 mini-suite 的证据等级不变。复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的 RL rollout 加速算子；不把确定性小型评测写成论文完整复现。版本边界（2026-10-15 复核）：本页与 specroll 保留原 v1 的 fast/slow 机制，不代表已经实现 v2 SPARK。v2 改为同一 prompt group 内共享、每轮重置的低秩 logit correction，并由 verifier 反馈更新、跨 rollout 学习投影；不能把旧 adapter 改名就算新版已接入。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04962">原论文</a> · <a href="../../../../post-training/2608.04962-specroll/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="CoBA-RL LLM 后训练 Zhejiang University 2026-06-21 普通 RLVR 可能只重新分配 base model 已有轨迹的概率，提升 pass@1 却不扩展高采样 pass@k 所反映的能力边界。该方法先用多次采样估计边界，在边界附近/之外注入教师推理，再用 RL 巩固。 定位当前能力边界，对边界附近样本提供教师引导，再用 RL 固化新增推理模式。实现了边界状态、难度课程、真实教师触发、自由生成 RL、pass@k/教师缓存与成本曲线；本地 teacher 只有 0.5B，且最高只统计 pass@8，没有运行论文规模 pass@256 或同规模学生，因此不能宣称复现论文中的能力边界增量。本地算术 suite 带可复现难度；训练器维护动态 curriculum boundary、采样边界样本，无正确 rollout 时调用固定 revision 的真实 causal-LM teacher，并把教师 completion 以小权重 SFT 项注入 sequence RL。  能力边界课程 LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-coba-rl-1893eb3e">CoBA-RL</h2>
<p class="ar-learning-card__meta">Zhejiang University · 论文公开：2026-06-21</p>
<p><strong>方法要点：</strong>普通 RLVR 可能只重新分配 base model 已有轨迹的概率，提升 pass@1 却不扩展高采样 pass@k 所反映的能力边界。该方法先用多次采样估计边界，在边界附近/之外注入教师推理，再用 RL 巩固。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>定位当前能力边界，对边界附近样本提供教师引导，再用 RL 固化新增推理模式。实现了边界状态、难度课程、真实教师触发、自由生成 RL、pass@k/教师缓存与成本曲线；本地 teacher 只有 0.5B，且最高只统计 pass@8，没有运行论文规模 pass@256 或同规模学生，因此不能宣称复现论文中的能力边界增量。本地算术 suite 带可复现难度；训练器维护动态 curriculum boundary、采样边界样本，无正确 rollout 时调用固定 revision 的真实 causal-LM teacher，并把教师 completion 以小权重 SFT 项注入 sequence RL。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.22317">原论文</a> · <a href="../../../../post-training/2606.22317-coba-rl/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Beyond GRPO and On-Policy Distillation: An Empirical Sparse-to-Dense Reward Principle for Language-Model Post-Training LLM 后训练 LinkedIn 2026-05-12 Sec.2–3四阶段工作流和等标签预算经验对照是本论文核心；FKL在teacher occupancy、OPD在student occupancy，教师冻结且需共享tokenizer。库中已有GRPO/OPD/KL算子不等于本文完整流程；不重复包装通用KL或把四个状态标签称为复现。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。状态：仅文献与成本收录，没有可执行能力adapter，不以heuristic冒充核心模型。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本轮不提供可运行模型、loss包装或伪测试。库里已有通用KL/RL/统计工具并不构成本文核心流程；原文语义模型、API多轮生成或大规模训练不能用手工规则替换。仅保存经过核验的方法、资源、源码状态与原图，终态为 not_reproduced_high_cost。后续不得自动移回待训练队列。  训练流程与资源分配 Teacher RL与FKL-to-OPD LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-sparse-to-dense-reward-principle-66732323">Beyond GRPO and On-Policy Distillation: An Empirical Sparse-to-Dense Reward Principle for Language-Model Post-Training</h2>
<p class="ar-learning-card__meta">LinkedIn · 论文公开：2026-05-12</p>
<p><strong>方法要点：</strong>Sec.2–3四阶段工作流和等标签预算经验对照是本论文核心；FKL在teacher occupancy、OPD在student occupancy，教师冻结且需共享tokenizer。库中已有GRPO/OPD/KL算子不等于本文完整流程；不重复包装通用KL或把四个状态标签称为复现。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。状态：仅文献与成本收录，没有可执行能力adapter，不以heuristic冒充核心模型。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本轮不提供可运行模型、loss包装或伪测试。库里已有通用KL/RL/统计工具并不构成本文核心流程；原文语义模型、API多轮生成或大规模训练不能用手工规则替换。仅保存经过核验的方法、资源、源码状态与原图，终态为 not_reproduced_high_cost。后续不得自动移回待训练队列。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.12483v1">原论文</a> · <a href="../../../../post-training/2605.12483-sparse-to-dense-reward-principle/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Lightning OPD LLM 后训练 MIT HAN Lab 2026-04-14 传统在线蒸馏在每一步训练都调用教师，吞吐和成本受教师推理限制。Lightning OPD 先让学生在 SFT 数据上产生 on-policy rollout，再由同一个教师一次性计算 token 分布并缓存。训练只读取缓存，因此保留学生分布上的蒸馏信号，又不需要训练期在线教师。 保真度：本地实现复现教师预填充、teacher consistency 和训练期零在线教师调用；保真度：本地实现复现教师预填充、teacher consistency 和训练期零在线教师调用；当前使用候选策略验证机制，不等同于论文的 Qwen3 全参数训练。当前没有训练真实 Qwen3、token-level vocabulary distribution 或复跑 AIME；因此只能证明缓存式 OPD 数据流和教师调用约束成立，不能把本地 accuracy 与论文 AIME 数字比较。实现先为全部训练候选缓存教师概率，保存 teacher_prefill_calls 和 teacher_cache_entries；  On-policy distillation LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-lightning-opd-b1670874">Lightning OPD</h2>
<p class="ar-learning-card__meta">MIT HAN Lab · 论文公开：2026-04-14</p>
<p><strong>方法要点：</strong>传统在线蒸馏在每一步训练都调用教师，吞吐和成本受教师推理限制。Lightning OPD 先让学生在 SFT 数据上产生 on-policy rollout，再由同一个教师一次性计算 token 分布并缓存。训练只读取缓存，因此保留学生分布上的蒸馏信号，又不需要训练期在线教师。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：本地实现复现教师预填充、teacher consistency 和训练期零在线教师调用；保真度：本地实现复现教师预填充、teacher consistency 和训练期零在线教师调用；当前使用候选策略验证机制，不等同于论文的 Qwen3 全参数训练。当前没有训练真实 Qwen3、token-level vocabulary distribution 或复跑 AIME；因此只能证明缓存式 OPD 数据流和教师调用约束成立，不能把本地 accuracy 与论文 AIME 数字比较。实现先为全部训练候选缓存教师概率，保存 teacher_prefill_calls 和 teacher_cache_entries；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.13010">原论文</a> · <a href="../../../../post-training/2604.13010-lightning-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Large Reasoning Models Struggle to Transfer Parametric Knowledge Across Scripts LLM 后训练 Google Research 2026-03-17 Sec.4–6与Appendix A/H：观察性回归、训练专用entity提示干预和真实LoRA是定义性路径。不能把正则音译、手工插提示或小分类器当成其LLM知识检索机制。本文不是新闭式RL loss；本轮仅文献收录，不强造operator。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。状态：仅文献与成本收录，没有可执行能力adapter，不以heuristic冒充核心模型。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本轮不提供可运行模型、loss包装或伪测试。库里已有通用KL/RL/统计工具并不构成本文核心流程；原文语义模型、API多轮生成或大规模训练不能用手工规则替换。仅保存经过核验的方法、资源、源码状态与原图，终态为 not_reproduced_high_cost。后续不得自动移回待训练队列。  多语言后训练 跨文字系统知识迁移 LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-cross-script-knowledge-transfer-cff708b0">Large Reasoning Models Struggle to Transfer Parametric Knowledge Across Scripts</h2>
<p class="ar-learning-card__meta">Google Research · 论文公开：2026-03-17</p>
<p><strong>方法要点：</strong>Sec.4–6与Appendix A/H：观察性回归、训练专用entity提示干预和真实LoRA是定义性路径。不能把正则音译、手工插提示或小分类器当成其LLM知识检索机制。本文不是新闭式RL loss；本轮仅文献收录，不强造operator。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。状态：仅文献与成本收录，没有可执行能力adapter，不以heuristic冒充核心模型。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本轮不提供可运行模型、loss包装或伪测试。库里已有通用KL/RL/统计工具并不构成本文核心流程；原文语义模型、API多轮生成或大规模训练不能用手工规则替换。仅保存经过核验的方法、资源、源码状态与原图，终态为 not_reproduced_high_cost。后续不得自动移回待训练队列。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.17070v1">原论文</a> · <a href="../../../../post-training/2603.17070-cross-script-knowledge-transfer/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Prompt-Level Distillation: A Non-Parametric Alternative to Model Fine-Tuning for Efficient Reasoning LLM 后训练 Google 2026-02-24 PLD 不微调学生参数，而把教师推理抽象为可审查的系统指令：先用带标签训练样本提取微规则，经语义向量 DBSCAN 去掉噪声、合成规则，再根据训练错误修订冲突。学生最终使用整理后的规则，不读取每个测试样本的答案。图按原文 Figure 1 重绘。原始流程图。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。§4.1 使用 Gemini 3 Flash thinking 提取、Gemini 3 Pro thinking 合成和修复、Gemini Embedding 聚类，学生含 Gemma-3 4B / Gemini 2 Flash。多阶段闭源调用与完整多任务评测成本无法廉价固定，成本过高，不复现（审查 DONE），不下载模型探成本。  Context distillation 提示级非参数蒸馏 LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-prompt-level-distillation-91a64214">Prompt-Level Distillation: A Non-Parametric Alternative to Model Fine-Tuning for Efficient Reasoning</h2>
<p class="ar-learning-card__meta">Google · 论文公开：2026-02-24</p>
<p><strong>方法要点：</strong>PLD 不微调学生参数，而把教师推理抽象为可审查的系统指令：先用带标签训练样本提取微规则，经语义向量 DBSCAN 去掉噪声、合成规则，再根据训练错误修订冲突。学生最终使用整理后的规则，不读取每个测试样本的答案。图按原文 Figure 1 重绘。原始流程图。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。§4.1 使用 Gemini 3 Flash thinking 提取、Gemini 3 Pro thinking 合成和修复、Gemini Embedding 聚类，学生含 Gemma-3 4B / Gemini 2 Flash。多阶段闭源调用与完整多任务评测成本无法廉价固定，成本过高，不复现（审查 DONE），不下载模型探成本。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.21103v1">原论文</a> · <a href="../../../../post-training/2602.21103-prompt-level-distillation/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="CHORD LLM 后训练 Alibaba Group 2025-08-15 将 SFT 与 RL 串成两个独立阶段会造成 expert data 的过拟合或过早遗忘。CHORD 把专家 SFT 作为 on-policy RL 中动态退火的辅助目标，并以 token 级不确定性权重平滑从模仿过渡到探索。 本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地不训练 LLM token-level uncertainty model，gold candidate 仅是确定性 expert 代理。把 verified gold candidate 作为 expert trace，真实按训练进度退火 SFT 项并与 on-policy group-RL 梯度相加。  SFT-RL 动态混合 LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-chord-f1e12f5e">CHORD</h2>
<p class="ar-learning-card__meta">Alibaba Group · 论文公开：2025-08-15</p>
<p><strong>方法要点：</strong>将 SFT 与 RL 串成两个独立阶段会造成 expert data 的过拟合或过早遗忘。CHORD 把专家 SFT 作为 on-policy RL 中动态退火的辅助目标，并以 token 级不确定性权重平滑从模仿过渡到探索。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。本地不训练 LLM token-level uncertainty model，gold candidate 仅是确定性 expert 代理。把 verified gold candidate 作为 expert trace，真实按训练进度退火 SFT 项并与 on-policy group-RL 梯度相加。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.11408">原论文</a> · <a href="../../../../post-training/2508.11408-chord/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="SPIRAL LLM 后训练 Apple 2025-06-30 同一模型扮演出题者和解题者，在可自动判定的零和多轮语言游戏中形成逐步变难的课程。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.3438（+46.67%）；奖励、KL、长度和候选预算一致。  自博弈课程 LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-spiral-8df7f07c">SPIRAL</h2>
<p class="ar-learning-card__meta">Apple · 论文公开：2025-06-30</p>
<p><strong>方法要点：</strong>同一模型扮演出题者和解题者，在可自动判定的零和多轮语言游戏中形成逐步变难的课程。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.3438（+46.67%）；奖励、KL、长度和候选预算一致。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2506.24119">原论文</a> · <a href="../../../../post-training/2506.24119-spiral/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="Absolute Zero LLM 后训练 Tsinghua University 2025-05-06 proposer 自己生成可验证任务，solver 求解，程序 verifier 提供奖励；按当前能力边界组织课程。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.5938（+153.33%）；奖励、KL、长度和候选预算一致。  零数据自博弈 LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-absolute-zero-7e819456">Absolute Zero</h2>
<p class="ar-learning-card__meta">Tsinghua University · 论文公开：2025-05-06</p>
<p><strong>方法要点：</strong>proposer 自己生成可验证任务，solver 求解，程序 verifier 提供奖励；按当前能力边界组织课程。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy 0.2344 → 0.5938（+153.33%）；奖励、KL、长度和候选预算一致。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.03335">原论文</a> · <a href="../../../../post-training/2505.03335-absolute-zero/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/data-and-budget" data-search="RAFT LLM 后训练 HKUST 2023-04-13 PPO 的在线更新不稳定，而在固定 SFT 数据上训练又无法持续利用变好的策略。RAFT 每轮从当前模型生成多个响应，用 reward model 排序并丢弃低质量样本，只对选中的高质量响应执行普通 maximum-likelihood fine-tuning，然后用新策略进入下一轮。 未训练真实生成式 LLM/reward model，也未复刻扩散模型实验。本页实现“当前策略采样 → reward 选优 → 只在保留响应上 SFT → 再采样”的迭代 rejection-sampling 路径，和 RRHF 的全排序 loss 分开。实现在线采样、reward ranking、top-response filtering 和迭代 SFT；未训练真实生成式 LLM/reward model，也未复刻扩散模型实验。候选策略结果只验证算法状态转移。公开 GSM8K candidate 512/128、300 steps、seed 42；  Reward 选优微调 LLM 后训练 数据与预算：下一份算力花在哪里">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 数据与预算：下一份算力花在哪里</a></p>
<h2 id="paper-post-training-raft-fe9d648c">RAFT</h2>
<p class="ar-learning-card__meta">HKUST · 论文公开：2023-04-13</p>
<p><strong>方法要点：</strong>PPO 的在线更新不稳定，而在固定 SFT 数据上训练又无法持续利用变好的策略。RAFT 每轮从当前模型生成多个响应，用 reward model 排序并丢弃低质量样本，只对选中的高质量响应执行普通 maximum-likelihood fine-tuning，然后用新策略进入下一轮。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>未训练真实生成式 LLM/reward model，也未复刻扩散模型实验。本页实现“当前策略采样 → reward 选优 → 只在保留响应上 SFT → 再采样”的迭代 rejection-sampling 路径，和 RRHF 的全排序 loss 分开。实现在线采样、reward ranking、top-response filtering 和迭代 SFT；未训练真实生成式 LLM/reward model，也未复刻扩散模型实验。候选策略结果只验证算法状态转移。公开 GSM8K candidate 512/128、300 steps、seed 42；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2304.06767">原论文</a> · <a href="../../../../post-training/2304.06767-raft/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
