# 复现总览

这是全部 reproduction adapter、实现状态和实验结论的**底层统一总表**。后续新增论文或
重跑实验时，只更新本页和对应论文 README，不再新建阶段性审计或批次汇总页。

工业搜广推论文可按[公司](catalog/by-company.md)、[主题](catalog/by-topic.md)或
[年月](catalog/by-month.md)浏览；基础模型的架构、预训练、多模态与推理效率进入
[基础模型目录](../foundation-models/README.md)，训练后算法进入
[LLM 后训练](../post-training/README.md)。论文详情和物理路径保持不变。

每轮新增论文不再依赖零散搜索记录，而是先建立候选全集、再逐项进入明确终态；规则、
机器账本和强制校验见[论文发现闭环与防遗漏审计](../paper-discovery-audit.md)。

## 原论文关键图规范

每篇论文页在“背景与主要改动”和“核心公式”之间固定展示一张原论文关键图，
优先选择架构图、模型结构图或训练/推理流程图。图片本地保存到论文目录的
`assets/paper-figure-01.png`，页面同时链接原始来源并保留版权说明。论文没有
结构图时，选择最能解释方法的原始流程、算法或实验截图；无法自动取得全文的
页面必须明确写出公开来源边界，不能用本地 Mermaid 图冒充原论文截图。

新增或刷新论文图时执行：

```bash
python -m pip install -e '.[paper-figures]'
python scripts/sync_paper_figures.py --only <arXiv ID 或论文目录关键词>
```

全库检查可执行：

```bash
python scripts/sync_paper_figures.py --workers 3
pytest tests/test_research_module_docs.py
```

抽取器优先使用 arXiv HTML 的图注关系，老论文自动回退到 PDF 图注定位裁剪。
少数非 arXiv 论文使用脚本中经过人工核验的公开 PDF 映射；稳定注释标记允许
后续重复刷新而不产生重复小节。

## 选文与记录规则 {#selection-policy}

- **工业论文硬门槛**：正文必须披露真实生产流量的量化线上 A/B；或由用户明确认可论文所述的统计显著全流量发布、业务收益与 guardrail 结论。仅“已部署”、离线 SOTA 或模拟器结果不算；未披露具体 lift 的 full-traffic 论文必须明确标注，不能换算成百分比。
- **基础模型论文门槛**：不要求线上 A/B，但必须有公开 benchmark、同预算对照和可在 WikiText 等公开数据上实际训练的核心方法；只写公式或固定打分不进入复现表。
- **具名例外**：SASRec、TIGER、Wide & Deep、DCN-V2、DIEN、BST、DeepFM、YouTube DNN、ESMM、MMoE、PLE 是用户明确要求补齐的经典骨架；其中缺量化线上 A/B 的条目会逐篇明示，不据此放宽后续新工业论文的门槛。
- **本地结果口径**：每篇 README 明确基线、实验组、数据、主指标和相对变化；论文线上结果、本地跨模型比较、模块消融和效率对照分开写。
- **保真度**：公开数据替代私有数据或缩小规模可以接受；核心网络、训练目标或推理路径被 heuristic 替代时，只能标为“概念验证”。默认批量运行不包含概念验证。
- **论文信息**：每篇 README 顶部固定列出论文链接、公司/机构、精确首次公开日期及来源、原作者是否开源代码、Adapter 和本地复现代码位置；未找到原作者代码时必须明确写“否”，不能留空。没有独立 arXiv 页的正式会议论文使用官方论文集/机构发布页，不伪造 arXiv ID。

统一 DIN 实验使用 MovieLens-100K、时间 leave-two-out、全物品排序和 seeds 42/43/44；SERAL、LEADRE、COBRA、ARGUS、GR4AD、MM-LLM 使用同一 DIN NDCG@10 `0.02167`，Cross-domain KD 在独立 target split 上使用 DIN `0.05518`。这些结果只代表当前公开小数据协议，不等同于论文私有工业数据结论。

## 当前进度

- 已审计个人博客两个工业落地章节的 94 个主条目和 138 个 arXiv 链接。
- 已登记并复核 268 个 adapter；其中推荐论文继续执行线上 A/B/full-traffic 证据门槛，基础模型论文执行公开 benchmark 与真实训练门槛。
- 暂缓：AIGQ（缺等价 query/CTR reward）、RaG（依赖视频生成与质量反馈）、RoleGen（缺 conversion trajectory 与线上反馈闭环）、LCU（数据需保密协议）。
- 跳过：EGA-V1；仅有离线结果或无法核验量化线上 A/B 的论文不进入实现队列。
- 2026 年剩余硬门槛论文已进入核心机制复现；2026-07-27 的 P1 批次加入 8 篇工业推荐论文，并把 Engram、Looped Latent Attention、GaugeQuant 三个真实算子接入 LLM evolve。GRACE、DLMRec、LO-FAR、PRL 因缺量化线上证据未纳入推荐复现。
- 2026-07-28 最近论文增量加入 Meta Mosaic、快手 UniR²、美团 CORE 与基础模型 DataOrchestra；前三篇均通过量化线上 A/B 门槛，DataOrchestra 有官方代码与公开预训练 benchmark。
- 2026-07-30 跨领域增量加入腾讯 CCFormer、Teads Open Web UFM、Meta ROCS 与基础模型 WIDE；前三篇分别提供线上 A/B、全生产流量或量化部署证据，WIDE 提供官方代码和公开剪枝/吞吐实验。
- 2025 工业 P0 补漏加入 MIM、FilterLLM、FuXi-α、RecGPT-V2、HiGR、DRL-PUT、AdaF²M²、MGOE 与 Click A Buy B；9 篇均有量化生产 A/B，并已在 MovieLens-1M 上执行独立核心机制。
- 2025 LLM evolve P0 加入 DeepSeek NSA、Qwen Gated Attention 与 Moonshot Muon；结构和优化器可组合搜索，并完成 WikiText-2 同预算对照与四轮 evolve。

## Google / Meta 正文证据补漏（10 个 P0 adapter）

- `memory-layer` · [Meta Memory Layer](2607.25110-memory-layer/README.md)：训练内 eta=1 writeback 把 item cache 纳入模型状态，并用 always-on 属性表征覆盖冷启动与缺失 ID。
- `scalr` · [Meta SCALR](2606.00282-scalr/README.md)：从跨域事件学习条件分布，以概率采样而非 top-k 复制生成覆盖更广的训练事件。
- `hill-index` · [Meta HILL](2604.12965-hill-index/README.md)：以 coarse-to-fine residual quantization 学习分层索引并减少在线候选打分量。
- `semantic-native-longseq` · [Google Semantic-Native Long Sequence Modeling](2606.07546-semantic-native-longseq/README.md)：用层级语义 ID、bigram、时间折叠及 global-local pooling 扩展视频历史。

- `ha-moe` · [Google Discover HA-MoE](2607.27577-ha-moe/README.md)：异构性门控多专家；7 天 1% 流量 A/B。
- `dual-sid` · [YouTube Dual-purpose Semantic IDs](2607.24865-dual-sid/README.md)：SID 同时表达协同身份并重建内容 embedding。
- `agentic-rec-tune` · [Google Discover AgenticRecTune](2604.26969-agentic-rec-tune/README.md)：Actor–Critic–SkillHub 多轮推荐优化闭环。
- `mfli` · [Meta MFLI](2602.16124-mfli/README.md)：多切面可学习实时检索索引。
- `kunlun` · [Meta Kunlun](2602.10016-kunlun/README.md)：GDPA、分层 seed pooling 与 CompSkip 的统一深层架构。
- `ultra-hstu` · [Meta ULTRA-HSTU](2602.16986-ultra-hstu/README.md)：semi-local attention、LBSL 与 Mixture of Transducers。

这批候选均由机构/主题先召回，再逐篇检查正文和表格；不再要求摘要先出现 `A/B` 关键词。六篇均完成公开数据实验、固定指标、论文原图与 evolve 可执行映射（AgenticRecTune 对应控制器回归样例，而非伪造网络结构）。

## 2026-08-24 近期跨领域增量

- `oneshot-index` · [OneShot](2607.27475-oneshot-index/README.md)：Meta/Instagram 将层级索引与排序目标共同训练，并以 neural scoring 替代纯点积检索；已全量部署全球流量。
- `clockrope` · [ClockRoPE](2607.26369-clockrope/README.md)：YouTube/Google DeepMind 从周期 kernel 的 Fourier 频谱采样旋转频率，为生成式召回显式建模日、周 routine。
- `next-vlm` · [NEXT](2607.24789-next-vlm/README.md)：Meta 用 8B VLM 构造 item→intent→item 的 directed NKG，并把推理移到离线、线上只注入验证边。
- `onemodel` · [OneModel](2608.18606-onemodel/README.md)：小红书以共享长序列 backbone、场景门控和分层用户表征统一推荐、广告与商家排序，并披露三个生产场景的量化 A/B。
- `rare` · [RARE](2608.21236-rare/README.md)：把表征编辑方向投影到 MoE router 零空间，并在下游保护层校正传播漂移，保持原专家路径。

## 2026-08-26 最新增量

- `tagr` · [TAGR](2608.24034-tagr/README.md)：快手直播广告用稳定词表的两级语义/协同 ID、多尺度兴趣和行为价值门控做生成式推荐；论文生产 A/B 的 LRE +8.5%、SCC +7.4%、Revenue +16.1%。
- `wemm-embedding` · [WeMM-Embedding](2608.24053-wemm-embedding/README.md)：微信把多模态对齐、跨尺度 teacher refinement 与 Matryoshka embedding 合成统一检索模型；报告说明 14 项线上 A/B 收益已全量发布并公开代码与权重。

