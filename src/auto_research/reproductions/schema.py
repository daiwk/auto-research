from __future__ import annotations

import math
import hashlib
import importlib.metadata
from functools import lru_cache
import platform
import statistics
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .base import ReproductionAdapter
from .manifest import PaperManifest


RESULT_SCHEMA_VERSION = 2


def _commit_sha() -> str | None:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], check=True, capture_output=True,
            text=True, timeout=2,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None


@lru_cache(maxsize=16)
def dataset_fingerprint(path: Path) -> str:
    """Cheap content-manifest fingerprint without reading multi-GB datasets."""
    digest = hashlib.sha256()
    if not path.exists():
        return "missing"
    files = sorted(item for item in path.rglob("*") if item.is_file())
    for item in files[:10_000]:
        stat = item.stat()
        digest.update(str(item.relative_to(path)).encode())
        digest.update(f":{stat.st_size}:{stat.st_mtime_ns}".encode())
    digest.update(f":files={len(files)}".encode())
    return digest.hexdigest()


def _package_versions() -> dict[str, str]:
    versions = {}
    for package in ("auto-research", "numpy", "torch", "transformers"):
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            continue
    return versions


def aggregate_seed_metrics(seed_results: list[dict[str, Any]]) -> dict[str, Any]:
    numeric: dict[str, list[float]] = {}
    for result in seed_results:
        for key, value in _flatten_metrics(result).items():
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                if key in {"seed", "schema_version"} or key.endswith(".seed"):
                    continue
                numeric.setdefault(key, []).append(float(value))
    aggregate: dict[str, Any] = {}
    for key, values in numeric.items():
        mean = statistics.fmean(values)
        std = statistics.stdev(values) if len(values) > 1 else 0.0
        ci95 = 1.96 * std / math.sqrt(len(values)) if len(values) > 1 else None
        aggregate[key] = {"mean": mean, "std": std, "ci95": ci95, "n": len(values)}
    return aggregate


def _flatten_metrics(payload: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    flattened = {}
    for key, value in payload.items():
        name = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            flattened.update(_flatten_metrics(value, name))
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            flattened[name] = value
    return flattened


def enrich_result(
    adapter: ReproductionAdapter,
    result: dict[str, Any],
    *,
    seeds: tuple[int, ...],
    dataset_dir: Path,
    budget: str,
    seed_results: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    enriched = dict(result)
    enriched["schema_version"] = RESULT_SCHEMA_VERSION
    enriched["manifest"] = PaperManifest.from_adapter(adapter).to_dict()
    enriched["provenance"] = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "code_commit": _commit_sha(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "dataset_dir": str(dataset_dir.resolve()),
        "dataset_fingerprint": dataset_fingerprint(dataset_dir),
        "packages": _package_versions(),
    }
    enriched["evaluation_protocol"] = {
        "tier": adapter.evaluation_tier.value,
        "tier_label": adapter.evaluation_tier.label,
        "seeds": list(seeds),
        "budget": budget,
        "formal_comparison": seed_results is not None and len(seed_results) >= 3,
        "claim_policy": (
            "formal multi-seed comparison" if seed_results is not None and len(seed_results) >= 3
            else "single/few-seed smoke result; do not claim a stable improvement"
        ),
    }
    if seed_results is not None:
        enriched["seed_results"] = seed_results
        enriched["aggregate_metrics"] = aggregate_seed_metrics(seed_results)
    return enriched
