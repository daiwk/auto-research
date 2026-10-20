# Harness² 与 Google/Meta 历史筛选补漏

本轮新增 **1 个低成本 CPU 控制器**，补 **12 篇高成本资料**，关联 **1 篇已有诊断**，
并为本次确实读过方法/资源段的 **22 个论文身份**追加独立处置。
22 篇的完整模型/API 实验均标注**“成本过高，不复现（审查 DONE）”**；
其中 Harness² 的局部 CPU 组件已实现，其余新资料不能算成算法已实现。
本轮没有新 CUDA 路径，不需要启动 A100/A30；没有运行付费 API 或下载模型。

## Harness²：已实现的部分

[论文详情与一键运行](../../agent-research/2610.14224-harness2/README.md)包括：

- 固定模型、环境、初始 Harness 和改进器版本；任务内 Propose–Probe–Compose。
- 并行扩宽、顺序加深，检查 $4k$ 次执行与 $3k$ 个编辑阶段。
- 选择器只能读公开任务与匿名的既有最终产物，不获得 gold、rubric 或来源 Harness。
- 同域先前任务的持久经验库、完整采用 Harness、被引用执行对照、冲突拒绝与失败保留。

实跑 seed 42/43/44、两种模式、每种两个流水任务，合计 **96 次真实 Python subprocess**、
72 个编辑阶段；原始执行约 1.78 秒。编辑器与选择器是确定性机制替身，
所以只有 **L1 机制证据**，不是 LLM 能力、官方基准成绩或已经打通 Evolve。
标量证据见[单篇指标](../../agent-research/2610.14224-harness2/metrics/component-cpu-seeds42-44.json)。

## 修正的筛选漏洞

| 旧行为 | 新行为 |
| --- | --- |
| 只要出现在 ledger 就归入 reviewed | 日期/身份初筛不关闭方法审查；普通 `new` 观察也不变成已审 |
| 窗口之前的首发被拒绝并关闭后续队列 | 官方 Google/Meta 新证据可召回旧文，单列历史补漏，不算当天新首发；明确未来首发不进入回补 |
| 机构优先规则只看特定查询名 | 同时识别官方机构来源、精确 GitHub owner 和机构字段；不从摘要的“meta-learning”猜作者机构 |
| accepted 但未交付，被泛化 known/review_done 遮住 | 单列 `implementation-pending`，显示在候选摘要；generic known 不盖过明确待交付 |
| 同一 ID 多次观察按第一次存在去重 | catalog 优先，其次真实方法/成本/来源终态，再是待交付，最后是泛化标签；保留冻结快照 |

明确高成本不复现仍是终态；即使保留旧 metadata-only 字段，也不会重新拉起昂贵实验。
`record_discovery_review.py` 拒绝把日期初筛或待交付状态写成新的终态；
Google/Meta 的正文来源要求不再仅由查询名触发。

## 本轮补资料与关联

以下均属于历史补漏，不是今天新发表；完整实验不复现。

