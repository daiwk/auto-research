# 按主题

采用“研究方向 → 方法簇 → 论文”的两级结构。同一篇论文可以出现在多个方法簇下；
每次出现都独占一行，并说明它与该方法簇相关的主要机制。

## 大模型能力与推荐融合

### LLM / Foundation model + Recommendation
- [Netflix GenRec](../2608.10257-genrec-netflix/README.md)：把用户历史、内容和请求上下文文本化，以 LoRA 后训练 causal LLM，再由 catalog-aware head 输出全目录分数。
- [Open Web UFM](../2607.28019-open-web-ufm/README.md)：在开放网页行为上联合双裁剪对比学习与 next-item 目标预训练共享 user encoder，再迁移到广告 CTR 和访问率任务。
- [RecoReward](../2607.25901-reco-reward/README.md)：用行为推荐器产生 RAS reward 来优化多模态内容描述，但 serving 不读取用户行为。
- [Melo](../2607.23718-melo/README.md)：将 LLM 音乐 Agent 与实体 grounding、检索校验和反思重试组合为生产 playlist 流程。
- [RECAP](../2607.15730-recap/README.md)：用 causal Transformer 更新固定容量语义画像，再通过双塔反馈评价器与 GRPO 让画像直接服务未来推荐。
- [RecGPT-V3](../2607.15591-recgpt-v3/README.md)：让 LLM 读取可演化用户记忆并联合生成文本/SID，再以 latent token 重建蒸馏与排序反馈降低显式推理成本。
- [Prompt Generation](../2607.11326-prompt-generation/README.md)：把异构推荐特征转成 Qwen 生成提示，并通过 token 压缩与配置化合并完成召回。
- [TokenMinds](../2606.25147-tokenminds/README.md)：把观看、搜索与场景信号编码为稠密用户向量和 SID 用户 token，以双输出和 multi-context decoding 支持下游排序与跨场景复用。
- [Pinterest Complementary LLM Predictor](../2605.27856-pinterest-ads-llm/README.md)：对广告主列表进行 SFT/GRPO，让 LLM 补充传统召回和排序特征。
- [AKT-Rec](../2605.23310-akt-rec/README.md)：用真实 LLM 对齐物品共现和用户兴趣，再以 Semantic ID 支持面向长尾的非对称知识迁移。
- [HARNESS-LM](../2605.23572-harness-lm/README.md)：通过强 teacher、L2 embedding alignment 与冻结文档索引精修构造非对称轻量检索器。
- [LLM Retrieval](../2605.21969-llm-ad-retrieval/README.md)：用 domain SFT 生成层级广告属性，构建语义图并约束召回稳定性。
- [FLUID](../2605.21832-fluid/README.md)：用多模态大模型编码直播切片，经 RQ-KMeans 与 prefix n-gram 形成 LUCID，最终移除候选 item ID。
- [MM-LLM](../2605.09338-mm-llm/README.md)：把多模态内容转为 LLM caption/token 特征，再注入推荐排序模型。
- [UniVA](../2605.05803-univa/README.md)：以 Commercial SID 和 generation-as-ranking 统一广告生成，再用价值对齐 RL 优化收益。
- [RecGPT-Mobile](../2605.04726-recgpt-mobile/README.md)：用端侧 LoRA+INT8 LLM 将近期行为生成为下一意图 query，并依据意图漂移按需触发推理。
- [LWGR](../2605.18771-lwgr/README.md)：把个性化 soft instruction 注入 LLM 世界知识，并用拉格朗日约束完成分数融合。
- [SOLARIS](../2604.12110-solaris/README.md)：预测未来请求并异步缓存 foundation-model latent，把大模型计算移出线上请求路径。
- [Cross-domain KD](../2603.28994-cross-domain-kd/README.md)：把源域大模型知识蒸馏到目标推荐域，实现零样本跨域迁移。
- [IDProxy](../2603.01590-idproxy/README.md)：把多模态 LLM 内容表征对齐到协同 item-ID 空间，再通过多层 proxy 和 gate 注入工业排序。
- [SIGMA](../2602.22913-sigma/README.md)：用 LLM 做多视角 grounding，并以混合 SID/ID token 训练七任务生成模型。
- [S-GRec](../2602.10606-s-grec/README.md)：用 LLM 个性化语义 judge 产生偏好监督，再以 A2PO 蒸馏到轻量生成器。
- [Self-Evolving RecSys](../2602.10226-self-evolving-rec/README.md)：本地指令 LLM 读取实验 journal，逐轮选择未尝试的优化器、门控与 reward 配置，再以 validation 反馈晋级。
- [LLaTTE](../2601.20083-llatte/README.md)：用 BERT 语义特征、MLA 上游压缩、候选感知在线 attention 和 DHEN 门控连接多阶段序列。
- [RecGPT-V2](../2512.14503-recgpt-v2/README.md)：以层级 multi-agent、meta-prompt 和约束偏好 RL 生成淘宝用户意图标签与解释。
- [CRSD](../2510.11056-crsd/README.md)：用领域 LLM 产生标签与 reasoning 视图，通过同一学生的双视图对比自蒸馏把推理能力压入低延迟排序模型。
- [PLUM](../2510.07784-plum/README.md)：对 LLM 进行推荐语料 CPT 与 SFT，再以 Semantic ID 生成物品序列。
- [PinFM](../2507.12704-pinfm/README.md)：构建推荐 foundation model，并通过预训练—微调适配多个流量场景。
- [FilterLLM](../2502.16924-filterllm/README.md)：让 LLM 从新品文本直接预测用户词表分布，避免逐候选判断。
- [SERAL](../2502.13539-seral/README.md)：用 LLM 认知画像表示用户兴趣，再通过 IPO 与 nearline 链路优化惊喜度推荐。
- [LUM](../2502.08309-lum/README.md)：通过 next-condition-item 与 group query 学习用户知识，再把生成表征注入判别模型。
- [MIM](../2502.00321-mim/README.md)：多模态内容预训练和内容兴趣感知 SFT 把协同偏好对齐到内容空间。
- [MSD](../2412.06860-msd/README.md)：把 teacher 知识自回归蒸馏到 student，并用 LoRA 对齐 CTR 目标。
- [PRECISE](../2412.06308-precise/README.md)：联合 LLM 语义 token 与协同 ID，通过 top-k MoE 和两阶段训练建模用户序列。
- [LEADRE](../2411.13789-leadre/README.md)：以意图感知 Semantic ID 表示广告，并用 DPO 对齐展示与转化偏好。
- [LEARN](../2405.03988-learn/README.md)：冻结 LLM 生成内容增强表征，并用协同域适配改善冷启动。
- [BAHE](../2403.19347-bahe/README.md)：缓存原子行为的浅层语言编码，只在线执行高层行为聚合。
- [LSVCR](../2403.13574-lsvcr/README.md)：用 LoRA 学习 LLM 偏好，再通过 SSC/VCC 双序列目标对齐评论与行为。
- [NoteLLM](../2403.01744-notellm/README.md)：把内容压缩到特殊 token，以 GCL 注入协同信号，并用 CSFT 保持生成能力。
- [BEQUE](../2311.03758-beque/README.md)：生成 query rewrite，并用离线反馈、自采样和 PRO 优化改写质量。
- [KAR](../2306.10933-kar/README.md)：让 LLM 生成用户偏好和物品事实知识，再由 hybrid-expert adapter 融合进推荐器。
- [M6-Rec](../2205.08084-m6rec/README.md)：把多种推荐任务统一成自然语言形式，并以 option-adapter 轻量适配预训练模型。

