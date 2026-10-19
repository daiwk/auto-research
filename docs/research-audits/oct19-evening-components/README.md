# 2026-10-19 晚间公告：低成本组件与版本升级

本批固定 **14 篇：11 个可执行组件/接口、3 篇仅资料**，合在一个 MR。13 个论文身份是 10 月 19 日公告中的新增收录，首发日主要为 10 月 15–16 日；UniRec 是 9 月论文的 **v3 实质更新**，不是第 14 篇当日首发。Google/Meta 优先核验：纳入 MSU/Meta ProPerAgent 和 ASU/Meta EgoP²C。

## 完整范围

| 领域 / 优先级 | 论文 | 本地可执行范围 | 验证 |
| --- | --- | --- | --- |
| Agent / P0 | [ProPerAgent](../../agent-research/2610.22671-proper-agent/README.md) | 因果图记忆、PPR、gate 来源接纳、内容×时机联合评分；抽取/语义模型由外部提供 | CPU，42/43/44 |
| Agent / P1 | [HDA](../../agent-research/2610.22466-harness-decomposition/README.md) | 四臂配对 bootstrap、人工确认控制、算力/过拟合/剩余上界带符号分解 | CPU，42/43/44 |
| Agent / P1 | [DRAGO](../../agent-research/2610.22568-drago/README.md) | grounded STRIPS 删除松弛、完整 BFS 诊断、拒绝弱化问题的修复门 | CPU，42/43/44 |
| 多模态 / P0 | [EgoP²C](../../foundation-models/2610.22681-ego-p2c/README.md) | 角色 FFN/LoRA、上下文白名单、片段实际采样及分配冻结教师的 MOPD | A100，42/43/44 |
| 基础模型 / P1 | [BMuon](../../foundation-models/2610.23571-bmuon/README.md) | 全局通道预算 MM 分配、双边加权 polar 更新；精确 SVD 非高速 kernel | A100，42/43/44 |
| 基础模型 / P1 | [Sink-Sparse](../../foundation-models/2610.22975-sink-sparse/README.md) | 校准集 block mass、覆盖前缀 mask、pooled-KV 与 LSE 正确融合 | A100，42/43/44 |
| 后训练 / P1 | [TreeOPSD](../../post-training/2610.23181-treeopsd/README.md) | 共享完整前缀树、策略概率回传、有界后验 KL 与实际微型 policy 更新 | A100，42/43/44 |
| 后训练 / P1 | [SimOPD](../../post-training/2610.23306-simopd/README.md) | 学生生成、配对更新前 FIFO bank、跨 hidden dim 的关系分布 KL | A100，42/43/44 |
| 后训练 / P1 | [GR-OPD](../../post-training/2610.23042-gr-opd/README.md) | 折扣均值、组相对序列信用、逐响应均衡 PPO、冻结教师 | A100，42/43/44 |
| 搜广推 / P0 升级 | [UniRec v3](../../reproductions/2609.11052-unirec/README.md) | CPPA/CAPP、AGRR 组内 KL、停止梯度的跨阶段目标；旧启发式降为概念演示 | A100，42/43/44 |
| JEV / P1 | [葡语 IR](../../foundation-models/2610.23346-jev-portuguese-ir/README.md) | 独立概率批量排序、精确覆盖、线性 nDCG/MRR、κ/τ-b；另复算原文表格 | CPU，42/43/44；未调用 JEV |
| 世界模型 / P1 | [PPMem](../../foundation-models/2610.23795-ppmem/README.md) | 仅方法、元数据、原图、代码可用性与成本判断 | 完整实验不复现，DONE |
| 后训练 / P1 | [MGE-PO](../../post-training/2610.23245-mge-po/README.md) | 仅四象限信用、课程和熵 KL 方法资料及实验限制 | 完整实验不复现，DONE |
| 后训练 / P1 | [MultiAgent-OPD](../../post-training/2610.23234-multiagent-opd/README.md) | 仅两阶段教师/学生团队、分角色监督资料及成本判断 | 完整实验不复现，DONE |

## 原始来源与日期

