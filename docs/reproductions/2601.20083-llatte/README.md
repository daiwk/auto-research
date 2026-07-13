# LLaTTE: Multi-stage sequence scaling

- 论文：[arXiv 2601.20083](https://arxiv.org/abs/2601.20083)，2026-01-27，Meta
- Adapter：`llatte`
- 代码：`src/auto_research/reproductions/llatte/`
- 数据：MovieLens 100K
- 运行：`auto-research reproduce --paper llatte --seed 42`

## 论文线上证据

Meta 在多轮大规模 A/B 中报告 Facebook Feed/Reels conversion **+4.3%**，旗舰广告排序模型 NE **-0.25%**，且 P99 ranking latency 无可测变化。

## 实现范围

实现 target-aware 在线序列注意力、pyramidal recent-token reduction，以及异步 upstream 全历史用户表示与在线分数融合。验证集联合选择 target-aware/upstream 权重；NumPy embedding 替代 MLA、DHEN、LLaMA semantic features 和 H100 serving。

## 实验协议

评分 >= 4 作为正反馈；per-user leave-two-out；validation 只用于联合选择 target-aware/upstream 融合权重，test 在调参期间不可见；完整 item catalog 排序；三个 seed。

## 本机结果（2026-07-13）

| Architecture | Hit@10 | NDCG@10 |
|---|---:|---:|
| Short online sequence | **0.0851 ± 0.0040** | **0.0420 ± 0.0021** |
| LLaTTE two-stage proxy | 0.0823 ± 0.0036 | 0.0405 ± 0.0014 |

## 结论与边界

NDCG@10 **-3.57%**。在 MovieLens 的短历史和弱内容特征条件下，异步全历史表示没有复现生产收益；这与论文强调“强语义特征是 scaling 前提”的结论一致。
