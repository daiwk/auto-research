# 按年月

同月论文保留在同一小节，但每篇独占一行，并附主要方法简介。

## 2026-08
- [Sona](../2608.11015-sona/README.md)：压缩长历史并自回归生成层级 Semantic ID，再以 item ranker 统一替换音乐推荐级联。
- [MetaStrategy](../2608.09440-metastrategy/README.md)：根据请求生成带类型的多目标排序策略，并由确定性 compiler 校验、执行和审计。
- [Gryphon-v2](../2608.06213-gryphon-v2/README.md)：Yandex 用共享 encoder 串联 SID 生成与 item-level ranking，并从当前 rollout 和真实曝光双路蒸馏高容量 teacher。
- [DEGR](../2608.04809-degr/README.md)：京东把 cohort 多样性约束与 reward-adaptive ORPO 加入生成式重排，再以多样性 greedy selection 输出列表。
- [Twitch Multi-Objective Ranking](../2608.04455-twitch-mor/README.md)：以 fresh/delayed 双目标、生命周期 gate 与共享专家联合优化直播推荐，兼顾即时互动和延迟价值。
- [LLM Thompson Priors](../2608.03382-llm-ts-prior/README.md)：让 LLM 为冷启动评论提供分群 Beta 先验，再由 Thompson Sampling 持续用真实反馈校正探索策略。
- [DME](../2608.02148-dme/README.md)：抖音以 typed latent evidence 与 cross-conditional reconstruction 在保持向量召回效率的同时补足细粒度多模态语义。
- [KGD](../2608.02738-kgd/README.md)：把可刷新预训练知识与下游几何结构解耦，通过 BMTP 与正交约束降低流式推荐迁移时的表示冲突。
- [SPEAR](../2608.01738-spear/README.md)：得物以双 embedding、乘法改写门和 request-specific selector 消除通用词改写捷径。
- [STEPS](../2608.01949-steps/README.md)：把推送执行与下一次唤醒规划成自触发 Agent 闭环，并用轻量 filter 控制开销和异常行为。
- [HRPO](../2608.00750-hrpo/README.md)：按 Semantic ID 层级分配残差 credit-to-go，使生成式推荐的组相对策略优化能感知前缀质量和后续回报。

