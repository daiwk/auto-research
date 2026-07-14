# Industrial recommendation paper selection: online A/B required

检索复核日期：2026-07-14。该规则适用于后续新增的推荐系统论文。

个人博客两个工业落地章节的全量解析、去重和后续队列见[专项审计](blog-llm-rec-industrial-audit.md)。

## 硬性门槛

一篇论文必须同时满足：

1. 正文明确说明真实生产流量的 online/live A/B test；
2. 给出至少一个量化业务指标及相对或绝对提升；
3. 对照组是当时生产 baseline，不能是模拟器、离线 replay 或 LLM user agent；
4. 方法能够映射到召回、排序、生成式推荐、训练或 serving 的可实现模块。

“已部署”“服务大量用户”“离线 SOTA”“开源完整”都不能替代量化线上 A/B。已有 SIS、MDCNS 是该规则确定前的专项实现，保留但不作为后续筛选范例。

## 本轮新增并实现

| Paper | Organization | Area | Quantified online A/B |
|---|---|---|---|
| [PinRec](https://arxiv.org/abs/2504.10507) | Pinterest | outcome-conditioned multi-token retrieval | Homefeed Grid Clicks +4.01%；MT+OC Time Spent +0.55% |
| [GenRank](https://arxiv.org/abs/2505.04180) | Xiaohongshu | action-oriented generative ranking | Engagements +1.2474%；Time Spent +0.3345% |
| [LEARN](https://arxiv.org/abs/2405.03988) | Kuaishou | frozen LLM embedding、PCH | 冷启 item Revenue +8.77%；长尾 +4.63% |
| [NoteLLM](https://arxiv.org/abs/2403.01744) | Xiaohongshu | compression token、GCL、CSFT | I2I CTR +16.20%；comments +1.10% |
| [KAR](https://arxiv.org/abs/2306.10933) | Huawei | LLM 知识生成、hybrid-expert、CTR/召回 | 新闻 Recall +7%；音乐播放量 +1.70%、时长 +1.57% |
| [BAHE](https://arxiv.org/abs/2403.19347) | Ant Group | 原子行为缓存、长文本 CTR、训练效率 | 两周广告 A/B：CTR +9.65%、CPM +2.41% |
| [BEQUE](https://arxiv.org/abs/2311.03758) | Alibaba | Query rewrite、离线反馈、PRO | 淘宝搜索 14 天：GMV +0.40%、交易数 +0.34%、UV +0.33% |
| [M6-Rec](https://arxiv.org/abs/2205.08084) | Alibaba | 预训练语言模型、option-adapter、开放式推荐 | Alipay mini-app retrieval 相对 CTR >+1.0%，后全量部署 |
| [OneRec-V2](https://arxiv.org/abs/2508.20900) | Kuaishou | lazy decoder、真实反馈 RL、GBPO | 5% 流量一周；Kuaishou stay +0.467%，Lite +0.741% |
| [PLUM](https://arxiv.org/abs/2510.07784) | Google DeepMind / YouTube | LLM CPT、Semantic ID、生成式召回 | LFV Panel CTR +0.76%；Shorts +4.96% |
| [OneRec](https://arxiv.org/abs/2502.18965) | Kuaishou | session generation、MoE、IPA/DPO | 1% 流量；watch time +1.68%，view duration +6.56% |
| [LONGER](https://arxiv.org/abs/2505.04421) | ByteDance / Douyin | 超长序列、token merge、KV cache | Douyin Ads ADSS +1.063%–+2.097%；电商 Order/U +4.6125%–+7.9222% |
| [MixFormer](https://arxiv.org/abs/2602.14110) | ByteDance / Douyin | dense/sequence 统一 scaling | Douyin duration +0.2799%；Douyin Lite +0.4105% |
| [RankMixer](https://arxiv.org/abs/2507.15551) | ByteDance / Douyin | token mixing、per-token FFN、Sparse MoE | Active Days +0.3%；App duration +1.08% |
| [HyFormer](https://arxiv.org/abs/2601.12681) | ByteDance / Douyin Search | query decoding、query boosting | Watch time +0.293%；Finish/U +1.111%；Query change -0.236% |
| [OneTrans](https://arxiv.org/abs/2510.26104) | ByteDance | unified causal Transformer、KV cache | Feeds GMV/U +5.6848%；Mall +3.6696%；p99 latency 下降 |
| [Rec-Distill](https://arxiv.org/abs/2605.29755) | ByteDance / Douyin / TikTok | teacher/student distillation、batch+stream | Ads ADVV +1.00%；Rec Finish/U +1.2725%；Live gift revenue +0.78% |
| [DIN](https://arxiv.org/abs/1706.06978) | Alibaba | candidate-aware interest、CTR ranking | CTR +10.0%；RPM +3.8% |
| [HSTU](https://arxiv.org/abs/2402.17152) | Meta | generative sequential ranking、long history | Engagement +12.4%；Consumption +4.4% |
| [TransAct V2](https://arxiv.org/abs/2506.02267) | Pinterest | lifelong sequence、candidate NN、next-action loss | Repin +6.35%；Hide -12.80%；Time Spent +1.41% |
| [PinFM](https://arxiv.org/abs/2507.12704) | Pinterest | sequence foundation model、DCAT、pretrain/fine-tune | HF Sitewide Saves +1.20%；Fresh Saves +5.70%；I2I +0.72% |
| [LLM Retrieval](https://arxiv.org/abs/2605.21969) | Meta | LLM hierarchical attributes、semantic graph、predictability | top-line +0.45%；final-stage recall +1.2%；A/A' difference -8.62% |

## 用户指定的经典基线例外

以下论文没有量化真实线上 A/B，因此不属于自动选文候选；本次仅因用户明确点名而实现，用作基础能力和公平对照：

| Paper | Role | Online A/B | Local status |
|---|---|---|---|
| [SASRec](https://arxiv.org/abs/1808.09781) | 经典序列推荐 baseline | 未报告 | 完整核心链路，MovieLens-100K 全库评估 |
| [TIGER](https://arxiv.org/abs/2305.05065) | 经典生成式检索 | 未报告 | RQ-VAE Semantic ID + 自回归检索核心机制 |

这两个具名例外不构成放宽硬门槛的先例。

## 合格候选队列

| Paper | Organization | Online evidence | Status |
|---|---|---|---|
| [OneRec Technical Report](https://arxiv.org/abs/2506.13695) | Kuaishou | App Stay Time +0.54%/+1.24% | 与 OneRec adapter 机制重叠，先不重复实现 |
| [GR4AD](https://arxiv.org/abs/2602.22732) | Kuaishou | Ad revenue 最高 +4.2% | 与 OneRec-V2 的 LazyAR 链路重叠，候选保留 |

## Google / Meta 2026 专项审计

时间窗为 2026-01-01 至 2026-07-13，要求作者单位属于 Google 或 Meta，并披露真实流量的量化线上 A/B。该专项不再维护单独的重复文档。

| Status | Paper | Company | Quantified online A/B |
|---|---|---|---|
| 已实现 | LLaTTE (2601.20083) | Meta | conversion +4.3%、NE -0.25% |
| 已实现 | Self-Evolving RecSys (2602.10226) | Google | 多项 YouTube/surface 指标 +0.03%–+0.14% |
| 已实现 | Memento (2605.24051) | Meta | CTR +1.0%、CVR +1.2% |
| 已实现 | G2Rec (2606.20554) | Meta | engagement +0.06%–+0.19% |
| 已实现 | CMSL (2606.28533) | Meta | retrieval 指标 +0.092%–+0.171% |
| 已实现 | Cluster GOOBS (2607.00448) | Meta | CTR +53%，头部曝光集中度下降 |
| 候选保留 | Zero-shot Cross-domain KD for YouTube Music (2603.28994) | Google | 两周 live experiments；与现有蒸馏 adapter 部分重叠 |
| 候选保留 | MM-LLM Multimedia Understanding (2605.09338) | Meta | engagement +0.02%；与现有语义特征方向重叠 |
| 已实现 | LLM Retrieval for Stable Ad Recommendations (2605.21969) | Meta | top-line +0.45%、final-stage recall +1.2%、A/A' difference -8.62% |

排除示例：SilverTorch 首次提交于 2025-11，超出时间窗；Fine-Tuned LLM as a Complementary Predictor 的部署属于 Pinterest；Rec-Distill 不属于 Google/Meta，但已按扩大后的公司范围实现。

## 明确排除

- OpenOneRec Technical Report（arXiv 2512.24762）：开源价值高，但正文没有可核验的量化生产 A/B；不满足硬门槛。
- MiniOneRec：公开 scaling/离线实验为主，没有量化线上 A/B。
- 仅在 VirtualTB、LLM agent 或日志 replay 中评估的论文：不属于真实流量 A/B。
