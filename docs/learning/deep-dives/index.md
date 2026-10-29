---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 专题精读

围绕一个问题，把多篇论文放在一起比较：先读机制对照，再看取舍分析，最后用跨论文问答自测。

每个子主题维护一张卡片。新论文进入后，更新对应卡片的比较或结论，并记录这次变化；不必再从头读整批论文。

31 张精读卡片 · 1043 篇主题资料 · 按主题折叠

<details class="ar-deep-shelf"><summary>搜广推 · 7 张</summary>
<div class="ar-deep-grid">
<article class="ar-deep-tile">
<h2><a href="recommendation/retrieval-matching/">召回覆盖从哪里来：用户表示、正例组织与负例难度</a></h2>
<p>候选生成先决定后续排序能看见什么。YouTube DNN说明单用户向量如何进入近邻检索，Airbnb EBR把监督放回搜索—浏览—预订旅程，MIMA让同请求多正例分配给互补兴趣，MDCNS改变负例的难度与多视角监督。这四种改动分别作用于表示、标签、兴趣分工和梯度，不能用召回数变大统一解释。</p>
<p class="ar-learning-topic-meta">4 篇重点对照 · 3 个跨论文问答 · 2026-10-27</p>
</article>
<article class="ar-deep-tile">
<h2><a href="recommendation/content-semantic-ids/">知识、协同向量与语义码：相同内容怎样进入不同推荐接口？</a></h2>
<p>KAR生成外部知识后适配既有推荐器，NoteLLM用共读监督训练可检索压缩状态，Dual-purpose SID让短码兼顾身份与内容重建，FineSID则保留细粒度token和完整交互骨干做阶段迁移。它们不只是“都用LLM或SID”：对齐信号、压缩对象与下游继承内容各不相同。</p>
<p class="ar-learning-topic-meta">4 篇重点对照 · 3 个跨论文问答 · 2026-10-27</p>
</article>
<article class="ar-deep-tile">
<h2><a href="recommendation/history-ranking-backbones/">DIN、HSTU、LONGER、SlimPer、RankMixer：究竟让谁与谁交互？</a></h2>
<p>比较排序骨干前先画三条边：历史到历史、候选到历史、字段到字段。DIN按候选激活历史，HSTU在输入窗口内逐层改写历史状态，LONGER先合并再以短查询读长KV，SlimPer反复读取用户池但只传播小知识库，RankMixer则更换异构字段交互。它们可处于同一流水线的不同位置，不能按一个长度变量或一张本地结果表排总名次。</p>
<p class="ar-learning-topic-meta">5 篇重点对照 · 3 个跨论文问答 · 2026-10-27</p>
</article>
<article class="ar-deep-tile">
<h2><a href="recommendation/generative-retrieval-reasoning/">生成一个物品，先后跨过码本、模型分布与合法目录三道关</a></h2>
<p>TIGER把物品变成层次码并学习下一码序列，COBRA在稀疏码后补回条件稠密向量，PLUM把已有LLM通过继续预训练接到行为/SID空间。STATIC不改表示而改变合法解码的执行方式，Reward Guided Decoding则在既有支持上倾斜业务偏好。先定位改变的是哪一关，再判断它能否找回漏掉的物品。</p>
<p class="ar-learning-topic-meta">6 篇重点对照 · 4 个跨论文问答 · 2026-10-29</p>
</article>
<article class="ar-deep-tile">
<h2><a href="recommendation/feedback-multitask-causality/">从CTR到满意度与uplift：先定义监督对象，再决定怎样共享</a></h2>
<p>ESMM约束点击—转化漏斗概率，MMoE和PLE安排不同任务怎样共享专家，FLVM尝试把消费、主动参与和正负方向分开，Incrementality则比较采取与不采取动作的潜在结果。预测更多头、共享更多参数或拆出潜因子，都不自动解决因果识别。</p>
<p class="ar-learning-topic-meta">6 篇重点对照 · 4 个跨论文问答 · 2026-10-29</p>
</article>
<article class="ar-deep-tile">
<h2><a href="recommendation/slates-business-value/">好物品怎样组成好列表：边际价值、策略权重与约束</a></h2>
<p>CDM把相关性与去冗余的教师选择蒸馏给学生，SORT-Gen直接估计前缀条件下的列表边际价值，PRL-PUTS扫描多目标权重策略，Primal-Dual Decoding则在解码中根据约束松弛量更新乘子。它们分别改变列表上下文、效用模型、策略选择和约束控制，不能把多样性更高或某一目标更好当成全面胜出。</p>
<p class="ar-learning-topic-meta">4 篇重点对照 · 3 个跨论文问答 · 2026-10-27</p>
</article>
<article class="ar-deep-tile">
<h2><a href="recommendation/research-serving-loop/">从更便宜的一次前向，到可验证的长期研究闭环</a></h2>
<p>ROCS减少请求内重复计算，Rec-Distill将昂贵教师知识移到训练，Effective Training Time追踪训练生命周期损耗，FORTE控制特征退役风险，Self-Evolving RecSys把提案、实验和线上反馈接成长期循环。它们优化的时间尺度不同；省GPU、删特征和自动提出方案，都不能直接当作推荐效果提升。</p>
<p class="ar-learning-topic-meta">5 篇重点对照 · 4 个跨论文问答 · 2026-10-27</p>
</article>
</div></details>

