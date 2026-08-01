# 按公司

每篇论文独占一行；简介只概括主要方法，实验效果与复现边界请进入单篇文档查看。

## Alibaba
- 2026-07 · [SWAG](../2607.25233-swag-bid/README.md)：以 masked future plan 和滑动窗口目标进行长周期生成式自动出价。
- 2026-07 · [TSGR](../2607.18796-tsgr/README.md)：用 residual semantic prefix 加并行全局/query 价值码生成候选，再以联合 VRM 把相关性与商业价值统一排序。
- 2026-07 · [RecGPT-V3](../2607.15591-recgpt-v3/README.md)：以可增量 Memory Hub 压缩长期行为，把文本与商品 Semantic ID 统一进基础模型，再将显式 CoT 蒸馏为可重建 latent intent token。
- 2026-07 · [TMallGS](../2607.13398-tmallgs/README.md)：通过 field-wise QKV、噪声门控、FiLM 与 progressive supervision 统一 query、行为和商品字段。
- 2026-07 · [DANet](../2607.12578-danet/README.md)：对折扣率时间序列做高低频分解，并用用户折扣偏好和促销上下文修正 CVR 预测。
- 2026-07 · [SAM](../2607.12714-sam/README.md)：学习购买后的兴趣退出与个性化恢复周期，通过 ASGU 在注意力 logit 上动态压制重复意图。
- 2026-07 · [Prompt Generation](../2607.11326-prompt-generation/README.md)：把异构特征组织成配置驱动的生成提示，通过 token 压缩和多种合并策略服务搜索与推荐召回。
- 2026-06 · [EvoRec](../2606.28368-evorec/README.md)：让模型候选和优化方法双轨进化，并从持久实验记忆中提炼下一代可复用技能。
- 2026-05 · [DeGRe](../2605.25749-degre/README.md)：离线用累计价值评估器做前瞻 beam 搜索，把逐前缀 dense 价值分布蒸馏到在线单次生成器。
- 2026-05 · [AKT-Rec](../2605.23310-akt-rec/README.md)：用 LLM 对齐内容与协同信号并生成层级 Semantic ID，通过非对称 head-to-tail 迁移改善长尾 CTR 排序。
- 2026-05 · [GrowthGR](../2605.17994-growthgr/README.md)：用 ItemLTV 估计新品点击的长期增量，并以多价值 MoPO 对 Semantic ID 生成策略做偏好对齐。
- 2026-05 · [CQ-SID](../2605.14434-cq-sid/README.md)：用类目约束残差 Semantic ID 表示商品，再以多专家奖励和 EG-GRPO 优化生成检索。
- 2026-05 · [RecGPT-Mobile](../2605.04726-recgpt-mobile/README.md)：在端侧用量化 LoRA LLM 把异构行为翻译成下一意图 query，并以 adaptive prompt 和漂移触发控制资源消耗。
- 2026-05 · [LWGR](../2605.18771-lwgr/README.md)：把个性化 soft instruction 注入 LLM 世界知识，并用交叉注意力和拉格朗日约束与推荐分数融合。
- 2026-02 · [GRC](../2602.23639-grc/README.md)：把生成、首错位置/属性反思和纠正串成结构化轨迹，再以 GRPO 与熵调度优化有限纠错预算。
- 2026-02 · [SIGMA](../2602.22913-sigma/README.md)：用 LLM 对物品做多视角语义 grounding，以混合 SID/ID token 和多任务 SFT 训练生成式推荐器。
- 2026-02 · [HiSAC](../2602.21009-hisac/README.md)：用层级投票生成少量兴趣 agent，再对超长历史做 query-conditioned soft routing。
- 2025-12 · [RecGPT-V2](../2512.14503-recgpt-v2/README.md)：以层级意图 agents、混合压缩表示、meta-prompt 和约束偏好 RL 升级淘宝意图推理。
- 2025-08 · [SaviorRec](../2508.01375-saviorrec/README.md)：用行为监督训练内容编码器，生成 RQ Semantic ID，并通过多行为适配模块改善冷启动。
- 2025-06 · [MGOE](../2506.10520-mgoe/README.md)：构建宏观任务合并图，让 graph experts 显式传播多任务关系后进入独立预测塔。
- 2025-05 · [SORT-Gen](../2505.07197-sort-gen/README.md)：用 causal Transformer ordered regression 估计列表前缀多目标价值，再以目标队列、mask 和 MMR 单次批量生成 slate。
- 2025-05 · [Gated Attention](../2505.06708-gated-attention/README.md)：在每个 softmax attention head 的 SDPA 输出后施加 query-dependent sigmoid gate，增强非线性并抑制无用输出。
- 2025-02 · [FilterLLM](../2502.16924-filterllm/README.md)：把新品文本一次性映射到用户词表分布，并用历史行为约束冷启动召回。
- 2025-02 · [SERAL](../2502.13539-seral/README.md)：构建用户认知画像，用 IPO 对齐惊喜度偏好，并通过 nearline 链路注入推荐排序。
- 2025-02 · [LUM](../2502.08309-lum/README.md)：通过 next-condition-item 预训练和 group query 压缩用户知识，再把生成表征注入判别式排序器。
- 2025-02 · [MIM](../2502.00321-mim/README.md)：以遮盖多模态预训练和内容兴趣感知 SFT 对齐内容/协同空间，再由 CiUBM 融合排序。
- 2023-11 · [BEQUE](../2311.03758-beque/README.md)：生成用户相关的搜索改写，并结合离线检索反馈、自采样与偏好排序优化改写质量。
- 2022-05 · [M6-Rec](../2205.08084-m6rec/README.md)：把推荐任务统一改写为自然语言任务，在预训练语言模型上使用轻量 option-adapter 完成多场景适配。
- 2019-05 · [BST](../1905.06874-bst/README.md)：把候选商品作为 token 与用户行为共同送入 Transformer，显式建模序列内依赖。
- 2018-09 · [DIEN](../1809.03672-dien/README.md)：用 GRU 抽取逐步兴趣，以下一行为辅助监督并由候选相关门控控制兴趣演化。
- 2018-04 · [ESMM](../1804.07931-esmm/README.md)：在全曝光空间联合训练 CTR 与 CTCVR，并用 pCTR×pCVR 缓解点击后转化的选择偏差。
- 2017-06 · [DIN](../1706.06978-din/README.md)：用候选物品感知的局部激活单元，从用户历史中动态提取相关兴趣，并以 Dice 激活训练 CTR 排序模型。