## 2026-07
- [CCFormer](../2607.28070-ccformer/README.md)：腾讯以字段分离的 ID/content 表征、门控融合和分层历史压缩，同时降低超长行为序列开销并增强内容泛化。
- [HA-MoE](../2607.27577-ha-moe/README.md)：Google Discover 依据 session 内容异构性动态路由多个专长 expert，统一排序开放网页内容。
- [Open Web UFM](../2607.28019-open-web-ufm/README.md)：Teads 在开放网页行为上用双裁剪对比学习与 next-item 目标预训练共享用户编码器，再迁移到广告排序。
- [ROCS](../2607.27744-rocs/README.md)：Meta 将请求侧特征只编码一次，把候选相关交互延后到批量评分阶段，以统一服务检索和排序并提升 QPS。
- [ASARL](../2607.26593-asarl/README.md)：以 ReasonAgent、CriticAgent、GenAgent 闭环整理 QQ 社交搜索数据，再经 SCT、PGO 和 Social Distillation 服务在线模型。
- [RecoReward](../2607.25901-reco-reward/README.md)：用冻结推荐双塔的目标/非目标亲和力差训练内容描述，并保持线上 content-only serving。
- [SWAG](../2607.25233-swag-bid/README.md)：用 masked future plan、七日滑窗目标和逐步 gate 优化跨 episode 自动出价。
- [TWICE](../2607.25404-twice/README.md)：分离点击和转化时钟，以 current-status likelihood 和单调 delay CDF 学习长期 CVR。
- [CORE](../2607.24417-core-relevance/README.md)：美团把 High/Mid/Low 相关性拆成条件二分类，用逐 step GRPO 优化 reasoning，再通过 PostCoT 蒸馏到低延迟双头模型。
- [Mosaic](../2607.24015-mosaic/README.md)：Meta 将 memorization、dense、sequential 与 CoTrain 用户表征组织成 specialist fleet，并以 MRM 和 cosine redundancy loss 挖掘增量信息。
- [OxygenREC-v2](../2607.24255-oxygenrec-v2/README.md)：把目标行为写入生成 decoder prefix，并用未来交互 privileged teacher 和熵路由蒸馏内化判别能力。
- [UniR²](../2607.24439-unir2/README.md)：快手用 Dual-Query Prefix-Causal Attention 在同一 decoder 序列内统一层级 SID 生成和多目标排序，并以 ranking-only LoRA 隔离梯度。
- [Dual-purpose Semantic IDs](../2607.24865-dual-sid/README.md)：YouTube 用同一分层 SID 表达协同身份，并以 Semantic Decoder 恢复内容语义表示。
- [Melo](../2607.23718-melo/README.md)：以多节点音乐 Agent、实体目录 grounding 和反思重试生成可靠 playlist。
- [YouTube Freshness](../2607.23749-youtube-freshness/README.md)：组合 recency、IPS、可移除 bias tower 与不确定性探索打破新内容反馈环。
- [BARGE](../2607.21028-barge/README.md)：用 ICA 恢复 item token 结构、HPR 重排累计语义路径，再以 OSQ 正交双通道和 OR-fusion 补充可达候选。
- [PinEqualizer](../2607.22518-pinequalizer/README.md)：在 Pinterest 全漏斗维护 fresh exploration corpus，并以 engagement dropout、内容交叉、分 cohort calibration 和 UCB 减少旧内容偏置。
- [TSGR](../2607.18796-tsgr/README.md)：把 residual semantic prefix 与并行全局/query 价值码结合，再由联合 VRM 完成价值感知生成召回。
- [RAMP](../2607.17473-ramp/README.md)：显式训练个性化和公共字段双路径，用 feature mask 与 prediction alignment 适配隐私受限流量。
- [Pin-SCALE](../sigir2026-pin-scale-pin-scale/README.md)：Pinterest 用 engagement-aware Semantic ID、级联 pooling 与多视角对比学习接入 dense retrieval。
- [UAME](../2607.17092-uame/README.md)：联合预测满意度均值和不确定性，以概率 pairwise loss 和冲突加权缓解多目标标签偏差。
- [WHALE](../2607.17017-whale/README.md)：逐层交换 Wukong 特征交互分支与 HSTU 行为序列分支，构成统一可扩展排序模型。
- [RECAP](../2607.15730-recap/README.md)：维护固定容量流式语义画像，并把历史推荐反馈训练成 GRPO reward，形成画像优化闭环。
- [RecGPT-V3](../2607.15591-recgpt-v3/README.md)：用可演化 Memory Hub、文本/SID 混合基础模型和可重建 latent reasoning 同时改进长期用户理解、商品 grounding 与推理效率。
- [Downstream Rewards](../2607.14192-downstream-rewards/README.md)：筛选与未来参与度相关的 session reward，并通过模型无关 reward heads 接入多个推荐 surface。
- [Long-History User Transformers](../2607.14331-long-history-transformer/README.md)：离线编码完整历史并缓存固定状态，在线仅融合近期行为以控制广告排序延迟。
- [TMallGS](../2607.13398-tmallgs/README.md)：以 field-wise QKV、噪声门控、FiLM 和逐层误差监督统一电商搜索异构字段。
- [Causal Retrieval](../2607.14161-causal-retrieval/README.md)：Pinterest 用 doubly-robust uplift 判断是否触发 shopping candidate generator。
- [DANet](../2607.12578-danet/README.md)：融合兴趣建模、折扣时频分解与个性化折扣偏好预测 CVR。
- [MESH](../2607.12392-mesh/README.md)：用异构模块塔和 residual gated bias correction 保护 fresh 内容的缩放收益。
- [NONTP](../2607.12277-nontp/README.md)：通过 TCL 感知多步未来轨迹，并以 TDL 为跨域目标增加共享预测头的第二条梯度路径。
- [Proximity Features](../2607.12246-proximity-features/README.md)：自适应聚合地理群体行为，为匿名用户提供不依赖持久 ID 的冷启动信号。
- [SAM](../2607.12714-sam/README.md)：学习购买后兴趣退出及恢复节奏，在注意力层抑制重复推荐。
- [SlimPer](../2607.12281-slimper/README.md)：通过固定知识库的 Select–Match–Refine 循环替代全序列逐层传播，降低长历史排序的计算和中间状态。
- [Prompt Generation](../2607.11326-prompt-generation/README.md)：把异构特征组织成配置驱动的生成提示，通过 token 压缩和多种合并策略服务搜索与推荐召回。
- [Cluster GOOBS](../2607.00448-cluster-goobs/README.md)：在线聚类用户或物品表征，并以 cluster-aware sampler 改善训练样本覆盖和头部集中。

