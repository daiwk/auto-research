# 2026-11-15 增量论文交付：新公告与历史补漏分开

本轮固定收录 **18 篇：13 个低成本组件/接口、5 篇资料收录**。其中 7 个组件在单张 A100 上做真实三种子小张量验证；这些是 L0 接口或 L1 机制诊断，**没有完整模型能力复现，也没有新增 evolve 提升证据**。

## 本轮清单

| 领域 | 论文与本地范围 | 交付边界 |
| --- | --- | --- |
| 搜广推 | [ReSID](../../recommendation-components/2611.16404-resid/README.md) | 并行量化、势能引导束搜索、部分 SID 匹配；CPU L1 |
| 搜广推 | [TriGen](../../recommendation-components/2611.16395-trigen/README.md) | 固定窗口尾部注入、原始历史双路径条件、逐层 PFFN；CPU/CUDA L1 |
| 评测 | [KuaiRecV2](../../recommendation-components/2611.16795-kuairec-v2-protocol/README.md) | 日级 validation、实例加权汇总、一次召回评估多行为；CPU L0，非完整基准接入 |
| 基础模型 | [Unbundling](../../foundation-models/2611.17334-unbundling-vision/README.md) | Meta FAIR，视觉专属 QKVO/FFN 的小块机制；CPU/CUDA L1 |
| 基础模型 | [ArchSpace](../../foundation-models/2611.17332-archspace/README.md) | 耦合扩展规律与训练配方的算术；CPU L1，非结构搜索 |
| 基础模型 | [D-JEPA](../../foundation-models/2611.16639-d-jepa/README.md) | shared/private 四组约束与单 context 目标；CPU/CUDA L1 |
| 基础模型 | [DuoJEPA](../../foundation-models/2611.15968-duojepa/README.md) | 目标空间双向损失、精确 SVD 初始化的 skipless 层；CPU/CUDA L1 |
| 后训练 | [LGPO](../../post-training/2611.15404-lgpo/README.md) | 当前策略均值似然门控与真实梯度；CPU/CUDA L1 |
| 后训练 | [Safety as a Budget](../../post-training/2611.16628-safety-budget-cgrpo/README.md) | PAV 校准、分离惩罚/dual通道及显式状态；CPU L1 |
| 后训练 | [Bait 防御组件](../../post-training/2611.16369-bait-reward-defense/README.md) | Google DeepMind 合作；仅数值 probe 奖励差和整组符号变换，非攻击模型；CPU L1 |
| Agent | [CoReMem](../../agent-research/2611.17316-coremem/README.md) | 成功优先 reward、来源门控与记忆信用；CPU/CUDA L1 |
| Agent | [CapLite](../../agent-research/2611.17115-caplite/README.md) | 平面 schema、精确请求 grounding、已承诺写操作前缀；CPU L1 |
| Agent | [ACE-RL](../../agent-research/2611.16409-ace-rl/README.md) | 三角色信用、playbook编辑和 clipped目标；CPU/CUDA L1 |
| 高成本资料 | [PixVid](../../multimodal-models/2611.17336-pixvid/README.md) | 完整视频模型实验不复现，审查 DONE，无伪运行入口 |
| 高成本资料 | [MULTILOOP](../../agent-research/2611.15754-multiloop/README.md) | Google 合作的多 loop 实证研究；不制造“新优化算法” |
| 历史补漏 | [Stellar Colosseum](../../agent-research/2609.15983-stellar-colosseum/README.md) | Google，9月首发、11月官方博客触发补录；长程证明实验不复现 |
| 历史修订 | [LEAP](../../agent-research/2606.03303-leap-formal-math/README.md) | Google，6月首发、固定 v3 审读；收费形式化数学全实验不复现 |
| 理论资料 | [Spectral Ghost](../../foundation-models/2601.20154-spectral-ghost/README.md) | 1月首发、固定 v4；原文无实证实验，不编造“高成本训练”理由，保留 v1 Google 署名历史 |

所有论文均有完整元信息、原论文关键图、中英文正文、四层问答和同主题深读更新。JEPA 是表征研究，不混入以 typed decisions 为核心的 System One / JEV 主题。

## 扫描覆盖与例外

六个官方 arXiv 当前公告页面均完整解析，公告日为 **2026-11-13**；去重后 1,403 个元数据身份包括新稿、交叉收录和旧文修订，**不是 1,403 篇符合要求的论文，也不是待实现队列**。见[来源收据和例外](source-coverage.json)、[元数据索引](announcement-index.json)及[固定交付范围](task-scope.json)。

Google/Meta 按原文署名核验，不因作者姓名熟悉就判机构。Meta 官方入口本次不可用，但 Unbundling 的固定原文独立确认了 Meta FAIR。Google 的产品公告、天气/基因领域资料、已收录 AlphaProof Code 与真正的新方法分流记录，未伪称全部进入代码库。Serving-Aligned CTR KD 原文只有离线结果，不满足工业线上证据门槛；PolyMorphWBC 是本轮主题外的专用全身控制，且一作机构未列。

这次是有界选题交付，不是从审查水位到今天的完整逐篇闭环。**统一审查水位仍为 2026-11-09**，没有用本轮发布日期偷换水位。未读线索与不可用入口保留其真实状态，不自动重试昂贵实验。

## 验证口径

[预检预算](preflight.json)限定最多一张 A100/A30、180秒、三个种子 42/43/44；模型/数据下载、预训练模型调用和 API 调用均为零。[CPU 原始执行](raw-cpu.json)、[A100 原始执行](raw-cuda.json)和[Git 源码证明](frozen-sources.json)绑定同一真实提交。每篇有独立指标文件，7项另有经统一验证器接受的去机器身份回执。

最终冻结前严格门发现并修正：ArchSpace 诊断缺 seed，Safety 的 NumPy 布尔类型不可 JSON 序列化，DuoJEPA 的 SVD 初始化不应先落 CPU。独立审查还补了非有限控制量和 padding NaN 的拒绝路径。历史尝试与成功但非最终源码的原始产物保留，不覆盖伪装；最终验收只使用上面最终源证明和 raw 文件。

这里“通过”仅表示原始算子、负对照、梯度或接口契约正确。三种子、零失败或局部损失下降都不能证明推荐收益、Agent 成功率、世界模型能力或安全保证。完整高成本实验明确不复现，按用户规则视为审查 DONE，不再阻塞选题闭环。

## 同一 PR 的 V-CoLA 依赖兼容修复

远端新依赖暴露了已有 V-CoLA 的边界问题：Transformers 5.23 把 grouped-value attention 的 Q/K 连续分组扩展移进 kernel，外部轴仍为 `[batch, sequence, heads, dimension]`，不是轴布局改变。本地现在仅在捕获后、状态重放前按官方 `repeat_interleave` 规则对齐 Q/K；不改变真实 kernel 调用、原状态算法或数值门槛，已扩展的旧输入保持原样。

旧 5.14 和新 5.23 的 18 项回归均通过，包括原始完整前向等价、物理缩短、并发隔离与异常恢复。另有[固定源码证明](vcola-compat/frozen-sources.json)、[CPU](vcola-compat/raw-cpu.json)和[真实 A100 三种子小模型记录](vcola-compat/raw-cuda.json)：执行随机初始化的微型 Qwen3.5 真实视觉编码器和混合层，不下载权重/数据，不把它说成重新验证 9B checkpoint 的质量。此前 9B 实验及其旧回执保留为历史测量；这次新增的是接口兼容验收，不增加论文数量或能力复现数量。