## Ant Group
- 2024-03 · [BAHE](../2403.19347-bahe/README.md)：缓存每个原子行为的浅层语言表示，只在线聚合高层序列，从而降低长文本 CTR 建模成本。

## Baidu
- 2025-03 · [COBRA](../2503.02453-cobra/README.md)：先用稀疏生成缩小候选空间，再用稠密生成细排，形成级联式生成召回。

## ByteDance / Douyin / TikTok
- 2026-05 · [Rec-Distill](../2605.29755-rec-distill/README.md)：结合 batch 与 streaming teacher，把大模型知识蒸馏到轻量推荐 student，并优化跨任务可迁移性。
- 2026-05 · [FLUID](../2605.21832-fluid/README.md)：把直播多模态切片量化成 slice/room 两级 LUCID，以 prefix n-gram late fusion 完全替代短生命周期候选 ID。
- 2026-02 · [MixFormer](../2602.14110-mixformer/README.md)：在统一 Transformer 中平衡 dense 特征交互与序列建模，并按预算选择可训练模块。
- 2026-02 · [MDL](../2602.07520-mdl/README.md)：把 feature、scenario、task 全部 token 化，并以 domain-feature attention 深层共享。
- 2026-02 · [MSN](../2602.07526-msn/README.md)：用两轴 Product-Key Memory 扩大参数容量，每次只激活 top-k 槽位并与 dense 主干门控融合。
- 2026-02 · [TokenMixer-Large](../2602.06563-tokenmixer-large/README.md)：交替执行无参数 token mixing、head-wise/token-wise SwiGLU，并以间隔残差和辅助头稳定深层扩容。
- 2026-01 · [HyFormer](../2601.12681-hyformer/README.md)：联合编码用户序列与搜索 query，通过 query decoding 和 boosting 强化搜索推荐信号。
- 2025-10 · [OneTrans](../2510.26104-onetrans/README.md)：用统一因果 Transformer 覆盖多场景排序，并复用 KV cache 降低线上推理成本。
- 2025-07 · [RankMixer](../2507.15551-rankmixer/README.md)：交替进行 token mixing 与逐 token FFN，并探索稀疏 MoE 以扩展工业排序网络。
- 2025-05 · [LONGER](../2505.04421-longer/README.md)：结合混合注意力、InnerTrans、token merge 与 KV cache，扩展超长用户行为序列建模。
- 2025-01 · [AdaF²M²](../2501.15816-adaf2m2/README.md)：通过 feature-mask 多次前向学习完整表征，再按用户/物品状态动态调节 adapter。

