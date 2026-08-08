# Agent0：零人工数据的自进化多 Agent 课程

> **保真度：核心机制复现**。本页不把确定性 mini-suite 冒充原论文完整 benchmark。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [Agent0：零人工数据的自进化多 Agent 课程（arXiv 2511.16043）](https://arxiv.org/abs/2511.16043) |
| 公司 / 机构 | Peng Xia 等（按一作归档） |
| 首次公开日期 | 2025-11-20（arXiv v1） |
| 原作者代码 | 未发现/未发布原作者官方代码仓库 |
| 本地 adapter / 方法键 | `agent0` |
| 本地复现代码 | [`src/auto_research/agent_research/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/agent_research/) |

## 原始论文总结

### 背景与主要改动

任务生成 Agent 提议可验证工具任务，多个执行 Agent 产生候选并多数投票，课程按当前能力边界升级。

```mermaid
flowchart LR
 A["公开输入 / 历史"] --> B["agent0 训练 / 执行闭环"]
 B --> C["论文特有状态或目标"]
 C --> D["同预算评测"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![Agent0：零人工数据的自进化多 Agent 课程 原论文 Figure 1](assets/paper-figure-01.png)](https://ar5iv.labs.arxiv.org/html/2511.16043/assets/x1.png)

> **原论文 Figure 1（关键图）**：展示原论文提出的核心架构、主要模块及其连接关系。图片来自[原论文](https://arxiv.org/abs/2511.16043)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
x\sim\pi_{task},\ y_{1:K}\sim\pi_{agent},\ \hat y=\operatorname{mode}(y_{1:K}),\quad R=V(x,\hat y).
$$

### 论文离线与线上效果

论文从零种子数据构建 tool-integrated reasoning curriculum，并提升多项 agent benchmark。 论文未报告生产线上 A/B，本页不补造线上数字。

## 本地复现

PlanBench mini-suite、120 episodes、seed 42：joint success **1.0000**，average cost 0.3200；方法特有操作有非零 telemetry。

```bash
auto-research agent-eval --method agent0 --benchmark planbench-mini --episodes 120 --seed 42
auto-research evolve --model agent --dataset planbench-mini --direction "组合 agent0 与已安装论文算子" --generations 2 --population 4
```

固定指标见 [`../../experiments/global-p0-20260808-seed42.json`](../../experiments/global-p0-20260808-seed42.json)。

## 复现边界

本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。
