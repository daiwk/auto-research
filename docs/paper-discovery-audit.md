# 论文发现闭环与防遗漏审计

过去出现大量遗漏，不是某一个关键词没搜到，而是流程只做了“增量发现”，没有做
“候选全集闭环”：搜索范围、四条研究线、线上证据、代码可得性、已实现去重和明确
排除项没有落到同一份可机器检查的账本里。结果是每次回答了“这一批找到什么”，却
没有回答“固定时间窗内还有什么没有处理”。

从 2026-08-08 起，新增论文批次必须执行下面的闭环，不能只更新 README：

1. **冻结范围**：记录检索截止时间、时间窗、四个领域（工业搜广推与 LLM 应用、
   基础模型、后训练、Agent）、每个领域的二级主题和 P0/P1 口径。全域批次必须声明
   `scope_kind: global` 与 `required_subtopics`，不能再用“每个领域搜到几篇”代替覆盖审计。
2. **多路发现**：arXiv 分类与关键词、Google/Meta/ByteDance/Alibaba/Kuaishou 等
   机构反查、已纳入论文的 related work / 引用链、原作者主页与官方仓库四路取并集。
3. **证据归档**：工业论文必须记录量化线上 A/B 或用户认可的全流量证据；其他领域
   记录公开 benchmark、同预算对照、代码状态和可在本地执行的核心机制。
4. **稳定去重**：按 arXiv ID、正式论文 ID、标题规范化三层去重，并与 adapter、
   后训练 method、Agent method 和 evolve mutation 四个 registry 交叉比对。
5. **逐项终态**：账本内每项只能是 `implemented`、`deferred` 或 `rejected`；后两者
   必须写原因。P0/P1 只要还有无终态条目，批次就不能宣称完成。
6. **实现验收**：代码路径、论文特有 telemetry、固定指标、完整中文论文页、原文关键图、
   分类目录、evolve 映射（适用时）和单测必须同时存在。
7. **结束审计**：运行 `python scripts/audit_paper_coverage.py --strict` 和全量测试；
   PR 描述列出候选总数、实现数、延期数、排除数及原因。

## Google / Meta 最高优先级规则

Google（含 Google DeepMind、YouTube）和 Meta（含 Instagram）是工业搜广推与 LLM
应用论文的最高优机构。只要论文属于当前研究范围，并满足“量化线上 A/B”或用户认可的
“统计显著且明确全流量部署”证据，必须标为 `P0`，不能因为同一子主题已有其他论文而跳过。

机构优先批次必须使用 `scope_kind: institution-priority`，在 ledger 中同时保存：

- Google、Meta 两家各自的机构/产品检索语句；
- 检索命中的全部 candidate ID；
- 每项的机构、线上证据门槛、P0 原因和最终状态。

`audit_paper_coverage.py --strict` 会检查上述字段和候选闭环。arXiv API 不提供作者单位，
因此机构反查不能只搜 API 元数据：必须读取论文首页 affiliation，并同时覆盖 `A/B`、
`live launch`、`full traffic`、`fully deployed` 等证据措辞。2026-08-09 的纠错批次由
TokenMinds（Google/YouTube）和 SlimPer（Meta/Instagram）触发。

候选召回与线上证据判定必须分成两步：先仅按**作者机构 + 搜广推/LLM 应用主题**形成
候选全集，再逐篇检查 PDF/HTML 全文。摘要中是否出现 `A/B` 不得影响候选召回；摘要、
标题和 arXiv API 元数据也不能单独作为“不满足线上门槛”的拒绝依据。机构优先批次若未
声明 `candidate_discovery_gate: affiliation-and-topic`、
`abstract_online_evidence_required: false`、`full_text_review_required: true`，或候选未记录
正文证据章节和命中措辞，严格审计直接失败。SlimPer 就是该规则的回归样例：摘要只写
部署收益，正文 §4.3 才明确写 A/B、全流量与统计显著性。

