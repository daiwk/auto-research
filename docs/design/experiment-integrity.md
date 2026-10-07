# 实验可信度与运行契约（MR-A）

本次统一解决四组问题：证据晋级、断点恢复与缓存、负结果记忆、超时及 GPU 并发。
不改变论文算法，不把历史诊断实验改名为能力评测，也不删除已有实验数据。

## 证据统计不等于能力证明

`evidence_policy.assess_evidence` 是复现报告、三 seed 汇总和公开看板的共同判定入口。
三个不同 seed 只是必要条件，不会把 L0/L1、concept demo、gold-derived 候选或明确
`diagnostic_only / promotion_eligible=False` 的实验晋级。混合输入按最弱证据处理。

正式比较需要实际实验提供以下 `comparison_contract`，不能由文件名或文档推测：

| 字段 | 事实来源 |
|---|---|
| `protocol_id` | 本次执行的版本化评测协议 |
| `dataset_revision` | 公开数据版本或内容 hash |
| `split_revision` | 实际 train/validation/test 划分版本或 hash |
| `baseline` | 同协议下实际执行的冻结基线 |
| `code_revision` | 实现版本/内容 hash |
| `test_isolated` | test 未用于结构、参数或候选选择的显式保证 |

聚合还检查 seed 对齐、重复 seed、失败记录和不同 seed 的协议冲突。
正式比较不自动等于“有提升”；统计显著性、效应大小与复现边界仍需单独判断。
Evolve 的 validation 候选选择共用诊断排除规则，但少量 seed 的探索本身不算正式结论。

历史产物里的指标和原始声明不改写。看板按新规则重新审核展示，缺失契约的历史结果
显示“未满足正式比较协议”，不伪造缺失版本，也不把真实测量降为不存在。
原始 JSON 可能保留旧 `formal_comparison`；使用时以新 policy 的审核结果为准。

## ExperimentSpec 与恢复运行

`experiment_contract.py` 保存版本化参数、输入内容 hash 和实现源码 hash。
输入文件按内容计算，不按 mtime，不仅以目录名缓存，不截断为前 10000 个文件。
首次运行会有一次读取输入的成本，尤其是大 checkpoint；这是恢复正确性的成本，不是训练预算。

`result.json` 保存 `experiment_spec`；相同内容的代码/数据才可恢复。
允许增加 generations，以及调整 output/resume 位置、workers、CPU threads、GPU slots、
每任务显存预算和负结果文件位置。不能降低 generations；数据、seed、steps、population、
结构选择条件、checkpoint、设备或超时重试预算变化需开启新 run。
没有指纹的旧 run 仍可阅读，不能无证据地继续选冠军。

每一代在执行前保存完整候选计划和父代；中断后只执行未完成 trial。
各代使用确定性的独立随机序列，完成顺序不会改变平分时的选择。
同一恢复目录拒绝并发写入。最终 test 也受硬超时约束；失败会保留 validation 轨迹并报错。

三 seed 汇总的 `state.json` 同样绑定参数、输入和实现版本，不再仅按方法/seed 复用缓存。
公开数据应预先准备；输入目录内容变化会拒绝复用既有 state，避免不同数据混合。
Topic research 的 trial cache 也纳入数据内容与本地实现版本，外部命令仍必须显式提供 revision。

## 负结果适用范围

新条目绑定 ExperimentSpec、完整 genome 和比较基线，而不是单独 architecture 名。
一次学习率失败不封禁其他学习率；代码、数据或基线变化时可以重新探索。
临时 runtime failure 不作为永久跳过依据，由有界重试处理。
旧条目保留供审计，缺少细粒度身份时不用于自动排除方法。

## 执行与资源控制

baseline、单 worker、多 worker、重试和最终 test 都在 spawn 子进程执行。
时间预算包含子进程启动、评估与所有重试；达到预算终止并回收子进程，支持的环境同时清理其进程组。
注入的 evaluator 必须可以被 spawn 序列化；不能依赖父进程内存副作用。
结果通过管道及时接收，避免等待子进程退出时大结果填满队列。

先解析 `auto` 的真实设备，再使用 GPU slots 与所选 CUDA 设备的可用显存限制并发。
显存预算不足一个任务时明确报错，不强行启动。实际显存仍受其他用户进程影响；slots 是本控制器的上限。

运行 CUDA 验证：

```bash
python scripts/validate_mra_gpu.py --data data --output runs/mra-gpu --commit <tested-commit>
```

脚本实际执行公开 MovieLens 数据上的 RankMixer 训练、validation/test，以及 CUDA
参数更新、1/2 槽位并发和超时回收。该运行是调度与设备烟测，不是论文效果比较。
回执只保留指标、公开数据 hash、随机初始化说明、加速器型号、源码版本与命令，排除机器路径和身份信息。

## 范围与剩余 MR

MR-A 的回归集中在 `tests/test_experiment_integrity.py`，并运行受影响合同及全套质量门禁。
MR-B 才处理惰性 registry、最小安装、扫描检查点/覆盖状态、统一论文 spec 和日期批次拆分。
本次不声称已完成 MR-B，也不声称已逐篇重跑全部论文。
