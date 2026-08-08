# Visual Instruction Tuning

> **保真度：核心机制复现**。原文结论、本地公开数据实验和未复刻部分分开陈述。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [NeurIPS 2023 Oral](https://arxiv.org/abs/2304.08485) |
| 公司/机构 | University of Wisconsin-Madison / Microsoft Research / Columbia University |
| 首次公开日期 | 2023-04-17（arXiv v1） |
| 原文开源代码 | 是：[原作者仓库](https://github.com/haotian-liu/LLaVA) |
| Adapter | `llava` |
| 本地复现代码 | [`src/auto_research/reproductions/llava/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/llava/) |

## 原始论文总结

### 背景与主要改动

冻结视觉 encoder，用可训练 projector 把视觉特征映射到 LLM token 空间，再在 GPT-4 生成的多模态指令数据上做端到端 instruction tuning。

```mermaid
flowchart LR
 A["公开输入"] --> B["llava 核心机制"]
 B --> C["同预算训练 / 执行"]
 C --> D["公开评测与诊断"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![Visual Instruction Tuning 原论文 Figure 6](assets/paper-figure-01.png)](https://ar5iv.labs.arxiv.org/html/2304.08485/assets/x7.png)

> **原论文 Figure 6（关键图）**：展示原论文的训练流程与关键优化环节。图片来自[原论文](https://arxiv.org/abs/2304.08485)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
H_v=W_pE_v(I),\quad\mathcal L=-\sum_t\log p_\theta(y_t|H_v,x,y_{<t}).
$$

### 论文离线与线上效果

合成多模态指令集达到 GPT-4 的 85.1% 相对分；LLaVA+GPT-4 在 ScienceQA 为 92.53%。

## 本地复现

> **本地对照口径**：基线为 `majority response`，实验组为 `frozen encoder + trained projector + response decoder`，只改变论文核心机制；`instruction_accuracy` 0.2893 → **0.9750，相对基线 +237.04%**。

```bash
auto-research reproduce --paper llava --dataset-dir data --seed 42
```

固定指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)。

## 复现边界

公开 item 内容向量替代图像 encoder，训练真实跨模态 projector 和 instruction 分类头；未调用 GPT-4 或复刻 LLaVA-13B。 本地相对变化不得与原文指标混写。