## 生成、排序与冷启动

### 生成式召回与端到端推荐
- [Sona](../2608.11015-sona/README.md)：以历史压缩、层级 Semantic ID 生成和 item ranking 统一原有音乐推荐级联。
- [MetaStrategy](../2608.09440-metastrategy/README.md)：让 LLM 产生 typed ranking strategy，再由确定性 compiler 执行请求级多目标排序。
- [Gryphon-v2](../2608.06213-gryphon-v2/README.md)：共享生成和排序 encoder，以当前 rollout 与真实曝光双路 teacher distillation 统一召回、预排和精排。
- [HRPO](../2608.00750-hrpo/README.md)：将序列总奖励拆成层级 Semantic ID 前缀的 residual credit-to-go，以细粒度组相对更新改善生成推荐轨迹。
- [OxygenREC-v2](../2607.24255-oxygenrec-v2/README.md)：以目标行为 instruction 直接控制 SID 候选生成，再以训练期未来交互做熵感知自蒸馏。
- [UniR²](../2607.24439-unir2/README.md)：把用户 prefix、SID 轨迹和 item features 放入单一 decoder，以 DQ-PCA 和 ranking-only LoRA 同时完成生成召回与多目标排序。
- [Dual-purpose Semantic IDs](../2607.24865-dual-sid/README.md)：以分层协同 SID 统一检索 token 与可重建的内容 embedding，减少推荐模型 I/O。
- [BARGE](../2607.21028-barge/README.md)：以 ICA 保留 item 内多 token 结构，用 HPR 修正逐层 beam 漂移，并融合两个正交量化通道的候选。
- [TSGR](../2607.18796-tsgr/README.md)：用 residual semantic prefix 和并行价值码同时表达商品语义、全局价值与 query 条件价值，再联合训练 VRM。
- [RecGPT-V3](../2607.15591-recgpt-v3/README.md)：用两级 RQ-VAE 建立 SID 模态，联合记忆驱动意图与 latent reasoning 生成可直接检索的商品标识。
- [NONTP](../2607.12277-nontp/README.md)：用 EMA 未来状态对比和跨域池化补充 NTP 监督，并在推理时移除全部辅助分支。
- [Prompt Generation](../2607.11326-prompt-generation/README.md)：把异构特征压缩为生成提示，并以配置驱动方式支持多种召回合并策略。
- [CMSL](../2606.28533-cmsl/README.md)：以可学习 lenses 切分多兴趣 strand，再使用 HSTU 生成推荐结果。
- [G2Rec](../2606.20554-g2rec/README.md)：联合 soft graph 与生成式双目标学习结构化用户—物品关系。
- [DeGRe](../2605.25749-degre/README.md)：用离线前瞻列表价值产生 dense prefix labels，再蒸馏到低延迟在线生成器。
- [GrowthGR](../2605.17994-growthgr/README.md)：把新品长期 uplift 纳入生成式召回 reward，以 MoPO 平衡即时和长期价值。
- [CQ-SID](../2605.14434-cq-sid/README.md)：以类目约束残差 Semantic ID 缩小生成空间，再由专家奖励引导 group-relative 策略更新。
- [UniVA](../2605.05803-univa/README.md)：使用 Commercial SID、generation-as-ranking 和价值引导 trie beam 生成广告候选。
- [GloRank](../2604.25291-glorank/README.md)：全局 SID action space、listwise SFT 与组相对奖励共同优化全库生成重排。
- [GenRec](../2604.14878-genrec/README.md)：把整页作为 NTP 目标，并以 GRPO-SR 和 NLL 约束联合优化 page policy。
- [LWGR](../2605.18771-lwgr/README.md)：把 LLM 世界知识与推荐分数做约束融合，生成兼顾相关性与知识性的候选。
- [MBGR](../2604.02684-mbgr/README.md)：以 business-aware SID、共享专家和动态标签路由联合多个业务生成目标。
- [GLIDE](../2603.17540-glide/README.md)：用 residual Semantic ID 与长短期双 prompt 直接生成召回候选，强化非习惯内容探索。
- [GRC](../2602.23639-grc/README.md)：用结构化反思标签、轨迹 GRPO 和熵调度纠正 Semantic ID 自回归错误。
- [GR4AD](../2602.22732-gr4ad/README.md)：结合用户感知 Semantic ID、LazyAR 和可变长度生成完成广告召回。
- [SIGMA](../2602.22913-sigma/README.md)：以多视角 grounding 和混合 SID/ID token 进行多任务生成式推荐。
- [MFLI](../2602.16124-mfli/README.md)：把语义、新鲜度等多个索引 facet 联合学习，并以请求相关 allocation 完成快速召回。
- [S-GRec](../2602.10606-s-grec/README.md)：用 LLM judge 生成个性化偏好监督，再通过 A2PO 蒸馏到 SID 生成器。
- [DOS](../2602.04460-dos/README.md)：以协同/语义双流和正交 residual quantization 对齐 SID codebook 与生成空间。
- [OneMall](../2601.21770-onemall/README.md)：以场景 prompt、Semantic ID 和跨行为融合统一多个电商生成推荐场景。
- [HiGR](../2512.24787-higr/README.md)：通过层级 Semantic ID、粗到细 slate decoder 和 ORPO 生成整组推荐结果。
- [DualGR](../2511.12518-dualgr/README.md)：以长短兴趣路由、约束 SID 前缀和曝光惩罚改善生成召回。
- [IntSR](../2509.21179-intsr/README.md)：用显式 query、隐式会话意图与时间上下文统一搜索和推荐生成。
- [OnePiece](../2509.18091-onepiece/README.md)：在级联推荐中加入 context token、块级 latent reasoning 与渐进多任务训练。
- [OneRec-V2](../2508.20900-onerec-v2/README.md)：用 lazy decoder 提升生成效率，并通过真实反馈 RL 与 GBPO 优化序列。
- [GenRank](../2505.04180-genrank/README.md)：把点击、互动等动作编码成生成目标，以 action-oriented generation 完成排序。
- [PinRec](../2504.10507-pinrec/README.md)：根据目标 outcome 条件生成多 token 物品表示，直接完成召回。
- [COBRA](../2503.02453-cobra/README.md)：级联稀疏生成与稠密生成，在逐级缩小空间的同时保持精排能力。
- [OneRec](../2502.18965-onerec/README.md)：把推荐建模为 session Semantic ID 序列生成，并用 MoE 与偏好优化对齐反馈。
- [SessionRec](../2502.10157-sessionrec/README.md)：按 session 自回归生成候选，并结合曝光负例与 hard negative 训练。
- [LEADRE](../2411.13789-leadre/README.md)：生成意图感知 Semantic ID，并用 DPO 对齐广告序列的业务偏好。
- [HSTU](../2402.17152-hstu/README.md)：用分层顺序转导单元和生成式目标统一超长序列推荐。
- [TIGER](../2305.05065-tiger/README.md)：先用 RQ-VAE 构造层级 Semantic ID，再自回归生成目标物品。

