---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 类型化读出：从生成句子到候选分布

[结构化决策](index.md) / 9 个问题 · 9 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">9 个问题 · 9 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:editjev" data-paper-title="EditJev: System One Routing for Image Editing Models" data-learning-pending="false" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/typed-readout" data-search="EditJev: System One Routing for Image Editing Models 基础模型 Peking University 2026-10-23 固定使用一个图像编辑器会忽视样本级互补性。EditJev先离线让所有候选产生输出并由judge评分，再将可靠质量差转为pairwise监督；router不生成模型名称，而直接输出固定候选顺序的utility vector。推理无需先运行各编辑器，仅对utility加beta倍固定速度分后选一次argmax。 成本过高，不复现（审查 DONE）。完整方案Qwen3-VL-4B LoRA router，五个编辑器FLUX.2 Klein4B/9B、Kontext、OmniGen2、Qwen-Image-Edit（20B），离线所有候选生成及Qwen3-VL-32B/GPT judge，737 ImgEdit+606 GEdit-En请求和多组消融。论文RTX PRO6000延迟计时不适合伪装成A100本地实测，不下载多套编辑权重或批量调API。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  System One / JEV 多模态模型路由 结构化决策 类型化读出：从生成句子到候选分布 EditJev离线要运行所有编辑器，为什么推理时却只运行被选中的一个？ 离线全候选生成与评审用于建立成对质量监督，让路由器学会按请求预测各编辑器效用。部署时效用加上固定速度偏好即可选一次，无需先看各编辑结果。候选顺序必须一致，速度权重表达取舍而非质量真值；完整多编辑器流程本地因成本过高未复现。 例如移除背景时先预测哪个编辑器更合适，再只调用它；若先把所有编辑器都跑完再选，就失去路由节约生成成本的目的。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 类型化读出：从生成句子到候选分布</a></p>
<span id="paper-foundation-models-editjev-bb39e611" class="ar-learning-paper-anchor"></span>
<h2 id="qa-4d16236f11c750b3">EditJev离线要运行所有编辑器，为什么推理时却只运行被选中的一个？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aeditjev">EditJev: System One Routing for Image Editing Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>离线全候选生成与评审用于建立成对质量监督，让路由器学会按请求预测各编辑器效用。部署时效用加上固定速度偏好即可选一次，无需先看各编辑结果。候选顺序必须一致，速度权重表达取舍而非质量真值；完整多编辑器流程本地因成本过高未复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如移除背景时先预测哪个编辑器更合适，再只调用它；若先把所有编辑器都跑完再选，就失去路由节约生成成本的目的。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32635v1">原论文</a> · <a href="../../../../foundation-models/2610.32635-editjev/">实现解读</a> · <a href="#qa-4d16236f11c750b3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:pathjev" data-paper-title="PathJev: Decision-Native Vision–Language Modelling for Histopathology" data-learning-pending="false" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/typed-readout" data-search="PathJev: Decision-Native Vision–Language Modelling for Histopathology 基础模型 University of Naples Federico II 2026-10-23 模型一遍前向在question/candidate markers读取hidden，decision head混合candidate线性项、question-candidate交互和set attention，对runtime候选做softmax。head和两阶段训练继承已有OmniMed-Jev；PathJev的重要新增是病理40K states、专家标签到三种typed decisions、split/overlap审计、未见器官与generative readout对照。 成本过高，不复现（审查 DONE）。MedGemma1.5-4B NF4、896×896图像、LoRA+head约39.6M参数、40Kstates；Table7单GPU每seed PathJev全程10.4–10.5h、Gen-SFT16.3–16.5h，另有超参选择/3seeds/多数据集推理、whole-slide。远超单卡短时预算，不下载公开权重来重复验证成本。无本地operator/metrics/GPUreceipt；原作者repo与分析计划可直接查阅。没有下载MedGemma、病理patch/whole-slide、没有用通用分类head或字段校验冒充完整病理方法。  System One / JEV 医疗多模态决策 结构化决策 类型化读出：从生成句子到候选分布 PathJev的重要贡献为什么不能缩成病理图像上接一个softmax？ 候选头结合候选线性项、问题交互及集合注意力，但这些结构继承已有模型；新增证据还依赖病理状态数据、类型化专家标签、重叠审计和未见器官对照。普通分类核只能覆盖小部分计算，不能证明病理泛化。本地完整训练因成本过高未复现，目标标签也不进入提示。 例如肿瘤等级作为运行时文字选项参与打分，训练采用原始等级标签；即使一个小softmax能算梯度，也不能代表跨器官识别已通过。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 类型化读出：从生成句子到候选分布</a></p>
<span id="paper-foundation-models-pathjev-38649f0d" class="ar-learning-paper-anchor"></span>
<h2 id="qa-2dc91c86955e14a5">PathJev的重要贡献为什么不能缩成病理图像上接一个softmax？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Apathjev">PathJev: Decision-Native Vision–Language Modelling for Histopathology</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Naples Federico II</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>候选头结合候选线性项、问题交互及集合注意力，但这些结构继承已有模型；新增证据还依赖病理状态数据、类型化专家标签、重叠审计和未见器官对照。普通分类核只能覆盖小部分计算，不能证明病理泛化。本地完整训练因成本过高未复现，目标标签也不进入提示。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如肿瘤等级作为运行时文字选项参与打分，训练采用原始等级标签；即使一个小softmax能算梯度，也不能代表跨器官识别已通过。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32478v1">原论文</a> · <a href="../../../../foundation-models/2610.32478-pathjev/">实现解读</a> · <a href="#qa-2dc91c86955e14a5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:system-one-rerank" data-paper-title="Multimodal Reranking Is a System One Decision" data-learning-pending="false" data-domain="multimodal-models" data-theme="system-one" data-topic="system-one/typed-readout" data-search="Multimodal Reranking Is a System One Decision 多模态大模型 Aalto University 2026-10-20 论文把重排视作一个选择决策：把 query 和首阶段候选放入同一多模态上下文，让通用视觉语言模型比较全部候选。它不生成排序文本，也不额外训练一个 pointwise reranker，而是在首个答案位置直接读取候选字母的概率。该读出继承 setwise / FIRST 的方法；论文的新论点与实验是通用 VLM 在图像、视觉文档上的零样本表现，以及纯文本 decision tuning 是否迁移到视觉重排。 全量实验决策为成本过高，不复现（审查 DONE），不下载、不试跑、不进入自动重试或实现队列；预训练小 VLM 的少样本执行属于 L1 读出机制诊断，不是27B论文结果，也不能证明它优于首阶段或监督 reranker。本地是可执行 choice-readout / 多模态输入组件，不是独立训练的“System One 模型”，没有复现 TypeSafe 未公开的 Jev 核心算法。ForwardVLMReranker 接收调用方已加载的可信 processor 和视觉语言模型，不下载权重、不调用生成 API，也不接受预先给定的候选分数：  多模态检索 JEV与System One决策 单次前向重排 结构化决策 类型化读出：从生成句子到候选分布 多模态System One重排为什么要同时报告候选内概率和标签在全词表中的质量？ 候选标签内归一化总能给出和为一的分布，即使模型原本几乎不愿输出任何合法标签。额外报告全词表标签质量，可以揭示低支持而非把相对选择误作绝对信心。所有标签需是当前分词器下不同的单词元，本地读出组件不是独立训练的System One模型。 例如合法字母总共只占很少词表质量，但其中A相对最高；可以据此排序，却不能直接宣称模型以同样高的绝对置信度认可A。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 类型化读出：从生成句子到候选分布</a></p>
<span id="paper-multimodal-models-system-one-rerank-459582b4" class="ar-learning-paper-anchor"></span>
<h2 id="qa-5c92ef210edd63d0">多模态System One重排为什么要同时报告候选内概率和标签在全词表中的质量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Asystem-one-rerank">Multimodal Reranking Is a System One Decision</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Aalto University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>候选标签内归一化总能给出和为一的分布，即使模型原本几乎不愿输出任何合法标签。额外报告全词表标签质量，可以揭示低支持而非把相对选择误作绝对信心。所有标签需是当前分词器下不同的单词元，本地读出组件不是独立训练的System One模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如合法字母总共只占很少词表质量，但其中A相对最高；可以据此排序，却不能直接宣称模型以同样高的绝对置信度认可A。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28435v1">原论文</a> · <a href="../../../../multimodal-models/2610.28435-system-one-rerank/">实现解读</a> · <a href="#qa-5c92ef210edd63d0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jev-portuguese-ir" data-paper-title="Jev-as-a-Judge for Brazilian Portuguese Information Retrieval: Relevance Assessment and Reranking" data-learning-pending="false" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/typed-readout" data-search="Jev-as-a-Judge for Brazilian Portuguese Information Retrieval: Relevance Assessment and Reranking 基础模型 Câmara dos Deputados 2026-10-16 检索中“给文档打离散相关性标签”和“给候选排序”并不是同一个任务。论文在四个巴西葡语检索集上，用 Choice 输出有序标签并比较人工/原始 qrels；另在 Quati 中把每个文档是否直接回答查询表示为独立 Noul 概率，收集全部批次再排序。候选不在单一 Choice 中竞争，也不与 BM25 分数混合，不训练校准模型。 成本过高，不复现（审查 DONE）。状态：低成本评测协议接口，不是 JEV 模型复现。本地只做离线合同验证和已发表混淆矩阵的算术复核，不调用商业 API、不生成新模型预测、不声称重现论文检索提升。此命令只运行构造协议样例。fixture provider 按公开 id 返回预设概率，不理解葡语、不称作 JEV。qrels 只传给独立评分函数，不进入模型请求。三种子只改变候选输入顺序，不表示三次模型能力实验；输出明确 real_backend_used=false、language_model_evaluated=false，不晋升 evolve。  System One / JEV 检索排序与评测协议 结构化决策 类型化读出：从生成句子到候选分布 JEV葡语检索为什么用每文档独立二元概率重排，而不把全部文档塞入同一Choice竞争？ 独立提问衡量各文档是否直接回答查询，收齐分数后才能跨批排序；同一Choice给出的则是候选内竞争份额，加入文档会改变分母。离散相关等级标注又是另一任务，需保留原标签顺序。该重排不混BM25分数，也没有训练校准模型，评测不能删掉零相关查询。 例如两篇文档都直接回答问题，可各自取得较高二元概率；在二选一分布里它们必须分享总概率，不能把两种数值当成同一含义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 类型化读出：从生成句子到候选分布</a></p>
<span id="paper-foundation-models-jev-portuguese-ir-ac19af30" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d635814939fe58b9">JEV葡语检索为什么用每文档独立二元概率重排，而不把全部文档塞入同一Choice竞争？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ajev-portuguese-ir">Jev-as-a-Judge for Brazilian Portuguese Information Retrieval: Relevance Assessment and Reranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Câmara dos Deputados</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立提问衡量各文档是否直接回答查询，收齐分数后才能跨批排序；同一Choice给出的则是候选内竞争份额，加入文档会改变分母。离散相关等级标注又是另一任务，需保留原标签顺序。该重排不混BM25分数，也没有训练校准模型，评测不能删掉零相关查询。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两篇文档都直接回答问题，可各自取得较高二元概率；在二选一分布里它们必须分享总概率，不能把两种数值当成同一含义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23346">原论文</a> · <a href="../../../../foundation-models/2610.23346-jev-portuguese-ir/">实现解读</a> · <a href="#qa-d635814939fe58b9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mjev-spatial" data-paper-title="MJev-Spatial: System One Spatial Intelligence via Native Attention Matching" data-learning-pending="false" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/typed-readout" data-search="MJev-Spatial: System One Spatial Intelligence via Native Attention Matching 基础模型 未注明（论文未列一作机构；公开发布主体为 MindLab） 2026-10-15 空间问题往往只需选项、数值或二维点，却仍让 VLM 自回归生成并解析答案。MJev-Spatial 将三者统一为候选分类：decision marker 提供 query，candidate-end marker 提供 key，直接复用骨干最终注意力投影。连续量通过分桶或三级区域细化预测，不增加独立分类头。 完整实验明显超过单卡预算，成本过高，不复现（审查 DONE）。随机分类标签只是梯度诊断，不是空间任务准确率。seeds42/43/44，固定程序化 revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1。随机16维因果 Transformer 产生候选/决策状态，最终层 Q/K、RMSNorm 和 headnorm 以同一模块对象注入读出器；不是加载或转换真实 Qwen checkpoint。  JEV与单步决策 原生注意力与空间候选 结构化决策 类型化读出：从生成句子到候选分布 MJev-Spatial为什么复用最终注意力的Q/K读候选，而不另接一个普通分类头？ 决策标记提供查询，候选结束标记提供键，利用骨干原生注意力投影形成候选分数；这使选项、分桶数值与区域选择共享一种读出方式。位置编码和分组查询映射不能随意省略。连续点还需逐级选区并从原图裁剪，候选分类本身不直接保证空间精度。 例如先从九个大区域选一个，再从原图裁出该区域继续细分；若总在上次缩放图上再裁剪，坐标和细节协议就改变了。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 类型化读出：从生成句子到候选分布</a></p>
<span id="paper-foundation-models-mjev-spatial-987f608c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-8616ff0ec0b4fbe8">MJev-Spatial为什么复用最终注意力的Q/K读候选，而不另接一个普通分类头？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amjev-spatial">MJev-Spatial: System One Spatial Intelligence via Native Attention Matching</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 未注明（论文未列一作机构；公开发布主体为 MindLab）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>决策标记提供查询，候选结束标记提供键，利用骨干原生注意力投影形成候选分数；这使选项、分桶数值与区域选择共享一种读出方式。位置编码和分组查询映射不能随意省略。连续点还需逐级选区并从原图裁剪，候选分类本身不直接保证空间精度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先从九个大区域选一个，再从原图裁出该区域继续细分；若总在上次缩放图上再裁剪，坐标和细节协议就改变了。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22276">原论文</a> · <a href="../../../../foundation-models/2610.22276-mjev-spatial/">实现解读</a> · <a href="#qa-8616ff0ec0b4fbe8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:metaencoder" data-paper-title="MetaEncoder: Exploring the Limit of Bi-Encoders for Multimodal System One Decision Making with Natural Language Interface" data-learning-pending="false" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/typed-readout" data-search="MetaEncoder: Exploring the Limit of Bi-Encoders for Multimodal System One Decision Making with Natural Language Interface 基础模型 Meta AI 2026-10-08 将Muse-Glimmer30B变为共享双塔，请求和候选均可含自然语言及图像/视频；保留因果注意力，取归一化末token向量。候选独立编码可缓存；闭集允许将选项加入请求，训练时部分dropout选项，防止仅依赖文字匹配。原文§3 成本过高，不复现（审查 DONE）；Google/Meta优先资料。成本过高，不复现（审查 DONE）；只整理原文与开源评测，不下载30B权重。官方评测README为30B BF16副本约62GB/卡，目标8张80GBGPU，数据含数百GB图像/视频。单卡可能装载不等于190任务便宜。成本过高，不复现（审查 DONE）；不下载、不试跑，不将随机向量余弦函数称MetaEncoder实现。无本地指标/GPU回执，无evolve晋级资格。  多模态基础模型 自然语言决策编码器 结构化决策 类型化读出：从生成句子到候选分布 MetaEncoder的候选可以缓存，为什么请求端加入选项仍不等于候选间全交互？ 共享双塔分别编码请求与候选，以归一化末词元向量做匹配，候选不依赖当前请求即可缓存。闭集请求可包含选项，但训练中部分丢弃它们，减少只靠文字匹配。候选塔仍是独立表示，复杂交叉推理能力受限；缓存条件也要求模型、提示和候选内容一致。 例如工具描述预先编码，用户请求临时编码后比较向量；工具定义改了就应更新缓存，不能把旧向量继续当作新工具的表示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 类型化读出：从生成句子到候选分布</a></p>
<span id="paper-foundation-models-metaencoder-e65c35d0" class="ar-learning-paper-anchor"></span>
<h2 id="qa-ec82c7d79648130a">MetaEncoder的候选可以缓存，为什么请求端加入选项仍不等于候选间全交互？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ametaencoder">MetaEncoder: Exploring the Limit of Bi-Encoders for Multimodal System One Decision Making with Natural Language Interface</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共享双塔分别编码请求与候选，以归一化末词元向量做匹配，候选不依赖当前请求即可缓存。闭集请求可包含选项，但训练中部分丢弃它们，减少只靠文字匹配。候选塔仍是独立表示，复杂交叉推理能力受限；缓存条件也要求模型、提示和候选内容一致。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如工具描述预先编码，用户请求临时编码后比较向量；工具定义改了就应更新缓存，不能把旧向量继续当作新工具的表示。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与原文效果；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11316">原论文</a> · <a href="../../../../foundation-models/2610.11316-metaencoder/">实现解读</a> · <a href="#qa-ec82c7d79648130a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:llm2jev" data-paper-title="LLM2Jev: LLMs Are Already Jev-Style Decision Models -- When and How to Fine-Tune Them" data-learning-pending="false" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/typed-readout" data-search="LLM2Jev: LLMs Are Already Jev-Style Decision Models -- When and How to Fine-Tune Them 基础模型 Microsoft（按作者邮箱） 2026-10-01 直接从括号数字选项的 next-token 概率形成有限类别分布；微调时使用 listwise 决策损失，并以 KL 锚定基础模型辅助输出。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行候选联合打分和 KL 锚定；未加载 4B checkpoint 或跑 JevBench。执行候选联合打分和 KL 锚定；未加载 4B checkpoint 或跑 JevBench。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Jev 决策模型 校准 结构化决策 类型化读出：从生成句子到候选分布 LLM2Jev为何要把选项字符串的联合概率归一化，而不能随便取最后一个token？ 有限选项可以由现有语言模型的词元概率构成决策分布，但多词元选项需要按完整条件链计算联合分数。微调再用列表决策损失，并以基础模型的辅助分布作KL锚点，限制偏移。标签长度和分词协议会影响读出，本地候选核未运行完整检查点评测。 例如选项标记被分成两个词元时，应计算两步条件概率的乘积；只取末尾那一片会遗漏前一片的可能性，产生不同排名。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 类型化读出：从生成句子到候选分布</a></p>
<span id="paper-foundation-models-llm2jev-33a9437e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-e4b3afe35eff8796">LLM2Jev为何要把选项字符串的联合概率归一化，而不能随便取最后一个token？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Allm2jev">LLM2Jev: LLMs Are Already Jev-Style Decision Models -- When and How to Fine-Tune Them</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft（按作者邮箱）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>有限选项可以由现有语言模型的词元概率构成决策分布，但多词元选项需要按完整条件链计算联合分数。微调再用列表决策损失，并以基础模型的辅助分布作KL锚点，限制偏移。标签长度和分词协议会影响读出，本地候选核未运行完整检查点评测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如选项标记被分成两个词元时，应计算两步条件概率的乘积；只取末尾那一片会遗漏前一片的可能性，产生不同排名。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02076">原论文</a> · <a href="../../../../foundation-models/2610.02076-llm2jev/">实现解读</a> · <a href="#qa-e4b3afe35eff8796">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:chinese-jev" data-paper-title="Chinese-Jev: Bringing System One Model to Chinese-Language Tasks" data-learning-pending="false" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/typed-readout" data-search="Chinese-Jev: Bringing System One Model to Chinese-Language Tasks 基础模型 Fudan University 2026-09-29 Chinese-Jev 面向分类、路由、候选选择等封闭输出任务，用轻量 encoder 读取中文上下文和候选项，以各候选 marker 的隐藏状态直接评分。异构标注统一成候选概率分布，先做 1000 万条通用预训练，再按医疗、法律、金融分别微调。 复现级别：L1 目标函数与模型头。复现级别：L1 目标函数与模型头。实现候选 marker 表示、候选概率监督与 RLCD 风格校准项；未训练论文 1000 万样本模型。ChineseJevHead 可前后向并验证概率归一化和有限梯度；没有论文数据、完整 backbone、移动端 INT8 部署或论文级性能对照。  System One / JEV 中文理解 高效决策模型 结构化决策 类型化读出：从生成句子到候选分布 Chinese-Jev为什么在候选marker上直接评分，而不是生成选项名称再解析？ 封闭输出任务需要的是候选之间的决策分布。编码器读取上下文与候选后，用对应标记的隐藏状态评分，再对候选归一化，可省去自由生成和格式解析。软标签还能保留标注中的概率信息；候选概率是集合内份额，不天然等于独立正确率，本地目标核也不代表通用预训练已复现。 例如把工单分到退款、物流或账户三类，模型直接输出三项分布；增加一个类别后份额会变化，不能把原退款概率当作固定置信度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 类型化读出：从生成句子到候选分布</a></p>
<span id="paper-foundation-models-chinese-jev-c9409f9e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-5ae535374df8fc78">Chinese-Jev为什么在候选marker上直接评分，而不是生成选项名称再解析？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Achinese-jev">Chinese-Jev: Bringing System One Model to Chinese-Language Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Fudan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>封闭输出任务需要的是候选之间的决策分布。编码器读取上下文与候选后，用对应标记的隐藏状态评分，再对候选归一化，可省去自由生成和格式解析。软标签还能保留标注中的概率信息；候选概率是集合内份额，不天然等于独立正确率，本地目标核也不代表通用预训练已复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把工单分到退款、物流或账户三类，模型直接输出三项分布；增加一个类别后份额会变化，不能把原退款概率当作固定置信度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36965">原论文</a> · <a href="../../../../foundation-models/2609.36965-chinese-jev/">实现解读</a> · <a href="#qa-5ae535374df8fc78">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gliclass" data-paper-title="GLiClass: Generalist Lightweight Model for Sequence Classification Tasks" data-learning-pending="false" data-domain="foundation-models" data-theme="system-one" data-topic="system-one/typed-readout" data-search="GLiClass: Generalist Lightweight Model for Sequence Classification Tasks 基础模型 Knowledgator 2025-08-11 GLiClass 把文本和运行时给定的候选标签放进同一个分类接口，避免生成式 LLM 的解析不稳定，也避免 cross-encoder 对每个文本—标签对逐次推理。本仓库保留“候选内容参与打分”和“一次归一化得到全候选分布”这两个定义性机制。本地实现是 NumPy 机制基线，不加载 GLiClass 权重，不宣称复现论文的完整 Transformer、PPO 多标签训练或论文数值。它用于 System One 的 Banking77 统一协议和 Evolve operator。 只复现动态候选交互与一次归一化机制，不复现 GLiClass 完整权重、训练语料或 PPO 流程。  动态候选分类 System One 相邻方法 结构化决策 类型化读出：从生成句子到候选分布 GLiClass运行时可以换候选标签，为什么不能退化成只看文本的固定分类器？ 候选内容参与评分，才可能在运行时改变标签集合；只对文本输出固定类别编号无法理解新增标签描述。候选交互后形成统一分布，也减少逐候选调用与生成解析开销。本地双线性或中心化打分只验证这两个机制，没有加载完整GLiClass权重或复刻训练。 例如同一句咨询在账户标签集合与信用卡标签集合中需要不同选择；新增标签要带语义描述，不能只给一个训练时没见过的编号。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 类型化读出：从生成句子到候选分布</a></p>
<span id="paper-foundation-models-gliclass-1a6b1ec2" class="ar-learning-paper-anchor"></span>
<h2 id="qa-96863e6767089111">GLiClass运行时可以换候选标签，为什么不能退化成只看文本的固定分类器？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agliclass">GLiClass: Generalist Lightweight Model for Sequence Classification Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Knowledgator</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>候选内容参与评分，才可能在运行时改变标签集合；只对文本输出固定类别编号无法理解新增标签描述。候选交互后形成统一分布，也减少逐候选调用与生成解析开销。本地双线性或中心化打分只验证这两个机制，没有加载完整GLiClass权重或复刻训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一句咨询在账户标签集合与信用卡标签集合中需要不同选择；新增标签要带语义描述，不能只给一个训练时没见过的编号。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.07662">原论文</a> · <a href="../../../../foundation-models/2508.07662-gliclass/">实现解读</a> · <a href="#qa-96863e6767089111">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

