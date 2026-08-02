# 基础模型：按主题

采用“研究方向 → 方法簇 → 论文”的两级结构，覆盖架构、预训练、多模态和推理效率；训练后算法进入独立的 LLM 后训练研究域。

## 网络架构

### 递归与 latent computation

- [Penelope: Localized Latent Recurrence for Efficient Structured Reasoning](../../reproductions/2607.25915-penelope/README.md)（`penelope`）：只在一个 decoder 边界执行共享权重的 latent recurrence，用门控状态反复精炼表示，避免整条 decoder 重跑。
- [Convolution for Large Language Models](../../reproductions/2607.18413-conv-llm/README.md)（`conv-llm`）：自注意力擅长全局依赖，却没有显式的短程归纳偏置。论文固定 Qwen3 主干，系统比较 17 个卷积插入位置，最终选择在 Q/K/V 线性投影后、attention 聚合前加入 `kernel=3` 的逐通道一维卷积；残差旁路保留原投影，不加归一化或激活，额外参数低于 `0.01%`。

### MoE、状态空间与残差路径

- [Naju: A Native Discrete State-Space Model with Independent Retention and Writing for Long-Sequence Memory](../../reproductions/2607.21000-naju/README.md)（`naju`）：Mamba 从连续时间系统离散化得到转移，单一耦合门也容易形成“强保留就难写入”的约束。Naju 直接参数化离散 pole，将 retain gate 和 write gate 分开，并保留 token-dependent $B/C$ 方向、短程因果卷积、直接 feedthrough 与输出调制。
- [mHC: Manifold-Constrained Hyper-Connections](../../reproductions/2512.24880-mhc/README.md)（`mhc`）：Hyper-Connections 把单一 residual stream 扩为多个流并动态混合，但任意残差矩阵会破坏 identity mapping，深层组合可能放大信号。mHC 将 $H^{res}$ 投影到 Birkhoff polytope（非负、行列和均为 1），同时约束 $H^{pre}$、$H^{post}$ 非负；这样既保留跨流信息交换，又让每层残差映射非扩张。
- [Mamba: Linear-Time Sequence Modeling with Selective State Spaces](../../reproductions/2312.00752-mamba/README.md)（`mamba`）：Mamba 让 SSM 的步长、读写向量依赖当前 token，从而选择性保留信息，同时保持序列长度线性复杂度。
- [Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity](../../reproductions/2101.03961-switch-transformer/README.md)（`switch-transformer`）：Switch 把 dense FFN 替换为每个 token 只激活一个专家的稀疏 MoE，在近似固定 FLOPs 下扩大参数容量。

### 条件记忆与知识注入

- [Memory Grafting: Scaling Language Model Pre-training via Offline Conditional Memory](../../reproductions/2605.20948-memory-grafting/README.md)（`memory-grafting`）：Engram 的大容量条件记忆需要随主模型从零训练。Memory Grafting 先统计高频 2/3/4-gram，用已经预训练的 grafting model 离线编码每个短语最后 token 的中间 hidden state并冻结；recipient 在线只做期望 $O(1)$ 的最长后缀精确查询。
- [Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models](../../reproductions/2601.07372-engram/README.md)（`engram`）：MoE 只增加条件计算，模型仍需用计算层反复重建静态局部模式。Engram 把规范化 n-gram 哈希到大 embedding table，进行确定性的 $O(1)$ lookup，并在早期层门控注入，让 attention/FFN 留给组合推理。

## 注意力与长上下文

### 位置编码与 KV 压缩

- [Anti-Periodic Positional Encoding: Möbius Boundary Conditions Make In-Context Retrieval Reliable](../../reproductions/2607.21405-mobius-rope/README.md)（`mobius-rope`）：标准 RoPE 的随机种子会显著影响长距离 needle retrieval。论文为部分 attention heads 使用反周期频率梯度，使跨完整训练窗口的旋转恒为 $-I$；其余 heads 保留标准 RoPE，以维持语言建模能力。
- [Looped Latent Attention: Cross-Loop KV Compression for Looped Transformers](../../reproductions/2607.15456-looped-latent-attention/README.md)（`looped-latent-attention`）：Looped Transformer 重复使用同一组权重，但不同 loop 的 KV cache 仍重复占内存。LLA 学习跨 loop 共享的低秩 K/V latent，服务时按 loop 重建专用 K/V，从 recurrence 冗余中换取近无损压缩。

### 稀疏、门控与动态注意力

