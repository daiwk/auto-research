---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 从更便宜的一次前向，到可验证的长期研究闭环

[搜广推](../index.md) · 更新 2026-11-20 · 23 篇主题资料 / 9 篇重点对照

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
| [CutAgent: Creative-Gene-Driven Planning and Experience-Guided Self-Refinement for High-CTR E-commerce Advertising Video Creation](../../../recommendation-components/2611.22418-cutagent/README.md) · [原始来源](https://arxiv.org/abs/2611.22418v1)<br>章节：背景与主要改动、核心公式、同主题对照、高成本完整实验 | CutAgent把多模态商品理解与可靠视频制作拆为GeneAgent和VideoAgent，以结构化creative gene连接。Gene规定narrative units和配音／音乐／脚本规则；前者经高CTR SFT和CTR-level GRPO学习规划，后者展开分镜并检索商品素材、做TTS/BGM和渲染，再只修复带时间证据的缺陷。 | AgenticRecTune把推荐系统配置方案经实验平台反馈沉淀到SkillHub，CutAgent把广告制作失败修复写成类目／gene条件经验。二者都复用执行经验，但优化对象、反馈和测试权限不同；本篇的LightGBM surrogate不是推荐实验平台，也不能替代真实线上随机分流证据。 |
| [MLE Agents: Autonomous ML Engineering in Large-scale Recommendation Systems](../../../recommendation-components/2611.23910-mle-agents/README.md) · [原始来源](https://arxiv.org/abs/2611.23910v1)<br>章节：背景与主要改动、核心公式、同主题对照 | Meta把提假设、改代码、训练和读指标组成有人监督的模型研发循环。2.0每轮名义上并行七个候选和一个方差探针，使用与线上影响校准过的加权NE，而不是只追逐点击AUPRC。失败块名单、结构化输出和只回传近期未采纳赢家控制上下文陈旧；最终模型仍由工程师审核并独立做线上实验。 | EvoPilot先锁定控制/实验两臂的比较合同并拒绝不匹配证据；MLE Agents强调搜索目标与同轮噪声探针。二者都不让“训练结束”自动成为可发布结论，目标校准也不能取代EvoPilot的产物一致性检查。 |
| [MARS Technical Report](../../../recommendation-components/2611.24006-mars-fapo/README.md) · [原始来源](https://arxiv.org/abs/2611.24006v1)<br>章节：背景与主要改动、核心公式、同主题对照 | MARS让近线0.6B策略为用户产生跨召回、粗排、精排和重排的七维配置，经校验后缓存，在线始终不等待LLM。SFT建立合法格式，FAPO把偏好比较集中到实际不同的动作值token，最后GRPO在沙箱回放和冻结奖励模型上继续优化。正文版权行为Taobao，贡献者按名字母排序，不虚构个人一作机构。 | EvoPilot校验模型开发实验的两臂证据，MARS生成和训练线上流水线配置。MARS的缓存/fallback是服务安全，不能替代开发比较合同；ActionMask loss也不能证明策略已经能生成合法或优质配置。 |
| [Cost-Aware Agentic Feature Optimization System for Fleet-Scale Ranking Models](../../../recommendation-components/2611.26531-fleet-feature-optimization/README.md) · [原始来源](https://arxiv.org/abs/2611.26531v1)<br>章节：背景与主要改动、核心公式、同主题比较与边界 | Meta把特征创建、FI估计、跨任务Pareto分层、多来源混合和有约束搜索连成fleet级流程。LLM提出假设，确定性工具验证；每个模型同时面对自身serving限制和跨模型共享的上游pipeline预算。另一个模型已经使用某特征时，新增使用不一定新增pipeline成本。 | MLE Agents用同轮方差探针对候选研发做目标准入；Fleet侧重特征共享成本与serving可行性。低NE不能覆盖资源超限，低成本也不能绕过NE必须优于基线的准入。两者诊断接口都不能自行证明模型研发或线上收益。 |

</div>

## 取舍分析 {#analysis}

### 先给成本记上正确的账

ROCS把同请求多候选共享编码，节省在线重复工作；Rec-Distill把大模型影响移入训练再部署轻main tower，可能增加训练工作。ETT统计训练端到端真正推进新数据的比例，既不测请求时延，也不等同设备利用率。三种指标可同时改善或互相权衡，必须记录优化发生在哪个阶段。

对照来源：[rocs](../../../reproductions/2607.27744-rocs/README.md) · [rec-distill](../../../reproductions/2605.29755-rec-distill/README.md) · [effective-training-time](../../../reproductions/2610.02057-effective-training-time/README.md)

### 自动研究必须学会接受“不改”

FORTE把成本节省的提案放进多道质量与血缘门槛，本地无候选通过后保留原模型是有效结论。Self-Evolving RecSys的外层状态机同样不能把内层成功跑完当成可上线；ETT也提醒把失败恢复和重复开销算进生命周期。长期记忆应保存失败原因、预算和消费者边界，而非只积累宣称成功的方案名。

对照来源：[forte](../../../reproductions/2610.13806-forte/README.md) · [self-evolving-rec](../../../reproductions/2602.10226-self-evolving-rec/README.md) · [effective-training-time](../../../reproductions/2610.02057-effective-training-time/README.md)

### CutAgent：以创意基因连接广告规划、制作与经验反思：区别机制与能力

GeneAgent采用Qwen3-VL-8B，冻结视觉模块、仅语言LoRA；SFT取观测CTR前20%，GRPO每商品采8个gene。LightGBM按类目内Low/Mid/High预测CTR-level，仅是训练奖励，不充当线上CTR。VideoAgent先按43类目选memory shard，再用gene相似度取已验证failure-correction作为制作约束；memory不是商品clip pool，反思不能用固定模板成功代替。 AgenticRecTune把推荐系统配置方案经实验平台反馈沉淀到SkillHub，CutAgent把广告制作失败修复写成类目／gene条件经验。二者都复用执行经验，但优化对象、反馈和测试权限不同；本篇的LightGBM surrogate不是推荐实验平台，也不能替代真实线上随机分流证据。

对照来源：[cutagent](../../../recommendation-components/2611.22418-cutagent/README.md) · [agentic-rec-tune](../../../reproductions/2604.26969-agentic-rec-tune/README.md)

### MLE Agents：工业精排的目标校准与方差探针准入：机制和证据边界

§1.2给出0.3/0.7目标，§3.5明确与同轮variance probe比较，而不是任意旧基线。完成状态须有两条独立信号；一候选只改一项连贯机制。阈值来自历史噪声探针，不能把0.0005说成显著性检验或跨数据通用常数。接口返回离线搜索接纳和仍需人工审核，不发起训练或生产发布。 EvoPilot先锁定控制/实验两臂的比较合同并拒绝不匹配证据；MLE Agents强调搜索目标与同轮噪声探针。二者都不让“训练结束”自动成为可发布结论，目标校准也不能取代EvoPilot的产物一致性检查。

对照来源：[mle-agents](../../../recommendation-components/2611.23910-mle-agents/README.md) · [evopilot](../../../reproductions/2609.21257-evopilot/README.md)

### MARS：近线推荐编排与ActionMask偏好优化：机制和证据边界

Eq11–13保留全chosen回答的生成anchor，只有偏好项乘clip(1+2(p+−p−)/p均值,0.2,3)。缺失任一历史V2P时权重为1。只有弱证据且达到相对gap才允许反转chosen/rejected；强证据不反转。动作mask由可信的字段值span/token对齐层提供，必须包含完整变化值而非共享JSON结构；不以脆弱字符串搜索冒充原tokenizer。历史配置V2P是观察统计，不是因果后验。 EvoPilot校验模型开发实验的两臂证据，MARS生成和训练线上流水线配置。MARS的缓存/fallback是服务安全，不能替代开发比较合同；ActionMask loss也不能证明策略已经能生成合法或优质配置。

对照来源：[mars-fapo](../../../recommendation-components/2611.24006-mars-fapo/README.md) · [evopilot](../../../reproductions/2609.21257-evopilot/README.md)

### Cost-Aware Agentic Feature Optimization System for Fleet-Scale Ranking Models

MLE Agents用同轮方差探针对候选研发做目标准入；Fleet侧重特征共享成本与serving可行性。低NE不能覆盖资源超限，低成本也不能绕过NE必须优于基线的准入。两者诊断接口都不能自行证明模型研发或线上收益。 FI向量按所有任务的逐维支配关系分层，不先把任务loss相加。多个来源固定顺序取未选特征，论文写round(pi_m N)，却没有规定舍入与末层同分切分；本地将整数quota及层内顺序显式交给调用方。成本使用完整特征集合oracle，不把共享成本猜成各特征价格求和；跨预算的最贵删除顺序也由外部提供。QPS约束必须先变换成1/QPS这种上界口径。

对照来源：[fleet-feature-optimization](../../../recommendation-components/2611.26531-fleet-feature-optimization/README.md) · [mle-agents](../../../recommendation-components/2611.23910-mle-agents/README.md)

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

### CutAgent memory与AgenticRecTune SkillHub一样吗？ {#cross-cross-nov18-latest-cutagent}

??? note "展开答案与例子"

    **答案：** 复用思路相近但前者保存类目／gene条件的制作缺陷修复，后者保存配置实验经验。

    **教学例子：** 教学例：减少开场重复近景不能直接变成推荐融合权重。

    对照来源：[cutagent](../../../recommendation-components/2611.22418-cutagent/README.md) · [agentic-rec-tune](../../../reproductions/2604.26969-agentic-rec-tune/README.md)

### MLE Agents和EvoPilot的准入能互代吗？ {#cross-cross-nov19-mle-agents}

??? note "展开答案与例子"

    **答案：** 不能。前者校准目标/训练噪声，后者核对两臂实验与产物；都还需要最终人工和线上确认。

    **教学例子：** 教学例：数据版本不同的两臂即使NE差够大，也不能用噪声门槛盖过协议失败。

    对照来源：[mle-agents](../../../recommendation-components/2611.23910-mle-agents/README.md) · [evopilot](../../../reproductions/2609.21257-evopilot/README.md)

### MARS和EvoPilot都是Agent，有什么根本区别？ {#cross-cross-nov19-mars-fapo}

??? note "展开答案与例子"

    **答案：** MARS训练用户流水线动作；EvoPilot审核模型开发比较证据。配置格式合法不等于实验结论可信。

    **教学例子：** 教学例：合法Minimal动作不能代替控制/实验模型的数据版本核对。

    对照来源：[mars-fapo](../../../recommendation-components/2611.24006-mars-fapo/README.md) · [evopilot](../../../reproductions/2609.21257-evopilot/README.md)

### 与MLE Agents的方差探针准入相比，本篇多了什么限制？ {#cross-nov20-fleet-feature-optimization}

??? note "展开答案与例子"

    **答案：** 本篇显式处理每模型资源上界和fleet共享pipeline预算；离线NE更好也不能接受超预算trial。它没有替代MLE Agents的同轮噪声参照。

    **教学例子：** 教学例：NE0.1但inverse-QPS超cap的候选必须让位于NE0.6且可行的候选。

    对照来源：[fleet-feature-optimization](../../../recommendation-components/2611.26531-fleet-feature-optimization/README.md) · [mle-agents](../../../recommendation-components/2611.23910-mle-agents/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-11-20** · MLE Agents用同轮方差探针对候选研发做目标准入；Fleet侧重特征共享成本与serving可行性。低NE不能覆盖资源超限，低成本也不能绕过NE必须优于基线的准入。两者诊断接口都不能自行证明模型研发或线上收益。 原文线上证据与本地合同分开记录。

涉及：[fleet-feature-optimization](../../../recommendation-components/2611.26531-fleet-feature-optimization/README.md) · [mle-agents](../../../recommendation-components/2611.23910-mle-agents/README.md)

**2026-11-19** · 本地只实现posterior启发式权重、弱证据翻转规则与FAPO张量损失；没有0.6B生成、字段tokenizer、SFT/GRPO、Sandbox、奖励模型、iGraph缓存或实时推荐。结构token仍有生成梯度，rejected非动作token没有偏好梯度。 完整高成本实验不复现，审查DONE。

涉及：[mars-fapo](../../../recommendation-components/2611.24006-mars-fapo/README.md) · [evopilot](../../../reproductions/2609.21257-evopilot/README.md)

**2026-11-19** · 本地只执行目标与完成/准入接口。没有运行Claude研究调用、候选代码生成、私有数据分布式训练或线上A/B，也没有新增可执行Evolve搜索策略。合成输入不代表Meta模型指标。 完整高成本实验不复现，审查DONE。

涉及：[mle-agents](../../../recommendation-components/2611.23910-mle-agents/README.md) · [evopilot](../../../reproductions/2609.21257-evopilot/README.md)

**2026-11-18** · 本篇review-only，完整实验成本过高，不复现（审查DONE）。70K商品每件90–120clips、多模态teacher、8B训练／检索、TTS与渲染、397Bjudge及真实流量均未运行；不下载资源，不编造creative-gene规划器、素材检索或本地CTR。固定v1没有核实本篇作者仓库，FireRed等第三方baseline代码不算CutAgent开源。 完整实验高成本不复现，未作能力或Evolve晋级证据。

涉及：[cutagent](../../../recommendation-components/2611.22418-cutagent/README.md) · [agentic-rec-tune](../../../reproductions/2604.26969-agentic-rec-tune/README.md)

**2026-10-27** · 首版：比较rocs、rec-distill、effective-training-time、forte、self-evolving-rec，围绕成本属于训练、请求内推理还是长期研发生命周期与复用与删除要求哪些依赖/消费者保持一致建立分析和跨论文问答。

覆盖 19 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 23 篇资料</summary>

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
- [CutAgent: Creative-Gene-Driven Planning and Experience-Guided Self-Refinement for High-CTR E-commerce Advertising Video Creation](../../../recommendation-components/2611.22418-cutagent/README.md)
- [MLE Agents: Autonomous ML Engineering in Large-scale Recommendation Systems](../../../recommendation-components/2611.23910-mle-agents/README.md)
- [MARS Technical Report](../../../recommendation-components/2611.24006-mars-fapo/README.md)
- [Cost-Aware Agentic Feature Optimization System for Fleet-Scale Ranking Models](../../../recommendation-components/2611.26531-fleet-feature-optimization/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/recommendation/research-serving-loop.md) · [返回全部精读卡片](../index.md)