## 2026-06
- [CMSL](../2606.28533-cmsl/README.md)：用可学习兴趣 lenses 拆分多兴趣序列，并结合 HSTU 建模不同语义 strand。
- [NOVA](../2606.27243-nova/README.md)：以 architecture gradient 汇总验证和指标反馈，并通过四级级联阻断静默错误架构。
- [TokenMinds](../2606.25147-tokenminds/README.md)：共享序列 encoder，同时输出稠密用户向量和分层 SID 用户 token，再以可学习 token embedding 注入生产排序模型。
- [G2Rec](../2606.20554-g2rec/README.md)：构建可微 soft graph，并联合图结构与生成式双目标学习用户—物品关系。
- [RankGraph-2](../2606.18379-rankgraph2/README.md)：对图边去热门偏置，离线预计算多跳 PPR，再以 cluster index 服务召回。
- [EvoRec](../2606.28368-evorec/README.md)：让 Research/Code Agent 迭代模型，Skill Evolver 从持久 Memory 中提炼优化方法。

## 2026-05
- [Rec-Distill](../2605.29755-rec-distill/README.md)：结合 batch 与 streaming teacher，把大模型知识蒸馏到轻量推荐 student，并优化跨任务可迁移性。
- [Pinterest Ads LLM](../2605.27856-pinterest-ads-llm/README.md)：对广告主列表进行 SFT/GRPO，让 LLM 作为传统广告召回与排序的补充预测器。
- [DeGRe](../2605.25749-degre/README.md)：将离线 lookahead evaluator 的列表价值蒸馏成在线 dense 生成监督。
- [AKT-Rec](../2605.23310-akt-rec/README.md)：用 LLM Semantic ID 构造语义簇，以非对称对比学习和活动度门控把头部知识迁移到长尾。
- [HARNESS-LM](../2605.23572-harness-lm/README.md)：以 teacher、L2 对齐和对比精修三阶段训练轻量非对称检索器。
- [Memento](../2605.24051-memento/README.md)：采用 query-conditioned MMR 在相关性与多样性之间动态权衡，进行候选重排。
- [LLM Retrieval](../2605.21969-llm-ad-retrieval/README.md)：通过 domain SFT 生成层级广告属性，构建语义图并约束召回结果对属性扰动的稳定性。
- [FLUID](../2605.21832-fluid/README.md)：将直播多模态切片离散为 slice/room LUCID，以独立 prefix token 晚融合并逐阶段退掉候选 item ID。
- [MDCNS](../2605.19651-mdcns/README.md)：从多种负样本分布协同采样，并通过双模型更新降低单一采样偏差。
- [GrowthGR](../2605.17994-growthgr/README.md)：用 ItemLTV 与多价值 MoPO 引导生成式召回发现高潜新品。
- [CQ-SID](../2605.14434-cq-sid/README.md)：用类目约束残差 Semantic ID 与 expert-guided GRPO 优化天猫搜索生成式检索。
- [MM-LLM](../2605.09338-mm-llm/README.md)：把多模态内容转成 caption/token 特征，再注入推荐模型增强内容理解。
- [UniVA](../2605.05803-univa/README.md)：用 Commercial SID 和 generation-as-ranking 统一广告生成，并通过价值对齐 RL 与 trie beam 优化收益。
- [RecGPT-Mobile](../2605.04726-recgpt-mobile/README.md)：将 LoRA+INT8 小模型部署到端侧，通过预算约束 prompt 和 entropy/Jaccard/JS 漂移分数按需生成用户意图。
- [LWGR](../2605.18771-lwgr/README.md)：把个性化 soft instruction 注入 LLM 世界知识，并用交叉注意力和拉格朗日约束与推荐分数融合。

