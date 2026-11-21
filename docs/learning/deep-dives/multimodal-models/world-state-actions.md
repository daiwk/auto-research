---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 会预测下一幕，还不等于会行动或保持同一个世界

[多模态](../index.md) · 更新 2026-11-21 · 36 篇主题资料 / 20 篇重点对照

世界模型需要分别回答：状态表征保留什么、动作如何影响未来、计划怎样被验收、跨段记忆如何维持。LeWAM与V-JEPA Policy连接预测和动作，预测—规划评测拆解误差，WOVEN提供视觉转移监督，PPMem维护几何记忆，VBVR-Pro定义可执行验收。 SWIM从离线动作可预测性学习状态坐标的相对权重，训练期校准latent距离，部署时不向规划器增加真实状态。

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
| [SWIM: Learning What Matters from Behaviors for JEPA World Models](../../../foundation-models/2610.36662-swim/README.md) · [原始来源](https://arxiv.org/abs/2610.36662v1)<br>章节：背景与主要改动、核心公式、高成本完整实验 | 用当前状态和门控未来位移预测固定记录动作chunk，NLL加cyclic discrimination与L1学习gate；随后以sqrt(g)加权状态距离校准latent几何。 | 离线行为监督不是规划输入；gate只识别相对权重且不可二次标准化。本地不含视觉encoder、SIGReg、环境或CEM，完整训练不复现。 |
| [RS-JEPA: Remote Sensing Joint-Embedding Predictive Architecture with Scan-Path Views for Cross-Sensor Image Retrieval](../../../multimodal-models/2611.14496-rs-jepa/README.md) · [原始来源](https://arxiv.org/abs/2611.14496)<br>章节：背景与主要改动、核心公式、结果、负控与边界 | 利用Vision Mamba扫描次序形成无像素编辑视图，以直通加反梯度hard half-split增加隐藏预测难度，并让四个排除twin的传感器邻域分布对齐detached共识。 | 同主干stop-gradient target不是EMA教师；跨传感器检索表征不等于动作条件未来预测或策略。局部扫描/梯度/邻域核不含Vim、完整CVA/predictor或遥感检索成绩，四V100完整实验不复现。 |
| [OnlyAct: Extracting Action Representations from Foundation Models for World Models](../../../multimodal-models/2611.14420-onlyact/README.md) · [原始来源](https://arxiv.org/abs/2611.14420)<br>章节：背景与主要改动、核心公式、结果、负控与边界 | 在预训练V-JEPA2联合帧表征上，以场景交换正例及同视频非重叠hard negative适配动作几何，再冻结供世界模型使用。 | RS-JEPA用扫描视图和跨传感器邻域共识学习场景检索；OnlyAct希望保留动作、抑制场景。共享JEPA来源不代表优化目标相同。本地两者均只有独立公式/梯度L1，不提供图像检索或动作迁移能力排名。 |
| [Personalized health coaching via coachable health age and counterfactual wearable trajectories](../../../multimodal-models/2611.08568-sensorwm-planning/README.md) · [原始来源](https://arxiv.org/abs/2611.08568)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、结果、负控与边界 | 动作条件可穿戴JEPA以状态依赖线性算子递推潜位移，再以未来status-quo对照、个体努力归一化收益排序外部候选。 | 完整论文用私有生理数据建模；本地只实现Eq55–56排序，不产生预测、不执行动作、不给医疗建议。与LeWAM实际学习策略/动力学及闭环不同，数学排序不等于世界模型控制或临床安全。 |
| [Back to Pixels: Lifting Latent Video Diffusion into Pixel Space](../../../multimodal-models/2611.17336-pixvid/README.md) · [原始来源](https://arxiv.org/abs/2611.17336v1)<br>章节：背景与主要改动、核心机制与公式、论文离线与线上效果 | 以像素-latent线性对齐、时间校准和detailer把预训练视频DiT迁移到pixel空间，处理高分辨率细节与跨帧一致性；本轮仅资料收录。 | WOVEN用动作条件rollout形成转移监督并训练MLLM回答；PixVid改变生成器的表示与计算路径。更清晰的生成不自动意味着因果/动作正确，也不是选择题准确率。 |
| [What Should World Models Forget? Stratified Retention for Continual Adaptation](../../../foundation-models/2610.03713-stratified-retention-protocol/README.md) · [原始来源](https://arxiv.org/abs/2610.03713v2)<br>章节：背景与主要改动、核心公式、论文离线与线上效果 | 把世界知识按环境不变时间尺度分层，分别报告逐轮不变量保持和新episode修订延迟；原文是无新实证的评测提案，本地仅L0报告协议。 | WOVEN用(s,a,s&#x27;)视觉转移产生受控监督并训练MLLM；分层保持不生成训练数据、不指定适应算法。WOVEN的source_id隔离不代替逐轮不变量面板与变化后新episode查询，不能把两个分数直接排名。 |
| [RSLiveBench-UAV: A Continually Evolving Vision-Language Benchmark for Aerial Spatial Intelligence](../../../multimodal-models/2611.14953-rslivebench-uav-protocol/README.md) · [原始来源](https://arxiv.org/abs/2611.14953v1)<br>章节：背景与主要改动、核心公式、论文离线与线上效果 | 以真实新UAV观察、四场景FIFO和答案禁运控制持续评测；本地只实现采集/发布时窗、日历月禁运、SC子计分及缺失感知层次聚合。 | WOVEN训练视觉状态转移推理并按scene/action/reasoning验证迁移；RSLiveBench-UAV重点是航空几何与持续刷新。时间新鲜、真实采集和scene-OOD是不同维度，二者分数不能直接比较。 |
| [WM-Quant: Rollout-Aware Post-Training Quantization for JEPA-Style World Models](../../../foundation-models/2611.21882-wm-quant/README.md) · [原始来源](https://arxiv.org/abs/2611.21882v1)<br>章节：背景与主要改动、核心公式、同主题比较与边界 | JEPA世界模型把连续latent递归输入预测器，量化误差不会像离散token一样重置。WM-Quant保留前三个encoder blocks的8-bit激活、浮点action/proprioception控制通路，并联合优化encoder范围和每个rollout step独立的predictor范围。 | LeWAM联合训练视觉encoder、latent动力学与action flow，再对策略候选做潜空间规划；WM-Quant研究连续rollout中的量化误差与范围校准。注意新论文实验对象是LeWM/DINO-WM，不是LeWAM，未声称把WM-Quant接入了LeWAM训练或规划。 |
| [Decoding Without a Decoder: Direct Pixel Prediction from Diffusion Transformers](../../../multimodal-models/2611.22287-dwd/README.md) · [原始来源](https://arxiv.org/abs/2611.22287v1)<br>章节：背景与主要改动、核心公式、同主题比较与边界 | DWD在预训练DiT最后隐状态上并联线性pixel head，原denoising head继续驱动采样，只有最后一个非零time step才由pixel head输出图像/视频。通过分离pixel质量目标与trajectory anchoring，避免让同一输出承担冲突目标。 | PixVid迁移latent DiT到pixel输入/生成空间并加detailer；DWD保留latent采样，只改变最终读出。输出是像素不意味着整个采样都在pixel空间。 |
| [Counterfactual World Models: JEPAs That Reason About &quot;What If&quot;](../../../foundation-models/2611.24778-counterfactual-wm/README.md) · [原始来源](https://arxiv.org/abs/2611.24778v1)<br>章节：背景与主要改动、核心公式、同主题比较与边界 | 普通world model给动作的平均结果，不能仅凭更准的事实分布识别同一扰动下的个体反事实。本文将实际观测结果作为事件信息，加上同一事实预测器对两个动作的预测差；加性扰动时精确，平滑短时动力学下有交互误差界，但碰撞、乘法故障和弯曲坐标可破坏近似。 | DT-JEPA在历史下预测未来latent分布并用于决策，真实未来只在训练目标出现；CWM在一个事实结果已经可见后推断同一事件的替代动作结果。不能让CWM提前使用尚未观测的未来，亦不能把DT-JEPA的均值直接称个体反事实。 |
| [Autoregressive View Model](../../../multimodal-models/2611.23417-autoregressive-view-model/README.md) · [原始来源](https://arxiv.org/abs/2611.23417v1)<br>章节：背景与主要改动、核心公式、同主题比较与边界 | AVM不拟合显式3D表示，而在给定相机路径下生成短视图片段。预填图像/视频与历史生成片段统一成为context；检索保持活动上下文有界。先把双向视频DiT微调为N-in-1-out的flow matching，再以自身rollout做因果tuning和蒸馏，让生成内容可回到历史中支持后续重访。 | CWM在一个事实事件之后改变动作并复用同一扰动残差；AVM沿相机轨迹继续生成并检索历史视图。二者都使用world model语汇，但AVM的场景重访一致性不证明同一扰动反事实可识别。 |
| [JEPA Dots: Dual-Latent World Model for Language-Guided Robot Control](../../../multimodal-models/2611.24062-jepa-dots/README.md) · [原始来源](https://arxiv.org/abs/2611.24062v1)<br>章节：背景与主要改动、核心公式、同主题比较与边界 | 共享视觉骨干之后拆动力学和任务两条latent路径，语言FiLM只进入任务路径。world query只读动力学历史和给定clean动作，policy读历史、goal和noisy动作；多层mask同时阻断间接泄漏。固定参数、观测和给定动作时，换指令不能改变world预测，但policy可以生成不同动作。 | LeWAM联合world/action并用预测模型规划；JEPA Dots强调语言目标与动力学给定动作输入的隔离，部署world分支不参与动作搜索。相同masked-MoT背景不代表推理链相同。 |
| [MV-JEPA: Post-Training Video Encoders for Cross-View Understanding](../../../foundation-models/2611.25172-mv-jepa/README.md) · [原始来源](https://arxiv.org/abs/2611.25172v1)<br>章节：背景与主要改动、核心公式、同主题比较与边界 | MV-JEPA直接后训练已有JEPA视频编码器，强化不同摄像头视角之间的对象/时刻对应。共享student分别编码各context view的可见token；联合predictor利用所有context特征，既重建被mask的context位置，又预测一个完全held-out视图。held-out图像/特征从不进入student或predictor，只提供teacher目标；推理仍可独立编码单视角。 | Time-JEPA用物理时序作额外训练目标，在同一online encoder上执行masked潜变量预测和unmasked物理态回归；MV-JEPA用另一个摄像头的latent作held-out目标，并让联合predictor从多个独立context视图推断。两者都不能把训练目标喂回推理输入，但MV-JEPA的跨view query不是Time-JEPA的传感器head；重放保持表征和物理时序对齐也是不同验收。 |

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

### 行为监督可以改几何，但不应变成未来状态oracle

GUI-JEPA在候选动作条件下生成latent残差，并通过候选决策损失学习打分；SWIM则先在离线记录上判断哪些状态位移更有助于预测当前固定动作chunk，再把连续gate冻结为latent几何的监督权重。两者都不能因latent运算通过就宣称执行成功。SWIM的h只控制未来state间隔，动作目标仍是当前决策步固定chunk；部署时逆动力学与真实未来state均不进入规划。sqrt(g)后再逐坐标标准化还会抵消权重。

对照来源：[swim](../../../foundation-models/2610.36662-swim/README.md) · [gui-jepa](../../../foundation-models/2610.36877-gui-jepa/README.md)

### JEPA表征对齐与world-action闭环，需要不同的监督与验收

RS-JEPA把配准传感器图像与不同扫描视图变成更一致的检索表征，hard划分与邻域损失针对当前场景关系；没有因其名字带JEPA就实现动作条件状态转移。V-JEPA Policy冻结预训练encoder，再训练future-latent predictor与action expert，动作输出及环境成功另需验收。遥感F1@5、latent预测误差和机器人成功率不能汇成一条分数。

对照来源：[rs-jepa](../../../multimodal-models/2611.14496-rs-jepa/README.md) · [vjepa-policy](../../../foundation-models/2609.37250-vjepa-policy/README.md)

### 跨视图保持的内容，可以是场景，也可以是动作

RS-JEPA希望不同传感器检索到同一场景，并让其邻域关系一致；OnlyAct反而把动作保持但场景改变的样本拉近，用同场景不同窗作为难负例。二者对场景身份的需求不同，不能直接拼接一个通用InfoNCE就声称兼得。OnlyAct正负构造依赖光流/相机静动假设，局部候选mask与损失的CUDA通过不能验证这些语义假设。

对照来源：[onlyact](../../../multimodal-models/2611.14420-onlyact/README.md) · [rs-jepa](../../../multimodal-models/2611.14496-rs-jepa/README.md)

### 有动作条件预测，不等于已经识别干预效果或完成控制

LeWAM在联合表征与动作flowmatching后，用冻结动力学rollout、动作梯度优化和环境反馈闭环；其现有本地结果仍是非holdout诊断，未测到规划优势。SensorWM则从观察性可穿戴数据学习条件轨迹，并按个体行为变动尺度把预测收益转成候选比值。它明确不识别因果干预效果；离线教练偏好也不是实际健康结局。二者都需区分预测、选择、执行和效果证据，本地SensorWM排序更不能替代缺失的模型。

对照来源：[sensorwm-planning](../../../multimodal-models/2611.08568-sensorwm-planning/README.md) · [lewam](../../../reproductions/2610.12818-lewam/README.md)

### 生成视频与学习状态转移不是同一次验收

视频生成器可以作为下游转移训练的数据源，但要分开验证视觉质量、动作条件忠实度、状态一致性和学习后的推理能力。PixVid完整14B/130万clip矩阵不运行；WOVEN既有小样本SFT负结果也不用于推断PixVid的收益。两者不构成本地联合系统。

对照来源：[pixvid](../../../multimodal-models/2611.17336-pixvid/README.md) · [woven](../../../reproductions/2610.12417-woven/README.md)

### 状态变化监督不等于“该改什么”的持续评测

WOVEN按scene/action/reasoning控制训练与泛化，真实视觉状态转移进入response-only SFT；本地已有分组小样本负结果。Stratified Retention进一步区分旧事实过期与结构遗忘：应保持的不变量可纠错但不能退化，实例位置必须及时更新。要把二者连起来，需预先标注稳定性层、适应后逐轮probe和新episode修订轨迹；本轮没有这些模型实验，只有拒绝泄漏与删失混淆的协议。

对照来源：[stratified-retention-protocol](../../../foundation-models/2610.03713-stratified-retention-protocol/README.md) · [woven](../../../reproductions/2610.12417-woven/README.md)

### 新拍摄与新场景不是同一个泛化控制

WOVEN源初始图分组防止多个动作/问题跨split，RSLiveBench-UAV要求每批图像在相邻release之间拍摄，并退役最早入窗场景。持续更新降低旧答案暴露但不自动消除场景偏差；反过来，生成场景的OOD测试不提供真实航空空间几何。小FIFO重放只检验时窗与分母，不证明任何VLM空间能力或完整benchmark已接入。

对照来源：[rslivebench-uav-protocol](../../../multimodal-models/2611.14953-rslivebench-uav-protocol/README.md) · [woven](../../../reproductions/2610.12417-woven/README.md)

### 先学习可控制的动力学，再讨论数值精度如何改变rollout

实读LeWAM说明其action flow、latent MSE和SIGReg联合训练，规划只更新动作，选择用未惩罚goal cost；本地训练轨迹目标仍是非holdout诊断。WM-Quant冻结基础模型并联合校准encoder/逐步predictor范围，控制通路保留浮点，且必须遵循整数zero-point Eq1–2。两篇都依赖动作条件rollout，但训练动力学、规划搜索与PTQ校准不能互相补证；本轮小张量校准没有执行LeWAM量化或机器人成功率比较。

对照来源：[wm-quant](../../../foundation-models/2611.21882-wm-quant/README.md) · [lewam](../../../reproductions/2610.12818-lewam/README.md)

### DWD：将最终像素读出与去噪目标分开

PixVid迁移latent DiT到pixel输入/生成空间并加detailer；DWD保留latent采样，只改变最终读出。输出是像素不意味着整个采样都在pixel空间。 pixel与trajectory损失从不同time distributions取样，两次反传后统一optimizer step。末步不用CFG，因为该步读出像素而不推进trajectory；t=0的“当成decoder”模式在原文退化。

对照来源：[dwd](../../../multimodal-models/2611.22287-dwd/README.md) · [pixvid](../../../multimodal-models/2611.17336-pixvid/README.md)

### Counterfactual WM：复用已发生事件的残差，而非预测平均未来

DT-JEPA在历史下预测未来latent分布并用于决策，真实未来只在训练目标出现；CWM在一个事实结果已经可见后推断同一事件的替代动作结果。不能让CWM提前使用尚未观测的未来，亦不能把DT-JEPA的均值直接称个体反事实。 观测是已经执行动作a之后的结果，替代动作真值不作为算法输入。先在embedding运输后decode，与先decode每项再做残差运输一般不同；选择坐标需要额外readout假设。误差等于个体动作效应与平均动作效应之差，不是“world model零误差就保证反事实零误差”。

对照来源：[counterfactual-wm](../../../foundation-models/2611.24778-counterfactual-wm/README.md) · [dt-jepa](../../../foundation-models/2610.32657-dt-jepa/README.md)

### AVM：把场景作为带检索上下文的视图流生成

CWM在一个事实事件之后改变动作并复用同一扰动残差；AVM沿相机轨迹继续生成并检索历史视图。二者都使用world model语汇，但AVM的场景重访一致性不证明同一扰动反事实可识别。 上式用统一记号概括原文flow目标与context检索，不补造新的算法。检索对象既有真实输入也有模型生成的历史；没有显式3D不等于没有几何条件。相机、时间和context角色仍影响生成。

对照来源：[autoregressive-view-model](../../../multimodal-models/2611.23417-autoregressive-view-model/README.md) · [counterfactual-wm](../../../foundation-models/2611.24778-counterfactual-wm/README.md)

### JEPA Dots：隔离语言任务表征与固定动作下的动力学预测

LeWAM联合world/action并用预测模型规划；JEPA Dots强调语言目标与动力学给定动作输入的隔离，部署world分支不参与动作搜索。相同masked-MoT背景不代表推理链相同。 不变性约束的是forward信息通路，不是说共享骨干训练后两种latent统计独立。world预测分支只在训练监督中使用，部署是action flow生成8动作、执行前2个后重规划，不是用world model在线搜索动作。

对照来源：[jepa-dots](../../../multimodal-models/2611.24062-jepa-dots/README.md) · [lewam](../../../reproductions/2610.12818-lewam/README.md)

### MV-JEPA: Post-Training Video Encoders for Cross-View Understanding

Time-JEPA用物理时序作额外训练目标，在同一online encoder上执行masked潜变量预测和unmasked物理态回归；MV-JEPA用另一个摄像头的latent作held-out目标，并让联合predictor从多个独立context视图推断。两者都不能把训练目标喂回推理输入，但MV-JEPA的跨view query不是Time-JEPA的传感器head；重放保持表征和物理时序对齐也是不同验收。 完整context和held-out由EMA teacher编码，经逐token LayerNorm并stop-gradient。context视图分配互异随机view ID，held-out使用专属ID；masked-context和held-out使用两种不同mask embedding。Eq4对masked-context和全部held-out目标token等权，先逐example归一化，再对batch取均值，不能按view等权或全batch微平均。每epoch随机打散152次多视图与148次原始单视图replay，共享online encoder和predictor；optimizer后按0.99925更新teacher。

对照来源：[mv-jepa](../../../foundation-models/2611.25172-mv-jepa/README.md) · [time-jepa](../../../foundation-models/2610.23982-time-jepa/README.md)

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

### SWIM训练读取q(t+h)，与GUI-JEPA按候选动作打分，为什么都不允许把真实后继直接交给部署策略？ {#cross-swim-training-future-not-planning-oracle}

??? note "展开答案与例子"

    **答案：** q(t+h)是SWIM训练逆动力学和学习gate的离线标签，门控后迁移的是状态距离监督；部署只按图像latent规划。GUI-JEPA对后继的条件表示也只是模型计算，不是已观察环境反馈。真实后继若直接给受测策略，会把预测问题替换为oracle。

    **教学例子：** 教学示意：训练时可用录像中5h帧后的状态评估位移，但选择下一动作时不能先看录像答案；h变化也不把目标动作从固定五帧自动扩为整个h段。

    对照来源：[swim](../../../foundation-models/2610.36662-swim/README.md) · [gui-jepa](../../../foundation-models/2610.36877-gui-jepa/README.md)

### RS-JEPA的跨传感器邻域一致，是否证明已经能规划动作？ {#cross-retrieval-jepa-not-action-policy}

??? note "展开答案与例子"

    **答案：** 不能。它约束配准图像的检索表示及其他场景的相似性关系，没有定义动作条件动力学和策略输出。V-JEPA Policy另有future predictor与flow-matching action expert；表示核通过也不能代替环境任务验收。

    **教学例子：** 教学例：两个传感器都把同一类农田排为相似邻居，只说明表征关系一致；它没有给出机器人移动一步后会看到什么或应该输出哪个动作。

    对照来源：[rs-jepa](../../../multimodal-models/2611.14496-rs-jepa/README.md) · [vjepa-policy](../../../foundation-models/2609.37250-vjepa-policy/README.md)

### RS-JEPA与OnlyAct都做表征学习，为什么不能用同场景跨传感器正例替代OnlyAct正例？ {#cross-cross-jepa-scene-versus-action-invariance}

??? note "展开答案与例子"

    **答案：** 同场景对齐保留场景身份，而OnlyAct要跨场景保留动作。替换会改变不变性目标，甚至鼓励动作编码器依赖场景捷径。InfoNCE公式相似不说明配对语义相同，真实动作迁移需要独立验证。

    **教学例子：** 教学例：同一桥梁的SAR和光学图适合RS-JEPA；OnlyAct需要不同房间里的相同开门动作，而不是同房间任意两个动作。

    对照来源：[onlyact](../../../multimodal-models/2611.14420-onlyact/README.md) · [rs-jepa](../../../multimodal-models/2611.14496-rs-jepa/README.md)

### SensorWM排序核与LeWAMplanner都返回较优候选，是否能用同一个“规划成功率”来比较？ {#cross-cross-worldmodel-ranking-versus-closed-loop-evidence}

??? note "展开答案与例子"

    **答案：** 不能。SensorWM局部核只对外部端点做收益/努力排序，没有模型、医疗判断或执行；LeWAMplanner从模型产生动作并进入环境闭环，现有结果也未形成holdout能力证据。成功分母、预测来源、因果语义与执行证据完全不同。

    **教学例子：** 教学例：给定三个数并选最大比值，不会让机器人到达goal，也不会让用户12周后更健康；两类后果都要独立验证。

    对照来源：[sensorwm-planning](../../../multimodal-models/2611.08568-sensorwm-planning/README.md) · [lewam](../../../reproductions/2610.12818-lewam/README.md)

### 把WOVEN的视频生成器替换成PixVid，能直接说状态推理更强吗？ {#cross-nov15-pixvid}

??? note "展开答案与例子"

    **答案：** 不能。需先测生成对动作和状态的忠实度，再用冻结数据协议训练/评测下游模型；画面更清晰只覆盖一个轴。本轮没有执行这样的组合。

    **教学例子：** 更清晰地生成一个错误动作结果，仍会把错误监督传给下游转移问答。

    对照来源：[pixvid](../../../multimodal-models/2611.17336-pixvid/README.md) · [woven](../../../reproductions/2610.12417-woven/README.md)

### WOVEN训练后某旧场景题准确率下降，能据此断言发生有害遗忘吗？ {#cross-nov18-stratified-retention-protocol}

??? note "展开答案与例子"

    **答案：** 不能。先判断旧答案是否仍真实；正确修订过期实例与忘掉不变量应分开。WOVEN现有分组accuracy也不提供逐轮差分保持证据，需要额外稳定面板、新episode变化查询和假修订对照。

    **教学例子：** 椅子移动后不再选旧坐标可能是好事；若遮挡后认为椅子不存在才违反稳定知识。最终恢复正确也不能掩盖中途一次负翻转。

    对照来源：[stratified-retention-protocol](../../../foundation-models/2610.03713-stratified-retention-protocol/README.md) · [woven](../../../reproductions/2610.12417-woven/README.md)

### 用昨天新拍的同一停车场替换一个场景，是否同时完成了freshness和scene-OOD评测？ {#cross-nov18-rslivebench-uav-protocol}

??? note "展开答案与例子"

    **答案：** 不一定。可满足capture时窗与FIFO，但若地点、实体和视角类似，未必形成未见场景泛化。WOVEN的scene轴和UAV持续时间控制需各自按协议记录。

    **教学例子：** 新拍同一停车场可算新观察；一个从未见过的生成餐厅可算场景OOD，却不代表真实UAV跨视角车辆几何。

    对照来源：[rslivebench-uav-protocol](../../../multimodal-models/2611.14953-rslivebench-uav-protocol/README.md) · [woven](../../../reproductions/2610.12417-woven/README.md)

### WM-Quant与LeWAM都用JEPA rollout，是否说明本轮已经量化验证了LeWAM？ {#cross-nov18-wm-quant}

??? note "展开答案与例子"

    **答案：** 不是。WM-Quant论文评测LeWM/DINO-WM，LeWAM是另一套联合世界—动作模型。本地仅验证量化格点、跨步范围目标与控制保留，没有接入LeWAM模型、CEM或机器人环境。

    **教学例子：** 教学例：LeWAM的三臂机器人结果不能替代WM-Quant的低比特规划评测；一个校准loss也不能证明LeWAM规划能力。

    对照来源：[wm-quant](../../../foundation-models/2611.21882-wm-quant/README.md) · [lewam](../../../reproductions/2610.12818-lewam/README.md)

### 和PixVid都去掉decoder，有何关键不同？ {#cross-nov18-dwd}

??? note "展开答案与例子"

    **答案：** PixVid迁移输入与整个pixel生成路径，DWD保留latent denoising加最终输出head；改动范围和监督不同。

    **教学例子：** 删除VAE后直接换线性输出，不会自动获得PixVid的时间映射/detailer。

    对照来源：[dwd](../../../multimodal-models/2611.22287-dwd/README.md) · [pixvid](../../../multimodal-models/2611.17336-pixvid/README.md)

### 与DT-JEPA查询时的信息有什么不同？ {#cross-nov19-counterfactual-wm}

??? note "展开答案与例子"

    **答案：** DT-JEPA用行动前历史预测未来；CWM需已执行事实动作的结果。允许的信息集和问题不同，不能比较为同一预测任务。

    **教学例子：** 教学例：第一次执行动作前不能拿尚不存在的observed_outcome喂CWM。

    对照来源：[counterfactual-wm](../../../foundation-models/2611.24778-counterfactual-wm/README.md) · [dt-jepa](../../../foundation-models/2610.32657-dt-jepa/README.md)

### 场景重访一致是否等于CWM的反事实能力？ {#cross-nov19-autoregressive-view-model}

??? note "展开答案与例子"

    **答案：** 不等于。重访是在相机轨迹和生成历史下维持场景；个体反事实还需同一扰动下不同动作结果的耦合假设。

    **教学例子：** 教学例：门框位置保持不变，不能说明同一阵风下船改航向会到哪里。

    对照来源：[autoregressive-view-model](../../../multimodal-models/2611.23417-autoregressive-view-model/README.md) · [counterfactual-wm](../../../foundation-models/2611.24778-counterfactual-wm/README.md)

### 与LeWAM的world-action联学相比，部署差异是什么？ {#cross-nov19-jepa-dots}

??? note "展开答案与例子"

    **答案：** JEPA Dots world分支只供训练监督，部署执行flow policy；不能因此说它已复现LeWAM通过world模型优化动作的规划链。

    **教学例子：** 教学例：生成8步动作后执行2步再观测，是receding-horizon policy，不等于对world cost做梯度规划。

    对照来源：[jepa-dots](../../../multimodal-models/2611.24062-jepa-dots/README.md) · [lewam](../../../reproductions/2610.12818-lewam/README.md)

### MV-JEPA和Time-JEPA都用额外监督，目标能互换吗？ {#cross-nov21-mv-jepa}

??? note "展开答案与例子"

    **答案：** 不能。前者是跨摄像头latent并需要联合view predictor；后者是对齐物理时序并有unmasked回归分支。二者训练目标都不应变成student输入。

    **教学例子：** 教学例：速度标量属于Time-JEPA物理head，背面视图的一组token属于MV-JEPA held-out query；换标签不等于同一任务。

    对照来源：[mv-jepa](../../../foundation-models/2611.25172-mv-jepa/README.md) · [time-jepa](../../../foundation-models/2610.23982-time-jepa/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-11-21** · Time-JEPA用物理时序作额外训练目标，在同一online encoder上执行masked潜变量预测和unmasked物理态回归；MV-JEPA用另一个摄像头的latent作held-out目标，并让联合predictor从多个独立context视图推断。两者都不能把训练目标喂回推理输入，但MV-JEPA的跨view query不是Time-JEPA的传感器head；重放保持表征和物理时序对齐也是不同验收。 本地组件证据与完整实验不复现分开记录。

涉及：[mv-jepa](../../../foundation-models/2611.25172-mv-jepa/README.md) · [time-jepa](../../../foundation-models/2610.23982-time-jepa/README.md)

**2026-11-19** · LeWAM联合world/action并用预测模型规划；JEPA Dots强调语言目标与动力学给定动作输入的隔离，部署world分支不参与动作搜索。相同masked-MoT背景不代表推理链相同。 高成本完整实验不复现，组件与能力证据分开。

涉及：[jepa-dots](../../../multimodal-models/2611.24062-jepa-dots/README.md) · [lewam](../../../reproductions/2610.12818-lewam/README.md)

**2026-11-19** · CWM在一个事实事件之后改变动作并复用同一扰动残差；AVM沿相机轨迹继续生成并检索历史视图。二者都使用world model语汇，但AVM的场景重访一致性不证明同一扰动反事实可识别。 本地组件合同和高成本不复现分别记录。

涉及：[autoregressive-view-model](../../../multimodal-models/2611.23417-autoregressive-view-model/README.md) · [counterfactual-wm](../../../foundation-models/2611.24778-counterfactual-wm/README.md)

**2026-11-19** · DT-JEPA在历史下预测未来latent分布并用于决策，真实未来只在训练目标出现；CWM在一个事实结果已经可见后推断同一事件的替代动作结果。不能让CWM提前使用尚未观测的未来，亦不能把DT-JEPA的均值直接称个体反事实。 本地组件合同和高成本不复现分别记录。

涉及：[counterfactual-wm](../../../foundation-models/2611.24778-counterfactual-wm/README.md) · [dt-jepa](../../../foundation-models/2610.32657-dt-jepa/README.md)

**2026-11-18** · PixVid迁移latent DiT到pixel输入/生成空间并加detailer；DWD保留latent采样，只改变最终读出。输出是像素不意味着整个采样都在pixel空间。 本地边界与完整高成本不复现分别记录。

涉及：[dwd](../../../multimodal-models/2611.22287-dwd/README.md) · [pixvid](../../../multimodal-models/2611.17336-pixvid/README.md)

**2026-11-18** · LeWAM联合训练视觉encoder、latent动力学与action flow，再对策略候选做潜空间规划；WM-Quant研究连续rollout中的量化误差与范围校准。注意新论文实验对象是LeWM/DINO-WM，不是LeWAM，未声称把WM-Quant接入了LeWAM训练或规划。 本次实读已有同主题代表README，按真实研究轴比较，不借比较对象改变算法或宣称跨论文效果复现。

涉及：[wm-quant](../../../foundation-models/2611.21882-wm-quant/README.md) · [lewam](../../../reproductions/2610.12818-lewam/README.md)

**2026-11-18** · 补入RSLiveBench-UAV的L0发布/scorer协议，与WOVEN场景迁移分开；完整采集、标注和30模型高成本矩阵不复现。

涉及：[rslivebench-uav-protocol](../../../multimodal-models/2611.14953-rslivebench-uav-protocol/README.md) · [woven](../../../reproductions/2610.12417-woven/README.md)

**2026-11-18** · 补入分层保持的L0报告协议，与WOVEN视觉转移训练分轴比较；无原始完整实证，不虚构高成本训练或能力排名。

涉及：[stratified-retention-protocol](../../../foundation-models/2610.03713-stratified-retention-protocol/README.md) · [woven](../../../reproductions/2610.12417-woven/README.md)

**2026-11-15** · 补入固定版本方法、低成本组件或明确资料收录，分开原文结果、本地诊断及高成本不复现范围。

涉及：[pixvid](../../../multimodal-models/2611.17336-pixvid/README.md) · [woven](../../../reproductions/2610.12417-woven/README.md)

**2026-11-12** · 加入Google可穿戴世界模型案例，区分动作条件观察预测、个体努力候选排序与实际控制/因果健康收益。本地CPU三seed仅验证Eq55–56数学，完整私有JEPA与临床/API实验高成本不复现。

涉及：[sensorwm-planning](../../../multimodal-models/2611.08568-sensorwm-planning/README.md) · [lewam](../../../reproductions/2610.12818-lewam/README.md)

**2026-11-12** · 补入从JEPA时空先验提取动作的对比适配，明确场景检索与动作场景解耦目标差异；A100三seed只验证精确bank/冻结投影/梯度，完整视频训练不复现。

涉及：[onlyact](../../../multimodal-models/2611.14420-onlyact/README.md)

**2026-11-11** · 加入RS-JEPA，区分扫描视图/对抗划分/邻域一致性与V-JEPA Policy的未来动作闭环；明确同主干stop-gradient而非momentum target。仅L1 tensor机制，完整Vim/CVA/predictor和多数据集检索实验不复现。

涉及：[rs-jepa](../../../multimodal-models/2611.14496-rs-jepa/README.md) · [vjepa-policy](../../../foundation-models/2609.37250-vjepa-policy/README.md)

**2026-10-30** · 精读修正后的SWIM固定动作chunk与h分离、ungated当前state、cyclic负例、真实gate梯度及sqrt(g)几何迁移；与GUI-JEPA候选残差路径对照，不把训练未来状态当规划输入。

涉及：[swim](../../../foundation-models/2610.36662-swim/README.md) · [gui-jepa](../../../foundation-models/2610.36877-gui-jepa/README.md)

**2026-10-29** · GUI-JEPA在当前屏幕latent上预测候选动作导致的残差后继，并结合动作ROI/global区域和结构余弦评分。它与像素视频生成的监督/输出不同，也不等于真实GUI执行器；当前组件接外部冻结latent和文本匹配分数，保留真实三层predictor与训练头，但不使用训练正样本标签替forward选动作。

涉及：[gui-jepa](../../../foundation-models/2610.36877-gui-jepa/README.md)

**2026-10-27** · 首版：比较联合或冻结视觉编码的动作模型、预测与规划验收、WOVEN转移监督、PPMem几何记忆与VBVR程序评分；已阅22篇摘要，精读6篇。

覆盖 22 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 36 篇资料</summary>

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
- [SWIM: Learning What Matters from Behaviors for JEPA World Models](../../../foundation-models/2610.36662-swim/README.md)
- [RS-JEPA: Remote Sensing Joint-Embedding Predictive Architecture with Scan-Path Views for Cross-Sensor Image Retrieval](../../../multimodal-models/2611.14496-rs-jepa/README.md)
- [OnlyAct: Extracting Action Representations from Foundation Models for World Models](../../../multimodal-models/2611.14420-onlyact/README.md)
- [Personalized health coaching via coachable health age and counterfactual wearable trajectories](../../../multimodal-models/2611.08568-sensorwm-planning/README.md)
- [Back to Pixels: Lifting Latent Video Diffusion into Pixel Space](../../../multimodal-models/2611.17336-pixvid/README.md)
- [What Should World Models Forget? Stratified Retention for Continual Adaptation](../../../foundation-models/2610.03713-stratified-retention-protocol/README.md)
- [RSLiveBench-UAV: A Continually Evolving Vision-Language Benchmark for Aerial Spatial Intelligence](../../../multimodal-models/2611.14953-rslivebench-uav-protocol/README.md)
- [WM-Quant: Rollout-Aware Post-Training Quantization for JEPA-Style World Models](../../../foundation-models/2611.21882-wm-quant/README.md)
- [Decoding Without a Decoder: Direct Pixel Prediction from Diffusion Transformers](../../../multimodal-models/2611.22287-dwd/README.md)
- [Counterfactual World Models: JEPAs That Reason About &quot;What If&quot;](../../../foundation-models/2611.24778-counterfactual-wm/README.md)
- [Autoregressive View Model](../../../multimodal-models/2611.23417-autoregressive-view-model/README.md)
- [JEPA Dots: Dual-Latent World Model for Language-Guided Robot Control](../../../multimodal-models/2611.24062-jepa-dots/README.md)
- [MV-JEPA: Post-Training Video Encoders for Cross-View Understanding](../../../foundation-models/2611.25172-mv-jepa/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/multimodal-models/world-state-actions.md) · [返回全部精读卡片](../index.md)