### 排序网络与长序列
- [Netflix GenRec](../2608.10257-genrec-netflix/README.md)：用 prefill-only LLM 取代逐 token 解码，联合 catalog head、language loss 和 reward-weighted ranking loss 执行大目录精排。
- [CCFormer](../2607.28070-ccformer/README.md)：以字段分离的 ID/content 编码和门控融合增强冷内容泛化，再分层压缩远期 token、保留近期行为细节。
- [HA-MoE](../2607.27577-ha-moe/README.md)：用内容异构性控制多门控 MoE，在同一排序器内平衡通用与领域专长信号。
- [ROCS](../2607.27744-rocs/README.md)：把 request-side encoder 与 candidate-side late interaction 解耦，使同一表征路径覆盖大候选检索和精排序批量打分。
- [TWICE](../2607.25404-twice/README.md)：以点击/转化双时钟和单调 delay CDF 处理长期转化反馈未成熟问题。
- [CORE](../2607.24417-core-relevance/README.md)：将有序相关性拆成 High/Non-High 与条件 Mid/Low 两道边界，并把 step-GRPO reasoning 经 PostCoT 蒸馏给在线双头排序器。
- [Mosaic](../2607.24015-mosaic/README.md)：把不同归纳偏置的 user embedding 作为可独立演进的 specialist fleet，用 MRM 复合监督和去冗余损失增加下游有效信息。
- [YouTube Freshness](../2607.23749-youtube-freshness/README.md)：联合训练去偏与 serving 探索，专门改善新发行内容的曝光反馈闭环。
- [WHALE](../2607.17017-whale/README.md)：逐层耦合 Wukong 高阶交互和门控 HSTU 序列状态，避免双分支只在末端融合。
- [Long-History User Transformers](../2607.14331-long-history-transformer/README.md)：把长历史异步压缩成固定缓存，线上只运行近期事件 Transformer，兼顾历史容量与实时延迟。
- [TMallGS](../2607.13398-tmallgs/README.md)：对异构字段使用独立 QKV、噪声门控、FiLM 和 progressive loss，统一特征交互与序列建模。
- [DANet](../2607.12578-danet/README.md)：联合兴趣网络、折扣时频表征和用户/促销分布修正预测转化率。
- [MESH](../2607.12392-mesh/README.md)：用异构模块塔、信号放大与 RGBC 缓解 fresh/tail 梯度被头部内容淹没的问题。
- [SAM](../2607.12714-sam/README.md)：预测品类补货周期并动态屏蔽购买前已满足意图，降低购买后重复推荐。
- [SlimPer](../2607.12281-slimper/README.md)：以固定 knowledge slots 反复访问原始用户 token，把逐层状态从序列长度中解耦并支持 request-only 共享。
- [Memento](../2605.24051-memento/README.md)：用 query-conditioned MMR 动态平衡相关性与多样性。
- [HAP](../2603.03770-hap/README.md)：按候选难度分配轻量或强分支并对齐异构预排输出。
- [OneRanker](../2603.02999-oneranker/README.md)：用 fake item token 和一致性损失统一 generation/value/ranking。
- [HiSAC](../2602.21009-hisac/README.md)：用层级投票压缩超长历史，再以 query-conditioned soft routing 选择兴趣 agent。
- [ULTRA-HSTU](../2602.16986-ultra-hstu/README.md)：以半局部 attention、LBSL 逐层扩窗和 Mixture of Transducers 扩展 16k 用户历史。
- [MixFormer](../2602.14110-mixformer/README.md)：在统一网络中融合 dense 特征交互和序列建模，并按预算选择训练模块。
- [Kunlun](../2602.10016-kunlun/README.md)：在每层组合 GDPA Transformer 与分层 seed/global interaction block，并以 CompSkip 稳定深层训练。
- [MDL](../2602.07520-mdl/README.md)：把 feature、scenario 和 task token 化，让领域与任务参与每层特征交互。
- [MSN](../2602.07526-msn/README.md)：把大容量参数放入稀疏 Product-Key Memory，只激活 top-k 槽位控制计算。
- [TokenMixer-Large](../2602.06563-tokenmixer-large/README.md)：用 mixing/reverting、双粒度 SwiGLU、interval residual 和辅助监督扩展工业精排。
- [HyFormer](../2601.12681-hyformer/README.md)：联合用户序列与 query decoding，通过 query boosting 强化搜索排序。
- [OneTrans](../2510.26104-onetrans/README.md)：用统一因果 Transformer 覆盖多场景排序，并复用 KV cache。
- [ARGUS](../2507.15994-argus/README.md)：分解用户反馈与物品表示，在 Transformer 中建模超长音乐序列。
- [RankMixer](../2507.15551-rankmixer/README.md)：交替使用 token mixing 与逐 token FFN，并探索稀疏 MoE 扩容。
- [Click A, Buy B](../2507.15113-click-a-buy-b/README.md)：联合 CABA/CABB 分支和商品 taxonomy 重构电商转化归因。
- [MGOE](../2506.10520-mgoe/README.md)：把多任务相关性编码成宏观图，再由 graph experts 和任务塔联合预测。
- [TransAct V2](../2506.02267-transact-v2/README.md)：以候选感知终身序列和 next-action 多任务目标增强排序。
- [SORT-Gen](../2505.07197-sort-gen/README.md)：以 causal ordered regression 学习列表前缀的 CLICK/PAY 价值，通过多目标队列和内嵌 MMR 生成最终重排列表。
- [LONGER](../2505.04421-longer/README.md)：结合混合注意力、InnerTrans、token merge 与 KV cache 扩展超长序列。
- [FuXi-α](../2502.03036-fuxi-alpha/README.md)：用多通道注意力和 multi-stage FFN 扩展特征交互模型容量。
- [AdaF²M²](../2501.15816-adaf2m2/README.md)：用 feature-mask 多次前向和 state-aware adapter 改善特征学习与状态适配。
- [TWIN-V2](../2407.16357-twin-v2/README.md)：把百万级生命周期行为离线压缩为层次兴趣簇，再以候选相关粗搜和精确注意力恢复原始行为信号。
- [CWM](../2406.07932-cwm/README.md)：估计统一时长干预下的反事实观看收益以抵消 duration bias。
- [PLE](../recsys2020-ple-ple/README.md)：把共享与任务专属 experts 分开，并以 CGC gate 渐进抽取多任务表示。
- [DCN-V2](../2008.13535-dcn-v2/README.md)：使用低秩专家混合显式构造特征交互，并与 deep tower 联合排序。
- [SIM](../2006.05639-sim/README.md)：用候选条件 GSU 从超长历史中搜索相关子序列，再由 ESU 计算精确候选—行为交互。
- [BST](../1905.06874-bst/README.md)：让 Transformer 联合编码候选商品与带位置的行为序列。
- [DIEN](../1809.03672-dien/README.md)：用辅助监督抽取兴趣状态，再让候选相关门控驱动兴趣演化。
- [SASRec](../1808.09781-sasrec/README.md)：以因果自注意力编码行为序列，并预测下一物品。
- [MMoE](../kdd2018-mmoe-mmoe/README.md)：共享一组 experts，但由每个任务的独立 gate 学习不同专家组合。
- [ESMM](../1804.07931-esmm/README.md)：用 CTR 与 CTCVR 的 entire-space 联合目标学习 CVR，避免只看点击样本造成选择偏差。
- [DIN](../1706.06978-din/README.md)：使用候选感知局部激活从历史行为中提取相关兴趣，是经典 CTR 排序结构。
- [DeepFM](../1703.04247-deepfm/README.md)：让 FM 二阶交互与 deep 分支共享 embedding，端到端覆盖低阶和高阶特征组合。
- [YouTube DNN](../recsys2016-youtube-dnn-youtube-dnn/README.md)：把观看历史聚合为用户向量并经非线性塔变换，以 item embedding 点积完成候选召回。
- [Wide & Deep](../1606.07792-wide-deep/README.md)：联合显式 wide 交叉与 deep 表征，是工业精排从线性模型向深度模型过渡的经典骨架。

