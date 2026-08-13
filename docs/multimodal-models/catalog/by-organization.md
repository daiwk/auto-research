# 多模态大模型：按机构/公司/学校

按论文一作第一署名单位聚合；单位内按首次公开日期倒序排列。

## ByteDance

- 2026-08-12 · [Generation as Auxiliary Supervision: Enhancing Visual Understanding at Zero Inference Overhead via Decoupled Embedding Prediction](../../reproductions/2608.12209-gas/README.md)（`gas`）：常规 MLLM 只用文本 next-token loss，视觉结构只能被语言间接监督；统一理解/生成模型又会把生成参数和开销留到部署阶段。GAS 把生成改成纯训练期辅助任务：理解分支与生成分支共享较低层视觉路径，上层 Transformer 参数解耦；生成分支在与 LLM 输入相同的连续视觉空间自回归预测目标图像 embedding。

## Google DeepMind

- 2025-02-20 · [SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features](../../reproductions/2502.14786-siglip2/README.md)（`siglip2`）：SigLIP 2 在 SigLIP 的 pairwise sigmoid loss 上组合 captioning pretraining、global-local self-distillation、masked prediction、在线数据筛选和 NaFlex 动态分辨率，改善语义、定位、 dense feature 与多语言公平性。

## Hugging Face

- 2025-04-07 · [SmolVLM: Redefining small and efficient multimodal models](../../reproductions/2504.05299-smolvlm/README.md)（`smolvlm`）：SmolVLM 重新分配小模型视觉/语言侧算力，以 pixel shuffle 将相邻空间 token 搬到 channel 维，再用 MLP 映射到 LM 空间；同时研究长上下文、图像切片、学习位置 token 和数据配比， 使 256M/500M/2.2B 模型在低显存下保持图像与视频能力。

## OpenAI

- 2021-02-26 · [Learning Transferable Visual Models From Natural Language Supervision](../../reproductions/2103.00020-clip/README.md)（`clip`）：用独立图像/文本 encoder 将配对样本映射到同一单位球面，通过双向 batch contrastive objective 学习可迁移零样本表示。

## Salesforce Research

- 2023-01-30 · [BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models](../../reproductions/2301.12597-blip2/README.md)（`blip2`）：BLIP-2 冻结已有视觉 encoder 和 LLM，只训练轻量 Q-Former。固定数量的可学习 query 通过 cross-attention 从视觉 token 提取与语言最相关的信息；第一阶段做图文表征学习，第二阶段将 query 输出投影成冻结 LLM 的 soft visual prompt。

## University of Wisconsin-Madison

- 2023-04-17 · [Visual Instruction Tuning](../../reproductions/2304.08485-llava/README.md)（`llava`）：冻结视觉 encoder，用可训练 projector 把视觉特征映射到 LLM token 空间，再在 GPT-4 生成的多模态指令数据上做端到端 instruction tuning。
