#!/usr/bin/env python3
"""Build the public, committed dashboard payload from audited docs metrics only."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auto_research.experiment_store.store import ExperimentStore, sync_experiments  # noqa: E402


OUTPUT = ROOT / "docs" / "assets" / "data" / "experiment-dashboard.json"


def _paper_metadata() -> dict[str, dict]:
    manifest = json.loads((ROOT / "docs" / "research-manifest.json").read_text(encoding="utf-8"))
    return {
        str(Path(paper["detail_path"]).parent): paper
        for paper in manifest["papers"]
    }


def _metadata_for(path: str, papers: dict[str, dict]) -> dict | None:
    relative = path.removeprefix("docs/")
    return next(
        (paper for prefix, paper in papers.items() if relative.startswith(f"{prefix}/")),
        None,
    )


def _public_domain(domain: str) -> str:
    return {
        "agent-research": "agent",
        "foundation-models": "foundation-model",
    }.get(domain, domain)


def build_payload() -> dict:
    papers = _paper_metadata()
    with tempfile.TemporaryDirectory() as directory:
        database = Path(directory) / "experiments.sqlite"
        imported, failed = sync_experiments(database, [ROOT / "docs"])
        if failed:
            raise RuntimeError(f"{failed} committed metric artifacts could not be indexed")
        with ExperimentStore(database) as store:
            rows = sorted(store.rows(), key=lambda row: (row.domain, row.method, row.path))
    experiments = []
    for row in rows:
        paper = _metadata_for(row.path, papers)
        experiments.append({
            "path": row.path,
            "domain": _public_domain(paper["domain"]) if paper else row.domain,
            "method": paper["key"] if paper else row.method,
            "title": paper["title"] if paper else "",
            "dataset": row.dataset,
            "seed": row.seed,
            "metrics": row.metrics,
        })
    experiments.sort(key=lambda item: (item["domain"], item["method"], item["path"]))
    return {
        "schema_version": 1,
        "source": "committed audited metrics under docs/",
        "experiments": experiments,
        "artifact_count": imported,
    }


def main() -> int:
    payload = build_payload()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {payload['artifact_count']} public experiments to {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
