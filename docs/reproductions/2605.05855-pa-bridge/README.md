# PA-Bridge：主动表达与被动行为的分布桥接

> **Fidelity: 核心机制复现**。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2605.05855](https://arxiv.org/abs/2605.05855) |
| 公司/机构 | ByteDance（按第一作者所属机构聚合） |
| 首次公开日期 | 2026-05-07（arXiv v1） |
| 原文开源代码 | 否：未找到原作者公开代码（核查日期：2026-09-02） |
| Adapter | `pa-bridge` |
| 本地复现代码 | [`src/auto_research/reproductions/pa_bridge/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/pa_bridge/) |

## 原始论文总结

### 背景与主要改动

用分布对齐器把被动浏览行为迁移到主动查询空间，再通过语义离散化和重加权削弱曝光反馈回路，改善 conversation starter 的覆盖与多样性。

```mermaid
flowchart LR
  A["公开行为与候选"] --> B["pa-bridge 核心机制"]
  B --> C["同预算方法输出"]
  A --> D["统一直接基线"]
  C --> E["全目录排序与结构诊断"]
  D --> E
```

<!-- paper-figure:start -->
### 原论文关键图

[![PA-Bridge：主动表达与被动行为的分布桥接 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/pdf/2605.05855#page=2)

> **原论文 Figure 2（关键图）**：展示原论文提出的核心架构、主要模块及其连接关系。图片来自[原论文](https://arxiv.org/abs/2605.05855)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
z=\\operatorname{Align}(h_{passive},h_{active}),\\qquad \\mathcal L=\\sum_i \\omega(c_i)\\ell(f(z_i),y_i).
$$

### 论文离线与线上效果

- 线上 A/B：功能渗透率 +0.54%、用户活跃天数 +0.04%；曝光与点击的唯一查询数分别 +30.65% 和 +56.50%。
- 上述数字只复述论文线上证据，不写入本地公开数据效果结论。

## 本地复现

> **本地对照口径**：同一 MovieLens 全目录协议下，基线 NDCG@10 为 `0.05401`，实验组为 `0.04938`，相对变化 **-8.57%**。本地代理目标与论文生产任务不同，不能外推线上 lift。

三随机种子完整结果、均值、标准差与 95% CI：

- [`metrics/public-seeds42-44.json`](metrics/public-seeds42-44.json)

```bash
auto-research reproduce --paper pa-bridge --dataset-dir data --seeds 42,43,44
```

## 复现边界

本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。
