# 近期论文扫描记录（2026-09-27）

## 扫描范围与边界

- 延续上一批，按 2026-09-20 至 2026-09-27 的重叠窗口运行四领域分页发现与统一 manifest / ledger 差分。
- arXiv API 四领域分页均成功且未回退缓存；Google Research 与 Meta AI 官方发表页抓取超时，因此本轮不宣称跨来源穷尽，也不推进全来源发现 watermark。
- 发现脚本为覆盖晚索引记录会纳入整个月的 arXiv ID；`new` 是“尚未在本仓库终态登记”，不是“这一周发表”。机构关键词命中也不是作者单位证据。每条查询先按 100 条上限完成一次分页；200 条上限扩扫因 arXiv 限速耗时过长而中止，本次覆盖并非穷尽。
- 以下论文的线上数字均为**论文报告**，不是本仓库复现结果。只有代码、公开数据实验、验证/测试隔离及文档合同完成后才能改为 `implemented`。

| 领域 | 检索命中（去重后） | 仓库未终态登记 | 解释 |
| --- | ---: | ---: | --- |
| 搜广推 | 143 | 92 | 包含机构词误命中与晚索引旧文，非 92 篇本周新论文 |
| 基础模型 | 600 | 532 | 宽查询召回，待按真实领域与日期筛选 |
| 后训练 | 313 | 257 | 同上；Meta MaD-RL 由官网补查，不在本次 arXiv 候选内 |
| Agent | 548 | 491 | 同上；不能把未登记数当成可实现数 |

## 全文优先队列

| 优先级 | 论文 | 核查依据 | 当前状态 |
| --- | --- | --- | --- |
| P0 | [OneTrans-V2](https://arxiv.org/abs/2609.28589)（09-23，ByteDance） | 正文 §6.3：用户级 50/50 线上 A/B；共享 causal 用户上下文、三阶段联合训练、决策条件生成召回与精排→预排蒸馏 | 待实现；公开数据缺成交额/广告/真实三级漏斗，须严格区分替代口径 |
| P0 | [X-Rec](https://arxiv.org/abs/2609.29180)（09-24，TikTok） | 正文 §5：两次垂类上线；论文报告垂类互动 +4.1484%、全局互动 +0.0111%；anchor-conditioned 球面 flow matching、late-interaction DiT | 待实现；公开数据只能检验检索核心和吞吐，不可声称 TikTok 线上复现 |
| P0 | [CMRec](https://arxiv.org/abs/2609.28972)（09-24，Alibaba International Digital Commerce Group） | [正文 §4.2](https://arxiv.org/html/2609.28972v1)报告 2026-05-10～20、10% 流量线上 A/B：广告收入 +1.77%、订单 +2.64%；共享代码本、双约束 token 混合、上下文加权损失 | 待实现；工业广告数据私有，论文另用公开 Amazon M2 六语区数据；须核对原作者代码状态 |
| P0 | [AgentX-Model](https://arxiv.org/abs/2609.30001)（09-24） | 正文 §4.3：五次线上 A/B；双 Agent、Reproduce/Follow-up/Composition/Diagnose 及有依赖的历史回放 | 待实现；私有 473 节点图与线上门禁不可复刻，公开历史回放应标机制边界 |

## 其他领域的 P1 全文复核

| 论文 | 适合接入的部分 | 先决验证 |
| --- | --- | --- |
| [MaD-RL（Meta 官方发表页）](https://ai.meta.com/research/publications/mad-rl-matching-distributions-for-calibrating-llms-with-reinforcement-learning/)（09-24，Meta，优先） | 以 KL / Jensen–Shannon 等散度约束输出属性分布，比较 GRPO 的 mode collapse 与目标分布匹配 | 本轮官方源抓取超时后通过定向补查发现；先取得原文公式与实验协议、核对 arXiv 版本/作者代码，再决定可执行复现范围，不能仅实现熵正则 |
| [DeltaS](https://arxiv.org/abs/2609.27470) | 多模态视频的门控线性注意力状态漂移驱动 KV 淘汰 | 原作者代码已链接；需真实混合注意力 checkpoint、固定缓存预算和真实视频基准 |
| [KITE](https://arxiv.org/abs/2609.27294) | KV 不变的双塔扩展与 prefill/decode 成本对照 | 须核实可公开训练的小模型路径；仅参数/FLOPs 算术不算模型复现 |
| [PACT](https://arxiv.org/abs/2609.26355)、[DCRL](https://arxiv.org/abs/2609.27572) | 后训练 critic 对齐与策略—奖励耦合 | 读公式、代码/数据许可、同预算生成式基线；不能仅新增算法名 |
| [Trajectory-graph advantages](https://arxiv.org/abs/2609.28963) | Agentic RL 的 step-level credit | 需要不泄漏答案的多轮轨迹和可训练策略；固定 gold 轨迹只能作诊断 |
| [IterSynth](https://arxiv.org/abs/2609.29444) | 多轮 deep-search Agent 的角色解耦合成 | 需真实检索环境、独立 judge 和成本对照 |

这些是**复核队列**，不是已经通过可复现性验收的 P1 实现清单。先做完整正文、代码与数据核查，再登记每项终态。

## 明确排除与去重

- [A Flexible Recommendation System for Individuals and Groups](https://arxiv.org/abs/2609.27998) 被机构词查询误标为 Google / Meta 优先；arXiv 首页显示 IMT Atlantique / Lab-STICC，实验是合成组数据，无工业线上证据，不进入工业 P0。
- [When LLM-Based User Profiling Adds Value](https://arxiv.org/abs/2609.27183) 虽使用生产流媒体数据，摘要仅为离线四策略比较；在未找到量化线上 A/B 前不进入工业 P0。
- [From Interests to Semantic IDs](https://arxiv.org/abs/2609.29983) 使用 Amazon Reviews 离线实验，未见工业线上门槛，保留为非工业方法候选。
- 已在上一批处理的 Light Heads、Music Rationales、UNIQUE、MuSeR 和 Meta layered engagement 不因重叠窗口重做；其中 MuSeR、Meta 私有链路的未完成边界继续保留。

## 下轮执行约束

1. 先补 Google/Meta 官方页超时的来源复核、超过每查询 100 条的剩余分页，以及本批 P0 的原作者代码状态；定向补查已找出 Meta MaD-RL，证明 arXiv 分页不能代替机构来源。
2. P0 依次按公开机制可执行性落地，优先复用 OneTrans / 现有生成式召回 adapter；每篇保持独立论文信息块、原图、独立指标、三 seed 和公平基线。需要 CUDA 的路径按项目 GPU 门槛去 A100/A30 跑真实验证。
3. P1 在公式、公开数据和可执行预算确认后入队；不把注册表标签或 gold 轨迹当作正式实现。
