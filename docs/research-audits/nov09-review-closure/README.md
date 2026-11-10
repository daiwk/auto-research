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

## 11 月 10 日第一轮续审

该轮补录 **70** 个原始来源决定；当时总计 **119** 个，**73** 个为高成本完整实验不复现。
这次补录包括早于窗口首次发布的论文和日终尾段；不能直接从原快照窗口内待审数中减去 70。

- [优先与工业补审](supplemental-priority-reviews.json)：按原文核对 Google、Meta 的作者归属，
  并确认[快手 WISE](https://arxiv.org/html/2611.06777v2)与[沃尔玛 BehaveRec](https://arxiv.org/html/2610.36239v1)
  正文有生产 A/B；[Meta 创作者曝光](https://arxiv.org/html/2610.38155v1)只有仿真与生产分布对照，未通过线上门槛。
- [修订版](revision-primary-reviews.json)：原先待核的 **17** 个已逐个核对固定 HTML/PDF，
  同步更新版本基线，不升级本地实现等级。另有[晚索引原文](late-index-primary-reviews.json)和
  [重点方法](continued-primary-reviews.json)的原文决定。
- [晚索引日期对账](late-index-scope.json)：原 624 条中 **395** 条只有上轮截止前的日期证据，
  在已冻结捕获中没有后续信号；仅关闭本轮日期筛查。[标题与摘要核对](abstract-scope-screen.json)
  另确认 **33** 条本轮召回为明确跨领域碰撞。两类均不写入全局论文审查账本。
- [日终尾段官方 Atom 回执](nov09-tail-source-receipt.json)：从上海时间 18:23:24 到午夜按秒去重，
  有 **122** 条此前未捕获的首发。已核对其中 **9** 条；包括
  [TS-GEAR 的生产 A/B](https://arxiv.org/html/2611.12180v1#S4.SS3)、
  [RecoGEM 的生产延迟对照](https://arxiv.org/html/2611.12296v1#S5.SS6)和
  [AgentOPSD 改写版](https://arxiv.org/html/2611.12587v1)对库内原实验的复用。

## 标题与摘要复筛

本轮新增 **142** 个原始来源决定，其中 **68** 项高成本完整实验不复现。
同一账本累计 **261** 条决定，其中 **141** 条高成本已结案。

[窗口内分流](continued-in-window-routing.json)将 22,220 条捕获观测归并为 4,941 个固定版本身份；
[晚索引与尾段分流](continued-late-tail-triage.json)另覆盖 334 个身份。
规范化标题、摘要没有给出可合并的跨 ID 精确重复。摘要中的机构名可能是引用、模型或基准名称，
只用于排序，不能证明作者归属；分流不等于原文审查。另有 [46 条窗口内](continued-in-window-scope.json)
和 **80 条**晚索引或尾段候选经明确主题与摘要核对排除出本轮范围，不写入全局论文终态。

- **Google/Meta**：[第一轮](continued-google-meta-reviews.json)、[第二轮](continued-google-meta-followup-reviews.json)
  和[第三轮](continued-google-meta-third-pass-reviews.json)结合已核对作者及官方来源反查固定原文，
  共作 51 条决定，其中 15 条确认有 Google/Meta 研究参与。
  [Google Accelerated Dataflow](https://arxiv.org/html/2610.22731v2) 的作者栏为 Google，原文是多工作者推理压测；
  [Meta PRISM](https://arxiv.org/html/2610.39175v1) 有线上训练，但效果在留出生产日志上验证，不能算生产 A/B。
- **工业证据**：[首批](continued-industrial-reviews.json)与[次批](continued-industrial-secondary-reviews.json)
  共核对 58 条固定版本。确认 [腾讯 TGR-EvoDAG](https://arxiv.org/html/2610.32326v1) 正文有 14 天、5% 的生产 A/B。
  把测得生产影响与线上日志、离线回放、仿真和排行榜分别记录。
- **方法与评测**：[重点方法](continued-method-primary-reviews.json)、[机构与生产信号](continued-signal-primary-reviews.json)
  和[晚索引/尾段原文](continued-late-tail-primary-reviews.json)单列结论。原文成本足以确认的完整实验标注不复现并结案；
  可低成本验证的核心组件只记录审查接受，本轮未实现或运行。

## 哪些还没闭环

以[去重登记和召回回执](review-inventory.json)的 `counts` 和 `pending_in_window_counts_by_title_abstract_route` 为准。
登记保留待审 arXiv ID、版本、命中轨道和上海日期，并把原快照、晚索引与尾段待审分开统计。
仍有 **4,773** 个窗口内身份、**169** 个晚索引条目、**65** 个日终补查条目未决。
`pending_revisions` 已清空的是原先识别到的修订清单，不保证后来索引的修订也已审。
`manual-review`、工业/优先原文队列、低信号候选与宽查询碰撞都是**待审状态**，不是自动拒收。
晚索引重叠项与已有论文的版本变化单独列出。只有确实尝试过仍无法确认的来源才记例外，
不拿它替代尚未审查的候选，也不把仅目录命中当作作者归属。

本 PR 的账本只写入真正已有决定的身份，不批量把未读候选记为延期、成本过高或已审。
完成剩余候选和例外对账后，再用现有审计推进统一水位。
