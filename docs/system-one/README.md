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

## 可执行契约

- `Choice`：2–255 个动态候选，返回选择、完整概率分布和 confidence；
- `Score`：按有序 rubric 给分，同时保留各档概率；
- `Noul`：返回命题为真的概率；
- 多个问题使用同一份 state，但彼此独立评估。

代码入口：`src/auto_research/system_one/`。HTTP provider 严格校验 HTTPS、question id 和概率和；本地 provider 不访问标准答案，也不会生成一段“answer”冒充决策能力。

## Evolve

`system-one` 已进入统一多轮控制器，候选不是网上临时生成的黑盒代码，而是仓库内可执行且测试覆盖的四个 operator：

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

选择阶段只读取 validation；test 在冠军确定后报告。默认协议为 `foundation.banking77.system_one.v1`，同时报告 accuracy、NLL、Brier、ECE、覆盖率和选择性准确率。

当前公开三 seed 本地基线为 accuracy `0.1353±0.0475`、Brier `0.9749±0.0004`、ECE `0.1048±0.0508`；完整逐 seed 数据见[指标产物](metrics/banking77-local-seeds42-44.json)。这是 800 次样本更新的小预算基线，明显不是 Jev 产品性能，也不应与 GLiClass 完整 checkpoint 数字横比。

## 延伸阅读

- [方法索引](catalog.md)
- [按机构/公司/学校](catalog/by-organization.md) · [按主题](catalog/by-topic.md) · [按年份](catalog/by-year.md)
- [Jev 与开放实现](implementations.md)
- [社区实现全量快照](implementation-tracker.md)：48 项资料按技术路线归类，含 P0/P1 集成候选
- [论文谱系与缺口](lineage.md)
- [评测协议](benchmark.md)
- [TypeSafe 官方介绍](https://docs.typesafe.ai/introduction)
- [TypeSafe Choice 契约](https://docs.typesafe.ai/primitives/choice)
