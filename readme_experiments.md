# 运行论文实验与自动研究

[返回项目首页](README.md) · [文档站](https://daiwk.github.io/auto-research/)

先完成[安装与数据准备](readme_setup.md)。以下保留各工作流的完整命令示例；模型与数据成本请先按对应文档评估。

## 运行论文复现

列出的 key 会由 adapter registry 动态生成：

```bash
auto-research list
auto-research reproduce --help
```

运行单篇或全部论文：

```bash
auto-research reproduce --paper memento --seed 42
auto-research reproduce --paper sasrec --seed 42
auto-research reproduce --paper hstu --seed 42
auto-research reproduce --paper transact-v2 --seed 42
auto-research reproduce --paper pinfm --seed 42
auto-research reproduce --paper m6rec --seed 42
auto-research reproduce --paper kar --seed 42
auto-research reproduce --paper bahe --seed 42
auto-research reproduce --paper beque --seed 42
auto-research reproduce --paper precise --seed 42
auto-research reproduce --paper pinrec --seed 42
auto-research reproduce --paper genrank --seed 42
auto-research reproduce --paper learn --seed 42
auto-research reproduce --paper notellm --seed 42
auto-research reproduce --paper onerec-v2 --seed 42
auto-research reproduce --paper self-evolving-rec --seed 42
auto-research reproduce --paper prompt-generation --seed 42
auto-research reproduce --paper univa --seed 42
auto-research reproduce --paper pinterest-ads-llm --seed 42
auto-research reproduce --paper lwgr --seed 42
auto-research reproduce --paper sigma --seed 42
auto-research reproduce --paper s-grec --seed 42
auto-research reproduce --paper all --seed 42

# 仅在明确需要查看旧概念验证时加入
auto-research reproduce --paper all --include-concept-demos --seed 42
```

正式批量比较建议使用统一筛选、三个 seed 和可恢复状态文件：

```bash
auto-research reproduce --paper all --track recommendation --topic ranking \
  --fidelity full_pipeline --seeds 42,43,44 --workers 3 \
  --state-file runs/reproductions/ranking-state.json
```

新结果使用 schema v2，写入论文 manifest、L0–L3 评测层级、代码 commit、环境、预算
和 seed；多 seed 批次额外生成均值、标准差和 95% 置信区间。单 seed 只属于 smoke，
不能表述为稳定提升。

`--budget smoke|standard` 不是标签：每个 adapter 会在独立进程执行，分别施加 5 分钟
和 60 分钟硬截止，超时后终止进程并返回失败；可用 `--budget-seconds` 做显式覆盖。
`paper-specific` 保留论文 adapter 自己声明的训练日程，不增加统一截止。

每篇论文、每次运行写入独立且不可变的目录：

```text
runs/reproductions/<arxiv-id>-<adapter>/<timestamp>/
├── result.json   # 机器可读事实来源
└── report.md     # adapter 渲染的实验结论
```

`data/` 与 `runs/` 默认不进入 Git。经过复核的长期结论写入 `docs/reproductions/<arxiv-id>-<adapter>/README.md`。

## 运行模型自动进化

内置基础模型包括推荐侧 RankMixer/HyFormer，以及可在 Mac、Linux GPU 或 Linux CPU 从头训练的 `micro-llm`。推荐正式实验建议使用 MovieLens-1M：

候选来源需要先区分清楚：

- 运行时会按 `--direction` 搜索最新论文，但尚未在仓库实现的论文只标记为
  `evidence-only`，不会直接执行；
- 真正进入训练的论文结构或算法都已经在本仓库实现、测试并登记映射；
- 系统会在这些白名单算子之间做组合和超参数变异。这可以产生新的工程实验假设，
  默认不会根据论文 PDF 现场执行任意代码。可选的 `--candidate-generator-command`
  只把外部生成结果写入隔离候选区并执行验证；仍需显式 `candidate promote --approve`
  后，候选才可能在后续运行注册为可执行算子。

具体例子、离线模式和报告中的来源标记见
[候选到底从哪里来](docs/model-evolution.md#candidate-sources)。

```bash
auto-research evolve \
  --model rankmixer \
  --dataset movielens-1m \
  --direction "加入 LONGER、UniMixer 和相关高效 Transformer 结构" \
  --workers 3 \
  --generations 3 \
  --population 4 \
  --steps 100 \
  --papers 8 \
  --benchmark-suite public \
  --fitness-metric public_composite \
  --seeds 42,43,44
```

调研方向同时约束论文检索和可执行结构空间；每一代并行比较论文启发结构与训练参数，再根据 validation 形成下一轮决策。目前包括 LONGER、UniMixer、WHALE、TMallGS、Long-History Transformer、RAMP 及组合结构；在线发现但尚未映射为安全算子的论文只进入证据池。

公共评测套件会在 MovieLens 上固定评估 overall、长历史、长尾目标、recent-only 和个性化特征受限切片；`public_composite` 用这些切片 NDCG 的等权平均晋级。若只想保持原先总体 NDCG 选择口径，使用 `--fitness-metric primary`；若要跳过额外切片，使用 `--benchmark-suite core`。

统一排序研究还可使用
`--benchmark-suite unirank --fitness-metric unirank_composite`，增加时间序
pointwise AUC/logloss；协议、官方五数据集和完整 runner 的边界见
[UniRank 公共评测接入](docs/unirank.md)。

运行产物位于 `runs/evolution/<model>-<timestamp>/`，包含机器可读 JSON、中文 Markdown 报告和可直接打开的 HTML 研究看板。详细协议见[模型自动进化文档](docs/model-evolution.md)。

LLM 结构、预训练数据和后训练方法的三轮自动研究示例：

```bash
auto-research evolve \
  --model micro-llm \
  --dataset wikitext-2 \
  --direction "调研高效 LLM 结构、训练数据配比和 SFT/NEFTune 后训练方法" \
  --generations 3 \
  --population 6 \
  --workers 1 \
  --steps 300 \
  --papers 8 \
  --benchmark-suite public \
  --fitness-metric public_composite \
  --seeds 42
```

默认 `micro-llm` 约 12M–16M 参数；WikiText-2、Tiny Shakespeare、Stanford Alpaca、官方 GSM8K 和 BPE tokenizer 自动下载/构建并缓存到 `data/`。第一轮只比较结构，第二轮只比较数据配方，第三轮比较 SFT、NEFTune、DynamicRubric 与 Off-Context GRPO。public suite 同时记录 Alpaca preference accuracy 和 GSM8K candidate Pass@1；详细定义见[模型自动进化文档](docs/model-evolution.md)。

Agent 与生成式推荐也使用同一多轮控制器。Agent 可组合 memory、planner、tool、critic、
可训练 policy 和 failure recovery；`genrec` 在 MovieLens-1M 真实保留 catalog 上组合
context、catalog head、reward 与 distillation，并强制全目录评估：

```bash
auto-research evolve --model agent --dataset evomem-mini \
  --direction "组合 Agent Lightning policy、跨 episode memory 与 Reflexion recovery" \
  --generations 3 --population 8 --seeds 42,43,44

auto-research evolve --model genrec --dataset movielens-1m \
  --direction "组合 Netflix/JD GenRec 与 OxygenREC-v2 的 context、reward 和蒸馏" \
  --generations 3 --population 8 --steps 100 --seeds 42,43,44
```

Agent 的论文机制回归与能力比较分层运行。L1 mini-suite 只验证机制；L2.1 在接口层隐藏
reference answer/plan/route，删除 guide，并用隔离 train/validation/test 比较规划、故障恢复和成本：

```bash
auto-research agent-capability \
  --methods long-context,react,reflexion,agent-g2,ahead,auso \
  --train-episodes 36 --episodes 60 --seeds 42,43,44
```

协议与固定三 seed 结果见
[Agent L2.1 隔离能力评测与自动进化](docs/agent-research/capability-benchmark.md)。

同一评测也可直接作为 Agent Evolve 的 validation/test 目标；多轮控制器搜索九个组件轴，
只用 validation 晋级，并在全部代际结束后运行隔离 test：

```bash
auto-research evolve --model agent --dataset toolroute-l2.1 \
  --direction "组合 memory、planner、tool、critic、policy、recovery、reflection、verifier 与 context compression" \
  --generations 3 --population 9 --workers 3 \
  --agent-episodes 60 --seeds 42,43,44
```

重点方法从单 seed 机制验证晋级到三 seed 正式证据时，使用可断点续跑的统一入口：

```bash
auto-research promote-evidence --dataset-dir data --seeds 42,43,44
```

默认覆盖 RankMixer、Switch Transformer、GRPO 和 Agent Lightning，输出逐 seed 成败、
均值、标准差与 95% 置信区间；少于三个成功 seed 时禁止稳定提升声明。详细协议见
[模型自动进化文档](docs/model-evolution.md#three-seed-evidence-promotion)。

## 运行 Topic research loop

LLM 示例：

```bash
auto-research run \
  --topic "efficient post-training and preference optimization" \
  --track llm \
  --trials 8 \
  --papers 8
```

推荐算法示例：

```bash
auto-research run \
  --topic "ranking loss and hard negative sampling" \
  --track recommendation \
  --trials 8 \
  --papers 8
```

通用运行产物位于 `runs/<timestamp>/report.md`、`result.json` 和 `events.jsonl`。内置低成本实验用于验证研究流水线和快速筛选假设，不等同于某篇论文的专用 adapter。

相同实验修订、数据目录、seed 和参数的已完成 trial 会复用 `.auto-research/cache/` 中的标量指标。使用 `--force-rerun` 可强制重跑。外部实验代码必须在配置中设置 `experiment_revision` 才会启用缓存，代码或数据协议变化后应更新该值。

## 接入外部真实实验

先生成配置：

```bash
auto-research init research.json --track recommendation
```

配置可指定实现命令、训练命令和搜索空间：

```json
{
  "topic": "new retrieval loss",
  "track": "recommendation",
  "max_papers": 10,
  "max_trials": 6,
  "implementation_command": ["codex", "exec", "Read AUTO_RESEARCH_MANIFEST and implement the selected hypothesis"],
  "proposal_command": ["python", "experiments/propose_next.py"],
  "experiment_command": ["python", "experiments/train.py"],
  "search_space": {
    "learning_rate": [0.0001, 0.0003],
    "architecture": ["baseline", "candidate"]
  },
  "metric_name": "validation_loss",
  "direction": "minimize",
  "experiment_revision": "retrieval-loss-v1",
  "timeout_seconds": 3600
}
```

论文清单通过 `AUTO_RESEARCH_MANIFEST` 传给实现命令，每轮参数通过 `AUTO_RESEARCH_PARAMS` 传给实验命令。实验命令最后一行必须输出指标 JSON，例如：

```json
{"validation_loss": 1.234}
```

如果配置 `proposal_command`，它会在每轮收到 `AUTO_RESEARCH_MANIFEST` 和 `AUTO_RESEARCH_HISTORY`，最后一行返回 `{"params": {...}}` 或 `{"stop": true}`。因此 agent 能依据前几轮成功、失败和缓存结果自适应选择下一组参数；未配置时继续使用确定性搜索空间。
