# 按公司

每篇论文独占一行；简介只概括主要方法，实验效果与复现边界请进入单篇文档查看。

## Yandex
- 2026-08 · [Sona](../2608.11015-sona/README.md)：压缩长历史并自回归生成层级 Semantic ID，再以 item ranker 统一替换音乐推荐级联。
- 2026-08 · [Gryphon-v2](../2608.06213-gryphon-v2/README.md)：以共享历史编码器统一 SID 生成和 item-level 排序，用 rollout 与 logged impression 双来源蒸馏训练期 teacher。

## AI VK
- 2026-08 · [VK Friend-GNN](../2608.27413-friend-gnn/README.md)：以多哈希共享表压缩超大用户 embedding，并用时序邻接与 cutoff 避免邻居采样泄漏未来边。

## Netflix
- 2026-08 · [Multimedia Asset Personalization via Multimodal Embeddings at Netflix](../2608.18322-netflix-mediafm/README.md)：把冻结多模态 embedding 接入统一资产双塔，并用查询相似度增强搜索画布打分。
- 2026-08 · [Netflix GenRec](../2608.10257-genrec-netflix/README.md)：用文本化上下文和 causal LLM 产生用户表示，catalog-aware head 一次打分全目录，并以联合语言/排序与长期 reward 目标后训练。
- 2026-06 · [GenPage: Towards End-to-End Generative Homepage Construction at Netflix](../2606.31031-genpage/README.md)：用一个模型直接生成整页，并以长期用户奖励和业务约束进行后训练。

## JD.com
- 2026-08 · [DEGR](../2608.04809-degr/README.md)：联合 next-item CE、cohort 多样性与 reward-adaptive ORPO，并在推理时执行多样性感知重排。

## Alibaba
- 2026-08 · [DCEO](../2608.25635-dceo/README.md)：以直接因果效应分离短期点击与长期用户价值，并用多目标策略权重优化电商搜索排序。
- 2026-08 · [TransRetrieval](../2608.25528-transretrieval/README.md)：把 target token 压缩、多域归一化与大规模 Transformer 检索结合，在受控 serving 预算下扩展召回模型。
- 2026-08 · [DREAM](../2608.09408-dream/README.md)：以 L0/L1/L2 意图、策略记忆和有界 typed compiler 控制现有推荐链路，再用离线探索与线上结论回流持续更新策略。
- 2026-08 · [MetaStrategy](../2608.09440-metastrategy/README.md)：根据请求生成带类型的多目标排序策略，并由确定性 compiler 校验、执行和审计。
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
- 2025-09 · [IntSR](../2509.21179-intsr/README.md)：把显式 query、隐式会话意图、时间信息和 POI 词表统一为搜索推荐生成框架。
- 2025-08 · [SaviorRec](../2508.01375-saviorrec/README.md)：用行为监督训练内容编码器，生成 RQ Semantic ID，并通过多行为适配模块改善冷启动。
- 2025-06 · [MGOE](../2506.10520-mgoe/README.md)：构建宏观任务合并图，让 graph experts 显式传播多任务关系后进入独立预测塔。
- 2025-05 · [SORT-Gen](../2505.07197-sort-gen/README.md)：用 causal Transformer ordered regression 估计列表前缀多目标价值，再以目标队列、mask 和 MMR 单次批量生成 slate。
- 2025-02 · [FilterLLM](../2502.16924-filterllm/README.md)：把新品文本一次性映射到用户词表分布，并用历史行为约束冷启动召回。
- 2025-02 · [SERAL](../2502.13539-seral/README.md)：构建用户认知画像，用 IPO 对齐惊喜度偏好，并通过 nearline 链路注入推荐排序。
- 2025-02 · [LUM](../2502.08309-lum/README.md)：通过 next-condition-item 预训练和 group query 压缩用户知识，再把生成表征注入判别式排序器。
- 2025-02 · [MIM](../2502.00321-mim/README.md)：以遮盖多模态预训练和内容兴趣感知 SFT 对齐内容/协同空间，再由 CiUBM 融合排序。
- 2023-11 · [BEQUE](../2311.03758-beque/README.md)：生成用户相关的搜索改写，并结合离线检索反馈、自采样与偏好排序优化改写质量。
- 2022-05 · [M6-Rec](../2205.08084-m6rec/README.md)：把推荐任务统一改写为自然语言任务，在预训练语言模型上使用轻量 option-adapter 完成多场景适配。
- 2020-06 · [SIM](../2006.05639-sim/README.md)：以候选 item 为 query，先从超长历史检索相关行为，再由精确搜索单元做候选相关注意力聚合。
- 2019-05 · [BST](../1905.06874-bst/README.md)：把候选商品作为 token 与用户行为共同送入 Transformer，显式建模序列内依赖。
- 2018-09 · [DIEN](../1809.03672-dien/README.md)：用 GRU 抽取逐步兴趣，以下一行为辅助监督并由候选相关门控控制兴趣演化。
- 2018-04 · [ESMM](../1804.07931-esmm/README.md)：在全曝光空间联合训练 CTR 与 CTCVR，并用 pCTR×pCVR 缓解点击后转化的选择偏差。
- 2017-06 · [DIN](../1706.06978-din/README.md)：用候选物品感知的局部激活单元，从用户历史中动态提取相关兴趣，并以 Dice 激活训练 CTR 排序模型。

