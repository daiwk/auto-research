# Paper reproductions

这里是论文专用 adapter 的长期实验索引。每篇论文的模型、实验、报告和结论文档独立存放，不与通用 topic research loop 混写。

后续新增工业论文执行[真实线上 A/B 硬门槛](industrial-online-ab-selection.md)。DIN 与 HSTU 满足该门槛；用户明确指定的经典基线 SASRec、TIGER 没有线上 A/B，只作为具名例外，不扩大后续选文范围。2026-01-01 至 2026-07-13 的 Google/Meta 专项筛选见[原报告](2026-google-meta-online-ab-selection.md)。

个人博客两个“工业界+落地”章节的 94 个主条目全量审计见[博客专项清单](blog-llm-rec-industrial-audit.md)。

可按[公司](catalog/by-company.md)、[主题](catalog/by-topic.md)或[年月](catalog/by-month.md)浏览；物理 adapter 路径保持稳定。

## 保真度门槛

数据规模缩小、私有数据替换为公开数据不自动构成折损；但论文核心网络、训练目标或推理路径被 heuristic 替代时，必须标为“概念验证（非论文复现）”。默认 `--paper all` 只运行前两级。

## 当前审计

| Fidelity | Adapter / paper | Paper online evidence | Local status |
|---|---|---|---|
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

共享的公开数据切分、逐用户及矩阵化全库指标位于 `reproductions/rec_utils.py`，序列模型的 all-position 训练位于 `reproductions/sequence_training.py`，下载器位于 `datasets.py`。论文特有网络、采样、调参和报告逻辑保留在论文目录中。每篇 README 固定包含原论文背景、主要改动、Mermaid 架构图、核心公式、论文离线/在线效果、本地协议和复现边界。扩展规则见[架构文档](../architecture.md)。
