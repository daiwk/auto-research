---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 从更便宜的一次前向，到可验证的长期研究闭环

[搜广推](../index.md) · 更新 2026-10-27 · 19 篇主题资料 / 5 篇重点对照

ROCS减少请求内重复计算，Rec-Distill将昂贵教师知识移到训练，Effective Training Time追踪训练生命周期损耗，FORTE控制特征退役风险，Self-Evolving RecSys把提案、实验和线上反馈接成长期循环。它们优化的时间尺度不同；省GPU、删特征和自动提出方案，都不能直接当作推荐效果提升。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/recommendation/research-serving-loop.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：成本属于训练、请求内推理还是长期研发生命周期 · 复用与删除要求哪些依赖/消费者保持一致 · 离线门槛、重训和真实线上反馈如何衔接 · 负结果与未通过门槛如何进入后续决策

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [ROCS: Request-Oriented Compute Sharing for Efficient Large-Scale Recommendation](../../../reproductions/2607.27744-rocs/README.md) · [原始来源](https://arxiv.org/abs/2607.27744)<br>章节：背景与主要改动、核心公式、复现边界 | 保持候选隔离，用户请求编码一次，以延迟DCA交互评分候选；生产IKBO在kernel内广播request表示。 | 共享收益以用户表示不依赖具体候选为条件；本地未复刻GLM/IKBO CUDA kernel及生产集群，解析复用不能换算成真实吞吐。 |
| [Rec-Distill: An Industrial Distillation Pipeline for Large-Scale Recommendation Models](../../../reproductions/2605.29755-rec-distill/README.md) · [原始来源](https://arxiv.org/abs/2605.29755)<br>章节：背景与主要改动、核心公式、本地复现 | teacher自身前向物化raw logits，学生侧作采样校正；main tower只收真标签并服务，aux tower承担task+distill并共享backbone。 | 训练期多付教师/辅助塔成本以降低部署负担，但教师更强不等于学生必受益；teacher/student概率空间要先对齐，需与同预算学生比较。 |
| [Optimizing Effective Training Time for Large-Scale Recommendation Systems](../../../reproductions/2610.02057-effective-training-time/README.md) · [原始来源](https://arxiv.org/abs/2610.02057)<br>章节：背景与主要改动、核心公式、复现边界 | 以消费新数据的训练时间除端到端wall time，按初始化、编译、checkpoint、发布和恢复等阶段归因损耗。 | 提高ETT不等于提升模型准确率，也不同于GPU忙碌率；本地是生命周期分解与owner归因组件，不是推荐模型能力实验。 |
| [FORTE: A Production Framework for Feature Evaluation and Deprecation in Industrial Recommender Systems](../../../reproductions/2610.13806-forte/README.md) · [原始来源](https://arxiv.org/abs/2610.13806)<br>章节：背景与主要改动、核心公式、复现边界 | 冻结模型扰动依赖，经所有头/时间窗筛选，再联合消融、真实重训、线上实验与所有消费者血缘审计逐级退役特征。 | 单特征弱依赖不能相加推导联合安全；本地A100三种子没有候选通过全部门槛，最终保留基线，流程完成不等于删除带来收益。 |
| [Self-Evolving Recommendation System: End-To-End Autonomous Model Optimization With LLM Agents](../../../reproductions/2602.10226-self-evolving-rec/README.md) · [原始来源](https://arxiv.org/abs/2602.10226)<br>章节：背景与主要改动、核心公式、本地复现 | 内层研究agent提出optimizer/结构/reward并运行工具，外层状态机控制约束、离线门槛和真实A/B promotion，结论写回journal。 | 可执行试验与独立评价是闭环必要条件，提案或注册名称不是能力；原文生产反馈不能用本地小实验替代，也不能因agent主动探索跳过门槛。 |

</div>

## 取舍分析 {#analysis}

### 先给成本记上正确的账

ROCS把同请求多候选共享编码，节省在线重复工作；Rec-Distill把大模型影响移入训练再部署轻main tower，可能增加训练工作。ETT统计训练端到端真正推进新数据的比例，既不测请求时延，也不等同设备利用率。三种指标可同时改善或互相权衡，必须记录优化发生在哪个阶段。

对照来源：[rocs](../../../reproductions/2607.27744-rocs/README.md) · [rec-distill](../../../reproductions/2605.29755-rec-distill/README.md) · [effective-training-time](../../../reproductions/2610.02057-effective-training-time/README.md)

### 自动研究必须学会接受“不改”

FORTE把成本节省的提案放进多道质量与血缘门槛，本地无候选通过后保留原模型是有效结论。Self-Evolving RecSys的外层状态机同样不能把内层成功跑完当成可上线；ETT也提醒把失败恢复和重复开销算进生命周期。长期记忆应保存失败原因、预算和消费者边界，而非只积累宣称成功的方案名。

对照来源：[forte](../../../reproductions/2610.13806-forte/README.md) · [self-evolving-rec](../../../reproductions/2602.10226-self-evolving-rec/README.md) · [effective-training-time](../../../reproductions/2610.02057-effective-training-time/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### ROCS与Rec-Distill都降低在线成本，为什么二者节省的计算不能直接相加估算？ {#cross-sharing-versus-distillation}

??? note "展开答案与例子"

    **答案：** ROCS减少同一请求内可共享用户编码的重复，Rec-Distill改变部署模型并把教师/辅助塔留在训练。蒸馏后的结构可能改变原来能共享的比例，kernel和带宽也会影响时延。需要测组合后的实际链路，而非把两个独立加速数字相乘或相加。

    **教学例子：** 示意：学生已把用户编码缩得很轻，ROCS能省掉的重复部分就可能变小；反之teacher训练耗时增加，也不会体现在单次请求延迟里。

    对照来源：[rocs](../../../reproductions/2607.27744-rocs/README.md) · [rec-distill](../../../reproductions/2605.29755-rec-distill/README.md)

### GPU一直忙、ROCS单请求也更快，为什么训练的Effective Training Time仍可能很低？ {#cross-effective-time-versus-busy-time}

??? note "展开答案与例子"

    **答案：** ETT的分子是真正消费新数据的训练时间，分母含初始化、编译、checkpoint、发布和恢复。设备可能忙于这些阶段，ROCS又优化在线请求而非训练生命周期。要按阶段和owner定位损耗，不能用设备忙碌或推理时延替代ETT。

    **教学例子：** 示意：10小时wall time中8小时训练新数据、2小时编译与恢复，ETT为80%；即使那2小时GPU也满载，分子仍不是10小时。

    对照来源：[effective-training-time](../../../reproductions/2610.02057-effective-training-time/README.md) · [rocs](../../../reproductions/2607.27744-rocs/README.md)

### FORTE发现两个特征单独扰动都几乎无损，自动研究agent为什么不能直接一起删除？ {#cross-joint-removal-needs-new-evidence}

??? note "展开答案与例子"

    **答案：** 两个特征可能互为备份，单独破坏时另一条仍提供信号；联合删除会暴露非加性损失。FORTE因此还要联合消融、重训和所有消费者审计。Self-Evolving RecSys应把此提案送入实际门槛，用失败证据更新journal，而不是按两个单项结果推断安全。

    **教学例子：** 示意：品牌ID与文本品牌词都能识别品牌，单删任一个变化很小，同时删掉可能损伤某个稀疏任务；教学例子不代表论文某次实测。

    对照来源：[forte](../../../reproductions/2610.13806-forte/README.md) · [self-evolving-rec](../../../reproductions/2602.10226-self-evolving-rec/README.md)

### Rec-Distill学生的离线分数略高，研究agent把方案记进journal后就算完成上线闭环吗？ {#cross-research-memory-is-not-promotion}

??? note "展开答案与例子"

    **答案：** 不算。先核对学生采样校正、main/aux职责及同预算对照，确保提升不是协议变化；随后还需按Self-Evolving RecSys外层约束完成独立验证和适用的线上门槛。journal保存的是可复核试验与结论，不能替代执行证据或直接授予promotion。

    **教学例子：** 示意：学生换了负采样率后AUC变化，若教师logits仍在旧概率空间，先修协议再比较；记录一个“蒸馏成功”标题不能解决这个差异。

    对照来源：[rec-distill](../../../reproductions/2605.29755-rec-distill/README.md) · [self-evolving-rec](../../../reproductions/2602.10226-self-evolving-rec/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-27** · 首版：比较rocs、rec-distill、effective-training-time、forte、self-evolving-rec，围绕成本属于训练、请求内推理还是长期研发生命周期与复用与删除要求哪些依赖/消费者保持一致建立分析和跨论文问答。

覆盖 19 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 19 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [AgenticRecTune: Multi-Agent with Self-Evolving Skillhub for Recommendation System Optimization](../../../reproductions/2604.26969-agentic-rec-tune/README.md)
- [AutoLR: Automating the Path from Research to Launch Review in Industrial Recommender Systems](../../../reproductions/2609.04871-autolr/README.md)
- [CORAL: An LLM-Native Harness for Production Recommender Systems](../../../reproductions/2609.02730-coral/README.md)
- [Optimizing Effective Training Time for Large-Scale Recommendation Systems](../../../reproductions/2610.02057-effective-training-time/README.md)
- [Verify, Don&#x27;t Trust: Agentic Model Development for Video Discovery Retrieval at Scale](../../../reproductions/2609.21257-evopilot/README.md)
- [EvoRec: Self-Evolving Agentic Recommender Systems](../../../reproductions/2606.28368-evorec/README.md)
- [EvoSkillRec: Skill-Genome Evolution for Recommender Architecture Discovery](../../../reproductions/2609.34552-evoskillrec/README.md)
- [FORTE: A Production Framework for Feature Evaluation and Deprecation in Industrial Recommender Systems](../../../reproductions/2610.13806-forte/README.md)
- [Memory Layer: Train the In-Model Cache for Recommendation Models](../../../reproductions/2607.25110-memory-layer/README.md)
- [NOVA: A Verification-Aware Agent Harness for Architecture Evolution in Industrial Recommender Systems](../../../reproductions/2606.27243-nova/README.md)
- [Prompt Generation Technical Report](../../../reproductions/2607.11326-prompt-generation/README.md)
- [RADAR: Recall Augmentation through Deferred Asynchronous Retrieval](../../../reproductions/2506.07261-radar/README.md)
- [Rec-Distill: An Industrial Distillation Pipeline for Large-Scale Recommendation Models](../../../reproductions/2605.29755-rec-distill/README.md)
- [RecEvolve: A Knowledge-Driven Autonomous Agent System for Recommender Systems](../../../reproductions/2609.01622-recevolve/README.md)
- [RecHarness: A Bandit-Routed Agentic Harness for Self-Evolving Recommender Systems](../../../reproductions/2607.29241-recharness/README.md)
- [ROCS: Request-Oriented Compute Sharing for Efficient Large-Scale Recommendation](../../../reproductions/2607.27744-rocs/README.md)
- [Self-Evolving Recommendation System: End-To-End Autonomous Model Optimization With LLM Agents](../../../reproductions/2602.10226-self-evolving-rec/README.md)
- [SOLARIS: Speculative Offloading of Latent-bAsed Representation for Inference Scaling](../../../reproductions/2604.12110-solaris/README.md)
- [Compute Only Once: UG-Separation for Efficient Large Recommendation Models](../../../reproductions/2602.10455-ug-sep/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/recommendation/research-serving-loop.md) · [返回全部精读卡片](../index.md)
