# 多模态大模型：按主题

按跨模态训练目标、连接器与视觉 token 压缩分组；每篇论文独占一行。

## 代码、视频与动作联合生成

- 2026-10-21 · [Agentic World Action Models](../../multimodal-models/2610.30136-aw0/README.md)（`aw0`）：世界动作模型能预测未来视觉和控制轨迹，但通常缺少可组合的技能结构；代码型机器人 Agent 能重用程序，却未必把计划与物理动态预测统一起来。AW-0 在 Mixture-of-Transformers 中组合三个专家：代码专家产生参数化程序片段，视频专家预测未来场景，动作专家产生连续控制。程序既能约束预测，也可在可选执行模式中调用技能库。 **成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。**

## 低资源语音翻译评测

- 2026-04-17 · [NaijaS2ST: A Multi-Accent Benchmark for Speech-to-Speech Translation in Low-Resource Nigerian Languages](../../multimodal-models/2604.16287-naijas2st/README.md)（`naijas2st`）：核固定v3 Sections3–4及AppendixC：284说话人、约6K平行句、质控后约269h；5shot来自DEV，方向分开；Seamless不支持的Hausa映射Arabic、Naijá映射French仅为fine-tuned extension。S2TT SSA-COMET/ChrF++，S2ST先OmnilingualASR转写再SSA-COMET，不能用文本exactmatch替代。 **成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。**

## 冻结中间层探针与验证器自举

- 2026-10-08 · [Unsupervised Multimodal Reward Modeling](../../reproductions/2610.12707-umrm/README.md)（`umrm`）：偏好pair昂贵，reward benchmark名次也不必代表部署选择效用。作者冻结Qwen3-VL，在中间language层只均值池化response tokens，再训练无bias线性reward head；公开caption为positive，同一caption的颜色/数量/尺寸/方位单span变化、tail splice、clause shuffle及cross-image caption为negative，不需人工偏好标注。

## 单次前向结构化重排

- 2026-10-20 · [Multimodal Reranking Is a System One Decision](../../multimodal-models/2610.28435-system-one-rerank/README.md)（`system-one-rerank`）：论文把重排视作一个选择决策：把 query 和首阶段候选放入同一多模态上下文，让通用视觉语言模型比较全部候选。它不生成排序文本，也不额外训练一个 pointwise reranker，而是在首个答案位置直接读取候选字母的概率。该读出继承 setwise / FIRST 的方法；论文的新论点与实验是通用 VLM 在图像、视觉文档上的零样本表现，以及纯文本 decision tuning 是否迁移到视觉重排。

## 图像匹配与稀疏对应

- 2026-10-23 · [FlexGlue: Sparse-to-Dense Feature Matching and Visual Disambiguation](../../multimodal-models/2610.32976-flexglue/README.md)（`flexglue`）：稀疏matcher受两图keypoint重复检测能力限制，dense matcher则昂贵，而且两者常只在共视正样本训练，面对对称建筑等doppelganger会给出高置信假匹配。FlexGlue在stride8全图token网格上先做self/cross attention，再只对给定query插值读取特征并寻找另一图的坐标。局部3×3窗口读取避免全局期望在多个候选间平均；轻量MLP对两个方向的offset bins取期望做局部细化。 **成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。**

## 多实例编辑与注意力隔离

- 2026-06-30 · [Editing Everything Everywhere All at Once](../../multimodal-models/2606.31278-mice/README.md)（`mice`）：多区域同时编辑容易把一处指令的属性传到另一处。MICE 在联合注意力中隔离不同文字组，并用实例掩码的平滑空间偏置控制视觉交互，以兼顾局部绑定与周围区域融合。方法不训练新的编辑模型。

## 对比预训练与自蒸馏

- 2025-02-20 · [SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features](../../reproductions/2502.14786-siglip2/README.md)（`siglip2`）：SigLIP 2 在 SigLIP 的 pairwise sigmoid loss 上组合 captioning pretraining、global-local self-distillation、masked prediction、在线数据筛选和 NaFlex 动态分辨率，改善语义、定位、 dense feature 与多语言公平性。

## 生成辅助监督与理解增强

- 2026-08-12 · [Generation as Auxiliary Supervision: Enhancing Visual Understanding at Zero Inference Overhead via Decoupled Embedding Prediction](../../reproductions/2608.12209-gas/README.md)（`gas`）：常规 MLLM 只用文本 next-token loss，视觉结构只能被语言间接监督；统一理解/生成模型又会把生成参数和开销留到部署阶段。GAS 把生成改成纯训练期辅助任务：理解分支与生成分支共享较低层视觉路径，上层 Transformer 参数解耦；生成分支在与 LLM 输入相同的连续视觉空间自回归预测目标图像 embedding。

## 统一动作表示与条件注意力

- 2026-10-23 · [UniAction: Unified Action Conditioning for World Models](../../multimodal-models/2610.32977-uniaction/README.md)（`uniaction`）：异质动作以不同粒度编码，token较多的动作在同一softmax中会仅因数量而占据更大attention mass。UniAction以共享semantic codebook编码元素身份，将(t,y,x)送入既有视频模型的native positional mechanism，再对action部分统一加一个基数bias，保持action内部相对logits不变，同时移除总mass对Na的线性依赖。

## 视觉 token 与跨模态检索