## Ant Group
- 2024-03 · [BAHE](../2403.19347-bahe/README.md)：缓存每个原子行为的浅层语言表示，只在线聚合高层序列，从而降低长文本 CTR 建模成本。

## Baidu
- 2025-03 · [COBRA](../2503.02453-cobra/README.md)：先用稀疏生成缩小候选空间，再用稠密生成细排，形成级联式生成召回。

## ByteDance / Douyin / TikTok
- 2026-08 · [DME](../2608.02148-dme/README.md)：先做多模态对比预训练，再以 typed latent evidence 和 cross-conditional reconstruction 保留细粒度对侧语义。
- 2026-08 · [STEPS](../2608.01949-steps/README.md)：用 ordinal planning、trajectory execution 与 filtering agent 闭合“是否推送—何时再唤醒”，并已在抖音全量部署。
- 2026-05 · [Rec-Distill](../2605.29755-rec-distill/README.md)：结合 batch 与 streaming teacher，把大模型知识蒸馏到轻量推荐 student，并优化跨任务可迁移性。
- 2026-05 · [FLUID](../2605.21832-fluid/README.md)：把直播多模态切片量化成 slice/room 两级 LUCID，以 prefix n-gram late fusion 完全替代短生命周期候选 ID。
- 2026-03 · [HAP](../2603.03770-hap/README.md)：按候选异质难度路由轻量/强预排分支，并以 harmonization 对齐不同计算预算。
- 2026-02 · [MixFormer](../2602.14110-mixformer/README.md)：在统一 Transformer 中平衡 dense 特征交互与序列建模，并按预算选择可训练模块。
- 2026-02 · [MDL](../2602.07520-mdl/README.md)：把 feature、scenario、task 全部 token 化，并以 domain-feature attention 深层共享。
- 2026-02 · [MSN](../2602.07526-msn/README.md)：用两轴 Product-Key Memory 扩大参数容量，每次只激活 top-k 槽位并与 dense 主干门控融合。
- 2026-02 · [TokenMixer-Large](../2602.06563-tokenmixer-large/README.md)：交替执行无参数 token mixing、head-wise/token-wise SwiGLU，并以间隔残差和辅助头稳定深层扩容。
- 2026-01 · [HyFormer](../2601.12681-hyformer/README.md)：联合编码用户序列与搜索 query，通过 query decoding 和 boosting 强化搜索推荐信号。
- 2025-10 · [OneTrans](../2510.26104-onetrans/README.md)：用统一因果 Transformer 覆盖多场景排序，并复用 KV cache 降低线上推理成本。
- 2025-07 · [RankMixer](../2507.15551-rankmixer/README.md)：交替进行 token mixing 与逐 token FFN，并探索稀疏 MoE 以扩展工业排序网络。
- 2025-05 · [LONGER](../2505.04421-longer/README.md)：结合混合注意力、InnerTrans、token merge 与 KV cache，扩展超长用户行为序列建模。
- 2025-01 · [AdaF²M²](../2501.15816-adaf2m2/README.md)：通过 feature-mask 多次前向学习完整表征，再按用户/物品状态动态调节 adapter。

## Dewu
- 2026-08 · [SPEAR](../2608.01738-spear/README.md)：用双 embedding、confidence×relevance 乘法门和动态 selector 联合优化个性化改写与检索。

## Google / YouTube
- 2026-07 · [HA-MoE](../2607.27577-ha-moe/README.md)：依据内容异构性动态路由领域、转移、内容与新鲜度专家，在单一模型中统一开放网页排序。
- 2026-07 · [ClockRoPE](../2607.26369-clockrope/README.md)：从日/周周期 kernel 的 Fourier 频谱采样旋转频率，为生成式召回显式建模用户 routine。
- 2026-07 · [Dual-purpose Semantic IDs](../2607.24865-dual-sid/README.md)：让分层 SID 同时承载协同身份并通过 Semantic Decoder 重建内容 embedding。
- 2026-07 · [YouTube Freshness](../2607.23749-youtube-freshness/README.md)：比较 recency、IPS、bias tower 与不确定性探索对新内容反馈环的影响。
- 2026-06 · [TokenMinds](../2606.25147-tokenminds/README.md)：让共享 encoder 同时产生稠密用户向量，并由 decoder 生成可落到内容语义空间的 SID 用户 token，再共同服务下游排序。
- 2026-05 · [Semantic-Native Long Sequence Modeling](../2606.07546-semantic-native-longseq/README.md)：以层级语义 ID、bigram、时间折叠和 global-local pooling 扩展视频长历史。
- 2026-04 · [AgenticRecTune](../2604.26969-agentic-rec-tune/README.md)：以 Actor、Critic、Insight、Skill 和 Online agent 闭合推荐配置的多轮实验反馈。
- 2026-03 · [Cross-domain KD](../2603.28994-cross-domain-kd/README.md)：把 YouTube 等源域 teacher 的知识蒸馏到目标域，实现面向音乐发现的零样本迁移。
- 2026-02 · [Self-Evolving RecSys](../2602.10226-self-evolving-rec/README.md)：让 LLM Agent 根据历史实验提出、评估和迭代推荐策略，形成自动改进闭环。
- 2025-10 · [PLUM](../2510.07784-plum/README.md)：对 LLM 进行推荐语料 CPT 与 SFT，并以 Semantic ID 生成物品序列。
- 2023-05 · [TIGER](../2305.05065-tiger/README.md)：用 RQ-VAE 把物品量化为层级 Semantic ID，再通过自回归模型直接生成召回结果。
- 2020-08 · [DCN-V2](../2008.13535-dcn-v2/README.md)：用低秩 cross experts 与输入相关 gate 高效学习有界阶数特征交互。
- 2018-08 · [MMoE](../kdd2018-mmoe-mmoe/README.md)：为 CTR、转化等任务学习独立 gates，以不同权重组合同一组共享 experts。
- 2016-09 · [YouTube DNN](../recsys2016-youtube-dnn-youtube-dnn/README.md)：用观看历史聚合与深层用户塔学习候选召回向量，再做大规模 item 近邻检索。
- 2016-06 · [Wide & Deep](../1606.07792-wide-deep/README.md)：联合显式 wide 特征交叉与 deep tower，兼顾共现记忆和未见组合泛化。

