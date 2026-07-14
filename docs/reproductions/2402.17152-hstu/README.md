# HSTU：Hierarchical Sequential Transduction Units

> 保真度：**核心机制复现**。UVQK SiLU projection、非 softmax pointwise aggregation、相对位置偏置、post-pooling normalization、U-gate、残差与 all-position 生成式训练均实际执行；未复刻异构 action/time token、stochastic-length kernel、M-FALCON 和万亿参数 serving。

论文：[arXiv 2402.17152](https://arxiv.org/abs/2402.17152) · [Meta 官方实现](https://github.com/meta-recsys/generative-recommenders)

## 背景与主要改动

工业推荐历史包含多种 action，长度与规模远超经典 next-item 数据。HSTU 把推荐统一为生成式序列建模，并用适合稀疏长历史的 transduction layer 替代标准 Transformer 的 softmax attention 和独立 FFN。

```mermaid
flowchart LR
    S["Action / item 序列"] --> E["Item + position embedding"]
    E --> P["SiLU UVQK projection"]
    P --> A["Causal pointwise aggregated attention + relative bias"]
    A --> N["Post-pooling normalization"]
    N --> G["U gate"]
    G --> R["Output projection + residual"]
    R --> O["所有位置的下一 item logits"]
```

## 核心公式

HSTU layer 先得到 \(U,V,Q,K=\operatorname{SiLU}(\operatorname{Norm}(X)W_{UVQK})\)，再计算

\[
A(X)V=\frac{1}{N}\operatorname{SiLU}(QK^\top+b_{rel})V,
\qquad
X'=X+W_O\left(U\odot\operatorname{Norm}(A(X)V)\right),
\]

并施加 causal mask。与标准 attention 不同，这里没有 softmax 归一化；训练对序列所有有效位置做 sampled-softmax next-item 预测。

## 论文报告效果

- 离线：论文 MovieLens-1M 表中，SASRec HR@10/NDCG@10 为 0.2828/0.1545，HSTU 为 0.3043/0.1700（+7.6%/+10.1%），HSTU-large 为 0.3306/0.1858。
- 在线：Meta 排序生产 A/B 中，Generative Recommender 相对 DLRM 的 engagement +12.4%、consumption +4.4%。

## 本地复现

MovieLens-100K，932 个有效用户、1,682 个物品，时间顺序 leave-two-out、全库排名。HSTU 与 SASRec 固定 64 维、2 层、2 heads、相同 sampled-softmax 目标和 320 step；种子 42/43/44，Apple MPS。

| Model | Hit@10 | NDCG@10 | Head share@10 |
|---|---:|---:|---:|
| Matched SASRec | 0.09156 ± 0.00182 | 0.04389 ± 0.00160 | 0.90665 |
| HSTU | 0.07761 ± 0.00253 | 0.03611 ± 0.00208 | 0.93877 |

HSTU 相对 matched SASRec 的 NDCG@10 为 **-17.73%**。负结果在三个 seed 上一致；当前 MovieLens 只有单一评分事件、序列较短，无法提供 HSTU 为异构 action/time 设计的主要信号。该实验验证核心 layer 和训练路径，不支持把小数据负结果外推到论文的工业规模。

审计指标见 [metrics/movielens-100k-seeds42-44.json](metrics/movielens-100k-seeds42-44.json)。

## 复现命令

```bash
AUTO_RESEARCH_HSTU_STEPS=320 auto-research reproduce --paper hstu --seed 42
```
