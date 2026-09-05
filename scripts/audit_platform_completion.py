#!/usr/bin/env python3
"""Fail when a claimed P0/P1 platform migration regresses."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auto_research.reproductions.manifest import PaperManifest
from auto_research.reproductions.registry import list_adapters
from auto_research.reproductions.execution import BUDGETS

from migrate_metric_schema_v2 import metric_paths


GENERIC_BASELINES = {"baseline", "paper-specific matched baseline"}
GENERIC_METRICS = {"paper-specific primary metric"}


def audit() -> list[str]:
    errors: list[str] = []
    adapters = list_adapters()
    research_manifest = json.loads(
        (ROOT / "docs" / "research-manifest.json").read_text(encoding="utf-8")
    )
    identities = [
        (paper["domain"], paper["key"])
        for paper in research_manifest.get("papers", [])
    ]
    if len(identities) != len(set(identities)):
        errors.append("unified research manifest contains duplicate domain/key pairs")
    if len(identities) < 312:
        errors.append(f"unified research manifest regressed: {len(identities)} < 312")
    manifest_adapter_keys = {
        paper["key"] for paper in research_manifest.get("papers", [])
        if isinstance(paper.get("adapter"), dict)
    }
    missing_adapters = {adapter.key for adapter in adapters} - manifest_adapter_keys
    if missing_adapters:
        errors.append(f"unified research manifest misses adapters: {sorted(missing_adapters)}")
    for paper in research_manifest.get("papers", []):
        if paper["domain"] in {"post-training", "agent-research"}:
            if not paper.get("first_author") or not paper.get("first_author_affiliation"):
                errors.append(
                    f"{paper['domain']}/{paper['key']}: first-author metadata missing"
                )
    if len(adapters) < 186:
        errors.append(f"adapter count regressed: {len(adapters)} < 186")
    for adapter in adapters:
        manifest = PaperManifest.from_adapter(adapter)
        prefix = adapter.key
        if not manifest.datasets:
            errors.append(f"{prefix}: datasets missing")
        if not manifest.baseline or manifest.baseline in GENERIC_BASELINES:
            errors.append(f"{prefix}: precise baseline missing")
        if not manifest.metrics or set(manifest.metrics) & GENERIC_METRICS:
            errors.append(f"{prefix}: precise metrics missing")
        if not manifest.default_seeds:
            errors.append(f"{prefix}: seeds missing")
        if not manifest.budget:
            errors.append(f"{prefix}: budget missing")
        if not manifest.device_capabilities:
            errors.append(f"{prefix}: device capabilities missing")
        if manifest.requires_gpu_validation and not manifest.gpu_validation_artifact:
            errors.append(f"{prefix}: required GPU validation receipt missing")
        for index, evidence in enumerate(manifest.online_evidence):
            if not evidence.get("source_url") or not evidence.get("source_location"):
                errors.append(f"{prefix}: online evidence {index} is not traceable")
            if evidence.get("source_location") == "paper online-experiment section":
                errors.append(f"{prefix}: online evidence {index} uses a generic location")

    if BUDGETS["smoke"].timeout_seconds != 300:
        errors.append("smoke reproduction budget is not an enforceable five-minute limit")
    if BUDGETS["standard"].timeout_seconds != 3600:
        errors.append("standard reproduction budget is not an enforceable one-hour limit")

    facade_limits = {
        ROOT / "src/auto_research/agent_research/methods.py": 150,
        ROOT / "src/auto_research/post_training/algorithms.py": 150,
        ROOT / "src/auto_research/evolution/llm_model.py": 150,
    }
    for path, limit in facade_limits.items():
        lines = len(path.read_text(encoding="utf-8").splitlines())
        if lines > limit:
            errors.append(f"{path.relative_to(ROOT)} facade regressed to {lines} lines")

    paths = metric_paths()
    if len(paths) < 214:
        errors.append(f"historical metric inventory regressed: {len(paths)} < 214")
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        relative = path.relative_to(ROOT)
        if payload.get("schema_version") != 2:
            errors.append(f"{relative}: schema_version != 2")
        if not payload.get("manifest_ref"):
            errors.append(f"{relative}: manifest_ref missing")
        protocol = payload.get("evaluation_protocol") or {}
        seeds = protocol.get("seeds") or []
        if not seeds or not protocol.get("claim_policy"):
            errors.append(f"{relative}: incomplete evaluation protocol")
        # Three or more seeds are necessary for a formal comparison, but are
        # not sufficient: an L1 mechanism diagnostic can use multiple seeds
        # solely to check determinism/stability without measuring capability.
        if protocol.get("formal_comparison") and len(seeds) < 3:
            errors.append(f"{relative}: formal comparison requires at least three seeds")
        provenance = payload.get("provenance") or {}
        if not provenance.get("artifact_path") or not provenance.get("dataset_fingerprint"):
            errors.append(f"{relative}: incomplete provenance")
    return errors


def main() -> int:
    errors = audit()
    if errors:
        print("\n".join(errors))
        return 1
    print("platform completion audit passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
