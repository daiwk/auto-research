# MLLMCLIP：从多模态大模型蒸馏通用 CLIP

> **Fidelity：公开 checkpoint 核心路径。** 主路径加载真实 SmolVLM teacher 与 CLIP student，在公开图像上训练 CKA projection；MovieLens/NumPy 路径仅保留为快速机制诊断。

## 论文信息

| 项目 | 内容 |
|---|---|
| 论文链接 | [arXiv 2608.25575](https://arxiv.org/abs/2608.25575) |
| 公司/机构 | KAIST / Sony Group Corporation（第一作者第一署名单位为 KAIST） |
| 首次公开日期 | 2026-08-26（arXiv v1） |
| 原文开源代码 | 否：未发现原作者公开代码（核查日期：2026-08-28） |
| Adapter | `mllmclip` |
| 本地复现代码 | [`src/auto_research/reproductions/mllmclip/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/mllmclip/) |

## 原始论文总结

### 背景与主要改动

MLLM 的丰富视觉语义难以直接迁移到轻量 CLIP。论文从 teacher 各层按 attention 自适应选 token，以 CKA 对齐 student 图像/文本特征，保留部署时的双塔效率。

```mermaid
flowchart LR
  I[图像/文本] --> M[冻结 MLLM teacher]
  M --> A[逐层 attention token selection]
  A --> K[CKA alignment]
  C[CLIP student] --> K
  K --> C
```

<!-- paper-figure:start -->
### 原论文关键图

[![MLLMCLIP：从多模态大模型蒸馏通用 CLIP 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/html/2608.25575v1/main3.png)

> **原论文 Figure 2（关键图）**：展示原论文提出的核心架构、主要模块及其连接关系。图片来自[原论文](https://arxiv.org/abs/2608.25575)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
\operatorname{CKA}(X,Y)=\frac{\lVert Y^TX\rVert_F^2}{\lVert X^TX\rVert_F\lVert Y^TY\rVert_F},\qquad \mathcal L=1-\operatorname{CKA}(X,Y).
$$

### 论文离线与线上效果

论文在 26 个 compositionality、zero-shot classification 与 retrieval benchmark 上报告最佳平均结果；无工业线上 A/B。

## 本地复现

### 真实 checkpoint CUDA 路径（主结果）

该路径加载公开的 **SmolVLM2-256M** teacher 与 **CLIP ViT-B/32** student，在 CIFAR-10 公开图像上冻结两个 encoder，只训练匹配维度的 feature projection，并联合优化 cosine 与 linear CKA loss。结果记录精确 checkpoint revision、数据规模、seed、loss、held-out CKA、1-NN accuracy、耗时与峰值显存；checkpoint 和缓存不提交 GitHub。

```bash
AUTO_RESEARCH_DEVICE=cuda python -m \
  auto_research.reproductions.mllmclip.checkpoint \
  --data-dir data/cifar10 \
  --train-examples 128 --test-examples 64 \
  --steps 40 --seed 42 \
  --output runs/mllmclip/checkpoint-seed42.json
```

该路径受 `python scripts/validate_gpu_evidence.py` 合入门禁约束：必须先在真实 A100/A30 上跑通并提交去机器标识的 receipt。

### NumPy 机制诊断（非主结果）

> **本地对照口径**：基线为未蒸馏的公开内容特征；实验组以同一数据的协同视图作 teacher proxy。MovieLens proxy Recall@10 **0.0194 → 0.8306（+4171.43%）**；这个巨大增幅只反映代理视图可预测性，不能外推视觉 benchmark。

指标见 [`metrics/movielens-proxy-seed42.json`](metrics/movielens-proxy-seed42.json)。

```bash
auto-research reproduce --paper mllmclip --dataset-dir data --seed 42
```

## 复现边界

真实 checkpoint 路径使用公开图像和 SmolVLM 视觉 encoder feature，但仍未复刻论文完整 26-benchmark 训练规模、原始 teacher 配方与全量 CLIP 预训练。MovieLens proxy 仍为 diagnostic-only，不能与视觉 benchmark 混报。
