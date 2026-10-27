---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 推理压缩先找瓶颈：权重、KV 内容与缓存层级

[基础模型](../index.md) · 更新 2026-10-27 · 29 篇主题资料 / 6 篇重点对照

AWQ 减权重位宽，GQA 减 KV 头，DropKV 与 TwinKV 改保留内容，KVMEM 管可执行历史视图，Remote KV Tiers 解决跨层级加载。它们可以组合，但不能用一个“压缩率”解释质量、可恢复性和端到端速度。

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

</div>

## 取舍分析 {#analysis}

### 容量下降有四种不同含义

AWQ 让同一权重更省字节；GQA 让每个 token 需要更少 KV heads；DropKV 删除一些历史位置；TwinKV 则在相同位置预算内重新分配保留名额。前两者不自动减少历史长度，后两者也不减少模型权重。若服务主要受长输出 KV 增长限制，单做 AWQ 可能释放一些空间，却未处理增长机制；若瓶颈是权重读取，内容淘汰也未必带来对应收益。

对照来源：[awq](../../../reproductions/2306.00978-awq/README.md) · [gqa](../../../reproductions/2305.13245-gqa/README.md) · [drop-kv](../../../foundation-models/2610.22130-drop-kv/README.md) · [twinkv](../../../reproductions/2608.27128-twinkv/README.md)

### 删掉与移走，决定将来能不能重新访问

DropKV/TwinKV 的当前保留集合会限制可见历史；KVMEM 把大地址空间与小执行视图区分，未选 block 仍可保留在 backing store。Remote KV Tiers 再追问取回来是否比重算便宜，其加载时间含固定开销与数据量除带宽。由此，缓存命中、原始数据仍在、GPU 显存下降和响应变快是不同证据。KVMEM 本地保留完整 backing cache、远端方案未实现的状态都应保持，不能拿逻辑架构替代系统测量。

对照来源：[drop-kv](../../../foundation-models/2610.22130-drop-kv/README.md) · [kvmem](../../../reproductions/2609.04852-kvmem/README.md) · [remote-kv-tiers](../../../foundation-models/2610.21500-remote-kv-tiers/README.md)

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

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-27** · 首版：比较低比特权重、共享KV头、扰动驱逐、等预算修复、历史执行视图与远端加载，分开容量、恢复和时延证据。

覆盖 29 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 29 篇资料</summary>

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

</details>

[进入本主题逐篇四层问答](../../paths/foundation-models/compression-and-cache.md) · [返回全部精读卡片](../index.md)
