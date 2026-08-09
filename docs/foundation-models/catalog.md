# 基础模型论文与资料索引

本页由 `docs/research-manifest.json` 自动生成；论文元数据只在统一 manifest
维护。背景、架构、公式、原文效果和本地实验请进入独立详情页。

## 已实现论文与资料

<div class="ar-method-index" markdown>

| 方向 | 方法 | 机构与日期 | 原作者代码 | 本地入口 |
|---|---|---|---|---|
| 网络架构 | [Role-Decoupled Attention Residuals](../reproductions/2608.01075-rd-attnres/README.md) | Kehan Wang（论文未列机构），2026-08-03 | 未发现官方代码 | `rd-attnres` |
| 多模态基础模型 | [ReToken: One Token to Improve Vision–Language Models for Visual Retrieval](../reproductions/2607.28627-retoken/README.md) | UIUC / Microsoft Research / Google DeepMind，2026-07-30 | [已开源](https://github.com/avaxiao/ReToken) | `retoken` |
| 推理与系统效率 | [WIDE: Boosting Adaptive LLM Inference via Token-level Dynamic Width Pruning](../reproductions/2607.28418-wide/README.md) | EIT-NLP / LMU Munich，2026-07-30 | [已开源](https://github.com/EIT-NLP/LLM-Pruning/tree/main/WIDE) | `wide` |
| 网络架构 | [Penelope: Localized Latent Recurrence for Efficient Structured Reasoning](../reproductions/2607.25915-penelope/README.md) | Academic author team，2026-07-28 | 未发现官方代码 | `penelope` |
| 预训练与数据 | [DataOrchestra: Learning to Orchestrate Per-Example Curation of Pretraining Data](../reproductions/2607.24717-data-orchestra/README.md) | Fudan University / Shanghai Jiao Tong University / SII-GAIR，2026-07-27 | [已开源](https://github.com/GAIR-NLP/DataOrchestra) | `data-orchestra` |
| 推理与系统效率 | [Adaptive Depth Sparse Framework: Similarity-Driven Resource Allocation for Pre-Trained LLMs](../reproductions/2607.21291-adadsf/README.md) | Huawei ACS Lab / Southern University of Science and Technology，2026-07-23 | 未发现官方代码 | `adadsf` |
| 注意力与长上下文 | [Anti-Periodic Positional Encoding: Möbius Boundary Conditions Make In-Context Retrieval Reliable](../reproductions/2607.21405-mobius-rope/README.md) | Independent researcher，2026-07-23 | 未发现官方代码 | `mobius-rope` |
| 网络架构 | [Naju: A Native Discrete State-Space Model with Independent Retention and Writing for Long-Sequence Memory](../reproductions/2607.21000-naju/README.md) | Independent researchers，2026-07-23 | 未发现官方代码 | `naju` |
| 注意力与长上下文 | [Parameter-free Adaptive Sparse Attention via Compression-Based Content Selection](../reproductions/2607.21752-gzip-sparse-attention/README.md) | Pennsylvania State University，2026-07-23 | 未发现官方代码 | `gzip-sparse-attention` |
| 推理与系统效率 | [Windowed-MTP: Removing the Full-Context Draft-KV Tax at Million-Token Context](../reproductions/2607.21535-windowed-mtp/README.md) | NVIDIA，2026-07-23 | [已开源](https://github.com/avalliappan-nvidia/windowed-mtp-b200) | `windowed-mtp` |
| 推理与系统效率 | [GaugeQuant: Online Learning of Quantization-Optimal Bases from LLM Symmetries](../reproductions/2607.20757-gaugequant/README.md) | University of Cambridge，2026-07-22 | [已开源](https://github.com/MPedraBento/gauge-quant) | `gaugequant` |
| 网络架构 | [Convolution for Large Language Models](../reproductions/2607.18413-conv-llm/README.md) | Huawei / Peking University / Tsinghua University，2026-07-20 | 未发现官方代码 | `conv-llm` |
| 预训练与数据 | [PPL-Factory: Task-Aware and Budget-Aware Data Selection from Language Modeling to Reasoning](../reproductions/2607.18199-ppl-factory/README.md) | McGill University，2026-07-20 | 未发现官方代码 | `ppl-factory` |
| 预训练与数据 | [OpenLanguageModel: Readable and Composable Small-Language-Model Pretraining for Education and Research](../reproductions/2607.16669-open-language-model/README.md) | Indian Institute of Technology Madras，2026-07-18 | [已开源](https://github.com/openlanguagemodel/openlanguagemodel) | `open-language-model` |
| 注意力与长上下文 | [Looped Latent Attention: Cross-Loop KV Compression for Looped Transformers](../reproductions/2607.15456-looped-latent-attention/README.md) | University of Maryland / Meta AI，2026-07-16 | 未发现官方代码 | `looped-latent-attention` |
| 注意力与长上下文 | [MiniMax Sparse Attention](../reproductions/2606.13392-minimax-sparse-attention/README.md) | MiniMax，2026-06-11 | [已开源](https://github.com/MiniMax-AI/MSA) | `minimax-sparse-attention` |
| 网络架构 | [Memory Grafting: Scaling Language Model Pre-training via Offline Conditional Memory](../reproductions/2605.20948-memory-grafting/README.md) | Tsinghua University / Microsoft Research Asia，2026-05-20 | 未发现官方代码 | `memory-grafting` |
| 注意力与长上下文 | [Switch Attention: Towards Dynamic and Fine-grained Hybrid Transformers](../reproductions/2603.26380-switch-attention/README.md) | Peking University / Huawei Technologies，2026-03-27 | 未发现官方代码 | `switch-attention` |
| 网络架构 | [Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models](../reproductions/2601.07372-engram/README.md) | DeepSeek，2026-01-12 | [已开源](https://github.com/deepseek-ai/Engram) | `engram` |
| 网络架构 | [mHC: Manifold-Constrained Hyper-Connections](../reproductions/2512.24880-mhc/README.md) | DeepSeek-AI，2025-12-31 | 未发现官方代码 | `mhc` |
| 注意力与长上下文 | [Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free](../reproductions/2505.06708-gated-attention/README.md) | Qwen / Alibaba，2025-05-10 | [已开源](https://github.com/qiuzh20/gated_attention) | `gated-attention` |
| 预训练与数据 | [Muon is Scalable for LLM Training](../reproductions/2502.16982-muon/README.md) | Moonshot AI / UCLA，2025-02-24 | [已开源](https://github.com/MoonshotAI/Moonlight) | `muon` |
| 注意力与长上下文 | [MoBA: Mixture of Block Attention for Long-Context LLMs](../reproductions/2502.13189-moba/README.md) | Moonshot AI，2025-02-18 | [已开源](https://github.com/MoonshotAI/MoBA) | `moba` |
| 注意力与长上下文 | [Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention](../reproductions/2502.11089-native-sparse-attention/README.md) | DeepSeek，2025-02-16 | 未发现官方代码 | `native-sparse-attention` |
| 网络架构 | [Byte Latent Transformer: Patches Scale Better Than Tokens](../reproductions/2412.09871-blt/README.md) | Meta FAIR，2024-12-13 | [已开源](https://github.com/facebookresearch/blt) | `blt` |
| 网络架构 | [Hymba: A Hybrid-head Architecture for Small Language Models](../reproductions/2411.13676-hymba/README.md) | NVIDIA，2024-11-20 | [已开源](https://github.com/NVlabs/hymba) | `hymba` |
| 预训练与数据 | [Data Mixing Laws: Optimizing Data Mixtures by Predicting Language Modeling Performance](../reproductions/2403.16952-data-mixing-laws/README.md) | University of Cambridge / Shanghai AI Laboratory，2024-03-25 | [已开源](https://github.com/yegcjs/mixinglaws) | `data-mixing-laws` |
| 推理与系统效率 | [Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](../reproductions/2401.10774-medusa/README.md) | Together AI / Princeton University / University of Illinois Urbana-Champaign，2024-01-19 | [已开源](https://github.com/FasterDecoding/Medusa) | `medusa` |
| 网络架构 | [Mamba: Linear-Time Sequence Modeling with Selective State Spaces](../reproductions/2312.00752-mamba/README.md) | Carnegie Mellon University / Princeton University，2023-12-01 | [已开源](https://github.com/state-spaces/mamba) | `mamba` |
| 推理与系统效率 | [AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration](../reproductions/2306.00978-awq/README.md) | MIT / NVIDIA / Harvard / SJTU，2023-06-01 | [已开源](https://github.com/mit-han-lab/llm-awq) | `awq` |
| 注意力与长上下文 | [GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](../reproductions/2305.13245-gqa/README.md) | Google Research，2023-05-22 | 未发现官方代码 | `gqa` |
| 预训练与数据 | [DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining](../reproductions/2305.10429-doremi/README.md) | Stanford University / Google Research，2023-05-17 | [已开源](https://github.com/sangmichaelxie/doremi) | `doremi` |
| 多模态基础模型 | [Visual Instruction Tuning](../reproductions/2304.08485-llava/README.md) | University of Wisconsin-Madison / Microsoft Research / Columbia University，2023-04-17 | [已开源](https://github.com/haotian-liu/LLaVA) | `llava` |
| 推理与系统效率 | [Fast Inference from Transformers via Speculative Decoding](../reproductions/2211.17192-speculative-decoding/README.md) | Google Research，2022-11-30 | [已开源](https://github.com/google-research/google-research/tree/master/speculative_decoding) | `speculative-decoding` |
| 注意力与长上下文 | [Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation](../reproductions/2108.12409-alibi/README.md) | University of Washington / Meta AI，2021-08-27 | [已开源](https://github.com/ofirpress/attention_with_linear_biases) | `alibi` |
| 注意力与长上下文 | [RoFormer: Enhanced Transformer with Rotary Position Embedding](../reproductions/2104.09864-rope/README.md) | Zhuiyi Technology，2021-04-20 | [已开源](https://github.com/ZhuiyiTechnology/roformer) | `rope` |
| 多模态基础模型 | [Learning Transferable Visual Models From Natural Language Supervision](../reproductions/2103.00020-clip/README.md) | OpenAI，2021-02-26 | [已开源](https://github.com/openai/CLIP) | `clip` |
| 网络架构 | [Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity](../reproductions/2101.03961-switch-transformer/README.md) | Google Brain，2021-01-11 | [已开源](https://github.com/tensorflow/mesh) | `switch-transformer` |

</div>

分类浏览：

- [按机构/公司/学校](catalog/by-organization.md)
- [按主题](catalog/by-topic.md)
- [按年份](catalog/by-year.md)
