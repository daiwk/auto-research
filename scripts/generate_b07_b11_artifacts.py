#!/usr/bin/env python3
"""Run and document the fixed historical implementation batches B07--B11."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auto_research.agent_research.models import AgentResearchConfig
from auto_research.agent_research.runner import AgentResearchRunner
from auto_research.historical_b07_b11 import PAPERS, HistoricalPaper
from auto_research.post_training.models import PostTrainingConfig
from auto_research.post_training.runner import PostTrainingRunner
from auto_research.reproductions.historical_b07 import reproduce


SEED = 42
POST_KEYS = {paper.key for paper in PAPERS if paper.domain == "post-training"}
AGENT_KEYS = {paper.key for paper in PAPERS if paper.domain == "agent-research"}


def _slug(paper: HistoricalPaper) -> str:
    return f"{paper.arxiv_id}-{paper.key}"


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _code_cell(paper: HistoricalPaper) -> str:
    if paper.code_url:
        return f"是：[{paper.code_url.rstrip('/').split('/')[-1]}]({paper.code_url})"
    return "否：截至 2026-08-24 未发现原作者公开代码"


def _mermaid(paper: HistoricalPaper) -> str:
    if paper.domain == "post-training":
        return (
            "flowchart LR\n  P[同一 candidate policy] --> R[on-policy rollout]\n"
            f"  R --> M[{paper.key} 核心目标]\n  T[奖励 / 教师 / rubric] --> M\n"
            "  M --> U[参数更新]\n  U --> R"
        )
    if paper.domain == "agent-research":
        return (
            "flowchart LR\n  O[任务与观察] --> P[规划 / 状态管理]\n"
            f"  P --> M[{paper.key} 核心机制]\n  M --> A[动作 / 工具]\n"
            "  A --> V[验证与反馈]\n  V --> P"
        )
    return (
        "flowchart LR\n  X[固定公开 mini-suite] --> B[recent-window 对照]\n"
        f"  X --> M[{paper.key} 核心机制]\n  B --> E[同样本评测]\n  M --> E"
    )


def _b07_readme(paper: HistoricalPaper, result: dict) -> str:
    base = result["baseline"]["accuracy"]
    baseline_name = result["baseline"]["name"]
    final = result["method"]["accuracy"]
    delta = result["relative"]["accuracy_points"]
    package = paper.key.replace("-", "_")
    return f"""# {paper.title}

