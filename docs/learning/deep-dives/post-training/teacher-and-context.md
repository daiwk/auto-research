---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 教师更强仍可能教错：信息、兼容性与成功行为保护

[LLM 后训练](../index.md) · 更新 2026-11-12 · 52 篇主题资料 / 11 篇重点对照

教师的价值不只取决于总分。OPSD改变训练期可见信息，MOPD与逐token路由组织多教师，CSD先统一概率事件，SPOD保护学生已成功选择，VAD筛出可归于视觉证据的修正；这些约束要在模仿之前分别成立。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/post-training/teacher-and-context.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：教师来源：同参数特权视图或独立领域专家 · 组合粒度：按域、逐token路由、成功action保护 · 可比接口：同词表坐标或共同文本事件 · 信息归因：额外证据、语言先验与学生已会行为

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [OPSD](../../../post-training/2601.18734-opsd/README.md) · [原始来源](https://arxiv.org/abs/2601.18734)<br>章节：背景与主要改动、核心公式、复现边界 | 同一模型以两种条件分布充当师生，教师额外看已验证答案，学生自行生成无答案前缀。 | 额外信息仅限训练教师；本地候选双视图未复刻Qwen参数级训练。 |
| [MOPD](../../../post-training/2606.30406-mopd/README.md) · [原始来源](https://arxiv.org/abs/2606.30406)<br>章节：背景与主要改动、核心公式、复现边界 | 各域先独立训练RL教师，再在同一学生rollout上混合领域分布信号。 | 复用专家但共享学生仍可能出现域间干扰；本地确定性mini-suite不代表大模型能力融合。 |
| [Compatibility Matters: A Framework for Token-Level Teacher Selection in On-Policy Distillation](../../../post-training/2610.21234-token-teacher-selection/README.md) · [原始来源](https://arxiv.org/abs/2610.21234v1)<br>章节：背景与主要改动、核心公式、结果、代码映射与边界 | 每个学生前缀按置信、Hellinger距离或对齐特征距离选教师，软路由算术混合概率。 | 合适程度不等于教师更自信；异维特征不可直接相减。完整训练未复现，当前随机策略L1组件。 |
| [Beyond the Teacher: Understanding and Preserving Distillation Overshoot in Agentic On-Policy Distillation](../../../post-training/2610.25034-spod/README.md) · [原始来源](https://arxiv.org/abs/2610.25034v1)<br>章节：背景与主要改动、核心公式、结果、代码映射与边界 | 仅保护成功episode中教师原始完整action概率更低的decision，取消该处蒸馏并加软floor。 | 其余decision继续学，soft floor不保证共享参数下永不退化；完整Agent实验因成本未复现。 |
| [CSD: Common-Support Distillation for Cross-Tokenizer Knowledge Transfer](../../../post-training/2610.28895-csd/README.md) · [原始来源](https://arxiv.org/abs/2610.28895v1)<br>章节：背景与主要改动、核心公式、结果、代码映射与边界 | 先按字符区间与解码文本构造共同chunk事件，用链式概率及REST保留未匹配质量。 | 跨tokenizer不再假装同ID同含义，但事件覆盖受限；本地是不同小词表的对齐与梯度诊断。 |
| [VAD](../../../post-training/2607.28590-vad/README.md) · [原始来源](https://arxiv.org/abs/2607.28590)<br>章节：背景与主要改动、核心公式、复现边界 | 对比同一教师证据存在/移除视图，将原修正单侧投影到视觉方向后重建学生锚定目标。 | 操作性对比不证明所有修正皆真视觉因果；本地过程证据轴替代真实crop，未运行原视觉模型。 |
| [P²-MOPD: Accelerating Multi-Teacher On-Policy Distillation via Parameter Priors](../../../post-training/2611.03953-p2-mopd/README.md) · [原始来源](https://arxiv.org/abs/2611.03953v1)<br>章节：背景与主要改动、核心公式、结果、负控与边界 | 把冻结专家任务向量保留为可学习优化方向；自由学生权重与系数由同一更新前梯度共同推进，推理仍使用一个物化学生模型。 | 不只改变教师logit或合并初始点；未裁剪系数梯度、独立全局clip和零decay决定多步等价。完整MOPD模型/轨迹未复现，本地只验参数更新L1。 |
| [Stabilizing On-Policy Targeted Guidance in Agentic Reinforcement Learning](../../../post-training/2611.05266-targeted-guidance/README.md) · [原始来源](https://arxiv.org/abs/2611.05266v1)<br>章节：背景与主要改动、核心公式、结果、负控与边界 | 在失败Agent turn前加入文本反馈，以同权重反馈条件教师做完整词表reverse KL，并保留criterion的普通RL奖励。 | 只在失败处蒸馏，按整条响应token数归一；全部满足后恢复原RL。组件不提供实际judge、反馈有效性筛选或Agent轨迹，不能凭loss下降声称代码能力提高。 |
| [RAGCompass: Generalizable Retriever Routing via Reranking](../../../post-training/2611.05596-ragcompass/README.md) · [原始来源](https://arxiv.org/abs/2611.05596v1)<br>章节：核心公式、数据协议与代码映射 | RAGCompass 把每组检索证据交给同一个 reranker；将固定 reader 的离线答案 F1 软化为整组候选的监督分布，优化候选集 KL。 | 不需要检索器 ID 或相互不可比的置信度，但训练标签依赖固定 reader 与有参考答案的离线数据。推理只比较分数，不用真实 F1 或筛选 gap。 |
| [Bootstrapped On-Policy Distillation](../../../post-training/2611.13680-bopd/README.md) · [原始来源](https://arxiv.org/abs/2611.13680v1)<br>章节：背景与主要改动、核心公式、结果、负控与边界 | 先由reference-conditioned冻结M0构造中间M1，再冻结M1并移除reference，向从M0精确恢复、使用新optimizer的学生做teacher→student FKL。 | 不同于持续特权视图OPSD，reset的是学生与optimizer，教师则保留已学参数；本地仅真实FKL/handoff，不含LM rollout或原文未可审核的pointwise clipping。空作者仓库不记为已开源实现。 |
| [Which Successes Make Good References? Action-Sequence Alignment for Multi-Turn On-Policy Distillation](../../../post-training/2611.13135-lcs-reference-opd/README.md) · [原始来源](https://arxiv.org/abs/2611.13135v1)<br>章节：核心公式、数据协议与代码映射、结果、负控与边界 | 按同任务完整动作LCS选最兼容成功reference，free-target OT独立argmax且允许复用；只更新失败episode，无引用时reference-free，ALFWorld/tau3分别使用不同归一化。 | 不同于SPOD只在成功episode内保护teacher较不支持的action，这里整条成功轨迹不更新。LCS状态解释需要可恢复绕行，不是潜状态等价；本地没有Agent/OPD trainer，4500A100小时完整矩阵不复现。 |

</div>

## 取舍分析 {#analysis}

### 先确认教师信号说的是同一件事

MOPD和token路由都可能混合多个教师，但域级组合与逐位置选择并不相同。若师生tokenizer不同，CSD还要求先构建解码文本等价事件，不能直接混合同坐标概率。OPSD则未必换更大模型，它利用额外条件提高教师信息量；这与增加独立专家是另一轴。

对照来源：[mopd](../../../post-training/2606.30406-mopd/README.md) · [token-teacher-selection](../../../post-training/2610.21234-token-teacher-selection/README.md) · [csd](../../../post-training/2610.28895-csd/README.md) · [opsd](../../../post-training/2601.18734-opsd/README.md)

### 教师修正应被审查，而不是自动全部接纳

SPOD指出学生成功动作也可能不符合教师偏好，保护粒度是具体action而不是整段成功episode。VAD进一步区分特权教师的修正来自视觉证据还是共享语言偏差。这两种约束分别审查“学生已有成功”与“教师证据来源”，不能只看teacher总分更高就跳过。

对照来源：[spod](../../../post-training/2610.25034-spod/README.md) · [vad](../../../post-training/2607.28590-vad/README.md) · [opsd](../../../post-training/2601.18734-opsd/README.md)

### 教师既给logit，也能给参数方向，但两条证据不能互换

MOPD组织领域教师在学生轨迹上的监督；P²-MOPD进一步把专家bank的任务向量保留为连续可学习方向。教师选择回答谁给token反馈，参数先验则还改变权重空间怎样走。自由B允许离开任务向量空间，系数学习低维方向，导出仍是单学生。原文采用的支持受限MOPD surrogate、同一未裁剪梯度和双通道optimizer时序都有独立合同，旧候选混合接口不能直接冒充该完整训练。

对照来源：[p2-mopd](../../../post-training/2611.03953-p2-mopd/README.md) · [mopd](../../../post-training/2606.30406-mopd/README.md)

### 特权上下文应作用在哪里，与有没有teacher同样重要

OPSD区分学生可见问题与teacher私有参考；Targeted Guidance把特权信息换成失败turn前的文本反馈，并只在这些轮次施加辅助reverse KL，同时保留普通criterion RL。稀疏门控选择梯度位置，整条response-token归一控制每条rollout的总体尺度，两者不能混成删token后重算均值。无失败时严格退化原RL是数值合同，不代表反馈已经通过有效性筛选或代码任务真的提升。

对照来源：[targeted-guidance](../../../post-training/2611.05266-targeted-guidance/README.md) · [opsd](../../../post-training/2601.18734-opsd/README.md)

### 额外信息进入教师条件，还是只定义训练标签？

OPSD 把验证解交给同权重教师，在学生前缀上给词表分布；Targeted Guidance 只在失败轮次插入判定反馈，再加上普通 RL 奖励。RAGCompass 的参考答案只在候选证据产生答案后计算离线 F1 标签，监督轴是整个候选集合，不是 token。三者都要防止把训练期可见的额外信息带到推理。

对照来源：[ragcompass](../../../post-training/2611.05596-ragcompass/README.md) · [opsd](../../../post-training/2601.18734-opsd/README.md) · [targeted-guidance](../../../post-training/2611.05266-targeted-guidance/README.md)

### 先构造可无参考使用的教师，与始终依赖特权视图是不同路径

OPSD让教师额外读取验证解，学生只见自身前缀；BOPD先把这种监督写入中间参数，再让无参考中间教师指导从初始checkpoint恢复的新学生。它不是把Stage I末尾学生继续训练，也不能把Stage I特权分数缓存成Stage II无参考监督。权重冻结不意味着在新学生前缀上预测恒定，必须保留阶段、上下文与参数状态三条来源。

对照来源：[bopd](../../../post-training/2611.13680-bopd/README.md) · [opsd](../../../post-training/2601.18734-opsd/README.md)

### 保护成功episode与保护成功里的特定action，更新集合不一样

LCS reference方法先排除全部成功学生episode，再为失败者选同任务引用并校正；SPOD仍可训练成功episode，只对teacher完整action概率低于student的decision取消KL并加软floor。前者还改变reference信息来源，后者改变action级监督。不能把二者统称success mask后混用分母、概率条件和更新门控，且训练用成功reference都不应暴露给被评估学生。

对照来源：[lcs-reference-opd](../../../post-training/2611.13135-lcs-reference-opd/README.md) · [spod](../../../post-training/2610.25034-spod/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### OPSD师生权重相同，为什么不是让学生直接抄标准答案？ {#cross-same-weights-privileged-view}

??? note "展开答案与例子"

    **答案：** 两者条件不同：学生只读问题并生成自己的前缀，教师在训练时额外读已验证答案，再评分同一前缀。监督的是无特权条件下的学生分布。MOPD主要换独立领域教师，而非必须给学生额外上下文；无论哪种路径，都不能将训练参考答案接入正式学生预测输入。

    **教学例子：** 教学例子：教师知道解法来判断学生下一步，但学生生成时不能看到解法；给学生也加答案会变成另一种任务。

    对照来源：[opsd](../../../post-training/2601.18734-opsd/README.md) · [mopd](../../../post-training/2606.30406-mopd/README.md)

### 逐token教师路由能否直接平均不同tokenizer的同编号logits？ {#cross-mixture-events-before-probabilities}

??? note "展开答案与例子"

    **答案：** 不能。路由软混合的是相同事件上的概率，平均logits或logp通常是另一种组合；不同tokenizer还可能让同ID对应不同文本。CSD先做文本事件对齐，并保留REST质量，再比较分布。教师选择发生得再细，也不能代替概率事件具有共同含义。

    **教学例子：** 教学例子：编号17在一位教师是完整词，在学生是词片段，二者不能因编号相同就被相加当作一个候选。

    对照来源：[token-teacher-selection](../../../post-training/2610.21234-token-teacher-selection/README.md) · [csd](../../../post-training/2610.28895-csd/README.md) · [mopd](../../../post-training/2606.30406-mopd/README.md)

### 学生episode成功但教师不喜欢其中一个action，SPOD会停掉整段学习吗？ {#cross-success-not-whole-episode-freeze}

??? note "展开答案与例子"

    **答案：** 不会。SPOD依据成功位和完整action原始概率比较，只在符合条件的decision取消蒸馏并施加软floor，其他decision继续正常学。普通MOPD或OPSD并不自动拥有这一保护；教师偏好与已验证成功不一致时，需要明确决定如何保留已有行为。

    **教学例子：** 教学例子：三步任务里第二步虽不常见却有效，只保护第二步不代表第一、三步的教师修正也要全部丢弃。

    对照来源：[spod](../../../post-training/2610.25034-spod/README.md) · [mopd](../../../post-training/2606.30406-mopd/README.md) · [opsd](../../../post-training/2601.18734-opsd/README.md)

### 给OPSD教师更多视觉证据，就能确定它的全部修正都来自看图吗？ {#cross-privilege-not-visual-attribution}

??? note "展开答案与例子"

    **答案：** 不能。教师还可能改变语言先验、风格或继承错误前缀。VAD用同教师、同学生前缀的证据存在/移除对比构造视觉方向，并投影原修正；这是额外的归因设计，不是增加特权输入自动带来的性质，本地代理也不能冒充真实视觉归因能力。

    **教学例子：** 教学例子：换成证据crop后教师更爱简短措辞，简短偏好不必来自图像；需要对照视图区分共享变化。

    对照来源：[opsd](../../../post-training/2601.18734-opsd/README.md) · [vad](../../../post-training/2607.28590-vad/README.md)

### P²-MOPD学到一个更大的专家系数，是否等于MOPD提高了该教师的token混合权重？ {#cross-parameter-prior-not-teacher-mixture}

??? note "展开答案与例子"

    **答案：** 不等同。参数先验系数乘的是固定权重任务向量，改变学生参数空间的更新方向；教师路由或混合系数作用于输出监督分布。P²-MOPD仍要由领域教师给学生轨迹评分，不能用一个方向系数替代反馈分布，也不能把两类系数拿来直接解释同一种置信度。

    **教学例子：** 教学例：沿医疗专家参数方向把alpha从0.25改为0.3，不等于每个token的医疗教师概率都从25%混到30%；神经网络的参数到输出映射并不线性。

    对照来源：[p2-mopd](../../../post-training/2611.03953-p2-mopd/README.md) · [mopd](../../../post-training/2606.30406-mopd/README.md)

### OPSD和Targeted Guidance都有额外教师上下文，能统一为整条轨迹的teacher KL吗？ {#cross-feedback-mask-not-global-privilege}

??? note "展开答案与例子"

    **答案：** 不能抹掉门控与归约。Targeted Guidance只在criterion失败的Agent turn施加student到冻结teacher的完整词表KL，分母仍是整条响应有效token，并保留普通RL奖励；普通OPSD的特权参考不自动包含这些局部失败合同。额外信息只允许进入训练教师，不能交给正式学生作为未来错误提示。

    **教学例子：** 教学例：100个响应token中只有1个失败token且KL为2，辅助量按2/100计算；把其余99个token删掉后平均会变成2，也不再是原门控强度。

    对照来源：[targeted-guidance](../../../post-training/2611.05266-targeted-guidance/README.md) · [opsd](../../../post-training/2601.18734-opsd/README.md)

### 两个检索候选的离线 F1 很接近，能否在 RAGCompass 推理时沿用 0.05 门槛？它和 OPSD 的特权信息有什么不同？ {#cross-ragcompass-offline-gap}

??? note "展开答案与例子"

    **答案：** 不能。门槛只用于筛选有参考答案的离线样本；推理用 reranker 或比较头的得分。OPSD 的特权解进入教师输入，改变词表预测；RAGCompass 的参考答案只定义候选标签，不输入候选 scorer。

    **教学例子：** 离线 F1 是 0.50 和 0.48 时，该样本不满足筛选门槛。部署时如果两个 scorer 分数是 0.2 和 0.7，仍选第二个；不能查真值 F1 重新筛选。

    对照来源：[ragcompass](../../../post-training/2611.05596-ragcompass/README.md) · [opsd](../../../post-training/2601.18734-opsd/README.md)

### 把OPSD的teacher去掉reference，再继续原学生，等于BOPD吗？ {#cross-cross-bootstrap-teacher-versus-privileged-view}

??? note "展开答案与例子"

    **答案：** 不等于。BOPD的Stage II教师来自Stage I学得的中间模型，而学生精确恢复初始模型并新建optimizer；去reference只是其中一条条件变化。继续原学生或换回初始teacher都改变了方法。

    **教学例子：** 教学例：Stage I把权重1学到1.2。Stage II teacher用1.2、student用1、optimizer空状态；两者都用1.2只是继续训练，不是该handoff。

    对照来源：[bopd](../../../post-training/2611.13680-bopd/README.md) · [opsd](../../../post-training/2601.18734-opsd/README.md)

### LCS failure-only和SPOD都保护成功，为什么不能复用同一个success mask？ {#cross-cross-whole-success-versus-action-protection}

??? note "展开答案与例子"

    **答案：** LCS跳过整个成功episode；SPOD还比较teacher/student的完整action概率，只保护满足条件的decision，其他位置继续蒸馏。因此mask粒度、归约和保留的loss都不同。

    **教学例子：** 教学例：一条成功episode中teacher对某动作比student更支持，SPOD可继续该动作KL；LCS方法仍跳过整条成功轨迹。

    对照来源：[lcs-reference-opd](../../../post-training/2611.13135-lcs-reference-opd/README.md) · [spod](../../../post-training/2610.25034-spod/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-11-12** · 补审LCS同任务引用选择，区分整episode失败过滤与SPOD完整action保护；保留free-target独立选择、双normalizer和teacher-only reference。仅CPU选择核，不用fixture冒充多轮Agent训练。

涉及：[lcs-reference-opd](../../../post-training/2611.13135-lcs-reference-opd/README.md)

**2026-11-12** · 补审BOPD，区分持续特权视图与两阶段无参考教师迁移，保留学生/optimizer重置及逐轨迹FKL；本地A100只验收loss/handoff，完整多GPU与长生成实验不复现。

涉及：[bopd](../../../post-training/2611.13680-bopd/README.md)

**2026-11-06** · 加入 RAGCompass 候选证据效用蒸馏，与 OPSD 和 Targeted Guidance 对读监督轴、反馈入口及离线筛选与部署分界。

涉及：[ragcompass](../../../post-training/2611.05596-ragcompass/README.md) · [opsd](../../../post-training/2601.18734-opsd/README.md) · [targeted-guidance](../../../post-training/2611.05266-targeted-guidance/README.md)

**2026-11-05** · 补入P²-MOPD参数先验双通道和Targeted Guidance失败turn反馈；对照MOPD教师监督与OPSD特权上下文，保留独立更新方向、原分母及完整实验高成本未复现边界。

涉及：[p2-mopd](../../../post-training/2611.03953-p2-mopd/README.md) · [targeted-guidance](../../../post-training/2611.05266-targeted-guidance/README.md) · [mopd](../../../post-training/2606.30406-mopd/README.md) · [opsd](../../../post-training/2601.18734-opsd/README.md)

**2026-10-27** · 首版：比较特权自教师、多领域与逐token路由、CSD文本事件对齐、SPOD成功保护和VAD视觉归因；已阅47篇摘要，精读6篇。

覆盖 47 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 52 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [P²-MOPD: Accelerating Multi-Teacher On-Policy Distillation via Parameter Priors](../../../post-training/2611.03953-p2-mopd/README.md)
- [Stabilizing On-Policy Targeted Guidance in Agentic Reinforcement Learning](../../../post-training/2611.05266-targeted-guidance/README.md)
- [When to Follow the Teacher: Advantage-Based On-Policy Distillation](../../../post-training/2610.31563-aopd/README.md)
- [Edit, Don&#x27;t Imitate: Minimal-Edit On-Policy Distillation for Multimodal Reasoning](../../../post-training/2610.30231-minimal-edit-opd/README.md)
- [CSD: Common-Support Distillation for Cross-Tokenizer Knowledge Transfer](../../../post-training/2610.28895-csd/README.md)
- [Reinforcement Learning with Visually Attributable On-Policy Self-Distillation](../../../post-training/2610.26856-vag/README.md)
- [Correctness-Dependent Asymmetric Target Distributions for Self-Distillation Policy Optimization](../../../post-training/2610.25973-apsd/README.md)
- [Beyond the Teacher: Understanding and Preserving Distillation Overshoot in Agentic On-Policy Distillation](../../../post-training/2610.25034-spod/README.md)
- [Tree-Aware Posterior Distillation for Long-Horizon Agentic Reinforcement Learning](../../../post-training/2610.23181-treeopsd/README.md)
- [MultiAgent-OPD: End-to-End Training of Hierarchical Multi-Agent Systems with On-Policy Distillation](../../../post-training/2610.23234-multiagent-opd/README.md)
- [Waypoint-OPD: Transferring RL-Induced Policy Shifts via Gated On-Policy Distillation](../../../post-training/2610.21601-waypoint-opd/README.md)
- [Compatibility Matters: A Framework for Token-Level Teacher Selection in On-Policy Distillation](../../../post-training/2610.21234-token-teacher-selection/README.md)
- [Training-Free On-Policy Distillation](../../../post-training/2610.22236-tf-opd/README.md)
- [Learning from Unverified Peers via Shared Residual Distillation](../../../post-training/2610.22080-shared-residual-distillation/README.md)
- [OPRD: On-Policy Reminder Distillation for Long-Horizon Coding Agents](../../../post-training/2610.21496-oprd-reminder/README.md)
- [EliteReplay: Preserving Diverse Solutions in RL Post-Training via Quality-Diversity Search](../../../post-training/2610.22290-elite-replay/README.md)
- [Condition-Contrastive Extrapolation for On-Policy Distillation of Language Models](../../../post-training/2610.21195-cce-opd/README.md)
- [Failure Is the Mother of Success: Recovering Supervision with Grounding Hindsight](../../../post-training/2610.21018-rshd/README.md)
- [LoOPSD: On-Policy Self-Distillation with Looped Teachers](../../../reproductions/2610.18162-loopsd/README.md)
- [Beyond Domain-Routed Supervision: Cross-Teacher Guarding for Multi-Teacher On-Policy Distillation](../../../reproductions/2610.13521-road-mopd/README.md)
- [CAST: Credit Alignment for Cross-Tokenizer On-Policy Distillation](../../../reproductions/2610.13257-cast-opd/README.md)
- [Which Skill to Distill? SGUID: Selecting a Compact Skill Bank for Model–Skill Co-Evolution](../../../post-training/2610.12367-sguid/README.md)
- [MetaOPD: Meta-Learned Token Weighting for On-Policy Distillation](../../../post-training/2610.11989-meta-opd/README.md)
- [Where-OPD: Spatially Guided On-Policy Self-Distillation of MLLMs with Synthetic Scenes](../../../post-training/2610.02117-where-opd/README.md)
- [The Weakest Link: Distilling LLM Reasoning with Worst-Case Constrained Reinforcement Learning](../../../post-training/2610.00332-weakest-link/README.md)
- [PR-OPD: Privileged Representation On-policy Self-Distillation for Agentic Reinforcement Learning](../../../post-training/2609.36642-pr-opd/README.md)
- [From Dissonance to Orchestration: Teacher Intervention in On-Policy Distillation](../../../post-training/2609.37510-maestro/README.md)
- [LEGO-OPD: Factorized Teacher Composition for Multimodal On-Policy Distillation](../../../post-training/2610.00333-lego-opd/README.md)
- [AdviSD: Learning to Advise Frontier LLMs via Targeted Multi-Turn Self-Distillation](../../../post-training/2609.38142-advisd/README.md)
- [Learning from Teacher Continuations at Student States](../../../post-training/2609.36246-olive/README.md)
- [MAS-OPD: On-Policy Distillation for Multi-Agent Systems](../../../post-training/2609.34234-mas-opd/README.md)
- [OPD-Aha: From Linguistic Momentum to Visual Reflection in Multimodal On-Policy Distillation](../../../post-training/2609.16459-opd-aha/README.md)
- [Negative Self-Distillation: Learning to Reason by Avoiding Flaws](../../../post-training/2609.11699-nsd/README.md)
- [CompassOPD: Cross-Family On-Policy Distillation via Within-Family Likelihood Shifts](../../../post-training/2609.10154-compass-opd/README.md)
- [Eliciting Weak-to-Strong Generalization with On-Policy Reverse Distillation](../../../post-training/2609.08798-oprd/README.md)
- [Boosting LLM Exploration via Weak-Model Guidance in RLVR](../../../post-training/2608.27420-weak-guide-rlvr/README.md)
- [Video-OPSD: Exploiting Privileged Visual Evidence for On-Policy Self-Distillation in Video Large Language Models](../../../post-training/2608.27065-video-opsd/README.md)
- [Preserving General Capabilities during Domain Specialization with Uncertainty-Calibrated MOPD](../../../post-training/2608.26735-uc-mopd/README.md)
- [Where to Look Matters: On-Policy Self-Distillation for Long-Video Understanding](../../../post-training/2608.25356-clue-opsd/README.md)
- [SMOPD: Multi-Reward Reinforcement Learning via Specialize-and-Merge Online Policy Distillation](../../../post-training/2608.03092-smopd/README.md)
- [Distill Where You Fail: Recovering Learning Signals of Negative RL-Groups from Adaptive Teacher Guidance](../../../post-training/2608.00782-rstg/README.md)
- [VAD](../../../post-training/2607.28590-vad/README.md)
- [Contrastive Reinforced Policy Optimization via Privileged Self-Distillation](../../../post-training/2607.28026-crpo/README.md)
- [Distilled RL](../../../post-training/2607.17247-distilled-rl/README.md)
- [ARMOR](../../../post-training/2607.10481-armor/README.md)
- [MOPD](../../../post-training/2606.30406-mopd/README.md)
- [POLARIS: Guiding Small Models to Write Long Stories](../../../post-training/2606.04095-polaris-hri/README.md)
- [OPCD](../../../post-training/2602.12275-opcd/README.md)
- [OPSD](../../../post-training/2601.18734-opsd/README.md)
- [RAGCompass: Generalizable Retriever Routing via Reranking](../../../post-training/2611.05596-ragcompass/README.md)
- [Bootstrapped On-Policy Distillation](../../../post-training/2611.13680-bopd/README.md)
- [Which Successes Make Good References? Action-Sequence Alignment for Multi-Turn On-Policy Distillation](../../../post-training/2611.13135-lcs-reference-opd/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/post-training/teacher-and-context.md) · [返回全部精读卡片](../index.md)
