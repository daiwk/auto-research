# 2026-10-16～11-09 选题审查闭环

按用户 11 月 11 日明确批准的 [P2 选题级结案口径](p2-selection-policy.json)，本窗口已闭环，
官方[审查水位](../../paper-discovery-watermark.json)推进至 **2026-11-09**。
它表示**标题摘要选题筛查 + 受保护候选原文审查**完成，不表示每篇方法已核验、实现或运行。
Google/Meta、疑似真实生产 A/B 与捕获冲突不允许由 P2 自动豁免。
下面保留推进过程中的快照；最终精确分区见[完整登记](paper-register.json)和[P2 筛查产物](p2-selection-screen.json)。
没有训练、GPU 探针或新算法交付。

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
该次快照累计 **261** 条决定，其中 **141** 条高成本已结案；后续增量见下节。

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

## 11 月 11 日：按获批口径批量结案

用户批准：标题和摘要明确表明是单一应用报告、重复评测或观点总结，且没有新的可独立复现算法或公开基准时，
可按**本窗口不收录**结案。[选择口径](batch-terminal-policy.json)不允许因为低优先级、缺代码或缺摘要 A/B 关键词排除新方法，
也不允许把摘要判断记成全文审查或高成本。

本次从原 **5,007** 条未决中完成 **648** 条：**286** 条必要原文段落审查，以及 **362** 条逐篇标题/摘要终态。
同一账本现累计 **547** 条原文决定，其中 **231** 条高成本完整实验不复现，均无自动重试或实现任务。
本次原文决定有 **143** 条接受有界核心/协议但未实现，**90** 条完整实验因原始资源配置不复现，
其余为专用资源不可用、领域外、应用报告不选或未通过工业线上门槛。没有训练、实验或 GPU 运行。

- **优先来源**：[重点原文](batch-terminal-priority-reviews.json)及[第二批](batch-terminal-priority-followup-reviews.json)
  核对作者归属与方法/实验配置。新确认 [Google 临床访前准备随机试验](batch-terminal-google-clinical-review.json)、
  [Google Urania](batch-terminal-google-urania-review.json)和[含 Google 合作者的 SPELUNKA](https://arxiv.org/html/2610.23979v2)。
  临床随机试验不是搜广推 CTR A/B；Urania 的私有对话分布分析不是新的图像生成模型。
- **生产证据**：[七项生产线索](batch-terminal-production-reviews.json)及[另一项生产经验报告](batch-terminal-production-b-review.json)
  分开记录随机 A/B、上线观测、轨迹回放和既有生产系统基线。
  DoorDash 的 feature-flag A/B 用途不是本次清理算法的随机实验；Volvo 的新配置在访谈时尚未向测试员发布。
- **重叠与尾段**：[晚索引第一批](batch-terminal-overlap-primary-reviews.json)、[第二批](batch-terminal-late-secondary-reviews.json)
  完成剩余 **169** 条；[日终尾段](batch-terminal-tail-primary-reviews.json)完成剩余 **65** 条。
  固定 HTML 不可用时补读官方固定版本 PDF，未把下载失败直接当作“高成本”。
- **摘要终态与纠错**：[A 组](batch-terminal-scope-a.json)保留 **177** 条，[B 组](batch-terminal-scope-b.json)保留 **185** 条，
  逐项有版本、捕获哈希、标题/摘要证据和理由。这些窗口级记录不进入全局实质审查账本。
  独立复核撤回 **27** 条过度排除：[3 条已读原文重新判定](batch-terminal-insurance-review.json)，
  [24 条恢复待审](batch-terminal-corrections-b-reviews.json)。不能把领域用途或负结果直接等同于“没有独立算法”。

官方目录只声明实际核对范围。后续已核对 Google 第 31 页的 9 个详情：7 篇历史论文、1 篇题外、1 篇在上海时间 11 月 10 日发布；
DeepMind 首页相对旧清单的两个身份差异也已确认为已知或历史论文。未把没有重爬的中间页记成访问故障，
也不宣称重爬全部目录。Meta 两项真实目录局限及逐条身份/文档例外保留在非阻塞例外清单。

## P2 授权后的最终闭环

上一快照的 **4,359** 条未决身份固定在[输入清单](p2-selection-input.json)，没有因结案而删除。
其中 **4,293** 条按 P2 选题级结案，另外 **66** 条完成必要原文审查；累计 **613** 条来源审查终态，
包括 **611** 条必要原文核验及 **2** 条撤稿通知/摘要范围终态，其中 **247** 条完整实验因高成本不复现。
这里的累计量包含前述历史快照，不是本轮新增论文数，也不表示通读了 613 篇全文。
逐篇记录准确版本、原始捕获/摘要哈希、主题分流和选择理由；采用可重放的自动选题规则，
**不声称人工逐篇读完全文**。明确新算法或新公共基准也可以“本窗口未纳入重点”，不能写成没有原创性。

疑似机构、生产和实际用户部署先保护，模型品牌、仿真、硬件运行或未来部署动机须有逐项上下文澄清后才移出文本保护。
[优先原文](p2-priority-primary-reviews.json)、[工业原文](p2-industrial-primary-reviews.json)、
[平台与工作流原文](p2-additional-production-reviews.json)及最后的
[工业补核](p2-residual-industrial-reviews.json)、[优先补核](p2-residual-priority-reviews.json)
记录受保护项的实际方法、线上证据、历史重刊和成本判断。
Google VeriCUA、Meta AutoRefine 与 Meta Yielding Fairness 的署名均已在原文确认；
1688 SPAR 的真实商家 A/B、Alexa 的生产路径与完整多卡训练配置分开记录。

[去重回执](review-inventory.json)中的窗口内、晚索引、日终尾段和已知修订未决均为 **0**。
八份归一化召回回执保留原查询实际边界、原触顶记录和实际拆月替代；不把传输取尽改称全文取尽。
Google/Meta 官方来源的核对范围及当前访问/分页限制见统一状态引用的来源审查与[非阻塞例外](exception-archive.json)。

P2 选择终态不写入全局实质性拒绝账本，不作为算法接受、高成本、GPU 或能力证据，也不进入实现/Evolve 队列。
后续相同版本可识别为独立的选题已审状态；新版本、元数据变化、独立优先来源/生产证据或用户新指定方向可重开。
下一轮从 **11 月 8 日**重叠扫描至新的截止时间，区分新首发、旧文补漏和修订；不承诺全网绝无遗漏。