- [Parameter-free Adaptive Sparse Attention via Compression-Based Content Selection](../../reproductions/2607.21752-gzip-sparse-attention/README.md)（`gzip-sparse-attention`）：固定 BigBird/Longformer mask 不理解内容，learned mask 又需要额外参数、梯度估计或专用 kernel。论文把字节序列切成固定 block，用 gzip 压缩率作为无需训练的信息密度信号：高于样本均值的 literal blocks 互相建立长程连接，所有 block 保留局部窗口，不设置固定 global token。
- [MiniMax Sparse Attention](../../reproductions/2606.13392-minimax-sparse-attention/README.md)（`minimax-sparse-attention`）：长上下文 dense attention 的二次复杂度成为主要瓶颈。MSA 为每个 GQA 组增加轻量 index branch，先选择少数历史 block，主分支再对命中 token 做精确 attention；训练和推理使用同一路径。
- [Switch Attention: Towards Dynamic and Fine-grained Hybrid Transformers](../../reproductions/2603.26380-switch-attention/README.md)（`switch-attention`）：静态 hybrid attention 对所有 token 使用固定模式。Switch Attention 学习细粒度 router，只让需要全局信息的 token 走 full attention。
- [Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free](../../reproductions/2505.06708-gated-attention/README.md)（`gated-attention`）：softmax attention 的 value aggregation 到 output projection 之间基本是线性映射。论文系统比较 30 种门控变体，发现最简单稳定的方案是在每个 attention head 的 SDPA 输出后施加 query-dependent sigmoid gate：既增加非线性，也能稀疏抑制无用 head 输出。
- [Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention](../../reproductions/2502.11089-native-sparse-attention/README.md)（`native-sparse-attention`）：全注意力的计算和 KV 读取随上下文长度平方增长。NSA 不是在训练后裁剪 attention，而是从预训练开始并行学习三条路径：压缩历史块负责全局轮廓，query 相关的 block selection 恢复重要细节，滑窗保留近期精确信息；三路输出再由可学习门控融合。

## 预训练与数据

### 数据清洗、编排与选择

- [DataOrchestra: Learning to Orchestrate Per-Example Curation of Pretraining Data](../../reproductions/2607.24717-data-orchestra/README.md)（`data-orchestra`）：固定 corpus-level 清洗会过度处理本来干净的文本，也会对不同噪声使用同一操作。DataOrchestra 为每个 1024-token chunk 生成计划：先选 Drop、Untouch 或 Clean；Clean 时再按 NP（Noise Pruning）→ SR（Surface Rectification）→ PA（Pedagogical Augmentation）选择阶段，并为 rewrite 生成该 chunk 专属 instruction。
- [PPL-Factory: Task-Aware and Budget-Aware Data Selection from Language Modeling to Reasoning](../../reproductions/2607.18199-ppl-factory/README.md)（`ppl-factory`）：固定的“选最难/最容易”规则会随任务和数据预算失效。PPL-Factory 先用冻结基础模型计算任务相关 NLL：语言建模按 packed block，推理 SFT 只看 reasoning/answer response；再按预算切换策略，高预算偏 easy，较低预算选 middle，极低预算从 middle pool 随机抽样以保覆盖。

### 优化器与训练效率

- [Muon is Scalable for LLM Training](../../reproductions/2502.16982-muon/README.md)（`muon`）：AdamW 把矩阵参数当作独立标量更新，Muon 则把隐藏层梯度视为矩阵，通过 momentum 与 Newton–Schulz 近似极分解得到正交化更新方向。论文为大规模训练补上 weight decay 和按参数形状缩放；非隐藏矩阵参数继续使用 AdamW。

## 多模态基础模型

### 视觉 token 与跨模态检索

- [ReToken: One Token to Improve Vision–Language Models for Visual Retrieval](../../reproductions/2607.28627-retoken/README.md)（`retoken`）：常规 VLM 检索需要先用外部 retriever 找图，再把入选图重新编码，无法直接复用预填充的视觉 KV cache。ReToken 在输入中增加一个可学习 token，让它在最后一层 value projection 空间与每张图的平均 value 向量打分；只训练该 token 和一张投影矩阵，以 class-balanced BCE 监督相关/无关图，VLM 默认冻结。

## 推理与系统效率

### 动态计算与模型压缩

- [WIDE: Boosting Adaptive LLM Inference via Token-level Dynamic Width Pruning](../../reproductions/2607.28418-wide/README.md)（`wide`）：静态剪枝无法按 token 难度分配算力，动态深度又过于粗粒度。WIDE 对每个 token 分别路由 attention head group 和 FFN channel group，并将 mask reorder、block skip 与设备内跳过联合设计。
- [Adaptive Depth Sparse Framework: Similarity-Driven Resource Allocation for Pre-Trained LLMs](../../reproductions/2607.21291-adadsf/README.md)（`adadsf`）：固定比例的 Mixture-of-Depths 会给每一层相同 token budget，但不同层对表示的改写强度并不相同。AdaDSF 先在 dense teacher 上测量各层输入/输出 cosine similarity，再把更多计算分给变化更大的层；每层 MLP router 只把 Top-K token 送入原 Transformer block，其他 token 走 residual bypass。

### 推测解码与 KV cache

- [Windowed-MTP: Removing the Full-Context Draft-KV Tax at Million-Token Context](../../reproductions/2607.21535-windowed-mtp/README.md)（`windowed-mtp`）：内置 MTP/NEXTN draft 通常每提出一个 token 都读取完整 KV cache；在百万 token 上，即使 target 已使用 GDN/Mamba 等便宜 verifier，draft 的全量 KV read 仍会成为瓶颈。Windowed-MTP 只改变 draft：保留最前面的 attention sink 与最近 $W$ 个 token，同时 target 继续读取完整上下文并验证所有候选。

### 量化

- [GaugeQuant: Online Learning of Quantization-Optimal Bases from LLM Symmetries](../../reproductions/2607.20757-gaugequant/README.md)（`gaugequant`）：LLM 内部通道存在保持函数不变的 gauge 对称性，但不同等价基的量化误差差异很大。GaugeQuant 在训练中在线学习量化友好正交基，以 LogSumExp 压制 activation outliers，不需要额外 calibration corpus。
