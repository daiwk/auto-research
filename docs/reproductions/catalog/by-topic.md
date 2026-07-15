# 按主题

同一篇论文可以出现在多个主题下；每次出现都独占一行，并说明它与该主题相关的主要方法。

## LLM / Foundation model + Recommendation

- [AKT-Rec](../2605.23310-akt-rec/README.md)：用真实 LLM 对齐物品共现和用户兴趣，再以 Semantic ID 支持面向长尾的非对称知识迁移。
- [S-GRec](../2602.10606-s-grec/README.md)：用 LLM 个性化语义 judge 产生偏好监督，再以 A2PO 蒸馏到轻量生成器。
- [Pinterest Complementary LLM Predictor](../2605.27856-pinterest-ads-llm/README.md)：对广告主列表进行 SFT/GRPO，让 LLM 补充传统召回和排序特征。
- [LWGR](../2605.18771-lwgr/README.md)：把个性化 soft instruction 注入 LLM 世界知识，并用拉格朗日约束完成分数融合。
- [SIGMA](../2602.22913-sigma/README.md)：用 LLM 做多视角 grounding，并以混合 SID/ID token 训练七任务生成模型。
- [UniVA](../2605.05803-univa/README.md)：以 Commercial SID 和 generation-as-ranking 统一广告生成，再用价值对齐 RL 优化收益。
- [Prompt Generation](../2607.11326-prompt-generation/README.md)：把异构推荐特征转成 Qwen 生成提示，并通过 token 压缩与配置化合并完成召回。
- [PRECISE](../2412.06308-precise/README.md)：联合 LLM 语义 token 与协同 ID，通过 top-k MoE 和两阶段训练建模用户序列。
- [LUM](../2502.08309-lum/README.md)：通过 next-condition-item 与 group query 学习用户知识，再把生成表征注入判别模型。
- [MSD](../2412.06860-msd/README.md)：把 teacher 知识自回归蒸馏到 student，并用 LoRA 对齐 CTR 目标。
- [LSVCR](../2403.13574-lsvcr/README.md)：用 LoRA 学习 LLM 偏好，再通过 SSC/VCC 双序列目标对齐评论与行为。
- [LEARN](../2405.03988-learn/README.md)：冻结 LLM 生成内容增强表征，并用协同域适配改善冷启动。
- [NoteLLM](../2403.01744-notellm/README.md)：把内容压缩到特殊 token，以 GCL 注入协同信号，并用 CSFT 保持生成能力。
- [KAR](../2306.10933-kar/README.md)：让 LLM 生成用户偏好和物品事实知识，再由 hybrid-expert adapter 融合进推荐器。
- [BAHE](../2403.19347-bahe/README.md)：缓存原子行为的浅层语言编码，只在线执行高层行为聚合。
- [BEQUE](../2311.03758-beque/README.md)：生成 query rewrite，并用离线反馈、自采样和 PRO 优化改写质量。
- [M6-Rec](../2205.08084-m6rec/README.md)：把多种推荐任务统一成自然语言形式，并以 option-adapter 轻量适配预训练模型。
- [PLUM](../2510.07784-plum/README.md)：对 LLM 进行推荐语料 CPT 与 SFT，再以 Semantic ID 生成物品序列。
- [Self-Evolving RecSys](../2602.10226-self-evolving-rec/README.md)：让 LLM Agent 根据历史实验提出并评估推荐策略，形成自动研究闭环；当前属于概念验证。
- [PinFM](../2507.12704-pinfm/README.md)：构建推荐 foundation model，并通过预训练—微调适配多个流量场景。
- [LLaTTE](../2601.20083-llatte/README.md)：把 LLM 语义特征与推荐表征结合；当前本地实现仍属于概念验证。
- [LLM Retrieval](../2605.21969-llm-ad-retrieval/README.md)：用 domain SFT 生成层级广告属性，构建语义图并约束召回稳定性。
- [SERAL](../2502.13539-seral/README.md)：用 LLM 认知画像表示用户兴趣，再通过 IPO 与 nearline 链路优化惊喜度推荐。
- [LEADRE](../2411.13789-leadre/README.md)：以意图感知 Semantic ID 表示广告，并用 DPO 对齐展示与转化偏好。
- [MM-LLM](../2605.09338-mm-llm/README.md)：把多模态内容转为 LLM caption/token 特征，再注入推荐排序模型。
- [Cross-domain KD](../2603.28994-cross-domain-kd/README.md)：把源域大模型知识蒸馏到目标推荐域，实现零样本跨域迁移。

