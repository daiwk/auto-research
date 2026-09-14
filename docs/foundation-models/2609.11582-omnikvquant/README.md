# OmniKVQuant: KV Cache Quantization for Omni-LLMs

> **复现级别：L1 核心机制诊断。** 本地执行 2-bit 窗口量化和模态独立旋转的 NumPy reference；Triton kernel 另需 A100/A30 验证。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [OmniKVQuant: KV Cache Quantization for Omni-LLMs](https://arxiv.org/abs/2609.11582) |
| 公司/机构 | KAIST（按第一作者署名单位） |
| 首次公开日期 | 2026-09-10 |
| 原文开源代码 | 是：[https://github.com/kaistmm/OmniKVQuant](https://github.com/kaistmm/OmniKVQuant) |
| Adapter / 方法 | `omnikvquant` |
| 本地复现代码 | [`src/auto_research/foundation_latest_20260914.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/foundation_latest_20260914.py) |

## 原始论文总结

### 背景与主要改动

按短时间窗确定 key 量化范围，并按模态分别旋转 value，处理 temporal drift 与异构几何。

```mermaid
flowchart LR
  I[输入与公开状态] --> M[omnikvquant 核心机制]
  M --> A[可审计中间量]
  A --> O[输出或更新]
```

<!-- paper-figure:start -->
### 原论文关键图

[![OmniKVQuant: KV Cache Quantization for Omni-LLMs 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/html/2609.11582v1/pca_value.png)

> **原论文 Figure 2（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2609.11582)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式或操作

本地代码把论文决定性操作实现为确定性的 reference kernel，并显式输出门控、选择、投影、图边或状态更新统计；测试覆盖公式不变量和边界条件。

### 论文离线与线上效果

Qwen2.5-Omni 在七个视听 benchmark 上以 2-bit KV 保留 98.1% FP16 表现。 这些数字来自原论文，不与本地缩小实验直接比较；论文未报告线上 A/B 时不推断线上收益。

## 本地复现

三种子指标见 [`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。

### 复现边界

本地执行 2-bit 窗口量化和模态独立旋转的 NumPy reference；Triton kernel 另需 A100/A30 验证。
