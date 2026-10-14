# 2026-10-13 实现清单与验收范围

本轮以已合入 PR #200 的主分支为基线，接受 3 篇 P0、16 篇 P1 和扫描器改进，最终合在一个 PR。这里是执行清单，不代表已实现、已实跑或审查水位推进。

**2026-10-14 交付范围变更：18 篇可执行机制实现与扫描器改进；MagicBeanStalk 仅保留研究资料、实验源码和失败证据。** 用户要求 MBS 待验收、先交付其余成果，随后新增强制成本门槛。MBS 标为“成本过高，暂不复现”，移出可执行 registry 和公开 runner；原 CUDA 规格原样归档，不伪造回执或降低门禁。19 篇固定审查清单保留，不等同于 19 篇实现全部完成。审查水位仍为 2026-10-12，本轮不因实现交付推进。

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
| P1 | DoubleCat / SemiCat / `doublecat-semicat` | [2610.13834v1](https://arxiv.org/html/2610.13834v1) | 无额外前向的两层连续插值、离散 reveal、真实 diffusion LM 训练 |
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

- 已验收的18篇有独立可执行入口、行为测试、中文文档、完整论文元数据和可复核指标；MBS保留待验收实验材料，不能冒充可执行实现。
- 真正的公开数据训练与原文结果分开；缩小规模、未运行原 benchmark、负结果和诊断等级明确标注。
- Agent 策略不得读取 gold answer/plan；外部 verifier 只在训练奖励/离线评估边界内读取标签。
- CUDA 路径在用户指定的 A100/A30 实跑，提交脱敏、绑定执行 commit 的 receipt。
- 运行相关算法测试、文档生成一致性、GPU evidence gate 和完整 CI 契约；未完成的项目必须明确报告，不以通过单测代替完成范围。
- 完成后提交一个 PR，不自动合并或部署。

## 当前执行检查点（尚未收口）

| 部分 | 当前可核验进度 | 仍需完成 |
| --- | --- | --- |
| 扫描器 | 公告独立召回、缩写查询、版本复核队列、Google/Meta 官方来源优先级、限时重试；相关回归测试已运行。本轮明确审查的 19 篇版本/固定全文来源已登记到 `paper-discovery-versions.json` | 其他历史论文没有假设版本基线；真实新扫描的覆盖与例外仍需单独闭环，不自动推进水位 |
| UxSID | 四结构、943 用户、MovieLens-100K 实际 A100 三 seed 训练、同 SID 缓存一致性、adapter/spec/中文详情与绑定源码的实测指标 | 全局生成同步与 CI；本次没有稳定提升，不是工业线上复现 |
| State-OPD | `6aabe57a` A100 默认/完整历史 OPD/无扩采三臂各三 seed，九项实际更新及源码/原始 SHA 核验完成；8 题 accuracy 前后均为 0 | 全局 CI；原三个 benchmark 未运行，不宣称能力提升 |
| GPPO / TAPO | 原快照 A100 三 seed 真实更新，独立 GRPO-control 三 seed 完成；原文与本地指标分开 | 统一指标/目录/CI 核验；8 题短预算仅支持机制诊断，不宣称稳定能力收益 |
| DoubleCat-SemiCat | 修正后的无额外前向核心在 A30 新快照三 seed 实跑，参数变化、实际调用数与负结果已核验 | 全局 CI；原完整 benchmark 未运行，不复用旧标准 SC 结果 |
| CV-OPD / OAL / ReplaySSM | A100 三 seed 与对照/回放实跑及脱敏回执核验完成；CV-OPD 六臂负差值、OAL seed 44 不优、ReplaySSM 编译兼容边界均保留 | 全局 CI；非原论文完整能力或 serving 效率比较 |
| NEAR / Beyond | A30 八项实跑；共享 bank 各三 seed及严格 bank-disjoint 各一项，固定编码器/切分与原始 SHA 核验完成 | 全局 CI；同数据三 seed 非独立重复，严格切分仅两条 test，非官方 benchmark |
| SkillDreamer | `47f0e9ce`完整三臂×42/43/44 A100结果逐字段核验并签机制回执：1931次响应、195501tokens、348次CSI、44题加载、285次方法成功计算器调用；no-skills平均20.83%，direct/方法均0。独立observer为`27adb791`，原raw/trace与7字段复算一致 | 只支持L1机制执行，零提交/负结果保留，不代表能力提升；最终整批CI与同步待完成。42有短教师诊断重叠，43/44并行，墙钟不作效率比较 |
| LeWAM | `0f5dca9f` A100 三 seed 原生联合训练与新候选三臂闭环已核验，均无规划优势 | 全局 CI；目标来自训练轨迹，非 holdout，未运行原完整训练预算 |
| SmolWAM | `2b84c377` A100 三 seed 均完成 teacher KD、两布局课程及新学生同初态闭环；24 次真实更新，学生与 no-op 均零成功，源码/原始文件/新权重绑定独立核验通过 | 全局 CI；旧 adapter 输入失败保留，缩放单任务诊断不是正式能力或原规模复现 |
| SynthSelf / Progressive contraction | 完整42/43/44 native和独立回执已从实际raw复算并保存。SynthSelf seed43 retention为0，Contraction三seed均与full-SFT相同，负结果保留 | 最终整批目录与CI；不宣称稳定能力提升或总计算节省 |
| UPTURN | 完整42/43有真实救援信号，44救援优势全0、只有熵梯度，保持failed-no-rescue-signal。失败native与完整执行cohort已核验保存 | 最终整批同步与CI；不生成三种子全通过回执、不为通过挑预算 |
| MagicBeanStalk（延期） | `4c4710cd`新greedy路径已实际A100结束：314.887秒、34814tokens，77条响应与构造audit独立回放一致。root4的新学生/教师baseline为25%/100%，无经验零成功学生；root7/8教师独解失败，无合格后代/0RL。教师短诊断仍单独保留，不当整方法结果 | 成本过高，暂不复现；缺整方法通过回执，43/44未启动。用户已要求先交付其他成果；不再试跑，已移出可执行范围，保留原规格和失败材料 |
| SOAR | `b9086275` A100默认42/43/44×两臂六个实际run已逐字段复算；方法12次、消融10次真更新，消融43准确率0保留；独立三seed回执已保存 | 最终整批目录与CI；仅4条validation/seed的L1机制诊断，不是稳定能力或原benchmark复现 |
| 难度课程 | `b9086275` A30默认42/43/44×五臂15个实际run已独立复算并签新源回执；151次真实更新、38个等值组精确跳过，staged42准确率0与too-hard非零更新均保留 | 最终整批目录与CI；三seed仍仅L1，不复用旧数值异常controls、不宣称稳定相对提升 |

原源码快照 `ccad3e67` 与后续不可变快照均已保存；各项运行绑定自己的不可变源，不互换。课程修后默认十五项计划和SkillDreamer完整三种子计划已完成。MBS完整方法仍缺回执，但按用户决定从可执行交付范围分离；统一GPU门禁继续审核每个活跃CUDA adapter。本表不代表19篇通过最终验收；registry、单测和提交不能替代实际验证。

本地目录/原图合同、基础wheel安装及文档严格构建已通过；新增教师短诊断和SkillDreamer严格成本摘录后稳定完整回归为2878项通过、24warnings、304.79秒。随后`4c4710cd`教师采样隔离及相关检查174项通过，明确绑定内层源码的全量回归也以exit0结束、24warnings；之后新增的证据整理工具仍须各自定向核验及最终集成检查。仍不能冒充GPU门禁通过，远端CI尚未触发。详见[本地收口检查点](../research-audits/oct13-local-closeout.md)。

UxSID 的一次 CPU 诊断使用固定公开 SmolLM2-135M 属性编码器、100 用户、10,719 条训练、100 条 validation 和 100 条 test、1 epoch/seed 42。Validation 选择的是 `agnostic` 消融；UxSID 的 test AUC 为 0.5848，对照为 0.5916。这是小规模负结果，保留在本地运行产物，不代表原论文或稳定能力比较。其缓存与直接计算最大差异为 0。

新增标签访问的角色复核：`proximal_checkpoint` 与 `state_opd/checkpoint` 的参考答案只进入独立 verifier；`ArithmeticEnvironment` 的 `arguments.answer` 是模型自己的提交，不是参考答案。上述被评估策略消息不接收参考答案，行为测试覆盖此边界。SynthSelf 的离线 aligner 与独立 self-builder 则按论文训练构造角色读取 train gold；不能把其构造生成与无 gold 的 student 评估推理混称。环境步数计数仅反映实际 `step` 调用，不独立作为任务能力证据。

A100 原有四篇实跑已产生绑定 `7e125fd0` 的脱敏 GPU receipt；新快照验证启动时 SSH 在认证代理阶段关闭连接，不能宣称任务已启动。大资源传输中断保留断点；旧结果不覆盖新路径。用户已批准三个分领域实现代理，以及本轮相关源码/脚本和固定版本公开资源的同步，新增资源总量不超过 20 GB；不传私有数据、密钥或整个工作区。

以上连接失败是 10 月 13 日的历史记录；10 月 14 日后续实际执行情况以本页当前表格和各篇绑定源码的回执为准。新增 MBS 配对根题只从 train 读取标签，参考答案仍只在构造 verifier / RL 训练奖励边界使用，不进入被评估策略消息。

本轮另接受收尾清理要求：先检查本地占用，删除可重建的站点、构建和打包残留，保留源码、未提交改动、实验结果（含失败）、验证凭据和有复用价值的公开数据/权重缓存；清理不等于删除历史研究证据。
