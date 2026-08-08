# 全主题系统缺口审计（2026-08-08）

这不是“再列几篇论文”，而是一次按固定二维口径完成的全域复查：横轴覆盖搜广推与
LLM 应用、基础模型、纯 LLM 后训练、Agent；纵轴覆盖每个领域的二级主题。所有候选均
记录在 [`paper-discovery-ledger.json`](paper-discovery-ledger.json)，状态只允许为已实现、
延后或拒绝，避免“搜到但下次忘记”。

## 审计方法与边界

1. 从仓库 adapter、详情页和方法索引反向建立“已覆盖集合”，不以页面里出现过名字为已实现。
2. 对经典主干、2025 年、2026 年至 8 月 8 日分别检索；再按机构、引用链和官方仓库反查。
3. 工业搜广推继续执行硬门槛：必须有量化线上 A/B、明确全流量上线证据，或用户具名批准的
   经典例外；离线指标和“已部署但无数字”不能自动进入实现队列。
4. 基础模型、后训练与 Agent 要求核心机制可真实训练或执行，并有公开 benchmark；纯分析论文
   可以进入研究索引，但不创建假 adapter。
5. “延后”表示已核验、尚未实现或等待证据/运行环境；“拒绝”表示不满足当前门槛，不是遗漏。

本轮也暴露了旧流程的问题：此前 `2026-08-08-p0-p1-closed-audit` 只证明当时选出的 15 篇已
闭环，并未声明二级主题覆盖，因此不能据此得出“全领域无遗漏”。现在全域批次会被测试强制
检查 24 个二级主题是否都有审计记录。

## 结论摘要与完成状态

> 2026-08-08：本页识别的 **38 个 P0 与 15 个 P1 已全部实现**。P0 包括 19 个 reproduction
> adapter、11 个后训练 objective 和 8 个 Agent 方法；固定 seed 指标见
> [`experiments/global-p0-20260808-seed42.json`](experiments/global-p0-20260808-seed42.json)。P1 包括
> 8 个 reproduction adapter、3 个后训练 objective 和 4 个 Agent 方法，指标见
> [`experiments/global-p1-20260808-seed42.json`](experiments/global-p1-20260808-seed42.json)。

| 领域 | 真正的主要缺口 | P0 建议 | P1 / P2 与边界 |
|---|---|---:|---|
| 搜广推与 LLM 应用 | 近期生成式推荐、重排、长历史、异构粗排及内容相关性 | 11 | 经典长序列与证据待核验论文；审核风控暂无满足硬门槛的新候选 |
| 基础模型 | 位置编码、GQA/混合结构、数据配比、tokenizer-free、多模态、推理解码 | 8 | 5 个本地/单卡 P1；FlashAttention 等进入 GPU kernel 专项 |
| LLM 后训练 | RLAIF、过程奖励、test-time RL、自博弈课程、off-policy 稳定性 | 11 | 3 个 P1；理论分析与现有 objective 同构者不重复建 adapter |
| Agent | 工具 RL、deep research、技能固化、自进化 RL、公共 benchmark | 8 | 4 个方法/评测 P1；真实浏览器与官方 SWE-bench 延续用户暂缓决定 |

这里的数量是“当前明确值得实现的优先队列”，不是 arXiv 搜索命中数。完整候选、拒绝理由与
优先级以机器账本为准。

## 搜广推与 LLM 应用

### 已实现的 P0

