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
