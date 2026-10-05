# 2026-10-05：新公告定向复核（未完成全来源覆盖）

本轮接续 10-02 watermark，从 10-01 重叠窗口核查。官方 arXiv 的 cs.LG、cs.CL、cs.AI、cs.IR 近期列表在 10 月 5 日已有新公告；其中本页核查的 v1 实际提交日是 **10 月 2 日**，并非“几小时内新发多篇”。[cs.LG](https://arxiv.org/list/cs.LG/recent) · [cs.CL](https://arxiv.org/list/cs.CL/recent) · [cs.AI](https://arxiv.org/list/cs.AI/recent) · [cs.IR](https://arxiv.org/list/cs.IR/recent)。没有使用 DeepXiv。

仓库四领域扫描器的 recommendation 轨在 arXiv 批量 API 的首批请求中长时间等待，已中止；其余三轨及 Google/Meta 官方站点没有完成完整分页复核。因此 `coverage_complete=false`，**不推进 watermark 2026-10-02**，下轮仍从 10-01 复核。网页定向阅读不等于四领域高召回扫描完成。

## 本轮已执行

- [LESSER](post-training/2610.03702-lesser/README.md)：输出层解析梯度、共享双侧 Rademacher 投影、round-robin 选择器；三 seed CPU 自动微分恒等式检查。仅 L1 诊断，不声称真实 LLM 后训练或论文速度收益。原文一作单位 University of Pennsylvania；全文未找到作者代码链接。

## 已见但未晋升为“已实现”

| 论文 | 当前判断 | 下一道门槛 |
|---|---|---|
| [Recursive Harness Self-Improvement](https://arxiv.org/abs/2610.03548) | RSI/Agent 数据生成候选；原文需固定 verifier、真实 generator 与同 cohort 成本门槛 | 先核可用代码/模型及公开题目，不能用静态脚本冒充自主进化 |
| [RC-OPD](https://arxiv.org/abs/2610.03515) | 后训练候选；要定位学生首错、修复并让学生继续 rollout | 需真实学生/教师与纠错轨迹、同预算基线；CUDA 声明前跑 A100/A30 |
| [DepGPO](https://arxiv.org/abs/2610.03634) | Agentic RL 候选；依赖终端执行读写图与 verifier 实际读取资源 | 需可审计 terminal trace、无金标泄漏和真实策略更新 |
| [AIMS](https://arxiv.org/abs/2610.02600) | 工业推荐+LLM 候选；摘要只列离线 Recall/NDCG | 必须读完整论文的生产 A/B/全流量证据；没有则不进入工业实现队列 |

Google/Meta 继续置顶，但**本轮机构来源未完成**，不能推断 10-01 至今没有其合格新论文。上述候选优先级尚未正式终态；下轮要补完整来源与全文，避免把迟公告和漏项误记成新发表。
