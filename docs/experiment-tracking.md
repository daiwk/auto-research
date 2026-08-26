# 统一实验数据库与看板

论文复现、Evolve、LLM 后训练、Agent 与多模态实验过去分别保存 JSON。本模块不改变这些可审计的原始产物，而是在其上建立一个可重建的 SQLite 索引，统一回答“某模型在某数据集、seed 和预算下得到什么指标”。数据库和 HTML 看板属于本地产物，默认位于 `runs/`，不会提交 checkpoint 或二进制数据库。

无需运行命令也可以查看[公开实验看板](public-experiment-dashboard.md)。公开版只汇总仓库中已经提交并接受审计的 `docs/` 指标；本地版还会额外包含 `runs/` 中尚未提交的实验，适合调试和比较迭代过程。

## 一键建立索引

```bash
auto-research experiments sync \
  --database runs/experiments.sqlite \
  --roots docs,runs

auto-research experiments dashboard \
  --database runs/experiments.sqlite \
  --roots docs,runs \
  --output runs/experiment-dashboard.html
```

`sync` 会幂等导入 `metrics.json`、`result.json`、`matrix.json` 及 `metrics/` 下的 JSON；同一路径重复运行只更新内容，不产生重复记录。`evolve` 完成后会自动把本轮 `result.json` 登记到输出目录上一级的 `experiments.sqlite`。

## 查询与 Pareto 前沿

```bash
auto-research experiments list --domain recommendation --dataset movielens-1m

auto-research experiments pareto \
  --x-metric latency_seconds_per_example \
  --y-metric ndcg_at_10
```

默认认为横轴越小越好、纵轴越大越好；可用 `--maximize-x` 或 `--minimize-y` 改变方向。HTML 看板支持领域和全文筛选；每个实验以卡片展示最多六项核心指标，其余指标按需展开，长方法名和指标名会自动换行。

## 数据契约

SQLite schema v1 包含：

- `experiments`：产物路径、内容哈希、领域、方法、数据集、seed、时间和原始 JSON；
- `metrics`：扁平化后的数值指标，保留完整点路径，例如 `validation.ndcg_at_10`；
- `metadata`：数据库 schema 版本。

原始 JSON 始终是真实来源；数据库可以删除后从 `docs/` 与 `runs/` 全量重建。
