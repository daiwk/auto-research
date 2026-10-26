---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 能力证据：评测采样、读出与可靠性

[基础模型](index.md) / 子主题导学 · 约 3 分钟 · 13 张论文卡

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

## 这个子主题的论文卡片

导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">
<div class="ar-learning-controls">
<label for="learning-search">搜索卡片
<input id="learning-search" type="search" data-learning-search placeholder="搜索论文、机制、机构或本地边界"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">共 13 张卡片</p>
<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Building Auditable AI Text Detectors with Sparse Autoencoders 基础模型 University of Pennsylvania 2026-10-21 DetectorScope 把黑盒检测器的残差流转换为 SAE 稀疏特征，按 token 取最大值后跨层拼接，再用自动解释的验证分数筛掉不可靠概念。轻量 L1 线性头只使用保留特征，因此每个预测能分解成可置零核验的概念贡献，而不是在黑盒输出后补写理由。原文还包含 SAE 训练、Gemini 描述生成与验证、大语料特征缓存和多条件检测实验；这些不是本地稀疏头的隐式功能。描述文字存在不代表语义正确，Spearman 分数也不是人工审查或误伤风险担保。 完整实验成本过高，不复现（审查 DONE）。诊断使用小规模合成激活张量，12 个训练文档、4 个隔离预测输入；本地仅实现 L1 小张量机制：冻结 SAE 特征接口、描述验证分数、稀疏线性头与精确归因。不是完整 AI 文本检测器，也不是公开 benchmark 能力复现。完整实验成本过高，不复现（审查 DONE）。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  可解释性 稀疏特征与可审计检测 基础模型 能力证据：评测采样、读出与可靠性">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<h2 id="paper-foundation-models-detector-scope-a45f37d9">Building Auditable AI Text Detectors with Sparse Autoencoders</h2>
<p class="ar-learning-card__meta">University of Pennsylvania · 论文公开：2026-10-21</p>
<p><strong>方法要点：</strong>DetectorScope 把黑盒检测器的残差流转换为 SAE 稀疏特征，按 token 取最大值后跨层拼接，再用自动解释的验证分数筛掉不可靠概念。轻量 L1 线性头只使用保留特征，因此每个预测能分解成可置零核验的概念贡献，而不是在黑盒输出后补写理由。原文还包含 SAE 训练、Gemini 描述生成与验证、大语料特征缓存和多条件检测实验；这些不是本地稀疏头的隐式功能。描述文字存在不代表语义正确，Spearman 分数也不是人工审查或误伤风险担保。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）。诊断使用小规模合成激活张量，12 个训练文档、4 个隔离预测输入；本地仅实现 L1 小张量机制：冻结 SAE 特征接口、描述验证分数、稀疏线性头与精确归因。不是完整 AI 文本检测器，也不是公开 benchmark 能力复现。完整实验成本过高，不复现（审查 DONE）。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30006v1">原论文</a> · <a href="../../../../foundation-models/2610.30006-detector-scope/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="DeepSEA: A Multilingual Evaluation Benchmark for Southeast Asia 基础模型 Google Research 2026-10-19 现有多语言评测对东南亚低资源语言覆盖不足。DeepSEA 通过专业翻译与质量审核扩展五类公开任务，支持按语言资源层级比较推理、问答和生成表现；研究同时分析英语中转、错误类型及 tokenizer 效率。它是 benchmark，而非改变语言模型参数的训练算法。 因此完整模型实验成本过高，不复现（审查 DONE），不下载大权重、不试跑全量矩阵、不自动重试。诊断只报告 scorer_contract_cases、reference_score_error、coverage_rejection_count 和 model_calls=0。DeepSEATask 深复制 evaluator 私有参考；预测回调仅接收不可变 PublicExample。各任务用字段白名单重建公开输入：问题、选项、上下文或源文本；answer、answer_with_cot、附加 metadata 和 few-shot 示例不会自动流入预测。预测按固定的语言/学科/行号绑定；  多语言与分词 公开评测协议 基础模型 能力证据：评测采样、读出与可靠性">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<h2 id="paper-foundation-models-deepsea-86ba1d33">DeepSEA: A Multilingual Evaluation Benchmark for Southeast Asia</h2>
<p class="ar-learning-card__meta">Google Research · 论文公开：2026-10-19</p>
<p><strong>方法要点：</strong>现有多语言评测对东南亚低资源语言覆盖不足。DeepSEA 通过专业翻译与质量审核扩展五类公开任务，支持按语言资源层级比较推理、问答和生成表现；研究同时分析英语中转、错误类型及 tokenizer 效率。它是 benchmark，而非改变语言模型参数的训练算法。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>因此完整模型实验成本过高，不复现（审查 DONE），不下载大权重、不试跑全量矩阵、不自动重试。诊断只报告 scorer_contract_cases、reference_score_error、coverage_rejection_count 和 model_calls=0。DeepSEATask 深复制 evaluator 私有参考；预测回调仅接收不可变 PublicExample。各任务用字段白名单重建公开输入：问题、选项、上下文或源文本；answer、answer_with_cot、附加 metadata 和 few-shot 示例不会自动流入预测。预测按固定的语言/学科/行号绑定；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.26155v1">原论文</a> · <a href="../../../../foundation-models/2610.26155-deepsea/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Words Speak Louder Than Order: A Behavioral Evaluation of Gemma 4 基础模型 Google 2026-09-25 论文把双文档冲突中的词偏好、来源措辞和呈现顺序分别测量。方法与资源已核：四路交叉、十种提示条件、跨条件共同保留集，以及未筛选敏感性分析。研究范围是单模型、短上下文、英文单词选择；不是新的训练算法，也不是神经回路证据。 故完整模型实验记 not_run_scope_limited_protocol，不是已验证能力，也不在没有成本依据时硬标为“成本过高”。four_cell_effects 执行真实四路线性对照；analyze_cells 要求十条件、唯一项目ID、同序同量、有限数字，并同时输出主分析和敏感性分析。bca_interval 延迟加载 SciPy，采用9,999次、seed42、BCa95%；TOST使用0.15 nats界限和BCa90%。BCa失败保留 failed，零方差保留 degenerate；两者 equivalent=null，不静默改成percentile，不把退化输入伪造成通过。  公开评测协议 来源与顺序偏差 基础模型 能力证据：评测采样、读出与可靠性">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<h2 id="paper-foundation-models-gemma-priority-protocol-ec648fc1">Words Speak Louder Than Order: A Behavioral Evaluation of Gemma 4</h2>
<p class="ar-learning-card__meta">Google · 论文公开：2026-09-25</p>
<p><strong>方法要点：</strong>论文把双文档冲突中的词偏好、来源措辞和呈现顺序分别测量。方法与资源已核：四路交叉、十种提示条件、跨条件共同保留集，以及未筛选敏感性分析。研究范围是单模型、短上下文、英文单词选择；不是新的训练算法，也不是神经回路证据。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>故完整模型实验记 not_run_scope_limited_protocol，不是已验证能力，也不在没有成本依据时硬标为“成本过高”。four_cell_effects 执行真实四路线性对照；analyze_cells 要求十条件、唯一项目ID、同序同量、有限数字，并同时输出主分析和敏感性分析。bca_interval 延迟加载 SciPy，采用9,999次、seed42、BCa95%；TOST使用0.15 nats界限和BCa90%。BCa失败保留 failed，零方差保留 degenerate；两者 equivalent=null，不静默改成percentile，不把退化输入伪造成通过。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.30716v1">原论文</a> · <a href="../../../../foundation-models/2609.30716-gemma-priority-protocol/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="How Calibration Content Shapes Attention-Based Reranking 基础模型 UC San Diego 2026-09-15 固定v1 Section3 Eq4–7：ΔN=s(empty,I)−s(empty,empty)，Sλ=s(q,I)−[λs(empty,I)+(1−λ)s(empty,empty)]；λ1标准ICR、λ0bare-null。调用方真实三pass提分数并保证doc identity对齐；λ只能validation选。论文oracle λ对全数据查询调参，不能当独立test结果。 成本过高，不复现（审查 DONE）。Gemma3-4B/Qwen3-4B/Llama3.1-8B/Qwen3-14B，top100每doc130tokens、16Kcontext三prefill，多benchmark/5fold/λ网格/QRhead选择；单A10040GB配置。完整模型加载和广泛矩阵超短时组件预算；不宣称真实retrieval改善。输入是已有三次模型attention读出的、相同doc ID顺序下的分数。本地实现Eq4–7及稳定ranking，没有真实attention extractor、ICR outlier filter/QRhead选择、LLM加载或工业线上A/B；  基础模型检索与排序 注意力读出与校准 基础模型 能力证据：评测采样、读出与可靠性">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<h2 id="paper-foundation-models-interpolated-null-calibration-34c35a07">How Calibration Content Shapes Attention-Based Reranking</h2>
<p class="ar-learning-card__meta">UC San Diego · 论文公开：2026-09-15</p>
<p><strong>方法要点：</strong>固定v1 Section3 Eq4–7：ΔN=s(empty,I)−s(empty,empty)，Sλ=s(q,I)−[λs(empty,I)+(1−λ)s(empty,empty)]；λ1标准ICR、λ0bare-null。调用方真实三pass提分数并保证doc identity对齐；λ只能validation选。论文oracle λ对全数据查询调参，不能当独立test结果。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。Gemma3-4B/Qwen3-4B/Llama3.1-8B/Qwen3-14B，top100每doc130tokens、16Kcontext三prefill，多benchmark/5fold/λ网格/QRhead选择；单A10040GB配置。完整模型加载和广泛矩阵超短时组件预算；不宣称真实retrieval改善。输入是已有三次模型attention读出的、相同doc ID顺序下的分数。本地实现Eq4–7及稳定ranking，没有真实attention extractor、ICR outlier filter/QRhead选择、LLM加载或工业线上A/B；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17764v1">原论文</a> · <a href="../../../../foundation-models/2609.17764-interpolated-null-calibration/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="CritICL: Inference-Time Weak-to-Strong Generalization from Small Language Model Failure Modes 基础模型 The Ohio State University 2026-08-27 弱模型错误不是随机噪声，而会聚成可跨模型尺度迁移的失败模式。CritICL 离线归纳 CritBank；static 使用全局高频失败模式，dynamic 根据当前输入检索相关 critique，再让强模型只生成一次答案。 复现级别：模型无关核心机制。复现级别：模型无关核心机制。实现 CritBank、静态/动态检索和单次推理提示构造，不伪造 checkpoint 指标。单元测试覆盖确定性 static/dynamic 检索、failure-mode 去重和零在线弱模型调用。当前没有下载大 checkpoint，因此不发布准确率；该机制也没有冒充 Micro-LLM 结构算子。  弱模型失败模式 ICL 基础模型 能力证据：评测采样、读出与可靠性">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<h2 id="paper-foundation-models-criticl-4a912854">CritICL: Inference-Time Weak-to-Strong Generalization from Small Language Model Failure Modes</h2>
<p class="ar-learning-card__meta">The Ohio State University · 论文公开：2026-08-27</p>
<p><strong>方法要点：</strong>弱模型错误不是随机噪声，而会聚成可跨模型尺度迁移的失败模式。CritICL 离线归纳 CritBank；static 使用全局高频失败模式，dynamic 根据当前输入检索相关 critique，再让强模型只生成一次答案。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：模型无关核心机制。复现级别：模型无关核心机制。实现 CritBank、静态/动态检索和单次推理提示构造，不伪造 checkpoint 指标。单元测试覆盖确定性 static/dynamic 检索、failure-mode 去重和零在线弱模型调用。当前没有下载大 checkpoint，因此不发布准确率；该机制也没有冒充 Micro-LLM 结构算子。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27455">原论文</a> · <a href="../../../../foundation-models/2608.27455-criticl/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Fast A/B/n Testing: Exact Multi-Policy Comparison via Tree-Coupled Feedback Sharing 基础模型 New York University 2026-08-13 用最大耦合和最小生成树共享相同决策的反馈，同时保持每个自适应策略的边际轨迹分布不变。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 independent A/B/n feedback，实验组为 tcab；单 seed 变化为 +0.00% 个百分点。  评测基础设施 在线实验 基础模型 能力证据：评测采样、读出与可靠性">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<h2 id="paper-foundation-models-tcab-036a095f">Fast A/B/n Testing: Exact Multi-Policy Comparison via Tree-Coupled Feedback Sharing</h2>
<p class="ar-learning-card__meta">New York University · 论文公开：2026-08-13</p>
<p><strong>方法要点：</strong>用最大耦合和最小生成树共享相同决策的反馈，同时保持每个自适应策略的边际轨迹分布不变。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 independent A/B/n feedback，实验组为 tcab；单 seed 变化为 +0.00% 个百分点。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.12831">原论文</a> · <a href="../../../../reproductions/2608.12831-tcab/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Detecting Safety Training Modification in Language Models via Activation Analysis 基础模型 Google Cloud 2026-08-06 通过三个安全相关概念的对照输入，寻找中层激活的类别分离与方向；第一层检查分离程度，第二层与同架构基线比较方向和漂移。该结构信号存在明确盲区，不能替代行为安全评测。核心见§IV，代码约定核对固定上游 extractor.py。 十四模型、多权重族及行为生成的完整campaign成本过高，不复现（审查 DONE） GPU回执只支持真实checkpoint诊断，不是安全能力认证。实现最后token提取、层扫描、差分方向、分离度、两层检测及独立数值测试。固定官方48对输入经静态AST核对，与原始 concepts.py 全部相同；保留Google版权及Apache许可全文，JSON转换新增来源说明但未修改输入对文字，不执行上游代码、不执行输入文字、不生成任何回答。  评测与可靠性 激活安全结构诊断 基础模型 能力证据：评测采样、读出与可靠性">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<h2 id="paper-foundation-models-activation-model-scanner-171bac1e">Detecting Safety Training Modification in Language Models via Activation Analysis</h2>
<p class="ar-learning-card__meta">Google Cloud · 论文公开：2026-08-06</p>
<p><strong>方法要点：</strong>通过三个安全相关概念的对照输入，寻找中层激活的类别分离与方向；第一层检查分离程度，第二层与同架构基线比较方向和漂移。该结构信号存在明确盲区，不能替代行为安全评测。核心见§IV，代码约定核对固定上游 extractor.py。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>十四模型、多权重族及行为生成的完整campaign成本过高，不复现（审查 DONE） GPU回执只支持真实checkpoint诊断，不是安全能力认证。实现最后token提取、层扫描、差分方向、分离度、两层检测及独立数值测试。固定官方48对输入经静态AST核对，与原始 concepts.py 全部相同；保留Google版权及Apache许可全文，JSON转换新增来源说明但未修改输入对文字，不执行上游代码、不执行输入文字、不生成任何回答。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05578">原论文</a> · <a href="../../../../foundation-models/2608.05578-activation-model-scanner/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Cross-Lingual Exploration for Parametric Knowledge 基础模型 The Hebrew University of Jerusalem 2026-06-23 Sec.3.1–4.4与Appendix C/E：完整提示保持原问题语言，majority/minority-aware实际使用语言模型提示聚合而非简单字符串计数，语义正确性和跨语言一致性也由Gemini判定。把counter或字符串翻译器当主模型会破坏核心；本轮不造heuristic组件。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。状态：仅文献与成本收录，没有可执行能力adapter，不以heuristic冒充核心模型。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本轮不提供可运行模型、loss包装或伪测试。库里已有通用KL/RL/统计工具并不构成本文核心流程；原文语义模型、API多轮生成或大规模训练不能用手工规则替换。仅保存经过核验的方法、资源、源码状态与原图，终态为 not_reproduced_high_cost。后续不得自动移回待训练队列。  多语言推理与评估 参数知识探索与聚合 基础模型 能力证据：评测采样、读出与可靠性">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<h2 id="paper-foundation-models-cross-lingual-exploration-96009007">Cross-Lingual Exploration for Parametric Knowledge</h2>
<p class="ar-learning-card__meta">The Hebrew University of Jerusalem · 论文公开：2026-06-23</p>
<p><strong>方法要点：</strong>Sec.3.1–4.4与Appendix C/E：完整提示保持原问题语言，majority/minority-aware实际使用语言模型提示聚合而非简单字符串计数，语义正确性和跨语言一致性也由Gemini判定。把counter或字符串翻译器当主模型会破坏核心；本轮不造heuristic组件。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。状态：仅文献与成本收录，没有可执行能力adapter，不以heuristic冒充核心模型。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本轮不提供可运行模型、loss包装或伪测试。库里已有通用KL/RL/统计工具并不构成本文核心流程；原文语义模型、API多轮生成或大规模训练不能用手工规则替换。仅保存经过核验的方法、资源、源码状态与原图，终态为 not_reproduced_high_cost。后续不得自动移回待训练队列。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.24579v1">原论文</a> · <a href="../../../../foundation-models/2606.24579-cross-lingual-exploration/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="XLGoBench: Detecting cross-lingual skill gaps with algorithmic tasks 基础模型 Google DeepMind 2026-05-29 固定v1 Section2+AppendixC：SLT财富/系数整数−9..9并jumbled chain；DSA状态/动作数相同；PrDSA15动作、传播完整状态概率、top8集合顺序无关；GraphSP唯一最短路（本地rho0 backbone+bypass固定例）；T-RankHamiltonian DAG+transitive edges、nodes:edges1:3。callback只收task/problem白名单深拷贝，score完整JSON，无LLMjudge。 成本过高，不复现（审查 DONE）。本地仅5任务结构化诊断、没有代造已验证翻译或跨语言accuracy。原文4模型×5算法×7语言×20复杂度×每级50题，包含frontierAPI和Gemma31B，另有重复/置信区间拟合。完整矩阵和人工验证翻译不跑；本地仅5任务结构化诊断、没有代造已验证翻译或跨语言accuracy。只交付结构化小题、五个精确scorer与gold隔离接口。没有下载Zenodo补充包，不复制其模板，不自动翻译成七语后声称已人工校验；也未实现完整复杂度扫描、gamma/SMD置信区间拟合或任何LLM能力比较。  跨语言评测 算法推理与评测隔离 基础模型 能力证据：评测采样、读出与可靠性">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<h2 id="paper-foundation-models-xlgobench-677fa08c">XLGoBench: Detecting cross-lingual skill gaps with algorithmic tasks</h2>
<p class="ar-learning-card__meta">Google DeepMind · 论文公开：2026-05-29</p>
<p><strong>方法要点：</strong>固定v1 Section2+AppendixC：SLT财富/系数整数−9..9并jumbled chain；DSA状态/动作数相同；PrDSA15动作、传播完整状态概率、top8集合顺序无关；GraphSP唯一最短路（本地rho0 backbone+bypass固定例）；T-RankHamiltonian DAG+transitive edges、nodes:edges1:3。callback只收task/problem白名单深拷贝，score完整JSON，无LLMjudge。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。本地仅5任务结构化诊断、没有代造已验证翻译或跨语言accuracy。原文4模型×5算法×7语言×20复杂度×每级50题，包含frontierAPI和Gemma31B，另有重复/置信区间拟合。完整矩阵和人工验证翻译不跑；本地仅5任务结构化诊断、没有代造已验证翻译或跨语言accuracy。只交付结构化小题、五个精确scorer与gold隔离接口。没有下载Zenodo补充包，不复制其模板，不自动翻译成七语后声称已人工校验；也未实现完整复杂度扫描、gamma/SMD置信区间拟合或任何LLM能力比较。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.30788v1">原论文</a> · <a href="../../../../foundation-models/2605.30788-xlgobench/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="ProEval: Proactive Failure Discovery and Efficient Performance Estimation for Generative AI Evaluation 基础模型 Google DeepMind 2026-04-25 昂贵模型或评审器不适合每次全量评分。ProEval复用历史模型之间逐题表现的相关性，形成目标模型的概率评分替身；目标分数只在对应题被选中后传入更新。主源：v1 §2.1–2.4 Eq2、5、7、10、12。 完整多基准/API实验成本过高，不复现（审查DONE）；仅4份历史评分数学夹具和4题目标分数；采集器只得到已查询分数，不接受整个隐藏目标数组。独立测试逐候选比较解析方差减少与真正增加一次观测后的方差之差。记录位于metrics/component-cpu-seed42.json，diagnostic_only=true，无真实LLM评价、正式能力或evolve晋级声明。  模型评测 历史分数迁移与主动采样 基础模型 能力证据：评测采样、读出与可靠性">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<h2 id="paper-foundation-models-proeval-344b21b9">ProEval: Proactive Failure Discovery and Efficient Performance Estimation for Generative AI Evaluation</h2>
<p class="ar-learning-card__meta">Google DeepMind · 论文公开：2026-04-25</p>
<p><strong>方法要点：</strong>昂贵模型或评审器不适合每次全量评分。ProEval复用历史模型之间逐题表现的相关性，形成目标模型的概率评分替身；目标分数只在对应题被选中后传入更新。主源：v1 §2.1–2.4 Eq2、5、7、10、12。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整多基准/API实验成本过高，不复现（审查DONE）；仅4份历史评分数学夹具和4题目标分数；采集器只得到已查询分数，不接受整个隐藏目标数组。独立测试逐候选比较解析方差减少与真正增加一次观测后的方差之差。记录位于metrics/component-cpu-seed42.json，diagnostic_only=true，无真实LLM评价、正式能力或evolve晋级声明。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.23099">原论文</a> · <a href="../../../../foundation-models/2604.23099-proeval/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="FUSE: Ensembling Verifiers with Zero Labeled Data 基础模型 Stanford University 2026-04-20 多个验证器并不独立，直接平均可能让相关错误相互放大。FUSE 只读取候选分数矩阵，通过二、三阶矩估计查询条件下的验证器质量，选择能缓解相关性的分数变换，再构造正确后验并优化集成器；真实正确标签只用于独立评估。图按原文 Figure 2 / Algorithm 1 重绘。原始流程图。 成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。附录 F 的 HLE/IMO 新生成与验证采用 8×H100-80GB，完整生成实验成本过高，不复现（审查 DONE）。但论文明确：读取既有分数的矩阵计算无需 GPU，不能据完整生成规模错误拒绝离线核心。  推理与系统效率 无标签验证器集成 基础模型 能力证据：评测采样、读出与可靠性">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<h2 id="paper-foundation-models-fuse-verifiers-1ae3c639">FUSE: Ensembling Verifiers with Zero Labeled Data</h2>
<p class="ar-learning-card__meta">Stanford University · 论文公开：2026-04-20</p>
<p><strong>方法要点：</strong>多个验证器并不独立，直接平均可能让相关错误相互放大。FUSE 只读取候选分数矩阵，通过二、三阶矩估计查询条件下的验证器质量，选择能缓解相关性的分数变换，再构造正确后验并优化集成器；真实正确标签只用于独立评估。图按原文 Figure 2 / Algorithm 1 重绘。原始流程图。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。附录 F 的 HLE/IMO 新生成与验证采用 8×H100-80GB，完整生成实验成本过高，不复现（审查 DONE）。但论文明确：读取既有分数的矩阵计算无需 GPU，不能据完整生成规模错误拒绝离线核心。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.18547v1">原论文</a> · <a href="../../../../foundation-models/2604.18547-fuse-verifiers/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Detecting Post-generation Edits to Watermarked LLM Outputs via Combinatorial Watermarking 基础模型 University of Minnesota 2025-10-02 固定v1 Section3 Eqs2–5：调用方提供真实secret分区与base logits；bias δ到当前pattern tag后softmax。Iw(t)对所有cyclic phases检查，global mean；local在完整interior t=w−1..T−w平均w个covering windows。全局&gt;=threshold、局部&lt;threshold，阈值需在calibration控制TypeI。binary周期整周期删除可以不可检测，不能承诺完美定位。 成本过高，不复现（审查 DONE）。诊断不加载tokenizer/LLM。完整实验Llama2-7B/OPT1.3B，WikiText多水印强度/模式/1–6token编辑×三种编辑方式，1000条64token、阈值校准及PPL矩阵；原文RTX6000Ada48GB。完整模型数据构造与全矩阵不跑，不编造总耗时；只保留CPU公式和负控。调用方提供vocabulary partition与base logits；CPU实现bias、softmax、cyclic窗口统计和阈值判定，不提供production secret系统或密码安全保证。诊断不加载tokenizer/LLM。  安全与可验证性 文本水印与编辑检测 基础模型 能力证据：评测采样、读出与可靠性">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<h2 id="paper-foundation-models-combinatorial-watermark-183aedb0">Detecting Post-generation Edits to Watermarked LLM Outputs via Combinatorial Watermarking</h2>
<p class="ar-learning-card__meta">University of Minnesota · 论文公开：2025-10-02</p>
<p><strong>方法要点：</strong>固定v1 Section3 Eqs2–5：调用方提供真实secret分区与base logits；bias δ到当前pattern tag后softmax。Iw(t)对所有cyclic phases检查，global mean；local在完整interior t=w−1..T−w平均w个covering windows。全局&gt;=threshold、局部&lt;threshold，阈值需在calibration控制TypeI。binary周期整周期删除可以不可检测，不能承诺完美定位。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。诊断不加载tokenizer/LLM。完整实验Llama2-7B/OPT1.3B，WikiText多水印强度/模式/1–6token编辑×三种编辑方式，1000条64token、阈值校准及PPL矩阵；原文RTX6000Ada48GB。完整模型数据构造与全矩阵不跑，不编造总耗时；只保留CPU公式和负控。调用方提供vocabulary partition与base logits；CPU实现bias、softmax、cyclic窗口统计和阈值判定，不提供production secret系统或密码安全保证。诊断不加载tokenizer/LLM。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.01637v1">原论文</a> · <a href="../../../../foundation-models/2510.01637-combinatorial-watermark/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/evaluation-and-evidence" data-search="Model Directions, Not Words: Mechanistic Topic Models Using Sparse Autoencoders 基础模型 Columbia University 2025-07-31 固定v3 Section4.2.2 Eqs9–13：δN(0,I)、θ=softmaxδ、βk=sigmoid(W_in vk+b)，W_in为冻结SAE ENCODER，不是decoder；每个feature计数Binomial(Ntokens,[θβ]i)。variational q拓扑与MC noise显式外传，优化NLL+analytic Gaussian KL。Eqs16–19仅steering才用独立SAE DECODER列方向加权单位化，再移除已有parallel分量、注入指定strength。 成本过高，不复现（审查 DONE）。Gemma2-9B、layer10的16K GemmaScope SAE、8数据集、LDA/ETM/BERTopic多变种及Bayesian优化，GPT4.1 topic judge每数据集2800成对比较和额外coherence/steering评测。完整矩阵超单卡短时预算；不下载LLM/SAE或调API，不编造未报告总GPU小时。MechanisticETM接冻结SAE encoder_weights与真实过滤后的activation counts；steering函数单独接不同的decoder方向和decoder bias。  可解释性 SAE主题模型与控制 基础模型 能力证据：评测采样、读出与可靠性">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 能力证据：评测采样、读出与可靠性</a></p>
<h2 id="paper-foundation-models-mechanistic-etm-c8c4eb6c">Model Directions, Not Words: Mechanistic Topic Models Using Sparse Autoencoders</h2>
<p class="ar-learning-card__meta">Columbia University · 论文公开：2025-07-31</p>
<p><strong>方法要点：</strong>固定v3 Section4.2.2 Eqs9–13：δN(0,I)、θ=softmaxδ、βk=sigmoid(W_in vk+b)，W_in为冻结SAE ENCODER，不是decoder；每个feature计数Binomial(Ntokens,[θβ]i)。variational q拓扑与MC noise显式外传，优化NLL+analytic Gaussian KL。Eqs16–19仅steering才用独立SAE DECODER列方向加权单位化，再移除已有parallel分量、注入指定strength。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。Gemma2-9B、layer10的16K GemmaScope SAE、8数据集、LDA/ETM/BERTopic多变种及Bayesian优化，GPT4.1 topic judge每数据集2800成对比较和额外coherence/steering评测。完整矩阵超单卡短时预算；不下载LLM/SAE或调API，不编造未报告总GPU小时。MechanisticETM接冻结SAE encoder_weights与真实过滤后的activation counts；steering函数单独接不同的decoder方向和decoder bias。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.23220v1">原论文</a> · <a href="../../../../foundation-models/2507.23220-mechanistic-etm/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
