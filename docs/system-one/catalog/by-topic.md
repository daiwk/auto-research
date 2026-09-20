# 结构化决策：按主题

## 类型化决策协议

- [TypeSafe Jev](../implementations.md#official-jev)：Choice、Score、Noul 三类问题共享状态输入，返回机器可直接消费的概率化结果。

## 动态候选分类

- [GLiClass](../../foundation-models/2508.07662-gliclass/README.md)：候选标签在运行时提供，文本与候选发生显式交互后统一归一化。
- [Bespoke Nimble](https://github.com/bespokelabsai/nimble)：在 Qwen3.5-9B 上训练 typed-schema logits，公开 checkpoint、数据与配方。
- [NanoJev](https://github.com/TianyuCodings/NanoJev)：在 Qwen3-0.6B 上训练 Choice、Boolean、Score 决策头。
- [Laya](https://github.com/NandhaKishorM/laya)：训练类型化决策模型，并公开温度校准路径。

## 并行约束解码与服务

- [SemIf](https://github.com/TheoLeeCJ/SemIf)：一次 shared-state prefill 后读取候选 logits，是工程路线而非训练式 Jev 复现。
- [openjev-sglang](https://github.com/ekzhang/openjev-sglang)：以 SGLang 验证并行约束解码的 GPU serving。
- 其余轻量 wrapper 见[社区实现全量快照](../implementation-tracker.md#decode-routes)。

## 扩散语言模型决策

- [DiffusionGemma / vLLM 等路线](../implementation-tracker.md#diffusion-routes)：探索非自回归并行决策，必须与训练 decision-head 路线分别评测。

## 概率校准与置信度

- [RLCR](../../post-training/2507.16806-rlcr/README.md)：将 proper scoring rule 纳入训练奖励，抑制无差别过度自信。
- [Calibration-Aware RL](../../post-training/2601.13284-calibration-aware-rl/README.md)：直接优化决策概率校准，并隔离 validation 与 test。

## 选择性预测与拒答

- 当前统一协议已经报告 coverage 与 selective accuracy，但尚缺公开、多难度、可比较的 abstention benchmark；列为 [P1 缺口](../lineage.md#selective-prediction)。
- [jev-ood-calibration](https://github.com/scienthoon/jev-ood-calibration) 是后续 OOD 与 coverage-risk 对照候选。

## 结构化评分、路由与风控

- Score 与 Noul 已进入 typed contract 和本地 provider；下一步需要增加有序评分、布尔风险决策和成本敏感路由的公共数据协议。
