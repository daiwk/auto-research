# Not All Candidates are Created Equal: Heterogeneity-Aware Pre-ranking

> **保真度：核心机制复现**。原文结论、本地公开数据实验和未复刻部分分开陈述。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2603.03770](https://arxiv.org/abs/2603.03770) |
| 公司/机构 | ByteDance / Toutiao |
| 首次公开日期 | 2026-03-04（arXiv v1） |
| 原文开源代码 | 是：[官方/作者代码](https://github.com/Toutiao-Rec/HAP) |
| Adapter | `hap` |
| 本地复现代码 | [`src/auto_research/reproductions/hap/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/hap/) |

## 原始论文总结

### 背景与主要改动

按候选难度把样本路由到轻量或强预排分支，再以跨分支 harmonization 约束不同计算预算下的排序尺度。

```mermaid
flowchart LR
 A["公开输入 / 历史"] --> B["hap 核心路径"]
 B --> C["论文特有状态或目标"]
 C --> D["同预算评测"]
```

<!-- paper-figure:start -->
### 原论文关键图

[![Not All Candidates are Created Equal: Heterogeneity-Aware Pre-ranking 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/html/2603.03770v1/x2.png)

> **原论文 Figure 2（关键图）**：展示原论文提出的核心架构、主要模块及其连接关系。图片来自[原论文](https://arxiv.org/abs/2603.03770)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
s_i=g_i f_{strong}(x_i)+(1-g_i)f_{light}(x_i),\quad\mathcal L=\mathcal L_{rank}+\lambda\mathcal L_{harm}.
$$

### 论文离线与线上效果

今日头条部署九个月：使用时长 +0.4%，活跃天数 +0.05%。

## 本地复现

> **本地对照口径**：基线为共享 transition + content scorer，实验组只加入 `hap` 核心机制；相对 NDCG@10 +4.90%。

MovieLens-100K、260 users / 420 items、seed 42：NDCG@10 0.0354 → **0.0371（+4.90%）**。基线是共享 transition + content scorer；实验组只加入论文核心路径。

```bash
auto-research reproduce --paper hap --dataset-dir data --seed 42
auto-research evolve --model rankmixer --dataset movielens-100k --direction "组合 hap 与已安装论文算子" --generations 2 --population 4
```

固定指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)。

## 复现边界

在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。 本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。
