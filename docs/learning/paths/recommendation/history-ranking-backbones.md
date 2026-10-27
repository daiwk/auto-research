---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 用户历史与排序骨干

[搜广推](index.md) / 299 个问题 · 73 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

[阅读本主题精读卡片：多篇论文对比、分析与问答](../../deep-dives/recommendation/history-ranking-backbones.md)

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
<p class="ar-learning-status" data-learning-status role="status">299 个问题 · 73 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:echo-selector-loss" data-paper-title="ECHO: Efficient Cascade with Homogeneous Operators for Distillation-Guided 100K-Sequence Modeling" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="ECHO: Efficient Cascade with Homogeneous Operators for Distillation-Guided 100K-Sequence Modeling 搜广推与 LLM 应用 Kuaishou Technology 2026-10-20 将100K历史压成少量潜向量会丢失记录地址；逐候选扫描全部历史又过贵。ECHO让用户侧DS保留原始记录，再由目标侧TFR选更小子集。训练侧候选感知教师通过完整软分布和选择边界监督DS，教师相关性参数还导出到检索和聚合。线上不运行DS，也不扫描完整历史。 原文完整实验成本过高，不复现（审查 DONE）。仅L1诊断，不是完整ECHO/TWIN或推荐能力；已实现选择器蒸馏损失，在真实A100上验证公式、梯度和短时更新。仅L1诊断，不是完整ECHO/TWIN或推荐能力；原文完整实验成本过高，不复现（审查 DONE）。固定合成logit、seed42/43/44，在A100执行逐标量CE参考、实际学生参数更新、教师无梯度、padding零梯度及同排序无有效边界配对的负对照。未加载预训练checkpoint，无推荐准确率或正式比较资格。  长序列推荐 蒸馏选择与边界监督 搜广推 用户历史与排序骨干 ECHO 为什么要保留历史记录地址，而不是仅缓存几个兴趣潜向量？ 潜向量压缩方便，却难按候选取回具体事件。保留可寻址记录再做目标侧小子集检索，让细粒度证据与用户侧复用并存。地址保留并不表示线上逐候选扫描全历史，实际服务需遵循导出索引与参数路径，本地损失组件不能代替该系统。 示意：相机候选可取近期微距浏览记录，跑鞋候选读取运动证据；只有“爱户外”的静态潜向量时，难恢复具体是哪次行为支持推荐。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-echo-selector-loss-59466a02" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d7c77411b2cad8f3">ECHO 为什么要保留历史记录地址，而不是仅缓存几个兴趣潜向量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aecho-selector-loss">ECHO: Efficient Cascade with Homogeneous Operators for Distillation-Guided 100K-Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>潜向量压缩方便，却难按候选取回具体事件。保留可寻址记录再做目标侧小子集检索，让细粒度证据与用户侧复用并存。地址保留并不表示线上逐候选扫描全历史，实际服务需遵循导出索引与参数路径，本地损失组件不能代替该系统。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>相机候选可取近期微距浏览记录，跑鞋候选读取运动证据；只有“爱户外”的静态潜向量时，难恢复具体是哪次行为支持推荐。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28569v1">原论文</a> · <a href="../../../../recommendation-components/2610.28569-echo-selector-loss/">实现解读</a> · <a href="#qa-d7c77411b2cad8f3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:echo-selector-loss" data-paper-title="ECHO: Efficient Cascade with Homogeneous Operators for Distillation-Guided 100K-Sequence Modeling" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="ECHO: Efficient Cascade with Homogeneous Operators for Distillation-Guided 100K-Sequence Modeling 搜广推与 LLM 应用 Kuaishou Technology 2026-10-20 将100K历史压成少量潜向量会丢失记录地址；逐候选扫描全部历史又过贵。ECHO让用户侧DS保留原始记录，再由目标侧TFR选更小子集。训练侧候选感知教师通过完整软分布和选择边界监督DS，教师相关性参数还导出到检索和聚合。线上不运行DS，也不扫描完整历史。 原文完整实验成本过高，不复现（审查 DONE）。仅L1诊断，不是完整ECHO/TWIN或推荐能力；已实现选择器蒸馏损失，在真实A100上验证公式、梯度和短时更新。仅L1诊断，不是完整ECHO/TWIN或推荐能力；原文完整实验成本过高，不复现（审查 DONE）。固定合成logit、seed42/43/44，在A100执行逐标量CE参考、实际学生参数更新、教师无梯度、padding零梯度及同排序无有效边界配对的负对照。未加载预训练checkpoint，无推荐准确率或正式比较资格。  长序列推荐 蒸馏选择与边界监督 搜广推 用户历史与排序骨干 ECHO为什么既蒸馏完整教师分布，又特别惩罚选择边界上的漏选？ 完整软分布传递教师对各历史项的相对相关性，但学生仍可能在有限选择预算下漏掉关键记录。边界监督比较高质量漏选项与低质量已选项，直接推动二者交换次序；权重来自停止梯度的教师差异。该组件保留记录地址而非只压成潜向量，本地仅验证损失与梯度，并未验证100K推荐效果。 示意：学生只选两条历史，却漏掉教师最看重的一条、保留一条低相关记录；软标签教整体偏好，边界配对则明确要求把这两条的选择顺序调换。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-1e00f3b69701b501">ECHO为什么既蒸馏完整教师分布，又特别惩罚选择边界上的漏选？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aecho-selector-loss">ECHO: Efficient Cascade with Homogeneous Operators for Distillation-Guided 100K-Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>完整软分布传递教师对各历史项的相对相关性，但学生仍可能在有限选择预算下漏掉关键记录。边界监督比较高质量漏选项与低质量已选项，直接推动二者交换次序；权重来自停止梯度的教师差异。该组件保留记录地址而非只压成潜向量，本地仅验证损失与梯度，并未验证100K推荐效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>学生只选两条历史，却漏掉教师最看重的一条、保留一条低相关记录；软标签教整体偏好，边界配对则明确要求把这两条的选择顺序调换。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28569v1">原论文</a> · <a href="../../../../recommendation-components/2610.28569-echo-selector-loss/">实现解读</a> · <a href="#qa-1e00f3b69701b501">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:echo-selector-loss" data-paper-title="ECHO: Efficient Cascade with Homogeneous Operators for Distillation-Guided 100K-Sequence Modeling" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="ECHO: Efficient Cascade with Homogeneous Operators for Distillation-Guided 100K-Sequence Modeling 搜广推与 LLM 应用 Kuaishou Technology 2026-10-20 将100K历史压成少量潜向量会丢失记录地址；逐候选扫描全部历史又过贵。ECHO让用户侧DS保留原始记录，再由目标侧TFR选更小子集。训练侧候选感知教师通过完整软分布和选择边界监督DS，教师相关性参数还导出到检索和聚合。线上不运行DS，也不扫描完整历史。 原文完整实验成本过高，不复现（审查 DONE）。仅L1诊断，不是完整ECHO/TWIN或推荐能力；已实现选择器蒸馏损失，在真实A100上验证公式、梯度和短时更新。仅L1诊断，不是完整ECHO/TWIN或推荐能力；原文完整实验成本过高，不复现（审查 DONE）。固定合成logit、seed42/43/44，在A100执行逐标量CE参考、实际学生参数更新、教师无梯度、padding零梯度及同排序无有效边界配对的负对照。未加载预训练checkpoint，无推荐准确率或正式比较资格。  长序列推荐 蒸馏选择与边界监督 搜广推 用户历史与排序骨干 ECHO 边界配对与全分布 KD，为何对不同错误提供监督？ 全分布传递整体教师偏好，边界项直接比较漏选高质量与已选低质量记录，推动真正影响 Top-K 的交换。配对权重强调教师质量差，不能让离散选择本身可导；学生被配对 logits 接收梯度。两个信号互补而非简单重复摘要。 示意：第十与第十一条跨选择边界，整体分布差异很小却决定关键记录是否保留；边界损失可专门纠正这一对，而不是平均照顾所有尾部。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f213f30adacee7d0">ECHO 边界配对与全分布 KD，为何对不同错误提供监督？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aecho-selector-loss">ECHO: Efficient Cascade with Homogeneous Operators for Distillation-Guided 100K-Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全分布传递整体教师偏好，边界项直接比较漏选高质量与已选低质量记录，推动真正影响 Top-K 的交换。配对权重强调教师质量差，不能让离散选择本身可导；学生被配对 logits 接收梯度。两个信号互补而非简单重复摘要。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第十与第十一条跨选择边界，整体分布差异很小却决定关键记录是否保留；边界损失可专门纠正这一对，而不是平均照顾所有尾部。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28569v1">原论文</a> · <a href="../../../../recommendation-components/2610.28569-echo-selector-loss/">实现解读</a> · <a href="#qa-f213f30adacee7d0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:echo-selector-loss" data-paper-title="ECHO: Efficient Cascade with Homogeneous Operators for Distillation-Guided 100K-Sequence Modeling" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="ECHO: Efficient Cascade with Homogeneous Operators for Distillation-Guided 100K-Sequence Modeling 搜广推与 LLM 应用 Kuaishou Technology 2026-10-20 将100K历史压成少量潜向量会丢失记录地址；逐候选扫描全部历史又过贵。ECHO让用户侧DS保留原始记录，再由目标侧TFR选更小子集。训练侧候选感知教师通过完整软分布和选择边界监督DS，教师相关性参数还导出到检索和聚合。线上不运行DS，也不扫描完整历史。 原文完整实验成本过高，不复现（审查 DONE）。仅L1诊断，不是完整ECHO/TWIN或推荐能力；已实现选择器蒸馏损失，在真实A100上验证公式、梯度和短时更新。仅L1诊断，不是完整ECHO/TWIN或推荐能力；原文完整实验成本过高，不复现（审查 DONE）。固定合成logit、seed42/43/44，在A100执行逐标量CE参考、实际学生参数更新、教师无梯度、padding零梯度及同排序无有效边界配对的负对照。未加载预训练checkpoint，无推荐准确率或正式比较资格。  长序列推荐 蒸馏选择与边界监督 搜广推 用户历史与排序骨干 ECHO 为什么按全 batch 有效配对权重归一，并对教师及权重 detach？ 逐行平均会让配对少的请求被额外放大，全批归一保留定义贡献。教师与挖掘权重固定，损失只更新对应学生分数；padding 不参与概率、选择或梯度。联合细节是损失保真的核心，不能仅输出一个有限标量就称通过机制验证。 示意：一行十对、另一行一对，逐行平均让后者单对权重大十倍；统一分母避免该偏置，教师冻结也防止双方一起移动掩盖错误。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-bb9a81762fca55db">ECHO 为什么按全 batch 有效配对权重归一，并对教师及权重 detach？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aecho-selector-loss">ECHO: Efficient Cascade with Homogeneous Operators for Distillation-Guided 100K-Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>逐行平均会让配对少的请求被额外放大，全批归一保留定义贡献。教师与挖掘权重固定，损失只更新对应学生分数；padding 不参与概率、选择或梯度。联合细节是损失保真的核心，不能仅输出一个有限标量就称通过机制验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一行十对、另一行一对，逐行平均让后者单对权重大十倍；统一分母避免该偏置，教师冻结也防止双方一起移动掩盖错误。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28569v1">原论文</a> · <a href="../../../../recommendation-components/2610.28569-echo-selector-loss/">实现解读</a> · <a href="#qa-bb9a81762fca55db">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:repair-state" data-paper-title="Not All Is Lost: Repairing Lossy User Preference States of Personalization Encoders" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Not All Is Lost: Repairing Lossy User Preference States of Personalization Encoders 搜广推与 LLM 应用 原文首页未列第一作者机构 2026-10-01 冻结 encoder 与原 task head，从已有 forward cache 中比较各 timestep 表征和当前 preference state，选择长程、近期或局部 burst 的纠正证据并做 residual repair。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 frozen-cache evidence selection 与 residual correction；用户批准为学术/Evolve 例外，无线上 A/B。收录例外：用户于 2026-10-02 明确批准的学术/Evolve 机制例外；论文没有量化线上 A/B，不进入工业证据结论。执行 frozen-cache evidence selection 与 residual correction；用户批准为学术/Evolve 例外，无线上 A/B。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。  personalization state-repair sequential-recommendation 搜广推 用户历史与排序骨干 Repair-State 中 ht 与当前偏好 z 都是向量，为什么不能随便互换？ ht 是某个时间位置的上下文化状态，z 是当前供任务头使用的偏好汇总，两者维度相同但覆盖与时点不同。单个旧状态可能只反映当时局部需求，不能直接代表现在全部兴趣。修补需要选择相关证据并保留当前状态，而非见到同形张量就直接覆盖。 示意：去年的相机比较状态包含当时需求，当前用户已准备露营；直接用旧 ht 替换 z 会丢掉近期信息，同为 d 维并不让它们语义相同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-repair-state-eec04848" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-834d6a05b8e38552">Repair-State 中 ht 与当前偏好 z 都是向量，为什么不能随便互换？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arepair-state">Not All Is Lost: Repairing Lossy User Preference States of Personalization Encoders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>ht 是某个时间位置的上下文化状态，z 是当前供任务头使用的偏好汇总，两者维度相同但覆盖与时点不同。单个旧状态可能只反映当时局部需求，不能直接代表现在全部兴趣。修补需要选择相关证据并保留当前状态，而非见到同形张量就直接覆盖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>去年的相机比较状态包含当时需求，当前用户已准备露营；直接用旧 ht 替换 z 会丢掉近期信息，同为 d 维并不让它们语义相同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01270">原论文</a> · <a href="../../../../reproductions/2610.01270-repair-state/">实现解读</a> · <a href="#qa-834d6a05b8e38552">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:repair-state" data-paper-title="Not All Is Lost: Repairing Lossy User Preference States of Personalization Encoders" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Not All Is Lost: Repairing Lossy User Preference States of Personalization Encoders 搜广推与 LLM 应用 原文首页未列第一作者机构 2026-10-01 冻结 encoder 与原 task head，从已有 forward cache 中比较各 timestep 表征和当前 preference state，选择长程、近期或局部 burst 的纠正证据并做 residual repair。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 frozen-cache evidence selection 与 residual correction；用户批准为学术/Evolve 例外，无线上 A/B。收录例外：用户于 2026-10-02 明确批准的学术/Evolve 机制例外；论文没有量化线上 A/B，不进入工业证据结论。执行 frozen-cache evidence selection 与 residual correction；用户批准为学术/Evolve 例外，无线上 A/B。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。  personalization state-repair sequential-recommendation 搜广推 用户历史与排序骨干 Repair-State 为什么在冻结编码器和任务头的情况下，用历史状态差分修补当前 preference state？ 冻结模型避免重新训练整条链路，已有前向缓存则提供不同时间位置的证据。方法比较历史状态与当前偏好，选择长程、近期或突发片段，用加权残差把被压缩丢失的相关方向补回来。它纠正的是当前表示，不会创造缓存中不存在的信息；选择错误证据也可能把过时兴趣重新注入。 示意：当前汇总偏好被长期电影兴趣主导，但最近连续看育儿内容。无需重训编码器，可从缓存挑出这段突发证据，以差分残差补入当前状态，再交给原任务头。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-d799684e7cf1cfcc">Repair-State 为什么在冻结编码器和任务头的情况下，用历史状态差分修补当前 preference state？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arepair-state">Not All Is Lost: Repairing Lossy User Preference States of Personalization Encoders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冻结模型避免重新训练整条链路，已有前向缓存则提供不同时间位置的证据。方法比较历史状态与当前偏好，选择长程、近期或突发片段，用加权残差把被压缩丢失的相关方向补回来。它纠正的是当前表示，不会创造缓存中不存在的信息；选择错误证据也可能把过时兴趣重新注入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>当前汇总偏好被长期电影兴趣主导，但最近连续看育儿内容。无需重训编码器，可从缓存挑出这段突发证据，以差分残差补入当前状态，再交给原任务头。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01270">原论文</a> · <a href="../../../../reproductions/2610.01270-repair-state/">实现解读</a> · <a href="#qa-d799684e7cf1cfcc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:repair-state" data-paper-title="Not All Is Lost: Repairing Lossy User Preference States of Personalization Encoders" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Not All Is Lost: Repairing Lossy User Preference States of Personalization Encoders 搜广推与 LLM 应用 原文首页未列第一作者机构 2026-10-01 冻结 encoder 与原 task head，从已有 forward cache 中比较各 timestep 表征和当前 preference state，选择长程、近期或局部 burst 的纠正证据并做 residual repair。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 frozen-cache evidence selection 与 residual correction；用户批准为学术/Evolve 例外，无线上 A/B。收录例外：用户于 2026-10-02 明确批准的学术/Evolve 机制例外；论文没有量化线上 A/B，不进入工业证据结论。执行 frozen-cache evidence selection 与 residual correction；用户批准为学术/Evolve 例外，无线上 A/B。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。  personalization state-repair sequential-recommendation 搜广推 用户历史与排序骨干 Repair-State 与重训整个 encoder，相比改动范围和限制在哪里？ 状态修复只对已有 forward cache 做后置调整，保持 encoder 和原头不变，部署更轻；重训能改变特征提取但更贵。缓存没记录的信息无法靠残差创造，选证据策略也未必适配所有任务。来源仅诊断，不支持正式模型能力排名。 示意：缓存保留了一段突发兴趣可修补，被编码器彻底忽略的稀有事件则无从恢复；重训也许可学回来，但属于另一成本路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7595444adbde5955">Repair-State 与重训整个 encoder，相比改动范围和限制在哪里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arepair-state">Not All Is Lost: Repairing Lossy User Preference States of Personalization Encoders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>状态修复只对已有 forward cache 做后置调整，保持 encoder 和原头不变，部署更轻；重训能改变特征提取但更贵。缓存没记录的信息无法靠残差创造，选证据策略也未必适配所有任务。来源仅诊断，不支持正式模型能力排名。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>缓存保留了一段突发兴趣可修补，被编码器彻底忽略的稀有事件则无从恢复；重训也许可学回来，但属于另一成本路径。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01270">原论文</a> · <a href="../../../../reproductions/2610.01270-repair-state/">实现解读</a> · <a href="#qa-7595444adbde5955">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:repair-state" data-paper-title="Not All Is Lost: Repairing Lossy User Preference States of Personalization Encoders" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Not All Is Lost: Repairing Lossy User Preference States of Personalization Encoders 搜广推与 LLM 应用 原文首页未列第一作者机构 2026-10-01 冻结 encoder 与原 task head，从已有 forward cache 中比较各 timestep 表征和当前 preference state，选择长程、近期或局部 burst 的纠正证据并做 residual repair。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 frozen-cache evidence selection 与 residual correction；用户批准为学术/Evolve 例外，无线上 A/B。收录例外：用户于 2026-10-02 明确批准的学术/Evolve 机制例外；论文没有量化线上 A/B，不进入工业证据结论。执行 frozen-cache evidence selection 与 residual correction；用户批准为学术/Evolve 例外，无线上 A/B。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。  personalization state-repair sequential-recommendation 搜广推 用户历史与排序骨干 Repair-State 的 Top-K 与 softmax mask，为什么要在修复前检查有效历史？ padding、未来状态和不同用户缓存都不合法，选集必须先屏蔽；权重只在选中有效位置归一，差分与 z 维度一致。空历史需返回定义的原状态或失败，不应用随机填充值制造纠正证据。固定 encoder 也不能防数据本身泄漏。 示意：真实两条历史却选 K=5，若空位零分胜过负分事件，会把 padding 当强证据拉 z 向零；这不是有意义修复。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-21fc126e36070136">Repair-State 的 Top-K 与 softmax mask，为什么要在修复前检查有效历史？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arepair-state">Not All Is Lost: Repairing Lossy User Preference States of Personalization Encoders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>padding、未来状态和不同用户缓存都不合法，选集必须先屏蔽；权重只在选中有效位置归一，差分与 z 维度一致。空历史需返回定义的原状态或失败，不应用随机填充值制造纠正证据。固定 encoder 也不能防数据本身泄漏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>真实两条历史却选 K=5，若空位零分胜过负分事件，会把 padding 当强证据拉 z 向零；这不是有意义修复。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01270">原论文</a> · <a href="../../../../reproductions/2610.01270-repair-state/">实现解读</a> · <a href="#qa-21fc126e36070136">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:helix" data-paper-title="HELIX: Purified and Unified - Rethinking Feature Interaction and Sequence Modeling for Large-Scale Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="HELIX: Purified and Unified - Rethinking Feature Interaction and Sequence Modeling for Large-Scale Recommendation 搜广推与 LLM 应用 TikTok / ByteDance 2026-09-29 工业排序通常分别扩大异构特征交互与长行为序列，两条轴单独扩展都会遇到上限。HELIX 交错 SeqFormer 与 MixFormer，但强制信息只从可复用的 user-only sequence state 流向 candidate-conditioned mix tokens，使用户侧序列计算能跨候选复用，同时保持两轴的跨深度通信。 复现级别：L1 架构机制。复现级别：L1 架构机制。实现三流 token、单向 U-only 缓存、跨深度 MixFormer/SeqFormer 交互与多任务头；没有 TikTok 私有数据和线上流量。本地使用合成张量，不含私有训练数据、线上 A/B 或论文规模系统优化，因此 reproduction_level=concept_demo。只有接入公开公平数据、基线和多种子 validation/test 隔离后，才能讨论效果复现或进入 Evolve 搜索空间。本地对照口径：基线为同一 user cache 下的候选 A，实验组为候选 B；只检查候选敏感性与 cache 不变量，没有公开效果指标，相对变化不适用。  ranking feature-interaction sequence-modeling 搜广推 用户历史与排序骨干 HELIX 为什么同时扩展 sequence 与异构特征交互两条轴？ 长历史和字段组合各含不同信息，单独扩大任一分支会遇到表示瓶颈。交错模块让候选混合状态在多层读取用户序列，结合两轴知识，同时保留用户状态候选无关。它不是两套模型末端简单拼接，交互方向也受缓存要求约束。 示意：用户历史揭示旅行兴趣，价格与设备字段逐层结合这些证据；只扩字段无法读取更多历史，只扩序列也未必学会异构条件组合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-helix-94ed43e6" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-21fa62a2c298c656">HELIX 为什么同时扩展 sequence 与异构特征交互两条轴？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahelix">HELIX: Purified and Unified - Rethinking Feature Interaction and Sequence Modeling for Large-Scale Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · TikTok / ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长历史和字段组合各含不同信息，单独扩大任一分支会遇到表示瓶颈。交错模块让候选混合状态在多层读取用户序列，结合两轴知识，同时保留用户状态候选无关。它不是两套模型末端简单拼接，交互方向也受缓存要求约束。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户历史揭示旅行兴趣，价格与设备字段逐层结合这些证据；只扩字段无法读取更多历史，只扩序列也未必学会异构条件组合。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37183">原论文</a> · <a href="../../../../reproductions/2609.37183-helix/">实现解读</a> · <a href="#qa-21fa62a2c298c656">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:helix" data-paper-title="HELIX: Purified and Unified - Rethinking Feature Interaction and Sequence Modeling for Large-Scale Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="HELIX: Purified and Unified - Rethinking Feature Interaction and Sequence Modeling for Large-Scale Recommendation 搜广推与 LLM 应用 TikTok / ByteDance 2026-09-29 工业排序通常分别扩大异构特征交互与长行为序列，两条轴单独扩展都会遇到上限。HELIX 交错 SeqFormer 与 MixFormer，但强制信息只从可复用的 user-only sequence state 流向 candidate-conditioned mix tokens，使用户侧序列计算能跨候选复用，同时保持两轴的跨深度通信。 复现级别：L1 架构机制。复现级别：L1 架构机制。实现三流 token、单向 U-only 缓存、跨深度 MixFormer/SeqFormer 交互与多任务头；没有 TikTok 私有数据和线上流量。本地使用合成张量，不含私有训练数据、线上 A/B 或论文规模系统优化，因此 reproduction_level=concept_demo。只有接入公开公平数据、基线和多种子 validation/test 隔离后，才能讨论效果复现或进入 Evolve 搜索空间。本地对照口径：基线为同一 user cache 下的候选 A，实验组为候选 B；只检查候选敏感性与 cache 不变量，没有公开效果指标，相对变化不适用。  ranking feature-interaction sequence-modeling 搜广推 用户历史与排序骨干 HELIX让序列状态流向候选混合token，为什么禁止候选反向写回共享序列？ 单向依赖使昂贵的用户历史编码保持候选无关，从而一次请求内可复用于多候选；候选侧仍能在多层读取用户信息，保留深交互。若允许反向写回，序列状态就随候选变化，复用前提被破坏。本地只验证候选敏感性和缓存不变量，不代表已获得生产吞吐或推荐提升。 示意：评相机和鞋时共用同一份历史状态，各候选分别读取；若相机信息先改写了历史，再把该缓存用于鞋，就混入了另一候选，已不再是共享用户证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-fdc7e424eea56b8a">HELIX让序列状态流向候选混合token，为什么禁止候选反向写回共享序列？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahelix">HELIX: Purified and Unified - Rethinking Feature Interaction and Sequence Modeling for Large-Scale Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · TikTok / ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单向依赖使昂贵的用户历史编码保持候选无关，从而一次请求内可复用于多候选；候选侧仍能在多层读取用户信息，保留深交互。若允许反向写回，序列状态就随候选变化，复用前提被破坏。本地只验证候选敏感性和缓存不变量，不代表已获得生产吞吐或推荐提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>评相机和鞋时共用同一份历史状态，各候选分别读取；若相机信息先改写了历史，再把该缓存用于鞋，就混入了另一候选，已不再是共享用户证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37183">原论文</a> · <a href="../../../../reproductions/2609.37183-helix/">实现解读</a> · <a href="#qa-fdc7e424eea56b8a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:helix" data-paper-title="HELIX: Purified and Unified - Rethinking Feature Interaction and Sequence Modeling for Large-Scale Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="HELIX: Purified and Unified - Rethinking Feature Interaction and Sequence Modeling for Large-Scale Recommendation 搜广推与 LLM 应用 TikTok / ByteDance 2026-09-29 工业排序通常分别扩大异构特征交互与长行为序列，两条轴单独扩展都会遇到上限。HELIX 交错 SeqFormer 与 MixFormer，但强制信息只从可复用的 user-only sequence state 流向 candidate-conditioned mix tokens，使用户侧序列计算能跨候选复用，同时保持两轴的跨深度通信。 复现级别：L1 架构机制。复现级别：L1 架构机制。实现三流 token、单向 U-only 缓存、跨深度 MixFormer/SeqFormer 交互与多任务头；没有 TikTok 私有数据和线上流量。本地使用合成张量，不含私有训练数据、线上 A/B 或论文规模系统优化，因此 reproduction_level=concept_demo。只有接入公开公平数据、基线和多种子 validation/test 隔离后，才能讨论效果复现或进入 Evolve 搜索空间。本地对照口径：基线为同一 user cache 下的候选 A，实验组为候选 B；只检查候选敏感性与 cache 不变量，没有公开效果指标，相对变化不适用。  ranking feature-interaction sequence-modeling 搜广推 用户历史与排序骨干 HELIX 的单向跨分支通信与 WHALE 式双向交换，缓存条件有何差别？ HELIX 禁止候选条件 mix 写回公共序列，保持 user-only 状态可复用；双向交换可更充分共同演化，却会改变候选依赖。两者是信息与服务取舍，不能只按都有 cross-attention 就说等价，也没有来源支持任意场景效果排序。 示意：相机候选读历史后不改公共用户记忆，跑鞋可读同份缓存；若相机状态写回历史，跑鞋再复用就带入不该共享的候选信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-63277b17cffa622f">HELIX 的单向跨分支通信与 WHALE 式双向交换，缓存条件有何差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahelix">HELIX: Purified and Unified - Rethinking Feature Interaction and Sequence Modeling for Large-Scale Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · TikTok / ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>HELIX 禁止候选条件 mix 写回公共序列，保持 user-only 状态可复用；双向交换可更充分共同演化，却会改变候选依赖。两者是信息与服务取舍，不能只按都有 cross-attention 就说等价，也没有来源支持任意场景效果排序。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>相机候选读历史后不改公共用户记忆，跑鞋可读同份缓存；若相机状态写回历史，跑鞋再复用就带入不该共享的候选信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37183">原论文</a> · <a href="../../../../reproductions/2609.37183-helix/">实现解读</a> · <a href="#qa-63277b17cffa622f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:helix" data-paper-title="HELIX: Purified and Unified - Rethinking Feature Interaction and Sequence Modeling for Large-Scale Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="HELIX: Purified and Unified - Rethinking Feature Interaction and Sequence Modeling for Large-Scale Recommendation 搜广推与 LLM 应用 TikTok / ByteDance 2026-09-29 工业排序通常分别扩大异构特征交互与长行为序列，两条轴单独扩展都会遇到上限。HELIX 交错 SeqFormer 与 MixFormer，但强制信息只从可复用的 user-only sequence state 流向 candidate-conditioned mix tokens，使用户侧序列计算能跨候选复用，同时保持两轴的跨深度通信。 复现级别：L1 架构机制。复现级别：L1 架构机制。实现三流 token、单向 U-only 缓存、跨深度 MixFormer/SeqFormer 交互与多任务头；没有 TikTok 私有数据和线上流量。本地使用合成张量，不含私有训练数据、线上 A/B 或论文规模系统优化，因此 reproduction_level=concept_demo。只有接入公开公平数据、基线和多种子 validation/test 隔离后，才能讨论效果复现或进入 Evolve 搜索空间。本地对照口径：基线为同一 user cache 下的候选 A，实验组为候选 B；只检查候选敏感性与 cache 不变量，没有公开效果指标，相对变化不适用。  ranking feature-interaction sequence-modeling 搜广推 用户历史与排序骨干 HELIX 本地为何同时检查候选 delta、user cache 不变与有限梯度？ 候选变化应能影响输出，公共用户状态应不受候选变化影响，两项缺一可能分别表示候选被忽略或缓存污染。有限 loss 与梯度再检查训练可执行性。这些是不变量诊断，没有公开效果指标，不能把通过率当推荐质量提升。 示意：换两件商品分数完全相同可能没用候选；分数不同但 cache 也变则失去共享条件，两者都不能只凭前向成功算验收。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d081140a6218cc83">HELIX 本地为何同时检查候选 delta、user cache 不变与有限梯度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahelix">HELIX: Purified and Unified - Rethinking Feature Interaction and Sequence Modeling for Large-Scale Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · TikTok / ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>候选变化应能影响输出，公共用户状态应不受候选变化影响，两项缺一可能分别表示候选被忽略或缓存污染。有限 loss 与梯度再检查训练可执行性。这些是不变量诊断，没有公开效果指标，不能把通过率当推荐质量提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>换两件商品分数完全相同可能没用候选；分数不同但 cache 也变则失去共享条件，两者都不能只凭前向成功算验收。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37183">原论文</a> · <a href="../../../../reproductions/2609.37183-helix/">实现解读</a> · <a href="#qa-d081140a6218cc83">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recap-ctr" data-paper-title="Beyond Interaction Capacity: Estimator Scaling with Recursive Models for CTR Prediction" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Beyond Interaction Capacity: Estimator Scaling with Recursive Models for CTR Prediction 搜广推与 LLM 应用 Georgia Institute of Technology / Google Research 2026-09-29 不再只增加单个 CTR predictor 的交互容量，而是扩展相关 estimator；RECAP 在共享参数的递归 backbone 上形成多条 route，并结合独立模型蒸馏、训练轨迹 EMA 与推理 route 平均。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行共享递归、route 平均、trajectory EMA 和可运行 RankMixer Evolve block；未做 benchmark 训练或独立模型蒸馏。执行共享递归、route 平均、trajectory EMA 和可运行 RankMixer Evolve block；未做 benchmark 训练或独立模型蒸馏。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  ctr estimator-scaling recursive-network 搜广推 用户历史与排序骨干 RECAP-CTR 平均 route 的 logit，与平均各 route 的点击概率是同一件事吗？ 不是。sigmoid 是非线性，先平均 logit 再变成概率，通常不同于先逐路变概率再平均。来源用 route logit 的均值，不能无说明替换运算顺序；这只是聚合定义，也不代表多个共享 route 是相互独立的完整模型。 示意：两路 logit 为零和四，先平均再 sigmoid 约零点八八；各自 sigmoid 后平均约零点七四，顺序变化会实质改变预测。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-recap-ctr-8a9efe0a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5aaae777d05508db">RECAP-CTR 平均 route 的 logit，与平均各 route 的点击概率是同一件事吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecap-ctr">Beyond Interaction Capacity: Estimator Scaling with Recursive Models for CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Georgia Institute of Technology / Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。sigmoid 是非线性，先平均 logit 再变成概率，通常不同于先逐路变概率再平均。来源用 route logit 的均值，不能无说明替换运算顺序；这只是聚合定义，也不代表多个共享 route 是相互独立的完整模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两路 logit 为零和四，先平均再 sigmoid 约零点八八；各自 sigmoid 后平均约零点七四，顺序变化会实质改变预测。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37905">原论文</a> · <a href="../../../../reproductions/2609.37905-recap-ctr/">实现解读</a> · <a href="#qa-5aaae777d05508db">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recap-ctr" data-paper-title="Beyond Interaction Capacity: Estimator Scaling with Recursive Models for CTR Prediction" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Beyond Interaction Capacity: Estimator Scaling with Recursive Models for CTR Prediction 搜广推与 LLM 应用 Georgia Institute of Technology / Google Research 2026-09-29 不再只增加单个 CTR predictor 的交互容量，而是扩展相关 estimator；RECAP 在共享参数的递归 backbone 上形成多条 route，并结合独立模型蒸馏、训练轨迹 EMA 与推理 route 平均。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行共享递归、route 平均、trajectory EMA 和可运行 RankMixer Evolve block；未做 benchmark 训练或独立模型蒸馏。执行共享递归、route 平均、trajectory EMA 和可运行 RankMixer Evolve block；未做 benchmark 训练或独立模型蒸馏。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  ctr estimator-scaling recursive-network 搜广推 用户历史与排序骨干 RECAP-CTR 为什么共享递归 block 却平均多个 route 的预测，还保留训练轨迹 EMA？ 单个大预测器可能仍缺少互补估计。共享递归结构用不同路径产生多个 logit，在控制参数开销的同时增加估计差异，推理平均降低单一路径波动；轨迹 EMA 则沿训练时间平滑参数。路径平均和时间平均作用于不同变化来源，但相关路径的收益有限，本地仅验证状态与算子不变量，不能冒充规模效果。 示意：同一共享 block 经两条递归路径得到略不同点击预测，平均可减小某一路径偶然偏高。EMA 另行平滑相邻训练步的模型，它不是又增加一个完全独立的模型。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-6d48a3ea0b094184">RECAP-CTR 为什么共享递归 block 却平均多个 route 的预测，还保留训练轨迹 EMA？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecap-ctr">Beyond Interaction Capacity: Estimator Scaling with Recursive Models for CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Georgia Institute of Technology / Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单个大预测器可能仍缺少互补估计。共享递归结构用不同路径产生多个 logit，在控制参数开销的同时增加估计差异，推理平均降低单一路径波动；轨迹 EMA 则沿训练时间平滑参数。路径平均和时间平均作用于不同变化来源，但相关路径的收益有限，本地仅验证状态与算子不变量，不能冒充规模效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一共享 block 经两条递归路径得到略不同点击预测，平均可减小某一路径偶然偏高。EMA 另行平滑相邻训练步的模型，它不是又增加一个完全独立的模型。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37905">原论文</a> · <a href="../../../../reproductions/2609.37905-recap-ctr/">实现解读</a> · <a href="#qa-6d48a3ea0b094184">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recap-ctr" data-paper-title="Beyond Interaction Capacity: Estimator Scaling with Recursive Models for CTR Prediction" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Beyond Interaction Capacity: Estimator Scaling with Recursive Models for CTR Prediction 搜广推与 LLM 应用 Georgia Institute of Technology / Google Research 2026-09-29 不再只增加单个 CTR predictor 的交互容量，而是扩展相关 estimator；RECAP 在共享参数的递归 backbone 上形成多条 route，并结合独立模型蒸馏、训练轨迹 EMA 与推理 route 平均。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行共享递归、route 平均、trajectory EMA 和可运行 RankMixer Evolve block；未做 benchmark 训练或独立模型蒸馏。执行共享递归、route 平均、trajectory EMA 和可运行 RankMixer Evolve block；未做 benchmark 训练或独立模型蒸馏。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  ctr estimator-scaling recursive-network 搜广推 用户历史与排序骨干 route 平均与训练轨迹 EMA，为什么不能互相代替？ 前者在同一时刻组合不同路径输出，后者沿训练时间平滑参数，减少的变化来源不同。路径共用参数时收益受相关性限制，EMA 也可能滞后新分布。来源本地仅不变量诊断，不可据平滑更稳定就宣称 CTR 或推荐能力提升。 示意：三路都同时偏高，输出平均仍偏高；时间 EMA 可抑某步异常，却不能弥补所有路线缺少同一类特征，两种平均都各有限制。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e72f1a396b8fee34">route 平均与训练轨迹 EMA，为什么不能互相代替？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecap-ctr">Beyond Interaction Capacity: Estimator Scaling with Recursive Models for CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Georgia Institute of Technology / Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者在同一时刻组合不同路径输出，后者沿训练时间平滑参数，减少的变化来源不同。路径共用参数时收益受相关性限制，EMA 也可能滞后新分布。来源本地仅不变量诊断，不可据平滑更稳定就宣称 CTR 或推荐能力提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三路都同时偏高，输出平均仍偏高；时间 EMA 可抑某步异常，却不能弥补所有路线缺少同一类特征，两种平均都各有限制。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37905">原论文</a> · <a href="../../../../reproductions/2609.37905-recap-ctr/">实现解读</a> · <a href="#qa-e72f1a396b8fee34">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:recap-ctr" data-paper-title="Beyond Interaction Capacity: Estimator Scaling with Recursive Models for CTR Prediction" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Beyond Interaction Capacity: Estimator Scaling with Recursive Models for CTR Prediction 搜广推与 LLM 应用 Georgia Institute of Technology / Google Research 2026-09-29 不再只增加单个 CTR predictor 的交互容量，而是扩展相关 estimator；RECAP 在共享参数的递归 backbone 上形成多条 route，并结合独立模型蒸馏、训练轨迹 EMA 与推理 route 平均。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行共享递归、route 平均、trajectory EMA 和可运行 RankMixer Evolve block；未做 benchmark 训练或独立模型蒸馏。执行共享递归、route 平均、trajectory EMA 和可运行 RankMixer Evolve block；未做 benchmark 训练或独立模型蒸馏。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  ctr estimator-scaling recursive-network 搜广推 用户历史与排序骨干 RECAP-CTR 的 EMA 状态为什么需要在训练与恢复时单独保存？ EMA 是跨步累积参数，恢复若丢掉会改变模型历史，不等于继续同一估计器。route 输出数量与平均分母也须一致，不能把缺失路径当零贡献。应分别核验递归共享、EMA 更新和导出模型，而非只用最终有限分数算全部机制通过。 示意：中断后直接将 EMA 重置成当前参数，会丢前几千步平滑；即使训练能继续，恢复后的曲线不再是原运行的无缝延续。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ec50d7a4585aae79">RECAP-CTR 的 EMA 状态为什么需要在训练与恢复时单独保存？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arecap-ctr">Beyond Interaction Capacity: Estimator Scaling with Recursive Models for CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Georgia Institute of Technology / Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>EMA 是跨步累积参数，恢复若丢掉会改变模型历史，不等于继续同一估计器。route 输出数量与平均分母也须一致，不能把缺失路径当零贡献。应分别核验递归共享、EMA 更新和导出模型，而非只用最终有限分数算全部机制通过。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>中断后直接将 EMA 重置成当前参数，会丢前几千步平滑；即使训练能继续，恢复后的曲线不再是原运行的无缝延续。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37905">原论文</a> · <a href="../../../../reproductions/2609.37905-recap-ctr/">实现解读</a> · <a href="#qa-ec50d7a4585aae79">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onetrans-v2" data-paper-title="OneTrans-V2: Unifying Retrieval, Pre-rank, and Fine-rank with One Transformer in Industrial Recommender" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OneTrans-V2: Unifying Retrieval, Pre-rank, and Fine-rank with One Transformer in Industrial Recommender 搜广推与 LLM 应用 ByteDance 2026-09-23 工业推荐先检索海量候选，再预排缩小集合，最后精排。三套独立模型会反复编码同一用户历史，也难以让精排经验稳定反馈给上游。OneTrans-V2 保留三个阶段各自的输入与目标，却让它们共享一个因果 Transformer 用户上下文。行为序列不读阶段 token；每个阶段 token 只读请求时刻前的行为，不在阶段之间交叉读取。这既复用昂贵的用户编码，也防止未来信息泄漏。 故 adapter 标记为 concept_demo，不声称复刻 GMV、QPS 或完整 DCGR 业务控制。Fidelity：概念验证（非论文完整复现）；证据等级：L1 机制验证，使用完整 MovieLens-1M。三阶段核心计算与损失已执行，但公开 MovieLens 没有交易、广告供给和真实曝光漏斗，不能把代理指标解释为论文的业务提升。已执行共享因果用户编码、阶段隔离、三级 SID 自回归、可观测代理决策、双阶段多目标 BCE 与精排向预排蒸馏。未执行真实购买/金额/广告决策、工业物品编码、稀疏 MoE、Sequence-Native Training 的跨曝光摊销、线上服务与 A/B。  multi-stage-ranking generative-retrieval cross-stage-distillation 搜广推 用户历史与排序骨干 OneTrans-V2 为什么共享用户上下文但仍保留三个阶段的输入和目标？ 检索、预排和精排候选规模与可用特征不同，完全合并目标会失去阶段约束。公共因果历史避免重复编码，各阶段 token 按自身信息输出，再以受控损失传经验。统一主干不等于一个任务可以读取别阶段的未来标签。 示意：检索可只知语义码，精排额外知商品细字段；共享历史并不允许检索在请求时偷看精排才有的后验结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-onetrans-v2-65020d24" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-298dd87277815a64">OneTrans-V2 为什么共享用户上下文但仍保留三个阶段的输入和目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonetrans-v2">OneTrans-V2: Unifying Retrieval, Pre-rank, and Fine-rank with One Transformer in Industrial Recommender</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>检索、预排和精排候选规模与可用特征不同，完全合并目标会失去阶段约束。公共因果历史避免重复编码，各阶段 token 按自身信息输出，再以受控损失传经验。统一主干不等于一个任务可以读取别阶段的未来标签。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>检索可只知语义码，精排额外知商品细字段；共享历史并不允许检索在请求时偷看精排才有的后验结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.28589">原论文</a> · <a href="../../../../reproductions/2609.28589-onetrans-v2/">实现解读</a> · <a href="#qa-298dd87277815a64">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onetrans-v2" data-paper-title="OneTrans-V2: Unifying Retrieval, Pre-rank, and Fine-rank with One Transformer in Industrial Recommender" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OneTrans-V2: Unifying Retrieval, Pre-rank, and Fine-rank with One Transformer in Industrial Recommender 搜广推与 LLM 应用 ByteDance 2026-09-23 工业推荐先检索海量候选，再预排缩小集合，最后精排。三套独立模型会反复编码同一用户历史，也难以让精排经验稳定反馈给上游。OneTrans-V2 保留三个阶段各自的输入与目标，却让它们共享一个因果 Transformer 用户上下文。行为序列不读阶段 token；每个阶段 token 只读请求时刻前的行为，不在阶段之间交叉读取。这既复用昂贵的用户编码，也防止未来信息泄漏。 故 adapter 标记为 concept_demo，不声称复刻 GMV、QPS 或完整 DCGR 业务控制。Fidelity：概念验证（非论文完整复现）；证据等级：L1 机制验证，使用完整 MovieLens-1M。三阶段核心计算与损失已执行，但公开 MovieLens 没有交易、广告供给和真实曝光漏斗，不能把代理指标解释为论文的业务提升。已执行共享因果用户编码、阶段隔离、三级 SID 自回归、可观测代理决策、双阶段多目标 BCE 与精排向预排蒸馏。未执行真实购买/金额/广告决策、工业物品编码、稀疏 MoE、Sequence-Native Training 的跨曝光摊销、线上服务与 A/B。  multi-stage-ranking generative-retrieval cross-stage-distillation 搜广推 用户历史与排序骨干 OneTrans-V2 三个阶段共享用户上下文，为什么又禁止阶段 token 彼此交叉读取？ 用户行为编码是三个阶段反复使用的昂贵公共部分，共享它可以减少重复计算。各阶段保留自己的输入和目标，并只读取请求时刻之前的行为，防止下游信息或未来行为通过注意力路径泄漏到上游。精排知识通过受控蒸馏损失反馈给预排，而非开放任意读取；本地没有独立三级基线，不能声称级联效果改善。 示意：召回、预排、精排都读同一份已发生的浏览历史，但召回 token 不直接看精排标签或未来点击。预排学习精排判断时走停止梯度的教师信号，而不是偷看答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-e6a597373c4b5370">OneTrans-V2 三个阶段共享用户上下文，为什么又禁止阶段 token 彼此交叉读取？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonetrans-v2">OneTrans-V2: Unifying Retrieval, Pre-rank, and Fine-rank with One Transformer in Industrial Recommender</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用户行为编码是三个阶段反复使用的昂贵公共部分，共享它可以减少重复计算。各阶段保留自己的输入和目标，并只读取请求时刻之前的行为，防止下游信息或未来行为通过注意力路径泄漏到上游。精排知识通过受控蒸馏损失反馈给预排，而非开放任意读取；本地没有独立三级基线，不能声称级联效果改善。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>召回、预排、精排都读同一份已发生的浏览历史，但召回 token 不直接看精排标签或未来点击。预排学习精排判断时走停止梯度的教师信号，而不是偷看答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.28589">原论文</a> · <a href="../../../../reproductions/2609.28589-onetrans-v2/">实现解读</a> · <a href="#qa-e6a597373c4b5370">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onetrans-v2" data-paper-title="OneTrans-V2: Unifying Retrieval, Pre-rank, and Fine-rank with One Transformer in Industrial Recommender" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OneTrans-V2: Unifying Retrieval, Pre-rank, and Fine-rank with One Transformer in Industrial Recommender 搜广推与 LLM 应用 ByteDance 2026-09-23 工业推荐先检索海量候选，再预排缩小集合，最后精排。三套独立模型会反复编码同一用户历史，也难以让精排经验稳定反馈给上游。OneTrans-V2 保留三个阶段各自的输入与目标，却让它们共享一个因果 Transformer 用户上下文。行为序列不读阶段 token；每个阶段 token 只读请求时刻前的行为，不在阶段之间交叉读取。这既复用昂贵的用户编码，也防止未来信息泄漏。 故 adapter 标记为 concept_demo，不声称复刻 GMV、QPS 或完整 DCGR 业务控制。Fidelity：概念验证（非论文完整复现）；证据等级：L1 机制验证，使用完整 MovieLens-1M。三阶段核心计算与损失已执行，但公开 MovieLens 没有交易、广告供给和真实曝光漏斗，不能把代理指标解释为论文的业务提升。已执行共享因果用户编码、阶段隔离、三级 SID 自回归、可观测代理决策、双阶段多目标 BCE 与精排向预排蒸馏。未执行真实购买/金额/广告决策、工业物品编码、稀疏 MoE、Sequence-Native Training 的跨曝光摊销、线上服务与 A/B。  multi-stage-ranking generative-retrieval cross-stage-distillation 搜广推 用户历史与排序骨干 OneTrans-V2 的独立阶段注意力与精排到预排蒸馏，为什么不是互相矛盾？ 前向隔离限制服务时可见输入，蒸馏在训练侧通过停止梯度教师提供软监督，影响参数但不让预排在线读精排输出。两条路径作用时点不同。来源没有独立三级基线，不能据阶段均可运行推断级联收益。 示意：训练教预排模仿精排判断合理，上线预排仍须单独执行；若每次先跑完精排再将分数送预排，已经失去原阶段顺序与成本目标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-aab24cdef04fe358">OneTrans-V2 的独立阶段注意力与精排到预排蒸馏，为什么不是互相矛盾？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonetrans-v2">OneTrans-V2: Unifying Retrieval, Pre-rank, and Fine-rank with One Transformer in Industrial Recommender</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前向隔离限制服务时可见输入，蒸馏在训练侧通过停止梯度教师提供软监督，影响参数但不让预排在线读精排输出。两条路径作用时点不同。来源没有独立三级基线，不能据阶段均可运行推断级联收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练教预排模仿精排判断合理，上线预排仍须单独执行；若每次先跑完精排再将分数送预排，已经失去原阶段顺序与成本目标。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.28589">原论文</a> · <a href="../../../../reproductions/2609.28589-onetrans-v2/">实现解读</a> · <a href="#qa-aab24cdef04fe358">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onetrans-v2" data-paper-title="OneTrans-V2: Unifying Retrieval, Pre-rank, and Fine-rank with One Transformer in Industrial Recommender" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OneTrans-V2: Unifying Retrieval, Pre-rank, and Fine-rank with One Transformer in Industrial Recommender 搜广推与 LLM 应用 ByteDance 2026-09-23 工业推荐先检索海量候选，再预排缩小集合，最后精排。三套独立模型会反复编码同一用户历史，也难以让精排经验稳定反馈给上游。OneTrans-V2 保留三个阶段各自的输入与目标，却让它们共享一个因果 Transformer 用户上下文。行为序列不读阶段 token；每个阶段 token 只读请求时刻前的行为，不在阶段之间交叉读取。这既复用昂贵的用户编码，也防止未来信息泄漏。 故 adapter 标记为 concept_demo，不声称复刻 GMV、QPS 或完整 DCGR 业务控制。Fidelity：概念验证（非论文完整复现）；证据等级：L1 机制验证，使用完整 MovieLens-1M。三阶段核心计算与损失已执行，但公开 MovieLens 没有交易、广告供给和真实曝光漏斗，不能把代理指标解释为论文的业务提升。已执行共享因果用户编码、阶段隔离、三级 SID 自回归、可观测代理决策、双阶段多目标 BCE 与精排向预排蒸馏。未执行真实购买/金额/广告决策、工业物品编码、稀疏 MoE、Sequence-Native Training 的跨曝光摊销、线上服务与 A/B。  multi-stage-ranking generative-retrieval cross-stage-distillation 搜广推 用户历史与排序骨干 OneTrans-V2 的 decision offset 为什么只该直接改决策 logits？ 本地机制测试把 offset 作用在两维可观测代理决策，给定决策的 SID 分布以及预排、精排输出不应被直接改写。它检查控制接口独立性，不代表购买金额、广告供给等未观测业务都实现。真实评分阈值也不能改称 CTR/CVR。 示意：提高“发现”代理 offset 应改变决策选择机会，不应直接给所有精排分加常数；若后者一起变，就不是独立决策前缀接口。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-4f365ce2631ae170">OneTrans-V2 的 decision offset 为什么只该直接改决策 logits？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonetrans-v2">OneTrans-V2: Unifying Retrieval, Pre-rank, and Fine-rank with One Transformer in Industrial Recommender</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>本地机制测试把 offset 作用在两维可观测代理决策，给定决策的 SID 分布以及预排、精排输出不应被直接改写。它检查控制接口独立性，不代表购买金额、广告供给等未观测业务都实现。真实评分阈值也不能改称 CTR/CVR。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>提高“发现”代理 offset 应改变决策选择机会，不应直接给所有精排分加常数；若后者一起变，就不是独立决策前缀接口。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.28589">原论文</a> · <a href="../../../../reproductions/2609.28589-onetrans-v2/">实现解读</a> · <a href="#qa-4f365ce2631ae170">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:lazformer" data-paper-title="LazFormer: Scaling Transformers for Industrial Recommendation via Transferable Generative Pre-training" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="LazFormer: Scaling Transformers for Industrial Recommendation via Transferable Generative Pre-training 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-09-14 先做可迁移生成式预训练，再用 ranking residual adapter、近密远疏 token 与 hybrid sparse attention 适配排序；两周 A/B 报告 IPV +5.21%、GMV +9.85%。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。私有日志、生产 checkpoint 与 serving 栈均未复刻。本地只验证公开数据上的核心状态转换；未复刻私有训练数据、大模型生成器、生产流量反馈或在线服务。当前不映射 evolve，避免 registry-only 标签。线上数字来自论文正文 A/B，不与本地 MovieLens 结果混写。本地 seeds 42/43/44 见 metrics/movielens-100k-seeds42-44.json。首个 seed 的统一 NDCG@10 基线为 0.05401，实验组为 0.05048，相对变化 -6.53%。  ranking generative-pretraining residual-adapter hybrid-sparse-attention 搜广推 用户历史与排序骨干 LazFormer 为什么区分可迁移生成预训与 ranking residual adapter？ 预训学习广泛序列与语义结构，排序需适配候选价值和服务目标，残差提供任务特有更新而不完全重写基础表示。近密远疏输入和稀疏注意力另控制历史成本。它不是把已有打分器换个名字，实际训练与服务结构需逐项核验。 示意：预训知道用户从相机到镜头的兴趣演化，排序适配再考虑当前候选价格；单独迁移表示未必已经学会这份业务取舍。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-lazformer-e00dc3de" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9216d984ce591cdc">LazFormer 为什么区分可迁移生成预训与 ranking residual adapter？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alazformer">LazFormer: Scaling Transformers for Industrial Recommendation via Transferable Generative Pre-training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>预训学习广泛序列与语义结构，排序需适配候选价值和服务目标，残差提供任务特有更新而不完全重写基础表示。近密远疏输入和稀疏注意力另控制历史成本。它不是把已有打分器换个名字，实际训练与服务结构需逐项核验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>预训知道用户从相机到镜头的兴趣演化，排序适配再考虑当前候选价格；单独迁移表示未必已经学会这份业务取舍。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.14978">原论文</a> · <a href="../../../../reproductions/2609.14978-lazformer/">实现解读</a> · <a href="#qa-9216d984ce591cdc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:lazformer" data-paper-title="LazFormer: Scaling Transformers for Industrial Recommendation via Transferable Generative Pre-training" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="LazFormer: Scaling Transformers for Industrial Recommendation via Transferable Generative Pre-training 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-09-14 先做可迁移生成式预训练，再用 ranking residual adapter、近密远疏 token 与 hybrid sparse attention 适配排序；两周 A/B 报告 IPV +5.21%、GMV +9.85%。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。私有日志、生产 checkpoint 与 serving 栈均未复刻。本地只验证公开数据上的核心状态转换；未复刻私有训练数据、大模型生成器、生产流量反馈或在线服务。当前不映射 evolve，避免 registry-only 标签。线上数字来自论文正文 A/B，不与本地 MovieLens 结果混写。本地 seeds 42/43/44 见 metrics/movielens-100k-seeds42-44.json。首个 seed 的统一 NDCG@10 基线为 0.05401，实验组为 0.05048，相对变化 -6.53%。  ranking generative-pretraining residual-adapter hybrid-sparse-attention 搜广推 用户历史与排序骨干 LazFormer为什么在可迁移预训练骨干之外保留ranking residual adapter？ 生成式预训练学习通用序列规律，工业排序还需要候选交互与高频更新，直接全量覆盖可能破坏可迁移知识。残差适配为排序新增专门路径，近密远疏token和稀疏attention再控制长历史成本。本地仅保留确定性映射与适配组合组件，不能把其打分结果包装成完整生成式预训练已复现。 示意：预训骨干已掌握长期消费模式，新促销任务需要额外价格交互；残差路径可补这种任务信息，但用一个固定加权器不能证明原论文训练链路已经跑通。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-2a1ae90a18185961">LazFormer为什么在可迁移预训练骨干之外保留ranking residual adapter？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alazformer">LazFormer: Scaling Transformers for Industrial Recommendation via Transferable Generative Pre-training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>生成式预训练学习通用序列规律，工业排序还需要候选交互与高频更新，直接全量覆盖可能破坏可迁移知识。残差适配为排序新增专门路径，近密远疏token和稀疏attention再控制长历史成本。本地仅保留确定性映射与适配组合组件，不能把其打分结果包装成完整生成式预训练已复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>预训骨干已掌握长期消费模式，新促销任务需要额外价格交互；残差路径可补这种任务信息，但用一个固定加权器不能证明原论文训练链路已经跑通。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.14978">原论文</a> · <a href="../../../../reproductions/2609.14978-lazformer/">实现解读</a> · <a href="#qa-2a1ae90a18185961">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:lazformer" data-paper-title="LazFormer: Scaling Transformers for Industrial Recommendation via Transferable Generative Pre-training" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="LazFormer: Scaling Transformers for Industrial Recommendation via Transferable Generative Pre-training 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-09-14 先做可迁移生成式预训练，再用 ranking residual adapter、近密远疏 token 与 hybrid sparse attention 适配排序；两周 A/B 报告 IPV +5.21%、GMV +9.85%。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。私有日志、生产 checkpoint 与 serving 栈均未复刻。本地只验证公开数据上的核心状态转换；未复刻私有训练数据、大模型生成器、生产流量反馈或在线服务。当前不映射 evolve，避免 registry-only 标签。线上数字来自论文正文 A/B，不与本地 MovieLens 结果混写。本地 seeds 42/43/44 见 metrics/movielens-100k-seeds42-44.json。首个 seed 的统一 NDCG@10 基线为 0.05401，实验组为 0.05048，相对变化 -6.53%。  ranking generative-pretraining residual-adapter hybrid-sparse-attention 搜广推 用户历史与排序骨干 近密远疏 token 与固定最近截断，相比长程信息保留有什么区别？ 截断直接丢远史，近密远疏让远期仍以较粗表示存在，近期保持细节，配合稀疏连接减少两两开销。压缩可能丢稀有事件，不能说信息无损；本地确定性映射与残差仅示意部分接口，不等于原文长序列预训。 示意：近两天点击逐条保留，去年兴趣按组摘要；比只看最近十条更能记长期偏好，但旧摘要未必保留一次重要的特殊需求。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a9b8ac400463b5cf">近密远疏 token 与固定最近截断，相比长程信息保留有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alazformer">LazFormer: Scaling Transformers for Industrial Recommendation via Transferable Generative Pre-training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>截断直接丢远史，近密远疏让远期仍以较粗表示存在，近期保持细节，配合稀疏连接减少两两开销。压缩可能丢稀有事件，不能说信息无损；本地确定性映射与残差仅示意部分接口，不等于原文长序列预训。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>近两天点击逐条保留，去年兴趣按组摘要；比只看最近十条更能记长期偏好，但旧摘要未必保留一次重要的特殊需求。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.14978">原论文</a> · <a href="../../../../reproductions/2609.14978-lazformer/">实现解读</a> · <a href="#qa-a9b8ac400463b5cf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:lazformer" data-paper-title="LazFormer: Scaling Transformers for Industrial Recommendation via Transferable Generative Pre-training" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="LazFormer: Scaling Transformers for Industrial Recommendation via Transferable Generative Pre-training 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-09-14 先做可迁移生成式预训练，再用 ranking residual adapter、近密远疏 token 与 hybrid sparse attention 适配排序；两周 A/B 报告 IPV +5.21%、GMV +9.85%。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。私有日志、生产 checkpoint 与 serving 栈均未复刻。本地只验证公开数据上的核心状态转换；未复刻私有训练数据、大模型生成器、生产流量反馈或在线服务。当前不映射 evolve，避免 registry-only 标签。线上数字来自论文正文 A/B，不与本地 MovieLens 结果混写。本地 seeds 42/43/44 见 metrics/movielens-100k-seeds42-44.json。首个 seed 的统一 NDCG@10 基线为 0.05401，实验组为 0.05048，相对变化 -6.53%。  ranking generative-pretraining residual-adapter hybrid-sparse-attention 搜广推 用户历史与排序骨干 LazFormer 本地实现为什么不能用论文两周 A/B 数字作为自身训练结果？ 来源明确限制为确定性候选打分、可迁移映射与 ranking residual，并只在验证选融合系数，没有完整大模型训练和线上系统。应报告实际公开协议负结果，把论文业务提升单独引用，不能用机制名称覆盖缺失链路。 示意：本地电影分数有一项 residual，并不表示已完成生成预训；将原文 GMV 百分比填进本地指标，会混淆完全不同证据来源。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0bb2b4577fe253e9">LazFormer 本地实现为什么不能用论文两周 A/B 数字作为自身训练结果？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alazformer">LazFormer: Scaling Transformers for Industrial Recommendation via Transferable Generative Pre-training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>来源明确限制为确定性候选打分、可迁移映射与 ranking residual，并只在验证选融合系数，没有完整大模型训练和线上系统。应报告实际公开协议负结果，把论文业务提升单独引用，不能用机制名称覆盖缺失链路。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>本地电影分数有一项 residual，并不表示已完成生成预训；将原文 GMV 百分比填进本地指标，会混淆完全不同证据来源。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.14978">原论文</a> · <a href="../../../../reproductions/2609.14978-lazformer/">实现解读</a> · <a href="#qa-0bb2b4577fe253e9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:chronicle-rec" data-paper-title="ChronicleRec: Pre-training Temporally Anchored Tokens for Lifelong User Modeling" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="ChronicleRec: Pre-training Temporally Anchored Tokens for Lifelong User Modeling 搜广推与 LLM 应用 Tencent 2026-09-11 逐候选检索超长历史会重复计算，统一压成无序 token 又容易丢失时间结构。ChronicleRec 对近、中、远历史采用逐渐增大的合并步幅，把 query token 插入时间轴并使用 causal encoder，使每个 token 只概括其锚点之前的历史；多分支分别遮掉不同长度的近期行为，alignment 预训练再用压缩过去预测近期意图。生成的 Chronicle Tokens 与候选无关，可缓存并复用于多个候选。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行近密远疏合并、因果 query 锚点、多 horizon 分支与面向近期目标的 alignment；不复刻腾讯私有 MixFormer 与缓存系统。公开短序列不能代表 2K–4K 乃至更长的生产历史；本地用线性 alignment 替代四层 causal Transformer，未复刻 AdLive、MixFormer 和异步 KV cache。实现只声明 CPU 公开数据核心机制。MovieLens 100K、seeds 42/43/44 的固定协议见 metrics/movielens-100k-seeds42-44.json。  ranking long-sequence sequence-compression pretraining 搜广推 用户历史与排序骨干 ChronicleRec 为什么要同时表达近、中、远历史，而不只生成几枚无序兴趣 token？ 多尺度合并保留兴趣的时间结构，query token 的锚点限定它总结哪段过去，使模型区分稳定偏好与近期变化。候选无关 Chronicle Tokens 可缓存，但这种公共压缩不保证保存所有目标相关细节，时间布局仍是理解摘要含义的一部分。 示意：长期爱科幻与本周集中看育儿可分别留下不同时间尺度线索；若全部变成无序“科幻、育儿”两词，模型难判断哪个刚出现。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-chronicle-rec-efcf1d9a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ae60800a02e46d24">ChronicleRec 为什么要同时表达近、中、远历史，而不只生成几枚无序兴趣 token？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Achronicle-rec">ChronicleRec: Pre-training Temporally Anchored Tokens for Lifelong User Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多尺度合并保留兴趣的时间结构，query token 的锚点限定它总结哪段过去，使模型区分稳定偏好与近期变化。候选无关 Chronicle Tokens 可缓存，但这种公共压缩不保证保存所有目标相关细节，时间布局仍是理解摘要含义的一部分。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>长期爱科幻与本周集中看育儿可分别留下不同时间尺度线索；若全部变成无序“科幻、育儿”两词，模型难判断哪个刚出现。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.12375">原论文</a> · <a href="../../../../reproductions/2609.12375-chronicle-rec/">实现解读</a> · <a href="#qa-ae60800a02e46d24">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:chronicle-rec" data-paper-title="ChronicleRec: Pre-training Temporally Anchored Tokens for Lifelong User Modeling" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="ChronicleRec: Pre-training Temporally Anchored Tokens for Lifelong User Modeling 搜广推与 LLM 应用 Tencent 2026-09-11 逐候选检索超长历史会重复计算，统一压成无序 token 又容易丢失时间结构。ChronicleRec 对近、中、远历史采用逐渐增大的合并步幅，把 query token 插入时间轴并使用 causal encoder，使每个 token 只概括其锚点之前的历史；多分支分别遮掉不同长度的近期行为，alignment 预训练再用压缩过去预测近期意图。生成的 Chronicle Tokens 与候选无关，可缓存并复用于多个候选。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行近密远疏合并、因果 query 锚点、多 horizon 分支与面向近期目标的 alignment；不复刻腾讯私有 MixFormer 与缓存系统。公开短序列不能代表 2K–4K 乃至更长的生产历史；本地用线性 alignment 替代四层 causal Transformer，未复刻 AdLive、MixFormer 和异步 KV cache。实现只声明 CPU 公开数据核心机制。MovieLens 100K、seeds 42/43/44 的固定协议见 metrics/movielens-100k-seeds42-44.json。  ranking long-sequence sequence-compression pretraining 搜广推 用户历史与排序骨干 Chronicle Token为什么必须带时间锚点并只概括锚点之前的历史？ 没有时间边界的摘要容易把未来行为混入较早时刻的表示，既破坏训练因果性，也让跨请求缓存语义不清。ChronicleRec以不同粒度压缩远近历史，在时间轴上放置query，只允许它读取此前事件，再用多种近期遮蔽对齐短期意图。候选无关的锚定摘要才具备跨候选复用的基础。 示意：周三的摘要不能包含周五才购买的相机，否则周四推荐镜头时已偷看未来；固定时间锚点后，可让同一摘要服务当时的多个候选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-fe7e940e49d3f624">Chronicle Token为什么必须带时间锚点并只概括锚点之前的历史？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Achronicle-rec">ChronicleRec: Pre-training Temporally Anchored Tokens for Lifelong User Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有时间边界的摘要容易把未来行为混入较早时刻的表示，既破坏训练因果性，也让跨请求缓存语义不清。ChronicleRec以不同粒度压缩远近历史，在时间轴上放置query，只允许它读取此前事件，再用多种近期遮蔽对齐短期意图。候选无关的锚定摘要才具备跨候选复用的基础。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>周三的摘要不能包含周五才购买的相机，否则周四推荐镜头时已偷看未来；固定时间锚点后，可让同一摘要服务当时的多个候选。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.12375">原论文</a> · <a href="../../../../reproductions/2609.12375-chronicle-rec/">实现解读</a> · <a href="#qa-fe7e940e49d3f624">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:chronicle-rec" data-paper-title="ChronicleRec: Pre-training Temporally Anchored Tokens for Lifelong User Modeling" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="ChronicleRec: Pre-training Temporally Anchored Tokens for Lifelong User Modeling 搜广推与 LLM 应用 Tencent 2026-09-11 逐候选检索超长历史会重复计算，统一压成无序 token 又容易丢失时间结构。ChronicleRec 对近、中、远历史采用逐渐增大的合并步幅，把 query token 插入时间轴并使用 causal encoder，使每个 token 只概括其锚点之前的历史；多分支分别遮掉不同长度的近期行为，alignment 预训练再用压缩过去预测近期意图。生成的 Chronicle Tokens 与候选无关，可缓存并复用于多个候选。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行近密远疏合并、因果 query 锚点、多 horizon 分支与面向近期目标的 alignment；不复刻腾讯私有 MixFormer 与缓存系统。公开短序列不能代表 2K–4K 乃至更长的生产历史；本地用线性 alignment 替代四层 causal Transformer，未复刻 AdLive、MixFormer 和异步 KV cache。实现只声明 CPU 公开数据核心机制。MovieLens 100K、seeds 42/43/44 的固定协议见 metrics/movielens-100k-seeds42-44.json。  ranking long-sequence sequence-compression pretraining 搜广推 用户历史与排序骨干 ChronicleRec 的 alignment 预训练与普通下一物品预测，监督焦点有什么不同？ 它通过不同分支遮掉一定长度近期行为，让压缩过去预测近期意图，迫使摘要在缺失最近证据时仍有用。普通下一物品预测可能主要依赖紧邻行为。遮蔽提供更强压缩训练，但不能在评估时把被遮目标又放回输入，否则失去该检验含义。 示意：隐藏最近三次育儿浏览，让更早历史尝试预测这段新意图；这比只根据最后一条育儿内容再猜下一条更难，也更能检查长程摘要。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-491ae24f291ae309">ChronicleRec 的 alignment 预训练与普通下一物品预测，监督焦点有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Achronicle-rec">ChronicleRec: Pre-training Temporally Anchored Tokens for Lifelong User Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它通过不同分支遮掉一定长度近期行为，让压缩过去预测近期意图，迫使摘要在缺失最近证据时仍有用。普通下一物品预测可能主要依赖紧邻行为。遮蔽提供更强压缩训练，但不能在评估时把被遮目标又放回输入，否则失去该检验含义。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>隐藏最近三次育儿浏览，让更早历史尝试预测这段新意图；这比只根据最后一条育儿内容再猜下一条更难，也更能检查长程摘要。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.12375">原论文</a> · <a href="../../../../reproductions/2609.12375-chronicle-rec/">实现解读</a> · <a href="#qa-491ae24f291ae309">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:chronicle-rec" data-paper-title="ChronicleRec: Pre-training Temporally Anchored Tokens for Lifelong User Modeling" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="ChronicleRec: Pre-training Temporally Anchored Tokens for Lifelong User Modeling 搜广推与 LLM 应用 Tencent 2026-09-11 逐候选检索超长历史会重复计算，统一压成无序 token 又容易丢失时间结构。ChronicleRec 对近、中、远历史采用逐渐增大的合并步幅，把 query token 插入时间轴并使用 causal encoder，使每个 token 只概括其锚点之前的历史；多分支分别遮掉不同长度的近期行为，alignment 预训练再用压缩过去预测近期意图。生成的 Chronicle Tokens 与候选无关，可缓存并复用于多个候选。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行近密远疏合并、因果 query 锚点、多 horizon 分支与面向近期目标的 alignment；不复刻腾讯私有 MixFormer 与缓存系统。公开短序列不能代表 2K–4K 乃至更长的生产历史；本地用线性 alignment 替代四层 causal Transformer，未复刻 AdLive、MixFormer 和异步 KV cache。实现只声明 CPU 公开数据核心机制。MovieLens 100K、seeds 42/43/44 的固定协议见 metrics/movielens-100k-seeds42-44.json。  ranking long-sequence sequence-compression pretraining 搜广推 用户历史与排序骨干 Chronicle Token 的窗口 pooling 为什么要按有效 mask 数量归一，并在 query 位置读出？ 窗口可能含 padding，按总长度平均会使短历史被人为缩小；有效 mask 和安全分母只汇聚真实事件。因果编码后在 query 锚点读取，才能保证状态只总结锚点前信息。读取其他位置或让 padding 参与，会改变压缩语义而不一定触发维度错误。 示意：窗口四格只有两条真实行为，应除以二而非四；query 放在二者之后才能总结它们，放到中间就不应看到后面的事件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ae7ea3a33cae636b">Chronicle Token 的窗口 pooling 为什么要按有效 mask 数量归一，并在 query 位置读出？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Achronicle-rec">ChronicleRec: Pre-training Temporally Anchored Tokens for Lifelong User Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>窗口可能含 padding，按总长度平均会使短历史被人为缩小；有效 mask 和安全分母只汇聚真实事件。因果编码后在 query 锚点读取，才能保证状态只总结锚点前信息。读取其他位置或让 padding 参与，会改变压缩语义而不一定触发维度错误。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>窗口四格只有两条真实行为，应除以二而非四；query 放在二者之后才能总结它们，放到中间就不应看到后面的事件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.12375">原论文</a> · <a href="../../../../reproductions/2609.12375-chronicle-rec/">实现解读</a> · <a href="#qa-ae7ea3a33cae636b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unirec" data-paper-title="UniRec: Cross-Stage Multi-Task Fusion with Preference Optimization for Cascaded Recommender Systems" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="UniRec: Cross-Stage Multi-Task Fusion with Preference Optimization for Cascaded Recommender Systems 搜广推与 LLM 应用 Kuaishou 2026-09-10 预排和精排的候选范围、输入质量和延迟约束不同，直接复制精排的融合权重不能保证上游排序一致。UniRec 以部分共享 embedding、独立 DCN/Mixer 与 AutoInt-Lite 塔联合训练两阶段融合模块；下游偏好只作为上游训练监督，不作为预排线上输入。v3 明确保留多目标冲突的 CPPA、置信剪枝 CAPP，以及以组内 KL 抑制视频时长等属性引起的分布漂移。 成本过高，不复现（审查 DONE）。复现级别：组件诊断，非完整论文复现。复现级别：组件诊断，非完整论文复现。新增 v3 的 CPPA/CAPP、AGRR 组内 KL 与跨阶段偏好目标，验证前向、梯度和负对照。旧 unirec NumPy adapter 是固定权重启发式，现明确降为 concept_demo；历史测量与负结果完整保留。旧 MovieLens 100K、seeds 42/43/44 结果见 metrics/movielens-100k-seeds42-44.json。  pre-ranking ranking cross-stage-alignment industrial-recommendation 搜广推 用户历史与排序骨干 预排精排UniRec为什么保留两条独立塔？ 两阶段输入质量、候选范围和时延不同，部分共享embedding但保留不同交互结构，再以训练对齐传下游偏好。精排信息不变成预排线上可见输入。 例如精排拥有昂贵细特征，上游只能通过监督学习其偏好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-unirec-cd2efe22" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-505d1682319fe757">预排精排UniRec为什么保留两条独立塔？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunirec">UniRec: Cross-Stage Multi-Task Fusion with Preference Optimization for Cascaded Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两阶段输入质量、候选范围和时延不同，部分共享embedding但保留不同交互结构，再以训练对齐传下游偏好。精排信息不变成预排线上可见输入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如精排拥有昂贵细特征，上游只能通过监督学习其偏好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11052">原论文</a> · <a href="../../../../reproductions/2609.11052-unirec/">实现解读</a> · <a href="#qa-505d1682319fe757">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unirec" data-paper-title="UniRec: Cross-Stage Multi-Task Fusion with Preference Optimization for Cascaded Recommender Systems" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="UniRec: Cross-Stage Multi-Task Fusion with Preference Optimization for Cascaded Recommender Systems 搜广推与 LLM 应用 Kuaishou 2026-09-10 预排和精排的候选范围、输入质量和延迟约束不同，直接复制精排的融合权重不能保证上游排序一致。UniRec 以部分共享 embedding、独立 DCN/Mixer 与 AutoInt-Lite 塔联合训练两阶段融合模块；下游偏好只作为上游训练监督，不作为预排线上输入。v3 明确保留多目标冲突的 CPPA、置信剪枝 CAPP，以及以组内 KL 抑制视频时长等属性引起的分布漂移。 成本过高，不复现（审查 DONE）。复现级别：组件诊断，非完整论文复现。复现级别：组件诊断，非完整论文复现。新增 v3 的 CPPA/CAPP、AGRR 组内 KL 与跨阶段偏好目标，验证前向、梯度和负对照。旧 unirec NumPy adapter 是固定权重启发式，现明确降为 concept_demo；历史测量与负结果完整保留。旧 MovieLens 100K、seeds 42/43/44 结果见 metrics/movielens-100k-seeds42-44.json。  pre-ranking ranking cross-stage-alignment industrial-recommendation 搜广推 用户历史与排序骨干 UniRec 的 CPPA 为什么保留同一 pair 的正反目标证据，而不先多数表决成单一胜负？ 点击、购买等目标可能对同一候选对给出相反偏好，多数表决会抹去冲突强度和少数目标。CPPA 分别累积正反证据，两种方向的 softplus 惩罚同时存在；CAPP 再选置信差距大的有向 pair，属性组 KL 控制分布漂移。下游偏好用于训练上游，不能作为预排服务时偷读的输入。 示意：甲比乙更易点击，乙比甲更易购买。保留两方向损失可表达这份取舍；若直接三票对两票判甲胜，购买侧反对证据就会被丢掉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-0c25f39de037db51">UniRec 的 CPPA 为什么保留同一 pair 的正反目标证据，而不先多数表决成单一胜负？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunirec">UniRec: Cross-Stage Multi-Task Fusion with Preference Optimization for Cascaded Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>点击、购买等目标可能对同一候选对给出相反偏好，多数表决会抹去冲突强度和少数目标。CPPA 分别累积正反证据，两种方向的 softplus 惩罚同时存在；CAPP 再选置信差距大的有向 pair，属性组 KL 控制分布漂移。下游偏好用于训练上游，不能作为预排服务时偷读的输入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>甲比乙更易点击，乙比甲更易购买。保留两方向损失可表达这份取舍；若直接三票对两票判甲胜，购买侧反对证据就会被丢掉。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11052">原论文</a> · <a href="../../../../reproductions/2609.11052-unirec/">实现解读</a> · <a href="#qa-0c25f39de037db51">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unirec" data-paper-title="UniRec: Cross-Stage Multi-Task Fusion with Preference Optimization for Cascaded Recommender Systems" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="UniRec: Cross-Stage Multi-Task Fusion with Preference Optimization for Cascaded Recommender Systems 搜广推与 LLM 应用 Kuaishou 2026-09-10 预排和精排的候选范围、输入质量和延迟约束不同，直接复制精排的融合权重不能保证上游排序一致。UniRec 以部分共享 embedding、独立 DCN/Mixer 与 AutoInt-Lite 塔联合训练两阶段融合模块；下游偏好只作为上游训练监督，不作为预排线上输入。v3 明确保留多目标冲突的 CPPA、置信剪枝 CAPP，以及以组内 KL 抑制视频时长等属性引起的分布漂移。 成本过高，不复现（审查 DONE）。复现级别：组件诊断，非完整论文复现。复现级别：组件诊断，非完整论文复现。新增 v3 的 CPPA/CAPP、AGRR 组内 KL 与跨阶段偏好目标，验证前向、梯度和负对照。旧 unirec NumPy adapter 是固定权重启发式，现明确降为 concept_demo；历史测量与负结果完整保留。旧 MovieLens 100K、seeds 42/43/44 结果见 metrics/movielens-100k-seeds42-44.json。  pre-ranking ranking cross-stage-alignment industrial-recommendation 搜广推 用户历史与排序骨干 CPPA与先对多个目标多数表决有什么不同？ 相反目标的正负证据同时进入softplus，保留冲突强度；多数表决只留一边会丢信息。CAPP再按置信选有向pair，AGRR另处理属性组漂移，不能混成同一权重。 例如点击赞成A、时长赞成B，两个方向都需留在目标里。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-dee5064fb3689990">CPPA与先对多个目标多数表决有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunirec">UniRec: Cross-Stage Multi-Task Fusion with Preference Optimization for Cascaded Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相反目标的正负证据同时进入softplus，保留冲突强度；多数表决只留一边会丢信息。CAPP再按置信选有向pair，AGRR另处理属性组漂移，不能混成同一权重。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如点击赞成A、时长赞成B，两个方向都需留在目标里。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11052">原论文</a> · <a href="../../../../reproductions/2609.11052-unirec/">实现解读</a> · <a href="#qa-dee5064fb3689990">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:unirec" data-paper-title="UniRec: Cross-Stage Multi-Task Fusion with Preference Optimization for Cascaded Recommender Systems" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="UniRec: Cross-Stage Multi-Task Fusion with Preference Optimization for Cascaded Recommender Systems 搜广推与 LLM 应用 Kuaishou 2026-09-10 预排和精排的候选范围、输入质量和延迟约束不同，直接复制精排的融合权重不能保证上游排序一致。UniRec 以部分共享 embedding、独立 DCN/Mixer 与 AutoInt-Lite 塔联合训练两阶段融合模块；下游偏好只作为上游训练监督，不作为预排线上输入。v3 明确保留多目标冲突的 CPPA、置信剪枝 CAPP，以及以组内 KL 抑制视频时长等属性引起的分布漂移。 成本过高，不复现（审查 DONE）。复现级别：组件诊断，非完整论文复现。复现级别：组件诊断，非完整论文复现。新增 v3 的 CPPA/CAPP、AGRR 组内 KL 与跨阶段偏好目标，验证前向、梯度和负对照。旧 unirec NumPy adapter 是固定权重启发式，现明确降为 concept_demo；历史测量与负结果完整保留。旧 MovieLens 100K、seeds 42/43/44 结果见 metrics/movielens-100k-seeds42-44.json。  pre-ranking ranking cross-stage-alignment industrial-recommendation 搜广推 用户历史与排序骨干 UniRec跨阶段项和AGRR怎样避免梯度与剪枝混淆？ 跨阶段只用survivor并冻结精排方向，AGRR证据从未剪枝输入算再在属性组构成KL目标。它不是组中心化分数，标准差和分位tie本地约定需明示。 例如先剪掉冲突pair再统计原证据，会改变AGRR原本观察到的分布。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7061b74a6ba3a598">UniRec跨阶段项和AGRR怎样避免梯度与剪枝混淆？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aunirec">UniRec: Cross-Stage Multi-Task Fusion with Preference Optimization for Cascaded Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>跨阶段只用survivor并冻结精排方向，AGRR证据从未剪枝输入算再在属性组构成KL目标。它不是组中心化分数，标准差和分位tie本地约定需明示。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先剪掉冲突pair再统计原证据，会改变AGRR原本观察到的分布。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11052">原论文</a> · <a href="../../../../reproductions/2609.11052-unirec/">实现解读</a> · <a href="#qa-7061b74a6ba3a598">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sequenceo1" data-paper-title="SequenceO1: End-to-End Ultra-Long (100K) Sequence Modeling in Recommendation with Low-Rank Caching" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="SequenceO1: End-to-End Ultra-Long (100K) Sequence Modeling in Recommendation with Low-Rank Caching 搜广推与 LLM 应用 ByteDance / Douyin 2026-09-08 直接注意全部历史难以服务 100K 级用户行为。SequenceO1 用 Sketch Attention 把远期历史压缩为固定数量原型，并保留近期行为分支；STCA 让 sketch 与 recent 信息并行交互，控制成本同时保留长期兴趣。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行固定预算 prototype sketch 与 recent 双分支；MovieLens 不具备论文的 100K 事件历史。MovieLens 100K 三种子结果见 metrics/movielens-100k-seeds42-44.json。原型由训练历史 farthest-first 初始化并做一次 assignment/update，固定为 4 个；未实现 MRLB、FlashSA 或线上 cache，且暂不登记不可执行的 evolve 标签。  long-sequence sketch-attention prototype-compression industrial-recommendation 搜广推 用户历史与排序骨干 SequenceO1的sketch是原样保留的一段旧历史吗？ 不是。远期历史被压成固定预算的原型表示，近期分支另保留较细行为。原型概括长期模式，并非可逐条还原的完整事件副本；固定的是表示预算，不是原始历史长度。先分清摘要表示与原始记录，才能判断信息可能在哪里损失。 教学例子：几千次远期行为可被若干兴趣原型概括；看到一个原型不能反推出所有事件的准确时间和顺序。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-sequenceo1-53b97674" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9ce0f15f4b39cfbb">SequenceO1的sketch是原样保留的一段旧历史吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asequenceo1">SequenceO1: End-to-End Ultra-Long (100K) Sequence Modeling in Recommendation with Low-Rank Caching</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。远期历史被压成固定预算的原型表示，近期分支另保留较细行为。原型概括长期模式，并非可逐条还原的完整事件副本；固定的是表示预算，不是原始历史长度。先分清摘要表示与原始记录，才能判断信息可能在哪里损失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>几千次远期行为可被若干兴趣原型概括；看到一个原型不能反推出所有事件的准确时间和顺序。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08443">原论文</a> · <a href="../../../../reproductions/2609.08443-sequenceo1/">实现解读</a> · <a href="#qa-9ce0f15f4b39cfbb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sequenceo1" data-paper-title="SequenceO1: End-to-End Ultra-Long (100K) Sequence Modeling in Recommendation with Low-Rank Caching" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="SequenceO1: End-to-End Ultra-Long (100K) Sequence Modeling in Recommendation with Low-Rank Caching 搜广推与 LLM 应用 ByteDance / Douyin 2026-09-08 直接注意全部历史难以服务 100K 级用户行为。SequenceO1 用 Sketch Attention 把远期历史压缩为固定数量原型，并保留近期行为分支；STCA 让 sketch 与 recent 信息并行交互，控制成本同时保留长期兴趣。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行固定预算 prototype sketch 与 recent 双分支；MovieLens 不具备论文的 100K 事件历史。MovieLens 100K 三种子结果见 metrics/movielens-100k-seeds42-44.json。原型由训练历史 farthest-first 初始化并做一次 assignment/update，固定为 4 个；未实现 MRLB、FlashSA 或线上 cache，且暂不登记不可执行的 evolve 标签。  long-sequence sketch-attention prototype-compression industrial-recommendation 搜广推 用户历史与排序骨干 SequenceO1 把远期历史压成固定 sketch 后，哪些成本变得可控，哪些仍会随历史变化？ 固定预算原型让后续候选匹配与 sketch 交互的规模不再随远期事件数直接增长，近期分支保留即时行为，STCA 再连接两种时间尺度。但读取历史、构造或更新 sketch 仍有成本，不能把端到端处理十万行为都称为常数时间。本地原型近似只验证预算化远期分支，不是完整工业注意力路径。 示意：十万条旧行为先压成几十个兴趣原型，每个候选只与这些原型匹配；新行为到来仍需更新摘要。像查一份定长索引很快，但建立与维护索引不是免费的。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8c0f466df9e7082f">SequenceO1 把远期历史压成固定 sketch 后，哪些成本变得可控，哪些仍会随历史变化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asequenceo1">SequenceO1: End-to-End Ultra-Long (100K) Sequence Modeling in Recommendation with Low-Rank Caching</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定预算原型让后续候选匹配与 sketch 交互的规模不再随远期事件数直接增长，近期分支保留即时行为，STCA 再连接两种时间尺度。但读取历史、构造或更新 sketch 仍有成本，不能把端到端处理十万行为都称为常数时间。本地原型近似只验证预算化远期分支，不是完整工业注意力路径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>十万条旧行为先压成几十个兴趣原型，每个候选只与这些原型匹配；新行为到来仍需更新摘要。像查一份定长索引很快，但建立与维护索引不是免费的。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08443">原论文</a> · <a href="../../../../reproductions/2609.08443-sequenceo1/">实现解读</a> · <a href="#qa-8c0f466df9e7082f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sequenceo1" data-paper-title="SequenceO1: End-to-End Ultra-Long (100K) Sequence Modeling in Recommendation with Low-Rank Caching" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="SequenceO1: End-to-End Ultra-Long (100K) Sequence Modeling in Recommendation with Low-Rank Caching 搜广推与 LLM 应用 ByteDance / Douyin 2026-09-08 直接注意全部历史难以服务 100K 级用户行为。SequenceO1 用 Sketch Attention 把远期历史压缩为固定数量原型，并保留近期行为分支；STCA 让 sketch 与 recent 信息并行交互，控制成本同时保留长期兴趣。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行固定预算 prototype sketch 与 recent 双分支；MovieLens 不具备论文的 100K 事件历史。MovieLens 100K 三种子结果见 metrics/movielens-100k-seeds42-44.json。原型由训练历史 farthest-first 初始化并做一次 assignment/update，固定为 4 个；未实现 MRLB、FlashSA 或线上 cache，且暂不登记不可执行的 evolve 标签。  long-sequence sketch-attention prototype-compression industrial-recommendation 搜广推 用户历史与排序骨干 Sketch加recent与纯recent截断的主要信息差别？ 前者保留长期模式的压缩通路，后者完全不看远期；固定原型也可能合并不同兴趣，不能因为有长期分支就宣称无损保留全部历史。 例如近期偶然看旅行，远期运动兴趣仍可能通过原型影响召回。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d39fd3f417fbc390">Sketch加recent与纯recent截断的主要信息差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asequenceo1">SequenceO1: End-to-End Ultra-Long (100K) Sequence Modeling in Recommendation with Low-Rank Caching</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者保留长期模式的压缩通路，后者完全不看远期；固定原型也可能合并不同兴趣，不能因为有长期分支就宣称无损保留全部历史。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如近期偶然看旅行，远期运动兴趣仍可能通过原型影响召回。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08443">原论文</a> · <a href="../../../../reproductions/2609.08443-sequenceo1/">实现解读</a> · <a href="#qa-d39fd3f417fbc390">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sequenceo1" data-paper-title="SequenceO1: End-to-End Ultra-Long (100K) Sequence Modeling in Recommendation with Low-Rank Caching" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="SequenceO1: End-to-End Ultra-Long (100K) Sequence Modeling in Recommendation with Low-Rank Caching 搜广推与 LLM 应用 ByteDance / Douyin 2026-09-08 直接注意全部历史难以服务 100K 级用户行为。SequenceO1 用 Sketch Attention 把远期历史压缩为固定数量原型，并保留近期行为分支；STCA 让 sketch 与 recent 信息并行交互，控制成本同时保留长期兴趣。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。执行固定预算 prototype sketch 与 recent 双分支；MovieLens 不具备论文的 100K 事件历史。MovieLens 100K 三种子结果见 metrics/movielens-100k-seeds42-44.json。原型由训练历史 farthest-first 初始化并做一次 assignment/update，固定为 4 个；未实现 MRLB、FlashSA 或线上 cache，且暂不登记不可执行的 evolve 标签。  long-sequence sketch-attention prototype-compression industrial-recommendation 搜广推 用户历史与排序骨干 本地0.65/0.35融合可直接当原文100K系统公式吗？ 不能，这是公开参考打分代理，原型预算与recent分支可验证成本方向，未复刻生产STCA与长历史服务。标准化与候选mask应固定，不能用测试结果挑融合权重。 例如小目录混合分数的提升，不等于十万历史端到端延迟改善。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ede261f2274aee28">本地0.65/0.35融合可直接当原文100K系统公式吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asequenceo1">SequenceO1: End-to-End Ultra-Long (100K) Sequence Modeling in Recommendation with Low-Rank Caching</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，这是公开参考打分代理，原型预算与recent分支可验证成本方向，未复刻生产STCA与长历史服务。标准化与候选mask应固定，不能用测试结果挑融合权重。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如小目录混合分数的提升，不等于十万历史端到端延迟改善。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08443">原论文</a> · <a href="../../../../reproductions/2609.08443-sequenceo1/">实现解读</a> · <a href="#qa-ede261f2274aee28">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rest" data-paper-title="From Language to Behavior: Scaling Sequence Transformers for Industrial Recommendation Ranking with Rec-Native Designs" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="From Language to Behavior: Scaling Sequence Transformers for Industrial Recommendation Ranking with Rec-Native Designs 搜广推与 LLM 应用 ByteDance 2026-09-01 ReST 不直接照搬语言 Transformer：双门控注意力抑制行为噪声，RoPE 与相对时间编码同时表达顺序和时间间隔；系统侧把一次请求拆成可复用的重型用户 encoder 与轻型候选 cross decoder，实现 compute-once、decode-many。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现双门控时序编码、重用户编码/轻候选交叉的计算路径。未复刻私有行为日志、生产 checkpoint 和 shared-prefix serving kernel；本实现仅声明 CPU 公共数据核心机制，不宣传 CUDA 路径。在 MovieLens 100K 固定 220 用户/360 物品协议上执行时序衰减、信号门控与候选交叉路径；三 seed 结果见 metrics/public-seeds42-44.json。  ranking-network long-sequence shared-prefix-serving 搜广推 用户历史与排序骨干 ReST 为什么同时使用 RoPE 与相对时间编码？ 位置顺序与真实间隔不同，相邻两次行为可隔一分钟或一年；RoPE 提供序列位置关系，时间编码补充节奏，双门控再筛噪声。多种编码不保证捕捉所有周期，也不能将时间间隔越大都简单视为无用。 示意：同样相邻的两次相机浏览，一次隔五分钟是集中比较，另一次隔半年可能是新需求；仅位置一格无法区分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-rest-5ed56a69" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-587482482f0ab50e">ReST 为什么同时使用 RoPE 与相对时间编码？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arest">From Language to Behavior: Scaling Sequence Transformers for Industrial Recommendation Ranking with Rec-Native Designs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>位置顺序与真实间隔不同，相邻两次行为可隔一分钟或一年；RoPE 提供序列位置关系，时间编码补充节奏，双门控再筛噪声。多种编码不保证捕捉所有周期，也不能将时间间隔越大都简单视为无用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同样相邻的两次相机浏览，一次隔五分钟是集中比较，另一次隔半年可能是新需求；仅位置一格无法区分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.01240">原论文</a> · <a href="../../../../reproductions/2609.01240-rest/">实现解读</a> · <a href="#qa-587482482f0ab50e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rest" data-paper-title="From Language to Behavior: Scaling Sequence Transformers for Industrial Recommendation Ranking with Rec-Native Designs" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="From Language to Behavior: Scaling Sequence Transformers for Industrial Recommendation Ranking with Rec-Native Designs 搜广推与 LLM 应用 ByteDance 2026-09-01 ReST 不直接照搬语言 Transformer：双门控注意力抑制行为噪声，RoPE 与相对时间编码同时表达顺序和时间间隔；系统侧把一次请求拆成可复用的重型用户 encoder 与轻型候选 cross decoder，实现 compute-once、decode-many。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现双门控时序编码、重用户编码/轻候选交叉的计算路径。未复刻私有行为日志、生产 checkpoint 和 shared-prefix serving kernel；本实现仅声明 CPU 公共数据核心机制，不宣传 CUDA 路径。在 MovieLens 100K 固定 220 用户/360 物品协议上执行时序衰减、信号门控与候选交叉路径；三 seed 结果见 metrics/public-seeds42-44.json。  ranking-network long-sequence shared-prefix-serving 搜广推 用户历史与排序骨干 ReST 的 compute-once、decode-many 为什么需要区分重型用户编码和轻型候选交互？ 长历史的门控注意力与顺序、时间间隔建模是用户侧公共成本，先算一次可供同请求多个候选使用。候选 cross decoder 再按物品读取相关用户信息，保留候选相关交互而避免重复完整编码。双门控减少噪声，但共享只适用于不依赖候选的状态；历史改变或缓存版本变化时仍要更新。 示意：对同一用户评估两百部电影，先统一编码其观看历史与间隔，再让每部电影做轻量查询。不能把为某个候选专门计算的交互结果直接当成所有电影通用用户表示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-ffc3ae495ed6b99c">ReST 的 compute-once、decode-many 为什么需要区分重型用户编码和轻型候选交互？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arest">From Language to Behavior: Scaling Sequence Transformers for Industrial Recommendation Ranking with Rec-Native Designs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长历史的门控注意力与顺序、时间间隔建模是用户侧公共成本，先算一次可供同请求多个候选使用。候选 cross decoder 再按物品读取相关用户信息，保留候选相关交互而避免重复完整编码。双门控减少噪声，但共享只适用于不依赖候选的状态；历史改变或缓存版本变化时仍要更新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>对同一用户评估两百部电影，先统一编码其观看历史与间隔，再让每部电影做轻量查询。不能把为某个候选专门计算的交互结果直接当成所有电影通用用户表示。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.01240">原论文</a> · <a href="../../../../reproductions/2609.01240-rest/">实现解读</a> · <a href="#qa-ffc3ae495ed6b99c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rest" data-paper-title="From Language to Behavior: Scaling Sequence Transformers for Industrial Recommendation Ranking with Rec-Native Designs" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="From Language to Behavior: Scaling Sequence Transformers for Industrial Recommendation Ranking with Rec-Native Designs 搜广推与 LLM 应用 ByteDance 2026-09-01 ReST 不直接照搬语言 Transformer：双门控注意力抑制行为噪声，RoPE 与相对时间编码同时表达顺序和时间间隔；系统侧把一次请求拆成可复用的重型用户 encoder 与轻型候选 cross decoder，实现 compute-once、decode-many。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现双门控时序编码、重用户编码/轻候选交叉的计算路径。未复刻私有行为日志、生产 checkpoint 和 shared-prefix serving kernel；本实现仅声明 CPU 公共数据核心机制，不宣传 CUDA 路径。在 MovieLens 100K 固定 220 用户/360 物品协议上执行时序衰减、信号门控与候选交叉路径；三 seed 结果见 metrics/public-seeds42-44.json。  ranking-network long-sequence shared-prefix-serving 搜广推 用户历史与排序骨干 ReST 的门控噪声抑制与只缩短历史，相比证据保留在哪里？ 截断删掉未保留事件，门控可在较广历史中降低噪声但保留潜在长期相关项，再由候选 decoder 取用。门控也可能误压关键事件，成本仍随输入处理增长。来源本地微负结果不支持门控天然优于任何近期基线。 示意：一年前摄影兴趣可保低但非零权重，误点新闻被压制；固定截断若全删旧史就无法再为相机候选取回这份偏好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b147c7ec89040e41">ReST 的门控噪声抑制与只缩短历史，相比证据保留在哪里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arest">From Language to Behavior: Scaling Sequence Transformers for Industrial Recommendation Ranking with Rec-Native Designs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>截断删掉未保留事件，门控可在较广历史中降低噪声但保留潜在长期相关项，再由候选 decoder 取用。门控也可能误压关键事件，成本仍随输入处理增长。来源本地微负结果不支持门控天然优于任何近期基线。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一年前摄影兴趣可保低但非零权重，误点新闻被压制；固定截断若全删旧史就无法再为相机候选取回这份偏好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.01240">原论文</a> · <a href="../../../../reproductions/2609.01240-rest/">实现解读</a> · <a href="#qa-b147c7ec89040e41">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rest" data-paper-title="From Language to Behavior: Scaling Sequence Transformers for Industrial Recommendation Ranking with Rec-Native Designs" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="From Language to Behavior: Scaling Sequence Transformers for Industrial Recommendation Ranking with Rec-Native Designs 搜广推与 LLM 应用 ByteDance 2026-09-01 ReST 不直接照搬语言 Transformer：双门控注意力抑制行为噪声，RoPE 与相对时间编码同时表达顺序和时间间隔；系统侧把一次请求拆成可复用的重型用户 encoder 与轻型候选 cross decoder，实现 compute-once、decode-many。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现双门控时序编码、重用户编码/轻候选交叉的计算路径。未复刻私有行为日志、生产 checkpoint 和 shared-prefix serving kernel；本实现仅声明 CPU 公共数据核心机制，不宣传 CUDA 路径。在 MovieLens 100K 固定 220 用户/360 物品协议上执行时序衰减、信号门控与候选交叉路径；三 seed 结果见 metrics/public-seeds42-44.json。  ranking-network long-sequence shared-prefix-serving 搜广推 用户历史与排序骨干 ReST 的重用户 encoder 缓存跨候选可复用，跨请求还要检查哪些依赖？ 同请求共享 hU 以历史和版本不变为前提，跨请求新增事件、时间差编码或模型更新可能使状态失效。候选 cross-decoder 输出仍专属，不应回写公共缓存。本地执行结构不代表已经测到生产 QPS 和完整 cache 更新系统。 示意：用户刚购买相机后再请求，旧历史摘要可能应更新；只因 user ID 一样就永久复用，会把已经完成需求继续当待满足兴趣。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-106636ac34f6a61f">ReST 的重用户 encoder 缓存跨候选可复用，跨请求还要检查哪些依赖？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arest">From Language to Behavior: Scaling Sequence Transformers for Industrial Recommendation Ranking with Rec-Native Designs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同请求共享 hU 以历史和版本不变为前提，跨请求新增事件、时间差编码或模型更新可能使状态失效。候选 cross-decoder 输出仍专属，不应回写公共缓存。本地执行结构不代表已经测到生产 QPS 和完整 cache 更新系统。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户刚购买相机后再请求，旧历史摘要可能应更新；只因 user ID 一样就永久复用，会把已经完成需求继续当待满足兴趣。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.01240">原论文</a> · <a href="../../../../reproductions/2609.01240-rest/">实现解读</a> · <a href="#qa-106636ac34f6a61f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onemodel" data-paper-title="OneModel: A Unified Foundation for Platform-Scale Multi-Scenario Ranking" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OneModel: A Unified Foundation for Platform-Scale Multi-Scenario Ranking 搜广推与 LLM 应用 Xiaohongshu 2026-08-19 推荐、广告和商家推荐通常各训一套排序模型，既重复消耗资源，也无法充分共享跨场景行为。OneModel 将异构特征先投影到统一 event token，再以共享 causal decoder 建模混合长历史；SAIM 用场景条件 gate 调制 FFN，分层表征同时保留全局 attentive pooling 与最近局部状态，从而兼顾迁移与专门化。 Fidelity: 核心机制复现。本地真实执行多场景统计、场景投影、SAIM 式门控和全局/局部分层表征；生产 Transformer 与私有特征未复刻。使用本地 MovieLens-1M 公开数据；没有小红书私有多流日志、action token、统一 Transformer decoder、训练早期梯度隔离、选择性反向传播和在线 serving。核心场景门控路径已执行，但本地指标只验证机制与失败边界。本地对照口径：基线为共享全局转移排序器；实验组加入由 MovieLens genre 派生的三个场景、场景转移、sigmoid 门控和 global/local 融合。  ranking multi-scenario foundation-model long-sequence 搜广推 用户历史与排序骨干 OneModel 为什么先把各场景异构字段映射成统一 event token？ 混合历史来自不同业务，字段结构和动作含义不一致，场景专属投影先建立共享维度，再附场景、动作、时间与位置，让因果主干能处理共同序列。统一维度不表示语义完全一致，场景 gate 和分层表征继续保留差异。 示意：观看十秒与购买一次不能只作为两个无标签 ID 拼接；event token 告诉主干它来自什么场景和动作，才有条件解释关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-onemodel-224b06a8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-623ba2ebeaea8822">OneModel 为什么先把各场景异构字段映射成统一 event token？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonemodel">OneModel: A Unified Foundation for Platform-Scale Multi-Scenario Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>混合历史来自不同业务，字段结构和动作含义不一致，场景专属投影先建立共享维度，再附场景、动作、时间与位置，让因果主干能处理共同序列。统一维度不表示语义完全一致，场景 gate 和分层表征继续保留差异。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>观看十秒与购买一次不能只作为两个无标签 ID 拼接；event token 告诉主干它来自什么场景和动作，才有条件解释关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.18606">原论文</a> · <a href="../../../../reproductions/2608.18606-onemodel/">实现解读</a> · <a href="#qa-623ba2ebeaea8822">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onemodel" data-paper-title="OneModel: A Unified Foundation for Platform-Scale Multi-Scenario Ranking" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OneModel: A Unified Foundation for Platform-Scale Multi-Scenario Ranking 搜广推与 LLM 应用 Xiaohongshu 2026-08-19 推荐、广告和商家推荐通常各训一套排序模型，既重复消耗资源，也无法充分共享跨场景行为。OneModel 将异构特征先投影到统一 event token，再以共享 causal decoder 建模混合长历史；SAIM 用场景条件 gate 调制 FFN，分层表征同时保留全局 attentive pooling 与最近局部状态，从而兼顾迁移与专门化。 Fidelity: 核心机制复现。本地真实执行多场景统计、场景投影、SAIM 式门控和全局/局部分层表征；生产 Transformer 与私有特征未复刻。使用本地 MovieLens-1M 公开数据；没有小红书私有多流日志、action token、统一 Transformer decoder、训练早期梯度隔离、选择性反向传播和在线 serving。核心场景门控路径已执行，但本地指标只验证机制与失败边界。本地对照口径：基线为共享全局转移排序器；实验组加入由 MovieLens genre 派生的三个场景、场景转移、sigmoid 门控和 global/local 融合。  ranking multi-scenario foundation-model long-sequence 搜广推 用户历史与排序骨干 OneModel 已共享因果主干，SAIM 的场景 gate 还保留了什么专门化能力？ 异构事件先投影到统一空间，使不同业务能共享历史建模；但完全共用 FFN 容易把场景差异压平。SAIM 依据场景嵌入调制共享 FFN 的激活，让同一中间表示在不同任务里使用不同通道。全局聚合与最近局部状态再分别保留稳定偏好和即时变化，避免统一表示只剩一种时间尺度。 示意：用户既看旅游内容也买旅行用品。共享主干能理解这些行为相关，但广告场景和内容推荐场景用不同门控组合特征，近期订机票的信号也可通过局部状态保留。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-56f6b3788fa8c230">OneModel 已共享因果主干，SAIM 的场景 gate 还保留了什么专门化能力？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonemodel">OneModel: A Unified Foundation for Platform-Scale Multi-Scenario Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>异构事件先投影到统一空间，使不同业务能共享历史建模；但完全共用 FFN 容易把场景差异压平。SAIM 依据场景嵌入调制共享 FFN 的激活，让同一中间表示在不同任务里使用不同通道。全局聚合与最近局部状态再分别保留稳定偏好和即时变化，避免统一表示只剩一种时间尺度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户既看旅游内容也买旅行用品。共享主干能理解这些行为相关，但广告场景和内容推荐场景用不同门控组合特征，近期订机票的信号也可通过局部状态保留。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.18606">原论文</a> · <a href="../../../../reproductions/2608.18606-onemodel/">实现解读</a> · <a href="#qa-56f6b3788fa8c230">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onemodel" data-paper-title="OneModel: A Unified Foundation for Platform-Scale Multi-Scenario Ranking" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OneModel: A Unified Foundation for Platform-Scale Multi-Scenario Ranking 搜广推与 LLM 应用 Xiaohongshu 2026-08-19 推荐、广告和商家推荐通常各训一套排序模型，既重复消耗资源，也无法充分共享跨场景行为。OneModel 将异构特征先投影到统一 event token，再以共享 causal decoder 建模混合长历史；SAIM 用场景条件 gate 调制 FFN，分层表征同时保留全局 attentive pooling 与最近局部状态，从而兼顾迁移与专门化。 Fidelity: 核心机制复现。本地真实执行多场景统计、场景投影、SAIM 式门控和全局/局部分层表征；生产 Transformer 与私有特征未复刻。使用本地 MovieLens-1M 公开数据；没有小红书私有多流日志、action token、统一 Transformer decoder、训练早期梯度隔离、选择性反向传播和在线 serving。核心场景门控路径已执行，但本地指标只验证机制与失败边界。本地对照口径：基线为共享全局转移排序器；实验组加入由 MovieLens genre 派生的三个场景、场景转移、sigmoid 门控和 global/local 融合。  ranking multi-scenario foundation-model long-sequence 搜广推 用户历史与排序骨干 OneModel 的 global/local 融合与一个 pooled 用户状态，相比保留哪些时间尺度？ 全局 attentive pooling 概括稳定模式，最近局部状态捕捉快速变化，融合避免一种时间尺度独占。单 pooled 状态更紧凑但可能平均掉新需求。人工 genre 场景会降低本地数据密度，来源退化不能用于否定真实跨业务，更不能隐去负号。 示意：长期旅游兴趣与刚开始装修可同时存在，global/local 让两者有不同位置；若全部均值，装修信号可能被多年旅游数量稀释。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a72433aecc431d2e">OneModel 的 global/local 融合与一个 pooled 用户状态，相比保留哪些时间尺度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonemodel">OneModel: A Unified Foundation for Platform-Scale Multi-Scenario Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全局 attentive pooling 概括稳定模式，最近局部状态捕捉快速变化，融合避免一种时间尺度独占。单 pooled 状态更紧凑但可能平均掉新需求。人工 genre 场景会降低本地数据密度，来源退化不能用于否定真实跨业务，更不能隐去负号。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>长期旅游兴趣与刚开始装修可同时存在，global/local 让两者有不同位置；若全部均值，装修信号可能被多年旅游数量稀释。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.18606">原论文</a> · <a href="../../../../reproductions/2608.18606-onemodel/">实现解读</a> · <a href="#qa-a72433aecc431d2e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onemodel" data-paper-title="OneModel: A Unified Foundation for Platform-Scale Multi-Scenario Ranking" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OneModel: A Unified Foundation for Platform-Scale Multi-Scenario Ranking 搜广推与 LLM 应用 Xiaohongshu 2026-08-19 推荐、广告和商家推荐通常各训一套排序模型，既重复消耗资源，也无法充分共享跨场景行为。OneModel 将异构特征先投影到统一 event token，再以共享 causal decoder 建模混合长历史；SAIM 用场景条件 gate 调制 FFN，分层表征同时保留全局 attentive pooling 与最近局部状态，从而兼顾迁移与专门化。 Fidelity: 核心机制复现。本地真实执行多场景统计、场景投影、SAIM 式门控和全局/局部分层表征；生产 Transformer 与私有特征未复刻。使用本地 MovieLens-1M 公开数据；没有小红书私有多流日志、action token、统一 Transformer decoder、训练早期梯度隔离、选择性反向传播和在线 serving。核心场景门控路径已执行，但本地指标只验证机制与失败边界。本地对照口径：基线为共享全局转移排序器；实验组加入由 MovieLens genre 派生的三个场景、场景转移、sigmoid 门控和 global/local 融合。  ranking multi-scenario foundation-model long-sequence 搜广推 用户历史与排序骨干 OneModel 的 SAIM gate 应由什么信息生成，为什么不能读取预测后业务标签？ gate 来自请求时已知场景嵌入并调制共享 FFN，任务标签只作监督，不能先看是否购买再决定场景门。event 序列也需因果 mask 和正确域投影。本地场景由 genre 派生，是公开代理而非真实推荐、广告、商家三套日志。 示意：知道当前是广告请求可选 gate，知道之后买了才选购买 gate 则泄漏；两者在字段名字上相近，实际可见时间完全不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-dbf522267491af2d">OneModel 的 SAIM gate 应由什么信息生成，为什么不能读取预测后业务标签？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonemodel">OneModel: A Unified Foundation for Platform-Scale Multi-Scenario Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>gate 来自请求时已知场景嵌入并调制共享 FFN，任务标签只作监督，不能先看是否购买再决定场景门。event 序列也需因果 mask 和正确域投影。本地场景由 genre 派生，是公开代理而非真实推荐、广告、商家三套日志。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>知道当前是广告请求可选 gate，知道之后买了才选购买 gate 则泄漏；两者在字段名字上相近，实际可见时间完全不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.18606">原论文</a> · <a href="../../../../reproductions/2608.18606-onemodel/">实现解读</a> · <a href="#qa-dbf522267491af2d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:genrec-netflix" data-paper-title="GenRec: An LLM-Backed Recommendation Ranker at Netflix" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="GenRec: An LLM-Backed Recommendation Ranker at Netflix 搜广推与 LLM 应用 Netflix 2026-08-10 传统 Netflix 排序系统依赖大量人工特征、特征交互和场景专用网络。新增内容形态或推荐场景时，往往要重新设计特征、模型和基础设施。GenRec 把问题从“特征工程”转成“上下文工程”：把用户历史、内容元数据、设备和时间等信号表达成文本，让共享 LLM 主干学习语义与高阶交互。论文采用两阶段训练：Phase 1 在开源 LLM 上继续训练 Netflix 内容和用户数据，获得内部 foundation LLM； Fidelity：核心机制复现。本地真实加载 causal LLM、执行 LoRA Phase-2 后训练、文本化用户历史、全目录 catalog-aware ranking head、联合语言/排序目标和 reward-weighted loss；Netflix 私有 Phase-1 基座与线上 reward model 不可公开，未用固定规则冒充。Netflix 内部 Phase-1 foundation LLM、数千生产特征和数千亿交互事件不可获得；本地使用公开 SmolLM2 和 MovieLens 文本/反馈。  ranking llm-recommendation post-training reward-weighting context-engineering training-serving 搜广推 用户历史与排序骨干 Netflix GenRec 的 catalog-aware head 为什么能避免目录外物品幻觉？ 模型不是自由生成名字，而是从一次 prefill 的 pooled 状态对固定目录 item 评分，输出身份受目录头限制。文本化上下文提供丰富特征，语言目标维持理解能力。目录内合法仍不保证相关或可服务，库存等约束与模型外映射也需一致。 示意：即使语言模型知道未上架电影，目录头没有对应输出列就不会直接推荐它；相反，目录中的无关影片仍可能被误排高，需要相关性学习。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-genrec-netflix-691b65fa" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-443e09eaf7bff5ef">Netflix GenRec 的 catalog-aware head 为什么能避免目录外物品幻觉？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agenrec-netflix">GenRec: An LLM-Backed Recommendation Ranker at Netflix</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Netflix</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>模型不是自由生成名字，而是从一次 prefill 的 pooled 状态对固定目录 item 评分，输出身份受目录头限制。文本化上下文提供丰富特征，语言目标维持理解能力。目录内合法仍不保证相关或可服务，库存等约束与模型外映射也需一致。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>即使语言模型知道未上架电影，目录头没有对应输出列就不会直接推荐它；相反，目录中的无关影片仍可能被误排高，需要相关性学习。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.10257">原论文</a> · <a href="../../../../reproductions/2608.10257-genrec-netflix/">实现解读</a> · <a href="#qa-443e09eaf7bff5ef">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:genrec-netflix" data-paper-title="GenRec: An LLM-Backed Recommendation Ranker at Netflix" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="GenRec: An LLM-Backed Recommendation Ranker at Netflix 搜广推与 LLM 应用 Netflix 2026-08-10 传统 Netflix 排序系统依赖大量人工特征、特征交互和场景专用网络。新增内容形态或推荐场景时，往往要重新设计特征、模型和基础设施。GenRec 把问题从“特征工程”转成“上下文工程”：把用户历史、内容元数据、设备和时间等信号表达成文本，让共享 LLM 主干学习语义与高阶交互。论文采用两阶段训练：Phase 1 在开源 LLM 上继续训练 Netflix 内容和用户数据，获得内部 foundation LLM； Fidelity：核心机制复现。本地真实加载 causal LLM、执行 LoRA Phase-2 后训练、文本化用户历史、全目录 catalog-aware ranking head、联合语言/排序目标和 reward-weighted loss；Netflix 私有 Phase-1 基座与线上 reward model 不可公开，未用固定规则冒充。Netflix 内部 Phase-1 foundation LLM、数千生产特征和数千亿交互事件不可获得；本地使用公开 SmolLM2 和 MovieLens 文本/反馈。  ranking llm-recommendation post-training reward-weighting context-engineering training-serving 搜广推 用户历史与排序骨干 Netflix GenRec使用decoder-only LLM，为什么线上却不逐token生成推荐清单？ 文本上下文经LLM前向得到用户表示后，catalog-aware head直接对目录物品评分，服务可以只做prefill，不必自回归写出商品名。这样既利用语义与高阶交互，又避免目录外生成和多步解码成本。联合语言目标服务表示学习，并不改变最终是目录排序；本地单种子路径不证明Netflix规模收益。 示意：模型读完用户历史和场景后，一次输出目录里每部电影的分数；它无需先写第一部片名，再把片名回填生成第二部，因此不会凭空推荐目录外作品。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-7c9e2f93989e3d7b">Netflix GenRec使用decoder-only LLM，为什么线上却不逐token生成推荐清单？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agenrec-netflix">GenRec: An LLM-Backed Recommendation Ranker at Netflix</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Netflix</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文本上下文经LLM前向得到用户表示后，catalog-aware head直接对目录物品评分，服务可以只做prefill，不必自回归写出商品名。这样既利用语义与高阶交互，又避免目录外生成和多步解码成本。联合语言目标服务表示学习，并不改变最终是目录排序；本地单种子路径不证明Netflix规模收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型读完用户历史和场景后，一次输出目录里每部电影的分数；它无需先写第一部片名，再把片名回填生成第二部，因此不会凭空推荐目录外作品。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.10257">原论文</a> · <a href="../../../../reproductions/2608.10257-genrec-netflix/">实现解读</a> · <a href="#qa-7c9e2f93989e3d7b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:genrec-netflix" data-paper-title="GenRec: An LLM-Backed Recommendation Ranker at Netflix" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="GenRec: An LLM-Backed Recommendation Ranker at Netflix 搜广推与 LLM 应用 Netflix 2026-08-10 传统 Netflix 排序系统依赖大量人工特征、特征交互和场景专用网络。新增内容形态或推荐场景时，往往要重新设计特征、模型和基础设施。GenRec 把问题从“特征工程”转成“上下文工程”：把用户历史、内容元数据、设备和时间等信号表达成文本，让共享 LLM 主干学习语义与高阶交互。论文采用两阶段训练：Phase 1 在开源 LLM 上继续训练 Netflix 内容和用户数据，获得内部 foundation LLM； Fidelity：核心机制复现。本地真实加载 causal LLM、执行 LoRA Phase-2 后训练、文本化用户历史、全目录 catalog-aware ranking head、联合语言/排序目标和 reward-weighted loss；Netflix 私有 Phase-1 基座与线上 reward model 不可公开，未用固定规则冒充。Netflix 内部 Phase-1 foundation LLM、数千生产特征和数千亿交互事件不可获得；本地使用公开 SmolLM2 和 MovieLens 文本/反馈。  ranking llm-recommendation post-training reward-weighting context-engineering training-serving 搜广推 用户历史与排序骨干 Netflix GenRec 的 reward-weighted ranking 与对生成列表做在线 RL，训练对象有何不同？ 此处多 reward 汇总为样本权重，调整目录排名损失的贡献，同时联合语言目标；不是逐 token rollout 后给整张列表策略梯度。服务也只 prefill 评分。两种方法可以都用奖励一词，却有不同概率空间与计算路径，不能混称。 示意：满意度高样本在分类损失里权重大，不表示模型在线生成十条清单再做 PPO；一边是加权监督，一边是另一类策略更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-da9c9def46906001">Netflix GenRec 的 reward-weighted ranking 与对生成列表做在线 RL，训练对象有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agenrec-netflix">GenRec: An LLM-Backed Recommendation Ranker at Netflix</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Netflix</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>此处多 reward 汇总为样本权重，调整目录排名损失的贡献，同时联合语言目标；不是逐 token rollout 后给整张列表策略梯度。服务也只 prefill 评分。两种方法可以都用奖励一词，却有不同概率空间与计算路径，不能混称。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>满意度高样本在分类损失里权重大，不表示模型在线生成十条清单再做 PPO；一边是加权监督，一边是另一类策略更新。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.10257">原论文</a> · <a href="../../../../reproductions/2608.10257-genrec-netflix/">实现解读</a> · <a href="#qa-da9c9def46906001">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:genrec-netflix" data-paper-title="GenRec: An LLM-Backed Recommendation Ranker at Netflix" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="GenRec: An LLM-Backed Recommendation Ranker at Netflix 搜广推与 LLM 应用 Netflix 2026-08-10 传统 Netflix 排序系统依赖大量人工特征、特征交互和场景专用网络。新增内容形态或推荐场景时，往往要重新设计特征、模型和基础设施。GenRec 把问题从“特征工程”转成“上下文工程”：把用户历史、内容元数据、设备和时间等信号表达成文本，让共享 LLM 主干学习语义与高阶交互。论文采用两阶段训练：Phase 1 在开源 LLM 上继续训练 Netflix 内容和用户数据，获得内部 foundation LLM； Fidelity：核心机制复现。本地真实加载 causal LLM、执行 LoRA Phase-2 后训练、文本化用户历史、全目录 catalog-aware ranking head、联合语言/排序目标和 reward-weighted loss；Netflix 私有 Phase-1 基座与线上 reward model 不可公开，未用固定规则冒充。Netflix 内部 Phase-1 foundation LLM、数千生产特征和数千亿交互事件不可获得；本地使用公开 SmolLM2 和 MovieLens 文本/反馈。  ranking llm-recommendation post-training reward-weighting context-engineering training-serving 搜广推 用户历史与排序骨干 Netflix GenRec 本地对 GRU 的比较为什么不能解释为同参数量架构消融？ 实验组真实加载更大的公开 causal LLM 并训练 LoRA，基线是 ID-only GRU，参数与语义输入都不同；它比较两条机制路径，而非只换一个算子。单 seed、缩小目录与公开奖励代理限制稳定性，不能直接与原文线上百分比横比。 示意：LLM 多了标题语义和大量预训参数，优于小 GRU 时不能把全部差值归给 catalog head；需另做匹配对照才可隔离该组件贡献。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6926175c877ccaf4">Netflix GenRec 本地对 GRU 的比较为什么不能解释为同参数量架构消融？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agenrec-netflix">GenRec: An LLM-Backed Recommendation Ranker at Netflix</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Netflix</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>实验组真实加载更大的公开 causal LLM 并训练 LoRA，基线是 ID-only GRU，参数与语义输入都不同；它比较两条机制路径，而非只换一个算子。单 seed、缩小目录与公开奖励代理限制稳定性，不能直接与原文线上百分比横比。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>LLM 多了标题语义和大量预训参数，优于小 GRU 时不能把全部差值归给 catalog head；需另做匹配对照才可隔离该组件贡献。</p>
<p class="ar-learning-sources">依据：本地复现、对照口径；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.10257">原论文</a> · <a href="../../../../reproductions/2608.10257-genrec-netflix/">实现解读</a> · <a href="#qa-6926175c877ccaf4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:inthq" data-paper-title="IntHQ: Task-Interactive Hierarchical Query on Dual-Stream Representations for Generative Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="IntHQ: Task-Interactive Hierarchical Query on Dual-Stream Representations for Generative Recommendation 搜广推与 LLM 应用 Amap / Alibaba 2026-08-10 双流分别保留行为与上下文表示，when/where/how/via 四个任务查询在多个层级交互检索，使任务信号进入编码器而非只留在任务头。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  multi-task-learning generative-recommendation long-sequence 搜广推 用户历史与排序骨干 IntHQ 的 when、where、how、via 为什么是查询角色，而不只是四个标签？ 查询引导模型从行为和上下文流中抽取不同证据，使任务需求影响中间表示，不只在末端各预测一个结果。双流保留来源差异，多层交互再联系时间、地点、方式和渠道。名称提供语义假设，是否真正分工仍需检查。 示意：何时回访更关注间隔，去哪里更关注地点历史；若两者只接同一固定向量，早期编码无法按这两种问题分别取证。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-inthq-fbf3d84e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ec8aa37e3eb59e97">IntHQ 的 when、where、how、via 为什么是查询角色，而不只是四个标签？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ainthq">IntHQ: Task-Interactive Hierarchical Query on Dual-Stream Representations for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Amap / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>查询引导模型从行为和上下文流中抽取不同证据，使任务需求影响中间表示，不只在末端各预测一个结果。双流保留来源差异，多层交互再联系时间、地点、方式和渠道。名称提供语义假设，是否真正分工仍需检查。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>何时回访更关注间隔，去哪里更关注地点历史；若两者只接同一固定向量，早期编码无法按这两种问题分别取证。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.09634">原论文</a> · <a href="../../../../reproductions/2608.09634-inthq/">实现解读</a> · <a href="#qa-ec8aa37e3eb59e97">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:inthq" data-paper-title="IntHQ: Task-Interactive Hierarchical Query on Dual-Stream Representations for Generative Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="IntHQ: Task-Interactive Hierarchical Query on Dual-Stream Representations for Generative Recommendation 搜广推与 LLM 应用 Amap / Alibaba 2026-08-10 双流分别保留行为与上下文表示，when/where/how/via 四个任务查询在多个层级交互检索，使任务信号进入编码器而非只留在任务头。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  multi-task-learning generative-recommendation long-sequence 搜广推 用户历史与排序骨干 IntHQ让when、where、how、via查询进入多层编码，而不只加四个输出头，有何作用？ 仅在末端分头预测，早期编码仍可能按同一种方式压缩所有信息。任务查询在不同层级读取行为与上下文双流，让任务需求参与选择证据，例如时间问题关注周期、渠道问题关注入口。共享底层仍可保留共性，但这种互动不意味着任务冲突自动消失，需要检查各查询是否产生真实分工。 示意：同一条午间搜索记录，时间查询关心午休周期，渠道查询关心搜索入口；让两种问题在编码中取证，比最后对同一摘要各接一层分类头更灵活。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-787bc07ff99b39ff">IntHQ让when、where、how、via查询进入多层编码，而不只加四个输出头，有何作用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ainthq">IntHQ: Task-Interactive Hierarchical Query on Dual-Stream Representations for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Amap / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>仅在末端分头预测，早期编码仍可能按同一种方式压缩所有信息。任务查询在不同层级读取行为与上下文双流，让任务需求参与选择证据，例如时间问题关注周期、渠道问题关注入口。共享底层仍可保留共性，但这种互动不意味着任务冲突自动消失，需要检查各查询是否产生真实分工。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一条午间搜索记录，时间查询关心午休周期，渠道查询关心搜索入口；让两种问题在编码中取证，比最后对同一摘要各接一层分类头更灵活。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.09634">原论文</a> · <a href="../../../../reproductions/2608.09634-inthq/">实现解读</a> · <a href="#qa-787bc07ff99b39ff">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:inthq" data-paper-title="IntHQ: Task-Interactive Hierarchical Query on Dual-Stream Representations for Generative Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="IntHQ: Task-Interactive Hierarchical Query on Dual-Stream Representations for Generative Recommendation 搜广推与 LLM 应用 Amap / Alibaba 2026-08-10 双流分别保留行为与上下文表示，when/where/how/via 四个任务查询在多个层级交互检索，使任务信号进入编码器而非只留在任务头。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  multi-task-learning generative-recommendation long-sequence 搜广推 用户历史与排序骨干 IntHQ 的双流交互与把行为上下文一次拼接，相比保留什么结构？ 双流先区分事件与上下文，再由任务查询跨层读取，避免所有字段从一开始无差别混合。一次拼接更简单却较难显式追踪来源和任务条件。结构更强不保证效果，来源本地公开代理退化，不能用查询名字代替任务评估。 示意：工作日午间是上下文，最近餐饮点击是行为；双流可分别编码后回答“何时、何处”，而不必让二者同等作用于所有目标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7d208b2271a6edac">IntHQ 的双流交互与把行为上下文一次拼接，相比保留什么结构？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ainthq">IntHQ: Task-Interactive Hierarchical Query on Dual-Stream Representations for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Amap / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>双流先区分事件与上下文，再由任务查询跨层读取，避免所有字段从一开始无差别混合。一次拼接更简单却较难显式追踪来源和任务条件。结构更强不保证效果，来源本地公开代理退化，不能用查询名字代替任务评估。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>工作日午间是上下文，最近餐饮点击是行为；双流可分别编码后回答“何时、何处”，而不必让二者同等作用于所有目标。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.09634">原论文</a> · <a href="../../../../reproductions/2608.09634-inthq/">实现解读</a> · <a href="#qa-7d208b2271a6edac">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:inthq" data-paper-title="IntHQ: Task-Interactive Hierarchical Query on Dual-Stream Representations for Generative Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="IntHQ: Task-Interactive Hierarchical Query on Dual-Stream Representations for Generative Recommendation 搜广推与 LLM 应用 Amap / Alibaba 2026-08-10 双流分别保留行为与上下文表示，when/where/how/via 四个任务查询在多个层级交互检索，使任务信号进入编码器而非只留在任务头。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  multi-task-learning generative-recommendation long-sequence 搜广推 用户历史与排序骨干 IntHQ 多层查询聚合时，为什么任务轴与历史轴不能混用？ 每个任务 query 应对相应流或层级的 K/V 读取，再形成该任务状态，softmax 轴需按实际候选证据定义。将四个任务一起当历史归一，会变成任务彼此竞争。输入输出角色一致比末维相同更重要，公开代理也不覆盖全部真实时空任务。 示意：when query 的权重应在历史时点间分配，不能与 where query 的权重一起总和为一，否则位置任务出现会改变时间任务的证据预算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-4176beff76081d52">IntHQ 多层查询聚合时，为什么任务轴与历史轴不能混用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ainthq">IntHQ: Task-Interactive Hierarchical Query on Dual-Stream Representations for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Amap / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每个任务 query 应对相应流或层级的 K/V 读取，再形成该任务状态，softmax 轴需按实际候选证据定义。将四个任务一起当历史归一，会变成任务彼此竞争。输入输出角色一致比末维相同更重要，公开代理也不覆盖全部真实时空任务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>when query 的权重应在历史时点间分配，不能与 where query 的权重一起总和为一，否则位置任务出现会改变时间任务的证据预算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.09634">原论文</a> · <a href="../../../../reproductions/2608.09634-inthq/">实现解读</a> · <a href="#qa-4176beff76081d52">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tm20k" data-paper-title="Teacher Retains Full Tokens, Student Merges Efficiently: TM20K for E-Commerce Sequence Modeling in Ad Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Teacher Retains Full Tokens, Student Merges Efficiently: TM20K for E-Commerce Sequence Modeling in Ad Recommendation 搜广推与 LLM 应用 ByteDance 2026-08-07 教师网络保留完整行为 token 提供细粒度监督，学生把连续行为按组以 sum/√n 合并到固定 token 预算，再蒸馏教师注意力与排序分布，兼顾长序列信息和线上成本。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为无蒸馏的合并 token student，实验组从 full-token teacher 蒸馏；seed 42 的 NDCG@10 为 0.04022，基线为 0.03446。  advertising long-sequence token-merging distillation 搜广推 用户历史与排序骨干 TM20K为什么教师保留全token而学生合并？ 完整教师提供细粒度注意与排序监督，学生用有限token预算控制线上长历史成本。压缩与蒸馏配合，不意味着合并表示天然保留所有细节。 例如老师读完整两万行为，学生读分组摘要并学习老师关注点。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-tm20k-e967dab7" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-016bcc070aa74faf">TM20K为什么教师保留全token而学生合并？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atm20k">Teacher Retains Full Tokens, Student Merges Efficiently: TM20K for E-Commerce Sequence Modeling in Ad Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>完整教师提供细粒度注意与排序监督，学生用有限token预算控制线上长历史成本。压缩与蒸馏配合，不意味着合并表示天然保留所有细节。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如老师读完整两万行为，学生读分组摘要并学习老师关注点。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.07055">原论文</a> · <a href="../../../../reproductions/2608.07055-tm20k/">实现解读</a> · <a href="#qa-016bcc070aa74faf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tm20k" data-paper-title="Teacher Retains Full Tokens, Student Merges Efficiently: TM20K for E-Commerce Sequence Modeling in Ad Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Teacher Retains Full Tokens, Student Merges Efficiently: TM20K for E-Commerce Sequence Modeling in Ad Recommendation 搜广推与 LLM 应用 ByteDance 2026-08-07 教师网络保留完整行为 token 提供细粒度监督，学生把连续行为按组以 sum/√n 合并到固定 token 预算，再蒸馏教师注意力与排序分布，兼顾长序列信息和线上成本。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为无蒸馏的合并 token student，实验组从 full-token teacher 蒸馏；seed 42 的 NDCG@10 为 0.04022，基线为 0.03446。  advertising long-sequence token-merging distillation 搜广推 用户历史与排序骨干 TM20K 为什么把一组行为按 sum/√n 合并，并蒸馏完整 token teacher？ 分组合并把序列压到固定 token 预算，除以组大小平方根可缓和求和随组长增长的尺度变化，相较均值保留另一种组规模信息。完整教师仍能看到细粒度行为，注意力与排序蒸馏帮助压缩学生补回仅靠聚合易丢的关系。聚合不可逆，蒸馏只能学习有用近似，不能保证还原组内每次行为。 示意：四次相关浏览合为一个 token，按平方根缩放避免数值随组长直接翻倍。教师能区分四次内部关系，再把软信号传给压缩学生，但学生不再拥有原始四个位置。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-74a2478da4c70ed5">TM20K 为什么把一组行为按 sum/√n 合并，并蒸馏完整 token teacher？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atm20k">Teacher Retains Full Tokens, Student Merges Efficiently: TM20K for E-Commerce Sequence Modeling in Ad Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分组合并把序列压到固定 token 预算，除以组大小平方根可缓和求和随组长增长的尺度变化，相较均值保留另一种组规模信息。完整教师仍能看到细粒度行为，注意力与排序蒸馏帮助压缩学生补回仅靠聚合易丢的关系。聚合不可逆，蒸馏只能学习有用近似，不能保证还原组内每次行为。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>四次相关浏览合为一个 token，按平方根缩放避免数值随组长直接翻倍。教师能区分四次内部关系，再把软信号传给压缩学生，但学生不再拥有原始四个位置。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.07055">原论文</a> · <a href="../../../../reproductions/2608.07055-tm20k/">实现解读</a> · <a href="#qa-74a2478da4c70ed5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tm20k" data-paper-title="Teacher Retains Full Tokens, Student Merges Efficiently: TM20K for E-Commerce Sequence Modeling in Ad Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Teacher Retains Full Tokens, Student Merges Efficiently: TM20K for E-Commerce Sequence Modeling in Ad Recommendation 搜广推与 LLM 应用 ByteDance 2026-08-07 教师网络保留完整行为 token 提供细粒度监督，学生把连续行为按组以 sum/√n 合并到固定 token 预算，再蒸馏教师注意力与排序分布，兼顾长序列信息和线上成本。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为无蒸馏的合并 token student，实验组从 full-token teacher 蒸馏；seed 42 的 NDCG@10 为 0.04022，基线为 0.03446。  advertising long-sequence token-merging distillation 搜广推 用户历史与排序骨干 sum除√n与均值池化的尺度有什么不同？ 均值除n，√n归一保留不同组大小下另一种能量尺度，尤其行为特征相关性影响幅度。两者不能随手替换后仍声称原合并规则相同。 例如同样向量重复多次，两种归一得到的表示范数增长不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4fc9b1e5b55bbd3a">sum除√n与均值池化的尺度有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atm20k">Teacher Retains Full Tokens, Student Merges Efficiently: TM20K for E-Commerce Sequence Modeling in Ad Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>均值除n，√n归一保留不同组大小下另一种能量尺度，尤其行为特征相关性影响幅度。两者不能随手替换后仍声称原合并规则相同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同样向量重复多次，两种归一得到的表示范数增长不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.07055">原论文</a> · <a href="../../../../reproductions/2608.07055-tm20k/">实现解读</a> · <a href="#qa-4fc9b1e5b55bbd3a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tm20k" data-paper-title="Teacher Retains Full Tokens, Student Merges Efficiently: TM20K for E-Commerce Sequence Modeling in Ad Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Teacher Retains Full Tokens, Student Merges Efficiently: TM20K for E-Commerce Sequence Modeling in Ad Recommendation 搜广推与 LLM 应用 ByteDance 2026-08-07 教师网络保留完整行为 token 提供细粒度监督，学生把连续行为按组以 sum/√n 合并到固定 token 预算，再蒸馏教师注意力与排序分布，兼顾长序列信息和线上成本。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为无蒸馏的合并 token student，实验组从 full-token teacher 蒸馏；seed 42 的 NDCG@10 为 0.04022，基线为 0.03446。  advertising long-sequence token-merging distillation 搜广推 用户历史与排序骨干 TM20K注意力蒸馏如何处理师生不同长度？ 需明确教师细粒度到学生分组位置的映射，不能直接相减不同形状矩阵；mask与组大小保持。当前公开代理未复刻生产长历史、模型和线上流量。 例如四个原事件合成一槽，要先说明对应哪些教师注意项。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-78f74f3d70d3c699">TM20K注意力蒸馏如何处理师生不同长度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atm20k">Teacher Retains Full Tokens, Student Merges Efficiently: TM20K for E-Commerce Sequence Modeling in Ad Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>需明确教师细粒度到学生分组位置的映射，不能直接相减不同形状矩阵；mask与组大小保持。当前公开代理未复刻生产长历史、模型和线上流量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如四个原事件合成一槽，要先说明对应哪些教师注意项。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.07055">原论文</a> · <a href="../../../../reproductions/2608.07055-tm20k/">实现解读</a> · <a href="#qa-78f74f3d70d3c699">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:transx" data-paper-title="TransX: Scaling Transformer-based Recommendation via Behavioral and Serving Stream Crossings" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TransX: Scaling Transformer-based Recommendation via Behavioral and Serving Stream Crossings 搜广推与 LLM 应用 LinkedIn 2026-07-31 将可离线缓存的长行为流与请求时产生的短服务流解耦；行为端形成 global/local 缓存，候选端只对缓存做 cross-attention，从而避免每个请求重算完整 self-attention。 成本过高，不复现（审查 DONE）：报告的 32 H200、约 13 小时收敛、生产 Kafka/KV/多租户服务和完整多基准实验不在本批预算内。它们是公式/梯度诊断，不是新的推荐得分；历史 adapter：concept demo。model.py 的 NumPy 路径使用固定权重与既有特征，没有训练论文网络；历史结果原样保留，但不再标成核心模型训练或正式能力比较。下文另列本次技术报告的真实可微组件及独立验收证据。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；  ranking long-sequence cross-attention serving 搜广推 用户历史与排序骨干 TransX为什么拆行为流与请求服务流？ 长行为可离线形成global/local缓存，请求侧短候选只cross-attend缓存，避免每候选重算长self-attention。缓存适合共享部分，不能把候选依赖状态随意缓存。 例如同一用户多个候选读取一份历史状态，但仍各自做匹配。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-transx-58683026" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ef59c1c3050aa984">TransX为什么拆行为流与请求服务流？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atransx">TransX: Scaling Transformer-based Recommendation via Behavioral and Serving Stream Crossings</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长行为可离线形成global/local缓存，请求侧短候选只cross-attend缓存，避免每候选重算长self-attention。缓存适合共享部分，不能把候选依赖状态随意缓存。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一用户多个候选读取一份历史状态，但仍各自做匹配。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28940">原论文</a> · <a href="../../../../reproductions/2607.28940-transx/">实现解读</a> · <a href="#qa-ef59c1c3050aa984">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:transx" data-paper-title="TransX: Scaling Transformer-based Recommendation via Behavioral and Serving Stream Crossings" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TransX: Scaling Transformer-based Recommendation via Behavioral and Serving Stream Crossings 搜广推与 LLM 应用 LinkedIn 2026-07-31 将可离线缓存的长行为流与请求时产生的短服务流解耦；行为端形成 global/local 缓存，候选端只对缓存做 cross-attention，从而避免每个请求重算完整 self-attention。 成本过高，不复现（审查 DONE）：报告的 32 H200、约 13 小时收敛、生产 Kafka/KV/多租户服务和完整多基准实验不在本批预算内。它们是公式/梯度诊断，不是新的推荐得分；历史 adapter：concept demo。model.py 的 NumPy 路径使用固定权重与既有特征，没有训练论文网络；历史结果原样保留，但不再标成核心模型训练或正式能力比较。下文另列本次技术报告的真实可微组件及独立验收证据。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；  ranking long-sequence cross-attention serving 搜广推 用户历史与排序骨干 TransX 为什么把行为流缓存为 global/local 两种状态，而让短服务流只做 cross-attention？ 长行为流在多个请求间变化较慢，离线或异步形成缓存能摊销自注意力成本；global 保存整体偏好，local 保留近期细节，服务流再用当前候选查询它们。每次请求省掉的是重复行为编码，缓存构建与更新仍有成本，也必须避免把候选相关状态误缓存成公共用户信息。 示意：用户一天内多次打开推荐，长期兴趣缓存可复用，局部缓存随新行为刷新。某次候选只读取需要的片段，不必为了这一件商品把整段多年历史重新自注意力一次。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f63260b88299146b">TransX 为什么把行为流缓存为 global/local 两种状态，而让短服务流只做 cross-attention？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atransx">TransX: Scaling Transformer-based Recommendation via Behavioral and Serving Stream Crossings</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长行为流在多个请求间变化较慢，离线或异步形成缓存能摊销自注意力成本；global 保存整体偏好，local 保留近期细节，服务流再用当前候选查询它们。每次请求省掉的是重复行为编码，缓存构建与更新仍有成本，也必须避免把候选相关状态误缓存成公共用户信息。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户一天内多次打开推荐，长期兴趣缓存可复用，局部缓存随新行为刷新。某次候选只读取需要的片段，不必为了这一件商品把整段多年历史重新自注意力一次。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28940">原论文</a> · <a href="../../../../reproductions/2607.28940-transx/">实现解读</a> · <a href="#qa-f63260b88299146b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:transx" data-paper-title="TransX: Scaling Transformer-based Recommendation via Behavioral and Serving Stream Crossings" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TransX: Scaling Transformer-based Recommendation via Behavioral and Serving Stream Crossings 搜广推与 LLM 应用 LinkedIn 2026-07-31 将可离线缓存的长行为流与请求时产生的短服务流解耦；行为端形成 global/local 缓存，候选端只对缓存做 cross-attention，从而避免每个请求重算完整 self-attention。 成本过高，不复现（审查 DONE）：报告的 32 H200、约 13 小时收敛、生产 Kafka/KV/多租户服务和完整多基准实验不在本批预算内。它们是公式/梯度诊断，不是新的推荐得分；历史 adapter：concept demo。model.py 的 NumPy 路径使用固定权重与既有特征，没有训练论文网络；历史结果原样保留，但不再标成核心模型训练或正式能力比较。下文另列本次技术报告的真实可微组件及独立验收证据。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；  ranking long-sequence cross-attention serving 搜广推 用户历史与排序骨干 补充报告的共享多cutoff与普通独立池化怎样比较？ 用可合并softmax统计复用前缀，前向和梯度应与独立计算等价；这是公式复用，不是不同推荐得分。报告Base、Retrieval、Ranking还是不同生产实验，不能跨表排胜负。 例如共享计算节省重复工作，不应改变同一输入下池化结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-89587d43acc170b5">补充报告的共享多cutoff与普通独立池化怎样比较？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atransx">TransX: Scaling Transformer-based Recommendation via Behavioral and Serving Stream Crossings</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用可合并softmax统计复用前缀，前向和梯度应与独立计算等价；这是公式复用，不是不同推荐得分。报告Base、Retrieval、Ranking还是不同生产实验，不能跨表排胜负。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如共享计算节省重复工作，不应改变同一输入下池化结果。</p>
<p class="ar-learning-sources">依据：补充核心公式、补充报告效果与本地验收；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28940">原论文</a> · <a href="../../../../reproductions/2607.28940-transx/">实现解读</a> · <a href="#qa-89587d43acc170b5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:transx" data-paper-title="TransX: Scaling Transformer-based Recommendation via Behavioral and Serving Stream Crossings" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TransX: Scaling Transformer-based Recommendation via Behavioral and Serving Stream Crossings 搜广推与 LLM 应用 LinkedIn 2026-07-31 将可离线缓存的长行为流与请求时产生的短服务流解耦；行为端形成 global/local 缓存，候选端只对缓存做 cross-attention，从而避免每个请求重算完整 self-attention。 成本过高，不复现（审查 DONE）：报告的 32 H200、约 13 小时收敛、生产 Kafka/KV/多租户服务和完整多基准实验不在本批预算内。它们是公式/梯度诊断，不是新的推荐得分；历史 adapter：concept demo。model.py 的 NumPy 路径使用固定权重与既有特征，没有训练论文网络；历史结果原样保留，但不再标成核心模型训练或正式能力比较。下文另列本次技术报告的真实可微组件及独立验收证据。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；  ranking long-sequence cross-attention serving 搜广推 用户历史与排序骨干 TransX补充稀疏行更新为何先聚合重复行再平方？ 平方非线性，逐microbatch先平方后加不同于逻辑步总梯度平方。当前A100小张量验证了该边界，未实现32H200生产系统，也未提升旧adapter保真标签。 例如同一行两次相反梯度应先抵消，先平方会错误累积大统计。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-78624c18f023b1ae">TransX补充稀疏行更新为何先聚合重复行再平方？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atransx">TransX: Scaling Transformer-based Recommendation via Behavioral and Serving Stream Crossings</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>平方非线性，逐microbatch先平方后加不同于逻辑步总梯度平方。当前A100小张量验证了该边界，未实现32H200生产系统，也未提升旧adapter保真标签。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一行两次相反梯度应先抵消，先平方会错误累积大统计。</p>
<p class="ar-learning-sources">依据：补充核心公式、补充报告效果与本地验收；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28940">原论文</a> · <a href="../../../../reproductions/2607.28940-transx/">实现解读</a> · <a href="#qa-78624c18f023b1ae">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ccformer" data-paper-title="CCFormer: Efficient Cross-Field Interaction and Hierarchical Sequence Compression for Industrial Recommendation at Tencent" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="CCFormer: Efficient Cross-Field Interaction and Hierarchical Sequence Compression for Industrial Recommendation at Tencent 搜广推与 LLM 应用 Tencent Platform and Content Group 2026-07-30 工业排序既要细粒度字段交互，又要吃进千长度行为序列。CCFormer 让 ID、内容等字段先分离投影再 cross attention，并用逐层扩大感受野的 token mixing 压缩旧历史，近期行为保持细粒度。 Fidelity: 核心机制复现。实现跨字段门控、分层旧序列压缩和 recent-token 保留；不复刻腾讯私有数据与 kernel。未包含 40 亿私有样本、千长度线上序列、并行多 target kernel；本地结果只验证机制方向。本地对照口径：基线为同预算 GRU；实验组为 CCFormer core，相对基线 NDCG@10 +22.44%。  ranking long-sequence sequence-compression token-mixing 搜广推 用户历史与排序骨干 CCFormer 为什么将字段分离投影，而不把 ID、内容和长历史直接视作同质 token？ 不同字段来源和统计尺度不同，分离投影提供各自的表示入口，再通过 cross-attention 建立关系，避免强字段主导统一空间。长历史另用分层压缩控制成本，因此特征交互与序列长度被共同考虑，不能把它简化为仅增加 Transformer 层数。 示意：用户 ID 是稀疏记忆，内容向量是语义，相同投影可能偏向常见 ID；分开变换后再交互，才更容易保留两类信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-ccformer-b04b720c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9e54784b884cf046">CCFormer 为什么将字段分离投影，而不把 ID、内容和长历史直接视作同质 token？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Accformer">CCFormer: Efficient Cross-Field Interaction and Hierarchical Sequence Compression for Industrial Recommendation at Tencent</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent Platform and Content Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同字段来源和统计尺度不同，分离投影提供各自的表示入口，再通过 cross-attention 建立关系，避免强字段主导统一空间。长历史另用分层压缩控制成本，因此特征交互与序列长度被共同考虑，不能把它简化为仅增加 Transformer 层数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户 ID 是稀疏记忆，内容向量是语义，相同投影可能偏向常见 ID；分开变换后再交互，才更容易保留两类信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28070">原论文</a> · <a href="../../../../reproductions/2607.28070-ccformer/">实现解读</a> · <a href="#qa-9e54784b884cf046">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ccformer" data-paper-title="CCFormer: Efficient Cross-Field Interaction and Hierarchical Sequence Compression for Industrial Recommendation at Tencent" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="CCFormer: Efficient Cross-Field Interaction and Hierarchical Sequence Compression for Industrial Recommendation at Tencent 搜广推与 LLM 应用 Tencent Platform and Content Group 2026-07-30 工业排序既要细粒度字段交互，又要吃进千长度行为序列。CCFormer 让 ID、内容等字段先分离投影再 cross attention，并用逐层扩大感受野的 token mixing 压缩旧历史，近期行为保持细粒度。 Fidelity: 核心机制复现。实现跨字段门控、分层旧序列压缩和 recent-token 保留；不复刻腾讯私有数据与 kernel。未包含 40 亿私有样本、千长度线上序列、并行多 target kernel；本地结果只验证机制方向。本地对照口径：基线为同预算 GRU；实验组为 CCFormer core，相对基线 NDCG@10 +22.44%。  ranking long-sequence sequence-compression token-mixing 搜广推 用户历史与排序骨干 CCFormer为什么让远期历史逐层扩大压缩感受野，却保留近期行为细节？ 远期行为数量大，逐条高成本交互会挤占排序预算；近期行为更可能包含当前意图变化，过早合并容易损失精细差异。CCFormer用层次token mixing压缩旧历史，同时对不同字段保留分离投影与cross-attention。压缩和字段交互各解决不同瓶颈，不能只用更短序列长度评价模型是否有效。 示意：上个月反复浏览的同类商品可逐步合并，刚刚连续查看的两个不同尺码则应保留；候选相关字段还能从压缩历史中读到长期偏好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-16b5de07814be92e">CCFormer为什么让远期历史逐层扩大压缩感受野，却保留近期行为细节？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Accformer">CCFormer: Efficient Cross-Field Interaction and Hierarchical Sequence Compression for Industrial Recommendation at Tencent</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent Platform and Content Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>远期行为数量大，逐条高成本交互会挤占排序预算；近期行为更可能包含当前意图变化，过早合并容易损失精细差异。CCFormer用层次token mixing压缩旧历史，同时对不同字段保留分离投影与cross-attention。压缩和字段交互各解决不同瓶颈，不能只用更短序列长度评价模型是否有效。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>上个月反复浏览的同类商品可逐步合并，刚刚连续查看的两个不同尺码则应保留；候选相关字段还能从压缩历史中读到长期偏好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28070">原论文</a> · <a href="../../../../reproductions/2607.28070-ccformer/">实现解读</a> · <a href="#qa-16b5de07814be92e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ccformer" data-paper-title="CCFormer: Efficient Cross-Field Interaction and Hierarchical Sequence Compression for Industrial Recommendation at Tencent" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="CCFormer: Efficient Cross-Field Interaction and Hierarchical Sequence Compression for Industrial Recommendation at Tencent 搜广推与 LLM 应用 Tencent Platform and Content Group 2026-07-30 工业排序既要细粒度字段交互，又要吃进千长度行为序列。CCFormer 让 ID、内容等字段先分离投影再 cross attention，并用逐层扩大感受野的 token mixing 压缩旧历史，近期行为保持细粒度。 Fidelity: 核心机制复现。实现跨字段门控、分层旧序列压缩和 recent-token 保留；不复刻腾讯私有数据与 kernel。未包含 40 亿私有样本、千长度线上序列、并行多 target kernel；本地结果只验证机制方向。本地对照口径：基线为同预算 GRU；实验组为 CCFormer core，相对基线 NDCG@10 +22.44%。  ranking long-sequence sequence-compression token-mixing 搜广推 用户历史与排序骨干 CCFormer 的逐层压缩与固定最近 N 条截断，分别会丢失什么？ 截断直接抛弃远期记录，后层没有机会利用它；压缩让远期信息以较粗粒度继续存在，换取更小计算，但稀有细节可能被合并。近期保细节与旧史扩感受野是设计取舍，不能称压缩完全无损，也不能由本地对 GRU 比较推断所有长序列模型排序。 示意：一年前多次摄影兴趣可压成摘要保留，最近三次露营浏览逐条保留；只取最近十条可能完全忘记摄影，压缩则可能忘掉某次特殊机型。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-021f89a6ded28d16">CCFormer 的逐层压缩与固定最近 N 条截断，分别会丢失什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Accformer">CCFormer: Efficient Cross-Field Interaction and Hierarchical Sequence Compression for Industrial Recommendation at Tencent</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent Platform and Content Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>截断直接抛弃远期记录，后层没有机会利用它；压缩让远期信息以较粗粒度继续存在，换取更小计算，但稀有细节可能被合并。近期保细节与旧史扩感受野是设计取舍，不能称压缩完全无损，也不能由本地对 GRU 比较推断所有长序列模型排序。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一年前多次摄影兴趣可压成摘要保留，最近三次露营浏览逐条保留；只取最近十条可能完全忘记摄影，压缩则可能忘掉某次特殊机型。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28070">原论文</a> · <a href="../../../../reproductions/2607.28070-ccformer/">实现解读</a> · <a href="#qa-021f89a6ded28d16">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ccformer" data-paper-title="CCFormer: Efficient Cross-Field Interaction and Hierarchical Sequence Compression for Industrial Recommendation at Tencent" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="CCFormer: Efficient Cross-Field Interaction and Hierarchical Sequence Compression for Industrial Recommendation at Tencent 搜广推与 LLM 应用 Tencent Platform and Content Group 2026-07-30 工业排序既要细粒度字段交互，又要吃进千长度行为序列。CCFormer 让 ID、内容等字段先分离投影再 cross attention，并用逐层扩大感受野的 token mixing 压缩旧历史，近期行为保持细粒度。 Fidelity: 核心机制复现。实现跨字段门控、分层旧序列压缩和 recent-token 保留；不复刻腾讯私有数据与 kernel。未包含 40 亿私有样本、千长度线上序列、并行多 target kernel；本地结果只验证机制方向。本地对照口径：基线为同预算 GRU；实验组为 CCFormer core，相对基线 NDCG@10 +22.44%。  ranking long-sequence sequence-compression token-mixing 搜广推 用户历史与排序骨干 实现 CCFormer 的层级 token mixing 时，如何区分“压缩旧历史”与“全序列等比例压缩”？ 应根据层级和时间区域扩大远期感受野，同时保留近期细粒度路径，再由字段专属查询投影交互。若所有位置同样合并，便丢掉时间分辨率分配这一设计。来源本地 core 规模有限，验收应检查连接和长度变化，而非只看最终张量能运行。 示意：第一层仍保留最近四次行为各一 token，旧八次可合并；下一层只扩大旧史窗口，不该连刚发生的关键点击一起平均掉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7f9b2732273cf149">实现 CCFormer 的层级 token mixing 时，如何区分“压缩旧历史”与“全序列等比例压缩”？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Accformer">CCFormer: Efficient Cross-Field Interaction and Hierarchical Sequence Compression for Industrial Recommendation at Tencent</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent Platform and Content Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>应根据层级和时间区域扩大远期感受野，同时保留近期细粒度路径，再由字段专属查询投影交互。若所有位置同样合并，便丢掉时间分辨率分配这一设计。来源本地 core 规模有限，验收应检查连接和长度变化，而非只看最终张量能运行。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第一层仍保留最近四次行为各一 token，旧八次可合并；下一层只扩大旧史窗口，不该连刚发生的关键点击一起平均掉。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28070">原论文</a> · <a href="../../../../reproductions/2607.28070-ccformer/">实现解读</a> · <a href="#qa-7f9b2732273cf149">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ha-moe" data-paper-title="Heterogeneous Ranking in Industrial-Scale Recommender Systems: A Case Study" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Heterogeneous Ranking in Industrial-Scale Recommender Systems: A Case Study 搜广推与 LLM 应用 Google / Discover 2026-07-30 Discover 要在同一 feed 中比较新闻、视频、体育等开放网页内容，单一共享塔会让高频内容支配梯度。HA-MoE 用内容异构性特征控制 multi-gate MoE，把通用信号与领域专长分开；LENS 则追踪 expert 使用率和分领域 DL-AUC，避免总体指标掩盖局部退化。 Fidelity: 核心机制复现。本地执行异构性度量、专长 expert 与多门控融合，不把 MovieLens 代理实验写成 Google Discover 生产复刻。MovieLens genre 代理开放网页内容类型；未复刻 Discover 私有样本、LENS 生产观测系统和 DL-AUC 服务。本地对照口径：基线为同切分的 homogeneous transition-content ranker，实验组加入 HA-MoE；NDCG@10 相对 -1.77%。  ranking mixture-of-experts heterogeneity diversity 搜广推 用户历史与排序骨干 HA-MoE 为什么依据内容异构性选择专家，而不只给每种内容一个固定模型？ 固定分域容易割裂共性，一套共享塔又可能被高频内容主导。异构门控组合通用与专长专家，在新闻、视频等内容间共享有用部分并保留差异。专家实际分工需要监测，不能因名字叫体育专家就认为已学到对应能力。 示意：体育新闻既可用通用时效专家，也可借体育专长；若完全独立模型，跨域共通知识难共享，完全统一又可能让大流量视频压过新闻。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-ha-moe-beffade8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4d9f4d295ac21e2b">HA-MoE 为什么依据内容异构性选择专家，而不只给每种内容一个固定模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aha-moe">Heterogeneous Ranking in Industrial-Scale Recommender Systems: A Case Study</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / Discover</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定分域容易割裂共性，一套共享塔又可能被高频内容主导。异构门控组合通用与专长专家，在新闻、视频等内容间共享有用部分并保留差异。专家实际分工需要监测，不能因名字叫体育专家就认为已学到对应能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>体育新闻既可用通用时效专家，也可借体育专长；若完全独立模型，跨域共通知识难共享，完全统一又可能让大流量视频压过新闻。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27577">原论文</a> · <a href="../../../../reproductions/2607.27577-ha-moe/">实现解读</a> · <a href="#qa-4d9f4d295ac21e2b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ha-moe" data-paper-title="Heterogeneous Ranking in Industrial-Scale Recommender Systems: A Case Study" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Heterogeneous Ranking in Industrial-Scale Recommender Systems: A Case Study 搜广推与 LLM 应用 Google / Discover 2026-07-30 Discover 要在同一 feed 中比较新闻、视频、体育等开放网页内容，单一共享塔会让高频内容支配梯度。HA-MoE 用内容异构性特征控制 multi-gate MoE，把通用信号与领域专长分开；LENS 则追踪 expert 使用率和分领域 DL-AUC，避免总体指标掩盖局部退化。 Fidelity: 核心机制复现。本地执行异构性度量、专长 expert 与多门控融合，不把 MovieLens 代理实验写成 Google Discover 生产复刻。MovieLens genre 代理开放网页内容类型；未复刻 Discover 私有样本、LENS 生产观测系统和 DL-AUC 服务。本地对照口径：基线为同切分的 homogeneous transition-content ranker，实验组加入 HA-MoE；NDCG@10 相对 -1.77%。  ranking mixture-of-experts heterogeneity diversity 搜广推 用户历史与排序骨干 HA-MoE为什么用内容异构性控制专家，还要按领域监测DL-AUC？ 同一feed混合新闻、视频与体育时，高频领域可能支配共享梯度。异构性门控让不同样本借用不同专家组合，保留通用能力与领域专长；分领域监测检查专家利用率和局部质量，防止总体平均掩盖小领域退化。专家多不代表真正分工，必须同时看路由和切片结果。 示意：新闻流量占多数时，总体分数上涨可能盖住体育视频下降；领域感知路由可分配专长，但只有分领域评价才能发现这种被平均数隐藏的损伤。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-dda89f7194e99a78">HA-MoE为什么用内容异构性控制专家，还要按领域监测DL-AUC？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aha-moe">Heterogeneous Ranking in Industrial-Scale Recommender Systems: A Case Study</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / Discover</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一feed混合新闻、视频与体育时，高频领域可能支配共享梯度。异构性门控让不同样本借用不同专家组合，保留通用能力与领域专长；分领域监测检查专家利用率和局部质量，防止总体平均掩盖小领域退化。专家多不代表真正分工，必须同时看路由和切片结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新闻流量占多数时，总体分数上涨可能盖住体育视频下降；领域感知路由可分配专长，但只有分领域评价才能发现这种被平均数隐藏的损伤。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27577">原论文</a> · <a href="../../../../reproductions/2607.27577-ha-moe/">实现解读</a> · <a href="#qa-dda89f7194e99a78">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ha-moe" data-paper-title="Heterogeneous Ranking in Industrial-Scale Recommender Systems: A Case Study" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Heterogeneous Ranking in Industrial-Scale Recommender Systems: A Case Study 搜广推与 LLM 应用 Google / Discover 2026-07-30 Discover 要在同一 feed 中比较新闻、视频、体育等开放网页内容，单一共享塔会让高频内容支配梯度。HA-MoE 用内容异构性特征控制 multi-gate MoE，把通用信号与领域专长分开；LENS 则追踪 expert 使用率和分领域 DL-AUC，避免总体指标掩盖局部退化。 Fidelity: 核心机制复现。本地执行异构性度量、专长 expert 与多门控融合，不把 MovieLens 代理实验写成 Google Discover 生产复刻。MovieLens genre 代理开放网页内容类型；未复刻 Discover 私有样本、LENS 生产观测系统和 DL-AUC 服务。本地对照口径：基线为同切分的 homogeneous transition-content ranker，实验组加入 HA-MoE；NDCG@10 相对 -1.77%。  ranking mixture-of-experts heterogeneity diversity 搜广推 用户历史与排序骨干 LENS 的分领域 DL-AUC 与只看总体 AUC，为什么可能导向不同结论？ 总体受大流量领域支配，少数领域退化可被掩盖。分域指标与专家使用率揭示路由是否忽略某类内容，以及主指标改善来自哪里。监测不是训练保证，来源本地 NDCG 未提高，也不能用头部下降替代质量改善。 示意：视频占九成流量稍升，新闻明显变差，总 AUC 仍可能升；分领域检查会指出新闻用户受到损失，而非宣布所有内容都受益。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-2e44383e9cb5eef1">LENS 的分领域 DL-AUC 与只看总体 AUC，为什么可能导向不同结论？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aha-moe">Heterogeneous Ranking in Industrial-Scale Recommender Systems: A Case Study</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / Discover</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>总体受大流量领域支配，少数领域退化可被掩盖。分域指标与专家使用率揭示路由是否忽略某类内容，以及主指标改善来自哪里。监测不是训练保证，来源本地 NDCG 未提高，也不能用头部下降替代质量改善。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>视频占九成流量稍升，新闻明显变差，总 AUC 仍可能升；分领域检查会指出新闻用户受到损失，而非宣布所有内容都受益。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27577">原论文</a> · <a href="../../../../reproductions/2607.27577-ha-moe/">实现解读</a> · <a href="#qa-2e44383e9cb5eef1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ha-moe" data-paper-title="Heterogeneous Ranking in Industrial-Scale Recommender Systems: A Case Study" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Heterogeneous Ranking in Industrial-Scale Recommender Systems: A Case Study 搜广推与 LLM 应用 Google / Discover 2026-07-30 Discover 要在同一 feed 中比较新闻、视频、体育等开放网页内容，单一共享塔会让高频内容支配梯度。HA-MoE 用内容异构性特征控制 multi-gate MoE，把通用信号与领域专长分开；LENS 则追踪 expert 使用率和分领域 DL-AUC，避免总体指标掩盖局部退化。 Fidelity: 核心机制复现。本地执行异构性度量、专长 expert 与多门控融合，不把 MovieLens 代理实验写成 Google Discover 生产复刻。MovieLens genre 代理开放网页内容类型；未复刻 Discover 私有样本、LENS 生产观测系统和 DL-AUC 服务。本地对照口径：基线为同切分的 homogeneous transition-content ranker，实验组加入 HA-MoE；NDCG@10 相对 -1.77%。  ranking mixture-of-experts heterogeneity diversity 搜广推 用户历史与排序骨干 HA-MoE 门控 softmax 应在哪个维度，LENS 又需绑定哪些分组？ 每个样本按异构上下文在专家维归一，各专家输出先对齐再组合；使用率应按领域与时间记录，不能只有全局平均。本地以 session 熵代理异构性，并非真实开放网页全部特征，结果只解释该固定专家集合。 示意：新闻请求可对四个专家分配独立权重，不应把一批新闻与视频共同归一；否则某样本权重会受同批别人的内容类型影响。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-82c0025bf2b8bc76">HA-MoE 门控 softmax 应在哪个维度，LENS 又需绑定哪些分组？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aha-moe">Heterogeneous Ranking in Industrial-Scale Recommender Systems: A Case Study</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / Discover</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每个样本按异构上下文在专家维归一，各专家输出先对齐再组合；使用率应按领域与时间记录，不能只有全局平均。本地以 session 熵代理异构性，并非真实开放网页全部特征，结果只解释该固定专家集合。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新闻请求可对四个专家分配独立权重，不应把一批新闻与视频共同归一；否则某样本权重会受同批别人的内容类型影响。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27577">原论文</a> · <a href="../../../../reproductions/2607.27577-ha-moe/">实现解读</a> · <a href="#qa-82c0025bf2b8bc76">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:clockrope" data-paper-title="ClockRoPE: Random Fourier Rotations for Temporal Routine Modeling" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="ClockRoPE: Random Fourier Rotations for Temporal Routine Modeling 搜广推与 LLM 应用 YouTube / Google DeepMind 2026-07-29 普通 RoPE 的对数线性频率偏向“距离越远相关性越弱”，但推荐行为常有日周期和周周期。ClockRoPE 从目标周期 kernel 的 Fourier 变换中采样旋转频率，使 query-key 点积在相同小时或星期附近重新增强，并可与标准 RoPE 各占一半通道。 Fidelity: 核心机制复现。本地执行周期 Gaussian Fourier kernel 对序列注意力的调制；公开数据缺少 YouTube 的小时级行为语境，因此结果只验证机制和边界。公开 MovieLens 只提供稀疏评分时间，本地用确定性事件间隔构造周期位置；未复刻 YouTube 私有日志、生成式检索模型、TPU kernel 和线上 serving。本地对照口径：基线为不使用周期调制的 RoPE-style recency ranker；实验组加入日/周 ClockRoPE kernel，NDCG@10 相对 -2.30%。  generative-retrieval temporal-modeling rope long-sequence 搜广推 用户历史与排序骨干 ClockRoPE 为什么用周期 kernel，而不是仅认为距离越远关系越弱？ 推荐习惯常在相同小时或星期重复，线性远近无法表达“隔一周比隔两天更像”。周期 kernel 让特定时间差重新增强，旋转频率承载该结构。周期是先验，不保证所有用户都有规律，也不应把无真实时间戳的代理结果当作周期行为证据。 示意：用户每周五晚看长片，隔七天的行为可比周三更有参考价值；对作息不规律的人，同样周期增强也可能引入噪声。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-clockrope-0d0da402" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a12f3605b45b2935">ClockRoPE 为什么用周期 kernel，而不是仅认为距离越远关系越弱？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aclockrope">ClockRoPE: Random Fourier Rotations for Temporal Routine Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · YouTube / Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>推荐习惯常在相同小时或星期重复，线性远近无法表达“隔一周比隔两天更像”。周期 kernel 让特定时间差重新增强，旋转频率承载该结构。周期是先验，不保证所有用户都有规律，也不应把无真实时间戳的代理结果当作周期行为证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户每周五晚看长片，隔七天的行为可比周三更有参考价值；对作息不规律的人，同样周期增强也可能引入噪声。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26369">原论文</a> · <a href="../../../../reproductions/2607.26369-clockrope/">实现解读</a> · <a href="#qa-a12f3605b45b2935">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:clockrope" data-paper-title="ClockRoPE: Random Fourier Rotations for Temporal Routine Modeling" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="ClockRoPE: Random Fourier Rotations for Temporal Routine Modeling 搜广推与 LLM 应用 YouTube / Google DeepMind 2026-07-29 普通 RoPE 的对数线性频率偏向“距离越远相关性越弱”，但推荐行为常有日周期和周周期。ClockRoPE 从目标周期 kernel 的 Fourier 变换中采样旋转频率，使 query-key 点积在相同小时或星期附近重新增强，并可与标准 RoPE 各占一半通道。 Fidelity: 核心机制复现。本地执行周期 Gaussian Fourier kernel 对序列注意力的调制；公开数据缺少 YouTube 的小时级行为语境，因此结果只验证机制和边界。公开 MovieLens 只提供稀疏评分时间，本地用确定性事件间隔构造周期位置；未复刻 YouTube 私有日志、生成式检索模型、TPU kernel 和线上 serving。本地对照口径：基线为不使用周期调制的 RoPE-style recency ranker；实验组加入日/周 ClockRoPE kernel，NDCG@10 相对 -2.30%。  generative-retrieval temporal-modeling rope long-sequence 搜广推 用户历史与排序骨干 为什么ClockRoPE会让相隔一周的行为，比相隔两天的行为更相关？ 许多消费习惯具有周期，相关性并不随时间距离单调减弱。ClockRoPE按目标周期kernel的频谱采样旋转频率，使query-key点积在相同小时或星期附近重新增强；还可与普通RoPE分担通道，保留近期信号。周期编码提供归纳偏置，不意味着每位用户都存在同样稳定的周规律。 示意：周一早晨的通勤新闻可能与上周一早晨更接近，而非周六深夜的娱乐视频；周期旋转允许表达这种回归，同时仍可保留普通近期偏好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-4dacd6aabb5cf7c7">为什么ClockRoPE会让相隔一周的行为，比相隔两天的行为更相关？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aclockrope">ClockRoPE: Random Fourier Rotations for Temporal Routine Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · YouTube / Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>许多消费习惯具有周期，相关性并不随时间距离单调减弱。ClockRoPE按目标周期kernel的频谱采样旋转频率，使query-key点积在相同小时或星期附近重新增强；还可与普通RoPE分担通道，保留近期信号。周期编码提供归纳偏置，不意味着每位用户都存在同样稳定的周规律。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>周一早晨的通勤新闻可能与上周一早晨更接近，而非周六深夜的娱乐视频；周期旋转允许表达这种回归，同时仍可保留普通近期偏好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26369">原论文</a> · <a href="../../../../reproductions/2607.26369-clockrope/">实现解读</a> · <a href="#qa-4dacd6aabb5cf7c7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:clockrope" data-paper-title="ClockRoPE: Random Fourier Rotations for Temporal Routine Modeling" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="ClockRoPE: Random Fourier Rotations for Temporal Routine Modeling 搜广推与 LLM 应用 YouTube / Google DeepMind 2026-07-29 普通 RoPE 的对数线性频率偏向“距离越远相关性越弱”，但推荐行为常有日周期和周周期。ClockRoPE 从目标周期 kernel 的 Fourier 变换中采样旋转频率，使 query-key 点积在相同小时或星期附近重新增强，并可与标准 RoPE 各占一半通道。 Fidelity: 核心机制复现。本地执行周期 Gaussian Fourier kernel 对序列注意力的调制；公开数据缺少 YouTube 的小时级行为语境，因此结果只验证机制和边界。公开 MovieLens 只提供稀疏评分时间，本地用确定性事件间隔构造周期位置；未复刻 YouTube 私有日志、生成式检索模型、TPU kernel 和线上 serving。本地对照口径：基线为不使用周期调制的 RoPE-style recency ranker；实验组加入日/周 ClockRoPE kernel，NDCG@10 相对 -2.30%。  generative-retrieval temporal-modeling rope long-sequence 搜广推 用户历史与排序骨干 ClockRoPE 与直接加“星期几”特征，相比改变的是哪部分交互？ 星期特征提供绝对时间标签，ClockRoPE 通过 query-key 相对旋转让成对注意力随周期时间差变化。它把周期写进相似度核，而不仅让下游自行组合两个日期。两者可有重叠也可互补，机制差别不意味着在任意数据上一定胜过简单时间特征。 示意：周五标签告诉模型现在周五，周期旋转则直接让本周五与上周五在注意力关系上相近；这不是同一个位置增加了一枚类别 embedding。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5181ac128751cc15">ClockRoPE 与直接加“星期几”特征，相比改变的是哪部分交互？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aclockrope">ClockRoPE: Random Fourier Rotations for Temporal Routine Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · YouTube / Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>星期特征提供绝对时间标签，ClockRoPE 通过 query-key 相对旋转让成对注意力随周期时间差变化。它把周期写进相似度核，而不仅让下游自行组合两个日期。两者可有重叠也可互补，机制差别不意味着在任意数据上一定胜过简单时间特征。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>周五标签告诉模型现在周五，周期旋转则直接让本周五与上周五在注意力关系上相近；这不是同一个位置增加了一枚类别 embedding。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26369">原论文</a> · <a href="../../../../reproductions/2607.26369-clockrope/">实现解读</a> · <a href="#qa-5181ac128751cc15">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:clockrope" data-paper-title="ClockRoPE: Random Fourier Rotations for Temporal Routine Modeling" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="ClockRoPE: Random Fourier Rotations for Temporal Routine Modeling 搜广推与 LLM 应用 YouTube / Google DeepMind 2026-07-29 普通 RoPE 的对数线性频率偏向“距离越远相关性越弱”，但推荐行为常有日周期和周周期。ClockRoPE 从目标周期 kernel 的 Fourier 变换中采样旋转频率，使 query-key 点积在相同小时或星期附近重新增强，并可与标准 RoPE 各占一半通道。 Fidelity: 核心机制复现。本地执行周期 Gaussian Fourier kernel 对序列注意力的调制；公开数据缺少 YouTube 的小时级行为语境，因此结果只验证机制和边界。公开 MovieLens 只提供稀疏评分时间，本地用确定性事件间隔构造周期位置；未复刻 YouTube 私有日志、生成式检索模型、TPU kernel 和线上 serving。本地对照口径：基线为不使用周期调制的 RoPE-style recency ranker；实验组加入日/周 ClockRoPE kernel，NDCG@10 相对 -2.30%。  generative-retrieval temporal-modeling rope long-sequence 搜广推 用户历史与排序骨干 ClockRoPE 的日、周周期参数为什么必须和时间单位一致？ 本地 kernel 使用 T 为二十四与一百六十八，前提是时间差以小时计。若输入秒数不转换，周期位置完全改变；旋转频率采样和混合通道也要符合维度配对。测试应检查相差一周期时的增强，而不仅检查输出形状。 示意：七天应转换为一百六十八小时，代入周周期回到相近相位；若直接填六十多万秒，模型就会把同一时间差解释成许多错误周期。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-45fd047e4127727e">ClockRoPE 的日、周周期参数为什么必须和时间单位一致？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aclockrope">ClockRoPE: Random Fourier Rotations for Temporal Routine Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · YouTube / Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>本地 kernel 使用 T 为二十四与一百六十八，前提是时间差以小时计。若输入秒数不转换，周期位置完全改变；旋转频率采样和混合通道也要符合维度配对。测试应检查相差一周期时的增强，而不仅检查输出形状。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>七天应转换为一百六十八小时，代入周周期回到相近相位；若直接填六十多万秒，模型就会把同一时间差解释成许多错误周期。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26369">原论文</a> · <a href="../../../../reproductions/2607.26369-clockrope/">实现解读</a> · <a href="#qa-45fd047e4127727e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:specformer" data-paper-title="SpecFormer: Mitigating Embedding and Attention Collapse via Spectral-Aware Transformer for Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="SpecFormer: Mitigating Embedding and Attention Collapse via Spectral-Aware Transformer for Recommendation 搜广推与 LLM 应用 Zhejiang University 2026-07-27 以奇异值谱软化和谱残差位置编码，抑制推荐 Transformer 的 embedding/attention collapse。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 SpecFormer 为 0.04999，相对变化 -7.44%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  ranking transformer spectral-softening 搜广推 用户历史与排序骨干 SpecFormer为什么观察奇异值谱来处理表征坍缩？ 向量集中到少数方向会降低表达多样性，谱软化改变奇异值相对幅度，谱位置残差再影响注意力。谱更平不直接等于推荐更好，仍需任务验证。 例如许多用户向量几乎平行，模型难分不同偏好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-specformer-bc626a07" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-af3ed7d85d90e349">SpecFormer为什么观察奇异值谱来处理表征坍缩？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aspecformer">SpecFormer: Mitigating Embedding and Attention Collapse via Spectral-Aware Transformer for Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>向量集中到少数方向会降低表达多样性，谱软化改变奇异值相对幅度，谱位置残差再影响注意力。谱更平不直接等于推荐更好，仍需任务验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如许多用户向量几乎平行，模型难分不同偏好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24025">原论文</a> · <a href="../../../../reproductions/2607.24025-specformer/">实现解读</a> · <a href="#qa-af3ed7d85d90e349">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:specformer" data-paper-title="SpecFormer: Mitigating Embedding and Attention Collapse via Spectral-Aware Transformer for Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="SpecFormer: Mitigating Embedding and Attention Collapse via Spectral-Aware Transformer for Recommendation 搜广推与 LLM 应用 Zhejiang University 2026-07-27 以奇异值谱软化和谱残差位置编码，抑制推荐 Transformer 的 embedding/attention collapse。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 SpecFormer 为 0.04999，相对变化 -7.44%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  ranking transformer spectral-softening 搜广推 用户历史与排序骨干 SpecFormer 的奇异值谱软化为什么有助于对抗表示坍缩？ 表示若被少数巨大奇异值主导，很多 token 会挤在近似同一低维方向，深层交互难增加信息。对谱做软化缩小强弱方向差距，谱残差位置编码再给注意力额外结构信号，意在保留更丰富的方向。它不是让所有方向等权的无损变换，弱方向可能也含噪声，效果仍需任务证据。 示意：一组向量几乎全沿“热门程度”方向变化，主题差别被淹没。压低最强方向的相对支配后，题材等较弱方向更可能被模型利用，但也要防止放大随机噪声。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-2c07d9b7ab232c29">SpecFormer 的奇异值谱软化为什么有助于对抗表示坍缩？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aspecformer">SpecFormer: Mitigating Embedding and Attention Collapse via Spectral-Aware Transformer for Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>表示若被少数巨大奇异值主导，很多 token 会挤在近似同一低维方向，深层交互难增加信息。对谱做软化缩小强弱方向差距，谱残差位置编码再给注意力额外结构信号，意在保留更丰富的方向。它不是让所有方向等权的无损变换，弱方向可能也含噪声，效果仍需任务证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一组向量几乎全沿“热门程度”方向变化，主题差别被淹没。压低最强方向的相对支配后，题材等较弱方向更可能被模型利用，但也要防止放大随机噪声。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24025">原论文</a> · <a href="../../../../reproductions/2607.24025-specformer/">实现解读</a> · <a href="#qa-2c07d9b7ab232c29">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:specformer" data-paper-title="SpecFormer: Mitigating Embedding and Attention Collapse via Spectral-Aware Transformer for Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="SpecFormer: Mitigating Embedding and Attention Collapse via Spectral-Aware Transformer for Recommendation 搜广推与 LLM 应用 Zhejiang University 2026-07-27 以奇异值谱软化和谱残差位置编码，抑制推荐 Transformer 的 embedding/attention collapse。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 SpecFormer 为 0.04999，相对变化 -7.44%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  ranking transformer spectral-softening 搜广推 用户历史与排序骨干 谱软化与简单把所有embedding归一化有什么不同？ 单位化限制各向量长度，却不直接改变整体方向谱；奇异值变换调整群体子空间能量。两者可有不同作用，不能把L2 normalize重命名为SVD软化。 例如所有向量都长度一也能完全同向，坍缩并未因此消失。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7082029b0c37a3e7">谱软化与简单把所有embedding归一化有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aspecformer">SpecFormer: Mitigating Embedding and Attention Collapse via Spectral-Aware Transformer for Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单位化限制各向量长度，却不直接改变整体方向谱；奇异值变换调整群体子空间能量。两者可有不同作用，不能把L2 normalize重命名为SVD软化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如所有向量都长度一也能完全同向，坍缩并未因此消失。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24025">原论文</a> · <a href="../../../../reproductions/2607.24025-specformer/">实现解读</a> · <a href="#qa-7082029b0c37a3e7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:specformer" data-paper-title="SpecFormer: Mitigating Embedding and Attention Collapse via Spectral-Aware Transformer for Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="SpecFormer: Mitigating Embedding and Attention Collapse via Spectral-Aware Transformer for Recommendation 搜广推与 LLM 应用 Zhejiang University 2026-07-27 以奇异值谱软化和谱残差位置编码，抑制推荐 Transformer 的 embedding/attention collapse。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 SpecFormer 为 0.04999，相对变化 -7.44%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  ranking transformer spectral-softening 搜广推 用户历史与排序骨干 SpecFormer本地SVD路径应审查什么边界？ 输入形状、奇异值非负及变换重建需正确，位置残差与attention维度对齐；零秩或小奇异值要稳定。公开代理未复刻生产模型，不把谱图变化当线上lift。 例如二维分解重建正确，只说明计算路径，不代表用户兴趣被真实恢复。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3e7646edbc80120a">SpecFormer本地SVD路径应审查什么边界？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aspecformer">SpecFormer: Mitigating Embedding and Attention Collapse via Spectral-Aware Transformer for Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>输入形状、奇异值非负及变换重建需正确，位置残差与attention维度对齐；零秩或小奇异值要稳定。公开代理未复刻生产模型，不把谱图变化当线上lift。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如二维分解重建正确，只说明计算路径，不代表用户兴趣被真实恢复。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24025">原论文</a> · <a href="../../../../reproductions/2607.24025-specformer/">实现解读</a> · <a href="#qa-3e7646edbc80120a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:whale" data-paper-title="WHALE: A Scalable Unified Model for Recommendation with Wukong-HSTU Architecture" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="WHALE: A Scalable Unified Model for Recommendation with Wukong-HSTU Architecture 搜广推与 LLM 应用 Meta Platforms, Inc. 2026-07-19 工业推荐通常把稀疏特征交互和用户行为序列分成两个模型，扩展规模时容易形成表示与算力割裂。WHALE 用 Wukong 分支递归建模高阶特征交互，用 HSTU 分支建模行为序列，并在每层用 cross-attention 双向交换状态，形成可共同扩展的统一网络。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练 Wukong、HSTU 与逐层交换；Meta 私有特征规模和生产内核未复刻。本地实际训练 Wukong 乘性交互、门控因果 HSTU 和逐层 cross-branch attention，并以同维度、同层数的 late-fusion Transformer 为直接对照。  ranking hstu feature-interaction scaling 搜广推 用户历史与排序骨干 WHALE为什么把Wukong和HSTU两路逐层交互？ 稀疏高阶特征与行为序列原本分开，逐层交换让两种表示共同演化并扩容，而非最后才拼接一个向量。更多耦合也可能引入干扰，需任务验证。 例如用户属性可影响序列兴趣，序列状态也反过来帮助解释属性交叉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-whale-9ea1c28b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-263367f367c9a7fa">WHALE为什么把Wukong和HSTU两路逐层交互？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Awhale">WHALE: A Scalable Unified Model for Recommendation with Wukong-HSTU Architecture</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Platforms, Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>稀疏高阶特征与行为序列原本分开，逐层交换让两种表示共同演化并扩容，而非最后才拼接一个向量。更多耦合也可能引入干扰，需任务验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户属性可影响序列兴趣，序列状态也反过来帮助解释属性交叉。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.17017">原论文</a> · <a href="../../../../reproductions/2607.17017-whale/">实现解读</a> · <a href="#qa-263367f367c9a7fa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:whale" data-paper-title="WHALE: A Scalable Unified Model for Recommendation with Wukong-HSTU Architecture" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="WHALE: A Scalable Unified Model for Recommendation with Wukong-HSTU Architecture 搜广推与 LLM 应用 Meta Platforms, Inc. 2026-07-19 工业推荐通常把稀疏特征交互和用户行为序列分成两个模型，扩展规模时容易形成表示与算力割裂。WHALE 用 Wukong 分支递归建模高阶特征交互，用 HSTU 分支建模行为序列，并在每层用 cross-attention 双向交换状态，形成可共同扩展的统一网络。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练 Wukong、HSTU 与逐层交换；Meta 私有特征规模和生产内核未复刻。本地实际训练 Wukong 乘性交互、门控因果 HSTU 和逐层 cross-branch attention，并以同维度、同层数的 late-fusion Transformer 为直接对照。  ranking hstu feature-interaction scaling 搜广推 用户历史与排序骨干 WHALE 为什么让 Wukong 与 HSTU 每层双向交换状态，而不是各自编码后只在末端融合？ 特征交互分支擅长高阶字段组合，序列分支擅长行为演化，末端融合只能组合两份已完成的表示。逐层 cross-attention 让字段关系影响后续历史解释，也让行为状态改变后续特征交互，从而联合扩容。双向交流增加计算与依赖，不同于纯用户缓存结构；本地比较也只支持公开缩比任务。 示意：场景字段显示周末出游，序列分支据此关注近期露营行为；更新后的兴趣再影响价格与品类交叉。若只末端拼接，两条分支在此前多层都无法互相调整。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-0dbf74a57516dd91">WHALE 为什么让 Wukong 与 HSTU 每层双向交换状态，而不是各自编码后只在末端融合？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Awhale">WHALE: A Scalable Unified Model for Recommendation with Wukong-HSTU Architecture</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Platforms, Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>特征交互分支擅长高阶字段组合，序列分支擅长行为演化，末端融合只能组合两份已完成的表示。逐层 cross-attention 让字段关系影响后续历史解释，也让行为状态改变后续特征交互，从而联合扩容。双向交流增加计算与依赖，不同于纯用户缓存结构；本地比较也只支持公开缩比任务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>场景字段显示周末出游，序列分支据此关注近期露营行为；更新后的兴趣再影响价格与品类交叉。若只末端拼接，两条分支在此前多层都无法互相调整。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.17017">原论文</a> · <a href="../../../../reproductions/2607.17017-whale/">实现解读</a> · <a href="#qa-0dbf74a57516dd91">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:whale" data-paper-title="WHALE: A Scalable Unified Model for Recommendation with Wukong-HSTU Architecture" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="WHALE: A Scalable Unified Model for Recommendation with Wukong-HSTU Architecture 搜广推与 LLM 应用 Meta Platforms, Inc. 2026-07-19 工业推荐通常把稀疏特征交互和用户行为序列分成两个模型，扩展规模时容易形成表示与算力割裂。WHALE 用 Wukong 分支递归建模高阶特征交互，用 HSTU 分支建模行为序列，并在每层用 cross-attention 双向交换状态，形成可共同扩展的统一网络。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练 Wukong、HSTU 与逐层交换；Meta 私有特征规模和生产内核未复刻。本地实际训练 Wukong 乘性交互、门控因果 HSTU 和逐层 cross-branch attention，并以同维度、同层数的 late-fusion Transformer 为直接对照。  ranking hstu feature-interaction scaling 搜广推 用户历史与排序骨干 双向cross-attention与late fusion有何机制区别？ late fusion前两路各自独立，双向交互从中层就改变彼此表示。它增加候选或特征依赖计算，不应把两塔最终分数相加称逐层统一模型。 例如第二层的序列状态已经读过特征，后续行为建模会随之不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-cfe5edc9b606fe28">双向cross-attention与late fusion有何机制区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Awhale">WHALE: A Scalable Unified Model for Recommendation with Wukong-HSTU Architecture</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Platforms, Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>late fusion前两路各自独立，双向交互从中层就改变彼此表示。它增加候选或特征依赖计算，不应把两塔最终分数相加称逐层统一模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如第二层的序列状态已经读过特征，后续行为建模会随之不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.17017">原论文</a> · <a href="../../../../reproductions/2607.17017-whale/">实现解读</a> · <a href="#qa-cfe5edc9b606fe28">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:whale" data-paper-title="WHALE: A Scalable Unified Model for Recommendation with Wukong-HSTU Architecture" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="WHALE: A Scalable Unified Model for Recommendation with Wukong-HSTU Architecture 搜广推与 LLM 应用 Meta Platforms, Inc. 2026-07-19 工业推荐通常把稀疏特征交互和用户行为序列分成两个模型，扩展规模时容易形成表示与算力割裂。WHALE 用 Wukong 分支递归建模高阶特征交互，用 HSTU 分支建模行为序列，并在每层用 cross-attention 双向交换状态，形成可共同扩展的统一网络。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练 Wukong、HSTU 与逐层交换；Meta 私有特征规模和生产内核未复刻。本地实际训练 Wukong 乘性交互、门控因果 HSTU 和逐层 cross-branch attention，并以同维度、同层数的 late-fusion Transformer 为直接对照。  ranking hstu feature-interaction scaling 搜广推 用户历史与排序骨干 WHALE公式两路更新要留意同步还是原位覆盖吗？ 应明确该层query、key、value来自约定的同层状态，避免先覆盖一支让另一支意外读新状态。当前公开路径不含原工业全量特征与系统，不能直接报生产scaling。 例如先更新x再把新x给h，可能与两者都读旧层状态的公式不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0fa6f09b32e968b2">WHALE公式两路更新要留意同步还是原位覆盖吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Awhale">WHALE: A Scalable Unified Model for Recommendation with Wukong-HSTU Architecture</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Platforms, Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>应明确该层query、key、value来自约定的同层状态，避免先覆盖一支让另一支意外读新状态。当前公开路径不含原工业全量特征与系统，不能直接报生产scaling。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先更新x再把新x给h，可能与两者都读旧层状态的公式不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.17017">原论文</a> · <a href="../../../../reproductions/2607.17017-whale/">实现解读</a> · <a href="#qa-0fa6f09b32e968b2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:long-history-transformer" data-paper-title="Long-History User Transformers for Real-Time Ad Ranking" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Long-History User Transformers for Real-Time Ad Ranking 搜广推与 LLM 应用 Yandex 2026-07-15 广告排序需要长历史，但请求时重算完整序列会增加延迟。论文把系统拆成异步 full-history Transformer 和在线 lightweight Transformer：离线部分周期性刷新固定维度用户状态，在线只编码最近事件并读取缓存；训练先用 next-event 与 feedback 辅助任务预训练，再针对目标广告 surface 微调。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练离线缓存与在线近期双 encoder；Yandex 生产特征系统未复刻。代码实际训练 24 步长的离线历史 encoder、32 维缓存、仅查看最近 4 个事件的在线 encoder，以及 next-item/feedback 辅助目标；基线只能在请求时查看最近 4 个事件。  advertising long-sequence cached-user-representation serving 搜广推 用户历史与排序骨干 Long-History Transformer 为什么给离线缓存配一条在线近期路径？ 异步长模型保留稳定兴趣却有刷新滞后，在线轻模型捕捉刚发生变化并读取缓存，兼顾覆盖与响应。缓存不是完整实时历史，也可能压掉细节；训练辅助目标与广告任务微调各负责不同阶段，不能只把长向量拼接当全部机制。 示意：后台记用户爱摄影，今天刚开始寻找婴儿用品，在线最近行为可立即改变判断；等待下一轮长缓存才更新会慢半拍。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-long-history-transformer-f4293ee0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-eb7894ea434ef53a">Long-History Transformer 为什么给离线缓存配一条在线近期路径？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Along-history-transformer">Long-History User Transformers for Real-Time Ad Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Yandex</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>异步长模型保留稳定兴趣却有刷新滞后，在线轻模型捕捉刚发生变化并读取缓存，兼顾覆盖与响应。缓存不是完整实时历史，也可能压掉细节；训练辅助目标与广告任务微调各负责不同阶段，不能只把长向量拼接当全部机制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>后台记用户爱摄影，今天刚开始寻找婴儿用品，在线最近行为可立即改变判断；等待下一轮长缓存才更新会慢半拍。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14331">原论文</a> · <a href="../../../../reproductions/2607.14331-long-history-transformer/">实现解读</a> · <a href="#qa-eb7894ea434ef53a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:long-history-transformer" data-paper-title="Long-History User Transformers for Real-Time Ad Ranking" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Long-History User Transformers for Real-Time Ad Ranking 搜广推与 LLM 应用 Yandex 2026-07-15 广告排序需要长历史，但请求时重算完整序列会增加延迟。论文把系统拆成异步 full-history Transformer 和在线 lightweight Transformer：离线部分周期性刷新固定维度用户状态，在线只编码最近事件并读取缓存；训练先用 next-event 与 feedback 辅助任务预训练，再针对目标广告 surface 微调。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练离线缓存与在线近期双 encoder；Yandex 生产特征系统未复刻。代码实际训练 24 步长的离线历史 encoder、32 维缓存、仅查看最近 4 个事件的在线 encoder，以及 next-item/feedback 辅助目标；基线只能在请求时查看最近 4 个事件。  advertising long-sequence cached-user-representation serving 搜广推 用户历史与排序骨干 异步长历史模型已有缓存，在线轻量Transformer为什么还要保留最近事件？ 长历史缓存覆盖稳定模式，但刷新有延迟，新发生的行为可能尚未进入。在线模型读取短窗口并结合缓存，补足实时变化，避免每个请求重算完整历史。训练辅助目标还让两部分学习可用表示；缓存尺寸小并不意味着没有压缩损失，也不能把离线新鲜状态与线上旧缓存混用评估。 示意：昨夜缓存记录用户爱摄影，今天突然连续搜索育儿用品；在线最近事件能反映新需求，不必等待下一轮长历史刷新，也不必重新编码全部旧记录。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-269d7fd18f895962">异步长历史模型已有缓存，在线轻量Transformer为什么还要保留最近事件？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Along-history-transformer">Long-History User Transformers for Real-Time Ad Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Yandex</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长历史缓存覆盖稳定模式，但刷新有延迟，新发生的行为可能尚未进入。在线模型读取短窗口并结合缓存，补足实时变化，避免每个请求重算完整历史。训练辅助目标还让两部分学习可用表示；缓存尺寸小并不意味着没有压缩损失，也不能把离线新鲜状态与线上旧缓存混用评估。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>昨夜缓存记录用户爱摄影，今天突然连续搜索育儿用品；在线最近事件能反映新需求，不必等待下一轮长历史刷新，也不必重新编码全部旧记录。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14331">原论文</a> · <a href="../../../../reproductions/2607.14331-long-history-transformer/">实现解读</a> · <a href="#qa-269d7fd18f895962">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:long-history-transformer" data-paper-title="Long-History User Transformers for Real-Time Ad Ranking" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Long-History User Transformers for Real-Time Ad Ranking 搜广推与 LLM 应用 Yandex 2026-07-15 广告排序需要长历史，但请求时重算完整序列会增加延迟。论文把系统拆成异步 full-history Transformer 和在线 lightweight Transformer：离线部分周期性刷新固定维度用户状态，在线只编码最近事件并读取缓存；训练先用 next-event 与 feedback 辅助任务预训练，再针对目标广告 surface 微调。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练离线缓存与在线近期双 encoder；Yandex 生产特征系统未复刻。代码实际训练 24 步长的离线历史 encoder、32 维缓存、仅查看最近 4 个事件的在线 encoder，以及 next-item/feedback 辅助目标；基线只能在请求时查看最近 4 个事件。  advertising long-sequence cached-user-representation serving 搜广推 用户历史与排序骨干 两级异步模型与请求时完整长序列编码，相比把哪些成本移到了后台？ 后台提前处理长历史并缓存固定维状态，在线只读短段和缓存，减少重复长 self-attention。代价是刷新、存储、失效管理与压缩误差，成本并未消失。来源没有真实 Yandex feature-store 系统测量，不能按结构直接报生产延迟收益。 示意：一天多次请求共用长摘要，后台周期重算；请求更轻，但用户少请求却频繁刷新时，也要考虑后台预算是否划算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-2629bc85bd284c14">两级异步模型与请求时完整长序列编码，相比把哪些成本移到了后台？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Along-history-transformer">Long-History User Transformers for Real-Time Ad Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Yandex</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>后台提前处理长历史并缓存固定维状态，在线只读短段和缓存，减少重复长 self-attention。代价是刷新、存储、失效管理与压缩误差，成本并未消失。来源没有真实 Yandex feature-store 系统测量，不能按结构直接报生产延迟收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一天多次请求共用长摘要，后台周期重算；请求更轻，但用户少请求却频繁刷新时，也要考虑后台预算是否划算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14331">原论文</a> · <a href="../../../../reproductions/2607.14331-long-history-transformer/">实现解读</a> · <a href="#qa-2629bc85bd284c14">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:long-history-transformer" data-paper-title="Long-History User Transformers for Real-Time Ad Ranking" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Long-History User Transformers for Real-Time Ad Ranking 搜广推与 LLM 应用 Yandex 2026-07-15 广告排序需要长历史，但请求时重算完整序列会增加延迟。论文把系统拆成异步 full-history Transformer 和在线 lightweight Transformer：离线部分周期性刷新固定维度用户状态，在线只编码最近事件并读取缓存；训练先用 next-event 与 feedback 辅助任务预训练，再针对目标广告 surface 微调。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练离线缓存与在线近期双 encoder；Yandex 生产特征系统未复刻。代码实际训练 24 步长的离线历史 encoder、32 维缓存、仅查看最近 4 个事件的在线 encoder，以及 next-item/feedback 辅助目标；基线只能在请求时查看最近 4 个事件。  advertising long-sequence cached-user-representation serving 搜广推 用户历史与排序骨干 本地二十四步离线、四步在线的模型应怎样划分输入截止？ 离线历史与在线最近段都只能包含当前预测前的事件，重叠部分按定义处理，缓存不得由完整含 test 的用户序列生成。next-item、feedback 辅助标签只在训练侧。三十二维缓存是缩比配置，不代表原文长历史长度与特征规模。 示意：猜最后一片时先用所有二十四条含该片生成缓存，即使在线只看前四条也泄漏；两个分支都必须截在目标之前。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1e6ddaa6ed1b5743">本地二十四步离线、四步在线的模型应怎样划分输入截止？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Along-history-transformer">Long-History User Transformers for Real-Time Ad Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Yandex</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>离线历史与在线最近段都只能包含当前预测前的事件，重叠部分按定义处理，缓存不得由完整含 test 的用户序列生成。next-item、feedback 辅助标签只在训练侧。三十二维缓存是缩比配置，不代表原文长历史长度与特征规模。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>猜最后一片时先用所有二十四条含该片生成缓存，即使在线只看前四条也泄漏；两个分支都必须截在目标之前。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.14331">原论文</a> · <a href="../../../../reproductions/2607.14331-long-history-transformer/">实现解读</a> · <a href="#qa-1e6ddaa6ed1b5743">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tmallgs" data-paper-title="TMallGS: Scaling Unified Feature and Sequence Modeling for Generative E-commerce Search" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TMallGS: Scaling Unified Feature and Sequence Modeling for Generative E-commerce Search 搜广推与 LLM 应用 Taobao &amp; Tmall Group of Alibaba 2026-07-15 电商搜索同时包含 query、短期/长期行为、用户和商品等异构字段，直接拼 token 会放大字段噪声。TMallGS 为不同字段学习独立 Q/K/V，用 distribution-calibrated saliency 和 noise-adaptive gate 控制交互；内容特征通过 FiLM 注入，context bias 修正最终分数，并用中间层误差自适应分配 progressive supervision。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练 field-adaptive 交互和 progressive loss；天猫私有字段与生产规模未复刻。本地把 MovieLens 类型和序列映射为异构字段，真实训练 field-wise QKV、噪声门控、显式内容 FiLM、context bias 和 error-aware progressive loss。  search-ranking transformer scaling feature-interaction 搜广推 用户历史与排序骨干 TMallGS为什么按字段学习独立Q/K/V？ query、用户历史和商品字段语义与噪声不同，统一投影易混信号。字段化交互再配saliency校准与noise gate，尝试让异构信息按可靠程度进入排序。 例如一次搜索词与多年浏览汇总，不必用同一投影方式解释。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-tmallgs-f2b12094" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c3dfd8bedd01d8cd">TMallGS为什么按字段学习独立Q/K/V？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atmallgs">TMallGS: Scaling Unified Feature and Sequence Modeling for Generative E-commerce Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group of Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>query、用户历史和商品字段语义与噪声不同，统一投影易混信号。字段化交互再配saliency校准与noise gate，尝试让异构信息按可靠程度进入排序。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一次搜索词与多年浏览汇总，不必用同一投影方式解释。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.13398">原论文</a> · <a href="../../../../reproductions/2607.13398-tmallgs/">实现解读</a> · <a href="#qa-c3dfd8bedd01d8cd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tmallgs" data-paper-title="TMallGS: Scaling Unified Feature and Sequence Modeling for Generative E-commerce Search" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TMallGS: Scaling Unified Feature and Sequence Modeling for Generative E-commerce Search 搜广推与 LLM 应用 Taobao &amp; Tmall Group of Alibaba 2026-07-15 电商搜索同时包含 query、短期/长期行为、用户和商品等异构字段，直接拼 token 会放大字段噪声。TMallGS 为不同字段学习独立 Q/K/V，用 distribution-calibrated saliency 和 noise-adaptive gate 控制交互；内容特征通过 FiLM 注入，context bias 修正最终分数，并用中间层误差自适应分配 progressive supervision。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练 field-adaptive 交互和 progressive loss；天猫私有字段与生产规模未复刻。本地把 MovieLens 类型和序列映射为异构字段，真实训练 field-wise QKV、噪声门控、显式内容 FiLM、context bias 和 error-aware progressive loss。  search-ranking transformer scaling feature-interaction 搜广推 用户历史与排序骨干 TMallGS 为什么为字段独立学习 Q/K/V，还要叠加噪声 gate 与逐层监督？ 查询、历史、用户和商品字段分布不同，共用一套投影可能混淆它们的含义。字段专属投影先建立适合的交互空间，显著性校准与噪声门控再控制哪些交互值得保留；FiLM 注入内容，逐层损失按中间误差分配训练信号。多个环节分别处理异构性、噪声和深层学习，不能只归因于增加注意力头数。 示意：一次偶然点击不应像明确搜索词一样强烈影响商品排序。字段投影区分两者，门控降低噪声历史贡献，中间层监督再帮助模型逐步学到更稳定的相关性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-d7c6269d0941de88">TMallGS 为什么为字段独立学习 Q/K/V，还要叠加噪声 gate 与逐层监督？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atmallgs">TMallGS: Scaling Unified Feature and Sequence Modeling for Generative E-commerce Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group of Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>查询、历史、用户和商品字段分布不同，共用一套投影可能混淆它们的含义。字段专属投影先建立适合的交互空间，显著性校准与噪声门控再控制哪些交互值得保留；FiLM 注入内容，逐层损失按中间误差分配训练信号。多个环节分别处理异构性、噪声和深层学习，不能只归因于增加注意力头数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次偶然点击不应像明确搜索词一样强烈影响商品排序。字段投影区分两者，门控降低噪声历史贡献，中间层监督再帮助模型逐步学到更稳定的相关性。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.13398">原论文</a> · <a href="../../../../reproductions/2607.13398-tmallgs/">实现解读</a> · <a href="#qa-d7c6269d0941de88">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tmallgs" data-paper-title="TMallGS: Scaling Unified Feature and Sequence Modeling for Generative E-commerce Search" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TMallGS: Scaling Unified Feature and Sequence Modeling for Generative E-commerce Search 搜广推与 LLM 应用 Taobao &amp; Tmall Group of Alibaba 2026-07-15 电商搜索同时包含 query、短期/长期行为、用户和商品等异构字段，直接拼 token 会放大字段噪声。TMallGS 为不同字段学习独立 Q/K/V，用 distribution-calibrated saliency 和 noise-adaptive gate 控制交互；内容特征通过 FiLM 注入，context bias 修正最终分数，并用中间层误差自适应分配 progressive supervision。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练 field-adaptive 交互和 progressive loss；天猫私有字段与生产规模未复刻。本地把 MovieLens 类型和序列映射为异构字段，真实训练 field-wise QKV、噪声门控、显式内容 FiLM、context bias 和 error-aware progressive loss。  search-ranking transformer scaling feature-interaction 搜广推 用户历史与排序骨干 FiLM内容注入与简单拼接内容向量有何不同？ FiLM用内容生成逐维缩放与偏置来调制状态，拼接只把两向量交给后续层。progressive supervision还按中层误差分配目标，不能用单MLP拼接替代整套。 例如内容条件可强调某些隐藏方向，而不是只多放一组输入列。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-37475999840701e5">FiLM内容注入与简单拼接内容向量有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atmallgs">TMallGS: Scaling Unified Feature and Sequence Modeling for Generative E-commerce Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group of Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>FiLM用内容生成逐维缩放与偏置来调制状态，拼接只把两向量交给后续层。progressive supervision还按中层误差分配目标，不能用单MLP拼接替代整套。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如内容条件可强调某些隐藏方向，而不是只多放一组输入列。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.13398">原论文</a> · <a href="../../../../reproductions/2607.13398-tmallgs/">实现解读</a> · <a href="#qa-37475999840701e5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tmallgs" data-paper-title="TMallGS: Scaling Unified Feature and Sequence Modeling for Generative E-commerce Search" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TMallGS: Scaling Unified Feature and Sequence Modeling for Generative E-commerce Search 搜广推与 LLM 应用 Taobao &amp; Tmall Group of Alibaba 2026-07-15 电商搜索同时包含 query、短期/长期行为、用户和商品等异构字段，直接拼 token 会放大字段噪声。TMallGS 为不同字段学习独立 Q/K/V，用 distribution-calibrated saliency 和 noise-adaptive gate 控制交互；内容特征通过 FiLM 注入，context bias 修正最终分数，并用中间层误差自适应分配 progressive supervision。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实训练 field-adaptive 交互和 progressive loss；天猫私有字段与生产规模未复刻。本地把 MovieLens 类型和序列映射为异构字段，真实训练 field-wise QKV、噪声门控、显式内容 FiLM、context bias 和 error-aware progressive loss。  search-ranking transformer scaling feature-interaction 搜广推 用户历史与排序骨干 本地TMallGS极大相对NDCG提升能否说明稳定胜出？ 不能，README记录绝对命中很少，主要证明field-wise、门控、FiLM、bias和中层监督训练链可运行。单seed小基数百分比不代表生产模型统计稳定提升。 例如从极少命中增加一点可有很大百分比，但证据仍需看绝对量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-229c564ec8014c24">本地TMallGS极大相对NDCG提升能否说明稳定胜出？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atmallgs">TMallGS: Scaling Unified Feature and Sequence Modeling for Generative E-commerce Search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group of Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，README记录绝对命中很少，主要证明field-wise、门控、FiLM、bias和中层监督训练链可运行。单seed小基数百分比不代表生产模型统计稳定提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如从极少命中增加一点可有很大百分比，但证据仍需看绝对量。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.13398">原论文</a> · <a href="../../../../reproductions/2607.13398-tmallgs/">实现解读</a> · <a href="#qa-229c564ec8014c24">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:nontp" data-paper-title="Not Only NTP: Extending Training Signal Coverage for Generative Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Not Only NTP: Extending Training Signal Coverage for Generative Recommendation 搜广推与 LLM 应用 Meituan 2026-07-14 标准 next-token prediction 只要求当前位置预测紧邻的下一个物品：它既没有监督 hidden state 理解更远的未来轨迹，也没有让跨业务上下文直接更新稀疏域目标物品。NONTP 将前者称为 temporal locality，后者称为 spatial locality。TCL 用在线 backbone 的第个状态预测 EMA teacher 的第个未来状态，并只把其他用户序列作为负例； Fidelity: 核心机制复现。本地真实执行 NTP、EMA teacher、三个未来步 predictor、跨序列 InfoNCE、跨域 hidden-state pooling 与共享预测头；训练辅助分支在推理时全部移除。保留论文、、和两个辅助损失权重 0.1。本地对照口径：基线是相同 causal backbone、相同初始化和训练预算的 ntp；实验组是同时加入 TCL 与 TDL 的 nontp。三随机种子下 Hit@10 从 0.05079 降到 0.04828（-4.93%），NDCG@10 从 0.02431 降到 0.02222（-8.62%）。  generative-recommendation contrastive-learning multi-domain 搜广推 用户历史与排序骨干 NONTP 为什么只在训练增加辅助模块而保持线上 NTP 结构？ TCL 与 TDL 把远期和跨域监督写入 backbone，推理不必再计算未来教师或辅助分支，保留原服务预算。训练更丰富不保证全部任务更好，特别弱域标签与短历史可能提供少信息。未来监督可用不等于线上能读未来。 示意：训练时教当前状态理解几步后的轨迹，上线仍只算当前历史状态与 item head，既不加载未来记录也不多跑教师。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-nontp-bd610948" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-56b178d9e31f5503">NONTP 为什么只在训练增加辅助模块而保持线上 NTP 结构？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Anontp">Not Only NTP: Extending Training Signal Coverage for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>TCL 与 TDL 把远期和跨域监督写入 backbone，推理不必再计算未来教师或辅助分支，保留原服务预算。训练更丰富不保证全部任务更好，特别弱域标签与短历史可能提供少信息。未来监督可用不等于线上能读未来。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练时教当前状态理解几步后的轨迹，上线仍只算当前历史状态与 item head，既不加载未来记录也不多跑教师。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12277">原论文</a> · <a href="../../../../reproductions/2607.12277-nontp/">实现解读</a> · <a href="#qa-56b178d9e31f5503">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:nontp" data-paper-title="Not Only NTP: Extending Training Signal Coverage for Generative Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Not Only NTP: Extending Training Signal Coverage for Generative Recommendation 搜广推与 LLM 应用 Meituan 2026-07-14 标准 next-token prediction 只要求当前位置预测紧邻的下一个物品：它既没有监督 hidden state 理解更远的未来轨迹，也没有让跨业务上下文直接更新稀疏域目标物品。NONTP 将前者称为 temporal locality，后者称为 spatial locality。TCL 用在线 backbone 的第个状态预测 EMA teacher 的第个未来状态，并只把其他用户序列作为负例； Fidelity: 核心机制复现。本地真实执行 NTP、EMA teacher、三个未来步 predictor、跨序列 InfoNCE、跨域 hidden-state pooling 与共享预测头；训练辅助分支在推理时全部移除。保留论文、、和两个辅助损失权重 0.1。本地对照口径：基线是相同 causal backbone、相同初始化和训练预算的 ntp；实验组是同时加入 TCL 与 TDL 的 nontp。三随机种子下 Hit@10 从 0.05079 降到 0.04828（-4.93%），NDCG@10 从 0.02431 降到 0.02222（-8.62%）。  generative-recommendation contrastive-learning multi-domain 搜广推 用户历史与排序骨干 NONTP 的 TCL 与 TDL 分别补足 next-token prediction 的哪两种局部性？ TCL 让当前状态预测 EMA 教师的较远未来状态，补上只监督紧邻下一步的时间局部性；TDL 用目标之前的异域状态经共享物品头预测目标，让稀疏域获得跨域信号。两项只在训练时使用，推理仍走原主干。未来状态是训练监督而非上线输入，不能把这种训练方式理解为允许推理读取未来。 示意：用户先看家居内容再购买灯具。TCL 训练早期状态理解更远的轨迹，TDL 让购买前的异域浏览也参与预测灯具；真实请求时仍只能读取已经发生的行为。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-0d443595c80ba49d">NONTP 的 TCL 与 TDL 分别补足 next-token prediction 的哪两种局部性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Anontp">Not Only NTP: Extending Training Signal Coverage for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>TCL 让当前状态预测 EMA 教师的较远未来状态，补上只监督紧邻下一步的时间局部性；TDL 用目标之前的异域状态经共享物品头预测目标，让稀疏域获得跨域信号。两项只在训练时使用，推理仍走原主干。未来状态是训练监督而非上线输入，不能把这种训练方式理解为允许推理读取未来。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户先看家居内容再购买灯具。TCL 训练早期状态理解更远的轨迹，TDL 让购买前的异域浏览也参与预测灯具；真实请求时仍只能读取已经发生的行为。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12277">原论文</a> · <a href="../../../../reproductions/2607.12277-nontp/">实现解读</a> · <a href="#qa-0d443595c80ba49d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:nontp" data-paper-title="Not Only NTP: Extending Training Signal Coverage for Generative Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Not Only NTP: Extending Training Signal Coverage for Generative Recommendation 搜广推与 LLM 应用 Meituan 2026-07-14 标准 next-token prediction 只要求当前位置预测紧邻的下一个物品：它既没有监督 hidden state 理解更远的未来轨迹，也没有让跨业务上下文直接更新稀疏域目标物品。NONTP 将前者称为 temporal locality，后者称为 spatial locality。TCL 用在线 backbone 的第个状态预测 EMA teacher 的第个未来状态，并只把其他用户序列作为负例； Fidelity: 核心机制复现。本地真实执行 NTP、EMA teacher、三个未来步 predictor、跨序列 InfoNCE、跨域 hidden-state pooling 与共享预测头；训练辅助分支在推理时全部移除。保留论文、、和两个辅助损失权重 0.1。本地对照口径：基线是相同 causal backbone、相同初始化和训练预算的 ntp；实验组是同时加入 TCL 与 TDL 的 nontp。三随机种子下 Hit@10 从 0.05079 降到 0.04828（-4.93%），NDCG@10 从 0.02431 降到 0.02222（-8.62%）。  generative-recommendation contrastive-learning multi-domain 搜广推 用户历史与排序骨干 TCL 的 EMA teacher 与直接拿在线未来状态作目标，相比稳定性在哪里？ EMA 平滑参数变化并作为停止梯度目标，减少两边一起追逐的抖动；但仍需未来状态只作训练监督。负例来自其他用户，避免把同用户相邻兴趣误作负例。稳定目标不是准确目标保证，EMA 也可能保留旧偏差。 示意：在线模型刚更新较大，直接互相对齐会不断移动靶子；缓慢教师提供较稳参照，但若教师一直学热门模式，稳定也不能自动变有用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ea47c7bf8e79cb75">TCL 的 EMA teacher 与直接拿在线未来状态作目标，相比稳定性在哪里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Anontp">Not Only NTP: Extending Training Signal Coverage for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>EMA 平滑参数变化并作为停止梯度目标，减少两边一起追逐的抖动；但仍需未来状态只作训练监督。负例来自其他用户，避免把同用户相邻兴趣误作负例。稳定目标不是准确目标保证，EMA 也可能保留旧偏差。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>在线模型刚更新较大，直接互相对齐会不断移动靶子；缓慢教师提供较稳参照，但若教师一直学热门模式，稳定也不能自动变有用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12277">原论文</a> · <a href="../../../../reproductions/2607.12277-nontp/">实现解读</a> · <a href="#qa-ea47c7bf8e79cb75">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:nontp" data-paper-title="Not Only NTP: Extending Training Signal Coverage for Generative Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Not Only NTP: Extending Training Signal Coverage for Generative Recommendation 搜广推与 LLM 应用 Meituan 2026-07-14 标准 next-token prediction 只要求当前位置预测紧邻的下一个物品：它既没有监督 hidden state 理解更远的未来轨迹，也没有让跨业务上下文直接更新稀疏域目标物品。NONTP 将前者称为 temporal locality，后者称为 spatial locality。TCL 用在线 backbone 的第个状态预测 EMA teacher 的第个未来状态，并只把其他用户序列作为负例； Fidelity: 核心机制复现。本地真实执行 NTP、EMA teacher、三个未来步 predictor、跨序列 InfoNCE、跨域 hidden-state pooling 与共享预测头；训练辅助分支在推理时全部移除。保留论文、、和两个辅助损失权重 0.1。本地对照口径：基线是相同 causal backbone、相同初始化和训练预算的 ntp；实验组是同时加入 TCL 与 TDL 的 nontp。三随机种子下 Hit@10 从 0.05079 降到 0.04828（-4.93%），NDCG@10 从 0.02431 降到 0.02222（-8.62%）。  generative-recommendation contrastive-learning multi-domain 搜广推 用户历史与排序骨干 TDL 选择异域历史时，为什么同时要求在目标之前，并复用同一 item head？ 时间条件防泄漏，异域条件聚焦跨业务迁移；均值后的状态通过 NTP 相同分类头，使辅助监督直接更新目标物品空间。空集合需跳过而非造零标签，不能另接完全独立头仍声称同接口迁移。 示意：预测购物目标只取此前其他域状态，不能取目标后视频行为；若没有异域历史，该位置没有 TDL 证据，不应强行填一个假正例。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e76a922081830518">TDL 选择异域历史时，为什么同时要求在目标之前，并复用同一 item head？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Anontp">Not Only NTP: Extending Training Signal Coverage for Generative Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meituan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>时间条件防泄漏，异域条件聚焦跨业务迁移；均值后的状态通过 NTP 相同分类头，使辅助监督直接更新目标物品空间。空集合需跳过而非造零标签，不能另接完全独立头仍声称同接口迁移。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>预测购物目标只取此前其他域状态，不能取目标后视频行为；若没有异域历史，该位置没有 TDL 证据，不应强行填一个假正例。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12277">原论文</a> · <a href="../../../../reproductions/2607.12277-nontp/">实现解读</a> · <a href="#qa-e76a922081830518">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sam" data-paper-title="Learning to Forget: Satiation-Aware Long-Sequence Transducers for Mitigating Post-Purchase Redundancy" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Learning to Forget: Satiation-Aware Long-Sequence Transducers for Mitigating Post-Purchase Redundancy 搜广推与 LLM 应用 Alibaba Group 2026-07-14 购买完成的是一簇意图，继续放大购买前点击会制造重复推荐。SAM 用 pointwise cross-attention 定位要压制的历史节点，并从长期购买序列预测补货节奏；ASGU 在刚购买时强抑制、接近周期时逐渐恢复，再以 log-mask 修改注意力 logits。 Fidelity: 核心机制复现。双路径 intent/rhythm、ASGU、log-mask intervention 与 TTNP 周期监督均实际执行。没有真实补货型商品和 censored purchase log；只验证机制和失败边界。本地对照口径：基线是 DIN-like interest score；实验组 SAM 加入按 genre 学习的周期与 ASGU，相对基线 Hit@10 -12.50%、NDCG@10 -6.60%。  ranking long-sequence satiation 搜广推 用户历史与排序骨干 SAM的购买后抑制，是把同类商品直接加入不可推荐黑名单吗？ 不是。定义性操作是降低相关历史节点在注意力中的权重，并随时间逐渐恢复；它改变证据利用强度，不是给所有同类候选设置永久禁用规则。先区分软注意力抑制与硬过滤，才能理解为何模型仍可根据其他信号推荐相关商品。 教学例子：买过洗发水后降低那段旧浏览历史的影响，不等于规定任何洗护商品都绝不能再次进入候选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-sam-b9df9dfc" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f667ebf89a92beef">SAM的购买后抑制，是把同类商品直接加入不可推荐黑名单吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asam">Learning to Forget: Satiation-Aware Long-Sequence Transducers for Mitigating Post-Purchase Redundancy</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。定义性操作是降低相关历史节点在注意力中的权重，并随时间逐渐恢复；它改变证据利用强度，不是给所有同类候选设置永久禁用规则。先区分软注意力抑制与硬过滤，才能理解为何模型仍可根据其他信号推荐相关商品。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>买过洗发水后降低那段旧浏览历史的影响，不等于规定任何洗护商品都绝不能再次进入候选。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12714">原论文</a> · <a href="../../../../reproductions/2607.12714-sam/">实现解读</a> · <a href="#qa-f667ebf89a92beef">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sam" data-paper-title="Learning to Forget: Satiation-Aware Long-Sequence Transducers for Mitigating Post-Purchase Redundancy" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Learning to Forget: Satiation-Aware Long-Sequence Transducers for Mitigating Post-Purchase Redundancy 搜广推与 LLM 应用 Alibaba Group 2026-07-14 购买完成的是一簇意图，继续放大购买前点击会制造重复推荐。SAM 用 pointwise cross-attention 定位要压制的历史节点，并从长期购买序列预测补货节奏；ASGU 在刚购买时强抑制、接近周期时逐渐恢复，再以 log-mask 修改注意力 logits。 Fidelity: 核心机制复现。双路径 intent/rhythm、ASGU、log-mask intervention 与 TTNP 周期监督均实际执行。没有真实补货型商品和 censored purchase log；只验证机制和失败边界。本地对照口径：基线是 DIN-like interest score；实验组 SAM 加入按 genre 学习的周期与 ASGU，相对基线 Hit@10 -12.50%、NDCG@10 -6.60%。  ranking long-sequence satiation 搜广推 用户历史与排序骨干 SAM 为什么购买后先压制相关历史，再随补货周期逐渐恢复注意力？ 购买常意味着一个需求已经完成，继续照抄购买前点击会导致重复推荐。SAM 先定位属于同一已完成意图的历史节点，再依据长期购买节奏估计周期，用时间门控和 log-mask 压低注意力，接近补货时间时逐渐解除。它区分需求完成与永久厌恶；本地用评分代理购买事件，不能验证真实补货规律。 示意：刚买大包装洗衣液时减少同类推荐，几周后按个人使用节奏逐步恢复；若永久删掉这类兴趣会错过补货，完全不抑制又会立刻重复展示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-90747e26d9c7c6ae">SAM 为什么购买后先压制相关历史，再随补货周期逐渐恢复注意力？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asam">Learning to Forget: Satiation-Aware Long-Sequence Transducers for Mitigating Post-Purchase Redundancy</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>购买常意味着一个需求已经完成，继续照抄购买前点击会导致重复推荐。SAM 先定位属于同一已完成意图的历史节点，再依据长期购买节奏估计周期，用时间门控和 log-mask 压低注意力，接近补货时间时逐渐解除。它区分需求完成与永久厌恶；本地用评分代理购买事件，不能验证真实补货规律。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>刚买大包装洗衣液时减少同类推荐，几周后按个人使用节奏逐步恢复；若永久删掉这类兴趣会错过补货，完全不抑制又会立刻重复展示。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12714">原论文</a> · <a href="../../../../reproductions/2607.12714-sam/">实现解读</a> · <a href="#qa-90747e26d9c7c6ae">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sam" data-paper-title="Learning to Forget: Satiation-Aware Long-Sequence Transducers for Mitigating Post-Purchase Redundancy" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Learning to Forget: Satiation-Aware Long-Sequence Transducers for Mitigating Post-Purchase Redundancy 搜广推与 LLM 应用 Alibaba Group 2026-07-14 购买完成的是一簇意图，继续放大购买前点击会制造重复推荐。SAM 用 pointwise cross-attention 定位要压制的历史节点，并从长期购买序列预测补货节奏；ASGU 在刚购买时强抑制、接近周期时逐渐恢复，再以 log-mask 修改注意力 logits。 Fidelity: 核心机制复现。双路径 intent/rhythm、ASGU、log-mask intervention 与 TTNP 周期监督均实际执行。没有真实补货型商品和 censored purchase log；只验证机制和失败边界。本地对照口径：基线是 DIN-like interest score；实验组 SAM 加入按 genre 学习的周期与 ASGU，相对基线 Hit@10 -12.50%、NDCG@10 -6.60%。  ranking long-sequence satiation 搜广推 用户历史与排序骨干 SAM与简单购买后固定冷却天数有什么差别？ 模型按相关历史节点和长期购买节奏个性化抑制，固定冷却对用户商品一刀切。周期预测不准也会误伤，且非补货商品未必适用同样假设。 例如咖啡与电视的重复需求周期不能统一设成一周。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c312c786eab5bae1">SAM与简单购买后固定冷却天数有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asam">Learning to Forget: Satiation-Aware Long-Sequence Transducers for Mitigating Post-Purchase Redundancy</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>模型按相关历史节点和长期购买节奏个性化抑制，固定冷却对用户商品一刀切。周期预测不准也会误伤，且非补货商品未必适用同样假设。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如咖啡与电视的重复需求周期不能统一设成一周。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12714">原论文</a> · <a href="../../../../reproductions/2607.12714-sam/">实现解读</a> · <a href="#qa-c312c786eab5bae1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sam" data-paper-title="Learning to Forget: Satiation-Aware Long-Sequence Transducers for Mitigating Post-Purchase Redundancy" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Learning to Forget: Satiation-Aware Long-Sequence Transducers for Mitigating Post-Purchase Redundancy 搜广推与 LLM 应用 Alibaba Group 2026-07-14 购买完成的是一簇意图，继续放大购买前点击会制造重复推荐。SAM 用 pointwise cross-attention 定位要压制的历史节点，并从长期购买序列预测补货节奏；ASGU 在刚购买时强抑制、接近周期时逐渐恢复，再以 log-mask 修改注意力 logits。 Fidelity: 核心机制复现。双路径 intent/rhythm、ASGU、log-mask intervention 与 TTNP 周期监督均实际执行。没有真实补货型商品和 censored purchase log；只验证机制和失败边界。本地对照口径：基线是 DIN-like interest score；实验组 SAM 加入按 genre 学习的周期与 ASGU，相对基线 Hit@10 -12.50%、NDCG@10 -6.60%。  ranking long-sequence satiation 搜广推 用户历史与排序骨干 SAM把mask放到attention哪里，本地有哪些数据边界？ 以log-mask加到attention logits，需保护mask为正并裁数值范围，不是最终分数直接相乘。当前没有真实补货商品和删失购买日志，只验证机制和失败边界。 例如mask接近零时需数值保护，但不能因此声称真实复购周期已预测。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-2bd429203c7ebdc1">SAM把mask放到attention哪里，本地有哪些数据边界？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asam">Learning to Forget: Satiation-Aware Long-Sequence Transducers for Mitigating Post-Purchase Redundancy</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>以log-mask加到attention logits，需保护mask为正并裁数值范围，不是最终分数直接相乘。当前没有真实补货商品和删失购买日志，只验证机制和失败边界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如mask接近零时需数值保护，但不能因此声称真实复购周期已预测。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12714">原论文</a> · <a href="../../../../reproductions/2607.12714-sam/">实现解读</a> · <a href="#qa-2bd429203c7ebdc1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:slimper" data-paper-title="SlimPer: Make Personalization Model Slim and Smart" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="SlimPer: Make Personalization Model Slim and Smart 搜广推与 LLM 应用 Meta Platforms, Inc. 2026-07-14 SlimPer 每层用固定槽位的 user-item 知识库查询用户 token 池，执行 Select–Match–Refine。用户池保持可读，精炼层之间只传播小知识库；输入编码仍可带局部上下文。 本地只在短历史 MovieLens 上验证缩小机制；NDCG@10 +1.29% 仅为 seed 42 的 smoke，未实测生产 QPS 或显存。ROO 共享用户编码，候选相关知识库仍逐候选更新。 为什么用户 tokens 能共享，但 knowledge base 的更新结果不能全部共享？ ranking long-sequence serving-efficiency 搜广推 用户历史与排序骨干 SlimPer 不逐层更新全历史，是否意味着它完全不建模相邻行为之间的关系？ 不是。原文§2.5在事件 token 化时加入局部上下文编码，可用卷积或滑窗注意力融合邻近行为；后续层才反复读取这些用户 token 并更新固定知识库。因此它减少的是深层全量两两历史交互，而非禁止任何历史关系。固定知识槽也只是中间状态预算，原始输入存储与每层读取仍随历史长度增长。 示意：连续搜索、比较、加购可先编码成带局部背景的事件，再由多层知识槽按候选读取。虽然每层不重写整条历史，这些事件也不必被当成彼此孤立的点击。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-slimper-ce7fc963" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c31fdda2ede9afd6">SlimPer 不逐层更新全历史，是否意味着它完全不建模相邻行为之间的关系？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aslimper">SlimPer: Make Personalization Model Slim and Smart</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Platforms, Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。原文§2.5在事件 token 化时加入局部上下文编码，可用卷积或滑窗注意力融合邻近行为；后续层才反复读取这些用户 token 并更新固定知识库。因此它减少的是深层全量两两历史交互，而非禁止任何历史关系。固定知识槽也只是中间状态预算，原始输入存储与每层读取仍随历史长度增长。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>连续搜索、比较、加购可先编码成带局部背景的事件，再由多层知识槽按候选读取。虽然每层不重写整条历史，这些事件也不必被当成彼此孤立的点击。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12281">原论文</a> · <a href="../../../../reproductions/2607.12281-slimper/">实现解读</a> · <a href="#qa-c31fdda2ede9afd6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:slimper" data-paper-title="SlimPer: Make Personalization Model Slim and Smart" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="SlimPer: Make Personalization Model Slim and Smart 搜广推与 LLM 应用 Meta Platforms, Inc. 2026-07-14 SlimPer 每层用固定槽位的 user-item 知识库查询用户 token 池，执行 Select–Match–Refine。用户池保持可读，精炼层之间只传播小知识库；输入编码仍可带局部上下文。 本地只在短历史 MovieLens 上验证缩小机制；NDCG@10 +1.29% 仅为 seed 42 的 smoke，未实测生产 QPS 或显存。ROO 共享用户编码，候选相关知识库仍逐候选更新。 为什么用户 tokens 能共享，但 knowledge base 的更新结果不能全部共享？ ranking long-sequence serving-efficiency 搜广推 用户历史与排序骨干 SlimPer每层都读取长历史，为什么还能只保留固定大小的knowledge base？ 被反复更新的是少量候选相关知识槽，而原始用户token作为只读证据被重新访问。Select取出相关证据，Match与知识模板显式比较，Refine再更新槽位；层间无需传播全部历史隐藏状态。共享的是用户编码，候选相关knowledge base仍分别演化，并不是所有候选共用一个最终兴趣向量。 示意：同一份购买记录可供鞋和相机两个候选共读，但两组小知识槽分别整理尺寸需求和摄影兴趣，不能把鞋候选更新过的槽直接给相机。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-4a13e5753d9c783b">SlimPer每层都读取长历史，为什么还能只保留固定大小的knowledge base？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aslimper">SlimPer: Make Personalization Model Slim and Smart</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Platforms, Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>被反复更新的是少量候选相关知识槽，而原始用户token作为只读证据被重新访问。Select取出相关证据，Match与知识模板显式比较，Refine再更新槽位；层间无需传播全部历史隐藏状态。共享的是用户编码，候选相关knowledge base仍分别演化，并不是所有候选共用一个最终兴趣向量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一份购买记录可供鞋和相机两个候选共读，但两组小知识槽分别整理尺寸需求和摄影兴趣，不能把鞋候选更新过的槽直接给相机。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12281">原论文</a> · <a href="../../../../reproductions/2607.12281-slimper/">实现解读</a> · <a href="#qa-4a13e5753d9c783b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:slimper" data-paper-title="SlimPer: Make Personalization Model Slim and Smart" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="SlimPer: Make Personalization Model Slim and Smart 搜广推与 LLM 应用 Meta Platforms, Inc. 2026-07-14 SlimPer 每层用固定槽位的 user-item 知识库查询用户 token 池，执行 Select–Match–Refine。用户池保持可读，精炼层之间只传播小知识库；输入编码仍可带局部上下文。 本地只在短历史 MovieLens 上验证缩小机制；NDCG@10 +1.29% 仅为 seed 42 的 smoke，未实测生产 QPS 或显存。ROO 共享用户编码，候选相关知识库仍逐候选更新。 为什么用户 tokens 能共享，但 knowledge base 的更新结果不能全部共享？ ranking long-sequence serving-efficiency 搜广推 用户历史与排序骨干 SlimPer 已经用 attention 选取证据，为什么还要与 knowledge templates 显式点积匹配？ Select 用当前知识库生成查询，得到少量被聚合的用户证据，回答“该取哪些信息”；Match 再把这些证据与同一知识库生成的多个模板比较，形成查询数乘模板数的相关性矩阵。Refine 利用这些显式关系更新知识，而非把聚合向量直接当最终兴趣。两步把证据检索与多方面相关性判断分开。 示意：面对跑鞋候选，Select 找到用户跑步距离与尺码相关行为；Match 再分别比较舒适度、用途等模板，更新知识槽。找到证据不等于已经判断它支持候选的哪个方面。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c8469615c85e200f">SlimPer 已经用 attention 选取证据，为什么还要与 knowledge templates 显式点积匹配？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aslimper">SlimPer: Make Personalization Model Slim and Smart</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Platforms, Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Select 用当前知识库生成查询，得到少量被聚合的用户证据，回答“该取哪些信息”；Match 再把这些证据与同一知识库生成的多个模板比较，形成查询数乘模板数的相关性矩阵。Refine 利用这些显式关系更新知识，而非把聚合向量直接当最终兴趣。两步把证据检索与多方面相关性判断分开。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>面对跑鞋候选，Select 找到用户跑步距离与尺码相关行为；Match 再分别比较舒适度、用途等模板，更新知识槽。找到证据不等于已经判断它支持候选的哪个方面。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12281">原论文</a> · <a href="../../../../reproductions/2607.12281-slimper/">实现解读</a> · <a href="#qa-c8469615c85e200f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:slimper" data-paper-title="SlimPer: Make Personalization Model Slim and Smart" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="SlimPer: Make Personalization Model Slim and Smart 搜广推与 LLM 应用 Meta Platforms, Inc. 2026-07-14 SlimPer 每层用固定槽位的 user-item 知识库查询用户 token 池，执行 Select–Match–Refine。用户池保持可读，精炼层之间只传播小知识库；输入编码仍可带局部上下文。 本地只在短历史 MovieLens 上验证缩小机制；NDCG@10 +1.29% 仅为 seed 42 的 smoke，未实测生产 QPS 或显存。ROO 共享用户编码，候选相关知识库仍逐候选更新。 为什么用户 tokens 能共享，但 knowledge base 的更新结果不能全部共享？ ranking long-sequence serving-efficiency 搜广推 用户历史与排序骨干 SlimPer与HSTU或LONGER比较时，为什么不能只把它当序列encoder？ SlimPer面向user-item relevance，KB还接收item与cross特征，每层Select–Match–Refine直接形成个性化排序状态。比较需包含候选交互与任务头，不能只拿一个用户序列向量排同协议胜负。 例如同一长历史面对两个候选可有不同知识库，不能只与候选无关encoder输出硬比。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-85f55baa2ea8d44b">SlimPer与HSTU或LONGER比较时，为什么不能只把它当序列encoder？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aslimper">SlimPer: Make Personalization Model Slim and Smart</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Platforms, Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>SlimPer面向user-item relevance，KB还接收item与cross特征，每层Select–Match–Refine直接形成个性化排序状态。比较需包含候选交互与任务头，不能只拿一个用户序列向量排同协议胜负。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一长历史面对两个候选可有不同知识库，不能只与候选无关encoder输出硬比。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12281">原论文</a> · <a href="../../../../reproductions/2607.12281-slimper/">实现解读</a> · <a href="#qa-85f55baa2ea8d44b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:slimper" data-paper-title="SlimPer: Make Personalization Model Slim and Smart" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="SlimPer: Make Personalization Model Slim and Smart 搜广推与 LLM 应用 Meta Platforms, Inc. 2026-07-14 SlimPer 每层用固定槽位的 user-item 知识库查询用户 token 池，执行 Select–Match–Refine。用户池保持可读，精炼层之间只传播小知识库；输入编码仍可带局部上下文。 本地只在短历史 MovieLens 上验证缩小机制；NDCG@10 +1.29% 仅为 seed 42 的 smoke，未实测生产 QPS 或显存。ROO 共享用户编码，候选相关知识库仍逐候选更新。 为什么用户 tokens 能共享，但 knowledge base 的更新结果不能全部共享？ ranking long-sequence serving-efficiency 搜广推 用户历史与排序骨干 SlimPer固定KB后是否可以每层不再读取长历史？ 不可以，每层仍查询共享原始tokens；省的是逐层更新N个历史状态，计算仍有KN访问。当前短MovieLens、AdamW和解析元素统计不代表生产长序列QPS或Shampoo实验。 例如KB只有少量槽，也必须再次看原证据，不能把它误写为一次压缩后彻底丢历史。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8b4dfeda1146dd5b">SlimPer固定KB后是否可以每层不再读取长历史？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aslimper">SlimPer: Make Personalization Model Slim and Smart</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Platforms, Inc.</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不可以，每层仍查询共享原始tokens；省的是逐层更新N个历史状态，计算仍有KN访问。当前短MovieLens、AdamW和解析元素统计不代表生产长序列QPS或Shampoo实验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如KB只有少量槽，也必须再次看原证据，不能把它误写为一次压缩后彻底丢历史。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.12281">原论文</a> · <a href="../../../../reproductions/2607.12281-slimper/">实现解读</a> · <a href="#qa-8b4dfeda1146dd5b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:poem" data-paper-title="POEM: Partial-Order Enhanced Real-Time Sequential Modeling for Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="POEM: Partial-Order Enhanced Real-Time Sequential Modeling for Recommendation 搜广推与 LLM 应用 Kuaishou 2026-06-29 把当前请求多个排序目标产生的相对次序转成偏序信号，动态构造比纯时间序更贴近实时兴趣的训练序列。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 POEM 为 0.05009，相对变化 -7.25%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  sequential-recommendation partial-order real-time 搜广推 用户历史与排序骨干 POEM 使用的“名次”与 CTR、GMV 原始数值有何区别？ 名次保留同一目标内谁排前谁排后，不保留原始量纲和差距大小，因此可将不同目标的相对顺序转成比较证据。它也会丢失价值幅度：一元和百元的差别不能仅由先后表示。理解这个信息损失，才不会把偏序信号当作所有目标数值的等价替身。 示意：甲点击率只略高于乙，却交易额低很多，两项名次各提供一个方向；名次本身没有告诉模型“略高”与“低很多”的幅度差异。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-poem-c8eda543" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ed49350b97afd6ab">POEM 使用的“名次”与 CTR、GMV 原始数值有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apoem">POEM: Partial-Order Enhanced Real-Time Sequential Modeling for Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>名次保留同一目标内谁排前谁排后，不保留原始量纲和差距大小，因此可将不同目标的相对顺序转成比较证据。它也会丢失价值幅度：一元和百元的差别不能仅由先后表示。理解这个信息损失，才不会把偏序信号当作所有目标数值的等价替身。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>甲点击率只略高于乙，却交易额低很多，两项名次各提供一个方向；名次本身没有告诉模型“略高”与“低很多”的幅度差异。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.29946">原论文</a> · <a href="../../../../reproductions/2606.29946-poem/">实现解读</a> · <a href="#qa-ed49350b97afd6ab">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:poem" data-paper-title="POEM: Partial-Order Enhanced Real-Time Sequential Modeling for Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="POEM: Partial-Order Enhanced Real-Time Sequential Modeling for Recommendation 搜广推与 LLM 应用 Kuaishou 2026-06-29 把当前请求多个排序目标产生的相对次序转成偏序信号，动态构造比纯时间序更贴近实时兴趣的训练序列。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 POEM 为 0.05009，相对变化 -7.25%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  sequential-recommendation partial-order real-time 搜广推 用户历史与排序骨干 POEM 为什么把当前请求多个目标的相对次序变成偏序，而不只按历史时间排训练序列？ 时间顺序描述事件发生先后，不一定描述当前请求最在意的候选关系。POEM 汇总多个目标对候选的相对排序，构造反映请求偏好的偏序信号，再据此组织训练。多目标分歧可保留为不完全确定的关系；它借用的是已有目标的判断，不能被当作独立、无偏的真实用户偏好。 示意：两个商品先后被浏览，但当前点击和购买模型都更偏好后者。偏序信号可以表达“后者在本请求更优”，而不是强迫模型把浏览时间先后当成偏好强弱。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-47020eb5235815f6">POEM 为什么把当前请求多个目标的相对次序变成偏序，而不只按历史时间排训练序列？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apoem">POEM: Partial-Order Enhanced Real-Time Sequential Modeling for Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>时间顺序描述事件发生先后，不一定描述当前请求最在意的候选关系。POEM 汇总多个目标对候选的相对排序，构造反映请求偏好的偏序信号，再据此组织训练。多目标分歧可保留为不完全确定的关系；它借用的是已有目标的判断，不能被当作独立、无偏的真实用户偏好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个商品先后被浏览，但当前点击和购买模型都更偏好后者。偏序信号可以表达“后者在本请求更优”，而不是强迫模型把浏览时间先后当成偏好强弱。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.29946">原论文</a> · <a href="../../../../reproductions/2606.29946-poem/">实现解读</a> · <a href="#qa-47020eb5235815f6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:poem" data-paper-title="POEM: Partial-Order Enhanced Real-Time Sequential Modeling for Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="POEM: Partial-Order Enhanced Real-Time Sequential Modeling for Recommendation 搜广推与 LLM 应用 Kuaishou 2026-06-29 把当前请求多个排序目标产生的相对次序转成偏序信号，动态构造比纯时间序更贴近实时兴趣的训练序列。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 POEM 为 0.05009，相对变化 -7.25%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  sequential-recommendation partial-order real-time 搜广推 用户历史与排序骨干 POEM 的多数目标比较与保留所有冲突证据，相比会丢什么信息？ 多数规则将多个目标压成一条方向，便于构序列，却可能丢掉少数任务强烈反对与差距大小。不同于同时保留正反证据的目标，偏序关注总体次序。此处只是机制取舍，不能借另一论文实验断言谁在所有场景更好。 示意：三项轻微支持甲、两项很强支持乙，多数仍判甲；它简洁表达方向，却不说明金额幅度或购买目标的强反对。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-2b4709f97e0a86d4">POEM 的多数目标比较与保留所有冲突证据，相比会丢什么信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apoem">POEM: Partial-Order Enhanced Real-Time Sequential Modeling for Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多数规则将多个目标压成一条方向，便于构序列，却可能丢掉少数任务强烈反对与差距大小。不同于同时保留正反证据的目标，偏序关注总体次序。此处只是机制取舍，不能借另一论文实验断言谁在所有场景更好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三项轻微支持甲、两项很强支持乙，多数仍判甲；它简洁表达方向，却不说明金额幅度或购买目标的强反对。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.29946">原论文</a> · <a href="../../../../reproductions/2606.29946-poem/">实现解读</a> · <a href="#qa-2b4709f97e0a86d4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:poem" data-paper-title="POEM: Partial-Order Enhanced Real-Time Sequential Modeling for Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="POEM: Partial-Order Enhanced Real-Time Sequential Modeling for Recommendation 搜广推与 LLM 应用 Kuaishou 2026-06-29 把当前请求多个排序目标产生的相对次序转成偏序信号，动态构造比纯时间序更贴近实时兴趣的训练序列。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 POEM 为 0.05009，相对变化 -7.25%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  sequential-recommendation partial-order real-time 搜广推 用户历史与排序骨干 POEM 的两两多数关系为什么需要检查平局或循环，而不能当作天然总序？ 多目标偏好可能出现甲胜乙、乙胜丙、丙胜甲，平局也无唯一方向。若最终构序列，要遵循定义的稳定处理，不能悄悄排序成任意结果再声称原偏序保留。测试标签不能用于打破循环选择最有利答案。 示意：三个目标各支持不同排列可形成循环；直接按 item ID 拆解虽可运行，却是额外规则，应记录而非称所有候选都有一致真实顺序。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-54078c13921f4ddf">POEM 的两两多数关系为什么需要检查平局或循环，而不能当作天然总序？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apoem">POEM: Partial-Order Enhanced Real-Time Sequential Modeling for Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多目标偏好可能出现甲胜乙、乙胜丙、丙胜甲，平局也无唯一方向。若最终构序列，要遵循定义的稳定处理，不能悄悄排序成任意结果再声称原偏序保留。测试标签不能用于打破循环选择最有利答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三个目标各支持不同排列可形成循环；直接按 item ID 拆解虽可运行，却是额外规则，应记录而非称所有候选都有一致真实顺序。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.29946">原论文</a> · <a href="../../../../reproductions/2606.29946-poem/">实现解读</a> · <a href="#qa-54078c13921f4ddf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cmsl" data-paper-title="CMSL: Constructive Multi-Sequence Learning for Recommendation Systems" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="CMSL: Constructive Multi-Sequence Learning for Recommendation Systems 搜广推与 LLM 应用 Meta 2026-06-26 把点击、观看、互动等所有行为塞进单一长序列会混合多个意图，且 self-attention 成本随长度快速增长。CMSL 不依赖预定义业务 taxonomy，而是利用当前上下文特征学习多个 contextual lens，把原始历史动态构造成 K 条 latent semantic sequence；每条 strand 独立编码，再用当前非序列上下文作为 query 做 PMA 聚合。论文还给出 degree-2 polynomial feature map 的线性 HSTU 近似，以支持工业长序列。 Fidelity: 核心机制复现。当前实现让 contextual lenses、软序列构造和 HSTU-style gated attention 一起反向传播；未复刻 Meta 私有特征、规模和分布式 serving。本地对照口径：基线与实验组共享 embedding、HSTU block、优化器和训练预算；实验组仅增加 6 个 learned contextual lenses 和多 strand 聚合，NDCG@10 +29.42%，不是相对 DIN。   搜广推 用户历史与排序骨干 CMSL 的 contextual lens 为什么要以当前非序列上下文为条件？ 同一历史包含多种潜在意图，当前场景决定哪些事件应共同解释。lens 依上下文对事件软分配，形成多条语义 strand，再由上下文查询聚合，避免固定业务类型分桶忽略细分需求。软路由并不保证分出人类预想的主题，需要检查是否发生重复或坍缩。 示意：同一购物历史在旅行场景可分出轻便装备，在居家场景强调收纳；若只按点击或购买分组，两种需求仍会混在每组里。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-cmsl-b229ccb6" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-eff0ba3837f4f0a0">CMSL 的 contextual lens 为什么要以当前非序列上下文为条件？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acmsl">CMSL: Constructive Multi-Sequence Learning for Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一历史包含多种潜在意图，当前场景决定哪些事件应共同解释。lens 依上下文对事件软分配，形成多条语义 strand，再由上下文查询聚合，避免固定业务类型分桶忽略细分需求。软路由并不保证分出人类预想的主题，需要检查是否发生重复或坍缩。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一购物历史在旅行场景可分出轻便装备，在居家场景强调收纳；若只按点击或购买分组，两种需求仍会混在每组里。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.28533">原论文</a> · <a href="../../../../reproductions/2606.28533-cmsl/">实现解读</a> · <a href="#qa-eff0ba3837f4f0a0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cmsl" data-paper-title="CMSL: Constructive Multi-Sequence Learning for Recommendation Systems" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="CMSL: Constructive Multi-Sequence Learning for Recommendation Systems 搜广推与 LLM 应用 Meta 2026-06-26 把点击、观看、互动等所有行为塞进单一长序列会混合多个意图，且 self-attention 成本随长度快速增长。CMSL 不依赖预定义业务 taxonomy，而是利用当前上下文特征学习多个 contextual lens，把原始历史动态构造成 K 条 latent semantic sequence；每条 strand 独立编码，再用当前非序列上下文作为 query 做 PMA 聚合。论文还给出 degree-2 polynomial feature map 的线性 HSTU 近似，以支持工业长序列。 Fidelity: 核心机制复现。当前实现让 contextual lenses、软序列构造和 HSTU-style gated attention 一起反向传播；未复刻 Meta 私有特征、规模和分布式 serving。本地对照口径：基线与实验组共享 embedding、HSTU block、优化器和训练预算；实验组仅增加 6 个 learned contextual lenses 和多 strand 聚合，NDCG@10 +29.42%，不是相对 DIN。   搜广推 用户历史与排序骨干 CMSL的contextual lens为什么不是预先按点击、购买等行为类型分桶？ 固定业务分桶未必对应用户当下的潜在意图。CMSL根据事件和当前上下文学习软分配，让同一历史形成多个语义strand，各自编码后再按非序列上下文聚合。它把兴趣拆分和场景选择都变成可学习过程；软分配不保证天然互补，仍需检查不同strand是否重复或失去有效历史。 示意：一次厨房用品点击既可能属于日常补货，也可能属于搬家准备；上下文不同，事件可被不同lens赋权，而不必永远留在同一个点击桶里。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-89f711951fa492ec">CMSL的contextual lens为什么不是预先按点击、购买等行为类型分桶？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acmsl">CMSL: Constructive Multi-Sequence Learning for Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定业务分桶未必对应用户当下的潜在意图。CMSL根据事件和当前上下文学习软分配，让同一历史形成多个语义strand，各自编码后再按非序列上下文聚合。它把兴趣拆分和场景选择都变成可学习过程；软分配不保证天然互补，仍需检查不同strand是否重复或失去有效历史。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次厨房用品点击既可能属于日常补货，也可能属于搬家准备；上下文不同，事件可被不同lens赋权，而不必永远留在同一个点击桶里。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.28533">原论文</a> · <a href="../../../../reproductions/2606.28533-cmsl/">实现解读</a> · <a href="#qa-89f711951fa492ec">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cmsl" data-paper-title="CMSL: Constructive Multi-Sequence Learning for Recommendation Systems" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="CMSL: Constructive Multi-Sequence Learning for Recommendation Systems 搜广推与 LLM 应用 Meta 2026-06-26 把点击、观看、互动等所有行为塞进单一长序列会混合多个意图，且 self-attention 成本随长度快速增长。CMSL 不依赖预定义业务 taxonomy，而是利用当前上下文特征学习多个 contextual lens，把原始历史动态构造成 K 条 latent semantic sequence；每条 strand 独立编码，再用当前非序列上下文作为 query 做 PMA 聚合。论文还给出 degree-2 polynomial feature map 的线性 HSTU 近似，以支持工业长序列。 Fidelity: 核心机制复现。当前实现让 contextual lenses、软序列构造和 HSTU-style gated attention 一起反向传播；未复刻 Meta 私有特征、规模和分布式 serving。本地对照口径：基线与实验组共享 embedding、HSTU block、优化器和训练预算；实验组仅增加 6 个 learned contextual lenses 和多 strand 聚合，NDCG@10 +29.42%，不是相对 DIN。   搜广推 用户历史与排序骨干 CMSL 多 strand 与简单增加多个 attention head，有何组织差别？ 多头在同一输入序列上投影不同子空间，contextual lens 先按上下文改变事件分组或权重，构造不同潜在序列再编码。两者都可多视角，但分工发生的位置不同。来源的线性 HSTU 是特定核近似，不能从使用 strand 推出标准 HSTU 自动线性。 示意：多头像多人读同一本未分类账本，lens 先按当前任务把账目重组为几册再读；每册仍需有合适编码，不能仅靠册数增多获得信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-829930983eb478a2">CMSL 多 strand 与简单增加多个 attention head，有何组织差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acmsl">CMSL: Constructive Multi-Sequence Learning for Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多头在同一输入序列上投影不同子空间，contextual lens 先按上下文改变事件分组或权重，构造不同潜在序列再编码。两者都可多视角，但分工发生的位置不同。来源的线性 HSTU 是特定核近似，不能从使用 strand 推出标准 HSTU 自动线性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>多头像多人读同一本未分类账本，lens 先按当前任务把账目重组为几册再读；每册仍需有合适编码，不能仅靠册数增多获得信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.28533">原论文</a> · <a href="../../../../reproductions/2606.28533-cmsl/">实现解读</a> · <a href="#qa-829930983eb478a2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cmsl" data-paper-title="CMSL: Constructive Multi-Sequence Learning for Recommendation Systems" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="CMSL: Constructive Multi-Sequence Learning for Recommendation Systems 搜广推与 LLM 应用 Meta 2026-06-26 把点击、观看、互动等所有行为塞进单一长序列会混合多个意图，且 self-attention 成本随长度快速增长。CMSL 不依赖预定义业务 taxonomy，而是利用当前上下文特征学习多个 contextual lens，把原始历史动态构造成 K 条 latent semantic sequence；每条 strand 独立编码，再用当前非序列上下文作为 query 做 PMA 聚合。论文还给出 degree-2 polynomial feature map 的线性 HSTU 近似，以支持工业长序列。 Fidelity: 核心机制复现。当前实现让 contextual lenses、软序列构造和 HSTU-style gated attention 一起反向传播；未复刻 Meta 私有特征、规模和分布式 serving。本地对照口径：基线与实验组共享 embedding、HSTU block、优化器和训练预算；实验组仅增加 6 个 learned contextual lenses 和多 strand 聚合，NDCG@10 +29.42%，不是相对 DIN。   搜广推 用户历史与排序骨干 CMSL 的二阶 feature map 近似为什么需要单独检查宽度成本？ 将 SiLU 点积近似分解后可重排乘法，减少对序列长度的二次依赖；但二阶映射包含交叉项，维度随原特征宽度增长，不能只写线性长度就忽略常数和宽度。来源本地主要验证 learned lenses 与 HSTU-style 路径，生产核应另行核验。 示意：历史从一千到两千可在长度项上近似翻倍，但若特征宽度也翻倍，二阶映射可能扩大更多；总 FLOPs 不能只按历史长度估算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-cac1ed972c28ccb8">CMSL 的二阶 feature map 近似为什么需要单独检查宽度成本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acmsl">CMSL: Constructive Multi-Sequence Learning for Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>将 SiLU 点积近似分解后可重排乘法，减少对序列长度的二次依赖；但二阶映射包含交叉项，维度随原特征宽度增长，不能只写线性长度就忽略常数和宽度。来源本地主要验证 learned lenses 与 HSTU-style 路径，生产核应另行核验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>历史从一千到两千可在长度项上近似翻倍，但若特征宽度也翻倍，二阶映射可能扩大更多；总 FLOPs 不能只按历史长度估算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.28533">原论文</a> · <a href="../../../../reproductions/2606.28533-cmsl/">实现解读</a> · <a href="#qa-cac1ed972c28ccb8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:uniformer" data-paper-title="UniFormer: Efficient and Unified Model-Centric Scaling for Industrial Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="UniFormer: Efficient and Unified Model-Centric Scaling for Industrial Recommendation 搜广推与 LLM 应用 Kuaishou 2026-06-25 把 item-independent/dependent 特征与不同任务拆成语义 token，通过统一交互模块共同扩展序列、特征和任务空间。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 UniFormer 为 0.04131，相对变化 -23.50%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  ranking feature-tokenization multi-task 搜广推 用户历史与排序骨干 UniFormer为什么把特征类型与任务都做成语义token？ 统一交互接口可同时承载候选无关、候选相关与任务状态，扩展序列和任务空间。token化保留不同含义，不是把所有字段无区别拼成一个向量。 例如用户历史、当前商品与点击任务各占对应token。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-uniformer-655acc49" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a1a76d598f2841bc">UniFormer为什么把特征类型与任务都做成语义token？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Auniformer">UniFormer: Efficient and Unified Model-Centric Scaling for Industrial Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>统一交互接口可同时承载候选无关、候选相关与任务状态，扩展序列和任务空间。token化保留不同含义，不是把所有字段无区别拼成一个向量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户历史、当前商品与点击任务各占对应token。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.27058">原论文</a> · <a href="../../../../reproductions/2606.27058-uniformer/">实现解读</a> · <a href="#qa-a1a76d598f2841bc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:uniformer" data-paper-title="UniFormer: Efficient and Unified Model-Centric Scaling for Industrial Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="UniFormer: Efficient and Unified Model-Centric Scaling for Industrial Recommendation 搜广推与 LLM 应用 Kuaishou 2026-06-25 把 item-independent/dependent 特征与不同任务拆成语义 token，通过统一交互模块共同扩展序列、特征和任务空间。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 UniFormer 为 0.04131，相对变化 -23.50%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  ranking feature-tokenization multi-task 搜广推 用户历史与排序骨干 UniFormer 为什么显式区分 item-independent、item-dependent 与 task token 后再统一交互？ 候选无关特征可表达用户公共状态，候选相关特征负责当前匹配，任务 token 指明预测目标。先明确语义角色再交互，有助统一序列、字段与任务的扩展接口，避免把所有输入视为同质字段。统一模块不等于这些状态都能跨候选缓存；一旦发生候选相关信息流，复用边界仍需由掩码和结构保证。 示意：用户年龄属于公共 token，候选价格属于商品相关 token，购买任务另有目标 token。三者可共同建模，但包含某件商品价格的交互状态不能直接复用给另一件商品。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-b79ebda446d84c88">UniFormer 为什么显式区分 item-independent、item-dependent 与 task token 后再统一交互？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Auniformer">UniFormer: Efficient and Unified Model-Centric Scaling for Industrial Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>候选无关特征可表达用户公共状态，候选相关特征负责当前匹配，任务 token 指明预测目标。先明确语义角色再交互，有助统一序列、字段与任务的扩展接口，避免把所有输入视为同质字段。统一模块不等于这些状态都能跨候选缓存；一旦发生候选相关信息流，复用边界仍需由掩码和结构保证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户年龄属于公共 token，候选价格属于商品相关 token，购买任务另有目标 token。三者可共同建模，但包含某件商品价格的交互状态不能直接复用给另一件商品。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.27058">原论文</a> · <a href="../../../../reproductions/2606.27058-uniformer/">实现解读</a> · <a href="#qa-b79ebda446d84c88">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:uniformer" data-paper-title="UniFormer: Efficient and Unified Model-Centric Scaling for Industrial Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="UniFormer: Efficient and Unified Model-Centric Scaling for Industrial Recommendation 搜广推与 LLM 应用 Kuaishou 2026-06-25 把 item-independent/dependent 特征与不同任务拆成语义 token，通过统一交互模块共同扩展序列、特征和任务空间。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 UniFormer 为 0.04131，相对变化 -23.50%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  ranking feature-tokenization multi-task 搜广推 用户历史与排序骨干 统一task token与每任务独立模型有何取舍？ 共享交互利于跨任务信息与维护，任务token表达条件差异，但共享参数仍会有干扰。不能仅因结构统一就推断所有目标都同时变好。 例如观看任务的有用表示可能帮助点击，也可能与交易偏好冲突。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-8301b52622a60f8a">统一task token与每任务独立模型有何取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Auniformer">UniFormer: Efficient and Unified Model-Centric Scaling for Industrial Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共享交互利于跨任务信息与维护，任务token表达条件差异，但共享参数仍会有干扰。不能仅因结构统一就推断所有目标都同时变好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如观看任务的有用表示可能帮助点击，也可能与交易偏好冲突。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.27058">原论文</a> · <a href="../../../../reproductions/2606.27058-uniformer/">实现解读</a> · <a href="#qa-8301b52622a60f8a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:uniformer" data-paper-title="UniFormer: Efficient and Unified Model-Centric Scaling for Industrial Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="UniFormer: Efficient and Unified Model-Centric Scaling for Industrial Recommendation 搜广推与 LLM 应用 Kuaishou 2026-06-25 把 item-independent/dependent 特征与不同任务拆成语义 token，通过统一交互模块共同扩展序列、特征和任务空间。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 UniFormer 为 0.04131，相对变化 -23.50%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  ranking feature-tokenization multi-task 搜广推 用户历史与排序骨干 UniFormer本地如何避免任务或候选特征错位？ token类型、位置和有效mask需与输入字段一一对应，任务头读其对应状态。公开MovieLens代理没有工业多场景字段和serving，不把小scale结果写成完整生产扩展。 例如任务A头误读任务B token，形状虽对但学习目标已错。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-52f840ed13b3837f">UniFormer本地如何避免任务或候选特征错位？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Auniformer">UniFormer: Efficient and Unified Model-Centric Scaling for Industrial Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>token类型、位置和有效mask需与输入字段一一对应，任务头读其对应状态。公开MovieLens代理没有工业多场景字段和serving，不把小scale结果写成完整生产扩展。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如任务A头误读任务B token，形状虽对但学习目标已错。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.27058">原论文</a> · <a href="../../../../reproductions/2606.27058-uniformer/">实现解读</a> · <a href="#qa-52f840ed13b3837f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:journeyformer" data-paper-title="JourneyFormer: Encoding Airbnb Guest Journey with Sequence Modeling" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="JourneyFormer: Encoding Airbnb Guest Journey with Sequence Modeling 搜广推与 LLM 应用 Airbnb 2026-06-17 统一编码 Airbnb 长期和短期 guest journey，以事件类型、时间和 listing 表示构建序列，并通过缓存和稀疏计算满足线上时延。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  search-ranking sequence-modeling long-sequence 搜广推 用户历史与排序骨干 JourneyFormer 为什么编码 guest journey，而非只保留已浏览 listing 集合？ 搜索、查看、收藏和预订等事件代表旅程不同阶段，时间间隔也影响需求是否仍有效。类型与时间嵌入让同一房源在不同路径中有不同含义，长期短期共同建模。事件标注不等于因果解释，历史完成旅程也可能与当前需求不同。 示意：三个月前已预订的海边房源与今天刚收藏的城市公寓不该同等当作未满足需求；仅存房源集合会丢掉这种状态差别。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-journeyformer-09e3e4a3" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-dbedf876ab0f5949">JourneyFormer 为什么编码 guest journey，而非只保留已浏览 listing 集合？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ajourneyformer">JourneyFormer: Encoding Airbnb Guest Journey with Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Airbnb</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>搜索、查看、收藏和预订等事件代表旅程不同阶段，时间间隔也影响需求是否仍有效。类型与时间嵌入让同一房源在不同路径中有不同含义，长期短期共同建模。事件标注不等于因果解释，历史完成旅程也可能与当前需求不同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三个月前已预订的海边房源与今天刚收藏的城市公寓不该同等当作未满足需求；仅存房源集合会丢掉这种状态差别。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.19108">原论文</a> · <a href="../../../../reproductions/2606.19108-journeyformer/">实现解读</a> · <a href="#qa-dbedf876ab0f5949">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:journeyformer" data-paper-title="JourneyFormer: Encoding Airbnb Guest Journey with Sequence Modeling" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="JourneyFormer: Encoding Airbnb Guest Journey with Sequence Modeling 搜广推与 LLM 应用 Airbnb 2026-06-17 统一编码 Airbnb 长期和短期 guest journey，以事件类型、时间和 listing 表示构建序列，并通过缓存和稀疏计算满足线上时延。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  search-ranking sequence-modeling long-sequence 搜广推 用户历史与排序骨干 JourneyFormer为什么把事件类型与时间编码进guest journey，而不只记录浏览过的房源？ 相同房源出现在搜索、浏览、收藏或预订阶段，表达的决策进展不同；时间间隔又区分同次旅行与较早计划。统一旅程序列让模型学习阶段之间的关联，兼顾长期偏好和短期出行需求。缓存与稀疏计算只减少成本，不能因此忽略每个请求当时可见的事件边界。 示意：用户去年收藏海边房源，今天连续搜索市中心并查看商务公寓；房源ID列表不够区分两次旅行，事件类型和时间能帮助识别当前行程。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-d64a894bfbe04f44">JourneyFormer为什么把事件类型与时间编码进guest journey，而不只记录浏览过的房源？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ajourneyformer">JourneyFormer: Encoding Airbnb Guest Journey with Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Airbnb</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相同房源出现在搜索、浏览、收藏或预订阶段，表达的决策进展不同；时间间隔又区分同次旅行与较早计划。统一旅程序列让模型学习阶段之间的关联，兼顾长期偏好和短期出行需求。缓存与稀疏计算只减少成本，不能因此忽略每个请求当时可见的事件边界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户去年收藏海边房源，今天连续搜索市中心并查看商务公寓；房源ID列表不够区分两次旅行，事件类型和时间能帮助识别当前行程。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.19108">原论文</a> · <a href="../../../../reproductions/2606.19108-journeyformer/">实现解读</a> · <a href="#qa-d64a894bfbe04f44">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:journeyformer" data-paper-title="JourneyFormer: Encoding Airbnb Guest Journey with Sequence Modeling" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="JourneyFormer: Encoding Airbnb Guest Journey with Sequence Modeling 搜广推与 LLM 应用 Airbnb 2026-06-17 统一编码 Airbnb 长期和短期 guest journey，以事件类型、时间和 listing 表示构建序列，并通过缓存和稀疏计算满足线上时延。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  search-ranking sequence-modeling long-sequence 搜广推 用户历史与排序骨干 统一长短 journey 与只看最近窗口，相比多保留什么又多承担什么？ 长历史保留稳定目的地与住宿偏好，短窗口反映当前旅行阶段；统一编码可能联系两者，却增加注意力与更新成本，需缓存和稀疏策略。旧旅行也可能过时，更多历史不自动更准，来源本地负结果只能限定代理任务。 示意：长期偏好家庭房但当前商务出差，需要同时保留稳定空间需求与新场景；只看最近可能忘长期偏好，全部旧史等权又可能干扰。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e9c189d7e07fb75f">统一长短 journey 与只看最近窗口，相比多保留什么又多承担什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ajourneyformer">JourneyFormer: Encoding Airbnb Guest Journey with Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Airbnb</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长历史保留稳定目的地与住宿偏好，短窗口反映当前旅行阶段；统一编码可能联系两者，却增加注意力与更新成本，需缓存和稀疏策略。旧旅行也可能过时，更多历史不自动更准，来源本地负结果只能限定代理任务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>长期偏好家庭房但当前商务出差，需要同时保留稳定空间需求与新场景；只看最近可能忘长期偏好，全部旧史等权又可能干扰。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.19108">原论文</a> · <a href="../../../../reproductions/2606.19108-journeyformer/">实现解读</a> · <a href="#qa-e9c189d7e07fb75f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:journeyformer" data-paper-title="JourneyFormer: Encoding Airbnb Guest Journey with Sequence Modeling" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="JourneyFormer: Encoding Airbnb Guest Journey with Sequence Modeling 搜广推与 LLM 应用 Airbnb 2026-06-17 统一编码 Airbnb 长期和短期 guest journey，以事件类型、时间和 listing 表示构建序列，并通过缓存和稀疏计算满足线上时延。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  search-ranking sequence-modeling long-sequence 搜广推 用户历史与排序骨干 JourneyFormer 缓存增量状态时，为什么 listing、event type、time 要同一版本？ 状态由三类信息共同形成，修改事件类型或时间编码会使旧缓存不再对应新输入。因果序列只可包含当时已发生事件，未来预订不能提前成为当前特征。本地未包含真实住宿库存和完整生产刷新系统，不能据代理延迟推断线上性能。 示意：把一次查看后改为已预订，原缓存仍将其当探索，会错误继续推荐；只刷新 listing 向量而不更新事件状态不够。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3d6bbeba9e6d3e71">JourneyFormer 缓存增量状态时，为什么 listing、event type、time 要同一版本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ajourneyformer">JourneyFormer: Encoding Airbnb Guest Journey with Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Airbnb</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>状态由三类信息共同形成，修改事件类型或时间编码会使旧缓存不再对应新输入。因果序列只可包含当时已发生事件，未来预订不能提前成为当前特征。本地未包含真实住宿库存和完整生产刷新系统，不能据代理延迟推断线上性能。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把一次查看后改为已预订，原缓存仍将其当探索，会错误继续推荐；只刷新 listing 向量而不更新事件状态不够。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.19108">原论文</a> · <a href="../../../../reproductions/2606.19108-journeyformer/">实现解读</a> · <a href="#qa-3d6bbeba9e6d3e71">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onerank" data-paper-title="OneRank: Unified Transformer-Native Ranking Architecture for Multi-Task Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OneRank: Unified Transformer-Native Ranking Architecture for Multi-Task Recommendation 搜广推与 LLM 应用 Renmin University of China 2026-06-15 取消 encoder 与 task predictor 的割裂，把结构化特征和任务 token 放进统一序列，并用 task-private channel 与梯度隔离控制任务冲突。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 OneRank 为 0.09540，相对变化 +76.65%。这是公开代理任务上的机制结果，生产线上 lift 的外推不适用。  ranking multi-task transformer 搜广推 用户历史与排序骨干 OneRank 的 task token 为什么进入统一编码，而不是只控制最后输出头？ 任务条件在层内参与特征解释，允许同一结构字段为不同目标形成不同上下文，减少 encoder 与 predictor 割裂。私有通道仍保留差异，统一不等于所有参数对全部任务共享。任务 token 存在本身也不保证模型实际使用它。 示意：购买任务可在中间层更关注预算，点击任务更关注新鲜感；若只最后换头，两者先前读到的是同一已压缩表示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-onerank-a08d1448" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-584c43bca671b73a">OneRank 的 task token 为什么进入统一编码，而不是只控制最后输出头？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonerank">OneRank: Unified Transformer-Native Ranking Architecture for Multi-Task Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Renmin University of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>任务条件在层内参与特征解释，允许同一结构字段为不同目标形成不同上下文，减少 encoder 与 predictor 割裂。私有通道仍保留差异，统一不等于所有参数对全部任务共享。任务 token 存在本身也不保证模型实际使用它。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>购买任务可在中间层更关注预算，点击任务更关注新鲜感；若只最后换头，两者先前读到的是同一已压缩表示。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.16838">原论文</a> · <a href="../../../../reproductions/2606.16838-onerank/">实现解读</a> · <a href="#qa-584c43bca671b73a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onerank" data-paper-title="OneRank: Unified Transformer-Native Ranking Architecture for Multi-Task Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OneRank: Unified Transformer-Native Ranking Architecture for Multi-Task Recommendation 搜广推与 LLM 应用 Renmin University of China 2026-06-15 取消 encoder 与 task predictor 的割裂，把结构化特征和任务 token 放进统一序列，并用 task-private channel 与梯度隔离控制任务冲突。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 OneRank 为 0.09540，相对变化 +76.65%。这是公开代理任务上的机制结果，生产线上 lift 的外推不适用。  ranking multi-task transformer 搜广推 用户历史与排序骨干 OneRank 为什么在统一序列里保留 task-private channel，并隔离其他任务对它的梯度？ 任务 token 能让共享主干感知要预测什么，但所有参数仍共享时，冲突目标会争夺同一表示。私有通道为每个任务保留专属容量，梯度隔离保证其他任务损失不会直接改写该部分。统一输入负责共享信息，私有通道负责差异；它控制冲突的路径，而不是假设不同任务的最优表示完全一致。 示意：点击任务偏重新颖，购买任务偏重可靠。两者共用商品与用户序列，但点击损失不能直接更新购买私有通道，让购买相关的细分特征不被另一目标覆盖。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-1cd8516d4afdddcd">OneRank 为什么在统一序列里保留 task-private channel，并隔离其他任务对它的梯度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonerank">OneRank: Unified Transformer-Native Ranking Architecture for Multi-Task Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Renmin University of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>任务 token 能让共享主干感知要预测什么，但所有参数仍共享时，冲突目标会争夺同一表示。私有通道为每个任务保留专属容量，梯度隔离保证其他任务损失不会直接改写该部分。统一输入负责共享信息，私有通道负责差异；它控制冲突的路径，而不是假设不同任务的最优表示完全一致。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>点击任务偏重新颖，购买任务偏重可靠。两者共用商品与用户序列，但点击损失不能直接更新购买私有通道，让购买相关的细分特征不被另一目标覆盖。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.16838">原论文</a> · <a href="../../../../reproductions/2606.16838-onerank/">实现解读</a> · <a href="#qa-1cd8516d4afdddcd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onerank" data-paper-title="OneRank: Unified Transformer-Native Ranking Architecture for Multi-Task Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OneRank: Unified Transformer-Native Ranking Architecture for Multi-Task Recommendation 搜广推与 LLM 应用 Renmin University of China 2026-06-15 取消 encoder 与 task predictor 的割裂，把结构化特征和任务 token 放进统一序列，并用 task-private channel 与梯度隔离控制任务冲突。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 OneRank 为 0.09540，相对变化 +76.65%。这是公开代理任务上的机制结果，生产线上 lift 的外推不适用。  ranking multi-task transformer 搜广推 用户历史与排序骨干 OneRank 的 task-private channel 与 MMoE 的 task-specific gate，隔离对象有何不同？ gate 决定如何混合共享专家，私有通道直接保留特定任务参数并限制其他任务梯度，保护路径不同。两者都可共享知识但不能互称完全独立。机制比较不支持普遍效果排序，来源公开代理也不能证明工业多任务负迁移已全解决。 示意：购买 gate 只调共享专家比例，专家仍受点击更新；购买私有通道则应不被点击 loss 改写，二者保护强度与容量位置不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-3b19d5509abeb544">OneRank 的 task-private channel 与 MMoE 的 task-specific gate，隔离对象有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonerank">OneRank: Unified Transformer-Native Ranking Architecture for Multi-Task Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Renmin University of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>gate 决定如何混合共享专家，私有通道直接保留特定任务参数并限制其他任务梯度，保护路径不同。两者都可共享知识但不能互称完全独立。机制比较不支持普遍效果排序，来源公开代理也不能证明工业多任务负迁移已全解决。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>购买 gate 只调共享专家比例，专家仍受点击更新；购买私有通道则应不被点击 loss 改写，二者保护强度与容量位置不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.16838">原论文</a> · <a href="../../../../reproductions/2606.16838-onerank/">实现解读</a> · <a href="#qa-3b19d5509abeb544">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onerank" data-paper-title="OneRank: Unified Transformer-Native Ranking Architecture for Multi-Task Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OneRank: Unified Transformer-Native Ranking Architecture for Multi-Task Recommendation 搜广推与 LLM 应用 Renmin University of China 2026-06-15 取消 encoder 与 task predictor 的割裂，把结构化特征和任务 token 放进统一序列，并用 task-private channel 与梯度隔离控制任务冲突。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 OneRank 为 0.09540，相对变化 +76.65%。这是公开代理任务上的机制结果，生产线上 lift 的外推不适用。  ranking multi-task transformer 搜广推 用户历史与排序骨干 OneRank 怎样检查 Lj 不会更新别人的 φk，又不误冻全部共享 θ？ 对单一任务 loss 反传时，其他任务私有参数梯度应为零，本任务私有与允许共享参数仍可有梯度。只把整个 backbone detach 会失去共同学习；只断输出头又可能没隔离私有内部路径。参数组与任务身份需一一对应。 示意：只训练点击时，购买私有通道不变而共享字段层可更新；若共享层也全零，代码虽然安全隔离，却变成了另一种冻结适配方案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-985fc19979a70550">OneRank 怎样检查 Lj 不会更新别人的 φk，又不误冻全部共享 θ？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonerank">OneRank: Unified Transformer-Native Ranking Architecture for Multi-Task Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Renmin University of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>对单一任务 loss 反传时，其他任务私有参数梯度应为零，本任务私有与允许共享参数仍可有梯度。只把整个 backbone detach 会失去共同学习；只断输出头又可能没隔离私有内部路径。参数组与任务身份需一一对应。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>只训练点击时，购买私有通道不变而共享字段层可更新；若共享层也全零，代码虽然安全隔离，却变成了另一种冻结适配方案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.16838">原论文</a> · <a href="../../../../reproductions/2606.16838-onerank/">实现解读</a> · <a href="#qa-985fc19979a70550">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:memento" data-paper-title="Memento: Personalized RAG-Style Long-Retention Data Scaling for Online Ads Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Memento: Personalized RAG-Style Long-Retention Data Scaling for Online Ads Recommendation 搜广推与 LLM 应用 Meta 2026-05-22 工业推荐模型通常只保留有限长度历史，长期但相关的行为被截断；训练数据也会因一次 SGD 后被“忘记”。Memento 将 RAG 思想分成两条路径：Representation Memento 从最长 365 天用户历史 embedding 库检索与当前 query 相关且互不冗余的事件，再用 Ember 条件变换融入主模型；Data Memento 从历史训练样本库检索被当前模型遗忘、但与当前 batch 有关的样本做第二次 replay。 未复现 Ember、INT8 检索服务与 Data Memento replay。Fidelity: 核心机制复现。query-conditioned MMR 长历史检索实际执行；Meta 私有 Ember、replay 与 INT8 serving 未复刻。本地对照口径：基线是 LastN 历史截断；实验组是 query-conditioned Memento MMR；NDCG@10 从 0.0443 升至 0.0464（+4.78%）。这是历史检索策略消融，不是相对 DIN。   搜广推 用户历史与排序骨干 Representation Memento 与 Data Memento 为什么是两种不同记忆库？ 前者检索用户长期行为证据供当前预测读取，后者找模型已遗忘且与当前 batch 相关的旧训练样本再次更新参数。一个补输入覆盖，一个补训练记忆，存储、更新和评估位置都不同，不能实现其一就声称两路闭环都完成。 示意：找回一年前摄影浏览用于今天推荐是表征记忆；重放旧训练样本防止模型忘某类用户，则是参数学习层面的数据记忆。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-memento-1c9d9291" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-91698d7766f5d11a">Representation Memento 与 Data Memento 为什么是两种不同记忆库？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amemento">Memento: Personalized RAG-Style Long-Retention Data Scaling for Online Ads Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者检索用户长期行为证据供当前预测读取，后者找模型已遗忘且与当前 batch 相关的旧训练样本再次更新参数。一个补输入覆盖，一个补训练记忆，存储、更新和评估位置都不同，不能实现其一就声称两路闭环都完成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>找回一年前摄影浏览用于今天推荐是表征记忆；重放旧训练样本防止模型忘某类用户，则是参数学习层面的数据记忆。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.24051">原论文</a> · <a href="../../../../reproductions/2605.24051-memento/">实现解读</a> · <a href="#qa-91698d7766f5d11a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:memento" data-paper-title="Memento: Personalized RAG-Style Long-Retention Data Scaling for Online Ads Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Memento: Personalized RAG-Style Long-Retention Data Scaling for Online Ads Recommendation 搜广推与 LLM 应用 Meta 2026-05-22 工业推荐模型通常只保留有限长度历史，长期但相关的行为被截断；训练数据也会因一次 SGD 后被“忘记”。Memento 将 RAG 思想分成两条路径：Representation Memento 从最长 365 天用户历史 embedding 库检索与当前 query 相关且互不冗余的事件，再用 Ember 条件变换融入主模型；Data Memento 从历史训练样本库检索被当前模型遗忘、但与当前 batch 有关的样本做第二次 replay。 未复现 Ember、INT8 检索服务与 Data Memento replay。Fidelity: 核心机制复现。query-conditioned MMR 长历史检索实际执行；Meta 私有 Ember、replay 与 INT8 serving 未复刻。本地对照口径：基线是 LastN 历史截断；实验组是 query-conditioned Memento MMR；NDCG@10 从 0.0443 升至 0.0464（+4.78%）。这是历史检索策略消融，不是相对 DIN。   搜广推 用户历史与排序骨干 Memento的Representation路径和Data replay路径分别在挽救哪种遗忘？ 历史截断让推理时缺少远期兴趣，Representation路径检索相关且不冗余的事件并条件化融入模型。训练样本只用一次则可能被参数更新遗忘，Data路径回放与当前batch有关的旧样本。一个补输入证据，一个补训练经验，不能把只实现历史检索的本地结果说成两种记忆都已验证。 示意：一年前的摄影兴趣从输入窗口消失，可检索回来；模型曾学过但后来淡化的冷门类别，则需要训练回放。把旧向量塞进当前输入并不等于重新学过旧样本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-b1cdd545af184e84">Memento的Representation路径和Data replay路径分别在挽救哪种遗忘？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amemento">Memento: Personalized RAG-Style Long-Retention Data Scaling for Online Ads Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>历史截断让推理时缺少远期兴趣，Representation路径检索相关且不冗余的事件并条件化融入模型。训练样本只用一次则可能被参数更新遗忘，Data路径回放与当前batch有关的旧样本。一个补输入证据，一个补训练经验，不能把只实现历史检索的本地结果说成两种记忆都已验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一年前的摄影兴趣从输入窗口消失，可检索回来；模型曾学过但后来淡化的冷门类别，则需要训练回放。把旧向量塞进当前输入并不等于重新学过旧样本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.24051">原论文</a> · <a href="../../../../reproductions/2605.24051-memento/">实现解读</a> · <a href="#qa-b1cdd545af184e84">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:memento" data-paper-title="Memento: Personalized RAG-Style Long-Retention Data Scaling for Online Ads Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Memento: Personalized RAG-Style Long-Retention Data Scaling for Online Ads Recommendation 搜广推与 LLM 应用 Meta 2026-05-22 工业推荐模型通常只保留有限长度历史，长期但相关的行为被截断；训练数据也会因一次 SGD 后被“忘记”。Memento 将 RAG 思想分成两条路径：Representation Memento 从最长 365 天用户历史 embedding 库检索与当前 query 相关且互不冗余的事件，再用 Ember 条件变换融入主模型；Data Memento 从历史训练样本库检索被当前模型遗忘、但与当前 batch 有关的样本做第二次 replay。 未复现 Ember、INT8 检索服务与 Data Memento replay。Fidelity: 核心机制复现。query-conditioned MMR 长历史检索实际执行；Meta 私有 Ember、replay 与 INT8 serving 未复刻。本地对照口径：基线是 LastN 历史截断；实验组是 query-conditioned Memento MMR；NDCG@10 从 0.0443 升至 0.0464（+4.78%）。这是历史检索策略消融，不是相对 DIN。   搜广推 用户历史与排序骨干 Memento 的 query-conditioned MMR 与 LastN，相比相关和冗余如何取舍？ LastN 按时间取固定近邻，MMR 选择与当前 query 相关且与已选记录不过度重复的历史，可召回远期不同证据。它也可能受 query 表示错误影响，λ 决定相关性与覆盖。来源本地只验证该检索策略，不含 Ember 或 Data replay。 示意：最近十条都在看同一镜头，MMR 可保留一条镜头并找更早相机用途记录；但若候选 query 不准，也可能选错远期内容。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b0af300afefe60c1">Memento 的 query-conditioned MMR 与 LastN，相比相关和冗余如何取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amemento">Memento: Personalized RAG-Style Long-Retention Data Scaling for Online Ads Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>LastN 按时间取固定近邻，MMR 选择与当前 query 相关且与已选记录不过度重复的历史，可召回远期不同证据。它也可能受 query 表示错误影响，λ 决定相关性与覆盖。来源本地只验证该检索策略，不含 Ember 或 Data replay。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>最近十条都在看同一镜头，MMR 可保留一条镜头并找更早相机用途记录；但若候选 query 不准，也可能选错远期内容。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.24051">原论文</a> · <a href="../../../../reproductions/2605.24051-memento/">实现解读</a> · <a href="#qa-b0af300afefe60c1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:memento" data-paper-title="Memento: Personalized RAG-Style Long-Retention Data Scaling for Online Ads Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Memento: Personalized RAG-Style Long-Retention Data Scaling for Online Ads Recommendation 搜广推与 LLM 应用 Meta 2026-05-22 工业推荐模型通常只保留有限长度历史，长期但相关的行为被截断；训练数据也会因一次 SGD 后被“忘记”。Memento 将 RAG 思想分成两条路径：Representation Memento 从最长 365 天用户历史 embedding 库检索与当前 query 相关且互不冗余的事件，再用 Ember 条件变换融入主模型；Data Memento 从历史训练样本库检索被当前模型遗忘、但与当前 batch 有关的样本做第二次 replay。 未复现 Ember、INT8 检索服务与 Data Memento replay。Fidelity: 核心机制复现。query-conditioned MMR 长历史检索实际执行；Meta 私有 Ember、replay 与 INT8 serving 未复刻。本地对照口径：基线是 LastN 历史截断；实验组是 query-conditioned Memento MMR；NDCG@10 从 0.0443 升至 0.0464（+4.78%）。这是历史检索策略消融，不是相对 DIN。   搜广推 用户历史与排序骨干 Memento 本地指标为什么不能验证 Ember 条件变换与 Data replay？ 来源只执行 Representation Memento 的 MMR，未复现 Ember affine/quadratic、生产检索及历史样本重放。需要分别看到条件参数学习、实际 replay 更新和对应对照才可扩展声明。λ 由验证选，不能用 test 最佳检索权重补齐证据。 示意：成功检回旧摄影事件并提高 NDCG，说明输入证据有用；没有重放训练样本的优化步，就不能说已解决 SGD 后的遗忘。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e6291b49903b2a5c">Memento 本地指标为什么不能验证 Ember 条件变换与 Data replay？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amemento">Memento: Personalized RAG-Style Long-Retention Data Scaling for Online Ads Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>来源只执行 Representation Memento 的 MMR，未复现 Ember affine/quadratic、生产检索及历史样本重放。需要分别看到条件参数学习、实际 replay 更新和对应对照才可扩展声明。λ 由验证选，不能用 test 最佳检索权重补齐证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>成功检回旧摄影事件并提高 NDCG，说明输入证据有用；没有重放训练样本的优化步，就不能说已解决 SGD 后的遗忘。</p>
<p class="ar-learning-sources">依据：本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.24051">原论文</a> · <a href="../../../../reproductions/2605.24051-memento/">实现解读</a> · <a href="#qa-e6291b49903b2a5c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tubifm" data-paper-title="TubiFM: Unified Item, Carousel, and Search Ranking for Streaming Discovery" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TubiFM: Unified Item, Carousel, and Search Ranking for Streaming Discovery 搜广推与 LLM 应用 Tubi 2026-05-22 以统一 user story 序列描述跨页面旅程，同一个生成式 foundation model 通过任务提示完成 item、carousel 与 search 三种排序。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  foundation-model multi-task-learning search-ranking 搜广推 用户历史与排序骨干 TubiFM为什么把跨页面旅程序列化为user story？ 用户在item、carousel与search间行为相关，统一历史和任务提示让单模型共享信息，又能按任务输出排序。不同任务目标仍需明确，不是所有页面一套无条件分。 例如先搜索后浏览栏目，这段旅程可帮助解释当前选片需求。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-tubifm-2a9a268d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4b28124dc59a54c0">TubiFM为什么把跨页面旅程序列化为user story？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atubifm">TubiFM: Unified Item, Carousel, and Search Ranking for Streaming Discovery</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tubi</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用户在item、carousel与search间行为相关，统一历史和任务提示让单模型共享信息，又能按任务输出排序。不同任务目标仍需明确，不是所有页面一套无条件分。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先搜索后浏览栏目，这段旅程可帮助解释当前选片需求。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.23702">原论文</a> · <a href="../../../../reproductions/2605.23702-tubifm/">实现解读</a> · <a href="#qa-4b28124dc59a54c0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tubifm" data-paper-title="TubiFM: Unified Item, Carousel, and Search Ranking for Streaming Discovery" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TubiFM: Unified Item, Carousel, and Search Ranking for Streaming Discovery 搜广推与 LLM 应用 Tubi 2026-05-22 以统一 user story 序列描述跨页面旅程，同一个生成式 foundation model 通过任务提示完成 item、carousel 与 search 三种排序。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  foundation-model multi-task-learning search-ranking 搜广推 用户历史与排序骨干 TubiFM 为什么用统一 user story 描述跨页面旅程，再以任务提示区分 item、carousel 与 search？ 分散页面模型容易各自截取局部行为，难以连接用户旅程。统一序列把不同页面事件放入同一上下文，任务提示再告诉生成式模型当前评分对象和目标，让共享知识服务不同入口。统一输入格式并不意味着所有页面目标相同，也不自动解决不同候选类型的校准，本地核心代理只验证接口层面的机制。 示意：用户先搜索悬疑片，再在专题轮播中浏览，最后点进具体电影。用同一旅程序列建模后，任务提示决定此刻排序的是电影、专题栏还是搜索结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-23cac2c087366ab8">TubiFM 为什么用统一 user story 描述跨页面旅程，再以任务提示区分 item、carousel 与 search？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atubifm">TubiFM: Unified Item, Carousel, and Search Ranking for Streaming Discovery</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tubi</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分散页面模型容易各自截取局部行为，难以连接用户旅程。统一序列把不同页面事件放入同一上下文，任务提示再告诉生成式模型当前评分对象和目标，让共享知识服务不同入口。统一输入格式并不意味着所有页面目标相同，也不自动解决不同候选类型的校准，本地核心代理只验证接口层面的机制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户先搜索悬疑片，再在专题轮播中浏览，最后点进具体电影。用同一旅程序列建模后，任务提示决定此刻排序的是电影、专题栏还是搜索结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.23702">原论文</a> · <a href="../../../../reproductions/2605.23702-tubifm/">实现解读</a> · <a href="#qa-23cac2c087366ab8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tubifm" data-paper-title="TubiFM: Unified Item, Carousel, and Search Ranking for Streaming Discovery" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TubiFM: Unified Item, Carousel, and Search Ranking for Streaming Discovery 搜广推与 LLM 应用 Tubi 2026-05-22 以统一 user story 序列描述跨页面旅程，同一个生成式 foundation model 通过任务提示完成 item、carousel 与 search 三种排序。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  foundation-model multi-task-learning search-ranking 搜广推 用户历史与排序骨干 统一任务提示模型与各页面独立模型有什么取舍？ 共享可迁移跨页面信号并减少重复维护，也可能出现任务干扰。必须按任务评测和预算比较，不能只因一个模型替三模型就认定各任务都提升。 例如搜索意图很明确，不一定应被首页长期兴趣完全覆盖。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1d95b771a3c778eb">统一任务提示模型与各页面独立模型有什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atubifm">TubiFM: Unified Item, Carousel, and Search Ranking for Streaming Discovery</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tubi</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共享可迁移跨页面信号并减少重复维护，也可能出现任务干扰。必须按任务评测和预算比较，不能只因一个模型替三模型就认定各任务都提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如搜索意图很明确，不一定应被首页长期兴趣完全覆盖。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.23702">原论文</a> · <a href="../../../../reproductions/2605.23702-tubifm/">实现解读</a> · <a href="#qa-1d95b771a3c778eb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tubifm" data-paper-title="TubiFM: Unified Item, Carousel, and Search Ranking for Streaming Discovery" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TubiFM: Unified Item, Carousel, and Search Ranking for Streaming Discovery 搜广推与 LLM 应用 Tubi 2026-05-22 以统一 user story 序列描述跨页面旅程，同一个生成式 foundation model 通过任务提示完成 item、carousel 与 search 三种排序。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  foundation-model multi-task-learning search-ranking 搜广推 用户历史与排序骨干 TubiFM本地任务serialize与生产foundation model怎样区分？ 公开固定候选只验证独立模型状态与任务条件打分，缺少私有特征、生产规模和线上流量。任务token、历史边界与item标签需对齐，不能把同一公式换名当独立实现。 例如三个任务提示必须真正影响执行路径，而非只改日志里的名称。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e0525cf7c7b8ff4c">TubiFM本地任务serialize与生产foundation model怎样区分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atubifm">TubiFM: Unified Item, Carousel, and Search Ranking for Streaming Discovery</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tubi</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>公开固定候选只验证独立模型状态与任务条件打分，缺少私有特征、生产规模和线上流量。任务token、历史边界与item标签需对齐，不能把同一公式换名当独立实现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如三个任务提示必须真正影响执行路径，而非只改日志里的名称。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.23702">原论文</a> · <a href="../../../../reproductions/2605.23702-tubifm/">实现解读</a> · <a href="#qa-e0525cf7c7b8ff4c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:uxsid" data-paper-title="UxSID: Semantic-Aware User Interests Modeling for Ultra-Long Sequence" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="UxSID: Semantic-Aware User Interests Modeling for Ultra-Long Sequence 搜广推与 LLM 应用 Kuaishou 2026-05-09 UxSID 在逐候选检索和完全候选无关的历史压缩之间加入“目标语义组共享记忆”：用目标物品第一层 SID 查询全历史与可学习兴趣锚点，利用全局兴趣门控第二层语义探针。语义相近的候选共享用户兴趣表示，使离线端到端训练与线上按用户/SID 查表使用同一记忆。IAIC 先用可学习锚点对行为序列做交叉注意力，再为每个锚点配置独立 Sigmoid PFFN、残差及 LayerNorm；正交项抑制兴趣坍缩。目标 SID 对原序列取全局响应，并以该响应门控 SID 后查询压缩锚点，最后拼接两级兴趣表示进行监督训练。 一次早期 CPU/seed42/100 用户/1 epoch 诊断中，UxSID test AUC 0.5848，validation 选择的 agnostic 为 0.5916；默认 encoder 是固定版本 Qwen2.5-0.5B-Instruct 7ae557604adf67be50417f59c2c2f167def9a775；仅输入公开电影标题和 genre。所有 encoder 参数冻结，mask mean pooling 后归一化，不读取评分/验证/测试标签。公开文本语义不是私有视频/世界知识对齐 MLLM。  long-sequence ranking semantic-id compression 搜广推 用户历史与排序骨干 UxSID为什么按用户与目标SID共享记忆？ 逐候选检索贵，完全候选无关压缩又粗；同第一层SID的相近目标共享兴趣状态，居中折中精度与缓存。语义同组不保证具体商品偏好完全一样。 例如同类鞋可复用部分兴趣记忆，但最终商品仍有不同特征。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-uxsid-c8fb3e15" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f96582456061914a">UxSID为什么按用户与目标SID共享记忆？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Auxsid">UxSID: Semantic-Aware User Interests Modeling for Ultra-Long Sequence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>逐候选检索贵，完全候选无关压缩又粗；同第一层SID的相近目标共享兴趣状态，居中折中精度与缓存。语义同组不保证具体商品偏好完全一样。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同类鞋可复用部分兴趣记忆，但最终商品仍有不同特征。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.09040">原论文</a> · <a href="../../../../reproductions/2605.09040-uxsid/">实现解读</a> · <a href="#qa-f96582456061914a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:uxsid" data-paper-title="UxSID: Semantic-Aware User Interests Modeling for Ultra-Long Sequence" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="UxSID: Semantic-Aware User Interests Modeling for Ultra-Long Sequence 搜广推与 LLM 应用 Kuaishou 2026-05-09 UxSID 在逐候选检索和完全候选无关的历史压缩之间加入“目标语义组共享记忆”：用目标物品第一层 SID 查询全历史与可学习兴趣锚点，利用全局兴趣门控第二层语义探针。语义相近的候选共享用户兴趣表示，使离线端到端训练与线上按用户/SID 查表使用同一记忆。IAIC 先用可学习锚点对行为序列做交叉注意力，再为每个锚点配置独立 Sigmoid PFFN、残差及 LayerNorm；正交项抑制兴趣坍缩。目标 SID 对原序列取全局响应，并以该响应门控 SID 后查询压缩锚点，最后拼接两级兴趣表示进行监督训练。 一次早期 CPU/seed42/100 用户/1 epoch 诊断中，UxSID test AUC 0.5848，validation 选择的 agnostic 为 0.5916；默认 encoder 是固定版本 Qwen2.5-0.5B-Instruct 7ae557604adf67be50417f59c2c2f167def9a775；仅输入公开电影标题和 genre。所有 encoder 参数冻结，mask mean pooling 后归一化，不读取评分/验证/测试标签。公开文本语义不是私有视频/世界知识对齐 MLLM。  long-sequence ranking semantic-id compression 搜广推 用户历史与排序骨干 UxSID 为什么按目标第一层 SID 共享记忆，而不逐候选检索或完全候选无关地压缩历史？ 逐候选读全历史重复昂贵，完全公共摘要又容易丢掉目标相关细节。UxSID 让语义同组候选共享用户兴趣，第一层 SID 先响应原历史并门控后续语义探针，再读取可学习锚点；独立 PFFN 与正交约束减少兴趣坍缩。共享粒度介于用户与单物品之间，但同组候选仍可能存在被压平的差异。 示意：多件露营商品共享一份用户露营记忆，而相机组读取另一份。这样不用每顶帐篷都遍历全历史，又比所有商品只用一个通用用户向量更有针对性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-79650491f8323060">UxSID 为什么按目标第一层 SID 共享记忆，而不逐候选检索或完全候选无关地压缩历史？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Auxsid">UxSID: Semantic-Aware User Interests Modeling for Ultra-Long Sequence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>逐候选读全历史重复昂贵，完全公共摘要又容易丢掉目标相关细节。UxSID 让语义同组候选共享用户兴趣，第一层 SID 先响应原历史并门控后续语义探针，再读取可学习锚点；独立 PFFN 与正交约束减少兴趣坍缩。共享粒度介于用户与单物品之间，但同组候选仍可能存在被压平的差异。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>多件露营商品共享一份用户露营记忆，而相机组读取另一份。这样不用每顶帐篷都遍历全历史，又比所有商品只用一个通用用户向量更有针对性。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.09040">原论文</a> · <a href="../../../../reproductions/2605.09040-uxsid/">实现解读</a> · <a href="#qa-79650491f8323060">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:uxsid" data-paper-title="UxSID: Semantic-Aware User Interests Modeling for Ultra-Long Sequence" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="UxSID: Semantic-Aware User Interests Modeling for Ultra-Long Sequence 搜广推与 LLM 应用 Kuaishou 2026-05-09 UxSID 在逐候选检索和完全候选无关的历史压缩之间加入“目标语义组共享记忆”：用目标物品第一层 SID 查询全历史与可学习兴趣锚点，利用全局兴趣门控第二层语义探针。语义相近的候选共享用户兴趣表示，使离线端到端训练与线上按用户/SID 查表使用同一记忆。IAIC 先用可学习锚点对行为序列做交叉注意力，再为每个锚点配置独立 Sigmoid PFFN、残差及 LayerNorm；正交项抑制兴趣坍缩。目标 SID 对原序列取全局响应，并以该响应门控 SID 后查询压缩锚点，最后拼接两级兴趣表示进行监督训练。 一次早期 CPU/seed42/100 用户/1 epoch 诊断中，UxSID test AUC 0.5848，validation 选择的 agnostic 为 0.5916；默认 encoder 是固定版本 Qwen2.5-0.5B-Instruct 7ae557604adf67be50417f59c2c2f167def9a775；仅输入公开电影标题和 genre。所有 encoder 参数冻结，mask mean pooling 后归一化，不读取评分/验证/测试标签。公开文本语义不是私有视频/世界知识对齐 MLLM。  long-sequence ranking semantic-id compression 搜广推 用户历史与排序骨干 全局与局部两级probe为什么不是重复attention？ 目标先查完整历史获得全局响应，门控SID后再查压缩锚点获取局部兴趣，两级输入不同。只保留锚点查询会失去全局响应调节，不能当完整原机制。 例如先知道这类兴趣在历史强不强，再决定到哪些锚点细查。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c5172297d44da3dd">全局与局部两级probe为什么不是重复attention？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Auxsid">UxSID: Semantic-Aware User Interests Modeling for Ultra-Long Sequence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标先查完整历史获得全局响应，门控SID后再查压缩锚点获取局部兴趣，两级输入不同。只保留锚点查询会失去全局响应调节，不能当完整原机制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先知道这类兴趣在历史强不强，再决定到哪些锚点细查。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.09040">原论文</a> · <a href="../../../../reproductions/2605.09040-uxsid/">实现解读</a> · <a href="#qa-c5172297d44da3dd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:uxsid" data-paper-title="UxSID: Semantic-Aware User Interests Modeling for Ultra-Long Sequence" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="UxSID: Semantic-Aware User Interests Modeling for Ultra-Long Sequence 搜广推与 LLM 应用 Kuaishou 2026-05-09 UxSID 在逐候选检索和完全候选无关的历史压缩之间加入“目标语义组共享记忆”：用目标物品第一层 SID 查询全历史与可学习兴趣锚点，利用全局兴趣门控第二层语义探针。语义相近的候选共享用户兴趣表示，使离线端到端训练与线上按用户/SID 查表使用同一记忆。IAIC 先用可学习锚点对行为序列做交叉注意力，再为每个锚点配置独立 Sigmoid PFFN、残差及 LayerNorm；正交项抑制兴趣坍缩。目标 SID 对原序列取全局响应，并以该响应门控 SID 后查询压缩锚点，最后拼接两级兴趣表示进行监督训练。 一次早期 CPU/seed42/100 用户/1 epoch 诊断中，UxSID test AUC 0.5848，validation 选择的 agnostic 为 0.5916；默认 encoder 是固定版本 Qwen2.5-0.5B-Instruct 7ae557604adf67be50417f59c2c2f167def9a775；仅输入公开电影标题和 genre。所有 encoder 参数冻结，mask mean pooling 后归一化，不读取评分/验证/测试标签。公开文本语义不是私有视频/世界知识对齐 MLLM。  long-sequence ranking semantic-id compression 搜广推 用户历史与排序骨干 IAIC每锚PFFN与正交项有哪些不可替换细节？ PFFN参数各锚独立；正交分母是整矩阵平方L2而非逐行余弦归一。当前量化也明确用本地两级k-means加残差代理，不能冒称原LETTER码本。 例如把所有锚共用一个FFN，虽维度一致，却削弱原本的槽位专长。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3502ab9fa810ccda">IAIC每锚PFFN与正交项有哪些不可替换细节？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Auxsid">UxSID: Semantic-Aware User Interests Modeling for Ultra-Long Sequence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>PFFN参数各锚独立；正交分母是整矩阵平方L2而非逐行余弦归一。当前量化也明确用本地两级k-means加残差代理，不能冒称原LETTER码本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把所有锚共用一个FFN，虽维度一致，却削弱原本的槽位专长。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.09040">原论文</a> · <a href="../../../../reproductions/2605.09040-uxsid/">实现解读</a> · <a href="#qa-3502ab9fa810ccda">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:semantic-native-longseq" data-paper-title="Beyond Item IDs: Scaling Short-Form-Video Recommendation via Semantic-Native Long Sequence Modeling" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Beyond Item IDs: Scaling Short-Form-Video Recommendation via Semantic-Native Long Sequence Modeling 搜广推与 LLM 应用 Google 2026-05-04 原子 Video ID 只能记忆内容，embedding table 随 corpus 无界增长，新视频也没有可迁移语义；完整 attention 又让千级历史成本呈平方增长。论文先用 RQ-VAE 产生 coarse-to-fine SID，并截断为 bounded bigram vocabulary；再把相邻个事件无参数折叠为 super-token，同时加入统一 global query，使模型在保留全局兴趣的情况下处理更长历史。 本地未训练 Google RQ-VAE，没有 billion-user 私有流量、2,000-event 服务序列、异步长历史模块或定制 HBM kernel。Fidelity: 核心机制复现。本地实际构建 residual-quantized Semantic ID，执行 depth-truncated bigram、parameter-free temporal folding、global query attention 和 global-local pooling。MovieLens feature 只代理多模态视频表征；  long-sequence semantic-id rq-vae efficient-transformer cold-start 搜广推 用户历史与排序骨干 Semantic-Native的层级SID前缀相同，是否代表两条视频就是同一物品？ 不必然。层级语义码共享前缀表示粗粒度语义相近，具体物品身份仍需完整路径与目录映射。它与为每个视频分配互不相关的原子ID不同，目的在于共享表示；不能把粗粒度语义相同当成交互日志中的同一条视频。 教学例子：两条不同露营视频可共享粗级语义前缀，却有各自内容与行为记录；合并前缀不等于合并物品身份。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-semantic-native-longseq-dee361e1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-707a5bb5919e2395">Semantic-Native的层级SID前缀相同，是否代表两条视频就是同一物品？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asemantic-native-longseq">Beyond Item IDs: Scaling Short-Form-Video Recommendation via Semantic-Native Long Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不必然。层级语义码共享前缀表示粗粒度语义相近，具体物品身份仍需完整路径与目录映射。它与为每个视频分配互不相关的原子ID不同，目的在于共享表示；不能把粗粒度语义相同当成交互日志中的同一条视频。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两条不同露营视频可共享粗级语义前缀，却有各自内容与行为记录；合并前缀不等于合并物品身份。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.07546">原论文</a> · <a href="../../../../reproductions/2606.07546-semantic-native-longseq/">实现解读</a> · <a href="#qa-707a5bb5919e2395">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:semantic-native-longseq" data-paper-title="Beyond Item IDs: Scaling Short-Form-Video Recommendation via Semantic-Native Long Sequence Modeling" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Beyond Item IDs: Scaling Short-Form-Video Recommendation via Semantic-Native Long Sequence Modeling 搜广推与 LLM 应用 Google 2026-05-04 原子 Video ID 只能记忆内容，embedding table 随 corpus 无界增长，新视频也没有可迁移语义；完整 attention 又让千级历史成本呈平方增长。论文先用 RQ-VAE 产生 coarse-to-fine SID，并截断为 bounded bigram vocabulary；再把相邻个事件无参数折叠为 super-token，同时加入统一 global query，使模型在保留全局兴趣的情况下处理更长历史。 本地未训练 Google RQ-VAE，没有 billion-user 私有流量、2,000-event 服务序列、异步长历史模块或定制 HBM kernel。Fidelity: 核心机制复现。本地实际构建 residual-quantized Semantic ID，执行 depth-truncated bigram、parameter-free temporal folding、global query attention 和 global-local pooling。MovieLens feature 只代理多模态视频表征；  long-sequence semantic-id rq-vae efficient-transformer cold-start 搜广推 用户历史与排序骨干 Semantic-Native LongSeq 为什么同时压缩 SID 词表和时间序列，而不是只扩大历史窗口？ 原子 ID 表随内容增长，长序列全注意力又随长度平方增加。层级 SID 截断为有界词表处理表示规模，相邻事件折叠为 super-token 处理时间长度，全局 query 再收集跨窗口兴趣。两种压缩针对不同瓶颈，都会牺牲分辨率；本地用均值与近期组合代理折叠，不能当作原文通道重排的等价实现。 示意：四十八条历史每四条折成一个 token，只需处理十二个局部位置；同时用粗细语义码共享内容知识。被折在同一窗口的事件顺序仍可能损失，不能说完整细节都保留。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-63e5da9e21228955">Semantic-Native LongSeq 为什么同时压缩 SID 词表和时间序列，而不是只扩大历史窗口？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asemantic-native-longseq">Beyond Item IDs: Scaling Short-Form-Video Recommendation via Semantic-Native Long Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原子 ID 表随内容增长，长序列全注意力又随长度平方增加。层级 SID 截断为有界词表处理表示规模，相邻事件折叠为 super-token 处理时间长度，全局 query 再收集跨窗口兴趣。两种压缩针对不同瓶颈，都会牺牲分辨率；本地用均值与近期组合代理折叠，不能当作原文通道重排的等价实现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>四十八条历史每四条折成一个 token，只需处理十二个局部位置；同时用粗细语义码共享内容知识。被折在同一窗口的事件顺序仍可能损失，不能说完整细节都保留。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.07546">原论文</a> · <a href="../../../../reproductions/2606.07546-semantic-native-longseq/">实现解读</a> · <a href="#qa-63e5da9e21228955">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:semantic-native-longseq" data-paper-title="Beyond Item IDs: Scaling Short-Form-Video Recommendation via Semantic-Native Long Sequence Modeling" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Beyond Item IDs: Scaling Short-Form-Video Recommendation via Semantic-Native Long Sequence Modeling 搜广推与 LLM 应用 Google 2026-05-04 原子 Video ID 只能记忆内容，embedding table 随 corpus 无界增长，新视频也没有可迁移语义；完整 attention 又让千级历史成本呈平方增长。论文先用 RQ-VAE 产生 coarse-to-fine SID，并截断为 bounded bigram vocabulary；再把相邻个事件无参数折叠为 super-token，同时加入统一 global query，使模型在保留全局兴趣的情况下处理更长历史。 本地未训练 Google RQ-VAE，没有 billion-user 私有流量、2,000-event 服务序列、异步长历史模块或定制 HBM kernel。Fidelity: 核心机制复现。本地实际构建 residual-quantized Semantic ID，执行 depth-truncated bigram、parameter-free temporal folding、global query attention 和 global-local pooling。MovieLens feature 只代理多模态视频表征；  long-sequence semantic-id rq-vae efficient-transformer cold-start 搜广推 用户历史与排序骨干 temporal folding与只截最近历史有什么区别？ 折叠把邻近事件沿特征重组保留粗粒度旧信息，截断直接丢远期。压缩损失时间分辨率，global queries也不保证细节无损，不能当完整历史等价。 例如四次连续行为压成一super-token，顺序细节可能弱化但不全部删除。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-8b1c2fa9a1b3c3ca">temporal folding与只截最近历史有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asemantic-native-longseq">Beyond Item IDs: Scaling Short-Form-Video Recommendation via Semantic-Native Long Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>折叠把邻近事件沿特征重组保留粗粒度旧信息，截断直接丢远期。压缩损失时间分辨率，global queries也不保证细节无损，不能当完整历史等价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如四次连续行为压成一super-token，顺序细节可能弱化但不全部删除。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.07546">原论文</a> · <a href="../../../../reproductions/2606.07546-semantic-native-longseq/">实现解读</a> · <a href="#qa-8b1c2fa9a1b3c3ca">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:semantic-native-longseq" data-paper-title="Beyond Item IDs: Scaling Short-Form-Video Recommendation via Semantic-Native Long Sequence Modeling" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Beyond Item IDs: Scaling Short-Form-Video Recommendation via Semantic-Native Long Sequence Modeling 搜广推与 LLM 应用 Google 2026-05-04 原子 Video ID 只能记忆内容，embedding table 随 corpus 无界增长，新视频也没有可迁移语义；完整 attention 又让千级历史成本呈平方增长。论文先用 RQ-VAE 产生 coarse-to-fine SID，并截断为 bounded bigram vocabulary；再把相邻个事件无参数折叠为 super-token，同时加入统一 global query，使模型在保留全局兴趣的情况下处理更长历史。 本地未训练 Google RQ-VAE，没有 billion-user 私有流量、2,000-event 服务序列、异步长历史模块或定制 HBM kernel。Fidelity: 核心机制复现。本地实际构建 residual-quantized Semantic ID，执行 depth-truncated bigram、parameter-free temporal folding、global query attention 和 global-local pooling。MovieLens feature 只代理多模态视频表征；  long-sequence semantic-id rq-vae efficient-transformer cold-start 搜广推 用户历史与排序骨干 本地折叠是否逐字实现原论文channel重组？ 不是，本地mean/recent组合只保留时间分辨率换表达的原则，未训练Google RQ-VAE或生产模块。池化mask包含始终有效global query，不能漏计它们或把padding当历史。 例如均值代理能验粗压缩，但不能冒称原折叠张量布局。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7ff6d57f3d2e041c">本地折叠是否逐字实现原论文channel重组？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asemantic-native-longseq">Beyond Item IDs: Scaling Short-Form-Video Recommendation via Semantic-Native Long Sequence Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是，本地mean/recent组合只保留时间分辨率换表达的原则，未训练Google RQ-VAE或生产模块。池化mask包含始终有效global query，不能漏计它们或把padding当历史。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如均值代理能验粗压缩，但不能冒称原折叠张量布局。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.07546">原论文</a> · <a href="../../../../reproductions/2606.07546-semantic-native-longseq/">实现解读</a> · <a href="#qa-7ff6d57f3d2e041c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rankup" data-paper-title="RankUp: Towards High-rank Representations for Large Scale Advertising Recommender Systems" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="RankUp: Towards High-rank Representations for Large Scale Advertising Recommender Systems 搜广推与 LLM 应用 Tencent 2026-04-20 RankUp 针对深层推荐网络的表征坍缩，组合随机置换分组、多套 embedding、全局 token、交叉预训练 embedding 注入和任务 token 解耦，让随模型规模增长的参数真正转化为更高秩的表达空间。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04702，相对变化 -12.94%。本地代理目标与论文生产任务不同，不能外推线上 lift。  advertising representation-collapse feature-interaction 搜广推 用户历史与排序骨干 RankUp 所追求的较高表示秩，为什么不能单独证明学到了更有用的兴趣？ 秩描述向量变化包含多少独立方向，不衡量这些方向是否对应目标信息。随机噪声也可增加秩，甚至分散原本有用结构。因此要把谱与任务指标、真实信号分组一起检查，不能只因深层 token 不再相同就宣布推荐质量或泛化已改善。 示意：给每位用户加随机正交噪声可让矩阵更满秩，却没有增加任何偏好知识；只有新方向携带能预测行为的线索，才可能帮助推荐。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-rankup-a9399758" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-94f1626a3266cd89">RankUp 所追求的较高表示秩，为什么不能单独证明学到了更有用的兴趣？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arankup">RankUp: Towards High-rank Representations for Large Scale Advertising Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>秩描述向量变化包含多少独立方向，不衡量这些方向是否对应目标信息。随机噪声也可增加秩，甚至分散原本有用结构。因此要把谱与任务指标、真实信号分组一起检查，不能只因深层 token 不再相同就宣布推荐质量或泛化已改善。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>给每位用户加随机正交噪声可让矩阵更满秩，却没有增加任何偏好知识；只有新方向携带能预测行为的线索，才可能帮助推荐。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.17878">原论文</a> · <a href="../../../../reproductions/2604.17878-rankup/">实现解读</a> · <a href="#qa-94f1626a3266cd89">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rankup" data-paper-title="RankUp: Towards High-rank Representations for Large Scale Advertising Recommender Systems" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="RankUp: Towards High-rank Representations for Large Scale Advertising Recommender Systems 搜广推与 LLM 应用 Tencent 2026-04-20 RankUp 针对深层推荐网络的表征坍缩，组合随机置换分组、多套 embedding、全局 token、交叉预训练 embedding 注入和任务 token 解耦，让随模型规模增长的参数真正转化为更高秩的表达空间。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04702，相对变化 -12.94%。本地代理目标与论文生产任务不同，不能外推线上 lift。  advertising representation-collapse feature-interaction 搜广推 用户历史与排序骨干 RankUp 为什么不仅增加 embedding 或层数，还用随机置换分组和全局 token 对抗低秩坍缩？ 参数增加并不保证表示包含更多独立方向，深层交互可能反复使用相同子空间。不同置换与多套 embedding 改变特征组合路径，全局 token 提供跨组交流，外部表征与任务解耦再补充不同信息。目标是让新增容量转成更丰富的表示秩；这些结构只是缓解手段，不能把参数变多等同于有效秩必然提高。 示意：四组特征若始终按同一种方式分组，层数再多也可能重复同样交叉。换不同分组并保留全局交流通道，可让原先从未同组的特征形成新的组合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-0478859fae50a11a">RankUp 为什么不仅增加 embedding 或层数，还用随机置换分组和全局 token 对抗低秩坍缩？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arankup">RankUp: Towards High-rank Representations for Large Scale Advertising Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>参数增加并不保证表示包含更多独立方向，深层交互可能反复使用相同子空间。不同置换与多套 embedding 改变特征组合路径，全局 token 提供跨组交流，外部表征与任务解耦再补充不同信息。目标是让新增容量转成更丰富的表示秩；这些结构只是缓解手段，不能把参数变多等同于有效秩必然提高。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>四组特征若始终按同一种方式分组，层数再多也可能重复同样交叉。换不同分组并保留全局交流通道，可让原先从未同组的特征形成新的组合。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.17878">原论文</a> · <a href="../../../../reproductions/2604.17878-rankup/">实现解读</a> · <a href="#qa-0478859fae50a11a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rankup" data-paper-title="RankUp: Towards High-rank Representations for Large Scale Advertising Recommender Systems" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="RankUp: Towards High-rank Representations for Large Scale Advertising Recommender Systems 搜广推与 LLM 应用 Tencent 2026-04-20 RankUp 针对深层推荐网络的表征坍缩，组合随机置换分组、多套 embedding、全局 token、交叉预训练 embedding 注入和任务 token 解耦，让随模型规模增长的参数真正转化为更高秩的表达空间。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04702，相对变化 -12.94%。本地代理目标与论文生产任务不同，不能外推线上 lift。  advertising representation-collapse feature-interaction 搜广推 用户历史与排序骨干 RankUp 的随机置换分组与全共享输入，相比怎样改变交叉机会？ 不同分组让原来未同组的特征有机会相遇，独立 embedding 提供多视角，全局 token 维持组间通信。全共享可能被强字段支配，分组则可能漏关系或重复。来源多项联合变化不支持把任何一个部件单独认定为全部收益来源。 示意：年龄与品类原被分开，另一置换让它们同组组合；若置换每次只打乱输出却不对齐参数，也可能破坏而非增加有效交互。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f98e38ec565ff9d5">RankUp 的随机置换分组与全共享输入，相比怎样改变交叉机会？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arankup">RankUp: Towards High-rank Representations for Large Scale Advertising Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同分组让原来未同组的特征有机会相遇，独立 embedding 提供多视角，全局 token 维持组间通信。全共享可能被强字段支配，分组则可能漏关系或重复。来源多项联合变化不支持把任何一个部件单独认定为全部收益来源。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>年龄与品类原被分开，另一置换让它们同组组合；若置换每次只打乱输出却不对齐参数，也可能破坏而非增加有效交互。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.17878">原论文</a> · <a href="../../../../reproductions/2604.17878-rankup/">实现解读</a> · <a href="#qa-f98e38ec565ff9d5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rankup" data-paper-title="RankUp: Towards High-rank Representations for Large Scale Advertising Recommender Systems" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="RankUp: Towards High-rank Representations for Large Scale Advertising Recommender Systems 搜广推与 LLM 应用 Tencent 2026-04-20 RankUp 针对深层推荐网络的表征坍缩，组合随机置换分组、多套 embedding、全局 token、交叉预训练 embedding 注入和任务 token 解耦，让随模型规模增长的参数真正转化为更高秩的表达空间。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04702，相对变化 -12.94%。本地代理目标与论文生产任务不同，不能外推线上 lift。  advertising representation-collapse feature-interaction 搜广推 用户历史与排序骨干 RankUp 的置换矩阵与字段 identity 为什么需要同步追踪？ XP 改变输入顺序，后续对应 embedding 与分组参数必须遵循同一映射，不然语义错位。多套表与全局 token 的残差维也要一致；测试不能用目标反馈挑最有利置换。本地 proxy 不提供完整生产 scaling law 验证。 示意：交换价格和年龄后仍按原语义查表，会把十八当价格编码；即使网络能拟合训练，不能称执行了同义随机分组方案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-075dc39c4c00dc0e">RankUp 的置换矩阵与字段 identity 为什么需要同步追踪？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arankup">RankUp: Towards High-rank Representations for Large Scale Advertising Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>XP 改变输入顺序，后续对应 embedding 与分组参数必须遵循同一映射，不然语义错位。多套表与全局 token 的残差维也要一致；测试不能用目标反馈挑最有利置换。本地 proxy 不提供完整生产 scaling law 验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>交换价格和年龄后仍按原语义查表，会把十八当价格编码；即使网络能拟合训练，不能称执行了同义随机分组方案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.17878">原论文</a> · <a href="../../../../reproductions/2604.17878-rankup/">实现解读</a> · <a href="#qa-075dc39c4c00dc0e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:uniscale" data-paper-title="UniScale: Synergistic Entire Space Data and Model Scaling for Search Ranking" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="UniScale: Synergistic Entire Space Data and Model Scaling for Search Ranking 搜广推与 LLM 应用 Taobao &amp; Tmall Group / Alibaba 2026-03-25 ES³ 从曝光外全空间扩充数据，HHSFT 分层融合异构样本；数据规模和模型容量协同扩展，并配合低成本部署。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 uniscale 核心机制，相对 NDCG@10 -2.20%。  search-ranking model-scaling entire-space-learning 搜广推 用户历史与排序骨干 UniScale为什么同时扩数据空间与模型容量？ 只放大模型仍受曝光偏置和样本覆盖限制，只加数据也可能超过模型表达。ES³拓展曝光外空间，HHSFT融合异构样本，再与可部署容量协同。 例如从未曝光区域补数据，与给旧曝光数据多加层，作用不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-uniscale-5256c0f4" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-18cbfa80cab3f0a4">UniScale为什么同时扩数据空间与模型容量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Auniscale">UniScale: Synergistic Entire Space Data and Model Scaling for Search Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只放大模型仍受曝光偏置和样本覆盖限制，只加数据也可能超过模型表达。ES³拓展曝光外空间，HHSFT融合异构样本，再与可部署容量协同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如从未曝光区域补数据，与给旧曝光数据多加层，作用不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.24226">原论文</a> · <a href="../../../../reproductions/2603.24226-uniscale/">实现解读</a> · <a href="#qa-18cbfa80cab3f0a4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:uniscale" data-paper-title="UniScale: Synergistic Entire Space Data and Model Scaling for Search Ranking" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="UniScale: Synergistic Entire Space Data and Model Scaling for Search Ranking 搜广推与 LLM 应用 Taobao &amp; Tmall Group / Alibaba 2026-03-25 ES³ 从曝光外全空间扩充数据，HHSFT 分层融合异构样本；数据规模和模型容量协同扩展，并配合低成本部署。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 uniscale 核心机制，相对 NDCG@10 -2.20%。  search-ranking model-scaling entire-space-learning 搜广推 用户历史与排序骨干 UniScale 为什么把曝光外数据扩充与分层异构训练一起做，而不只增加模型参数？ 仅扩大网络仍受现有曝光日志覆盖限制，新增容量可能继续拟合同样狭窄的样本。曝光外扩充增加学习范围，分层融合为不同来源和质量的数据安排合适路径，再协同扩大容量。关键是数据与模型共同扩展，合成或曝光外样本的可信度仍要控制；数据更多不自动意味着偏差更小。 示意：模型原来只见过首页曝光商品，即使参数翻倍也难学未曝光品类。扩充其他空间样本后，再按来源层次融合，可避免把高置信点击和弱监督样本完全等量对待。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f29a5b9c1c823d5f">UniScale 为什么把曝光外数据扩充与分层异构训练一起做，而不只增加模型参数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Auniscale">UniScale: Synergistic Entire Space Data and Model Scaling for Search Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>仅扩大网络仍受现有曝光日志覆盖限制，新增容量可能继续拟合同样狭窄的样本。曝光外扩充增加学习范围，分层融合为不同来源和质量的数据安排合适路径，再协同扩大容量。关键是数据与模型共同扩展，合成或曝光外样本的可信度仍要控制；数据更多不自动意味着偏差更小。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型原来只见过首页曝光商品，即使参数翻倍也难学未曝光品类。扩充其他空间样本后，再按来源层次融合，可避免把高置信点击和弱监督样本完全等量对待。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.24226">原论文</a> · <a href="../../../../reproductions/2603.24226-uniscale/">实现解读</a> · <a href="#qa-f29a5b9c1c823d5f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:uniscale" data-paper-title="UniScale: Synergistic Entire Space Data and Model Scaling for Search Ranking" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="UniScale: Synergistic Entire Space Data and Model Scaling for Search Ranking 搜广推与 LLM 应用 Taobao &amp; Tmall Group / Alibaba 2026-03-25 ES³ 从曝光外全空间扩充数据，HHSFT 分层融合异构样本；数据规模和模型容量协同扩展，并配合低成本部署。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 uniscale 核心机制，相对 NDCG@10 -2.20%。  search-ranking model-scaling entire-space-learning 搜广推 用户历史与排序骨干 曝光外样本与直接随机负采样能等同吗？ 不能，来源和标签可信度不同，需按方法定义融合；未曝光不是用户明确不喜欢。扩全空间也不自动消除选择偏差，不能把未知全部标负。 例如用户没看见某商品，不能断言他见到也不会点。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5d1802efe29e31aa">曝光外样本与直接随机负采样能等同吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Auniscale">UniScale: Synergistic Entire Space Data and Model Scaling for Search Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，来源和标签可信度不同，需按方法定义融合；未曝光不是用户明确不喜欢。扩全空间也不自动消除选择偏差，不能把未知全部标负。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户没看见某商品，不能断言他见到也不会点。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.24226">原论文</a> · <a href="../../../../reproductions/2603.24226-uniscale/">实现解读</a> · <a href="#qa-5d1802efe29e31aa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:uniscale" data-paper-title="UniScale: Synergistic Entire Space Data and Model Scaling for Search Ranking" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="UniScale: Synergistic Entire Space Data and Model Scaling for Search Ranking 搜广推与 LLM 应用 Taobao &amp; Tmall Group / Alibaba 2026-03-25 ES³ 从曝光外全空间扩充数据，HHSFT 分层融合异构样本；数据规模和模型容量协同扩展，并配合低成本部署。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 uniscale 核心机制，相对 NDCG@10 -2.20%。  search-ranking model-scaling entire-space-learning 搜广推 用户历史与排序骨干 UniScale本地门控FFN能代表完整ES³数据工程吗？ 不能，参考网络只验证异构分支交互，私有全空间采样、生产模型和低成本部署未复刻。样本域标签、训练切分与融合权重需可审计。 例如多个FFN可运行，不等于真实曝光外数据已经被可靠生成。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-49ea328e0fbe6bb4">UniScale本地门控FFN能代表完整ES³数据工程吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Auniscale">UniScale: Synergistic Entire Space Data and Model Scaling for Search Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taobao &amp; Tmall Group / Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，参考网络只验证异构分支交互，私有全空间采样、生产模型和低成本部署未复刻。样本域标签、训练切分与融合权重需可审计。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如多个FFN可运行，不等于真实曝光外数据已经被可靠生成。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.24226">原论文</a> · <a href="../../../../reproductions/2603.24226-uniscale/">实现解读</a> · <a href="#qa-49ea328e0fbe6bb4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sort-ranking" data-paper-title="SORT: A Systematically Optimized Ranking Transformer for Industrial-scale Recommenders" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="SORT: A Systematically Optimized Ranking Transformer for Industrial-scale Recommenders 搜广推与 LLM 应用 Alibaba International Digital Commerce 2026-03-04 系统重做特征 token 化、注意力和 FFN，并以面向工业硬件的结构压缩长序列，使单一 Transformer 替代传统 DLRM。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 sort-ranking 核心机制，相对 NDCG@10 -13.11%。  ranking transformer serving-efficiency 搜广推 用户历史与排序骨干 SORT Ranking为什么不是把普通Transformer直接套推荐？ 它围绕工业特征token化、attention、FFN与硬件结构重做设计，目标是让统一排序Transformer承担传统DLRM角色。通用残差公式不足以涵盖系统设计。 例如稀疏特征怎样成token，与自然语言逐字输入不是同一个前处理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-sort-ranking-bed02966" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-3e9bf08ccb75e4b5">SORT Ranking为什么不是把普通Transformer直接套推荐？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asort-ranking">SORT: A Systematically Optimized Ranking Transformer for Industrial-scale Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它围绕工业特征token化、attention、FFN与硬件结构重做设计，目标是让统一排序Transformer承担传统DLRM角色。通用残差公式不足以涵盖系统设计。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如稀疏特征怎样成token，与自然语言逐字输入不是同一个前处理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.03988">原论文</a> · <a href="../../../../reproductions/2603.03988-sort-ranking/">实现解读</a> · <a href="#qa-3e9bf08ccb75e4b5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sort-ranking" data-paper-title="SORT: A Systematically Optimized Ranking Transformer for Industrial-scale Recommenders" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="SORT: A Systematically Optimized Ranking Transformer for Industrial-scale Recommenders 搜广推与 LLM 应用 Alibaba International Digital Commerce 2026-03-04 系统重做特征 token 化、注意力和 FFN，并以面向工业硬件的结构压缩长序列，使单一 Transformer 替代传统 DLRM。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 sort-ranking 核心机制，相对 NDCG@10 -13.11%。  ranking transformer serving-efficiency 搜广推 用户历史与排序骨干 SORT Ranking 为什么连特征 token 化、注意力与 FFN 都要一起改，而不直接把语言 Transformer 搬到排序？ 推荐输入包含语义各异的字段和长行为序列，token 组织决定哪些信息能交互，注意力决定信息流，FFN 决定逐 token 的变换容量。硬件约束下压缩长序列还会改变计算分配，因此几个环节需要协同设计。使用 Transformer 只是框架选择，本地简化机制不能证明完整工业 DLRM 替换方案的吞吐与精度。 示意：把年龄、商品类别和数百次行为都当同一种文本词直接堆入模型，可能浪费预算。先设计字段接口与历史压缩，再分配注意力和 FFN，才有机会匹配排序负载。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-a030a6e6a420cbd7">SORT Ranking 为什么连特征 token 化、注意力与 FFN 都要一起改，而不直接把语言 Transformer 搬到排序？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asort-ranking">SORT: A Systematically Optimized Ranking Transformer for Industrial-scale Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>推荐输入包含语义各异的字段和长行为序列，token 组织决定哪些信息能交互，注意力决定信息流，FFN 决定逐 token 的变换容量。硬件约束下压缩长序列还会改变计算分配，因此几个环节需要协同设计。使用 Transformer 只是框架选择，本地简化机制不能证明完整工业 DLRM 替换方案的吞吐与精度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把年龄、商品类别和数百次行为都当同一种文本词直接堆入模型，可能浪费预算。先设计字段接口与历史压缩，再分配注意力和 FFN，才有机会匹配排序负载。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.03988">原论文</a> · <a href="../../../../reproductions/2603.03988-sort-ranking/">实现解读</a> · <a href="#qa-a030a6e6a420cbd7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sort-ranking" data-paper-title="SORT: A Systematically Optimized Ranking Transformer for Industrial-scale Recommenders" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="SORT: A Systematically Optimized Ranking Transformer for Industrial-scale Recommenders 搜广推与 LLM 应用 Alibaba International Digital Commerce 2026-03-04 系统重做特征 token 化、注意力和 FFN，并以面向工业硬件的结构压缩长序列，使单一 Transformer 替代传统 DLRM。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 sort-ranking 核心机制，相对 NDCG@10 -13.11%。  ranking transformer serving-efficiency 搜广推 用户历史与排序骨干 统一排序Transformer与传统DLRM的主要机制差异是什么？ Transformer通过token交互建模特征和长序列，DLRM常依嵌入与显式交叉及MLP；工业成本与特征处理决定适配，不能仅按模型名称排性能。 例如同样ID特征，交互发生的位置和计算复用方式可不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-2bf52e7b5dfc4fcf">统一排序Transformer与传统DLRM的主要机制差异是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asort-ranking">SORT: A Systematically Optimized Ranking Transformer for Industrial-scale Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Transformer通过token交互建模特征和长序列，DLRM常依嵌入与显式交叉及MLP；工业成本与特征处理决定适配，不能仅按模型名称排性能。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同样ID特征，交互发生的位置和计算复用方式可不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.03988">原论文</a> · <a href="../../../../reproductions/2603.03988-sort-ranking/">实现解读</a> · <a href="#qa-2bf52e7b5dfc4fcf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sort-ranking" data-paper-title="SORT: A Systematically Optimized Ranking Transformer for Industrial-scale Recommenders" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="SORT: A Systematically Optimized Ranking Transformer for Industrial-scale Recommenders 搜广推与 LLM 应用 Alibaba International Digital Commerce 2026-03-04 系统重做特征 token 化、注意力和 FFN，并以面向工业硬件的结构压缩长序列，使单一 Transformer 替代传统 DLRM。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 sort-ranking 核心机制，相对 NDCG@10 -13.11%。  ranking transformer serving-efficiency 搜广推 用户历史与排序骨干 本地SORT残差MHA/FFN实现能证明工业硬件压缩吗？ 不能，公开固定候选只验证中心模型路径，没有私有特征、生产规模或kernel。参数和mask需审查，但解析结构存在不等于真实QPS或在线业务增长。 例如小目录训练能跑通，不代表工业大量稀疏token仍满足时延预算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-654aff3c4fd7e4fa">本地SORT残差MHA/FFN实现能证明工业硬件压缩吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asort-ranking">SORT: A Systematically Optimized Ranking Transformer for Industrial-scale Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba International Digital Commerce</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，公开固定候选只验证中心模型路径，没有私有特征、生产规模或kernel。参数和mask需审查，但解析结构存在不等于真实QPS或在线业务增长。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如小目录训练能跑通，不代表工业大量稀疏token仍满足时延预算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.03988">原论文</a> · <a href="../../../../reproductions/2603.03988-sort-ranking/">实现解读</a> · <a href="#qa-654aff3c4fd7e4fa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hpgr" data-paper-title="Beyond the Flat Sequence: Hierarchical and Preference-Aware Generative Recommendations" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Beyond the Flat Sequence: Hierarchical and Preference-Aware Generative Recommendations 搜广推与 LLM 应用 Harbin Institute of Technology 2026-03-01 HPGR 先通过基于 session 的掩码物品建模学习层级行为结构，再在微调阶段使用偏好引导稀疏注意力，只保留与当前意图最相关的历史事件，减少平铺长序列里的噪声和计算。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05467，相对变化 +1.23%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation hierarchical-sequence sparse-attention 搜广推 用户历史与排序骨干 HPGR 为什么用 session 掩码建模学习层级行为结构？ 会话内事件往往共享意图，跨会话代表迁移，先学习这两级结构能给后续偏好选择提供较有意义状态。平铺长历史只按相邻位置建模可能混合不同访问。预训练监督来自已观测训练内容，不允许在测试输入恢复本该未知目标。 示意：一次访问集中看帐篷与睡袋，下一次看登山鞋，session 编码先区分两段需求，而非把所有物品当同一连续意图。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-hpgr-f17a7799" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-61bf64fdb6e80c78">HPGR 为什么用 session 掩码建模学习层级行为结构？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahpgr">Beyond the Flat Sequence: Hierarchical and Preference-Aware Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>会话内事件往往共享意图，跨会话代表迁移，先学习这两级结构能给后续偏好选择提供较有意义状态。平铺长历史只按相邻位置建模可能混合不同访问。预训练监督来自已观测训练内容，不允许在测试输入恢复本该未知目标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次访问集中看帐篷与睡袋，下一次看登山鞋，session 编码先区分两段需求，而非把所有物品当同一连续意图。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.00980">原论文</a> · <a href="../../../../reproductions/2603.00980-hpgr/">实现解读</a> · <a href="#qa-61bf64fdb6e80c78">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hpgr" data-paper-title="Beyond the Flat Sequence: Hierarchical and Preference-Aware Generative Recommendations" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Beyond the Flat Sequence: Hierarchical and Preference-Aware Generative Recommendations 搜广推与 LLM 应用 Harbin Institute of Technology 2026-03-01 HPGR 先通过基于 session 的掩码物品建模学习层级行为结构，再在微调阶段使用偏好引导稀疏注意力，只保留与当前意图最相关的历史事件，减少平铺长序列里的噪声和计算。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05467，相对变化 +1.23%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation hierarchical-sequence sparse-attention 搜广推 用户历史与排序骨干 HPGR为什么先做session掩码预训练，再用偏好引导的稀疏注意力选历史？ session结构描述一段行为内部的关联，先通过掩码任务学习它，可避免把长历史当作无差别平铺事件。微调时再依据当前偏好选择相关历史，把计算集中在有用证据上，而非只按时间截断。稀疏选择也可能丢掉罕见但关键的兴趣，因此选中项的覆盖与最终预测需要一起检验。 示意：用户上周的一组相机比较属于同一session，今天评镜头时可整组提取；最近一次无关购物不应只因更近就挤掉这段有组织的历史。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f5ebe6d332af25ec">HPGR为什么先做session掩码预训练，再用偏好引导的稀疏注意力选历史？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahpgr">Beyond the Flat Sequence: Hierarchical and Preference-Aware Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>session结构描述一段行为内部的关联，先通过掩码任务学习它，可避免把长历史当作无差别平铺事件。微调时再依据当前偏好选择相关历史，把计算集中在有用证据上，而非只按时间截断。稀疏选择也可能丢掉罕见但关键的兴趣，因此选中项的覆盖与最终预测需要一起检验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户上周的一组相机比较属于同一session，今天评镜头时可整组提取；最近一次无关购物不应只因更近就挤掉这段有组织的历史。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.00980">原论文</a> · <a href="../../../../reproductions/2603.00980-hpgr/">实现解读</a> · <a href="#qa-f5ebe6d332af25ec">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hpgr" data-paper-title="Beyond the Flat Sequence: Hierarchical and Preference-Aware Generative Recommendations" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Beyond the Flat Sequence: Hierarchical and Preference-Aware Generative Recommendations 搜广推与 LLM 应用 Harbin Institute of Technology 2026-03-01 HPGR 先通过基于 session 的掩码物品建模学习层级行为结构，再在微调阶段使用偏好引导稀疏注意力，只保留与当前意图最相关的历史事件，减少平铺长序列里的噪声和计算。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05467，相对变化 +1.23%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation hierarchical-sequence sparse-attention 搜广推 用户历史与排序骨干 HPGR 的偏好引导稀疏选择与固定最近窗口，相比可用哪些远期证据？ 最近窗口直接按时间保留，稀疏选择按当前意图挑事件，允许远期相关记录进入有限预算。它依赖选择器质量，漏掉的信息下游读不到；层级预训练提供结构也不能保证选择正确。来源公开代理增益仅限对应协议。 示意：最近浏览小说但当前候选相机，选择器可找更早摄影记录；固定最近十条也许完全没有它，但错误选择也可能把过时需求带回。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7cfc34a2cc8db770">HPGR 的偏好引导稀疏选择与固定最近窗口，相比可用哪些远期证据？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahpgr">Beyond the Flat Sequence: Hierarchical and Preference-Aware Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最近窗口直接按时间保留，稀疏选择按当前意图挑事件，允许远期相关记录进入有限预算。它依赖选择器质量，漏掉的信息下游读不到；层级预训练提供结构也不能保证选择正确。来源公开代理增益仅限对应协议。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>最近浏览小说但当前候选相机，选择器可找更早摄影记录；固定最近十条也许完全没有它，但错误选择也可能把过时需求带回。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.00980">原论文</a> · <a href="../../../../reproductions/2603.00980-hpgr/">实现解读</a> · <a href="#qa-7cfc34a2cc8db770">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hpgr" data-paper-title="Beyond the Flat Sequence: Hierarchical and Preference-Aware Generative Recommendations" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Beyond the Flat Sequence: Hierarchical and Preference-Aware Generative Recommendations 搜广推与 LLM 应用 Harbin Institute of Technology 2026-03-01 HPGR 先通过基于 session 的掩码物品建模学习层级行为结构，再在微调阶段使用偏好引导稀疏注意力，只保留与当前意图最相关的历史事件，减少平铺长序列里的噪声和计算。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05467，相对变化 +1.23%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation hierarchical-sequence sparse-attention 搜广推 用户历史与排序骨干 HPGR 的 Top-K 注意力在实现中怎样避免把 padding 或未来目标选入？ 排序分应只对合法历史事件计算，padding 在 Top-K 前屏蔽，输入截止当前时刻；不足 K 时按有效长度处理，不能重复补假事件。session 边界与偏好 query 要一致，不能用 gold 下一物品构造一个测试时不可得的选择条件。 示意：真实历史三条而 K 为五，只能读三条有效记录；若空位保留零分且真实分为负，未屏蔽 padding 会被错误排进前五。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0a1842453e297052">HPGR 的 Top-K 注意力在实现中怎样避免把 padding 或未来目标选入？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahpgr">Beyond the Flat Sequence: Hierarchical and Preference-Aware Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>排序分应只对合法历史事件计算，padding 在 Top-K 前屏蔽，输入截止当前时刻；不足 K 时按有效长度处理，不能重复补假事件。session 边界与偏好 query 要一致，不能用 gold 下一物品构造一个测试时不可得的选择条件。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>真实历史三条而 K 为五，只能读三条有效记录；若空位保留零分且真实分为负，未屏蔽 padding 会被错误排进前五。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.00980">原论文</a> · <a href="../../../../reproductions/2603.00980-hpgr/">实现解读</a> · <a href="#qa-0a1842453e297052">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hisac" data-paper-title="HiSAC: Hierarchical Sparse Activation Compression for Ultra-long Sequence Modeling in Recommenders" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="HiSAC: Hierarchical Sparse Activation Compression for Ultra-long Sequence Modeling in Recommenders 搜广推与 LLM 应用 Alibaba / Taobao 2026-02-24 超长行为全量 attention 成本高，固定压缩又损失长尾兴趣。HiSAC 用多模态 RQ-VAE 形成层级 code，逐层投票生成用户特定 interest agents，再让当前 query 只 soft-route 到少量相关 agent。 Fidelity: 核心机制复现。执行 residual codes、层级投票、兴趣 agent 与 soft routing。本地最多 64 行为，未复刻淘宝多模态 embedding、超长日志、稀疏 kernel 和线上服务。本地对照口径：基线是 recent-window dense proxy；实验组使用三层 codes、hierarchical voting 和 soft routing，NDCG@10 0.03540→0.03586，相对 +1.31%，Hit@10 相对 -4.35%。  long-sequence sparse-activation semantic-id 搜广推 用户历史与排序骨干 HiSAC 的 interest agent 为什么不是实时运行的一组语言 agent？ 这里 agent 是由层级语义码和用户行为汇聚的兴趣表示，当前 query 路由到少数相关节点，不意味着每个节点都会独立调用 LLM 推理。名称描述组织角色，实际算子是量化、投票与加权聚合。理解这一点可避免误估能力和服务成本。 示意：摄影与露营 agent 可只是两份汇聚向量，查询选择其中一份；它们不需要互发消息或生成长回答才能完成一次检索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-hisac-bc7a3c37" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5cf60ed6519d3925">HiSAC 的 interest agent 为什么不是实时运行的一组语言 agent？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahisac">HiSAC: Hierarchical Sparse Activation Compression for Ultra-long Sequence Modeling in Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这里 agent 是由层级语义码和用户行为汇聚的兴趣表示，当前 query 路由到少数相关节点，不意味着每个节点都会独立调用 LLM 推理。名称描述组织角色，实际算子是量化、投票与加权聚合。理解这一点可避免误估能力和服务成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>摄影与露营 agent 可只是两份汇聚向量，查询选择其中一份；它们不需要互发消息或生成长回答才能完成一次检索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.21009">原论文</a> · <a href="../../../../reproductions/2602.21009-hisac/">实现解读</a> · <a href="#qa-5cf60ed6519d3925">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hisac" data-paper-title="HiSAC: Hierarchical Sparse Activation Compression for Ultra-long Sequence Modeling in Recommenders" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="HiSAC: Hierarchical Sparse Activation Compression for Ultra-long Sequence Modeling in Recommenders 搜广推与 LLM 应用 Alibaba / Taobao 2026-02-24 超长行为全量 attention 成本高，固定压缩又损失长尾兴趣。HiSAC 用多模态 RQ-VAE 形成层级 code，逐层投票生成用户特定 interest agents，再让当前 query 只 soft-route 到少量相关 agent。 Fidelity: 核心机制复现。执行 residual codes、层级投票、兴趣 agent 与 soft routing。本地最多 64 行为，未复刻淘宝多模态 embedding、超长日志、稀疏 kernel 和线上服务。本地对照口径：基线是 recent-window dense proxy；实验组使用三层 codes、hierarchical voting 和 soft routing，NDCG@10 0.03540→0.03586，相对 +1.31%，Hit@10 相对 -4.35%。  long-sequence sparse-activation semantic-id 搜广推 用户历史与排序骨干 HiSAC为什么先形成层级interest agents，再让当前query只路由到少量agent？ 全历史attention昂贵，固定单摘要又易丢长尾兴趣。层级码与投票先把行为组织成用户特定兴趣表示，query再选择相关部分，减少逐请求需要读取的状态。兴趣agent不是能自由推理的独立LLM，而是结构化压缩单元；若层级划分或路由遗漏稀有兴趣，后续聚合也无法自动恢复。 示意：长历史里有摄影、烹饪和骑行三组兴趣，推荐镜头时主要读取摄影agent；若把少量天文摄影行为压掉，再精确的query路由也找不到那部分证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-4e26b8af5e5c89d6">HiSAC为什么先形成层级interest agents，再让当前query只路由到少量agent？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahisac">HiSAC: Hierarchical Sparse Activation Compression for Ultra-long Sequence Modeling in Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全历史attention昂贵，固定单摘要又易丢长尾兴趣。层级码与投票先把行为组织成用户特定兴趣表示，query再选择相关部分，减少逐请求需要读取的状态。兴趣agent不是能自由推理的独立LLM，而是结构化压缩单元；若层级划分或路由遗漏稀有兴趣，后续聚合也无法自动恢复。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>长历史里有摄影、烹饪和骑行三组兴趣，推荐镜头时主要读取摄影agent；若把少量天文摄影行为压掉，再精确的query路由也找不到那部分证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.21009">原论文</a> · <a href="../../../../reproductions/2602.21009-hisac/">实现解读</a> · <a href="#qa-4e26b8af5e5c89d6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hisac" data-paper-title="HiSAC: Hierarchical Sparse Activation Compression for Ultra-long Sequence Modeling in Recommenders" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="HiSAC: Hierarchical Sparse Activation Compression for Ultra-long Sequence Modeling in Recommenders 搜广推与 LLM 应用 Alibaba / Taobao 2026-02-24 超长行为全量 attention 成本高，固定压缩又损失长尾兴趣。HiSAC 用多模态 RQ-VAE 形成层级 code，逐层投票生成用户特定 interest agents，再让当前 query 只 soft-route 到少量相关 agent。 Fidelity: 核心机制复现。执行 residual codes、层级投票、兴趣 agent 与 soft routing。本地最多 64 行为，未复刻淘宝多模态 embedding、超长日志、稀疏 kernel 和线上服务。本地对照口径：基线是 recent-window dense proxy；实验组使用三层 codes、hierarchical voting 和 soft routing，NDCG@10 0.03540→0.03586，相对 +1.31%，Hit@10 相对 -4.35%。  long-sequence sparse-activation semantic-id 搜广推 用户历史与排序骨干 HiSAC 的层级兴趣路由与固定单个用户向量，保留了什么选择空间？ 多个层级节点分别保留粗细兴趣，query 按需使用，减少把多峰兴趣平均掉的情况；单向量更省接口但难回到具体子兴趣。路由也可能漏掉低权重稀有需求，量化会损细节。来源小幅 NDCG 上升与 Hit 下降应分别解释。 示意：用户既摄影也跑步，相机 query 读摄影节点，跑鞋读运动节点；若压成一个平均向量，两种方向可能相互稀释。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-73ff7709cf627e84">HiSAC 的层级兴趣路由与固定单个用户向量，保留了什么选择空间？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahisac">HiSAC: Hierarchical Sparse Activation Compression for Ultra-long Sequence Modeling in Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多个层级节点分别保留粗细兴趣，query 按需使用，减少把多峰兴趣平均掉的情况；单向量更省接口但难回到具体子兴趣。路由也可能漏掉低权重稀有需求，量化会损细节。来源小幅 NDCG 上升与 Hit 下降应分别解释。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户既摄影也跑步，相机 query 读摄影节点，跑鞋读运动节点；若压成一个平均向量，两种方向可能相互稀释。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.21009">原论文</a> · <a href="../../../../reproductions/2602.21009-hisac/">实现解读</a> · <a href="#qa-73ff7709cf627e84">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hisac" data-paper-title="HiSAC: Hierarchical Sparse Activation Compression for Ultra-long Sequence Modeling in Recommenders" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="HiSAC: Hierarchical Sparse Activation Compression for Ultra-long Sequence Modeling in Recommenders 搜广推与 LLM 应用 Alibaba / Taobao 2026-02-24 超长行为全量 attention 成本高，固定压缩又损失长尾兴趣。HiSAC 用多模态 RQ-VAE 形成层级 code，逐层投票生成用户特定 interest agents，再让当前 query 只 soft-route 到少量相关 agent。 Fidelity: 核心机制复现。执行 residual codes、层级投票、兴趣 agent 与 soft routing。本地最多 64 行为，未复刻淘宝多模态 embedding、超长日志、稀疏 kernel 和线上服务。本地对照口径：基线是 recent-window dense proxy；实验组使用三层 codes、hierarchical voting 和 soft routing，NDCG@10 0.03540→0.03586，相对 +1.31%，Hit@10 相对 -4.35%。  long-sequence sparse-activation semantic-id 搜广推 用户历史与排序骨干 HiSAC 按 code 聚合行为时，为什么空节点与重复投票需要明确处理？ 节点均值按有效权重和归一，没有成员就没有可估兴趣，不能凭空生成强证据；层级投票和 query 子集选择要保留一致身份。重复行为的权重应按定义计入，不应把同一事件沿层展开误当多次独立消费。 示意：一条摄影行为在粗细两层都有节点，不代表用户消费两次；空的潜水节点更不能因初始化向量恰好相似而被当作真实兴趣。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b820ba3ed40479e1">HiSAC 按 code 聚合行为时，为什么空节点与重复投票需要明确处理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahisac">HiSAC: Hierarchical Sparse Activation Compression for Ultra-long Sequence Modeling in Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba / Taobao</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>节点均值按有效权重和归一，没有成员就没有可估兴趣，不能凭空生成强证据；层级投票和 query 子集选择要保留一致身份。重复行为的权重应按定义计入，不应把同一事件沿层展开误当多次独立消费。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一条摄影行为在粗细两层都有节点，不代表用户消费两次；空的潜水节点更不能因初始化向量恰好相似而被当作真实兴趣。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.21009">原论文</a> · <a href="../../../../reproductions/2602.21009-hisac/">实现解读</a> · <a href="#qa-b820ba3ed40479e1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ultra-hstu" data-paper-title="Bending the Scaling Law Curve in Large-Scale Recommendation Systems" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Bending the Scaling Law Curve in Large-Scale Recommendation Systems 搜广推与 LLM 应用 Meta 2026-02-19 原始 HSTU 扩展到 16k 行为和更深网络时，attention 与内存成本成为瓶颈。ULTRA-HSTU 用 semi-local attention 保留局部 token 和少量 landmark，LBSL 令越深层看到越宽范围，再以 Mixture of Transducers、attention truncation、混合精度和动态拓扑共同提升训练与推理斜率。 Fidelity: 核心机制复现。本地执行 semi-local attention、LBSL 逐层扩窗与 Mixture of Transducers。48-event 序列替代 16k 历史；不复刻 18 层生产模型、动态 topology、FP8 kernel 或 Meta 私有日志。本地对照口径：基线为 short-history transition-content ranker，实验组执行 ULTRA-HSTU compact core；NDCG@10 相对 -0.95%。  ranking long-sequence scaling-law attention serving 搜广推 用户历史与排序骨干 ULTRA-HSTU为什么在局部窗口之外加landmark？ 局部保细节，少量landmark连接远期信息，降低超长注意力成本；LBSL随深层扩大范围。它不是直接把原HSTU完整序列等价压缩，远期细节仍可能损失。 例如近期行为逐条读，远期用代表位置提供跨段联系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-ultra-hstu-194b1e9b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9fed2ecbf8d76051">ULTRA-HSTU为什么在局部窗口之外加landmark？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aultra-hstu">Bending the Scaling Law Curve in Large-Scale Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>局部保细节，少量landmark连接远期信息，降低超长注意力成本；LBSL随深层扩大范围。它不是直接把原HSTU完整序列等价压缩，远期细节仍可能损失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如近期行为逐条读，远期用代表位置提供跨段联系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.16986">原论文</a> · <a href="../../../../reproductions/2602.16986-ultra-hstu/">实现解读</a> · <a href="#qa-9fed2ecbf8d76051">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ultra-hstu" data-paper-title="Bending the Scaling Law Curve in Large-Scale Recommendation Systems" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Bending the Scaling Law Curve in Large-Scale Recommendation Systems 搜广推与 LLM 应用 Meta 2026-02-19 原始 HSTU 扩展到 16k 行为和更深网络时，attention 与内存成本成为瓶颈。ULTRA-HSTU 用 semi-local attention 保留局部 token 和少量 landmark，LBSL 令越深层看到越宽范围，再以 Mixture of Transducers、attention truncation、混合精度和动态拓扑共同提升训练与推理斜率。 Fidelity: 核心机制复现。本地执行 semi-local attention、LBSL 逐层扩窗与 Mixture of Transducers。48-event 序列替代 16k 历史；不复刻 18 层生产模型、动态 topology、FP8 kernel 或 Meta 私有日志。本地对照口径：基线为 short-history transition-content ranker，实验组执行 ULTRA-HSTU compact core；NDCG@10 相对 -0.95%。  ranking long-sequence scaling-law attention serving 搜广推 用户历史与排序骨干 ULTRA-HSTU 为什么在局部窗口之外保留 landmark，并让更深层扩大可见范围？ 只看固定局部窗口会失去远期连接，全连接又难承受长序列成本。landmark 提供稀疏全局通道，随层加宽的局部范围让深层逐步整合更远信息，再配合混合 transducer 和系统优化扩展规模。稀疏模式改变可达路径，不是无损替代全注意力；端到端效率还受窗口、landmark 数和具体内核影响。 示意：浅层先理解最近几次点击，少量代表点连接过去兴趣，深层再扩大窗口组合更多上下文。像先看邻里再看城区，不能假设第一层已经读过所有历史细节。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-11dc09f7eb43dcda">ULTRA-HSTU 为什么在局部窗口之外保留 landmark，并让更深层扩大可见范围？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aultra-hstu">Bending the Scaling Law Curve in Large-Scale Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只看固定局部窗口会失去远期连接，全连接又难承受长序列成本。landmark 提供稀疏全局通道，随层加宽的局部范围让深层逐步整合更远信息，再配合混合 transducer 和系统优化扩展规模。稀疏模式改变可达路径，不是无损替代全注意力；端到端效率还受窗口、landmark 数和具体内核影响。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>浅层先理解最近几次点击，少量代表点连接过去兴趣，深层再扩大窗口组合更多上下文。像先看邻里再看城区，不能假设第一层已经读过所有历史细节。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.16986">原论文</a> · <a href="../../../../reproductions/2602.16986-ultra-hstu/">实现解读</a> · <a href="#qa-11dc09f7eb43dcda">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ultra-hstu" data-paper-title="Bending the Scaling Law Curve in Large-Scale Recommendation Systems" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Bending the Scaling Law Curve in Large-Scale Recommendation Systems 搜广推与 LLM 应用 Meta 2026-02-19 原始 HSTU 扩展到 16k 行为和更深网络时，attention 与内存成本成为瓶颈。ULTRA-HSTU 用 semi-local attention 保留局部 token 和少量 landmark，LBSL 令越深层看到越宽范围，再以 Mixture of Transducers、attention truncation、混合精度和动态拓扑共同提升训练与推理斜率。 Fidelity: 核心机制复现。本地执行 semi-local attention、LBSL 逐层扩窗与 Mixture of Transducers。48-event 序列替代 16k 历史；不复刻 18 层生产模型、动态 topology、FP8 kernel 或 Meta 私有日志。本地对照口径：基线为 short-history transition-content ranker，实验组执行 ULTRA-HSTU compact core；NDCG@10 相对 -0.95%。  ranking long-sequence scaling-law attention serving 搜广推 用户历史与排序骨干 semi-local加深层宽窗与所有层固定窗口有何差别？ 深层逐步获得更广上下文，固定窗每层只在相同局部连接。真实感受野还依堆叠和landmark，不能用一个窗口公式替代Mixture、精度和系统优化全套。 例如浅层细看会话，深层再联系跨会话兴趣。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c16315fe2bbd6913">semi-local加深层宽窗与所有层固定窗口有何差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aultra-hstu">Bending the Scaling Law Curve in Large-Scale Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>深层逐步获得更广上下文，固定窗每层只在相同局部连接。真实感受野还依堆叠和landmark，不能用一个窗口公式替代Mixture、精度和系统优化全套。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如浅层细看会话，深层再联系跨会话兴趣。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.16986">原论文</a> · <a href="../../../../reproductions/2602.16986-ultra-hstu/">实现解读</a> · <a href="#qa-c16315fe2bbd6913">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ultra-hstu" data-paper-title="Bending the Scaling Law Curve in Large-Scale Recommendation Systems" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Bending the Scaling Law Curve in Large-Scale Recommendation Systems 搜广推与 LLM 应用 Meta 2026-02-19 原始 HSTU 扩展到 16k 行为和更深网络时，attention 与内存成本成为瓶颈。ULTRA-HSTU 用 semi-local attention 保留局部 token 和少量 landmark，LBSL 令越深层看到越宽范围，再以 Mixture of Transducers、attention truncation、混合精度和动态拓扑共同提升训练与推理斜率。 Fidelity: 核心机制复现。本地执行 semi-local attention、LBSL 逐层扩窗与 Mixture of Transducers。48-event 序列替代 16k 历史；不复刻 18 层生产模型、动态 topology、FP8 kernel 或 Meta 私有日志。本地对照口径：基线为 short-history transition-content ranker，实验组执行 ULTRA-HSTU compact core；NDCG@10 相对 -0.95%。  ranking long-sequence scaling-law attention serving 搜广推 用户历史与排序骨干 48-event本地消融能证明16k生产scaling law吗？ 不能，缺少18层生产模型、动态拓扑、FP8内核和私有日志。结构计数或小样本分数只检验路径，扩展曲线需多规模同协议训练与设备测量。 例如把最大长度配置写16000但只喂几十条，不算超长验证。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-265d87b066b4fd3e">48-event本地消融能证明16k生产scaling law吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aultra-hstu">Bending the Scaling Law Curve in Large-Scale Recommendation Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，缺少18层生产模型、动态拓扑、FP8内核和私有日志。结构计数或小样本分数只检验路径，扩展曲线需多规模同协议训练与设备测量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把最大长度配置写16000但只喂几十条，不算超长验证。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.16986">原论文</a> · <a href="../../../../reproductions/2602.16986-ultra-hstu/">实现解读</a> · <a href="#qa-265d87b066b4fd3e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mixformer" data-paper-title="MixFormer: Co-Scaling Up Dense and Sequence in Industrial Recommenders" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="MixFormer: Co-Scaling Up Dense and Sequence in Industrial Recommenders 搜广推与 LLM 应用 ByteDance / Douyin 2026-02-15 现有推荐模型通常把 dense feature interaction 与 behavior-sequence Transformer 做成两个独立模块，模型预算必须在两边手工分配，且交互只发生在末端。MixFormer 将非序列字段和行为序列统一成同一 Transformer token space，共享参数、逐层发生高阶交互，从而联合扩大 dense capacity 与 sequence length。 Fidelity: 完整核心链路复现。当前代码在 matched local budget 下实际训练 stacked baseline 与 unified MixFormer blocks；proposed 将 dense feature-split tokens 和行为 tokens 放进共享 backbone，并复用 user encoding 对所有候选打分。本地对照口径：基线是参数量匹配的 Stacked Dense+Sequence；实验组是 Unified MixFormer；NDCG@10 从 0.0054 升至 0.0063（+17.41%）。   搜广推 用户历史与排序骨干 MixFormer 的统一 token space 为什么要同时包含稠密字段与行为序列？ 字段交互和序列兴趣分别编码会推迟信息交流，统一空间使多层共同更新，两种容量可联合扩展。异构字段仍需适当投影，不等于把它们都当语言词。服务再解耦用户与候选依赖，统一训练不代表所有状态都可公共缓存。 示意：雨天场景字段可在早层帮助解释户外浏览，更新后的兴趣又影响字段组合，而不必等两塔最终拼接才看到对方。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-mixformer-c586b532" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f3c5d69fa3b41645">MixFormer 的统一 token space 为什么要同时包含稠密字段与行为序列？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amixformer">MixFormer: Co-Scaling Up Dense and Sequence in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>字段交互和序列兴趣分别编码会推迟信息交流，统一空间使多层共同更新，两种容量可联合扩展。异构字段仍需适当投影，不等于把它们都当语言词。服务再解耦用户与候选依赖，统一训练不代表所有状态都可公共缓存。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>雨天场景字段可在早层帮助解释户外浏览，更新后的兴趣又影响字段组合，而不必等两塔最终拼接才看到对方。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.14110">原论文</a> · <a href="../../../../reproductions/2602.14110-mixformer/">实现解读</a> · <a href="#qa-f3c5d69fa3b41645">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mixformer" data-paper-title="MixFormer: Co-Scaling Up Dense and Sequence in Industrial Recommenders" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="MixFormer: Co-Scaling Up Dense and Sequence in Industrial Recommenders 搜广推与 LLM 应用 ByteDance / Douyin 2026-02-15 现有推荐模型通常把 dense feature interaction 与 behavior-sequence Transformer 做成两个独立模块，模型预算必须在两边手工分配，且交互只发生在末端。MixFormer 将非序列字段和行为序列统一成同一 Transformer token space，共享参数、逐层发生高阶交互，从而联合扩大 dense capacity 与 sequence length。 Fidelity: 完整核心链路复现。当前代码在 matched local budget 下实际训练 stacked baseline 与 unified MixFormer blocks；proposed 将 dense feature-split tokens 和行为 tokens 放进共享 backbone，并复用 user encoding 对所有候选打分。本地对照口径：基线是参数量匹配的 Stacked Dense+Sequence；实验组是 Unified MixFormer；NDCG@10 从 0.0054 升至 0.0063（+17.41%）。   搜广推 用户历史与排序骨干 MixFormer 把稠密字段和行为序列放进同一 token 空间，和两个塔最后拼接有什么信息流区别？ 末端拼接时，字段交互与序列编码先各自完成，早期层无法根据对方的信息调整表示。MixFormer 让两类 token 在多层统一交互中共同更新，把预算和参数用于联合建模。服务时再解耦可共享的用户计算与候选相关计算；统一建模不等于每个候选都重算完整用户历史。 示意：用户刚连续浏览户外装备，当前场景是雨天。统一层可以在建模历史时利用场景字段，逐层强化防水需求；末端拼接只能拿已压缩的两份表示再组合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-7b0558ebad0e78da">MixFormer 把稠密字段和行为序列放进同一 token 空间，和两个塔最后拼接有什么信息流区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amixformer">MixFormer: Co-Scaling Up Dense and Sequence in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>末端拼接时，字段交互与序列编码先各自完成，早期层无法根据对方的信息调整表示。MixFormer 让两类 token 在多层统一交互中共同更新，把预算和参数用于联合建模。服务时再解耦可共享的用户计算与候选相关计算；统一建模不等于每个候选都重算完整用户历史。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户刚连续浏览户外装备，当前场景是雨天。统一层可以在建模历史时利用场景字段，逐层强化防水需求；末端拼接只能拿已压缩的两份表示再组合。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.14110">原论文</a> · <a href="../../../../reproductions/2602.14110-mixformer/">实现解读</a> · <a href="#qa-7b0558ebad0e78da">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mixformer" data-paper-title="MixFormer: Co-Scaling Up Dense and Sequence in Industrial Recommenders" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="MixFormer: Co-Scaling Up Dense and Sequence in Industrial Recommenders 搜广推与 LLM 应用 ByteDance / Douyin 2026-02-15 现有推荐模型通常把 dense feature interaction 与 behavior-sequence Transformer 做成两个独立模块，模型预算必须在两边手工分配，且交互只发生在末端。MixFormer 将非序列字段和行为序列统一成同一 Transformer token space，共享参数、逐层发生高阶交互，从而联合扩大 dense capacity 与 sequence length。 Fidelity: 完整核心链路复现。当前代码在 matched local budget 下实际训练 stacked baseline 与 unified MixFormer blocks；proposed 将 dense feature-split tokens 和行为 tokens 放进共享 backbone，并复用 user encoding 对所有候选打分。本地对照口径：基线是参数量匹配的 Stacked Dense+Sequence；实验组是 Unified MixFormer；NDCG@10 从 0.0054 升至 0.0063（+17.41%）。   搜广推 用户历史与排序骨干 MixFormer 对参数匹配 stacked baseline 的比较，为什么比旧固定 semantic-gate 更能隔离架构？ 匹配两边预算并真实训练 stacked 与 unified，才能更接近比较交互组织，而固定打分门控只是代理。参数相近仍不消除优化难度、数据特征与方差差异。来源已撤旧代理，不能把旧数字混为同一实验或声称稳定工业幅度。 示意：两层统一网络与同量级独立两塔比较有架构意义；给现成分数加一个语义常数，只能测融合规则，不是统一 Transformer 训练。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1bc780cf4206ff6c">MixFormer 对参数匹配 stacked baseline 的比较，为什么比旧固定 semantic-gate 更能隔离架构？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amixformer">MixFormer: Co-Scaling Up Dense and Sequence in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>匹配两边预算并真实训练 stacked 与 unified，才能更接近比较交互组织，而固定打分门控只是代理。参数相近仍不消除优化难度、数据特征与方差差异。来源已撤旧代理，不能把旧数字混为同一实验或声称稳定工业幅度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两层统一网络与同量级独立两塔比较有架构意义；给现成分数加一个语义常数，只能测融合规则，不是统一 Transformer 训练。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.14110">原论文</a> · <a href="../../../../reproductions/2602.14110-mixformer/">实现解读</a> · <a href="#qa-1bc780cf4206ff6c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mixformer" data-paper-title="MixFormer: Co-Scaling Up Dense and Sequence in Industrial Recommenders" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="MixFormer: Co-Scaling Up Dense and Sequence in Industrial Recommenders 搜广推与 LLM 应用 ByteDance / Douyin 2026-02-15 现有推荐模型通常把 dense feature interaction 与 behavior-sequence Transformer 做成两个独立模块，模型预算必须在两边手工分配，且交互只发生在末端。MixFormer 将非序列字段和行为序列统一成同一 Transformer token space，共享参数、逐层发生高阶交互，从而联合扩大 dense capacity 与 sequence length。 Fidelity: 完整核心链路复现。当前代码在 matched local budget 下实际训练 stacked baseline 与 unified MixFormer blocks；proposed 将 dense feature-split tokens 和行为 tokens 放进共享 backbone，并复用 user encoding 对所有候选打分。本地对照口径：基线是参数量匹配的 Stacked Dense+Sequence；实验组是 Unified MixFormer；NDCG@10 从 0.0054 升至 0.0063（+17.41%）。   搜广推 用户历史与排序骨干 MixFormer 本地一次 user encoding 后点积全候选，为什么要检查 candidate 是否进入公共主干？ 若候选已写入统一用户状态，换候选不能直接复用；本地把用户字段与历史先统一编码，候选通过后续向量打分，才满足一次编码。应以实际依赖判断共享，不由“unified”名称推断。公开 genre 替代私有字段也限制保真范围。 示意：用户侧四字段与三十二行为先成一个向量，候选相机和鞋各自点积合法；若相机先被拼入主干，再把输出给鞋就不是同一路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-cd3913255c1e2934">MixFormer 本地一次 user encoding 后点积全候选，为什么要检查 candidate 是否进入公共主干？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amixformer">MixFormer: Co-Scaling Up Dense and Sequence in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若候选已写入统一用户状态，换候选不能直接复用；本地把用户字段与历史先统一编码，候选通过后续向量打分，才满足一次编码。应以实际依赖判断共享，不由“unified”名称推断。公开 genre 替代私有字段也限制保真范围。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户侧四字段与三十二行为先成一个向量，候选相机和鞋各自点积合法；若相机先被拼入主干，再把输出给鞋就不是同一路径。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.14110">原论文</a> · <a href="../../../../reproductions/2602.14110-mixformer/">实现解读</a> · <a href="#qa-cd3913255c1e2934">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:linkedin-feed-sr" data-paper-title="An Industrial-Scale Sequential Recommender for LinkedIn Feed Ranking" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="An Industrial-Scale Sequential Recommender for LinkedIn Feed Ranking 搜广推与 LLM 应用 LinkedIn 2026-02-12 将 Feed 候选、交互历史和上下文统一成超长序列，采用 HSTU 式目标注意力、负样本自由评估及增量服务优化。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 linkedin-feed-sr 核心机制，相对 NDCG@10 -0.12%。  ranking sequential-recommendation long-sequence 搜广推 用户历史与排序骨干 LinkedIn Feed 为什么将候选、交互历史和上下文统一为序列？ 不同输入共同影响当前内容价值，序列接口让目标相关信息在同一骨干交互，避免多模块只在末端接合。超长历史可保留长期职业兴趣，也增加计算与候选依赖，需增量服务优化。统一表示不保证所有状态可跨候选复用。 示意：用户近期求职，长期关注技术，当前候选是招聘信息；历史与上下文共同解释其价值，比只记录曾点赞文章集合更有条件性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-linkedin-feed-sr-d07e7f6a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5c0c37f2494e9faa">LinkedIn Feed 为什么将候选、交互历史和上下文统一为序列？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alinkedin-feed-sr">An Industrial-Scale Sequential Recommender for LinkedIn Feed Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同输入共同影响当前内容价值，序列接口让目标相关信息在同一骨干交互，避免多模块只在末端接合。超长历史可保留长期职业兴趣，也增加计算与候选依赖，需增量服务优化。统一表示不保证所有状态可跨候选复用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户近期求职，长期关注技术，当前候选是招聘信息；历史与上下文共同解释其价值，比只记录曾点赞文章集合更有条件性。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12354">原论文</a> · <a href="../../../../reproductions/2602.12354-linkedin-feed-sr/">实现解读</a> · <a href="#qa-5c0c37f2494e9faa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:linkedin-feed-sr" data-paper-title="An Industrial-Scale Sequential Recommender for LinkedIn Feed Ranking" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="An Industrial-Scale Sequential Recommender for LinkedIn Feed Ranking 搜广推与 LLM 应用 LinkedIn 2026-02-12 将 Feed 候选、交互历史和上下文统一成超长序列，采用 HSTU 式目标注意力、负样本自由评估及增量服务优化。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 linkedin-feed-sr 核心机制，相对 NDCG@10 -0.12%。  ranking sequential-recommendation long-sequence 搜广推 用户历史与排序骨干 LinkedIn Feed序列模型为什么强调不依赖随机负采样的评价？ 随机抽少量容易负例会把排名任务变简单，掩盖大候选池中真正难区分的物品关系。统一候选、历史和上下文的序列模型需要在明确且一致的实际候选口径下评价，才能判断扩展与增量服务是否保留质量。本地代理排序不等于LinkedIn生产候选分布，更不能混用不同负例数量比较提升。 示意：在一个正例加九个明显无关内容中命中，和从数千相近Feed候选中找出同一内容不是同一难度；即使模型相同，两种指标也不能直接相减。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-35861795e0c6722e">LinkedIn Feed序列模型为什么强调不依赖随机负采样的评价？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alinkedin-feed-sr">An Industrial-Scale Sequential Recommender for LinkedIn Feed Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>随机抽少量容易负例会把排名任务变简单，掩盖大候选池中真正难区分的物品关系。统一候选、历史和上下文的序列模型需要在明确且一致的实际候选口径下评价，才能判断扩展与增量服务是否保留质量。本地代理排序不等于LinkedIn生产候选分布，更不能混用不同负例数量比较提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>在一个正例加九个明显无关内容中命中，和从数千相近Feed候选中找出同一内容不是同一难度；即使模型相同，两种指标也不能直接相减。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12354">原论文</a> · <a href="../../../../reproductions/2602.12354-linkedin-feed-sr/">实现解读</a> · <a href="#qa-35861795e0c6722e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:linkedin-feed-sr" data-paper-title="An Industrial-Scale Sequential Recommender for LinkedIn Feed Ranking" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="An Industrial-Scale Sequential Recommender for LinkedIn Feed Ranking 搜广推与 LLM 应用 LinkedIn 2026-02-12 将 Feed 候选、交互历史和上下文统一成超长序列，采用 HSTU 式目标注意力、负样本自由评估及增量服务优化。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 linkedin-feed-sr 核心机制，相对 NDCG@10 -0.12%。  ranking sequential-recommendation long-sequence 搜广推 用户历史与排序骨干 无随机负采样评价与一正加少量随机负例，相比检验难度为何不同？ 采样集合常缺少真正竞争候选，指标会随负例数量与难度变化，容易把模型排序能力估高。更完整候选口径接近真实分发竞争，但成本也更高。名称为负样本自由不表示训练无需负信号，更不能把不同候选协议百分比直接横比。 示意：在九十九篇随机无关文章中找目标较容易，在完整专业内容库中还要胜过许多相似文章；相同 NDCG 名称并不代表同一任务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-500035993adfd631">无随机负采样评价与一正加少量随机负例，相比检验难度为何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alinkedin-feed-sr">An Industrial-Scale Sequential Recommender for LinkedIn Feed Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>采样集合常缺少真正竞争候选，指标会随负例数量与难度变化，容易把模型排序能力估高。更完整候选口径接近真实分发竞争，但成本也更高。名称为负样本自由不表示训练无需负信号，更不能把不同候选协议百分比直接横比。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>在九十九篇随机无关文章中找目标较容易，在完整专业内容库中还要胜过许多相似文章；相同 NDCG 名称并不代表同一任务。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12354">原论文</a> · <a href="../../../../reproductions/2602.12354-linkedin-feed-sr/">实现解读</a> · <a href="#qa-500035993adfd631">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:linkedin-feed-sr" data-paper-title="An Industrial-Scale Sequential Recommender for LinkedIn Feed Ranking" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="An Industrial-Scale Sequential Recommender for LinkedIn Feed Ranking 搜广推与 LLM 应用 LinkedIn 2026-02-12 将 Feed 候选、交互历史和上下文统一成超长序列，采用 HSTU 式目标注意力、负样本自由评估及增量服务优化。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 linkedin-feed-sr 核心机制，相对 NDCG@10 -0.12%。  ranking sequential-recommendation long-sequence 搜广推 用户历史与排序骨干 Feed 序列增量服务为什么要先验证候选无关历史状态？ 可复用前缀必须不依赖待替换候选，历史变化与模型更新也会改变缓存有效性。目标注意力可以在候选侧读取公共状态，不允许无说明把已交互状态缓存给其他候选。来源本地核心代理缺完整 LinkedIn 系统，不能当真实超长序列吞吐证据。 示意：新文章候选只改查询时可读旧历史 K/V；若它已写回历史，再给另一文章共享就污染，程序运行很快也不符合复用契约。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b6718059174fd2c3">Feed 序列增量服务为什么要先验证候选无关历史状态？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alinkedin-feed-sr">An Industrial-Scale Sequential Recommender for LinkedIn Feed Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>可复用前缀必须不依赖待替换候选，历史变化与模型更新也会改变缓存有效性。目标注意力可以在候选侧读取公共状态，不允许无说明把已交互状态缓存给其他候选。来源本地核心代理缺完整 LinkedIn 系统，不能当真实超长序列吞吐证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新文章候选只改查询时可读旧历史 K/V；若它已写回历史，再给另一文章共享就污染，程序运行很快也不符合复用契约。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12354">原论文</a> · <a href="../../../../reproductions/2602.12354-linkedin-feed-sr/">实现解读</a> · <a href="#qa-b6718059174fd2c3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mlcc" data-paper-title="Compress, Cross and Scale: Multi-Level Compression Cross Networks for Efficient Scaling in Recommender Systems" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Compress, Cross and Scale: Multi-Level Compression Cross Networks for Efficient Scaling in Recommender Systems 搜广推与 LLM 应用 Bilibili 2026-02-12 在每一层先压缩高维特征，再在紧凑空间执行动态显式交叉并回注主干；MC-MLCC 使用多个并行子空间横向扩展表达力，使参数和 FLOPs 增长更可控。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05530，相对变化 +2.40%。本地代理目标与论文生产任务不同，不能外推线上 lift。  feature-interaction compression scaling-law 搜广推 用户历史与排序骨干 MLCC 为什么把紧凑空间交叉结果重新回注高维主干？ 低维 z 负责控制交互成本，高维残差主干继续保留原信息，回投 P 将新组合补充进去，避免所有层只困在同一压缩空间。压缩仍可能漏掉关键方向，残差只能保留已有信息，不能保证每个高阶交叉都被学到。 示意：先用小空间组合预算与品类，再把结果加回全部字段表示，其他原特征仍可继续参与下一层，而不是被一次降维全部替换。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-mlcc-9b40fb24" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5652f96f3280d4b4">MLCC 为什么把紧凑空间交叉结果重新回注高维主干？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amlcc">Compress, Cross and Scale: Multi-Level Compression Cross Networks for Efficient Scaling in Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Bilibili</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>低维 z 负责控制交互成本，高维残差主干继续保留原信息，回投 P 将新组合补充进去，避免所有层只困在同一压缩空间。压缩仍可能漏掉关键方向，残差只能保留已有信息，不能保证每个高阶交叉都被学到。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先用小空间组合预算与品类，再把结果加回全部字段表示，其他原特征仍可继续参与下一层，而不是被一次降维全部替换。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12041">原论文</a> · <a href="../../../../reproductions/2602.12041-mlcc/">实现解读</a> · <a href="#qa-5652f96f3280d4b4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mlcc" data-paper-title="Compress, Cross and Scale: Multi-Level Compression Cross Networks for Efficient Scaling in Recommender Systems" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Compress, Cross and Scale: Multi-Level Compression Cross Networks for Efficient Scaling in Recommender Systems 搜广推与 LLM 应用 Bilibili 2026-02-12 在每一层先压缩高维特征，再在紧凑空间执行动态显式交叉并回注主干；MC-MLCC 使用多个并行子空间横向扩展表达力，使参数和 FLOPs 增长更可控。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05530，相对变化 +2.40%。本地代理目标与论文生产任务不同，不能外推线上 lift。  feature-interaction compression scaling-law 搜广推 用户历史与排序骨干 MLCC 为什么每层先压缩再做显式交叉，而不是只在输入端压缩一次？ 每层表示已经包含不同阶的交互，逐层压缩让后续交叉依赖当前状态，而不是始终围绕同一份输入投影。紧凑空间内的动态交叉再回注主干，控制高维运算的开销。多个并行子空间可覆盖不同关系，但表达力取决于压缩是否保留关键方向，不能把压缩视为无损操作。 示意：第一层先组合“地区与品类”，第二层可压缩这份新表示，再与价格偏好交叉；若只压缩最初字段，后续难以重新选择已形成的高阶关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-0f3168e9435168fe">MLCC 为什么每层先压缩再做显式交叉，而不是只在输入端压缩一次？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amlcc">Compress, Cross and Scale: Multi-Level Compression Cross Networks for Efficient Scaling in Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Bilibili</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每层表示已经包含不同阶的交互，逐层压缩让后续交叉依赖当前状态，而不是始终围绕同一份输入投影。紧凑空间内的动态交叉再回注主干，控制高维运算的开销。多个并行子空间可覆盖不同关系，但表达力取决于压缩是否保留关键方向，不能把压缩视为无损操作。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第一层先组合“地区与品类”，第二层可压缩这份新表示，再与价格偏好交叉；若只压缩最初字段，后续难以重新选择已形成的高阶关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12041">原论文</a> · <a href="../../../../reproductions/2602.12041-mlcc/">实现解读</a> · <a href="#qa-0f3168e9435168fe">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mlcc" data-paper-title="Compress, Cross and Scale: Multi-Level Compression Cross Networks for Efficient Scaling in Recommender Systems" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Compress, Cross and Scale: Multi-Level Compression Cross Networks for Efficient Scaling in Recommender Systems 搜广推与 LLM 应用 Bilibili 2026-02-12 在每一层先压缩高维特征，再在紧凑空间执行动态显式交叉并回注主干；MC-MLCC 使用多个并行子空间横向扩展表达力，使参数和 FLOPs 增长更可控。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05530，相对变化 +2.40%。本地代理目标与论文生产任务不同，不能外推线上 lift。  feature-interaction compression scaling-law 搜广推 用户历史与排序骨干 MC-MLCC 多并行子空间与只扩大单个压缩维度，相比归纳偏置有何不同？ 多个子空间可分别学习不同交叉方向并横向组合，单大空间把容量集中在一个映射里。前者可能更易分工也可能重复，实际参数与 FLOPs 需匹配才可判断。来源机制描述不支持“多通道一定更省且更准”的普遍结论。 示意：一个子空间学习价格—预算，另一个学时间—场景，比同样宽度无分工投影更显式；但若两路都学热门度，容量并未互补。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-acd8a77f6ca3a463">MC-MLCC 多并行子空间与只扩大单个压缩维度，相比归纳偏置有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amlcc">Compress, Cross and Scale: Multi-Level Compression Cross Networks for Efficient Scaling in Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Bilibili</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多个子空间可分别学习不同交叉方向并横向组合，单大空间把容量集中在一个映射里。前者可能更易分工也可能重复，实际参数与 FLOPs 需匹配才可判断。来源机制描述不支持“多通道一定更省且更准”的普遍结论。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个子空间学习价格—预算，另一个学时间—场景，比同样宽度无分工投影更显式；但若两路都学热门度，容量并未互补。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12041">原论文</a> · <a href="../../../../reproductions/2602.12041-mlcc/">实现解读</a> · <a href="#qa-acd8a77f6ca3a463">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mlcc" data-paper-title="Compress, Cross and Scale: Multi-Level Compression Cross Networks for Efficient Scaling in Recommender Systems" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Compress, Cross and Scale: Multi-Level Compression Cross Networks for Efficient Scaling in Recommender Systems 搜广推与 LLM 应用 Bilibili 2026-02-12 在每一层先压缩高维特征，再在紧凑空间执行动态显式交叉并回注主干；MC-MLCC 使用多个并行子空间横向扩展表达力，使参数和 FLOPs 增长更可控。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05530，相对变化 +2.40%。本地代理目标与论文生产任务不同，不能外推线上 lift。  feature-interaction compression scaling-law 搜广推 用户历史与排序骨干 MLCC 每层的 Cl 与 Pl 为什么必须与该层状态一致？ z 由当前 xl 压缩，动态门依该 z 计算，回投再映到 xl 的维度。若误用最初输入的压缩或共享错层参数，逐层高阶更新会退化。残差形状正确仅是起点，还应核对每层实际接收到上层新状态。 示意：第二层应压缩已经含第一层交叉的表示，若仍用原始 x0 生成 z，两层可能只是重复同一种交叉，而没有递进利用新关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7e302b2505b1994e">MLCC 每层的 Cl 与 Pl 为什么必须与该层状态一致？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amlcc">Compress, Cross and Scale: Multi-Level Compression Cross Networks for Efficient Scaling in Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Bilibili</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>z 由当前 xl 压缩，动态门依该 z 计算，回投再映到 xl 的维度。若误用最初输入的压缩或共享错层参数，逐层高阶更新会退化。残差形状正确仅是起点，还应核对每层实际接收到上层新状态。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第二层应压缩已经含第一层交叉的表示，若仍用原始 x0 生成 z，两层可能只是重复同一种交叉，而没有递进利用新关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12041">原论文</a> · <a href="../../../../reproductions/2602.12041-mlcc/">实现解读</a> · <a href="#qa-7e302b2505b1994e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cadet" data-paper-title="CADET: Context-Conditioned Ads CTR Prediction With a Decoder-Only Transformer" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="CADET: Context-Conditioned Ads CTR Prediction With a Decoder-Only Transformer 搜广推与 LLM 应用 LinkedIn 2026-02-11 Decoder-only Transformer 先编码可缓存历史，候选打分后再注入 post-scoring context，避免训练与服务错位并统一广告 CTR 模型。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 cadet 核心机制，相对 NDCG@10 -6.20%。  advertising ctr-prediction decoder-only-transformer 搜广推 用户历史与排序骨干 CADET 为什么强调 post-scoring context 的可见时点？ 训练日志可能包含候选打分以后才产生的信息，若在评分前使用就会造成训练服务错位。把可缓存历史先编码，再按合法阶段接入上下文，明确哪些信息在预测当时可知。时间顺序是特征契约，不是多加一类 token 就能忽略的细节。 示意：推荐展示后的用户反应可以成为下一次历史，却不能用于预测本次点击；训练里若把它提前拼入输入，离线会看起来更准而上线不可执行。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-cadet-4647b60d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b40ffc952504d31e">CADET 为什么强调 post-scoring context 的可见时点？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acadet">CADET: Context-Conditioned Ads CTR Prediction With a Decoder-Only Transformer</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>训练日志可能包含候选打分以后才产生的信息，若在评分前使用就会造成训练服务错位。把可缓存历史先编码，再按合法阶段接入上下文，明确哪些信息在预测当时可知。时间顺序是特征契约，不是多加一类 token 就能忽略的细节。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>推荐展示后的用户反应可以成为下一次历史，却不能用于预测本次点击；训练里若把它提前拼入输入，离线会看起来更准而上线不可执行。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.11410">原论文</a> · <a href="../../../../reproductions/2602.11410-cadet/">实现解读</a> · <a href="#qa-b40ffc952504d31e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cadet" data-paper-title="CADET: Context-Conditioned Ads CTR Prediction With a Decoder-Only Transformer" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="CADET: Context-Conditioned Ads CTR Prediction With a Decoder-Only Transformer 搜广推与 LLM 应用 LinkedIn 2026-02-11 Decoder-only Transformer 先编码可缓存历史，候选打分后再注入 post-scoring context，避免训练与服务错位并统一广告 CTR 模型。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 cadet 核心机制，相对 NDCG@10 -6.20%。  advertising ctr-prediction decoder-only-transformer 搜广推 用户历史与排序骨干 CADET为什么要把可缓存历史和post-scoring context放在不同的信息流阶段？ 缓存历史必须在候选或后续上下文变化时仍保持语义有效。CADET先编码历史并进行候选打分，再在规定阶段注入post-scoring context，避免训练时借到服务打分点尚不可用的信号。若把所有信息一开始混入序列，即使离线分更高，也可能破坏复用条件并造成训练与服务错位。 示意：同一历史对应多个待评广告，不能把广告A打分后的上下文写进共享历史再给广告B；应保持共享前缀与后续条件化状态的明确边界。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-3572deb35e23e95e">CADET为什么要把可缓存历史和post-scoring context放在不同的信息流阶段？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acadet">CADET: Context-Conditioned Ads CTR Prediction With a Decoder-Only Transformer</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>缓存历史必须在候选或后续上下文变化时仍保持语义有效。CADET先编码历史并进行候选打分，再在规定阶段注入post-scoring context，避免训练时借到服务打分点尚不可用的信号。若把所有信息一开始混入序列，即使离线分更高，也可能破坏复用条件并造成训练与服务错位。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一历史对应多个待评广告，不能把广告A打分后的上下文写进共享历史再给广告B；应保持共享前缀与后续条件化状态的明确边界。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.11410">原论文</a> · <a href="../../../../reproductions/2602.11410-cadet/">实现解读</a> · <a href="#qa-3572deb35e23e95e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cadet" data-paper-title="CADET: Context-Conditioned Ads CTR Prediction With a Decoder-Only Transformer" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="CADET: Context-Conditioned Ads CTR Prediction With a Decoder-Only Transformer 搜广推与 LLM 应用 LinkedIn 2026-02-11 Decoder-only Transformer 先编码可缓存历史，候选打分后再注入 post-scoring context，避免训练与服务错位并统一广告 CTR 模型。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 cadet 核心机制，相对 NDCG@10 -6.20%。  advertising ctr-prediction decoder-only-transformer 搜广推 用户历史与排序骨干 CADET 的分阶段上下文与将全部日志字段一起输入 Transformer，差别在哪里？ 无差别拼接让模型可能利用不可用字段并把候选相关计算写入公共历史。分阶段信息流把公共可缓存部分与评分后上下文分开，牺牲一些任意交互自由换取服务一致性。来源本地仅公开数据代理，不能将其结果视作完整广告时序特征验证。 示意：当前请求特征和下一步行为日志若同时出现在同一序列，模型可能走捷径；规定接入阶段后只能使用请求发生时已存在的证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4ea6effe523c3e05">CADET 的分阶段上下文与将全部日志字段一起输入 Transformer，差别在哪里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acadet">CADET: Context-Conditioned Ads CTR Prediction With a Decoder-Only Transformer</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>无差别拼接让模型可能利用不可用字段并把候选相关计算写入公共历史。分阶段信息流把公共可缓存部分与评分后上下文分开，牺牲一些任意交互自由换取服务一致性。来源本地仅公开数据代理，不能将其结果视作完整广告时序特征验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>当前请求特征和下一步行为日志若同时出现在同一序列，模型可能走捷径；规定接入阶段后只能使用请求发生时已存在的证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.11410">原论文</a> · <a href="../../../../reproductions/2602.11410-cadet/">实现解读</a> · <a href="#qa-4ea6effe523c3e05">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:cadet" data-paper-title="CADET: Context-Conditioned Ads CTR Prediction With a Decoder-Only Transformer" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="CADET: Context-Conditioned Ads CTR Prediction With a Decoder-Only Transformer 搜广推与 LLM 应用 LinkedIn 2026-02-11 Decoder-only Transformer 先编码可缓存历史，候选打分后再注入 post-scoring context，避免训练与服务错位并统一广告 CTR 模型。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 cadet 核心机制，相对 NDCG@10 -6.20%。  advertising ctr-prediction decoder-only-transformer 搜广推 用户历史与排序骨干 CADET 缓存历史 K/V 时，如何判断新增上下文是否使旧缓存失效？ 应检查它是否改变历史编码输入、掩码或模型参数；若只在后续候选查询路径注入，原公共 K/V 才可保留。来源公式让上下文查询读取此前历史，不能反推所有上下文都可任意塞回缓存主干。每个张量的依赖比“用户侧”名称更重要。 示意：新上下文只改查询向量时可继续读历史缓存；若修改了历史事件时间编码，旧 K/V 已不对应同一输入，就应重新计算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e6af216519561e37">CADET 缓存历史 K/V 时，如何判断新增上下文是否使旧缓存失效？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Acadet">CADET: Context-Conditioned Ads CTR Prediction With a Decoder-Only Transformer</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · LinkedIn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>应检查它是否改变历史编码输入、掩码或模型参数；若只在后续候选查询路径注入，原公共 K/V 才可保留。来源公式让上下文查询读取此前历史，不能反推所有上下文都可任意塞回缓存主干。每个张量的依赖比“用户侧”名称更重要。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新上下文只改查询向量时可继续读历史缓存；若修改了历史事件时间编码，旧 K/V 已不对应同一输入，就应重新计算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.11410">原论文</a> · <a href="../../../../reproductions/2602.11410-cadet/">实现解读</a> · <a href="#qa-e6af216519561e37">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:kunlun" data-paper-title="Kunlun: Establishing Scaling Laws for Massive-Scale Recommendation Systems through Unified Architecture Design" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Kunlun: Establishing Scaling Laws for Massive-Scale Recommendation Systems through Unified Architecture Design 搜广推与 LLM 应用 Meta 2026-02-10 传统广告模型把序列塔、稠密交叉和系统并行分别优化，扩大规模后收益快速饱和。Kunlun 在每层同时放置 Transformer Block 与 Interaction Block：GDPA/PFFN 建模序列，HSP 汇总序列 seed，Global Interaction 交换序列与非序列信息；CompSkip 和 expert parallel 保持深层训练稳定与吞吐。 Fidelity: 核心机制复现。本地执行 GDPA、分层 seed pooling、expert routing 和 CompSkip；不声称复刻 Meta Ads 模型规模。本地仅验证网络算子和信息流；没有 Meta Ads 私有数据、万亿参数、expert parallel 或硬件 MFU 对照。本地对照口径：基线为 shallow transition-content ranker，实验组执行 Kunlun compact core；NDCG@10 相对 -5.25%。  ranking scaling-law long-sequence mixture-of-experts serving 搜广推 用户历史与排序骨干 Kunlun 为什么在同一层同时设置序列块和交互块？ 序列块提取行为依赖，交互块组合异构字段，Global Interaction 在层间交换信息，避免独立扩塔遇到沟通瓶颈。HSP 汇总序列 seed，系统并行和 CompSkip 又处理深层规模。多个组件承担不同问题，不能仅扩大一个 FFN 就称同结构。 示意：历史显露露营需求，用户预算字段在交互块中调整解读，再影响后续融合；两塔只末端拼接会更晚才看到对方线索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-kunlun-7994f8f7" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-062a5b981a1264df">Kunlun 为什么在同一层同时设置序列块和交互块？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Akunlun">Kunlun: Establishing Scaling Laws for Massive-Scale Recommendation Systems through Unified Architecture Design</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>序列块提取行为依赖，交互块组合异构字段，Global Interaction 在层间交换信息，避免独立扩塔遇到沟通瓶颈。HSP 汇总序列 seed，系统并行和 CompSkip 又处理深层规模。多个组件承担不同问题，不能仅扩大一个 FFN 就称同结构。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>历史显露露营需求，用户预算字段在交互块中调整解读，再影响后续融合；两塔只末端拼接会更晚才看到对方线索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.10016">原论文</a> · <a href="../../../../reproductions/2602.10016-kunlun/">实现解读</a> · <a href="#qa-062a5b981a1264df">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:kunlun" data-paper-title="Kunlun: Establishing Scaling Laws for Massive-Scale Recommendation Systems through Unified Architecture Design" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Kunlun: Establishing Scaling Laws for Massive-Scale Recommendation Systems through Unified Architecture Design 搜广推与 LLM 应用 Meta 2026-02-10 传统广告模型把序列塔、稠密交叉和系统并行分别优化，扩大规模后收益快速饱和。Kunlun 在每层同时放置 Transformer Block 与 Interaction Block：GDPA/PFFN 建模序列，HSP 汇总序列 seed，Global Interaction 交换序列与非序列信息；CompSkip 和 expert parallel 保持深层训练稳定与吞吐。 Fidelity: 核心机制复现。本地执行 GDPA、分层 seed pooling、expert routing 和 CompSkip；不声称复刻 Meta Ads 模型规模。本地仅验证网络算子和信息流；没有 Meta Ads 私有数据、万亿参数、expert parallel 或硬件 MFU 对照。本地对照口径：基线为 shallow transition-content ranker，实验组执行 Kunlun compact core；NDCG@10 相对 -5.25%。  ranking scaling-law long-sequence mixture-of-experts serving 搜广推 用户历史与排序骨干 Kunlun为什么交错序列块与交互块，而不只把其中一条塔扩得更大？ 序列模型负责历史依赖，异构交互负责字段关系，单独扩一侧可能受另一侧信息瓶颈限制。Kunlun在层间交换序列seed与非序列信息，并用门控和残差控制深层更新，再结合并行工程承载规模。结构联合扩展并非所有模块都可免费复用，必须区分候选依赖与实际服务开销。 示意：长历史提取了户外兴趣，但价格与场景交叉只在末端出现，可能无法影响更深的兴趣解释；交错结构让这两类信息在多层协同，而不只是concat一次。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-4031a3745258df11">Kunlun为什么交错序列块与交互块，而不只把其中一条塔扩得更大？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Akunlun">Kunlun: Establishing Scaling Laws for Massive-Scale Recommendation Systems through Unified Architecture Design</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>序列模型负责历史依赖，异构交互负责字段关系，单独扩一侧可能受另一侧信息瓶颈限制。Kunlun在层间交换序列seed与非序列信息，并用门控和残差控制深层更新，再结合并行工程承载规模。结构联合扩展并非所有模块都可免费复用，必须区分候选依赖与实际服务开销。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>长历史提取了户外兴趣，但价格与场景交叉只在末端出现，可能无法影响更深的兴趣解释；交错结构让这两类信息在多层协同，而不只是concat一次。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.10016">原论文</a> · <a href="../../../../reproductions/2602.10016-kunlun/">实现解读</a> · <a href="#qa-4031a3745258df11">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:kunlun" data-paper-title="Kunlun: Establishing Scaling Laws for Massive-Scale Recommendation Systems through Unified Architecture Design" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Kunlun: Establishing Scaling Laws for Massive-Scale Recommendation Systems through Unified Architecture Design 搜广推与 LLM 应用 Meta 2026-02-10 传统广告模型把序列塔、稠密交叉和系统并行分别优化，扩大规模后收益快速饱和。Kunlun 在每层同时放置 Transformer Block 与 Interaction Block：GDPA/PFFN 建模序列，HSP 汇总序列 seed，Global Interaction 交换序列与非序列信息；CompSkip 和 expert parallel 保持深层训练稳定与吞吐。 Fidelity: 核心机制复现。本地执行 GDPA、分层 seed pooling、expert routing 和 CompSkip；不声称复刻 Meta Ads 模型规模。本地仅验证网络算子和信息流；没有 Meta Ads 私有数据、万亿参数、expert parallel 或硬件 MFU 对照。本地对照口径：基线为 shallow transition-content ranker，实验组执行 Kunlun compact core；NDCG@10 相对 -5.25%。  ranking scaling-law long-sequence mixture-of-experts serving 搜广推 用户历史与排序骨干 Kunlun 的门控 GDPA 与普通 softmax attention，相比 gate 在何处影响证据？ 来源将 gate 的 log-sigmoid 加入注意力 logit，相当于在归一前抑制部分关系，而不是事后随意缩放最终向量。门控可能降低噪声，也可能压掉稀有重要行为。CompSkip 再调残差深度是另一机制，不应把两者都归为注意力提升。 示意：某条偶然点击在归一前被降权，其他历史相对获得更多份额；事后把整个用户向量乘小并不能产生相同的候选关系变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-26d7b73cacf6f46c">Kunlun 的门控 GDPA 与普通 softmax attention，相比 gate 在何处影响证据？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Akunlun">Kunlun: Establishing Scaling Laws for Massive-Scale Recommendation Systems through Unified Architecture Design</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>来源将 gate 的 log-sigmoid 加入注意力 logit，相当于在归一前抑制部分关系，而不是事后随意缩放最终向量。门控可能降低噪声，也可能压掉稀有重要行为。CompSkip 再调残差深度是另一机制，不应把两者都归为注意力提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某条偶然点击在归一前被降权，其他历史相对获得更多份额；事后把整个用户向量乘小并不能产生相同的候选关系变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.10016">原论文</a> · <a href="../../../../reproductions/2602.10016-kunlun/">实现解读</a> · <a href="#qa-26d7b73cacf6f46c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:kunlun" data-paper-title="Kunlun: Establishing Scaling Laws for Massive-Scale Recommendation Systems through Unified Architecture Design" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Kunlun: Establishing Scaling Laws for Massive-Scale Recommendation Systems through Unified Architecture Design 搜广推与 LLM 应用 Meta 2026-02-10 传统广告模型把序列塔、稠密交叉和系统并行分别优化，扩大规模后收益快速饱和。Kunlun 在每层同时放置 Transformer Block 与 Interaction Block：GDPA/PFFN 建模序列，HSP 汇总序列 seed，Global Interaction 交换序列与非序列信息；CompSkip 和 expert parallel 保持深层训练稳定与吞吐。 Fidelity: 核心机制复现。本地执行 GDPA、分层 seed pooling、expert routing 和 CompSkip；不声称复刻 Meta Ads 模型规模。本地仅验证网络算子和信息流；没有 Meta Ads 私有数据、万亿参数、expert parallel 或硬件 MFU 对照。本地对照口径：基线为 shallow transition-content ranker，实验组执行 Kunlun compact core；NDCG@10 相对 -5.25%。  ranking scaling-law long-sequence mixture-of-experts serving 搜广推 用户历史与排序骨干 Kunlun 的 CompSkip 混合为什么要明确旧状态和 F 输出的同维关系？ h(l+1)=αhl+(1−α)Fl(hl) 要在相同表示空间组合，α 的范围与广播轴应明确，不能误把候选或批轴当门控轴。序列与交互的同步更新也要遵守设计。本地四层 compact core 的质量波动不能替代生产吞吐证据。 示意：α 是逐层混合时，不能无意变成每个候选不同且污染共享状态；即使广播让代码跑通，残差语义也已改变。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f1652e912362ce49">Kunlun 的 CompSkip 混合为什么要明确旧状态和 F 输出的同维关系？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Akunlun">Kunlun: Establishing Scaling Laws for Massive-Scale Recommendation Systems through Unified Architecture Design</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>h(l+1)=αhl+(1−α)Fl(hl) 要在相同表示空间组合，α 的范围与广播轴应明确，不能误把候选或批轴当门控轴。序列与交互的同步更新也要遵守设计。本地四层 compact core 的质量波动不能替代生产吞吐证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>α 是逐层混合时，不能无意变成每个候选不同且污染共享状态；即使广播让代码跑通，残差语义也已改变。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.10016">原论文</a> · <a href="../../../../reproductions/2602.10016-kunlun/">实现解读</a> · <a href="#qa-f1652e912362ce49">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ml-dcn" data-paper-title="ML-DCN: Masked Low-Rank Deep Crossing Network Towards Scalable Ads Click-through Rate Prediction at Pinterest" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="ML-DCN: Masked Low-Rank Deep Crossing Network Towards Scalable Ads Click-through Rate Prediction at Pinterest 搜广推与 LLM 应用 Pinterest 2026-02-09 把 DCNv2 的全维交叉替换为可调内部维度的低秩交叉，并以可学习 mask 选择交叉通道，在相同 FLOPs 下扩大容量。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 ml-dcn 核心机制，相对 NDCG@10 -2.08%。  advertising feature-crossing serving-efficiency 搜广推 用户历史与排序骨干 ML-DCN 的 mask 为什么作用于交叉输入，而不是最终分数？ 交叉前选择通道会改变哪些特征参与后续乘性交互，最终分数缩放只改变已形成结果，无法撤销无用交叉。低秩投影再控制内部计算维度，两者分别负责信息选择与容量预算。mask 学到的值仍不是因果重要性，不保证小值字段可全链路删除。 示意：价格通道在某类样本噪声大，先抑制它可避免与其他字段产生错误组合；事后乘整个预测值会连有用信号也一并压低。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-ml-dcn-5baa5b42" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-780a90dec56504ba">ML-DCN 的 mask 为什么作用于交叉输入，而不是最终分数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aml-dcn">ML-DCN: Masked Low-Rank Deep Crossing Network Towards Scalable Ads Click-through Rate Prediction at Pinterest</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>交叉前选择通道会改变哪些特征参与后续乘性交互，最终分数缩放只改变已形成结果，无法撤销无用交叉。低秩投影再控制内部计算维度，两者分别负责信息选择与容量预算。mask 学到的值仍不是因果重要性，不保证小值字段可全链路删除。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>价格通道在某类样本噪声大，先抑制它可避免与其他字段产生错误组合；事后乘整个预测值会连有用信号也一并压低。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.09194">原论文</a> · <a href="../../../../reproductions/2602.09194-ml-dcn/">实现解读</a> · <a href="#qa-780a90dec56504ba">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ml-dcn" data-paper-title="ML-DCN: Masked Low-Rank Deep Crossing Network Towards Scalable Ads Click-through Rate Prediction at Pinterest" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="ML-DCN: Masked Low-Rank Deep Crossing Network Towards Scalable Ads Click-through Rate Prediction at Pinterest 搜广推与 LLM 应用 Pinterest 2026-02-09 把 DCNv2 的全维交叉替换为可调内部维度的低秩交叉，并以可学习 mask 选择交叉通道，在相同 FLOPs 下扩大容量。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 ml-dcn 核心机制，相对 NDCG@10 -2.08%。  advertising feature-crossing serving-efficiency 搜广推 用户历史与排序骨干 ML-DCN 为什么在显式交叉前同时引入低秩投影和可学习 mask？ 全维交叉的容量与计算会一起增长。低秩投影把交叉压到可调内部维度，再映回原空间，减少昂贵的全维变换；mask 则调节哪些输入通道参与交叉。两者分别控制交叉的计算规模和信息选择，残差保留原表示，但低秩瓶颈也可能丢失不能被该子空间表达的关系。 示意：年龄、城市、设备等上千维特征不必全部两两充分交互。先保留与当前目标相关的通道，再用几十维子空间组合，省下的计算可用于增加层数或容量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-b8e34d21c8c29d9b">ML-DCN 为什么在显式交叉前同时引入低秩投影和可学习 mask？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aml-dcn">ML-DCN: Masked Low-Rank Deep Crossing Network Towards Scalable Ads Click-through Rate Prediction at Pinterest</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全维交叉的容量与计算会一起增长。低秩投影把交叉压到可调内部维度，再映回原空间，减少昂贵的全维变换；mask 则调节哪些输入通道参与交叉。两者分别控制交叉的计算规模和信息选择，残差保留原表示，但低秩瓶颈也可能丢失不能被该子空间表达的关系。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>年龄、城市、设备等上千维特征不必全部两两充分交互。先保留与当前目标相关的通道，再用几十维子空间组合，省下的计算可用于增加层数或容量。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.09194">原论文</a> · <a href="../../../../reproductions/2602.09194-ml-dcn/">实现解读</a> · <a href="#qa-b8e34d21c8c29d9b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ml-dcn" data-paper-title="ML-DCN: Masked Low-Rank Deep Crossing Network Towards Scalable Ads Click-through Rate Prediction at Pinterest" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="ML-DCN: Masked Low-Rank Deep Crossing Network Towards Scalable Ads Click-through Rate Prediction at Pinterest 搜广推与 LLM 应用 Pinterest 2026-02-09 把 DCNv2 的全维交叉替换为可调内部维度的低秩交叉，并以可学习 mask 选择交叉通道，在相同 FLOPs 下扩大容量。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 ml-dcn 核心机制，相对 NDCG@10 -2.08%。  advertising feature-crossing serving-efficiency 搜广推 用户历史与排序骨干 ML-DCN 与 DCN-V2 全矩阵 cross，相比秩与通道选择怎样交换表达力？ 全矩阵可表达更一般线性变换，低秩将其限制在较小子空间，mask 又提供自适应选择，省下预算可增加容量。低秩也可能漏关系，更多层不必完全补回。来源本地共享 scorer 代理不是完整 DCN-V2 参数匹配对照，不能将小差值全归算法优劣。 示意：一千维交叉先压到几十维更省，但稀有地理—品类关系若不在子空间会丢失；mask 也不能创造投影已经删掉的方向。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e8d71d1a1a2da70a">ML-DCN 与 DCN-V2 全矩阵 cross，相比秩与通道选择怎样交换表达力？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aml-dcn">ML-DCN: Masked Low-Rank Deep Crossing Network Towards Scalable Ads Click-through Rate Prediction at Pinterest</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全矩阵可表达更一般线性变换，低秩将其限制在较小子空间，mask 又提供自适应选择，省下预算可增加容量。低秩也可能漏关系，更多层不必完全补回。来源本地共享 scorer 代理不是完整 DCN-V2 参数匹配对照，不能将小差值全归算法优劣。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一千维交叉先压到几十维更省，但稀有地理—品类关系若不在子空间会丢失；mask 也不能创造投影已经删掉的方向。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.09194">原论文</a> · <a href="../../../../reproductions/2602.09194-ml-dcn/">实现解读</a> · <a href="#qa-e8d71d1a1a2da70a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:ml-dcn" data-paper-title="ML-DCN: Masked Low-Rank Deep Crossing Network Towards Scalable Ads Click-through Rate Prediction at Pinterest" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="ML-DCN: Masked Low-Rank Deep Crossing Network Towards Scalable Ads Click-through Rate Prediction at Pinterest 搜广推与 LLM 应用 Pinterest 2026-02-09 把 DCNv2 的全维交叉替换为可调内部维度的低秩交叉，并以可学习 mask 选择交叉通道，在相同 FLOPs 下扩大容量。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 ml-dcn 核心机制，相对 NDCG@10 -2.08%。  advertising feature-crossing serving-efficiency 搜广推 用户历史与排序骨干 ML-DCN 的 V、U、mask 与 x0 应满足怎样的形状关系？ mask 先与当前 xl 逐通道相乘，V 将原维投到内部秩，U 映回后与原始 x0 相乘，再加残差与偏置。x0 不能每层改成 xl，mask 也不能广播到批轴。实现应检查真实梯度流，不用固定筛选代替可学习 mask。 示意：内部秩三十二不表示输出只有三十二维，必须映回原维才能与 x0 逐元素相乘；直接残差相加会改变网络定义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7f87b3e0f77bd8f8">ML-DCN 的 V、U、mask 与 x0 应满足怎样的形状关系？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aml-dcn">ML-DCN: Masked Low-Rank Deep Crossing Network Towards Scalable Ads Click-through Rate Prediction at Pinterest</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>mask 先与当前 xl 逐通道相乘，V 将原维投到内部秩，U 映回后与原始 x0 相乘，再加残差与偏置。x0 不能每层改成 xl，mask 也不能广播到批轴。实现应检查真实梯度流，不用固定筛选代替可学习 mask。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>内部秩三十二不表示输出只有三十二维，必须映回原维才能与 x0 逐元素相乘；直接残差相加会改变网络定义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.09194">原论文</a> · <a href="../../../../reproductions/2602.09194-ml-dcn/">实现解读</a> · <a href="#qa-7f87b3e0f77bd8f8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mdl" data-paper-title="MDL: A Unified Multi-Distribution Learner in Large-scale Industrial Recommendation through Tokenization" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="MDL: A Unified Multi-Distribution Learner in Large-scale Industrial Recommendation through Tokenization 搜广推与 LLM 应用 ByteDance / Douyin 2026-02-07 工业多场景、多任务模型常只在浅层做 gate，未充分共享大模型参数。MDL 把 feature、scenario 和 task 都表示成 token，经 feature self-attention、domain-feature attention 和 domain-fused aggregation 深层交互。 Fidelity: 核心机制复现。执行 feature/scenario/task tokens 与 domain-feature attention。MovieLens genre/next-item 代理抖音场景与任务，未复刻生产参数规模、私有标签和 serving。本地对照口径：基线是共享但非 tokenized ranker；实验组加入 19 feature tokens、19 scenario tokens 和 2 task tokens，NDCG@10 0.03540→0.04012，相对 +13.34%，但 head share +73.43%。  ranking multi-scenario multi-task tokenization 搜广推 用户历史与排序骨干 MDL 为什么把 scenario 和 task 也 token 化？ 场景和目标不只决定最后接哪个头，也决定哪些字段关系值得建模。domain-feature attention 让场景查询在深层读取特征，任务 token 与聚合再形成特定输出。token 化提供交互接口，但不能确保每个 token 自动学得人类预期语义。 示意：同一用户特征在直播购买与短视频观看场景作用不同，场景 token 可在中间层调节读取，而不是到最后才换一个分类头。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-mdl-daad794f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f6f40c7f4f0b55d9">MDL 为什么把 scenario 和 task 也 token 化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amdl">MDL: A Unified Multi-Distribution Learner in Large-scale Industrial Recommendation through Tokenization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>场景和目标不只决定最后接哪个头，也决定哪些字段关系值得建模。domain-feature attention 让场景查询在深层读取特征，任务 token 与聚合再形成特定输出。token 化提供交互接口，但不能确保每个 token 自动学得人类预期语义。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一用户特征在直播购买与短视频观看场景作用不同，场景 token 可在中间层调节读取，而不是到最后才换一个分类头。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.07520">原论文</a> · <a href="../../../../reproductions/2602.07520-mdl/">实现解读</a> · <a href="#qa-f6f40c7f4f0b55d9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mdl" data-paper-title="MDL: A Unified Multi-Distribution Learner in Large-scale Industrial Recommendation through Tokenization" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="MDL: A Unified Multi-Distribution Learner in Large-scale Industrial Recommendation through Tokenization 搜广推与 LLM 应用 ByteDance / Douyin 2026-02-07 工业多场景、多任务模型常只在浅层做 gate，未充分共享大模型参数。MDL 把 feature、scenario 和 task 都表示成 token，经 feature self-attention、domain-feature attention 和 domain-fused aggregation 深层交互。 Fidelity: 核心机制复现。执行 feature/scenario/task tokens 与 domain-feature attention。MovieLens genre/next-item 代理抖音场景与任务，未复刻生产参数规模、私有标签和 serving。本地对照口径：基线是共享但非 tokenized ranker；实验组加入 19 feature tokens、19 scenario tokens 和 2 task tokens，NDCG@10 0.03540→0.04012，相对 +13.34%，但 head share +73.43%。  ranking multi-scenario multi-task tokenization 搜广推 用户历史与排序骨干 MDL为什么把scenario和task也做成token，而不只在输出端选不同head？ 末端分头无法让场景和任务需求持续影响特征选择。把它们作为token加入多层交互，domain query可读取相关字段，任务信息也能参与共享表示构造，增强深层复用。共享更深同时带来干扰可能，仍需检查低流量场景是否被大场景覆盖，不能用统一架构名称代替跨任务收益验证。 示意：相同商品字段用于首页点击和搜索转化时关注点不同；场景与任务token可在编码中改变取证方式，而不是所有信息压成同一向量后才分头判断。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f4f1ac6ba42c0ed1">MDL为什么把scenario和task也做成token，而不只在输出端选不同head？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amdl">MDL: A Unified Multi-Distribution Learner in Large-scale Industrial Recommendation through Tokenization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>末端分头无法让场景和任务需求持续影响特征选择。把它们作为token加入多层交互，domain query可读取相关字段，任务信息也能参与共享表示构造，增强深层复用。共享更深同时带来干扰可能，仍需检查低流量场景是否被大场景覆盖，不能用统一架构名称代替跨任务收益验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>相同商品字段用于首页点击和搜索转化时关注点不同；场景与任务token可在编码中改变取证方式，而不是所有信息压成同一向量后才分头判断。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.07520">原论文</a> · <a href="../../../../reproductions/2602.07520-mdl/">实现解读</a> · <a href="#qa-f4f1ac6ba42c0ed1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mdl" data-paper-title="MDL: A Unified Multi-Distribution Learner in Large-scale Industrial Recommendation through Tokenization" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="MDL: A Unified Multi-Distribution Learner in Large-scale Industrial Recommendation through Tokenization 搜广推与 LLM 应用 ByteDance / Douyin 2026-02-07 工业多场景、多任务模型常只在浅层做 gate，未充分共享大模型参数。MDL 把 feature、scenario 和 task 都表示成 token，经 feature self-attention、domain-feature attention 和 domain-fused aggregation 深层交互。 Fidelity: 核心机制复现。执行 feature/scenario/task tokens 与 domain-feature attention。MovieLens genre/next-item 代理抖音场景与任务，未复刻生产参数规模、私有标签和 serving。本地对照口径：基线是共享但非 tokenized ranker；实验组加入 19 feature tokens、19 scenario tokens 和 2 task tokens，NDCG@10 0.03540→0.04012，相对 +13.34%，但 head share +73.43%。  ranking multi-scenario multi-task tokenization 搜广推 用户历史与排序骨干 MDL 的深层 domain-feature 交互与浅层 gate，相比条件化范围有何不同？ 浅 gate 多在已编码特征上调比例，深层交互让域条件反复影响表示形成，具有更丰富联合建模空间。代价是更多计算与负迁移风险，来源准确率改善伴随头部明显上升，不能把扩大共享解释为全部群体获益。 示意：场景先强调价格，下一层再结合用户预算，深层可组合新关系；浅门控只能对已完成特征加减权，较难重写早期交叉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-bc0887908bac6b4c">MDL 的深层 domain-feature 交互与浅层 gate，相比条件化范围有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amdl">MDL: A Unified Multi-Distribution Learner in Large-scale Industrial Recommendation through Tokenization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>浅 gate 多在已编码特征上调比例，深层交互让域条件反复影响表示形成，具有更丰富联合建模空间。代价是更多计算与负迁移风险，来源准确率改善伴随头部明显上升，不能把扩大共享解释为全部群体获益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>场景先强调价格，下一层再结合用户预算，深层可组合新关系；浅门控只能对已完成特征加减权，较难重写早期交叉。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.07520">原论文</a> · <a href="../../../../reproductions/2602.07520-mdl/">实现解读</a> · <a href="#qa-bc0887908bac6b4c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:mdl" data-paper-title="MDL: A Unified Multi-Distribution Learner in Large-scale Industrial Recommendation through Tokenization" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="MDL: A Unified Multi-Distribution Learner in Large-scale Industrial Recommendation through Tokenization 搜广推与 LLM 应用 ByteDance / Douyin 2026-02-07 工业多场景、多任务模型常只在浅层做 gate，未充分共享大模型参数。MDL 把 feature、scenario 和 task 都表示成 token，经 feature self-attention、domain-feature attention 和 domain-fused aggregation 深层交互。 Fidelity: 核心机制复现。执行 feature/scenario/task tokens 与 domain-feature attention。MovieLens genre/next-item 代理抖音场景与任务，未复刻生产参数规模、私有标签和 serving。本地对照口径：基线是共享但非 tokenized ranker；实验组加入 19 feature tokens、19 scenario tokens 和 2 task tokens，NDCG@10 0.03540→0.04012，相对 +13.34%，但 head share +73.43%。  ranking multi-scenario multi-task tokenization 搜广推 用户历史与排序骨干 MDL 的 feature、scenario、task 三类 token 在实现中为何需要身份标签？ 即使末维相同，它们在注意力中担任证据、条件和预测角色，布局与读出必须一致。把场景数当批维或从错误 task 位置读出，会静默改变目标；本地十九场景代理是具体构造，不是十九真实工业业务。 示意：购买 task token 的输出不能接观看标签，只因都是二维向量不会报错；需按身份映射核验，而不只检查张量尺寸。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7411c8a5b2cb6b28">MDL 的 feature、scenario、task 三类 token 在实现中为何需要身份标签？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amdl">MDL: A Unified Multi-Distribution Learner in Large-scale Industrial Recommendation through Tokenization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>即使末维相同，它们在注意力中担任证据、条件和预测角色，布局与读出必须一致。把场景数当批维或从错误 task 位置读出，会静默改变目标；本地十九场景代理是具体构造，不是十九真实工业业务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>购买 task token 的输出不能接观看标签，只因都是二维向量不会报错；需按身份映射核验，而不只检查张量尺寸。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.07520">原论文</a> · <a href="../../../../reproductions/2602.07520-mdl/">实现解读</a> · <a href="#qa-7411c8a5b2cb6b28">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:msn" data-paper-title="MSN: A Memory-based Sparse Activation Scaling Framework for Large-scale Industrial Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="MSN: A Memory-based Sparse Activation Scaling Framework for Large-scale Industrial Recommendation 搜广推与 LLM 应用 ByteDance / Douyin Search 2026-02-07 工业排序希望扩大参数量但不同比例增加计算。MSN 将大容量知识放入两轴 Product-Key Memory，根据 query 只激活少量槽位，再用 gate 与 dense backbone 融合。 复现保真度：核心机制复现。复现保真度：核心机制复现。Product-Key Memory、top-k 稀疏读取和门控主干均实际执行。公开 genre 构造两轴 key，交互转移写入 memory value，每次只读取四个槽位。  search-ranking sparse-memory product-key-memory 搜广推 用户历史与排序骨干 MSN 为什么把大容量知识放入记忆槽而不全放 dense 网络？ 稠密网络每次常激活全部参数，大记忆可存更多值、查询仅读少数槽，让容量增长不按同样比例增加每次计算。Product-Key 分两轴组织地址，gate 决定如何结合主干。读取稀疏不代表记忆维护免费，也不保证槽里有可靠知识。 示意：资料库很大但一次查四个文件，比每次通读全部文件省；如果地址路由错了，大库仍不能帮助当前推荐。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-msn-56fd8b3f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-008ce07355140f61">MSN 为什么把大容量知识放入记忆槽而不全放 dense 网络？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amsn">MSN: A Memory-based Sparse Activation Scaling Framework for Large-scale Industrial Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin Search</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>稠密网络每次常激活全部参数，大记忆可存更多值、查询仅读少数槽，让容量增长不按同样比例增加每次计算。Product-Key 分两轴组织地址，gate 决定如何结合主干。读取稀疏不代表记忆维护免费，也不保证槽里有可靠知识。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>资料库很大但一次查四个文件，比每次通读全部文件省；如果地址路由错了，大库仍不能帮助当前推荐。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.07526">原论文</a> · <a href="../../../../reproductions/2602.07526-msn/">实现解读</a> · <a href="#qa-008ce07355140f61">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:msn" data-paper-title="MSN: A Memory-based Sparse Activation Scaling Framework for Large-scale Industrial Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="MSN: A Memory-based Sparse Activation Scaling Framework for Large-scale Industrial Recommendation 搜广推与 LLM 应用 ByteDance / Douyin Search 2026-02-07 工业排序希望扩大参数量但不同比例增加计算。MSN 将大容量知识放入两轴 Product-Key Memory，根据 query 只激活少量槽位，再用 gate 与 dense backbone 融合。 复现保真度：核心机制复现。复现保真度：核心机制复现。Product-Key Memory、top-k 稀疏读取和门控主干均实际执行。公开 genre 构造两轴 key，交互转移写入 memory value，每次只读取四个槽位。  search-ranking sparse-memory product-key-memory 搜广推 用户历史与排序骨干 MSN 的两轴 Product-Key Memory 如何增加参数容量而只读取少量知识？ 把键拆成两个轴后，一个槽位由两轴键的组合确定，组合空间可以很大。查询按两轴相似度的和寻找高分组合，只读取少量对应值，再通过 gate 与稠密主干融合。存储容量因此不必全部参与每次前向计算；效果仍依赖路由能否命中有用槽位，未激活的参数不会自动提供帮助。 示意：两组各一百个键可组合出一万个槽位，但一次请求只取最相关的四个。像从有两层索引的资料柜查少数文件，而不是把一万个文件全部读一遍。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8c4d706cf2e88507">MSN 的两轴 Product-Key Memory 如何增加参数容量而只读取少量知识？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amsn">MSN: A Memory-based Sparse Activation Scaling Framework for Large-scale Industrial Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin Search</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>把键拆成两个轴后，一个槽位由两轴键的组合确定，组合空间可以很大。查询按两轴相似度的和寻找高分组合，只读取少量对应值，再通过 gate 与稠密主干融合。存储容量因此不必全部参与每次前向计算；效果仍依赖路由能否命中有用槽位，未激活的参数不会自动提供帮助。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两组各一百个键可组合出一万个槽位，但一次请求只取最相关的四个。像从有两层索引的资料柜查少数文件，而不是把一万个文件全部读一遍。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.07526">原论文</a> · <a href="../../../../reproductions/2602.07526-msn/">实现解读</a> · <a href="#qa-8c4d706cf2e88507">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:msn" data-paper-title="MSN: A Memory-based Sparse Activation Scaling Framework for Large-scale Industrial Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="MSN: A Memory-based Sparse Activation Scaling Framework for Large-scale Industrial Recommendation 搜广推与 LLM 应用 ByteDance / Douyin Search 2026-02-07 工业排序希望扩大参数量但不同比例增加计算。MSN 将大容量知识放入两轴 Product-Key Memory，根据 query 只激活少量槽位，再用 gate 与 dense backbone 融合。 复现保真度：核心机制复现。复现保真度：核心机制复现。Product-Key Memory、top-k 稀疏读取和门控主干均实际执行。公开 genre 构造两轴 key，交互转移写入 memory value，每次只读取四个槽位。  search-ranking sparse-memory product-key-memory 搜广推 用户历史与排序骨干 MSN 的 top-k PKM 与普通全部专家 soft mixture，相比激活成本有何不同？ 全混合通常计算所有专家再加权，PKM 按两轴键找少量组合并只取相关值，更多参数留在未激活槽。路由搜索和内存访问仍有开销，硬 top-k 也可能漏知识；不能只用总参数除活跃数推断真实延迟。 示意：一万槽只读四个与一百专家全部算完不同，前者更依赖索引命中；若硬件读取分散，理论 FLOPs 少也未必更快。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0b30c3fb7efee183">MSN 的 top-k PKM 与普通全部专家 soft mixture，相比激活成本有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amsn">MSN: A Memory-based Sparse Activation Scaling Framework for Large-scale Industrial Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin Search</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全混合通常计算所有专家再加权，PKM 按两轴键找少量组合并只取相关值，更多参数留在未激活槽。路由搜索和内存访问仍有开销，硬 top-k 也可能漏知识；不能只用总参数除活跃数推断真实延迟。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一万槽只读四个与一百专家全部算完不同，前者更依赖索引命中；若硬件读取分散，理论 FLOPs 少也未必更快。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.07526">原论文</a> · <a href="../../../../reproductions/2602.07526-msn/">实现解读</a> · <a href="#qa-0b30c3fb7efee183">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:msn" data-paper-title="MSN: A Memory-based Sparse Activation Scaling Framework for Large-scale Industrial Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="MSN: A Memory-based Sparse Activation Scaling Framework for Large-scale Industrial Recommendation 搜广推与 LLM 应用 ByteDance / Douyin Search 2026-02-07 工业排序希望扩大参数量但不同比例增加计算。MSN 将大容量知识放入两轴 Product-Key Memory，根据 query 只激活少量槽位，再用 gate 与 dense backbone 融合。 复现保真度：核心机制复现。复现保真度：核心机制复现。Product-Key Memory、top-k 稀疏读取和门控主干均实际执行。公开 genre 构造两轴 key，交互转移写入 memory value，每次只读取四个槽位。  search-ranking sparse-memory product-key-memory 搜广推 用户历史与排序骨干 MSN 的两轴键组合为什么要保留唯一槽索引与 top-k 去重？ 每个槽由轴一、轴二地址共同确定，分数是两侧相似度之和；同一组合若重复进入会无端加大权重。选中 value 维度需与主干融合一致，空或不足候选也要按定义处理。本地 genre 与 transition 写槽只是公开内容代理。 示意：键对二、三与三、二是不同槽，不能仅把和五当地址；同一个二、三出现两次也不应被当两条独立知识加倍。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c06429233f8f31d0">MSN 的两轴键组合为什么要保留唯一槽索引与 top-k 去重？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Amsn">MSN: A Memory-based Sparse Activation Scaling Framework for Large-scale Industrial Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin Search</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每个槽由轴一、轴二地址共同确定，分数是两侧相似度之和；同一组合若重复进入会无端加大权重。选中 value 维度需与主干融合一致，空或不足候选也要按定义处理。本地 genre 与 transition 写槽只是公开内容代理。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>键对二、三与三、二是不同槽，不能仅把和五当地址；同一个二、三出现两次也不应被当两条独立知识加倍。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.07526">原论文</a> · <a href="../../../../reproductions/2602.07526-msn/">实现解读</a> · <a href="#qa-c06429233f8f31d0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tokenmixer-large" data-paper-title="TokenMixer-Large: Scaling Up Large Ranking Models in Industrial Recommenders" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TokenMixer-Large: Scaling Up Large Ranking Models in Industrial Recommenders 搜广推与 LLM 应用 ByteDance 2026-02-06 TokenMixer-Large 将候选与多域特征 token 先无参数 mixing，再分别做 head-wise SwiGLU，revert 后执行 token-wise SwiGLU；深层网络加入间隔残差和中间监督，使推荐精排能够稳定扩容。 复现保真度：完整核心链路复现。复现保真度：完整核心链路复现。主干、interval residual、中层辅助损失均真实训练，仅缩小规模。MovieLens 100K 上 TokenMixer-Large 与 rankmixer_dense 使用相同维度、层数、负采样和训练步数。  ranking token-mixing scaling 搜广推 用户历史与排序骨干 TokenMixer-Large的无参数mixing是否意味着整个模型无参数？ 不是，mix/revert是确定重排，head-wise与token-wise SwiGLU仍可训练，深层残差及辅助监督也参与学习。无参数只修饰重排算子，不是整个排序网络。 例如打乱再还原通道不学参数，中间处理这些通道的FFN仍需训练。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-tokenmixer-large-095f089c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-3e02f63426f1ac85">TokenMixer-Large的无参数mixing是否意味着整个模型无参数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atokenmixer-large">TokenMixer-Large: Scaling Up Large Ranking Models in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是，mix/revert是确定重排，head-wise与token-wise SwiGLU仍可训练，深层残差及辅助监督也参与学习。无参数只修饰重排算子，不是整个排序网络。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如打乱再还原通道不学参数，中间处理这些通道的FFN仍需训练。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.06563">原论文</a> · <a href="../../../../reproductions/2602.06563-tokenmixer-large/">实现解读</a> · <a href="#qa-3e02f63426f1ac85">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tokenmixer-large" data-paper-title="TokenMixer-Large: Scaling Up Large Ranking Models in Industrial Recommenders" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TokenMixer-Large: Scaling Up Large Ranking Models in Industrial Recommenders 搜广推与 LLM 应用 ByteDance 2026-02-06 TokenMixer-Large 将候选与多域特征 token 先无参数 mixing，再分别做 head-wise SwiGLU，revert 后执行 token-wise SwiGLU；深层网络加入间隔残差和中间监督，使推荐精排能够稳定扩容。 复现保真度：完整核心链路复现。复现保真度：完整核心链路复现。主干、interval residual、中层辅助损失均真实训练，仅缩小规模。MovieLens 100K 上 TokenMixer-Large 与 rankmixer_dense 使用相同维度、层数、负采样和训练步数。  ranking token-mixing scaling 搜广推 用户历史与排序骨干 TokenMixer-Large 为什么在无参数 mixing 后做 head-wise SwiGLU，revert 后还要 token-wise SwiGLU？ mixing 重排特征通道，让 head 视角看到跨 token 的组合，head-wise 非线性先学习这些组合；revert 恢复 token 布局后，token-wise 变换再处理各位置内部表示。两种轴上的学习互补，间隔残差与中间监督支持深层训练。无参数混合只负责搬运信息，真正可学习交互来自其后的网络。 示意：把多个字段的通道重新分组，先学习“价格与消费偏好”等跨字段组合，再放回原布局做逐 token 处理。只有重排而没有后续非线性，不会凭空学会这些关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-9a0857a64a43674f">TokenMixer-Large 为什么在无参数 mixing 后做 head-wise SwiGLU，revert 后还要 token-wise SwiGLU？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atokenmixer-large">TokenMixer-Large: Scaling Up Large Ranking Models in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>mixing 重排特征通道，让 head 视角看到跨 token 的组合，head-wise 非线性先学习这些组合；revert 恢复 token 布局后，token-wise 变换再处理各位置内部表示。两种轴上的学习互补，间隔残差与中间监督支持深层训练。无参数混合只负责搬运信息，真正可学习交互来自其后的网络。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把多个字段的通道重新分组，先学习“价格与消费偏好”等跨字段组合，再放回原布局做逐 token 处理。只有重排而没有后续非线性，不会凭空学会这些关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.06563">原论文</a> · <a href="../../../../reproductions/2602.06563-tokenmixer-large/">实现解读</a> · <a href="#qa-9a0857a64a43674f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tokenmixer-large" data-paper-title="TokenMixer-Large: Scaling Up Large Ranking Models in Industrial Recommenders" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TokenMixer-Large: Scaling Up Large Ranking Models in Industrial Recommenders 搜广推与 LLM 应用 ByteDance 2026-02-06 TokenMixer-Large 将候选与多域特征 token 先无参数 mixing，再分别做 head-wise SwiGLU，revert 后执行 token-wise SwiGLU；深层网络加入间隔残差和中间监督，使推荐精排能够稳定扩容。 复现保真度：完整核心链路复现。复现保真度：完整核心链路复现。主干、interval residual、中层辅助损失均真实训练，仅缩小规模。MovieLens 100K 上 TokenMixer-Large 与 rankmixer_dense 使用相同维度、层数、负采样和训练步数。  ranking token-mixing scaling 搜广推 用户历史与排序骨干 与单纯token-wise FFN相比，mix–headFFN–revert增加什么交互？ 重排把不同token切片送入head-wise非线性处理，再回原布局，使信息跨token混合。它不是动态attention，也不能由单seed小提升证明注意力可全面替代。 例如head看到拼合片段，回位后每个token获得其他token变换过的信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-411f9977314d5723">与单纯token-wise FFN相比，mix–headFFN–revert增加什么交互？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atokenmixer-large">TokenMixer-Large: Scaling Up Large Ranking Models in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>重排把不同token切片送入head-wise非线性处理，再回原布局，使信息跨token混合。它不是动态attention，也不能由单seed小提升证明注意力可全面替代。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如head看到拼合片段，回位后每个token获得其他token变换过的信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.06563">原论文</a> · <a href="../../../../reproductions/2602.06563-tokenmixer-large/">实现解读</a> · <a href="#qa-411f9977314d5723">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:tokenmixer-large" data-paper-title="TokenMixer-Large: Scaling Up Large Ranking Models in Industrial Recommenders" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TokenMixer-Large: Scaling Up Large Ranking Models in Industrial Recommenders 搜广推与 LLM 应用 ByteDance 2026-02-06 TokenMixer-Large 将候选与多域特征 token 先无参数 mixing，再分别做 head-wise SwiGLU，revert 后执行 token-wise SwiGLU；深层网络加入间隔残差和中间监督，使推荐精排能够稳定扩容。 复现保真度：完整核心链路复现。复现保真度：完整核心链路复现。主干、interval residual、中层辅助损失均真实训练，仅缩小规模。MovieLens 100K 上 TokenMixer-Large 与 rankmixer_dense 使用相同维度、层数、负采样和训练步数。  ranking token-mixing scaling 搜广推 用户历史与排序骨干 本地TokenMixer-Large与RankMixer对照能支持哪些结论？ 同维度层数负采样步数下有单seed结果，但规模小且非完整attention对照。实现需保持FFN绑定混合位置及revert顺序，不能把原token语义错配后仍称同结构。 例如重排后的第一个head不等于原第一个特征槽，参数绑定要按当前布局。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-456741bae5caa17a">本地TokenMixer-Large与RankMixer对照能支持哪些结论？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atokenmixer-large">TokenMixer-Large: Scaling Up Large Ranking Models in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同维度层数负采样步数下有单seed结果，但规模小且非完整attention对照。实现需保持FFN绑定混合位置及revert顺序，不能把原token语义错配后仍称同结构。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如重排后的第一个head不等于原第一个特征槽，参数绑定要按当前布局。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.06563">原论文</a> · <a href="../../../../reproductions/2602.06563-tokenmixer-large/">实现解读</a> · <a href="#qa-456741bae5caa17a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:zenith" data-paper-title="Zenith: Scaling up Ranking Models for Billion-scale Livestreaming Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Zenith: Scaling up Ranking Models for Billion-scale Livestreaming Recommendation 搜广推与 LLM 应用 North Carolina State University 2026-01-29 Token Fusion 将大量异构稀疏特征压成少量高维 Prime Tokens，RSA/TMHSA 保持 token 差异；TSwiGLU/TSMoE 对每个 token 独立增强，改善模型规模与计算量的 scaling law。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04623，相对变化 -14.40%。本地代理目标与论文生产任务不同，不能外推线上 lift。  ranking-network scaling-law feature-interaction 搜广推 用户历史与排序骨干 Zenith为什么将大量特征融合成少量Prime Tokens？ 减少token交互成本同时提高每token表达，后续差异化注意和独立增强保留特征多样性。融合有信息瓶颈，不能仅因token少就称无损。 例如把许多稀疏字段压到几个高维槽，仍需避免槽全部变得一样。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-zenith-6db3b2a2" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-bcef87acbc65f178">Zenith为什么将大量特征融合成少量Prime Tokens？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Azenith">Zenith: Scaling up Ranking Models for Billion-scale Livestreaming Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · North Carolina State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>减少token交互成本同时提高每token表达，后续差异化注意和独立增强保留特征多样性。融合有信息瓶颈，不能仅因token少就称无损。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把许多稀疏字段压到几个高维槽，仍需避免槽全部变得一样。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.21285">原论文</a> · <a href="../../../../reproductions/2601.21285-zenith/">实现解读</a> · <a href="#qa-bcef87acbc65f178">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:zenith" data-paper-title="Zenith: Scaling up Ranking Models for Billion-scale Livestreaming Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Zenith: Scaling up Ranking Models for Billion-scale Livestreaming Recommendation 搜广推与 LLM 应用 North Carolina State University 2026-01-29 Token Fusion 将大量异构稀疏特征压成少量高维 Prime Tokens，RSA/TMHSA 保持 token 差异；TSwiGLU/TSMoE 对每个 token 独立增强，改善模型规模与计算量的 scaling law。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04623，相对变化 -14.40%。本地代理目标与论文生产任务不同，不能外推线上 lift。  ranking-network scaling-law feature-interaction 搜广推 用户历史与排序骨干 Zenith 为什么先把异构稀疏特征融合成少量高维 Prime Tokens，再做 token 专属增强？ 大量短 token 会放大交互开销，Token Fusion 把特征压成少量更宽的表示，重新分配 token 数与通道容量。RSA/TMHSA 维持不同 token 的差异，专属 SwiGLU 或 MoE 再提供针对性非线性，避免压缩后都趋同。压缩可能损失细节，扩宽与专属参数是否值得需按同计算预算验证。 示意：原来一百个细字段逐对交互，先融合为少数宽 token 后可减少注意力位置数；但还要让用户与商品等角色保持差异，否则只得到几份相似的大向量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-cc81feea6d61f783">Zenith 为什么先把异构稀疏特征融合成少量高维 Prime Tokens，再做 token 专属增强？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Azenith">Zenith: Scaling up Ranking Models for Billion-scale Livestreaming Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · North Carolina State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>大量短 token 会放大交互开销，Token Fusion 把特征压成少量更宽的表示，重新分配 token 数与通道容量。RSA/TMHSA 维持不同 token 的差异，专属 SwiGLU 或 MoE 再提供针对性非线性，避免压缩后都趋同。压缩可能损失细节，扩宽与专属参数是否值得需按同计算预算验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>原来一百个细字段逐对交互，先融合为少数宽 token 后可减少注意力位置数；但还要让用户与商品等角色保持差异，否则只得到几份相似的大向量。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.21285">原论文</a> · <a href="../../../../reproductions/2601.21285-zenith/">实现解读</a> · <a href="#qa-cc81feea6d61f783">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:zenith" data-paper-title="Zenith: Scaling up Ranking Models for Billion-scale Livestreaming Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Zenith: Scaling up Ranking Models for Billion-scale Livestreaming Recommendation 搜广推与 LLM 应用 North Carolina State University 2026-01-29 Token Fusion 将大量异构稀疏特征压成少量高维 Prime Tokens，RSA/TMHSA 保持 token 差异；TSwiGLU/TSMoE 对每个 token 独立增强，改善模型规模与计算量的 scaling law。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04623，相对变化 -14.40%。本地代理目标与论文生产任务不同，不能外推线上 lift。  ranking-network scaling-law feature-interaction 搜广推 用户历史与排序骨干 token独立TSwiGLU与全token共享FFN有什么区别？ 独立增强允许各Prime Token专门化，共享FFN假设同一变换适合所有槽。更多参数也有预算成本，不能把规模差异误认为架构必然更优。 例如用户槽与商品槽可能需要不同非线性，而不是完全共用一套权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7420947d22866257">token独立TSwiGLU与全token共享FFN有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Azenith">Zenith: Scaling up Ranking Models for Billion-scale Livestreaming Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · North Carolina State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立增强允许各Prime Token专门化，共享FFN假设同一变换适合所有槽。更多参数也有预算成本，不能把规模差异误认为架构必然更优。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户槽与商品槽可能需要不同非线性，而不是完全共用一套权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.21285">原论文</a> · <a href="../../../../reproductions/2601.21285-zenith/">实现解读</a> · <a href="#qa-7420947d22866257">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:zenith" data-paper-title="Zenith: Scaling up Ranking Models for Billion-scale Livestreaming Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Zenith: Scaling up Ranking Models for Billion-scale Livestreaming Recommendation 搜广推与 LLM 应用 North Carolina State University 2026-01-29 Token Fusion 将大量异构稀疏特征压成少量高维 Prime Tokens，RSA/TMHSA 保持 token 差异；TSwiGLU/TSMoE 对每个 token 独立增强，改善模型规模与计算量的 scaling law。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04623，相对变化 -14.40%。本地代理目标与论文生产任务不同，不能外推线上 lift。  ranking-network scaling-law feature-interaction 搜广推 用户历史与排序骨干 Zenith本地能证明原论文scaling law吗？ 不能，固定公开小样本只验证Fusion、差异化交互与增强路径，缺生产规模和硬件栈。需多规模同预算曲线，不能从单seed点或解析FLOPs推出扩展斜率。 例如一个小模型分高于基线，不代表越放大领先越大。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-df55bed66463ce54">Zenith本地能证明原论文scaling law吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Azenith">Zenith: Scaling up Ranking Models for Billion-scale Livestreaming Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · North Carolina State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，固定公开小样本只验证Fusion、差异化交互与增强路径，缺生产规模和硬件栈。需多规模同预算曲线，不能从单seed点或解析FLOPs推出扩展斜率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个小模型分高于基线，不代表越放大领先越大。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.21285">原论文</a> · <a href="../../../../reproductions/2601.21285-zenith/">实现解读</a> · <a href="#qa-df55bed66463ce54">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:llatte" data-paper-title="LLaTTE: Scaling Laws for Multi-Stage Sequence Modeling in Large-Scale Ads Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="LLaTTE: Scaling Laws for Multi-Stage Sequence Modeling in Large-Scale Ads Recommendation 搜广推与 LLM 应用 Meta 2026-01-27 工业推荐序列模型同时受训练 FLOPs、在线延迟和跨阶段信息损失约束：直接把历史拉长会让在线 ranking 代价失控，只扩大下游模型又无法恢复上游丢掉的长期兴趣。LLaTTE 将 scaling 拆成两级：上游异步大序列模型读取超长、多源历史并缓存 2,048 维 user representation； Fidelity: 核心机制复现。当前实现实际运行 BERT-tiny semantic features、MLA 上游 latent、target-aware 在线 attention 与 DHEN 门控；未复刻 Meta 私有广告特征和异步生产 serving。本地对照口径：基线是相同 ID/语义 embedding 的 short online sequence；实验组增加 MLA upstream、候选感知 online attention 与 DHEN，NDCG@10 +49.81%。训练预算一致，不是相对 DIN。   搜广推 用户历史与排序骨干 LLaTTE 为什么把上游异步长历史与下游短在线序列分开 scaling？ 上游可承担大历史计算并缓存概况，下游用最新事件与候选感知交互补时效和目标细节，避免每请求重算大模型。两级各有瓶颈，单纯提高上游质量未必被下游完全利用，压缩与迁移效率因此需要测量。 示意：后台保存多年兴趣，用户刚浏览婴儿用品时在线短序列立刻响应；若只等下一次上游刷新，会错过新需求。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-llatte-05036174" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a305aa9a8dee1f67">LLaTTE 为什么把上游异步长历史与下游短在线序列分开 scaling？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Allatte">LLaTTE: Scaling Laws for Multi-Stage Sequence Modeling in Large-Scale Ads Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>上游可承担大历史计算并缓存概况，下游用最新事件与候选感知交互补时效和目标细节，避免每请求重算大模型。两级各有瓶颈，单纯提高上游质量未必被下游完全利用，压缩与迁移效率因此需要测量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>后台保存多年兴趣，用户刚浏览婴儿用品时在线短序列立刻响应；若只等下一次上游刷新，会错过新需求。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.20083">原论文</a> · <a href="../../../../reproductions/2601.20083-llatte/">实现解读</a> · <a href="#qa-a305aa9a8dee1f67">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:llatte" data-paper-title="LLaTTE: Scaling Laws for Multi-Stage Sequence Modeling in Large-Scale Ads Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="LLaTTE: Scaling Laws for Multi-Stage Sequence Modeling in Large-Scale Ads Recommendation 搜广推与 LLM 应用 Meta 2026-01-27 工业推荐序列模型同时受训练 FLOPs、在线延迟和跨阶段信息损失约束：直接把历史拉长会让在线 ranking 代价失控，只扩大下游模型又无法恢复上游丢掉的长期兴趣。LLaTTE 将 scaling 拆成两级：上游异步大序列模型读取超长、多源历史并缓存 2,048 维 user representation； Fidelity: 核心机制复现。当前实现实际运行 BERT-tiny semantic features、MLA 上游 latent、target-aware 在线 attention 与 DHEN 门控；未复刻 Meta 私有广告特征和异步生产 serving。本地对照口径：基线是相同 ID/语义 embedding 的 short online sequence；实验组增加 MLA upstream、候选感知 online attention 与 DHEN，NDCG@10 +49.81%。训练预算一致，不是相对 DIN。   搜广推 用户历史与排序骨干 LLaTTE已经缓存大模型用户表示，为什么下游仍要读取短历史并做候选感知attention？ 上游长历史编码能异步承载较大计算，却存在刷新间隔和压缩损失；在线短序列补充最新行为，候选query再选择对当前打分有用的证据。上下游因此各承担稳定知识与实时相关性，而不是把一个缓存向量当全部用户状态。上游指标改善是否有效迁移到下游，需要单独测量而非默认全额保留。 示意：昨夜缓存记录长期摄影兴趣，用户刚开始搜索旅行背包；在线近期序列应反映新意图，再结合当前候选读取相关知识，而不只复用昨夜的固定结论。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-b35ec683629a5330">LLaTTE已经缓存大模型用户表示，为什么下游仍要读取短历史并做候选感知attention？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Allatte">LLaTTE: Scaling Laws for Multi-Stage Sequence Modeling in Large-Scale Ads Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>上游长历史编码能异步承载较大计算，却存在刷新间隔和压缩损失；在线短序列补充最新行为，候选query再选择对当前打分有用的证据。上下游因此各承担稳定知识与实时相关性，而不是把一个缓存向量当全部用户状态。上游指标改善是否有效迁移到下游，需要单独测量而非默认全额保留。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>昨夜缓存记录长期摄影兴趣，用户刚开始搜索旅行背包；在线近期序列应反映新意图，再结合当前候选读取相关知识，而不只复用昨夜的固定结论。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.20083">原论文</a> · <a href="../../../../reproductions/2601.20083-llatte/">实现解读</a> · <a href="#qa-b35ec683629a5330">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:llatte" data-paper-title="LLaTTE: Scaling Laws for Multi-Stage Sequence Modeling in Large-Scale Ads Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="LLaTTE: Scaling Laws for Multi-Stage Sequence Modeling in Large-Scale Ads Recommendation 搜广推与 LLM 应用 Meta 2026-01-27 工业推荐序列模型同时受训练 FLOPs、在线延迟和跨阶段信息损失约束：直接把历史拉长会让在线 ranking 代价失控，只扩大下游模型又无法恢复上游丢掉的长期兴趣。LLaTTE 将 scaling 拆成两级：上游异步大序列模型读取超长、多源历史并缓存 2,048 维 user representation； Fidelity: 核心机制复现。当前实现实际运行 BERT-tiny semantic features、MLA 上游 latent、target-aware 在线 attention 与 DHEN 门控；未复刻 Meta 私有广告特征和异步生产 serving。本地对照口径：基线是相同 ID/语义 embedding 的 short online sequence；实验组增加 MLA upstream、候选感知 online attention 与 DHEN，NDCG@10 +49.81%。训练预算一致，不是相对 DIN。   搜广推 用户历史与排序骨干 LLaTTE 的迁移效率 τ 与上游单独 NE 改善，为什么不是同一指标？ 上游更好不代表下游获得等比例收益，缓存维度、融合能力与任务目标都可能损失信息。τ 比较两阶段改善，帮助判断继续投上游算力是否值得。分母很小或两侧口径不一致时比率会不稳定，不能把经验律当普适定理。 示意：上游 NE 明显下降，下游几乎没变，说明瓶颈可能在读取接口；此时继续加上游参数未必比改候选感知融合更有效。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a3ca85e63b834cce">LLaTTE 的迁移效率 τ 与上游单独 NE 改善，为什么不是同一指标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Allatte">LLaTTE: Scaling Laws for Multi-Stage Sequence Modeling in Large-Scale Ads Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>上游更好不代表下游获得等比例收益，缓存维度、融合能力与任务目标都可能损失信息。τ 比较两阶段改善，帮助判断继续投上游算力是否值得。分母很小或两侧口径不一致时比率会不稳定，不能把经验律当普适定理。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>上游 NE 明显下降，下游几乎没变，说明瓶颈可能在读取接口；此时继续加上游参数未必比改候选感知融合更有效。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.20083">原论文</a> · <a href="../../../../reproductions/2601.20083-llatte/">实现解读</a> · <a href="#qa-a3ca85e63b834cce">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:llatte" data-paper-title="LLaTTE: Scaling Laws for Multi-Stage Sequence Modeling in Large-Scale Ads Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="LLaTTE: Scaling Laws for Multi-Stage Sequence Modeling in Large-Scale Ads Recommendation 搜广推与 LLM 应用 Meta 2026-01-27 工业推荐序列模型同时受训练 FLOPs、在线延迟和跨阶段信息损失约束：直接把历史拉长会让在线 ranking 代价失控，只扩大下游模型又无法恢复上游丢掉的长期兴趣。LLaTTE 将 scaling 拆成两级：上游异步大序列模型读取超长、多源历史并缓存 2,048 维 user representation； Fidelity: 核心机制复现。当前实现实际运行 BERT-tiny semantic features、MLA 上游 latent、target-aware 在线 attention 与 DHEN 门控；未复刻 Meta 私有广告特征和异步生产 serving。本地对照口径：基线是相同 ID/语义 embedding 的 short online sequence；实验组增加 MLA upstream、候选感知 online attention 与 DHEN，NDCG@10 +49.81%。训练预算一致，不是相对 DIN。   搜广推 用户历史与排序骨干 LLaTTE 本地四 latent query 与 recent-12 路径，为什么不能外推生产两千维缓存收益？ 本地只是固定小规模的长摘要、短历史及门控训练，对真实缓存刷新、线上约四百事件和多源特征没有完整测量。应核验两路梯度与候选依赖，再报告匹配短基线和头部变化；解析规模差异不能填成真实 QPS 或转化提升。 示意：四个摘要向量读二十四条电影历史能验证信息流，但不代表读取万级多源历史与生产缓存延迟相同，更不能从小模型耗时按比例换算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1ceb5ad8c87ef2cd">LLaTTE 本地四 latent query 与 recent-12 路径，为什么不能外推生产两千维缓存收益？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Allatte">LLaTTE: Scaling Laws for Multi-Stage Sequence Modeling in Large-Scale Ads Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>本地只是固定小规模的长摘要、短历史及门控训练，对真实缓存刷新、线上约四百事件和多源特征没有完整测量。应核验两路梯度与候选依赖，再报告匹配短基线和头部变化；解析规模差异不能填成真实 QPS 或转化提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>四个摘要向量读二十四条电影历史能验证信息流，但不代表读取万级多源历史与生产缓存延迟相同，更不能从小模型耗时按比例换算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.20083">原论文</a> · <a href="../../../../reproductions/2601.20083-llatte/">实现解读</a> · <a href="#qa-1ceb5ad8c87ef2cd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sparsectr" data-paper-title="Unleashing the Potential of Sparse Attention on Long-term Behaviors for CTR Prediction" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Unleashing the Potential of Sparse Attention on Long-term Behaviors for CTR Prediction 搜广推与 LLM 应用 Institute of Software, Chinese Academy of Sciences 2026-01-25 TimeChunking 按个体行为时间间隔自适应分块；EvoAttention 并联全局 chunk、兴趣转移和局部窗口三路注意力，RelTemporal 再注入时间间隔、小时和周末相对偏置。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05519，相对变化 +2.19%。本地代理目标与论文生产任务不同，不能外推线上 lift。  ctr-prediction long-sequence sparse-attention 搜广推 用户历史与排序骨干 SparseCTR为什么按个体时间间隔分块？ 统一事件数量窗口难区分密集会话和长期断点，时间自适应块更贴行为节奏。全局块、兴趣转移和局部窗口三路再分别捕捉不同尺度关系。 例如一天连续浏览与隔月再访，不应只因事件相邻就视为同一局部节奏。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-sparsectr-7769ddba" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-66b713ab69ef6033">SparseCTR为什么按个体时间间隔分块？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asparsectr">Unleashing the Potential of Sparse Attention on Long-term Behaviors for CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Software, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>统一事件数量窗口难区分密集会话和长期断点，时间自适应块更贴行为节奏。全局块、兴趣转移和局部窗口三路再分别捕捉不同尺度关系。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一天连续浏览与隔月再访，不应只因事件相邻就视为同一局部节奏。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.17836">原论文</a> · <a href="../../../../reproductions/2601.17836-sparsectr/">实现解读</a> · <a href="#qa-66b713ab69ef6033">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sparsectr" data-paper-title="Unleashing the Potential of Sparse Attention on Long-term Behaviors for CTR Prediction" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Unleashing the Potential of Sparse Attention on Long-term Behaviors for CTR Prediction 搜广推与 LLM 应用 Institute of Software, Chinese Academy of Sciences 2026-01-25 TimeChunking 按个体行为时间间隔自适应分块；EvoAttention 并联全局 chunk、兴趣转移和局部窗口三路注意力，RelTemporal 再注入时间间隔、小时和周末相对偏置。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05519，相对变化 +2.19%。本地代理目标与论文生产任务不同，不能外推线上 lift。  ctr-prediction long-sequence sparse-attention 搜广推 用户历史与排序骨干 SparseCTR 为什么按个体行为间隔自适应分块，还并联全局、转移和局部三路注意力？ 相同条数的行为可能跨几分钟也可能跨几个月，固定窗口会混淆会话边界。时间分块先组织个体节奏，三路分别提取长期概况、兴趣迁移和近邻细节，相对时间偏置再表达间隔与周期。它把时间结构写进信息流，而非只加一个绝对位置；分块与融合仍需避免压掉突发或稀疏兴趣。 示意：用户周末集中浏览十件家具，隔一个月又买耗材。按时间间隔可把两段分开，局部路保留同次采购细节，转移路学习从装修到补充用品的变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-132c0a2e3ff407c5">SparseCTR 为什么按个体行为间隔自适应分块，还并联全局、转移和局部三路注意力？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asparsectr">Unleashing the Potential of Sparse Attention on Long-term Behaviors for CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Software, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相同条数的行为可能跨几分钟也可能跨几个月，固定窗口会混淆会话边界。时间分块先组织个体节奏，三路分别提取长期概况、兴趣迁移和近邻细节，相对时间偏置再表达间隔与周期。它把时间结构写进信息流，而非只加一个绝对位置；分块与融合仍需避免压掉突发或稀疏兴趣。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户周末集中浏览十件家具，隔一个月又买耗材。按时间间隔可把两段分开，局部路保留同次采购细节，转移路学习从装修到补充用品的变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.17836">原论文</a> · <a href="../../../../reproductions/2601.17836-sparsectr/">实现解读</a> · <a href="#qa-132c0a2e3ff407c5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sparsectr" data-paper-title="Unleashing the Potential of Sparse Attention on Long-term Behaviors for CTR Prediction" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Unleashing the Potential of Sparse Attention on Long-term Behaviors for CTR Prediction 搜广推与 LLM 应用 Institute of Software, Chinese Academy of Sciences 2026-01-25 TimeChunking 按个体行为时间间隔自适应分块；EvoAttention 并联全局 chunk、兴趣转移和局部窗口三路注意力，RelTemporal 再注入时间间隔、小时和周末相对偏置。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05519，相对变化 +2.19%。本地代理目标与论文生产任务不同，不能外推线上 lift。  ctr-prediction long-sequence sparse-attention 搜广推 用户历史与排序骨干 三路EvoAttention与只取局部稀疏窗口有什么差别？ 局部保细节，chunk全局保跨段兴趣，transition保兴趣迁移；仅局部会缺其他信息。时间偏置提供相对间隔和日历线索，也不是绝对正确的因果特征。 例如周末规律可能与兴趣相关，但不说明周末本身导致点击。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-88c258ca85063872">三路EvoAttention与只取局部稀疏窗口有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asparsectr">Unleashing the Potential of Sparse Attention on Long-term Behaviors for CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Software, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>局部保细节，chunk全局保跨段兴趣，transition保兴趣迁移；仅局部会缺其他信息。时间偏置提供相对间隔和日历线索，也不是绝对正确的因果特征。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如周末规律可能与兴趣相关，但不说明周末本身导致点击。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.17836">原论文</a> · <a href="../../../../reproductions/2601.17836-sparsectr/">实现解读</a> · <a href="#qa-88c258ca85063872">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sparsectr" data-paper-title="Unleashing the Potential of Sparse Attention on Long-term Behaviors for CTR Prediction" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Unleashing the Potential of Sparse Attention on Long-term Behaviors for CTR Prediction 搜广推与 LLM 应用 Institute of Software, Chinese Academy of Sciences 2026-01-25 TimeChunking 按个体行为时间间隔自适应分块；EvoAttention 并联全局 chunk、兴趣转移和局部窗口三路注意力，RelTemporal 再注入时间间隔、小时和周末相对偏置。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05519，相对变化 +2.19%。本地代理目标与论文生产任务不同，不能外推线上 lift。  ctr-prediction long-sequence sparse-attention 搜广推 用户历史与排序骨干 SparseCTR本地时间特征能代替原生产日志全部时序吗？ 不能，MovieLens固定子集只验证分块和偏置机制。分块需按请求前时间排序，bias与有效mask对齐，不能把未来事件或全库标签混入历史。 例如跨用户时间阈值误共享，可能把不同节奏的人强行同样切块。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-adfe96136481aa5b">SparseCTR本地时间特征能代替原生产日志全部时序吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asparsectr">Unleashing the Potential of Sparse Attention on Long-term Behaviors for CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Software, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，MovieLens固定子集只验证分块和偏置机制。分块需按请求前时间排序，bias与有效mask对齐，不能把未来事件或全库标签混入历史。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如跨用户时间阈值误共享，可能把不同节奏的人强行同样切块。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.17836">原论文</a> · <a href="../../../../reproductions/2601.17836-sparsectr/">实现解读</a> · <a href="#qa-adfe96136481aa5b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hyformer" data-paper-title="HyFormer: Revisiting the Roles of Sequence Modeling and Feature Interaction in CTR Prediction" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="HyFormer: Revisiting the Roles of Sequence Modeling and Feature Interaction in CTR Prediction 搜广推与 LLM 应用 ByteDance / Douyin Search 2026-01-19 LONGER→RankMixer 类串行架构先压缩长序列、再做异构字段交互，信息流晚且单向。HyFormer 从非序列字段和 sequence mean 生成 Global Queries，每层用 queries cross-attend 当前 sequence K/V，再把 decoded queries 与非序列 tokens 做 RankMixer-style boosting；boosted queries 进入下一层重新解码，实现双向、逐层共同演化。 Fidelity: 完整核心链路复现。本地逐层执行 Query Generation、Query Decoding 和 Query Boosting；私有多行为序列替换为 MovieLens 单序列。本地对照口径：基线是独立 sequence Transformer+dense MLP 的 Late Fusion；实验组是 HyFormer；NDCG@10 从 0.0048 升至 0.0116（+143.77%），head share 同时 +30.90pt。这是 query co-evolution 架构消融，不是相对 DIN。   搜广推 用户历史与排序骨干 HyFormer 的 Global Queries 为什么由非序列字段与 sequence mean 初始化？ 查询需要知道当前全局上下文和历史概况，才能有针对性读取长序列，而不是从固定无条件槽起步。每层解码后再 boosting，逐步将字段与历史结合。初始化摘要可能丢细节，后续重读证据有助补充但不保证完全恢复。 示意：场景为旅行、历史概况偏摄影，初始查询可更早关注轻便拍摄需求；若只是固定常量 query，当前场景要等后层才进入解释。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-hyformer-d0fa9291" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2138dbf99ca17a2d">HyFormer 的 Global Queries 为什么由非序列字段与 sequence mean 初始化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahyformer">HyFormer: Revisiting the Roles of Sequence Modeling and Feature Interaction in CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin Search</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>查询需要知道当前全局上下文和历史概况，才能有针对性读取长序列，而不是从固定无条件槽起步。每层解码后再 boosting，逐步将字段与历史结合。初始化摘要可能丢细节，后续重读证据有助补充但不保证完全恢复。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>场景为旅行、历史概况偏摄影，初始查询可更早关注轻便拍摄需求；若只是固定常量 query，当前场景要等后层才进入解释。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.12681">原论文</a> · <a href="../../../../reproductions/2601.12681-hyformer/">实现解读</a> · <a href="#qa-2138dbf99ca17a2d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hyformer" data-paper-title="HyFormer: Revisiting the Roles of Sequence Modeling and Feature Interaction in CTR Prediction" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="HyFormer: Revisiting the Roles of Sequence Modeling and Feature Interaction in CTR Prediction 搜广推与 LLM 应用 ByteDance / Douyin Search 2026-01-19 LONGER→RankMixer 类串行架构先压缩长序列、再做异构字段交互，信息流晚且单向。HyFormer 从非序列字段和 sequence mean 生成 Global Queries，每层用 queries cross-attend 当前 sequence K/V，再把 decoded queries 与非序列 tokens 做 RankMixer-style boosting；boosted queries 进入下一层重新解码，实现双向、逐层共同演化。 Fidelity: 完整核心链路复现。本地逐层执行 Query Generation、Query Decoding 和 Query Boosting；私有多行为序列替换为 MovieLens 单序列。本地对照口径：基线是独立 sequence Transformer+dense MLP 的 Late Fusion；实验组是 HyFormer；NDCG@10 从 0.0048 升至 0.0116（+143.77%），head share 同时 +30.90pt。这是 query co-evolution 架构消融，不是相对 DIN。   搜广推 用户历史与排序骨干 HyFormer为什么每层读完历史后还要做Query Boosting，再返回下一层读取？ 若先把历史压成摘要再做字段交叉，字段信息无法改变下一次取证方向。HyFormer交替读取序列与混合非序列token，使刚得到的历史证据参与字段交互，再由增强query重新查询历史。这里共同演化的是紧凑query与字段表示，不应理解为每个候选都必须改写整段原始历史。 示意：第一层发现用户看过户外内容，结合雨天和商品材质后，下一层query可更关注防水装备；一次性摘要再接MLP就难把这条新问题反馈给历史读取。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-64a45769bae35220">HyFormer为什么每层读完历史后还要做Query Boosting，再返回下一层读取？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahyformer">HyFormer: Revisiting the Roles of Sequence Modeling and Feature Interaction in CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin Search</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若先把历史压成摘要再做字段交叉，字段信息无法改变下一次取证方向。HyFormer交替读取序列与混合非序列token，使刚得到的历史证据参与字段交互，再由增强query重新查询历史。这里共同演化的是紧凑query与字段表示，不应理解为每个候选都必须改写整段原始历史。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第一层发现用户看过户外内容，结合雨天和商品材质后，下一层query可更关注防水装备；一次性摘要再接MLP就难把这条新问题反馈给历史读取。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.12681">原论文</a> · <a href="../../../../reproductions/2601.12681-hyformer/">实现解读</a> · <a href="#qa-64a45769bae35220">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hyformer" data-paper-title="HyFormer: Revisiting the Roles of Sequence Modeling and Feature Interaction in CTR Prediction" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="HyFormer: Revisiting the Roles of Sequence Modeling and Feature Interaction in CTR Prediction 搜广推与 LLM 应用 ByteDance / Douyin Search 2026-01-19 LONGER→RankMixer 类串行架构先压缩长序列、再做异构字段交互，信息流晚且单向。HyFormer 从非序列字段和 sequence mean 生成 Global Queries，每层用 queries cross-attend 当前 sequence K/V，再把 decoded queries 与非序列 tokens 做 RankMixer-style boosting；boosted queries 进入下一层重新解码，实现双向、逐层共同演化。 Fidelity: 完整核心链路复现。本地逐层执行 Query Generation、Query Decoding 和 Query Boosting；私有多行为序列替换为 MovieLens 单序列。本地对照口径：基线是独立 sequence Transformer+dense MLP 的 Late Fusion；实验组是 HyFormer；NDCG@10 从 0.0048 升至 0.0116（+143.77%），head share 同时 +30.90pt。这是 query co-evolution 架构消融，不是相对 DIN。   搜广推 用户历史与排序骨干 HyFormer 的逐层 query co-evolution 与 LONGER 后接 RankMixer，相比交互时机有什么不同？ 串行路径先形成序列摘要再做字段混合，早期历史读取不受后续字段结果调整；HyFormer boosting 后的查询回到下一层重读，形成多轮条件化。更早交流增加表达也可能强化热门偏差，来源本地 head share 大增，不能全归为更好个性化。 示意：第一轮发现露营线索，字段混合加入预算条件，下一轮再找轻量装备证据；单次串行摘要完成后通常不能再按新条件回查原历史。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a3b7a374c10d8c91">HyFormer 的逐层 query co-evolution 与 LONGER 后接 RankMixer，相比交互时机有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahyformer">HyFormer: Revisiting the Roles of Sequence Modeling and Feature Interaction in CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin Search</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>串行路径先形成序列摘要再做字段混合，早期历史读取不受后续字段结果调整；HyFormer boosting 后的查询回到下一层重读，形成多轮条件化。更早交流增加表达也可能强化热门偏差，来源本地 head share 大增，不能全归为更好个性化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第一轮发现露营线索，字段混合加入预算条件，下一轮再找轻量装备证据；单次串行摘要完成后通常不能再按新条件回查原历史。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.12681">原论文</a> · <a href="../../../../reproductions/2601.12681-hyformer/">实现解读</a> · <a href="#qa-a3b7a374c10d8c91">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hyformer" data-paper-title="HyFormer: Revisiting the Roles of Sequence Modeling and Feature Interaction in CTR Prediction" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="HyFormer: Revisiting the Roles of Sequence Modeling and Feature Interaction in CTR Prediction 搜广推与 LLM 应用 ByteDance / Douyin Search 2026-01-19 LONGER→RankMixer 类串行架构先压缩长序列、再做异构字段交互，信息流晚且单向。HyFormer 从非序列字段和 sequence mean 生成 Global Queries，每层用 queries cross-attend 当前 sequence K/V，再把 decoded queries 与非序列 tokens 做 RankMixer-style boosting；boosted queries 进入下一层重新解码，实现双向、逐层共同演化。 Fidelity: 完整核心链路复现。本地逐层执行 Query Generation、Query Decoding 和 Query Boosting；私有多行为序列替换为 MovieLens 单序列。本地对照口径：基线是独立 sequence Transformer+dense MLP 的 Late Fusion；实验组是 HyFormer；NDCG@10 从 0.0048 升至 0.0116（+143.77%），head share 同时 +30.90pt。这是 query co-evolution 架构消融，不是相对 DIN。   搜广推 用户历史与排序骨干 HyFormer 实现每层 boosting 后，为什么要将更新后的 query 送回下一次 cross-attention？ 若始终使用最初 Q，每层只重复同一问题，就丢掉共同演化。当前层 sequence K/V、decoded queries 与 NS tokens 的布局也需对齐，per-token 变换作用在混合布局。本地两 query 缩比是具体实现，不应宣称与完整生产参数和缓存路径完全一致。 示意：第二轮 query 应带上第一轮新获得的预算与用途信息；若代码意外复用 Q0，虽然层数增加、loss 可下降，仍未执行论文的迭代信息回路。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-26d294f33aa7d17b">HyFormer 实现每层 boosting 后，为什么要将更新后的 query 送回下一次 cross-attention？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahyformer">HyFormer: Revisiting the Roles of Sequence Modeling and Feature Interaction in CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin Search</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若始终使用最初 Q，每层只重复同一问题，就丢掉共同演化。当前层 sequence K/V、decoded queries 与 NS tokens 的布局也需对齐，per-token 变换作用在混合布局。本地两 query 缩比是具体实现，不应宣称与完整生产参数和缓存路径完全一致。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第二轮 query 应带上第一轮新获得的预算与用途信息；若代码意外复用 Q0，虽然层数增加、loss 可下降，仍未执行论文的迭代信息回路。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.12681">原论文</a> · <a href="../../../../reproductions/2601.12681-hyformer/">实现解读</a> · <a href="#qa-26d294f33aa7d17b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onetrans" data-paper-title="OneTrans: Unified Feature Interaction and Sequence Modeling with One Transformer in Industrial Recommender" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OneTrans: Unified Feature Interaction and Sequence Modeling with One Transformer in Industrial Recommender 搜广推与 LLM 应用 ByteDance 2025-10-30 OneTrans 把行为 S-tokens 放在异构 NS-tokens 前，使用一个 causal Transformer 同时完成序列建模和字段交互。语义同质的 S-token 共享 QKV/FFN；每个 NS-token 拥有独立参数。因果顺序使 NS-token 能读取完整历史，pyramid stack 逐层只保留近期 S queries。线上用 cross-candidate/cross-request KV cache 复用 S-side 计算。 Fidelity: 完整核心链路复现。本地执行 unified S/NS tokenization、mixed QKV、mixed FFN、causal attention 和 pyramid tail pruning；持久化跨请求 KV 服务系统未复刻。本地对照口径：基线是独立 sequence encoder 后与 candidate 交互的 Encode-then-Interact；实验组是 OneTrans；NDCG@10 从 0.0069 升至 0.0154（+123.58%），但 head share 达 92%。这是统一架构相对 stacked 架构的消融，不是相对 DIN。   搜广推 用户历史与排序骨干 OneTrans 为什么让 S-token 共享参数、NS-token 使用位置专属参数？ 行为事件语义相近，适合共用序列变换；用户、候选等异构字段角色不同，专属参数保留差异。两类统一在因果序列交互，不代表它们变成同质词。更多专属容量也有成本，字段顺序变化须同步参数映射。 示意：所有点击事件可共用 QKV，年龄与商品价格则不必用同一 FFN；若字段交换位置却仍沿旧参数，会把价格当年龄处理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-onetrans-113b41b8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c23a89463d63552a">OneTrans 为什么让 S-token 共享参数、NS-token 使用位置专属参数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonetrans">OneTrans: Unified Feature Interaction and Sequence Modeling with One Transformer in Industrial Recommender</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>行为事件语义相近，适合共用序列变换；用户、候选等异构字段角色不同，专属参数保留差异。两类统一在因果序列交互，不代表它们变成同质词。更多专属容量也有成本，字段顺序变化须同步参数映射。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>所有点击事件可共用 QKV，年龄与商品价格则不必用同一 FFN；若字段交换位置却仍沿旧参数，会把价格当年龄处理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.26104">原论文</a> · <a href="../../../../reproductions/2510.26104-onetrans/">实现解读</a> · <a href="#qa-c23a89463d63552a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onetrans" data-paper-title="OneTrans: Unified Feature Interaction and Sequence Modeling with One Transformer in Industrial Recommender" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OneTrans: Unified Feature Interaction and Sequence Modeling with One Transformer in Industrial Recommender 搜广推与 LLM 应用 ByteDance 2025-10-30 OneTrans 把行为 S-tokens 放在异构 NS-tokens 前，使用一个 causal Transformer 同时完成序列建模和字段交互。语义同质的 S-token 共享 QKV/FFN；每个 NS-token 拥有独立参数。因果顺序使 NS-token 能读取完整历史，pyramid stack 逐层只保留近期 S queries。线上用 cross-candidate/cross-request KV cache 复用 S-side 计算。 Fidelity: 完整核心链路复现。本地执行 unified S/NS tokenization、mixed QKV、mixed FFN、causal attention 和 pyramid tail pruning；持久化跨请求 KV 服务系统未复刻。本地对照口径：基线是独立 sequence encoder 后与 candidate 交互的 Encode-then-Interact；实验组是 OneTrans；NDCG@10 从 0.0069 升至 0.0154（+123.58%），但 head share 达 92%。这是统一架构相对 stacked 架构的消融，不是相对 DIN。   搜广推 用户历史与排序骨干 OneTrans 为什么把行为 token 放在非序列字段之前，并让两类 token 使用不同参数共享方式？ 因果顺序允许后面的字段读取此前全部行为，同时行为状态不依赖后置候选字段，因此可复用用户侧计算。行为 token 语义同质，适合共享 QKV 与 FFN；异构字段含义不同，使用位置专属参数保留差异。金字塔逐层缩短行为查询降低后层开销，但缓存复用仍受时间窗口、参数版本和依赖关系约束。 示意：历史点击序列先编码，后面再放用户属性和候选商品字段。换一个候选时，之前的行为表示可复用；候选字段读取同一历史，却通过自己的参数解释价格与品类。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-3a6324bb9639c16d">OneTrans 为什么把行为 token 放在非序列字段之前，并让两类 token 使用不同参数共享方式？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonetrans">OneTrans: Unified Feature Interaction and Sequence Modeling with One Transformer in Industrial Recommender</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>因果顺序允许后面的字段读取此前全部行为，同时行为状态不依赖后置候选字段，因此可复用用户侧计算。行为 token 语义同质，适合共享 QKV 与 FFN；异构字段含义不同，使用位置专属参数保留差异。金字塔逐层缩短行为查询降低后层开销，但缓存复用仍受时间窗口、参数版本和依赖关系约束。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>历史点击序列先编码，后面再放用户属性和候选商品字段。换一个候选时，之前的行为表示可复用；候选字段读取同一历史，却通过自己的参数解释价格与品类。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.26104">原论文</a> · <a href="../../../../reproductions/2510.26104-onetrans/">实现解读</a> · <a href="#qa-3a6324bb9639c16d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onetrans" data-paper-title="OneTrans: Unified Feature Interaction and Sequence Modeling with One Transformer in Industrial Recommender" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OneTrans: Unified Feature Interaction and Sequence Modeling with One Transformer in Industrial Recommender 搜广推与 LLM 应用 ByteDance 2025-10-30 OneTrans 把行为 S-tokens 放在异构 NS-tokens 前，使用一个 causal Transformer 同时完成序列建模和字段交互。语义同质的 S-token 共享 QKV/FFN；每个 NS-token 拥有独立参数。因果顺序使 NS-token 能读取完整历史，pyramid stack 逐层只保留近期 S queries。线上用 cross-candidate/cross-request KV cache 复用 S-side 计算。 Fidelity: 完整核心链路复现。本地执行 unified S/NS tokenization、mixed QKV、mixed FFN、causal attention 和 pyramid tail pruning；持久化跨请求 KV 服务系统未复刻。本地对照口径：基线是独立 sequence encoder 后与 candidate 交互的 Encode-then-Interact；实验组是 OneTrans；NDCG@10 从 0.0069 升至 0.0154（+123.58%），但 head share 达 92%。这是统一架构相对 stacked 架构的消融，不是相对 DIN。   搜广推 用户历史与排序骨干 OneTrans 的 pyramid S queries 与每层保留完整序列，相比在哪减少成本？ 后层只保留较少近期行为查询，减少输出与后续交互预算，较早历史可通过先前状态或合法 K/V 提供信息。它不是从输入开始完全丢远史，也不是所有层不再有历史依赖。来源小数据高头部集中说明架构正向不等于泛化质量获证。 示意：浅层读较长历史，深层重点更新近期查询；若第一步直接截掉全部远史，就没有同样的信息整合机会。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-26773a58a0fb82a3">OneTrans 的 pyramid S queries 与每层保留完整序列，相比在哪减少成本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonetrans">OneTrans: Unified Feature Interaction and Sequence Modeling with One Transformer in Industrial Recommender</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>后层只保留较少近期行为查询，减少输出与后续交互预算，较早历史可通过先前状态或合法 K/V 提供信息。它不是从输入开始完全丢远史，也不是所有层不再有历史依赖。来源小数据高头部集中说明架构正向不等于泛化质量获证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>浅层读较长历史，深层重点更新近期查询；若第一步直接截掉全部远史，就没有同样的信息整合机会。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.26104">原论文</a> · <a href="../../../../reproductions/2510.26104-onetrans/">实现解读</a> · <a href="#qa-26773a58a0fb82a3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onetrans" data-paper-title="OneTrans: Unified Feature Interaction and Sequence Modeling with One Transformer in Industrial Recommender" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OneTrans: Unified Feature Interaction and Sequence Modeling with One Transformer in Industrial Recommender 搜广推与 LLM 应用 ByteDance 2025-10-30 OneTrans 把行为 S-tokens 放在异构 NS-tokens 前，使用一个 causal Transformer 同时完成序列建模和字段交互。语义同质的 S-token 共享 QKV/FFN；每个 NS-token 拥有独立参数。因果顺序使 NS-token 能读取完整历史，pyramid stack 逐层只保留近期 S queries。线上用 cross-candidate/cross-request KV cache 复用 S-side 计算。 Fidelity: 完整核心链路复现。本地执行 unified S/NS tokenization、mixed QKV、mixed FFN、causal attention 和 pyramid tail pruning；持久化跨请求 KV 服务系统未复刻。本地对照口径：基线是独立 sequence encoder 后与 candidate 交互的 Encode-then-Interact；实验组是 OneTrans；NDCG@10 从 0.0069 升至 0.0154（+123.58%），但 head share 达 92%。这是统一架构相对 stacked 架构的消融，不是相对 DIN。   搜广推 用户历史与排序骨干 OneTrans 的 NS 顺序与 causal mask 为什么决定可见信息？ S 放在前使后面的字段可读历史，S 不读后置候选从而公共可复用；不同 NS 位置之间可见性仍依具体掩码，不可假定任意全交互。跨请求 cache 还需检查历史、时间编码和参数版本，不由同一 user ID 自动有效。 示意：候选在历史后能查前缀，若把它移到前面，后续历史可能读到候选，缓存条件随之改变，不能只移动数组不改契约。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-cc6751d4905424ae">OneTrans 的 NS 顺序与 causal mask 为什么决定可见信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonetrans">OneTrans: Unified Feature Interaction and Sequence Modeling with One Transformer in Industrial Recommender</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>S 放在前使后面的字段可读历史，S 不读后置候选从而公共可复用；不同 NS 位置之间可见性仍依具体掩码，不可假定任意全交互。跨请求 cache 还需检查历史、时间编码和参数版本，不由同一 user ID 自动有效。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>候选在历史后能查前缀，若把它移到前面，后续历史可能读到候选，缓存条件随之改变，不能只移动数组不改契约。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.26104">原论文</a> · <a href="../../../../reproductions/2510.26104-onetrans/">实现解读</a> · <a href="#qa-cc6751d4905424ae">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onepiece" data-paper-title="OnePiece: Bringing Context Engineering and Reasoning to Industrial Cascade Ranking" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OnePiece: Bringing Context Engineering and Reasoning to Industrial Cascade Ranking 搜广推与 LLM 应用 Shopee 2025-09-22 把上下文 token、块级 latent reasoning 与递进多任务目标合并到级联排序器，让召回、点击和价值任务共享表示但分阶段收敛。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 onepiece 核心机制；相对 NDCG@10 +22.87%。  ranking retrieval latent-reasoning multi-task 搜广推 用户历史与排序骨干 OnePiece 为什么同时覆盖召回、点击和价值目标？ 级联各阶段本来接收不同监督，独立优化会失去共享线索；统一上下文与潜在块更新尝试让表示承接多种需求，再通过递进目标安排学习。多目标仍有冲突，潜在状态不能因叫 reasoning 就视为已验证的语言推理。 示意：先理解商品是否相关，再区分是否点击和可能价值，两类知识可互补；但高点击不一定高购买，不能把所有标签合成一个不加区分的正例。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-onepiece-1b14efa1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6cb4f874464f620f">OnePiece 为什么同时覆盖召回、点击和价值目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonepiece">OnePiece: Bringing Context Engineering and Reasoning to Industrial Cascade Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shopee</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>级联各阶段本来接收不同监督，独立优化会失去共享线索；统一上下文与潜在块更新尝试让表示承接多种需求，再通过递进目标安排学习。多目标仍有冲突，潜在状态不能因叫 reasoning 就视为已验证的语言推理。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先理解商品是否相关，再区分是否点击和可能价值，两类知识可互补；但高点击不一定高购买，不能把所有标签合成一个不加区分的正例。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2509.18091">原论文</a> · <a href="../../../../reproductions/2509.18091-onepiece/">实现解读</a> · <a href="#qa-6cb4f874464f620f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onepiece" data-paper-title="OnePiece: Bringing Context Engineering and Reasoning to Industrial Cascade Ranking" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OnePiece: Bringing Context Engineering and Reasoning to Industrial Cascade Ranking 搜广推与 LLM 应用 Shopee 2025-09-22 把上下文 token、块级 latent reasoning 与递进多任务目标合并到级联排序器，让召回、点击和价值任务共享表示但分阶段收敛。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 onepiece 核心机制；相对 NDCG@10 +22.87%。  ranking retrieval latent-reasoning multi-task 搜广推 用户历史与排序骨干 OnePiece 的块级潜在推理与递进多任务权重，为什么比一次性相加所有任务损失更有区别？ 块级更新让上下文条件下的中间状态经过多步残差变换，而不是只在末端接多个头。递进权重再控制各训练阶段由哪些任务主导，使共享表示逐步适应召回、点击和价值目标。关键在更新路径与收敛顺序，不是仅增加任务数；本地代理机制不能证明潜在状态具有可验证的语言推理过程。 示意：先让表示学会区分相关与无关商品，再逐渐提高购买价值目标权重。相较从第一步就同时强推所有目标，这种安排意在减少早期难任务对基础相关性学习的干扰。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-10aa9ef73312afbd">OnePiece 的块级潜在推理与递进多任务权重，为什么比一次性相加所有任务损失更有区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonepiece">OnePiece: Bringing Context Engineering and Reasoning to Industrial Cascade Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shopee</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>块级更新让上下文条件下的中间状态经过多步残差变换，而不是只在末端接多个头。递进权重再控制各训练阶段由哪些任务主导，使共享表示逐步适应召回、点击和价值目标。关键在更新路径与收敛顺序，不是仅增加任务数；本地代理机制不能证明潜在状态具有可验证的语言推理过程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先让表示学会区分相关与无关商品，再逐渐提高购买价值目标权重。相较从第一步就同时强推所有目标，这种安排意在减少早期难任务对基础相关性学习的干扰。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2509.18091">原论文</a> · <a href="../../../../reproductions/2509.18091-onepiece/">实现解读</a> · <a href="#qa-10aa9ef73312afbd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onepiece" data-paper-title="OnePiece: Bringing Context Engineering and Reasoning to Industrial Cascade Ranking" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OnePiece: Bringing Context Engineering and Reasoning to Industrial Cascade Ranking 搜广推与 LLM 应用 Shopee 2025-09-22 把上下文 token、块级 latent reasoning 与递进多任务目标合并到级联排序器，让召回、点击和价值任务共享表示但分阶段收敛。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 onepiece 核心机制；相对 NDCG@10 +22.87%。  ranking retrieval latent-reasoning multi-task 搜广推 用户历史与排序骨干 递进任务权重与从第一步固定等权训练，相比影响什么学习顺序？ 固定权重始终同等施压，递进方案随阶段调任务贡献，让基础相关性与较难价值目标分步收敛。先后可能减少某些冲突，也可能遗忘早期目标，需分阶段指标核验。来源代理结果不支持任意课程都优于固定权重。 示意：早期先学区分无关商品，后期提高价值权重，避免稀疏交易信号过早主导；若后期完全抛弃相关性，也可能学出高价却无关列表。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d12bd2773766ed64">递进任务权重与从第一步固定等权训练，相比影响什么学习顺序？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonepiece">OnePiece: Bringing Context Engineering and Reasoning to Industrial Cascade Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shopee</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定权重始终同等施压，递进方案随阶段调任务贡献，让基础相关性与较难价值目标分步收敛。先后可能减少某些冲突，也可能遗忘早期目标，需分阶段指标核验。来源代理结果不支持任意课程都优于固定权重。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>早期先学区分无关商品，后期提高价值权重，避免稀疏交易信号过早主导；若后期完全抛弃相关性，也可能学出高价却无关列表。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2509.18091">原论文</a> · <a href="../../../../reproductions/2509.18091-onepiece/">实现解读</a> · <a href="#qa-d12bd2773766ed64">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:onepiece" data-paper-title="OnePiece: Bringing Context Engineering and Reasoning to Industrial Cascade Ranking" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="OnePiece: Bringing Context Engineering and Reasoning to Industrial Cascade Ranking 搜广推与 LLM 应用 Shopee 2025-09-22 把上下文 token、块级 latent reasoning 与递进多任务目标合并到级联排序器，让召回、点击和价值任务共享表示但分阶段收敛。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 onepiece 核心机制；相对 NDCG@10 +22.87%。  ranking retrieval latent-reasoning multi-task 搜广推 用户历史与排序骨干 OnePiece 的 H(k+1) 残差更新与 αt(k) 调度，应怎样分别验收？ 前者是当前上下文条件下表示逐块更新，后者是训练阶段的任务权重，两种 k 必须按实现定义避免混淆。需看到中间状态传递与实际 loss 权重变化，而不是只在结果表写课程名称。本地固定 scorer 的机制范围不能自动扩展到完整级联训练。 示意：增加网络块数不意味着训练权重已递进，调整 loss 也不意味着潜状态多步更新；两条路径需要各自的配置与日志证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d554085990e57412">OnePiece 的 H(k+1) 残差更新与 αt(k) 调度，应怎样分别验收？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aonepiece">OnePiece: Bringing Context Engineering and Reasoning to Industrial Cascade Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shopee</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者是当前上下文条件下表示逐块更新，后者是训练阶段的任务权重，两种 k 必须按实现定义避免混淆。需看到中间状态传递与实际 loss 权重变化，而不是只在结果表写课程名称。本地固定 scorer 的机制范围不能自动扩展到完整级联训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>增加网络块数不意味着训练权重已递进，调整 loss 也不意味着潜状态多步更新；两条路径需要各自的配置与日志证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2509.18091">原论文</a> · <a href="../../../../reproductions/2509.18091-onepiece/">实现解读</a> · <a href="#qa-d554085990e57412">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:argus" data-paper-title="Scaling Recommender Transformers to One Billion Parameters" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Scaling Recommender Transformers to One Billion Parameters 搜广推与 LLM 应用 Yandex 2025-07-21 直接 next-item 预测把“用户会怎样反馈”和“会消费哪个 item”纠缠。ARGUS 先预测 feedback token，再以其条件化 next-item，使多种反馈共享序列主干并获得更好的 scaling。 两种口径均未验证收益。Fidelity: 核心机制复现。matched Transformer 中实际执行 feedback-first、next-item-second 分解；未复刻十亿参数规模与私有音乐反馈。本地对照口径：统一跨模型基线是 DIN，ARGUS NDCG@10 相对 DIN -4.12%；内部 next-item-only 基线加入 feedback decomposition 后 -20.95%。两种口径均未验证收益。统一为 180 users/280 items 后，DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；  long-sequence transformer multi-task 搜广推 用户历史与排序骨干 ARGUS 把下一步分成 feedback 与 item 两部分，联合分布如何理解？ 先由历史估计反馈类型概率，再在该反馈条件下预测物品，两项相乘组成下一步联合分布。反馈不是事后附加标签，而是决定物品分布的一部分；训练可以用已发生反馈作监督，推理却不能提前知道用户真正会做出的反馈。 示意：同一历史在“点赞”条件下可能偏向有共鸣视频，在“长看”条件下偏向完整教程；上线需要模型预测或指定条件，不能偷读下一次真实动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-argus-3c7d662d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-06db608db356f93c">ARGUS 把下一步分成 feedback 与 item 两部分，联合分布如何理解？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aargus">Scaling Recommender Transformers to One Billion Parameters</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Yandex</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>先由历史估计反馈类型概率，再在该反馈条件下预测物品，两项相乘组成下一步联合分布。反馈不是事后附加标签，而是决定物品分布的一部分；训练可以用已发生反馈作监督，推理却不能提前知道用户真正会做出的反馈。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一历史在“点赞”条件下可能偏向有共鸣视频，在“长看”条件下偏向完整教程；上线需要模型预测或指定条件，不能偷读下一次真实动作。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.15994">原论文</a> · <a href="../../../../reproductions/2507.15994-argus/">实现解读</a> · <a href="#qa-06db608db356f93c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:argus" data-paper-title="Scaling Recommender Transformers to One Billion Parameters" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Scaling Recommender Transformers to One Billion Parameters 搜广推与 LLM 应用 Yandex 2025-07-21 直接 next-item 预测把“用户会怎样反馈”和“会消费哪个 item”纠缠。ARGUS 先预测 feedback token，再以其条件化 next-item，使多种反馈共享序列主干并获得更好的 scaling。 两种口径均未验证收益。Fidelity: 核心机制复现。matched Transformer 中实际执行 feedback-first、next-item-second 分解；未复刻十亿参数规模与私有音乐反馈。本地对照口径：统一跨模型基线是 DIN，ARGUS NDCG@10 相对 DIN -4.12%；内部 next-item-only 基线加入 feedback decomposition 后 -20.95%。两种口径均未验证收益。统一为 180 users/280 items 后，DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；  long-sequence transformer multi-task 搜广推 用户历史与排序骨干 ARGUS先预测feedback token再预测物品，和直接预测下一个物品有何差别？ 直接next-item把消费对象与反馈类型混在一个目标里。ARGUS将联合概率拆为先判断用户会产生何种反馈，再在该条件下选择物品，使多种反馈共享主干却保留条件差异；推理时预测反馈不能偷读真实未来行为。本地对应消融出现负结果，因此不能把这种分解视为必然更优。 示意：同一历史既可能接着长看纪录片，也可能快速划走短视频；先区分预期反馈，再选对象，表达的是联合行为，而不是只猜物品名字。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-34e00691c873ae6a">ARGUS先预测feedback token再预测物品，和直接预测下一个物品有何差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aargus">Scaling Recommender Transformers to One Billion Parameters</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Yandex</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直接next-item把消费对象与反馈类型混在一个目标里。ARGUS将联合概率拆为先判断用户会产生何种反馈，再在该条件下选择物品，使多种反馈共享主干却保留条件差异；推理时预测反馈不能偷读真实未来行为。本地对应消融出现负结果，因此不能把这种分解视为必然更优。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一历史既可能接着长看纪录片，也可能快速划走短视频；先区分预期反馈，再选对象，表达的是联合行为，而不是只猜物品名字。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.15994">原论文</a> · <a href="../../../../reproductions/2507.15994-argus/">实现解读</a> · <a href="#qa-34e00691c873ae6a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:argus" data-paper-title="Scaling Recommender Transformers to One Billion Parameters" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Scaling Recommender Transformers to One Billion Parameters 搜广推与 LLM 应用 Yandex 2025-07-21 直接 next-item 预测把“用户会怎样反馈”和“会消费哪个 item”纠缠。ARGUS 先预测 feedback token，再以其条件化 next-item，使多种反馈共享序列主干并获得更好的 scaling。 两种口径均未验证收益。Fidelity: 核心机制复现。matched Transformer 中实际执行 feedback-first、next-item-second 分解；未复刻十亿参数规模与私有音乐反馈。本地对照口径：统一跨模型基线是 DIN，ARGUS NDCG@10 相对 DIN -4.12%；内部 next-item-only 基线加入 feedback decomposition 后 -20.95%。两种口径均未验证收益。统一为 180 users/280 items 后，DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；  long-sequence transformer multi-task 搜广推 用户历史与排序骨干 ARGUS 的条件分解与简单增加一个并行反馈辅助头，有何信息流区别？ 并行头可给共享主干额外监督，但物品头未必使用反馈预测。ARGUS 的分解要求物品分布显式以反馈为条件，改变生成路径而非只改变损失数量。反馈预测错误会传给物品选择，因此需要分别检查反馈质量和条件物品预测，不能只看总 loss。 示意：一个模型同时输出“会点赞”和候选电影但两头不相连，只是多任务；若电影分布实际接收反馈 token，才会随反馈条件变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e31c2f745c08191d">ARGUS 的条件分解与简单增加一个并行反馈辅助头，有何信息流区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aargus">Scaling Recommender Transformers to One Billion Parameters</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Yandex</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>并行头可给共享主干额外监督，但物品头未必使用反馈预测。ARGUS 的分解要求物品分布显式以反馈为条件，改变生成路径而非只改变损失数量。反馈预测错误会传给物品选择，因此需要分别检查反馈质量和条件物品预测，不能只看总 loss。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个模型同时输出“会点赞”和候选电影但两头不相连，只是多任务；若电影分布实际接收反馈 token，才会随反馈条件变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.15994">原论文</a> · <a href="../../../../reproductions/2507.15994-argus/">实现解读</a> · <a href="#qa-e31c2f745c08191d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:argus" data-paper-title="Scaling Recommender Transformers to One Billion Parameters" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Scaling Recommender Transformers to One Billion Parameters 搜广推与 LLM 应用 Yandex 2025-07-21 直接 next-item 预测把“用户会怎样反馈”和“会消费哪个 item”纠缠。ARGUS 先预测 feedback token，再以其条件化 next-item，使多种反馈共享序列主干并获得更好的 scaling。 两种口径均未验证收益。Fidelity: 核心机制复现。matched Transformer 中实际执行 feedback-first、next-item-second 分解；未复刻十亿参数规模与私有音乐反馈。本地对照口径：统一跨模型基线是 DIN，ARGUS NDCG@10 相对 DIN -4.12%；内部 next-item-only 基线加入 feedback decomposition 后 -20.95%。两种口径均未验证收益。统一为 180 users/280 items 后，DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；  long-sequence transformer multi-task 搜广推 用户历史与排序骨干 ARGUS 本地比较中，为什么要区分 DIN 与 next-item-only 两个基线？ DIN 是统一跨模型参照，next-item-only 则隔离是否加入反馈分解。两者回答的问题不同：前者比较整体模型，后者检查定义性模块。本地两种口径都未验证收益，不能挑较好的一种数值，把反馈分解本身的负结果隐藏掉。 示意：即使某整体模型接近 DIN，也可能是其基础骨干较强，新增反馈路径反而退化；只有同骨干去掉该路径的对照才能识别模块变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a3a287cea14c8c52">ARGUS 本地比较中，为什么要区分 DIN 与 next-item-only 两个基线？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aargus">Scaling Recommender Transformers to One Billion Parameters</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Yandex</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>DIN 是统一跨模型参照，next-item-only 则隔离是否加入反馈分解。两者回答的问题不同：前者比较整体模型，后者检查定义性模块。本地两种口径都未验证收益，不能挑较好的一种数值，把反馈分解本身的负结果隐藏掉。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>即使某整体模型接近 DIN，也可能是其基础骨干较强，新增反馈路径反而退化；只有同骨干去掉该路径的对照才能识别模块变化。</p>
<p class="ar-learning-sources">依据：本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.15994">原论文</a> · <a href="../../../../reproductions/2507.15994-argus/">实现解读</a> · <a href="#qa-a3a287cea14c8c52">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rankmixer" data-paper-title="RankMixer: Scaling Up Ranking Models in Industrial Recommenders" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="RankMixer: Scaling Up Ranking Models in Industrial Recommenders 搜广推与 LLM 应用 ByteDance / Douyin 2025-07-21 RankMixer 用固定的多头 TokenMix 让不同 feature token 的分量相遇，再由各 token 独立的 FFN 学习组合。这里替换的是异构特征交互模块；上游长序列模块仍可使用 attention。 本地只有 seed 42 的 smoke。Shared FFN 与 Dense per-token 都含 TokenMix，且参数量不同，不能据此验证 TokenMix 优于 attention。Sparse 没有追平 Dense，当前路由与原文双 router DTSI 仍有差异。 TokenMix 没有可训练参数，整个模型为什么仍能学习特征关系？  搜广推 用户历史与排序骨干 RankMixer 去掉的 attention 到底是哪一部分，序列输入还能用注意力吗？ 替换的是异构字段 feature interaction，输入的行为序列可先经独立序列模块处理，该模块不必去掉 attention。TokenMix 将字段通道重排后交给独立 FFN 学关系。将论文称为整个系统完全无注意力会忽略前置序列建模和特征来源。 示意：历史先用序列注意力提取摄影兴趣，再与价格、候选字段进入 RankMixer；字段交叉无 QK 注意力，不代表第一步也被禁止。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-rankmixer-298d1226" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-558c5d17470ec022">RankMixer 去掉的 attention 到底是哪一部分，序列输入还能用注意力吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arankmixer">RankMixer: Scaling Up Ranking Models in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>替换的是异构字段 feature interaction，输入的行为序列可先经独立序列模块处理，该模块不必去掉 attention。TokenMix 将字段通道重排后交给独立 FFN 学关系。将论文称为整个系统完全无注意力会忽略前置序列建模和特征来源。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>历史先用序列注意力提取摄影兴趣，再与价格、候选字段进入 RankMixer；字段交叉无 QK 注意力，不代表第一步也被禁止。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.15551">原论文</a> · <a href="../../../../reproductions/2507.15551-rankmixer/">实现解读</a> · <a href="#qa-558c5d17470ec022">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rankmixer" data-paper-title="RankMixer: Scaling Up Ranking Models in Industrial Recommenders" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="RankMixer: Scaling Up Ranking Models in Industrial Recommenders 搜广推与 LLM 应用 ByteDance / Douyin 2025-07-21 RankMixer 用固定的多头 TokenMix 让不同 feature token 的分量相遇，再由各 token 独立的 FFN 学习组合。这里替换的是异构特征交互模块；上游长序列模块仍可使用 attention。 本地只有 seed 42 的 smoke。Shared FFN 与 Dense per-token 都含 TokenMix，且参数量不同，不能据此验证 TokenMix 优于 attention。Sparse 没有追平 Dense，当前路由与原文双 router DTSI 仍有差异。 TokenMix 没有可训练参数，整个模型为什么仍能学习特征关系？  搜广推 用户历史与排序骨干 固定TokenMix没有学习权重，为什么后面的独立FFN仍能学到跨字段交互？ TokenMix先按head切开每个输入token，再把各输入的同号片段拼成新token，让不同字段的信号进入同一个非线性FFN。学习发生在混合后的专属变换中，而非动态相似度权重；原文取head数等于token数并要求维度可整除。它替换字段交互，不意味着序列模块也应取消attention。 示意：用户、商品和场景各拆三块，同号块被送到一起；FFN可联合判断其中的年龄、品类和时段关系，固定搬运本身不需要先计算相似度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-a18a983529fe37d7">固定TokenMix没有学习权重，为什么后面的独立FFN仍能学到跨字段交互？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arankmixer">RankMixer: Scaling Up Ranking Models in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>TokenMix先按head切开每个输入token，再把各输入的同号片段拼成新token，让不同字段的信号进入同一个非线性FFN。学习发生在混合后的专属变换中，而非动态相似度权重；原文取head数等于token数并要求维度可整除。它替换字段交互，不意味着序列模块也应取消attention。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户、商品和场景各拆三块，同号块被送到一起；FFN可联合判断其中的年龄、品类和时段关系，固定搬运本身不需要先计算相似度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.15551">原论文</a> · <a href="../../../../reproductions/2507.15551-rankmixer/">实现解读</a> · <a href="#qa-a18a983529fe37d7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rankmixer" data-paper-title="RankMixer: Scaling Up Ranking Models in Industrial Recommenders" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="RankMixer: Scaling Up Ranking Models in Industrial Recommenders 搜广推与 LLM 应用 ByteDance / Douyin 2025-07-21 RankMixer 用固定的多头 TokenMix 让不同 feature token 的分量相遇，再由各 token 独立的 FFN 学习组合。这里替换的是异构特征交互模块；上游长序列模块仍可使用 attention。 本地只有 seed 42 的 smoke。Shared FFN 与 Dense per-token 都含 TokenMix，且参数量不同，不能据此验证 TokenMix 优于 attention。Sparse 没有追平 Dense，当前路由与原文双 router DTSI 仍有差异。 TokenMix 没有可训练参数，整个模型为什么仍能学习特征关系？  搜广推 用户历史与排序骨干 RankMixer 的 ReLU 路由和双路由 DTSI 分别解决什么问题，为什么只做稀疏 top-k 不够？ ReLU 加稀疏正则允许不同 token 激活不同数量专家，处理固定 top-k 分配预算过于僵硬的问题。DTSI 另设训练与推理路由，稀疏正则只加在推理路由上，使专家训练不因稀疏选择长期饥饿。两者分别控制动态激活和专家训练覆盖；本地稀疏路径尚不能视作原文双路由方案的等价验证。 示意：信息复杂的 token 可用更多专家，简单 token 少用；训练时仍给较少被选专家足够学习机会。若从头只更新固定少数专家，其余专家即使参数很多也可能一直没有学好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-473b102f64b8ecd6">RankMixer 的 ReLU 路由和双路由 DTSI 分别解决什么问题，为什么只做稀疏 top-k 不够？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arankmixer">RankMixer: Scaling Up Ranking Models in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>ReLU 加稀疏正则允许不同 token 激活不同数量专家，处理固定 top-k 分配预算过于僵硬的问题。DTSI 另设训练与推理路由，稀疏正则只加在推理路由上，使专家训练不因稀疏选择长期饥饿。两者分别控制动态激活和专家训练覆盖；本地稀疏路径尚不能视作原文双路由方案的等价验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>信息复杂的 token 可用更多专家，简单 token 少用；训练时仍给较少被选专家足够学习机会。若从头只更新固定少数专家，其余专家即使参数很多也可能一直没有学好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.15551">原论文</a> · <a href="../../../../reproductions/2507.15551-rankmixer/">实现解读</a> · <a href="#qa-473b102f64b8ecd6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rankmixer" data-paper-title="RankMixer: Scaling Up Ranking Models in Industrial Recommenders" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="RankMixer: Scaling Up Ranking Models in Industrial Recommenders 搜广推与 LLM 应用 ByteDance / Douyin 2025-07-21 RankMixer 用固定的多头 TokenMix 让不同 feature token 的分量相遇，再由各 token 独立的 FFN 学习组合。这里替换的是异构特征交互模块；上游长序列模块仍可使用 attention。 本地只有 seed 42 的 smoke。Shared FFN 与 Dense per-token 都含 TokenMix，且参数量不同，不能据此验证 TokenMix 优于 attention。Sparse 没有追平 Dense，当前路由与原文双 router DTSI 仍有差异。 TokenMix 没有可训练参数，整个模型为什么仍能学习特征关系？  搜广推 用户历史与排序骨干 RankMixer 本地 Dense 对 Shared FFN 的大提升，为什么不能全归无参数 TokenMix？ 两组本来都执行 TokenMix，主要差异含共享与混合 token 专属 FFN，并且参数量明显不同。比较支持该缩比配置变化，不能隔离重排本身；稀疏组又未追平 dense。公平结论应同时说明预算、头部偏置与 sparse 差距。 示意：两辆车都有同样传动器，换更大独立引擎后提速，不能全说传动器发明有效；本地数值也不能替原文 MFU 与生产 A/B。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-603d4772b072a0eb">RankMixer 本地 Dense 对 Shared FFN 的大提升，为什么不能全归无参数 TokenMix？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arankmixer">RankMixer: Scaling Up Ranking Models in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两组本来都执行 TokenMix，主要差异含共享与混合 token 专属 FFN，并且参数量明显不同。比较支持该缩比配置变化，不能隔离重排本身；稀疏组又未追平 dense。公平结论应同时说明预算、头部偏置与 sparse 差距。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两辆车都有同样传动器，换更大独立引擎后提速，不能全说传动器发明有效；本地数值也不能替原文 MFU 与生产 A/B。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.15551">原论文</a> · <a href="../../../../reproductions/2507.15551-rankmixer/">实现解读</a> · <a href="#qa-603d4772b072a0eb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rankmixer" data-paper-title="RankMixer: Scaling Up Ranking Models in Industrial Recommenders" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="RankMixer: Scaling Up Ranking Models in Industrial Recommenders 搜广推与 LLM 应用 ByteDance / Douyin 2025-07-21 RankMixer 用固定的多头 TokenMix 让不同 feature token 的分量相遇，再由各 token 独立的 FFN 学习组合。这里替换的是异构特征交互模块；上游长序列模块仍可使用 attention。 本地只有 seed 42 的 smoke。Shared FFN 与 Dense per-token 都含 TokenMix，且参数量不同，不能据此验证 TokenMix 优于 attention。Sparse 没有追平 Dense，当前路由与原文双 router DTSI 仍有差异。 TokenMix 没有可训练参数，整个模型为什么仍能学习特征关系？  搜广推 用户历史与排序骨干 RankMixer 为什么设置 head 数 H 等于 token 数 T，并要求隐藏维度可整除？ 每个输入 token 被等分为 H 个长度 D/H 的片段，混合后得到 H 个长度 TD/H 的新 token。取 H=T 才恢复 T×D 形状，能与原输入直接做残差相加；D 也必须能被 H 整除。这里是张量布局条件，不是注意力头的语义约束，随意换 token 数却保留原 reshape 会改变或破坏结构。 示意：四个64维 token 各拆四份，每份16维；同号四份拼接后仍是四个64维 token。若改成三个 head，64无法等分，原样重排和残差就不成立。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-67c000ac06ff074b">RankMixer 为什么设置 head 数 H 等于 token 数 T，并要求隐藏维度可整除？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arankmixer">RankMixer: Scaling Up Ranking Models in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每个输入 token 被等分为 H 个长度 D/H 的片段，混合后得到 H 个长度 TD/H 的新 token。取 H=T 才恢复 T×D 形状，能与原输入直接做残差相加；D 也必须能被 H 整除。这里是张量布局条件，不是注意力头的语义约束，随意换 token 数却保留原 reshape 会改变或破坏结构。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>四个64维 token 各拆四份，每份16维；同号四份拼接后仍是四个64维 token。若改成三个 head，64无法等分，原样重排和残差就不成立。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.15551">原论文</a> · <a href="../../../../reproductions/2507.15551-rankmixer/">实现解读</a> · <a href="#qa-67c000ac06ff074b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:rankmixer" data-paper-title="RankMixer: Scaling Up Ranking Models in Industrial Recommenders" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="RankMixer: Scaling Up Ranking Models in Industrial Recommenders 搜广推与 LLM 应用 ByteDance / Douyin 2025-07-21 RankMixer 用固定的多头 TokenMix 让不同 feature token 的分量相遇，再由各 token 独立的 FFN 学习组合。这里替换的是异构特征交互模块；上游长序列模块仍可使用 attention。 本地只有 seed 42 的 smoke。Shared FFN 与 Dense per-token 都含 TokenMix，且参数量不同，不能据此验证 TokenMix 优于 attention。Sparse 没有追平 Dense，当前路由与原文双 router DTSI 仍有差异。 TokenMix 没有可训练参数，整个模型为什么仍能学习特征关系？  搜广推 用户历史与排序骨干 RankMixer 的 per-token FFN 参数是对应原字段还是 TokenMix 后的位置？ FFN 接收的是重排后 token，每个位置含所有原 token 的同号 head，因此专属参数服务混合子空间，而非永远一套只管年龄、一套只管价格。输入字段 token、head 和输出位置需正确对应；旧字段名称不能直接解释所有深层专家语义。 示意：四字段各取第一片拼成新 token，一号 FFN同时看四字段片段；说它只处理第一个原字段，就误读了真正信息流。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ad1e554a4b682966">RankMixer 的 per-token FFN 参数是对应原字段还是 TokenMix 后的位置？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Arankmixer">RankMixer: Scaling Up Ranking Models in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>FFN 接收的是重排后 token，每个位置含所有原 token 的同号 head，因此专属参数服务混合子空间，而非永远一套只管年龄、一套只管价格。输入字段 token、head 和输出位置需正确对应；旧字段名称不能直接解释所有深层专家语义。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>四字段各取第一片拼成新 token，一号 FFN同时看四字段片段；说它只处理第一个原字段，就误读了真正信息流。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.15551">原论文</a> · <a href="../../../../reproductions/2507.15551-rankmixer/">实现解读</a> · <a href="#qa-ad1e554a4b682966">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pinfm" data-paper-title="PinFM: Foundation Model for User Activity Sequences at a Billion-scale Visual Discovery Platform" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="PinFM: Foundation Model for User Activity Sequences at a Billion-scale Visual Discovery Platform 搜广推与 LLM 应用 Pinterest 2025-07-17 PinFM 把“先在跨场景用户行为上预训练，再接入各排序模型微调”的 Foundation Model 范式带到工业推荐。decoder-only backbone 学习 next/multi/future token；下游把候选追加到用户序列做 early fusion。DCAT 利用同一请求的候选共享用户历史，把 context self-attention 只算一次，然后让候选对缓存的 context KV 做 cross-attention。 保真度：核心机制复现。保真度：核心机制复现。NTL/MTL/FTL 对比预训练、预训练后下游微调、candidate early fusion、Candidate ID Randomization、backbone 低学习率和 DCAT 均实际执行；省略 Pinterest 多 action/surface 语料、fresh-item age dropout、分布式 20B embedding、int4 与 Triton kernel。本地对照口径：基线是 scratch DCAT；实验组是预训练后微调的 PinFM；   搜广推 用户历史与排序骨干 PinFM 的 next、multi、future token 目标为什么共同用于用户基础表征？ 紧邻下一项、未来窗口与从指定位置看后续分别提供不同时间粒度监督，减少只记最近行为的局限，再迁到各排序任务。辅助未来属于训练目标，不可提前输入。跨场景预训也可能负迁移，不能由基础模型称谓预设所有场景改善。 示意：下一次点击教即时意图，窗口多个内容教并存兴趣，较远目标补长期方向；三类标签都只用于训练，线上仍只读已发生行为。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-pinfm-c653f7d8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-73e242cb9a591ae2">PinFM 的 next、multi、future token 目标为什么共同用于用户基础表征？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apinfm">PinFM: Foundation Model for User Activity Sequences at a Billion-scale Visual Discovery Platform</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>紧邻下一项、未来窗口与从指定位置看后续分别提供不同时间粒度监督，减少只记最近行为的局限，再迁到各排序任务。辅助未来属于训练目标，不可提前输入。跨场景预训也可能负迁移，不能由基础模型称谓预设所有场景改善。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>下一次点击教即时意图，窗口多个内容教并存兴趣，较远目标补长期方向；三类标签都只用于训练，线上仍只读已发生行为。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.12704">原论文</a> · <a href="../../../../reproductions/2507.12704-pinfm/">实现解读</a> · <a href="#qa-73e242cb9a591ae2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pinfm" data-paper-title="PinFM: Foundation Model for User Activity Sequences at a Billion-scale Visual Discovery Platform" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="PinFM: Foundation Model for User Activity Sequences at a Billion-scale Visual Discovery Platform 搜广推与 LLM 应用 Pinterest 2025-07-17 PinFM 把“先在跨场景用户行为上预训练，再接入各排序模型微调”的 Foundation Model 范式带到工业推荐。decoder-only backbone 学习 next/multi/future token；下游把候选追加到用户序列做 early fusion。DCAT 利用同一请求的候选共享用户历史，把 context self-attention 只算一次，然后让候选对缓存的 context KV 做 cross-attention。 保真度：核心机制复现。保真度：核心机制复现。NTL/MTL/FTL 对比预训练、预训练后下游微调、candidate early fusion、Candidate ID Randomization、backbone 低学习率和 DCAT 均实际执行；省略 Pinterest 多 action/surface 语料、fresh-item age dropout、分布式 20B embedding、int4 与 Triton kernel。本地对照口径：基线是 scratch DCAT；实验组是预训练后微调的 PinFM；   搜广推 用户历史与排序骨干 PinFM 的 DCAT 为什么能保留候选早融合，同时避免每个候选重算用户上下文？ 早融合让候选在模型内部与历史交互，但把同一用户历史为每个候选重复展开会浪费大量计算。DCAT 先对去重后的上下文做一次自注意力并缓存各层 K/V，再让候选侧查询读取这些状态。复用的前提是上下文计算不依赖被替换的候选；预训练收益与这种服务优化是不同问题，本地负结果也需保留。 示意：一位用户有五百条历史、待评一百个候选。先算一份历史记忆，再让每个候选读取相关部分，比复制一百份历史各算一次更省，而候选仍能在层内接触历史。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-4eaf16c90d354ace">PinFM 的 DCAT 为什么能保留候选早融合，同时避免每个候选重算用户上下文？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apinfm">PinFM: Foundation Model for User Activity Sequences at a Billion-scale Visual Discovery Platform</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>早融合让候选在模型内部与历史交互，但把同一用户历史为每个候选重复展开会浪费大量计算。DCAT 先对去重后的上下文做一次自注意力并缓存各层 K/V，再让候选侧查询读取这些状态。复用的前提是上下文计算不依赖被替换的候选；预训练收益与这种服务优化是不同问题，本地负结果也需保留。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一位用户有五百条历史、待评一百个候选。先算一份历史记忆，再让每个候选读取相关部分，比复制一百份历史各算一次更省，而候选仍能在层内接触历史。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.12704">原论文</a> · <a href="../../../../reproductions/2507.12704-pinfm/">实现解读</a> · <a href="#qa-4eaf16c90d354ace">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pinfm" data-paper-title="PinFM: Foundation Model for User Activity Sequences at a Billion-scale Visual Discovery Platform" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="PinFM: Foundation Model for User Activity Sequences at a Billion-scale Visual Discovery Platform 搜广推与 LLM 应用 Pinterest 2025-07-17 PinFM 把“先在跨场景用户行为上预训练，再接入各排序模型微调”的 Foundation Model 范式带到工业推荐。decoder-only backbone 学习 next/multi/future token；下游把候选追加到用户序列做 early fusion。DCAT 利用同一请求的候选共享用户历史，把 context self-attention 只算一次，然后让候选对缓存的 context KV 做 cross-attention。 保真度：核心机制复现。保真度：核心机制复现。NTL/MTL/FTL 对比预训练、预训练后下游微调、candidate early fusion、Candidate ID Randomization、backbone 低学习率和 DCAT 均实际执行；省略 Pinterest 多 action/surface 语料、fresh-item age dropout、分布式 20B embedding、int4 与 Triton kernel。本地对照口径：基线是 scratch DCAT；实验组是预训练后微调的 PinFM；   搜广推 用户历史与排序骨干 PinFM 的 scratch DCAT 与预训后微调，对照为何不同于 DCAT 对普通 Transformer？ 两组都用 DCAT 时隔离的是预训练知识增量，换结构对照才检验缓存分解或早融合方式。来源本地预训版本选择后 test 为负，不能因为 DCAT 数学保真就声称预训有效。效率与表征迁移的证据应分别记。 示意：两辆车同底盘，一辆先做跨域训练，差异检验训练配方；不能把结果解释成底盘优于另一种从未参与比较的结构。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c67c18389f789088">PinFM 的 scratch DCAT 与预训后微调，对照为何不同于 DCAT 对普通 Transformer？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apinfm">PinFM: Foundation Model for User Activity Sequences at a Billion-scale Visual Discovery Platform</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两组都用 DCAT 时隔离的是预训练知识增量，换结构对照才检验缓存分解或早融合方式。来源本地预训版本选择后 test 为负，不能因为 DCAT 数学保真就声称预训有效。效率与表征迁移的证据应分别记。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两辆车同底盘，一辆先做跨域训练，差异检验训练配方；不能把结果解释成底盘优于另一种从未参与比较的结构。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.12704">原论文</a> · <a href="../../../../reproductions/2507.12704-pinfm/">实现解读</a> · <a href="#qa-c67c18389f789088">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:pinfm" data-paper-title="PinFM: Foundation Model for User Activity Sequences at a Billion-scale Visual Discovery Platform" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="PinFM: Foundation Model for User Activity Sequences at a Billion-scale Visual Discovery Platform 搜广推与 LLM 应用 Pinterest 2025-07-17 PinFM 把“先在跨场景用户行为上预训练，再接入各排序模型微调”的 Foundation Model 范式带到工业推荐。decoder-only backbone 学习 next/multi/future token；下游把候选追加到用户序列做 early fusion。DCAT 利用同一请求的候选共享用户历史，把 context self-attention 只算一次，然后让候选对缓存的 context KV 做 cross-attention。 保真度：核心机制复现。保真度：核心机制复现。NTL/MTL/FTL 对比预训练、预训练后下游微调、candidate early fusion、Candidate ID Randomization、backbone 低学习率和 DCAT 均实际执行；省略 Pinterest 多 action/surface 语料、fresh-item age dropout、分布式 20B embedding、int4 与 Triton kernel。本地对照口径：基线是 scratch DCAT；实验组是预训练后微调的 PinFM；   搜广推 用户历史与排序骨干 DCAT 全库推理为何要确认真正复用 context K/V，而非每个候选重算后丢弃？ 分解要求公共 context self-attention 一次形成缓存，候选层只计算其查询与合法候选侧部分。数值输出相同不代表效率路径相同，需检查执行次数与依赖。缓存受历史和版本约束，不能把候选相关状态误放公共区。 示意：循环一千个候选每次重算历史再取最后输出，可能与缓存版分数接近，却没有摊销成本；只看 NDCG 无法证明复用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-fdbf98eb2bd2f065">DCAT 全库推理为何要确认真正复用 context K/V，而非每个候选重算后丢弃？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Apinfm">PinFM: Foundation Model for User Activity Sequences at a Billion-scale Visual Discovery Platform</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分解要求公共 context self-attention 一次形成缓存，候选层只计算其查询与合法候选侧部分。数值输出相同不代表效率路径相同，需检查执行次数与依赖。缓存受历史和版本约束，不能把候选相关状态误放公共区。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>循环一千个候选每次重算历史再取最后输出，可能与缓存版分数接近，却没有摊销成本；只看 NDCG 无法证明复用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.12704">原论文</a> · <a href="../../../../reproductions/2507.12704-pinfm/">实现解读</a> · <a href="#qa-fdbf98eb2bd2f065">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:transact-v2" data-paper-title="TransAct V2: Lifelong User Action Sequence Modeling on Pinterest Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TransAct V2: Lifelong User Action Sequence Modeling on Pinterest Recommendation 搜广推与 LLM 应用 Pinterest 2025-06-02 TransAct 主要建模约百条实时行为，容易忽略用户多年的长期兴趣。TransAct V2 从约条 lifelong 序列中按候选相似度取回相关行为，同时保留最近行为，再通过共享 Transformer 做 CTR 排序；额外的 Next Action Loss 迫使序列表征预测下一次正向互动。论文也包含 SKUT、request deduplication 等 serving 优化，本地复现聚焦模型链路。 保真度：核心机制复现。保真度：核心机制复现。候选锚定的长/短序列近邻检索、最近行为保留、early-fusion causal Transformer 和 Next Action Loss 均实际训练；MovieLens genre 替代 PinSage embedding，省略 Pinterest action/surface 字段、曝光日志负例及生产 Triton kernel。本地对照口径：基线是参数量匹配的 TransAct；实验组是 TransAct V2；NDCG@10 从 0.01277 升至 0.02460（+92.65%），head share 同时 +14.70pt。   搜广推 用户历史与排序骨干 TransAct V2为什么把lifelong与recent历史一起用？ 近期表达即时意图，候选锚定检索从长期找相关证据，两者互补。统一Transformer再early fusion候选，不是用长历史简单替换所有实时信息。 例如最近一次浏览可与多年前相似兴趣同时帮助当前候选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-transact-v2-c124d4cb" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b825891732ff4c2e">TransAct V2为什么把lifelong与recent历史一起用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atransact-v2">TransAct V2: Lifelong User Action Sequence Modeling on Pinterest Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>近期表达即时意图，候选锚定检索从长期找相关证据，两者互补。统一Transformer再early fusion候选，不是用长历史简单替换所有实时信息。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如最近一次浏览可与多年前相似兴趣同时帮助当前候选。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2506.02267">原论文</a> · <a href="../../../../reproductions/2506.02267-transact-v2/">实现解读</a> · <a href="#qa-b825891732ff4c2e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:transact-v2" data-paper-title="TransAct V2: Lifelong User Action Sequence Modeling on Pinterest Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TransAct V2: Lifelong User Action Sequence Modeling on Pinterest Recommendation 搜广推与 LLM 应用 Pinterest 2025-06-02 TransAct 主要建模约百条实时行为，容易忽略用户多年的长期兴趣。TransAct V2 从约条 lifelong 序列中按候选相似度取回相关行为，同时保留最近行为，再通过共享 Transformer 做 CTR 排序；额外的 Next Action Loss 迫使序列表征预测下一次正向互动。论文也包含 SKUT、request deduplication 等 serving 优化，本地复现聚焦模型链路。 保真度：核心机制复现。保真度：核心机制复现。候选锚定的长/短序列近邻检索、最近行为保留、early-fusion causal Transformer 和 Next Action Loss 均实际训练；MovieLens genre 替代 PinSage embedding，省略 Pinterest action/surface 字段、曝光日志负例及生产 Triton kernel。本地对照口径：基线是参数量匹配的 TransAct；实验组是 TransAct V2；NDCG@10 从 0.01277 升至 0.02460（+92.65%），head share 同时 +14.70pt。   搜广推 用户历史与排序骨干 TransAct V2 为什么候选检索终身历史时仍保留一段原样近期行为，并增加 Next Action Loss？ 相似度检索擅长找到与当前候选相关的旧事件，却可能遗漏刚形成但尚未显式相似的新意图。保留近期分支保证即时信号可见，再用共享 Transformer 融合检索片段。Next Action Loss 让状态直接学习下一正向互动，补充 CTR 监督；检索选不中的远期事件仍不可见，服务优化也需单独验证。 示意：候选是帐篷，旧露营浏览被检回，同时保留最近突然关注亲子出游的行为。辅助下一动作目标促使状态理解需求变化，而不只判断当前这次曝光是否点击。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-38858cbd67f8f10d">TransAct V2 为什么候选检索终身历史时仍保留一段原样近期行为，并增加 Next Action Loss？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atransact-v2">TransAct V2: Lifelong User Action Sequence Modeling on Pinterest Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相似度检索擅长找到与当前候选相关的旧事件，却可能遗漏刚形成但尚未显式相似的新意图。保留近期分支保证即时信号可见，再用共享 Transformer 融合检索片段。Next Action Loss 让状态直接学习下一正向互动，补充 CTR 监督；检索选不中的远期事件仍不可见，服务优化也需单独验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>候选是帐篷，旧露营浏览被检回，同时保留最近突然关注亲子出游的行为。辅助下一动作目标促使状态理解需求变化，而不只判断当前这次曝光是否点击。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2506.02267">原论文</a> · <a href="../../../../reproductions/2506.02267-transact-v2/">实现解读</a> · <a href="#qa-38858cbd67f8f10d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:transact-v2" data-paper-title="TransAct V2: Lifelong User Action Sequence Modeling on Pinterest Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TransAct V2: Lifelong User Action Sequence Modeling on Pinterest Recommendation 搜广推与 LLM 应用 Pinterest 2025-06-02 TransAct 主要建模约百条实时行为，容易忽略用户多年的长期兴趣。TransAct V2 从约条 lifelong 序列中按候选相似度取回相关行为，同时保留最近行为，再通过共享 Transformer 做 CTR 排序；额外的 Next Action Loss 迫使序列表征预测下一次正向互动。论文也包含 SKUT、request deduplication 等 serving 优化，本地复现聚焦模型链路。 保真度：核心机制复现。保真度：核心机制复现。候选锚定的长/短序列近邻检索、最近行为保留、early-fusion causal Transformer 和 Next Action Loss 均实际训练；MovieLens genre 替代 PinSage embedding，省略 Pinterest action/surface 字段、曝光日志负例及生产 Triton kernel。本地对照口径：基线是参数量匹配的 TransAct；实验组是 TransAct V2；NDCG@10 从 0.01277 升至 0.02460（+92.65%），head share 同时 +14.70pt。   搜广推 用户历史与排序骨干 强制recent保留与全历史纯top-k检索有什么不同？ 前者确保新近信号不会因相似度低被滤掉，其他部分再按候选检索；纯top-k可能遗漏新兴趣。更多保留也增加成本，效果取决于候选与数据。 例如用户刚转向新主题，旧相似度模型可能尚未把新行为排进top-k。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5693f8fb31713bda">强制recent保留与全历史纯top-k检索有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atransact-v2">TransAct V2: Lifelong User Action Sequence Modeling on Pinterest Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者确保新近信号不会因相似度低被滤掉，其他部分再按候选检索；纯top-k可能遗漏新兴趣。更多保留也增加成本，效果取决于候选与数据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户刚转向新主题，旧相似度模型可能尚未把新行为排进top-k。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2506.02267">原论文</a> · <a href="../../../../reproductions/2506.02267-transact-v2/">实现解读</a> · <a href="#qa-5693f8fb31713bda">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:transact-v2" data-paper-title="TransAct V2: Lifelong User Action Sequence Modeling on Pinterest Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TransAct V2: Lifelong User Action Sequence Modeling on Pinterest Recommendation 搜广推与 LLM 应用 Pinterest 2025-06-02 TransAct 主要建模约百条实时行为，容易忽略用户多年的长期兴趣。TransAct V2 从约条 lifelong 序列中按候选相似度取回相关行为，同时保留最近行为，再通过共享 Transformer 做 CTR 排序；额外的 Next Action Loss 迫使序列表征预测下一次正向互动。论文也包含 SKUT、request deduplication 等 serving 优化，本地复现聚焦模型链路。 保真度：核心机制复现。保真度：核心机制复现。候选锚定的长/短序列近邻检索、最近行为保留、early-fusion causal Transformer 和 Next Action Loss 均实际训练；MovieLens genre 替代 PinSage embedding，省略 Pinterest action/surface 字段、曝光日志负例及生产 Triton kernel。本地对照口径：基线是参数量匹配的 TransAct；实验组是 TransAct V2；NDCG@10 从 0.01277 升至 0.02460（+92.65%），head share 同时 +14.70pt。   搜广推 用户历史与排序骨干 Next Action Loss的标签可以进入当前序列输入吗？ 不可以，下一正向行为只作训练目标，当前表示只读过去；负样本也需合法。当前实现聚焦模型，未覆盖SKUT与request dedup等生产serving，不能由NAL通过推断系统吞吐。 例如预测下一次点击时若已把它拼进历史，会使辅助loss轻易作弊。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-10ca6a9f91815dd7">Next Action Loss的标签可以进入当前序列输入吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atransact-v2">TransAct V2: Lifelong User Action Sequence Modeling on Pinterest Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Pinterest</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不可以，下一正向行为只作训练目标，当前表示只读过去；负样本也需合法。当前实现聚焦模型，未覆盖SKUT与request dedup等生产serving，不能由NAL通过推断系统吞吐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如预测下一次点击时若已把它拼进历史，会使辅助loss轻易作弊。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2506.02267">原论文</a> · <a href="../../../../reproductions/2506.02267-transact-v2/">实现解读</a> · <a href="#qa-10ca6a9f91815dd7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:genrank" data-paper-title="Towards Large-scale Generative Ranking" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Towards Large-scale Generative Ranking 搜广推与 LLM 应用 Xiaohongshu 2025-05-07 HSTU 式排序把 item 与 action 交错为两倍长序列。GenRank 将 action 作为同一 item token 的监督/特征，并加入 position 与 time bias，在不丢掉多行为生成目标的前提下降低排序成本。 Fidelity: 完整核心链路复现。真实执行 item/action 交错基线、action-oriented 组织、位置/时间偏置、因果 Transformer 和 action 生成；缩小为 MovieLens 显式反馈。本地对照口径：基线是 item/action 交错序列模型；实验组是 GenRank action-oriented 组织；延迟 -25.66%，但 AUC -0.46%。这是序列组织的效率—效果对照，不是准确率提升，也不是相对 DIN。  generative-ranking action-modeling efficiency 搜广推 用户历史与排序骨干 GenRank 为什么把 action 和 item 放在同一位置而仍保留多行为学习？ 行动类型仍作为特征或监督参与预测，只是不再为每项单独再占一个序列位置，减少交错序列长度。位置与时间偏置补充时序信息。压缩的是表示组织，不意味着行为信息不重要；但是否完全保留原表达能力需实测，不能仅看长度推断。 示意：一次商品曝光与其点击反馈在同位置关联，不必展开成两个位置；模型仍要区分点击和跳过，而不是把两者都删成只有 item。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-genrank-a86f2304" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c377e9c8c77101ce">GenRank 为什么把 action 和 item 放在同一位置而仍保留多行为学习？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agenrank">Towards Large-scale Generative Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>行动类型仍作为特征或监督参与预测，只是不再为每项单独再占一个序列位置，减少交错序列长度。位置与时间偏置补充时序信息。压缩的是表示组织，不意味着行为信息不重要；但是否完全保留原表达能力需实测，不能仅看长度推断。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次商品曝光与其点击反馈在同位置关联，不必展开成两个位置；模型仍要区分点击和跳过，而不是把两者都删成只有 item。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.04180">原论文</a> · <a href="../../../../reproductions/2505.04180-genrank/">实现解读</a> · <a href="#qa-c377e9c8c77101ce">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:genrank" data-paper-title="Towards Large-scale Generative Ranking" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Towards Large-scale Generative Ranking 搜广推与 LLM 应用 Xiaohongshu 2025-05-07 HSTU 式排序把 item 与 action 交错为两倍长序列。GenRank 将 action 作为同一 item token 的监督/特征，并加入 position 与 time bias，在不丢掉多行为生成目标的前提下降低排序成本。 Fidelity: 完整核心链路复现。真实执行 item/action 交错基线、action-oriented 组织、位置/时间偏置、因果 Transformer 和 action 生成；缩小为 MovieLens 显式反馈。本地对照口径：基线是 item/action 交错序列模型；实验组是 GenRank action-oriented 组织；延迟 -25.66%，但 AUC -0.46%。这是序列组织的效率—效果对照，不是准确率提升，也不是相对 DIN。  generative-ranking action-modeling efficiency 搜广推 用户历史与排序骨干 GenRank把action并入item token，为什么能改变HSTU式排序的计算成本？ 交错item与action会增加序列位置，二次交互成本随长度显著增长。GenRank把同一行为的action作为item位置的特征或监督，保留多行为目标却减少独立token，并用位置与时间偏置补充结构。序列更短并不保证信息完全等价，本地效率改善同时伴随质量变化，需联合报告。 示意：十次行为原来对应二十个交错位置，合并后只保留十个item位置及其反馈信息；注意力矩阵变小，但仍要检验是否损失了某些反馈依赖。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-9b301295110c48a6">GenRank把action并入item token，为什么能改变HSTU式排序的计算成本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agenrank">Towards Large-scale Generative Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>交错item与action会增加序列位置，二次交互成本随长度显著增长。GenRank把同一行为的action作为item位置的特征或监督，保留多行为目标却减少独立token，并用位置与时间偏置补充结构。序列更短并不保证信息完全等价，本地效率改善同时伴随质量变化，需联合报告。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>十次行为原来对应二十个交错位置，合并后只保留十个item位置及其反馈信息；注意力矩阵变小，但仍要检验是否损失了某些反馈依赖。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.04180">原论文</a> · <a href="../../../../reproductions/2505.04180-genrank/">实现解读</a> · <a href="#qa-9b301295110c48a6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:genrank" data-paper-title="Towards Large-scale Generative Ranking" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Towards Large-scale Generative Ranking 搜广推与 LLM 应用 Xiaohongshu 2025-05-07 HSTU 式排序把 item 与 action 交错为两倍长序列。GenRank 将 action 作为同一 item token 的监督/特征，并加入 position 与 time bias，在不丢掉多行为生成目标的前提下降低排序成本。 Fidelity: 完整核心链路复现。真实执行 item/action 交错基线、action-oriented 组织、位置/时间偏置、因果 Transformer 和 action 生成；缩小为 MovieLens 显式反馈。本地对照口径：基线是 item/action 交错序列模型；实验组是 GenRank action-oriented 组织；延迟 -25.66%，但 AUC -0.46%。这是序列组织的效率—效果对照，不是准确率提升，也不是相对 DIN。  generative-ranking action-modeling efficiency 搜广推 用户历史与排序骨干 GenRank 与 item/action 交错排序，相比为何需要同时比较延迟和 AUC？ 序列缩短减少注意力位置，但行为进入方式改变可能损失某些交互表达，因此效率与质量需并列。来源本地延迟下降却 AUC 下降，只验证部分效率路径，不能写成精度持平或优于 HSTU。候选和硬件条件也影响延迟外推。 示意：把一百个事件从两百位置缩到一百位置可能更快，但错过行动顺序细节；只报速度会隐藏模型判断上的损失。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0c454283f597f484">GenRank 与 item/action 交错排序，相比为何需要同时比较延迟和 AUC？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agenrank">Towards Large-scale Generative Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>序列缩短减少注意力位置，但行为进入方式改变可能损失某些交互表达，因此效率与质量需并列。来源本地延迟下降却 AUC 下降，只验证部分效率路径，不能写成精度持平或优于 HSTU。候选和硬件条件也影响延迟外推。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把一百个事件从两百位置缩到一百位置可能更快，但错过行动顺序细节；只报速度会隐藏模型判断上的损失。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.04180">原论文</a> · <a href="../../../../reproductions/2505.04180-genrank/">实现解读</a> · <a href="#qa-0c454283f597f484">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:genrank" data-paper-title="Towards Large-scale Generative Ranking" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Towards Large-scale Generative Ranking 搜广推与 LLM 应用 Xiaohongshu 2025-05-07 HSTU 式排序把 item 与 action 交错为两倍长序列。GenRank 将 action 作为同一 item token 的监督/特征，并加入 position 与 time bias，在不丢掉多行为生成目标的前提下降低排序成本。 Fidelity: 完整核心链路复现。真实执行 item/action 交错基线、action-oriented 组织、位置/时间偏置、因果 Transformer 和 action 生成；缩小为 MovieLens 显式反馈。本地对照口径：基线是 item/action 交错序列模型；实验组是 GenRank action-oriented 组织；延迟 -25.66%，但 AUC -0.46%。这是序列组织的效率—效果对照，不是准确率提升，也不是相对 DIN。  generative-ranking action-modeling efficiency 搜广推 用户历史与排序骨干 GenRank 对当前待预测 action，为什么不能像已发生历史 action 一样输入？ 历史动作已可知，可与对应 item 编码；当前 action 是监督目标，若直接加入待预测位置就泄漏标签。需要清楚区分输入与输出字段及 causal mask，position/time bias 也只能用请求时可得信息。代码形状相同不能代替可见性检查。 示意：已点过的相机可带 click token，当前要猜是否点击的鞋不能预先带真实 click；否则 AUC 很高也只是读到了正确答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-4dcd00e7785d310d">GenRank 对当前待预测 action，为什么不能像已发生历史 action 一样输入？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Agenrank">Towards Large-scale Generative Ranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiaohongshu</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>历史动作已可知，可与对应 item 编码；当前 action 是监督目标，若直接加入待预测位置就泄漏标签。需要清楚区分输入与输出字段及 causal mask，position/time bias 也只能用请求时可得信息。代码形状相同不能代替可见性检查。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>已点过的相机可带 click token，当前要猜是否点击的鞋不能预先带真实 click；否则 AUC 很高也只是读到了正确答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.04180">原论文</a> · <a href="../../../../reproductions/2505.04180-genrank/">实现解读</a> · <a href="#qa-4dcd00e7785d310d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:longer" data-paper-title="LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders 搜广推与 LLM 应用 ByteDance / Douyin 2025-05-07 LONGER 先以 Token Merge 合并相邻行为，首层用少量 Query 读取长 K/V，后续沿短序列继续 self-attention。学习重点是区分合并输入和压缩查询这两步。 当前本地 encode 拼接 global/merged/recent 后做单层 self-attention，尚缺论文的首层短 Q/长 K/V hybrid attention 路径和 causal mask。历史实验不作为该核心路径或生产缓存的验证。 首层之后，模型还能否直接重新读取完整长 K/V？  搜广推 用户历史与排序骨干 LONGER 的 global token 为什么不应被理解为固定且候选无关的用户摘要？ global 是可汇聚全局信息的角色，可包含 CLS、用户及目标相关字段，是否公共取决于依赖。首层短查询读取长 K/V 后输出随查询长度传播，目标相关 global 仍会逐候选变化。不能因名称里有 global 就把所有状态共享。 示意：用户 ID token 可公共，商品价格形成的 global token 则属于当前候选；两者都能参与全局读取，却不能一概放入同一跨候选缓存。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-longer-50bd52b2" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5b0338092be4725e">LONGER 的 global token 为什么不应被理解为固定且候选无关的用户摘要？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alonger">LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>global 是可汇聚全局信息的角色，可包含 CLS、用户及目标相关字段，是否公共取决于依赖。首层短查询读取长 K/V 后输出随查询长度传播，目标相关 global 仍会逐候选变化。不能因名称里有 global 就把所有状态共享。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户 ID token 可公共，商品价格形成的 global token 则属于当前候选；两者都能参与全局读取，却不能一概放入同一跨候选缓存。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.04421">原论文</a> · <a href="../../../../reproductions/2505.04421-longer/">实现解读</a> · <a href="#qa-5b0338092be4725e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:longer" data-paper-title="LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders 搜广推与 LLM 应用 ByteDance / Douyin 2025-05-07 LONGER 先以 Token Merge 合并相邻行为，首层用少量 Query 读取长 K/V，后续沿短序列继续 self-attention。学习重点是区分合并输入和压缩查询这两步。 当前本地 encode 拼接 global/merged/recent 后做单层 self-attention，尚缺论文的首层短 Q/长 K/V hybrid attention 路径和 causal mask。历史实验不作为该核心路径或生产缓存的验证。 首层之后，模型还能否直接重新读取完整长 K/V？  搜广推 用户历史与排序骨干 LONGER把长历史留给K/V后，后续层还要重复更新整段历史吗？ 论文首层用global与近期token组成较短Q，读取合并后的长历史K/V；输出长度跟Q走，后续层只在这组短状态上做self-attention。压缩因此发生在层间传播状态，而非先完全截掉远期证据。本地同名实现尚未完整保留这条首层路径，历史指标不能证明它已被验证。 示意：长历史像一本资料册，首层让几张近期问题卡查阅全册；后续只反复整理这些问题卡，而不是每层重新改写整本资料册。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-b94e636f79ea884b">LONGER把长历史留给K/V后，后续层还要重复更新整段历史吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alonger">LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>论文首层用global与近期token组成较短Q，读取合并后的长历史K/V；输出长度跟Q走，后续层只在这组短状态上做self-attention。压缩因此发生在层间传播状态，而非先完全截掉远期证据。本地同名实现尚未完整保留这条首层路径，历史指标不能证明它已被验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>长历史像一本资料册，首层让几张近期问题卡查阅全册；后续只反复整理这些问题卡，而不是每层重新改写整本资料册。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.04421">原论文</a> · <a href="../../../../reproductions/2505.04421-longer/">实现解读</a> · <a href="#qa-b94e636f79ea884b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:longer" data-paper-title="LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders 搜广推与 LLM 应用 ByteDance / Douyin 2025-05-07 LONGER 先以 Token Merge 合并相邻行为，首层用少量 Query 读取长 K/V，后续沿短序列继续 self-attention。学习重点是区分合并输入和压缩查询这两步。 当前本地 encode 拼接 global/merged/recent 后做单层 self-attention，尚缺论文的首层短 Q/长 K/V hybrid attention 路径和 causal mask。历史实验不作为该核心路径或生产缓存的验证。 首层之后，模型还能否直接重新读取完整长 K/V？  搜广推 用户历史与排序骨干 LONGER 与先按候选取 Top-K 历史再精编，相比在哪一步压缩信息？ 两阶段检索先删未选事件，后续无法再读；LONGER 首层让短 query 访问合并后的长 K/V，再只传播短输出，保留更广一次取证机会。合并本身仍有信息取舍，不是原始全史完全无损。来源本地首层路径未完整保真，历史指标不能证明该区别已验证。 示意：Top-K 先把资料册撕到十页再读，LONGER 更像几张问题卡先翻阅较完整合并资料，再把答案卡交后层；合并资料也可能缺细节。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5e49e56233e457f1">LONGER 与先按候选取 Top-K 历史再精编，相比在哪一步压缩信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alonger">LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两阶段检索先删未选事件，后续无法再读；LONGER 首层让短 query 访问合并后的长 K/V，再只传播短输出，保留更广一次取证机会。合并本身仍有信息取舍，不是原始全史完全无损。来源本地首层路径未完整保真，历史指标不能证明该区别已验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>Top-K 先把资料册撕到十页再读，LONGER 更像几张问题卡先翻阅较完整合并资料，再把答案卡交后层；合并资料也可能缺细节。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.04421">原论文</a> · <a href="../../../../reproductions/2505.04421-longer/">实现解读</a> · <a href="#qa-5e49e56233e457f1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:longer" data-paper-title="LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders 搜广推与 LLM 应用 ByteDance / Douyin 2025-05-07 LONGER 先以 Token Merge 合并相邻行为，首层用少量 Query 读取长 K/V，后续沿短序列继续 self-attention。学习重点是区分合并输入和压缩查询这两步。 当前本地 encode 拼接 global/merged/recent 后做单层 self-attention，尚缺论文的首层短 Q/长 K/V hybrid attention 路径和 causal mask。历史实验不作为该核心路径或生产缓存的验证。 首层之后，模型还能否直接重新读取完整长 K/V？  搜广推 用户历史与排序骨干 LONGER 每 K 个 token 合并一次，为什么 K 更大不一定更省总 FLOPs？ 原文§3.4同时缩短序列并增宽合并表示：总 FLOPs 比例含随 K 增长的投影项和随 K 下降的注意力项。因此合并减少位置数，却会提高通道变换与参数成本，存在平衡点。InnerTrans 还用于补足组内交互；不能把这套设计等同于固定维度均值池化，也不能断言压缩越强效果越好。 示意：四条行为拼成一个更宽 token，位置更少但后续矩阵更大；再合并到八条可能让投影成本反弹。像减少箱子数量，却把每箱变得更大更难搬。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f90aa5aa39428720">LONGER 每 K 个 token 合并一次，为什么 K 更大不一定更省总 FLOPs？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alonger">LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原文§3.4同时缩短序列并增宽合并表示：总 FLOPs 比例含随 K 增长的投影项和随 K 下降的注意力项。因此合并减少位置数，却会提高通道变换与参数成本，存在平衡点。InnerTrans 还用于补足组内交互；不能把这套设计等同于固定维度均值池化，也不能断言压缩越强效果越好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>四条行为拼成一个更宽 token，位置更少但后续矩阵更大；再合并到八条可能让投影成本反弹。像减少箱子数量，却把每箱变得更大更难搬。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.04421">原论文</a> · <a href="../../../../reproductions/2505.04421-longer/">实现解读</a> · <a href="#qa-f90aa5aa39428720">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:longer" data-paper-title="LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders 搜广推与 LLM 应用 ByteDance / Douyin 2025-05-07 LONGER 先以 Token Merge 合并相邻行为，首层用少量 Query 读取长 K/V，后续沿短序列继续 self-attention。学习重点是区分合并输入和压缩查询这两步。 当前本地 encode 拼接 global/merged/recent 后做单层 self-attention，尚缺论文的首层短 Q/长 K/V hybrid attention 路径和 causal mask。历史实验不作为该核心路径或生产缓存的验证。 首层之后，模型还能否直接重新读取完整长 K/V？  搜广推 用户历史与排序骨干 LONGER 的 global token 可含候选信息，为什么仍能使用用户 KV cache？ 原文§3.5.2与§3.6.3用掩码确保用户序列不读取候选特有 global token，用户 K/V 才能先计算并跨候选复用。候选 global token 再与缓存历史交互，相关输出仍逐候选生成。global 代表可汇聚全局信息的角色，不代表所有 global token 都候选无关；缓存资格取决于实际依赖路径。 示意：两件商品共用用户浏览序列 K/V，但各有自己的候选 global token 查询历史。若先让用户序列吸收了商品甲信息，再给商品乙复用，就破坏了共享条件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-906a6ef0a4addaf4">LONGER 的 global token 可含候选信息，为什么仍能使用用户 KV cache？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alonger">LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原文§3.5.2与§3.6.3用掩码确保用户序列不读取候选特有 global token，用户 K/V 才能先计算并跨候选复用。候选 global token 再与缓存历史交互，相关输出仍逐候选生成。global 代表可汇聚全局信息的角色，不代表所有 global token 都候选无关；缓存资格取决于实际依赖路径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两件商品共用用户浏览序列 K/V，但各有自己的候选 global token 查询历史。若先让用户序列吸收了商品甲信息，再给商品乙复用，就破坏了共享条件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.04421">原论文</a> · <a href="../../../../reproductions/2505.04421-longer/">实现解读</a> · <a href="#qa-906a6ef0a4addaf4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:longer" data-paper-title="LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders 搜广推与 LLM 应用 ByteDance / Douyin 2025-05-07 LONGER 先以 Token Merge 合并相邻行为，首层用少量 Query 读取长 K/V，后续沿短序列继续 self-attention。学习重点是区分合并输入和压缩查询这两步。 当前本地 encode 拼接 global/merged/recent 后做单层 self-attention，尚缺论文的首层短 Q/长 K/V hybrid attention 路径和 causal mask。历史实验不作为该核心路径或生产缓存的验证。 首层之后，模型还能否直接重新读取完整长 K/V？  搜广推 用户历史与排序骨干 LONGER 代码验收为什么要同时检查第一层 Q 长度与后续层状态长度？ 定义性结构是首层 global/recent 短 Q 对长 K/V，输出长度随 Q，后层 self-attention 只接这份短状态。若把 merged、global、recent 全部拼接后每层自注意力，虽名字相同却是另一信息流。应先检查真实张量与掩码，再解释指标，不用旧 README 声称代替代码事实。 示意：长 K/V 五百位置、Q 一百位置，首层输出应一百；若第二层仍接六百多位置，就没有执行预期的短查询传播，成本结论也随之改变。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1fb09578a44894ee">LONGER 代码验收为什么要同时检查第一层 Q 长度与后续层状态长度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Alonger">LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>定义性结构是首层 global/recent 短 Q 对长 K/V，输出长度随 Q，后层 self-attention 只接这份短状态。若把 merged、global、recent 全部拼接后每层自注意力，虽名字相同却是另一信息流。应先检查真实张量与掩码，再解释指标，不用旧 README 声称代替代码事实。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>长 K/V 五百位置、Q 一百位置，首层输出应一百；若第二层仍接六百多位置，就没有执行预期的短查询传播，成本结论也随之改变。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2505.04421">原论文</a> · <a href="../../../../reproductions/2505.04421-longer/">实现解读</a> · <a href="#qa-1fb09578a44894ee">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:fuxi-alpha" data-paper-title="FuXi-α: Scaling Recommendation Model with Feature Interaction Enhanced Transformer" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="FuXi-α: Scaling Recommendation Model with Feature Interaction Enhanced Transformer 搜广推与 LLM 应用 Huawei / USTC 2025-02-05 常规推荐 Transformer 扩参时容易受浅层特征交互限制。FuXi-α 用多个自适应交互通道建模不同关系，再以 multi-stage FFN 逐级融合。 Fidelity: 核心机制复现。实际执行时间、语义和流行度多通道注意力及分阶段交互门控。本地是小型数值通道实现，不包含论文十亿级 scaling、华为音乐私有连续特征与分布式训练。本地对照口径：相对单通道注意力基线，实验组 NDCG@10 -4.25%。  ranking transformer feature-interaction scaling 搜广推 用户历史与排序骨干 FuXi-α 为什么认为特征交互通道需要分工？ 异构字段之间包含多种关系，单一交互空间可能只学到最强模式，扩宽未必让弱关系出现。多个自适应通道分别建模，再由多阶段 FFN 融合，让网络有机会保留不同结构。通道数量不是语义多样性的保证，仍可能学成重复表示。 示意：用户与商品匹配、场景与价格关系可走不同通道；如果三个通道最后都只看热门度，增加通道也没有得到互补知识。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-fuxi-alpha-d5540b18" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-bfdf2b6b061fc0a3">FuXi-α 为什么认为特征交互通道需要分工？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Afuxi-alpha">FuXi-α: Scaling Recommendation Model with Feature Interaction Enhanced Transformer</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei / USTC</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>异构字段之间包含多种关系，单一交互空间可能只学到最强模式，扩宽未必让弱关系出现。多个自适应通道分别建模，再由多阶段 FFN 融合，让网络有机会保留不同结构。通道数量不是语义多样性的保证，仍可能学成重复表示。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户与商品匹配、场景与价格关系可走不同通道；如果三个通道最后都只看热门度，增加通道也没有得到互补知识。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.03036">原论文</a> · <a href="../../../../reproductions/2502.03036-fuxi-alpha/">实现解读</a> · <a href="#qa-bfdf2b6b061fc0a3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:fuxi-alpha" data-paper-title="FuXi-α: Scaling Recommendation Model with Feature Interaction Enhanced Transformer" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="FuXi-α: Scaling Recommendation Model with Feature Interaction Enhanced Transformer 搜广推与 LLM 应用 Huawei / USTC 2025-02-05 常规推荐 Transformer 扩参时容易受浅层特征交互限制。FuXi-α 用多个自适应交互通道建模不同关系，再以 multi-stage FFN 逐级融合。 Fidelity: 核心机制复现。实际执行时间、语义和流行度多通道注意力及分阶段交互门控。本地是小型数值通道实现，不包含论文十亿级 scaling、华为音乐私有连续特征与分布式训练。本地对照口径：相对单通道注意力基线，实验组 NDCG@10 -4.25%。  ranking transformer feature-interaction scaling 搜广推 用户历史与排序骨干 FuXi-α为什么用多个交互通道和逐级FFN，而不是只把单路attention堆得更宽？ 单一路径可能把不同字段关系挤进同一表示，增加宽度未必改善交互组织。多个自适应通道先表达不同关系，multi-stage FFN再逐级融合，使参数扩展与特征交叉相配合。但通道数量增加也可能重复建模，不能因参数更多就宣布更有效，需与单通道及同预算配置比较。 示意：用户—商品、场景—商品、行为—候选的关系可先由不同通道捕获，再逐步组合；若所有通道都学成相同注意力，扩大它们只会增加成本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-034c54f6610a2785">FuXi-α为什么用多个交互通道和逐级FFN，而不是只把单路attention堆得更宽？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Afuxi-alpha">FuXi-α: Scaling Recommendation Model with Feature Interaction Enhanced Transformer</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei / USTC</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单一路径可能把不同字段关系挤进同一表示，增加宽度未必改善交互组织。多个自适应通道先表达不同关系，multi-stage FFN再逐级融合，使参数扩展与特征交叉相配合。但通道数量增加也可能重复建模，不能因参数更多就宣布更有效，需与单通道及同预算配置比较。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户—商品、场景—商品、行为—候选的关系可先由不同通道捕获，再逐步组合；若所有通道都学成相同注意力，扩大它们只会增加成本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.03036">原论文</a> · <a href="../../../../reproductions/2502.03036-fuxi-alpha/">实现解读</a> · <a href="#qa-034c54f6610a2785">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:fuxi-alpha" data-paper-title="FuXi-α: Scaling Recommendation Model with Feature Interaction Enhanced Transformer" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="FuXi-α: Scaling Recommendation Model with Feature Interaction Enhanced Transformer 搜广推与 LLM 应用 Huawei / USTC 2025-02-05 常规推荐 Transformer 扩参时容易受浅层特征交互限制。FuXi-α 用多个自适应交互通道建模不同关系，再以 multi-stage FFN 逐级融合。 Fidelity: 核心机制复现。实际执行时间、语义和流行度多通道注意力及分阶段交互门控。本地是小型数值通道实现，不包含论文十亿级 scaling、华为音乐私有连续特征与分布式训练。本地对照口径：相对单通道注意力基线，实验组 NDCG@10 -4.25%。  ranking transformer feature-interaction scaling 搜广推 用户历史与排序骨干 多阶段融合与把多路 attention 输出一次拼接到最终头，相比信息交换在哪发生？ 逐级 FFN 在中间层融合当前状态与各通道，再把结果传给后续层，关系可以继续组合；末端拼接只给最终头一次融合机会。前者增加深层容量与成本，不能从结构复杂推出效果更好，来源本地 NDCG 下降需保留。 示意：先形成“夜间场景”与“价格敏感”关系，再在后层组合为夜间优惠需求；末端拼接只能基于两路最终摘要做一次整合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-08ca36f70ea32158">多阶段融合与把多路 attention 输出一次拼接到最终头，相比信息交换在哪发生？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Afuxi-alpha">FuXi-α: Scaling Recommendation Model with Feature Interaction Enhanced Transformer</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei / USTC</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>逐级 FFN 在中间层融合当前状态与各通道，再把结果传给后续层，关系可以继续组合；末端拼接只给最终头一次融合机会。前者增加深层容量与成本，不能从结构复杂推出效果更好，来源本地 NDCG 下降需保留。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先形成“夜间场景”与“价格敏感”关系，再在后层组合为夜间优惠需求；末端拼接只能基于两路最终摘要做一次整合。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.03036">原论文</a> · <a href="../../../../reproductions/2502.03036-fuxi-alpha/">实现解读</a> · <a href="#qa-08ca36f70ea32158">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:fuxi-alpha" data-paper-title="FuXi-α: Scaling Recommendation Model with Feature Interaction Enhanced Transformer" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="FuXi-α: Scaling Recommendation Model with Feature Interaction Enhanced Transformer 搜广推与 LLM 应用 Huawei / USTC 2025-02-05 常规推荐 Transformer 扩参时容易受浅层特征交互限制。FuXi-α 用多个自适应交互通道建模不同关系，再以 multi-stage FFN 逐级融合。 Fidelity: 核心机制复现。实际执行时间、语义和流行度多通道注意力及分阶段交互门控。本地是小型数值通道实现，不包含论文十亿级 scaling、华为音乐私有连续特征与分布式训练。本地对照口径：相对单通道注意力基线，实验组 NDCG@10 -4.25%。  ranking transformer feature-interaction scaling 搜广推 用户历史与排序骨干 FuXi-α 递进残差融合时，通道输出需要满足什么形状与更新顺序？ 不同通道可有各自 Q/K/V，但拼接后经 FFN 必须映回主状态维度才能残差相加，层号和旧新状态应保持一致。通道权重训练需真实更新，不能用几份固定相似分拼接冒充自适应交互；本地对照仅针对实际实现预算。 示意：三个通道各输出 d 维，拼接连同主干变成多倍宽，FFN 需投回 d；直接把拼接结果与原向量相加虽想法相近，数学结构不成立。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-83eae398ef9dda36">FuXi-α 递进残差融合时，通道输出需要满足什么形状与更新顺序？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Afuxi-alpha">FuXi-α: Scaling Recommendation Model with Feature Interaction Enhanced Transformer</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei / USTC</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同通道可有各自 Q/K/V，但拼接后经 FFN 必须映回主状态维度才能残差相加，层号和旧新状态应保持一致。通道权重训练需真实更新，不能用几份固定相似分拼接冒充自适应交互；本地对照仅针对实际实现预算。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三个通道各输出 d 维，拼接连同主干变成多倍宽，FFN 需投回 d；直接把拼接结果与原向量相加虽想法相近，数学结构不成立。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.03036">原论文</a> · <a href="../../../../reproductions/2502.03036-fuxi-alpha/">实现解读</a> · <a href="#qa-83eae398ef9dda36">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:adaf2m2" data-paper-title="AdaF²M²: Comprehensive Learning and Responsive Leveraging Features in Recommendation System" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="AdaF²M²: Comprehensive Learning and Responsive Leveraging Features in Recommendation System 搜广推与 LLM 应用 ByteDance / Douyin 2025-01-27 单次全特征前向容易过度依赖强特征，且不同用户/物品状态需要不同特征。AdaF²M² 通过多种 mask 重复前向学习互补表示，再以 state-aware adapter 动态融合。 Fidelity: 核心机制复现。实际执行三组 feature-mask 前向、共享聚合与用户/物品状态自适应 adapter。状态仅由历史长度和物品热度构造；没有抖音私有特征、全链路联合训练和线上资源成本。本地对照口径：相对单前向全特征基线，实验组 NDCG@10 +2.42%。  ranking feature-masking state-aware-adapter multi-forward 搜广推 用户历史与排序骨干 AdaF²M² 中的 state-aware 融合为什么不是给所有样本固定使用同一套特征？ 不同用户活跃度和物品反馈量决定哪些信号可靠。多种 mask 产生互补表示，state-aware 权重再依据当前状态分配贡献，避免强特征在所有情形都占主导。状态是选择信息的条件，不能把一次融合权重理解为永久特征重要性。 示意：老用户历史丰富时重视行为分支，新用户只有内容线索时提高内容分支权重；两人的输入字段种类相同，也可得到不同融合比例。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-adaf2m2-4b0f92a1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0e7822ea0cb4f1b1">AdaF²M² 中的 state-aware 融合为什么不是给所有样本固定使用同一套特征？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aadaf2m2">AdaF²M²: Comprehensive Learning and Responsive Leveraging Features in Recommendation System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同用户活跃度和物品反馈量决定哪些信号可靠。多种 mask 产生互补表示，state-aware 权重再依据当前状态分配贡献，避免强特征在所有情形都占主导。状态是选择信息的条件，不能把一次融合权重理解为永久特征重要性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>老用户历史丰富时重视行为分支，新用户只有内容线索时提高内容分支权重；两人的输入字段种类相同，也可得到不同融合比例。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2501.15816">原论文</a> · <a href="../../../../reproductions/2501.15816-adaf2m2/">实现解读</a> · <a href="#qa-0e7822ea0cb4f1b1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:adaf2m2" data-paper-title="AdaF²M²: Comprehensive Learning and Responsive Leveraging Features in Recommendation System" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="AdaF²M²: Comprehensive Learning and Responsive Leveraging Features in Recommendation System 搜广推与 LLM 应用 ByteDance / Douyin 2025-01-27 单次全特征前向容易过度依赖强特征，且不同用户/物品状态需要不同特征。AdaF²M² 通过多种 mask 重复前向学习互补表示，再以 state-aware adapter 动态融合。 Fidelity: 核心机制复现。实际执行三组 feature-mask 前向、共享聚合与用户/物品状态自适应 adapter。状态仅由历史长度和物品热度构造；没有抖音私有特征、全链路联合训练和线上资源成本。本地对照口径：相对单前向全特征基线，实验组 NDCG@10 +2.42%。  ranking feature-masking state-aware-adapter multi-forward 搜广推 用户历史与排序骨干 AdaF²M²的多种mask前向，和只随机丢一次特征有什么区别？ 多路mask让模型在不同信号缺席时分别学习互补表示，而非只拿一次受扰结果训练。state-aware adapter再根据当前用户或物品状态分配各路权重，使强特征可用时利用它、脆弱时依赖其他路径。收益来自条件化融合，不能把多路简单平均视为同一机制。 示意：老商品可重用行为路，新商品更依赖内容路；同一次请求分别计算遮掉行为、遮掉内容的表示，再由状态决定组合比例。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c63df32fe423b84d">AdaF²M²的多种mask前向，和只随机丢一次特征有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aadaf2m2">AdaF²M²: Comprehensive Learning and Responsive Leveraging Features in Recommendation System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多路mask让模型在不同信号缺席时分别学习互补表示，而非只拿一次受扰结果训练。state-aware adapter再根据当前用户或物品状态分配各路权重，使强特征可用时利用它、脆弱时依赖其他路径。收益来自条件化融合，不能把多路简单平均视为同一机制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>老商品可重用行为路，新商品更依赖内容路；同一次请求分别计算遮掉行为、遮掉内容的表示，再由状态决定组合比例。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2501.15816">原论文</a> · <a href="../../../../reproductions/2501.15816-adaf2m2/">实现解读</a> · <a href="#qa-c63df32fe423b84d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:adaf2m2" data-paper-title="AdaF²M²: Comprehensive Learning and Responsive Leveraging Features in Recommendation System" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="AdaF²M²: Comprehensive Learning and Responsive Leveraging Features in Recommendation System 搜广推与 LLM 应用 ByteDance / Douyin 2025-01-27 单次全特征前向容易过度依赖强特征，且不同用户/物品状态需要不同特征。AdaF²M² 通过多种 mask 重复前向学习互补表示，再以 state-aware adapter 动态融合。 Fidelity: 核心机制复现。实际执行三组 feature-mask 前向、共享聚合与用户/物品状态自适应 adapter。状态仅由历史长度和物品热度构造；没有抖音私有特征、全链路联合训练和线上资源成本。本地对照口径：相对单前向全特征基线，实验组 NDCG@10 +2.42%。  ranking feature-masking state-aware-adapter multi-forward 搜广推 用户历史与排序骨干 AdaF²M² 的多前向融合与单模型特征 dropout，训练和服务目标有何不同？ 单次 dropout 主要迫使同一网络适应缺失输入，多前向则保留多种遮罩对应的表示，融合器学习它们在当前状态下的互补性。额外分支带来计算成本，不能只按参数量认为与一次前向等价；来源的局部比较也不证明任意部署预算下都更优。 示意：一次随机删掉价格只训练抗缺失；同时保留含价格与不含价格两种预测，再依商品状态融合，才是在使用两个视角作决策。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7d8fa2ddf0c300e8">AdaF²M² 的多前向融合与单模型特征 dropout，训练和服务目标有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aadaf2m2">AdaF²M²: Comprehensive Learning and Responsive Leveraging Features in Recommendation System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单次 dropout 主要迫使同一网络适应缺失输入，多前向则保留多种遮罩对应的表示，融合器学习它们在当前状态下的互补性。额外分支带来计算成本，不能只按参数量认为与一次前向等价；来源的局部比较也不证明任意部署预算下都更优。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次随机删掉价格只训练抗缺失；同时保留含价格与不含价格两种预测，再依商品状态融合，才是在使用两个视角作决策。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2501.15816">原论文</a> · <a href="../../../../reproductions/2501.15816-adaf2m2/">实现解读</a> · <a href="#qa-7d8fa2ddf0c300e8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:adaf2m2" data-paper-title="AdaF²M²: Comprehensive Learning and Responsive Leveraging Features in Recommendation System" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="AdaF²M²: Comprehensive Learning and Responsive Leveraging Features in Recommendation System 搜广推与 LLM 应用 ByteDance / Douyin 2025-01-27 单次全特征前向容易过度依赖强特征，且不同用户/物品状态需要不同特征。AdaF²M² 通过多种 mask 重复前向学习互补表示，再以 state-aware adapter 动态融合。 Fidelity: 核心机制复现。实际执行三组 feature-mask 前向、共享聚合与用户/物品状态自适应 adapter。状态仅由历史长度和物品热度构造；没有抖音私有特征、全链路联合训练和线上资源成本。本地对照口径：相对单前向全特征基线，实验组 NDCG@10 +2.42%。  ranking feature-masking state-aware-adapter multi-forward 搜广推 用户历史与排序骨干 实现 AdaF²M² 的融合时，softmax 应沿哪个维度计算？ 对同一样本的多个 mask 分支计算权重，softmax 沿分支维归一，使各分支表示按权重求和得到一个输出。批次中不同样本应各有自己的权重，不能把用户混在同一归一化轴；各分支输出维度也要一致才能相加。 示意：批内两位用户各有三份表示，应各生成三个和为一的权重，而不是把六个数一起归一，使一位用户的权重依赖另一位用户。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ae32381c26ab8834">实现 AdaF²M² 的融合时，softmax 应沿哪个维度计算？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Aadaf2m2">AdaF²M²: Comprehensive Learning and Responsive Leveraging Features in Recommendation System</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance / Douyin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>对同一样本的多个 mask 分支计算权重，softmax 沿分支维归一，使各分支表示按权重求和得到一个输出。批次中不同样本应各有自己的权重，不能把用户混在同一归一化轴；各分支输出维度也要一致才能相加。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>批内两位用户各有三份表示，应各生成三个和为一的权重，而不是把六个数一起归一，使一位用户的权重依赖另一位用户。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2501.15816">原论文</a> · <a href="../../../../reproductions/2501.15816-adaf2m2/">实现解读</a> · <a href="#qa-ae32381c26ab8834">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:twin-v2" data-paper-title="TWIN V2: Scaling Ultra-Long User Behavior Sequence Modeling for Enhanced CTR Prediction at Kuaishou" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TWIN V2: Scaling Ultra-Long User Behavior Sequence Modeling for Enhanced CTR Prediction at Kuaishou 搜广推与 LLM 应用 Kuaishou 2024-07-23 离线层次聚类将百万级生命周期行为压缩成带规模信息的虚拟物品；在线 GSU 检索相关簇，ESU 以 cluster-aware target attention 精排。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上执行论文的候选相关检索、层级压缩或蒸馏目标；未使用公司私有日志与线上 serving，线上 A/B 只引用原文。本地相对变化不得与原文指标混写。本地对照口径：基线为 shared transition + content baseline，实验组为 TWIN-V2，只改变论文核心机制；ndcg_at_10 0.0354 → 0.0433，相对基线 +22.45%。  ranking long-sequence training-serving 搜广推 用户历史与排序骨干 TWIN V2为什么用带规模的虚拟item压缩生命周期历史？ 百万行为逐项在线匹配太贵，离线层次簇概括相似历史并记录规模，在线候选检索相关簇再精排。簇大小影响代表意义，不是把所有行为无权平均。 例如用户多次类似行为形成一簇，需与仅一次偶然行为区分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-twin-v2-72f26bc8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9b5a1473f6d5e8e0">TWIN V2为什么用带规模的虚拟item压缩生命周期历史？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atwin-v2">TWIN V2: Scaling Ultra-Long User Behavior Sequence Modeling for Enhanced CTR Prediction at Kuaishou</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>百万行为逐项在线匹配太贵，离线层次簇概括相似历史并记录规模，在线候选检索相关簇再精排。簇大小影响代表意义，不是把所有行为无权平均。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户多次类似行为形成一簇，需与仅一次偶然行为区分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2407.16357">原论文</a> · <a href="../../../../reproductions/2407.16357-twin-v2/">实现解读</a> · <a href="#qa-9b5a1473f6d5e8e0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:twin-v2" data-paper-title="TWIN V2: Scaling Ultra-Long User Behavior Sequence Modeling for Enhanced CTR Prediction at Kuaishou" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TWIN V2: Scaling Ultra-Long User Behavior Sequence Modeling for Enhanced CTR Prediction at Kuaishou 搜广推与 LLM 应用 Kuaishou 2024-07-23 离线层次聚类将百万级生命周期行为压缩成带规模信息的虚拟物品；在线 GSU 检索相关簇，ESU 以 cluster-aware target attention 精排。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上执行论文的候选相关检索、层级压缩或蒸馏目标；未使用公司私有日志与线上 serving，线上 A/B 只引用原文。本地相对变化不得与原文指标混写。本地对照口径：基线为 shared transition + content baseline，实验组为 TWIN-V2，只改变论文核心机制；ndcg_at_10 0.0354 → 0.0433，相对基线 +22.45%。  ranking long-sequence training-serving 搜广推 用户历史与排序骨干 TWIN-V2 为什么把生命周期行为聚成带规模信息的虚拟物品，再做候选相关检索？ 极长历史无法逐事件在线精算，离线层级聚类先把重复或相似行为压成代表簇。在线 GSU 选择候选相关簇，ESU 再做 cluster-aware 交互，并考虑簇规模，避免把大簇仅因人数多而重复放大。压缩提高可服务性，却可能掩盖簇内稀有事件，不能把虚拟物品看作无损替代全部历史。 示意：用户多年里反复浏览相似跑鞋，可聚成一个带次数的虚拟物品。候选是越野鞋时检索相关簇，再利用规模信息，而不是把几千次近似浏览逐个计算注意力。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-646dc7ef8fc54339">TWIN-V2 为什么把生命周期行为聚成带规模信息的虚拟物品，再做候选相关检索？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atwin-v2">TWIN V2: Scaling Ultra-Long User Behavior Sequence Modeling for Enhanced CTR Prediction at Kuaishou</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>极长历史无法逐事件在线精算，离线层级聚类先把重复或相似行为压成代表簇。在线 GSU 选择候选相关簇，ESU 再做 cluster-aware 交互，并考虑簇规模，避免把大簇仅因人数多而重复放大。压缩提高可服务性，却可能掩盖簇内稀有事件，不能把虚拟物品看作无损替代全部历史。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户多年里反复浏览相似跑鞋，可聚成一个带次数的虚拟物品。候选是越野鞋时检索相关簇，再利用规模信息，而不是把几千次近似浏览逐个计算注意力。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2407.16357">原论文</a> · <a href="../../../../reproductions/2407.16357-twin-v2/">实现解读</a> · <a href="#qa-646dc7ef8fc54339">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:twin-v2" data-paper-title="TWIN V2: Scaling Ultra-Long User Behavior Sequence Modeling for Enhanced CTR Prediction at Kuaishou" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TWIN V2: Scaling Ultra-Long User Behavior Sequence Modeling for Enhanced CTR Prediction at Kuaishou 搜广推与 LLM 应用 Kuaishou 2024-07-23 离线层次聚类将百万级生命周期行为压缩成带规模信息的虚拟物品；在线 GSU 检索相关簇，ESU 以 cluster-aware target attention 精排。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上执行论文的候选相关检索、层级压缩或蒸馏目标；未使用公司私有日志与线上 serving，线上 A/B 只引用原文。本地相对变化不得与原文指标混写。本地对照口径：基线为 shared transition + content baseline，实验组为 TWIN-V2，只改变论文核心机制；ndcg_at_10 0.0354 → 0.0433，相对基线 +22.45%。  ranking long-sequence training-serving 搜广推 用户历史与排序骨干 簇检索与SIM直接检索原始行为有何区别？ 一个在压缩原型层筛选后还原或聚合细节，一个直接从行为选子序列；覆盖、精度与成本不同。聚类误差可能丢细节，不能只看支持更长历史就断言全面更准。 例如稀有兴趣被大簇合并后，原始行为检索或许仍能找到它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-041577c428d8fcae">簇检索与SIM直接检索原始行为有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atwin-v2">TWIN V2: Scaling Ultra-Long User Behavior Sequence Modeling for Enhanced CTR Prediction at Kuaishou</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一个在压缩原型层筛选后还原或聚合细节，一个直接从行为选子序列；覆盖、精度与成本不同。聚类误差可能丢细节，不能只看支持更长历史就断言全面更准。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如稀有兴趣被大簇合并后，原始行为检索或许仍能找到它。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2407.16357">原论文</a> · <a href="../../../../reproductions/2407.16357-twin-v2/">实现解读</a> · <a href="#qa-041577c428d8fcae">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:twin-v2" data-paper-title="TWIN V2: Scaling Ultra-Long User Behavior Sequence Modeling for Enhanced CTR Prediction at Kuaishou" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="TWIN V2: Scaling Ultra-Long User Behavior Sequence Modeling for Enhanced CTR Prediction at Kuaishou 搜广推与 LLM 应用 Kuaishou 2024-07-23 离线层次聚类将百万级生命周期行为压缩成带规模信息的虚拟物品；在线 GSU 检索相关簇，ESU 以 cluster-aware target attention 精排。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上执行论文的候选相关检索、层级压缩或蒸馏目标；未使用公司私有日志与线上 serving，线上 A/B 只引用原文。本地相对变化不得与原文指标混写。本地对照口径：基线为 shared transition + content baseline，实验组为 TWIN-V2，只改变论文核心机制；ndcg_at_10 0.0354 → 0.0433，相对基线 +22.45%。  ranking long-sequence training-serving 搜广推 用户历史与排序骨干 TWIN V2本地公开全库排序能证明百万行为服务吗？ 不能，当前只执行候选相关检索和层级压缩参考路径，没有私有全生命周期日志或serving。簇成员、规模与时间mask应一致，线上A/B仅作原文引用。 例如小MovieLens簇检索跑通，不代表生产百万条历史延迟已测。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d3fdc1036f68dd31">TWIN V2本地公开全库排序能证明百万行为服务吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Atwin-v2">TWIN V2: Scaling Ultra-Long User Behavior Sequence Modeling for Enhanced CTR Prediction at Kuaishou</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kuaishou</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，当前只执行候选相关检索和层级压缩参考路径，没有私有全生命周期日志或serving。簇成员、规模与时间mask应一致，线上A/B仅作原文引用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如小MovieLens簇检索跑通，不代表生产百万条历史延迟已测。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2407.16357">原论文</a> · <a href="../../../../reproductions/2407.16357-twin-v2/">实现解读</a> · <a href="#qa-d3fdc1036f68dd31">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hstu" data-paper-title="Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations 搜广推与 LLM 应用 Meta 2024-02-27 HSTU 在输入窗口内逐层更新历史 token，用因果交互建模行为之间的依赖。学习重点是把历史首算成本与 M-FALCON 缓存后的多候选增量成本分开。 保真度：核心机制复现。本地为核心层与 all-position 训练的缩小实现，未复刻异构 action/time、Stochastic Length 或 M-FALCON。MovieLens-100K 的三 seed 结果仅适用于匹配 SASRec 的本地协议，不能外推到工业系统。 有 M-FALCON 缓存后，哪些历史计算可以共享，哪些候选路径仍要重算？  搜广推 用户历史与排序骨干 HSTU 的历史 token 之间会不会交互，和只让候选读取一份静态历史向量有什么差别？ 会。HSTU 在有效输入窗口内逐层更新 token 状态，每个位置可聚合此前可见历史；较晚行为因而能结合更早上下文形成新表示。排序时目标 token 再读取这些状态，保留目标相关交互。因果掩码限制的是可见方向，不是禁止历史之间建模；窗口外未输入的事件也不会自动进入计算。 示意：先浏览相机再看镜头，镜头位置的状态可结合相机背景；候选三脚架读取的是这类已带上下文的历史状态，而不只是互不交流的原始物品向量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-hstu-2703dd1e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6d826e4c63d0f978">HSTU 的历史 token 之间会不会交互，和只让候选读取一份静态历史向量有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahstu">Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>会。HSTU 在有效输入窗口内逐层更新 token 状态，每个位置可聚合此前可见历史；较晚行为因而能结合更早上下文形成新表示。排序时目标 token 再读取这些状态，保留目标相关交互。因果掩码限制的是可见方向，不是禁止历史之间建模；窗口外未输入的事件也不会自动进入计算。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先浏览相机再看镜头，镜头位置的状态可结合相机背景；候选三脚架读取的是这类已带上下文的历史状态，而不只是互不交流的原始物品向量。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2402.17152">原论文</a> · <a href="../../../../reproductions/2402.17152-hstu/">实现解读</a> · <a href="#qa-6d826e4c63d0f978">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hstu" data-paper-title="Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations 搜广推与 LLM 应用 Meta 2024-02-27 HSTU 在输入窗口内逐层更新历史 token，用因果交互建模行为之间的依赖。学习重点是把历史首算成本与 M-FALCON 缓存后的多候选增量成本分开。 保真度：核心机制复现。本地为核心层与 all-position 训练的缩小实现，未复刻异构 action/time、Stochastic Length 或 M-FALCON。MovieLens-100K 的三 seed 结果仅适用于匹配 SASRec 的本地协议，不能外推到工业系统。 有 M-FALCON 缓存后，哪些历史计算可以共享，哪些候选路径仍要重算？  搜广推 用户历史与排序骨干 HSTU 在 ranking 与 retrieval 中预测的对象为什么不同？ 检索预测下一相关物品，排序则需要给定目标后预测动作；原文将 item 与 action 交错，使候选能及早读取历史并输出反馈概率。两者可共用 transduction 思想，却不能把 next-item 全库指标当作完整多任务 ranking 验证。 示意：先猜用户会看哪部电影是检索，已给电影后猜点击或长看是排序；后一任务需要候选参与，不能只缓存一个最终物品分布便完成。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-defbb4068319dd08">HSTU 在 ranking 与 retrieval 中预测的对象为什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahstu">Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>检索预测下一相关物品，排序则需要给定目标后预测动作；原文将 item 与 action 交错，使候选能及早读取历史并输出反馈概率。两者可共用 transduction 思想，却不能把 next-item 全库指标当作完整多任务 ranking 验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先猜用户会看哪部电影是检索，已给电影后猜点击或长看是排序；后一任务需要候选参与，不能只缓存一个最终物品分布便完成。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2402.17152">原论文</a> · <a href="../../../../reproductions/2402.17152-hstu/">实现解读</a> · <a href="#qa-defbb4068319dd08">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hstu" data-paper-title="Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations 搜广推与 LLM 应用 Meta 2024-02-27 HSTU 在输入窗口内逐层更新历史 token，用因果交互建模行为之间的依赖。学习重点是把历史首算成本与 M-FALCON 缓存后的多候选增量成本分开。 保真度：核心机制复现。本地为核心层与 all-position 训练的缩小实现，未复刻异构 action/time、Stochastic Length 或 M-FALCON。MovieLens-100K 的三 seed 结果仅适用于匹配 SASRec 的本地协议，不能外推到工业系统。 有 M-FALCON 缓存后，哪些历史计算可以共享，哪些候选路径仍要重算？  搜广推 用户历史与排序骨干 HSTU为什么去掉softmax，却还要在聚合后归一化并加U-gate？ softmax把历史权重归一成总和固定的分布，容易弱化相关行为数量携带的偏好强度。HSTU用逐点SiLU聚合保留这种变化，再靠聚合后归一化稳定数值；U分支按当前token调制聚合结果。它仍在输入窗口内做因果历史交互，并没有因此变成线性复杂度模型。 示意：两位用户分别出现一次和十次同类行为，归一化平均可能看起来相似；逐点聚合允许区分强度，再由门控决定向下一层传多少信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-d1b7f594100aaa20">HSTU为什么去掉softmax，却还要在聚合后归一化并加U-gate？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahstu">Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>softmax把历史权重归一成总和固定的分布，容易弱化相关行为数量携带的偏好强度。HSTU用逐点SiLU聚合保留这种变化，再靠聚合后归一化稳定数值；U分支按当前token调制聚合结果。它仍在输入窗口内做因果历史交互，并没有因此变成线性复杂度模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两位用户分别出现一次和十次同类行为，归一化平均可能看起来相似；逐点聚合允许区分强度，再由门控决定向下一层传多少信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2402.17152">原论文</a> · <a href="../../../../reproductions/2402.17152-hstu/">实现解读</a> · <a href="#qa-d1b7f594100aaa20">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hstu" data-paper-title="Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations 搜广推与 LLM 应用 Meta 2024-02-27 HSTU 在输入窗口内逐层更新历史 token，用因果交互建模行为之间的依赖。学习重点是把历史首算成本与 M-FALCON 缓存后的多候选增量成本分开。 保真度：核心机制复现。本地为核心层与 all-position 训练的缩小实现，未复刻异构 action/time、Stochastic Length 或 M-FALCON。MovieLens-100K 的三 seed 结果仅适用于匹配 SASRec 的本地协议，不能外推到工业系统。 有 M-FALCON 缓存后，哪些历史计算可以共享，哪些候选路径仍要重算？  搜广推 用户历史与排序骨干 HSTU 与匹配预算 SASRec 的本地负结果，为什么不能解释为工业场景的最终优劣？ 同维度、层数、损失和步数的对照能比较本地 core，但 MovieLens 只有单类评分事件和较短序列，缺少原文异构动作、时间与工业规模。负结果应保留，也不能据它否定论文生产证据；相反生产收益也不能覆盖本地退化。 示意：在短电影序列上 HSTU 不如匹配 SASRec，说明这个预算与数据下未见收益；不能因此断言十万动作排序一定失败，或反用线上数值假装本地成功。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-3b88d0c3b149bbc6">HSTU 与匹配预算 SASRec 的本地负结果，为什么不能解释为工业场景的最终优劣？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahstu">Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同维度、层数、损失和步数的对照能比较本地 core，但 MovieLens 只有单类评分事件和较短序列，缺少原文异构动作、时间与工业规模。负结果应保留，也不能据它否定论文生产证据；相反生产收益也不能覆盖本地退化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>在短电影序列上 HSTU 不如匹配 SASRec，说明这个预算与数据下未见收益；不能因此断言十万动作排序一定失败，或反用线上数值假装本地成功。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2402.17152">原论文</a> · <a href="../../../../reproductions/2402.17152-hstu/">实现解读</a> · <a href="#qa-3b88d0c3b149bbc6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hstu" data-paper-title="Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations 搜广推与 LLM 应用 Meta 2024-02-27 HSTU 在输入窗口内逐层更新历史 token，用因果交互建模行为之间的依赖。学习重点是把历史首算成本与 M-FALCON 缓存后的多候选增量成本分开。 保真度：核心机制复现。本地为核心层与 all-position 训练的缩小实现，未复刻异构 action/time、Stochastic Length 或 M-FALCON。MovieLens-100K 的三 seed 结果仅适用于匹配 SASRec 的本地协议，不能外推到工业系统。 有 M-FALCON 缓存后，哪些历史计算可以共享，哪些候选路径仍要重算？  搜广推 用户历史与排序骨干 M-FALCON 缓存了哪些用户计算，为什么不能把整个 ranking 分数缓存给所有候选？ 原文§3.4与附录H把候选放入隔离的微批，复用各层候选无关历史 K/V；候选之间不互读，各自仍计算投影、目标到历史的交互和输出。缓存摊销历史编码，并未取消目标依赖。跨请求复用还要求历史、特征与模型版本等条件适用；本地 HSTU 没有实现该服务优化。 示意：一千个候选可分批读取同一份历史记忆，但相机和跑鞋各自的查询与分数仍不同。历史新增购买或模型更新后，也不能直接沿用旧缓存假装用户状态未变。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a6dfb7484be36691">M-FALCON 缓存了哪些用户计算，为什么不能把整个 ranking 分数缓存给所有候选？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahstu">Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原文§3.4与附录H把候选放入隔离的微批，复用各层候选无关历史 K/V；候选之间不互读，各自仍计算投影、目标到历史的交互和输出。缓存摊销历史编码，并未取消目标依赖。跨请求复用还要求历史、特征与模型版本等条件适用；本地 HSTU 没有实现该服务优化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一千个候选可分批读取同一份历史记忆，但相机和跑鞋各自的查询与分数仍不同。历史新增购买或模型更新后，也不能直接沿用旧缓存假装用户状态未变。</p>
<p class="ar-learning-sources">依据：背景与主要改动、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2402.17152">原论文</a> · <a href="../../../../reproductions/2402.17152-hstu/">实现解读</a> · <a href="#qa-a6dfb7484be36691">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:hstu" data-paper-title="Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations 搜广推与 LLM 应用 Meta 2024-02-27 HSTU 在输入窗口内逐层更新历史 token，用因果交互建模行为之间的依赖。学习重点是把历史首算成本与 M-FALCON 缓存后的多候选增量成本分开。 保真度：核心机制复现。本地为核心层与 all-position 训练的缩小实现，未复刻异构 action/time、Stochastic Length 或 M-FALCON。MovieLens-100K 的三 seed 结果仅适用于匹配 SASRec 的本地协议，不能外推到工业系统。 有 M-FALCON 缓存后，哪些历史计算可以共享，哪些候选路径仍要重算？  搜广推 用户历史与排序骨干 HSTU 的 all-position 训练如何同时利用多个目标又保持因果性？ 每个有效位置只读取其可见前缀，下一物品作监督，padding 与无效目标不进入 loss；这样一次编码服务多个位置目标而非逐条重算历史。候选 ranking 的动作交错是另一输入契约，本地 next-item 路径不能自动声称已实现所有异构动作任务。 示意：序列甲乙丙可在甲位置预测乙、乙位置预测丙，但甲状态不能读取乙丙；若整条无掩码先编码再预测，多目标训练会泄漏答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e74368e779e676f8">HSTU 的 all-position 训练如何同时利用多个目标又保持因果性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Ahstu">Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每个有效位置只读取其可见前缀，下一物品作监督，padding 与无效目标不进入 loss；这样一次编码服务多个位置目标而非逐条重算历史。候选 ranking 的动作交错是另一输入契约，本地 next-item 路径不能自动声称已实现所有异构动作任务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>序列甲乙丙可在甲位置预测乙、乙位置预测丙，但甲状态不能读取乙丙；若整条无掩码先编码再预测，多目标训练会泄漏答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2402.17152">原论文</a> · <a href="../../../../reproductions/2402.17152-hstu/">实现解读</a> · <a href="#qa-e74368e779e676f8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dcn-v2" data-paper-title="DCN V2: Improved Deep &amp; Cross Network and Practical Lessons for Web-scale Learning to Rank Systems" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="DCN V2: Improved Deep &amp; Cross Network and Practical Lessons for Web-scale Learning to Rank Systems 搜广推与 LLM 应用 Google 2020-08-19 DCN-V2 显式构造有界阶数的特征交互，并用低秩矩阵与专家混合降低 web-scale ranking 的参数和计算成本。 Fidelity: 核心机制复现。实现低秩 cross experts、输入相关 gate 与 deep tower。未使用 Google 私有数据和生产级专家规模；结果只验证显式交叉在公开数据上的作用。本地对照口径：基线是 deep-only；实验组是两层低秩 cross experts 与 gate；三 seed NDCG@10 相对 +22.87%。  ranking classic feature-interaction 搜广推 用户历史与排序骨干 DCN-V2 的显式交叉为什么说阶数受层数控制？ 每层把原输入与当前线性变换逐元素相乘，逐层形成更高阶组合，再以残差保留已有阶数。它提供结构可追踪的多项式交互路径，不同于只靠一般 MLP 隐式拟合关系；但实际表达还受矩阵秩、宽度和训练约束。 示意：第一层可产生用户年龄与品类组合，下一层继续乘原特征形成更高阶条件；残差使低阶信号不必在加深后消失。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-dcn-v2-7ac56e9e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-31f19cb8fdc20457">DCN-V2 的显式交叉为什么说阶数受层数控制？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adcn-v2">DCN V2: Improved Deep &amp; Cross Network and Practical Lessons for Web-scale Learning to Rank Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每层把原输入与当前线性变换逐元素相乘，逐层形成更高阶组合，再以残差保留已有阶数。它提供结构可追踪的多项式交互路径，不同于只靠一般 MLP 隐式拟合关系；但实际表达还受矩阵秩、宽度和训练约束。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第一层可产生用户年龄与品类组合，下一层继续乘原特征形成更高阶条件；残差使低阶信号不必在加深后消失。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2008.13535">原论文</a> · <a href="../../../../reproductions/2008.13535-dcn-v2/">实现解读</a> · <a href="#qa-31f19cb8fdc20457">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dcn-v2" data-paper-title="DCN V2: Improved Deep &amp; Cross Network and Practical Lessons for Web-scale Learning to Rank Systems" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="DCN V2: Improved Deep &amp; Cross Network and Practical Lessons for Web-scale Learning to Rank Systems 搜广推与 LLM 应用 Google 2020-08-19 DCN-V2 显式构造有界阶数的特征交互，并用低秩矩阵与专家混合降低 web-scale ranking 的参数和计算成本。 Fidelity: 核心机制复现。实现低秩 cross experts、输入相关 gate 与 deep tower。未使用 Google 私有数据和生产级专家规模；结果只验证显式交叉在公开数据上的作用。本地对照口径：基线是 deep-only；实验组是两层低秩 cross experts 与 gate；三 seed NDCG@10 相对 +22.87%。  ranking classic feature-interaction 搜广推 用户历史与排序骨干 DCN-V2为什么每一层都把原始输入x₀乘回当前交叉变换？ 原始输入作为锚点反复进入，使层数增加时产生可解释的更高阶特征组合，而非完全依赖普通MLP隐式拟合。矩阵形式能表达更丰富交叉，低秩分解与专家门控再控制参数与计算成本。低秩是容量约束和效率选择，不保证任意压缩都保持同样表达力，需与深层路径共同检验。 示意：第一层可组合用户与品类，下一层仍乘原始场景字段，就能形成用户—品类—时段交叉；低秩专家限制的是这些组合如何共享参数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-a5fba110bcfcd1e9">DCN-V2为什么每一层都把原始输入x₀乘回当前交叉变换？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adcn-v2">DCN V2: Improved Deep &amp; Cross Network and Practical Lessons for Web-scale Learning to Rank Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原始输入作为锚点反复进入，使层数增加时产生可解释的更高阶特征组合，而非完全依赖普通MLP隐式拟合。矩阵形式能表达更丰富交叉，低秩分解与专家门控再控制参数与计算成本。低秩是容量约束和效率选择，不保证任意压缩都保持同样表达力，需与深层路径共同检验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第一层可组合用户与品类，下一层仍乘原始场景字段，就能形成用户—品类—时段交叉；低秩专家限制的是这些组合如何共享参数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2008.13535">原论文</a> · <a href="../../../../reproductions/2008.13535-dcn-v2/">实现解读</a> · <a href="#qa-a5fba110bcfcd1e9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dcn-v2" data-paper-title="DCN V2: Improved Deep &amp; Cross Network and Practical Lessons for Web-scale Learning to Rank Systems" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="DCN V2: Improved Deep &amp; Cross Network and Practical Lessons for Web-scale Learning to Rank Systems 搜广推与 LLM 应用 Google 2020-08-19 DCN-V2 显式构造有界阶数的特征交互，并用低秩矩阵与专家混合降低 web-scale ranking 的参数和计算成本。 Fidelity: 核心机制复现。实现低秩 cross experts、输入相关 gate 与 deep tower。未使用 Google 私有数据和生产级专家规模；结果只验证显式交叉在公开数据上的作用。本地对照口径：基线是 deep-only；实验组是两层低秩 cross experts 与 gate；三 seed NDCG@10 相对 +22.87%。  ranking classic feature-interaction 搜广推 用户历史与排序骨干 DCN-V2 的低秩专家混合与一张完整 cross 矩阵，有什么容量—计算取舍？ 低秩 U、V 将昂贵矩阵分解到较小子空间，多个专家和 gate 提供输入相关组合，增加表达灵活性。单专家低秩限制可表示方向，多专家则增加存储与路由成本。不能把参数省下比例直接当作端到端延迟比例，embedding 和其他模块仍占成本。 示意：一张上千维矩阵可先投到几十维再映回，专家分别学习不同交叉；省计算的同时，过低秩可能遗漏稀有但重要的字段关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-46f4f5f89cf26086">DCN-V2 的低秩专家混合与一张完整 cross 矩阵，有什么容量—计算取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adcn-v2">DCN V2: Improved Deep &amp; Cross Network and Practical Lessons for Web-scale Learning to Rank Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>低秩 U、V 将昂贵矩阵分解到较小子空间，多个专家和 gate 提供输入相关组合，增加表达灵活性。单专家低秩限制可表示方向，多专家则增加存储与路由成本。不能把参数省下比例直接当作端到端延迟比例，embedding 和其他模块仍占成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一张上千维矩阵可先投到几十维再映回，专家分别学习不同交叉；省计算的同时，过低秩可能遗漏稀有但重要的字段关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2008.13535">原论文</a> · <a href="../../../../reproductions/2008.13535-dcn-v2/">实现解读</a> · <a href="#qa-46f4f5f89cf26086">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dcn-v2" data-paper-title="DCN V2: Improved Deep &amp; Cross Network and Practical Lessons for Web-scale Learning to Rank Systems" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="DCN V2: Improved Deep &amp; Cross Network and Practical Lessons for Web-scale Learning to Rank Systems 搜广推与 LLM 应用 Google 2020-08-19 DCN-V2 显式构造有界阶数的特征交互，并用低秩矩阵与专家混合降低 web-scale ranking 的参数和计算成本。 Fidelity: 核心机制复现。实现低秩 cross experts、输入相关 gate 与 deep tower。未使用 Google 私有数据和生产级专家规模；结果只验证显式交叉在公开数据上的作用。本地对照口径：基线是 deep-only；实验组是两层低秩 cross experts 与 gate；三 seed NDCG@10 相对 +22.87%。  ranking classic feature-interaction 搜广推 用户历史与排序骨干 DCN-V2 实现时 x0 与 xl 分别应来自哪一层？ x0 始终是该 cross stack 的原始输入，xl 是当前层状态，不能每层把 x0 替换为 xl，否则改变交叉定义。各专家低秩输出需映回原维度再与 x0 相乘，gate 也要按专家轴归一。残差维度一致只是必要条件，不能替代算子核验。 示意：第二层仍乘最初的用户与商品向量，而不是拿上一层状态平方；两种写法形状相同，却产生不同阶次和不同信息路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-80771f1fac3afa44">DCN-V2 实现时 x0 与 xl 分别应来自哪一层？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adcn-v2">DCN V2: Improved Deep &amp; Cross Network and Practical Lessons for Web-scale Learning to Rank Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>x0 始终是该 cross stack 的原始输入，xl 是当前层状态，不能每层把 x0 替换为 xl，否则改变交叉定义。各专家低秩输出需映回原维度再与 x0 相乘，gate 也要按专家轴归一。残差维度一致只是必要条件，不能替代算子核验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第二层仍乘最初的用户与商品向量，而不是拿上一层状态平方；两种写法形状相同，却产生不同阶次和不同信息路径。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2008.13535">原论文</a> · <a href="../../../../reproductions/2008.13535-dcn-v2/">实现解读</a> · <a href="#qa-80771f1fac3afa44">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sim" data-paper-title="Search-based User Interest Modeling with Lifelong Sequential Behavior Data for CTR Prediction" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Search-based User Interest Modeling with Lifelong Sequential Behavior Data for CTR Prediction 搜广推与 LLM 应用 Alibaba 2020-06-10 以候选 item 为 query，GSU 从终身行为中快速搜索相关子序列，ESU 再计算候选与子序列的精确注意力。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上执行论文的候选相关检索、层级压缩或蒸馏目标；未使用公司私有日志与线上 serving，线上 A/B 只引用原文。本地相对变化不得与原文指标混写。本地对照口径：基线为 shared transition + content baseline，实验组为 SIM，只改变论文核心机制；ndcg_at_10 0.0354 → 0.0471，相对基线 +32.97%。  ranking long-sequence training-serving 搜广推 用户历史与排序骨干 SIM为什么先用GSU搜索再用ESU注意？ 终身历史过长，候选相关快速检索先缩小子序列，再做较精细匹配，分开覆盖成本与交互精度。它不是固定保留最近几项。 例如候选是相机，可从多年行为先找摄影相关片段。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-sim-df73a28d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-3e6a146e9f258a78">SIM为什么先用GSU搜索再用ESU注意？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asim">Search-based User Interest Modeling with Lifelong Sequential Behavior Data for CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>终身历史过长，候选相关快速检索先缩小子序列，再做较精细匹配，分开覆盖成本与交互精度。它不是固定保留最近几项。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如候选是相机，可从多年行为先找摄影相关片段。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2006.05639">原论文</a> · <a href="../../../../reproductions/2006.05639-sim/">实现解读</a> · <a href="#qa-3e6a146e9f258a78">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sim" data-paper-title="Search-based User Interest Modeling with Lifelong Sequential Behavior Data for CTR Prediction" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Search-based User Interest Modeling with Lifelong Sequential Behavior Data for CTR Prediction 搜广推与 LLM 应用 Alibaba 2020-06-10 以候选 item 为 query，GSU 从终身行为中快速搜索相关子序列，ESU 再计算候选与子序列的精确注意力。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上执行论文的候选相关检索、层级压缩或蒸馏目标；未使用公司私有日志与线上 serving，线上 A/B 只引用原文。本地相对变化不得与原文指标混写。本地对照口径：基线为 shared transition + content baseline，实验组为 SIM，只改变论文核心机制；ndcg_at_10 0.0354 → 0.0471，相对基线 +32.97%。  ranking long-sequence training-serving 搜广推 用户历史与排序骨干 SIM 为什么先用 GSU 搜相关历史，再由 ESU 做精细注意力，而不是对终身历史直接打分？ 候选相关的终身历史通常只占少数，对全部事件做精确交互成本高且噪声大。GSU 用较便宜的匹配选出子序列，ESU 再在这份候选相关证据上做精细注意力，把计算集中到可能有用的行为。两阶段的瓶颈是粗搜召回率：GSU 漏掉的关键事件，ESU 无法从不存在的输入中补回来。 示意：候选是相机时，先从多年历史中找摄影相关浏览，再比较具体品牌与用途。若粗搜只按错误类别过滤掉镜头历史，后面的精细注意力再强也读不到它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-ff2b1a817c0aa800">SIM 为什么先用 GSU 搜相关历史，再由 ESU 做精细注意力，而不是对终身历史直接打分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asim">Search-based User Interest Modeling with Lifelong Sequential Behavior Data for CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>候选相关的终身历史通常只占少数，对全部事件做精确交互成本高且噪声大。GSU 用较便宜的匹配选出子序列，ESU 再在这份候选相关证据上做精细注意力，把计算集中到可能有用的行为。两阶段的瓶颈是粗搜召回率：GSU 漏掉的关键事件，ESU 无法从不存在的输入中补回来。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>候选是相机时，先从多年历史中找摄影相关浏览，再比较具体品牌与用途。若粗搜只按错误类别过滤掉镜头历史，后面的精细注意力再强也读不到它。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2006.05639">原论文</a> · <a href="../../../../reproductions/2006.05639-sim/">实现解读</a> · <a href="#qa-ff2b1a817c0aa800">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sim" data-paper-title="Search-based User Interest Modeling with Lifelong Sequential Behavior Data for CTR Prediction" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Search-based User Interest Modeling with Lifelong Sequential Behavior Data for CTR Prediction 搜广推与 LLM 应用 Alibaba 2020-06-10 以候选 item 为 query，GSU 从终身行为中快速搜索相关子序列，ESU 再计算候选与子序列的精确注意力。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上执行论文的候选相关检索、层级压缩或蒸馏目标；未使用公司私有日志与线上 serving，线上 A/B 只引用原文。本地相对变化不得与原文指标混写。本地对照口径：基线为 shared transition + content baseline，实验组为 SIM，只改变论文核心机制；ndcg_at_10 0.0354 → 0.0471，相对基线 +32.97%。  ranking long-sequence training-serving 搜广推 用户历史与排序骨干 SIM候选相关选择与统一用户向量有什么差别？ 同用户面对不同候选检索不同证据，统一向量则把历史压成一份共享表示。前者增加候选依赖计算，后者利于缓存，不能单凭结构判断精度与成本优劣。 例如运动鞋与书籍可触发同一用户的不同历史兴趣。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e023b625f1151b67">SIM候选相关选择与统一用户向量有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asim">Search-based User Interest Modeling with Lifelong Sequential Behavior Data for CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同用户面对不同候选检索不同证据，统一向量则把历史压成一份共享表示。前者增加候选依赖计算，后者利于缓存，不能单凭结构判断精度与成本优劣。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如运动鞋与书籍可触发同一用户的不同历史兴趣。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2006.05639">原论文</a> · <a href="../../../../reproductions/2006.05639-sim/">实现解读</a> · <a href="#qa-e023b625f1151b67">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sim" data-paper-title="Search-based User Interest Modeling with Lifelong Sequential Behavior Data for CTR Prediction" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Search-based User Interest Modeling with Lifelong Sequential Behavior Data for CTR Prediction 搜广推与 LLM 应用 Alibaba 2020-06-10 以候选 item 为 query，GSU 从终身行为中快速搜索相关子序列，ESU 再计算候选与子序列的精确注意力。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上执行论文的候选相关检索、层级压缩或蒸馏目标；未使用公司私有日志与线上 serving，线上 A/B 只引用原文。本地相对变化不得与原文指标混写。本地对照口径：基线为 shared transition + content baseline，实验组为 SIM，只改变论文核心机制；ndcg_at_10 0.0354 → 0.0471，相对基线 +32.97%。  ranking long-sequence training-serving 搜广推 用户历史与排序骨干 SIM top-k子序列需要怎样避免未来行为泄漏？ 检索只从当前请求前可见历史，候选query与目标标签分开，ESU只读选中内容。当前MovieLens全库路径验证机制，不含真实公司serving与在线A/B。 例如下一次真实点击不能先进入历史再被GSU检索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-24ca72f5435a3fec">SIM top-k子序列需要怎样避免未来行为泄漏？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asim">Search-based User Interest Modeling with Lifelong Sequential Behavior Data for CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>检索只从当前请求前可见历史，候选query与目标标签分开，ESU只读选中内容。当前MovieLens全库路径验证机制，不含真实公司serving与在线A/B。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如下一次真实点击不能先进入历史再被GSU检索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2006.05639">原论文</a> · <a href="../../../../reproductions/2006.05639-sim/">实现解读</a> · <a href="#qa-24ca72f5435a3fec">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:bst" data-paper-title="Behavior Sequence Transformer for E-commerce Recommendation in Alibaba" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Behavior Sequence Transformer for E-commerce Recommendation in Alibaba 搜广推与 LLM 应用 Alibaba 2019-05-15 BST 用自注意力统一建模行为之间及行为与候选之间的关系，替代固定 pooling 或单一目标注意力。 Fidelity: 核心机制复现。实现候选 token、位置编码和行为序列 Transformer。公开数据替代淘宝日志；没有复刻用户画像、上下文特征和生产推理系统。本地对照口径：基线是 DIN；实验组是候选参与编码的 Transformer；三 seed NDCG@10 相对 +20.29%。  ranking classic sequence-modeling 搜广推 用户历史与排序骨干 BST 的候选 token 为什么要进入行为编码，而不是只在最后 MLP 中拼接？ 候选参与注意力后，历史表示可在编码阶段根据目标调整，模型同时学习行为之间与目标到历史的关系。最终拼接只允许已压缩表示与候选交互，早层无法改变取舍。这里的上下文是给定候选的条件表示，不应误认为所有候选通用。 示意：目标是登山鞋时，露营与徒步历史可互相支持；换成相机，编码阶段就应重新关注摄影片段，而非沿用鞋候选下形成的历史状态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-bst-730383cc" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a525ddf7b84c2c8a">BST 的候选 token 为什么要进入行为编码，而不是只在最后 MLP 中拼接？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Abst">Behavior Sequence Transformer for E-commerce Recommendation in Alibaba</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>候选参与注意力后，历史表示可在编码阶段根据目标调整，模型同时学习行为之间与目标到历史的关系。最终拼接只允许已压缩表示与候选交互，早层无法改变取舍。这里的上下文是给定候选的条件表示，不应误认为所有候选通用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>目标是登山鞋时，露营与徒步历史可互相支持；换成相机，编码阶段就应重新关注摄影片段，而非沿用鞋候选下形成的历史状态。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1905.06874">原论文</a> · <a href="../../../../reproductions/1905.06874-bst/">实现解读</a> · <a href="#qa-a525ddf7b84c2c8a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:bst" data-paper-title="Behavior Sequence Transformer for E-commerce Recommendation in Alibaba" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Behavior Sequence Transformer for E-commerce Recommendation in Alibaba 搜广推与 LLM 应用 Alibaba 2019-05-15 BST 用自注意力统一建模行为之间及行为与候选之间的关系，替代固定 pooling 或单一目标注意力。 Fidelity: 核心机制复现。实现候选 token、位置编码和行为序列 Transformer。公开数据替代淘宝日志；没有复刻用户画像、上下文特征和生产推理系统。本地对照口径：基线是 DIN；实验组是候选参与编码的 Transformer；三 seed NDCG@10 相对 +20.29%。  ranking classic sequence-modeling 搜广推 用户历史与排序骨干 BST把候选与行为一起做self-attention，和DIN只用候选给历史加权有什么不同？ DIN主要学习候选对各条行为的激活，BST还让行为之间交换信息，并让候选参与统一编码。这样某条历史的含义可以受其他行为影响，而不是始终作为固定键值独立出现；代价是更多序列计算，以及候选进入后部分状态不再能跨候选直接复用。是否值得要对齐预算与输入窗口比较。 示意：单独看一次相机点击可能是偶然，结合接连观看镜头和摄影教程后，行为间交互能强化摄影意图；换候选时共同编码的状态也可能随之改变。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-a856ffcdedab0d96">BST把候选与行为一起做self-attention，和DIN只用候选给历史加权有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Abst">Behavior Sequence Transformer for E-commerce Recommendation in Alibaba</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>DIN主要学习候选对各条行为的激活，BST还让行为之间交换信息，并让候选参与统一编码。这样某条历史的含义可以受其他行为影响，而不是始终作为固定键值独立出现；代价是更多序列计算，以及候选进入后部分状态不再能跨候选直接复用。是否值得要对齐预算与输入窗口比较。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>单独看一次相机点击可能是偶然，结合接连观看镜头和摄影教程后，行为间交互能强化摄影意图；换候选时共同编码的状态也可能随之改变。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1905.06874">原论文</a> · <a href="../../../../reproductions/1905.06874-bst/">实现解读</a> · <a href="#qa-a856ffcdedab0d96">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:bst" data-paper-title="Behavior Sequence Transformer for E-commerce Recommendation in Alibaba" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Behavior Sequence Transformer for E-commerce Recommendation in Alibaba 搜广推与 LLM 应用 Alibaba 2019-05-15 BST 用自注意力统一建模行为之间及行为与候选之间的关系，替代固定 pooling 或单一目标注意力。 Fidelity: 核心机制复现。实现候选 token、位置编码和行为序列 Transformer。公开数据替代淘宝日志；没有复刻用户画像、上下文特征和生产推理系统。本地对照口径：基线是 DIN；实验组是候选参与编码的 Transformer；三 seed NDCG@10 相对 +20.29%。  ranking classic sequence-modeling 搜广推 用户历史与排序骨干 BST 与固定历史 pooling 相比，多出的自注意力能力与成本是什么？ 固定 pooling 对每次行为使用预设或简化权重，难以表达行为组合。BST 通过成对交互学习上下文依赖，代价是长度相关的注意力计算，以及候选参与后重复编码的可能。模型更灵活不意味着必然胜出，仍需同数据、预算和候选协议比较。 示意：先看相机再看镜头与只看一条相机可能代表不同成熟度，pooling 易混淆；自注意力可组合两事件，但处理上千条历史也更费计算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-54c96f178108af99">BST 与固定历史 pooling 相比，多出的自注意力能力与成本是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Abst">Behavior Sequence Transformer for E-commerce Recommendation in Alibaba</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定 pooling 对每次行为使用预设或简化权重，难以表达行为组合。BST 通过成对交互学习上下文依赖，代价是长度相关的注意力计算，以及候选参与后重复编码的可能。模型更灵活不意味着必然胜出，仍需同数据、预算和候选协议比较。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先看相机再看镜头与只看一条相机可能代表不同成熟度，pooling 易混淆；自注意力可组合两事件，但处理上千条历史也更费计算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1905.06874">原论文</a> · <a href="../../../../reproductions/1905.06874-bst/">实现解读</a> · <a href="#qa-54c96f178108af99">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:bst" data-paper-title="Behavior Sequence Transformer for E-commerce Recommendation in Alibaba" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Behavior Sequence Transformer for E-commerce Recommendation in Alibaba 搜广推与 LLM 应用 Alibaba 2019-05-15 BST 用自注意力统一建模行为之间及行为与候选之间的关系，替代固定 pooling 或单一目标注意力。 Fidelity: 核心机制复现。实现候选 token、位置编码和行为序列 Transformer。公开数据替代淘宝日志；没有复刻用户画像、上下文特征和生产推理系统。本地对照口径：基线是 DIN；实验组是候选参与编码的 Transformer；三 seed NDCG@10 相对 +20.29%。  ranking classic sequence-modeling 搜广推 用户历史与排序骨干 BST 的候选条件状态为什么不能直接缓存成跨候选的公共用户 embedding？ 候选一旦参与 self-attention，就可能写入行为隐藏状态，替换候选会改变后续层输入。除非结构另加隔离掩码，缓存只能对应特定依赖条件。来源本地使用候选参与编码的 Transformer 与 DIN 比较，不能据此宣称实现了公共用户侧缓存。 示意：为鞋算出的历史状态已经放大鞋相关片段，拿它直接给电影评分会带入旧候选影响；公共缓存必须在候选写入之前截断。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f764ff81a314536c">BST 的候选条件状态为什么不能直接缓存成跨候选的公共用户 embedding？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Abst">Behavior Sequence Transformer for E-commerce Recommendation in Alibaba</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>候选一旦参与 self-attention，就可能写入行为隐藏状态，替换候选会改变后续层输入。除非结构另加隔离掩码，缓存只能对应特定依赖条件。来源本地使用候选参与编码的 Transformer 与 DIN 比较，不能据此宣称实现了公共用户侧缓存。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>为鞋算出的历史状态已经放大鞋相关片段，拿它直接给电影评分会带入旧候选影响；公共缓存必须在候选写入之前截断。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1905.06874">原论文</a> · <a href="../../../../reproductions/1905.06874-bst/">实现解读</a> · <a href="#qa-f764ff81a314536c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dien" data-paper-title="Deep Interest Evolution Network for Click-Through Rate Prediction" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Deep Interest Evolution Network for Click-Through Rate Prediction 搜广推与 LLM 应用 Alibaba 2018-09-11 DIN 直接激活历史兴趣，DIEN 则先用辅助监督抽取逐步兴趣，再让目标商品控制兴趣状态的演化速度。 Fidelity: 核心机制复现。实现兴趣抽取 GRU、下一行为辅助损失和候选相关兴趣演化。MovieLens 的短序列和稀疏信号不能替代 Taobao 广告特征；未使用生产 fused AUGRU kernel。本地对照口径：基线是同一训练协议的 DIN；实验组加入 GRU、辅助目标和候选相关演化；三 seed NDCG@10 相对 -1.98%，未迁移论文收益。  ranking classic sequence-modeling 搜广推 用户历史与排序骨干 DIEN 为什么把兴趣提取与目标相关演化分成两个阶段？ 前阶段按行为序列提取兴趣状态，辅助目标促使这些状态有预测意义；后阶段再由候选相关性控制哪些状态对当前目标产生更强更新。区分两阶段避免把原始点击直接等同于兴趣，同时保留目标条件，仍可能受辅助负例与历史噪声影响。 示意：连续看相机和镜头先形成摄影兴趣，面对旅行相机时相关阶段被强化；候选是小说时，同一摄影状态无需同样强地改变最终兴趣。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-dien-3d6c73b7" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9c333f1e60e9ad6d">DIEN 为什么把兴趣提取与目标相关演化分成两个阶段？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adien">Deep Interest Evolution Network for Click-Through Rate Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前阶段按行为序列提取兴趣状态，辅助目标促使这些状态有预测意义；后阶段再由候选相关性控制哪些状态对当前目标产生更强更新。区分两阶段避免把原始点击直接等同于兴趣，同时保留目标条件，仍可能受辅助负例与历史噪声影响。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>连续看相机和镜头先形成摄影兴趣，面对旅行相机时相关阶段被强化；候选是小说时，同一摄影状态无需同样强地改变最终兴趣。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1809.03672">原论文</a> · <a href="../../../../reproductions/1809.03672-dien/">实现解读</a> · <a href="#qa-9c333f1e60e9ad6d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dien" data-paper-title="Deep Interest Evolution Network for Click-Through Rate Prediction" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Deep Interest Evolution Network for Click-Through Rate Prediction 搜广推与 LLM 应用 Alibaba 2018-09-11 DIN 直接激活历史兴趣，DIEN 则先用辅助监督抽取逐步兴趣，再让目标商品控制兴趣状态的演化速度。 Fidelity: 核心机制复现。实现兴趣抽取 GRU、下一行为辅助损失和候选相关兴趣演化。MovieLens 的短序列和稀疏信号不能替代 Taobao 广告特征；未使用生产 fused AUGRU kernel。本地对照口径：基线是同一训练协议的 DIN；实验组加入 GRU、辅助目标和候选相关演化；三 seed NDCG@10 相对 -1.98%，未迁移论文收益。  ranking classic sequence-modeling 搜广推 用户历史与排序骨干 DIEN把目标相关权重乘进GRU更新门，而不只在最后对历史池化，改变了什么？ 辅助目标先帮助抽取每一步的兴趣状态，候选相关注意力再调节状态更新速度。相关行为可以更强地改写当前兴趣，不相关行为则较少覆盖已有记忆，目标信息因此参与整条演化链。若仅在结尾加权，前面的状态已可能被无关事件改写；多一个循环模块也不保证在短历史数据上更好。 示意：用户连续看摄影内容后偶然点一次食品广告，推荐镜头时可减弱这次食品行为对兴趣状态的更新，而不是等最后才试图从被改写的状态中恢复摄影兴趣。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-6b9b05c208996f59">DIEN把目标相关权重乘进GRU更新门，而不只在最后对历史池化，改变了什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adien">Deep Interest Evolution Network for Click-Through Rate Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>辅助目标先帮助抽取每一步的兴趣状态，候选相关注意力再调节状态更新速度。相关行为可以更强地改写当前兴趣，不相关行为则较少覆盖已有记忆，目标信息因此参与整条演化链。若仅在结尾加权，前面的状态已可能被无关事件改写；多一个循环模块也不保证在短历史数据上更好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户连续看摄影内容后偶然点一次食品广告，推荐镜头时可减弱这次食品行为对兴趣状态的更新，而不是等最后才试图从被改写的状态中恢复摄影兴趣。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1809.03672">原论文</a> · <a href="../../../../reproductions/1809.03672-dien/">实现解读</a> · <a href="#qa-6b9b05c208996f59">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dien" data-paper-title="Deep Interest Evolution Network for Click-Through Rate Prediction" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Deep Interest Evolution Network for Click-Through Rate Prediction 搜广推与 LLM 应用 Alibaba 2018-09-11 DIN 直接激活历史兴趣，DIEN 则先用辅助监督抽取逐步兴趣，再让目标商品控制兴趣状态的演化速度。 Fidelity: 核心机制复现。实现兴趣抽取 GRU、下一行为辅助损失和候选相关兴趣演化。MovieLens 的短序列和稀疏信号不能替代 Taobao 广告特征；未使用生产 fused AUGRU kernel。本地对照口径：基线是同一训练协议的 DIN；实验组加入 GRU、辅助目标和候选相关演化；三 seed NDCG@10 相对 -1.98%，未迁移论文收益。  ranking classic sequence-modeling 搜广推 用户历史与排序骨干 DIEN 与 DIN 的目标注意力相比，候选信息进入时间上有什么不同？ DIN 在聚合时给历史加权，DIEN 将相关权重乘进循环更新门，影响每一步保留旧状态与接收新状态的比例。它改变兴趣演化过程，而非仅最终读出。增加时间路径也带来训练与预算差异，来源本地未复现收益，不能据结构复杂就预设更好。 示意：某次镜头浏览对相机候选重要，DIEN 可当时更强更新循环状态；若只最后加权，之前状态如何被压缩已经决定，无法同样改写。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-50f77630c64f3a37">DIEN 与 DIN 的目标注意力相比，候选信息进入时间上有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adien">Deep Interest Evolution Network for Click-Through Rate Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>DIN 在聚合时给历史加权，DIEN 将相关权重乘进循环更新门，影响每一步保留旧状态与接收新状态的比例。它改变兴趣演化过程，而非仅最终读出。增加时间路径也带来训练与预算差异，来源本地未复现收益，不能据结构复杂就预设更好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某次镜头浏览对相机候选重要，DIEN 可当时更强更新循环状态；若只最后加权，之前状态如何被压缩已经决定，无法同样改写。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1809.03672">原论文</a> · <a href="../../../../reproductions/1809.03672-dien/">实现解读</a> · <a href="#qa-50f77630c64f3a37">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:dien" data-paper-title="Deep Interest Evolution Network for Click-Through Rate Prediction" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Deep Interest Evolution Network for Click-Through Rate Prediction 搜广推与 LLM 应用 Alibaba 2018-09-11 DIN 直接激活历史兴趣，DIEN 则先用辅助监督抽取逐步兴趣，再让目标商品控制兴趣状态的演化速度。 Fidelity: 核心机制复现。实现兴趣抽取 GRU、下一行为辅助损失和候选相关兴趣演化。MovieLens 的短序列和稀疏信号不能替代 Taobao 广告特征；未使用生产 fused AUGRU kernel。本地对照口径：基线是同一训练协议的 DIN；实验组加入 GRU、辅助目标和候选相关演化；三 seed NDCG@10 相对 -1.98%，未迁移论文收益。  ranking classic sequence-modeling 搜广推 用户历史与排序骨干 DIEN 的辅助下一行为监督应如何避免和测试未来混淆？ 辅助目标可使用训练序列的下一行为作为标签，但兴趣提取输入仍限于当前及以前位置，采样负例也来自训练口径。评估时不能把 held-out 下一物品输入 GRU。候选相关更新门要保持逐步状态递推，而不是事后拿同一权重乘最终向量。 示意：训练在位置二预测位置三合理；测试想猜位置三时若先把它喂进序列，即使只称辅助任务，也已读到正确答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-fcaef89988ef9b8e">DIEN 的辅助下一行为监督应如何避免和测试未来混淆？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adien">Deep Interest Evolution Network for Click-Through Rate Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>辅助目标可使用训练序列的下一行为作为标签，但兴趣提取输入仍限于当前及以前位置，采样负例也来自训练口径。评估时不能把 held-out 下一物品输入 GRU。候选相关更新门要保持逐步状态递推，而不是事后拿同一权重乘最终向量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>训练在位置二预测位置三合理；测试想猜位置三时若先把它喂进序列，即使只称辅助任务，也已读到正确答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1809.03672">原论文</a> · <a href="../../../../reproductions/1809.03672-dien/">实现解读</a> · <a href="#qa-fcaef89988ef9b8e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sasrec" data-paper-title="Self-Attentive Sequential Recommendation" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Self-Attentive Sequential Recommendation 搜广推与 LLM 应用 UC San Diego 2018-08-20 Markov Chain 偏重最近行为，RNN 又需要逐步计算。SASRec 用因果自注意力直接选择序列中与下一物品相关的行为，在稀疏与稠密数据之间取得更灵活的感受野，并成为序列推荐常用基线。 保真度：完整核心链路复现。保真度：完整核心链路复现。模型、原论文 pairwise BCE 训练目标与序列推理均实际执行；仅把公开数据从 MovieLens-1M 缩到 MovieLens-100K，并采用更严格的全库评估。本地对照口径：基线是 popularity 排序；实验组是 SASRec；主指标 NDCG@10 从 0.02969 降至 0.02933（-1.24%）。这是跨模型基线比较，不是 SASRec 模块消融。   搜广推 用户历史与排序骨干 SASRec训练时，每个历史位置的输入与要预测的下一物品怎样错开？ 位置i只能读取截至该位置的历史，目标是紧接其后的物品，未来事件作为监督而不是额外输入。一个用户序列因此可产生多个前缀预测任务；padding位置还需排除。先理解这种位移，才能判断实现是否不小心把目标物品喂回了当前表示。 教学例子：历史为甲、乙、丙时，可用甲预测乙、用甲乙预测丙；预测乙的表示不能提前读取丙。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-sasrec-6f67bc6e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7d35ae6cc7ed04c8">SASRec训练时，每个历史位置的输入与要预测的下一物品怎样错开？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asasrec">Self-Attentive Sequential Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>位置i只能读取截至该位置的历史，目标是紧接其后的物品，未来事件作为监督而不是额外输入。一个用户序列因此可产生多个前缀预测任务；padding位置还需排除。先理解这种位移，才能判断实现是否不小心把目标物品喂回了当前表示。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>历史为甲、乙、丙时，可用甲预测乙、用甲乙预测丙；预测乙的表示不能提前读取丙。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1808.09781">原论文</a> · <a href="../../../../reproductions/1808.09781-sasrec/">实现解读</a> · <a href="#qa-7d35ae6cc7ed04c8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sasrec" data-paper-title="Self-Attentive Sequential Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Self-Attentive Sequential Recommendation 搜广推与 LLM 应用 UC San Diego 2018-08-20 Markov Chain 偏重最近行为，RNN 又需要逐步计算。SASRec 用因果自注意力直接选择序列中与下一物品相关的行为，在稀疏与稠密数据之间取得更灵活的感受野，并成为序列推荐常用基线。 保真度：完整核心链路复现。保真度：完整核心链路复现。模型、原论文 pairwise BCE 训练目标与序列推理均实际执行；仅把公开数据从 MovieLens-1M 缩到 MovieLens-100K，并采用更严格的全库评估。本地对照口径：基线是 popularity 排序；实验组是 SASRec；主指标 NDCG@10 从 0.02969 降至 0.02933（-1.24%）。这是跨模型基线比较，不是 SASRec 模块消融。   搜广推 用户历史与排序骨干 SASRec 的因果自注意力如何兼顾短期与较远兴趣，又怎样避免训练时读取未来？ 每个位置可按内容对此前多个行为分配注意力，不像固定阶 Markov 只看近邻，也不必像 RNN 逐步递推全部历史。因果掩码禁止当前位置读取后续事件，下一物品仅作为监督目标。位置表示保留顺序，网络因数据稀疏程度可学不同感受野；自注意力本身不保证自动忽略所有无关历史。 示意：用户最近看喜剧，但较早看过多部科幻。预测下一片时可回看相关科幻行为，同时训练位置三不能看到位置四的电影，即使它正是要预测的标签。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-9e5caa204add37ff">SASRec 的因果自注意力如何兼顾短期与较远兴趣，又怎样避免训练时读取未来？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asasrec">Self-Attentive Sequential Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每个位置可按内容对此前多个行为分配注意力，不像固定阶 Markov 只看近邻，也不必像 RNN 逐步递推全部历史。因果掩码禁止当前位置读取后续事件，下一物品仅作为监督目标。位置表示保留顺序，网络因数据稀疏程度可学不同感受野；自注意力本身不保证自动忽略所有无关历史。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户最近看喜剧，但较早看过多部科幻。预测下一片时可回看相关科幻行为，同时训练位置三不能看到位置四的电影，即使它正是要预测的标签。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1808.09781">原论文</a> · <a href="../../../../reproductions/1808.09781-sasrec/">实现解读</a> · <a href="#qa-9e5caa204add37ff">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sasrec" data-paper-title="Self-Attentive Sequential Recommendation" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Self-Attentive Sequential Recommendation 搜广推与 LLM 应用 UC San Diego 2018-08-20 Markov Chain 偏重最近行为，RNN 又需要逐步计算。SASRec 用因果自注意力直接选择序列中与下一物品相关的行为，在稀疏与稠密数据之间取得更灵活的感受野，并成为序列推荐常用基线。 保真度：完整核心链路复现。保真度：完整核心链路复现。模型、原论文 pairwise BCE 训练目标与序列推理均实际执行；仅把公开数据从 MovieLens-1M 缩到 MovieLens-100K，并采用更严格的全库评估。本地对照口径：基线是 popularity 排序；实验组是 SASRec；主指标 NDCG@10 从 0.02969 降至 0.02933（-1.24%）。这是跨模型基线比较，不是 SASRec 模块消融。   搜广推 用户历史与排序骨干 SASRec的因果下一物品训练，与允许左右邻居的掩码物品恢复有何区别？ 前者只能利用过去，目标对应未来下一项；后者可把某个中间项遮住并利用两侧信息恢复。两者读取条件与任务目标不同。双向上下文在恢复任务中可能合法，却不能直接放入SASRec下一步预测并沿用同一无泄露解释。 教学例子：恢复甲、[MASK]、丙里的乙可看丙；在只观察到甲的时间点预测乙，则丙仍属于不可见未来。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-128c509fca314590">SASRec的因果下一物品训练，与允许左右邻居的掩码物品恢复有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asasrec">Self-Attentive Sequential Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者只能利用过去，目标对应未来下一项；后者可把某个中间项遮住并利用两侧信息恢复。两者读取条件与任务目标不同。双向上下文在恢复任务中可能合法，却不能直接放入SASRec下一步预测并沿用同一无泄露解释。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>恢复甲、[MASK]、丙里的乙可看丙；在只观察到甲的时间点预测乙，则丙仍属于不可见未来。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1808.09781">原论文</a> · <a href="../../../../reproductions/1808.09781-sasrec/">实现解读</a> · <a href="#qa-128c509fca314590">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:sasrec" data-paper-title="Self-Attentive Sequential Recommendation" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Self-Attentive Sequential Recommendation 搜广推与 LLM 应用 UC San Diego 2018-08-20 Markov Chain 偏重最近行为，RNN 又需要逐步计算。SASRec 用因果自注意力直接选择序列中与下一物品相关的行为，在稀疏与稠密数据之间取得更灵活的感受野，并成为序列推荐常用基线。 保真度：完整核心链路复现。保真度：完整核心链路复现。模型、原论文 pairwise BCE 训练目标与序列推理均实际执行；仅把公开数据从 MovieLens-1M 缩到 MovieLens-100K，并采用更严格的全库评估。本地对照口径：基线是 popularity 排序；实验组是 SASRec；主指标 NDCG@10 从 0.02969 降至 0.02933（-1.24%）。这是跨模型基线比较，不是 SASRec 模块消融。   搜广推 用户历史与排序骨干 SASRec输入输出embedding与负样本目标怎样保持原机制？ 输入item向量与输出权重绑定，每位置使用正物品和采样负物品的pairwise BCE，不能擅换全库CE后说目标未变。padding和未来位置都需mask。 例如负样本不能抽到该位置真实正例，再让模型把同一物品同时推高压低。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7b580fbe795a484e">SASRec输入输出embedding与负样本目标怎样保持原机制？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Asasrec">Self-Attentive Sequential Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>输入item向量与输出权重绑定，每位置使用正物品和采样负物品的pairwise BCE，不能擅换全库CE后说目标未变。padding和未来位置都需mask。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如负样本不能抽到该位置真实正例，再让模型把同一物品同时推高压低。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1808.09781">原论文</a> · <a href="../../../../reproductions/1808.09781-sasrec/">实现解读</a> · <a href="#qa-7b580fbe795a484e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:din" data-paper-title="Deep Interest Network for Click-Through Rate Prediction" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Deep Interest Network for Click-Through Rate Prediction 搜广推与 LLM 应用 Alibaba 2017-06-21 传统 CTR 模型把用户全部行为压成固定向量，但用户与候选物品相关的兴趣只占历史的一部分。DIN 不再生成一个与候选无关的用户向量，而是用候选物品逐条激活历史行为，再把局部兴趣送入点击网络；Dice 根据当前特征分布自适应调整激活边界。 保真度：核心机制复现。保真度：核心机制复现。本实现实际训练候选物品条件化的 local activation、加权兴趣池化、Dice 与 CTR 网络；未复刻 Alibaba 私有稀疏特征、mini-batch-aware regularization 和生产 serving。本地对照口径：基线是移除 candidate-aware attention、改用 mean pooling 的同参数模型；实验组是 DIN；主指标 NDCG@10 从 0.01783 降至 0.01659（-6.97%）。这是 DIN 核心注意力的内部消融，不是相对其他推荐模型的提升。   搜广推 用户历史与排序骨干 DIN 的“局部兴趣”为什么是候选条件的，而不是用户只拥有一个短期兴趣？ 局部指从全部历史中取与当前目标相关的部分，用户仍可能同时有多种兴趣。候选换了，激活权重和汇总向量也换，模型无需先确定一个唯一兴趣标签。历史里没有的需求不能被注意力创造，低相关权重也不表示用户永久不喜欢该内容。 示意：同一用户既看科幻又看烹饪，面对电影候选激活观影历史，面对厨具候选关注烹饪行为；两种兴趣可以同时存在。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-din-dfe7b0eb" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7c7ffdd9c88660a4">DIN 的“局部兴趣”为什么是候选条件的，而不是用户只拥有一个短期兴趣？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adin">Deep Interest Network for Click-Through Rate Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>局部指从全部历史中取与当前目标相关的部分，用户仍可能同时有多种兴趣。候选换了，激活权重和汇总向量也换，模型无需先确定一个唯一兴趣标签。历史里没有的需求不能被注意力创造，低相关权重也不表示用户永久不喜欢该内容。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一用户既看科幻又看烹饪，面对电影候选激活观影历史，面对厨具候选关注烹饪行为；两种兴趣可以同时存在。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1706.06978">原论文</a> · <a href="../../../../reproductions/1706.06978-din/">实现解读</a> · <a href="#qa-7c7ffdd9c88660a4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:din" data-paper-title="Deep Interest Network for Click-Through Rate Prediction" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Deep Interest Network for Click-Through Rate Prediction 搜广推与 LLM 应用 Alibaba 2017-06-21 传统 CTR 模型把用户全部行为压成固定向量，但用户与候选物品相关的兴趣只占历史的一部分。DIN 不再生成一个与候选无关的用户向量，而是用候选物品逐条激活历史行为，再把局部兴趣送入点击网络；Dice 根据当前特征分布自适应调整激活边界。 保真度：核心机制复现。保真度：核心机制复现。本实现实际训练候选物品条件化的 local activation、加权兴趣池化、Dice 与 CTR 网络；未复刻 Alibaba 私有稀疏特征、mini-batch-aware regularization 和生产 serving。本地对照口径：基线是移除 candidate-aware attention、改用 mean pooling 的同参数模型；实验组是 DIN；主指标 NDCG@10 从 0.01783 降至 0.01659（-6.97%）。这是 DIN 核心注意力的内部消融，不是相对其他推荐模型的提升。   搜广推 用户历史与排序骨干 DIN为什么对同一个用户也会得到不同的兴趣向量？ 用户历史包含多种兴趣，哪些行为重要取决于当前候选。DIN用候选和每条历史的组合特征学习激活，再加权聚合，因此用户表示随候选变化，而非始终是一个固定均值。候选感知提高表达力，却也意味着完整聚合状态通常不能跨所有候选直接复用；效果需与同预算池化对照判断。 示意：历史里既有跑鞋也有烤箱，评估运动袜时突出跑步行为，评估烘焙工具时突出厨房行为；两次使用同一份历史，却应得到不同的兴趣摘要。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-13240dbf0db3f265">DIN为什么对同一个用户也会得到不同的兴趣向量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adin">Deep Interest Network for Click-Through Rate Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用户历史包含多种兴趣，哪些行为重要取决于当前候选。DIN用候选和每条历史的组合特征学习激活，再加权聚合，因此用户表示随候选变化，而非始终是一个固定均值。候选感知提高表达力，却也意味着完整聚合状态通常不能跨所有候选直接复用；效果需与同预算池化对照判断。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>历史里既有跑鞋也有烤箱，评估运动袜时突出跑步行为，评估烘焙工具时突出厨房行为；两次使用同一份历史，却应得到不同的兴趣摘要。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1706.06978">原论文</a> · <a href="../../../../reproductions/1706.06978-din/">实现解读</a> · <a href="#qa-13240dbf0db3f265">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:din" data-paper-title="Deep Interest Network for Click-Through Rate Prediction" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Deep Interest Network for Click-Through Rate Prediction 搜广推与 LLM 应用 Alibaba 2017-06-21 传统 CTR 模型把用户全部行为压成固定向量，但用户与候选物品相关的兴趣只占历史的一部分。DIN 不再生成一个与候选无关的用户向量，而是用候选物品逐条激活历史行为，再把局部兴趣送入点击网络；Dice 根据当前特征分布自适应调整激活边界。 保真度：核心机制复现。保真度：核心机制复现。本实现实际训练候选物品条件化的 local activation、加权兴趣池化、Dice 与 CTR 网络；未复刻 Alibaba 私有稀疏特征、mini-batch-aware regularization 和生产 serving。本地对照口径：基线是移除 candidate-aware attention、改用 mean pooling 的同参数模型；实验组是 DIN；主指标 NDCG@10 从 0.01783 降至 0.01659（-6.97%）。这是 DIN 核心注意力的内部消融，不是相对其他推荐模型的提升。   搜广推 用户历史与排序骨干 DIN 的 local activation 与普通点积注意力，在交互输入上有什么区别？ 来源激活网络同时读取候选、行为、差值和逐元素乘积，能学习比单一点积更丰富的匹配；这不保证学习到真实因果关系。Dice 又按特征分布调整激活边界。机制灵活性要由同预算消融检验，来源本地对均值池化并未观察到收益。 示意：两件商品点积接近时，差值可突出价格维度差别，乘积可强调共同品类；小网络可学习这些组合，而不是只比较向量夹角。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-77536cb95e45f6d4">DIN 的 local activation 与普通点积注意力，在交互输入上有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adin">Deep Interest Network for Click-Through Rate Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>来源激活网络同时读取候选、行为、差值和逐元素乘积，能学习比单一点积更丰富的匹配；这不保证学习到真实因果关系。Dice 又按特征分布调整激活边界。机制灵活性要由同预算消融检验，来源本地对均值池化并未观察到收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两件商品点积接近时，差值可突出价格维度差别，乘积可强调共同品类；小网络可学习这些组合，而不是只比较向量夹角。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1706.06978">原论文</a> · <a href="../../../../reproductions/1706.06978-din/">实现解读</a> · <a href="#qa-77536cb95e45f6d4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:din" data-paper-title="Deep Interest Network for Click-Through Rate Prediction" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Deep Interest Network for Click-Through Rate Prediction 搜广推与 LLM 应用 Alibaba 2017-06-21 传统 CTR 模型把用户全部行为压成固定向量，但用户与候选物品相关的兴趣只占历史的一部分。DIN 不再生成一个与候选无关的用户向量，而是用候选物品逐条激活历史行为，再把局部兴趣送入点击网络；Dice 根据当前特征分布自适应调整激活边界。 保真度：核心机制复现。保真度：核心机制复现。本实现实际训练候选物品条件化的 local activation、加权兴趣池化、Dice 与 CTR 网络；未复刻 Alibaba 私有稀疏特征、mini-batch-aware regularization 和生产 serving。本地对照口径：基线是移除 candidate-aware attention、改用 mean pooling 的同参数模型；实验组是 DIN；主指标 NDCG@10 从 0.01783 降至 0.01659（-6.97%）。这是 DIN 核心注意力的内部消融，不是相对其他推荐模型的提升。   搜广推 用户历史与排序骨干 DIN 的候选权重应在哪个轴归一，padding 又应怎样处理？ 对同一用户、同一候选的有效历史位置归一，padding 在归一前屏蔽，避免空行为分走权重。不同候选分别计算，不应把批次或候选轴当历史轴。Dice 的训练批统计与服务状态也须一致，不能拿测试批标签调整统计。 示意：三条真实行为加五条 padding，权重应只在三条间分配；若八条都参与，短历史用户表示被稀释，结果即使维度正确也偏离机制。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-fce6f5413a09b608">DIN 的候选权重应在哪个轴归一，padding 又应怎样处理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adin">Deep Interest Network for Click-Through Rate Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>对同一用户、同一候选的有效历史位置归一，padding 在归一前屏蔽，避免空行为分走权重。不同候选分别计算，不应把批次或候选轴当历史轴。Dice 的训练批统计与服务状态也须一致，不能拿测试批标签调整统计。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三条真实行为加五条 padding，权重应只在三条间分配；若八条都参与，短历史用户表示被稀释，结果即使维度正确也偏离机制。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1706.06978">原论文</a> · <a href="../../../../reproductions/1706.06978-din/">实现解读</a> · <a href="#qa-fce6f5413a09b608">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:deepfm" data-paper-title="DeepFM: A Factorization-Machine based Neural Network for CTR Prediction" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="DeepFM: A Factorization-Machine based Neural Network for CTR Prediction 搜广推与 LLM 应用 Huawei Noah&#x27;s Ark Lab 2017-03-13 CTR 排序既依赖低阶组合特征，也依赖高阶非线性交互。传统 Wide &amp; Deep 需要人工构造 wide 特征，DeepFM 则让两条路径端到端共享 embedding。模型把 FM 的一阶/二阶项与 MLP 输出相加。相同 field embedding 同时进入两条路径，减少人工交叉和重复参数。 复现级别：核心机制复现。复现级别：核心机制复现。实际联合训练 FM 二阶交互与 deep 分支；私有工业特征和线上系统不在本地复现范围。本地对照口径：基线为 embedding MLP，实验组为共享 embedding 的 FM + deep 分支；NDCG@10 相对 +23.58%，见 metrics/movielens-100k-seeds42-44.json。  ranking classic feature-interaction 搜广推 用户历史与排序骨干 DeepFM 的 FM 一阶、二阶与 DNN 输出分别补充什么信息？ 一阶项表达单特征贡献，FM 通过向量内积显式覆盖二阶组合，DNN 学习更复杂非线性关系，最终共同形成点击 logit。共享 embedding 让两条路径互相约束，不代表二阶与高阶完全互不重叠，也不能把三部分概率直接相加。 示意：城市本身影响点击，一座城市与某品类的组合是二阶，再加价格和时间形成复杂条件可由深路学习，三类信号在同一 logit 汇合。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-deepfm-65a63b7d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-aa25bf5c7ee147c5">DeepFM 的 FM 一阶、二阶与 DNN 输出分别补充什么信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adeepfm">DeepFM: A Factorization-Machine based Neural Network for CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Noah&#x27;s Ark Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一阶项表达单特征贡献，FM 通过向量内积显式覆盖二阶组合，DNN 学习更复杂非线性关系，最终共同形成点击 logit。共享 embedding 让两条路径互相约束，不代表二阶与高阶完全互不重叠，也不能把三部分概率直接相加。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>城市本身影响点击，一座城市与某品类的组合是二阶，再加价格和时间形成复杂条件可由深路学习，三类信号在同一 logit 汇合。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1703.04247">原论文</a> · <a href="../../../../reproductions/1703.04247-deepfm/">实现解读</a> · <a href="#qa-aa25bf5c7ee147c5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:deepfm" data-paper-title="DeepFM: A Factorization-Machine based Neural Network for CTR Prediction" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="DeepFM: A Factorization-Machine based Neural Network for CTR Prediction 搜广推与 LLM 应用 Huawei Noah&#x27;s Ark Lab 2017-03-13 CTR 排序既依赖低阶组合特征，也依赖高阶非线性交互。传统 Wide &amp; Deep 需要人工构造 wide 特征，DeepFM 则让两条路径端到端共享 embedding。模型把 FM 的一阶/二阶项与 MLP 输出相加。相同 field embedding 同时进入两条路径，减少人工交叉和重复参数。 复现级别：核心机制复现。复现级别：核心机制复现。实际联合训练 FM 二阶交互与 deep 分支；私有工业特征和线上系统不在本地复现范围。本地对照口径：基线为 embedding MLP，实验组为共享 embedding 的 FM + deep 分支；NDCG@10 相对 +23.58%，见 metrics/movielens-100k-seeds42-44.json。  ranking classic feature-interaction 搜广推 用户历史与排序骨干 DeepFM为什么让FM与DNN共享同一份field embedding？ FM直接建模一阶和二阶组合，DNN学习更高阶非线性关系，两路需要的是同一组基础字段语义。共享embedding减少重复参数，并让低阶与高阶监督共同塑造底层表示，避免像手工wide交叉那样额外维护特征。但共享也会产生梯度耦合，不能把两路分数相加视为天然无冲突。 示意：用户职业与商品类目的一对组合可由FM学习，职业、类目、价格三者的复杂条件交给DNN；两路都更新同一字段向量，而不是各存一套互不沟通的词表。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c7aa48572635a536">DeepFM为什么让FM与DNN共享同一份field embedding？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adeepfm">DeepFM: A Factorization-Machine based Neural Network for CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Noah&#x27;s Ark Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>FM直接建模一阶和二阶组合，DNN学习更高阶非线性关系，两路需要的是同一组基础字段语义。共享embedding减少重复参数，并让低阶与高阶监督共同塑造底层表示，避免像手工wide交叉那样额外维护特征。但共享也会产生梯度耦合，不能把两路分数相加视为天然无冲突。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用户职业与商品类目的一对组合可由FM学习，职业、类目、价格三者的复杂条件交给DNN；两路都更新同一字段向量，而不是各存一套互不沟通的词表。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1703.04247">原论文</a> · <a href="../../../../reproductions/1703.04247-deepfm/">实现解读</a> · <a href="#qa-c7aa48572635a536">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:deepfm" data-paper-title="DeepFM: A Factorization-Machine based Neural Network for CTR Prediction" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="DeepFM: A Factorization-Machine based Neural Network for CTR Prediction 搜广推与 LLM 应用 Huawei Noah&#x27;s Ark Lab 2017-03-13 CTR 排序既依赖低阶组合特征，也依赖高阶非线性交互。传统 Wide &amp; Deep 需要人工构造 wide 特征，DeepFM 则让两条路径端到端共享 embedding。模型把 FM 的一阶/二阶项与 MLP 输出相加。相同 field embedding 同时进入两条路径，减少人工交叉和重复参数。 复现级别：核心机制复现。复现级别：核心机制复现。实际联合训练 FM 二阶交互与 deep 分支；私有工业特征和线上系统不在本地复现范围。本地对照口径：基线为 embedding MLP，实验组为共享 embedding 的 FM + deep 分支；NDCG@10 相对 +23.58%，见 metrics/movielens-100k-seeds42-44.json。  ranking classic feature-interaction 搜广推 用户历史与排序骨干 DeepFM 与需要人工 wide 交叉的 Wide &amp; Deep，主要工程假设有何不同？ DeepFM 用 FM 向量内积学习二阶关系，减少逐一设计人工交叉，同时让 FM 和深路共享字段表示。人工 wide 可精确定义特殊规则，但覆盖与维护成本高；FM 也受嵌入表达限制，减少工程不意味着无需字段设计与数据治理。 示意：不必为每个城市与品类组合手写列，FM 可从字段向量学习关系；但若某项业务禁止组合，仍需显式规则，不能指望 FM 自动学成合规约束。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a20cf160a75d260a">DeepFM 与需要人工 wide 交叉的 Wide &amp; Deep，主要工程假设有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adeepfm">DeepFM: A Factorization-Machine based Neural Network for CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Noah&#x27;s Ark Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>DeepFM 用 FM 向量内积学习二阶关系，减少逐一设计人工交叉，同时让 FM 和深路共享字段表示。人工 wide 可精确定义特殊规则，但覆盖与维护成本高；FM 也受嵌入表达限制，减少工程不意味着无需字段设计与数据治理。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>不必为每个城市与品类组合手写列，FM 可从字段向量学习关系；但若某项业务禁止组合，仍需显式规则，不能指望 FM 自动学成合规约束。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1703.04247">原论文</a> · <a href="../../../../reproductions/1703.04247-deepfm/">实现解读</a> · <a href="#qa-a20cf160a75d260a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:deepfm" data-paper-title="DeepFM: A Factorization-Machine based Neural Network for CTR Prediction" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="DeepFM: A Factorization-Machine based Neural Network for CTR Prediction 搜广推与 LLM 应用 Huawei Noah&#x27;s Ark Lab 2017-03-13 CTR 排序既依赖低阶组合特征，也依赖高阶非线性交互。传统 Wide &amp; Deep 需要人工构造 wide 特征，DeepFM 则让两条路径端到端共享 embedding。模型把 FM 的一阶/二阶项与 MLP 输出相加。相同 field embedding 同时进入两条路径，减少人工交叉和重复参数。 复现级别：核心机制复现。复现级别：核心机制复现。实际联合训练 FM 二阶交互与 deep 分支；私有工业特征和线上系统不在本地复现范围。本地对照口径：基线为 embedding MLP，实验组为共享 embedding 的 FM + deep 分支；NDCG@10 相对 +23.58%，见 metrics/movielens-100k-seeds42-44.json。  ranking classic feature-interaction 搜广推 用户历史与排序骨干 DeepFM 计算二阶项时，为什么必须只计 i&lt;j，而不能连自身项一起求？ FM 定义的是不同特征对，加入 i=j 会额外产生自平方项，重复计 i,j 与 j,i 也改变尺度。可用平方和减各项平方的恒等式高效计算再乘二分之一；两路须使用同一份 embedding 参数，复制初值并不等于共享。 示意：年龄与品类算一次交互即可，年龄与自己不应混进二阶对；若 FM 和 DNN 各复制一份向量，训练后会分叉，失去共享学习定义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-41c1dda6c15dea15">DeepFM 计算二阶项时，为什么必须只计 i&lt;j，而不能连自身项一起求？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Adeepfm">DeepFM: A Factorization-Machine based Neural Network for CTR Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Huawei Noah&#x27;s Ark Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>FM 定义的是不同特征对，加入 i=j 会额外产生自平方项，重复计 i,j 与 j,i 也改变尺度。可用平方和减各项平方的恒等式高效计算再乘二分之一；两路须使用同一份 embedding 参数，复制初值并不等于共享。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>年龄与品类算一次交互即可，年龄与自己不应混进二阶对；若 FM 和 DNN 各复制一份向量，训练后会分叉，失去共享学习定义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1703.04247">原论文</a> · <a href="../../../../reproductions/1703.04247-deepfm/">实现解读</a> · <a href="#qa-41c1dda6c15dea15">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:wide-deep" data-paper-title="Wide &amp; Deep Learning for Recommender Systems" data-learning-pending="false" data-level="basics" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Wide &amp; Deep Learning for Recommender Systems 搜广推与 LLM 应用 Google 2016-06-24 纯线性模型善于记忆稀疏共现但泛化弱，纯 DNN 能泛化却可能推荐不相关组合。论文联合训练两路并共享最终 logit。 Fidelity: 核心机制复现。本地实现联合记忆型 wide 交叉与泛化型 deep tower。公开 MovieLens 替代 Google Play 私有日志；未复刻生产特征工程、分布式训练与 serving。本地对照口径：基线是参数匹配的 deep-only 模型；实验组加入 candidate 与 genre 交叉的 wide 路径；MovieLens-100K 三 seed 全库 NDCG@10 相对 +5.45%。  ranking classic feature-interaction 搜广推 用户历史与排序骨干 Wide &amp; Deep为什么同时保留线性与深层两路？ wide擅长记忆稀疏共现和人工交叉，deep经embedding泛化到未见组合；联合logit把两类优势放进一个训练目标，不是简单两个独立模型轮流服务。 例如已常见的组合可靠记忆，新组合通过相似表征泛化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<span id="paper-recommendation-wide-deep-604050a0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-44139f39f329ea5a">Wide &amp; Deep为什么同时保留线性与深层两路？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Awide-deep">Wide &amp; Deep Learning for Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>wide擅长记忆稀疏共现和人工交叉，deep经embedding泛化到未见组合；联合logit把两类优势放进一个训练目标，不是简单两个独立模型轮流服务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如已常见的组合可靠记忆，新组合通过相似表征泛化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1606.07792">原论文</a> · <a href="../../../../reproductions/1606.07792-wide-deep/">实现解读</a> · <a href="#qa-44139f39f329ea5a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:wide-deep" data-paper-title="Wide &amp; Deep Learning for Recommender Systems" data-learning-pending="false" data-level="mechanism" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Wide &amp; Deep Learning for Recommender Systems 搜广推与 LLM 应用 Google 2016-06-24 纯线性模型善于记忆稀疏共现但泛化弱，纯 DNN 能泛化却可能推荐不相关组合。论文联合训练两路并共享最终 logit。 Fidelity: 核心机制复现。本地实现联合记忆型 wide 交叉与泛化型 deep tower。公开 MovieLens 替代 Google Play 私有日志；未复刻生产特征工程、分布式训练与 serving。本地对照口径：基线是参数匹配的 deep-only 模型；实验组加入 candidate 与 genre 交叉的 wide 路径；MovieLens-100K 三 seed 全库 NDCG@10 相对 +5.45%。  ranking classic feature-interaction 搜广推 用户历史与排序骨干 Wide &amp; Deep 为什么联合训练线性交叉与深网络，而不是只对两个独立模型做分数平均？ wide 路径可直接记忆已观察到的稀疏交叉，deep 路径通过嵌入与非线性共享知识，二者共同贡献一个 logit 并接受同一目标梯度。联合训练让各自学习补充尚未解释的部分，而非独立训练后固定融合。人工交叉覆盖有限，deep 泛化也可能产生不合理组合，因此两路能力互补但都需控制。 示意：wide 可记住“某用户群经常买某类商品”的明确交叉，deep 把相似品类经验迁移给新组合。共同训练时两者调整相对贡献，不是先各自最优再简单取平均。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-bc8a20781ba57a95">Wide &amp; Deep 为什么联合训练线性交叉与深网络，而不是只对两个独立模型做分数平均？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Awide-deep">Wide &amp; Deep Learning for Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>wide 路径可直接记忆已观察到的稀疏交叉，deep 路径通过嵌入与非线性共享知识，二者共同贡献一个 logit 并接受同一目标梯度。联合训练让各自学习补充尚未解释的部分，而非独立训练后固定融合。人工交叉覆盖有限，deep 泛化也可能产生不合理组合，因此两路能力互补但都需控制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>wide 可记住“某用户群经常买某类商品”的明确交叉，deep 把相似品类经验迁移给新组合。共同训练时两者调整相对贡献，不是先各自最优再简单取平均。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1606.07792">原论文</a> · <a href="../../../../reproductions/1606.07792-wide-deep/">实现解读</a> · <a href="#qa-bc8a20781ba57a95">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:wide-deep" data-paper-title="Wide &amp; Deep Learning for Recommender Systems" data-learning-pending="false" data-level="comparison" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Wide &amp; Deep Learning for Recommender Systems 搜广推与 LLM 应用 Google 2016-06-24 纯线性模型善于记忆稀疏共现但泛化弱，纯 DNN 能泛化却可能推荐不相关组合。论文联合训练两路并共享最终 logit。 Fidelity: 核心机制复现。本地实现联合记忆型 wide 交叉与泛化型 deep tower。公开 MovieLens 替代 Google Play 私有日志；未复刻生产特征工程、分布式训练与 serving。本地对照口径：基线是参数匹配的 deep-only 模型；实验组加入 candidate 与 genre 交叉的 wide 路径；MovieLens-100K 三 seed 全库 NDCG@10 相对 +5.45%。  ranking classic feature-interaction 搜广推 用户历史与排序骨干 wide记忆与deep泛化为何可能各有失败？ 记忆难覆盖未见组合，泛化可能把看似相似但不相关组合推高。互补动机不保证任一任务都需要相同容量，需检查数据稀疏性与特征工程。 例如某品牌和配件的特定兼容关系，不能只凭语义近就推荐。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-67f85dbf50d8bc49">wide记忆与deep泛化为何可能各有失败？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Awide-deep">Wide &amp; Deep Learning for Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>记忆难覆盖未见组合，泛化可能把看似相似但不相关组合推高。互补动机不保证任一任务都需要相同容量，需检查数据稀疏性与特征工程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某品牌和配件的特定兼容关系，不能只凭语义近就推荐。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1606.07792">原论文</a> · <a href="../../../../reproductions/1606.07792-wide-deep/">实现解读</a> · <a href="#qa-67f85dbf50d8bc49">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="recommendation:wide-deep" data-paper-title="Wide &amp; Deep Learning for Recommender Systems" data-learning-pending="false" data-level="implementation" data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/history-ranking-backbones" data-search="Wide &amp; Deep Learning for Recommender Systems 搜广推与 LLM 应用 Google 2016-06-24 纯线性模型善于记忆稀疏共现但泛化弱，纯 DNN 能泛化却可能推荐不相关组合。论文联合训练两路并共享最终 logit。 Fidelity: 核心机制复现。本地实现联合记忆型 wide 交叉与泛化型 deep tower。公开 MovieLens 替代 Google Play 私有日志；未复刻生产特征工程、分布式训练与 serving。本地对照口径：基线是参数匹配的 deep-only 模型；实验组加入 candidate 与 genre 交叉的 wide 路径；MovieLens-100K 三 seed 全库 NDCG@10 相对 +5.45%。  ranking classic feature-interaction 搜广推 用户历史与排序骨干 本地Wide &amp; Deep是否使用Google Play生产交叉特征？ 没有，MovieLens替代私有日志，未复刻分布式训练serving。两路logit应在sigmoid前相加联合更新，不能先各自变概率再平均后声称同公式。 例如sigmoid(a+b)一般不等于两个sigmoid概率的平均。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 用户历史与排序骨干</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a065020fe4b932b1">本地Wide &amp; Deep是否使用Google Play生产交叉特征？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=recommendation%3Awide-deep">Wide &amp; Deep Learning for Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有，MovieLens替代私有日志，未复刻分布式训练serving。两路logit应在sigmoid前相加联合更新，不能先各自变概率再平均后声称同公式。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如sigmoid(a+b)一般不等于两个sigmoid概率的平均。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/1606.07792">原论文</a> · <a href="../../../../reproductions/1606.07792-wide-deep/">实现解读</a> · <a href="#qa-a065020fe4b932b1">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

计算预算应该花在历史内部、候选与历史，还是异构字段之间？

## 记住这一点

先分清交互对象：DIN按候选激活相关历史；HSTU让输入窗口中的历史状态逐层交互；RankMixer用固定TokenMix和独立FFN处理异构特征。长历史压缩、统一序列与字段、稀疏注意力以及预训练迁移，都在选择保留什么状态、何时交换信息。不同骨干可互补，不能仅凭都有Transformer就视为同一路线。

## 一个例子

用户长期喜欢园艺，最近连续看猫视频。推荐猫粮时，候选条件化读历史可以关注近期养猫线索；推荐园艺工具时则要找回远期兴趣。随后还要把价格、场景和用户字段一起交叉，历史建模与字段交互各自承担不同工作。

## 什么时候要小心

字段token数与历史长度不是同一变量，不能直接比较两张复杂度表。缓存只有在状态不依赖当前候选时才可共享。短历史公开数据上的正负结果，都不能单独证明工业长序列效果或生产吞吐。

## 先读这几篇

先读 DIN 辨认候选条件化兴趣，再读 HSTU 理解历史状态如何逐层变化，最后读 RankMixer 区分字段交互；再看[本主题精读对比](../../deep-dives/recommendation/history-ranking-backbones.md)，比较 LONGER 的短查询路径与 SlimPer 的固定用户池。本地结果以各自数据与保真度为限。

1. [Deep Interest Network for Click-Through Rate Prediction](../../../reproductions/1706.06978-din/README.md) · [原论文](https://arxiv.org/abs/1706.06978)
2. [Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations](../../../reproductions/2402.17152-hstu/README.md) · [原论文](https://arxiv.org/abs/2402.17152)
3. [RankMixer: Scaling Up Ranking Models in Industrial Recommenders](../../../reproductions/2507.15551-rankmixer/README.md) · [原论文](https://arxiv.org/abs/2507.15551)

## 自测一下

一个用户状态已经读过候选A的信息，还能原样作为候选B的共享用户缓存吗？

??? note "展开参考答案"

    通常不能。该状态已依赖A，会污染B的计算。需要保持候选无关的共享路径，或明确重新计算候选相关部分；只给模块起名为用户塔并不能保证可复用。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