## 生成式召回与端到端推荐

- [NONTP](../2607.12277-nontp/README.md)：用 EMA 未来状态对比和跨域池化补充 NTP 监督，并在推理时移除全部辅助分支。
- [S-GRec](../2602.10606-s-grec/README.md)：用 LLM judge 生成个性化偏好监督，再通过 A2PO 蒸馏到 SID 生成器。
- [LWGR](../2605.18771-lwgr/README.md)：把 LLM 世界知识与推荐分数做约束融合，生成兼顾相关性与知识性的候选。
- [SIGMA](../2602.22913-sigma/README.md)：以多视角 grounding 和混合 SID/ID token 进行多任务生成式推荐。
- [UniVA](../2605.05803-univa/README.md)：使用 Commercial SID、generation-as-ranking 和价值引导 trie beam 生成广告候选。
- [Prompt Generation](../2607.11326-prompt-generation/README.md)：把异构特征压缩为生成提示，并以配置驱动方式支持多种召回合并策略。
- [SessionRec](../2502.10157-sessionrec/README.md)：按 session 自回归生成候选，并结合曝光负例与 hard negative 训练。
- [PinRec](../2504.10507-pinrec/README.md)：根据目标 outcome 条件生成多 token 物品表示，直接完成召回。
- [GenRank](../2505.04180-genrank/README.md)：把点击、互动等动作编码成生成目标，以 action-oriented generation 完成排序。
- [TIGER](../2305.05065-tiger/README.md)：先用 RQ-VAE 构造层级 Semantic ID，再自回归生成目标物品。
- [OneRec](../2502.18965-onerec/README.md)：把推荐建模为 session Semantic ID 序列生成，并用 MoE 与偏好优化对齐反馈。
- [OneRec-V2](../2508.20900-onerec-v2/README.md)：用 lazy decoder 提升生成效率，并通过真实反馈 RL 与 GBPO 优化序列。
- [G2Rec](../2606.20554-g2rec/README.md)：联合 soft graph 与生成式双目标学习结构化用户—物品关系。
- [HSTU](../2402.17152-hstu/README.md)：用分层顺序转导单元和生成式目标统一超长序列推荐。
- [CMSL](../2606.28533-cmsl/README.md)：以可学习 lenses 切分多兴趣 strand，再使用 HSTU 生成推荐结果。
- [COBRA](../2503.02453-cobra/README.md)：级联稀疏生成与稠密生成，在逐级缩小空间的同时保持精排能力。
- [GR4AD](../2602.22732-gr4ad/README.md)：结合用户感知 Semantic ID、LazyAR 和可变长度生成完成广告召回。
- [LEADRE](../2411.13789-leadre/README.md)：生成意图感知 Semantic ID，并用 DPO 对齐广告序列的业务偏好。

## 排序网络与长序列

- [DIN](../1706.06978-din/README.md)：使用候选感知局部激活从历史行为中提取相关兴趣，是经典 CTR 排序结构。
- [SASRec](../1808.09781-sasrec/README.md)：以因果自注意力编码行为序列，并预测下一物品。
- [LONGER](../2505.04421-longer/README.md)：结合混合注意力、InnerTrans、token merge 与 KV cache 扩展超长序列。
- [RankMixer](../2507.15551-rankmixer/README.md)：交替使用 token mixing 与逐 token FFN，并探索稀疏 MoE 扩容。
- [HyFormer](../2601.12681-hyformer/README.md)：联合用户序列与 query decoding，通过 query boosting 强化搜索排序。
- [OneTrans](../2510.26104-onetrans/README.md)：用统一因果 Transformer 覆盖多场景排序，并复用 KV cache。
- [MixFormer](../2602.14110-mixformer/README.md)：在统一网络中融合 dense 特征交互和序列建模，并按预算选择训练模块。
- [TransAct V2](../2506.02267-transact-v2/README.md)：以候选感知终身序列和 next-action 多任务目标增强排序。
- [Memento](../2605.24051-memento/README.md)：用 query-conditioned MMR 动态平衡相关性与多样性。
- [ARGUS](../2507.15994-argus/README.md)：分解用户反馈与物品表示，在 Transformer 中建模超长音乐序列。

## 冷启动与语义-行为对齐

