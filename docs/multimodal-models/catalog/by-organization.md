# 多模态大模型：按机构/公司/学校

按论文一作第一署名单位聚合；单位内按首次公开日期倒序排列。

## Aalto University

- 2026-10-20 · [Multimodal Reranking Is a System One Decision](../../multimodal-models/2610.28435-system-one-rerank/README.md)（`system-one-rerank`）：论文把重排视作一个选择决策：把 query 和首阶段候选放入同一多模态上下文，让通用视觉语言模型比较全部候选。它不生成排序文本，也不额外训练一个 pointwise reranker，而是在首个答案位置直接读取候选字母的概率。该读出继承 setwise / FIRST 的方法；论文的新论点与实验是通用 VLM 在图像、视觉文档上的零样本表现，以及纯文本 decision tuning 是否迁移到视觉重排。

## Alibaba Cloud Computing

- 2026-10-08 · [V-CoLA: Vision Token Compression with Linear Attention](../../multimodal-models/2610.11251-vcola/README.md)（`vcola`）：传统视觉 Token 筛选依赖 softmax attention 或特征相似度，不能直接迁移到包含 Gated DeltaNet 的混合 VLM。V-CoLA 用线性注意力最终状态的可回读程度衡量长期保留，再用更新前后状态对短窗口 query 的响应变化衡量独特性；按累计重要性划分连续块并加权合并，深层再退出视觉 Token。[方法见官方正文第 3 节](https://arxiv.org/html/2610.11251v1#S3)。

## ByteDance

- 2026-08-12 · [Generation as Auxiliary Supervision: Enhancing Visual Understanding at Zero Inference Overhead via Decoupled Embedding Prediction](../../reproductions/2608.12209-gas/README.md)（`gas`）：常规 MLLM 只用文本 next-token loss，视觉结构只能被语言间接监督；统一理解/生成模型又会把生成参数和开销留到部署阶段。GAS 把生成改成纯训练期辅助任务：理解分支与生成分支共享较低层视觉路径，上层 Transformer 参数解耦；生成分支在与 LLM 输入相同的连续视觉空间自回归预测目标图像 embedding。

## City University of Hong Kong

- 2026-10-08 · [Look Back, Think Ahead: Visual Memory on Demand for Efficient Multimodal Reasoning](../../multimodal-models/2610.12060-vimod/README.md)（`vimod`）：一次性压缩图像可能丢掉后续推理需要的细节。DART 学习可变区域大小和成员，生成始终驻留的 Coarse KV；原始 Fine KV 仍保留。TRACE 根据已生成文本的因果隐状态决定保持或替换工作集，通过 Joint-KV 恢复原始细节。

## Google DeepMind

- 2026-10-06 · [EmbeddingGemma 2: Open Multimodal Embeddings](../../multimodal-models/embeddinggemma2/README.md)（`embedding-gemma2`）：EmbeddingGemma 2 将文本、图像、音频与视频映射到统一的 768 维空间，支持检索、分类和聚类。独立模态塔可以按需关闭；文本使用任务前缀，输出经 attention-mask 均值池化，MRL 允许保留前 128/256/512 维并重新归一化，以权衡质量与向量存储成本。
- 2025-02-20 · [SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features](../../reproductions/2502.14786-siglip2/README.md)（`siglip2`）：SigLIP 2 在 SigLIP 的 pairwise sigmoid loss 上组合 captioning pretraining、global-local self-distillation、masked prediction、在线数据筛选和 NaFlex 动态分辨率，改善语义、定位、 dense feature 与多语言公平性。

## Hugging Face

- 2025-04-07 · [SmolVLM: Redefining small and efficient multimodal models](../../reproductions/2504.05299-smolvlm/README.md)（`smolvlm`）：SmolVLM 重新分配小模型视觉/语言侧算力，以 pixel shuffle 将相邻空间 token 搬到 channel 维，再用 MLP 映射到 LM 空间；同时研究长上下文、图像切片、学习位置 token 和数据配比， 使 256M/500M/2.2B 模型在低显存下保持图像与视频能力。

## Massachusetts Institute of Technology

- 2026-10-08 · [Unsupervised Multimodal Reward Modeling](../../reproductions/2610.12707-umrm/README.md)（`umrm`）：偏好pair昂贵，reward benchmark名次也不必代表部署选择效用。作者冻结Qwen3-VL，在中间language层只均值池化response tokens，再训练无bias线性reward head；公开caption为positive，同一caption的颜色/数量/尺寸/方位单span变化、tail splice、clause shuffle及cross-image caption为negative，不需人工偏好标注。

## Northwestern University

- 2026-10-08 · [WOVEN: Weaving Visual World Modeling into Multimodal LLMs](../../reproductions/2610.12417-woven/README.md)（`woven`）：静态识别不等于理解状态变化。WOVEN以$(s,a,s')$为共同对象，用视频生成模型rollout提供结果/中间状态，而非在prompt里预写结果。相同初始状态在不同动作下的rollout提供counterfactual候选；按scene、action、reasoning三个轴形成可控监督，用error-typed distractors区分错误机制。

## OpenAI

- 2021-02-26 · [Learning Transferable Visual Models From Natural Language Supervision](../../reproductions/2103.00020-clip/README.md)（`clip`）：用独立图像/文本 encoder 将配对样本映射到同一单位球面，通过双向 batch contrastive objective 学习可迁移零样本表示。

## Salesforce Research

- 2023-01-30 · [BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models](../../reproductions/2301.12597-blip2/README.md)（`blip2`）：BLIP-2 冻结已有视觉 encoder 和 LLM，只训练轻量 Q-Former。固定数量的可学习 query 通过 cross-attention 从视觉 token 提取与语言最相关的信息；第一阶段做图文表征学习，第二阶段将 query 输出投影成冻结 LLM 的 soft visual prompt。

## Sichuan University

- 2026-09-15 · [StackTok: Accelerating VLMs Inference with Budget-Adaptive Visual Token Selection](../../multimodal-models/2609.16841-stacktok/README.md)（`stacktok`）：把 query relevance 作为目标、coverage 作为随预算变化的支撑约束，逐步在两种选取准则间切换。

## University of Modena and Reggio Emilia

- 2026-06-30 · [Editing Everything Everywhere All at Once](../../multimodal-models/2606.31278-mice/README.md)（`mice`）：多区域同时编辑容易把一处指令的属性传到另一处。MICE 在联合注意力中隔离不同文字组，并用实例掩码的平滑空间偏置控制视觉交互，以兼顾局部绑定与周围区域融合。方法不训练新的编辑模型。

## University of Science and Technology of China

- 2026-09-15 · [VideoMM: Adaptive Macro-Micro Inference for Efficient Video MLLMs](../../multimodal-models/2609.16722-videomm/README.md)（`videomm`）：先在低分辨率 Macro Proxy 上定位相关区域，仅在宏观共识不足时激活高保真 Micro Tokens。

## University of Wisconsin-Madison

- 2023-04-17 · [Visual Instruction Tuning](../../reproductions/2304.08485-llava/README.md)（`llava`）：冻结视觉 encoder，用可训练 projector 把视觉特征映射到 LLM token 空间，再在 GPT-4 生成的多模态指令数据上做端到端 instruction tuning。

## Xiamen University

- 2026-10-09 · [CV-OPD: Contrastive Vision On-policy Distillation](../../reproductions/2610.13264-cv-opd/README.md)（`cv-opd`）：原来的 crop-to-full-image OPD 可以教会模型答案分布，却不必然教会它依赖正确视觉区域。作者在移除答案相关区域后发现，Vision-OPD 仍取得明显高于随机的准确率。CV-OPD 用同图、同尺寸、低 IoU 的负区域构造第二个共享参数教师，把“接近正教师、远离负教师”的约束加入 JSD 蒸馏。
