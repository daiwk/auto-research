# Jev 相关论文与方法谱系

目前没有公开的 Jev 技术论文，因此不能从产品名反推其内部结构。下列工作是可验证的**相邻方法**，用于构造本仓库的独立基线与评测轴。

| 方向 | 论文 | 可迁移到本仓库的机制 | 状态 |
|---|---|---|---|
| 动态候选分类 | [GLiClass](../foundation-models/2508.07662-gliclass/README.md) | 单次编码、文本与候选标签交互 | 本地 scorer operator |
| 校准奖励 | [RLCR](../post-training/2507.16806-rlcr/README.md) | 正确性 + proper scoring rule | Brier / hybrid objective |
| 决策 token 校准 | [Calibration-Aware RL](../post-training/2601.13284-calibration-aware-rl/README.md) | 对决策概率直接施加校准目标 | ECE/Brier 与 validation 温度校准 |

这些映射只说明“研究轴来自哪里”，不表示 Jev 采用了相同结构。
