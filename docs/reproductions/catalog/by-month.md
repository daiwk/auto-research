# 按年月

同月论文保留在同一小节，但每篇独占一行，并附主要方法简介。

## 2026-07

- [DynamicRubric](../2607.20083-dynamic-rubric/README.md)：根据当前回答集合动态生成 rubric，以区分性和锚定目标让 evaluator 与 policy 多轮协同进化。
- [TSGR](../2607.18796-tsgr/README.md)：把 residual semantic prefix 与并行全局/query 价值码结合，再由联合 VRM 完成价值感知生成召回。
- [Off-Context GRPO](../2607.19313-off-context-grpo/README.md)：用含特权解题过程的 behavior policy 增加成功 rollout，并以 importance ratio 校正无提示目标。
- [RAMP](../2607.17473-ramp/README.md)：显式训练个性化和公共字段双路径，用 feature mask 与 prediction alignment 适配隐私受限流量。
- [WHALE](../2607.17017-whale/README.md)：逐层交换 Wukong 特征交互分支与 HSTU 行为序列分支，构成统一可扩展排序模型。
- [TMallGS](../2607.13398-tmallgs/README.md)：以 field-wise QKV、噪声门控、FiLM 和逐层误差监督统一电商搜索异构字段。
- [Long-History User Transformers](../2607.14331-long-history-transformer/README.md)：离线编码完整历史并缓存固定状态，在线仅融合近期行为以控制广告排序延迟。
- [Downstream Rewards](../2607.14192-downstream-rewards/README.md)：筛选与未来参与度相关的 session reward，并通过模型无关 reward heads 接入多个推荐 surface。
- [RecGPT-V3](../2607.15591-recgpt-v3/README.md)：用可演化 Memory Hub、文本/SID 混合基础模型和可重建 latent reasoning 同时改进长期用户理解、商品 grounding 与推理效率。
- [SlimPer](../2607.12281-slimper/README.md)：通过固定知识库的 Select–Match–Refine 循环替代全序列逐层传播，降低长历史排序的计算和中间状态。
- [Convolution for LLMs](../2607.18413-conv-llm/README.md)：在 Q/K/V 投影后加入 `k=3` residual depthwise Conv1D，以低参数成本增强局部 token 交互。
- [PPL-Factory](../2607.18199-ppl-factory/README.md)：用任务相关 NLL 衡量训练样本难度，再根据数据预算选择 easy、middle 或中段随机子集。
- [UAME](../2607.17092-uame/README.md)：联合预测满意度均值和不确定性，以概率 pairwise loss 和冲突加权缓解多目标标签偏差。
- [RECAP](../2607.15730-recap/README.md)：维护固定容量流式语义画像，并把历史推荐反馈训练成 GRPO reward，形成画像优化闭环。
- [Proximity Features](../2607.12246-proximity-features/README.md)：自适应聚合地理群体行为，为匿名用户提供不依赖持久 ID 的冷启动信号。
- [MESH](../2607.12392-mesh/README.md)：用异构模块塔和 residual gated bias correction 保护 fresh 内容的缩放收益。
- [DANet](../2607.12578-danet/README.md)：融合兴趣建模、折扣时频分解与个性化折扣偏好预测 CVR。
- [SAM](../2607.12714-sam/README.md)：学习购买后兴趣退出及恢复节奏，在注意力层抑制重复推荐。
- [NONTP](../2607.12277-nontp/README.md)：通过 TCL 感知多步未来轨迹，并以 TDL 为跨域目标增加共享预测头的第二条梯度路径。
- [Prompt Generation](../2607.11326-prompt-generation/README.md)：把异构特征组织成配置驱动的生成提示，通过 token 压缩和多种合并策略服务搜索与推荐召回。
- [SIS](../2607.04728-sis/README.md)：依据样本重要性动态调整训练权重，使有限预算更集中于高价值序列与 token。
- [Cluster GOOBS](../2607.00448-cluster-goobs/README.md)：在线聚类用户或物品表征，并以 cluster-aware sampler 改善训练样本覆盖和头部集中。

## 2026-06