当前闭环批次的机器可读账本是
[`paper-discovery-ledger.json`](paper-discovery-ledger.json)。它不替代搜索，而是强制把
搜索结果变成可审计终态；下一批必须追加新 batch，不能覆盖旧记录。

最新一次跨领域复查见[全主题系统缺口审计（2026-08-08）](full-domain-gap-review-20260808.md)。
它明确纠正了“局部候选批次闭环等于全库无遗漏”的错误，并给出下一轮 P0/P1 队列。

## 2026-08-13 GenRec 纠错

Netflix GenRec（arXiv 2608.10257）于 2026-08-10 发布，但旧流程将长查询拆成
严格 AND，每个查询只取前 8 条，并只校验“已被发现的候选”是否闭环。因此它
虽然在时间窗内，仍可以在候选阶段被截断。

现在使用九组主题查询、优先机构反查、每组最多 200 条分页结果取并集，
按 canonical arXiv ID 去重，并保留 `matched_queries`。召回后才进行 PDF/HTML 全文
证据判定；摘要没有 A/B 不再是拒绝理由。定时 GitHub Actions 每日生成过去
14 天的 `paper-candidates.json` artifact，但 artifact 只是待审候选，不会伪装成已通过
线上证据门槛。基础模型、LLM 后训练和 Agent 也使用各自的多查询矩阵，不再只扫描搜广推。

本地可复现同一扫描：

```bash
PYTHONPATH=src python scripts/discover_papers.py \
  --track recommendation \
  --lookback-days 14 \
  --page-size 50 \
  --maximum-results-per-query 200 \
  --cross-source-config configs/paper-discovery-sources.json \
  --output paper-candidates.json
```

arXiv API 不提供结构化 affiliation，所以机构词查询只是补充召回；Google/Meta
等优先机构仍必须使用作者首页 affiliation/官方页反查，再逐篇审查正文。

每日任务还会把候选与统一 manifest、历史 ledger 自动差分，在 Actions Summary 中分成
“Google / Meta 重点复核”“其他新候选”和“已处理候选”。Netflix 等其他机构继续参与
召回，但不触发置顶预警。实施队列统一维护在[后续路线图与 TODO](research-roadmap.md)。

## 跨来源召回与终态回写

单一 arXiv 查询之外，定时任务现在还会读取
[`configs/paper-discovery-sources.json`](https://github.com/daiwk/auto-research/blob/main/configs/paper-discovery-sources.json)，覆盖 Google
Research、Google DeepMind、Meta AI 官方论文页，RecSys/SIGIR 会议页以及 Google/Meta
研究 GitHub 组织页。配置也支持作者主页；已知相关论文可通过 `--snowball-seeds` 调用
Semantic Scholar references/citations 扩展。每个命中保留：

- 来源名称、类型与 URL；
- 机构（来源能够确定时）；
- direct、reference 或 citation 关系；
- citation snowball 的 seed arXiv ID；
- 单个来源失败信息，避免某个页面失败后整批静默少召回。

artifact 仍然只是待审队列。人工全文审查完成后，把决定写成 JSON：

```json
{
  "source_artifact": "paper-candidates-recommendation.json",
  "decisions": [
    {"id": "2608.12345", "priority": "P0", "status": "rejected", "reason": "正文无量化线上证据"}
  ]
}
```

再执行：

```bash
PYTHONPATH=src python scripts/record_discovery_review.py \
  --artifact paper-candidates-recommendation.json \
  --decisions review-decisions.json \
  --batch review-20260820-recommendation

python scripts/audit_paper_coverage.py --strict \
  --pending-artifact paper-candidates-recommendation.json
```

回写器要求每个 `new` 候选都有 `implemented/rejected/deferred` 终态；严格审计同时检查
待审 artifact 与 ledger，未闭环候选会直接失败，而不是留到下一轮后被遗忘。
