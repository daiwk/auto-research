# 2026-10-02 P0/P1 论文扫描与实现收口

## 扫描口径

- 时间窗口：2026-09-30 至 2026-10-02；另外回补 Google 2026-05-15 的企业 LLM 全文证据遗漏。
- 一手来源：arXiv 官方摘要、HTML/PDF，Google Research 官方论文页，作者官方仓库与项目页。
- 优先级：Google、Meta 优先；工业搜广推必须读取全文部署与实验章节，摘要未出现 A/B 不能直接淘汰。
- DeepXiv：未使用。
- 去重：按 arXiv ID、标题、adapter key 和既有发现台账交叉检查。

## 本批结论

本批共实现 17 篇：P0 7 篇、P1 10 篇。所有论文均有独立详情页、中文机制说明、原论文关键图、三种子 L1 机制指标和边界说明。

### P0

| 论文 | 领域 | 收录依据 | 本地实现 |
|---|---|---|---|
| Gemini for Google | 基础模型 | Google 29,000 开发者盲 A/B | 企业数据与通用 replay 混合目标 |
| GEAR | 搜广推 | 抖音 7 天、每组 5% 流量 A/B | BasisVQ 与碰撞重排 |
| DARS | 后训练 | Agentic RL 依赖奖励 | 依赖失效、修复和 potential 差分 |
| ActiveSaddler | Agent | 主动课程优化 harness | 动态 failure arm 与探索/利用 |
| Safety Must Survive Self-Improvement | Agent/RSI | 自改进安全协议 | 当前验证、founder 回滚 |
| Range-GRPO | 后训练 | 奖励区间上的组相对优化 | 区间成对关系 advantage |
| VeriHarness | Agent | 长程任务验证 harness | 证据支持、冲突与共识挑战 |

### P1

| 论文 | 领域 | 收录边界 | 本地实现 |
|---|---|---|---|
| Effective Training Time | 搜广推基础设施 | 用户批准的生产部署例外，不作为推荐效果 A/B | ETT 分解与损耗归因 |
| TACO | 基础模型 | CUDA 路径必须真实 GPU 验证 | 列一稀疏方向与低精度列状态 |
| VETO | 多模态基础模型 | CUDA 路径必须真实 GPU 验证 | 空间先行、时间后继 token 压缩 |
| Mem++ | Agent | 组织长期记忆 | 非破坏写入、as-of 与混合检索 |
| DeFA | Agent | 失败归因 | 依赖反向传播与 decisive error |
| My FAULT | 后训练 | Agentic RL 信用分配 | 经验证自诊断与终局 credit 守恒 |
| FloWright | Agent/RSI | workflow 自进化 | 拓扑感知层级 credit |
| Where-OPD | 多模态后训练 | 合成空间场景 OPD | spatial mask 上的 on-policy KL |
| GrIS | 生成式推荐 | 用户批准的学术/Evolve 例外，无线上 A/B | 图引导层级 Semantic ID |
| REPAIR | 个性化推荐 | 用户批准的学术/Evolve 例外，无线上 A/B | 冻结 cache 上的 preference state 修复 |

## 证据边界

- GEAR 和 Gemini for Google 的线上结果只作为原论文结果记录，本地 L1 指标不复述为线上收益。
- ETT、GrIS、REPAIR 的例外写入统一元数据；它们不会进入工业论文证据结论。
- DARS 官方仓库截至本次检查仍标注代码在准备中，因此“原文开源代码”明确写为未发布，而不是仅凭仓库存在标为开源。
- TACO 与 VETO 只有在 A100/A30 的真实 CUDA receipt 通过校验后，才能作为完成项交付。

## 后续重叠窗口

下次增量扫描从 **2026-10-01** 开始，保留至少两天重叠，覆盖 arXiv 跨日修订、官方页面延迟和正文证据回补。
