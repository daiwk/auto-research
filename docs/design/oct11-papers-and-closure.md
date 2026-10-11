# 2026-10-11 论文与平台收口批次

接受范围：12 篇论文、1 项 OPD 诊断设施，以及历史状态对账、真实评测证据、可执行 Evolve 接入、回归/GPU 验证四项收口。论文首次公开日期均为 2026-10-08，不称作 10 月 11 日新发表。本页保留接受范围和验收重点；实际进度、测量及未完成项以[完整实现状态](../research-audits/oct11-implementation-scope.md)为准，不能用注册或公式单测替代交付。

| 优先级 | 论文 / 设施 | arXiv | 验收重点 |
| --- | --- | --- | --- |
| P0 | ZIP-SR / ZE-EDEN | 2610.12444 | 低精度更新、公开语言建模、可执行优化器 Evolve |
| P0 | VFold | 2610.12338 | 权重折叠数值合同与实际共享 cache |
| P0 | Option-Channel Attack | 2610.12292 | 六策略、校准隔离与条件 ASR 分母 |
| P0 | ReCal | 2610.11332 | 真实 FFN 删除、SFT→OPD 与负结果 |
| P0 | ZCPO | 2610.12161 | 有效奖励组、真实参数更新、train-only manifest |
| P1 | SparseDecoding | 2610.12327 | 解码校准与实际 CUDA bitmask kernel |
| P1 | V-CoLA | 2610.11251 | 实际 delta-state 贡献、视觉合并和层退出 |
| P1 | Data-Space Iteration | 2610.12102 | 真实 teacher / fake / generator 交替训练 |
| P1 | OnTrack | 2610.12375 | 流式对齐、生命周期、公开轨迹隔离 |
| P1 | Memento3 | 2610.11794 | 生成世界模型、安全解释、回放与失配 |
| P1 | PIVOT | 2610.11167 | 领域 few-shot、共享 warmup 和三配方 |
| P1 | SGUID | 2610.12367 | live 教师、真实持续性筛选、恢复与两轮重训练 |
| P1 诊断 | OPD Learning Signals | 2610.11247 | 表征、梯度及 occupancy 诊断而非能力收益 |

## 完成条件

- 每项保留论文核心算法；公开 checkpoint / 数据路径可执行，明确缩规模、诊断与未测边界。
- 历史候选与 manifest 自动对账，不改写冻结审查快照；不把接受候选算成已实现。
- Evolve 的 operator 必须被控制器执行、重新评测；proposal prior 不复制成 fitness。
- 完成相关行为测试、CI 门槛、生成器和文档构建；CUDA 路径在真实 A100/A30 执行并提交脱敏回执。
- 不读 gold 作为 Agent 输入，不伪造测量，不重建 uv.lock，不修改原始脏工作区。
- 最终提交单个 PR，不以本批实现自动推进审查水位。
