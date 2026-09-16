# TIAO: Token Importance-Aware Policy Optimization for Text Summarization

> **复现级别：L1 核心机制诊断。** 本地执行 token dependency 与双尺度 credit；未训练 7B 模型。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [TIAO: Token Importance-Aware Policy Optimization for Text Summarization](https://arxiv.org/abs/2609.16748) |
| 公司/机构 | National University of Defense Technology（按第一作者署名单位） |
| 首次公开日期 | 2026-09-15（arXiv v1） |
| 原文开源代码 | 是：[https://github.com/TechCloud-x/TIAO](https://github.com/TechCloud-x/TIAO) |
| Adapter / 方法 | `tiao` |
| 本地复现代码 | [`src/auto_research/post_training/latest_20260916_followup.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/post_training/latest_20260916_followup.py) |

## 原始论文总结

### 背景与主要改动

通过遮蔽源文档前后的 token 概率变化估计依赖性，同时重塑轨迹优势并聚焦重要 token 更新。

```mermaid
flowchart LR
  I[公开输入与当前状态] --> M[tiao 核心机制]
  M --> A[可审计中间量]
  A --> O[输出或状态更新]
```

<!-- paper-figure:start -->
### 原论文关键图

[![TIAO: Token Importance-Aware Policy Optimization for Text Summarization 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2609.16748v1/dependency_grouped_figure.png)

> **原论文 Figure 1（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2609.16748)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式与实现对应

本地 reference kernel 保留决定性的排序、门控、偏好方向、信用权重或状态转换，并输出可审计统计。三种子 fixture 用来验证不变量和边界，不把随机 mini-suite 分数解释成论文能力。

### 论文效果

论文中的准确率、速度、训练损失或 benchmark 结论只作为原文结果；本地结果不与其直接横比，也不外推线上收益。

## 本地复现

三种子结果见 [`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)。统一 receipt 标记 `diagnostic_only=true`，不能进入正式能力排名。

CUDA 路径的真实机器验证见本页论文信息所对应的 `docs/gpu-validations/` receipt；receipt 不包含主机名、SSH alias 或驱动/build 字符串。

## 复现边界

本地执行 token dependency 与双尺度 credit；未训练 7B 模型。