## Huawei
- 2026-07 · [RAMP](../2607.17473-ramp/README.md)：用个性化/公共双路径、可用性 mask 和 prediction-alignment 蒸馏提升缺失用户字段时的广告排序鲁棒性。
- 2025-02 · [FuXi-α](../2502.03036-fuxi-alpha/README.md)：用时间、语义等自适应多通道注意力和 multi-stage FFN 扩展推荐特征交互模型。
- 2023-06 · [KAR](../2306.10933-kar/README.md)：让 LLM 生成用户偏好与物品事实知识，再由 hybrid-expert adapter 融合进传统推荐模型。
- 2017-03 · [DeepFM](../1703.04247-deepfm/README.md)：用共享 embedding 联合 FM 二阶交互和 deep 高阶交互，减少手工特征交叉。

## Kuaishou
- 2026-08 · [HRPO](../2608.00750-hrpo/README.md)：按层级 Semantic ID 前缀构造 residual credit-to-go，让生成式推荐的策略更新同时优化局部 token 与整条推荐轨迹。
- 2026-07 · [RecoReward](../2607.25901-reco-reward/README.md)：以目标/非目标推荐亲和力差作为多模态描述的训练奖励。
- 2026-07 · [TWICE](../2607.25404-twice/README.md)：用双时钟和双窗口校正在线广告长期延迟转化。
- 2026-07 · [UniR²](../2607.24439-unir2/README.md)：用统一 decoder 和 Dual-Query Prefix-Causal Attention 同时学习层级 SID 生成与多目标排序，并以 ranking-only LoRA 避免梯度冲突。
- 2026-07 · [UAME](../2607.17092-uame/README.md)：把满意度分数建模为均值—方差 Gaussian 变量，用多目标冲突产生的不确定性加权 pairwise 排序训练。
- 2026-07 · [RECAP](../2607.15730-recap/README.md)：把流式用户画像维护为固定容量语义状态，并用推荐反馈评价器和 GRPO 闭环优化画像更新策略。
- 2026-04 · [GloRank](../2604.25291-glorank/README.md)：在全局 Semantic ID action space 上做 listwise SFT 与组相对奖励优化，避免局部候选池限制。
- 2026-04 · [CS3](../2604.19269-cs3/README.md)：通过循环自修正、跨塔同步和级联教师信号增强仍可 ANN 服务的双塔模型。
- 2026-04 · [Dual-Rerank](../2604.07420-dual-rerank/README.md)：以 AR 顺序教师蒸馏 NAR 并行名次学生，并把列表效用与延迟共同纳入目标。
- 2026-02 · [GR4AD](../2602.22732-gr4ad/README.md)：构造用户感知 Semantic ID，结合 LazyAR、可变长度生成和 RSPO 完成生成式广告召回。
- 2026-01 · [OneMall](../2601.21770-onemall/README.md)：以统一 Semantic ID、场景 prompt 和跨行为融合覆盖商品卡、短视频与直播生成推荐。
- 2025-11 · [DualGR](../2511.12518-dualgr/README.md)：融合长短期兴趣路由、受约束 SID 前缀和曝光感知损失完成生成召回。
- 2025-08 · [MPFormer](../2508.20400-mpformer/README.md)：以任务 token 驱动共享序列检索器，并按难度动态分配容量与 serving 配额。
- 2025-08 · [OneRec-V2](../2508.20900-onerec-v2/README.md)：使用 lazy decoder 降低生成延迟，并用真实反馈强化学习和 GBPO 优化推荐序列。
- 2025-02 · [OneRec](../2502.18965-onerec/README.md)：把 session 推荐建模为 Semantic ID 序列生成，并结合 MoE 与偏好优化对齐真实反馈。
- 2024-07 · [TWIN-V2](../2407.16357-twin-v2/README.md)：离线层次压缩生命周期行为，在线通过候选相关 GSU 检索兴趣簇，再以 ESU 精确建模原始行为。
- 2024-06 · [CDM](../2406.09021-cdm/README.md)：将可控 MMR 教师的上下文多样性边际收益蒸馏到低延迟学生。
- 2024-06 · [CWM](../2406.07932-cwm/README.md)：以统一视频时长干预下的反事实观看收益抵消 duration bias。
- 2024-05 · [LEARN](../2405.03988-learn/README.md)：冻结 LLM 生成内容增强表征，再通过协同域适配改善冷启动和长尾推荐。
- 2024-03 · [LSVCR](../2403.13574-lsvcr/README.md)：用 LoRA 学习 LLM 偏好，通过 SSC/VCC 双序列目标对齐评论语义和用户行为。