### 冷启动与语义-行为对齐
- [LLM Thompson Priors](../2608.03382-llm-ts-prior/README.md)：把 LLM 对新评论质量的语义判断编码为分群 Beta 先验，再让真实曝光反馈逐步覆盖先验。
- [PinEqualizer](../2607.22518-pinequalizer/README.md)：在 corpus、召回、排序和 utility 全漏斗识别 fresh 内容瓶颈，以内容特征、engagement dropout、cohort calibration 和 UCB 打破曝光反馈回路。
- [Pin-SCALE](../sigir2026-pin-scale-pin-scale/README.md)：以 engagement-aware residual codebook 和多视角对齐把 Semantic ID 接入判别式召回。
- [Proximity Features](../2607.12246-proximity-features/README.md)：以自适应群体地理 key 聚合行为，为匿名和首次访问用户提供冷启动特征。
- [LLM Retrieval](../2605.21969-llm-ad-retrieval/README.md)：生成 creative 层级语义属性，并用 primary/shadow 机制稳定广告召回。
- [PinCLIP](../2603.03544-pinclip/README.md)：把图文 contrastive learning 与 Pin-Board 共现邻居对齐，改善 fresh 内容表示。
- [Podcast MTL](../2601.02306-podcast-mtl/README.md)：共享 organic stream 与 ads/promotion 表征，把高资源任务知识迁移到冷启动 podcast。
- [SaviorRec](../2508.01375-saviorrec/README.md)：用行为监督训练内容 encoder，生成 RQ Semantic ID，再通过多行为模块对齐冷启动物品。
- [PRECISE](../2412.06308-precise/README.md)：联合 LLM 语义 token 与协同 ID，并针对冷启动物品进行序列预训练。