## Google / YouTube
- 2026-07 · [YouTube Freshness](../2607.23749-youtube-freshness/README.md)：比较 recency、IPS、bias tower 与不确定性探索对新内容反馈环的影响。
- 2026-03 · [Cross-domain KD](../2603.28994-cross-domain-kd/README.md)：把 YouTube 等源域 teacher 的知识蒸馏到目标域，实现面向音乐发现的零样本迁移。
- 2026-02 · [Self-Evolving RecSys](../2602.10226-self-evolving-rec/README.md)：让 LLM Agent 根据历史实验提出、评估和迭代推荐策略，形成自动改进闭环。
- 2025-10 · [PLUM](../2510.07784-plum/README.md)：对 LLM 进行推荐语料 CPT 与 SFT，并以 Semantic ID 生成物品序列。
- 2023-05 · [TIGER](../2305.05065-tiger/README.md)：用 RQ-VAE 把物品量化为层级 Semantic ID，再通过自回归模型直接生成召回结果。
- 2021-01 · [Switch Transformer](../2101.03961-switch-transformer/README.md)：让每个 token 只路由到一个 FFN expert，以近似固定计算扩展模型容量。
- 2020-08 · [DCN-V2](../2008.13535-dcn-v2/README.md)：用低秩 cross experts 与输入相关 gate 高效学习有界阶数特征交互。
- 2018-08 · [MMoE](../kdd2018-mmoe-mmoe/README.md)：为 CTR、转化等任务学习独立 gates，以不同权重组合同一组共享 experts。
- 2016-09 · [YouTube DNN](../recsys2016-youtube-dnn-youtube-dnn/README.md)：用观看历史聚合与深层用户塔学习候选召回向量，再做大规模 item 近邻检索。
- 2016-06 · [Wide & Deep](../1606.07792-wide-deep/README.md)：联合显式 wide 特征交叉与 deep tower，兼顾共现记忆和未见组合泛化。

## Huawei
- 2026-07 · [AdaDSF](../2607.21291-adadsf/README.md)：根据 dense 层输入/输出相似度分配逐层 token budget，用轻量 Top-K router 和特征对齐保留稀疏模型能力。
- 2026-07 · [RAMP](../2607.17473-ramp/README.md)：用个性化/公共双路径、可用性 mask 和 prediction-alignment 蒸馏提升缺失用户字段时的广告排序鲁棒性。
- 2026-03 · [Switch Attention](../2603.26380-switch-attention/README.md)：与北大合作学习逐 token full/local attention 路由，把全局计算集中到必要位置。
- 2025-02 · [FuXi-α](../2502.03036-fuxi-alpha/README.md)：用时间、语义等自适应多通道注意力和 multi-stage FFN 扩展推荐特征交互模型。
- 2023-06 · [KAR](../2306.10933-kar/README.md)：让 LLM 生成用户偏好与物品事实知识，再由 hybrid-expert adapter 融合进传统推荐模型。
- 2017-03 · [DeepFM](../1703.04247-deepfm/README.md)：用共享 embedding 联合 FM 二阶交互和 deep 高阶交互，减少手工特征交叉。

## NVIDIA
- 2026-07 · [Windowed-MTP](../2607.21535-windowed-mtp/README.md)：只让内置 MTP draft 读取 attention sink 与最近窗口，并由完整上下文 target 验证候选以保持输出分布不变。