<details class="ar-deep-shelf"><summary>基础模型 · 6 张</summary>
<div class="ar-deep-grid">
<article class="ar-deep-tile">
<h2><a href="foundation-models/context-and-state/">长上下文不是一条轴：位置、读取与状态压缩</a></h2>
<p>先问历史以什么形式存在，再问当前 token 怎样读它。RoPE 改变相对位置关系，Mamba 把历史写入递归状态，NSA 在多条读取路径间分工，OpenAttention 为未精读部分保留代理，TTR 则为当前输入求一个压缩表示。这些方法不能只按“支持多长”排成一列。</p>
<p class="ar-learning-topic-meta">7 篇重点对照 · 4 个跨论文问答 · 2026-10-29</p>
</article>
<article class="ar-deep-tile">
<h2><a href="foundation-models/conditional-compute/">按需算力：选择专家、跳过计算，还是查回旧知识</a></h2>
<p>参数容量、每 token 激活量与部署时延是三件事。Switch 选择计算专家，Engram 和 Memory Grafting 查局部模式；AdaDSF、Telescopic LM 与 WIDE 则分别从 token—层、整体深度和组宽度分配计算。先识别路由对象，才能讨论容量和省算。</p>
<p class="ar-learning-topic-meta">6 篇重点对照 · 3 个跨论文问答 · 2026-10-27</p>
</article>
<article class="ar-deep-tile">
<h2><a href="foundation-models/training-budget/">训练预算：改数据、改更新方向，还是改比较口径</a></h2>
<p>同一预算内训练得更好，可能来自更合适的数据、逐样本处理、更有效更新或更低状态开销。DoReMi、Mixing Laws、DataOrchestra、Muon 和 ECO 改动不同环节；Muon Paired Budget 则提醒先冻结选参规则，再分别回答等数据和等时间问题。</p>
<p class="ar-learning-topic-meta">6 篇重点对照 · 3 个跨论文问答 · 2026-10-27</p>
</article>
<article class="ar-deep-tile">
<h2><a href="foundation-models/compression-and-cache/">推理压缩先找瓶颈：权重、KV 内容与缓存层级</a></h2>
<p>AWQ 减权重位宽，GQA 减 KV 头，DropKV 与 TwinKV 改保留内容，KVMEM 管可执行历史视图，Remote KV Tiers 解决跨层级加载。它们可以组合，但不能用一个“压缩率”解释质量、可恢复性和端到端速度。</p>
<p class="ar-learning-topic-meta">8 篇重点对照 · 4 个跨论文问答 · 2026-10-29</p>
</article>
<article class="ar-deep-tile">
<h2><a href="foundation-models/generation-paths/">少做串行步骤：验证草稿与学习迭代不是同一条路</a></h2>
<p>推测解码用便宜提案换昂贵验证批次，精确校正可保持原 target 分布；扩散语言和数据空间迭代则改变生成轨迹或训练目标。比较时先问谁决定最终分布，再问每步做什么、跨步保留什么，以及 NFE 或接受长度能否转成真实时间收益。</p>
<p class="ar-learning-topic-meta">6 篇重点对照 · 3 个跨论文问答 · 2026-10-27</p>
</article>
<article class="ar-deep-tile">
<h2><a href="foundation-models/evaluation-and-evidence/">能力证据：准确打分、节省观测与解释预测</a></h2>
<p>先区分“正确答案怎样定义”“下一题测谁”“多个裁判怎样融合”和“预测怎样解释”。XLGoBench、ProEval、FUSE、TCAB 与 DetectorScope 分别改变这些环节；观测更少或解释可加，不等于被测能力本身更强。</p>
<p class="ar-learning-topic-meta">5 篇重点对照 · 3 个跨论文问答 · 2026-10-27</p>
</article>
</div></details>

