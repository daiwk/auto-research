# SSRLive：动态语义 ID 的直播推荐

> **Fidelity: 核心机制复现**。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2606.06970](https://arxiv.org/abs/2606.06970) |
| 公司/机构 | Taobao & Tmall Group, Alibaba（按第一作者所属机构聚合） |
| 首次公开日期 | 2026-06-05（arXiv v1） |
| 原文开源代码 | 否：未找到原作者公开代码（核查日期：2026-09-02） |
| Adapter | `ssrlive` |
| 本地复现代码 | [`src/auto_research/reproductions/ssrlive/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/ssrlive/) |

## 原始论文总结

### 背景与主要改动

用静态语义 ID 表达主播长期内容，用动态语义 ID 捕获实时直播状态，再融合用户—主播交互特征完成观看、交易与互动多任务预测。

```mermaid
flowchart LR
  A["公开行为与候选"] --> B["ssrlive 核心机制"]
  B --> C["同预算方法输出"]
  A --> D["统一直接基线"]
  C --> E["全目录排序与结构诊断"]
  D --> E
```

<!-- paper-figure:start -->
### 原论文关键图

[![SSRLive：动态语义 ID 的直播推荐 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/pdf/2606.06970#page=4)

> **原论文 Figure 2（关键图）**：展示原论文提出的核心架构、主要模块及其连接关系。图片来自[原论文](https://arxiv.org/abs/2606.06970)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
h_i=\\operatorname{Fuse}(e^{static}_{sid},e^{dynamic}_{sid},e_{u\\leftrightarrow s}),\\qquad \\hat y_t=f_t(h_i).
$$

### 论文离线与线上效果

- 淘宝直播线上 A/B：观看时长 +3.38%、GMV +0.72%、关注 +3.12%、互动人数 +2.92%，且优化后延迟仅比 DLRM 高 1.33%。
- 上述数字只复述论文线上证据，不写入本地公开数据效果结论。

## 本地复现

> **本地对照口径**：同一 MovieLens 全目录协议下，基线 NDCG@10 为 `0.05401`，实验组为 `0.05351`，相对变化 **-0.92%**。本地代理目标与论文生产任务不同，不能外推线上 lift。

三随机种子完整结果、均值、标准差与 95% CI：

- [`metrics/public-seeds42-44.json`](metrics/public-seeds42-44.json)

```bash
auto-research reproduce --paper ssrlive --dataset-dir data --seeds 42,43,44
```

## 复现边界

本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。
