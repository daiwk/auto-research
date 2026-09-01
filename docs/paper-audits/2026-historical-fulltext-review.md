# 2026 历史全文审计终态

> 本页关闭的是“是否值得进入实现队列”的全文审查，不把晋级论文冒充成已实现。
> 逐篇结构化证据见 [`2026-historical-fulltext-decisions.json`](2026-historical-fulltext-decisions.json)。

## 审计结果

| 终态 | 数量 | 含义 |
|---|---:|---|
| P0 实现候选 | 55 | 公司归属、方法范围和正文量化线上证据同时成立；已冻结到[固定实现路线图](2026-historical-p0-implementation-roadmap.md)，H01 已完成 |
| 全文审后 P2 | 273 | 已读全文，但没有达到当前 P0/P1 门槛；保留记录 |
| 原文不可用 | 3 | arXiv HTML/PDF 均不可用；不作方法或效果判断 |
| 未决全文 backlog | **0** | 每个历史候选均有终态 |

严格门槛会排除只说“未来做 A/B”、模拟 A/B、A/B 方法论文和没有量化线上结果的论文。

## 晋级 P0 实现队列

按首次公开时间倒排；Google / Meta 论文仍在实际实现排期中优先。

| 论文 | 首个署名机构 | 正文证据位置 | 量化 token |
|---|---|---|---|
| [2608.12778](https://arxiv.org/abs/2608.12778) DrEM: Dual-Side Robust Ensemble Ranking from Noisy User Preference Predictions in Video Recommendation | Affiliation: Shenzhen University , Shenzhen , China | 5.4. Online A/B Test (RQ3) | 5.1% |
| [2608.10182](https://arxiv.org/abs/2608.10182) From Prediction to Incrementality: Causal Optimization for Large-Scale Targeting and Recommendation | Affiliation: LinkedIn , Seattle , USA | From Prediction to Incrementality: Causal Optimization for Large-Scale Targeting and Recommendation | 7.20 % |
| [2608.07055](https://arxiv.org/abs/2608.07055) Teacher Retains Full Tokens, Student Merges Efficiently: TM20K for E-Commerce Sequence Modeling in Ad Recommendation | Affiliation: ByteDance , {lixinchun.bu,zhengduoru,zhaowenlin,dinghaoran,zhouziyi.828,tanjingxuan,yanghuizhi,jiangyuchen.jyc,chenzhe.john, zhengyuchao.yc,chenlinlan,wangdongjian.msg,wangdongyue,lixiaosong.1,maohongyue,tanyaocheng}@bytedance.com | 5.4. Online A/B Results | 10%, 1.036%, 5.6%, 5.6 % |
| [2607.28940](https://arxiv.org/abs/2607.28940) TransX: Scaling Transformer-based Recommendation via Behavioral and Serving Stream Crossings | Affiliation: LinkedIn , Sunnyvale , California , USA | TransX: Scaling Transformer-based Recommendation via Behavioral and Serving Stream Crossings | 6.0 %, 4.4 %, 80 % |
| [2607.28895](https://arxiv.org/abs/2607.28895) LLM-Based Generative Retrieval for Snapchat Content Recommendation | Affiliation: Snap, Inc. , USA | LLM-Based Generative Retrieval for Snapchat Content Recommendation | 0.37%, 0.09%, 0.18%, 0.11% |
| [2607.26427](https://arxiv.org/abs/2607.26427) PSG: Pair-Space Generation for Efficient Generative Reranking | Affiliation: Kuaishou Tech , Beijing , China | 5.2. Online A/B test | 0.178%, 0.1%, 80% |
| [2607.26418](https://arxiv.org/abs/2607.26418) DIRECTOR: Dynamic Index-based Recommendation with Transport-Optimized Retrieval | Affiliation: University of Science & Technology of China , Hefei , Anhui , China | 6.1.4. Implementation. | 99% |
| [2607.25344](https://arxiv.org/abs/2607.25344) Reward Guided Decoding for Generative Recommendation | Affiliation: 1 Institute of Information Engineering, Chinese Academy of Sciences, Beijing, China 2 School of Cyber Security, University of Chinese Academy of Sciences, Beijing, China 3 Kuaishou Technology, Beijing, China 4 Peking University, Beijing, China , {yangruochen, shengjiawei, liutingwen}@iie.ac.cn, {huangyusheng, zhengyoufeng, wenshuang, chenliangliang03, xupengbo03, zhangxiaoyu, wangshijun03, yangshuang08, zhaotianxing, hulantao, luocheng10}@kuaishou.com | 5.4. Online A/B Test (RQ4) | +0.392%, +0.689%, +0.349% |
| [2607.25110](https://arxiv.org/abs/2607.25110) Memory Layer: Train the In-Model Cache for Recommendation Models | Affiliation: Meta , | Memory Layer: Train the In-Model Cache for Recommendation Models | 96%, 100%, 86%, 6%, 30% |
| [2607.24025](https://arxiv.org/abs/2607.24025) SpecFormer: Mitigating Embedding and Attention Collapse via Spectral-Aware Transformer for Recommendation | Affiliation: Zhejiang University Hangzhou, China cuiyu23@zju.edu.cn ORCID: 0009-0001-6203-3022 | I Introduction | 1.34 %, 16.72 % |
| [2607.23038](https://arxiv.org/abs/2607.23038) EGR: Embedding-Native Generative Retrieval with a Shared LLM | Affiliation: Snap Inc. , Bellevue , WA , USA | 1. Introduction | 2.91 % |
| [2607.10910](https://arxiv.org/abs/2607.10910) ZoRRO: A Zero-Weight Personalized Recommender System for Scalable News Recommendation | Affiliation: Technical University of Denmark , Kongens Lyngby , Denmark | 4.3. Online A/B test | 45 %, 10 % |
| [2607.10239](https://arxiv.org/abs/2607.10239) Multilingual Semantic Retrieval for Apple Music Search | Affiliation: Apple , Cupertino , CA , USA | Multilingual Semantic Retrieval for Apple Music Search Note: Accepted to the Industry Track of the 20th ACM Conference on Recommender Systems (RecSys 2026). This is the authors’ ac | 69%, 2.28%, 86%, 7.93%, 0.89%, 0.14% |
| [2606.29946](https://arxiv.org/abs/2606.29946) POEM: Partial-Order Enhanced Real-Time Sequential Modeling for Recommendation | Affiliation: Kuaishou Technology , Beijing , China | 1. Introduction | +0.249%, +0.213% |
| [2606.27058](https://arxiv.org/abs/2606.27058) UniFormer: Efficient and Unified Model-Centric Scaling for Industrial Recommendation | Affiliation: Kuaishou Technology , Beijing , China | UniFormer: Efficient and Unified Model-Centric Scaling for Industrial Recommendation Thanks: ∗ Equal contributions. † Corresponding authors. | +0.101%, +0.260%, +0.729%, +1.113% |
| [2606.25496](https://arxiv.org/abs/2606.25496) Recommendation as Generation: Unifying Personalized Video Generation and Recommendation at Industrial Scale | Affiliation: 1 Kuaishou Technology Beijing, China 2 Beihang University Beijing, China | Recommendation as Generation: Unifying Personalized Video Generation and Recommendation at Industrial Scale Thanks: ∗ Equal contribution. § Work done during an internship at Kuaish | 1.87% |
| [2606.16838](https://arxiv.org/abs/2606.16838) OneRank: Unified Transformer-Native Ranking Architecture for Multi-Task Recommendation | Affiliation: Gaoling School of Artificial Intelligence, Renmin University of China , Beijing , China | 4.5. Online A/B Testing | 10% |
| [2606.16641](https://arxiv.org/abs/2606.16641) PIANO: Personalized Reranking via Information Aggregation Node for Music Search Optimization | Affiliation: NetEase Cloud Music, Hangzhou, China | PIANO: Personalized Reranking via Information Aggregation Node for Music Search Optimization | +0.62%, +4.45% |
| [2606.10357](https://arxiv.org/abs/2606.10357) Atomic Intent Reasoning: Bringing LLM Semantics to Industrial Cross-Domain Recommendations | Affiliation: The Hong Kong Polytechnic University , Hong Kong SAR , China | Atomic Intent Reasoning: Bringing LLM Semantics to Industrial Cross-Domain Recommendations | +3.446% |
| [2606.08466](https://arxiv.org/abs/2606.08466) ToolRec: Calibrated Preference Alignment for Query Recommendation in On-Device Assistants | Affiliation: Huazhong University of Science and Technology , Wuhan , China | 5.2. Main Online Results | 5% |
| [2606.06970](https://arxiv.org/abs/2606.06970) SSRLive: Live Streaming Recommendation with Dynamic Semantic ID | Affiliation: 1 Taobao & Tmall Group of Alibaba, Beijing, China | 1. Introduction | +3.38%, +0.72%, +3.12%, +2.92% |
| [2606.03866](https://arxiv.org/abs/2606.03866) Taiji: Pareto Optimal Policy Optimization with Semantics-IDs Trade-off for Industrial LLM-Enhanced Recommendation | Affiliation: Kuaishou Technology , Beijing , China | 1. Introduction | 2.83%, 3.30% |
| [2606.00282](https://arxiv.org/abs/2606.00282) Synthetic Data from Cross-Domain Events for Large-Scale Recommendation Systems | Affiliation: Meta | 5.2 Online A/B Test Results | 0.24 % |
| [2607.19357](https://arxiv.org/abs/2607.19357) Stochastic Primal-Dual Decoding for Multiobjective Generative Recommender Systems | Affiliation: Spotify , London , United Kingdom | Stochastic Primal-Dual Decoding for Multiobjective Generative Recommender Systems | +1.8% |
| [2605.27103](https://arxiv.org/abs/2605.27103) MuChator: Enabling Active Music Discovery via Conversational Music LLMs in Douyin Music | Affiliation: ByteDance , Beijing , China | MuChator: Enabling Active Music Discovery via Conversational Music LLMs in Douyin Music | 46.49% |
| [2605.27043](https://arxiv.org/abs/2605.27043) Causal Representation Learning for Generalisable Recommendation | Affiliation: University of Warwick | 4.3 Online A/B test on personalised playlist generation | 95% |
| [2605.16479](https://arxiv.org/abs/2605.16479) Policy-Grounded Dynamic Facet Suggestions for Job Search | Affiliation: LinkedIn Corporation , Mountain View , CA , USA | Policy-Grounded Dynamic Facet Suggestions for Job Search | 80 % |
| [2605.05855](https://arxiv.org/abs/2605.05855) Bridging Passive and Active: Enhancing Conversation Starter Recommendation via Active Expression Modeling | Affiliation: Bytedance , Beijing , China | Bridging Passive and Active: Enhancing Conversation Starter Recommendation via Active Expression Modeling | 0.54%, 0.04% |
| [2606.07546](https://arxiv.org/abs/2606.07546) Beyond Item IDs: Scaling Short-Form-Video Recommendation via Semantic-Native Long Sequence Modeling | Affiliation: Google , Mountain View, USA | 3.2. Semantic-Native Representations Eval | 6.81 % |
| [2604.18146](https://arxiv.org/abs/2604.18146) Modular Representation Compression: Adapting LLMs for Efficient and Effective Recommendations | Affiliation: Shanghai Jiao Tong University , Shanghai , China | Modular Representation Compression: Adapting LLMs for Efficient and Effective Recommendations | 2.82% |
| [2604.17878](https://arxiv.org/abs/2604.17878) RankUp: Towards High-rank Representations for Large Scale Advertising Recommender Systems | Affiliation: Tencent Inc. | 1. Introduction | 20%, 3.41%, 4.81%, 2.12% |
| [2604.12965](https://arxiv.org/abs/2604.12965) Efficient Retrieval Scaling with Hierarchical Indexing for Large Scale Recommendation | Affiliation: Meta , USA | 4.5. Online Service Report | 2.57% |
| [2604.10471](https://arxiv.org/abs/2604.10471) SID-Coord: Coordinating Semantic IDs for ID-based Ranking in Short-Video Search | Affiliation: Kuaishou Technology , Beijing , China | SID-Coord: Coordinating Semantic IDs for ID-based Ranking in Short-Video Search | +0.664%, +0.369% |
| [2603.28124](https://arxiv.org/abs/2603.28124) RCLRec: Reverse Curriculum Learning for Modeling Sparse Conversions in Generative Recommendation | Affiliation: Alibaba International Digital Commerce Group , Hangzhou , China | RCLRec: Reverse Curriculum Learning for Modeling Sparse Conversions in Generative Recommendation | +2.09%, +1.86% |
| [2603.21481](https://arxiv.org/abs/2603.21481) TagLLM: A Fine-Grained Tag Generation Approach for Note Recommendation | Affiliation: Department of Computer Science and Technology, Tongji University, Shanghai, China | TagLLM: A Fine-Grained Tag Generation Approach for Note Recommendation | 0.31%, 0.96%, 32.37% |
| [2603.19665](https://arxiv.org/abs/2603.19665) GenFacet: End-to-End Generative Faceted Search via Multi-Task Preference Alignment in E-Commerce | Affiliation: JD.com , BeiJing , China | GenFacet: End-to-End Generative Faceted Search via Multi-Task Preference Alignment in E-Commerce | 42.0%, 2.0% |
| [2603.04227](https://arxiv.org/abs/2603.04227) Constraint-Aware Generative Re-ranking for Multi-Objective Optimization in Advertising Feeds | Affiliation: Bilibili Inc | 13 Conclusion | 85% |
| [2603.00980](https://arxiv.org/abs/2603.00980) Beyond the Flat Sequence: Hierarchical and Preference-Aware Generative Recommendations | Affiliation: Harbin Institute of Technology , Harbin , China | 1. Introduction | +1.99% |
| [2602.13581](https://arxiv.org/abs/2602.13581) Climber-Pilot: A Non-Myopic Generative Recommendation Model Towards Better Instruction-Following | Affiliation: NetEase Cloud Music , Hangzhou , China | Climber-Pilot : A Non-Myopic Generative Recommendation Model Towards Better Instruction-Following | 4.24% |
| [2602.13134](https://arxiv.org/abs/2602.13134) Awakening Dormant Users: Generative Recommendation with Counterfactual Functional Role Reasoning | Affiliation: Institute of Artificial Intelligence , Beihang University , Beijing , China | Awakening Dormant Users: Generative Recommendation with Counterfactual Functional Role Reasoning | 6.2%, 7.3% |
| [2602.12972](https://arxiv.org/abs/2602.12972) Jointly Optimizing Debiased CTR and Uplift for Coupons Marketing: A Unified Causal Framework | Affiliation: 1 Kuaishou Technology, 2 Beijing Institute of Technology 3 Independent Researcher | 5.4. Online A/B Test (RQ3) | 10% |
| [2602.12593](https://arxiv.org/abs/2602.12593) RQ-GMM: Residual Quantized Gaussian Mixture Model for Multimodal Semantic Discretization in CTR Prediction | Affiliation: Tencent , Beijing , China | RQ-GMM: Residual Quantized Gaussian Mixture Model for Multimodal Semantic Discretization in CTR Prediction | 1.502% |
| [2602.12564](https://arxiv.org/abs/2602.12564) CAPTS: Channel-Aware, Preference-Aligned Trigger Selection for Multi-Channel Item-to-Item Retrieval | Affiliation: Kuaishou Technology , Beijing , China | CAPTS: Channel-Aware, Preference-Aligned Trigger Selection for Multi-Channel Item-to-Item Retrieval | +0.713%, +0.586% |
| [2602.12041](https://arxiv.org/abs/2602.12041) Compress, Cross and Scale: Multi-Level Compression Cross Networks for Efficient Scaling in Recommender Systems | Affiliation: Bilibili Inc. , Shanghai , China | Compress, Cross and Scale: Multi-Level Compression Cross Networks for Efficient Scaling in Recommender Systems | 0.52% |
| [2602.10455](https://arxiv.org/abs/2602.10455) Compute Only Once: UG-Separation for Efficient Large Recommendation Models | Affiliation: 1 ByteDance AML 2 ByteDance | Compute Only Once: UG-Separated TokenMixer for Efficient Large Recommendation Models Thanks: *These authors contributed equally. † Corresponding Author. | 20% |
| [2602.09386](https://arxiv.org/abs/2602.09386) SMES: Towards Scalable Multi-Task Recommendation via Expert Sparsity | Affiliation: Kuaishou Technology Co., Ltd. , Beijing , China | 4.7. Online A/B Test | 3.5%, +0.31%, +0.64%, +1.56%, +2.45%, 50% |
| [2602.08530](https://arxiv.org/abs/2602.08530) PIT: A Dynamic Personalized Item Tokenizer for End-to-End Generative Recommendation | Affiliation: Beijing University of Posts and Telecommunications , Beijing , China | PIT: A Dynamic Personalized Item Tokenizer for End-to-End Generative Recommendation | 0.402% |
| [2601.21285](https://arxiv.org/abs/2601.21285) Zenith: Scaling up Ranking Models for Billion-scale Livestreaming Recommendation | Affiliation: NC State University 1 , TikTok 2 , ByteDance 3 , ByteDance AML 4 rzhang38@ncsu.edu, zexi.huang@tiktok.com, {wangzikai.kevin, ke.sun1, zhengbohang, jiangyuchen.jyc, chenzhe.john, ouyangzhen, xiehuimin.weyman, phil.shen, zhangjunlin.neicul, zhengyuchao.yc, wentao.guo, wangqinglei}@bytedance.com | 1. Introduction | +1.05%, -1.10%, +9.93%, +8.11% |
| [2601.20215](https://arxiv.org/abs/2601.20215) Towards End-to-End Alignment of User Satisfaction via Questionnaire in Video Recommendation | Affiliation: Kuaishou Technology , Beijing , China | 5.3. Online A/B Testing | 5.1% |
| [2601.18664](https://arxiv.org/abs/2601.18664) S$^2$GR: Stepwise Semantic-Guided Reasoning in Latent Space for Generative Recommendation | Affiliation: Kuaishou Technology , Beijing , China | 5.4. Online Testing | 5.25% |
| [2601.17836](https://arxiv.org/abs/2601.17836) Unleashing the Potential of Sparse Attention on Long-term Behaviors for CTR Prediction | Affiliation: Institute of Software, Chinese
Academy of Sciences , University of Chinese Academy of Sciences
, Beijing , China | Unleashing the Potential of Sparse Attention on Long-term Behaviors for CTR Prediction Thanks: † Corresponding author. | 1.72%, 1.41% |
| [2601.14333](https://arxiv.org/abs/2601.14333) Hierarchical Contextual Uplift Bandits for Catalog Personalization | Affiliation: Dream11 , Mumbai , Maharashtra , India | 1. Introduction | 0.42%, 0.51%, 4%, 5% |
| [2601.06873](https://arxiv.org/abs/2601.06873) Applying Embedding-Based Retrieval to Airbnb Search | Affiliation: Airbnb, Inc., USA | 6.3 Online A/B Testing Results | 0.31%, 16% |
| [2601.04674](https://arxiv.org/abs/2601.04674) PROMISE: Process Reward Models Unlock Test-Time Scaling Laws in Generative Recommendations | Affiliation: Kuaishou Inc. , Beijing , China | 4.3. Online A/B Test Result (RQ2) | 5% |
| [2601.02955](https://arxiv.org/abs/2601.02955) Rethinking Multi-objective Ranking Ensemble in Recommender System: From Score Fusion to Rank Consistency | Affiliation: Kuaishou Technology , Beijing , China | 5.7. Online Results (RQ4) | 2.635%, 0.451% |

## 审计可复现性

提交仓库的不是论文全文，而是来源 URL、全文 SHA-256、证据章节、匹配术语、短量化 token、机构和代码 URL。
运行 `python scripts/review_historical_backlog.py --check` 可验证 331 篇覆盖、唯一性和 P0 证据字段。
