# 2026-10-04：10-02 公告七篇补漏实现

## 范围与扫描状态

本轮交付用户批准的三个 P0 和四个 P1：Jev lookahead、T2SPO、Weakest-Link、CMP、TESS、RLCPR、Mingbird。它们来自 10-02 已公告窗口的遗漏核查，不是几小时里新发表七篇。来源为官方 arXiv 全文与论文作者链接；没有使用 DeepXiv。

本轮不是新的全领域分页扫描，也没有完整重跑 Google/Meta 机构来源，因此 `coverage_complete=false`，watermark 保持 **2026-10-02**，下轮仍从 **2026-10-01** 重叠复核。

## 交付清单

| 级别 | 方法与来源 | 实现 | 证据边界 |
|---|---|---|---|
| P0 | [Jev lookahead](agent-research/2610.01834-jev-lookahead/README.md) | 克隆模拟 + 新可用动作 + System One provider | L1；诊断 provider，不报 ALFWorld 成功率 |
| P0 | [T2SPO](post-training/2610.00388-t2spo/README.md) | 真实 TabPFN、支持集标准化/SVD、信用分配和裁剪目标 | L1；TabPFN CPU 官方 checkpoint、合成状态 |
| P0 | [Weakest-Link](post-training/2610.00332-weakest-link/README.md) | 所有前缀约束、吸收惩罚、全词表即时梯度 | L1；实际小策略优化，不是 LLM 蒸馏 |
| P1 | [CMP](agent-research/2610.02070-causal-memory-policy/README.md) | 随机检索曝光、Hájek 与风险决策 | L1；随机干预测量，不是长期删除能力 |
| P1 | [TESS](foundation-models/2610.02092-tess/README.md) | 两模型顺序训练、PVM selector 与独立池评分 | L1；合成分类模型，不报语言模型提升 |
| P1 | [RLCPR](post-training/2610.01458-rlcpr/README.md) | 熵分桶和集中后验条件下的长度惩罚 | L1；公式/梯度实验 |
| P1 | [Mingbird](agent-research/2610.02001-mingbird/README.md) | 可移植 M1/M3/M4/M5 与真实工具验收循环 | L1；脚本策略，不报真实 Agent 准确率 |

这些是**可调用机制 API**，没有虚构注册成支持全流程的 `auto-research reproduce` adapter，也没有仅靠 registry 标签宣称接入 Evolve。

## 运行方式

```bash
PYTHONPATH=src python scripts/run_oct04_seven_papers.py
python -m pytest tests/test_oct04_seven_papers.py
```

TabPFN 使用单独环境（固定 `tabpfn==2.2.1`），命令及 checkpoint revision 见 T2SPO 页面。实际三 seed MAE 分别为 0.00290、0.00138、0.00234；状态中的剩余距离本身是合成可学习特征，这个小误差不代表真实环境预测能力。原论文文本编码器和完整 RL 训练不在该证据内。

Weakest-Link 三动作优化把高成本动作概率均值从 0.3546 降至 0.01036；TESS selector 的 PVM 均值由 0.0803 降至 0.0129。CMP 每个记忆都获得 100 次曝光。所有产物 `diagnostic_only=true`，即使三个 seed 也不能进入正式能力排行榜。

## 未完成项

完整 benchmark、真实 LLM/托管 Jev、跨任务记忆效用与各论文大规模训练仍未完成；详见[唯一路线图](research-roadmap.md)。这批没有新增声明为 CUDA 的执行路径，不能宣称 A100/A30 验证。CMRec 的 Amazon-M2 数据阻塞与其他历史边界不被本轮覆盖。
