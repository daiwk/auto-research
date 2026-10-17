# 基础模型：按机构/公司/学校

按论文一作的第一署名单位聚合；单位内按首次公开日期倒序排列。联合工作只归入一作的第一署名单位，不会重复归入全部合作单位。

## Ai2

- 2026-08-10 · [Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension](../../reproductions/2608.10296-olmpool-long-context/README.md)（`olmpool-long-context`）：以受控 7B 模型池隔离 normalization、GQA、预训练长度和滑窗注意力对长上下文扩展的复合影响。

## Apple

- 2026-10-09 · [On the Design Space of Continuous Diffusion Language Models](../../reproductions/2610.13834-doublecat-semicat/README.md)（`doublecat-semicat`）：One-hot continuous flow 在接近终点时训练几乎只看见低熵顶点，但推理跟随有熵 denoiser 概率，产生轨迹错配。DoubleCat 在高斯路径内部再插入 simplex prior 到 one-hot 的插值，把训练质量移到更像推理的 simplex 内部。
- 2026-09-29 · [On Trajectory-Aware Training for Masked Diffusion Language Models](../../foundation-models/2609.37974-pumba/README.md)（`pumba`）：训练时沿模型自己的 progressive-unmasking 轨迹连续展开多个 denoising step，把隐藏 carry 传给下一步，并在固定窗口内通过时间反向传播，使前一步学会产生对后续有用的 carry。

## Authors did not disclose affiliation

- 2026-07-31 · [TransMem: Transforming Hidden States into Memory for Large Language Models](../../reproductions/2607.29032-transmem/README.md)（`transmem`）：将冻结骨干的稀疏历史 hidden states 变换成可复用参数记忆，并用 evidence-conditioned self-distillation 学门控。

## Bar-Ilan University

- 2026-09-29 · [Cross-Entropy Guided Routing in Mixture-of-Experts Large Language Models](../../foundation-models/2609.37751-ce-guided-moe/README.md)（`ce-guided-moe`）：在原生 MoE affinity 旁增加逐 expert token-error head，并用预测误差的 started-log 对路由 logit 做衰减；高预测错误的 expert 在 Top-K 前被降权，同时误差头由真实 next-token CE 监督。

## Beijing University of Posts and Telecommunications

- 2026-09-03 · [Lngram v2: Latent N-Gram Memory with Interpretable Discrete Representations](../../reproductions/2609.03426-lngram-v2/README.md)（`lngram-v2`）：Lngram v2 把 backbone hidden state 投影成多路二进制地址，以最近 1/2-gram 的离散组合 O(1) 查 memory table；多个 route token 经 GQA 读回主干。硬地址保证表示可解释，反事实邻接地址提供训练梯度，零 Sink 允许模型拒绝无用记忆。

## ByteDance

- 2026-08-12 · [Generation as Auxiliary Supervision: Enhancing Visual Understanding at Zero Inference Overhead via Decoupled Embedding Prediction](../../reproductions/2608.12209-gas/README.md)（`gas`）：常规 MLLM 只用文本 next-token loss，视觉结构只能被语言间接监督；统一理解/生成模型又会把生成参数和开销留到部署阶段。GAS 把生成改成纯训练期辅助任务：理解分支与生成分支共享较低层视觉路径，上层 Transformer 参数解耦；生成分支在与 LLM 输入相同的连续视觉空间自回归预测目标图像 embedding。

## ByteDance Seed

