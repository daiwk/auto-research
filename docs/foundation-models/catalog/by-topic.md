# 基础模型：按主题

采用“研究方向 → 方法簇 → 论文”的两级结构，覆盖架构、预训练、多模态和推理效率；训练后算法进入独立的 LLM 后训练研究域。

## 网络架构

### MoE、状态空间与残差路径

- [RARE: Decoupling Representation Steering from Expert Routing in Mixture-of-Experts Language Models](../../reproductions/2608.21236-rare/README.md)（`rare`）：Dense LLM 的 activation steering 直接用于 MoE 时会改变 router logits，token 被送往不同专家后，原估计的行为方向失效。RARE 将任意 steering direction 投影到 router 的零空间，并在后续保护层再次移除传播产生的 router-visible 分量，在保留原专家路径的同时改变行为表征。
- [Role-Decoupled Attention Residuals](../../reproductions/2608.01075-rd-attnres/README.md)（`rd-attnres`）：Block AttnRes 让注意力层从全部历史 residual sources 动态读取，但 Q、K、V 共用一条深度路由。论文指出 QK 负责匹配、V 负责承载内容，两者偏好的深度未必相同；RD-AttnRes 在不改变 residual sources 和 attention 主体的情况下，只为 V 增加一个 model-width 路由向量。
- [Naju: A Native Discrete State-Space Model with Independent Retention and Writing for Long-Sequence Memory](../../reproductions/2607.21000-naju/README.md)（`naju`）：Mamba 从连续时间系统离散化得到转移，单一耦合门也容易形成“强保留就难写入”的约束。Naju 直接参数化离散 pole，将 retain gate 和 write gate 分开，并保留 token-dependent $B/C$ 方向、短程因果卷积、直接 feedthrough 与输出调制。
- [mHC: Manifold-Constrained Hyper-Connections](../../reproductions/2512.24880-mhc/README.md)（`mhc`）：Hyper-Connections 把单一 residual stream 扩为多个流并动态混合，但任意残差矩阵会破坏 identity mapping，深层组合可能放大信号。mHC 将 $H^{res}$ 投影到 Birkhoff polytope（非负、行列和均为 1），同时约束 $H^{pre}$、$H^{post}$ 非负；这样既保留跨流信息交换，又让每层残差映射非扩张。
- [Hymba: A Hybrid-head Architecture for Small Language Models](../../reproductions/2411.13676-hymba/README.md)（`hymba`）：同一层并行执行 attention 与状态空间分支，再用输入相关 gate 融合局部精确检索和线性长程状态。
- [Mamba: Linear-Time Sequence Modeling with Selective State Spaces](../../reproductions/2312.00752-mamba/README.md)（`mamba`）：Mamba 让 SSM 的步长、读写向量依赖当前 token，从而选择性保留信息，同时保持序列长度线性复杂度。
- [Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity](../../reproductions/2101.03961-switch-transformer/README.md)（`switch-transformer`）：Switch 把 dense FFN 替换为每个 token 只激活一个专家的稀疏 MoE，在近似固定 FLOPs 下扩大参数容量。

### 动态层路由与残差路径

- [MACRO: Markov Chain Routing of Transformer Layers](../../reproductions/2608.05872-macro/README.md)（`macro`）：**主题：动态层路由。** 固定顺序执行所有 Transformer 层并非总是最优。

### 递归与 latent computation

- [DART: Decoded Attention over Recurrent States for Efficient Long-Context Sequence Modeling](../../reproductions/2608.02032-dart/README.md)（`dart`）：保留 Mamba-2 chunk state contributions，解码 token-conditioned K/V 并执行 state-memory attention。
- [Penelope: Localized Latent Recurrence for Efficient Structured Reasoning](../../reproductions/2607.25915-penelope/README.md)（`penelope`）：只在一个 decoder 边界执行共享权重的 latent recurrence，用门控状态反复精炼表示，避免整条 decoder 重跑。
- [Convolution for Large Language Models](../../reproductions/2607.18413-conv-llm/README.md)（`conv-llm`）：自注意力擅长全局依赖，却没有显式的短程归纳偏置。论文固定 Qwen3 主干，系统比较 17 个卷积插入位置，最终选择在 Q/K/V 线性投影后、attention 聚合前加入 `kernel=3` 的逐通道一维卷积；残差旁路保留原投影，不加归一化或激活，额外参数低于 `0.01%`。
- [Byte Latent Transformer: Patches Scale Better Than Tokens](../../reproductions/2412.09871-blt/README.md)（`blt`）：直接处理 byte，并依据 next-byte entropy 动态形成 patch；全局 Transformer 在 patch 级计算，局部编码器/解码器恢复 byte。

