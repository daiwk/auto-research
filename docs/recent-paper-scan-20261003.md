# 2026-10-03 近期论文扫描与实现收口

## 扫描口径

- 扫描窗口：2026-10-01 至 2026-10-03，并保留 2026-09-29～09-30 的晚索引重叠区。
- 覆盖领域：搜广推与 LLM 应用、基础模型与多模态、LLM 后训练、Agent / RSI / Jev。
- 来源：arXiv 官方 API、arXiv HTML/PDF、论文首页及原作者公开仓库；**未使用 DeepXiv**。
- Google（含 DeepMind、YouTube）与 Meta（含 Instagram）先做标题召回，再检查作者单位和全文；摘要没有 A/B 字样不能直接拒绝工业论文。
- 本轮 arXiv 请求成功，但 Google Research、Google DeepMind、Meta AI 等官方列表有 5 项传输或标题对账失败。因此本批完成下列 P0/P1 实现，但 `coverage_complete=false`，全来源水位仍停在 **2026-10-02**，下一轮继续从 2026-10-01 重叠扫描。

## 本批实现

| 优先级 | 领域 | 论文 / 方法 | 本地执行范围 |
|---|---|---|---|
| P0 | 搜索 / LLM 推荐 | RPTune | 查询—商品打分、裁剪与 suffix 编排 |
| P1 | Agent 推荐 | AgentWebRec | 时序语义检索、低置信协作门控、隐私审计 |
| P0 | 基础模型 / Jev | LLM2Jev | 有限选项联合概率与辅助 KL 锚定 |
| P1 | 多模态嵌入 | Omni-Embed-Mini | 稠密描述 teacher 的共享几何蒸馏 |
| P1 | 多模态效率 | MWOP | 模态路径与 FFN 通道的独立剪枝 |
| P1 | 优化器 | AF-Muon | tied vocabulary 的 support-aware 有限帽方向 |
| P1 | 长上下文 | REA | persistent instruction 与 episodic memory 分离 |
| P1 | 多模态推理 | HAWK | 多层隐藏态混合与 shifted teacher |
| P1 | 模型压缩 | IrekoGPT | 共享投影基的嵌套宽度子网 |
| P0 | 后训练 / Agentic RL | Sharpening Tax | 固定预算覆盖率损失诊断 |
| P1 | 后训练 | CARM | 防 signed-ratio 抵消的响应掩码 |
| P1 | 后训练 | GMC-GRPO | 异步 group mass capping |
| P1 | 偏好优化 | GAW-PO | rejected-token 梯度对齐权重 |
| P1 | Agentic RL | SHARPO | 交互 segment 级自蒸馏 credit |
| P1 | 视频 RL | TVRL | reward 敏感度驱动的 token credit |
| P1 | 多模态 OPD | LEGO-OPD | language prior × grounding likelihood teacher |
| P1 | VLA OPD | DriftOPD | reverse-KL 与 future potential 分解 |
| P0 | Coding Agent | AutoCompact | decision / summary / next action 三字段原位纠错 |
| P1 | 长程 Agent | Explicit Belief State | 未解决需求状态与 trapping 检测 |
| P1 | Agent 安全 | PACE | effect 前 capability 与 provenance 联合授权 |
| P1 | RSI / Coding Agent | RuleEvolve | 规则变异后的 validation-only 选择 |
| P1 | Jev / Agent 推理 | JevSpawn | 反馈加权分支后验与多分支保留 |
| P1 | Agent 记忆 | MemFit | append-only 原始 turn 与混合检索接口 |

每篇论文都包含统一论文信息、中文方法解读、原论文关键图、定义性机制代码、三种子 L1 指标和明确复现边界。L1 结果仅证明算子与不变量可运行，不等同于论文规模模型、私有数据、在线 A/B 或正式能力收益。

## 工业证据边界

- **RPTune** 的第一作者机构为 Google，正文报告 7 个真实商家上的目录实验，但没有量化线上 A/B；本地按学术 / Evolve 机制收录，仅复现上下文编排核心，不把原文数字写成本地收益，也不进入工业线上证据结论。
- **AgentWebRec** 没有量化线上 A/B，按用户已认可的学术 / Evolve 机制例外收录，并明确排除在工业线上证据结论之外。
- 本轮没有发现通过量化线上证据门槛的新 Meta 工业搜广推论文；官方 Meta 列表对账失败也意味着不能据此声称“没有遗漏”。

## 未进入实现队列的命中

以下条目保留在扫描 artifact 或审计结论中，不因关键词命中就生成占位 adapter：

- 仅使用 LLM/VLM 的医疗、金融、机器人、遥感等垂直应用，缺少可迁移到现有研究域的定义性机制；
- benchmark、survey、数据分析或安全审计论文，但没有本仓库可执行的新模型、目标函数或控制器；
- 普通 RL / 控制论文，与 LLM 后训练、Agentic RL、Jev 或 RSI 无直接机制关系；
- 工业搜广推候选若没有量化线上 A/B、用户明确认可的全流量证据或既有经典例外，不进入工业实现队列；
- 标题中出现 `agent`、`evolve`、`recommendation` 等词但正文任务不属于本项目四个研究域的误召回。

## 下一轮起点

由于官方交叉来源没有完成对账，下一轮仍以 **2026-10-01** 为 overlap start，直到官方来源恢复并完成未匹配标题复核；届时才把统一 watermark 推进到 2026-10-03 以后。