## 训练目标与决策优化

### 采样、蒸馏与强化学习
- [LLM Thompson Priors](../2608.03382-llm-ts-prior/README.md)：用 LLM 初始化分群 bandit 先验，并由 Thompson Sampling 在持续反馈下完成可校正的冷启动决策。
- [KGD](../2608.02738-kgd/README.md)：以 BMTP 和冻结知识分支保留可刷新的预训练信息，并用正交 ACR 控制它与协同几何的干扰。
- [HRPO](../2608.00750-hrpo/README.md)：依据层级生成前缀的后续收益分配 residual credit，使组相对策略优化不再只依赖整序列标量奖励。
- [ASARL](../2607.26593-asarl/README.md)：用多 Agent 校验与补齐长尾 relevance 数据，执行 SCT、交互偏好优化和在线 student 蒸馏。
- [RAMP](../2607.17473-ramp/README.md)：以富个性化路径为 teacher，通过 feature mask 和 KL alignment 改善仅有公共字段的流量。
- [UAME](../2607.17092-uame/README.md)：利用 Gaussian 排序不确定性识别多 pxtr 冲突样本，并自适应提高高偏差 pair 的训练权重。
- [Downstream Rewards](../2607.14192-downstream-rewards/README.md)：先筛选预测长期参与度的候选奖励，再将独立 reward heads 与即时目标联合优化。
- [Cluster GOOBS](../2607.00448-cluster-goobs/README.md)：用在线聚类感知的 sampler 扩大样本覆盖并缓解头部集中。
- [Rec-Distill](../2605.29755-rec-distill/README.md)：结合 batch/stream teacher，把大模型知识蒸馏到轻量 student。
- [Pinterest Complementary LLM Predictor](../2605.27856-pinterest-ads-llm/README.md)：先用 SFT 学习广告主列表，再以 GRPO 奖励优化列表质量。
- [MDCNS](../2605.19651-mdcns/README.md)：从多种负样本分布协同采样，并通过双模型交替更新减少偏差。
- [UniVA](../2605.05803-univa/README.md)：在请求内归一化 eCPM reward，并交替执行监督学习与强化学习。
- [AgenticRecTune](../2604.26969-agentic-rec-tune/README.md)：用 Actor–Critic 生成和审查配置，以 Online agent 回收实验反馈并由 SkillHub 跨轮复用。
- [LWGR](../2605.18771-lwgr/README.md)：用 reference confidence 约束融合结果，并通过 primal-dual 更新拉格朗日乘子。
- [Cross-domain KD](../2603.28994-cross-domain-kd/README.md)：把源域 teacher 知识蒸馏到目标域，减少跨域冷启动监督需求。
- [GR4AD](../2602.22732-gr4ad/README.md)：通过 RSPO 优化可变长度广告生成，并结合 LazyAR 降低推理成本。
- [S-GRec](../2602.10606-s-grec/README.md)：只采样少量 PSJ 反馈，并用 advantage 符号门控和幅度约束稳定 A2PO。
- [DRL-PUT](../2509.05292-drl-put/README.md)：使用 logged propensity 和策略梯度自动调节广告排序 utility 权重。
- [MPFormer](../2508.20400-mpformer/README.md)：目标 token 与动态 quota 让多任务检索共享训练/serving 资源。
- [OneRec-V2](../2508.20900-onerec-v2/README.md)：利用真实时长反馈和 GBPO 对生成序列进行强化学习。
- [SERAL](../2502.13539-seral/README.md)：通过 IPO 对齐惊喜度偏好，并在 nearline 链路应用认知画像。
- [LEADRE](../2411.13789-leadre/README.md)：使用 DPO 对齐 Semantic ID 生成与广告转化偏好。
- [BEQUE](../2311.03758-beque/README.md)：结合离线检索反馈、自采样和 PRO，优化生成式 query rewrite。

