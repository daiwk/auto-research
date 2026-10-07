# 统一后续路线图与 TODO

## 2026-10-07 论文实现与来源复核

[本轮扫描/实现记录](recent-paper-scan-20261007.md)保留四轨查询、完整去重标题池与前轮 48 个 Agent 标题初筛。宽查询命中不是新增合格论文；Google/Meta 来源仍有失败且查询触顶，水位不推进。

| 项目 | 当前状态 | 剩余验收 |
|---|---|---|
| FrugalEvo | 独立控制器已实现，A100 验证中 | 真实 7B/4B 生成、固定预算外部几何评测；完整论文与统一 Evolve 未完成 |
| Sentry | 独立控制器与 A100 三 seed 验证完成 | 本地 EM 29.17%，基线 41.67%，保留负结果；原文四环境与统一 Evolve 未完成 |
| Google TEE-FL · P0 | 09-25 旧文补发现；正文线上证据通过 | 核验开源 TEE 栈与公开训练可复现范围；不以普通 GPU 代替远程证明 |
| Airbnb SIFT · P0 | 10-06 新文；PDF A/B 表已核验 | 旅程、过滤器及有序容量标签的公开数据方案和真实训练 |
| RC-OPD / KV² · P1 | 方法已审，未实现 | 真实修复蒸馏训练 / 实际 KV 重建与压缩 |
| Dynamic Expert Pruning / Pivot-SD / Recursive Harness · P1 | 方法与可行性已审，未实现 | 真实 MoE、扩散模型及固定 verifier 环境；分别完成端到端验证 |
| 来源闭环 | 部分完成 | 五个机构页超时重试、触顶查询补扫、其余标题全文核验；不将 1,010 条宽查询匹配称作已审论文 |

此表覆盖下方 OCT06-FRU/SEN/DEP-MOE/SRC 的旧状态；不是宣称旧表全部清零。

## 2026-10-07 架构重构 MR-A / MR-B

