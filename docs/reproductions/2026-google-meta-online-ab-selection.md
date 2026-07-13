# 2026 Google / Meta recommendation paper selection

检索日期：2026-07-13；arXiv 首次提交时间窗：2026-01-01 至 2026-07-13。

## 硬性筛选条件

1. arXiv 首次提交日期位于时间窗内；
2. 至少一位作者单位为 Google 或 Meta；
3. 主题是推荐系统、广告推荐或推荐模型自动优化；
4. 正文明确披露真实流量的量化线上 A/B 结果。

只有离线 benchmark、系统吞吐或模拟用户实验的论文不入选。

## 已实现的代表作

| Paper | Company | Submitted | Area | Disclosed online A/B |
|---|---|---:|---|---|
| [LLaTTE](https://arxiv.org/abs/2601.20083) | Meta | 2026-01-27 | 长序列 scaling、两阶段 serving | conversion +4.3%，NE -0.25% |
| [Self-Evolving RecSys](https://arxiv.org/abs/2602.10226) | Google | 2026-02-10 | Gemini agent、结构/优化器/reward 自动发现 | 多项 YouTube/surface 指标 +0.03%–+0.14% |
| [Memento](https://arxiv.org/abs/2605.24051) | Meta | 2026-05-22 | 长期历史 RAG、MMR、数据 replay | CTR +1.0%，CVR +1.2% |
| [G2Rec](https://arxiv.org/abs/2606.20554) | Meta | 2026-06-18 | 生成式推荐、图兴趣 token | in-session >+0.03%；engagement +0.06%–+0.19% |
| [CMSL](https://arxiv.org/abs/2606.28533) | Meta | 2026-06-26 | 多兴趣序列、线性注意力 | 四项 retrieval 指标 +0.092%–+0.171% |
| [Cluster GOOBS](https://arxiv.org/abs/2607.00448) | Meta | 2026-07-01 | LLM 聚类、双塔难负采样 | CTR +53%；top-100 曝光贡献 50%→32% |

这六篇覆盖自动研究、模型结构、长历史、生成式推荐和召回采样，避免重复实现多个机制近似的候选。

## 合格但本轮未实现

| Paper | Company | Submitted | Reason retained / not implemented |
|---|---|---:|---|
| [Zero-shot Cross-domain KD for YouTube Music](https://arxiv.org/abs/2603.28994) | Google | 2026-03-30 | 两周 live experiments；与现有蒸馏/排序 adapter 重叠。其会议版本为 RecSys 2025，但 arXiv 首次提交在本时间窗内。 |
| [MM-LLM Multimedia Understanding](https://arxiv.org/abs/2605.09338) | Meta | 2026-05-10 | online engagement +0.02%；与已有 G2Rec/Cluster GOOBS 的语义特征方向重叠。 |
| [LLM Retrieval for Stable Ad Recommendations](https://arxiv.org/abs/2605.21969) | Meta | 2026-05-21 | top-line +0.45%、final-stage recall +1.2%、A/A' difference -8.62%；与 Cluster GOOBS 同属 LLM 语义召回。 |

## 明确排除示例

- Meta SilverTorch（arXiv 2511.14881）：首次提交于 2025-11，超出时间窗。
- Fine-Tuned LLM as a Complementary Predictor（arXiv 2605.27856）：有线上 RoAS 结果，但部署描述指向 Pinterest surfaces，不属于 Google 或 Meta。
- Rec-Distill（arXiv 2605.29755）：有线上 A/B，但属于 ByteDance/Douyin/TikTok。
