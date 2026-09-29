# Agent 与后训练合并批次：可执行边界

本批次将 Agent/推理效率与后训练纳入同一工作分支，但不把机制单测等同于论文复现。

## 已落地的机制

- [ToolSearcher](https://arxiv.org/html/2609.30906)：`toolsearcher_credit.py` 实现原文式 (2)、(5)、(7) 的首次发现事件、组内归一化信用与“先搜齐、后选择”的门控。原作者[公开仓库](https://github.com/zhenlongDai/ToolSearcher)含 StableToolBench/AppWorld 训练流程。本地目前只检验信用分配，不宣称完成 Qwen RL、检索器或 AppWorld 评测。
- [ActKV](https://arxiv.org/html/2609.31395)：`actkv_policy.py` 实现 Algorithm 1 的动作区域 attention-aware LRFU 选择。原文的 paged attention 恢复、CUDA 原位压实、真实 Agent 回合及吞吐未接入；因此这里只是算法单元，不是端到端 ActKV。

## 完整复现前的门槛

| 工作 | 尚缺的可核验证据 |
|---|---|
| ToolSearcher | 公开 StableToolBench 数据和 16k 工具索引固定版本、Qwen2.5-7B 或 Qwen3-4B 的同预算 RL/基线、AppWorld 测试 |
| ActKV | 原文模型的真实动作 KV、同预算 FullKV/SnapKV/R-KV 对照、paged kernel 和 A100/A30 吞吐/内存实测 |
| Code-Based Skills | 原作者 CodeHack 可获取仓库、NetHack/MiniHack 环境、primitive/skill/mixed 同 seed 对照 |
| GRAFT/KITE/DeltaS | 各自原论文任务/模型环境与公平预算评测；已有低预算诊断不能替代 |
| Recursive OPSD、MaD-RL | Qwen3-4B 公开任务的多 seed、同预算基线与隔离 test 结果 |
| MuSeR | 公开商品语义与缓存刷新链路的可审计数据、在线/离线公平对照 |

GPU 路径只有在 A100/A30 真实运行、提交脱敏 receipt 并通过 `scripts/validate_gpu_evidence.py` 后才能标成完成。
