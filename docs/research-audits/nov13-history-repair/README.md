# 2026-11-13：ScientistTwo 与 Google/Meta 历史补漏

[English](../../en/research-audits/nov13-history-repair/README.md)

> 后续更新：本页保留当时的六篇交付与24条待核快照；这24条现已在[后续固定范围核查](../nov13-colm-remaining/README.md)收口，新增23个有界组件/接口、1条实质范围排除。下文“待核/未选”描述属于旧快照，不是当前积压。

本轮交付 **6 篇历史补漏：4 个低成本 CPU 控制组件、2 篇审查资料收录**。它们不是 11 月 13 日新首发。所有完整模型／科研实验均未运行：其中 5 篇有原文规模依据，明确**成本过高，不复现（审查 DONE）**；DS-STAR 单任务开发成本并不高，单独标记商业模型与完整评测依赖未运行，不编造“大训练成本”。

| 论文 | 原始 v1 日期（UTC） | 本轮交付 |
| --- | --- | --- |
| [ScientistTwo](../../agent-research/2609.19644-scientist-two/README.md) | 2026-09-17 | 有界阶段、子集升阶、成功／失败历史、严格改进与评审预算 |
| [DS-STAR](../../agent-research/2509.21825-ds-star/README.md) | 2025-09-26 | 外部 verifier/router 驱动的追加／回溯再规划，预算末稿保持未验证 |
| [ERA](../../agent-research/2509.06503-era-flat-puct/README.md) | 2025-09-08 | 全节点平铺 PUCT、排名归一化、祖先访问计数与 validation 选优 |
| [EnvHarness](../../agent-research/2608.19880-envharness/README.md) | 2026-08-20 | 可达状态回放、动作／观察合同、共享预算串联与原始 verifier 合取 |
| [MLE-STAR](../../agent-research/2506.15692-mle-star/README.md) | 2025-05-27 | 真实消融定位与两层细化的方法／资源审查；没有本地 Agent |
| [AlphaEvolve](../../agent-research/2506.13131-alphaevolve/README.md) | 2025-06-16 | 程序进化、异步级联评估及作者结果资料审查；没有本地搜索实验 |

Google/DeepMind 优先来自核对过的作者或官方研究来源，不由标题里的 “Meta” 或引用推断。按一作第一署名单位聚合与机构优先是不同字段：例如 EnvHarness 一作来自 Washington University in St. Louis，Google 实习工作及 Google 合作者提供优先来源证据，不能把一作单位直接改为 Google。Meta 的有限官方核查未建立本专题额外可固定身份的新论文；目录不可用等限制公开保留，不宣称 Meta 全研究不存在遗漏。

## 为什么 ScientistTwo 之前没收录

修复前 canonical manifest、账本、保留的旧审查与代码中没有该身份。9 月 19 日摘要页声称覆盖 9 月 15–18 日，但列出的论文中缺少它；现存抓取不足以重建当时的完整召回链。**不能把某个查询、去重器或 P2 决定臆断成已证明的唯一原因。**

能确认的流程问题是：有限近期差集、首尾页复查和日期／摘要级终态，不能代替历史机构来源的独立身份对账。原记录保留为快照，本轮新增明确补漏，不重写过去为“其实已经审过”。逐项来源和首发、机构、上游代码、方法／成本位置见[优先线索核查](priority-inventory-review.json)及 [ScientistTwo 专项审查](scientist-two-review.json)。

## 检查方式怎么改

[历史对账工具与使用说明](history-reconciliation.md)已接入默认扫描：

- 在近期日期过滤前，保留配置官方页面的精确 arXiv 身份、可见版本、实际页面 URL、捕获时间及解码文本 SHA。
- 独立比对 canonical manifest 和实质审查／成本终态。旧 P2 选题、日期初筛和泛化 known 不关闭受保护的 Google/Meta 方法审查；明确高成本／来源归档不自动重试。
- 主扫描产物内嵌历史报告，并另写 `paper-candidates-*-historical-review.json`，每日工作流一并上传。
- 既有 Google、DeepMind、Meta 页面与新增 COLM 来源均使用有限预算；配置存在、HTTP 成功和近期零新增都不等于历史穷尽。

本轮从真实捕获的 Google COLM 2026 活动页提取 **28 个唯一身份**，以[独立来源观察](historical-source-observation.json)支持[离线对账](historical-source-reconciliation.json)。这是跨领域活动索引，不是 28 篇合格漏收或实施任务；未原文核实的身份仍明确待核，不伪装成已审。PolicyBank 留作本轮未纳入重点的可追踪线索，未声称算法已实现。当前水位仍为 **2026-11-09**，本轮不关闭新日期窗口。

## 实际执行与证据等级

四个组件已在冻结源码后执行 **42、43、44 三种子**，见[冻结源码证明](frozen-sources.json)、[原始 CPU 结果](raw-cpu.json)及各论文旁的 `metrics/component-cpu-seeds42-44.json`。

```bash
PYTHONPATH=src:scripts python scripts/run_nov13_history_components.py --check
PYTHONPATH=src python scripts/reconcile_priority_history.py \
  --artifact docs/research-audits/nov13-history-repair/historical-source-observation.json \
  --output /tmp/priority-history-current.json
```

第一条命令离线核验已提交源码、Git 对象证明、原始结果和指标链；第二条用当前 manifest／账本重算来源身份状态。两者都不读取未提交 `.cache`、不联网、不训练。

三种子仅排列或改变固定控制夹具，不是三个独立研究任务。外部 LLM、语义判据、程序生成／沙箱、实际科研执行、文件分析、EnvRigger 和真实 benchmark bridge 均未被假实现。状态仍为 `l1_mechanism / diagnostic_only`，无能力比较、Evolve 晋级或执行型集成；本轮无 CUDA 广告路径，因此无需也不伪造 A100/A30 回执。

完整实验不会为了“试一下成本”而下载资源、调用商业模型、启动长训练或自动重跑。DS-STAR 的原文 USD 0.23 是十个 development 任务的作者均值，不是完整三 benchmark 的本地价格或耗时，故保留独立商业依赖终态。

## 学习与双语交付

六篇均有完整元数据、原论文关键图、中文解读及逐页校对英文。每篇新增基础、机制、比较、实现四层独立问答，共 **24 道**，并加入有真实比较对象、源指纹及校对英文的专题精读更新。学习区和公开看板由单篇事实源重新生成；审查资料不冒充实验指标。

[固定交付范围](task-scope.json)区分组件完成、完整实验不复现、未选线索、来源例外和非穷尽边界，不再用“历史都完成”概括这些不同状态。