[来源回执](source-coverage.json)来自真实抓取的 51 页：8 个 arXiv 分类公告、Google 28 页、Meta 6 页、DeepMind 9 页。八公告均显示 **2026-10-19**，共解析 1,344 个分类条目，含 cross-list 和 replacement，**不能等同于 1,344 篇新论文**。分类解析条数与页面声明一致，不代表全部逐篇全文审查。

官方目录对比上一批抓取 SHA256 基线：Google 417、Meta 144、DeepMind 265 个唯一目录 URL 均无新增/字段变化。目录未变化不表示 Meta 没有新 arXiv 论文；两篇优先项由正文机构信息发现。完整摘要抓取仅保留在本地审计输入，不把 MB 级摘要快照塞入 Git；提交逐页 URL、时间、SHA256、解析计数及比较基线。

本批是**精选实现**，没有声称所有来源穷尽，也没有把“摘要没写 A/B”当成工业论文拒绝条件。UniRec v3 的正文明确九周监控、5% 随机流量、最终周 KPI 及全量部署；旧文档的 20%/一周和核心机制级别一并纠正。

其他重点读过的候选并未自动堆成组件：QART/Ori 等本轮不扩范围；Flash RNN-T 的定义性贡献是融合与重算 kernel，不以 PyTorch wrapper 冒充；AuditKIT/Tool Recommendation 等避免重复成熟上游或把封闭服务检索壳当模型。未完成逐篇全文核验的候选不标成“已实现”或“全量审结”。

## 实测与证据等级

执行源码固定于 `73a1e8b818bdddcdc33be13902e4d4c335c8fa26`，之后才在真实 **NVIDIA A100-SXM4-80GB** 上执行七项、每项三个 seed。三组 GPU runner 的实际运行时间分别约 1.68 秒、2.23 秒、1.44 秒，不含 SSH/加载开销；无数据集、checkpoint 下载或长实验。这是小张量/随机微型策略的机制验证，不是生产/语言/视觉任务成绩。

所有逐 seed 指标与 GPU 收据都链接在对应论文页；[冻结源码 Merkle 证明](frozen-sources.json)支持 squash 后浅克隆的离线校验，不依赖旧分支一直存在。收据只保留模型型号、公开合成配方、命令、代码提交、seed、结果与 hash，不写机器别名、用户名或驱动构建串。原始完整轨迹保留在本地 `runs/oct19-evening-components/`；Git 中的逐 seed 文件只含标量和审计 hash，避免重复提交几千行轨迹。

全部输出 `diagnostic_only=true`、`promotion_eligible=false`、`evolve_integrated=false`。EgoP²C 的固定 PLAN/DIRECT 骨架、随机冻结教师，Agent 的确定性回调，JEV 的 inert provider，都明确是诊断，不宣称语言/视频/Agent 能力。JEV [原文混淆矩阵算术复核](jev-published-table-arithmetic.json)独立标记为已发表聚合数字复算，不混进新模型推理指标。

## 同批修复与验收

- JEV 保留 Quati 与 JurisTCU 不同的等级 1 语义；两概率有限/归一化检查防止 NaN 绕过。
- GR-OPD 在 log ratio 空间选择等价 PPO 分支，避免正优势裁剪后 `0×inf` 反向 NaN；真正不可表示的负优势分支显式拒绝。
- SimOPD 拒绝零 hidden 维和 dtype 变更；BMuon 恢复全局步数，修复 subnormal score 分配数值边界。
- 原图逐张可视检查；修正 ProPerAgent PDF Figure 5 与 HTML 编号差异，并去除 HDA/BMuon/MultiAgent-OPD 裁剪中的无关正文。
- UniRec 历史 NDCG@10 负结果 −12.58% 原样保留，仅纠正概念演示的证据标签。新算子不能反向升级旧 adapter 的保真度。

14 篇的**完整实验**均为“成本过高，不复现（审查 DONE）”，不自动重试、不进实现队列、不阻塞批次。11 项组件验收与完整论文复现状态分开保存。

## 覆盖与水位

此批没有完成所有来源、所有公告条目的全文审查闭环，**审查水位维持 2026-10-15**。新公告观察日期、已审结候选、组件通过和全窗口水位是不同字段；不能因这 11 项通过就把全覆盖日期改到今天。
