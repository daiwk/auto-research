---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 推理压缩：权重、KV 缓存与服务带宽

[基础模型](index.md) / 子主题导学 · 约 3 分钟 · 29 张论文卡

## 先想一个问题

显存或时延不够时，真正占资源的是模型权重、历史状态，还是服务搬运？

## 记住这一点

AWQ 依据校准激活识别重要通道，以等价缩放降低低比特权重量化误差；GQA 则让多个 Query head 共享较少的 KV head，减少每个历史位置要存的状态。KV 驱逐、量化和分层存储又分别改变保留哪些 token、每个状态用多少位、状态放在哪里。这些机制针对不同资源，不能互相替代。

## 一个例子

把 prompt 从 1k 拉到 32k，模型权重大小基本不变，KV 随序列和并发增长。W4 可能先解决装载问题，却解决不了无限增长的缓存；减少 KV head、压缩状态或驱逐 token 可降低缓存成本，但后两者还要检验量化误差或证据丢失。

## 什么时候要小心

低比特文件变小不等于延迟成比例下降，解包 kernel、带宽和 batch 都有影响。缓存压缩也要检查恢复与重复使用条件。本地重建误差、解析元素数或 CPU 算子通过，不能代替 GPU 吞吐或长上下文能力测量。

## 先读这几篇

先读 AWQ，定位激活感知缩放保护的对象；再读 GQA，画出 Query head 与 KV head 的共享关系。理解静态权重与动态缓存后，再选驱逐、缓存量化或远程存储路线。

