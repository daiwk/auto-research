---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 会预测下一幕，还不等于会行动或保持同一个世界

[多模态](../index.md) · 更新 2026-10-29 · 23 篇主题资料 / 7 篇重点对照

世界模型需要分别回答：状态表征保留什么、动作如何影响未来、计划怎样被验收、跨段记忆如何维持。LeWAM与V-JEPA Policy连接预测和动作，预测—规划评测拆解误差，WOVEN提供视觉转移监督，PPMem维护几何记忆，VBVR-Pro定义可执行验收。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/multimodal-models/world-state-actions.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：学习对象：未来latent、动作分布、视觉转移、持久几何 · 控制连接：联合塑造encoder或冻结视觉表征 · 误差接口：latent loss、物理状态误差、实际规划成功 · 证据生成与验收：生成候选、程序约束、跨视角一致性

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [LeWAM: End-to-End World and Action Modeling with JEPAs](../../../reproductions/2610.12818-lewam/README.md) · [原始来源](https://arxiv.org/abs/2610.12818)<br>章节：背景与主要改动、核心公式、数据协议、结果与边界 | 同阶段联合学习视觉encoder、动作条件latent动力学与flow-matching策略，并可精炼候选动作计划。 | 控制监督可塑造表示，但训练目标与规划仍需分别验收；A100缩放闭环是非holdout诊断，未观察到规划优势。 |
| [V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents](../../../foundation-models/2609.37250-vjepa-policy/README.md) · [原始来源](https://arxiv.org/abs/2609.37250)<br>章节：背景与主要改动、核心公式、复现边界 | 冻结V-JEPA 2.1视觉encoder，联合训练未来latent predictor与读取未来上下文的action expert。 | 复用预训练视觉空间，控制不能任意改写encoder；本地仅L1 stop-gradient与flow核，未加载原模型和机器人数据。 |
| [One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models](../../../foundation-models/2610.19375-jepa-prediction-planning/README.md) · [原始来源](https://arxiv.org/abs/2610.19375v1)<br>章节：背景与主要改动、核心公式、预算与实现差异、聚合、结果与边界 | 同一冻结物理decoder分别读取真实与预测latent，拆分表示误差、预测误差及excess，再独立评规划。 | 一步误差不替代长程成功；完整多环境重训/MPC成本过高未复现，CPU指标仅接口诊断。 |
| [WOVEN: Weaving Visual World Modeling into Multimodal LLMs](../../../reproductions/2610.12417-woven/README.md) · [原始来源](https://arxiv.org/abs/2610.12417)<br>章节：背景与主要改动、核心公式、数据协议、公开资源与结果 | 以(s,a,s′)组织真实生成视频rollout，构造前向、反向与反事实视觉转移监督进入MLLM训练。 | 生成转移的可信度与OOD任务须另验；本地有小样本真实transition SFT，未运行后续GRPO。 |
| [Persistent Planar Memory for Video World Models](../../../foundation-models/2610.23795-ppmem/README.md) · [原始来源](https://arxiv.org/abs/2610.23795)<br>章节：背景与主要改动、核心公式与流程、本地复现与成本判断 | 将局部平面primitive合并到世界坐标持久pool，光栅化深度反馈后续视频chunk。 | 压缩几何要处理遮挡、去重和相机条件；当前仅研究资料，完整视频/几何训练成本过高未复现。 |
| [VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning](../../../reproductions/2608.26105-vbvr-pro/README.md) · [原始来源](https://arxiv.org/abs/2608.26105)<br>章节：背景与主要改动、核心公式、复现边界 | 以任务专用可执行scorer核对中间状态、约束和最终状态，为生成模型提供奖励。 | 确定性判据只覆盖明确定义任务；本地程序scorer不等同已训练14B/19B视频模型。 |
| [GUI-JEPA: Candidate-Conditioned JEPA Latents as a Fast Action Policy for Mobile GUI Agents](../../../foundation-models/2610.36877-gui-jepa/README.md) · [原始来源](https://arxiv.org/abs/2610.36877v1)<br>章节：背景与主要改动、核心公式 | 候选动作条件残差predictor及ROI/global结构评分，listwise正例损失。 | 真实屏幕编码、候选生成与环境外置；没有GUI benchmark能力结果。 |

</div>

## 取舍分析 {#analysis}

### 表征能读、未来能预测、行动能成功是三次不同验收

LeWAM让控制与预测共同训练视觉表示，V-JEPA Policy则固定encoder后学习未来与动作。无论选哪条路径，都需要知道物理状态是否已在表示中、预测器额外引入多少误差、规划是否真正成功。预测—规划评测用同一物理decoder拆前两项，再单独运行规划，防止用较小latent loss包办全部结论。

对照来源：[lewam](../../../reproductions/2610.12818-lewam/README.md) · [vjepa-policy](../../../foundation-models/2609.37250-vjepa-policy/README.md) · [jepa-prediction-planning](../../../foundation-models/2610.19375-jepa-prediction-planning/README.md)

### 生成合理候选与验证世界一致性需要不同接口

WOVEN用生成的视频转移提供训练材料，关键是视觉变化实际进入监督，而不是提示先写结果。PPMem另解决跨chunk与跨视角的几何持久性，给定下一相机轨迹不等于知道未来真实帧。VBVR-Pro把可执行约束变成验收，但scorer实现不自动带来强生成器；这三项分别对应数据、记忆与验证。

对照来源：[woven](../../../reproductions/2610.12417-woven/README.md) · [ppmem](../../../foundation-models/2610.23795-ppmem/README.md) · [vbvr-pro](../../../reproductions/2608.26105-vbvr-pro/README.md)

### 10月29日：新方法与来源变化

GUI-JEPA在当前屏幕latent上预测候选动作导致的残差后继，并结合动作ROI/global区域和结构余弦评分。它与像素视频生成的监督/输出不同，也不等于真实GUI执行器；当前组件接外部冻结latent和文本匹配分数，保留真实三层predictor与训练头，但不使用训练正样本标签替forward选动作。

对照来源：[lewam](../../../reproductions/2610.12818-lewam/README.md) · [gui-jepa](../../../foundation-models/2610.36877-gui-jepa/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### LeWAM与V-JEPA Policy都有未来latent和action expert，是否只是换了视觉backbone？ {#cross-frozen-versus-joint-encoder}

??? note "展开答案与例子"

    **答案：** 不只是。LeWAM联合更新视觉encoder、动力学和策略，原文使用online target；V-JEPA Policy冻结预训练encoder并对未来目标stop-gradient。控制梯度能否塑造视觉空间、未来目标是否移动，都是训练合同。不能只把两者画成同一框图，就忽略这些差异。

    **教学例子：** 教学例子：某位置特征不利于抓取时，一条路径可让控制监督调整encoder，另一条主要在固定表征上调整predictor和动作模块。

    对照来源：[lewam](../../../reproductions/2610.12818-lewam/README.md) · [vjepa-policy](../../../foundation-models/2609.37250-vjepa-policy/README.md)

### JEPA预测误差更低，能直接认定LeWAM的候选规划比reactive policy强吗？ {#cross-low-prediction-loss-not-planning}

??? note "展开答案与例子"

    **答案：** 不能。预测误差混合表征本身是否可读与预测器新增偏差，且长程计划还受动作候选、累积误差和目标分布影响。预测—规划评测要求同decoder拆项并独立测规划。LeWAM当前本地闭环未观察到规划优势，也属非holdout诊断，不能从loss补写成功结论。

    **教学例子：** 教学例子：模型准确预测不动时的画面，仍可能选不出能到目标的动作；预测容易不等于控制有效。

    对照来源：[jepa-prediction-planning](../../../foundation-models/2610.19375-jepa-prediction-planning/README.md) · [lewam](../../../reproductions/2610.12818-lewam/README.md)

### WOVEN的反事实视频、PPMem的平面记忆与VBVR-Pro程序评分，谁提供正确性保证？ {#cross-rollout-memory-verifier}

??? note "展开答案与例子"

    **答案：** 三者承担不同职责：WOVEN产生动作条件视觉转移材料，PPMem维持几何记忆，VBVR-Pro在已定义任务上执行约束检查。生成逼真不保证转移正确，记忆存在不保证几何无误，程序验收也只覆盖其判据。需把数据来源、状态维护和评分覆盖逐项核对，不能互相背书。

    **教学例子：** 教学例子：回到旧视角时物体位置一致可由几何记忆帮助，但是否满足任务中的数量或顺序要求，仍需相应验证规则。

    对照来源：[woven](../../../reproductions/2610.12417-woven/README.md) · [ppmem](../../../foundation-models/2610.23795-ppmem/README.md) · [vbvr-pro](../../../reproductions/2608.26105-vbvr-pro/README.md)

### GUI-JEPA预测latent后继，为什么不能直接当作已在手机上验证动作成功？ {#cross-oct29-method-boundary}

??? note "展开答案与例子"

    **答案：** 后继是学到的表示预测，模型可能漏掉状态约束；执行成功需真实环境反馈。小latent前向、候选排列等变和梯度检查只验证模块合同，不能替代动作到环境的闭环。

    **教学例子：** 教学例：模型预测点击后的页面向量接近目标，不等于已经检测到真实设备按钮可点击或请求成功。

    对照来源：[lewam](../../../reproductions/2610.12818-lewam/README.md) · [gui-jepa](../../../foundation-models/2610.36877-gui-jepa/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-29** · GUI-JEPA在当前屏幕latent上预测候选动作导致的残差后继，并结合动作ROI/global区域和结构余弦评分。它与像素视频生成的监督/输出不同，也不等于真实GUI执行器；当前组件接外部冻结latent和文本匹配分数，保留真实三层predictor与训练头，但不使用训练正样本标签替forward选动作。

涉及：[gui-jepa](../../../foundation-models/2610.36877-gui-jepa/README.md)

**2026-10-27** · 首版：比较联合或冻结视觉编码的动作模型、预测与规划验收、WOVEN转移监督、PPMem几何记忆与VBVR程序评分；已阅22篇摘要，精读6篇。

覆盖 22 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 23 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [ALPS: Visual State Encoders for World Models](../../../foundation-models/2610.30120-alps/README.md)
- [Agentic World Action Models](../../../multimodal-models/2610.30136-aw0/README.md)
- [DT-JEPA: Learning to Predict Future Representations for Decision-Making](../../../foundation-models/2610.32657-dt-jepa/README.md)
- [EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video](../../../foundation-models/2610.22681-ego-p2c/README.md)
- [EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos](../../../foundation-models/2610.20904-egojepa/README.md)
- [ESC: Escaping 2D Diffusion Ambiguity with Geometric Constraints for Consistent Novel View Synthesis](../../../foundation-models/2610.23732-esc/README.md)
- [EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference](../../../reproductions/2610.14324-ev-jepa/README.md)
- [Gen4P: Video Generators are 4D Perceivers](../../../foundation-models/2610.22371-gen4p/README.md)
- [Inside-JEPA: From Prediction to Relational Grounding in Latent World Models](../../../foundation-models/2610.31194-inside-jepa/README.md)
- [One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models](../../../foundation-models/2610.19375-jepa-prediction-planning/README.md)
- [LeWAM: End-to-End World and Action Modeling with JEPAs](../../../reproductions/2610.12818-lewam/README.md)
- [LocaLeJEPA: Maximum Entropy Representations under Geometric Priors](../../../foundation-models/2610.28458-locale-jepa/README.md)
- [Editing Everything Everywhere All at Once](../../../multimodal-models/2606.31278-mice/README.md)
- [Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning](../../../reproductions/2610.20158-oob-regularization/README.md)
- [Persistent Planar Memory for Video World Models](../../../foundation-models/2610.23795-ppmem/README.md)
- [Mid-Training Language Models on Raw Video](../../../multimodal-models/2610.11019-raw-video-midtraining/README.md)
- [SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices](../../../reproductions/2610.13740-smolwam/README.md)
- [Time-JEPA: Grounding Video World Models with Physical Time Series](../../../foundation-models/2610.23982-time-jepa/README.md)
- [UniAction: Unified Action Conditioning for World Models](../../../multimodal-models/2610.32977-uniaction/README.md)
- [VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning](../../../reproductions/2608.26105-vbvr-pro/README.md)
- [V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents](../../../foundation-models/2609.37250-vjepa-policy/README.md)
- [WOVEN: Weaving Visual World Modeling into Multimodal LLMs](../../../reproductions/2610.12417-woven/README.md)
- [GUI-JEPA: Candidate-Conditioned JEPA Latents as a Fast Action Policy for Mobile GUI Agents](../../../foundation-models/2610.36877-gui-jepa/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/multimodal-models/world-state-actions.md) · [返回全部精读卡片](../index.md)
