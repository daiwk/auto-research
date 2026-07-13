# auto-research

一个面向 macOS 本地环境的机器学习研究闭环：输入 topic，检索最新论文，在公开数据集上实现和迭代实验，生成隔离的 JSON/Markdown 产物，并可通过 GitHub CLI 提交 Pull Request（GitLab 语境中的 MR）。

## 当前能力

项目包含两层互补能力：

1. **Topic research loop**：按 topic 检索 arXiv，运行可配置参数搜索，逐轮保存 checkpoint。
2. **Paper reproduction adapters**：每篇论文拥有独立模型、实验和报告代码，运行真实公开数据集对照实验。

支持两条研究轨道：

- `llm`：网络结构、预训练和后训练；内置 Tiny Shakespeare 低成本实验。
- `recommendation`：召回、粗排、精排、混排、loss、采样、训练与 serving；按论文优先使用 Amazon Beauty 5-core、MovieLens-1M 等同源公开数据，内部数据论文使用 MovieLens-100K proxy。

## 已实现的论文

| Track | Adapter | Paper / organization | Public dataset | Local headline |
|---|---|---|---|---:|
| LLM | `sis` | SIS · arXiv 2607.04728 | Tiny Shakespeare | importance-weight variance -6.62% |
| Recommendation | `mdcns` | MDCNS · arXiv 2605.19651 | Amazon Beauty 5-core（作者切分） | NDCG@10 +104.75% vs Uniform |
| Recommendation | `llatte` | LLaTTE · Meta · arXiv 2601.20083 | MovieLens 100K | NDCG@10 -3.57% |
| Recommendation | `self-evolving-rec` | Self-Evolving RecSys · Google · arXiv 2602.10226 | MovieLens 100K | NDCG@10 +7.13% |
| Recommendation | `memento` | Memento · Meta · arXiv 2605.24051 | MovieLens 100K | NDCG@10 +4.78% |
| Recommendation | `g2rec` | G2Rec · Meta · arXiv 2606.20554 | Amazon Beauty 5-core | NDCG@10 +0.72% |
| Recommendation | `cmsl` | CMSL · Meta · arXiv 2606.28533 | MovieLens 100K | NDCG@10 +0.95% |
| Recommendation | `cluster-goobs` | Cluster GOOBS · Meta · arXiv 2607.00448 | MovieLens-1M | NDCG@10 +0.98%、head share -1.81% |
| Recommendation | `plum` | PLUM · Google/YouTube · arXiv 2510.07784 | MovieLens-1M | NDCG@10 +24.62% |
| Recommendation | `onerec` | OneRec · Kuaishou · arXiv 2502.18965 | MovieLens-1M | NDCG@10 +28.78% |
| Recommendation | `longer` | LONGER · ByteDance/Douyin · arXiv 2505.04421 | MovieLens-100K | NDCG@10 +0.41% |
| Recommendation | `mixformer` | MixFormer · ByteDance/Douyin · arXiv 2602.14110 | MovieLens-100K | NDCG@10 +0.53% |

这里的 local headline 是本机公开数据结果，不是论文线上 A/B 数字。完整实验协议、生产 A/B 证据和负结果解释见[论文复现索引](docs/reproductions/README.md)。后续推荐论文必须通过[真实线上 A/B 硬门槛](docs/reproductions/industrial-online-ab-selection.md)；Google/Meta 时间窗筛选仍见[专项报告](docs/reproductions/2026-google-meta-online-ab-selection.md)。

## 代码结构

```text
src/auto_research/
├── cli.py                         # run / reproduce / publish 命令入口
├── runner.py                      # topic research loop 与逐轮 checkpoint
├── datasets.py                    # 公开数据下载和缓存
├── papers.py                      # arXiv 检索
└── reproductions/
    ├── base.py                    # adapter 稳定接口
    ├── registry.py                # 自动发现 */adapter.py
    ├── reporting.py               # 隔离的 JSON/Markdown 产物
    ├── rec_utils.py               # 推荐实验共享数据切分与指标
    └── <paper>/
        ├── adapter.py             # 论文元数据与注册
        ├── model.py               # 论文特有模型或算法
        ├── experiment.py          # baseline、调参、评估
        └── report.py              # 论文专用 Markdown 报告

docs/reproductions/<arxiv-id>-<adapter>/README.md
tests/reproductions/
```

新增论文不需要修改 CLI：registry 会自动发现带有 `adapter.py` 的论文目录。详细约定见[架构与扩展指南](docs/architecture.md)。

## 安装

要求 macOS/Linux 和 Python 3.11+。

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

Tiny Shakespeare、MovieLens-100K/1M、Amazon Beauty 5-core 和 MDCNS 作者 Beauty 切分会按 adapter 首次运行时下载到 `data/`，之后复用本地缓存。下载器只接入体量适合本地 Mac 的公开原始数据；生产内部数据不会伪造为“原数据复现”。

## 运行论文复现

列出的 key 会由 adapter registry 动态生成：

```bash
auto-research reproduce --help
```

运行单篇或全部论文：

```bash
auto-research reproduce --paper memento --seed 42
auto-research reproduce --paper self-evolving-rec --seed 42
auto-research reproduce --paper all --seed 42
```

每篇论文、每次运行写入独立且不可变的目录：

```text
runs/reproductions/<arxiv-id>-<adapter>/<timestamp>/
├── result.json   # 机器可读事实来源
└── report.md     # adapter 渲染的实验结论
```

`data/` 与 `runs/` 默认不进入 Git。经过复核的长期结论写入 `docs/reproductions/<arxiv-id>-<adapter>/README.md`。

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

通用运行产物位于 `runs/<timestamp>/report.md` 和 `result.json`。内置低成本实验用于验证研究流水线和快速筛选假设，不等同于某篇论文的专用 adapter。

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
  "experiment_command": ["python", "experiments/train.py"],
  "search_space": {
    "learning_rate": [0.0001, 0.0003],
    "architecture": ["baseline", "candidate"]
  },
  "metric_name": "validation_loss",
  "direction": "minimize",
  "timeout_seconds": 3600
}
```

论文清单通过 `AUTO_RESEARCH_MANIFEST` 传给实现命令，每轮参数通过 `AUTO_RESEARCH_PARAMS` 传给实验命令。实验命令最后一行必须输出指标 JSON，例如：

```json
{"validation_loss": 1.234}
```

## 提交 GitHub PR

```bash
brew install gh
gh auth login

auto-research publish runs/<timestamp>/report.md \
  --title "research: evaluate retrieval loss"
```

发布命令要求工作区没有无关修改；必要时从 `main`/`master` 创建 `agent/...` 分支，只暂存指定报告，提交、推送并创建 draft PR。增加 `--ready` 可创建非草稿 PR。

## 实验解释边界

- 论文新旧以 arXiv `submittedDate` 为准，并记录实际检索日期。
- 公开数据实验只复现可公开实现的核心机制；私有日志、生产基础设施和超大模型使用明确标注的代理。
- 论文披露的线上 A/B 与本机离线指标始终分开记录。
- 正向、负向和跨 seed 不稳定结果都会保留，参数只能根据 validation 选择。

## 测试

```bash
pytest
```

当前测试覆盖 adapter 自动发现、核心论文机制、运行产物隔离和通用 research loop。
