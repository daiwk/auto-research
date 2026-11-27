---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 推理压缩先找瓶颈：权重、KV 内容与缓存层级

[基础模型](../index.md) · 更新 2026-11-27 · 44 篇主题资料 / 21 篇重点对照

AWQ 减权重位宽，GQA 减 KV 头，DropKV 与 TwinKV 改保留内容，KVMEM 管可执行历史视图，Remote KV Tiers 解决跨层级加载。它们可以组合，但不能用一个“压缩率”解释质量、可恢复性和端到端速度。 FoldBias另解决压缩缓存的接口障碍：把静态bias折进同维key，但未来query漂移仍会引入误差。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/foundation-models/compression-and-cache.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：压缩对象是权重、KV 头、token 还是分页存储 · 信息被量化、永久淘汰还是留在外部待取回 · 选择依赖激活、query、相似替代关系还是带宽模型 · 节省显存、带宽和重算时间分别需要什么条件

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration](../../../reproductions/2306.00978-awq/README.md) · [原始来源](https://arxiv.org/abs/2306.00978)<br>章节：背景与主要改动、核心公式、复现边界 | 用校准激活识别显著输入通道，通过等价缩放保护其低比特权重重建。 | 主要改权重存储与乘法接口，不解决历史长度；本地 W4 重建 MSE 不代表 TinyChat 端到端吞吐。 |
| [GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](../../../reproductions/2305.13245-gqa/README.md) · [原始来源](https://arxiv.org/abs/2305.13245)<br>章节：背景与主要改动、核心公式、复现边界 | 多个 query heads 共享较少 KV heads，减少每个历史位置的 KV 存储与读取。 | 改变模型表示结构，通常需要适配；token 总数仍会增长。本地从头小训练不同于论文 checkpoint uptraining。 |
| [DropKV: Decoupling Residual-Output Perturbation for Near-Optimal KV-Cache Eviction](../../../foundation-models/2610.22130-drop-kv/README.md) · [原始来源](https://arxiv.org/abs/2610.22130)<br>章节：背景与主要改动、核心公式、代码映射与边界 | 根据删除单项造成的 attention 输出扰动评分，同时考虑概率和 value 差异，保护近期窗口。 | 单项近似并非任意组合的最优驱逐；本地是合成 QKV 与 A100 数值诊断，没有完整 cache 服务集成。 |
| [TwinKV: A Composable Repair Pass for KV Cache Eviction via Pairwise Key Redundancy](../../../reproductions/2608.27128-twinkv/README.md) · [原始来源](https://arxiv.org/abs/2608.27128)<br>章节：背景与主要改动、核心公式、本地复现 | 在既定 eviction 之后，用冗余 donor 与无替代 orphan 成对交换，保持 KV 数不变。 | 依赖 key 相似度及基础策略，不能保证每次 repair 改善；本地 checkpoint 重建负结果不隐去，也非完整生成基准。 |
| [KVMem: Virtualizing Million-Token Agent Workspaces on a Consumer GPU](../../../reproductions/2609.04852-kvmem/README.md) · [原始来源](https://arxiv.org/abs/2609.04852)<br>章节：背景与主要改动、核心公式、复现边界 | 历史 KV 可留在分层 backing store，通过模型注意力空间检索 block，物化原生窗口内执行视图。 | 不等于所有历史同时参加当前 attention；本地 Python 保留完整 backing cache，未实现异步 NVMe 系统且不宣称显存或延迟收益。 |
| [When the KV Cache Is Slower Than the GPU: Scaling Remote KV Tiers for Context-Parallel Prefill](../../../foundation-models/2610.21500-remote-kv-tiers/README.md) · [原始来源](https://arxiv.org/abs/2610.21500)<br>章节：背景与主要改动、核心公式、复现边界 | 先比较远端加载与重新计算，再以 rank 分片和异步加载治理传输与队首阻塞。 | 命中不一定更快，固定开销与带宽决定盈亏；论文端到端对比含布局变化，本地无分布式实现，完整实验高成本。 |
| [ResCom: Activation Residual Compensation for Large Language Model Quantization](../../../foundation-models/2610.35955-rescom/README.md) · [原始来源](https://arxiv.org/abs/2610.35955v1)<br>章节：背景与主要改动、核心公式 | 以中心化残差/输出误差统计白化，再做截断SVD和截距恢复。 | 校准只适用于固定宿主，未实现量化器或原生低比特内核。 |
| [Hilbert Operator for Progressive Encoding (HOPE): A Mathematical Framework for Deconstructing Learned Representations in Deep Networks](../../../foundation-models/2607.21366-hope-hilbert/README.md) · [原始来源](https://arxiv.org/abs/2607.21366v1)<br>章节：背景与主要改动、核心公式 | 以biased Gaussian-ReLU核和Hilbert代理计算剪枝率，支持小Dense层均值补偿与单步恢复。 | 假设激活的Gaussian代理，不实现MERGE/EVICT/完整HOPE或DEFT；与Sleep的Hope架构不是同一方法。 |
| [Folding Attention Biases into Keys Makes Compacted KV Caches Run on Standard Kernels](../../../foundation-models/2610.36520-fold-bias/README.md) · [原始来源](https://arxiv.org/abs/2610.36520v1)<br>章节：背景与主要改动、核心公式、高成本完整实验 | 从上下文query拟合均值投影为1的共享方向，以K+√dβu折叠静态bias；实际bf16舍入后再最小二乘refit V。 | 不像GQA减少KV头，也不负责AM选key/NNLS；不对任意未来query等价，值更换或舍入后不能直接套同值未舍入误差界。 |
| [Multi-layer Indexer: Overlapping Selection and Attention in DeepSeek Sparse Attention](../../../foundation-models/2611.03768-multi-layer-indexer/README.md) · [原始来源](https://arxiv.org/abs/2611.03768)<br>章节：背景与主要改动、核心公式、成本判断与复现边界 | 让当前层消费较早full layer为同一token计算的新selection，将索引器放到侧stream，与主stream的attention、投影和FFN重叠；首次消费时join并保留tensor生命周期。 | 改变依赖与调度，不压缩KV，也不是复用上一token的过期selection。完整路径需8张H200、TP8大模型与SGLang内核，本库仅review，未实现runtime或生成吞吐metrics。 |
| [Turbocharging PiPNN for Proximity and k-NN Graph Building](../../../foundation-models/2611.05690-pipnn-ii/README.md) · [原始来源](https://arxiv.org/abs/2611.05690v1)<br>章节：背景与主要改动、核心公式、结果、负控与边界 | 在近邻图构建的叶内，对已解码的量化候选做有符号点积修正，应用各行尺度后直接更新 top-K，避免物化完整候选分数矩阵。 | 缩小的是图构建的输入表示和中间分数流量，不是 LM 权重、KV 或跨层依赖；本地只做 CPU 分数和排序参考，未实现编码、分区、剪枝或生产 SIMD/Hopper 核。 |
| [GINGER: Spicing Up Graph-Based Vector Search](../../../foundation-models/2611.08306-ginger/README.md) · [原始来源](https://arxiv.org/abs/2611.08306v1)<br>章节：核心公式、数据协议与代码映射 | 在同一已旋转向量的固定 4-bit 高斯粗码上做分区 Lloyd–Max 细化，导航只读粗码及其尺度，重排才加载细码。 | 细位宽独立于导航前缀，换取更准的重排；仍需保留两套尺度，并为入围项读取细位。本地只验证量化与内积，不覆盖图或 SIMD。 |
| [e-means: outperforming k-means (in one-tenth the epochs)](../../../foundation-models/2611.09501-e-means/README.md) · [原始来源](https://arxiv.org/abs/2611.09501v1)<br>章节：核心公式、结果、负控与边界 | 用计数与向量和的小批量 EMA 训练质心，每五批分裂活跃 donor 复苏弱簇，再用末轮历史分配均值收尾。 | 加快的是聚类优化，不是 GINGER 的候选读带宽或 PiPNN II 的构建打分；CPU 固定标签 MSE 不代表 IVF 召回或 GPU 吞吐。 |
| [Spool: Low-Latency Streaming Inference for Hybrid Vision-Language Models](../../../foundation-models/2611.23228-spool/README.md) · [原始来源](https://arxiv.org/abs/2611.23228v1)<br>章节：背景与主要改动、核心公式、同主题比较与边界 | GDN的key/value/gates只依赖已记录的层输入，因此状态更新对旧状态是仿射的。每帧缓存一个变换，以非交换的时间顺序组成segment tree；窗口到期时从prefix anchor重放保留摘要，而非重跑所有视频token。 | DropKV直接挑选attention KV驱逐项，Spool处理递归共享状态的到期重建。后者的固定层输入精确性不能推导为保留视频内容的全网络精确性。 |
| [Communicate the Change: Efficient Expert Parallelism via Activation Compression](../../../foundation-models/2611.22215-echomoe/README.md) · [原始来源](https://arxiv.org/abs/2611.22215v1)<br>章节：背景与主要改动、核心公式、同主题比较与边界 | 每组MoE层先广播参考z，其余层只发送x-a⊙z的压缩code；router仍读取完整x。专家将reference gain和dispatch decoder折入gate/up权重，再将combine compressor折入down权重，避免完整重建或输出物化。 | MoEZip保护路由敏感KV token；EchoMoE压缩专家并行激活通信，两者不是同一缓存，也不能共享“压缩率”作为吞吐对照。 |
| [RISA: Recoverable Sparse Attention for Block-Diffusion Language Models](../../../foundation-models/2611.22191-risa/README.md) · [原始来源](https://arxiv.org/abs/2611.22191v1)<br>章节：背景与主要改动、核心公式、同主题比较与边界 | RISA区分长期HOT/COLD存储优先级和当前denoising block的短期read plan。未读取页面不被删除，后续query可以恢复COLD。seed根据page min/max key摘要评分，保护初始/近期HOT并加入mandatory近期/current行。 | DropKV实际驱逐KV以缩减存储；RISA主要限制每步读取但保留COLD以便恢复。读得少与存得少是不同预算，不能互换显存/延迟结论。 |
| [Beyond Bitwidth: Deployment-Constrained Mixed-Precision Quantization for Multilingual LLM Inference on NVIDIA Blackwell](../../../foundation-models/2611.21974-beyond-bitwidth/README.md) · [原始来源](https://arxiv.org/abs/2611.21974v1)<br>章节：背景与主要改动、核心公式、同主题比较与边界 | 低比特名称不保证GPU真的按该格式执行，也不保证多语种质量。本文用固定诊断/selection/final切分，逐fused-module核对weight类型、activation policy、kernel、fallback和显存，再按服务质量约束配置保护。 | AWQ用calibration activation搜索等价通道缩放后统一做低比特weight-only量化；Beyond Bitwidth研究B200原生format、mixed precision分配及质量/显存/延迟门槛。保护重要通道与给模块分配不同格式不是同一算法，AWQ的小型输出MSE不能充当Blackwell执行证据。 |
| [LoopCache: Accelerating Long-Context Self-Speculative Decoding for Looped Transformers](../../../foundation-models/2611.24301-loopcache-interface/README.md) · [原始来源](https://arxiv.org/abs/2611.24301v1)<br>章节：背景与主要改动、核心公式、同主题比较与边界 | 固定深度的draft可能沿过时轨迹继续推进。LoopCache用新候选相对旧候选的logit差控制替换，并清除依赖旧token的所有后代。推测路径轮转读取同一loop cache，独立KV分支再以正确loop缓存重算；浅层差异较大时才单独读取对应loop的cache。 | Spool重建固定记录层输入下的递归状态；LoopCache安排loop-specific KV读取并以exact分支纠正近似推测。前者的摘要精确性与后者的目标解码精确性证明对象不同。 |
| [FrontierReplay: Split-Free Exact Prefix Caching for Hybrid Language Models](../../../foundation-models/2611.26020-frontier-replay/README.md) · [原始来源](https://arxiv.org/abs/2611.26020v1)<br>章节：背景与主要改动、核心公式、同主题比较与边界 | 混合模型的attention KV可按页复用，但递归状态只在保存过的精确位置恢复。FrontierReplay先根据已观察到的模板稳定尾、已完成turn和分叉点规划检查点；原生prefill不断开，之后只重放短窗递归输入生成精确状态。保留策略优先保护仍在执行的请求锚点和已证明可复用的分叉，而非只看历史频率。 | ReplaySSM主要减少decode/投机时的逐token矩阵状态写回，把输入缓存、output-only读取和接受回滚联动；FrontierReplay主要为下一次prefill的结构边界补造精确检查点，并管理哪些状态值得保留。前者的周期刷新和高低精度anchor不是后者的会话frontier保留策略。本地ReplaySSM已有独立Triton证据，但不能把那份执行回执借给本页的host策略，更不能把两种输入日志视为可互换。 |
| [DuoMI: Dual Mutual Information Regularization for Expert Reuse in Looped Transformers](../../../foundation-models/2611.33952-duomi/README.md) · [原始来源](https://arxiv.org/abs/2611.33952v1)<br>章节：背景与主要改动、核心公式、同主题比较与边界 | DuoMI按相同token在两轮的全部expert软路由计算两种互信息：聚合使用对齐与逐token变化区间，训练时约束共享expert池的实际复用。 | EchoMoE复用跨层激活参考并压缩通信变化量；DuoMI共享expert参数并约束路由。前者的reference不是后者的expert池，减少通信和改变专家复用不是可交换收益；小张量反传不代表语言模型提升。 |
| [DeCo-Attention: Decompose to Compensate for Low-Precision Attention](../../../foundation-models/2611.32035-deco-attention/README.md) · [原始来源](https://arxiv.org/abs/2611.32035v1)<br>章节：背景与主要改动、核心公式、同主题比较与边界 | DeCo在runtime逐head估计主子空间，用Q侧和K侧一阶残差投影构造额外通道，让一个扩展QK点积带入两侧补偿；额外通道同样量化。 | DualQuant仅从静态权重拟合row/column尺度并重缩放激活；DeCo每次attention从Q/K本身估计basis，补偿两边量化残差，不训练静态权重尺度。两者的浮点仿真都不等于packed低位CUDA kernel，更不能以A100浮点执行宣称原生FP4加速。 |

</div>

## 取舍分析 {#analysis}

### 容量下降有四种不同含义

AWQ 让同一权重更省字节；GQA 让每个 token 需要更少 KV heads；DropKV 删除一些历史位置；TwinKV 则在相同位置预算内重新分配保留名额。前两者不自动减少历史长度，后两者也不减少模型权重。若服务主要受长输出 KV 增长限制，单做 AWQ 可能释放一些空间，却未处理增长机制；若瓶颈是权重读取，内容淘汰也未必带来对应收益。

对照来源：[awq](../../../reproductions/2306.00978-awq/README.md) · [gqa](../../../reproductions/2305.13245-gqa/README.md) · [drop-kv](../../../foundation-models/2610.22130-drop-kv/README.md) · [twinkv](../../../reproductions/2608.27128-twinkv/README.md)

### 删掉与移走，决定将来能不能重新访问

DropKV/TwinKV 的当前保留集合会限制可见历史；KVMEM 把大地址空间与小执行视图区分，未选 block 仍可保留在 backing store。Remote KV Tiers 再追问取回来是否比重算便宜，其加载时间含固定开销与数据量除带宽。由此，缓存命中、原始数据仍在、GPU 显存下降和响应变快是不同证据。KVMEM 本地保留完整 backing cache、远端方案未实现的状态都应保持，不能拿逻辑架构替代系统测量。

对照来源：[drop-kv](../../../foundation-models/2610.22130-drop-kv/README.md) · [kvmem](../../../reproductions/2609.04852-kvmem/README.md) · [remote-kv-tiers](../../../foundation-models/2610.21500-remote-kv-tiers/README.md)

### 10月29日：新方法与来源变化

ResCom与HOPE压缩的对象不同：前者在固定量化宿主外增加读取activation rounding residual的低秩校正，校准统计与截距需对应同一宿主；后者用Gaussian-ReLU/Hilbert代理评价神经元结构删除，并补偿下游均值。它们不是一个在任意模型上保证等价的剪枝量化组合；本地都只实现精确小组件，未跑LLM或ImageNet能力矩阵。

对照来源：[awq](../../../reproductions/2306.00978-awq/README.md) · [rescom](../../../foundation-models/2610.35955-rescom/README.md) · [hope-hilbert](../../../foundation-models/2607.21366-hope-hilbert/README.md)

### 能写进标准cache，不等于压缩误差消失

GQA通过共享KV head改变每个token的存储结构；FoldBias保持head维度和query路径，处理的是已有压缩结果多出的静态logit bias。它将bias变成β(q·u)，只在投影接近1的query上近似原偏置，所以兼容标准kernel不意味着任意未来query等价。values须按舍入后的keys拟合，否则拟合与实际内核读入值不一致。AM的key选择、NNLS与engine安装仍是独立环节，本地小矩阵通过不提供吞吐或完整cache质量证据。

对照来源：[fold-bias](../../../foundation-models/2610.36520-fold-bias/README.md) · [gqa](../../../reproductions/2305.13245-gqa/README.md)

### 数据量没变，也可以重排关键依赖

GQA减少每个位置的KV heads，KVMEM决定历史block何时进入执行视图；MLI不以减少KV字节为目标，而是把selection的生产与消费分到不同full layers，让同一token的索引工作和主计算重叠。回退步数按保留索引器的full layers计，不是简单减去物理层号；开头没有前驱的层仍用标准schedule。并发执行还必须在首次消费者等待事件、持有输入和输出直到join，否则逻辑依赖图正确也可能出现读未完成或内存复用。它不是跨token缓存旧selection，单CPU依赖模拟或普通CUDA同步前向也不能证明论文overlap；本库仅收录review，完整高成本实验不复现，无本地运行或吞吐证据。

对照来源：[gqa](../../../reproductions/2305.13245-gqa/README.md) · [kvmem](../../../reproductions/2609.04852-kvmem/README.md) · [multi-layer-indexer](../../../foundation-models/2611.03768-multi-layer-indexer/README.md)

### 减少输入字节、减少中间写回与重叠调度不可混算

AWQ 通过激活感知缩放保护模型权重的低比特表示；PiPNN II 量化的是外部近邻图的数据点，且在每条候选缩放之后直接维护最优 K，去掉完整距离矩阵写回。MLI 则重排同 token 跨层 selection 的关键依赖，未以字节压缩为目标。分别按权重误差、图构建 recall/时间与真实服务流重叠验收；小矩阵和全排序一致只支持 PiPNN 的局部打分语义，不能推出大图召回或 kernel 性能。

对照来源：[awq](../../../reproductions/2306.00978-awq/README.md) · [pipnn-ii](../../../foundation-models/2611.05690-pipnn-ii/README.md) · [multi-layer-indexer](../../../foundation-models/2611.03768-multi-layer-indexer/README.md)

### 分清压缩对象、写回和随机读取

AWQ 改模型权重：由校准激活决定等价缩放，再做低比特重建。PiPNN II 在建图时把量化分数与 top-K 融合，避免写出候选分数矩阵。GINGER 在已有图上做检索，省的是扫描候选时对向量的读带宽。三者分别用权重输出误差、构建时间与图召回、固定召回的查询吞吐验收；合成 NTQ 误差不代替后两类系统数据。

对照来源：[ginger](../../../foundation-models/2611.08306-ginger/README.md) · [pipnn-ii](../../../foundation-models/2611.05690-pipnn-ii/README.md) · [awq](../../../reproductions/2306.00978-awq/README.md)

### Spool：用仿射摘要维护混合 VLM 的滑动窗口

DropKV直接挑选attention KV驱逐项，Spool处理递归共享状态的到期重建。后者的固定层输入精确性不能推导为保留视频内容的全网络精确性。 摘要存D=A-I避免BF16把接近单位矩阵的小变化舍入掉；合并顺序不可交换。逐层、固定记录输入下精确，不等于整个多层网络重新处理剩余帧，因为高层缓存输入可能仍含已到期帧的影响。

对照来源：[spool](../../../foundation-models/2611.23228-spool/README.md) · [drop-kv](../../../foundation-models/2610.22130-drop-kv/README.md)

### EchoMoE：复用跨层参考，只通信压缩变化量

MoEZip保护路由敏感KV token；EchoMoE压缩专家并行激活通信，两者不是同一缓存，也不能共享“压缩率”作为吞吐对照。 相对于压缩后模型，折叠与未折叠线性代数等价；不等于压缩模型无损于原backbone。原文还以projection-weighted重建初始化，再执行KL蒸馏和少量next-token训练。通信公式是张量/路由字节计算，不是测得RDMA流量。

对照来源：[echomoe](../../../foundation-models/2611.22215-echomoe/README.md) · [moezip](../../../foundation-models/2610.30206-moezip/README.md)

### RISA：保留可恢复KV存储，只缓存稀疏读取地址

DropKV实际驱逐KV以缩减存储；RISA主要限制每步读取但保留COLD以便恢复。读得少与存得少是不同预算，不能互换显存/延迟结论。 max在两个完整dot之后进行，不是QUEST的逐坐标上界。后续步只重用地址，用新query/current KV重新计算同一个softmax；不能把history和current分别归一化后平均。精确存储不等于dense-equivalent解码。

对照来源：[risa](../../../foundation-models/2611.22191-risa/README.md) · [drop-kv](../../../foundation-models/2610.22130-drop-kv/README.md)

### 保护量化敏感内容，不等于验证部署格式

实读AWQ的核心是XW=(XS^-1)(SW)，用激活统计搜索缩放以减少量化输出误差；本地未用TinyChat CUDA kernel，MSE不代表端到端吞吐。Beyond Bitwidth按fused module核weight type、activation policy、kernel及fallback，在独立final集合验证服务约束；单模块BF16恢复效应不可相加，最终activation精度与INT8保护共同改变，不能把全部收益归于allocation。原生NVFP4/B200路径也不能由A100上的模拟误差替代。

对照来源：[beyond-bitwidth](../../../foundation-models/2611.21974-beyond-bitwidth/README.md) · [awq](../../../reproductions/2306.00978-awq/README.md)

### LoopCache：循环KV调度与有条件草稿更新接口

Spool重建固定记录层输入下的递归状态；LoopCache安排loop-specific KV读取并以exact分支纠正近似推测。前者的摘要精确性与后者的目标解码精确性证明对象不同。 阈值相等也触发替换；无需未来loop预测来决定当前更新。未来回到旧token的harmful-switch定义只用于分析，不能变成运行时oracle。近似spec cache不能直接提交token，必须等待独立exact分支。

对照来源：[loopcache-interface](../../../foundation-models/2611.24301-loopcache-interface/README.md) · [spool](../../../foundation-models/2611.23228-spool/README.md)

### FrontierReplay: Split-Free Exact Prefix Caching for Hybrid Language Models

ReplaySSM主要减少decode/投机时的逐token矩阵状态写回，把输入缓存、output-only读取和接受回滚联动；FrontierReplay主要为下一次prefill的结构边界补造精确检查点，并管理哪些状态值得保留。前者的周期刷新和高低精度anchor不是后者的会话frontier保留策略。本地ReplaySSM已有独立Triton证据，但不能把那份执行回执借给本页的host策略，更不能把两种输入日志视为可互换。 正文§4.3使用16-token页；native chunk end必须已经16对齐，不能静默向下取整来虚构该位置已有状态。完成turn可按原文取decode已经经过的最后页边界，结构目标仍可向下对齐后请求回放。分叉至少256token，回放窗最多1024token；缺少活锚点/日志页则退化为exact cut。Falcon-H1不在1568token以下保存或恢复状态。§4.4分层为dead=-1、superseded=0、natural=1、未用template/turn=2、proven=3、running=4；两次来自同一request的restore不能晋升proven。只有完成事件后才公开新检查点，失败/未完成状态不能命中；lease保护正在用的锚点。长前缀额外保护稳定尾之前一个prefill预算内、深度至少4096的最深natural检查点。

对照来源：[frontier-replay](../../../foundation-models/2611.26020-frontier-replay/README.md) · [replayssm](../../../reproductions/2610.13778-replayssm/README.md)

### DuoMI: Dual Mutual Information Regularization for Expert Reuse in Looped Transformers

EchoMoE复用跨层激活参考并压缩通信变化量；DuoMI共享expert参数并约束路由。前者的reference不是后者的expert池，减少通信和改变专家复用不是可交换收益；小张量反传不代表语言模型提升。 每组8条序列；先逐group、逐pool计算阈值罚项，再平均。默认tau=1、g_max=.02 bits、D区间[.05,.30] bits、三个权重均.1。D是平均JSD，soft D不是Top-k替换比例；只有均匀硬Top-k分布才有D=1−retention。基础语言、负载均衡与z-loss保持原配置。

对照来源：[duomi](../../../foundation-models/2611.33952-duomi/README.md) · [echomoe](../../../foundation-models/2611.22215-echomoe/README.md)

### DeCo-Attention: Decompose to Compensate for Low-Precision Attention

DualQuant仅从静态权重拟合row/column尺度并重缩放激活；DeCo每次attention从Q/K本身估计basis，补偿两边量化残差，不训练静态权重尺度。两者的浮点仿真都不等于packed低位CUDA kernel，更不能以A100浮点执行宣称原生FP4加速。 Eq6的sample是旋转后尚未量化的Q/K，各Gram独立trace归一化；sample为max(N/256,2r)，混合text/audio/video需分层抽样。Appendix Eq25每组用power-of-two全局scale、每16channel unsigned E4M3 block scale和E2M1值，额外通道不能保持高精度。attention除以原始sqrt(d)，不是扩展维数sqrt(d+2r)。

对照来源：[deco-attention](../../../foundation-models/2611.32035-deco-attention/README.md) · [dualquant](../../../reproductions/2610.13767-dualquant/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### 长对话越跑越占显存，AWQ 与 GQA 各能改变什么，为什么仍可能需要内容选择？ {#cross-weights-versus-history}

??? note "展开答案与例子"

    **答案：** AWQ 降低权重位宽，释放的是模型常驻权重空间；GQA 减少每个历史 token 的 KV heads，降低增长斜率，但 token 数仍继续增加。若还需限制历史总量，可考虑 DropKV 等选择策略，并接受信息遗漏风险。三种收益应分别按权重字节、每 token KV 字节和保留条数记账。

    **教学例子：** 教学例：把书柜本身做薄，不会减少每天新进的书；GQA 像缩小每本书，eviction 才是在固定格数里决定留哪本。

    对照来源：[awq](../../../reproductions/2306.00978-awq/README.md) · [gqa](../../../reproductions/2305.13245-gqa/README.md) · [drop-kv](../../../foundation-models/2610.22130-drop-kv/README.md)

### 两个 KV 都很重要却高度重复时，DropKV 与 TwinKV 会怎样提出不同选择依据？ {#cross-importance-versus-substitution}

??? note "展开答案与例子"

    **答案：** DropKV 用当前观察窗口中的输出扰动估计单项保留价值，value 与 attention 概率都参与；TwinKV 在基础保留结果上检查替代关系，把有 twin 的 donor 换给缺少替代者的 orphan。一个看单项输出影响，一个修集合覆盖，二者可以组合但没有普遍改善保证，交换后仍应检查质量与预算。

    **教学例子：** 教学例：保留了同一计划的两个近重复 token，却删掉唯一授权范围；集合修复可能建议交换，但必须验证 key 相似是否真代表可替代。

    对照来源：[drop-kv](../../../foundation-models/2610.22130-drop-kv/README.md) · [twinkv](../../../reproductions/2608.27128-twinkv/README.md)

### KVMEM 找到旧 KV block 后，为什么 Remote KV Tiers 仍可能建议直接重算？ {#cross-cache-hit-versus-recompute}

??? note "展开答案与例子"

    **答案：** 找到地址只说明数据可复用，加载还要支付固定延迟和传输时间。若远端带宽不足、block 太小或排队严重，T0 加数据量除带宽可能超过重新 prefill 的时间。KVMEM 的执行视图预算解决可见范围，远端盈亏模型解决获取方式，不能仅按命中率决定两者优劣。

    **教学例子：** 教学例：一个很短的旧前缀虽命中远端，但建立请求就耗很久；在本机重新计算可能更快，长前缀才摊薄固定成本。

    对照来源：[kvmem](../../../reproductions/2609.04852-kvmem/README.md) · [remote-kv-tiers](../../../foundation-models/2610.21500-remote-kv-tiers/README.md)

### 为什么ResCom的校正rank预算不能直接当作HOPE的可删神经元数？ {#cross-oct29-method-boundary}

??? note "展开答案与例子"

    **答案：** ResCom预算控制的是输出误差补偿分支的低秩容量，HOPE的候选成本还依赖神经元Hilbert容量与初始参数footprint。它们的参数位置、状态和校准假设不同，不能互换预算单位。

    **教学例子：** 教学例：保留一层的全部量化输出并加rank2校正，与删掉两个神经元再补下游均值，不是同一前向网络。

    对照来源：[awq](../../../reproductions/2306.00978-awq/README.md) · [rescom](../../../foundation-models/2610.35955-rescom/README.md) · [hope-hilbert](../../../foundation-models/2607.21366-hope-hilbert/README.md)

### FoldBias保持head维度且可接标准kernel，为什么还必须测未来query质量？ {#cross-fold-bias-compatibility-not-universal-equivalence}

??? note "展开答案与例子"

    **答案：** 折叠后的偏置是β(q·u)，并非对所有query恒等于β。上下文上拟合μ·u=1只约束该分布的平均投影，未来query可漂移。GQA减少KV头与这种bias近似也不是同一压缩对象；接口兼容、内存和质量需分别验收。

    **教学例子：** 教学示意：拟合query满足q·u≈1，后续query却为0.6，则原bias只剩约六成；即使张量shape完全能被kernel读取，attention仍已变化。

    对照来源：[fold-bias](../../../foundation-models/2610.36520-fold-bias/README.md) · [gqa](../../../reproductions/2305.13245-gqa/README.md)

### MLI读较早层的selection，为什么不等于KVMEM取回旧block，也不等于复用上一生成token的选择？ {#cross-nov04b-overlap-not-kv-compression}

??? note "展开答案与例子"

    **答案：** MLI移动的是同一token内selection的消费层，选择仍由该token的索引器新计算，跨full layer产生可重叠窗口；KVMEM决定历史KV block如何检索并物化到有限执行视图。旧token的selection可能已不适合当前query，不能用跨token复用替代MLI。是否真正重叠还需事件等待、张量生命周期和真实服务内核，本库对此仅review，不用CPU模拟宣称已实现。

    **教学例子：** 教学例：让当前层读较早full layer刚为当前token算出的top-k，是依赖调度；直接拿上一个生成token留下的top-k，则改变了选择的新鲜度。两种复用看起来相似，并不代表是同一个算法。

    对照来源：[multi-layer-indexer](../../../foundation-models/2611.03768-multi-layer-indexer/README.md) · [kvmem](../../../reproductions/2609.04852-kvmem/README.md)

### PiPNN II 和 MLI 都把步骤靠得更近，为什么不能用同一种“省中间张量”来解释？ {#cross-nov06-score-fusion-versus-scheduling}

??? note "展开答案与例子"

    **答案：** PiPNN II 在同一条候选上执行打分和 top-K 更新，避免先物化所有距离，且必须先应用各行尺度。MLI 仍要计算新 selection；让较后 full layer 消费此前结果，从而能并行做同 token 的索引和主计算。一个改变物化，另一个改变依赖和重叠，不能用一次 CPU 全排序比对证明 GPU 重叠。

    **教学例子：** 教学例：100 行只留 3 个距离，检验的是没有全表写回且结果相同；两条 CUDA stream 能否同时推进，需另测事件和首次消费者。

    对照来源：[pipnn-ii](../../../foundation-models/2611.05690-pipnn-ii/README.md) · [multi-layer-indexer](../../../foundation-models/2611.03768-multi-layer-indexer/README.md)

### 如果 NTQ 每个候选少读几字节，能直接推出 PiPNN II 建图会更快或 GINGER 的生产 QPS 会提高吗？ {#cross-ginger-versus-pipnn-evidence}

??? note "展开答案与例子"

    **答案：** 不能。PiPNN II 的融合打分在构建路径，NTQ 拆流在检索路径；实际查询还受图邻接、重排候选数和硬件缓存影响，必须在固定召回下计时。局部字节数不包括尺度和图索引，更不是系统内存。

    **教学例子：** 31 维 CPU 例子里，导航读 16 个粗码字节，只有入围项多读 8 个细码字节。它不能说明完整图的总读取量或构建耗时。

    对照来源：[ginger](../../../foundation-models/2611.08306-ginger/README.md) · [pipnn-ii](../../../foundation-models/2611.05690-pipnn-ii/README.md)

### Spool的精确与DropKV的近似驱逐有何不同？ {#cross-nov18-spool}

??? note "展开答案与例子"

    **答案：** Spool精确重放固定记录层输入的状态变换；DropKV估计删除KV对attention输出的扰动。Spool也不保证整个多层网络重算等价。

    **教学例子：** 高层某帧特征已受旧帧影响，删除低层旧帧摘要不会改写那份缓存特征。

    对照来源：[spool](../../../foundation-models/2611.23228-spool/README.md) · [drop-kv](../../../foundation-models/2610.22130-drop-kv/README.md)

### 与MoEZip的routing-aware压缩能直接比压缩率吗？ {#cross-nov18-echomoe}

??? note "展开答案与例子"

    **答案：** 不能。MoEZip选择attention KV行，EchoMoE发送低维专家激活，分母、额外参考成本和质量误差都不同。

    **教学例子：** 少存50%KV不等于少发50%RDMA字节。

    对照来源：[echomoe](../../../foundation-models/2611.22215-echomoe/README.md) · [moezip](../../../foundation-models/2610.30206-moezip/README.md)

### 与DropKV的驱逐是同一预算吗？ {#cross-nov18-risa}

??? note "展开答案与例子"

    **答案：** 不是。DropKV删除存储条目，RISA保留未选COLD并减少循环读取；RISA的HOT cap还不包含protected、COLD和mandatory部分。

    **教学例子：** 512页cap并不意味着总共只读取或保存512页。

    对照来源：[risa](../../../foundation-models/2611.22191-risa/README.md) · [drop-kv](../../../foundation-models/2610.22130-drop-kv/README.md)

### AWQ输出误差更小，是否已经满足Beyond Bitwidth的部署门槛？ {#cross-nov18-beyond-bitwidth}

??? note "展开答案与例子"

    **答案：** 没有。AWQ等价缩放的局部MSE只检验量化近似，部署门槛还要求真实packed格式、activation policy、无fallback、显存/延迟与独立服务质量评测。

    **教学例子：** 教学例：一层W4输出MSE降低，不说明整个8B模型在B200按目标格式执行，也不说明韩语保留率过门槛。

    对照来源：[beyond-bitwidth](../../../foundation-models/2611.21974-beyond-bitwidth/README.md) · [awq](../../../reproductions/2306.00978-awq/README.md)

### 与Spool的精确状态重建是同一个承诺吗？ {#cross-nov19-loopcache-interface}

??? note "展开答案与例子"

    **答案：** 不是。Spool对固定记录输入重放状态变换；LoopCache的lossless token提交还依赖完整正确loop KV分支。

    **教学例子：** 教学例：调度编号正确不意味着已运行目标模型验证。

    对照来源：[loopcache-interface](../../../foundation-models/2611.24301-loopcache-interface/README.md) · [spool](../../../foundation-models/2611.23228-spool/README.md)

### FrontierReplay和ReplaySSM都记录输入，解决的是同一个问题吗？ {#cross-nov21-frontier-replay}

??? note "展开答案与例子"

    **答案：** 不是。ReplaySSM围绕decode状态写回、output-only和投机回滚；FrontierReplay围绕prefill结构边界的检查点产生与保留。相似代数不代表服务策略、精度或证据可直接共用。

    **教学例子：** 教学例：16步decode刷新正确，不能证明下一会话的模板边界已保存、仍驻留且可命中。

    对照来源：[frontier-replay](../../../foundation-models/2611.26020-frontier-replay/README.md) · [replayssm](../../../reproductions/2610.13778-replayssm/README.md)

### DuoMI和EchoMoE里的跨层复用是同一种东西吗？ {#cross-nov26-duomi}

??? note "展开答案与例子"

    **答案：** 不是。DuoMI约束共享FFN池的router选择；EchoMoE复用激活reference并压缩差值通信。

    **教学例子：** 教学例：同一个expert可被两轮选择，但两轮激活差值仍很大；专家复用率不能替代通信字节测量。

    对照来源：[duomi](../../../foundation-models/2611.33952-duomi/README.md) · [echomoe](../../../foundation-models/2611.22215-echomoe/README.md)

### DeCo能直接替换DualQuant的权重尺度求解器吗？ {#cross-nov27-deco-attention}

??? note "展开答案与例子"

    **答案：** 不能。DualQuant优化静态weight重建的row/column尺度，DeCo纠正动态attention Q/K残差；对象和运行时机不同。

    **教学例子：** 教学例：两个prompt产生不同Q/K，DeCo需重估basis；静态weight尺度通常可复用。

    对照来源：[deco-attention](../../../foundation-models/2611.32035-deco-attention/README.md) · [dualquant](../../../reproductions/2610.13767-dualquant/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-11-27** · DualQuant仅从静态权重拟合row/column尺度并重缩放激活；DeCo每次attention从Q/K本身估计basis，补偿两边量化残差，不训练静态权重尺度。两者的浮点仿真都不等于packed低位CUDA kernel，更不能以A100浮点执行宣称原生FP4加速。 本轮为Nov24补漏CPU L1，完整实验高成本终态。

涉及：[deco-attention](../../../foundation-models/2611.32035-deco-attention/README.md) · [dualquant](../../../reproductions/2610.13767-dualquant/README.md)

**2026-11-26** · EchoMoE复用跨层激活参考并压缩通信变化量；DuoMI共享expert参数并约束路由。前者的reference不是后者的expert池，减少通信和改变专家复用不是可交换收益；小张量反传不代表语言模型提升。 完整矩阵高成本终态，不以L1或审查充当能力证据。

涉及：[duomi](../../../foundation-models/2611.33952-duomi/README.md) · [echomoe](../../../foundation-models/2611.22215-echomoe/README.md)

**2026-11-21** · ReplaySSM主要减少decode/投机时的逐token矩阵状态写回，把输入缓存、output-only读取和接受回滚联动；FrontierReplay主要为下一次prefill的结构边界补造精确检查点，并管理哪些状态值得保留。前者的周期刷新和高低精度anchor不是后者的会话frontier保留策略。本地ReplaySSM已有独立Triton证据，但不能把那份执行回执借给本页的host策略，更不能把两种输入日志视为可互换。 本地组件证据与完整实验不复现分开记录。

涉及：[frontier-replay](../../../foundation-models/2611.26020-frontier-replay/README.md) · [replayssm](../../../reproductions/2610.13778-replayssm/README.md)

**2026-11-19** · Spool重建固定记录层输入下的递归状态；LoopCache安排loop-specific KV读取并以exact分支纠正近似推测。前者的摘要精确性与后者的目标解码精确性证明对象不同。 本地组件合同和高成本不复现分别记录。

涉及：[loopcache-interface](../../../foundation-models/2611.24301-loopcache-interface/README.md) · [spool](../../../foundation-models/2611.23228-spool/README.md)

**2026-11-18** · AWQ用calibration activation搜索等价通道缩放后统一做低比特weight-only量化；Beyond Bitwidth研究B200原生format、mixed precision分配及质量/显存/延迟门槛。保护重要通道与给模块分配不同格式不是同一算法，AWQ的小型输出MSE不能充当Blackwell执行证据。 本次实读已有同主题代表README，按真实研究轴比较，不借比较对象改变算法或宣称跨论文效果复现。

涉及：[beyond-bitwidth](../../../foundation-models/2611.21974-beyond-bitwidth/README.md) · [awq](../../../reproductions/2306.00978-awq/README.md)

**2026-11-18** · DropKV实际驱逐KV以缩减存储；RISA主要限制每步读取但保留COLD以便恢复。读得少与存得少是不同预算，不能互换显存/延迟结论。 本地边界与完整高成本不复现分别记录。

涉及：[risa](../../../foundation-models/2611.22191-risa/README.md) · [drop-kv](../../../foundation-models/2610.22130-drop-kv/README.md)

**2026-11-18** · MoEZip保护路由敏感KV token；EchoMoE压缩专家并行激活通信，两者不是同一缓存，也不能共享“压缩率”作为吞吐对照。 本地边界与完整高成本不复现分别记录。

涉及：[echomoe](../../../foundation-models/2611.22215-echomoe/README.md) · [moezip](../../../foundation-models/2610.30206-moezip/README.md)

**2026-11-18** · DropKV直接挑选attention KV驱逐项，Spool处理递归共享状态的到期重建。后者的固定层输入精确性不能推导为保留视频内容的全网络精确性。 本地边界与完整高成本不复现分别记录。

涉及：[spool](../../../foundation-models/2611.23228-spool/README.md) · [drop-kv](../../../foundation-models/2610.22130-drop-kv/README.md)

**2026-11-09** · 加入 e-means，对比质心训练、图构建与查询读带宽三个阶段。末轮固定分配均值能减小相应训练目标，不保证留出误差或检索性能都改善。

涉及：[e-means](../../../foundation-models/2611.09501-e-means/README.md)

**2026-11-07** · 加入 GINGER 嵌套 TurboQuant，与 AWQ 和 PiPNN II 对照权重压缩、建图写回和查询读取；核对 GINGER 指向的 PiPNN II 官方仓库仍是占位，未更改此前本地证据。

涉及：[ginger](../../../foundation-models/2611.08306-ginger/README.md) · [pipnn-ii](../../../foundation-models/2611.05690-pipnn-ii/README.md) · [awq](../../../reproductions/2306.00978-awq/README.md)

**2026-11-06** · 增加 PiPNN II，与 AWQ、MLI 比较输入位宽、中间分数写回与关键路径；注明候选缩放后排序及本地 CPU 语义参考不代表完整图构建性能。

涉及：[pipnn-ii](../../../foundation-models/2611.05690-pipnn-ii/README.md)

**2026-11-04** · 收录MLI并与GQA、KVMEM对照：它重排同token跨full layer的selection依赖，不压缩KV、不复用旧token选择。注明事件和张量生命周期条件；完整8H200实验成本过高不复现，本库仅review、无runtime或吞吐指标。

涉及：[multi-layer-indexer](../../../foundation-models/2611.03768-multi-layer-indexer/README.md)

**2026-10-30** · 精读FoldBias的约束方向、rank-one位移、bf16先于value refit与同值误差界；相对GQA明确接口兼容与压缩结构的不同，保留未来query漂移风险。

涉及：[fold-bias](../../../foundation-models/2610.36520-fold-bias/README.md) · [gqa](../../../reproductions/2305.13245-gqa/README.md)

**2026-10-29** · ResCom与HOPE压缩的对象不同：前者在固定量化宿主外增加读取activation rounding residual的低秩校正，校准统计与截距需对应同一宿主；后者用Gaussian-ReLU/Hilbert代理评价神经元结构删除，并补偿下游均值。它们不是一个在任意模型上保证等价的剪枝量化组合；本地都只实现精确小组件，未跑LLM或ImageNet能力矩阵。

涉及：[rescom](../../../foundation-models/2610.35955-rescom/README.md) · [hope-hilbert](../../../foundation-models/2607.21366-hope-hilbert/README.md)

**2026-10-27** · 首版：比较低比特权重、共享KV头、扰动驱逐、等预算修复、历史执行视图与远端加载，分开容量、恢复和时延证据。

覆盖 29 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 44 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [AgentKV: Phase-Aware KV Eviction for Agentic LLMs](../../../foundation-models/2609.14872-agentkv/README.md)
- [AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration](../../../reproductions/2306.00978-awq/README.md)
- [BaKron: Efficient Quantization with Kronecker-Factored Hessians](../../../reproductions/2608.06291-bakron/README.md)
- [BeaconKV: Key-Value Cache Compression Guided by Beacon Queries for Efficient Large Reasoning Model Inference](../../../reproductions/2609.04971-beaconkv/README.md)
- [C²KV: Compressed and Composable KV Cache Reuse for Efficient LLM Inference](../../../reproductions/2607.17715-c2kv/README.md)
- [DistillCache: KL-Guided Adaptive KV-Cache Eviction for Memory-Efficient LLM Inference](../../../reproductions/2608.08878-distillcache/README.md)
- [DropKV: Decoupling Residual-Output Perturbation for Near-Optimal KV-Cache Eviction](../../../foundation-models/2610.22130-drop-kv/README.md)
- [DualQuant: Dual-scale Calibration-free Weight-and-Activation Quantization for LLMs](../../../reproductions/2610.13767-dualquant/README.md)
- [FLINT: Fixed-budget Late Interaction](../../../foundation-models/2610.27273-flint/README.md)
- [Fractional Power-of-Two Quantization for Efficient and Effective Multiplier-Free LLM Inference](../../../foundation-models/2610.21257-fpot/README.md)
- [GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](../../../reproductions/2305.13245-gqa/README.md)
- [IrekoGPT: Turning Structured Pruning into Post-Hoc Slimmable LLMs](../../../foundation-models/2610.00426-irekogpt/README.md)
- [KVMem: Virtualizing Million-Token Agent Workspaces on a Consumer GPU](../../../reproductions/2609.04852-kvmem/README.md)
- [LeapQuant: Efficient Linear Attention with Accurate Recurrent State Quantization](../../../foundation-models/2609.38166-leapquant/README.md)
- [MoEZip: Routing-Aware KV Cache Compression for Sparse Mixture-of-Experts LLMs](../../../foundation-models/2610.30206-moezip/README.md)
- [PN-Mix: Pair-Norm Guided Mixed-Precision Key Cache Quantization for Efficient Long-Output LLM Inference](../../../reproductions/2610.19605-pn-mix/README.md)
- [QEvict: Recoverable Quantized KV Eviction for Attention-Drift-Robust Long-Context Decoding](../../../reproductions/2608.05326-qevict/README.md)
- [RACE: RoPE-Aligned Attention Compression Based on Query-Key Activation Energies](../../../foundation-models/2610.28385-race-rope-compression/README.md)
- [Random Attention: Rethinking KV Cache Eviction for Efficient Reasoning](../../../reproductions/2609.03430-random-attention/README.md)
- [When the KV Cache Is Slower Than the GPU: Scaling Remote KV Tiers for Context-Parallel Prefill](../../../foundation-models/2610.21500-remote-kv-tiers/README.md)
- [ReplaySSM: Cache SSM Inputs, Not State](../../../reproductions/2610.13778-replayssm/README.md)
- [Right On Q: Recovering Reasoning under Quantization via Self-Generated Trajectories](../../../foundation-models/2610.29378-right-on-q/README.md)
- [RoleQ: Role-Aligned Scales for Converting Language Models to Ternary](../../../foundation-models/2610.21808-roleq/README.md)
- [Compression Does Not End at Selection: Post-Selection Positional Geometry for Sparse KV Caches](../../../foundation-models/2610.21126-rope-relay/README.md)
- [SPLASH: Switching Parallel Layouts of Attention with Seamless Handoff for LLM Serving](../../../foundation-models/2609.37626-splash/README.md)
- [STEPQuant: When and Where Errors Matter in Delta-Rule Recurrent State Quantization](../../../foundation-models/2609.38169-stepquant/README.md)
- [TaskPress: Query-Agnostic KV Cache Compression via Task-Guided Pruning](../../../foundation-models/2608.03276-taskpress/README.md)
- [TwinKV: A Composable Repair Pass for KV Cache Eviction via Pairwise Key Redundancy](../../../reproductions/2608.27128-twinkv/README.md)
- [VFold: Symmetry-Aware Cross-Layer Value Cache Compression](../../../foundation-models/2610.12338-vfold/README.md)
- [ResCom: Activation Residual Compensation for Large Language Model Quantization](../../../foundation-models/2610.35955-rescom/README.md)
- [Hilbert Operator for Progressive Encoding (HOPE): A Mathematical Framework for Deconstructing Learned Representations in Deep Networks](../../../foundation-models/2607.21366-hope-hilbert/README.md)
- [Folding Attention Biases into Keys Makes Compacted KV Caches Run on Standard Kernels](../../../foundation-models/2610.36520-fold-bias/README.md)
- [Multi-layer Indexer: Overlapping Selection and Attention in DeepSeek Sparse Attention](../../../foundation-models/2611.03768-multi-layer-indexer/README.md)
- [Turbocharging PiPNN for Proximity and k-NN Graph Building](../../../foundation-models/2611.05690-pipnn-ii/README.md)
- [GINGER: Spicing Up Graph-Based Vector Search](../../../foundation-models/2611.08306-ginger/README.md)
- [e-means: outperforming k-means (in one-tenth the epochs)](../../../foundation-models/2611.09501-e-means/README.md)
- [Spool: Low-Latency Streaming Inference for Hybrid Vision-Language Models](../../../foundation-models/2611.23228-spool/README.md)
- [Communicate the Change: Efficient Expert Parallelism via Activation Compression](../../../foundation-models/2611.22215-echomoe/README.md)
- [RISA: Recoverable Sparse Attention for Block-Diffusion Language Models](../../../foundation-models/2611.22191-risa/README.md)
- [Beyond Bitwidth: Deployment-Constrained Mixed-Precision Quantization for Multilingual LLM Inference on NVIDIA Blackwell](../../../foundation-models/2611.21974-beyond-bitwidth/README.md)
- [LoopCache: Accelerating Long-Context Self-Speculative Decoding for Looped Transformers](../../../foundation-models/2611.24301-loopcache-interface/README.md)
- [FrontierReplay: Split-Free Exact Prefix Caching for Hybrid Language Models](../../../foundation-models/2611.26020-frontier-replay/README.md)
- [DuoMI: Dual Mutual Information Regularization for Expert Reuse in Looped Transformers](../../../foundation-models/2611.33952-duomi/README.md)
- [DeCo-Attention: Decompose to Compensate for Low-Precision Attention](../../../foundation-models/2611.32035-deco-attention/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/foundation-models/compression-and-cache.md) · [返回全部精读卡片](../index.md)
