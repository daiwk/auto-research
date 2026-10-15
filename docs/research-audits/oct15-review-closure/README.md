# 2026-10-13～10-15 审查收口

审查水位推进至 **2026-10-15**。这是截至 [本次状态的 `review_as_of`](../../paper-discovery-watermark.json)
的有界审查，不是未来整天、全网或全站无遗漏的保证，也不代表论文全部实现。
本 MR 只做审查、证据整理和校验：没有训练、GPU 探针、大权重下载或新算法实现。

高成本候选按用户要求记为 **成本过高，不复现（审查 DONE）**：保存原文配置、成本依据和单卡预算，
不进入自动重试、实现或执行型 evolve 队列，不再作为待算力的 TODO。
“无法用便宜只读核对确定完整成本”与“原文实报多卡/数小时”分开记录，均不是本机实测。
尚可负担的候选只表示审查接受，**本轮未实现**；后续若做，应另定小而忠实的验收范围。

## 这次到底处理了多少

<!-- closure-summary:start -->
| 项目 | 数量 | 实际含义 |
| --- | ---: | --- |
| 配置召回去重身份 | 3,742 | 不是合格论文数，也不是全文数 |
| 新登记、窗口内首发 | 794 | 依据 arXiv `published`，不是公告或目录日期 |
| 新登记、历史/重叠 | 1,320 | 日期/范围分流，或明确单列的旧文补复核 |
| 已有身份 | 1,628 | 继承旧决定，不重复算新审全文 |
| 已知身份最新版本另审 | 11 | 已包含于已有身份，不另加总 |
| 非 arXiv 官方身份 | 2 | CATWILD / Meta AutoformBench；不伪造 arXiv 或首发日 |
| 高成本不复现、审查完成 | 383 | 包含重点补发现/修订版，不是未完成训练 TODO |
| 可负担的审查接受 | 14 | 未实现、无新实验、不自动执行 |
| 非阻塞来源例外 | 37 | 官方日期/身份/分页与2项有界原文例外 |
| 本轮新增论文实现 / GPU 训练 | 0 | 不把审查完成当作实现完成 |

截至时间：`2026-10-15T15:39:55+08:00`；[完整登记](paper-register.json)含 3,744 个唯一身份。
<!-- closure-summary:end -->

宽查询会包含数学、临床、传统控制等范围外文章；它们不是“新增合格论文”。
794 条是此前未登记、且首发日期在本窗口的记录；另有 1 条窗口首发已有记录，未重复计新。
历史/重叠项可以只完成身份、日期和摘要范围分流，不冒称本窗口新论文的算法全文审查。
每条都保留实际读法：摘要初筛、指定方法/评测/资源段落、或继承旧决定；没有整篇通读声明。

- [P0/P1 与低成本候选的可读清单](priority-decisions.md)：逐篇中文理由、成本与版本边界。
- [完整去重登记](paper-register.json)：所有召回身份、决定、来源回执和非阻塞原文例外。
- 领域决定：[搜广推](recommendation-reviews.json)、[基础模型/多模态](foundation-model-reviews.json)、
  [后训练](post-training-reviews.json)、[Agent/RSI](agent-reviews.json)。
- [根代理独立重点复核](root-priority-reviews.json)、[已知论文的最新版本复核](revision-reviews.json)。
- [非阻塞例外清单](exception-archive.json)、[目录/实现独立对账](implementation-status.md)。

## 召回如何闭环

