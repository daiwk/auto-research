# 审查截至 2026-10-12：覆盖、补发现与例外

[统一状态](../../paper-discovery-watermark.json)的审查水位已推进到 **2026-10-12**，
四轨、双通道、逐ID处置与官方来源/例外清单通过 `audit_paper_coverage.py --strict`。
这是固定窗口的实际审查闭环，不是全网穷尽或全部论文实现完成。
本轮检索于2026-10-12 12:55（上海时区）启动，覆盖10月8～12日，另含公告重叠与月份编号补查；
不声称覆盖10月12日结束前尚未发布、尚未索引的内容。下一轮从10月11日重叠扫描。

## 计数口径

| 项目 | 数量 | 含义 |
|---|---:|---|
| 八组查询去重ID | 1,597 | 四研究轨道，各有submission-window与late-index通道 |
| 其中继承已审记录 | 1,019 | 不重复算作新论文或本轮原文重读 |
| 本轮新审查询记录 | 578 | 每项都有实际审查终态；有不可用原文的延期，不把它算成全文接受 |
| 查询之外定向补发现 | 10 | 冻结16项中的9篇，以及条件候选ECC；不回填查询召回数 |
| 本轮查询之外的继承记录 | 3 | 保留旧审查证明，不静默删除 |
| 完整登记集合 | 1,610 | 520接受、618审后延期、424拒绝/范围外、48已有记录 |

逐项理由、原文SHA、阅读位置与继承来源见 [paper-register.json](paper-register.json)。
“接受”是进入适合实现的队列，不意味着原模型/原环境已完整复现。
[当前实现对账](implementation-status.md)独立检查目录、可执行注册与GPU证据，
不根据接受状态推断能力提升。冻结16项的实现验收另见 [本批范围](../../design/oct12-papers-and-review.md)。

## 原文审查证据

- [工业搜广推12项](recommendation-reviews.json)：方法、生产实验和限制分别记录。
- [后训练105项](post-training-reviews.json)：公开目标与评测边界；Google LES明确延期，不按摘要缺A/B拒绝。
- [基础模型主分配139项及4项旧交叉检查](foundation-model-reviews.json)、[其余119项](foundation-tail-reviews.json)。
- [Agent 203项](agent-reviews.json)：203摘要、198有界原文核验、5原文不可用明确延期。
- 冻结短名单的独立来源：[后训练4篇](frozen-post-training-reviews.json)、[Agent/Jev 6篇](frozen-agent-reviews.json)、[基础模型/多模态5篇](frozen-foundation-reviews.json)。FORTE在工业12项中。
- [ECC条件候选](ecc-review.json)：原文真实线上点击证据成立，但私有点击数据与未发布代码/商业图像backend使当前16项之外的实现延期。

阅读边界按记录逐项标注：已读决定性方法与相关实验段落，不宣称每篇正文/附录逐段全部读完。
代码链接只作为待核查来源，不能把依赖或网页壳认作作者发布的完整实现。

## 官方机构来源

| 来源 | 本轮目录范围 | 实际核验 |
|---|---|---|
| Google Research | 28页、406条 | 398个旧URL继承证明；8个真新增URL独立核对身份/日期；已剔除Preview/JavaScript噪声 |
| Meta | 6页、144条 | 与旧基线URL集合完全一致；本轮刷新分页，继承旧审查而非重算新论文 |
| Google DeepMind | 9页、265条 | 官方日期均早于窗口，逐条时间范围核验；不是265篇算法全文重读 |

回执：[Google](google-source-review.json)、[Meta](meta-source-review.json)、[DeepMind](google-deepmind-source-review.json)、[Google新条目独立核验](google-new-entry-decisions.json)。
arXiv中的Google/Meta作者机构另由原稿反查，不仅依赖机构目录；正文生产实验优先，摘要未写A/B不构成拒绝理由。

[33项归档例外](exception-archive.json)非阻塞，仅新证据出现时重开；不能把确认属于窗口的未读候选归档来跳过审查。
严格来源穷尽水位已退休，`all_sources_exhaustive=false`、`implementation_complete=false`保持不变。

## 后续候选

新增合格线索继续保留逐项理由，不混进这次已接受的16项实现承诺。
例如Google/Meta的Self-Preservation、MetaEncoder、X-AgentRed，以及工业LLM-BlockFE，
分别需要独立的数据、评测或安全执行边界；后续按优先级分批核验，不将尚未实现的条目宣传为能力实现。