## Meituan
- 2026-07 · [CORE](../2607.24417-core-relevance/README.md)：把三级电商相关性拆成两道条件边界，以 step-GRPO 提供细粒度 credit，再将 PostCoT LLM 蒸馏到在线双头模型。
- 2026-07 · [NONTP](../2607.12277-nontp/README.md)：在 NTP 上加入未来状态对比学习和跨域 hidden-state pooling，扩大生成式推荐的训练监督覆盖。
- 2026-04 · [MBGR](../2604.02684-mbgr/README.md)：通过 business-aware SID、共享 MoE 和最近未来标签路由，同时学习多个业务域的生成目标。
- 2026-02 · [DOS](../2602.04460-dos/README.md)：用协同/语义双流和正交 residual quantization 对齐 SID codebook 与生成空间。
- 2025-10 · [CRSD](../2510.11056-crsd/README.md)：用领域 reasoning teacher 构造增强视图，再让同一轻量学生执行普通/推理双视图对比自蒸馏，线上无需生成推理链。
- 2025-02 · [SessionRec](../2502.10157-sessionrec/README.md)：按真实 session 生成候选，并利用曝光负例和 hard negative 改善会话级召回。
- 2024-12 · [MSD](../2412.06860-msd/README.md)：把 teacher 的用户知识自回归蒸馏到小模型，再通过 LoRA 和缓存表征对齐 CTR 任务。

## Meta
- 2026-07 · [ROCS](../2607.27744-rocs/README.md)：复用单次 request encoding，并在候选端执行轻量 late interaction，统一覆盖广告/自然流量的检索和排序 serving。
- 2026-07 · [OneShot](../2607.27475-oneshot-index/README.md)：将层级索引纳入 ranking objective 共同训练，并以 neural interaction scoring 突破纯点积检索。
- 2026-07 · [Memory Layer](../2607.25110-memory-layer/README.md)：把 cache 纳入模型训练，以 eta=1 writeback 和 always-on 属性表征消除训练服务偏差与冷启动缺口。
- 2026-07 · [Mosaic](../2607.24015-mosaic/README.md)：将多类用户 embedding 组织为 specialist fleet，并通过 MRM 联合标签与 cosine redundancy loss 保持新增表征的独特信息。
- 2026-07 · [WHALE](../2607.17017-whale/README.md)：逐层耦合 Wukong 高阶特征交互和门控 HSTU 序列建模，形成共同扩展的统一排序模型。
- 2026-07 · [SlimPer](../2607.12281-slimper/README.md)：用固定容量 user-item knowledge base 逐层查询完整历史，并通过 Select–Match–Refine 把计算集中到候选相关证据。
- 2026-07 · [Cluster GOOBS](../2607.00448-cluster-goobs/README.md)：在线聚类用户或物品表征，并以 cluster-aware sampler 改善训练样本覆盖和头部集中。
- 2026-06 · [NEXT](../2607.24789-next-vlm/README.md)：用 VLM 生成并验证 item→intent→item directed edges，离线构图后在正反馈时在线注入。
- 2026-06 · [CMSL](../2606.28533-cmsl/README.md)：用可学习兴趣 lenses 拆分多兴趣序列，并结合 HSTU 建模不同语义 strand。
- 2026-06 · [G2Rec](../2606.20554-g2rec/README.md)：构建可微 soft graph，并联合图结构与生成式双目标学习用户—物品关系。
- 2026-06 · [RankGraph-2](../2606.18379-rankgraph2/README.md)：用流行度校正边、离线多跳 PPR 和 residual cluster index 降低工业图召回的在线成本。
- 2026-05 · [SCALR](../2606.00282-scalr/README.md)：学习跨域条件分布并概率采样合成训练事件，替代覆盖度较低的确定性 top-k 翻译。
- 2026-05 · [Memento](../2605.24051-memento/README.md)：采用 query-conditioned MMR 在相关性与多样性之间动态权衡，进行候选重排。
- 2026-05 · [LLM Retrieval](../2605.21969-llm-ad-retrieval/README.md)：通过 domain SFT 生成层级广告属性，构建语义图并约束召回结果对属性扰动的稳定性。
- 2026-05 · [MM-LLM](../2605.09338-mm-llm/README.md)：把多模态内容转成 caption/token 特征，再注入推荐模型增强内容理解。
- 2026-04 · [HILL](../2604.12965-hill-index/README.md)：用跨层 residual quantization 学习 coarse-to-fine 检索索引，减少候选打分量。
- 2026-04 · [SOLARIS](../2604.12110-solaris/README.md)：预测未来 user-item 请求，异步预计算 foundation-model latent，并通过 cache/fallback 服务线上排序。
- 2026-02 · [ULTRA-HSTU](../2602.16986-ultra-hstu/README.md)：组合半局部注意力、逐层扩窗 LBSL 与 Mixture of Transducers 扩展超长历史。
- 2026-02 · [MFLI](../2602.16124-mfli/README.md)：联合学习语义、流行度与新鲜度等多个 facet 索引，替代静态单空间 ANN。
- 2026-02 · [Kunlun](../2602.10016-kunlun/README.md)：用 GDPA、分层 seed pooling、全局交互与 CompSkip 统一深层广告排序架构。
- 2026-01 · [LLaTTE](../2601.20083-llatte/README.md)：把 LLM 语义特征与推荐表征结合，并面向大规模排序设计特征交互结构。
- 2025-06 · [RADAR](../2506.07261-radar/README.md)：在请求后异步运行完整排序器，把高价值结果缓存为下一请求的召回补充。
- 2024-02 · [HSTU](../2402.17152-hstu/README.md)：以分层顺序转导单元建模超长行为历史，用生成式目标统一大规模推荐排序。