任务只需从候选中选择时，怎样让模型直接输出可用的决策？

## 记住这一点

先明确状态、问题和候选，再选择读出路径。LLM-as-Jev 从模型的选项读出形成有限候选分布，并研究冻结模型与带 KL 锚定的微调；MetaEncoder 把请求和候选独立编码，用相似度做闭集决策或开放检索。前者可以让模型联合看选项，后者能缓存独立候选表示，两者的交互能力与复用成本不同。

## 一个例子

工具路由只有“搜索、计算、拒答”三个动作时，直接返回概率比解析一段自由文本更容易约束。候选多达百万时，双塔可以预编码工具/条目再检索；但需要比较两个候选细节的复杂推理，未必能由一个独立相似度充分表达。

## 什么时候要小心

输出合法 schema 不保证选对，也不保证校准、独立性或任意候选数量下性能稳定。双塔缓存要求候选编码不依赖当前请求。本地 LLM-as-Jev 仅有机制诊断；MetaEncoder 因训练评估成本过高未复现，不能当成本地现成能力。

## 先读这几篇

先读 LLM-as-Jev 的有限候选读出，理解“输出分布而非长句”；再读 MetaEncoder 的共享双塔和独立候选缓存，比较联合选项交互与可检索性。两篇的本地能力状态仍以各自正文为准。

1. [LLM2Jev: LLMs Are Already Jev-Style Decision Models -- When and How to Fine-Tune Them](../../../foundation-models/2610.02076-llm2jev/README.md) · [原论文](https://arxiv.org/abs/2610.02076)
2. [MetaEncoder: Exploring the Limit of Bi-Encoders for Multimodal System One Decision Making with Natural Language Interface](../../../foundation-models/2610.11316-metaencoder/README.md) · [原论文](https://arxiv.org/abs/2610.11316)

## 自测一下

候选独立编码并缓存，是否意味着请求也无需重新编码？

??? note "展开参考答案"

    不是。候选可复用，但状态、问题或图像变化后仍要编码新请求，并计算或检索匹配。若把请求特有信息写进候选编码，原缓存也会失效；应按实际依赖关系划分复用边界。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
