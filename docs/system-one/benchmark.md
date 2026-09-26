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

`system-one-public` 使用 Nimble-compatible human-labeled JSONL，覆盖 Choice、Noul、Score。
正式 v1 是固定的 200 条公开人工标注样本，来源及许可见
[`manifest`](https://github.com/daiwk/auto-research/blob/main/data/system-one/system-one-public-v1.manifest.json)：

| 划分 | 数量 | 数据来源 | 用途 |
|---|---:|---|---|
| calibration | 60 | BoolQ、HelpSteer2、PubMedQA | 选择 backend、温度、阈值 |
| test | 60 | 相同来源的不同 ID | 冠军确定后一次报告 |
| OOD | 80 | ARC-Challenge、TruthfulQA | 跨来源压力测试；仅 Choice |

该固定切片采用各公开源前 40 条，先定样本后运行模型，没有模型依赖筛选；它覆盖
三种 typed decision，但不代表各数据集全集或官方排行榜。每个来源的 API URL、
配置、许可、响应 SHA256 与转换后套件 SHA256 均在 manifest 记录。构建器下载
公开数据；评测与 Evolve 默认只读取提交的 JSONL，不在线变更样本。

- `input` 只含 state/question；`reference.target` 永不进入 provider request；
- v1 按显式 calibration/test/OOD 字段切分，唯一 ID 防止重复；旧格式保留 family 划分；
- calibration 选择 backend、temperature 与 confidence threshold；test/OOD 仅报告冠军；
- 固定 checkpoint 只运行一次，不用重复 seed 制造“多 seed”表象；
- 通用指标为 accuracy、NLL、multiclass Brier、ECE、coverage、selective accuracy；
  Score 额外报告 MAE，并输出按 primitive 和 domain 的切片与最差组准确率。

该协议能评估开放实现之间的 typed-decision 互操作、校准与 OOD 行为，但不同模型的
训练域并不相同，因此单个小套件不能被解释为通用能力排行榜。

### A100 真实多轮验证（2026-09-26）

在固定 v1 数据哈希 `387638878933f8b6293b240a1daf5017fb317bd3c226e511c4e72cf3af46140d`
上，Nimble 与 Laya 开放 checkpoint 参加了 2 轮、5 个 trial 的 System One Evolve；
NanoJev 未提供给本次搜索，因此没有出现在候选中。控制器仅凭 60 条 calibration
选择，最终仍选初始 Nimble 配置 `g0-t0`，没有找到超过基线的改进。隔离 test 60 条
的 accuracy 为 `0.7333`、coverage `0.6167`、selective accuracy `0.8649`；
跨来源 OOD 80 条的 accuracy 为 `0.7625`、coverage `0.7500`。这是一次固定
checkpoint / seed 的可执行验证，不能推广为显著性提升或完整数据集排名。

完整去机器化证据见 [A100 receipt](../gpu-validations/system-one-formal-evolve-a100-20260926.json)；
原始预测、checkpoint 与包含绝对路径的运行产物不提交 Git。

本协议属于公开数据 L2 评测。它能比较相同 typed-decision 契约下的实现，但不能证明本地模型复现了 Jev 的训练方法或产品性能。

- [三 seed 汇总结果](metrics/banking77-local-seeds42-44.json)
- [可读报告](banking77-local-report.md)
- [NanoJev A100 checkpoint receipt](../gpu-validations/nanojev-checkpoint-a100-20260921.json)
- [Laya A100 checkpoint receipt](../gpu-validations/laya-checkpoint-a100-20260921.json)
- [Nimble A100 checkpoint receipt](../gpu-validations/nimble-checkpoint-a100-20260921.json)
