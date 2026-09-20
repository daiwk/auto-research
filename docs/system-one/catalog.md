# 结构化决策方法索引

本页汇总 System One 领域的官方产品契约、相邻论文方法和社区独立实现。Jev 未公开内部架构，因此“可调用官方模型”“论文官方代码”和“社区复现”必须分开理解。

## 官方产品与协议

| 方法 | 机构 | 类型 | 主要作用 | 集成状态 |
|---|---|---|---|---|
| [TypeSafe Jev](implementations.md#official-jev) | TypeSafe AI | 托管 System One 模型 | 对 `state` 上的 Choice、Score、Noul 问题直接返回概率化结构决策，不经过自然语言解析 | HTTPS provider 与 typed contract 已接入；未获密钥时不发起真实调用 |

## 论文方法

| 方向 | 方法 | 机构 | 日期 | 主要方法 | 本地入口 |
|---|---|---|---|---|---|
| 动态候选分类 | [GLiClass](../foundation-models/2508.07662-gliclass/README.md) | Knowledgator | 2025-08-11 | 联合编码输入与运行时候选标签，通过一次候选交互得到完整分类分布 | `system-one:bilinear-ce`、`system-one:rival-ce` |
| 置信度训练 | [RLCR](../post-training/2507.16806-rlcr/README.md) | MIT | 2025-07-22 | 把 proper scoring rule 加入奖励，使正确性与诚实置信度共同进入优化目标 | `system-one:rival-brier`、`system-one:rival-hybrid` |
| 决策概率校准 | [Calibration-Aware RL](../post-training/2601.13284-calibration-aware-rl/README.md) | USC / AWS AI Labs | 2026-01-19 | 直接约束 decision-token 概率，并以 validation 温度校准降低过度自信 | validation calibration 与 ECE/Brier 报告 |

## 开放实现主干

| 实现 | 路线 | 方法摘要 | 集成状态 |
|---|---|---|---|
| [Bespoke Nimble](https://github.com/bespokelabsai/nimble) | 训练模型 | Qwen3.5-9B LoRA 对 flat typed schema 直接读取 enum/boolean logits | P0 候选；已收录、待统一执行 |
| [NanoJev](https://github.com/TianyuCodings/NanoJev) | 训练决策头 | Qwen3-0.6B + set-attention heads，覆盖 Choice、Boolean、Score | P0 候选；已收录、待统一执行 |
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
