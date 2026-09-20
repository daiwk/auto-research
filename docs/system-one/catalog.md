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

## 开放实现

| 实现 | 作者/机构 | 方法摘要 | 边界 |
|---|---|---|---|
| [NanoJev](https://github.com/TianyuCodings/NanoJev) | TianyuCodings | 在公开 Qwen3 基座上实现动态候选式结构化决策，提供可审计模型与数据路径 | 社区独立实现，不代表 Jev 内部结构 |
| [jevlike](https://github.com/vinnylarouge/jevlike) | vinnylarouge | 使用 option attention 为每个候选输出概率，复现 Jev 风格接口 | 社区独立实现，不与官方模型宣称等价 |

## 浏览入口

- [按机构/公司/学校](catalog/by-organization.md)
- [按主题](catalog/by-topic.md)
- [按年份](catalog/by-year.md)
- [论文谱系与缺口](lineage.md)
- [统一评测协议](benchmark.md)
