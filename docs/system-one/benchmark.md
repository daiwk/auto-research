# System One 统一评测协议

协议 ID：`foundation.banking77.system_one.v1`。

- 数据：PolyAI Banking77（CC BY 4.0）；官方 train 用于训练，官方 test 按固定奇偶索引拆成 validation/test；
- 候选：每个样本均看到完整的 77 个 intent，禁止先用 gold label 缩小候选集；
- 选择：结构、目标、学习率和温度只看 validation；test 只用于最终报告；
- 种子：42、43、44；
- 主指标：accuracy；校准指标：NLL、Brier、ECE；决策指标：coverage、selective accuracy；
- 在线 Jev：一次请求可产生费用，默认不自动运行，也不把其结果伪装成本地复现结果。

本协议属于公开数据 L2 评测。它能比较相同 typed-decision 契约下的实现，但不能证明本地模型复现了 Jev 的训练方法或产品性能。

- [三 seed 汇总结果](metrics/banking77-local-seeds42-44.json)
- [可读报告](banking77-local-report.md)
