# System One 统一评测协议

协议 ID：`foundation.banking77.system_one.v1`。

- 数据：PolyAI Banking77（CC BY 4.0）；官方 train 用于训练，官方 test 按固定奇偶索引拆成 validation/test；
- 候选：每个样本均看到完整的 77 个 intent，禁止先用 gold label 缩小候选集；
- 选择：结构、目标、学习率和温度只看 validation；test 只用于最终报告；
- 种子：42、43、44；
- 主指标：accuracy；校准指标：NLL、Brier、ECE；决策指标：coverage、selective accuracy；
- 在线 Jev：一次请求可产生费用，默认不自动运行，也不把其结果伪装成本地复现结果。
- NanoJev：固定到公开 checkpoint commit；单 seed checkpoint 烟测不伪装成多 seed，且与本地从头训练基线分开报告。

## 多类型公共协议

`system-one-public` 使用 Nimble-compatible human-labeled JSONL，覆盖 Choice、Noul、Score：

- `input` 只含 state/question；`reference.target` 永不进入 provider request；
- 以完整 `family` 为单位确定性拆分 validation/test，禁止同源样本跨切分；
- validation 选择 backend、temperature 与 confidence threshold；test 仅报告冠军；
- 固定 checkpoint 只运行一次，不用重复 seed 制造“多 seed”表象；
- 通用指标为 accuracy、NLL、multiclass Brier、ECE、coverage、selective accuracy；
  Score 额外报告 MAE，并输出按 primitive 和 domain 的切片。

该协议能评估开放实现之间的 typed-decision 互操作、校准与 OOD 行为，但不同模型的
训练域并不相同，因此单个小套件不能被解释为通用能力排行榜。

本协议属于公开数据 L2 评测。它能比较相同 typed-decision 契约下的实现，但不能证明本地模型复现了 Jev 的训练方法或产品性能。

- [三 seed 汇总结果](metrics/banking77-local-seeds42-44.json)
- [可读报告](banking77-local-report.md)
- [NanoJev A100 checkpoint receipt](../gpu-validations/nanojev-checkpoint-a100-20260921.json)
- [Laya A100 checkpoint receipt](../gpu-validations/laya-checkpoint-a100-20260921.json)
- [Nimble A100 checkpoint receipt](../gpu-validations/nimble-checkpoint-a100-20260921.json)