<details class="ar-deep-shelf"><summary>结构化决策 · 3 张</summary>
<div class="ar-deep-grid">
<article class="ar-deep-tile">
<h2><a href="system-one/typed-readout/">同样输出候选分布，读出位置与缓存边界为何不同？</a></h2>
<p>类型化决策先把输出空间限定下来，但“无需生成长句”并不指定唯一架构。LLM2Jev读选项标签的语言概率，System One重排读首答案位置的候选字母，MJev-Spatial复用原生注意力Q/K，MetaEncoder则把请求和候选独立编码。先看打分依赖谁，再判断是否可缓存、能否开放检索，以及连续输出怎样离散化。</p>
<p class="ar-learning-topic-meta">4 篇重点对照 · 3 个跨论文问答 · 2026-10-27</p>
</article>
<article class="ar-deep-tile">
<h2><a href="system-one/candidate-invariance/">排序不变、概率校准与完整集合恢复，是三种不同承诺</a></h2>
<p>Prism-1约束分数的计算依赖，JEV请求审计设计配对干预，多正确选项审计检查分布能否恢复正确集合。三者分别回答“架构保证什么”“实验改变了什么”“评价目标是什么”，不能用合法输出或一次top-1准确率代替。</p>
<p class="ar-learning-topic-meta">3 篇重点对照 · 3 个跨论文问答 · 2026-10-27</p>
</article>
<article class="ar-deep-tile">
<h2><a href="system-one/adaptive-decisions/">追加推理、跨语言路由与持续反馈，各在哪个时刻改变决策？</a></h2>
<p>按需决策有三条时间轴：Selective Reasoning在单题内分配推理和读取预算，跨语言级联在不同后端间分配请求，Jev-DLC用已发生反馈影响后续请求。能力评测提供基线边界，却不自动证明任何控制策略有效。所有选择都要在当前测试目标揭晓之前冻结或作出。</p>
<p class="ar-learning-topic-meta">4 篇重点对照 · 3 个跨论文问答 · 2026-10-27</p>
</article>
</div></details>

<details class="ar-deep-shelf"><summary>多模态 · 3 张</summary>
<div class="ar-deep-grid">
<article class="ar-deep-tile">
<h2><a href="multimodal-models/alignment-interfaces/">多模态对齐到底对齐什么：向量、视觉接口还是证据依赖</a></h2>
<p>CLIP与EmbeddingGemma 2产出可比较向量，BLIP-2与LLaVA连接视觉到条件生成，CV-OPD训练证据依赖，UMRM给回答评分。它们的输出合同和监督对象不同，不是同一条从小到大的能力排行榜。</p>
<p class="ar-learning-topic-meta">6 篇重点对照 · 4 个跨论文问答 · 2026-10-29</p>
</article>
<article class="ar-deep-tile">
<h2><a href="multimodal-models/visual-evidence-budget/">少看、晚看还是再看：把视觉预算放到正确阶段</a></h2>
<p>视觉预算不只有token数。StackTok选择已编码证据，PACE提前分配输入分辨率，ViMoD保留可恢复细节，Frames-on-Demand按需取帧，AdaLoop多算已有视觉状态，OmniKVQuant减少每份cache的位宽。必须同时追踪信息是否还在、哪段成本已支付。</p>
<p class="ar-learning-topic-meta">6 篇重点对照 · 3 个跨论文问答 · 2026-10-27</p>
</article>
<article class="ar-deep-tile">
<h2><a href="multimodal-models/world-state-actions/">会预测下一幕，还不等于会行动或保持同一个世界</a></h2>
<p>世界模型需要分别回答：状态表征保留什么、动作如何影响未来、计划怎样被验收、跨段记忆如何维持。LeWAM与V-JEPA Policy连接预测和动作，预测—规划评测拆解误差，WOVEN提供视觉转移监督，PPMem维护几何记忆，VBVR-Pro定义可执行验收。</p>
<p class="ar-learning-topic-meta">7 篇重点对照 · 4 个跨论文问答 · 2026-10-29</p>
</article>
</div></details>

