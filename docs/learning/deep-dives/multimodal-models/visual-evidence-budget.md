---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 少看、晚看还是再看：把视觉预算放到正确阶段

[多模态](../index.md) · 更新 2026-10-27 · 16 篇主题资料 / 6 篇重点对照

视觉预算不只有token数。StackTok选择已编码证据，PACE提前分配输入分辨率，ViMoD保留可恢复细节，Frames-on-Demand按需取帧，AdaLoop多算已有视觉状态，OmniKVQuant减少每份cache的位宽。必须同时追踪信息是否还在、哪段成本已支付。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/multimodal-models/visual-evidence-budget.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：介入阶段：输入编码前、编码后、生成中、cache存储 · 信息去向：丢弃、聚合、外存保留、重新读取 · 适应条件：问题相关性、覆盖、已生成文本、稳定停止 · 预算对象：token数、峰值存储、视觉循环、低位表示

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [StackTok: Accelerating VLMs Inference with Budget-Adaptive Visual Token Selection](../../../multimodal-models/2609.16841-stacktok/README.md) · [原始来源](https://arxiv.org/abs/2609.16841)<br>章节：背景与主要改动、核心公式与实现对应、复现边界 | 以query relevance为目标，按预算调节coverage约束，在选择准则之间切换。 | 相关性与覆盖不能只留一项；本地是单crop reference selector，未加载论文五个VLM，不能进入能力排名。 |
| [PACE: A Unified Condense-and-Extract Paradigm for Fast VLM Inference](../../../reproductions/2608.27206-pace-vlm/README.md) · [原始来源](https://arxiv.org/abs/2608.27206)<br>章节：背景与主要改动、核心公式、复现边界 | PACE的APC用浅层preview自适应缩放图像，DDAE再按置信融合语言与视觉注意力做抽取。 | 编码前缩放与编码后选token节省不同环节；真实checkpoint smoke主要跑APC，DDAE仍为独立公式/单测证据。 |
| [Look Back, Think Ahead: Visual Memory on Demand for Efficient Multimodal Reasoning](../../../multimodal-models/2610.12060-vimod/README.md) · [原始来源](https://arxiv.org/abs/2610.12060)<br>章节：背景与主要改动、核心公式、数据协议与结果、代码映射与边界 | DART保留Coarse KV与原始Fine KV，TRACE按因果文本状态HOLD或替换细节工作集。 | 可恢复不等于Fine KV不占内存；已有真实checkpoint及CUDA梯度诊断，但适配模型范围需按README限定。 |
| [Caption-once, Frames-on-Demand: Visual-Need Routing for Budget-Aware Agentic Long Video Understanding](../../../foundation-models/2609.11899-frames-on-demand/README.md) · [原始来源](https://arxiv.org/abs/2609.11899)<br>章节：背景与主要改动、复现边界 | 先建立一次caption memory，仅在文字证据不足时用固定预算回看相关视频帧。 | 文字索引可能遗漏细节，门控错误会漏看；本地确定性caption/query gate未运行长视频VLM或学得路由器。 |
| [AdaLoop: Thinking with the Vision Encoder](../../../foundation-models/2610.21323-adaloop-vision/README.md) · [原始来源](https://arxiv.org/abs/2610.21323)<br>章节：背景与主要改动、核心公式、结果与独立对照 | 以问题向量调制共享冻结视觉块，循环更新视觉状态，将额外计算投入视觉侧。 | 循环增加处理机会而非新增原始证据；完整多臂训练成本过高未复现，当前随机token梯度诊断。 |
| [OmniKVQuant: KV Cache Quantization for Omni-LLMs](../../../foundation-models/2609.11582-omnikvquant/README.md) · [原始来源](https://arxiv.org/abs/2609.11582)<br>章节：背景与主要改动、复现边界 | key按短时间窗设量化范围，value按模态独立旋转，降低KV表示位宽。 | 压缩cache数值与减少cache条目不同；本地2-bit NumPy reference无真实GPU kernel加速证据。 |

</div>

## 取舍分析 {#analysis}

### token变少时，先问原始细节还在哪里

PACE在编码前缩放可能已改变可见细节，StackTok从编码结果中按问题和覆盖选取；ViMoD则明确保留Fine KV，并在生成中恢复所需工作集。Frames-on-Demand保留的是可回看的视频与文字索引。它们的“少看”并不等价：能否恢复，取决于是否还保存原证据以及有没有可执行的回读路径。

对照来源：[pace-vlm](../../../reproductions/2608.27206-pace-vlm/README.md) · [stacktok](../../../multimodal-models/2609.16841-stacktok/README.md) · [vimod](../../../multimodal-models/2610.12060-vimod/README.md) · [frames-on-demand](../../../foundation-models/2609.11899-frames-on-demand/README.md)

### 活动工作集、峰值内存与额外计算应分开记账

ViMoD较小的活动细节集不自动意味着原始Fine KV已从存储中消失；OmniKVQuant处理的是每份KV的数值位宽与误差。AdaLoop再从另一轴增加视觉循环，以计算换更有问题针对性的表示。若只报token减少率，会同时漏掉存储、回读和循环开销，无法判断实际设备预算是否满足。

对照来源：[vimod](../../../multimodal-models/2610.12060-vimod/README.md) · [omnikvquant](../../../foundation-models/2609.11582-omnikvquant/README.md) · [adaloop-vision](../../../foundation-models/2610.21323-adaloop-vision/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### ViMoD只激活少量Fine KV，就一定比KV量化更省峰值内存吗？ {#cross-active-versus-resident-cache}

??? note "展开答案与例子"

    **答案：** 不能这样推出。ViMoD仍保留原Fine KV以便恢复，活动工作集小与全部驻留状态小不同；OmniKVQuant降低每份cache的位宽，又有旋转、量化和解包代价。比较要测同输入下的存储位置、峰值内存及端到端延迟，不能将工作集比例与bit数直接相乘当结果。

    **教学例子：** 教学例子：桌面只摆一本书不代表仓库其余书已消失；把每本书压缩存储则是另一种节省，取书也有成本。

    对照来源：[vimod](../../../multimodal-models/2610.12060-vimod/README.md) · [omnikvquant](../../../foundation-models/2609.11582-omnikvquant/README.md)

### PACE把图像先缩小，与StackTok选择token、ViMoD按需回读细节，信息损失发生在同一位置吗？ {#cross-shrink-before-encode-versus-recover}

??? note "展开答案与例子"

    **答案：** 不同。PACE的APC可在完整编码前改变图像预算，StackTok面对已编码token，ViMoD明确保留原Fine KV供后续读取。已在低分辨率输入中消失的信息，不能只靠末端选择规则恢复。不同阶段的压缩既影响质量，也决定哪些编码成本已经支付。

    **教学例子：** 教学例子：小字在缩图后不可辨，与高分辨率已编码但暂未激活，是两种状态；后者才可能沿已有细节cache回读。

    对照来源：[pace-vlm](../../../reproductions/2608.27206-pace-vlm/README.md) · [stacktok](../../../multimodal-models/2609.16841-stacktok/README.md) · [vimod](../../../multimodal-models/2610.12060-vimod/README.md)

### AdaLoop多循环一次，是否就等于Frames-on-Demand多读取一帧？ {#cross-more-processing-versus-more-evidence}

??? note "展开答案与例子"

    **答案：** 不是。AdaLoop用共享视觉块继续处理已有状态，问题调制可改变表示；Frames-on-Demand在需要时取得额外帧证据。多计算不必带来新观测，多观测也不保证被正确利用。不能把循环次数、帧数和答案稳定性混成同一种“看得更多”，更不能用gold决定部署停止。

    **教学例子：** 教学例子：反复分析一张模糊截图，与取回视频中另一张更清晰的帧，增加的信息条件并不相同。

    对照来源：[adaloop-vision](../../../foundation-models/2610.21323-adaloop-vision/README.md) · [frames-on-demand](../../../foundation-models/2609.11899-frames-on-demand/README.md) · [vimod](../../../multimodal-models/2610.12060-vimod/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-27** · 首版：比较StackTok选择、PACE输入预算、ViMoD可恢复KV、按需帧读取、视觉循环与KV量化；已阅16篇摘要，精读6篇。

覆盖 16 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 16 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [AdaLoop: Thinking with the Vision Encoder](../../../foundation-models/2610.21323-adaloop-vision/README.md)
- [Caption-once, Frames-on-Demand: Visual-Need Routing for Budget-Aware Agentic Long Video Understanding](../../../foundation-models/2609.11899-frames-on-demand/README.md)
- [HAWK: Rethinking Multimodal Drafting for Speculative Decoding](../../../foundation-models/2610.00623-hawk/README.md)
- [Muse Glimmer 30B: An On-Device Agentic Model](../../../foundation-models/2610.24628-muse-glimmer-30b/README.md)
- [MWOP: Modality-aware Width-wise Operation Pruning for Efficient MLLMs](../../../foundation-models/2610.01434-mwop/README.md)
- [OmniKVQuant: KV Cache Quantization for Omni-LLMs](../../../foundation-models/2609.11582-omnikvquant/README.md)
- [PACE: A Unified Condense-and-Extract Paradigm for Fast VLM Inference](../../../reproductions/2608.27206-pace-vlm/README.md)
- [Retrofitting Recurrent Vision-Language Models from Pretrained Backbones](../../../foundation-models/2610.22075-rr-vlm/README.md)
- [Sink-Sparse Hybrid Attention for Efficient Inference in T2I/T2V Diffusion Transformers](../../../foundation-models/2610.22975-sink-sparse/README.md)
- [SoftCache: Adaptive Step Size Caching for Diffusion Transformers](../../../foundation-models/2610.22369-softcache/README.md)
- [StackTok: Accelerating VLMs Inference with Budget-Adaptive Visual Token Selection](../../../multimodal-models/2609.16841-stacktok/README.md)
- [V-CoLA: Vision Token Compression with Linear Attention](../../../multimodal-models/2610.11251-vcola/README.md)
- [VETO: Video Efficient Token Optimization for Vision Language Models](../../../foundation-models/2610.01785-veto/README.md)
- [Video Encoders Built on Image Representations](../../../foundation-models/2610.06616-video-encoder-selection/README.md)
- [VideoMM: Adaptive Macro-Micro Inference for Efficient Video MLLMs](../../../multimodal-models/2609.16722-videomm/README.md)
- [Look Back, Think Ahead: Visual Memory on Demand for Efficient Multimodal Reasoning](../../../multimodal-models/2610.12060-vimod/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/multimodal-models/visual-evidence-budget.md) · [返回全部精读卡片](../index.md)
