# 10 月 16 日：两项 P0、十二项 P1 与 TransX 补充升级

本批范围由用户确认，统一在一个 MR 交付。目标是可实际调用和验收的有限组件/公共评测接口，不是把完整论文实验缩成空壳。高成本完整实验统一为 **成本过高，不复现（审查 DONE）**，不进入自动重试队列，也不冒充算法实现完成。

## 接受范围与成本门槛

| 级别 | 论文 / 稳定键 | 本批实现与验收范围 | 完整实验成本依据与处置 |
| --- | --- | --- | --- |
| P0 历史补漏 | [STATIC](https://arxiv.org/abs/2602.22647) / `static-constraint-decoding` | CSR trie、向量化 token 约束、beam 状态与有限 GPU 对照 | TPU v6e / 1B 模型与 YouTube 私有线上实验；不复现 DONE |
| P0 历史补核 | [Cross-Task Relationships](https://arxiv.org/abs/2609.28776) / `cross-task-relationships` | 成对辅助头、合法多反馈标签、真实小网络梯度与公平消融 | 每日数十亿私有样本、多周训练和 YouTube 全量策略；不复现 DONE |
| 既有方法升级 | [TransX report](https://arxiv.org/abs/2610.20913) / `transx` | 多 cutoff 的精确 local/global memory、可微前缀复用与稀疏行优化器 | 32 H200，约 13 小时生产收敛；不复现 DONE |
| P1 | [Novelty Patching](https://arxiv.org/abs/2610.22100) / `novelty-patching` | 严格因果查表、训练集阈值与边界诊断 | 1.9 GB、多模型/规则/seed 原实验；不复现 DONE |
| P1 | [RoPERelay](https://arxiv.org/abs/2610.21126) / `rope-relay` | RoPE 逆变换/重定位、mask、后续 query 一致性 | 多 selector / 128K / 32B judge；不复现 DONE |
| P1 | [CoTS](https://arxiv.org/abs/2610.20642) / `cots` | 概率竞争调度、离散/soft 混合与 phase lock | 9B/12B、多长推理 benchmark；不复现 DONE |
| P1 | [TF-OPD](https://arxiv.org/abs/2610.22236) / `tf-opd` | 教师生成统计、Gram 收缩、融合线性求解 | 双 7B 约 10 GPUh，评测另计；不复现 DONE |
| P1 | [Waypoint-OPD](https://arxiv.org/abs/2610.21601) / `waypoint-opd` | 三快照 early/late shift gate 与 loss/scorer | 8B 配置约 64.31 GPUh，不含评测；不复现 DONE |
| P1 | [GGPO](https://arxiv.org/abs/2610.20814) / `ggpo` | 稳定 gap objective 与真实小策略更新 | 4 GH200、8000 更新、多 benchmark；不复现 DONE |
| P1 | [STOPD](https://arxiv.org/abs/2610.21337) / `stopd` | 生成前 cutoff、自然 EOS、IPW 与期望梯度 | 每 run 2 H100，长 rollout × 3 seeds；不复现 DONE |
| P1 | [CCE-OPD](https://arxiv.org/abs/2610.21195) / `cce-opd` | 双条件视图、support、熵 gate 与 PPO-OPD | 8B 教师、多学生、多臂与遮罩标注；不复现 DONE |
| P1 | [SIF](https://arxiv.org/abs/2610.21392) / `sif` | eligibility、双层投票、group norm 与双 loss mask | 8 A100-40GB 全参训练，多 benchmark；不复现 DONE |
| P1 公共评测 | [ToolBottleneckBench](https://arxiv.org/abs/2610.21098) / `tool-bottleneck-bench` | 官方有限任务、工具状态、exact grader、预算与失败分母 | 原 26,576 条件 / USD 768.38 托管采集；不复现 DONE |
| P1 公共结果 | [Librarian Agents](https://arxiv.org/abs/2610.22273) / `librarian-agents` | 官方 compact records 重算、filesystem / provenance 合同 | 4B builder、35B executor、60K token 轨迹与外部服务；不复现 DONE |
| P1 公共评测 | [SciPIvot](https://arxiv.org/abs/2610.21082) / `scipivot` | 已发布 options-only 双顺序与隔离评分 | 五前沿模型 × 十二条件；project histories 未公开；完整不复现 DONE |

成本为原文配置/官方要求的审查判断，不是本地运行测量。本批任何小网络、人工张量或历史分数重算都必须明确 diagnostic，不支持论文级能力提升，也不自动接入 Evolve。

## 验收状态

15 项有限组件/公共接口已实现；11 条 CUDA 路径已在 **NVIDIA A100-SXM4-80GB** 上实际执行，固定 seeds `42,43,44`。另外四项为 CPU 的确定性表拟合或官方记录审计，不假造随机 seeds，也没有调用托管模型 API。各详情页提供原文图、公式、代码入口、上游版本和实测指标。

| 验收组 | 已交付项目 | 实测产物与边界 |
| --- | --- | --- |
| 搜广推 / CUDA | STATIC、Cross-Task、TransX report | [STATIC 回执](../../gpu-validations/static-constraint-decoding-a100-20261016.json)、[Cross-Task 回执](../../gpu-validations/cross-task-relationships-a100-20261016.json)、[TransX 回执](../../gpu-validations/transx-report-components-a100-20261016.json)；有限约束解码、真实小网络消融、精确可微 memory 和优化器，不是生产收益复现 |
| 基础模型 / CUDA | RoPERelay、CoTS | [RoPERelay 回执](../../gpu-validations/rope-relay-a100-20261016.json)、[CoTS 回执](../../gpu-validations/cots-a100-20261016.json)；位置/混合算子及真实梯度，不是长上下文或推理能力评测 |
| 后训练 / CUDA | TF-OPD、Waypoint-OPD、GGPO、STOPD、CCE-OPD、SIF | [TF](../../gpu-validations/tf-opd-a100-20261016.json)、[Waypoint](../../gpu-validations/waypoint-opd-a100-20261016.json)、[GGPO](../../gpu-validations/ggpo-a100-20261016.json)、[STOPD](../../gpu-validations/stopd-a100-20261016.json)、[CCE](../../gpu-validations/cce-opd-a100-20261016.json)、[SIF](../../gpu-validations/sif-a100-20261016.json)；公开文本上的真实 tiny-policy 生成、融合或参数更新，不是预训练 LLM benchmark |
| 基础模型 / CPU | Novelty Patching | [训练集因果表拟合](../../foundation-models/2610.22100-novelty-patching/metrics/component-cpu.json)，262,144 字节、494 个训练文档；patch rate `0.100296`，不训练 BLT |
| Agent / CPU | ToolBottleneckBench、Librarian Agents、SciPIvot | [216 条工具计划审计](../../agent-research/2610.21098-tool-bottleneck-bench/README.md)、[443 问官方记录复算](../../agent-research/2610.22273-librarian-agents/README.md)、[248 case / 60 aggregate 行审计](../../agent-research/2610.21082-scipivot/README.md)；公共接口和历史结果，不是本地 Agent 能力 |

Cross-Task 三臂共享初始化与 minibatch，32 步固定预算后才读取 test；平均 validation BCE 为 baseline `0.668841`、cross-label `0.668480`，但 test BCE 为 `0.664956`、`0.665026`（越低越好），**没有得到稳定 test 改善**。保留负结果，不选择有利 seed 或据此晋升 Evolve。TransX 共享/直接计算最大前向误差 `8.89e-16`、梯度误差 `5.33e-15`；旧固定权重 NumPy scorer 的原始数字全部保留，证据改正为 concept demo，不能因新增算子就升级旧实验保真度。

首次 CUDA 执行的后训练组曾因 Waypoint 无有效梯度而失败，见[失败记录](first-cuda-failure.json)。修正的是 tiny teacher fixture 的因果首动作 REINFORCE 与固定 `8×64` 预算、`0/4/8` 快照；没有改 Waypoint 门控或降低非零梯度断言。随后冻结提交 `781a8178f12069c5c3691093b5f3ba79a48b5322` 实跑通过，逐项回执绑定执行源码 hash。

所有 15 项的**完整原实验**仍是“成本过高，不复现（审查 DONE）”，不进入自动重试队列。组件全部 `diagnostic_only: true`、`promotion_eligible: false`、`evolve_integrated: false`；这里的验收不等于完整论文复现或能力提升。

## 日期与发现口径

STATIC / Cross-Task 是历史未落地项；TransX 是已有方法的新报告补充。P1 来自 10-16 公告暴露的近期首发与更早补发现，并非全都在上次扫描后提交。本批实施不等于完成 10-16 所有公告审查，不因实现这十五项就自动推进审查水位。
