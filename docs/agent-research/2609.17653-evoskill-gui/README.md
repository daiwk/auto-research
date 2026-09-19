# Reflect, Revise, Reuse: Training-Free Skill Evolution for GUI Agents

> **复现级别：L1 核心机制诊断。** 本地只从公开 observation 读证据并演示受限技能修订；未运行 MobileWorld/AndroidWorld/OSWorld。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [Reflect, Revise, Reuse: Training-Free Skill Evolution for GUI Agents](https://arxiv.org/abs/2609.17653) |
| 公司/机构 | Zhejiang University（按第一作者署名单位） |
| 首次公开日期 | 2026-09-15（arXiv v1） |
| 原文开源代码 | 是：[https://github.com/ZJU-REAL/EvoSkill-GUI](https://github.com/ZJU-REAL/EvoSkill-GUI) |
| Adapter / 方法 | `evoskill-gui` |
| 本地复现代码 | [`src/auto_research/agent_research/latest_20260919.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/agent_research/latest_20260919.py) |

## 原始论文总结

### 背景与主要改动

把 GUI 技能拆成可编辑组件，执行失败后由信息隔离 critic 反思，并只修改责任组件，验证后的技能可跨任务复用。

```mermaid
flowchart LR
  I[公开输入/当前状态] --> M[evoskill-gui 核心机制]
  M --> A[可审计中间量]
  A --> O[输出/状态更新]
```

<!-- paper-figure:start -->
### 原论文关键图

[![Reflect, Revise, Reuse: Training-Free Skill Evolution for GUI Agents 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/html/2609.17653v1/method.png)

> **原论文 Figure 2（关键图）**：展示原论文提出的核心架构、主要模块及其连接关系。图片来自[原论文](https://arxiv.org/abs/2609.17653)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

本地 reference kernel 保留论文决定性的门控、权重、状态转换或调度规则，并把中间量写入指标产物；具体公式与变量对应见实现函数及测试中的不变量断言。

### 论文离线与线上效果

论文报告的线上、benchmark、训练效率或推理速度只作为原文结果。本地三种子 artifact 只验证核心机制、形状和状态不变量，不与论文数字直接横比。指标见 [`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)。

## 复现边界

本地只从公开 observation 读证据并演示受限技能修订；未运行 MobileWorld/AndroidWorld/OSWorld。
