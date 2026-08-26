from __future__ import annotations

import json
from pathlib import Path

from auto_research.experiment_store.dashboard import write_dashboard
from auto_research.experiment_store.store import ExperimentStore, sync_experiments


def _artifact(path: Path, method: str, score: float, latency: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "domain": "recommendation", "method": method, "dataset": "toy",
        "seed": 42, "metrics": {"ndcg": score, "latency": latency},
    }), encoding="utf-8")


def test_store_sync_is_idempotent_and_queryable(tmp_path):
    root = tmp_path / "runs"
    _artifact(root / "a" / "metrics.json", "baseline", 0.1, 2.0)
    _artifact(root / "b" / "result.json", "candidate", 0.2, 1.0)
    database = tmp_path / "experiments.sqlite"
    assert sync_experiments(database, [root]) == (2, 0)
    assert sync_experiments(database, [root]) == (2, 0)
    with ExperimentStore(database) as store:
        assert len(store.rows(domain="recommendation")) == 2
        assert {row.method for row in store.rows(metric="ndcg")} == {"baseline", "candidate"}
        assert [row.method for row in store.pareto_frontier("latency", "ndcg")] == ["candidate"]


def test_dashboard_embeds_filters_and_wrap_safe_table(tmp_path):
    root = tmp_path / "runs"
    _artifact(root / "long-method" / "metrics.json", "a-very-long-method", 0.2, 1.0)
    database = tmp_path / "experiments.sqlite"
    sync_experiments(database, [root])
    output = write_dashboard(database, tmp_path / "dashboard.html")
    text = output.read_text(encoding="utf-8")
    assert "统一实验看板" in text
    assert "a-very-long-method" in text
    assert "overflow-wrap:anywhere" in text
    assert "查看全部" in text


def test_metrics_directory_uses_paper_or_artifact_as_method(tmp_path):
    docs = tmp_path / "docs"
    nested = docs / "multimodal-models" / "metrics" / "clip-a30.json"
    nested.parent.mkdir(parents=True)
    nested.write_text(json.dumps({"metrics": {"accuracy": 0.8}}), encoding="utf-8")
    paper = docs / "reproductions" / "2601.00001-example" / "metrics" / "result.json"
    paper.parent.mkdir(parents=True)
    paper.write_text(json.dumps({"metrics": {"ndcg": 0.1}}), encoding="utf-8")

    database = tmp_path / "experiments.sqlite"
    sync_experiments(database, [docs])
    with ExperimentStore(database) as store:
        methods = {row.method for row in store.rows()}

    assert methods == {"clip-a30", "2601.00001-example"}
    assert "metrics" not in methods