## 2026-04
- [GloRank](../2604.25291-glorank/README.md)：在全局 SID 空间用 listwise SFT 与 RL 优化全库生成重排。
- [AgenticRecTune](../2604.26969-agentic-rec-tune/README.md)：Google Discover 以多 Agent 和自进化 SkillHub 自动提出、审查、执行并沉淀推荐配置实验。
- [CS3](../2604.19269-cs3/README.md)：以循环自修正、跨塔同步和级联教师增强可在线部署的双塔召回。
- [GenRec](../2604.14878-genrec/README.md)：用 page-wise NTP、非对称 Token Merger 和带 NLL 正则的 GRPO-SR 优化整页结果。
- [SOLARIS](../2604.12110-solaris/README.md)：预测未来 user-item pair，异步预计算并缓存 foundation-model latent，在线命中直接消费。
- [Dual-Rerank](../2604.07420-dual-rerank/README.md)：蒸馏 AR 顺序知识到 NAR 并行重排器并显式优化效用/延迟。
- [MBGR](../2604.02684-mbgr/README.md)：以 business-aware SID、共享专家和动态标签路由统一多个业务域的生成式推荐。

## 2026-03
- [Cross-domain KD](../2603.28994-cross-domain-kd/README.md)：把 YouTube 等源域 teacher 的知识蒸馏到目标域，实现面向音乐发现的零样本迁移。
- [GLIDE](../2603.17540-glide/README.md)：用 residual Semantic ID 自回归生成候选，并同时注入近期历史和长期用户 prompt。
- [HAP](../2603.03770-hap/README.md)：按候选异质性动态路由不同计算量的预排模型。
- [OneRanker](../2603.02999-oneranker/README.md)：用统一 token 空间联合生成和 value-aware 广告排序。
- [PinCLIP](../2603.03544-pinclip/README.md)：把 VLM 图文对齐与 Pin-Board 共现邻居目标结合，改善 fresh 内容表征。
- [IDProxy](../2603.01590-idproxy/README.md)：把多模态内容表征先对齐到 item-ID 协同空间，再经多层 proxy 与 gate 接入排序。

## 2026-02
- [GRC](../2602.23639-grc/README.md)：让生成式推荐器结构化地反思首错位置和语义属性，再纠正 SID 轨迹。
- [GR4AD](../2602.22732-gr4ad/README.md)：构造用户感知 Semantic ID，结合 LazyAR、可变长度生成和 RSPO 完成生成式广告召回。
- [SIGMA](../2602.22913-sigma/README.md)：用 LLM 对物品做多视角语义 grounding，以混合 SID/ID token 和多任务 SFT 训练生成式推荐器。
- [HiSAC](../2602.21009-hisac/README.md)：用层级投票把超长历史压缩为少量兴趣 agent，再做 query-conditioned soft routing。
- [ULTRA-HSTU](../2602.16986-ultra-hstu/README.md)：Meta 用 semi-local attention、LBSL 和 Mixture of Transducers 提升超长历史的训练与推理 scaling efficiency。
- [MFLI](../2602.16124-mfli/README.md)：Meta 将多切面 index 与 item 表示联合学习，并按请求动态分配 facet 召回预算。
- [MixFormer](../2602.14110-mixformer/README.md)：在统一 Transformer 中平衡 dense 特征交互与序列建模，并按预算选择可训练模块。
- [S-GRec](../2602.10606-s-grec/README.md)：以 LLM 个性化语义 judge 产生偏好监督，再用 A2PO 蒸馏到轻量 SID 生成器。
- [Kunlun](../2602.10016-kunlun/README.md)：Meta 在逐层 Transformer/Interaction 双 block 中组合 GDPA、HSP、全局交互与 CompSkip。
- [Self-Evolving RecSys](../2602.10226-self-evolving-rec/README.md)：让 LLM Agent 根据历史实验提出、评估和迭代推荐策略，形成自动改进闭环。
- [MDL](../2602.07520-mdl/README.md)：把 feature、scenario 和 task 统一 token 化，以 domain-feature attention 支持多分布推荐。
- [MSN](../2602.07526-msn/README.md)：用 Product-Key Memory 增加容量，只读取 top-k 槽位并门控融合 dense 主干。
- [TokenMixer-Large](../2602.06563-tokenmixer-large/README.md)：以 token mixing/reverting、head/token SwiGLU、间隔残差和辅助监督扩展排序模型。
- [DOS](../2602.04460-dos/README.md)：用协同/语义双流和正交 residual quantization 训练生成推荐 Semantic ID。

