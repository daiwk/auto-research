# Industrial recommendation paper selection: online A/B required

检索复核日期：2026-07-14。该规则适用于后续新增的推荐系统论文。

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
| [OneRec-V2](https://arxiv.org/abs/2508.20900) | Kuaishou | App Stay Time +0.467%/+0.741% | 下一批：lazy decoder 与真实反馈 RL |

## 明确排除

- OpenOneRec Technical Report（arXiv 2512.24762）：开源价值高，但正文没有可核验的量化生产 A/B；不满足硬门槛。
- MiniOneRec：公开 scaling/离线实验为主，没有量化线上 A/B。
- 仅在 VirtualTB、LLM agent 或日志 replay 中评估的论文：不属于真实流量 A/B。
