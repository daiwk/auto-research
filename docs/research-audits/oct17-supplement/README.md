# 10 月 17 日补审组件：固定范围与成本合同

本批来自同一 **10 月 16 日公告、10 月 15 日 v1** 的补审，不是新公告增量。用户批准在一个 MR 中交付九项低成本组件、两项评测接口及三篇仅资料论文；不会以本批实施推断全源覆盖完成或推进审查水位。

## 接受范围

| 类别 | 论文 / 稳定键 | 接受的本地范围 | 完整实验成本依据与决定 |
| --- | --- | --- | --- |
| 组件 | Prism-1 / `prism-1` | 独立 option block、共享 position、赔率读出与不变性 | 8B/12B，多臂多种子；原文 H100 单次约 50–85 分钟。完整实验不复现（审查 DONE）。 |
| 组件 | LangDiT / `langdit` | 连续扩散 denoiser、shortcut codebook 梯度路径、有界校准与 self-conditioning | 约 334M、七组×250K 更新、每步 512×1024 tokens。完整实验不复现（审查 DONE）。 |
| 组件 | OPRD / `oprd-reminder` | teacher-only 提醒作用域、成功 NLL / 失败 reverse KL、共享支持与刷新 | 16 H20、131072 context、三 epochs 和在线仓库 rollout。完整实验不复现（审查 DONE）。 |
| 组件 | OpCredit / `opcredit` | BOC 支持去重、FTC 势差、决策跨度与联合策略损失 | 八张 RTX5880、约 2500 GPU 小时与 Freebase 服务。完整实验不复现（审查 DONE）。 |
| 组件 | SSR / `structural-signal-retriever` | 有界结构信号、IDF 倒排检索、确定性排序 | 全量 8.84M passages、约 124 GiB RAM 和 API 编排。完整实验不复现（审查 DONE）。 |
| 组件 | RSIFlow / `rsiflow` | 冻结父代、M/H/A 干预、接受/拒绝与失败经验 | 4B/8B、分布式训练、多轮多候选和 3000 训练 / 744 报告任务。完整实验不复现（审查 DONE）。 |
| 组件 | LEASH / `leash` | pooled-LDA、任务级 OOF 校准与升级后监督调度 | OSWorld 262 任务、多弱模型与商业强模型、长 GUI 交互。完整实验不复现（审查 DONE）。 |
| 组件 | PROBE / `probe` | trace verifier、首次/重复奖励、覆盖分母和确定性复评分 | 4B auditor / 30B target、双 A100、多优化器多臂。完整实验不复现（审查 DONE）。 |
| 组件 | Terminal-RSI / `terminal-rsi` | TB-GAE、分块续传、FDR/SPR 与 family divisor | 27B、256K、多阶段分布式 PPO、3000 任务。完整实验不复现（审查 DONE）。 |
| 评测接口 | GACC-Bench / `gacc-bench` | 压缩/读取/评分隔离、预算截断、复用与多问题统计 | 十模型、多预算、281 contexts / 500 goals / 2571 questions 的长上下文 API 扫评。完整实验不复现（审查 DONE）。 |
| 评测接口 | Muon paired-budget / `muon-paired-budget` | 同数据/时间域 AUC、配对统计、调参预算 regret | 四 workload、23 候选和五匹配种子的完整训练。完整实验不复现（审查 DONE）。 |
| 仅资料 | Google Gemini Minecraft / `gemini-minecraft` | 方法、单次案例、原图与费用边界 | 四执行 Agent 加 Observer，单次约 27 小时、约 24000 调用。成本过高，不复现（审查 DONE）。 |
| 仅资料 | Hy-Memory / `hy-memory` | OPD、归因奖励、记忆写入研究解读 | 30B-A3B、128 H20、64 windows×8 rollout。成本过高，不复现（审查 DONE）。 |
| 仅资料 | Athanor / `athanor` | 研究流水线及资源边界 | 32 GPU×104 小时、约 12000 美元。成本过高，不复现（审查 DONE）。 |

以上是原文配置，不是本地耗时预测或 GPU 实测。预算只假设一张 A100 **或** A30；不下载大权重或全量数据，不启动长 rollout，不把公式 fixture 改标为能力验证。

## 验收合同

- 独立模块与运行命令可执行，不以 registry 标签冒充接入；本批不承诺 Evolve 能力晋级。
- 每项以独立参考、负对照和失败输入检查决定性机制；训练目标只对训练数据使用 gold，受评 Agent/压缩器/路由器不可读取答案。
- CUDA 组件先冻结源代码，再在真实 NVIDIA A100/A30 做有界三种子诊断；回执绑定命令、输入身份、commit 和执行源 SHA。CPU 组件不伪造 GPU 回执。
- 每篇 metrics 独立保存，全部 `diagnostic_only: true`、`promotion_eligible: false`；公共评测接口通过不意味着执行原模型。
- 保留 PROBE judge 的已知误判和确定性重评分差异；不将 Terminal-RSI 的主表收益归因于未核实进入 checkpoint 的 TB-GAE。
- 原作者代码入口与许可证分开；无明确许可证不复制上游实现。完整高成本决定为终态，不自动重试，不阻塞其他交付。

## 实测与证据

九个组件和两个评测接口均已实现；四项 CUDA 组件在 **NVIDIA A100-SXM4-80GB** 上完成 seeds42/43/44 有界机制验证，七项CPU组件/接口完成同种子诊断。各篇保存独立 metrics，不合并成一份伪造排行榜；上述数字不是原论文 benchmark 效果。

- GPU：Prism-1的独立前向等价/不变性与负对照，LangDiT的梯度路径/四种极值归一化，OPRD的teacher隔离/真实更新，OpCredit的独立信用分配/联合损失与真实更新。
- CPU：SSR与全扫描参考一致；Muon共同数据/时间预算排序可反转；RSIFlow保留失败和拒绝；LEASH任务级OOF与1/4/7监督调度；PROBE区分原始重复命中与去重覆盖；Terminal-RSI完整分块续传；GACC压缩器不见问题/gold、零预算严格为空且不padding。
- 新论文 OPRD 的资料键为 `oprd-reminder`，内部独立runner参数仍为 `--methods oprd`；旧 `auto-research reproduce --paper oprd`（2609.08798 reverse distillation）保持不变。
- LEASH的三项计数器只记录已执行回调，OPRD的refresh计数只记录教师快照刷新，**不是新模型能力证据**；已逐项复核AST边界清单后再生成 inventory。
- 三篇高成本资料没有算法入口、伪造指标或GPU通过回执；全部完整实验是终态不复现、审查DONE，不自动重试。

所有14篇具备论文信息块和原图，目录/公开看板同步。定向机制与交付合同共110项测试通过；全量测试、Ruff、最小依赖入口、严格文档构建、paper-spec、指标迁移、GPU证据及平台审计门禁均通过。最终收口会重新验证逐seed失败状态、聚合重算与冻结提交，不能仅凭已有文件宣称验收。本批不推进审查水位，不把已实现固定候选清单推断为全源穷尽。