1. [AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration](../../../reproductions/2306.00978-awq/README.md) · [原论文](https://arxiv.org/abs/2306.00978)
2. [GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](../../../reproductions/2305.13245-gqa/README.md) · [原论文](https://arxiv.org/abs/2305.13245)

## 自测一下

AWQ 的权重量化与 KV 驱逐是否都属于“丢掉不重要的历史 token”？

??? note "展开参考答案"

    不是。AWQ 改模型静态权重的数值表示；KV 驱逐删除推理中某些位置的缓存。前者主要影响参数存储和数值误差，后者改变可访问的历史证据，必须分别做质量与资源验证。

## 这个子主题的论文卡片

导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">
<div class="ar-learning-controls">
<label for="learning-search">搜索卡片
<input id="learning-search" type="search" data-learning-search placeholder="搜索论文、机制、机构或本地边界"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">共 29 张卡片</p>
<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="MoEZip: Routing-Aware KV Cache Compression for Sparse Mixture-of-Experts LLMs 基础模型 Korea University 2026-10-21 MoE 的 KV 删除会扰动 attention 输出，进而改变路由。MoEZip 用已观察 instruction token 的路由分布 Fisher trace 作为敏感性代理，经 attention 传播到 context 位置，预留全局 routing anchors；其余预算沿用调用者提供的 dense/MoE base compressor 分数。future answer 不可用于真实选择。 完整实验成本过高，不复现（审查 DONE）；3 seeds 仍只是 L1 机制诊断，不构成 MoE 能力或质量提升证据。fisher_trace、select_cache、compress_cache 保留两种 gate、跨头 max、全局 anchors、App C 默认预算边界、base 排除重复补齐及真实 KV gather。输出原 context 索引并维持升序，调用者必须据此保留 position IDs。base 分数是显式接口，不伪装成已实现 KVZip。  MoE路由 KV缓存与稀疏推理 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-moezip-03b66820">MoEZip: Routing-Aware KV Cache Compression for Sparse Mixture-of-Experts LLMs</h2>
<p class="ar-learning-card__meta">Korea University · 论文公开：2026-10-21</p>
<p><strong>方法要点：</strong>MoE 的 KV 删除会扰动 attention 输出，进而改变路由。MoEZip 用已观察 instruction token 的路由分布 Fisher trace 作为敏感性代理，经 attention 传播到 context 位置，预留全局 routing anchors；其余预算沿用调用者提供的 dense/MoE base compressor 分数。future answer 不可用于真实选择。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）；3 seeds 仍只是 L1 机制诊断，不构成 MoE 能力或质量提升证据。fisher_trace、select_cache、compress_cache 保留两种 gate、跨头 max、全局 anchors、App C 默认预算边界、base 排除重复补齐及真实 KV gather。输出原 context 索引并维持升序，调用者必须据此保留 position IDs。base 分数是显式接口，不伪装成已实现 KVZip。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30206v1">原论文</a> · <a href="../../../../foundation-models/2610.30206-moezip/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="Right On Q: Recovering Reasoning under Quantization via Self-Generated Trajectories 基础模型 University of Michigan, Ann Arbor 2026-10-21 低比特量化会改变模型生成的前缀。只在固定的全精度参考回答上蒸馏，不能覆盖量化学生真正遇到的错误和长推理状态。OnQ 从逐 block 校准开始，让量化学生自己生成回答，再由冻结的原始全精度教师在相同学生前缀上提供分布监督。第二个问题是同一前缀中不同候选 token 的偏差方向不同：学生既可能低估某些 token，也可能高估另一些 token。论文采用候选级 Dynamic KL，用教师与学生概率的比值调整 forward / reverse KL 的权重，而不是整句共用一个混合系数。 收录状态：高成本研究资料，完整实验不复现（审查 DONE）。后续若单独批准实现，至少需同时保留逐 block 初始化、学生真实量化前向 / rollout、冻结同前缀教师监督、候选级 stop-gradient 权重与残差概率类别，才可讨论对应保真度。收录状态：高成本研究资料，完整实验不复现（审查 DONE）。未实现 runtime、量化训练、教师服务或 benchmark；没有本地指标，没有 GPU 验证要求，也不进入 evolve 晋级。不能把本页的公式解读标成模型复现。正文 §4 与 Appendix A.1-A.2 给出完整训练预算：  模型压缩与量化 量化学生在策略蒸馏 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-right-on-q-5ed3d308">Right On Q: Recovering Reasoning under Quantization via Self-Generated Trajectories</h2>
<p class="ar-learning-card__meta">University of Michigan, Ann Arbor · 论文公开：2026-10-21</p>
<p><strong>方法要点：</strong>低比特量化会改变模型生成的前缀。只在固定的全精度参考回答上蒸馏，不能覆盖量化学生真正遇到的错误和长推理状态。OnQ 从逐 block 校准开始，让量化学生自己生成回答，再由冻结的原始全精度教师在相同学生前缀上提供分布监督。第二个问题是同一前缀中不同候选 token 的偏差方向不同：学生既可能低估某些 token，也可能高估另一些 token。论文采用候选级 Dynamic KL，用教师与学生概率的比值调整 forward / reverse KL 的权重，而不是整句共用一个混合系数。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>收录状态：高成本研究资料，完整实验不复现（审查 DONE）。后续若单独批准实现，至少需同时保留逐 block 初始化、学生真实量化前向 / rollout、冻结同前缀教师监督、候选级 stop-gradient 权重与残差概率类别，才可讨论对应保真度。收录状态：高成本研究资料，完整实验不复现（审查 DONE）。未实现 runtime、量化训练、教师服务或 benchmark；没有本地指标，没有 GPU 验证要求，也不进入 evolve 晋级。不能把本页的公式解读标成模型复现。正文 §4 与 Appendix A.1-A.2 给出完整训练预算：</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.29378v1">原论文</a> · <a href="../../../../foundation-models/2610.29378-right-on-q/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="RACE: RoPE-Aligned Attention Compression Based on Query-Key Activation Energies 基础模型 MIT CSAIL 2026-10-20 把KV写成低秩形式却在注意力前还原，可能节省缓存但增加运算。RACE直接改变注意力head的宽度：Q和K共享选择，只保留完整RoPE旋转对；V通过校准激活的右奇异子空间投影；再将两种变换折叠到Q/K/V/O权重。保留原模型频率及原head维度缩放，避免把缩小维度当作新模型重新编码。 整套矩阵超出本轮单A100/A30短时预算，成本过高，不复现（审查 DONE），不下载、不试跑、不进入重试队列。校准与该小向量诊断不是validation/test能力评测；race_pair_selection支持split-half和interleaved两种物理旋转布局；calibrate_race得到detached QK选择与V子空间；fold_race_weights真实生成缩小后的四个投影；native_race_attention仅在保留维度执行因果注意力，不还原完整Q/K/V。当前是单头、全RoPE参考算子，不是HuggingFace整模型转换器，也未实现GQA/partial-RoPE部署。  注意力与长上下文 KV缓存与原生维度压缩 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-race-rope-compression-5eb673ad">RACE: RoPE-Aligned Attention Compression Based on Query-Key Activation Energies</h2>
<p class="ar-learning-card__meta">MIT CSAIL · 论文公开：2026-10-20</p>
<p><strong>方法要点：</strong>把KV写成低秩形式却在注意力前还原，可能节省缓存但增加运算。RACE直接改变注意力head的宽度：Q和K共享选择，只保留完整RoPE旋转对；V通过校准激活的右奇异子空间投影；再将两种变换折叠到Q/K/V/O权重。保留原模型频率及原head维度缩放，避免把缩小维度当作新模型重新编码。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>整套矩阵超出本轮单A100/A30短时预算，成本过高，不复现（审查 DONE），不下载、不试跑、不进入重试队列。校准与该小向量诊断不是validation/test能力评测；race_pair_selection支持split-half和interleaved两种物理旋转布局；calibrate_race得到detached QK选择与V子空间；fold_race_weights真实生成缩小后的四个投影；native_race_attention仅在保留维度执行因果注意力，不还原完整Q/K/V。当前是单头、全RoPE参考算子，不是HuggingFace整模型转换器，也未实现GQA/partial-RoPE部署。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28385v1">原论文</a> · <a href="../../../../foundation-models/2610.28385-race-rope-compression/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="FLINT: Fixed-budget Late Interaction 基础模型 University of Illinois Urbana-Champaign 2026-10-19 ColBERT 对每个 token 保留向量，文档越长索引越大，长查询也需要更多次向量检索。ConstBERT 固定了文档侧预算，但查询仍逐 token。FLINT 则在共享 backbone 后，用两套不同的可学习 latent 分别读取查询和文档 token；交叉注意力、FFN 参数共享，双方输出都固定为个向量。它不是截取前个 token，也不是简单平均池化。 这些完整训练/索引/多基准实验明显超过单 A100/A30 的本轮短预算，标注成本过高，不复现（审查 DONE），不下载、不试跑、不进入自动重试队列。FlintLatentPool 实现共享多头 cross-attention、两套 latent、pre-LN、残差及 GELU FFN；FlintFixedBudgetRetrieval 接收已经编码的 token 张量，执行投影、归一化和 aligned-batch MaxSim。它不包含 tokenizer、BERT/ModernBERT backbone、教师蒸馏、训练数据或 PLAID 索引，因此不是可直接用于文本检索的完整模型。  推理与系统效率 多向量检索与固定预算池化 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-flint-b6635740">FLINT: Fixed-budget Late Interaction</h2>
<p class="ar-learning-card__meta">University of Illinois Urbana-Champaign · 论文公开：2026-10-19</p>
<p><strong>方法要点：</strong>ColBERT 对每个 token 保留向量，文档越长索引越大，长查询也需要更多次向量检索。ConstBERT 固定了文档侧预算，但查询仍逐 token。FLINT 则在共享 backbone 后，用两套不同的可学习 latent 分别读取查询和文档 token；交叉注意力、FFN 参数共享，双方输出都固定为个向量。它不是截取前个 token，也不是简单平均池化。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>这些完整训练/索引/多基准实验明显超过单 A100/A30 的本轮短预算，标注成本过高，不复现（审查 DONE），不下载、不试跑、不进入自动重试队列。FlintLatentPool 实现共享多头 cross-attention、两套 latent、pre-LN、残差及 GELU FFN；FlintFixedBudgetRetrieval 接收已经编码的 token 张量，执行投影、归一化和 aligned-batch MaxSim。它不包含 tokenizer、BERT/ModernBERT backbone、教师蒸馏、训练数据或 PLAID 索引，因此不是可直接用于文本检索的完整模型。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.27273v1">原论文</a> · <a href="../../../../foundation-models/2610.27273-flint/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="DropKV: Decoupling Residual-Output Perturbation for Near-Optimal KV-Cache Eviction 基础模型 University at Albany, SUNY 2026-10-15 只按 attention 权重淘汰 KV 会忽略 value 内容。DropKV 将组合驱逐近似为逐 token 输出扰动，跨观察窗口累加、池化，并保护近期 token。§3 与 Algorithm 1 定义评分；§4 的近似保证有条件，不能解释成任意输入上的全局最优。 完整 7B/8B 多模型、4K–128K、多预算、多基准评估超出本轮单 A100/A30 的低成本范围，成本过高，不复现（审查 DONE）。CUDA 诊断记录与真实GPU回执保存设备、种子及源码身份。无数据集/模型下载。输入为固定种子 42/43/44 的合成 Q/K/V，revision synthetic-formula-and-bit-patterns@oct17-foundation-components-v1，不是能力 benchmark。每 seed：1 batch、4 query heads、2 KV heads、19 历史槽、3 query、8 维，驱逐 7 项；不接触训练/验证/测试答案。  KV缓存 输出扰动驱逐 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-drop-kv-30cd8cec">DropKV: Decoupling Residual-Output Perturbation for Near-Optimal KV-Cache Eviction</h2>
<p class="ar-learning-card__meta">University at Albany, SUNY · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>只按 attention 权重淘汰 KV 会忽略 value 内容。DropKV 将组合驱逐近似为逐 token 输出扰动，跨观察窗口累加、池化，并保护近期 token。§3 与 Algorithm 1 定义评分；§4 的近似保证有条件，不能解释成任意输入上的全局最优。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整 7B/8B 多模型、4K–128K、多预算、多基准评估超出本轮单 A100/A30 的低成本范围，成本过高，不复现（审查 DONE）。CUDA 诊断记录与真实GPU回执保存设备、种子及源码身份。无数据集/模型下载。输入为固定种子 42/43/44 的合成 Q/K/V，revision synthetic-formula-and-bit-patterns@oct17-foundation-components-v1，不是能力 benchmark。每 seed：1 batch、4 query heads、2 KV heads、19 历史槽、3 query、8 维，驱逐 7 项；不接触训练/验证/测试答案。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22130">原论文</a> · <a href="../../../../foundation-models/2610.22130-drop-kv/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="Fractional Power-of-Two Quantization for Efficient and Effective Multiplier-Free LLM Inference 基础模型 Seoul National University 2026-10-15 传统power-of-two权重网格较粗。FPoT将相邻指数间隔减半，兼顾4-bit量化误差与移位加法实现；对奇指数的平方根2系数使用1.5近似，并让校准直接适配这一实际网格，避免“先精确量化、部署时再替换系数”的额外误差。 这一实验矩阵成本过高，不复现（审查 DONE）。完整数据见实际A100逐seed诊断指标与真实GPU验收回执。固定公开合成recipe synthetic-fpot-and-native-layer-kernel-features@oct19-foundation-mechanisms-v1、seeds42/43/44。生成6×16权重与8×16整数激活；不下载模型或数据。每次只写新的不可变产物路径：  推理与系统效率 低比特量化与整数计算 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-fpot-d99f8a99">Fractional Power-of-Two Quantization for Efficient and Effective Multiplier-Free LLM Inference</h2>
<p class="ar-learning-card__meta">Seoul National University · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>传统power-of-two权重网格较粗。FPoT将相邻指数间隔减半，兼顾4-bit量化误差与移位加法实现；对奇指数的平方根2系数使用1.5近似，并让校准直接适配这一实际网格，避免“先精确量化、部署时再替换系数”的额外误差。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>这一实验矩阵成本过高，不复现（审查 DONE）。完整数据见实际A100逐seed诊断指标与真实GPU验收回执。固定公开合成recipe synthetic-fpot-and-native-layer-kernel-features@oct19-foundation-mechanisms-v1、seeds42/43/44。生成6×16权重与8×16整数激活；不下载模型或数据。每次只写新的不可变产物路径：</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21257">原论文</a> · <a href="../../../../foundation-models/2610.21257-fpot/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="When the KV Cache Is Slower Than the GPU: Scaling Remote KV Tiers for Context-Parallel Prefill 基础模型 Multiverse Computing 2026-10-15 缓存命中不一定更快。该工作先计算加载与重算的盈亏平衡带宽和固定开销，再把MLA KV缓存按PCP rank分片，并使用rank独立远程实例和异步加载消除队首阻塞。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地能力指标、训练结果或可执行 Evolve 算子。无本地adapter、指标文件或GPU回执，也不登记可执行Evolve算子。原论文结果仅作为阅读资料。范围见本轮实现与审查合同。本轮只完成方法、资源需求、公开代码状态及原图收录，没有运行完整实验、下载checkpoint或制造模拟能力分数。  推理与系统效率 KV缓存与分布式服务 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-remote-kv-tiers-30f3c03e">When the KV Cache Is Slower Than the GPU: Scaling Remote KV Tiers for Context-Parallel Prefill</h2>
<p class="ar-learning-card__meta">Multiverse Computing · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>缓存命中不一定更快。该工作先计算加载与重算的盈亏平衡带宽和固定开销，再把MLA KV缓存按PCP rank分片，并使用rank独立远程实例和异步加载消除队首阻塞。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地能力指标、训练结果或可执行 Evolve 算子。无本地adapter、指标文件或GPU回执，也不登记可执行Evolve算子。原论文结果仅作为阅读资料。范围见本轮实现与审查合同。本轮只完成方法、资源需求、公开代码状态及原图收录，没有运行完整实验、下载checkpoint或制造模拟能力分数。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21500">原论文</a> · <a href="../../../../foundation-models/2610.21500-remote-kv-tiers/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="RoleQ: Role-Aligned Scales for Converting Language Models to Ternary 基础模型 Harvard University 2026-10-15 按矩阵布局统一逐行放scale，会把写入残差流的不同功能单元混在一起。RoleQ按功能角色选轴：reader（Q/K/V与MLP输入）每输出单元一scale，writer（O与MLP输出）每输入单元一scale。完整RoleQ-T还需要旋转、GPTQ、蒸馏及可选Fisher二平面，不能以单个量化函数替代。 原文8B转换3–4 A100小时、二平面阶段不足10小时，完整实验成本过高，不复现（审查 DONE）。CUDA诊断记录与真实GPU回执保存设备、种子、真实测量与源码身份。固定seeds42/43/44；合成公式revision synthetic-formula-and-bit-patterns@oct17-foundation-components-v1，无预训练模型或能力数据。runner用长度4向量全部81种三值码独立穷举全局最优；单测长度5、243码。7×11矩阵用于角色轴与pack/unpack。  量化与压缩 角色对齐三值量化 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-roleq-9df6d043">RoleQ: Role-Aligned Scales for Converting Language Models to Ternary</h2>
<p class="ar-learning-card__meta">Harvard University · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>按矩阵布局统一逐行放scale，会把写入残差流的不同功能单元混在一起。RoleQ按功能角色选轴：reader（Q/K/V与MLP输入）每输出单元一scale，writer（O与MLP输出）每输入单元一scale。完整RoleQ-T还需要旋转、GPTQ、蒸馏及可选Fisher二平面，不能以单个量化函数替代。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>原文8B转换3–4 A100小时、二平面阶段不足10小时，完整实验成本过高，不复现（审查 DONE）。CUDA诊断记录与真实GPU回执保存设备、种子、真实测量与源码身份。固定seeds42/43/44；合成公式revision synthetic-formula-and-bit-patterns@oct17-foundation-components-v1，无预训练模型或能力数据。runner用长度4向量全部81种三值码独立穷举全局最优；单测长度5、243码。7×11矩阵用于角色轴与pack/unpack。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21808">原论文</a> · <a href="../../../../foundation-models/2610.21808-roleq/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="Compression Does Not End at Selection: Post-Selection Positional Geometry for Sparse KV Caches 基础模型 National University of Defense Technology 2026-10-15 selector 删除 token 后，K 仍携带稀疏旧坐标的旋转相位。RoPERelay 不重选内容、不重新 prefill 历史，将选中状态按原始时间排序、压紧坐标，并同步问题及生成坐标。来源为 §3、附录 A 的 Algorithm 1 和数值约定。 按该公开配置，完整多臂长上下文评测超出本轮单 A100/A30/Mac 的低成本预算，成本过高，不复现（审查 DONE），不下载权重或大数据。用合成固定 K/V 进行独立 complex 参考与 attention/梯度诊断，未加载模型或长记忆数据。保留实数 Torch 梯度的 cache 算子，支持 scaled/partial RoPE、split-half/interleaved 两种布局、异长 mask、共同 continuation anchor。用合成固定 K/V 进行独立 complex 参考与 attention/梯度诊断，未加载模型或长记忆数据。  KV缓存 旋转位置重建 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-rope-relay-6493fdc7">Compression Does Not End at Selection: Post-Selection Positional Geometry for Sparse KV Caches</h2>
<p class="ar-learning-card__meta">National University of Defense Technology · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>selector 删除 token 后，K 仍携带稀疏旧坐标的旋转相位。RoPERelay 不重选内容、不重新 prefill 历史，将选中状态按原始时间排序、压紧坐标，并同步问题及生成坐标。来源为 §3、附录 A 的 Algorithm 1 和数值约定。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>按该公开配置，完整多臂长上下文评测超出本轮单 A100/A30/Mac 的低成本预算，成本过高，不复现（审查 DONE），不下载权重或大数据。用合成固定 K/V 进行独立 complex 参考与 attention/梯度诊断，未加载模型或长记忆数据。保留实数 Torch 梯度的 cache 算子，支持 scaled/partial RoPE、split-half/interleaved 两种布局、异长 mask、共同 continuation anchor。用合成固定 K/V 进行独立 complex 参考与 attention/梯度诊断，未加载模型或长记忆数据。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21126">原论文</a> · <a href="../../../../foundation-models/2610.21126-rope-relay/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="PN-Mix: Pair-Norm Guided Mixed-Precision Key Cache Quantization for Efficient Long-Output LLM Inference 基础模型 Seoul National University 2026-10-14 长输出解码的 KV cache 随 token 数增长；一律把 K 降到低位宽，会放大 attention logit 的偏差。PN-Mix 的精度分配不是仅按 K 的幅度排序：它同时观察 prefill 的 Q 和 K，把实际 RoPE 旋转耦合的两个通道作为整体，以两侧平均范数乘积预测重要性。每个 KV head 选择一次高精度通道对，后续所有量化页复用这份选择，不读取未来解码状态重选。 完整 8B–32B、32K 输出、多任务与吞吐研究为成本过高，不复现（审查 DONE）；本地是 L1 可执行组件诊断，不是完整论文效果复现。本地是 L1 可执行组件诊断，不是完整论文效果复现。已实现 prefill 的 query–key 通道对评分、H3/L1 真正打包、1-bit 中点校正、sink/residual 缓存与量化后 attention 消费。完整 8B–32B、32K 输出、多任务与吞吐研究为成本过高，不复现（审查 DONE）；不进入自动 Evolve 晋级。本地对照口径：基线与实验组使用同一 Q/K/V、因果位置与输入网络；  kv-cache quantization inference-serving long-context 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-pn-mix-d9cac8c7">PN-Mix: Pair-Norm Guided Mixed-Precision Key Cache Quantization for Efficient Long-Output LLM Inference</h2>
<p class="ar-learning-card__meta">Seoul National University · 论文公开：2026-10-14</p>
<p><strong>方法要点：</strong>长输出解码的 KV cache 随 token 数增长；一律把 K 降到低位宽，会放大 attention logit 的偏差。PN-Mix 的精度分配不是仅按 K 的幅度排序：它同时观察 prefill 的 Q 和 K，把实际 RoPE 旋转耦合的两个通道作为整体，以两侧平均范数乘积预测重要性。每个 KV head 选择一次高精度通道对，后续所有量化页复用这份选择，不读取未来解码状态重选。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整 8B–32B、32K 输出、多任务与吞吐研究为成本过高，不复现（审查 DONE）；本地是 L1 可执行组件诊断，不是完整论文效果复现。本地是 L1 可执行组件诊断，不是完整论文效果复现。已实现 prefill 的 query–key 通道对评分、H3/L1 真正打包、1-bit 中点校正、sink/residual 缓存与量化后 attention 消费。完整 8B–32B、32K 输出、多任务与吞吐研究为成本过高，不复现（审查 DONE）；不进入自动 Evolve 晋级。本地对照口径：基线与实验组使用同一 Q/K/V、因果位置与输入网络；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19605">原论文</a> · <a href="../../../../reproductions/2610.19605-pn-mix/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="DualQuant: Dual-scale Calibration-free Weight-and-Activation Quantization for LLMs 基础模型 d-Matrix 2026-10-09 W+A量化中，权重与激活误差相互放大；仅最小化逐row动态范围不能消除跨row系统性column outlier。DualQuant只读取静态权重，以row/block尺度与column尺度共同最小化重建MSE。column尺度同时变成推理时的激活重缩放，不需要校准样本、激活统计或Hessian。 默认量化公开SmolLM2-135M的前四个decoder nn.Linear，每row tile128、column group32，属于部分checkpoint机制诊断；本地对照口径：相同公开checkpoint中相同线性层的single-scale INT4 W+A为基线，dual-scale为实验组；相对吞吐和内存不适用，software simulation只报告重建MSE与隔离test NLL。  quantization calibration-free weight-activation-quantization 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-dualquant-6a91d161">DualQuant: Dual-scale Calibration-free Weight-and-Activation Quantization for LLMs</h2>
<p class="ar-learning-card__meta">d-Matrix · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>W+A量化中，权重与激活误差相互放大；仅最小化逐row动态范围不能消除跨row系统性column outlier。DualQuant只读取静态权重，以row/block尺度与column尺度共同最小化重建MSE。column尺度同时变成推理时的激活重缩放，不需要校准样本、激活统计或Hessian。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>默认量化公开SmolLM2-135M的前四个decoder nn.Linear，每row tile128、column group32，属于部分checkpoint机制诊断；本地对照口径：相同公开checkpoint中相同线性层的single-scale INT4 W+A为基线，dual-scale为实验组；相对吞吐和内存不适用，software simulation只报告重建MSE与隔离test NLL。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13767">原论文</a> · <a href="../../../../reproductions/2610.13767-dualquant/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="ReplaySSM: Cache SSM Inputs, Not State 基础模型 Princeton University 2026-10-09 Mamba2/GDN 解码一般每 token 读写完整矩阵状态，常受显存带宽限制。ReplaySSM 把持久化状态与输出计算拆开：每 16 token 才刷新 checkpoint，其间只记录小型输入；输出由 checkpoint 与输入重放计算。投机验证使用 output-only 形式，避免为每个 draft 物化完整状态。接受长度只推进已提交输入指针；被拒 draft 不进入 recurrence。 不签失败为 passed，也不把新证据重绑定到未执行的新源码。cpu-contracts.json记录 seed 42 独立参考：最大输出误差 1.1920928955078125e-7、接受 12 个 token、刷新 3 次；4 个行为测试覆盖公式、GDN、pending/rollback 和低精度 read 不进入 recurrence。core_mechanism / L1 分成两条证据：独立 PyTorch 参考执行 checkpoint、accept/rollback、output-only、GDN 三角解与双精度刷新；  推理与系统效率 SSM 缓存与回滚 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-replayssm-704fd9a0">ReplaySSM: Cache SSM Inputs, Not State</h2>
<p class="ar-learning-card__meta">Princeton University · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>Mamba2/GDN 解码一般每 token 读写完整矩阵状态，常受显存带宽限制。ReplaySSM 把持久化状态与输出计算拆开：每 16 token 才刷新 checkpoint，其间只记录小型输入；输出由 checkpoint 与输入重放计算。投机验证使用 output-only 形式，避免为每个 draft 物化完整状态。接受长度只推进已提交输入指针；被拒 draft 不进入 recurrence。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不签失败为 passed，也不把新证据重绑定到未执行的新源码。cpu-contracts.json记录 seed 42 独立参考：最大输出误差 1.1920928955078125e-7、接受 12 个 token、刷新 3 次；4 个行为测试覆盖公式、GDN、pending/rollback 和低精度 read 不进入 recurrence。core_mechanism / L1 分成两条证据：独立 PyTorch 参考执行 checkpoint、accept/rollback、output-only、GDN 三角解与双精度刷新；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13778">原论文</a> · <a href="../../../../reproductions/2610.13778-replayssm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="VFold: Symmetry-Aware Cross-Layer Value Cache Compression 基础模型 Johns Hopkins University 2026-10-08 相邻层的 Value 不一定在同一坐标系。VFold 用满秩 CCA 对齐和 Hungarian 头匹配，离线把变换折进 Value/输出投影；当前 token 先以完整 Value 参与注意力，随后才与相邻层平均共享。Key 不合并，首尾重要 token 独立保存。 已实现真实权重折叠和持久共享缓存；当前结果是 L1 运行诊断，不是 LongBench/RULER 能力复现或推理加速证明。使用 Qwen3-4B、A100、seed 42；32 个训练问题校准，4 个训练集派生的独立验证问题解码，最多生成 256 token。数据来源、安装及参数见运行说明。  推理与系统效率 KV 缓存压缩 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-vfold-b54fea4f">VFold: Symmetry-Aware Cross-Layer Value Cache Compression</h2>
<p class="ar-learning-card__meta">Johns Hopkins University · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>相邻层的 Value 不一定在同一坐标系。VFold 用满秩 CCA 对齐和 Hungarian 头匹配，离线把变换折进 Value/输出投影；当前 token 先以完整 Value 参与注意力，随后才与相邻层平均共享。Key 不合并，首尾重要 token 独立保存。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>已实现真实权重折叠和持久共享缓存；当前结果是 L1 运行诊断，不是 LongBench/RULER 能力复现或推理加速证明。使用 Qwen3-4B、A100、seed 42；32 个训练问题校准，4 个训练集派生的独立验证问题解码，最多生成 256 token。数据来源、安装及参数见运行说明。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12338">原论文</a> · <a href="../../../../foundation-models/2610.12338-vfold/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="IrekoGPT: Turning Structured Pruning into Post-Hoc Slimmable LLMs 基础模型 University of Modena and Reggio Emilia 2026-10-01 保留 SliceGPT 投影矩阵而非直接丢弃，使同一 checkpoint 暴露嵌套宽度；再以多压缩率校准和 ridge 修正下游线性层。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行嵌套子网合同；未加载原模型或复现吞吐。执行嵌套子网合同；未加载原模型或复现吞吐。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  结构剪枝 可伸缩模型 推理效率 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-irekogpt-3d6c018e">IrekoGPT: Turning Structured Pruning into Post-Hoc Slimmable LLMs</h2>
<p class="ar-learning-card__meta">University of Modena and Reggio Emilia · 论文公开：2026-10-01</p>
<p><strong>方法要点：</strong>保留 SliceGPT 投影矩阵而非直接丢弃，使同一 checkpoint 暴露嵌套宽度；再以多压缩率校准和 ridge 修正下游线性层。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行嵌套子网合同；未加载原模型或复现吞吐。执行嵌套子网合同；未加载原模型或复现吞吐。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00426">原论文</a> · <a href="../../../../foundation-models/2610.00426-irekogpt/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="LeapQuant: Efficient Linear Attention with Accurate Recurrent State Quantization 基础模型 UC Berkeley 2026-09-29 逐 token 量化递归状态会不断重新舍入。LeapQuant 在一个窗口内保留低比特基态，并以高精度缓冲本窗口更新，窗口末才量化一次；同时把最大 outlier 分解成少量高精度 compensator tokens，对剩余状态平滑后再量化。 复现级别：L1 机制实现。复现级别：L1 机制实现。保留 per-window state quantization、低秩补偿 token 与 residual smoothing；未复刻论文 CUDA kernel 和完整模型吞吐。机制诊断覆盖窗口边界、补偿 rank、状态误差及 CUDA 执行；未实现作者专用 kernel。A100 脱敏记录见 ../../gpu-validations/leapquant-a100-20260930.json。  推理与系统效率 线性注意力 状态量化 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-leapquant-7df56645">LeapQuant: Efficient Linear Attention with Accurate Recurrent State Quantization</h2>
<p class="ar-learning-card__meta">UC Berkeley · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>逐 token 量化递归状态会不断重新舍入。LeapQuant 在一个窗口内保留低比特基态，并以高精度缓冲本窗口更新，窗口末才量化一次；同时把最大 outlier 分解成少量高精度 compensator tokens，对剩余状态平滑后再量化。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：L1 机制实现。复现级别：L1 机制实现。保留 per-window state quantization、低秩补偿 token 与 residual smoothing；未复刻论文 CUDA kernel 和完整模型吞吐。机制诊断覆盖窗口边界、补偿 rank、状态误差及 CUDA 执行；未实现作者专用 kernel。A100 脱敏记录见 ../../gpu-validations/leapquant-a100-20260930.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38166">原论文</a> · <a href="../../../../foundation-models/2609.38166-leapquant/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="SPLASH: Switching Parallel Layouts of Attention with Seamless Handoff for LLM Serving 基础模型 Institute of Computing Technology, Chinese Academy of Sciences 2026-09-29 统一描述 attention weight 与 KV cache 的所有权，引入权重分片、请求独占 KV 的 DOP；调度器把布局切换成本按剩余步数摊销，在 TP、DP、CP、DOP 间在线切换。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行内存模型和 transition-aware layout planner；未实现 CUDA handoff，也不声称经过 B200/H200 性能验证。执行内存模型和 transition-aware layout planner；未实现 CUDA handoff，也不声称经过 B200/H200 性能验证。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  推理系统 并行布局 KV cache 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-splash-7002fc08">SPLASH: Switching Parallel Layouts of Attention with Seamless Handoff for LLM Serving</h2>
<p class="ar-learning-card__meta">Institute of Computing Technology, Chinese Academy of Sciences · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>统一描述 attention weight 与 KV cache 的所有权，引入权重分片、请求独占 KV 的 DOP；调度器把布局切换成本按剩余步数摊销，在 TP、DP、CP、DOP 间在线切换。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行内存模型和 transition-aware layout planner；未实现 CUDA handoff，也不声称经过 B200/H200 性能验证。执行内存模型和 transition-aware layout planner；未实现 CUDA handoff，也不声称经过 B200/H200 性能验证。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37626">原论文</a> · <a href="../../../../foundation-models/2609.37626-splash/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="STEPQuant: When and Where Errors Matter in Delta-Rule Recurrent State Quantization 基础模型 Zhejiang University 2026-09-29 Delta-rule 线性注意力的固定大小状态会被每个并发请求长期持有，统一低比特量化又会让误差随更新累积。STEPQuant 同时建模状态记忆的剩余寿命和不同 key row 对输出的影响：在固定平均 bit 预算下给重要块更高精度，再用 key-row / value-column 两组 scale 拟合状态分布。 复现级别：L1 机制实现。复现级别：L1 机制实现。本地实现寿命感知 bit 分配与行/列双轴 scale 拟合；未复刻 SGLang kernel、Qwen3.8/Kimi-Linear 全模型吞吐。本地验证 bit 预算、有限 scale、递归状态 MSE 和 CUDA 前后向；不声称复现论文吞吐或精度。A100 脱敏记录见 ../../gpu-validations/stepquant-a100-20260930.json。  推理与系统效率 线性注意力 状态量化 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-stepquant-3ce3e159">STEPQuant: When and Where Errors Matter in Delta-Rule Recurrent State Quantization</h2>
<p class="ar-learning-card__meta">Zhejiang University · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>Delta-rule 线性注意力的固定大小状态会被每个并发请求长期持有，统一低比特量化又会让误差随更新累积。STEPQuant 同时建模状态记忆的剩余寿命和不同 key row 对输出的影响：在固定平均 bit 预算下给重要块更高精度，再用 key-row / value-column 两组 scale 拟合状态分布。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：L1 机制实现。复现级别：L1 机制实现。本地实现寿命感知 bit 分配与行/列双轴 scale 拟合；未复刻 SGLang kernel、Qwen3.8/Kimi-Linear 全模型吞吐。本地验证 bit 预算、有限 scale、递归状态 MSE 和 CUDA 前后向；不声称复现论文吞吐或精度。A100 脱敏记录见 ../../gpu-validations/stepquant-a100-20260930.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38169">原论文</a> · <a href="../../../../foundation-models/2609.38169-stepquant/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="AgentKV: Phase-Aware KV Eviction for Agentic LLMs 基础模型 University of Cambridge 2026-09-14 按 Agent 阶段保留代表性 query buffer，以跨阶段查询相关性决定 KV 淘汰。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 phase-aware scoring；未修改 SGLang 或运行 CUDA kernel。本地执行 phase-aware scoring；未修改 SGLang 或运行 CUDA kernel。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  Agent 推理 KV Cache 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-agentkv-c25693b7">AgentKV: Phase-Aware KV Eviction for Agentic LLMs</h2>
<p class="ar-learning-card__meta">University of Cambridge · 论文公开：2026-09-14</p>
<p><strong>方法要点：</strong>按 Agent 阶段保留代表性 query buffer，以跨阶段查询相关性决定 KV 淘汰。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 phase-aware scoring；未修改 SGLang 或运行 CUDA kernel。本地执行 phase-aware scoring；未修改 SGLang 或运行 CUDA kernel。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.14872">原论文</a> · <a href="../../../../foundation-models/2609.14872-agentkv/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="BeaconKV: Key-Value Cache Compression Guided by Beacon Queries for Efficient Large Reasoning Model Inference 基础模型 Hanyang University 2026-09-04 长推理中会出现重新关注早期计划的 Thought Revisiting Token，只用最近 query 预测未来注意力会丢失这些远程依赖。BeaconKV 对历史 query 聚类并维护少量代表 query，用它们为 KV 重要性投票，在固定缓存预算中兼顾近期上下文和远程重访。 复现级别：核心选择算法 + 真实 checkpoint CUDA smoke。复现级别：核心选择算法 + 真实 checkpoint CUDA smoke。保留近期 token，并用最远点采样维护能代表历史查询簇的 beacon。旧版 checkpoint 验证漏掉 query normalization 与 RoPE，并在 softmax 前平均 GQA query head，旧相似度作废。  kv-cache long-context reasoning inference-serving 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-beaconkv-c9b2fe88">BeaconKV: Key-Value Cache Compression Guided by Beacon Queries for Efficient Large Reasoning Model Inference</h2>
<p class="ar-learning-card__meta">Hanyang University · 论文公开：2026-09-04</p>
<p><strong>方法要点：</strong>长推理中会出现重新关注早期计划的 Thought Revisiting Token，只用最近 query 预测未来注意力会丢失这些远程依赖。BeaconKV 对历史 query 聚类并维护少量代表 query，用它们为 KV 重要性投票，在固定缓存预算中兼顾近期上下文和远程重访。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心选择算法 + 真实 checkpoint CUDA smoke。复现级别：核心选择算法 + 真实 checkpoint CUDA smoke。保留近期 token，并用最远点采样维护能代表历史查询簇的 beacon。旧版 checkpoint 验证漏掉 query normalization 与 RoPE，并在 softmax 前平均 GQA query head，旧相似度作废。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04971">原论文</a> · <a href="../../../../reproductions/2609.04971-beaconkv/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="KVMem: Virtualizing Million-Token Agent Workspaces on a Consumer GPU 基础模型 Shanghai University of Finance and Economics 2026-09-04 长寿命 Agent 的历史会同时超过显存和模型原生窗口；摘要压缩会丢证据，文本检索又要重复 prefill。KVMEM 把已计算 KV 分页放到 GPU、主存和 NVMe，用模型自身的注意力空间索引挑选相关 block，再物化为不超过原生窗口的执行视图。 复现级别：查询相关 block 选择 + 真实 checkpoint CUDA smoke。复现级别：查询相关 block 选择 + 真实 checkpoint CUDA smoke。实现固定显存预算下的 query-conditioned KV 工作视图。旧版 checkpoint 验证漏掉 query normalization 与 RoPE，并在 softmax 前平均 GQA query head，旧相似度作废。  agent-memory kv-cache long-context inference-serving 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-kvmem-cf5b3efc">KVMem: Virtualizing Million-Token Agent Workspaces on a Consumer GPU</h2>
<p class="ar-learning-card__meta">Shanghai University of Finance and Economics · 论文公开：2026-09-04</p>
<p><strong>方法要点：</strong>长寿命 Agent 的历史会同时超过显存和模型原生窗口；摘要压缩会丢证据，文本检索又要重复 prefill。KVMEM 把已计算 KV 分页放到 GPU、主存和 NVMe，用模型自身的注意力空间索引挑选相关 block，再物化为不超过原生窗口的执行视图。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：查询相关 block 选择 + 真实 checkpoint CUDA smoke。复现级别：查询相关 block 选择 + 真实 checkpoint CUDA smoke。实现固定显存预算下的 query-conditioned KV 工作视图。旧版 checkpoint 验证漏掉 query normalization 与 RoPE，并在 softmax 前平均 GQA query head，旧相似度作废。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04852">原论文</a> · <a href="../../../../reproductions/2609.04852-kvmem/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="Random Attention: Rethinking KV Cache Eviction for Efficient Reasoning 基础模型 Salesforce AI Research / University of Illinois Urbana-Champaign 2026-09-03 传统 KV 淘汰先计算 token 重要性，Random Attention 则始终保护 prompt，仅在已生成 token 中逐 head 独立随机保留固定预算；它省掉评分 pass，也避免所有 head 被同一排序规则约束。 复现级别：核心机制 + 真实 checkpoint GPU 验证。复现级别：核心机制 + 真实 checkpoint GPU 验证。保留完整 prompt，并对生成 trace 按 attention head 独立均匀随机采样。未声称复刻论文六任务矩阵和官方 vLLM kernel 吞吐；本地 GPU 路径验证真实 KV 张量上的选择与 attention 重建，并可作为 LLM Evolve attention 算子。CPU 三 seed 机制结果见 metrics/public-seeds42-44.json；  kv-cache reasoning inference-serving compression 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-random-attention-6364631b">Random Attention: Rethinking KV Cache Eviction for Efficient Reasoning</h2>
<p class="ar-learning-card__meta">Salesforce AI Research / University of Illinois Urbana-Champaign · 论文公开：2026-09-03</p>
<p><strong>方法要点：</strong>传统 KV 淘汰先计算 token 重要性，Random Attention 则始终保护 prompt，仅在已生成 token 中逐 head 独立随机保留固定预算；它省掉评分 pass，也避免所有 head 被同一排序规则约束。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 + 真实 checkpoint GPU 验证。复现级别：核心机制 + 真实 checkpoint GPU 验证。保留完整 prompt，并对生成 trace 按 attention head 独立均匀随机采样。未声称复刻论文六任务矩阵和官方 vLLM kernel 吞吐；本地 GPU 路径验证真实 KV 张量上的选择与 attention 重建，并可作为 LLM Evolve attention 算子。CPU 三 seed 机制结果见 metrics/public-seeds42-44.json；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.03430">原论文</a> · <a href="../../../../reproductions/2609.03430-random-attention/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="TwinKV: A Composable Repair Pass for KV Cache Eviction via Pairwise Key Redundancy 基础模型 The Hong Kong University of Science and Technology (Guangzhou) 2026-08-27 现有 KV eviction 常按 token 重要性选择缓存，但可能同时保留多个几乎重复的 key，并删掉没有替代者的 orphan。TwinKV 不替代 StreamingLLM、H2O 等基础策略，而是一个可组合 repair pass：在完全不增加 KV budget 的前提下，找出“被删且没有相似保留项”的 orphan，与“已保留但有高度相似 twin”的 donor 成对交换。 复现级别：核心机制 + 真实 checkpoint KV 验证。复现级别：核心机制 + 真实 checkpoint KV 验证。Equation 4、等预算 swap 与 Qwen3 实际 KV tensor 均执行；没有把 attention reconstruction 指标写成完整 LongBench 分数。正式 GPU smoke 使用 Qwen3 的真实 K/V 和公开 WikiText-2 长上下文，评测三个代表层的 attention reconstruction；它不是完整 LongBench generation。  kv-cache long-context inference-serving compression 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-twinkv-b8f534bd">TwinKV: A Composable Repair Pass for KV Cache Eviction via Pairwise Key Redundancy</h2>
<p class="ar-learning-card__meta">The Hong Kong University of Science and Technology (Guangzhou) · 论文公开：2026-08-27</p>
<p><strong>方法要点：</strong>现有 KV eviction 常按 token 重要性选择缓存，但可能同时保留多个几乎重复的 key，并删掉没有替代者的 orphan。TwinKV 不替代 StreamingLLM、H2O 等基础策略，而是一个可组合 repair pass：在完全不增加 KV budget 的前提下，找出“被删且没有相似保留项”的 orphan，与“已保留但有高度相似 twin”的 donor 成对交换。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 + 真实 checkpoint KV 验证。复现级别：核心机制 + 真实 checkpoint KV 验证。Equation 4、等预算 swap 与 Qwen3 实际 KV tensor 均执行；没有把 attention reconstruction 指标写成完整 LongBench 分数。正式 GPU smoke 使用 Qwen3 的真实 K/V 和公开 WikiText-2 长上下文，评测三个代表层的 attention reconstruction；它不是完整 LongBench generation。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27128">原论文</a> · <a href="../../../../reproductions/2608.27128-twinkv/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="DistillCache: KL-Guided Adaptive KV-Cache Eviction for Memory-Efficient LLM Inference 基础模型 Oklahoma State University 2026-08-09 把 KV 淘汰视为序列决策，以逐步 KL 奖励训练轻量策略保留未来预测分布。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 distillcache；单 seed 变化为 +92.19% 个百分点。  推理与系统效率 KV cache 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-distillcache-374f7173">DistillCache: KL-Guided Adaptive KV-Cache Eviction for Memory-Efficient LLM Inference</h2>
<p class="ar-learning-card__meta">Oklahoma State University · 论文公开：2026-08-09</p>
<p><strong>方法要点：</strong>把 KV 淘汰视为序列决策，以逐步 KL 奖励训练轻量策略保留未来预测分布。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 distillcache；单 seed 变化为 +92.19% 个百分点。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.08878">原论文</a> · <a href="../../../../reproductions/2608.08878-distillcache/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="BaKron: Efficient Quantization with Kronecker-Factored Hessians 基础模型 University of California, San Diego 2026-08-06 主题：二阶量化。GPTQ 通常只利用输入侧曲率；双侧 Kronecker Hessian 更丰富但直接向量化求解昂贵。BaKron 以反对角并行和递归分治实现双侧自适应 rounding。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。对随机权重执行 Kronecker 加权 4-bit rounding 与逐行尺度搜索，和全局 GPTQ-style rounding 比较加权误差。  quantization hessian inference-efficiency 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-bakron-8758065a">BaKron: Efficient Quantization with Kronecker-Factored Hessians</h2>
<p class="ar-learning-card__meta">University of California, San Diego · 论文公开：2026-08-06</p>
<p><strong>方法要点：</strong>主题：二阶量化。GPTQ 通常只利用输入侧曲率；双侧 Kronecker Hessian 更丰富但直接向量化求解昂贵。BaKron 以反对角并行和递归分治实现双侧自适应 rounding。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。对随机权重执行 Kronecker 加权 4-bit rounding 与逐行尺度搜索，和全局 GPTQ-style rounding 比较加权误差。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06291">原论文</a> · <a href="../../../../reproductions/2608.06291-bakron/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="QEvict: Recoverable Quantized KV Eviction for Attention-Drift-Robust Long-Context Decoding 基础模型 Indian Institute of Technology Roorkee 2026-08-05 主题：长上下文 KV cache。二元保留/删除无法应对注意力漂移：今天不重要的窗口可能稍后重新活跃。QEvict 设置全精度、量化可恢复、删除三层，累计注意力变化时可将窗口解量化晋升。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。在固定槽位预算的向量 attention 流上执行三层缓存、量化恢复与晋升，比较不可恢复 eviction recall。  long-context kv-cache quantization serving 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-qevict-bcd29a04">QEvict: Recoverable Quantized KV Eviction for Attention-Drift-Robust Long-Context Decoding</h2>
<p class="ar-learning-card__meta">Indian Institute of Technology Roorkee · 论文公开：2026-08-05</p>
<p><strong>方法要点：</strong>主题：长上下文 KV cache。二元保留/删除无法应对注意力漂移：今天不重要的窗口可能稍后重新活跃。QEvict 设置全精度、量化可恢复、删除三层，累计注意力变化时可将窗口解量化晋升。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。在固定槽位预算的向量 attention 流上执行三层缓存、量化恢复与晋升，比较不可恢复 eviction recall。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05326">原论文</a> · <a href="../../../../reproductions/2608.05326-qevict/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="TaskPress: Query-Agnostic KV Cache Compression via Task-Guided Pruning 基础模型 Google 2026-08-04 固定v2 Section3 Eqs1–3：sum over guide→odd-K零padding平均池化；γ=max|v|/(2^(b−1)−1)，scores=keyimportance×γ，各head同budget独立topk。输入显式是task-to-context sliced attention，不看真实下游query；真实K/V按时间排序gather，guideKV不保留，原position不能重编号。K/GQA聚合由调用方显式给出，tie按低index为本地约定。 成本过高，不复现（审查 DONE）。Llama3.1-8B/Qwen3-8B/32B，LongBench/RULER16K至64K上下文多压缩比例/方法矩阵；guide演化单A10040GB原文约25.2min加Gemini调用，完整多任务矩阵更大。只做算子，不跑全量加载/演化、无速度计时复现。taskpress_scores消费task-to-context attention与既有per-token value_scale；symmetric_value_scale是显式浮点数值参考，不是假装已运行int4 kernel。  推理与系统效率 KV缓存压缩 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-taskpress-8d6c3897">TaskPress: Query-Agnostic KV Cache Compression via Task-Guided Pruning</h2>
<p class="ar-learning-card__meta">Google · 论文公开：2026-08-04</p>
<p><strong>方法要点：</strong>固定v2 Section3 Eqs1–3：sum over guide→odd-K零padding平均池化；γ=max|v|/(2^(b−1)−1)，scores=keyimportance×γ，各head同budget独立topk。输入显式是task-to-context sliced attention，不看真实下游query；真实K/V按时间排序gather，guideKV不保留，原position不能重编号。K/GQA聚合由调用方显式给出，tie按低index为本地约定。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。Llama3.1-8B/Qwen3-8B/32B，LongBench/RULER16K至64K上下文多压缩比例/方法矩阵；guide演化单A10040GB原文约25.2min加Gemini调用，完整多任务矩阵更大。只做算子，不跑全量加载/演化、无速度计时复现。taskpress_scores消费task-to-context attention与既有per-token value_scale；symmetric_value_scale是显式浮点数值参考，不是假装已运行int4 kernel。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03276v1">原论文</a> · <a href="../../../../foundation-models/2608.03276-taskpress/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="C²KV: Compressed and Composable KV Cache Reuse for Efficient LLM Inference 基础模型 Shanghai Jiao Tong University 2026-07-20 以 compression tokens 和结构化 attention 学习位置无关、可拼接的压缩 KV manifold，并联合训练压缩与复用。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 c2kv；单 seed 变化为 +76.56% 个百分点。  推理与系统效率 KV cache 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-c2kv-5a6eab64">C²KV: Compressed and Composable KV Cache Reuse for Efficient LLM Inference</h2>
<p class="ar-learning-card__meta">Shanghai Jiao Tong University · 论文公开：2026-07-20</p>
<p><strong>方法要点：</strong>以 compression tokens 和结构化 attention 学习位置无关、可拼接的压缩 KV manifold，并联合训练压缩与复用。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 c2kv；单 seed 变化为 +76.56% 个百分点。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.17715">原论文</a> · <a href="../../../../reproductions/2607.17715-c2kv/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration 基础模型 MIT / NVIDIA / Harvard / SJTU 2023-06-01 利用 calibration activation 找到显著输入通道，通过等价通道缩放保护约 1% 关键权重，再执行硬件友好的统一低比特 weight-only 量化。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。用 WikiText-2 激活统计搜索 AWQ 等价缩放并真实执行 W4 量化；未使用 TinyChat CUDA kernel，MSE 不代表端到端吞吐。本地相对变化不得与原文指标混写。本地对照口径：基线为 round-to-nearest W4，实验组为 activation-aware equivalent scaling W4，只改变论文核心机制；output_mse 0.0054 → 0.0052，相对基线 -4.22%。  inference-serving quantization 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-awq-9367c7ce">AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration</h2>
<p class="ar-learning-card__meta">MIT / NVIDIA / Harvard / SJTU · 论文公开：2023-06-01</p>
<p><strong>方法要点：</strong>利用 calibration activation 找到显著输入通道，通过等价通道缩放保护约 1% 关键权重，再执行硬件友好的统一低比特 weight-only 量化。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。用 WikiText-2 激活统计搜索 AWQ 等价缩放并真实执行 W4 量化；未使用 TinyChat CUDA kernel，MSE 不代表端到端吞吐。本地相对变化不得与原文指标混写。本地对照口径：基线为 round-to-nearest W4，实验组为 activation-aware equivalent scaling W4，只改变论文核心机制；output_mse 0.0054 → 0.0052，相对基线 -4.22%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2306.00978">原论文</a> · <a href="../../../../reproductions/2306.00978-awq/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints 基础模型 Google Research 2023-05-22 多个 query head 共享较少的 K/V head，在 MHA 质量与 MQA 解码带宽之间取得可控折中。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际让 4 个 query heads 分组共享 2 个 K/V heads，并报告 KV cache 缩减；从头小模型训练替代论文从 MHA checkpoint 的 5% compute uptraining。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 gqa；相对 PPL +2.15%。  attention kv-cache serving architecture 基础模型 推理压缩：权重、KV 缓存与服务带宽">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<h2 id="paper-foundation-models-gqa-9496fcce">GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints</h2>
<p class="ar-learning-card__meta">Google Research · 论文公开：2023-05-22</p>
<p><strong>方法要点：</strong>多个 query head 共享较少的 K/V head，在 MHA 质量与 MQA 解码带宽之间取得可控折中。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际让 4 个 query heads 分组共享 2 个 K/V heads，并报告 KV cache 缩减；从头小模型训练替代论文从 MHA checkpoint 的 5% compute uptraining。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 gqa；相对 PPL +2.15%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.13245">原论文</a> · <a href="../../../../reproductions/2305.13245-gqa/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