## Pinterest
- 2026-07 · [PinEqualizer](../2607.22518-pinequalizer/README.md)：贯通探索 corpus、召回、排序与 utility，通过 engagement dropout、内容交叉、分 cohort calibration 和 UCB 缓解 fresh 内容反馈回路。
- 2026-07 · [Pin-SCALE](../sigir2026-pin-scale-pin-scale/README.md)：用 engagement-aware SID、级联 pooling 和多视角对比对齐接入 dense retrieval。
- 2026-07 · [Downstream Rewards](../2607.14192-downstream-rewards/README.md)：离线筛选能预测未来参与度的长期 reward，再以模型无关附加头接入多个推荐 surface。
- 2026-07 · [Causal Retrieval](../2607.14161-causal-retrieval/README.md)：用 doubly-robust uplift 决定是否触发 shopping candidate generator。
- 2026-07 · [MESH](../2607.12392-mesh/README.md)：把 user/item/context 特征放入独立放大塔，再用 residual gated bias correction 保护 fresh 内容信号。
- 2026-05 · [Complementary LLM Ads Predictor](../2605.27856-pinterest-ads-llm/README.md)：对广告主列表进行 SFT/GRPO，让 LLM 作为传统广告召回与排序的补充预测器。
- 2026-05 · [A Production-Ready RL Framework for Personalized Utility Tuning with Pareto Sweeping in Pinterest Recommender Systems](../2605.16344-prl-puts/README.md)：以双头 Q 网络和 Pareto 扫描选择可治理的个性化多目标 utility 策略。
- 2026-03 · [PinCLIP](../2603.03544-pinclip/README.md)：以 VLM 图文对齐加 Pin-Board 邻居目标改善 fresh 内容表征。
- 2026-02 · [ML-DCN: Masked Low-Rank Deep Crossing Network Towards Scalable Ads Click-through Rate Prediction at Pinterest](../2602.09194-ml-dcn/README.md)：用可学习 mask 与低秩交叉扩大 DCN 容量并保持线上成本中性。
- 2025-09 · [DRL-PUT](../2509.05292-drl-put/README.md)：从 logged ads behavior 学习相关性、新颖性和收益等排序 utility 的动态权重策略。
- 2025-07 · [Click A, Buy B](../2507.15113-click-a-buy-b/README.md)：拆分同物品 CABA 与跨物品 CABB 转化归因，并用商品 taxonomy 建立协同权重。
- 2025-07 · [PinFM](../2507.12704-pinfm/README.md)：以 DCAT 等序列模块构建推荐 foundation model，并通过预训练—微调适配多个流量场景。
- 2025-06 · [TransAct V2](../2506.02267-transact-v2/README.md)：用候选感知的终身行为序列和 next-action 多任务目标增强 Homefeed 排序。
- 2025-04 · [PinRec](../2504.10507-pinrec/README.md)：根据目标 outcome 生成多 token 物品表示，以条件生成方式完成召回。

