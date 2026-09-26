# 结构化决策 / System One

Jev 是 TypeSafe AI 公布的第一个 **System One** 模型：输入一份 `state` 和若干 typed questions，直接返回可供程序消费的结构化决策，不生成自然语言答案。本仓库把这条路线拆成三层，避免把社区猜测写成官方事实。

这是与基础模型、后训练和 Agent 并列的独立研究域。它研究的不是如何生成自然语言，而是如何在动态候选、评分量表或布尔命题上给出类型安全、概率可校准、可直接执行的决策。Jev 是核心产品入口；GLiClass、校准学习与社区实现构成可公开验证的方法谱系。

| 层次 | 本仓库提供什么 | 证据边界 |
|---|---|---|
| 官方契约 | Choice、Score、Noul 数据结构与可选 TypeSafe HTTP provider | 只实现公开 API；TypeSafe 未公布 Jev 的权重、训练集或模型结构 |
| 可复现实验 | 动态候选 scorer、proper-scoring objective、温度校准、Banking77 三 seed 协议 | 独立、可审计的本地基线，不宣称复现 Jev 内部架构 |
| 开放生态 | 48 项社区实现、评测和索引的分层快照 | 训练 checkpoint、推理解码、扩散路线和解释材料分别标注，收录不等于已集成 |

## 一键运行

本地后端无需密钥，也无需 GPU：

```bash
auto-research system-one-eval \
  --backend local \
  --architecture rival_attention \
  --objective hybrid \
  --seeds 42,43,44
```

在线对照只在用户显式配置 `TYPESAFE_API_KEY` 时调用，不会把密钥写入结果：

```bash
TYPESAFE_API_KEY=... auto-research system-one-eval --backend typesafe
```

三个开放 checkpoint 后端均固定到经过审计的不可变 revision。NanoJev、Nimble 的
审计路径需要 CUDA；Laya 同时支持 CPU，但正式证据仍在 A100 上复核：

```bash
pip install -e '.[system-one-gpu]'
auto-research system-one-eval \
  --backend nanojev --device cuda:0 --precision bf16 \
  --maximum-eval-examples 100
```

Nimble 是 Qwen3.5-9B LoRA，离线执行时必须同时给 adapter 与固定 base snapshot；
Laya 是 421M ModernBERT typed-decision head：

```bash
auto-research system-one-eval --backend nimble --dataset public-jsonl \
  --public-data data/system-one/system-one-public-v1.jsonl \
  --checkpoint-dir /checkpoints/nimble --base-model-dir /checkpoints/qwen3.5-9b \
  --offline --device cuda:0

auto-research system-one-eval --backend laya --dataset public-jsonl \
  --public-data data/system-one/system-one-public-v1.jsonl \
  --checkpoint-dir /checkpoints/laya --offline --device cuda:0
```

未指定 `--checkpoint-dir` 时会下载 `C-Tianyu/NanoJev` 的固定 commit；`--offline`
模式必须提供已下载目录。该 provider 执行作者发布的真实 0.6B checkpoint，不读取
gold answer，也没有自回归输出 token。

## 可执行契约

- `Choice`：2–255 个动态候选，返回选择、完整概率分布和 confidence；
- `Score`：按有序 rubric 给分，同时保留各档概率；
- `Noul`：返回命题为真的概率；
- 多个问题使用同一份 state，但彼此独立评估。

代码入口：`src/auto_research/system_one/`。HTTP provider 严格校验 HTTPS、question id 和概率和；本地 provider 不访问标准答案，也不会生成一段“answer”冒充决策能力。

## Evolve

`system-one` 已进入统一多轮控制器。候选不是只有名字的 registry 条目：控制器仅在
用户提供对应 checkpoint 路径后，才暴露并实际执行 NanoJev、Nimble 或 Laya operator。
本地训练有四个 operator：

- `system-one:bilinear-ce`
- `system-one:rival-ce`
- `system-one:rival-brier`
- `system-one:rival-hybrid`

