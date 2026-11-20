"""One-shot authored foundation/risk bundle; never edits shared learning banks.

Run before result curation. PDFs are small fixed-v1 research sources, not model
downloads. All prose/questions below are authored and bilingual-reviewed.
"""

from hashlib import sha256
import json
from pathlib import Path

import fitz

from english_learning_sources import question_units

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache/nov20-latest/foundation"
AUDIT = ROOT / "docs/research-audits/nov20-latest"
DATE = "2026-11-20"

PAPERS = [
    {
        "aid": "2611.26363", "key": "hisa", "domain": "foundation-models",
        "title": "HiSA: Sparsifying the Hidden Dimension of RoPE Attention in LLMs",
        "author": "Ambroise Borbely",
        "org": "EPFL / Swiss Data Science Center (EPFL and ETH Zurich)",
        "published_at": "2026-11-19T16:31:46Z", "priority": "P1",
        "topic": ["注意力与长上下文", "RoPE与隐藏维稀疏"],
        "module": "hisa_components", "tier": "l1_mechanism",
        "code": "https://github.com/ambroise-b/hisa",
        "revision": "6224a46e7e439385ce432ce3f600afb88fb1e5a2",
        "intake": "new_first_release", "sections": ["3", "4", "Appendix A–D"],
        "card": "foundation-models/context-and-state", "peer": "foundation-models:rope",
        "diagram": "flowchart LR\n Q[Pre RoPE Q and K] --> R[Position rotations]\n P[Absolute token positions] --> M[Unwrapped distance times frequency below Phi]\n R --> S[Sum only admitted pair scores]\n M --> S\n S --> N[Fixed sqrt d normalization]\n N --> C[Causal and within reach mask]\n C --> O[Softmax and original values]",
        "figure": [2, [54, 72, 544, 264], "Figure 1: dense, token-sparse and hidden-sparse attention"],
        "formula": r"s_{ij}=d^{-1/2}\sum_{l=0}^{d/2-1}\mathbf 1[0\le(i-j)\theta_l<\Phi]\langle R_{i\theta_l}q_i^{(l)},R_{j\theta_l}k_j^{(l)}\rangle,\quad\theta_l=b^{-2l/d}.",
        "cn": {
            "overview": "HiSA不先筛token，而是对每个query-key点积只保留尚未超过角度预算的RoPE频率对。近处key保留更多分量，远处仅保留慢频分量；Q/K投影不变，规则只由位置、RoPE base和预算决定。",
            "detail": "使用未绕回的相对旋转量，严格小于Phi，不是对2pi取模后比较。分母始终为sqrt(d)，不按剩余维数重标定。没有任何频率对仍有效的key必须退出softmax，而不是留下零logit；因果未来key也必须屏蔽。Phi无穷时恢复dense RoPE。本地位置限定为非负int64范围，uint64在转换前检查上界，其余整数转int64后验证；两个非负int64位置的差在安全范围内，不允许uint8相减回绕造成未来泄漏。",
            "results": "原文表7在d=64、base=1e4、Phi=90度时，4K因果QK乘加保留29.3%；表8对应理想逐pair KV比例61.9%，实际按chunk存储为66.5%。这些是不同口径，不能把QK运算节省直接称为训练或端到端加速。未报告生产线上A/B。",
            "local": "实现精确Eq3的fp32/fp64小张量参考、因果/越reach屏蔽、带绝对位置的decode对齐与梯度负控。显式物化每pair分数，不是稀疏kernel；不实现FA3 block近似、GQA存储压缩、decoder训练、真实KV allocator或吞吐优化。GPU验收另由主运行器冻结后实跑，不以CPU单测代替。",
            "compare": "RoFormer保留所有RoPE二维对，使用相对旋转来编码距离；HiSA额外根据距离和频率删掉部分点积项。这是打分规则变化，不等于在既有checkpoint上无训练切换后仍保留能力。与只删整token的策略也不同，后者不能表达同一key只保留慢频分量。",
            "cost": "原文从头训练135M/360M模型，分别2.7B/7.24B token，单H200每run，并包含学习率选择、长上下文续训、三seed子研究和dense对照。完整训练矩阵超出本轮单A100/A30短预算；仅小张量组件预期三seed合计小于30秒，零模型/数据下载、零API。",
        },
        "en": {
            "overview": "HiSA retains selected RoPE frequency pairs inside each query-key dot product rather than selecting whole tokens first. Nearby keys retain more pairs; distant keys retain slower pairs. Q/K projections stay unchanged, and positions, base and angle budget determine the static rule.",
            "detail": "The rule compares the unwrapped relative angle strictly with Phi, not its remainder modulo2pi. Scaling stays1/sqrt(d), not the number of surviving dimensions. A key with no active pair must leave softmax; a zero logit would still attract probability. Future keys are masked. Infinite Phi recovers dense RoPE. Local positions are nonnegative signed-int64-range integers. uint64 bounds are checked before casting; other integers are converted before subtraction. Differences between nonnegative int64 values cannot overflow, and uint8 wraparound must not expose future keys.",
            "results": "For d64, base1e4 and90degrees, paper Table7 retains29.3% of causal4K QK multiply-adds. Table8 gives61.9% ideal per-pair KV storage, versus66.5% with actual chunk storage. QK work, cache size and end-to-end speed are different quantities. No production A/B is reported.",
            "local": "Implements exact Eq3 as a small fp32/fp64 tensor reference, causal/out-of-reach masking, positioned decoding parity and gradient controls. It materializes pair scores, not a sparse kernel. There is no FA3 block approximation, GQA cache allocator, trained decoder or throughput optimization. Frozen real-GPU validation is separate; CPU tests do not substitute for it.",
            "compare": "RoFormer keeps every RoPE pair and encodes relative position by rotation. HiSA additionally removes pair contributions according to distance and frequency. This changes scoring and does not prove that switching an existing checkpoint without training preserves quality. Whole-token eviction cannot express retaining only a key's slow-frequency pairs.",
            "cost": "The paper trains135M/360M models from scratch on2.7B/7.24B tokens using one H200 per run, with tuning, long-context continuation, a three-seed substudy and dense controls. The complete campaign is outside this short single-A100/A30 budget. The tensor component is expected to take under30seconds across three seeds, with no model/data downloads or API calls.",
        },
        "qa": [
            ["pair-not-token", "basics", "HiSA稀疏的是token还是点积维度？", "主要是每个点积里的RoPE二维频率对；同一key可以只剩慢频部分，而不是整token统一保留或删除。", "教学例：一个远处key可舍弃最快的8对而保留后24对；只有最后一对也过期才整key退出。", "Does HiSA sparsify tokens or dot-product dimensions?", "Primarily the two-dimensional RoPE pairs within each dot product. A key can retain slow pairs without retaining fast ones; only an entirely expired key leaves attention.", "A distant key may drop the fastest8 pairs while keeping24 slower pairs."],
            ["unwrapped-strict-angle", "mechanism", "旋转已经转完一圈，频率对能重新参与吗？", "不能。门槛比较未绕回的Delta乘theta，而且用严格小于；周期性cos相同不代表该项重新进入。", "教学例：theta=1、Phi=1时，距离1已排除；距离7也不会因为7模2pi小于1而恢复。", "Can a pair return after a full rotation?", "No. The threshold uses the unwrapped distance times frequency and a strict inequality. Periodic cosine values do not reactivate an expired pair.", "With theta1 and Phi1, distance1 is excluded; distance7 is also excluded despite its small wrapped angle."],
            ["rope-versus-score", "comparison", "与RoFormer保留旋转、再按token截窗口有什么区别？", "RoFormer本身使用所有对；整token窗口只能整列删key。HiSA在每个距离对不同频率有不同保留窗口，仍统一除以sqrt(d)。", "教学例：d=64但只剩16个分量时仍除以8，不能擅自改成除以4。", "How does this differ from RoFormer plus a token window?", "RoFormer uses all pairs. A token window drops whole keys; HiSA gives frequency pairs distinct distance windows while keeping the original1/sqrt(d) scale.", "With d64 and only16 surviving components, divide by8, not4."],
            ["expired-key-softmax", "implementation", "为什么不能把过期key分数写0后照常softmax？", "零logit仍有正概率，会把本应不可见的value读回来。必须将整key屏蔽；完全无可用key的query明确报错。位置差也须用已验证的有符号整数计算，不能让uint8未来差值回绕；uint64越界在转换前拒绝。", "教学例：过期value=100、当前value=3；正确输出只读3，零logit会污染它。", "Why not leave an expired key at zero logit?", "Zero logits still receive positive mass and expose expired values. Mask the key and reject queries without reachable causal keys. Position differences also use validated signed integers: uint8 wraparound cannot admit future keys, and out-of-range uint64 is rejected before casting.", "With expired value100 and current value3, the correct read is3; a zero logit contaminates it."],
        ],
    },
    {
        "aid": "2611.24963", "key": "canon-layers-scale", "domain": "foundation-models",
        "title": "Physics of Language Models: Part 4.2, Canon Layers at Scale where Synthetic Pretraining Resonates in Reality",
        "author": "Zeyuan Allen-Zhu", "org": "Allen-Zhu Research",
        "published_at": "2026-11-12T18:51:19Z", "priority": "P0",
        "topic": ["网络架构", "局部混合与规模比较"], "module": None, "tier": "review_only",
        "code": "https://github.com/facebookresearch/PhysicsLM4",
        "revision": "75806965208c55e9f7f2e2363d3793d2da75d2e4",
        "intake": "historical_announcement_backfill",
        "sections": ["2.1", "3–6", "Appendix A–D", "F"],
        "card": "foundation-models/context-and-state", "peer": "foundation-models:mamba",
        "diagram": "flowchart LR\n H[Token hidden sequence] --> A[Canon A before attention]\n A --> B[Canon B on projected Q K V]\n B --> C[Canon C before MLP]\n C --> D[Canon D on gated MLP branches]\n D --> E[Matched scale and tuned baselines]\n E --> F[Knowledge scores plus retrieval and two hop probes]",
        "figure": [26, [72, 365, 542, 522], "Figure 12: Canon horizontal residual connections and four insertion points"],
        "formula": r"h'_t=h_t+\sum_{r=0}^{3}w_r\odot h_{t-r},\qquad g(x)=\operatorname{SiLU}(G_1G_2x+b),\quad\operatorname{rank}(G_1G_2)\le16.",
        "cn": {
            "overview": "Canon在层内多个位置加入沿token轴的残差短卷积，显式提供邻近信息。本文把此前小规模合成训练得到的结构判断放到64组1.3B–8B真实语料预训练中检验，并对线性模型使用低秩输出门的GLA5/GDN2。重要贡献还包括对预算、基线调参和可测技能的重新审视。",
            "detail": "Canon是每通道独立、kernel=4、左侧补零的因果卷积，带原hidden残差；A/C在norm后、B在QKV投影后、D覆盖门控MLP两支。线性模型低秩约束作用于SiLU之前的G1G2，激活后门不保证低秩。公开LlamaCanon还用quarter RoPE，不能把其全部差异只归因于卷积。",
            "results": "8B/1T比较中，Canon达到vanilla Llama最终MMLU所需token约减少30%；但标准知识分数更高的线性模型仍会在约500token的简单检索上失败，简单两跳也未被可靠学会。这不等于线性结构普遍无效。论文没有线上A/B。arXiv首发是11月12日；正文日期2025-12-09及历史代码公开时间另记，今日公告不是新算法首发。",
            "local": "仅固定原文、原图、作者机构、公开代码修订、成本与证据局限收录。没有Canon/GLA5/GDN2实现、metrics、GPU回执或可执行Evolve operator；不另造小卷积demo来声称完成64组预训练。当前作者机构是Allen-Zhu Research；正文明确实验在FAIR at Meta完成，官方代码位于facebookresearch，不能把实验关系改写成当前一作Meta署名。",
            "compare": "Canon的宽4因果残差只提供局部token混合，本身不是长历史状态，也不能独立读取任意远位置；它可插入attention、线性attention或SSM。Mamba除局部卷积外还维护输入选择的递归状态，两者功能不能等同。比较需对齐参数/状态与调参，并另测上下文检索；知识分数更高不推出固定状态已具备attention式远程读取。",
            "cost": "64组从头预训练，1.3B/3B/8B、1–2T Nemotron-CC token；原文估计单8B run约10万美元，并对每配置跑多个学习率和评测。已远超单A100/A30或Mac预算，完整实验不复现，不下载checkpoint、不做训练探针。",
        },
        "en": {
            "overview": "Canon adds residual short convolutions along the token axis at several within-layer locations. This paper tests architecture lessons from smaller synthetic training in64 real-corpus pretraining runs at1.3B–8B parameters, including GLA5/GDN2 with low-rank output gates. Budget alignment, baseline tuning and measurable skills are central to the study.",
            "detail": "Canon is a per-channel causal width4 convolution with left zero padding and a hidden-state residual. A/C follow normalization, B follows QKV projections, and D covers both gated-MLP branches. The rank constraint applies before SiLU; the activated gate need not be low-rank. Released LlamaCanon also uses quarter RoPE, so its differences are not solely convolution.",
            "results": "At8B/1T, Canon needs roughly30% fewer tokens to reach vanilla Llama's final MMLU. Yet linear models with stronger standard scores still struggle with simple retrieval in roughly500-token contexts and unreliable two-hop reasoning. This is not universal evidence against linear models. No online A/B is reported. ArXiv v1 is November12; the manuscript's2025-12-09 date and earlier code releases are separate from today's announcement.",
            "local": "Review-only fixed-source documentation, figures, affiliation, code revision, cost and limitations. No Canon/GLA5/GDN2 implementation, metrics, GPU receipt or executable Evolve operator is added. A small convolution demo would not reproduce64 pretraining runs. The current byline is Allen-Zhu Research; experiments were conducted at FAIR at Meta and code is in facebookresearch, not proof of current Meta authorship.",
            "compare": "Canon's causal width4 residual supplies local token mixing, not a long-history state or independent access to arbitrary distant positions; it can augment attention, linear attention or SSMs. Mamba also maintains input-selective recurrent state beyond its local convolution. These roles differ. Align parameters/state and tuning, then separately test retrieval: stronger knowledge scores do not establish attention-like remote reads from fixed-size state.",
            "cost": "The study contains64 from-scratch1.3B/3B/8B runs on1–2T Nemotron-CC tokens, multiple learning rates and evaluations. The paper estimates about100kUSD per8B run. This exceeds one A100/A30 or Mac budget; no checkpoint download or training probe is attempted.",
        },
        "qa": [
            ["horizontal-residual", "basics", "Canon所说horizontal residual连接什么？", "它在同一通道沿时间连接当前token和最近几个token，而不是只在深度方向跳层。", "教学例：kernel=4时，时刻t能直接组合t、t-1、t-2、t-3的同一通道。", "What does a horizontal residual connect?", "It mixes a channel across nearby token positions, rather than only skipping layers along depth.", "A width4 kernel combines a channel at t, t-1, t-2 and t-3."],
            ["gate-rank-location", "mechanism", "GLA5/GDN2的rank16约束能否延伸到激活后的gate？", "不能。低秩约束属于线性乘积G1G2，逐元素SiLU之后不再保证矩阵低秩；不能据此把整个激活门当低秩算子。", "教学例：对秩1矩阵逐元素施加非线性，通常可得到更高秩矩阵。", "Does rank16 also constrain the activated gate?", "No. The linear product G1G2 is rank-constrained, but elementwise SiLU need not preserve that rank. The complete activated gate is not a low-rank linear operator.", "Applying a nonlinear function elementwise to a rank1 matrix can increase its rank."],
            ["tokens-versus-time", "comparison", "30% token节省能否直接称训练快30%？", "不能。每step计算可能增加，还要固定达到的技能或分数。原文用约13%朴素step开销举例时，0.7乘1.13约0.79，对应约21%时间节省。", "教学例：token少30%但每step慢13%，总时长不是原来的70%。", "Is a30% token saving a30% training speedup?", "No. Per-step cost and the target skill must also match. With the paper's illustrative13% naive step overhead,0.7 times1.13 is about0.79, or roughly21% less time.", "Using30% fewer tokens with13% slower steps does not take70% of the original time."],
            ["review-not-run", "implementation", "为什么这次没有为Canon写一个小卷积并报复现完成？", "小卷积不能验收本文关于规模、充分调参和技能差异的中心实证结论。完整64组预训练昂贵，因此明确只收录，不生成proxy指标或Evolve资格。", "教学例：32维随机输入上的卷积形状正确，不是8B/1T达到同等MMLU的证据。", "Why not mark a small convolution demo as reproduced?", "It cannot test the paper's central claims about scale, tuning and skills. The costly64-run campaign remains review-only, without proxy metrics or Evolve eligibility.", "A shape-correct32-dimensional convolution says nothing about8B/1T MMLU token savings."],
        ],
    },
    {
        "aid": "2611.25403", "key": "antom-3-in-1", "domain": "recommendation",
        "title": "Antom 3-in-1 Transformer: A Payment Foundation Model",
        "author": "Weiyu Han", "org": "Ant International",
        "published_at": "2026-11-19T02:47:14Z", "priority": "P1",
        "topic": ["内容理解、审核与风险控制", "支付交易风险"],
        "module": None, "tier": "review_only", "code": None, "revision": None,
        "intake": "new_first_release", "sections": ["2", "3", "4.1–4.6", "Appendix A/B.2"],
        "card": "recommendation/feedback-multitask-causality", "peer": "recommendation:mmoe",
        "diagram": "flowchart LR\n H[User card device histories] --> S[Independent sequence towers]\n T[Transaction fields] --> F[Field attention]\n G[Rolling user graph] --> O[Frozen offline graph encoder]\n S --> Q[Task query fusion and sparse experts]\n F --> Q\n Q --> R[Online risk head]\n O --> R\n R --> P[Same policy and intervention budget]",
        "figure": [3, [70, 60, 545, 385], "Figure 1: sequence, tabular and graph inputs with task-conditioned fusion"],
        "formula": r"\sum_i a_i(q)w_i=q\sum_iw_i,\qquad \mathrm{R@}q=\frac{\sum_i a_i(q)w_iy_i}{\sum_iw_iy_i},\qquad \mathrm{LossRate}=\frac{\mathrm{realized\ financial\ loss}}{\mathrm{successful\ transaction\ amount}}.",
        "cn": {
            "overview": "Antom把用户/卡/设备历史、当前交易字段和滚动用户图分开编码，再用任务query、共享注意力与稀疏专家做多任务融合。序列先做prefix-future对比，图先做视图对比及关系计数重建；下游图encoder冻结，图表示离线生成并按交易时间查询，其余主要模块在线打分。",
            "detail": "这里列的是附录A已公开的固定预算评测口径，不是未公开的完整训练loss或router算法。采样数据使用逆纳入权重；预算边界同分交易可共享分数配额，保证总权重仍等于q倍总体。金额损失率的分母是成功交易金额，不是交易笔数。§2明确未公开详细架构、训练配置和数据构造，不能补写猜测的实现。",
            "results": "2026-06-08至10-14的随机分流试验整体覆盖平台30%交易；试验内XGB、SAINT、Antom份额约32.1/37.4/30.4%，并非各占全站同等比例。业务组合总体相对XGB：CB率-37.74%、损失率-37.88%。I阶段无干预；II阶段同0.5%预算真实决策，CB率相对-28.28%，以66个共同交易日期重加权为-26.09%。这些口径不可混作同一个lift；原文未提供线上置信区间。",
            "local": "只收录经核对的生产证据、方法边界、原图和成本；没有本地模型、训练/推理代码、metrics、GPU回执或Evolve operator。公开IBM/图benchmark的存在不补全缺失配置和私有训练链路；不以小型拼接/MLP冒充7B支付基础模型。",
            "compare": "MMoE通过每任务gate组合共享专家；Antom在多模态编码之后，用任务query聚合共享信息再路由，并额外查离线图表示。多任务路由这一共性不表示两者可等价替换。原文生产对照是XGB/SAINT，不是MMoE；不能捏造两者实测胜负。",
            "cost": "原文约6.92B总参数、每路由激活1.74B，主要预训练使用内部交易/关系数据，并有多业务适配与四个月生产试验；完整训练细节又未公开。单A100/A30不能低成本忠实复做，不下载或探跑大模型，仅审查收录。",
        },
        "en": {
            "overview": "Antom separately encodes user/card/device histories, transaction fields and rolling user graphs. Task queries, shared attention and sparse experts fuse modalities for multiple tasks. Sequence pretraining contrasts prefixes with future summaries; graph pretraining combines view agreement and relation-count reconstruction. The frozen graph encoder runs offline; time-aligned embeddings augment online scoring.",
            "detail": "These are the disclosed AppendixA evaluation definitions, not an invented full training loss or router algorithm. Sampled populations use inverse-inclusion weights, and tied boundary scores share a fractional allocation to keep the budget fixed. Loss rate divides financial loss by successful transaction amount, not transaction count. Section2 withholds detailed architecture, training and dataset construction.",
            "results": "The June8–October14 randomized trial covers30% of platform transactions; within it, XGB/SAINT/Antom shares are32.1/37.4/30.4%, not those fractions of all traffic. Portfolio CB/loss rates fall37.74/37.88% versus XGB. StageI has no intervention. StageII uses the same0.5% decision budget: CB falls28.28% pooled or26.09% after common-date weighting over66 dates. These are distinct estimands; online confidence intervals are not provided.",
            "local": "Review-only production evidence, mechanism boundaries, original figure and cost. No local model, training/inference code, metrics, GPU receipt or Evolve operator. Public IBM/graph benchmarks do not supply the missing recipe or private training path. A small concatenation/MLP proxy would not reproduce this7B payment foundation model.",
            "compare": "MMoE uses task-specific gates over shared experts. Antom first encodes modalities, aggregates them with task queries, routes experts and adds offline graph embeddings. Shared multitask routing does not make them interchangeable. Reported production controls are XGB/SAINT, not MMoE; no measured head-to-head claim is made.",
            "cost": "The industrial model has about6.92B parameters and1.74B active per route, private transaction/graph pretraining, multiple adaptations and a four-month production trial. Detailed training configuration is also withheld. A faithful low-cost single-A100/A30 reproduction is unavailable; no large model download or probe is attempted.",
        },
        "qa": [
            ["three-modalities", "basics", "3-in-1指什么，图encoder也每笔交易重跑吗？", "指交易序列、表格字段和关系图三种模态。图encoder在微调时冻结、离线产出表示，在线只查满足时间条件的图向量。", "教学例：新交易在线编码其历史和字段，但不能用交易发生后才形成的关系图作特征。", "What are the three modalities, and is the graph rerun per payment?", "Sequences, tabular fields and relational graphs. The graph encoder is frozen during adaptation and produces offline representations; online scoring looks up time-eligible graph embeddings.", "A new payment may use prior history and fields, not graph edges created after that payment."],
            ["fixed-budget-ties", "mechanism", "固定0.5%干预预算时，同分边界怎么处理？", "附录按总体权重分配边界的分数配额，使选中权重恰好占q；不能因大量相同历史同分而无意扩大预算。", "教学例：剩10单位预算而同分组有20单位，每个样本分配0.5，不能全选20单位。", "How are ties handled at a fixed0.5% budget?", "The appendix fractionally allocates a boundary score group so selected population weight equals q. Ties must not silently expand the intervention budget.", "If10 budget units remain for a tied group of20, allocate0.5 to each, not the whole group."],
            ["portfolio-versus-stage", "comparison", "为什么不能把37.88%和26.09%当成同一指标的重复验证？", "前者是业务组合总体损失率相对变化，后者是II阶段CB率按共同日期重加权的相对变化；分子、样本聚合和阶段不同。", "教学例：赔付争议追回会改变最终损失，但不一定同幅改变原始CB金额。", "Why are37.88% and26.09% not repeated estimates of one metric?", "The former is portfolio overall-loss reduction; the latter is StageII common-date-weighted chargeback-rate reduction. Numerators, aggregation and stages differ.", "Dispute recoveries can change realized loss without changing original chargeback amounts by the same proportion."],
            ["not-open-recipe", "implementation", "有公开IBM数据和生产A/B，为什么仍不写完整模型复现？", "公开评测数据不等于公开预训练数据、结构和训练配方。§2明确省略这些细节，因此只收录证据，不用便宜proxy代替定义性模型。", "教学例：在IBM上训练一个三路MLP不能验证私有7B模型的37.88%线上损失改善。", "Why is the model not reproduced despite public IBM data and A/B evidence?", "A public evaluation dataset does not reveal pretraining data, architecture and recipe. Section2 explicitly withholds them, so documentation does not replace the defining model with a cheap proxy.", "A three-branch MLP on IBM data cannot validate the private7B model's37.88% production loss reduction."],
        ],
    },
]


