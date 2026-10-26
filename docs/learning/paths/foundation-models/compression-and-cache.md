---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 推理压缩：权重、KV 缓存与服务带宽

[基础模型](index.md) / 29 个问题 · 29 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">29 个问题 · 29 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:moezip" data-paper-title="MoEZip: Routing-Aware KV Cache Compression for Sparse Mixture-of-Experts LLMs" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="MoEZip: Routing-Aware KV Cache Compression for Sparse Mixture-of-Experts LLMs 基础模型 Korea University 2026-10-21 MoE 的 KV 删除会扰动 attention 输出，进而改变路由。MoEZip 用已观察 instruction token 的路由分布 Fisher trace 作为敏感性代理，经 attention 传播到 context 位置，预留全局 routing anchors；其余预算沿用调用者提供的 dense/MoE base compressor 分数。future answer 不可用于真实选择。 完整实验成本过高，不复现（审查 DONE）；3 seeds 仍只是 L1 机制诊断，不构成 MoE 能力或质量提升证据。fisher_trace、select_cache、compress_cache 保留两种 gate、跨头 max、全局 anchors、App C 默认预算边界、base 排除重复补齐及真实 KV gather。输出原 context 索引并维持升序，调用者必须据此保留 position IDs。base 分数是显式接口，不伪装成已实现 KVZip。  MoE路由 KV缓存与稀疏推理 基础模型 推理压缩：权重、KV 缓存与服务带宽 MoEZip为什么要在普通KV压缩预算中预留路由锚点？ 删除KV不仅改变注意力输出，还可能改变后续专家路由。方法把已观察指令位置的路由Fisher敏感性经注意力传播到上下文，先保留全局锚点，其余沿用基础压缩器预算。该敏感性不是路由翻转的充分条件，未来答案和离线金标诊断不得进入真实选择器。 例如一段旧证据对答案词元注意力不高，却影响调用哪个专家，可被锚点保护；不能偷看将来的标准答案再倒选该保留哪段历史。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-moezip-03b66820" class="ar-learning-paper-anchor"></span>
<h2 id="qa-88eb9936565008cf">MoEZip为什么要在普通KV压缩预算中预留路由锚点？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amoezip">MoEZip: Routing-Aware KV Cache Compression for Sparse Mixture-of-Experts LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Korea University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>删除KV不仅改变注意力输出，还可能改变后续专家路由。方法把已观察指令位置的路由Fisher敏感性经注意力传播到上下文，先保留全局锚点，其余沿用基础压缩器预算。该敏感性不是路由翻转的充分条件，未来答案和离线金标诊断不得进入真实选择器。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一段旧证据对答案词元注意力不高，却影响调用哪个专家，可被锚点保护；不能偷看将来的标准答案再倒选该保留哪段历史。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30206v1">原论文</a> · <a href="../../../../foundation-models/2610.30206-moezip/">实现解读</a> · <a href="#qa-88eb9936565008cf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:right-on-q" data-paper-title="Right On Q: Recovering Reasoning under Quantization via Self-Generated Trajectories" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="Right On Q: Recovering Reasoning under Quantization via Self-Generated Trajectories 基础模型 University of Michigan, Ann Arbor 2026-10-21 低比特量化会改变模型生成的前缀。只在固定的全精度参考回答上蒸馏，不能覆盖量化学生真正遇到的错误和长推理状态。OnQ 从逐 block 校准开始，让量化学生自己生成回答，再由冻结的原始全精度教师在相同学生前缀上提供分布监督。第二个问题是同一前缀中不同候选 token 的偏差方向不同：学生既可能低估某些 token，也可能高估另一些 token。论文采用候选级 Dynamic KL，用教师与学生概率的比值调整 forward / reverse KL 的权重，而不是整句共用一个混合系数。 收录状态：高成本研究资料，完整实验不复现（审查 DONE）。后续若单独批准实现，至少需同时保留逐 block 初始化、学生真实量化前向 / rollout、冻结同前缀教师监督、候选级 stop-gradient 权重与残差概率类别，才可讨论对应保真度。收录状态：高成本研究资料，完整实验不复现（审查 DONE）。未实现 runtime、量化训练、教师服务或 benchmark；没有本地指标，没有 GPU 验证要求，也不进入 evolve 晋级。不能把本页的公式解读标成模型复现。正文 §4 与 Appendix A.1-A.2 给出完整训练预算：  模型压缩与量化 量化学生在策略蒸馏 基础模型 推理压缩：权重、KV 缓存与服务带宽 OnQ为什么在量化学生自己的前缀上蒸馏，并对同位置不同候选使用不同KL混合权重？ 量化改变生成路径，全精度教师标准轨迹未必覆盖学生实际错误状态。教师因此沿学生前缀评分，再按每个候选的师生概率比平衡正反KL，以分别处理低估和高估。混合系数停止梯度，近似词表还保留剩余质量桶，不能只归一化少数候选掩盖误差。 例如学生在一个前缀低估正确数字却高估某个连接词，两种偏差不应共用整句权重；教师也不能换回自己的理想前缀来评分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-right-on-q-5ed3d308" class="ar-learning-paper-anchor"></span>
<h2 id="qa-fbeed3269c200615">OnQ为什么在量化学生自己的前缀上蒸馏，并对同位置不同候选使用不同KL混合权重？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aright-on-q">Right On Q: Recovering Reasoning under Quantization via Self-Generated Trajectories</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Michigan, Ann Arbor</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>量化改变生成路径，全精度教师标准轨迹未必覆盖学生实际错误状态。教师因此沿学生前缀评分，再按每个候选的师生概率比平衡正反KL，以分别处理低估和高估。混合系数停止梯度，近似词表还保留剩余质量桶，不能只归一化少数候选掩盖误差。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生在一个前缀低估正确数字却高估某个连接词，两种偏差不应共用整句权重；教师也不能换回自己的理想前缀来评分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.29378v1">原论文</a> · <a href="../../../../foundation-models/2610.29378-right-on-q/">实现解读</a> · <a href="#qa-fbeed3269c200615">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:race-rope-compression" data-paper-title="RACE: RoPE-Aligned Attention Compression Based on Query-Key Activation Energies" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="RACE: RoPE-Aligned Attention Compression Based on Query-Key Activation Energies 基础模型 MIT CSAIL 2026-10-20 把KV写成低秩形式却在注意力前还原，可能节省缓存但增加运算。RACE直接改变注意力head的宽度：Q和K共享选择，只保留完整RoPE旋转对；V通过校准激活的右奇异子空间投影；再将两种变换折叠到Q/K/V/O权重。保留原模型频率及原head维度缩放，避免把缩小维度当作新模型重新编码。 整套矩阵超出本轮单A100/A30短时预算，成本过高，不复现（审查 DONE），不下载、不试跑、不进入重试队列。校准与该小向量诊断不是validation/test能力评测；race_pair_selection支持split-half和interleaved两种物理旋转布局；calibrate_race得到detached QK选择与V子空间；fold_race_weights真实生成缩小后的四个投影；native_race_attention仅在保留维度执行因果注意力，不还原完整Q/K/V。当前是单头、全RoPE参考算子，不是HuggingFace整模型转换器，也未实现GQA/partial-RoPE部署。  注意力与长上下文 KV缓存与原生维度压缩 基础模型 推理压缩：权重、KV 缓存与服务带宽 RACE压窄注意力后为什么仍保留原RoPE频率和原head缩放？ 压缩是原模型上的子空间变换，不是重新定义一套更窄模型。Q/K共同保留完整旋转对，频率不重编号，缩放仍按原维度；V子空间变换再折叠进输入输出权重，直接在低维计算。联合能量仅优化校准上界，不保证全局最小语言模型损失。 例如保留原来的第二和第五个旋转平面，应继续使用它们原频率；若把它们改编成第一、第二频率，就同时改变了位置编码含义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-race-rope-compression-5eb673ad" class="ar-learning-paper-anchor"></span>
<h2 id="qa-0fa836509cee57ad">RACE压窄注意力后为什么仍保留原RoPE频率和原head缩放？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Arace-rope-compression">RACE: RoPE-Aligned Attention Compression Based on Query-Key Activation Energies</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · MIT CSAIL</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>压缩是原模型上的子空间变换，不是重新定义一套更窄模型。Q/K共同保留完整旋转对，频率不重编号，缩放仍按原维度；V子空间变换再折叠进输入输出权重，直接在低维计算。联合能量仅优化校准上界，不保证全局最小语言模型损失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如保留原来的第二和第五个旋转平面，应继续使用它们原频率；若把它们改编成第一、第二频率，就同时改变了位置编码含义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28385v1">原论文</a> · <a href="../../../../foundation-models/2610.28385-race-rope-compression/">实现解读</a> · <a href="#qa-0fa836509cee57ad">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:flint" data-paper-title="FLINT: Fixed-budget Late Interaction" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="FLINT: Fixed-budget Late Interaction 基础模型 University of Illinois Urbana-Champaign 2026-10-19 ColBERT 对每个 token 保留向量，文档越长索引越大，长查询也需要更多次向量检索。ConstBERT 固定了文档侧预算，但查询仍逐 token。FLINT 则在共享 backbone 后，用两套不同的可学习 latent 分别读取查询和文档 token；交叉注意力、FFN 参数共享，双方输出都固定为个向量。它不是截取前个 token，也不是简单平均池化。 这些完整训练/索引/多基准实验明显超过单 A100/A30 的本轮短预算，标注成本过高，不复现（审查 DONE），不下载、不试跑、不进入自动重试队列。FlintLatentPool 实现共享多头 cross-attention、两套 latent、pre-LN、残差及 GELU FFN；FlintFixedBudgetRetrieval 接收已经编码的 token 张量，执行投影、归一化和 aligned-batch MaxSim。它不包含 tokenizer、BERT/ModernBERT backbone、教师蒸馏、训练数据或 PLAID 索引，因此不是可直接用于文本检索的完整模型。  推理与系统效率 多向量检索与固定预算池化 基础模型 推理压缩：权重、KV 缓存与服务带宽 FLINT把查询与文档都压成固定V个向量后，为什么评分仍不是对称平均相似度？ 两侧分别由可学习latent读取token，得到固定预算的多向量表示；后续对每个查询向量取文档侧最大匹配，再沿查询求和。两侧编码预算固定不意味着池化随意，也不意味着交换查询和文档后分数一样。关键在于查询各部分分别寻找最合适的文档证据。 教学例子：查询有“地点”和“时间”两个latent，每个各找文档中的最佳匹配再相加；若反过来要求文档所有latent都找查询匹配，求和对象变了，数值通常不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-flint-b6635740" class="ar-learning-paper-anchor"></span>
<h2 id="qa-10237052848a4d0f">FLINT把查询与文档都压成固定V个向量后，为什么评分仍不是对称平均相似度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aflint">FLINT: Fixed-budget Late Interaction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两侧分别由可学习latent读取token，得到固定预算的多向量表示；后续对每个查询向量取文档侧最大匹配，再沿查询求和。两侧编码预算固定不意味着池化随意，也不意味着交换查询和文档后分数一样。关键在于查询各部分分别寻找最合适的文档证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>查询有“地点”和“时间”两个latent，每个各找文档中的最佳匹配再相加；若反过来要求文档所有latent都找查询匹配，求和对象变了，数值通常不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.27273v1">原论文</a> · <a href="../../../../foundation-models/2610.27273-flint/">实现解读</a> · <a href="#qa-10237052848a4d0f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:drop-kv" data-paper-title="DropKV: Decoupling Residual-Output Perturbation for Near-Optimal KV-Cache Eviction" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="DropKV: Decoupling Residual-Output Perturbation for Near-Optimal KV-Cache Eviction 基础模型 University at Albany, SUNY 2026-10-15 只按 attention 权重淘汰 KV 会忽略 value 内容。DropKV 将组合驱逐近似为逐 token 输出扰动，跨观察窗口累加、池化，并保护近期 token。§3 与 Algorithm 1 定义评分；§4 的近似保证有条件，不能解释成任意输入上的全局最优。 完整 7B/8B 多模型、4K–128K、多预算、多基准评估超出本轮单 A100/A30 的低成本范围，成本过高，不复现（审查 DONE）。CUDA 诊断记录与真实GPU回执保存设备、种子及源码身份。无数据集/模型下载。输入为固定种子 42/43/44 的合成 Q/K/V，revision synthetic-formula-and-bit-patterns@oct17-foundation-components-v1，不是能力 benchmark。每 seed：1 batch、4 query heads、2 KV heads、19 历史槽、3 query、8 维，驱逐 7 项；不接触训练/验证/测试答案。  KV缓存 输出扰动驱逐 基础模型 推理压缩：权重、KV 缓存与服务带宽 DropKV为什么不只按attention权重低就淘汰，还要考虑value与当前输出的差？ 删除一项会同时移除它的value贡献并重新归一化其他权重，影响取决于p除以一减p，以及当前聚合输出与该value的差。高权重项若内容与输出接近，未必造成最大扰动；低权重但value特殊也可能重要。方法据单项扰动近似累计决策，近似保证有条件。 教学例子：两个token权重同为0.1，一个value几乎等于当前输出，另一个携带截然不同的信息；删去后者的输出变化可以大得多，权重本身分辨不出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-drop-kv-30cd8cec" class="ar-learning-paper-anchor"></span>
<h2 id="qa-ec49fca15913baed">DropKV为什么不只按attention权重低就淘汰，还要考虑value与当前输出的差？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adrop-kv">DropKV: Decoupling Residual-Output Perturbation for Near-Optimal KV-Cache Eviction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University at Albany, SUNY</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>删除一项会同时移除它的value贡献并重新归一化其他权重，影响取决于p除以一减p，以及当前聚合输出与该value的差。高权重项若内容与输出接近，未必造成最大扰动；低权重但value特殊也可能重要。方法据单项扰动近似累计决策，近似保证有条件。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个token权重同为0.1，一个value几乎等于当前输出，另一个携带截然不同的信息；删去后者的输出变化可以大得多，权重本身分辨不出。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22130">原论文</a> · <a href="../../../../foundation-models/2610.22130-drop-kv/">实现解读</a> · <a href="#qa-ec49fca15913baed">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:fpot" data-paper-title="Fractional Power-of-Two Quantization for Efficient and Effective Multiplier-Free LLM Inference" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="Fractional Power-of-Two Quantization for Efficient and Effective Multiplier-Free LLM Inference 基础模型 Seoul National University 2026-10-15 传统power-of-two权重网格较粗。FPoT将相邻指数间隔减半，兼顾4-bit量化误差与移位加法实现；对奇指数的平方根2系数使用1.5近似，并让校准直接适配这一实际网格，避免“先精确量化、部署时再替换系数”的额外误差。 这一实验矩阵成本过高，不复现（审查 DONE）。完整数据见实际A100逐seed诊断指标与真实GPU验收回执。固定公开合成recipe synthetic-fpot-and-native-layer-kernel-features@oct19-foundation-mechanisms-v1、seeds42/43/44。生成6×16权重与8×16整数激活；不下载模型或数据。每次只写新的不可变产物路径：  推理与系统效率 低比特量化与整数计算 基础模型 推理压缩：权重、KV 缓存与服务带宽 FPoT部署用1.5近似平方根2，为什么校准阶段也要使用这份实际网格？ 若先按精确半指数网格量化，部署再换近似系数，会引入校准未优化的额外误差。FPoT让尺度与相位选择适配真实移位加法网格，奇指数项由移位与加法实现。整数右移还有舍入细节，不能把它与实数乘1.5处处视为精确相同；激活与KV格式也有独立约定。 教学例子：一个权重被精确网格选到平方根2倍尺度，执行时却变成1.5倍；如果校准早知道会用1.5，就可重新选择尺度或码点，减少这次后置替换造成的偏差。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-fpot-d99f8a99" class="ar-learning-paper-anchor"></span>
<h2 id="qa-81d4a22b9952e7e2">FPoT部署用1.5近似平方根2，为什么校准阶段也要使用这份实际网格？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Afpot">Fractional Power-of-Two Quantization for Efficient and Effective Multiplier-Free LLM Inference</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Seoul National University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若先按精确半指数网格量化，部署再换近似系数，会引入校准未优化的额外误差。FPoT让尺度与相位选择适配真实移位加法网格，奇指数项由移位与加法实现。整数右移还有舍入细节，不能把它与实数乘1.5处处视为精确相同；激活与KV格式也有独立约定。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个权重被精确网格选到平方根2倍尺度，执行时却变成1.5倍；如果校准早知道会用1.5，就可重新选择尺度或码点，减少这次后置替换造成的偏差。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21257">原论文</a> · <a href="../../../../foundation-models/2610.21257-fpot/">实现解读</a> · <a href="#qa-81d4a22b9952e7e2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:remote-kv-tiers" data-paper-title="When the KV Cache Is Slower Than the GPU: Scaling Remote KV Tiers for Context-Parallel Prefill" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="When the KV Cache Is Slower Than the GPU: Scaling Remote KV Tiers for Context-Parallel Prefill 基础模型 Multiverse Computing 2026-10-15 缓存命中不一定更快。该工作先计算加载与重算的盈亏平衡带宽和固定开销，再把MLA KV缓存按PCP rank分片，并使用rank独立远程实例和异步加载消除队首阻塞。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地能力指标、训练结果或可执行 Evolve 算子。无本地adapter、指标文件或GPU回执，也不登记可执行Evolve算子。原论文结果仅作为阅读资料。范围见本轮实现与审查合同。本轮只完成方法、资源需求、公开代码状态及原图收录，没有运行完整实验、下载checkpoint或制造模拟能力分数。  推理与系统效率 KV缓存与分布式服务 基础模型 推理压缩：权重、KV 缓存与服务带宽 远程KV命中为什么有时比直接重新prefill更慢？ 加载需要固定请求开销与随KV体积增长的传输时间，重算则由模型预填充吞吐决定。只有带宽与长度越过盈亏平衡，命中才划算；分片实例和异步加载还要避免队首阻塞。缓存命中率不是延迟收益，本地仅文献收录，没有远程系统适配器或GPU结果。 例如一个很短前缀的KV虽已缓存，但远程连接等待超过本地重算时间；把命中次数提高，并不能保证用户首词延迟下降。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-remote-kv-tiers-30f3c03e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-a402f43cbcb16963">远程KV命中为什么有时比直接重新prefill更慢？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aremote-kv-tiers">When the KV Cache Is Slower Than the GPU: Scaling Remote KV Tiers for Context-Parallel Prefill</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Multiverse Computing</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>加载需要固定请求开销与随KV体积增长的传输时间，重算则由模型预填充吞吐决定。只有带宽与长度越过盈亏平衡，命中才划算；分片实例和异步加载还要避免队首阻塞。缓存命中率不是延迟收益，本地仅文献收录，没有远程系统适配器或GPU结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个很短前缀的KV虽已缓存，但远程连接等待超过本地重算时间；把命中次数提高，并不能保证用户首词延迟下降。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21500">原论文</a> · <a href="../../../../foundation-models/2610.21500-remote-kv-tiers/">实现解读</a> · <a href="#qa-a402f43cbcb16963">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:roleq" data-paper-title="RoleQ: Role-Aligned Scales for Converting Language Models to Ternary" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="RoleQ: Role-Aligned Scales for Converting Language Models to Ternary 基础模型 Harvard University 2026-10-15 按矩阵布局统一逐行放scale，会把写入残差流的不同功能单元混在一起。RoleQ按功能角色选轴：reader（Q/K/V与MLP输入）每输出单元一scale，writer（O与MLP输出）每输入单元一scale。完整RoleQ-T还需要旋转、GPTQ、蒸馏及可选Fisher二平面，不能以单个量化函数替代。 原文8B转换3–4 A100小时、二平面阶段不足10小时，完整实验成本过高，不复现（审查 DONE）。CUDA诊断记录与真实GPU回执保存设备、种子、真实测量与源码身份。固定seeds42/43/44；合成公式revision synthetic-formula-and-bit-patterns@oct17-foundation-components-v1，无预训练模型或能力数据。runner用长度4向量全部81种三值码独立穷举全局最优；单测长度5、243码。7×11矩阵用于角色轴与pack/unpack。  量化与压缩 角色对齐三值量化 基础模型 推理压缩：权重、KV 缓存与服务带宽 RoleQ为什么给reader按输出单元放scale，却给writer按输入单元放scale？ reader各输出单元读取信息，writer各输入单元向残差流写入贡献，功能方向不同，统一按矩阵行量化会混合这些单元。三值单向量解对所声明轴的未加权目标可精确求得，但不等于整模型量化全局最优；完整流程还需旋转、误差补偿及蒸馏。 例如输出投影的一列代表某输入特征写向多个残差维度，应作为功能向量处理；不能仅因权重存储为行就机械逐行给scale。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-roleq-9df6d043" class="ar-learning-paper-anchor"></span>
<h2 id="qa-cf8caf43e45c624a">RoleQ为什么给reader按输出单元放scale，却给writer按输入单元放scale？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aroleq">RoleQ: Role-Aligned Scales for Converting Language Models to Ternary</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harvard University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>reader各输出单元读取信息，writer各输入单元向残差流写入贡献，功能方向不同，统一按矩阵行量化会混合这些单元。三值单向量解对所声明轴的未加权目标可精确求得，但不等于整模型量化全局最优；完整流程还需旋转、误差补偿及蒸馏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如输出投影的一列代表某输入特征写向多个残差维度，应作为功能向量处理；不能仅因权重存储为行就机械逐行给scale。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21808">原论文</a> · <a href="../../../../foundation-models/2610.21808-roleq/">实现解读</a> · <a href="#qa-cf8caf43e45c624a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:rope-relay" data-paper-title="Compression Does Not End at Selection: Post-Selection Positional Geometry for Sparse KV Caches" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="Compression Does Not End at Selection: Post-Selection Positional Geometry for Sparse KV Caches 基础模型 National University of Defense Technology 2026-10-15 selector 删除 token 后，K 仍携带稀疏旧坐标的旋转相位。RoPERelay 不重选内容、不重新 prefill 历史，将选中状态按原始时间排序、压紧坐标，并同步问题及生成坐标。来源为 §3、附录 A 的 Algorithm 1 和数值约定。 按该公开配置，完整多臂长上下文评测超出本轮单 A100/A30/Mac 的低成本预算，成本过高，不复现（审查 DONE），不下载权重或大数据。用合成固定 K/V 进行独立 complex 参考与 attention/梯度诊断，未加载模型或长记忆数据。保留实数 Torch 梯度的 cache 算子，支持 scaled/partial RoPE、split-half/interleaved 两种布局、异长 mask、共同 continuation anchor。用合成固定 K/V 进行独立 complex 参考与 attention/梯度诊断，未加载模型或长记忆数据。  KV缓存 旋转位置重建 基础模型 推理压缩：权重、KV 缓存与服务带宽 RoPERelay压紧稀疏KV坐标时，为什么只重旋转K而不对V做同样旋转？ 选择后的键仍带原位置相位，需要先逆去旧旋转再施加紧凑新坐标；值只同步排序，不承载该键位置旋转。各头长度不同时还需共享右端锚点，并同步问题和后续生成位置。它修复坐标而不重选证据，缩放旋转的逆也不能误写为单位旋转转置。 例如保留历史第十和第一百个位置后，将它们搬到连续槽位，K要重建相位，V只搬位置；问题也要从新锚点开始，不能沿旧编号。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-rope-relay-6493fdc7" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f27fcf57090c69bc">RoPERelay压紧稀疏KV坐标时，为什么只重旋转K而不对V做同样旋转？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Arope-relay">Compression Does Not End at Selection: Post-Selection Positional Geometry for Sparse KV Caches</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Defense Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>选择后的键仍带原位置相位，需要先逆去旧旋转再施加紧凑新坐标；值只同步排序，不承载该键位置旋转。各头长度不同时还需共享右端锚点，并同步问题和后续生成位置。它修复坐标而不重选证据，缩放旋转的逆也不能误写为单位旋转转置。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如保留历史第十和第一百个位置后，将它们搬到连续槽位，K要重建相位，V只搬位置；问题也要从新锚点开始，不能沿旧编号。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21126">原论文</a> · <a href="../../../../foundation-models/2610.21126-rope-relay/">实现解读</a> · <a href="#qa-f27fcf57090c69bc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:pn-mix" data-paper-title="PN-Mix: Pair-Norm Guided Mixed-Precision Key Cache Quantization for Efficient Long-Output LLM Inference" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="PN-Mix: Pair-Norm Guided Mixed-Precision Key Cache Quantization for Efficient Long-Output LLM Inference 基础模型 Seoul National University 2026-10-14 长输出解码的 KV cache 随 token 数增长；一律把 K 降到低位宽，会放大 attention logit 的偏差。PN-Mix 的精度分配不是仅按 K 的幅度排序：它同时观察 prefill 的 Q 和 K，把实际 RoPE 旋转耦合的两个通道作为整体，以两侧平均范数乘积预测重要性。每个 KV head 选择一次高精度通道对，后续所有量化页复用这份选择，不读取未来解码状态重选。 完整 8B–32B、32K 输出、多任务与吞吐研究为成本过高，不复现（审查 DONE）；本地是 L1 可执行组件诊断，不是完整论文效果复现。本地是 L1 可执行组件诊断，不是完整论文效果复现。已实现 prefill 的 query–key 通道对评分、H3/L1 真正打包、1-bit 中点校正、sink/residual 缓存与量化后 attention 消费。完整 8B–32B、32K 输出、多任务与吞吐研究为成本过高，不复现（审查 DONE）；不进入自动 Evolve 晋级。本地对照口径：基线与实验组使用同一 Q/K/V、因果位置与输入网络；  kv-cache quantization inference-serving long-context 基础模型 推理压缩：权重、KV 缓存与服务带宽 PN-Mix为什么按真实RoPE通道对的Q/K范数乘积分配精度，而不只看K幅度？ 注意力误差由查询与键共同决定，只看键大小会忽视查询是否使用该方向。把同一旋转平面的两维整体评分，才能保留RoPE耦合结构；每个共享KV头在预填充阶段选定高精度对并复用，不能读取未来解码状态重选。存储布局相邻也未必是实际旋转配对。 例如某键方向很大但查询几乎不用，未必最值得高精度；Llama前后半维配对时，把内存相邻两维当一对会保护错误方向。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-pn-mix-d9cac8c7" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1d6512262c17fb80">PN-Mix为什么按真实RoPE通道对的Q/K范数乘积分配精度，而不只看K幅度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Apn-mix">PN-Mix: Pair-Norm Guided Mixed-Precision Key Cache Quantization for Efficient Long-Output LLM Inference</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Seoul National University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>注意力误差由查询与键共同决定，只看键大小会忽视查询是否使用该方向。把同一旋转平面的两维整体评分，才能保留RoPE耦合结构；每个共享KV头在预填充阶段选定高精度对并复用，不能读取未来解码状态重选。存储布局相邻也未必是实际旋转配对。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某键方向很大但查询几乎不用，未必最值得高精度；Llama前后半维配对时，把内存相邻两维当一对会保护错误方向。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19605">原论文</a> · <a href="../../../../reproductions/2610.19605-pn-mix/">实现解读</a> · <a href="#qa-1d6512262c17fb80">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:dualquant" data-paper-title="DualQuant: Dual-scale Calibration-free Weight-and-Activation Quantization for LLMs" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="DualQuant: Dual-scale Calibration-free Weight-and-Activation Quantization for LLMs 基础模型 d-Matrix 2026-10-09 W+A量化中，权重与激活误差相互放大；仅最小化逐row动态范围不能消除跨row系统性column outlier。DualQuant只读取静态权重，以row/block尺度与column尺度共同最小化重建MSE。column尺度同时变成推理时的激活重缩放，不需要校准样本、激活统计或Hessian。 默认量化公开SmolLM2-135M的前四个decoder nn.Linear，每row tile128、column group32，属于部分checkpoint机制诊断；本地对照口径：相同公开checkpoint中相同线性层的single-scale INT4 W+A为基线，dual-scale为实验组；相对吞吐和内存不适用，software simulation只报告重建MSE与隔离test NLL。  quantization calibration-free weight-activation-quantization 基础模型 推理压缩：权重、KV 缓存与服务带宽 DualQuant不看校准激活，为什么仍要同时求row尺度与column尺度？ 只平衡每行范围无法消除跨行共用的异常列；方法以静态权重重构误差联合求两侧尺度，列尺度再成为推理时的激活重缩放。固定codes时解一维最小二乘，并投影到格式合法尺度，再重新量化迭代。它不是简单搜索几个经验指数，也不保证codes变化期间误差无条件单调。 教学例子：同一列在许多行都特别大，只做逐行缩放仍会留下系统性列不平衡；列尺度可共同处理它，但必须同步调整输入并使用硬件可表示的尺度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-dualquant-6a91d161" class="ar-learning-paper-anchor"></span>
<h2 id="qa-446916bce4be2de7">DualQuant不看校准激活，为什么仍要同时求row尺度与column尺度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adualquant">DualQuant: Dual-scale Calibration-free Weight-and-Activation Quantization for LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · d-Matrix</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只平衡每行范围无法消除跨行共用的异常列；方法以静态权重重构误差联合求两侧尺度，列尺度再成为推理时的激活重缩放。固定codes时解一维最小二乘，并投影到格式合法尺度，再重新量化迭代。它不是简单搜索几个经验指数，也不保证codes变化期间误差无条件单调。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一列在许多行都特别大，只做逐行缩放仍会留下系统性列不平衡；列尺度可共同处理它，但必须同步调整输入并使用硬件可表示的尺度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13767">原论文</a> · <a href="../../../../reproductions/2610.13767-dualquant/">实现解读</a> · <a href="#qa-446916bce4be2de7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:replayssm" data-paper-title="ReplaySSM: Cache SSM Inputs, Not State" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="ReplaySSM: Cache SSM Inputs, Not State 基础模型 Princeton University 2026-10-09 Mamba2/GDN 解码一般每 token 读写完整矩阵状态，常受显存带宽限制。ReplaySSM 把持久化状态与输出计算拆开：每 16 token 才刷新 checkpoint，其间只记录小型输入；输出由 checkpoint 与输入重放计算。投机验证使用 output-only 形式，避免为每个 draft 物化完整状态。接受长度只推进已提交输入指针；被拒 draft 不进入 recurrence。 不签失败为 passed，也不把新证据重绑定到未执行的新源码。cpu-contracts.json记录 seed 42 独立参考：最大输出误差 1.1920928955078125e-7、接受 12 个 token、刷新 3 次；4 个行为测试覆盖公式、GDN、pending/rollback 和低精度 read 不进入 recurrence。core_mechanism / L1 分成两条证据：独立 PyTorch 参考执行 checkpoint、accept/rollback、output-only、GDN 三角解与双精度刷新；  推理与系统效率 SSM 缓存与回滚 基础模型 推理压缩：权重、KV 缓存与服务带宽 ReplaySSM为什么只提交被接受的输入，并让高精度递归锚点独立于低精度读出副本？ 输出可从检查点和短输入记录重放，减少每词元完整状态写回；投机拒绝的草稿不能进入已提交递归。低精度副本只用于读取，更新须从高精度锚点与原始记录重建，避免舍入误差逐轮反馈。输出重括号计算也不等于省略递归依赖。 例如提议四个草稿仅接受两个，状态指针只推进两步；刷新时从真实接受输入重算，不能把被拒后缀或已舍入读出当成新锚点。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-replayssm-704fd9a0" class="ar-learning-paper-anchor"></span>
<h2 id="qa-e28927a2b0831632">ReplaySSM为什么只提交被接受的输入，并让高精度递归锚点独立于低精度读出副本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Areplayssm">ReplaySSM: Cache SSM Inputs, Not State</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>输出可从检查点和短输入记录重放，减少每词元完整状态写回；投机拒绝的草稿不能进入已提交递归。低精度副本只用于读取，更新须从高精度锚点与原始记录重建，避免舍入误差逐轮反馈。输出重括号计算也不等于省略递归依赖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如提议四个草稿仅接受两个，状态指针只推进两步；刷新时从真实接受输入重算，不能把被拒后缀或已舍入读出当成新锚点。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13778">原论文</a> · <a href="../../../../reproductions/2610.13778-replayssm/">实现解读</a> · <a href="#qa-e28927a2b0831632">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:vfold" data-paper-title="VFold: Symmetry-Aware Cross-Layer Value Cache Compression" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="VFold: Symmetry-Aware Cross-Layer Value Cache Compression 基础模型 Johns Hopkins University 2026-10-08 相邻层的 Value 不一定在同一坐标系。VFold 用满秩 CCA 对齐和 Hungarian 头匹配，离线把变换折进 Value/输出投影；当前 token 先以完整 Value 参与注意力，随后才与相邻层平均共享。Key 不合并，首尾重要 token 独立保存。 已实现真实权重折叠和持久共享缓存；当前结果是 L1 运行诊断，不是 LongBench/RULER 能力复现或推理加速证明。使用 Qwen3-4B、A100、seed 42；32 个训练问题校准，4 个训练集派生的独立验证问题解码，最多生成 256 token。数据来源、安装及参数见运行说明。  推理与系统效率 KV 缓存压缩 基础模型 推理压缩：权重、KV 缓存与服务带宽 VFold为什么先对齐相邻层的Value坐标，再共享缓存，而且当前词元先用完整Value？ 不同层的值空间未必可直接平均，CCA与头匹配先建立可比较坐标，并把变换折进值与输出投影。当前词元先完成完整注意力，再进入跨层共享，限制即时扰动；键和重要首尾词元保持独立。可逆变换的等价性不表示后续平均也完全无损。 例如两层各用不同坐标表示同一特征，直接平均会抵消信息；先对齐再共享较合理，但仍须评估平均近似的影响，不能称为严格无损。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-vfold-b54fea4f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-5e1e272ca0060eaa">VFold为什么先对齐相邻层的Value坐标，再共享缓存，而且当前词元先用完整Value？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Avfold">VFold: Symmetry-Aware Cross-Layer Value Cache Compression</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Johns Hopkins University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同层的值空间未必可直接平均，CCA与头匹配先建立可比较坐标，并把变换折进值与输出投影。当前词元先完成完整注意力，再进入跨层共享，限制即时扰动；键和重要首尾词元保持独立。可逆变换的等价性不表示后续平均也完全无损。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两层各用不同坐标表示同一特征，直接平均会抵消信息；先对齐再共享较合理，但仍须评估平均近似的影响，不能称为严格无损。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12338">原论文</a> · <a href="../../../../foundation-models/2610.12338-vfold/">实现解读</a> · <a href="#qa-5e1e272ca0060eaa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:irekogpt" data-paper-title="IrekoGPT: Turning Structured Pruning into Post-Hoc Slimmable LLMs" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="IrekoGPT: Turning Structured Pruning into Post-Hoc Slimmable LLMs 基础模型 University of Modena and Reggio Emilia 2026-10-01 保留 SliceGPT 投影矩阵而非直接丢弃，使同一 checkpoint 暴露嵌套宽度；再以多压缩率校准和 ridge 修正下游线性层。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行嵌套子网合同；未加载原模型或复现吞吐。执行嵌套子网合同；未加载原模型或复现吞吐。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  结构剪枝 可伸缩模型 推理效率 基础模型 推理压缩：权重、KV 缓存与服务带宽 IrekoGPT为什么保留投影基，才能让一个检查点支持多种嵌套宽度？ 结构化剪枝若直接丢弃被裁方向，就固定了模型宽度。保留有序投影基后，不同宽度可取同一基的不同前缀，再用多压缩率校准与下游线性修正减轻切换误差。共享嵌套结构不保证所有宽度质量相同，本地只验证子网合同，未测原模型吞吐。 例如同一检查点临时取较窄子网处理简单请求，再恢复较宽子网；若之前把其余投影永久删除，就无法靠切换参数恢复这些方向。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-irekogpt-3d6c018e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-7a064a673ce4212b">IrekoGPT为什么保留投影基，才能让一个检查点支持多种嵌套宽度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Airekogpt">IrekoGPT: Turning Structured Pruning into Post-Hoc Slimmable LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Modena and Reggio Emilia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>结构化剪枝若直接丢弃被裁方向，就固定了模型宽度。保留有序投影基后，不同宽度可取同一基的不同前缀，再用多压缩率校准与下游线性修正减轻切换误差。共享嵌套结构不保证所有宽度质量相同，本地只验证子网合同，未测原模型吞吐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一检查点临时取较窄子网处理简单请求，再恢复较宽子网；若之前把其余投影永久删除，就无法靠切换参数恢复这些方向。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00426">原论文</a> · <a href="../../../../foundation-models/2610.00426-irekogpt/">实现解读</a> · <a href="#qa-7a064a673ce4212b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:leapquant" data-paper-title="LeapQuant: Efficient Linear Attention with Accurate Recurrent State Quantization" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="LeapQuant: Efficient Linear Attention with Accurate Recurrent State Quantization 基础模型 UC Berkeley 2026-09-29 逐 token 量化递归状态会不断重新舍入。LeapQuant 在一个窗口内保留低比特基态，并以高精度缓冲本窗口更新，窗口末才量化一次；同时把最大 outlier 分解成少量高精度 compensator tokens，对剩余状态平滑后再量化。 复现级别：L1 机制实现。复现级别：L1 机制实现。保留 per-window state quantization、低秩补偿 token 与 residual smoothing；未复刻论文 CUDA kernel 和完整模型吞吐。机制诊断覆盖窗口边界、补偿 rank、状态误差及 CUDA 执行；未实现作者专用 kernel。A100 脱敏记录见 ../../gpu-validations/leapquant-a100-20260930.json。  推理与系统效率 线性注意力 状态量化 基础模型 推理压缩：权重、KV 缓存与服务带宽 LeapQuant为什么把窗口内更新保留高精度，而不在每个递归步骤重新量化？ 递归状态被反复舍入时，误差会反馈到后续更新。窗口内以低比特基态加高精度增量表示，只在边界重量化，可减少重复舍入；补偿项另保护显著异常方向。窗口缓冲与补偿也有存储成本，本地截断SVD是诊断构造，未实现作者专用内核或复现吞吐。 例如一段连续的小更新先积累后再舍入，避免每次都被低位宽抹掉；强异常方向单独补回，并非把所有状态都偷偷保留全精度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-leapquant-7df56645" class="ar-learning-paper-anchor"></span>
<h2 id="qa-7d05f7382a4bdff1">LeapQuant为什么把窗口内更新保留高精度，而不在每个递归步骤重新量化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aleapquant">LeapQuant: Efficient Linear Attention with Accurate Recurrent State Quantization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>递归状态被反复舍入时，误差会反馈到后续更新。窗口内以低比特基态加高精度增量表示，只在边界重量化，可减少重复舍入；补偿项另保护显著异常方向。窗口缓冲与补偿也有存储成本，本地截断SVD是诊断构造，未实现作者专用内核或复现吞吐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一段连续的小更新先积累后再舍入，避免每次都被低位宽抹掉；强异常方向单独补回，并非把所有状态都偷偷保留全精度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38166">原论文</a> · <a href="../../../../foundation-models/2609.38166-leapquant/">实现解读</a> · <a href="#qa-7d05f7382a4bdff1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:splash" data-paper-title="SPLASH: Switching Parallel Layouts of Attention with Seamless Handoff for LLM Serving" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="SPLASH: Switching Parallel Layouts of Attention with Seamless Handoff for LLM Serving 基础模型 Institute of Computing Technology, Chinese Academy of Sciences 2026-09-29 统一描述 attention weight 与 KV cache 的所有权，引入权重分片、请求独占 KV 的 DOP；调度器把布局切换成本按剩余步数摊销，在 TP、DP、CP、DOP 间在线切换。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行内存模型和 transition-aware layout planner；未实现 CUDA handoff，也不声称经过 B200/H200 性能验证。执行内存模型和 transition-aware layout planner；未实现 CUDA handoff，也不声称经过 B200/H200 性能验证。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  推理系统 并行布局 KV cache 基础模型 推理压缩：权重、KV 缓存与服务带宽 SPLASH为什么要把布局切换成本摊到剩余生成步数，而不能只选当前最快布局？ 不同并行布局分配注意力权重与KV所有权的方式不同，切换会引入搬运和交接成本。剩余步骤足够多时，后续收益才可能覆盖一次转换；只看单步速度会频繁切换而更慢。内存可行性也需同时满足，本地只有规划器，没有真实CUDA交接与服务吞吐证据。 例如请求只剩少量词元，搬一次缓存可能比继续旧布局更贵；长请求则可能值得转换，不能让两者仅按相同单步耗时决策。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-splash-7002fc08" class="ar-learning-paper-anchor"></span>
<h2 id="qa-6e69fab0b2bf646b">SPLASH为什么要把布局切换成本摊到剩余生成步数，而不能只选当前最快布局？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asplash">SPLASH: Switching Parallel Layouts of Attention with Seamless Handoff for LLM Serving</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Computing Technology, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同并行布局分配注意力权重与KV所有权的方式不同，切换会引入搬运和交接成本。剩余步骤足够多时，后续收益才可能覆盖一次转换；只看单步速度会频繁切换而更慢。内存可行性也需同时满足，本地只有规划器，没有真实CUDA交接与服务吞吐证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如请求只剩少量词元，搬一次缓存可能比继续旧布局更贵；长请求则可能值得转换，不能让两者仅按相同单步耗时决策。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37626">原论文</a> · <a href="../../../../foundation-models/2609.37626-splash/">实现解读</a> · <a href="#qa-6e69fab0b2bf646b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:stepquant" data-paper-title="STEPQuant: When and Where Errors Matter in Delta-Rule Recurrent State Quantization" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="STEPQuant: When and Where Errors Matter in Delta-Rule Recurrent State Quantization 基础模型 Zhejiang University 2026-09-29 Delta-rule 线性注意力的固定大小状态会被每个并发请求长期持有，统一低比特量化又会让误差随更新累积。STEPQuant 同时建模状态记忆的剩余寿命和不同 key row 对输出的影响：在固定平均 bit 预算下给重要块更高精度，再用 key-row / value-column 两组 scale 拟合状态分布。 复现级别：L1 机制实现。复现级别：L1 机制实现。本地实现寿命感知 bit 分配与行/列双轴 scale 拟合；未复刻 SGLang kernel、Qwen3.8/Kimi-Linear 全模型吞吐。本地验证 bit 预算、有限 scale、递归状态 MSE 和 CUDA 前后向；不声称复现论文吞吐或精度。A100 脱敏记录见 ../../gpu-validations/stepquant-a100-20260930.json。  推理与系统效率 线性注意力 状态量化 基础模型 推理压缩：权重、KV 缓存与服务带宽 STEPQuant为什么同时看状态的剩余寿命和key行影响，再分配bit预算？ 递归状态误差能持续传播，而不同方向对输出的影响也不相同；只按当前幅度分配精度会漏掉时间与空间两类重要性。方法在平均bit约束下分配块精度，并用行列两轴scale拟合状态。本地预算与误差诊断未复现论文吞吐，也不是统一INT8改名。 例如一个不大的状态方向会影响许多后续步，可能比即将被遗忘的大值更值得保留精度；预算有限时需要比较累计风险。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-stepquant-3ce3e159" class="ar-learning-paper-anchor"></span>
<h2 id="qa-fdaae29f29c743af">STEPQuant为什么同时看状态的剩余寿命和key行影响，再分配bit预算？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Astepquant">STEPQuant: When and Where Errors Matter in Delta-Rule Recurrent State Quantization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>递归状态误差能持续传播，而不同方向对输出的影响也不相同；只按当前幅度分配精度会漏掉时间与空间两类重要性。方法在平均bit约束下分配块精度，并用行列两轴scale拟合状态。本地预算与误差诊断未复现论文吞吐，也不是统一INT8改名。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个不大的状态方向会影响许多后续步，可能比即将被遗忘的大值更值得保留精度；预算有限时需要比较累计风险。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38169">原论文</a> · <a href="../../../../foundation-models/2609.38169-stepquant/">实现解读</a> · <a href="#qa-fdaae29f29c743af">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:agentkv" data-paper-title="AgentKV: Phase-Aware KV Eviction for Agentic LLMs" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="AgentKV: Phase-Aware KV Eviction for Agentic LLMs 基础模型 University of Cambridge 2026-09-14 按 Agent 阶段保留代表性 query buffer，以跨阶段查询相关性决定 KV 淘汰。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 phase-aware scoring；未修改 SGLang 或运行 CUDA kernel。本地执行 phase-aware scoring；未修改 SGLang 或运行 CUDA kernel。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  Agent 推理 KV Cache 基础模型 推理压缩：权重、KV 缓存与服务带宽 AgentKV为何保留跨阶段代表query，而不只用最近几步决定淘汰哪些KV？ Agent任务会在规划、工具使用和总结等阶段切换；最近query只代表当前阶段，可能低估稍后会重新需要的证据。代表query buffer让缓存重要性兼顾多个阶段的读取需求。它改变淘汰依据，不会让被删除的KV自动可恢复，阶段代表性本身也需要验证。 教学例子：工具执行阶段反复关注命令参数，但最终总结还要回看最初的任务要求；只按最近命令查询淘汰，可能把最后仍需要的要求删掉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-agentkv-c25693b7" class="ar-learning-paper-anchor"></span>
<h2 id="qa-df79f24c8c97731f">AgentKV为何保留跨阶段代表query，而不只用最近几步决定淘汰哪些KV？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aagentkv">AgentKV: Phase-Aware KV Eviction for Agentic LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Cambridge</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Agent任务会在规划、工具使用和总结等阶段切换；最近query只代表当前阶段，可能低估稍后会重新需要的证据。代表query buffer让缓存重要性兼顾多个阶段的读取需求。它改变淘汰依据，不会让被删除的KV自动可恢复，阶段代表性本身也需要验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>工具执行阶段反复关注命令参数，但最终总结还要回看最初的任务要求；只按最近命令查询淘汰，可能把最后仍需要的要求删掉。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.14872">原论文</a> · <a href="../../../../foundation-models/2609.14872-agentkv/">实现解读</a> · <a href="#qa-df79f24c8c97731f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:beaconkv" data-paper-title="BeaconKV: Key-Value Cache Compression Guided by Beacon Queries for Efficient Large Reasoning Model Inference" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="BeaconKV: Key-Value Cache Compression Guided by Beacon Queries for Efficient Large Reasoning Model Inference 基础模型 Hanyang University 2026-09-04 长推理中会出现重新关注早期计划的 Thought Revisiting Token，只用最近 query 预测未来注意力会丢失这些远程依赖。BeaconKV 对历史 query 聚类并维护少量代表 query，用它们为 KV 重要性投票，在固定缓存预算中兼顾近期上下文和远程重访。 复现级别：核心选择算法 + 真实 checkpoint CUDA smoke。复现级别：核心选择算法 + 真实 checkpoint CUDA smoke。保留近期 token，并用最远点采样维护能代表历史查询簇的 beacon。旧版 checkpoint 验证漏掉 query normalization 与 RoPE，并在 softmax 前平均 GQA query head，旧相似度作废。  kv-cache long-context reasoning inference-serving 基础模型 推理压缩：权重、KV 缓存与服务带宽 BeaconKV怎样避免“只看近期query”删掉长推理稍后还会重访的计划？ 它对历史query保持少量具有代表性的beacon，用这些代表查询为KV重要性提供跨阶段依据，并保护近期窗口。这样淘汰不完全受最近一步支配，适合推理中回看早期思路的情况。代表查询只能近似未来需求，不能保证固定预算内所有远程证据都保存。 教学例子：中间十步都在计算局部数字，最后却要检查最初的计划约束；早期beacon可让相关KV继续获得重要性，而不因十步未被关注就立刻淘汰。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-beaconkv-c9b2fe88" class="ar-learning-paper-anchor"></span>
<h2 id="qa-8c86ea72842083a1">BeaconKV怎样避免“只看近期query”删掉长推理稍后还会重访的计划？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Abeaconkv">BeaconKV: Key-Value Cache Compression Guided by Beacon Queries for Efficient Large Reasoning Model Inference</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Hanyang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它对历史query保持少量具有代表性的beacon，用这些代表查询为KV重要性提供跨阶段依据，并保护近期窗口。这样淘汰不完全受最近一步支配，适合推理中回看早期思路的情况。代表查询只能近似未来需求，不能保证固定预算内所有远程证据都保存。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>中间十步都在计算局部数字，最后却要检查最初的计划约束；早期beacon可让相关KV继续获得重要性，而不因十步未被关注就立刻淘汰。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04971">原论文</a> · <a href="../../../../reproductions/2609.04971-beaconkv/">实现解读</a> · <a href="#qa-8c86ea72842083a1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:kvmem" data-paper-title="KVMem: Virtualizing Million-Token Agent Workspaces on a Consumer GPU" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="KVMem: Virtualizing Million-Token Agent Workspaces on a Consumer GPU 基础模型 Shanghai University of Finance and Economics 2026-09-04 长寿命 Agent 的历史会同时超过显存和模型原生窗口；摘要压缩会丢证据，文本检索又要重复 prefill。KVMEM 把已计算 KV 分页放到 GPU、主存和 NVMe，用模型自身的注意力空间索引挑选相关 block，再物化为不超过原生窗口的执行视图。 复现级别：查询相关 block 选择 + 真实 checkpoint CUDA smoke。复现级别：查询相关 block 选择 + 真实 checkpoint CUDA smoke。实现固定显存预算下的 query-conditioned KV 工作视图。旧版 checkpoint 验证漏掉 query normalization 与 RoPE，并在 softmax 前平均 GQA query head，旧相似度作废。  agent-memory kv-cache long-context inference-serving 基础模型 推理压缩：权重、KV 缓存与服务带宽 KVMEM把历史地址空间与执行窗口分开，为什么不等于模型一次注意全部历史？ 历史KV分块存放在不同存储层，当前查询在注意力空间检索相关块，再物化成原生窗口内的执行视图。地址可以很大，单步注意的内容仍有界，未命中证据可能被遗漏。本地参考路径还保留完整后备缓存，未实现完整异步分层系统，不能据此宣称显存节省或加速。 例如长会话有许多旧文件，当前只把检索命中的几块KV搬入窗口；这避免重复处理全文，但没有让窗口外全部证据同时参与注意。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-kvmem-cf5b3efc" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d8a15b1ab7d92db2">KVMEM把历史地址空间与执行窗口分开，为什么不等于模型一次注意全部历史？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Akvmem">KVMem: Virtualizing Million-Token Agent Workspaces on a Consumer GPU</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai University of Finance and Economics</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>历史KV分块存放在不同存储层，当前查询在注意力空间检索相关块，再物化成原生窗口内的执行视图。地址可以很大，单步注意的内容仍有界，未命中证据可能被遗漏。本地参考路径还保留完整后备缓存，未实现完整异步分层系统，不能据此宣称显存节省或加速。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如长会话有许多旧文件，当前只把检索命中的几块KV搬入窗口；这避免重复处理全文，但没有让窗口外全部证据同时参与注意。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04852">原论文</a> · <a href="../../../../reproductions/2609.04852-kvmem/">实现解读</a> · <a href="#qa-d8a15b1ab7d92db2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:random-attention" data-paper-title="Random Attention: Rethinking KV Cache Eviction for Efficient Reasoning" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="Random Attention: Rethinking KV Cache Eviction for Efficient Reasoning 基础模型 Salesforce AI Research / University of Illinois Urbana-Champaign 2026-09-03 传统 KV 淘汰先计算 token 重要性，Random Attention 则始终保护 prompt，仅在已生成 token 中逐 head 独立随机保留固定预算；它省掉评分 pass，也避免所有 head 被同一排序规则约束。 复现级别：核心机制 + 真实 checkpoint GPU 验证。复现级别：核心机制 + 真实 checkpoint GPU 验证。保留完整 prompt，并对生成 trace 按 attention head 独立均匀随机采样。未声称复刻论文六任务矩阵和官方 vLLM kernel 吞吐；本地 GPU 路径验证真实 KV 张量上的选择与 attention 重建，并可作为 LLM Evolve attention 算子。CPU 三 seed 机制结果见 metrics/public-seeds42-44.json；  kv-cache reasoning inference-serving compression 基础模型 推理压缩：权重、KV 缓存与服务带宽 Random Attention为什么保护完整prompt，却在生成轨迹中逐头独立随机保留？ 任务说明与原始证据留在prompt中，保护它们避免随机删除改变任务条件；生成轨迹按头独立采样，省去重要性评分并让各头拥有不同覆盖。预算必须容纳受保护部分，随机策略仍可能漏掉关键中间步骤；本地GPU重建验证不代表完整任务矩阵与内核吞吐。 例如几个注意力头保留不同的中间推理片段，仍都能读取原问题；若把题干也随意删去，就不再是在同一输入条件下比较淘汰策略。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-random-attention-6364631b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-11ce14334bb11855">Random Attention为什么保护完整prompt，却在生成轨迹中逐头独立随机保留？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Arandom-attention">Random Attention: Rethinking KV Cache Eviction for Efficient Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Salesforce AI Research / University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>任务说明与原始证据留在prompt中，保护它们避免随机删除改变任务条件；生成轨迹按头独立采样，省去重要性评分并让各头拥有不同覆盖。预算必须容纳受保护部分，随机策略仍可能漏掉关键中间步骤；本地GPU重建验证不代表完整任务矩阵与内核吞吐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如几个注意力头保留不同的中间推理片段，仍都能读取原问题；若把题干也随意删去，就不再是在同一输入条件下比较淘汰策略。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.03430">原论文</a> · <a href="../../../../reproductions/2609.03430-random-attention/">实现解读</a> · <a href="#qa-11ce14334bb11855">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:twinkv" data-paper-title="TwinKV: A Composable Repair Pass for KV Cache Eviction via Pairwise Key Redundancy" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="TwinKV: A Composable Repair Pass for KV Cache Eviction via Pairwise Key Redundancy 基础模型 The Hong Kong University of Science and Technology (Guangzhou) 2026-08-27 现有 KV eviction 常按 token 重要性选择缓存，但可能同时保留多个几乎重复的 key，并删掉没有替代者的 orphan。TwinKV 不替代 StreamingLLM、H2O 等基础策略，而是一个可组合 repair pass：在完全不增加 KV budget 的前提下，找出“被删且没有相似保留项”的 orphan，与“已保留但有高度相似 twin”的 donor 成对交换。 复现级别：核心机制 + 真实 checkpoint KV 验证。复现级别：核心机制 + 真实 checkpoint KV 验证。Equation 4、等预算 swap 与 Qwen3 实际 KV tensor 均执行；没有把 attention reconstruction 指标写成完整 LongBench 分数。正式 GPU smoke 使用 Qwen3 的真实 K/V 和公开 WikiText-2 长上下文，评测三个代表层的 attention reconstruction；它不是完整 LongBench generation。  kv-cache long-context inference-serving compression 基础模型 推理压缩：权重、KV 缓存与服务带宽 TwinKV为什么交换冗余donor与缺少替代者的orphan，而不直接扩大KV预算？ 基础淘汰可能留下多个相似键，却删掉唯一证据。修复先识别被删且无相似保留项的孤立项，再用有远处相似副本的冗余保留项交换，预算保持不变；受保护的起始与近期项不能作供体。键相似也不保证语义等价，本地重建评测不代表完整生成结果。 例如缓存保留两段近似重复说明，却漏掉唯一日期，可拿冗余项换回日期；不能一边加回孤立项一边不删除任何项，再声称相同预算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-twinkv-b8f534bd" class="ar-learning-paper-anchor"></span>
<h2 id="qa-3a498fa6937cd63c">TwinKV为什么交换冗余donor与缺少替代者的orphan，而不直接扩大KV预算？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atwinkv">TwinKV: A Composable Repair Pass for KV Cache Eviction via Pairwise Key Redundancy</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hong Kong University of Science and Technology (Guangzhou)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>基础淘汰可能留下多个相似键，却删掉唯一证据。修复先识别被删且无相似保留项的孤立项，再用有远处相似副本的冗余保留项交换，预算保持不变；受保护的起始与近期项不能作供体。键相似也不保证语义等价，本地重建评测不代表完整生成结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如缓存保留两段近似重复说明，却漏掉唯一日期，可拿冗余项换回日期；不能一边加回孤立项一边不删除任何项，再声称相同预算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27128">原论文</a> · <a href="../../../../reproductions/2608.27128-twinkv/">实现解读</a> · <a href="#qa-3a498fa6937cd63c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:distillcache" data-paper-title="DistillCache: KL-Guided Adaptive KV-Cache Eviction for Memory-Efficient LLM Inference" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="DistillCache: KL-Guided Adaptive KV-Cache Eviction for Memory-Efficient LLM Inference 基础模型 Oklahoma State University 2026-08-09 把 KV 淘汰视为序列决策，以逐步 KL 奖励训练轻量策略保留未来预测分布。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 distillcache；单 seed 变化为 +92.19% 个百分点。  推理与系统效率 KV cache 基础模型 推理压缩：权重、KV 缓存与服务带宽 DistillCache为什么用完整缓存与淘汰缓存的预测KL作奖励，而不直接奖励多删token？ 缓存目标是保留后续预测所需信息，多删token只是资源动作。逐步比较完整缓存与淘汰后的分布，让策略看到某次淘汰损伤了多少行为，并在预算下学习取舍。训练用完整路径作参照，不代表部署每步都能免费运行它；低KL也不自动等于所有下游任务都无损。 教学例子：删去格式填充和删去关键编号都省一个KV，但后者可能显著改变下一步分布；分布奖励能区分这两种动作，而简单计数奖励会同样鼓励它们。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-distillcache-374f7173" class="ar-learning-paper-anchor"></span>
<h2 id="qa-58b3581acbd44eb8">DistillCache为什么用完整缓存与淘汰缓存的预测KL作奖励，而不直接奖励多删token？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adistillcache">DistillCache: KL-Guided Adaptive KV-Cache Eviction for Memory-Efficient LLM Inference</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Oklahoma State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>缓存目标是保留后续预测所需信息，多删token只是资源动作。逐步比较完整缓存与淘汰后的分布，让策略看到某次淘汰损伤了多少行为，并在预算下学习取舍。训练用完整路径作参照，不代表部署每步都能免费运行它；低KL也不自动等于所有下游任务都无损。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>删去格式填充和删去关键编号都省一个KV，但后者可能显著改变下一步分布；分布奖励能区分这两种动作，而简单计数奖励会同样鼓励它们。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.08878">原论文</a> · <a href="../../../../reproductions/2608.08878-distillcache/">实现解读</a> · <a href="#qa-58b3581acbd44eb8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:bakron" data-paper-title="BaKron: Efficient Quantization with Kronecker-Factored Hessians" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="BaKron: Efficient Quantization with Kronecker-Factored Hessians 基础模型 University of California, San Diego 2026-08-06 主题：二阶量化。GPTQ 通常只利用输入侧曲率；双侧 Kronecker Hessian 更丰富但直接向量化求解昂贵。BaKron 以反对角并行和递归分治实现双侧自适应 rounding。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。对随机权重执行 Kronecker 加权 4-bit rounding 与逐行尺度搜索，和全局 GPTQ-style rounding 比较加权误差。  quantization hessian inference-efficiency 基础模型 推理压缩：权重、KV 缓存与服务带宽 BaKron为何引入双侧Kronecker曲率，而不只考虑输入激活侧误差？ 权重量化误差不仅受输入方向影响，也受输出侧的曲率结构影响；Kronecker近似把两侧关联纳入同一二次目标。直接展开完整大Hessian代价高，因此方法用结构化的并行与分治组织舍入。更丰富的误差模型不代表可以忽略近似假设或把每个权重独立round当作同一算法。 教学例子：两个输入方向误差相同，但输出方向对最终loss的敏感程度不同；只看输入侧可能把它们视为等价，双侧曲率则能区分这种影响。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-bakron-8758065a" class="ar-learning-paper-anchor"></span>
<h2 id="qa-cb4b0da0ce3093eb">BaKron为何引入双侧Kronecker曲率，而不只考虑输入激活侧误差？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Abakron">BaKron: Efficient Quantization with Kronecker-Factored Hessians</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>权重量化误差不仅受输入方向影响，也受输出侧的曲率结构影响；Kronecker近似把两侧关联纳入同一二次目标。直接展开完整大Hessian代价高，因此方法用结构化的并行与分治组织舍入。更丰富的误差模型不代表可以忽略近似假设或把每个权重独立round当作同一算法。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个输入方向误差相同，但输出方向对最终loss的敏感程度不同；只看输入侧可能把它们视为等价，双侧曲率则能区分这种影响。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06291">原论文</a> · <a href="../../../../reproductions/2608.06291-bakron/">实现解读</a> · <a href="#qa-cb4b0da0ce3093eb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:qevict" data-paper-title="QEvict: Recoverable Quantized KV Eviction for Attention-Drift-Robust Long-Context Decoding" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="QEvict: Recoverable Quantized KV Eviction for Attention-Drift-Robust Long-Context Decoding 基础模型 Indian Institute of Technology Roorkee 2026-08-05 主题：长上下文 KV cache。二元保留/删除无法应对注意力漂移：今天不重要的窗口可能稍后重新活跃。QEvict 设置全精度、量化可恢复、删除三层，累计注意力变化时可将窗口解量化晋升。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。在固定槽位预算的向量 attention 流上执行三层缓存、量化恢复与晋升，比较不可恢复 eviction recall。  long-context kv-cache quantization serving 基础模型 推理压缩：权重、KV 缓存与服务带宽 QEvict为什么在全精度与删除之间增加可恢复量化层？ 长生成中注意力会漂移，当前不重要的窗口以后可能重新相关。量化层用较小存储保留可恢复内容，累计注意力升高时可解量化晋升；彻底删除则失去这种机会。恢复只能挽回保留近似信息，不能消除既有量化误差，本地状态验证不等于完整服务性能复现。 例如前文人物线索暂时不用，先降到量化层；后续再次提问时可恢复参与注意，若先彻底删除，就只能另行重算或检索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-qevict-bcd29a04" class="ar-learning-paper-anchor"></span>
<h2 id="qa-6e5f2217749ab819">QEvict为什么在全精度与删除之间增加可恢复量化层？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aqevict">QEvict: Recoverable Quantized KV Eviction for Attention-Drift-Robust Long-Context Decoding</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Indian Institute of Technology Roorkee</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长生成中注意力会漂移，当前不重要的窗口以后可能重新相关。量化层用较小存储保留可恢复内容，累计注意力升高时可解量化晋升；彻底删除则失去这种机会。恢复只能挽回保留近似信息，不能消除既有量化误差，本地状态验证不等于完整服务性能复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如前文人物线索暂时不用，先降到量化层；后续再次提问时可恢复参与注意，若先彻底删除，就只能另行重算或检索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05326">原论文</a> · <a href="../../../../reproductions/2608.05326-qevict/">实现解读</a> · <a href="#qa-6e5f2217749ab819">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:taskpress" data-paper-title="TaskPress: Query-Agnostic KV Cache Compression via Task-Guided Pruning" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="TaskPress: Query-Agnostic KV Cache Compression via Task-Guided Pruning 基础模型 Google 2026-08-04 固定v2 Section3 Eqs1–3：sum over guide→odd-K零padding平均池化；γ=max|v|/(2^(b−1)−1)，scores=keyimportance×γ，各head同budget独立topk。输入显式是task-to-context sliced attention，不看真实下游query；真实K/V按时间排序gather，guideKV不保留，原position不能重编号。K/GQA聚合由调用方显式给出，tie按低index为本地约定。 成本过高，不复现（审查 DONE）。Llama3.1-8B/Qwen3-8B/32B，LongBench/RULER16K至64K上下文多压缩比例/方法矩阵；guide演化单A10040GB原文约25.2min加Gemini调用，完整多任务矩阵更大。只做算子，不跑全量加载/演化、无速度计时复现。taskpress_scores消费task-to-context attention与既有per-token value_scale；symmetric_value_scale是显式浮点数值参考，不是假装已运行int4 kernel。  推理与系统效率 KV缓存压缩 基础模型 推理压缩：权重、KV 缓存与服务带宽 TaskPress宣称不看下游query，为什么仍需要task guide对context的注意力？ 任务级引导提供可复用的压缩偏好，选择器只读引导到上下文的注意力并结合值的量化尺度，不能借实际未来查询定制缓存。引导自身KV随后丢弃，保留历史的位置编号。真实引导生成与多任务效果不由小张量选择核证明，完整配置本地因成本过高未复现。 例如同一摘要任务可用通用引导压缩多段材料，未来具体提问尚未给出；若先读真实问题再挑证据，就不再是查询无关压缩。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-taskpress-8d6c3897" class="ar-learning-paper-anchor"></span>
<h2 id="qa-e794d7481f5d8483">TaskPress宣称不看下游query，为什么仍需要task guide对context的注意力？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ataskpress">TaskPress: Query-Agnostic KV Cache Compression via Task-Guided Pruning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>任务级引导提供可复用的压缩偏好，选择器只读引导到上下文的注意力并结合值的量化尺度，不能借实际未来查询定制缓存。引导自身KV随后丢弃，保留历史的位置编号。真实引导生成与多任务效果不由小张量选择核证明，完整配置本地因成本过高未复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一摘要任务可用通用引导压缩多段材料，未来具体提问尚未给出；若先读真实问题再挑证据，就不再是查询无关压缩。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03276v1">原论文</a> · <a href="../../../../foundation-models/2608.03276-taskpress/">实现解读</a> · <a href="#qa-e794d7481f5d8483">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:c2kv" data-paper-title="C²KV: Compressed and Composable KV Cache Reuse for Efficient LLM Inference" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="C²KV: Compressed and Composable KV Cache Reuse for Efficient LLM Inference 基础模型 Shanghai Jiao Tong University 2026-07-20 以 compression tokens 和结构化 attention 学习位置无关、可拼接的压缩 KV manifold，并联合训练压缩与复用。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 recent-window attention，实验组为 c2kv；单 seed 变化为 +76.56% 个百分点。  推理与系统效率 KV cache 基础模型 推理压缩：权重、KV 缓存与服务带宽 C²KV为何同时学习压缩与拼接复用，而不是先压短缓存再任意组合？ 独立压缩后的KV可能依赖原位置和原上下文，拼起来未必仍能被模型正确读取。方法通过compression tokens及结构化attention学习更可组合的压缩表示，让多个片段的复用也进入训练目标。压缩表示仍有信息损失与接口条件，不能把任意摘要都视为位置无关的可拼接缓存。 教学例子：分别压缩两份文档后，要在同一请求中一起使用；训练需让模型理解两个压缩片段如何共同提供证据，而不只保证各片段单独重构时看起来合理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-c2kv-5a6eab64" class="ar-learning-paper-anchor"></span>
<h2 id="qa-325fef9068a4285a">C²KV为何同时学习压缩与拼接复用，而不是先压短缓存再任意组合？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ac2kv">C²KV: Compressed and Composable KV Cache Reuse for Efficient LLM Inference</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Jiao Tong University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立压缩后的KV可能依赖原位置和原上下文，拼起来未必仍能被模型正确读取。方法通过compression tokens及结构化attention学习更可组合的压缩表示，让多个片段的复用也进入训练目标。压缩表示仍有信息损失与接口条件，不能把任意摘要都视为位置无关的可拼接缓存。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>分别压缩两份文档后，要在同一请求中一起使用；训练需让模型理解两个压缩片段如何共同提供证据，而不只保证各片段单独重构时看起来合理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.17715">原论文</a> · <a href="../../../../reproductions/2607.17715-c2kv/">实现解读</a> · <a href="#qa-325fef9068a4285a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:awq" data-paper-title="AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration 基础模型 MIT / NVIDIA / Harvard / SJTU 2023-06-01 利用 calibration activation 找到显著输入通道，通过等价通道缩放保护约 1% 关键权重，再执行硬件友好的统一低比特 weight-only 量化。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。用 WikiText-2 激活统计搜索 AWQ 等价缩放并真实执行 W4 量化；未使用 TinyChat CUDA kernel，MSE 不代表端到端吞吐。本地相对变化不得与原文指标混写。本地对照口径：基线为 round-to-nearest W4，实验组为 activation-aware equivalent scaling W4，只改变论文核心机制；output_mse 0.0054 → 0.0052，相对基线 -4.22%。  inference-serving quantization 基础模型 推理压缩：权重、KV 缓存与服务带宽 AWQ保护关键通道时，为何先做等价缩放，而不是给少量权重单独存更高精度？ 校准激活帮助识别对输出更敏感的输入通道，再对输入和权重作相互抵消的通道缩放，使关键权重在统一低比特码本中更易保真。浮点函数保持等价，量化误差却随缩放改变。保护对象由激活重要性指引，并不意味着所有大权重天然重要，也不自动解决动态KV缓存增长。 教学例子：两个权重数值相近，但一条输入通道经常幅度很大，它的误差对输出更显著；合法缩放可优先降低这条通道的量化影响，同时仍使用统一低比特格式。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-awq-9367c7ce" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d1ecb6d714c57abd">AWQ保护关键通道时，为何先做等价缩放，而不是给少量权重单独存更高精度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aawq">AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · MIT / NVIDIA / Harvard / SJTU</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>校准激活帮助识别对输出更敏感的输入通道，再对输入和权重作相互抵消的通道缩放，使关键权重在统一低比特码本中更易保真。浮点函数保持等价，量化误差却随缩放改变。保护对象由激活重要性指引，并不意味着所有大权重天然重要，也不自动解决动态KV缓存增长。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个权重数值相近，但一条输入通道经常幅度很大，它的误差对输出更显著；合法缩放可优先降低这条通道的量化影响，同时仍使用统一低比特格式。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2306.00978">原论文</a> · <a href="../../../../reproductions/2306.00978-awq/">实现解读</a> · <a href="#qa-d1ecb6d714c57abd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gqa" data-paper-title="GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/compression-and-cache" data-search="GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints 基础模型 Google Research 2023-05-22 多个 query head 共享较少的 K/V head，在 MHA 质量与 MQA 解码带宽之间取得可控折中。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际让 4 个 query heads 分组共享 2 个 K/V heads，并报告 KV cache 缩减；从头小模型训练替代论文从 MHA checkpoint 的 5% compute uptraining。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为同预算 llama_modern，实验组为 gqa；相对 PPL +2.15%。  attention kv-cache serving architecture 基础模型 推理压缩：权重、KV 缓存与服务带宽 GQA减少的是query head还是KV head，为什么这主要影响解码缓存与带宽？ 多个query head共享较少的key/value head，查询仍可保留多组投影和读取偏好。每个历史位置需要存的KV头数因此减少，逐步解码要读取的状态也相应变少。共享会约束不同头的独立性，形成MHA与更强共享之间的折中；它不是直接把历史token数量缩短。 教学例子：8个query head按组共享2个KV head，历史每个位置只存2组K/V，而不是8组；但8个查询仍可对共享的内容产生不同注意力权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 推理压缩：权重、KV 缓存与服务带宽</a></p>
<span id="paper-foundation-models-gqa-9496fcce" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b644d6aec39b7b8b">GQA减少的是query head还是KV head，为什么这主要影响解码缓存与带宽？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agqa">GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多个query head共享较少的key/value head，查询仍可保留多组投影和读取偏好。每个历史位置需要存的KV头数因此减少，逐步解码要读取的状态也相应变少。共享会约束不同头的独立性，形成MHA与更强共享之间的折中；它不是直接把历史token数量缩短。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>8个query head按组共享2个KV head，历史每个位置只存2组K/V，而不是8组；但8个查询仍可对共享的内容产生不同注意力权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.13245">原论文</a> · <a href="../../../../reproductions/2305.13245-gqa/">实现解读</a> · <a href="#qa-b644d6aec39b7b8b">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

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

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
