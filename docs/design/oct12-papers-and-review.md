# 2026-10-12：16 项实现与固定窗口审查收口

用户接受范围：上一轮短名单的全部 P0/P1，以及两篇 10 月 8 日补漏，合为一个 MR。
与实现并行，完成四轨、双召回通道和 Google/Meta 来源审查；审查闭环通过后才将水位从
2026-10-07 推进到 2026-10-12。不能用这些实现完成代替候选全集审查。

扫描冻结时刻：2026-10-12T12:55:18+08:00。目标窗口 2026-10-08～2026-10-12，
另保留前置公告重叠与月份编号补查；只声明冻结时刻实际来源覆盖，不声称当天结束或全网穷尽。

| 优先级 | 论文 / 设施 | arXiv | 负责范围 | 实际状态 |
|---|---|---|---|---|
| P0 | Evo² | 2610.13025 | Agent / RSI | 已实现；[A100](../gpu-validations/oct12-evo2-a100.json) SFT + 4次真GRPO；8题GSM搜索诊断，circle失败保留 |
| P0 | FORTE | 2610.13806 | 工业搜广推 | 已实现；[A100三seed](../gpu-validations/oct12-forte-a100.json)全部保留基线，未选择下线特征 |
| P0 | RSI-Anything | 2610.13912 | Agent / RSI | 已实现；[A100](../gpu-validations/oct12-rsi-anything-a100.json)预测器更新与pair gate，circle收益仍为0 |
| P0 | BranchOPD | 2610.13481 | 后训练 | 已实现；[A100](../gpu-validations/branch-opd-a100-20261012.json)12分支、8次PBR约束及真实参数更新 |
| P0 | CAST OPD | 2610.13257 | 后训练 | 已实现；[A100](../gpu-validations/cast-opd-a100-20261012.json)跨tokenizer对齐512token；独立`cast-opd`命名空间 |
| P1 | Road MOPD | 2610.13521 | 后训练 | 已实现；[A100](../gpu-validations/road-mopd-a100-20261012.json)39张量冲突/投影；两算术子域，非原专科教师 |
| P1 | MSAR | 2610.13630 | 基础模型 | 已实现；[A100三seed](../gpu-validations/oct12-msar-a100.json)字节模型实训；参数量不等，不作正式收益比较 |
| P1 | Orthros | 2610.13735 | 基础模型 | 已实现；[A100三seed](../gpu-validations/oct12-orthros-a100.json)训练与KV等价核验；NLL负结果保留 |
| P1 | DualQuant | 2610.13767 | 基础模型 | 已实现；[A100](../gpu-validations/oct12-dualquant-a100.json)公开135M权重全线性层；软件量化，非原生FP4加速 |
| P1 | BoundaryEvo | 2610.13285 | 后训练 | 已实现；[A100](../gpu-validations/boundary-evo-a100-20261012.json)原门槛下完成1次Stage2真实更新；第二轮无合格教师轨迹而跳过，早期负结果保留 |
| P1 | JANUS | 2610.13194 | Agent / RSI | 已实现；[A100](../gpu-validations/oct12-janus-a100.json) SDPA真实搜索/执行/技能演化完成，执行负结果与旧eager OOM保留 |
| P1 | T2Mem | 2610.13348 | Agent | 已实现；[A100](../gpu-validations/oct12-t2mem-a100.json)两官方query完整98session；外部token F1为0 |
| P1 | RATED | 2610.13889 | Agent 工具检索 | 已实现；[A100](../gpu-validations/oct12-rated-a100.json)双encoder训练/反馈bandit；原API缺失，执行失败率保留 |
| P1 设施 | Jev Agent 工作流评测 | 2610.13092 | Jev / Agent | 已实现；[A100三seed测量](../gpu-validations/oct12-jev-workflow-measurement-a100.json)真实checkpoint生成、成本单位与sandbox；非JeV权重能力复现 |
| 补漏 | WOVEN | 2610.12417 | 多模态 | 已实现；[A100](../gpu-validations/oct12-woven-a100.json)原图与transition训练；测试负结果保留 |
| 补漏 | Unsupervised Multimodal Reward Modeling | 2610.12707 | 多模态 / 奖励 | 已实现；[A100](../gpu-validations/oct12-umrm-a100.json)冻结VLM探针、验证器自举/重训；未测得best-of-N收益 |

