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

### 后续来源解析补强（仍非覆盖完成）

现已接入 [Google DeepMind 出版物列表](https://deepmind.google/research/publications/)的标题、详情页和列表日期，以及 [RecSys 2026 海报页 1](https://recsys.acm.org/recsys26/posters-1/)、[页 2](https://recsys.acm.org/recsys26/posters-2/)、[页 3](https://recsys.acm.org/recsys26/posters-3/)和 [SIGIR 2026 官方录用名单](https://sigir2026.org/en-AU/pages/program/accepted-papers)的标题。用真实官网页面做过解析核验：DeepMind **当前首页** 30 条，RecSys 三页 46/44/42 条，SIGIR 各轨道（含全文、短文、工业、资源、演示等）去重后 667 条。这些是**页面标题数，不是新论文数或合格论文数**；SIGIR 页面没有逐篇链接，记录指向官方名单页，RecSys 海报条目指向页面内对应 accordion，均待与原论文一一核对。会议举办日期不冒充论文首次发布日期。会议列表中的 arXiv 引文也不能当作该条海报的论文 ID，只有已知论文或 arXiv 精确标题且唯一匹配才关联。

DeepMind 官网偶发返回 gzip 压缩正文但未以可直接解码的文本呈现，抓取器现识别 gzip 头并解压。此阶段来源仍标记 `partial`：当时 DeepMind 仅首页、RecSys 仅海报，SIGIR 标题与原文身份也未逐篇终审；标题反查受每来源预算限制。`cross_source.coverage_complete` 保持 `false`。以下记录后续补齐分页和正式场次的进展，但不改变逐篇核验全文部署证据的要求。

### 09-29 再次收口：分页、会议场次与待审队列

[Google DeepMind 出版物列表](https://deepmind.google/research/publications/)的实际分页路径是 `/research/publications/page/N/`；发现器现从首页读取末页，并受配置上限约束逐页抓取。真实页面核验时首页声明 9 页，九页分别解析出 30/30/30/30/30/30/30/30/24 个页面条目。此数是**列表条目数**，既未跨页按论文身份去重，也不表示符合本库门槛。现还补入 [RecSys 2026 正式程序](https://recsys.acm.org/recsys26/recsys-26-program/)链接的八个 session 页；真实页面依次解析出 14/13/14/14/14/12/13/14 个条目。它们可能与海报重复，不能直接相加成唯一论文数。

每日扫描额外产出 `paper-official-review-<track>.json`：把官方列表中尚未匹配到唯一 arXiv 身份的标题、详情链接和机构集中保存，Google/Meta 来源优先；相同规范化标题只形成**待审组**，不自动认定为同一篇论文。已收录论文通过 manifest 的精确标题匹配标记，避免重复排队。GitHub API 请求在 Actions 中使用仓库作用域 `GITHUB_TOKEN`，只发送至 HTTPS `api.github.com`。某一分页临时失败会留下显式失败记录并保留其他已抓页面，不会虚报完整覆盖。

本次 source-only 复核中，Google Research 官方页请求超时；它不是“无新论文”的证据，也没有被标记为覆盖完成。Meta 官方页和 GitHub API 的动态可用性同样需由每日 artifact 核对。未匹配标题仍须逐篇查原文身份、一作机构和全文线上证据；历史大队列没有因此获得终审状态，`cross_source.coverage_complete` 继续保持 `false`。

### 09-30 合并后扫描失败与修复

[首次合并后四领域工作流](https://github.com/daiwk/auto-research/actions/runs/36600018480)全部在 arXiv 查询阶段收到 HTTP 429，因而没有生成可审核的候选 artifact；这**不是零候选**。根因是四个 matrix job 并发运行，虽然每个客户端内部间隔三秒，但总体仍违反 [arXiv legacy API 的单连接、每三秒至多一请求限制](https://info.arxiv.org/help/api/tou.html)。后续工作流将四个领域串行调度，并把扫描专用的限流重试延长到最多五次；429 仍须显式失败，不能退化为空结果。修复合并后需重新运行并审核四领域 artifact，才进入下一批论文收录。

[修复分支的四领域验证运行](https://github.com/daiwk/auto-research/actions/runs/36601663347)已全部成功。四个领域均由 arXiv 实时页面生成产物，`cache_fallback_pages` 为 0、`arxiv_transport.coverage_complete` 为 `true`，证明串行调度与全局三秒节流消除了本次并发 429。验证产物的规模如下；这里的“新”仍指**尚未入库或终审**，不是本日新发表或已通过复现门槛。

| 领域 | 检索候选 | 尚未审计候选 | 已实现 | 已审计 | 官方待核身份 |
|---|---:|---:|---:|---:|---:|
| 搜广推与 LLM 应用 | 184 | 127 | 22 | 35 | 1192 |
| 基础模型 | 1048 | 951 | 20 | 77 | 357 |
| LLM 后训练 | 542 | 450 | 22 | 70 | 352 |
| Agent | 950 | 846 | 19 | 85 | 355 |

四条产物的 `cross_source.coverage_complete` 仍为 `false`：Google、Meta、DeepMind 与会议官网条目有大量标题身份尚未解析，不能因 arXiv 通道恢复而宣称跨来源扫描完结。推荐轨道机器规则标出的 4 个“Google/Meta”命中均为关键词误召回，不代表机构归属；本轮没有把它们晋级为优先论文。Meta 官方队列中的 MaD-RL 已在前述复核中关联到 arXiv:2609.31644，仍须按后训练论文门槛独立处理。

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
