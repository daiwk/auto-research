# Learning from Teacher Continuations at Student States

> **复现级别：L1 核心机制诊断。** 执行 student-prefix/teacher-continuation 的精确 loss mask；未调用闭源 teacher。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [Learning from Teacher Continuations at Student States](https://arxiv.org/abs/2609.36246) |
| 公司/机构 | University of Illinois Urbana-Champaign（按第一作者署名单位） |
| 首次公开日期 | 2026-09-28（arXiv v1） |
| 原文开源代码 | 是：[https://dylanzsz.github.io/olive/](https://dylanzsz.github.io/olive/) |
| Adapter / 方法 | `olive` |
| 本地复现代码 | [`src/auto_research/post_training/latest_20260930_closure.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/post_training/latest_20260930_closure.py) |

## 原始论文总结

### 背景与主要改动

由当前 student 生成前缀，再让 teacher 从该 student state 续写；student 只在 teacher continuation token 上计算交叉熵。

```mermaid
flowchart LR
  I[公开输入/当前状态] --> M[olive 核心机制]
  M --> A[可审计中间量]
  A --> O[输出/更新状态]
```

<!-- paper-figure:start -->
### 原论文关键图

[![Learning from Teacher Continuations at Student States 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/pdf/2609.36246#page=5)

> **原论文 Figure 2（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2609.36246)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

本地 reference kernel 保留论文决定性的门控、掩码、递归、信用权重或晋级条件；测试同时检查梯度隔离、类型边界和确定性。

### 论文离线与线上效果

论文中的 benchmark、速度或训练曲线属于原文结果。本地三种子 mini-suite 仅检验机制和不变量，不与论文规模结果横比，也不外推线上收益。

## 本地复现

三种子诊断见 [`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)。其中 `diagnostic_only=true`，不能进入正式能力排名。

## 复现边界

执行 student-prefix/teacher-continuation 的精确 loss mask；未调用闭源 teacher。
