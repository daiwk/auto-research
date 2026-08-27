#!/usr/bin/env python3
"""Build the public, committed dashboard payload from audited docs metrics only."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auto_research.experiment_store.store import ExperimentStore, sync_experiments  # noqa: E402


OUTPUT = ROOT / "docs" / "assets" / "data" / "experiment-dashboard.json"
AGENT_CAPABILITY_METRICS = ("answer_accuracy", "plan_success", "joint_success")
GENERIC_AGENT_DIAGNOSTICS = {
    "episodes", "memory_size", "actions", "reasoning_steps", "tool_evictions",
}


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


def _artifact_payload(path: str) -> dict[str, Any]:
    payload = json.loads((ROOT / path).read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def _protocol(payload: dict[str, Any]) -> dict[str, Any]:
    protocol = payload.get("evaluation_protocol")
    return protocol if isinstance(protocol, dict) else {}


def _seed(row_seed: str, payload: dict[str, Any], path: str) -> str:
    if row_seed:
        return row_seed
    seeds = _protocol(payload).get("seeds")
    if isinstance(seeds, list) and seeds:
        return ", ".join(str(seed) for seed in seeds)
    if seeds not in (None, "", []):
        return str(seeds)
    match = re.search(r"seed(?:s)?[-_]?([0-9][0-9_-]*)", Path(path).stem, re.I)
    return match.group(1).replace("_", ", ").replace("-", "–") if match else ""


def _agent_evidence(payload: dict[str, Any], metrics: dict[str, float]) -> dict[str, Any]:
    protocol = _protocol(payload)
    diagnostics = payload.get("diagnostics")
    diagnostics = diagnostics if isinstance(diagnostics, dict) else {}
    fidelity = str(diagnostics.get("fidelity", payload.get("fidelity", "")))
    tier = str(protocol.get("tier", payload.get("evaluation_tier", "")))
    formal = protocol.get("formal_comparison")
    diagnostic_only = (
        tier.startswith("l1_")
        or "deterministic" in fidelity.lower()
    )
    saturated = diagnostic_only and all(
        metrics.get(name) == 1.0 for name in AGENT_CAPABILITY_METRICS
    )
    mechanism_metrics = {
        key: float(value)
        for key, value in diagnostics.items()
        if (
            key not in GENERIC_AGENT_DIAGNOSTICS
            and not isinstance(value, bool)
            and isinstance(value, (int, float))
            and value != 0
        )
    }
    return {
        "tier": tier or "unclassified",
        "formal_comparison": formal,
        "claim_policy": str(protocol.get("claim_policy", "")),
        "diagnostic_only": diagnostic_only,
        "capability_metrics_saturated": saturated,
        "episodes": diagnostics.get("episodes"),
        "mechanism_metrics": mechanism_metrics,
    }


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
        payload = _artifact_payload(row.path)
        public_domain = _public_domain(paper["domain"]) if paper else row.domain
        benchmark = str(payload.get("benchmark", ""))
        item = {
            "path": row.path,
            "domain": public_domain,
            "method": paper["key"] if paper else row.method,
            "title": paper["title"] if paper else "",
            "dataset": row.dataset or benchmark,
            "seed": _seed(row.seed, payload, row.path),
            "metrics": row.metrics,
        }
        if public_domain == "agent":
            item["evidence"] = _agent_evidence(payload, row.metrics)
        experiments.append(item)
    experiments.sort(key=lambda item: (item["domain"], item["method"], item["path"]))
    return {
        "schema_version": 2,
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