<details class="ar-deep-shelf"><summary>LLM 后训练 · 6 张</summary>
<div class="ar-deep-grid">
<article class="ar-deep-tile">
<h2><a href="post-training/preference-and-alignment/">偏好不是一个分数：先确定反馈格式，再选对齐目标</a></h2>
<p>DPO、KTO、SimPO、ORPO和IPO主要改变“怎样使用反馈”，CleanRM先处理“反馈是否可信”。参考模型、长度归一化、有限间隔和噪声校正是不同设计轴，不能因都在扩大好坏回答差异就当成同一方法。</p>
<p class="ar-learning-topic-meta">6 篇重点对照 · 3 个跨论文问答 · 2026-10-27</p>
</article>
<article class="ar-deep-tile">
<h2><a href="post-training/policy-optimization/">同一个GRPO名字之外：优势尺度、裁剪单位与训推失配</a></h2>
<p>GRPO家族的差别可拆成三问：奖励怎样变成优势、哪种概率比被裁剪、样本到底由哪个分布生成。Dr. GRPO、DAPO、GSPO与TIS/IcePop分别改动这些环节，不能把所有ratio都叫同一种off-policy校正。</p>
<p class="ar-learning-topic-meta">6 篇重点对照 · 3 个跨论文问答 · 2026-10-27</p>
</article>
<article class="ar-deep-tile">
<h2><a href="post-training/reward-and-credit/">奖励从哪里来，信用才该分到哪里</a></h2>
<p>过程标签、最终结果、模型自置信与回溯归因是不同证据。逐步PRM、MRTPO、TACO和MART-GRPO分别做标签获取、奖励定位、正信用降权和失败后缀过滤；INTUITOR则改用内在分布信号，不能把它当外部正确性验证器。</p>
<p class="ar-learning-topic-meta">6 篇重点对照 · 3 个跨论文问答 · 2026-10-27</p>
</article>
<article class="ar-deep-tile">
<h2><a href="post-training/student-trajectory-distillation/">沿学生前缀蒸馏：采样分布与散度方向要分开看</a></h2>
<p>“on-policy”描述监督发生在哪些状态，FKL/RKL/JSD描述在这些状态怎样比较分布。GKD和MiniLLM建立这两个轴，DrOPD、AP-OPD再调整纠错位置或强度，Semi-OPD与学习信号诊断则提醒：离线复用和残余损失各有不同含义。</p>
<p class="ar-learning-topic-meta">6 篇重点对照 · 3 个跨论文问答 · 2026-10-27</p>
</article>
<article class="ar-deep-tile">
<h2><a href="post-training/teacher-and-context/">教师更强仍可能教错：信息、兼容性与成功行为保护</a></h2>
<p>教师的价值不只取决于总分。OPSD改变训练期可见信息，MOPD与逐token路由组织多教师，CSD先统一概率事件，SPOD保护学生已成功选择，VAD筛出可归于视觉证据的修正；这些约束要在模仿之前分别成立。</p>
<p class="ar-learning-topic-meta">6 篇重点对照 · 4 个跨论文问答 · 2026-10-27</p>
</article>
<article class="ar-deep-tile">
<h2><a href="post-training/data-and-budget/">省掉哪一份算力：选问题、少生成、分枝与有条件重放</a></h2>
<p>数据与预算方法改变的是训练链路的不同位置。课程重估当前难度，LESSER降低筛选特征成本，STOPD随机少生成并校正，BranchOPD增加关键分枝，Lightning缓存教师，TAR召回被压制的正确模式；少调用一次教师不等于整个训练更便宜。</p>
<p class="ar-learning-topic-meta">6 篇重点对照 · 3 个跨论文问答 · 2026-10-27</p>
</article>
</div></details>

