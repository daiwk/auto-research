# 2026-10-16～11-09 审查补齐（进行中）

这批完成了召回覆盖对账和一组优先原文审查，但**还没有完成全窗口逐项决定**。
官方审查水位仍是 [2026-10-15](../../paper-discovery-watermark.json)；
11 月 9 日是本轮拟收口日期与召回窗口的上界，不是已完成的水位。没有训练、GPU 探针或新算法交付。

## 已补的召回和优先证据

复用三轮真实 GitHub 扫描：[10 月 22 日](https://github.com/daiwk/auto-research/actions/runs/39731868655)、
[10 月 29 日](https://github.com/daiwk/auto-research/actions/runs/40832864995)、
[11 月 9 日](https://github.com/daiwk/auto-research/actions/runs/42582487347)。
四轨两通道、共 24 份输出覆盖目标日期和 10、11 月编号；保留原查询范围、候选数、来源运行与哈希。
最后一轮基础模型 `LLM` 晚索引原查询在 2,000 条触顶，**没有改写原回执**。
实际按两个月拆开查询，10 月 **2,098** 条、11 月 **368** 条，均取尽且没有缓存回退。
11 月 9 日 CI 捕获的 [arXiv 官方公告](https://arxiv.org/list/cs.AI/new) 已更新到当日；
公告日、原文 v1 提交、原文版本与本轮审查时间不混用。

[Google/Meta 优先审查](priority-primary-reviews.json)保存官方目录范围、逐条变化及原文决定。
[Meta Axia](https://arxiv.org/pdf/2611.05643v1) 正文 §6 将线上指标与真实流量 A/B 和既有生产模型配置相连，
但这不等于开源复现；[Google Busy Beaver](https://arxiv.org/html/2610.22603v1)、
[TURTLE](https://arxiv.org/html/2610.27307v2)、[Muir](https://arxiv.org/pdf/2611.08376v1) 与
[VERID](https://arxiv.org/pdf/2610.32755v1) 也补上了具体原文和资源依据。
[工业证据核查](industrial-primary-reviews.json)分开保存通过线上门槛、仅离线、旧文补漏和原文访问例外。
[其它重点方法](additional-primary-reviews.json)涵盖 FP4 解码、RSI 和 OPD。正文证据只覆盖列出的段落，
不宣称整篇通读。高成本且已有依据的完整实验记为 **不复现（审查 DONE）**，不重试、不进实现队列。

## 哪些还没闭环

以[去重登记和召回回执](review-inventory.json)的 `counts` 和 `pending_bucket_counts` 为准。
这份登记保留待审 arXiv ID、观测版本、命中的轨道、上海日期及第一轮分流结果。
`manual-review`、工业/优先原文队列、低信号候选与宽查询碰撞都是**待审状态**，不是自动拒收。
晚索引重叠项与已有论文的版本变化单独列出。只有确实尝试过仍无法确认的来源才记例外，
不拿它替代尚未审查的候选，也不把仅目录命中当作作者归属。

本 PR 的账本只写入真正已有决定的身份，不批量把未读候选记为延期、成本过高或已审。
完成剩余候选决定、修订版核对及例外对账后，再用现有严格审计推进统一水位。
