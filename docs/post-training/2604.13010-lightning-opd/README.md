# Lightning OPD：离线教师缓存的 On-Policy Distillation

> 保真度：本地实现复现教师预填充、teacher consistency 和训练期零在线教师调用；
> 当前使用候选策略验证机制，不等同于论文的 Qwen3 全参数训练。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [Lightning OPD（arXiv 2604.13010）](https://arxiv.org/abs/2604.13010) |
| 公司 / 机构 | MIT HAN Lab / Jet AI |
| 首次公开日期 | 2026-04-14 |
| 原作者代码 | [jet-ai-projects/Lightning-OPD](https://github.com/jet-ai-projects/Lightning-OPD) |
| 本地 adapter / 算法键 | `lightning-opd` |
| 本地复现代码 | [`src/auto_research/post_training/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/post_training) |

## 原始论文总结

### 背景与主要改动

传统在线蒸馏在每一步训练都调用教师，吞吐和成本受教师推理限制。Lightning OPD 先让
学生在 SFT 数据上产生 on-policy rollout，再由同一个教师一次性计算 token 分布并缓存。
训练只读取缓存，因此保留学生分布上的蒸馏信号，又不需要训练期在线教师。

```mermaid
flowchart LR
    S["SFT prompts"] --> R["Student on-policy rollouts"]
    R --> T["同一 Teacher 一次性打分"]
    T --> C["Teacher log-prob cache"]
    C --> O["Offline distillation updates"]
    O --> M["Student model"]
```

### 核心公式

$$
\mathcal{L}_{\mathrm{OPD}}
=-\mathbb{E}_{x,y\sim\mathcal{D}_{\mathrm{SFT}}}
\sum_t p_T(y_t\mid x,y_{<t})\log p_\theta(y_t\mid x,y_{<t}).
$$

关键约束是 rollout 和离线标签来自一致教师配置，避免 teacher mismatch。

### 论文离线与线上效果

论文在 Qwen3-8B Base 上报告 AIME 2024 69.9%，总训练约 30 GPU hours，训练效率约
提升 4 倍；Qwen3-30B-A3B 在单个 8×H100 节点上报告 AIME 2024 71.0%。论文是离线
benchmark 研究，未报告生产线上 A/B。

## 本地复现

实现先为全部训练候选缓存教师概率，保存 `teacher_prefill_calls` 和
`teacher_cache_entries`；更新阶段强制 `online_teacher_calls=0`。策略更新、KL 和评测
与 DPO/GRPO 使用同一数据划分。

```bash
auto-research post-train --algorithm lightning-opd \
  --dataset gsm8k-candidate --maximum-examples 512 \
  --steps 300 --seed 42
```

| 指标 | 未训练策略 | Lightning OPD |
|---|---:|---:|
| GSM8K candidate accuracy | 0.1641 | **0.8359** |
| mean reward | 0.3126 | **0.8561** |
| KL(reference) | 0.0000 | 0.8269 |
| 在线教师调用 | — | 0 |

稳定指标见
[`post-training-gsm8k-candidate-seed42.json`](../../experiments/post-training-gsm8k-candidate-seed42.json)。

## 复现边界

当前没有训练真实 Qwen3、token-level vocabulary distribution 或复跑 AIME；因此只能
证明缓存式 OPD 数据流和教师调用约束成立，不能把本地 accuracy 与论文 AIME 数字比较。