## 2026-01
- [OneMall](../2601.21770-onemall/README.md)：以场景 prompt、层级 Semantic ID 和跨行为融合统一多个电商推荐场景。
- [LLaTTE](../2601.20083-llatte/README.md)：把 LLM 语义特征与推荐表征结合，并面向大规模排序设计特征交互结构。
- [HyFormer](../2601.12681-hyformer/README.md)：联合编码用户序列与搜索 query，通过 query decoding 和 boosting 强化搜索推荐信号。
- [Podcast MTL](../2601.02306-podcast-mtl/README.md)：共享广告、推广与 organic stream 表征，改善 podcast 冷启动。

## 2025-12
- [HiGR](../2512.24787-higr/README.md)：联合 residual Semantic ID、粗到细 slate decoder 与 ORPO 列表偏好对齐。
- [HiGR](../2512.24787-higr/README.md)：先生成层级 Semantic ID 簇再解码物品 slate，并以 ORPO 做列表偏好对齐。
- [RecGPT-V2](../2512.14503-recgpt-v2/README.md)：把用户意图推理组织成层级 multi-agent 协作，并以 meta-prompt、压缩表示和约束偏好 RL 优化标签与解释。
- [RecGPT-V2](../2512.14503-recgpt-v2/README.md)：以层级意图 agents、混合压缩表示、meta-prompt 和约束偏好 RL 升级淘宝意图推理。

## 2025-11
- [DualGR](../2511.12518-dualgr/README.md)：长短兴趣双路由、约束 SID 和曝光感知生成召回。

## 2025-09
- [IntSR](../2509.21179-intsr/README.md)：显式/隐式意图和时间词表统一搜索与推荐生成。
- [OnePiece](../2509.18091-onepiece/README.md)：上下文工程、块级 latent reasoning 和级联多任务排序。
- [DRL-PUT](../2509.05292-drl-put/README.md)：从 logged ads behavior 学习相关性、新颖性和收益等排序 utility 的动态权重策略。

## 2025-10
- [OneTrans](../2510.26104-onetrans/README.md)：用统一因果 Transformer 覆盖多场景排序，并复用 KV cache 降低线上推理成本。
- [CRSD](../2510.11056-crsd/README.md)：用领域 reasoning teacher 和普通/推理双视图对比自蒸馏训练轻量在线学生。
- [PLUM](../2510.07784-plum/README.md)：对 LLM 进行推荐语料 CPT 与 SFT，并以 Semantic ID 生成物品序列。

## 2025-08
- [MPFormer](../2508.20400-mpformer/README.md)：任务条件化序列检索和资源自适应共享。
- [OneRec-V2](../2508.20900-onerec-v2/README.md)：使用 lazy decoder 降低生成延迟，并用真实反馈强化学习和 GBPO 优化推荐序列。
- [SaviorRec](../2508.01375-saviorrec/README.md)：用行为监督训练内容编码器，生成 RQ Semantic ID，并通过多行为适配模块改善冷启动。

## 2025-07
- [ARGUS](../2507.15994-argus/README.md)：分解用户反馈与物品表示，在大规模 Transformer 中联合建模音乐序列。
- [RankMixer](../2507.15551-rankmixer/README.md)：交替进行 token mixing 与逐 token FFN，并探索稀疏 MoE 以扩展工业排序网络。
- [Click A, Buy B](../2507.15113-click-a-buy-b/README.md)：显式区分点击 A 后购买 A/B 的归因路径，并用 taxonomy-aware weighting 共享跨物品信号。
- [Click A, Buy B](../2507.15113-click-a-buy-b/README.md)：拆分同物品 CABA 与跨物品 CABB 转化归因，并用商品 taxonomy 建立协同权重。
- [PinFM](../2507.12704-pinfm/README.md)：以 DCAT 等序列模块构建推荐 foundation model，并通过预训练—微调适配多个流量场景。

