# Agent 与后训练合并批次：可执行边界

本批次将 Agent/推理效率与后训练纳入同一工作分支。机制单测、公开小模型诊断和论文完整复现是不同证据等级，不可互换。

## 已落地、可独立运行的单元

- [ToolSearcher](https://arxiv.org/html/2609.30906)：`toolsearcher_credit.py` 实现首次发现事件、组内归一化信用与“先搜齐、后选择”门控；`toolsearcher_objective.py` 实现可微的事件级 clipped policy loss，并用梯度测试确保检索返回文本不参与策略或 KL 更新。原作者[公开仓库](https://github.com/zhenlongDai/ToolSearcher)含 StableToolBench/AppWorld 训练流程。本地未运行 Qwen RL、检索器或 AppWorld 评测。
- [ActKV](https://arxiv.org/html/2609.31395)：`actkv_policy.py` 实现 Algorithm 1 的动作区域 attention-aware LRFU 选择；`actkv_budget.py` 实现 Algorithm 2 的置信度趋势和预算上调。原文的 token 公式使用 surprisal 的符号，但其“下降则增加预算”的判据描述的是 confidence；本实现先转为 confidence 再拟合，避免相反触发。尚未接入 paged attention 恢复、CUDA 原位压实、真实 Agent 回合及吞吐，因此不是端到端 ActKV。
- `paired_public_comparison.py` 要求至少三种子、同 checkpoint/数据版本和更新、生成 token 上限，仅用 validation 选方法，再报告成对 test 差值。[Recursive OPSD 官方 GSM8K 三种子诊断](../reproductions/2609.30652-recursive-opsd/README.md)和 [MaD-RL Qwen 三种子诊断](mad-rl-mechanism.md)已在 A100 运行，均未观察到优势；后者仍是合成五选项任务，不是原论文数学/代码基准。
- [KITE 小模型等算量诊断](sep29-kite-equal-flops.md)：公开 WikiText-2 上完成三种子、近似 FLOPs 匹配的 2+2 SST 与 4 层 dense 对照；另在 A100 测量随机初始化小模型的 CUDA prefill/decode，未见明确延迟优势。两者都不代表论文 67B MoE 结论。
- Code-Based Skills：已固定原作者 CodeHack 与定制 NLE wheel 的公开版本，并在 Linux 隔离环境用真实 `MiniHack-Room-5x5-v0` 跑通 primitive/skill/mixed 三种动作空间、各三种子、共 9 个 episode，均无运行错误。`scripts/run_codehack_minihack.py` 与[脱敏运行摘要](evidence/codehack-minihack-seeds42-44.json)可复核。控制器只是 seeded uniform random，三个动作空间大小不同，**不能**拿各模式完成率比较方法优劣；原作者 baseline 仓库只作版本参照，未执行其单卡 LLM 评估或八卡训练流程。

已安装原作者 `codehack` 和其 README 指定的定制 NLE wheel 的 Linux 环境可复跑环境检查：

```bash
python scripts/run_codehack_minihack.py \
  --seeds 42,43,44 --max-decisions 8 --primitive-budget 64 \
  --output runs/codehack-minihack-smoke.json
```

## 完整复现前的门槛

| 工作 | 尚缺的可核验证据 |
|---|---|
| ToolSearcher | 固定版本的公开 StableToolBench 与 16k 工具索引，Qwen2.5-7B/Qwen3-4B 同预算 RL/基线，AppWorld 隔离测试 |
| ActKV | 原文模型真实动作 KV，同预算 FullKV/SnapKV/R-KV，对应 paged kernel 与 A100/A30 吞吐/内存实测 |
| Code-Based Skills | 原作者 [CodeHack](https://github.com/BartekCupial/codehack) `3026cdb7`、[基线仓库](https://github.com/BartekCupial/codehack-baselines) `ba2c532b` 与定制 NLE 已核对；真实 MiniHack 九个环境 episode 跑通，但随机控制器不等于原文 LLM policy，还须运行相同模型、数据、决策/原始步数预算下的三模式对照 |
| GRAFT/DeltaS | 各自原论文任务、模型环境及公平预算评测；已有低预算机制诊断不能替代 |
| KITE | 原论文模型/语料规模、真实长上下文与吞吐；小模型 CUDA prefill/decode 已测但仅为 launch-bound 微基准，不是论文速度复现 |
| Recursive OPSD、MaD-RL | Qwen3-4B 三种子同预算诊断与隔离 test 已完成，均为负结果；仍缺原文训练分布、原文基准和对应预算，因此保持机制/公开任务诊断，不宣称原文成绩 |
| MuSeR | 可审计的公开商品语义与缓存刷新链路、在线/离线公平对照；当前 KuaiRand tag 代理并非原论文语义编码 |

需要 CUDA 的升级路径，只有在 A100/A30 真实运行、提交脱敏 receipt 并通过 `scripts/validate_gpu_evidence.py` 后才能标为完成。缺少公开数据或原作者环境的论文保留缺口，不使用合成替身冒充正式结果。
