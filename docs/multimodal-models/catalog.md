# 多模态大模型方法索引

本页汇总具有独立源码入口的论文；公开数据实跑与 GPU 验收状态请查各篇详情和回执。
底座 connector 与论文 genome 的对应关系也在同一处维护。

## 已实现论文

<div class="ar-method-index" markdown>

| 方法族 | 论文 | 机构与日期 | Adapter |
|---|---|---|---|
| 视觉证据约束蒸馏 | [CV-OPD: Contrastive Vision On-policy Distillation](../reproductions/2610.13264-cv-opd/README.md) | Xiamen University，2026-10-09 | `cv-opd` |
| 视觉 token 压缩与动态证据恢复 | [Look Back, Think Ahead: Visual Memory on Demand for Efficient Multimodal Reasoning](../multimodal-models/2610.12060-vimod/README.md) | City University of Hong Kong，2026-10-08 | `vimod` |
| 冻结中间层探针与验证器自举 | [Unsupervised Multimodal Reward Modeling](../reproductions/2610.12707-umrm/README.md) | Massachusetts Institute of Technology，2026-10-08 | `umrm` |
| 视觉 token 压缩与动态证据恢复 | [V-CoLA: Vision Token Compression with Linear Attention](../multimodal-models/2610.11251-vcola/README.md) | Alibaba Cloud Computing，2026-10-08 | `vcola` |
| 视觉状态转移监督 | [WOVEN: Weaving Visual World Modeling into Multimodal LLMs](../reproductions/2610.12417-woven/README.md) | Northwestern University，2026-10-08 | `woven` |
| 视觉 token 与跨模态检索 | [StackTok: Accelerating VLMs Inference with Budget-Adaptive Visual Token Selection](../multimodal-models/2609.16841-stacktok/README.md) | Sichuan University，2026-09-15 | `stacktok` |
| 视频理解与 token 压缩 | [VideoMM: Adaptive Macro-Micro Inference for Efficient Video MLLMs](../multimodal-models/2609.16722-videomm/README.md) | University of Science and Technology of China，2026-09-15 | `videomm` |
| 生成辅助监督与理解增强 | [Generation as Auxiliary Supervision: Enhancing Visual Understanding at Zero Inference Overhead via Decoupled Embedding Prediction](../reproductions/2608.12209-gas/README.md) | ByteDance，2026-08-12 | `gas` |
| 高效视觉 token 压缩 | [SmolVLM: Redefining small and efficient multimodal models](../reproductions/2504.05299-smolvlm/README.md) | Hugging Face，2025-04-07 | `smolvlm` |
| 对比预训练与自蒸馏 | [SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features](../reproductions/2502.14786-siglip2/README.md) | Google DeepMind，2025-02-20 | `siglip2` |
| 视觉 token 与跨模态检索 | [Visual Instruction Tuning](../reproductions/2304.08485-llava/README.md) | University of Wisconsin-Madison，2023-04-17 | `llava` |
| 跨模态连接器与冻结骨干 | [BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models](../reproductions/2301.12597-blip2/README.md) | Salesforce Research，2023-01-30 | `blip2` |
| 视觉 token 与跨模态检索 | [Learning Transferable Visual Models From Natural Language Supervision](../reproductions/2103.00020-clip/README.md) | OpenAI，2021-02-26 | `clip` |

</div>

## 可进入 evolve 的论文算子

| Genome | 来源 | 主要变化 |
|---|---|---|
| `micro_vlm_linear` | CLIP / LLaVA 基础投影 | 保留全部 patch token 的线性连接器 |
| `micro_vlm_mlp` | LLaVA | 两层非线性 projector |
| `micro_vlm_qformer` | BLIP-2 | 可学习 query cross-attention，16→4 token |
| `micro_vlm_pixelshuffle` | SmolVLM | 2×2 space-to-depth，16→4 token |
| `objective:siglip2` | SigLIP 2 | sigmoid 图文目标与 masked-view consistency |

分类浏览：[按机构/公司/学校](catalog/by-organization.md) · [按主题](catalog/by-topic.md) · [按年份](catalog/by-year.md)
