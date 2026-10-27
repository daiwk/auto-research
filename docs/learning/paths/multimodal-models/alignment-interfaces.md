---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 跨模态对齐：表征、连接器与监督

[多模态](index.md) / 80 个问题 · 20 篇论文

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
<p class="ar-learning-status" data-learning-status role="status">80 个问题 · 20 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:flexglue" data-paper-title="FlexGlue: Sparse-to-Dense Feature Matching and Visual Disambiguation" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="FlexGlue: Sparse-to-Dense Feature Matching and Visual Disambiguation 多模态大模型 ETH Zurich 2026-10-23 稀疏matcher受两图keypoint重复检测能力限制，dense matcher则昂贵，而且两者常只在共视正样本训练，面对对称建筑等doppelganger会给出高置信假匹配。FlexGlue在stride8全图token网格上先做self/cross attention，再只对给定query插值读取特征并寻找另一图的坐标。局部3×3窗口读取避免全局期望在多个候选间平均；轻量MLP对两个方向的offset bins取期望做局部细化。共视分支给每个token一个sigmoid vote，并在每层监督； 成本过高，不复现（审查 DONE）。原文第7页：冻结DINOv3 ConvNeXt-B、9层512维Transformer、8数据集、512×512图像，50epochs、每epoch150K样本，在4张H200上约4 GPU-days；gradient checkpointing后4张RTX4090约1.5天，另有10epoch消歧fine-tune与多数据集/重建评测。这里保持作者的GPU-days口径，不虚构单卡总时长。本轮没有operator、local command、metrics或GPU收据，gpu_validation_passed=false。保留作者仓库作为可查来源；  多模态表征 视觉匹配与几何 多模态 跨模态对齐：表征、连接器与监督 FlexGlue 的稠密网格为什么仍能处理任意位置的匹配查询？ 模型先在 stride-8 特征网格上进行全局交互，再把指定查询插值到网格特征中，通过跨图注意力读取另一图坐标。查询不必恰好位于某个固定 cell 中心，因此可在稠密表示上支持连续位置匹配，而非只返回固定关键点集合。 例如查询落在四个网格点之间，可先插值得到其特征，再到另一张图读取对应位置，而无需把它硬移到最近格点。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<span id="paper-multimodal-models-flexglue-0459516f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2e891739cff8d495">FlexGlue 的稠密网格为什么仍能处理任意位置的匹配查询？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Aflexglue">FlexGlue: Sparse-to-Dense Feature Matching and Visual Disambiguation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ETH Zurich</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>模型先在 stride-8 特征网格上进行全局交互，再把指定查询插值到网格特征中，通过跨图注意力读取另一图坐标。查询不必恰好位于某个固定 cell 中心，因此可在稠密表示上支持连续位置匹配，而非只返回固定关键点集合。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如查询落在四个网格点之间，可先插值得到其特征，再到另一张图读取对应位置，而无需把它硬移到最近格点。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32976v1">原论文</a> · <a href="../../../../multimodal-models/2610.32976-flexglue/">实现解读</a> · <a href="#qa-2e891739cff8d495">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:flexglue" data-paper-title="FlexGlue: Sparse-to-Dense Feature Matching and Visual Disambiguation" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="FlexGlue: Sparse-to-Dense Feature Matching and Visual Disambiguation 多模态大模型 ETH Zurich 2026-10-23 稀疏matcher受两图keypoint重复检测能力限制，dense matcher则昂贵，而且两者常只在共视正样本训练，面对对称建筑等doppelganger会给出高置信假匹配。FlexGlue在stride8全图token网格上先做self/cross attention，再只对给定query插值读取特征并寻找另一图的坐标。局部3×3窗口读取避免全局期望在多个候选间平均；轻量MLP对两个方向的offset bins取期望做局部细化。共视分支给每个token一个sigmoid vote，并在每层监督； 成本过高，不复现（审查 DONE）。原文第7页：冻结DINOv3 ConvNeXt-B、9层512维Transformer、8数据集、512×512图像，50epochs、每epoch150K样本，在4张H200上约4 GPU-days；gradient checkpointing后4张RTX4090约1.5天，另有10epoch消歧fine-tune与多数据集/重建评测。这里保持作者的GPU-days口径，不虚构单卡总时长。本轮没有operator、local command、metrics或GPU收据，gpu_validation_passed=false。保留作者仓库作为可查来源；  多模态表征 视觉匹配与几何 多模态 跨模态对齐：表征、连接器与监督 FlexGlue 为什么只在峰值附近的局部窗口读坐标，而不对全图坐标求期望？ 若相似建筑在两处形成峰值，全局期望可能落在二者中间的错误位置。局部窗口围绕最强候选计算坐标，减少多峰平均；随后细化位移，而共视投票与困难负例负责判断两图是否真的可匹配。高相似度本身不能替代共视验证。 例如左右两扇相同窗户都得高分，全图平均会落在墙上；围绕被选窗户做局部读取才有合理初始坐标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c8472fbb022dc303">FlexGlue 为什么只在峰值附近的局部窗口读坐标，而不对全图坐标求期望？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Aflexglue">FlexGlue: Sparse-to-Dense Feature Matching and Visual Disambiguation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ETH Zurich</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若相似建筑在两处形成峰值，全局期望可能落在二者中间的错误位置。局部窗口围绕最强候选计算坐标，减少多峰平均；随后细化位移，而共视投票与困难负例负责判断两图是否真的可匹配。高相似度本身不能替代共视验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如左右两扇相同窗户都得高分，全图平均会落在墙上；围绕被选窗户做局部读取才有合理初始坐标。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32976v1">原论文</a> · <a href="../../../../multimodal-models/2610.32976-flexglue/">实现解读</a> · <a href="#qa-c8472fbb022dc303">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:flexglue" data-paper-title="FlexGlue: Sparse-to-Dense Feature Matching and Visual Disambiguation" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="FlexGlue: Sparse-to-Dense Feature Matching and Visual Disambiguation 多模态大模型 ETH Zurich 2026-10-23 稀疏matcher受两图keypoint重复检测能力限制，dense matcher则昂贵，而且两者常只在共视正样本训练，面对对称建筑等doppelganger会给出高置信假匹配。FlexGlue在stride8全图token网格上先做self/cross attention，再只对给定query插值读取特征并寻找另一图的坐标。局部3×3窗口读取避免全局期望在多个候选间平均；轻量MLP对两个方向的offset bins取期望做局部细化。共视分支给每个token一个sigmoid vote，并在每层监督； 成本过高，不复现（审查 DONE）。原文第7页：冻结DINOv3 ConvNeXt-B、9层512维Transformer、8数据集、512×512图像，50epochs、每epoch150K样本，在4张H200上约4 GPU-days；gradient checkpointing后4张RTX4090约1.5天，另有10epoch消歧fine-tune与多数据集/重建评测。这里保持作者的GPU-days口径，不虚构单卡总时长。本轮没有operator、local command、metrics或GPU收据，gpu_validation_passed=false。保留作者仓库作为可查来源；  多模态表征 视觉匹配与几何 多模态 跨模态对齐：表征、连接器与监督 FlexGlue的逐层共视门控，与无论是否共视都跑满全部层相比，何时可以提前结束？ 共视分支在每层产生token级sigmoid vote，双图vote均值低于该层阈值tγ^(L−k)时提前退出。它检查两图是否值得继续匹配，而不是把最强局部匹配分数当共视证据；提前退出也依赖门控可靠，不能将少跑几层直接解释为匹配质量提高。 教学例子：两张对称建筑图片局部很像，但双图整体共视vote低，可在中间层退出，而不是继续细化一个高置信假匹配。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-55aa95e8e4472093">FlexGlue的逐层共视门控，与无论是否共视都跑满全部层相比，何时可以提前结束？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Aflexglue">FlexGlue: Sparse-to-Dense Feature Matching and Visual Disambiguation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ETH Zurich</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共视分支在每层产生token级sigmoid vote，双图vote均值低于该层阈值tγ^(L−k)时提前退出。它检查两图是否值得继续匹配，而不是把最强局部匹配分数当共视证据；提前退出也依赖门控可靠，不能将少跑几层直接解释为匹配质量提高。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两张对称建筑图片局部很像，但双图整体共视vote低，可在中间层退出，而不是继续细化一个高置信假匹配。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32976v1">原论文</a> · <a href="../../../../multimodal-models/2610.32976-flexglue/">实现解读</a> · <a href="#qa-55aa95e8e4472093">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:flexglue" data-paper-title="FlexGlue: Sparse-to-Dense Feature Matching and Visual Disambiguation" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="FlexGlue: Sparse-to-Dense Feature Matching and Visual Disambiguation 多模态大模型 ETH Zurich 2026-10-23 稀疏matcher受两图keypoint重复检测能力限制，dense matcher则昂贵，而且两者常只在共视正样本训练，面对对称建筑等doppelganger会给出高置信假匹配。FlexGlue在stride8全图token网格上先做self/cross attention，再只对给定query插值读取特征并寻找另一图的坐标。局部3×3窗口读取避免全局期望在多个候选间平均；轻量MLP对两个方向的offset bins取期望做局部细化。共视分支给每个token一个sigmoid vote，并在每层监督； 成本过高，不复现（审查 DONE）。原文第7页：冻结DINOv3 ConvNeXt-B、9层512维Transformer、8数据集、512×512图像，50epochs、每epoch150K样本，在4张H200上约4 GPU-days；gradient checkpointing后4张RTX4090约1.5天，另有10epoch消歧fine-tune与多数据集/重建评测。这里保持作者的GPU-days口径，不虚构单卡总时长。本轮没有operator、local command、metrics或GPU收据，gpu_validation_passed=false。保留作者仓库作为可查来源；  多模态表征 视觉匹配与几何 多模态 跨模态对齐：表征、连接器与监督 用普通 softmax 加交叉熵就能称为 FlexGlue 的实际粗匹配实现吗？ 不能。正文明确实际使用 1.5-entmax 与 Fenchel–Young loss；粗标签是亚像素坐标周围四个 cell 的双线性权重，细化时对粗坐标停止梯度。当前本地没有完整 operator、训练指标或 GPU 收据，不能把通用 softmax 演示当作复现。 例如真值在四格交界处应分配四个权重，若强行选最近格点作为 one-hot，监督目标已经不同于论文。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a4c29d72335d48b2">用普通 softmax 加交叉熵就能称为 FlexGlue 的实际粗匹配实现吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Aflexglue">FlexGlue: Sparse-to-Dense Feature Matching and Visual Disambiguation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ETH Zurich</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。正文明确实际使用 1.5-entmax 与 Fenchel–Young loss；粗标签是亚像素坐标周围四个 cell 的双线性权重，细化时对粗坐标停止梯度。当前本地没有完整 operator、训练指标或 GPU 收据，不能把通用 softmax 演示当作复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如真值在四格交界处应分配四个权重，若强行选最近格点作为 one-hot，监督目标已经不同于论文。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32976v1">原论文</a> · <a href="../../../../multimodal-models/2610.32976-flexglue/">实现解读</a> · <a href="#qa-a4c29d72335d48b2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:lamp" data-paper-title="LAMP: Layerwise Adaptive Mixing of Predictors for Training-Free Few-Shot Vision-Language Adaptation" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="LAMP: Layerwise Adaptive Mixing of Predictors for Training-Free Few-Shot Vision-Language Adaptation 基础模型 Taizhou Institute of Science and Technology, Nanjing University of Science and Technology 2026-10-15 冻结视觉编码器的中间层包含不同粒度的信息，但维度和相似性结构不同。LAMP不将它们投影到统一特征维度，而是分别拟合支持标签相对CLIP先验的残差，再在类别分数空间混合。区域核只以support bank校准；LAMP-F适配文本原型时，同步更新残差预测，避免原型改变而支持残差仍陈旧。 完整实验成本过高，不复现（审查 DONE）。测试标签在所有选择与一次原型更新完成后才用于最终诊断报告。固定recipe synthetic-fpot-and-native-layer-kernel-features@oct19-foundation-mechanisms-v1，seeds42/43/44。冻结三层小MLP编码4×4合成patch；三层区域宽度分别为5/7/9，全局宽度6。支持12视图、验证6样本、测试5样本具有不重叠身份，彼此独立生成；不是CLIP或公开图像benchmark。  多模态基础模型 冻结特征与少样本适配 多模态 跨模态对齐：表征、连接器与监督 LAMP 所拟合的标签残差是相对什么计算的？ 残差是支持集真实类别标签减去原始 CLIP 文本原型给出的类别分数。各层核预测器学习纠正这个已有先验，而非从零重复学习全部类别；因此先验原型改变后，支持集残差也应随之改变，否则修正项与被修正对象不再一致。 例如某支持图的真实类别向量为猫，但 CLIP 给猫的分数偏低，核分支学习的是补足这一差额，而非再训练图像编码器。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<span id="paper-foundation-models-lamp-52f612c4" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f533d9685d57ba72">LAMP 所拟合的标签残差是相对什么计算的？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alamp">LAMP: Layerwise Adaptive Mixing of Predictors for Training-Free Few-Shot Vision-Language Adaptation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taizhou Institute of Science and Technology, Nanjing University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>残差是支持集真实类别标签减去原始 CLIP 文本原型给出的类别分数。各层核预测器学习纠正这个已有先验，而非从零重复学习全部类别；因此先验原型改变后，支持集残差也应随之改变，否则修正项与被修正对象不再一致。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某支持图的真实类别向量为猫，但 CLIP 给猫的分数偏低，核分支学习的是补足这一差额，而非再训练图像编码器。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22182">原论文</a> · <a href="../../../../foundation-models/2610.22182-lamp/">实现解读</a> · <a href="#qa-f533d9685d57ba72">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:lamp" data-paper-title="LAMP: Layerwise Adaptive Mixing of Predictors for Training-Free Few-Shot Vision-Language Adaptation" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="LAMP: Layerwise Adaptive Mixing of Predictors for Training-Free Few-Shot Vision-Language Adaptation 基础模型 Taizhou Institute of Science and Technology, Nanjing University of Science and Technology 2026-10-15 冻结视觉编码器的中间层包含不同粒度的信息，但维度和相似性结构不同。LAMP不将它们投影到统一特征维度，而是分别拟合支持标签相对CLIP先验的残差，再在类别分数空间混合。区域核只以support bank校准；LAMP-F适配文本原型时，同步更新残差预测，避免原型改变而支持残差仍陈旧。 完整实验成本过高，不复现（审查 DONE）。测试标签在所有选择与一次原型更新完成后才用于最终诊断报告。固定recipe synthetic-fpot-and-native-layer-kernel-features@oct19-foundation-mechanisms-v1，seeds42/43/44。冻结三层小MLP编码4×4合成patch；三层区域宽度分别为5/7/9，全局宽度6。支持12视图、验证6样本、测试5样本具有不重叠身份，彼此独立生成；不是CLIP或公开图像benchmark。  多模态基础模型 冻结特征与少样本适配 多模态 跨模态对齐：表征、连接器与监督 LAMP 为什么在类别分数空间混合多层预测，而不先把各层特征拼起来？ 各层特征的维度与相似性结构不一致，强行统一会引入额外投影假设。LAMP 让每个分支根据支持集拟合相对 CLIP 先验的残差，再在共同的类别分数空间加权；若文本原型变化，残差也需同步更新，否则适配的是过时的错误方向。 例如浅层分支擅长纹理、深层擅长语义，二者都先给猫犬打分，再混合两份分数而非生硬拼接向量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-d272f3c9d6e7debd">LAMP 为什么在类别分数空间混合多层预测，而不先把各层特征拼起来？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alamp">LAMP: Layerwise Adaptive Mixing of Predictors for Training-Free Few-Shot Vision-Language Adaptation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taizhou Institute of Science and Technology, Nanjing University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>各层特征的维度与相似性结构不一致，强行统一会引入额外投影假设。LAMP 让每个分支根据支持集拟合相对 CLIP 先验的残差，再在共同的类别分数空间加权；若文本原型变化，残差也需同步更新，否则适配的是过时的错误方向。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如浅层分支擅长纹理、深层擅长语义，二者都先给猫犬打分，再混合两份分数而非生硬拼接向量。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22182">原论文</a> · <a href="../../../../foundation-models/2610.22182-lamp/">实现解读</a> · <a href="#qa-d272f3c9d6e7debd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:lamp" data-paper-title="LAMP: Layerwise Adaptive Mixing of Predictors for Training-Free Few-Shot Vision-Language Adaptation" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="LAMP: Layerwise Adaptive Mixing of Predictors for Training-Free Few-Shot Vision-Language Adaptation 基础模型 Taizhou Institute of Science and Technology, Nanjing University of Science and Technology 2026-10-15 冻结视觉编码器的中间层包含不同粒度的信息，但维度和相似性结构不同。LAMP不将它们投影到统一特征维度，而是分别拟合支持标签相对CLIP先验的残差，再在类别分数空间混合。区域核只以support bank校准；LAMP-F适配文本原型时，同步更新残差预测，避免原型改变而支持残差仍陈旧。 完整实验成本过高，不复现（审查 DONE）。测试标签在所有选择与一次原型更新完成后才用于最终诊断报告。固定recipe synthetic-fpot-and-native-layer-kernel-features@oct19-foundation-mechanisms-v1，seeds42/43/44。冻结三层小MLP编码4×4合成patch；三层区域宽度分别为5/7/9，全局宽度6。支持12视图、验证6样本、测试5样本具有不重叠身份，彼此独立生成；不是CLIP或公开图像benchmark。  多模态基础模型 冻结特征与少样本适配 多模态 跨模态对齐：表征、连接器与监督 LAMP用support bank校准区域核，与把待评query一起放进均值统计有何区别？ 校准中的m(x)和b都以支持集为统计基准，query只按这套固定基准计算核值。把待评query或测试批混入统计，会让同一查询的结果依赖同时评估哪些样本，改变原合同；它也不能借此读取测试标签选择混合权重。 教学例子：固定支持集后单独评甲与批量评甲乙，甲应沿用同一校准基准；不能因为乙加入而重定义支持集均值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7084f5f48e922c1a">LAMP用support bank校准区域核，与把待评query一起放进均值统计有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alamp">LAMP: Layerwise Adaptive Mixing of Predictors for Training-Free Few-Shot Vision-Language Adaptation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taizhou Institute of Science and Technology, Nanjing University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>校准中的m(x)和b都以支持集为统计基准，query只按这套固定基准计算核值。把待评query或测试批混入统计，会让同一查询的结果依赖同时评估哪些样本，改变原合同；它也不能借此读取测试标签选择混合权重。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>固定支持集后单独评甲与批量评甲乙，甲应沿用同一校准基准；不能因为乙加入而重定义支持集均值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22182">原论文</a> · <a href="../../../../foundation-models/2610.22182-lamp/">实现解读</a> · <a href="#qa-7084f5f48e922c1a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:lamp" data-paper-title="LAMP: Layerwise Adaptive Mixing of Predictors for Training-Free Few-Shot Vision-Language Adaptation" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="LAMP: Layerwise Adaptive Mixing of Predictors for Training-Free Few-Shot Vision-Language Adaptation 基础模型 Taizhou Institute of Science and Technology, Nanjing University of Science and Technology 2026-10-15 冻结视觉编码器的中间层包含不同粒度的信息，但维度和相似性结构不同。LAMP不将它们投影到统一特征维度，而是分别拟合支持标签相对CLIP先验的残差，再在类别分数空间混合。区域核只以support bank校准；LAMP-F适配文本原型时，同步更新残差预测，避免原型改变而支持残差仍陈旧。 完整实验成本过高，不复现（审查 DONE）。测试标签在所有选择与一次原型更新完成后才用于最终诊断报告。固定recipe synthetic-fpot-and-native-layer-kernel-features@oct19-foundation-mechanisms-v1，seeds42/43/44。冻结三层小MLP编码4×4合成patch；三层区域宽度分别为5/7/9，全局宽度6。支持12视图、验证6样本、测试5样本具有不重叠身份，彼此独立生成；不是CLIP或公开图像benchmark。  多模态基础模型 冻结特征与少样本适配 多模态 跨模态对齐：表征、连接器与监督 LAMP-F 更新文本原型时，为什么 cached response 要随之修正？ 原型更新同时影响 query 的先验分数与 support 的残差。缓存的线性响应刻画核解对原型变化的影响，可精确更新结果而不重新完整求解；只改 query 先验、沿用旧支持残差会遗漏一项。核统计与混合权重在该阶段保持冻结。 例如文本原型向猫图方向移动，支持猫图的先验也上升，其待补残差应减小；若只提高查询分数就会重复补偿。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-35cf268cc640f6cd">LAMP-F 更新文本原型时，为什么 cached response 要随之修正？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alamp">LAMP: Layerwise Adaptive Mixing of Predictors for Training-Free Few-Shot Vision-Language Adaptation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Taizhou Institute of Science and Technology, Nanjing University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原型更新同时影响 query 的先验分数与 support 的残差。缓存的线性响应刻画核解对原型变化的影响，可精确更新结果而不重新完整求解；只改 query 先验、沿用旧支持残差会遗漏一项。核统计与混合权重在该阶段保持冻结。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如文本原型向猫图方向移动，支持猫图的先验也上升，其待补残差应减小；若只提高查询分数就会重复补偿。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、代码映射与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22182">原论文</a> · <a href="../../../../foundation-models/2610.22182-lamp/">实现解读</a> · <a href="#qa-35cf268cc640f6cd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:cv-opd" data-paper-title="CV-OPD: Contrastive Vision On-policy Distillation" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="CV-OPD: Contrastive Vision On-policy Distillation 多模态大模型 Xiamen University / Moxin Technology 2026-10-09 原来的 crop-to-full-image OPD 可以教会模型答案分布，却不必然教会它依赖正确视觉区域。作者在移除答案相关区域后发现，Vision-OPD 仍取得明显高于随机的准确率。CV-OPD 用同图、同尺寸、低 IoU 的负区域构造第二个共享参数教师，把“接近正教师、远离负教师”的约束加入 JSD 蒸馏。三个不可省略的约束是：正负教师只改变 crop、读取同一学生前缀；CDL 使用有界 JSD 的 margin； 当前实现为 core_mechanism / L1 核心机制诊断，真实 VLM 更新而非图像分类打分代理。cpu-contracts.json记录已重跑的 7 个行为测试：bbox 尺寸与 IoU、JSD/Top-K tail、样本与 token gate、教师停止梯度和零正确样本的零梯度，以及严格多类 verifier、标签隔离和图像来源/切分哈希。每项先固定 seed 42，专用 crop/gate 用例内部使用 seed 2；这些是单测用例，不是独立多 seed 能力实验。测试通过不代表视觉推理能力或 GPU 训练完成。  视觉证据对齐 On-policy distillation 多模态 跨模态对齐：表征、连接器与监督 CV-OPD 为什么要给同一张图准备正 crop 与负 crop？ 正区域提供回答所需的局部证据，负区域在同图、同尺寸、低重叠条件下提供视觉反事实。学生读完整图像，教师只改变看到的区域；这样可以检查学生是否接近正确证据下的分布，并区别于依靠语言先验也能答对的情况。 例如问路牌文字，正 crop 包含路牌、负 crop 只含相邻墙面；两位教师共享参数，使主要变化来自视觉输入。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<span id="paper-multimodal-models-cv-opd-6105b27e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7fbea63986417aa5">CV-OPD 为什么要给同一张图准备正 crop 与负 crop？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Acv-opd">CV-OPD: Contrastive Vision On-policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiamen University / Moxin Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>正区域提供回答所需的局部证据，负区域在同图、同尺寸、低重叠条件下提供视觉反事实。学生读完整图像，教师只改变看到的区域；这样可以检查学生是否接近正确证据下的分布，并区别于依靠语言先验也能答对的情况。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如问路牌文字，正 crop 包含路牌、负 crop 只含相邻墙面；两位教师共享参数，使主要变化来自视觉输入。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13264">原论文</a> · <a href="../../../../reproductions/2610.13264-cv-opd/">实现解读</a> · <a href="#qa-7fbea63986417aa5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:cv-opd" data-paper-title="CV-OPD: Contrastive Vision On-policy Distillation" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="CV-OPD: Contrastive Vision On-policy Distillation 多模态大模型 Xiamen University / Moxin Technology 2026-10-09 原来的 crop-to-full-image OPD 可以教会模型答案分布，却不必然教会它依赖正确视觉区域。作者在移除答案相关区域后发现，Vision-OPD 仍取得明显高于随机的准确率。CV-OPD 用同图、同尺寸、低 IoU 的负区域构造第二个共享参数教师，把“接近正教师、远离负教师”的约束加入 JSD 蒸馏。三个不可省略的约束是：正负教师只改变 crop、读取同一学生前缀；CDL 使用有界 JSD 的 margin； 当前实现为 core_mechanism / L1 核心机制诊断，真实 VLM 更新而非图像分类打分代理。cpu-contracts.json记录已重跑的 7 个行为测试：bbox 尺寸与 IoU、JSD/Top-K tail、样本与 token gate、教师停止梯度和零正确样本的零梯度，以及严格多类 verifier、标签隔离和图像来源/切分哈希。每项先固定 seed 42，专用 crop/gate 用例内部使用 seed 2；这些是单测用例，不是独立多 seed 能力实验。测试通过不代表视觉推理能力或 GPU 训练完成。  视觉证据对齐 On-policy distillation 多模态 跨模态对齐：表征、连接器与监督 CV-OPD 为什么要求正负教师看同一学生前缀，只改变视觉 crop？ 这样正负教师分布的差别才能主要归因于可见区域，而非文本历史变化。学生在自身 rollout 前缀上接近正确区域教师，同时通过有界 JSD margin 远离负区域教师；这补充了普通答案蒸馏可能只学语言先验、未学正确视觉依赖的问题。 例如问题问杯子颜色，正 crop 包含杯子，负 crop 是同尺寸背景；两位教师都接收学生已经生成的相同文字。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-be9768a40b798c69">CV-OPD 为什么要求正负教师看同一学生前缀，只改变视觉 crop？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Acv-opd">CV-OPD: Contrastive Vision On-policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiamen University / Moxin Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这样正负教师分布的差别才能主要归因于可见区域，而非文本历史变化。学生在自身 rollout 前缀上接近正确区域教师，同时通过有界 JSD margin 远离负区域教师；这补充了普通答案蒸馏可能只学语言先验、未学正确视觉依赖的问题。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如问题问杯子颜色，正 crop 包含杯子，负 crop 是同尺寸背景；两位教师都接收学生已经生成的相同文字。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13264">原论文</a> · <a href="../../../../reproductions/2610.13264-cv-opd/">实现解读</a> · <a href="#qa-be9768a40b798c69">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:cv-opd" data-paper-title="CV-OPD: Contrastive Vision On-policy Distillation" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="CV-OPD: Contrastive Vision On-policy Distillation 多模态大模型 Xiamen University / Moxin Technology 2026-10-09 原来的 crop-to-full-image OPD 可以教会模型答案分布，却不必然教会它依赖正确视觉区域。作者在移除答案相关区域后发现，Vision-OPD 仍取得明显高于随机的准确率。CV-OPD 用同图、同尺寸、低 IoU 的负区域构造第二个共享参数教师，把“接近正教师、远离负教师”的约束加入 JSD 蒸馏。三个不可省略的约束是：正负教师只改变 crop、读取同一学生前缀；CDL 使用有界 JSD 的 margin； 当前实现为 core_mechanism / L1 核心机制诊断，真实 VLM 更新而非图像分类打分代理。cpu-contracts.json记录已重跑的 7 个行为测试：bbox 尺寸与 IoU、JSD/Top-K tail、样本与 token gate、教师停止梯度和零正确样本的零梯度，以及严格多类 verifier、标签隔离和图像来源/切分哈希。每项先固定 seed 42，专用 crop/gate 用例内部使用 seed 2；这些是单测用例，不是独立多 seed 能力实验。测试通过不代表视觉推理能力或 GPU 训练完成。  视觉证据对齐 On-policy distillation 多模态 跨模态对齐：表征、连接器与监督 与只向正 crop 教师蒸馏相比，CDL 增加什么关系？ 单一正教师蒸馏只要求学生靠近正分布；CDL 还要求学生到负教师的 JSD 足够大，以有界散度上的 margin 表达区分。它并不要求无限拉开分布，也不保证每个 benchmark 都提高，比较应先限于监督关系的变化。 例如学生离正教师和负教师一样近时，正蒸馏可能已有较小损失；加入 margin 后仍会因未区分区域而受罚。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5ad827d370c8181c">与只向正 crop 教师蒸馏相比，CDL 增加什么关系？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Acv-opd">CV-OPD: Contrastive Vision On-policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiamen University / Moxin Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单一正教师蒸馏只要求学生靠近正分布；CDL 还要求学生到负教师的 JSD 足够大，以有界散度上的 margin 表达区分。它并不要求无限拉开分布，也不保证每个 benchmark 都提高，比较应先限于监督关系的变化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生离正教师和负教师一样近时，正蒸馏可能已有较小损失；加入 margin 后仍会因未区分区域而受罚。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13264">原论文</a> · <a href="../../../../reproductions/2610.13264-cv-opd/">实现解读</a> · <a href="#qa-5ad827d370c8181c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:cv-opd" data-paper-title="CV-OPD: Contrastive Vision On-policy Distillation" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="CV-OPD: Contrastive Vision On-policy Distillation 多模态大模型 Xiamen University / Moxin Technology 2026-10-09 原来的 crop-to-full-image OPD 可以教会模型答案分布，却不必然教会它依赖正确视觉区域。作者在移除答案相关区域后发现，Vision-OPD 仍取得明显高于随机的准确率。CV-OPD 用同图、同尺寸、低 IoU 的负区域构造第二个共享参数教师，把“接近正教师、远离负教师”的约束加入 JSD 蒸馏。三个不可省略的约束是：正负教师只改变 crop、读取同一学生前缀；CDL 使用有界 JSD 的 margin； 当前实现为 core_mechanism / L1 核心机制诊断，真实 VLM 更新而非图像分类打分代理。cpu-contracts.json记录已重跑的 7 个行为测试：bbox 尺寸与 IoU、JSD/Top-K tail、样本与 token gate、教师停止梯度和零正确样本的零梯度，以及严格多类 verifier、标签隔离和图像来源/切分哈希。每项先固定 seed 42，专用 crop/gate 用例内部使用 seed 2；这些是单测用例，不是独立多 seed 能力实验。测试通过不代表视觉推理能力或 GPU 训练完成。  视觉证据对齐 On-policy distillation 多模态 跨模态对齐：表征、连接器与监督 至少一条 rollout 答对时，应只留下正确 rollout 吗？ 不应。样本通过“至少一条正确”的门槛后，该样本全部 rollout 都保留。DAG 在整个保留 batch 的 token 上用严格大于均值的 JSD 选门；教师、生成过程与 gate 不反传，主 JSD 的 Top-100 近似还需保留完整 tail bucket。 例如八条 rollout 只有一条正确，门槛通过后仍保留八条；把另外七条删除会改变原算法的训练分布。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-438df272d6627df3">至少一条 rollout 答对时，应只留下正确 rollout 吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Acv-opd">CV-OPD: Contrastive Vision On-policy Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xiamen University / Moxin Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不应。样本通过“至少一条正确”的门槛后，该样本全部 rollout 都保留。DAG 在整个保留 batch 的 token 上用严格大于均值的 JSD 选门；教师、生成过程与 gate 不反传，主 JSD 的 Top-100 近似还需保留完整 tail bucket。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如八条 rollout 只有一条正确，门槛通过后仍保留八条；把另外七条删除会改变原算法的训练分布。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、本地结果与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13264">原论文</a> · <a href="../../../../reproductions/2610.13264-cv-opd/">实现解读</a> · <a href="#qa-438df272d6627df3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:umrm" data-paper-title="Unsupervised Multimodal Reward Modeling" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Unsupervised Multimodal Reward Modeling 多模态大模型 Massachusetts Institute of Technology 2026-10-08 偏好pair昂贵，reward benchmark名次也不必代表部署选择效用。作者冻结Qwen3-VL，在中间language层只均值池化response tokens，再训练无bias线性reward head；公开caption为positive，同一caption的颜色/数量/尺寸/方位单span变化、tail splice、clause shuffle及cross-image caption为negative，不需人工偏好标注。 bootstrap另与random own-candidate选择比较，相对原论文CHAIR不适用，小样本诊断不代表稳定能力提升。本地对照口径：零bias-free head的tie计半为pair基线，验证集选中的真实中间层head为实验组；bootstrap另与random own-candidate选择比较，相对原论文CHAIR不适用，小样本诊断不代表稳定能力提升。  multimodal-foundation-model reward-modeling frozen-layer-probe verifier-bootstrap 多模态 跨模态对齐：表征、连接器与监督 UMRM 的“无监督”是否表示训练和选择过程完全不用标签？ 不是。它主要指训练偏好 pair 可由真实 caption 的扰动构造，无需人工成对偏好标注；中间层选择使用有标注 development 集，bootstrap 还使用 cheap verifier 标签。应分别标明偏好来源、模型选择与部署效用监督，避免扩大无监督范围。 例如自动把“两个杯子”改成“三个杯子”生成负例，不需人排偏好；选择哪个隐藏层最可靠仍可需要验证标签。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<span id="paper-multimodal-models-umrm-4950018b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f4751b3724468f3d">UMRM 的“无监督”是否表示训练和选择过程完全不用标签？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Aumrm">Unsupervised Multimodal Reward Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Massachusetts Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。它主要指训练偏好 pair 可由真实 caption 的扰动构造，无需人工成对偏好标注；中间层选择使用有标注 development 集，bootstrap 还使用 cheap verifier 标签。应分别标明偏好来源、模型选择与部署效用监督，避免扩大无监督范围。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如自动把“两个杯子”改成“三个杯子”生成负例，不需人排偏好；选择哪个隐藏层最可靠仍可需要验证标签。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12707">原论文</a> · <a href="../../../../reproductions/2610.12707-umrm/">实现解读</a> · <a href="#qa-f4751b3724468f3d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:umrm" data-paper-title="Unsupervised Multimodal Reward Modeling" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Unsupervised Multimodal Reward Modeling 多模态大模型 Massachusetts Institute of Technology 2026-10-08 偏好pair昂贵，reward benchmark名次也不必代表部署选择效用。作者冻结Qwen3-VL，在中间language层只均值池化response tokens，再训练无bias线性reward head；公开caption为positive，同一caption的颜色/数量/尺寸/方位单span变化、tail splice、clause shuffle及cross-image caption为negative，不需人工偏好标注。 bootstrap另与random own-candidate选择比较，相对原论文CHAIR不适用，小样本诊断不代表稳定能力提升。本地对照口径：零bias-free head的tie计半为pair基线，验证集选中的真实中间层head为实验组；bootstrap另与random own-candidate选择比较，相对原论文CHAIR不适用，小样本诊断不代表稳定能力提升。  multimodal-foundation-model reward-modeling frozen-layer-probe verifier-bootstrap 多模态 跨模态对齐：表征、连接器与监督 UMRM 为什么用全部 B² 正负组合，而不是只比较每个样本自己的正负对？ 批内每个正例与每个负例都参与排序，让奖励头学习跨样本的分数区分，而非只拟合孤立配对。表示只池化 response token，避免图像或提示淹没回答差异；合成负例定义了训练方向，并不保证已经识别真实策略产生的所有幻觉。 例如两条正描述与两条负描述应产生四次比较，而非仅两次原配比较；这扩大了批内排序约束但不创造真实偏好标签。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-9c4a885e90ab44ef">UMRM 为什么用全部 B² 正负组合，而不是只比较每个样本自己的正负对？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Aumrm">Unsupervised Multimodal Reward Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Massachusetts Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>批内每个正例与每个负例都参与排序，让奖励头学习跨样本的分数区分，而非只拟合孤立配对。表示只池化 response token，避免图像或提示淹没回答差异；合成负例定义了训练方向，并不保证已经识别真实策略产生的所有幻觉。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两条正描述与两条负描述应产生四次比较，而非仅两次原配比较；这扩大了批内排序约束但不创造真实偏好标签。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12707">原论文</a> · <a href="../../../../reproductions/2610.12707-umrm/">实现解读</a> · <a href="#qa-9c4a885e90ab44ef">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:umrm" data-paper-title="Unsupervised Multimodal Reward Modeling" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Unsupervised Multimodal Reward Modeling 多模态大模型 Massachusetts Institute of Technology 2026-10-08 偏好pair昂贵，reward benchmark名次也不必代表部署选择效用。作者冻结Qwen3-VL，在中间language层只均值池化response tokens，再训练无bias线性reward head；公开caption为positive，同一caption的颜色/数量/尺寸/方位单span变化、tail splice、clause shuffle及cross-image caption为negative，不需人工偏好标注。 bootstrap另与random own-candidate选择比较，相对原论文CHAIR不适用，小样本诊断不代表稳定能力提升。本地对照口径：零bias-free head的tie计半为pair基线，验证集选中的真实中间层head为实验组；bootstrap另与random own-candidate选择比较，相对原论文CHAIR不适用，小样本诊断不代表稳定能力提升。  multimodal-foundation-model reward-modeling frozen-layer-probe verifier-bootstrap 多模态 跨模态对齐：表征、连接器与监督 caption 扰动准确率与 policy 自产候选的选择效用为什么可能反向变化？ 扰动负例与真实 policy 错误分布不一定一致，奖励头可能学会识别人工修改的特征，而非部署中的关键错误。用 policy 自产候选及 verifier 重训会改变奖励方向，因此某个 reward benchmark 下降，也可能同时改善实际 Best-of-N 选择。 例如颜色替换负例很好识别，但 policy 常犯的是漏掉对象；对前者高分的头未必能从真实候选中挑出最忠实描述。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ee7e257a9c99039a">caption 扰动准确率与 policy 自产候选的选择效用为什么可能反向变化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Aumrm">Unsupervised Multimodal Reward Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Massachusetts Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>扰动负例与真实 policy 错误分布不一定一致，奖励头可能学会识别人工修改的特征，而非部署中的关键错误。用 policy 自产候选及 verifier 重训会改变奖励方向，因此某个 reward benchmark 下降，也可能同时改善实际 Best-of-N 选择。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如颜色替换负例很好识别，但 policy 常犯的是漏掉对象；对前者高分的头未必能从真实候选中挑出最忠实描述。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12707">原论文</a> · <a href="../../../../reproductions/2610.12707-umrm/">实现解读</a> · <a href="#qa-ee7e257a9c99039a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:umrm" data-paper-title="Unsupervised Multimodal Reward Modeling" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Unsupervised Multimodal Reward Modeling 多模态大模型 Massachusetts Institute of Technology 2026-10-08 偏好pair昂贵，reward benchmark名次也不必代表部署选择效用。作者冻结Qwen3-VL，在中间language层只均值池化response tokens，再训练无bias线性reward head；公开caption为positive，同一caption的颜色/数量/尺寸/方位单span变化、tail splice、clause shuffle及cross-image caption为negative，不需人工偏好标注。 bootstrap另与random own-candidate选择比较，相对原论文CHAIR不适用，小样本诊断不代表稳定能力提升。本地对照口径：零bias-free head的tie计半为pair基线，验证集选中的真实中间层head为实验组；bootstrap另与random own-candidate选择比较，相对原论文CHAIR不适用，小样本诊断不代表稳定能力提升。  multimodal-foundation-model reward-modeling frozen-layer-probe verifier-bootstrap 多模态 跨模态对齐：表征、连接器与监督 UMRM构造扰动负例时，应改回答文本，还是把输入图像也替换成与负描述匹配的图？ 负采样在模型外编辑response，原图像保持不变；可做单span属性变化、tail splice、clause shuffle，或引入cross-image caption，后者默认概率为0.15。若同时换成符合负描述的图片，就改变了正负区分条件。图像与prompt还不能混入response池化。 教学例子：图中两只狗的正描述可把“两只”改成“三只”作负例，但仍给原图；不能同步换成真的有三只狗的图。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b5de587fd0730601">UMRM构造扰动负例时，应改回答文本，还是把输入图像也替换成与负描述匹配的图？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Aumrm">Unsupervised Multimodal Reward Modeling</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Massachusetts Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>负采样在模型外编辑response，原图像保持不变；可做单span属性变化、tail splice、clause shuffle，或引入cross-image caption，后者默认概率为0.15。若同时换成符合负描述的图片，就改变了正负区分条件。图像与prompt还不能混入response池化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>图中两只狗的正描述可把“两只”改成“三只”作负例，但仍给原图；不能同步换成真的有三只狗的图。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12707">原论文</a> · <a href="../../../../reproductions/2610.12707-umrm/">实现解读</a> · <a href="#qa-b5de587fd0730601">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:embedding-gemma2" data-paper-title="EmbeddingGemma 2: Open Multimodal Embeddings" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="EmbeddingGemma 2: Open Multimodal Embeddings 多模态大模型 Google DeepMind 2026-10-06 EmbeddingGemma 2 将文本、图像、音频与视频映射到统一的 768 维空间，支持检索、分类和聚类。独立模态塔可以按需关闭；文本使用任务前缀，输出经 attention-mask 均值池化，MRL 允许保留前 128/256/512 维并重新归一化，以权衡质量与向量存储成本。官方总参数约 740M，其中文本约 270M、视觉约 170M、音频约 300M。本地只实例化文本和视觉，约 440M，不使用随机小模型代替官方 checkpoint。 使用独立环境，避免改变旧论文依赖的 HF Hub &lt;2 环境。固定官方 Transformers 源码，而不是长期依赖浮动 main；缺少架构时直接报错，不换成别的 embedding 模型。  多模态基础模型 跨模态检索 Matryoshka 表示 多模态 跨模态对齐：表征、连接器与监督 统一 768 维空间是否意味着四种模态总要同时输入？ 不是。统一空间指各模态结果可以用同一种向量相似度比较，模态塔可按任务选择加载。文本、图像、音频和视频的支持范围也要与实际运行路径区分；当前本地只验证官方 checkpoint 的文本和图像，不代表其他输入管线已接通。 例如图搜文只需图像与文本路径；只运行这两条路径后，不能把音频检索也列作本地已验证功能。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<span id="paper-multimodal-models-embedding-gemma2-1f83fce4" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8d009645d6382686">统一 768 维空间是否意味着四种模态总要同时输入？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Aembedding-gemma2">EmbeddingGemma 2: Open Multimodal Embeddings</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。统一空间指各模态结果可以用同一种向量相似度比较，模态塔可按任务选择加载。文本、图像、音频和视频的支持范围也要与实际运行路径区分；当前本地只验证官方 checkpoint 的文本和图像，不代表其他输入管线已接通。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如图搜文只需图像与文本路径；只运行这两条路径后，不能把音频检索也列作本地已验证功能。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://blog.google/innovation-and-ai/technology/developers-tools/embeddinggemma-2/">原论文</a> · <a href="../../../../multimodal-models/embeddinggemma2/">实现解读</a> · <a href="#qa-8d009645d6382686">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:embedding-gemma2" data-paper-title="EmbeddingGemma 2: Open Multimodal Embeddings" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="EmbeddingGemma 2: Open Multimodal Embeddings 多模态大模型 Google DeepMind 2026-10-06 EmbeddingGemma 2 将文本、图像、音频与视频映射到统一的 768 维空间，支持检索、分类和聚类。独立模态塔可以按需关闭；文本使用任务前缀，输出经 attention-mask 均值池化，MRL 允许保留前 128/256/512 维并重新归一化，以权衡质量与向量存储成本。官方总参数约 740M，其中文本约 270M、视觉约 170M、音频约 300M。本地只实例化文本和视觉，约 440M，不使用随机小模型代替官方 checkpoint。 使用独立环境，避免改变旧论文依赖的 HF Hub &lt;2 环境。固定官方 Transformers 源码，而不是长期依赖浮动 main；缺少架构时直接报错，不换成别的 embedding 模型。  多模态基础模型 跨模态检索 Matryoshka 表示 多模态 跨模态对齐：表征、连接器与监督 Matryoshka 向量截断后为什么必须再次归一化？ 截断保留前若干维后，向量范数通常不再为一；直接点积会把保留能量差异混进相似度。重新归一化恢复余弦比较的尺度。它利用模型训练好的前缀表示，不等于任意 embedding 都能随意截断；池化时也必须排除 padding。 例如两条七百六十八维向量都截成一百二十八维，先各自归一化再检索，避免范数较大者平白占优。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c1671088f314bae5">Matryoshka 向量截断后为什么必须再次归一化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Aembedding-gemma2">EmbeddingGemma 2: Open Multimodal Embeddings</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>截断保留前若干维后，向量范数通常不再为一；直接点积会把保留能量差异混进相似度。重新归一化恢复余弦比较的尺度。它利用模型训练好的前缀表示，不等于任意 embedding 都能随意截断；池化时也必须排除 padding。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两条七百六十八维向量都截成一百二十八维，先各自归一化再检索，避免范数较大者平白占优。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://blog.google/innovation-and-ai/technology/developers-tools/embeddinggemma-2/">原论文</a> · <a href="../../../../multimodal-models/embeddinggemma2/">实现解读</a> · <a href="#qa-c1671088f314bae5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:embedding-gemma2" data-paper-title="EmbeddingGemma 2: Open Multimodal Embeddings" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="EmbeddingGemma 2: Open Multimodal Embeddings 多模态大模型 Google DeepMind 2026-10-06 EmbeddingGemma 2 将文本、图像、音频与视频映射到统一的 768 维空间，支持检索、分类和聚类。独立模态塔可以按需关闭；文本使用任务前缀，输出经 attention-mask 均值池化，MRL 允许保留前 128/256/512 维并重新归一化，以权衡质量与向量存储成本。官方总参数约 740M，其中文本约 270M、视觉约 170M、音频约 300M。本地只实例化文本和视觉，约 440M，不使用随机小模型代替官方 checkpoint。 使用独立环境，避免改变旧论文依赖的 HF Hub &lt;2 环境。固定官方 Transformers 源码，而不是长期依赖浮动 main；缺少架构时直接报错，不换成别的 embedding 模型。  多模态基础模型 跨模态检索 Matryoshka 表示 多模态 跨模态对齐：表征、连接器与监督 MRL 截断与随机删去向量维度有什么区别？ MRL 训练使预定的前缀维度也能承担表示任务，因此可保留前 128、256 或 512 维，再归一化。随机挑选维度没有这种训练约定；较短前缀节省存储与检索成本，但具体质量变化仍需按任务和固定维度报告。 例如完整向量有七百六十八维，取前一百二十八维属于预设使用方式；每次随机抽一百二十八维不是同一种压缩。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-eed6fdf443ec6128">MRL 截断与随机删去向量维度有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Aembedding-gemma2">EmbeddingGemma 2: Open Multimodal Embeddings</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>MRL 训练使预定的前缀维度也能承担表示任务，因此可保留前 128、256 或 512 维，再归一化。随机挑选维度没有这种训练约定；较短前缀节省存储与检索成本，但具体质量变化仍需按任务和固定维度报告。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如完整向量有七百六十八维，取前一百二十八维属于预设使用方式；每次随机抽一百二十八维不是同一种压缩。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://blog.google/innovation-and-ai/technology/developers-tools/embeddinggemma-2/">原论文</a> · <a href="../../../../multimodal-models/embeddinggemma2/">实现解读</a> · <a href="#qa-eed6fdf443ec6128">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:embedding-gemma2" data-paper-title="EmbeddingGemma 2: Open Multimodal Embeddings" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="EmbeddingGemma 2: Open Multimodal Embeddings 多模态大模型 Google DeepMind 2026-10-06 EmbeddingGemma 2 将文本、图像、音频与视频映射到统一的 768 维空间，支持检索、分类和聚类。独立模态塔可以按需关闭；文本使用任务前缀，输出经 attention-mask 均值池化，MRL 允许保留前 128/256/512 维并重新归一化，以权衡质量与向量存储成本。官方总参数约 740M，其中文本约 270M、视觉约 170M、音频约 300M。本地只实例化文本和视觉，约 440M，不使用随机小模型代替官方 checkpoint。 使用独立环境，避免改变旧论文依赖的 HF Hub &lt;2 环境。固定官方 Transformers 源码，而不是长期依赖浮动 main；缺少架构时直接报错，不换成别的 embedding 模型。  多模态基础模型 跨模态检索 Matryoshka 表示 多模态 跨模态对齐：表征、连接器与监督 均值池化、截断和精度设置中有哪些不可忽略的细节？ 池化必须用 attention mask 排除 padding；截取前缀后再次 L2 归一化。文本查询与文档采用各自前缀，图像不加文本前缀；官方激活范围可能让 FP16 产生非有限值，本地固定 FP32，并显式拒绝非有限值或零向量。 例如两条内容相同、补齐长度不同的文本，应在 mask 池化后得到一致表示；把 padding 算入均值会制造长度依赖。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1730598e354b01ed">均值池化、截断和精度设置中有哪些不可忽略的细节？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Aembedding-gemma2">EmbeddingGemma 2: Open Multimodal Embeddings</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>池化必须用 attention mask 排除 padding；截取前缀后再次 L2 归一化。文本查询与文档采用各自前缀，图像不加文本前缀；官方激活范围可能让 FP16 产生非有限值，本地固定 FP32，并显式拒绝非有限值或零向量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两条内容相同、补齐长度不同的文本，应在 mask 池化后得到一致表示；把 padding 算入均值会制造长度依赖。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、结果与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://blog.google/innovation-and-ai/technology/developers-tools/embeddinggemma-2/">原论文</a> · <a href="../../../../multimodal-models/embeddinggemma2/">实现解读</a> · <a href="#qa-1730598e354b01ed">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:omni-embed-mini" data-paper-title="Omni-Embed-Mini: Binding Modalities Without Forgetting via Dense Distillation" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Omni-Embed-Mini: Binding Modalities Without Forgetting via Dense Distillation 基础模型 原文首页未列第一作者机构 2026-10-01 冻结文本骨干，把每个媒体样本的稠密级联描述经同一文本骨干得到 teacher target，再训练轻量投影器和分阶段 LoRA 对齐六种模态。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行同几何空间的稠密描述蒸馏；未训练模态编码器或复现实测榜单。执行同几何空间的稠密描述蒸馏；未训练模态编码器或复现实测榜单。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  多模态嵌入 蒸馏 LoRA 多模态 跨模态对齐：表征、连接器与监督 Omni-Embed-Mini接收媒体后，要输出一份新媒体，还是用于检索的向量？ 这里学习的是媒体的语义embedding，媒体表示与描述文本目标在同一向量空间比较；不是根据描述生成图片、音频或视频。稠密描述在训练时提供目标表示，实际媒体路径仍要编码媒体输入，不能把“多模态”直接理解成具备各种媒体生成能力。 教学例子：给一段音频得到可与文字查询比较的向量，是表示任务；按一句文字合成一段音频，则是另一个生成任务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<span id="paper-foundation-models-omni-embed-mini-210068e5" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5145055c5225c1c3">Omni-Embed-Mini接收媒体后，要输出一份新媒体，还是用于检索的向量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aomni-embed-mini">Omni-Embed-Mini: Binding Modalities Without Forgetting via Dense Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这里学习的是媒体的语义embedding，媒体表示与描述文本目标在同一向量空间比较；不是根据描述生成图片、音频或视频。稠密描述在训练时提供目标表示，实际媒体路径仍要编码媒体输入，不能把“多模态”直接理解成具备各种媒体生成能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>给一段音频得到可与文字查询比较的向量，是表示任务；按一句文字合成一段音频，则是另一个生成任务。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02148">原论文</a> · <a href="../../../../foundation-models/2610.02148-omni-embed-mini/">实现解读</a> · <a href="#qa-5145055c5225c1c3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:omni-embed-mini" data-paper-title="Omni-Embed-Mini: Binding Modalities Without Forgetting via Dense Distillation" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Omni-Embed-Mini: Binding Modalities Without Forgetting via Dense Distillation 基础模型 原文首页未列第一作者机构 2026-10-01 冻结文本骨干，把每个媒体样本的稠密级联描述经同一文本骨干得到 teacher target，再训练轻量投影器和分阶段 LoRA 对齐六种模态。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行同几何空间的稠密描述蒸馏；未训练模态编码器或复现实测榜单。执行同几何空间的稠密描述蒸馏；未训练模态编码器或复现实测榜单。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  多模态嵌入 蒸馏 LoRA 多模态 跨模态对齐：表征、连接器与监督 用描述文本作蒸馏目标，为什么能减少媒体适配对文本骨干的干扰？ 冻结文本骨干提供稳定的语义坐标，媒体样本的稠密描述在该坐标中形成教师目标。投影器与受控 LoRA 学习把媒体映射过去，而不是让文本空间随每种模态任意漂移；教师目标停止梯度，仍需检验描述是否遗漏媒体中的关键信息。 例如同一视频的动作与场景被写入描述，视频表示向冻结文本目标靠近；若描述漏掉小字，蒸馏也不会凭空补全。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-4491baa96084cd11">用描述文本作蒸馏目标，为什么能减少媒体适配对文本骨干的干扰？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aomni-embed-mini">Omni-Embed-Mini: Binding Modalities Without Forgetting via Dense Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冻结文本骨干提供稳定的语义坐标，媒体样本的稠密描述在该坐标中形成教师目标。投影器与受控 LoRA 学习把媒体映射过去，而不是让文本空间随每种模态任意漂移；教师目标停止梯度，仍需检验描述是否遗漏媒体中的关键信息。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一视频的动作与场景被写入描述，视频表示向冻结文本目标靠近；若描述漏掉小字，蒸馏也不会凭空补全。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02148">原论文</a> · <a href="../../../../foundation-models/2610.02148-omni-embed-mini/">实现解读</a> · <a href="#qa-4491baa96084cd11">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:omni-embed-mini" data-paper-title="Omni-Embed-Mini: Binding Modalities Without Forgetting via Dense Distillation" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Omni-Embed-Mini: Binding Modalities Without Forgetting via Dense Distillation 基础模型 原文首页未列第一作者机构 2026-10-01 冻结文本骨干，把每个媒体样本的稠密级联描述经同一文本骨干得到 teacher target，再训练轻量投影器和分阶段 LoRA 对齐六种模态。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行同几何空间的稠密描述蒸馏；未训练模态编码器或复现实测榜单。执行同几何空间的稠密描述蒸馏；未训练模态编码器或复现实测榜单。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  多模态嵌入 蒸馏 LoRA 多模态 跨模态对齐：表征、连接器与监督 冻结文本骨干的蒸馏与全参数联合多模态训练有何取舍？ 冻结骨干给新模态提供相对稳定的语义坐标，减少改写既有文本表示的风险，训练重点落在投影器与分阶段适配上。全参数训练可调整更广，却也可能改变旧文本能力；这里是参数更新范围的取舍，不能直接推成任一方法效果必胜。 例如接入音频时保持旧文本检索向量稳定较容易维护索引，但声音特有信息能否表达仍受现有目标空间约束。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a011fd986e9bb29b">冻结文本骨干的蒸馏与全参数联合多模态训练有何取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aomni-embed-mini">Omni-Embed-Mini: Binding Modalities Without Forgetting via Dense Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冻结骨干给新模态提供相对稳定的语义坐标，减少改写既有文本表示的风险，训练重点落在投影器与分阶段适配上。全参数训练可调整更广，却也可能改变旧文本能力；这里是参数更新范围的取舍，不能直接推成任一方法效果必胜。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如接入音频时保持旧文本检索向量稳定较容易维护索引，但声音特有信息能否表达仍受现有目标空间约束。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02148">原论文</a> · <a href="../../../../foundation-models/2610.02148-omni-embed-mini/">实现解读</a> · <a href="#qa-a011fd986e9bb29b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:omni-embed-mini" data-paper-title="Omni-Embed-Mini: Binding Modalities Without Forgetting via Dense Distillation" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Omni-Embed-Mini: Binding Modalities Without Forgetting via Dense Distillation 基础模型 原文首页未列第一作者机构 2026-10-01 冻结文本骨干，把每个媒体样本的稠密级联描述经同一文本骨干得到 teacher target，再训练轻量投影器和分阶段 LoRA 对齐六种模态。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行同几何空间的稠密描述蒸馏；未训练模态编码器或复现实测榜单。执行同几何空间的稠密描述蒸馏；未训练模态编码器或复现实测榜单。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  多模态嵌入 蒸馏 LoRA 多模态 跨模态对齐：表征、连接器与监督 余弦蒸馏中 stopgrad 应施加在哪条路径？ 目标来自冻结文本骨干编码的描述，应停止该目标路径的梯度；媒体表示与目标计算余弦损失，由允许更新的媒体接口接收梯度。本地只执行相同几何空间的稠密描述蒸馏诊断，没有训练完整六模态编码器或复现检索榜单。 例如降低媒体向量与描述向量的夹角时，只移动待训练的媒体映射；若连目标也一起自由移动，就改变了固定语义锚点。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-87c149ce97e5da8a">余弦蒸馏中 stopgrad 应施加在哪条路径？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aomni-embed-mini">Omni-Embed-Mini: Binding Modalities Without Forgetting via Dense Distillation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标来自冻结文本骨干编码的描述，应停止该目标路径的梯度；媒体表示与目标计算余弦损失，由允许更新的媒体接口接收梯度。本地只执行相同几何空间的稠密描述蒸馏诊断，没有训练完整六模态编码器或复现检索榜单。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如降低媒体向量与描述向量的夹角时，只移动待训练的媒体映射；若连目标也一起自由移动，就改变了固定语义锚点。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02148">原论文</a> · <a href="../../../../foundation-models/2610.02148-omni-embed-mini/">实现解读</a> · <a href="#qa-87c149ce97e5da8a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:sensenova-u1-5" data-paper-title="SenseNova-U1.5: Towards Native Unified Visual Intelligence" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="SenseNova-U1.5: Towards Native Unified Visual Intelligence 基础模型 SenseTime Research 2026-09-10 用空间 patch reconstruction 摆脱 tokenizer/VAE，并以多专家 OPD 统一视觉理解与生成后训练。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 masked patch target 与 expert OPD 融合；未复刻 8B 多阶段训练。本地执行 masked patch target 与 expert OPD 融合；未复刻 8B 多阶段训练。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  统一多模态 视觉生成与理解 多模态 跨模态对齐：表征、连接器与监督 SenseNova-U1.5的视觉理解与视觉生成，是同一种输入输出方向吗？ 不是。理解任务以视觉内容为条件形成回答或判断，生成任务则根据条件产生视觉内容；统一模型要承接两种方向的监督。空间patch重建描述的是生成表示路径，多专家OPD描述后训练信号组织，不能因统一命名就把某个patch算子当成两种能力均已完成。 教学例子：看图回答“有什么”与按条件产生一幅图，验收对象不同；前者回答正确不等于后者已能生成对应图像。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<span id="paper-foundation-models-sensenova-u1-5-44bbf8fb" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ccda8ef48387ba89">SenseNova-U1.5的视觉理解与视觉生成，是同一种输入输出方向吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asensenova-u1-5">SenseNova-U1.5: Towards Native Unified Visual Intelligence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · SenseTime Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。理解任务以视觉内容为条件形成回答或判断，生成任务则根据条件产生视觉内容；统一模型要承接两种方向的监督。空间patch重建描述的是生成表示路径，多专家OPD描述后训练信号组织，不能因统一命名就把某个patch算子当成两种能力均已完成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>看图回答“有什么”与按条件产生一幅图，验收对象不同；前者回答正确不等于后者已能生成对应图像。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11929">原论文</a> · <a href="../../../../foundation-models/2609.11929-sensenova-u1-5/">实现解读</a> · <a href="#qa-ccda8ef48387ba89">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:sensenova-u1-5" data-paper-title="SenseNova-U1.5: Towards Native Unified Visual Intelligence" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="SenseNova-U1.5: Towards Native Unified Visual Intelligence 基础模型 SenseTime Research 2026-09-10 用空间 patch reconstruction 摆脱 tokenizer/VAE，并以多专家 OPD 统一视觉理解与生成后训练。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 masked patch target 与 expert OPD 融合；未复刻 8B 多阶段训练。本地执行 masked patch target 与 expert OPD 融合；未复刻 8B 多阶段训练。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  统一多模态 视觉生成与理解 多模态 跨模态对齐：表征、连接器与监督 直接做空间 patch reconstruction 与先预测离散图像码有什么区别？ 离散路线先依赖 tokenizer 或 VAE 把图像变成另一种码，再学习这些码的预测；空间 patch 重建直接以图像局部结构作为训练对象，减少对该中间接口的依赖。这改变了表示与监督路径，但不能据此断言没有信息瓶颈或生成成本必然更低。 例如同一张图片可先变成码本编号再预测，也可直接训练重建空间小块；两种路线的误差来源需要分开检查。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-48a83136d0677aa9">直接做空间 patch reconstruction 与先预测离散图像码有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asensenova-u1-5">SenseNova-U1.5: Towards Native Unified Visual Intelligence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · SenseTime Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>离散路线先依赖 tokenizer 或 VAE 把图像变成另一种码，再学习这些码的预测；空间 patch 重建直接以图像局部结构作为训练对象，减少对该中间接口的依赖。这改变了表示与监督路径，但不能据此断言没有信息瓶颈或生成成本必然更低。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一张图片可先变成码本编号再预测，也可直接训练重建空间小块；两种路线的误差来源需要分开检查。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11929">原论文</a> · <a href="../../../../foundation-models/2609.11929-sensenova-u1-5/">实现解读</a> · <a href="#qa-48a83136d0677aa9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:sensenova-u1-5" data-paper-title="SenseNova-U1.5: Towards Native Unified Visual Intelligence" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="SenseNova-U1.5: Towards Native Unified Visual Intelligence 基础模型 SenseTime Research 2026-09-10 用空间 patch reconstruction 摆脱 tokenizer/VAE，并以多专家 OPD 统一视觉理解与生成后训练。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 masked patch target 与 expert OPD 融合；未复刻 8B 多阶段训练。本地执行 masked patch target 与 expert OPD 融合；未复刻 8B 多阶段训练。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  统一多模态 视觉生成与理解 多模态 跨模态对齐：表征、连接器与监督 多专家 OPD 与仅向单一教师蒸馏，在监督组织上有何区别？ 多专家提供不同任务或能力方向的教师信号，统一模型需要协调这些信号，而单教师蒸馏只对齐一种教师分布。多来源可以扩大监督覆盖，也可能产生不一致；不能因为专家数量更多就推断理解与生成质量必然同时提升。 例如理解教师强调物体关系，生成教师强调图像重建，两种信号要由统一模型融合，不能简单当成同一个目标的重复样本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b3467848fb9faad3">多专家 OPD 与仅向单一教师蒸馏，在监督组织上有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asensenova-u1-5">SenseNova-U1.5: Towards Native Unified Visual Intelligence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · SenseTime Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多专家提供不同任务或能力方向的教师信号，统一模型需要协调这些信号，而单教师蒸馏只对齐一种教师分布。多来源可以扩大监督覆盖，也可能产生不一致；不能因为专家数量更多就推断理解与生成质量必然同时提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如理解教师强调物体关系，生成教师强调图像重建，两种信号要由统一模型融合，不能简单当成同一个目标的重复样本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11929">原论文</a> · <a href="../../../../foundation-models/2609.11929-sensenova-u1-5/">实现解读</a> · <a href="#qa-b3467848fb9faad3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:sensenova-u1-5" data-paper-title="SenseNova-U1.5: Towards Native Unified Visual Intelligence" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="SenseNova-U1.5: Towards Native Unified Visual Intelligence 基础模型 SenseTime Research 2026-09-10 用空间 patch reconstruction 摆脱 tokenizer/VAE，并以多专家 OPD 统一视觉理解与生成后训练。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 masked patch target 与 expert OPD 融合；未复刻 8B 多阶段训练。本地执行 masked patch target 与 expert OPD 融合；未复刻 8B 多阶段训练。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  统一多模态 视觉生成与理解 多模态 跨模态对齐：表征、连接器与监督 本地 masked patch 与 expert OPD 统计能证明统一 8B 模型完成了吗？ 不能。当前仅有决定性算子的 reference kernel 与三 seed 状态转换诊断，覆盖 masked patch target 和专家蒸馏融合；没有复刻统一 8B 模型的多阶段训练。算子门控或损失数值可检查执行路径，但不能充当真实理解和生成 benchmark。 例如小张量上专家权重相加正确，只证明融合公式运行；它没有展示八十亿参数模型生成可用图像或回答真实问题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-65cee03b70bff28b">本地 masked patch 与 expert OPD 统计能证明统一 8B 模型完成了吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asensenova-u1-5">SenseNova-U1.5: Towards Native Unified Visual Intelligence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · SenseTime Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。当前仅有决定性算子的 reference kernel 与三 seed 状态转换诊断，覆盖 masked patch target 和专家蒸馏融合；没有复刻统一 8B 模型的多阶段训练。算子门控或损失数值可检查执行路径，但不能充当真实理解和生成 benchmark。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如小张量上专家权重相加正确，只证明融合公式运行；它没有展示八十亿参数模型生成可用图像或回答真实问题。</p>
<p class="ar-learning-sources">依据：核心公式或操作、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11929">原论文</a> · <a href="../../../../foundation-models/2609.11929-sensenova-u1-5/">实现解读</a> · <a href="#qa-65cee03b70bff28b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:cue2narrate-drl" data-paper-title="From Visual Cues to Spoken Narration: Rethinking Audio Description" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="From Visual Cues to Spoken Narration: Rethinking Audio Description 多模态大模型 TU Darmstadt &amp; hessian.AI 2026-09-01 固定v1 Section4.3 Eqs5–8：SFT按每个AD目标token求和；positive/negative评分均为同一当前模型和prompt上的token-mean logp，prompt/padding排除；DRL=-logsigmoid((s+−s−)/0.5)，全loss加0.2DRL。离线负caption生成冻结，但其当前模型likelihood仍反传。 成本过高，不复现（审查 DONE）。6.64M双头定位器，Qwen2.5-VL-7B/Qwen3-VL-8B LoRA，训练32帧/推理64帧，多阶段长电影训练；LSMDC研究限制授权、MAD-Eval NDA。完整数据/定位+VLM训练超单卡短时预算，不下载视频或权重；本文未给总GPU小时，不编造。输入是当前模型对AD与缓存negative caption的teacher-forced logits/labels，必须正确对齐并以-100排除prompt/padding；不包含Stage1、visual cue提取、character bank或负caption生成。  多模态生成 视频音频描述 多模态 跨模态对齐：表征、连接器与监督 这里的负 caption 为什么仍与同一视觉线索和 prompt 配对？ 正负描述要在相同条件下比较，差异才集中于描述内容是否适合目标音频描述任务。若同时更换图像或提示，分数差可能来自条件难度，而非模型是否区分有效线索；离线准备负描述只是构造训练材料，不是部署时额外生成负样本。 例如同一电影片段的正确描述是“她把杯子放下”，负描述改成无关动作；两者都必须使用同一片段和同一任务提示评分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<span id="paper-multimodal-models-cue2narrate-drl-b44764fd" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c735438cc2e66022">这里的负 caption 为什么仍与同一视觉线索和 prompt 配对？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Acue2narrate-drl">From Visual Cues to Spoken Narration: Rethinking Audio Description</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · TU Darmstadt &amp; hessian.AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>正负描述要在相同条件下比较，差异才集中于描述内容是否适合目标音频描述任务。若同时更换图像或提示，分数差可能来自条件难度，而非模型是否区分有效线索；离线准备负描述只是构造训练材料，不是部署时额外生成负样本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一电影片段的正确描述是“她把杯子放下”，负描述改成无关动作；两者都必须使用同一片段和同一任务提示评分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.01725v1">原论文</a> · <a href="../../../../multimodal-models/2609.01725-cue2narrate-drl/">实现解读</a> · <a href="#qa-c735438cc2e66022">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:cue2narrate-drl" data-paper-title="From Visual Cues to Spoken Narration: Rethinking Audio Description" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="From Visual Cues to Spoken Narration: Rethinking Audio Description 多模态大模型 TU Darmstadt &amp; hessian.AI 2026-09-01 固定v1 Section4.3 Eqs5–8：SFT按每个AD目标token求和；positive/negative评分均为同一当前模型和prompt上的token-mean logp，prompt/padding排除；DRL=-logsigmoid((s+−s−)/0.5)，全loss加0.2DRL。离线负caption生成冻结，但其当前模型likelihood仍反传。 成本过高，不复现（审查 DONE）。6.64M双头定位器，Qwen2.5-VL-7B/Qwen3-VL-8B LoRA，训练32帧/推理64帧，多阶段长电影训练；LSMDC研究限制授权、MAD-Eval NDA。完整数据/定位+VLM训练超单卡短时预算，不下载视频或权重；本文未给总GPU小时，不编造。输入是当前模型对AD与缓存negative caption的teacher-forced logits/labels，必须正确对齐并以-100排除prompt/padding；不包含Stage1、visual cue提取、character bank或负caption生成。  多模态生成 视频音频描述 多模态 跨模态对齐：表征、连接器与监督 负描述由冻结模型生成，为什么训练时还要对它的当前似然反向传播？ 冻结负描述生成器只固定负样本内容；当前模型对正负文本的评分仍应可训练。DRL 比较同一视觉输入下两段有效目标文本的平均对数似然，梯度同时提高正描述相对负描述的偏好；若把负评分也 detach，就改变了原本的对比优化方向。 例如同一画面正描述说人在走路、负描述说人在跑步；固定两句话后，当前模型仍须调整二者的相对评分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-611aae51c5d5db99">负描述由冻结模型生成，为什么训练时还要对它的当前似然反向传播？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Acue2narrate-drl">From Visual Cues to Spoken Narration: Rethinking Audio Description</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · TU Darmstadt &amp; hessian.AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冻结负描述生成器只固定负样本内容；当前模型对正负文本的评分仍应可训练。DRL 比较同一视觉输入下两段有效目标文本的平均对数似然，梯度同时提高正描述相对负描述的偏好；若把负评分也 detach，就改变了原本的对比优化方向。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一画面正描述说人在走路、负描述说人在跑步；固定两句话后，当前模型仍须调整二者的相对评分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.01725v1">原论文</a> · <a href="../../../../multimodal-models/2609.01725-cue2narrate-drl/">实现解读</a> · <a href="#qa-611aae51c5d5db99">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:cue2narrate-drl" data-paper-title="From Visual Cues to Spoken Narration: Rethinking Audio Description" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="From Visual Cues to Spoken Narration: Rethinking Audio Description 多模态大模型 TU Darmstadt &amp; hessian.AI 2026-09-01 固定v1 Section4.3 Eqs5–8：SFT按每个AD目标token求和；positive/negative评分均为同一当前模型和prompt上的token-mean logp，prompt/padding排除；DRL=-logsigmoid((s+−s−)/0.5)，全loss加0.2DRL。离线负caption生成冻结，但其当前模型likelihood仍反传。 成本过高，不复现（审查 DONE）。6.64M双头定位器，Qwen2.5-VL-7B/Qwen3-VL-8B LoRA，训练32帧/推理64帧，多阶段长电影训练；LSMDC研究限制授权、MAD-Eval NDA。完整数据/定位+VLM训练超单卡短时预算，不下载视频或权重；本文未给总GPU小时，不编造。输入是当前模型对AD与缓存negative caption的teacher-forced logits/labels，必须正确对齐并以-100排除prompt/padding；不包含Stage1、visual cue提取、character bank或负caption生成。  多模态生成 视频音频描述 多模态 跨模态对齐：表征、连接器与监督 DRL 与只做正描述 SFT 多加了什么约束？ SFT 提高正确描述各目标 token 的似然，DRL 还显式拉开正负描述的平均对数概率差。它因此提供相对区分信号；但负描述的构造质量决定了信号含义，容易识别的负例并不自动教会细粒度视觉事实判断。 例如模型同时很喜欢“她坐下”和错误的“她跑开”，只提高前者概率未必压低后者；相对损失会直接约束这对分数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0bcd2ec1cbd06a88">DRL 与只做正描述 SFT 多加了什么约束？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Acue2narrate-drl">From Visual Cues to Spoken Narration: Rethinking Audio Description</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · TU Darmstadt &amp; hessian.AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>SFT 提高正确描述各目标 token 的似然，DRL 还显式拉开正负描述的平均对数概率差。它因此提供相对区分信号；但负描述的构造质量决定了信号含义，容易识别的负例并不自动教会细粒度视觉事实判断。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型同时很喜欢“她坐下”和错误的“她跑开”，只提高前者概率未必压低后者；相对损失会直接约束这对分数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.01725v1">原论文</a> · <a href="../../../../multimodal-models/2609.01725-cue2narrate-drl/">实现解读</a> · <a href="#qa-0bcd2ec1cbd06a88">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:cue2narrate-drl" data-paper-title="From Visual Cues to Spoken Narration: Rethinking Audio Description" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="From Visual Cues to Spoken Narration: Rethinking Audio Description 多模态大模型 TU Darmstadt &amp; hessian.AI 2026-09-01 固定v1 Section4.3 Eqs5–8：SFT按每个AD目标token求和；positive/negative评分均为同一当前模型和prompt上的token-mean logp，prompt/padding排除；DRL=-logsigmoid((s+−s−)/0.5)，全loss加0.2DRL。离线负caption生成冻结，但其当前模型likelihood仍反传。 成本过高，不复现（审查 DONE）。6.64M双头定位器，Qwen2.5-VL-7B/Qwen3-VL-8B LoRA，训练32帧/推理64帧，多阶段长电影训练；LSMDC研究限制授权、MAD-Eval NDA。完整数据/定位+VLM训练超单卡短时预算，不下载视频或权重；本文未给总GPU小时，不编造。输入是当前模型对AD与缓存negative caption的teacher-forced logits/labels，必须正确对齐并以-100排除prompt/padding；不包含Stage1、visual cue提取、character bank或负caption生成。  多模态生成 视频音频描述 多模态 跨模态对齐：表征、连接器与监督 SFT 和 DRL 的长度归一化能统一成同一个均值吗？ 不能。README 固定的公式要求 SFT 在每个样本内对有效目标 token 求和后再做批平均，DRL 则先分别计算正负描述的 token 平均 logp。prompt 与 padding 均排除；负描述生成器冻结也不意味着当前模型对负描述的 logp 停止梯度。 例如正描述十个 token、负描述二十个 token，DRL 比较各自均值；若直接比较总和，长度较长者会被额外惩罚。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e8bcd9e2f80d297e">SFT 和 DRL 的长度归一化能统一成同一个均值吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Acue2narrate-drl">From Visual Cues to Spoken Narration: Rethinking Audio Description</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · TU Darmstadt &amp; hessian.AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。README 固定的公式要求 SFT 在每个样本内对有效目标 token 求和后再做批平均，DRL 则先分别计算正负描述的 token 平均 logp。prompt 与 padding 均排除；负描述生成器冻结也不意味着当前模型对负描述的 logp 停止梯度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如正描述十个 token、负描述二十个 token，DRL 比较各自均值；若直接比较总和，长度较长者会被额外惩罚。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.01725v1">原论文</a> · <a href="../../../../multimodal-models/2609.01725-cue2narrate-drl/">实现解读</a> · <a href="#qa-e8bcd9e2f80d297e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mllmclip" data-paper-title="MLLMCLIP: Feature-Level Distillation of MLLM for Robust Vision-Language Representations" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="MLLMCLIP: Feature-Level Distillation of MLLM for Robust Vision-Language Representations 基础模型 KAIST / Sony AI 2026-08-26 MLLM 的丰富视觉语义难以直接迁移到轻量 CLIP。论文从 teacher 各层按 attention 自适应选 token，以 CKA 对齐 student 图像/文本特征，保留部署时的双塔效率。 Fidelity：公开 checkpoint 核心路径。主路径加载真实 SmolVLM teacher 与 CLIP student，在公开图像上训练 CKA projection；MovieLens/NumPy 路径仅保留为快速机制诊断。真实 checkpoint 路径使用公开图像和 SmolVLM 视觉 encoder feature，但仍未复刻论文完整 26-benchmark 训练规模、原始 teacher 配方与全量 CLIP 预训练。MovieLens proxy 仍为 diagnostic-only，不能与视觉 benchmark 混报。  multimodal-foundation-model feature-distillation compositionality cka 多模态 跨模态对齐：表征、连接器与监督 MLLMCLIP 为什么把多模态大模型放在教师端而保留双塔学生？ 教师具有丰富的图文交互语义，但直接部署其生成路径成本较高；学生保持 CLIP 图像与文本独立编码的接口，通过特征蒸馏吸收关系知识。训练读取教师不意味着在线检索也必须每次调用教师，因此应分别核算训练与部署代价。 例如离线用大模型分析图文关系并训练学生，线上可预先缓存商品图向量，再用文本向量检索，无需逐商品生成回答。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<span id="paper-foundation-models-mllmclip-2c53372a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-39e7cdcd2b99eef2">MLLMCLIP 为什么把多模态大模型放在教师端而保留双塔学生？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amllmclip">MLLMCLIP: Feature-Level Distillation of MLLM for Robust Vision-Language Representations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST / Sony AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>教师具有丰富的图文交互语义，但直接部署其生成路径成本较高；学生保持 CLIP 图像与文本独立编码的接口，通过特征蒸馏吸收关系知识。训练读取教师不意味着在线检索也必须每次调用教师，因此应分别核算训练与部署代价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如离线用大模型分析图文关系并训练学生，线上可预先缓存商品图向量，再用文本向量检索，无需逐商品生成回答。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25575">原论文</a> · <a href="../../../../reproductions/2608.25575-mllmclip/">实现解读</a> · <a href="#qa-39e7cdcd2b99eef2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mllmclip" data-paper-title="MLLMCLIP: Feature-Level Distillation of MLLM for Robust Vision-Language Representations" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="MLLMCLIP: Feature-Level Distillation of MLLM for Robust Vision-Language Representations 基础模型 KAIST / Sony AI 2026-08-26 MLLM 的丰富视觉语义难以直接迁移到轻量 CLIP。论文从 teacher 各层按 attention 自适应选 token，以 CKA 对齐 student 图像/文本特征，保留部署时的双塔效率。 Fidelity：公开 checkpoint 核心路径。主路径加载真实 SmolVLM teacher 与 CLIP student，在公开图像上训练 CKA projection；MovieLens/NumPy 路径仅保留为快速机制诊断。真实 checkpoint 路径使用公开图像和 SmolVLM 视觉 encoder feature，但仍未复刻论文完整 26-benchmark 训练规模、原始 teacher 配方与全量 CLIP 预训练。MovieLens proxy 仍为 diagnostic-only，不能与视觉 benchmark 混报。  multimodal-foundation-model feature-distillation compositionality cka 多模态 跨模态对齐：表征、连接器与监督 CKA 蒸馏为什么能在师生特征维度不同的情况下传递结构？ CKA 比较样本间表示关系的对齐程度，而不要求逐维一一相等。教师先按注意力选择有信息的 token，再用这种结构约束训练学生图文表示；学生仍保持轻量双塔部署，迁移的是特征关系，不是把大型教师的全部推理过程复制进去。 例如教师输出一千维、学生输出五百维，仍可约束两者把相似样本放近；无需把每个坐标硬配成同一含义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-e4e11c01b301e672">CKA 蒸馏为什么能在师生特征维度不同的情况下传递结构？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amllmclip">MLLMCLIP: Feature-Level Distillation of MLLM for Robust Vision-Language Representations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST / Sony AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>CKA 比较样本间表示关系的对齐程度，而不要求逐维一一相等。教师先按注意力选择有信息的 token，再用这种结构约束训练学生图文表示；学生仍保持轻量双塔部署，迁移的是特征关系，不是把大型教师的全部推理过程复制进去。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如教师输出一千维、学生输出五百维，仍可约束两者把相似样本放近；无需把每个坐标硬配成同一含义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25575">原论文</a> · <a href="../../../../reproductions/2608.25575-mllmclip/">实现解读</a> · <a href="#qa-e4e11c01b301e672">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mllmclip" data-paper-title="MLLMCLIP: Feature-Level Distillation of MLLM for Robust Vision-Language Representations" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="MLLMCLIP: Feature-Level Distillation of MLLM for Robust Vision-Language Representations 基础模型 KAIST / Sony AI 2026-08-26 MLLM 的丰富视觉语义难以直接迁移到轻量 CLIP。论文从 teacher 各层按 attention 自适应选 token，以 CKA 对齐 student 图像/文本特征，保留部署时的双塔效率。 Fidelity：公开 checkpoint 核心路径。主路径加载真实 SmolVLM teacher 与 CLIP student，在公开图像上训练 CKA projection；MovieLens/NumPy 路径仅保留为快速机制诊断。真实 checkpoint 路径使用公开图像和 SmolVLM 视觉 encoder feature，但仍未复刻论文完整 26-benchmark 训练规模、原始 teacher 配方与全量 CLIP 预训练。MovieLens proxy 仍为 diagnostic-only，不能与视觉 benchmark 混报。  multimodal-foundation-model feature-distillation compositionality cka 多模态 跨模态对齐：表征、连接器与监督 MLLMCLIP按教师attention选择token，与不加区分地蒸馏全部token，监督对象有什么不同？ 选择策略先从教师各层找出较有信息的token，再对这些表示建立结构蒸馏信号；全token方案则把所有位置都纳入同一监督范围。区别在教师信息的筛选，而不是CKA是否允许异维表示；选择可能遗漏信息，不能未经对照就宣称一定更优。 教学例子：教师一层有许多背景位置，attention选择让部分位置成为监督来源；并非只要token更多，学生就必然学到更多有效知识。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-40aa0ee3239e5e79">MLLMCLIP按教师attention选择token，与不加区分地蒸馏全部token，监督对象有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amllmclip">MLLMCLIP: Feature-Level Distillation of MLLM for Robust Vision-Language Representations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST / Sony AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>选择策略先从教师各层找出较有信息的token，再对这些表示建立结构蒸馏信号；全token方案则把所有位置都纳入同一监督范围。区别在教师信息的筛选，而不是CKA是否允许异维表示；选择可能遗漏信息，不能未经对照就宣称一定更优。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教师一层有许多背景位置，attention选择让部分位置成为监督来源；并非只要token更多，学生就必然学到更多有效知识。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25575">原论文</a> · <a href="../../../../reproductions/2608.25575-mllmclip/">实现解读</a> · <a href="#qa-40aa0ee3239e5e79">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:mllmclip" data-paper-title="MLLMCLIP: Feature-Level Distillation of MLLM for Robust Vision-Language Representations" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="MLLMCLIP: Feature-Level Distillation of MLLM for Robust Vision-Language Representations 基础模型 KAIST / Sony AI 2026-08-26 MLLM 的丰富视觉语义难以直接迁移到轻量 CLIP。论文从 teacher 各层按 attention 自适应选 token，以 CKA 对齐 student 图像/文本特征，保留部署时的双塔效率。 Fidelity：公开 checkpoint 核心路径。主路径加载真实 SmolVLM teacher 与 CLIP student，在公开图像上训练 CKA projection；MovieLens/NumPy 路径仅保留为快速机制诊断。真实 checkpoint 路径使用公开图像和 SmolVLM 视觉 encoder feature，但仍未复刻论文完整 26-benchmark 训练规模、原始 teacher 配方与全量 CLIP 预训练。MovieLens proxy 仍为 diagnostic-only，不能与视觉 benchmark 混报。  multimodal-foundation-model feature-distillation compositionality cka 多模态 跨模态对齐：表征、连接器与监督 当前真实 checkpoint 路径是否训练了完整 CLIP 学生？ 没有。README 的该路径冻结 SmolVLM2 教师与 CLIP 编码器，训练匹配维度的 feature projection，并以独立验证选择权重。三 seed 留出 CKA 和邻域重合未稳定提升；退化标签的伪满分已标为无效，不能当成分类能力证据。 例如投影后的特征能运行 CKA 计算，只说明蒸馏算子链路可检查；它不是完成原论文二十六个 benchmark 的整体学生训练。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-55f94a382f44503d">当前真实 checkpoint 路径是否训练了完整 CLIP 学生？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amllmclip">MLLMCLIP: Feature-Level Distillation of MLLM for Robust Vision-Language Representations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST / Sony AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。README 的该路径冻结 SmolVLM2 教师与 CLIP 编码器，训练匹配维度的 feature projection，并以独立验证选择权重。三 seed 留出 CKA 和邻域重合未稳定提升；退化标签的伪满分已标为无效，不能当成分类能力证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如投影后的特征能运行 CKA 计算，只说明蒸馏算子链路可检查；它不是完成原论文二十六个 benchmark 的整体学生训练。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25575">原论文</a> · <a href="../../../../reproductions/2608.25575-mllmclip/">实现解读</a> · <a href="#qa-55f94a382f44503d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:wemm-embedding" data-paper-title="WeMM-Embedding: WeChat Multi-Modal Embedding Technical Report" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="WeMM-Embedding: WeChat Multi-Modal Embedding Technical Report 基础模型 WeChat Vision, Tencent 2026-08-25 不同检索任务通常维护独立的文本、图像、视频或文档 encoder。WeMM 把任意交错多模态输入映射到同一空间：第一阶段用数亿 pair 做大规模 alignment；第二阶段加入精选 relevance、细粒度监督和跨尺度知识迁移，并用 Matryoshka 表征支持按成本选择输出维度。 Fidelity：核心机制复现。本地执行两阶段跨模态对齐、cross-scale teacher refinement 与 Matryoshka 截断评测；未冒充 2B/4B/9B checkpoint 训练。没有加载原始大 checkpoint 或私有多模态 pair；公开 MovieLens 的内容/协同视图只验证共享空间、两阶段 refinement 与截断维度机制，不代表 MMEB-v2 或微信业务结果复刻。本地对照口径：基线为第一阶段共享空间；实验组加入 relevance/cross-scale teacher refinement。  multimodal-foundation-model embedding retrieval matryoshka-representation 多模态 跨模态对齐：表征、连接器与监督 WeMM 的交错多模态输入与单一图片向量有什么区别？ 一个输入可以包含文本、图像、视频或文档片段及其交错关系，再被映射为统一检索表示。目标不仅是给每种媒体单独建索引，还要表达组合输入的语义；统一空间并不意味着任意模态组合都无需训练或无需单独验证。 例如查询可以同时含产品照片和“找同款但蓝色”的文本，组合语义不同于只检索照片或只检索颜色词。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<span id="paper-foundation-models-wemm-embedding-30d32b14" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ca5d1f605b157f3e">WeMM 的交错多模态输入与单一图片向量有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Awemm-embedding">WeMM-Embedding: WeChat Multi-Modal Embedding Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · WeChat Vision, Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一个输入可以包含文本、图像、视频或文档片段及其交错关系，再被映射为统一检索表示。目标不仅是给每种媒体单独建索引，还要表达组合输入的语义；统一空间并不意味着任意模态组合都无需训练或无需单独验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如查询可以同时含产品照片和“找同款但蓝色”的文本，组合语义不同于只检索照片或只检索颜色词。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24053">原论文</a> · <a href="../../../../reproductions/2608.24053-wemm-embedding/">实现解读</a> · <a href="#qa-ca5d1f605b157f3e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:wemm-embedding" data-paper-title="WeMM-Embedding: WeChat Multi-Modal Embedding Technical Report" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="WeMM-Embedding: WeChat Multi-Modal Embedding Technical Report 基础模型 WeChat Vision, Tencent 2026-08-25 不同检索任务通常维护独立的文本、图像、视频或文档 encoder。WeMM 把任意交错多模态输入映射到同一空间：第一阶段用数亿 pair 做大规模 alignment；第二阶段加入精选 relevance、细粒度监督和跨尺度知识迁移，并用 Matryoshka 表征支持按成本选择输出维度。 Fidelity：核心机制复现。本地执行两阶段跨模态对齐、cross-scale teacher refinement 与 Matryoshka 截断评测；未冒充 2B/4B/9B checkpoint 训练。没有加载原始大 checkpoint 或私有多模态 pair；公开 MovieLens 的内容/协同视图只验证共享空间、两阶段 refinement 与截断维度机制，不代表 MMEB-v2 或微信业务结果复刻。本地对照口径：基线为第一阶段共享空间；实验组加入 relevance/cross-scale teacher refinement。  multimodal-foundation-model embedding retrieval matryoshka-representation 多模态 跨模态对齐：表征、连接器与监督 WeMM 为什么先做大规模 alignment，再引入精选 relevance 与跨尺度蒸馏？ 第一阶段先建立多模态共享空间，第二阶段再用更精细的相关性监督修正“内容相似但不满足查询”的情况。跨尺度蒸馏与 Matryoshka 表征让不同输出尺寸承接语义结构；两阶段承担不同角色，不能把向量相近直接解释为业务相关或答案正确。 例如一张红鞋图与“红色物品”很相似，但“适合雨天的鞋”还需要用途相关性；精选监督进一步约束这种差别。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-7d696f2db780b54a">WeMM 为什么先做大规模 alignment，再引入精选 relevance 与跨尺度蒸馏？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Awemm-embedding">WeMM-Embedding: WeChat Multi-Modal Embedding Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · WeChat Vision, Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>第一阶段先建立多模态共享空间，第二阶段再用更精细的相关性监督修正“内容相似但不满足查询”的情况。跨尺度蒸馏与 Matryoshka 表征让不同输出尺寸承接语义结构；两阶段承担不同角色，不能把向量相近直接解释为业务相关或答案正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一张红鞋图与“红色物品”很相似，但“适合雨天的鞋”还需要用途相关性；精选监督进一步约束这种差别。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24053">原论文</a> · <a href="../../../../reproductions/2608.24053-wemm-embedding/">实现解读</a> · <a href="#qa-7d696f2db780b54a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:wemm-embedding" data-paper-title="WeMM-Embedding: WeChat Multi-Modal Embedding Technical Report" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="WeMM-Embedding: WeChat Multi-Modal Embedding Technical Report 基础模型 WeChat Vision, Tencent 2026-08-25 不同检索任务通常维护独立的文本、图像、视频或文档 encoder。WeMM 把任意交错多模态输入映射到同一空间：第一阶段用数亿 pair 做大规模 alignment；第二阶段加入精选 relevance、细粒度监督和跨尺度知识迁移，并用 Matryoshka 表征支持按成本选择输出维度。 Fidelity：核心机制复现。本地执行两阶段跨模态对齐、cross-scale teacher refinement 与 Matryoshka 截断评测；未冒充 2B/4B/9B checkpoint 训练。没有加载原始大 checkpoint 或私有多模态 pair；公开 MovieLens 的内容/协同视图只验证共享空间、两阶段 refinement 与截断维度机制，不代表 MMEB-v2 或微信业务结果复刻。本地对照口径：基线为第一阶段共享空间；实验组加入 relevance/cross-scale teacher refinement。  multimodal-foundation-model embedding retrieval matryoshka-representation 多模态 跨模态对齐：表征、连接器与监督 WeMM对多个Matryoshka尺寸做跨尺度KD，与只监督最大尺寸有什么不同？ 公式对不同学生尺度分别计算教师到学生的KL再求和，使各输出尺寸都收到蒸馏信号。只训练最大尺寸没有同样显式约束较短表示。多个尺寸共享语义目标，不意味着质量完全相同或任意截断都合法；应按规定尺寸分别评估成本与检索质量。 教学例子：完整向量对齐教师，并不能单凭这一点保证前半段也好用；多尺度目标会另外检查短表示对应的预测分布。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1adb4bf127b3b1b7">WeMM对多个Matryoshka尺寸做跨尺度KD，与只监督最大尺寸有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Awemm-embedding">WeMM-Embedding: WeChat Multi-Modal Embedding Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · WeChat Vision, Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>公式对不同学生尺度分别计算教师到学生的KL再求和，使各输出尺寸都收到蒸馏信号。只训练最大尺寸没有同样显式约束较短表示。多个尺寸共享语义目标，不意味着质量完全相同或任意截断都合法；应按规定尺寸分别评估成本与检索质量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>完整向量对齐教师，并不能单凭这一点保证前半段也好用；多尺度目标会另外检查短表示对应的预测分布。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24053">原论文</a> · <a href="../../../../reproductions/2608.24053-wemm-embedding/">实现解读</a> · <a href="#qa-1adb4bf127b3b1b7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:wemm-embedding" data-paper-title="WeMM-Embedding: WeChat Multi-Modal Embedding Technical Report" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="WeMM-Embedding: WeChat Multi-Modal Embedding Technical Report 基础模型 WeChat Vision, Tencent 2026-08-25 不同检索任务通常维护独立的文本、图像、视频或文档 encoder。WeMM 把任意交错多模态输入映射到同一空间：第一阶段用数亿 pair 做大规模 alignment；第二阶段加入精选 relevance、细粒度监督和跨尺度知识迁移，并用 Matryoshka 表征支持按成本选择输出维度。 Fidelity：核心机制复现。本地执行两阶段跨模态对齐、cross-scale teacher refinement 与 Matryoshka 截断评测；未冒充 2B/4B/9B checkpoint 训练。没有加载原始大 checkpoint 或私有多模态 pair；公开 MovieLens 的内容/协同视图只验证共享空间、两阶段 refinement 与截断维度机制，不代表 MMEB-v2 或微信业务结果复刻。本地对照口径：基线为第一阶段共享空间；实验组加入 relevance/cross-scale teacher refinement。  multimodal-foundation-model embedding retrieval matryoshka-representation 多模态 跨模态对齐：表征、连接器与监督 本地 MovieLens 的 Matryoshka 结果能替代微信线上 A/B 吗？ 不能。本地以公开内容与协同视图验证共享空间、精炼与截断维度，没有加载原始大 checkpoint 或私有多模态 pair。原文 MMEB 与微信线上实验属于作者系统证据，本地小维度推荐代理只说明对应数据流，不能作为业务复刻或同表排名。 例如四维与十六维代理向量的 Recall 可比较本地机制，却不能推算视频号流量上的收益百分点。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1b68c75f5ea78fa1">本地 MovieLens 的 Matryoshka 结果能替代微信线上 A/B 吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Awemm-embedding">WeMM-Embedding: WeChat Multi-Modal Embedding Technical Report</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · WeChat Vision, Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。本地以公开内容与协同视图验证共享空间、精炼与截断维度，没有加载原始大 checkpoint 或私有多模态 pair。原文 MMEB 与微信线上实验属于作者系统证据，本地小维度推荐代理只说明对应数据流，不能作为业务复刻或同表排名。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如四维与十六维代理向量的 Recall 可比较本地机制，却不能推算视频号流量上的收益百分点。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24053">原论文</a> · <a href="../../../../reproductions/2608.24053-wemm-embedding/">实现解读</a> · <a href="#qa-1b68c75f5ea78fa1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gas" data-paper-title="Generation as Auxiliary Supervision: Enhancing Visual Understanding at Zero Inference Overhead via Decoupled Embedding Prediction" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Generation as Auxiliary Supervision: Enhancing Visual Understanding at Zero Inference Overhead via Decoupled Embedding Prediction 基础模型 ByteDance 2026-08-12 常规 MLLM 只用文本 next-token loss，视觉结构只能被语言间接监督；统一理解/生成模型又会把生成参数和开销留到部署阶段。GAS 把生成改成纯训练期辅助任务：理解分支与生成分支共享较低层视觉路径，上层 Transformer 参数解耦；生成分支在与 LLM 输入相同的连续视觉空间自回归预测目标图像 embedding。这样生成梯度能改善共享视觉表征，又不会直接改写理解上层，部署时可整条删除。 Fidelity：核心机制复现。本地真实训练共享视觉 trunk、独立 MoT 生成上层、连续 Next Embedding Prediction（NEP）与 EMA target；未复刻 2B/4B Qwen3-VL、10M 生成数据和 32-GPU 两阶段训练。本地用水平镜像后的同类目标图像构造高度相关的生成任务，并在连续 patch embedding 空间执行 shifted cosine NEP；保留 EMA、渐增、分支隔离与推理删除机制。结果只说明小规模公开数据上的机制可执行，不能与论文 10M 生成样本和 2B/4B benchmark 数字直接比较。  multimodal generation-guided-training next-embedding-prediction 多模态 跨模态对齐：表征、连接器与监督 GAS 预测的 next embedding 是离散图像 token 吗？ 它预测与语言模型视觉输入相同空间中的连续视觉 embedding，以余弦目标对齐 EMA 投影得到的目标表示，而不是训练离散图像码本分类器。生成任务服务于共享视觉表征的训练，主要目标仍是增强理解，部署并不要求真的生成图像。 例如目标 patch 用一个连续向量表示，生成头预测其方向；损失比较两个向量，而不是在上万个图像词表项中选编号。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<span id="paper-foundation-models-gas-1fb6a8b0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a203eea136c296da">GAS 预测的 next embedding 是离散图像 token 吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agas">Generation as Auxiliary Supervision: Enhancing Visual Understanding at Zero Inference Overhead via Decoupled Embedding Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它预测与语言模型视觉输入相同空间中的连续视觉 embedding，以余弦目标对齐 EMA 投影得到的目标表示，而不是训练离散图像码本分类器。生成任务服务于共享视觉表征的训练，主要目标仍是增强理解，部署并不要求真的生成图像。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如目标 patch 用一个连续向量表示，生成头预测其方向；损失比较两个向量，而不是在上万个图像词表项中选编号。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.12209">原论文</a> · <a href="../../../../reproductions/2608.12209-gas/">实现解读</a> · <a href="#qa-a203eea136c296da">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gas" data-paper-title="Generation as Auxiliary Supervision: Enhancing Visual Understanding at Zero Inference Overhead via Decoupled Embedding Prediction" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Generation as Auxiliary Supervision: Enhancing Visual Understanding at Zero Inference Overhead via Decoupled Embedding Prediction 基础模型 ByteDance 2026-08-12 常规 MLLM 只用文本 next-token loss，视觉结构只能被语言间接监督；统一理解/生成模型又会把生成参数和开销留到部署阶段。GAS 把生成改成纯训练期辅助任务：理解分支与生成分支共享较低层视觉路径，上层 Transformer 参数解耦；生成分支在与 LLM 输入相同的连续视觉空间自回归预测目标图像 embedding。这样生成梯度能改善共享视觉表征，又不会直接改写理解上层，部署时可整条删除。 Fidelity：核心机制复现。本地真实训练共享视觉 trunk、独立 MoT 生成上层、连续 Next Embedding Prediction（NEP）与 EMA target；未复刻 2B/4B Qwen3-VL、10M 生成数据和 32-GPU 两阶段训练。本地用水平镜像后的同类目标图像构造高度相关的生成任务，并在连续 patch embedding 空间执行 shifted cosine NEP；保留 EMA、渐增、分支隔离与推理删除机制。结果只说明小规模公开数据上的机制可执行，不能与论文 10M 生成样本和 2B/4B benchmark 数字直接比较。  multimodal generation-guided-training next-embedding-prediction 多模态 跨模态对齐：表征、连接器与监督 GAS 的生成辅助监督为什么可以在部署时整条删除？ 辅助生成分支只在训练期预测连续视觉 embedding，与理解分支共享较低层视觉路径，因此它的梯度能改善共享表示。上层生成参数与理解上层解耦，推理输出不依赖该辅助分支；删除的是额外路径，而训练得到的共享参数仍被保留。 例如训练时同时要求理解图片并预测目标图像特征；上线只回答图像问题，保留被训练过的共享视觉部分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-4f6e57e97260ca61">GAS 的生成辅助监督为什么可以在部署时整条删除？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agas">Generation as Auxiliary Supervision: Enhancing Visual Understanding at Zero Inference Overhead via Decoupled Embedding Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>辅助生成分支只在训练期预测连续视觉 embedding，与理解分支共享较低层视觉路径，因此它的梯度能改善共享表示。上层生成参数与理解上层解耦，推理输出不依赖该辅助分支；删除的是额外路径，而训练得到的共享参数仍被保留。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如训练时同时要求理解图片并预测目标图像特征；上线只回答图像问题，保留被训练过的共享视觉部分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.12209">原论文</a> · <a href="../../../../reproductions/2608.12209-gas/">实现解读</a> · <a href="#qa-4f6e57e97260ca61">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gas" data-paper-title="Generation as Auxiliary Supervision: Enhancing Visual Understanding at Zero Inference Overhead via Decoupled Embedding Prediction" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Generation as Auxiliary Supervision: Enhancing Visual Understanding at Zero Inference Overhead via Decoupled Embedding Prediction 基础模型 ByteDance 2026-08-12 常规 MLLM 只用文本 next-token loss，视觉结构只能被语言间接监督；统一理解/生成模型又会把生成参数和开销留到部署阶段。GAS 把生成改成纯训练期辅助任务：理解分支与生成分支共享较低层视觉路径，上层 Transformer 参数解耦；生成分支在与 LLM 输入相同的连续视觉空间自回归预测目标图像 embedding。这样生成梯度能改善共享视觉表征，又不会直接改写理解上层，部署时可整条删除。 Fidelity：核心机制复现。本地真实训练共享视觉 trunk、独立 MoT 生成上层、连续 Next Embedding Prediction（NEP）与 EMA target；未复刻 2B/4B Qwen3-VL、10M 生成数据和 32-GPU 两阶段训练。本地用水平镜像后的同类目标图像构造高度相关的生成任务，并在连续 patch embedding 空间执行 shifted cosine NEP；保留 EMA、渐增、分支隔离与推理删除机制。结果只说明小规模公开数据上的机制可执行，不能与论文 10M 生成样本和 2B/4B benchmark 数字直接比较。  multimodal generation-guided-training next-embedding-prediction 多模态 跨模态对齐：表征、连接器与监督 GAS的next-embedding prediction与把当前patch直接重建回自身，有何条件信息差别？ NEP按自回归次序用上下文和此前视觉embedding预测下一位置，目标来自EMA投影的视觉表示。若把同位置目标直接作为当前输入再重建，就改变了可见信息和预测任务，可能退化成复制。训练辅助分支是否能删除是另一问题，不能替代移位预测的合同。 教学例子：预测第i个视觉embedding时只给此前序列与允许的上下文；不能先输入第i个目标向量，再把复制正确当预测成功。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ea7ba395bdabb73a">GAS的next-embedding prediction与把当前patch直接重建回自身，有何条件信息差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agas">Generation as Auxiliary Supervision: Enhancing Visual Understanding at Zero Inference Overhead via Decoupled Embedding Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>NEP按自回归次序用上下文和此前视觉embedding预测下一位置，目标来自EMA投影的视觉表示。若把同位置目标直接作为当前输入再重建，就改变了可见信息和预测任务，可能退化成复制。训练辅助分支是否能删除是另一问题，不能替代移位预测的合同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>预测第i个视觉embedding时只给此前序列与允许的上下文；不能先输入第i个目标向量，再把复制正确当预测成功。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.12209">原论文</a> · <a href="../../../../reproductions/2608.12209-gas/">实现解读</a> · <a href="#qa-ea7ba395bdabb73a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gas" data-paper-title="Generation as Auxiliary Supervision: Enhancing Visual Understanding at Zero Inference Overhead via Decoupled Embedding Prediction" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Generation as Auxiliary Supervision: Enhancing Visual Understanding at Zero Inference Overhead via Decoupled Embedding Prediction 基础模型 ByteDance 2026-08-12 常规 MLLM 只用文本 next-token loss，视觉结构只能被语言间接监督；统一理解/生成模型又会把生成参数和开销留到部署阶段。GAS 把生成改成纯训练期辅助任务：理解分支与生成分支共享较低层视觉路径，上层 Transformer 参数解耦；生成分支在与 LLM 输入相同的连续视觉空间自回归预测目标图像 embedding。这样生成梯度能改善共享视觉表征，又不会直接改写理解上层，部署时可整条删除。 Fidelity：核心机制复现。本地真实训练共享视觉 trunk、独立 MoT 生成上层、连续 Next Embedding Prediction（NEP）与 EMA target；未复刻 2B/4B Qwen3-VL、10M 生成数据和 32-GPU 两阶段训练。本地用水平镜像后的同类目标图像构造高度相关的生成任务，并在连续 patch embedding 空间执行 shifted cosine NEP；保留 EMA、渐增、分支隔离与推理删除机制。结果只说明小规模公开数据上的机制可执行，不能与论文 10M 生成样本和 2B/4B benchmark 数字直接比较。  multimodal generation-guided-training next-embedding-prediction 多模态 跨模态对齐：表征、连接器与监督 为什么检查“部署参数为零增量”还要确认分支依赖？ 只有理解前向不再读取生成上层、vision head 或 EMA projector，删除它们才不会改变部署图。训练期 NEP 要保留移位的自回归预测、EMA 目标与分支隔离；本地镜像目标的小规模诊断不能验证原文大规模生成数据的能力收益。 例如误把生成分支的中间输出接回理解输出，即使声称删掉参数，实际推理仍依赖它，便不满足可删除辅助分支的设定。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1371d6b9ed359eda">为什么检查“部署参数为零增量”还要确认分支依赖？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agas">Generation as Auxiliary Supervision: Enhancing Visual Understanding at Zero Inference Overhead via Decoupled Embedding Prediction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只有理解前向不再读取生成上层、vision head 或 EMA projector，删除它们才不会改变部署图。训练期 NEP 要保留移位的自回归预测、EMA 目标与分支隔离；本地镜像目标的小规模诊断不能验证原文大规模生成数据的能力收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如误把生成分支的中间输出接回理解输出，即使声称删掉参数，实际推理仍依赖它，便不满足可删除辅助分支的设定。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.12209">原论文</a> · <a href="../../../../reproductions/2608.12209-gas/">实现解读</a> · <a href="#qa-1371d6b9ed359eda">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:physics-mm-pretraining" data-paper-title="Towards Physics of Multimodal Pretraining: Knowledge Flow, Modality Synergy, Early Unification, and Recipes" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Towards Physics of Multimodal Pretraining: Knowledge Flow, Modality Synergy, Early Unification, and Recipes 基础模型 Meta 2026-08-05 用受控实验刻画模态知识流、协同/竞争、早期统一和共享 attention+norm/模态专属 FFN 配方。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 single-modality representation，实验组为 physics-mm-pretraining；单 seed 变化为 +0.00% 个百分点。  多模态基础模型 预训练与数据 多模态 跨模态对齐：表征、连接器与监督 这项研究中的“模态协同”是否只是同时加入更多数据？ 研究关注一种模态的训练是否改善另一种模态所需的知识与表征，并通过受控设置区别协同与竞争。单纯增加样本量会同时改变计算、数据覆盖与目标权重，不能据此识别知识流；需要固定关键条件比较模态组合和架构安排。 例如加入图像训练后文本推理提升，仍需检查总 token 与计算是否匹配，才能讨论提升是否来自跨模态共享知识。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<span id="paper-foundation-models-physics-mm-pretraining-bcf29586" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-bdcb4cabe9c03d38">这项研究中的“模态协同”是否只是同时加入更多数据？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aphysics-mm-pretraining">Towards Physics of Multimodal Pretraining: Knowledge Flow, Modality Synergy, Early Unification, and Recipes</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>研究关注一种模态的训练是否改善另一种模态所需的知识与表征，并通过受控设置区别协同与竞争。单纯增加样本量会同时改变计算、数据覆盖与目标权重，不能据此识别知识流；需要固定关键条件比较模态组合和架构安排。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如加入图像训练后文本推理提升，仍需检查总 token 与计算是否匹配，才能讨论提升是否来自跨模态共享知识。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05000">原论文</a> · <a href="../../../../reproductions/2608.05000-physics-mm-pretraining/">实现解读</a> · <a href="#qa-bdcb4cabe9c03d38">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:physics-mm-pretraining" data-paper-title="Towards Physics of Multimodal Pretraining: Knowledge Flow, Modality Synergy, Early Unification, and Recipes" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Towards Physics of Multimodal Pretraining: Knowledge Flow, Modality Synergy, Early Unification, and Recipes 基础模型 Meta 2026-08-05 用受控实验刻画模态知识流、协同/竞争、早期统一和共享 attention+norm/模态专属 FFN 配方。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 single-modality representation，实验组为 physics-mm-pretraining；单 seed 变化为 +0.00% 个百分点。  多模态基础模型 预训练与数据 多模态 跨模态对齐：表征、连接器与监督 共享 attention 与 norm、保留模态专属 FFN，分别在控制什么？ 共享部分让不同模态在相同交互路径上交换信息，专属 FFN 则保留各自变换与容量，缓解完全共享时的竞争。要判断知识协同而非资源变化，必须控制数据、目标权重和预算；联合训练的总分上升，并不说明每个模态都同样受益。 例如文字与图像共同参与注意力，但各走自己的 FFN；这像共享讨论渠道而保留各自加工方式，需分别测两类任务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f2bb66ec4c595c03">共享 attention 与 norm、保留模态专属 FFN，分别在控制什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aphysics-mm-pretraining">Towards Physics of Multimodal Pretraining: Knowledge Flow, Modality Synergy, Early Unification, and Recipes</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共享部分让不同模态在相同交互路径上交换信息，专属 FFN 则保留各自变换与容量，缓解完全共享时的竞争。要判断知识协同而非资源变化，必须控制数据、目标权重和预算；联合训练的总分上升，并不说明每个模态都同样受益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如文字与图像共同参与注意力，但各走自己的 FFN；这像共享讨论渠道而保留各自加工方式，需分别测两类任务。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05000">原论文</a> · <a href="../../../../reproductions/2608.05000-physics-mm-pretraining/">实现解读</a> · <a href="#qa-f2bb66ec4c595c03">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:physics-mm-pretraining" data-paper-title="Towards Physics of Multimodal Pretraining: Knowledge Flow, Modality Synergy, Early Unification, and Recipes" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Towards Physics of Multimodal Pretraining: Knowledge Flow, Modality Synergy, Early Unification, and Recipes 基础模型 Meta 2026-08-05 用受控实验刻画模态知识流、协同/竞争、早期统一和共享 attention+norm/模态专属 FFN 配方。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 single-modality representation，实验组为 physics-mm-pretraining；单 seed 变化为 +0.00% 个百分点。  多模态基础模型 预训练与数据 多模态 跨模态对齐：表征、连接器与监督 这项研究的早期联合训练，与分别训练各模态后只把最终向量拼接，有何知识交换区别？ 联合训练让不同任务的损失作用于共享交互参数，因而可以研究跨模态梯度带来的协同或竞争。训练后拼接独立表示只改变下游可见特征，不会倒推产生同样的共享预训练过程。两者即使使用相同数据量，也不能据最终总分直接认定知识流相同。 教学例子：文本任务更新了共享attention后再测视觉任务，是跨任务影响；把两个已冻结向量并排放置并未发生这次更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-464a2649c054e233">这项研究的早期联合训练，与分别训练各模态后只把最终向量拼接，有何知识交换区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aphysics-mm-pretraining">Towards Physics of Multimodal Pretraining: Knowledge Flow, Modality Synergy, Early Unification, and Recipes</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>联合训练让不同任务的损失作用于共享交互参数，因而可以研究跨模态梯度带来的协同或竞争。训练后拼接独立表示只改变下游可见特征，不会倒推产生同样的共享预训练过程。两者即使使用相同数据量，也不能据最终总分直接认定知识流相同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>文本任务更新了共享attention后再测视觉任务，是跨任务影响；把两个已冻结向量并排放置并未发生这次更新。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05000">原论文</a> · <a href="../../../../reproductions/2608.05000-physics-mm-pretraining/">实现解读</a> · <a href="#qa-464a2649c054e233">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:physics-mm-pretraining" data-paper-title="Towards Physics of Multimodal Pretraining: Knowledge Flow, Modality Synergy, Early Unification, and Recipes" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Towards Physics of Multimodal Pretraining: Knowledge Flow, Modality Synergy, Early Unification, and Recipes 基础模型 Meta 2026-08-05 用受控实验刻画模态知识流、协同/竞争、早期统一和共享 attention+norm/模态专属 FFN 配方。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 single-modality representation，实验组为 physics-mm-pretraining；单 seed 变化为 +0.00% 个百分点。  多模态基础模型 预训练与数据 多模态 跨模态对齐：表征、连接器与监督 联合目标的权重为什么属于复现契约，而不是无关超参？ 总损失包含文本、理解与生成三项，两个系数改变各任务对共享参数的梯度贡献，从而改变协同或竞争条件。只验证小套件的数据流可执行不能等价于训练 13.5B MoE 与两万亿 token；本地单 seed 满分也不构成规模结论。 例如把生成权重增大十倍会改变共享层受到的优化压力；即使三项名称不变，也不是相同训练配方。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1caaede64820e758">联合目标的权重为什么属于复现契约，而不是无关超参？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aphysics-mm-pretraining">Towards Physics of Multimodal Pretraining: Knowledge Flow, Modality Synergy, Early Unification, and Recipes</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>总损失包含文本、理解与生成三项，两个系数改变各任务对共享参数的梯度贡献，从而改变协同或竞争条件。只验证小套件的数据流可执行不能等价于训练 13.5B MoE 与两万亿 token；本地单 seed 满分也不构成规模结论。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把生成权重增大十倍会改变共享层受到的优化压力；即使三项名称不变，也不是相同训练配方。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05000">原论文</a> · <a href="../../../../reproductions/2608.05000-physics-mm-pretraining/">实现解读</a> · <a href="#qa-1caaede64820e758">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:retoken" data-paper-title="ReToken: One Token to Improve Vision–Language Models for Visual Retrieval" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="ReToken: One Token to Improve Vision–Language Models for Visual Retrieval 基础模型 UIUC / Microsoft Research / Google DeepMind 2026-07-30 常规 VLM 检索需要先用外部 retriever 找图，再把入选图重新编码，无法直接复用预填充的视觉 KV cache。ReToken 在输入中增加一个可学习 token，让它在最后一层 value projection 空间与每张图的平均 value 向量打分；只训练该 token 和一张投影矩阵，以 class-balanced BCE 监督相关/无关图，VLM 默认冻结。 Fidelity: 核心机制复现。实际训练单个 retrieval target、value-space projection 与稀疏 cache 选择，并接入 LLM evolve；本地文本实验不冒充完整 VLM。本地没有运行冻结大 VLM、MIRAGE 图文监督和两小时视频；文本 token cache 只复现论文决定性的“单 retrieval target + value-space 打分 + 稀疏选择”机制，不能与论文视觉 benchmark 数字直接比较。本地对照口径：基线为同预算 dense LLaMA，实验组为 ReToken value-cache Top-K；相对基线 PPL +3.70%（变差）。  vision-language-model visual-retrieval kv-cache sparse-attention 多模态 跨模态对齐：表征、连接器与监督 ReToken的可学习RET token是一张图片的固定ID吗？ 不是。它是输入中的一个可学习检索标记，经过VLM上下文处理后产生当前请求的隐藏状态，再投影后与各图的平均value表示匹配。共享的是标记参数，不意味着所有请求的隐藏状态或相关图片都相同；它也不是把整套图片目录装进一个ID。 教学例子：两次请求使用同一个RET标记，但问题内容不同，其上下文化表示可不同，因而可以给同一组图片不同相关分数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<span id="paper-foundation-models-retoken-1f7ac688" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-925d7e6a3ddb726f">ReToken的可学习RET token是一张图片的固定ID吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aretoken">ReToken: One Token to Improve Vision–Language Models for Visual Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UIUC / Microsoft Research / Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。它是输入中的一个可学习检索标记，经过VLM上下文处理后产生当前请求的隐藏状态，再投影后与各图的平均value表示匹配。共享的是标记参数，不意味着所有请求的隐藏状态或相关图片都相同；它也不是把整套图片目录装进一个ID。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两次请求使用同一个RET标记，但问题内容不同，其上下文化表示可不同，因而可以给同一组图片不同相关分数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28627">原论文</a> · <a href="../../../../reproductions/2607.28627-retoken/">实现解读</a> · <a href="#qa-925d7e6a3ddb726f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:retoken" data-paper-title="ReToken: One Token to Improve Vision–Language Models for Visual Retrieval" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="ReToken: One Token to Improve Vision–Language Models for Visual Retrieval 基础模型 UIUC / Microsoft Research / Google DeepMind 2026-07-30 常规 VLM 检索需要先用外部 retriever 找图，再把入选图重新编码，无法直接复用预填充的视觉 KV cache。ReToken 在输入中增加一个可学习 token，让它在最后一层 value projection 空间与每张图的平均 value 向量打分；只训练该 token 和一张投影矩阵，以 class-balanced BCE 监督相关/无关图，VLM 默认冻结。 Fidelity: 核心机制复现。实际训练单个 retrieval target、value-space projection 与稀疏 cache 选择，并接入 LLM evolve；本地文本实验不冒充完整 VLM。本地没有运行冻结大 VLM、MIRAGE 图文监督和两小时视频；文本 token cache 只复现论文决定性的“单 retrieval target + value-space 打分 + 稀疏选择”机制，不能与论文视觉 benchmark 数字直接比较。本地对照口径：基线为同预算 dense LLaMA，实验组为 ReToken value-cache Top-K；相对基线 PPL +3.70%（变差）。  vision-language-model visual-retrieval kv-cache sparse-attention 多模态 跨模态对齐：表征、连接器与监督 ReToken 为什么把检索分数算在最后一层 value 空间？ 预填充后的视觉 KV 已包含每张图的表示，在同一 value 空间读取相似度就有机会复用缓存，而无需重新运行外部检索器并重编码图片。可学习检索 token 与投影负责适配相关性，冻结 VLM 并不表示检索头无需监督或能直接泛化所有任务。 例如十张图已预填充到缓存，新增问题先用检索 token 与各图平均 value 打分，再选择相关图继续使用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-ac564f018c0c2564">ReToken 为什么把检索分数算在最后一层 value 空间？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aretoken">ReToken: One Token to Improve Vision–Language Models for Visual Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UIUC / Microsoft Research / Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>预填充后的视觉 KV 已包含每张图的表示，在同一 value 空间读取相似度就有机会复用缓存，而无需重新运行外部检索器并重编码图片。可学习检索 token 与投影负责适配相关性，冻结 VLM 并不表示检索头无需监督或能直接泛化所有任务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如十张图已预填充到缓存，新增问题先用检索 token 与各图平均 value 打分，再选择相关图继续使用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28627">原论文</a> · <a href="../../../../reproductions/2607.28627-retoken/">实现解读</a> · <a href="#qa-ac564f018c0c2564">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:retoken" data-paper-title="ReToken: One Token to Improve Vision–Language Models for Visual Retrieval" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="ReToken: One Token to Improve Vision–Language Models for Visual Retrieval 基础模型 UIUC / Microsoft Research / Google DeepMind 2026-07-30 常规 VLM 检索需要先用外部 retriever 找图，再把入选图重新编码，无法直接复用预填充的视觉 KV cache。ReToken 在输入中增加一个可学习 token，让它在最后一层 value projection 空间与每张图的平均 value 向量打分；只训练该 token 和一张投影矩阵，以 class-balanced BCE 监督相关/无关图，VLM 默认冻结。 Fidelity: 核心机制复现。实际训练单个 retrieval target、value-space projection 与稀疏 cache 选择，并接入 LLM evolve；本地文本实验不冒充完整 VLM。本地没有运行冻结大 VLM、MIRAGE 图文监督和两小时视频；文本 token cache 只复现论文决定性的“单 retrieval target + value-space 打分 + 稀疏选择”机制，不能与论文视觉 benchmark 数字直接比较。本地对照口径：基线为同预算 dense LLaMA，实验组为 ReToken value-cache Top-K；相对基线 PPL +3.70%（变差）。  vision-language-model visual-retrieval kv-cache sparse-attention 多模态 跨模态对齐：表征、连接器与监督 ReToken的逐图BCE监督，与要求唯一相关图的候选softmax，有何标签假设差别？ BCE对每张图的相关或无关标签分别计算损失，并用类别权重调节两类贡献；它不要求所有图的sigmoid分数相加为一。单正例softmax则让候选竞争一份概率质量。不能在存在多张相关图时，未经说明只保留一个赢家并沿用原监督解释。 教学例子：一个问题可需要两张图的证据，二者都可标为相关；不必为了凑成唯一winner而把其中一张改成负例。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-3387fd902dfccf78">ReToken的逐图BCE监督，与要求唯一相关图的候选softmax，有何标签假设差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aretoken">ReToken: One Token to Improve Vision–Language Models for Visual Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UIUC / Microsoft Research / Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>BCE对每张图的相关或无关标签分别计算损失，并用类别权重调节两类贡献；它不要求所有图的sigmoid分数相加为一。单正例softmax则让候选竞争一份概率质量。不能在存在多张相关图时，未经说明只保留一个赢家并沿用原监督解释。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个问题可需要两张图的证据，二者都可标为相关；不必为了凑成唯一winner而把其中一张改成负例。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28627">原论文</a> · <a href="../../../../reproductions/2607.28627-retoken/">实现解读</a> · <a href="#qa-3387fd902dfccf78">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:retoken" data-paper-title="ReToken: One Token to Improve Vision–Language Models for Visual Retrieval" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="ReToken: One Token to Improve Vision–Language Models for Visual Retrieval 基础模型 UIUC / Microsoft Research / Google DeepMind 2026-07-30 常规 VLM 检索需要先用外部 retriever 找图，再把入选图重新编码，无法直接复用预填充的视觉 KV cache。ReToken 在输入中增加一个可学习 token，让它在最后一层 value projection 空间与每张图的平均 value 向量打分；只训练该 token 和一张投影矩阵，以 class-balanced BCE 监督相关/无关图，VLM 默认冻结。 Fidelity: 核心机制复现。实际训练单个 retrieval target、value-space projection 与稀疏 cache 选择，并接入 LLM evolve；本地文本实验不冒充完整 VLM。本地没有运行冻结大 VLM、MIRAGE 图文监督和两小时视频；文本 token cache 只复现论文决定性的“单 retrieval target + value-space 打分 + 稀疏选择”机制，不能与论文视觉 benchmark 数字直接比较。本地对照口径：基线为同预算 dense LLaMA，实验组为 ReToken value-cache Top-K；相对基线 PPL +3.70%（变差）。  vision-language-model visual-retrieval kv-cache sparse-attention 多模态 跨模态对齐：表征、连接器与监督 本地文本 cache 实验与论文视觉训练之间缺少哪些条件？ 本地在 WikiText-2 训练单检索目标、value 打分与稀疏选择，未运行冻结大 VLM、MIRAGE 图文监督或长视频。短前缀还不足固定 Top-K，保留率会受前缀长度影响；PPL 退化必须按文本机制实验报告，不能改写为视觉检索增益。 例如只有三个历史 token 时设 Top-K 为十并不会产生十个可选项；跨长度平均保留率因此不等于固定压缩比例。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3cc4c368978edb1c">本地文本 cache 实验与论文视觉训练之间缺少哪些条件？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aretoken">ReToken: One Token to Improve Vision–Language Models for Visual Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UIUC / Microsoft Research / Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>本地在 WikiText-2 训练单检索目标、value 打分与稀疏选择，未运行冻结大 VLM、MIRAGE 图文监督或长视频。短前缀还不足固定 Top-K，保留率会受前缀长度影响；PPL 退化必须按文本机制实验报告，不能改写为视觉检索增益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只有三个历史 token 时设 Top-K 为十并不会产生十个可选项；跨长度平均保留率因此不等于固定压缩比例。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28627">原论文</a> · <a href="../../../../reproductions/2607.28627-retoken/">实现解读</a> · <a href="#qa-3cc4c368978edb1c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:mveb" data-paper-title="MVEB: Massive Video Embedding Benchmark" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="MVEB: Massive Video Embedding Benchmark 多模态大模型 Harvard University 2026-06-12 固定v1 Section3：MVEB23任务从184任务池缩减；var-length fps2/cap64frames，固定帧模型遵循其训练配置，音频按model采样率/长度；无per-task finetune。分类8shot frozen logistic probe，retrieval cosine/nDCG10，VCQA候选池accuracy，视频/音频版本配对且只跑模型支持modality。 成本过高，不复现（审查 DONE）。33个公开checkpoint约200M–10.7B，23主任务及184池，多模型视频+音频/8方向矩阵；Table1单H100测LCO7B：MVEB31.9h、MVEB+302.7h。远超单A100/A30短时预算，不下载模型或视频、不构造假的通用指标代理。本轮仅核查论文身份、合作机构、方法/资源/许可证与成本，收录资料和原图。没有把通用聚合器或字段检查包装为官方benchmark接口；没有模型调用、训练或正式指标。  多模态表征 视频嵌入评测 多模态 跨模态对齐：表征、连接器与监督 MVEB 的视频问答评测为什么仍属于 embedding 评测？ 其 VCQA 把候选回答放入检索池，用视频与候选表示的匹配选择答案，统计候选池准确率，并非让生成模型自由回答。评测时冻结 embedding 模型，分类等任务也使用指定探针，因此不同任务的输出形式与指标不能混成同一种生成正确率。 例如四个候选动作描述都已给定，模型选出最相似的一项；这与自由生成动作名称后再做语言评审是不同协议。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<span id="paper-multimodal-models-mveb-9298f9f8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-bd709b40f21ee758">MVEB 的视频问答评测为什么仍属于 embedding 评测？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Amveb">MVEB: Massive Video Embedding Benchmark</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harvard University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>其 VCQA 把候选回答放入检索池，用视频与候选表示的匹配选择答案，统计候选池准确率，并非让生成模型自由回答。评测时冻结 embedding 模型，分类等任务也使用指定探针，因此不同任务的输出形式与指标不能混成同一种生成正确率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如四个候选动作描述都已给定，模型选出最相似的一项；这与自由生成动作名称后再做语言评审是不同协议。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.14958v1">原论文</a> · <a href="../../../../multimodal-models/2606.14958-mveb/">实现解读</a> · <a href="#qa-bd709b40f21ee758">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:mveb" data-paper-title="MVEB: Massive Video Embedding Benchmark" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="MVEB: Massive Video Embedding Benchmark 多模态大模型 Harvard University 2026-06-12 固定v1 Section3：MVEB23任务从184任务池缩减；var-length fps2/cap64frames，固定帧模型遵循其训练配置，音频按model采样率/长度；无per-task finetune。分类8shot frozen logistic probe，retrieval cosine/nDCG10，VCQA候选池accuracy，视频/音频版本配对且只跑模型支持modality。 成本过高，不复现（审查 DONE）。33个公开checkpoint约200M–10.7B，23主任务及184池，多模型视频+音频/8方向矩阵；Table1单H100测LCO7B：MVEB31.9h、MVEB+302.7h。远超单A100/A30短时预算，不下载模型或视频、不构造假的通用指标代理。本轮仅核查论文身份、合作机构、方法/资源/许可证与成本，收录资料和原图。没有把通用聚合器或字段检查包装为官方benchmark接口；没有模型调用、训练或正式指标。  多模态表征 视频嵌入评测 多模态 跨模态对齐：表征、连接器与监督 MVEB 比较 video-only 与 audio+video 时，为什么必须使用同一组 clip？ 否则性能差可能来自样本难度变化，而非音轨是否提供信息。配对同一视频后才能隔离模态增量；编码器保持冻结，各任务使用规定的探针或检索指标，并按模型声明处理帧数和音频。给不支持音频的模型补一个虚构分数会破坏比较。 例如同一段敲门视频分别保留和移除声音；若换成另一段更简单的视频，就无法判断增益究竟来自哪里。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-4086d8bd7c3aa807">MVEB 比较 video-only 与 audio+video 时，为什么必须使用同一组 clip？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Amveb">MVEB: Massive Video Embedding Benchmark</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harvard University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>否则性能差可能来自样本难度变化，而非音轨是否提供信息。配对同一视频后才能隔离模态增量；编码器保持冻结，各任务使用规定的探针或检索指标，并按模型声明处理帧数和音频。给不支持音频的模型补一个虚构分数会破坏比较。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一段敲门视频分别保留和移除声音；若换成另一段更简单的视频，就无法判断增益究竟来自哪里。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.14958v1">原论文</a> · <a href="../../../../multimodal-models/2606.14958-mveb/">实现解读</a> · <a href="#qa-4086d8bd7c3aa807">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:mveb" data-paper-title="MVEB: Massive Video Embedding Benchmark" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="MVEB: Massive Video Embedding Benchmark 多模态大模型 Harvard University 2026-06-12 固定v1 Section3：MVEB23任务从184任务池缩减；var-length fps2/cap64frames，固定帧模型遵循其训练配置，音频按model采样率/长度；无per-task finetune。分类8shot frozen logistic probe，retrieval cosine/nDCG10，VCQA候选池accuracy，视频/音频版本配对且只跑模型支持modality。 成本过高，不复现（审查 DONE）。33个公开checkpoint约200M–10.7B，23主任务及184池，多模型视频+音频/8方向矩阵；Table1单H100测LCO7B：MVEB31.9h、MVEB+302.7h。远超单A100/A30短时预算，不下载模型或视频、不构造假的通用指标代理。本轮仅核查论文身份、合作机构、方法/资源/许可证与成本，收录资料和原图。没有把通用聚合器或字段检查包装为官方benchmark接口；没有模型调用、训练或正式指标。  多模态表征 视频嵌入评测 多模态 跨模态对齐：表征、连接器与监督 统一把所有视频模型设为 64 帧，是否比遵循各自配置更公平？ 不一定。MVEB 对可变长模型使用 2fps 且最多 64 帧，对固定帧模型遵循其训练配置；强行统一可能偏离模型有效输入范围。公平还要求视频与音视频版本使用同一 clip，不能给不支持音频的模型虚构音视频结果。 例如一个固定八帧模型不应被硬塞六十四帧，再把失败解释为表示质量差；音视频对比也必须保持片段相同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ac8fad29eea9e7f7">统一把所有视频模型设为 64 帧，是否比遵循各自配置更公平？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Amveb">MVEB: Massive Video Embedding Benchmark</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harvard University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不一定。MVEB 对可变长模型使用 2fps 且最多 64 帧，对固定帧模型遵循其训练配置；强行统一可能偏离模型有效输入范围。公平还要求视频与音视频版本使用同一 clip，不能给不支持音频的模型虚构音视频结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个固定八帧模型不应被硬塞六十四帧，再把失败解释为表示质量差；音视频对比也必须保持片段相同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.14958v1">原论文</a> · <a href="../../../../multimodal-models/2606.14958-mveb/">实现解读</a> · <a href="#qa-ac8fad29eea9e7f7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:mveb" data-paper-title="MVEB: Massive Video Embedding Benchmark" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="MVEB: Massive Video Embedding Benchmark 多模态大模型 Harvard University 2026-06-12 固定v1 Section3：MVEB23任务从184任务池缩减；var-length fps2/cap64frames，固定帧模型遵循其训练配置，音频按model采样率/长度；无per-task finetune。分类8shot frozen logistic probe，retrieval cosine/nDCG10，VCQA候选池accuracy，视频/音频版本配对且只跑模型支持modality。 成本过高，不复现（审查 DONE）。33个公开checkpoint约200M–10.7B，23主任务及184池，多模型视频+音频/8方向矩阵；Table1单H100测LCO7B：MVEB31.9h、MVEB+302.7h。远超单A100/A30短时预算，不下载模型或视频、不构造假的通用指标代理。本轮仅核查论文身份、合作机构、方法/资源/许可证与成本，收录资料和原图。没有把通用聚合器或字段检查包装为官方benchmark接口；没有模型调用、训练或正式指标。  多模态表征 视频嵌入评测 多模态 跨模态对齐：表征、连接器与监督 本地能否用一个余弦聚合函数宣称已接入 MVEB 全部任务？ 不能。各任务使用官方规定的 evaluator，如检索 nDCG@10、聚类 V-measure、每类八样本逻辑回归和候选问答准确率，并有模态及采样约束。当前 README 只有资料与成本核查，没有模型调用或正式指标，通用字段检查不能替代任务接口。 例如检索结果必须按相关性标签算 nDCG，不能把平均余弦值改名为 MVEB 分数，也不能声称其等于问答准确率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-af25b7c17d30df09">本地能否用一个余弦聚合函数宣称已接入 MVEB 全部任务？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Amveb">MVEB: Massive Video Embedding Benchmark</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harvard University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。各任务使用官方规定的 evaluator，如检索 nDCG@10、聚类 V-measure、每类八样本逻辑回归和候选问答准确率，并有模态及采样约束。当前 README 只有资料与成本核查，没有模型调用或正式指标，通用字段检查不能替代任务接口。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如检索结果必须按相关性标签算 nDCG，不能把平均余弦值改名为 MVEB 分数，也不能声称其等于问答准确率。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.14958v1">原论文</a> · <a href="../../../../multimodal-models/2606.14958-mveb/">实现解读</a> · <a href="#qa-af25b7c17d30df09">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:naijas2st" data-paper-title="NaijaS2ST: A Multi-Accent Benchmark for Speech-to-Speech Translation in Low-Resource Nigerian Languages" data-learning-pending="false" data-level="basics" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="NaijaS2ST: A Multi-Accent Benchmark for Speech-to-Speech Translation in Low-Resource Nigerian Languages 多模态大模型 Mila - Quebec AI Institute 2026-04-17 核固定v3 Sections3–4及AppendixC：284说话人、约6K平行句、质控后约269h；5shot来自DEV，方向分开；Seamless不支持的Hausa映射Arabic、Naijá映射French仅为fine-tuned extension。S2TT SSA-COMET/ChrF++，S2ST先OmnilingualASR转写再SSA-COMET，不能用文本exactmatch替代。 成本过高，不复现（审查 DONE）。每语言40余小时语音，Omnilingual-ASR1B、NLLB3.3B/TinyAya3B、Seamless2.3B mono/multi多个方向3–10epochs，另有Gemini/GPT-Audio推理、TTS和人工评审。整套明显超单卡短时预算，不下载音频/模型、不调用付费API。本轮仅核查论文身份、合作机构、方法/资源/许可证与成本，收录资料和原图。没有把通用聚合器或字段检查包装为官方benchmark接口；没有模型调用、训练或正式指标。  语音多模态 低资源语音翻译评测 多模态 跨模态对齐：表征、连接器与监督 NaijaS2ST 的多口音设置对翻译评测提出什么额外要求？ 同一语言的发音差异会影响语音理解和输出评估，所以数据覆盖多位说话人与口音，并按翻译方向分别报告。语音到文本和语音到语音也要区分，不能把一个方向或少数说话人的结果概括为所有尼日利亚语言与口音的能力。 例如英语到 Hausa 的结果不能替代 Hausa 到英语；某口音识别顺利也不能证明另一口音的语音合成同样可靠。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<span id="paper-multimodal-models-naijas2st-20646330" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-3e74dca2ad6800c6">NaijaS2ST 的多口音设置对翻译评测提出什么额外要求？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Anaijas2st">NaijaS2ST: A Multi-Accent Benchmark for Speech-to-Speech Translation in Low-Resource Nigerian Languages</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Mila - Quebec AI Institute</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一语言的发音差异会影响语音理解和输出评估，所以数据覆盖多位说话人与口音，并按翻译方向分别报告。语音到文本和语音到语音也要区分，不能把一个方向或少数说话人的结果概括为所有尼日利亚语言与口音的能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如英语到 Hausa 的结果不能替代 Hausa 到英语；某口音识别顺利也不能证明另一口音的语音合成同样可靠。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.16287v1">原论文</a> · <a href="../../../../multimodal-models/2604.16287-naijas2st/">实现解读</a> · <a href="#qa-3e74dca2ad6800c6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:naijas2st" data-paper-title="NaijaS2ST: A Multi-Accent Benchmark for Speech-to-Speech Translation in Low-Resource Nigerian Languages" data-learning-pending="false" data-level="mechanism" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="NaijaS2ST: A Multi-Accent Benchmark for Speech-to-Speech Translation in Low-Resource Nigerian Languages 多模态大模型 Mila - Quebec AI Institute 2026-04-17 核固定v3 Sections3–4及AppendixC：284说话人、约6K平行句、质控后约269h；5shot来自DEV，方向分开；Seamless不支持的Hausa映射Arabic、Naijá映射French仅为fine-tuned extension。S2TT SSA-COMET/ChrF++，S2ST先OmnilingualASR转写再SSA-COMET，不能用文本exactmatch替代。 成本过高，不复现（审查 DONE）。每语言40余小时语音，Omnilingual-ASR1B、NLLB3.3B/TinyAya3B、Seamless2.3B mono/multi多个方向3–10epochs，另有Gemini/GPT-Audio推理、TTS和人工评审。整套明显超单卡短时预算，不下载音频/模型、不调用付费API。本轮仅核查论文身份、合作机构、方法/资源/许可证与成本，收录资料和原图。没有把通用聚合器或字段检查包装为官方benchmark接口；没有模型调用、训练或正式指标。  语音多模态 低资源语音翻译评测 多模态 跨模态对齐：表征、连接器与监督 为什么语音到语音翻译不能用参考文本的 exact match 直接评价？ 模型输出的是音频，需要先通过真实 ASR 得到转写，再以规定的语义翻译指标比较；转写误差与翻译误差都影响结果。文本完全一致会忽略合理同义表达，也绕过声音输出链路。few-shot 示例应取开发集，不能把测试参考作为提示。 例如两段不同措辞的语音都正确表达“请明天来”，字面不一致并不必然是翻译错误，应保留语义和音频链路。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-dbd5bc66fec4aff6">为什么语音到语音翻译不能用参考文本的 exact match 直接评价？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Anaijas2st">NaijaS2ST: A Multi-Accent Benchmark for Speech-to-Speech Translation in Low-Resource Nigerian Languages</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Mila - Quebec AI Institute</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>模型输出的是音频，需要先通过真实 ASR 得到转写，再以规定的语义翻译指标比较；转写误差与翻译误差都影响结果。文本完全一致会忽略合理同义表达，也绕过声音输出链路。few-shot 示例应取开发集，不能把测试参考作为提示。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两段不同措辞的语音都正确表达“请明天来”，字面不一致并不必然是翻译错误，应保留语义和音频链路。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.16287v1">原论文</a> · <a href="../../../../multimodal-models/2604.16287-naijas2st/">实现解读</a> · <a href="#qa-dbd5bc66fec4aff6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:naijas2st" data-paper-title="NaijaS2ST: A Multi-Accent Benchmark for Speech-to-Speech Translation in Low-Resource Nigerian Languages" data-learning-pending="false" data-level="comparison" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="NaijaS2ST: A Multi-Accent Benchmark for Speech-to-Speech Translation in Low-Resource Nigerian Languages 多模态大模型 Mila - Quebec AI Institute 2026-04-17 核固定v3 Sections3–4及AppendixC：284说话人、约6K平行句、质控后约269h；5shot来自DEV，方向分开；Seamless不支持的Hausa映射Arabic、Naijá映射French仅为fine-tuned extension。S2TT SSA-COMET/ChrF++，S2ST先OmnilingualASR转写再SSA-COMET，不能用文本exactmatch替代。 成本过高，不复现（审查 DONE）。每语言40余小时语音，Omnilingual-ASR1B、NLLB3.3B/TinyAya3B、Seamless2.3B mono/multi多个方向3–10epochs，另有Gemini/GPT-Audio推理、TTS和人工评审。整套明显超单卡短时预算，不下载音频/模型、不调用付费API。本轮仅核查论文身份、合作机构、方法/资源/许可证与成本，收录资料和原图。没有把通用聚合器或字段检查包装为官方benchmark接口；没有模型调用、训练或正式指标。  语音多模态 低资源语音翻译评测 多模态 跨模态对齐：表征、连接器与监督 NaijaS2ST的文本翻译评测中，SSA-COMET与ChrF++关注的是同一种一致性吗？ 两者都比较译文，但SSA-COMET依赖多语言语义模型，ChrF++主要利用字符及词片段重叠，不能把两个分数当成同尺度的正确率。不同措辞可能保留语义却改变表面重叠；这是文本输出的互补指标，语音输出仍需经过规定的ASR链路。 教学例子：同一意思用两种合理措辞表达，字符重叠可能不同；不能因一个指标数值更大，就说它对应更多百分比的正确翻译。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-3ae01580dff4059e">NaijaS2ST的文本翻译评测中，SSA-COMET与ChrF++关注的是同一种一致性吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Anaijas2st">NaijaS2ST: A Multi-Accent Benchmark for Speech-to-Speech Translation in Low-Resource Nigerian Languages</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Mila - Quebec AI Institute</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两者都比较译文，但SSA-COMET依赖多语言语义模型，ChrF++主要利用字符及词片段重叠，不能把两个分数当成同尺度的正确率。不同措辞可能保留语义却改变表面重叠；这是文本输出的互补指标，语音输出仍需经过规定的ASR链路。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一意思用两种合理措辞表达，字符重叠可能不同；不能因一个指标数值更大，就说它对应更多百分比的正确翻译。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.16287v1">原论文</a> · <a href="../../../../multimodal-models/2604.16287-naijas2st/">实现解读</a> · <a href="#qa-3ae01580dff4059e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:naijas2st" data-paper-title="NaijaS2ST: A Multi-Accent Benchmark for Speech-to-Speech Translation in Low-Resource Nigerian Languages" data-learning-pending="false" data-level="implementation" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="NaijaS2ST: A Multi-Accent Benchmark for Speech-to-Speech Translation in Low-Resource Nigerian Languages 多模态大模型 Mila - Quebec AI Institute 2026-04-17 核固定v3 Sections3–4及AppendixC：284说话人、约6K平行句、质控后约269h；5shot来自DEV，方向分开；Seamless不支持的Hausa映射Arabic、Naijá映射French仅为fine-tuned extension。S2TT SSA-COMET/ChrF++，S2ST先OmnilingualASR转写再SSA-COMET，不能用文本exactmatch替代。 成本过高，不复现（审查 DONE）。每语言40余小时语音，Omnilingual-ASR1B、NLLB3.3B/TinyAya3B、Seamless2.3B mono/multi多个方向3–10epochs，另有Gemini/GPT-Audio推理、TTS和人工评审。整套明显超单卡短时预算，不下载音频/模型、不调用付费API。本轮仅核查论文身份、合作机构、方法/资源/许可证与成本，收录资料和原图。没有把通用聚合器或字段检查包装为官方benchmark接口；没有模型调用、训练或正式指标。  语音多模态 低资源语音翻译评测 多模态 跨模态对齐：表征、连接器与监督 five-shot 示例和代理语言 token 分别有哪些使用边界？ 五个示例应取自 DEV，不能从正式 test 选最有帮助的示例。部分 Seamless 微调扩展将 Hausa 映到 Arabic、Naijá 映到 French token，仅是适配约定，不能声称原模型原生支持；当前本地未下载音频或执行完整训练评测。 例如为 Hausa 微调使用 Arabic 标记，不代表输入真被翻译成阿拉伯语，也不构成无需训练就支持 Hausa 的证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-4223dcd722be9bd5">five-shot 示例和代理语言 token 分别有哪些使用边界？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Anaijas2st">NaijaS2ST: A Multi-Accent Benchmark for Speech-to-Speech Translation in Low-Resource Nigerian Languages</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Mila - Quebec AI Institute</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>五个示例应取自 DEV，不能从正式 test 选最有帮助的示例。部分 Seamless 微调扩展将 Hausa 映到 Arabic、Naijá 映到 French token，仅是适配约定，不能声称原模型原生支持；当前本地未下载音频或执行完整训练评测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如为 Hausa 微调使用 Arabic 标记，不代表输入真被翻译成阿拉伯语，也不构成无需训练就支持 Hausa 的证据。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.16287v1">原论文</a> · <a href="../../../../multimodal-models/2604.16287-naijas2st/">实现解读</a> · <a href="#qa-4223dcd722be9bd5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:smolvlm" data-paper-title="SmolVLM: Redefining small and efficient multimodal models" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="SmolVLM: Redefining small and efficient multimodal models 基础模型 Hugging Face 2025-04-07 SmolVLM 重新分配小模型视觉/语言侧算力，以 pixel shuffle 将相邻空间 token 搬到 channel 维，再用 MLP 映射到 LM 空间；同时研究长上下文、图像切片、学习位置 token 和数据配比，使 256M/500M/2.2B 模型在低显存下保持图像与视频能力。 保真度：核心机制复现。保真度：核心机制复现。本地执行论文中心的 pixel-shuffle 视觉 token 压缩与投影；未复刻 256M–2.2B decoder、视频和完整数据配方。使用 32×32 真实服饰图像和 2×2 space-to-depth；没有复刻高分辨率切片、视频采样、8k/16k context、学习位置 token 或 SmolLM decoder。本地对照口径：基线为线性 mean-pooling connector，实验组为 r=2 pixel shuffle + projector；  multimodal efficient-vlm visual-token-compression 多模态 跨模态对齐：表征、连接器与监督 SmolVLM的小模型设计，只是把语言模型层数削少吗？ 不是。它重新安排视觉与语言侧的计算，同时涉及视觉token压缩、图像切片、位置token、长上下文和数据配比。模型参数较少与视觉输入较便宜是不同预算轴；先识别这些组成，才能理解为什么一个局部重排算子并不代表完整小VLM配方。 教学例子：换更小语言骨干后若仍输入大量高分辨率视觉token，视觉编码与上下文成本仍在，不能只看语言参数量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<span id="paper-foundation-models-smolvlm-5de2167d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6da8d28c15e0fd0d">SmolVLM的小模型设计，只是把语言模型层数削少吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asmolvlm">SmolVLM: Redefining small and efficient multimodal models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Hugging Face</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。它重新安排视觉与语言侧的计算，同时涉及视觉token压缩、图像切片、位置token、长上下文和数据配比。模型参数较少与视觉输入较便宜是不同预算轴；先识别这些组成，才能理解为什么一个局部重排算子并不代表完整小VLM配方。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>换更小语言骨干后若仍输入大量高分辨率视觉token，视觉编码与上下文成本仍在，不能只看语言参数量。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.05299">原论文</a> · <a href="../../../../reproductions/2504.05299-smolvlm/">实现解读</a> · <a href="#qa-6da8d28c15e0fd0d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:smolvlm" data-paper-title="SmolVLM: Redefining small and efficient multimodal models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="SmolVLM: Redefining small and efficient multimodal models 基础模型 Hugging Face 2025-04-07 SmolVLM 重新分配小模型视觉/语言侧算力，以 pixel shuffle 将相邻空间 token 搬到 channel 维，再用 MLP 映射到 LM 空间；同时研究长上下文、图像切片、学习位置 token 和数据配比，使 256M/500M/2.2B 模型在低显存下保持图像与视频能力。 保真度：核心机制复现。保真度：核心机制复现。本地执行论文中心的 pixel-shuffle 视觉 token 压缩与投影；未复刻 256M–2.2B decoder、视频和完整数据配方。使用 32×32 真实服饰图像和 2×2 space-to-depth；没有复刻高分辨率切片、视频采样、8k/16k context、学习位置 token 或 SmolLM decoder。本地对照口径：基线为线性 mean-pooling connector，实验组为 r=2 pixel shuffle + projector；  multimodal efficient-vlm visual-token-compression 多模态 跨模态对齐：表征、连接器与监督 pixel shuffle 减少视觉 token 时，原来的邻域信息被放到哪里？ 相邻空间 token 被拼到通道维，再通过 MLP 接到语言模型，所以序列缩短并非简单丢弃每隔几个 patch。它把注意力需要处理的长度换成更宽的局部表示与连接器加工；压缩后是否保留小字和空间关系，仍需按具体任务验证。 例如四个相邻 patch 合并成一个更宽向量，token 数变为四分之一，但语言侧看到的空间粒度也随之改变。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-14e67387d09772aa">pixel shuffle 减少视觉 token 时，原来的邻域信息被放到哪里？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asmolvlm">SmolVLM: Redefining small and efficient multimodal models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Hugging Face</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相邻空间 token 被拼到通道维，再通过 MLP 接到语言模型，所以序列缩短并非简单丢弃每隔几个 patch。它把注意力需要处理的长度换成更宽的局部表示与连接器加工；压缩后是否保留小字和空间关系，仍需按具体任务验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如四个相邻 patch 合并成一个更宽向量，token 数变为四分之一，但语言侧看到的空间粒度也随之改变。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.05299">原论文</a> · <a href="../../../../reproductions/2504.05299-smolvlm/">实现解读</a> · <a href="#qa-14e67387d09772aa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:smolvlm" data-paper-title="SmolVLM: Redefining small and efficient multimodal models" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="SmolVLM: Redefining small and efficient multimodal models 基础模型 Hugging Face 2025-04-07 SmolVLM 重新分配小模型视觉/语言侧算力，以 pixel shuffle 将相邻空间 token 搬到 channel 维，再用 MLP 映射到 LM 空间；同时研究长上下文、图像切片、学习位置 token 和数据配比，使 256M/500M/2.2B 模型在低显存下保持图像与视频能力。 保真度：核心机制复现。保真度：核心机制复现。本地执行论文中心的 pixel-shuffle 视觉 token 压缩与投影；未复刻 256M–2.2B decoder、视频和完整数据配方。使用 32×32 真实服饰图像和 2×2 space-to-depth；没有复刻高分辨率切片、视频采样、8k/16k context、学习位置 token 或 SmolLM decoder。本地对照口径：基线为线性 mean-pooling connector，实验组为 r=2 pixel shuffle + projector；  multimodal efficient-vlm visual-token-compression 多模态 跨模态对齐：表征、连接器与监督 与把四个 patch 直接平均相比，space-to-depth 保留了什么区别？ 平均在聚合时抹去各 patch 的独立通道位置；space-to-depth 把它们按固定空间顺序拼接，后续投影仍可区分每个子位置。它增加单 token 的输入宽度以换取较短序列，但效果还依赖投影容量和训练，不能仅凭重排保证精细识别。 例如左上是黑块、右下是白块，平均后可能与相反排列一样；按位置拼接仍可区分两个局部图案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-9ffdba7ecafa65b8">与把四个 patch 直接平均相比，space-to-depth 保留了什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asmolvlm">SmolVLM: Redefining small and efficient multimodal models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Hugging Face</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>平均在聚合时抹去各 patch 的独立通道位置；space-to-depth 把它们按固定空间顺序拼接，后续投影仍可区分每个子位置。它增加单 token 的输入宽度以换取较短序列，但效果还依赖投影容量和训练，不能仅凭重排保证精细识别。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如左上是黑块、右下是白块，平均后可能与相反排列一样；按位置拼接仍可区分两个局部图案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.05299">原论文</a> · <a href="../../../../reproductions/2504.05299-smolvlm/">实现解读</a> · <a href="#qa-9ffdba7ecafa65b8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:smolvlm" data-paper-title="SmolVLM: Redefining small and efficient multimodal models" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="SmolVLM: Redefining small and efficient multimodal models 基础模型 Hugging Face 2025-04-07 SmolVLM 重新分配小模型视觉/语言侧算力，以 pixel shuffle 将相邻空间 token 搬到 channel 维，再用 MLP 映射到 LM 空间；同时研究长上下文、图像切片、学习位置 token 和数据配比，使 256M/500M/2.2B 模型在低显存下保持图像与视频能力。 保真度：核心机制复现。保真度：核心机制复现。本地执行论文中心的 pixel-shuffle 视觉 token 压缩与投影；未复刻 256M–2.2B decoder、视频和完整数据配方。使用 32×32 真实服饰图像和 2×2 space-to-depth；没有复刻高分辨率切片、视频采样、8k/16k context、学习位置 token 或 SmolLM decoder。本地对照口径：基线为线性 mean-pooling connector，实验组为 r=2 pixel shuffle + projector；  multimodal efficient-vlm visual-token-compression 多模态 跨模态对齐：表征、连接器与监督 本地 r=2 的接口验证包含 SmolVLM 的长视频与高分辨率配方吗？ 不包含。当前使用 32×32 服饰图像和 2×2 space-to-depth，未执行高分辨率切片、视频采样、长上下文、学习位置 token 或 SmolLM decoder。验证应限于重排与投影机制，不把 token 减少或分类结果推广为完整视频能力。 例如十六个 patch 压成四个可检查张量形状，但这没有测试长视频跨帧定位，也没有验证八千 token 的上下文。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-99a7266698fe9edc">本地 r=2 的接口验证包含 SmolVLM 的长视频与高分辨率配方吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asmolvlm">SmolVLM: Redefining small and efficient multimodal models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Hugging Face</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不包含。当前使用 32×32 服饰图像和 2×2 space-to-depth，未执行高分辨率切片、视频采样、长上下文、学习位置 token 或 SmolLM decoder。验证应限于重排与投影机制，不把 token 减少或分类结果推广为完整视频能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如十六个 patch 压成四个可检查张量形状，但这没有测试长视频跨帧定位，也没有验证八千 token 的上下文。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.05299">原论文</a> · <a href="../../../../reproductions/2504.05299-smolvlm/">实现解读</a> · <a href="#qa-99a7266698fe9edc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:siglip2" data-paper-title="SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features 基础模型 Google DeepMind 2025-02-20 SigLIP 2 在 SigLIP 的 pairwise sigmoid loss 上组合 captioning pretraining、global-local self-distillation、masked prediction、在线数据筛选和 NaFlex 动态分辨率，改善语义、定位、dense feature 与多语言公平性。 保真度：核心机制复现。保真度：核心机制复现。本地执行 sigmoid 对比目标与遮盖视图自蒸馏；未复刻多语言 web 数据、caption decoder 和 dense localization。Fashion-MNIST 类别文本替代多语言 caption；实际训练 sigmoid pair loss 和中心遮盖视图的 student-teacher consistency，没有复刻 caption decoder、active curation、NaFlex 和定位头。  multimodal sigmoid-contrastive self-distillation 多模态 跨模态对齐：表征、连接器与监督 SigLIP 2的NaFlex动态分辨率，是在调整类别标签数量吗？ 不是。动态分辨率处理视觉输入如何表示与分配计算，类别文本或其他下游标签是另一维。SigLIP 2同时涉及输入适应性、图文语义和局部表示训练，不能把改变图像尺寸的路径理解成扩展类别词表，也不能以单一固定尺寸的损失核代替完整输入配方。 教学例子：同一组猫狗标签下，可以给模型不同尺寸的图片；图像输入改变，并不意味着类别从两种变成更多种。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<span id="paper-foundation-models-siglip2-8c923237" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-27ae7a096e03b542">SigLIP 2的NaFlex动态分辨率，是在调整类别标签数量吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asiglip2">SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。动态分辨率处理视觉输入如何表示与分配计算，类别文本或其他下游标签是另一维。SigLIP 2同时涉及输入适应性、图文语义和局部表示训练，不能把改变图像尺寸的路径理解成扩展类别词表，也不能以单一固定尺寸的损失核代替完整输入配方。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一组猫狗标签下，可以给模型不同尺寸的图片；图像输入改变，并不意味着类别从两种变成更多种。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.14786">原论文</a> · <a href="../../../../reproductions/2502.14786-siglip2/">实现解读</a> · <a href="#qa-27ae7a096e03b542">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:siglip2" data-paper-title="SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features 基础模型 Google DeepMind 2025-02-20 SigLIP 2 在 SigLIP 的 pairwise sigmoid loss 上组合 captioning pretraining、global-local self-distillation、masked prediction、在线数据筛选和 NaFlex 动态分辨率，改善语义、定位、dense feature 与多语言公平性。 保真度：核心机制复现。保真度：核心机制复现。本地执行 sigmoid 对比目标与遮盖视图自蒸馏；未复刻多语言 web 数据、caption decoder 和 dense localization。Fashion-MNIST 类别文本替代多语言 caption；实际训练 sigmoid pair loss 和中心遮盖视图的 student-teacher consistency，没有复刻 caption decoder、active curation、NaFlex 和定位头。  multimodal sigmoid-contrastive self-distillation 多模态 跨模态对齐：表征、连接器与监督 为什么 pairwise sigmoid 对齐还要加入局部自蒸馏与 masked prediction？ 全局图文匹配主要约束整张图与描述的兼容性，未必充分训练局部位置与稠密特征。局部自蒸馏及掩码预测补充空间细节监督，captioning 与数据筛选又改善语义来源；这些组件的贡献要通过对照区分，不能都归因于单一 sigmoid 损失。 例如整图描述只说“街上有车”，局部训练还能要求遮住的车轮附近表示可恢复，帮助保留更细的空间线索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-1288afe0b0bfc12f">为什么 pairwise sigmoid 对齐还要加入局部自蒸馏与 masked prediction？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asiglip2">SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全局图文匹配主要约束整张图与描述的兼容性，未必充分训练局部位置与稠密特征。局部自蒸馏及掩码预测补充空间细节监督，captioning 与数据筛选又改善语义来源；这些组件的贡献要通过对照区分，不能都归因于单一 sigmoid 损失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如整图描述只说“街上有车”，局部训练还能要求遮住的车轮附近表示可恢复，帮助保留更细的空间线索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.14786">原论文</a> · <a href="../../../../reproductions/2502.14786-siglip2/">实现解读</a> · <a href="#qa-1288afe0b0bfc12f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:siglip2" data-paper-title="SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features 基础模型 Google DeepMind 2025-02-20 SigLIP 2 在 SigLIP 的 pairwise sigmoid loss 上组合 captioning pretraining、global-local self-distillation、masked prediction、在线数据筛选和 NaFlex 动态分辨率，改善语义、定位、dense feature 与多语言公平性。 保真度：核心机制复现。保真度：核心机制复现。本地执行 sigmoid 对比目标与遮盖视图自蒸馏；未复刻多语言 web 数据、caption decoder 和 dense localization。Fashion-MNIST 类别文本替代多语言 caption；实际训练 sigmoid pair loss 和中心遮盖视图的 student-teacher consistency，没有复刻 caption decoder、active curation、NaFlex 和定位头。  multimodal sigmoid-contrastive self-distillation 多模态 跨模态对齐：表征、连接器与监督 pairwise sigmoid 与 CLIP 的批内 softmax 在配对约束上有何不同？ softmax 在一行或一列的候选之间归一化，让正配对与同批其他项竞争；sigmoid 为每个图文 pair 使用正负标签与独立二分类形式。两者的归一化及温度、偏置作用不同，但损失形式的差别本身不是跨数据集效果结论。 例如一个批次的猫图与猫文是一对正例，猫图与狗文是一对负例；sigmoid 分别给两对施加二分类约束。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-476ced67a785f2fa">pairwise sigmoid 与 CLIP 的批内 softmax 在配对约束上有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asiglip2">SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>softmax 在一行或一列的候选之间归一化，让正配对与同批其他项竞争；sigmoid 为每个图文 pair 使用正负标签与独立二分类形式。两者的归一化及温度、偏置作用不同，但损失形式的差别本身不是跨数据集效果结论。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个批次的猫图与猫文是一对正例，猫图与狗文是一对负例；sigmoid 分别给两对施加二分类约束。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.14786">原论文</a> · <a href="../../../../reproductions/2502.14786-siglip2/">实现解读</a> · <a href="#qa-476ced67a785f2fa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:siglip2" data-paper-title="SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features 基础模型 Google DeepMind 2025-02-20 SigLIP 2 在 SigLIP 的 pairwise sigmoid loss 上组合 captioning pretraining、global-local self-distillation、masked prediction、在线数据筛选和 NaFlex 动态分辨率，改善语义、定位、dense feature 与多语言公平性。 保真度：核心机制复现。保真度：核心机制复现。本地执行 sigmoid 对比目标与遮盖视图自蒸馏；未复刻多语言 web 数据、caption decoder 和 dense localization。Fashion-MNIST 类别文本替代多语言 caption；实际训练 sigmoid pair loss 和中心遮盖视图的 student-teacher consistency，没有复刻 caption decoder、active curation、NaFlex 和定位头。  multimodal sigmoid-contrastive self-distillation 多模态 跨模态对齐：表征、连接器与监督 实现 sigmoid 配对损失时，z 的符号和偏置如何进入公式？ 正负 pair 的标签为加一或减一，统一放入负号内的 log(1+exp(-z·score))，其中 score 包含缩放点积和偏置。把标签误写成零和一而不改公式会让负例失去约束；本地还只做了类别文本与 masked-view 一致性。 例如负 pair 取 z=-1 时，高相似度会增加损失；若误取 z=0，损失恒定，模型便收不到排斥负例的梯度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-15aecb074ef6effd">实现 sigmoid 配对损失时，z 的符号和偏置如何进入公式？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asiglip2">SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>正负 pair 的标签为加一或减一，统一放入负号内的 log(1+exp(-z·score))，其中 score 包含缩放点积和偏置。把标签误写成零和一而不改公式会让负例失去约束；本地还只做了类别文本与 masked-view 一致性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如负 pair 取 z=-1 时，高相似度会增加损失；若误取 z=0，损失恒定，模型便收不到排斥负例的梯度。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.14786">原论文</a> · <a href="../../../../reproductions/2502.14786-siglip2/">实现解读</a> · <a href="#qa-15aecb074ef6effd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:llava" data-paper-title="Visual Instruction Tuning" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Visual Instruction Tuning 基础模型 University of Wisconsin-Madison / Microsoft Research / Columbia University 2023-04-17 冻结视觉 encoder，用可训练 projector 把视觉特征映射到 LLM token 空间，再在 GPT-4 生成的多模态指令数据上做端到端 instruction tuning。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。使用 Fashion-MNIST 真实像素、冻结的轻量 patch encoder、可训练 projector 与问答分类头；未调用 GPT-4，未执行多模态 instruction data generation，也未复刻 LLaVA-13B。单 seed 结果仅用于检验 projector 结构，不能外推到大模型指令微调。  multimodal instruction-tuning 多模态 跨模态对齐：表征、连接器与监督 视觉 projector 在 LLaVA 的图像到回答路径中承担什么角色？ 视觉编码器先产生图像特征，projector 将其变成语言模型可以读取的视觉 token 表示，再与问题和历史文本一起用于预测回答。它解决输入接口的连接，但能否遵循指令还依赖多模态指令训练，维度相同本身并不等于语义对齐。 例如图像编码器输出的维度与语言模型隐藏层不同，需要先投影；投影矩阵形状正确后，模型仍需学会哪些视觉信息对应用户问题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<span id="paper-foundation-models-llava-9b58a1f9" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-dfa5b553021f92af">视觉 projector 在 LLaVA 的图像到回答路径中承担什么角色？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Allava">Visual Instruction Tuning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Wisconsin-Madison / Microsoft Research / Columbia University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>视觉编码器先产生图像特征，projector 将其变成语言模型可以读取的视觉 token 表示，再与问题和历史文本一起用于预测回答。它解决输入接口的连接，但能否遵循指令还依赖多模态指令训练，维度相同本身并不等于语义对齐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如图像编码器输出的维度与语言模型隐藏层不同，需要先投影；投影矩阵形状正确后，模型仍需学会哪些视觉信息对应用户问题。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2304.08485">原论文</a> · <a href="../../../../reproductions/2304.08485-llava/">实现解读</a> · <a href="#qa-dfa5b553021f92af">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:llava" data-paper-title="Visual Instruction Tuning" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Visual Instruction Tuning 基础模型 University of Wisconsin-Madison / Microsoft Research / Columbia University 2023-04-17 冻结视觉 encoder，用可训练 projector 把视觉特征映射到 LLM token 空间，再在 GPT-4 生成的多模态指令数据上做端到端 instruction tuning。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。使用 Fashion-MNIST 真实像素、冻结的轻量 patch encoder、可训练 projector 与问答分类头；未调用 GPT-4，未执行多模态 instruction data generation，也未复刻 LLaVA-13B。单 seed 结果仅用于检验 projector 结构，不能外推到大模型指令微调。  multimodal instruction-tuning 多模态 跨模态对齐：表征、连接器与监督 把视觉特征投影到 LLM 的维度，为什么还不足以完成视觉指令跟随？ 维度相同只解决输入形状，不能保证视觉向量已具有语言模型需要的语义。连接器需要学习视觉到语言的接口，指令监督再训练模型根据图像与问题生成回应；只做投影而没有对应训练，不会自动获得读图、定位或多轮回答能力。 例如一张猫图经投影后可以作为向量输入，但模型仍需通过图像问答训练学会针对“它在哪里”组织答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-0ba55b5e7a12c6c3">把视觉特征投影到 LLM 的维度，为什么还不足以完成视觉指令跟随？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Allava">Visual Instruction Tuning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Wisconsin-Madison / Microsoft Research / Columbia University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>维度相同只解决输入形状，不能保证视觉向量已具有语言模型需要的语义。连接器需要学习视觉到语言的接口，指令监督再训练模型根据图像与问题生成回应；只做投影而没有对应训练，不会自动获得读图、定位或多轮回答能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一张猫图经投影后可以作为向量输入，但模型仍需通过图像问答训练学会针对“它在哪里”组织答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2304.08485">原论文</a> · <a href="../../../../reproductions/2304.08485-llava/">实现解读</a> · <a href="#qa-0ba55b5e7a12c6c3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:llava" data-paper-title="Visual Instruction Tuning" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Visual Instruction Tuning 基础模型 University of Wisconsin-Madison / Microsoft Research / Columbia University 2023-04-17 冻结视觉 encoder，用可训练 projector 把视觉特征映射到 LLM token 空间，再在 GPT-4 生成的多模态指令数据上做端到端 instruction tuning。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。使用 Fashion-MNIST 真实像素、冻结的轻量 patch encoder、可训练 projector 与问答分类头；未调用 GPT-4，未执行多模态 instruction data generation，也未复刻 LLaVA-13B。单 seed 结果仅用于检验 projector 结构，不能外推到大模型指令微调。  multimodal instruction-tuning 多模态 跨模态对齐：表征、连接器与监督 LLaVA 的指令监督与 CLIP 的双塔对比监督训练什么不同关系？ LLaVA 条件生成回答，直接学习视觉输入、问题与目标回答 token 的关系；CLIP 主要让配对图文在共享向量空间中相近，用于相似度匹配。二者监督对象不同，不能把 CLIP 检索分数当成指令生成质量，也不能仅据结构比较效果。 例如“这两个人为何撑伞”需要生成条件回答；给整张图选择最相似的一句文本，是另一种输出接口。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f7c311ba118b0143">LLaVA 的指令监督与 CLIP 的双塔对比监督训练什么不同关系？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Allava">Visual Instruction Tuning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Wisconsin-Madison / Microsoft Research / Columbia University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>LLaVA 条件生成回答，直接学习视觉输入、问题与目标回答 token 的关系；CLIP 主要让配对图文在共享向量空间中相近，用于相似度匹配。二者监督对象不同，不能把 CLIP 检索分数当成指令生成质量，也不能仅据结构比较效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如“这两个人为何撑伞”需要生成条件回答；给整张图选择最相似的一句文本，是另一种输出接口。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2304.08485">原论文</a> · <a href="../../../../reproductions/2304.08485-llava/">实现解读</a> · <a href="#qa-f7c311ba118b0143">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:llava" data-paper-title="Visual Instruction Tuning" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Visual Instruction Tuning 基础模型 University of Wisconsin-Madison / Microsoft Research / Columbia University 2023-04-17 冻结视觉 encoder，用可训练 projector 把视觉特征映射到 LLM token 空间，再在 GPT-4 生成的多模态指令数据上做端到端 instruction tuning。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。使用 Fashion-MNIST 真实像素、冻结的轻量 patch encoder、可训练 projector 与问答分类头；未调用 GPT-4，未执行多模态 instruction data generation，也未复刻 LLaVA-13B。单 seed 结果仅用于检验 projector 结构，不能外推到大模型指令微调。  multimodal instruction-tuning 多模态 跨模态对齐：表征、连接器与监督 本地两层 MLP projector 的负结果能否否定原论文指令微调？ 不能。本地固定轻量视觉 patch encoder、问答分类头与小训练预算，只比较线性和两层 MLP 接口，没有生成 GPT-4 指令数据或训练 LLaVA-13B。其负结果说明该小任务增加接口容量未自动受益，范围应限于当前结构与预算。 例如小衣物分类任务上 MLP 分数下降，只能报告这次受控比较，不能推导大模型多轮图像对话也会下降。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f05675cd47b434ea">本地两层 MLP projector 的负结果能否否定原论文指令微调？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Allava">Visual Instruction Tuning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Wisconsin-Madison / Microsoft Research / Columbia University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。本地固定轻量视觉 patch encoder、问答分类头与小训练预算，只比较线性和两层 MLP 接口，没有生成 GPT-4 指令数据或训练 LLaVA-13B。其负结果说明该小任务增加接口容量未自动受益，范围应限于当前结构与预算。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如小衣物分类任务上 MLP 分数下降，只能报告这次受控比较，不能推导大模型多轮图像对话也会下降。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2304.08485">原论文</a> · <a href="../../../../reproductions/2304.08485-llava/">实现解读</a> · <a href="#qa-f05675cd47b434ea">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:blip2" data-paper-title="BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models 基础模型 Salesforce Research 2023-01-30 BLIP-2 冻结已有视觉 encoder 和 LLM，只训练轻量 Q-Former。固定数量的可学习 query 通过 cross-attention 从视觉 token 提取与语言最相关的信息；第一阶段做图文表征学习，第二阶段将 query 输出投影成冻结 LLM 的 soft visual prompt。 保真度：核心机制复现。保真度：核心机制复现。本地执行 Q-Former 的可学习 query 与 cross-attention；论文两阶段大规模预训练和冻结大模型未复刻。使用 Fashion-MNIST 真实像素和四 query multi-head cross-attention；没有加载 ViT-g、OPT/FlanT5，也没有执行 ITC/ITM/ITG 两阶段 129M 图像预训练。本地对照口径：基线为相同预算的线性 mean-pooling connector，实验组为四 query Q-Former；  multimodal q-former frozen-encoders 多模态 跨模态对齐：表征、连接器与监督 Q-Former 的 query 是待回答的问题文本吗？ 这里的 query 是固定数量、可学习的向量，不是用户问句。它们通过交叉注意力从冻结视觉编码器的 token 中抽取信息，再交给语言侧；数量固定形成视觉信息瓶颈，因此输入图片更复杂并不会自动增加输出 token 数。 例如一张图产生数百个 patch，四个可学习 query 可以读全部 patch，却只把四个向量交给后续语言模型。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<span id="paper-foundation-models-blip2-9ce69b95" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6fff6daeb7b674ec">Q-Former 的 query 是待回答的问题文本吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ablip2">BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Salesforce Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这里的 query 是固定数量、可学习的向量，不是用户问句。它们通过交叉注意力从冻结视觉编码器的 token 中抽取信息，再交给语言侧；数量固定形成视觉信息瓶颈，因此输入图片更复杂并不会自动增加输出 token 数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一张图产生数百个 patch，四个可学习 query 可以读全部 patch，却只把四个向量交给后续语言模型。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2301.12597">原论文</a> · <a href="../../../../reproductions/2301.12597-blip2/">实现解读</a> · <a href="#qa-6fff6daeb7b674ec">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:blip2" data-paper-title="BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models 基础模型 Salesforce Research 2023-01-30 BLIP-2 冻结已有视觉 encoder 和 LLM，只训练轻量 Q-Former。固定数量的可学习 query 通过 cross-attention 从视觉 token 提取与语言最相关的信息；第一阶段做图文表征学习，第二阶段将 query 输出投影成冻结 LLM 的 soft visual prompt。 保真度：核心机制复现。保真度：核心机制复现。本地执行 Q-Former 的可学习 query 与 cross-attention；论文两阶段大规模预训练和冻结大模型未复刻。使用 Fashion-MNIST 真实像素和四 query multi-head cross-attention；没有加载 ViT-g、OPT/FlanT5，也没有执行 ITC/ITM/ITG 两阶段 129M 图像预训练。本地对照口径：基线为相同预算的线性 mean-pooling connector，实验组为四 query Q-Former；  multimodal q-former frozen-encoders 多模态 跨模态对齐：表征、连接器与监督 为什么冻结视觉编码器和语言模型后，Q-Former 仍能学会把图像接给语言模型？ 梯度仍可经过冻结模块传到连接器；冻结的是参数更新，不是计算图。可学习 Query 通过交叉注意力从视觉特征中选取信息，再投影成语言模型能消费的软提示。两阶段训练分别处理图文表征对齐与语言生成接口，瓶颈也可能丢失细节。 例如把十六块图像特征压成四个 Query，语言模型仍能接收四个视觉提示，但小字可能需要更多容量。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-49e7f356a5e01708">为什么冻结视觉编码器和语言模型后，Q-Former 仍能学会把图像接给语言模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ablip2">BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Salesforce Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>梯度仍可经过冻结模块传到连接器；冻结的是参数更新，不是计算图。可学习 Query 通过交叉注意力从视觉特征中选取信息，再投影成语言模型能消费的软提示。两阶段训练分别处理图文表征对齐与语言生成接口，瓶颈也可能丢失细节。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把十六块图像特征压成四个 Query，语言模型仍能接收四个视觉提示，但小字可能需要更多容量。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2301.12597">原论文</a> · <a href="../../../../reproductions/2301.12597-blip2/">实现解读</a> · <a href="#qa-49e7f356a5e01708">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:blip2" data-paper-title="BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models 基础模型 Salesforce Research 2023-01-30 BLIP-2 冻结已有视觉 encoder 和 LLM，只训练轻量 Q-Former。固定数量的可学习 query 通过 cross-attention 从视觉 token 提取与语言最相关的信息；第一阶段做图文表征学习，第二阶段将 query 输出投影成冻结 LLM 的 soft visual prompt。 保真度：核心机制复现。保真度：核心机制复现。本地执行 Q-Former 的可学习 query 与 cross-attention；论文两阶段大规模预训练和冻结大模型未复刻。使用 Fashion-MNIST 真实像素和四 query multi-head cross-attention；没有加载 ViT-g、OPT/FlanT5，也没有执行 ITC/ITM/ITG 两阶段 129M 图像预训练。本地对照口径：基线为相同预算的线性 mean-pooling connector，实验组为四 query Q-Former；  multimodal q-former frozen-encoders 多模态 跨模态对齐：表征、连接器与监督 BLIP-2 与给每个视觉 patch 加线性投影相比，接口结构有何不同？ 逐 patch 投影主要改变特征维度，通常保留原 token 数；Q-Former 用可学习查询主动聚合视觉信息，再做投影。两者因此在信息选择与序列长度上不同，但瓶颈是否损失细节取决于训练和任务，不能由结构直接推定准确率更高。 例如识别衣服类别也许只需整体轮廓，读取小字却可能需要瓶颈保留局部细节；四个 query 并非在两类任务上都足够。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-56462053ed6b555f">BLIP-2 与给每个视觉 patch 加线性投影相比，接口结构有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ablip2">BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Salesforce Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>逐 patch 投影主要改变特征维度，通常保留原 token 数；Q-Former 用可学习查询主动聚合视觉信息，再做投影。两者因此在信息选择与序列长度上不同，但瓶颈是否损失细节取决于训练和任务，不能由结构直接推定准确率更高。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如识别衣服类别也许只需整体轮廓，读取小字却可能需要瓶颈保留局部细节；四个 query 并非在两类任务上都足够。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2301.12597">原论文</a> · <a href="../../../../reproductions/2301.12597-blip2/">实现解读</a> · <a href="#qa-56462053ed6b555f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:blip2" data-paper-title="BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models 基础模型 Salesforce Research 2023-01-30 BLIP-2 冻结已有视觉 encoder 和 LLM，只训练轻量 Q-Former。固定数量的可学习 query 通过 cross-attention 从视觉 token 提取与语言最相关的信息；第一阶段做图文表征学习，第二阶段将 query 输出投影成冻结 LLM 的 soft visual prompt。 保真度：核心机制复现。保真度：核心机制复现。本地执行 Q-Former 的可学习 query 与 cross-attention；论文两阶段大规模预训练和冻结大模型未复刻。使用 Fashion-MNIST 真实像素和四 query multi-head cross-attention；没有加载 ViT-g、OPT/FlanT5，也没有执行 ITC/ITM/ITG 两阶段 129M 图像预训练。本地对照口径：基线为相同预算的线性 mean-pooling connector，实验组为四 query Q-Former；  multimodal q-former frozen-encoders 多模态 跨模态对齐：表征、连接器与监督 本地四 query 结果能验证原论文两阶段预训练吗？ 不能。本地使用真实 Fashion-MNIST 像素与四 query 交叉注意力，未加载 ViT-g 或大型语言模型，也没有执行原文 ITC、ITM、ITG 与第二阶段的大规模训练。它可检查 token 压缩路径与小预算行为，不能充当原论文零样本能力验证。 例如观察到视觉 token 从十六降到四，只能证明当前接口缩短了序列，不能据此声称完成了一亿多图像的预训练。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-519bd14a28b1f0be">本地四 query 结果能验证原论文两阶段预训练吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ablip2">BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Salesforce Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。本地使用真实 Fashion-MNIST 像素与四 query 交叉注意力，未加载 ViT-g 或大型语言模型，也没有执行原文 ITC、ITM、ITG 与第二阶段的大规模训练。它可检查 token 压缩路径与小预算行为，不能充当原论文零样本能力验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如观察到视觉 token 从十六降到四，只能证明当前接口缩短了序列，不能据此声称完成了一亿多图像的预训练。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2301.12597">原论文</a> · <a href="../../../../reproductions/2301.12597-blip2/">实现解读</a> · <a href="#qa-519bd14a28b1f0be">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:clip" data-paper-title="Learning Transferable Visual Models From Natural Language Supervision" data-learning-pending="false" data-level="basics" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Learning Transferable Visual Models From Natural Language Supervision 基础模型 OpenAI 2021-02-26 用独立图像/文本 encoder 将配对样本映射到同一单位球面，通过双向 batch contrastive objective 学习可迁移零样本表示。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。使用 Fashion-MNIST 的真实像素与类别文本复现双塔、归一化和对称式对比目标；没有复刻 4 亿图文对、自然语言长尾语义或大规模视觉 encoder。单 seed 小预算结果只验证机制可执行，不等价于原论文 zero-shot 指标。本地对照口径：在真实 Fashion-MNIST 图像与类别文本构成的 10 类图文任务上，基线为均匀随机检索（10.0%），实验组为对称式图文对比学习双塔；测试准确率达到 72.0%（+62.0 个百分点），打乱图像后降至 10.3%，说明结果依赖视觉输入。  multimodal contrastive-pretraining 多模态 跨模态对齐：表征、连接器与监督 CLIP 的零样本分类为什么可以不用重新训练类别分类头？ 图像与类别描述分别经过两个编码器，归一化后在共享空间比较相似度。类别文本本身提供分类原型，因此可以替换描述以定义新标签；这依赖预训练已学到相关概念，并不保证任意新概念或细粒度关系都能正确识别。 例如给一张鞋图分别计算与“一双鞋”“一件外套”的相似度，可直接选择较高者，无需为这两个类别另训线性头。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<span id="paper-foundation-models-clip-b03c09f0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a637592f066a62d1">CLIP 的零样本分类为什么可以不用重新训练类别分类头？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aclip">Learning Transferable Visual Models From Natural Language Supervision</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · OpenAI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>图像与类别描述分别经过两个编码器，归一化后在共享空间比较相似度。类别文本本身提供分类原型，因此可以替换描述以定义新标签；这依赖预训练已学到相关概念，并不保证任意新概念或细粒度关系都能正确识别。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如给一张鞋图分别计算与“一双鞋”“一件外套”的相似度，可直接选择较高者，无需为这两个类别另训线性头。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2103.00020">原论文</a> · <a href="../../../../reproductions/2103.00020-clip/">实现解读</a> · <a href="#qa-a637592f066a62d1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:clip" data-paper-title="Learning Transferable Visual Models From Natural Language Supervision" data-learning-pending="false" data-level="mechanism" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Learning Transferable Visual Models From Natural Language Supervision 基础模型 OpenAI 2021-02-26 用独立图像/文本 encoder 将配对样本映射到同一单位球面，通过双向 batch contrastive objective 学习可迁移零样本表示。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。使用 Fashion-MNIST 的真实像素与类别文本复现双塔、归一化和对称式对比目标；没有复刻 4 亿图文对、自然语言长尾语义或大规模视觉 encoder。单 seed 小预算结果只验证机制可执行，不等价于原论文 zero-shot 指标。本地对照口径：在真实 Fashion-MNIST 图像与类别文本构成的 10 类图文任务上，基线为均匀随机检索（10.0%），实验组为对称式图文对比学习双塔；测试准确率达到 72.0%（+62.0 个百分点），打乱图像后降至 10.3%，说明结果依赖视觉输入。  multimodal contrastive-pretraining 多模态 跨模态对齐：表征、连接器与监督 CLIP 为什么既做图到文、也做文到图的对比学习？ 同一批图文可形成两个分类问题：给每张图找到配对文本，给每段文本找到配对图像。两个方向共同约束共享相似度空间，避免只照顾一种检索方向；负例来自批内其他配对，但整体匹配分数并不等于细粒度事实正确率。 例如猫图与猫描述互为正例，犬图与犬描述互为另一正例；两个方向都要把对应配对排在前面。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-48eaa29686fc2e90">CLIP 为什么既做图到文、也做文到图的对比学习？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aclip">Learning Transferable Visual Models From Natural Language Supervision</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · OpenAI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一批图文可形成两个分类问题：给每张图找到配对文本，给每段文本找到配对图像。两个方向共同约束共享相似度空间，避免只照顾一种检索方向；负例来自批内其他配对，但整体匹配分数并不等于细粒度事实正确率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如猫图与猫描述互为正例，犬图与犬描述互为另一正例；两个方向都要把对应配对排在前面。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2103.00020">原论文</a> · <a href="../../../../reproductions/2103.00020-clip/">实现解读</a> · <a href="#qa-48eaa29686fc2e90">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:clip" data-paper-title="Learning Transferable Visual Models From Natural Language Supervision" data-learning-pending="false" data-level="comparison" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Learning Transferable Visual Models From Natural Language Supervision 基础模型 OpenAI 2021-02-26 用独立图像/文本 encoder 将配对样本映射到同一单位球面，通过双向 batch contrastive objective 学习可迁移零样本表示。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。使用 Fashion-MNIST 的真实像素与类别文本复现双塔、归一化和对称式对比目标；没有复刻 4 亿图文对、自然语言长尾语义或大规模视觉 encoder。单 seed 小预算结果只验证机制可执行，不等价于原论文 zero-shot 指标。本地对照口径：在真实 Fashion-MNIST 图像与类别文本构成的 10 类图文任务上，基线为均匀随机检索（10.0%），实验组为对称式图文对比学习双塔；测试准确率达到 72.0%（+62.0 个百分点），打乱图像后降至 10.3%，说明结果依赖视觉输入。  multimodal contrastive-pretraining 多模态 跨模态对齐：表征、连接器与监督 CLIP把类别文字编码成向量，与自回归模型逐词生成类别名称，输出合同有何不同？ CLIP在给定类别文本之间比较图文相似度，返回候选内的选择或排序；自回归模型则预测类别名称的词元序列，还需要处理生成和解析。前者的类别描述是输入原型，不是要生成的目标文本，因此相似度接口本身不提供开放式图像描述能力。 教学例子：输入“猫的照片”和“狗的照片”两段类别描述后，CLIP比较两个分数；它不必先生成“这是一只猫”这句话。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d51dbad1f172823e">CLIP把类别文字编码成向量，与自回归模型逐词生成类别名称，输出合同有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aclip">Learning Transferable Visual Models From Natural Language Supervision</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · OpenAI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>CLIP在给定类别文本之间比较图文相似度，返回候选内的选择或排序；自回归模型则预测类别名称的词元序列，还需要处理生成和解析。前者的类别描述是输入原型，不是要生成的目标文本，因此相似度接口本身不提供开放式图像描述能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>输入“猫的照片”和“狗的照片”两段类别描述后，CLIP比较两个分数；它不必先生成“这是一只猫”这句话。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2103.00020">原论文</a> · <a href="../../../../reproductions/2103.00020-clip/">实现解读</a> · <a href="#qa-d51dbad1f172823e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:clip" data-paper-title="Learning Transferable Visual Models From Natural Language Supervision" data-learning-pending="false" data-level="implementation" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Learning Transferable Visual Models From Natural Language Supervision 基础模型 OpenAI 2021-02-26 用独立图像/文本 encoder 将配对样本映射到同一单位球面，通过双向 batch contrastive objective 学习可迁移零样本表示。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。使用 Fashion-MNIST 的真实像素与类别文本复现双塔、归一化和对称式对比目标；没有复刻 4 亿图文对、自然语言长尾语义或大规模视觉 encoder。单 seed 小预算结果只验证机制可执行，不等价于原论文 zero-shot 指标。本地对照口径：在真实 Fashion-MNIST 图像与类别文本构成的 10 类图文任务上，基线为均匀随机检索（10.0%），实验组为对称式图文对比学习双塔；测试准确率达到 72.0%（+62.0 个百分点），打乱图像后降至 10.3%，说明结果依赖视觉输入。  multimodal contrastive-pretraining 多模态 跨模态对齐：表征、连接器与监督 计算 CLIP 相似度矩阵前，为什么需要逐向量归一化？ 归一化使点积主要反映方向一致性，而不是通过增大向量范数提高分数；再用温度控制分布尖锐程度。批内图文配对的标签位于矩阵对角线，两方向损失分别使用原矩阵与转置矩阵，不能把全部配对都当正例。 例如图向量范数翻倍不应使其对所有文本都更“正确”；单位化后只有方向变化会改变余弦匹配关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-54de2a460ec3a509">计算 CLIP 相似度矩阵前，为什么需要逐向量归一化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aclip">Learning Transferable Visual Models From Natural Language Supervision</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · OpenAI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>归一化使点积主要反映方向一致性，而不是通过增大向量范数提高分数；再用温度控制分布尖锐程度。批内图文配对的标签位于矩阵对角线，两方向损失分别使用原矩阵与转置矩阵，不能把全部配对都当正例。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如图向量范数翻倍不应使其对所有文本都更“正确”；单位化后只有方向变化会改变余弦匹配关系。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2103.00020">原论文</a> · <a href="../../../../reproductions/2103.00020-clip/">实现解读</a> · <a href="#qa-54de2a460ec3a509">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

