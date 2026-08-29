# 统一后续路线图与 TODO

## 2026-08-26 平台 P0

| ID | 状态 | 交付 |
| --- | --- | --- |
| INFRA-003 | DONE | 跨论文复现、Evolve、后训练、Agent 和多模态的 SQLite 实验索引、查询、Pareto 前沿与静态 HTML 看板 |
| INFRA-004 | DONE | 全量 adapter `paper.yaml`、确定性生成/校验和拒绝覆盖的脚手架 |
| EVOLVE-005 | DONE | 论文算子 registry、模型/槽位/依赖/冲突/资源预算校验，并接入候选规划过滤 |

完成这三个 P0 后，新增论文的标准路径是：补 adapter 与公开实验 → 同步声明 → 映射可执行 Evolve 算子 → 统一实验库登记指标。平台维护不再依赖手工复制目录数字或跨页面同步元数据。

## 2026-08-27 平台 P1

| ID | 状态 | 交付 |
| --- | --- | --- |
| INFRA-005 | DONE · [PR #128](https://github.com/daiwk/auto-research/pull/128) | Local / SSH / Slurm 统一执行契约，含日志、状态、重试、硬超时、显存声明和成本上限 |
| EVAL-001 | DONE · [PR #128](https://github.com/daiwk/auto-research/pull/128) | 推荐、基础模型、多模态、后训练与 Agent 的版本化公平评测协议；拒绝跨协议横向比较 |
| AUTO-001 | DONE · [PR #128](https://github.com/daiwk/auto-research/pull/128) | `paper.yaml` 到实验假设、算子、消融、搜索空间的可审计提案，保留来源并要求人工确认 |
| EVAL-002 | DONE · [PR #128](https://github.com/daiwk/auto-research/pull/128) | 配对 bootstrap、置换检验、Holm 校正、顺序 seed 与成本约束决策 |
| MEMORY-001 | DONE · [PR #128](https://github.com/daiwk/auto-research/pull/128) | 精确上下文负结果知识库，并接入 Evolve 的候选过滤和逐轮研究记忆 |

完整使用方式、边界和命令见[自动研究平台 P1](research-platform-p1.md)。

本页是仓库后续工作的**唯一权威待办清单**。各领域谱系页只解释覆盖范围和技术关系，
不再维护另一份易漂移的 TODO。以后每个实现 MR 都要更新本页的状态、验收证据和 PR；
新发现的工作先登记，再开始实现。

更新基线：**2026-08-29**。8 月 29 日四领域增量扫描的九篇 P0 已完成，详见
[扫描审计](recent-paper-scan-20260829.md)。已登记的静态 P0/P1 队列均有终态；当前没有尚未实现的
静态能力建设任务。每日扫描发现的新候选仍会动态产生新的论文任务。

## 优先级和状态

| 标记 | 含义 |
| --- | --- |
| P0 | 新发现且通过硬门槛的最高优先论文，优先于本页 P1；工业方向中 Google / Meta 最高优先 |
| P1 | 已有可靠实现路径和公开数据，可分批交付的能力建设 |
| EVIDENCE | 方向重要，但尚缺公开证据、数据或公平评测，不能用占位 adapter 冒充实现 |
| DEFERRED | 用户明确延后，或依赖复杂外部环境；恢复前不进入执行队列 |
| DONE | 已完成并有代码、文档、指标和测试证据 |

Google（含 DeepMind、YouTube）和 Meta（含 Instagram）是唯一自动置顶机构。Netflix、
ByteDance、Alibaba、Kuaishou、Pinterest 等仍进入高召回扫描和正常评审队列，但不自动
置顶。机构查询命中只触发全文复核，不能替代论文首页 affiliation 和正文证据。

## 动态 P0：论文发现闭环

| ID | 状态 | 工作 | 完成条件 |
| --- | --- | --- | --- |
| DISC-001 | DONE | 每日四领域多查询、分页、canonical arXiv ID 去重 | GitHub Actions 生成四个候选 artifact |
| DISC-002 | DONE | 候选与 manifest、历史 ledger 自动差分 | JSON 和 Actions 摘要区分新候选、已实现、已审计 |
| DISC-003 | DONE | Google / Meta 新候选自动置顶预警 | 仅两家触发 warning；Netflix 等保持普通候选 |
| DISC-004 | DONE · [PR #113](https://github.com/daiwk/auto-research/pull/113) | 跨来源召回 | 官方研究页、会议列表、作者主页/GitHub 和 citation snowball 均保留 provenance 与单源失败 |
| DISC-005 | DONE · [PR #113](https://github.com/daiwk/auto-research/pull/113) | 批次终态自动回写 | 回写器要求全部新候选终态；strict audit 可核对待审 artifact 与 ledger |

每个新工业候选先按“机构/主题”召回，再读 PDF/HTML 全文。只有量化线上 A/B，或用户
明确认可的统计显著全流量部署，才进入实现队列；摘要未写 A/B 不能作为拒绝依据。

## P1 执行队列

建议按表内顺序推进；同一编号应尽量作为一个可独立合并的 MR。

### 基础模型与多模态

| ID | 状态 | 工作 | 最小验收条件 |
| --- | --- | --- | --- |
| FM-001 | DONE · [PR #113](https://github.com/daiwk/auto-research/pull/113) | test-time compute、verifier、动态 reasoning budget | 固定 SmolLM2 revision；GSM8K/算术多预算曲线同时报告正确率、token、延迟和调用成本 |
| FM-002 | DONE · [PR #114](https://github.com/daiwk/auto-research/pull/114) | scaling-law 多预算基础设施 | 默认 4 个模型规模/数据/step 预算点；记录实际参数量、tokens seen、FLOPs proxy、逐点残差、RMSE/R² 和不可外推边界 |
| MM-001 | DONE · [PR #115](https://github.com/daiwk/auto-research/pull/115) | 视频多模态 | 固定 SmolVLM2 commit；Video-MME-v2 Parquet/JSONL + MP4；逐题续跑、三 seed、置信区间和子集边界 |
| MM-002 | DONE · [PR #115](https://github.com/daiwk/auto-research/pull/115) | 音频多模态 | 固定 CLAP commit；ESC-50/ESC-10 真实 WAV；zero-shot top-1/top-5 和 text embedding cache fingerprint |
| MM-003 | DONE · [PR #116](https://github.com/daiwk/auto-research/pull/116) | 具身与大规模多模态后训练 | SmolVLA/LeRobot 真实训练入口、数据 manifest 与明确的 simulator/硬件成功率边界 |

### LLM 后训练

| ID | 状态 | 工作 | 最小验收条件 |
| --- | --- | --- | --- |
| PT-001 | DONE · [PR #113](https://github.com/daiwk/auto-research/pull/113) | L2 切换到可下载 pretrained causal LM | SmolLM2 固定 revision，GSM8K unrestricted generation 与 3 seeds |
| PT-002 | DONE · [PR #115](https://github.com/daiwk/auto-research/pull/115) | CoBA-RL 完整教师路径 | 固定 Qwen2.5 teacher commit；pass@k/教师双缓存、真实调用率、token 成本与训练前后能力边界曲线 |
| PT-003 | DONE · [PR #113](https://github.com/daiwk/auto-research/pull/113) | 公开偏好数据 | 固定 UltraFeedback revision/MIT 元数据，DPO/ORPO 同预算真实模型对照 |
| PT-004 | DONE · [PR #113](https://github.com/daiwk/auto-research/pull/113) | GPU 训练完整性 | batch、gradient accumulation、mixed precision、safe checkpoint 与 optimizer resume；CPU/Mac 保留路径 |

### Agent

| ID | 状态 | 工作 | 最小验收条件 |
| --- | --- | --- | --- |
| AG-001 | DONE · [PR #116](https://github.com/daiwk/auto-research/pull/116) | Agent Lightning 连接可训练 LLM policy | SmolLM2 pairwise policy update、显式 transition credit、真实测试 executor 与 token/tool 成本 |
| AG-002 | DONE · [PR #116](https://github.com/daiwk/auto-research/pull/116) | Agent 真实 executor 的公平矩阵 | 相同仓库 fixture、相同 subprocess 上限、三 seed 比较 controller policy |
| AG-003 | DONE · [PR #131](https://github.com/daiwk/auto-research/pull/131) | Agent L2.1 隔离能力评测与九轴自动进化 | 删除 guide/oracle；train/validation/test 隔离；六方法、五消融、三 seed CI；validation 选冠军且 test 只在代际结束后运行 |

### Auto Research / Evolve

| ID | 状态 | 工作 | 最小验收条件 |
| --- | --- | --- | --- |
| EV-001 | DONE · [PR #113](https://github.com/daiwk/auto-research/pull/113) | 将 FM-001 的推理预算算子接入统一 genome | `reasoning-checkpoint` 搜索采样预算、self-consistency verifier、停止阈值并生成逐代报告 |
| EV-002 | DONE · [PR #116](https://github.com/daiwk/auto-research/pull/116) | 将 PT-001～PT-004 接入后训练 genome | data/objective/teacher/rollout/accumulation/precision 成为可继承组合轴并进入逐代报告 |
| EV-003 | DONE · [PR #117](https://github.com/daiwk/auto-research/pull/117) | 将 AG-001/AG-002 接入 Agent genome | memory/planner/tool/critic/policy/recovery 可组合，跨 episode 复用与失败恢复可测 |
| EV-004 | DONE · [PR #117](https://github.com/daiwk/auto-research/pull/117) | GenRec 类生成式推荐 evolve | MovieLens-1M 真实全目录 head、context/reward/distillation 旋钮和统一 ID-catalog 基线；Netflix 不因此获得论文优先级 |
| INFRA-001 | DONE · [PR #111](https://github.com/daiwk/auto-research/pull/111) | GPU 依赖防护 | pip dry-run 阻止静默替换现有 PyTorch；Linux CPU 合同测试覆盖，既有 A30 关键路径回归继续保留 |
| INFRA-002 | DONE · [PR #117](https://github.com/daiwk/auto-research/pull/117) | 重点方法多 seed 晋级 | 推荐/基础模型 adapter、后训练和 Agent 统一 3 seeds、置信区间、逐 seed 失败记录与断点续跑 |

## 等待公开证据，不创建占位实现

| ID | 状态 | 缺口 | 恢复条件 |
| --- | --- | --- | --- |
| EVD-001 | EVIDENCE | 审核、作弊、欺诈、广告合规与风控 | 公开标注数据以及 precision/recall、误杀率和 guardrail 协议 |
| EVD-002 | EVIDENCE | 私有大规模广告竞价/转化日志 | 可公开替代数据和不会泄漏业务信息的公平离线协议 |
| EVD-003 | EVIDENCE | 公开端到端 LLM 推荐产品复现 | 用户、catalog、生成、排序、反馈闭环均有合法公开数据 |
| EVD-004 | EVIDENCE | AIGQ、RaG、RoleGen、LCU | 公开 reward、视频/用户反馈或转化轨迹及清晰数据许可 |
| EVD-005 | EVIDENCE | RecoChain、DIG 等工业候选 | 核实量化线上 A/B 或用户认可的全流量部署正文证据 |

## 用户已延后

| ID | 状态 | 工作 | 恢复条件 |
| --- | --- | --- | --- |
| DEF-001 | DEFERRED | 官方 SWE-bench Lite | 准备官方容器、镜像缓存、执行预算和长时 CI/开发机窗口 |
| DEF-002 | DEFERRED | ToolHop 正式全集 | 确认数据/评测依赖、模型调用预算和可复现 runner |
| DEF-003 | DEFERRED | 真实浏览器 Agent 环境 | 提供隔离 sandbox、凭据策略、网络策略和失败重放能力 |

## 每个后续 MR 的更新契约

1. 开工前在本页登记编号、优先级、状态与验收条件；动态 P0 插到 P1 前执行。
2. 论文实现必须满足统一 metadata、中文解读、原文关键图、代码、指标和测试合同。
3. evolve 接入必须说明算子来自已实现论文、实时检索还是新组合假设，不能混写。
4. 完成后把状态改成 `DONE`，补充 PR 链接和关键证据；未完成部分拆出新编号。
5. 不在其他页面复制待办表；谱系页只链接本页，避免多个“剩余任务”互相矛盾。