| 论文 | 本轮实际交付 |
| --- | --- |
| [Harmony Harness](../../agent-research/2610.15150-harmony-harness/README.md) | 多目标、功能/安全权衡、范围受限框架演化的资料与成本 |
| [SEER](../../agent-research/2610.04109-seer-forecasting/README.md) | 事件检索、反思记忆、反馈成熟与测试冻结的资料与成本 |
| [MARS](../../agent-research/2602.02660-mars-research/README.md) | 模块化研究、预算搜索与执行经验的资料与成本 |
| [ECO](../../foundation-models/2601.22101-eco-optimizer/README.md) | 量化误差注入动量、免 master weights 的资料与成本 |
| [SA-DPO](../../post-training/2604.27733-sa-dpo/README.md) | 语义距离自适应偏好间隔的资料与成本 |
| [FUSE](../../foundation-models/2604.18547-fuse-verifiers/README.md) | 无标签 verifier 集成及独立性假设的资料与成本 |
| [Prompt-Level Distillation](../../post-training/2602.21103-prompt-level-distillation/README.md) | 教师规则抽象、聚类与冲突修订的资料与成本 |
| [RL for Code Optimization](../../post-training/2607.25970-code-optimization-rl/README.md) | 代码优化 RL 与多节点资源成本的资料 |
| [AutoformBot](../../agent-research/2605.29955-autoformbot/README.md) | 数学形式化 Agent 的资料与资源成本 |
| [AIRS-Bench](../../agent-research/2602.06855-airs-bench/README.md) | AI 研究评测协议资料；不是已接入的评测接口 |
| [MetaEncoder](../../foundation-models/2610.11316-metaencoder/README.md) | 双塔自然语言决策及官方 30B 评测成本 |
| [Raw Video Mid-Training](../../multimodal-models/2610.11019-raw-video-midtraining/README.md) | 连续视觉 next-token 训练与匹配对照的资料和成本 |
| [MaD-RL](../../post-training/2609.31644-mad-rl/README.md) | 修正首发日期，关联旧字符模型/A100 诊断和负结果；不改旧测量，不重复实现或跑 GPU |

另对既有 Meta Logbook、Render2Reason、PAT、CanonQ、Mixture of Layers、
Omni-Diffusion-Distill、X-AgentRed，以及 Compute Optimal Tokenization 补资源决定。
这些只在[逐项处置](closure-decisions.json)和审计中关闭完整实验，不冒充新增组件或全部有独立资料页。

## 实际覆盖范围与未完成事项

- Google：逐项枚举已保存的 **102 条潜在范围历史记录**；DeepMind **27 条 2026 目录记录**；
  另核对 **198 个日期归档身份**，并对 7 篇补读明确的方法、实验、资源与发布段。
- Meta：逐项对账已保存的 **48 条 2026 官方目录记录**；核对 9 条已接受但未交付的旧记录，
  为这 9 条补齐具体原文资源成本判断。
- 共关联 **83 个已识别的论文身份**。按当前仓库状态，7 个已有组件/实现目录、22 个已审处置，
  **仍有 54 个没有实质终态**；这不表示它们都符合要求，更不表示已阅读全文。
- 原始全账本还存在 **521 个未交付的旧接受条目**。本轮让它们可见，
  **没有把这 521 个全部实施，也没有用统一高成本标签冒充逐篇审查**。
  它们不是本 MR 的新增实施承诺，后续应按机构优先、主题和成本分批核查。

逐项清单：[Google/DeepMind 审计](google-audit.json)、[Meta 审计](meta-audit.json)、
[当前对账](backfill-inventory.json)、[22 项新处置](closure-decisions.json)。
无身份/日期或原文无法核实的项保持显式元数据例外，不算接受、全文 DONE 或实现。
**本轮不是全历史/全来源穷尽审查，审查水位保持 2026-10-15，不自动推进。**

## 验证与复跑

```bash
PYTHONPATH=src python -m pytest tests/agent_research/test_harness2_component.py \
  tests/test_historical_priority_discovery.py tests/test_harness2_priority_delivery.py \
  tests/test_harness2_meta_reference_catalog.py
PYTHONPATH=src python scripts/audit_historical_priority_backfill.py --check
```

共享发现、来源、审查写入和水位测试也必须通过。完整质量检查与 MR CI 状态由交付时实际结果说明，
不把上面的复跑命令当成已运行证据。

本轮已运行：196 项发现/审查相关回归、95 项新增定向测试、30 项文档测试、
最小 wheel 安装契约、指标/GPU 证据校验与严格文档构建，结果均通过。
已删除本轮临时站点、隔离安装环境、构建缓存与上游克隆等约 478 MiB；
保留原始 CPU 执行记录（包括早期诊断）、提交的指标与论文图片，不清理共享模型/数据缓存。