## Kuaishou
- 2026-07 · [RecoReward](../2607.25901-reco-reward/README.md)：以目标/非目标推荐亲和力差作为多模态描述的训练奖励。
- 2026-07 · [TWICE](../2607.25404-twice/README.md)：用双时钟和双窗口校正在线广告长期延迟转化。
- 2026-07 · [UniR²](../2607.24439-unir2/README.md)：用统一 decoder 和 Dual-Query Prefix-Causal Attention 同时学习层级 SID 生成与多目标排序，并以 ranking-only LoRA 避免梯度冲突。
- 2026-07 · [UAME](../2607.17092-uame/README.md)：把满意度分数建模为均值—方差 Gaussian 变量，用多目标冲突产生的不确定性加权 pairwise 排序训练。
- 2026-07 · [RECAP](../2607.15730-recap/README.md)：把流式用户画像维护为固定容量语义状态，并用推荐反馈评价器和 GRPO 闭环优化画像更新策略。
- 2026-04 · [CS3](../2604.19269-cs3/README.md)：通过循环自修正、跨塔同步和级联教师信号增强仍可 ANN 服务的双塔模型。
- 2026-02 · [GR4AD](../2602.22732-gr4ad/README.md)：构造用户感知 Semantic ID，结合 LazyAR、可变长度生成和 RSPO 完成生成式广告召回。
- 2026-01 · [OneMall](../2601.21770-onemall/README.md)：以统一 Semantic ID、场景 prompt 和跨行为融合覆盖商品卡、短视频与直播生成推荐。
- 2025-08 · [OneRec-V2](../2508.20900-onerec-v2/README.md)：使用 lazy decoder 降低生成延迟，并用真实反馈强化学习和 GBPO 优化推荐序列。
- 2025-02 · [OneRec](../2502.18965-onerec/README.md)：把 session 推荐建模为 Semantic ID 序列生成，并结合 MoE 与偏好优化对齐真实反馈。
- 2024-05 · [LEARN](../2405.03988-learn/README.md)：冻结 LLM 生成内容增强表征，再通过协同域适配改善冷启动和长尾推荐。
- 2024-03 · [LSVCR](../2403.13574-lsvcr/README.md)：用 LoRA 学习 LLM 偏好，通过 SSC/VCC 双序列目标对齐评论语义和用户行为。

## Meituan
- 2026-07 · [CORE](../2607.24417-core-relevance/README.md)：把三级电商相关性拆成两道条件边界，以 step-GRPO 提供细粒度 credit，再将 PostCoT LLM 蒸馏到在线双头模型。
- 2026-07 · [NONTP](../2607.12277-nontp/README.md)：在 NTP 上加入未来状态对比学习和跨域 hidden-state pooling，扩大生成式推荐的训练监督覆盖。
- 2026-04 · [MBGR](../2604.02684-mbgr/README.md)：通过 business-aware SID、共享 MoE 和最近未来标签路由，同时学习多个业务域的生成目标。
- 2026-02 · [DOS](../2602.04460-dos/README.md)：用协同/语义双流和正交 residual quantization 对齐 SID codebook 与生成空间。
- 2025-02 · [SessionRec](../2502.10157-sessionrec/README.md)：按真实 session 生成候选，并利用曝光负例和 hard negative 改善会话级召回。
- 2024-12 · [MSD](../2412.06860-msd/README.md)：把 teacher 的用户知识自回归蒸馏到小模型，再通过 LoRA 和缓存表征对齐 CTR 任务。