## Tencent / WeChat
- 2026-07 · [CCFormer](../2607.28070-ccformer/README.md)：分离 ID 与内容字段后门控融合，并以分层压缩保留近期细节和远期兴趣，服务腾讯视频推荐。
- 2026-07 · [ASARL](../2607.26593-asarl/README.md)：用 Reason/Critic/Gen 多 Agent 闭环整理社交搜索数据，再经 SCT、偏好优化和蒸馏得到在线相关性模型。
- 2026-07 · [BARGE](../2607.21028-barge/README.md)：用 item-level ICA 恢复多 token Semantic ID 边界，通过逐层 HPR 与正交双路径 DPD 抑制生成漂移。
- 2026-06 · [NOVA](../2606.27243-nova/README.md)：以 architecture gradient 驱动候选修改，并用四级验证级联阻断可运行但语义错误的架构。
- 2026-05 · [UniVA](../2605.05803-univa/README.md)：用 Commercial SID 和 generation-as-ranking 统一广告生成，并通过价值对齐 RL 与 trie beam 优化收益。
- 2026-03 · [OneRanker](../2603.02999-oneranker/README.md)：用 fake item token 统一生成、价值预测和工业广告排序，并约束两种分布一致。
- 2026-02 · [S-GRec](../2602.10606-s-grec/README.md)：以 LLM 个性化语义 judge 产生偏好监督，再用 A2PO 蒸馏到轻量 SID 生成器。
- 2025-12 · [HiGR](../2512.24787-higr/README.md)：先生成层级 Semantic ID 簇再解码物品 slate，并以 ORPO 做列表偏好对齐。
- 2024-12 · [PRECISE](../2412.06308-precise/README.md)：联合 LLM 语义 token 与协同 ID，使用 top-k MoE 和通用/目标训练建模序列推荐。
- 2024-11 · [LEADRE](../2411.13789-leadre/README.md)：生成意图感知 Semantic ID，并通过 DPO 对齐广告展示与转化偏好。
- 2020-09 · [PLE](../recsys2020-ple-ple/README.md)：把共享 experts 与任务专属 experts 分组，通过 CGC gates 逐层分离共性和任务特性。

## Xiaohongshu
- 2026-08 · [OneModel](../2608.18606-onemodel/README.md)：以共享长序列 backbone、场景条件门控和全局/局部分层表征统一推荐、广告与商家排序。
- 2026-03 · [IDProxy](../2603.01590-idproxy/README.md)：先把多模态 LLM 表征对齐到协同 ID 空间，再通过多层 proxy adapter 和残差门控注入排序器。
- 2025-05 · [GenRank](../2505.04180-genrank/README.md)：把多种用户动作编码为生成目标，通过 action-oriented generation 完成端到端排序。
- 2024-03 · [NoteLLM](../2403.01744-notellm/README.md)：把内容压缩到特殊 token，以 GCL 注入协同信号，并用 CSFT 保持生成能力。

## Yandex
- 2026-07 · [Long-History User Transformers](../2607.14331-long-history-transformer/README.md)：用异步全历史 Transformer 生成固定缓存，线上只编码近期事件，在不重算长序列的情况下增强广告排序。
- 2025-07 · [ARGUS](../2507.15994-argus/README.md)：分解用户反馈与物品表示，在大规模 Transformer 中联合建模音乐序列。

## Microsoft / Bing Ads
- 2026-05 · [HARNESS-LM](../2605.23572-harness-lm/README.md)：先训练强检索 teacher，再以 L2 对齐和冻结文档塔对比精修压缩在线 query encoder。

## Airbnb
- 2026-07 · [Proximity Features](../2607.12246-proximity-features/README.md)：用自适应地理桶聚合群体行为，为无持久 user ID 的匿名用户提供隐私合规冷启动特征。
- 2026-06 · [JourneyFormer: Encoding Airbnb Guest Journey with Sequence Modeling](../2606.19108-journeyformer/README.md)：统一编码长短 guest journey 与事件时间，在生产搜索中替代手工序列特征。

## Teads
- 2026-07 · [Open Web UFM](../2607.28019-open-web-ufm/README.md)：以开放网页用户行为做双裁剪对比预训练和 next-item 监督，再把共享 user encoder 迁移到广告 CTR 与访问预测。

## Spotify
- 2026-03 · [GLIDE](../2603.17540-glide/README.md)：用 residual Semantic ID 自回归检索，并联合近期历史与长期用户 soft prompt 扩大探索。
- 2026-01 · [Podcast MTL](../2601.02306-podcast-mtl/README.md)：共享广告、推广与 organic stream 表征，将高资源任务知识迁移给冷启动 podcast。

## NetEase
- 2026-07 · [Melo](../2607.23718-melo/README.md)：用多节点音乐 Agent、实体目录 grounding 和反思重试生成可靠 playlist。

## Shopee
- 2026-08 · [KGD](../2608.02738-kgd/README.md)：以 BMTP、冻结知识迁移和正交 ACR 解耦预训练知识与推荐几何，使流式模型可以低成本刷新外部知识。
- 2025-09 · [OnePiece](../2509.18091-onepiece/README.md)：用上下文 token、块级 latent reasoning 和递进多任务训练统一级联排序。

## Twitch
- 2026-08 · [Twitch Multi-Objective Ranking](../2608.04455-twitch-mor/README.md)：联合即时与延迟直播反馈，并以生命周期分群 gate 调节共享专家，避免单一短期目标主导排序。

## NAVER WEBTOON
- 2026-08 · [LLM Thompson Priors](../2608.03382-llm-ts-prior/README.md)：用 LLM 语义判断初始化评论冷启动先验，再通过分群 Thompson Sampling 在探索与点击收益之间自适应取舍。

