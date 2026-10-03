# PACE: Provenance-Aware Capability Enforcement for Tool-Using LLM Agents

> **复现级别：L1 核心机制诊断。** 执行 pre-effect capability/provenance gate；不运行浏览器或系统工具。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv v1](https://arxiv.org/abs/2610.01349) |
| 公司/机构 | 原文首页未列第一作者机构（按第一作者署名单位） |
| 首次公开日期 | 2026-10-01（arXiv v1） |
| 原文开源代码 | 否：截至 2026-10-03 未找到原作者公开实现 |
| Adapter | `pace-capability` |
| 本地复现代码 | [`src/auto_research/agent_research/latest_20261003.py`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/agent_research/latest_20261003.py) |

## 原始论文总结

### 背景与主要改动

在每次工具副作用发生前，根据认证请求编译出的 authority 与输入 provenance 同时检查 effect；入库时安全不代表执行时可信。

```mermaid
flowchart LR
  I[输入与当前状态] --> M[pace-capability 核心机制]
  M --> A[可审计中间量]
  A --> O[输出或状态更新]
```

<!-- paper-figure:start -->
### 原论文关键图

[![PACE: Provenance-Aware Capability Enforcement for Tool-Using LLM Agents 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2610.01349v1/PACE.png)

> **原论文 Figure 1（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2610.01349)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$allow=effects(call)\subseteq authority\land trusted(provenance)$。

### 论文离线与线上效果

论文给出认证执行合同和多类注入攻击评测。

## 本地复现

> **本地对照口径**：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。

- 三种子诊断：[`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)
- `diagnostic_only=true`，不进入正式能力排名。

## 复现边界

执行 pre-effect capability/provenance gate；不运行浏览器或系统工具。