### 条件记忆与知识注入

- [TransMem: Transforming Hidden States into Memory for Large Language Models](../../reproductions/2607.29032-transmem/README.md)（`transmem`）：将冻结骨干的稀疏历史 hidden states 变换成可复用参数记忆，并用 evidence-conditioned self-distillation 学门控。
- [Memory Grafting: Scaling Language Model Pre-training via Offline Conditional Memory](../../reproductions/2605.20948-memory-grafting/README.md)（`memory-grafting`）：Engram 的大容量条件记忆需要随主模型从零训练。Memory Grafting 先统计高频 2/3/4-gram，用已经预训练的 grafting model 离线编码每个短语最后 token 的中间 hidden state并冻结；recipient 在线只做期望 $O(1)$ 的最长后缀精确查询。
- [Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models](../../reproductions/2601.07372-engram/README.md)（`engram`）：MoE 只增加条件计算，模型仍需用计算层反复重建静态局部模式。Engram 把规范化 n-gram 哈希到大 embedding table，进行确定性的 $O(1)$ lookup，并在早期层门控注入，让 attention/FFN 留给组合推理。

## 注意力与长上下文

### 稀疏、门控与动态注意力

- [Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension](../../reproductions/2608.10296-olmpool-long-context/README.md)（`olmpool-long-context`）：以受控 7B 模型池隔离 normalization、GQA、预训练长度和滑窗注意力对长上下文扩展的复合影响。
- [Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry](../../reproductions/2608.06849-autonomy-heads/README.md)（`autonomy-heads`）：直接从冻结 QK 投影的谱有效秩区分 retrieval 与 streaming heads，无需校准数据或运行时门控。
- [Parameter-free Adaptive Sparse Attention via Compression-Based Content Selection](../../reproductions/2607.21752-gzip-sparse-attention/README.md)（`gzip-sparse-attention`）：固定 BigBird/Longformer mask 不理解内容，learned mask 又需要额外参数、梯度估计或专用 kernel。论文把字节序列切成固定 block，用 gzip 压缩率作为无需训练的信息密度信号：高于样本均值的 literal blocks 互相建立长程连接，所有 block 保留局部窗口，不设置固定 global token。
- [MiniMax Sparse Attention](../../reproductions/2606.13392-minimax-sparse-attention/README.md)（`minimax-sparse-attention`）：长上下文 dense attention 的二次复杂度成为主要瓶颈。MSA 为每个 GQA 组增加轻量 index branch，先选择少数历史 block，主分支再对命中 token 做精确 attention；训练和推理使用同一路径。
- [Switch Attention: Towards Dynamic and Fine-grained Hybrid Transformers](../../reproductions/2603.26380-switch-attention/README.md)（`switch-attention`）：静态 hybrid attention 对所有 token 使用固定模式。Switch Attention 学习细粒度 router，只让需要全局信息的 token 走 full attention。
- [Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free](../../reproductions/2505.06708-gated-attention/README.md)（`gated-attention`）：softmax attention 的 value aggregation 到 output projection 之间基本是线性映射。论文系统比较 30 种门控变体，发现最简单稳定的方案是在每个 attention head 的 SDPA 输出后施加 query-dependent sigmoid gate：既增加非线性，也能稀疏抑制无用 head 输出。
- [MoBA: Mixture of Block Attention for Long-Context LLMs](../../reproductions/2502.13189-moba/README.md)（`moba`）：把序列切成 block，以可微 router 为每个 query 选择少量相关块，同时保留当前因果块。
- [Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention](../../reproductions/2502.11089-native-sparse-attention/README.md)（`native-sparse-attention`）：全注意力的计算和 KV 读取随上下文长度平方增长。NSA 不是在训练后裁剪 attention，而是从预训练开始并行学习三条路径：压缩历史块负责全局轮廓，query 相关的 block selection 恢复重要细节，滑窗保留近期精确信息；三路输出再由可学习门控融合。

### 位置编码与 KV 压缩

