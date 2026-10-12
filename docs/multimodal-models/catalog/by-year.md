# 多模态大模型：按年份

按 arXiv v1 首次公开年份浏览；同年论文按日期倒序排列。

## 2026

- 2026-10 · [Look Back, Think Ahead: Visual Memory on Demand for Efficient Multimodal Reasoning](../../multimodal-models/2610.12060-vimod/README.md)（`vimod`）：一次性压缩图像可能丢掉后续推理需要的细节。DART 学习可变区域大小和成员，生成始终驻留的 Coarse KV；原始 Fine KV 仍保留。TRACE 根据已生成文本的因果隐状态决定保持或替换工作集，通过 Joint-KV 恢复原始细节。
- 2026-10 · [Unsupervised Multimodal Reward Modeling](../../reproductions/2610.12707-umrm/README.md)（`umrm`）：偏好pair昂贵，reward benchmark名次也不必代表部署选择效用。作者冻结Qwen3-VL，在中间language层只均值池化response tokens，再训练无bias线性reward head；公开caption为positive，同一caption的颜色/数量/尺寸/方位单span变化、tail splice、clause shuffle及cross-image caption为negative，不需人工偏好标注。
- 2026-10 · [V-CoLA: Vision Token Compression with Linear Attention](../../multimodal-models/2610.11251-vcola/README.md)（`vcola`）：传统视觉 Token 筛选依赖 softmax attention 或特征相似度，不能直接迁移到包含 Gated DeltaNet 的混合 VLM。V-CoLA 用线性注意力最终状态的可回读程度衡量长期保留，再用更新前后状态对短窗口 query 的响应变化衡量独特性；按累计重要性划分连续块并加权合并，深层再退出视觉 Token。[方法见官方正文第 3 节](https://arxiv.org/html/2610.11251v1#S3)。
- 2026-10 · [WOVEN: Weaving Visual World Modeling into Multimodal LLMs](../../reproductions/2610.12417-woven/README.md)（`woven`）：静态识别不等于理解状态变化。WOVEN以$(s,a,s')$为共同对象，用视频生成模型rollout提供结果/中间状态，而非在prompt里预写结果。相同初始状态在不同动作下的rollout提供counterfactual候选；按scene、action、reasoning三个轴形成可控监督，用error-typed distractors区分错误机制。
- 2026-09 · [StackTok: Accelerating VLMs Inference with Budget-Adaptive Visual Token Selection](../../multimodal-models/2609.16841-stacktok/README.md)（`stacktok`）：把 query relevance 作为目标、coverage 作为随预算变化的支撑约束，逐步在两种选取准则间切换。
- 2026-09 · [VideoMM: Adaptive Macro-Micro Inference for Efficient Video MLLMs](../../multimodal-models/2609.16722-videomm/README.md)（`videomm`）：先在低分辨率 Macro Proxy 上定位相关区域，仅在宏观共识不足时激活高保真 Micro Tokens。
- 2026-08 · [Generation as Auxiliary Supervision: Enhancing Visual Understanding at Zero Inference Overhead via Decoupled Embedding Prediction](../../reproductions/2608.12209-gas/README.md)（`gas`）：常规 MLLM 只用文本 next-token loss，视觉结构只能被语言间接监督；统一理解/生成模型又会把生成参数和开销留到部署阶段。GAS 把生成改成纯训练期辅助任务：理解分支与生成分支共享较低层视觉路径，上层 Transformer 参数解耦；生成分支在与 LLM 输入相同的连续视觉空间自回归预测目标图像 embedding。

## 2025

- 2025-04 · [SmolVLM: Redefining small and efficient multimodal models](../../reproductions/2504.05299-smolvlm/README.md)（`smolvlm`）：SmolVLM 重新分配小模型视觉/语言侧算力，以 pixel shuffle 将相邻空间 token 搬到 channel 维，再用 MLP 映射到 LM 空间；同时研究长上下文、图像切片、学习位置 token 和数据配比， 使 256M/500M/2.2B 模型在低显存下保持图像与视频能力。
- 2025-02 · [SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features](../../reproductions/2502.14786-siglip2/README.md)（`siglip2`）：SigLIP 2 在 SigLIP 的 pairwise sigmoid loss 上组合 captioning pretraining、global-local self-distillation、masked prediction、在线数据筛选和 NaFlex 动态分辨率，改善语义、定位、 dense feature 与多语言公平性。

## 2023

- 2023-04 · [Visual Instruction Tuning](../../reproductions/2304.08485-llava/README.md)（`llava`）：冻结视觉 encoder，用可训练 projector 把视觉特征映射到 LLM token 空间，再在 GPT-4 生成的多模态指令数据上做端到端 instruction tuning。
- 2023-01 · [BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models](../../reproductions/2301.12597-blip2/README.md)（`blip2`）：BLIP-2 冻结已有视觉 encoder 和 LLM，只训练轻量 Q-Former。固定数量的可学习 query 通过 cross-attention 从视觉 token 提取与语言最相关的信息；第一阶段做图文表征学习，第二阶段将 query 输出投影成冻结 LLM 的 soft visual prompt。

## 2021

- 2021-02 · [Learning Transferable Visual Models From Natural Language Supervision](../../reproductions/2103.00020-clip/README.md)（`clip`）：用独立图像/文本 encoder 将配对样本映射到同一单位球面，通过双向 batch contrastive objective 学习可迁移零样本表示。
