# 2026-10-06：10 月重叠窗口补扫与 DepGPO 机制落地

本轮接续 [10 月 5 日的未闭环扫描](recent-paper-scan-20261005-followup.md)，从 **2026-10-01** 重叠复核，仍把最后完整水位保留在 **2026-10-02**。使用 arXiv 官方 API、论文全文与 Google/Meta 官方来源；未用 DeepXiv。

## 覆盖与计数解释

| 轨道/来源 | 本轮结果 | 仍未完成 |
|---|---|---|
| 搜广推 arXiv | 分页请求成功；窗口内未审标题 2 篇，均不符合当前工业系统论文范围 | Google Research 3 页、Meta 2 页官方目录请求超时；无法宣称机构反查完成 |
| Agent arXiv | 分页请求成功；宽查询召回窗口内未审 48 篇 | 48 是**标题召回数**，混有机器人、应用、安全与评测；尚未逐篇全文审计，不能叫“48 篇待实现” |
| 基础模型、后训练 | 接续上一轮已完成的 arXiv 分页，并复核本轮重点候选的官方全文 | 当前尚未重新完成全来源机构对账 |
| Google DeepMind、Google/Meta 官方网页 | DeepMind 可读；Google Research 与 Meta 目录在扫描器中超时，浏览器可打开部分结果 | 只能做定向交叉核查，不能推进四轨总水位 |

扫描器的“新候选”是仓库尚未审计的查询命中，还包含晚索引或历史论文。按 arXiv v1 的实际提交日期核对，不能把一次 429 重试后的批量结果说成“今天新增”。本轮详细机器输出在本地扫描回执；网页只保留人工核查结论。

## 本轮落地

- [DepGPO](agent-research/2610.03634-depgpo/README.md)（arXiv v1 2026-10-02）：实现结构化 trace 的读写图、verifier 相关写入、支持性读取、步级与 token 级优势归一化；手工 trace 和属性测试通过。**L1 机制诊断**，没有真实终端 tracer、Qwen 策略训练或 Terminal-Bench 增益。完整复现缺口保留。
- [Meta AIMS](https://arxiv.org/html/2610.02600)：此前已查正文，只有离线工业日志结果，未核实生产线上 A/B 或全流量效果；本轮未改变其工业收录结论。

## 下一轮应优先全文审计的候选

这些是**候选，不是已实现**，按项目方向和可验证性排序：

1. [FrugalEvo](https://arxiv.org/html/2610.03675)：有[作者代码](https://github.com/chchenhui/frugalevo)，成本预算、强模型提策略/弱模型写代码、BA-AUC 与共享前缀缓存直接契合 Evolve；下一步需固定模型调用成本和公开任务，不能仅复用 BA-AUC 公式冒充完整进化。
2. [Sentry](https://arxiv.org/abs/2610.02994)：条件触发的失败恢复、只在成功恢复后写经验；需要真实失败检测、隔离测试任务及无 reward 泄漏评测。
3. [Dynamic Expert Pruning](https://arxiv.org/abs/2610.02951)：按 Agent 提示动态裁剪 MoE 专家；需要真实 MoE 权重、预测器训练与质量/显存/延迟对照；若声明 CUDA，必须先在 A100/A30 验证。
4. [RC-OPD](https://arxiv.org/html/2610.03515)、[Recursive Harness Self-Improvement](https://arxiv.org/html/2610.03548)、[Pivot-SD](https://arxiv.org/html/2610.03665)、[KV²](https://arxiv.org/html/2610.03198)：沿用上轮的完整机制与数据/GPU 门槛，不降级成占位实现。

后续继续从 10 月 1 日重叠补查 Google/Meta 官方来源和上述全文；只有全来源核验完成后才推进水位。近期新论文则从最后**已审日期**增量扫描，而不是从“上次发 PR 的日期”推断已覆盖。