- [Learning What to Remember: Test-Time Training via Context Distillation](../../reproductions/2608.01672-ttcd/README.md)（`ttcd`）：长窗口教师以隐藏状态差异监督短窗口学生的 fast weights，使有限记忆优先保留未来有用信息。
- [Anti-Periodic Positional Encoding: Möbius Boundary Conditions Make In-Context Retrieval Reliable](../../reproductions/2607.21405-mobius-rope/README.md)（`mobius-rope`）：标准 RoPE 的随机种子会显著影响长距离 needle retrieval。论文为部分 attention heads 使用反周期频率梯度，使跨完整训练窗口的旋转恒为 $-I$；其余 heads 保留标准 RoPE，以维持语言建模能力。
- [Looped Latent Attention: Cross-Loop KV Compression for Looped Transformers](../../reproductions/2607.15456-looped-latent-attention/README.md)（`looped-latent-attention`）：Looped Transformer 重复使用同一组权重，但不同 loop 的 KV cache 仍重复占内存。LLA 学习跨 loop 共享的低秩 K/V latent，服务时按 loop 重建专用 K/V，从 recurrence 冗余中换取近无损压缩。
- [GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](../../reproductions/2305.13245-gqa/README.md)（`gqa`）：多个 query head 共享较少的 K/V head，在 MHA 质量与 MQA 解码带宽之间取得可控折中。
- [Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation](../../reproductions/2108.12409-alibi/README.md)（`alibi`）：不学习位置向量，而是在每个 head 的注意力 logits 上加入线性距离惩罚，实现 train-short/test-long 外推。
- [RoFormer: Enhanced Transformer with Rotary Position Embedding](../../reproductions/2104.09864-rope/README.md)（`rope`）：对每个 attention head 的 Q/K 二维子空间施加随位置旋转，使点积天然只依赖相对位移。

## 预训练与数据

### 训练框架与可组合实验

- [Fast A/B/n Testing: Exact Multi-Policy Comparison via Tree-Coupled Feedback Sharing](../../reproductions/2608.12831-tcab/README.md)（`tcab`）：用最大耦合和最小生成树共享相同决策的反馈，同时保持每个自适应策略的边际轨迹分布不变。
- [OpenLanguageModel: Readable and Composable Small-Language-Model Pretraining for Education and Research](../../reproductions/2607.16669-open-language-model/README.md)（`open-language-model`）：许多预训练框架把模型结构、训练循环和分布式运行强耦合，难以做透明消融。OLM 让组件保持普通 PyTorch module，用 Block、Residual、Repeat、Parallel 描述布线，同一模型可从 notebook 迁移到 CPU、单 GPU 和单机多 GPU。

### latent 与多步预测

- [Hierarchical Latent Prediction for Language Models](../../reproductions/2608.05806-hilp/README.md)（`hilp`）：**主题：分层 latent 预训练。** NextLat 的逐步 latent rollout 会累积误差。

### 数据清洗、编排与选择

- [DataOrchestra: Learning to Orchestrate Per-Example Curation of Pretraining Data](../../reproductions/2607.24717-data-orchestra/README.md)（`data-orchestra`）：固定 corpus-level 清洗会过度处理本来干净的文本，也会对不同噪声使用同一操作。DataOrchestra 为每个 1024-token chunk 生成计划：先选 Drop、Untouch 或 Clean；Clean 时再按 NP（Noise Pruning）→ SR（Surface Rectification）→ PA（Pedagogical Augmentation）选择阶段，并为 rewrite 生成该 chunk 专属 instruction。
- [PPL-Factory: Task-Aware and Budget-Aware Data Selection from Language Modeling to Reasoning](../../reproductions/2607.18199-ppl-factory/README.md)（`ppl-factory`）：固定的“选最难/最容易”规则会随任务和数据预算失效。PPL-Factory 先用冻结基础模型计算任务相关 NLL：语言建模按 packed block，推理 SFT 只看 reasoning/answer response；再按预算切换策略，高预算偏 easy，较低预算选 middle，极低预算从 middle pool 随机抽样以保覆盖。
- [Data Mixing Laws: Optimizing Data Mixtures by Predicting Language Modeling Performance](../../reproductions/2403.16952-data-mixing-laws/README.md)（`data-mixing-laws`）：先训练多组小预算 domain mixture，拟合各评测域的混合缩放律，再搜索未训练过的最优配比。
- [DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining](../../reproductions/2305.10429-doremi/README.md)（`doremi`）：用小型 proxy model 的 excess loss 做 group DRO，动态提升欠拟合域权重，再按所得配比训练目标模型。

