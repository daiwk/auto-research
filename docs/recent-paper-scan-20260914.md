# 近期论文扫描记录（2026-09-14）

## 覆盖声明

- 复核窗口：2026-09-09 至 2026-09-11，覆盖上一轮因 arXiv API 限流未能推进的重叠区间；
- 轨道：工业搜广推与风控、基础模型 / Evolve、LLM 后训练、Agent；
- 来源：arXiv 官方 recent/HTML/PDF、Google Research 官方论文页与博客、作者公开仓库；
- Google、Meta 候选继续最高优先，且工业论文按正文实验与部署段落而非摘要关键词判断；
- 本轮记录的是已逐篇核验的公开批次，不把 2026-09-12 至 2026-09-14 周末“无新提交”
  误写成穷尽性结果。下一轮保持从 2026-09-11 起的重叠扫描。

## 已实现 P0

| 领域 | 论文 | 本地 key | 实现与证据边界 |
|---|---|---|---|
| 工业风控 | SIRF（2609.11752） | `sirf` | 规则交互内化与 P95 阈值；概念诊断，不替代 8B CPT |
| LLM 后训练 | NSD（2609.11699） | `nsd` | 负教师与 reasoning gate；候选策略机制诊断 |
| Agent | COBRA-Skills（2609.11682） | `cobra-skills` | contextual-UCB 技能预算与反馈接纳 |
| Agent | Ecdysis（2609.11677） | `ecdysis` | 跨实例失败聚合与 FDCR 修复触发 |
| Agent | Grounding Agent Memory（2609.11060） | `grounded-memory` | 只读环境探测、冲突拒绝和记忆准入 |
| 基础模型 | OmniKVQuant（2609.11582） | `omnikvquant` | 2-bit windowed key quantization 与模态独立 value rotation |
| Agent | ToolGrad（2508.04086） | `toolgrad` | 补收 Google 官方发布的 answer-first textual gradient 路线 |
| Agent / 系统 | PROMPTS（MLSys 2026） | `prompts` | profiler 证据排序与受限 sharding 提案 |

## 已实现 P1

| 领域 | 论文 | 本地 key | 实现与证据边界 |
|---|---|---|---|
| 多模态基础模型 | SenseNova-U1.5（2609.11929） | `sensenova-u1-5` | 空间 patch target 与多专家 OPD reference |
| 多模态基础模型 | Caption-once, Frames-on-Demand（2609.11899） | `frames-on-demand` | visual-need gate 与帧预算选择 |
| 基础模型 | Data Scarcity and Model Sparsity（2609.11917） | `repeat-aware-moe` | 重复倍数/稀疏度感知正则 schedule |
| LLM 后训练 | Unified Per-Token OPD Gate（2609.11768） | `adaptive-opd-gate` | 四信号逐 token FKL/RKL gate |
| LLM 后训练 | LOCUS（2609.11739） | `locus` | task-aware SVD 低秩更新子空间 |
| 基础模型 | Musec（2609.11655） | `musec` | Muon momentum 的平滑谱裁剪 |
| 基础模型 | SWRouter（2609.11414） | `swrouter` | 相似度收缩窗口与模型路由 |
| LLM 后训练 | TASCO（2609.11393） | `tasco` | 邻域扰动稳定性约束的测试时适配 |
| Agent | SearchAtlas（2609.10901） | `searchatlas` | query-evidence-answer 图审计 |
| Agent | When Synthetic Data Hurts（2609.10750） | `skill-retention` | 真实样本 replay 与 anchor 抗遗忘 |
| Agent | T1（2609.11042） | `t1-terminal-rl` | exact-token 与 MoE route replay 诊断 |

所有条目均有独立中文页、论文信息块、原文关键图、三 seed 机制产物与明确复现边界。
后训练和 Agent 论文算子同时进入组合式 evolve；相关测试要求 mutation 改变真实执行路径和
中间量，只有 registry 名称不算接入。OmniKVQuant 当前只声明 NumPy reference，不宣称
Triton/CUDA 路径已完成，因此不伪造 GPU 验证回执。
