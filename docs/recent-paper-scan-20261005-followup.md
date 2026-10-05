# 2026-10-05：重叠窗口继续扫描（来源未闭环）

接续 [10 月 5 日定向复核](recent-paper-scan-20261005.md)，仍从 **2026-10-01** 重叠检查；上次完整水位 **2026-10-02** 不变。本轮用官方 arXiv API、论文全文、作者仓库，以及 Google Research、Google DeepMind、Meta 的官方来源；未用 DeepXiv。

## 已完成与未完成的覆盖

| 来源 / 轨道 | 本轮状态 | 对结论的影响 |
|---|---|---|
| arXiv：后训练、基础模型 | 批量分页完成；部分 ID 回查遇到 429 | 可核对这些轨道的窗口候选，不能替代机构反查 |
| arXiv：Agent、搜广推 | 批量请求遇到 HTTP 429，未完成分页 | **不能宣称四轨完整扫描**；下轮需重试 |
| Google Research、Meta 官方页面 | 请求超时 | **不能宣称最高优先级机构已排除遗漏** |
| Google DeepMind 官方页面 | 可读但交叉核对不完整 | 仍需连同上述机构重新复核 |

扫描器的 `new` 原始计数还含按 arXiv ID 月份召回的旧稿和不相关领域，**不是 10 月 2 日新发或符合收录门槛的论文数**。只有全文和证据门槛核验后才列为实施候选。由于来源未闭环，`coverage_complete=false`，不推进水位；下一轮继续从 10 月 1 日开始。

## 本轮实现

| 论文 | 机制与本地证据 | 边界 |
|---|---|---|
| [Follow the Winners](post-training/2610.03361-follow-the-winners/README.md) | FIFO replay、重复 minibatch top-$K$、带 KL 的交叉熵投影；三 seed CPU bandit 机制诊断 | L1；非论文 Search-R1/Sokoban 结果，无 LLM 训练或能力晋级 |
| [AdaStep](agent-research/2610.03223-adastep/README.md) | 锚点状态内按动作分组的方差归因与步级 credit；三 seed 合成回报诊断 | L1；无真实 Agent 策略训练或任务成功率比较 |

两篇均为 arXiv v1 **2026-10-02 提交、10 月 5 日公告**；不是数小时内出现的两个新研究方向。详情页明确区分论文结果与本地诊断指标。

## 全文门槛与待处理候选

- [AIMS（Meta）](https://arxiv.org/html/2610.02600)：已查全文实验与部署叙述，找到离线 Recall/NDCG 和工业日志数据，**未找到生产线上随机 A/B 或全流量效果证据**。因此不纳入工业搜广推实现队列；不是仅凭摘要拒绝。
- [Pivot-SD](https://arxiv.org/html/2610.03665)：需要真实 LLaDA 式去噪轨迹及训练流程；没有用采样启发式替代核心算法。
- [RC-OPD](https://arxiv.org/html/2610.03515)：作者仓库目前公开 checkpoint/评估结果，但注明代码待评审后发布；真实学生首错修复、教师继续 rollout 与同预算基线待验证。
- [DepGPO](https://arxiv.org/html/2610.03634)：真实终端读写依赖图、verifier 读取集合、策略更新和无金标泄漏门槛待验证。
- [Recursive Harness Self-Improvement](https://arxiv.org/html/2610.03548)：真实 generator、固定 verifier 和同 cohort 成本门槛待验证。
- [KV²](https://arxiv.org/html/2610.03198)：有[作者代码](https://anonymous.4open.science/r/KVsquared-0B97/)；若实现或升级 CUDA 声明，先在 A100/A30 执行并提交脱敏回执。

这些是**待审候选，不是已实现或已通过门槛**。下轮先补 Agent/搜广推分页及 Google/Meta 官方机构反查，再按证据与复现忠实度排序；避免把扫描中断误写成“没有新论文”。