## 2025-06
- [MGOE](../2506.10520-mgoe/README.md)：从任务统计构建 Macro Task Merging Graph，在 graph experts 中传播关系后分别预测各目标。
- [MGOE](../2506.10520-mgoe/README.md)：构建宏观任务合并图，让 graph experts 显式传播多任务关系后进入独立预测塔。
- [RADAR](../2506.07261-radar/README.md)：延迟异步全库排序结果回流下一请求召回。
- [TransAct V2](../2506.02267-transact-v2/README.md)：用候选感知的终身行为序列和 next-action 多任务目标增强 Homefeed 排序。

## 2025-05
- [SORT-Gen](../2505.07197-sort-gen/README.md)：用 ordered-regression Transformer 预测多目标前缀价值，再以多目标队列、mask-driven selection 和 MMR 生成 slate。
- [GenRank](../2505.04180-genrank/README.md)：把多种用户动作编码为生成目标，通过 action-oriented generation 完成端到端排序。
- [LONGER](../2505.04421-longer/README.md)：结合混合注意力、InnerTrans、token merge 与 KV cache，扩展超长用户行为序列建模。

## 2025-04
- [PinRec](../2504.10507-pinrec/README.md)：根据目标 outcome 生成多 token 物品表示，以条件生成方式完成召回。

## 2025-03
- [COBRA](../2503.02453-cobra/README.md)：先用稀疏生成缩小候选空间，再用稠密生成细排，形成级联式生成召回。

## 2025-02
- [OneRec](../2502.18965-onerec/README.md)：把 session 推荐建模为 Semantic ID 序列生成，并结合 MoE 与偏好优化对齐真实反馈。
- [FilterLLM](../2502.16924-filterllm/README.md)：将新品文本直接生成为用户分布，并用行为信号校准十亿级冷启动召回。
- [FilterLLM](../2502.16924-filterllm/README.md)：把新品文本映射到用户词表分布，并用历史行为约束冷启动召回。
- [SERAL](../2502.13539-seral/README.md)：构建用户认知画像，用 IPO 对齐惊喜度偏好，并通过 nearline 链路注入推荐排序。
- [SessionRec](../2502.10157-sessionrec/README.md)：按真实 session 生成候选，并利用曝光负例和 hard negative 改善会话级召回。
- [LUM](../2502.08309-lum/README.md)：通过 next-condition-item 预训练和 group query 压缩用户知识，再把生成表征注入判别式排序器。
- [FuXi-α](../2502.03036-fuxi-alpha/README.md)：以自适应多通道注意力和分阶段 FFN 扩展推荐特征交互容量。
- [FuXi-α](../2502.03036-fuxi-alpha/README.md)：用多通道注意力和 multi-stage FFN 扩展特征交互模型容量。
- [MIM](../2502.00321-mim/README.md)：以多模态遮盖预训练、内容兴趣 SFT 与 CiUBM 把内容语义注入用户行为建模。
- [MIM](../2502.00321-mim/README.md)：以遮盖多模态预训练和内容兴趣 SFT 对齐内容/协同空间，再由 CiUBM 融合排序。

## 2025-01
- [AdaF²M²](../2501.15816-adaf2m2/README.md)：通过 feature-mask 多次前向学习完整表征，再按用户/物品状态动态调节 adapter。

## 2025-01
- [AdaF²M²](../2501.15816-adaf2m2/README.md)：用 feature-mask multi-forward 学习全面特征，再由 state-aware adapter 响应不同用户/物品状态。

## 2024-12
- [MSD](../2412.06860-msd/README.md)：把 teacher 的用户知识自回归蒸馏到小模型，再通过 LoRA 和缓存表征对齐 CTR 任务。
- [PRECISE](../2412.06308-precise/README.md)：联合 LLM 语义 token 与协同 ID，使用 top-k MoE 和通用/目标训练建模序列推荐。

## 2024-11
- [LEADRE](../2411.13789-leadre/README.md)：生成意图感知 Semantic ID，并通过 DPO 对齐广告展示与转化偏好。

