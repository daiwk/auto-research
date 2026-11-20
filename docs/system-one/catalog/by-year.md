# 结构化决策：按年份

论文按 arXiv v1 日期倒序排列。Jev 是持续更新的托管产品，不伪造论文发布日期，因此放在单独的产品入口。

## 2026

- **2026-11-19** — [LoopRoute](../2611.25363-looproute/README.md)：重复公共state-action对触发两步LLM接管；仅CPU控制核，完整模型评测不复现。

- **2026-11-18** — [EgoJev](../2611.24616-egojev/README.md)：显式决策概率的窗口融合和分位数选帧；CPU后处理组件，完整VLM视频矩阵不复现。
- **2026-11-18** — [Jeveration](../2611.24738-jeveration/README.md)：共享随机状态的一次前向图像code生成；完整多日训练不复现，仅资料收录。

- **2026-10-23** — [Typed Inbox](../2610.32955-typed-inbox-protocol/README.md)：冻结模型可见快照、整线程隔离，以validation成本选行动阈值；L0协议不是邮箱模型复现。
- **2026-10-21** — [When Multiple Choices Are Correct](../2610.29217-jev-multicorrect/README.md)：排序正确不等于恢复全部正确选项；本地仅CPU评分、概率精度与validation/test隔离协议，完整付费API实验不复现。
- **2026-10-20** — [System One多模态重排](../../multimodal-models/2610.28435-system-one-rerank/README.md)：同一图文上下文一次前向读取候选概率；A100真实小VLM接口诊断，不是完整27B评测。
- **2026-10-16** — [Jev 葡语 IR](../../foundation-models/2610.23346-jev-portuguese-ir/README.md)：有序判定与独立概率重排协议；CPU 合同检查和原文表格复算，不调用 Jev，完整 API 实验不复现。
- **2026-10-15** — [Prism-1](../../foundation-models/2610.22066-prism-1/README.md)：选项隔离与共享位置下的单步赔率决策；A100三种子机制组件，非完整模型能力实验。
- **2026-01-19** — [Calibration-Aware Reinforcement Learning](../../post-training/2601.13284-calibration-aware-rl/README.md)：直接约束决策概率，在保持任务正确率的同时改善 ECE。

## 2025

- **2025-08-11** — [GLiClass](../../foundation-models/2508.07662-gliclass/README.md)：面向运行时动态标签的一次编码分类架构。
- **2025-07-22** — [RLCR](../../post-training/2507.16806-rlcr/README.md)：使用 proper scoring rule 训练诚实置信度。

## 产品与开放实现

- [TypeSafe Jev](../implementations.md#official-jev)
- [NanoJev](https://github.com/TianyuCodings/NanoJev)
- [jevlike](https://github.com/vinnylarouge/jevlike)
