from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import lru_cache
import importlib
import json
from pathlib import Path
import re
from typing import Any

from ..reproductions.base import ReproductionAdapter


DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass(frozen=True)
class PaperSpec:
    schema_version: int
    key: str
    arxiv_id: str
    title: str
    paper_url: str
    organization: str
    published: str
    upstream_code: str
    track: str
    topics: tuple[str, ...]
    local_code: str
    documentation: str
    fidelity: str
    evaluation_tier: str
    datasets: tuple[str, ...]
    baseline: str
    metrics: tuple[str, ...]
    mechanisms: tuple[str, ...]
    evolve_operators: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        for key in (
            "topics",
            "datasets",
            "metrics",
            "mechanisms",
            "evolve_operators",
        ):
            payload[key] = list(payload[key])
        return payload


@lru_cache(maxsize=4)
def _documentation_index(root: Path) -> tuple[Path, ...]:
    return tuple(sorted(root.glob("docs/**/README.md")))


def _documentation_path(root: Path, adapter: ReproductionAdapter) -> str:
    needle = f"{adapter.paper.arxiv_id}-{adapter.key}"
    documents = _documentation_index(root)
    candidates = [path for path in documents if path.parent.name == needle]
    if not candidates:
        candidates = [
            path for path in documents if path.parent.name.startswith(f"{adapter.paper.arxiv_id}-")
        ]
    return candidates[0].relative_to(root).as_posix() if candidates else ""


def adapter_directory(adapter: ReproductionAdapter, root: Path) -> Path:
    base = root / "src" / "auto_research" / "reproductions"
    conventional = base / adapter.key.replace("-", "_")
    if (conventional / "adapter.py").exists():
        return conventional
    matches = []
    key_pattern = re.compile(rf"\bkey\s*=\s*['\"]{re.escape(adapter.key)}['\"]")
    for path in base.glob("*/adapter.py"):
        module = importlib.import_module(f"auto_research.reproductions.{path.parent.name}.adapter")
        if getattr(
            getattr(module, "ADAPTER", None), "key", None
        ) == adapter.key or key_pattern.search(path.read_text(encoding="utf-8")):
            matches.append(path.parent)
    if len(matches) != 1:
        raise ValueError(
            f"expected one adapter.py declaring key {adapter.key!r}, found {len(matches)}"
        )
    return matches[0]


def _exact_date_from_document(root: Path, documentation: str) -> str:
    if not documentation:
        return ""
    text = (root / documentation).read_text(encoding="utf-8")
    match = re.search(r"(?:首次公开日期|发布日期|日期)\s*\|\s*(\d{4}-\d{2}-\d{2})", text)
    return match.group(1) if match else ""


def _field_from_document(root: Path, documentation: str, labels: tuple[str, ...]) -> str:
    if not documentation:
        return ""
    text = (root / documentation).read_text(encoding="utf-8")
    for label in labels:
        match = re.search(rf"\|\s*{re.escape(label)}\s*\|\s*(.*?)\s*\|", text)
        if match:
            return match.group(1).strip()
    return ""


def spec_from_adapter(adapter: ReproductionAdapter, root: Path) -> PaperSpec:
    module_path = adapter_directory(adapter, root).relative_to(root.resolve()).as_posix()
    paper = adapter.paper
    documentation = _documentation_path(root, adapter)
    published = paper.published or ""
    if not DATE_PATTERN.match(published):
        published = _exact_date_from_document(root, documentation)
    organization = paper.organization or _field_from_document(
        root,
        documentation,
        ("公司/机构", "机构/公司/学校", "机构"),
    )
    upstream_code = paper.code_url or _field_from_document(
        root,
        documentation,
        ("原文开源代码", "原作者开源代码"),
    )
    mechanism = tuple(adapter.omitted_core_components) or (paper.title,)
    return PaperSpec(
        schema_version=1,
        key=adapter.key,
        arxiv_id=paper.arxiv_id,
        title=paper.title,
        paper_url=paper.url,
        organization=organization or "not listed in paper",
        published=published,
        upstream_code=upstream_code or "not released / not found",
        track=paper.track,
        topics=paper.topics,
        local_code=module_path,
        documentation=documentation,
        fidelity=adapter.fidelity.value,
        evaluation_tier=adapter.evaluation_tier.value,
        datasets=adapter.datasets,
        baseline=adapter.baseline or "not declared",
        metrics=adapter.metrics,
        mechanisms=mechanism,
        evolve_operators=adapter.evolve_operators,
    )


def write_spec(spec: PaperSpec, path: Path) -> Path:
    """Write JSON-compatible YAML without adding a runtime YAML dependency."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(spec.to_dict(), ensure_ascii=False, indent=2) + "\n")
    return path


def load_spec(path: Path) -> PaperSpec:
    payload = json.loads(path.read_text(encoding="utf-8"))
    for key in ("topics", "datasets", "metrics", "mechanisms", "evolve_operators"):
        payload[key] = tuple(payload.get(key, ()))
    return PaperSpec(**payload)


def validate_spec(
    spec: PaperSpec,
    *,
    root: Path | None = None,
    adapter: ReproductionAdapter | None = None,
) -> list[str]:
    errors: list[str] = []
    required = {
        "key": spec.key,
        "arxiv_id": spec.arxiv_id,
        "title": spec.title,
        "paper_url": spec.paper_url,
        "organization": spec.organization,
        "published": spec.published,
        "upstream_code": spec.upstream_code,
        "track": spec.track,
        "local_code": spec.local_code,
        "documentation": spec.documentation,
        "baseline": spec.baseline,
    }
    errors.extend(f"{key} is required" for key, value in required.items() if not value)
    if spec.schema_version != 1:
        errors.append("schema_version must be 1")
    if spec.published and not DATE_PATTERN.match(spec.published):
        errors.append("published must be an exact YYYY-MM-DD date")
    if not spec.mechanisms:
        errors.append("at least one implemented mechanism is required")
    if not spec.metrics:
        errors.append("at least one metric is required")
    if root:
        for label, value in (
            ("local_code", spec.local_code),
            ("documentation", spec.documentation),
        ):
            if value and not (root / value).exists():
                errors.append(f"{label} does not exist: {value}")
    if adapter:
        expected = {
            "key": adapter.key,
            "arxiv_id": adapter.paper.arxiv_id,
            "title": adapter.paper.title,
            "paper_url": adapter.paper.url,
            "track": adapter.paper.track,
        }
        for key, value in expected.items():
            if getattr(spec, key) != value:
                errors.append(f"{key} differs from adapter registry")
    return errors
