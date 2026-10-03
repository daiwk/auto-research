# LEGO-OPD: Factorized Teacher Composition for Multimodal On-Policy Distillation

> **复现级别：L1 核心机制诊断。** 执行 factorized teacher composition；未加载 LLM/VLM teacher。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv v1](https://arxiv.org/abs/2610.00333) |
| 公司/机构 | KAIST（按第一作者署名单位） |
| 首次公开日期 | 2026-09-29（arXiv v1） |
| 原文开源代码 | 否：截至 2026-10-03 未找到原作者公开实现 |
| Adapter | `lego-opd` |
| 本地复现代码 | [`src/auto_research/post_training/latest_20261003.py`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/post_training/latest_20261003.py) |

## 原始论文总结

### 背景与主要改动

把语言专家作为 token prior，把 grounding 专家只作为视觉 likelihood，以乘积专家形式组成 OPD teacher，避免连同 VLM 语言偏差一起蒸馏。

```mermaid
flowchart LR
  I[输入与当前状态] --> M[lego-opd 核心机制]
  M --> A[可审计中间量]
  A --> O[输出或状态更新]
```

<!-- paper-figure:start -->
### 原论文关键图

[![LEGO-OPD: Factorized Teacher Composition for Multimodal On-Policy Distillation 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2610.00333v1/LEGOOPD_main_fig.png)

> **原论文 Figure 1（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2610.00333)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$p_T(y|x,v)\propto p_L(y|x)p_G(y|x,v)^lpha$。

### 论文离线与线上效果

多模态 benchmark 上改善 grounding，同时较直接 VLM teacher 更好保留语言推理。

## 本地复现

> **本地对照口径**：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。

- 三种子诊断：[`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)
- `diagnostic_only=true`，不进入正式能力排名。

## 复现边界

执行 factorized teacher composition；未加载 LLM/VLM teacher。
