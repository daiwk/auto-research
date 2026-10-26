---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 在策略蒸馏：沿学生实际走过的前缀学习

[LLM 后训练](index.md) / 子主题导学 · 约 3 分钟 · 40 张论文卡

## 先想一个问题

学生总在自己的错误前缀上继续生成，为什么只模仿教师完整答案可能教不到那里？

## 记住这一点

自回归学生在推理时会访问自己的前缀。GKD让学生先生成，再由教师在这些状态上提供分布监督，缩小训练与使用状态的差距；MiniLLM说明散度方向也会改变学生如何覆盖教师概率质量。这组先关注轨迹从哪里来、师生是否看到相同生成前缀，以及怎样把分布差异变成更新信号。

## 一个例子

教学例子：教师答案是“先求面积再求比例”，学生先写了一个错误公式。仅在教师前缀上做SFT，可能没教过学生从错误公式如何继续。OPD可在学生这个前缀上重新查询教师分布；但教师也可能跟随错误前缀，所以状态覆盖改善并不自动保证监督正确。还需关注教师能力、散度和验证信号。

## 什么时候要小心

在学生轨迹上评分不等于教师重新生成一条答案，也不保证学生能学到教师所有能力。KL数值、有限梯度或候选分布诊断只支持局部机制；本库GKD/MiniLLM的轻量实现不等于原论文checkpoint训练。多seed数值检查不会自动成为正式能力比较。

## 先读这几篇

先读GKD，把采样前缀与教师评分画成两条线；再读MiniLLM，比较散度方向及采样稳定化；最后读Learning Signals，区分损失尚大与真正仍有有效学习方向。