### 优化器与训练效率

- [Muon is Scalable for LLM Training](../../reproductions/2502.16982-muon/README.md)（`muon`）：AdamW 把矩阵参数当作独立标量更新，Muon 则把隐藏层梯度视为矩阵，通过 momentum 与 Newton–Schulz 近似极分解得到正交化更新方向。论文为大规模训练补上 weight decay 和按参数形状缩放；非隐藏矩阵参数继续使用 AdamW。

## 多模态基础模型

### 对比预训练与自蒸馏

- [WeMM-Embedding: WeChat Multi-Modal Embedding Technical Report](../../reproductions/2608.24053-wemm-embedding/README.md)（`wemm-embedding`）：不同检索任务通常维护独立的文本、图像、视频或文档 encoder。WeMM 把任意交错多模态输入映射到同一空间：第一阶段用数亿 pair 做大规模 alignment；第二阶段加入精选 relevance、细粒度监督和跨尺度知识迁移，并用 Matryoshka 表征支持按成本选择输出维度。
- [Towards Physics of Multimodal Pretraining: Knowledge Flow, Modality Synergy, Early Unification, and Recipes](../../reproductions/2608.05000-physics-mm-pretraining/README.md)（`physics-mm-pretraining`）：用受控实验刻画模态知识流、协同/竞争、早期统一和共享 attention+norm/模态专属 FFN 配方。
- [SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features](../../reproductions/2502.14786-siglip2/README.md)（`siglip2`）：SigLIP 2 在 SigLIP 的 pairwise sigmoid loss 上组合 captioning pretraining、global-local self-distillation、masked prediction、在线数据筛选和 NaFlex 动态分辨率，改善语义、定位、 dense feature 与多语言公平性。

### 生成辅助监督与理解增强

- [Generation as Auxiliary Supervision: Enhancing Visual Understanding at Zero Inference Overhead via Decoupled Embedding Prediction](../../reproductions/2608.12209-gas/README.md)（`gas`）：常规 MLLM 只用文本 next-token loss，视觉结构只能被语言间接监督；统一理解/生成模型又会把生成参数和开销留到部署阶段。GAS 把生成改成纯训练期辅助任务：理解分支与生成分支共享较低层视觉路径，上层 Transformer 参数解耦；生成分支在与 LLM 输入相同的连续视觉空间自回归预测目标图像 embedding。

### 视觉 token 与跨模态检索

- [ReToken: One Token to Improve Vision–Language Models for Visual Retrieval](../../reproductions/2607.28627-retoken/README.md)（`retoken`）：常规 VLM 检索需要先用外部 retriever 找图，再把入选图重新编码，无法直接复用预填充的视觉 KV cache。ReToken 在输入中增加一个可学习 token，让它在最后一层 value projection 空间与每张图的平均 value 向量打分；只训练该 token 和一张投影矩阵，以 class-balanced BCE 监督相关/无关图，VLM 默认冻结。
- [Visual Instruction Tuning](../../reproductions/2304.08485-llava/README.md)（`llava`）：冻结视觉 encoder，用可训练 projector 把视觉特征映射到 LLM token 空间，再在 GPT-4 生成的多模态指令数据上做端到端 instruction tuning。
- [Learning Transferable Visual Models From Natural Language Supervision](../../reproductions/2103.00020-clip/README.md)（`clip`）：用独立图像/文本 encoder 将配对样本映射到同一单位球面，通过双向 batch contrastive objective 学习可迁移零样本表示。

### 高效视觉 token 压缩

- [SmolVLM: Redefining small and efficient multimodal models](../../reproductions/2504.05299-smolvlm/README.md)（`smolvlm`）：SmolVLM 重新分配小模型视觉/语言侧算力，以 pixel shuffle 将相邻空间 token 搬到 channel 维，再用 MLP 映射到 LM 空间；同时研究长上下文、图像切片、学习位置 token 和数据配比， 使 256M/500M/2.2B 模型在低显存下保持图像与视频能力。

### 跨模态连接器与冻结骨干

- [BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models](../../reproductions/2301.12597-blip2/README.md)（`blip2`）：BLIP-2 冻结已有视觉 encoder 和 LLM，只训练轻量 Q-Former。固定数量的可学习 query 通过 cross-attention 从视觉 token 提取与语言最相关的信息；第一阶段做图文表征学习，第二阶段将 query 输出投影成冻结 LLM 的 soft visual prompt。

