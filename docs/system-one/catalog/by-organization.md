# 结构化决策：按机构/公司/学校

论文按第一作者所属机构聚合；产品和社区项目单独标明，避免把开源作者误写成论文机构。

## TypeSafe AI

- [Jev](../implementations.md#official-jev)：官方托管 System One 模型，公开 Choice、Score、Noul 类型化决策协议；内部架构、训练集和权重尚未公开。

## Knowledgator

- [GLiClass](../../foundation-models/2508.07662-gliclass/README.md)（2025-08-11）：把输入文本和动态候选标签共同编码，以一次前向计算输出完整候选分布。

## Massachusetts Institute of Technology

- [RLCR](../../post-training/2507.16806-rlcr/README.md)（2025-07-22）：用 proper scoring rule 联合优化正确性和置信度，提供结构化决策的校准训练轴。

## University of Southern California / AWS AI Labs

- [Calibration-Aware RL](../../post-training/2601.13284-calibration-aware-rl/README.md)（2026-01-19）：直接校准决策概率，并要求校准参数只在 validation 上选择。

## 社区独立实现

- [NanoJev](https://github.com/TianyuCodings/NanoJev)：公开基座上的 Jev 风格动态候选实现。
- [jevlike](https://github.com/vinnylarouge/jevlike)：基于 option attention 的 Jev 风格概率决策实现。
