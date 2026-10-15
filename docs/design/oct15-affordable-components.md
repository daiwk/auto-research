# 10 月 15 日五项低成本组件与接口

本批从已合并的 PR #203 继续。用户明确要求实现下午候选中的低成本组件和接口，
不是重新打开完整高成本实验。审查水位、旧审查决定与实现验收分开保存。

## 固定范围与验收

| 论文 | 本轮必须可执行的范围 | 验证 | 不执行的完整研究 |
| --- | --- | --- | --- |
| CASI，2610.20293 | 一次检索后的不可变快照、去重合并、coalition value 缓存、精确/置换 Shapley、组共享标准差、真正的有界零和投影与 token/action advantage 映射 | 加性、交互、负边际、快照冻结、查询次数、均值与边界性质；有界实际机制运行 | 私有广告拍卖、LLM 生成与多轮策略训练、生产收益复现 |
| PN-Mix，2610.19605 | RoPE pair-norm 精度分配、1-bit 重构中点校正、sink/residual 保护；量化结果实际进入 attention/cache 消费路径 | CPU 公式/边界对照与 A100/A30 实际推理诊断 | 8B–32B 多模型、32K 长输出、多任务完整扫评与生产吞吐结论 |
| SMRC / PMRC，2610.19844 | 子空间外残差、基更新修正及原文对应优化器更新；可保存/恢复真实 optimizer state | 数值更新、换基/满秩/零梯度边界、实际参数更新与 CUDA 验证 | 2–8 卡、最高 26.84B token 的多规模预训练 |
| Meta AutoformBench | 固定上游 revision 的341任务清单、source-free 边界、任务导出/执行配置、官方结果导入和协议校验 | 真实公开清单/结果解析；未知/重复 task、缺失结果、预算与条件不一致必须拒绝 | 九类 frontier 模型的长轨迹 Lean 评测；不下载教材，不将原排行榜 source-present 条件冒充本地 source-free 成绩 |
| JEPA prediction vs planning，2610.19375 | 冻结 decoder 的表示/预测/超额误差、训练集共享方差、episode 隔离、成对规划结果、分层配对 bootstrap 与退化/噪声检查 | 不等长 episode、种子配对、零方差、负结果与预测变好但规划不变的受控案例 | 三环境重新训练、完整 checkpoint ladder、多 decoder/planning seed 研究 |

所有结果默认是组件/接口或 L0/L1 机制验证，`diagnostic_only`，不能自动进入 Evolve
作为能力提升证据。不用私有拍卖、金标策略或虚拟 Lean 成功响应代替原论文运行。

## 成本与运行约束

- 单张 A100 或 A30，一次只占用一台；优先使用已有公开数据和 checkpoint 缓存。
- 先完成 CPU 合同与有界资源检查；GPU 验证按组件控制在分钟级，整个批次不启动小时级研究。
- GPU 运行绑定不可变源码 commit；只同步本轮相关源码/脚本，保存脱敏回执与负结果。
- 大资源、完整成本仍实质不明或运行超出本批上限时，停止该完整实验并明确记为
  **成本过高，不复现（审查 DONE）**，不以放松断言、删失败或廉价替代算法凑完成。
- AutoformBench 的原文首页日期、软件引用日期、官方发布页日期语义不同；未证实的首次公开日不补造。

## 当前状态

以下状态对应实际代码和运行产物；所有完整高成本实验仍为“不复现（审查 DONE）”。本轮不是新来源扫描，不修改 `2026-10-15T15:39:55+08:00` 的审查截至时间。

| 项目 | 实现 | 本地/公开输入运行 | CUDA（如适用） |
| --- | --- | --- | --- |
| [CASI](../reproductions/2610.20293-casi/README.md) | 完成：快照/信用/优势组件 | 五动作 31 子集、三种子置换诊断；不是策略训练 | 不适用，仅 CPU |
| [PN-Mix](../reproductions/2610.19605-pn-mix/README.md) | 完成：真实位打包和缓存消费 | CPU 与 A100 随机初始化输入；不是预训练 LLM 评测 | [A100 三 seed + 统一 CLI](../gpu-validations/pn-mix-a100-20261015.json) |
| [SMRC / PMRC](../reproductions/2610.19844-smrc-pmrc/README.md) | 完成：真实优化器和保存恢复 | 六对照二次问题/小 MLP，保留负结果 | [A100 三 seed + 统一 CLI](../gpu-validations/smrc-pmrc-a100-20261015.json)；含 FP16/BF16 |
| [AutoformBench](../agent-research/autoformbench/README.md) | 完成：清单、执行计划、结果/协议接口 | 固定 341 任务与九 CSV 共 3069 行；严格预算拒绝真实超额行 | 不适用，未执行 Lean/模型 |
| [JEPA 评测协议](../foundation-models/2610.19375-jepa-prediction-planning/README.md) | 完成：冻结 decoder、误差分解与配对统计 | 受控数组实际 MLP 拟合、泄漏/聚合/负结果单测；无新规划轨迹 | 不适用，仅 CPU |

## 真实失败和集成复核

SMRC/PMRC 首轮 A100 运行发现独立 CPU oracle 依赖该 Torch 构建未包含的 LAPACK；
改用 NumPy 的相同 FP64 SVD/QR 后通过，未改 CUDA 优化器、数学公式或数值容差。
PN-Mix 与 SMRC/PMRC 都发现并修复了统一 CLI 默认退回 CPU 的路由问题；现在脚本与
统一 CLI 均在 A100 实跑，seed42 的关键数值相同。失败和修复依据保留在各篇回执。

所有五篇均补中文方法、完整元数据和原论文关键图；分类目录只显示真实组件/接口状态，
AutoformBench 的未知首次公开日仍未知。没有新增自动 Evolve 能力晋级或小时级训练。

## 本地验证

- 全量回归：`3254 passed, 1 skipped`（约 4 分 55 秒）；Mac 无 CUDA 的单元检查被跳过，独立 A100 实跑另有回执。
- 基础 wheel 仅安装基础依赖后，元数据发现与 CLI 检查通过，没有隐式加载 Torch/Transformers。
- Ruff、规格生成/校验、指标 schema、GPU 回执、平台完整性、审查覆盖与实现对账通过；生成文件重跑无差异。
- 严格文档构建通过；清理本轮约 412 MB 临时环境、网页构建和重复 PDF，保留公开输入缓存与小型验证证据。

PN-Mix 的可选真实 checkpoint 提取接口没有实际权重端到端验收，不在默认缓存组件的
GPU 回执范围内；当前没有把它广告为已验证模型适配。GitHub CI 以该 MR 最新提交的 checks 为准。

最终合为一个 MR，核对完整五项范围、生成文档、GPU 回执与必需 CI；不自动合并或部署。