## Meta
- 2026-07 · [ROCS](../2607.27744-rocs/README.md)：复用单次 request encoding，并在候选端执行轻量 late interaction，统一覆盖广告/自然流量的检索和排序 serving。
- 2026-07 · [Mosaic](../2607.24015-mosaic/README.md)：将多类用户 embedding 组织为 specialist fleet，并通过 MRM 联合标签与 cosine redundancy loss 保持新增表征的独特信息。
- 2026-07 · [Off-Context GRPO](../2607.19313-off-context-grpo/README.md)：只在训练采样时提供特权解题信息，并用重要性比率把更新校正回无提示目标策略。
- 2026-07 · [WHALE](../2607.17017-whale/README.md)：逐层耦合 Wukong 高阶特征交互和门控 HSTU 序列建模，形成共同扩展的统一排序模型。
- 2026-07 · [Looped Latent Attention](../2607.15456-looped-latent-attention/README.md)：UMD/Meta AI 在权重共享循环中复用低维 K/V latent，压缩跨 loop cache。
- 2026-07 · [SlimPer](../2607.12281-slimper/README.md)：用固定容量 user-item knowledge base 逐层查询完整历史，并通过 Select–Match–Refine 把计算集中到候选相关证据。
- 2026-07 · [Cluster GOOBS](../2607.00448-cluster-goobs/README.md)：在线聚类用户或物品表征，并以 cluster-aware sampler 改善训练样本覆盖和头部集中。
- 2026-06 · [CMSL](../2606.28533-cmsl/README.md)：用可学习兴趣 lenses 拆分多兴趣序列，并结合 HSTU 建模不同语义 strand。
- 2026-06 · [G2Rec](../2606.20554-g2rec/README.md)：构建可微 soft graph，并联合图结构与生成式双目标学习用户—物品关系。
- 2026-06 · [RankGraph-2](../2606.18379-rankgraph2/README.md)：用流行度校正边、离线多跳 PPR 和 residual cluster index 降低工业图召回的在线成本。
- 2026-05 · [Memento](../2605.24051-memento/README.md)：采用 query-conditioned MMR 在相关性与多样性之间动态权衡，进行候选重排。
- 2026-05 · [LLM Retrieval](../2605.21969-llm-ad-retrieval/README.md)：通过 domain SFT 生成层级广告属性，构建语义图并约束召回结果对属性扰动的稳定性。
- 2026-05 · [MM-LLM](../2605.09338-mm-llm/README.md)：把多模态内容转成 caption/token 特征，再注入推荐模型增强内容理解。
- 2026-04 · [SOLARIS](../2604.12110-solaris/README.md)：预测未来 user-item 请求，异步预计算 foundation-model latent，并通过 cache/fallback 服务线上排序。
- 2026-01 · [LLaTTE](../2601.20083-llatte/README.md)：把 LLM 语义特征与推荐表征结合，并面向大规模排序设计特征交互结构。
- 2024-02 · [HSTU](../2402.17152-hstu/README.md)：以分层顺序转导单元建模超长行为历史，用生成式目标统一大规模推荐排序。

## Pinterest
- 2026-07 · [PinEqualizer](../2607.22518-pinequalizer/README.md)：贯通探索 corpus、召回、排序与 utility，通过 engagement dropout、内容交叉、分 cohort calibration 和 UCB 缓解 fresh 内容反馈回路。
- 2026-07 · [Pin-SCALE](../sigir2026-pin-scale-pin-scale/README.md)：用 engagement-aware SID、级联 pooling 和多视角对比对齐接入 dense retrieval。
- 2026-07 · [Downstream Rewards](../2607.14192-downstream-rewards/README.md)：离线筛选能预测未来参与度的长期 reward，再以模型无关附加头接入多个推荐 surface。
- 2026-07 · [Causal Retrieval](../2607.14161-causal-retrieval/README.md)：用 doubly-robust uplift 决定是否触发 shopping candidate generator。
- 2026-07 · [MESH](../2607.12392-mesh/README.md)：把 user/item/context 特征放入独立放大塔，再用 residual gated bias correction 保护 fresh 内容信号。
- 2026-05 · [Complementary LLM Ads Predictor](../2605.27856-pinterest-ads-llm/README.md)：对广告主列表进行 SFT/GRPO，让 LLM 作为传统广告召回与排序的补充预测器。
- 2026-03 · [PinCLIP](../2603.03544-pinclip/README.md)：以 VLM 图文对齐加 Pin-Board 邻居目标改善 fresh 内容表征。
- 2025-09 · [DRL-PUT](../2509.05292-drl-put/README.md)：从 logged ads behavior 学习相关性、新颖性和收益等排序 utility 的动态权重策略。
- 2025-07 · [Click A, Buy B](../2507.15113-click-a-buy-b/README.md)：拆分同物品 CABA 与跨物品 CABB 转化归因，并用商品 taxonomy 建立协同权重。
- 2025-07 · [PinFM](../2507.12704-pinfm/README.md)：以 DCAT 等序列模块构建推荐 foundation model，并通过预训练—微调适配多个流量场景。
- 2025-06 · [TransAct V2](../2506.02267-transact-v2/README.md)：用候选感知的终身行为序列和 next-action 多任务目标增强 Homefeed 排序。
- 2025-04 · [PinRec](../2504.10507-pinrec/README.md)：根据目标 outcome 生成多 token 物品表示，以条件生成方式完成召回。