### 因果推断与长期价值
- [SWAG](../2607.25233-swag-bid/README.md)：把七日滑窗长期目标编码为 future plan，并门控影响当前广告 bid。
- [Downstream Rewards](../2607.14192-downstream-rewards/README.md)：筛选能预测未来参与度的长期 reward，再以独立 reward heads 注入多个推荐 surface。
- [Causal Retrieval](../2607.14161-causal-retrieval/README.md)：用 doubly-robust uplift 估计触发 shopping candidate generator 的增量收益，并同时考虑召回成本。
- [GrowthGR](../2605.17994-growthgr/README.md)：把新品长期 ItemLTV 纳入生成式召回 reward，平衡即时反馈与长期价值。

## 多阶段排序与混排

### 召回、粗排与精排协同
- [SPEAR](../2608.01738-spear/README.md)：以双 embedding 和乘法选择门把 query rewrite 与 item relevance 端到端对齐，同时保留原 query residual。
- [STEPS](../2608.01949-steps/README.md)：以 planning、execution、filter 三 Agent 联合决定推送动作和下一次系统唤醒时刻。
- [ROCS](../2607.27744-rocs/README.md)：把 request-side encoder 与 candidate-side late interaction 解耦，使同一表征路径覆盖大候选检索和精排序批量打分。
- [SlimPer](../2607.12281-slimper/README.md)：以固定 knowledge slots 反复读取用户历史，让 request-only 表征可跨候选复用，再进行候选相关精排。
- [CS3](../2604.19269-cs3/README.md)：在保持双塔 ANN 召回兼容的前提下，通过循环修正、跨塔同步和级联教师增强交互能力。
- [COBRA](../2503.02453-cobra/README.md)：先执行稀疏生成缩小候选空间，再用稠密生成细排，形成级联召回—排序路径。