| 二级主题 | 论文 | 为什么属于缺口 | 原文线上证据 |
|---|---|---|---|
| 生成式推荐 | [GloRank](https://arxiv.org/abs/2604.25291) | 全局 Semantic ID action space，SFT + GRPO | 快手 7.8% 流量、14 天；Watch Time +0.095%，多项互动提升 |
| 重排/混排 | [Dual-Rerank](https://arxiv.org/abs/2604.07420) | 顺序知识蒸馏与 latency-aware dual reranker | 5% 流量一个月；Long-View +1.107%，P99/均值延迟显著下降 |
| 精排 | [OneRanker](https://arxiv.org/abs/2603.02999) | 统一 value-aware 生成与广告排序 | 微信广告全量部署，GMV +1.34% |
| 召回 | [RADAR](https://arxiv.org/abs/2506.07261) | 将完整排序模型异步用于下一请求召回 | Recall@200 约 2 倍，线上 engagement +0.8% |
| 召回 | [DualGR](https://arxiv.org/abs/2511.12518) | 长短兴趣路由、约束 SID 与 exposure-aware loss | 快手 views +0.527%，watch time +0.432% |
| 训练/Serving | [MPFormer](https://arxiv.org/abs/2508.20400) | 多任务 retriever 与资源共享 | watch time +0.426%；训练资源 -60%，serving -66.7% |
| 粗排 | [HAP](https://arxiv.org/abs/2603.03770) | 异构样本与动态计算预算 | 今日头条运行九个月；时长 +0.4%，活跃天数 +0.05% |
| 生成式推荐 | [OnePiece](https://arxiv.org/abs/2509.18091) | context engineering、blockwise latent reasoning、渐进 MTL | Shopee GMV/UU 超过 +2%，广告收入 +2.90% |
| 内容理解 | [IntSR](https://arxiv.org/abs/2509.21179) | 搜索推荐一体化的意图与 POI 理解 | 高德 GMV +9.34%，POI CTR +2.76% |
| 重排/混排 | [CDM](https://arxiv.org/abs/2406.09021) | 将多样性作为可控的工业混排目标 | 快手主端 watch time +0.406%，聚类系数 -0.957% |

此外，[CWM](https://arxiv.org/abs/2406.07932) 有 MWT +2.9%、VV +2.5%、CTR +0.3% 的
量化线上结果，机制上属于反事实长期价值排序，也应和上述 P0 同批公平复现。

### P1（已实现）、证据队列与拒绝项

- [SIM](https://arxiv.org/abs/2006.05639)、[TWIN-V2](https://arxiv.org/abs/2407.16357) 与
  [CRSD](https://arxiv.org/abs/2510.11056) 已实现；对应原文线上表格已固化，未使用摘要中的
  “significant improvement”替代数字。MUSE 仍需满足同一证据门槛。
- EGA-V2、RecoChain、SynerGen 等只看到离线评测或进行中证据，按硬门槛拒绝。
- **审核风控**：本轮没有找到同时满足“工业论文 + 量化线上 A/B/全流量证据”的公开候选。
  该子领域不是漏搜，而是“已审计、无合格候选”；若后续放宽为公开审核 benchmark，应独立改门槛。

## 基础模型

### P0：已在本地公平复现并接入 evolve

| 二级主题 | 论文 | 需要补的真实变量 |
|---|---|---|
| 长上下文 | [RoPE / RoFormer](https://arxiv.org/abs/2104.09864) | 相同参数量下的绝对位置、RoPE 长度外推对照 |
| 长上下文 | [ALiBi](https://arxiv.org/abs/2108.12409) | train-short/test-long 的 attention bias 对照 |
| 架构 | [GQA](https://arxiv.org/abs/2305.13245) | MHA/MQA/GQA 的质量、KV cache 与吞吐联合指标 |
| 架构 | [Hymba](https://arxiv.org/abs/2411.13676) | attention 与 SSM 并行 head，而不是配置名占位 |
| 架构 | [MoBA](https://arxiv.org/abs/2502.13189) | 可微 block routing 和真实稀疏计算 |
| 预训练数据 | [DoReMi](https://arxiv.org/abs/2305.10429) | proxy loss 驱动的 domain weight 更新 |
| 预训练数据 | [Data Mixing Laws](https://arxiv.org/abs/2403.16952) | 多 domain 小预算曲线预测配比，不用单次结果拟合 |
| 架构/Tokenizer | [Byte Latent Transformer](https://arxiv.org/abs/2412.09871) | entropy patching、byte encoder/decoder 与同 FLOPs 对照 |

### P1（已实现）/ P2

- 多模态经典锚点 [CLIP](https://arxiv.org/abs/2103.00020) 与
  [LLaVA](https://arxiv.org/abs/2304.08485) 已实现。
- 推理侧 [Speculative Decoding](https://arxiv.org/abs/2211.17192)、
  [AWQ](https://arxiv.org/abs/2306.00978) 和 [Medusa](https://arxiv.org/abs/2401.10774) 已实现。
- [FlashAttention](https://arxiv.org/abs/2205.14135) 与 vLLM/PagedAttention 属于 P2
  系统复刻，必须测真实 CUDA/Triton kernel、显存和吞吐，不能用普通 PyTorch attention 冒充。

## 纯 LLM 后训练

当前 DPO/GRPO/OPD 等 objective 数量很多，但“objective 名字多”掩盖了三条真正缺失的主干。

### P0（已实现）

| 主干 | 论文 | 缺失机制 |
|---|---|---|
| AI feedback | [RLAIF](https://arxiv.org/abs/2309.00267) | 生成原则/偏好标签、AI preference model 到 policy update 的完整闭环 |
| 过程奖励 | [Let's Verify Step by Step](https://arxiv.org/abs/2305.20050) | outcome reward 与 process reward 的 step-level 公平对照 |
| 过程奖励 | [Math-Shepherd](https://arxiv.org/abs/2312.08935) | 自动构造逐步监督与 step verifier |
| 自奖励 | [Self-Rewarding Language Models](https://arxiv.org/abs/2401.10020) | 同一模型 judge、生成 preference、迭代更新 |
| Reasoning RL | [LUFFY](https://arxiv.org/abs/2504.14945) | offline 数据下保持 on-policy 行为的修正 |
| Test-time RL | [TTRL](https://arxiv.org/abs/2504.16084) | 无标注测试样本上的奖励估计与在线适配 |
| 自博弈 | [Absolute Zero](https://arxiv.org/abs/2505.03335) | 自生成任务、验证器和 curriculum 联动 |
| 自置信奖励 | [INTUITOR](https://arxiv.org/abs/2505.19590) | 无外部 verifier 的 self-certainty reward |
| 稳定性 | [CISPO](https://arxiv.org/abs/2506.13585) | token importance sampling 与 clipping 的实际梯度路径 |
| 自博弈 | [SPIRAL](https://arxiv.org/abs/2506.24119) | language-game curriculum 与双角色更新 |
| 稳定性 | [ConSPO](https://arxiv.org/abs/2605.12969) | sequence consistency constraint |

PPO、GAE、DeepSeek-R1/GRPO 等原论文没有被再次列为“缺失 adapter”，因为核心机制已经由现有
实现覆盖；技术报告或纯理论分析若没有新的可执行 objective，只进入谱系注释。这能避免同一
算法换标题后被重复计数。

## Agent

### P0（已实现）

| 二级主题 | 论文 | 缺失机制 |
|---|---|---|
| 深度研究 | [DeepResearcher](https://arxiv.org/abs/2504.03160) | search/browse/answer 的长轨迹 RL 与引用奖励 |
| 工具 RL | [ReTool](https://arxiv.org/abs/2504.11536) | reasoning 中动态调用工具的 RL curriculum |
| 工具 RL | [ToolRL](https://arxiv.org/abs/2504.13958) | 多工具选择、参数生成和执行反馈训练 |
| 技能库 | [SAGE](https://arxiv.org/abs/2512.17102) | RL 驱动的技能生成、更新与复用 |
| 记忆/技能 | [MemSkill](https://arxiv.org/abs/2602.02474) | episodic memory 到可执行 skill 的固化 |
| 记忆/技能 | [Memento-Skills](https://arxiv.org/abs/2603.18743) | 经验抽取、技能检索和跨任务迁移 |
| Agentic RL | [SEARL](https://arxiv.org/abs/2604.07791) | 自进化轨迹池与 policy improvement 闭环 |
| 多 Agent | [Agent0](https://arxiv.org/abs/2511.16043) | 自生成任务与多 Agent curriculum |

P1 的 Agent-R1、CAMEL、ToolBench/ToolLLM 和 GAIA 已全部实现；
WebArena、官方 SWE-bench、OSWorld/真实浏览器需要容器、站点快照或外部 runtime。用户此前已经
决定后续再做，因此它们被明确标为 P2 延后，现有 deterministic mini-suite 不得改名冒充接入。

## 本轮实际执行结果

1. 工业 P0 已完成并逐篇记录量化线上证据、原作者代码状态、本地公平基线和负结果。
2. RoPE、ALiBi、GQA、Hymba、MoBA、BLT、DoReMi 与 Data Mixing Laws 已成为可执行 adapter；
   结构和数据配比算子已进入 evolve。
3. 11 个后训练方法进入统一 reward、KL、长度、seed 协议；TTRL/INTUITOR 在当前无分布漂移
   mini-suite 上未提升，作为保真边界而非“失败隐藏”。
4. 8 个 Agent 方法已运行 120 episodes 并记录方法特有 telemetry；真实浏览器和官方
   SWE-bench 仍保持延后，不伪装完成。
5. 后续每轮“有没有遗漏”继续追加 `scope_kind: global` 或明确局部范围的 ledger batch；
   全域审计缺任一二级主题时 CI 直接失败。