## JD.com
- 2026-07 · [OxygenREC-v2](../2607.24255-oxygenrec-v2/README.md)：把 click/cart/order instruction 内化到 SID 生成，并用未来交互特权教师与熵路由蒸馏联合后训练。
- 2026-04 · [GenRec](../2604.14878-genrec/README.md)：把下一页作为联合生成目标，通过非对称 Token Merger 和带 NLL 约束的 GRPO-SR 优化整页。

## 学术与经典基线
- 2026-05 · [MDCNS](../2605.19651-mdcns/README.md)：从多种负样本分布协同采样，并通过双模型更新降低单一采样偏差。
- 2018-08 · [SASRec](../1808.09781-sasrec/README.md)：用因果自注意力编码用户行为序列，并预测下一物品，作为经典序列推荐基线。

## Michigan State University
- 2026-08 · [ConnectionMind](../2608.10187-connectionmind/README.md)：在时序异构社交图上用最短正路径 SFT 和规则奖励 GRPO 学习多步探索，再把路径教师蒸馏给 GNN student。

## Kuaishou Technology
- 2026-08 · [TAGR](../2608.24034-tagr/README.md)：用稳定两级语义/协同 ID、多尺度用户兴趣和行为价值门控，在直播广告中生成兼顾相关性与商业价值的候选。
- 2026-08 · [From a Static Multi-Level Small Semantic Codebook to a Dynamic Single-Level Large Semantic Codebook for Generative Recommendation](../2608.21012-dynamic-codebook/README.md)：用曝光加权动态大码本替代多级小码本，并保留独立碰撞码以缩短 SID 解码。
- 2026-08 · [Once Generated, Ranked: End-to-End Generative Slate Recommendation with Unified Semantic-Collaborative IDs](../2608.17613-ogr/README.md)：以统一语义-协同 ID 生成整张 slate，再用列表反馈做保守策略对齐。
- 2026-08 · [PushDualGen: Enabling LLMs to Generate Semantic IDs with Interpretable Copy for Industrial Push Recommendation](../2608.07989-pushdualgen/README.md)：先生成可服务 SID，再按需生成可解释 copy，并在在线侧融合两种表示。
- 2026-05 · [DADF: A Distribution-Aware Debiasing Framework for Watch-Time Regression in Recommender Systems](../2605.17863-dadf/README.md)：冻结成熟 watch-time 模型，学习分布感知乘性残差且保持服务接口不变。
- 2026-03 · [SaFRO: Satisfaction-Aware Fusion via Dual-Relative Policy Optimization for Short-Video Search](../2603.19585-safro/README.md)：用满意度奖励和双重相对优势优化短视频搜索多任务融合。

## Amap / Alibaba
- 2026-08 · [IntHQ: Task-Interactive Hierarchical Query on Dual-Stream Representations for Generative Recommendation](../2608.09634-inthq/README.md)：让多个业务任务在长短双流的不同层级执行交互查询，而非仅共享底层编码。
- 2026-07 · [Guess Where You Go: Generative Next Point-of-Interest Recommendation in Amap](../2607.26073-guess-where-you-go/README.md)：把时空历史编码为 SID，并以课程训练和长期反馈优化下一 POI 生成。

## Huazhong Agricultural University (Kuaishou internship)
- 2026-07 · [RecHarness: A Bandit-Routed Agentic Harness for Self-Evolving Recommender Systems](../2607.29241-recharness/README.md)：用 bandit 在有限预算下路由候选结构实验，并把验证反馈写回下一轮。
- 2026-07 · [From Understanding to Action: Feedback-Grounded Policy Discovery for Generative Recommendation](../2607.27789-feedback-policy/README.md)：从真实反馈发现生成策略，再用双空间关系蒸馏到轻量线上排序器。

## Rajax Network Technology / Taobao Shangou / Alibaba
- 2026-07 · [GALA: Generative Aligned Learning for Adaptive Multimodal Representation in the Taobao Shangou Recommender System](../2607.29213-gala/README.md)：通过三元组预训练、GRPO 行为对齐和 ID/多模态门控形成可部署表示。

## QuintoAndar
- 2026-07 · [LLM-Based Re-Ranking for Real Estate Search](../2607.14835-real-estate-rerank/README.md)：结合对话需求、房源属性、文本描述与候选集合统计执行 LLM 重排。

## University of Washington
- 2026-07 · [Adaptive Ad Load Design for Sponsored Search Markets: Evidence, Theory, and Deployment](../2607.14418-adaptive-ad-load/README.md)：从随机现场实验学习收入—转化曲线，再按请求动态选择广告数量。

## NetEase Cloud Music
- 2026-05 · [L2Rec: Towards Dual-View Understanding of LLMs for Personalized Recommendation](../2605.26717-l2rec/README.md)：用个性化双视图 LoRA-MoE 分别适配语义和行为，再自适应融合。

## University of Science and Technology of China / Alibaba
- 2026-05 · [From Item-Only to Query-Item: Query-Conditioned Generative Search with QGS in Quark](../2605.25514-qgs/README.md)：把 query-item 联合序列交给 Linear HSTU，并融合稀疏交叉特征做生成式搜索。

