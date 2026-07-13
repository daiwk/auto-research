# Memento: RAG-style long-retention recommendation

- 论文：[arXiv 2605.24051](https://arxiv.org/abs/2605.24051)，2026-05-22，Meta
- Adapter：`memento`
- 代码：`src/auto_research/reproductions/memento/`
- 数据：MovieLens 100K

## 入选原因

Meta 经过多轮大规模 A/B 将 Memento 部署到主要 CTR/CVR 模型，报告 Facebook Feed/Reels CTR **+1.0%**、Offsite Conversion CVR **+1.2%**。

## 实现范围

实现 query-conditioned MMR，在长期历史中平衡相关性与冗余度，验证集选择 MMR 权重，并与 LastN 对照。公开实验不包含 Meta 的 365 天 embedding corpus、INT8 serving、Ember 和 Data Memento replay。

## 本机结果（2026-07-13）

| History method | Hit@10 | NDCG@10 | Head share@10 |
|---|---:|---:|---:|
| LastN | 0.0901 | 0.0443 | 0.2979 |
| Memento MMR | **0.0966** | **0.0464** | 0.3093 |

NDCG@10 **+4.78%**。MMR 的相关性权重由验证集选择为 0.30，说明这个数据上保留多样性比纯相似度检索更重要；热门曝光有小幅上升，需要在更大数据集继续验证。
