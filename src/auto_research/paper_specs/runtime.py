"""Dependency-free runtime view of packaged, authoritative paper specs.

Reading a catalog never imports a model. Only invoking run/render resolves the
paper's binding module. Metadata inference from README/metrics is migration-only.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import importlib
from pathlib import Path
from typing import Any

from .schema import PaperSpec, load_spec, validate_spec
from ..reproductions.base import (
    EvaluationTier,
    OnlineABEvidence,
    PaperMetadata,
    ReproductionAdapter,
    ReproductionFidelity,
)

ROOT = Path(__file__).resolve().parents[1] / "reproductions"


@lru_cache(maxsize=1)
def spec_index() -> dict[str, PaperSpec]:
    result = {}
    for path in sorted(ROOT.glob("*/paper.yaml")):
        spec = load_spec(path)
        errors = validate_spec(spec)
        expected_module = f"auto_research.reproductions.{path.parent.name}.adapter"
        if spec.adapter_module != expected_module or not path.with_name("adapter.py").is_file():
            errors.append("adapter_module must match its packaged binding file")
        if errors:
            raise ValueError(f"invalid packaged spec {path}: {'; '.join(errors)}")
        if spec.key in result:
            raise ValueError(f"duplicate paper spec: {spec.key}")
        result[spec.key] = spec
    return result


@dataclass(frozen=True)
class LazyBinding:
    """Picklable binding, including under the spawn execution contract."""

    module: str
    attribute: str

    def __call__(self, *args, **kwargs):
        adapter = importlib.import_module(self.module).ADAPTER
        target = getattr(adapter, self.attribute)
        if isinstance(target, LazyBinding):
            raise RuntimeError(f"unresolved adapter binding: {self.module}.{self.attribute}")
        return target(*args, **kwargs)


def adapter_from_spec(key: str, *, run=None, render=None) -> ReproductionAdapter:
    spec = spec_index()[key]
    values: dict[str, Any] = dict(spec.execution or {})
    paper = dict(values.pop("paper"))
    paper.update(
        arxiv_id=spec.arxiv_id,
        title=spec.title,
        url=spec.paper_url,
        track=spec.track,
        topics=spec.topics,
    )
    paper["online_ab"] = tuple(OnlineABEvidence(**row) for row in paper.get("online_ab", ()))
    values["paper"] = PaperMetadata(**paper)
    values["paper"].validate_catalog_entry()
    values["fidelity"] = ReproductionFidelity(spec.fidelity)
    values["evaluation_tier"] = EvaluationTier(spec.evaluation_tier)
    for name in ("datasets", "baseline", "metrics", "evolve_operators"):
        values[name] = getattr(spec, name)
    for name in (
        "omitted_core_components",
        "datasets",
        "metrics",
        "evolve_operators",
        "default_seeds",
        "device_capabilities",
    ):
        values[name] = tuple(values.get(name, ()))
    # Packaged contracts already include the normalized values. Do not inspect
    # local docs or execute a training fixture to reconstruct runtime metadata.
    values["infer_device_capabilities"] = False
    return ReproductionAdapter(
        key=key,
        run=run or LazyBinding(spec.adapter_module, "run"),
        render=render or LazyBinding(spec.adapter_module, "render"),
        **values,
    )
