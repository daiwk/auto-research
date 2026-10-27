---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 能力证据：评测采样、读出与可靠性

[基础模型](index.md) / 52 个问题 · 13 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

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
<p class="ar-learning-status" data-learning-status role="status">52 个问题 · 13 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:detector-scope" data-paper-title="Building Auditable AI Text Detectors with Sparse Autoencoders" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Building Auditable AI Text Detectors with Sparse Autoencoders 基础模型 University of Pennsylvania 2026-10-21 DetectorScope 把黑盒检测器的残差流转换为 SAE 稀疏特征，按 token 取最大值后跨层拼接，再用自动解释的验证分数筛掉不可靠概念。轻量 L1 线性头只使用保留特征，因此每个预测能分解成可置零核验的概念贡献，而不是在黑盒输出后补写理由。原文还包含 SAE 训练、Gemini 描述生成与验证、大语料特征缓存和多条件检测实验；这些不是本地稀疏头的隐式功能。描述文字存在不代表语义正确，Spearman 分数也不是人工审查或误伤风险担保。 完整实验成本过高，不复现（审查 DONE）。诊断使用小规模合成激活张量，12 个训练文档、4 个隔离预测输入；本地仅实现 L1 小张量机制：冻结 SAE 特征接口、描述验证分数、稀疏线性头与精确归因。不是完整 AI 文本检测器，也不是公开 benchmark 能力复现。完整实验成本过高，不复现（审查 DONE）。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  可解释性 稀疏特征与可审计检测 基础模型 能力证据：评测采样、读出与可靠性 DetectorScope 为什么把检测预测建立在可检查的稀疏特征上？ 它先池化SAE特征并筛除描述不可靠的概念，再用轻量稀疏线性头预测，使每次logit能分解为明确特征贡献。可解释性来自实际计算结构，而非预测后补写一句理由。 示意：某概念贡献可通过置零该特征核对，不必相信一段与检测分数无关的生成解释。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<span id="paper-foundation-models-detector-scope-a45f37d9" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d312990e6a285659">DetectorScope 为什么把检测预测建立在可检查的稀疏特征上？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adetector-scope">Building Auditable AI Text Detectors with Sparse Autoencoders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pennsylvania</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它先池化SAE特征并筛除描述不可靠的概念，再用轻量稀疏线性头预测，使每次logit能分解为明确特征贡献。可解释性来自实际计算结构，而非预测后补写一句理由。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某概念贡献可通过置零该特征核对，不必相信一段与检测分数无关的生成解释。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30006v1">原论文</a> · <a href="../../../../foundation-models/2610.30006-detector-scope/">实现解读</a> · <a href="#qa-d312990e6a285659">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:detector-scope" data-paper-title="Building Auditable AI Text Detectors with Sparse Autoencoders" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Building Auditable AI Text Detectors with Sparse Autoencoders 基础模型 University of Pennsylvania 2026-10-21 DetectorScope 把黑盒检测器的残差流转换为 SAE 稀疏特征，按 token 取最大值后跨层拼接，再用自动解释的验证分数筛掉不可靠概念。轻量 L1 线性头只使用保留特征，因此每个预测能分解成可置零核验的概念贡献，而不是在黑盒输出后补写理由。原文还包含 SAE 训练、Gemini 描述生成与验证、大语料特征缓存和多条件检测实验；这些不是本地稀疏头的隐式功能。描述文字存在不代表语义正确，Spearman 分数也不是人工审查或误伤风险担保。 完整实验成本过高，不复现（审查 DONE）。诊断使用小规模合成激活张量，12 个训练文档、4 个隔离预测输入；本地仅实现 L1 小张量机制：冻结 SAE 特征接口、描述验证分数、稀疏线性头与精确归因。不是完整 AI 文本检测器，也不是公开 benchmark 能力复现。完整实验成本过高，不复现（审查 DONE）。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  可解释性 稀疏特征与可审计检测 基础模型 能力证据：评测采样、读出与可靠性 DetectorScope的概念贡献为什么等于置零特征的logit差，却不能称为改写文本的因果效果？ 稀疏特征池化后进入线性检测头，每个权重乘激活都可精确分解，因此置零该池化特征的logit变化可核验。改写原文会同时改变多个特征与上下文，不受这条线性等式约束。自动描述和相关验证也不保证语义无误，本地头组件不含完整SAE与解释生成流程。 例如某概念贡献增加检测分数，置零它能验证分数差；删除原文一个词可能连带改变其他概念，不能把二者变化当作同一种干预。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-cf2ae2f87e6ebcb4">DetectorScope的概念贡献为什么等于置零特征的logit差，却不能称为改写文本的因果效果？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adetector-scope">Building Auditable AI Text Detectors with Sparse Autoencoders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pennsylvania</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>稀疏特征池化后进入线性检测头，每个权重乘激活都可精确分解，因此置零该池化特征的logit变化可核验。改写原文会同时改变多个特征与上下文，不受这条线性等式约束。自动描述和相关验证也不保证语义无误，本地头组件不含完整SAE与解释生成流程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某概念贡献增加检测分数，置零它能验证分数差；删除原文一个词可能连带改变其他概念，不能把二者变化当作同一种干预。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30006v1">原论文</a> · <a href="../../../../foundation-models/2610.30006-detector-scope/">实现解读</a> · <a href="#qa-cf2ae2f87e6ebcb4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:detector-scope" data-paper-title="Building Auditable AI Text Detectors with Sparse Autoencoders" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Building Auditable AI Text Detectors with Sparse Autoencoders 基础模型 University of Pennsylvania 2026-10-21 DetectorScope 把黑盒检测器的残差流转换为 SAE 稀疏特征，按 token 取最大值后跨层拼接，再用自动解释的验证分数筛掉不可靠概念。轻量 L1 线性头只使用保留特征，因此每个预测能分解成可置零核验的概念贡献，而不是在黑盒输出后补写理由。原文还包含 SAE 训练、Gemini 描述生成与验证、大语料特征缓存和多条件检测实验；这些不是本地稀疏头的隐式功能。描述文字存在不代表语义正确，Spearman 分数也不是人工审查或误伤风险担保。 完整实验成本过高，不复现（审查 DONE）。诊断使用小规模合成激活张量，12 个训练文档、4 个隔离预测输入；本地仅实现 L1 小张量机制：冻结 SAE 特征接口、描述验证分数、稀疏线性头与精确归因。不是完整 AI 文本检测器，也不是公开 benchmark 能力复现。完整实验成本过高，不复现（审查 DONE）。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  可解释性 稀疏特征与可审计检测 基础模型 能力证据：评测采样、读出与可靠性 DetectorScope 的概念描述验证，与人工确认该概念语义可靠相同吗？ Spearman衡量外部真实与预测激活的秩相关，是筛选信号，不能当作人工审查或误伤担保。常量序列甚至无法验证描述，不能强行给高分后称其可解释。 示意：一段描述与少量激活排序相关，仍不足以证明在所有文本上语义都准确。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-2d18e295a89d2470">DetectorScope 的概念描述验证，与人工确认该概念语义可靠相同吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adetector-scope">Building Auditable AI Text Detectors with Sparse Autoencoders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pennsylvania</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Spearman衡量外部真实与预测激活的秩相关，是筛选信号，不能当作人工审查或误伤担保。常量序列甚至无法验证描述，不能强行给高分后称其可解释。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一段描述与少量激活排序相关，仍不足以证明在所有文本上语义都准确。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30006v1">原论文</a> · <a href="../../../../foundation-models/2610.30006-detector-scope/">实现解读</a> · <a href="#qa-2d18e295a89d2470">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:detector-scope" data-paper-title="Building Auditable AI Text Detectors with Sparse Autoencoders" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Building Auditable AI Text Detectors with Sparse Autoencoders 基础模型 University of Pennsylvania 2026-10-21 DetectorScope 把黑盒检测器的残差流转换为 SAE 稀疏特征，按 token 取最大值后跨层拼接，再用自动解释的验证分数筛掉不可靠概念。轻量 L1 线性头只使用保留特征，因此每个预测能分解成可置零核验的概念贡献，而不是在黑盒输出后补写理由。原文还包含 SAE 训练、Gemini 描述生成与验证、大语料特征缓存和多条件检测实验；这些不是本地稀疏头的隐式功能。描述文字存在不代表语义正确，Spearman 分数也不是人工审查或误伤风险担保。 完整实验成本过高，不复现（审查 DONE）。诊断使用小规模合成激活张量，12 个训练文档、4 个隔离预测输入；本地仅实现 L1 小张量机制：冻结 SAE 特征接口、描述验证分数、稀疏线性头与精确归因。不是完整 AI 文本检测器，也不是公开 benchmark 能力复现。完整实验成本过高，不复现（审查 DONE）。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  可解释性 稀疏特征与可审计检测 基础模型 能力证据：评测采样、读出与可靠性 DetectorScope 的 L1 更新为何不能既做次梯度惩罚又再 soft-threshold 一次？ 文档先做BCE梯度SGD momentum，再执行ηλ soft-threshold，不额外对L1求次梯度，也不惩罚bias。RMS只从训练拟合且不中心化，预测不可重拟合held-out尺度。 示意：两次施加L1会让稀疏强度超过所声明λ，改变头的实际训练目标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c1a5afb8140989d8">DetectorScope 的 L1 更新为何不能既做次梯度惩罚又再 soft-threshold 一次？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adetector-scope">Building Auditable AI Text Detectors with Sparse Autoencoders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pennsylvania</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档先做BCE梯度SGD momentum，再执行ηλ soft-threshold，不额外对L1求次梯度，也不惩罚bias。RMS只从训练拟合且不中心化，预测不可重拟合held-out尺度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两次施加L1会让稀疏强度超过所声明λ，改变头的实际训练目标。</p>
<p class="ar-learning-sources">依据：核心公式、数据协议与结果；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30006v1">原论文</a> · <a href="../../../../foundation-models/2610.30006-detector-scope/">实现解读</a> · <a href="#qa-c1a5afb8140989d8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:deepsea" data-paper-title="DeepSEA: A Multilingual Evaluation Benchmark for Southeast Asia" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="DeepSEA: A Multilingual Evaluation Benchmark for Southeast Asia 基础模型 Google Research 2026-10-19 现有多语言评测对东南亚低资源语言覆盖不足。DeepSEA 通过专业翻译与质量审核扩展五类公开任务，支持按语言资源层级比较推理、问答和生成表现；研究同时分析英语中转、错误类型及 tokenizer 效率。它是 benchmark，而非改变语言模型参数的训练算法。 因此完整模型实验成本过高，不复现（审查 DONE），不下载大权重、不试跑全量矩阵、不自动重试。诊断只报告 scorer_contract_cases、reference_score_error、coverage_rejection_count 和 model_calls=0。DeepSEATask 深复制 evaluator 私有参考；预测回调仅接收不可变 PublicExample。各任务用字段白名单重建公开输入：问题、选项、上下文或源文本；answer、answer_with_cot、附加 metadata 和 few-shot 示例不会自动流入预测。预测按固定的语言/学科/行号绑定；  多语言与分词 公开评测协议 基础模型 能力证据：评测采样、读出与可靠性 DeepSEA 为什么不只报告一个多语言总分？ 研究针对东南亚低资源语言覆盖，按语言资源层级和任务报告能看出平均分掩盖的差距。它提供评测数据与协议，不是改变模型参数的训练算法。 示意：高资源语言表现很好，可能把低资源语言的明显失误淹没在总体均值里。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<span id="paper-foundation-models-deepsea-86ba1d33" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c952637f784a5e5b">DeepSEA 为什么不只报告一个多语言总分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adeepsea">DeepSEA: A Multilingual Evaluation Benchmark for Southeast Asia</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>研究针对东南亚低资源语言覆盖，按语言资源层级和任务报告能看出平均分掩盖的差距。它提供评测数据与协议，不是改变模型参数的训练算法。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>高资源语言表现很好，可能把低资源语言的明显失误淹没在总体均值里。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.26155v1">原论文</a> · <a href="../../../../foundation-models/2610.26155-deepsea/">实现解读</a> · <a href="#qa-c952637f784a5e5b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:deepsea" data-paper-title="DeepSEA: A Multilingual Evaluation Benchmark for Southeast Asia" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="DeepSEA: A Multilingual Evaluation Benchmark for Southeast Asia 基础模型 Google Research 2026-10-19 现有多语言评测对东南亚低资源语言覆盖不足。DeepSEA 通过专业翻译与质量审核扩展五类公开任务，支持按语言资源层级比较推理、问答和生成表现；研究同时分析英语中转、错误类型及 tokenizer 效率。它是 benchmark，而非改变语言模型参数的训练算法。 因此完整模型实验成本过高，不复现（审查 DONE），不下载大权重、不试跑全量矩阵、不自动重试。诊断只报告 scorer_contract_cases、reference_score_error、coverage_rejection_count 和 model_calls=0。DeepSEATask 深复制 evaluator 私有参考；预测回调仅接收不可变 PublicExample。各任务用字段白名单重建公开输入：问题、选项、上下文或源文本；answer、answer_with_cot、附加 metadata 和 few-shot 示例不会自动流入预测。预测按固定的语言/学科/行号绑定；  多语言与分词 公开评测协议 基础模型 能力证据：评测采样、读出与可靠性 DeepSEA按语言资源分组报告，为什么仍必须固定预测顺序并隔离Gold？ 各语言与任务的覆盖不同，只有严格校验语言、数量和顺序，才能让预测与相应样本评分正确对齐。公开输入只投影问题所需字段，答案由评测器独占，防止把翻译标注或评分信息送给被测模型。该基准衡量低资源语言表现，不是提升参数能力的训练算法。 例如同一题的两种语言输出交换位置，会把语言差异变成对齐错误；预测器应只见问题，不能同时拿到评分器保存的正确答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8cb698c67be1a136">DeepSEA按语言资源分组报告，为什么仍必须固定预测顺序并隔离Gold？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adeepsea">DeepSEA: A Multilingual Evaluation Benchmark for Southeast Asia</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>各语言与任务的覆盖不同，只有严格校验语言、数量和顺序，才能让预测与相应样本评分正确对齐。公开输入只投影问题所需字段，答案由评测器独占，防止把翻译标注或评分信息送给被测模型。该基准衡量低资源语言表现，不是提升参数能力的训练算法。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一题的两种语言输出交换位置，会把语言差异变成对齐错误；预测器应只见问题，不能同时拿到评分器保存的正确答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与评分口径；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.26155v1">原论文</a> · <a href="../../../../foundation-models/2610.26155-deepsea/">实现解读</a> · <a href="#qa-8cb698c67be1a136">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:deepsea" data-paper-title="DeepSEA: A Multilingual Evaluation Benchmark for Southeast Asia" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="DeepSEA: A Multilingual Evaluation Benchmark for Southeast Asia 基础模型 Google Research 2026-10-19 现有多语言评测对东南亚低资源语言覆盖不足。DeepSEA 通过专业翻译与质量审核扩展五类公开任务，支持按语言资源层级比较推理、问答和生成表现；研究同时分析英语中转、错误类型及 tokenizer 效率。它是 benchmark，而非改变语言模型参数的训练算法。 因此完整模型实验成本过高，不复现（审查 DONE），不下载大权重、不试跑全量矩阵、不自动重试。诊断只报告 scorer_contract_cases、reference_score_error、coverage_rejection_count 和 model_calls=0。DeepSEATask 深复制 evaluator 私有参考；预测回调仅接收不可变 PublicExample。各任务用字段白名单重建公开输入：问题、选项、上下文或源文本；answer、answer_with_cot、附加 metadata 和 few-shot 示例不会自动流入预测。预测按固定的语言/学科/行号绑定；  多语言与分词 公开评测协议 基础模型 能力证据：评测采样、读出与可靠性 确定性 scorer 与 LLM judge，在 DeepSEA 接口中是同一个可替换环节吗？ 评分必须遵循各任务固定上游口径，不应临时换成另一个judge后仍直接横比。预测与参考的绑定也需固定语言/学科/行号；分组报告不能修复错位评分。 示意：把语言A的第1条预测配到语言B参考，即使总条数一致，分数也没有有效含义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-599f68d2d3a3631c">确定性 scorer 与 LLM judge，在 DeepSEA 接口中是同一个可替换环节吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adeepsea">DeepSEA: A Multilingual Evaluation Benchmark for Southeast Asia</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>评分必须遵循各任务固定上游口径，不应临时换成另一个judge后仍直接横比。预测与参考的绑定也需固定语言/学科/行号；分组报告不能修复错位评分。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把语言A的第1条预测配到语言B参考，即使总条数一致，分数也没有有效含义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、公共输入与 Gold 隔离；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.26155v1">原论文</a> · <a href="../../../../foundation-models/2610.26155-deepsea/">实现解读</a> · <a href="#qa-599f68d2d3a3631c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:deepsea" data-paper-title="DeepSEA: A Multilingual Evaluation Benchmark for Southeast Asia" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="DeepSEA: A Multilingual Evaluation Benchmark for Southeast Asia 基础模型 Google Research 2026-10-19 现有多语言评测对东南亚低资源语言覆盖不足。DeepSEA 通过专业翻译与质量审核扩展五类公开任务，支持按语言资源层级比较推理、问答和生成表现；研究同时分析英语中转、错误类型及 tokenizer 效率。它是 benchmark，而非改变语言模型参数的训练算法。 因此完整模型实验成本过高，不复现（审查 DONE），不下载大权重、不试跑全量矩阵、不自动重试。诊断只报告 scorer_contract_cases、reference_score_error、coverage_rejection_count 和 model_calls=0。DeepSEATask 深复制 evaluator 私有参考；预测回调仅接收不可变 PublicExample。各任务用字段白名单重建公开输入：问题、选项、上下文或源文本；answer、answer_with_cot、附加 metadata 和 few-shot 示例不会自动流入预测。预测按固定的语言/学科/行号绑定；  多语言与分词 公开评测协议 基础模型 能力证据：评测采样、读出与可靠性 预测回调能收到 evaluator 对象或 benchmark 文件路径，再承诺不看 Gold 吗？ 不应这样设计。文档用白名单不可变公开输入与深复制私有参考隔离，缺语言、数量或字符串类型直接报错；该数据流合同也不是操作系统沙箱，不能额外开放shell绕过边界。 示意：回调只应收到题目、选项或上下文，不应拿到含answer_with_cot的原始记录。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-67c358643609ee55">预测回调能收到 evaluator 对象或 benchmark 文件路径，再承诺不看 Gold 吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adeepsea">DeepSEA: A Multilingual Evaluation Benchmark for Southeast Asia</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不应这样设计。文档用白名单不可变公开输入与深复制私有参考隔离，缺语言、数量或字符串类型直接报错；该数据流合同也不是操作系统沙箱，不能额外开放shell绕过边界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>回调只应收到题目、选项或上下文，不应拿到含answer_with_cot的原始记录。</p>
<p class="ar-learning-sources">依据：公共输入与 Gold 隔离；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.26155v1">原论文</a> · <a href="../../../../foundation-models/2610.26155-deepsea/">实现解读</a> · <a href="#qa-67c358643609ee55">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gemma-priority-protocol" data-paper-title="Words Speak Louder Than Order: A Behavioral Evaluation of Gemma 4" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Words Speak Louder Than Order: A Behavioral Evaluation of Gemma 4 基础模型 Google 2026-09-25 论文把双文档冲突中的词偏好、来源措辞和呈现顺序分别测量。方法与资源已核：四路交叉、十种提示条件、跨条件共同保留集，以及未筛选敏感性分析。研究范围是单模型、短上下文、英文单词选择；不是新的训练算法，也不是神经回路证据。 故完整模型实验记 not_run_scope_limited_protocol，不是已验证能力，也不在没有成本依据时硬标为“成本过高”。four_cell_effects 执行真实四路线性对照；analyze_cells 要求十条件、唯一项目ID、同序同量、有限数字，并同时输出主分析和敏感性分析。bca_interval 延迟加载 SciPy，采用9,999次、seed42、BCa95%；TOST使用0.15 nats界限和BCa90%。BCa失败保留 failed，零方差保留 degenerate；两者 equivalent=null，不静默改成percentile，不把退化输入伪造成通过。  公开评测协议 来源与顺序偏差 基础模型 能力证据：评测采样、读出与可靠性 Gemma 来源优先协议为什么把双文档冲突设计成多路交叉？ 词项本身、来源角色和呈现位置都可能影响选择。四路交叉让这些因素被单独分解，避免把词偏好或位置效应误写成模型信任某种来源。 示意：总是偏向词B，与总是偏向新文档提供的词，是两个不同倾向。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<span id="paper-foundation-models-gemma-priority-protocol-ec648fc1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c0619dc9d306ed2f">Gemma 来源优先协议为什么把双文档冲突设计成多路交叉？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agemma-priority-protocol">Words Speak Louder Than Order: A Behavioral Evaluation of Gemma 4</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>词项本身、来源角色和呈现位置都可能影响选择。四路交叉让这些因素被单独分解，避免把词偏好或位置效应误写成模型信任某种来源。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>总是偏向词B，与总是偏向新文档提供的词，是两个不同倾向。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.30716v1">原论文</a> · <a href="../../../../foundation-models/2609.30716-gemma-priority-protocol/">实现解读</a> · <a href="#qa-c0619dc9d306ed2f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gemma-priority-protocol" data-paper-title="Words Speak Louder Than Order: A Behavioral Evaluation of Gemma 4" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Words Speak Louder Than Order: A Behavioral Evaluation of Gemma 4 基础模型 Google 2026-09-25 论文把双文档冲突中的词偏好、来源措辞和呈现顺序分别测量。方法与资源已核：四路交叉、十种提示条件、跨条件共同保留集，以及未筛选敏感性分析。研究范围是单模型、短上下文、英文单词选择；不是新的训练算法，也不是神经回路证据。 故完整模型实验记 not_run_scope_limited_protocol，不是已验证能力，也不在没有成本依据时硬标为“成本过高”。four_cell_effects 执行真实四路线性对照；analyze_cells 要求十条件、唯一项目ID、同序同量、有限数字，并同时输出主分析和敏感性分析。bca_interval 延迟加载 SciPy，采用9,999次、seed42、BCa95%；TOST使用0.15 nats界限和BCa90%。BCa失败保留 failed，零方差保留 degenerate；两者 equivalent=null，不静默改成percentile，不把退化输入伪造成通过。  公开评测协议 来源与顺序偏差 基础模型 能力证据：评测采样、读出与可靠性 双文档冲突实验为什么要同时交换词项身份和呈现顺序，而不只调换两段文字？ 只换顺序会把词本身偏好、来源角色与位置混在一起。四路交叉用正交对照分别估计这些效应，再按跨条件共同筛选集比较，未筛选敏感性分析仍保留。来源效应与位置效应不能由两个简单均值替代，该协议也只支持单模型短英文选择的行为结论。 例如模型偏爱某个词时，它放哪都容易被选；同时交换哪个词代表旧来源，才有机会分清来源标签与先后位置各贡献了多少。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-a7630018ee8af5c2">双文档冲突实验为什么要同时交换词项身份和呈现顺序，而不只调换两段文字？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agemma-priority-protocol">Words Speak Louder Than Order: A Behavioral Evaluation of Gemma 4</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只换顺序会把词本身偏好、来源角色与位置混在一起。四路交叉用正交对照分别估计这些效应，再按跨条件共同筛选集比较，未筛选敏感性分析仍保留。来源效应与位置效应不能由两个简单均值替代，该协议也只支持单模型短英文选择的行为结论。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型偏爱某个词时，它放哪都容易被选；同时交换哪个词代表旧来源，才有机会分清来源标签与先后位置各贡献了多少。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.30716v1">原论文</a> · <a href="../../../../foundation-models/2609.30716-gemma-priority-protocol/">实现解读</a> · <a href="#qa-a7630018ee8af5c2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gemma-priority-protocol" data-paper-title="Words Speak Louder Than Order: A Behavioral Evaluation of Gemma 4" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Words Speak Louder Than Order: A Behavioral Evaluation of Gemma 4 基础模型 Google 2026-09-25 论文把双文档冲突中的词偏好、来源措辞和呈现顺序分别测量。方法与资源已核：四路交叉、十种提示条件、跨条件共同保留集，以及未筛选敏感性分析。研究范围是单模型、短上下文、英文单词选择；不是新的训练算法，也不是神经回路证据。 故完整模型实验记 not_run_scope_limited_protocol，不是已验证能力，也不在没有成本依据时硬标为“成本过高”。four_cell_effects 执行真实四路线性对照；analyze_cells 要求十条件、唯一项目ID、同序同量、有限数字，并同时输出主分析和敏感性分析。bca_interval 延迟加载 SciPy，采用9,999次、seed42、BCa95%；TOST使用0.15 nats界限和BCa90%。BCa失败保留 failed，零方差保留 degenerate；两者 equivalent=null，不静默改成percentile，不把退化输入伪造成通过。  公开评测协议 来源与顺序偏差 基础模型 能力证据：评测采样、读出与可靠性 四路分解中的顺序零对照 O 与位置效应 S，为什么不能混称？ 两者使用不同正负组合，测量对象不同；文档S才是位置效应，负S表示偏首，O用于零对照。各量是半效应，完整极差还要乘2，不能换标签横比。 示意：同一组e1到e4，换一组符号组合会得到另一种效应而非同名结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-8b9be55c7b07d71e">四路分解中的顺序零对照 O 与位置效应 S，为什么不能混称？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agemma-priority-protocol">Words Speak Louder Than Order: A Behavioral Evaluation of Gemma 4</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两者使用不同正负组合，测量对象不同；文档S才是位置效应，负S表示偏首，O用于零对照。各量是半效应，完整极差还要乘2，不能换标签横比。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一组e1到e4，换一组符号组合会得到另一种效应而非同名结果。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.30716v1">原论文</a> · <a href="../../../../foundation-models/2609.30716-gemma-priority-protocol/">实现解读</a> · <a href="#qa-8b9be55c7b07d71e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gemma-priority-protocol" data-paper-title="Words Speak Louder Than Order: A Behavioral Evaluation of Gemma 4" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Words Speak Louder Than Order: A Behavioral Evaluation of Gemma 4 基础模型 Google 2026-09-25 论文把双文档冲突中的词偏好、来源措辞和呈现顺序分别测量。方法与资源已核：四路交叉、十种提示条件、跨条件共同保留集，以及未筛选敏感性分析。研究范围是单模型、短上下文、英文单词选择；不是新的训练算法，也不是神经回路证据。 故完整模型实验记 not_run_scope_limited_protocol，不是已验证能力，也不在没有成本依据时硬标为“成本过高”。four_cell_effects 执行真实四路线性对照；analyze_cells 要求十条件、唯一项目ID、同序同量、有限数字，并同时输出主分析和敏感性分析。bca_interval 延迟加载 SciPy，采用9,999次、seed42、BCa95%；TOST使用0.15 nats界限和BCa90%。BCa失败保留 failed，零方差保留 degenerate；两者 equivalent=null，不静默改成percentile，不把退化输入伪造成通过。  公开评测协议 来源与顺序偏差 基础模型 能力证据：评测采样、读出与可靠性 BCa 区间失败或输入零方差时，能默默回退再给出 equivalent=true 吗？ 文档明确保留failed或degenerate并令equivalent=null，不静默换percentile。十条件主分析还应共用剔除并集，并保留未筛选敏感性分析，不能逐条件挑有利样本。 示意：bootstrap无法提供有效区间时，应显示未判定，而不是把异常处理当成等价通过。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-72e8f96ddb1142bd">BCa 区间失败或输入零方差时，能默默回退再给出 equivalent=true 吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agemma-priority-protocol">Words Speak Louder Than Order: A Behavioral Evaluation of Gemma 4</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档明确保留failed或degenerate并令equivalent=null，不静默换percentile。十条件主分析还应共用剔除并集，并保留未筛选敏感性分析，不能逐条件挑有利样本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>bootstrap无法提供有效区间时，应显示未判定，而不是把异常处理当成等价通过。</p>
<p class="ar-learning-sources">依据：核心公式、实现与数据协议；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.30716v1">原论文</a> · <a href="../../../../foundation-models/2609.30716-gemma-priority-protocol/">实现解读</a> · <a href="#qa-72e8f96ddb1142bd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:interpolated-null-calibration" data-paper-title="How Calibration Content Shapes Attention-Based Reranking" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="How Calibration Content Shapes Attention-Based Reranking 基础模型 UC San Diego 2026-09-15 固定v1 Section3 Eq4–7：ΔN=s(empty,I)−s(empty,empty)，Sλ=s(q,I)−[λs(empty,I)+(1−λ)s(empty,empty)]；λ1标准ICR、λ0bare-null。调用方真实三pass提分数并保证doc identity对齐；λ只能validation选。论文oracle λ对全数据查询调参，不能当独立test结果。 成本过高，不复现（审查 DONE）。Gemma3-4B/Qwen3-4B/Llama3.1-8B/Qwen3-14B，top100每doc130tokens、16Kcontext三prefill，多benchmark/5fold/λ网格/QRhead选择；单A10040GB配置。完整模型加载和广泛矩阵超短时组件预算；不宣称真实retrieval改善。输入是已有三次模型attention读出的、相同doc ID顺序下的分数。本地实现Eq4–7及稳定ranking，没有真实attention extractor、ICR outlier filter/QRhead选择、LLM加载或工业线上A/B；  基础模型检索与排序 注意力读出与校准 基础模型 能力证据：评测采样、读出与可靠性 attention reranking 为什么需要比较带指令 null 与 bare null？ 无真实query时，指令本身也可能改变文档得分。插值null校准分开度量这部分影响，并控制从query+instruction得分中扣除哪种基线，避免把校准内容当成无关细节。 示意：相同文档仅因出现“判断相关性”指令而更高分，这部分未必来自用户query。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<span id="paper-foundation-models-interpolated-null-calibration-34c35a07" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ff4ec052068c69b3">attention reranking 为什么需要比较带指令 null 与 bare null？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ainterpolated-null-calibration">How Calibration Content Shapes Attention-Based Reranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>无真实query时，指令本身也可能改变文档得分。插值null校准分开度量这部分影响，并控制从query+instruction得分中扣除哪种基线，避免把校准内容当成无关细节。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>相同文档仅因出现“判断相关性”指令而更高分，这部分未必来自用户query。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17764v1">原论文</a> · <a href="../../../../foundation-models/2609.17764-interpolated-null-calibration/">实现解读</a> · <a href="#qa-ff4ec052068c69b3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:interpolated-null-calibration" data-paper-title="How Calibration Content Shapes Attention-Based Reranking" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="How Calibration Content Shapes Attention-Based Reranking 基础模型 UC San Diego 2026-09-15 固定v1 Section3 Eq4–7：ΔN=s(empty,I)−s(empty,empty)，Sλ=s(q,I)−[λs(empty,I)+(1−λ)s(empty,empty)]；λ1标准ICR、λ0bare-null。调用方真实三pass提分数并保证doc identity对齐；λ只能validation选。论文oracle λ对全数据查询调参，不能当独立test结果。 成本过高，不复现（审查 DONE）。Gemma3-4B/Qwen3-4B/Llama3.1-8B/Qwen3-14B，top100每doc130tokens、16Kcontext三prefill，多benchmark/5fold/λ网格/QRhead选择；单A10040GB配置。完整模型加载和广泛矩阵超短时组件预算；不宣称真实retrieval改善。输入是已有三次模型attention读出的、相同doc ID顺序下的分数。本地实现Eq4–7及稳定ranking，没有真实attention extractor、ICR outlier filter/QRhead选择、LLM加载或工业线上A/B；  基础模型检索与排序 注意力读出与校准 基础模型 能力证据：评测采样、读出与可靠性 插值null校准取λ=0时，为什么仍不是完全不校准？ 插值在含指令空查询分数与完全空基线之间调节，零权重仍减去bare-null分数，只是不扣含指令那部分。三次模型评分必须按文档身份对齐，权重只能用验证集选；用全数据最佳权重得到的oracle分数不是独立测试收益。本地只实现分数运算核。 例如文档即使没有问题也因长度获得偏高注意分，bare-null仍会扣掉这种基线；把零权重直接当原始分数，会比较错方法。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-bcefd02394192a61">插值null校准取λ=0时，为什么仍不是完全不校准？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ainterpolated-null-calibration">How Calibration Content Shapes Attention-Based Reranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>插值在含指令空查询分数与完全空基线之间调节，零权重仍减去bare-null分数，只是不扣含指令那部分。三次模型评分必须按文档身份对齐，权重只能用验证集选；用全数据最佳权重得到的oracle分数不是独立测试收益。本地只实现分数运算核。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如文档即使没有问题也因长度获得偏高注意分，bare-null仍会扣掉这种基线；把零权重直接当原始分数，会比较错方法。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17764v1">原论文</a> · <a href="../../../../foundation-models/2609.17764-interpolated-null-calibration/">实现解读</a> · <a href="#qa-bcefd02394192a61">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:interpolated-null-calibration" data-paper-title="How Calibration Content Shapes Attention-Based Reranking" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="How Calibration Content Shapes Attention-Based Reranking 基础模型 UC San Diego 2026-09-15 固定v1 Section3 Eq4–7：ΔN=s(empty,I)−s(empty,empty)，Sλ=s(q,I)−[λs(empty,I)+(1−λ)s(empty,empty)]；λ1标准ICR、λ0bare-null。调用方真实三pass提分数并保证doc identity对齐；λ只能validation选。论文oracle λ对全数据查询调参，不能当独立test结果。 成本过高，不复现（审查 DONE）。Gemma3-4B/Qwen3-4B/Llama3.1-8B/Qwen3-14B，top100每doc130tokens、16Kcontext三prefill，多benchmark/5fold/λ网格/QRhead选择；单A10040GB配置。完整模型加载和广泛矩阵超短时组件预算；不宣称真实retrieval改善。输入是已有三次模型attention读出的、相同doc ID顺序下的分数。本地实现Eq4–7及稳定ranking，没有真实attention extractor、ICR outlier filter/QRhead选择、LLM加载或工业线上A/B；  基础模型检索与排序 注意力读出与校准 基础模型 能力证据：评测采样、读出与可靠性 标准 ICR、bare-null 与完全不校准，分别减去了什么？ λ=1减带指令null，λ=0减bare null，完全不校准才不减任何null。三者不是同一条参数轴的含混名字；比较时要把真实三pass输入与扣减项说明白。 示意：s(empty,empty)非零时，λ=0的排序分数仍可能明显不同于原始s(q,I)。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4fd6cf0787d7d93f">标准 ICR、bare-null 与完全不校准，分别减去了什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ainterpolated-null-calibration">How Calibration Content Shapes Attention-Based Reranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>λ=1减带指令null，λ=0减bare null，完全不校准才不减任何null。三者不是同一条参数轴的含混名字；比较时要把真实三pass输入与扣减项说明白。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>s(empty,empty)非零时，λ=0的排序分数仍可能明显不同于原始s(q,I)。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17764v1">原论文</a> · <a href="../../../../foundation-models/2609.17764-interpolated-null-calibration/">实现解读</a> · <a href="#qa-4fd6cf0787d7d93f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:interpolated-null-calibration" data-paper-title="How Calibration Content Shapes Attention-Based Reranking" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="How Calibration Content Shapes Attention-Based Reranking 基础模型 UC San Diego 2026-09-15 固定v1 Section3 Eq4–7：ΔN=s(empty,I)−s(empty,empty)，Sλ=s(q,I)−[λs(empty,I)+(1−λ)s(empty,empty)]；λ1标准ICR、λ0bare-null。调用方真实三pass提分数并保证doc identity对齐；λ只能validation选。论文oracle λ对全数据查询调参，不能当独立test结果。 成本过高，不复现（审查 DONE）。Gemma3-4B/Qwen3-4B/Llama3.1-8B/Qwen3-14B，top100每doc130tokens、16Kcontext三prefill，多benchmark/5fold/λ网格/QRhead选择；单A10040GB配置。完整模型加载和广泛矩阵超短时组件预算；不宣称真实retrieval改善。输入是已有三次模型attention读出的、相同doc ID顺序下的分数。本地实现Eq4–7及稳定ranking，没有真实attention extractor、ICR outlier filter/QRhead选择、LLM加载或工业线上A/B；  基础模型检索与排序 注意力读出与校准 基础模型 能力证据：评测采样、读出与可靠性 三次模型 pass 的分数数组长度相同，是否就能直接逐项相减？ 还必须保证文档ID和顺序完全一致，不能只看shape。λ需按validation选择，不能拿全数据oracle λ当独立test效果；本地分数算子也不包含真实attention extractor。 示意：第二次pass把docA和docB交换了，逐位置减法会把另一个文档的null扣过来。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-29ced52dac6ef415">三次模型 pass 的分数数组长度相同，是否就能直接逐项相减？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ainterpolated-null-calibration">How Calibration Content Shapes Attention-Based Reranking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>还必须保证文档ID和顺序完全一致，不能只看shape。λ需按validation选择，不能拿全数据oracle λ当独立test效果；本地分数算子也不包含真实attention extractor。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>第二次pass把docA和docB交换了，逐位置减法会把另一个文档的null扣过来。</p>
<p class="ar-learning-sources">依据：背景与主要改动、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17764v1">原论文</a> · <a href="../../../../foundation-models/2609.17764-interpolated-null-calibration/">实现解读</a> · <a href="#qa-29ced52dac6ef415">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:criticl" data-paper-title="CritICL: Inference-Time Weak-to-Strong Generalization from Small Language Model Failure Modes" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="CritICL: Inference-Time Weak-to-Strong Generalization from Small Language Model Failure Modes 基础模型 The Ohio State University 2026-08-27 弱模型错误不是随机噪声，而会聚成可跨模型尺度迁移的失败模式。CritICL 离线归纳 CritBank；static 使用全局高频失败模式，dynamic 根据当前输入检索相关 critique，再让强模型只生成一次答案。 复现级别：模型无关核心机制。复现级别：模型无关核心机制。实现 CritBank、静态/动态检索和单次推理提示构造，不伪造 checkpoint 指标。单元测试覆盖确定性 static/dynamic 检索、failure-mode 去重和零在线弱模型调用。当前没有下载大 checkpoint，因此不发布准确率；该机制也没有冒充 Micro-LLM 结构算子。  弱模型失败模式 ICL 基础模型 能力证据：评测采样、读出与可靠性 CritICL 为什么先从弱模型错误构建 CritBank？ 弱模型错误可聚成较稳定失败模式，离线整理后可作为强模型推理前的提醒。它把反思成本前移，不要求每个部署问题先让强模型失败一次。 示意：常见“忽略单位换算”的失败模式，可在新题作答前作为critique提示。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<span id="paper-foundation-models-criticl-4a912854" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-429d311a384d5142">CritICL 为什么先从弱模型错误构建 CritBank？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Acriticl">CritICL: Inference-Time Weak-to-Strong Generalization from Small Language Model Failure Modes</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Ohio State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>弱模型错误可聚成较稳定失败模式，离线整理后可作为强模型推理前的提醒。它把反思成本前移，不要求每个部署问题先让强模型失败一次。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>常见“忽略单位换算”的失败模式，可在新题作答前作为critique提示。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27455">原论文</a> · <a href="../../../../foundation-models/2608.27455-criticl/">实现解读</a> · <a href="#qa-429d311a384d5142">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:criticl" data-paper-title="CritICL: Inference-Time Weak-to-Strong Generalization from Small Language Model Failure Modes" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="CritICL: Inference-Time Weak-to-Strong Generalization from Small Language Model Failure Modes 基础模型 The Ohio State University 2026-08-27 弱模型错误不是随机噪声，而会聚成可跨模型尺度迁移的失败模式。CritICL 离线归纳 CritBank；static 使用全局高频失败模式，dynamic 根据当前输入检索相关 critique，再让强模型只生成一次答案。 复现级别：模型无关核心机制。复现级别：模型无关核心机制。实现 CritBank、静态/动态检索和单次推理提示构造，不伪造 checkpoint 指标。单元测试覆盖确定性 static/dynamic 检索、failure-mode 去重和零在线弱模型调用。当前没有下载大 checkpoint，因此不发布准确率；该机制也没有冒充 Micro-LLM 结构算子。  弱模型失败模式 ICL 基础模型 能力证据：评测采样、读出与可靠性 CritICL从弱模型错误归纳critique，为什么部署时不需要先让强模型答错再反思？ 离线失败模式库把重复错误抽象成可复用提示，静态版本用常见模式，动态版本按当前问题检索相关提醒。强模型在回答前读取这些提醒，只生成一次，不依赖本次错误答案反馈。迁移的是失败模式而非弱答案本身，提示相关性与库覆盖仍决定是否有用。 例如弱模型常忘记单位换算，库中形成检查单位的提醒；新题可在首次回答前检索它，而不能先读取该测试题正确解再写针对性批评。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-a53e3dc987414704">CritICL从弱模型错误归纳critique，为什么部署时不需要先让强模型答错再反思？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Acriticl">CritICL: Inference-Time Weak-to-Strong Generalization from Small Language Model Failure Modes</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Ohio State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>离线失败模式库把重复错误抽象成可复用提示，静态版本用常见模式，动态版本按当前问题检索相关提醒。强模型在回答前读取这些提醒，只生成一次，不依赖本次错误答案反馈。迁移的是失败模式而非弱答案本身，提示相关性与库覆盖仍决定是否有用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如弱模型常忘记单位换算，库中形成检查单位的提醒；新题可在首次回答前检索它，而不能先读取该测试题正确解再写针对性批评。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27455">原论文</a> · <a href="../../../../foundation-models/2608.27455-criticl/">实现解读</a> · <a href="#qa-a53e3dc987414704">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:criticl" data-paper-title="CritICL: Inference-Time Weak-to-Strong Generalization from Small Language Model Failure Modes" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="CritICL: Inference-Time Weak-to-Strong Generalization from Small Language Model Failure Modes 基础模型 The Ohio State University 2026-08-27 弱模型错误不是随机噪声，而会聚成可跨模型尺度迁移的失败模式。CritICL 离线归纳 CritBank；static 使用全局高频失败模式，dynamic 根据当前输入检索相关 critique，再让强模型只生成一次答案。 复现级别：模型无关核心机制。复现级别：模型无关核心机制。实现 CritBank、静态/动态检索和单次推理提示构造，不伪造 checkpoint 指标。单元测试覆盖确定性 static/dynamic 检索、failure-mode 去重和零在线弱模型调用。当前没有下载大 checkpoint，因此不发布准确率；该机制也没有冒充 Micro-LLM 结构算子。  弱模型失败模式 ICL 基础模型 能力证据：评测采样、读出与可靠性 CritICL static 与 dynamic 的 critique 选择有什么不同？ static复用全局高频失败模式，dynamic根据当前问题从CritBank检索相关critique。两者都应在生成前提供帮助，dynamic额外引入检索；不能把全局提醒当作已实现输入相关选择。 示意：数学题可检索计算类提醒，另一类输入则可能检索不同失败模式。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-72ab8c1467b98e00">CritICL static 与 dynamic 的 critique 选择有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Acriticl">CritICL: Inference-Time Weak-to-Strong Generalization from Small Language Model Failure Modes</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Ohio State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>static复用全局高频失败模式，dynamic根据当前问题从CritBank检索相关critique。两者都应在生成前提供帮助，dynamic额外引入检索；不能把全局提醒当作已实现输入相关选择。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>数学题可检索计算类提醒，另一类输入则可能检索不同失败模式。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27455">原论文</a> · <a href="../../../../foundation-models/2608.27455-criticl/">实现解读</a> · <a href="#qa-72ab8c1467b98e00">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:criticl" data-paper-title="CritICL: Inference-Time Weak-to-Strong Generalization from Small Language Model Failure Modes" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="CritICL: Inference-Time Weak-to-Strong Generalization from Small Language Model Failure Modes 基础模型 The Ohio State University 2026-08-27 弱模型错误不是随机噪声，而会聚成可跨模型尺度迁移的失败模式。CritICL 离线归纳 CritBank；static 使用全局高频失败模式，dynamic 根据当前输入检索相关 critique，再让强模型只生成一次答案。 复现级别：模型无关核心机制。复现级别：模型无关核心机制。实现 CritBank、静态/动态检索和单次推理提示构造，不伪造 checkpoint 指标。单元测试覆盖确定性 static/dynamic 检索、failure-mode 去重和零在线弱模型调用。当前没有下载大 checkpoint，因此不发布准确率；该机制也没有冒充 Micro-LLM 结构算子。  弱模型失败模式 ICL 基础模型 能力证据：评测采样、读出与可靠性 CritICL 部署时为什么不能先用当前题正确答案来挑最有效 critique？ 这样会把评测目标泄漏进提示选择。文档dynamic依赖当前输入与已有CritBank的相似度，再让强模型生成一次；离线失败模式与当前题隐藏答案需保持边界。 示意：先看该题标准答案再选“刚好能纠正它”的critique，不是可部署的输入检索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-496c385698250dff">CritICL 部署时为什么不能先用当前题正确答案来挑最有效 critique？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Acriticl">CritICL: Inference-Time Weak-to-Strong Generalization from Small Language Model Failure Modes</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Ohio State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这样会把评测目标泄漏进提示选择。文档dynamic依赖当前输入与已有CritBank的相似度，再让强模型生成一次；离线失败模式与当前题隐藏答案需保持边界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先看该题标准答案再选“刚好能纠正它”的critique，不是可部署的输入检索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27455">原论文</a> · <a href="../../../../foundation-models/2608.27455-criticl/">实现解读</a> · <a href="#qa-496c385698250dff">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:tcab" data-paper-title="Fast A/B/n Testing: Exact Multi-Policy Comparison via Tree-Coupled Feedback Sharing" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Fast A/B/n Testing: Exact Multi-Policy Comparison via Tree-Coupled Feedback Sharing 基础模型 New York University 2026-08-13 用最大耦合和最小生成树共享相同决策的反馈，同时保持每个自适应策略的边际轨迹分布不变。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 independent A/B/n feedback，实验组为 tcab；单 seed 变化为 +0.00% 个百分点。  评测基础设施 在线实验 基础模型 能力证据：评测采样、读出与可靠性 TCAB 为什么希望多个自适应策略共享一次真实反馈？ 分别运行A/B/n可能为相同上下文与决策重复付出反馈成本。方法用耦合组织策略选择，在保持各策略边际轨迹分布的条件下复用可共享反馈，减少重复查询。 示意：两策略在同一状态都选同一动作，可以考虑一次环境反馈供两者对应更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<span id="paper-foundation-models-tcab-036a095f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0b3ed7d3bbc398fd">TCAB 为什么希望多个自适应策略共享一次真实反馈？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atcab">Fast A/B/n Testing: Exact Multi-Policy Comparison via Tree-Coupled Feedback Sharing</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · New York University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分别运行A/B/n可能为相同上下文与决策重复付出反馈成本。方法用耦合组织策略选择，在保持各策略边际轨迹分布的条件下复用可共享反馈，减少重复查询。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两策略在同一状态都选同一动作，可以考虑一次环境反馈供两者对应更新。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.12831">原论文</a> · <a href="../../../../reproductions/2608.12831-tcab/">实现解读</a> · <a href="#qa-0b3ed7d3bbc398fd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:tcab" data-paper-title="Fast A/B/n Testing: Exact Multi-Policy Comparison via Tree-Coupled Feedback Sharing" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Fast A/B/n Testing: Exact Multi-Policy Comparison via Tree-Coupled Feedback Sharing 基础模型 New York University 2026-08-13 用最大耦合和最小生成树共享相同决策的反馈，同时保持每个自适应策略的边际轨迹分布不变。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 independent A/B/n feedback，实验组为 tcab；单 seed 变化为 +0.00% 个百分点。  评测基础设施 在线实验 基础模型 能力证据：评测采样、读出与可靠性 TCAB为什么要求完整上下文与动作都匹配，不能只因两策略选了同一动作就共享反馈？ 同一动作在不同用户或候选集合下可能有不同结果，单看动作相同会改变反馈分布。树上最大耦合匹配完整上下文动作对，才可共享条件奖励并保持各策略单独运行的边际轨迹分布。策略间刻意相关而非独立，省查询也不等于任意联合设计的全局最优。 例如两策略都点同一商品，但用户状态不同，不能复用一次点击；只有完整情境与动作匹配，才能在相应奖励模型假设下共享反馈。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-31a085596f880eba">TCAB为什么要求完整上下文与动作都匹配，不能只因两策略选了同一动作就共享反馈？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atcab">Fast A/B/n Testing: Exact Multi-Policy Comparison via Tree-Coupled Feedback Sharing</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · New York University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一动作在不同用户或候选集合下可能有不同结果，单看动作相同会改变反馈分布。树上最大耦合匹配完整上下文动作对，才可共享条件奖励并保持各策略单独运行的边际轨迹分布。策略间刻意相关而非独立，省查询也不等于任意联合设计的全局最优。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两策略都点同一商品，但用户状态不同，不能复用一次点击；只有完整情境与动作匹配，才能在相应奖励模型假设下共享反馈。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.12831">原论文</a> · <a href="../../../../reproductions/2608.12831-tcab/">实现解读</a> · <a href="#qa-31a085596f880eba">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:tcab" data-paper-title="Fast A/B/n Testing: Exact Multi-Policy Comparison via Tree-Coupled Feedback Sharing" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Fast A/B/n Testing: Exact Multi-Policy Comparison via Tree-Coupled Feedback Sharing 基础模型 New York University 2026-08-13 用最大耦合和最小生成树共享相同决策的反馈，同时保持每个自适应策略的边际轨迹分布不变。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 independent A/B/n feedback，实验组为 tcab；单 seed 变化为 +0.00% 个百分点。  评测基础设施 在线实验 基础模型 能力证据：评测采样、读出与可靠性 耦合后的策略轨迹彼此相关，是否等于每个策略自己的分布被改变？ 不一定。耦合可以改变联合相关性，同时保持各策略各自的边际分布；这正是共享反馈需保留的条件。只检查最终准确率相同，不能替代边际轨迹与自适应更新合同。 示意：两个随机选择可以更常同时相同，但每个单独看仍遵循原来的选择概率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-6c5e5b73ef108829">耦合后的策略轨迹彼此相关，是否等于每个策略自己的分布被改变？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atcab">Fast A/B/n Testing: Exact Multi-Policy Comparison via Tree-Coupled Feedback Sharing</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · New York University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不一定。耦合可以改变联合相关性，同时保持各策略各自的边际分布；这正是共享反馈需保留的条件。只检查最终准确率相同，不能替代边际轨迹与自适应更新合同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个随机选择可以更常同时相同，但每个单独看仍遵循原来的选择概率。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.12831">原论文</a> · <a href="../../../../reproductions/2608.12831-tcab/">实现解读</a> · <a href="#qa-6c5e5b73ef108829">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:tcab" data-paper-title="Fast A/B/n Testing: Exact Multi-Policy Comparison via Tree-Coupled Feedback Sharing" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Fast A/B/n Testing: Exact Multi-Policy Comparison via Tree-Coupled Feedback Sharing 基础模型 New York University 2026-08-13 用最大耦合和最小生成树共享相同决策的反馈，同时保持每个自适应策略的边际轨迹分布不变。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 independent A/B/n feedback，实验组为 tcab；单 seed 变化为 +0.00% 个百分点。  评测基础设施 在线实验 基础模型 能力证据：评测采样、读出与可靠性 TCAB 记录反馈节省时，为什么不能只统计“动作字符串相同”的次数？ 反馈可共享还取决于完整上下文与策略状态条件；相同动作在不同环境下可能得到不同结果。应对照真实共享调用与树边差异计数，不能把任意同名动作当成一次可合并观测。 示意：不同用户都点击推荐动作A，反馈不因此是同一条可复用样本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-35f6f43d12979124">TCAB 记录反馈节省时，为什么不能只统计“动作字符串相同”的次数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atcab">Fast A/B/n Testing: Exact Multi-Policy Comparison via Tree-Coupled Feedback Sharing</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · New York University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>反馈可共享还取决于完整上下文与策略状态条件；相同动作在不同环境下可能得到不同结果。应对照真实共享调用与树边差异计数，不能把任意同名动作当成一次可合并观测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>不同用户都点击推荐动作A，反馈不因此是同一条可复用样本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.12831">原论文</a> · <a href="../../../../reproductions/2608.12831-tcab/">实现解读</a> · <a href="#qa-35f6f43d12979124">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:activation-model-scanner" data-paper-title="Detecting Safety Training Modification in Language Models via Activation Analysis" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Detecting Safety Training Modification in Language Models via Activation Analysis 基础模型 Google Cloud 2026-08-06 通过三个安全相关概念的对照输入，寻找中层激活的类别分离与方向；第一层检查分离程度，第二层与同架构基线比较方向和漂移。该结构信号存在明确盲区，不能替代行为安全评测。核心见§IV，代码约定核对固定上游 extractor.py。 十四模型、多权重族及行为生成的完整campaign成本过高，不复现（审查 DONE） GPU回执只支持真实checkpoint诊断，不是安全能力认证。实现最后token提取、层扫描、差分方向、分离度、两层检测及独立数值测试。固定官方48对输入经静态AST核对，与原始 concepts.py 全部相同；保留Google版权及Apache许可全文，JSON转换新增来源说明但未修改输入对文字，不执行上游代码、不执行输入文字、不生成任何回答。  评测与可靠性 激活安全结构诊断 基础模型 能力证据：评测采样、读出与可靠性 AMS 为什么用对照输入的激活差异检查模型修改？ 它先找安全相关概念在中层激活中的分离方向，再与同架构基线比较方向和漂移，提供结构诊断信号。它不生成行为答案，也无法用结构阈值替代行为安全评测。 示意：两个概念在某层容易分开，仍不能据此保证所有相关真实请求都处理正确。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<span id="paper-foundation-models-activation-model-scanner-171bac1e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2c950ffb6691c1f4">AMS 为什么用对照输入的激活差异检查模型修改？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aactivation-model-scanner">Detecting Safety Training Modification in Language Models via Activation Analysis</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它先找安全相关概念在中层激活中的分离方向，再与同架构基线比较方向和漂移，提供结构诊断信号。它不生成行为答案，也无法用结构阈值替代行为安全评测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个概念在某层容易分开，仍不能据此保证所有相关真实请求都处理正确。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05578">原论文</a> · <a href="../../../../foundation-models/2608.05578-activation-model-scanner/">实现解读</a> · <a href="#qa-2c950ffb6691c1f4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:activation-model-scanner" data-paper-title="Detecting Safety Training Modification in Language Models via Activation Analysis" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Detecting Safety Training Modification in Language Models via Activation Analysis 基础模型 Google Cloud 2026-08-06 通过三个安全相关概念的对照输入，寻找中层激活的类别分离与方向；第一层检查分离程度，第二层与同架构基线比较方向和漂移。该结构信号存在明确盲区，不能替代行为安全评测。核心见§IV，代码约定核对固定上游 extractor.py。 十四模型、多权重族及行为生成的完整campaign成本过高，不复现（审查 DONE） GPU回执只支持真实checkpoint诊断，不是安全能力认证。实现最后token提取、层扫描、差分方向、分离度、两层检测及独立数值测试。固定官方48对输入经静态AST核对，与原始 concepts.py 全部相同；保留Google版权及Apache许可全文，JSON转换新增来源说明但未修改输入对文字，不执行上游代码、不执行输入文字、不生成任何回答。  评测与可靠性 激活安全结构诊断 基础模型 能力证据：评测采样、读出与可靠性 AMS的激活方向分离通过阈值，为什么不能据此宣布模型行为安全？ 对照输入的中层激活方向检验结构分离，再与同架构基线比较方向和漂移，可作为安全训练修改的线索。阈值只对应指定协议，方向分离与真实行为之间仍有盲区；层号、方差定义和基线一致性都会影响结果。组件诊断不能替代独立行为安全评测。 例如模型能把安全与风险概念分开表示，却仍可能在特定上下文给出不当回答；可分离方向说明内部信号存在，不证明所有输出可靠。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-2aacee6d37ba8428">AMS的激活方向分离通过阈值，为什么不能据此宣布模型行为安全？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aactivation-model-scanner">Detecting Safety Training Modification in Language Models via Activation Analysis</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>对照输入的中层激活方向检验结构分离，再与同架构基线比较方向和漂移，可作为安全训练修改的线索。阈值只对应指定协议，方向分离与真实行为之间仍有盲区；层号、方差定义和基线一致性都会影响结果。组件诊断不能替代独立行为安全评测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型能把安全与风险概念分开表示，却仍可能在特定上下文给出不当回答；可分离方向说明内部信号存在，不证明所有输出可靠。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05578">原论文</a> · <a href="../../../../foundation-models/2608.05578-activation-model-scanner/">实现解读</a> · <a href="#qa-2aacee6d37ba8428">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:activation-model-scanner" data-paper-title="Detecting Safety Training Modification in Language Models via Activation Analysis" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Detecting Safety Training Modification in Language Models via Activation Analysis 基础模型 Google Cloud 2026-08-06 通过三个安全相关概念的对照输入，寻找中层激活的类别分离与方向；第一层检查分离程度，第二层与同架构基线比较方向和漂移。该结构信号存在明确盲区，不能替代行为安全评测。核心见§IV，代码约定核对固定上游 extractor.py。 十四模型、多权重族及行为生成的完整campaign成本过高，不复现（审查 DONE） GPU回执只支持真实checkpoint诊断，不是安全能力认证。实现最后token提取、层扫描、差分方向、分离度、两层检测及独立数值测试。固定官方48对输入经静态AST核对，与原始 concepts.py 全部相同；保留Google版权及Apache许可全文，JSON转换新增来源说明但未修改输入对文字，不执行上游代码、不执行输入文字、不生成任何回答。  评测与可靠性 激活安全结构诊断 基础模型 能力证据：评测采样、读出与可靠性 AMS Tier1 分离度与 Tier2 基线方向比较，分别回答什么问题？ Tier1看正负概念投影是否分离，Tier2比较同层同维基线的方向一致性和相对漂移。一个模型内部很可分，不等于它与基线保持相同方向或行为。 示意：两组投影分得很开，但方向可能相对原模型翻转，两个tier可给不同信号。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-bc23a004bfa13d4a">AMS Tier1 分离度与 Tier2 基线方向比较，分别回答什么问题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aactivation-model-scanner">Detecting Safety Training Modification in Language Models via Activation Analysis</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Tier1看正负概念投影是否分离，Tier2比较同层同维基线的方向一致性和相对漂移。一个模型内部很可分，不等于它与基线保持相同方向或行为。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两组投影分得很开，但方向可能相对原模型翻转，两个tier可给不同信号。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05578">原论文</a> · <a href="../../../../foundation-models/2608.05578-activation-model-scanner/">实现解读</a> · <a href="#qa-bc23a004bfa13d4a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:activation-model-scanner" data-paper-title="Detecting Safety Training Modification in Language Models via Activation Analysis" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Detecting Safety Training Modification in Language Models via Activation Analysis 基础模型 Google Cloud 2026-08-06 通过三个安全相关概念的对照输入，寻找中层激活的类别分离与方向；第一层检查分离程度，第二层与同架构基线比较方向和漂移。该结构信号存在明确盲区，不能替代行为安全评测。核心见§IV，代码约定核对固定上游 extractor.py。 十四模型、多权重族及行为生成的完整campaign成本过高，不复现（审查 DONE） GPU回执只支持真实checkpoint诊断，不是安全能力认证。实现最后token提取、层扫描、差分方向、分离度、两层检测及独立数值测试。固定官方48对输入经静态AST核对，与原始 concepts.py 全部相同；保留Google版权及Apache许可全文，JSON转换新增来源说明但未修改输入对文字，不执行上游代码、不执行输入文字、不生成任何回答。  评测与可靠性 激活安全结构诊断 基础模型 能力证据：评测采样、读出与可靠性 从 HuggingFace hidden_states 取 AMS 扫描层时，为什么要加1？ 文档block hooks从0计数，而hidden_states[0]是embedding，故block_id对应hidden_states[block_id+1]。还需取最后真实token，并按固定上游population variance与严格阈值边界计算。 示意：报告block9应读取hidden_states[10]，不能把embedding当作第一个block输出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-00d402cba51d2174">从 HuggingFace hidden_states 取 AMS 扫描层时，为什么要加1？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aactivation-model-scanner">Detecting Safety Training Modification in Language Models via Activation Analysis</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档block hooks从0计数，而hidden_states[0]是embedding，故block_id对应hidden_states[block_id+1]。还需取最后真实token，并按固定上游population variance与严格阈值边界计算。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>报告block9应读取hidden_states[10]，不能把embedding当作第一个block输出。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05578">原论文</a> · <a href="../../../../foundation-models/2608.05578-activation-model-scanner/">实现解读</a> · <a href="#qa-00d402cba51d2174">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:cross-lingual-exploration" data-paper-title="Cross-Lingual Exploration for Parametric Knowledge" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Cross-Lingual Exploration for Parametric Knowledge 基础模型 The Hebrew University of Jerusalem 2026-06-23 Sec.3.1–4.4与Appendix C/E：完整提示保持原问题语言，majority/minority-aware实际使用语言模型提示聚合而非简单字符串计数，语义正确性和跨语言一致性也由Gemini判定。把counter或字符串翻译器当主模型会破坏核心；本轮不造heuristic组件。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。状态：仅文献与成本收录，没有可执行能力adapter，不以heuristic冒充核心模型。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本轮不提供可运行模型、loss包装或伪测试。库里已有通用KL/RL/统计工具并不构成本文核心流程；原文语义模型、API多轮生成或大规模训练不能用手工规则替换。仅保存经过核验的方法、资源、源码状态与原图，终态为 not_reproduced_high_cost。后续不得自动移回待训练队列。  多语言推理与评估 参数知识探索与聚合 基础模型 能力证据：评测采样、读出与可靠性 跨语言探索为什么会对同一个知识问题走多条语言路径？ 模型参数中的知识在不同语言表达下可能呈现不同可访问性，方法通过多语探索再聚合语义回答。它不是仅把同一个字符串翻译多遍，也不是多数票天然正确。 示意：不同语言路径给出不同表述，需要判断它们是否在语义上指向同一实体。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<span id="paper-foundation-models-cross-lingual-exploration-96009007" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-cc3fd0b5d67ab87f">跨语言探索为什么会对同一个知识问题走多条语言路径？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Across-lingual-exploration">Cross-Lingual Exploration for Parametric Knowledge</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hebrew University of Jerusalem</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>模型参数中的知识在不同语言表达下可能呈现不同可访问性，方法通过多语探索再聚合语义回答。它不是仅把同一个字符串翻译多遍，也不是多数票天然正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>不同语言路径给出不同表述，需要判断它们是否在语义上指向同一实体。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.24579v1">原论文</a> · <a href="../../../../foundation-models/2606.24579-cross-lingual-exploration/">实现解读</a> · <a href="#qa-cc3fd0b5d67ab87f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:cross-lingual-exploration" data-paper-title="Cross-Lingual Exploration for Parametric Knowledge" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Cross-Lingual Exploration for Parametric Knowledge 基础模型 The Hebrew University of Jerusalem 2026-06-23 Sec.3.1–4.4与Appendix C/E：完整提示保持原问题语言，majority/minority-aware实际使用语言模型提示聚合而非简单字符串计数，语义正确性和跨语言一致性也由Gemini判定。把counter或字符串翻译器当主模型会破坏核心；本轮不造heuristic组件。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。状态：仅文献与成本收录，没有可执行能力adapter，不以heuristic冒充核心模型。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本轮不提供可运行模型、loss包装或伪测试。库里已有通用KL/RL/统计工具并不构成本文核心流程；原文语义模型、API多轮生成或大规模训练不能用手工规则替换。仅保存经过核验的方法、资源、源码状态与原图，终态为 not_reproduced_high_cost。后续不得自动移回待训练队列。  多语言推理与评估 参数知识探索与聚合 基础模型 能力证据：评测采样、读出与可靠性 跨语言探索为什么不能用字符串多数票代替语义聚合，还要计入聚合成本？ 不同语言路径可能用不同说法表达同一事实，字符串计数会把等义答案拆开，也可能把相似错误误并。原方法由语言模型进行多数与少数感知聚合，语义正确性及跨语言一致性另行判断。所有路径与聚合词元都属预算，本地只有文献记录，未实现语义模块。 例如两条路径分别回答同一城市的不同语言名称，应先判断是否指同一实体；不能把拼写不同当分歧，再只计算最短一条路径成本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-51de139df064f40c">跨语言探索为什么不能用字符串多数票代替语义聚合，还要计入聚合成本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Across-lingual-exploration">Cross-Lingual Exploration for Parametric Knowledge</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hebrew University of Jerusalem</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同语言路径可能用不同说法表达同一事实，字符串计数会把等义答案拆开，也可能把相似错误误并。原方法由语言模型进行多数与少数感知聚合，语义正确性及跨语言一致性另行判断。所有路径与聚合词元都属预算，本地只有文献记录，未实现语义模块。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两条路径分别回答同一城市的不同语言名称，应先判断是否指同一实体；不能把拼写不同当分歧，再只计算最短一条路径成本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.24579v1">原论文</a> · <a href="../../../../foundation-models/2606.24579-cross-lingual-exploration/">实现解读</a> · <a href="#qa-51de139df064f40c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:cross-lingual-exploration" data-paper-title="Cross-Lingual Exploration for Parametric Knowledge" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Cross-Lingual Exploration for Parametric Knowledge 基础模型 The Hebrew University of Jerusalem 2026-06-23 Sec.3.1–4.4与Appendix C/E：完整提示保持原问题语言，majority/minority-aware实际使用语言模型提示聚合而非简单字符串计数，语义正确性和跨语言一致性也由Gemini判定。把counter或字符串翻译器当主模型会破坏核心；本轮不造heuristic组件。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。状态：仅文献与成本收录，没有可执行能力adapter，不以heuristic冒充核心模型。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本轮不提供可运行模型、loss包装或伪测试。库里已有通用KL/RL/统计工具并不构成本文核心流程；原文语义模型、API多轮生成或大规模训练不能用手工规则替换。仅保存经过核验的方法、资源、源码状态与原图，终态为 not_reproduced_high_cost。后续不得自动移回待训练队列。  多语言推理与评估 参数知识探索与聚合 基础模型 能力证据：评测采样、读出与可靠性 语义模型聚合与字符串 counter 多数票，为什么不能互相充当实现？ 相同意思可有不同字面表达，相同字符串也可能语境不同；原文使用语言模型提示完成majority/minority-aware聚合及语义判定。字符串计数会替换定义性语义模块。 示意：“United States”与“USA”可能同义，纯字符串计数却会分成两个候选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-730b132540b80efd">语义模型聚合与字符串 counter 多数票，为什么不能互相充当实现？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Across-lingual-exploration">Cross-Lingual Exploration for Parametric Knowledge</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hebrew University of Jerusalem</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相同意思可有不同字面表达，相同字符串也可能语境不同；原文使用语言模型提示完成majority/minority-aware聚合及语义判定。字符串计数会替换定义性语义模块。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>“United States”与“USA”可能同义，纯字符串计数却会分成两个候选。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.24579v1">原论文</a> · <a href="../../../../foundation-models/2606.24579-cross-lingual-exploration/">实现解读</a> · <a href="#qa-730b132540b80efd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:cross-lingual-exploration" data-paper-title="Cross-Lingual Exploration for Parametric Knowledge" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Cross-Lingual Exploration for Parametric Knowledge 基础模型 The Hebrew University of Jerusalem 2026-06-23 Sec.3.1–4.4与Appendix C/E：完整提示保持原问题语言，majority/minority-aware实际使用语言模型提示聚合而非简单字符串计数，语义正确性和跨语言一致性也由Gemini判定。把counter或字符串翻译器当主模型会破坏核心；本轮不造heuristic组件。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。状态：仅文献与成本收录，没有可执行能力adapter，不以heuristic冒充核心模型。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本轮不提供可运行模型、loss包装或伪测试。库里已有通用KL/RL/统计工具并不构成本文核心流程；原文语义模型、API多轮生成或大规模训练不能用手工规则替换。仅保存经过核验的方法、资源、源码状态与原图，终态为 not_reproduced_high_cost。后续不得自动移回待训练队列。  多语言推理与评估 参数知识探索与聚合 基础模型 能力证据：评测采样、读出与可靠性 计算跨语言探索预算时，为什么不能只数各路径的生成 token？ 文档预算还包含路径输入以及聚合模型token，完整实验也用模型进行语义正确性与一致性判断。漏掉聚合成本会失真；当前没有运行这些API流程，也不提供启发式替代模型。 示意：十条探索很短，但一次长上下文聚合仍可能消耗大量输入token。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-023dadc002ad7698">计算跨语言探索预算时，为什么不能只数各路径的生成 token？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Across-lingual-exploration">Cross-Lingual Exploration for Parametric Knowledge</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hebrew University of Jerusalem</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档预算还包含路径输入以及聚合模型token，完整实验也用模型进行语义正确性与一致性判断。漏掉聚合成本会失真；当前没有运行这些API流程，也不提供启发式替代模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>十条探索很短，但一次长上下文聚合仍可能消耗大量输入token。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.24579v1">原论文</a> · <a href="../../../../foundation-models/2606.24579-cross-lingual-exploration/">实现解读</a> · <a href="#qa-023dadc002ad7698">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:xlgobench" data-paper-title="XLGoBench: Detecting cross-lingual skill gaps with algorithmic tasks" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="XLGoBench: Detecting cross-lingual skill gaps with algorithmic tasks 基础模型 Google DeepMind 2026-05-29 固定v1 Section2+AppendixC：SLT财富/系数整数−9..9并jumbled chain；DSA状态/动作数相同；PrDSA15动作、传播完整状态概率、top8集合顺序无关；GraphSP唯一最短路（本地rho0 backbone+bypass固定例）；T-RankHamiltonian DAG+transitive edges、nodes:edges1:3。callback只收task/problem白名单深拷贝，score完整JSON，无LLMjudge。 成本过高，不复现（审查 DONE）。本地仅5任务结构化诊断、没有代造已验证翻译或跨语言accuracy。原文4模型×5算法×7语言×20复杂度×每级50题，包含frontierAPI和Gemma31B，另有重复/置信区间拟合。完整矩阵和人工验证翻译不跑；本地仅5任务结构化诊断、没有代造已验证翻译或跨语言accuracy。只交付结构化小题、五个精确scorer与gold隔离接口。没有下载Zenodo补充包，不复制其模板，不自动翻译成七语后声称已人工校验；也未实现完整复杂度扫描、gamma/SMD置信区间拟合或任何LLM能力比较。  跨语言评测 算法推理与评测隔离 基础模型 能力证据：评测采样、读出与可靠性 XLGoBench 为什么用有确定性算法答案的任务测跨语言差距？ 受控算法问题可明确难度结构和正确答案，减少开放生成judge的歧义，再在不同语言表达下比较模型表现。它仍需真正运行模型和验证语言版本，不能只凭scorer存在就报告能力。 示意：同一状态转移题换语言表达后，答案仍可由同一确定算法计算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<span id="paper-foundation-models-xlgobench-677fa08c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e970d2cec3e9d35d">XLGoBench 为什么用有确定性算法答案的任务测跨语言差距？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Axlgobench">XLGoBench: Detecting cross-lingual skill gaps with algorithmic tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>受控算法问题可明确难度结构和正确答案，减少开放生成judge的歧义，再在不同语言表达下比较模型表现。它仍需真正运行模型和验证语言版本，不能只凭scorer存在就报告能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一状态转移题换语言表达后，答案仍可由同一确定算法计算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.30788v1">原论文</a> · <a href="../../../../foundation-models/2605.30788-xlgobench/">实现解读</a> · <a href="#qa-e970d2cec3e9d35d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:xlgobench" data-paper-title="XLGoBench: Detecting cross-lingual skill gaps with algorithmic tasks" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="XLGoBench: Detecting cross-lingual skill gaps with algorithmic tasks 基础模型 Google DeepMind 2026-05-29 固定v1 Section2+AppendixC：SLT财富/系数整数−9..9并jumbled chain；DSA状态/动作数相同；PrDSA15动作、传播完整状态概率、top8集合顺序无关；GraphSP唯一最短路（本地rho0 backbone+bypass固定例）；T-RankHamiltonian DAG+transitive edges、nodes:edges1:3。callback只收task/problem白名单深拷贝，score完整JSON，无LLMjudge。 成本过高，不复现（审查 DONE）。本地仅5任务结构化诊断、没有代造已验证翻译或跨语言accuracy。原文4模型×5算法×7语言×20复杂度×每级50题，包含frontierAPI和Gemma31B，另有重复/置信区间拟合。完整矩阵和人工验证翻译不跑；本地仅5任务结构化诊断、没有代造已验证翻译或跨语言accuracy。只交付结构化小题、五个精确scorer与gold隔离接口。没有下载Zenodo补充包，不复制其模板，不自动翻译成七语后声称已人工校验；也未实现完整复杂度扫描、gamma/SMD置信区间拟合或任何LLM能力比较。  跨语言评测 算法推理与评测隔离 基础模型 能力证据：评测采样、读出与可靠性 XLGoBench有确定性算法答案，为什么本地小实例通过仍不能证明跨语言能力差距？ 算法评分可排除主观评审差异，任务复杂度与语言变化仍需真实模型在经过验证的翻译上生成结果。局部生成器只覆盖指定结构范围，不能冒充全噪声或全难度矩阵。金标只在评分端计算，预测回调只接收公开题目；本地五任务诊断没有跨语言准确率证据。 例如同一图问题可由算法核验最短路，但用中文和另一语言描述是否同义还需审核；只让内部求解器答对一张小图，并未测到语言影响。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-40641ea146f76b91">XLGoBench有确定性算法答案，为什么本地小实例通过仍不能证明跨语言能力差距？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Axlgobench">XLGoBench: Detecting cross-lingual skill gaps with algorithmic tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>算法评分可排除主观评审差异，任务复杂度与语言变化仍需真实模型在经过验证的翻译上生成结果。局部生成器只覆盖指定结构范围，不能冒充全噪声或全难度矩阵。金标只在评分端计算，预测回调只接收公开题目；本地五任务诊断没有跨语言准确率证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一图问题可由算法核验最短路，但用中文和另一语言描述是否同义还需审核；只让内部求解器答对一张小图，并未测到语言影响。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.30788v1">原论文</a> · <a href="../../../../foundation-models/2605.30788-xlgobench/">实现解读</a> · <a href="#qa-40641ea146f76b91">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:xlgobench" data-paper-title="XLGoBench: Detecting cross-lingual skill gaps with algorithmic tasks" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="XLGoBench: Detecting cross-lingual skill gaps with algorithmic tasks 基础模型 Google DeepMind 2026-05-29 固定v1 Section2+AppendixC：SLT财富/系数整数−9..9并jumbled chain；DSA状态/动作数相同；PrDSA15动作、传播完整状态概率、top8集合顺序无关；GraphSP唯一最短路（本地rho0 backbone+bypass固定例）；T-RankHamiltonian DAG+transitive edges、nodes:edges1:3。callback只收task/problem白名单深拷贝，score完整JSON，无LLMjudge。 成本过高，不复现（审查 DONE）。本地仅5任务结构化诊断、没有代造已验证翻译或跨语言accuracy。原文4模型×5算法×7语言×20复杂度×每级50题，包含frontierAPI和Gemma31B，另有重复/置信区间拟合。完整矩阵和人工验证翻译不跑；本地仅5任务结构化诊断、没有代造已验证翻译或跨语言accuracy。只交付结构化小题、五个精确scorer与gold隔离接口。没有下载Zenodo补充包，不复制其模板，不自动翻译成七语后声称已人工校验；也未实现完整复杂度扫描、gamma/SMD置信区间拟合或任何LLM能力比较。  跨语言评测 算法推理与评测隔离 基础模型 能力证据：评测采样、读出与可靠性 算法 scorer 的正确性，与模型跨语言泛化结果是同一份证据吗？ 不是。scorer正确说明给定预测可被按约定评价；泛化比较还需要各语言真实输入、模型输出、复杂度扫描与统计。小实例通过不能替代完整七语矩阵或人工校验翻译。 示意：最短路程序能算对12节点题，不说明某语言的LLM也能稳定答对它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-daca851c3385f112">算法 scorer 的正确性，与模型跨语言泛化结果是同一份证据吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Axlgobench">XLGoBench: Detecting cross-lingual skill gaps with algorithmic tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。scorer正确说明给定预测可被按约定评价；泛化比较还需要各语言真实输入、模型输出、复杂度扫描与统计。小实例通过不能替代完整七语矩阵或人工校验翻译。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>最短路程序能算对12节点题，不说明某语言的LLM也能稳定答对它。</p>
<p class="ar-learning-sources">依据：本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.30788v1">原论文</a> · <a href="../../../../foundation-models/2605.30788-xlgobench/">实现解读</a> · <a href="#qa-daca851c3385f112">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:xlgobench" data-paper-title="XLGoBench: Detecting cross-lingual skill gaps with algorithmic tasks" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="XLGoBench: Detecting cross-lingual skill gaps with algorithmic tasks 基础模型 Google DeepMind 2026-05-29 固定v1 Section2+AppendixC：SLT财富/系数整数−9..9并jumbled chain；DSA状态/动作数相同；PrDSA15动作、传播完整状态概率、top8集合顺序无关；GraphSP唯一最短路（本地rho0 backbone+bypass固定例）；T-RankHamiltonian DAG+transitive edges、nodes:edges1:3。callback只收task/problem白名单深拷贝，score完整JSON，无LLMjudge。 成本过高，不复现（审查 DONE）。本地仅5任务结构化诊断、没有代造已验证翻译或跨语言accuracy。原文4模型×5算法×7语言×20复杂度×每级50题，包含frontierAPI和Gemma31B，另有重复/置信区间拟合。完整矩阵和人工验证翻译不跑；本地仅5任务结构化诊断、没有代造已验证翻译或跨语言accuracy。只交付结构化小题、五个精确scorer与gold隔离接口。没有下载Zenodo补充包，不复制其模板，不自动翻译成七语后声称已人工校验；也未实现完整复杂度扫描、gamma/SMD置信区间拟合或任何LLM能力比较。  跨语言评测 算法推理与评测隔离 基础模型 能力证据：评测采样、读出与可靠性 XLGoBench 的 Pr-DSA top8 评分为什么既忽略顺序又拒绝重复？ 目标是完整概率传播得到的top8集合，集合内部顺序不重要，但重复会减少实际覆盖项数，不能以列表长度8掩盖缺项。其它任务也按完整JSON合同评价，不用部分匹配凑通过。 示意：[A,A,B,...]虽有八个条目，实际不同状态不足八个，应被拒绝。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7c3c5ef680fb6a56">XLGoBench 的 Pr-DSA top8 评分为什么既忽略顺序又拒绝重复？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Axlgobench">XLGoBench: Detecting cross-lingual skill gaps with algorithmic tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标是完整概率传播得到的top8集合，集合内部顺序不重要，但重复会减少实际覆盖项数，不能以列表长度8掩盖缺项。其它任务也按完整JSON合同评价，不用部分匹配凑通过。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>[A,A,B,...]虽有八个条目，实际不同状态不足八个，应被拒绝。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.30788v1">原论文</a> · <a href="../../../../foundation-models/2605.30788-xlgobench/">实现解读</a> · <a href="#qa-7c3c5ef680fb6a56">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:proeval" data-paper-title="ProEval: Proactive Failure Discovery and Efficient Performance Estimation for Generative AI Evaluation" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="ProEval: Proactive Failure Discovery and Efficient Performance Estimation for Generative AI Evaluation 基础模型 Google DeepMind 2026-04-25 昂贵模型或评审器不适合每次全量评分。ProEval复用历史模型之间逐题表现的相关性，形成目标模型的概率评分替身；目标分数只在对应题被选中后传入更新。主源：v1 §2.1–2.4 Eq2、5、7、10、12。 完整多基准/API实验成本过高，不复现（审查DONE）；仅4份历史评分数学夹具和4题目标分数；采集器只得到已查询分数，不接受整个隐藏目标数组。独立测试逐候选比较解析方差减少与真正增加一次观测后的方差之差。记录位于metrics/component-cpu-seed42.json，diagnostic_only=true，无真实LLM评价、正式能力或evolve晋级声明。  模型评测 历史分数迁移与主动采样 基础模型 能力证据：评测采样、读出与可靠性 ProEval 为什么复用历史逐题评分来减少新模型评价调用？ 历史模型之间的题目相关性可形成新目标模型的概率评分替身，有限查询逐步更新后验，再估计总体分数及不确定性。它节省实际评分，但估计并不等于已问过全部题。 示意：只查询几题后，用历史相关结构预测其它题，但仍需报告剩余方差。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<span id="paper-foundation-models-proeval-344b21b9" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b5a18b39b2bf1adc">ProEval 为什么复用历史逐题评分来减少新模型评价调用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aproeval">ProEval: Proactive Failure Discovery and Efficient Performance Estimation for Generative AI Evaluation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>历史模型之间的题目相关性可形成新目标模型的概率评分替身，有限查询逐步更新后验，再估计总体分数及不确定性。它节省实际评分，但估计并不等于已问过全部题。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>只查询几题后，用历史相关结构预测其它题，但仍需报告剩余方差。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.23099">原论文</a> · <a href="../../../../foundation-models/2604.23099-proeval/">实现解读</a> · <a href="#qa-b5a18b39b2bf1adc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:proeval" data-paper-title="ProEval: Proactive Failure Discovery and Efficient Performance Estimation for Generative AI Evaluation" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="ProEval: Proactive Failure Discovery and Efficient Performance Estimation for Generative AI Evaluation 基础模型 Google DeepMind 2026-04-25 昂贵模型或评审器不适合每次全量评分。ProEval复用历史模型之间逐题表现的相关性，形成目标模型的概率评分替身；目标分数只在对应题被选中后传入更新。主源：v1 §2.1–2.4 Eq2、5、7、10、12。 完整多基准/API实验成本过高，不复现（审查DONE）；仅4份历史评分数学夹具和4题目标分数；采集器只得到已查询分数，不接受整个隐藏目标数组。独立测试逐候选比较解析方差减少与真正增加一次观测后的方差之差。记录位于metrics/component-cpu-seed42.json，diagnostic_only=true，无真实LLM评价、正式能力或evolve晋级声明。  模型评测 历史分数迁移与主动采样 基础模型 能力证据：评测采样、读出与可靠性 ProEval为什么必须先选题再读取目标模型分数，历史矩阵还要排除目标模型？ 历史模型相关性提供目标表现的先验，只有被主动选中的题才能返回真实目标分数并更新后验。若完整目标列预先参与协方差或选题，便把昂贵评估答案偷渡到替身中。方差缩减衡量估计收益，不保证目标超出历史分布时仍可靠，本地组件也不是全量评审替代证明。 例如先依据旧模型记录选择一道最有信息的题，再调用新模型评分；不能把新模型整列成绩先读入，随后声称只查询少量题就估准总分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-b22fb32d4dcf178a">ProEval为什么必须先选题再读取目标模型分数，历史矩阵还要排除目标模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aproeval">ProEval: Proactive Failure Discovery and Efficient Performance Estimation for Generative AI Evaluation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>历史模型相关性提供目标表现的先验，只有被主动选中的题才能返回真实目标分数并更新后验。若完整目标列预先参与协方差或选题，便把昂贵评估答案偷渡到替身中。方差缩减衡量估计收益，不保证目标超出历史分布时仍可靠，本地组件也不是全量评审替代证明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先依据旧模型记录选择一道最有信息的题，再调用新模型评分；不能把新模型整列成绩先读入，随后声称只查询少量题就估准总分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.23099">原论文</a> · <a href="../../../../foundation-models/2604.23099-proeval/">实现解读</a> · <a href="#qa-b22fb32d4dcf178a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:proeval" data-paper-title="ProEval: Proactive Failure Discovery and Efficient Performance Estimation for Generative AI Evaluation" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="ProEval: Proactive Failure Discovery and Efficient Performance Estimation for Generative AI Evaluation 基础模型 Google DeepMind 2026-04-25 昂贵模型或评审器不适合每次全量评分。ProEval复用历史模型之间逐题表现的相关性，形成目标模型的概率评分替身；目标分数只在对应题被选中后传入更新。主源：v1 §2.1–2.4 Eq2、5、7、10、12。 完整多基准/API实验成本过高，不复现（审查DONE）；仅4份历史评分数学夹具和4题目标分数；采集器只得到已查询分数，不接受整个隐藏目标数组。独立测试逐候选比较解析方差减少与真正增加一次观测后的方差之差。记录位于metrics/component-cpu-seed42.json，diagnostic_only=true，无真实LLM评价、正式能力或evolve晋级声明。  模型评测 历史分数迁移与主动采样 基础模型 能力证据：评测采样、读出与可靠性 BQ 的总体方差减少采集，与直接选择当前均值最低的题有什么不同？ BQ按候选观测对wᵀKw的预期下降选择，关注总体评分不确定性；均值最低关注困难程度。文档失败采集也有自己的候选条件，不能把所有策略都叫“挑最难题”。 示意：某题均值不低，但与许多未问题强相关，查询它可能更能减少总分方差。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-abfb841936daff0f">BQ 的总体方差减少采集，与直接选择当前均值最低的题有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aproeval">ProEval: Proactive Failure Discovery and Efficient Performance Estimation for Generative AI Evaluation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>BQ按候选观测对wᵀKw的预期下降选择，关注总体评分不确定性；均值最低关注困难程度。文档失败采集也有自己的候选条件，不能把所有策略都叫“挑最难题”。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某题均值不低，但与许多未问题强相关，查询它可能更能减少总分方差。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.23099">原论文</a> · <a href="../../../../foundation-models/2604.23099-proeval/">实现解读</a> · <a href="#qa-abfb841936daff0f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:proeval" data-paper-title="ProEval: Proactive Failure Discovery and Efficient Performance Estimation for Generative AI Evaluation" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="ProEval: Proactive Failure Discovery and Efficient Performance Estimation for Generative AI Evaluation 基础模型 Google DeepMind 2026-04-25 昂贵模型或评审器不适合每次全量评分。ProEval复用历史模型之间逐题表现的相关性，形成目标模型的概率评分替身；目标分数只在对应题被选中后传入更新。主源：v1 §2.1–2.4 Eq2、5、7、10、12。 完整多基准/API实验成本过高，不复现（审查DONE）；仅4份历史评分数学夹具和4题目标分数；采集器只得到已查询分数，不接受整个隐藏目标数组。独立测试逐候选比较解析方差减少与真正增加一次观测后的方差之差。记录位于metrics/component-cpu-seed42.json，diagnostic_only=true，无真实LLM评价、正式能力或evolve晋级声明。  模型评测 历史分数迁移与主动采样 基础模型 能力证据：评测采样、读出与可靠性 ProEval 为什么拒绝重复目标观察和历史矩阵里的目标模型 ID？ 重复观测会破坏声明的查询预算与后验更新口径，把目标完整历史放入先验更会泄漏未查询分数。接口只接所选题反馈；至少三份历史记录也只是本地门槛，不自动验证理论条件。 示意：目标模型完整一列已经藏在历史矩阵中，就不能再把省下的查询称为有效迁移。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-9ddb161d95e906b1">ProEval 为什么拒绝重复目标观察和历史矩阵里的目标模型 ID？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aproeval">ProEval: Proactive Failure Discovery and Efficient Performance Estimation for Generative AI Evaluation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>重复观测会破坏声明的查询预算与后验更新口径，把目标完整历史放入先验更会泄漏未查询分数。接口只接所选题反馈；至少三份历史记录也只是本地门槛，不自动验证理论条件。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>目标模型完整一列已经藏在历史矩阵中，就不能再把省下的查询称为有效迁移。</p>
<p class="ar-learning-sources">依据：核心公式、代码映射与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.23099">原论文</a> · <a href="../../../../foundation-models/2604.23099-proeval/">实现解读</a> · <a href="#qa-9ddb161d95e906b1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:fuse-verifiers" data-paper-title="FUSE: Ensembling Verifiers with Zero Labeled Data" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="FUSE: Ensembling Verifiers with Zero Labeled Data 基础模型 Stanford University 2026-04-20 多个验证器并不独立，直接平均可能让相关错误相互放大。FUSE 只读取候选分数矩阵，通过二、三阶矩估计查询条件下的验证器质量，选择能缓解相关性的分数变换，再构造正确后验并优化集成器；真实正确标签只用于独立评估。图按原文 Figure 2 / Algorithm 1 重绘。原始流程图。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。附录 F 的 HLE/IMO 新生成与验证采用 8×H100-80GB，完整生成实验成本过高，不复现（审查 DONE）。但论文明确：读取既有分数的矩阵计算无需 GPU，不能据完整生成规模错误拒绝离线核心。  推理与系统效率 无标签验证器集成 基础模型 能力证据：评测采样、读出与可靠性 FUSE 为什么不满足于把多个验证器分数直接平均？ 相关验证器可能一起犯错，平均会重复计算同一类证据。FUSE从候选分数矩阵估计查询条件质量，选择变换缓解相关性，再构造估计后验训练集成器。 示意：三个几乎一样的验证器一致，不一定比一位独立验证器提供三倍可靠证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<span id="paper-foundation-models-fuse-verifiers-1ae3c639" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0e8d40806e950df8">FUSE 为什么不满足于把多个验证器分数直接平均？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Afuse-verifiers">FUSE: Ensembling Verifiers with Zero Labeled Data</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相关验证器可能一起犯错，平均会重复计算同一类证据。FUSE从候选分数矩阵估计查询条件质量，选择变换缓解相关性，再构造估计后验训练集成器。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三个几乎一样的验证器一致，不一定比一位独立验证器提供三倍可靠证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.18547v1">原论文</a> · <a href="../../../../foundation-models/2604.18547-fuse-verifiers/">实现解读</a> · <a href="#qa-0e8d40806e950df8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:fuse-verifiers" data-paper-title="FUSE: Ensembling Verifiers with Zero Labeled Data" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="FUSE: Ensembling Verifiers with Zero Labeled Data 基础模型 Stanford University 2026-04-20 多个验证器并不独立，直接平均可能让相关错误相互放大。FUSE 只读取候选分数矩阵，通过二、三阶矩估计查询条件下的验证器质量，选择能缓解相关性的分数变换，再构造正确后验并优化集成器；真实正确标签只用于独立评估。图按原文 Figure 2 / Algorithm 1 重绘。原始流程图。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。附录 F 的 HLE/IMO 新生成与验证采用 8×H100-80GB，完整生成实验成本过高，不复现（审查 DONE）。但论文明确：读取既有分数的矩阵计算无需 GPU，不能据完整生成规模错误拒绝离线核心。  推理与系统效率 无标签验证器集成 基础模型 能力证据：评测采样、读出与可靠性 FUSE不用标准答案估计验证器质量，为什么仍不能保证相关验证器越多越可靠？ 无标签矩估计依赖多数优于随机、三元条件独立等可识别假设，并用分数变换缓解相关性后形成估计后验。多个验证器若共享错误，增加数量仍可能重复同一偏差；后验不是金标。真实标签只用于独立评估，直接平均或读答案调权重都不等于实现该方法。 例如三位验证器复制同一错误规则，分数一致不代表答案正确；估计器需要检查信号条件，不能把一致票数直接解释为独立证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-1971a030f622491f">FUSE不用标准答案估计验证器质量，为什么仍不能保证相关验证器越多越可靠？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Afuse-verifiers">FUSE: Ensembling Verifiers with Zero Labeled Data</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>无标签矩估计依赖多数优于随机、三元条件独立等可识别假设，并用分数变换缓解相关性后形成估计后验。多个验证器若共享错误，增加数量仍可能重复同一偏差；后验不是金标。真实标签只用于独立评估，直接平均或读答案调权重都不等于实现该方法。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如三位验证器复制同一错误规则，分数一致不代表答案正确；估计器需要检查信号条件，不能把一致票数直接解释为独立证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.18547v1">原论文</a> · <a href="../../../../foundation-models/2604.18547-fuse-verifiers/">实现解读</a> · <a href="#qa-1971a030f622491f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:fuse-verifiers" data-paper-title="FUSE: Ensembling Verifiers with Zero Labeled Data" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="FUSE: Ensembling Verifiers with Zero Labeled Data 基础模型 Stanford University 2026-04-20 多个验证器并不独立，直接平均可能让相关错误相互放大。FUSE 只读取候选分数矩阵，通过二、三阶矩估计查询条件下的验证器质量，选择能缓解相关性的分数变换，再构造正确后验并优化集成器；真实正确标签只用于独立评估。图按原文 Figure 2 / Algorithm 1 重绘。原始流程图。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。附录 F 的 HLE/IMO 新生成与验证采用 8×H100-80GB，完整生成实验成本过高，不复现（审查 DONE）。但论文明确：读取既有分数的矩阵计算无需 GPU，不能据完整生成规模错误拒绝离线核心。  推理与系统效率 无标签验证器集成 基础模型 能力证据：评测采样、读出与可靠性 FUSE 的矩估计后验，与独立标准答案标签提供的保证相同吗？ 不是。后验依赖多数优于随机、三元条件独立等识别假设，高相关或常量分数可能使估计失效。它是无标签估计，不能把高后验当作真实正确性或安全保证。 示意：所有验证器复制同一种错误规则时，一致性很高也未必能识别真实答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-28aa8f0196230b9c">FUSE 的矩估计后验，与独立标准答案标签提供的保证相同吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Afuse-verifiers">FUSE: Ensembling Verifiers with Zero Labeled Data</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。后验依赖多数优于随机、三元条件独立等识别假设，高相关或常量分数可能使估计失效。它是无标签估计，不能把高后验当作真实正确性或安全保证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>所有验证器复制同一种错误规则时，一致性很高也未必能识别真实答案。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.18547v1">原论文</a> · <a href="../../../../foundation-models/2604.18547-fuse-verifiers/">实现解读</a> · <a href="#qa-28aa8f0196230b9c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:fuse-verifiers" data-paper-title="FUSE: Ensembling Verifiers with Zero Labeled Data" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="FUSE: Ensembling Verifiers with Zero Labeled Data 基础模型 Stanford University 2026-04-20 多个验证器并不独立，直接平均可能让相关错误相互放大。FUSE 只读取候选分数矩阵，通过二、三阶矩估计查询条件下的验证器质量，选择能缓解相关性的分数变换，再构造正确后验并优化集成器；真实正确标签只用于独立评估。图按原文 Figure 2 / Algorithm 1 重绘。原始流程图。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。附录 F 的 HLE/IMO 新生成与验证采用 8×H100-80GB，完整生成实验成本过高，不复现（审查 DONE）。但论文明确：读取既有分数的矩阵计算无需 GPU，不能据完整生成规模错误拒绝离线核心。  推理与系统效率 无标签验证器集成 基础模型 能力证据：评测采样、读出与可靠性 无标签 FUSE 拟合中，标准答案能参与选择分数变换或集成参数吗？ 按文档流程，拟合只读取验证器分数矩阵，真实标签留给独立评估。把Gold用于挑变换再在同一题集报告效果，会破坏无标签学习及独立评价的边界。 示意：先试很多变换并用答案选最好的一个，不能仍宣称选择过程未读取标准答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-025e98a438bb7ffe">无标签 FUSE 拟合中，标准答案能参与选择分数变换或集成参数吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Afuse-verifiers">FUSE: Ensembling Verifiers with Zero Labeled Data</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>按文档流程，拟合只读取验证器分数矩阵，真实标签留给独立评估。把Gold用于挑变换再在同一题集报告效果，会破坏无标签学习及独立评价的边界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先试很多变换并用答案选最好的一个，不能仍宣称选择过程未读取标准答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.18547v1">原论文</a> · <a href="../../../../foundation-models/2604.18547-fuse-verifiers/">实现解读</a> · <a href="#qa-025e98a438bb7ffe">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:combinatorial-watermark" data-paper-title="Detecting Post-generation Edits to Watermarked LLM Outputs via Combinatorial Watermarking" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Detecting Post-generation Edits to Watermarked LLM Outputs via Combinatorial Watermarking 基础模型 University of Minnesota 2025-10-02 固定v1 Section3 Eqs2–5：调用方提供真实secret分区与base logits；bias δ到当前pattern tag后softmax。Iw(t)对所有cyclic phases检查，global mean；local在完整interior t=w−1..T−w平均w个covering windows。全局&gt;=threshold、局部&lt;threshold，阈值需在calibration控制TypeI。binary周期整周期删除可以不可检测，不能承诺完美定位。 成本过高，不复现（审查 DONE）。诊断不加载tokenizer/LLM。完整实验Llama2-7B/OPT1.3B，WikiText多水印强度/模式/1–6token编辑×三种编辑方式，1000条64token、阈值校准及PPL矩阵；原文RTX6000Ada48GB。完整模型数据构造与全矩阵不跑，不编造总耗时；只保留CPU公式和负控。调用方提供vocabulary partition与base logits；CPU实现bias、softmax、cyclic窗口统计和阈值判定，不提供production secret系统或密码安全保证。诊断不加载tokenizer/LLM。  安全与可验证性 文本水印与编辑检测 基础模型 能力证据：评测采样、读出与可靠性 组合水印为什么按周期 pattern 给不同词表分区加偏置？ 生成时按当前tag轻微改变相应分区的logits，使序列出现可统计的周期结构；检测器再检查窗口对任意循环相位的匹配，用于水印与潜在编辑诊断。 示意：AB周期控制偏置分区，检测并不要求观察文本正好从周期第一个位置开始。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<span id="paper-foundation-models-combinatorial-watermark-183aedb0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c09d9ae85d58f347">组合水印为什么按周期 pattern 给不同词表分区加偏置？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Acombinatorial-watermark">Detecting Post-generation Edits to Watermarked LLM Outputs via Combinatorial Watermarking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Minnesota</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>生成时按当前tag轻微改变相应分区的logits，使序列出现可统计的周期结构；检测器再检查窗口对任意循环相位的匹配，用于水印与潜在编辑诊断。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>AB周期控制偏置分区，检测并不要求观察文本正好从周期第一个位置开始。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.01637v1">原论文</a> · <a href="../../../../foundation-models/2510.01637-combinatorial-watermark/">实现解读</a> · <a href="#qa-c09d9ae85d58f347">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:combinatorial-watermark" data-paper-title="Detecting Post-generation Edits to Watermarked LLM Outputs via Combinatorial Watermarking" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Detecting Post-generation Edits to Watermarked LLM Outputs via Combinatorial Watermarking 基础模型 University of Minnesota 2025-10-02 固定v1 Section3 Eqs2–5：调用方提供真实secret分区与base logits；bias δ到当前pattern tag后softmax。Iw(t)对所有cyclic phases检查，global mean；local在完整interior t=w−1..T−w平均w个covering windows。全局&gt;=threshold、局部&lt;threshold，阈值需在calibration控制TypeI。binary周期整周期删除可以不可检测，不能承诺完美定位。 成本过高，不复现（审查 DONE）。诊断不加载tokenizer/LLM。完整实验Llama2-7B/OPT1.3B，WikiText多水印强度/模式/1–6token编辑×三种编辑方式，1000条64token、阈值校准及PPL矩阵；原文RTX6000Ada48GB。完整模型数据构造与全矩阵不跑，不编造总耗时；只保留CPU公式和负控。调用方提供vocabulary partition与base logits；CPU实现bias、softmax、cyclic窗口统计和阈值判定，不提供production secret系统或密码安全保证。诊断不加载tokenizer/LLM。  安全与可验证性 文本水印与编辑检测 基础模型 能力证据：评测采样、读出与可靠性 组合水印检查所有循环相位，为什么仍可能漏掉整周期删除？ 循环相位检测避免位置整体偏移就破坏匹配，但周期结构本身也产生盲区：删除完整周期可能保留相位与局部模式。全局检测与局部编辑提示须用独立校准阈值控制误报，不能把硬模式诊断外推为软水印完美定位。本地未运行完整模型编辑矩阵。 例如周期为红蓝红蓝，删去完整一轮后余下仍与某循环相位吻合；这类编辑可能难以发现，而非把阈值调高就必然解决。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-66b97bbf9772dff1">组合水印检查所有循环相位，为什么仍可能漏掉整周期删除？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Acombinatorial-watermark">Detecting Post-generation Edits to Watermarked LLM Outputs via Combinatorial Watermarking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Minnesota</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>循环相位检测避免位置整体偏移就破坏匹配，但周期结构本身也产生盲区：删除完整周期可能保留相位与局部模式。全局检测与局部编辑提示须用独立校准阈值控制误报，不能把硬模式诊断外推为软水印完美定位。本地未运行完整模型编辑矩阵。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如周期为红蓝红蓝，删去完整一轮后余下仍与某循环相位吻合；这类编辑可能难以发现，而非把阈值调高就必然解决。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.01637v1">原论文</a> · <a href="../../../../foundation-models/2510.01637-combinatorial-watermark/">实现解读</a> · <a href="#qa-66b97bbf9772dff1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:combinatorial-watermark" data-paper-title="Detecting Post-generation Edits to Watermarked LLM Outputs via Combinatorial Watermarking" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Detecting Post-generation Edits to Watermarked LLM Outputs via Combinatorial Watermarking 基础模型 University of Minnesota 2025-10-02 固定v1 Section3 Eqs2–5：调用方提供真实secret分区与base logits；bias δ到当前pattern tag后softmax。Iw(t)对所有cyclic phases检查，global mean；local在完整interior t=w−1..T−w平均w个covering windows。全局&gt;=threshold、局部&lt;threshold，阈值需在calibration控制TypeI。binary周期整周期删除可以不可检测，不能承诺完美定位。 成本过高，不复现（审查 DONE）。诊断不加载tokenizer/LLM。完整实验Llama2-7B/OPT1.3B，WikiText多水印强度/模式/1–6token编辑×三种编辑方式，1000条64token、阈值校准及PPL矩阵；原文RTX6000Ada48GB。完整模型数据构造与全矩阵不跑，不编造总耗时；只保留CPU公式和负控。调用方提供vocabulary partition与base logits；CPU实现bias、softmax、cyclic窗口统计和阈值判定，不提供production secret系统或密码安全保证。诊断不加载tokenizer/LLM。  安全与可验证性 文本水印与编辑检测 基础模型 能力证据：评测采样、读出与可靠性 全局 D 与局部 E(t) 的阈值判定，能互相替代吗？ 全局均值用于判断整段是否有水印，局部覆盖窗口均值用于提示可能编辑位置；统计范围和阈值方向不同。阈值还需独立校准控制误报，不能用硬pattern样例推导软水印安全保证。 示意：整段全局通过，也可能有一小段局部得分低；局部低并不自动精确定位全部编辑。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-9acb87bf75defb5d">全局 D 与局部 E(t) 的阈值判定，能互相替代吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Acombinatorial-watermark">Detecting Post-generation Edits to Watermarked LLM Outputs via Combinatorial Watermarking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Minnesota</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全局均值用于判断整段是否有水印，局部覆盖窗口均值用于提示可能编辑位置；统计范围和阈值方向不同。阈值还需独立校准控制误报，不能用硬pattern样例推导软水印安全保证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>整段全局通过，也可能有一小段局部得分低；局部低并不自动精确定位全部编辑。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.01637v1">原论文</a> · <a href="../../../../foundation-models/2510.01637-combinatorial-watermark/">实现解读</a> · <a href="#qa-9acb87bf75defb5d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:combinatorial-watermark" data-paper-title="Detecting Post-generation Edits to Watermarked LLM Outputs via Combinatorial Watermarking" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Detecting Post-generation Edits to Watermarked LLM Outputs via Combinatorial Watermarking 基础模型 University of Minnesota 2025-10-02 固定v1 Section3 Eqs2–5：调用方提供真实secret分区与base logits；bias δ到当前pattern tag后softmax。Iw(t)对所有cyclic phases检查，global mean；local在完整interior t=w−1..T−w平均w个covering windows。全局&gt;=threshold、局部&lt;threshold，阈值需在calibration控制TypeI。binary周期整周期删除可以不可检测，不能承诺完美定位。 成本过高，不复现（审查 DONE）。诊断不加载tokenizer/LLM。完整实验Llama2-7B/OPT1.3B，WikiText多水印强度/模式/1–6token编辑×三种编辑方式，1000条64token、阈值校准及PPL矩阵；原文RTX6000Ada48GB。完整模型数据构造与全矩阵不跑，不编造总耗时；只保留CPU公式和负控。调用方提供vocabulary partition与base logits；CPU实现bias、softmax、cyclic窗口统计和阈值判定，不提供production secret系统或密码安全保证。诊断不加载tokenizer/LLM。  安全与可验证性 文本水印与编辑检测 基础模型 能力证据：评测采样、读出与可靠性 局部 E(t) 到文本边缘时，能补零并继续按同一检测合同算吗？ 文档只在完整interior t=w−1到T−w定义局部统计，不补零边界、不改分母。还要检查所有循环相位，保留整周期删除的不可检测负控，而非声称所有删除必被发现。 示意：缺少完整覆盖窗口的开头位置，不应因人为补零被误标成编辑。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-cb75a73b696eddd8">局部 E(t) 到文本边缘时，能补零并继续按同一检测合同算吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Acombinatorial-watermark">Detecting Post-generation Edits to Watermarked LLM Outputs via Combinatorial Watermarking</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Minnesota</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档只在完整interior t=w−1到T−w定义局部统计，不补零边界、不改分母。还要检查所有循环相位，保留整周期删除的不可检测负控，而非声称所有删除必被发现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>缺少完整覆盖窗口的开头位置，不应因人为补零被误标成编辑。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.01637v1">原论文</a> · <a href="../../../../foundation-models/2510.01637-combinatorial-watermark/">实现解读</a> · <a href="#qa-cb75a73b696eddd8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mechanistic-etm" data-paper-title="Model Directions, Not Words: Mechanistic Topic Models Using Sparse Autoencoders" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Model Directions, Not Words: Mechanistic Topic Models Using Sparse Autoencoders 基础模型 Columbia University 2025-07-31 固定v3 Section4.2.2 Eqs9–13：δN(0,I)、θ=softmaxδ、βk=sigmoid(W_in vk+b)，W_in为冻结SAE ENCODER，不是decoder；每个feature计数Binomial(Ntokens,[θβ]i)。variational q拓扑与MC noise显式外传，优化NLL+analytic Gaussian KL。Eqs16–19仅steering才用独立SAE DECODER列方向加权单位化，再移除已有parallel分量、注入指定strength。 成本过高，不复现（审查 DONE）。Gemma2-9B、layer10的16K GemmaScope SAE、8数据集、LDA/ETM/BERTopic多变种及Bayesian优化，GPT4.1 topic judge每数据集2800成对比较和额外coherence/steering评测。完整矩阵超单卡短时预算；不下载LLM/SAE或调API，不编造未报告总GPU小时。MechanisticETM接冻结SAE encoder_weights与真实过滤后的activation counts；steering函数单独接不同的decoder方向和decoder bias。  可解释性 SAE主题模型与控制 基础模型 能力证据：评测采样、读出与可靠性 Mechanistic ETM 为什么以 SAE feature 而非词项作为主题观察？ 它用稀疏激活方向描述文档概念，主题经冻结SAE encoder形成feature概率，再拟合文档比例与feature计数。可解释对象因此是模型内部方向，不只是高频词列表。 示意：不同表面词可激活相近概念feature，而同一词在不同语境中也未必代表同一主题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<span id="paper-foundation-models-mechanistic-etm-c8c4eb6c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ccc999e66bb8be20">Mechanistic ETM 为什么以 SAE feature 而非词项作为主题观察？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amechanistic-etm">Model Directions, Not Words: Mechanistic Topic Models Using Sparse Autoencoders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Columbia University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它用稀疏激活方向描述文档概念，主题经冻结SAE encoder形成feature概率，再拟合文档比例与feature计数。可解释对象因此是模型内部方向，不只是高频词列表。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>不同表面词可激活相近概念feature，而同一词在不同语境中也未必代表同一主题。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.23220v1">原论文</a> · <a href="../../../../foundation-models/2507.23220-mechanistic-etm/">实现解读</a> · <a href="#qa-ccc999e66bb8be20">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mechanistic-etm" data-paper-title="Model Directions, Not Words: Mechanistic Topic Models Using Sparse Autoencoders" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Model Directions, Not Words: Mechanistic Topic Models Using Sparse Autoencoders 基础模型 Columbia University 2025-07-31 固定v3 Section4.2.2 Eqs9–13：δN(0,I)、θ=softmaxδ、βk=sigmoid(W_in vk+b)，W_in为冻结SAE ENCODER，不是decoder；每个feature计数Binomial(Ntokens,[θβ]i)。variational q拓扑与MC noise显式外传，优化NLL+analytic Gaussian KL。Eqs16–19仅steering才用独立SAE DECODER列方向加权单位化，再移除已有parallel分量、注入指定strength。 成本过高，不复现（审查 DONE）。Gemma2-9B、layer10的16K GemmaScope SAE、8数据集、LDA/ETM/BERTopic多变种及Bayesian优化，GPT4.1 topic judge每数据集2800成对比较和额外coherence/steering评测。完整矩阵超单卡短时预算；不下载LLM/SAE或调API，不编造未报告总GPU小时。MechanisticETM接冻结SAE encoder_weights与真实过滤后的activation counts；steering函数单独接不同的decoder方向和decoder bias。  可解释性 SAE主题模型与控制 基础模型 能力证据：评测采样、读出与可靠性 Mechanistic ETM为什么用SAE encoder构造主题概率，却用独立decoder做steering？ encoder把主题方向映射到特征激活概率，服务于计数的二项似然；decoder则把特征组合映回残差空间，服务于干预，二者不能隐式绑权。steering还需移除原有平行分量后注入指定强度，直接加向量会保留未知旧强度。本地公式核不含完整大模型主题实验。 例如主题涉及几个稀疏特征，先估计它们出现概率，再用解码方向修改残差；若直接拿编码权重当解码方向，即使维度相容也改变了机制。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-9dd5440b4796e943">Mechanistic ETM为什么用SAE encoder构造主题概率，却用独立decoder做steering？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amechanistic-etm">Model Directions, Not Words: Mechanistic Topic Models Using Sparse Autoencoders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Columbia University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>encoder把主题方向映射到特征激活概率，服务于计数的二项似然；decoder则把特征组合映回残差空间，服务于干预，二者不能隐式绑权。steering还需移除原有平行分量后注入指定强度，直接加向量会保留未知旧强度。本地公式核不含完整大模型主题实验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如主题涉及几个稀疏特征，先估计它们出现概率，再用解码方向修改残差；若直接拿编码权重当解码方向，即使维度相容也改变了机制。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.23220v1">原论文</a> · <a href="../../../../foundation-models/2507.23220-mechanistic-etm/">实现解读</a> · <a href="#qa-9dd5440b4796e943">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mechanistic-etm" data-paper-title="Model Directions, Not Words: Mechanistic Topic Models Using Sparse Autoencoders" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Model Directions, Not Words: Mechanistic Topic Models Using Sparse Autoencoders 基础模型 Columbia University 2025-07-31 固定v3 Section4.2.2 Eqs9–13：δN(0,I)、θ=softmaxδ、βk=sigmoid(W_in vk+b)，W_in为冻结SAE ENCODER，不是decoder；每个feature计数Binomial(Ntokens,[θβ]i)。variational q拓扑与MC noise显式外传，优化NLL+analytic Gaussian KL。Eqs16–19仅steering才用独立SAE DECODER列方向加权单位化，再移除已有parallel分量、注入指定strength。 成本过高，不复现（审查 DONE）。Gemma2-9B、layer10的16K GemmaScope SAE、8数据集、LDA/ETM/BERTopic多变种及Bayesian优化，GPT4.1 topic judge每数据集2800成对比较和额外coherence/steering评测。完整矩阵超单卡短时预算；不下载LLM/SAE或调API，不编造未报告总GPU小时。MechanisticETM接冻结SAE encoder_weights与真实过滤后的activation counts；steering函数单独接不同的decoder方向和decoder bias。  可解释性 SAE主题模型与控制 基础模型 能力证据：评测采样、读出与可靠性 feature 计数为什么用 Binomial，而不能先归一化成普通 multinomial 词袋？ 每个feature在每token最多激活一次，但一个token可涉及多个feature，计数并非互斥词类别总数。按Ntokens形成独立feature计数模型，与把总计数强制归一化成词袋，是不同似然。 示意：同一token同时激活两个feature时，feature计数和可以超过token数量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-20b9436154bf0269">feature 计数为什么用 Binomial，而不能先归一化成普通 multinomial 词袋？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amechanistic-etm">Model Directions, Not Words: Mechanistic Topic Models Using Sparse Autoencoders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Columbia University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每个feature在每token最多激活一次，但一个token可涉及多个feature，计数并非互斥词类别总数。按Ntokens形成独立feature计数模型，与把总计数强制归一化成词袋，是不同似然。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一token同时激活两个feature时，feature计数和可以超过token数量。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.23220v1">原论文</a> · <a href="../../../../foundation-models/2507.23220-mechanistic-etm/">实现解读</a> · <a href="#qa-20b9436154bf0269">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mechanistic-etm" data-paper-title="Model Directions, Not Words: Mechanistic Topic Models Using Sparse Autoencoders" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Model Directions, Not Words: Mechanistic Topic Models Using Sparse Autoencoders 基础模型 Columbia University 2025-07-31 固定v3 Section4.2.2 Eqs9–13：δN(0,I)、θ=softmaxδ、βk=sigmoid(W_in vk+b)，W_in为冻结SAE ENCODER，不是decoder；每个feature计数Binomial(Ntokens,[θβ]i)。variational q拓扑与MC noise显式外传，优化NLL+analytic Gaussian KL。Eqs16–19仅steering才用独立SAE DECODER列方向加权单位化，再移除已有parallel分量、注入指定strength。 成本过高，不复现（审查 DONE）。Gemma2-9B、layer10的16K GemmaScope SAE、8数据集、LDA/ETM/BERTopic多变种及Bayesian优化，GPT4.1 topic judge每数据集2800成对比较和额外coherence/steering评测。完整矩阵超单卡短时预算；不下载LLM/SAE或调API，不编造未报告总GPU小时。MechanisticETM接冻结SAE encoder_weights与真实过滤后的activation counts；steering函数单独接不同的decoder方向和decoder bias。  可解释性 SAE主题模型与控制 基础模型 能力证据：评测采样、读出与可靠性 ETM steering 的 strength=0，是否表示完全不改 activation？ 不一定。文档先移除已有平行分量，再注入λs并加回decoder bias；λ=0仍会去掉原平行分量。它不是简单a+λs，且steering使用独立decoder，不能绑成encoder权重。 示意：原activation已沿主题方向投影很大，λ=0会删除该方向而非保持原值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-624e698062a65845">ETM steering 的 strength=0，是否表示完全不改 activation？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amechanistic-etm">Model Directions, Not Words: Mechanistic Topic Models Using Sparse Autoencoders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Columbia University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不一定。文档先移除已有平行分量，再注入λs并加回decoder bias；λ=0仍会去掉原平行分量。它不是简单a+λs，且steering使用独立decoder，不能绑成encoder权重。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>原activation已沿主题方向投影很大，λ=0会删除该方向而非保持原值。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.23220v1">原论文</a> · <a href="../../../../foundation-models/2507.23220-mechanistic-etm/">实现解读</a> · <a href="#qa-624e698062a65845">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

