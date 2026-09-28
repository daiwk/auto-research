# 近期论文扫描记录（2026-09-28）

## 覆盖与口径

延续 09-27 批次，四领域均按 **2026-09-20～09-28** 请求、再向前重叠一天；
每查询取前 50 条并与统一 manifest/ledger 差分。相同请求先前出现 HTTP 406，
本次不改查询即可返回 200；客户端现对偶发 406 有界重试，四领域本次均未使用
缓存回退。这里的“未审”只表示仓库尚未登记终态，**不等于这几天新发表、符合
准入、或需要全部实现**。晚索引的 arXiv ID 仍独立进入召回，摘要现分开列示。

| 领域 | 去重召回 | 仓库未审 | 原始发表于 09-20～28 的未审 |
|---|---:|---:|---:|
| 搜广推与 LLM 应用 | 134 | 98 | 32 |
| 基础模型与多模态 | 334 | 321 | 217 |
| 后训练 | 232 | 187 | 90 |
| Agent | 311 | 300 | 201 |

上表是宽查询**候选数量，不是合格论文数量**。跨来源配置中的 Meta 官方总入口
返回 HTTP 500，Google/Meta GitHub 机构 API 返回 403 限流；Google 官方入口
成功但并不等于全部全文都完成。已通过定向官方页补查 Meta 论文。由于每查询只
审到前 50 条且三处来源失败，**全来源发现水位不推进**，下一轮仍需重叠窗口。

## 全文复核后最值得推进的条目

| 优先级 | 论文 | 核对后的证据与当前边界 |
|---|---|---|
| P0 · 工业 | [KuaFu](https://arxiv.org/html/2609.31045)（腾讯，09-25） | 正文 §4.8 是按访客随机分流的 A/B，资源一致；100% rollout 后保留 5% 对照，十个月 GMV +1.37%，95% CI [0.71%, 2.03%]。公开 MRQA/RecBench 可评测，但训练行为日志私有；应先做独立条目级压缩器、双轴 projector 和可执行的三阶段训练，再把 hallucination-aware DAPO 与公开任务接入，不能用单个压缩函数冒充四阶段复现。 |
| P0 · Meta 后训练 | [Recursive Self-Improvement via On-Policy Distillation](https://arxiv.org/html/2609.30652)（09-25 arXiv；一作 Meta AI/UCR） | 原文 Dynamic Co-Evolution 逐轮用更新后的学生刷新 privileged teacher，并以通过答案验证的更短自改写作 SRCL；作者在 Qwen3、AIME/HMMT 对比 OPSD。A100 已有原文 Qwen3-4B-Instruct-2507 公开 checkpoint，但本仓库尚未实现该训练/验证链，不能将既有 OPD 近似权重映射为本论文。 |
| P1 · Agent 系统 | [ActKV](https://arxiv.org/html/2609.31395)（09-25，USTC） | 根据 agent action 对 KV 作预算分配，需要真实推理器和等预算任务/吞吐；与现有 KV 方法应公平对照。 |
| P1 · Agent RL | [ToolSearcher](https://arxiv.org/html/2609.30906)（09-25，浙江大学/蚂蚁） | 原文面向大量工具的检索选择 RL，公开 AppWorld 数据与代码线索需核实后运行完整 retriever-policy 路径。 |
| P1 · Agent 技能 | [Code-Based Skills for Language Agents](https://arxiv.org/html/2609.31076)（09-25） | NetHack/MiniHack 的 primitive/skill 混合接口与 RL；公开环境可作为后续独立公平评测，不能用现有工具 tag mini-suite 代表其任务。 |

既有 [MaD-RL](experiments/mad-rl-mechanism.md) 是 **Meta 09-24 官方发布、论文
本体落款 09-23** 的优先待升级项：四种散度公式与字符策略诊断已经实现，但没有
原论文 Qwen3-4B + GSM8K/MATH/CodeContests 多语言训练。A100 上已核验存在
Qwen3-4B-Instruct-2507 checkpoint 和 CUDA，但缺公开数据协议落地、LoRA 依赖、
多语言预热与三 seed 成本对照；不能因为有 checkpoint 就声称 GPU 复现完成。

09-27 的 GRAFT/KITE/DeltaS 并非本次新发现；[GRAFT 公开工具环境三 seed
对照](experiments/sep28-three-mechanisms.md)已新增，但结果为零增益，正式 LLM
policy、同预算 scaling、真实视频模型三项验收仍未完成。CMRec 的 Amazon-M2
数据用户暂未提供，不以伪造跨语区切分代替。

## 下一步验收顺序

1. KuaFu：公开数据和可获取 checkpoint 下复刻条目压缩、双轴 projector、训练阶段及同预算无压缩/截断控制；GPU 路径须 A100/A30 receipt。
2. Meta OPD 和 MaD-RL：以原文 Qwen3-4B 与公开数学任务、同预算基线训练，验证目标分布/正确率或准确率/token 成本；只用 validation 选配置。
3. ActKV/ToolSearcher/Code Skills：先核实作者代码、公开环境与固定预算，按可执行性逐项实现。GRAFT、KITE、DeltaS 的欠账继续按[路线图](research-roadmap.md)验收。

本页不把上表 P0/P1 写成“已实现”；只有代码、公开任务、三 seed、文档和必要的
A100/A30 收据完成后才能升级状态。
