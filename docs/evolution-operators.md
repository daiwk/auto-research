# Evolve 组件兼容图

Evolve 的候选不再只是字符串列表。所有从论文映射出的结构、训练目标、数据策略、记忆、规划、工具、critic、policy 和恢复策略都进入统一 `OperatorSpec` registry，并声明以下约束：

- 来源论文与研究领域；
- 可用模型和 genome 槽位；
- 前置依赖与显式冲突；
- 是否允许与同槽组件组合；
- 相对 compute、memory、latency 成本。

规划器在形成候选集时先经过兼容过滤，避免把推荐结构接进纯 LLM、把 Agent 记忆算子接进后训练 objective，或在同一非组合槽同时选择互斥方法。

## 使用方式

```bash
# 浏览全部论文算子
auto-research operators list

# 验证组合与资源预算
auto-research operators check \
  --model agent \
  --operators memory:u-mem,planner:react,tool:toolformer \
  --max-compute 6 --max-memory 6 --max-latency 6

# 导出机器可读图，供看板或外部候选生成器使用
auto-research operators export --output runs/operator-graph.json
```

Agent 的 `memory/planner/tool/critic/policy/recovery` 是不同槽，可以组合；DPO 与 GRPO 都占用后训练 `objective` 槽，直接并列会被拒绝。未知的本地候选仍可在单算子模式下验证，但必须经过候选 staging、确定性测试和人工 promotion 才会成为已安装论文算子。

## 与实时检索的边界

实时检索论文只产生 `retrieved-design-only` 候选，不会因为标题相似就进入可执行图。只有仓库已经实现并映射的论文算子，或通过 candidate promotion 的代码，才带有可执行来源和兼容契约；因此报告会区分“来自已实现论文”“实时检索启发”和“本轮组合假设”。
