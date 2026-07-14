# PinFM：Foundation Model for User Activity Sequences

> 保真度：**核心机制复现**。NTL/MTL/FTL 对比预训练、预训练后下游微调、candidate early fusion、Candidate ID Randomization、backbone 低学习率和 DCAT 均实际执行；省略 Pinterest 多 action/surface 语料、fresh-item age dropout、分布式 20B embedding、int4 与 Triton kernel。

论文：[arXiv 2507.12704](https://arxiv.org/abs/2507.12704) · 机构：Pinterest

## 背景与主要改动

PinFM 把“先在跨场景用户行为上预训练，再接入各排序模型微调”的 Foundation Model 范式带到工业推荐。decoder-only backbone 学习 next/multi/future token；下游把候选追加到用户序列做 early fusion。DCAT 利用同一请求的候选共享用户历史，把 context self-attention 只算一次，然后让候选对缓存的 context KV 做 cross-attention。

```mermaid
flowchart LR
    U["跨场景用户 ID 序列"] --> P["Decoder-only pretraining"]
    P --> L["NTL + MTL + FTL"]
    L --> W["Pretrained backbone"]
    W --> C["一次 context self-attention + KV cache"]
    I["候选 ID + 内容特征"] --> X["Candidate cross-attention"]
    C --> X
    X --> R["下游排序 loss + NTL 微调"]
```

## 核心公式

预训练表征为

\[
H=\phi_{out}\!\left(M\left(\phi_{in}(E_{item}+E_{action}+E_{surface})\right)\right).
\]

单个未来物品使用 InfoNCE：

\[
\ell(H_i,z_j)=-\log\frac{e^{H_i^Tz_j/\tau}}
{e^{H_i^Tz_j/\tau}+\sum_k e^{H_i^Tz_k^-/\tau}}.
\]

\(L_{NTL}\) 预测下一 token，\(L_{MTL}\) 预测未来窗口，\(L_{FTL}\) 从下游固定长度位置预测后续窗口。DCAT 对去重 context 计算并缓存 \(K_u^l,V_u^l\)，候选层执行：

\[
X_c^l=g\!\left(Attn(Q_c^l,[K_u^l;K_c^l],[V_u^l;V_c^l]),X_c^{l-1}\right).
\]

本实现保留这一数学分解并在全库评估中真实复用 context KV，不以普通 pooled Transformer 代理。

## 论文报告效果

- 离线：Homefeed Save HIT@3 中 PinFM-base +2.91%、GraphSAGE-LT +3.76%；加入 CIR、age dropout 与 GraphSAGE-LT 后，28 日内新物品 Save HIT@3 +17.72%。
- 在线：95% 置信水平显著；Homefeed sitewide/surface/fresh Saves +1.20%/+2.60%/+5.70%，I2I sitewide/surface Saves +0.72%/+2.09%。
- 效率：DCAT serving throughput +600%、training throughput +200%；int4 A/B 相对全精度业务指标中性。这些基础设施结果未在本地冒充复现。

## 本地复现与两轮迭代

MovieLens-100K，932 个有效用户、1,682 个物品，时间顺序 leave-two-out、全库排序；两个模型均为 165,426 参数。scratch DCAT 直接做下游训练；PinFM 先做 NTL+MTL+FTL，再以 backbone 1/10 学习率微调。Apple MPS，种子 42/43/44。

| Round | Pretrain / finetune | Validation conclusion | Test NDCG change |
|---|---:|---|---:|
| 1（保留） | 160 / 160 | PinFM 0.01318 vs scratch 0.01409（-6.46%） | -3.57% |
| 2 | 240 / 320 | PinFM 0.01765 vs scratch 0.02020（-12.66%） | +1.54% |

第二轮测试集：

| Model | Hit@10 | NDCG@10 | Head share@10 |
|---|---:|---:|---:|
| Scratch DCAT | 0.03004 ± 0.00303 | 0.01343 ± 0.00170 | 0.75569 |
| PinFM | 0.02682 ± 0.01139 | 0.01295 ± 0.00648 | 0.20165 |

两轮都没有验证 validation 相关性收益，因此按 validation 选择退化较小的 160/160，而没有采用 test 偶然为正的长训练轮次。所选配置 test **-3.57%** 且方差较高，不能判定稳定相关性提升；同时 head share 降低 55.40 个百分点，说明预训练显著改变了长尾覆盖。MovieLens 缺少论文决定迁移价值的跨 surface、多 action、亿级 ID 语料，继续堆 step 更可能过拟合，因此停止迭代。

审计指标见 [metrics/movielens-100k-seeds42-44.json](metrics/movielens-100k-seeds42-44.json)。

## 复现命令

```bash
auto-research reproduce --paper pinfm --seed 42
```
