from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from .base import ReproductionAdapter


@dataclass(frozen=True)
class PaperManifest:
    """Canonical, serializable view consumed by CLI, reports and catalog generators.

    Adapter modules remain the authoring source for now; every other consumer should
    use this normalized view instead of maintaining another paper table.
    """

    adapter_key: str
    arxiv_id: str
    title: str
    paper_url: str
    track: str
    organization: str | None
    published: str | None
    code_url: str | None
    topics: tuple[str, ...]
    local_code_dir: str
    fidelity: str
    evaluation_tier: str
    datasets: tuple[str, ...]
    baseline: str | None
    metrics: tuple[str, ...]
    default_seeds: tuple[int, ...]
    budget: str
    device_capabilities: tuple[str, ...]
    online_evidence: tuple[dict[str, Any], ...]
    selection_exception: str | None
    evolve_operators: tuple[str, ...] = ()

    @classmethod
    def from_adapter(
        cls, adapter: ReproductionAdapter, evolve_operators: Iterable[str] = ()
    ) -> "PaperManifest":
        paper = adapter.paper
        module = adapter.render.__module__.split(".reproductions.", 1)[-1]
        package = module.split(".", 1)[0]
        evidence = []
        for item in paper.online_ab:
            normalized = item.to_dict()
            normalized.setdefault("source_url", paper.url)
            normalized.setdefault(
                "source_location",
                "original paper online-result disclosure: "
                f"product={item.product}; metric={item.metric}",
            )
            evidence.append(normalized)
        return cls(
            adapter_key=adapter.key,
            arxiv_id=paper.arxiv_id,
            title=paper.title,
            paper_url=paper.url,
            track=paper.track,
            organization=paper.organization,
            published=paper.published,
            code_url=paper.code_url,
            topics=paper.topics,
            local_code_dir=f"src/auto_research/reproductions/{package}",
            fidelity=adapter.fidelity.value,
            evaluation_tier=adapter.evaluation_tier.value,
            datasets=adapter.datasets,
            baseline=adapter.baseline,
            metrics=adapter.metrics,
            default_seeds=adapter.default_seeds,
            budget=adapter.budget,
            device_capabilities=adapter.device_capabilities,
            online_evidence=tuple(evidence),
            selection_exception=paper.selection_exception,
            evolve_operators=tuple(evolve_operators),
        )

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        for key in (
            "topics", "datasets", "metrics", "default_seeds",
            "device_capabilities", "online_evidence", "evolve_operators",
        ):
            payload[key] = list(payload[key])
        return payload


def manifests(adapters: Iterable[ReproductionAdapter]) -> tuple[PaperManifest, ...]:
    return tuple(PaperManifest.from_adapter(adapter) for adapter in adapters)


def write_manifest(path: Path, adapters: Iterable[ReproductionAdapter]) -> Path:
    import json

    payload = {
        "schema_version": 1,
        "papers": [item.to_dict() for item in manifests(adapters)],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path