## Tencent / WeChat
- 2026-07 · [CCFormer](../2607.28070-ccformer/README.md)：分离 ID 与内容字段后门控融合，并以分层压缩保留近期细节和远期兴趣，服务腾讯视频推荐。
- 2026-07 · [ASARL](../2607.26593-asarl/README.md)：用 Reason/Critic/Gen 多 Agent 闭环整理社交搜索数据，再经 SCT、偏好优化和蒸馏得到在线相关性模型。
- 2026-07 · [BARGE](../2607.21028-barge/README.md)：用 item-level ICA 恢复多 token Semantic ID 边界，通过逐层 HPR 与正交双路径 DPD 抑制生成漂移。
- 2026-07 · [DynamicRubric](../2607.20083-dynamic-rubric/README.md)：根据当前回答集合动态生成 rubric 权重，以区分性和锚定目标驱动评估器与策略协同进化。
- 2026-06 · [NOVA](../2606.27243-nova/README.md)：以 architecture gradient 驱动候选修改，并用四级验证级联阻断可运行但语义错误的架构。
- 2026-05 · [UniVA](../2605.05803-univa/README.md)：用 Commercial SID 和 generation-as-ranking 统一广告生成，并通过价值对齐 RL 与 trie beam 优化收益。
- 2026-02 · [S-GRec](../2602.10606-s-grec/README.md)：以 LLM 个性化语义 judge 产生偏好监督，再用 A2PO 蒸馏到轻量 SID 生成器。
- 2025-12 · [HiGR](../2512.24787-higr/README.md)：先生成层级 Semantic ID 簇再解码物品 slate，并以 ORPO 做列表偏好对齐。
- 2024-12 · [PRECISE](../2412.06308-precise/README.md)：联合 LLM 语义 token 与协同 ID，使用 top-k MoE 和通用/目标训练建模序列推荐。
- 2024-11 · [LEADRE](../2411.13789-leadre/README.md)：生成意图感知 Semantic ID，并通过 DPO 对齐广告展示与转化偏好。
- 2020-09 · [PLE](../recsys2020-ple-ple/README.md)：把共享 experts 与任务专属 experts 分组，通过 CGC gates 逐层分离共性和任务特性。

## Xiaohongshu
- 2026-03 · [IDProxy](../2603.01590-idproxy/README.md)：先把多模态 LLM 表征对齐到协同 ID 空间，再通过多层 proxy adapter 和残差门控注入排序器。
- 2025-05 · [GenRank](../2505.04180-genrank/README.md)：把多种用户动作编码为生成目标，通过 action-oriented generation 完成端到端排序。
- 2024-03 · [NoteLLM](../2403.01744-notellm/README.md)：把内容压缩到特殊 token，以 GCL 注入协同信号，并用 CSFT 保持生成能力。

## Yandex
- 2026-07 · [Long-History User Transformers](../2607.14331-long-history-transformer/README.md)：用异步全历史 Transformer 生成固定缓存，线上只编码近期事件，在不重算长序列的情况下增强广告排序。
- 2025-07 · [ARGUS](../2507.15994-argus/README.md)：分解用户反馈与物品表示，在大规模 Transformer 中联合建模音乐序列。

## Microsoft / Bing Ads
- 2026-05 · [HARNESS-LM](../2605.23572-harness-lm/README.md)：先训练强检索 teacher，再以 L2 对齐和冻结文档塔对比精修压缩在线 query encoder。

## Tsinghua University / Microsoft Research Asia
- 2026-05 · [Memory Grafting](../2605.20948-memory-grafting/README.md)：用预训练 grafting model 离线构造冻结 n-gram hidden bank，通过最长匹配与 Engram fallback 扩展 recipient 容量。

## DeepSeek-AI
- 2026-01 · [Engram](../2601.07372-engram/README.md)：用确定性 hashed n-gram 查表给 LLM 增加 O(1) 条件记忆。
- 2025-12 · [mHC](../2512.24880-mhc/README.md)：将多流 Hyper-Connections 的残差映射投影到双随机矩阵流形，稳定深层信号传播。
- 2025-02 · [Native Sparse Attention](../2502.11089-native-sparse-attention/README.md)：联合可训练的压缩历史、query 选择 fine blocks 与局部滑窗，在保留全局/局部信息的同时减少长上下文注意力边。

## Airbnb
- 2026-07 · [Proximity Features](../2607.12246-proximity-features/README.md)：用自适应地理桶聚合群体行为，为无持久 user ID 的匿名用户提供隐私合规冷启动特征。

## Teads
- 2026-07 · [Open Web UFM](../2607.28019-open-web-ufm/README.md)：以开放网页用户行为做双裁剪对比预训练和 next-item 监督，再把共享 user encoder 迁移到广告 CTR 与访问预测。

