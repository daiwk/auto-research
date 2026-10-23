# 结构化决策方法索引

本页汇总 System One 领域的官方产品契约、相邻论文方法和社区独立实现。Jev 未公开内部架构，因此“可调用官方模型”“论文官方代码”和“社区复现”必须分开理解。

## 官方产品与协议

| 方法 | 机构 | 类型 | 主要作用 | 集成状态 |
|---|---|---|---|---|
| [TypeSafe Jev](implementations.md#official-jev) | TypeSafe AI | 托管 System One 模型 | 对 `state` 上的 Choice、Score、Noul 问题直接返回概率化结构决策，不经过自然语言解析 | HTTPS provider 与 typed contract 已接入；未获密钥时不发起真实调用 |

## 论文方法

| 方向 | 方法 | 机构 | 日期 | 主要方法 | 本地入口 |
|---|---|---|---|---|---|
| 类型反馈持续适配 | [Jev-DLC](2610.31521-jev-dlc/README.md) | HKUST (Guangzhou) | 2026-10-22 | 冻结scorer上语义计数、双通道PA-I与fixed-share可靠性，严格先决策后反馈 | CPU状态组件与独立参考；不加载JEV，27B完整实验高成本不复现 |
| 多正确项校准审计 | [When Multiple Choices Are Correct](2610.29217-jev-multicorrect/README.md) | Independent Researcher | 2026-10-21 | 分离概率排序、完整集合恢复与独立二元校准；验证阈值固定后再评测test | CPU评分/隔离契约，未调用JEV，完整API实验高成本不复现 |
| 多模态choice重排 | [Multimodal Reranking Is a System One Decision](../multimodal-models/2610.28435-system-one-rerank/README.md) | Aalto University | 2026-10-20 | 同一图文上下文单前向读取候选字母logits，稳定重排并保留尾部 | SmolVLM-256M真实A100前向；仅L1接口，完整27B实验不复现 |
| 检索判定与重排 | [Jev 葡语 IR](../foundation-models/2610.23346-jev-portuguese-ir/README.md) | Câmara dos Deputados | 2026-10-16 | Choice 有序 qrels 与独立 Noul 概率排序分离，线性 nDCG/MRR、加权 κ 与 τ-b | CPU 协议接口与原文表格算术复核；未评测 Jev，完整实验不复现 |
| 选项独立决策 | [Prism-1](../foundation-models/2610.22066-prism-1/README.md) | NTU | 2026-10-15 | block mask 与共享位置消除跨选项依赖，以 yes/no 对数赔率形成选择分布 | 独立小模型组件，A100三种子机制验证；完整实验不复现 |
| 模拟前瞻 | [Code Owns the Simulation](../agent-research/2610.01834-jev-lookahead/README.md) | CUHK | 2026-10-01 | 代码逐动作克隆并模拟下一观察，把新可用动作交给 Jev 评分 | `choose_with_lookahead`；L1 协议诊断，未测真实 Jev |
| 动态候选分类 | [GLiClass](../foundation-models/2508.07662-gliclass/README.md) | Knowledgator | 2025-08-11 | 联合编码输入与运行时候选标签，通过一次候选交互得到完整分类分布 | `system-one:bilinear-ce`、`system-one:rival-ce` |
| 置信度训练 | [RLCR](../post-training/2507.16806-rlcr/README.md) | MIT | 2025-07-22 | 把 proper scoring rule 加入奖励，使正确性与诚实置信度共同进入优化目标 | `system-one:rival-brier`、`system-one:rival-hybrid` |
| 决策概率校准 | [Calibration-Aware RL](../post-training/2601.13284-calibration-aware-rl/README.md) | USC / AWS AI Labs | 2026-01-19 | 直接约束 decision-token 概率，并以 validation 温度校准降低过度自信 | validation calibration 与 ECE/Brier 报告 |

## 开放实现主干

| 实现 | 路线 | 方法摘要 | 集成状态 |
|---|---|---|---|
| [Bespoke Nimble](https://github.com/bespokelabsai/nimble) | 训练模型 | Qwen3.5-9B LoRA 对 flat typed schema 直接读取 enum/boolean logits | P0 候选；已收录、待统一执行 |
| [NanoJev](https://github.com/TianyuCodings/NanoJev) | 训练决策头 | Qwen3-0.6B + set-attention heads，覆盖 Choice、Boolean、Score | 已接入固定 checkpoint provider；A100 OOD 烟测通过 |
| [Laya](https://github.com/NandhaKishorM/laya) | 训练模型与校准 | typed decision + validation 温度校准 | P0 候选；已收录、待统一执行 |
| [SemIf](https://github.com/TheoLeeCJ/SemIf) | 并行约束解码 | shared-state prefill 后直接比较 option logits | P1 工程候选；不是训练式复现 |
| [DiffusionGemma routes](implementation-tracker.md#diffusion-routes) | 扩散模型 | 非自回归并行决策实验 | 独立路线；待校准和吞吐验证 |

[选型与集成路线图](implementations.md)解释各路线的适用场景；[社区实现全量快照](implementation-tracker.md)保存 tracker 的 48 项资料，避免把索引、解释文章或未发布预告计作可运行模型。

## 浏览入口

- [按机构/公司/学校](catalog/by-organization.md)
- [按主题](catalog/by-topic.md)
- [按年份](catalog/by-year.md)
- [论文谱系与缺口](lineage.md)
- [统一评测协议](benchmark.md)
- [Jev 开放实现选型](implementations.md)
- [社区实现全量快照](implementation-tracker.md)
