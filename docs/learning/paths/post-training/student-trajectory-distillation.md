---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 在策略蒸馏：沿学生实际走过的前缀学习

[LLM 后训练](index.md) / 40 个问题 · 40 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">40 个问题 · 40 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:opst" data-paper-title="On-Policy Self-Training: Data-Free Self-Improvement in Large Language Models" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="On-Policy Self-Training: Data-Free Self-Improvement in Large Language Models LLM 后训练 Google 2026-10-23 通常的 on-policy self-distillation 仍需要人工问题集。OPST 按主题自生成问题和特权解题线索，经独立重答、改写与学生难度门过滤，再由额外看到线索的 EMA 教师在学生实际生成的前缀上提供分布监督，而不是要求学生直接模仿生成器表述。过滤分为两个方向：生成器在不含的新上下文中重答原题及保义改写题，两次都须匹配候选答案；学生的条 rollout 只有全部匹配候选答案时才作为过易题丢弃。“全部答成另一个答案”不能被泛化的 consensus 规则误删。 成本过高，不复现（审查 DONE）；诊断直接使用合成 divergence 张量，不称为 OPST loss 复现。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  On-policy distillation 自生成课程与EMA教师 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 OPST为什么只把学生全部匹配候选答案的题当作过易，全部一致但答成别的答案不能删？ 课程门要判断学生是否已掌握经过独立验证的候选答案，普通一致性只能说明回答相同。全体一致地答错仍有学习需求。教师额外线索只用于在学生前缀上评分；生成题还需独立重答与保义改写验证，不能让出题器自己的答案未经检查就成为真值。 教学例子：学生每次都给出同一个错误结果，不能因为共识很高就认定题目太容易；应先与课程已验证的候选答案对照。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-opst-37fdd7dd" class="ar-learning-paper-anchor"></span>
<h2 id="qa-36db4c81ae6babb0">OPST为什么只把学生全部匹配候选答案的题当作过易，全部一致但答成别的答案不能删？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aopst">On-Policy Self-Training: Data-Free Self-Improvement in Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>课程门要判断学生是否已掌握经过独立验证的候选答案，普通一致性只能说明回答相同。全体一致地答错仍有学习需求。教师额外线索只用于在学生前缀上评分；生成题还需独立重答与保义改写验证，不能让出题器自己的答案未经检查就成为真值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>学生每次都给出同一个错误结果，不能因为共识很高就认定题目太容易；应先与课程已验证的候选答案对照。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32770v1">原论文</a> · <a href="../../../../post-training/2610.32770-opst/">实现解读</a> · <a href="#qa-36db4c81ae6babb0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gift" data-paper-title="GIFT: Gradient Informed Filtering for Distillation Augmented Reasoning RL" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="GIFT: Gradient Informed Filtering for Distillation Augmented Reasoning RL LLM 后训练 Shanghai Jiao Tong University 2026-10-22 终局正确性驱动的 RL 梯度与教师模仿梯度可能相冲突。GIFT 在原始词表 logits 空间分解两者：先最少纳入冲突 token，再优先保留提供正交新方向的教师监督；训练逐步缩减被蒸馏的 token 数量，保留项的强度不稀释。 完整实验：成本过高，不复现（审查 DONE）。它是数值诊断，不是可晋级 Agent，也无 validation 选模 / test 能力评估。本地状态：L1 精确损失组件，diagnostic only。保留 token 级梯度几何、exact-quota 排序、coverage annealing 与 sparse top-k+tail KL；不是完整推理能力复现。完整实验：成本过高，不复现（审查 DONE）。gift_loss 实现一个 actor training sub-batch、单位 rollout IS 权重下的 clipped GRPO 与 GIFT。  On-policy distillation RL与蒸馏梯度几何 后训练算法组件 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 GIFT为什么按logit梯度几何挑token，却不能说它会永久排除所有冲突监督？ 配额优先选择不冲突且提供正交新方向的教师信号，但配额大于可用非冲突位置时，仍可能补入较弱冲突token。它做的是token选择，不是把教师梯度投影掉；保留项仍按全部有效token数归一。局部logit一阶性质不能保证共享参数有限步更新始终安全。 教学例子：一个子批次需要保留的token比完全不冲突的位置还多，算法可能选最弱冲突补齐；不能把配额选择称作零冲突保证。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-gift-0ba87e11" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b3048c4edc48d7f1">GIFT为什么按logit梯度几何挑token，却不能说它会永久排除所有冲突监督？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agift">GIFT: Gradient Informed Filtering for Distillation Augmented Reasoning RL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Jiao Tong University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>配额优先选择不冲突且提供正交新方向的教师信号，但配额大于可用非冲突位置时，仍可能补入较弱冲突token。它做的是token选择，不是把教师梯度投影掉；保留项仍按全部有效token数归一。局部logit一阶性质不能保证共享参数有限步更新始终安全。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个子批次需要保留的token比完全不冲突的位置还多，算法可能选最弱冲突补齐；不能把配额选择称作零冲突保证。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30796v1">原论文</a> · <a href="../../../../post-training/2610.30796-gift/">实现解读</a> · <a href="#qa-b3048c4edc48d7f1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:userarena-optd" data-paper-title="UserArena: Benchmarking Interactive User Simulation for Long-Horizon Shopping Agents" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="UserArena: Benchmarking Interactive User Simulation for Long-Horizon Shopping Agents LLM 后训练 Leiden University 2026-10-22 逐步动作命中率不能说明用户模拟器能否保持跨会话偏好，更不能说明模拟出来的推荐政策差异是否接近真实生产A/B。UserArena把细粒度页面、动作和跨会话记录统一成13种动作环境，分Replay与Rollout评估五层保真度：可执行性、局部行为、轨迹动态、个体群体差异和最终结果。OPTD的区别不是“直接给学生看未来轨迹”。完整训练轨迹先被提炼成抽象偏好、顾虑和比较准则，只提供给冻结教师；教师在学生自己生成的前缀上给完整词表分布。 完整实验：成本过高，不复现（审查 DONE），不自动重试。本地状态：L1 精确损失组件，diagnostic only；不是用户模拟器、购物环境或官方 benchmark 接入。完整实验：成本过高，不复现（审查 DONE），不自动重试。实现Eq.5–10完整词表几何目标、逐token二分、广义JSD、独立GT grounding、两级均值和教师detach。接受两组不同长度的学生logits；padding可含NaN但不贡献损失/梯度，有效位置必须有限、词表和配对状态必须对齐。FP16/BF16提升到FP32计算，非法空响应、越界gold与不合法预算直接拒绝。  On-policy distillation 轨迹意图与逐token信任域 Agent用户模拟 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 UserArena的OPTD为什么只把抽象意图给教师，并逐token限制它带来的分布变化？ 完整轨迹可能泄漏未来商品或动作，先提炼抽象偏好并只给冻结教师，可保持学生部署输入边界。含意图与无意图教师重放同一学生前缀，信任域限制额外指导强度，再结合真实响应grounding。KL约束不能证明意图提取器没有泄漏，内容过滤仍必须独立检查。 教学例子：教师可知道用户更看重耐用性，但不能直接拿到下一页商品ID和最终购买结果，再把这些未来动作暗示给学生。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-userarena-optd-fa417c42" class="ar-learning-paper-anchor"></span>
<h2 id="qa-c1b0f08383a3b1a7">UserArena的OPTD为什么只把抽象意图给教师，并逐token限制它带来的分布变化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Auserarena-optd">UserArena: Benchmarking Interactive User Simulation for Long-Horizon Shopping Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Leiden University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>完整轨迹可能泄漏未来商品或动作，先提炼抽象偏好并只给冻结教师，可保持学生部署输入边界。含意图与无意图教师重放同一学生前缀，信任域限制额外指导强度，再结合真实响应grounding。KL约束不能证明意图提取器没有泄漏，内容过滤仍必须独立检查。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教师可知道用户更看重耐用性，但不能直接拿到下一页商品ID和最终购买结果，再把这些未来动作暗示给学生。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30932v1">原论文</a> · <a href="../../../../post-training/2610.30932-userarena-optd/">实现解读</a> · <a href="#qa-c1b0f08383a3b1a7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ap-opd" data-paper-title="Adaptive Pullback: Reweighting Supervision at Penalty Jumps in On-Policy Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Adaptive Pullback: Reweighting Supervision at Penalty Jumps in On-Policy Distillation LLM 后训练 Nanjing University 2026-10-20 同样高的 OPD 惩罚可能是持续稳定的，也可能刚刚突增。AP-OPD 用相邻 token 块定位后一种情况，再把突增后整块监督按一个比率回拉；不增加教师 forward，不改变 token 系数的正负。均值和检测器始终读取原始、未加权统计，不能递归使用已回拉的前块。 完整实验成本过高，不复现（审查 DONE）；诊断响应长 10，块长缩为 2 以覆盖多个边界；L1 定义性损失组件，不是数学或代码能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接入 Evolve。无下载。随机初始化 12-token、8 维因果 GRU 策略实际采样响应，独立冻结教师在相同前缀重放，默认每 seed 3 次 SGD。诊断响应长 10，块长缩为 2 以覆盖多个边界；通用算子默认仍是论文。合成 token 不代表自然语言数学能力，输出不可覆盖，CUDA 不可用不回退。  On-policy distillation 蒸馏信号门控与训练稳定性 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 AP-OPD为什么检测器一直读取原始块统计，回拉时又连负系数一起缩放？ 若用已加权前块继续检测，局部回拉会递归改变后续基准，产生原方法没有的传播。检测依赖正向惩罚的原均值，但回拉作用于后块全部有符号监督，保留正负方向而减弱强度；不重新归一化，允许权重为零，也不能把门槛当校准显著性检验。 教学例子：第二块刚发生惩罚跳升而被缩小，第三块仍应与第二块原始水平比较；不能让一次缩小自动制造新的连续跳升。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-ap-opd-602f5990" class="ar-learning-paper-anchor"></span>
<h2 id="qa-0ab6844a2ad8b41b">AP-OPD为什么检测器一直读取原始块统计，回拉时又连负系数一起缩放？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aap-opd">Adaptive Pullback: Reweighting Supervision at Penalty Jumps in On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若用已加权前块继续检测，局部回拉会递归改变后续基准，产生原方法没有的传播。检测依赖正向惩罚的原均值，但回拉作用于后块全部有符号监督，保留正负方向而减弱强度；不重新归一化，允许权重为零，也不能把门槛当校准显著性检验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第二块刚发生惩罚跳升而被缩小，第三块仍应与第二块原始水平比较；不能让一次缩小自动制造新的连续跳升。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28194v1">原论文</a> · <a href="../../../../post-training/2610.28194-ap-opd/">实现解读</a> · <a href="#qa-0ab6844a2ad8b41b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:optd" data-paper-title="On-Policy Transition Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="On-Policy Transition Distillation LLM 后训练 The Hong Kong Polytechnic University 2026-10-20 最终层分布接近教师，不一定代表模型沿深度修正预测的方式接近教师。OPTD 保留最终层 OPD，再对选定浅到深 readout 的 log 概率增量施加监督。候选 token 在最终学生层选定后，全路径保持同一身份；不是每层独立 top-k，也不是隐状态 MSE。 完整实验成本过高，不复现（审查 DONE）；诊断 top-k 缩为 5，通用算子默认论文 16；L1 定义性损失组件，不是推理或代码能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接入 Evolve。无下载。随机 12-token 因果 GRU 加三个 residual-depth block，以同一个最终 LayerNorm/unembedding 构成四层 readout；实际学生采样、冻结教师同前缀重放，默认三次 SGD。诊断 top-k 缩为 5，通用算子默认论文 16；不声称该微型网络是论文 Transformer。CUDA 不可用不回退，输出不可覆盖。  On-policy distillation 层间预测转移蒸馏 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 OPTD为什么最终学生层只选一次候选token，浅深层比较时不能各自重做top-k？ 层间监督要追踪同一候选的预测如何沿深度修正，各层独立选词会把身份变化混成修正量。固定候选后比较完整词表归一化得到的log概率增量，再加最终层OPD。实际更新还有停止梯度与目的层权重，不是隐藏状态MSE，也不能随意替成精确转移KL。 教学例子：浅层偏爱词甲、深层偏爱词乙，若各自只保留最喜欢的词，就无法追踪甲的概率为何下降、乙为何上升。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-optd-ae85339e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-92cd60993660c41f">OPTD为什么最终学生层只选一次候选token，浅深层比较时不能各自重做top-k？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aoptd">On-Policy Transition Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hong Kong Polytechnic University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>层间监督要追踪同一候选的预测如何沿深度修正，各层独立选词会把身份变化混成修正量。固定候选后比较完整词表归一化得到的log概率增量，再加最终层OPD。实际更新还有停止梯度与目的层权重，不是隐藏状态MSE，也不能随意替成精确转移KL。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>浅层偏爱词甲、深层偏爱词乙，若各自只保留最喜欢的词，就无法追踪甲的概率为何下降、乙为何上升。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28048v1">原论文</a> · <a href="../../../../post-training/2610.28048-optd/">实现解读</a> · <a href="#qa-92cd60993660c41f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:projected-distillation" data-paper-title="Projected Distillation: On Learning to Solve Hard Problems from Close, Correct Targets" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Projected Distillation: On Learning to Solve Hard Problems from Close, Correct Targets LLM 后训练 University of Massachusetts 2026-10-20 困难问题的学生 rollout 可能全错，RL 得不到成功奖励；直接拟合外部完整答案又过于 off-policy。论文用 projector 最小改写学生的错误响应，经 verifier 接受后，只在变化片段做 DPO；学生自己答对的响应单独做 SFT，每轮重新采样和纠错。最小编辑只是“学生最可能生成的正确响应”的可计算近似，不保证是该优化问题的精确解。 完整实验成本过高，不复现（审查 DONE）。L1 编辑对齐、验证接口和损失公式诊断，不是语言纠错或在线闭环复现。L1 编辑对齐、验证接口和损失公式诊断，不是语言纠错或在线闭环复现。不可晋级、未接入 Evolve。完整实验成本过高，不复现（审查 DONE）。本页属于同一 10 月 21 日公告的补审。无下载和预训练模型调用。输入为合成 token pair 与随机 logits；测试用的显式 verifier 只验证已给定夹具，不扮演语言 projector。单次对齐最多一百万动态规划格，避免该诊断入口无界占内存；真实长文本流水线不在本轮范围。输出不可覆盖、最多三个 seed，CUDA 不回退。  On-policy distillation 最小修正与偏好学习 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 Projected Distillation为什么只在编辑片段做DPO，而SFT只用学生自己答对的响应？ 最小修正尽量保留学生已能生成的结构，让偏好更新聚焦真正改变的位置；经修正答案与学生自正确答案来源不同，不能混成同一种全段监督。两侧仍按各自完整因果前缀评分，未改位置直接梯度为零也不意味着共享参数完全不受影响。 教学例子：学生只在最后一个运算符出错，projector改这一处并验证；偏好学习聚焦改动，而不是把教师整段表达都重新模仿。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-projected-distillation-64e08dbb" class="ar-learning-paper-anchor"></span>
<h2 id="qa-89fafaf09dc10a31">Projected Distillation为什么只在编辑片段做DPO，而SFT只用学生自己答对的响应？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aprojected-distillation">Projected Distillation: On Learning to Solve Hard Problems from Close, Correct Targets</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Massachusetts</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最小修正尽量保留学生已能生成的结构，让偏好更新聚焦真正改变的位置；经修正答案与学生自正确答案来源不同，不能混成同一种全段监督。两侧仍按各自完整因果前缀评分，未改位置直接梯度为零也不意味着共享参数完全不受影响。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>学生只在最后一个运算符出错，projector改这一处并验证；偏好学习聚焦改动，而不是把教师整段表达都重新模仿。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.27467v1">原论文</a> · <a href="../../../../post-training/2610.27467-projected-distillation/">实现解读</a> · <a href="#qa-89fafaf09dc10a31">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gr-opd" data-paper-title="GR-OPD: Group-Relative Sequence Credit for On-Policy Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="GR-OPD: Group-Relative Sequence Credit for On-Policy Distillation LLM 后训练 Shanghai Jiao Tong University 2026-10-16 教师在每个 token 上更自信，不一定意味着整段推理更值得复制；教师与学生的推理模式不同还可能造成训练崩溃。GR-OPD 在学生轨迹上重放教师，把 log-prob 差聚合为序列分数，在同题回答之间分配相对信用；保留一部分组均值压力，以免纯中心化抹掉教师总体偏好，然后使用 clipped PPO 更新。原文方法原图建议：Figure 2 总览，保留折扣、组相对信用与广播三个阶段。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是数学推理能力复现。L1 定义性组件／梯度诊断，不是数学推理能力复现。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接 Evolve。随机初始化16词表、8维因果 GRU，教师单独随机初始化后冻结；旧学生实际为每个公开 prompt 采样长度2、3、4的回答，教师重放同一学生轨迹。不同长度用于检查逐响应均值，不提供预置候选或 gold 答案。  On-policy distillation 过程奖励与信用分配 后训练算法组件 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 GR-OPD为什么在组中心化后还保留一部分均值压力？ 纯相对中心化会抹掉教师对整组回答共同的偏好，只剩组内谁更好。保留适量均值项，使整体偏离教师的压力仍存在，再将序列信用广播到动作位置。折扣、标准化和裁剪会改变实际目标，不能直接继承未处理理论估计器的梯度保证。 教学例子：同题所有回答都明显不被教师支持，但彼此差异很小；只中心化可能几乎不更新，均值项保留共同纠偏方向。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-gr-opd-372c128f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-0c13ef09cde51e17">GR-OPD为什么在组中心化后还保留一部分均值压力？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agr-opd">GR-OPD: Group-Relative Sequence Credit for On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Jiao Tong University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>纯相对中心化会抹掉教师对整组回答共同的偏好，只剩组内谁更好。保留适量均值项，使整体偏离教师的压力仍存在，再将序列信用广播到动作位置。折扣、标准化和裁剪会改变实际目标，不能直接继承未处理理论估计器的梯度保证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同题所有回答都明显不被教师支持，但彼此差异很小；只中心化可能几乎不更新，均值项保留共同纠偏方向。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23042v1">原论文</a> · <a href="../../../../post-training/2610.23042-gr-opd/">实现解读</a> · <a href="#qa-0c13ef09cde51e17">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:simopd" data-paper-title="SimOPD: Relational Knowledge Transfer for On-Policy Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="SimOPD: Relational Knowledge Transfer for On-Policy Distillation LLM 后训练 Zhejiang University 2026-10-16 概率蒸馏只利用输出分布，直接匹配隐状态又要求学生迁就教师的坐标和维数。SimOPD 改为比较回答之间的关系：两模型分别编码同一批学生回答，在自己的空间里计算“当前回答与历史回答有多像”，再匹配这两个相似度分布。教师和学生维数可不同，不需要跨模型投影。原文 §3及算法1 原图建议：Figure 2 方法图，重点保留 paired bank 和两个独立表示空间。 完整实验成本过高，不复现（审查 DONE）；L1 定义性组件／梯度诊断，不是大模型知识迁移结果。L1 定义性组件／梯度诊断，不是大模型知识迁移结果。完整实验成本过高，不复现（审查 DONE）；不可晋级，未接 Evolve。随机初始化16词表因果 GRU，学生8维、冻结教师12维，选择 embedding 和循环状态两个层次。学生实际自回归生成回答，教师读取同一公开 prompt 与回答，不提供人工 gold 或教师生成的替代回答。每批4个回答，bank容量6，首批暖启动，之后默认3次真实优化更新。随机教师仅用来检查关系蒸馏路径，不具备预训练知识或自然语言教师能力。  On-policy distillation 跨模型表示蒸馏 后训练算法组件 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 SimOPD师生隐状态维数不同，为什么仍能做关系蒸馏，不必先投到同一坐标系？ 两边各自在自身空间计算当前回答与配对历史回答的相似度，再匹配以相同历史身份为索引的分布，比较对象不是跨模型向量本身。历史bank和教师都冻结并同步FIFO维护；只有一个历史点时分布恒定，不能提供有效关系监督。 教学例子：两位老师使用不同坐标描述回答，但都能说它更接近历史答案甲而非乙；学生学习这种关系排序，无需坐标逐项相等。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-simopd-1a5a0435" class="ar-learning-paper-anchor"></span>
<h2 id="qa-67acf86af9d51b82">SimOPD师生隐状态维数不同，为什么仍能做关系蒸馏，不必先投到同一坐标系？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asimopd">SimOPD: Relational Knowledge Transfer for On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两边各自在自身空间计算当前回答与配对历史回答的相似度，再匹配以相同历史身份为索引的分布，比较对象不是跨模型向量本身。历史bank和教师都冻结并同步FIFO维护；只有一个历史点时分布恒定，不能提供有效关系监督。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两位老师使用不同坐标描述回答，但都能说它更接近历史答案甲而非乙；学生学习这种关系排序，无需坐标逐项相等。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23306v1">原论文</a> · <a href="../../../../post-training/2610.23306-simopd/">实现解读</a> · <a href="#qa-67acf86af9d51b82">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:divergence-routed-opd" data-paper-title="Divergence-Routed On-Policy Distillation for Language Models" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Divergence-Routed On-Policy Distillation for Language Models LLM 后训练 Peking University 2026-10-14 DrOPD 在学生自己生成的轨迹上比较师生分布，以 JS 散度识别教师支持而学生严重欠覆盖的位置。它在所有位置保留 reverse-KL，并仅向高分歧位置增加 forward-KL 的纠正信号，通过候选级优势执行 PPO clipped 更新。reverse-KL 的 logit 梯度包含学生概率因子，学生几乎不给某个教师 token 概率时，纠正信号会变弱。forward-KL 的梯度为学生与教师概率之差，能继续推动这些教师模式；路由限制额外监督的位置，而不是直接把整个损失换成 forward-KL。 完整论文训练成本过高，不复现（审查 DONE）。L1 算法组件与真实在线更新诊断。L1 算法组件与真实在线更新诊断。本地执行候选并集、JS 路由和 PPO 更新；完整论文训练成本过高，不复现（审查 DONE）。与 Dr. OPD（2609.38025） 是不同论文，方法键不复用。微型 byte 自回归模型在固定公开文本上运行：教师先执行有界 next-token 训练后冻结，学生独立随机初始化，真实采样新 token，再执行上述 DrOPD 参数更新。没有预先固定响应候选、没有向模型返回标准答案；256 byte 词表只是缩小 backbone。  On-policy distillation 散度路由 Token 级监督 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 DrOPD为什么保留所有位置的reverse-KL，只在高分歧位置加forward-KL？ reverse-KL在学生已覆盖模式上提供模仿信号，但对学生几乎不给概率的教师模式可能纠正较弱。forward-KL补这类欠覆盖，JS路由限制额外干预范围。它不是把全损失换方向，也不是仅对采样词更新；候选并集、冻结优势与PPO路径共同构成实际机制。 教学例子：教师强烈支持词甲，学生几乎只选乙；仅沿学生常见词模仿可能难以抬起甲，高分歧位置的额外纠正用于补覆盖。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-divergence-routed-opd-a4becc18" class="ar-learning-paper-anchor"></span>
<h2 id="qa-3312d2d758d1406c">DrOPD为什么保留所有位置的reverse-KL，只在高分歧位置加forward-KL？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adivergence-routed-opd">Divergence-Routed On-Policy Distillation for Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>reverse-KL在学生已覆盖模式上提供模仿信号，但对学生几乎不给概率的教师模式可能纠正较弱。forward-KL补这类欠覆盖，JS路由限制额外干预范围。它不是把全损失换方向，也不是仅对采样词更新；候选并集、冻结优势与PPO路径共同构成实际机制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教师强烈支持词甲，学生几乎只选乙；仅沿学生常见词模仿可能难以抬起甲，高分歧位置的额外纠正用于补覆盖。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19572v1">原论文</a> · <a href="../../../../post-training/2610.19572-divergence-routed-opd/">实现解读</a> · <a href="#qa-3312d2d758d1406c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ig-opd" data-paper-title="Information-Gain Calibrated On-Policy Distillation for Deep Search Agents" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Information-Gain Calibrated On-Policy Distillation for Deep Search Agents LLM 后训练 The Chinese University of Hong Kong, Shenzhen 2026-10-14 普通 OPD 在检索前按教师偏好评分 query，却不知道检索结果是否有用；又按 token 数量分配预算，容易让很长的最终回答压过短而关键的搜索调用。IG-OPD 用检索后的答案置信变化校正两点：ITC 重新分配回合预算，IQC 用有符号增益修正动作关键 token 的方向。参考答案只供训练专用冻结教师探针使用，不进入学生采样上下文。原文 §4 原文 Figure 1 展示“教师不喜欢但能找到证据”的查询；Figure 2 分析 supervision budget 与信息增益失配。见原文方法图。 完整实验成本过高，不复现（审查 DONE）；L1 算法组件／梯度诊断，不是多模态搜索 Agent 复现。L1 算法组件／梯度诊断，不是多模态搜索 Agent 复现。完整实验成本过高，不复现（审查 DONE）；不进入 evolve 晋级。随机32词表策略真实采样三个回合，每回合2个 token，前两回合之后加入外部人工观察。冻结教师在初始与观察后上下文分别评分一个训练专用 reference token，真正计算势差；学生只能读提示、已采样响应和观察，不读 reference。这里只验证信息校准代数，不模拟真实 web search 的质量。  On-policy distillation Agentic RL 后训练算法组件 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 IG-OPD为什么用信息增益绝对值分预算，却用有符号增益校正query方向？ 一次检索无论显著变好还是变坏都值得关注，所以预算可依变化幅度分配；动作信用则必须区分正负后果，不能把伤害也奖励。两项相加且作用范围不同，答案只供冻结训练探针，不进学生采样；长最终回答也不该仅因token多吞掉短查询预算。 教学例子：一个查询取回误导网页，使答案支持下降，仍需分配足够监督去纠正它，但不能因为变化幅度大就给予正奖励。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-ig-opd-f18f6a41" class="ar-learning-paper-anchor"></span>
<h2 id="qa-4cddf433bec13e2a">IG-OPD为什么用信息增益绝对值分预算，却用有符号增益校正query方向？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aig-opd">Information-Gain Calibrated On-Policy Distillation for Deep Search Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Chinese University of Hong Kong, Shenzhen</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一次检索无论显著变好还是变坏都值得关注，所以预算可依变化幅度分配；动作信用则必须区分正负后果，不能把伤害也奖励。两项相加且作用范围不同，答案只供冻结训练探针，不进学生采样；长最终回答也不该仅因token多吞掉短查询预算。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个查询取回误导网页，使答案支持下降，仍需分配足够监督去纠正它，但不能因为变化幅度大就给予正奖励。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20664v1">原论文</a> · <a href="../../../../post-training/2610.20664-ig-opd/">实现解读</a> · <a href="#qa-4cddf433bec13e2a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:state-opd" data-paper-title="State-OPD: State-Grounded On-Policy Distillation for Multi-Turn Agents" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="State-OPD: State-Grounded On-Policy Distillation for Multi-Turn Agents LLM 后训练 Alibaba Group 2026-10-09 多轮OPD把旧reasoning和实际环境记录混在教师上下文中，可能继承错误推理。State-OPD只给教师已执行action/observation状态，学生仍保留完整history；在高完整词表熵状态扩采整段reasoning+action，额外action不执行。实现保留Appendix D.1实际sampled-K1双裁剪，而非打分启发式。 本页不声明未执行实验已经完成。本地对照口径：基线为冻结初始学生、同配置预算的独立root full-history OPD及无扩采对照，均已实际执行；实际监督token与耗时不同，不宣称实际总计算匹配或能力提升；实验组仅支持本页L0/L1机制，稳定相对提升不适用。  On-policy distillation Interaction-state isolation Entropy-budget allocation LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 State-OPD为什么让教师少看历史reasoning，扩采的额外action又不能真的执行？ 旧推理可能错误但环境动作与观察已真实发生，教师基于执行状态能减少继承旧思路；学生仍保留自身完整历史。高熵状态扩采用于同一状态的监督比较，若把额外action执行，会改变环境并破坏原状态对齐。这里的熵也应来自完整词表而非单词surprisal。 教学例子：学生先前误判网页内容，教师可只看真实点击与返回结果；额外生成几个候选点击用于训练评分，不意味着同时点击所有按钮。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-state-opd-163aa0d8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-4d262ea667bfbfb6">State-OPD为什么让教师少看历史reasoning，扩采的额外action又不能真的执行？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Astate-opd">State-OPD: State-Grounded On-Policy Distillation for Multi-Turn Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>旧推理可能错误但环境动作与观察已真实发生，教师基于执行状态能减少继承旧思路；学生仍保留自身完整历史。高熵状态扩采用于同一状态的监督比较，若把额外action执行，会改变环境并破坏原状态对齐。这里的熵也应来自完整词表而非单词surprisal。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>学生先前误判网页内容，教师可只看真实点击与返回结果；额外生成几个候选点击用于训练评分，不意味着同时点击所有按钮。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13238">原论文</a> · <a href="../../../../reproductions/2610.13238-state-opd/">实现解读</a> · <a href="#qa-4d262ea667bfbfb6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:opd-learning-signals" data-paper-title="Why On-Policy Distillation Sometimes Fails: Vanishing Learning Signals" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Why On-Policy Distillation Sometimes Fails: Vanishing Learning Signals LLM 后训练 University of Pennsylvania 2026-10-08 OPD 的残余差异可能仍大，但梯度提供的学习信号已变弱。论文同时记录损失、截断前梯度、两折 occupancy 估计、参数位移和逐层表征 CKA；这些是相关性诊断，不是因果证明。 3 步实跑不复现论文的 200 步平台期，也不能证明学习失败的原因。这是诊断设施，不是提高效果的新优化算法。这是诊断设施，不是提高效果的新优化算法。3 步实跑不复现论文的 200 步平台期，也不能证明学习失败的原因。Qwen3-4B 学生、公开 MOPD 教师、LoRA q/v 更新；3 步，每问题 8 条响应分成 2×4 折，最多生成 128 token。8 个独立验证问题仅用于提取表征，不生成答案。见运行说明。  On-policy distillation 学习信号诊断 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 OPD残余损失仍很大，为什么不能据此断言继续训练一定有足够学习信号？ 数值差异与可推动参数的有效梯度并不等同，饱和或覆盖变化可能让残差存在而梯度变弱。论文联合查看截断前梯度、两折估计、参数位移与表示变化；非正分母时相关比例应不定义。这些诊断提供线索，不证明某种因素已造成学习停滞。 教学例子：老师学生仍有分布差，但关键区域梯度几乎为零；只看loss曲线会以为还有很多可学内容，实际参数未明显移动。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-opd-learning-signals-810b86e8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f79a618fa17f4eb1">OPD残余损失仍很大，为什么不能据此断言继续训练一定有足够学习信号？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aopd-learning-signals">Why On-Policy Distillation Sometimes Fails: Vanishing Learning Signals</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pennsylvania</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>数值差异与可推动参数的有效梯度并不等同，饱和或覆盖变化可能让残差存在而梯度变弱。论文联合查看截断前梯度、两折估计、参数位移与表示变化；非正分母时相关比例应不定义。这些诊断提供线索，不证明某种因素已造成学习停滞。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>老师学生仍有分布差，但关键区域梯度几乎为零；只看loss曲线会以为还有很多可学内容，实际参数未明显移动。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11247">原论文</a> · <a href="../../../../post-training/2610.11247-opd-learning-signals/">实现解读</a> · <a href="#qa-f79a618fa17f4eb1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:semi-opd" data-paper-title="When Do We Need On-Policy Distillation? Distilling on Offline Student Rollouts Is Often Better" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="When Do We Need On-Policy Distillation? Distilling on Offline Student Rollouts Is Often Better LLM 后训练 UCLA / NVIDIA（论文注明实习） 2026-10-08 初始学生先一次性生成响应，教师评分缓存后固定复用。每次优化仍重新计算当前学生概率和 token 优势，不能把旧优势也一起缓存。 核心机制实现；短预算真实 checkpoint 运行只验证训练链路，不等同论文规模能力复现。完整安装、数据格式和命令见checkpoint 运行说明。  On-policy distillation Offline student rollouts LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 Semi-OPD缓存了教师评分，为什么学生概率与token优势仍要每步重算？ 固定轨迹和冻结教师可安全复用不变的评分，但学生更新后对同一token的支持会改变，教师学生差也随之改变。缓存旧优势会把过时方向反复施加，偏离定义目标。离线学生rollout能节约生成成本，却不能因此称为每步新鲜on-policy采样。 教学例子：一个词起初被学生低估，训练后已超过教师；若仍用最初的正优势，会继续推高它，而刷新差值可改变方向。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-semi-opd-2bdbc401" class="ar-learning-paper-anchor"></span>
<h2 id="qa-a786e75dec63a25d">Semi-OPD缓存了教师评分，为什么学生概率与token优势仍要每步重算？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asemi-opd">When Do We Need On-Policy Distillation? Distilling on Offline Student Rollouts Is Often Better</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UCLA / NVIDIA（论文注明实习）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定轨迹和冻结教师可安全复用不变的评分，但学生更新后对同一token的支持会改变，教师学生差也随之改变。缓存旧优势会把过时方向反复施加，偏离定义目标。离线学生rollout能节约生成成本，却不能因此称为每步新鲜on-policy采样。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个词起初被学生低估，训练后已超过教师；若仍用最初的正优势，会继续推高它，而刷新差值可改变方向。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11291">原论文</a> · <a href="../../../../post-training/2610.11291-semi-opd/">实现解读</a> · <a href="#qa-a786e75dec63a25d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dr-opd" data-paper-title="Dr. OPD: Learning What to Follow for Optimal On-Policy Distillation of Large Language Models" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Dr. OPD: Learning What to Follow for Optimal On-Policy Distillation of Large Language Models LLM 后训练 Rutgers University 2026-09-29 普通 OPD 对每个 teacher token 信号等权，但改正关键推理错误与替换同义措辞的下游价值不同。Dr. OPD 用双层优化定义“更新学生后预期 reward 最大”的 token 权重，并在每轮先闭式更新权重，再执行一次加权 OPD。 复现级别：L1 目标函数。复现级别：L1 目标函数。实现 discrepancy × reward-JVP token credit、闭式权重更新和加权 reverse-KL；未进行论文规模的双层迭代训练。本地验证权重有界、梯度有限和不同 token credit 能产生差异化权重。A100 脱敏记录见 ../../gpu-validations/dr-opd-a100-20260930.json。  On-policy distillation 双层优化 Token 权重 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 Dr. OPD为什么按下游reward对token更新方向的JVP加权，而不只看师生分歧大小？ 分歧大可能只是措辞不同，未必值得花监督预算；JVP估计沿该纠偏方向对下游回报的影响，把学习价值与差异结合。闭式权重再经限制和归一化后用于OPD。它依赖所用回报与局部近似，不能把较大权重解释为已证实的全局因果贡献。 教学例子：老师学生对结论运算符与礼貌词都分歧，只有前者改变任务奖励；单看分歧大小可能把预算花在无关表述上。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-dr-opd-97941784" class="ar-learning-paper-anchor"></span>
<h2 id="qa-7abf58626c0e76d6">Dr. OPD为什么按下游reward对token更新方向的JVP加权，而不只看师生分歧大小？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adr-opd">Dr. OPD: Learning What to Follow for Optimal On-Policy Distillation of Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Rutgers University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分歧大可能只是措辞不同，未必值得花监督预算；JVP估计沿该纠偏方向对下游回报的影响，把学习价值与差异结合。闭式权重再经限制和归一化后用于OPD。它依赖所用回报与局部近似，不能把较大权重解释为已证实的全局因果贡献。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>老师学生对结论运算符与礼貌词都分歧，只有前者改变任务奖励；单看分歧大小可能把预算花在无关表述上。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38025">原论文</a> · <a href="../../../../post-training/2609.38025-dr-opd/">实现解读</a> · <a href="#qa-7abf58626c0e76d6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:drift-opd" data-paper-title="DriftOPD: Sequence-Level Reverse-KL Distillation for One-Step VLA Policies" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="DriftOPD: Sequence-Level Reverse-KL Distillation for One-Step VLA Policies LLM 后训练 KAIST 2026-09-29 把序列级 reverse-KL 拆成当前 chunk 的一步 reverse-KL 与刻画长期动作后果的 future potential；critic 从离线 demonstrations 学习。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 objective 分解和 teacher stop-gradient；未运行机器人环境。执行 objective 分解和 teacher stop-gradient；未运行机器人环境。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  OPD VLA 长程信用 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 DriftOPD为什么在当前动作chunk的reverse-KL之外，还加入future potential？ 一步动作匹配只能比较眼前分布，无法完整反映动作对后续状态的影响。future potential由离线示范学习的critic估计长期后果，使序列级目标分解保留时间信息。critic质量和示范覆盖仍是前提，本地目标分解并未运行机器人环境验证长期控制。 教学例子：两个抓取动作当下都像教师，一个却把物体推到后续够不到的位置；仅看当前chunk相似度可能分不出长期差别。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-drift-opd-b3b01276" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1bd738afe55776dc">DriftOPD为什么在当前动作chunk的reverse-KL之外，还加入future potential？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adrift-opd">DriftOPD: Sequence-Level Reverse-KL Distillation for One-Step VLA Policies</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一步动作匹配只能比较眼前分布，无法完整反映动作对后续状态的影响。future potential由离线示范学习的critic估计长期后果，使序列级目标分解保留时间信息。critic质量和示范覆盖仍是前提，本地目标分解并未运行机器人环境验证长期控制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个抓取动作当下都像教师，一个却把物体推到后续够不到的位置；仅看当前chunk相似度可能分不出长期差别。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00317">原论文</a> · <a href="../../../../post-training/2610.00317-drift-opd/">实现解读</a> · <a href="#qa-1bd738afe55776dc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:flowmap-opd" data-paper-title="FlowMap-OPD: Rollout-Kernel Separation for On-Policy Distillation of Few-Step Flow-Map Generators" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="FlowMap-OPD: Rollout-Kernel Separation for On-Policy Distillation of Few-Step Flow-Map Generators LLM 后训练 Georgia Institute of Technology 2026-09-29 把生成状态的 rollout 分布与 teacher/student 比较 kernel 解耦：rollout 只负责提供具有正确边缘分布的状态，优化 kernel 在这些冻结状态上比较 flow map、诱导速度或瞬时速度。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 rollout state detach 与 local kernel KL；未训练图像 flow-map generator。执行 rollout state detach 与 local kernel KL；未训练图像 flow-map generator。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  On-policy distillation Flow map 生成模型 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 FlowMap-OPD为什么冻结rollout状态，只让比较kernel向学生反传？ rollout负责提供符合所需边缘分布的状态，局部kernel负责在这些状态比较flow map或速度，两者承担不同职责。若沿状态生成路径也反传，就增加了未定义的轨迹梯度项，改变估计器。状态虽停止梯度，后续仍可由更新策略重新采集，并非永久固定数据。 教学例子：先由当前生成器采一批中间状态，再冻结它们做局部教师比较；不应让该次局部损失回头穿过整个状态采样过程。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-flowmap-opd-fd47b0da" class="ar-learning-paper-anchor"></span>
<h2 id="qa-4852debd06b0bfd3">FlowMap-OPD为什么冻结rollout状态，只让比较kernel向学生反传？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aflowmap-opd">FlowMap-OPD: Rollout-Kernel Separation for On-Policy Distillation of Few-Step Flow-Map Generators</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Georgia Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>rollout负责提供符合所需边缘分布的状态，局部kernel负责在这些状态比较flow map或速度，两者承担不同职责。若沿状态生成路径也反传，就增加了未定义的轨迹梯度项，改变估计器。状态虽停止梯度，后续仍可由更新策略重新采集，并非永久固定数据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先由当前生成器采一批中间状态，再冻结它们做局部教师比较；不应让该次局部损失回头穿过整个状态采样过程。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37851">原论文</a> · <a href="../../../../post-training/2609.37851-flowmap-opd/">实现解读</a> · <a href="#qa-4852debd06b0bfd3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ipd" data-paper-title="Interpolated Policy Distillation: A Controllable Continuum Between Off-Policy and On-Policy Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Interpolated Policy Distillation: A Controllable Continuum Between Off-Policy and On-Policy Distillation LLM 后训练 WeChat Vision, Tencent 2026-09-29 在每个 token 状态把 student 与 teacher 分布按插值，从纯 on-policy 连续过渡到 off-policy teacher；论文再用验证感知的 speculative sampler 精确采样该目标策略。 高吞吐 speculative sampler 和模型训练未复现。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行精确 token mixture；高吞吐 speculative sampler 和模型训练未复现。执行精确 token mixture；高吞吐 speculative sampler 和模型训练未复现。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  策略蒸馏 分布插值 Speculative sampling LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 IPD逐token混合师生概率，为什么不等同于整条回答随机选一个教师或学生来生成？ 条件分布在每个前缀处插值，后续状态随已采到的token改变；整条轨迹只选一次来源，会产生另一种序列分布。概率混合也不同于logits平均。精确采到目标混合策略需要对应采样协议，本地端点与归一化检查没有复现高吞吐speculative sampler。 教学例子：第一步可能从教师更支持的词采到，第二步仍按新前缀重新混合；并不是开头掷一次硬币后整段只听同一个模型。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-ipd-4481efec" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b2efc7ad19f40b08">IPD逐token混合师生概率，为什么不等同于整条回答随机选一个教师或学生来生成？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aipd">Interpolated Policy Distillation: A Controllable Continuum Between Off-Policy and On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · WeChat Vision, Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>条件分布在每个前缀处插值，后续状态随已采到的token改变；整条轨迹只选一次来源，会产生另一种序列分布。概率混合也不同于logits平均。精确采到目标混合策略需要对应采样协议，本地端点与归一化检查没有复现高吞吐speculative sampler。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第一步可能从教师更支持的词采到，第二步仍按新前缀重新混合；并不是开头掷一次硬币后整段只听同一个模型。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37170">原论文</a> · <a href="../../../../post-training/2609.37170-ipd/">实现解读</a> · <a href="#qa-b2efc7ad19f40b08">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:oasis-opsd" data-paper-title="Overcoming Scaling Limits in On-Policy Self-Distillation for LLM Reasoning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Overcoming Scaling Limits in On-Policy Self-Distillation for LLM Reasoning LLM 后训练 North South University 2026-09-29 OASIS 把“在哪里监督”和“teacher 看什么 context”解耦：从同一题的 on-policy rollouts 中选最短的已验证轨迹作为 scaffold；teacher context 优先使用另一条未验证尝试；没有 verified rollout 的题不产生训练信号。这样只需要最终答案 verifier，而不需要 gold solution。 复现级别：L1 选择与损失机制。复现级别：L1 选择与损失机制。实现 shortest verified scaffold、独立同题 context 和 clipped forward-KL。测试保证未验证短轨迹不会被误选、teacher context 与 scaffold 不同、mask 外 token 无梯度。三种子机制结果见 metrics/mechanism-seeds42-44.json。未运行 Qwen3 1.7B–8B rollout/training，属于机制实现，不宣称 AIME/HMMT 增益。  On-policy self-distillation 可验证推理 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 OASIS为什么用最短已验证轨迹作scaffold，却可把另一条未验证尝试放进教师上下文？ scaffold决定在哪条可信学生轨迹上监督，教师上下文决定额外参考什么，两者被刻意解耦。未验证尝试可以提供可比较思路，但不能自动成为正确解；没有任何verified rollout的题不产生该训练信号。只需最终答案验证，也不代表学生能读取gold solution。 教学例子：同题一条短回答已通过验收，另一条探索较长但未确认；可在短回答前缀上评分，同时让教师参考探索中的信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-oasis-opsd-27f4197e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-9e59a6d301d00681">OASIS为什么用最短已验证轨迹作scaffold，却可把另一条未验证尝试放进教师上下文？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aoasis-opsd">Overcoming Scaling Limits in On-Policy Self-Distillation for LLM Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · North South University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>scaffold决定在哪条可信学生轨迹上监督，教师上下文决定额外参考什么，两者被刻意解耦。未验证尝试可以提供可比较思路，但不能自动成为正确解；没有任何verified rollout的题不产生该训练信号。只需最终答案验证，也不代表学生能读取gold solution。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同题一条短回答已通过验收，另一条探索较长但未确认；可在短回答前缀上评分，同时让教师参考探索中的信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37915">原论文</a> · <a href="../../../../post-training/2609.37915-oasis/">实现解读</a> · <a href="#qa-9e59a6d301d00681">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:ride-opd" data-paper-title="The Teacher Is a Direction, Not a Destination: Extrapolating RL-Induced Representation Residuals in On-Policy Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="The Teacher Is a Direction, Not a Destination: Extrapolating RL-Induced Representation Residuals in On-Policy Distillation LLM 后训练 原文未列机构 2026-09-29 RIDE 不在输出概率空间放大 teacher/student ratio，而是在每层每个 token 计算 RL teacher 相对其 pre-RL checkpoint 的 hidden residual：；学生回归到，其中把方向延伸到 teacher 之外。teacher/base 均 stop-gradient，避免目标分支被学生更新。 复现级别：L1 表征目标。复现级别：L1 表征目标。实现 base→RL teacher 的逐层残差外推与 masked regression。ride_target 与 ride_loss 覆盖退化、外推、mask 和 teacher stop-gradient；三种子机制结果见 metrics/mechanism-seeds42-44.json。未加载四组真实 base/RL teacher checkpoint，不能视为论文效果复现。  On-policy distillation 表征蒸馏 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 RIDE把教师超过基座的hidden residual继续外推，为什么不是放大输出概率比？ 残差定义在逐层逐token表示中，是RL教师相对其pre-RL基座的变化方向；学生回归到基座加放大残差的目标。输出概率比没有保存这条内部表示路径，不能互换。教师和基座停止梯度，外推系数超过一也不保证超过教师能力，仍需独立任务验证。 教学例子：先比较同一模型RL前后某层表示的位移，再沿该方向延长；这与把教师更喜欢的输出词统一加大权重不是一回事。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-ride-opd-b6296fc3" class="ar-learning-paper-anchor"></span>
<h2 id="qa-9eaccf1ab5755fc3">RIDE把教师超过基座的hidden residual继续外推，为什么不是放大输出概率比？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aride-opd">The Teacher Is a Direction, Not a Destination: Extrapolating RL-Induced Representation Residuals in On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>残差定义在逐层逐token表示中，是RL教师相对其pre-RL基座的变化方向；学生回归到基座加放大残差的目标。输出概率比没有保存这条内部表示路径，不能互换。教师和基座停止梯度，外推系数超过一也不保证超过教师能力，仍需独立任务验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先比较同一模型RL前后某层表示的位移，再沿该方向延长；这与把教师更喜欢的输出词统一加大权重不是一回事。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36484">原论文</a> · <a href="../../../../post-training/2609.36484-ride/">实现解读</a> · <a href="#qa-9eaccf1ab5755fc3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sipo" data-paper-title="SIPO: Unifying Reinforcement Learning with On-Policy Self-Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="SIPO: Unifying Reinforcement Learning with On-Policy Self-Distillation LLM 后训练 University of Illinois Urbana-Champaign 2026-09-29 RLVR 的轨迹 reward 稀疏，普通 OPSD 又会受自教师过度自信和长序列惩罚影响。SIPO 对同一 rollout 构造正/负两份特权上下文：两者 teacher log-prob 的差值抵消共享偏差，形成逐 token 信用；环境 reward 决定主方向，dense evidence 负责在 token 间重新分配。 复现级别：L1 目标函数。复现级别：L1 目标函数。实现双上下文 contrastive self-teacher、逐 token advantage 和 policy-gradient 组合；未执行论文规模 rollout 训练。机制测试覆盖全失败组仍有 token 信号、有限梯度及 reward 主方向。A100 脱敏记录见 ../../gpu-validations/sipo-a100-20260930.json。  RLVR On-policy self-distillation Token 信用分配 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 SIPO为什么对同一学生rollout构造正负两份教师上下文，而不只给一份正确提示？ 单份特权教师可能带有共享置信和风格偏差，正负上下文的log-prob对比尝试抵消共同部分，得到更聚焦的token证据。终局环境奖励决定主要方向，密集证据在位置间重分配；两份上下文都只用于训练评分，不能让学生原始采样读取gold。 教学例子：两种教师提示都偏爱礼貌措辞，只有涉及关键证据时支持不同；对比可减少把共同文风当作需要学习的主信号。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-sipo-d20b9ca6" class="ar-learning-paper-anchor"></span>
<h2 id="qa-272d9b14d8ce1c73">SIPO为什么对同一学生rollout构造正负两份教师上下文，而不只给一份正确提示？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asipo">SIPO: Unifying Reinforcement Learning with On-Policy Self-Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单份特权教师可能带有共享置信和风格偏差，正负上下文的log-prob对比尝试抵消共同部分，得到更聚焦的token证据。终局环境奖励决定主要方向，密集证据在位置间重分配；两份上下文都只用于训练评分，不能让学生原始采样读取gold。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两种教师提示都偏爱礼貌措辞，只有涉及关键证据时支持不同；对比可减少把共同文风当作需要学习的主信号。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36742">原论文</a> · <a href="../../../../post-training/2609.36742-sipo/">实现解读</a> · <a href="#qa-272d9b14d8ce1c73">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:lspd" data-paper-title="An RL View of OPD: Least Square Policy Distillation for Sample-Efficient LLM Reasoning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="An RL View of OPD: Least Square Policy Distillation for Sample-Efficient LLM Reasoning LLM 后训练 University of North Carolina at Chapel Hill 2026-09-28 LSPD 把教师与学生的 token log-prob 差视作可优化残差，以 least-square 形式直接收缩分布差距，并用 Huber 式尾部限制异常差值的梯度；同时允许复用历史 query-response 轨迹，提高样本效率。 未复现原作者完整 reasoning 数据管线与大规模教师 rollout，也未接入 Evolve。复现级别：L1 核心机制 + 真实 checkpoint CUDA 路径。复现级别：L1 核心机制 + 真实 checkpoint CUDA 路径。实现稳健 least-square policy-distillation 目标与离策略回放容器；不外推完整推理训练收益。未复现原作者完整 reasoning 数据管线与大规模教师 rollout，也未接入 Evolve。只有控制器能执行真实 LSPD 更新并在隔离验证集评价时，才会标为可进化算子。  On-policy distillation 离策略回放 推理 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 LSPD为什么对师生log-prob残差使用平方区间加Huber尾部，而不一律平方？ 平方项在小残差附近直接收缩差距，但极端log概率差可能产生过强梯度。线性尾部限制异常值影响，同时保留纠偏方向；回答内先平均，再跨回答等权，避免长度改变样本权重。重放旧轨迹可以节约数据，但不能把它们说成当前策略新采样。 教学例子：多数token师生接近，仅一个词被教师赋极低概率；一律平方可能让这个异常位置主导整批，而稳健尾部控制其影响。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-lspd-3161a2b9" class="ar-learning-paper-anchor"></span>
<h2 id="qa-940f981ab925625c">LSPD为什么对师生log-prob残差使用平方区间加Huber尾部，而不一律平方？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Alspd">An RL View of OPD: Least Square Policy Distillation for Sample-Efficient LLM Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of North Carolina at Chapel Hill</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>平方项在小残差附近直接收缩差距，但极端log概率差可能产生过强梯度。线性尾部限制异常值影响，同时保留纠偏方向；回答内先平均，再跨回答等权，避免长度改变样本权重。重放旧轨迹可以节约数据，但不能把它们说成当前策略新采样。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>多数token师生接近，仅一个词被教师赋极低概率；一律平方可能让这个异常位置主导整批，而稳健尾部控制其影响。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35505">原论文</a> · <a href="../../../../post-training/2609.35505-lspd/">实现解读</a> · <a href="#qa-940f981ab925625c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:recursive-opsd" data-paper-title="Recursive Self-Improvement via On-Policy Distillation for Reasoning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Recursive Self-Improvement via On-Policy Distillation for Reasoning LLM 后训练 Meta AI / University of California, Riverside 2026-09-25 传统 OPSD 让学生只看题目、冻结的特权教师额外看标准解，在学生自己的输出前缀上做逐 token 蒸馏。教师停留在初始权重时，后续学生学到的回看和纠错行为无法反哺教师。论文提出两个互补改动：DCE（动态共演化）：第 k 轮由当前学生采样回答 yᵏ；同一份当前权重、停止梯度且额外看到标准解的教师，对相同回答前缀给出分布 qᵏ。学生最小化 KL(qᵏ‖pᵏ)。更新后的权重同时成为下一轮学生和教师，教师不是独立优化的第二个模型。 本地只用公开 Qwen3-4B-Instruct-2507 与官方 GSM8K 的 4 道训练、2 道验证、2 道测试题，在 A100 上做 2 次 rank-8 更新、192-token 上限的机制诊断。本地只用公开 Qwen3-4B-Instruct-2507 与官方 GSM8K 的 4 道训练、2 道验证、2 道测试题，在 A100 上做 2 次 rank-8 更新、192-token 上限的机制诊断。seed 42，固定同一数据、步数和生成上限。稳定指标文件为 qwen3-4b-gsm8k-seed42.json。  On-policy self-distillation DCE SRCL reasoning LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 Recursive OPSD的DCE与SRCL为什么都更新同一模型，却必须给标准解划不同信息边界？ DCE用当前权重的特权教师在同一学生前缀上给分，更新后两种角色进入下一轮；SRCL则让模型只看自己的回答生成更短改写，标准解仅供验收。若把标准解给改写器，就把学习自修订变成照抄教师。两条目标互补，不是独立训练第二个教师模型。 教学例子：学生先尝试解题，教师借标准解评分；随后学生自行缩写原解，只在最终验收时检查正确，缩写提示不直接展示标准解。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-recursive-opsd-defa1333" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1cc48c02b9ecad3b">Recursive OPSD的DCE与SRCL为什么都更新同一模型，却必须给标准解划不同信息边界？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arecursive-opsd">Recursive Self-Improvement via On-Policy Distillation for Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI / University of California, Riverside</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>DCE用当前权重的特权教师在同一学生前缀上给分，更新后两种角色进入下一轮；SRCL则让模型只看自己的回答生成更短改写，标准解仅供验收。若把标准解给改写器，就把学习自修订变成照抄教师。两条目标互补，不是独立训练第二个教师模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>学生先尝试解题，教师借标准解评分；随后学生自行缩写原解，只在最终验收时检查正确，缩写提示不直接展示标准解。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.30652">原论文</a> · <a href="../../../../reproductions/2609.30652-recursive-opsd/">实现解读</a> · <a href="#qa-1cc48c02b9ecad3b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gamma-opd" data-paper-title="Beyond Token-Local Imitation: Reward-Compatible Temporal Credit Assignment for On-Policy Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Beyond Token-Local Imitation: Reward-Compatible Temporal Credit Assignment for On-Policy Distillation LLM 后训练 Tsinghua University / DiDi Voyager Labs 2026-09-15 以折扣时间信用逼近序列级 reverse-KL，再用有界奖励优势补入可验证结果。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行折扣回传和 RBM；未训练论文规模语言模型。本地执行折扣回传和 RBM；未训练论文规模语言模型。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  On-policy distillation 时间信用分配 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 Gamma-OPD为什么让教师信用沿时间折扣回传，还要补入可验证奖励优势？ 局部token模仿可能忽略当前选择对后续整条序列分布的影响，时间信用将后续教师信号纳入当前位置。可验证结果则约束模仿方向与任务回报相容，不能仅因教师更支持某词就断言正确。本地折扣和奖励组件诊断不代表完整语言模型训练或正式能力提升。 教学例子：前面一次选择导致后面连续偏离教师，信用不应只落在最后几个词；但最终正确性仍需独立验证信号约束。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-gamma-opd-41117d94" class="ar-learning-paper-anchor"></span>
<h2 id="qa-fca6a68c2c9769d1">Gamma-OPD为什么让教师信用沿时间折扣回传，还要补入可验证奖励优势？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agamma-opd">Beyond Token-Local Imitation: Reward-Compatible Temporal Credit Assignment for On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University / DiDi Voyager Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>局部token模仿可能忽略当前选择对后续整条序列分布的影响，时间信用将后续教师信号纳入当前位置。可验证结果则约束模仿方向与任务回报相容，不能仅因教师更支持某词就断言正确。本地折扣和奖励组件诊断不代表完整语言模型训练或正式能力提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>前面一次选择导致后面连续偏离教师，信用不应只落在最后几个词；但最终正确性仍需独立验证信号约束。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16937">原论文</a> · <a href="../../../../post-training/2609.16937-gamma-opd/">实现解读</a> · <a href="#qa-fca6a68c2c9769d1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:route-opd" data-paper-title="Distillation as Probability Transport: Routed On-Policy Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Distillation as Probability Transport: Routed On-Policy Distillation LLM 后训练 Tencent 2026-09-08 普通 OPD 对整个教师分布做密集匹配。RouteOPD 先识别学生高估的 source token 和低估的 destination token，再只搬运需要修正的概率质量，使监督更聚焦且可解释。 复现级别：候选策略机制诊断。复现级别：候选策略机制诊断。执行 source-to-destination 概率质量运输，不声称复现大模型推理能力。三种子结果见 metrics/arithmetic-smoke-seeds42-44.json。未执行原论文全参数模型、真实 rollout 或公开推理 benchmark；结果只证明路由算子执行且数值有限。  概率传输 OPD LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 RouteOPD把概率质量从source搬到destination，为什么不等于给所有教师高概率词加分？ source由学生相对教师的高估识别，destination对应学生的欠估，运输关注需要修正的差额，而非教师概率绝对大小。这样可以明确监督从哪里移出、向哪里补入，并保持概率口径一致。路由更可解释不代表教师正确，仍要控制支持集和任务评估。 教学例子：某词老师学生都很喜欢，未必需要再强化；另一个词教师支持却被学生忽略，才可能成为从高估区域补入的目的地。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-route-opd-eaed8417" class="ar-learning-paper-anchor"></span>
<h2 id="qa-2e92fef1b286ea86">RouteOPD把概率质量从source搬到destination，为什么不等于给所有教师高概率词加分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aroute-opd">Distillation as Probability Transport: Routed On-Policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>source由学生相对教师的高估识别，destination对应学生的欠估，运输关注需要修正的差额，而非教师概率绝对大小。这样可以明确监督从哪里移出、向哪里补入，并保持概率口径一致。路由更可解释不代表教师正确，仍要控制支持集和任务评估。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某词老师学生都很喜欢，未必需要再强化；另一个词教师支持却被学生忽略，才可能成为从高估区域补入的目的地。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08337">原论文</a> · <a href="../../../../post-training/2609.08337-route-opd/">实现解读</a> · <a href="#qa-2e92fef1b286ea86">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:opd-search-plus" data-paper-title="OPDSearch+: Search-Enhanced On-Policy Distillation with Reinforcement Learning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="OPDSearch+: Search-Enhanced On-Policy Distillation with Reinforcement Learning LLM 后训练 University of Chinese Academy of Sciences 2026-08-25 搜索 Agent 的多轮 SFT 数据昂贵，任务专用教师又需先训练。OPDSearch+ 直接冻结通用 instruct teacher，在学生自己的在线搜索轨迹上用 forward-KL 蒸馏 query、推理和答案 token；随后 RL 从更好的行为分布继续优化，突破教师与纯 RL 的局部最优。 复现级别：核心机制 candidate-policy。复现级别：核心机制 candidate-policy。实际执行 clipped forward-KL 与后续 verifier RL 两阶段目标；未训练 Qwen2.5-3B 搜索 Agent。本地用候选级 process signal 代替真实 query/reasoning/answer token 与搜索引擎反馈；未运行 3B/14B 模型、Wikipedia index 或七个 QA benchmark。arithmetic-smoke、100 steps、seed 42：accuracy 0.1953 → 0.6641。  搜索增强 OPD + RL LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 OPDSearch+为什么先用冻结通用教师蒸馏，再让搜索Agent继续RL？ 蒸馏先在学生自己的搜索轨迹上提供较密指导，改善query、推理与答案的行为起点；后续可验证RL再按环境结果调整，不必永久受教师偏好限制。通用教师无需先训练成任务专家，但其评分仍可能有偏，本地候选信号没有重现真实搜索引擎链路。 教学例子：先学会提出可用查询，再让检索结果与最终验收纠正查询习惯；不能把教师最喜欢的query直接当作最有效搜索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-opd-search-plus-8653157e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-094d17fb80fe1ba6">OPDSearch+为什么先用冻结通用教师蒸馏，再让搜索Agent继续RL？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aopd-search-plus">OPDSearch+: Search-Enhanced On-Policy Distillation with Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>蒸馏先在学生自己的搜索轨迹上提供较密指导，改善query、推理与答案的行为起点；后续可验证RL再按环境结果调整，不必永久受教师偏好限制。通用教师无需先训练成任务专家，但其评分仍可能有偏，本地候选信号没有重现真实搜索引擎链路。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先学会提出可用查询，再让检索结果与最终验收纠正查询习惯；不能把教师最喜欢的query直接当作最有效搜索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24310">原论文</a> · <a href="../../../../post-training/2608.24310-opd-search-plus/">实现解读</a> · <a href="#qa-094d17fb80fe1ba6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:opdvr" data-paper-title="OPDVR: On-Policy Distillation with Verifiable Rewards" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="OPDVR: On-Policy Distillation with Verifiable Rewards LLM 后训练 LeapLab, Tsinghua University 2026-08-25 Sampled-token OPD 的隐式奖励由教师/学生概率比决定，可能给正确轨迹负奖励、给错误轨迹正奖励。OPDVR 不再额外混合一个 RL loss，而是直接用 verifier correctness 对该隐式奖励做单侧 ReLU：正确轨迹只保留非负教师信号，错误轨迹只保留非正信号。 复现级别：核心机制 candidate-policy。复现级别：核心机制 candidate-policy。实际执行 sampled-token 隐式奖励和 correctness-aware ReLU gate，不用加权超参数拼接 OPD/RLVR。使用候选策略和精确 outcome 代理 token rollout；未运行 Qwen3、六个数学 benchmark 或真实 verifier rollout。arithmetic-smoke、100 steps、seed 42：accuracy 0.1953 → 0.6641，最终 KL(reference) 0.0018。单 seed 只验证 gate 与更新方向。  可验证奖励 OPD LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 OPDVR为什么对正确轨迹只保留非负教师信号，对错误轨迹只保留非正信号？ 采样token的师生log比可能与整条轨迹正确性冲突，例如教师不喜欢学生的正确写法。单侧ReLU用verifier校正隐式奖励符号，而不是再简单叠加一个独立RL loss。轨迹标签仍粗，不能证明其中每个token都正确；verifier也只在训练评分边界使用。 教学例子：学生用不同但正确的解法，教师给出负模仿信号；正确性门可挡住这类负向更新，而不要求学生照搬教师表达。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-opdvr-c33841ab" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1fbc2e745458cd71">OPDVR为什么对正确轨迹只保留非负教师信号，对错误轨迹只保留非正信号？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aopdvr">OPDVR: On-Policy Distillation with Verifiable Rewards</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LeapLab, Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>采样token的师生log比可能与整条轨迹正确性冲突，例如教师不喜欢学生的正确写法。单侧ReLU用verifier校正隐式奖励符号，而不是再简单叠加一个独立RL loss。轨迹标签仍粗，不能证明其中每个token都正确；verifier也只在训练评分边界使用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>学生用不同但正确的解法，教师给出负模仿信号；正确性门可挡住这类负向更新，而不要求学生照搬教师表达。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24696">原论文</a> · <a href="../../../../post-training/2608.24696-opdvr/">实现解读</a> · <a href="#qa-1fbc2e745458cd71">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:r2-opd" data-paper-title="Beyond Imitation: Filtering On-Policy Distillation by Reasoning Progress" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Beyond Imitation: Filtering On-Policy Distillation by Reasoning Progress LLM 后训练 Authors did not disclose affiliation 2026-08-19 分别按教师奖励和独立进展奖励排序 reasoning spans，冲突时屏蔽蒸馏信号。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  OPD 过程蒸馏 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 R²-OPD为什么要求教师排序与独立推理进展排序一致，冲突时不直接信教师？ 教师偏爱某段表达不一定意味着它推进了求解，独立进展信号用于检验两者方向。排序冲突时屏蔽对应蒸馏，减少模仿与任务目标相悖的更新。过滤只说明该信号不可靠，不证明被屏蔽段落一定错误；进展评价本身也需要独立质量检查。 教学例子：教师偏爱流畅的长解释，但进展评估显示关键约束尚未解决；此时不应仅因教师高分就强化整段表达。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-r2-opd-a6acbe83" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d2ad241badb27cb1">R²-OPD为什么要求教师排序与独立推理进展排序一致，冲突时不直接信教师？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Ar2-opd">Beyond Imitation: Filtering On-Policy Distillation by Reasoning Progress</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>教师偏爱某段表达不一定意味着它推进了求解，独立进展信号用于检验两者方向。排序冲突时屏蔽对应蒸馏，减少模仿与任务目标相悖的更新。过滤只说明该信号不可靠，不证明被屏蔽段落一定错误；进展评价本身也需要独立质量检查。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教师偏爱流畅的长解释，但进展评估显示关键约束尚未解决；此时不应仅因教师高分就强化整段表达。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.19408">原论文</a> · <a href="../../../../post-training/2608.19408-r2-opd/">实现解读</a> · <a href="#qa-d2ad241badb27cb1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:sr-opsd" data-paper-title="SR-OPSD: Self-Referenced On-Policy Self-Distillation" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="SR-OPSD: Self-Referenced On-Policy Self-Distillation LLM 后训练 Independent Researcher 2026-08-10 把自教师与 reference 做几何插值得到有效目标，再用 Rényi divergence 控制投影几何和密度比敏感度。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  OPD 自蒸馏 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 SR-OPSD为什么对自教师和reference做几何插值，而不是把两份概率直接平均？ 几何插值在log空间组合支持，归一化后形成有效目标，与线性概率混合对尾部和相互冲突模式的处理不同。reference提供锚点，自教师提供额外指导，再由散度控制投影敏感度。更换混合方式会改变目标，不能只因端点相同就视为同一个算法。 教学例子：两个分布各自强烈支持不同词，几何组合与各取一半的概率平均可能给出很不一样的中间目标，需明确所用形式。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-sr-opsd-5465332e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-bd8058cd01b40f35">SR-OPSD为什么对自教师和reference做几何插值，而不是把两份概率直接平均？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Asr-opsd">SR-OPSD: Self-Referenced On-Policy Self-Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Independent Researcher</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>几何插值在log空间组合支持，归一化后形成有效目标，与线性概率混合对尾部和相互冲突模式的处理不同。reference提供锚点，自教师提供额外指导，再由散度控制投影敏感度。更换混合方式会改变目标，不能只因端点相同就视为同一个算法。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个分布各自强烈支持不同词，几何组合与各取一半的概率平均可能给出很不一样的中间目标，需明确所用形式。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.09745">原论文</a> · <a href="../../../../post-training/2608.09745-sr-opsd/">实现解读</a> · <a href="#qa-bd8058cd01b40f35">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:dash" data-paper-title="DASH" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="DASH LLM 后训练 Nanjing University 2026-08-06 普通 OPSD 对每个 token 独立匹配 privileged teacher，难把后续可靠推理对前面决策的信用传回去。DASH 由局部 teacher/student divergence 产生停止梯度 gate，再从后向前递推聚合权重；不增加 teacher forward pass，却获得自适应 distillation horizon。 Fidelity：核心机制复现。实现局部散度裁剪、stop-gradient gate 与反向 horizon 聚合；候选位置代理 token 位置。候选位置不是完整 token trajectory；未复刻 Qwen3、数学推理语料和多卡训练。Arithmetic candidate suite、120 steps、seed 42：accuracy 0.2344 → 0.5781（+146.67%），最后 gate mean 0.4822、平均 horizon coefficient 1.5617、额外 teacher forward 为 0。  自适应自蒸馏 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 DASH为什么由局部分歧控制向后递推的horizon，而不固定把后续所有信号都传回？ 后续教师反馈可能有用，也可能因局部偏离而不可靠。停止梯度gate依据局部分歧调节传播强度，使不同位置看到不同有效监督范围，而无需额外教师前向。固定长horizon会一律混入远处信号，固定短horizon又可能漏掉重要后果，gate本身也不是真值判断。 教学例子：连续几步与教师一致时可累积后续帮助，某处突然严重分歧时应弱化继续回传；不是每个位置都用同一个窗口。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-dash-1d95c042" class="ar-learning-paper-anchor"></span>
<h2 id="qa-67cd03485d3aa1a0">DASH为什么由局部分歧控制向后递推的horizon，而不固定把后续所有信号都传回？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Adash">DASH</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>后续教师反馈可能有用，也可能因局部偏离而不可靠。停止梯度gate依据局部分歧调节传播强度，使不同位置看到不同有效监督范围，而无需额外教师前向。固定长horizon会一律混入远处信号，固定短horizon又可能漏掉重要后果，gate本身也不是真值判断。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>连续几步与教师一致时可累积后续帮助，某处突然严重分歧时应弱化继续回传；不是每个位置都用同一个窗口。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06243">原论文</a> · <a href="../../../../post-training/2608.06243-dash/">实现解读</a> · <a href="#qa-67cd03485d3aa1a0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:opd2" data-paper-title="On-Policy Delta Distillation for Multilingual Math Reasoning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="On-Policy Delta Distillation for Multilingual Math Reasoning LLM 后训练 NAVER AI Lab 2026-08-06 以 post-trained teacher 相对其 base model 的概率增量作为蒸馏信号，减少复制教师原有偏差。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  OPD 多语言推理 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 OPD²为什么蒸馏后训练教师相对其base的增量，而不复制教师全部偏好？ 教师原本就有语言、风格和知识倾向，学生直接模仿会把这些与后训练新增能力一起搬走。比较教师前后log概率变化，目标更聚焦训练带来的方向。base与teacher必须是可比阶段，增量也不是已证明的纯能力信号，本地小分布诊断不能证明跨语言迁移。 教学例子：教师一直偏好某种客套开头，而RL主要改善推理结尾；前后增量可减少把原有客套风格当新增能力传给学生。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-opd2-d840d7f7" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1c97a90289933840">OPD²为什么蒸馏后训练教师相对其base的增量，而不复制教师全部偏好？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aopd2">On-Policy Delta Distillation for Multilingual Math Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NAVER AI Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>教师原本就有语言、风格和知识倾向，学生直接模仿会把这些与后训练新增能力一起搬走。比较教师前后log概率变化，目标更聚焦训练带来的方向。base与teacher必须是可比阶段，增量也不是已证明的纯能力信号，本地小分布诊断不能证明跨语言迁移。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教师一直偏好某种客套开头，而RL主要改善推理结尾；前后增量可减少把原有客套风格当新增能力传给学生。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05802">原论文</a> · <a href="../../../../post-training/2608.05802-opd2/">实现解读</a> · <a href="#qa-1c97a90289933840">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:rp-opsd" data-paper-title="RP-OPSD" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="RP-OPSD LLM 后训练 Nanjing University 2026-08-06 跨语言迁移中，表面措辞与真正改变推理状态的 pivot 不应同权。RP-OPSD 比较带英文参考解与去掉参考解的匹配教师视图，用分布位移定位 pivot，再在这些位置强化 privileged distillation 并保留 reference anchor。 诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现 reference-conditioned / ablated 双视图、pivot gate 与 reference anchor。  推理枢纽蒸馏 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 RP-OPSD为什么比较有无英文参考解的匹配教师视图来找pivot，而不统一强化全部译文token？ 参考解对某位置分布造成的变化提供它是否改变推理状态的线索，而表面翻译词可能几乎不受影响。定位后集中进行特权蒸馏，并保留reference锚定。两视图应匹配其他条件，参考解仅在训练教师侧使用，不能让目标语学生直接照抄金标。 教学例子：跨语言答案里，连接词的翻译与决定运算顺序的词作用不同；加入参考解后，真正推理转折位置可能变化更明显。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-rp-opsd-6ed9619b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-e5b5363bc9a06ac0">RP-OPSD为什么比较有无英文参考解的匹配教师视图来找pivot，而不统一强化全部译文token？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arp-opsd">RP-OPSD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>参考解对某位置分布造成的变化提供它是否改变推理状态的线索，而表面翻译词可能几乎不受影响。定位后集中进行特权蒸馏，并保留reference锚定。两视图应匹配其他条件，参考解仅在训练教师侧使用，不能让目标语学生直接照抄金标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>跨语言答案里，连接词的翻译与决定运算顺序的词作用不同；加入参考解后，真正推理转折位置可能变化更明显。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06347">原论文</a> · <a href="../../../../post-training/2608.06347-rp-opsd/">实现解读</a> · <a href="#qa-e5b5363bc9a06ac0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:u-opsd" data-paper-title="U-OPSD" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="U-OPSD LLM 后训练 University of California, San Diego 2026-08-06 U-OPSD 不使用答案、环境奖励或更大教师。模型多次采样后做多数投票，以最短一致解作为 privileged view，定点修复最长且高置信错误轨迹，是真正依赖内部一致性的自蒸馏。 诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现多 rollout 自一致投票、置信门控与无 gold 伪教师；公开算术 mini-suite 上该无监督假设并不成立，因此如实记录退化结果。  无监督自蒸馏 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 U-OPSD用最短一致解构造特权视图，没有gold时怎样避免把“共识”说成真值？ 多次采样的内部一致性用于选参照与决定何处修复，减少对外部教师和答案的依赖；它提供的是伪监督，不是独立正确性验证。全体共同犯错仍可能被强化，所以应分开报告内部一致性与外部留出任务表现，不能向学生输入隐藏金标来弥补。 教学例子：几份回答都采用同一错误公式，最短的那份仍可能错；“最短一致解”只确定内部参照，不自动成为标准解。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-u-opsd-4619f519" class="ar-learning-paper-anchor"></span>
<h2 id="qa-4ad69881270380a9">U-OPSD用最短一致解构造特权视图，没有gold时怎样避免把“共识”说成真值？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Au-opsd">U-OPSD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多次采样的内部一致性用于选参照与决定何处修复，减少对外部教师和答案的依赖；它提供的是伪监督，不是独立正确性验证。全体共同犯错仍可能被强化，所以应分开报告内部一致性与外部留出任务表现，不能向学生输入隐藏金标来弥补。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>几份回答都采用同一错误公式，最短的那份仍可能错；“最短一致解”只确定内部参照，不自动成为标准解。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06296">原论文</a> · <a href="../../../../post-training/2608.06296-u-opsd/">实现解读</a> · <a href="#qa-4ad69881270380a9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:causal-opd" data-paper-title="CausalOPD: First-Wrong-Step Supervision for Distilling Causal Chain Reasoning" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="CausalOPD: First-Wrong-Step Supervision for Distilling Causal Chain Reasoning LLM 后训练 Authors did not disclose affiliation 2026-08-04 教师定位 on-policy 因果链第一个错误步骤，以短 horizon RL 修复，并按证据→机制→结论推进课程。 复现级别：核心目标 candidate-policy mini-suite。复现级别：核心目标 candidate-policy mini-suite。本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 runs/post-training/，仓库只提交指标，不提交 checkpoint。另见 ../../experiments/。  OPD 过程监督 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 CausalOPD为什么优先定位第一个错误步骤，再用短horizon修复？ 因果链一旦前面出现错误，后续很多步骤可能只是沿错前提继续，逐项模仿末端结论难以修正源头。先定位首错，把短程更新集中到这一转折，再组织证据到机制到结论的课程。教师定位仍可能有误，本地候选诊断也不等于自然语言因果推理能力。 教学例子：把相关性误当因果发生在开头，后面推导虽工整仍基于错前提；应先修这一跳，而非只改最后一句。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-causal-opd-da48af2a" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f522c88f42ea42cb">CausalOPD为什么优先定位第一个错误步骤，再用短horizon修复？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Acausal-opd">CausalOPD: First-Wrong-Step Supervision for Distilling Causal Chain Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Authors did not disclose affiliation</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>因果链一旦前面出现错误，后续很多步骤可能只是沿错前提继续，逐项模仿末端结论难以修正源头。先定位首错，把短程更新集中到这一转折，再组织证据到机制到结论的课程。教师定位仍可能有误，本地候选诊断也不等于自然语言因果推理能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把相关性误当因果发生在开头，后面推导虽工整仍基于错前提；应先修这一跳，而非只改最后一句。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03673">原论文</a> · <a href="../../../../post-training/2608.03673-causal-opd/">实现解读</a> · <a href="#qa-f522c88f42ea42cb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:pcsd" data-paper-title="PCSD" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="PCSD LLM 后训练 论文未列机构 2026-08-03 单 token teacher gap 容易受噪声影响，整步共享权重又会抹掉位置差异。PCSD 在自适应窗口内指数累积 teacher-favoring signal，并对下降趋势衰减，最后用连续 sigmoid gate 与 GRPO 联合训练。 诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现指数持续证据、趋势衰减与连续门控，候选位置作为 token 位置代理。  持续一致性蒸馏 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 PCSD为什么累积一段持续的teacher-favoring信号，而不看到单token gap就开关监督？ 单点师生差容易受概率噪声影响，整轮共用权重又会丢掉位置差异。窗口内指数累积与下降趋势衰减折中这两点，再通过连续gate控制OPSD与GRPO结合。持续支持仍不保证教师正确，平滑只是稳定信号，不应被当作额外独立验证。 教学例子：一个词偶然被教师高估，周围位置却不支持该方向；与连续一段都支持相比，监督强度不必相同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-pcsd-bac5e7a6" class="ar-learning-paper-anchor"></span>
<h2 id="qa-285b4151125240b5">PCSD为什么累积一段持续的teacher-favoring信号，而不看到单token gap就开关监督？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Apcsd">PCSD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单点师生差容易受概率噪声影响，整轮共用权重又会丢掉位置差异。窗口内指数累积与下降趋势衰减折中这两点，再通过连续gate控制OPSD与GRPO结合。持续支持仍不保证教师正确，平滑只是稳定信号，不应被当作额外独立验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个词偶然被教师高估，周围位置却不支持该方向；与连续一段都支持相比，监督强度不必相同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01837">原论文</a> · <a href="../../../../post-training/2608.01837-pcsd/">实现解读</a> · <a href="#qa-285b4151125240b5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:beta-opsd" data-paper-title="β-OPSD" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="β-OPSD LLM 后训练 University of Maryland, College Park 2026-07-30 论文指出 vanilla OPSD 是 β=1 的 KL 正则策略优化特例。先推导 reference policy 与 privileged teacher 之间的最优几何插值，再把昂贵高方差的 RL 解转成 token-logit 蒸馏目标，并以 return-to-go 做长推理信用分配。 保真度：实现 reference/privileged teacher 几何插值、可控 β 与 return-to-go 权重；保真度：实现 reference/privileged teacher 几何插值、可控 β 与 return-to-go 权重；不冒充论文 Qwen3 训练。候选动作对应 token 分布，线性 return-to-go 代理序列位置；未复刻 Qwen3、LoRA 和 A6000/H200 训练。本地对照口径：同一 GSM8K candidate-policy、120 steps、seed 42；相对未训练基线 accuracy 从 0.1719 到 0.7656（+345.45%）。  On-policy self-distillation LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 β-OPSD为什么把reference和特权教师的插值与return-to-go放进同一推导？ 几何插值规定在基准策略与特权指导间向哪里靠近，return-to-go则决定后续蒸馏差异怎样影响更早选择，两者分别控制目标和时间信用。vanilla设置只是其中一种参数情形，不能把任意logit平均都称为同一最优解；本地位置代理也不是完整长序列。 教学例子：先决定学生要多大程度靠近教师，再考虑开头选择会不会引发后面连续偏差；目标强度与回传范围是两件事。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-beta-opsd-d0fa334d" class="ar-learning-paper-anchor"></span>
<h2 id="qa-0f8dd46538565b98">β-OPSD为什么把reference和特权教师的插值与return-to-go放进同一推导？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Abeta-opsd">β-OPSD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Maryland, College Park</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>几何插值规定在基准策略与特权指导间向哪里靠近，return-to-go则决定后续蒸馏差异怎样影响更早选择，两者分别控制目标和时间信用。vanilla设置只是其中一种参数情形，不能把任意logit平均都称为同一最优解；本地位置代理也不是完整长序列。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先决定学生要多大程度靠近教师，再考虑开头选择会不会引发后面连续偏差；目标强度与回传范围是两件事。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28582">原论文</a> · <a href="../../../../post-training/2607.28582-beta-opsd/">实现解读</a> · <a href="#qa-0f8dd46538565b98">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:flux-opd" data-paper-title="Flux-OPD" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Flux-OPD LLM 后训练 Peking University 2026-07-30 固定上下文很快被学生吸收，直接更换上下文 teacher 又会让目标跳变。Flux-OPD 固定 context-free teacher 为锚，只注入多个演化上下文 teacher 相对锚点的 log-probability 差，并用几何均值归一化常数表示冲突、冲突越大修正越弱。 保真度：实现 context-free anchor、几何 teacher、contextual correction 与 conflict weighting。本地两个 reward axis 代理演化上下文 teacher；未调用视频模型、医疗 teacher 或大模型上下文抽取。本地对照口径：同一 GSM8K candidate-policy、120 steps、seed 42；accuracy 从 0.1719 到 0.8438（+390.91%）。  Context distillation LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 Flux-OPD为什么固定context-free锚点，再对演化上下文的修正做冲突加权？ 直接替换教师上下文会让目标跳变，固定锚点使每轮只注入相对差异；多个上下文教师的几何组合反映共同支持，冲突大时减弱修正。几何归一化常数承担冲突线索，不等于任意两教师的意见差；本地奖励轴代理也未执行真实上下文抽取。 教学例子：两份提示分别建议相反的推理路径，保留通用锚点并减弱冲突修正，比每轮完全追随新提示更能控制目标漂移。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-flux-opd-da1bf9b3" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1307998183aef378">Flux-OPD为什么固定context-free锚点，再对演化上下文的修正做冲突加权？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aflux-opd">Flux-OPD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直接替换教师上下文会让目标跳变，固定锚点使每轮只注入相对差异；多个上下文教师的几何组合反映共同支持，冲突大时减弱修正。几何归一化常数承担冲突线索，不等于任意两教师的意见差；本地奖励轴代理也未执行真实上下文抽取。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两份提示分别建议相反的推理路径，保留通用锚点并减弱冲突修正，比每轮完全追随新提示更能控制目标漂移。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28022">原论文</a> · <a href="../../../../post-training/2607.28022-flux-opd/">实现解读</a> · <a href="#qa-1307998183aef378">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:relay-opd" data-paper-title="Relay-OPD" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="Relay-OPD LLM 后训练 Zhejiang University 2026-07-28 检测学生前缀失效后让教师短暂接管，再把轨迹交还学生；有限接力预算把监督集中到关键早期位置。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。本地教师是可复现的候选分布缓存，并非 Qwen3-4B；因此验证接力状态机和监督方向，不冒充论文八卡训练。GSM8K candidate-policy 上实现失效前缀检测、教师 handoff、有限 relay budget 和学生恢复生成；与同一未训练策略公平比较。  On-policy distillation LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 Relay-OPD教师短暂接管后又还给学生，为什么不能把接力轨迹算作纯学生rollout？ 接管区间的动作来自教师，后续学生又处在教师改变过的前缀中，整条轨迹是混合来源。接力预算让监督集中于关键失效位置，状态机须记录谁生成哪些片段。它能减少无效探索，但不能把外部帮助当成学生独立成功，更不能在评测时隐瞒教师调用成本。 教学例子：学生卡在第一步，老师带过两步后学生继续；最终答对并不表示学生从无帮助状态也会走到同样结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-relay-opd-4c82d340" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f4000dc4715f9afd">Relay-OPD教师短暂接管后又还给学生，为什么不能把接力轨迹算作纯学生rollout？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Arelay-opd">Relay-OPD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>接管区间的动作来自教师，后续学生又处在教师改变过的前缀中，整条轨迹是混合来源。接力预算让监督集中于关键失效位置，状态机须记录谁生成哪些片段。它能减少无效探索，但不能把外部帮助当成学生独立成功，更不能在评测时隐瞒教师调用成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>学生卡在第一步，老师带过两步后学生继续；最终答对并不表示学生从无帮助状态也会走到同样结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26057">原论文</a> · <a href="../../../../post-training/2607.26057-relay-opd/">实现解读</a> · <a href="#qa-f4000dc4715f9afd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:opd-lm" data-paper-title="OPDLM" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="OPDLM LLM 后训练 Texas A&amp;M University 2026-06-04 ARLM 改成双向注意力后既会遗忘原知识，也有随机 mask 训练与 confidence decoding 推理之间的偏移。OPDLM 让双向学生在自身推理轨迹上生成，冻结 AR 教师在同一轨迹给 target logits。 诊断字段完整记录在固定指标文件中。Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。用相邻候选状态模拟双向去噪视图，保留冻结 AR teacher anchor；不冒充完整 diffusion decoder。  AR-to-Diffusion 蒸馏 LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 OPDLM为什么要沿双向学生自己的解码轨迹蒸馏，而不只用随机mask复刻AR教师？ 随机mask训练状态与confidence decoding实际访问状态不同，直接改注意力还可能遗忘原知识。让学生按自身解码过程产生状态，再由冻结AR教师提供对应目标，可减少这类状态错配。教师仍按自己的因果条件评分，不能把不同可见信息的分布随意逐位等同。 教学例子：学生推理时先填高置信位置，训练却总随机遮词；两种顺序会形成不同上下文，蒸馏需要面对实际解码状态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-opd-lm-752e6c98" class="ar-learning-paper-anchor"></span>
<h2 id="qa-9e0f2193c9ec3461">OPDLM为什么要沿双向学生自己的解码轨迹蒸馏，而不只用随机mask复刻AR教师？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aopd-lm">OPDLM</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Texas A&amp;M University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>随机mask训练状态与confidence decoding实际访问状态不同，直接改注意力还可能遗忘原知识。让学生按自身解码过程产生状态，再由冻结AR教师提供对应目标，可减少这类状态错配。教师仍按自己的因果条件评分，不能把不同可见信息的分布随意逐位等同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>学生推理时先填高置信位置，训练却总随机遮词；两种顺序会形成不同上下文，蒸馏需要面对实际解码状态。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.06712">原论文</a> · <a href="../../../../post-training/2606.06712-opd-lm/">实现解读</a> · <a href="#qa-9e0f2193c9ec3461">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:gkd" data-paper-title="GKD" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="GKD LLM 后训练 Google DeepMind 2023-06-23 固定教师轨迹会让学生训练时看到的前缀与推理时自身生成的前缀不一致。GKD 让学生生成当前策略轨迹，再让教师在这些学生实际访问的状态给出完整分布；同时用 student data fraction 在固定数据和 on-policy 数据之间插值，并允许 forward KL、reverse KL 或广义 JSD。 保真度：本地实现了学生 on-policy 采样、教师对学生访问状态打分、on/off-policy 混合和散度诊断；保真度：本地实现了学生 on-policy 采样、教师对学生访问状态打分、on/off-policy 混合和散度诊断；当前是候选策略机制复现，不等同于 T5-XL 到小模型的 token 级蒸馏。本地候选项对应可审计的学生轨迹支撑集，教师分布由 GSM8K 结果与过程质量构造；没有训练真实自回归 T5，也没有复跑 XSum/WMT。因此本地百分比只能验证数据流和目标函数，不能与论文指标横向比较。稳定指标见 classic-agentic-rl-opd-seed42.json。  经典 On-policy distillation LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 GKD让教师给学生前缀打分，为什么比只学教师完整答案更能覆盖学生自身错误？ 教师轨迹常避开学生会遇到的偏离状态，固定答案训练因此有分布错配。学生自己采样后，教师在相同前缀上给出分布，监督可以到达这些状态；混合比例再控制固定与在策略数据。覆盖改善不保证教师能从所有错误前缀恢复，也不自动决定应选哪种散度。 教学例子：学生先写错一步后才需要纠偏，而教师标准解从不经过这一步；在学生前缀评分能针对这个已发生的状态提供帮助。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-gkd-c556ce32" class="ar-learning-paper-anchor"></span>
<h2 id="qa-8925a124ecc2e55c">GKD让教师给学生前缀打分，为什么比只学教师完整答案更能覆盖学生自身错误？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Agkd">GKD</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>教师轨迹常避开学生会遇到的偏离状态，固定答案训练因此有分布错配。学生自己采样后，教师在相同前缀上给出分布，监督可以到达这些状态；混合比例再控制固定与在策略数据。覆盖改善不保证教师能从所有错误前缀恢复，也不自动决定应选哪种散度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>学生先写错一步后才需要纠偏，而教师标准解从不经过这一步；在学生前缀评分能针对这个已发生的状态提供帮助。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2306.13649">原论文</a> · <a href="../../../../post-training/2306.13649-gkd/">实现解读</a> · <a href="#qa-8925a124ecc2e55c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="post-training:minillm" data-paper-title="MiniLLM" data-learning-pending="false" data-domain="post-training" data-theme="post-training" data-topic="post-training/student-trajectory-distillation" data-search="MiniLLM LLM 后训练 Tsinghua University 2023-06-14 标准 forward KL 倾向覆盖教师所有概率质量，小学生可能因此高估教师的低概率区域。MiniLLM 改用 mode-seeking 的 reverse KL，在学生自身生成分布上优化，并通过 teacher-mixed sampling、单步分解、长度归一化和 reward baseline 稳定策略梯度。 保真度：实现学生 rollout 上的 reverse KL、teacher-mixed sampling、方差缩减 baseline 和长度归一化诊断；保真度：实现学生 rollout 上的 reverse KL、teacher-mixed sampling、方差缩减 baseline 和长度归一化诊断；当前未训练论文中的 120M–13B 自回归模型。候选策略可以验证 reverse KL 的采样与梯度方向，但没有真实 tokenizer、长文本生成和 GPT-4 judge。本地 accuracy 不是论文的生成质量分数。稳定指标见 classic-agentic-rl-opd-seed42.json。  Reverse-KL distillation LLM 后训练 在策略蒸馏：沿学生实际走过的前缀学习 MiniLLM的reverse-KL为什么对小学生与教师尾部概率的关系有影响？ reverse-KL在学生采样分布下比较log学生与log教师，倾向把有限容量放在学生访问且教师支持的模式；forward-KL则更强调覆盖教师质量。方向改变期望分布与梯度，不能只交换公式参数。teacher-mixed采样等稳定化也需保留，候选分布验证不等于长文本蒸馏。 教学例子：教师能给出多种罕见表达，小学生容量有限；覆盖所有尾部与集中于若干可靠表达，会对散度方向提出不同取舍。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">LLM 后训练 / 在策略蒸馏：沿学生实际走过的前缀学习</a></p>
<span id="paper-post-training-minillm-8f5f3ddd" class="ar-learning-paper-anchor"></span>
<h2 id="qa-446e1e3109c8e57a">MiniLLM的reverse-KL为什么对小学生与教师尾部概率的关系有影响？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=post-training%3Aminillm">MiniLLM</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>reverse-KL在学生采样分布下比较log学生与log教师，倾向把有限容量放在学生访问且教师支持的模式；forward-KL则更强调覆盖教师质量。方向改变期望分布与梯度，不能只交换公式参数。teacher-mixed采样等稳定化也需保留，候选分布验证不等于长文本蒸馏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教师能给出多种罕见表达，小学生容量有限；覆盖所有尾部与集中于若干可靠表达，会对散度方向提出不同取舍。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2306.08543">原论文</a> · <a href="../../../../post-training/2306.08543-minillm/">实现解读</a> · <a href="#qa-446e1e3109c8e57a">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

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

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