def write(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def detail_path(p):
    section = "recommendation-components" if p["domain"] == "recommendation" else p["domain"]
    return f"{section}/{p['aid']}-{p['key']}/README.md"


def document(p, english=False):
    lang = "en" if english else "cn"
    body = p[lang]
    source = f"https://arxiv.org/pdf/{p['aid']}v1"
    module = p["module"]
    code_dir = "src/auto_research/foundation_models/hisa_components.py" if module else "None (review-only; no reproduction code)" if english else "无（仅审查收录，没有复现代码）"
    upstream = (
        f"[{p['code']}]({p['code']}); Apache-2.0; revision `{p['revision']}`"
        if p["code"] else
        "No released author method code found; Section2 withholds the detailed recipe."
        if english else "未找到已发布的原作者方法代码；§2明确未公开详细配方。"
    )
    labels = ["Paper information", "Original paper summary", "Background and principal changes", "Original paper figure", "Core equations", "Paper offline and online results", "Local reproduction", "Data protocol and code mapping", "Same-topic comparison and boundaries", "High-cost full experiment"] if english else ["论文信息", "原始论文总结", "背景与主要改动", "原论文关键图", "核心公式", "论文离线与线上效果", "本地复现", "数据协议与代码映射", "同主题比较与边界", "高成本完整实验"]
    fields = ["Paper link", "Company / institution / school", "Original publication date", "Original source code", "Local adapter / key", "Local reproduction code directory"] if english else ["论文链接", "公司 / 机构 / 学校", "首次公开日期", "原作者开源代码", "本地 adapter / key", "本地复现代码目录"]
    values = [f"[arXiv:{p['aid']}v1](https://arxiv.org/abs/{p['aid']}v1); [fixed PDF]({source})", f"{p['author']}: {p['org']} (fixed-v1 byline)", f"{p['published_at']} (arXiv v1); announced2026-11-20", upstream, f"`{p['key']}`; `adapter: null`; not Evolve-integrated", f"`{code_dir}`"]
    warning = "L1 reference component, diagnostic only" if module and english else "L1参考组件，仅机制诊断" if module else "Review only; no executable reproduction" if english else "仅审查收录；没有可执行复现"
    text = f"# {p['title']}\n\n" + ("[简体中文](README.md)" if english else "[English](README-en.md)") + f"\n\n> **{warning}**. " + ("Full experiment: **high cost, not reproduced (review DONE)**." if english else "完整实验：**成本过高，不复现（审查 DONE）**。") + f"\n\n## {labels[0]}\n\n| Field | Value |\n| --- | --- |\n"
    text += "".join(f"| {a} | {b} |\n" for a,b in zip(fields,values,strict=True))
    if p["key"] == "canon-layers-scale":
        text += "\n" + ("Current author affiliation is Allen-Zhu Research. The fixed paper states experiments were conducted at FAIR at Meta; this research relationship does not change the byline grouping.\n" if english else "当前一作机构为Allen-Zhu Research；固定原文明确实验在FAIR at Meta完成。Meta研究执行/官方代码关系与作者当前机构分别记录，不修改机构聚合。\n")
    text += f"\n## {labels[1]}\n\n### {labels[2]}\n\n{body['overview']}\n\n[Fixed-v1 primary source]({source})\n\n~~~mermaid\n{p['diagram']}\n~~~\n\n"
    text += f"<!-- paper-figure:start -->\n### {labels[3]}\n\n[![{p['figure'][2]}](assets/paper-figure-01.png)]({source}#page={p['figure'][0]})\n\n" + ("Original PDF crop, no semantic editing; author evidence, not a local result. [Provenance](assets/provenance.json). Copyright remains with the authors.\n" if english else "原始PDF裁切，没有语义编辑；是作者方法/结果，不是本地证据。[页码、裁切与SHA256](assets/provenance.json)，版权归原作者。\n") + "<!-- paper-figure:end -->\n\n"
    text += f"### {labels[4]}\n\n$$\n{p['formula']}\n$$\n\n{body['detail']}\n\n### {labels[5]}\n\n{body['results']}\n\n## {labels[6]}\n\n### {labels[7]}\n\n{body['local']}\n\n"
    if module:
        text += "```bash\nPYTHONPATH=src python -c 'from auto_research.foundation_models.hisa_components import diagnostic; print(diagnostic(42))'\nPYTHONPATH=src python -m pytest tests/test_nov20_hisa_components.py -q\n```\n\n" + ("Generated tensors are diagnostics, not public capability benchmarks. CPU tests do not fulfill the CUDA gate.\n\n" if english else "生成小张量不是公开能力benchmark；CPU单测不完成CUDA验收。\n\n")
    text += f"### {labels[8]}\n\n{body['compare']}\n\n### {labels[9]}\n\n{body['cost']}\n\n" + ("Configuration-based cost judgment, not measured full-run time. **High cost, not reproduced (review DONE)**; no automatic retry or implementation queue, no capability improvement or Evolve promotion claim.\n" if english else "这是依据原文配置的成本判断，不是完整实验实测耗时。**成本过高，不复现（审查 DONE）**；不自动重试、不加入实现队列，不声明能力提升或Evolve晋级。\n")
    return text


def main():
    if (AUDIT / "foundation-review.json").exists():
        raise RuntimeError("one-shot bundle already authored; edit sources explicitly rather than overwrite curated evidence")
    known = json.loads((ROOT / "docs/research-manifest.json").read_text())["papers"]
    paths = {p["domain"] + ":" + p["key"]: p["detail_path"] for p in known}
    paths.update({p["domain"] + ":" + p["key"]: detail_path(p) for p in PAPERS})
    accepted, bank, overlays, proposals = [], {}, {}, []
    for p in PAPERS:
        identity = p["domain"] + ":" + p["key"]
        pdf = CACHE / (p["aid"] + "v1.pdf")
        pdf_hash = sha256(pdf.read_bytes()).hexdigest()
        directory = ROOT / "docs" / detail_path(p)
        assets = directory.parent / "assets"
        assets.mkdir(parents=True, exist_ok=True)
        doc = fitz.open(pdf)
        page, box, caption = p["figure"]
        asset = assets / "paper-figure-01.png"
        doc[page - 1].get_pixmap(matrix=fitz.Matrix(2,2), clip=fitz.Rect(box), alpha=False).save(asset)
        write(assets / "provenance.json", {"source_url":f"https://arxiv.org/pdf/{p['aid']}v1", "paper_url":f"https://arxiv.org/abs/{p['aid']}v1", "reviewed_version":"v1", "retrieved_on":DATE,"page":page,"crop_box_pdf_points":box,"caption":caption,"extraction":"Original PDF crop, no semantic editing", "source_pdf_sha256":pdf_hash,"asset_sha256":sha256(asset.read_bytes()).hexdigest(),"copyright":"Copyright retained by the original authors; research commentary, not a local result."})
        cn = document(p)
        directory.write_text(cn)
        (directory.parent / "README-en.md").write_text("<!-- source-sha256: " + sha256(cn.encode()).hexdigest() + " -->\n" + document(p,True))
        component = p["module"] is not None
        cost = {"source":f"https://arxiv.org/pdf/{p['aid']}v1; " + ", ".join(p["sections"]),"available_resource":"one A100 or A30, or local Mac","paper_configuration":p["cn"]["cost"],"model_scale":p["en"]["cost"],"estimated_cost_basis":"Fixed-paper configuration, not measured full-run time; no costly probe.","decision":"成本过高，不复现（审查 DONE）；" + ("仅低成本HiSA公式组件验收" if component else "仅审查收录，无实现")}
        spec = {"domain":p["domain"],"key":p["key"],"title":p["title"],"paper_url":f"https://arxiv.org/abs/{p['aid']}v1","reviewed_version_url":f"https://arxiv.org/pdf/{p['aid']}v1","reviewed_version":"v1","published":p["published_at"][:10],"published_at":p["published_at"],"announced_on":DATE,"detail_path":detail_path(p),"topic":p["topic"],"first_author":p["author"],"first_author_affiliation":p["org"],"affiliation_evidence":"Fixed-v1 PDF byline cross-checked against fixed HTML; research-execution relations kept separate.","verified_priority_organizations":[],"code":p["code"],"code_status":f"已发布原作者源码：[{p['code']}]({p['code']})；Apache-2.0；已核对修订{p['revision']}。" if p["code"] else "未找到原作者模型源码；§2明确详细架构、训练配置和数据构建不在本次公开范围。","code_license":"Apache-2.0" if p["code"] else "未发布/未找到可核验方法代码许可证","upstream_revision":p["revision"],"method_source_sha256":pdf_hash,"adapter":None,"priority":p["priority"],"intake_class":p["intake"],"implementation_status":"component_only" if component else "deferred_high_cost","evaluation_tier":p["tier"],"diagnostic_only":True,"promotion_eligible":False,"evolve_integrated":False,"local_operator":"auto_research.foundation_models.hisa_components.diagnostic" if component else None,"local_command":"PYTHONPATH=src python -c 'from auto_research.foundation_models.hisa_components import diagnostic; print(diagnostic(42))'" if component else None,"requires_gpu_validation":component,"gpu_validation_passed":False,"gpu_validation_artifact":"docs/gpu-validations/hisa-a100-20261120-latest.json" if component else None,"full_experiment_status":"not_reproduced_high_cost","full_experiment_review_done":True,"review_done":True,"review_resolution":"not_reproduced_high_cost","automatic_retry":False,"automatic_implementation_queue":False,"cost_assessment":cost,"summary":p["cn"]["overview"] + " " + p["cn"]["local"]}
        if not component:spec["deferral_reason"] = p["cn"]["cost"] + " 成本过高，不复现（审查 DONE）。"
        if p["key"] == "canon-layers-scale":
            spec["research_execution_organizations"] = ["FAIR at Meta"]
            spec["priority_relation"] = "Fixed paper states all experiments conducted at FAIR at Meta; official historical code under facebookresearch; current first-author affiliation remains Allen-Zhu Research."
        if p["key"] == "antom-3-in-1":
            spec["online_ab_review"] = {"source":f"https://arxiv.org/pdf/{p['aid']}v1","sections":["4.2", "Appendix B.2"],"production":True,"randomized_assignment_reported":True,"trial_platform_traffic_fraction":0.30,"intervention_budget_fraction":0.005,"stage_i":"2026-06-08/2026-08-02, scoring only","stage_ii":"2026-08-03/2026-10-14, production intervention","baseline":"XGB-Online; SAINT-style","portfolio_loss_rate_relative_change":-0.3788,"stage_ii_pooled_cb_relative_change":-0.2828,"stage_ii_date_weighted_cb_relative_change":-0.2609,"common_transaction_dates":66,"reported_confidence_interval":None,"limitations":"Private full recipe/data; estimates use distinct metrics/stages; no local reproduction."}
        write(ROOT / f"src/auto_research/paper_specs/catalog/{p['domain']}/{p['key']}.json",spec)
        accepted.append({"arxiv_id":p["aid"],"key":p["key"],"domain":p["domain"],"identity":identity,"title":p["title"],"first_author":p["author"],"first_author_affiliation":p["org"],"first_published_at":p["published_at"],"announced_on":DATE,"priority":p["priority"],"intake_class":p["intake"],"reviewed_version":"v1","reviewed_source_url":spec["reviewed_version_url"],"source_sha256":pdf_hash,"sections_read":p["sections"],"implementation_status":spec["implementation_status"],"evaluation_tier":p["tier"],"scope":p["en"]["local"],"cost_basis":p["en"]["cost"],"component_budget":"At most30seconds/three seeds, zero model/data/API; exact small tensor reference." if component else None,"requires_gpu_validation":component,"gpu_validation_passed":False,"local_detail_path":detail_path(p),"code_url":p["code"],"upstream_revision":p["revision"],"full_experiment_status":"not_reproduced_high_cost","full_experiment_review_done":True,"review_done":True,"review_resolution":"not_reproduced_high_cost","automatic_retry":False,"automatic_implementation_queue":False})
        questions=[]; english={}
        for qid,level,q,a,example,eq,ea,ee in p["qa"]:
            questions.append({"id":qid,"level":level,"question":q,"answer":a,"example":example,"source_sections":["背景与主要改动","核心公式","数据协议与代码映射","同主题比较与边界","高成本完整实验"],"added":DATE})
            english[qid]={"question":eq,"answer":ea,"example":ee}
        bank[identity]={"questions":questions}
        units=question_units({identity:questions})
        for q in questions:
            uid=f"qa/{identity}/{q['id']}"
            overlays[uid]={"source_sha256":units[uid].source_sha256,"reviewed":True,"fields":english[q["id"]]}
        pair=[identity,p["peer"]]
        revisions={pid:sha256((ROOT/"docs"/paths[pid]).read_bytes()).hexdigest() for pid in pair}
        comparison=questions[2]
        proposals.append({"paper":identity,"target_card":p["card"],"source_revisions":revisions,"comparison":{"position":p["cn"]["overview"],"tradeoff":p["cn"]["compare"],"sections":["背景与主要改动","核心公式","同主题比较与边界"]},"analysis":{"title":p["title"],"body":p["cn"]["compare"]+" "+p["cn"]["detail"],"papers":pair},"question":{"id":"nov20-"+p["key"],"question":comparison["question"],"answer":comparison["answer"],"example":comparison["example"],"papers":pair},"update":{"date":DATE,"papers":pair,"summary":p["cn"]["compare"]+" 本地证据层级与完整实验不复现分别记录。"},"english":{"comparison":{"position":p["en"]["overview"],"tradeoff":p["en"]["compare"]},"analysis":{"title":p["title"],"body":p["en"]["compare"]+" "+p["en"]["detail"]},"question":english[comparison["id"]],"update":p["en"]["compare"]+" Local evidence and high-cost non-reproduction remain separate."}})
    write(AUDIT/"foundation-authored-bundle.json",{"schema_version":1,"date":DATE,"papers":bank,"english_question_units":overlays})
    write(AUDIT/"deep-dive-proposals-foundation.json",{"schema_version":1,"reviewed_on":DATE,"integration_owner":"root","proposals":proposals})
    write(AUDIT/"foundation-review.json",{"schema_version":1,"reviewed_on":DATE,"requested_window":["2026-11-19",DATE],"scope":"Finite first-source review; HiSA and Antom are new first releases, Canon is historical announcement/official-Meta-research backfill, not a new algorithm today.","preflight_before_implementation":True,"available_resource":"one A100 or A30, or local Mac","large_downloads_authorized_or_needed":False,"watermark_change_claimed":False,"accepted":accepted,"unselected_candidates":[{"arxiv_id":"2611.24969","title":"Global Importance Estimation for KV Cache Eviction","original_published_at":"2026-11-16T02:29:03Z","reason":"New bulletin but older nonpriority first release; outside this finite selected implementation scope, not a method rejection."},{"arxiv_id":"2611.25938","title":"DTS: Delta-Based Tile Scoring for Efficient Long-Context Sparse Attention","original_published_at":"2026-11-19T11:23:22Z","reason":"Relevant low-cost candidate, not selected into this bounded batch; no completed implementation claim."},{"arxiv_id":"2611.25172","title":"MV-JEPA: Post-Training Video Encoders for Cross-View Understanding","original_published_at":"2026-11-18T20:58:38Z","reason":"New bulletin overlap; not selected in this fixed scope. Single-GPU9000 updates is not automatically low-cost; no experiment launched."}],"selection_notes":["Canon byline is Allen-Zhu Research; FAIR at Meta experiment and official repository relationship are separately recorded.","Antom production randomization and fixed intervention budget meet evidence selection; missing private recipe still prevents faithful local reproduction.","No model/data downloads, paid APIs, complete campaigns, proxy capability comparisons or Evolve promotion."]})
    print("Authored3papers,1component,12reviewed bilingual questions and3deep-dive proposals; shared banks untouched.")


if __name__ == "__main__":
    main()
