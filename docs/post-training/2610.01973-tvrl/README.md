# Token-Level Video Reinforcement Learning

> **复现级别：L1 核心机制诊断。** 执行梯度 credit 归一化；未训练视频扩散模型。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv v1](https://arxiv.org/abs/2610.01973) |
| 公司/机构 | 原文首页未列第一作者机构（按第一作者署名单位） |
| 首次公开日期 | 2026-10-01（arXiv v1） |
| 原文开源代码 | 否：截至 2026-10-03 未找到原作者公开实现 |
| Adapter | `tvrl` |
| 本地复现代码 | [`src/auto_research/post_training/latest_20261003.py`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/post_training/latest_20261003.py) |

## 原始论文总结

### 背景与主要改动

冻结 VLM 的视频输入梯度定位对 reward 最敏感的生成 token，再把同组 advantage 稠密重分配到 token。

```mermaid
flowchart LR
  I[输入与当前状态] --> M[tvrl 核心机制]
  M --> A[可审计中间量]
  A --> O[输出或状态更新]
```

<!-- paper-figure:start -->
### 原论文关键图

[![Token-Level Video Reinforcement Learning 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2610.01973v1/teaser_results.png)

> **原论文 Figure 1（关键图）**：展示原论文的训练流程与关键优化环节。图片来自[原论文](https://arxiv.org/abs/2610.01973)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$c_t=\|\partial R/\partial z_t\|/mean_t\|\partial R/\partial z_t\|$。

### 论文离线与线上效果

论文在视频生成评测上报告比标量 GRPO 更好的提示遵循和时序质量。

## 本地复现

> **本地对照口径**：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。

- 三种子诊断：[`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)
- `diagnostic_only=true`，不进入正式能力排名。

## 复现边界

执行梯度 credit 归一化；未训练视频扩散模型。
