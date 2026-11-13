# 历史优先机构线索对账：使用与边界

[English](../../en/research-audits/nov13-history-repair/history-reconciliation.md)

近期公告没有新身份、官网首尾页没有新增链接，**都不能证明历史机构论文已经审完**。独立的历史 inventory 从已登记官方机构／活动、项目或作者来源保留明确 arXiv 身份，再与 canonical manifest 和实质方法／成本终态对账。当前默认配置包括 Google Research 2026、跨年目录、DeepMind、Meta 四个机构页面及 [Google COLM 2026](https://research.google/conferences-and-events/google-at-colm-2026/) 活动入口；框架不把 ScientistTwo 名称、ID 或特定会议写进通用判断规则。

## 日常扫描会自动生成什么

沿用现有命令和来源注册表即可启用，不需要单独执行一个遗忘的补漏步骤：

```bash
PYTHONPATH=src python scripts/discover_papers.py \
  --track agent \
  --start-date 2026-11-12 --end-date 2026-11-13 \
  --cross-source-config configs/paper-discovery-sources.json \
  --output paper-candidates-agent.json
```

默认同时生成 `paper-candidates-agent-historical-review.json`，完整历史报告也保存在主产物的 `cross_source.historical_review`。可用 `--historical-review-output PATH` 指定独立文件；没有 `--output` 时，报告随主 JSON 输出，不会静默消失。

来源注册项使用可选 `historical_inventory=true`，复用 `DiscoverySource`、既有分页预算和身份提取。每个成功页面保留实际 URL、捕获时间、`decoded_text_sha256`、解码后 UTF-8 字节数及原链接中的可见版本。这个 SHA 标识传入提取器的解码文本，**不是未经说明的网络原始字节证明**。原始 HTTP／文件回执可以另行归档；仅有机构来源也不证明每条参考链接的作者归属。

| 默认历史来源 | 最多目录页 | 标题查找上限 | 详情查找上限 |
| --- | ---: | ---: | ---: |
| Google Research 2026 目录 | 40 | 5 | 12 |
| Google Research 跨年目录 | 2 | 3 | 6 |
| Google DeepMind 目录 | 20 | 5 | 12 |
| Meta publications 目录 | 6 | 5 | 12 |
| Google COLM 2026 活动页 | 1 | 0 | 0 |

以上是**既有配置预算上限**，不表示本轮每页均成功或论文方法已审。为四个既有机构来源增加历史标记，只保存原有抓取页面中的身份，不追加分页、详情预算或额外历史爬取；实际来源可能提前结束、部分失败或超过预算。目录返回 PDF、空壳或无可提取身份时，不按 HTTP 成功推断覆盖完成；分页／捕获缺口进入历史报告的显式异常，详情查找错误仍保留在主来源产物。后续论文正文确实不可用时，须记录真实读取尝试并按既有来源例外口径处理，不能因索引有 ID 就声称方法已核验。

历史身份不按近期首发日期丢弃。只有来源明确召回、需要实质审查的 Google／Meta 历史身份才重新进入优先原文审查；普通旧 P2、已明确成本结案、来源归档或已知 catalog 身份不会因此自动成为新实施任务。工业搜广推仍需原文线上证据，未放宽 A/B 门槛。

## 离线重算：不依赖本地网页缓存

已保存的主扫描产物包含来源 inventory，可在普通 clone 安装依赖后离线对账：

```bash
PYTHONPATH=src python scripts/reconcile_priority_history.py \
  --artifact paper-candidates-agent.json \
  --source-config configs/paper-discovery-sources.json \
  --manifest docs/research-manifest.json \
  --ledger docs/paper-discovery-ledger.json \
  --output priority-history-agent.json
```

也接受顶层 `source_stats` 的独立来源产物。此命令不联网、不重读 `.cache` 网页、不下载权重、不训练，也不修改账本或水位。它依据**当前** manifest／ledger 重算状态，因此后续新收录或实质结案可以改变报告；旧产物应保留，不能冒称重新抓取过网页。

## 审查、目录与实现是不同维度

| 历史对账状态 | 含义与后续 |
| --- | --- |
| `needs-review` | 精确机构来源身份没有可识别实质闭环；进入 `priority-fulltext-review`，不是已接收论文或自动实施队列 |
| `catalogued` | 同一明确 arXiv 身份已在 canonical manifest；不按相似标题／URL slug 猜测，也不重复计新实现 |
| `reviewed` | 保留实质审查或明确高成本不复现终态；成本审查完成不等于原算法已实现或能力已验证 |
| `accepted-unimplemented` | 已有原文审查接受，但实现尚未交付；只是机会记录，不自动追加执行授权 |
| `archived-exception` | 保留已有不可确认来源归档；不伪装成原文方法已核验，不自动反复重试 |

日期初筛、`historical_first_publication`、泛化 `known` 标签和窗口级 P2 选题结案，都不能单独替代优先机构方法／成本审查。回归测试覆盖 ScientistTwo 的 missing→needs-review、旧 P2→优先原文，以及明确高成本 DONE 不反复重开。`method_review_completed` 只有存在结构化原文位置时才为真；成本／来源终态与它分开。

`source_identity_count` 是有界来源身份数，**不是新增合格论文数、接受数量或待实施 backlog**。报告从不自动运行复现或登记 Evolve，`automatic_implementation_queue=false`、`automatic_retry=false`，也不会推进审查水位。

## 覆盖与异常必须公开

这是配置来源及已捕获页面的对账，**不宣称 Google／Meta 全历史穷尽**。未捕获配置源、真实访问失败、分页超预算、页面无固定身份或身份缺少捕获 witness，分别进入显式 `exceptions`。`attempted=false` 的未覆盖项不是“实际尝试后已归档”；来源不可用也不能伪装成零新增或已读方法。

新增机构博客、会议／活动、项目或作者入口时，应在同一来源注册表登记可追溯 URL、机构线索、明确历史标记和有限分页预算。来源优先信号仍须原文作者栏核验。新 revision、独立机构证据或作者澄清可以按既有规则重开，不通过扩大便宜夹具绕过成本与 GPU 验收门槛。

建议工作流除现有主候选 JSON 外，一并上传 `paper-candidates-*-historical-review.json`；若指定自定义文件名，则上传对应显式路径。报告与实施交付清单应分别展示。
