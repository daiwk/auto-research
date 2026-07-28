# Agent 统一评测协议

Agent 方法不仅比较最终成功率，还必须比较上下文、知识获取和工具维护成本。当前
mini-suite 保证 Mac/Linux CPU 可重复运行，后续真实 LLM executor 沿用相同指标接口。

## 评测矩阵

| Benchmark | 主要能力 | 本地任务 | 关键指标 |
|---|---|---|---|
| `evomem-mini` | episode 内/跨 episode 的知识与执行记忆 | EvoMem 四象限任务 | joint success、获取成本、memory size |
| `planbench-mini` | 可验证规划与过程复用 | 结构化动作序列 | plan success、平均成本、reused plans |
| `scalemcp-mini` | 有限上下文中的动态工具集合 | 多轮工具路由 | task success、上下文成本、tool evictions |

这些是仓库自带的确定性 mini-suite，不是完整 EvoMemBench、PlanBench 或 ScaleMCP。

## 公平口径

- 固定 120 episodes 和 seed 42，方法与基线使用同一任务序列。
- `long-context` 是不压缩历史的对照，成本按保留的上下文单元累计。
- 成功率相同时，比较平均成本和方法特有诊断；不能只用成本推断真实 LLM 效果。
- 新方法必须保存逐步 trace，标明记忆写入、检索、升级、复用和淘汰事件。
- 调用外部模型时必须记录模型、采样参数、token 成本、失败重试和缓存命中。

## 稳定结果

| 方法与 benchmark | joint success | 平均成本 | 诊断 |
|---|---:|---:|---|
| Long-context · EvoMem mini | 1.0000 | 64.5000 | 历史线性增长 |
| U-Mem · EvoMem mini | 1.0000 | 3.0500 | memory size 12 |
| LEGOMem · PlanBench mini | 1.0000 | 1.1200 | reused plans 108 |
| MemTool · ScaleMCP mini | 1.0000 | 1.9812 | tool evictions 200 |
| ReAct · ScaleMCP mini | 1.0000 | 3.0000 | reasoning/actions 360/360 |
| Reflexion · PlanBench mini | 0.9000 | 1.1000 | reflections 12 |
| Voyager · PlanBench mini | 1.0000 | 1.1200 | skills created/reused 12/108 |
| Tree of Thoughts · PlanBench mini | 1.0000 | 2.5000 | expanded/backtracked 1200/480 |
| LATS · PlanBench mini | 1.0000 | 4.0000 | rollouts/reflections 480/360 |
| Toolformer · ScaleMCP mini | 1.0000 | 3.0000 | accepted/candidate calls 360/540 |

稳定数据：
[`agent-mini-suites-seed42.json`](../experiments/agent-mini-suites-seed42.json)。
经典方法结果：
[`classic-agent-mini-suites-seed42.json`](../experiments/classic-agent-mini-suites-seed42.json)。

## 运行与产物

```bash
auto-research agent-eval --method voyager \
  --benchmark planbench-mini --episodes 120 --seed 42
```

产物写入 `runs/agent-research/<method>-<benchmark>-seed<seed>/`，包括逐 episode
trace、`metrics.json` 和中文 `report.md`。

## 新方法验收

新增方法必须通过单元测试、对应 mini-suite、稳定指标检查和 MkDocs 严格构建。
若论文依赖私有环境、付费 API 或人工 judge，页面必须说明未覆盖部分，并优先增加
公开 benchmark 适配器，不能用确定性任务分数冒充论文结果。
