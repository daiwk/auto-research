# Unified experiment database and dashboard

<!-- source-sha256: 6dd848b3d927f2ab069bf63a59d2fe2072769a060089eaedc9854c717f012a2e -->

[简体中文](../experiment-tracking.md) · English

Paper reproduction, Evolve, LLM post-training, agent, and multimodal experiments previously stored their JSON results separately. This module leaves those auditable source artifacts unchanged. It builds a rebuildable SQLite index over them so you can ask which metrics a model achieved for a specific dataset, seed, and budget. The database and HTML dashboard are local artifacts under `runs/` by default. Neither checkpoints nor the binary database are committed.

You can browse the [public experiment dashboard](public-experiment-dashboard.md) without running any commands. It includes only committed, audited metrics from `docs/`. The local dashboard also includes uncommitted experiments in `runs/`, which is useful for debugging and comparing successive iterations.

## Build the index

```bash
auto-research experiments sync \
  --database runs/experiments.sqlite \
  --roots docs,runs

auto-research experiments dashboard \
  --database runs/experiments.sqlite \
  --roots docs,runs \
  --output runs/experiment-dashboard.html
```

`sync` idempotently imports `metrics.json`, `result.json`, `matrix.json`, and JSON files under `metrics/`. Re-running it for the same path updates the content without duplicating the record. When `evolve` finishes, it automatically registers that run's `result.json` in the `experiments.sqlite` database one level above its output directory.

## Query results and the Pareto frontier

```bash
auto-research experiments list --domain recommendation --dataset movielens-1m

auto-research experiments pareto \
  --x-metric latency_seconds_per_example \
  --y-metric ndcg_at_10
```

By default, lower values on the x-axis and higher values on the y-axis are preferred. Use `--maximize-x` or `--minimize-y` to reverse either direction. The HTML dashboard supports domain and full-text filters. Each experiment card shows up to six core metrics and lets you expand the rest on demand. Long method and metric names wrap automatically.

## Data contract

SQLite schema v1 contains:

- `experiments`: artifact path, content hash, domain, method, dataset, seed, time, and original JSON.
- `metrics`: flattened numeric metrics that retain their full dot-separated path, such as `validation.ndcg_at_10`.
- `metadata`: database schema version.

The original JSON remains the source of truth. You can delete the database and rebuild it entirely from `docs/` and `runs/`.