ECC 2610.13066、Google 用户模拟器 2610.13617 属于待资料候选，不在这 16 项实现承诺内，
但本批审查必须核验后给出延期 / 排除 / 接受理由，不能静默丢弃。其他召回候选同样逐项记录终态。

## 不可跳过的验收

- 原论文核心模型、目标、策略和实际执行路径保留；不得用固定候选或 fixture 能力分数替代。
- 每篇中文独立页完整元数据、方法、公式、架构、原图、原文结果、可运行入口和本地边界。
- L0、L1、L2 / 论文能力收益分开，负结果、截断、失败与无效更新保留。
- 新 CUDA 入口执行真实 A100/A30，固定公共 checkpoint/data revision 与源码提交；只提交脱敏回执。
- Controller 不读 gold，test 不用于选择；Evolve 只有真实执行并重新评价才算接入。
- 不修改原始脏工作区，不重建 uv.lock，不合并或部署；最终只有一个待审 MR。
- 四轨两个通道完整召回、全部候选审查、Google/Meta 官方来源与非阻塞例外清单一致，通过严格覆盖审计后才改水位。

## 恢复位置

工作分支 `codex/oct12-papers-and-review`，基线 `origin/main` 已含合并的 PR #199。
16项已完成有边界的算法/运行设施实现与实际GPU执行；这不是16篇原论文能力收益的完整复现。
审查水位已按来源闭环推进到10月12日，其他已审候选仍独立留队，不等于全库候选已实现。

## 新增 label / counter 路径的逐角色复核

`fidelity-source-inventory.json` 是审查索引，不是能力通过证明。本批在更新索引前核对了以下数据流：

| 路径 | 允许的 label / 状态用途 | 禁止的用途与验证 |
|---|---|---|
| `GSMHarnessEvaluator` | 官方 train-only validation 的 answer 仅在外部数值评分器读取；执行器输入 question + 生成的 PROMPT | 进化角色只得到 question/output SHA 与 correctness，不读参考答案或执行器原文；`test_oct12_agent_gsm_harness.py` 覆盖输入隔离与固定分区 |
| T2Mem entrypoint | `memory.answer` 是生成方法；query 的参考 answer 只在生成后算外部 token F1 | 不把 query label 传入记忆或生成接口；方法不是原文 LLM-judge 准确率 |
| WOVEN / COCO 加载 | WOVEN 旋转后正确字母用于训练目标和模型输出后的评分；COCO caption 是训练/验证 label | `woven_prompt` 的模型输入只含题目、选项与图像，gold flag 不进入 prompt；公开来源 group 先分区再训练/选层，test 不用于选择 |
| BoundaryEvo | 外部 analyzer 可以参考训练集 answer；fresh teacher 输出在外部 `verified_reward` 验证后才用于 SFT | student / expert / teacher generation 不读参考答案；无效 analyzer 不补值，未通过门槛不做 Stage2 更新；`test_oct12_post_training.py` 覆盖这些边界 |
| harness 执行计数 | `calls` 只描述尝试次数，配合实际 sandbox、冻结权重摘要和逐次输出 SHA | 计数增长不能替代执行证据、正梯度或参数更新；零优势优化器动量漂移不算 GRPO 学习 |

这些入口仍是有边界的 L1 机制实跑，不因多 seed、回执或语法审计自动升级为原论文能力复现。

## 最终本地验收

- 全套 `python -m pytest -q`：1,857项通过，退出码0；没有排除Boundary或削弱验收断言。
- 16份真实GPU回执通过验证；93条执行源码SHA256逐一匹配各自实际执行commit，不用最终HEAD倒填旧实验。
- `compileall`、Ruff、paper specs check/validate、fidelity inventory、基础wheel最小安装与CLI manifest检查通过；registry现有387个adapter。
- 指标schema-v2审计739份、平台完成审计、严格论文覆盖审计与实现对账通过。这里的“完成审计”不意味着正式能力比较完成。
- manifest/catalog/696条公开实验看板生成后再次运行无diff；`mkdocs build --strict`通过。
- 缓存、checkpoint、原始模型输出、机器连接信息和`uv.lock`均未加入本轮变更。GitHub CI以最终PR中的实际状态为准，不用本地检查冒充远端绿灯。
