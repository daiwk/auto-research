# 多模态大模型方法索引

本页汇总已经具有独立 adapter、真实公开图像实验和固定指标的论文实现。
底座 connector 与论文 genome 的对应关系也在同一处维护。

## 已实现论文

<div class="ar-method-index" markdown>

| 方法族 | 论文 | 机构与日期 | Adapter |
|---|---|---|---|
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
