# RECAP：用推荐反馈闭环优化流式语义画像

> **Fidelity: 核心机制复现**。真实训练 causal Transformer updater、双塔评价器和 clipped GRPO，并执行固定容量画像状态机。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2607.15730](https://arxiv.org/abs/2607.15730) |
| 公司/机构 | Kuaishou Technology / USTC |
| 首次公开日期 | 2026-07-17（arXiv v1） |
| 原文开源代码 | 否：论文未提供官方/作者代码（核查日期：2026-07-22） |
| Adapter | `recap` |
| 本地复现代码 | [`src/auto_research/reproductions/recap/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/recap/) |

## 原始论文总结

### 背景与主要改动

传统 LLM 用户画像只追求“总结得像”，没有直接优化未来推荐。RECAP 把画像变成带容量约束的结构化流式状态：LLM 负责语义 update，确定性逻辑负责生命周期、合并与淘汰；再用 LLM judge 筛出标签一致的行为 pair，训练双塔 evaluator，把匹配分数作为 GRPO reward 闭环更新画像生成器。

```mermaid
flowchart LR
  B[streaming behaviors] --> U[LLM profile updater]
  U --> S[bounded structured state]
  S --> C[decay / merge / evict]
  B --> J[LLM label-consistency judge]
  J --> E[dual-tower evaluator]
  E --> R[semantic reward]
  R --> G[GRPO]
  G --> U
  C --> REC[recommendation]
```

### 核心公式

对同一上下文采样一组画像更新 $o_i$，RECAP 使用组内标准化 advantage：

$$
A_i=\frac{r_i-\operatorname{mean}(r)}{\operatorname{std}(r)+\epsilon},\qquad
r_i=s_{\mathrm{eval}}(p_i,b^+).
$$

策略更新采用 clipped ratio，并加入 reference KL、格式和多样性约束；状态机始终满足 $|P_t|\le C$。

### 论文离线与线上效果

相对 base generator，离线 uAUC 绝对 `+0.0084`、Recall@2000 约 `+4.9%`。7 天线上 A/B 中，人均应用使用时长显著提升 `+0.139%`。

## 本地复现

> **本地对照口径**：基线是 open-loop SFT 流式画像；实验组增加反馈 evaluator 与 GRPO，NDCG@10 相对 **`-6.77%`**。

MovieLens-100K 固定 220 users / 360 items；genre token 作为可解释语义，画像容量为 4。GRPO mean reward 从 `0.5245` 升到 `0.7096`，但 test NDCG `0.04838 → 0.04511`；同时 head share `0.2400 → 0.1914`。说明本地 evaluator reward 上升没有可靠迁移到 next-item 指标。稳定指标见 [`metrics/movielens-100k-seed42.json`](metrics/movielens-100k-seed42.json)。

```bash
auto-research reproduce --paper recap --seed 42
```

## 复现边界

自然语言画像和工业 LLM 缩为 category-token causal Transformer；没有快手私有日志、生产 LLM judge 和在线闭环。核心 SFT→evaluator→GRPO→bounded state 链路实际执行，但不声称复现线上收益。