## 2026-08-27 最新增量

- `dceo` · [DCEO](2608.25635-dceo/README.md)：淘宝搜索以上下文条件 actor 直接优化长期用户价值的相对因果效果；41 天生产 A/B GMV +0.36%。
- `transretrieval` · [TransRetrieval](2608.25528-transretrieval/README.md)：跨域广告召回使用 norm-aware 聚合、target-token 压缩和位置化 domain embedding；一个月 5% 流量 A/B 收入 +2.53%。
- `vbvr-pro` · [VBVR-Pro](2608.26105-vbvr-pro/README.md)：以任务专用可执行 scorer 替代通用 VLM judge，为原生视觉推理提供状态级 verifiable reward。
- `mllmclip` · [MLLMCLIP](2608.25575-mllmclip/README.md)：从 MLLM 各层按 attention 选 teacher token，再以 CKA 对齐轻量 CLIP 的视觉与文本特征。

## 2026-08-29 最新增量

- `friend-gnn` · [VK Friend-GNN](2608.27413-friend-gnn/README.md)：以多哈希共享表压缩超大用户 embedding，并用按时间排序邻接与二分 cutoff 避免时序邻居采样的数据泄漏；论文在 VK 生产 A/B 中报告好友添加数 +16.0%、独立添加好友用户数 +11.5%。
- `pace-vlm` · [PACE](2608.27206-pace-vlm/README.md)：用浅层视觉 preview 自适应设置 token budget，并融合 LLM/ViT 注意力；真实 Qwen2.5-VL + RealWorldQA 路径在 A30 验证。
- `twinkv` · [TwinKV](2608.27128-twinkv/README.md)：以 orphan/donor 配对修复任意 KV eviction policy，保持缓存预算严格不变；真实 Qwen3 KV + WikiText-2 长上下文路径在 A30 验证。

## 2026 历史扫描 B01～B03（18 个 adapter）

- `dynamic-codebook` · [Dynamic Single-Level Large Semantic Codebook](2608.21012-dynamic-codebook/README.md)：曝光加权动态大码本、独立碰撞码和短 SID 解码。
- `netflix-mediafm` · [Netflix Multimedia Asset Personalization](2608.18322-netflix-mediafm/README.md)：冻结多模态特征、统一资产双塔和查询感知打分。
- `ogr` · [Once Generated, Ranked](2608.17613-ogr/README.md)：统一语义-协同 ID、列表规划与保守策略对齐。
- `inthq` · [IntHQ](2608.09634-inthq/README.md)：长短双流上的分层任务交互查询。
- `pushdualgen` · [PushDualGen](2608.07989-pushdualgen/README.md)：先生成 SID，再按需生成可解释 copy。
- `recharness` · [RecHarness](2607.29241-recharness/README.md)：用 bandit 在有限预算下路由多轮结构实验。
- `gala` · [GALA](2607.29213-gala/README.md)：多模态三元组预训练、GRPO 行为对齐和 ID 门控融合。
- `feedback-policy` · [Feedback-Grounded Policy Discovery](2607.27789-feedback-policy/README.md)：从反馈发现生成策略并蒸馏到线上轻量排序器。
- `real-estate-rerank` · [LLM-Based Re-Ranking for Real Estate Search](2607.14835-real-estate-rerank/README.md)：结合对话意图、房源文本和候选集合统计重排。
- `adaptive-ad-load` · [Adaptive Ad Load Design](2607.14418-adaptive-ad-load/README.md)：在收入与转化约束下动态选择广告数量。
- `guess-where-you-go` · [Guess Where You Go](2607.26073-guess-where-you-go/README.md)：时空 SID、课程训练和长期反馈策略优化。
- `genpage` · [GenPage](2606.31031-genpage/README.md)：以单模型生成整页并用长期奖励后训练。
- `journeyformer` · [JourneyFormer](2606.19108-journeyformer/README.md)：统一编码长期与短期 Airbnb guest journey。
- `l2rec` · [L2Rec](2605.26717-l2rec/README.md)：个性化双视图 LoRA-MoE 与跨视图融合。
- `qgs` · [QGS](2605.25514-qgs/README.md)：query-item 联合序列、Linear HSTU 和生成式搜索。
- `tubifm` · [TubiFM](2605.23702-tubifm/README.md)：同一 user-story foundation model 统一三种排序任务。
- `pearl-percentile` · [PEARL](2605.21752-pearl-percentile/README.md)：多样本对比得到低方差、低偏置的行为 percentile。
- `dadf` · [DADF](2605.17863-dadf/README.md)：冻结基模型并学习分布感知的乘性残差校正。

## 本轮全域 P0 补齐（19 个 adapter）

- `glorank` · [GloRank](2604.25291-glorank/README.md)
- `dual-rerank` · [Dual-Rerank](2604.07420-dual-rerank/README.md)
- `oneranker` · [OneRanker](2603.02999-oneranker/README.md)
- `radar` · [RADAR](2506.07261-radar/README.md)
- `dualgr` · [DualGR](2511.12518-dualgr/README.md)
- `mpformer` · [MPFormer](2508.20400-mpformer/README.md)
- `hap` · [HAP](2603.03770-hap/README.md)
- `onepiece` · [OnePiece](2509.18091-onepiece/README.md)
- `intsr` · [IntSR](2509.21179-intsr/README.md)
- `cdm` · [CDM](2406.09021-cdm/README.md)
- `cwm` · [CWM](2406.07932-cwm/README.md)
- `rope` · [RoPE / RoFormer](2104.09864-rope/README.md)
- `alibi` · [ALiBi](2108.12409-alibi/README.md)
- `gqa` · [GQA](2305.13245-gqa/README.md)
- `hymba` · [Hymba](2411.13676-hymba/README.md)
- `moba` · [MoBA](2502.13189-moba/README.md)
- `blt` · [Byte Latent Transformer](2412.09871-blt/README.md)
- `doremi` · [DoReMi](2305.10429-doremi/README.md)
- `data-mixing-laws` · [Data Mixing Laws](2403.16952-data-mixing-laws/README.md)

每篇详情页都给出原文代码状态、核心公式、原论文关键图、原文效果、本地公平基线、固定指标与可执行命令；本地负结果同样保留。

## 本轮全域 P1 补齐（8 个 adapter）

- 工业推荐：[TWIN-V2](2407.16357-twin-v2/README.md)、[SIM](2006.05639-sim/README.md)、[CRSD](2510.11056-crsd/README.md)。
- 多模态：[CLIP](2103.00020-clip/README.md)、[BLIP-2](2301.12597-blip2/README.md)、[LLaVA](2304.08485-llava/README.md)、[SigLIP 2](2502.14786-siglip2/README.md)、[SmolVLM](2504.05299-smolvlm/README.md)。
- 推理与部署：[Speculative Decoding](2211.17192-speculative-decoding/README.md)、[AWQ](2306.00978-awq/README.md)、[Medusa](2401.10774-medusa/README.md)。

## 2026-08-09 P0/P1 增量（9 个 adapter）

- `twitch-mor` · [Twitch Multi-Objective Ranking](2608.04455-twitch-mor/README.md)
- `llm-ts-prior` · [LLM-Derived Thompson Priors](2608.03382-llm-ts-prior/README.md)
- `kgd` · [KGD](2608.02738-kgd/README.md)
- `hrpo` · [HRPO](2608.00750-hrpo/README.md)
- `bakron` · [BaKron](2608.06291-bakron/README.md)
- `macro` · [MACRO](2608.05872-macro/README.md)
- `hilp` · [HiLP](2608.05806-hilp/README.md)
- `dblast` · [DBLast](2608.05448-dblast/README.md)
- `qevict` · [QEvict](2608.05326-qevict/README.md)

前四篇工业论文满足量化线上 A/B / 全量部署门槛；后五篇归入基础模型目录。所有条目均已执行核心机制并保存 seed 42 指标，负结果与不显著线上结果不做美化。

## 2026-08-13 MR7 增量（3 个 adapter）

- `sona` · [Sona](2608.11015-sona/README.md)：压缩历史、Semantic ID 自回归生成与 item ranker 单模型替换音乐推荐级联。
- `metastrategy` · [MetaStrategy](2608.09440-metastrategy/README.md)：LLM 生成 typed strategy，由确定性 compiler 执行多目标排序。
- `gas` · [GAS](2608.12209-gas/README.md)：用可删除 MoT 生成分支执行连续 Next Embedding Prediction，以零部署开销增强多模态理解。

两篇工业论文均在正文披露真实流量量化 A/B；本地 MovieLens-1M 训练均保留负结果，不把原文线上收益移植为复现指标。GAS 属于基础模型/多模态论文，不要求线上 A/B，本地公开像素实验与论文数字分栏呈现。

## 2026-08-20 工业增量（2 个 adapter）

- `connectionmind` · [ConnectionMind](2608.10187-connectionmind/README.md)：Meta 与密歇根州立大学将时序异构图、最短路径 SFT、规则奖励 GRPO 和路径蒸馏组合为社交推荐系统；数千万用户多周 A/B 的曝光、观看时长和 session 均有量化提升。
- `dream` · [DREAM](2608.09408-dream/README.md)：淘宝在原召回/排序链路上增加三层意图、策略记忆、typed 参数编译与离线/在线 Reward Dual Loop；精排+重排线上 IPV +2.71%、Core IPV +3.06%、GMV +1.31%。

两篇均执行了各自核心训练/控制链路；ConnectionMind 使用论文同款 Delicious 数据并保留 NDCG@10 -7.44% 的负结果，DREAM 的本地正向相关性伴随明显头部偏置，文档同时披露。

## 2026 历史扫描 B04～B06（19 个 adapter）

