---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 世界建模：状态、生成与动作条件

[多模态](index.md) / 149 个问题 · 37 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

[阅读本主题精读卡片：多篇论文对比、分析与问答](../../deep-dives/multimodal-models/world-state-actions.md)

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
<p class="ar-learning-status" data-learning-status role="status">149 个问题 · 37 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:criticjepa" data-paper-title="CriticJEPA: World Models Are Better Critics Than Optimizers" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="CriticJEPA: World Models Are Better Critics Than Optimizers 基础模型 Tsinghua University 2026-11-24 对一个预测器找到更低的预测 cost，需要其梯度方向可靠；从一组好候选中挑更好的，只要求局部排序有信息。论文在冻结 H-JEPA 上观察到：长梯度搜索可继续降低预测 cost，但实际行动不再改善；同一预测器却能比较 goal-conditioned 提案。CriticJEPA 在每个时间层级训练 flow proposer，再用冻结 rollout 选择；只给提案做短的有锚精修，而不让无约束搜索承担整个规划。 成本过高，不复现（审查 DONE）。仅审查收录，无本地代码、无环境实跑、无 CPU/CUDA 机制代理、无本地成功率。此页与成本审查记录只保存来源、方法和高成本边界，不设 metrics 目录；论文表格不是本地测量，也不需要为此收录伪造 GPU receipt。  JEPA与世界模型 提案选择与有锚规划 多模态 世界建模：状态、生成与动作条件 能正确比较两个计划，就表示世界模型梯度能持续改进动作吗？ 不表示。排序仅需候选间相对评分有信息；优化需要沿局部梯度移动也改善真实执行。持续搜索还可能利用预测误差。 教学例：模型把安全绕行排在撞墙前，仍可能在绕行附近沿错误梯度把动作推向墙；该例说明逻辑差异，不是论文实测轨迹。 2026-11-25">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-criticjepa-1e87f1a4" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-05295c40f0825d92">能正确比较两个计划，就表示世界模型梯度能持续改进动作吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Acriticjepa">CriticJEPA: World Models Are Better Critics Than Optimizers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-25 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不表示。排序仅需候选间相对评分有信息；优化需要沿局部梯度移动也改善真实执行。持续搜索还可能利用预测误差。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：模型把安全绕行排在撞墙前，仍可能在绕行附近沿错误梯度把动作推向墙；该例说明逻辑差异，不是论文实测轨迹。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、同主题比较与边界、数据协议与代码映射、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.32357v1">原论文</a> · <a href="../../../../foundation-models/2611.32357-criticjepa/">实现解读</a> · <a href="#qa-05295c40f0825d92">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:criticjepa" data-paper-title="CriticJEPA: World Models Are Better Critics Than Optimizers" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="CriticJEPA: World Models Are Better Critics Than Optimizers 基础模型 Tsinghua University 2026-11-24 对一个预测器找到更低的预测 cost，需要其梯度方向可靠；从一组好候选中挑更好的，只要求局部排序有信息。论文在冻结 H-JEPA 上观察到：长梯度搜索可继续降低预测 cost，但实际行动不再改善；同一预测器却能比较 goal-conditioned 提案。CriticJEPA 在每个时间层级训练 flow proposer，再用冻结 rollout 选择；只给提案做短的有锚精修，而不让无约束搜索承担整个规划。 成本过高，不复现（审查 DONE）。仅审查收录，无本地代码、无环境实跑、无 CPU/CUDA 机制代理、无本地成功率。此页与成本审查记录只保存来源、方法和高成本边界，不设 metrics 目录；论文表格不是本地测量，也不需要为此收录伪造 GPU receipt。  JEPA与世界模型 提案选择与有锚规划 多模态 世界建模：状态、生成与动作条件 anchor惩罚为什么不留在最终选择cost里？ anchor限制每个候选偏离自身提案的距离，用于局部精修；最终需要比较实际rollout目标cost，而不是奖励离初始候选更近。 教学例：A的rollout cost为1但移动0.5，B为2但未移动；最终应选A，不能因为A离提案远就让anchor翻转排名。 2026-11-25">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-7b63e892e0032e2f">anchor惩罚为什么不留在最终选择cost里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Acriticjepa">CriticJEPA: World Models Are Better Critics Than Optimizers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-25 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>anchor限制每个候选偏离自身提案的距离，用于局部精修；最终需要比较实际rollout目标cost，而不是奖励离初始候选更近。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：A的rollout cost为1但移动0.5，B为2但未移动；最终应选A，不能因为A离提案远就让anchor翻转排名。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、同主题比较与边界、数据协议与代码映射、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.32357v1">原论文</a> · <a href="../../../../foundation-models/2611.32357-criticjepa/">实现解读</a> · <a href="#qa-7b63e892e0032e2f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:criticjepa" data-paper-title="CriticJEPA: World Models Are Better Critics Than Optimizers" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="CriticJEPA: World Models Are Better Critics Than Optimizers 基础模型 Tsinghua University 2026-11-24 对一个预测器找到更低的预测 cost，需要其梯度方向可靠；从一组好候选中挑更好的，只要求局部排序有信息。论文在冻结 H-JEPA 上观察到：长梯度搜索可继续降低预测 cost，但实际行动不再改善；同一预测器却能比较 goal-conditioned 提案。CriticJEPA 在每个时间层级训练 flow proposer，再用冻结 rollout 选择；只给提案做短的有锚精修，而不让无约束搜索承担整个规划。 成本过高，不复现（审查 DONE）。仅审查收录，无本地代码、无环境实跑、无 CPU/CUDA 机制代理、无本地成功率。此页与成本审查记录只保存来源、方法和高成本边界，不设 metrics 目录；论文表格不是本地测量，也不需要为此收录伪造 GPU receipt。  JEPA与世界模型 提案选择与有锚规划 多模态 世界建模：状态、生成与动作条件 CriticJEPA比预测—规划评测多区分了什么？ 前者在同一冻结模型里改变候选来源与搜索方式，区分能否排序、梯度是否有效和环境成功；后者用冻结解码协议拆表示与预测误差，并单独要求真实规划结果。 教学例：一步误差相同的模型可对flow提案有用、对长搜索生成的离分布候选无用；因此不能仅按一步loss选规划器。 2026-11-25">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1055275115f6ef1d">CriticJEPA比预测—规划评测多区分了什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Acriticjepa">CriticJEPA: World Models Are Better Critics Than Optimizers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-25 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者在同一冻结模型里改变候选来源与搜索方式，区分能否排序、梯度是否有效和环境成功；后者用冻结解码协议拆表示与预测误差，并单独要求真实规划结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：一步误差相同的模型可对flow提案有用、对长搜索生成的离分布候选无用；因此不能仅按一步loss选规划器。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、同主题比较与边界、数据协议与代码映射、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.32357v1">原论文</a> · <a href="../../../../foundation-models/2611.32357-criticjepa/">实现解读</a> · <a href="#qa-1055275115f6ef1d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:criticjepa" data-paper-title="CriticJEPA: World Models Are Better Critics Than Optimizers" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="CriticJEPA: World Models Are Better Critics Than Optimizers 基础模型 Tsinghua University 2026-11-24 对一个预测器找到更低的预测 cost，需要其梯度方向可靠；从一组好候选中挑更好的，只要求局部排序有信息。论文在冻结 H-JEPA 上观察到：长梯度搜索可继续降低预测 cost，但实际行动不再改善；同一预测器却能比较 goal-conditioned 提案。CriticJEPA 在每个时间层级训练 flow proposer，再用冻结 rollout 选择；只给提案做短的有锚精修，而不让无约束搜索承担整个规划。 成本过高，不复现（审查 DONE）。仅审查收录，无本地代码、无环境实跑、无 CPU/CUDA 机制代理、无本地成功率。此页与成本审查记录只保存来源、方法和高成本边界，不设 metrics 目录；论文表格不是本地测量，也不需要为此收录伪造 GPU receipt。  JEPA与世界模型 提案选择与有锚规划 多模态 世界建模：状态、生成与动作条件 用预先写好的好动作候选能算低成本CriticJEPA复现吗？ 不能。conditional flow的训练、生成及跨层目标/时间窗决定候选分布，是核心机制。固定候选可诊断critic接口，但不能声称复现提案能力；完整矩阵已按成本终态不复现。 教学例：手填一条到目标的动作再让critic选中，只证明列表里有答案；本地因此不写这种可执行operator，也不报告控制成功率。 2026-11-25">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-4e9e6417175d8206">用预先写好的好动作候选能算低成本CriticJEPA复现吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Acriticjepa">CriticJEPA: World Models Are Better Critics Than Optimizers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-25 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。conditional flow的训练、生成及跨层目标/时间窗决定候选分布，是核心机制。固定候选可诊断critic接口，但不能声称复现提案能力；完整矩阵已按成本终态不复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：手填一条到目标的动作再让critic选中，只证明列表里有答案；本地因此不写这种可执行operator，也不报告控制成功率。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、同主题比较与边界、数据协议与代码映射、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.32357v1">原论文</a> · <a href="../../../../foundation-models/2611.32357-criticjepa/">实现解读</a> · <a href="#qa-4e9e6417175d8206">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:counterfactual-wm" data-paper-title="Counterfactual World Models: JEPAs That Reason About &quot;What If&quot;" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Counterfactual World Models: JEPAs That Reason About &quot;What If&quot; 基础模型 Brown University / AMI Labs 2026-11-18 普通world model给动作的平均结果，不能仅凭更准的事实分布识别同一扰动下的个体反事实。本文将实际观测结果作为事件信息，加上同一事实预测器对两个动作的预测差；加性扰动时精确，平滑短时动力学下有交互误差界，但碰撞、乘法故障和弯曲坐标可破坏近似。Fixed-v1 source. 不是完整模型. 完整实验：成本过高，不复现（审查 DONE）。未训练JEPA、加载encoder、采集模拟轨迹或执行规划；l1_mechanism组件；不是完整模型. 完整实验：成本过高，不复现（审查 DONE）。执行Eq6残差复用和Eq7 readout坐标运输，严格拒绝隐式broadcast；加性系统验证等式，乘法gain fault与非线性readout保留预期失效。未训练JEPA、加载encoder、采集模拟轨迹或执行规划；诊断中的分析函数不冒充训练好的world model。  世界模型与JEPA 反事实预测与可识别性 多模态 世界建模：状态、生成与动作条件 为什么平均未来预测准确还不等于反事实准确？ 事实分布只给不同动作的边缘结果，没说明两种结果属于同一扰动事件的哪一对。个体反事实需要这份配对结构。 教学例：U与1-U都均匀分布，但观测U=0.2时两种耦合的替代结果分别是0.2和0.8。 2026-11-19">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-counterfactual-wm-f2e1144d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5f79bc24ae17fcbb">为什么平均未来预测准确还不等于反事实准确？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Acounterfactual-wm">Counterfactual World Models: JEPAs That Reason About &quot;What If&quot;</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-19 · Brown University / AMI Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>事实分布只给不同动作的边缘结果，没说明两种结果属于同一扰动事件的哪一对。个体反事实需要这份配对结构。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：U与1-U都均匀分布，但观测U=0.2时两种耦合的替代结果分别是0.2和0.8。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、同主题比较与边界、数据协议与代码映射、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.24778v1">原论文</a> · <a href="../../../../foundation-models/2611.24778-counterfactual-wm/">实现解读</a> · <a href="#qa-5f79bc24ae17fcbb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:counterfactual-wm" data-paper-title="Counterfactual World Models: JEPAs That Reason About &quot;What If&quot;" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Counterfactual World Models: JEPAs That Reason About &quot;What If&quot; 基础模型 Brown University / AMI Labs 2026-11-18 普通world model给动作的平均结果，不能仅凭更准的事实分布识别同一扰动下的个体反事实。本文将实际观测结果作为事件信息，加上同一事实预测器对两个动作的预测差；加性扰动时精确，平滑短时动力学下有交互误差界，但碰撞、乘法故障和弯曲坐标可破坏近似。Fixed-v1 source. 不是完整模型. 完整实验：成本过高，不复现（审查 DONE）。未训练JEPA、加载encoder、采集模拟轨迹或执行规划；l1_mechanism组件；不是完整模型. 完整实验：成本过高，不复现（审查 DONE）。执行Eq6残差复用和Eq7 readout坐标运输，严格拒绝隐式broadcast；加性系统验证等式，乘法gain fault与非线性readout保留预期失效。未训练JEPA、加载encoder、采集模拟轨迹或执行规划；诊断中的分析函数不冒充训练好的world model。  世界模型与JEPA 反事实预测与可识别性 多模态 世界建模：状态、生成与动作条件 残差复用到底复用了什么？ 复用事实观测与事实预测之差，再加到替代动作预测上；无需恢复真实扰动变量。只在动作与扰动的交互足够小等条件下可靠。 教学例：原预测向东1米，实测1.3米；替代预测向北1米时保留这次事件的0.3米漂移。 2026-11-19">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-4441583312b3f382">残差复用到底复用了什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Acounterfactual-wm">Counterfactual World Models: JEPAs That Reason About &quot;What If&quot;</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-19 · Brown University / AMI Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>复用事实观测与事实预测之差，再加到替代动作预测上；无需恢复真实扰动变量。只在动作与扰动的交互足够小等条件下可靠。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：原预测向东1米，实测1.3米；替代预测向北1米时保留这次事件的0.3米漂移。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、同主题比较与边界、数据协议与代码映射、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.24778v1">原论文</a> · <a href="../../../../foundation-models/2611.24778-counterfactual-wm/">实现解读</a> · <a href="#qa-4441583312b3f382">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:counterfactual-wm" data-paper-title="Counterfactual World Models: JEPAs That Reason About &quot;What If&quot;" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Counterfactual World Models: JEPAs That Reason About &quot;What If&quot; 基础模型 Brown University / AMI Labs 2026-11-18 普通world model给动作的平均结果，不能仅凭更准的事实分布识别同一扰动下的个体反事实。本文将实际观测结果作为事件信息，加上同一事实预测器对两个动作的预测差；加性扰动时精确，平滑短时动力学下有交互误差界，但碰撞、乘法故障和弯曲坐标可破坏近似。Fixed-v1 source. 不是完整模型. 完整实验：成本过高，不复现（审查 DONE）。未训练JEPA、加载encoder、采集模拟轨迹或执行规划；l1_mechanism组件；不是完整模型. 完整实验：成本过高，不复现（审查 DONE）。执行Eq6残差复用和Eq7 readout坐标运输，严格拒绝隐式broadcast；加性系统验证等式，乘法gain fault与非线性readout保留预期失效。未训练JEPA、加载encoder、采集模拟轨迹或执行规划；诊断中的分析函数不冒充训练好的world model。  世界模型与JEPA 反事实预测与可识别性 多模态 世界建模：状态、生成与动作条件 与DT-JEPA查询时的信息有什么不同？ DT-JEPA用行动前历史预测未来；CWM需已执行事实动作的结果。允许的信息集和问题不同，不能比较为同一预测任务。 教学例：第一次执行动作前不能拿尚不存在的observed_outcome喂CWM。 2026-11-19">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-3ea4e66199ef2d91">与DT-JEPA查询时的信息有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Acounterfactual-wm">Counterfactual World Models: JEPAs That Reason About &quot;What If&quot;</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-19 · Brown University / AMI Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>DT-JEPA用行动前历史预测未来；CWM需已执行事实动作的结果。允许的信息集和问题不同，不能比较为同一预测任务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：第一次执行动作前不能拿尚不存在的observed_outcome喂CWM。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、同主题比较与边界、数据协议与代码映射、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.24778v1">原论文</a> · <a href="../../../../foundation-models/2611.24778-counterfactual-wm/">实现解读</a> · <a href="#qa-3ea4e66199ef2d91">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:counterfactual-wm" data-paper-title="Counterfactual World Models: JEPAs That Reason About &quot;What If&quot;" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Counterfactual World Models: JEPAs That Reason About &quot;What If&quot; 基础模型 Brown University / AMI Labs 2026-11-18 普通world model给动作的平均结果，不能仅凭更准的事实分布识别同一扰动下的个体反事实。本文将实际观测结果作为事件信息，加上同一事实预测器对两个动作的预测差；加性扰动时精确，平滑短时动力学下有交互误差界，但碰撞、乘法故障和弯曲坐标可破坏近似。Fixed-v1 source. 不是完整模型. 完整实验：成本过高，不复现（审查 DONE）。未训练JEPA、加载encoder、采集模拟轨迹或执行规划；l1_mechanism组件；不是完整模型. 完整实验：成本过高，不复现（审查 DONE）。执行Eq6残差复用和Eq7 readout坐标运输，严格拒绝隐式broadcast；加性系统验证等式，乘法gain fault与非线性readout保留预期失效。未训练JEPA、加载encoder、采集模拟轨迹或执行规划；诊断中的分析函数不冒充训练好的world model。  世界模型与JEPA 反事实预测与可识别性 多模态 世界建模：状态、生成与动作条件 为什么测试里应保留乘法故障的非零误差？ 该故障使扰动与动作相乘，个体动作效应随事件变化，违反共享加性残差条件。清掉误差会掩盖论文已说明的边界。 教学例：实际执行只有命令的50%时，原动作残差不能无条件照搬到两倍命令上。 2026-11-19">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e06f52cb0a81dd08">为什么测试里应保留乘法故障的非零误差？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Acounterfactual-wm">Counterfactual World Models: JEPAs That Reason About &quot;What If&quot;</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-19 · Brown University / AMI Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>该故障使扰动与动作相乘，个体动作效应随事件变化，违反共享加性残差条件。清掉误差会掩盖论文已说明的边界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：实际执行只有命令的50%时，原动作残差不能无条件照搬到两倍命令上。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、同主题比较与边界、数据协议与代码映射、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.24778v1">原论文</a> · <a href="../../../../foundation-models/2611.24778-counterfactual-wm/">实现解读</a> · <a href="#qa-e06f52cb0a81dd08">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mv-jepa" data-paper-title="MV-JEPA: Post-Training Video Encoders for Cross-View Understanding" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="MV-JEPA: Post-Training Video Encoders for Cross-View Understanding 基础模型 University of Minnesota, Twin Cities 2026-11-18 MV-JEPA直接后训练已有JEPA视频编码器，强化不同摄像头视角之间的对象/时刻对应。共享student分别编码各context view的可见token；联合predictor利用所有context特征，既重建被mask的context位置，又预测一个完全held-out视图。held-out图像/特征从不进入student或predictor，只提供teacher目标；推理仍可独立编码单视角。 完整实验：成本过高，不复现（审查 DONE）。诊断检查隔离与梯度，不是视觉能力或Evolve证据。L1策略/训练连线组件，不是完整论文复现。完整实验：成本过高，不复现（审查 DONE）。实现真实小型shared self-attention encoder、独立context编码、联合predictor、两种query、互异view ID、teacher-only held-out、Eq4损失、共享单视图replay和显式EMA。输入为人工构造token特征，不是像素，不加载V-JEPA权重；位置编码是声明过的tiny一维正弦码，不冒充原生时空position。  JEPA与世界模型 跨视角表征与预测后训练 多模态 世界建模：状态、生成与动作条件 held-out视图是多给student一台摄像头吗？ 不是。它只由teacher产生目标；student和predictor必须根据其他context视图推断它，推理时也不要求该额外观察。 教学例：遮住背面照片，只给正面和侧面；背面latent只在loss端使用。 2026-11-21">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-mv-jepa-faca4e13" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-860ec1807e0faebf">held-out视图是多给student一台摄像头吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amv-jepa">MV-JEPA: Post-Training Video Encoders for Cross-View Understanding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-21 · University of Minnesota, Twin Cities</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。它只由teacher产生目标；student和predictor必须根据其他context视图推断它，推理时也不要求该额外观察。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：遮住背面照片，只给正面和侧面；背面latent只在loss端使用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、数据协议与代码映射、同主题比较与边界、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.25172v1">原论文</a> · <a href="../../../../foundation-models/2611.25172-mv-jepa/">实现解读</a> · <a href="#qa-860ec1807e0faebf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mv-jepa" data-paper-title="MV-JEPA: Post-Training Video Encoders for Cross-View Understanding" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="MV-JEPA: Post-Training Video Encoders for Cross-View Understanding 基础模型 University of Minnesota, Twin Cities 2026-11-18 MV-JEPA直接后训练已有JEPA视频编码器，强化不同摄像头视角之间的对象/时刻对应。共享student分别编码各context view的可见token；联合predictor利用所有context特征，既重建被mask的context位置，又预测一个完全held-out视图。held-out图像/特征从不进入student或predictor，只提供teacher目标；推理仍可独立编码单视角。 完整实验：成本过高，不复现（审查 DONE）。诊断检查隔离与梯度，不是视觉能力或Evolve证据。L1策略/训练连线组件，不是完整论文复现。完整实验：成本过高，不复现（审查 DONE）。实现真实小型shared self-attention encoder、独立context编码、联合predictor、两种query、互异view ID、teacher-only held-out、Eq4损失、共享单视图replay和显式EMA。输入为人工构造token特征，不是像素，不加载V-JEPA权重；位置编码是声明过的tiny一维正弦码，不冒充原生时空position。  JEPA与世界模型 跨视角表征与预测后训练 多模态 世界建模：状态、生成与动作条件 为什么Eq4不能先对每个view的loss求平均？ mask数量可能不同；论文给每个监督token同等权重，而不是每个view同等权重。还要先逐example归一化，再平均batch。 教学例：两个context各1和3个mask，加held-out4个token；总共8个目标等权，不是三组各占三分之一。 2026-11-21">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-49a32e076c487037">为什么Eq4不能先对每个view的loss求平均？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amv-jepa">MV-JEPA: Post-Training Video Encoders for Cross-View Understanding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-21 · University of Minnesota, Twin Cities</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>mask数量可能不同；论文给每个监督token同等权重，而不是每个view同等权重。还要先逐example归一化，再平均batch。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：两个context各1和3个mask，加held-out4个token；总共8个目标等权，不是三组各占三分之一。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、数据协议与代码映射、同主题比较与边界、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.25172v1">原论文</a> · <a href="../../../../foundation-models/2611.25172-mv-jepa/">实现解读</a> · <a href="#qa-49a32e076c487037">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mv-jepa" data-paper-title="MV-JEPA: Post-Training Video Encoders for Cross-View Understanding" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="MV-JEPA: Post-Training Video Encoders for Cross-View Understanding 基础模型 University of Minnesota, Twin Cities 2026-11-18 MV-JEPA直接后训练已有JEPA视频编码器，强化不同摄像头视角之间的对象/时刻对应。共享student分别编码各context view的可见token；联合predictor利用所有context特征，既重建被mask的context位置，又预测一个完全held-out视图。held-out图像/特征从不进入student或predictor，只提供teacher目标；推理仍可独立编码单视角。 完整实验：成本过高，不复现（审查 DONE）。诊断检查隔离与梯度，不是视觉能力或Evolve证据。L1策略/训练连线组件，不是完整论文复现。完整实验：成本过高，不复现（审查 DONE）。实现真实小型shared self-attention encoder、独立context编码、联合predictor、两种query、互异view ID、teacher-only held-out、Eq4损失、共享单视图replay和显式EMA。输入为人工构造token特征，不是像素，不加载V-JEPA权重；位置编码是声明过的tiny一维正弦码，不冒充原生时空position。  JEPA与世界模型 跨视角表征与预测后训练 多模态 世界建模：状态、生成与动作条件 MV-JEPA和Time-JEPA都用额外监督，目标能互换吗？ 不能。前者是跨摄像头latent并需要联合view predictor；后者是对齐物理时序并有unmasked回归分支。二者训练目标都不应变成student输入。 教学例：速度标量属于Time-JEPA物理head，背面视图的一组token属于MV-JEPA held-out query；换标签不等于同一任务。 2026-11-21">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d6b9990bfc0ac635">MV-JEPA和Time-JEPA都用额外监督，目标能互换吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amv-jepa">MV-JEPA: Post-Training Video Encoders for Cross-View Understanding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-21 · University of Minnesota, Twin Cities</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。前者是跨摄像头latent并需要联合view predictor；后者是对齐物理时序并有unmasked回归分支。二者训练目标都不应变成student输入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：速度标量属于Time-JEPA物理head，背面视图的一组token属于MV-JEPA held-out query；换标签不等于同一任务。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、数据协议与代码映射、同主题比较与边界、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.25172v1">原论文</a> · <a href="../../../../foundation-models/2611.25172-mv-jepa/">实现解读</a> · <a href="#qa-d6b9990bfc0ac635">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mv-jepa" data-paper-title="MV-JEPA: Post-Training Video Encoders for Cross-View Understanding" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="MV-JEPA: Post-Training Video Encoders for Cross-View Understanding 基础模型 University of Minnesota, Twin Cities 2026-11-18 MV-JEPA直接后训练已有JEPA视频编码器，强化不同摄像头视角之间的对象/时刻对应。共享student分别编码各context view的可见token；联合predictor利用所有context特征，既重建被mask的context位置，又预测一个完全held-out视图。held-out图像/特征从不进入student或predictor，只提供teacher目标；推理仍可独立编码单视角。 完整实验：成本过高，不复现（审查 DONE）。诊断检查隔离与梯度，不是视觉能力或Evolve证据。L1策略/训练连线组件，不是完整论文复现。完整实验：成本过高，不复现（审查 DONE）。实现真实小型shared self-attention encoder、独立context编码、联合predictor、两种query、互异view ID、teacher-only held-out、Eq4损失、共享单视图replay和显式EMA。输入为人工构造token特征，不是像素，不加载V-JEPA权重；位置编码是声明过的tiny一维正弦码，不冒充原生时空position。  JEPA与世界模型 跨视角表征与预测后训练 多模态 世界建模：状态、生成与动作条件 怎样检查held-out和masked context没有偷进student？ 固定view ID，任意改held-out内容或被mask的context token，predictor输出应不变；这些改动可改变teacher目标/loss，但不能产生held-out输入梯度。teacher参数也必须无梯度，只做显式EMA。 教学例：把held-out token乘30后，预测不变而目标可变；若预测变化，就有训练输入泄漏。 2026-11-21">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-68b29514f7878f8e">怎样检查held-out和masked context没有偷进student？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amv-jepa">MV-JEPA: Post-Training Video Encoders for Cross-View Understanding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-21 · University of Minnesota, Twin Cities</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定view ID，任意改held-out内容或被mask的context token，predictor输出应不变；这些改动可改变teacher目标/loss，但不能产生held-out输入梯度。teacher参数也必须无梯度，只做显式EMA。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：把held-out token乘30后，预测不变而目标可变；若预测变化，就有训练输入泄漏。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、数据协议与代码映射、同主题比较与边界、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.25172v1">原论文</a> · <a href="../../../../foundation-models/2611.25172-mv-jepa/">实现解读</a> · <a href="#qa-68b29514f7878f8e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:jepa-dots" data-paper-title="JEPA Dots: Dual-Latent World Model for Language-Guided Robot Control" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="JEPA Dots: Dual-Latent World Model for Language-Guided Robot Control 多模态大模型 Z Robotics 2026-11-18 共享视觉骨干之后拆动力学和任务两条latent路径，语言FiLM只进入任务路径。world query只读动力学历史和给定clean动作，policy读历史、goal和noisy动作；多层mask同时阻断间接泄漏。固定参数、观测和给定动作时，换指令不能改变world预测，但policy可以生成不同动作。 无实现. 完整实验：成本过高，不复现（审查 DONE）。仅资料收录；无实现. 完整实验：成本过高，不复现（审查 DONE）。仅资料、公式、机构及成本收录，无operator、训练、LIBERO安装、机器人执行、metrics或GPU回执。不得用一个语言无关函数的恒等式fixture冒充完整双latent控制模型。  世界模型 任务与动力学分离 多模态 世界建模：状态、生成与动作条件 为什么相同观测和动作下world预测不该因语言改变？ 语言描述的是任务目标，不应改变这些已固定动作的物理后果；因此语言只进入task/policy而非world动力学通路。 教学例：同样向左移动夹爪，指令改成拿杯子不应让固定动作的预测位移突然向右。 2026-11-19">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-multimodal-models-jepa-dots-ebbd7b0b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-569ecbc969dd991d">为什么相同观测和动作下world预测不该因语言改变？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Ajepa-dots">JEPA Dots: Dual-Latent World Model for Language-Guided Robot Control</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-19 · Z Robotics</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语言描述的是任务目标，不应改变这些已固定动作的物理后果；因此语言只进入task/policy而非world动力学通路。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：同样向左移动夹爪，指令改成拿杯子不应让固定动作的预测位移突然向右。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、数据协议与代码映射、同主题比较与边界、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.24062v1">原论文</a> · <a href="../../../../multimodal-models/2611.24062-jepa-dots/">实现解读</a> · <a href="#qa-569ecbc969dd991d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:jepa-dots" data-paper-title="JEPA Dots: Dual-Latent World Model for Language-Guided Robot Control" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="JEPA Dots: Dual-Latent World Model for Language-Guided Robot Control 多模态大模型 Z Robotics 2026-11-18 共享视觉骨干之后拆动力学和任务两条latent路径，语言FiLM只进入任务路径。world query只读动力学历史和给定clean动作，policy读历史、goal和noisy动作；多层mask同时阻断间接泄漏。固定参数、观测和给定动作时，换指令不能改变world预测，但policy可以生成不同动作。 无实现. 完整实验：成本过高，不复现（审查 DONE）。仅资料收录；无实现. 完整实验：成本过高，不复现（审查 DONE）。仅资料、公式、机构及成本收录，无operator、训练、LIBERO安装、机器人执行、metrics或GPU回执。不得用一个语言无关函数的恒等式fixture冒充完整双latent控制模型。  世界模型 任务与动力学分离 多模态 世界建模：状态、生成与动作条件 隔离goal token是否足以防止泄漏？ 还需限制中间token的多层信息通路；只在最后一层屏蔽直接goal边，不保证前层信息没进入world可见token。 教学例：history token先读goal，再被world读到，会产生间接语言通道。 2026-11-19">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8f46ae596ce78656">隔离goal token是否足以防止泄漏？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Ajepa-dots">JEPA Dots: Dual-Latent World Model for Language-Guided Robot Control</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-19 · Z Robotics</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>还需限制中间token的多层信息通路；只在最后一层屏蔽直接goal边，不保证前层信息没进入world可见token。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：history token先读goal，再被world读到，会产生间接语言通道。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、数据协议与代码映射、同主题比较与边界、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.24062v1">原论文</a> · <a href="../../../../multimodal-models/2611.24062-jepa-dots/">实现解读</a> · <a href="#qa-8f46ae596ce78656">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:jepa-dots" data-paper-title="JEPA Dots: Dual-Latent World Model for Language-Guided Robot Control" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="JEPA Dots: Dual-Latent World Model for Language-Guided Robot Control 多模态大模型 Z Robotics 2026-11-18 共享视觉骨干之后拆动力学和任务两条latent路径，语言FiLM只进入任务路径。world query只读动力学历史和给定clean动作，policy读历史、goal和noisy动作；多层mask同时阻断间接泄漏。固定参数、观测和给定动作时，换指令不能改变world预测，但policy可以生成不同动作。 无实现. 完整实验：成本过高，不复现（审查 DONE）。仅资料收录；无实现. 完整实验：成本过高，不复现（审查 DONE）。仅资料、公式、机构及成本收录，无operator、训练、LIBERO安装、机器人执行、metrics或GPU回执。不得用一个语言无关函数的恒等式fixture冒充完整双latent控制模型。  世界模型 任务与动力学分离 多模态 世界建模：状态、生成与动作条件 与LeWAM的world-action联学相比，部署差异是什么？ JEPA Dots world分支只供训练监督，部署执行flow policy；不能因此说它已复现LeWAM通过world模型优化动作的规划链。 教学例：生成8步动作后执行2步再观测，是receding-horizon policy，不等于对world cost做梯度规划。 2026-11-19">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d18e12bfa93f2ea4">与LeWAM的world-action联学相比，部署差异是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Ajepa-dots">JEPA Dots: Dual-Latent World Model for Language-Guided Robot Control</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-19 · Z Robotics</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>JEPA Dots world分支只供训练监督，部署执行flow policy；不能因此说它已复现LeWAM通过world模型优化动作的规划链。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：生成8步动作后执行2步再观测，是receding-horizon policy，不等于对world cost做梯度规划。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、数据协议与代码映射、同主题比较与边界、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.24062v1">原论文</a> · <a href="../../../../multimodal-models/2611.24062-jepa-dots/">实现解读</a> · <a href="#qa-d18e12bfa93f2ea4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:jepa-dots" data-paper-title="JEPA Dots: Dual-Latent World Model for Language-Guided Robot Control" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="JEPA Dots: Dual-Latent World Model for Language-Guided Robot Control 多模态大模型 Z Robotics 2026-11-18 共享视觉骨干之后拆动力学和任务两条latent路径，语言FiLM只进入任务路径。world query只读动力学历史和给定clean动作，policy读历史、goal和noisy动作；多层mask同时阻断间接泄漏。固定参数、观测和给定动作时，换指令不能改变world预测，但policy可以生成不同动作。 无实现. 完整实验：成本过高，不复现（审查 DONE）。仅资料收录；无实现. 完整实验：成本过高，不复现（审查 DONE）。仅资料、公式、机构及成本收录，无operator、训练、LIBERO安装、机器人执行、metrics或GPU回执。不得用一个语言无关函数的恒等式fixture冒充完整双latent控制模型。  世界模型 任务与动力学分离 多模态 世界建模：状态、生成与动作条件 39.1M参数为何仍不跑完整实验？ 成本主要还来自多个训练run和40任务的数千闭环episode；参数少不能抵消环境模拟与评测矩阵。 教学例：4000episode各最多600步，单模型上限即240万环境步，尚未算三run消融。 2026-11-19">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-945082160c96079c">39.1M参数为何仍不跑完整实验？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Ajepa-dots">JEPA Dots: Dual-Latent World Model for Language-Guided Robot Control</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-19 · Z Robotics</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>成本主要还来自多个训练run和40任务的数千闭环episode；参数少不能抵消环境模拟与评测矩阵。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：4000episode各最多600步，单模型上限即240万环境步，尚未算三run消融。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、数据协议与代码映射、同主题比较与边界、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.24062v1">原论文</a> · <a href="../../../../multimodal-models/2611.24062-jepa-dots/">实现解读</a> · <a href="#qa-945082160c96079c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:autoregressive-view-model" data-paper-title="Autoregressive View Model" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Autoregressive View Model 多模态大模型 Meta / University of Oxford 2026-11-17 AVM不拟合显式3D表示，而在给定相机路径下生成短视图片段。预填图像/视频与历史生成片段统一成为context；检索保持活动上下文有界。先把双向视频DiT微调为N-in-1-out的flow matching，再以自身rollout做因果tuning和蒸馏，让生成内容可回到历史中支持后续重访。Fixed-v1 source. 无实现. 完整实验：成本过高，不复现（审查 DONE）。仅资料收录；无实现. 完整实验：成本过高，不复现（审查 DONE）。仅原文方法、机构、成本与边界收录；没有operator、模型加载、训练、合成数据、metrics或GPU回执。不会用通用图像相似度/检索fixture代替14B视频模型的场景持久性。  世界模型 自回归视频与场景持久性 多模态 世界建模：状态、生成与动作条件 没有显式3D表示，AVM怎样保留可用场景信息？ 用预填和历史视图作context，并按当前相机查询检索活动子集；它是生成条件，不是拟合NeRF或高斯场景。 教学例：重访一间屋子时可检索此前生成的门和桌面视角，而不是重建一份完整mesh。 2026-11-19">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-multimodal-models-autoregressive-view-model-901ae7b6" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-06f6dbaf2649d1d5">没有显式3D表示，AVM怎样保留可用场景信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Aautoregressive-view-model">Autoregressive View Model</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-19 · Meta / University of Oxford</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用预填和历史视图作context，并按当前相机查询检索活动子集；它是生成条件，不是拟合NeRF或高斯场景。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：重访一间屋子时可检索此前生成的门和桌面视角，而不是重建一份完整mesh。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、同主题比较与边界、数据协议与代码映射、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.23417v1">原论文</a> · <a href="../../../../multimodal-models/2611.23417-autoregressive-view-model/">实现解读</a> · <a href="#qa-06f6dbaf2649d1d5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:autoregressive-view-model" data-paper-title="Autoregressive View Model" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Autoregressive View Model 多模态大模型 Meta / University of Oxford 2026-11-17 AVM不拟合显式3D表示，而在给定相机路径下生成短视图片段。预填图像/视频与历史生成片段统一成为context；检索保持活动上下文有界。先把双向视频DiT微调为N-in-1-out的flow matching，再以自身rollout做因果tuning和蒸馏，让生成内容可回到历史中支持后续重访。Fixed-v1 source. 无实现. 完整实验：成本过高，不复现（审查 DONE）。仅资料收录；无实现. 完整实验：成本过高，不复现（审查 DONE）。仅原文方法、机构、成本与边界收录；没有operator、模型加载、训练、合成数据、metrics或GPU回执。不会用通用图像相似度/检索fixture代替14B视频模型的场景持久性。  世界模型 自回归视频与场景持久性 多模态 世界建模：状态、生成与动作条件 为什么双向训练后还做自身rollout的因果tuning？ 流式后续生成会接触自己产生的历史；只在真实context训练不覆盖这类误差累积。因果tuning和蒸馏处理流式路径与少步采样。 教学例：早期生成的桌腿略偏，后续片段需在这一历史上保持或修正，而非总拿真实桌腿作context。 2026-11-19">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-6e1b313d7ae3b591">为什么双向训练后还做自身rollout的因果tuning？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Aautoregressive-view-model">Autoregressive View Model</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-19 · Meta / University of Oxford</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>流式后续生成会接触自己产生的历史；只在真实context训练不覆盖这类误差累积。因果tuning和蒸馏处理流式路径与少步采样。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：早期生成的桌腿略偏，后续片段需在这一历史上保持或修正，而非总拿真实桌腿作context。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、同主题比较与边界、数据协议与代码映射、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.23417v1">原论文</a> · <a href="../../../../multimodal-models/2611.23417-autoregressive-view-model/">实现解读</a> · <a href="#qa-6e1b313d7ae3b591">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:autoregressive-view-model" data-paper-title="Autoregressive View Model" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Autoregressive View Model 多模态大模型 Meta / University of Oxford 2026-11-17 AVM不拟合显式3D表示，而在给定相机路径下生成短视图片段。预填图像/视频与历史生成片段统一成为context；检索保持活动上下文有界。先把双向视频DiT微调为N-in-1-out的flow matching，再以自身rollout做因果tuning和蒸馏，让生成内容可回到历史中支持后续重访。Fixed-v1 source. 无实现. 完整实验：成本过高，不复现（审查 DONE）。仅资料收录；无实现. 完整实验：成本过高，不复现（审查 DONE）。仅原文方法、机构、成本与边界收录；没有operator、模型加载、训练、合成数据、metrics或GPU回执。不会用通用图像相似度/检索fixture代替14B视频模型的场景持久性。  世界模型 自回归视频与场景持久性 多模态 世界建模：状态、生成与动作条件 场景重访一致是否等于CWM的反事实能力？ 不等于。重访是在相机轨迹和生成历史下维持场景；个体反事实还需同一扰动下不同动作结果的耦合假设。 教学例：门框位置保持不变，不能说明同一阵风下船改航向会到哪里。 2026-11-19">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-3aa5c4c6e8c08b0d">场景重访一致是否等于CWM的反事实能力？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Aautoregressive-view-model">Autoregressive View Model</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-19 · Meta / University of Oxford</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不等于。重访是在相机轨迹和生成历史下维持场景；个体反事实还需同一扰动下不同动作结果的耦合假设。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：门框位置保持不变，不能说明同一阵风下船改航向会到哪里。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、同主题比较与边界、数据协议与代码映射、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.23417v1">原论文</a> · <a href="../../../../multimodal-models/2611.23417-autoregressive-view-model/">实现解读</a> · <a href="#qa-3aa5c4c6e8c08b0d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:autoregressive-view-model" data-paper-title="Autoregressive View Model" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Autoregressive View Model 多模态大模型 Meta / University of Oxford 2026-11-17 AVM不拟合显式3D表示，而在给定相机路径下生成短视图片段。预填图像/视频与历史生成片段统一成为context；检索保持活动上下文有界。先把双向视频DiT微调为N-in-1-out的flow matching，再以自身rollout做因果tuning和蒸馏，让生成内容可回到历史中支持后续重访。Fixed-v1 source. 无实现. 完整实验：成本过高，不复现（审查 DONE）。仅资料收录；无实现. 完整实验：成本过高，不复现（审查 DONE）。仅原文方法、机构、成本与边界收录；没有operator、模型加载、训练、合成数据、metrics或GPU回执。不会用通用图像相似度/检索fixture代替14B视频模型的场景持久性。  世界模型 自回归视频与场景持久性 多模态 世界建模：状态、生成与动作条件 为什么本轮不加一个检索小样例就算复现？ 检索只是AVM一部分，不能替代14B视频生成、flow训练及自rollout路径。成本门槛要求透明不复现，而不是把便宜影子程序叫完整实现。 教学例：取出相近相机的旧帧不等于生成未见区域或动态物体。 2026-11-19">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f8376f4ada5931c4">为什么本轮不加一个检索小样例就算复现？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Aautoregressive-view-model">Autoregressive View Model</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-19 · Meta / University of Oxford</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>检索只是AVM一部分，不能替代14B视频生成、flow训练及自rollout路径。成本门槛要求透明不复现，而不是把便宜影子程序叫完整实现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：取出相近相机的旧帧不等于生成未见区域或动态物体。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、同主题比较与边界、数据协议与代码映射、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.23417v1">原论文</a> · <a href="../../../../multimodal-models/2611.23417-autoregressive-view-model/">实现解读</a> · <a href="#qa-f8376f4ada5931c4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:dwd" data-paper-title="Decoding Without a Decoder: Direct Pixel Prediction from Diffusion Transformers" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Decoding Without a Decoder: Direct Pixel Prediction from Diffusion Transformers 多模态大模型 Luma AI 2026-11-17 DWD在预训练DiT最后隐状态上并联线性pixel head，原denoising head继续驱动采样，只有最后一个非零time step才由pixel head输出图像/视频。通过分离pixel质量目标与trajectory anchoring，避免让同一输出承担冲突目标。已核方法位置：3.1–3.4, 4.1–4.2。 完整实验成本过高，不复现（审查 DONE）；资料收录，未实现。完整实验成本过高，不复现（审查 DONE）；无能力提升或Evolve晋级声明。仅资料收录，无operator、训练、metrics、GPU receipt或Evolve映射。线性层加MSE不足以兑现像素质量、少数后缀blocks适配与采样路径，不用便宜影子模型充数。  多模态生成 扩散生成路径 多模态 世界建模：状态、生成与动作条件 DWD输出像素是否意味着每步都在像素空间采样？ 不是。latent DiT仍按原denoising head推进，只有最后一轮pixel head直接读出最终图像/视频。 教学例：中间20步仍更新latent，最后一步才把hidden token映成pixel patch。 2026-11-18">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-multimodal-models-dwd-baf72c78" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-86259de281395870">DWD输出像素是否意味着每步都在像素空间采样？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Adwd">Decoding Without a Decoder: Direct Pixel Prediction from Diffusion Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-18 · Luma AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。latent DiT仍按原denoising head推进，只有最后一轮pixel head直接读出最终图像/视频。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：中间20步仍更新latent，最后一步才把hidden token映成pixel patch。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、数据协议与代码映射、同主题比较与边界、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.22287v1">原论文</a> · <a href="../../../../multimodal-models/2611.22287-dwd/">实现解读</a> · <a href="#qa-86259de281395870">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:dwd" data-paper-title="Decoding Without a Decoder: Direct Pixel Prediction from Diffusion Transformers" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Decoding Without a Decoder: Direct Pixel Prediction from Diffusion Transformers 多模态大模型 Luma AI 2026-11-17 DWD在预训练DiT最后隐状态上并联线性pixel head，原denoising head继续驱动采样，只有最后一个非零time step才由pixel head输出图像/视频。通过分离pixel质量目标与trajectory anchoring，避免让同一输出承担冲突目标。已核方法位置：3.1–3.4, 4.1–4.2。 完整实验成本过高，不复现（审查 DONE）；资料收录，未实现。完整实验成本过高，不复现（审查 DONE）；无能力提升或Evolve晋级声明。仅资料收录，无operator、训练、metrics、GPU receipt或Evolve映射。线性层加MSE不足以兑现像素质量、少数后缀blocks适配与采样路径，不用便宜影子模型充数。  多模态生成 扩散生成路径 多模态 世界建模：状态、生成与动作条件 为何两个head不共用同一个time分布？ pixel目标工作在最终小非零time区间，trajectory anchoring覆盖更广中间去噪区间；职责不同。 教学例：原文常用pixel范围[0,0.1]、trajectory范围[0.04,1]，shift前定义。 2026-11-18">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-a99e6ac124618c8d">为何两个head不共用同一个time分布？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Adwd">Decoding Without a Decoder: Direct Pixel Prediction from Diffusion Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-18 · Luma AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>pixel目标工作在最终小非零time区间，trajectory anchoring覆盖更广中间去噪区间；职责不同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：原文常用pixel范围[0,0.1]、trajectory范围[0.04,1]，shift前定义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、数据协议与代码映射、同主题比较与边界、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.22287v1">原论文</a> · <a href="../../../../multimodal-models/2611.22287-dwd/">实现解读</a> · <a href="#qa-a99e6ac124618c8d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:dwd" data-paper-title="Decoding Without a Decoder: Direct Pixel Prediction from Diffusion Transformers" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Decoding Without a Decoder: Direct Pixel Prediction from Diffusion Transformers 多模态大模型 Luma AI 2026-11-17 DWD在预训练DiT最后隐状态上并联线性pixel head，原denoising head继续驱动采样，只有最后一个非零time step才由pixel head输出图像/视频。通过分离pixel质量目标与trajectory anchoring，避免让同一输出承担冲突目标。已核方法位置：3.1–3.4, 4.1–4.2。 完整实验成本过高，不复现（审查 DONE）；资料收录，未实现。完整实验成本过高，不复现（审查 DONE）；无能力提升或Evolve晋级声明。仅资料收录，无operator、训练、metrics、GPU receipt或Evolve映射。线性层加MSE不足以兑现像素质量、少数后缀blocks适配与采样路径，不用便宜影子模型充数。  多模态生成 扩散生成路径 多模态 世界建模：状态、生成与动作条件 和PixVid都去掉decoder，有何关键不同？ PixVid迁移输入与整个pixel生成路径，DWD保留latent denoising加最终输出head；改动范围和监督不同。 教学例：删除VAE后直接换线性输出，不会自动获得PixVid的时间映射/detailer。 2026-11-18">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7c24bb38fd70015c">和PixVid都去掉decoder，有何关键不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Adwd">Decoding Without a Decoder: Direct Pixel Prediction from Diffusion Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-18 · Luma AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>PixVid迁移输入与整个pixel生成路径，DWD保留latent denoising加最终输出head；改动范围和监督不同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：删除VAE后直接换线性输出，不会自动获得PixVid的时间映射/detailer。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、数据协议与代码映射、同主题比较与边界、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.22287v1">原论文</a> · <a href="../../../../multimodal-models/2611.22287-dwd/">实现解读</a> · <a href="#qa-7c24bb38fd70015c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:dwd" data-paper-title="Decoding Without a Decoder: Direct Pixel Prediction from Diffusion Transformers" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Decoding Without a Decoder: Direct Pixel Prediction from Diffusion Transformers 多模态大模型 Luma AI 2026-11-17 DWD在预训练DiT最后隐状态上并联线性pixel head，原denoising head继续驱动采样，只有最后一个非零time step才由pixel head输出图像/视频。通过分离pixel质量目标与trajectory anchoring，避免让同一输出承担冲突目标。已核方法位置：3.1–3.4, 4.1–4.2。 完整实验成本过高，不复现（审查 DONE）；资料收录，未实现。完整实验成本过高，不复现（审查 DONE）；无能力提升或Evolve晋级声明。仅资料收录，无operator、训练、metrics、GPU receipt或Evolve映射。线性层加MSE不足以兑现像素质量、少数后缀blocks适配与采样路径，不用便宜影子模型充数。  多模态生成 扩散生成路径 多模态 世界建模：状态、生成与动作条件 为何本轮不只实现一个线性pixel head？ 完整作用依赖预训练DiT后缀适配、感知/对抗目标、trajectory anchoring和采样。独立线性层没有足够方法证据，完整矩阵高成本故只收录。 教学例：随机hidden映射到RGB的shape正确，不代表具备无decoder生成能力。 2026-11-18">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1e6dfdc48c592cb4">为何本轮不只实现一个线性pixel head？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Adwd">Decoding Without a Decoder: Direct Pixel Prediction from Diffusion Transformers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-18 · Luma AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>完整作用依赖预训练DiT后缀适配、感知/对抗目标、trajectory anchoring和采样。独立线性层没有足够方法证据，完整矩阵高成本故只收录。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：随机hidden映射到RGB的shape正确，不代表具备无decoder生成能力。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、数据协议与代码映射、同主题比较与边界、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.22287v1">原论文</a> · <a href="../../../../multimodal-models/2611.22287-dwd/">实现解读</a> · <a href="#qa-1e6dfdc48c592cb4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:wm-quant" data-paper-title="WM-Quant: Rollout-Aware Post-Training Quantization for JEPA-Style World Models" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="WM-Quant: Rollout-Aware Post-Training Quantization for JEPA-Style World Models 基础模型 University of South Carolina 2026-11-16 JEPA世界模型把连续latent递归输入预测器，量化误差不会像离散token一样重置。WM-Quant保留前三个encoder blocks的8-bit激活、浮点action/proprioception控制通路，并联合优化encoder范围和每个rollout step独立的predictor范围。已核方法位置：3.3–3.4, 4.1–4.2。 完整实验成本过高，不复现（审查 DONE）；仅为合成张量机制诊断，不含公开能力benchmark。L1机制组件；不是完整模型。完整实验成本过高，不复现（审查 DONE）；无能力提升或Evolve晋级声明。执行四个小型encoder blocks、共享线性递归预测器、浮点action通路、整数zero-point的STE范围bank和30步joint calibration；不加载LeWM/DINO-WM，不运行图像编码或CEM，不实现Orin整数GEMM。  推理与系统效率 世界模型量化 多模态 世界建模：状态、生成与动作条件 世界模型量化为什么要看多步而不是单步误差？ 预测latent会再次进入模型，早期误差被后续Jacobian传播，每步又注入新误差；单步最优范围未必使最终轨迹最优。 教学例：状态每步放大1.1倍时，第一步的误差会影响后面所有步。 2026-11-18">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-wm-quant-e55eb5ad" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-90fa9a3aebe05cfb">世界模型量化为什么要看多步而不是单步误差？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Awm-quant">WM-Quant: Rollout-Aware Post-Training Quantization for JEPA-Style World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-18 · University of South Carolina</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>预测latent会再次进入模型，早期误差被后续Jacobian传播，每步又注入新误差；单步最优范围未必使最终轨迹最优。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：状态每步放大1.1倍时，第一步的误差会影响后面所有步。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、数据协议与代码映射、同主题比较与边界、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.21882v1">原论文</a> · <a href="../../../../foundation-models/2611.21882-wm-quant/">实现解读</a> · <a href="#qa-90fa9a3aebe05cfb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:wm-quant" data-paper-title="WM-Quant: Rollout-Aware Post-Training Quantization for JEPA-Style World Models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="WM-Quant: Rollout-Aware Post-Training Quantization for JEPA-Style World Models 基础模型 University of South Carolina 2026-11-16 JEPA世界模型把连续latent递归输入预测器，量化误差不会像离散token一样重置。WM-Quant保留前三个encoder blocks的8-bit激活、浮点action/proprioception控制通路，并联合优化encoder范围和每个rollout step独立的predictor范围。已核方法位置：3.3–3.4, 4.1–4.2。 完整实验成本过高，不复现（审查 DONE）；仅为合成张量机制诊断，不含公开能力benchmark。L1机制组件；不是完整模型。完整实验成本过高，不复现（审查 DONE）；无能力提升或Evolve晋级声明。执行四个小型encoder blocks、共享线性递归预测器、浮点action通路、整数zero-point的STE范围bank和30步joint calibration；不加载LeWM/DINO-WM，不运行图像编码或CEM，不实现Orin整数GEMM。  推理与系统效率 世界模型量化 多模态 世界建模：状态、生成与动作条件 为何不把action和state一起低比特量化？ action差异小却决定候选轨迹排序，和大幅latent共享范围可能直接被舍入抹掉。原方法把控制通路保持浮点。 教学例：state量级10而两动作相差0.001时，共用3-bit范围可能让两个动作编码相同。 2026-11-18">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-5d9c83ed6332d91a">为何不把action和state一起低比特量化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Awm-quant">WM-Quant: Rollout-Aware Post-Training Quantization for JEPA-Style World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-18 · University of South Carolina</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>action差异小却决定候选轨迹排序，和大幅latent共享范围可能直接被舍入抹掉。原方法把控制通路保持浮点。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：state量级10而两动作相差0.001时，共用3-bit范围可能让两个动作编码相同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、数据协议与代码映射、同主题比较与边界、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.21882v1">原论文</a> · <a href="../../../../foundation-models/2611.21882-wm-quant/">实现解读</a> · <a href="#qa-5d9c83ed6332d91a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:wm-quant" data-paper-title="WM-Quant: Rollout-Aware Post-Training Quantization for JEPA-Style World Models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="WM-Quant: Rollout-Aware Post-Training Quantization for JEPA-Style World Models 基础模型 University of South Carolina 2026-11-16 JEPA世界模型把连续latent递归输入预测器，量化误差不会像离散token一样重置。WM-Quant保留前三个encoder blocks的8-bit激活、浮点action/proprioception控制通路，并联合优化encoder范围和每个rollout step独立的predictor范围。已核方法位置：3.3–3.4, 4.1–4.2。 完整实验成本过高，不复现（审查 DONE）；仅为合成张量机制诊断，不含公开能力benchmark。L1机制组件；不是完整模型。完整实验成本过高，不复现（审查 DONE）；无能力提升或Evolve晋级声明。执行四个小型encoder blocks、共享线性递归预测器、浮点action通路、整数zero-point的STE范围bank和30步joint calibration；不加载LeWM/DINO-WM，不运行图像编码或CEM，不实现Orin整数GEMM。  推理与系统效率 世界模型量化 多模态 世界建模：状态、生成与动作条件 fake quant为何不能把连续low当作量化网格起点？ 原文Eq1–2先算整数zero-point z=round(-low/s)，再量化round(r/s)+z并以s(q-z)还原。low+s*round((r-low)/s)是不同格点，可能把零量化成非零；STE只改变反向近似，不能更改前向整数网格。 教学例：3-bit、low=-0.3、范围宽约0.693时，原式将0精确还原为0；错误low锚网格会得到约-0.0029365。 2026-11-18">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-867334ec711b3eb8">fake quant为何不能把连续low当作量化网格起点？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Awm-quant">WM-Quant: Rollout-Aware Post-Training Quantization for JEPA-Style World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-18 · University of South Carolina</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原文Eq1–2先算整数zero-point z=round(-low/s)，再量化round(r/s)+z并以s(q-z)还原。low+s*round((r-low)/s)是不同格点，可能把零量化成非零；STE只改变反向近似，不能更改前向整数网格。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：3-bit、low=-0.3、范围宽约0.693时，原式将0精确还原为0；错误low锚网格会得到约-0.0029365。</p>
<p class="ar-learning-sources">依据：核心公式、数据协议与代码映射；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.21882v1">原论文</a> · <a href="../../../../foundation-models/2611.21882-wm-quant/">实现解读</a> · <a href="#qa-867334ec711b3eb8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:wm-quant" data-paper-title="WM-Quant: Rollout-Aware Post-Training Quantization for JEPA-Style World Models" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="WM-Quant: Rollout-Aware Post-Training Quantization for JEPA-Style World Models 基础模型 University of South Carolina 2026-11-16 JEPA世界模型把连续latent递归输入预测器，量化误差不会像离散token一样重置。WM-Quant保留前三个encoder blocks的8-bit激活、浮点action/proprioception控制通路，并联合优化encoder范围和每个rollout step独立的predictor范围。已核方法位置：3.3–3.4, 4.1–4.2。 完整实验成本过高，不复现（审查 DONE）；仅为合成张量机制诊断，不含公开能力benchmark。L1机制组件；不是完整模型。完整实验成本过高，不复现（审查 DONE）；无能力提升或Evolve晋级声明。执行四个小型encoder blocks、共享线性递归预测器、浮点action通路、整数zero-point的STE范围bank和30步joint calibration；不加载LeWM/DINO-WM，不运行图像编码或CEM，不实现Orin整数GEMM。  推理与系统效率 世界模型量化 多模态 世界建模：状态、生成与动作条件 每步独立范围是否意味着每步一套预测模型？ 不是。predictor权重、旋转和平滑共享，分开的只是少量激活范围；encoder范围也通过整个rollout联合更新。 教学例：同一W用在四步，四组min/max仍可不同。 2026-11-18">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1a999cdb8498e3ef">每步独立范围是否意味着每步一套预测模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Awm-quant">WM-Quant: Rollout-Aware Post-Training Quantization for JEPA-Style World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-18 · University of South Carolina</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。predictor权重、旋转和平滑共享，分开的只是少量激活范围；encoder范围也通过整个rollout联合更新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：同一W用在四步，四组min/max仍可不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、数据协议与代码映射、同主题比较与边界、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.21882v1">原论文</a> · <a href="../../../../foundation-models/2611.21882-wm-quant/">实现解读</a> · <a href="#qa-1a999cdb8498e3ef">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:wm-quant" data-paper-title="WM-Quant: Rollout-Aware Post-Training Quantization for JEPA-Style World Models" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="WM-Quant: Rollout-Aware Post-Training Quantization for JEPA-Style World Models 基础模型 University of South Carolina 2026-11-16 JEPA世界模型把连续latent递归输入预测器，量化误差不会像离散token一样重置。WM-Quant保留前三个encoder blocks的8-bit激活、浮点action/proprioception控制通路，并联合优化encoder范围和每个rollout step独立的predictor范围。已核方法位置：3.3–3.4, 4.1–4.2。 完整实验成本过高，不复现（审查 DONE）；仅为合成张量机制诊断，不含公开能力benchmark。L1机制组件；不是完整模型。完整实验成本过高，不复现（审查 DONE）；无能力提升或Evolve晋级声明。执行四个小型encoder blocks、共享线性递归预测器、浮点action通路、整数zero-point的STE范围bank和30步joint calibration；不加载LeWM/DINO-WM，不运行图像编码或CEM，不实现Orin整数GEMM。  推理与系统效率 世界模型量化 多模态 世界建模：状态、生成与动作条件 本地calibration loss下降能说明PushT成功率提升吗？ 不能。本地使用小型连续递推检验范围梯度、控制保留与误差目标，没有视觉checkpoint、CEM或环境成功标签。 教学例：30步优化减少latent差值，只是L1机制诊断，不生成机械臂任务成功率。 2026-11-18">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-783768aca0759009">本地calibration loss下降能说明PushT成功率提升吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Awm-quant">WM-Quant: Rollout-Aware Post-Training Quantization for JEPA-Style World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-18 · University of South Carolina</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。本地使用小型连续递推检验范围梯度、控制保留与误差目标，没有视觉checkpoint、CEM或环境成功标签。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：30步优化减少latent差值，只是L1机制诊断，不生成机械臂任务成功率。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、数据协议与代码映射、同主题比较与边界、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.21882v1">原论文</a> · <a href="../../../../foundation-models/2611.21882-wm-quant/">实现解读</a> · <a href="#qa-783768aca0759009">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:pixvid" data-paper-title="Back to Pixels: Lifting Latent Video Diffusion into Pixel Space" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Back to Pixels: Lifting Latent Video Diffusion into Pixel Space 多模态大模型 Roblox 2026-11-12 像素视频生成避免VAE潜空间约束，但直接从零学习大规模时空关系成本很高。PixVid保留预训练latent DiT知识，以离线像素—latent线性对齐融合进patch embedding、校准噪声时间步，再加入detailer处理高频细节。高分辨率patch初始化与新增上采样块控制token数量，不能只把VAE删掉就等同本文。§2—3 完整14B视频训练与评测成本过高，不复现（审查 DONE）；未实现组件、未生成视频、未运行GPU、没有指标产物；资料收录，未实现。完整14B视频训练与评测成本过高，不复现（审查 DONE）；普通flow loss或插值不是PixVid复现。本轮仅核对方法、首发时间、机构、代码发布状态与成本。未实现组件、未生成视频、未运行GPU、没有指标产物；不放入Evolve，不将原图或作者视频当本地结果。  视频生成与世界模型 像素空间视频扩散 多模态 世界建模：状态、生成与动作条件 PixVid在像素空间生成，是否意味着不使用预训练latent模型知识？ 不是。它迁移预训练latent DiT，通过离线像素-latent对齐和时间步校准保留知识，再新增detailer。像素输出空间与是否从零训练是两件事。 教学例：继承DiT权重但替换输入patch映射和输出detailer，仍属于利用latent预训练，不是随机初始化全模型。 2026-11-15">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-multimodal-models-pixvid-b6dfb4a6" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4ab5af937fce1a54">PixVid在像素空间生成，是否意味着不使用预训练latent模型知识？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Apixvid">Back to Pixels: Lifting Latent Video Diffusion into Pixel Space</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-15 · Roblox</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。它迁移预训练latent DiT，通过离线像素-latent对齐和时间步校准保留知识，再新增detailer。像素输出空间与是否从零训练是两件事。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：继承DiT权重但替换输入patch映射和输出detailer，仍属于利用latent预训练，不是随机初始化全模型。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制与公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.17336v1">原论文</a> · <a href="../../../../multimodal-models/2611.17336-pixvid/">实现解读</a> · <a href="#qa-4ab5af937fce1a54">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:pixvid" data-paper-title="Back to Pixels: Lifting Latent Video Diffusion into Pixel Space" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Back to Pixels: Lifting Latent Video Diffusion into Pixel Space 多模态大模型 Roblox 2026-11-12 像素视频生成避免VAE潜空间约束，但直接从零学习大规模时空关系成本很高。PixVid保留预训练latent DiT知识，以离线像素—latent线性对齐融合进patch embedding、校准噪声时间步，再加入detailer处理高频细节。高分辨率patch初始化与新增上采样块控制token数量，不能只把VAE删掉就等同本文。§2—3 完整14B视频训练与评测成本过高，不复现（审查 DONE）；未实现组件、未生成视频、未运行GPU、没有指标产物；资料收录，未实现。完整14B视频训练与评测成本过高，不复现（审查 DONE）；普通flow loss或插值不是PixVid复现。本轮仅核对方法、首发时间、机构、代码发布状态与成本。未实现组件、未生成视频、未运行GPU、没有指标产物；不放入Evolve，不将原图或作者视频当本地结果。  视频生成与世界模型 像素空间视频扩散 多模态 世界建模：状态、生成与动作条件 只实现带噪声尺度权重的flow MSE，能算PixVid核心完整实现吗？ 不能。还需要像素-latent线性对齐融合、SNR时间映射、patch迁移和时空detailer及其训练约束。通用loss没有兑现这些结构和依赖。 教学例：给任意卷积网络加1/sigma平方权重，不会自动获得原DiT知识或正确跨帧缓存。 2026-11-15">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-9e3b08012c24e2cd">只实现带噪声尺度权重的flow MSE，能算PixVid核心完整实现吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Apixvid">Back to Pixels: Lifting Latent Video Diffusion into Pixel Space</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-15 · Roblox</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。还需要像素-latent线性对齐融合、SNR时间映射、patch迁移和时空detailer及其训练约束。通用loss没有兑现这些结构和依赖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：给任意卷积网络加1/sigma平方权重，不会自动获得原DiT知识或正确跨帧缓存。</p>
<p class="ar-learning-sources">依据：核心机制与公式、本地范围与成本决定；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.17336v1">原论文</a> · <a href="../../../../multimodal-models/2611.17336-pixvid/">实现解读</a> · <a href="#qa-9e3b08012c24e2cd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:pixvid" data-paper-title="Back to Pixels: Lifting Latent Video Diffusion into Pixel Space" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Back to Pixels: Lifting Latent Video Diffusion into Pixel Space 多模态大模型 Roblox 2026-11-12 像素视频生成避免VAE潜空间约束，但直接从零学习大规模时空关系成本很高。PixVid保留预训练latent DiT知识，以离线像素—latent线性对齐融合进patch embedding、校准噪声时间步，再加入detailer处理高频细节。高分辨率patch初始化与新增上采样块控制token数量，不能只把VAE删掉就等同本文。§2—3 完整14B视频训练与评测成本过高，不复现（审查 DONE）；未实现组件、未生成视频、未运行GPU、没有指标产物；资料收录，未实现。完整14B视频训练与评测成本过高，不复现（审查 DONE）；普通flow loss或插值不是PixVid复现。本轮仅核对方法、首发时间、机构、代码发布状态与成本。未实现组件、未生成视频、未运行GPU、没有指标产物；不放入Evolve，不将原图或作者视频当本地结果。  视频生成与世界模型 像素空间视频扩散 多模态 世界建模：状态、生成与动作条件 PixVid与WOVEN都用视频模型，为什么不是同一任务？ PixVid研究生成器从latent到pixel的表示和计算路径；WOVEN用动作条件视频rollout形成状态转移监督，再训练多模态问答。生成质量不直接等于转移推理能力。 教学例：视频看起来更清晰，仍可能把动作结果生成错；正确回答转移选择题也不说明模型能生成高分辨率视频。 2026-11-15">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7a16e6f0bc6bfac6">PixVid与WOVEN都用视频模型，为什么不是同一任务？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Apixvid">Back to Pixels: Lifting Latent Video Diffusion into Pixel Space</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-15 · Roblox</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>PixVid研究生成器从latent到pixel的表示和计算路径；WOVEN用动作条件视频rollout形成状态转移监督，再训练多模态问答。生成质量不直接等于转移推理能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：视频看起来更清晰，仍可能把动作结果生成错；正确回答转移选择题也不说明模型能生成高分辨率视频。</p>
<p class="ar-learning-sources">依据：背景与主要改动、论文离线与线上效果；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.17336v1">原论文</a> · <a href="../../../../multimodal-models/2611.17336-pixvid/">实现解读</a> · <a href="#qa-7a16e6f0bc6bfac6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:pixvid" data-paper-title="Back to Pixels: Lifting Latent Video Diffusion into Pixel Space" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Back to Pixels: Lifting Latent Video Diffusion into Pixel Space 多模态大模型 Roblox 2026-11-12 像素视频生成避免VAE潜空间约束，但直接从零学习大规模时空关系成本很高。PixVid保留预训练latent DiT知识，以离线像素—latent线性对齐融合进patch embedding、校准噪声时间步，再加入detailer处理高频细节。高分辨率patch初始化与新增上采样块控制token数量，不能只把VAE删掉就等同本文。§2—3 完整14B视频训练与评测成本过高，不复现（审查 DONE）；未实现组件、未生成视频、未运行GPU、没有指标产物；资料收录，未实现。完整14B视频训练与评测成本过高，不复现（审查 DONE）；普通flow loss或插值不是PixVid复现。本轮仅核对方法、首发时间、机构、代码发布状态与成本。未实现组件、未生成视频、未运行GPU、没有指标产物；不放入Evolve，不将原图或作者视频当本地结果。  视频生成与世界模型 像素空间视频扩散 多模态 世界建模：状态、生成与动作条件 单张A100显存可能装得下一次PixVid推理，为什么本轮仍不复现？ 成本门槛看整套训练与评测，不只看是否装得下。论文有14B、约130万clip、20k更新和多臂分辨率矩阵；本轮资料收录并审查DONE，不下载资源或试训探成本。 教学例：原文一个设置需192秒生成一clip；成百上千clip、多种子和训练还另计，不能称为快速组件验证。 2026-11-15">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b26edbe834029176">单张A100显存可能装得下一次PixVid推理，为什么本轮仍不复现？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Apixvid">Back to Pixels: Lifting Latent Video Diffusion into Pixel Space</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-15 · Roblox</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>成本门槛看整套训练与评测，不只看是否装得下。论文有14B、约130万clip、20k更新和多臂分辨率矩阵；本轮资料收录并审查DONE，不下载资源或试训探成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：原文一个设置需192秒生成一clip；成百上千clip、多种子和训练还另计，不能称为快速组件验证。</p>
<p class="ar-learning-sources">依据：论文离线与线上效果、本地范围与成本决定；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.17336v1">原论文</a> · <a href="../../../../multimodal-models/2611.17336-pixvid/">实现解读</a> · <a href="#qa-b26edbe834029176">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:rslivebench-uav-protocol" data-paper-title="RSLiveBench-UAV: A Continually Evolving Vision-Language Benchmark for Aerial Spatial Intelligence" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="RSLiveBench-UAV: A Continually Evolving Vision-Language Benchmark for Aerial Spatial Intelligence 多模态大模型 East China Normal University 2026-11-11 航空空间题需要跨视角实体匹配、真实几何与新观察，不是给旧图片改写问题。作者将持续实地 UAV 采集、实体中心的答案生产、四场景滚动窗口和延迟公开答案组合成持续 benchmark。新版本只接受上一发布与本次发布之间拍摄的图像；每次退役最早入窗场景，更新的是 25% 场景，不是固定 25% 题目或分数。§3、附录评分协议 成本过高，不复现（审查 DONE）；L0 协议/部分 scorer。只重放四场景 FIFO、采集时窗、答案禁运和部分确定性计分，不采集无人机图像、不运行完整 17 任务 benchmark，也不提供 VLM 能力分数。RollingWindow.advance 验证时间严格不等式与 FIFO；disclosure_allowed 实现日历月禁运。strict_count_mra 只做 SC 子 scorer，不宣称涵盖框、角度、GPS、类别的完整 parser。aggregate_scores 对调用者声明的四组 inventory 做层次聚合，并拒绝重复/未知 ID、将缺预测传成 unavailable。  多模态评测与数据 航空空间与持续基准 多模态 世界建模：状态、生成与动作条件 四场景每轮换一个，为什么不能说固定更新25%的题或分数？ FIFO替换最早入窗场景，25%只对场景数成立。场景题量、任务组成和四组宏平均权重不同，不能把场景比例直接当题量或分数比例。 教学例：四场景分别有10、20、30、40题，退役10题场景只移除10%旧题；最终四能力组仍各占25%。 2026-11-18">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-multimodal-models-rslivebench-uav-protocol-52a74eb2" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-239f1081e4677a8a">四场景每轮换一个，为什么不能说固定更新25%的题或分数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Arslivebench-uav-protocol">RSLiveBench-UAV: A Continually Evolving Vision-Language Benchmark for Aerial Spatial Intelligence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-18 · East China Normal University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>FIFO替换最早入窗场景，25%只对场景数成立。场景题量、任务组成和四组宏平均权重不同，不能把场景比例直接当题量或分数比例。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：四场景分别有10、20、30、40题，退役10题场景只移除10%旧题；最终四能力组仍各占25%。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.14953v1">原论文</a> · <a href="../../../../multimodal-models/2611.14953-rslivebench-uav-protocol/">实现解读</a> · <a href="#qa-239f1081e4677a8a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:rslivebench-uav-protocol" data-paper-title="RSLiveBench-UAV: A Continually Evolving Vision-Language Benchmark for Aerial Spatial Intelligence" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="RSLiveBench-UAV: A Continually Evolving Vision-Language Benchmark for Aerial Spatial Intelligence 多模态大模型 East China Normal University 2026-11-11 航空空间题需要跨视角实体匹配、真实几何与新观察，不是给旧图片改写问题。作者将持续实地 UAV 采集、实体中心的答案生产、四场景滚动窗口和延迟公开答案组合成持续 benchmark。新版本只接受上一发布与本次发布之间拍摄的图像；每次退役最早入窗场景，更新的是 25% 场景，不是固定 25% 题目或分数。§3、附录评分协议 成本过高，不复现（审查 DONE）；L0 协议/部分 scorer。只重放四场景 FIFO、采集时窗、答案禁运和部分确定性计分，不采集无人机图像、不运行完整 17 任务 benchmark，也不提供 VLM 能力分数。RollingWindow.advance 验证时间严格不等式与 FIFO；disclosure_allowed 实现日历月禁运。strict_count_mra 只做 SC 子 scorer，不宣称涵盖框、角度、GPS、类别的完整 parser。aggregate_scores 对调用者声明的四组 inventory 做层次聚合，并拒绝重复/未知 ID、将缺预测传成 unavailable。  多模态评测与数据 航空空间与持续基准 多模态 世界建模：状态、生成与动作条件 答案为什么不能在发布120天后直接公开？ 协议要求场景已退役，且自首次发布至少经过4个日历月，取两者较晚时间。日历月不是固定120天；未退役时即使很久也不能公开。 教学例：1月31日首发、2月退役，最早到5月31日；5月30日仍禁运。若6月1日才退役，则需等6月1日。 2026-11-18">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-30a9a213d54055f3">答案为什么不能在发布120天后直接公开？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Arslivebench-uav-protocol">RSLiveBench-UAV: A Continually Evolving Vision-Language Benchmark for Aerial Spatial Intelligence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-18 · East China Normal University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>协议要求场景已退役，且自首次发布至少经过4个日历月，取两者较晚时间。日历月不是固定120天；未退役时即使很久也不能公开。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：1月31日首发、2月退役，最早到5月31日；5月30日仍禁运。若6月1日才退役，则需等6月1日。</p>
<p class="ar-learning-sources">依据：核心公式、数据协议与代码映射；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.14953v1">原论文</a> · <a href="../../../../multimodal-models/2611.14953-rslivebench-uav-protocol/">实现解读</a> · <a href="#qa-30a9a213d54055f3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:rslivebench-uav-protocol" data-paper-title="RSLiveBench-UAV: A Continually Evolving Vision-Language Benchmark for Aerial Spatial Intelligence" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="RSLiveBench-UAV: A Continually Evolving Vision-Language Benchmark for Aerial Spatial Intelligence 多模态大模型 East China Normal University 2026-11-11 航空空间题需要跨视角实体匹配、真实几何与新观察，不是给旧图片改写问题。作者将持续实地 UAV 采集、实体中心的答案生产、四场景滚动窗口和延迟公开答案组合成持续 benchmark。新版本只接受上一发布与本次发布之间拍摄的图像；每次退役最早入窗场景，更新的是 25% 场景，不是固定 25% 题目或分数。§3、附录评分协议 成本过高，不复现（审查 DONE）；L0 协议/部分 scorer。只重放四场景 FIFO、采集时窗、答案禁运和部分确定性计分，不采集无人机图像、不运行完整 17 任务 benchmark，也不提供 VLM 能力分数。RollingWindow.advance 验证时间严格不等式与 FIFO；disclosure_allowed 实现日历月禁运。strict_count_mra 只做 SC 子 scorer，不宣称涵盖框、角度、GPS、类别的完整 parser。aggregate_scores 对调用者声明的四组 inventory 做层次聚合，并拒绝重复/未知 ID、将缺预测传成 unavailable。  多模态评测与数据 航空空间与持续基准 多模态 世界建模：状态、生成与动作条件 RSLiveBench-UAV的freshness与WOVEN的scene-OOD有什么区别？ 前者用实地采集时间和滚动退役控制新观察与答案暴露；后者按视觉转移监督的场景轴划分泛化评测。时间新鲜不能代替跨场景泛化，生成场景的OOD也不能证明真实新采集无污染。 教学例：昨天新拍但一直同一停车场可满足采集时窗，却未必测新场景泛化；WOVEN未见过餐厅场景也不等于它有UAV几何。 2026-11-18">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f8d341a8e9573a40">RSLiveBench-UAV的freshness与WOVEN的scene-OOD有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Arslivebench-uav-protocol">RSLiveBench-UAV: A Continually Evolving Vision-Language Benchmark for Aerial Spatial Intelligence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-18 · East China Normal University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者用实地采集时间和滚动退役控制新观察与答案暴露；后者按视觉转移监督的场景轴划分泛化评测。时间新鲜不能代替跨场景泛化，生成场景的OOD也不能证明真实新采集无污染。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：昨天新拍但一直同一停车场可满足采集时窗，却未必测新场景泛化；WOVEN未见过餐厅场景也不等于它有UAV几何。</p>
<p class="ar-learning-sources">依据：背景与主要改动、论文离线与线上效果、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.14953v1">原论文</a> · <a href="../../../../multimodal-models/2611.14953-rslivebench-uav-protocol/">实现解读</a> · <a href="#qa-f8d341a8e9573a40">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:rslivebench-uav-protocol" data-paper-title="RSLiveBench-UAV: A Continually Evolving Vision-Language Benchmark for Aerial Spatial Intelligence" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="RSLiveBench-UAV: A Continually Evolving Vision-Language Benchmark for Aerial Spatial Intelligence 多模态大模型 East China Normal University 2026-11-11 航空空间题需要跨视角实体匹配、真实几何与新观察，不是给旧图片改写问题。作者将持续实地 UAV 采集、实体中心的答案生产、四场景滚动窗口和延迟公开答案组合成持续 benchmark。新版本只接受上一发布与本次发布之间拍摄的图像；每次退役最早入窗场景，更新的是 25% 场景，不是固定 25% 题目或分数。§3、附录评分协议 成本过高，不复现（审查 DONE）；L0 协议/部分 scorer。只重放四场景 FIFO、采集时窗、答案禁运和部分确定性计分，不采集无人机图像、不运行完整 17 任务 benchmark，也不提供 VLM 能力分数。RollingWindow.advance 验证时间严格不等式与 FIFO；disclosure_allowed 实现日历月禁运。strict_count_mra 只做 SC 子 scorer，不宣称涵盖框、角度、GPS、类别的完整 parser。aggregate_scores 对调用者声明的四组 inventory 做层次聚合，并拒绝重复/未知 ID、将缺预测传成 unavailable。  多模态评测与数据 航空空间与持续基准 多模态 世界建模：状态、生成与动作条件 模型没跑的题和返回格式错误的题为什么不能都当0分？ 格式错误是已观察失败，必须留在分母记0；没跑的题没有观察，官方完整得分应不可用。聚合先component再task再四组，不能按题数直接平均。 教学例：四组得分100、50、解析失败0、80时宏平均57.5；若最后一组根本没跑，则overall=null而不是把它补0。 2026-11-18">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-45111a721b9c19d8">模型没跑的题和返回格式错误的题为什么不能都当0分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Arslivebench-uav-protocol">RSLiveBench-UAV: A Continually Evolving Vision-Language Benchmark for Aerial Spatial Intelligence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-18 · East China Normal University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>格式错误是已观察失败，必须留在分母记0；没跑的题没有观察，官方完整得分应不可用。聚合先component再task再四组，不能按题数直接平均。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：四组得分100、50、解析失败0、80时宏平均57.5；若最后一组根本没跑，则overall=null而不是把它补0。</p>
<p class="ar-learning-sources">依据：核心公式、数据协议与代码映射、结果、负控与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.14953v1">原论文</a> · <a href="../../../../multimodal-models/2611.14953-rslivebench-uav-protocol/">实现解读</a> · <a href="#qa-45111a721b9c19d8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:onlyact" data-paper-title="OnlyAct: Extracting Action Representations from Foundation Models for World Models" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="OnlyAct: Extracting Action Representations from Foundation Models for World Models 多模态大模型 University of Oxford 2026-11-10 无标签 latent-action 方法常用重建瓶颈排除场景，但过窄会丢动作细节，过宽又会泄漏外观。OnlyAct 从已预训练的 V-JEPA 2 ViT-L 出发：两帧作为同一 clip 输入，tubelet 从第一层联合观察两帧，而不是先单帧编码再求差；均值池化、固定随机投影至 640 维并归一化。它用场景交换的同动作正例，以及同一视频不同时间窗的 hard negative 做对比适配。静态相机用 RAFT 光流提取移动区域，原像素共同平移并粘到另一场景； 完整矩阵明显超出本轮短预算，成本过高，不复现（审查 DONE）；真实 NVIDIA A100 的 CUDA 42/43/44 诊断也已通过，见真实 GPU 回执与三 seed 指标。L1 对比损失／输入合同组件，不是 V-JEPA 2 动作编码器或世界模型复现。本地执行全候选损失、固定投影和 hard-negative 合同，不伪造场景交换视频、光流或真实动作能力。pooled_action 只处理外部两帧联合编码 token 的池化、冻结投影和归一化，不含任何假 V-JEPA。bank_contract 定义精确候选与正例索引；contrastive_loss 执行对称 InfoNCE 并实际反传。  JEPA 表征学习 动作场景解耦与世界模型 多模态 世界建模：状态、生成与动作条件 OnlyAct为什么把同一视频的另一时间窗当hard negative，而不只用其他视频？ 不同视频常能仅凭背景外观分开，模型可能不必学习动作。同视频非重叠窗保留较相似场景，使这种捷径更难；但无动作标签，所以不同窗不保证动作语义真的不同。 教学例：同一厨房里“开抽屉”和“关抽屉”比厨房与游戏画面的对比更难用场景颜色直接区分。 2026-11-12">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-multimodal-models-onlyact-72d2c481" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b86c525ec0b5cdbb">OnlyAct为什么把同一视频的另一时间窗当hard negative，而不只用其他视频？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Aonlyact">OnlyAct: Extracting Action Representations from Foundation Models for World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-12 · University of Oxford</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同视频常能仅凭背景外观分开，模型可能不必学习动作。同视频非重叠窗保留较相似场景，使这种捷径更难；但无动作标签，所以不同窗不保证动作语义真的不同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：同一厨房里“开抽屉”和“关抽屉”比厨房与游戏画面的对比更难用场景颜色直接区分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.14420">原论文</a> · <a href="../../../../multimodal-models/2611.14420-onlyact/">实现解读</a> · <a href="#qa-b86c525ec0b5cdbb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:onlyact" data-paper-title="OnlyAct: Extracting Action Representations from Foundation Models for World Models" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="OnlyAct: Extracting Action Representations from Foundation Models for World Models 多模态大模型 University of Oxford 2026-11-10 无标签 latent-action 方法常用重建瓶颈排除场景，但过窄会丢动作细节，过宽又会泄漏外观。OnlyAct 从已预训练的 V-JEPA 2 ViT-L 出发：两帧作为同一 clip 输入，tubelet 从第一层联合观察两帧，而不是先单帧编码再求差；均值池化、固定随机投影至 640 维并归一化。它用场景交换的同动作正例，以及同一视频不同时间窗的 hard negative 做对比适配。静态相机用 RAFT 光流提取移动区域，原像素共同平移并粘到另一场景； 完整矩阵明显超出本轮短预算，成本过高，不复现（审查 DONE）；真实 NVIDIA A100 的 CUDA 42/43/44 诊断也已通过，见真实 GPU 回执与三 seed 指标。L1 对比损失／输入合同组件，不是 V-JEPA 2 动作编码器或世界模型复现。本地执行全候选损失、固定投影和 hard-negative 合同，不伪造场景交换视频、光流或真实动作能力。pooled_action 只处理外部两帧联合编码 token 的池化、冻结投影和归一化，不含任何假 V-JEPA。bank_contract 定义精确候选与正例索引；contrastive_loss 执行对称 InfoNCE 并实际反传。  JEPA 表征学习 动作场景解耦与世界模型 多模态 世界建模：状态、生成与动作条件 OnlyAct为什么不能用两个独立单帧embedding相减来替代原动作编码？ 原V-JEPA2把两帧组成一个clip，tubelet从第一层就联合观察时空变化；独立编码后相减没有同样的跨帧交互。后续池化、固定随机投影和归一化只处理该联合表征，学习发生在encoder LoRA，不是投影。 教学例：物体跨帧移动并同时改变光照；联合token可在上下文中比较运动，而两个独立全图向量差可能混合外观变化。 2026-11-12">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-3c09fc73e0d90dc7">OnlyAct为什么不能用两个独立单帧embedding相减来替代原动作编码？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Aonlyact">OnlyAct: Extracting Action Representations from Foundation Models for World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-12 · University of Oxford</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原V-JEPA2把两帧组成一个clip，tubelet从第一层就联合观察时空变化；独立编码后相减没有同样的跨帧交互。后续池化、固定随机投影和归一化只处理该联合表征，学习发生在encoder LoRA，不是投影。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：物体跨帧移动并同时改变光照；联合token可在上下文中比较运动，而两个独立全图向量差可能混合外观变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、数据协议与代码映射；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.14420">原论文</a> · <a href="../../../../multimodal-models/2611.14420-onlyact/">实现解读</a> · <a href="#qa-3c09fc73e0d90dc7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:onlyact" data-paper-title="OnlyAct: Extracting Action Representations from Foundation Models for World Models" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="OnlyAct: Extracting Action Representations from Foundation Models for World Models 多模态大模型 University of Oxford 2026-11-10 无标签 latent-action 方法常用重建瓶颈排除场景，但过窄会丢动作细节，过宽又会泄漏外观。OnlyAct 从已预训练的 V-JEPA 2 ViT-L 出发：两帧作为同一 clip 输入，tubelet 从第一层联合观察两帧，而不是先单帧编码再求差；均值池化、固定随机投影至 640 维并归一化。它用场景交换的同动作正例，以及同一视频不同时间窗的 hard negative 做对比适配。静态相机用 RAFT 光流提取移动区域，原像素共同平移并粘到另一场景； 完整矩阵明显超出本轮短预算，成本过高，不复现（审查 DONE）；真实 NVIDIA A100 的 CUDA 42/43/44 诊断也已通过，见真实 GPU 回执与三 seed 指标。L1 对比损失／输入合同组件，不是 V-JEPA 2 动作编码器或世界模型复现。本地执行全候选损失、固定投影和 hard-negative 合同，不伪造场景交换视频、光流或真实动作能力。pooled_action 只处理外部两帧联合编码 token 的池化、冻结投影和归一化，不含任何假 V-JEPA。bank_contract 定义精确候选与正例索引；contrastive_loss 执行对称 InfoNCE 并实际反传。  JEPA 表征学习 动作场景解耦与世界模型 多模态 世界建模：状态、生成与动作条件 OnlyAct与无标签动作重建瓶颈方法的区别，是否只是把编码器换大？ 不只是规模。它从预训练时空表征出发，用保动作换场景正例和同场景换时间负例重塑几何，不依靠窄瓶颈丢弃信息。瓶颈宽窄的表达力与场景泄漏折中，变成由构造与对比目标约束；真实解耦仍需下游检验。 教学例：窄码可能同时丢掉小幅动作；OnlyAct尝试用不同场景中同一移动区域互为正例保留这种变化，但合成loss下降不能证明成功。 2026-11-12">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d5a48f9ea7fb8958">OnlyAct与无标签动作重建瓶颈方法的区别，是否只是把编码器换大？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Aonlyact">OnlyAct: Extracting Action Representations from Foundation Models for World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-12 · University of Oxford</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不只是规模。它从预训练时空表征出发，用保动作换场景正例和同场景换时间负例重塑几何，不依靠窄瓶颈丢弃信息。瓶颈宽窄的表达力与场景泄漏折中，变成由构造与对比目标约束；真实解耦仍需下游检验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：窄码可能同时丢掉小幅动作；OnlyAct尝试用不同场景中同一移动区域互为正例保留这种变化，但合成loss下降不能证明成功。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、论文离线与线上效果；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.14420">原论文</a> · <a href="../../../../multimodal-models/2611.14420-onlyact/">实现解读</a> · <a href="#qa-d5a48f9ea7fb8958">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:onlyact" data-paper-title="OnlyAct: Extracting Action Representations from Foundation Models for World Models" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="OnlyAct: Extracting Action Representations from Foundation Models for World Models 多模态大模型 University of Oxford 2026-11-10 无标签 latent-action 方法常用重建瓶颈排除场景，但过窄会丢动作细节，过宽又会泄漏外观。OnlyAct 从已预训练的 V-JEPA 2 ViT-L 出发：两帧作为同一 clip 输入，tubelet 从第一层联合观察两帧，而不是先单帧编码再求差；均值池化、固定随机投影至 640 维并归一化。它用场景交换的同动作正例，以及同一视频不同时间窗的 hard negative 做对比适配。静态相机用 RAFT 光流提取移动区域，原像素共同平移并粘到另一场景； 完整矩阵明显超出本轮短预算，成本过高，不复现（审查 DONE）；真实 NVIDIA A100 的 CUDA 42/43/44 诊断也已通过，见真实 GPU 回执与三 seed 指标。L1 对比损失／输入合同组件，不是 V-JEPA 2 动作编码器或世界模型复现。本地执行全候选损失、固定投影和 hard-negative 合同，不伪造场景交换视频、光流或真实动作能力。pooled_action 只处理外部两帧联合编码 token 的池化、冻结投影和归一化，不含任何假 V-JEPA。bank_contract 定义精确候选与正例索引；contrastive_loss 执行对称 InfoNCE 并实际反传。  JEPA 表征学习 动作场景解耦与世界模型 多模态 世界建模：状态、生成与动作条件 OnlyAct的microbatch为2、梯度累积8次，为什么每个query仍只有4个负例？ 候选只来自当前forward的2组anchor/positive/hard negative，共6个；排除query自身后剩1正例和4负例。累积只把多次梯度相加，未建立memory queue或跨步候选bank。 教学例：一组query不能看到下一次forward才出现的视频pair；把effective batch16直接变成48候选会改写论文目标。 2026-11-12">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8fc1e1ae0781544d">OnlyAct的microbatch为2、梯度累积8次，为什么每个query仍只有4个负例？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Aonlyact">OnlyAct: Extracting Action Representations from Foundation Models for World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-12 · University of Oxford</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>候选只来自当前forward的2组anchor/positive/hard negative，共6个；排除query自身后剩1正例和4负例。累积只把多次梯度相加，未建立memory queue或跨步候选bank。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：一组query不能看到下一次forward才出现的视频pair；把effective batch16直接变成48候选会改写论文目标。</p>
<p class="ar-learning-sources">依据：核心公式、数据协议与代码映射、结果、负控与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.14420">原论文</a> · <a href="../../../../multimodal-models/2611.14420-onlyact/">实现解读</a> · <a href="#qa-8fc1e1ae0781544d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:rs-jepa" data-paper-title="RS-JEPA: Remote Sensing Joint-Embedding Predictive Architecture with Scan-Path Views for Cross-Sensor Image Retrieval" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="RS-JEPA: Remote Sensing Joint-Embedding Predictive Architecture with Scan-Path Views for Cross-Sensor Image Retrieval 多模态大模型 Prince Mohammad Bin Fahd University 2026-11-10 顺序敏感的 Vision Mamba 对相同图像 patch 的不同读取次序产生不同表征，RS-JEPA 据此构造无像素编辑的视图。学习到的 hard half-split 让隐藏特征预测更困难；邻域共识不只拉近配准 twin，还约束两个传感器对其他场景的相似性分布。训练 target 使用同一主干的 stop-gradient，不是另一个 momentum encoder。 完整多数据集比较成本过高，不复现（审查 DONE）；本地交付扫描排列、反梯度划分和邻域损失三个独立 tensor 组件，不含替身 Vim、完整模型或图像检索成绩。CUDA 路径必须由提交的 A100/A30 回执验收。scan_path() 返回精确排列；adversarial_partition() 实际执行 hard 分组、直通权重及反梯度；neighbourhood_consensus() 执行 Eq.8–9，拒绝单样本、零向量、非有限值和跨设备输入。采用合成小 tensor，不下载图像、checkpoint 或代理 backbone，不声称完整 JEPA 已训练。  JEPA 表征学习 扫描路径与跨传感器邻域对齐 多模态 世界建模：状态、生成与动作条件 RS-JEPA 为什么只改 patch 读取次序，也能构成不同自监督视图？ Vision Mamba的状态递推依赖之前读过的token，所以同一组像素在不同路径下产生不同上下文表征。位置嵌入先加入，排序后编码再恢复；改变的是扫描动态，不是像素内容或隐含的标签增强。 教学例：2×3网格的行序是0,1,2,3,4,5，列序是0,3,1,4,2,5；第二个patch看到的前缀已经不同。 2026-11-11">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-multimodal-models-rs-jepa-fcdebfcf" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8a826054d2e3770a">RS-JEPA 为什么只改 patch 读取次序，也能构成不同自监督视图？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Ars-jepa">RS-JEPA: Remote Sensing Joint-Embedding Predictive Architecture with Scan-Path Views for Cross-Sensor Image Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-11 · Prince Mohammad Bin Fahd University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Vision Mamba的状态递推依赖之前读过的token，所以同一组像素在不同路径下产生不同上下文表征。位置嵌入先加入，排序后编码再恢复；改变的是扫描动态，不是像素内容或隐含的标签增强。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：2×3网格的行序是0,1,2,3,4,5，列序是0,3,1,4,2,5；第二个patch看到的前缀已经不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.14496">原论文</a> · <a href="../../../../multimodal-models/2611.14496-rs-jepa/">实现解读</a> · <a href="#qa-8a826054d2e3770a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:rs-jepa" data-paper-title="RS-JEPA: Remote Sensing Joint-Embedding Predictive Architecture with Scan-Path Views for Cross-Sensor Image Retrieval" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="RS-JEPA: Remote Sensing Joint-Embedding Predictive Architecture with Scan-Path Views for Cross-Sensor Image Retrieval 多模态大模型 Prince Mohammad Bin Fahd University 2026-11-10 顺序敏感的 Vision Mamba 对相同图像 patch 的不同读取次序产生不同表征，RS-JEPA 据此构造无像素编辑的视图。学习到的 hard half-split 让隐藏特征预测更困难；邻域共识不只拉近配准 twin，还约束两个传感器对其他场景的相似性分布。训练 target 使用同一主干的 stop-gradient，不是另一个 momentum encoder。 完整多数据集比较成本过高，不复现（审查 DONE）；本地交付扫描排列、反梯度划分和邻域损失三个独立 tensor 组件，不含替身 Vim、完整模型或图像检索成绩。CUDA 路径必须由提交的 A100/A30 回执验收。scan_path() 返回精确排列；adversarial_partition() 实际执行 hard 分组、直通权重及反梯度；neighbourhood_consensus() 执行 Eq.8–9，拒绝单样本、零向量、非有限值和跨设备输入。采用合成小 tensor，不下载图像、checkpoint 或代理 backbone，不声称完整 JEPA 已训练。  JEPA 表征学习 扫描路径与跨传感器邻域对齐 多模态 世界建模：状态、生成与动作条件 RS-JEPA 既然前向仍是原 token，scorer 怎么能学到更难的划分？ Hard top-half决定成员，但直通权重前向抵消为1、反向仍保留sigmoid路径。梯度反转让scorer朝增大预测困难的方向更新；单纯top-k切片会切断这条学习信号。 教学例：相同前向token可有非零scorer梯度；测试应同时核对输出完全不变和梯度恰好取反，而不只检查shape。 2026-11-11">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-58ea66e7be7965f0">RS-JEPA 既然前向仍是原 token，scorer 怎么能学到更难的划分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Ars-jepa">RS-JEPA: Remote Sensing Joint-Embedding Predictive Architecture with Scan-Path Views for Cross-Sensor Image Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-11 · Prince Mohammad Bin Fahd University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Hard top-half决定成员，但直通权重前向抵消为1、反向仍保留sigmoid路径。梯度反转让scorer朝增大预测困难的方向更新；单纯top-k切片会切断这条学习信号。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：相同前向token可有非零scorer梯度；测试应同时核对输出完全不变和梯度恰好取反，而不只检查shape。</p>
<p class="ar-learning-sources">依据：核心公式、数据协议与代码映射；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.14496">原论文</a> · <a href="../../../../multimodal-models/2611.14496-rs-jepa/">实现解读</a> · <a href="#qa-58ea66e7be7965f0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:rs-jepa" data-paper-title="RS-JEPA: Remote Sensing Joint-Embedding Predictive Architecture with Scan-Path Views for Cross-Sensor Image Retrieval" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="RS-JEPA: Remote Sensing Joint-Embedding Predictive Architecture with Scan-Path Views for Cross-Sensor Image Retrieval 多模态大模型 Prince Mohammad Bin Fahd University 2026-11-10 顺序敏感的 Vision Mamba 对相同图像 patch 的不同读取次序产生不同表征，RS-JEPA 据此构造无像素编辑的视图。学习到的 hard half-split 让隐藏特征预测更困难；邻域共识不只拉近配准 twin，还约束两个传感器对其他场景的相似性分布。训练 target 使用同一主干的 stop-gradient，不是另一个 momentum encoder。 完整多数据集比较成本过高，不复现（审查 DONE）；本地交付扫描排列、反梯度划分和邻域损失三个独立 tensor 组件，不含替身 Vim、完整模型或图像检索成绩。CUDA 路径必须由提交的 A100/A30 回执验收。scan_path() 返回精确排列；adversarial_partition() 实际执行 hard 分组、直通权重及反梯度；neighbourhood_consensus() 执行 Eq.8–9，拒绝单样本、零向量、非有限值和跨设备输入。采用合成小 tensor，不下载图像、checkpoint 或代理 backbone，不声称完整 JEPA 已训练。  JEPA 表征学习 扫描路径与跨传感器邻域对齐 多模态 世界建模：状态、生成与动作条件 RS-JEPA 的邻域共识与只对齐配准 twin 的对比学习有何不同？ Twin对齐约束同一场景跨传感器接近，却不保证各传感器对其他场景的排序几何一致。共识比较四种邻域分布，并在每一种里排除同pair索引；该项补充而不替代原InfoNCE防坍缩目标。 教学例：两传感器都把同一桥梁配对拉近，但一个把河流当最近邻，另一个把城市当最近邻；共识针对这个差异。 2026-11-11">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-eb1672b725d557bc">RS-JEPA 的邻域共识与只对齐配准 twin 的对比学习有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Ars-jepa">RS-JEPA: Remote Sensing Joint-Embedding Predictive Architecture with Scan-Path Views for Cross-Sensor Image Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-11 · Prince Mohammad Bin Fahd University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Twin对齐约束同一场景跨传感器接近，却不保证各传感器对其他场景的排序几何一致。共识比较四种邻域分布，并在每一种里排除同pair索引；该项补充而不替代原InfoNCE防坍缩目标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：两传感器都把同一桥梁配对拉近，但一个把河流当最近邻，另一个把城市当最近邻；共识针对这个差异。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.14496">原论文</a> · <a href="../../../../multimodal-models/2611.14496-rs-jepa/">实现解读</a> · <a href="#qa-eb1672b725d557bc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:rs-jepa" data-paper-title="RS-JEPA: Remote Sensing Joint-Embedding Predictive Architecture with Scan-Path Views for Cross-Sensor Image Retrieval" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="RS-JEPA: Remote Sensing Joint-Embedding Predictive Architecture with Scan-Path Views for Cross-Sensor Image Retrieval 多模态大模型 Prince Mohammad Bin Fahd University 2026-11-10 顺序敏感的 Vision Mamba 对相同图像 patch 的不同读取次序产生不同表征，RS-JEPA 据此构造无像素编辑的视图。学习到的 hard half-split 让隐藏特征预测更困难；邻域共识不只拉近配准 twin，还约束两个传感器对其他场景的相似性分布。训练 target 使用同一主干的 stop-gradient，不是另一个 momentum encoder。 完整多数据集比较成本过高，不复现（审查 DONE）；本地交付扫描排列、反梯度划分和邻域损失三个独立 tensor 组件，不含替身 Vim、完整模型或图像检索成绩。CUDA 路径必须由提交的 A100/A30 回执验收。scan_path() 返回精确排列；adversarial_partition() 实际执行 hard 分组、直通权重及反梯度；neighbourhood_consensus() 执行 Eq.8–9，拒绝单样本、零向量、非有限值和跨设备输入。采用合成小 tensor，不下载图像、checkpoint 或代理 backbone，不声称完整 JEPA 已训练。  JEPA 表征学习 扫描路径与跨传感器邻域对齐 多模态 世界建模：状态、生成与动作条件 RS-JEPA 的损失值对上了，为什么还要单独核对 stop-gradient 和真实 CUDA？ 将consensus target忘记detach不会改变前向数值，却改变梯度；把device写成cuda也不说明运算在GPU上。独立循环须比对值和梯度，实际CUDA诊断检查tensor设备并运行反传，仍不等于训练完整Vim或复现图像检索。 教学例：batch只有两样本时每行仅一个非twin邻居，四个分布都为1，KL应为0；更大batch再检查梯度与传感器交换不变性。 2026-11-11">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ef96d26f392f61c2">RS-JEPA 的损失值对上了，为什么还要单独核对 stop-gradient 和真实 CUDA？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Ars-jepa">RS-JEPA: Remote Sensing Joint-Embedding Predictive Architecture with Scan-Path Views for Cross-Sensor Image Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-11 · Prince Mohammad Bin Fahd University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>将consensus target忘记detach不会改变前向数值，却改变梯度；把device写成cuda也不说明运算在GPU上。独立循环须比对值和梯度，实际CUDA诊断检查tensor设备并运行反传，仍不等于训练完整Vim或复现图像检索。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：batch只有两样本时每行仅一个非twin邻居，四个分布都为1，KL应为0；更大batch再检查梯度与传感器交换不变性。</p>
<p class="ar-learning-sources">依据：数据协议与代码映射、结果、负控与边界、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.14496">原论文</a> · <a href="../../../../multimodal-models/2611.14496-rs-jepa/">实现解读</a> · <a href="#qa-ef96d26f392f61c2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:sensorwm-planning" data-paper-title="Personalized health coaching via coachable health age and counterfactual wearable trajectories" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Personalized health coaching via coachable health age and counterfactual wearable trajectories 多模态大模型 Google Research / University of California, Los Angeles 2026-11-05 论文把可修改的可穿戴行为与生理状态分开：每日步数、主要睡眠时长、cardio-intensity minutes 作为动作；RHR、AZM 等作为预测结果，而不是可以直接指令改变的行为。Coachable Health Age（CHA）将可解释的可穿戴信号映射到年龄等价量，SensorWM 预测给定行为序列的未来状态，再对候选行为方案排序，最后交给 LLM 生成 12 周计划。SensorWM 的中心模型不是一个对行为加权的规则。 在单张 A100/A30 或 Mac 的本轮预算下，私有数据／未确认公开的预训练权重与完整训练评估依赖使其成本过高，不复现（审查 DONE）。诊断输入是明示的固定数学夹具，端点不是模型预测，seed 仅扰动候选输入顺序。L1 CPU 数学后处理，不是健康预测、医疗建议或完整规划能力。本地只执行论文 Eq.55–56；不提供私有 SensorWM、生成轨迹、125 方案网格、临床可行性判定或 LLM 健康教练。Actions 明确三动作顺序与单位；Candidate 强制外部有限预测端点和布尔 feasible；personalized_effort 执行 Eq.55；  JEPA 表征学习 可穿戴世界模型与外部候选排序 多模态 世界建模：状态、生成与动作条件 SensorWM排序为什么以保持原习惯的未来CHA为锚，而不是以当前观测CHA为锚？ 即使行为不变，模型也可能预测生理漂移。候选的增量收益应比较同一未来时点的status-quo与候选端点，避免把自然漂移误算成改变行为的效果。这仍是模型条件预测，不识别真实因果干预收益。 教学算术例，非健康预测：当前量为10，不变行为的未来为12，候选未来为11.5；增量收益是12−11.5=0.5，而不是10−11.5=−1.5。 2026-11-12">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-multimodal-models-sensorwm-planning-1889ab65" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-24eae8e2271e60ce">SensorWM排序为什么以保持原习惯的未来CHA为锚，而不是以当前观测CHA为锚？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Asensorwm-planning">Personalized health coaching via coachable health age and counterfactual wearable trajectories</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-12 · Google Research / University of California, Los Angeles</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>即使行为不变，模型也可能预测生理漂移。候选的增量收益应比较同一未来时点的status-quo与候选端点，避免把自然漂移误算成改变行为的效果。这仍是模型条件预测，不识别真实因果干预收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学算术例，非健康预测：当前量为10，不变行为的未来为12，候选未来为11.5；增量收益是12−11.5=0.5，而不是10−11.5=−1.5。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、论文离线与线上效果；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.08568">原论文</a> · <a href="../../../../multimodal-models/2611.08568-sensorwm-planning/">实现解读</a> · <a href="#qa-24eae8e2271e60ce">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:sensorwm-planning" data-paper-title="Personalized health coaching via coachable health age and counterfactual wearable trajectories" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Personalized health coaching via coachable health age and counterfactual wearable trajectories 多模态大模型 Google Research / University of California, Los Angeles 2026-11-05 论文把可修改的可穿戴行为与生理状态分开：每日步数、主要睡眠时长、cardio-intensity minutes 作为动作；RHR、AZM 等作为预测结果，而不是可以直接指令改变的行为。Coachable Health Age（CHA）将可解释的可穿戴信号映射到年龄等价量，SensorWM 预测给定行为序列的未来状态，再对候选行为方案排序，最后交给 LLM 生成 12 周计划。SensorWM 的中心模型不是一个对行为加权的规则。 在单张 A100/A30 或 Mac 的本轮预算下，私有数据／未确认公开的预训练权重与完整训练评估依赖使其成本过高，不复现（审查 DONE）。诊断输入是明示的固定数学夹具，端点不是模型预测，seed 仅扰动候选输入顺序。L1 CPU 数学后处理，不是健康预测、医疗建议或完整规划能力。本地只执行论文 Eq.55–56；不提供私有 SensorWM、生成轨迹、125 方案网格、临床可行性判定或 LLM 健康教练。Actions 明确三动作顺序与单位；Candidate 强制外部有限预测端点和布尔 feasible；personalized_effort 执行 Eq.55；  JEPA 表征学习 可穿戴世界模型与外部候选排序 多模态 世界建模：状态、生成与动作条件 为什么SensorWM的个体努力不能直接用三个动作增量相加？ 动作单位和个体历史变动尺度不同。Eq.55先除以有数值下限的个体标准差，再平方求和；这同时统一尺度并惩罚大幅偏离。下限只防止近零标准差导致极端努力，不是证明行为安全的医疗阈值。 教学算术例：个体sigma全为0，三个动作差分别为500、15、10，按论文floors各标准化为1，E=3；假设外部收益0.8，score=0.8/(1+3)=0.2，不是0.8/3。 2026-11-12">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-a61ba230cad502e9">为什么SensorWM的个体努力不能直接用三个动作增量相加？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Asensorwm-planning">Personalized health coaching via coachable health age and counterfactual wearable trajectories</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-12 · Google Research / University of California, Los Angeles</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>动作单位和个体历史变动尺度不同。Eq.55先除以有数值下限的个体标准差，再平方求和；这同时统一尺度并惩罚大幅偏离。下限只防止近零标准差导致极端努力，不是证明行为安全的医疗阈值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学算术例：个体sigma全为0，三个动作差分别为500、15、10，按论文floors各标准化为1，E=3；假设外部收益0.8，score=0.8/(1+3)=0.2，不是0.8/3。</p>
<p class="ar-learning-sources">依据：核心公式、数据协议与代码映射；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.08568">原论文</a> · <a href="../../../../multimodal-models/2611.08568-sensorwm-planning/">实现解读</a> · <a href="#qa-a61ba230cad502e9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:sensorwm-planning" data-paper-title="Personalized health coaching via coachable health age and counterfactual wearable trajectories" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Personalized health coaching via coachable health age and counterfactual wearable trajectories 多模态大模型 Google Research / University of California, Los Angeles 2026-11-05 论文把可修改的可穿戴行为与生理状态分开：每日步数、主要睡眠时长、cardio-intensity minutes 作为动作；RHR、AZM 等作为预测结果，而不是可以直接指令改变的行为。Coachable Health Age（CHA）将可解释的可穿戴信号映射到年龄等价量，SensorWM 预测给定行为序列的未来状态，再对候选行为方案排序，最后交给 LLM 生成 12 周计划。SensorWM 的中心模型不是一个对行为加权的规则。 在单张 A100/A30 或 Mac 的本轮预算下，私有数据／未确认公开的预训练权重与完整训练评估依赖使其成本过高，不复现（审查 DONE）。诊断输入是明示的固定数学夹具，端点不是模型预测，seed 仅扰动候选输入顺序。L1 CPU 数学后处理，不是健康预测、医疗建议或完整规划能力。本地只执行论文 Eq.55–56；不提供私有 SensorWM、生成轨迹、125 方案网格、临床可行性判定或 LLM 健康教练。Actions 明确三动作顺序与单位；Candidate 强制外部有限预测端点和布尔 feasible；personalized_effort 执行 Eq.55；  JEPA 表征学习 可穿戴世界模型与外部候选排序 多模态 世界建模：状态、生成与动作条件 SensorWM候选排序与LeWAM潜空间动作规划，为什么不能统称已实现世界模型控制？ LeWAM从学习策略产生动作候选，经冻结动力学rollout和动作梯度优化接入环境闭环；SensorWM这一本地组件只对外部预测端点和外部可行性声明做比值排序，没有模型、动作搜索或执行。两个数学分数的意义不同，更不能用L1排序测试证明健康或机器人能力。 教学例：把三个已给端点按收益/努力排序，不会产生缺失的12周轨迹；同样，给出一个goal距离公式也不会自动完成机器人闭环。 2026-11-12">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-edd7ba8363051b16">SensorWM候选排序与LeWAM潜空间动作规划，为什么不能统称已实现世界模型控制？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Asensorwm-planning">Personalized health coaching via coachable health age and counterfactual wearable trajectories</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-12 · Google Research / University of California, Los Angeles</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>LeWAM从学习策略产生动作候选，经冻结动力学rollout和动作梯度优化接入环境闭环；SensorWM这一本地组件只对外部预测端点和外部可行性声明做比值排序，没有模型、动作搜索或执行。两个数学分数的意义不同，更不能用L1排序测试证明健康或机器人能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：把三个已给端点按收益/努力排序，不会产生缺失的12周轨迹；同样，给出一个goal距离公式也不会自动完成机器人闭环。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、结果、负控与边界、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.08568">原论文</a> · <a href="../../../../multimodal-models/2611.08568-sensorwm-planning/">实现解读</a> · <a href="#qa-edd7ba8363051b16">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:sensorwm-planning" data-paper-title="Personalized health coaching via coachable health age and counterfactual wearable trajectories" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Personalized health coaching via coachable health age and counterfactual wearable trajectories 多模态大模型 Google Research / University of California, Los Angeles 2026-11-05 论文把可修改的可穿戴行为与生理状态分开：每日步数、主要睡眠时长、cardio-intensity minutes 作为动作；RHR、AZM 等作为预测结果，而不是可以直接指令改变的行为。Coachable Health Age（CHA）将可解释的可穿戴信号映射到年龄等价量，SensorWM 预测给定行为序列的未来状态，再对候选行为方案排序，最后交给 LLM 生成 12 周计划。SensorWM 的中心模型不是一个对行为加权的规则。 在单张 A100/A30 或 Mac 的本轮预算下，私有数据／未确认公开的预训练权重与完整训练评估依赖使其成本过高，不复现（审查 DONE）。诊断输入是明示的固定数学夹具，端点不是模型预测，seed 仅扰动候选输入顺序。L1 CPU 数学后处理，不是健康预测、医疗建议或完整规划能力。本地只执行论文 Eq.55–56；不提供私有 SensorWM、生成轨迹、125 方案网格、临床可行性判定或 LLM 健康教练。Actions 明确三动作顺序与单位；Candidate 强制外部有限预测端点和布尔 feasible；personalized_effort 执行 Eq.55；  JEPA 表征学习 可穿戴世界模型与外部候选排序 多模态 世界建模：状态、生成与动作条件 本地Candidate要求feasible是布尔值，并通过三seed检查，能否说明计划临床安全？ 不能。类型合同只防止缺失或模糊输入，feasible的真实性和临床依据必须由外部流程保证，模块不核验。端点也必须由真实模型及来源支持；本地固定夹具只测sigma、锚点、严格gain&gt;0.1和排序，不生成预测、目标动作或医疗建议。 教学例：外部把一条危险或无依据候选写成feasible=true，数学核无法识别；正确做法是保留其上游责任边界，而不是把返回ID当安全认证。 2026-11-12">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1bc1fbf7e31c01ff">本地Candidate要求feasible是布尔值，并通过三seed检查，能否说明计划临床安全？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Asensorwm-planning">Personalized health coaching via coachable health age and counterfactual wearable trajectories</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-12 · Google Research / University of California, Los Angeles</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。类型合同只防止缺失或模糊输入，feasible的真实性和临床依据必须由外部流程保证，模块不核验。端点也必须由真实模型及来源支持；本地固定夹具只测sigma、锚点、严格gain&gt;0.1和排序，不生成预测、目标动作或医疗建议。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：外部把一条危险或无依据候选写成feasible=true，数学核无法识别；正确做法是保留其上游责任边界，而不是把返回ID当安全认证。</p>
<p class="ar-learning-sources">依据：数据协议与代码映射、结果、负控与边界、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.08568">原论文</a> · <a href="../../../../multimodal-models/2611.08568-sensorwm-planning/">实现解读</a> · <a href="#qa-1bc1fbf7e31c01ff">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gui-jepa" data-paper-title="GUI-JEPA: Candidate-Conditioned JEPA Latents as a Fast Action Policy for Mobile GUI Agents" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="GUI-JEPA: Candidate-Conditioned JEPA Latents as a Fast Action Policy for Mobile GUI Agents 基础模型 Shanghai Jiao Tong University / Nanyang Technological University 2026-10-27 多数 GUI Agent 依靠 7B 级视觉语言模型逐 token 生成动作。GUI-JEPA 则从 accessibility tree 枚举可执行动作，用冻结 JEPA 编码器只编码一次画面；动作类型、坐标与 ROI 特征条件化残差 predictor，为每个候选生成 latent，再一次批量打分选 argmax，不解码动作文本。关键不是把“画面 latent 离目标越近”当动作价值。预测器通过真实候选上的 listwise 决策损失训练，结构头的候选视觉信息必须经过条件化 latent； 完整实验：成本过高，不复现（审查 DONE）；本地状态：L1 latent predictor / structural-head 组件、diagnostic only，不是 GUI Agent 或 AndroidControl 接入。完整实验：成本过高，不复现（审查 DONE）；不作为 evolve 能力证据。实现真实三层 Transformer residual predictor、候选 ROI / 全屏池化、cosine 结构头、动作类型 bias、外部 text score 相加、有效候选 mask 和 weighted listwise loss。  JEPA与世界模型 候选条件决策与GUI 多模态 世界建模：状态、生成与动作条件 GUI-JEPA为什么不需要逐token生成动作？ 它先从可访问性树枚举候选，再让每个候选条件化画面latent，一次批量打分选动作。动作空间来自观测侧枚举，不是语言模型自由生成。因此速度取决于候选数，也依赖像素型Agent不一定拥有的a11y输入，不能直接比较所有GUI系统。 教学例子：页面已有三种可执行按钮动作，系统分别算三个分数后选最高者；这不同于先生成JSON文本，再解析其中坐标。 2026-10-29">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-gui-jepa-f231a89e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6d61dbbeb9e00d39">GUI-JEPA为什么不需要逐token生成动作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agui-jepa">GUI-JEPA: Candidate-Conditioned JEPA Latents as a Fast Action Policy for Mobile GUI Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-29 · Shanghai Jiao Tong University / Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它先从可访问性树枚举候选，再让每个候选条件化画面latent，一次批量打分选动作。动作空间来自观测侧枚举，不是语言模型自由生成。因此速度取决于候选数，也依赖像素型Agent不一定拥有的a11y输入，不能直接比较所有GUI系统。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>页面已有三种可执行按钮动作，系统分别算三个分数后选最高者；这不同于先生成JSON文本，再解析其中坐标。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.36877v1">原论文</a> · <a href="../../../../foundation-models/2610.36877-gui-jepa/">实现解读</a> · <a href="#qa-6d61dbbeb9e00d39">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gui-jepa" data-paper-title="GUI-JEPA: Candidate-Conditioned JEPA Latents as a Fast Action Policy for Mobile GUI Agents" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="GUI-JEPA: Candidate-Conditioned JEPA Latents as a Fast Action Policy for Mobile GUI Agents 基础模型 Shanghai Jiao Tong University / Nanyang Technological University 2026-10-27 多数 GUI Agent 依靠 7B 级视觉语言模型逐 token 生成动作。GUI-JEPA 则从 accessibility tree 枚举可执行动作，用冻结 JEPA 编码器只编码一次画面；动作类型、坐标与 ROI 特征条件化残差 predictor，为每个候选生成 latent，再一次批量打分选 argmax，不解码动作文本。关键不是把“画面 latent 离目标越近”当动作价值。预测器通过真实候选上的 listwise 决策损失训练，结构头的候选视觉信息必须经过条件化 latent； 完整实验：成本过高，不复现（审查 DONE）；本地状态：L1 latent predictor / structural-head 组件、diagnostic only，不是 GUI Agent 或 AndroidControl 接入。完整实验：成本过高，不复现（审查 DONE）；不作为 evolve 能力证据。实现真实三层 Transformer residual predictor、候选 ROI / 全屏池化、cosine 结构头、动作类型 bias、外部 text score 相加、有效候选 mask 和 weighted listwise loss。  JEPA与世界模型 候选条件决策与GUI 多模态 世界建模：状态、生成与动作条件 为什么候选的动作与ROI需要先经过残差predictor，而不是直接送结构打分头？ 论文刻意让候选相关视觉信息通过条件化latent路径，避免打分头绕开JEPA predictor。动作与ROI影响query，三层Transformer产生残差latent，再做ROI与全局池化。它用决策损失训练，不自动意味着这个latent是准确的未来画面预测。 教学例子：两个都是click的按钮，ROI内容与坐标不同，应产生不同条件latent；若直接把原ROI接到额外捷径头，不能用该结果证明predictor有用。 2026-10-29">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-012814975154e4eb">为什么候选的动作与ROI需要先经过残差predictor，而不是直接送结构打分头？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agui-jepa">GUI-JEPA: Candidate-Conditioned JEPA Latents as a Fast Action Policy for Mobile GUI Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-29 · Shanghai Jiao Tong University / Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>论文刻意让候选相关视觉信息通过条件化latent路径，避免打分头绕开JEPA predictor。动作与ROI影响query，三层Transformer产生残差latent，再做ROI与全局池化。它用决策损失训练，不自动意味着这个latent是准确的未来画面预测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个都是click的按钮，ROI内容与坐标不同，应产生不同条件latent；若直接把原ROI接到额外捷径头，不能用该结果证明predictor有用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.36877v1">原论文</a> · <a href="../../../../foundation-models/2610.36877-gui-jepa/">实现解读</a> · <a href="#qa-012814975154e4eb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gui-jepa" data-paper-title="GUI-JEPA: Candidate-Conditioned JEPA Latents as a Fast Action Policy for Mobile GUI Agents" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="GUI-JEPA: Candidate-Conditioned JEPA Latents as a Fast Action Policy for Mobile GUI Agents 基础模型 Shanghai Jiao Tong University / Nanyang Technological University 2026-10-27 多数 GUI Agent 依靠 7B 级视觉语言模型逐 token 生成动作。GUI-JEPA 则从 accessibility tree 枚举可执行动作，用冻结 JEPA 编码器只编码一次画面；动作类型、坐标与 ROI 特征条件化残差 predictor，为每个候选生成 latent，再一次批量打分选 argmax，不解码动作文本。关键不是把“画面 latent 离目标越近”当动作价值。预测器通过真实候选上的 listwise 决策损失训练，结构头的候选视觉信息必须经过条件化 latent； 完整实验：成本过高，不复现（审查 DONE）；本地状态：L1 latent predictor / structural-head 组件、diagnostic only，不是 GUI Agent 或 AndroidControl 接入。完整实验：成本过高，不复现（审查 DONE）；不作为 evolve 能力证据。实现真实三层 Transformer residual predictor、候选 ROI / 全屏池化、cosine 结构头、动作类型 bias、外部 text score 相加、有效候选 mask 和 weighted listwise loss。  JEPA与世界模型 候选条件决策与GUI 多模态 世界建模：状态、生成与动作条件 GUI-JEPA的latent打分，与“预测下一状态然后选最接近目标”有何区别？ 它将latent作为通过listwise动作损失塑造的决策特征，而非把到目标的latent距离当作价值。论文随机初始化predictor也能匹配dynamics预训练版本，提示决策相关性和动力学预测不是一回事。不能从动作分数改善推导完整世界模型准确。 教学例子：点击确认可能使画面变化很小却完成任务，打开动画可能让视觉距离更接近某目标图但动作错误；决策分数不等于像素或latent相似度。 2026-10-29">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e4c26d5506f18c85">GUI-JEPA的latent打分，与“预测下一状态然后选最接近目标”有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agui-jepa">GUI-JEPA: Candidate-Conditioned JEPA Latents as a Fast Action Policy for Mobile GUI Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-29 · Shanghai Jiao Tong University / Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它将latent作为通过listwise动作损失塑造的决策特征，而非把到目标的latent距离当作价值。论文随机初始化predictor也能匹配dynamics预训练版本，提示决策相关性和动力学预测不是一回事。不能从动作分数改善推导完整世界模型准确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>点击确认可能使画面变化很小却完成任务，打开动画可能让视觉距离更接近某目标图但动作错误；决策分数不等于像素或latent相似度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、论文离线与线上效果；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.36877v1">原论文</a> · <a href="../../../../foundation-models/2610.36877-gui-jepa/">实现解读</a> · <a href="#qa-e4c26d5506f18c85">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gui-jepa" data-paper-title="GUI-JEPA: Candidate-Conditioned JEPA Latents as a Fast Action Policy for Mobile GUI Agents" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="GUI-JEPA: Candidate-Conditioned JEPA Latents as a Fast Action Policy for Mobile GUI Agents 基础模型 Shanghai Jiao Tong University / Nanyang Technological University 2026-10-27 多数 GUI Agent 依靠 7B 级视觉语言模型逐 token 生成动作。GUI-JEPA 则从 accessibility tree 枚举可执行动作，用冻结 JEPA 编码器只编码一次画面；动作类型、坐标与 ROI 特征条件化残差 predictor，为每个候选生成 latent，再一次批量打分选 argmax，不解码动作文本。关键不是把“画面 latent 离目标越近”当动作价值。预测器通过真实候选上的 listwise 决策损失训练，结构头的候选视觉信息必须经过条件化 latent； 完整实验：成本过高，不复现（审查 DONE）；本地状态：L1 latent predictor / structural-head 组件、diagnostic only，不是 GUI Agent 或 AndroidControl 接入。完整实验：成本过高，不复现（审查 DONE）；不作为 evolve 能力证据。实现真实三层 Transformer residual predictor、候选 ROI / 全屏池化、cosine 结构头、动作类型 bias、外部 text score 相加、有效候选 mask 和 weighted listwise loss。  JEPA与世界模型 候选条件决策与GUI 多模态 世界建模：状态、生成与动作条件 本地三层predictor和真实梯度通过验证，是否等于已经能操作Android？ 不能。当前接口只读外部画面与condition latent，验证残差结构头、候选mask和加权listwise损失。编码器、a11y枚举、MiniLM ranker与执行环境都没有接入；正例仅给训练loss，不能传进forward让模型看答案。GPU张量验证不是AndroidControl成功率。 教学例子：给两个合法latent候选反向更新参数，只能证明梯度路径工作；真正打开应用还需要从截图生成latent、找到合法候选、执行并观察下一页面。 2026-10-29">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3b5a93ef5e4fcae4">本地三层predictor和真实梯度通过验证，是否等于已经能操作Android？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agui-jepa">GUI-JEPA: Candidate-Conditioned JEPA Latents as a Fast Action Policy for Mobile GUI Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-29 · Shanghai Jiao Tong University / Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。当前接口只读外部画面与condition latent，验证残差结构头、候选mask和加权listwise损失。编码器、a11y枚举、MiniLM ranker与执行环境都没有接入；正例仅给训练loss，不能传进forward让模型看答案。GPU张量验证不是AndroidControl成功率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>给两个合法latent候选反向更新参数，只能证明梯度路径工作；真正打开应用还需要从截图生成latent、找到合法候选、执行并观察下一页面。</p>
<p class="ar-learning-sources">依据：本地复现、检查与负控、高成本完整实验；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.36877v1">原论文</a> · <a href="../../../../foundation-models/2610.36877-gui-jepa/">实现解读</a> · <a href="#qa-3b5a93ef5e4fcae4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:swim" data-paper-title="SWIM: Learning What Matters from Behaviors for JEPA World Models" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="SWIM: Learning What Matters from Behaviors for JEPA World Models 基础模型 Boston University / Unity Technologies 2026-10-27 JEPA world model 预测视觉 latent，但 latent 欧氏距离不一定反映规划进展。SCALE 用 simulator state 的距离校准 latent 几何；若状态中含无关坐标，均匀加权会把这些干扰也学进去。SWIM 先用已记录动作训练门控逆动力学，再把冻结的连续权重传给状态距离监督。第一阶段保留当前状态完整信息，只给未来位移逐坐标加 gate，避免把门控误写成当前与未来状态同时裁剪。 完整 world-model 训练与规划评测：成本过高，不复现（审查 DONE）；本地状态：L1 逆动力学门控目标与状态距离组件，diagnostic only，不含视觉 world model、环境或规划器。完整 world-model 训练与规划评测：成本过高，不复现（审查 DONE）；不是 Agent 成功率或 evolve 提升证据。GatedInverseDynamics 真实运行两层 LayerNorm / GELU MLP，输出 Gaussian mean 和限制在 [-5,2] 的 log standard deviation。论文 hidden width 1024，本地使用明确缩小的宽度以做 L1；  JEPA与世界模型 行为加权状态几何 多模态 世界建模：状态、生成与动作条件 SWIM学到的是机器人策略，还是状态距离该看哪些坐标？ SWIM先从离线记录动作中学习连续状态坐标权重，再用它构造world-model几何监督。逆动力学预测记录动作只是学习权重的训练目标；实际部署仍由图像encoder、latent dynamics和CEM等规划器决定动作。本地仅实现门控目标与距离，不等于可执行机器人策略。 教学例子：状态含方块位置和背景灯颜色，行为数据可能让方块位置获得较高相对权重；这只改变“相距多远”的定义，并没有直接输出抓取轨迹。 2026-10-30">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-swim-9da395d5" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-300d76e6b7918837">SWIM学到的是机器人策略，还是状态距离该看哪些坐标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aswim">SWIM: Learning What Matters from Behaviors for JEPA World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-30 · Boston University / Unity Technologies</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>SWIM先从离线记录动作中学习连续状态坐标权重，再用它构造world-model几何监督。逆动力学预测记录动作只是学习权重的训练目标；实际部署仍由图像encoder、latent dynamics和CEM等规划器决定动作。本地仅实现门控目标与距离，不等于可执行机器人策略。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>状态含方块位置和背景灯颜色，行为数据可能让方块位置获得较高相对权重；这只改变“相距多远”的定义，并没有直接输出抓取轨迹。</p>
<p class="ar-learning-sources">依据：背景与主要改动、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.36662v1">原论文</a> · <a href="../../../../foundation-models/2610.36662-swim/">实现解读</a> · <a href="#qa-300d76e6b7918837">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:swim" data-paper-title="SWIM: Learning What Matters from Behaviors for JEPA World Models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="SWIM: Learning What Matters from Behaviors for JEPA World Models 基础模型 Boston University / Unity Technologies 2026-10-27 JEPA world model 预测视觉 latent，但 latent 欧氏距离不一定反映规划进展。SCALE 用 simulator state 的距离校准 latent 几何；若状态中含无关坐标，均匀加权会把这些干扰也学进去。SWIM 先用已记录动作训练门控逆动力学，再把冻结的连续权重传给状态距离监督。第一阶段保留当前状态完整信息，只给未来位移逐坐标加 gate，避免把门控误写成当前与未来状态同时裁剪。 完整 world-model 训练与规划评测：成本过高，不复现（审查 DONE）；本地状态：L1 逆动力学门控目标与状态距离组件，diagnostic only，不含视觉 world model、环境或规划器。完整 world-model 训练与规划评测：成本过高，不复现（审查 DONE）；不是 Agent 成功率或 evolve 提升证据。GatedInverseDynamics 真实运行两层 LayerNorm / GELU MLP，输出 Gaussian mean 和限制在 [-5,2] 的 log standard deviation。论文 hidden width 1024，本地使用明确缩小的宽度以做 L1；  JEPA与世界模型 行为加权状态几何 多模态 世界建模：状态、生成与动作条件 为什么当前状态不能一起gate，为什么还需要真实错配的discrimination？ 当前状态提供动作发生的完整上下文，论文只门控未来位移；把两者都gate会改掉逆动力学输入定义。仅拟合正例时，模型可能忽略未来变化、只靠当前状态预测动作；cyclic错配让同一个当前状态和动作与错误未来对比，促使门控保留行为相关的位移信息。 教学例子：记录动作是向右，当前位置保持不变，正例未来向右；负例换成batch下一条未来再减当前位置。不能同时把当前状态也换掉，否则模型可能利用不同上下文区分正负。 2026-10-30">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-a40912dd5fb29c9d">为什么当前状态不能一起gate，为什么还需要真实错配的discrimination？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aswim">SWIM: Learning What Matters from Behaviors for JEPA World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-30 · Boston University / Unity Technologies</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>当前状态提供动作发生的完整上下文，论文只门控未来位移；把两者都gate会改掉逆动力学输入定义。仅拟合正例时，模型可能忽略未来变化、只靠当前状态预测动作；cyclic错配让同一个当前状态和动作与错误未来对比，促使门控保留行为相关的位移信息。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>记录动作是向右，当前位置保持不变，正例未来向右；负例换成batch下一条未来再减当前位置。不能同时把当前状态也换掉，否则模型可能利用不同上下文区分正负。</p>
<p class="ar-learning-sources">依据：核心公式、检查与负控；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.36662v1">原论文</a> · <a href="../../../../foundation-models/2610.36662-swim/">实现解读</a> · <a href="#qa-a40912dd5fb29c9d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:swim" data-paper-title="SWIM: Learning What Matters from Behaviors for JEPA World Models" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="SWIM: Learning What Matters from Behaviors for JEPA World Models 基础模型 Boston University / Unity Technologies 2026-10-27 JEPA world model 预测视觉 latent，但 latent 欧氏距离不一定反映规划进展。SCALE 用 simulator state 的距离校准 latent 几何；若状态中含无关坐标，均匀加权会把这些干扰也学进去。SWIM 先用已记录动作训练门控逆动力学，再把冻结的连续权重传给状态距离监督。第一阶段保留当前状态完整信息，只给未来位移逐坐标加 gate，避免把门控误写成当前与未来状态同时裁剪。 完整 world-model 训练与规划评测：成本过高，不复现（审查 DONE）；本地状态：L1 逆动力学门控目标与状态距离组件，diagnostic only，不含视觉 world model、环境或规划器。完整 world-model 训练与规划评测：成本过高，不复现（审查 DONE）；不是 Agent 成功率或 evolve 提升证据。GatedInverseDynamics 真实运行两层 LayerNorm / GELU MLP，输出 Gaussian mean 和限制在 [-5,2] 的 log standard deviation。论文 hidden width 1024，本地使用明确缩小的宽度以做 L1；  JEPA与世界模型 行为加权状态几何 多模态 世界建模：状态、生成与动作条件 把状态乘g还是sqrt(g)，以及之后再标准化，会得到同一个距离吗？ 不会。要让平方距离中的每维系数是g，坐标必须乘sqrt(g)；乘g会得到g²。权重作用于已经标准化的状态，之后再逐坐标标准化会抵消缩放。整体gate尺度在Pearson相关中会抵消，且可被逆模型吸收，所以绝对gate值也不是唯一可识别的重要性刻度。 教学例子：一维差值2、gate0.25，目标距离为0.25×4=1；乘sqrt(g)=0.5再平方也是1，直接乘g再平方却是0.25。再除以缩放后的标准差会把0.5抵消。 2026-10-30">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c1b394272419a8ac">把状态乘g还是sqrt(g)，以及之后再标准化，会得到同一个距离吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aswim">SWIM: Learning What Matters from Behaviors for JEPA World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-30 · Boston University / Unity Technologies</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不会。要让平方距离中的每维系数是g，坐标必须乘sqrt(g)；乘g会得到g²。权重作用于已经标准化的状态，之后再逐坐标标准化会抵消缩放。整体gate尺度在Pearson相关中会抵消，且可被逆模型吸收，所以绝对gate值也不是唯一可识别的重要性刻度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一维差值2、gate0.25，目标距离为0.25×4=1；乘sqrt(g)=0.5再平方也是1，直接乘g再平方却是0.25。再除以缩放后的标准差会把0.5抵消。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.36662v1">原论文</a> · <a href="../../../../foundation-models/2610.36662-swim/">实现解读</a> · <a href="#qa-c1b394272419a8ac">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:swim" data-paper-title="SWIM: Learning What Matters from Behaviors for JEPA World Models" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="SWIM: Learning What Matters from Behaviors for JEPA World Models 基础模型 Boston University / Unity Technologies 2026-10-27 JEPA world model 预测视觉 latent，但 latent 欧氏距离不一定反映规划进展。SCALE 用 simulator state 的距离校准 latent 几何；若状态中含无关坐标，均匀加权会把这些干扰也学进去。SWIM 先用已记录动作训练门控逆动力学，再把冻结的连续权重传给状态距离监督。第一阶段保留当前状态完整信息，只给未来位移逐坐标加 gate，避免把门控误写成当前与未来状态同时裁剪。 完整 world-model 训练与规划评测：成本过高，不复现（审查 DONE）；本地状态：L1 逆动力学门控目标与状态距离组件，diagnostic only，不含视觉 world model、环境或规划器。完整 world-model 训练与规划评测：成本过高，不复现（审查 DONE）；不是 Agent 成功率或 evolve 提升证据。GatedInverseDynamics 真实运行两层 LayerNorm / GELU MLP，输出 Gaussian mean 和限制在 [-5,2] 的 log standard deviation。论文 hidden width 1024，本地使用明确缩小的宽度以做 L1；  JEPA与世界模型 行为加权状态几何 多模态 世界建模：状态、生成与动作条件 怎样防止组件测试把“L1让gate变小”误当作学到了行为，或把未来state泄露到规划？ 先单独检查去掉L1后的行为项仍给gate梯度，再检查真实optimizer更新，而不只看参数有变化。第二阶段state距离停梯度，未来state只在离线训练构造位移，部署接口不能读取它。常量距离的Pearson没有定义，应拒绝，不能加任意epsilon后当成几何学习有效。 教学例子：若只算λsum(g)，gate当然会下降，即使记录动作全被忽略；因此本地另算λ=0的梯度。若所有frame pairs距离都为0，相关度分母为0，应报错而不是写成功率1。 2026-10-30">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0989a9f5d8371bbd">怎样防止组件测试把“L1让gate变小”误当作学到了行为，或把未来state泄露到规划？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aswim">SWIM: Learning What Matters from Behaviors for JEPA World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-30 · Boston University / Unity Technologies</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>先单独检查去掉L1后的行为项仍给gate梯度，再检查真实optimizer更新，而不只看参数有变化。第二阶段state距离停梯度，未来state只在离线训练构造位移，部署接口不能读取它。常量距离的Pearson没有定义，应拒绝，不能加任意epsilon后当成几何学习有效。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>若只算λsum(g)，gate当然会下降，即使记录动作全被忽略；因此本地另算λ=0的梯度。若所有frame pairs距离都为0，相关度分母为0，应报错而不是写成功率1。</p>
<p class="ar-learning-sources">依据：本地复现、检查与负控；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.36662v1">原论文</a> · <a href="../../../../foundation-models/2610.36662-swim/">实现解读</a> · <a href="#qa-0989a9f5d8371bbd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:dt-jepa" data-paper-title="DT-JEPA: Learning to Predict Future Representations for Decision-Making" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="DT-JEPA: Learning to Predict Future Representations for Decision-Making 基础模型 Southeast University 2026-10-23 传统DT用单个return-to-go条件，无法区分回报相同但未来动力学不同的轨迹。本方法将条件改成由历史预测的未来latent分布：历史encoder生成Gaussian参数，EMA target encoder只在训练期编码真实未来；重参数采样的预测未来通过独立gamma/beta MLP调制DT hidden。离线目标为BC加Gaussian NLL；在线通过双target critic的较小值构建多步target，并优化Q1指导的actor目标。 成本过高，不复现（审查 DONE）。D4RL共19个locomotion/navigation数据配置、主表5种子、多个未见reward的在线适配及基线/消融；附录DT4层/4头/512hidden、batch256/context20。原文未给总GPU小时，不臆测。完整offline+online矩阵超单卡短时预算，不安装MuJoCo、不下载轨迹、不启动环境试跑。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  JEPA与世界模型 未来表征与离线决策 多模态 世界建模：状态、生成与动作条件 Decision Transformer 为什么可能需要比“期望回报是多少”更丰富的未来条件？ 不同轨迹可能获得相同总回报，却通向完全不同状态，单个 return-to-go 无法区分这些动力学。DT-JEPA 用从历史预测的未来表示分布作为条件，让动作选择获得更具体的未来信息。未来只是预测，不是部署时可读取的真实结果，仍要管理不确定性和训练信息隔离。 教学例：两条路线奖励相同，一条到充电区、另一条到出口；相同回报数字未说明当前该往哪走，未来状态特征提供另一类条件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-dt-jepa-898e3cdc" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-656e6bff07c6b2fa">Decision Transformer 为什么可能需要比“期望回报是多少”更丰富的未来条件？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adt-jepa">DT-JEPA: Learning to Predict Future Representations for Decision-Making</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Southeast University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同轨迹可能获得相同总回报，却通向完全不同状态，单个 return-to-go 无法区分这些动力学。DT-JEPA 用从历史预测的未来表示分布作为条件，让动作选择获得更具体的未来信息。未来只是预测，不是部署时可读取的真实结果，仍要管理不确定性和训练信息隔离。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：两条路线奖励相同，一条到充电区、另一条到出口；相同回报数字未说明当前该往哪走，未来状态特征提供另一类条件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32657v1">原论文</a> · <a href="../../../../foundation-models/2610.32657-dt-jepa/">实现解读</a> · <a href="#qa-656e6bff07c6b2fa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:dt-jepa" data-paper-title="DT-JEPA: Learning to Predict Future Representations for Decision-Making" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="DT-JEPA: Learning to Predict Future Representations for Decision-Making 基础模型 Southeast University 2026-10-23 传统DT用单个return-to-go条件，无法区分回报相同但未来动力学不同的轨迹。本方法将条件改成由历史预测的未来latent分布：历史encoder生成Gaussian参数，EMA target encoder只在训练期编码真实未来；重参数采样的预测未来通过独立gamma/beta MLP调制DT hidden。离线目标为BC加Gaussian NLL；在线通过双target critic的较小值构建多步target，并优化Q1指导的actor目标。 成本过高，不复现（审查 DONE）。D4RL共19个locomotion/navigation数据配置、主表5种子、多个未见reward的在线适配及基线/消融；附录DT4层/4头/512hidden、batch256/context20。原文未给总GPU小时，不臆测。完整offline+online矩阵超单卡短时预算，不安装MuJoCo、不下载轨迹、不启动环境试跑。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  JEPA与世界模型 未来表征与离线决策 多模态 世界建模：状态、生成与动作条件 为什么未来 latent 要由历史预测，而真实未来只交给训练期的目标编码器？ 决策时真实未来尚未发生，直接用它作条件会造成泄漏。历史编码器预测未来分布，并通过重参数采样得到决策条件；EMA 目标只提供训练对齐信号。相同回报可能对应不同动力学，未来表征尝试补足单一 return-to-go 无法区分的信息。 例如两条轨迹都得十分，但一条将撞到障碍、另一条可通行；预测未来状态比仅给“目标十分”更能区分后续选择。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:dt-jepa" data-paper-title="DT-JEPA: Learning to Predict Future Representations for Decision-Making" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="DT-JEPA: Learning to Predict Future Representations for Decision-Making 基础模型 Southeast University 2026-10-23 传统DT用单个return-to-go条件，无法区分回报相同但未来动力学不同的轨迹。本方法将条件改成由历史预测的未来latent分布：历史encoder生成Gaussian参数，EMA target encoder只在训练期编码真实未来；重参数采样的预测未来通过独立gamma/beta MLP调制DT hidden。离线目标为BC加Gaussian NLL；在线通过双target critic的较小值构建多步target，并优化Q1指导的actor目标。 成本过高，不复现（审查 DONE）。D4RL共19个locomotion/navigation数据配置、主表5种子、多个未见reward的在线适配及基线/消融；附录DT4层/4头/512hidden、batch256/context20。原文未给总GPU小时，不臆测。完整offline+online矩阵超单卡短时预算，不安装MuJoCo、不下载轨迹、不启动环境试跑。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  JEPA与世界模型 未来表征与离线决策 多模态 世界建模：状态、生成与动作条件 预测高斯分布与直接用一个确定未来向量，有何建模取舍？ 高斯均值与方差允许表示不确定性，再经重参数采样调制 DT；确定向量只提供一个点条件。分布形式增加可训练的不确定性表达，但受对角高斯假设限制，不能因此声称可完整覆盖多峰未来，也不能把训练真实未来输入部署前向。 例如两条路都可能成功时，方差可反映预测不确定；但两个相距很远的离散目标未必能被单一高斯精确表达。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:dt-jepa" data-paper-title="DT-JEPA: Learning to Predict Future Representations for Decision-Making" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="DT-JEPA: Learning to Predict Future Representations for Decision-Making 基础模型 Southeast University 2026-10-23 传统DT用单个return-to-go条件，无法区分回报相同但未来动力学不同的轨迹。本方法将条件改成由历史预测的未来latent分布：历史encoder生成Gaussian参数，EMA target encoder只在训练期编码真实未来；重参数采样的预测未来通过独立gamma/beta MLP调制DT hidden。离线目标为BC加Gaussian NLL；在线通过双target critic的较小值构建多步target，并优化Q1指导的actor目标。 成本过高，不复现（审查 DONE）。D4RL共19个locomotion/navigation数据配置、主表5种子、多个未见reward的在线适配及基线/消融；附录DT4层/4头/512hidden、batch256/context20。原文未给总GPU小时，不臆测。完整offline+online矩阵超单卡短时预算，不安装MuJoCo、不下载轨迹、不启动环境试跑。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  JEPA与世界模型 未来表征与离线决策 多模态 世界建模：状态、生成与动作条件 NLL、BC 与 critic 的归约能都改成通用 MSE.mean 吗？ 不能。NLL 对 latent 维求和后批平均，BC 与 critic 对时间和动作维求和后批平均；归约改变会隐式改变损失相对权重。target 与 TD bootstrap 停止梯度，但 actor 的 Q 对动作梯度需保留，本地仅验证这些组件，不包含完整在线环境收集。 例如动作维翻倍时，全元素均值会缩小单样本总贡献；若其他项仍按维求和，原有权重关系就发生变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:uniaction" data-paper-title="UniAction: Unified Action Conditioning for World Models" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="UniAction: Unified Action Conditioning for World Models 多模态大模型 Stanford University 2026-10-23 异质动作以不同粒度编码，token较多的动作在同一softmax中会仅因数量而占据更大attention mass。UniAction以共享semantic codebook编码元素身份，将(t,y,x)送入既有视频模型的native positional mechanism，再对action部分统一加一个基数bias，保持action内部相对logits不变，同时移除总mass对Na的线性依赖。 成本过高，不复现（审查 DONE）。诊断回调仅证明参数传递，不能当成真实视频backbone位置实现。Wan2.2-I2V-A14B high-noise expert LoRA，GoalForce/SolarWM/EgoDex/DROID各10K clips，共40K段81帧480×832；410反事实生成、多个motion/pose估计器、4个专家和100人评测。完整视频训练/生成显著超过单A100/A30短时资源，不下载14B权重或40K视频，不试跑成本。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  世界模型与动作条件 统一动作表示 多模态 世界建模：状态、生成与动作条件 统一建模不同动作格式时，为什么 token 数量不应直接代表动作的重要性？ 不同动作可按不同粒度离散成 token，同一语义可能因编码更细而占更多位置。UniAction 区分元素身份与时空位置，并处理这种表示数量差异对联合注意力的影响。它约束的是编码粒度带来的偏置，新增真实动作仍可改变内容，不能把所有 token 增加都当成无意义复制。 教学例：同一移动轨迹分成十段或二十段，语义重要性未必翻倍；但若新增一次真正的抓取动作，模型当然应感知到新信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-multimodal-models-uniaction-704ab058" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-22a1c4fa397b7c64">统一建模不同动作格式时，为什么 token 数量不应直接代表动作的重要性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Auniaction">UniAction: Unified Action Conditioning for World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同动作可按不同粒度离散成 token，同一语义可能因编码更细而占更多位置。UniAction 区分元素身份与时空位置，并处理这种表示数量差异对联合注意力的影响。它约束的是编码粒度带来的偏置，新增真实动作仍可改变内容，不能把所有 token 增加都当成无意义复制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：同一移动轨迹分成十段或二十段，语义重要性未必翻倍；但若新增一次真正的抓取动作，模型当然应感知到新信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32977v1">原论文</a> · <a href="../../../../multimodal-models/2610.32977-uniaction/">实现解读</a> · <a href="#qa-22a1c4fa397b7c64">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:uniaction" data-paper-title="UniAction: Unified Action Conditioning for World Models" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="UniAction: Unified Action Conditioning for World Models 多模态大模型 Stanford University 2026-10-23 异质动作以不同粒度编码，token较多的动作在同一softmax中会仅因数量而占据更大attention mass。UniAction以共享semantic codebook编码元素身份，将(t,y,x)送入既有视频模型的native positional mechanism，再对action部分统一加一个基数bias，保持action内部相对logits不变，同时移除总mass对Na的线性依赖。 成本过高，不复现（审查 DONE）。诊断回调仅证明参数传递，不能当成真实视频backbone位置实现。Wan2.2-I2V-A14B high-noise expert LoRA，GoalForce/SolarWM/EgoDex/DROID各10K clips，共40K段81帧480×832；410反事实生成、多个motion/pose估计器、4个专家和100人评测。完整视频训练/生成显著超过单A100/A30短时资源，不下载14B权重或40K视频，不试跑成本。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  世界模型与动作条件 统一动作表示 多模态 世界建模：状态、生成与动作条件 为什么给 action logits 加 log(Nref/Na)，能抵消完全复制动作 Token 带来的注意力总权重变化？ 同一联合 softmax 中，复制相同 key/value 且位置编码相同，会增加重复项的指数和，使 action 总权重仅因数量变大。数量对应的对数偏置抵消这种重复，同时保留 action 内相对 logits；加入不同内容或不同位置的动作仍可合理改变输出。 例如把每个动作 token 连位置表示一起复制两份，未经校正动作会更占权重；校正后不应仅凭重复份数改变结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:uniaction" data-paper-title="UniAction: Unified Action Conditioning for World Models" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="UniAction: Unified Action Conditioning for World Models 多模态大模型 Stanford University 2026-10-23 异质动作以不同粒度编码，token较多的动作在同一softmax中会仅因数量而占据更大attention mass。UniAction以共享semantic codebook编码元素身份，将(t,y,x)送入既有视频模型的native positional mechanism，再对action部分统一加一个基数bias，保持action内部相对logits不变，同时移除总mass对Na的线性依赖。 成本过高，不复现（审查 DONE）。诊断回调仅证明参数传递，不能当成真实视频backbone位置实现。Wan2.2-I2V-A14B high-noise expert LoRA，GoalForce/SolarWM/EgoDex/DROID各10K clips，共40K段81帧480×832；410反事实生成、多个motion/pose估计器、4个专家和100人评测。完整视频训练/生成显著超过单A100/A30短时资源，不下载14B权重或40K视频，不试跑成本。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  世界模型与动作条件 统一动作表示 多模态 世界建模：状态、生成与动作条件 联合 softmax 校正与把视频、动作分别 softmax 后相加有何不同？ 联合 softmax 让两种信息在同一个归一化分母竞争，动作 logits 统一加 log(Nref/Na) 调节总量；分别归一化会各自总和为一，再相加形成另一种融合规则。两者即使动作内部排序相同，也不具有相同的跨模态权重。 例如视频证据很强、动作证据弱时，联合归一化可使动作总权重较小；分别归一化仍强行分配一整份动作权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:uniaction" data-paper-title="UniAction: Unified Action Conditioning for World Models" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="UniAction: Unified Action Conditioning for World Models 多模态大模型 Stanford University 2026-10-23 异质动作以不同粒度编码，token较多的动作在同一softmax中会仅因数量而占据更大attention mass。UniAction以共享semantic codebook编码元素身份，将(t,y,x)送入既有视频模型的native positional mechanism，再对action部分统一加一个基数bias，保持action内部相对logits不变，同时移除总mass对Na的线性依赖。 成本过高，不复现（审查 DONE）。诊断回调仅证明参数传递，不能当成真实视频backbone位置实现。Wan2.2-I2V-A14B high-noise expert LoRA，GoalForce/SolarWM/EgoDex/DROID各10K clips，共40K段81帧480×832；410反事实生成、多个motion/pose估计器、4个专家和100人评测。完整视频训练/生成显著超过单A100/A30短时资源，不下载14B权重或40K视频，不试跑成本。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  世界模型与动作条件 统一动作表示 多模态 世界建模：状态、生成与动作条件 复制不变性是否允许新增任意动作或改变位置编码？ 不允许。精确不变性要求复制的 key、value 及位置表示完全相同；不同新动作或不同位置可改变输出。Na 按每个请求的有效动作计数，padding 不计且 softmax 权重为零；native 位置回调必须显式提供，本地诊断回调不冒充 Wan 原生位置机制。 例如把同一动作复制到另一个时间点，位置表示变了就不再是完全复制，输出发生变化并不违反该不变性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:inside-jepa" data-paper-title="Inside-JEPA: From Prediction to Relational Grounding in Latent World Models" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Inside-JEPA: From Prediction to Relational Grounding in Latent World Models 基础模型 Australian Institute for Machine Learning, Adelaide University 2026-10-22 普通 JEPA 能预测潜在状态，但潜变量未必对应可解释关系。本文把每个有序实体对的关系通道直接拼入动态状态，并要求逆动态头根据前后关系通道恢复动作；预测损失的未来目标仍由 EMA 编码器提供，而逆动态的未来状态必须来自可反传的 online 编码器。仅预测、读全部状态、只读实体和打乱动作标签的对照用于区分信号来自哪里。原文 §3 该完整矩阵超出单 A100/A30/Mac 短时预算，成本过高，不复现（审查 DONE）；真实 crop、ResNet18、检测跟踪均由外部提供，当前未运行它们。RelationalStateEncoder 接收 [B,4,512] 冻结特征、[B,4,4] 归一化框、实体类型和共享实体 mask，本地组件每次调用最多64对帧；真实 crop、ResNet18、检测跟踪均由外部提供，当前未运行它们。InsideJEPA 实现预测器、可选离散/连续动作条件、五臂损失与显式 EMA 更新。  世界模型 JEPA 关系表示与逆动态 多模态 世界建模：状态、生成与动作条件 Inside-JEPA 为什么关注潜在状态能否表达“对象之间的关系”？ 世界模型可以预测向量变化，却未必把接触、相对位置等关系组织成可检查信息。Inside-JEPA 把实体与关系纳入状态，并研究动作监督如何塑造关系表示。可解释通道存在不等于语义已被学到，需要对照区分信号来源，不能用维度正确或预测 loss 低替代关系能力验证。 教学例：两个物体外观不变，但从分离变成接触，这种关系变化可能决定下一动作；仅识别物体类别并不足以描述。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-inside-jepa-840eadf0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c81bf3ff739be368">Inside-JEPA 为什么关注潜在状态能否表达“对象之间的关系”？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ainside-jepa">Inside-JEPA: From Prediction to Relational Grounding in Latent World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Australian Institute for Machine Learning, Adelaide University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>世界模型可以预测向量变化，却未必把接触、相对位置等关系组织成可检查信息。Inside-JEPA 把实体与关系纳入状态，并研究动作监督如何塑造关系表示。可解释通道存在不等于语义已被学到，需要对照区分信号来源，不能用维度正确或预测 loss 低替代关系能力验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：两个物体外观不变，但从分离变成接触，这种关系变化可能决定下一动作；仅识别物体类别并不足以描述。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与五臂；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31194v1">原论文</a> · <a href="../../../../foundation-models/2610.31194-inside-jepa/">实现解读</a> · <a href="#qa-c81bf3ff739be368">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:inside-jepa" data-paper-title="Inside-JEPA: From Prediction to Relational Grounding in Latent World Models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Inside-JEPA: From Prediction to Relational Grounding in Latent World Models 基础模型 Australian Institute for Machine Learning, Adelaide University 2026-10-22 普通 JEPA 能预测潜在状态，但潜变量未必对应可解释关系。本文把每个有序实体对的关系通道直接拼入动态状态，并要求逆动态头根据前后关系通道恢复动作；预测损失的未来目标仍由 EMA 编码器提供，而逆动态的未来状态必须来自可反传的 online 编码器。仅预测、读全部状态、只读实体和打乱动作标签的对照用于区分信号来自哪里。原文 §3 该完整矩阵超出单 A100/A30/Mac 短时预算，成本过高，不复现（审查 DONE）；真实 crop、ResNet18、检测跟踪均由外部提供，当前未运行它们。RelationalStateEncoder 接收 [B,4,512] 冻结特征、[B,4,4] 归一化框、实体类型和共享实体 mask，本地组件每次调用最多64对帧；真实 crop、ResNet18、检测跟踪均由外部提供，当前未运行它们。InsideJEPA 实现预测器、可选离散/连续动作条件、五臂损失与显式 EMA 更新。  世界模型 JEPA 关系表示与逆动态 多模态 世界建模：状态、生成与动作条件 为什么逆动态头的未来状态要来自可反传的 online 编码器，而非 EMA target？ 逆动态目标要把“哪些关系能解释动作”的信号传回表示层，若未来关系全停梯度，该侧就失去相应学习压力。JEPA 预测目标仍可使用稳定 EMA，但逆动态路径有不同梯度职责；还需通过只读实体、打乱动作等对照确认关系通道真正提供作用信息。 例如模型需根据移动前后的“杯子在盒子左侧”关系恢复动作；未来关系分支可反传，才能学会保留这种变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:inside-jepa" data-paper-title="Inside-JEPA: From Prediction to Relational Grounding in Latent World Models" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Inside-JEPA: From Prediction to Relational Grounding in Latent World Models 基础模型 Australian Institute for Machine Learning, Adelaide University 2026-10-22 普通 JEPA 能预测潜在状态，但潜变量未必对应可解释关系。本文把每个有序实体对的关系通道直接拼入动态状态，并要求逆动态头根据前后关系通道恢复动作；预测损失的未来目标仍由 EMA 编码器提供，而逆动态的未来状态必须来自可反传的 online 编码器。仅预测、读全部状态、只读实体和打乱动作标签的对照用于区分信号来自哪里。原文 §3 该完整矩阵超出单 A100/A30/Mac 短时预算，成本过高，不复现（审查 DONE）；真实 crop、ResNet18、检测跟踪均由外部提供，当前未运行它们。RelationalStateEncoder 接收 [B,4,512] 冻结特征、[B,4,4] 归一化框、实体类型和共享实体 mask，本地组件每次调用最多64对帧；真实 crop、ResNet18、检测跟踪均由外部提供，当前未运行它们。InsideJEPA 实现预测器、可选离散/连续动作条件、五臂损失与显式 EMA 更新。  世界模型 JEPA 关系表示与逆动态 多模态 世界建模：状态、生成与动作条件 INV-S、INV-R 与打乱标签控制分别用来区分什么信号？ INV-S 让逆动态只读关系通道，INV-R 只读实体 latent，可检查动作监督是否直接塑造关系；打乱标签臂只打乱 inverse 目标，而预测器仍读真实动作。它们是监督来源控制，不能简单将任意辅助头增益都解释为关系 grounding。 例如随机动作标签也能带来相似变化时，就需警惕收益来自一般正则而非正确动作与关系变化的对应。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:inside-jepa" data-paper-title="Inside-JEPA: From Prediction to Relational Grounding in Latent World Models" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Inside-JEPA: From Prediction to Relational Grounding in Latent World Models 基础模型 Australian Institute for Machine Learning, Adelaide University 2026-10-22 普通 JEPA 能预测潜在状态，但潜变量未必对应可解释关系。本文把每个有序实体对的关系通道直接拼入动态状态，并要求逆动态头根据前后关系通道恢复动作；预测损失的未来目标仍由 EMA 编码器提供，而逆动态的未来状态必须来自可反传的 online 编码器。仅预测、读全部状态、只读实体和打乱动作标签的对照用于区分信号来自哪里。原文 §3 该完整矩阵超出单 A100/A30/Mac 短时预算，成本过高，不复现（审查 DONE）；真实 crop、ResNet18、检测跟踪均由外部提供，当前未运行它们。RelationalStateEncoder 接收 [B,4,512] 冻结特征、[B,4,4] 归一化框、实体类型和共享实体 mask，本地组件每次调用最多64对帧；真实 crop、ResNet18、检测跟踪均由外部提供，当前未运行它们。InsideJEPA 实现预测器、可选离散/连续动作条件、五臂损失与显式 EMA 更新。  世界模型 JEPA 关系表示与逆动态 多模态 世界建模：状态、生成与动作条件 四实体 K=8 的状态为什么是 256 维，而不是删对角后的 224 维？ 实体 latent 为 4×32，有序对槽为 4×4×8，合计 256；padding 和对角槽固定零但仍保留形状。JEPA 未来目标来自 EMA 并停止梯度，inverse 的未来状态必须来自可反传 online 编码器；将二者混用会切断定义性训练信号。 例如把对角关系值设零不会删除那三十二个槽；若顺手移除它们，预测器输入维度与论文合同就不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:alps" data-paper-title="ALPS: Visual State Encoders for World Models" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="ALPS: Visual State Encoders for World Models 基础模型 University of California, Santa Cruz 2026-10-21 世界模型以视觉 token 为状态进行预测和规划，但一个编码器通常只擅长物理状态、语言对齐或像素重建中的一部分。ALPS 尝试让同一组 patch token 同时承担三种接口：机器人状态探针能读出位置，文字指令能对应图像，而未来 token 能被解码成图像以便检查。第一阶段从零训练 ViT-B/16：同一组未做最终 LayerNorm 的 patch token接受图文对比、caption、自重建和密集跨裁剪对应四种监督。第二阶段将第一阶段 encoder 同时用作学生初始化和固定教师； 完整预训练和实验成本过高，不复现（审查 DONE），not_reproduced_high_cost 为终态，不下载大模型/训练数据、不试探性跑完整训练、不自动重试。诊断使用两组裁剪、patch、8 维 query 和 6 维随机 token。输入会检查 shape、有限值、正尺度、裁剪范围和标准差；不静默修正无效数据。模块导入不要求 torch，执行时才加载；不联网、不自动安装依赖、不执行上游脚本或下载 checkpoint。正式评测必须将训练统计与测试轨迹隔离，验证集选参，测试集只用于最终报告。  视觉表征与世界模型 联合嵌入与自监督学习 多模态 世界建模：状态、生成与动作条件 ALPS 为什么希望一个视觉表示同时适合语言理解、状态预测和图像检查？ 世界模型规划需要表示可预测，指令任务需要语言对齐，检查预测结果又需要能恢复可读图像，单一目标训练可能只满足一部分。ALPS 研究让同一组 patch token 兼顾这些接口。多接口可读性仍要各自验证，能重建像素不能自动证明可规划，语言对齐也不保证物理状态完整。 教学例：机器人既要理解“把杯子移到右边”，又要预测位置并检查未来画面；若每种用途都需完全不同表示，接口会难以衔接。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-alps-4489dea8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-3824083e7eb834df">ALPS 为什么希望一个视觉表示同时适合语言理解、状态预测和图像检查？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aalps">ALPS: Visual State Encoders for World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Santa Cruz</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>世界模型规划需要表示可预测，指令任务需要语言对齐，检查预测结果又需要能恢复可读图像，单一目标训练可能只满足一部分。ALPS 研究让同一组 patch token 兼顾这些接口。多接口可读性仍要各自验证，能重建像素不能自动证明可规划，语言对齐也不保证物理状态完整。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：机器人既要理解“把杯子移到右边”，又要预测位置并检查未来画面；若每种用途都需完全不同表示，接口会难以衔接。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30120v1">原论文</a> · <a href="../../../../foundation-models/2610.30120-alps/">实现解读</a> · <a href="#qa-3824083e7eb834df">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:alps" data-paper-title="ALPS: Visual State Encoders for World Models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="ALPS: Visual State Encoders for World Models 基础模型 University of California, Santa Cruz 2026-10-21 世界模型以视觉 token 为状态进行预测和规划，但一个编码器通常只擅长物理状态、语言对齐或像素重建中的一部分。ALPS 尝试让同一组 patch token 同时承担三种接口：机器人状态探针能读出位置，文字指令能对应图像，而未来 token 能被解码成图像以便检查。第一阶段从零训练 ViT-B/16：同一组未做最终 LayerNorm 的 patch token接受图文对比、caption、自重建和密集跨裁剪对应四种监督。第二阶段将第一阶段 encoder 同时用作学生初始化和固定教师； 完整预训练和实验成本过高，不复现（审查 DONE），not_reproduced_high_cost 为终态，不下载大模型/训练数据、不试探性跑完整训练、不自动重试。诊断使用两组裁剪、patch、8 维 query 和 6 维随机 token。输入会检查 shape、有限值、正尺度、裁剪范围和标准差；不静默修正无效数据。模块导入不要求 torch，执行时才加载；不联网、不自动安装依赖、不执行上游脚本或下载 checkpoint。正式评测必须将训练统计与测试轨迹隔离，验证集选参，测试集只用于最终报告。  视觉表征与世界模型 联合嵌入与自监督学习 多模态 世界建模：状态、生成与动作条件 第二阶段为什么只监督教师裁剪 B 中落在学生裁剪 A 内的 patch？ 学生只看得到 A，要求它逐点预测完全不在视野内的 B 区域会把不可见内容也当成确定监督。几何映射先找可对应位置，再预测固定教师的目标，外观增强则训练鲁棒表示；教师固定与学生初始化相同，不意味着训练中两者会一起更新。 例如学生只看到图片左半边，教师裁剪横跨左右；应只监督二者重叠部分，而不能要求学生精确读出右侧从未见到的小字。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:alps" data-paper-title="ALPS: Visual State Encoders for World Models" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="ALPS: Visual State Encoders for World Models 基础模型 University of California, Santa Cruz 2026-10-21 世界模型以视觉 token 为状态进行预测和规划，但一个编码器通常只擅长物理状态、语言对齐或像素重建中的一部分。ALPS 尝试让同一组 patch token 同时承担三种接口：机器人状态探针能读出位置，文字指令能对应图像，而未来 token 能被解码成图像以便检查。第一阶段从零训练 ViT-B/16：同一组未做最终 LayerNorm 的 patch token接受图文对比、caption、自重建和密集跨裁剪对应四种监督。第二阶段将第一阶段 encoder 同时用作学生初始化和固定教师； 完整预训练和实验成本过高，不复现（审查 DONE），not_reproduced_high_cost 为终态，不下载大模型/训练数据、不试探性跑完整训练、不自动重试。诊断使用两组裁剪、patch、8 维 query 和 6 维随机 token。输入会检查 shape、有限值、正尺度、裁剪范围和标准差；不静默修正无效数据。模块导入不要求 torch，执行时才加载；不联网、不自动安装依赖、不执行上游脚本或下载 checkpoint。正式评测必须将训练统计与测试轨迹隔离，验证集选参，测试集只用于最终报告。  视觉表征与世界模型 联合嵌入与自监督学习 多模态 世界建模：状态、生成与动作条件 固定 Stage1 教师与 EMA 教师在第二阶段各意味着什么？ ALPS 用 Stage1 模型作为学生初始化和固定教师，教师在第二阶段不随学生更新。EMA 教师则会按学生参数持续移动，目标分布不同；不能把常见 JEPA 的 EMA 习惯套进 ALPS。训练后丢弃跨视图预测器，部署保留学生 encoder 和语言接口。 例如学生为增强鲁棒性发生变化时，固定教师仍提供同一干净裁剪目标；EMA 设置会让这些目标随训练一起漂移。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:alps" data-paper-title="ALPS: Visual State Encoders for World Models" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="ALPS: Visual State Encoders for World Models 基础模型 University of California, Santa Cruz 2026-10-21 世界模型以视觉 token 为状态进行预测和规划，但一个编码器通常只擅长物理状态、语言对齐或像素重建中的一部分。ALPS 尝试让同一组 patch token 同时承担三种接口：机器人状态探针能读出位置，文字指令能对应图像，而未来 token 能被解码成图像以便检查。第一阶段从零训练 ViT-B/16：同一组未做最终 LayerNorm 的 patch token接受图文对比、caption、自重建和密集跨裁剪对应四种监督。第二阶段将第一阶段 encoder 同时用作学生初始化和固定教师； 完整预训练和实验成本过高，不复现（审查 DONE），not_reproduced_high_cost 为终态，不下载大模型/训练数据、不试探性跑完整训练、不自动重试。诊断使用两组裁剪、patch、8 维 query 和 6 维随机 token。输入会检查 shape、有限值、正尺度、裁剪范围和标准差；不静默修正无效数据。模块导入不要求 torch，执行时才加载；不联网、不自动安装依赖、不执行上游脚本或下载 checkpoint。正式评测必须将训练统计与测试轨迹隔离，验证集选参，测试集只用于最终报告。  视觉表征与世界模型 联合嵌入与自监督学习 多模态 世界建模：状态、生成与动作条件 跨裁剪损失为什么先按图平均有效 patch，再对 batch 平均？ 每图重叠区域大小不同，先做图内均值可避免重叠更多的图自动占更大权重。有效性由 B 的 patch 中心是否落入 A 的半开区间决定；无重叠时损失安全贡献零，训练采样器另有最小有效数要求，不能把安全分母当完整采样策略。 例如甲图重叠一百格、乙图十格，整体 token 平均会让甲权重十倍；逐图平均让两张图各贡献一个样本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:aw0" data-paper-title="Agentic World Action Models" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Agentic World Action Models 多模态大模型 UC Berkeley 2026-10-21 世界动作模型能预测未来视觉和控制轨迹，但通常缺少可组合的技能结构；代码型机器人 Agent 能重用程序，却未必把计划与物理动态预测统一起来。AW-0 在 Mixture-of-Transformers 中组合三个专家：代码专家产生参数化程序片段，视频专家预测未来场景，动作专家产生连续控制。程序既能约束预测，也可在可选执行模式中调用技能库。每个专家有独立投影、归一化与 FFN，通过每层联合注意力交换信息；专家内部双向、专家之间按代码→视频→动作分块因果。 原始训练与完整对照矩阵明显超出低成本预算，且真实硬件和未随 release 提供的语料无法由合成 fixture 替代，因此成本过高，不复现（审查 DONE）。本地未验证、未生成预测，也没有生产搜广推线上 A/B 证据。本页、原论文 Figure 2、完整作者/代码元数据、成本依据和终态 catalog 已收录。没有运行 adapter、低成本 proxy、benchmark 指标或 GPU 验证收据；也不把“找到开源代码”当作复现完成。promotion_eligible=false、evolve_integrated=false，不进入 Evolve 训练或自动选参。  视频理解与世界模型 具身技能与联合动作生成 多模态 世界建模：状态、生成与动作条件 AW-0 为什么试图把可组合程序、未来视觉和机器人动作放在一个模型里？ 程序能表达可复用步骤，视频预测提供未来场景，连续动作负责真实控制，分别建模未必能把计划与物理后果联系好。AW-0 用三个专家联合生成这些对象，默认代码提供计划而非直接执行。实际效果还受视觉预测、动作质量和执行模式限制，本地仅完成资料审查。 教学例：整理物品可有程序级“抓取再放置”，同时预测下一场景并生成控制；默认产生的代码不意味着系统会直接运行任意 Python。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-multimodal-models-aw0-c41ecc38" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-63a711c06d27630b">AW-0 为什么试图把可组合程序、未来视觉和机器人动作放在一个模型里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Aaw0">Agentic World Action Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>程序能表达可复用步骤，视频预测提供未来场景，连续动作负责真实控制，分别建模未必能把计划与物理后果联系好。AW-0 用三个专家联合生成这些对象，默认代码提供计划而非直接执行。实际效果还受视觉预测、动作质量和执行模式限制，本地仅完成资料审查。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：整理物品可有程序级“抓取再放置”，同时预测下一场景并生成控制；默认产生的代码不意味着系统会直接运行任意 Python。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30136v1">原论文</a> · <a href="../../../../multimodal-models/2610.30136-aw0/">实现解读</a> · <a href="#qa-63a711c06d27630b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:aw0" data-paper-title="Agentic World Action Models" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Agentic World Action Models 多模态大模型 UC Berkeley 2026-10-21 世界动作模型能预测未来视觉和控制轨迹，但通常缺少可组合的技能结构；代码型机器人 Agent 能重用程序，却未必把计划与物理动态预测统一起来。AW-0 在 Mixture-of-Transformers 中组合三个专家：代码专家产生参数化程序片段，视频专家预测未来场景，动作专家产生连续控制。程序既能约束预测，也可在可选执行模式中调用技能库。每个专家有独立投影、归一化与 FFN，通过每层联合注意力交换信息；专家内部双向、专家之间按代码→视频→动作分块因果。 原始训练与完整对照矩阵明显超出低成本预算，且真实硬件和未随 release 提供的语料无法由合成 fixture 替代，因此成本过高，不复现（审查 DONE）。本地未验证、未生成预测，也没有生产搜广推线上 A/B 证据。本页、原论文 Figure 2、完整作者/代码元数据、成本依据和终态 catalog 已收录。没有运行 adapter、低成本 proxy、benchmark 指标或 GPU 验证收据；也不把“找到开源代码”当作复现完成。promotion_eligible=false、evolve_integrated=false，不进入 Evolve 训练或自动选参。  视频理解与世界模型 具身技能与联合动作生成 多模态 世界建模：状态、生成与动作条件 AW-0 为什么允许专家内部双向交互，却把专家之间限制为代码→视频→动作？ 内部双向交互有利于同一模态组织完整表示，跨专家分块因果则保持计划、场景预测与动作的条件方向。代码不应提前读取后续视频或动作来伪装规划，动作却可利用代码与预测场景；完全互读会改变信息可用性及推理时的执行顺序。 例如先生成“抓取杯子”的程序，视频专家据此预测场景，动作专家再产出控制；不能让程序先偷看真实未来动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:aw0" data-paper-title="Agentic World Action Models" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Agentic World Action Models 多模态大模型 UC Berkeley 2026-10-21 世界动作模型能预测未来视觉和控制轨迹，但通常缺少可组合的技能结构；代码型机器人 Agent 能重用程序，却未必把计划与物理动态预测统一起来。AW-0 在 Mixture-of-Transformers 中组合三个专家：代码专家产生参数化程序片段，视频专家预测未来场景，动作专家产生连续控制。程序既能约束预测，也可在可选执行模式中调用技能库。每个专家有独立投影、归一化与 FFN，通过每层联合注意力交换信息；专家内部双向、专家之间按代码→视频→动作分块因果。 原始训练与完整对照矩阵明显超出低成本预算，且真实硬件和未随 release 提供的语料无法由合成 fixture 替代，因此成本过高，不复现（审查 DONE）。本地未验证、未生成预测，也没有生产搜广推线上 A/B 证据。本页、原论文 Figure 2、完整作者/代码元数据、成本依据和终态 catalog 已收录。没有运行 adapter、低成本 proxy、benchmark 指标或 GPU 验证收据；也不把“找到开源代码”当作复现完成。promotion_eligible=false、evolve_integrated=false，不进入 Evolve 训练或自动选参。  视频理解与世界模型 具身技能与联合动作生成 多模态 世界建模：状态、生成与动作条件 三专家各有投影、归一化与 FFN，与完全共用一套模态变换有什么区别？ 独立变换给代码、视频和动作各自的表示处理路径，联合注意力再按规定边界交换信息；完全共享则对不同模态使用同一套参数映射。前者表达了模态分工，也增加参数与接口管理，不能据结构推断必然更好。原文是专家内部双向、专家之间分块因果的具体组合。 教学例：离散程序 token 与连续动作可以各用自己的 FFN，但仍通过联合注意力衔接；这不等于三份模型完全隔绝或完全互读。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-80ec646f7634554a">三专家各有投影、归一化与 FFN，与完全共用一套模态变换有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Aaw0">Agentic World Action Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立变换给代码、视频和动作各自的表示处理路径，联合注意力再按规定边界交换信息；完全共享则对不同模态使用同一套参数映射。前者表达了模态分工，也增加参数与接口管理，不能据结构推断必然更好。原文是专家内部双向、专家之间分块因果的具体组合。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：离散程序 token 与连续动作可以各用自己的 FFN，但仍通过联合注意力衔接；这不等于三份模型完全隔绝或完全互读。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30136v1">原论文</a> · <a href="../../../../multimodal-models/2610.30136-aw0/">实现解读</a> · <a href="#qa-80ec646f7634554a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:aw0" data-paper-title="Agentic World Action Models" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Agentic World Action Models 多模态大模型 UC Berkeley 2026-10-21 世界动作模型能预测未来视觉和控制轨迹，但通常缺少可组合的技能结构；代码型机器人 Agent 能重用程序，却未必把计划与物理动态预测统一起来。AW-0 在 Mixture-of-Transformers 中组合三个专家：代码专家产生参数化程序片段，视频专家预测未来场景，动作专家产生连续控制。程序既能约束预测，也可在可选执行模式中调用技能库。每个专家有独立投影、归一化与 FFN，通过每层联合注意力交换信息；专家内部双向、专家之间按代码→视频→动作分块因果。 原始训练与完整对照矩阵明显超出低成本预算，且真实硬件和未随 release 提供的语料无法由合成 fixture 替代，因此成本过高，不复现（审查 DONE）。本地未验证、未生成预测，也没有生产搜广推线上 A/B 证据。本页、原论文 Figure 2、完整作者/代码元数据、成本依据和终态 catalog 已收录。没有运行 adapter、低成本 proxy、benchmark 指标或 GPU 验证收据；也不把“找到开源代码”当作复现完成。promotion_eligible=false、evolve_integrated=false，不进入 Evolve 训练或自动选参。  视频理解与世界模型 具身技能与联合动作生成 多模态 世界建模：状态、生成与动作条件 连续 flow 目标与代码 masked diffusion 能使用同一噪声和监督 mask 吗？ 不能。视频与动作采用连续加噪及速度回归，代码采用独立 Bernoulli mask，只监督被遮挡程序 token；动作噪声与代码 mask 也不由视频噪声统一决定。视频混合采样还需不同重要性权重并截断归一化，单个 flow loss 不能代表完整训练。 例如视频噪声较低不意味着程序也只能遮少量 token；若三者共用一个随机 mask，就改变了论文规定的独立采样关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:locale-jepa" data-paper-title="LocaLeJEPA: Maximum Entropy Representations under Geometric Priors" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="LocaLeJEPA: Maximum Entropy Representations under Geometric Priors 基础模型 University of Pennsylvania 2026-10-20 LeJEPA 将整体表示推向各向同性高斯；当表示本身具有局部流形、双曲或等变几何时，单一全局分布不一定合适。LocaLeJEPA 不改写为另一种高斯损失，而是将每个 batch 的多视图平均表示分簇，在各簇内分别匹配均匀球分布。各簇位置不被拉向共同原点，局部形状通过重中心后的残差约束。 完整实验标注成本过高，不复现（审查 DONE），不下载、不试跑、不进入自动训练队列。3 seed 不改变 L1 诊断资格，无正式 capability comparison、无 Evolve 晋级。已实现 uniform_ball_cf、ballreg_loss、torch_kmeans_labels、local_ballreg_loss 和 locale_jepa_loss。前向真实计算局部均匀球统计并反向传播至投影；仅分簇赋值 detached，预测均值和重中心残差没有 stop-gradient。采用作者官方 pure-torch k-means 路径，不额外引入聚类依赖。  JEPA与世界模型 局部均匀球分布匹配 多模态 世界建模：状态、生成与动作条件 同一图像的不同视图越相似，为什么还要防止所有图像都变成同一个表示？ 跨视图一致让模型忽略增强噪声，但如果所有输入都输出常量，也能轻易达到一致。LocaLeJEPA 同时关心表示多样性，并考虑数据可能具有局部几何结构。两项需求分别是同对象稳定与不同对象可区分，不能把一致性 loss 低直接当成表示已学到有用信息。 教学例：猫的两种裁剪应相近，但猫和汽车若也全部变成同一向量，检索和分类就没有可用差别，尽管跨视图误差很低。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-locale-jepa-ba12e8f4" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-3d704fc3d2d42061">同一图像的不同视图越相似，为什么还要防止所有图像都变成同一个表示？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alocale-jepa">LocaLeJEPA: Maximum Entropy Representations under Geometric Priors</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pennsylvania</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>跨视图一致让模型忽略增强噪声，但如果所有输入都输出常量，也能轻易达到一致。LocaLeJEPA 同时关心表示多样性，并考虑数据可能具有局部几何结构。两项需求分别是同对象稳定与不同对象可区分，不能把一致性 loss 低直接当成表示已学到有用信息。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：猫的两种裁剪应相近，但猫和汽车若也全部变成同一向量，检索和分类就没有可用差别，尽管跨视图误差很低。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28458v1">原论文</a> · <a href="../../../../foundation-models/2610.28458-locale-jepa/">实现解读</a> · <a href="#qa-3d704fc3d2d42061">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:locale-jepa" data-paper-title="LocaLeJEPA: Maximum Entropy Representations under Geometric Priors" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="LocaLeJEPA: Maximum Entropy Representations under Geometric Priors 基础模型 University of Pennsylvania 2026-10-20 LeJEPA 将整体表示推向各向同性高斯；当表示本身具有局部流形、双曲或等变几何时，单一全局分布不一定合适。LocaLeJEPA 不改写为另一种高斯损失，而是将每个 batch 的多视图平均表示分簇，在各簇内分别匹配均匀球分布。各簇位置不被拉向共同原点，局部形状通过重中心后的残差约束。 完整实验标注成本过高，不复现（审查 DONE），不下载、不试跑、不进入自动训练队列。3 seed 不改变 L1 诊断资格，无正式 capability comparison、无 Evolve 晋级。已实现 uniform_ball_cf、ballreg_loss、torch_kmeans_labels、local_ballreg_loss 和 locale_jepa_loss。前向真实计算局部均匀球统计并反向传播至投影；仅分簇赋值 detached，预测均值和重中心残差没有 stop-gradient。采用作者官方 pure-torch k-means 路径，不额外引入聚类依赖。  JEPA与世界模型 局部均匀球分布匹配 多模态 世界建模：状态、生成与动作条件 为什么 LocaLeJEPA 不把所有簇都直接拉向同一个高斯分布？ 不同局部簇可能对应具有自身几何的状态，把它们统一拉向原点会破坏簇间位置和局部结构。方法先固定分组，再对各簇重中心残差匹配均匀球体分布，保留整体布局；簇太小时还要明确回退，不能把目标偷换为普通全局高斯正则。 例如两团表示分别对应两种运动模式，各自分散但位置不同；约束局部形状无需把两团的中心都拉到同一点。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:locale-jepa" data-paper-title="LocaLeJEPA: Maximum Entropy Representations under Geometric Priors" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="LocaLeJEPA: Maximum Entropy Representations under Geometric Priors 基础模型 University of Pennsylvania 2026-10-20 LeJEPA 将整体表示推向各向同性高斯；当表示本身具有局部流形、双曲或等变几何时，单一全局分布不一定合适。LocaLeJEPA 不改写为另一种高斯损失，而是将每个 batch 的多视图平均表示分簇，在各簇内分别匹配均匀球分布。各簇位置不被拉向共同原点，局部形状通过重中心后的残差约束。 完整实验标注成本过高，不复现（审查 DONE），不下载、不试跑、不进入自动训练队列。3 seed 不改变 L1 诊断资格，无正式 capability comparison、无 Evolve 晋级。已实现 uniform_ball_cf、ballreg_loss、torch_kmeans_labels、local_ballreg_loss 和 locale_jepa_loss。前向真实计算局部均匀球统计并反向传播至投影；仅分簇赋值 detached，预测均值和重中心残差没有 stop-gradient。采用作者官方 pure-torch k-means 路径，不额外引入聚类依赖。  JEPA与世界模型 局部均匀球分布匹配 多模态 世界建模：状态、生成与动作条件 均匀实心球目标与高斯或单位球面目标有什么区别？ 均匀实心球把概率分布在球体内部，半径取根号 d+2 使协方差为单位阵；高斯无界，球面则只在固定半径上有质量。三者特征函数不同，LocaLeJEPA 的目标不能由高斯公式或向量单位化代替。 例如二维均匀圆盘含中心附近样本，圆周分布没有内部质量，高斯还会在任意大半径出现样本；它们并非同一正则。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:locale-jepa" data-paper-title="LocaLeJEPA: Maximum Entropy Representations under Geometric Priors" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="LocaLeJEPA: Maximum Entropy Representations under Geometric Priors 基础模型 University of Pennsylvania 2026-10-20 LeJEPA 将整体表示推向各向同性高斯；当表示本身具有局部流形、双曲或等变几何时，单一全局分布不一定合适。LocaLeJEPA 不改写为另一种高斯损失，而是将每个 batch 的多视图平均表示分簇，在各簇内分别匹配均匀球分布。各簇位置不被拉向共同原点，局部形状通过重中心后的残差约束。 完整实验标注成本过高，不复现（审查 DONE），不下载、不试跑、不进入自动训练队列。3 seed 不改变 L1 诊断资格，无正式 capability comparison、无 Evolve 晋级。已实现 uniform_ball_cf、ballreg_loss、torch_kmeans_labels、local_ballreg_loss 和 locale_jepa_loss。前向真实计算局部均匀球统计并反向传播至投影；仅分簇赋值 detached，预测均值和重中心残差没有 stop-gradient。采用作者官方 pure-torch k-means 路径，不额外引入聚类依赖。  JEPA与世界模型 局部均匀球分布匹配 多模态 世界建模：状态、生成与动作条件 小簇过滤与簇数变化为什么影响有效正则强度？ 只保留至少四样本的簇，无有效簇时回退全 batch 并记录。各簇统计先乘其样本数，再对有效簇和视图等权平均，因此改变簇数不只是改变局部粒度，也改变损失尺度；积分采用球特征函数，不能把高斯窗口误作目标分布。 例如拆成更多有效小簇后，等权平均与样本数因子共同改变数值；沿用同一 λ 也不保证正则力度相同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ppmem" data-paper-title="Persistent Planar Memory for Video World Models" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Persistent Planar Memory for Video World Models 基础模型 Tsinghua University 2026-10-16 长视频生成若只保存少量历史帧，跨视角回访容易遗忘场景；持续保存全部像素点云又非常大。PPMem把场景记忆压成可光栅化的平面primitive，在视频生成过程中由同一骨干联合预测，再通过持久pool向后续chunk反馈深度。每个局部平面用中心深度、两个矩形尺度和四元数共7个参数表示，变换到世界坐标后合并。pool按遮挡投票删除错误旧面，按观察质量去重，并依据已给定的下一段相机轨迹提前淘汰即将被更好观测替换的面；它不是读取未来真实视频。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。没有本地世界模型、训练结果或Evolve能力算子。本轮只核原文方法、元数据、结果归属及成本，不下载模型或视频，不制造小张量“世界模型能力”分数。没有GPU回执要求，因为没有接受执行CUDA实现。  多模态基础模型 世界模型与持久三维记忆 多模态 世界建模：状态、生成与动作条件 长视频生成为什么在镜头回到旧位置时，容易忘记原来的场景布局？ 只条件化少量近期帧会丢掉更早看过的几何，保存全部像素或点云又成本很高。PPMem 研究用紧凑、可光栅化的平面场景记忆接续视频 chunk，使回访有可用空间依据。平面是近似表示，遮挡和错误几何仍需维护，不能从持久存储直接推断生成完全一致。 教学例：镜头先离开书桌再转回，书架不应无故换位置；近期帧看不到书架时，持久场景记忆可提供几何条件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-ppmem-5417d641" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4111c1cac44a1ce5">长视频生成为什么在镜头回到旧位置时，容易忘记原来的场景布局？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Appmem">Persistent Planar Memory for Video World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只条件化少量近期帧会丢掉更早看过的几何，保存全部像素或点云又成本很高。PPMem 研究用紧凑、可光栅化的平面场景记忆接续视频 chunk，使回访有可用空间依据。平面是近似表示，遮挡和错误几何仍需维护，不能从持久存储直接推断生成完全一致。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：镜头先离开书桌再转回，书架不应无故换位置；近期帧看不到书架时，持久场景记忆可提供几何条件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与流程；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23795">原论文</a> · <a href="../../../../foundation-models/2610.23795-ppmem/">实现解读</a> · <a href="#qa-4111c1cac44a1ce5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ppmem" data-paper-title="Persistent Planar Memory for Video World Models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Persistent Planar Memory for Video World Models 基础模型 Tsinghua University 2026-10-16 长视频生成若只保存少量历史帧，跨视角回访容易遗忘场景；持续保存全部像素点云又非常大。PPMem把场景记忆压成可光栅化的平面primitive，在视频生成过程中由同一骨干联合预测，再通过持久pool向后续chunk反馈深度。每个局部平面用中心深度、两个矩形尺度和四元数共7个参数表示，变换到世界坐标后合并。pool按遮挡投票删除错误旧面，按观察质量去重，并依据已给定的下一段相机轨迹提前淘汰即将被更好观测替换的面；它不是读取未来真实视频。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。没有本地世界模型、训练结果或Evolve能力算子。本轮只核原文方法、元数据、结果归属及成本，不下载模型或视频，不制造小张量“世界模型能力”分数。没有GPU回执要求，因为没有接受执行CUDA实现。  多模态基础模型 世界模型与持久三维记忆 多模态 世界建模：状态、生成与动作条件 依据下一段相机轨迹淘汰平面，为什么不等于读取未来真实视频？ 相机轨迹可以是生成任务已给定的控制条件，它说明之后将朝哪里看，并不提供那里的真实图像。平面池据此管理将被更好观测替换的几何，后续视频仍需模型生成；只有把未知未来观测或真值几何提前送入记忆，才构成另一种信息泄漏。 例如用户预先指定镜头绕桌子一圈，系统可据轨迹安排记忆；它仍不知道桌子背面的真实纹理，不能当成已经看到。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ppmem" data-paper-title="Persistent Planar Memory for Video World Models" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Persistent Planar Memory for Video World Models 基础模型 Tsinghua University 2026-10-16 长视频生成若只保存少量历史帧，跨视角回访容易遗忘场景；持续保存全部像素点云又非常大。PPMem把场景记忆压成可光栅化的平面primitive，在视频生成过程中由同一骨干联合预测，再通过持久pool向后续chunk反馈深度。每个局部平面用中心深度、两个矩形尺度和四元数共7个参数表示，变换到世界坐标后合并。pool按遮挡投票删除错误旧面，按观察质量去重，并依据已给定的下一段相机轨迹提前淘汰即将被更好观测替换的面；它不是读取未来真实视频。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。没有本地世界模型、训练结果或Evolve能力算子。本轮只核原文方法、元数据、结果归属及成本，不下载模型或视频，不制造小张量“世界模型能力”分数。没有GPU回执要求，因为没有接受执行CUDA实现。  多模态基础模型 世界模型与持久三维记忆 多模态 世界建模：状态、生成与动作条件 持久平面池与仅保留近期帧作为生成条件有什么差别？ 近期帧记忆容易在长时间离开某区域后忘记场景，世界坐标 pool 可在相机回访时继续提供几何条件。它还需遮挡投票、质量去重及淘汰维护，不能把不断追加平面当完整机制；已知未来相机轨迹也不等于读取未来真实视频。 例如镜头绕房间一圈后回到起点，旧墙面可仍在 pool 中；淘汰决策可知道下一段相机位置，却不知道未来真实像素。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ppmem" data-paper-title="Persistent Planar Memory for Video World Models" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Persistent Planar Memory for Video World Models 基础模型 Tsinghua University 2026-10-16 长视频生成若只保存少量历史帧，跨视角回访容易遗忘场景；持续保存全部像素点云又非常大。PPMem把场景记忆压成可光栅化的平面primitive，在视频生成过程中由同一骨干联合预测，再通过持久pool向后续chunk反馈深度。每个局部平面用中心深度、两个矩形尺度和四元数共7个参数表示，变换到世界坐标后合并。pool按遮挡投票删除错误旧面，按观察质量去重，并依据已给定的下一段相机轨迹提前淘汰即将被更好观测替换的面；它不是读取未来真实视频。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。没有本地世界模型、训练结果或Evolve能力算子。本轮只核原文方法、元数据、结果归属及成本，不下载模型或视频，不制造小张量“世界模型能力”分数。没有GPU回执要求，因为没有接受执行CUDA实现。  多模态基础模型 世界模型与持久三维记忆 多模态 世界建模：状态、生成与动作条件 几何 LoRA 是在每个视频去噪步都开启吗？ 不是。视频去噪使用 Stage1 冻结骨干并关闭几何 LoRA，视频生成完成后额外开启一次几何前向提取平面。两阶段训练还有深度、法线、光栅化与平滑目标，前千步不启用光栅化损失；当前本地仅资料收录，没有执行世界模型。 例如生成二十五帧 chunk 的多个去噪步不逐步更新平面；结束后一次几何提取再合并 pool，流程不同于每步联训几何。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ego-p2c" data-paper-title="EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video 基础模型 Arizona State University 2026-10-15 第一视角视频空间推理既要提问、采集证据，也要保证感知回答可靠。固定外部视觉工具无法随推理策略一起改进；把规划与感知压到同一组参数中又可能引入梯度冲突。EgoP²C先在冻结VLM上分别训练规划/组合（PC）与感知（V）的LoRA教师，再复制选定FFN形成PC、V、通用直接回答（G）专家。学生自己生成交互片段，由相应冻结教师实时评价同一批学生tokens，而非模仿教师另行生成的答案。公共视频前缀始终走冻结基础路径；角色私有文字、选项和历史不混入公共KV。 完整实验成本过高，不复现（审查 DONE）。本地保留真实角色FFN复制、q/k/v/o低秩残差、因果attention、公共前缀冻结、严格参数冻结、完整词表打分及上述损失。使用12维单层小型decoder和人工token ids，没有视觉编码器或真实视频。预设PLAN和DIRECT骨架，仅各片段内部由学生当前分布实时采样；没有训练过的空间教师、自由工具调用或学习到的路由器。  多模态基础模型 空间推理与分段多教师蒸馏 多模态 世界建模：状态、生成与动作条件 第一视角视频空间推理为什么需要同时改进提问规划和感知回答？ 复杂问题往往要先决定看哪里、问什么，再可靠读取局部证据，规划与感知任何一侧出错都会传给后续组合。EgoP²C 研究让这些角色能共同改进，同时保持各自信息范围。角色分离用于控制训练和交互，不代表感知结果天然可信，最终空间结论仍需验证。 教学例：问抽屉相对门的位置，规划者先选视角和子问题，感知者读具体位置；若读错左右，组合推理再流畅也会出错。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-ego-p2c-b2c2eae5" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-47077d41b441deb0">第一视角视频空间推理为什么需要同时改进提问规划和感知回答？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aego-p2c">EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Arizona State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>复杂问题往往要先决定看哪里、问什么，再可靠读取局部证据，规划与感知任何一侧出错都会传给后续组合。EgoP²C 研究让这些角色能共同改进，同时保持各自信息范围。角色分离用于控制训练和交互，不代表感知结果天然可信，最终空间结论仍需验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：问抽屉相对门的位置，规划者先选视角和子问题，感知者读具体位置；若读错左右，组合推理再流畅也会出错。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与信息边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22681">原论文</a> · <a href="../../../../foundation-models/2610.22681-ego-p2c/">实现解读</a> · <a href="#qa-47077d41b441deb0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ego-p2c" data-paper-title="EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video 基础模型 Arizona State University 2026-10-15 第一视角视频空间推理既要提问、采集证据，也要保证感知回答可靠。固定外部视觉工具无法随推理策略一起改进；把规划与感知压到同一组参数中又可能引入梯度冲突。EgoP²C先在冻结VLM上分别训练规划/组合（PC）与感知（V）的LoRA教师，再复制选定FFN形成PC、V、通用直接回答（G）专家。学生自己生成交互片段，由相应冻结教师实时评价同一批学生tokens，而非模仿教师另行生成的答案。公共视频前缀始终走冻结基础路径；角色私有文字、选项和历史不混入公共KV。 完整实验成本过高，不复现（审查 DONE）。本地保留真实角色FFN复制、q/k/v/o低秩残差、因果attention、公共前缀冻结、严格参数冻结、完整词表打分及上述损失。使用12维单层小型decoder和人工token ids，没有视觉编码器或真实视频。预设PLAN和DIRECT骨架，仅各片段内部由学生当前分布实时采样；没有训练过的空间教师、自由工具调用或学习到的路由器。  多模态基础模型 空间推理与分段多教师蒸馏 多模态 世界建模：状态、生成与动作条件 为什么分段蒸馏必须让各教师评价同一批学生 tokens？ 学生实际生成的交互决定了它访问的前缀，各角色教师在这些前缀上评分，才能分别指出规划、感知或直接回答的偏差。若改成模仿教师另写的一条答案，就丢失在策略监督；共享视频 KV 还不能混入角色私有历史，以免破坏信息隔离。 例如学生先提出一个视角问题，再给出空间判断；规划教师评前段、感知教师评相关片段，二者都评学生真正走过的文本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ego-p2c" data-paper-title="EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video 基础模型 Arizona State University 2026-10-15 第一视角视频空间推理既要提问、采集证据，也要保证感知回答可靠。固定外部视觉工具无法随推理策略一起改进；把规划与感知压到同一组参数中又可能引入梯度冲突。EgoP²C先在冻结VLM上分别训练规划/组合（PC）与感知（V）的LoRA教师，再复制选定FFN形成PC、V、通用直接回答（G）专家。学生自己生成交互片段，由相应冻结教师实时评价同一批学生tokens，而非模仿教师另行生成的答案。公共视频前缀始终走冻结基础路径；角色私有文字、选项和历史不混入公共KV。 完整实验成本过高，不复现（审查 DONE）。本地保留真实角色FFN复制、q/k/v/o低秩残差、因果attention、公共前缀冻结、严格参数冻结、完整词表打分及上述损失。使用12维单层小型decoder和人工token ids，没有视觉编码器或真实视频。预设PLAN和DIRECT骨架，仅各片段内部由学生当前分布实时采样；没有训练过的空间教师、自由工具调用或学习到的路由器。  多模态基础模型 空间推理与分段多教师蒸馏 多模态 世界建模：状态、生成与动作条件 PC、V 与通用 G 专家的参数，是否都采用相同的训练边界？ 角色专家从基础 FFN 复制初始化，但 G 的 FFN 始终冻结，G 的 attention residual 到 MOPD 阶段才训练；PC、V 则承担规划与感知的可训练角色路径。不同参数边界维护通用直接回答能力与专门化分工，不能把它简化成三份全参数模型一起更新。 教学例：给 G 保留原 FFN 不是完全禁止它的一切适配；attention residual 后续可训练，而底层复制初始化也不等于所有角色共享更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d2509c24f0c7580c">PC、V 与通用 G 专家的参数，是否都采用相同的训练边界？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aego-p2c">EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Arizona State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>角色专家从基础 FFN 复制初始化，但 G 的 FFN 始终冻结，G 的 attention residual 到 MOPD 阶段才训练；PC、V 则承担规划与感知的可训练角色路径。不同参数边界维护通用直接回答能力与专门化分工，不能把它简化成三份全参数模型一起更新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：给 G 保留原 FFN 不是完全禁止它的一切适配；attention residual 后续可训练，而底层复制初始化也不等于所有角色共享更新。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与信息边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22681">原论文</a> · <a href="../../../../foundation-models/2610.22681-ego-p2c/">实现解读</a> · <a href="#qa-d2509c24f0c7580c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ego-p2c" data-paper-title="EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video 基础模型 Arizona State University 2026-10-15 第一视角视频空间推理既要提问、采集证据，也要保证感知回答可靠。固定外部视觉工具无法随推理策略一起改进；把规划与感知压到同一组参数中又可能引入梯度冲突。EgoP²C先在冻结VLM上分别训练规划/组合（PC）与感知（V）的LoRA教师，再复制选定FFN形成PC、V、通用直接回答（G）专家。学生自己生成交互片段，由相应冻结教师实时评价同一批学生tokens，而非模仿教师另行生成的答案。公共视频前缀始终走冻结基础路径；角色私有文字、选项和历史不混入公共KV。 完整实验成本过高，不复现（审查 DONE）。本地保留真实角色FFN复制、q/k/v/o低秩残差、因果attention、公共前缀冻结、严格参数冻结、完整词表打分及上述损失。使用12维单层小型decoder和人工token ids，没有视觉编码器或真实视频。预设PLAN和DIRECT骨架，仅各片段内部由学生当前分布实时采样；没有训练过的空间教师、自由工具调用或学习到的路由器。  多模态基础模型 空间推理与分段多教师蒸馏 多模态 世界建模：状态、生成与动作条件 角色长度归一化的分母为何必须覆盖整条轨迹？ 同角色可出现多个片段，分母是该轨迹中该角色所有监督 token 总数，而非每段各平均一次。否则拆成更多短片段就会获得更大角色权重。教师与旧学生 logp 停止梯度，私有 decoder KV 不跨角色复用，本地随机教师诊断不等于空间推理能力。 例如 PC 总共十个 token，拆成两段各五个后总权重应不变；若每段独立平均，拆段会把 PC 贡献翻倍。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gen4p" data-paper-title="Gen4P: Video Generators are 4D Perceivers" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Gen4P: Video Generators are 4D Perceivers 基础模型 Nanyang Technological University 2026-10-15 视频生成预训练包含运动与几何先验。Gen4P不通过多次去噪恢复几何，而是在干净视频潜变量上运行一次DiT编码，用按需cross-attention查询输出3D轨迹、点云、深度和相机参数。连续时间查询适配不同视频长度，冻结depth-LoRA提供额外几何先验，独立4D-LoRA学习新任务。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地训练、能力指标或Evolve算子。无本地adapter、GPU验收、训练指标或可执行Evolve映射。上游repo存在不等同代码已开源；未来若作者真正发布实现，只有出现新的独立证据或用户明确需求时再审查。本轮只完成方法、代码发布状态与资源配置核验；没有下载视频、checkpoint、运行训练或制造小模型“4D能力”分数。  多模态基础模型 视频生成与四维感知 多模态 世界建模：状态、生成与动作条件 Gen4P 为什么尝试把视频生成模型的知识用于三维和四维感知？ 视频生成预训练需要理解外观、运动和部分几何结构，这些先验可能帮助估计深度、轨迹和相机，而不必只服务像素生成。Gen4P 从干净视频提取场景表示，再按查询输出所需属性。利用生成器不等于必须生成整段视频，感知预测仍需对应几何真值或任务验证。 教学例：输入一段移动镜头视频，用户需要的是某点的三维轨迹而非一段新视频；模型应把已有运动先验转为可查询感知结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-gen4p-e9a640f8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e01e783591ec19da">Gen4P 为什么尝试把视频生成模型的知识用于三维和四维感知？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agen4p">Gen4P: Video Generators are 4D Perceivers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>视频生成预训练需要理解外观、运动和部分几何结构，这些先验可能帮助估计深度、轨迹和相机，而不必只服务像素生成。Gen4P 从干净视频提取场景表示，再按查询输出所需属性。利用生成器不等于必须生成整段视频，感知预测仍需对应几何真值或任务验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：输入一段移动镜头视频，用户需要的是某点的三维轨迹而非一段新视频；模型应把已有运动先验转为可查询感知结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22371">原论文</a> · <a href="../../../../foundation-models/2610.22371-gen4p/">实现解读</a> · <a href="#qa-e01e783591ec19da">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gen4p" data-paper-title="Gen4P: Video Generators are 4D Perceivers" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Gen4P: Video Generators are 4D Perceivers 基础模型 Nanyang Technological University 2026-10-15 视频生成预训练包含运动与几何先验。Gen4P不通过多次去噪恢复几何，而是在干净视频潜变量上运行一次DiT编码，用按需cross-attention查询输出3D轨迹、点云、深度和相机参数。连续时间查询适配不同视频长度，冻结depth-LoRA提供额外几何先验，独立4D-LoRA学习新任务。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地训练、能力指标或Evolve算子。无本地adapter、GPU验收、训练指标或可执行Evolve映射。上游repo存在不等同代码已开源；未来若作者真正发布实现，只有出现新的独立证据或用户明确需求时再审查。本轮只完成方法、代码发布状态与资源配置核验；没有下载视频、checkpoint、运行训练或制造小模型“4D能力”分数。  多模态基础模型 视频生成与四维感知 多模态 世界建模：状态、生成与动作条件 使用视频生成器做四维感知时，为什么不必执行完整多步去噪？ Gen4P 利用预训练 DiT 内部的运动与几何表示，而不是要求它重新生成视频。干净视频潜变量经过一次规定条件的编码，查询再读出轨迹或深度；冻结几何适配与新任务 LoRA 承担不同职责。少一次生成过程并不意味着感知任务无需监督或解码器。 例如输入现有视频后查询某点三秒后的三维位置，读取一次场景表示即可训练预测头，不需要先生成另一段完整视频。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gen4p" data-paper-title="Gen4P: Video Generators are 4D Perceivers" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Gen4P: Video Generators are 4D Perceivers 基础模型 Nanyang Technological University 2026-10-15 视频生成预训练包含运动与几何先验。Gen4P不通过多次去噪恢复几何，而是在干净视频潜变量上运行一次DiT编码，用按需cross-attention查询输出3D轨迹、点云、深度和相机参数。连续时间查询适配不同视频长度，冻结depth-LoRA提供额外几何先验，独立4D-LoRA学习新任务。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地训练、能力指标或Evolve算子。无本地adapter、GPU验收、训练指标或可执行Evolve映射。上游repo存在不等同代码已开源；未来若作者真正发布实现，只有出现新的独立证据或用户明确需求时再审查。本轮只完成方法、代码发布状态与资源配置核验；没有下载视频、checkpoint、运行训练或制造小模型“4D能力”分数。  多模态基础模型 视频生成与四维感知 多模态 世界建模：状态、生成与动作条件 冻结 depth-LoRA 与训练 4D-LoRA 的分工，为什么不同于全参数微调？ 基础 DiT 和深度 LoRA 保持冻结，新增 4D-LoRA、查询与输出解码器承担感知任务适配，分别保留生成和深度先验。全参数微调会允许更广泛改变这些表示；双 LoRA 也并非每项指标必然改善，原文保留了深度结果下降的例子。 例如新任务需要追踪点的时间轨迹，可更新 4D 适配而不改已有深度更新，但仍要检查是否改善实际深度与追踪。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gen4p" data-paper-title="Gen4P: Video Generators are 4D Perceivers" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Gen4P: Video Generators are 4D Perceivers 基础模型 Nanyang Technological University 2026-10-15 视频生成预训练包含运动与几何先验。Gen4P不通过多次去噪恢复几何，而是在干净视频潜变量上运行一次DiT编码，用按需cross-attention查询输出3D轨迹、点云、深度和相机参数。连续时间查询适配不同视频长度，冻结depth-LoRA提供额外几何先验，独立4D-LoRA学习新任务。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地训练、能力指标或Evolve算子。无本地adapter、GPU验收、训练指标或可执行Evolve映射。上游repo存在不等同代码已开源；未来若作者真正发布实现，只有出现新的独立证据或用户明确需求时再审查。本轮只完成方法、代码发布状态与资源配置核验；没有下载视频、checkpoint、运行训练或制造小模型“4D能力”分数。  多模态基础模型 视频生成与四维感知 多模态 世界建模：状态、生成与动作条件 连续时间查询与 DiT 输入条件有哪些容易混淆的细节？ 时间查询用起终点 embedding 按 t/(T-1) 连续插值，DiT 则读取干净 z0，使用最终 scheduler 时间条件和空文本条件。不能把查询时间当作扩散加噪时刻，也不能改成迭代去噪。当前只有资料收录，无本地 adapter 或 4D 能力验证。 例如查询视频中间时刻使用两个时间端点的插值，并不是给该帧加一半噪声再让生成器恢复。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:egojepa" data-paper-title="EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos 基础模型 Mohamed bin Zayed University of Artificial Intelligence 2026-10-14 人类第一视角视频中的手运动不需要经规则映射为每种机器人的动作。EgoJEPA先用手部运动差分条件JEPA预测未来视觉表示，再联合建模视觉与潜动作，最后仅适配目标机器人的输入输出动作接口。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地能力指标、训练结果或可执行 Evolve 算子。无本地adapter、指标文件或GPU回执，也不登记可执行Evolve算子。原论文结果仅作为阅读资料。范围见本轮实现与审查合同。本轮只完成方法、资源需求、公开代码状态及原图收录，没有运行完整实验、下载checkpoint或制造模拟能力分数。  JEPA与世界模型 具身多模态 多模态 世界建模：状态、生成与动作条件 EgoJEPA 为什么尝试从大量人类第一视角视频学习可迁移的动作经验？ 机器人示范昂贵且不同本体接口各异，人类视频则含丰富的视觉变化与行动关系，却没有直接可用的机器人控制量。EgoJEPA 研究先学习视觉与动作的潜在结构，再适配目标机器人接口。视频中的相关变化不是任意机器人的可执行命令，真实控制仍需适配与环境验证。 教学例：人类打开抽屉的视频可提供动作与场景变化经验；换成机械臂后，关节控制仍须通过目标机器人接口学习。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-egojepa-867ae28c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-eace4b99f19a0163">EgoJEPA 为什么尝试从大量人类第一视角视频学习可迁移的动作经验？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aegojepa">EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Mohamed bin Zayed University of Artificial Intelligence</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>机器人示范昂贵且不同本体接口各异，人类视频则含丰富的视觉变化与行动关系，却没有直接可用的机器人控制量。EgoJEPA 研究先学习视觉与动作的潜在结构，再适配目标机器人接口。视频中的相关变化不是任意机器人的可执行命令，真实控制仍需适配与环境验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：人类打开抽屉的视频可提供动作与场景变化经验；换成机械臂后，关节控制仍须通过目标机器人接口学习。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20904">原论文</a> · <a href="../../../../foundation-models/2610.20904-egojepa/">实现解读</a> · <a href="#qa-eace4b99f19a0163">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:egojepa" data-paper-title="EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos 基础模型 Mohamed bin Zayed University of Artificial Intelligence 2026-10-14 人类第一视角视频中的手运动不需要经规则映射为每种机器人的动作。EgoJEPA先用手部运动差分条件JEPA预测未来视觉表示，再联合建模视觉与潜动作，最后仅适配目标机器人的输入输出动作接口。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地能力指标、训练结果或可执行 Evolve 算子。无本地adapter、指标文件或GPU回执，也不登记可执行Evolve算子。原论文结果仅作为阅读资料。范围见本轮实现与审查合同。本轮只完成方法、资源需求、公开代码状态及原图收录，没有运行完整实验、下载checkpoint或制造模拟能力分数。  JEPA与世界模型 具身多模态 多模态 世界建模：状态、生成与动作条件 EgoJEPA 为什么先学习潜动作，而不把人的手部轨迹直接规则映射成机器人关节？ 人的手与机器人的执行器形态不同，硬映射容易把特定身体结构当成通用动作。方法先用运动差分条件学习与视觉变化相关的潜动作，再联合视觉建模，最后适配目标机器人的动作接口；可迁移的是作用关系，而不是假设两种关节坐标天然等价。 例如人的捏取动作和夹爪闭合角度不同，但都能导致杯子被拿起；先学这一状态变化，再适配夹爪的输入输出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:egojepa" data-paper-title="EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos 基础模型 Mohamed bin Zayed University of Artificial Intelligence 2026-10-14 人类第一视角视频中的手运动不需要经规则映射为每种机器人的动作。EgoJEPA先用手部运动差分条件JEPA预测未来视觉表示，再联合建模视觉与潜动作，最后仅适配目标机器人的输入输出动作接口。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地能力指标、训练结果或可执行 Evolve 算子。无本地adapter、指标文件或GPU回执，也不登记可执行Evolve算子。原论文结果仅作为阅读资料。范围见本轮实现与审查合同。本轮只完成方法、资源需求、公开代码状态及原图收录，没有运行完整实验、下载checkpoint或制造模拟能力分数。  JEPA与世界模型 具身多模态 多模态 世界建模：状态、生成与动作条件 动作条件 JEPA 与后续视觉—潜动作联合 Flow Matching，分别学习什么关系？ 前一阶段利用手部运动差分预测未来视觉表示，让潜动作与可观察变化建立联系；后续联合建模视觉和潜动作，再通过目标机器人输入输出接口适配控制。它们不是同一个损失换名字，预测未来的表示学习与联合生成承担不同职责，也不能据前者成功推出真实机器人控制已完成。 教学例：先学“某类手部变化对应怎样的视觉后果”，再学习视觉与潜动作的联合结构；目标机械臂仍需要自己的控制接口。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-9a0417ac0042303b">动作条件 JEPA 与后续视觉—潜动作联合 Flow Matching，分别学习什么关系？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aegojepa">EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Mohamed bin Zayed University of Artificial Intelligence</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前一阶段利用手部运动差分预测未来视觉表示，让潜动作与可观察变化建立联系；后续联合建模视觉和潜动作，再通过目标机器人输入输出接口适配控制。它们不是同一个损失换名字，预测未来的表示学习与联合生成承担不同职责，也不能据前者成功推出真实机器人控制已完成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：先学“某类手部变化对应怎样的视觉后果”，再学习视觉与潜动作的联合结构；目标机械臂仍需要自己的控制接口。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20904">原论文</a> · <a href="../../../../foundation-models/2610.20904-egojepa/">实现解读</a> · <a href="#qa-9a0417ac0042303b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:egojepa" data-paper-title="EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos 基础模型 Mohamed bin Zayed University of Artificial Intelligence 2026-10-14 人类第一视角视频中的手运动不需要经规则映射为每种机器人的动作。EgoJEPA先用手部运动差分条件JEPA预测未来视觉表示，再联合建模视觉与潜动作，最后仅适配目标机器人的输入输出动作接口。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地能力指标、训练结果或可执行 Evolve 算子。无本地adapter、指标文件或GPU回执，也不登记可执行Evolve算子。原论文结果仅作为阅读资料。范围见本轮实现与审查合同。本轮只完成方法、资源需求、公开代码状态及原图收录，没有运行完整实验、下载checkpoint或制造模拟能力分数。  JEPA与世界模型 具身多模态 多模态 世界建模：状态、生成与动作条件 未来视觉目标在 JEPA 训练和实际控制时的可见性有什么区别？ 训练时真实未来帧经目标编码器提供停止梯度的表征，用于监督历史和手部差分条件预测；实际控制不能读取尚未发生的未来。当前本地只有方法和成本收录，无 adapter、指标或 GPU 回执，不能把公式说明当作真实机器人链路已实现。 例如给定前几帧预测拿起后的物体位置，目标帧只用于训练核对；部署时若直接输入该帧，就已提前泄露未来。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:esc" data-paper-title="ESC: Escaping 2D Diffusion Ambiguity with Geometric Constraints for Consistent Novel View Synthesis" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="ESC: Escaping 2D Diffusion Ambiguity with Geometric Constraints for Consistent Novel View Synthesis 基础模型 FAIR at Meta / Mila - Québec AI Institute / Université de Montréal 2026-10-14 单幅图像经扩散模型生成新视角时，2D视觉质量或相机姿态对齐不保证3D几何一致。ESC 联合生成 RGB 与逆深度，用 Plücker ray maps 条件化 Qwen MM-DiT，并以双向深度重投影约束 PCC 识别“物体消失”与“凭空出现”。推理时按 PCC 在多次随机生成中选优。 完整实验成本过高，不复现（审查 DONE）。未实现、未训练、未 GPU 验证。历史补发现，不是10月18日至21日的新首发。完整实验成本过高，不复现（审查 DONE）。本页没有可运行 adapter、没有本地效果指标，不进入自动训练或 Evolve 晋级队列。未实现、未训练、未 GPU 验证。本轮只有资料与算法边界收录，不提供伪 adapter、占位效果 JSON 或假 CUDA 回执。已核验固定 v1 正文、方法、架构图及 Appendix E.1 成本。  多模态基础模型 几何一致新视角生成 多模态 世界建模：状态、生成与动作条件 单图生成新视角时，ESC 为什么关心物体是否在三维场景中一致存在？ 图像生成器可能画出清晰、姿态看似正确的画面，却让物体凭空出现或在转视角后消失。ESC 研究把颜色与深度联系起来，用几何一致性检查这些错误。新视角与源图本来就不应逐像素相同，目标是可解释的空间变化，而非单纯追求更相似或更好看的图片。 教学例：镜头绕桌移动，杯子位置应随投影变化；若杯子在无遮挡处消失，画面再精致也不符合相同场景的几何关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-esc-e793a8c8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9fcdef57f9d4db58">单图生成新视角时，ESC 为什么关心物体是否在三维场景中一致存在？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aesc">ESC: Escaping 2D Diffusion Ambiguity with Geometric Constraints for Consistent Novel View Synthesis</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta / Mila - Québec AI Institute / Université de Montréal</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>图像生成器可能画出清晰、姿态看似正确的画面，却让物体凭空出现或在转视角后消失。ESC 研究把颜色与深度联系起来，用几何一致性检查这些错误。新视角与源图本来就不应逐像素相同，目标是可解释的空间变化，而非单纯追求更相似或更好看的图片。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：镜头绕桌移动，杯子位置应随投影变化；若杯子在无遮挡处消失，画面再精致也不符合相同场景的几何关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23732v1">原论文</a> · <a href="../../../../foundation-models/2610.23732-esc/">实现解读</a> · <a href="#qa-9fcdef57f9d4db58">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:esc" data-paper-title="ESC: Escaping 2D Diffusion Ambiguity with Geometric Constraints for Consistent Novel View Synthesis" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="ESC: Escaping 2D Diffusion Ambiguity with Geometric Constraints for Consistent Novel View Synthesis 基础模型 FAIR at Meta / Mila - Québec AI Institute / Université de Montréal 2026-10-14 单幅图像经扩散模型生成新视角时，2D视觉质量或相机姿态对齐不保证3D几何一致。ESC 联合生成 RGB 与逆深度，用 Plücker ray maps 条件化 Qwen MM-DiT，并以双向深度重投影约束 PCC 识别“物体消失”与“凭空出现”。推理时按 PCC 在多次随机生成中选优。 完整实验成本过高，不复现（审查 DONE）。未实现、未训练、未 GPU 验证。历史补发现，不是10月18日至21日的新首发。完整实验成本过高，不复现（审查 DONE）。本页没有可运行 adapter、没有本地效果指标，不进入自动训练或 Evolve 晋级队列。未实现、未训练、未 GPU 验证。本轮只有资料与算法边界收录，不提供伪 adapter、占位效果 JSON 或假 CUDA 回执。已核验固定 v1 正文、方法、架构图及 Appendix E.1 成本。  多模态基础模型 几何一致新视角生成 多模态 世界建模：状态、生成与动作条件 为什么新视角图像看起来清晰、相机姿态也正确，仍可能不满足 PCC？ 外观逼真不约束两视角是否描述同一个三维场景。PCC 用深度重投影及可见性检查双向几何差，区分物体消失与凭空出现；遮挡和无效像素必须处理，不能用普通 RGB 差代替。Best-of-N 选优比较的是几何一致性，而非直接选择最漂亮的图片。 例如转动镜头后桌上的杯子消失，新图依旧自然清晰；双向深度重投影却会暴露这处不一致。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:esc" data-paper-title="ESC: Escaping 2D Diffusion Ambiguity with Geometric Constraints for Consistent Novel View Synthesis" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="ESC: Escaping 2D Diffusion Ambiguity with Geometric Constraints for Consistent Novel View Synthesis 基础模型 FAIR at Meta / Mila - Québec AI Institute / Université de Montréal 2026-10-14 单幅图像经扩散模型生成新视角时，2D视觉质量或相机姿态对齐不保证3D几何一致。ESC 联合生成 RGB 与逆深度，用 Plücker ray maps 条件化 Qwen MM-DiT，并以双向深度重投影约束 PCC 识别“物体消失”与“凭空出现”。推理时按 PCC 在多次随机生成中选优。 完整实验成本过高，不复现（审查 DONE）。未实现、未训练、未 GPU 验证。历史补发现，不是10月18日至21日的新首发。完整实验成本过高，不复现（审查 DONE）。本页没有可运行 adapter、没有本地效果指标，不进入自动训练或 Evolve 晋级队列。未实现、未训练、未 GPU 验证。本轮只有资料与算法边界收录，不提供伪 adapter、占位效果 JSON 或假 CUDA 回执。已核验固定 v1 正文、方法、架构图及 Appendix E.1 成本。  多模态基础模型 几何一致新视角生成 多模态 世界建模：状态、生成与动作条件 PCC Best-of-N 与按 RGB 相似度选最像源图的候选有什么不同？ 新视角本来就应改变像素外观，RGB 相似不能直接代表几何正确。PCC 使用源与目标深度的双向投影、遮挡和有效覆盖判断缺失与幻觉几何，并选择分数最小的候选；它衡量特定几何约束，不保证所有图像质量指标同时最优。 例如相机转到桌子另一侧，正确图像与源图像素差很大；重复源图可能 RGB 更近，却不符合目标视角。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:esc" data-paper-title="ESC: Escaping 2D Diffusion Ambiguity with Geometric Constraints for Consistent Novel View Synthesis" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="ESC: Escaping 2D Diffusion Ambiguity with Geometric Constraints for Consistent Novel View Synthesis 基础模型 FAIR at Meta / Mila - Québec AI Institute / Université de Montréal 2026-10-14 单幅图像经扩散模型生成新视角时，2D视觉质量或相机姿态对齐不保证3D几何一致。ESC 联合生成 RGB 与逆深度，用 Plücker ray maps 条件化 Qwen MM-DiT，并以双向深度重投影约束 PCC 识别“物体消失”与“凭空出现”。推理时按 PCC 在多次随机生成中选优。 完整实验成本过高，不复现（审查 DONE）。未实现、未训练、未 GPU 验证。历史补发现，不是10月18日至21日的新首发。完整实验成本过高，不复现（审查 DONE）。本页没有可运行 adapter、没有本地效果指标，不进入自动训练或 Evolve 晋级队列。未实现、未训练、未 GPU 验证。本轮只有资料与算法边界收录，不提供伪 adapter、占位效果 JSON 或假 CUDA 回执。已核验固定 v1 正文、方法、架构图及 Appendix E.1 成本。  多模态基础模型 几何一致新视角生成 多模态 世界建模：状态、生成与动作条件 重投影计算为什么必须包含 z-buffer 和有效像素 mask？ 多个源点投到同一目标像素时要处理遮挡，负深度、越界或无源深度点也不能当有效误差。PCC 还含阈值、对数压缩、裁剪与覆盖归一化，不是简单绝对深度差。当前未实现或训练 ESC，本地没有可用能力指标。 例如墙后物体在目标视角被遮住，不应因缺少可见对应就算作消失；忽略遮挡会把正确几何当成失败。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jepa-prediction-planning" data-paper-title="One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models 基础模型 论文未列机构 2026-10-14 JEPA 在自己的潜空间预测下一观察，较小的一步 loss 不一定表示更好的长程行动。论文固定一个只在真实观察编码上拟合的物理状态解码器，分别解码真实下一表征与预测下一表征，把编码器本身的可读性和预测器新增的误差拆开。规划仍用相同 checkpoint、相同任务和配对种子单独执行，不能由预测指标推导成功率。 原文三个环境的世界模型重训、每环境多训练/解码/规划种子和完整 MPC：成本过高，不复现（审查 DONE）。CPU 接口实测保存真实解码器拟合与受控输入的诊断指标，不代表世界模型能力。本地对照口径：共享状态规范与归一化、同一冻结解码器；输入必须来自相同 transition。世界模型预测与外部规划分别评价，不自动接入 Evolve 选择。  世界模型评测 冻结物理状态解码器 预测与规划配对比较 多模态 世界建模：状态、生成与动作条件 JEPA 的下一步 latent loss 很小，为什么还不足以判断它理解了物理运动？ latent 是编码器自己的坐标，距离小未必对应位置、角度或速度误差小，也未必帮助长程规划。该工作把物理状态解码与真实规划分开检查，并用共享训练尺度组织误差。研究目标是厘清预测指标代表什么，不能从某个内部 loss 的下降直接宣布物理理解或控制成功。 教学例：两个预测向量很接近，解码后却可能对应不同物体角度；还需检查物理量误差，以及同任务中实际规划是否成功。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-jepa-prediction-planning-96c625cf" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c84d7475eab03391">JEPA 的下一步 latent loss 很小，为什么还不足以判断它理解了物理运动？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ajepa-prediction-planning">One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>latent 是编码器自己的坐标，距离小未必对应位置、角度或速度误差小，也未必帮助长程规划。该工作把物理状态解码与真实规划分开检查，并用共享训练尺度组织误差。研究目标是厘清预测指标代表什么，不能从某个内部 loss 的下降直接宣布物理理解或控制成功。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：两个预测向量很接近，解码后却可能对应不同物体角度；还需检查物理量误差，以及同任务中实际规划是否成功。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19375v1">原论文</a> · <a href="../../../../foundation-models/2610.19375-jepa-prediction-planning/">实现解读</a> · <a href="#qa-c84d7475eab03391">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jepa-prediction-planning" data-paper-title="One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models 基础模型 论文未列机构 2026-10-14 JEPA 在自己的潜空间预测下一观察，较小的一步 loss 不一定表示更好的长程行动。论文固定一个只在真实观察编码上拟合的物理状态解码器，分别解码真实下一表征与预测下一表征，把编码器本身的可读性和预测器新增的误差拆开。规划仍用相同 checkpoint、相同任务和配对种子单独执行，不能由预测指标推导成功率。 原文三个环境的世界模型重训、每环境多训练/解码/规划种子和完整 MPC：成本过高，不复现（审查 DONE）。CPU 接口实测保存真实解码器拟合与受控输入的诊断指标，不代表世界模型能力。本地对照口径：共享状态规范与归一化、同一冻结解码器；输入必须来自相同 transition。世界模型预测与外部规划分别评价，不自动接入 Evolve 选择。  世界模型评测 冻结物理状态解码器 预测与规划配对比较 多模态 世界建模：状态、生成与动作条件 为什么要从预测状态误差中减去真实表征经同一解码器得到的误差？ 解码误差同时混合编码器可读性、解码器不足和预测器偏差。固定同一解码器，先测真实下一表征，再测预测下一表征，差值更接近预测环节新增的影响；它可能为负，不能截零。即便差值小，长程规划成功率仍需独立配对验证。 例如解码器本来就把位置估错两格，预测表征又错三格；不能把全部三格都归因预测器，应先扣除真实表征的基础误差。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jepa-prediction-planning" data-paper-title="One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models 基础模型 论文未列机构 2026-10-14 JEPA 在自己的潜空间预测下一观察，较小的一步 loss 不一定表示更好的长程行动。论文固定一个只在真实观察编码上拟合的物理状态解码器，分别解码真实下一表征与预测下一表征，把编码器本身的可读性和预测器新增的误差拆开。规划仍用相同 checkpoint、相同任务和配对种子单独执行，不能由预测指标推导成功率。 原文三个环境的世界模型重训、每环境多训练/解码/规划种子和完整 MPC：成本过高，不复现（审查 DONE）。CPU 接口实测保存真实解码器拟合与受控输入的诊断指标，不代表世界模型能力。本地对照口径：共享状态规范与归一化、同一冻结解码器；输入必须来自相同 transition。世界模型预测与外部规划分别评价，不自动接入 Evolve 选择。  世界模型评测 冻结物理状态解码器 预测与规划配对比较 多模态 世界建模：状态、生成与动作条件 一步物理预测误差下降与规划成功率提升为什么需要分开测？ 规划反复调用模型，误差可能累积、偏向关键动作或改变搜索路径；一步平均误差无法表达这些闭环影响。应在同一 checkpoint、任务和配对种子上实际运行规划，再比较成功率，不能由一个预测指标自动推导行动能力。 例如模型在常见静止状态更准，却在碰撞附近稍错，整体一步误差下降仍可能让规划频繁撞墙。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jepa-prediction-planning" data-paper-title="One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models 基础模型 论文未列机构 2026-10-14 JEPA 在自己的潜空间预测下一观察，较小的一步 loss 不一定表示更好的长程行动。论文固定一个只在真实观察编码上拟合的物理状态解码器，分别解码真实下一表征与预测下一表征，把编码器本身的可读性和预测器新增的误差拆开。规划仍用相同 checkpoint、相同任务和配对种子单独执行，不能由预测指标推导成功率。 原文三个环境的世界模型重训、每环境多训练/解码/规划种子和完整 MPC：成本过高，不复现（审查 DONE）。CPU 接口实测保存真实解码器拟合与受控输入的诊断指标，不代表世界模型能力。本地对照口径：共享状态规范与归一化、同一冻结解码器；输入必须来自相同 transition。世界模型预测与外部规划分别评价，不自动接入 Evolve 选择。  世界模型评测 冻结物理状态解码器 预测与规划配对比较 多模态 世界建模：状态、生成与动作条件 E_excess 为负时应截成零吗？ 不应。它定义为预测表征解码误差减真实表征解码误差，预测表示偶然更适合冻结解码器时差值可为负。两种表示完全相同则差值必须为零；状态归一化方差只由共享训练数据确定，解码器不能用预测 test 表征重新拟合。 例如真实表征误差为三、预测为二，差值应为负一；截零会改变定义并掩盖解码器外推现象。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:oob-regularization" data-paper-title="Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning 基础模型 European Molecular Biology Laboratory (EMBL) 2026-10-14 联合嵌入自监督学习一方面拉近同一图像的不同增强视图，另一方面用抗坍塌正则保持表示多样性。小 batch 对整个表示分布的估计可能很差；单纯增大 GPU batch 又受显存限制。OOB 把“统计范围”与“本次优化 batch”解耦：定期编码整个训练集，按全数据分布构建每个样本的固定目标，再存入 CPU。在线训练只读取当前样本对应的锚点，不在每一步重新估计全数据正则。Gaussian 变体沿随机单位方向投影，把每列样本排序后匹配标准正态分位数； 完整原研究为成本过高，不复现（审查 DONE）。先核验 MD5 c99cafc152244af753f735de768cd75f，再解析官方 pickle，拒绝任意未验证 pickle。本地实现两种真实锚点算法，并在有限的官方 CIFAR 图像上执行有对照的训练。它不是原论文多数据集、100 epochs 的完整研究；短预算的负结果照实保留，不进入 Evolve 自动晋级。完整原研究为成本过高，不复现（审查 DONE）。本地对照口径：基线为同投影 / 分位数口径的 in-batch Gaussian 及 SimCLR；  self-supervised-learning joint-embedding small-batch representation-learning 多模态 世界建模：状态、生成与动作条件 小 batch 自监督学习为什么可能让图像视图对齐，却仍学不到可区分的表示？ 把同一图像的增强视图拉近，只约束一致性，所有样本输出常量也可满足；抗坍塌还需判断整体表示是否足够分散。小 batch 对分布估计容易不足，OOB 研究在显存受限时取得更广统计支持。统计范围更大不自动保证下游能力，仍需匹配目标与独立评估。 教学例：一个 batch 的几张图片编码相近，无法判断是样本本就相似还是全模型坍塌；只检查两视图差小，容易漏掉后一种问题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-oob-regularization-98328dd1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-24c359d6bb05f722">小 batch 自监督学习为什么可能让图像视图对齐，却仍学不到可区分的表示？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aoob-regularization">Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · European Molecular Biology Laboratory (EMBL)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>把同一图像的增强视图拉近，只约束一致性，所有样本输出常量也可满足；抗坍塌还需判断整体表示是否足够分散。小 batch 对分布估计容易不足，OOB 研究在显存受限时取得更广统计支持。统计范围更大不自动保证下游能力，仍需匹配目标与独立评估。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：一个 batch 的几张图片编码相近，无法判断是样本本就相似还是全模型坍塌；只检查两视图差小，容易漏掉后一种问题。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20158">原论文</a> · <a href="../../../../reproductions/2610.20158-oob-regularization/">实现解读</a> · <a href="#qa-24c359d6bb05f722">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:oob-regularization" data-paper-title="Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning 基础模型 European Molecular Biology Laboratory (EMBL) 2026-10-14 联合嵌入自监督学习一方面拉近同一图像的不同增强视图，另一方面用抗坍塌正则保持表示多样性。小 batch 对整个表示分布的估计可能很差；单纯增大 GPU batch 又受显存限制。OOB 把“统计范围”与“本次优化 batch”解耦：定期编码整个训练集，按全数据分布构建每个样本的固定目标，再存入 CPU。在线训练只读取当前样本对应的锚点，不在每一步重新估计全数据正则。Gaussian 变体沿随机单位方向投影，把每列样本排序后匹配标准正态分位数； 完整原研究为成本过高，不复现（审查 DONE）。先核验 MD5 c99cafc152244af753f735de768cd75f，再解析官方 pickle，拒绝任意未验证 pickle。本地实现两种真实锚点算法，并在有限的官方 CIFAR 图像上执行有对照的训练。它不是原论文多数据集、100 epochs 的完整研究；短预算的负结果照实保留，不进入 Evolve 自动晋级。完整原研究为成本过高，不复现（审查 DONE）。本地对照口径：基线为同投影 / 分位数口径的 in-batch Gaussian 及 SimCLR；  self-supervised-learning joint-embedding small-batch representation-learning 多模态 世界建模：状态、生成与动作条件 OOB 为什么能让小 batch 使用接近全数据范围的抗坍塌监督？ 它把全数据统计与在线优化分开：定期编码训练集并建立每样本锚点，随后小 batch 读取对应固定目标。这样在线更新无需每步重新估计完整分布，但锚点会随模型变化而陈旧，需要刷新；这不同于直接在小 batch 上计算普通方差或协方差损失。 例如显存一次只能放八张图，仍可事先用全训练集生成排序分位数目标，再让这八张各自匹配自己的缓存锚点。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:oob-regularization" data-paper-title="Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning 基础模型 European Molecular Biology Laboratory (EMBL) 2026-10-14 联合嵌入自监督学习一方面拉近同一图像的不同增强视图，另一方面用抗坍塌正则保持表示多样性。小 batch 对整个表示分布的估计可能很差；单纯增大 GPU batch 又受显存限制。OOB 把“统计范围”与“本次优化 batch”解耦：定期编码整个训练集，按全数据分布构建每个样本的固定目标，再存入 CPU。在线训练只读取当前样本对应的锚点，不在每一步重新估计全数据正则。Gaussian 变体沿随机单位方向投影，把每列样本排序后匹配标准正态分位数； 完整原研究为成本过高，不复现（审查 DONE）。先核验 MD5 c99cafc152244af753f735de768cd75f，再解析官方 pickle，拒绝任意未验证 pickle。本地实现两种真实锚点算法，并在有限的官方 CIFAR 图像上执行有对照的训练。它不是原论文多数据集、100 epochs 的完整研究；短预算的负结果照实保留，不进入 Evolve 自动晋级。完整原研究为成本过高，不复现（审查 DONE）。本地对照口径：基线为同投影 / 分位数口径的 in-batch Gaussian 及 SimCLR；  self-supervised-learning joint-embedding small-batch representation-learning 多模态 世界建模：状态、生成与动作条件 Gaussian sorted-quantile 目标与只约束均值零、方差一有何不同？ 排序分位数为每个样本沿随机方向分配正态目标，约束投影分布及样本对应；均值方差只约束少数矩，许多不同分布都满足。该目标也不是原始 Epps–Pulley 统计量，配对基线应使用同一分位数口径，避免把损失差异误作范围收益。 例如一半样本在负一、一半在正一也可均值零方差一，却不是正态分位数排列；锚点目标会区分两种分布。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:oob-regularization" data-paper-title="Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning 基础模型 European Molecular Biology Laboratory (EMBL) 2026-10-14 联合嵌入自监督学习一方面拉近同一图像的不同增强视图，另一方面用抗坍塌正则保持表示多样性。小 batch 对整个表示分布的估计可能很差；单纯增大 GPU batch 又受显存限制。OOB 把“统计范围”与“本次优化 batch”解耦：定期编码整个训练集，按全数据分布构建每个样本的固定目标，再存入 CPU。在线训练只读取当前样本对应的锚点，不在每一步重新估计全数据正则。Gaussian 变体沿随机单位方向投影，把每列样本排序后匹配标准正态分位数； 完整原研究为成本过高，不复现（审查 DONE）。先核验 MD5 c99cafc152244af753f735de768cd75f，再解析官方 pickle，拒绝任意未验证 pickle。本地实现两种真实锚点算法，并在有限的官方 CIFAR 图像上执行有对照的训练。它不是原论文多数据集、100 epochs 的完整研究；短预算的负结果照实保留，不进入 Evolve 自动晋级。完整原研究为成本过高，不复现（审查 DONE）。本地对照口径：基线为同投影 / 分位数口径的 in-batch Gaussian 及 SimCLR；  self-supervised-learning joint-embedding small-batch representation-learning 多模态 世界建模：状态、生成与动作条件 锚点刷新的方向、目标和梯度应怎样隔离？ 刷新后投影方向和按样本分配的目标固定，detach 后存 CPU，在线损失对 B、视图数 V、方向数 M 归一化，不通过锚点反传到刷新阶段。球面变体另优化单位锚点，不能替换为 Gaussian 目标；稳定索引丢失会把样本配到错误锚点。 例如数据加载器打乱顺序后仍需按原样本 ID 查锚点，不能把缓存第一个目标直接给当前 batch 的第一张图。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:time-jepa" data-paper-title="Time-JEPA: Grounding Video World Models with Physical Time Series" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Time-JEPA: Grounding Video World Models with Physical Time Series 基础模型 Harbin Institute of Technology 2026-10-14 视频自监督目标不必保留精确的速度、关节角等物理状态。Time-JEPA 用同步传感器或标注作辅助目标，但它们不是编码器输入：训练时同一个 online encoder 分别处理 masked 上下文和 unmasked 视频，评测移除物理态 head，仍只输入视频。 完整实验成本过高，不复现（审查 DONE）。CPU与真实单张A100的42/43/44三seed诊断已完成。实现不只封装 loss：包含时间戳 nearest 对齐、逐变量 valid tubelet 池化、训练独占统计、真正的上下文 self-attention encoder、masked latent predictor、unmasked 两层物理 head、冻结 target 和显式 EMA 更新。nearest 的距离阈值由调用方传入、平局取较早测量，是本地明确的对齐策略，不冒充所有原始数据集的具体解码流程。  JEPA与世界模型 物理时序监督 多模态 世界建模：状态、生成与动作条件 理解视频里的动作类别，与保留精确速度和关节角，为什么是不同学习要求？ 语义分类可在很多姿态和速度变化下保持不变，控制或物理分析却可能需要这些连续量。Time-JEPA 研究让视频表示在自监督之外保留更细的时间物理信息。目标不是把传感器当作部署捷径，准确连续状态也不能仅由动作标签正确推断，需要针对数值量独立检查。 教学例：两段视频都叫“抬手”，但快慢和肘部角度不同；类别判断相同不表示表示里已经保留足够精度供机器人使用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-time-jepa-c002ea0d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4391c33e37078638">理解视频里的动作类别，与保留精确速度和关节角，为什么是不同学习要求？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atime-jepa">Time-JEPA: Grounding Video World Models with Physical Time Series</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语义分类可在很多姿态和速度变化下保持不变，控制或物理分析却可能需要这些连续量。Time-JEPA 研究让视频表示在自监督之外保留更细的时间物理信息。目标不是把传感器当作部署捷径，准确连续状态也不能仅由动作标签正确推断，需要针对数值量独立检查。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：两段视频都叫“抬手”，但快慢和肘部角度不同；类别判断相同不表示表示里已经保留足够精度供机器人使用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与隔离要求；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23982">原论文</a> · <a href="../../../../foundation-models/2610.23982-time-jepa/">实现解读</a> · <a href="#qa-4391c33e37078638">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:time-jepa" data-paper-title="Time-JEPA: Grounding Video World Models with Physical Time Series" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Time-JEPA: Grounding Video World Models with Physical Time Series 基础模型 Harbin Institute of Technology 2026-10-14 视频自监督目标不必保留精确的速度、关节角等物理状态。Time-JEPA 用同步传感器或标注作辅助目标，但它们不是编码器输入：训练时同一个 online encoder 分别处理 masked 上下文和 unmasked 视频，评测移除物理态 head，仍只输入视频。 完整实验成本过高，不复现（审查 DONE）。CPU与真实单张A100的42/43/44三seed诊断已完成。实现不只封装 loss：包含时间戳 nearest 对齐、逐变量 valid tubelet 池化、训练独占统计、真正的上下文 self-attention encoder、masked latent predictor、unmasked 两层物理 head、冻结 target 和显式 EMA 更新。nearest 的距离阈值由调用方传入、平局取较早测量，是本地明确的对齐策略，不冒充所有原始数据集的具体解码流程。  JEPA与世界模型 物理时序监督 多模态 世界建模：状态、生成与动作条件 物理时间序列只作训练标签，为何还能改善仅输入视频的编码器？ 辅助头把视频表示映射到速度或关节角，误差反向推动编码器保留这些物理信息，部署时可以删除该头。传感器不进入输入，因此评测仍是视频任务；无效帧要保持掩码，归一化统计也只能来自训练集，避免伪造零标签或测试泄漏。 例如训练时用同步速度监督视频表示，测试只给运动画面；若把速度数值直接拼进测试输入，就变成不同任务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:time-jepa" data-paper-title="Time-JEPA: Grounding Video World Models with Physical Time Series" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Time-JEPA: Grounding Video World Models with Physical Time Series 基础模型 Harbin Institute of Technology 2026-10-14 视频自监督目标不必保留精确的速度、关节角等物理状态。Time-JEPA 用同步传感器或标注作辅助目标，但它们不是编码器输入：训练时同一个 online encoder 分别处理 masked 上下文和 unmasked 视频，评测移除物理态 head，仍只输入视频。 完整实验成本过高，不复现（审查 DONE）。CPU与真实单张A100的42/43/44三seed诊断已完成。实现不只封装 loss：包含时间戳 nearest 对齐、逐变量 valid tubelet 池化、训练独占统计、真正的上下文 self-attention encoder、masked latent predictor、unmasked 两层物理 head、冻结 target 和显式 EMA 更新。nearest 的距离阈值由调用方传入、平局取较早测量，是本地明确的对齐策略，不冒充所有原始数据集的具体解码流程。  JEPA与世界模型 物理时序监督 多模态 世界建模：状态、生成与动作条件 辅助物理目标与只做 masked latent prediction 约束什么不同信息？ masked latent 预测鼓励表征可预测，却未必保留精确物理量；同步物理监督直接推动同一 encoder 保留这些变量。它可能改善物理可读性，但仍受变量覆盖与跨域分布影响，不能将一个域的探针结果推广为所有物理任务或控制能力。 例如视频模型能补全道路纹理，却忽略速度微差；训练专用速度目标会直接要求表示区分这类差异。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:time-jepa" data-paper-title="Time-JEPA: Grounding Video World Models with Physical Time Series" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Time-JEPA: Grounding Video World Models with Physical Time Series 基础模型 Harbin Institute of Technology 2026-10-14 视频自监督目标不必保留精确的速度、关节角等物理状态。Time-JEPA 用同步传感器或标注作辅助目标，但它们不是编码器输入：训练时同一个 online encoder 分别处理 masked 上下文和 unmasked 视频，评测移除物理态 head，仍只输入视频。 完整实验成本过高，不复现（审查 DONE）。CPU与真实单张A100的42/43/44三seed诊断已完成。实现不只封装 loss：包含时间戳 nearest 对齐、逐变量 valid tubelet 池化、训练独占统计、真正的上下文 self-attention encoder、masked latent predictor、unmasked 两层物理 head、冻结 target 和显式 EMA 更新。nearest 的距离阈值由调用方传入、平局取较早测量，是本地明确的对齐策略，不冒充所有原始数据集的具体解码流程。  JEPA与世界模型 物理时序监督 多模态 世界建模：状态、生成与动作条件 tubelet 内某变量完全缺测时，能否补成有效零标签？ 不能。每个变量独立按 valid 帧求均值，空 tubelet 仍无效；归一化均值方差仅在训练集拟合并冻结。物理损失只在有效项上求 SmoothL1，β 为 0.5；不同域还各有 head、统计和权重，不能混成同一无条件标签空间。 例如两帧都没测到关节角，填零会把未知误当真实零角度；正确做法是让该变量该 tubelet 不贡献监督。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ev-jepa" data-paper-title="EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference 基础模型 Meta Reality Labs Research 2026-10-09 固定容量的视频模型难以同时适配端侧预算和跨设备协作，独立训练不同宽度也不保证中间表示兼容。EV-JEPA共享嵌套宽度参数，每步联合训练窄、宽与窄转宽三条路径，以冻结视频教师约束共同表示空间，并增加可调token压缩。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文§4.1：128 GPU、300epochs，Kinetics-710/SSv2/HowTo100M视频，冻结V-JEPA2 ViT-G教师；每步同时训练窄、宽、混合三路径。压缩器另需100epochs×300iterations、全局batch4096。不是本地测速，原预算显著超出单卡A100/A30或Mac；不下载全视频或尝试多臂训练。  jepa video-representation elastic-inference 多模态 世界建模：状态、生成与动作条件 同一视频模型为什么需要适应手机、服务器或跨设备分段执行的不同预算？ 固定尺寸模型未必适合所有设备，分别训练多个模型又可能让中间表示不兼容，难以把计算从一台设备接到另一台。EV-JEPA 研究共享参数的弹性宽度和兼容表示。可选择宽度并不表示任意切分都正确或免费，实际传输、压缩和任务质量仍需验证。 教学例：手机先运行较窄前半段，再把中间表示交给服务器继续；若两种宽度从未学习衔接，形状能对上也未必能接着推理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-ev-jepa-12c252ce" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-fd62dd8be67749b5">同一视频模型为什么需要适应手机、服务器或跨设备分段执行的不同预算？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aev-jepa">EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Reality Labs Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定尺寸模型未必适合所有设备，分别训练多个模型又可能让中间表示不兼容，难以把计算从一台设备接到另一台。EV-JEPA 研究共享参数的弹性宽度和兼容表示。可选择宽度并不表示任意切分都正确或免费，实际传输、压缩和任务质量仍需验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：手机先运行较窄前半段，再把中间表示交给服务器继续；若两种宽度从未学习衔接，形状能对上也未必能接着推理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14324">原论文</a> · <a href="../../../../reproductions/2610.14324-ev-jepa/">实现解读</a> · <a href="#qa-fd62dd8be67749b5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ev-jepa" data-paper-title="EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference 基础模型 Meta Reality Labs Research 2026-10-09 固定容量的视频模型难以同时适配端侧预算和跨设备协作，独立训练不同宽度也不保证中间表示兼容。EV-JEPA共享嵌套宽度参数，每步联合训练窄、宽与窄转宽三条路径，以冻结视频教师约束共同表示空间，并增加可调token压缩。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文§4.1：128 GPU、300epochs，Kinetics-710/SSv2/HowTo100M视频，冻结V-JEPA2 ViT-G教师；每步同时训练窄、宽、混合三路径。压缩器另需100epochs×300iterations、全局batch4096。不是本地测速，原预算显著超出单卡A100/A30或Mac；不下载全视频或尝试多臂训练。  jepa video-representation elastic-inference 多模态 世界建模：状态、生成与动作条件 为何训练窄模型和宽模型之外，还要专门训练“窄转宽”路径？ 两种宽度各自表现好，不保证窄模型中间状态可直接交给宽模型。混合路径显式训练切分层的升宽接口，并以共同冻结教师约束表示，使跨设备接力有训练依据；这与随意裁剪通道或在运行时硬接两个独立模型不同，也不能省掉接力通信成本。 例如手机先跑窄层再把状态交给服务器宽层；若从未训练这种交接，服务器接到的表示可能不在其熟悉的分布中。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ev-jepa" data-paper-title="EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference 基础模型 Meta Reality Labs Research 2026-10-09 固定容量的视频模型难以同时适配端侧预算和跨设备协作，独立训练不同宽度也不保证中间表示兼容。EV-JEPA共享嵌套宽度参数，每步联合训练窄、宽与窄转宽三条路径，以冻结视频教师约束共同表示空间，并增加可调token压缩。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文§4.1：128 GPU、300epochs，Kinetics-710/SSv2/HowTo100M视频，冻结V-JEPA2 ViT-G教师；每步同时训练窄、宽、混合三路径。压缩器另需100epochs×300iterations、全局batch4096。不是本地测速，原预算显著超出单卡A100/A30或Mac；不下载全视频或尝试多臂训练。  jepa video-representation elastic-inference 多模态 世界建模：状态、生成与动作条件 训练压缩器的切分层重建目标，与直接删掉 token，要求恢复什么信息？ 普通裁剪只减少保留位置，删除内容可能无法供后段读取；压缩器额外学习切分层重建，使压缩传输后的表示尽量适配后续计算。二者都减少输入量，但兼容性训练的目标不同。重建损失较低也不能自动推出端到端任务无损，更不等于本地已完成跨设备部署。 教学例：直接丢掉一半空间 token 与编码成较少 token 后训练重建，不是同一操作；后者尝试保留可供后续网络恢复的结构。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a740fcbaa2cbbe9d">训练压缩器的切分层重建目标，与直接删掉 token，要求恢复什么信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aev-jepa">EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Reality Labs Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>普通裁剪只减少保留位置，删除内容可能无法供后段读取；压缩器额外学习切分层重建，使压缩传输后的表示尽量适配后续计算。二者都减少输入量，但兼容性训练的目标不同。重建损失较低也不能自动推出端到端任务无损，更不等于本地已完成跨设备部署。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：直接丢掉一半空间 token 与编码成较少 token 后训练重建，不是同一操作；后者尝试保留可供后续网络恢复的结构。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14324">原论文</a> · <a href="../../../../reproductions/2610.14324-ev-jepa/">实现解读</a> · <a href="#qa-a740fcbaa2cbbe9d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ev-jepa" data-paper-title="EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference 基础模型 Meta Reality Labs Research 2026-10-09 固定容量的视频模型难以同时适配端侧预算和跨设备协作，独立训练不同宽度也不保证中间表示兼容。EV-JEPA共享嵌套宽度参数，每步联合训练窄、宽与窄转宽三条路径，以冻结视频教师约束共同表示空间，并增加可调token压缩。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文§4.1：128 GPU、300epochs，Kinetics-710/SSv2/HowTo100M视频，冻结V-JEPA2 ViT-G教师；每步同时训练窄、宽、混合三路径。压缩器另需100epochs×300iterations、全局batch4096。不是本地测速，原预算显著超出单卡A100/A30或Mac；不下载全视频或尝试多臂训练。  jepa video-representation elastic-inference 多模态 世界建模：状态、生成与动作条件 EV-JEPA 的教师是固定视频模型，还是跟随弹性学生更新的 EMA 副本？ 教师采用冻结 V-JEPA 2，为窄、宽和混合路径提供共同目标，不随学生做 EMA。三条学生路径共享嵌套参数，并在同一目标空间接受 masked-token L1 监督。固定教师不代表学生无需训练，也不能把只实现通道切片称为完成这种联合训练或跨设备能力验证。 教学例：一次学生更新会改变可切片的共享参数，教师输出仍由同一个固定模型产生；不能再按学生权重滑动平均偷偷改掉目标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-5a736aec4cf8931e">EV-JEPA 的教师是固定视频模型，还是跟随弹性学生更新的 EMA 副本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aev-jepa">EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Reality Labs Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>教师采用冻结 V-JEPA 2，为窄、宽和混合路径提供共同目标，不随学生做 EMA。三条学生路径共享嵌套参数，并在同一目标空间接受 masked-token L1 监督。固定教师不代表学生无需训练，也不能把只实现通道切片称为完成这种联合训练或跨设备能力验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：一次学生更新会改变可切片的共享参数，教师输出仍由同一个固定模型产生；不能再按学生权重滑动平均偷偷改掉目标。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、边界与后续触发条件；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14324">原论文</a> · <a href="../../../../reproductions/2610.14324-ev-jepa/">实现解读</a> · <a href="#qa-5a736aec4cf8931e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:smolwam" data-paper-title="SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices 基础模型 ML Collective 2026-10-09 Cosmos Policy 将机器人状态、两路相机、动作和未来状态编码为九个 latent frame，沿用视频生成接口：33 帧 VAE、T5-XXL、28-block 2B DiT、1764 tokens 和五步去噪。SmolWAM 并非只换一个轻量 action head，而是在保留预训练 trunk、token 原位置与 rectified-flow readout 的同时，逐项恢复接口改变造成的分布偏移。单帧 Wan VAE 配合 0.5M adapter，映射回原 clip latent 空间； 8 步仅是缩小训练机制诊断，不代表原68,830row/5000step效果。当前为 core_mechanism：真实 A100 已完成三 seed 缩放 teacher 蒸馏、两阶段布局课程与新 student LIBERO 闭环，不用 VQA/随机小网络替代。新 student 与 no-op 均无任务成功；原5000步蒸馏未重训，不能称 full_pipeline 或能力提升。本地对照口径：基线为同固定 LIBERO 初始状态实际执行的 no-op 策略，实验组为各 seed 新训练、validation-selected SmolWAM student；完整 teacher 保持率与相对提速不适用。  world-action-model robotics efficient-inference 多模态 世界建模：状态、生成与动作条件 SmolWAM 为什么把视频生成式机器人策略的整条接口都纳入轻量化？ 视频骨干、视觉编码、文字条件和动作表示都会影响推理成本，只缩小动作头仍可能留下大部分负担。SmolWAM 逐项改造这些接口，并恢复改变预训练分布造成的偏移。组件更小不等于原知识自动保留，既要检验前向等价和恢复训练，也要在真实控制协议下评估。 教学例：动作头很小，但仍运行大 VAE、长视觉序列和多步去噪，总成本未必低；轻量化需要看完整执行路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-smolwam-cc2de315" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0aa7cf4f31b523e5">SmolWAM 为什么把视频生成式机器人策略的整条接口都纳入轻量化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asmolwam">SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ML Collective</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>视频骨干、视觉编码、文字条件和动作表示都会影响推理成本，只缩小动作头仍可能留下大部分负担。SmolWAM 逐项改造这些接口，并恢复改变预训练分布造成的偏移。组件更小不等于原知识自动保留，既要检验前向等价和恢复训练，也要在真实控制协议下评估。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：动作头很小，但仍运行大 VAE、长视觉序列和多步去噪，总成本未必低；轻量化需要看完整执行路径。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13740">原论文</a> · <a href="../../../../reproductions/2610.13740-smolwam/">实现解读</a> · <a href="#qa-0aa7cf4f31b523e5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:smolwam" data-paper-title="SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices 基础模型 ML Collective 2026-10-09 Cosmos Policy 将机器人状态、两路相机、动作和未来状态编码为九个 latent frame，沿用视频生成接口：33 帧 VAE、T5-XXL、28-block 2B DiT、1764 tokens 和五步去噪。SmolWAM 并非只换一个轻量 action head，而是在保留预训练 trunk、token 原位置与 rectified-flow readout 的同时，逐项恢复接口改变造成的分布偏移。单帧 Wan VAE 配合 0.5M adapter，映射回原 clip latent 空间； 8 步仅是缩小训练机制诊断，不代表原68,830row/5000step效果。当前为 core_mechanism：真实 A100 已完成三 seed 缩放 teacher 蒸馏、两阶段布局课程与新 student LIBERO 闭环，不用 VQA/随机小网络替代。新 student 与 no-op 均无任务成功；原5000步蒸馏未重训，不能称 full_pipeline 或能力提升。本地对照口径：基线为同固定 LIBERO 初始状态实际执行的 no-op 策略，实验组为各 seed 新训练、validation-selected SmolWAM student；完整 teacher 保持率与相对提速不适用。  world-action-model robotics efficient-inference 多模态 世界建模：状态、生成与动作条件 为什么缩小动作查询接口时，还要保留原 token 位置与 rectified-flow 方向？ 预训练 trunk 已适应特定位置语义和从数据到噪声的速度定义，换轻量接口若同时改掉这些约定，会产生额外分布偏移。SmolWAM 逐项恢复适配而非只缩小动作头；载入权重成功也不能证明错误的噪声方向或位置设置下仍等价运行。 例如教师学的是噪声减数据的速度，若学生默认反向定义却仍套用原读出公式，动作恢复就可能朝错误方向变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:smolwam" data-paper-title="SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices 基础模型 ML Collective 2026-10-09 Cosmos Policy 将机器人状态、两路相机、动作和未来状态编码为九个 latent frame，沿用视频生成接口：33 帧 VAE、T5-XXL、28-block 2B DiT、1764 tokens 和五步去噪。SmolWAM 并非只换一个轻量 action head，而是在保留预训练 trunk、token 原位置与 rectified-flow readout 的同时，逐项恢复接口改变造成的分布偏移。单帧 Wan VAE 配合 0.5M adapter，映射回原 clip latent 空间； 8 步仅是缩小训练机制诊断，不代表原68,830row/5000step效果。当前为 core_mechanism：真实 A100 已完成三 seed 缩放 teacher 蒸馏、两阶段布局课程与新 student LIBERO 闭环，不用 VQA/随机小网络替代。新 student 与 no-op 均无任务成功；原5000步蒸馏未重训，不能称 full_pipeline 或能力提升。本地对照口径：基线为同固定 LIBERO 初始状态实际执行的 no-op 策略，实验组为各 seed 新训练、validation-selected SmolWAM student；完整 teacher 保持率与相对提速不适用。  world-action-model robotics efficient-inference 多模态 世界建模：状态、生成与动作条件 单帧 VAE 加 adapter 与直接换成单帧 VAE 有何不同？ 原 teacher 以视频 clip latent 接口训练，单帧编码的分布可能不同；adapter 将单帧结果映回原 clip latent 空间，以保留预训练 trunk 可用的输入结构。直接更换编码器省略这个恢复步骤，不能假定 token 位置相同就代表数值分布一致。 例如两个编码器都输出相同形状，数值尺度和时空语义仍可能不同；adapter 学的是让新单帧输入适应旧骨干。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:smolwam" data-paper-title="SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices 基础模型 ML Collective 2026-10-09 Cosmos Policy 将机器人状态、两路相机、动作和未来状态编码为九个 latent frame，沿用视频生成接口：33 帧 VAE、T5-XXL、28-block 2B DiT、1764 tokens 和五步去噪。SmolWAM 并非只换一个轻量 action head，而是在保留预训练 trunk、token 原位置与 rectified-flow readout 的同时，逐项恢复接口改变造成的分布偏移。单帧 Wan VAE 配合 0.5M adapter，映射回原 clip latent 空间； 8 步仅是缩小训练机制诊断，不代表原68,830row/5000step效果。当前为 core_mechanism：真实 A100 已完成三 seed 缩放 teacher 蒸馏、两阶段布局课程与新 student LIBERO 闭环，不用 VQA/随机小网络替代。新 student 与 no-op 均无任务成功；原5000步蒸馏未重训，不能称 full_pipeline 或能力提升。本地对照口径：基线为同固定 LIBERO 初始状态实际执行的 no-op 策略，实验组为各 seed 新训练、validation-selected SmolWAM student；完整 teacher 保持率与相对提速不适用。  world-action-model robotics efficient-inference 多模态 世界建模：状态、生成与动作条件 这里的 rectified-flow 速度方向与 LeWAM 相同吗？ 不同。SmolWAM 沿 teacher 的数据到噪声方向，插值 xτ=(1-τ)x0+τε，速度为 ε-x0，干净估计应与此符号一致；LeWAM 使用相反方向。还需保留十二个指定 block、原位置及零偏置 sink，不能只照抄另一篇 flow 公式。 例如从噪声端反推干净动作时若把速度符号颠倒，会朝错误方向更新；损失数值可运行并不说明读取方向正确。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:lewam" data-paper-title="LeWAM: End-to-End World and Action Modeling with JEPAs" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="LeWAM: End-to-End World and Action Modeling with JEPAs 基础模型 UC San Diego 2026-10-08 传统 JEPA 学习“给定动作会到什么状态”，之后另训逆动力学或在线搜索动作。两阶段会使控制监督无法塑造视觉表征，宽高斯动作搜索也较昂贵。LeWAM 在同一训练阶段更新视觉编码器、潜在动力学和随机策略：既预测动作导致的未来 latent，又通过 flow matching 学习如何行动。视觉编码器由从零训练的 ResNet-18、空间 softmax 和两层投影 MLP 组成。模拟版本约 16.9M 参数，latent/MoT 宽度 192，4 层、4 头。 当前为 core_mechanism：真实 A100 已完成三 seed 缩放联合训练→新候选三臂闭环，证据绑定实际源码与权重哈希。目标来自训练轨迹，仍是非 holdout 诊断；未观测到规划相对 reactive 的优势，不宣称完整论文效果复现。本地对照口径：本轮真实测量用各 seed 的新训练、validation-selected checkpoint；基线为同一候选的 reactive policy，实验组为 best-of-K 与梯度规划。原目标来自训练轨迹，稳定能力相对提升不适用。发布模型入口仍保留，但未将其成绩冒充新候选成绩。  world-action-model jepa latent-planning 多模态 世界建模：状态、生成与动作条件 LeWAM 为什么希望“预测动作后果”和“产生可用动作”在训练时互相联系？ 世界模型能预测给定动作的未来，却不一定高效找到达到目标的动作；另训策略又可能无法让控制需求塑造视觉表示。LeWAM 联合学习视觉状态、动力学和随机动作策略，使预测与控制共享训练信号。联合目标并不免除信息隔离或真实执行验证，模型规划也可能失准。 教学例：模型知道推一下物体会移动，却仍需决定往哪推、推多远；动作学习与未来预测相连，才能为具体目标产生候选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-lewam-7895d3a3" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-1a6959f95b4f9227">LeWAM 为什么希望“预测动作后果”和“产生可用动作”在训练时互相联系？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alewam">LeWAM: End-to-End World and Action Modeling with JEPAs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>世界模型能预测给定动作的未来，却不一定高效找到达到目标的动作；另训策略又可能无法让控制需求塑造视觉表示。LeWAM 联合学习视觉状态、动力学和随机动作策略，使预测与控制共享训练信号。联合目标并不免除信息隔离或真实执行验证，模型规划也可能失准。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：模型知道推一下物体会移动，却仍需决定往哪推、推多远；动作学习与未来预测相连，才能为具体目标产生候选。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12818">原论文</a> · <a href="../../../../reproductions/2610.12818-lewam/">实现解读</a> · <a href="#qa-1a6959f95b4f9227">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:lewam" data-paper-title="LeWAM: End-to-End World and Action Modeling with JEPAs" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="LeWAM: End-to-End World and Action Modeling with JEPAs 基础模型 UC San Diego 2026-10-08 传统 JEPA 学习“给定动作会到什么状态”，之后另训逆动力学或在线搜索动作。两阶段会使控制监督无法塑造视觉表征，宽高斯动作搜索也较昂贵。LeWAM 在同一训练阶段更新视觉编码器、潜在动力学和随机策略：既预测动作导致的未来 latent，又通过 flow matching 学习如何行动。视觉编码器由从零训练的 ResNet-18、空间 softmax 和两层投影 MLP 组成。模拟版本约 16.9M 参数，latent/MoT 宽度 192，4 层、4 头。 当前为 core_mechanism：真实 A100 已完成三 seed 缩放联合训练→新候选三臂闭环，证据绑定实际源码与权重哈希。目标来自训练轨迹，仍是非 holdout 诊断；未观测到规划相对 reactive 的优势，不宣称完整论文效果复现。本地对照口径：本轮真实测量用各 seed 的新训练、validation-selected checkpoint；基线为同一候选的 reactive policy，实验组为 best-of-K 与梯度规划。原目标来自训练轨迹，稳定能力相对提升不适用。发布模型入口仍保留，但未将其成绩冒充新候选成绩。  world-action-model jepa latent-planning 多模态 世界建模：状态、生成与动作条件 为什么 LeWAM 的噪声动作分支不能经中间层读取干净动作？ 干净动作作为未来动力学监督，在训练中可供状态查询使用，却不是部署时策略已知的信息。如果噪声动作通过共享注意力偷读它，就可能复制目标而不学从观察和目标生成动作。分支独立参数不够，必须同时约束跨层可见性以堵住间接泄漏。 例如训练给出真实“向左推”的动作供预测未来；生成动作的噪声分支不能先看见这个答案，再把恢复结果算成决策能力。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:lewam" data-paper-title="LeWAM: End-to-End World and Action Modeling with JEPAs" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="LeWAM: End-to-End World and Action Modeling with JEPAs 基础模型 UC San Diego 2026-10-08 传统 JEPA 学习“给定动作会到什么状态”，之后另训逆动力学或在线搜索动作。两阶段会使控制监督无法塑造视觉表征，宽高斯动作搜索也较昂贵。LeWAM 在同一训练阶段更新视觉编码器、潜在动力学和随机策略：既预测动作导致的未来 latent，又通过 flow matching 学习如何行动。视觉编码器由从零训练的 ResNet-18、空间 softmax 和两层投影 MLP 组成。模拟版本约 16.9M 参数，latent/MoT 宽度 192，4 层、4 头。 当前为 core_mechanism：真实 A100 已完成三 seed 缩放联合训练→新候选三臂闭环，证据绑定实际源码与权重哈希。目标来自训练轨迹，仍是非 holdout 诊断；未观测到规划相对 reactive 的优势，不宣称完整论文效果复现。本地对照口径：本轮真实测量用各 seed 的新训练、validation-selected checkpoint；基线为同一候选的 reactive policy，实验组为 best-of-K 与梯度规划。原目标来自训练轨迹，稳定能力相对提升不适用。发布模型入口仍保留，但未将其成绩冒充新候选成绩。  world-action-model jepa latent-planning 多模态 世界建模：状态、生成与动作条件 LeWAM 的动作 flow 策略与宽高斯随机搜索的区别是什么？ flow matching 学习从噪声到动作数据的速度场，提供更接近训练动作分布的候选，再在潜在动力学中规划。宽高斯搜索主要靠无结构采样覆盖动作；学得的候选可能更集中，但真实优势仍需独立控制任务验证，不能靠训练损失推断。 例如推物体时，学得策略可优先给出贴近桌面的推法，而不是大量采样穿过桌面的无效动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:lewam" data-paper-title="LeWAM: End-to-End World and Action Modeling with JEPAs" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="LeWAM: End-to-End World and Action Modeling with JEPAs 基础模型 UC San Diego 2026-10-08 传统 JEPA 学习“给定动作会到什么状态”，之后另训逆动力学或在线搜索动作。两阶段会使控制监督无法塑造视觉表征，宽高斯动作搜索也较昂贵。LeWAM 在同一训练阶段更新视觉编码器、潜在动力学和随机策略：既预测动作导致的未来 latent，又通过 flow matching 学习如何行动。视觉编码器由从零训练的 ResNet-18、空间 softmax 和两层投影 MLP 组成。模拟版本约 16.9M 参数，latent/MoT 宽度 192，4 层、4 头。 当前为 core_mechanism：真实 A100 已完成三 seed 缩放联合训练→新候选三臂闭环，证据绑定实际源码与权重哈希。目标来自训练轨迹，仍是非 holdout 诊断；未观测到规划相对 reactive 的优势，不宣称完整论文效果复现。本地对照口径：本轮真实测量用各 seed 的新训练、validation-selected checkpoint；基线为同一候选的 reactive policy，实验组为 best-of-K 与梯度规划。原目标来自训练轨迹，稳定能力相对提升不适用。发布模型入口仍保留，但未将其成绩冒充新候选成绩。  world-action-model jepa latent-planning 多模态 世界建模：状态、生成与动作条件 LeWAM 的动作精炼为什么用 proximity penalty 优化，却按原始 goal cost 选候选？ Adam 优化目标加入动作偏离采样计划的惩罚，限制精炼走得过远；最终选择则比较未加该项的 goal cost，让候选按到达目标的预测效果竞争。原始采样候选也保留，防止精炼退化。优化只更新动作，不把规划阶段误写成模型权重训练或真实任务成功保证。 教学例：精炼动作偏离原方案较多但更接近目标，最终应按目标误差比较；若精炼反而更差，仍可退回保留的原候选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c23e22f887512a09">LeWAM 的动作精炼为什么用 proximity penalty 优化，却按原始 goal cost 选候选？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alewam">LeWAM: End-to-End World and Action Modeling with JEPAs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Adam 优化目标加入动作偏离采样计划的惩罚，限制精炼走得过远；最终选择则比较未加该项的 goal cost，让候选按到达目标的预测效果竞争。原始采样候选也保留，防止精炼退化。优化只更新动作，不把规划阶段误写成模型权重训练或真实任务成功保证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：精炼动作偏离原方案较多但更接近目标，最终应按目标误差比较；若精炼反而更差，仍可退回保留的原候选。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、数据协议、结果与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12818">原论文</a> · <a href="../../../../reproductions/2610.12818-lewam/">实现解读</a> · <a href="#qa-c23e22f887512a09">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:raw-video-midtraining" data-paper-title="Mid-Training Language Models on Raw Video" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Mid-Training Language Models on Raw Video 多模态大模型 Meta AI / Massachusetts Institute of Technology 2026-10-08 将有序帧的patch编码为连续视觉token并按空间顺序序列化；因果LM预测下一视觉token，目标侧stop-gradient。中期训练没有字幕或文本损失；随后与对照使用相同图文指令调优，隔离视频阶段贡献。原文§3–4 成本过高，不复现（审查 DONE）；Google/Meta优先补漏。成本过高，不复现（审查 DONE）；不以MSE演示冒充视频中期训练。原文§4.1.4使用128张H100训练27300步，batch256、16K上下文，之后还有指令调优。原始资源配置  视频理解与世界模型 无字幕视频中期训练 多模态 世界建模：状态、生成与动作条件 没有字幕的原始视频，为什么仍可能为语言模型提供有用的中期训练信号？ 视频的有序画面含有物体、运动和时空关联，不必全部先压成文字说明才能学习。该方法把帧 patch 编成连续视觉序列，让因果模型预测后续表示，利用原始视觉变化。预测视觉 token 并不等于生成字幕或掌握真实物理规律，后续能力还需匹配调优与评测。 教学例：杯子被拿起的连续帧包含运动关系，字幕可能只写“有人拿杯子”；直接视觉序列可提供文字未逐项标注的变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-multimodal-models-raw-video-midtraining-db4472b0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-176304cc6cc0aa4d">没有字幕的原始视频，为什么仍可能为语言模型提供有用的中期训练信号？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Araw-video-midtraining">Mid-Training Language Models on Raw Video</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI / Massachusetts Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>视频的有序画面含有物体、运动和时空关联，不必全部先压成文字说明才能学习。该方法把帧 patch 编成连续视觉序列，让因果模型预测后续表示，利用原始视觉变化。预测视觉 token 并不等于生成字幕或掌握真实物理规律，后续能力还需匹配调优与评测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：杯子被拿起的连续帧包含运动关系，字幕可能只写“有人拿杯子”；直接视觉序列可提供文字未逐项标注的变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与原文效果；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11019">原论文</a> · <a href="../../../../multimodal-models/2610.11019-raw-video-midtraining/">实现解读</a> · <a href="#qa-176304cc6cc0aa4d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:raw-video-midtraining" data-paper-title="Mid-Training Language Models on Raw Video" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Mid-Training Language Models on Raw Video 多模态大模型 Meta AI / Massachusetts Institute of Technology 2026-10-08 将有序帧的patch编码为连续视觉token并按空间顺序序列化；因果LM预测下一视觉token，目标侧stop-gradient。中期训练没有字幕或文本损失；随后与对照使用相同图文指令调优，隔离视频阶段贡献。原文§3–4 成本过高，不复现（审查 DONE）；Google/Meta优先补漏。成本过高，不复现（审查 DONE）；不以MSE演示冒充视频中期训练。原文§4.1.4使用128张H100训练27300步，batch256、16K上下文，之后还有指令调优。原始资源配置  视频理解与世界模型 无字幕视频中期训练 多模态 世界建模：状态、生成与动作条件 目标侧 stop-gradient 为什么不意味着视觉 tokenizer 完全冻结？ 目标路径停止梯度是防止预测目标跟随预测一起塌缩或移动，输入侧视觉 tokenizer 仍可通过 LM 与预测头接收梯度。模型在无字幕中期训练中学习视觉序列关系，之后需匹配的指令调优对照；不能把没有文字损失误解为整个视觉前端不训练。 例如用前一帧 patch 预测下一 patch，下一目标不反传，但前一输入经过的视觉参数仍可被预测误差更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:raw-video-midtraining" data-paper-title="Mid-Training Language Models on Raw Video" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Mid-Training Language Models on Raw Video 多模态大模型 Meta AI / Massachusetts Institute of Technology 2026-10-08 将有序帧的patch编码为连续视觉token并按空间顺序序列化；因果LM预测下一视觉token，目标侧stop-gradient。中期训练没有字幕或文本损失；随后与对照使用相同图文指令调优，隔离视频阶段贡献。原文§3–4 成本过高，不复现（审查 DONE）；Google/Meta优先补漏。成本过高，不复现（审查 DONE）；不以MSE演示冒充视频中期训练。原文§4.1.4使用128张H100训练27300步，batch256、16K上下文，之后还有指令调优。原始资源配置  视频理解与世界模型 无字幕视频中期训练 多模态 世界建模：状态、生成与动作条件 与视频 caption 训练相比，raw video 路线避免了什么监督瓶颈？ caption 只保留文字描述覆盖的视觉内容，可能省略连续运动和细节；连续 token 预测直接利用原始视频顺序。它也引入更长序列与视觉回归训练成本，不能因为没有字幕就推断语义必然更好，后续还需匹配的图文指令调优比较。 例如字幕只写“球移动”，原始连续表示仍含路径与速度变化；但模型能否利用这些信息需要实际下游评测。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:raw-video-midtraining" data-paper-title="Mid-Training Language Models on Raw Video" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Mid-Training Language Models on Raw Video 多模态大模型 Meta AI / Massachusetts Institute of Technology 2026-10-08 将有序帧的patch编码为连续视觉token并按空间顺序序列化；因果LM预测下一视觉token，目标侧stop-gradient。中期训练没有字幕或文本损失；随后与对照使用相同图文指令调优，隔离视频阶段贡献。原文§3–4 成本过高，不复现（审查 DONE）；Google/Meta优先补漏。成本过高，不复现（审查 DONE）；不以MSE演示冒充视频中期训练。原文§4.1.4使用128张H100训练27300步，batch256、16K上下文，之后还有指令调优。原始资源配置  视频理解与世界模型 无字幕视频中期训练 多模态 世界建模：状态、生成与动作条件 视频中期训练后的图文指令调优，为什么必须与对照使用同一口径？ 最终能力同时受视频阶段与后续指令调优影响，若两侧调优数据或流程不同，就难把差异归因于 raw-video 阶段。论文用匹配图文指令调优隔离其贡献，文本保真结论也限于这一协议。不能据此推广为任意无字幕视频训练都不遗忘，本地组件不代替完整对照训练。 教学例：视频组多做一轮优质指令训练而基线没有，最终图像问答涨分就混入额外监督；需要先对齐后续调优条件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-9a155f198062cb83">视频中期训练后的图文指令调优，为什么必须与对照使用同一口径？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Araw-video-midtraining">Mid-Training Language Models on Raw Video</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI / Massachusetts Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最终能力同时受视频阶段与后续指令调优影响，若两侧调优数据或流程不同，就难把差异归因于 raw-video 阶段。论文用匹配图文指令调优隔离其贡献，文本保真结论也限于这一协议。不能据此推广为任意无字幕视频训练都不遗忘，本地组件不代替完整对照训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：视频组多做一轮优质指令训练而基线没有，最终图像问答涨分就混入额外监督；需要先对齐后续调优条件。</p>
<p class="ar-learning-sources">依据：核心公式与原文效果、本地复现与成本决策；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11019">原论文</a> · <a href="../../../../multimodal-models/2610.11019-raw-video-midtraining/">实现解读</a> · <a href="#qa-9a155f198062cb83">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:woven" data-paper-title="WOVEN: Weaving Visual World Modeling into Multimodal LLMs" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="WOVEN: Weaving Visual World Modeling into Multimodal LLMs 多模态大模型 Northwestern University 2026-10-08 静态识别不等于理解状态变化。WOVEN以为共同对象，用视频生成模型rollout提供结果/中间状态，而非在prompt里预写结果。相同初始状态在不同动作下的rollout提供counterfactual候选；按scene、action、reasoning三个轴形成可控监督，用error-typed distractors区分错误机制。该paper的核心是真实视觉转移监督进入MLLM训练，不是训练图片class scorer。 相对原论文benchmark不适用，source_id分组小样本accuracy只用于L1诊断。本地对照口径：同一冻结公共VLM零LoRA残差为基线，真实transition response SFT为实验组；相对原论文benchmark不适用，source_id分组小样本accuracy只用于L1诊断。  multimodal-foundation-model visual-transition-reasoning world-model-supervision 多模态 世界建模：状态、生成与动作条件 WOVEN 的状态转移监督为什么不是普通静态图片分类？ 共同对象是初始状态、动作与结果状态的关系，可要求前向预测、反推动作或反事实结果。视频生成 rollout 提供实际视觉转移及中间帧，而非在 prompt 里直接写结果；仅辨认物体类别无法覆盖这些操作，也不能替代模型对转移关系的学习。 例如同一初始球位，左推与右推得到不同结果，问题可要求选动作或选后果，不是只回答画面里有没有球。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:woven" data-paper-title="WOVEN: Weaving Visual World Modeling into Multimodal LLMs" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="WOVEN: Weaving Visual World Modeling into Multimodal LLMs 多模态大模型 Northwestern University 2026-10-08 静态识别不等于理解状态变化。WOVEN以为共同对象，用视频生成模型rollout提供结果/中间状态，而非在prompt里预写结果。相同初始状态在不同动作下的rollout提供counterfactual候选；按scene、action、reasoning三个轴形成可控监督，用error-typed distractors区分错误机制。该paper的核心是真实视觉转移监督进入MLLM训练，不是训练图片class scorer。 相对原论文benchmark不适用，source_id分组小样本accuracy只用于L1诊断。本地对照口径：同一冻结公共VLM零LoRA残差为基线，真实transition response SFT为实验组；相对原论文benchmark不适用，source_id分组小样本accuracy只用于L1诊断。  multimodal-foundation-model visual-transition-reasoning world-model-supervision 多模态 世界建模：状态、生成与动作条件 为什么要按初始场景或 source 分组切分，而不能随机拆散视觉转移问答？ 同一初始图像可以衍生多个动作、问题与反事实选项，随机按题切分可能把几乎相同的视觉状态放进训练和测试。分组隔离减少这种捷径，再区分场景、动作与推理操作的迁移；高同源问答分数不能自动说明理解了未知场景的状态变化。 例如同一桌面分别问“向左推会怎样”和“什么动作导致杯子移动”，两题共享底图，应作为一组切分而非分居训练测试。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:woven" data-paper-title="WOVEN: Weaving Visual World Modeling into Multimodal LLMs" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="WOVEN: Weaving Visual World Modeling into Multimodal LLMs 多模态大模型 Northwestern University 2026-10-08 静态识别不等于理解状态变化。WOVEN以为共同对象，用视频生成模型rollout提供结果/中间状态，而非在prompt里预写结果。相同初始状态在不同动作下的rollout提供counterfactual候选；按scene、action、reasoning三个轴形成可控监督，用error-typed distractors区分错误机制。该paper的核心是真实视觉转移监督进入MLLM训练，不是训练图片class scorer。 相对原论文benchmark不适用，source_id分组小样本accuracy只用于L1诊断。本地对照口径：同一冻结公共VLM零LoRA残差为基线，真实transition response SFT为实验组；相对原论文benchmark不适用，source_id分组小样本accuracy只用于L1诊断。  multimodal-foundation-model visual-transition-reasoning world-model-supervision 多模态 世界建模：状态、生成与动作条件 scene-OOD 与 state-perturbation 测试区分什么泛化问题？ scene-OOD 改变场景分布，state-perturbation 检查状态变化下的鲁棒性，两者不能因 ID 准确率高就视为解决。原文受控轴还含 action 与 reasoning，不同监督操作对迁移的贡献需分别比较，不能把按不同 benchmark 选 subset 的覆盖当成单模型全面提升。 例如模型在新餐厅场景表现好，仍可能对同一场景里物体位置的小变化敏感；两种测试关注不同失效模式。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:woven" data-paper-title="WOVEN: Weaving Visual World Modeling into Multimodal LLMs" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="WOVEN: Weaving Visual World Modeling into Multimodal LLMs 多模态大模型 Northwestern University 2026-10-08 静态识别不等于理解状态变化。WOVEN以为共同对象，用视频生成模型rollout提供结果/中间状态，而非在prompt里预写结果。相同初始状态在不同动作下的rollout提供counterfactual候选；按scene、action、reasoning三个轴形成可控监督，用error-typed distractors区分错误机制。该paper的核心是真实视觉转移监督进入MLLM训练，不是训练图片class scorer。 相对原论文benchmark不适用，source_id分组小样本accuracy只用于L1诊断。本地对照口径：同一冻结公共VLM零LoRA残差为基线，真实transition response SFT为实验组；相对原论文benchmark不适用，source_id分组小样本accuracy只用于L1诊断。  multimodal-foundation-model visual-transition-reasoning world-model-supervision 多模态 世界建模：状态、生成与动作条件 四种 option permutation 与 source_id 分组分别防什么问题？ 排列选项时要同步搬迁目标字母而保持内容和图像对应，避免固定字母捷径；划分按初始来源分组，防同源状态的不同问法跨集合泄露。prompt 只投影问题、选项和真实图像，distractor_type 等答案相关字段不能进入模型，本地也只运行 SFT 未运行 GRPO。 例如同一初始帧生成三道题，应一起划到训练或留出；否则模型可记住来源，再在所谓 test 回答变体问题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:stratified-retention-protocol" data-paper-title="What Should World Models Forget? Stratified Retention for Continual Adaptation" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="What Should World Models Forget? Stratified Retention for Continual Adaptation 基础模型 University of Maryland, College Park 2026-10-02 世界会变化：椅子移动后继续预测旧位置不是“记忆好”，而是知识过期；但物体永久性等结构知识不应随一次适应丢失。作者按环境知识保持为真的时间尺度分四层：不变量、长期环境规律、短期实例配置、即时状态。这里的时间尺度不是缓存 TTL，即时状态也不应统统写入权重。§3—5 单看旧任务准确率会奖励冻结模型。论文因此要求分别报告不变量保持、变化后的修订延迟，以及短暂扰动引起的假修订，不合成一个掩盖取舍的总分。 诊断输入包含先失效后恢复的不变量、改正旧错误、一直不改的冻结轨迹和临近结束的删失变化。L0 评测协议组件，非持续学习算法。原文是无新实证的研究提案；本地实现审计算术，不训练世界模型，也不声称获得更好的记忆或适应能力。ProbeRound/invariant_retention 接收外部评测结果，不接收模型、标签到策略的通路；要求 probe ID 固定且与适应样本不重叠。ChangeTrace/revision_report 显式区分 regularity、instance，要求评测 episode 不同于适应 episode，输出延迟、从未修订数与右删失数。  预训练与数据 持续适应与评测协议 多模态 世界建模：状态、生成与动作条件 椅子搬走后不再预测旧位置，为什么不应直接记成遗忘？ 旧位置已经不真实，应修订；物体永久性等不变量仍应保持。论文按环境中知识为真的时间尺度分层，不把所有旧答案都当必须保留。 教学例：门从开变关后预测关是正确更新；随后把“遮挡物仍存在”也忘掉才是不变量负翻转。 2026-11-18">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-stratified-retention-protocol-5f3cc655" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-284724fe14c075e2">椅子搬走后不再预测旧位置，为什么不应直接记成遗忘？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Astratified-retention-protocol">What Should World Models Forget? Stratified Retention for Continual Adaptation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-18 · University of Maryland, College Park</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>旧位置已经不真实，应修订；物体永久性等不变量仍应保持。论文按环境中知识为真的时间尺度分层，不把所有旧答案都当必须保留。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：门从开变关后预测关是正确更新；随后把“遮挡物仍存在”也忘掉才是不变量负翻转。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03713v2">原论文</a> · <a href="../../../../foundation-models/2610.03713-stratified-retention-protocol/">实现解读</a> · <a href="#qa-284724fe14c075e2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:stratified-retention-protocol" data-paper-title="What Should World Models Forget? Stratified Retention for Continual Adaptation" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="What Should World Models Forget? Stratified Retention for Continual Adaptation 基础模型 University of Maryland, College Park 2026-10-02 世界会变化：椅子移动后继续预测旧位置不是“记忆好”，而是知识过期；但物体永久性等结构知识不应随一次适应丢失。作者按环境知识保持为真的时间尺度分四层：不变量、长期环境规律、短期实例配置、即时状态。这里的时间尺度不是缓存 TTL，即时状态也不应统统写入权重。§3—5 单看旧任务准确率会奖励冻结模型。论文因此要求分别报告不变量保持、变化后的修订延迟，以及短暂扰动引起的假修订，不合成一个掩盖取舍的总分。 诊断输入包含先失效后恢复的不变量、改正旧错误、一直不改的冻结轨迹和临近结束的删失变化。L0 评测协议组件，非持续学习算法。原文是无新实证的研究提案；本地实现审计算术，不训练世界模型，也不声称获得更好的记忆或适应能力。ProbeRound/invariant_retention 接收外部评测结果，不接收模型、标签到策略的通路；要求 probe ID 固定且与适应样本不重叠。ChangeTrace/revision_report 显式区分 regularity、instance，要求评测 episode 不同于适应 episode，输出延迟、从未修订数与右删失数。  预训练与数据 持续适应与评测协议 多模态 世界建模：状态、生成与动作条件 修订延迟为什么不能用第一次答对或最终准确率代替？ 一次新事实偏好可能是瞬时抖动，需在新episode查询上连续超过已声明margin；延迟按相关区域观察次数计。未达门槛与临近结束无法判断的右删失必须分开。 教学例：差值0.2、-0.2、0.2、0.2，margin0.1、连续2次时延迟为4次观察，不是1；只来得及观察1次的变化应单列censored。 2026-11-18">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-a53ec8eb662bfa60">修订延迟为什么不能用第一次答对或最终准确率代替？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Astratified-retention-protocol">What Should World Models Forget? Stratified Retention for Continual Adaptation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-18 · University of Maryland, College Park</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一次新事实偏好可能是瞬时抖动，需在新episode查询上连续超过已声明margin；延迟按相关区域观察次数计。未达门槛与临近结束无法判断的右删失必须分开。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：差值0.2、-0.2、0.2、0.2，margin0.1、连续2次时延迟为4次观察，不是1；只来得及观察1次的变化应单列censored。</p>
<p class="ar-learning-sources">依据：核心公式、数据协议与代码映射；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03713v2">原论文</a> · <a href="../../../../foundation-models/2610.03713-stratified-retention-protocol/">实现解读</a> · <a href="#qa-a53ec8eb662bfa60">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:stratified-retention-protocol" data-paper-title="What Should World Models Forget? Stratified Retention for Continual Adaptation" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="What Should World Models Forget? Stratified Retention for Continual Adaptation 基础模型 University of Maryland, College Park 2026-10-02 世界会变化：椅子移动后继续预测旧位置不是“记忆好”，而是知识过期；但物体永久性等结构知识不应随一次适应丢失。作者按环境知识保持为真的时间尺度分四层：不变量、长期环境规律、短期实例配置、即时状态。这里的时间尺度不是缓存 TTL，即时状态也不应统统写入权重。§3—5 单看旧任务准确率会奖励冻结模型。论文因此要求分别报告不变量保持、变化后的修订延迟，以及短暂扰动引起的假修订，不合成一个掩盖取舍的总分。 诊断输入包含先失效后恢复的不变量、改正旧错误、一直不改的冻结轨迹和临近结束的删失变化。L0 评测协议组件，非持续学习算法。原文是无新实证的研究提案；本地实现审计算术，不训练世界模型，也不声称获得更好的记忆或适应能力。ProbeRound/invariant_retention 接收外部评测结果，不接收模型、标签到策略的通路；要求 probe ID 固定且与适应样本不重叠。ChangeTrace/revision_report 显式区分 regularity、instance，要求评测 episode 不同于适应 episode，输出延迟、从未修订数与右删失数。  预训练与数据 持续适应与评测协议 多模态 世界建模：状态、生成与动作条件 Stratified Retention和WOVEN都讨论状态变化，为什么不是两种可直接排名的训练算法？ WOVEN用视觉转移构造监督并训练MLLM；Stratified Retention提出应保留什么和怎样测修订，没有新训练算法或实证。评测协议可约束未来实验，但不能冒充训练收益。 教学例：WOVEN的source_id分组防止相同初始图跨切分；分层保持还要求逐轮不变量probe和新episode修订轨迹，二者测的轴不同。 2026-11-18">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-363ef434f77abd35">Stratified Retention和WOVEN都讨论状态变化，为什么不是两种可直接排名的训练算法？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Astratified-retention-protocol">What Should World Models Forget? Stratified Retention for Continual Adaptation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-18 · University of Maryland, College Park</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>WOVEN用视觉转移构造监督并训练MLLM；Stratified Retention提出应保留什么和怎样测修订，没有新训练算法或实证。评测协议可约束未来实验，但不能冒充训练收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：WOVEN的source_id分组防止相同初始图跨切分；分层保持还要求逐轮不变量probe和新episode修订轨迹，二者测的轴不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、论文离线与线上效果、完整实验状态；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03713v2">原论文</a> · <a href="../../../../foundation-models/2610.03713-stratified-retention-protocol/">实现解读</a> · <a href="#qa-363ef434f77abd35">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:stratified-retention-protocol" data-paper-title="What Should World Models Forget? Stratified Retention for Continual Adaptation" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="What Should World Models Forget? Stratified Retention for Continual Adaptation 基础模型 University of Maryland, College Park 2026-10-02 世界会变化：椅子移动后继续预测旧位置不是“记忆好”，而是知识过期；但物体永久性等结构知识不应随一次适应丢失。作者按环境知识保持为真的时间尺度分四层：不变量、长期环境规律、短期实例配置、即时状态。这里的时间尺度不是缓存 TTL，即时状态也不应统统写入权重。§3—5 单看旧任务准确率会奖励冻结模型。论文因此要求分别报告不变量保持、变化后的修订延迟，以及短暂扰动引起的假修订，不合成一个掩盖取舍的总分。 诊断输入包含先失效后恢复的不变量、改正旧错误、一直不改的冻结轨迹和临近结束的删失变化。L0 评测协议组件，非持续学习算法。原文是无新实证的研究提案；本地实现审计算术，不训练世界模型，也不声称获得更好的记忆或适应能力。ProbeRound/invariant_retention 接收外部评测结果，不接收模型、标签到策略的通路；要求 probe ID 固定且与适应样本不重叠。ChangeTrace/revision_report 显式区分 regularity、instance，要求评测 episode 不同于适应 episode，输出延迟、从未修订数与右删失数。  预训练与数据 持续适应与评测协议 多模态 世界建模：状态、生成与动作条件 本地协议怎样避免把“记住刚见过的答案”当成修订能力？ 固定probe ID必须与适应样本ID不重叠，ChangeTrace查询episode必须不同于适应episode。模块只读外部评测结果，没有模型或gold到策略的接口；人工轨迹只作L0反例。 教学例：adaptation_ids含gravity时，gravity不能同时出现在held-out面板；query_episode=adaptation_episode也直接报错。 2026-11-18">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-171e7767e46e5b4c">本地协议怎样避免把“记住刚见过的答案”当成修订能力？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Astratified-retention-protocol">What Should World Models Forget? Stratified Retention for Continual Adaptation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-18 · University of Maryland, College Park</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定probe ID必须与适应样本ID不重叠，ChangeTrace查询episode必须不同于适应episode。模块只读外部评测结果，没有模型或gold到策略的接口；人工轨迹只作L0反例。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：adaptation_ids含gravity时，gravity不能同时出现在held-out面板；query_episode=adaptation_episode也直接报错。</p>
<p class="ar-learning-sources">依据：数据协议与代码映射、结果、负控与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.03713v2">原论文</a> · <a href="../../../../foundation-models/2610.03713-stratified-retention-protocol/">实现解读</a> · <a href="#qa-171e7767e46e5b4c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:vjepa-policy" data-paper-title="V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents 基础模型 Tsinghua University 2026-09-29 冻结 V-JEPA 2.1 视觉编码器，在预测视觉潜空间中联合训练 instruction-conditioned future-latent predictor 和 flow-matching action expert；动作生成读取 predictor 的未来信息上下文。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 future-latent stop-gradient 与 action flow matching；未加载 V-JEPA 2.1 或机器人数据。执行 future-latent stop-gradient 与 action flow matching；未加载 V-JEPA 2.1 或机器人数据。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  世界动作模型 预测视觉潜变量 机器人 多模态 世界建模：状态、生成与动作条件 机器人动作策略为什么会从“预测将看到什么”中获得额外条件？ 仅靠当前图像选择动作，可能缺少目标执行后场景如何变化的线索。V-JEPA Policy 将指令条件未来表示预测与动作学习联系起来，让动作专家读取预测上下文。未来信息必须来自模型预测，不能在控制时偷读真实后续视频；预测有误也会影响动作，因此仍需实际执行验证。 教学例：指令要求把杯子放入盒子，未来表示可帮助描述目标视觉状态；机器人尚未行动，不能直接读取任务结束后的真实画面。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-vjepa-policy-d720eedd" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5edd75f877906c0b">机器人动作策略为什么会从“预测将看到什么”中获得额外条件？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Avjepa-policy">V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>仅靠当前图像选择动作，可能缺少目标执行后场景如何变化的线索。V-JEPA Policy 将指令条件未来表示预测与动作学习联系起来，让动作专家读取预测上下文。未来信息必须来自模型预测，不能在控制时偷读真实后续视频；预测有误也会影响动作，因此仍需实际执行验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：指令要求把杯子放入盒子，未来表示可帮助描述目标视觉状态；机器人尚未行动，不能直接读取任务结束后的真实画面。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37250">原论文</a> · <a href="../../../../foundation-models/2609.37250-vjepa-policy/">实现解读</a> · <a href="#qa-5edd75f877906c0b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:vjepa-policy" data-paper-title="V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents 基础模型 Tsinghua University 2026-09-29 冻结 V-JEPA 2.1 视觉编码器，在预测视觉潜空间中联合训练 instruction-conditioned future-latent predictor 和 flow-matching action expert；动作生成读取 predictor 的未来信息上下文。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 future-latent stop-gradient 与 action flow matching；未加载 V-JEPA 2.1 或机器人数据。执行 future-latent stop-gradient 与 action flow matching；未加载 V-JEPA 2.1 或机器人数据。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  世界动作模型 预测视觉潜变量 机器人 多模态 世界建模：状态、生成与动作条件 动作专家读取预测未来潜变量，与直接读取训练视频未来帧有何区别？ 预测未来由当前观察与指令生成，部署时也能获得；真实未来仅作为训练目标，用于塑造预测器。动作 flow expert 因而使用可计算的前瞻上下文，而非提前观察结果。冻结视觉编码器稳定表示，却不保证预测误差不会在控制过程中累积。 例如根据当前桌面预测抓取后的杯子位置，再产生动作；不能把实际抓取结束后的照片先传给策略再评价成功率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:vjepa-policy" data-paper-title="V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents 基础模型 Tsinghua University 2026-09-29 冻结 V-JEPA 2.1 视觉编码器，在预测视觉潜空间中联合训练 instruction-conditioned future-latent predictor 和 flow-matching action expert；动作生成读取 predictor 的未来信息上下文。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 future-latent stop-gradient 与 action flow matching；未加载 V-JEPA 2.1 或机器人数据。执行 future-latent stop-gradient 与 action flow matching；未加载 V-JEPA 2.1 或机器人数据。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  世界动作模型 预测视觉潜变量 机器人 多模态 世界建模：状态、生成与动作条件 联合世界与动作训练与先训预测器再独立训动作头有什么区别？ 联合训练让未来预测与动作 flow 在同一训练框架中协调，动作专家使用 predictor 提供的未来信息；两阶段独立训练则可能让预测表征未适配控制需要。这里视觉 encoder 仍冻结，不能将联合 predictor/action 训练扩大为所有视觉参数都端到端更新。 例如动作头需要未来抓取位置，联合训练可协调预测上下文；但冻结 V-JEPA 编码器的权重依然不会因动作损失而变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:vjepa-policy" data-paper-title="V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents 基础模型 Tsinghua University 2026-09-29 冻结 V-JEPA 2.1 视觉编码器，在预测视觉潜空间中联合训练 instruction-conditioned future-latent predictor 和 flow-matching action expert；动作生成读取 predictor 的未来信息上下文。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 future-latent stop-gradient 与 action flow matching；未加载 V-JEPA 2.1 或机器人数据。执行 future-latent stop-gradient 与 action flow matching；未加载 V-JEPA 2.1 或机器人数据。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  世界动作模型 预测视觉潜变量 机器人 多模态 世界建模：状态、生成与动作条件 future target 的梯度隔离与本地实现边界应怎样表述？ 真实未来经冻结视觉编码器产生目标并 stop-gradient，masked 位置上做 L1，同时训练动作速度损失。本地只执行 future-latent 隔离和 flow 机制诊断，没有加载 V-JEPA 2.1 或机器人数据，不能将三 seed 小张量更新说成 LIBERO 策略已验证。 例如检查目标张量没有梯度可确认监督边界，但没有任何机器人 rollout，就不能计算实际动作成功率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:vbvr-pro" data-paper-title="VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning 基础模型 Nanyang Technological University / VBVR Community 2026-08-26 通用 VLM judge 容易被流畅输出误导，难以逐实例核对时空状态。VBVR-Pro 为每种任务定义可执行 scorer，把中间状态、约束和最终状态都变成可验证奖励，并据此训练多模态生成模型。 Fidelity：核心机制的程序化验证。本地复刻 task-specific deterministic scorer 与标量 judge 对照，不训练视频生成大模型。该结果只验证 scorer 的确定性和可解释失败归因，不等同于论文七个外部 benchmark 或 14B/19B checkpoint 训练。本地对照口径：基线为带噪标量 VLM-judge analogue；实验组为三个确定性 task-specific verifier。300 个程序化任务 reward mean 0.5942 → 1.0000（+68.30%）。  multimodal-foundation-model native-visual-reasoning verifiable-reward benchmark 多模态 世界建模：状态、生成与动作条件 视觉推理生成了一个好看的终图，为什么还可能没有完成要求的任务？ 有些任务约束对象如何移动、何时经过某状态或是否避开禁区，终图正确也可能掩盖错误过程。VBVR-Pro 把这类任务规则变成可执行检查，为生成轨迹提供更具体反馈。程序化奖励覆盖已定义约束，不能自动衡量未定义的所有视觉质量，也不代表任意任务都有可靠 scorer。 教学例：物体最终到达目标点，但途中穿过禁止区域；只看终图会漏掉违反路径约束，过程检查才看得到。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-vbvr-pro-eb931970" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a689a1bd0391b575">视觉推理生成了一个好看的终图，为什么还可能没有完成要求的任务？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Avbvr-pro">VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University / VBVR Community</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>有些任务约束对象如何移动、何时经过某状态或是否避开禁区，终图正确也可能掩盖错误过程。VBVR-Pro 把这类任务规则变成可执行检查，为生成轨迹提供更具体反馈。程序化奖励覆盖已定义约束，不能自动衡量未定义的所有视觉质量，也不代表任意任务都有可靠 scorer。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：物体最终到达目标点，但途中穿过禁止区域；只看终图会漏掉违反路径约束，过程检查才看得到。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26105">原论文</a> · <a href="../../../../reproductions/2608.26105-vbvr-pro/">实现解读</a> · <a href="#qa-a689a1bd0391b575">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:vbvr-pro" data-paper-title="VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning 基础模型 Nanyang Technological University / VBVR Community 2026-08-26 通用 VLM judge 容易被流畅输出误导，难以逐实例核对时空状态。VBVR-Pro 为每种任务定义可执行 scorer，把中间状态、约束和最终状态都变成可验证奖励，并据此训练多模态生成模型。 Fidelity：核心机制的程序化验证。本地复刻 task-specific deterministic scorer 与标量 judge 对照，不训练视频生成大模型。该结果只验证 scorer 的确定性和可解释失败归因，不等同于论文七个外部 benchmark 或 14B/19B checkpoint 训练。本地对照口径：基线为带噪标量 VLM-judge analogue；实验组为三个确定性 task-specific verifier。300 个程序化任务 reward mean 0.5942 → 1.0000（+68.30%）。  multimodal-foundation-model native-visual-reasoning verifiable-reward benchmark 多模态 世界建模：状态、生成与动作条件 可执行 scorer 为什么比通用 VLM judge 更适合某些时空约束任务？ 任务若能明确列出中间状态、约束和最终条件，就可逐实例检查，而不只凭答案是否流畅判断。这样的奖励把可验证条件接入训练，但只覆盖已定义的规则；scorer 自身正确、被评模型不读 gold 与生成任务真正执行，仍是不同的验证要求。 例如移动方块不能穿墙且最终到达目标格，可逐步检查轨迹；一段听起来合理却实际穿墙的解释不应获得成功奖励。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:vbvr-pro" data-paper-title="VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning 基础模型 Nanyang Technological University / VBVR Community 2026-08-26 通用 VLM judge 容易被流畅输出误导，难以逐实例核对时空状态。VBVR-Pro 为每种任务定义可执行 scorer，把中间状态、约束和最终状态都变成可验证奖励，并据此训练多模态生成模型。 Fidelity：核心机制的程序化验证。本地复刻 task-specific deterministic scorer 与标量 judge 对照，不训练视频生成大模型。该结果只验证 scorer 的确定性和可解释失败归因，不等同于论文七个外部 benchmark 或 14B/19B checkpoint 训练。本地对照口径：基线为带噪标量 VLM-judge analogue；实验组为三个确定性 task-specific verifier。300 个程序化任务 reward mean 0.5942 → 1.0000（+68.30%）。  multimodal-foundation-model native-visual-reasoning verifiable-reward benchmark 多模态 世界建模：状态、生成与动作条件 约束奖励加权求和，与要求全部约束硬性通过，是不是同一种任务合同？ 加权和让各项满足程度贡献分数，高权重项目可能补偿低权重项目的失败；全部硬性通过则把任一违反视为不可行。两种定义表达不同偏好，不能从总分较高推断所有约束都满足。这是对论文公式的假设比较，不是声称作者另外做过这两种方法的对照实验。 教学例：两项各半权重的条件只过一项可得半分；若要求安全条件必须满足，即使其他项全对也不能把安全失败补偿掉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f61addb2d17becd9">约束奖励加权求和，与要求全部约束硬性通过，是不是同一种任务合同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Avbvr-pro">VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University / VBVR Community</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>加权和让各项满足程度贡献分数，高权重项目可能补偿低权重项目的失败；全部硬性通过则把任一违反视为不可行。两种定义表达不同偏好，不能从总分较高推断所有约束都满足。这是对论文公式的假设比较，不是声称作者另外做过这两种方法的对照实验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：两项各半权重的条件只过一项可得半分；若要求安全条件必须满足，即使其他项全对也不能把安全失败补偿掉。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26105">原论文</a> · <a href="../../../../reproductions/2608.26105-vbvr-pro/">实现解读</a> · <a href="#qa-f61addb2d17becd9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:vbvr-pro" data-paper-title="VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning 基础模型 Nanyang Technological University / VBVR Community 2026-08-26 通用 VLM judge 容易被流畅输出误导，难以逐实例核对时空状态。VBVR-Pro 为每种任务定义可执行 scorer，把中间状态、约束和最终状态都变成可验证奖励，并据此训练多模态生成模型。 Fidelity：核心机制的程序化验证。本地复刻 task-specific deterministic scorer 与标量 judge 对照，不训练视频生成大模型。该结果只验证 scorer 的确定性和可解释失败归因，不等同于论文七个外部 benchmark 或 14B/19B checkpoint 训练。本地对照口径：基线为带噪标量 VLM-judge analogue；实验组为三个确定性 task-specific verifier。300 个程序化任务 reward mean 0.5942 → 1.0000（+68.30%）。  multimodal-foundation-model native-visual-reasoning verifiable-reward benchmark 多模态 世界建模：状态、生成与动作条件 本地程序化 reward 从带噪基线到满分说明什么？ 只说明当前确定性 task-specific scorer 在给定程序化任务上的执行与失败归因，比带噪 judge analogue 稳定；不是多模态生成模型完成 RLVR 后的能力收益。原论文训练与外部 benchmark 需要真实轨迹、模型更新和独立评价，当前机制结果不能替代。 例如已知轨迹满足所有布尔条件时 scorer 返回一，验证的是评分器，不是证明生成模型能自己找到这样的轨迹。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:mice" data-paper-title="Editing Everything Everywhere All at Once" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Editing Everything Everywhere All at Once 多模态大模型 University of Modena and Reggio Emilia 2026-06-30 多区域同时编辑容易把一处指令的属性传到另一处。MICE 在联合注意力中隔离不同文字组，并用实例掩码的平滑空间偏置控制视觉交互，以兼顾局部绑定与周围区域融合。方法不训练新的编辑模型。 以单张 A100/A30 或 Mac 的资源限制评估，完整矩阵需要大权重、长时间生成和外部服务，标注成本过高，不复现（审查 DONE）。诊断使用 2 个生成掩码、6×8 raster 和随机 Q/K/V，真实执行 attention 与反向传播。实现 instance_aware_masks、instance_log_bias、mice_joint_bias、mice_joint_attention 和统一 diagnostic(seed, device)。模块导入不加载 PyTorch，实际调用时才需要。输入必须是已经在同一网格上的、非空、互不重叠的二值 mask；  视觉生成与编辑 多实例编辑与注意力隔离 多模态 世界建模：状态、生成与动作条件 同时编辑多个实例时，MICE 所说的属性串扰会怎样破坏用户指令？ 用户可能要求每个对象发生不同变化，若生成过程不能保持属性归属，一处颜色、形状或材质会传播到另一处。MICE 研究在无需新训练的编辑流程里维持局部绑定与周围融合。困难不是只生成更美图片，还要让每项变化落在指定实例，且不误改其他内容。 教学例：要求左杯变红、右杯变蓝，若两个杯子都变紫，就是不同编辑属性混在了一起；单一全局颜色描述难明确这种归属。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
<span id="paper-multimodal-models-mice-b52a199b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7fbd2b03fd6b9570">同时编辑多个实例时，MICE 所说的属性串扰会怎样破坏用户指令？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Amice">Editing Everything Everywhere All at Once</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Modena and Reggio Emilia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用户可能要求每个对象发生不同变化，若生成过程不能保持属性归属，一处颜色、形状或材质会传播到另一处。MICE 研究在无需新训练的编辑流程里维持局部绑定与周围融合。困难不是只生成更美图片，还要让每项变化落在指定实例，且不误改其他内容。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：要求左杯变红、右杯变蓝，若两个杯子都变紫，就是不同编辑属性混在了一起；单一全局颜色描述难明确这种归属。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.31278v1">原论文</a> · <a href="../../../../multimodal-models/2606.31278-mice/">实现解读</a> · <a href="#qa-7fbd2b03fd6b9570">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:mice" data-paper-title="Editing Everything Everywhere All at Once" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Editing Everything Everywhere All at Once 多模态大模型 University of Modena and Reggio Emilia 2026-06-30 多区域同时编辑容易把一处指令的属性传到另一处。MICE 在联合注意力中隔离不同文字组，并用实例掩码的平滑空间偏置控制视觉交互，以兼顾局部绑定与周围区域融合。方法不训练新的编辑模型。 以单张 A100/A30 或 Mac 的资源限制评估，完整矩阵需要大权重、长时间生成和外部服务，标注成本过高，不复现（审查 DONE）。诊断使用 2 个生成掩码、6×8 raster 和随机 Q/K/V，真实执行 attention 与反向传播。实现 instance_aware_masks、instance_log_bias、mice_joint_bias、mice_joint_attention 和统一 diagnostic(seed, device)。模块导入不加载 PyTorch，实际调用时才需要。输入必须是已经在同一网格上的、非空、互不重叠的二值 mask；  视觉生成与编辑 多实例编辑与注意力隔离 多模态 世界建模：状态、生成与动作条件 多实例编辑为什么同时需要文字组隔离与平滑空间偏置？ 文字组隔离减少一条编辑指令直接影响另一组语义，空间偏置则把该指令绑定到相应实例并允许边界附近融合。只有硬切区域可能产生接缝，只有全局文字约束又可能串色；偏置在注意力里控制可见性，并不等于训练了一个新的编辑模型。 例如要求左鞋变红、右鞋变蓝，文字组不应互相传播颜色，而平滑实例区域帮助各自颜色与周围图像自然衔接。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:mice" data-paper-title="Editing Everything Everywhere All at Once" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Editing Everything Everywhere All at Once 多模态大模型 University of Modena and Reggio Emilia 2026-06-30 多区域同时编辑容易把一处指令的属性传到另一处。MICE 在联合注意力中隔离不同文字组，并用实例掩码的平滑空间偏置控制视觉交互，以兼顾局部绑定与周围区域融合。方法不训练新的编辑模型。 以单张 A100/A30 或 Mac 的资源限制评估，完整矩阵需要大权重、长时间生成和外部服务，标注成本过高，不复现（审查 DONE）。诊断使用 2 个生成掩码、6×8 raster 和随机 Q/K/V，真实执行 attention 与反向传播。实现 instance_aware_masks、instance_log_bias、mice_joint_bias、mice_joint_attention 和统一 diagnostic(seed, device)。模块导入不加载 PyTorch，实际调用时才需要。输入必须是已经在同一网格上的、非空、互不重叠的二值 mask；  视觉生成与编辑 多实例编辑与注意力隔离 多模态 世界建模：状态、生成与动作条件 软空间偏置与对区域外 token 全部 hard mask 有何区别？ 平滑掩码取对数后给区域外有限负偏置，让边缘有逐渐衰减的交互以融合周围内容；hard mask 则彻底禁止。无关文字组仍用负无穷隔离，不能把所有边都统一软化；正文与作者默认代码还存在版本差异，本地明确遵循 paper_v1。 例如物体边缘附近的阴影可获得较弱联系帮助融合，但另一实例专属像素被清零，避免把局部编辑扩散过去。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:mice" data-paper-title="Editing Everything Everywhere All at Once" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Editing Everything Everywhere All at Once 多模态大模型 University of Modena and Reggio Emilia 2026-06-30 多区域同时编辑容易把一处指令的属性传到另一处。MICE 在联合注意力中隔离不同文字组，并用实例掩码的平滑空间偏置控制视觉交互，以兼顾局部绑定与周围区域融合。方法不训练新的编辑模型。 以单张 A100/A30 或 Mac 的资源限制评估，完整矩阵需要大权重、长时间生成和外部服务，标注成本过高，不复现（审查 DONE）。诊断使用 2 个生成掩码、6×8 raster 和随机 Q/K/V，真实执行 attention 与反向传播。实现 instance_aware_masks、instance_log_bias、mice_joint_bias、mice_joint_attention 和统一 diagnostic(seed, device)。模块导入不加载 PyTorch，实际调用时才需要。输入必须是已经在同一网格上的、非空、互不重叠的二值 mask；  视觉生成与编辑 多实例编辑与注意力隔离 多模态 世界建模：状态、生成与动作条件 为什么 ε=10^-30 的偏置至少用 float32，且 context 到视觉域不能随意加空间 mask？ float16 可能使极小 ε 下溢，改变有限 log 偏置的语义；softmax 与累加需至少 float32。本地采用正文 Case 5 的 context 到整个视觉域无偏置，不能混入示意图或默认 processor 的不同规则，再声称各版本完全等价。 例如区域外 log(ε) 本应是有限大负数，若下溢成零再取对数就变成负无穷，软衰减被意外改为硬禁止。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 世界建模：状态、生成与动作条件</a></p>
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

模型只描述观察，还是能判断动作怎样改变后续状态？

## 记住这一点

把观察、动作和后续状态放在一起，才能学习可用于预测或控制的表示。LeWAM 联合学习未来潜状态预测与动作 flow matching，让视觉表征和策略相互塑造；规划时再用潜动力学评价动作候选。WOVEN 则把视频生成的视觉转移组织成场景、动作、推理类型受控的监督，训练模型理解结果、原因与反事实。 SWIM补充“哪些状态坐标应影响latent距离”：离线逆动力学只门控未来位移，冻结gate后用sqrt(g)校准同帧对的状态距离；它不在规划时读取未来状态。SensorWM 将相同区分延伸到可穿戴序列：条件预测、候选排序与因果健康收益仍需要不同证据。

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
