# 近期论文扫描记录（2026-09-19）

## 覆盖范围

- arXiv 首次公开时间：2026-09-15 至 2026-09-18；以官方摘要页和 HTML/PDF 正文为准。
- 领域：工业搜广推与 LLM 应用、基础模型、LLM 后训练、Agent、多模态。
- 工业论文继续检查正文实验表、部署段和线上 A/B；摘要未写 A/B 不作为排除理由。
- Google / Meta 仍为工业扫描最高优先级；本窗口未发现满足线上证据门槛且尚未收录的新条目。

## 本批入选

| 优先级 | 论文 | 领域 | 本地实现 |
|---|---|---|---|
| P0 | ANGLE (2609.18296) | 广告检索 | L2 公开数据核心机制 |
| P0 | RetireOPD (2609.20784) | 后训练 / Agent RL | L1 |
| P0 | On-Demand Attention (2609.20734) | 基础模型 / 推理 | L1 + A100 |
| P0 | EvoSkill-GUI (2609.17653) | Agent | L1 observation-safe |
| P1 | ComPO (2609.19144) | 后训练 | L1 |
| P1 | Trajectory Learnability (2609.18321) | 后训练 | L1 |
| P1 | Dependency-Aware Trajectory Refinement (2609.18417) | Agent | L1 observation-safe |
| P1 | Harness Design for Coding Agents (2609.20804) | Agent 基础设施 | L1 observation-safe |
| P1 | CERA-MoA (2609.18779) | 多 Agent | L1 observation-safe |
| P1 | dQwen3.5 (2609.20751) | 基础模型 | L1 + A100 |
| P1 | ASPIRE (2609.17943) | 基础模型 / 推理 | L1 + A100 |

## 证据边界

本批基础模型 CUDA receipt 只证明 reference kernel 在真实 A100 上可执行且输出有限，不等于论文 checkpoint 或 serving 系统复现。Agent mini-suite 不读取 gold answer/plan；没有接入真实 GUI、SWE-bench 或 Terminal-Bench 的方法保持 `diagnostic_only`。ANGLE 的线上数字仅记录原文证据，本地结果来自 MovieLens 100K，二者不直接比较。