19 篇均逐篇核验正文中的生产 A/B 位置，并在 MovieLens-100K 的相同切分、候选集与 seed 42 下运行独立核心机制；线上数字与本地结果严格分栏。

### B04

- `prl-puts` · [PRL-PUTS](2605.16344-prl-puts/README.md)：双头 Q 网络与 Pareto utility 扫描。
- `ektm` · [Effective Knowledge Transfer for Multi-Task Recommendation Models](2605.05730-ektm/README.md)：任务相似度驱动的多任务知识迁移。
- `adasid` · [AdaSID](2604.23522-adasid/README.md)：碰撞负载与语义相容性驱动的动态 SID。
- `unirec-coa` · [UniRec](2604.12234-unirec-coa/README.md)：属性链生成与业务偏好对齐。
- `uniscale` · [UniScale](2603.24226-uniscale/README.md)：Entire-Space 数据与模型协同扩展。
- `gatesid` · [GateSID](2603.22916-gatesid/README.md)：冷启动感知的语义/协同门控。

### B05

- `aigq` · [AIGQ](2603.19710-aigq/README.md)：混合 query 生成与 IL-GRPO。
- `safro` · [SaFRO](2603.19585-safro/README.md)：满意度感知的双重相对策略优化。
- `sort-ranking` · [SORT](2603.03988-sort-ranking/README.md)：工业 Ranking Transformer 系统优化。
- `quasid` · [QuaSID](2603.00632-quasid/README.md)：资格感知的 SID 碰撞约束。
- `gpl-prerank` · [Generative Pseudo-Labeling](2602.20995-gpl-prerank/README.md)：LLM 伪标签增强在线预排序。
- `ltv-video-ranking` · [Long-term Value Prediction](2602.17058-ltv-video-ranking/README.md)：位置去偏与长期价值建模。

### B06

- `rgalign-rec` · [RGAlign-Rec](2602.12968-rgalign-rec/README.md)：排序器指导的潜在 query 对齐。
- `linkedin-feed-sr` · [LinkedIn Feed SR](2602.12354-linkedin-feed-sr/README.md)：工业长序列 Feed 排序。
- `cadet` · [CADET](2602.11410-cadet/README.md)：候选后上下文条件化广告 CTR。
- `diffureason` · [DiffuReason](2602.09744-diffureason/README.md)：扩散式潜在推理与 GRPO。
- `sarm` · [SARM](2602.09401-sarm/README.md)：MLLM 语义 anchor 增强直播排序。
- `ml-dcn` · [ML-DCN](2602.09194-ml-dcn/README.md)：Masked Low-Rank DCN 特征交叉。
- `rag-qac` · [RAG-QAC](2602.01023-rag-qac/README.md)：RAG 与多目标对齐的查询补全。

<!-- historical-b07:start -->
## 2026 历史扫描 B07（9 个基础模型 / 基础设施 adapter）

- `tcab` · [Fast A/B/n Testing: Exact Multi-Policy Comparison via Tree-Coupled Feedback Sharing](2608.12831-tcab/README.md)：用最大耦合和最小生成树共享相同决策的反馈，同时保持每个自适应策略的边际轨迹分布不变。
- `olmpool-long-context` · [Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension](2608.10296-olmpool-long-context/README.md)：以受控 7B 模型池隔离 normalization、GQA、预训练长度和滑窗注意力对长上下文扩展的复合影响。
- `distillcache` · [DistillCache: KL-Guided Adaptive KV-Cache Eviction for Memory-Efficient LLM Inference](2608.08878-distillcache/README.md)：把 KV 淘汰视为序列决策，以逐步 KL 奖励训练轻量策略保留未来预测分布。
- `autonomy-heads` · [Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry](2608.06849-autonomy-heads/README.md)：直接从冻结 QK 投影的谱有效秩区分 retrieval 与 streaming heads，无需校准数据或运行时门控。
- `physics-mm-pretraining` · [Towards Physics of Multimodal Pretraining: Knowledge Flow, Modality Synergy, Early Unification, and Recipes](2608.05000-physics-mm-pretraining/README.md)：用受控实验刻画模态知识流、协同/竞争、早期统一和共享 attention+norm/模态专属 FFN 配方。
- `ttcd` · [Learning What to Remember: Test-Time Training via Context Distillation](2608.01672-ttcd/README.md)：长窗口教师以隐藏状态差异监督短窗口学生的 fast weights，使有限记忆优先保留未来有用信息。
- `dart` · [DART: Decoded Attention over Recurrent States for Efficient Long-Context Sequence Modeling](2608.02032-dart/README.md)：保留 Mamba-2 chunk state contributions，解码 token-conditioned K/V 并执行 state-memory attention。
- `transmem` · [TransMem: Transforming Hidden States into Memory for Large Language Models](2607.29032-transmem/README.md)：将冻结骨干的稀疏历史 hidden states 变换成可复用参数记忆，并用 evidence-conditioned self-distillation 学门控。
- `c2kv` · [C²KV: Compressed and Composable KV Cache Reuse for Efficient LLM Inference](2607.17715-c2kv/README.md)：以 compression tokens 和结构化 attention 学习位置无关、可拼接的压缩 KV manifold，并联合训练压缩与复用。

<!-- historical-b07:end -->

## 全部复现（262/262）

