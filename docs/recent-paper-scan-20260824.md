# 近期论文扫描与实现（2026-08-24）

本轮冻结时间窗为 **2026-08-10 至 2026-08-24**，同时扫描工业搜广推与 LLM
应用、基础模型、LLM 后训练和 Agent 四条研究线。候选发现使用项目的多查询矩阵、
跨来源配置和 canonical arXiv ID 去重；工业论文继续执行“量化线上 A/B 或明确全流量
部署”的硬门槛，Google / Meta 机构反查优先于其他来源。

## 可复现扫描

四条研究线分别执行：

```bash
PYTHONPATH=src python scripts/discover_papers.py \
  --track <recommendation|foundation-model|post-training|agent> \
  --date-from 2026-08-10 \
  --date-to 2026-08-24 \
  --page-size 50 \
  --maximum-results-per-query 200 \
  --cross-source-config configs/paper-discovery-sources.json \
  --output paper-candidates.json
```

高召回候选池的原始规模如下。这里的“候选”只是关键词或来源命中，**不等于已满足
收录门槛**；尤其基础模型、后训练和 Agent 的宽查询会召回大量相邻工作。

| 研究线 | 去重候选 | 新候选 | 已实现/已审 |
|---|---:|---:|---:|
| 工业搜广推与 LLM 应用 | 74 | 68 | 6 |
| 基础模型 | 505 | 502 | 3 |
| LLM 后训练 | 162 | 161 | 1 |
| Agent | 430 | 428 | 2 |

## 本轮全文核验并实现

| 研究线 | 论文 | 入选依据 | 本地结论 |
|---|---|---|---|
| 工业搜广推 | [OneModel](reproductions/2608.18606-onemodel/README.md) | 小红书三个生产场景均披露量化 A/B | MovieLens-1M 上场景化简化实现未超过共享序列基线，负结果已保留 |
| 基础模型 | [RARE](reproductions/2608.21236-rare/README.md) | MoE 表征编辑与路由解耦机制明确、可独立验证 | 路由一致率从 82.37% 提升到 100%，同时保持目标 steering 强度 |
| LLM 后训练 | [GCPO](post-training/2608.11674-gcpo/README.md) | rollout RL 的子空间诊断与约束，可组合进 evolve | 固定算术任务代理实验最终准确率 63.28%，主方向重合移除 99.56% |
| Agent | [AUSO](agent-research/2608.21292-auso/README.md) | 动作级 JSD 驱动技能内化、探索和利用，官方代码公开 | PlanBench mini-suite 成功率持平时上下文成本下降 9.09% |

每篇详情页均保存论文信息、原作者代码状态、本地 adapter/方法路径、原文关键图、
公式、论文指标、固定本地指标和复现边界。OneModel 的公开数据结果没有因低于基线而被
隐藏；这也是本轮区分“实现了论文机制”和“复现了生产收益”的关键样例。

## Google / Meta 优先反查

本轮机构优先查询额外命中 2608.18531、2608.15780 和 2608.15424。阅读全文或主题
核验后，它们不属于满足当前工业搜广推线上证据门槛的新论文，因此未进入实现队列。
摘要是否出现 A/B 没有被用作拒绝条件。

## 尚未宣称闭环的范围

上述千级候选池是高召回 artifact，不是已逐篇阅读全文的全域闭环账本。本轮只把四条
研究线中机制清晰、证据充分且能形成非占位实现的代表性新论文写入终态；其余新候选
仍属于后续增量审阅池。后续批次必须继续从 artifact 与统一 manifest 的差集开始，不能
把本页解读成“时间窗内所有候选均已拒绝或实现”。