图像、语音和文字如何接上同一任务接口，学到的是相似度还是可生成的回答？

## 记住这一点

CLIP 用独立图像/文本编码器和配对对比目标学习共享表示，相似度可服务零样本分类与检索。BLIP-2 冻结视觉编码器和 LLM，通过少量 Query 的 Q-Former 提取视觉信息，分阶段连接图文表示与语言生成。指令微调、蒸馏、奖励建模和专门评测进一步改变监督与读出；应逐项追踪输入、训练目标和输出接口。

## 一个例子

“找与红色雨伞描述最匹配的图片”适合比较图文 embedding；“图里第二行小字是什么”需要细粒度视觉证据和能输出文本的接口。把图片接到 LLM 并不自动获得 OCR 能力，压缩后的视觉 Query 也可能丢掉细节。

## 什么时候要小心

检索相似度不是事实正确性的概率，词语匹配也不等于图像真正被使用。检查打乱图像等视觉依赖负控，并区分自然图文、语音口音和视频域。现有小图像实验、随机 fixture 与正式公开 benchmark 有不同证据等级，不能混用。

## 先读这几篇

先读 CLIP 的双塔、归一化和对比目标；再读 BLIP-2 的 Q-Former 及两阶段连接，区分共享 embedding 与接入语言生成。之后按任务选择指令、蒸馏、奖励或跨模态评测。

1. [Learning Transferable Visual Models From Natural Language Supervision](../../../reproductions/2103.00020-clip/README.md) · [原论文](https://arxiv.org/abs/2103.00020)
2. [BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models](../../../reproductions/2301.12597-blip2/README.md) · [原论文](https://arxiv.org/abs/2301.12597)

## 自测一下

CLIP 检索得分很高，能否直接断言模型可以读出图中所有文字？

??? note "展开参考答案"

    不能。配对对比学习主要约束整体图文兼容性，细小文字读取需要足够视觉分辨率、局部表示与解码监督。应用应单独测 OCR 或对应细粒度任务，并验证结果随图像内容改变。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