- [PRECISE](../2412.06308-precise/README.md)：联合 LLM 语义 token 与协同 ID，并针对冷启动物品进行序列预训练。
- [LLM Retrieval](../2605.21969-llm-ad-retrieval/README.md)：生成 creative 层级语义属性，并用 primary/shadow 机制稳定广告召回。
- [SaviorRec](../2508.01375-saviorrec/README.md)：用行为监督训练内容 encoder，生成 RQ Semantic ID，再通过多行为模块对齐冷启动物品。

## 采样、蒸馏与强化学习

- [S-GRec](../2602.10606-s-grec/README.md)：只采样少量 PSJ 反馈，并用 advantage 符号门控和幅度约束稳定 A2PO。
- [Pinterest Complementary LLM Predictor](../2605.27856-pinterest-ads-llm/README.md)：先用 SFT 学习广告主列表，再以 GRPO 奖励优化列表质量。
- [LWGR](../2605.18771-lwgr/README.md)：用 reference confidence 约束融合结果，并通过 primal-dual 更新拉格朗日乘子。
- [UniVA](../2605.05803-univa/README.md)：在请求内归一化 eCPM reward，并交替执行监督学习与强化学习。
- [BEQUE](../2311.03758-beque/README.md)：结合离线检索反馈、自采样和 PRO，优化生成式 query rewrite。
- [MDCNS](../2605.19651-mdcns/README.md)：从多种负样本分布协同采样，并通过双模型交替更新减少偏差。
- [Cluster GOOBS](../2607.00448-cluster-goobs/README.md)：用在线聚类感知的 sampler 扩大样本覆盖并缓解头部集中。
- [Rec-Distill](../2605.29755-rec-distill/README.md)：结合 batch/stream teacher，把大模型知识蒸馏到轻量 student。
- [OneRec-V2](../2508.20900-onerec-v2/README.md)：利用真实时长反馈和 GBPO 对生成序列进行强化学习。
- [SIS](../2607.04728-sis/README.md)：依据样本重要性动态分配训练权重，把预算集中到高价值 token。
- [SERAL](../2502.13539-seral/README.md)：通过 IPO 对齐惊喜度偏好，并在 nearline 链路应用认知画像。
- [LEADRE](../2411.13789-leadre/README.md)：使用 DPO 对齐 Semantic ID 生成与广告转化偏好。
- [GR4AD](../2602.22732-gr4ad/README.md)：通过 RSPO 优化可变长度广告生成，并结合 LazyAR 降低推理成本。
- [Cross-domain KD](../2603.28994-cross-domain-kd/README.md)：把源域 teacher 知识蒸馏到目标域，减少跨域冷启动监督需求。

## Serving / efficiency

- [S-GRec](../2602.10606-s-grec/README.md)：LLM judge 只在训练期调用，线上仅部署轻量 SID generator。
- [Pinterest Complementary LLM Predictor](../2605.27856-pinterest-ads-llm/README.md)：离线批量生成 advertiser prior，线上作为传统候选生成的补充信号。
- [LWGR](../2605.18771-lwgr/README.md)：在 nearline 阶段缓存世界知识，线上只执行轻量 cross-attention 融合。
- [SIGMA](../2602.22913-sigma/README.md)：使用 prefix-local item retrieval 和 nearline U2I 控制生成检索成本。
- [UniVA](../2605.05803-univa/README.md)：按请求构造个性化 trie，并用 value-guided beam search 约束有效广告路径。
- [Prompt Generation](../2607.11326-prompt-generation/README.md)：训练和 serving 共享特征配置，并通过 event replay 与 token compression 控制延迟。
- [MSD](../2412.06860-msd/README.md)：把 teacher 知识蒸馏到小模型，并以 LoRA 与缓存表征控制 CTR serving 成本。
- [BAHE](../2403.19347-bahe/README.md)：缓存原子行为的浅层编码，只在线执行高层序列聚合。
- [BEQUE](../2311.03758-beque/README.md)：将检索反馈放在离线训练阶段，线上只保留轻量 query 生成。
- [M6-Rec](../2205.08084-m6rec/README.md)：冻结大部分预训练语言模型，仅用 option-adapter 适配推荐任务。
- [OneRec-V2](../2508.20900-onerec-v2/README.md)：用 lazy decoder 和并行策略降低生成式推荐延迟。
- [OneTrans](../2510.26104-onetrans/README.md)：在多场景间共享因果 Transformer，并复用 KV cache 加速线上推理。
- [LONGER](../2505.04421-longer/README.md)：通过 token merge、混合注意力和缓存降低超长序列 serving 成本。
