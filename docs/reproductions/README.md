# Paper reproductions

这里是论文专用 adapter 的长期实验索引。每篇论文的模型、实验、报告和结论文档独立存放，不与通用 topic research loop 混写。

后续新增论文执行[真实线上 A/B 硬门槛](industrial-online-ab-selection.md)。2026-01-01 至 2026-07-13 的 Google/Meta 专项筛选见[原报告](2026-google-meta-online-ab-selection.md)。

## 保真度门槛

数据规模缩小、私有数据替换为公开数据不自动构成折损；但论文核心网络、训练目标或推理路径被 heuristic 替代时，必须标为“概念验证（非论文复现）”。默认 `--paper all` 只运行前两级。

## 当前审计

| Fidelity | Adapter / paper | Paper online evidence | Local status |
|---|---|---|---|
| 完整核心链路 | `plum` · [PLUM](2510.07784-plum/README.md) | YouTube Panel CTR +0.76%/+4.96% | CPT 降低 loss；Recall@10 R1/CR1 0.5%，R2/CR2 0，未验证召回增益 |
| 完整核心链路 | `onerec` · [OneRec](2502.18965-onerec/README.md) | Kuaishou watch time +1.68% | 核心链路均执行；DPO 将本地 NDCG@10 从 0.0157 降至 0 |
| 完整核心链路 | `g2rec` · [G2Rec](2606.20554-g2rec/README.md) | Meta +0.06%–+0.19% | Beauty 上 soft graph + generative dual-loss；NDCG@10 +11.92% |
| 完整核心链路 | `mixformer` · [MixFormer](2602.14110-mixformer/README.md) | Douyin duration +0.2799% | matched-budget trainable blocks；NDCG@10 +17.41% |
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

共享的公开数据切分和指标位于 `reproductions/rec_utils.py`，下载器位于 `datasets.py`。论文特有网络、采样、调参和报告逻辑保留在论文目录中。每篇 README 固定包含原论文背景、主要改动、Mermaid 架构图、核心公式、论文离线/在线效果、本地协议和复现边界。扩展规则见[架构文档](../architecture.md)。
