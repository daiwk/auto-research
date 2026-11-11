---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 少做串行步骤：验证草稿与学习迭代不是同一条路

[基础模型](../index.md) · 更新 2026-11-11 · 16 篇主题资料 / 7 篇重点对照

推测解码用便宜提案换昂贵验证批次，精确校正可保持原 target 分布；扩散语言和数据空间迭代则改变生成轨迹或训练目标。比较时先问谁决定最终分布，再问每步做什么、跨步保留什么，以及 NFE 或接受长度能否转成真实时间收益。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/foundation-models/generation-paths.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：最终分布由原target验证还是由新训练目标决定 · 提案来自独立draft、多未来头或去噪状态 · 跨步骤共享的是KV、hidden carry还是固定噪声 · 成本看验证接受长度、网络前向数还是完整墙钟

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [Fast Inference from Transformers via Speculative Decoding](../../../reproductions/2211.17192-speculative-decoding/README.md) · [原始来源](https://arxiv.org/abs/2211.17192)<br>章节：背景与主要改动、核心公式、复现边界 | draft 提出 token，target 批量验证，拒绝时按残差分布校正以保持 target 分布。 | 加速取决于提案成本与接受长度；本地 Markov LM 调用数不是大模型 GPU 延迟。 |
| [Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](../../../reproductions/2401.10774-medusa/README.md) · [原始来源](https://arxiv.org/abs/2401.10774)<br>章节：背景与主要改动、核心公式、复现边界 | 在同一 backbone 上训练多个 future-token heads，构建候选树并集中验证。 | 减少独立 draft 部署负担，却需训练未来头和树验证；不能把“多头并行”本身当成任意采样规则的精确分布证明。 |
| [Windowed-MTP: Removing the Full-Context Draft-KV Tax at Million-Token Context](../../../reproductions/2607.21535-windowed-mtp/README.md) · [原始来源](https://arxiv.org/abs/2607.21535)<br>章节：背景与主要改动、核心公式、复现边界 | 只把 draft 的读取限制为 sink 与近期窗口，target 保持全历史及原验证规则。 | draft 便宜可能同时降低接受率；本地小模型一致性与 MPS 测量不代表百万上下文 B200 服务。 |
| [dQwen3.5: Adapting Hybrid Language Models into Bidirectional Diffusion Language Models](../../../foundation-models/2609.20751-dqwen35/README.md) · [原始来源](https://arxiv.org/abs/2609.20751)<br>章节：背景与主要改动、复现边界 | 把混合 attention/RNN 骨干改成双向传播，用掩码去噪训练为 diffusion LM。 | 改变条件结构与生成目标，需要重新训练；本地双向 kernel 诊断未加载原 9B 模型，不能当成无损 AR 加速。 |
| [On Trajectory-Aware Training for Masked Diffusion Language Models](../../../foundation-models/2609.37974-pumba/README.md) · [原始来源](https://arxiv.org/abs/2609.37974)<br>章节：背景与主要改动、核心公式、复现边界 | 沿自身 progressive-unmasking 轨迹展开连续步骤，carry 在窗口内传递并接受 BPTT。 | 训练窗口与截断控制计算和信用范围；本地只验 carry 梯度，不是 LLaDA-8B 少步能力复现。 |
| [Few-Step Generation via Data-Space Iteration](../../../foundation-models/2610.12102-data-space-iteration/README.md) · [原始来源](https://arxiv.org/abs/2610.12102)<br>章节：背景与主要改动、核心公式、复现边界与 Evolve | 固定一份噪声，在数据预测空间反复精炼；仅当前 refinement 建生成器梯度，teacher/fake 给蒸馏方向。 | 步号不是 flow time，且目标不与语言模型相同；本地缩小图像模型三seed有正有负，像素特征距离不是 Inception FID。 |
| [Blurring the Block Boundaries: Overlapping Block Denoising for Efficient Diffusion Language Models](../../../foundation-models/2611.14387-b3/README.md) · [原始来源](https://arxiv.org/abs/2611.14387v1)<br>章节：核心公式、数据协议与代码映射、结果与复现边界 | 在兼容self-editing的扩散解码中重叠当前/未来两块，以块因果mask保护当前输出；用上一拍前沿左侧熵的跨块候选均值控制spawn。 | 门控不是扩散backbone，不能把AR模型直接变双向DLM；候选排除frontier、future-active阶段与EOS，并保留一拍滞后。局部注意力不变不证明整段分布不变、质量或TPS。 |

</div>

## 取舍分析 {#analysis}

### 并行提案不等于改写目标分布

精确 speculative decoding 允许 draft 很不完美，因为 target 验证与残差校正负责最终分布；Windowed-MTP 因此可以只压 draft 上下文，把风险主要转为接受率与速度。Medusa 把提案放进 backbone 的多个未来头，仍要具体看验证和采样方式，不能仅凭树形并行宣称无损。核心边界是验证器的历史与规则是否保持，而非 draft 是否看到了全部信息。

对照来源：[speculative-decoding](../../../reproductions/2211.17192-speculative-decoding/README.md) · [windowed-mtp](../../../reproductions/2607.21535-windowed-mtp/README.md) · [medusa](../../../reproductions/2401.10774-medusa/README.md)

### 同样是多步，步之间的依赖不同

DQwen3.5 的步围绕掩码去噪，PUMBA 进一步让前一步 carry 对后续 loss 负责；Data-Space Iteration 的步则是在固定噪声下精炼数据预测，前缀 rollout 不建梯度。这些步骤不能按一个通用“迭代次数”直接比较，语言与图像任务的质量指标也不同。需要分别写清状态、条件与梯度跨越范围，再报告对应训练和推理成本。

对照来源：[dqwen35](../../../foundation-models/2609.20751-dqwen35/README.md) · [pumba](../../../foundation-models/2609.37974-pumba/README.md) · [data-space-iteration](../../../foundation-models/2610.12102-data-space-iteration/README.md)

### 改变模型的生成条件，与安排已有解码器何时工作是两层改动

dQwen3.5把混合attention/RNN骨干改成双向条件并用掩码去噪训练；B3在已有兼容扩散模型上安排两块重叠时机，不提供该模型本身。B3的块因果mask只保护当前块不读取未来草稿，不意味着未来块无需self-edit，也不是推测解码那种完整目标分布保持证明。应分别验收backbone、sampler与门控。

对照来源：[b3](../../../foundation-models/2611.14387-b3/README.md) · [dqwen35](../../../foundation-models/2609.20751-dqwen35/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### Windowed-MTP 缩小 draft 窗口，为什么与直接缩小 target 窗口不是同一种质量承诺？ {#cross-draft-window-versus-target-window}

??? note "展开答案与例子"

    **答案：** 精确推测解码允许 draft 分布变化，只要 target 仍在原历史上验证并采用正确校正，最终仍由原 target 分布决定。若连 target 窗口也缩小，条件分布本身已经改变，就不能沿用同一承诺。代价上，draft 越便宜未必越快，因为接受长度可能下降，需要把两侧成本一起除以实际接受量。

    **教学例子：** 教学例：草稿忘了早期人名，target 可拒绝并纠正；若 target 也看不到该人名，验证就不再是原完整历史下的模型。

    对照来源：[windowed-mtp](../../../reproductions/2607.21535-windowed-mtp/README.md) · [speculative-decoding](../../../reproductions/2211.17192-speculative-decoding/README.md)

### Medusa 同时提议多个未来 token，与 DQwen3.5 多位置去噪，为什么不能直接视为同一种并行生成？ {#cross-future-heads-versus-denoising}

??? note "展开答案与例子"

    **答案：** Medusa 的未来头形成候选，backbone 验证决定接收哪些分支；DQwen3.5 则把混合骨干训练成双向掩码去噪模型，条件和训练目标都改变。前者主要重组原生成流程，后者学习新的生成过程。比较时需分别说明采样规则、训练投入和质量口径，不能用并行位置数推断输出分布等价。

    **教学例子：** 教学例：一次提出三个字后逐项核验，与一次填写多个空位后继续去噪，可能都有并行计算，却依赖不同上下文和接受机制。

    对照来源：[medusa](../../../reproductions/2401.10774-medusa/README.md) · [dqwen35](../../../foundation-models/2609.20751-dqwen35/README.md)

### PUMBA 与 Data-Space Iteration 都复用前一步结果，为什么训练梯度不能用同一规则处理？ {#cross-carry-gradient-versus-prefix-stopgrad}

??? note "展开答案与例子"

    **答案：** PUMBA 特意让窗口内梯度穿过 carry，使早期步骤学会为后续服务；Data-Space Iteration 对选定 refinement 的前缀 rollout 停止建图，只更新当前生成步骤，并冻结 teacher/fake 的生成器侧梯度。复用状态不自动规定可反传范围，混用会改变目标、内存成本和训练算法。

    **教学例子：** 教学例：把 PUMBA 每步 carry 全部 detach 会切断它要学的跨步信用；让数据空间前缀全部反传，也不再是已声明训练配方。

    对照来源：[pumba](../../../foundation-models/2609.37974-pumba/README.md) · [data-space-iteration](../../../foundation-models/2610.12102-data-space-iteration/README.md)

### 给普通AR模型加B3的spawn gate，是否就得到了扩散语言模型？ {#cross-spawn-gate-not-diffusion-backbone}

??? note "展开答案与例子"

    **答案：** 没有。gate仅决定兼容扩散解码器何时开启未来块；还需要双向/块条件结构、去噪与self-editing sampler。dQwen3.5的模型改造和掩码训练属于另一层，不能由门控替代。

    **教学例子：** 教学例：CPU门控输入低熵并返回True，只是许可状态；它既没有预测下一个token，也不能把固定因果AR权重改成可以编辑未来块的模型。

    对照来源：[b3](../../../foundation-models/2611.14387-b3/README.md) · [dqwen35](../../../foundation-models/2609.20751-dqwen35/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-11-11** · 加入B3，区分扩散backbone改造与已有解码器的重叠调度；核对前沿、一拍滞后、活动未来块及EOS保护。CPU门控不冒充DLM生成，完整16B/26B/100B吞吐矩阵不复现。

涉及：[b3](../../../foundation-models/2611.14387-b3/README.md) · [dqwen35](../../../foundation-models/2609.20751-dqwen35/README.md)

**2026-10-27** · 首版：比较精确草稿验证、多未来头、窗口draft、扩散语言与数据空间精炼，区分分布承诺、跨步状态和梯度范围。

覆盖 15 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 16 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [ASPIRE: Asynchronous Batch Self-Speculative Decoding](../../../foundation-models/2609.17943-aspire/README.md)
- [Few-Step Generation via Data-Space Iteration](../../../foundation-models/2610.12102-data-space-iteration/README.md)
- [DBLast: Dependent Block Drafting for Stochastic Speculative Decoding](../../../reproductions/2608.05448-dblast/README.md)
- [On the Design Space of Continuous Diffusion Language Models](../../../reproductions/2610.13834-doublecat-semicat/README.md)
- [dQwen3.5: Adapting Hybrid Language Models into Bidirectional Diffusion Language Models](../../../foundation-models/2609.20751-dqwen35/README.md)
- [ECHO: Early-layer Collaborative Hierarchical Orchestration with Bonus Logits in Speculative Decoding](../../../foundation-models/2609.17241-echo/README.md)
- [Designing Transformers for Continuous Diffusion Language Models](../../../foundation-models/2610.22330-langdit/README.md)
- [LoopSpec: Pipelined Self-Speculative Decoding for Looped Transformers](../../../foundation-models/2609.17184-loopspec/README.md)
- [Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](../../../reproductions/2401.10774-medusa/README.md)
- [On Trajectory-Aware Training for Masked Diffusion Language Models](../../../foundation-models/2609.37974-pumba/README.md)
- [Efficient, Property-Aligned Fan-Out Retrieval via RL-Compiled Diffusion](../../../foundation-models/2603.06397-r4t/README.md)
- [Register Tokens for Bounded-State Reasoning in Diffusion Language Models](../../../foundation-models/2609.16372-register-tokens-dllm/README.md)
- [Fast Inference from Transformers via Speculative Decoding](../../../reproductions/2211.17192-speculative-decoding/README.md)
- [Time-Anchored Diffusion Language Models: Latent-Space Caching for Fast Generation](../../../foundation-models/2609.37924-tadm/README.md)
- [Windowed-MTP: Removing the Full-Context Draft-KV Tax at Million-Token Context](../../../reproductions/2607.21535-windowed-mtp/README.md)
- [Blurring the Block Boundaries: Overlapping Block Denoising for Efficient Diffusion Language Models](../../../foundation-models/2611.14387-b3/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/foundation-models/generation-paths.md) · [返回全部精读卡片](../index.md)