1. [GKD](../../../post-training/2306.13649-gkd/README.md) · [原论文](https://arxiv.org/abs/2306.13649)
2. [MiniLLM](../../../post-training/2306.08543-minillm/README.md) · [原论文](https://arxiv.org/abs/2306.08543)
3. [Why On-Policy Distillation Sometimes Fails: Vanishing Learning Signals](../../../post-training/2610.11247-opd-learning-signals/README.md) · [原论文](https://arxiv.org/abs/2610.11247)

## 自测一下

把缓存的教师答案重复训练十遍，是否就获得了学生在策略数据？

??? note "展开参考答案"

    没有。数据仍来自固定教师轨迹。需要辨认是否由当前或指定学生策略采样、是否在学生前缀上取得教师监督；若复用离线学生轨迹，还要单独讨论分布漂移和更新口径，不能仅因数据名称含student就称为当前on-policy。

## 这个子主题的论文卡片

导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">
<div class="ar-learning-controls">
<label for="learning-search">搜索卡片
<input id="learning-search" type="search" data-learning-search placeholder="搜索论文、机制、机构或本地边界"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">共 40 张卡片</p>
<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="On-Policy Self-Training: Data-Free Self-Improvement in Large Language Models LLM 后训练 Google 2026-10-23 通常的 on-policy self-distillation 仍需要人工问题集。OPST 按主题自生成问题和特权解题线索，经独立重答、改写与学生难度门过滤，再由额外看到线索的 EMA 教师在学生实际生成的前缀上提供分布监督，而不是要求学生直接模仿生成器表述。过滤分为两个方向：生成器在不含的新上下文中重答原题及保义改写题，两次都须匹配候选答案；学生的条 rollout 只有全部匹配候选答案时才作为过易题丢弃。“全部答成另一个答案”不能被泛化的 consensus 规则误删。 成本过高，不复现（审查 DONE）；诊断直接使用合成 divergence 张量，不称为 OPST loss 复现。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  On-policy distillation 自生成课程与EMA教师 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-opst-37fdd7dd">On-Policy Self-Training: Data-Free Self-Improvement in Large Language Models</h2>
<p class="ar-learning-card__meta">Google · 论文公开：2026-10-23</p>
<p><strong>方法要点：</strong>通常的 on-policy self-distillation 仍需要人工问题集。OPST 按主题自生成问题和特权解题线索，经独立重答、改写与学生难度门过滤，再由额外看到线索的 EMA 教师在学生实际生成的前缀上提供分布监督，而不是要求学生直接模仿生成器表述。过滤分为两个方向：生成器在不含的新上下文中重答原题及保义改写题，两次都须匹配候选答案；学生的条 rollout 只有全部匹配候选答案时才作为过易题丢弃。“全部答成另一个答案”不能被泛化的 consensus 规则误删。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）；诊断直接使用合成 divergence 张量，不称为 OPST loss 复现。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32770v1">原论文</a> · <a href="../../../../post-training/2610.32770-opst/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="GIFT: Gradient Informed Filtering for Distillation Augmented Reasoning RL LLM 后训练 Shanghai Jiao Tong University 2026-10-22 终局正确性驱动的 RL 梯度与教师模仿梯度可能相冲突。GIFT 在原始词表 logits 空间分解两者：先最少纳入冲突 token，再优先保留提供正交新方向的教师监督；训练逐步缩减被蒸馏的 token 数量，保留项的强度不稀释。 完整实验：成本过高，不复现（审查 DONE）。它是数值诊断，不是可晋级 Agent，也无 validation 选模 / test 能力评估。本地状态：L1 精确损失组件，diagnostic only。保留 token 级梯度几何、exact-quota 排序、coverage annealing 与 sparse top-k+tail KL；不是完整推理能力复现。完整实验：成本过高，不复现（审查 DONE）。gift_loss 实现一个 actor training sub-batch、单位 rollout IS 权重下的 clipped GRPO 与 GIFT。  On-policy distillation RL与蒸馏梯度几何 后训练算法组件 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-gift-0ba87e11">GIFT: Gradient Informed Filtering for Distillation Augmented Reasoning RL</h2>
<p class="ar-learning-card__meta">Shanghai Jiao Tong University · 论文公开：2026-10-22</p>
<p><strong>方法要点：</strong>终局正确性驱动的 RL 梯度与教师模仿梯度可能相冲突。GIFT 在原始词表 logits 空间分解两者：先最少纳入冲突 token，再优先保留提供正交新方向的教师监督；训练逐步缩减被蒸馏的 token 数量，保留项的强度不稀释。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验：成本过高，不复现（审查 DONE）。它是数值诊断，不是可晋级 Agent，也无 validation 选模 / test 能力评估。本地状态：L1 精确损失组件，diagnostic only。保留 token 级梯度几何、exact-quota 排序、coverage annealing 与 sparse top-k+tail KL；不是完整推理能力复现。完整实验：成本过高，不复现（审查 DONE）。gift_loss 实现一个 actor training sub-batch、单位 rollout IS 权重下的 clipped GRPO 与 GIFT。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30796v1">原论文</a> · <a href="../../../../post-training/2610.30796-gift/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="UserArena: Benchmarking Interactive User Simulation for Long-Horizon Shopping Agents LLM 后训练 Leiden University 2026-10-22 逐步动作命中率不能说明用户模拟器能否保持跨会话偏好，更不能说明模拟出来的推荐政策差异是否接近真实生产A/B。UserArena把细粒度页面、动作和跨会话记录统一成13种动作环境，分Replay与Rollout评估五层保真度：可执行性、局部行为、轨迹动态、个体群体差异和最终结果。OPTD的区别不是“直接给学生看未来轨迹”。完整训练轨迹先被提炼成抽象偏好、顾虑和比较准则，只提供给冻结教师；教师在学生自己生成的前缀上给完整词表分布。 完整实验：成本过高，不复现（审查 DONE），不自动重试。本地状态：L1 精确损失组件，diagnostic only；不是用户模拟器、购物环境或官方 benchmark 接入。完整实验：成本过高，不复现（审查 DONE），不自动重试。实现Eq.5–10完整词表几何目标、逐token二分、广义JSD、独立GT grounding、两级均值和教师detach。接受两组不同长度的学生logits；padding可含NaN但不贡献损失/梯度，有效位置必须有限、词表和配对状态必须对齐。FP16/BF16提升到FP32计算，非法空响应、越界gold与不合法预算直接拒绝。  On-policy distillation 轨迹意图与逐token信任域 Agent用户模拟 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-userarena-optd-fa417c42">UserArena: Benchmarking Interactive User Simulation for Long-Horizon Shopping Agents</h2>
<p class="ar-learning-card__meta">Leiden University · 论文公开：2026-10-22</p>
<p><strong>方法要点：</strong>逐步动作命中率不能说明用户模拟器能否保持跨会话偏好，更不能说明模拟出来的推荐政策差异是否接近真实生产A/B。UserArena把细粒度页面、动作和跨会话记录统一成13种动作环境，分Replay与Rollout评估五层保真度：可执行性、局部行为、轨迹动态、个体群体差异和最终结果。OPTD的区别不是“直接给学生看未来轨迹”。完整训练轨迹先被提炼成抽象偏好、顾虑和比较准则，只提供给冻结教师；教师在学生自己生成的前缀上给完整词表分布。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验：成本过高，不复现（审查 DONE），不自动重试。本地状态：L1 精确损失组件，diagnostic only；不是用户模拟器、购物环境或官方 benchmark 接入。完整实验：成本过高，不复现（审查 DONE），不自动重试。实现Eq.5–10完整词表几何目标、逐token二分、广义JSD、独立GT grounding、两级均值和教师detach。接受两组不同长度的学生logits；padding可含NaN但不贡献损失/梯度，有效位置必须有限、词表和配对状态必须对齐。FP16/BF16提升到FP32计算，非法空响应、越界gold与不合法预算直接拒绝。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30932v1">原论文</a> · <a href="../../../../post-training/2610.30932-userarena-optd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Adaptive Pullback: Reweighting Supervision at Penalty Jumps in On-Policy Distillation LLM 后训练 Nanjing University 2026-10-20 同样高的 OPD 惩罚可能是持续稳定的，也可能刚刚突增。AP-OPD 用相邻 token 块定位后一种情况，再把突增后整块监督按一个比率回拉；不增加教师 forward，不改变 token 系数的正负。均值和检测器始终读取原始、未加权统计，不能递归使用已回拉的前块。 完整实验成本过高，不复现（审查 DONE）；诊断响应长 10，块长缩为 2 以覆盖多个边界；L1 定义性损失组件，不是数学或代码能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接入 Evolve。无下载。随机初始化 12-token、8 维因果 GRU 策略实际采样响应，独立冻结教师在相同前缀重放，默认每 seed 3 次 SGD。诊断响应长 10，块长缩为 2 以覆盖多个边界；通用算子默认仍是论文。合成 token 不代表自然语言数学能力，输出不可覆盖，CUDA 不可用不回退。  On-policy distillation 蒸馏信号门控与训练稳定性 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-ap-opd-602f5990">Adaptive Pullback: Reweighting Supervision at Penalty Jumps in On-Policy Distillation</h2>
<p class="ar-learning-card__meta">Nanjing University · 论文公开：2026-10-20</p>
<p><strong>方法要点：</strong>同样高的 OPD 惩罚可能是持续稳定的，也可能刚刚突增。AP-OPD 用相邻 token 块定位后一种情况，再把突增后整块监督按一个比率回拉；不增加教师 forward，不改变 token 系数的正负。均值和检测器始终读取原始、未加权统计，不能递归使用已回拉的前块。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）；诊断响应长 10，块长缩为 2 以覆盖多个边界；L1 定义性损失组件，不是数学或代码能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接入 Evolve。无下载。随机初始化 12-token、8 维因果 GRU 策略实际采样响应，独立冻结教师在相同前缀重放，默认每 seed 3 次 SGD。诊断响应长 10，块长缩为 2 以覆盖多个边界；通用算子默认仍是论文。合成 token 不代表自然语言数学能力，输出不可覆盖，CUDA 不可用不回退。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28194v1">原论文</a> · <a href="../../../../post-training/2610.28194-ap-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="On-Policy Transition Distillation LLM 后训练 The Hong Kong Polytechnic University 2026-10-20 最终层分布接近教师，不一定代表模型沿深度修正预测的方式接近教师。OPTD 保留最终层 OPD，再对选定浅到深 readout 的 log 概率增量施加监督。候选 token 在最终学生层选定后，全路径保持同一身份；不是每层独立 top-k，也不是隐状态 MSE。 完整实验成本过高，不复现（审查 DONE）；诊断 top-k 缩为 5，通用算子默认论文 16；L1 定义性损失组件，不是推理或代码能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接入 Evolve。无下载。随机 12-token 因果 GRU 加三个 residual-depth block，以同一个最终 LayerNorm/unembedding 构成四层 readout；实际学生采样、冻结教师同前缀重放，默认三次 SGD。诊断 top-k 缩为 5，通用算子默认论文 16；不声称该微型网络是论文 Transformer。CUDA 不可用不回退，输出不可覆盖。  On-policy distillation 层间预测转移蒸馏 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-optd-ae85339e">On-Policy Transition Distillation</h2>
<p class="ar-learning-card__meta">The Hong Kong Polytechnic University · 论文公开：2026-10-20</p>
<p><strong>方法要点：</strong>最终层分布接近教师，不一定代表模型沿深度修正预测的方式接近教师。OPTD 保留最终层 OPD，再对选定浅到深 readout 的 log 概率增量施加监督。候选 token 在最终学生层选定后，全路径保持同一身份；不是每层独立 top-k，也不是隐状态 MSE。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）；诊断 top-k 缩为 5，通用算子默认论文 16；L1 定义性损失组件，不是推理或代码能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接入 Evolve。无下载。随机 12-token 因果 GRU 加三个 residual-depth block，以同一个最终 LayerNorm/unembedding 构成四层 readout；实际学生采样、冻结教师同前缀重放，默认三次 SGD。诊断 top-k 缩为 5，通用算子默认论文 16；不声称该微型网络是论文 Transformer。CUDA 不可用不回退，输出不可覆盖。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28048v1">原论文</a> · <a href="../../../../post-training/2610.28048-optd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Projected Distillation: On Learning to Solve Hard Problems from Close, Correct Targets LLM 后训练 University of Massachusetts 2026-10-20 困难问题的学生 rollout 可能全错，RL 得不到成功奖励；直接拟合外部完整答案又过于 off-policy。论文用 projector 最小改写学生的错误响应，经 verifier 接受后，只在变化片段做 DPO；学生自己答对的响应单独做 SFT，每轮重新采样和纠错。最小编辑只是“学生最可能生成的正确响应”的可计算近似，不保证是该优化问题的精确解。 完整实验成本过高，不复现（审查 DONE）。L1 编辑对齐、验证接口和损失公式诊断，不是语言纠错或在线闭环复现。L1 编辑对齐、验证接口和损失公式诊断，不是语言纠错或在线闭环复现。不可晋级、未接入 Evolve。完整实验成本过高，不复现（审查 DONE）。本页属于同一 10 月 21 日公告的补审。无下载和预训练模型调用。输入为合成 token pair 与随机 logits；测试用的显式 verifier 只验证已给定夹具，不扮演语言 projector。单次对齐最多一百万动态规划格，避免该诊断入口无界占内存；真实长文本流水线不在本轮范围。输出不可覆盖、最多三个 seed，CUDA 不回退。  On-policy distillation 最小修正与偏好学习 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-projected-distillation-64e08dbb">Projected Distillation: On Learning to Solve Hard Problems from Close, Correct Targets</h2>
<p class="ar-learning-card__meta">University of Massachusetts · 论文公开：2026-10-20</p>
<p><strong>方法要点：</strong>困难问题的学生 rollout 可能全错，RL 得不到成功奖励；直接拟合外部完整答案又过于 off-policy。论文用 projector 最小改写学生的错误响应，经 verifier 接受后，只在变化片段做 DPO；学生自己答对的响应单独做 SFT，每轮重新采样和纠错。最小编辑只是“学生最可能生成的正确响应”的可计算近似，不保证是该优化问题的精确解。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）。L1 编辑对齐、验证接口和损失公式诊断，不是语言纠错或在线闭环复现。L1 编辑对齐、验证接口和损失公式诊断，不是语言纠错或在线闭环复现。不可晋级、未接入 Evolve。完整实验成本过高，不复现（审查 DONE）。本页属于同一 10 月 21 日公告的补审。无下载和预训练模型调用。输入为合成 token pair 与随机 logits；测试用的显式 verifier 只验证已给定夹具，不扮演语言 projector。单次对齐最多一百万动态规划格，避免该诊断入口无界占内存；真实长文本流水线不在本轮范围。输出不可覆盖、最多三个 seed，CUDA 不回退。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.27467v1">原论文</a> · <a href="../../../../post-training/2610.27467-projected-distillation/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="GR-OPD: Group-Relative Sequence Credit for On-Policy Distillation LLM 后训练 Shanghai Jiao Tong University 2026-10-16 教师在每个 token 上更自信，不一定意味着整段推理更值得复制；教师与学生的推理模式不同还可能造成训练崩溃。GR-OPD 在学生轨迹上重放教师，把 log-prob 差聚合为序列分数，在同题回答之间分配相对信用；保留一部分组均值压力，以免纯中心化抹掉教师总体偏好，然后使用 clipped PPO 更新。原文方法原图建议：Figure 2 总览，保留折扣、组相对信用与广播三个阶段。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是数学推理能力复现。L1 定义性组件／梯度诊断，不是数学推理能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接 Evolve。随机初始化16词表、8维因果 GRU，教师单独随机初始化后冻结；旧学生实际为每个公开 prompt 采样长度2、3、4的回答，教师重放同一学生轨迹。不同长度用于检查逐响应均值，不提供预置候选或 gold 答案。  On-policy distillation 过程奖励与信用分配 后训练算法组件 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-gr-opd-372c128f">GR-OPD: Group-Relative Sequence Credit for On-Policy Distillation</h2>
<p class="ar-learning-card__meta">Shanghai Jiao Tong University · 论文公开：2026-10-16</p>
<p><strong>方法要点：</strong>教师在每个 token 上更自信，不一定意味着整段推理更值得复制；教师与学生的推理模式不同还可能造成训练崩溃。GR-OPD 在学生轨迹上重放教师，把 log-prob 差聚合为序列分数，在同题回答之间分配相对信用；保留一部分组均值压力，以免纯中心化抹掉教师总体偏好，然后使用 clipped PPO 更新。原文方法原图建议：Figure 2 总览，保留折扣、组相对信用与广播三个阶段。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是数学推理能力复现。L1 定义性组件／梯度诊断，不是数学推理能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接 Evolve。随机初始化16词表、8维因果 GRU，教师单独随机初始化后冻结；旧学生实际为每个公开 prompt 采样长度2、3、4的回答，教师重放同一学生轨迹。不同长度用于检查逐响应均值，不提供预置候选或 gold 答案。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23042v1">原论文</a> · <a href="../../../../post-training/2610.23042-gr-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="SimOPD: Relational Knowledge Transfer for On-Policy Distillation LLM 后训练 Zhejiang University 2026-10-16 概率蒸馏只利用输出分布，直接匹配隐状态又要求学生迁就教师的坐标和维数。SimOPD 改为比较回答之间的关系：两模型分别编码同一批学生回答，在自己的空间里计算“当前回答与历史回答有多像”，再匹配这两个相似度分布。教师和学生维数可不同，不需要跨模型投影。原文 §3及算法1 原图建议：Figure 2 方法图，重点保留 paired bank 和两个独立表示空间。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是大模型知识迁移结果。L1 定义性组件／梯度诊断，不是大模型知识迁移结果。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接 Evolve。随机初始化16词表因果 GRU，学生8维、冻结教师12维，选择 embedding 和循环状态两个层次。学生实际自回归生成回答，教师读取同一公开 prompt 与回答，不提供人工 gold 或教师生成的替代回答。每批4个回答，bank容量6，首批暖启动，之后默认3次真实优化更新。随机教师仅用来检查关系蒸馏路径，不具备预训练知识或自然语言教师能力。  On-policy distillation 跨模型表示蒸馏 后训练算法组件 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-simopd-1a5a0435">SimOPD: Relational Knowledge Transfer for On-Policy Distillation</h2>
<p class="ar-learning-card__meta">Zhejiang University · 论文公开：2026-10-16</p>
<p><strong>方法要点：</strong>概率蒸馏只利用输出分布，直接匹配隐状态又要求学生迁就教师的坐标和维数。SimOPD 改为比较回答之间的关系：两模型分别编码同一批学生回答，在自己的空间里计算“当前回答与历史回答有多像”，再匹配这两个相似度分布。教师和学生维数可不同，不需要跨模型投影。原文 §3及算法1 原图建议：Figure 2 方法图，重点保留 paired bank 和两个独立表示空间。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是大模型知识迁移结果。L1 定义性组件／梯度诊断，不是大模型知识迁移结果。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接 Evolve。随机初始化16词表因果 GRU，学生8维、冻结教师12维，选择 embedding 和循环状态两个层次。学生实际自回归生成回答，教师读取同一公开 prompt 与回答，不提供人工 gold 或教师生成的替代回答。每批4个回答，bank容量6，首批暖启动，之后默认3次真实优化更新。随机教师仅用来检查关系蒸馏路径，不具备预训练知识或自然语言教师能力。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23306v1">原论文</a> · <a href="../../../../post-training/2610.23306-simopd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Divergence-Routed On-Policy Distillation for Language Models LLM 后训练 Peking University 2026-10-14 DrOPD 在学生自己生成的轨迹上比较师生分布，以 JS 散度识别教师支持而学生严重欠覆盖的位置。它在所有位置保留 reverse-KL，并仅向高分歧位置增加 forward-KL 的纠正信号，通过候选级优势执行 PPO clipped 更新。reverse-KL 的 logit 梯度包含学生概率因子，学生几乎不给某个教师 token 概率时，纠正信号会变弱。forward-KL 的梯度为学生与教师概率之差，能继续推动这些教师模式；路由限制额外监督的位置，而不是直接把整个损失换成 forward-KL。 完整论文训练成本过高，不复现（审查 DONE）。L1 算法组件与真实在线更新诊断。L1 算法组件与真实在线更新诊断。本地执行候选并集、JS 路由和 PPO 更新；完整论文训练成本过高，不复现（审查 DONE）。与 Dr. OPD（2609.38025） 是不同论文，方法键不复用。微型 byte 自回归模型在固定公开文本上运行：教师先执行有界 next-token 训练后冻结，学生独立随机初始化，真实采样新 token，再执行上述 DrOPD 参数更新。没有预先固定响应候选、没有向模型返回标准答案；256 byte 词表只是缩小 backbone。  On-policy distillation 散度路由 Token 级监督 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-divergence-routed-opd-a4becc18">Divergence-Routed On-Policy Distillation for Language Models</h2>
<p class="ar-learning-card__meta">Peking University · 论文公开：2026-10-14</p>
<p><strong>方法要点：</strong>DrOPD 在学生自己生成的轨迹上比较师生分布，以 JS 散度识别教师支持而学生严重欠覆盖的位置。它在所有位置保留 reverse-KL，并仅向高分歧位置增加 forward-KL 的纠正信号，通过候选级优势执行 PPO clipped 更新。reverse-KL 的 logit 梯度包含学生概率因子，学生几乎不给某个教师 token 概率时，纠正信号会变弱。forward-KL 的梯度为学生与教师概率之差，能继续推动这些教师模式；路由限制额外监督的位置，而不是直接把整个损失换成 forward-KL。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整论文训练成本过高，不复现（审查 DONE）。L1 算法组件与真实在线更新诊断。L1 算法组件与真实在线更新诊断。本地执行候选并集、JS 路由和 PPO 更新；完整论文训练成本过高，不复现（审查 DONE）。与 Dr. OPD（2609.38025） 是不同论文，方法键不复用。微型 byte 自回归模型在固定公开文本上运行：教师先执行有界 next-token 训练后冻结，学生独立随机初始化，真实采样新 token，再执行上述 DrOPD 参数更新。没有预先固定响应候选、没有向模型返回标准答案；256 byte 词表只是缩小 backbone。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19572v1">原论文</a> · <a href="../../../../post-training/2610.19572-divergence-routed-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Information-Gain Calibrated On-Policy Distillation for Deep Search Agents LLM 后训练 The Chinese University of Hong Kong, Shenzhen 2026-10-14 普通 OPD 在检索前按教师偏好评分 query，却不知道检索结果是否有用；又按 token 数量分配预算，容易让很长的最终回答压过短而关键的搜索调用。IG-OPD 用检索后的答案置信变化校正两点：ITC 重新分配回合预算，IQC 用有符号增益修正动作关键 token 的方向。参考答案只供训练专用冻结教师探针使用，不进入学生采样上下文。原文 §4 原文 Figure 1 展示“教师不喜欢但能找到证据”的查询；Figure 2 分析 supervision budget 与信息增益失配。见原文方法图。 完整实验成本过高，不复现（审查 DONE）；L1 算法组件／梯度诊断，不是多模态搜索 Agent 复现。L1 算法组件／梯度诊断，不是多模态搜索 Agent 复现。完整实验成本过高，不复现（审查 DONE）；不进入 evolve 晋级。随机32词表策略真实采样三个回合，每回合2个 token，前两回合之后加入外部人工观察。冻结教师在初始与观察后上下文分别评分一个训练专用 reference token，真正计算势差；学生只能读提示、已采样响应和观察，不读 reference。这里只验证信息校准代数，不模拟真实 web search 的质量。  On-policy distillation Agentic RL 后训练算法组件 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-ig-opd-f18f6a41">Information-Gain Calibrated On-Policy Distillation for Deep Search Agents</h2>
<p class="ar-learning-card__meta">The Chinese University of Hong Kong, Shenzhen · 论文公开：2026-10-14</p>
<p><strong>方法要点：</strong>普通 OPD 在检索前按教师偏好评分 query，却不知道检索结果是否有用；又按 token 数量分配预算，容易让很长的最终回答压过短而关键的搜索调用。IG-OPD 用检索后的答案置信变化校正两点：ITC 重新分配回合预算，IQC 用有符号增益修正动作关键 token 的方向。参考答案只供训练专用冻结教师探针使用，不进入学生采样上下文。原文 §4 原文 Figure 1 展示“教师不喜欢但能找到证据”的查询；Figure 2 分析 supervision budget 与信息增益失配。见原文方法图。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）；L1 算法组件／梯度诊断，不是多模态搜索 Agent 复现。L1 算法组件／梯度诊断，不是多模态搜索 Agent 复现。完整实验成本过高，不复现（审查 DONE）；不进入 evolve 晋级。随机32词表策略真实采样三个回合，每回合2个 token，前两回合之后加入外部人工观察。冻结教师在初始与观察后上下文分别评分一个训练专用 reference token，真正计算势差；学生只能读提示、已采样响应和观察，不读 reference。这里只验证信息校准代数，不模拟真实 web search 的质量。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20664v1">原论文</a> · <a href="../../../../post-training/2610.20664-ig-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="State-OPD: State-Grounded On-Policy Distillation for Multi-Turn Agents LLM 后训练 Alibaba Group 2026-10-09 多轮OPD把旧reasoning和实际环境记录混在教师上下文中，可能继承错误推理。State-OPD只给教师已执行action/observation状态，学生仍保留完整history；在高完整词表熵状态扩采整段reasoning+action，额外action不执行。实现保留Appendix D.1实际sampled-K1双裁剪，而非打分启发式。 本页不声明未执行实验已经完成。本地对照口径：基线为冻结初始学生、同配置预算的独立root full-history OPD及无扩采对照，均已实际执行；实际监督token与耗时不同，不宣称实际总计算匹配或能力提升；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  On-policy distillation Interaction-state isolation Entropy-budget allocation LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-state-opd-163aa0d8">State-OPD: State-Grounded On-Policy Distillation for Multi-Turn Agents</h2>
<p class="ar-learning-card__meta">Alibaba Group · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>多轮OPD把旧reasoning和实际环境记录混在教师上下文中，可能继承错误推理。State-OPD只给教师已执行action/observation状态，学生仍保留完整history；在高完整词表熵状态扩采整段reasoning+action，额外action不执行。实现保留Appendix D.1实际sampled-K1双裁剪，而非打分启发式。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本页不声明未执行实验已经完成。本地对照口径：基线为冻结初始学生、同配置预算的独立root full-history OPD及无扩采对照，均已实际执行；实际监督token与耗时不同，不宣称实际总计算匹配或能力提升；实验组仅支持本页L0/L1机制，稳定相对提升不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13238">原论文</a> · <a href="../../../../reproductions/2610.13238-state-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Why On-Policy Distillation Sometimes Fails: Vanishing Learning Signals LLM 后训练 University of Pennsylvania 2026-10-08 OPD 的残余差异可能仍大，但梯度提供的学习信号已变弱。论文同时记录损失、截断前梯度、两折 occupancy 估计、参数位移和逐层表征 CKA；这些是相关性诊断，不是因果证明。 3 步实跑不复现论文的 200 步平台期，也不能证明学习失败的原因。这是诊断设施，不是提高效果的新优化算法。这是诊断设施，不是提高效果的新优化算法。3 步实跑不复现论文的 200 步平台期，也不能证明学习失败的原因。Qwen3-4B 学生、公开 MOPD 教师、LoRA q/v 更新；3 步，每问题 8 条响应分成 2×4 折，最多生成 128 token。8 个独立验证问题仅用于提取表征，不生成答案。见运行说明。  On-policy distillation 学习信号诊断 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-opd-learning-signals-810b86e8">Why On-Policy Distillation Sometimes Fails: Vanishing Learning Signals</h2>
<p class="ar-learning-card__meta">University of Pennsylvania · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>OPD 的残余差异可能仍大，但梯度提供的学习信号已变弱。论文同时记录损失、截断前梯度、两折 occupancy 估计、参数位移和逐层表征 CKA；这些是相关性诊断，不是因果证明。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>3 步实跑不复现论文的 200 步平台期，也不能证明学习失败的原因。这是诊断设施，不是提高效果的新优化算法。这是诊断设施，不是提高效果的新优化算法。3 步实跑不复现论文的 200 步平台期，也不能证明学习失败的原因。Qwen3-4B 学生、公开 MOPD 教师、LoRA q/v 更新；3 步，每问题 8 条响应分成 2×4 折，最多生成 128 token。8 个独立验证问题仅用于提取表征，不生成答案。见运行说明。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11247">原论文</a> · <a href="../../../../post-training/2610.11247-opd-learning-signals/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="When Do We Need On-Policy Distillation? Distilling on Offline Student Rollouts Is Often Better LLM 后训练 UCLA / NVIDIA（论文注明实习） 2026-10-08 初始学生先一次性生成响应，教师评分缓存后固定复用。每次优化仍重新计算当前学生概率和 token 优势，不能把旧优势也一起缓存。 核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式和命令见checkpoint 运行说明。  On-policy distillation Offline student rollouts LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-semi-opd-2bdbc401">When Do We Need On-Policy Distillation? Distilling on Offline Student Rollouts Is Often Better</h2>
<p class="ar-learning-card__meta">UCLA / NVIDIA（论文注明实习） · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>初始学生先一次性生成响应，教师评分缓存后固定复用。每次优化仍重新计算当前学生概率和 token 优势，不能把旧优势也一起缓存。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式和命令见checkpoint 运行说明。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11291">原论文</a> · <a href="../../../../post-training/2610.11291-semi-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Dr. OPD: Learning What to Follow for Optimal On-Policy Distillation of Large Language Models LLM 后训练 Rutgers University 2026-09-29 普通 OPD 对每个 teacher token 信号等权，但改正关键推理错误与替换同义措辞的下游价值不同。Dr. OPD 用双层优化定义“更新学生后预期 reward 最大”的 token 权重，并在每轮先闭式更新权重，再执行一次加权 OPD。 复现级别：L1 目标函数。复现级别：L1 目标函数。实现 discrepancy × reward-JVP token credit、闭式权重更新和加权 reverse-KL；未进行论文规模的双层迭代训练。本地验证权重有界、梯度有限和不同 token credit 能产生差异化权重。A100 脱敏记录见 ../../gpu-validations/dr-opd-a100-20260930.json。  On-policy distillation 双层优化 Token 权重 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-dr-opd-97941784">Dr. OPD: Learning What to Follow for Optimal On-Policy Distillation of Large Language Models</h2>
<p class="ar-learning-card__meta">Rutgers University · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>普通 OPD 对每个 teacher token 信号等权，但改正关键推理错误与替换同义措辞的下游价值不同。Dr. OPD 用双层优化定义“更新学生后预期 reward 最大”的 token 权重，并在每轮先闭式更新权重，再执行一次加权 OPD。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：L1 目标函数。复现级别：L1 目标函数。实现 discrepancy × reward-JVP token credit、闭式权重更新和加权 reverse-KL；未进行论文规模的双层迭代训练。本地验证权重有界、梯度有限和不同 token credit 能产生差异化权重。A100 脱敏记录见 ../../gpu-validations/dr-opd-a100-20260930.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38025">原论文</a> · <a href="../../../../post-training/2609.38025-dr-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="DriftOPD: Sequence-Level Reverse-KL Distillation for One-Step VLA Policies LLM 后训练 KAIST 2026-09-29 把序列级 reverse-KL 拆成当前 chunk 的一步 reverse-KL 与刻画长期动作后果的 future potential；critic 从离线 demonstrations 学习。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 objective 分解和 teacher stop-gradient；未运行机器人环境。执行 objective 分解和 teacher stop-gradient；未运行机器人环境。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  OPD VLA 长程信用 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-drift-opd-b3b01276">DriftOPD: Sequence-Level Reverse-KL Distillation for One-Step VLA Policies</h2>
<p class="ar-learning-card__meta">KAIST · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>把序列级 reverse-KL 拆成当前 chunk 的一步 reverse-KL 与刻画长期动作后果的 future potential；critic 从离线 demonstrations 学习。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 objective 分解和 teacher stop-gradient；未运行机器人环境。执行 objective 分解和 teacher stop-gradient；未运行机器人环境。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00317">原论文</a> · <a href="../../../../post-training/2610.00317-drift-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="FlowMap-OPD: Rollout-Kernel Separation for On-Policy Distillation of Few-Step Flow-Map Generators LLM 后训练 Georgia Institute of Technology 2026-09-29 把生成状态的 rollout 分布与 teacher/student 比较 kernel 解耦：rollout 只负责提供具有正确边缘分布的状态，优化 kernel 在这些冻结状态上比较 flow map、诱导速度或瞬时速度。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 rollout state detach 与 local kernel KL；未训练图像 flow-map generator。执行 rollout state detach 与 local kernel KL；未训练图像 flow-map generator。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  On-policy distillation Flow map 生成模型 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-flowmap-opd-fd47b0da">FlowMap-OPD: Rollout-Kernel Separation for On-Policy Distillation of Few-Step Flow-Map Generators</h2>
<p class="ar-learning-card__meta">Georgia Institute of Technology · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>把生成状态的 rollout 分布与 teacher/student 比较 kernel 解耦：rollout 只负责提供具有正确边缘分布的状态，优化 kernel 在这些冻结状态上比较 flow map、诱导速度或瞬时速度。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 rollout state detach 与 local kernel KL；未训练图像 flow-map generator。执行 rollout state detach 与 local kernel KL；未训练图像 flow-map generator。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37851">原论文</a> · <a href="../../../../post-training/2609.37851-flowmap-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Interpolated Policy Distillation: A Controllable Continuum Between Off-Policy and On-Policy Distillation LLM 后训练 WeChat Vision, Tencent 2026-09-29 在每个 token 状态把 student 与 teacher 分布按插值，从纯 on-policy 连续过渡到 off-policy teacher；论文再用验证感知的 speculative sampler 精确采样该目标策略。 高吞吐 speculative sampler 和模型训练未复现。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行精确 token mixture；高吞吐 speculative sampler 和模型训练未复现。执行精确 token mixture；高吞吐 speculative sampler 和模型训练未复现。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  策略蒸馏 分布插值 Speculative sampling LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-ipd-4481efec">Interpolated Policy Distillation: A Controllable Continuum Between Off-Policy and On-Policy Distillation</h2>
<p class="ar-learning-card__meta">WeChat Vision, Tencent · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>在每个 token 状态把 student 与 teacher 分布按插值，从纯 on-policy 连续过渡到 off-policy teacher；论文再用验证感知的 speculative sampler 精确采样该目标策略。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>高吞吐 speculative sampler 和模型训练未复现。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行精确 token mixture；高吞吐 speculative sampler 和模型训练未复现。执行精确 token mixture；高吞吐 speculative sampler 和模型训练未复现。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37170">原论文</a> · <a href="../../../../post-training/2609.37170-ipd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Overcoming Scaling Limits in On-Policy Self-Distillation for LLM Reasoning LLM 后训练 North South University 2026-09-29 OASIS 把“在哪里监督”和“teacher 看什么 context”解耦：从同一题的 on-policy rollouts 中选最短的已验证轨迹作为 scaffold；teacher context 优先使用另一条未验证尝试；没有 verified rollout 的题不产生训练信号。这样只需要最终答案 verifier，而不需要 gold solution。 复现级别：L1 选择与损失机制。复现级别：L1 选择与损失机制。实现 shortest verified scaffold、独立同题 context 和 clipped forward-KL。测试保证未验证短轨迹不会被误选、teacher context 与 scaffold 不同、mask 外 token 无梯度。三种子机制结果见 metrics/mechanism-seeds42-44.json。未运行 Qwen3 1.7B–8B rollout/training，属于机制实现，不宣称 AIME/HMMT 增益。  On-policy self-distillation 可验证推理 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-oasis-opsd-27f4197e">Overcoming Scaling Limits in On-Policy Self-Distillation for LLM Reasoning</h2>
<p class="ar-learning-card__meta">North South University · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>OASIS 把“在哪里监督”和“teacher 看什么 context”解耦：从同一题的 on-policy rollouts 中选最短的已验证轨迹作为 scaffold；teacher context 优先使用另一条未验证尝试；没有 verified rollout 的题不产生训练信号。这样只需要最终答案 verifier，而不需要 gold solution。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：L1 选择与损失机制。复现级别：L1 选择与损失机制。实现 shortest verified scaffold、独立同题 context 和 clipped forward-KL。测试保证未验证短轨迹不会被误选、teacher context 与 scaffold 不同、mask 外 token 无梯度。三种子机制结果见 metrics/mechanism-seeds42-44.json。未运行 Qwen3 1.7B–8B rollout/training，属于机制实现，不宣称 AIME/HMMT 增益。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37915">原论文</a> · <a href="../../../../post-training/2609.37915-oasis/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="The Teacher Is a Direction, Not a Destination: Extrapolating RL-Induced Representation Residuals in On-Policy Distillation LLM 后训练 原文未列机构 2026-09-29 RIDE 不在输出概率空间放大 teacher/student ratio，而是在每层每个 token 计算 RL teacher 相对其 pre-RL checkpoint 的 hidden residual：；学生回归到，其中把方向延伸到 teacher 之外。teacher/base 均 stop-gradient，避免目标分支被学生更新。 复现级别：L1 表征目标。复现级别：L1 表征目标。实现 base→RL teacher 的逐层残差外推与 masked regression。ride_target 与 ride_loss 覆盖退化、外推、mask 和 teacher stop-gradient；三种子机制结果见 metrics/mechanism-seeds42-44.json。未加载四组真实 base/RL teacher checkpoint，不能视为论文效果复现。  On-policy distillation 表征蒸馏 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-ride-opd-b6296fc3">The Teacher Is a Direction, Not a Destination: Extrapolating RL-Induced Representation Residuals in On-Policy Distillation</h2>
<p class="ar-learning-card__meta">原文未列机构 · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>RIDE 不在输出概率空间放大 teacher/student ratio，而是在每层每个 token 计算 RL teacher 相对其 pre-RL checkpoint 的 hidden residual：；学生回归到，其中把方向延伸到 teacher 之外。teacher/base 均 stop-gradient，避免目标分支被学生更新。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：L1 表征目标。复现级别：L1 表征目标。实现 base→RL teacher 的逐层残差外推与 masked regression。ride_target 与 ride_loss 覆盖退化、外推、mask 和 teacher stop-gradient；三种子机制结果见 metrics/mechanism-seeds42-44.json。未加载四组真实 base/RL teacher checkpoint，不能视为论文效果复现。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36484">原论文</a> · <a href="../../../../post-training/2609.36484-ride/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="SIPO: Unifying Reinforcement Learning with On-Policy Self-Distillation LLM 后训练 University of Illinois Urbana-Champaign 2026-09-29 RLVR 的轨迹 reward 稀疏，普通 OPSD 又会受自教师过度自信和长序列惩罚影响。SIPO 对同一 rollout 构造正/负两份特权上下文：两者 teacher log-prob 的差值抵消共享偏差，形成逐 token 信用；环境 reward 决定主方向，dense evidence 负责在 token 间重新分配。 复现级别：L1 目标函数。复现级别：L1 目标函数。实现双上下文 contrastive self-teacher、逐 token advantage 和 policy-gradient 组合；未执行论文规模 rollout 训练。机制测试覆盖全失败组仍有 token 信号、有限梯度及 reward 主方向。A100 脱敏记录见 ../../gpu-validations/sipo-a100-20260930.json。  RLVR On-policy self-distillation Token 信用分配 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-sipo-d20b9ca6">SIPO: Unifying Reinforcement Learning with On-Policy Self-Distillation</h2>
<p class="ar-learning-card__meta">University of Illinois Urbana-Champaign · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>RLVR 的轨迹 reward 稀疏，普通 OPSD 又会受自教师过度自信和长序列惩罚影响。SIPO 对同一 rollout 构造正/负两份特权上下文：两者 teacher log-prob 的差值抵消共享偏差，形成逐 token 信用；环境 reward 决定主方向，dense evidence 负责在 token 间重新分配。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：L1 目标函数。复现级别：L1 目标函数。实现双上下文 contrastive self-teacher、逐 token advantage 和 policy-gradient 组合；未执行论文规模 rollout 训练。机制测试覆盖全失败组仍有 token 信号、有限梯度及 reward 主方向。A100 脱敏记录见 ../../gpu-validations/sipo-a100-20260930.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36742">原论文</a> · <a href="../../../../post-training/2609.36742-sipo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="An RL View of OPD: Least Square Policy Distillation for Sample-Efficient LLM Reasoning LLM 后训练 University of North Carolina at Chapel Hill 2026-09-28 LSPD 把教师与学生的 token log-prob 差视作可优化残差，以 least-square 形式直接收缩分布差距，并用 Huber 式尾部限制异常差值的梯度；同时允许复用历史 query-response 轨迹，提高样本效率。 未复现原作者完整 reasoning 数据管线与大规模教师 rollout，也未接入 Evolve。复现级别：L1 核心机制 + 真实 checkpoint CUDA 路径。复现级别：L1 核心机制 + 真实 checkpoint CUDA 路径。实现稳健 least-square policy-distillation 目标与离策略回放容器；不外推完整推理训练收益。未复现原作者完整 reasoning 数据管线与大规模教师 rollout，也未接入 Evolve。只有控制器能执行真实 LSPD 更新并在隔离验证集评价时，才会标为可进化算子。  On-policy distillation 离策略回放 推理 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-lspd-3161a2b9">An RL View of OPD: Least Square Policy Distillation for Sample-Efficient LLM Reasoning</h2>
<p class="ar-learning-card__meta">University of North Carolina at Chapel Hill · 论文公开：2026-09-28</p>
<p><strong>方法要点：</strong>LSPD 把教师与学生的 token log-prob 差视作可优化残差，以 least-square 形式直接收缩分布差距，并用 Huber 式尾部限制异常差值的梯度；同时允许复用历史 query-response 轨迹，提高样本效率。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>未复现原作者完整 reasoning 数据管线与大规模教师 rollout，也未接入 Evolve。复现级别：L1 核心机制 + 真实 checkpoint CUDA 路径。复现级别：L1 核心机制 + 真实 checkpoint CUDA 路径。实现稳健 least-square policy-distillation 目标与离策略回放容器；不外推完整推理训练收益。未复现原作者完整 reasoning 数据管线与大规模教师 rollout，也未接入 Evolve。只有控制器能执行真实 LSPD 更新并在隔离验证集评价时，才会标为可进化算子。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35505">原论文</a> · <a href="../../../../post-training/2609.35505-lspd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Recursive Self-Improvement via On-Policy Distillation for Reasoning LLM 后训练 Meta AI / University of California, Riverside 2026-09-25 传统 OPSD 让学生只看题目、冻结的特权教师额外看标准解，在学生自己的输出前缀上做逐 token 蒸馏。教师停留在初始权重时，后续学生学到的回看和纠错行为无法反哺教师。论文提出两个互补改动：DCE（动态共演化）：第 k 轮由当前学生采样回答 yᵏ；同一份当前权重、停止梯度且额外看到标准解的教师，对相同回答前缀给出分布 qᵏ。学生最小化 KL(qᵏ‖pᵏ)。更新后的权重同时成为下一轮学生和教师，教师不是独立优化的第二个模型。 本地只用公开 Qwen3-4B-Instruct-2507 与官方 GSM8K 的 4 道训练、2 道验证、2 道测试题，在 A100 上做 2 次 rank-8 更新、192-token 上限的机制诊断。本地只用公开 Qwen3-4B-Instruct-2507 与官方 GSM8K 的 4 道训练、2 道验证、2 道测试题，在 A100 上做 2 次 rank-8 更新、192-token 上限的机制诊断。seed 42，固定同一数据、步数和生成上限。稳定指标文件为 qwen3-4b-gsm8k-seed42.json。  On-policy self-distillation DCE SRCL reasoning LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-recursive-opsd-defa1333">Recursive Self-Improvement via On-Policy Distillation for Reasoning</h2>
<p class="ar-learning-card__meta">Meta AI / University of California, Riverside · 论文公开：2026-09-25</p>
<p><strong>方法要点：</strong>传统 OPSD 让学生只看题目、冻结的特权教师额外看标准解，在学生自己的输出前缀上做逐 token 蒸馏。教师停留在初始权重时，后续学生学到的回看和纠错行为无法反哺教师。论文提出两个互补改动：DCE（动态共演化）：第 k 轮由当前学生采样回答 yᵏ；同一份当前权重、停止梯度且额外看到标准解的教师，对相同回答前缀给出分布 qᵏ。学生最小化 KL(qᵏ‖pᵏ)。更新后的权重同时成为下一轮学生和教师，教师不是独立优化的第二个模型。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本地只用公开 Qwen3-4B-Instruct-2507 与官方 GSM8K 的 4 道训练、2 道验证、2 道测试题，在 A100 上做 2 次 rank-8 更新、192-token 上限的机制诊断。本地只用公开 Qwen3-4B-Instruct-2507 与官方 GSM8K 的 4 道训练、2 道验证、2 道测试题，在 A100 上做 2 次 rank-8 更新、192-token 上限的机制诊断。seed 42，固定同一数据、步数和生成上限。稳定指标文件为 qwen3-4b-gsm8k-seed42.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.30652">原论文</a> · <a href="../../../../reproductions/2609.30652-recursive-opsd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Beyond Token-Local Imitation: Reward-Compatible Temporal Credit Assignment for On-Policy Distillation LLM 后训练 Tsinghua University / DiDi Voyager Labs 2026-09-15 以折扣时间信用逼近序列级 reverse-KL，再用有界奖励优势补入可验证结果。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行折扣回传和 RBM；未训练论文规模语言模型。本地执行折扣回传和 RBM；未训练论文规模语言模型。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  On-policy distillation 时间信用分配 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-gamma-opd-41117d94">Beyond Token-Local Imitation: Reward-Compatible Temporal Credit Assignment for On-Policy Distillation</h2>
<p class="ar-learning-card__meta">Tsinghua University / DiDi Voyager Labs · 论文公开：2026-09-15</p>
<p><strong>方法要点：</strong>以折扣时间信用逼近序列级 reverse-KL，再用有界奖励优势补入可验证结果。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行折扣回传和 RBM；未训练论文规模语言模型。本地执行折扣回传和 RBM；未训练论文规模语言模型。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16937">原论文</a> · <a href="../../../../post-training/2609.16937-gamma-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Distillation as Probability Transport: Routed On-Policy Distillation LLM 后训练 Tencent 2026-09-08 普通 OPD 对整个教师分布做密集匹配。RouteOPD 先识别学生高估的 source token 和低估的 destination token，再只搬运需要修正的概率质量，使监督更聚焦且可解释。 复现级别：候选策略机制诊断。复现级别：候选策略机制诊断。执行 source-to-destination 概率质量运输，不声称复现大模型推理能力。三种子结果见 metrics/arithmetic-smoke-seeds42-44.json。未执行原论文全参数模型、真实 rollout 或公开推理 benchmark；结果只证明路由算子执行且数值有限。  概率传输 OPD LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-route-opd-eaed8417">Distillation as Probability Transport: Routed On-Policy Distillation</h2>
<p class="ar-learning-card__meta">Tencent · 论文公开：2026-09-08</p>
<p><strong>方法要点：</strong>普通 OPD 对整个教师分布做密集匹配。RouteOPD 先识别学生高估的 source token 和低估的 destination token，再只搬运需要修正的概率质量，使监督更聚焦且可解释。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：候选策略机制诊断。复现级别：候选策略机制诊断。执行 source-to-destination 概率质量运输，不声称复现大模型推理能力。三种子结果见 metrics/arithmetic-smoke-seeds42-44.json。未执行原论文全参数模型、真实 rollout 或公开推理 benchmark；结果只证明路由算子执行且数值有限。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08337">原论文</a> · <a href="../../../../post-training/2609.08337-route-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="OPDSearch+: Search-Enhanced On-Policy Distillation with Reinforcement Learning LLM 后训练 University of Chinese Academy of Sciences 2026-08-25 搜索 Agent 的多轮 SFT 数据昂贵，任务专用教师又需先训练。OPDSearch+ 直接冻结通用 instruct teacher，在学生自己的在线搜索轨迹上用 forward-KL 蒸馏 query、推理和答案 token；随后 RL 从更好的行为分布继续优化，突破教师与纯 RL 的局部最优。 复现级别：核心机制 candidate-policy。复现级别：核心机制 candidate-policy。实际执行 clipped forward-KL 与后续 verifier RL 两阶段目标；未训练 Qwen2.5-3B 搜索 Agent。本地用候选级 process signal 代替真实 query/reasoning/answer token 与搜索引擎反馈；未运行 3B/14B 模型、Wikipedia index 或七个 QA benchmark。arithmetic-smoke、100 steps、seed 42：accuracy 0.1953 → 0.6641。  搜索增强 OPD + RL LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-opd-search-plus-8653157e">OPDSearch+: Search-Enhanced On-Policy Distillation with Reinforcement Learning</h2>
<p class="ar-learning-card__meta">University of Chinese Academy of Sciences · 论文公开：2026-08-25</p>
<p><strong>方法要点：</strong>搜索 Agent 的多轮 SFT 数据昂贵，任务专用教师又需先训练。OPDSearch+ 直接冻结通用 instruct teacher，在学生自己的在线搜索轨迹上用 forward-KL 蒸馏 query、推理和答案 token；随后 RL 从更好的行为分布继续优化，突破教师与纯 RL 的局部最优。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 candidate-policy。复现级别：核心机制 candidate-policy。实际执行 clipped forward-KL 与后续 verifier RL 两阶段目标；未训练 Qwen2.5-3B 搜索 Agent。本地用候选级 process signal 代替真实 query/reasoning/answer token 与搜索引擎反馈；未运行 3B/14B 模型、Wikipedia index 或七个 QA benchmark。arithmetic-smoke、100 steps、seed 42：accuracy 0.1953 → 0.6641。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24310">原论文</a> · <a href="../../../../post-training/2608.24310-opd-search-plus/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="OPDVR: On-Policy Distillation with Verifiable Rewards LLM 后训练 LeapLab, Tsinghua University 2026-08-25 Sampled-token OPD 的隐式奖励由教师/学生概率比决定，可能给正确轨迹负奖励、给错误轨迹正奖励。OPDVR 不再额外混合一个 RL loss，而是直接用 verifier correctness 对该隐式奖励做单侧 ReLU：正确轨迹只保留非负教师信号，错误轨迹只保留非正信号。 复现级别：核心机制 candidate-policy。复现级别：核心机制 candidate-policy。实际执行 sampled-token 隐式奖励和 correctness-aware ReLU gate，不用加权超参数拼接 OPD/RLVR。使用候选策略和精确 outcome 代理 token rollout；未运行 Qwen3、六个数学 benchmark 或真实 verifier rollout。arithmetic-smoke、100 steps、seed 42：accuracy 0.1953 → 0.6641，最终 KL(reference) 0.0018。单 seed 只验证 gate 与更新方向。  可验证奖励 OPD LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-opdvr-c33841ab">OPDVR: On-Policy Distillation with Verifiable Rewards</h2>
<p class="ar-learning-card__meta">LeapLab, Tsinghua University · 论文公开：2026-08-25</p>
<p><strong>方法要点：</strong>Sampled-token OPD 的隐式奖励由教师/学生概率比决定，可能给正确轨迹负奖励、给错误轨迹正奖励。OPDVR 不再额外混合一个 RL loss，而是直接用 verifier correctness 对该隐式奖励做单侧 ReLU：正确轨迹只保留非负教师信号，错误轨迹只保留非正信号。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 candidate-policy。复现级别：核心机制 candidate-policy。实际执行 sampled-token 隐式奖励和 correctness-aware ReLU gate，不用加权超参数拼接 OPD/RLVR。使用候选策略和精确 outcome 代理 token rollout；未运行 Qwen3、六个数学 benchmark 或真实 verifier rollout。arithmetic-smoke、100 steps、seed 42：accuracy 0.1953 → 0.6641，最终 KL(reference) 0.0018。单 seed 只验证 gate 与更新方向。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24696">原论文</a> · <a href="../../../../post-training/2608.24696-opdvr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Beyond Imitation: Filtering On-Policy Distillation by Reasoning Progress LLM 后训练 Authors did not disclose affiliation 2026-08-19 分别按教师奖励和独立进展奖励排序 reasoning spans，冲突时屏蔽蒸馏信号。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  OPD 过程蒸馏 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-r2-opd-a6acbe83">Beyond Imitation: Filtering On-Policy Distillation by Reasoning Progress</h2>
<p class="ar-learning-card__meta">Authors did not disclose affiliation · 论文公开：2026-08-19</p>
<p><strong>方法要点：</strong>分别按教师奖励和独立进展奖励排序 reasoning spans，冲突时屏蔽蒸馏信号。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.19408">原论文</a> · <a href="../../../../post-training/2608.19408-r2-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="SR-OPSD: Self-Referenced On-Policy Self-Distillation LLM 后训练 Independent Researcher 2026-08-10 把自教师与 reference 做几何插值得到有效目标，再用 Rényi divergence 控制投影几何和密度比敏感度。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  OPD 自蒸馏 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-sr-opsd-5465332e">SR-OPSD: Self-Referenced On-Policy Self-Distillation</h2>
<p class="ar-learning-card__meta">Independent Researcher · 论文公开：2026-08-10</p>
<p><strong>方法要点：</strong>把自教师与 reference 做几何插值得到有效目标，再用 Rényi divergence 控制投影几何和密度比敏感度。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.09745">原论文</a> · <a href="../../../../post-training/2608.09745-sr-opsd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="DASH LLM 后训练 Nanjing University 2026-08-06 普通 OPSD 对每个 token 独立匹配 privileged teacher，难把后续可靠推理对前面决策的信用传回去。DASH 由局部 teacher/student divergence 产生停止梯度 gate，再从后向前递推聚合权重；不增加 teacher forward pass，却获得自适应 distillation horizon。 Fidelity：核心机制复现。实现局部散度裁剪、stop-gradient gate 与反向 horizon 聚合；候选位置代理 token 位置。候选位置不是完整 token trajectory；未复刻 Qwen3、数学推理语料和多卡训练。Arithmetic candidate suite、120 steps、seed 42：accuracy 0.2344 → 0.5781（+146.67%），最后 gate mean 0.4822、平均 horizon coefficient 1.5617、额外 teacher forward 为 0。  自适应自蒸馏 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-dash-1d95c042">DASH</h2>
<p class="ar-learning-card__meta">Nanjing University · 论文公开：2026-08-06</p>
<p><strong>方法要点：</strong>普通 OPSD 对每个 token 独立匹配 privileged teacher，难把后续可靠推理对前面决策的信用传回去。DASH 由局部 teacher/student divergence 产生停止梯度 gate，再从后向前递推聚合权重；不增加 teacher forward pass，却获得自适应 distillation horizon。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity：核心机制复现。实现局部散度裁剪、stop-gradient gate 与反向 horizon 聚合；候选位置代理 token 位置。候选位置不是完整 token trajectory；未复刻 Qwen3、数学推理语料和多卡训练。Arithmetic candidate suite、120 steps、seed 42：accuracy 0.2344 → 0.5781（+146.67%），最后 gate mean 0.4822、平均 horizon coefficient 1.5617、额外 teacher forward 为 0。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06243">原论文</a> · <a href="../../../../post-training/2608.06243-dash/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="On-Policy Delta Distillation for Multilingual Math Reasoning LLM 后训练 NAVER AI Lab 2026-08-06 以 post-trained teacher 相对其 base model 的概率增量作为蒸馏信号，减少复制教师原有偏差。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  OPD 多语言推理 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-opd2-d840d7f7">On-Policy Delta Distillation for Multilingual Math Reasoning</h2>
<p class="ar-learning-card__meta">NAVER AI Lab · 论文公开：2026-08-06</p>
<p><strong>方法要点：</strong>以 post-trained teacher 相对其 base model 的概率增量作为蒸馏信号，减少复制教师原有偏差。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05802">原论文</a> · <a href="../../../../post-training/2608.05802-opd2/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="RP-OPSD LLM 后训练 Nanjing University 2026-08-06 跨语言迁移中，表面措辞与真正改变推理状态的 pivot 不应同权。RP-OPSD 比较带英文参考解与去掉参考解的匹配教师视图，用分布位移定位 pivot，再在这些位置强化 privileged distillation 并保留 reference anchor。 诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现 reference-conditioned / ablated 双视图、pivot gate 与 reference anchor。  推理枢纽蒸馏 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-rp-opsd-6ed9619b">RP-OPSD</h2>
<p class="ar-learning-card__meta">Nanjing University · 论文公开：2026-08-06</p>
<p><strong>方法要点：</strong>跨语言迁移中，表面措辞与真正改变推理状态的 pivot 不应同权。RP-OPSD 比较带英文参考解与去掉参考解的匹配教师视图，用分布位移定位 pivot，再在这些位置强化 privileged distillation 并保留 reference anchor。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现 reference-conditioned / ablated 双视图、pivot gate 与 reference anchor。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06347">原论文</a> · <a href="../../../../post-training/2608.06347-rp-opsd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="U-OPSD LLM 后训练 University of California, San Diego 2026-08-06 U-OPSD 不使用答案、环境奖励或更大教师。模型多次采样后做多数投票，以最短一致解作为 privileged view，定点修复最长且高置信错误轨迹，是真正依赖内部一致性的自蒸馏。 诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现多 rollout 自一致投票、置信门控与无 gold 伪教师；公开算术 mini-suite 上该无监督假设并不成立，因此如实记录退化结果。  无监督自蒸馏 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-u-opsd-4619f519">U-OPSD</h2>
<p class="ar-learning-card__meta">University of California, San Diego · 论文公开：2026-08-06</p>
<p><strong>方法要点：</strong>U-OPSD 不使用答案、环境奖励或更大教师。模型多次采样后做多数投票，以最短一致解作为 privileged view，定点修复最长且高置信错误轨迹，是真正依赖内部一致性的自蒸馏。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现多 rollout 自一致投票、置信门控与无 gold 伪教师；公开算术 mini-suite 上该无监督假设并不成立，因此如实记录退化结果。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06296">原论文</a> · <a href="../../../../post-training/2608.06296-u-opsd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="CausalOPD: First-Wrong-Step Supervision for Distilling Causal Chain Reasoning LLM 后训练 Authors did not disclose affiliation 2026-08-04 教师定位 on-policy 因果链第一个错误步骤，以短 horizon RL 修复，并按证据→机制→结论推进课程。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  OPD 过程监督 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-causal-opd-da48af2a">CausalOPD: First-Wrong-Step Supervision for Distilling Causal Chain Reasoning</h2>
<p class="ar-learning-card__meta">Authors did not disclose affiliation · 论文公开：2026-08-04</p>
<p><strong>方法要点：</strong>教师定位 on-policy 因果链第一个错误步骤，以短 horizon RL 修复，并按证据→机制→结论推进课程。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03673">原论文</a> · <a href="../../../../post-training/2608.03673-causal-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="PCSD LLM 后训练 论文未列机构 2026-08-03 单 token teacher gap 容易受噪声影响，整步共享权重又会抹掉位置差异。PCSD 在自适应窗口内指数累积 teacher-favoring signal，并对下降趋势衰减，最后用连续 sigmoid gate 与 GRPO 联合训练。 诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现指数持续证据、趋势衰减与连续门控，候选位置作为 token 位置代理。  持续一致性蒸馏 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-pcsd-bac5e7a6">PCSD</h2>
<p class="ar-learning-card__meta">论文未列机构 · 论文公开：2026-08-03</p>
<p><strong>方法要点：</strong>单 token teacher gap 容易受噪声影响，整步共享权重又会抹掉位置差异。PCSD 在自适应窗口内指数累积 teacher-favoring signal，并对下降趋势衰减，最后用连续 sigmoid gate 与 GRPO 联合训练。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现指数持续证据、趋势衰减与连续门控，候选位置作为 token 位置代理。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01837">原论文</a> · <a href="../../../../post-training/2608.01837-pcsd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="β-OPSD LLM 后训练 University of Maryland, College Park 2026-07-30 论文指出 vanilla OPSD 是 β=1 的 KL 正则策略优化特例。先推导 reference policy 与 privileged teacher 之间的最优几何插值，再把昂贵高方差的 RL 解转成 token-logit 蒸馏目标，并以 return-to-go 做长推理信用分配。 保真度：实现 reference/privileged teacher 几何插值、可控 β 与 return-to-go 权重；保真度：实现 reference/privileged teacher 几何插值、可控 β 与 return-to-go 权重；不冒充论文 Qwen3 训练。候选动作对应 token 分布，线性 return-to-go 代理序列位置；未复刻 Qwen3、LoRA 和 A6000/H200 训练。本地对照口径：同一 GSM8K candidate-policy、120 steps、seed 42；相对未训练基线 accuracy 从 0.1719 到 0.7656（+345.45%）。  On-policy self-distillation LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-beta-opsd-d0fa334d">β-OPSD</h2>
<p class="ar-learning-card__meta">University of Maryland, College Park · 论文公开：2026-07-30</p>
<p><strong>方法要点：</strong>论文指出 vanilla OPSD 是 β=1 的 KL 正则策略优化特例。先推导 reference policy 与 privileged teacher 之间的最优几何插值，再把昂贵高方差的 RL 解转成 token-logit 蒸馏目标，并以 return-to-go 做长推理信用分配。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：实现 reference/privileged teacher 几何插值、可控 β 与 return-to-go 权重；保真度：实现 reference/privileged teacher 几何插值、可控 β 与 return-to-go 权重；不冒充论文 Qwen3 训练。候选动作对应 token 分布，线性 return-to-go 代理序列位置；未复刻 Qwen3、LoRA 和 A6000/H200 训练。本地对照口径：同一 GSM8K candidate-policy、120 steps、seed 42；相对未训练基线 accuracy 从 0.1719 到 0.7656（+345.45%）。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28582">原论文</a> · <a href="../../../../post-training/2607.28582-beta-opsd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Flux-OPD LLM 后训练 Peking University 2026-07-30 固定上下文很快被学生吸收，直接更换上下文 teacher 又会让目标跳变。Flux-OPD 固定 context-free teacher 为锚，只注入多个演化上下文 teacher 相对锚点的 log-probability 差，并用几何均值归一化常数表示冲突、冲突越大修正越弱。 保真度：实现 context-free anchor、几何 teacher、contextual correction 与 conflict weighting。本地两个 reward axis 代理演化上下文 teacher；未调用视频模型、医疗 teacher 或大模型上下文抽取。本地对照口径：同一 GSM8K candidate-policy、120 steps、seed 42；accuracy 从 0.1719 到 0.8438（+390.91%）。  Context distillation LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-flux-opd-da1bf9b3">Flux-OPD</h2>
<p class="ar-learning-card__meta">Peking University · 论文公开：2026-07-30</p>
<p><strong>方法要点：</strong>固定上下文很快被学生吸收，直接更换上下文 teacher 又会让目标跳变。Flux-OPD 固定 context-free teacher 为锚，只注入多个演化上下文 teacher 相对锚点的 log-probability 差，并用几何均值归一化常数表示冲突、冲突越大修正越弱。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：实现 context-free anchor、几何 teacher、contextual correction 与 conflict weighting。本地两个 reward axis 代理演化上下文 teacher；未调用视频模型、医疗 teacher 或大模型上下文抽取。本地对照口径：同一 GSM8K candidate-policy、120 steps、seed 42；accuracy 从 0.1719 到 0.8438（+390.91%）。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28022">原论文</a> · <a href="../../../../post-training/2607.28022-flux-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Relay-OPD LLM 后训练 Zhejiang University 2026-07-28 检测学生前缀失效后让教师短暂接管，再把轨迹交还学生；有限接力预算把监督集中到关键早期位置。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。本地教师是可复现的候选分布缓存，并非 Qwen3-4B；因此验证接力状态机和监督方向，不冒充论文八卡训练。GSM8K candidate-policy 上实现失效前缀检测、教师 handoff、有限 relay budget 和学生恢复生成；与同一未训练策略公平比较。  On-policy distillation LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-relay-opd-4c82d340">Relay-OPD</h2>
<p class="ar-learning-card__meta">Zhejiang University · 论文公开：2026-07-28</p>
<p><strong>方法要点：</strong>检测学生前缀失效后让教师短暂接管，再把轨迹交还学生；有限接力预算把监督集中到关键早期位置。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。本地教师是可复现的候选分布缓存，并非 Qwen3-4B；因此验证接力状态机和监督方向，不冒充论文八卡训练。GSM8K candidate-policy 上实现失效前缀检测、教师 handoff、有限 relay budget 和学生恢复生成；与同一未训练策略公平比较。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26057">原论文</a> · <a href="../../../../post-training/2607.26057-relay-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="OPDLM LLM 后训练 Texas A&amp;M University 2026-06-04 ARLM 改成双向注意力后既会遗忘原知识，也有随机 mask 训练与 confidence decoding 推理之间的偏移。OPDLM 让双向学生在自身推理轨迹上生成，冻结 AR 教师在同一轨迹给 target logits。 诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。用相邻候选状态模拟双向去噪视图，保留冻结 AR teacher anchor；不冒充完整 diffusion decoder。  AR-to-Diffusion 蒸馏 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-opd-lm-752e6c98">OPDLM</h2>
<p class="ar-learning-card__meta">Texas A&amp;M University · 论文公开：2026-06-04</p>
<p><strong>方法要点：</strong>ARLM 改成双向注意力后既会遗忘原知识，也有随机 mask 训练与 confidence decoding 推理之间的偏移。OPDLM 让双向学生在自身推理轨迹上生成，冻结 AR 教师在同一轨迹给 target logits。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。用相邻候选状态模拟双向去噪视图，保留冻结 AR teacher anchor；不冒充完整 diffusion decoder。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.06712">原论文</a> · <a href="../../../../post-training/2606.06712-opd-lm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="GKD LLM 后训练 Google DeepMind 2023-06-23 固定教师轨迹会让学生训练时看到的前缀与推理时自身生成的前缀不一致。GKD 让学生生成当前策略轨迹，再让教师在这些学生实际访问的状态给出完整分布；同时用 student data fraction 在固定数据和 on-policy 数据之间插值，并允许 forward KL、reverse KL 或广义 JSD。 保真度：本地实现了学生 on-policy 采样、教师对学生访问状态打分、on/off-policy 混合和散度诊断；保真度：本地实现了学生 on-policy 采样、教师对学生访问状态打分、on/off-policy 混合和散度诊断；当前是候选策略机制复现，不等同于 T5-XL 到小模型的 token 级蒸馏。本地候选项对应可审计的学生轨迹支撑集，教师分布由 GSM8K 结果与过程质量构造；没有训练真实自回归 T5，也没有复跑 XSum/WMT。因此本地百分比只能验证数据流和目标函数，不能与论文指标横向比较。稳定指标见 classic-agentic-rl-opd-seed42.json。  经典 On-policy distillation LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-gkd-c556ce32">GKD</h2>
<p class="ar-learning-card__meta">Google DeepMind · 论文公开：2023-06-23</p>
<p><strong>方法要点：</strong>固定教师轨迹会让学生训练时看到的前缀与推理时自身生成的前缀不一致。GKD 让学生生成当前策略轨迹，再让教师在这些学生实际访问的状态给出完整分布；同时用 student data fraction 在固定数据和 on-policy 数据之间插值，并允许 forward KL、reverse KL 或广义 JSD。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：本地实现了学生 on-policy 采样、教师对学生访问状态打分、on/off-policy 混合和散度诊断；保真度：本地实现了学生 on-policy 采样、教师对学生访问状态打分、on/off-policy 混合和散度诊断；当前是候选策略机制复现，不等同于 T5-XL 到小模型的 token 级蒸馏。本地候选项对应可审计的学生轨迹支撑集，教师分布由 GSM8K 结果与过程质量构造；没有训练真实自回归 T5，也没有复跑 XSum/WMT。因此本地百分比只能验证数据流和目标函数，不能与论文指标横向比较。稳定指标见 classic-agentic-rl-opd-seed42.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2306.13649">原论文</a> · <a href="../../../../post-training/2306.13649-gkd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="MiniLLM LLM 后训练 Tsinghua University 2023-06-14 标准 forward KL 倾向覆盖教师所有概率质量，小学生可能因此高估教师的低概率区域。MiniLLM 改用 mode-seeking 的 reverse KL，在学生自身生成分布上优化，并通过 teacher-mixed sampling、单步分解、长度归一化和 reward baseline 稳定策略梯度。 保真度：实现学生 rollout 上的 reverse KL、teacher-mixed sampling、方差缩减 baseline 和长度归一化诊断；保真度：实现学生 rollout 上的 reverse KL、teacher-mixed sampling、方差缩减 baseline 和长度归一化诊断；当前未训练论文中的 120M–13B 自回归模型。候选策略可以验证 reverse KL 的采样与梯度方向，但没有真实 tokenizer、长文本生成和 GPT-4 judge。本地 accuracy 不是论文的生成质量分数。稳定指标见 classic-agentic-rl-opd-seed42.json。  Reverse-KL distillation LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<h2 id="paper-post-training-minillm-8f5f3ddd">MiniLLM</h2>
<p class="ar-learning-card__meta">Tsinghua University · 论文公开：2023-06-14</p>
<p><strong>方法要点：</strong>标准 forward KL 倾向覆盖教师所有概率质量，小学生可能因此高估教师的低概率区域。MiniLLM 改用 mode-seeking 的 reverse KL，在学生自身生成分布上优化，并通过 teacher-mixed sampling、单步分解、长度归一化和 reward baseline 稳定策略梯度。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：实现学生 rollout 上的 reverse KL、teacher-mixed sampling、方差缩减 baseline 和长度归一化诊断；保真度：实现学生 rollout 上的 reverse KL、teacher-mixed sampling、方差缩减 baseline 和长度归一化诊断；当前未训练论文中的 120M–13B 自回归模型。候选策略可以验证 reverse KL 的采样与梯度方向，但没有真实 tokenizer、长文本生成和 GPT-4 judge。本地 accuracy 不是论文的生成质量分数。稳定指标见 classic-agentic-rl-opd-seed42.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2306.08543">原论文</a> · <a href="../../../../post-training/2306.08543-minillm/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