> **复现级别：核心机制 mini-suite。** 本地只验证论文可独立实现的算法路径，不把小规模 NumPy 实验冒充原论文规模训练或线上结果。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv {paper.arxiv_id}](https://arxiv.org/abs/{paper.arxiv_id}) |
| 公司/机构 | {paper.organization} |
| 第一作者 | {paper.first_author} |
| 首次公开日期 | {paper.published}（arXiv v1） |
| 原文开源代码 | {_code_cell(paper)} |
| Adapter | `{paper.key}` |
| 本地复现代码 | [`src/auto_research/reproductions/{package}/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/{package}/) |

## 原始论文总结

### 背景与主要改动

{paper.summary}

```mermaid
{_mermaid(paper)}
```

### 核心公式

$$
{paper.formula}
$$

### 论文离线与线上效果

{paper.paper_result} 这是原文口径；若原文没有工业 A/B，本页不会把本地结果写成线上收益。

## 本地复现

> **本地对照口径**：基线为同样本 `{baseline_name}`，实验组为 `{paper.key}`；单 seed 变化为 `{delta:+.2f}%` 个百分点。

同一 seed、同一 64 条样本上，`{baseline_name}` baseline accuracy 为 `{base:.4f}`，`{paper.key}` 为 `{final:.4f}`，绝对变化 `{delta:+.2f}` 个百分点。单篇原始指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)，批次索引见 [`../../experiments/historical-b07-b11-seed42.json`](../../experiments/historical-b07-b11-seed42.json)。

```bash
auto-research reproduce --paper {paper.key} --seed 42
```

## 复现边界

本地使用固定长上下文/多模态/评测 mini-suite，未训练论文规模 checkpoint、未实现定制 CUDA kernel，也未复刻论文完整公开 benchmark。该实现用于确认核心数据流、公式和相对计算路径可执行。
"""


def _post_readme(paper: HistoricalPaper, payload: dict) -> str:
    base = payload["baseline"]["accuracy"]
    final = payload["final"]["accuracy"]
    return f"""# {paper.title}

> **复现级别：核心目标 candidate-policy mini-suite。** 本地真实执行该论文独有的 advantage、蒸馏或约束更新；不是论文大模型训练的数值复刻。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv {paper.arxiv_id}](https://arxiv.org/abs/{paper.arxiv_id}) |
| 公司 / 机构 | {paper.organization} |
| 第一作者 | {paper.first_author} |
| 首次公开日期 | {paper.published}（arXiv v1） |
| 原作者代码 | {_code_cell(paper)} |
| 本地 adapter / 方法 | `{paper.key}` |
| 本地复现代码 | `src/auto_research/post_training/historical_b08_b09.py` |

## 原始论文总结

### 背景与主要改动

{paper.summary}

```mermaid
{_mermaid(paper)}
```

### 核心公式

$$
{paper.formula}
$$

### 论文离线与线上效果

{paper.paper_result} 以上为原论文报告值；论文没有工业线上 A/B 时不作线上效果推断。

## 本地复现

同一 arithmetic-smoke candidate policy 运行 120 次更新：训练前 accuracy `{base:.4f}`，训练后 `{final:.4f}`，变化 `{final-base:+.4f}`。这是训练前后 smoke 结果，不表示相对其他 RL/OPD 算法的公平优势。单篇原始指标见 [`metrics/arithmetic-smoke-seed42.json`](metrics/arithmetic-smoke-seed42.json)，批次索引见 [`../../experiments/historical-b07-b11-seed42.json`](../../experiments/historical-b07-b11-seed42.json)。

```bash
auto-research post-train --algorithm {paper.key} --dataset arithmetic-smoke --steps 120 --seed 42 --no-network
```

## 复现边界

本地策略是可审计 candidate-policy，复现论文的核心 objective 和诊断量；未下载论文大模型 checkpoint，未声称复刻其完整数据、算力、多 seed 或 benchmark。运行产物默认写入 `runs/post-training/`，仓库只提交指标，不提交 checkpoint。另见 [`../../experiments/`](../../experiments/)。
"""


def _agent_readme(paper: HistoricalPaper, payload: dict, baseline: dict) -> str:
    metrics = payload["metrics"]
    bmetrics = baseline["metrics"]
    return f"""# {paper.title}

> **复现级别：核心 Agent 机制 mini-suite。** 本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv {paper.arxiv_id}](https://arxiv.org/abs/{paper.arxiv_id}) |
| 公司 / 机构 | {paper.organization} |
| 第一作者 | {paper.first_author} |
| 首次公开日期 | {paper.published}（arXiv v1） |
| 原作者代码 | {_code_cell(paper)} |
| 本地 adapter / 方法 | `{paper.key}` |
| 本地复现代码 | `src/auto_research/agent_research/historical_b10_b11.py` |

## 原始论文总结

### 背景与主要改动

{paper.summary}

```mermaid
{_mermaid(paper)}
```

### 核心公式

$$
{paper.formula}
$$

### 论文离线与线上效果

{paper.paper_result} 以上是原文结果，不将本地 mini-suite 推广成原论文 benchmark 或线上结论。

## 本地复现

在 planbench-mini 120 episodes 上，`{paper.key}` joint success 为 `{metrics['joint_success']:.4f}`、average cost `{metrics['average_cost']:.4f}`；long-context 对照分别为 `{bmetrics['joint_success']:.4f}` 与 `{bmetrics['average_cost']:.4f}`。正确率饱和时重点核验 trace、source 和论文专属诊断计数，而不虚构效果提升。单篇指标见 [`metrics/planbench-mini-seed42.json`](metrics/planbench-mini-seed42.json)，批次索引见 [`../../experiments/historical-b07-b11-seed42.json`](../../experiments/historical-b07-b11-seed42.json)。

```bash
auto-research agent-research --method {paper.key} --benchmark planbench-mini --episodes 120 --seed 42
```

## 复现边界

确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 `runs/agent-research/`，仓库只保存指标。另见 [`../../experiments/`](../../experiments/)。
"""


def main() -> None:
    tmp = Path("/tmp/auto-research-b07-b11-runs")
    summary: list[dict] = []
    baseline_agent, baseline_dir = AgentResearchRunner(AgentResearchConfig(
        method="long-context", benchmark="planbench-mini", episodes=120,
        memory_size=24, seed=SEED, output_dir=tmp / "agent",
    )).run()
    baseline_payload = json.loads((baseline_dir / "metrics.json").read_text(encoding="utf-8"))

    for paper in PAPERS:
        docs_domain = "reproductions" if paper.batch == "B07" else paper.domain
        detail = ROOT / "docs" / docs_domain / _slug(paper)
        if paper.batch == "B07":
            result = reproduce(paper.key, ROOT / "data", SEED)
            metric_path = detail / "metrics" / "public-seed42.json"
            _write_json(metric_path, result)
            readme = _b07_readme(paper, result)
            local = {"baseline": result["baseline"], "method": result["method"]}
        elif paper.key in POST_KEYS:
            result, run_dir = PostTrainingRunner(PostTrainingConfig(
                algorithm=paper.key, dataset="arithmetic-smoke", output_dir=tmp / "post",
                steps=120, maximum_examples=512, seed=SEED, allow_network=False,
            )).run()
            payload = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
            metric_path = detail / "metrics" / "arithmetic-smoke-seed42.json"
            _write_json(metric_path, payload)
            readme = _post_readme(paper, payload)
            local = {"baseline": payload["baseline"], "final": payload["final"]}
        elif paper.key in AGENT_KEYS:
            result, run_dir = AgentResearchRunner(AgentResearchConfig(
                method=paper.key, benchmark="planbench-mini", episodes=120,
                memory_size=24, seed=SEED, output_dir=tmp / "agent",
            )).run()
            payload = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
            metric_path = detail / "metrics" / "planbench-mini-seed42.json"
            _write_json(metric_path, payload)
            readme = _agent_readme(paper, payload, baseline_payload)
            local = {"baseline": baseline_agent.metrics, "method": result.metrics}
        else:
            raise AssertionError(paper)
        (detail / "README.md").write_text(readme, encoding="utf-8")
        summary.append({
            "batch": paper.batch, "domain": paper.domain, "key": paper.key,
            "arxiv_id": paper.arxiv_id, "seed": SEED,
            "metric_path": str(metric_path.relative_to(ROOT)), "local_result": local,
        })

    _write_json(ROOT / "docs/experiments/historical-b07-b11-seed42.json", {
        "description": "Navigation index only; each paper keeps its own raw metric artifact.",
        "seed": SEED, "papers": summary,
    })
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