### 重排、混排与多目标页面决策
- [DEGR](../2608.04809-degr/README.md)：用 cohort 内 embedding 多样性、adaptive reward ORPO 和 greedy selection 控制跨曝光重复。
- [Twitch Multi-Objective Ranking](../2608.04455-twitch-mor/README.md)：以 fresh/delayed 标签、生命周期 gate 和共享专家统一直播场景的多目标排序，显式平衡即时互动与滞后价值。
- [Pinterest Complementary LLM Predictor](../2605.27856-pinterest-ads-llm/README.md)：把 LLM advertiser prior 与常规候选按 validation 选择的 quota 混合，再作为排序特征使用。
- [DeGRe](../2605.25749-degre/README.md)：将离线 lookahead 的列表价值蒸馏为在线 dense prefix labels，降低生成式重排延迟。
- [Memento](../2605.24051-memento/README.md)：用 query-conditioned MMR 在相关性和多样性之间动态调整混排权重。
- [GenRec](../2604.14878-genrec/README.md)：把整页结果作为生成目标，并联合 page reward 与 NLL 约束优化页面级决策。
- [Dual-Rerank](../2604.07420-dual-rerank/README.md)：AR 教师刻画顺序依赖，NAR 学生并行推理并联合列表效用蒸馏。
- [DRL-PUT](../2509.05292-drl-put/README.md)：利用 logged propensity 和策略梯度自动调节广告混排 utility 权重。
- [SORT-Gen](../2505.07197-sort-gen/README.md)：以 ordered regression 估计列表前缀价值，再按 CLICK/PAY 队列、mask 和 MMR 生成混排结果。
- [CDM](../2406.09021-cdm/README.md)：用 MMR 教师生成可控多样性列表并蒸馏上下文边际收益。

## 内容理解、审核与风险控制

### 内容理解与语义表征
- [DME](../2608.02148-dme/README.md)：以对比预训练建立统一向量空间，再用 typed latent reasoning 和双向重建保留检索相关的细粒度多模态证据。
- [FLUID](../2605.21832-fluid/README.md)：把直播内容切片量化为两级 LUCID，以内容表示替代生命周期很短的候选 ID。
- [MM-LLM](../2605.09338-mm-llm/README.md)：把图像、视频等内容转换为 caption/token 特征，再注入推荐模型增强内容理解。
- [PinCLIP](../2603.03544-pinclip/README.md)：把图文对比学习与 Pin-Board 共现邻居目标结合，改善 fresh 内容表示。
- [IDProxy](../2603.01590-idproxy/README.md)：把多模态内容先对齐到 item-ID 协同空间，再通过多层 proxy 与 gate 接入排序。
- [MIM](../2502.00321-mim/README.md)：以遮盖多模态预训练和内容兴趣感知 SFT 对齐内容与协同空间。
- [PRECISE](../2412.06308-precise/README.md)：联合 LLM 语义 token 与协同 ID，并针对冷启动内容进行序列预训练。

