# Paper reproductions

这里是论文专用 adapter 的长期实验索引。每篇论文的模型、实验、报告和结论文档独立存放，不与通用 topic research loop 混写。

后续新增论文执行[真实线上 A/B 硬门槛](industrial-online-ab-selection.md)。2026-01-01 至 2026-07-13 的 Google/Meta 专项筛选见[原报告](2026-google-meta-online-ab-selection.md)。

## 当前结果

| Track | Adapter | Paper | Paper evidence | Local public-data result |
|---|---|---|---|---:|
| LLM | `sis` | [SIS](2607.04728-sis/README.md) | 非本轮 Google/Meta A/B 集合 | weight variance -6.62% |
| Recommendation | `mdcns` | [MDCNS](2605.19651-mdcns/README.md) | 论文公开离线结果 | Beauty NDCG@10 +104.75% vs Uniform |
| Recommendation | `llatte` | [LLaTTE](2601.20083-llatte/README.md) | Meta conversion +4.3% | NDCG@10 -3.57% |
| Recommendation | `self-evolving-rec` | [Self-Evolving RecSys](2602.10226-self-evolving-rec/README.md) | Google online metrics +0.03%–+0.14% | NDCG@10 +7.13% |
| Recommendation | `memento` | [Memento](2605.24051-memento/README.md) | Meta CTR +1.0%、CVR +1.2% | NDCG@10 +4.78% |
| Recommendation | `g2rec` | [G2Rec](2606.20554-g2rec/README.md) | Meta engagement +0.06%–+0.19% | Beauty NDCG@10 +0.72% |
| Recommendation | `cmsl` | [CMSL](2606.28533-cmsl/README.md) | Meta retrieval +0.092%–+0.171% | NDCG@10 +0.95% |
| Recommendation | `cluster-goobs` | [Cluster GOOBS](2607.00448-cluster-goobs/README.md) | Meta CTR +53% | ML-1M NDCG@10 +0.98% |
| Recommendation | `plum` | [PLUM](2510.07784-plum/README.md) | YouTube Panel CTR +0.76%/+4.96% | ML-1M NDCG@10 +24.62% |
| Recommendation | `onerec` | [OneRec](2502.18965-onerec/README.md) | Kuaishou watch time +1.68% | ML-1M NDCG@10 +28.78% |
| Recommendation | `longer` | [LONGER](2505.04421-longer/README.md) | Douyin Ads/电商多项 A/B | ML-100K NDCG@10 +0.41% |
| Recommendation | `mixformer` | [MixFormer](2602.14110-mixformer/README.md) | Douyin duration +0.2799% | ML-100K NDCG@10 +0.53% |

本地百分比均相对于各自 README 中定义的 baseline，不应与论文线上 A/B 直接比较。

## 统一运行方式

```bash
# 单篇
auto-research reproduce --paper <adapter> --seed 42

# 全部
auto-research reproduce --paper all --seed 42
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

共享的公开数据切分和指标位于 `reproductions/rec_utils.py`，下载器位于 `datasets.py`。论文特有网络、采样、调参和报告逻辑保留在论文目录中。每篇 README 固定包含原论文背景、主要改动、Mermaid 架构图、核心公式、论文离线/在线效果、本地协议和复现边界。扩展规则见[架构文档](../architecture.md)。
