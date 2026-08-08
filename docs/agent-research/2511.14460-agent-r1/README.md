# Agent-R1

> **保真度：核心机制复现**。本页不把确定性 mini-suite 冒充原论文完整 benchmark。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [Agent-R1（arXiv 2511.14460）](https://arxiv.org/abs/2511.14460) |
| 公司 / 机构 | University of Science and Technology of China |
| 首次公开日期 | 2025-11-18（arXiv v1） |
| 原作者代码 | 是：[原作者仓库](https://github.com/AgentR1/Agent-R1) |
| 本地 adapter / 方法键 | `agent-r1` |
| 本地复现代码 | [`src/auto_research/agent_research/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/agent_research/) |

## 原始论文总结

### 背景与主要改动

把每次 agent/environment 交互作为独立 transition，以可插拔上下文管理、环境接口与优化器支持 token 或 step 级信用。

```mermaid
flowchart LR
 A["公开输入"] --> B["agent-r1 核心机制"]
 B --> C["同预算训练 / 执行"]
 C --> D["公开评测与诊断"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![Agent-R1 原论文 Figure 3](assets/paper-figure-01.png)](https://arxiv.org/html/2511.14460v2/x3.png)

> **原论文 Figure 3（关键图）**：展示原论文提出的核心架构、主要模块及其连接关系。图片来自[原论文](https://arxiv.org/abs/2511.14460)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
\tau=(s_t,a_t,o_{t+1})_{t=1}^T,\quad A_t=\delta_t+\gamma\lambda A_{t+1}.
$$

### 论文离线与线上效果

技术报告展示统一框架对多轮 agentic RL 工作流的支持；无生产 A/B。 论文未报告生产线上 A/B，本页不补造线上数字。

## 本地复现

planbench-mini、120 episodes、seed 42：joint success **1.0000**，average cost **0.9600**。

```bash
auto-research agent-study --method agent-r1 --benchmark planbench-mini --episodes 120 --seed 42
auto-research evolve --model agent --dataset planbench-mini --direction "组合 agent-r1 与已安装论文算子" --generations 2 --population 4
```

固定指标见 [`../../experiments/global-p1-20260808-seed42.json`](../../experiments/global-p1-20260808-seed42.json)。

## 复现边界

本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。