- 2026-10-08 · [Few-Step Generation via Data-Space Iteration](../../foundation-models/2610.12102-data-space-iteration/README.md)（`data-space-iteration`）：常规 few-step flow generator 需要预设时间离散化，每步在加噪/去噪轨迹上前进。Data-Space Iteration 改为固定同一份噪声，用共享网络反复改进数据预测；每步 index 只表示 refinement，不是 flow time。训练沿用 distribution matching distillation：真实冻结 teacher 与逐步拟合生成分布的 fake 给出方向，前缀 rollout 无梯度，仅当前 refinement 更新 generator。[正文方法与附录代码](https://arxiv.org/html/2610.12102v1#S2)。

## Carnegie Mellon University

- 2023-12-01 · [Mamba: Linear-Time Sequence Modeling with Selective State Spaces](../../reproductions/2312.00752-mamba/README.md)（`mamba`）：Mamba 让 SSM 的步长、读写向量依赖当前 token，从而选择性保留信息，同时保持序列长度线性复杂度。

## Dalian Maritime University

- 2026-10-08 · [Specialized Decision Models vs. General-Purpose LLMs: Benchmarking Jev Across Knowledge, Reasoning, and Multilingual Tasks](../../system-one/2610.11978-jev-capability/README.md)（`jev-capability`）：论文用有限候选选择评估 Jev 的知识、推理和多语言能力。每题只提交问题与候选，运行一次；数学任务表现弱于知识任务。原文中的供应商分数与作者实测并非统一提示协议，本地实现因此分别记录，不混成可比排名。本文是评测研究，不提供新架构或训练目标。

## DeepSeek

- 2026-01-12 · [Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models](../../reproductions/2601.07372-engram/README.md)（`engram`）：MoE 只增加条件计算，模型仍需用计算层反复重建静态局部模式。Engram 把规范化 n-gram 哈希到大 embedding table，进行确定性的 $O(1)$ lookup，并在早期层门控注入，让 attention/FFN 留给组合推理。
- 2025-02-16 · [Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention](../../reproductions/2502.11089-native-sparse-attention/README.md)（`native-sparse-attention`）：全注意力的计算和 KV 读取随上下文长度平方增长。NSA 不是在训练后裁剪 attention，而是从预训练开始并行学习三条路径：压缩历史块负责全局轮廓，query 相关的 block selection 恢复重要细节，滑窗保留近期精确信息；三路输出再由可学习门控融合。

## DeepSeek-AI

- 2025-12-31 · [mHC: Manifold-Constrained Hyper-Connections](../../reproductions/2512.24880-mhc/README.md)（`mhc`）：Hyper-Connections 把单一 residual stream 扩为多个流并动态混合，但任意残差矩阵会破坏 identity mapping，深层组合可能放大信号。mHC 将 $H^{res}$ 投影到 Birkhoff polytope（非负、行列和均为 1），同时约束 $H^{pre}$、$H^{post}$ 非负；这样既保留跨流信息交换，又让每层残差映射非扩张。

## Dots Studio, Xiaohongshu

- 2026-10-15 · [Designing Transformers for Continuous Diffusion Language Models](../../foundation-models/2610.22330-langdit/README.md)（`langdit`）：连续扩散语言模型要从带高斯噪声的 token 嵌入恢复离散分布。原文§3把架构改动分为三个位置：backbone 的 RMS/QK 归一与噪声条件容量；词表 likelihood shortcut 的显式码本梯度路由和有界校准；训练期 bootstrap self-conditioning 的置信度衰减。LangFlow 的表示、交叉熵和采样器保持不变；Plaid 适配只迁移兼容子集，不能把两套梯度规则混为一谈。

## EIT-NLP

- 2026-07-30 · [WIDE: Boosting Adaptive LLM Inference via Token-level Dynamic Width Pruning](../../reproductions/2607.28418-wide/README.md)（`wide`）：静态剪枝无法按 token 难度分配算力，动态深度又过于粗粒度。WIDE 对每个 token 分别路由 attention head group 和 FFN channel group，并将 mask reorder、block skip 与设备内跳过联合设计。

## ETH Zurich

- 2026-10-15 · [Rethinking Routing Exploration in Modern Mixture-of-Experts](../../foundation-models/2610.22353-mirror-moe/README.md)（`mirror-moe`）：共享专家占据较多输出后，改变路由专家带来的表征差异减弱，而细粒度分割又扩大组合空间。MirrorMoE 不简单增噪，而是以镜像选择暂时抑制部分专家，随训练退火恢复普通路由。主源是 §3 的公式 3–6。

## European Molecular Biology Laboratory (EMBL)

- 2026-10-14 · [Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning](../../reproductions/2610.20158-oob-regularization/README.md)（`oob-regularization`）：联合嵌入自监督学习一方面拉近同一图像的不同增强视图，另一方面用抗坍塌正则保持表示多样性。小 batch 对整个表示分布的估计可能很差；单纯增大 GPU batch 又受显存限制。

## FAIR, Meta

- 2026-10-14 · [Open-world AI: a Tale of Three Requirements](../../foundation-models/2610.20782-memory-mosaics-plus/README.md)（`memory-mosaics-plus`）：固定任务的 IID 泛化不等于在开放世界中学习新任务。论文提出推理时学习、丰富表示和预测性解耦三个要求。§3.2 的 Mosaics+ 用短期模块先处理近期依赖，再以 Gaussian-kernel 长期记忆检索预测关联；two-stage 版本分别估计当前任务与相关任务，避免一锅混池让不相关历史越多越有害。

## FITec Labs

- 2026-09-15 · [Persistent Recurrent Memory Between Transformer Layers Improves Language Model Generalization](../../foundation-models/2609.17251-persistent-recurrent-memory/README.md)（`persistent-recurrent-memory`）：在 Transformer 上下半层之间插入 observe–GRU update–gated influence 的持久状态通路。

## Fudan University

- 2026-07-27 · [DataOrchestra: Learning to Orchestrate Per-Example Curation of Pretraining Data](../../reproductions/2607.24717-data-orchestra/README.md)（`data-orchestra`）：固定 corpus-level 清洗会过度处理本来干净的文本，也会对不同噪声使用同一操作。DataOrchestra 为每个 1024-token chunk 生成计划：先选 Drop、Untouch 或 Clean；Clean 时再按 NP（Noise Pruning）→ SR（Surface Rectification）→ PA（Pedagogical Augmentation）选择阶段，并为 rewrite 生成该 chunk 专属 instruction。

## Gensyn

- 2026-09-15 · [OPEN-1B: A Fully Auditable Training Run](../../foundation-models/2609.17380-open-1b-audit/README.md)（`open-1b-audit`）：固定 kernel reduction、数据批次与集体通信顺序，并用逐步状态哈希支持异构硬件单步重放审计。

## Google Brain

- 2021-01-11 · [Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity](../../reproductions/2101.03961-switch-transformer/README.md)（`switch-transformer`）：Switch 把 dense FFN 替换为每个 token 只激活一个专家的稀疏 MoE，在近似固定 FLOPs 下扩大参数容量。

## Google DeepMind

- 2025-02-20 · [SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features](../../reproductions/2502.14786-siglip2/README.md)（`siglip2`）：SigLIP 2 在 SigLIP 的 pairwise sigmoid loss 上组合 captioning pretraining、global-local self-distillation、masked prediction、在线数据筛选和 NaFlex 动态分辨率，改善语义、定位、 dense feature 与多语言公平性。

## Google Research

- 2023-05-22 · [GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](../../reproductions/2305.13245-gqa/README.md)（`gqa`）：多个 query head 共享较少的 K/V head，在 MHA 质量与 MQA 解码带宽之间取得可控折中。
- 2022-11-30 · [Fast Inference from Transformers via Speculative Decoding](../../reproductions/2211.17192-speculative-decoding/README.md)（`speculative-decoding`）：小 draft model 并行提出多个 token，target model 一次验证整个块；拒绝时从校正后的残差分布采样，从而严格保持 target 分布。

## Hanyang University

- 2026-09-04 · [BeaconKV: Key-Value Cache Compression Guided by Beacon Queries for Efficient Large Reasoning Model Inference](../../reproductions/2609.04971-beaconkv/README.md)（`beaconkv`）：长推理中会出现重新关注早期计划的 Thought Revisiting Token，只用最近 query 预测未来注意力会丢失这些远程依赖。BeaconKV 对历史 query 聚类并维护少量代表 query，用它们为 KV 重要性投票，在固定缓存预算中兼顾近期上下文和远程重访。

## Harvard University

- 2026-10-15 · [AdaLoop: Thinking with the Vision Encoder](../../foundation-models/2610.21323-adaloop-vision/README.md)（`adaloop-vision`）：普通 VLM 对所有问题只编码图像一次。视觉 AdaLoop 保持预训练视觉权重冻结，以问题池化向量调制共享视觉块，再循环更新内部视觉状态。它将“看几次”与问题联系起来，而不是让语言模型独自承担全部推理。
- 2026-10-15 · [RoleQ: Role-Aligned Scales for Converting Language Models to Ternary](../../foundation-models/2610.21808-roleq/README.md)（`roleq`）：按矩阵布局统一逐行放scale，会把写入残差流的不同功能单元混在一起。RoleQ按功能角色选轴：reader（Q/K/V与MLP输入）每输出单元一scale，writer（O与MLP输出）每输入单元一scale。完整RoleQ-T还需要旋转、GPTQ、蒸馏及可选Fisher二平面，不能以单个量化函数替代。

## Heinrich Heine University Düsseldorf

- 2026-08-06 · [MACRO: Markov Chain Routing of Transformer Layers](../../reproductions/2608.05872-macro/README.md)（`macro`）：**主题：动态层路由。** 固定顺序执行所有 Transformer 层并非总是最优。

## Huawei

- 2026-07-20 · [Convolution for Large Language Models](../../reproductions/2607.18413-conv-llm/README.md)（`conv-llm`）：自注意力擅长全局依赖，却没有显式的短程归纳偏置。论文固定 Qwen3 主干，系统比较 17 个卷积插入位置，最终选择在 Q/K/V 线性投影后、attention 聚合前加入 `kernel=3` 的逐通道一维卷积；残差旁路保留原投影，不加归一化或激活，额外参数低于 `0.01%`。

## Huawei ACS Lab

- 2026-07-23 · [Adaptive Depth Sparse Framework: Similarity-Driven Resource Allocation for Pre-Trained LLMs](../../reproductions/2607.21291-adadsf/README.md)（`adadsf`）：固定比例的 Mixture-of-Depths 会给每一层相同 token budget，但不同层对表示的改写强度并不相同。AdaDSF 先在 dense teacher 上测量各层输入/输出 cosine similarity，再把更多计算分给变化更大的层；每层 MLP router 只把 Top-K token 送入原 Transformer block，其他 token 走 residual bypass。

## Huawei Technologies Canada

- 2026-08-05 · [DBLast: Dependent Block Drafting for Stochastic Speculative Decoding](../../reproductions/2608.05448-dblast/README.md)（`dblast`）：**主题：推测解码。** 并行 block drafter 常把位置条件独立化，在高熵采样时难以匹配联合分布。

## Huazhong University of Science and Technology

- 2026-08-21 · [RARE: Decoupling Representation Steering from Expert Routing in Mixture-of-Experts Language Models](../../reproductions/2608.21236-rare/README.md)（`rare`）：Dense LLM 的 activation steering 直接用于 MoE 时会改变 router logits，token 被送往不同专家后，原估计的行为方向失效。RARE 将任意 steering direction 投影到 router 的零空间，并在后续保护层再次移除传播产生的 router-visible 分量，在保留原专家路径的同时改变行为表征。

## Hugging Face

- 2025-04-07 · [SmolVLM: Redefining small and efficient multimodal models](../../reproductions/2504.05299-smolvlm/README.md)（`smolvlm`）：SmolVLM 重新分配小模型视觉/语言侧算力，以 pixel shuffle 将相邻空间 token 搬到 channel 维，再用 MLP 映射到 LM 空间；同时研究长上下文、图像切片、学习位置 token 和数据配比， 使 256M/500M/2.2B 模型在低显存下保持图像与视频能力。

## Independent Researcher, Chile

- 2026-10-15 · [Patch where the text is new: a compression view of where byte-level models should spend compute](../../foundation-models/2610.22100-novelty-patching/README.md)（`novelty-patching`）：Byte-level 模型按 patch 调用全局模型。本文用近期重复程度预测替代纯熵边界；离线计算匹配标签，在线只查前两字节。主源位置为 §3 方法、§4-7 结果及负结果、§8 限制和 Code and data。

## Independent researchers

- 2026-07-23 · [Anti-Periodic Positional Encoding: Möbius Boundary Conditions Make In-Context Retrieval Reliable](../../reproductions/2607.21405-mobius-rope/README.md)（`mobius-rope`）：标准 RoPE 的随机种子会显著影响长距离 needle retrieval。论文为部分 attention heads 使用反周期频率梯度，使跨完整训练窗口的旋转恒为 $-I$；其余 heads 保留标准 RoPE，以维持语言建模能力。
- 2026-07-23 · [Naju: A Native Discrete State-Space Model with Independent Retention and Writing for Long-Sequence Memory](../../reproductions/2607.21000-naju/README.md)（`naju`）：Mamba 从连续时间系统离散化得到转移，单一耦合门也容易形成“强保留就难写入”的约束。Naju 直接参数化离散 pole，将 retain gate 和 write gate 分开，并保留 token-dependent $B/C$ 方向、短程因果卷积、直接 feedthrough 与输出调制。

## Indian Institute of Technology Madras

- 2026-07-18 · [OpenLanguageModel: Readable and Composable Small-Language-Model Pretraining for Education and Research](../../reproductions/2607.16669-open-language-model/README.md)（`open-language-model`）：许多预训练框架把模型结构、训练循环和分布式运行强耦合，难以做透明消融。OLM 让组件保持普通 PyTorch module，用 Block、Residual、Repeat、Parallel 描述布线，同一模型可从 notebook 迁移到 CPU、单 GPU 和单机多 GPU。

## Indian Institute of Technology Roorkee

- 2026-08-05 · [QEvict: Recoverable Quantized KV Eviction for Attention-Drift-Robust Long-Context Decoding](../../reproductions/2608.05326-qevict/README.md)（`qevict`）：**主题：长上下文 KV cache。** 二元保留/删除无法应对注意力漂移：今天不重要的窗口可能稍后重新活跃。

## Institute of Computing Technology, Chinese Academy of Sciences

- 2026-09-29 · [SPLASH: Switching Parallel Layouts of Attention with Seamless Handoff for LLM Serving](../../foundation-models/2609.37626-splash/README.md)（`splash`）：统一描述 attention weight 与 KV cache 的所有权，引入权重分片、请求独占 KV 的 DOP；调度器把布局切换成本按剩余步数摊销，在 TP、DP、CP、DOP 间在线切换。
- 2026-08-07 · [Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry](../../reproductions/2608.06849-autonomy-heads/README.md)（`autonomy-heads`）：直接从冻结 QK 投影的谱有效秩区分 retrieval 与 streaming heads，无需校准数据或运行时门控。

## Johns Hopkins University

- 2026-10-08 · [VFold: Symmetry-Aware Cross-Layer Value Cache Compression](../../foundation-models/2610.12338-vfold/README.md)（`vfold`）：相邻层的 Value 不一定在同一坐标系。VFold 用满秩 CCA 对齐和 Hungarian 头匹配，离线把变换折进 Value/输出投影；当前 token 先以完整 Value 参与注意力，随后才与相邻层平均共享。Key 不合并，首尾重要 token 独立保存。

## KAIST

- 2026-08-26 · [MLLMCLIP: Feature-Level Distillation of MLLM for Robust Vision-Language Representations](../../reproductions/2608.25575-mllmclip/README.md)（`mllmclip`）：MLLM 的丰富视觉语义难以直接迁移到轻量 CLIP。论文从 teacher 各层按 attention 自适应选 token，以 CKA 对齐 student 图像/文本特征，保留部署时的双塔效率。

## MIT

- 2023-06-01 · [AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration](../../reproductions/2306.00978-awq/README.md)（`awq`）：利用 calibration activation 找到显著输入通道，通过等价通道缩放保护约 1% 关键权重，再执行硬件友好的统一低比特 weight-only 量化。

## ML Collective

- 2026-10-09 · [SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices](../../reproductions/2610.13740-smolwam/README.md)（`smolwam`）：Cosmos Policy 将机器人状态、两路相机、动作和未来状态编码为九个 latent frame，沿用视频生成接口：33 帧 VAE、T5-XXL、28-block 2B DiT、1764 tokens 和五步去噪。SmolWAM 并非只换一个轻量 action head，而是在保留预训练 trunk、token 原位置与 rectified-flow readout 的同时，逐项恢复接口改变造成的分布偏移。

## McGill University

- 2026-07-20 · [PPL-Factory: Task-Aware and Budget-Aware Data Selection from Language Modeling to Reasoning](../../reproductions/2607.18199-ppl-factory/README.md)（`ppl-factory`）：固定的“选最难/最容易”规则会随任务和数据预算失效。PPL-Factory 先用冻结基础模型计算任务相关 NLL：语言建模按 packed block，推理 SFT 只看 reasoning/answer response；再按预算切换策略，高预算偏 easy，较低预算选 middle，极低预算从 middle pool 随机抽样以保覆盖。

## Meta

- 2026-10-15 · [Architecting for Hardware Diversity: Meta's End-to-End Co-Design for High-Performance AI Training on AMD GPUs](../../foundation-models/2610.22230-hardware-diversity/README.md)（`hardware-diversity`）：CUDA 程序能够转换为 HIP，不代表跨硬件性能相同。本文以推荐训练为案例，联合修改模型/并行与内存策略，用分析模型选择 GEMM 配置，并用 Agent 辅助编译、调试和内核移植；它是系统研究报告，而非单一新推荐模型。 **成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。**
- 2026-08-05 · [Towards Physics of Multimodal Pretraining: Knowledge Flow, Modality Synergy, Early Unification, and Recipes](../../reproductions/2608.05000-physics-mm-pretraining/README.md)（`physics-mm-pretraining`）：用受控实验刻画模态知识流、协同/竞争、早期统一和共享 attention+norm/模态专属 FFN 配方。

## Meta FAIR

- 2024-12-13 · [Byte Latent Transformer: Patches Scale Better Than Tokens](../../reproductions/2412.09871-blt/README.md)（`blt`）：直接处理 byte，并依据 next-byte entropy 动态形成 patch；全局 Transformer 在 patch 级计算，局部编码器/解码器恢复 byte。

## Meta Reality Labs Research

- 2026-10-09 · [EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference](../../reproductions/2610.14324-ev-jepa/README.md)（`ev-jepa`）：固定容量的视频模型难以同时适配端侧预算和跨设备协作，独立训练不同宽度也不保证中间表示兼容。EV-JEPA共享嵌套宽度参数，每步联合训练窄、宽与窄转宽三条路径，以冻结视频教师约束共同表示空间，并增加可调token压缩。 **成本过高，暂不复现；待验收，未注册可执行入口。**

## MiniMax

- 2026-06-11 · [MiniMax Sparse Attention](../../reproductions/2606.13392-minimax-sparse-attention/README.md)（`minimax-sparse-attention`）：长上下文 dense attention 的二次复杂度成为主要瓶颈。MSA 为每个 GQA 组增加轻量 index branch，先选择少数历史 block，主分支再对命中 token 做精确 attention；训练和推理使用同一路径。

## Mohamed bin Zayed University of Artificial Intelligence

- 2026-10-14 · [EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos](../../foundation-models/2610.20904-egojepa/README.md)（`egojepa`）：人类第一视角视频中的手运动不需要经规则映射为每种机器人的动作。EgoJEPA先用手部运动差分条件JEPA预测未来视觉表示，再联合建模视觉与潜动作，最后仅适配目标机器人的输入输出动作接口。 **成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。**

## Moonshot AI

- 2025-02-24 · [Muon is Scalable for LLM Training](../../reproductions/2502.16982-muon/README.md)（`muon`）：AdamW 把矩阵参数当作独立标量更新，Muon 则把隐藏层梯度视为矩阵，通过 momentum 与 Newton–Schulz 近似极分解得到正交化更新方向。论文为大规模训练补上 weight decay 和按参数形状缩放；非隐藏矩阵参数继续使用 AdamW。
- 2025-02-18 · [MoBA: Mixture of Block Attention for Long-Context LLMs](../../reproductions/2502.13189-moba/README.md)（`moba`）：把序列切成 block，以可微 router 为每个 query 选择少量相关块，同时保留当前因果块。

## Multiverse Computing

- 2026-10-15 · [When the KV Cache Is Slower Than the GPU: Scaling Remote KV Tiers for Context-Parallel Prefill](../../foundation-models/2610.21500-remote-kv-tiers/README.md)（`remote-kv-tiers`）：缓存命中不一定更快。该工作先计算加载与重算的盈亏平衡带宽和固定开销，再把MLA KV缓存按PCP rank分片，并使用rank独立远程实例和异步加载消除队首阻塞。 **成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。**

## NVIDIA

- 2026-07-23 · [Windowed-MTP: Removing the Full-Context Draft-KV Tax at Million-Token Context](../../reproductions/2607.21535-windowed-mtp/README.md)（`windowed-mtp`）：内置 MTP/NEXTN draft 通常每提出一个 token 都读取完整 KV cache；在百万 token 上，即使 target 已使用 GDN/Mamba 等便宜 verifier，draft 的全量 KV read 仍会成为瓶颈。Windowed-MTP 只改变 draft：保留最前面的 attention sink 与最近 $W$ 个 token，同时 target 继续读取完整上下文并验证所有候选。
- 2024-11-20 · [Hymba: A Hybrid-head Architecture for Small Language Models](../../reproductions/2411.13676-hymba/README.md)（`hymba`）：同一层并行执行 attention 与状态空间分支，再用输入相关 gate 融合局部精确检索和线性长程状态。

## Nanjing University

- 2026-10-14 · [Memory-Efficient Subspace Optimization with Residual Correction: From Momentum SGD to Muon](../../reproductions/2610.19844-smrc-pmrc/README.md)（`smrc-pmrc`）：低秩优化器只存投影后的动量，能减少持久状态；但梯度主奇异方向可能被噪声占据，直接丢掉子空间外分量会遗漏有效下降方向。本文让低秩动量负责投影内更新，原始梯度的正交残差负责其余方向，不额外保存一个全尺寸残差状态。

## Nanyang Technological University

- 2026-10-15 · [Prism-1: Position- and Rival-Independent Scoring for System One Models](../../foundation-models/2610.22066-prism-1/README.md)（`prism-1`）：JEV/System One 选择模型希望在一次前向中选出工具、意图或界面元素。普通多选提示会让答案依赖选项顺序和无关选项。§2–4 由 Luce 选择公理推导：每个选项的分数只能看共享状态、问题和该选项本身；最后对独立分数做 softmax。只在输出层加 softmax、不隔离 attention 或不重置位置，都不能保证这一性质。
- 2026-10-01 · [TESS: Scalable, Transferable Meta-network for Data Selection Requires a Different Loss (and Why the Obvious Choice is Problematic)](../../foundation-models/2610.02092-tess/README.md)（`tess`）：先分别训练仅看训练集的模型和加入验证集指导的模型，以两者逐样本损失差构造价值伪标签；再用 pointwise value matching 训练数据 selector。避免直接选择目标的病态优化，并让小规模教师产生的选样规则迁移到更大的未见数据池。
- 2026-08-26 · [VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning](../../reproductions/2608.26105-vbvr-pro/README.md)（`vbvr-pro`）：通用 VLM judge 容易被流畅输出误导，难以逐实例核对时空状态。VBVR-Pro 为每种任务定义可执行 scorer，把中间状态、约束和最终状态都变成可验证奖励，并据此训练多模态生成模型。

## National University of Defense Technology

- 2026-10-15 · [Compression Does Not End at Selection: Post-Selection Positional Geometry for Sparse KV Caches](../../foundation-models/2610.21126-rope-relay/README.md)（`rope-relay`）：selector 删除 token 后，K 仍携带稀疏旧坐标的旋转相位。RoPERelay 不重选内容、不重新 prefill 历史，将选中状态按原始时间排序、压紧坐标，并同步问题及生成坐标。来源为 §3、附录 A 的 Algorithm 1 和数值约定。

## New York University

- 2026-08-13 · [Fast A/B/n Testing: Exact Multi-Policy Comparison via Tree-Coupled Feedback Sharing](../../reproductions/2608.12831-tcab/README.md)（`tcab`）：用最大耦合和最小生成树共享相同决策的反馈，同时保持每个自适应策略的边际轨迹分布不变。

## Oklahoma State University

- 2026-08-09 · [DistillCache: KL-Guided Adaptive KV-Cache Eviction for Memory-Efficient LLM Inference](../../reproductions/2608.08878-distillcache/README.md)（`distillcache`）：把 KV 淘汰视为序列决策，以逐步 KL 奖励训练轻量策略保留未来预测分布。

## OpenAI

- 2021-02-26 · [Learning Transferable Visual Models From Natural Language Supervision](../../reproductions/2103.00020-clip/README.md)（`clip`）：用独立图像/文本 encoder 将配对样本映射到同一单位球面，通过双向 batch contrastive objective 学习可迁移零样本表示。

## Peking University

- 2026-03-27 · [Switch Attention: Towards Dynamic and Fine-grained Hybrid Transformers](../../reproductions/2603.26380-switch-attention/README.md)（`switch-attention`）：静态 hybrid attention 对所有 token 使用固定模式。Switch Attention 学习细粒度 router，只让需要全局信息的 token 走 full attention。

## Pennsylvania State University

- 2026-07-23 · [Parameter-free Adaptive Sparse Attention via Compression-Based Content Selection](../../reproductions/2607.21752-gzip-sparse-attention/README.md)（`gzip-sparse-attention`）：固定 BigBird/Longformer mask 不理解内容，learned mask 又需要额外参数、梯度估计或专用 kernel。论文把字节序列切成固定 block，用 gzip 压缩率作为无需训练的信息密度信号：高于样本均值的 literal blocks 互相建立长程连接，所有 block 保留局部窗口，不设置固定 global token。

## Princeton University

- 2026-10-09 · [ReplaySSM: Cache SSM Inputs, Not State](../../reproductions/2610.13778-replayssm/README.md)（`replayssm`）：Mamba2/GDN 解码一般每 token 读写完整矩阵状态，常受显存带宽限制。ReplaySSM 把持久化状态与输出计算拆开：每 16 token 才刷新 checkpoint，其间只记录小型输入；输出由 checkpoint 与输入重放计算。
- 2026-08-03 · [Learning What to Remember: Test-Time Training via Context Distillation](../../reproductions/2608.01672-ttcd/README.md)（`ttcd`）：长窗口教师以隐藏状态差异监督短窗口学生的 fast weights，使有限记忆优先保留未来有用信息。

## Qwen

- 2025-05-10 · [Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free](../../reproductions/2505.06708-gated-attention/README.md)（`gated-attention`）：softmax attention 的 value aggregation 到 output projection 之间基本是线性映射。论文系统比较 30 种门控变体，发现最简单稳定的方案是在每个 attention head 的 SDPA 输出后施加 query-dependent sigmoid gate：既增加非线性，也能稀疏抑制无用 head 输出。

## Salesforce AI Research

- 2026-09-03 · [Random Attention: Rethinking KV Cache Eviction for Efficient Reasoning](../../reproductions/2609.03430-random-attention/README.md)（`random-attention`）：传统 KV 淘汰先计算 token 重要性，Random Attention 则始终保护 prompt，仅在已生成 token 中逐 head 独立随机保留固定预算；它省掉评分 pass，也避免所有 head 被同一排序规则约束。

## Salesforce Research

- 2023-01-30 · [BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models](../../reproductions/2301.12597-blip2/README.md)（`blip2`）：BLIP-2 冻结已有视觉 encoder 和 LLM，只训练轻量 Q-Former。固定数量的可学习 query 通过 cross-attention 从视觉 token 提取与语言最相关的信息；第一阶段做图文表征学习，第二阶段将 query 输出投影成冻结 LLM 的 soft visual prompt。

## Seoul National University

- 2026-10-14 · [PN-Mix: Pair-Norm Guided Mixed-Precision Key Cache Quantization for Efficient Long-Output LLM Inference](../../reproductions/2610.19605-pn-mix/README.md)（`pn-mix`）：长输出解码的 KV cache 随 token 数增长；一律把 K 降到低位宽，会放大 attention logit 的偏差。PN-Mix 的精度分配不是仅按 K 的幅度排序：它同时观察 prefill 的 Q 和 K，把实际 RoPE 旋转耦合的两个通道作为整体，以两侧平均范数乘积预测重要性。

## Shanghai AI Laboratory

- 2026-10-08 · [Smoothing the Top-k Exposure Boundary for Sparse Mixture-of-Experts](../../foundation-models/2610.11575-elastic-expert-routing/README.md)（`elastic-expert-routing`）：固定 Top-k 会让排序边界外的专家长期缺少训练曝光。该方法训练时为每个 token、每层独立抽取邻近的专家预算，在不改变期望预算的情况下，让边界附近专家参与真实稀疏计算。部署时恢复固定 k。

## Shanghai Jiao Tong University

- 2026-10-09 · [Multi-Stream Attention Residuals](../../reproductions/2610.13630-msar/README.md)（`msar`）：标准残差把历史更新压成一个累加向量；AttnRes 能逐层检索，但只有一个深度注意力流。MSAR 保留每个完整 hidden 向量，用序列上下文产生不同尺度的完整视图，再对每个流独立做深度 softmax。
- 2026-07-20 · [C²KV: Compressed and Composable KV Cache Reuse for Efficient LLM Inference](../../reproductions/2607.17715-c2kv/README.md)（`c2kv`）：以 compression tokens 和结构化 attention 学习位置无关、可拼接的压缩 KV manifold，并联合训练压缩与复用。

## Shanghai University of Finance and Economics

- 2026-09-04 · [KVMem: Virtualizing Million-Token Agent Workspaces on a Consumer GPU](../../reproductions/2609.04852-kvmem/README.md)（`kvmem`）：长寿命 Agent 的历史会同时超过显存和模型原生窗口；摘要压缩会丢证据，文本检索又要重复 prefill。KVMEM 把已计算 KV 分页放到 GPU、主存和 NVMe，用模型自身的注意力空间索引挑选相关 block，再物化为不超过原生窗口的执行视图。

## Stanford University

- 2023-05-17 · [DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining](../../reproductions/2305.10429-doremi/README.md)（`doremi`）：用小型 proxy model 的 excess loss 做 group DRO，动态提升欠拟合域权重，再按所得配比训练目标模型。

## Sun Yat-sen University

- 2026-08-27 · [PACE: A Unified Condense-and-Extract Paradigm for Fast VLM Inference](../../reproductions/2608.27206-pace-vlm/README.md)（`pace-vlm`）：VLM 的视觉 token 一方面在 prefill 阶段带来大量计算，另一方面在抽取阶段仍会保留大量与问题无关的内容。PACE 将两个阶段拆开处理：APC 用浅层 ViT preview 同时估计全局语义密度和局部细节，按图像难度自适应缩放；DDAE 再融合 LLM 与视觉编码器的注意力，以置信度决定两种证据各占多少权重，而不是固定只信一种注意力图。

## Tel Aviv University

- 2026-10-15 · [SoftCache: Adaptive Step Size Caching for Diffusion Transformers](../../foundation-models/2610.22369-softcache/README.md)（`softcache`）：动态缓存通常只决定“刷新/重用”，仍沿固定时间网格走。SoftCache 将累计陈旧度距离阈值的 headroom 转成连续步长：缓存越可靠就走得更远。它用两次新鲜残差作时间外推，并重新排布剩余节点，使跳过的节点不会又被访问。

## Tencent HY LLM Frontier

- 2026-09-11 · [SAS: Simple Attention Sparsification via End-to-End Optimization of Context Ranking](../../reproductions/2609.13141-sas-attention/README.md)（`sas-attention`）：硬 Top-K 只能改变被选中的索引，语言模型损失无法沿离散索引直接训练 selector。SAS 不再蒸馏 dense attention：selector 先给历史块连续打分，训练时保留 Top-K 块的连续 gate，并把 `log(gate)` 加到注意力 logits 内。

## The Chinese University of Hong Kong, Shenzhen

- 2026-10-09 · [Not All Dimensions Are Equal: Outlier-Aware Attention Linearization with Grouped Quadratic Kernels](../../reproductions/2610.13674-oal/README.md)（`oal`）：预训练 attention 的 QK 各维度贡献不均匀，少量高贡献坐标包含较多 softmax 近似误差。OAL 先在 post-RoPE QK 上计算因果贡献，以 prompt bootstrap 识别高贡献尾部的稳定边界；随后学习共享组和组对系数的二次核。

## The Hong Kong Polytechnic University

- 2026-10-09 · [Orthros: Phase-Aware Heterogeneous Attention for Efficient Transformers](../../reproductions/2610.13735-orthros/README.md)（`orthros`）：长 prompt、短回答的推理中，prefill 与 decode 的计算角色不同。Orthros 保留两个 token 流：base tokens 对所有位置执行固定窗口 SWA，并构建完整的逐层 KV；output-specific tokens 只在需预测输出的位置出现，用共享 KV 做全历史 causal cross-attention。

## The Hong Kong University of Science and Technology (Guangzhou)

- 2026-08-27 · [TwinKV: A Composable Repair Pass for KV Cache Eviction via Pairwise Key Redundancy](../../reproductions/2608.27128-twinkv/README.md)（`twinkv`）：现有 KV eviction 常按 token 重要性选择缓存，但可能同时保留多个几乎重复的 key，并删掉没有替代者的 orphan。TwinKV 不替代 StreamingLLM、H2O 等基础策略，而是一个可组合 repair pass：在完全不增加 KV budget 的前提下，找出“被删且没有相似保留项”的 orphan，与“已保留但有高度相似 twin”的 donor 成对交换。

## The University of Texas at Austin

- 2026-09-29 · [Time-Anchored Diffusion Language Models: Latent-Space Caching for Fast Generation](../../foundation-models/2609.37924-tadm/README.md)（`tadm`）：将昂贵 anchor network 的潜表示跨多个反向扩散步缓存，只周期性刷新；小型 fusion module 根据当前状态门控修正陈旧 anchor，再交给轻量 denoiser。

## Together AI

- 2024-01-19 · [Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](../../reproductions/2401.10774-medusa/README.md)（`medusa`）：在冻结或联合微调的 backbone 上增加多个 future-token heads，以 tree attention 同时验证候选分支，减少串行解码步数。

## Tsinghua University

- 2026-09-29 · [V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents](../../foundation-models/2609.37250-vjepa-policy/README.md)（`vjepa-policy`）：冻结 V-JEPA 2.1 视觉编码器，在预测视觉潜空间中联合训练 instruction-conditioned future-latent predictor 和 flow-matching action expert；动作生成读取 predictor 的未来信息上下文。
- 2026-05-20 · [Memory Grafting: Scaling Language Model Pre-training via Offline Conditional Memory](../../reproductions/2605.20948-memory-grafting/README.md)（`memory-grafting`）：Engram 的大容量条件记忆需要随主模型从零训练。Memory Grafting 先统计高频 2/3/4-gram，用已经预训练的 grafting model 离线编码每个短语最后 token 的中间 hidden state并冻结；recipient 在线只做期望 $O(1)$ 的最长后缀精确查询。

## University at Albany, SUNY

- 2026-10-15 · [DropKV: Decoupling Residual-Output Perturbation for Near-Optimal KV-Cache Eviction](../../foundation-models/2610.22130-drop-kv/README.md)（`drop-kv`）：只按 attention 权重淘汰 KV 会忽略 value 内容。DropKV 将组合驱逐近似为逐 token 输出扰动，跨观察窗口累加、池化，并保护近期 token。§3 与 Algorithm 1 定义评分；§4 的近似保证有条件，不能解释成任意输入上的全局最优。

## University of California, San Diego

- 2026-10-08 · [LeWAM: End-to-End World and Action Modeling with JEPAs](../../reproductions/2610.12818-lewam/README.md)（`lewam`）：传统 JEPA 学习“给定动作会到什么状态”，之后另训逆动力学或在线搜索动作。两阶段会使控制监督无法塑造视觉表征，宽高斯动作搜索也较昂贵。
- 2026-08-06 · [BaKron: Efficient Quantization with Kronecker-Factored Hessians](../../reproductions/2608.06291-bakron/README.md)（`bakron`）：**主题：二阶量化。** GPTQ 通常只利用输入侧曲率；双侧 Kronecker Hessian 更丰富但直接向量化求解昂贵。

## University of Cambridge

- 2026-10-15 · [BitSparse: Compact Activation Storage for ReLU Feed-Forward Networks](../../foundation-models/2610.22256-bit-sparse/README.md)（`bit-sparse`）：ReLU 家族已有大量精确零；BitSparse 保存 bitmask、正值和 tile prefix，在反向时无损重建，避免靠有损量化或额外前向换空间。§3 定义格式，公式 1–2 与 Appendix C 定义 ReLU/ReLU² 线性层反向。
- 2026-10-15 · [LCT: Losslessly Compressed Tensors with GPU friendly execution for Training](../../foundation-models/2610.22179-lct/README.md)（`lct`）：浮点指数往往比 sign/mantissa 更可压缩，但训练需要反复编码。LCT 将两部分分开，以固定模型预计算短码，运行时中心变换适应量级，循环 stream 在固定预算之外保留原始指数尾。主源 §4、Appendix B/C；不是用通用 zlib 压缩替代算法。
- 2026-07-22 · [GaugeQuant: Online Learning of Quantization-Optimal Bases from LLM Symmetries](../../reproductions/2607.20757-gaugequant/README.md)（`gaugequant`）：LLM 内部通道存在保持函数不变的 gauge 对称性，但不同等价基的量化误差差异很大。GaugeQuant 在训练中在线学习量化友好正交基，以 LogSumExp 压制 activation outliers，不需要额外 calibration corpus。
- 2024-03-25 · [Data Mixing Laws: Optimizing Data Mixtures by Predicting Language Modeling Performance](../../reproductions/2403.16952-data-mixing-laws/README.md)（`data-mixing-laws`）：先训练多组小预算 domain mixture，拟合各评测域的混合缩放律，再搜索未训练过的最优配比。

## University of Electronic Science and Technology of China

- 2026-10-14 · [Selective Reasoning for Typed Decision Models: When to Start, Read, and Stop](../../system-one/2610.19644-selective-reasoning/README.md)（`selective-reasoning`）：Typed decision model 从明确候选中返回选择，适合 JEV / System One 式判断，但直接读出不一定足以完成多步推理。始终生成很长的推理又浪费算力。本论文在冻结 Qwen3.5-4B 上拟合共享 candidate-answer reader，让空推理前缀和中间推理前缀都能返回候选分布。

## University of Illinois Urbana-Champaign

- 2026-07-30 · [ReToken: One Token to Improve Vision–Language Models for Visual Retrieval](../../reproductions/2607.28627-retoken/README.md)（`retoken`）：常规 VLM 检索需要先用外部 retriever 找图，再把入选图重新编码，无法直接复用预填充的视觉 KV cache。ReToken 在输入中增加一个可学习 token，让它在最后一层 value projection 空间与每张图的平均 value 向量打分；只训练该 token 和一张投影矩阵，以 class-balanced BCE 监督相关/无关图，VLM 默认冻结。

## University of Maryland

- 2026-07-16 · [Looped Latent Attention: Cross-Loop KV Compression for Looped Transformers](../../reproductions/2607.15456-looped-latent-attention/README.md)（`looped-latent-attention`）：Looped Transformer 重复使用同一组权重，但不同 loop 的 KV cache 仍重复占内存。LLA 学习跨 loop 共享的低秩 K/V latent，服务时按 loop 重建专用 K/V，从 recurrence 冗余中换取近无损压缩。

## University of Texas at Austin

- 2026-08-06 · [Hierarchical Latent Prediction for Language Models](../../reproductions/2608.05806-hilp/README.md)（`hilp`）：**主题：分层 latent 预训练。** NextLat 的逐步 latent rollout 会累积误差。

## University of Tübingen

- 2026-10-15 · [Retrofitting Recurrent Vision-Language Models from Pretrained Backbones](../../foundation-models/2610.22075-rr-vlm/README.md)（`rr-vlm`）：预训练 VLM 的语言层可以剪掉一段，再共享循环保留核心块；但直接手术会破坏语言能力及图文对齐。RR-VLM 用一个线性 adapter 融合 prelude 上下文与循环状态，并依次执行文本恢复、projector 对齐、全模型指令恢复；文本和最终阶段加入原始未剪模型蒸馏。

## University of Washington

- 2021-08-27 · [Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation](../../reproductions/2108.12409-alibi/README.md)（`alibi`）：不学习位置向量，而是在每个 head 的注意力 logits 上加入线性距离惩罚，实现 train-short/test-long 外推。

## University of Wisconsin-Madison

- 2023-04-17 · [Visual Instruction Tuning](../../reproductions/2304.08485-llava/README.md)（`llava`）：冻结视觉 encoder，用可训练 projector 把视觉特征映射到 LLM token 空间，再在 GPT-4 生成的多模态指令数据上做端到端 instruction tuning。

## University of Wisconsin–Madison

- 2026-09-14 · [Register Tokens for Bounded-State Reasoning in Diffusion Language Models](../../foundation-models/2609.16372-register-tokens-dllm/README.md)（`register-tokens-dllm`）：清除上一段文本后仅携带固定数量的连续 register hidden states，让扩散语言模型跨 chunk 推理。

## WeChat Vision, Tencent

- 2026-08-25 · [WeMM-Embedding: WeChat Multi-Modal Embedding Technical Report](../../reproductions/2608.24053-wemm-embedding/README.md)（`wemm-embedding`）：不同检索任务通常维护独立的文本、图像、视频或文档 encoder。WeMM 把任意交错多模态输入映射到同一空间：第一阶段用数亿 pair 做大规模 alignment；第二阶段加入精选 relevance、细粒度监督和跨尺度知识迁移，并用 Matryoshka 表征支持按成本选择输出维度。

## Westlake University

- 2026-10-08 · [SparseDecoding: Decoding-Aware Pruning for Accurate and Efficient LLM Inference](../../foundation-models/2610.12327-sparse-decoding/README.md)（`sparse-decoding`）：固定文本的 teacher-forcing 激活不等于模型自回归生成时的激活。该方法让稠密模型先从任务问题生成回答，只保存逐 token 解码激活、排除 prefill，再用这些统计量执行剪枝。校准协议与剪枝后端分离：原文主要使用 SparseGPT，也报告 Wanda 消融。

## Wuhan University

- 2026-09-15 · [ECHO: Early-layer Collaborative Hierarchical Orchestration with Bonus Logits in Speculative Decoding](../../foundation-models/2609.17241-echo/README.md)（`echo`）：用早层高频探索与末层低频权威校验组成双循环；两侧 bonus logits 协同补树，并保留精确拒绝采样校正。

## Xiaomi AI Lab

- 2026-10-08 · [CoTS: Competitive Token Selection for Latent Reasoning in Large Language Models](../../foundation-models/2610.20642-cots/README.md)（`cots`）：连续 reasoning 的 soft token 可能偏离离散轨迹。CoTS 用 top-2 概率竞争分配 soft 混合强度，保留 sampled token 至少半数权重，并在结束推理后锁定纯离散输出。主源为 §3.1-3.3 的公式 1-6；实验配置和消融见 §4。

## Zhejiang University

- 2026-08-03 · [DART: Decoded Attention over Recurrent States for Efficient Long-Context Sequence Modeling](../../reproductions/2608.02032-dart/README.md)（`dart`）：保留 Mamba-2 chunk state contributions，解码 token-conditioned K/V 并执行 state-memory attention。

## Zhuiyi Technology

- 2021-04-20 · [RoFormer: Enhanced Transformer with Rotary Position Embedding](../../reproductions/2104.09864-rope/README.md)（`rope`）：对每个 attention head 的 Q/K 二维子空间施加随位置旋转，使点积天然只依赖相对位移。

## d-Matrix

- 2026-10-09 · [DualQuant: Dual-scale Calibration-free Weight-and-Activation Quantization for LLMs](../../reproductions/2610.13767-dualquant/README.md)（`dualquant`）：W+A量化中，权重与激活误差相互放大；仅最小化逐row动态范围不能消除跨row系统性column outlier。DualQuant只读取静态权重，以row/block尺度与column尺度共同最小化重建MSE。

## 未注明（论文未列一作机构；公开发布主体为 MindLab）

- 2026-10-15 · [MJev-Spatial: System One Spatial Intelligence via Native Attention Matching](../../foundation-models/2610.22276-mjev-spatial/README.md)（`mjev-spatial`）：空间问题往往只需选项、数值或二维点，却仍让 VLM 自回归生成并解析答案。MJev-Spatial 将三者统一为候选分类：decision marker 提供 query，candidate-end marker 提供 key，直接复用骨干最终注意力投影。连续量通过分桶或三级区域细化预测，不增加独立分类头。

## 论文未列一作机构

- 2026-10-15 · [When Does Muon Actually Win? A Paired Data-, Time-, and Tuning-Budget Benchmark](../../foundation-models/2610.21555-muon-paired-budget/README.md)（`muon-paired-budget`）：优化器每步效果更好不等于同时间更好，也不意味着更容易调参。论文在单A100上对齐初始化、数据顺序和开发候选数，分别比较数据、训练时间、冻结调参池三种预算。它不是新的Muon优化公式，主要贡献是谨慎分离比较口径。测试数据在选参和轨迹分析冻结后只评一次。

## 论文未列机构

- 2026-10-14 · [One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models](../../foundation-models/2610.19375-jepa-prediction-planning/README.md)（`jepa-prediction-planning`）：JEPA 在自己的潜空间预测下一观察，较小的一步 loss 不一定表示更好的长程行动。论文固定一个只在真实观察编码上拟合的物理状态解码器，分别解码真实下一表征与预测下一表征，把编码器本身的可读性和预测器新增的误差拆开。规划仍用相同 checkpoint、相同任务和配对种子单独执行，不能由预测指标推导成功率。
- 2026-08-03 · [Role-Decoupled Attention Residuals](../../reproductions/2608.01075-rd-attnres/README.md)（`rd-attnres`）：Block AttnRes 让注意力层从全部历史 residual sources 动态读取，但 Q、K、V 共用一条深度路由。论文指出 QK 负责匹配、V 负责承载内容，两者偏好的深度未必相同；RD-AttnRes 在不改变 residual sources 和 attention 主体的情况下，只为 V 增加一个 model-width 路由向量。
- 2026-07-28 · [Penelope: Localized Latent Recurrence for Efficient Structured Reasoning](../../reproductions/2607.25915-penelope/README.md)（`penelope`）：只在一个 decoder 边界执行共享权重的 latent recurrence，用门控状态反复精炼表示，避免整条 decoder 重跑。
