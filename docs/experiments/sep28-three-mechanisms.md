# 2026-09-28：三篇新论文的可执行机制批次

> **状态：缩比机制实验，不是三篇论文的完整复现。** 本批只把已核对公式的
> 路径落成可测试代码。没有使用答案/计划作为 Agent 输入，也没有将合成
> 状态或小模型结果冒充论文公开基准。Amazon-M2 尚不可用，CMRec 不在本批。

## GRAFT：跨轨迹图信用分配

| 论文信息 | 内容 |
|---|---|
| 论文 | [arXiv:2609.28963v1](https://arxiv.org/html/2609.28963v1) |
| 一作机构 | 上海交通大学（工作期间在腾讯 AI Platform 实习） |
| 首次公开 | 2026-09-24 |
| 原作者源码 | 论文写明“将公开”，[所指仓库](https://github.com/xcyao00/GRAFT)截至本次核查返回 404，故按**未找到可用源码**处理 |
| 本地 key / 代码 | `graft-mechanism`；`src/auto_research/agent_research/graft.py` |

论文把同一任务多条 rollout 合成状态—动作图，对终止节点赋予结果奖励，
通过 Bellman 迭代求中间状态值，再以 `γV(s')−V(s)` 给单步分配信用。
本地实现原文 Eq. 5–10 的**精确状态匹配**分支，按原始边计数求经验
转移概率和 Graph GAE；测试验证一条失败轨迹中的早期有益动作仍可取得
正信用，且同一终止状态不能携带互相冲突的标签。

有一个值得继续核查的边界：在本地完整经验边、精确 Bellman 收敛下，
每个后继节点的平均 TD 残差为零，Graph GAE 项数值退化为一步 TD。
它不构成对论文其他近似图/训练设置的反证；本批也未运行 LLM policy
更新、ALFWorld/WebShop 或 embedding 相似状态合并。

### 公开工具环境里的可训练策略对照

为了检查图信用能否用于真实动作选择，现另用仓库已有的 `toolroute-l2.1-v1`
无金标工具环境训练一个 **tabular softmax 工具策略**。策略只读取任务 observation、
工具 tag 和实时反馈；训练结束后才运行独立 validation/test 任务族。对照为相同任务、
轮数和学习率的终局结果 REINFORCE。这里的策略不是 LLM，环境也不是论文的
ALFWorld/WebShop，因此仍只属于诊断，不登记正式 GRAFT adapter。

```bash
PYTHONPATH=src python scripts/run_graft_public.py \
  --seeds 42,43,44 --train-episodes 36 --evaluation-episodes 60 \
  --epochs 4 --learning-rate 0.25
```

每 seed 训练 36 个任务、4 轮，validation/test 各 60 个任务；三 seed 的 test
联合成功率对两法均为 `0.7778`，计划步骤 F1 均为 `0.8535`，平均工具成本均为
`5.3176`。本次预算下**图信用没有带来可测提升**。精确经验图在 Bellman
收敛时多步平均 TD 残差接近零，且当前任务公开 tag 已使多数步骤只有一个可选
动作；这两点均限制了此诊断对论文优势的检验力。三 seed 逐项结果见
[公开指标产物](metrics/graft-public-toolroute-l21.json)。结果不支持将 GRAFT 提升为
正式 L2 论文复现，也不把它作为 Evolve 的已证实算子。

## KITE：只由 Prefiller 生成 KV 的双塔

| 论文信息 | 内容 |
|---|---|
| 论文 | [arXiv:2609.27294v1](https://arxiv.org/html/2609.27294v1) |
| 一作机构 | StepFun |
| 首次公开 | 2026-09-23 |
| 原作者源码 | 论文正文未提供可核实的模型/训练源码，**未找到公开代码** |
| 本地 key / 代码 | `kite-sst-small`；`src/auto_research/foundation_models/kite_sst.py`、`scripts/run_kite_sst.py` |

本地先训练两层 Prefiller，再从其参数扩展出两层 Decoder，第二阶段联合
训练两个塔。Decoder 对齐读取 Prefiller 每层 KV；Decoder 本身不写 KV，
所以 bulk prefill 可以跳过历史位置的 Decoder 计算，只对 prompt 最后
位置运行它。单 token 增量 decode 与整段前向的最后位置 logits 在测试中
误差低于 `1e-5`，梯度确实到达 Prefiller KV 投影和 Decoder query。

运行方式（CPU-only；公开 WikiText-2，训练/验证/测试原文件隔离）：

```bash
PYTHONPATH=src python scripts/run_kite_sst.py --data-root data \
  --source-steps 30 --continuation-steps 30
```

固定三 seed `42,43,44`、每 seed 从训练文本抽 8×33 byte 样本，验证/测试
各抽 64×33 byte 样本。SST 与两层 source-only 控制均使用相同训练样本、
60 次更新和中途 optimizer 重置；SST 在中途扩展。结果是**负结果**：

| 指标（NLL↓） | SST 2+2 层 | source-only 2 层 |
|---|---:|---:|
| 验证，三 seed 均值 | 3.6152 | 3.5942 |
| 测试，三 seed 均值 | 3.6241 | 3.6057 |

SST 为 64,704 参数，对照为 43,648 参数；它没有在这个微预算设置里
提升质量。`last_only` 与完整 Decoder 的最后位置 logits 最大误差在三
seed 均不超过 `7.2e-7`。这只验证 KV 不变量和小模型训练路径，**不**
支持论文的 67B MoE、同 FLOPs scaling、端到端 prefill 延迟或下游任务结论。
脚本输出每 seed 与 WikiText-2 文件 SHA-256，便于重跑。

## DeltaS：线性注意力状态漂移决定 KV 保留

| 论文信息 | 内容 |
|---|---|
| 论文 | [arXiv:2609.27470v1](https://arxiv.org/html/2609.27470v1) |
| 一作机构 | Maum AI Inc. / Seoul National University |
| 首次公开 | 2026-09-23 |
| 原作者源码 | [论文给出的仓库](https://github.com/MaumAI-Company/DeltaS) 可访问但截至本次核查为空；**未找到可运行源码** |
| 本地 key / 代码 | `deltas-eviction`；`src/auto_research/multimodal/deltas_eviction.py` |

实现原文 Eq. 3 的层平均相对 Frobenius 状态变化，并按原文算法保留
attention sink、最近窗口及分时间桶的高漂移旧 token。空桶额度会补给
其余高分 token；反复淘汰仍保留原始位置 ID，不依据后续问题重排。
单测覆盖状态漂移、固定预算、时间桶和再次淘汰。状态必须由真实
Gated DeltaNet 推理器提供；本批未接 Qwen3.5-9B 视频 checkpoint，
未运行 Video-MME/MLVU，因此**不能**声称论文准确率或吞吐改善。

## 下一步与边界

三项均未登记为正式 reproduction adapter，也不暴露给 Evolve：目前还没有
可公平选择的完整下游评测。需要推进时分别补 GRAFT 的可训练 Agent
policy/无泄漏环境、KITE 的同 FLOPs 规模梯队与真实延迟、DeltaS 的
Qwen3.5 视频状态/KV 适配和等预算公开视频评测。Meta MaD-RL 另见
[已有机制实验](mad-rl-mechanism.md)，仍待真实 checkpoint 数学/代码任务。
