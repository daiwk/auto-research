# auto-research

一个 local-first 的机器学习自动研究闭环：输入 topic，检索最新论文，在公开数据集上进行可复现实验，多轮搜索参数，并输出 Markdown 结论；确认结果后可提交 GitHub Pull Request（即 GitLab 语境中的 MR）。

当前支持两条可扩展研究轨道：

- `llm`：网络结构、预训练、后训练。内置 Tiny Shakespeare 字符 n-gram 低成本代理实验。
- `recommendation`：召回、粗排、精排、混排、loss、采样、训练与 serving。内置 MovieLens 100K 矩阵分解实验。

另外提供五个已落到代码的论文 adapter，而不是只展示论文摘要：

- SIS，arXiv `2607.04728`：实现论文 Algorithm 1 的 top-K envelope rejection sampling，并与 token-level importance sampling 对照。
- MDCNS，arXiv `2605.19651`：实现 Teacher–Peer–Self 多源打分、divergence re-ranking 和 consensus distillation，并与 Uniform、DNS 对照。
- CMSL，arXiv `2606.28533`：实现构造式多兴趣序列与线性注意力近似，并与单序列基线对照。
- G2Rec，arXiv `2606.20554`：实现 co-engagement graph、soft interest tokens 与 item-only 基线。
- Cluster GOOBS，arXiv `2607.00448`：实现 cluster-conditioned OOB 难负采样，并与随机 OOB 对照。

内置实验的目标是验证研究流水线和快速筛选想法，并不等同于复现某篇论文。严谨实验应通过自定义实验命令接入 PyTorch/JAX 项目。

## 流程

```text
topic
  → arXiv 按提交时间检索
  → 固化论文元数据和实验搜索空间
  → 下载/复用公开数据集
  → 多轮候选实验（单次失败不终止整个 run）
  → 每轮 checkpoint result.json + report.md
  → 人工确认
  → 独立分支、commit、push、draft PR
```

## 快速开始

要求 macOS/Linux 和 Python 3.11+。

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'

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
  --trials 8
```

结果位于 `runs/<timestamp>/report.md` 和 `result.json`。数据集缓存在 `data/`，二者默认不提交 Git。

## 复现已支持的论文方法

```bash
# 分别运行，或使用 --paper all
auto-research reproduce --paper sis
auto-research reproduce --paper mdcns
auto-research reproduce --paper cmsl
auto-research reproduce --paper g2rec
auto-research reproduce --paper cluster-goobs
```

SIS 使用 Tiny Shakespeare；四个推荐 adapter 使用 MovieLens 100K，并报告排序质量、随机种子波动及适用时的热门曝光占比。论文与实测结果索引见 [docs/reproductions/README.md](docs/reproductions/README.md)，本轮 Google/Meta 严格筛选清单见 [selection report](docs/reproductions/2026-07-meta-online-ab-selection.md)，新增论文的开发约定见 [docs/architecture.md](docs/architecture.md)。

运行产物不再堆到同一个文件，而是写入 `runs/reproductions/<arxiv-id>-<adapter>/<timestamp>/`，每次运行包含独立的 `report.md` 与 `result.json`。

这是保留论文核心算法的 Mac-scale mechanism reproduction，不声称复现论文中 Qwen 大模型或六数据集的 headline number；报告会明确记录这个范围。

## 自定义真实实验

先生成配置：

```bash
auto-research init research.json --track llm
```

在 JSON 中增加：

```json
{
  "topic": "new attention architecture",
  "track": "llm",
  "max_papers": 10,
  "max_trials": 6,
  "implementation_command": ["codex", "exec", "Read AUTO_RESEARCH_MANIFEST and implement the selected hypothesis in experiments/train.py"],
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

每轮参数通过环境变量 `AUTO_RESEARCH_PARAMS` 传给命令。命令最后一行必须输出 JSON，例如：

```json
{"validation_loss": 1.234}
```

这种接口允许复用任意训练框架，同时只有用户在配置中明确批准的命令会执行。建议在训练脚本中固定数据切分与随机种子，并记录模型版本、数据版本、硬件和峰值内存。

可选的 `implementation_command` 会在实验前执行一次，并通过 `AUTO_RESEARCH_MANIFEST` 获得 topic、track 与最新论文的标题、摘要、链接和日期。它适合接入你选定的 coding agent 来生成或修改实验 adapter。因为这一步会改代码且论文复现通常需要工程判断，所以默认关闭；建议在独立分支或容器中运行并审查 diff。

## 发布报告

需要安装并登录 GitHub CLI：

```bash
brew install gh
gh auth login
auto-research publish runs/<timestamp>/report.md \
  --title "research: evaluate efficient post-training"
```

发布命令只会在工作区没有其他未提交修改时继续；从 `main` 自动创建 `agent/...` 分支，精确暂存报告、提交、推送并创建 draft PR。使用 `--ready` 可创建非草稿 PR。

## 设计边界与扩展点

- 论文“最新”以 arXiv `submittedDate` 为准，报告记录实际检索日期和论文日期。
- 搜索空间目前采用有种子的随机排列，确保轻量、确定且零额外依赖；后续可接入 Optuna/贝叶斯优化。
- 真实论文实现不是可靠的全自动步骤。建议将论文假设转成受审查的 experiment adapter，再交给此工具重复执行。
- 新轨道可在 `TRACK_CATEGORIES`、`DEFAULT_SPACES` 和 `builtin_experiment` 中注册；报告和发布层无需改动。

## 测试

```bash
pytest
```
