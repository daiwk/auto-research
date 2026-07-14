# 博客 LLM+推荐工业落地论文全量审计

来源：[个人博客的 ID/SID 工业落地章节](https://www.daiwk.net/1.7.llm_recommend#llm-tui-jian-shu-ru-idsid-gong-ye-jie--luo-di)与[文本工业落地章节](https://www.daiwk.net/1.7.llm_recommend#llm-tui-jian-shu-ru-wen-ben-gong-ye-jie--luo-di)。复核日期：2026-07-14。

本轮解析了两个章节的 **94 个主论文条目**，并回查章节内 **138 个 arXiv 链接**。自动初筛有 74 个主条目在 online/deployment 段附近出现百分比；百分比可能是流量、离线指标或成本，最终仍须人工阅读原文确认，不能直接等同于合格 A/B。

## 已实现且满足量化生产 A/B

| Route | Papers |
|---|---|
| ID/SID / generative | HSTU、OneRec、OneRec-V2、LONGER、RankMixer、PinFM、PinRec、GenRank |
| Text / LLM embedding | PLUM、M6-Rec、KAR、BAHE、BEQUE、LEARN、NoteLLM |

本轮新增的是 PinRec、GenRank、LEARN、NoteLLM；此前 PR #14 的 KAR/BAHE/BEQUE 只是首批，不再代表全量筛选。

## 已核验、后续实现队列

| Paper | Company | 代表性 | 原文量化线上证据 |
|---|---|---|---|
| SessionRec (2502.10157) | Meituan | next-session generative retrieval | 7 天；Pay PV +0.603%、PVCTCVR +0.564% |
| EGA-V1 (2505.19755) | Meituan | end-to-end ads allocation | CTR +5.2%、RPM +13.6%、ROI +3.1% |
| LSVCR (2403.13574) | Kuaishou | video/comment joint LLM rec | comment watch time +4.1264% |
| MSD (2412.06860) | Meituan | LLM-infused CTR + cache | CTR +2.12%、CPM +2.59% |
| LUM (2502.08309) | Alibaba | LLM user model / pre-trigger | CTR +2.9%、RPM +1.2% |
| SERAL (2502.13539) | Alibaba | serendipity alignment | S-PVR +5.7pt，另报告 CTR/业务指标 |
| SaviorRec (2508.01375) | Alibaba | multimodal cold-start alignment | clicks +13.31%、orders +13.44%、CTR +12.80% |
| PRECISE (2412.06308) | WeChat | pretrained content embedding | 最高 shares +2.560%，并报告 clicks/read time |
| LCU (2504.01602) | Kuaishou | LLM comment understanding | staytime +1.27%、exposure +0.81% |
| LEADRE (2411.13789) | Tencent | LLM-enhanced ad retrieval | Channels GMV +1.57%、Moments +1.17% |
| COBRA (2503.02453) | Baidu | sparse+dense generative retrieval | conversion +3.60%、ARPU +4.15% |
| ARGUS (2507.15994) | Yandex | long-context music Transformer | ARGUS TLT +2.26%、like likelihood +6.37% |

优先级按“新机制覆盖度、与已有 adapter 重合度、公开数据可复现性”确定，而不是只按线上涨幅排序。

## 暂不进入实现队列

- 章节中未在原文找到量化线上 A/B 的条目，例如 Meta sid+ID 表征、HeteroRec、MTGRBoost、OpenOneRec、NoteLLM-2 等；部署或离线提升不替代硬门槛。
- 与已有 adapter 核心链路高度重合的论文先保留，例如更多 OneRec/HSTU scaling 变体。
- 需要广告拍卖、地理位置或内容审核专有环境才能验证核心结论的论文，先记录而不做弱代理。

该清单会随博客更新继续追加；所有进入 adapter 的论文仍需独立 README、公式、架构、原文离线/线上表、本地多 seed 指标及边界说明。