| 保真度 | Adapter / 论文 | 原论文线上效果 | 本地结论 |
|---|---|---|---|
| 核心机制 | `pace-vlm` · [PACE](2608.27206-pace-vlm/README.md) | 无工业 A/B；论文报告 10% 视觉 token 保留 93.8% 平均性能、TTFT 最高 3.1× | APC/DDAE 公式、RealWorldQA 同 checkpoint 质量/token/延迟/显存和 Evolve 配方均可审计 |
| 核心机制 | `twinkv` · [TwinKV](2608.27128-twinkv/README.md) | 无工业 A/B；LongBench/LooGLE/RULER/MMLU-Pro 离线结果且含失败任务 | fixed-budget repair、真实 Qwen3 KV reconstruction/延迟/显存和 Evolve attention operator 均可审计 |
| 核心机制 | `prl-puts` · [PRL-PUTS](2605.16344-prl-puts/README.md) | P2P impressions +0.30% | 双头 Q 网络与 Pareto utility 扫描；NDCG@10 +39.64% |
| 核心机制 | `ektm` · [Effective Knowledge Transfer for Multi-Task Recommendation Models](2605.05730-ektm/README.md) | eCPM +3.93% | 任务相似度驱动的多任务知识迁移；NDCG@10 +10.98% |
| 核心机制 | `adasid` · [AdaSID](2604.23522-adasid/README.md) | GPM +1.16% | 碰撞负载与语义相容性驱动的动态 SID；NDCG@10 -6.30% |
| 核心机制 | `unirec-coa` · [UniRec](2604.12234-unirec-coa/README.md) | GMV +5.60% | 属性链生成与业务偏好对齐；NDCG@10 -4.93% |
| 核心机制 | `uniscale` · [UniScale](2603.24226-uniscale/README.md) | GMV +2.04% | Entire-Space 数据与模型协同扩展；NDCG@10 -2.20% |
| 核心机制 | `gatesid` · [GateSID](2603.22916-gatesid/README.md) | GMV +2.60% | 冷启动感知的语义/协同门控；NDCG@10 +34.95% |
| 核心机制 | `aigq` · [AIGQ](2603.19710-aigq/README.md) | GMV +10.68% | 混合 query 生成与 IL-GRPO；NDCG@10 +8.09% |
| 核心机制 | `safro` · [SaFRO](2603.19585-safro/README.md) | watch time +0.61% | 满意度感知的双重相对策略优化；NDCG@10 +81.86% |
| 核心机制 | `sort-ranking` · [SORT](2603.03988-sort-ranking/README.md) | orders +6.35% | 工业 Ranking Transformer 系统优化；NDCG@10 -13.11% |
| 核心机制 | `quasid` · [QuaSID](2603.00632-quasid/README.md) | GMV-S2 +2.38% | 资格感知的 SID 碰撞约束；NDCG@10 -0.55% |
| 核心机制 | `gpl-prerank` · [Generative Pseudo-Labeling](2602.20995-gpl-prerank/README.md) | CTR +3.07% | LLM 伪标签增强在线预排序；NDCG@10 +12.84% |
| 核心机制 | `ltv-video-ranking` · [Long-term Value Prediction](2602.17058-ltv-video-ranking/README.md) | VV +2.49% | 位置去偏与长期价值建模；NDCG@10 +9.73% |
| 核心机制 | `rgalign-rec` · [RGAlign-Rec](2602.12968-rgalign-rec/README.md) | CTR@3 incremental over QE-Rec +0.13% | 排序器指导的潜在 query 对齐；NDCG@10 -14.03% |
| 核心机制 | `linkedin-feed-sr` · [LinkedIn Feed SR](2602.12354-linkedin-feed-sr/README.md) | time spent +2.10% | 工业长序列 Feed 排序；NDCG@10 -0.12% |
| 核心机制 | `cadet` · [CADET](2602.11410-cadet/README.md) | CTR +11.04% | 候选后上下文条件化广告 CTR；NDCG@10 -6.20% |
| 核心机制 | `diffureason` · [DiffuReason](2602.09744-diffureason/README.md) | ad consumption +1.15% | 扩散式潜在推理与 GRPO；NDCG@10 -6.50% |
| 核心机制 | `sarm` · [SARM](2602.09401-sarm/README.md) | watch count +1.19% | MLLM 语义 anchor 增强直播排序；NDCG@10 +44.74% |
| 核心机制 | `ml-dcn` · [ML-DCN](2602.09194-ml-dcn/README.md) | platform-wide CTR +1.89% | Masked Low-Rank DCN 特征交叉；NDCG@10 -2.08% |
| 核心机制 | `rag-qac` · [RAG-QAC](2602.01023-rag-qac/README.md) | suggestions taken +3.46% | RAG 与多目标对齐的查询补全；NDCG@10 -4.48% |
| 核心机制 | `dynamic-codebook` · [Dynamic Codebook](2608.21012-dynamic-codebook/README.md) | 消费指标 +0.792%，解码 FLOPs 约 -48% | 动态码本与碰撞码；NDCG@10 -18.73%，保留负结果 |
| 核心机制 | `netflix-mediafm` · [Netflix MediaFM](2608.18322-netflix-mediafm/README.md) | Search playthrough +0.36% | 冻结多模态特征与查询打分；NDCG@10 -9.52% |
| 核心机制 | `ogr` · [OGR](2608.17613-ogr/README.md) | Effective Views +1.120% | 统一 SID、列表规划与保守对齐；NDCG@10 +13.25% |
| 核心机制 | `inthq` · [IntHQ](2608.09634-inthq/README.md) | UVCTR +1.60% | 分层任务查询；NDCG@10 -7.38% |
| 核心机制 | `pushdualgen` · [PushDualGen](2608.07989-pushdualgen/README.md) | 有效播放率 +8.50%、不满意率 -37.70% | SID→可选 copy；NDCG@10 +1.19% |
| 核心机制 | `recharness` · [RecHarness](2607.29241-recharness/README.md) | ADVV +2.084%、Revenue +0.534% | UCB 预算路由；NDCG@10 -9.02% |
| 核心机制 | `gala` · [GALA](2607.29213-gala/README.md) | 订单量 +0.55% | 多模态行为对齐门控；NDCG@10 -5.60% |
| 核心机制 | `feedback-policy` · [Feedback Policy](2607.27789-feedback-policy/README.md) | Revenue +4.506%、ADVV +4.621% | 反馈策略与保守增量；NDCG@10 +2.76% |
| 核心机制 | `real-estate-rerank` · [Real Estate Re-ranker](2607.14835-real-estate-rerank/README.md) | CTR +5.3%、预约看房 +4.8% | 文本/属性集合重排；NDCG@10 -8.21% |
| 核心机制 | `adaptive-ad-load` · [Adaptive Ad Load](2607.14418-adaptive-ad-load/README.md) | Revenue +36.8%、Conversion -1.1% | 受约束广告负载；NDCG@10 持平 |
| 核心机制 | `guess-where-you-go` · [Gwhere](2607.26073-guess-where-you-go/README.md) | P-CTR +5.83%、U-CTR +6.20% | 时空 SID 下一 POI；NDCG@10 +9.38% |
| 核心机制 | `genpage` · [GenPage](2606.31031-genpage/README.md) | 核心参与度 +0.24%、时延 -20% | 页面联合效用；NDCG@10 -3.98% |
| 核心机制 | `journeyformer` · [JourneyFormer](2606.19108-journeyformer/README.md) | Bookers +0.55%、Booked Nights +0.82% | 长短 journey 时间编码；NDCG@10 -2.77% |
| 核心机制 | `l2rec` · [L2Rec](2605.26717-l2rec/README.md) | CTR +9.24%、Reply Rate +3.15% | 双视图个性化适配；NDCG@10 -5.04% |
| 核心机制 | `qgs` · [QGS](2605.25514-qgs/README.md) | CTR +0.62%、PV Duration +3.55% | query-conditioned SID 打分；NDCG@10 +0.73% |
| 核心机制 | `tubifm` · [TubiFM](2605.23702-tubifm/README.md) | Search TVT +3.9%、Carousel TVT +0.30% | 统一三任务模型；NDCG@10 +0.45% |
| 核心机制 | `pearl-percentile` · [PEARL](2605.21752-pearl-percentile/README.md) | Watch Duration +2.10%、Report Rate -6.91% | 多样本 percentile；NDCG@10 -10.65% |
| 核心机制 | `dadf` · [DADF](2605.17863-dadf/README.md) | Time Spent +0.649%、生产 MAE -12.57% | 冻结基模乘性残差；NDCG@10 持平 |
| 核心机制 | `connectionmind` · [ConnectionMind](2608.10187-connectionmind/README.md) | Meta 数千万用户多周 A/B：曝光 +0.33%、观看时长 +0.43%、视频 session +0.22% | Delicious-2K 路径 SFT→GRPO→蒸馏混合推理；NDCG@10 -7.44%，保留负结果 |
| 核心机制 | `dream` · [DREAM](2608.09408-dream/README.md) | 淘宝精排+重排 IPV +2.71%、Core IPV +3.06%、GMV +1.31% | 意图→策略记忆→安全编译→双环门控；NDCG@10 +39.36%，但 head share +94.37% |
| 核心机制 | `gas` · [GAS](2608.12209-gas/README.md) | 纯多模态：from-scratch Overall 47.25→48.25；推理开销 0% | MoT + NEP + EMA；Fashion-MNIST QA 61.1%→63.5%，部署参数开销 0% |
| 核心机制 | `sona` · [Sona](2608.11015-sona/README.md) | Yandex Music Active Users +4.53%、时长 +6.30%、Likes +11.42% | history compression + SID decoder + ranker；NDCG@10 -92.05%，保留负迁移 |
| 核心机制 | `metastrategy` · [MetaStrategy](2608.09440-metastrategy/README.md) | 淘宝 click PV +2.11%、IPV +3.12%、交易金额 +2.83% | typed bundle + deterministic compiler；NDCG@10 -8.51%，head share -42.94% |
| 核心机制 | `crsd` · [CRSD](2510.11056-crsd/README.md) | 美团 AdCTR +0.91%、AdCVR +1.06%、GTV +0.40% | 两阶段 reasoning distillation；MovieLens-100K NDCG@10 -2.14%，保留负迁移 |
| 核心机制 | `twin-v2` · [TWIN-V2](2407.16357-twin-v2/README.md) | 快手三场景 Watch Time +0.672%/+0.800%/+0.728%，主流量 | 层级压缩 + GSU/ESU；NDCG@10 +22.45% |
| 核心机制 | `medusa` · [Medusa](2401.10774-medusa/README.md) | 纯 LLM：Medusa-1 2.2×，Medusa-2 2.3–3.6× | WikiText-2 三 future heads；backbone calls -50%，输出完全一致 |
| 核心机制 | `awq` · [AWQ](2306.00978-awq/README.md) | 纯 LLM：TinyChat 相对 FP16 超过 3× | activation-aware W4；输出 MSE -4.22% |
| 核心机制 | `smolvlm` · [SmolVLM](2504.05299-smolvlm/README.md) | 纯多模态：原文报告更低视觉 token 成本下保持竞争力 | pixel-shuffle 视觉 token 16→4；Fashion-MNIST QA +19.0 points |
| 核心机制 | `siglip2` · [SigLIP 2](2502.14786-siglip2/README.md) | 纯多模态：原文在多类图文 benchmark 改善语义与定位能力 | sigmoid 对比 + masked-view 自蒸馏；Fashion-MNIST QA +56.9 points |
| 核心机制 | `llava` · [LLaVA](2304.08485-llava/README.md) | 纯多模态：ScienceQA 92.53% | MLP projector 对线性 connector -3.4 points，保留小数据负结果 |
| 核心机制 | `blip2` · [BLIP-2](2301.12597-blip2/README.md) | 纯多模态：zero-shot VQAv2 相对 Flamingo-80B +8.7 points | 四 query Q-Former 将 token 16→4；accuracy -5.3 points，保留负结果 |
| 核心机制 | `speculative-decoding` · [Speculative Decoding](2211.17192-speculative-decoding/README.md) | 纯 LLM：T5-XXL 2–3× 且分布不变 | 低秩 draft + exact verification；target calls -75%，输出一致 |
| 核心机制 | `clip` · [CLIP](2103.00020-clip/README.md) | 纯多模态：ImageNet zero-shot 匹配监督 ResNet-50 | 双向对比学习；Fashion-MNIST 图文任务 72.0%，打乱图像 10.3% |
| 核心机制 | `sim` · [SIM](2006.05639-sim/README.md) | 阿里 CTR +7.1%、RPM +4.4%，主流量 | GSU/ESU 长历史检索；NDCG@10 +32.97% |
| 核心机制 | `dme` · [DME](2608.02148-dme/README.md) | 抖音搜索 Lifetime +0.1%，内部离线 +2.92% | typed latent + cross reconstruction；MovieLens-100K NDCG@10 -8.84%，保留负结果 |
| 核心机制 | `steps` · [STEPS](2608.01949-steps/README.md) | active days +0.2843%、permission disablement -1.9089%，已全量 | planning/execution/filter 闭环；MovieLens-100K NDCG@10 +66.05% |
| 核心机制 | `spear` · [SPEAR](2608.01738-spear/README.md) | query-view CTR +0.259、reading depth +0.733，已全量 | 双 embedding + 乘法门；MovieLens-100K NDCG@10 +26.95% |
| 核心机制 | `open-language-model` · [OpenLanguageModel](2607.16669-open-language-model/README.md) | 纯 LLM：四卡 weak scaling 90.6%；无线上 A/B | `olm_composable` genome；WikiText-2 同预算 PPL 基本等价，验证可组合结构语义 |
| 核心机制 | `gryphon-v2` · [Gryphon-v2](2608.06213-gryphon-v2/README.md) | Yandex Music active users +1.41% | rollout/impression 双路 teacher distillation；NDCG@10 -26.84%，保留负迁移 |
| 核心机制 | `degr` · [DEGR](2608.04809-degr/README.md) | 京东 UCTR +1.22%、PV +0.20% | diversity + adaptive reward ORPO；NDCG 持平、head share -1.21% |
| 核心机制 | `rd-attnres` · [RD-AttnRes](2608.01075-rd-attnres/README.md) | 纯 LLM：120M/343M PPL -2.97%/-2.43% | 相对 Block AttnRes PPL +0.61%（变差），QK/V route JS=0.00489 |
| 核心机制 | `retoken` · [ReToken](2607.28627-retoken/README.md) | Visual Haystacks：Qwen3-VL-8B +13.4 points；无线上 A/B | 单 retrieval target + value-cache Top-K；WikiText-2 PPL +3.70%（变差） |
| 核心机制 | `ccformer` · [CCFormer](2607.28070-ccformer/README.md) | 腾讯视频 CTR +3.57%、广告收入 +1.71%，实验后全流量 | 分字段 ID/content gate + 分层历史压缩；MovieLens-1M NDCG@10 +22.44%，token 24→12 |
| 核心机制 | `open-web-ufm` · [Open Web UFM](2607.28019-open-web-ufm/README.md) | Teads 50/50 A/B：CTR +2.13%、eCPC -1.13%、visit rate +2.37% | 双裁剪对比预训练 + next-item 代理任务；MovieLens-1M NDCG@10 +0.00%，如实保留零收益 |
| 核心机制 | `rocs` · [ROCS](2607.27744-rocs/README.md) | Meta 检索最高 3× QPS；短视频排序 LogLoss -0.5%、QPS +50% | request-once / candidate-late interaction；MovieLens-1M NDCG@10 +8.19%，进程内候选打分 129.58× |
| 核心机制 | `wide` · [WIDE](2607.28418-wide/README.md) | 纯 LLM：50% sparsity 下 kernel prefill 1.98×、decode 4.95× | token 级 head/FFN group Top-K；WikiText-2 PPL +0.81%（变差），dense PyTorch 未获得 kernel 加速 |
| 核心机制 | `asarl` · [ASARL](2607.26593-asarl/README.md) | QQ 频道 CTR +2.69%、群 GSB +16.66%，1200 万 DAU | Reason/Critic/Gen + SCT/PGO/SD；NDCG@10 -72.72%，保留代理负迁移 |
| 核心机制 | `oxygenrec-v2` · [OxygenREC-v2](2607.24255-oxygenrec-v2/README.md) | 京东 UCTCVR +1.61%–+4.44%，首页 GMV +21.21% | 行为指令 + privileged distillation；NDCG@10 -54.09%，保留代理负迁移 |
| 核心机制 | `reco-reward` · [RecoReward](2607.25901-reco-reward/README.md) | 快手有效用户渗透 +0.265%、外流曝光 +0.791% | RAS target/non-target reward；Hit@10 -16.00%，保留负结果 |
| 核心机制 | `twice` · [TWICE](2607.25404-twice/README.md) | expected revenue +2.486%、conversion +2.061%，已全流量 | 双时钟与 delay CDF；NDCG@10 +14.31% |
| 核心机制 | `swag-bid` · [SWAG](2607.25233-swag-bid/README.md) | GMV +3.42%、ROAS +5.65% | 滑窗 masked planner；NDCG@10 +0.00% |
| 核心机制 | `youtube-freshness` · [YouTube Freshness](2607.23749-youtube-freshness/README.md) | 1-day new-release engagement +4.33% | IPS + bias tower + uncertainty；head share -28.72% |
| 核心机制 | `melo` · [Melo](2607.23718-melo/README.md) | 系统级 A/B retention >2pp | grounding + retry；fresh Hit@10 +50.00%，系统归因单列 |
| 核心机制 | `penelope` · [Penelope](2607.25915-penelope/README.md) | 纯 LLM：结构化推理 accuracy/compute 改善 | 两步 localized recurrence；composite loss -0.63% |
| 核心机制 | `mim` · [MIM](2502.00321-mim/README.md) | 淘宝 CTR +14.14%、RPM +4.12% | 遮盖多模态对齐 + CiUBM；NDCG@10 +0.94%，Hit@10 下降 |
| 核心机制 | `filterllm` · [FilterLLM](2502.16924-filterllm/README.md) | Cold-PV +5.13%、GMV +10.86% | text-to-user-distribution；NDCG@10 -9.82%，保留负结果 |
| 核心机制 | `fuxi-alpha` · [FuXi-α](2502.03036-fuxi-alpha/README.md) | 播放歌曲 +4.67%、时长 +5.10% | 三通道交互；Hit@10 略升、NDCG@10 -4.25% |
| 核心机制 | `recgpt-v2` · [RecGPT-V2](2512.14503-recgpt-v2/README.md) | 淘宝 CTR +2.98%、IPV +3.71%、NER +11.46% | 层级 agents + 约束路由；NDCG@10 +18.52% |
| 核心机制 | `higr` · [HiGR](2512.24787-higr/README.md) | 腾讯播放量 +1.73%、观看时长 +1.22% | 层级 SID slate + ORPO；NDCG@10 -12.32% |
| 核心机制 | `drl-put` · [DRL-PUT](2509.05292-drl-put/README.md) | Pinterest 收入 +0.27%、CTR +1.62% | logged bandit 策略调权；NDCG@10 +19.13% |
| 核心机制 | `adaf2m2` · [AdaF²M²](2501.15816-adaf2m2/README.md) | 抖音活跃天数 +1.37%、时长 +1.89% | feature-mask multi-forward + adapter；NDCG@10 +2.42% |
| 核心机制 | `mgoe` · [MGOE](2506.10520-mgoe/README.md) | 阿里 GMV +16.46%、CVR +5.88% | macro task graph experts；NDCG@10 +7.03% |
| 核心机制 | `click-a-buy-b` · [Click A Buy B](2507.15113-click-a-buy-b/README.md) | Pinterest 主业务指标 +0.25% | CABA/CABB + taxonomy；NDCG@10 +33.70% |
| 核心机制 | `mosaic` · [Mosaic](2607.24015-mosaic/README.md) | Meta 三个 surface +0.10%/+0.15%/+0.28% | 四 specialist + MRM + CRL；NDCG@10 +3.49%，Hit@10 -7.69% |
| 核心机制 | `unir2` · [UniR²](2607.24439-unir2/README.md) | 快手播放量 +1.177%、点赞率 +2.560%；极速版送礼金额 +2.569% | DQ-PCA + ranking LoRA；SID code accuracy +34.04%，NDCG@10 -13.19% |
| 核心机制 | `core-relevance` · [CORE](2607.24417-core-relevance/README.md) | 美团 NDCG@5 +0.20%、Badcase@5 -15.9% | 级联头 + step-GRPO + PostCoT；NDCG@5 +0.98%、Badcase@5 -50.00%，accuracy -0.52 points |
| 核心机制 | `data-orchestra` · [DataOrchestra](2607.24717-data-orchestra/README.md) | 纯 LLM：0.5B/1.5B/7B benchmark average 稳定提升 | 逐样本路由；PPL 较固定清洗 -1.03%，较 raw +8.60%（变差） |
| 核心机制 | `native-sparse-attention` · [NSA](2502.11089-native-sparse-attention/README.md) | 纯 LLM：质量不低于 full attention，64K 三阶段显著加速 | 三路稀疏注意力；attention edge -43.65%，PPL -3.17% |
| 核心机制 | `gated-attention` · [Gated Attention](2505.06708-gated-attention/README.md) | 纯 LLM：改善 scaling、稳定性与长上下文外推 | post-SDPA 逐头 gate；PPL -0.72% |
| 核心机制 | `muon` · [Muon](2502.16982-muon/README.md) | 纯 LLM：约 2× compute efficiency | 正交矩阵更新已执行；PPL +5.61%（变差） |
| 核心机制 | `wide-deep` · [Wide & Deep](1606.07792-wide-deep/README.md) | Google Play acquisition +3.9% | wide crosses + deep tower；NDCG@10 +5.45% |
| 核心机制 | `deepfm` · [DeepFM](1703.04247-deepfm/README.md) | 用户批准的经典例外 | FM + deep 共享 embedding；NDCG@10 +23.58% |
| 核心机制 | `youtube-dnn` · [YouTube DNN](recsys2016-youtube-dnn-youtube-dnn/README.md) | 用户批准的经典例外；未披露量化 lift | 非线性用户塔；NDCG@10 -6.61%，保留负结果 |
| 核心机制 | `esmm` · [ESMM](1804.07931-esmm/README.md) | 用户批准的经典例外 | entire-space CTR×CVR；平均 AUC +1.69% |
| 核心机制 | `mmoe` · [MMoE](kdd2018-mmoe-mmoe/README.md) | 用户批准的经典例外 | 共享 experts + 任务 gates；平均 AUC +1.30% |
| 核心机制 | `ple` · [PLE](recsys2020-ple-ple/README.md) | 用户批准的经典例外 | 共享/专属 experts；平均 AUC +1.34% |
| 核心机制 | `dcn-v2` · [DCN-V2](2008.13535-dcn-v2/README.md) | 经典例外：线上显著但未披露 lift | low-rank cross experts；NDCG@10 +22.87% |
| 核心机制 | `dien` · [DIEN](1809.03672-dien/README.md) | CTR +20.7%、eCPM +17.1% | GRU + auxiliary + interest evolution；NDCG@10 -1.98% |
| 核心机制 | `bst` · [BST](1905.06874-bst/README.md) | CTR +7.57% | target-token Transformer；NDCG@10 +20.29% |
| 核心机制 | `cs3` · [CS3](2604.19269-cs3/README.md) | Revenue +8.356%/+1.366%/+2.177% | cycle/sync/cascade；NDCG@10 -16.06% |
| 核心机制 | `cq-sid` · [CQ-SID](2605.14434-cq-sid/README.md) | GMV +1.15%、UCTCVR +0.40% | category SID + EG-GRPO；NDCG@10 +1.66% |
| 核心机制 | `switch-transformer` · [Switch Transformer](2101.03961-switch-transformer/README.md) | 纯 LLM：预训练约 7× 加速 | top-1 MoE；30-step PPL -3.29% |
| 核心机制 | `mamba` · [Mamba](2312.00752-mamba/README.md) | 纯 LLM：推理最高约 5× | selective scan；30-step PPL +48.82%（变差） |
| 核心机制 | `switch-attention` · [Switch Attention](2603.26380-switch-attention/README.md) | 纯 LLM：32K decode >4× | dynamic full/local router；30-step PPL +0.19%（略差） |
| 核心机制 | `onemall` · [OneMall](2601.21770-onemall/README.md) | 商品卡 GMV +13.01%、短视频订单 +15.32%、直播订单 +2.78% | 场景 prompt + SID + 跨行为融合；NDCG@10 +4.33% |
| 核心机制 | `dos` · [DOS](2602.04460-dos/README.md) | 美团收入 +1.15% | 双流 ORQ；NDCG@10 +11.26% |
| 核心机制 | `mdl` · [MDL](2602.07520-mdl/README.md) | 抖音 LT30 +0.0626%、rewrite -0.3267% | 三类 token 与 domain attention；NDCG@10 +13.34%，head share +73.43% |
| 核心机制 | `hisac` · [HiSAC](2602.21009-hisac/README.md) | 淘宝 CTR +1.65% | 层级 interest agents；NDCG@10 +1.31% |
| 核心机制 | `pinclip` · [PinCLIP](2603.03544-pinclip/README.md) | fresh Repin +15%、new Ads click +8.7% | 邻居对齐 NDCG@10 -1.41%，未迁移收益 |
| 核心机制 | `pin-scale` · [Pin-SCALE](sigir2026-pin-scale-pin-scale/README.md) | Repin +3.67%、DAU +0.05% | engagement-aware SID；NDCG@10 +13.61%、fresh Hit +50.00% |
| 核心机制 | `causal-retrieval` · [Causal Retrieval](2607.14161-causal-retrieval/README.md) | trigger -85%、session +0.26%、Save +1.10% | DR uplift trigger；合成 treatment NDCG@10 +80.77% |
| 核心机制 | `podcast-mtl` · [Podcast MTL](2601.02306-podcast-mtl/README.md) | eCPS -22%、stream +18%–24% | shared MTL NDCG@10 -20.63%，出现 negative transfer |
| 核心机制 | `engram` · [Engram](2601.07372-engram/README.md) | 纯 LLM：MMLU +3.4、BBH +5.0、HumanEval +3.0 | O(1) memory 已接 evolve；30-step PPL +50.12%（变差） |
| 核心机制 | `looped-latent-attention` · [Looped Latent Attention](2607.15456-looped-latent-attention/README.md) | 纯 LLM：KV 最多 32× 压缩 | 已接 evolve；参数 -42.28%，PPL +5.56% |
| 核心机制 | `gaugequant` · [GaugeQuant](2607.20757-gaugequant/README.md) | 纯 LLM：LLaMA-2 7B W4A4 PPL 8.22→6.73 | 已接 evolve；本地 W4A4 STE PPL -1.56% |
| 核心机制 | `nova` · [NOVA](2606.27243-nova/README.md) | 腾讯三个 pCVR 目标 GMV +1.25%/+1.70%/+2.02% | 四级 verification cascade、失败方向和 architecture gradient 实际接入 evolve |
| 核心机制 | `evorec` · [EvoRec](2606.28368-evorec/README.md) | Revenue +1.85%、CTR +1.02% | 三代模型/方法双轨进化与持久 skill memory |
| 完整核心链路 | `tokenmixer-large` · [TokenMixer-Large](2602.06563-tokenmixer-large/README.md) | Orders +1.66%、payment GMV +2.98% | mixing/reverting、双 SwiGLU、interval residual 和辅助损失实际训练 |
| 核心机制 | `msn` · [MSN](2602.07526-msn/README.md) | Watch time +0.2958%、finish +0.2071% | Product-Key Memory、top-k sparse read 与 gate |
| 核心机制 | `idproxy` · [IDProxy](2603.01590-idproxy/README.md) | 内容互动 +0.50%、广告 ADVV +1.93% | 对比损失 6.073→5.358；NDCG@10 +5.32% |
| 核心机制 | `glide` · [GLIDE](2603.17540-glide/README.md) | Non-habitual streaming +5.4%、new-show discovery +14.3% | residual Semantic ID 生成与长短期双 prompt |
| 核心机制 | `genrec` · [GenRec](2604.14878-genrec/README.md) | Clicks +9.5%、transactions +8.7% | page-wise NTP、Token Merger 与 GRPO-SR/NLL |
| 核心机制 | `genrec-netflix` · [Netflix GenRec](2608.10257-genrec-netflix/README.md) | 10% 流量 4 周；短期首页参与 +0.115%、长期核心指标 +0.006% | SmolLM2 LoRA + catalog head + reward weighting；NDCG@10 +35.07%（单 seed） |
| 核心机制 | `rankgraph2` · [RankGraph-2](2606.18379-rankgraph2/README.md) | CTR +0.96%、CVR +2.75% | 去偏边、多跳 PPR 与两级 residual index；NDCG@10 +109.65% |
| 核心机制 | `solaris` · [SOLARIS](2604.12110-solaris/README.md) | 全流量 top-line revenue +0.67% | future-pair predictor、异步 latent cache 与 fallback |
| 核心机制 | `minimax-sparse-attention` · [MiniMax Sparse Attention](2606.13392-minimax-sparse-attention/README.md) | 纯 LLM：1M context attention compute -28.4× | attention pairs -79.95%，PPL +0.41%（变差），未融合 MPS 耗时 +67.58% |
| 核心机制 | `pinequalizer` · [PinEqualizer](2607.22518-pinequalizer/README.md) | Related Pins ranking architecture：all-fresh +8.63%、underexplored +6.57% | MovieLens-1M fresh NDCG +448.62%、underexplored exposure +471.02%，但整体 NDCG -16.44% |
| 核心机制 | `gzip-sparse-attention` · [Gzip-guided Sparse Attention](2607.21752-gzip-sparse-attention/README.md) | 纯 LLM：PG-19 BPB 2.34→1.71（对 BigBird） | 同参数 256-context BPB 较 BigBird +1.02%（变差），attention edges -70.82% |
| 核心机制 | `windowed-mtp` · [Windowed-MTP](2607.21535-windowed-mtp/README.md) | 纯 LLM serving：1M step latency +28.3%–+44.3% | 16K KV read -99.56%、MPS draft latency -50.25%；输出完全一致，acceptance 41.67%→25.00% |
| 核心机制 | `adadsf` · [AdaDSF](2607.21291-adadsf/README.md) | 纯 LLM：80% retention PPL 21.6→18.9（对 MoD） | 同 teacher/budget 下 PPL 较 Uniform MoD +0.30%（变差） |
| 核心机制 | `barge` · [BARGE](2607.21028-barge/README.md) | 腾讯 CTR +0.60%、点击 UV +1.34%、阅读时长 +1.70% | OSQ+ICA+HPR+DPD；NDCG@10 +85.77%，但 head share +165.02% |
| 核心机制 | `mobius-rope` · [Möbius RoPE](2607.21405-mobius-rope/README.md) | 纯 LLM：needle 63.3%→90.3%，PPL 持平 | PPL -0.03%，单 seed needle -2.08 points，未迁移论文收益 |
| 核心机制 | `naju` · [Naju](2607.21000-naju/README.md) | 纯 LLM：WikiText-103 PPL 28.31→26.20 | preserve-first gates 正确；WikiText-2 PPL +25.67%（变差） |
| 核心机制 | `dynamic-rubric` · [DynamicRubric](2607.20083-dynamic-rubric/README.md) | 微信搜索全 AI 流量统计显著；具体 lift 未披露 | Alpaca preference accuracy 83.89%→87.78%，相对 +4.64% |
| 核心机制 | `tsgr` · [TSGR](2607.18796-tsgr/README.md) | 淘宝 IPV +0.43%、成交 +1.12%、GMV +1.64% | 并行价值 SID + 联合 VRM；NDCG@10 +115.73% |
| 核心机制 | `off-context-grpo` · [Off-Context GRPO](2607.19313-off-context-grpo/README.md) | 纯 LLM：Qwen2.5-7B 相对 GRPO +13.8% | 官方 GSM8K Pass@1 2.67%→3.33%，相对 +25.00% |
| 核心机制 | `ramp` · [RAMP](2607.17473-ramp/README.md) | 工业 CVR Total Advertiser Value >+3% | 受限个性化字段流量 NDCG@10 +417.23% |
| 核心机制 | `whale` · [WHALE](2607.17017-whale/README.md) | Meta 主指标 +0.113%、Metric 1 +0.824% | Wukong-HSTU 渐进交换；NDCG@10 -83.20%，未迁移收益 |
| 核心机制 | `tmallgs` · [TMallGS](2607.13398-tmallgs/README.md) | 天猫 UCTCVR +1.38%、GMV +1.52% | Field-adaptive gated Transformer；NDCG@10 +310.42% |
| 核心机制 | `long-history-transformer` · [Long-History User Transformers](2607.14331-long-history-transformer/README.md) | Yandex Search 主指标 +2.77%、Revenue +2.26% | 缓存全历史 + 在线近期 encoder；NDCG@10 +57.08% |
| 核心机制 | `downstream-rewards` · [Downstream Rewards](2607.14192-downstream-rewards/README.md) | 多 surface +0.11%–+0.36% | 筛选长期 reward head；NDCG@10 -5.10%，未迁移收益 |
| 核心机制 | `recgpt-mobile` · [RecGPT-Mobile](2605.04726-recgpt-mobile/README.md) | 淘宝 CLICK +1.8%、PAY +2.7%、GMV +2.5% | 真实 135M LoRA semantic intent accuracy +100.00%；INT8 相对 -6.25%、体积 -53.68%，触发器跳过 96.21% 推理 |
| 核心机制 | `sort-gen` · [SORT-Gen](2505.07197-sort-gen/README.md) | 相对部署基线 CLICK +4.13%、GMV +8.10% | ordered regression + 单次 mask-driven queue generation；Click +5.10%、Pay +8.46%、GMV proxy +9.00%、ILAD +2.89% |
| 核心机制 | `recgpt-v3` · [RecGPT-V3](2607.15591-recgpt-v3/README.md) | 淘宝 Feed IPV +1.28%、CTR +1.00%、GMV +3.97%；资源 -52.4% | 两阶段教师蒸馏后 NDCG@10 +36.96%，memory token -65%、latent slots -90%，但 head share +71.43% |
| 核心机制 | `slimper` · [SlimPer](2607.12281-slimper/README.md) | Instagram Reels/Feed 统计显著全流量提升；具体 lift 未披露 | 参数匹配下 NDCG@10 +1.29%，attention-score elements -94.12% |
| 核心机制 | `tokenminds` · [TokenMinds](2606.25147-tokenminds/README.md) | YouTube SFV Engaged Users +0.11%、Satisfied Engagement +0.62%，多 surface 全流量 | dense + SID user token 双输出实际训练；单 seed NDCG@10 -0.35%，不宣称稳定提升 |
| 核心机制 | `recap` · [RECAP](2607.15730-recap/README.md) | 快手人均应用使用时长 +0.139% | GRPO reward 0.5245→0.7096，但 NDCG@10 -6.77%、head share -20.27% |
| 核心机制 | `uame` · [UAME](2607.17092-uame/README.md) | LongView 最高 +1.614%、Forward 最高 +1.598% | 三路公开 proxy 下 NDCG@10 -62.28%，未迁移线上收益 |
| 核心机制 | `conv-llm` · [Convolution for LLMs](2607.18413-conv-llm/README.md) | 纯 LLM：Qwen3-1.7B PPL 13.42→12.79 | 同预算 WikiText-2 test PPL 305.664→304.787（-0.29%） |
| 核心机制 | `ppl-factory` · [PPL-Factory](2607.18199-ppl-factory/README.md) | 纯 LLM：10% 数据时 GSM8K +0.9、MATH +4.8 points | 20% middle selection PPL 较随机变差 1.79%，easy 最好 |
| 核心机制 | `fluid` · [FLUID](2605.21832-fluid/README.md) | QWD +0.55%、冷启房间播放 +2.05% | 去候选 ID 后 NDCG -20.63%，fresh Hit +100.00%、head share -58.32% |
| 核心机制 | `memory-grafting` · [Memory Grafting](2605.20948-memory-grafting/README.md) | 纯 LLM：benchmark average 53.86 | PPL 较 Transformer -3.59%，但较 Engram +0.03%，未超过直接可训练记忆 |
| 核心机制 | `mhc` · [mHC](2512.24880-mhc/README.md) | 纯 LLM：benchmark +2.1%–2.3% | PPL 未提升；残差行列误差归零、谱范数 1.089→1.000 |
| 核心机制 | `degre` · [DeGRe](2605.25749-degre/README.md) | Taobao Flash CTR +2.85%、GMV +3.75% | evaluator→beam→dense distillation；NDCG@10 +3.31% |
| 核心机制 | `harness-lm` · [HARNESS-LM](2605.23572-harness-lm/README.md) | Bing Ads Revenue +1.0%、Clicks +0.4% | 三阶段收敛但 test NDCG -28.05% |
| 核心机制 | `grc` · [GRC](2602.23639-grc/README.md) | Revenue +1.79%、CTR +2.11%、GMV +2.04% | structured SFT→GRPO→EGRS；NDCG -11.12% |
| 核心机制 | `mbgr` · [MBGR](2604.02684-mbgr/README.md) | Meituan CTCVR +3.98% | BID/MBP/LDR；NDCG -5.92% |
| 核心机制 | `growthgr` · [GrowthGR](2605.17994-growthgr/README.md) | 新品 GMV +5.3%、全站 GMV +0.3% | ItemLTV→SID→MoPO；NDCG +2.05% |
| 核心机制 | `mesh` · [MESH](2607.12392-mesh/README.md) | fresh repins +5.5%、retention +0.46% | 三塔与 RGBC；NDCG -3.54% |
| 核心机制 | `sam` · [SAM](2607.12714-sam/README.md) | CTR +1.1%、GMV +0.9%、bad-case -74.5% | ASGU/TTNP；NDCG -6.60% |
| 核心机制 | `danet` · [DANet](2607.12578-danet/README.md) | pCVR +3.63%、GMV +2.23% | TFTM/DCM；NDCG -1.46%、fresh Hit +50.00% |
| 核心机制 | `proximity-features` · [Proximity Features](2607.12246-proximity-features/README.md) | first-time bookers +2.0%、booking +0.16% | ZIP adaptive buckets；Hit@10 +16.67%、NDCG +22.91% |
| 核心机制 | `nontp` · [NONTP](2607.12277-nontp/README.md) | Meituan DSP CTR +1.8%、GMV +2.1% | EMA teacher TCL、跨域 TDL 与零额外推理路径实际执行；Hit@10 -4.93%、NDCG -8.62% |
| 核心机制 | `akt-rec` · [AKT-Rec](2605.23310-akt-rec/README.md) | Tmall CTR +2.76%、GMV +3.47% | 真实小型 LLM、RQ-VAE 与非对称迁移实际执行；AUC +3.44%、GAUC +5.53%、tail AUC +2.15% |
| 完整核心链路 | `s-grec` · [S-GRec](2602.10606-s-grec/README.md) | WeChat GMV +1.19%、CTR +1.16%、dislike -2.02% | 真实 LLM PSJ + SID generator + 5% A2PO；A2PO 经 validation 晋级，test HR@10 +0%、NDCG -4.53%，约束零越界 |
| 完整核心链路 | `pinterest-ads-llm` · [Complementary LLM Predictor](2605.27856-pinterest-ads-llm/README.md) | US Shopping RoAS +4.94%、opt-in +6.69% | SFT 被选中；GRPO Recall@20 +0%，LLM 排序特征 AUC +2.59%，召回 quota=0 |
| 完整核心链路 | `lwgr` · [LWGR](2605.18771-lwgr/README.md) | Ads revenue +1.35%、CTR +1.17% | reference 被选中；LWGR Recall@10 +0%、NDCG -4.29%，dual update 执行但约束未改善 |
| 完整核心链路 | `sigma` · [SIGMA](2602.22913-sigma/README.md) | AliExpress Order +2.80%、GMV +7.84% | top1-prefix HR@20 1/128→9/128；APF 相对 top1 -11.11% |
| 完整核心链路 | `univa` · [UniVA](2605.05803-univa/README.md) | WeChat Channels GMV +1.50%、GMV(normal) +1.42% | Office 公开代理；HR@100 +4.76%、ValueHR +6.56%，但 wNDCG -8.43%；trie 有效路径 50/50 |
| 核心机制 | `prompt-generation` · [Prompt Generation](2607.11326-prompt-generation/README.md) | Taobao Search transaction +0.47%、GMV +0.51%；Shop Search +4.01% | 同源 Amazon Office + Qwen2.5-0.5B；选中 Title 的 HR@10 -11.11%，mean merger 较原始 Title 打分 -90.38% |
| 完整核心链路 | `precise` · [PRECISE](2412.06308-precise/README.md) | WeChat ranking Clicks +1.961%、Shares +1.433% | SmolLM token + MoE + UT/TT；Recall@10 +40.0%，Cold Recall -50.0% |
| 完整核心链路 | `lum` · [LUM](2502.08309-lum/README.md) | Taobao CTR +2.9%、RPM +1.2% | next-condition-item + group query + DLRM；AUC +14.60%，3/3 seeds 正向 |
| 完整核心链路 | `lsvcr` · [LSVCR](2403.13574-lsvcr/README.md) | Kuaishou comment watch time +4.1264% | q/v-LoRA + SSC/VCC；comment NDCG +50.40%，item NDCG -56.42% |
| 完整核心链路 | `msd` · [MSD](2412.06860-msd/README.md) | Meituan CTR +2.12%、CPM +2.59% | teacher→T5 distill + LoRA/cache fusion；AUC +1.55%，2/3 seeds 正向 |
| 核心机制 | `sessionrec` · [SessionRec](2502.10157-sessionrec/README.md) | Meituan Pay PV +0.603%、PVCTCVR +0.564% | KuaiRand 真实 session、曝光负例；NDCG@20 -22.05%，仅 1/3 seeds 正向 |
| 核心机制 | `saviorrec` · [SaviorRec](2508.01375-saviorrec/README.md) | Taobao Clicks +13.31%、Orders +13.44%、CTR +12.80% | 行为 encoder + RQ-SID + MBA + BiTargetAttn；cold AUC 均值 +6.92%，仅 1/3 seeds 正向 |
| 完整核心链路 | `pinrec` · [PinRec](2504.10507-pinrec/README.md) | Grid Clicks +4.01%、Time Spent +0.55% | OC + unordered MT 实际训练；Recall@10 -27.78% |
| 完整核心链路 | `genrank` · [GenRank](2505.04180-genrank/README.md) | Engagements +1.2474% | action-oriented 延迟 -25.66%，AUC -0.46% |
| 完整核心链路 | `learn` · [LEARN](2405.03988-learn/README.md) | cold-item Revenue +8.77% | NDCG +233.10%，但 head share 69.50% |
| 完整核心链路 | `notellm` · [NoteLLM](2403.01744-notellm/README.md) | I2I CTR +16.20% | GCL+CSFT；NDCG +7.15%，3/3 seeds 正向 |
| 完整核心链路 | `kar` · [KAR](2306.10933-kar/README.md) | Huawei 新闻 Recall +7%；音乐播放量 +1.70% | 真实 LLM 知识生成与 hybrid experts；AUC 均值 +0.81%，2/3 seeds 正向 |
| 完整核心链路 | `bahe` · [BAHE](2403.19347-bahe/README.md) | Ads CTR +9.65%、CPM +2.41% | 原子行为缓存 + 上层聚合；耗时 -53.61%，AUC -2.94% |
| 完整核心链路 | `beque` · [BEQUE](2311.03758-beque/README.md) | Taobao GMV +0.40%、交易数 +0.34% | SFT + 无泄漏自采样 + 离线反馈 + PRO；feedback +30.03%，increment -66.02% |
| 完整核心链路 | `onerec-v2` · [OneRec-V2](2508.20900-onerec-v2/README.md) | Kuaishou stay +0.467%、Lite +0.741% | KuaiRand 真实时长反馈；Lazy latency -54.78%，GBPO 均值 +21.66% 但仅 2/3 seeds 正向 |
| 完整核心链路 | `plum` · [PLUM](2510.07784-plum/README.md) | YouTube Panel CTR +0.76%/+4.96% | CPT 降低 loss；Recall@10 R1/CR1 0.5%，R2/CR2 0，未验证召回增益 |
| 完整核心链路 | `onerec` · [OneRec](2502.18965-onerec/README.md) | Kuaishou watch time +1.68% | 核心链路均执行；DPO 将本地 NDCG@10 从 0.0157 降至 0 |
| 完整核心链路 | `g2rec` · [G2Rec](2606.20554-g2rec/README.md) | Meta +0.06%–+0.19% | Beauty 上 soft graph + generative dual-loss；NDCG@10 +11.92% |
| 完整核心链路 | `mixformer` · [MixFormer](2602.14110-mixformer/README.md) | Douyin duration +0.2799% | matched-budget trainable blocks；NDCG@10 +17.41% |
| 完整核心链路 | `rankmixer` · [RankMixer](2507.15551-rankmixer/README.md) | Active Days +0.3%、duration +1.08% | dense per-token FFN 最优；sparse MoE 未追平 dense |
| 完整核心链路 | `hyformer` · [HyFormer](2601.12681-hyformer/README.md) | watch time +0.293%、finish +1.111% | NDCG@10 +143.77%，head share 同步上升 |
| 完整核心链路 | `onetrans` · [OneTrans](2510.26104-onetrans/README.md) | Feeds GMV/U +5.6848% | NDCG@10 +123.58%，但 92% 推荐落在头部 |
| 完整核心链路 | `rec-distill` · [Rec-Distill](2605.29755-rec-distill/README.md) | Ads ADVV +1.00%、Rec Finish/U +1.2725% | α 搜索后 transferability -4.11%，未验证蒸馏收益 |
| 完整核心链路 | `sasrec` · [SASRec](1808.09781-sasrec/README.md) | 无；用户指定经典基线例外 | 原论文 BCE 与全库推理；NDCG@10 0.02933，较 popularity -1.24% |
| 核心机制 | `hstu` · [HSTU](2402.17152-hstu/README.md) | Meta engagement +12.4%、consumption +4.4% | matched sampled-softmax SASRec 对照；NDCG@10 -17.73% |
| 核心机制 | `m6rec` · [M6-Rec](2205.08084-m6rec/README.md) | Alipay mini-app CTR >+1.0% | 冻结真实预训练 LM；option-adapter AUC 均值 +0.12% ± 0.41% |
| 核心机制 | `din` · [DIN](1706.06978-din/README.md) | Alibaba CTR +10.0%、RPM +3.8% | local activation 与 Dice 实际训练；较 mean pool NDCG@10 -6.97% |
| 核心机制 | `tiger` · [TIGER](2305.05065-tiger/README.md) | 无；用户指定经典论文例外 | RQ-VAE 与自回归检索实际训练；较等容量 random ID NDCG@10 -39.16% |
| 核心机制 | `transact-v2` · [TransAct V2](2506.02267-transact-v2/README.md) | Pinterest Repin +6.35%、Hide -12.80%、Time Spent +1.41% | NDCG@10 +92.65%，但 head share 升至 98.99% |
| 核心机制 | `pinfm` · [PinFM](2507.12704-pinfm/README.md) | Pinterest Homefeed Saves +1.20%–+5.70% | 两轮预训练/微调按 validation 选型；test -3.57%，head share 降至 20.16% |
| 核心机制 | `sis` · [SIS](2607.04728-sis/README.md) | 非本轮 A/B 集合 | SIS 公式实际执行；未训练 Qwen3/GRPO |
| 核心机制 | `mdcns` · [MDCNS](2605.19651-mdcns/README.md) | 论文公开离线结果 | 作者 Beauty 切分；三源采样与双模型更新实际执行 |
| 核心机制 | `memento` · [Memento](2605.24051-memento/README.md) | Meta CTR +1.0%、CVR +1.2% | query-conditioned MMR 实际执行；生产 replay/serving 省略 |
| 核心机制 | `llm-ad-retrieval` · [LLM Retrieval](2605.21969-llm-ad-retrieval/README.md) | Meta top-line +0.45%、final recall +1.2% | domain SFT + LLM attribute graph；Recall@20 +11.90%，score drift -77.36% |
| 完整核心链路 | `seral` · [SERAL](2502.13539-seral/README.md) | Taobao clicks +29.56%、transactions +27.6% | 相对 DIN NDCG +50.60%；novelty 未提升 |
| 完整核心链路 | `leadre` · [LEADRE](2411.13789-leadre/README.md) | WeChat GMV +1.57%/+1.17% | 相对 DIN +12.94%；DPO 消融 -4.53% |
| 完整核心链路 | `cobra` · [COBRA](2503.02453-cobra/README.md) | Conversion +3.60%、ARPU +4.15% | 相对 DIN +25.75%；热门集中上升 |
| 核心机制 | `argus` · [ARGUS](2507.15994-argus/README.md) | Listening +2.26%、likes +6.37% | 相对 DIN -4.12%，未验证收益 |
| 核心机制 | `gr4ad` · [GR4AD](2602.22732-gr4ad/README.md) | Kuaishou ad revenue +4.2% | 相对 DIN +69.67%，head share 0.505 |
| 核心机制 | `cross-domain-kd` · [Cross-domain KD](2603.28994-cross-domain-kd/README.md) | Music discovery +1.12% | target split 相对 DIN -68.46% |
| 核心机制 | `mm-llm` · [MM-LLM](2605.09338-mm-llm/README.md) | Meta engagement +0.02% | 相对 DIN -13.23%，未验证收益 |
| 核心机制 | `cluster-goobs` · [Cluster GOOBS](2607.00448-cluster-goobs/README.md) | Meta CTR +53% | online sampler 实际执行；genre 替换私有 LLM cluster |
| 核心机制 | `llatte` · [LLaTTE](2601.20083-llatte/README.md) | Meta conversion +4.3% | BERT semantic features、MLA、target-aware online attention 与 DHEN 均实际训练 |
| 核心机制 | `self-evolving-rec` · [Self-Evolving RecSys](2602.10226-self-evolving-rec/README.md) | Google +0.03%–+0.14% | 本地指令 LLM 读取 journal、逐轮提案、validation 反馈与隔离 test |
| 核心机制 | `cmsl` · [CMSL](2606.28533-cmsl/README.md) | Meta +0.092%–+0.171% | learned contextual lenses 与 HSTU-style backbone 实际训练 |
| 核心机制 | `longer` · [LONGER](2505.04421-longer/README.md) | Douyin Ads/电商 A/B | InnerTrans、global token 与 hybrid attention 端到端训练 |