| 批次 | 状态 | 范围与证据 |
|---|---|---|
| MR-A | 已合并 · [PR #192](https://github.com/daiwk/auto-research/pull/192) | [实验可信度与运行契约](design/experiment-integrity.md)：实验身份、恢复校验、GPU 执行闭环 |
| MR-B | 已合并 · [PR #193](https://github.com/daiwk/auto-research/pull/193) | [完整验收记录](design/architecture-mrb.md)：惰性注册/最小安装、逐命令 CLI、扫描页级断点、权威规格与稳定算法模块；1251 项全套测试、A100 回归及脱敏回执 |

MR-B 不新增论文，也不提升已有实现的证据等级。扫描状态修复不等于完成下方的官方来源重试
或全文筛选；跨源水位仍为 **2026-10-02**，后续按既有重叠窗口处理待审候选。

## 2026-10-06 重叠补扫批次

[本轮扫描记录](recent-paper-scan-20261006.md)补齐搜广推与 Agent 的 arXiv 分页，但 Google Research/Meta 官方目录仍超时，Agent 宽查询的窗口内 48 个标题也尚未逐篇全文核验。因此跨源水位仍为 **2026-10-02**，不能从 PR 日期直接开始下轮增量扫描。

| ID | 优先级 | 状态 | 交付/下一步验收 |
|---|---|---|---|
| OCT06-DEP | P1 | DONE · L1 机制 | [DepGPO](agent-research/2610.03634-depgpo/README.md)：读写/输出依赖、相关写入、支持性读取、token 权重守恒；完整 Agent 训练仍待 tracer、verifier 和真实策略更新 |
| OCT06-FRU | P1 | TODO · 正文与作者代码已核对 | FrugalEvo：强/弱模型实测程序搜索、共享前缀、固定成本公开任务的 BA-AUC；不能只复用面积公式 |
| OCT06-SEN | P1 | TODO · 候选 | Sentry：条件触发恢复与成功后记忆写入，隔离的 held-out 任务评测 |
| OCT06-DEP-MOE | P1 | TODO · 候选 | Dynamic Expert Pruning：真实 MoE 权重与预测器的质量/显存/延迟比较；CUDA 声明需 A100/A30 回执 |
| OCT06-SRC | P0 | TODO · 来源闭环 | Google/Meta 官方目录重试及 Agent 宽查询全文筛选；只有完成后推进扫描水位 |

后续对 RC-OPD、Recursive Harness Self-Improvement、Pivot-SD、KV² 的完整机制门槛仍见本轮扫描记录。此前 10 月 5 日条目是当时状态，不能覆盖这张更新后的待办表。

## 2026-10-05 定向复核与下一轮水位

[本轮记录](recent-paper-scan-20261005.md)从 10-01 重叠窗口定向核查，新增 [LESSER 输出层梯度数据选择](post-training/2610.03702-lesser/README.md)的 L1 CPU 机制与三 seed 恒等式证据。批量 arXiv API 请求长时间无响应，四领域及 Google/Meta 官方来源未完整收口，**发现水位仍为 2026-10-02**。下轮从 10-01 继续高召回与全文复核。RC-OPD、DepGPO、Recursive Harness Self-Improvement、AIMS 保持待审，不将名字或简单 proxy 登记为实现。

## 2026-10-04 七篇全文补漏批次

这是 10-02 已公告论文的补漏，不是 10-04 单日新增。七篇同一 PR 交付，全部保留 L1 机制/控制协议边界，**不意味着完整论文 benchmark、GPU 训练或 Evolve 能力集成已经完成**。

| 优先级 | 论文 | 本轮实现与验收 | 未覆盖的完整实验 |
|---|---|---|---|
| P0 | [Jev lookahead](agent-research/2610.01834-jev-lookahead/README.md) | 环境隔离前瞻、后继合法动作、既有 provider 契约；CPU 诊断 | 真实 Jev + ALFWorld/机器人 |
| P0 | [T2SPO](post-training/2610.00388-t2spo/README.md) | 历史成功轨迹、冻结真实 TabPFN CPU 三 seed、步骤信用/梯度 | 冻结文本编码器 + LLM 多轮任务 RL |
| P0 | [Weakest-Link](post-training/2610.00332-weakest-link/README.md) | 吸收式前缀约束、精确词表即时梯度、真实小策略优化 | 教师/学生 LLM 推理蒸馏与基准 |
| P1 | [CMP](agent-research/2610.02070-causal-memory-policy/README.md) | 均衡随机曝光、效应/SE、风险决策 | 真实 query 实验；跨 query 聚合本身不是论文已解决的问题 |
| P1 | [TESS](foundation-models/2610.02092-tess/README.md) | 两模型顺序训练、detached 价值标签、selector 优化 | LLM 数据选择后重新训练对照 |
| P1 | [RLCPR](post-training/2610.01458-rlcpr/README.md) | 严格 CDF 分桶、后验/长度 gate、奖励 | 真模型后验采集与完整 RL |
| P1 | [Mingbird](agent-research/2610.02001-mingbird/README.md) | schema 压缩、JSON rescue、循环纠偏、真实产物验收 | 真实本地模型 LRAB/τ²、Windows GUI/语音 |

可复跑入口、来源状态与统一边界见[批次报告](recent-paper-scan-20261004-followup.md)。新 CUDA 路径必须另行完成 A100/A30 门禁，不能使用这里的 CPU 回执替代。

## 2026-08-26 平台 P0

| ID | 状态 | 交付 |
| --- | --- | --- |
| INFRA-003 | DONE | 跨论文复现、Evolve、后训练、Agent 和多模态的 SQLite 实验索引、查询、Pareto 前沿与静态 HTML 看板 |
| INFRA-004 | DONE | 全量 adapter `paper.yaml`、确定性生成/校验和拒绝覆盖的脚手架 |
| EVOLVE-005 | DONE | 论文算子 registry、模型/槽位/依赖/冲突/资源预算校验，并接入候选规划过滤 |

完成这三个 P0 后，新增论文的标准路径是：补 adapter 与公开实验 → 同步声明 → 映射可执行 Evolve 算子 → 统一实验库登记指标。平台维护不再依赖手工复制目录数字或跨页面同步元数据。

## 2026-08-27 平台 P1

| ID | 状态 | 交付 |
| --- | --- | --- |
| INFRA-005 | DONE · [PR #128](https://github.com/daiwk/auto-research/pull/128) | Local / SSH / Slurm 统一执行契约，含日志、状态、重试、硬超时、显存声明和成本上限 |
| EVAL-001 | DONE · [PR #128](https://github.com/daiwk/auto-research/pull/128) | 推荐、基础模型、多模态、后训练与 Agent 的版本化公平评测协议；拒绝跨协议横向比较 |
| AUTO-001 | DONE · [PR #128](https://github.com/daiwk/auto-research/pull/128) | `paper.yaml` 到实验假设、算子、消融、搜索空间的可审计提案，保留来源并要求人工确认 |
| EVAL-002 | DONE · [PR #128](https://github.com/daiwk/auto-research/pull/128) | 配对 bootstrap、置换检验、Holm 校正、顺序 seed 与成本约束决策 |
| MEMORY-001 | DONE · [PR #128](https://github.com/daiwk/auto-research/pull/128) | 精确上下文负结果知识库，并接入 Evolve 的候选过滤和逐轮研究记忆 |

完整使用方式、边界和命令见[自动研究平台 P1](research-platform-p1.md)。

本页是仓库后续工作的**唯一权威待办清单**。各领域谱系页只解释覆盖范围和技术关系，
不再维护另一份易漂移的 TODO。以后每个实现 MR 都要更新本页的状态、验收证据和 PR；
新发现的工作先登记，再开始实现。

更新基线：**2026-09-30**。[最新官方来源重试与 P0/P1 合并批次](recent-paper-scan-20260930-followup.md)
新增 Snap GRP 工业 P0，以及 LIFT、Triadic Linear Attention、OASIS、GRAFT、RIDE、
PR-OPD、UserProxyBench、UpliftMem 八篇 P1。官方待审队列已按请求日期过滤历史噪声，
但仍有无日期/identity unresolved 标题，因此跨来源 watermark **不推进**。

[上一轮重叠扫描与收口](recent-paper-scan-20260930.md)
完成 09-27～09-30 四领域 arXiv 官方高召回扫描，并实现 HELIX、STEPQuant、LeapQuant、
Chinese-Jev、Dr. OPD、SIPO、ReMem 与 Video-RSI；高召回池与真正新增合格论文已分开统计。
机构官方入口本轮 TLS 超时，所以只确认 arXiv 传输完整，跨来源 watermark **不推进**。
上一轮的 [09-29 扫描与 RSI 专题核查](recent-paper-scan-20260929.md)
覆盖 09-20～09-29 四领域，并发现 Google/YouTube FLVM 工业 P0；arXiv 查询成功不等于
官方来源覆盖，Google/Meta 总入口提取零条 ID，发现 watermark **不推进**。历史上
[09-27 增量审计](recent-paper-scan-20260927.md)从 09-20
保留重叠窗口运行四领域分页；arXiv API 已恢复，但 Google/Meta 官方发表页抓取超时，
因此不宣称全来源穷尽，发现 watermark 暂不推进。[上一轮扫描记录](recent-paper-scan-20260926.md)按
2026-09-20～09-26 重叠窗口核验了四篇工业 P0 与一篇 Meta 评测 P1；完成和未完成的
边界保持在下表队列，不用占位 adapter 冒充复现。上一轮已合入
的 [PR #164](https://github.com/daiwk/auto-research/pull/164) 不因本轮扫描重做。

2026-09-28 [重叠窗口扩扫](recent-paper-scan-20260928.md)已在 arXiv API 恢复后
覆盖四领域、每查询前 50 条，并将原始本窗口发表与晚索引/历史未审分开；
Meta 官方总入口 500 和 GitHub 机构 API 403 仍使跨来源水位不可推进。
新增待验收优先队列：KuaFu（工业 P0）、Meta Recursive OPD（P0）、
ActKV/ToolSearcher/Code Skills（P1）。其中 ActKV 与 ToolSearcher 已有可测试的
**机制内核**，但缺真实推理器、原文环境和同预算基线；Code-Based Skills 仍待
NLE/MiniHack 环境对照。三者都**不是**完整论文 adapter，见
[合并批次边界](experiments/sep29-consolidated-mechanisms.md)。

System One 的 200 条固定公开切片和 2 轮 A100 真实 Evolve 已跑通；测试集与 OOD
仅在选择后读取，冠军没有优于初始配置。数据哈希、指标和运行边界见
[System One 评测协议](system-one/benchmark.md)。

### 2026-09-26 新论文执行队列

| ID | 优先级 | 状态 | 工作与完成条件 |
|---|---|---|---|
| SEP26-01 | P0 · Google | DONE（本分支） | Light Heads：共享塔动态轻头、重置和无 stop-gradient 消融；MovieLens 100K 显式评分双任务、三 seed、隔离 test，负结果原样保留 |
| SEP26-02 | P0 · Google | DONE（公开数据概念验证） | YouTube Music rationale：Qwen2.5-7B/A100 异步发现画像、Last.fm 艺人目录/新颖性/共享标签校验、在线提名增强与只附解释两臂、CF 回退；100 用户 test 0.38 对 CF 0.40，无公开理由曝光结果，不能验证论文线上收益 |
| SEP26-03 | P0 | DONE（缩比机制） | UNIQUE：KuaiRand-Pure 曝光时间留出，平面量化、早融合、target-attention split、生成/排序联合训练；三 seed CTR-AUC、code 召回和消融，负结果保留 |
| SEP26-04 | P0 | 部分完成（本分支） | MuSeR：已在 KuaiRand-Pure 训练多尺度压缩、多 query、候选路由与全库检索对照；原论文 ERNIE/BGE 语义、异步缓存和生产召回未完成，adapter 标为概念验证，不宣称论文复现完毕 |
| SEP26-05 | P1 · Meta | PROTOCOL（实证待数据） | layered engagement evaluation：已实现曝光前冻结校验、配对 bootstrap 与 CI-aware 决策协议；私有 scorer 和配对 A/B 不公开，不能声称复现 81.1% F1 |

### 2026-09-27 新论文执行队列

下表只登记已读到明确线上证据的工业 P0，其中 X-Rec 已有公开数据核心机制，但整项比较仍有缺口；正文证据、
各领域 P1 复核及排除项见[本轮扫描记录](recent-paper-scan-20260927.md)。

| ID | 优先级 | 状态 | 工作与完成条件 |
| --- | --- | --- | --- |
| SEP27-01 | P0 · ByteDance | 公开代理机制已实现 · [PR #169](https://github.com/daiwk/auto-research/pull/169) | [OneTrans-V2](reproductions/2609.28589-onetrans-v2/README.md)：共享 causal backbone、三级任务代理损失、DCGR 与精排→预排蒸馏，已记录三种子逐阶段指标；MovieLens 不具备真实交易/广告/漏斗标签，仍是概念验证 |
| SEP27-02 | P0 · TikTok | 公开核心机制与公平对照已实现 · [PR #169](https://github.com/daiwk/auto-research/pull/169) | [X-Rec](reproductions/2609.29180-xrec/README.md)：同 200 更新步的 SID-AR 对照、20×1 全目录召回与 CPU 生成吞吐已测；本地低预算结果为负，非生产 ANN 或线上复现 |
| SEP27-03 | P0 · Alibaba | 待实现 | CMRec：一作单位已核对为 Alibaba International Digital Commerce Group；尚须核查官方代码与可用跨域数据，完成共享语义代码本、双约束 code-mixing 和上下文加权损失的跨域消融 |
| SEP27-04 | P0 | 公开机制验证已实现 | [AgentX-Model](agent-research/2609.30001-agentx-model/README.md)：双角色提案/执行审查、四类动作、结果盲依赖回放与 MovieLens-1M 六节点三种子对照已运行；原文私有 473 节点图、LLM Agent 和线上收益不可复刻，故标为 concept demo |
| SEP27-05 | P1 · Meta | 小模型与 A100 三种子机制诊断已运行；正式复现未完成 | [MaD-RL](experiments/mad-rl-mechanism.md)：原文四种分布奖励有单测；Qwen3-4B 在五选项任务上完成 L2/forward KL/JSD 三种子同预算更新，验证和测试没有测出奖励差异。缺原文数学/代码自由生成任务、可核验的原图与原文规模基线，仍不登记正式复现 |

### 2026-09-28 缩比机制批次与待验证项

本轮 DeepXiv 检索服务不可达，arXiv API 四领域查询均返回 HTTP 406；
以下是基于 09-27 已登记队列、arXiv 正文和作者页的**定向推进**，
不是 09-28 全量新论文扫描。发现 watermark 不推进；恢复后须重新跑重叠窗口。

| ID | 优先级 | 状态 | 工作与完成条件 |
| --- | --- | --- | --- |
| SEP28-01 | P1 · Agent | L2.1 诊断已运行，正式复现待办 | [GRAFT](experiments/sep28-three-mechanisms.md)：经验轨迹图、Bellman 值、Graph GAE；无金标工具环境的三 seed tabular policy 对照未见提升，仍须 LLM policy 与论文任务环境 |
| SEP28-02 | P1 · 基础模型 | 小模型等算量及 CUDA 延迟诊断已运行，正式复现待办 | [KITE](experiments/sep28-three-mechanisms.md)：两阶段双塔、KV 不变量和 WikiText-2 三 seed 诊断；[近似等 FLOPs 对照及 A100 小模型 prefill/decode](experiments/sep29-kite-equal-flops.md)均已测，CUDA 未见明确加速；仍须原文规模、长上下文及吞吐 |
| SEP28-03 | P1 · 多模态 | L1 机制已实现，正式复现待办 | [DeltaS](experiments/sep28-three-mechanisms.md)：状态漂移与分桶 KV 淘汰；仍须真实混合模型状态、公开视频、等预算 GPU 验证 |
| SEP28-04 | P1 · 后训练/Agent | 待全文与数据协议复核 | DCRL、IterSynth：尚未找到能忠实跑通原定义算法且公平评测的公开低预算链路，不用名称注册或金标轨迹冒充实现 |
| SEP28-05 | P0 · Alibaba | 数据阻塞 | CMRec：Amazon-M2 暂不可用；不伪造跨语区数据或指标，保留 SEP27-03 |

### 2026-09-29 Agent 与后训练合并批次

此批的[证据边界和剩余验收项](experiments/sep29-consolidated-mechanisms.md)集中维护；下表的“机制/诊断”**不等于完整论文 adapter**。

| ID | 优先级 | 当前状态 | 下一道正式验收门槛 |
|---|---|---|---|
| SEP29-01 | P1 · Agent 推理效率 | ActKV 动作 attention LRFU 与动态预算机制单测完成 | 原文混合模型真实 KV、paged cache 压实、同预算基线与 A100/A30 端到端延迟/显存 |
| SEP29-02 | P1 · Agent 检索 | ToolSearcher 首次发现信用、门控和 masked policy loss 单测完成 | 固定版 StableToolBench/工具索引，真实 Qwen 组内 rollout 和 AppWorld 隔离评测 |
| SEP29-03 | P1 · Code-Based Skills | 原作者 CodeHack+定制 NLE 的真实 MiniHack 三模式、三种子环境烟测完成 | 同模型策略、同决策和环境步数预算的 primitive/skill/mixed 公平对照；当前随机控制器不用于论文性能比较 |
| SEP29-04 | P0 · Meta 后训练 | Recursive OPSD 官方 GSM8K 三臂三种子 A100 小预算对照完成，负结果 | 原文 OpenThoughts 精确切分、数学基准、原版 OPSD 和更接近论文规模的预算 |
| SEP29-05 | P1 · Meta 后训练 | MaD-RL Qwen3-4B 三奖励三种子 A100 五选项诊断完成，无差异 | 原文数学/代码自由生成任务与公平基线；合成选择题不能晋升正式复现 |
| SEP29-06 | P1 · 基础模型 | KITE 小模型近似等 FLOPs/本机延迟及 A100 CUDA prefill/decode 微基准完成，GPU 未见明确加速 | 原文规模梯队、长上下文与吞吐；小模型随机权重的微基准不代表论文速度结论 |
| SEP29-07 | P1 · Agent/多模态 | GRAFT、DeltaS 仍为机制诊断 | 前者需 LLM policy 与论文任务；后者需真实混合模型状态和公开视频 GPU 对照 |
| SEP29-08 | P0 · 工业推荐 | MuSeR 仍为公开 KuaiRand tag 代理 | 可审计的商品文本/多模态语义与缓存刷新链路；当前公开数据不含相应内容 |
| SEP29-09 | P0 · Google/YouTube 工业推荐 | [FLVM](reproductions/2609.32839-flvm/README.md) 公开 KuaiRand 三种子概念验证；Like AP 小幅变化，但长观看下降、稀疏负反馈波动，语义未稳定分离 | 无 YouTube 满意度调查、生产预排和线上流量；不能声称论文线上收益复现或推广为 Evolve 增益算子 |
| SEP29-10 | 跨领域 RSI | [递归自我改进专题](evolution/recursive-self-improvement.md) 已建，区分已执行机制与待审候选 | RRSI/RSIBench-Data 仍须真实任务与多轮继承、公平成本及 OOD 验收；专题不是新论文代码域 |
| SEP29-11 | 发现闭环 | 官方入口零 ID 与 PDF 误读已显性化 | 详情页遍历/feed 接入、机构全文核查、历史未审候选逐项终态后才能推进水位 |
| SEP29-12 | P0 · KuaFu 公平对照 | [MRQA 三种子 A100 独立训练对照](reproductions/2609.31045-kuafu/README.md)完成；压缩组均未超过同 token 预算对照 | 等 FLOPs 训练、有效幻觉 RL 更新、原文任务数据与更大规模评测；目前仅为公开小样本诊断 |

### 2026-09-30 P0/P1 合并批次

| ID | 优先级 | 状态 | 交付与边界 |
|---|---|---|---|
| SEP30-01 | P0 · 工业推荐 | DONE（本分支） | HELIX 三流 token、单向 user cache 与 MPTF；只引用 TikTok 全流量 A/B，公开张量诊断不冒充线上复现 |
| SEP30-02 | P1 · 基础模型 | DONE（本分支） | STEPQuant 与 LeapQuant 定义性状态量化机制、三种子诊断和 A100 CUDA 回执；不声称复现专用 kernel 吞吐 |
| SEP30-03 | P1 · System One | DONE（本分支） | Chinese-Jev 候选决策头与 CE/RLCD 目标，挂入 System One 索引；未训练 1000 万样本模型 |
| SEP30-04 | P1 · 后训练 | DONE（本分支） | Dr. OPD 与 SIPO token 信用机制、三种子诊断和 A100 CUDA 回执；未执行论文规模 rollout 训练 |
| SEP30-05 | P1 · Agent / RSI | DONE（本分支） | ReMem 时间演化记忆、Multi-Memory GRPO 与 Video-RSI Pareto 接纳；无真实浏览器/视频 Agent 环境，不登记为可执行 Evolve operator |
| SEP30-06 | 发现闭环 | PARTIAL | arXiv 四轨传输完整；机构官方入口 TLS 超时，RECAP 无线上 A/B，SelfSearch/VACE 依赖真实环境，watermark 不推进 |
| SEP30-07 | P0 · 工业推荐 | DONE（本分支） | Snap GRP：block-wise SID、detached MHP、mGRPO；正文线上 A/B 只作工业证据，本地不冒充线上复现 |
| SEP30-08 | P1 · 基础模型 | DONE（本分支） | LIFT top-k state feedback 与 Triadic 三阶线性注意力；均为 L1 mechanism，不声称大模型训练或 GPU kernel 性能 |
| SEP30-09 | P1 · 后训练 | DONE（本分支） | OASIS、GRAFT、RIDE、PR-OPD 的定义性选择/目标/表征机制，三种子诊断；无论文规模 rollout 训练 |
| SEP30-10 | P1 · Agent | DONE（本分支） | UserProxyBench UFS/泄漏审计与 UpliftMem paired uplift/EVSI；不使用 gold answer/plan |
| SEP30-11 | 发现闭环 | PARTIAL（本分支） | 官方入口恢复；修复历史 dated 标题和分页数字污染本轮队列。无日期或 identity unresolved 项仍保留，watermark 不推进 |

## 优先级和状态

| 标记 | 含义 |
| --- | --- |
| P0 | 新发现且通过硬门槛的最高优先论文，优先于本页 P1；工业方向中 Google / Meta 最高优先 |
| P1 | 已有可靠实现路径和公开数据，可分批交付的能力建设 |
| EVIDENCE | 方向重要，但尚缺公开证据、数据或公平评测，不能用占位 adapter 冒充实现 |
| DEFERRED | 用户明确延后，或依赖复杂外部环境；恢复前不进入执行队列 |
| DONE | 已完成并有代码、文档、指标和测试证据 |

Google（含 DeepMind、YouTube）和 Meta（含 Instagram）是唯一自动置顶机构。Netflix、
ByteDance、Alibaba、Kuaishou、Pinterest 等仍进入高召回扫描和正常评审队列，但不自动
置顶。机构查询命中只触发全文复核，不能替代论文首页 affiliation 和正文证据。

## 动态 P0：论文发现闭环

| ID | 状态 | 工作 | 完成条件 |
| --- | --- | --- | --- |
| DISC-001 | DONE | 每日四领域多查询、分页、canonical arXiv ID 去重 | GitHub Actions 生成四个候选 artifact |
| DISC-002 | DONE | 候选与 manifest、历史 ledger 自动差分 | JSON 和 Actions 摘要区分新候选、已实现、已审计 |
| DISC-003 | DONE | Google / Meta 新候选自动置顶预警 | 仅两家触发 warning；Netflix 等保持普通候选 |
| DISC-004 | DONE | 跨来源召回 | 动态研究页详情 arXiv 对账；静态会议 906 标题显式快照增量；传输、分页、身份状态分离；本窗口官方待核队列为零 |
| DISC-005 | DONE · [PR #113](https://github.com/daiwk/auto-research/pull/113) | 批次终态自动回写 | 回写器要求全部新候选终态；strict audit 可核对待审 artifact 与 ledger |

每个新工业候选先按“机构/主题”召回，再读 PDF/HTML 全文。只有量化线上 A/B，或用户
明确认可的统计显著全流量部署，才进入实现队列；摘要未写 A/B 不能作为拒绝依据。

## 2026-10-02 P0/P1 合并批次

| 优先级 | 领域 | 已完成论文 / 方法 | 验收状态 |
|---|---|---|---|
| P0 | 工业 LLM / 搜广推 | Gemini for Google、GEAR | 全文线上证据、独立详情页、可执行 L1 机制 |
| P0 | 后训练 | DARS、Range-GRPO | 依赖奖励与区间 GRPO 不变量测试通过 |
| P0 | Agent / RSI | ActiveSaddler、Safety Must Survive Self-Improvement、VeriHarness | 课程、验证、回滚协议测试通过 |
| P1 | 基础模型 / 多模态 | TACO、VETO | CUDA 机制实现；真实 A100 receipt 为合并门槛 |
| P1 | Agent / 后训练 | Mem++、DeFA、My FAULT、FloWright、Where-OPD | 状态、梯度、credit 与信息隔离合同通过 |
| P1 | 搜广推 | Effective Training Time、GrIS、REPAIR | 例外范围已写入元数据，不混入工业 A/B 结论 |

完整扫描、原文证据和边界见 [2026-10-02 扫描收口](recent-paper-scan-20261002.md)。

## 2026-10-03 P0/P1 合并批次

| 优先级 | 领域 | 已完成论文 / 方法 | 验收状态 |
|---|---|---|---|
| P0 | 搜索 / Jev | RPTune、LLM2Jev | Google 全文优先复核；定义性编排、决策分布与 KL 锚定可执行 |
| P0 | 后训练 | Sharpening Tax | 固定预算覆盖率损失诊断与三种子 L1 receipt |
| P0 | Agent | AutoCompact | 压缩决策、摘要、下一动作三字段纠错合同 |
| P1 | 搜广推 / 基础模型 | AgentWebRec、Omni-Embed-Mini、MWOP、AF-Muon、REA、HAWK、IrekoGPT | 独立详情、原文关键图、机制代码和边界齐全 |
| P1 | 后训练 | CARM、GMC-GRPO、GAW-PO、SHARPO、TVRL、LEGO-OPD、DriftOPD | 目标函数、掩码、credit 与 teacher composition 不变量通过 |
| P1 | Agent / RSI / Jev | Explicit Belief State、PACE、RuleEvolve、JevSpawn、MemFit | 状态、权限、验证选择、分支后验与追加式记忆合同通过 |
| 发现闭环 | 四领域 | PARTIAL | arXiv 成功；官方交叉源有 5 项失败，不推进 2026-10-02 watermark |

完整扫描、拒绝边界和下一轮重叠起点见 [2026-10-03 扫描收口](recent-paper-scan-20261003.md)。

## 2026-10-04 Meta 官方来源回溯补漏

| 优先级 | 领域 | 已完成论文 / 方法 | 验收状态 |
|---|---|---|---|
| P0 · Meta | Agent 检索 | SIRA | DF gate 与单次加权 BM25 组合可执行；不复刻论文 LLM 和大索引 |
| P0 · Meta | AI 研究 Agent | AIRA2 | 异步 steady-state 调度与 HCE 信号隔离可执行；不声明 8×H200 吞吐复现 |
| P0 · Meta | 个性化 Agent | PAHF | 行动前澄清、显式记忆和行动后漂移纠正均有不变量测试 |
| P0 · Meta | RSI / 开放式进化 | HyperAgents | 父代选择与有界 archive step 可执行；禁止生成代码执行 |
| 发现闭环 | 官方来源对账 | PARTIAL | 本轮是历史补漏；arXiv 批量请求 429，watermark 保持 2026-10-02 |

完整来源、日期、代码状态和复现边界见 [2026-10-04 Meta 官方补漏](recent-paper-scan-20261004.md)。

## P1 执行队列

建议按表内顺序推进；同一编号应尽量作为一个可独立合并的 MR。

### 基础模型与多模态

| ID | 状态 | 工作 | 最小验收条件 |
| --- | --- | --- | --- |
| FM-001 | DONE · [PR #113](https://github.com/daiwk/auto-research/pull/113) | test-time compute、verifier、动态 reasoning budget | 固定 SmolLM2 revision；GSM8K/算术多预算曲线同时报告正确率、token、延迟和调用成本 |
| FM-002 | DONE · [PR #114](https://github.com/daiwk/auto-research/pull/114) | scaling-law 多预算基础设施 | 默认 4 个模型规模/数据/step 预算点；记录实际参数量、tokens seen、FLOPs proxy、逐点残差、RMSE/R² 和不可外推边界 |
| MM-001 | DONE · [PR #115](https://github.com/daiwk/auto-research/pull/115) | 视频多模态 | 固定 SmolVLM2 commit；Video-MME-v2 Parquet/JSONL + MP4；逐题续跑、三 seed、置信区间和子集边界 |
| MM-002 | DONE · [PR #115](https://github.com/daiwk/auto-research/pull/115) | 音频多模态 | 固定 CLAP commit；ESC-50/ESC-10 真实 WAV；zero-shot top-1/top-5 和 text embedding cache fingerprint |
| MM-003 | DONE · [PR #116](https://github.com/daiwk/auto-research/pull/116) | 具身与大规模多模态后训练 | SmolVLA/LeRobot 真实训练入口、数据 manifest 与明确的 simulator/硬件成功率边界 |
| FM-003 | DONE · [PR #137](https://github.com/daiwk/auto-research/pull/137) | TwinKV 固定预算 KV eviction repair | 精确公式、Qwen3/Qwen2.5 真实 KV runner、公开 WikiText-2 长上下文、等预算质量/延迟/显存与 A30 receipt |
| MM-004 | DONE · [PR #137](https://github.com/daiwk/auto-research/pull/137) | PACE 视觉 token 压缩与抽取 | APC/DDAE、Qwen2.5-VL + RealWorldQA 默认路径、SmolVLM2 + POPE 真实验证、质量/token/延迟/显存与 A30 receipt |
| FM-004 | DONE | SAS 端到端稀疏注意力排序 | WikiText-2 真实 selector 训练、连续 log-gate 梯度、Top-K 路由与三 seed 隔离 test；Triton 性能明确不在本批声明 |

### LLM 后训练

| ID | 状态 | 工作 | 最小验收条件 |
| --- | --- | --- | --- |
| PT-001 | DONE · [PR #113](https://github.com/daiwk/auto-research/pull/113) | L2 切换到可下载 pretrained causal LM | SmolLM2 固定 revision，GSM8K unrestricted generation 与 3 seeds |
| PT-002 | DONE · [PR #115](https://github.com/daiwk/auto-research/pull/115) | CoBA-RL 完整教师路径 | 固定 Qwen2.5 teacher commit；pass@k/教师双缓存、真实调用率、token 成本与训练前后能力边界曲线 |
| PT-003 | DONE · [PR #113](https://github.com/daiwk/auto-research/pull/113) | 公开偏好数据 | 固定 UltraFeedback revision/MIT 元数据，DPO/ORPO 同预算真实模型对照 |
| PT-004 | DONE · [PR #113](https://github.com/daiwk/auto-research/pull/113) | GPU 训练完整性 | batch、gradient accumulation、mixed precision、safe checkpoint 与 optimizer resume；CPU/Mac 保留路径 |

### Agent

| ID | 状态 | 工作 | 最小验收条件 |
| --- | --- | --- | --- |
| AG-001 | DONE · [PR #116](https://github.com/daiwk/auto-research/pull/116) | Agent Lightning 连接可训练 LLM policy | SmolLM2 pairwise policy update、显式 transition credit、真实测试 executor 与 token/tool 成本 |
| AG-002 | DONE · [PR #116](https://github.com/daiwk/auto-research/pull/116) | Agent 真实 executor 的公平矩阵 | 相同仓库 fixture、相同 subprocess 上限、三 seed 比较 controller policy |
| AG-003 | DONE · [PR #131](https://github.com/daiwk/auto-research/pull/131) | Agent L2.1 隔离能力评测与九轴自动进化 | 删除 guide/oracle；train/validation/test 隔离；六方法、五消融、三 seed CI；validation 选冠军且 test 只在代际结束后运行 |

### Auto Research / Evolve

| ID | 状态 | 工作 | 最小验收条件 |
| --- | --- | --- | --- |
| EV-001 | DONE · [PR #113](https://github.com/daiwk/auto-research/pull/113) | 将 FM-001 的推理预算算子接入统一 genome | `reasoning-checkpoint` 搜索采样预算、self-consistency verifier、停止阈值并生成逐代报告 |
| EV-002 | DONE · [PR #116](https://github.com/daiwk/auto-research/pull/116) | 将 PT-001～PT-004 接入后训练 genome | data/objective/teacher/rollout/accumulation/precision 成为可继承组合轴并进入逐代报告 |
| EV-003 | DONE · [PR #117](https://github.com/daiwk/auto-research/pull/117) | 将 AG-001/AG-002 接入 Agent genome | memory/planner/tool/critic/policy/recovery 可组合，跨 episode 复用与失败恢复可测 |
| EV-004 | DONE · [PR #117](https://github.com/daiwk/auto-research/pull/117) | GenRec 类生成式推荐 evolve | MovieLens-1M 真实全目录 head、context/reward/distillation 旋钮和统一 ID-catalog 基线；Netflix 不因此获得论文优先级 |
| INFRA-001 | DONE · [PR #111](https://github.com/daiwk/auto-research/pull/111) | GPU 依赖防护 | pip dry-run 阻止静默替换现有 PyTorch；Linux CPU 合同测试覆盖，既有 A30 关键路径回归继续保留 |
| INFRA-002 | DONE · [PR #117](https://github.com/daiwk/auto-research/pull/117) | 重点方法多 seed 晋级 | 推荐/基础模型 adapter、后训练和 Agent 统一 3 seeds、置信区间、逐 seed 失败记录与断点续跑 |
| EV-005 | DONE · [PR #137](https://github.com/daiwk/auto-research/pull/137) | PACE 与 TwinKV checkpoint/结构算子 | 论文 ID → operator 可追踪；PACE 接入 VLM checkpoint 配方，TwinKV 接入可执行 micro-LLM attention，并与真实 checkpoint 复用 repair 函数 |
| EV-006 | DONE | EvoSkillRec typed skill genome | 控制器执行类型检查、候选运行、validation 评估、晋级和复用；RankMixer Evolve 可训练/评估 `rankmixer_evoskill`，不是 registry-only 标签 |

## 等待公开证据，不创建占位实现

| ID | 状态 | 缺口 | 恢复条件 |
| --- | --- | --- | --- |
| EVD-001 | EVIDENCE | 审核、作弊、欺诈、广告合规与风控 | 公开标注数据以及 precision/recall、误杀率和 guardrail 协议 |
| EVD-002 | EVIDENCE | 私有大规模广告竞价/转化日志 | 可公开替代数据和不会泄漏业务信息的公平离线协议 |
| EVD-003 | EVIDENCE | 公开端到端 LLM 推荐产品复现 | 用户、catalog、生成、排序、反馈闭环均有合法公开数据 |
| EVD-004 | EVIDENCE | AIGQ、RaG、RoleGen、LCU | 公开 reward、视频/用户反馈或转化轨迹及清晰数据许可 |
| EVD-005 | EVIDENCE | RecoChain、DIG 等工业候选 | 核实量化线上 A/B 或用户认可的全流量部署正文证据 |

## 用户已延后

| ID | 状态 | 工作 | 恢复条件 |
| --- | --- | --- | --- |
| DEF-001 | DEFERRED | 官方 SWE-bench Lite | 准备官方容器、镜像缓存、执行预算和长时 CI/开发机窗口 |
| DEF-002 | DEFERRED | ToolHop 正式全集 | 确认数据/评测依赖、模型调用预算和可复现 runner |
| DEF-003 | DEFERRED | 真实浏览器 Agent 环境 | 提供隔离 sandbox、凭据策略、网络策略和失败重放能力 |
| DEF-004 | DEFERRED | OneLA fused GPU 大 beam decode | 在 A100/A30 执行定义性 kernel，并提交显存、延迟和正确性 receipt |
| DEF-005 | DEFERRED | CanvasAnneal diffusion LM curriculum RL | 固定公开 DLM/teacher、训练预算和 MATH/tool-use 公平协议 |
| DEF-006 | DEFERRED | GAUGE grounded Agent 评测 | 公开 transcript/盲评标注可用，并接入 ranking/construct validity 协议 |
| DEF-007 | DEFERRED | AMDKernelVault ROCm/HIP | 提供 AMD CDNA/ROCm 执行环境并运行 kernel correctness/latency gate |

## 每个后续 MR 的更新契约

1. 开工前在本页登记编号、优先级、状态与验收条件；动态 P0 插到 P1 前执行。
2. 论文实现必须满足统一 metadata、中文解读、原文关键图、代码、指标和测试合同。
3. evolve 接入必须说明算子来自已实现论文、实时检索还是新组合假设，不能混写。
4. 完成后把状态改成 `DONE`，补充 PR 链接和关键证据；未完成部分拆出新编号。
5. 不在其他页面复制待办表；谱系页只链接本页，避免多个“剩余任务”互相矛盾。