## Independent researchers
- 2026-07 · [Möbius RoPE](../2607.21405-mobius-rope/README.md)：在部分 attention heads 上使用反周期频率梯度，以固定上下文边界的负 holonomy 改善长距检索稳定性。
- 2026-07 · [Naju](../2607.21000-naju/README.md)：直接参数化离散状态 pole，并以独立 retain/write gates、选择性 B/C 与短程卷积同时控制长期保留和覆盖写入。

## Spotify
- 2026-03 · [GLIDE](../2603.17540-glide/README.md)：用 residual Semantic ID 自回归检索，并联合近期历史与长期用户 soft prompt 扩大探索。
- 2026-01 · [Podcast MTL](../2601.02306-podcast-mtl/README.md)：共享广告、推广与 organic stream 表征，将高资源任务知识迁移给冷启动 podcast。

## NetEase
- 2026-07 · [Melo](../2607.23718-melo/README.md)：用多节点音乐 Agent、实体目录 grounding 和反思重试生成可靠 playlist。

## JD.com
- 2026-07 · [OxygenREC-v2](../2607.24255-oxygenrec-v2/README.md)：把 click/cart/order instruction 内化到 SID 生成，并用未来交互特权教师与熵路由蒸馏联合后训练。
- 2026-04 · [GenRec](../2604.14878-genrec/README.md)：把下一页作为联合生成目标，通过非对称 Token Merger 和带 NLL 约束的 GRPO-SR 优化整页。

## MiniMax
- 2026-06 · [MiniMax Sparse Attention](../2606.13392-minimax-sparse-attention/README.md)：轻量 index branch 为每个 GQA 组选择 top-k 历史块，主分支只对命中 token 做精确注意力。

## 学术与经典基线
- 2026-07 · [ReToken](../2607.28627-retoken/README.md)：UIUC、Microsoft Research 与 Google DeepMind 用单个 retrieval target 直接检索预填充 value cache，避免外部检索后重新编码视觉输入。
- 2026-07 · [WIDE](../2607.28418-wide/README.md)：EIT-NLP 与 LMU Munich 用 token 级 Top-K router 动态激活 attention head 和 FFN channel group，在固定稀疏度下缩减推理计算。
- 2026-07 · [Penelope](../2607.25915-penelope/README.md)：在局部 decoder 边界执行共享权重潜在递归，提高结构化推理计算效率。
- 2026-07 · [DataOrchestra](../2607.24717-data-orchestra/README.md)：复旦、上海交大与 SII-GAIR 训练逐样本 orchestrator，按需选择 Drop、Untouch 或多阶段 Clean 预训练数据处理计划。
- 2026-07 · [Gzip-guided Sparse Attention](../2607.21752-gzip-sparse-attention/README.md)：以逐 block gzip 压缩率选择信息密集区，组合 local、literal long-range 和 hybrid heads 构造零参数自适应 mask。
- 2026-07 · [GaugeQuant](../2607.20757-gaugequant/README.md)：Cambridge 在线学习量化友好正交基，以 LogSumExp 抑制 W4A4 outlier。
- 2026-07 · [Convolution for LLMs](../2607.18413-conv-llm/README.md)：在 Q/K/V 投影后加入带残差的逐通道短卷积，以极少参数补充注意力的局部归纳偏置。
- 2026-07 · [PPL-Factory](../2607.18199-ppl-factory/README.md)：用冻结语言模型计算任务相关 NLL，并按数据预算在 easy、middle 和 mid-random 选择规则间切换。
- 2026-07 · [SIS](../2607.04728-sis/README.md)：依据样本重要性动态调整训练权重，使有限预算更集中于高价值序列与 token。
- 2026-05 · [MDCNS](../2605.19651-mdcns/README.md)：从多种负样本分布协同采样，并通过双模型更新降低单一采样偏差。
- 2025-02 · [Muon](../2502.16982-muon/README.md)：Moonshot AI 与 UCLA 对隐藏矩阵梯度做 Newton–Schulz 正交化，并为大规模 LLM 加入 weight decay 和 shape-aware scaling。
- 2023-12 · [Mamba](../2312.00752-mamba/README.md)：使用输入相关的步长、写入和读取向量实现选择性状态空间递推与线性序列复杂度。
- 2018-08 · [SASRec](../1808.09781-sasrec/README.md)：用因果自注意力编码用户行为序列，并预测下一物品，作为经典序列推荐基线。