## 统一运行方式

```bash
# 单篇
auto-research reproduce --paper <adapter> --seed 42

# 全部
auto-research reproduce --paper all --seed 42

# 包含明确降级的概念验证
auto-research reproduce --paper all --include-concept-demos --seed 42
```

原始运行产物位于：

```text
runs/reproductions/<arxiv-id>-<adapter>/<timestamp>/
├── report.md
└── result.json
```

`runs/` 不进入 Git；`result.json` 是单次运行的事实来源。复核后的稳定结论、实验协议和边界条件才会摘录到对应论文 README。

## Adapter 目录约定

```text
src/auto_research/reproductions/<adapter>/
├── adapter.py
├── model.py 或 algorithm.py
├── experiment.py
└── report.py
```

共享的公开数据切分、逐用户及矩阵化全库指标位于 `reproductions/rec_utils.py`，序列模型的 all-position 训练位于 `reproductions/sequence_training.py`，下载器位于 `datasets.py`。论文特有网络、采样、调参和报告逻辑保留在论文目录中。每篇 README 固定包含完整论文信息、原论文背景、主要改动、Mermaid 架构图、核心公式、论文离线/在线效果、本地协议和复现边界。论文信息由 `scripts/sync_reproduction_metadata.py` 统一同步；扩展规则见[架构文档](../architecture.md)。