- [G2Rec](../2606.20554-g2rec/README.md)：构建可微 soft graph，并联合图结构与生成式双目标学习用户—物品关系。
- [CMSL](../2606.28533-cmsl/README.md)：用可学习兴趣 lenses 拆分多兴趣序列，并结合 HSTU 建模不同语义 strand。

## 2026-05

- [RecGPT-Mobile](../2605.04726-recgpt-mobile/README.md)：将 LoRA+INT8 小模型部署到端侧，通过预算约束 prompt 和 entropy/Jaccard/JS 漂移分数按需生成用户意图。
- [FLUID](../2605.21832-fluid/README.md)：将直播多模态切片离散为 slice/room LUCID，以独立 prefix token 晚融合并逐阶段退掉候选 item ID。
- [Memory Grafting](../2605.20948-memory-grafting/README.md)：离线构造冻结 n-gram hidden memory，recipient 通过最长后缀匹配、Engram fallback 与门控写入复用知识。
- [GrowthGR](../2605.17994-growthgr/README.md)：用 ItemLTV 与多价值 MoPO 引导生成式召回发现高潜新品。
- [HARNESS-LM](../2605.23572-harness-lm/README.md)：以 teacher、L2 对齐和对比精修三阶段训练轻量非对称检索器。
- [DeGRe](../2605.25749-degre/README.md)：将离线 lookahead evaluator 的列表价值蒸馏成在线 dense 生成监督。
- [AKT-Rec](../2605.23310-akt-rec/README.md)：用 LLM Semantic ID 构造语义簇，以非对称对比学习和活动度门控把头部知识迁移到长尾。
- [UniVA](../2605.05803-univa/README.md)：用 Commercial SID 和 generation-as-ranking 统一广告生成，并通过价值对齐 RL 与 trie beam 优化收益。
- [MM-LLM](../2605.09338-mm-llm/README.md)：把多模态内容转成 caption/token 特征，再注入推荐模型增强内容理解。
- [LWGR](../2605.18771-lwgr/README.md)：把个性化 soft instruction 注入 LLM 世界知识，并用交叉注意力和拉格朗日约束与推荐分数融合。
- [MDCNS](../2605.19651-mdcns/README.md)：从多种负样本分布协同采样，并通过双模型更新降低单一采样偏差。
- [LLM Retrieval](../2605.21969-llm-ad-retrieval/README.md)：通过 domain SFT 生成层级广告属性，构建语义图并约束召回结果对属性扰动的稳定性。
- [Memento](../2605.24051-memento/README.md)：采用 query-conditioned MMR 在相关性与多样性之间动态权衡，进行候选重排。
- [Pinterest Ads LLM](../2605.27856-pinterest-ads-llm/README.md)：对广告主列表进行 SFT/GRPO，让 LLM 作为传统广告召回与排序的补充预测器。
- [Rec-Distill](../2605.29755-rec-distill/README.md)：结合 batch 与 streaming teacher，把大模型知识蒸馏到轻量推荐 student，并优化跨任务可迁移性。

## 2026-04

- [MBGR](../2604.02684-mbgr/README.md)：以 business-aware SID、共享专家和动态标签路由统一多个业务域的生成式推荐。

## 2026-03

- [Cross-domain KD](../2603.28994-cross-domain-kd/README.md)：把 YouTube 等源域 teacher 的知识蒸馏到目标域，实现面向音乐发现的零样本迁移。

## 2026-02

- [GRC](../2602.23639-grc/README.md)：让生成式推荐器结构化地反思首错位置和语义属性，再纠正 SID 轨迹。
- [Self-Evolving RecSys](../2602.10226-self-evolving-rec/README.md)：让 LLM Agent 根据历史实验提出、评估和迭代推荐策略，形成自动改进闭环。
- [S-GRec](../2602.10606-s-grec/README.md)：以 LLM 个性化语义 judge 产生偏好监督，再用 A2PO 蒸馏到轻量 SID 生成器。
- [MixFormer](../2602.14110-mixformer/README.md)：在统一 Transformer 中平衡 dense 特征交互与序列建模，并按预算选择可训练模块。
- [GR4AD](../2602.22732-gr4ad/README.md)：构造用户感知 Semantic ID，结合 LazyAR、可变长度生成和 RSPO 完成生成式广告召回。
- [SIGMA](../2602.22913-sigma/README.md)：用 LLM 对物品做多视角语义 grounding，以混合 SID/ID token 和多任务 SFT 训练生成式推荐器。