四个研究轨道各有日期窗口与月份编号晚索引两通道，共八份回执。
复用的是[本日实际扫描运行](https://github.com/daiwk/auto-research/actions/runs/38689269736)
已取尽的包含范围，再明确派生 10-13～10-15 的审查子集；**没有把原查询日期改窄，冒充重新查询**。
每份回执保存原始 artifact 文件名、SHA-256、原请求窗口、实际查询边界和过滤规则。
提交回执去除了重复摘要正文，保留逐 ID 的日期、版本、查询命中与原始元数据指纹。

基础模型的跨 9～10 月 `LLM` 宽查询确实触顶，不能直接当作完成。
本轮实际补跑相同词的 **10 月编号范围**，上限 4,000、每页 100，取尽 **1,088** 个唯一身份；
原触顶回执与替代回执同时保存。这 1,088 条不是新首发数量，更不是合格论文数量。
最终八份回执均无未解决的触顶、失败或缓存回退。

| 轨道 | 日期窗口回执 | 晚索引回执 |
| --- | --- | --- |
| 搜广推 | [submission](recommendation-submission-window-retrieval.json) | [late-index](recommendation-late-index-retrieval.json) |
| 基础模型 | [submission](foundation-model-submission-window-retrieval.json) | [late-index](foundation-model-late-index-retrieval.json) |
| 后训练 | [submission](post-training-submission-window-retrieval.json) | [late-index](post-training-late-index-retrieval.json) |
| Agent | [submission](agent-submission-window-retrieval.json) | [late-index](agent-late-index-retrieval.json) |

## Google / Meta 与官方目录

Google/Meta 工业论文仍最高优；先按机构和主题召回，再检查正文业务线上 A/B/全流量证据，
不要求摘要出现 A/B。新目录 URL、旧 URL、旧首发和新版本分开处理。

| 官方范围 | 页面 | 记录 | 新详情 URL | 继承记录 |
| --- | ---: | ---: | ---: | ---: |
| [Google](google-source-review.json) | 28 | 412 | 7 | 405 |
| [Meta](meta-source-review.json) | 6 | 144 | 11 | 133 |
| [Google DeepMind](google-deepmind-source-review.json) | 9 | 265 | 0 | 265 |

旧 URL 与规范化题名一致的记录继承原决定；本次目录日期另行核对，不等于重读了 803 篇原文。
Meta 只是前六页的有界范围，不声称分页穷尽。目录更新日、文稿日期、软件引用日期与首次公开日
不是同一个字段，不能互相替代。

几个容易误判的例子：

- **Google G→W→L 级联**：正文比较训练稳定性、AUC/RMSE，没有该方法量化业务 A/B；不因 Google 署名绕过工业门槛。
- **CASI**：正文生产 A/B 通过，但生产回放/完整训练资源未公开，单卡可忠实复现的成本仍不确定；P0、不复现、审查完成。
- **DRanker**：首发 10-11，属旧文补发现；正文明确全球 A/B 与后续 holdout，不能漏掉，也不能把数亿私有样本装成公开复现。
- **PsyBer-Agent / AdCoEvo**：分别是固定后端人/模拟用户一致性、AuctionNet 模拟器，不当作生产推荐业务 A/B。
- **Meta AutoformBench**：与文档理解同名论文不是同一身份；官方页 10-13、PDF 文稿日期 10-05、软件引用日期 09-30 的语义不同，首公开日保留例外。
  其每题 \$200 是最高上限，不是所有题实际花费；341 题、9 个 frontier agent 的完整研究不在本轮复现。
- **Human-Guided Agentic EHR**：已看 PDF 关键方法/限制；原文不主张新 Agent 架构或独立 AI 能力 benchmark，不把临床病例研究算新算法。

## 修订版不能自动升级旧实现

[11 篇已知论文的最新版本复核](revision-reviews.json)独立于“新增论文”统计。
缺少旧版本语义基线时，只声明读过当前版本指定段落，不虚构精确 algorithm diff。

- **Dice Roll v2**：原文承认合成数据覆盖及错误计数字段，撤回固定次数 tiers；应先 pilot 再用方差分量求次数。
  仓库并无该算法实现，本次保留旧快照并新增勘误，不继续传播固定次数建议。
- **SPARK v2 / 旧 SpecRoll**：低秩 logit correction 与旧 fast/slow 路径不是改名关系；[旧论文页](../../post-training/2608.04962-specroll/README.md)
  已明确仅对应 v1，不声称 v2 已实现。
- **Rubric Dropout v2、RIDE v2、UniRec v5**：最新方法/资源与限制另记；旧 L1/公开小实验不自动覆盖新版全方案或生产收益。

版本登记目前共 434 项，其中本轮 383 项只登记历史身份/日期和已观察版本，另有成本或来源例外的有界记录。
这些范围字段写在 [版本基线](../../paper-discovery-versions.json)中，**不是 434 篇算法全文验收**；
目的之一是让相同版本不因“缺少旧全文基线”每轮反复排队，真正的新版本/元数据证据仍可触发复核。

## 例外与后续扫描

真正读不到的原文保留版本、URL、HTML/PDF 实际错误或本轮读取上限，不能接受为已阅读全文。
身份/日期/分页不确定项和这些原文例外统一非阻塞归档；未读、触顶和缺少决定的候选不能借例外消失。
只有独立新证据才重开来源例外；高成本复现则还需要用户获知成本后明确重开。

下一轮从 **10-14 重叠到新的截止时间**。本轮是 10-15 日内截至时间，之后提交/公告或晚索引的内容
由重叠扫描补入；新首发、晚发现旧文、修订版继续分开汇总。

本轮验证项目与实际结果见[交付记录](../2026-10-15-review-closeout.md)；机器验收入口为
`python scripts/audit_paper_coverage.py --strict`、相关回执回归、独立实现对账和严格文档构建。
