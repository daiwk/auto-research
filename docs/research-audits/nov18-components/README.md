# 2026-11-18：14 项低成本机会交付

[English](../../en/research-audits/nov18-components/README.md)

本批承接 [11.10—11.15 已闭环审查](../nov15-review-closure/README.md) 的 14 项机会，补齐可执行组件、独立指标、论文原图、中文与校对英文、四层学习问答和同主题对照。**不是新增 14 篇当天首发，也不是完整复现 14 个模型。** 审查水位仍为 2026-11-15，本批不声称又完成一次全来源扫描。

## 固定交付清单

| 方向 | 组件 | 本地边界 |
| --- | --- | --- |
| System One | [Typed Inbox](../../system-one/2610.32955-typed-inbox-protocol/README.md) | L0：冻结输入视图、线程隔离与 validation 行动成本阈值；不实现邮件分类模型 |
| Agent | [AskALCF](../../agent-research/2611.15700-askalcf-protocol/README.md) | L1：双范围充分性、粗粒度归因、版本缓存及人工 ship/revert；不是完整 28 规则系统 |
| Agent | [ProdPilot](../../agent-research/2611.17381-prodpilot-protocol/README.md) | L1：受限修复、独立复检、回滚和部署门；不连接真实云服务 |
| 多模态 | [FEND](../../multimodal-models/2611.18050-fend-protocol/README.md) | L0：20 秒截止、检测优先级与 human-FPR；没有音频模型 |
| 基础模型 | [Stratified Retention](../../foundation-models/2610.03713-stratified-retention-protocol/README.md) | L0：分层保留/修订评价提案；原文无经验实验，不捏造高成本实验 |
| 基础模型 | [Tokenization Premium](../../foundation-models/2611.13441-tokenization-premium/README.md) | L1：对齐文本一次性分词、UNK 排除、coverage/risk/ECE；不重建私有模型 |
| 多模态 | [RSLiveBench-UAV](../../multimodal-models/2611.14953-rslivebench-uav-protocol/README.md) | L0：滚动窗口、四个日历月 embargo、有限计分；无官方全数据或 VLM |
| 多模态 | [数字图书馆检索](../../multimodal-models/2611.17726-multimodal-library-protocol/README.md) | L0：外部嵌入检索、相关性指标与显式计时口径；不运行 Qdrant/ColPali |
| 后训练 | [Luce 相似性审计](../../post-training/2610.19095-luce-similarity-audit/README.md) | L1：相似性赔率、菜单偏移与迁移不确定性算术；不拟合偏好模型 |
| 基础模型 | [Runway](../../foundation-models/2611.12737-runway-inference-protocol/README.md) | L1：配置缓存、SLA 与单位一致的成本协议；不启动云推理 |
| 基础模型 | [Smart Routing](../../foundation-models/2611.15911-smart-model-routing/README.md) | L1：成本/质量和级联开销算术；不是线上推理路由器 |
| 后训练 | [Calibrated Judges](../../post-training/2611.19840-calibrated-judges-protocol/README.md) | L1：catch 校准、双 judge/双顺序与分歧 tie；不调用付费 judge |
| 基础模型 | [HVMap](../../foundation-models/2611.01514-hvmap/README.md) | L1：四层映射、跨目标 fuzzy loss、SCORE2 与 hub/spoke；不训练全量向量库 |
| 基础模型 | [Mixed Signals](../../foundation-models/2611.13758-mixed-signals-weights/README.md) | L0：外部原子补丁、practice 预算与评价接口；线性 harness 不是 TinyEEGNet |

逐篇定义、成本处置和机器可读状态见 [task-scope.json](task-scope.json)。每篇均有独立的 `metrics/component-cpu-seeds42-44.json`；仅两项 CUDA 路径另有 CUDA 指标和脱敏回执。评测框架/理论提案不伪装成一个新训练算法。

## 真实执行与证据边界

[预检预算](preflight.json) 固定单卡、180 秒、种子 42/43/44；模型/数据下载、预训练模型调用和 API 调用均为零。[CPU 原始产物](raw-cpu.json) 包含 14 项，[A100 原始产物](raw-cuda.json) 包含 HVMap 与 Mixed Signals 两项；绑定同一 [Git 源码证明](frozen-sources.json)。实际小算子批次 CPU 约 0.12 秒、CUDA 约 0.39 秒，**不是论文训练/推理的性能测量**。独立审查后的极值修复已重新冻结/实跑；[首轮记录](initial-9da5bfcf/disposition.json) 保留但不作最终验收。

HVMap 检查前后向、绝对对齐锚点、native 权重及联合排序；Mixed Signals 只检查真正写入权重并改变 forward、原子拒绝、失败消耗预算和外部指标。它没有 LLM 编辑器、EEG/ECG 模型或真实被试测试。协议例子的正确答案只留在独立评价器，不传给策略；多种子不改变 L0/L1 层级。没有能力比较、生产 A/B、Evolve 晋级或模型安全认证。

成本高的原论文完整矩阵明确 **不复现，审查 DONE**；私有架构缺失按不可重建范围记录，不硬套高成本；Stratified Retention 没有原始经验实验，保留 `no_original_experiment`。全部关闭自动重试和自动实现队列。

## 元数据与学习材料

Tokenization Premium 官方 Zenodo v1.0 已在 2026-09-22 发布，早于 11 月 arXiv；作者还提供测量脚本，不能写成“未开源”。HVMap 源码公开但未声明许可证，本地独立按公式实现。数字馆的数据库计时与端到端叙述不一致，显式分开口径，不把约 22k QPS 直接称作端到端表现。RA-Eval 的不同长度统计也保留原始分母差异。

四份学习问答源各包含四层问题，合计 56 题；英文逐题校对并绑定中文 SHA。14 条深读更新分别比较同主题既有论文，记录实际读取的 README SHA，不以目录标签代替比较。各领域的方法、机构、主题和时间目录及中英文学习页同步生成。

## 可复查命令

```bash
PYTHONPATH=src:scripts python -m pytest tests/test_nov18_root_components.py tests/test_nov18_agent_protocols.py tests/test_nov18_data_protocols.py tests/test_nov18_eval_protocols.py tests/test_nov18_delivery.py
PYTHONPATH=src:scripts python scripts/curate_nov18_evidence.py --check
python scripts/validate_gpu_evidence.py
python scripts/english_docs.py --require-complete
```

原始执行文件拒绝覆盖；复跑应指定新输出路径，不能改写已有通过/失败记录。
