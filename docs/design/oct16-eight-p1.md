# 10 月 16 日八项 P1：有界组件与评测接口

用户要求八项合在一个 MR，完整高成本实验不跑，CUDA 路径在真实 A100/A30 验证。
本批是实现收口，不是新一轮完整审查；不改变 `2026-10-15T15:39:55+08:00` 审查水位。

## 固定范围

| 项目 | 必须实际执行 | 验证与不作的声明 |
| --- | --- | --- |
| OOB Regularization | Gaussian-quantile / spherical CPU锚点缓存、实际训练、定期刷新、匹配in-batch基线 | 固定官方CIFAR训练子集内train/validation隔离；真实CUDA有限步数，不重做多数据100epoch研究 |
| transparent-compact | 保留对话原文、工具调用桩、显式删减标记、恢复索引 | CPU真实消息输入；不假造LLM记忆准确率，不运行完整27B/128k多臂评测 |
| FormCraft | 从论文独立实现类型序列组合、验证准入、持久库、递归复用 | CPU真实算子和独立holdout；上游未明示许可不vendor，不把序列域收益称LLM能力 |
| DrOPD | top-k并集/JS路由、候选reward、PPO clipped更新、真实online token rollout | 有界tiny自回归模型与公开文本、冻结teacher/隔离validation；不跑原11.83h及数学benchmark研究 |
| RAP-Walk | clarity/cycle可靠度、stationary credit、entropy tempering、GRPO优势混合 | CPU图/数值对照与CUDA backward；不训练视频模型/大judge，不声称视频效果 |
| CTXGAP | 固定版本公开数值表复算与聚类CI、observer/reference隔离、外部结果导入 | 历史结果复算≠独立重评；T_public≠T_full，失败不隐去，不运行原37run采集 |
| Selective Reasoning | 固定作者小发布包的CPU测量复算、gate/read/stop接口 | 缺原始prefix trace/cache边界保留，不将历史测量重算当在线模型能力 |
| CLASHarness | 固定官方格式/轨迹分析、gold与被测view隔离、缺陷与公平性审计导入 | 不执行不受信任轨迹命令，mock仅诊断；不下载8.5GB整库/重跑15模型付费评测 |

## 成本及证据门槛

- 仅使用单张A100或A30，一次只在一台运行实际实验。
- 小型公开资料可固定revision/hash下载；GPU优先原有缓存，不新增GB级checkpoint。
- CUDA默认验证控制在分钟级，有限步数/样本上限和超时显式入产物；失败和负结果保留。
- 所有完整高成本研究明确为 **成本过高，不复现（审查 DONE）**，使用 `not_reproduced_high_cost`，不进入自动重试/实现队列。
- CUDA回执绑定实际运行源码commit及hash、公开输入revision、seed/command/metrics和型号；不写主机、SSH别名、用户名、驱动或机器build字符串。
- 组件、历史复算和接口均不自动进入evolve能力晋级；测试/三seed不升级证据等级。

## 已执行的组件验收

| 项目 | 本轮实际结果 | 入口与证据 |
| --- | --- | --- |
| OOB Regularization | A100 三 seed、四训练臂各40步、512训练/128验证图像；每个OOB臂4次CPU锚点刷新；统一CLI与独立脚本同seed一致 | [论文与代码](../reproductions/2610.20158-oob-regularization/README.md)、[CUDA回执](../gpu-validations/oob-regularization-a100-20261016.json) |
| transparent-compact | 真实公开Pi会话196条消息；保留54段原文；145项删减负载按hash精确恢复；没有模型调用 | [论文、命令与CPU产物](../agent-research/2610.20116-transparent-compact/README.md) |
| FormCraft | 三seed真实CPU组合搜索、库快照落盘、销毁内存再冷加载；同一冷加载库每seed 12目标/24项配对最终测试通过 | [论文与序列域结果](../agent-research/2610.19414-formcraft/README.md) |
| DrOPD | A100三seed，独立初始化微型自回归学生，真实在线生成每seed64tokens并完成2次PPO更新；冻结教师未变化 | [论文与边界](../post-training/2610.19572-divergence-routed-opd/README.md)、[CUDA回执](../gpu-validations/divergence-routed-opd-a100-20261016.json) |
| RAP-Walk | A100三seed、每seed两张显式诊断图；平稳残差低于1e-9，真实GRPO backward与参数更新 | [论文与边界](../post-training/2610.20089-rap-walk/README.md)、[CUDA回执](../gpu-validations/rap-walk-a100-20261016.json) |
| CTXGAP | 官方37任务/4799有效探针、10,000次聚类bootstrap，与固定数值参考逐项一致；另有公开输入/评分侧隔离接口 | [论文与CPU统计验收](../agent-research/2610.20003-ctxgap/README.md) |
| Selective Reasoning | 9组/29,808行官方测量，16,888项固定数值全部复核通过；实现不读取gold的start/read/stop接口 | [论文与CPU复核](../system-one/2610.19644-selective-reasoning/README.md) |
| CLASHarness | 导入775项审计checks与306项保守并集、104条精选参考记录；保留1条零required不可评分记录；完整inventory缺失时不判完整成功 | [论文与接口验收](../agent-research/2610.19128-clasharness/README.md) |

OOB的A100短预算均值差为Gaussian / Contrastive各 **+0.02083**，但前者跨seed标准差为0.05083，
且CPU单seed曾得到两个负差值；这些小样本不支持稳定收益结论。DrOPD只有微型模型机制证据，
RAP-Walk没有视频或judge调用。CTXGAP、Selective和CLASH的作者历史分数不作为本地模型成绩。
所有八项均不进入Evolve自动晋级；高成本原研究为`not_reproduced_high_cost`且审查DONE。

### 真实验收发现并修复的问题

- DrOPD原实现把学生留在eval模式，CPU允许而cuDNN拒绝RNN反传；改为临时eval与明确train前向。另按附录修正为`round(ρN)`第K大阈值路由，含K=0和ties边界；补回归后在A100重跑。
- OOB统一入口误用共享设备函数参数；按真实runtime合同修复，覆盖CPU/CUDA/显式卡索引/MPS拒绝，并实际验证统一CUDA入口。
- CTXGAP补齐零质量cluster、有限数值权重及外部调用前计划检查；官方统计精确复算不变。
- CLASH只收到部分verdict不得报完整成功；公共输入是调用方声明的信任边界，不宣称字段过滤已证明全文无答案。
- 透明压缩补齐Pi原始toolCallId、错误与执行状态元数据，并在真实公开会话上重新验证；最终活跃JSON为138,550字符，旧值129,010只保留为修复前记录。
- FormCraft原实验只返回内存库计数，现已真实保存每seed不可覆盖快照并从冷加载对象执行两臂配对，固定数据划分和搜索计数未变。

## 交付检查

八项独立代码、可运行命令、算法/协议边界测试、实际有界运行结果、中文论文说明和重要原图，
补齐统一metadata与分类目录。集成后执行规格/元数据/指标/GPU证据验证、全量回归及严格文档构建，
核对单个PR的真实URL、diff和CI。未完成项必须如实列出，不通过重命名证据或放宽断言凑完成。