## Tubi
- 2026-05 · [TubiFM: Unified Item, Carousel, and Search Ranking for Streaming Discovery](../2605.23702-tubifm/README.md)：以统一 user story 和任务提示让同一模型完成 item、carousel 与 search 排序。

## TikTok
- 2026-05 · [PEARL: Unbiased Percentile Estimation via Contrastive Learning for Industrial-Scale Livestream Recommendation](../2605.21752-pearl-percentile/README.md)：通过多样本对比估计低方差行为 percentile，并扩展到多个直播目标。

## Huawei Technologies
- 2026-05 · [Effective Knowledge Transfer for Multi-Task Recommendation Models](../2605.05730-ektm/README.md)：按任务相似度把 CTR 知识迁移到多个 CVR 塔，并抑制难例负迁移。

## University of Electronic Science and Technology of China / Kuaishou
- 2026-04 · [Beyond Static Collision Handling: Adaptive Semantic ID Learning for Multimodal Recommendation at Industrial Scale](../2604.23522-adasid/README.md)：依据碰撞负载、语义相容性和训练阶段动态调节 SID 重叠约束。
- 2026-02 · [Stop Treating Collisions Equally: Qualification-Aware Semantic ID Learning for Recommendation at Industrial Scale](../2603.00632-quasid/README.md)：按业务资格信号设定碰撞 margin，提升冷启动 SID 可辨识度。

## Authors did not disclose affiliation / large-scale e-commerce platform
- 2026-04 · [UniRec: Bridging the Expressive Gap between Generative and Discriminative Recommendation via Chain-of-Attribute](../2604.12234-unirec-coa/README.md)：先生成属性链再生成容量受限 SID，并以 RFT/DPO 对齐业务目标。

## Taobao & Tmall Group / Alibaba
- 2026-03 · [UniScale: Synergistic Entire Space Data and Model Scaling for Search Ranking](../2603.24226-uniscale/README.md)：以 Entire-Space 数据和分层异构融合协同扩展搜索排序模型。
- 2026-03 · [AIGQ: An End-to-End Hybrid Generative Architecture for E-commerce Query Recommendation](../2603.19710-aigq/README.md)：组合 Direct/Reasoning query 生成、IL-GRPO 与混合在线服务。

## Alibaba International Digital Commerce
- 2026-03 · [GateSID: Adaptive Gating for Semantic-Collaborative Alignment in Cold-Start Recommendation](../2603.22916-gatesid/README.md)：用冷启动感知门控动态融合语义 SID 与协同行为信号。
- 2026-03 · [SORT: A Systematically Optimized Ranking Transformer for Industrial-scale Recommenders](../2603.03988-sort-ranking/README.md)：系统优化 token 化、注意力和 FFN，统一替代工业 DLRM 排序。

## Alibaba Group / Renmin University
- 2026-02 · [Generative Pseudo-Labeling for Pre-Ranking with LLMs](../2602.20995-gpl-prerank/README.md)：LLM 为未曝光候选生成伪标签，线上预排序器不增加 LLM 时延。

## Alibaba Group / Tsinghua University
- 2026-02 · [A Long-term Value Prediction Framework In Video Ranking](../2602.17058-ltv-video-ranking/README.md)：组合位置去偏、会话归因与作者周期任务建模长期价值。

## Forth AI / Shopee / Singapore University of Technology and Design
- 2026-02 · [RGAlign-Rec: Ranking-Guided Alignment for Latent Query Reasoning in Recommendation Systems](../2602.12968-rgalign-rec/README.md)：用真实排序模型偏好指导潜在 query 的 SFT 与 DPO 对齐。

## LinkedIn
- 2026-02 · [An Industrial-Scale Sequential Recommender for LinkedIn Feed Ranking](../2602.12354-linkedin-feed-sr/README.md)：用工业长序列推荐器重写 LinkedIn Feed 排序与服务链路。
- 2026-02 · [CADET: Context-Conditioned Ads CTR Prediction With a Decoder-Only Transformer](../2602.11410-cadet/README.md)：以候选后上下文条件化的 Decoder-only Transformer 统一广告 CTR。

## Tencent
- 2026-02 · [DiffuReason: Bridging Latent Reasoning and Generative Refinement for Sequential Recommendation](../2602.09744-diffureason/README.md)：将 Thinking Tokens、扩散去噪和 GRPO 组成端到端序列推荐。

## Institute of Information Engineering, CAS / Kuaishou
- 2026-02 · [SARM: LLM-Augmented Semantic Anchor for End-to-End Live-Streaming Ranking](../2602.09401-sarm/README.md)：离线 MLLM 生成语义 anchor，轻量非对称模块注入直播排序。

## Apple
- 2026-02 · [Unifying Ranking and Generation in Query Auto-Completion via Retrieval-Augmented Generation and Multi-Objective Alignment](../2602.01023-rag-qac/README.md)：以 RAG、SFT 和 DPO 同时优化补全相关性、安全与 groundedness。