- 2026-10-06 · [EmbeddingGemma 2: Unified and Efficient Multimodal Representations](../../multimodal-models/embeddinggemma2/README.md)（`embedding-gemma2`）：EmbeddingGemma 2 将文本、图像、音频与视频映射到统一的 768 维空间，支持检索、分类和聚类。独立模态塔可以按需关闭；文本使用任务前缀，输出经 attention-mask 均值池化，MRL 允许保留前 128/256/512 维并重新归一化，以权衡质量与向量存储成本。
- 2026-09-15 · [StackTok: Accelerating VLMs Inference with Budget-Adaptive Visual Token Selection](../../multimodal-models/2609.16841-stacktok/README.md)（`stacktok`）：把 query relevance 作为目标、coverage 作为随预算变化的支撑约束，逐步在两种选取准则间切换。
- 2023-04-17 · [Visual Instruction Tuning](../../reproductions/2304.08485-llava/README.md)（`llava`）：冻结视觉 encoder，用可训练 projector 把视觉特征映射到 LLM token 空间，再在 GPT-4 生成的多模态指令数据上做端到端 instruction tuning。
- 2021-02-26 · [Learning Transferable Visual Models From Natural Language Supervision](../../reproductions/2103.00020-clip/README.md)（`clip`）：用独立图像/文本 encoder 将配对样本映射到同一单位球面，通过双向 batch contrastive objective 学习可迁移零样本表示。

## 视觉 token 压缩与动态证据恢复

- 2026-10-08 · [Look Back, Think Ahead: Visual Memory on Demand for Efficient Multimodal Reasoning](../../multimodal-models/2610.12060-vimod/README.md)（`vimod`）：一次性压缩图像可能丢掉后续推理需要的细节。DART 学习可变区域大小和成员，生成始终驻留的 Coarse KV；原始 Fine KV 仍保留。TRACE 根据已生成文本的因果隐状态决定保持或替换工作集，通过 Joint-KV 恢复原始细节。
- 2026-10-08 · [V-CoLA: Vision Token Compression with Linear Attention](../../multimodal-models/2610.11251-vcola/README.md)（`vcola`）：传统视觉 Token 筛选依赖 softmax attention 或特征相似度，不能直接迁移到包含 Gated DeltaNet 的混合 VLM。V-CoLA 用线性注意力最终状态的可回读程度衡量长期保留，再用更新前后状态对短窗口 query 的响应变化衡量独特性；按累计重要性划分连续块并加权合并，深层再退出视觉 Token。[方法见官方正文第 3 节](https://arxiv.org/html/2610.11251v1#S3)。

## 视觉状态转移监督

- 2026-10-08 · [WOVEN: Weaving Visual World Modeling into Multimodal LLMs](../../reproductions/2610.12417-woven/README.md)（`woven`）：静态识别不等于理解状态变化。WOVEN以$(s,a,s')$为共同对象，用视频生成模型rollout提供结果/中间状态，而非在prompt里预写结果。相同初始状态在不同动作下的rollout提供counterfactual候选；按scene、action、reasoning三个轴形成可控监督，用error-typed distractors区分错误机制。

## 视觉证据约束蒸馏

- 2026-10-09 · [CV-OPD: Contrastive Vision On-policy Distillation](../../reproductions/2610.13264-cv-opd/README.md)（`cv-opd`）：原来的 crop-to-full-image OPD 可以教会模型答案分布，却不必然教会它依赖正确视觉区域。作者在移除答案相关区域后发现，Vision-OPD 仍取得明显高于随机的准确率。CV-OPD 用同图、同尺寸、低 IoU 的负区域构造第二个共享参数教师，把“接近正教师、远离负教师”的约束加入 JSD 蒸馏。

## 视频嵌入统一评测

- 2026-06-12 · [MVEB: Massive Video Embedding Benchmark](../../multimodal-models/2606.14958-mveb/README.md)（`mveb`）：固定v1 Section3：MVEB23任务从184任务池缩减；var-length fps2/cap64frames，固定帧模型遵循其训练配置，音频按model采样率/长度；无per-task finetune。分类8shot frozen logistic probe，retrieval cosine/nDCG10，VCQA候选池accuracy，视频/音频版本配对且只跑模型支持modality。 **成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。**

## 视频理解与 token 压缩

- 2026-09-15 · [VideoMM: Adaptive Macro-Micro Inference for Efficient Video MLLMs](../../multimodal-models/2609.16722-videomm/README.md)（`videomm`）：先在低分辨率 Macro Proxy 上定位相关区域，仅在宏观共识不足时激活高保真 Micro Tokens。

## 跨模态连接器与冻结骨干

- 2023-01-30 · [BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models](../../reproductions/2301.12597-blip2/README.md)（`blip2`）：BLIP-2 冻结已有视觉 encoder 和 LLM，只训练轻量 Q-Former。固定数量的可学习 query 通过 cross-attention 从视觉 token 提取与语言最相关的信息；第一阶段做图文表征学习，第二阶段将 query 输出投影成冻结 LLM 的 soft visual prompt。

## 音频描述与对比排序

- 2026-09-01 · [From Visual Cues to Spoken Narration: Rethinking Audio Description](../../multimodal-models/2609.01725-cue2narrate-drl/README.md)（`cue2narrate-drl`）：固定v1 Section4.3 Eqs5–8：SFT按每个AD目标token求和；positive/negative评分均为同一当前模型和prompt上的token-mean logp，prompt/padding排除；DRL=-logsigmoid((s+−s−)/0.5)，全loss加0.2DRL。离线负caption生成冻结，但其当前模型likelihood仍反传。

## 高效视觉 token 压缩

- 2025-04-07 · [SmolVLM: Redefining small and efficient multimodal models](../../reproductions/2504.05299-smolvlm/README.md)（`smolvlm`）：SmolVLM 重新分配小模型视觉/语言侧算力，以 pixel shuffle 将相邻空间 token 搬到 channel 维，再用 MLP 映射到 LM 空间；同时研究长上下文、图像切片、学习位置 token 和数据配比， 使 256M/500M/2.2B 模型在低显存下保持图像与视频能力。
