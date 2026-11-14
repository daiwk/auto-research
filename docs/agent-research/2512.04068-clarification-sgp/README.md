# SGP：成本可控澄清与解释均衡 ReST 选择

[English](README-en.md)

> **component_only／L1机制诊断，不是完整模型或Agent能力复现。** 完整实验成本过高，不复现（审查 DONE）；仅以下精确定义子组件可执行。

## 论文信息

| 字段 | 内容 |
| --- | --- |
| 论文链接 | [Learning Steerable Clarification Policies with Collaborative Self-play](https://arxiv.org/abs/2512.04068v1)，[固定 v1 原文](https://arxiv.org/html/2512.04068v1) |
| 公司 / 机构 | 一作 Jonathan Berant，Google Research；已核优先署名：Google Research / Google DeepMind / Meta，合作属性不覆盖第一署名机构 |
| 首次公开日期 | **2025-12-03 18:49:54 UTC**；历史补漏，不是2026-11-13新首发 |
| 原作者代码 | 固定v1与本轮有界官方入口检索未找到可核实专属源码；未把引用库或第三方复刻算作作者代码 |
| 本地 adapter / key | `clarification-sgp`；`adapter=null`；未接入Evolve |
| 本地复现代码 | `src/auto_research/agent_research/clarification_sgp.py` |

## 原始论文总结

### 背景与主要改动

同一条含糊问题可以直接猜、列出多种解释，或先提问。最优方式依赖用户能接受的轮次与篇幅成本。论文让 assistant 明确看到成本 α、β，与仅 user 知道真实解释的模拟用户自博弈；环境在对话结束后评分。

训练不是选一次幸运高分。先过滤低 F1 与 user 忽视 assistant 的轨迹，对每种动作序列按各解释的平均 reward 再平均，选最优序列；然后每个解释选该序列下最高 reward 的轨迹，只训练 assistant turns。完整语义生成、user 模拟和三轮 ReST 未在本地实现。

### 架构与流程

```mermaid
flowchart LR
  Q[含糊问题与解释分布] --> R[外部自博弈轨迹与环境评分]
  R --> F[过滤无效轨迹]
  F --> S[跨解释均衡动作序列均值]
  S --> B[每解释选best兼容轨迹]
  B --> T[外部assistant微调]
```

<!-- paper-figure:start -->
### 原论文关键图

[![clarification-sgp 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/html/2512.04068v1/figures/example_rollout_nano.png)

图片来自[原论文](https://arxiv.org/html/2512.04068v1#S3.F2)，版权归原作者所有。保存官方HTML原PNG字节，未裁剪、重画或PDF渲染。对话示例图；只用于解释信息分工，本地没有生成图中对话。
<!-- paper-figure:end -->

### 核心公式

$$
R(\rho)=100F_1(\rho)-\alpha n_{clar}(\rho)-\beta\,words_{assistant}(\rho),\qquad
s^*=\arg\max_s\frac1{|I|}\sum_{i\in I}\operatorname{mean}_{\rho\sim(s,i)}R(\rho).
$$

本地 F1 输入与过滤阈值使用 0–1，reward 明确转为百分制分数，与原文 Table 2–3 及 α={0,2,20}、β={0.1,0.7,5} 的量级对应；若用归一化 reward，成本也必须同时除以 100。只扣最终 assistant 回答的 whitespace word 数，不扣 user 最终回答或思考文本。无某解释样本的序列不能估计均衡期望，本地不补假样本；并列按序列／ID排序是局部确定性约定。

### 论文离线与线上效果

固定 v1 的 AmbigQA development、含糊问题上，作者 SGP 平均 reward 6.63、F1 19.94，相对 Prompted 的 −34.49／16.16；Pacific 对应为 54.32／65.73。它们是完整 Gemma2-9B 自博弈与训练结果，不是本地数值选择器的能力。未报告用户生产流量线上 A/B。

## 本地复现

### 数据协议与代码映射

`Rollout` 仅含离线评测值、解释 ID、动作序列与最后回答字数，不含 actor 的 gold 参数。`reward` 实际计算成本；`select_rollouts` 过滤、均衡解释均值、选择序列和逐解释选样。低 F1 默认阈值由调用方按 AmbigQA 0.1／Pacific 0.4 提供。user-answer overlap≥0.5 是原文拒绝忽视 assistant 的机械筛选，不是语义理解证明。

```bash
PYTHONPATH=src python -c 'from auto_research.agent_research.clarification_sgp import diagnostic; print(diagnostic(42))'
PYTHONPATH=src python -m pytest tests/test_nov13_colm_agent_components.py -q
```

### 结果与负控

正负控覆盖幸运单样本不能压过解释均衡均值、澄清成本改变选择、最终 assistant 字数单位、非法动作与缺失解释覆盖拒绝。固定离线分数只验证公式和选择，不生成训练语料或测得澄清策略。

三seed机制执行回执见[CPU组件指标](metrics/component-cpu-seeds42-44.json)及本轮冻结记录；它是固定输入机制诊断，不是完整训练、能力提升或线上收益。GPU验收仅以真实A100/A30回执为准。

## 复现边界

没有实现 user/assistant、token-F1 evaluator、ReST 微调、开发集 checkpoint 选择或正式对话基准。环境离线评分可使用参考答案，但不允许传入被评测 assistant；本地没有 actor 回调。完整实验高成本不复现，CPU选择器不等于完整算法有效性证明。

### 高成本完整实验

Gemma2-9B双模型、192训练rollout/query、64测试rollout/query、3轮ReST和两benchmark；完整多轮生成/训练高成本不复现。 这是论文／上游配置成本依据，不是本地训练测量。没有为估价试训、调用收费API或下载checkpoint。**成本过高，不复现（审查 DONE）**；不进入自动重试或自动实现队列。
