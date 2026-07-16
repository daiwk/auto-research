# Auto Research 自动研究

Auto Research 负责把“我想研究什么”转成一条可追踪、可复现的实验链路。它与论文复现互补：论文复现回答“这篇工业论文的方法在公开数据上如何表现”，Auto Research 回答“围绕一个 topic 或现有模型，下一步应该尝试什么，并怎样持续迭代”。

## 两种入口

| 入口 | 输入 | 自动执行 | 适用场景 |
|---|---|---|---|
| Topic research | topic、LLM/推荐轨道、论文数、实验次数 | arXiv 检索、参数提案、逐次实验、缓存与报告 | 探索一个较宽的研究问题 |
| Model evolution | 基础模型、数据集、自然语言调研方向 | 论文检索、结构/数据/训练消融、并行实验、冠军进化、隔离 test | 升级 RankMixer、HyFormer 或本地 LLM |

## Topic research

```bash
auto-research run \
  --topic "ranking loss and hard negative sampling" \
  --track recommendation \
  --trials 8 \
  --papers 8
```

系统会记录论文发现、每个 trial 的配置和指标、当前最优结果以及失败原因。内置低成本实验用于验证研究管线；正式研究可以通过配置文件接入自己的实现命令、实验命令、指标方向和参数空间。

LLM 方向使用 `--track llm`，推荐、搜索和广告方向使用 `--track recommendation`。无网络环境可加 `--offline`，已有实验缓存会继续复用。

## 模型定向进化

```bash
auto-research evolve \
  --model rankmixer \
  --dataset movielens-1m \
  --direction "把 LONGER、UniMixer 及相关高效 Transformer 结构加入 RankMixer" \
  --generations 3 \
  --population 6 \
  --workers 3 \
  --steps 300 \
  --papers 8 \
  --seeds 42,43,44
```

第一轮固定超参数，只比较结构；第二轮开始围绕冠军调整层数、维度、学习率、优化器与 batch size。同一代实验使用独立进程并行，validation 决定晋级，test 只在全部迭代结束后运行。

[查看完整的模型进化协议、数据规模和结构算子 →](model-evolution.md)

LLM 轨道使用 `micro-llm + WikiText-2`：第 1 轮比较 GQA、RoPE/RMSNorm/SwiGLU、parallel block 等结构；第 2 轮比较预训练数据配方；第 3 轮比较 SFT 与 NEFTune。默认模型约 12M–16M 参数，可以在 Apple Silicon 上从头训练。

## 研究产物

每次运行独立保存，不覆盖历史实验：

```text
runs/<research-id>/
├── result.json     # 配置、论文证据、指标和最优结果
├── report.md       # 可审查的研究结论
└── events.jsonl    # 逐阶段、逐 trial 事件日志

runs/evolution/<model>-<timestamp>/
├── result.json     # 结构 genome、父子关系和完整指标
├── report.md       # 中文多轮研究报告
└── index.html      # 可直接打开的研究看板
```

## 安全与可审计边界

- 在线发现但尚未实现的论文先进入 evidence-only，不直接执行任意生成代码。
- 模型晋级只读取 validation，禁止提前观察 test 选择方案。
- 数据裁剪、评估 cohort、seed、训练预算和失败实验全部进入报告。
- checkpoint、公开数据和原始 runs 留在本地，不提交 Git；稳定指标和复现方法才进入文档。
