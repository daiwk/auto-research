# 2026-10-13 实现清单与验收范围

本轮以已合入 PR #200 的主分支为基线，接受 3 篇 P0、16 篇 P1 和扫描器改进，最终合在一个 PR。这里是执行清单，不代表已实现、已实跑或审查水位推进。

## 固定论文清单

| 优先级 | 论文 / adapter 计划键 | 原文 | 需保留的核心链路 |
| --- | --- | --- | --- |
| P0 | UxSID / `uxsid` | [2605.09040v4](https://arxiv.org/html/2605.09040v4) | Res-KmeansFSQ、兴趣锚点压缩、双层 semantic probing、真实训练 |
| P0 | State-OPD / `state-opd` | [2610.13238v1](https://arxiv.org/html/2610.13238v1) | 已执行状态与旧 reasoning 隔离、同前缀教师监督、熵预算分配、真实更新 |
| P0 | MagicBeanStalk / `magicbeanstalk` | [2610.12659v1](https://arxiv.org/html/2610.12659v1) | 分解有效性测试、可验证合成、策略难度校准、非零优势 RLVR |
| P1 | GPPO / `gppo-framework` | [2610.13015v1](https://arxiv.org/html/2610.13015v1) | f-divergence × estimator 的实际近端目标 |
| P1 | TAPO / `tapo-trajectory` | [2610.13020v1](https://arxiv.org/html/2610.13020v1) | 前缀几何比率、长度感知裁剪、局部 stop-gradient |
| P1 | CV-OPD / `cv-opd` | [2610.13264v1](https://arxiv.org/html/2610.13264v1) | 同图正负裁剪、JSD、margin 对比、token/sample gate、真实 VLM 更新 |
| P1 | OAL / `oal` | [2610.13674v1](https://arxiv.org/html/2610.13674v1) | QK 离群分组、可分离二次核、输出校准、LoRA 转换 |
| P1 | ReplaySSM / `replayssm` | [2610.13778v1](https://arxiv.org/html/2610.13778v1) | checkpoint + 输入缓冲、rollback、分离状态精度、实际 CUDA 路径 |
| P1 | LeWAM / `lewam` | [2610.12818v1](https://arxiv.org/html/2610.12818v1) | 无信息泄漏的双分支注意力、潜状态预测、action flow、潜空间正则、控制/规划 |
| P1 | SmolWAM / `smolwam` | [2610.13740v1](https://arxiv.org/html/2610.13740v1) | 真实 Cosmos trunk、单帧接口、单步蒸馏、布局课程、LIBERO 动作评测 |
| P1 | NEAR / `near` | [2610.13314v1](https://arxiv.org/html/2610.13314v1) | 邻域残差、聚类查询参考、尺度融合、单索引检索 |
| P1 | Beyond the Final Embedding / `beyond-final-embedding` | [2610.13277v1](https://arxiv.org/html/2610.13277v1) | 冻结 token 表示稀疏匹配、记忆 ID 聚合、全局融合、可选 query adapter |
| P1 | SkillDreamer / `skilldreamer` | [2609.01642v2](https://arxiv.org/html/2609.01642v2) | pseudo skill 生成、混合检索、执行中的能力重评与技能调用 |
| P1 | SynthSelf / `synthself` | [2610.13113v1](https://arxiv.org/html/2610.13113v1) | 同家族 aligner、拒绝采样、离线训练、获取/保持双评测 |
| P1 | UPTURN / `upturn` | [2610.13672v1](https://arxiv.org/html/2610.13672v1) | 冻结 encoder + MLP、失败标签训练、新 user turn 干预、预算对照 |
| P1 | DoubleCat / SemiCat / `doublecat-semicat` | [2610.13834v1](https://arxiv.org/html/2610.13834v1) | 两层插值 self-conditioning、离散 reveal、真实 diffusion LM 训练 |
| P1 | SOAR / `soar` | [2610.13157v1](https://arxiv.org/html/2610.13157v1) | 内外知识来源流、来源一致性奖励、真实策略训练 |
| P1 | GRPO 难度课程 / `grpo-difficulty-curriculum` | [2610.13669v1](https://arxiv.org/html/2610.13669v1) | 当前策略难度估计、动态难度带、过难退化对照 |
| P1 | Uncertainty-guided progressive contraction / `progressive-contraction` | [2610.12933v1](https://arxiv.org/html/2610.12933v1) | Monte Carlo 推理树、教师池收缩、学生感知路由、教师成本核算 |

UxSID 的 v1 日期为 2026-05-09，SkillDreamer 的 v1 日期为 2026-08-28；本轮关注的是它们的实质修订，不计为 10 月的新 v1。DuoRate 与 VETR 不在本轮接受范围内。

GPPO 和 TAPO 与已有的其他论文缩写重名，本轮使用 `gppo-framework` 和 `tapo-trajectory`，不覆盖 2508.07629 / 2607.27973 的已有实现。

## 扫描器范围

1. arXiv 公告页作为独立召回通道，保留公告日期、类别、new/cross-list/replacement、版本和来源证据；关键词查询失败不丢弃已取得的公告条目。
2. 补充 OPD、RLVR、LLM、JEPA、world-action、memory retrieval 等缩写和同义词查询；保留 Google/Meta 的重点全文核验优先级。
3. 对已知论文记录已审版本与元数据摘要，实质版本更新进入独立复核队列；新 v1、历史补发现、旧文更新分开汇总。
4. 查询失败、公告过期和未完成的全文审查如实列入覆盖范围和例外清单，不将“零结果”写成来源穷尽，不自动推进审查水位。

## 验收与交付

- 各条目有独立可执行入口、行为测试、中文文档、完整论文元数据和可复核指标。
- 真正的公开数据训练与原文结果分开；缩小规模、未运行原 benchmark、负结果和诊断等级明确标注。
- Agent 策略不得读取 gold answer/plan；外部 verifier 只在训练奖励/离线评估边界内读取标签。
- CUDA 路径在用户指定的 A100/A30 实跑，提交脱敏、绑定执行 commit 的 receipt。
- 运行相关算法测试、文档生成一致性、GPU evidence gate 和完整 CI 契约；未完成的项目必须明确报告，不以通过单测代替完成范围。
- 完成后提交一个 PR，不自动合并或部署。

## 当前执行检查点（尚未收口）

| 部分 | 当前可核验进度 | 仍需完成 |
| --- | --- | --- |
| 扫描器 | 公告独立召回、缩写查询、版本复核队列、Google/Meta 官方来源优先级、限时重试；相关回归测试已运行 | 真实增量扫描与完整版本基线登记；不自动推进水位 |
| UxSID | 四结构真实 CPU 训练入口、属性编码、残差量化、双层 probing、同 SID 缓存一致性 | 完整公开协议复核、A100/A30 多 seed、adapter/spec/中文详情与指标 |
| State-OPD | 状态隔离、完整响应扩采、Appendix D.1 双裁剪、真实 checkpoint 更新入口、无 gold 的算术工具环境 | 真正 GPU 交互训练、原 benchmark 边界复核、adapter/spec/中文详情与指标 |
| GPPO / TAPO | 12 种 divergence/estimator 组合、两侧 log 的独立定义、局部梯度构造、真实 rollout/LoRA 训练入口 | GPU 非零优势更新与对照、adapter/spec/中文详情与指标 |
| 其余 15 篇 | 固定清单和原始来源缓存；作者公开仓库已开始核验 | 核心算法、可执行集成、实验、文档与证据均未完成 |

这四篇的代码目前是实施中的模块，**尚未作为验收完成的论文发布到 registry/公开目录**。不能把上述阶段进展说成 19 篇已完成。

UxSID 的一次 CPU 诊断使用固定公开 SmolLM2-135M 属性编码器、100 用户、10,719 条训练、100 条 validation 和 100 条 test、1 epoch/seed 42。Validation 选择的是 `agnostic` 消融；UxSID 的 test AUC 为 0.5848，对照为 0.5916。这是小规模负结果，保留在本地运行产物，不代表原论文或稳定能力比较。其缓存与直接计算最大差异为 0。

新增标签访问的角色复核：`proximal_checkpoint` 与 `state_opd/checkpoint` 的参考答案只进入独立 verifier；`ArithmeticEnvironment` 的 `arguments.answer` 是模型自己的提交，不是参考答案。生成器/教师消息均不接收数据参考答案，行为测试覆盖此边界。环境步数计数仅反映实际 `step` 调用，不独立作为任务能力证据。

A100 已通过只读连通/显存检查，已有公开 Qwen2.5-0.5B 与 7B 校验清单。当前尚未执行本轮 GPU 训练、同步新资源或签发新 receipt；并行代理和本轮源码/公开资源同步授权正在等待用户确认。