怎样确认高分来自目标能力，而非语言、输入顺序、读出方式或统计偏差？

## 记住这一点

XLGoBench 用跨语言可比较的算法任务和客观答案控制任务本身，再改变语言与复杂度以观察能力缺口。ProEval 利用历史逐题评分训练概率替身，按不确定性选择更有信息的测试输入，节省昂贵评分。激活探针、重排校准和水印则审计不同观测通道；先定义想测的能力与可观察量，才能解释分数。

## 一个例子

同一张图最短路题可以换语言而不换正确路径；如果换语言后更差，需要检查翻译是否保留约束。若预算只够测 100 题，主动选题又会改变样本分布，不能直接把所选难题平均分当总体正确率；应使用方法规定的估计与不确定性。

## 什么时候要小心

检测器分数、算子契约通过率和模型能力不同。代理模型可用历史数据，不能提前读目标未测分数或 gold；跨语言差异也不是所有语言能力的完整结论。本地 ProEval 子核心和 XLGoBench scorer 诊断不代表完整论文复现。

## 先读这几篇

先读 XLGoBench，理解同底层任务、语言和难度受控的比较；再读 ProEval，理解 GP 替身、主动选题与总体分数估计。之后再看探针、校准、安全检测或在线实验。

1. [XLGoBench: Detecting cross-lingual skill gaps with algorithmic tasks](../../../foundation-models/2605.30788-xlgobench/README.md) · [原论文](https://arxiv.org/abs/2605.30788v1)
2. [ProEval: Proactive Failure Discovery and Efficient Performance Estimation for Generative AI Evaluation](../../../foundation-models/2604.23099-proeval/README.md) · [原论文](https://arxiv.org/abs/2604.23099)

## 自测一下

主动挑选了一批疑似失败题，发现平均正确率低，能直接据此估计线上总体正确率吗？

??? note "展开参考答案"

    不能。样本是按失败可能性筛选的，存在选择偏差；需要定义目标分布并使用相应估计器或另取代表样本。失败发现能力和总体性能估计要分别报告。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
