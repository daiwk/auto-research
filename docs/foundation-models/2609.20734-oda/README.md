# On-Demand Attention: Efficient Long-Context Decoding with Learned Recall

> **复现级别：L1 核心机制诊断。** 本地执行 recall gate 和条件全局注意力；真实 A100 receipt 只证明 CUDA 路径，不外推 vLLM 吞吐。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [On-Demand Attention: Efficient Long-Context Decoding with Learned Recall](https://arxiv.org/abs/2609.20734) |
| 公司/机构 | Southern University of Science and Technology（按第一作者署名单位） |
| 首次公开日期 | 2026-09-17（arXiv v1） |
| 原文开源代码 | 否：截至 2026-09-19 未找到原作者公开实现仓库 |
| Adapter / 方法 | `oda` |
| 本地复现代码 | [`src/auto_research/foundation_latest_20260919.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/foundation_latest_20260919.py) |

## 原始论文总结

### 背景与主要改动

默认只读局部 KV，由轻量 recall head 在全局注意力发生前预测其收益；仅高收益 token 触发全局读取，完整 KV 仍保留。

```mermaid
flowchart LR
  I[公开输入/当前状态] --> M[oda 核心机制]
  M --> A[可审计中间量]
  A --> O[输出/状态更新]
```

<!-- paper-figure:start -->
### 原论文关键图

[![On-Demand Attention: Efficient Long-Context Decoding with Learned Recall 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2609.20734v1/fig_1_v2.png)

> **原论文 Figure 1（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2609.20734)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

本地 reference kernel 保留论文决定性的门控、权重、状态转换或调度规则，并把中间量写入指标产物；具体公式与变量对应见实现函数及测试中的不变量断言。

### 论文离线与线上效果

论文报告的线上、benchmark、训练效率或推理速度只作为原文结果。本地三种子 artifact 只验证核心机制、形状和状态不变量，不与论文数字直接横比。指标见 [`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)。

CUDA 路径已在真实 NVIDIA A100 上运行；脱敏 receipt 见 `docs/gpu-validations/`。

## 复现边界

本地执行 recall gate 和条件全局注意力；真实 A100 receipt 只证明 CUDA 路径，不外推 vLLM 吞吐。
