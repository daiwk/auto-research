# 2026-09-29 重叠窗口扫描与 RSI 专题核查

## 范围与覆盖边界

按既有四领域查询矩阵扫描 2026-09-20～09-29（含公告重叠），每查询分页最多 50 条，并与现有 adapter/审计记录去重。这里的“新候选”只是**尚未入库或终审的搜索召回项**，不等于 09-29 新发表，也不等于通过论文收录门槛；晚索引论文仍在召回集合内。

| 领域 | 检索候选 | 尚未审计候选 | 已实现 | 已审计 |
|---|---:|---:|---:|---:|
| 搜广推与 LLM 应用 | 141 | 109 | 20 | 12 |
| 基础模型 | 336 | 331 | 5 | 0 |
| LLM 后训练 | 252 | 215 | 11 | 26 |
| Agent | 296 | 292 | 1 | 3 |

四条 arXiv 查询本轮均无缓存回退，但**不能推进“全来源已覆盖”水位**。同一来源配置的直接解析复核发现：Google Research、Google DeepMind、Meta AI 官方总入口均可请求但提取 0 个 arXiv ID；RecSys 列表也为 0；SIGIR 配置实际指向 PDF，不能用 HTML 正则解析。首次复核 Google Research/Meta Research GitHub API 分别提取 8/2 个 ID，但验证性重扫时两者遇到 403 速率限制；它们不代表官方出版物入口已覆盖。此前的发现器把“HTTP 成功但提取 0”当作无异常；本轮增加每来源 `arxiv_ids_extracted`、`no_arxiv_ids` 与 `coverage_complete`，PDF 误读明确报错。重扫正确给出 `coverage_complete: false`，并记录 PDF 不兼容及 API 403。后续须补官方出版物详情页遍历或可核验的结构化 feed，再谈跨来源完结。

### 官方来源修复后的复扫（仍为部分覆盖）

发现器现读取 [Google Research 出版物列表](https://research.google/pubs/)与 [Meta AI 出版物列表](https://ai.meta.com/global_search/?content_types%5B0%5D=publication&page=1)的真实标题/详情链接，限定分页并按领域优先选择少量标题反查 arXiv；只有标题精确一致且身份唯一才关联论文。Meta 的列表发布日期另作跨月召回依据。未匹配标题、详情链接、已扫页数和标题查询失败均保留在 JSON artifact，任何一项都不能自动变成“来源覆盖完成”。2025 RecSys 静态页和 SIGIR PDF 已从**每日 HTML 来源配置**移出；它们的历史审计不删除，当前年份会议需另设可解析来源。

修复期间的 09-20～09-29 四领域重叠窗口试跑（候选数不是合格论文数）：推荐 184、基础模型 1048、后训练 542、Agent 950；Google 列表首 3 页约 45 条，Meta 首 2 页约 48 条，均为 `partial`，DeepMind 入口仍为 `no_arxiv_ids`。推荐、基础模型和后训练试跑发生在标题优先级与官方发布日期规则最终调整前，**这些数字不是最终覆盖计数**。后训练试跑从 [Meta 官方 MaD-RL 详情页](https://ai.meta.com/research/publications/mad-rl-matching-distributions-for-calibrating-llms-with-reinforcement-learning/)精确对上 [arXiv:2609.31644](https://arxiv.org/abs/2609.31644)；这只证明召回/来源归因，不代表该论文已通过复现门槛。下一步仍需补完整日期分页、DeepMind 官方详情、当前会议来源与所有未匹配条目的逐篇核查；在此之前 `cross_source.coverage_complete` 应继续为 `false`。

## 本轮全文复核后的明确项

| 候选 | 处理 | 证据及边界 |
|---|---|---|
| [FLVM / Google、YouTube](https://arxiv.org/abs/2609.32839) | P0；[公开数据概念验证](reproductions/2609.32839-flvm/README.md) | 2026-09-26 v1；论文 §4 报 YouTube Shorts 14 天线上 A/B，primary viewer enjoyment +2.67%，满足 Google 工业置顶门槛。KuaiRand-Pure 保留消费、参与、正负反馈与时间切分，但无满意度调查/生产特征，三种子结果不等于线上收益。它未被搜索摘要的 Google/Meta priority 标记可靠置顶，说明一作单位仍须全文核验。 |
| [RRSI](https://arxiv.org/abs/2609.24972) | RSI 待审候选，未建 adapter | Agent harness 的递归提案/选择机制；需要固定任务集、预算和独立回归/OOD 对照。 |
| [RSIBench-Data](https://arxiv.org/abs/2607.25886) | RSI 评测待审候选，未接入 | 测 Agent 是否继承训练反馈改进后训练数据；需公开任务与防测试集泄漏协议。 |

RSI 分类进入[自动研究与进化专题](evolution/recursive-self-improvement.md)，是跨模型、后训练与 Agent 的**实验闭环**，不复制论文原始所属领域，也不创建第七套指标索引。现有 [Recursive OPSD](reproductions/2609.30652-recursive-opsd/README.md) 仍为三种子小预算机制诊断，不能因挂入 RSI 专题自动晋级正式复现。

## 尚未收口

- 本窗口的海量候选**没有逐篇全文终审**；机器分类仅用于排队。不能把 `p2-deferred-review` 视为论文被正式拒绝。尤其要继续核对 Google/Meta 一作 affiliation 和正文线上段落，不能只看摘要或机构检索词。
- [KuaFu](reproductions/2609.31045-kuafu/README.md) 与 Recursive OPSD 的现有公开对照仍未达到原论文规模/基线，状态保留 P0 待补；本轮没有伪造独立训练或把小样本零优势更新写作 RL 成功。
- 官方页面直接 ID 提取失效、会议 PDF 源不兼容、历史未审候选都阻止本轮覆盖水位推进。下轮扫描从 09-20 重叠窗口继续，直到跨来源追踪与候选终态确实收口。