```bash
auto-research evolve \
  --model system-one \
  --dataset banking77 \
  --direction "比较动态候选交互结构与校准目标" \
  --generations 3 --population 4 --seeds 42,43,44
```

开放 checkpoint 可在同一份 human-labeled Choice/Noul/Score JSONL 上联合搜索后端、
温度和 selective confidence threshold：

```bash
auto-research evolve --model system-one --dataset system-one-public \
  --direction "比较开放 System One checkpoint、校准温度与拒答阈值" \
  --system-one-public-data data/system-one/system-one-public-v1.jsonl \
  --system-one-nimble-checkpoint /checkpoints/nimble \
  --system-one-nimble-base /checkpoints/qwen3.5-9b \
  --system-one-laya-checkpoint /checkpoints/laya \
  --offline --device cuda:0
```

公开套件 v1 包含 200 条固定人工标注样本：calibration 60、test 60、独立来源
OOD 80。选择阶段只读取 calibration；test/OOD 在冠军确定后报告。该套件用于
比较 Choice/Noul/Score 契约、校准与跨来源行为，不能解释为通用产品性能排名。
数据源、许可、逐源响应哈希及整体哈希见
[`system-one-public-v1.manifest.json`](https://github.com/daiwk/auto-research/blob/main/data/system-one/system-one-public-v1.manifest.json)；
可用 `python scripts/build_system_one_public_suite.py --output data/system-one/system-one-public-v1.jsonl`
重新构建。Banking77 本地训练仍使用独立的 `foundation.banking77.system_one.v1` 协议。

当前公开三 seed 本地基线为 accuracy `0.1353±0.0475`、Brier `0.9749±0.0004`、ECE `0.1048±0.0508`；完整逐 seed 数据见[指标产物](metrics/banking77-local-seeds42-44.json)。这是 800 次样本更新的小预算基线，明显不是 Jev 产品性能，也不应与 GLiClass 完整 checkpoint 数字横比。

NanoJev 在 A100 上的真实 checkpoint 烟测使用 12 条 validation 与 12 条隔离 test：
test accuracy `0.1667`、NLL `3.9825`、Brier `0.9745`、ECE `0.1397`、schema
validity `1.0`。这是游戏/决策 checkpoint 到 Banking77 的小样本 OOD 互操作验证，**不是**
稳定能力排名；去机器化证据见 [GPU receipt](../gpu-validations/nanojev-checkpoint-a100-20260921.json)。

Laya 的固定公开 checkpoint 也已在 A100 上执行 Choice、Noul、Score 混合协议；结果和
数据哈希见 [Laya GPU receipt](../gpu-validations/laya-checkpoint-a100-20260921.json)。
同一协议下的 Qwen3.5-9B + Nimble LoRA 路径亦完成真实 A100 验证；见
[Nimble GPU receipt](../gpu-validations/nimble-checkpoint-a100-20260921.json)。

公共多类型协议与 Nimble 上游发布格式兼容：每条记录把 `input` 和 `reference` 物理
分开，loader 会拒绝 input 中的 target/answer/label/gold 字段。正式 v1 使用显式
calibration/test/OOD 划分并核对唯一 ID；旧格式仍按 source family 切分。这样可以报告
Choice、Noul、Score 的 accuracy、NLL、Brier、
ECE、coverage、selective accuracy、Score MAE 和按类型/领域切片，而不会把标准答案交给模型。

## 延伸阅读

- [方法索引](catalog.md)
- [按机构/公司/学校](catalog/by-organization.md) · [按主题](catalog/by-topic.md) · [按年份](catalog/by-year.md)
- [Jev 与开放实现](implementations.md)
- [社区实现全量快照](implementation-tracker.md)：48 项资料按技术路线归类，含 P0/P1 集成候选
- [论文谱系与缺口](lineage.md)
- [评测协议](benchmark.md)
- [TypeSafe 官方介绍](https://docs.typesafe.ai/introduction)
- [TypeSafe Choice 契约](https://docs.typesafe.ai/primitives/choice)
