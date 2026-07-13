# 2026-07 Google / Meta recommendation paper selection

检索日期：2026-07-13；时间窗：2026-05-13 至 2026-07-13。

## 硬性筛选条件

1. arXiv 首次提交日期位于时间窗内；
2. 作者单位为 Google 或 Meta；
3. 主题是推荐系统，可包含 LLM；
4. 正文明确披露真实流量的量化线上 A/B 结果。

仅有离线 benchmark、系统吞吐、用户研究，或旧论文在近两个月发布公司博客，均不入选。

## 入选论文

| Paper | Company | Submitted | Area | Disclosed online A/B |
|---|---|---:|---|---|
| [G2Rec](https://arxiv.org/abs/2606.20554) | Meta | 2026-06-18 | 生成式推荐、图兴趣 token | in-session >+0.03%；engagement +0.06%–+0.19% |
| [CMSL](https://arxiv.org/abs/2606.28533) | Meta | 2026-06-26 | 多兴趣序列、线性注意力 | 四项 retrieval 指标 +0.092%–+0.171% |
| [Cluster GOOBS](https://arxiv.org/abs/2607.00448) | Meta | 2026-07-01 | LLM 聚类、双塔难负采样 | CTR +53%；top-100 曝光贡献 50%→32% |

这三篇分别覆盖生成式建模、长序列网络结构、召回训练采样，代表性比选择三个同类 ranking 模型更好。

## Google 检索结论

本时间窗内没有确认到同时满足上述四项条件的 Google 新论文。Google/YouTube 的一些相关论文要么早于 2026-05-13，要么没有在正文披露量化线上 A/B，因此没有为了凑公司数量而放宽标准。

## 明确排除示例

- Meta SilverTorch（arXiv 2511.14881）：论文首次提交于 2025-11，超出时间窗，且公开材料不满足本轮量化线上 A/B 条件。
- Rec-Distill（arXiv 2605.29755）：有大规模线上 A/B，但属于 ByteDance/Douyin/TikTok，不是 Google 或 Meta。
