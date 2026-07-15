# 2026 年近期工业界 LLM × 搜广推硬筛

检索日期：2026-07-15。纳入条件同时满足：2026 年近期公开、互联网大厂作者或明确生产平台、LLM/生成式模型与搜索/广告/推荐直接结合、正文披露量化线上 A/B。只写“deployed”或只有离线结果的不纳入。

| 优先级 | 论文 / 公司 | 线上 A/B | 本地忠实复现判断 |
|---|---|---|---|
| 已实现 | [Prompt Generation](https://arxiv.org/abs/2607.11326) · Alibaba/Taobao | 搜索成交笔数 +0.47%、GMV +0.51%；推荐 IPV +0.66%、PVR +7.93%；店铺搜索成交 +4.01% | **高**：论文给出双 JSON 协议、公开 Amazon Office 基准和完整特征消融；本仓库已实现 `prompt-generation` |
| 下一批 A | [UniVA](https://arxiv.org/abs/2605.05803) · Tencent/WeChat | GMV +1.5% | **高**：Commercial SID、generation-as-ranking、eCPM RL、value-guided beam search 均可在公开交互/价值代理上执行 |
| 下一批 A | [Fine-Tuned LLM as a Complementary Predictor Improving Ads System](https://arxiv.org/abs/2605.27856) · Pinterest | Shopping RoAS +4.94%；opt-in Shopping RoAS +6.69% | **高**：可执行真实小型 LLM SFT/GRPO、advertiser prediction、召回注入和排序特征；需明确公开数据中的 advertiser 映射 |
| 下一批 A | [LWGR](https://arxiv.org/abs/2605.18771) · Alibaba International | 广告 revenue +1.35% | **高**：论文含公开数据，soft instruction、世界知识抽取和 Lagrangian primal-dual 融合适合本地缩放复现 |
| 下一批 B | [SIGMA](https://arxiv.org/abs/2602.22913) · AliExpress | Order +2.80%、CVR +3.84%、GMV +7.84%、购买类目广度 +2.47% | **中高**：多视角对齐、hybrid SID、multi-task SFT 可复现；完整节日/趋势任务需构造公开时间切片 |
| 下一批 B | [S-GRec](https://arxiv.org/abs/2602.10606) · Tencent/WeChat | GMV +1.19%、GMV-Normal +1.55%、CTR +1.16%、dislike -2.02% | **中高**：论文使用公开 Amazon Industrial/Office；需实际训练 semantic judge、生成 backbone 和 A2PO，运行成本较高 |
| 通过但暂缓 | [AIGQ](https://arxiv.org/abs/2603.19710) · Alibaba/Taobao | HintQ UCTR +7.42%、归因订单 +10.31%、GMV +10.68%、7 日留存 +3.73% | **中**：IL-SFT/IL-GRPO 可做，但公开数据缺少与 HintQ 等价的用户→自然语言 query 列表及线上 CTR reward |
| 通过但暂缓 | [RaG](https://arxiv.org/abs/2606.25496) · Kuaishou | 相对生产 GRM，广告收入最高 +1.87% | **低（Mac）**：核心包含个性化视频生成、多 Agent 和跨域视频质量 reward；用图片或打分代理会折损核心，不应现在宣称复现 |
| 通过但暂缓 | [RoleGen](https://arxiv.org/abs/2602.13134) · Kuaishou | dormant-user 订单量 +7.3% | **中低**：需要真实 conversion trajectory、counterfactual reasoner 与线上反馈反思闭环；公开数据缺少关键轨迹监督 |

未纳入：LocalSUG 虽披露 CTR +0.35% 和 few/no-result -2.56%，但论文作者单位没有满足“大厂论文”的明确证据；LinkedIn Semantic Search 论文披露大量离线消融，但没有找到可核验的量化线上 A/B，因此均不通过本轮硬门槛。

执行顺序按“保真度优先，而非线上 lift 大小”排序：PG → UniVA → Pinterest Ads Predictor → LWGR → SIGMA/S-GRec。RaG 的线上结果很强，但在本地缺少视频生成与质量反馈链路，当前做简化版反而会重复此前的折损问题。