### 相关性审核与数据质量
- [ASARL](../2607.26593-asarl/README.md)：以 Reason、Critic 和 Gen Agent 审核、修复长尾 relevance 数据，再蒸馏到线上 student。
- [CORE](../2607.24417-core-relevance/README.md)：把 High/Mid/Low 相关性拆成级联边界，用 step-GRPO 训练 reasoning 后蒸馏给在线审核/排序头。
- [MESH](../2607.12392-mesh/README.md)：通过异构塔与 residual gated bias correction 防止 fresh/tail 内容信号被头部样本淹没。
- [Cluster GOOBS](../2607.00448-cluster-goobs/README.md)：用在线聚类感知采样扩大训练覆盖，降低头部内容对数据分布的支配。

### 隐私、策略约束与风险控制
!!! note "审核风控覆盖边界"
    当前实现主要覆盖相关性审核、训练数据质量、隐私受限特征与策略约束；内容安全、
    作弊/欺诈和广告合规仍是明确缺口，不能用相关性模型冒充已实现。

- [RAMP](../2607.17473-ramp/README.md)：训练个性化/公共双路径，并用 feature mask 与预测对齐适配隐私受限和字段缺失流量。
- [UAME](../2607.17092-uame/README.md)：显式建模多目标不确定性和标签冲突，降低高分歧样本对排序策略的风险。
- [Causal Retrieval](../2607.14161-causal-retrieval/README.md)：用 doubly-robust uplift 同时评估触发候选源的增量收益与调用成本，控制无效干预。
- [Proximity Features](../2607.12246-proximity-features/README.md)：以隐私合规的群体地理特征服务匿名用户，避免依赖持久用户 ID。

## Serving 与研究基础设施

### Serving / efficiency
- [ROCS](../2607.27744-rocs/README.md)：请求表征只计算一次，候选相关交互延后并批量执行；本地同时报告排序质量和进程内候选评分吞吐。
- [Prompt Generation](../2607.11326-prompt-generation/README.md)：训练和 serving 共享特征配置，并通过 event replay 与 token compression 控制延迟。
- [NOVA](../2606.27243-nova/README.md)：用四级验证、失败方向和 architecture gradient 提高自动架构进化的有效通过率。
- [RankGraph-2](../2606.18379-rankgraph2/README.md)：离线预计算 popularity-corrected PPR 并用 cluster index 压缩线上图召回。
- [EvoRec](../2606.28368-evorec/README.md)：把历史实验蒸馏为可复用 skill memory，使自动研究方法本身跨代进化。
- [Pinterest Complementary LLM Predictor](../2605.27856-pinterest-ads-llm/README.md)：离线批量生成 advertiser prior，线上作为传统候选生成的补充信号。
- [UniVA](../2605.05803-univa/README.md)：按请求构造个性化 trie，并用 value-guided beam search 约束有效广告路径。
- [CS3](../2604.19269-cs3/README.md)：在保持双塔 ANN 兼容的前提下，以循环修正、跨塔同步和教师协同补充交互能力。
- [LWGR](../2605.18771-lwgr/README.md)：在 nearline 阶段缓存世界知识，线上只执行轻量 cross-attention 融合。
- [SIGMA](../2602.22913-sigma/README.md)：使用 prefix-local item retrieval 和 nearline U2I 控制生成检索成本。
- [S-GRec](../2602.10606-s-grec/README.md)：LLM judge 只在训练期调用，线上仅部署轻量 SID generator。
- [OneTrans](../2510.26104-onetrans/README.md)：在多场景间共享因果 Transformer，并复用 KV cache 加速线上推理。
- [OneRec-V2](../2508.20900-onerec-v2/README.md)：用 lazy decoder 和并行策略降低生成式推荐延迟。
- [RADAR](../2506.07261-radar/README.md)：将高成本全排序移到请求后异步执行，并缓存为下一请求召回候选。
- [LONGER](../2505.04421-longer/README.md)：通过 token merge、混合注意力和缓存降低超长序列 serving 成本。
- [MSD](../2412.06860-msd/README.md)：把 teacher 知识蒸馏到小模型，并以 LoRA 与缓存表征控制 CTR serving 成本。
- [BAHE](../2403.19347-bahe/README.md)：缓存原子行为的浅层编码，只在线执行高层序列聚合。
- [BEQUE](../2311.03758-beque/README.md)：将检索反馈放在离线训练阶段，线上只保留轻量 query 生成。
- [M6-Rec](../2205.08084-m6rec/README.md)：冻结大部分预训练语言模型，仅用 option-adapter 适配推荐任务。