## 2024-07
- [TWIN-V2](../2407.16357-twin-v2/README.md)：离线压缩生命周期行为，在线以 GSU/ESU 完成候选相关粗搜与精确建模。

## 2024-06
- [CDM](../2406.09021-cdm/README.md)：将上下文多样性教师蒸馏到低延迟混排学生。
- [CWM](../2406.07932-cwm/README.md)：以反事实 watch time 消除视频时长偏置。

## 2024-05
- [LEARN](../2405.03988-learn/README.md)：冻结 LLM 生成内容增强表征，再通过协同域适配改善冷启动和长尾推荐。

## 2024-03
- [BAHE](../2403.19347-bahe/README.md)：缓存每个原子行为的浅层语言表示，只在线聚合高层序列，从而降低长文本 CTR 建模成本。
- [LSVCR](../2403.13574-lsvcr/README.md)：用 LoRA 学习 LLM 偏好，通过 SSC/VCC 双序列目标对齐评论语义和用户行为。
- [NoteLLM](../2403.01744-notellm/README.md)：把内容压缩到特殊 token，以 GCL 注入协同信号，并用 CSFT 保持生成能力。

## 2024-02
- [HSTU](../2402.17152-hstu/README.md)：以分层顺序转导单元建模超长行为历史，用生成式目标统一大规模推荐排序。

## 2023-11
- [BEQUE](../2311.03758-beque/README.md)：生成用户相关的搜索改写，并结合离线检索反馈、自采样与偏好排序优化改写质量。

## 2023-06
- [KAR](../2306.10933-kar/README.md)：让 LLM 生成用户偏好与物品事实知识，再由 hybrid-expert adapter 融合进传统推荐模型。

## 2023-05
- [TIGER](../2305.05065-tiger/README.md)：用 RQ-VAE 把物品量化为层级 Semantic ID，再通过自回归模型直接生成召回结果。

## 2022-05
- [M6-Rec](../2205.08084-m6rec/README.md)：把推荐任务统一改写为自然语言任务，在预训练语言模型上使用轻量 option-adapter 完成多场景适配。

## 2020-09
- [PLE](../recsys2020-ple-ple/README.md)：把专家拆成共享组与任务专属组，并由 CGC gate 渐进抽取共性和个性信息。

## 2020-08
- [DCN-V2](../2008.13535-dcn-v2/README.md)：用低秩 cross experts 和 gate 显式学习高阶特征交互。

## 2020-06
- [SIM](../2006.05639-sim/README.md)：先按候选搜索超长历史中的相关行为，再以精确搜索单元汇聚兴趣。

## 2019-05
- [BST](../1905.06874-bst/README.md)：用候选参与的 Transformer 建模电商用户行为序列。

## 2018-09
- [DIEN](../1809.03672-dien/README.md)：以辅助监督 GRU 抽取兴趣，再让候选相关门控控制兴趣演化。

## 2018-08
- [SASRec](../1808.09781-sasrec/README.md)：用因果自注意力编码用户行为序列，并预测下一物品，作为经典序列推荐基线。
- [MMoE](../kdd2018-mmoe-mmoe/README.md)：让每个任务用独立 gate 组合共享 experts，缓解任务相关性变化造成的负迁移。

## 2018-04
- [ESMM](../1804.07931-esmm/README.md)：在全曝光空间联合学习 CTR 与 CTCVR，并用概率乘积分解缓解 CVR 样本选择偏差。

## 2017-06
- [DIN](../1706.06978-din/README.md)：用候选物品感知的局部激活单元，从用户历史中动态提取相关兴趣，并以 Dice 激活训练 CTR 排序模型。

## 2017-03
- [DeepFM](../1703.04247-deepfm/README.md)：让 FM 二阶交互与深层网络共享 field embedding，端到端学习低阶和高阶组合。

## 2016-09
- [YouTube DNN](../recsys2016-youtube-dnn-youtube-dnn/README.md)：聚合观看历史并用非线性用户塔生成向量，再通过 item embedding 近邻召回候选。

## 2016-06
- [Wide & Deep](../1606.07792-wide-deep/README.md)：联合记忆型 wide 交叉和泛化型 deep tower，是工业深度推荐的经典起点。
