# 2026 年历史论文扫描与实现（截至 2026-08-24）

本轮已按用户要求把冻结时间窗扩大为 **2026-01-01 至 2026-08-24**，同时扫描工业搜广推与 LLM
应用、基础模型、LLM 后训练和 Agent 四条研究线。候选发现使用项目的多查询矩阵、
跨来源配置和 canonical arXiv ID 去重；工业论文继续执行“量化线上 A/B 或明确全流量
部署”的硬门槛，Google / Meta 机构反查优先于其他来源。

完整结果分成两层：

- [历史扫描清单与 B00–B11 实现批次](paper-audits/2026-historical-scan-plan.md)：面向读者，列出全部 404 个全文候选及 70 篇固定后续实现；
- [机器可读候选全集](paper-audits/2026-historical-candidates.json)：覆盖去重后的全部 3,906 个新候选，包括查询命中、初筛桶和计划状态。

## 可复现扫描

四条研究线分别执行：

```bash
PYTHONPATH=src python scripts/discover_papers.py \
  --track <recommendation|foundation-model|post-training|agent> \
  --date-from 2026-01-01 \
  --date-to 2026-08-24 \
  --page-size 50 \
  --maximum-results-per-query 200 \
  --cross-source-config configs/paper-discovery-sources.json \
  --output paper-candidates.json
```

高召回候选池的原始规模如下。这里的“候选”只是关键词或来源命中，**不等于已满足
收录门槛**；尤其基础模型、后训练和 Agent 的宽查询会召回大量相邻工作。

| 研究线 | 原始去重候选 | 新候选 | 需全文审查 |
|---|---:|---:|---:|
| 工业搜广推与 LLM 应用 | 716 | 627 | 237 |
| 基础模型 | 1,319 | 1,303 | 42 |
| LLM 后训练 | 1,121 | 1,092 | 73 |
| Agent | 1,245 | 1,221 | 57 |

四条检索链路合计命中 4,401 次；按 arXiv ID 跨领域去重后是 4,050 篇，其中 3,906 篇尚未在仓库关闭，404 篇进入全文审查。这里明确区分“检索命中”和“符合实现标准”。

## B00 首批全文核验并实现

| 研究线 | 论文 | 入选依据 | 本地结论 |
|---|---|---|---|
| 工业搜广推 | [OneModel](reproductions/2608.18606-onemodel/README.md) | 小红书三个生产场景均披露量化 A/B | MovieLens-1M 上场景化简化实现未超过共享序列基线，负结果已保留 |
| 基础模型 | [RARE](reproductions/2608.21236-rare/README.md) | MoE 表征编辑与路由解耦机制明确、可独立验证 | 路由一致率从 82.37% 提升到 100%，同时保持目标 steering 强度 |
| LLM 后训练 | [GCPO](post-training/2608.11674-gcpo/README.md) | rollout RL 的子空间诊断与约束，可组合进 evolve | 固定算术任务代理实验最终准确率 63.28%，主方向重合移除 99.56% |
| Agent | [AUSO](agent-research/2608.21292-auso/README.md) | 动作级 JSD 驱动技能内化、探索和利用，官方代码公开 | PlanBench mini-suite 成功率持平时上下文成本下降 9.09% |
| 工业搜广推 | [ClockRoPE](reproductions/2607.26369-clockrope/README.md) | YouTube / Google DeepMind 正文披露量化线上 A/B | MovieLens-100K NDCG@10 相对 -2.30%，负结果保留 |
| 工业搜广推 | [OneShot](reproductions/2607.27475-oneshot-index/README.md) | Meta / Instagram 全流量部署并披露线上指标 | MovieLens-100K NDCG@10 相对 -7.70%，负结果保留 |
| 工业搜广推 | [NEXT](reproductions/2607.24789-next-vlm/README.md) | Meta 约一亿用户多周 A/B | MovieLens-1M NDCG@10 相对 +20.33%（单种子诊断） |
| Agent | [AgentX](agent-research/2606.26859-agentx/README.md) | Kuaishou 三周生产自迭代闭环 | PlanBench-mini 12 次完整闭环、108 次知识复用 |

每篇详情页均保存论文信息、原作者代码状态、本地 adapter/方法路径、原文关键图、
公式、论文指标、固定本地指标和复现边界。OneModel 的公开数据结果没有因低于基线而被
隐藏；这也是本轮区分“实现了论文机制”和“复现了生产收益”的关键样例。

## Google / Meta 优先反查

本轮机构优先查询额外命中 2608.18531、2608.15780 和 2608.15424。阅读全文或主题
核验后，它们不属于满足当前工业搜广推线上证据门槛的新论文，因此未进入实现队列。
摘要是否出现 A/B 没有被用作拒绝条件。

## 后续固定批次

B01–B06 依次实现工业生成推荐、多模态、搜索、广告、混排、长期价值和 Semantic ID；B07
实现基础模型架构、长上下文、KV cache 与 A/B/n 评测设施；B08–B09 实现 OPD、rubric、
外部 rollout 与多奖励 RL；B10–B11 实现 Agentic RL、长时序 credit、记忆、工具规划和
自进化。每一批的确切论文 ID 已冻结在[批次清单](paper-audits/2026-historical-scan-plan.md)。

这不意味着其余 331 个全文候选已被拒绝：它们保留为 `fulltext-review-backlog`，后续必须
写入有证据的拒绝/延期理由或晋级新的固定批次。B01–B11 及该 backlog 全部关闭后，下一轮
才恢复“只看最近日期”的增量扫描。
