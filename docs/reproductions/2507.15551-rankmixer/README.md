# RankMixer: Scaling industrial ranking with token mixing

> **Fidelity: 完整核心链路复现**。本地模型实际训练 parameter-free multi-head token mixing、per-token FFN、ReLU-routed Sparse MoE 和 dense-training/sparse-inference；仅缩小字段、参数与 serving 工程规模。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2507.15551](https://arxiv.org/abs/2507.15551) |
| 公司/机构 | ByteDance / Douyin |
| 首次公开日期 | 2025-07-21（arXiv v1） |
| 原文开源代码 | 否：论文未提供官方/作者代码（核查日期：2026-07-22） |
| Adapter | `rankmixer` |
| 本地复现代码 | [`src/auto_research/reproductions/rankmixer/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/rankmixer/) |

## 原始论文总结

### 背景与主要改动

传统 ranking feature-cross 模块 MFU 低，扩大参数常同时推高延迟。RankMixer 把异构字段分为等宽 feature tokens，以无参数 head/token 重排代替 self-attention；每个输出 token 使用独立 FFN，防止高频字段支配共享参数。Sparse 版本为每个 token 配独立 experts，以 ReLU router 和稀疏正则允许不同 token 激活不同数量的 experts，并使用 dense-training/sparse-inference 避免 expert 欠训练。

```mermaid
flowchart LR
  A["user / sequence / candidate fields"] --> B["feature-group tokens"]
  B --> C["split each token into H heads"]
  C --> D["parameter-free cross-token concat"]
  D --> E["per-token FFN or Sparse MoE"]
  E --> F["residual + layer norm"]
  F --> G["ranking score"]
```

### 核心公式

核心 token mixing 为

$$
s^h=\operatorname{Concat}(x_1^h,\ldots,x_T^h),
$$

per-token FFN 为

$$
v_t=W_{t,2}\operatorname{GELU}(W_{t,1}s_t+b_{t,1})+b_{t,2},
$$

ReLU routing 为

$$
G_{i,j}=\operatorname{ReLU}(h(s_i)_j),\qquad v_i=\sum_jG_{i,j}e_{i,j}(s_i).
$$

### 论文离线与线上效果

论文离线 RankMixer-1B 相对生产 baseline 的 Finish/Skip AUC 最高约 `+0.95%/+1.82%`；MFU 从 4.5% 提升到 45%。全流量线上部署报告 Active Days `+0.3%`、App duration `+1.08%`。

## 本地复现

> **本地对照口径**：基线是 Shared FFN；实验组分别是 Dense per-token RankMixer 与 Sparse MoE；Dense NDCG@10 约 **+595.86%**，Sparse **+43.61%**。这是 token-FFN 架构消融；Sparse 没有追平 Dense，不能只报告最佳 Dense 增益。

四个公开 token 分别来自 genre profile、近期行为、最后行为和 candidate；64d、2 blocks、4 experts，训练 240 step。shared FFN、dense per-token FFN、Sparse MoE 使用同一采样与 full-catalog test。

| Architecture | Parameters | Hit@10 | NDCG@10 | Head share@10 |
|---|---:|---:|---:|---:|
| Shared FFN | 181,121 | 0.0054 | 0.0020 | **0.0888** |
| Dense per-token RankMixer | 379,649 | **0.0247** | **0.0136** | 0.6262 |
| Sparse MoE RankMixer | 647,457 | 0.0075 | 0.0028 | 0.4171 |

Dense per-token 参数隔离得到最大准确率，验证了论文核心设计方向；Sparse 相对 shared NDCG 提升 `43.61%`，但远未追平 dense，而且更偏头部，因此**没有验证本地 ReLU/DTSI 配置能够无损稀疏化**。公开数据无法测 MFU、kernel fusion 和量化延迟。

结构化指标：[metrics/movielens-100k-seed42.json](metrics/movielens-100k-seed42.json)。

```bash
pip install -e '.[neural-recs]'
auto-research reproduce --paper rankmixer --dataset-dir data --seed 42
```

原始运行目录只保存在被 Git 忽略的 `runs/`。
