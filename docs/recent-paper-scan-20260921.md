# 近期论文扫描记录（2026-09-21）

## 覆盖范围

- 首次公开时间：2026-09-18 至 2026-09-21，与上一批次重叠 1 天；以 arXiv 官方摘要/HTML/PDF 正文及作者仓库为准。
- 领域：工业搜广推与 LLM 应用、基础模型、LLM 后训练、Agent、多模态、System One / Jev。
- 工业论文继续检查正文实验和部署证据，摘要未写 A/B 不作为排除理由；Google / Meta 保持最高优先级。
- 本批发现 Meta EvoPilot 的明确 7 天随机线上实验，因此按 P0 收录；其余四篇 Agent 论文按可执行机制与开源证据收录为 P1。
- 基础模型、LLM 后训练与 System One / Jev 轨道均完成同窗口检索和正文抽查，本批没有发现达到现有 P0/P1 接入门槛且未被仓库覆盖的新候选。

## 本批实现

| 优先级 | 论文 | 领域 | 本地实现与边界 |
|---|---|---|---|
| P0 | [EvoPilot (2609.21257)](reproductions/2609.21257-evopilot/README.md) | 工业检索 / Auto Research | L2；执行比较协议、artifact attestation、fail-closed verifier 和匹配交互头对照，不复刻 Meta VDD 生产系统 |
| P1 | [AutoViewMem (2609.21940)](agent-research/2609.21940-autoviewmem/README.md) | Agent 长期记忆 | L1 observation-safe 视图发现、正交写入与压缩诊断 |
| P1 | [MACE (2609.21533)](agent-research/2609.21533-mace/README.md) | 多 Agent 记忆 | L1 observation-safe 功能单元、typed relation 与结果回写 |
| P1 | [ArenaFlow (2609.21378)](agent-research/2609.21378-arenaflow/README.md) | Agent RL | L1 observation-safe tournament、关键步骤与技能信用诊断 |
| P1 | [GraphSkillEvo (2609.21749)](agent-research/2609.21749-graphskillevo/README.md) | Agent 自进化 | L1 observation-safe 技能图 mutation/crossover 诊断 |

## 已审阅但本批不接入

| 论文 | 处置 | 原因 |
|---|---|---|
| MintAct (2609.22083) | deferred | 定义性贡献依赖大规模视觉 Agent 轨迹与真实 GUI 环境；当前本地 deterministic mini-suite 不能形成可靠能力证据 |
| NemotronLabs VoiceChat (2609.21967) | deferred | 需要 11B 全双工语音 checkpoint、音频数据和实时延迟评测，本批 System One A100 预算不同时扩张 |
| RAVEL (2609.21924) | deferred | 需要交互式检索环境和真实 RL 训练，不能用静态计数器代替核心策略学习 |
| SignGPT (2609.21709) | deferred | 属于手语多模态生成，需要公开视频/姿态数据和对应 checkpoint 评测，留给多模态专项批次 |
| AgentVidBench (2609.21386) | rejected as method implementation | 是评测数据/协议而非本轮实现方法；记录为后续视频 Agent 公共评测候选 |

## 覆盖结论

本窗口完成了候选发现、正文核验和终态登记，但不把它表述为对所有站点的穷尽式证明。下一次扫描从 2026-09-20 起保留两天 overlap；Meta / Google 新论文仍优先检查全文线上证据。
