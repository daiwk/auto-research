# β-OPSD：从策略优化闭式解回到自蒸馏

> 保真度：实现 reference/privileged teacher 几何插值、可控 β 与 return-to-go 权重；不冒充论文 Qwen3 训练。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [β-OPSD（arXiv 2607.28582）](https://arxiv.org/abs/2607.28582) |
| 公司 / 机构 | University of Maryland, College Park |
| 首次公开日期 | 2026-07-30 |
| 原作者代码 | 未发现/未发布官方实现（核查日期：2026-08-01） |
| 本地 adapter / 算法键 | `beta-opsd` |
| 本地复现代码 | [`src/auto_research/post_training/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/post_training/) |

## 原始论文总结

### 背景与主要改动

论文指出 vanilla OPSD 是 β=1 的 KL 正则策略优化特例。先推导 reference policy 与 privileged teacher 之间的最优几何插值，再把昂贵高方差的 RL 解转成 token-logit 蒸馏目标，并以 return-to-go 做长推理信用分配。

```mermaid
flowchart LR
    R["Reference logits"] --> I["β-controlled interpolant"]
    T["Privileged teacher"] --> I
    I --> D["On-policy distillation"]
    D --> G["Return-to-go credit"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![β-OPSD 原论文流程图](assets/paper-figure-01.png)](https://arxiv.org/html/2607.28582v1/x1.png)

图片来自[原论文](https://arxiv.org/abs/2607.28582)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
\tilde p_{\beta}=\operatorname{softmax}((1-w)z_{\bar\theta}+wz_T),\quad G_t=\sum_{s=t}^{T}\gamma^{s-t}(\log\pi_\theta-\log\tilde p_\beta)_s.
$$

### 论文离线与线上效果

Qwen3-8B 在 AIME24/AIME25/HMMT25 的 Avg@12 平均 60.18，比 vanilla OPSD +1.66；Qwen3-4B 平均 +1.76。论文没有生产线上 A/B。

## 本地复现

> **本地对照口径**：同一 GSM8K candidate-policy、120 steps、seed 42；相对未训练基线 accuracy 从 0.1719 到 **0.7656（+345.45%）**。

```bash
auto-research post-train --algorithm beta-opsd --dataset gsm8k-candidate --maximum-examples 256 --steps 120 --seed 42
```

固定指标见 [`beta-flux-opd-gsm8k-seed42.json`](../../experiments/beta-flux-opd-gsm8k-seed42.json)。

## 复现边界

候选动作对应 token 分布，线性 return-to-go 代理序列位置；未复刻 Qwen3、LoRA 和 A6000/H200 训练。
