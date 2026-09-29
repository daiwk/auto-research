# Agent 与后训练合并批次：可执行边界

本批次将 Agent/推理效率与后训练纳入同一工作分支。机制单测、公开小模型诊断和论文完整复现是不同证据等级，不可互换。

## 已落地、可独立运行的单元

- [ToolSearcher](https://arxiv.org/html/2609.30906)：`toolsearcher_credit.py` 实现首次发现事件、组内归一化信用与“先搜齐、后选择”门控；`toolsearcher_objective.py` 实现可微的事件级 clipped policy loss，并用梯度测试确保检索返回文本不参与策略或 KL 更新。原作者[公开仓库](https://github.com/zhenlongDai/ToolSearcher)含 StableToolBench/AppWorld 训练流程。本地未运行 Qwen RL、检索器或 AppWorld 评测。
- [ActKV](https://arxiv.org/html/2609.31395)：`actkv_policy.py` 实现 Algorithm 1 的动作区域 attention-aware LRFU 选择；`actkv_budget.py` 实现 Algorithm 2 的置信度趋势和预算上调。原文的 token 公式使用 surprisal 的符号，但其“下降则增加预算”的判据描述的是 confidence；本实现先转为 confidence 再拟合，避免相反触发。尚未接入 paged attention 恢复、CUDA 原位压实、真实 Agent 回合及吞吐，因此不是端到端 ActKV。
- `paired_public_comparison.py` 要求至少三种子、同 checkpoint/数据版本和更新、生成 token 预算，仅用 validation 选方法，再报告成对 test 差值。这是对照协议检查器，**不会自行产生 Qwen 实验结果**。
- [KITE 小模型等算量诊断](sep29-kite-equal-flops.md)：公开 WikiText-2 上完成三种子、近似 FLOPs 匹配的 2+2 SST 与 4 层 dense 对照，报告 NLL 和本机末 token 延迟。它不代表论文 67B MoE 结论。

## 完整复现前的门槛

| 工作 | 尚缺的可核验证据 |
|---|---|
| ToolSearcher | 固定版本的公开 StableToolBench 与 16k 工具索引，Qwen2.5-7B/Qwen3-4B 同预算 RL/基线，AppWorld 隔离测试 |
| ActKV | 原文模型真实动作 KV，同预算 FullKV/SnapKV/R-KV，对应 paged kernel 与 A100/A30 吞吐/内存实测 |
| Code-Based Skills | 原作者 [CodeHack](https://github.com/BartekCupial/codehack) 和[基线仓库](https://github.com/BartekCupial/codehack-baselines) 已定位；尚需固定 commit、安装 NLE/MiniHack，运行 primitive/skill/mixed 同 seed 对照 |
| GRAFT/DeltaS | 各自原论文任务、模型环境及公平预算评测；已有低预算机制诊断不能替代 |
| KITE | 原论文模型/语料规模、真实长上下文、GPU prefill/decode 与吞吐；当前小模型 FLOPs 匹配仅是诊断 |
| Recursive OPSD、MaD-RL | Qwen3-4B 公开任务多 seed、同预算基线和隔离 test 结果；现有单种子 GPU 记录为诊断 |
| MuSeR | 可审计的公开商品语义与缓存刷新链路、在线/离线公平对照；当前 KuaiRand tag 代理并非原论文语义编码 |

需要 CUDA 的升级路径，只有在 A100/A30 真实运行、提交脱敏 receipt 并通过 `scripts/validate_gpu_evidence.py` 后才能标为完成。缺少公开数据或原作者环境的论文保留缺口，不使用合成替身冒充正式结果。
