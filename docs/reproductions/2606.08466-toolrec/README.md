# ToolRec：面向工具查询推荐的校准偏好对齐

> **Fidelity: 核心机制复现**。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2606.08466](https://arxiv.org/abs/2606.08466) |
| 公司/机构 | Huazhong University of Science and Technology（按第一作者所属机构聚合） |
| 首次公开日期 | 2026-06-07（arXiv v1） |
| 原文开源代码 | 否：未找到原作者公开代码（核查日期：2026-09-02） |
| Adapter | `toolrec` |
| 本地复现代码 | [`src/auto_research/reproductions/toolrec/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/toolrec/) |

## 原始论文总结

### 背景与主要改动

在 KTO 式偏好目标上同时加入用户侧校准与工具频率驱动的动态系统侧校准，提升会触发工具的查询，同时约束上下文相关性下降。

```mermaid
flowchart LR
  A["公开行为与候选"] --> B["toolrec 核心机制"]
  B --> C["同预算方法输出"]
  A --> D["统一直接基线"]
  C --> E["全目录排序与结构诊断"]
  D --> E
```

<!-- paper-figure:start -->
### 原论文关键图

[![ToolRec：面向工具查询推荐的校准偏好对齐 原论文 Figure 3](assets/paper-figure-01.png)](https://arxiv.org/html/2606.08466v2/framework.png)

> **原论文 Figure 3（关键图）**：展示原论文的整体流程、关键阶段及其数据流向。图片来自[原论文](https://arxiv.org/abs/2606.08466)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
\\mathcal L=-w_u r_y\\log\\sigma(z)-w_s(f_{tool})(1-r_y)\\log\\sigma(-z).
$$

### 论文离线与线上效果

- OPPO 小布 2026-04-21 至 04-27、每组 5% 流量：点击数 +4.74%、CTR +3.32%，相关性相对变化 -1.44%。
- 上述数字只复述论文线上证据，不写入本地公开数据效果结论。

## 本地复现

> **本地对照口径**：同一 MovieLens 全目录协议下，基线 NDCG@10 为 `0.05401`，实验组为 `0.04819`，相对变化 **-10.78%**。本地代理目标与论文生产任务不同，不能外推线上 lift。

三随机种子完整结果、均值、标准差与 95% CI：

- [`metrics/public-seeds42-44.json`](metrics/public-seeds42-44.json)

```bash
auto-research reproduce --paper toolrec --dataset-dir data --seeds 42,43,44
```

## 复现边界

本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。
