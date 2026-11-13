---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 能力证据：评测采样、读出与可靠性

[基础模型](index.md) / 88 个问题 · 22 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

[阅读本主题精读卡片：多篇论文对比、分析与问答](../../deep-dives/foundation-models/evaluation-and-evidence.md)

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
<p class="ar-learning-status" data-learning-status role="status">88 个问题 · 22 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:xla-trenches" data-paper-title="XLA from the Trenches: Correctness on TPU Workloads at Scale" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="XLA from the Trenches: Correctness on TPU Workloads at Scale 基础模型 Google 2026-10-31 编译器成功生成并执行程序，不保证数值正确。Google 将模板引导合成程序、生产 autotuner 的真实融合配置和 agent swarm 组合，发现静默错编译；随后从大 HLO 图定位到单个 fusion，再保留 fusion 原貌检查 VREG 中间值。它是编译正确性基础设施，不是新的推荐模型或通过 A/B 门槛的工业推荐条目。 完整实验成本过高，不复现（审查 DONE）。只读核对固定 v1 的 Sections2–4、上游 isolation/evaluator 链接与日期；没有运行、训练或调用其内部 harness，没有本地算法目录、metrics、GPU 收据或 Evolve 映射。公开宏图工具不意味着 agent 编排、目标 ISA/MXU 仿真、VREG stepping 和生产样本全部公开。  推理与系统效率 编译器正确性与分层故障隔离 基础模型 能力证据：评测采样、读出与可靠性 编译成功、程序没有崩溃，为什么还不能说明XLA执行正确？ 静默错编译会返回合法形状的有限张量，但索引、舍入、buffer或同步语义已出错。没有错误信号，只看运行完成或loss短期正常会漏检；论文依赖合法输入下的差分参考及逐层隔离，不把成功启动当作正确性证据。 教学例：一次窄整数iota回绕可能让索引5的写操作也改到261，程序仍执行完成，只有与正确索引语义的输出比较才暴露问题。 2026-11-04">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<span id="paper-foundation-models-xla-trenches-c37e2d34" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-80a43e3611b0011e">编译成功、程序没有崩溃，为什么还不能说明XLA执行正确？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Axla-trenches">XLA from the Trenches: Correctness on TPU Workloads at Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-04 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>静默错编译会返回合法形状的有限张量，但索引、舍入、buffer或同步语义已出错。没有错误信号，只看运行完成或loss短期正常会漏检；论文依赖合法输入下的差分参考及逐层隔离，不把成功启动当作正确性证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：一次窄整数iota回绕可能让索引5的写操作也改到261，程序仍执行完成，只有与正确索引语义的输出比较才暴露问题。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制与数值例子；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.00624">原论文</a> · <a href="../../../../foundation-models/2611.00624-xla-trenches/">实现解读</a> · <a href="#qa-80a43e3611b0011e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:xla-trenches" data-paper-title="XLA from the Trenches: Correctness on TPU Workloads at Scale" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="XLA from the Trenches: Correctness on TPU Workloads at Scale 基础模型 Google 2026-10-31 编译器成功生成并执行程序，不保证数值正确。Google 将模板引导合成程序、生产 autotuner 的真实融合配置和 agent swarm 组合，发现静默错编译；随后从大 HLO 图定位到单个 fusion，再保留 fusion 原貌检查 VREG 中间值。它是编译正确性基础设施，不是新的推荐模型或通过 A/B 门槛的工业推荐条目。 完整实验成本过高，不复现（审查 DONE）。只读核对固定 v1 的 Sections2–4、上游 isolation/evaluator 链接与日期；没有运行、训练或调用其内部 harness，没有本地算法目录、metrics、GPU 收据或 Evolve 映射。公开宏图工具不意味着 agent 编排、目标 ISA/MXU 仿真、VREG stepping 和生产样本全部公开。  推理与系统效率 编译器正确性与分层故障隔离 基础模型 能力证据：评测采样、读出与可靠性 为什么分层隔离既要反向约束输入，又要保留fusion检查VREG？ 反向约束避免负数开方、除零等非法输入制造伪差异；宏图定位只缩小到fusion，内部lowering错误仍需查看寄存器中间值。拆fusion会改变内存精度和流水，使原bug消失，因此不能把拆图后正常当作原融合已经正确。 教学例：r=x−f32(f16(x))若在VREG中被省略舍入会全零；调试拆图后落入16位HBM反而恢复舍入，因此应观察原fusion而非替换它。 2026-11-04">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-098b3c2d60311839">为什么分层隔离既要反向约束输入，又要保留fusion检查VREG？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Axla-trenches">XLA from the Trenches: Correctness on TPU Workloads at Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-04 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>反向约束避免负数开方、除零等非法输入制造伪差异；宏图定位只缩小到fusion，内部lowering错误仍需查看寄存器中间值。拆fusion会改变内存精度和流水，使原bug消失，因此不能把拆图后正常当作原融合已经正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：r=x−f32(f16(x))若在VREG中被省略舍入会全零；调试拆图后落入16位HBM反而恢复舍入，因此应观察原fusion而非替换它。</p>
<p class="ar-learning-sources">依据：核心机制与数值例子、资源与复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.00624">原论文</a> · <a href="../../../../foundation-models/2611.00624-xla-trenches/">实现解读</a> · <a href="#qa-098b3c2d60311839">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:xla-trenches" data-paper-title="XLA from the Trenches: Correctness on TPU Workloads at Scale" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="XLA from the Trenches: Correctness on TPU Workloads at Scale 基础模型 Google 2026-10-31 编译器成功生成并执行程序，不保证数值正确。Google 将模板引导合成程序、生产 autotuner 的真实融合配置和 agent swarm 组合，发现静默错编译；随后从大 HLO 图定位到单个 fusion，再保留 fusion 原貌检查 VREG 中间值。它是编译正确性基础设施，不是新的推荐模型或通过 A/B 门槛的工业推荐条目。 完整实验成本过高，不复现（审查 DONE）。只读核对固定 v1 的 Sections2–4、上游 isolation/evaluator 链接与日期；没有运行、训练或调用其内部 harness，没有本地算法目录、metrics、GPU 收据或 Evolve 映射。公开宏图工具不意味着 agent 编排、目标 ISA/MXU 仿真、VREG stepping 和生产样本全部公开。  推理与系统效率 编译器正确性与分层故障隔离 基础模型 能力证据：评测采样、读出与可靠性 142项已修复、103项审查中，以及线上A/B收益，为什么是三种不同证据？ 已修复描述经工程流程解决的缺陷数；审查中仍可能被驳回或修改，不能相加成245项已修复。用户A/B需要真实分流对照和业务指标，不能从bug数量推出。本文符合Google系统基础设施收录，但不是因此通过工业推荐A/B门槛。 教学例：提交10个补丁、合入6个、其余4个审查中，完成数是6而不是10；即使全部合入，也没有给出CTR提升的随机实验。 2026-11-04">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0719ea969a0fdbee">142项已修复、103项审查中，以及线上A/B收益，为什么是三种不同证据？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Axla-trenches">XLA from the Trenches: Correctness on TPU Workloads at Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-04 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>已修复描述经工程流程解决的缺陷数；审查中仍可能被驳回或修改，不能相加成245项已修复。用户A/B需要真实分流对照和业务指标，不能从bug数量推出。本文符合Google系统基础设施收录，但不是因此通过工业推荐A/B门槛。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：提交10个补丁、合入6个、其余4个审查中，完成数是6而不是10；即使全部合入，也没有给出CTR提升的随机实验。</p>
<p class="ar-learning-sources">依据：论文工程与线上证据、背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.00624">原论文</a> · <a href="../../../../foundation-models/2611.00624-xla-trenches/">实现解读</a> · <a href="#qa-0719ea969a0fdbee">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:xla-trenches" data-paper-title="XLA from the Trenches: Correctness on TPU Workloads at Scale" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="XLA from the Trenches: Correctness on TPU Workloads at Scale 基础模型 Google 2026-10-31 编译器成功生成并执行程序，不保证数值正确。Google 将模板引导合成程序、生产 autotuner 的真实融合配置和 agent swarm 组合，发现静默错编译；随后从大 HLO 图定位到单个 fusion，再保留 fusion 原貌检查 VREG 中间值。它是编译正确性基础设施，不是新的推荐模型或通过 A/B 门槛的工业推荐条目。 完整实验成本过高，不复现（审查 DONE）。只读核对固定 v1 的 Sections2–4、上游 isolation/evaluator 链接与日期；没有运行、训练或调用其内部 harness，没有本地算法目录、metrics、GPU 收据或 Evolve 映射。公开宏图工具不意味着 agent 编排、目标 ISA/MXU 仿真、VREG stepping 和生产样本全部公开。  推理与系统效率 编译器正确性与分层故障隔离 基础模型 能力证据：评测采样、读出与可靠性 有公开OpenXLA代码，为什么本库仍将完整论文标为不复现，而不在A100跑个替代？ 公开macro隔离和evaluator只是部分链路；内部生产图、agent harness、目标ISA与MXU模拟、VREG逐步硬件调试和真实TPU确认并不随框架开源。A100没有相同寄存器/舍入/编译语义，运行CUDA例子不能验证TPU缺陷。资源和可得性不匹配，所以审查DONE、不复现而不伪造通过。 教学例：在CUDA上正确执行两次cast，不能证明某TPU lowering没有跳过cast；两者最终数值相同也没有覆盖原始TPU生成代码。 2026-11-04">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c830109380a835e9">有公开OpenXLA代码，为什么本库仍将完整论文标为不复现，而不在A100跑个替代？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Axla-trenches">XLA from the Trenches: Correctness on TPU Workloads at Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-04 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>公开macro隔离和evaluator只是部分链路；内部生产图、agent harness、目标ISA与MXU模拟、VREG逐步硬件调试和真实TPU确认并不随框架开源。A100没有相同寄存器/舍入/编译语义，运行CUDA例子不能验证TPU缺陷。资源和可得性不匹配，所以审查DONE、不复现而不伪造通过。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：在CUDA上正确执行两次cast，不能证明某TPU lowering没有跳过cast；两者最终数值相同也没有覆盖原始TPU生成代码。</p>
<p class="ar-learning-sources">依据：已核查与未实现、资源与复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2611.00624">原论文</a> · <a href="../../../../foundation-models/2611.00624-xla-trenches/">实现解读</a> · <a href="#qa-c830109380a835e9">问题链接</a></p>
</details>
</article>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:llm-stochasticity" data-paper-title="The Illusion of Stochasticity in LLMs" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="The Illusion of Stochasticity in LLMs 基础模型 National University of Singapore 2026-04-08 要求LLM“随机选一个数”不等价于访问可靠随机源。论文比较不同模型、离散/连续目标分布、逐次和批量提示，发现明显类别偏好、历史排斥和周期性；看起来均匀的直方图也可能来自确定性序列。 完整实验成本过高，不复现（审查 DONE）。所有metric仅属L1诊断，无gold给actor、无test选择、无模型效果提升声明。L1 机制/评测组件，diagnostic only，不是完整模型能力复现。CPU组件专测已通过；没有CUDA路径，不需要GPU验收。未接入Evolve，不可据本地fixture成绩晋级。evaluate_discrete_uniform 拒绝错误样本数、重复标签、布尔/非整数、support之外的值；evaluate_continuous 拒绝NaN和均匀分布越界。反例序列0,1,2,3不断循环：直方图卡方为0，却从无相邻重复且转移高度集中，说明边缘分布检验不足。  评测与可靠性 随机性与统计诊断 基础模型 能力证据：评测采样、读出与可靠性 直方图完全均匀，为什么仍不是真随机？ 直方图只描述单点边缘频率，不描述时间次序。确定性的0,1,2,3循环也完全均匀，但下一项可被前一项预测；需要另外检查转移和时序依赖。 循环1024项的卡方统计量为0，仍从不相邻重复。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<span id="paper-foundation-models-llm-stochasticity-133d0a6f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8335bb71e04411d5">直方图完全均匀，为什么仍不是真随机？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Allm-stochasticity">The Illusion of Stochasticity in LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直方图只描述单点边缘频率，不描述时间次序。确定性的0,1,2,3循环也完全均匀，但下一项可被前一项预测；需要另外检查转移和时序依赖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>循环1024项的卡方统计量为0，仍从不相邻重复。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制与公式、原文结果与限制、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.06543v1">原论文</a> · <a href="../../../../foundation-models/2604.06543-llm-stochasticity/">实现解读</a> · <a href="#qa-8335bb71e04411d5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:llm-stochasticity" data-paper-title="The Illusion of Stochasticity in LLMs" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="The Illusion of Stochasticity in LLMs 基础模型 National University of Singapore 2026-04-08 要求LLM“随机选一个数”不等价于访问可靠随机源。论文比较不同模型、离散/连续目标分布、逐次和批量提示，发现明显类别偏好、历史排斥和周期性；看起来均匀的直方图也可能来自确定性序列。 完整实验成本过高，不复现（审查 DONE）。所有metric仅属L1诊断，无gold给actor、无test选择、无模型效果提升声明。L1 机制/评测组件，diagnostic only，不是完整模型能力复现。CPU组件专测已通过；没有CUDA路径，不需要GPU验收。未接入Evolve，不可据本地fixture成绩晋级。evaluate_discrete_uniform 拒绝错误样本数、重复标签、布尔/非整数、support之外的值；evaluate_continuous 拒绝NaN和均匀分布越界。反例序列0,1,2,3不断循环：直方图卡方为0，却从无相邻重复且转移高度集中，说明边缘分布检验不足。  评测与可靠性 随机性与统计诊断 基础模型 能力证据：评测采样、读出与可靠性 KS或卡方p&gt;0.05应怎样解释？ 在指定原假设与检验前提下，当前样本未提供足够拒绝证据；不是模型有95%概率随机，也不是独立性证明。多次选prompt后挑最好p值还会改变推断口径。 一个精心构造的均匀周期序列可以得到p=1，但不能作为可靠熵源。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-83fe38b1f38d842f">KS或卡方p&gt;0.05应怎样解释？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Allm-stochasticity">The Illusion of Stochasticity in LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>在指定原假设与检验前提下，当前样本未提供足够拒绝证据；不是模型有95%概率随机，也不是独立性证明。多次选prompt后挑最好p值还会改变推断口径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个精心构造的均匀周期序列可以得到p=1，但不能作为可靠熵源。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制与公式、原文结果与限制、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.06543v1">原论文</a> · <a href="../../../../foundation-models/2604.06543-llm-stochasticity/">实现解读</a> · <a href="#qa-83fe38b1f38d842f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:llm-stochasticity" data-paper-title="The Illusion of Stochasticity in LLMs" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="The Illusion of Stochasticity in LLMs 基础模型 National University of Singapore 2026-04-08 要求LLM“随机选一个数”不等价于访问可靠随机源。论文比较不同模型、离散/连续目标分布、逐次和批量提示，发现明显类别偏好、历史排斥和周期性；看起来均匀的直方图也可能来自确定性序列。 完整实验成本过高，不复现（审查 DONE）。所有metric仅属L1诊断，无gold给actor、无test选择、无模型效果提升声明。L1 机制/评测组件，diagnostic only，不是完整模型能力复现。CPU组件专测已通过；没有CUDA路径，不需要GPU验收。未接入Evolve，不可据本地fixture成绩晋级。evaluate_discrete_uniform 拒绝错误样本数、重复标签、布尔/非整数、support之外的值；evaluate_continuous 拒绝NaN和均匀分布越界。反例序列0,1,2,3不断循环：直方图卡方为0，却从无相邻重复且转移高度集中，说明边缘分布检验不足。  评测与可靠性 随机性与统计诊断 基础模型 能力证据：评测采样、读出与可靠性 这里的外部PRNG与随机舍入里的随机数有何不同？ 论文检验LLM是否能按请求生成目标分布；外部PRNG是一个不同的可控随机源。SR使用明确generator实现相邻舍入概率，并检验条件均值，不是在证明LLM自身随机。 用NumPy生成均匀数不能填成Gemini采样结果；用torch generator检验SR也不能推断自然语言输出独立。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b2fbd708dbb1b403">这里的外部PRNG与随机舍入里的随机数有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Allm-stochasticity">The Illusion of Stochasticity in LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>论文检验LLM是否能按请求生成目标分布；外部PRNG是一个不同的可控随机源。SR使用明确generator实现相邻舍入概率，并检验条件均值，不是在证明LLM自身随机。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用NumPy生成均匀数不能填成Gemini采样结果；用torch generator检验SR也不能推断自然语言输出独立。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制与公式、原文结果与限制、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.06543v1">原论文</a> · <a href="../../../../foundation-models/2604.06543-llm-stochasticity/">实现解读</a> · <a href="#qa-b2fbd708dbb1b403">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:llm-stochasticity" data-paper-title="The Illusion of Stochasticity in LLMs" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="The Illusion of Stochasticity in LLMs 基础模型 National University of Singapore 2026-04-08 要求LLM“随机选一个数”不等价于访问可靠随机源。论文比较不同模型、离散/连续目标分布、逐次和批量提示，发现明显类别偏好、历史排斥和周期性；看起来均匀的直方图也可能来自确定性序列。 完整实验成本过高，不复现（审查 DONE）。所有metric仅属L1诊断，无gold给actor、无test选择、无模型效果提升声明。L1 机制/评测组件，diagnostic only，不是完整模型能力复现。CPU组件专测已通过；没有CUDA路径，不需要GPU验收。未接入Evolve，不可据本地fixture成绩晋级。evaluate_discrete_uniform 拒绝错误样本数、重复标签、布尔/非整数、support之外的值；evaluate_continuous 拒绝NaN和均匀分布越界。反例序列0,1,2,3不断循环：直方图卡方为0，却从无相邻重复且转移高度集中，说明边缘分布检验不足。  评测与可靠性 随机性与统计诊断 基础模型 能力证据：评测采样、读出与可靠性 遇到越界数或输出不足1024条时，为什么不能丢掉后继续？ 丢弃会改变被评测分布和样本数，可能只保留好看的输出。接口严格校验完整计数、support和有限性，解析失败应由上层单独记录，不静默改分母。 模型生成1000条合法数与24条越界数，不能把合法1000条当完整成功采样。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-eeba2316ffba1af7">遇到越界数或输出不足1024条时，为什么不能丢掉后继续？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Allm-stochasticity">The Illusion of Stochasticity in LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>丢弃会改变被评测分布和样本数，可能只保留好看的输出。接口严格校验完整计数、support和有限性，解析失败应由上层单独记录，不静默改分母。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型生成1000条合法数与24条越界数，不能把合法1000条当完整成功采样。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制与公式、原文结果与限制、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.06543v1">原论文</a> · <a href="../../../../foundation-models/2604.06543-llm-stochasticity/">实现解读</a> · <a href="#qa-eeba2316ffba1af7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:storyscope" data-paper-title="StoryScope: Investigating idiosyncrasies in AI fiction" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="StoryScope: Investigating idiosyncrasies in AI fiction 基础模型 University of Maryland, College Park 2026-04-03 作者身份检测常抓词汇或句长，却无法解释故事怎样组织主题、角色、时间和冲突。StoryScope 先把平行故事改为结构化叙事模板，在同一写作 prompt 的人类/五个模型之间比较，再归纳特征、去重、批量赋值。随后用分类器与 bootstrap SHAP 区分跨模型的人类–AI核心和特定模型指纹。本地没有把字数、几个关键词或已知作者标签假装成语义特征。贡献限定为真实外部特征统计上的精确核心门控，以及保持同 prompt 六个来源共同抽样的 bootstrap 索引。 完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。本地交付是 L1 数值/协议组件，不是完整论文能力复现。完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。prompt_bootstrap 对 prompt 采样并把该 prompt 所有行一并展开；重复抽中同一 prompt 也保留整组重复。select_core_features 验证输入并实际计算分位、中位数、显著性和跨模型门槛，返回核心 mask 与方向。没有 LLM 特征发现/赋值、完整 XGBoost/SHAP 拟合或可调用的文本检测模型。  评测与研究证据 可解释生成文本检测 基础模型 能力证据：评测采样、读出与可靠性 StoryScope 的叙事特征与数几个AI常用词有何区别？ 它描述主题显露、角色能动性、时间组织等跨句故事结构，通过平行prompt比较与LLM归纳/赋值获得。几词计数没有执行这些语义阶段，本地也不把便宜关键词替代成叙事模型。 教学例：两篇故事都不用相同词汇，但都在结尾明说教训；“是否明确主题”是结构线索，不是某个单词是否出现。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<span id="paper-foundation-models-storyscope-91aa94e5" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-409045ced6c7e999">StoryScope 的叙事特征与数几个AI常用词有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Astoryscope">StoryScope: Investigating idiosyncrasies in AI fiction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · University of Maryland, College Park</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它描述主题显露、角色能动性、时间组织等跨句故事结构，通过平行prompt比较与LLM归纳/赋值获得。几词计数没有执行这些语义阶段，本地也不把便宜关键词替代成叙事模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：两篇故事都不用相同词汇，但都在结尾明说教训；“是否明确主题”是结构线索，不是某个单词是否出现。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.03136v1">原论文</a> · <a href="../../../../foundation-models/2604.03136-storyscope/">实现解读</a> · <a href="#qa-409045ced6c7e999">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:storyscope" data-paper-title="StoryScope: Investigating idiosyncrasies in AI fiction" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="StoryScope: Investigating idiosyncrasies in AI fiction 基础模型 University of Maryland, College Park 2026-04-03 作者身份检测常抓词汇或句长，却无法解释故事怎样组织主题、角色、时间和冲突。StoryScope 先把平行故事改为结构化叙事模板，在同一写作 prompt 的人类/五个模型之间比较，再归纳特征、去重、批量赋值。随后用分类器与 bootstrap SHAP 区分跨模型的人类–AI核心和特定模型指纹。本地没有把字数、几个关键词或已知作者标签假装成语义特征。贡献限定为真实外部特征统计上的精确核心门控，以及保持同 prompt 六个来源共同抽样的 bootstrap 索引。 完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。本地交付是 L1 数值/协议组件，不是完整论文能力复现。完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。prompt_bootstrap 对 prompt 采样并把该 prompt 所有行一并展开；重复抽中同一 prompt 也保留整组重复。select_core_features 验证输入并实际计算分位、中位数、显著性和跨模型门槛，返回核心 mask 与方向。没有 LLM 特征发现/赋值、完整 XGBoost/SHAP 拟合或可调用的文本检测模型。  评测与研究证据 可解释生成文本检测 基础模型 能力证据：评测采样、读出与可靠性 为什么最高SHAP特征也可能不是跨模型核心？ 核心还要求稳定性、null显著性、top25频率、人类–AI均值差及五个AI模型之间较小spread。一个只对某模型很强的特征可能是指纹，不应因SHAP大就叫核心；本地逐项合取而非加权打分。 教学例：某特征五模型均值为0.8、0.8、0.8、0.8、0，spread0.8超过0.35，即使重要性最大也被核心门槛拒绝。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-de1fa713fe07f924">为什么最高SHAP特征也可能不是跨模型核心？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Astoryscope">StoryScope: Investigating idiosyncrasies in AI fiction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · University of Maryland, College Park</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>核心还要求稳定性、null显著性、top25频率、人类–AI均值差及五个AI模型之间较小spread。一个只对某模型很强的特征可能是指纹，不应因SHAP大就叫核心；本地逐项合取而非加权打分。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：某特征五模型均值为0.8、0.8、0.8、0.8、0，spread0.8超过0.35，即使重要性最大也被核心门槛拒绝。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.03136v1">原论文</a> · <a href="../../../../foundation-models/2604.03136-storyscope/">实现解读</a> · <a href="#qa-de1fa713fe07f924">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:storyscope" data-paper-title="StoryScope: Investigating idiosyncrasies in AI fiction" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="StoryScope: Investigating idiosyncrasies in AI fiction 基础模型 University of Maryland, College Park 2026-04-03 作者身份检测常抓词汇或句长，却无法解释故事怎样组织主题、角色、时间和冲突。StoryScope 先把平行故事改为结构化叙事模板，在同一写作 prompt 的人类/五个模型之间比较，再归纳特征、去重、批量赋值。随后用分类器与 bootstrap SHAP 区分跨模型的人类–AI核心和特定模型指纹。本地没有把字数、几个关键词或已知作者标签假装成语义特征。贡献限定为真实外部特征统计上的精确核心门控，以及保持同 prompt 六个来源共同抽样的 bootstrap 索引。 完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。本地交付是 L1 数值/协议组件，不是完整论文能力复现。完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。prompt_bootstrap 对 prompt 采样并把该 prompt 所有行一并展开；重复抽中同一 prompt 也保留整组重复。select_core_features 验证输入并实际计算分位、中位数、显著性和跨模型门槛，返回核心 mask 与方向。没有 LLM 特征发现/赋值、完整 XGBoost/SHAP 拟合或可调用的文本检测模型。  评测与研究证据 可解释生成文本检测 基础模型 能力证据：评测采样、读出与可靠性 StoryScope与DetectorScope的可解释性来自哪里，能互换特征吗？ StoryScope把叙事问题转成外部语义赋值，靠分类器/SHAP定位核心与指纹；DetectorScope依赖模型内部SAE特征和稀疏线性头的可加归因。两者解释单位、获取成本与错误模式不同，不能把未生成的叙事特征拿SAE随机列替代。 教学例：“结尾主题是否明说”要检查全文；SAE某列的激活贡献是另一个观测，不能凭列编号宣称它语义上等于该叙事问题。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-00b20bade33adf0d">StoryScope与DetectorScope的可解释性来自哪里，能互换特征吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Astoryscope">StoryScope: Investigating idiosyncrasies in AI fiction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · University of Maryland, College Park</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>StoryScope把叙事问题转成外部语义赋值，靠分类器/SHAP定位核心与指纹；DetectorScope依赖模型内部SAE特征和稀疏线性头的可加归因。两者解释单位、获取成本与错误模式不同，不能把未生成的叙事特征拿SAE随机列替代。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：“结尾主题是否明说”要检查全文；SAE某列的激活贡献是另一个观测，不能凭列编号宣称它语义上等于该叙事问题。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.03136v1">原论文</a> · <a href="../../../../foundation-models/2604.03136-storyscope/">实现解读</a> · <a href="#qa-00b20bade33adf0d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:storyscope" data-paper-title="StoryScope: Investigating idiosyncrasies in AI fiction" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="StoryScope: Investigating idiosyncrasies in AI fiction 基础模型 University of Maryland, College Park 2026-04-03 作者身份检测常抓词汇或句长，却无法解释故事怎样组织主题、角色、时间和冲突。StoryScope 先把平行故事改为结构化叙事模板，在同一写作 prompt 的人类/五个模型之间比较，再归纳特征、去重、批量赋值。随后用分类器与 bootstrap SHAP 区分跨模型的人类–AI核心和特定模型指纹。本地没有把字数、几个关键词或已知作者标签假装成语义特征。贡献限定为真实外部特征统计上的精确核心门控，以及保持同 prompt 六个来源共同抽样的 bootstrap 索引。 完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。本地交付是 L1 数值/协议组件，不是完整论文能力复现。完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。prompt_bootstrap 对 prompt 采样并把该 prompt 所有行一并展开；重复抽中同一 prompt 也保留整组重复。select_core_features 验证输入并实际计算分位、中位数、显著性和跨模型门槛，返回核心 mask 与方向。没有 LLM 特征发现/赋值、完整 XGBoost/SHAP 拟合或可调用的文本检测模型。  评测与研究证据 可解释生成文本检测 基础模型 能力证据：评测采样、读出与可靠性 同一prompt的六种来源为什么必须一起bootstrap？ 这些故事共享写作条件，不是独立同分布的任意六行。先按prompt隔离train/validation/test，再按prompt重采样并展开全部来源，可保留匹配结构。逐故事抽样或跨split同prompt会夸大独立证据。 教学例：抽中promptA两次，就把A的人类与五AI故事各出现两次；不能只抽人类A而漏掉五个AI版本来造更稳定SHAP。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-bbd0eae682f39c8b">同一prompt的六种来源为什么必须一起bootstrap？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Astoryscope">StoryScope: Investigating idiosyncrasies in AI fiction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · University of Maryland, College Park</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这些故事共享写作条件，不是独立同分布的任意六行。先按prompt隔离train/validation/test，再按prompt重采样并展开全部来源，可保留匹配结构。逐故事抽样或跨split同prompt会夸大独立证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：抽中promptA两次，就把A的人类与五AI故事各出现两次；不能只抽人类A而漏掉五个AI版本来造更稳定SHAP。</p>
<p class="ar-learning-sources">依据：数据协议与代码映射；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.03136v1">原论文</a> · <a href="../../../../foundation-models/2604.03136-storyscope/">实现解读</a> · <a href="#qa-bbd0eae682f39c8b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:latent-generalization" data-paper-title="Improving Latent Generalization Using Test-time Compute" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Improving Latent Generalization Using Test-time Compute 基础模型 Google DeepMind 2026-04-01 模型记住 A&gt;B 并不必然推出 B&lt;A，记住多个关系也不保证能答出未显式训练的组合。论文把知识获取、会思考的轨迹引导、正确性RL分开，研究在一个结构训练出的推理能力能否迁移到仅做知识SFT的另一个结构。 私有/商业训练依赖，完整实验不复现（审查 DONE）。所有metric仅属L1诊断，无gold给actor、无test选择、无模型效果提升声明。L1 机制/评测组件，diagnostic only，不是完整模型能力复现。CPU组件专测已通过；没有CUDA路径，不需要GPU验收。未接入Evolve，不可据本地fixture成绩晋级。score_completion 要求heldout是all的子集，primary属于heldout，且gold集合非空；exact_set_pass_at_n 对已经完成的独立尝试计算无偏pass估计。负控显示：train recall=1可以同时heldout recall=0；  知识与推理 潜在知识与泛化 基础模型 能力证据：评测采样、读出与可靠性 latent generalization与记住训练答案有什么区别？ 要答出未显式暴露的关系或组合，而不是复述已见completion。论文分别报告exposed和heldout recall，因为总体F1可能被大量已见答案撑高。 all={A,B,C}、heldout={C}，只答A和B时train recall=1但heldout recall=0。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<span id="paper-foundation-models-latent-generalization-265f2cc5" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e016f2e859cc84f9">latent generalization与记住训练答案有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alatent-generalization">Improving Latent Generalization Using Test-time Compute</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>要答出未显式暴露的关系或组合，而不是复述已见completion。论文分别报告exposed和heldout recall，因为总体F1可能被大量已见答案撑高。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>all={A,B,C}、heldout={C}，只答A和B时train recall=1但heldout recall=0。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制与公式、原文结果与限制、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.01430v1">原论文</a> · <a href="../../../../foundation-models/2604.01430-latent-generalization/">实现解读</a> · <a href="#qa-e016f2e859cc84f9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:latent-generalization" data-paper-title="Improving Latent Generalization Using Test-time Compute" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Improving Latent Generalization Using Test-time Compute 基础模型 Google DeepMind 2026-04-01 模型记住 A&gt;B 并不必然推出 B&lt;A，记住多个关系也不保证能答出未显式训练的组合。论文把知识获取、会思考的轨迹引导、正确性RL分开，研究在一个结构训练出的推理能力能否迁移到仅做知识SFT的另一个结构。 私有/商业训练依赖，完整实验不复现（审查 DONE）。所有metric仅属L1诊断，无gold给actor、无test选择、无模型效果提升声明。L1 机制/评测组件，diagnostic only，不是完整模型能力复现。CPU组件专测已通过；没有CUDA路径，不需要GPU验收。未接入Evolve，不可据本地fixture成绩晋级。score_completion 要求heldout是all的子集，primary属于heldout，且gold集合非空；exact_set_pass_at_n 对已经完成的独立尝试计算无偏pass估计。负控显示：train recall=1可以同时heldout recall=0；  知识与推理 潜在知识与泛化 基础模型 能力证据：评测采样、读出与可靠性 heldout recall=1是否意味着exact-set pass成功？ 不意味着。exact要求预测集合严格等于全部有效答案集合，不能有漏项或虚假附加项；primary inclusion也只是一个指定heldout答案出现的二值指标。 答A,B,C,错误D，heldout C的recall仍是1，但exact=0。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-059b3a359c603bf0">heldout recall=1是否意味着exact-set pass成功？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alatent-generalization">Improving Latent Generalization Using Test-time Compute</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不意味着。exact要求预测集合严格等于全部有效答案集合，不能有漏项或虚假附加项；primary inclusion也只是一个指定heldout答案出现的二值指标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>答A,B,C,错误D，heldout C的recall仍是1，但exact=0。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制与公式、原文结果与限制、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.01430v1">原论文</a> · <a href="../../../../foundation-models/2604.01430-latent-generalization/">实现解读</a> · <a href="#qa-059b3a359c603bf0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:latent-generalization" data-paper-title="Improving Latent Generalization Using Test-time Compute" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Improving Latent Generalization Using Test-time Compute 基础模型 Google DeepMind 2026-04-01 模型记住 A&gt;B 并不必然推出 B&lt;A，记住多个关系也不保证能答出未显式训练的组合。论文把知识获取、会思考的轨迹引导、正确性RL分开，研究在一个结构训练出的推理能力能否迁移到仅做知识SFT的另一个结构。 私有/商业训练依赖，完整实验不复现（审查 DONE）。所有metric仅属L1诊断，无gold给actor、无test选择、无模型效果提升声明。L1 机制/评测组件，diagnostic only，不是完整模型能力复现。CPU组件专测已通过；没有CUDA路径，不需要GPU验收。未接入Evolve，不可据本地fixture成绩晋级。score_completion 要求heldout是all的子集，primary属于heldout，且gold集合非空；exact_set_pass_at_n 对已经完成的独立尝试计算无偏pass估计。负控显示：train recall=1可以同时heldout recall=0；  知识与推理 潜在知识与泛化 基础模型 能力证据：评测采样、读出与可靠性 它与Thinking to Recall的协议分别定位什么问题？ 前者用受控知识获取和结构划分考察未显式答案的泛化；后者研究已有参数事实如何因计算和factual priming被读出。两者都不能把gold-conditioned teacher或事后标注暴露给最终actor。 同一事实被更容易召回，不等于模型学会了未训练关系反转；两者需要不同holdout。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-27c6bab8250f947e">它与Thinking to Recall的协议分别定位什么问题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alatent-generalization">Improving Latent Generalization Using Test-time Compute</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者用受控知识获取和结构划分考察未显式答案的泛化；后者研究已有参数事实如何因计算和factual priming被读出。两者都不能把gold-conditioned teacher或事后标注暴露给最终actor。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一事实被更容易召回，不等于模型学会了未训练关系反转；两者需要不同holdout。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制与公式、原文结果与限制、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.01430v1">原论文</a> · <a href="../../../../foundation-models/2604.01430-latent-generalization/">实现解读</a> · <a href="#qa-27c6bab8250f947e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:latent-generalization" data-paper-title="Improving Latent Generalization Using Test-time Compute" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Improving Latent Generalization Using Test-time Compute 基础模型 Google DeepMind 2026-04-01 模型记住 A&gt;B 并不必然推出 B&lt;A，记住多个关系也不保证能答出未显式训练的组合。论文把知识获取、会思考的轨迹引导、正确性RL分开，研究在一个结构训练出的推理能力能否迁移到仅做知识SFT的另一个结构。 私有/商业训练依赖，完整实验不复现（审查 DONE）。所有metric仅属L1诊断，无gold给actor、无test选择、无模型效果提升声明。L1 机制/评测组件，diagnostic only，不是完整模型能力复现。CPU组件专测已通过；没有CUDA路径，不需要GPU验收。未接入Evolve，不可据本地fixture成绩晋级。score_completion 要求heldout是all的子集，primary属于heldout，且gold集合非空；exact_set_pass_at_n 对已经完成的独立尝试计算无偏pass估计。负控显示：train recall=1可以同时heldout recall=0；  知识与推理 潜在知识与泛化 基础模型 能力证据：评测采样、读出与可靠性 为什么本地只实现这些集合指标，不提供一个简化Gemini训练器？ 原文依赖私有Gemini knowledge SFT、teacher trace与REINFORCE接口，公开方法不足以还原完整训练。精确指标核可负担且有独立价值；虚构通用RL循环会掩盖关键依赖。完整训练明确不复现DONE。 用随机答案数组测试F1公式，不得宣传为Gemini在OOD结构上的实测结果。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-79f71e514d5d6dde">为什么本地只实现这些集合指标，不提供一个简化Gemini训练器？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alatent-generalization">Improving Latent Generalization Using Test-time Compute</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原文依赖私有Gemini knowledge SFT、teacher trace与REINFORCE接口，公开方法不足以还原完整训练。精确指标核可负担且有独立价值；虚构通用RL循环会掩盖关键依赖。完整训练明确不复现DONE。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用随机答案数组测试F1公式，不得宣传为Gemini在OOD结构上的实测结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制与公式、原文结果与限制、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.01430v1">原论文</a> · <a href="../../../../foundation-models/2604.01430-latent-generalization/">实现解读</a> · <a href="#qa-79f71e514d5d6dde">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:decoding-constrained-beam" data-paper-title="Estimating near-verbatim extraction risk in language models with decoding-constrained beam search" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Estimating near-verbatim extraction risk in language models with decoding-constrained beam search 基础模型 AVERI / Stanford University 2026-03-26 只检查 greedy 是否生成训练原文，会漏掉许多单条概率不大、合计概率却很高的近逐字变体。普通 beam 的模型 softmax 分数也不等于实际 top-k 解码分布下的概率。本文把解码约束纳入每一步归一化，枚举部分高概率路径，对与目标后缀接近的路径求和得到确定性下界。本地用途是可审计的概率与距离算子：模型 callback 只接收前缀和已生成 token；目标后缀留在评价侧用于距离剪枝，不交给 callback。没有下载训练语料或加载被审计模型，也不把玩具转移概率称作真实记忆泄漏。 完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。本地交付是 L1 数值/协议组件，不是完整论文能力复现。完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。search 实际执行 top-k、路径 logp、带状编辑/Hamming 剪枝、确定性同分排序和末步质量求和。EOS 在非最终步被移除，最终扩展仍按原算法允许；固定长度协议不等于任意停止规则。没有实现可选的提前停止、批量 KV cache 或 GPU 模型执行，不能用 callback 次数证明原文吞吐。  评测与研究证据 近逐字提取风险 基础模型 能力证据：评测采样、读出与可靠性 greedy没有逐字命中，为什么不等于近逐字提取风险为零？ greedy只看一条最高局部路径。许多接近原文的变体各自概率不大，但总概率可能显著；CBS只枚举其中一部分，因此求和是确定性下界，不是无偏完整风险估计。 教学例：两个不同标点变体概率各0.08，greedy走向第三条不匹配路径，也不能抹掉这0.16的已知近逐字质量。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<span id="paper-foundation-models-decoding-constrained-beam-7d0bad73" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-668c7dba6665932c">greedy没有逐字命中，为什么不等于近逐字提取风险为零？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adecoding-constrained-beam">Estimating near-verbatim extraction risk in language models with decoding-constrained beam search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · AVERI / Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>greedy只看一条最高局部路径。许多接近原文的变体各自概率不大，但总概率可能显著；CBS只枚举其中一部分，因此求和是确定性下界，不是无偏完整风险估计。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：两个不同标点变体概率各0.08，greedy走向第三条不匹配路径，也不能抹掉这0.16的已知近逐字质量。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.24917v1">原论文</a> · <a href="../../../../foundation-models/2603.24917-decoding-constrained-beam/">实现解读</a> · <a href="#qa-668c7dba6665932c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:decoding-constrained-beam" data-paper-title="Estimating near-verbatim extraction risk in language models with decoding-constrained beam search" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Estimating near-verbatim extraction risk in language models with decoding-constrained beam search 基础模型 AVERI / Stanford University 2026-03-26 只检查 greedy 是否生成训练原文，会漏掉许多单条概率不大、合计概率却很高的近逐字变体。普通 beam 的模型 softmax 分数也不等于实际 top-k 解码分布下的概率。本文把解码约束纳入每一步归一化，枚举部分高概率路径，对与目标后缀接近的路径求和得到确定性下界。本地用途是可审计的概率与距离算子：模型 callback 只接收前缀和已生成 token；目标后缀留在评价侧用于距离剪枝，不交给 callback。没有下载训练语料或加载被审计模型，也不把玩具转移概率称作真实记忆泄漏。 完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。本地交付是 L1 数值/协议组件，不是完整论文能力复现。完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。search 实际执行 top-k、路径 logp、带状编辑/Hamming 剪枝、确定性同分排序和末步质量求和。EOS 在非最终步被移除，最终扩展仍按原算法允许；固定长度协议不等于任意停止规则。没有实现可选的提前停止、批量 KV cache 或 GPU 模型执行，不能用 callback 次数证明原文吞吐。  评测与研究证据 近逐字提取风险 基础模型 能力证据：评测采样、读出与可靠性 为何必须top-k内部归一化且最后不能再剪到B？ 要度量的是实际top-k解码分布，不是完整softmax。每条路径概率都须按该分布累乘；末步再剪B会丢掉已付前向成本得到的有效质量，原算法保留最多B×k。剪枝后也不对剩余路径重归一化。 教学例：原模型三token概率0.5、0.3、0.2，top2变成0.625、0.375；B=1的最后一步仍应保留这两条扩展，而非只留0.625。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-853ada14e4653cef">为何必须top-k内部归一化且最后不能再剪到B？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adecoding-constrained-beam">Estimating near-verbatim extraction risk in language models with decoding-constrained beam search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · AVERI / Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>要度量的是实际top-k解码分布，不是完整softmax。每条路径概率都须按该分布累乘；末步再剪B会丢掉已付前向成本得到的有效质量，原算法保留最多B×k。剪枝后也不对剩余路径重归一化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：原模型三token概率0.5、0.3、0.2，top2变成0.625、0.375；B=1的最后一步仍应保留这两条扩展，而非只留0.625。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.24917v1">原论文</a> · <a href="../../../../foundation-models/2603.24917-decoding-constrained-beam/">实现解读</a> · <a href="#qa-853ada14e4653cef">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:decoding-constrained-beam" data-paper-title="Estimating near-verbatim extraction risk in language models with decoding-constrained beam search" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Estimating near-verbatim extraction risk in language models with decoding-constrained beam search 基础模型 AVERI / Stanford University 2026-03-26 只检查 greedy 是否生成训练原文，会漏掉许多单条概率不大、合计概率却很高的近逐字变体。普通 beam 的模型 softmax 分数也不等于实际 top-k 解码分布下的概率。本文把解码约束纳入每一步归一化，枚举部分高概率路径，对与目标后缀接近的路径求和得到确定性下界。本地用途是可审计的概率与距离算子：模型 callback 只接收前缀和已生成 token；目标后缀留在评价侧用于距离剪枝，不交给 callback。没有下载训练语料或加载被审计模型，也不把玩具转移概率称作真实记忆泄漏。 完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。本地交付是 L1 数值/协议组件，不是完整论文能力复现。完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。search 实际执行 top-k、路径 logp、带状编辑/Hamming 剪枝、确定性同分排序和末步质量求和。EOS 在非最终步被移除，最终扩展仍按原算法允许；固定长度协议不等于任意停止规则。没有实现可选的提前停止、批量 KV cache 或 GPU 模型执行，不能用 callback 次数证明原文吞吐。  评测与研究证据 近逐字提取风险 基础模型 能力证据：评测采样、读出与可靠性 CBS概率下界能否替代DetectorScope的AI文本来源检测分数？ 不能。CBS假定有目标后缀并能访问模型条件概率，衡量该前缀下近目标生成质量；DetectorScope从文本的SAE特征预测来源。一个文本容易被模型生成不等于它真的由该模型写成，两类统计也不共享标签含义。 教学例：公开常见句在模型下概率很高，仍可能完全由人类撰写；高来源检测分数也不给某段训练原文的提取概率。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e5f81f1a027a0060">CBS概率下界能否替代DetectorScope的AI文本来源检测分数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adecoding-constrained-beam">Estimating near-verbatim extraction risk in language models with decoding-constrained beam search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · AVERI / Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。CBS假定有目标后缀并能访问模型条件概率，衡量该前缀下近目标生成质量；DetectorScope从文本的SAE特征预测来源。一个文本容易被模型生成不等于它真的由该模型写成，两类统计也不共享标签含义。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：公开常见句在模型下概率很高，仍可能完全由人类撰写；高来源检测分数也不给某段训练原文的提取概率。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.24917v1">原论文</a> · <a href="../../../../foundation-models/2603.24917-decoding-constrained-beam/">实现解读</a> · <a href="#qa-e5f81f1a027a0060">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:decoding-constrained-beam" data-paper-title="Estimating near-verbatim extraction risk in language models with decoding-constrained beam search" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Estimating near-verbatim extraction risk in language models with decoding-constrained beam search 基础模型 AVERI / Stanford University 2026-03-26 只检查 greedy 是否生成训练原文，会漏掉许多单条概率不大、合计概率却很高的近逐字变体。普通 beam 的模型 softmax 分数也不等于实际 top-k 解码分布下的概率。本文把解码约束纳入每一步归一化，枚举部分高概率路径，对与目标后缀接近的路径求和得到确定性下界。本地用途是可审计的概率与距离算子：模型 callback 只接收前缀和已生成 token；目标后缀留在评价侧用于距离剪枝，不交给 callback。没有下载训练语料或加载被审计模型，也不把玩具转移概率称作真实记忆泄漏。 完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。本地交付是 L1 数值/协议组件，不是完整论文能力复现。完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。search 实际执行 top-k、路径 logp、带状编辑/Hamming 剪枝、确定性同分排序和末步质量求和。EOS 在非最终步被移除，最终扩展仍按原算法允许；固定长度协议不等于任意停止规则。没有实现可选的提前停止、批量 KV cache 或 GPU 模型执行，不能用 callback 次数证明原文吞吐。  评测与研究证据 近逐字提取风险 基础模型 能力证据：评测采样、读出与可靠性 Levenshtein的行最小值没超epsilon，为何到最后还要查D[T,T]？ 行最小值只说明当前串能与目标某个前缀低成本对齐，是中间剪枝的必要条件；完成后必须与整个目标比较。把存活直接当成功会误计尚未覆盖目标末尾的路径。bank也只是被剪前缀的潜在质量，不是成功质量。 教学例：目标abc，某部分路径与a很接近，不说明完整输出和abc距离达标。专测以穷举分布检查LB≤p≤LB+bank，宽beam才恢复完整质量。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-84ee62e986a4b99f">Levenshtein的行最小值没超epsilon，为何到最后还要查D[T,T]？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adecoding-constrained-beam">Estimating near-verbatim extraction risk in language models with decoding-constrained beam search</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · AVERI / Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>行最小值只说明当前串能与目标某个前缀低成本对齐，是中间剪枝的必要条件；完成后必须与整个目标比较。把存活直接当成功会误计尚未覆盖目标末尾的路径。bank也只是被剪前缀的潜在质量，不是成功质量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：目标abc，某部分路径与a很接近，不说明完整输出和abc距离达标。专测以穷举分布检查LB≤p≤LB+bank，宽beam才恢复完整质量。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.24917v1">原论文</a> · <a href="../../../../foundation-models/2603.24917-decoding-constrained-beam/">实现解读</a> · <a href="#qa-84ee62e986a4b99f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:cultural-cue" data-paper-title="Steering LLMs for Culturally Localized Generation" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Steering LLMs for Culturally Localized Generation 基础模型 Carnegie Mellon University 2026-03-24 文化定位失败可能是知识缺失，也可能是已有知识不易被提示词唤起。CuE 从预训练 SAE 的稀疏特征中寻找与国家标签相关的维度，建立可解释文化原型，再沿目标文化相对其他文化的差向量干预残差流。国家只是论文采用的文化代理，不能把国家均值当成每个个体的价值观。这种方法不更新语言模型参数，也不是给模型简单补上一句国家名称。它需要真实 SAE、对齐的层/特征编号和 decoder；本地只实现这些外部结果上的确定性张量部分，不生成文化判断或假装理解刻板印象。 完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。本地交付是 L1 数值/协议组件，不是完整论文能力复现。完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。max_pool_features、select_cumulative_mi、country_prototypes、steering_direction、apply_steering 依次实现上述确定性算子。张量支持 CPU/CUDA；真实 NVIDIA 验收由统一批次记录，不能由单元测试替代。  评测与研究证据 可解释文化表征与干预 基础模型 能力证据：评测采样、读出与可靠性 CuE 为什么关注隐藏文化特征，而不只再加一句国家提示？ 它要区分缺少知识和已有知识没有被唤起，使用SAE特征构造白盒干预。显式提示与特征干预可以互补，但国家原型只是论文的群体代理，不能代表每个个体。 教学例：模型知道某地区的小众菜名，却在无地点食谱中总给常见菜；沿已验证文化特征方向干预是在测试知识唤起，不证明社会文化安全。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<span id="paper-foundation-models-cultural-cue-701f9550" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7a4c318f71d636fc">CuE 为什么关注隐藏文化特征，而不只再加一句国家提示？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Acultural-cue">Steering LLMs for Culturally Localized Generation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · Carnegie Mellon University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它要区分缺少知识和已有知识没有被唤起，使用SAE特征构造白盒干预。显式提示与特征干预可以互补，但国家原型只是论文的群体代理，不能代表每个个体。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：模型知道某地区的小众菜名，却在无地点食谱中总给常见菜；沿已验证文化特征方向干预是在测试知识唤起，不证明社会文化安全。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.23301v1">原论文</a> · <a href="../../../../foundation-models/2603.23301-cultural-cue/">实现解读</a> · <a href="#qa-7a4c318f71d636fc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:cultural-cue" data-paper-title="Steering LLMs for Culturally Localized Generation" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Steering LLMs for Culturally Localized Generation 基础模型 Carnegie Mellon University 2026-03-24 文化定位失败可能是知识缺失，也可能是已有知识不易被提示词唤起。CuE 从预训练 SAE 的稀疏特征中寻找与国家标签相关的维度，建立可解释文化原型，再沿目标文化相对其他文化的差向量干预残差流。国家只是论文采用的文化代理，不能把国家均值当成每个个体的价值观。这种方法不更新语言模型参数，也不是给模型简单补上一句国家名称。它需要真实 SAE、对齐的层/特征编号和 decoder；本地只实现这些外部结果上的确定性张量部分，不生成文化判断或假装理解刻板印象。 完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。本地交付是 L1 数值/协议组件，不是完整论文能力复现。完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。max_pool_features、select_cumulative_mi、country_prototypes、steering_direction、apply_steering 依次实现上述确定性算子。张量支持 CPU/CUDA；真实 NVIDIA 验收由统一批次记录，不能由单元测试替代。  评测与研究证据 可解释文化表征与干预 基础模型 能力证据：评测采样、读出与可靠性 rho=0.1 是否就是保留10%的SAE特征？ 不是。§2.3保留按MI降序的最短集合，使累计MI达到总MI的10%。信息高度集中时只需很少维度；按特征个数截10%会改变核心算法。 教学例：四个特征MI为0.97、0.01、0.01、0.01，rho=0.5只选第一个，而不是四舍五入选一半维度。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-957214d86e09fec1">rho=0.1 是否就是保留10%的SAE特征？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Acultural-cue">Steering LLMs for Culturally Localized Generation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · Carnegie Mellon University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。§2.3保留按MI降序的最短集合，使累计MI达到总MI的10%。信息高度集中时只需很少维度；按特征个数截10%会改变核心算法。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：四个特征MI为0.97、0.01、0.01、0.01，rho=0.5只选第一个，而不是四舍五入选一半维度。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.23301v1">原论文</a> · <a href="../../../../foundation-models/2603.23301-cultural-cue/">实现解读</a> · <a href="#qa-957214d86e09fec1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:cultural-cue" data-paper-title="Steering LLMs for Culturally Localized Generation" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Steering LLMs for Culturally Localized Generation 基础模型 Carnegie Mellon University 2026-03-24 文化定位失败可能是知识缺失，也可能是已有知识不易被提示词唤起。CuE 从预训练 SAE 的稀疏特征中寻找与国家标签相关的维度，建立可解释文化原型，再沿目标文化相对其他文化的差向量干预残差流。国家只是论文采用的文化代理，不能把国家均值当成每个个体的价值观。这种方法不更新语言模型参数，也不是给模型简单补上一句国家名称。它需要真实 SAE、对齐的层/特征编号和 decoder；本地只实现这些外部结果上的确定性张量部分，不生成文化判断或假装理解刻板印象。 完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。本地交付是 L1 数值/协议组件，不是完整论文能力复现。完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。max_pool_features、select_cumulative_mi、country_prototypes、steering_direction、apply_steering 依次实现上述确定性算子。张量支持 CPU/CUDA；真实 NVIDIA 验收由统一批次记录，不能由单元测试替代。  评测与研究证据 可解释文化表征与干预 基础模型 能力证据：评测采样、读出与可靠性 CuE 和 DetectorScope 都对SAE特征max-pool，为何不是同一方法？ 池化只是共享表示操作。CuE以特征–文化MI和国家原型差构造残差干预；DetectorScope用描述验证mask和稀疏检测头作预测与特征归因。前者方向不自动构成检测器，后者头权重也不等于文化干预。 教学例：一个食物特征能区分国家，却不一定区分人类与AI文本；检测头贡献大也不意味着沿该方向生成就文化忠实。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e841df37bb0cb2cb">CuE 和 DetectorScope 都对SAE特征max-pool，为何不是同一方法？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Acultural-cue">Steering LLMs for Culturally Localized Generation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · Carnegie Mellon University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>池化只是共享表示操作。CuE以特征–文化MI和国家原型差构造残差干预；DetectorScope用描述验证mask和稀疏检测头作预测与特征归因。前者方向不自动构成检测器，后者头权重也不等于文化干预。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：一个食物特征能区分国家，却不一定区分人类与AI文本；检测头贡献大也不意味着沿该方向生成就文化忠实。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.23301v1">原论文</a> · <a href="../../../../foundation-models/2603.23301-cultural-cue/">实现解读</a> · <a href="#qa-e841df37bb0cb2cb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:cultural-cue" data-paper-title="Steering LLMs for Culturally Localized Generation" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Steering LLMs for Culturally Localized Generation 基础模型 Carnegie Mellon University 2026-03-24 文化定位失败可能是知识缺失，也可能是已有知识不易被提示词唤起。CuE 从预训练 SAE 的稀疏特征中寻找与国家标签相关的维度，建立可解释文化原型，再沿目标文化相对其他文化的差向量干预残差流。国家只是论文采用的文化代理，不能把国家均值当成每个个体的价值观。这种方法不更新语言模型参数，也不是给模型简单补上一句国家名称。它需要真实 SAE、对齐的层/特征编号和 decoder；本地只实现这些外部结果上的确定性张量部分，不生成文化判断或假装理解刻板印象。 完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。本地交付是 L1 数值/协议组件，不是完整论文能力复现。完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。max_pool_features、select_cumulative_mi、country_prototypes、steering_direction、apply_steering 依次实现上述确定性算子。张量支持 CPU/CUDA；真实 NVIDIA 验收由统一批次记录，不能由单元测试替代。  评测与研究证据 可解释文化表征与干预 基础模型 能力证据：评测采样、读出与可靠性 其他国家的基线为什么要先各自求均值再等权平均？ 公式比较目标原型与其他国家原型的平均，国家样本数不是权重。直接把其他所有断言混在一起，会让数据多的国家支配方向。decoder还必须与该层所选特征一一对齐。 教学例：B国两条值2，C国一条值0，其他国家基线为(2+0)/2=1，不是(2+2+0)/3。目标A值4时差为3而非8/3。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-9a96eaffcdc6fb16">其他国家的基线为什么要先各自求均值再等权平均？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Acultural-cue">Steering LLMs for Culturally Localized Generation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · Carnegie Mellon University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>公式比较目标原型与其他国家原型的平均，国家样本数不是权重。直接把其他所有断言混在一起，会让数据多的国家支配方向。decoder还必须与该层所选特征一一对齐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：B国两条值2，C国一条值0，其他国家基线为(2+0)/2=1，不是(2+2+0)/3。目标A值4时差为3而非8/3。</p>
<p class="ar-learning-sources">依据：数据协议与代码映射；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.23301v1">原论文</a> · <a href="../../../../foundation-models/2603.23301-cultural-cue/">实现解读</a> · <a href="#qa-9a96eaffcdc6fb16">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:thinking-to-recall" data-paper-title="Thinking to Recall: How Reasoning Unlocks Parametric Knowledge in LLMs" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Thinking to Recall: How Reasoning Unlocks Parametric Knowledge in LLMs 基础模型 Google Research 2026-03-10 推理不仅可能分解复杂任务，也可能通过额外计算和相关事实的自检索帮助单跳知识召回。论文控制同一 hybrid 模型的 reasoning ON/OFF，区分计算缓冲与 factual priming，同时发现中间事实幻觉会连带增加最终答案错误。 完整实验成本过高，不复现（审查 DONE）。诊断中的真值数组是显式教学输入，不是Agent任务成绩。L1 机制/评测组件，diagnostic only，不是完整模型能力复现。CPU组件专测已通过；没有CUDA路径，不需要GPU验收。未接入Evolve，不可据本地fixture成绩晋级。conditional_expected_accuracy 只返回汇总统计、保留/剔除题数，绝不返回被oracle选中的轨迹、行动或训练样本；默认严格要求每题100条。pass_at_k 使用无偏组合数估计。负控同时覆盖共同题目mask、逐题宏平均而非微平均、空事实集合和缺失子集。  知识与推理 参数知识召回 基础模型 能力证据：评测采样、读出与可靠性 单跳事实题不需多步逻辑，为什么thinking仍可能有帮助？ 原文区分额外token带来的计算缓冲与相关事实的factual priming，两者都可能帮助参数知识读出；并不意味着所有思考内容都正确或推理越长越好。 重复dummy trace可检测内容无关计算，而相关事实提示测试语义桥接；它们不是同一个实验。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<span id="paper-foundation-models-thinking-to-recall-75a6061f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-1f1300a5c5f8f35d">单跳事实题不需多步逻辑，为什么thinking仍可能有帮助？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Athinking-to-recall">Thinking to Recall: How Reasoning Unlocks Parametric Knowledge in LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原文区分额外token带来的计算缓冲与相关事实的factual priming，两者都可能帮助参数知识读出；并不意味着所有思考内容都正确或推理越长越好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>重复dummy trace可检测内容无关计算，而相关事实提示测试语义桥接；它们不是同一个实验。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制与公式、原文结果与限制、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.09906v1">原论文</a> · <a href="../../../../foundation-models/2603.09906-thinking-to-recall/">实现解读</a> · <a href="#qa-1f1300a5c5f8f35d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:thinking-to-recall" data-paper-title="Thinking to Recall: How Reasoning Unlocks Parametric Knowledge in LLMs" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Thinking to Recall: How Reasoning Unlocks Parametric Knowledge in LLMs 基础模型 Google Research 2026-03-10 推理不仅可能分解复杂任务，也可能通过额外计算和相关事实的自检索帮助单跳知识召回。论文控制同一 hybrid 模型的 reasoning ON/OFF，区分计算缓冲与 factual priming，同时发现中间事实幻觉会连带增加最终答案错误。 完整实验成本过高，不复现（审查 DONE）。诊断中的真值数组是显式教学输入，不是Agent任务成绩。L1 机制/评测组件，diagnostic only，不是完整模型能力复现。CPU组件专测已通过；没有CUDA路径，不需要GPU验收。未接入Evolve，不可据本地fixture成绩晋级。conditional_expected_accuracy 只返回汇总统计、保留/剔除题数，绝不返回被oracle选中的轨迹、行动或训练样本；默认严格要求每题100条。pass_at_k 使用无偏组合数估计。负控同时覆盖共同题目mask、逐题宏平均而非微平均、空事实集合和缺失子集。  知识与推理 参数知识召回 基础模型 能力证据：评测采样、读出与可靠性 三种轨迹子集为什么必须用相同的题目集合？ 若只给干净子集剔除难题，而all臂保留，会把题目难度变化误当过滤收益。原文每题100条采样，任何条件子集为空时三臂共同剔除，再算每题比例的宏平均。 A题只有1条干净轨迹、B题有90条，仍先各算题内率再等权平均，不按91条合并微平均。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-bcaa798381c505d2">三种轨迹子集为什么必须用相同的题目集合？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Athinking-to-recall">Thinking to Recall: How Reasoning Unlocks Parametric Knowledge in LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若只给干净子集剔除难题，而all臂保留，会把题目难度变化误当过滤收益。原文每题100条采样，任何条件子集为空时三臂共同剔除，再算每题比例的宏平均。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>A题只有1条干净轨迹、B题有90条，仍先各算题内率再等权平均，不按91条合并微平均。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制与公式、原文结果与限制、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.09906v1">原论文</a> · <a href="../../../../foundation-models/2603.09906-thinking-to-recall/">实现解读</a> · <a href="#qa-bcaa798381c505d2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:thinking-to-recall" data-paper-title="Thinking to Recall: How Reasoning Unlocks Parametric Knowledge in LLMs" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Thinking to Recall: How Reasoning Unlocks Parametric Knowledge in LLMs 基础模型 Google Research 2026-03-10 推理不仅可能分解复杂任务，也可能通过额外计算和相关事实的自检索帮助单跳知识召回。论文控制同一 hybrid 模型的 reasoning ON/OFF，区分计算缓冲与 factual priming，同时发现中间事实幻觉会连带增加最终答案错误。 完整实验成本过高，不复现（审查 DONE）。诊断中的真值数组是显式教学输入，不是Agent任务成绩。L1 机制/评测组件，diagnostic only，不是完整模型能力复现。CPU组件专测已通过；没有CUDA路径，不需要GPU验收。未接入Evolve，不可据本地fixture成绩晋级。conditional_expected_accuracy 只返回汇总统计、保留/剔除题数，绝不返回被oracle选中的轨迹、行动或训练样本；默认严格要求每题100条。pass_at_k 使用无偏组合数估计。负控同时覆盖共同题目mask、逐题宏平均而非微平均、空事实集合和缺失子集。  知识与推理 参数知识召回 基础模型 能力证据：评测采样、读出与可靠性 这种“优先正确事实轨迹”能像在线Agent策略一样部署吗？ 本地实现不能；它使用事后外部标注的事实真值模拟条件期望，只是离线oracle分析。要部署还需要不看gold的可靠事实验证器，并计入调用成本和误判；这不是由汇总公式自动得到的。 用gold确认哪条轨迹正确，再展示该轨迹给actor，会泄漏答案，不能算推理提升。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-26c83fa9c9887b9d">这种“优先正确事实轨迹”能像在线Agent策略一样部署吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Athinking-to-recall">Thinking to Recall: How Reasoning Unlocks Parametric Knowledge in LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>本地实现不能；它使用事后外部标注的事实真值模拟条件期望，只是离线oracle分析。要部署还需要不看gold的可靠事实验证器，并计入调用成本和误判；这不是由汇总公式自动得到的。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>用gold确认哪条轨迹正确，再展示该轨迹给actor，会泄漏答案，不能算推理提升。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制与公式、原文结果与限制、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.09906v1">原论文</a> · <a href="../../../../foundation-models/2603.09906-thinking-to-recall/">实现解读</a> · <a href="#qa-26c83fa9c9887b9d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:thinking-to-recall" data-paper-title="Thinking to Recall: How Reasoning Unlocks Parametric Knowledge in LLMs" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Thinking to Recall: How Reasoning Unlocks Parametric Knowledge in LLMs 基础模型 Google Research 2026-03-10 推理不仅可能分解复杂任务，也可能通过额外计算和相关事实的自检索帮助单跳知识召回。论文控制同一 hybrid 模型的 reasoning ON/OFF，区分计算缓冲与 factual priming，同时发现中间事实幻觉会连带增加最终答案错误。 完整实验成本过高，不复现（审查 DONE）。诊断中的真值数组是显式教学输入，不是Agent任务成绩。L1 机制/评测组件，diagnostic only，不是完整模型能力复现。CPU组件专测已通过；没有CUDA路径，不需要GPU验收。未接入Evolve，不可据本地fixture成绩晋级。conditional_expected_accuracy 只返回汇总统计、保留/剔除题数，绝不返回被oracle选中的轨迹、行动或训练样本；默认严格要求每题100条。pass_at_k 使用无偏组合数估计。负控同时覆盖共同题目mask、逐题宏平均而非微平均、空事实集合和缺失子集。  知识与推理 参数知识召回 基础模型 能力证据：评测采样、读出与可靠性 接口为什么只返回统计而不返回“最佳轨迹”？ 让正确性标签局限在独立evaluator，避免被actor或训练选择器当成oracle。函数显式输出保留题数、剔除题数与offline标记；缺少任何条件子集就报错或共同剔除，不默默补一条假事实。 所有题都没有事实轨迹时应失败，而不是返回干净准确率1。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6416371045655a44">接口为什么只返回统计而不返回“最佳轨迹”？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Athinking-to-recall">Thinking to Recall: How Reasoning Unlocks Parametric Knowledge in LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>让正确性标签局限在独立evaluator，避免被actor或训练选择器当成oracle。函数显式输出保留题数、剔除题数与offline标记；缺少任何条件子集就报错或共同剔除，不默默补一条假事实。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>所有题都没有事实轨迹时应失败，而不是返回干净准确率1。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制与公式、原文结果与限制、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.09906v1">原论文</a> · <a href="../../../../foundation-models/2603.09906-thinking-to-recall/">实现解读</a> · <a href="#qa-6416371045655a44">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:qe-length-normalization" data-paper-title="Penalizing Length: Uncovering Systematic Bias in Quality Estimation Metrics" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Penalizing Length: Uncovering Systematic Bias in Quality Estimation Metrics 基础模型 Carnegie Mellon University / Google 2025-10-24 同样没有翻译错误，较长译文却被质量估计器判得更差，会把 reranking 和基于评分的训练导向短答案。本文不把长度和真实质量相关性混在一起：对同一文档的连续金标准段落构造一至五段的前缀，尽量固定领域和质量，再观察评分漂移。缓解方案之一是在训练时预测单位长度的错误密度，在推理时乘回译文长度。它改变监督目标及其分布，不是对已经训练好的 MetricX 输出做一次除法，就能声称修好了偏差。论文还检查引入参考文本的评估方案，本地未实现该模型分支。 完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。本地交付是 L1 数值/协议组件，不是完整论文能力复现。完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。density_targets、restore_ratings 对应监督目标和输出恢复；controlled_passages 对应同文档前缀与整组过滤；within_document_differences 只计算五个控制前缀的相对评分。没有下载 WMT、加载 MetricX/Gemini、重新训练评分器或生成翻译。  评测与研究证据 翻译指标与长度偏差 基础模型 能力证据：评测采样、读出与可靠性 QE 长度偏差为何不能靠比较任意长句和短句证明？ 长短句可能本来就有不同错误率、领域和难度。论文对同文档连续金标准段落做一至五段前缀，保持假设无错质量与领域，再看指标是否系统漂移。它仍依赖后编辑金标准近似无错的前提。 教学例：同一篇新闻的前三个正确段落拼起来后评分下降，不同于拿一段简单广告与一篇难译法律长文比较。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<span id="paper-foundation-models-qe-length-normalization-fae0f407" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8afab47abd83b7e9">QE 长度偏差为何不能靠比较任意长句和短句证明？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aqe-length-normalization">Penalizing Length: Uncovering Systematic Bias in Quality Estimation Metrics</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · Carnegie Mellon University / Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长短句可能本来就有不同错误率、领域和难度。论文对同文档连续金标准段落做一至五段前缀，保持假设无错质量与领域，再看指标是否系统漂移。它仍依赖后编辑金标准近似无错的前提。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：同一篇新闻的前三个正确段落拼起来后评分下降，不同于拿一段简单广告与一篇难译法律长文比较。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.22028v1">原论文</a> · <a href="../../../../foundation-models/2510.22028-qe-length-normalization/">实现解读</a> · <a href="#qa-8afab47abd83b7e9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:qe-length-normalization" data-paper-title="Penalizing Length: Uncovering Systematic Bias in Quality Estimation Metrics" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Penalizing Length: Uncovering Systematic Bias in Quality Estimation Metrics 基础模型 Carnegie Mellon University / Google 2025-10-24 同样没有翻译错误，较长译文却被质量估计器判得更差，会把 reranking 和基于评分的训练导向短答案。本文不把长度和真实质量相关性混在一起：对同一文档的连续金标准段落构造一至五段的前缀，尽量固定领域和质量，再观察评分漂移。缓解方案之一是在训练时预测单位长度的错误密度，在推理时乘回译文长度。它改变监督目标及其分布，不是对已经训练好的 MetricX 输出做一次除法，就能声称修好了偏差。论文还检查引入参考文本的评估方案，本地未实现该模型分支。 完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。本地交付是 L1 数值/协议组件，不是完整论文能力复现。完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。density_targets、restore_ratings 对应监督目标和输出恢复；controlled_passages 对应同文档前缀与整组过滤；within_document_differences 只计算五个控制前缀的相对评分。没有下载 WMT、加载 MetricX/Gemini、重新训练评分器或生成翻译。  评测与研究证据 翻译指标与长度偏差 基础模型 能力证据：评测采样、读出与可靠性 把现成 MetricX 输出除以长度，就复现了训练归一化吗？ 没有。原文把训练标签变为R/|h|，训练预测密度的模型，再把预测密度乘回同口径长度。冻结模型的后处理没有改变训练分布；本地只执行目标变换与恢复，不声称模型已去偏。 教学例：同为错误评分−5，10与20个计量单位的训练目标为−0.5与−0.25；乘回后都为−5，但这些数值不证明一个冻结模型真的学会密度。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-499312e689768aec">把现成 MetricX 输出除以长度，就复现了训练归一化吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aqe-length-normalization">Penalizing Length: Uncovering Systematic Bias in Quality Estimation Metrics</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · Carnegie Mellon University / Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。原文把训练标签变为R/|h|，训练预测密度的模型，再把预测密度乘回同口径长度。冻结模型的后处理没有改变训练分布；本地只执行目标变换与恢复，不声称模型已去偏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：同为错误评分−5，10与20个计量单位的训练目标为−0.5与−0.25；乘回后都为−5，但这些数值不证明一个冻结模型真的学会密度。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.22028v1">原论文</a> · <a href="../../../../foundation-models/2510.22028-qe-length-normalization/">实现解读</a> · <a href="#qa-499312e689768aec">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:qe-length-normalization" data-paper-title="Penalizing Length: Uncovering Systematic Bias in Quality Estimation Metrics" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Penalizing Length: Uncovering Systematic Bias in Quality Estimation Metrics 基础模型 Carnegie Mellon University / Google 2025-10-24 同样没有翻译错误，较长译文却被质量估计器判得更差，会把 reranking 和基于评分的训练导向短答案。本文不把长度和真实质量相关性混在一起：对同一文档的连续金标准段落构造一至五段的前缀，尽量固定领域和质量，再观察评分漂移。缓解方案之一是在训练时预测单位长度的错误密度，在推理时乘回译文长度。它改变监督目标及其分布，不是对已经训练好的 MetricX 输出做一次除法，就能声称修好了偏差。论文还检查引入参考文本的评估方案，本地未实现该模型分支。 完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。本地交付是 L1 数值/协议组件，不是完整论文能力复现。完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。density_targets、restore_ratings 对应监督目标和输出恢复；controlled_passages 对应同文档前缀与整组过滤；within_document_differences 只计算五个控制前缀的相对评分。没有下载 WMT、加载 MetricX/Gemini、重新训练评分器或生成翻译。  评测与研究证据 翻译指标与长度偏差 基础模型 能力证据：评测采样、读出与可靠性 错误密度训练与验证集温度校准解决同一个问题吗？ 不是。前者改变监督目标对长度的尺度关系；温度校准改变已有分类概率的锐度，通常不改变预测类别。二者都须明确数据和计量，但不能因为都叫校准就用温度替代MetricX重训。 教学例：将二类logit除以2能降低置信度，却不会使翻译错误评分自动按译文长度学习。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ab022e08119760af">错误密度训练与验证集温度校准解决同一个问题吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aqe-length-normalization">Penalizing Length: Uncovering Systematic Bias in Quality Estimation Metrics</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · Carnegie Mellon University / Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。前者改变监督目标对长度的尺度关系；温度校准改变已有分类概率的锐度，通常不改变预测类别。二者都须明确数据和计量，但不能因为都叫校准就用温度替代MetricX重训。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：将二类logit除以2能降低置信度，却不会使翻译错误评分自动按译文长度学习。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.22028v1">原论文</a> · <a href="../../../../foundation-models/2510.22028-qe-length-normalization/">实现解读</a> · <a href="#qa-ab022e08119760af">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:qe-length-normalization" data-paper-title="Penalizing Length: Uncovering Systematic Bias in Quality Estimation Metrics" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Penalizing Length: Uncovering Systematic Bias in Quality Estimation Metrics 基础模型 Carnegie Mellon University / Google 2025-10-24 同样没有翻译错误，较长译文却被质量估计器判得更差，会把 reranking 和基于评分的训练导向短答案。本文不把长度和真实质量相关性混在一起：对同一文档的连续金标准段落构造一至五段的前缀，尽量固定领域和质量，再观察评分漂移。缓解方案之一是在训练时预测单位长度的错误密度，在推理时乘回译文长度。它改变监督目标及其分布，不是对已经训练好的 MetricX 输出做一次除法，就能声称修好了偏差。论文还检查引入参考文本的评估方案，本地未实现该模型分支。 完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。本地交付是 L1 数值/协议组件，不是完整论文能力复现。完整实验成本过高，不复现（审查 DONE）；未执行模型/API训练，不启用自动重试或 evolve 晋级。density_targets、restore_ratings 对应监督目标和输出恢复；controlled_passages 对应同文档前缀与整组过滤；within_document_differences 只计算五个控制前缀的相对评分。没有下载 WMT、加载 MetricX/Gemini、重新训练评分器或生成翻译。  评测与研究证据 翻译指标与长度偏差 基础模型 能力证据：评测采样、读出与可靠性 为什么整组500-token门槛不能用独立段落的token数求和？ 分词依赖边界，串接后的token数不一定等于各段独立计数之和。接口要求五个实际前缀计数；第五超过500则丢弃整组，否则长度组不再是同一控制文档。长度单位也必须在密度训练与恢复时一致。 教学例：五段分别计100并不保证串接后恰好500；实测第五前缀501时五条都拒绝，不只删最长一条。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8d2fbee47169ed6a">为什么整组500-token门槛不能用独立段落的token数求和？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aqe-length-normalization">Penalizing Length: Uncovering Systematic Bias in Quality Estimation Metrics</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · Carnegie Mellon University / Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分词依赖边界，串接后的token数不一定等于各段独立计数之和。接口要求五个实际前缀计数；第五超过500则丢弃整组，否则长度组不再是同一控制文档。长度单位也必须在密度训练与恢复时一致。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：五段分别计100并不保证串接后恰好500；实测第五前缀501时五条都拒绝，不只删最长一条。</p>
<p class="ar-learning-sources">依据：数据协议与代码映射；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.22028v1">原论文</a> · <a href="../../../../foundation-models/2510.22028-qe-length-normalization/">实现解读</a> · <a href="#qa-8d2fbee47169ed6a">问题链接</a></p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:rosetta-unification" data-paper-title="Beyond the Rosetta Stone: Unification Forces in Generalization Dynamics" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Beyond the Rosetta Stone: Unification Forces in Generalization Dynamics 基础模型 Google DeepMind 2025-08-14 同一事实以不同语言出现时，模型可能把它们存成互不相通的表征。作者在受控合成知识图谱上从零训练小型 Transformer，分别改变平行事实比例、语言频率差异和语言可提取性，发现同语言准确率接近满分并不代表跨语言迁移良好。 完整实验成本过高，不复现（审查 DONE）。诊断验证尺度不变性、平均比值及集合自相似不等于对角线常数1。L1 机制/评测组件，diagnostic only，不是完整模型能力复现。CPU组件专测已通过；没有CUDA路径，不需要GPU验收。未接入Evolve，不可据本地fixture成绩晋级。average_cosine 与 unification_score 实现有限、非零表示的集合余弦和逐组比值，拒绝接近零的分母。诊断验证尺度不变性、平均比值及集合自相似不等于对角线常数1。外部特征没有由本地模型生成；诊断不证明跨语言准确率提高。  预训练与知识表示 跨语言知识迁移 基础模型 能力证据：评测采样、读出与可靠性 同语言召回接近100%，为什么仍可能跨语言答错？ 模型可能借助语言特征形成分离的知识表示；同一事实在训练语言中可读出，不代表另一语言能访问。论文用相同事实、不同语言分布的受控训练区分两者，不能用ID分数替代跨语言validation。 某个出生城市事实只用语言A表达；A的改写题全对，B的问题仍可能错。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<span id="paper-foundation-models-rosetta-unification-42d28816" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e283ba490c9106d0">同语言召回接近100%，为什么仍可能跨语言答错？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Arosetta-unification">Beyond the Rosetta Stone: Unification Forces in Generalization Dynamics</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>模型可能借助语言特征形成分离的知识表示；同一事实在训练语言中可读出，不代表另一语言能访问。论文用相同事实、不同语言分布的受控训练区分两者，不能用ID分数替代跨语言validation。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某个出生城市事实只用语言A表达；A的改写题全对，B的问题仍可能错。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制与公式、原文结果与限制、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.11017v1">原论文</a> · <a href="../../../../foundation-models/2508.11017-rosetta-unification/">实现解读</a> · <a href="#qa-e283ba490c9106d0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:rosetta-unification" data-paper-title="Beyond the Rosetta Stone: Unification Forces in Generalization Dynamics" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Beyond the Rosetta Stone: Unification Forces in Generalization Dynamics 基础模型 Google DeepMind 2025-08-14 同一事实以不同语言出现时，模型可能把它们存成互不相通的表征。作者在受控合成知识图谱上从零训练小型 Transformer，分别改变平行事实比例、语言频率差异和语言可提取性，发现同语言准确率接近满分并不代表跨语言迁移良好。 完整实验成本过高，不复现（审查 DONE）。诊断验证尺度不变性、平均比值及集合自相似不等于对角线常数1。L1 机制/评测组件，diagnostic only，不是完整模型能力复现。CPU组件专测已通过；没有CUDA路径，不需要GPU验收。未接入Evolve，不可据本地fixture成绩晋级。average_cosine 与 unification_score 实现有限、非零表示的集合余弦和逐组比值，拒绝接近零的分母。诊断验证尺度不变性、平均比值及集合自相似不等于对角线常数1。外部特征没有由本地模型生成；诊断不证明跨语言准确率提高。  预训练与知识表示 跨语言知识迁移 基础模型 能力证据：评测采样、读出与可靠性 统一度为什么要明确同语言基线，不能只算两个向量的余弦？ 原文比较跨语言语义等价组与同语言基线组的平均相似度，并对比值取平均。自余弦恒为1会改变定义；本地要求显式传入组和基线，并拒绝近零分母，不猜测隐藏状态与事实配对。 两组的numerator/denominator分别是0.8/0.6和0.6/0.8，分数是两个比值的均值，不是(0.8+0.6)/(0.6+0.8)。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8230e66a99e4d014">统一度为什么要明确同语言基线，不能只算两个向量的余弦？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Arosetta-unification">Beyond the Rosetta Stone: Unification Forces in Generalization Dynamics</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原文比较跨语言语义等价组与同语言基线组的平均相似度，并对比值取平均。自余弦恒为1会改变定义；本地要求显式传入组和基线，并拒绝近零分母，不猜测隐藏状态与事实配对。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两组的numerator/denominator分别是0.8/0.6和0.6/0.8，分数是两个比值的均值，不是(0.8+0.6)/(0.6+0.8)。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制与公式、原文结果与限制、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.11017v1">原论文</a> · <a href="../../../../foundation-models/2508.11017-rosetta-unification/">实现解读</a> · <a href="#qa-8230e66a99e4d014">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:rosetta-unification" data-paper-title="Beyond the Rosetta Stone: Unification Forces in Generalization Dynamics" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Beyond the Rosetta Stone: Unification Forces in Generalization Dynamics 基础模型 Google DeepMind 2025-08-14 同一事实以不同语言出现时，模型可能把它们存成互不相通的表征。作者在受控合成知识图谱上从零训练小型 Transformer，分别改变平行事实比例、语言频率差异和语言可提取性，发现同语言准确率接近满分并不代表跨语言迁移良好。 完整实验成本过高，不复现（审查 DONE）。诊断验证尺度不变性、平均比值及集合自相似不等于对角线常数1。L1 机制/评测组件，diagnostic only，不是完整模型能力复现。CPU组件专测已通过；没有CUDA路径，不需要GPU验收。未接入Evolve，不可据本地fixture成绩晋级。average_cosine 与 unification_score 实现有限、非零表示的集合余弦和逐组比值，拒绝接近零的分母。诊断验证尺度不变性、平均比值及集合自相似不等于对角线常数1。外部特征没有由本地模型生成；诊断不证明跨语言准确率提高。  预训练与知识表示 跨语言知识迁移 基础模型 能力证据：评测采样、读出与可靠性 Rosetta与Thinking to Recall都涉及事实，干预位置有什么不同？ Rosetta观察/干预预训练语言分布及表示统一度；Thinking to Recall分析推理时自生成事实及其正确性。前者的相似度不是事实真值judge，后者的oracle条件准确率也不证明跨语言表示统一。 提高两语言表示相似度，不会自动判断某条中间生日事实是否幻觉；过滤正确事实也不保证低资源语言可读出知识。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ccd798e2e8e68a79">Rosetta与Thinking to Recall都涉及事实，干预位置有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Arosetta-unification">Beyond the Rosetta Stone: Unification Forces in Generalization Dynamics</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Rosetta观察/干预预训练语言分布及表示统一度；Thinking to Recall分析推理时自生成事实及其正确性。前者的相似度不是事实真值judge，后者的oracle条件准确率也不证明跨语言表示统一。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>提高两语言表示相似度，不会自动判断某条中间生日事实是否幻觉；过滤正确事实也不保证低资源语言可读出知识。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制与公式、原文结果与限制、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.11017v1">原论文</a> · <a href="../../../../foundation-models/2508.11017-rosetta-unification/">实现解读</a> · <a href="#qa-ccd798e2e8e68a79">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:rosetta-unification" data-paper-title="Beyond the Rosetta Stone: Unification Forces in Generalization Dynamics" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Beyond the Rosetta Stone: Unification Forces in Generalization Dynamics 基础模型 Google DeepMind 2025-08-14 同一事实以不同语言出现时，模型可能把它们存成互不相通的表征。作者在受控合成知识图谱上从零训练小型 Transformer，分别改变平行事实比例、语言频率差异和语言可提取性，发现同语言准确率接近满分并不代表跨语言迁移良好。 完整实验成本过高，不复现（审查 DONE）。诊断验证尺度不变性、平均比值及集合自相似不等于对角线常数1。L1 机制/评测组件，diagnostic only，不是完整模型能力复现。CPU组件专测已通过；没有CUDA路径，不需要GPU验收。未接入Evolve，不可据本地fixture成绩晋级。average_cosine 与 unification_score 实现有限、非零表示的集合余弦和逐组比值，拒绝接近零的分母。诊断验证尺度不变性、平均比值及集合自相似不等于对角线常数1。外部特征没有由本地模型生成；诊断不证明跨语言准确率提高。  预训练与知识表示 跨语言知识迁移 基础模型 能力证据：评测采样、读出与可靠性 本地比值测试通过，能否宣称复现0.97的相关系数？ 不能。0.97来自作者跨多次模型训练的表示与独立准确率联合测量。本地只做给定数组的算术，既无模型特征抽取，也无跨语言答案；新实验还必须用validation选择而非test调参。 随机矩阵的比值有限只说明数值核可算，不是110次训练相关性证据。 2026-11-13">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-91f883c07674fabc">本地比值测试通过，能否宣称复现0.97的相关系数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Arosetta-unification">Beyond the Rosetta Stone: Unification Forces in Generalization Dynamics</a></p>
<p class="ar-learning-card__meta">问答新增：2026-11-13 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。0.97来自作者跨多次模型训练的表示与独立准确率联合测量。本地只做给定数组的算术，既无模型特征抽取，也无跨语言答案；新实验还必须用validation选择而非test调参。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>随机矩阵的比值有限只说明数值核可算，不是110次训练相关性证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制与公式、原文结果与限制、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.11017v1">原论文</a> · <a href="../../../../foundation-models/2508.11017-rosetta-unification/">实现解读</a> · <a href="#qa-91f883c07674fabc">问题链接</a></p>
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
