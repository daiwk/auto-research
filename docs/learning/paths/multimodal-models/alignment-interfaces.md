---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 跨模态对齐：表征、连接器与监督

[多模态](index.md) / 子主题导学 · 约 3 分钟 · 20 张论文卡

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

## 这个子主题的论文卡片

导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">
<div class="ar-learning-controls">
<label for="learning-search">搜索卡片
<input id="learning-search" type="search" data-learning-search placeholder="搜索论文、机制、机构或本地边界"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">共 20 张卡片</p>
<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card" data-learning-card data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="FlexGlue: Sparse-to-Dense Feature Matching and Visual Disambiguation 多模态大模型 ETH Zurich 2026-10-23 稀疏matcher受两图keypoint重复检测能力限制，dense matcher则昂贵，而且两者常只在共视正样本训练，面对对称建筑等doppelganger会给出高置信假匹配。FlexGlue在stride8全图token网格上先做self/cross attention，再只对给定query插值读取特征并寻找另一图的坐标。局部3×3窗口读取避免全局期望在多个候选间平均；轻量MLP对两个方向的offset bins取期望做局部细化。共视分支给每个token一个sigmoid vote，并在每层监督； 成本过高，不复现（审查 DONE）。原文第7页：冻结DINOv3 ConvNeXt-B、9层512维Transformer、8数据集、512×512图像，50epochs、每epoch150K样本，在4张H200上约4 GPU-days；gradient checkpointing后4张RTX4090约1.5天，另有10epoch消歧fine-tune与多数据集/重建评测。这里保持作者的GPU-days口径，不虚构单卡总时长。本轮没有operator、local command、metrics或GPU收据，gpu_validation_passed=false。保留作者仓库作为可查来源；  多模态表征 视觉匹配与几何 多模态 跨模态对齐：表征、连接器与监督">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<h2 id="paper-multimodal-models-flexglue-0459516f">FlexGlue: Sparse-to-Dense Feature Matching and Visual Disambiguation</h2>
<p class="ar-learning-card__meta">ETH Zurich · 论文公开：2026-10-23</p>
<p><strong>方法要点：</strong>稀疏matcher受两图keypoint重复检测能力限制，dense matcher则昂贵，而且两者常只在共视正样本训练，面对对称建筑等doppelganger会给出高置信假匹配。FlexGlue在stride8全图token网格上先做self/cross attention，再只对给定query插值读取特征并寻找另一图的坐标。局部3×3窗口读取避免全局期望在多个候选间平均；轻量MLP对两个方向的offset bins取期望做局部细化。共视分支给每个token一个sigmoid vote，并在每层监督；</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。原文第7页：冻结DINOv3 ConvNeXt-B、9层512维Transformer、8数据集、512×512图像，50epochs、每epoch150K样本，在4张H200上约4 GPU-days；gradient checkpointing后4张RTX4090约1.5天，另有10epoch消歧fine-tune与多数据集/重建评测。这里保持作者的GPU-days口径，不虚构单卡总时长。本轮没有operator、local command、metrics或GPU收据，gpu_validation_passed=false。保留作者仓库作为可查来源；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32976v1">原论文</a> · <a href="../../../../multimodal-models/2610.32976-flexglue/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="LAMP: Layerwise Adaptive Mixing of Predictors for Training-Free Few-Shot Vision-Language Adaptation 基础模型 Taizhou Institute of Science and Technology, Nanjing University of Science and Technology 2026-10-15 冻结视觉编码器的中间层包含不同粒度的信息，但维度和相似性结构不同。LAMP不将它们投影到统一特征维度，而是分别拟合支持标签相对CLIP先验的残差，再在类别分数空间混合。区域核只以support bank校准；LAMP-F适配文本原型时，同步更新残差预测，避免原型改变而支持残差仍陈旧。 完整实验成本过高，不复现（审查 DONE）。测试标签在所有选择与一次原型更新完成后才用于最终诊断报告。固定recipe synthetic-fpot-and-native-layer-kernel-features@oct19-foundation-mechanisms-v1，seeds42/43/44。冻结三层小MLP编码4×4合成patch；三层区域宽度分别为5/7/9，全局宽度6。支持12视图、验证6样本、测试5样本具有不重叠身份，彼此独立生成；不是CLIP或公开图像benchmark。  多模态基础模型 冻结特征与少样本适配 多模态 跨模态对齐：表征、连接器与监督">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<h2 id="paper-foundation-models-lamp-52f612c4">LAMP: Layerwise Adaptive Mixing of Predictors for Training-Free Few-Shot Vision-Language Adaptation</h2>
<p class="ar-learning-card__meta">Taizhou Institute of Science and Technology, Nanjing University of Science and Technology · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>冻结视觉编码器的中间层包含不同粒度的信息，但维度和相似性结构不同。LAMP不将它们投影到统一特征维度，而是分别拟合支持标签相对CLIP先验的残差，再在类别分数空间混合。区域核只以support bank校准；LAMP-F适配文本原型时，同步更新残差预测，避免原型改变而支持残差仍陈旧。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）。测试标签在所有选择与一次原型更新完成后才用于最终诊断报告。固定recipe synthetic-fpot-and-native-layer-kernel-features@oct19-foundation-mechanisms-v1，seeds42/43/44。冻结三层小MLP编码4×4合成patch；三层区域宽度分别为5/7/9，全局宽度6。支持12视图、验证6样本、测试5样本具有不重叠身份，彼此独立生成；不是CLIP或公开图像benchmark。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22182">原论文</a> · <a href="../../../../foundation-models/2610.22182-lamp/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="CV-OPD: Contrastive Vision On-policy Distillation 多模态大模型 Xiamen University / Moxin Technology 2026-10-09 原来的 crop-to-full-image OPD 可以教会模型答案分布，却不必然教会它依赖正确视觉区域。作者在移除答案相关区域后发现，Vision-OPD 仍取得明显高于随机的准确率。CV-OPD 用同图、同尺寸、低 IoU 的负区域构造第二个共享参数教师，把“接近正教师、远离负教师”的约束加入 JSD 蒸馏。三个不可省略的约束是：正负教师只改变 crop、读取同一学生前缀；CDL 使用有界 JSD 的 margin； 当前实现为 core_mechanism / L1 核心机制诊断，真实 VLM 更新而非图像分类打分代理。cpu-contracts.json记录已重跑的 7 个行为测试：bbox 尺寸与 IoU、JSD/Top-K tail、样本与 token gate、教师停止梯度和零正确样本的零梯度，以及严格多类 verifier、标签隔离和图像来源/切分哈希。每项先固定 seed 42，专用 crop/gate 用例内部使用 seed 2；这些是单测用例，不是独立多 seed 能力实验。测试通过不代表视觉推理能力或 GPU 训练完成。  视觉证据对齐 On-policy distillation 多模态 跨模态对齐：表征、连接器与监督">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<h2 id="paper-multimodal-models-cv-opd-6105b27e">CV-OPD: Contrastive Vision On-policy Distillation</h2>
<p class="ar-learning-card__meta">Xiamen University / Moxin Technology · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>原来的 crop-to-full-image OPD 可以教会模型答案分布，却不必然教会它依赖正确视觉区域。作者在移除答案相关区域后发现，Vision-OPD 仍取得明显高于随机的准确率。CV-OPD 用同图、同尺寸、低 IoU 的负区域构造第二个共享参数教师，把“接近正教师、远离负教师”的约束加入 JSD 蒸馏。三个不可省略的约束是：正负教师只改变 crop、读取同一学生前缀；CDL 使用有界 JSD 的 margin；</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>当前实现为 core_mechanism / L1 核心机制诊断，真实 VLM 更新而非图像分类打分代理。cpu-contracts.json记录已重跑的 7 个行为测试：bbox 尺寸与 IoU、JSD/Top-K tail、样本与 token gate、教师停止梯度和零正确样本的零梯度，以及严格多类 verifier、标签隔离和图像来源/切分哈希。每项先固定 seed 42，专用 crop/gate 用例内部使用 seed 2；这些是单测用例，不是独立多 seed 能力实验。测试通过不代表视觉推理能力或 GPU 训练完成。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13264">原论文</a> · <a href="../../../../reproductions/2610.13264-cv-opd/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Unsupervised Multimodal Reward Modeling 多模态大模型 Massachusetts Institute of Technology 2026-10-08 偏好pair昂贵，reward benchmark名次也不必代表部署选择效用。作者冻结Qwen3-VL，在中间language层只均值池化response tokens，再训练无bias线性reward head；公开caption为positive，同一caption的颜色/数量/尺寸/方位单span变化、tail splice、clause shuffle及cross-image caption为negative，不需人工偏好标注。 bootstrap另与random own-candidate选择比较，相对原论文CHAIR不适用，小样本诊断不代表稳定能力提升。本地对照口径：零bias-free head的tie计半为pair基线，验证集选中的真实中间层head为实验组；bootstrap另与random own-candidate选择比较，相对原论文CHAIR不适用，小样本诊断不代表稳定能力提升。  multimodal-foundation-model reward-modeling frozen-layer-probe verifier-bootstrap 多模态 跨模态对齐：表征、连接器与监督">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<h2 id="paper-multimodal-models-umrm-4950018b">Unsupervised Multimodal Reward Modeling</h2>
<p class="ar-learning-card__meta">Massachusetts Institute of Technology · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>偏好pair昂贵，reward benchmark名次也不必代表部署选择效用。作者冻结Qwen3-VL，在中间language层只均值池化response tokens，再训练无bias线性reward head；公开caption为positive，同一caption的颜色/数量/尺寸/方位单span变化、tail splice、clause shuffle及cross-image caption为negative，不需人工偏好标注。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>bootstrap另与random own-candidate选择比较，相对原论文CHAIR不适用，小样本诊断不代表稳定能力提升。本地对照口径：零bias-free head的tie计半为pair基线，验证集选中的真实中间层head为实验组；bootstrap另与random own-candidate选择比较，相对原论文CHAIR不适用，小样本诊断不代表稳定能力提升。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12707">原论文</a> · <a href="../../../../reproductions/2610.12707-umrm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="EmbeddingGemma 2: Open Multimodal Embeddings 多模态大模型 Google DeepMind 2026-10-06 EmbeddingGemma 2 将文本、图像、音频与视频映射到统一的 768 维空间，支持检索、分类和聚类。独立模态塔可以按需关闭；文本使用任务前缀，输出经 attention-mask 均值池化，MRL 允许保留前 128/256/512 维并重新归一化，以权衡质量与向量存储成本。官方总参数约 740M，其中文本约 270M、视觉约 170M、音频约 300M。本地只实例化文本和视觉，约 440M，不使用随机小模型代替官方 checkpoint。 使用独立环境，避免改变旧论文依赖的 HF Hub &lt;2 环境。固定官方 Transformers 源码，而不是长期依赖浮动 main；缺少架构时直接报错，不换成别的 embedding 模型。  多模态基础模型 跨模态检索 Matryoshka 表示 多模态 跨模态对齐：表征、连接器与监督">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<h2 id="paper-multimodal-models-embedding-gemma2-1f83fce4">EmbeddingGemma 2: Open Multimodal Embeddings</h2>
<p class="ar-learning-card__meta">Google DeepMind · 论文公开：2026-10-06</p>
<p><strong>方法要点：</strong>EmbeddingGemma 2 将文本、图像、音频与视频映射到统一的 768 维空间，支持检索、分类和聚类。独立模态塔可以按需关闭；文本使用任务前缀，输出经 attention-mask 均值池化，MRL 允许保留前 128/256/512 维并重新归一化，以权衡质量与向量存储成本。官方总参数约 740M，其中文本约 270M、视觉约 170M、音频约 300M。本地只实例化文本和视觉，约 440M，不使用随机小模型代替官方 checkpoint。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>使用独立环境，避免改变旧论文依赖的 HF Hub &lt;2 环境。固定官方 Transformers 源码，而不是长期依赖浮动 main；缺少架构时直接报错，不换成别的 embedding 模型。</p></details>
<p class="ar-learning-card__links"><a href="https://blog.google/innovation-and-ai/technology/developers-tools/embeddinggemma-2/">原论文</a> · <a href="../../../../multimodal-models/embeddinggemma2/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Omni-Embed-Mini: Binding Modalities Without Forgetting via Dense Distillation 基础模型 原文首页未列第一作者机构 2026-10-01 冻结文本骨干，把每个媒体样本的稠密级联描述经同一文本骨干得到 teacher target，再训练轻量投影器和分阶段 LoRA 对齐六种模态。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行同几何空间的稠密描述蒸馏；未训练模态编码器或复现实测榜单。执行同几何空间的稠密描述蒸馏；未训练模态编码器或复现实测榜单。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  多模态嵌入 蒸馏 LoRA 多模态 跨模态对齐：表征、连接器与监督">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<h2 id="paper-foundation-models-omni-embed-mini-210068e5">Omni-Embed-Mini: Binding Modalities Without Forgetting via Dense Distillation</h2>
<p class="ar-learning-card__meta">原文首页未列第一作者机构 · 论文公开：2026-10-01</p>
<p><strong>方法要点：</strong>冻结文本骨干，把每个媒体样本的稠密级联描述经同一文本骨干得到 teacher target，再训练轻量投影器和分阶段 LoRA 对齐六种模态。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行同几何空间的稠密描述蒸馏；未训练模态编码器或复现实测榜单。执行同几何空间的稠密描述蒸馏；未训练模态编码器或复现实测榜单。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02148">原论文</a> · <a href="../../../../foundation-models/2610.02148-omni-embed-mini/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="SenseNova-U1.5: Towards Native Unified Visual Intelligence 基础模型 SenseTime Research 2026-09-10 用空间 patch reconstruction 摆脱 tokenizer/VAE，并以多专家 OPD 统一视觉理解与生成后训练。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 masked patch target 与 expert OPD 融合；未复刻 8B 多阶段训练。本地执行 masked patch target 与 expert OPD 融合；未复刻 8B 多阶段训练。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  统一多模态 视觉生成与理解 多模态 跨模态对齐：表征、连接器与监督">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<h2 id="paper-foundation-models-sensenova-u1-5-44bbf8fb">SenseNova-U1.5: Towards Native Unified Visual Intelligence</h2>
<p class="ar-learning-card__meta">SenseTime Research · 论文公开：2026-09-10</p>
<p><strong>方法要点：</strong>用空间 patch reconstruction 摆脱 tokenizer/VAE，并以多专家 OPD 统一视觉理解与生成后训练。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 masked patch target 与 expert OPD 融合；未复刻 8B 多阶段训练。本地执行 masked patch target 与 expert OPD 融合；未复刻 8B 多阶段训练。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11929">原论文</a> · <a href="../../../../foundation-models/2609.11929-sensenova-u1-5/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="From Visual Cues to Spoken Narration: Rethinking Audio Description 多模态大模型 TU Darmstadt &amp; hessian.AI 2026-09-01 固定v1 Section4.3 Eqs5–8：SFT按每个AD目标token求和；positive/negative评分均为同一当前模型和prompt上的token-mean logp，prompt/padding排除；DRL=-logsigmoid((s+−s−)/0.5)，全loss加0.2DRL。离线负caption生成冻结，但其当前模型likelihood仍反传。 成本过高，不复现（审查 DONE）。6.64M双头定位器，Qwen2.5-VL-7B/Qwen3-VL-8B LoRA，训练32帧/推理64帧，多阶段长电影训练；LSMDC研究限制授权、MAD-Eval NDA。完整数据/定位+VLM训练超单卡短时预算，不下载视频或权重；本文未给总GPU小时，不编造。输入是当前模型对AD与缓存negative caption的teacher-forced logits/labels，必须正确对齐并以-100排除prompt/padding；不包含Stage1、visual cue提取、character bank或负caption生成。  多模态生成 视频音频描述 多模态 跨模态对齐：表征、连接器与监督">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<h2 id="paper-multimodal-models-cue2narrate-drl-b44764fd">From Visual Cues to Spoken Narration: Rethinking Audio Description</h2>
<p class="ar-learning-card__meta">TU Darmstadt &amp; hessian.AI · 论文公开：2026-09-01</p>
<p><strong>方法要点：</strong>固定v1 Section4.3 Eqs5–8：SFT按每个AD目标token求和；positive/negative评分均为同一当前模型和prompt上的token-mean logp，prompt/padding排除；DRL=-logsigmoid((s+−s−)/0.5)，全loss加0.2DRL。离线负caption生成冻结，但其当前模型likelihood仍反传。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。6.64M双头定位器，Qwen2.5-VL-7B/Qwen3-VL-8B LoRA，训练32帧/推理64帧，多阶段长电影训练；LSMDC研究限制授权、MAD-Eval NDA。完整数据/定位+VLM训练超单卡短时预算，不下载视频或权重；本文未给总GPU小时，不编造。输入是当前模型对AD与缓存negative caption的teacher-forced logits/labels，必须正确对齐并以-100排除prompt/padding；不包含Stage1、visual cue提取、character bank或负caption生成。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.01725v1">原论文</a> · <a href="../../../../multimodal-models/2609.01725-cue2narrate-drl/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="MLLMCLIP: Feature-Level Distillation of MLLM for Robust Vision-Language Representations 基础模型 KAIST / Sony AI 2026-08-26 MLLM 的丰富视觉语义难以直接迁移到轻量 CLIP。论文从 teacher 各层按 attention 自适应选 token，以 CKA 对齐 student 图像/文本特征，保留部署时的双塔效率。 Fidelity：公开 checkpoint 核心路径。主路径加载真实 SmolVLM teacher 与 CLIP student，在公开图像上训练 CKA projection；MovieLens/NumPy 路径仅保留为快速机制诊断。真实 checkpoint 路径使用公开图像和 SmolVLM 视觉 encoder feature，但仍未复刻论文完整 26-benchmark 训练规模、原始 teacher 配方与全量 CLIP 预训练。MovieLens proxy 仍为 diagnostic-only，不能与视觉 benchmark 混报。  multimodal-foundation-model feature-distillation compositionality cka 多模态 跨模态对齐：表征、连接器与监督">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<h2 id="paper-foundation-models-mllmclip-2c53372a">MLLMCLIP: Feature-Level Distillation of MLLM for Robust Vision-Language Representations</h2>
<p class="ar-learning-card__meta">KAIST / Sony AI · 论文公开：2026-08-26</p>
<p><strong>方法要点：</strong>MLLM 的丰富视觉语义难以直接迁移到轻量 CLIP。论文从 teacher 各层按 attention 自适应选 token，以 CKA 对齐 student 图像/文本特征，保留部署时的双塔效率。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity：公开 checkpoint 核心路径。主路径加载真实 SmolVLM teacher 与 CLIP student，在公开图像上训练 CKA projection；MovieLens/NumPy 路径仅保留为快速机制诊断。真实 checkpoint 路径使用公开图像和 SmolVLM 视觉 encoder feature，但仍未复刻论文完整 26-benchmark 训练规模、原始 teacher 配方与全量 CLIP 预训练。MovieLens proxy 仍为 diagnostic-only，不能与视觉 benchmark 混报。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25575">原论文</a> · <a href="../../../../reproductions/2608.25575-mllmclip/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="WeMM-Embedding: WeChat Multi-Modal Embedding Technical Report 基础模型 WeChat Vision, Tencent 2026-08-25 不同检索任务通常维护独立的文本、图像、视频或文档 encoder。WeMM 把任意交错多模态输入映射到同一空间：第一阶段用数亿 pair 做大规模 alignment；第二阶段加入精选 relevance、细粒度监督和跨尺度知识迁移，并用 Matryoshka 表征支持按成本选择输出维度。 Fidelity：核心机制复现。本地执行两阶段跨模态对齐、cross-scale teacher refinement 与 Matryoshka 截断评测；未冒充 2B/4B/9B checkpoint 训练。没有加载原始大 checkpoint 或私有多模态 pair；公开 MovieLens 的内容/协同视图只验证共享空间、两阶段 refinement 与截断维度机制，不代表 MMEB-v2 或微信业务结果复刻。本地对照口径：基线为第一阶段共享空间；实验组加入 relevance/cross-scale teacher refinement。  multimodal-foundation-model embedding retrieval matryoshka-representation 多模态 跨模态对齐：表征、连接器与监督">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<h2 id="paper-foundation-models-wemm-embedding-30d32b14">WeMM-Embedding: WeChat Multi-Modal Embedding Technical Report</h2>
<p class="ar-learning-card__meta">WeChat Vision, Tencent · 论文公开：2026-08-25</p>
<p><strong>方法要点：</strong>不同检索任务通常维护独立的文本、图像、视频或文档 encoder。WeMM 把任意交错多模态输入映射到同一空间：第一阶段用数亿 pair 做大规模 alignment；第二阶段加入精选 relevance、细粒度监督和跨尺度知识迁移，并用 Matryoshka 表征支持按成本选择输出维度。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity：核心机制复现。本地执行两阶段跨模态对齐、cross-scale teacher refinement 与 Matryoshka 截断评测；未冒充 2B/4B/9B checkpoint 训练。没有加载原始大 checkpoint 或私有多模态 pair；公开 MovieLens 的内容/协同视图只验证共享空间、两阶段 refinement 与截断维度机制，不代表 MMEB-v2 或微信业务结果复刻。本地对照口径：基线为第一阶段共享空间；实验组加入 relevance/cross-scale teacher refinement。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24053">原论文</a> · <a href="../../../../reproductions/2608.24053-wemm-embedding/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Generation as Auxiliary Supervision: Enhancing Visual Understanding at Zero Inference Overhead via Decoupled Embedding Prediction 基础模型 ByteDance 2026-08-12 常规 MLLM 只用文本 next-token loss，视觉结构只能被语言间接监督；统一理解/生成模型又会把生成参数和开销留到部署阶段。GAS 把生成改成纯训练期辅助任务：理解分支与生成分支共享较低层视觉路径，上层 Transformer 参数解耦；生成分支在与 LLM 输入相同的连续视觉空间自回归预测目标图像 embedding。这样生成梯度能改善共享视觉表征，又不会直接改写理解上层，部署时可整条删除。 Fidelity：核心机制复现。本地真实训练共享视觉 trunk、独立 MoT 生成上层、连续 Next Embedding Prediction（NEP）与 EMA target；未复刻 2B/4B Qwen3-VL、10M 生成数据和 32-GPU 两阶段训练。本地用水平镜像后的同类目标图像构造高度相关的生成任务，并在连续 patch embedding 空间执行 shifted cosine NEP；保留 EMA、渐增、分支隔离与推理删除机制。结果只说明小规模公开数据上的机制可执行，不能与论文 10M 生成样本和 2B/4B benchmark 数字直接比较。  multimodal generation-guided-training next-embedding-prediction 多模态 跨模态对齐：表征、连接器与监督">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<h2 id="paper-foundation-models-gas-1fb6a8b0">Generation as Auxiliary Supervision: Enhancing Visual Understanding at Zero Inference Overhead via Decoupled Embedding Prediction</h2>
<p class="ar-learning-card__meta">ByteDance · 论文公开：2026-08-12</p>
<p><strong>方法要点：</strong>常规 MLLM 只用文本 next-token loss，视觉结构只能被语言间接监督；统一理解/生成模型又会把生成参数和开销留到部署阶段。GAS 把生成改成纯训练期辅助任务：理解分支与生成分支共享较低层视觉路径，上层 Transformer 参数解耦；生成分支在与 LLM 输入相同的连续视觉空间自回归预测目标图像 embedding。这样生成梯度能改善共享视觉表征，又不会直接改写理解上层，部署时可整条删除。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity：核心机制复现。本地真实训练共享视觉 trunk、独立 MoT 生成上层、连续 Next Embedding Prediction（NEP）与 EMA target；未复刻 2B/4B Qwen3-VL、10M 生成数据和 32-GPU 两阶段训练。本地用水平镜像后的同类目标图像构造高度相关的生成任务，并在连续 patch embedding 空间执行 shifted cosine NEP；保留 EMA、渐增、分支隔离与推理删除机制。结果只说明小规模公开数据上的机制可执行，不能与论文 10M 生成样本和 2B/4B benchmark 数字直接比较。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.12209">原论文</a> · <a href="../../../../reproductions/2608.12209-gas/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Towards Physics of Multimodal Pretraining: Knowledge Flow, Modality Synergy, Early Unification, and Recipes 基础模型 Meta 2026-08-05 用受控实验刻画模态知识流、协同/竞争、早期统一和共享 attention+norm/模态专属 FFN 配方。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 single-modality representation，实验组为 physics-mm-pretraining；单 seed 变化为 +0.00% 个百分点。  多模态基础模型 预训练与数据 多模态 跨模态对齐：表征、连接器与监督">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<h2 id="paper-foundation-models-physics-mm-pretraining-bcf29586">Towards Physics of Multimodal Pretraining: Knowledge Flow, Modality Synergy, Early Unification, and Recipes</h2>
<p class="ar-learning-card__meta">Meta · 论文公开：2026-08-05</p>
<p><strong>方法要点：</strong>用受控实验刻画模态知识流、协同/竞争、早期统一和共享 attention+norm/模态专属 FFN 配方。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。本地对照口径：基线为同样本 single-modality representation，实验组为 physics-mm-pretraining；单 seed 变化为 +0.00% 个百分点。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05000">原论文</a> · <a href="../../../../reproductions/2608.05000-physics-mm-pretraining/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="ReToken: One Token to Improve Vision–Language Models for Visual Retrieval 基础模型 UIUC / Microsoft Research / Google DeepMind 2026-07-30 常规 VLM 检索需要先用外部 retriever 找图，再把入选图重新编码，无法直接复用预填充的视觉 KV cache。ReToken 在输入中增加一个可学习 token，让它在最后一层 value projection 空间与每张图的平均 value 向量打分；只训练该 token 和一张投影矩阵，以 class-balanced BCE 监督相关/无关图，VLM 默认冻结。 Fidelity: 核心机制复现。实际训练单个 retrieval target、value-space projection 与稀疏 cache 选择，并接入 LLM evolve；本地文本实验不冒充完整 VLM。本地没有运行冻结大 VLM、MIRAGE 图文监督和两小时视频；文本 token cache 只复现论文决定性的“单 retrieval target + value-space 打分 + 稀疏选择”机制，不能与论文视觉 benchmark 数字直接比较。本地对照口径：基线为同预算 dense LLaMA，实验组为 ReToken value-cache Top-K；相对基线 PPL +3.70%（变差）。  vision-language-model visual-retrieval kv-cache sparse-attention 多模态 跨模态对齐：表征、连接器与监督">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<h2 id="paper-foundation-models-retoken-1f7ac688">ReToken: One Token to Improve Vision–Language Models for Visual Retrieval</h2>
<p class="ar-learning-card__meta">UIUC / Microsoft Research / Google DeepMind · 论文公开：2026-07-30</p>
<p><strong>方法要点：</strong>常规 VLM 检索需要先用外部 retriever 找图，再把入选图重新编码，无法直接复用预填充的视觉 KV cache。ReToken 在输入中增加一个可学习 token，让它在最后一层 value projection 空间与每张图的平均 value 向量打分；只训练该 token 和一张投影矩阵，以 class-balanced BCE 监督相关/无关图，VLM 默认冻结。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。实际训练单个 retrieval target、value-space projection 与稀疏 cache 选择，并接入 LLM evolve；本地文本实验不冒充完整 VLM。本地没有运行冻结大 VLM、MIRAGE 图文监督和两小时视频；文本 token cache 只复现论文决定性的“单 retrieval target + value-space 打分 + 稀疏选择”机制，不能与论文视觉 benchmark 数字直接比较。本地对照口径：基线为同预算 dense LLaMA，实验组为 ReToken value-cache Top-K；相对基线 PPL +3.70%（变差）。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28627">原论文</a> · <a href="../../../../reproductions/2607.28627-retoken/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="MVEB: Massive Video Embedding Benchmark 多模态大模型 Harvard University 2026-06-12 固定v1 Section3：MVEB23任务从184任务池缩减；var-length fps2/cap64frames，固定帧模型遵循其训练配置，音频按model采样率/长度；无per-task finetune。分类8shot frozen logistic probe，retrieval cosine/nDCG10，VCQA候选池accuracy，视频/音频版本配对且只跑模型支持modality。 成本过高，不复现（审查 DONE）。33个公开checkpoint约200M–10.7B，23主任务及184池，多模型视频+音频/8方向矩阵；Table1单H100测LCO7B：MVEB31.9h、MVEB+302.7h。远超单A100/A30短时预算，不下载模型或视频、不构造假的通用指标代理。本轮仅核查论文身份、合作机构、方法/资源/许可证与成本，收录资料和原图。没有把通用聚合器或字段检查包装为官方benchmark接口；没有模型调用、训练或正式指标。  多模态表征 视频嵌入评测 多模态 跨模态对齐：表征、连接器与监督">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<h2 id="paper-multimodal-models-mveb-9298f9f8">MVEB: Massive Video Embedding Benchmark</h2>
<p class="ar-learning-card__meta">Harvard University · 论文公开：2026-06-12</p>
<p><strong>方法要点：</strong>固定v1 Section3：MVEB23任务从184任务池缩减；var-length fps2/cap64frames，固定帧模型遵循其训练配置，音频按model采样率/长度；无per-task finetune。分类8shot frozen logistic probe，retrieval cosine/nDCG10，VCQA候选池accuracy，视频/音频版本配对且只跑模型支持modality。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。33个公开checkpoint约200M–10.7B，23主任务及184池，多模型视频+音频/8方向矩阵；Table1单H100测LCO7B：MVEB31.9h、MVEB+302.7h。远超单A100/A30短时预算，不下载模型或视频、不构造假的通用指标代理。本轮仅核查论文身份、合作机构、方法/资源/许可证与成本，收录资料和原图。没有把通用聚合器或字段检查包装为官方benchmark接口；没有模型调用、训练或正式指标。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.14958v1">原论文</a> · <a href="../../../../multimodal-models/2606.14958-mveb/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="NaijaS2ST: A Multi-Accent Benchmark for Speech-to-Speech Translation in Low-Resource Nigerian Languages 多模态大模型 Mila - Quebec AI Institute 2026-04-17 核固定v3 Sections3–4及AppendixC：284说话人、约6K平行句、质控后约269h；5shot来自DEV，方向分开；Seamless不支持的Hausa映射Arabic、Naijá映射French仅为fine-tuned extension。S2TT SSA-COMET/ChrF++，S2ST先OmnilingualASR转写再SSA-COMET，不能用文本exactmatch替代。 成本过高，不复现（审查 DONE）。每语言40余小时语音，Omnilingual-ASR1B、NLLB3.3B/TinyAya3B、Seamless2.3B mono/multi多个方向3–10epochs，另有Gemini/GPT-Audio推理、TTS和人工评审。整套明显超单卡短时预算，不下载音频/模型、不调用付费API。本轮仅核查论文身份、合作机构、方法/资源/许可证与成本，收录资料和原图。没有把通用聚合器或字段检查包装为官方benchmark接口；没有模型调用、训练或正式指标。  语音多模态 低资源语音翻译评测 多模态 跨模态对齐：表征、连接器与监督">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<h2 id="paper-multimodal-models-naijas2st-20646330">NaijaS2ST: A Multi-Accent Benchmark for Speech-to-Speech Translation in Low-Resource Nigerian Languages</h2>
<p class="ar-learning-card__meta">Mila - Quebec AI Institute · 论文公开：2026-04-17</p>
<p><strong>方法要点：</strong>核固定v3 Sections3–4及AppendixC：284说话人、约6K平行句、质控后约269h；5shot来自DEV，方向分开；Seamless不支持的Hausa映射Arabic、Naijá映射French仅为fine-tuned extension。S2TT SSA-COMET/ChrF++，S2ST先OmnilingualASR转写再SSA-COMET，不能用文本exactmatch替代。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。每语言40余小时语音，Omnilingual-ASR1B、NLLB3.3B/TinyAya3B、Seamless2.3B mono/multi多个方向3–10epochs，另有Gemini/GPT-Audio推理、TTS和人工评审。整套明显超单卡短时预算，不下载音频/模型、不调用付费API。本轮仅核查论文身份、合作机构、方法/资源/许可证与成本，收录资料和原图。没有把通用聚合器或字段检查包装为官方benchmark接口；没有模型调用、训练或正式指标。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.16287v1">原论文</a> · <a href="../../../../multimodal-models/2604.16287-naijas2st/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="SmolVLM: Redefining small and efficient multimodal models 基础模型 Hugging Face 2025-04-07 SmolVLM 重新分配小模型视觉/语言侧算力，以 pixel shuffle 将相邻空间 token 搬到 channel 维，再用 MLP 映射到 LM 空间；同时研究长上下文、图像切片、学习位置 token 和数据配比，使 256M/500M/2.2B 模型在低显存下保持图像与视频能力。 保真度：核心机制复现。保真度：核心机制复现。本地执行论文中心的 pixel-shuffle 视觉 token 压缩与投影；未复刻 256M–2.2B decoder、视频和完整数据配方。使用 32×32 真实服饰图像和 2×2 space-to-depth；没有复刻高分辨率切片、视频采样、8k/16k context、学习位置 token 或 SmolLM decoder。本地对照口径：基线为线性 mean-pooling connector，实验组为 r=2 pixel shuffle + projector；  multimodal efficient-vlm visual-token-compression 多模态 跨模态对齐：表征、连接器与监督">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<h2 id="paper-foundation-models-smolvlm-5de2167d">SmolVLM: Redefining small and efficient multimodal models</h2>
<p class="ar-learning-card__meta">Hugging Face · 论文公开：2025-04-07</p>
<p><strong>方法要点：</strong>SmolVLM 重新分配小模型视觉/语言侧算力，以 pixel shuffle 将相邻空间 token 搬到 channel 维，再用 MLP 映射到 LM 空间；同时研究长上下文、图像切片、学习位置 token 和数据配比，使 256M/500M/2.2B 模型在低显存下保持图像与视频能力。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。本地执行论文中心的 pixel-shuffle 视觉 token 压缩与投影；未复刻 256M–2.2B decoder、视频和完整数据配方。使用 32×32 真实服饰图像和 2×2 space-to-depth；没有复刻高分辨率切片、视频采样、8k/16k context、学习位置 token 或 SmolLM decoder。本地对照口径：基线为线性 mean-pooling connector，实验组为 r=2 pixel shuffle + projector；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.05299">原论文</a> · <a href="../../../../reproductions/2504.05299-smolvlm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features 基础模型 Google DeepMind 2025-02-20 SigLIP 2 在 SigLIP 的 pairwise sigmoid loss 上组合 captioning pretraining、global-local self-distillation、masked prediction、在线数据筛选和 NaFlex 动态分辨率，改善语义、定位、dense feature 与多语言公平性。 保真度：核心机制复现。保真度：核心机制复现。本地执行 sigmoid 对比目标与遮盖视图自蒸馏；未复刻多语言 web 数据、caption decoder 和 dense localization。Fashion-MNIST 类别文本替代多语言 caption；实际训练 sigmoid pair loss 和中心遮盖视图的 student-teacher consistency，没有复刻 caption decoder、active curation、NaFlex 和定位头。  multimodal sigmoid-contrastive self-distillation 多模态 跨模态对齐：表征、连接器与监督">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<h2 id="paper-foundation-models-siglip2-8c923237">SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features</h2>
<p class="ar-learning-card__meta">Google DeepMind · 论文公开：2025-02-20</p>
<p><strong>方法要点：</strong>SigLIP 2 在 SigLIP 的 pairwise sigmoid loss 上组合 captioning pretraining、global-local self-distillation、masked prediction、在线数据筛选和 NaFlex 动态分辨率，改善语义、定位、dense feature 与多语言公平性。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。本地执行 sigmoid 对比目标与遮盖视图自蒸馏；未复刻多语言 web 数据、caption decoder 和 dense localization。Fashion-MNIST 类别文本替代多语言 caption；实际训练 sigmoid pair loss 和中心遮盖视图的 student-teacher consistency，没有复刻 caption decoder、active curation、NaFlex 和定位头。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.14786">原论文</a> · <a href="../../../../reproductions/2502.14786-siglip2/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Visual Instruction Tuning 基础模型 University of Wisconsin-Madison / Microsoft Research / Columbia University 2023-04-17 冻结视觉 encoder，用可训练 projector 把视觉特征映射到 LLM token 空间，再在 GPT-4 生成的多模态指令数据上做端到端 instruction tuning。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。使用 Fashion-MNIST 真实像素、冻结的轻量 patch encoder、可训练 projector 与问答分类头；未调用 GPT-4，未执行多模态 instruction data generation，也未复刻 LLaVA-13B。单 seed 结果仅用于检验 projector 结构，不能外推到大模型指令微调。  multimodal instruction-tuning 多模态 跨模态对齐：表征、连接器与监督">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<h2 id="paper-foundation-models-llava-9b58a1f9">Visual Instruction Tuning</h2>
<p class="ar-learning-card__meta">University of Wisconsin-Madison / Microsoft Research / Columbia University · 论文公开：2023-04-17</p>
<p><strong>方法要点：</strong>冻结视觉 encoder，用可训练 projector 把视觉特征映射到 LLM token 空间，再在 GPT-4 生成的多模态指令数据上做端到端 instruction tuning。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。使用 Fashion-MNIST 真实像素、冻结的轻量 patch encoder、可训练 projector 与问答分类头；未调用 GPT-4，未执行多模态 instruction data generation，也未复刻 LLaVA-13B。单 seed 结果仅用于检验 projector 结构，不能外推到大模型指令微调。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2304.08485">原论文</a> · <a href="../../../../reproductions/2304.08485-llava/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models 基础模型 Salesforce Research 2023-01-30 BLIP-2 冻结已有视觉 encoder 和 LLM，只训练轻量 Q-Former。固定数量的可学习 query 通过 cross-attention 从视觉 token 提取与语言最相关的信息；第一阶段做图文表征学习，第二阶段将 query 输出投影成冻结 LLM 的 soft visual prompt。 保真度：核心机制复现。保真度：核心机制复现。本地执行 Q-Former 的可学习 query 与 cross-attention；论文两阶段大规模预训练和冻结大模型未复刻。使用 Fashion-MNIST 真实像素和四 query multi-head cross-attention；没有加载 ViT-g、OPT/FlanT5，也没有执行 ITC/ITM/ITG 两阶段 129M 图像预训练。本地对照口径：基线为相同预算的线性 mean-pooling connector，实验组为四 query Q-Former；  multimodal q-former frozen-encoders 多模态 跨模态对齐：表征、连接器与监督">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<h2 id="paper-foundation-models-blip2-9ce69b95">BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models</h2>
<p class="ar-learning-card__meta">Salesforce Research · 论文公开：2023-01-30</p>
<p><strong>方法要点：</strong>BLIP-2 冻结已有视觉 encoder 和 LLM，只训练轻量 Q-Former。固定数量的可学习 query 通过 cross-attention 从视觉 token 提取与语言最相关的信息；第一阶段做图文表征学习，第二阶段将 query 输出投影成冻结 LLM 的 soft visual prompt。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。本地执行 Q-Former 的可学习 query 与 cross-attention；论文两阶段大规模预训练和冻结大模型未复刻。使用 Fashion-MNIST 真实像素和四 query multi-head cross-attention；没有加载 ViT-g、OPT/FlanT5，也没有执行 ITC/ITM/ITG 两阶段 129M 图像预训练。本地对照口径：基线为相同预算的线性 mean-pooling connector，实验组为四 query Q-Former；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2301.12597">原论文</a> · <a href="../../../../reproductions/2301.12597-blip2/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/alignment-interfaces" data-search="Learning Transferable Visual Models From Natural Language Supervision 基础模型 OpenAI 2021-02-26 用独立图像/文本 encoder 将配对样本映射到同一单位球面，通过双向 batch contrastive objective 学习可迁移零样本表示。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。使用 Fashion-MNIST 的真实像素与类别文本复现双塔、归一化和对称式对比目标；没有复刻 4 亿图文对、自然语言长尾语义或大规模视觉 encoder。单 seed 小预算结果只验证机制可执行，不等价于原论文 zero-shot 指标。本地对照口径：在真实 Fashion-MNIST 图像与类别文本构成的 10 类图文任务上，基线为均匀随机检索（10.0%），实验组为对称式图文对比学习双塔；测试准确率达到 72.0%（+62.0 个百分点），打乱图像后降至 10.3%，说明结果依赖视觉输入。  multimodal contrastive-pretraining 多模态 跨模态对齐：表征、连接器与监督">
<p class="ar-learning-card__domain"><a href="./">多模态 / 跨模态对齐：表征、连接器与监督</a></p>
<h2 id="paper-foundation-models-clip-b03c09f0">Learning Transferable Visual Models From Natural Language Supervision</h2>
<p class="ar-learning-card__meta">OpenAI · 论文公开：2021-02-26</p>
<p><strong>方法要点：</strong>用独立图像/文本 encoder 将配对样本映射到同一单位球面，通过双向 batch contrastive objective 学习可迁移零样本表示。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。使用 Fashion-MNIST 的真实像素与类别文本复现双塔、归一化和对称式对比目标；没有复刻 4 亿图文对、自然语言长尾语义或大规模视觉 encoder。单 seed 小预算结果只验证机制可执行，不等价于原论文 zero-shot 指标。本地对照口径：在真实 Fashion-MNIST 图像与类别文本构成的 10 类图文任务上，基线为均匀随机检索（10.0%），实验组为对称式图文对比学习双塔；测试准确率达到 72.0%（+62.0 个百分点），打乱图像后降至 10.3%，说明结果依赖视觉输入。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2103.00020">原论文</a> · <a href="../../../../reproductions/2103.00020-clip/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
