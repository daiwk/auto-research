# 结构化决策：按主题

## 类型化决策协议

- [TypeSafe Jev](../implementations.md#official-jev)：Choice、Score、Noul 三类问题共享状态输入，返回机器可直接消费的概率化结果。

## 动态候选分类

- [GLiClass](../../foundation-models/2508.07662-gliclass/README.md)：候选标签在运行时提供，文本与候选发生显式交互后统一归一化。
- [NanoJev](https://github.com/TianyuCodings/NanoJev)：在公开语言模型基座上实现动态候选接口。
- [jevlike](https://github.com/vinnylarouge/jevlike)：以 option attention 输出每候选概率。

## 概率校准与置信度

- [RLCR](../../post-training/2507.16806-rlcr/README.md)：将 proper scoring rule 纳入训练奖励，抑制无差别过度自信。
- [Calibration-Aware RL](../../post-training/2601.13284-calibration-aware-rl/README.md)：直接优化决策概率校准，并隔离 validation 与 test。

## 选择性预测与拒答

- 当前统一协议已经报告 coverage 与 selective accuracy，但尚缺公开、多难度、可比较的 abstention benchmark；列为 [P1 缺口](../lineage.md#selective-prediction)。

## 结构化评分、路由与风控

- Score 与 Noul 已进入 typed contract 和本地 provider；下一步需要增加有序评分、布尔风险决策和成本敏感路由的公共数据协议。