<details class="ar-deep-shelf"><summary>Agent · 6 张</summary>
<div class="ar-deep-grid">
<article class="ar-deep-tile">
<h2><a href="agent-research/planning-and-search/">规划先问何时见反馈，再问要不要展开搜索</a></h2>
<p>ReAct 与 ReWOO 改变计划接收观察的时机，ToT 与 LATS 改变候选搜索组织，Jev Lookahead 把后继模拟交给代码，DRAGO 则检查形式计划是否忠实。它们处理不同的不确定性：步骤未知、路线选择、环境可达性与规格错误，不应以搜索次数或本地满分统一排名。</p>
<p class="ar-learning-topic-meta">6 篇重点对照 · 3 个跨论文问答 · 2026-10-27</p>
</article>
<article class="ar-deep-tile">
<h2><a href="agent-research/memory-and-skills/">经验进入长期系统前，要解决存取、价值与准入</a></h2>
<p>MemGPT 管信息放在哪里，MemPrice 管有限窗口里保留何种精度，CMP 管效用如何识别；Voyager 把成功程序变技能，VaG 管技能进入库的风险，SkillRise 用后续任务检验整理价值。存得下、相关、合法和能帮助未来，是四个不同问题。</p>
<p class="ar-learning-topic-meta">7 篇重点对照 · 4 个跨论文问答 · 2026-10-29</p>
</article>
<article class="ar-deep-tile">
<h2><a href="agent-research/tools-and-collaboration/">从会调用到能交付：工具接口、可靠性与协作合同</a></h2>
<p>Toolformer 学何时调用，SWE-agent 设计动作接口，RATED 处理相关工具的运行可靠性；AutoGen 定义消息程序，MetaGPT 约束角色交付物，World of SWEcraft 再用隐藏下游检验群体产出。每层都可能失败，调用格式正确不是端到端完成的替身。</p>
<p class="ar-learning-topic-meta">6 篇重点对照 · 4 个跨论文问答 · 2026-10-29</p>
</article>
<article class="ar-deep-tile">
<h2><a href="agent-research/harness-and-self-improvement/">自改进先标对象：答案、经验、接口与系统版本</a></h2>
<p>Self-Refine 改当前产物，Reflexion 改下一次可读经验，HarnessLens 检查局部流程改动，Agent S4 演化接口仓库，RSIFlow 选择干预层，AgentX 把候选送到有护栏的生产闭环。多跑几轮不是共同算法，持久状态与接纳规则才决定在改什么。</p>
<p class="ar-learning-topic-meta">7 篇重点对照 · 4 个跨论文问答 · 2026-10-29</p>
</article>
<article class="ar-deep-tile">
<h2><a href="agent-research/agent-policy-learning/">交互学习：统一轨迹之后，信用和教师信息怎样分配</a></h2>
<p>Agent Lightning先把执行整理成可训练transition；GiGPO、AdaStep和DepGPO分别利用重复状态、回报方差与命令依赖分配信用；Frontier-OPD和ASTEROID则改变教师数据怎样进入学生学习。记录成轨迹只是入口，训练目标和可见信息才定义算法。</p>
<p class="ar-learning-topic-meta">6 篇重点对照 · 3 个跨论文问答 · 2026-10-27</p>
</article>
<article class="ar-deep-tile">
<h2><a href="agent-research/evaluation-and-reliability/">评测追问四件事：完成了、稳健吗、靠什么、花多少</a></h2>
<p>GAIA测最终任务回答，AgentPerturb检查单目标输入扰动，User Proxy Bench检查用户模拟是否偷省信息获取；AlphaDiana完整记录失败与重试，HDA拆解harness涨分来源，选择性评测则约束自动裁判的错误区域。高分只有在这些协议讲清后才有可解释性。</p>
<p class="ar-learning-topic-meta">6 篇重点对照 · 3 个跨论文问答 · 2026-10-27</p>
</article>
</div></details>

[逐篇四层问答](../all.md) · [学习入口](../index.md)
