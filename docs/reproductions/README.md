# 复现总览

这是论文筛选、实现状态和实验结论的**唯一汇总页**。后续新增论文或重跑实验时，只更新本页和对应论文 README，不再新建阶段性审计、候选或对照汇总页。

可按[公司](catalog/by-company.md)、[主题](catalog/by-topic.md)或[年月](catalog/by-month.md)浏览具体论文。

## 选文与记录规则 {#selection-policy}

- **工业论文硬门槛**：正文必须披露真实生产流量的量化线上 A/B；或由用户明确认可论文所述的统计显著全流量发布、业务收益与 guardrail 结论。仅“已部署”、离线 SOTA 或模拟器结果不算；未披露具体 lift 的 full-traffic 论文必须明确标注，不能换算成百分比。
- **纯 LLM 论文门槛**：不要求线上 A/B，但必须有公开 benchmark、同预算对照和可在 WikiText 等公开数据上实际训练的核心方法；只写公式或固定打分不进入复现表。
- **具名例外**：SASRec、TIGER 是用户指定的经典基线，没有线上 A/B，不据此放宽后续选文标准。
- **本地结果口径**：每篇 README 明确基线、实验组、数据、主指标和相对变化；论文线上结果、本地跨模型比较、模块消融和效率对照分开写。
- **保真度**：公开数据替代私有数据或缩小规模可以接受；核心网络、训练目标或推理路径被 heuristic 替代时，只能标为“概念验证”。默认批量运行不包含概念验证。
- **论文信息**：每篇 README 顶部固定列出论文链接、公司/机构、arXiv v1 日期、原作者是否开源代码、Adapter 和本地复现代码位置；未找到原作者代码时必须明确写“否”，不能留空。

统一 DIN 实验使用 MovieLens-100K、时间 leave-two-out、全物品排序和 seeds 42/43/44；SERAL、LEADRE、COBRA、ARGUS、GR4AD、MM-LLM 使用同一 DIN NDCG@10 `0.02167`，Cross-domain KD 在独立 target split 上使用 DIN `0.05518`。这些结果只代表当前公开小数据协议，不等同于论文私有工业数据结论。

## 当前进度

- 已审计个人博客两个工业落地章节的 94 个主条目和 138 个 arXiv 链接。
- 已登记并复核 73 个 adapter；其中推荐论文继续执行线上 A/B/full-traffic 证据门槛，纯 LLM 论文执行公开 benchmark 与真实训练门槛。
- 暂缓：AIGQ（缺等价 query/CTR reward）、RaG（依赖视频生成与质量反馈）、RoleGen（缺 conversion trajectory 与线上反馈闭环）、LCU（数据需保密协议）。
- 跳过：EGA-V1；仅有离线结果或无法核验量化线上 A/B 的论文不进入实现队列。
- 2026 年剩余硬门槛论文已进入核心机制复现；2026-07-22 再加入 RecGPT-V3、SlimPer、RECAP、UAME、Convolution for LLMs 与 PPL-Factory。SlimPer 由用户明确认可其统计显著全流量证据，文档不虚构具体线上 lift；PVTG 因缺量化生产证据、SCASRec 因业务指标证据有歧义未纳入。

## 全部复现（73/73）

| 保真度 | Adapter / 论文 | 原论文线上效果 | 本地结论 |
|---|---|---|---|
| 核心机制 | `recgpt-mobile` · [RecGPT-Mobile](2605.04726-recgpt-mobile/README.md) | 淘宝 CLICK +1.8%、PAY +2.7%、GMV +2.5% | 真实 135M LoRA semantic intent accuracy +100.00%；INT8 相对 -6.25%、体积 -53.68%，触发器跳过 96.21% 推理 |
| 核心机制 | `sort-gen` · [SORT-Gen](2505.07197-sort-gen/README.md) | 相对部署基线 CLICK +4.13%、GMV +8.10% | ordered regression + 单次 mask-driven queue generation；Click +5.10%、Pay +8.46%、GMV proxy +9.00%、ILAD +2.89% |
| 核心机制 | `recgpt-v3` · [RecGPT-V3](2607.15591-recgpt-v3/README.md) | 淘宝 Feed IPV +1.28%、CTR +1.00%、GMV +3.97%；资源 -52.4% | 两阶段教师蒸馏后 NDCG@10 +36.96%，memory token -65%、latent slots -90%，但 head share +71.43% |
| 核心机制 | `slimper` · [SlimPer](2607.12281-slimper/README.md) | Instagram Reels/Feed 统计显著全流量提升；具体 lift 未披露 | 参数匹配下 NDCG@10 +1.29%，attention-score elements -94.12% |
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
| 概念验证 | `llatte` · [LLaTTE](2601.20083-llatte/README.md) | Meta conversion +4.3% | 缺 MLA、DHEN、semantic LLM features |
| 概念验证 | `self-evolving-rec` · [Self-Evolving RecSys](2602.10226-self-evolving-rec/README.md) | Google +0.03%–+0.14% | 固定候选代替 LLM agent；无线上反馈闭环 |
| 概念验证 | `cmsl` · [CMSL](2606.28533-cmsl/README.md) | Meta +0.092%–+0.171% | 固定 genre strand 代替 learned lenses/HSTU |
| 概念验证 | `longer` · [LONGER](2505.04421-longer/README.md) | Douyin Ads/电商 A/B | 打分代理，未训练 hybrid attention/InnerTrans |

概念验证 README 中的历史本地百分比是旧的 heuristic 诊断结果，不应与论文离线或线上结果比较，也不能作为“论文方法有效”的证据。

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
