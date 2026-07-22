# PRECISE：LLM 语义与协同 ID 融合的渐进式序列预训练

> **Fidelity: 完整核心链路复现**。实际执行 LLM token hidden-state 初始化、可训练 token、top-k MoE attention、ID/text 交替训练、全场景 causal NIP、目标场景双向 Transformer、序列拼接 MLP 与 cross-user BPR。Qwen2-1.5B 缩为 SmolLM2-135M，WeChat 私有日志替换为 MovieLens-1M。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2412.06308](https://arxiv.org/abs/2412.06308) |
| 公司/机构 | Tencent / WeChat |
| 首次公开日期 | 2024-12-09（arXiv v1） |
| 原文开源代码 | 否：论文未提供官方/作者代码（核查日期：2026-07-22） |
| Adapter | `precise` |
| 本地复现代码 | [`src/auto_research/reproductions/precise/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/precise/) |

## 原始论文总结

### 背景与主要改动

纯 ID 序列模型能学协同关系，但长尾物品训练不足；纯文本/LLM 方法能迁移语义，却容易丢掉协同信号。PRECISE 将二者在 item 层融合，并把训练拆为 Universal Training（全场景兴趣）和 Targeted Training（稀疏目标场景/任务）。论文还针对文本表示过强导致 ID 学不动的问题，先冻结 token 训练 ID，再解冻联合训练。

```mermaid
flowchart LR
  T["item title / category"] --> L["Qwen2 token representations"]
  L --> E["top-k MoE attention experts"]
  I["trainable item ID"] --> F["ID + semantic concat"]
  E --> F
  F --> U["causal Transformer / all-scene NIP"]
  U --> W["warm-start all parameters"]
  W --> B["bidirectional Transformer / target scene"]
  B --> M["concat all positions + MLP"]
  M --> R["cross-user BPR / recall and ranking embeddings"]
```

### 核心公式

LLM 先产生按原文顺序排列的 token 表示，MoE 的每个 expert 用 attention 汇聚 token；gate 只激活 top-k expert：

$$
\mathbf x_i=LLM(T_i),\qquad gate(\mathbf x_i)=softmax(topk(\mathbf x_iW^{gate})),
$$

$$
\mathbf e_i=ID(i)\oplus\sum_{j=1}^{K}gate(\mathbf x_i)_j\,Attn_j(\mathbf x_i).
$$

Universal Training 使用 causal Transformer，在每个位置以其他序列采样的 item 为负例，优化 next-item sampled softmax：

$$
\mathcal L_{nip}=-\sum_{u,i}\log\frac{\exp(\mathbf h^H_{u,i}\cdot\mathbf e_{i+1})}{\exp(\mathbf h^H_{u,i}\cdot\mathbf e_{i+1})+\sum_{j\in N_u}\exp(\mathbf h^H_{u,i}\cdot\mathbf e_j)}.
$$

Targeted Training 从 UT 参数 warm-start，改为无 causal mask，并拼接所有位置后经 MLP 得到 user embedding：

$$
\mathbf h'_u=MLP(CONCAT(\mathbf h'^{H}_{u,1},\ldots,\mathbf h'^{H}_{u,n})),
$$

$$
\mathcal L_{bpr}=-\sum_u\sum_{u'\ne u}\log\sigma(\mathbf h'_u\cdot\mathbf e_{u,n+1}-\mathbf h'_{u'}\cdot\mathbf e_{u,n+1}).
$$

### 论文离线与线上效果

Amazon Books 上 PRECISE-UT 的 R@10/N@10 为 **0.0439/0.0269**，HLLM 为 0.0419/0.0227；WeChat-AllScene 为 **0.0197/0.0139**，HLLM 为 0.0174/0.0125。WeChat cold-item R@10 为 **0.0260**，较 HLLM 0.0227 提升约 14.5%。目标任务中，完整 PRECISE 的 Click R@10 为 **0.0158**（TT-only 0.0109），Share R@10 为 **0.0055**（TT-only 0.0018）。

线上排序 A/B 覆盖 1.8 亿参与者：active users **+0.174%**、clicks **+1.961%**、shares **+1.433%**、reading time **+0.884%**。召回实验中 Share-U2I 的 shares 最高 **+2.560%**。论文还描述了每日 user/item embedding 生成、U2I/U2I2I ANN recall，以及把预训练 embedding 与 dot-product 分数接入 DCN 的 serving 方式。

## 本地复现

> **本地对照口径**：基线是只做目标任务训练的 PRECISE-TT；实验组是 UT 全场景预训练后再 TT；Recall@10 **+40.00%**、NDCG@10 **+32.53%**，但 Cold Recall@10 **-50.00%**。这是预训练阶段消融，不是相对 DIN。

使用已下载到本地的 MovieLens-1M。评分 ≥3 的时间序列作为全场景正反馈，评分 ≥4 作为更稀疏的目标任务；每个用户最后一个高评分 item 留作测试，训练看不到该事件，并按原论文剔除训练目录中从未出现的测试 item。最终为 290 用户、2,822 items；电影标题和 genre 输入真实 SmolLM2-135M，缓存 8 个 contextual token hidden states，之后作为可训练变量参与 MoE 与推荐损失。

经过两轮迭代，修复了 in-batch 重复 item 被误当作互斥类别的问题，并将 TT 从 80 增到 240 steps。最终协议为 UT 120 steps（前 60 steps 冻结 token）+ TT 240 steps，3 seeds：

| Method | Recall@10 mean ± std | NDCG@10 mean ± std | Cold Recall@10 |
|---|---:|---:|---:|
| PRECISE-TT only | 0.005747 ± 0.003251 | 0.003007 ± 0.002280 | **0.011594 ± 0.004099** |
| PRECISE UT + TT | **0.008046 ± 0.004301** | **0.003986 ± 0.001879** | 0.005797 ± 0.004099 |

完整渐进训练的 Recall@10 相对 **+40.0%**，NDCG@10 相对 **+32.53%**；Recall 在 seed 43/44 提升、seed 42 持平。Cold Recall 则下降 **50.0%**，且指标绝对值很低：这说明缩小后的公开实验支持“全场景预训练缓解目标任务稀疏”这一方向，但没有复现论文的长尾收益，也不能外推到 WeChat 线上幅度。UT loss 在三个 seed 中分别从 6.661/6.615/6.613 降到 5.818/5.858/5.824。

```bash
pip install -e '.[plum]'
for seed in 42 43 44; do
  AUTO_RESEARCH_PRECISE_USERS=300 \
  AUTO_RESEARCH_PRECISE_UT_STEPS=120 \
  AUTO_RESEARCH_PRECISE_TT_STEPS=240 \
  auto-research reproduce --paper precise --dataset-dir data --seed "$seed"
done
```

LLM token cache 位于 `data/precise/`，首次生成约 5 秒，后续直接复用。数据、cache、逐次 runs 和 checkpoint 均不提交 Git；稳定标量见 [`metrics/movielens-1m-seeds42-44.json`](metrics/movielens-1m-seeds42-44.json)。