## 推理与系统效率

### 推测解码与 KV cache

- [DistillCache: KL-Guided Adaptive KV-Cache Eviction for Memory-Efficient LLM Inference](../../reproductions/2608.08878-distillcache/README.md)（`distillcache`）：把 KV 淘汰视为序列决策，以逐步 KL 奖励训练轻量策略保留未来预测分布。
- [DBLast: Dependent Block Drafting for Stochastic Speculative Decoding](../../reproductions/2608.05448-dblast/README.md)（`dblast`）：**主题：推测解码。** 并行 block drafter 常把位置条件独立化，在高熵采样时难以匹配联合分布。
- [QEvict: Recoverable Quantized KV Eviction for Attention-Drift-Robust Long-Context Decoding](../../reproductions/2608.05326-qevict/README.md)（`qevict`）：**主题：长上下文 KV cache。** 二元保留/删除无法应对注意力漂移：今天不重要的窗口可能稍后重新活跃。
- [Windowed-MTP: Removing the Full-Context Draft-KV Tax at Million-Token Context](../../reproductions/2607.21535-windowed-mtp/README.md)（`windowed-mtp`）：内置 MTP/NEXTN draft 通常每提出一个 token 都读取完整 KV cache；在百万 token 上，即使 target 已使用 GDN/Mamba 等便宜 verifier，draft 的全量 KV read 仍会成为瓶颈。Windowed-MTP 只改变 draft：保留最前面的 attention sink 与最近 $W$ 个 token，同时 target 继续读取完整上下文并验证所有候选。
- [C²KV: Compressed and Composable KV Cache Reuse for Efficient LLM Inference](../../reproductions/2607.17715-c2kv/README.md)（`c2kv`）：以 compression tokens 和结构化 attention 学习位置无关、可拼接的压缩 KV manifold，并联合训练压缩与复用。
- [Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](../../reproductions/2401.10774-medusa/README.md)（`medusa`）：在冻结或联合微调的 backbone 上增加多个 future-token heads，以 tree attention 同时验证候选分支，减少串行解码步数。
- [Fast Inference from Transformers via Speculative Decoding](../../reproductions/2211.17192-speculative-decoding/README.md)（`speculative-decoding`）：小 draft model 并行提出多个 token，target model 一次验证整个块；拒绝时从校正后的残差分布采样，从而严格保持 target 分布。

### 量化

- [BaKron: Efficient Quantization with Kronecker-Factored Hessians](../../reproductions/2608.06291-bakron/README.md)（`bakron`）：**主题：二阶量化。** GPTQ 通常只利用输入侧曲率；双侧 Kronecker Hessian 更丰富但直接向量化求解昂贵。
- [GaugeQuant: Online Learning of Quantization-Optimal Bases from LLM Symmetries](../../reproductions/2607.20757-gaugequant/README.md)（`gaugequant`）：LLM 内部通道存在保持函数不变的 gauge 对称性，但不同等价基的量化误差差异很大。GaugeQuant 在训练中在线学习量化友好正交基，以 LogSumExp 压制 activation outliers，不需要额外 calibration corpus。
- [AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration](../../reproductions/2306.00978-awq/README.md)（`awq`）：利用 calibration activation 找到显著输入通道，通过等价通道缩放保护约 1% 关键权重，再执行硬件友好的统一低比特 weight-only 量化。

### 动态计算与模型压缩

- [WIDE: Boosting Adaptive LLM Inference via Token-level Dynamic Width Pruning](../../reproductions/2607.28418-wide/README.md)（`wide`）：静态剪枝无法按 token 难度分配算力，动态深度又过于粗粒度。WIDE 对每个 token 分别路由 attention head group 和 FFN channel group，并将 mask reorder、block skip 与设备内跳过联合设计。
- [Adaptive Depth Sparse Framework: Similarity-Driven Resource Allocation for Pre-Trained LLMs](../../reproductions/2607.21291-adadsf/README.md)（`adadsf`）：固定比例的 Mixture-of-Depths 会给每一层相同 token budget，但不同层对表示的改写强度并不相同。AdaDSF 先在 dense teacher 上测量各层输入/输出 cosine similarity，再把更多计算分给变化更大的层；每层 MLP router 只把 Top-K token 送入原 Transformer block，其他 token 走 residual bypass。