## 2026-01

- [HyFormer](../2601.12681-hyformer/README.md)：联合编码用户序列与搜索 query，通过 query decoding 和 boosting 强化搜索推荐信号。
- [LLaTTE](../2601.20083-llatte/README.md)：把 LLM 语义特征与推荐表征结合，并面向大规模排序设计特征交互结构。

## 2025-12

- [mHC](../2512.24880-mhc/README.md)：以双随机流形约束多流 residual mixing，在保留信息交换的同时限制深层信号放大。

## 2025-10

- [PLUM](../2510.07784-plum/README.md)：对 LLM 进行推荐语料 CPT 与 SFT，并以 Semantic ID 生成物品序列。
- [OneTrans](../2510.26104-onetrans/README.md)：用统一因果 Transformer 覆盖多场景排序，并复用 KV cache 降低线上推理成本。

## 2025-08

- [SaviorRec](../2508.01375-saviorrec/README.md)：用行为监督训练内容编码器，生成 RQ Semantic ID，并通过多行为适配模块改善冷启动。
- [OneRec-V2](../2508.20900-onerec-v2/README.md)：使用 lazy decoder 降低生成延迟，并用真实反馈强化学习和 GBPO 优化推荐序列。

## 2025-07

- [PinFM](../2507.12704-pinfm/README.md)：以 DCAT 等序列模块构建推荐 foundation model，并通过预训练—微调适配多个流量场景。
- [RankMixer](../2507.15551-rankmixer/README.md)：交替进行 token mixing 与逐 token FFN，并探索稀疏 MoE 以扩展工业排序网络。
- [ARGUS](../2507.15994-argus/README.md)：分解用户反馈与物品表示，在大规模 Transformer 中联合建模音乐序列。

## 2025-06

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

- [LUM](../2502.08309-lum/README.md)：通过 next-condition-item 预训练和 group query 压缩用户知识，再把生成表征注入判别式排序器。
- [SessionRec](../2502.10157-sessionrec/README.md)：按真实 session 生成候选，并利用曝光负例和 hard negative 改善会话级召回。
- [SERAL](../2502.13539-seral/README.md)：构建用户认知画像，用 IPO 对齐惊喜度偏好，并通过 nearline 链路注入推荐排序。
- [OneRec](../2502.18965-onerec/README.md)：把 session 推荐建模为 Semantic ID 序列生成，并结合 MoE 与偏好优化对齐真实反馈。

## 2024-12

- [PRECISE](../2412.06308-precise/README.md)：联合 LLM 语义 token 与协同 ID，使用 top-k MoE 和通用/目标训练建模序列推荐。
- [MSD](../2412.06860-msd/README.md)：把 teacher 的用户知识自回归蒸馏到小模型，再通过 LoRA 和缓存表征对齐 CTR 任务。

## 2024-11

- [LEADRE](../2411.13789-leadre/README.md)：生成意图感知 Semantic ID，并通过 DPO 对齐广告展示与转化偏好。

## 2024-05

- [LEARN](../2405.03988-learn/README.md)：冻结 LLM 生成内容增强表征，再通过协同域适配改善冷启动和长尾推荐。

## 2024-03

- [NoteLLM](../2403.01744-notellm/README.md)：把内容压缩到特殊 token，以 GCL 注入协同信号，并用 CSFT 保持生成能力。
- [LSVCR](../2403.13574-lsvcr/README.md)：用 LoRA 学习 LLM 偏好，通过 SSC/VCC 双序列目标对齐评论语义和用户行为。
- [BAHE](../2403.19347-bahe/README.md)：缓存每个原子行为的浅层语言表示，只在线聚合高层序列，从而降低长文本 CTR 建模成本。

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

## 2018-08

- [SASRec](../1808.09781-sasrec/README.md)：用因果自注意力编码用户行为序列，并预测下一物品，作为经典序列推荐基线。

## 2017-06

- [DIN](../1706.06978-din/README.md)：用候选物品感知的局部激活单元，从用户历史中动态提取相关兴趣，并以 Dice 激活训练 CTR 排序模型。
