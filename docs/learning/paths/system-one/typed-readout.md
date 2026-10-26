---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 类型化读出：从生成句子到候选分布

[结构化决策](index.md) / 子主题导学 · 约 3 分钟 · 9 张论文卡

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

## 这个子主题的论文卡片

导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">
<div class="ar-learning-controls">
<label for="learning-search">搜索卡片
<input id="learning-search" type="search" data-learning-search placeholder="搜索论文、机制、机构或本地边界"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">共 9 张卡片</p>
<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="system-one" data-topic="system-one/typed-readout" data-search="EditJev: System One Routing for Image Editing Models 基础模型 Peking University 2026-10-23 固定使用一个图像编辑器会忽视样本级互补性。EditJev先离线让所有候选产生输出并由judge评分，再将可靠质量差转为pairwise监督；router不生成模型名称，而直接输出固定候选顺序的utility vector。推理无需先运行各编辑器，仅对utility加beta倍固定速度分后选一次argmax。 成本过高，不复现（审查 DONE）。完整方案Qwen3-VL-4B LoRA router，五个编辑器FLUX.2 Klein4B/9B、Kontext、OmniGen2、Qwen-Image-Edit（20B），离线所有候选生成及Qwen3-VL-32B/GPT judge，737 ImgEdit+606 GEdit-En请求和多组消融。论文RTX PRO6000延迟计时不适合伪装成A100本地实测，不下载多套编辑权重或批量调API。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  System One / JEV 多模态模型路由 结构化决策 类型化读出：从生成句子到候选分布">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 类型化读出：从生成句子到候选分布</a></p>
<h2 id="paper-foundation-models-editjev-bb39e611">EditJev: System One Routing for Image Editing Models</h2>
<p class="ar-learning-card__meta">Peking University · 论文公开：2026-10-23</p>
<p><strong>方法要点：</strong>固定使用一个图像编辑器会忽视样本级互补性。EditJev先离线让所有候选产生输出并由judge评分，再将可靠质量差转为pairwise监督；router不生成模型名称，而直接输出固定候选顺序的utility vector。推理无需先运行各编辑器，仅对utility加beta倍固定速度分后选一次argmax。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。完整方案Qwen3-VL-4B LoRA router，五个编辑器FLUX.2 Klein4B/9B、Kontext、OmniGen2、Qwen-Image-Edit（20B），离线所有候选生成及Qwen3-VL-32B/GPT judge，737 ImgEdit+606 GEdit-En请求和多组消融。论文RTX PRO6000延迟计时不适合伪装成A100本地实测，不下载多套编辑权重或批量调API。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32635v1">原论文</a> · <a href="../../../../foundation-models/2610.32635-editjev/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="system-one" data-topic="system-one/typed-readout" data-search="PathJev: Decision-Native Vision–Language Modelling for Histopathology 基础模型 University of Naples Federico II 2026-10-23 模型一遍前向在question/candidate markers读取hidden，decision head混合candidate线性项、question-candidate交互和set attention，对runtime候选做softmax。head和两阶段训练继承已有OmniMed-Jev；PathJev的重要新增是病理40K states、专家标签到三种typed decisions、split/overlap审计、未见器官与generative readout对照。 成本过高，不复现（审查 DONE）。MedGemma1.5-4B NF4、896×896图像、LoRA+head约39.6M参数、40Kstates；Table7单GPU每seed PathJev全程10.4–10.5h、Gen-SFT16.3–16.5h，另有超参选择/3seeds/多数据集推理、whole-slide。远超单卡短时预算，不下载公开权重来重复验证成本。无本地operator/metrics/GPUreceipt；原作者repo与分析计划可直接查阅。没有下载MedGemma、病理patch/whole-slide、没有用通用分类head或字段校验冒充完整病理方法。  System One / JEV 医疗多模态决策 结构化决策 类型化读出：从生成句子到候选分布">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 类型化读出：从生成句子到候选分布</a></p>
<h2 id="paper-foundation-models-pathjev-38649f0d">PathJev: Decision-Native Vision–Language Modelling for Histopathology</h2>
<p class="ar-learning-card__meta">University of Naples Federico II · 论文公开：2026-10-23</p>
<p><strong>方法要点：</strong>模型一遍前向在question/candidate markers读取hidden，decision head混合candidate线性项、question-candidate交互和set attention，对runtime候选做softmax。head和两阶段训练继承已有OmniMed-Jev；PathJev的重要新增是病理40K states、专家标签到三种typed decisions、split/overlap审计、未见器官与generative readout对照。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。MedGemma1.5-4B NF4、896×896图像、LoRA+head约39.6M参数、40Kstates；Table7单GPU每seed PathJev全程10.4–10.5h、Gen-SFT16.3–16.5h，另有超参选择/3seeds/多数据集推理、whole-slide。远超单卡短时预算，不下载公开权重来重复验证成本。无本地operator/metrics/GPUreceipt；原作者repo与分析计划可直接查阅。没有下载MedGemma、病理patch/whole-slide、没有用通用分类head或字段校验冒充完整病理方法。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32478v1">原论文</a> · <a href="../../../../foundation-models/2610.32478-pathjev/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="multimodal-models" data-theme="system-one" data-topic="system-one/typed-readout" data-search="Multimodal Reranking Is a System One Decision 多模态大模型 Aalto University 2026-10-20 论文把重排视作一个选择决策：把 query 和首阶段候选放入同一多模态上下文，让通用视觉语言模型比较全部候选。它不生成排序文本，也不额外训练一个 pointwise reranker，而是在首个答案位置直接读取候选字母的概率。该读出继承 setwise / FIRST 的方法；论文的新论点与实验是通用 VLM 在图像、视觉文档上的零样本表现，以及纯文本 decision tuning 是否迁移到视觉重排。 全量实验决策为成本过高，不复现（审查 DONE），不下载、不试跑、不进入自动重试或实现队列；预训练小 VLM 的少样本执行属于 L1 读出机制诊断，不是27B论文结果，也不能证明它优于首阶段或监督 reranker。本地是可执行 choice-readout / 多模态输入组件，不是独立训练的“System One 模型”，没有复现 TypeSafe 未公开的 Jev 核心算法。ForwardVLMReranker 接收调用方已加载的可信 processor 和视觉语言模型，不下载权重、不调用生成 API，也不接受预先给定的候选分数：  多模态检索 JEV与System One决策 单次前向重排 结构化决策 类型化读出：从生成句子到候选分布">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 类型化读出：从生成句子到候选分布</a></p>
<h2 id="paper-multimodal-models-system-one-rerank-459582b4">Multimodal Reranking Is a System One Decision</h2>
<p class="ar-learning-card__meta">Aalto University · 论文公开：2026-10-20</p>
<p><strong>方法要点：</strong>论文把重排视作一个选择决策：把 query 和首阶段候选放入同一多模态上下文，让通用视觉语言模型比较全部候选。它不生成排序文本，也不额外训练一个 pointwise reranker，而是在首个答案位置直接读取候选字母的概率。该读出继承 setwise / FIRST 的方法；论文的新论点与实验是通用 VLM 在图像、视觉文档上的零样本表现，以及纯文本 decision tuning 是否迁移到视觉重排。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>全量实验决策为成本过高，不复现（审查 DONE），不下载、不试跑、不进入自动重试或实现队列；预训练小 VLM 的少样本执行属于 L1 读出机制诊断，不是27B论文结果，也不能证明它优于首阶段或监督 reranker。本地是可执行 choice-readout / 多模态输入组件，不是独立训练的“System One 模型”，没有复现 TypeSafe 未公开的 Jev 核心算法。ForwardVLMReranker 接收调用方已加载的可信 processor 和视觉语言模型，不下载权重、不调用生成 API，也不接受预先给定的候选分数：</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28435v1">原论文</a> · <a href="../../../../multimodal-models/2610.28435-system-one-rerank/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="system-one" data-topic="system-one/typed-readout" data-search="Jev-as-a-Judge for Brazilian Portuguese Information Retrieval: Relevance Assessment and Reranking 基础模型 Câmara dos Deputados 2026-10-16 检索中“给文档打离散相关性标签”和“给候选排序”并不是同一个任务。论文在四个巴西葡语检索集上，用 Choice 输出有序标签并比较人工/原始 qrels；另在 Quati 中把每个文档是否直接回答查询表示为独立 Noul 概率，收集全部批次再排序。候选不在单一 Choice 中竞争，也不与 BM25 分数混合，不训练校准模型。 成本过高，不复现（审查 DONE）。状态：低成本评测协议接口，不是 JEV 模型复现。本地只做离线合同验证和已发表混淆矩阵的算术复核，不调用商业 API、不生成新模型预测、不声称重现论文检索提升。此命令只运行构造协议样例。fixture provider 按公开 id 返回预设概率，不理解葡语、不称作 JEV。qrels 只传给独立评分函数，不进入模型请求。三种子只改变候选输入顺序，不表示三次模型能力实验；输出明确 real_backend_used=false、language_model_evaluated=false，不晋升 evolve。  System One / JEV 检索排序与评测协议 结构化决策 类型化读出：从生成句子到候选分布">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 类型化读出：从生成句子到候选分布</a></p>
<h2 id="paper-foundation-models-jev-portuguese-ir-ac19af30">Jev-as-a-Judge for Brazilian Portuguese Information Retrieval: Relevance Assessment and Reranking</h2>
<p class="ar-learning-card__meta">Câmara dos Deputados · 论文公开：2026-10-16</p>
<p><strong>方法要点：</strong>检索中“给文档打离散相关性标签”和“给候选排序”并不是同一个任务。论文在四个巴西葡语检索集上，用 Choice 输出有序标签并比较人工/原始 qrels；另在 Quati 中把每个文档是否直接回答查询表示为独立 Noul 概率，收集全部批次再排序。候选不在单一 Choice 中竞争，也不与 BM25 分数混合，不训练校准模型。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。状态：低成本评测协议接口，不是 JEV 模型复现。本地只做离线合同验证和已发表混淆矩阵的算术复核，不调用商业 API、不生成新模型预测、不声称重现论文检索提升。此命令只运行构造协议样例。fixture provider 按公开 id 返回预设概率，不理解葡语、不称作 JEV。qrels 只传给独立评分函数，不进入模型请求。三种子只改变候选输入顺序，不表示三次模型能力实验；输出明确 real_backend_used=false、language_model_evaluated=false，不晋升 evolve。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23346">原论文</a> · <a href="../../../../foundation-models/2610.23346-jev-portuguese-ir/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="system-one" data-topic="system-one/typed-readout" data-search="MJev-Spatial: System One Spatial Intelligence via Native Attention Matching 基础模型 未注明（论文未列一作机构；公开发布主体为 MindLab） 2026-10-15 空间问题往往只需选项、数值或二维点，却仍让 VLM 自回归生成并解析答案。MJev-Spatial 将三者统一为候选分类：decision marker 提供 query，candidate-end marker 提供 key，直接复用骨干最终注意力投影。连续量通过分桶或三级区域细化预测，不增加独立分类头。 完整实验明显超过单卡预算，成本过高，不复现（审查 DONE）。随机分类标签只是梯度诊断，不是空间任务准确率。seeds42/43/44，固定程序化 revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1。随机16维因果 Transformer 产生候选/决策状态，最终层 Q/K、RMSNorm 和 headnorm 以同一模块对象注入读出器；不是加载或转换真实 Qwen checkpoint。  JEV与单步决策 原生注意力与空间候选 结构化决策 类型化读出：从生成句子到候选分布">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 类型化读出：从生成句子到候选分布</a></p>
<h2 id="paper-foundation-models-mjev-spatial-987f608c">MJev-Spatial: System One Spatial Intelligence via Native Attention Matching</h2>
<p class="ar-learning-card__meta">未注明（论文未列一作机构；公开发布主体为 MindLab） · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>空间问题往往只需选项、数值或二维点，却仍让 VLM 自回归生成并解析答案。MJev-Spatial 将三者统一为候选分类：decision marker 提供 query，candidate-end marker 提供 key，直接复用骨干最终注意力投影。连续量通过分桶或三级区域细化预测，不增加独立分类头。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验明显超过单卡预算，成本过高，不复现（审查 DONE）。随机分类标签只是梯度诊断，不是空间任务准确率。seeds42/43/44，固定程序化 revision synthetic-memory-spatial-vision-recurrence-and-ode@oct18-foundation-mechanisms-v1。随机16维因果 Transformer 产生候选/决策状态，最终层 Q/K、RMSNorm 和 headnorm 以同一模块对象注入读出器；不是加载或转换真实 Qwen checkpoint。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22276">原论文</a> · <a href="../../../../foundation-models/2610.22276-mjev-spatial/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="system-one" data-topic="system-one/typed-readout" data-search="MetaEncoder: Exploring the Limit of Bi-Encoders for Multimodal System One Decision Making with Natural Language Interface 基础模型 Meta AI 2026-10-08 将Muse-Glimmer30B变为共享双塔，请求和候选均可含自然语言及图像/视频；保留因果注意力，取归一化末token向量。候选独立编码可缓存；闭集允许将选项加入请求，训练时部分dropout选项，防止仅依赖文字匹配。原文§3 成本过高，不复现（审查 DONE）；Google/Meta优先资料。成本过高，不复现（审查 DONE）；只整理原文与开源评测，不下载30B权重。官方评测README为30B BF16副本约62GB/卡，目标8张80GBGPU，数据含数百GB图像/视频。单卡可能装载不等于190任务便宜。成本过高，不复现（审查 DONE）；不下载、不试跑，不将随机向量余弦函数称MetaEncoder实现。无本地指标/GPU回执，无evolve晋级资格。  多模态基础模型 自然语言决策编码器 结构化决策 类型化读出：从生成句子到候选分布">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 类型化读出：从生成句子到候选分布</a></p>
<h2 id="paper-foundation-models-metaencoder-e65c35d0">MetaEncoder: Exploring the Limit of Bi-Encoders for Multimodal System One Decision Making with Natural Language Interface</h2>
<p class="ar-learning-card__meta">Meta AI · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>将Muse-Glimmer30B变为共享双塔，请求和候选均可含自然语言及图像/视频；保留因果注意力，取归一化末token向量。候选独立编码可缓存；闭集允许将选项加入请求，训练时部分dropout选项，防止仅依赖文字匹配。原文§3</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）；Google/Meta优先资料。成本过高，不复现（审查 DONE）；只整理原文与开源评测，不下载30B权重。官方评测README为30B BF16副本约62GB/卡，目标8张80GBGPU，数据含数百GB图像/视频。单卡可能装载不等于190任务便宜。成本过高，不复现（审查 DONE）；不下载、不试跑，不将随机向量余弦函数称MetaEncoder实现。无本地指标/GPU回执，无evolve晋级资格。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11316">原论文</a> · <a href="../../../../foundation-models/2610.11316-metaencoder/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="system-one" data-topic="system-one/typed-readout" data-search="LLM2Jev: LLMs Are Already Jev-Style Decision Models -- When and How to Fine-Tune Them 基础模型 Microsoft（按作者邮箱） 2026-10-01 直接从括号数字选项的 next-token 概率形成有限类别分布；微调时使用 listwise 决策损失，并以 KL 锚定基础模型辅助输出。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行候选联合打分和 KL 锚定；未加载 4B checkpoint 或跑 JevBench。执行候选联合打分和 KL 锚定；未加载 4B checkpoint 或跑 JevBench。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Jev 决策模型 校准 结构化决策 类型化读出：从生成句子到候选分布">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 类型化读出：从生成句子到候选分布</a></p>
<h2 id="paper-foundation-models-llm2jev-33a9437e">LLM2Jev: LLMs Are Already Jev-Style Decision Models -- When and How to Fine-Tune Them</h2>
<p class="ar-learning-card__meta">Microsoft（按作者邮箱） · 论文公开：2026-10-01</p>
<p><strong>方法要点：</strong>直接从括号数字选项的 next-token 概率形成有限类别分布；微调时使用 listwise 决策损失，并以 KL 锚定基础模型辅助输出。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行候选联合打分和 KL 锚定；未加载 4B checkpoint 或跑 JevBench。执行候选联合打分和 KL 锚定；未加载 4B checkpoint 或跑 JevBench。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02076">原论文</a> · <a href="../../../../foundation-models/2610.02076-llm2jev/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="system-one" data-topic="system-one/typed-readout" data-search="Chinese-Jev: Bringing System One Model to Chinese-Language Tasks 基础模型 Fudan University 2026-09-29 Chinese-Jev 面向分类、路由、候选选择等封闭输出任务，用轻量 encoder 读取中文上下文和候选项，以各候选 marker 的隐藏状态直接评分。异构标注统一成候选概率分布，先做 1000 万条通用预训练，再按医疗、法律、金融分别微调。 复现级别：L1 目标函数与模型头。复现级别：L1 目标函数与模型头。实现候选 marker 表示、候选概率监督与 RLCD 风格校准项；未训练论文 1000 万样本模型。ChineseJevHead 可前后向并验证概率归一化和有限梯度；没有论文数据、完整 backbone、移动端 INT8 部署或论文级性能对照。  System One / JEV 中文理解 高效决策模型 结构化决策 类型化读出：从生成句子到候选分布">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 类型化读出：从生成句子到候选分布</a></p>
<h2 id="paper-foundation-models-chinese-jev-c9409f9e">Chinese-Jev: Bringing System One Model to Chinese-Language Tasks</h2>
<p class="ar-learning-card__meta">Fudan University · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>Chinese-Jev 面向分类、路由、候选选择等封闭输出任务，用轻量 encoder 读取中文上下文和候选项，以各候选 marker 的隐藏状态直接评分。异构标注统一成候选概率分布，先做 1000 万条通用预训练，再按医疗、法律、金融分别微调。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：L1 目标函数与模型头。复现级别：L1 目标函数与模型头。实现候选 marker 表示、候选概率监督与 RLCD 风格校准项；未训练论文 1000 万样本模型。ChineseJevHead 可前后向并验证概率归一化和有限梯度；没有论文数据、完整 backbone、移动端 INT8 部署或论文级性能对照。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36965">原论文</a> · <a href="../../../../foundation-models/2609.36965-chinese-jev/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="system-one" data-topic="system-one/typed-readout" data-search="GLiClass: Generalist Lightweight Model for Sequence Classification Tasks 基础模型 Knowledgator 2025-08-11 GLiClass 把文本和运行时给定的候选标签放进同一个分类接口，避免生成式 LLM 的解析不稳定，也避免 cross-encoder 对每个文本—标签对逐次推理。本仓库保留“候选内容参与打分”和“一次归一化得到全候选分布”这两个定义性机制。本地实现是 NumPy 机制基线，不加载 GLiClass 权重，不宣称复现论文的完整 Transformer、PPO 多标签训练或论文数值。它用于 System One 的 Banking77 统一协议和 Evolve operator。 只复现动态候选交互与一次归一化机制，不复现 GLiClass 完整权重、训练语料或 PPO 流程。  动态候选分类 System One 相邻方法 结构化决策 类型化读出：从生成句子到候选分布">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 类型化读出：从生成句子到候选分布</a></p>
<h2 id="paper-foundation-models-gliclass-1a6b1ec2">GLiClass: Generalist Lightweight Model for Sequence Classification Tasks</h2>
<p class="ar-learning-card__meta">Knowledgator · 论文公开：2025-08-11</p>
<p><strong>方法要点：</strong>GLiClass 把文本和运行时给定的候选标签放进同一个分类接口，避免生成式 LLM 的解析不稳定，也避免 cross-encoder 对每个文本—标签对逐次推理。本仓库保留“候选内容参与打分”和“一次归一化得到全候选分布”这两个定义性机制。本地实现是 NumPy 机制基线，不加载 GLiClass 权重，不宣称复现论文的完整 Transformer、PPO 多标签训练或论文数值。它用于 System One 的 Banking77 统一协议和 Evolve operator。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>只复现动态候选交互与一次归一化机制，不复现 GLiClass 完整权重、训练语料或 PPO 流程。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.07662">原论文</a> · <a href="../../../../foundation-models/2508.07662-gliclass/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
