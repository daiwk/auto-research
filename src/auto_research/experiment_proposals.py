"""Turn installed/retrieved papers into auditable experiment proposals."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any

from .evolution.compatibility import (
    describe_operator, operator_registry, validate_operator_set,
)
from .paper_specs import PaperSpec, load_spec
from .protocols import get_protocol

SOURCE_KINDS = {
    "installed-paper-component", "retrieved-paper-component", "parameter-variant",
    "automatic-combination", "novel-hypothesis",
}


@dataclass(frozen=True)
class ExperimentProposal:
    proposal_id: str
    paper_key: str
    paper_title: str
    source_kind: str
    model: str
    protocol_id: str
    hypothesis: str
    operators: tuple[str, ...]
    core_mechanisms: tuple[str, ...]
    formula_notes: tuple[str, ...]
    differences_from_baseline: tuple[str, ...]
    baseline: str
    ablations: tuple[str, ...]
    search_space: dict[str, tuple[Any, ...]]
    execution_plan: tuple[str, ...]
    status: str = "awaiting-human-confirmation"
    executable: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        for key in ("operators", "core_mechanisms", "formula_notes",
                    "differences_from_baseline", "ablations", "execution_plan"):
            payload[key] = list(payload[key])
        payload["search_space"] = {key: list(value) for key, value in self.search_space.items()}
        return payload


def find_paper_spec(root: Path, key: str) -> PaperSpec:
    matches = [path for path in root.glob("src/auto_research/reproductions/*/paper.yaml")
               if load_spec(path).key == key]
    if len(matches) != 1:
        raise ValueError(f"expected one paper spec for {key!r}, found {len(matches)}")
    return load_spec(matches[0])


def propose_from_paper(spec: PaperSpec, *, model: str, protocol_id: str,
                       direction: str = "", source_kind: str = "installed-paper-component",
                       operators: tuple[str, ...] | None = None,
                       formula_notes: tuple[str, ...] = ()) -> ExperimentProposal:
    if source_kind not in SOURCE_KINDS:
        raise ValueError(f"unknown proposal source: {source_kind}")
    protocol = get_protocol(protocol_id)
    installed = tuple(
        key for key, operator_spec in operator_registry().items()
        if spec.arxiv_id in operator_spec.paper_ids
    )
    selected = tuple(
        operators if operators is not None else (spec.evolve_operators or installed)
    )
    errors = validate_operator_set(model, selected) if selected else []
    if errors:
        raise ValueError("; ".join(errors))
    executable = bool(selected) and all(describe_operator(value, model).paper_ids for value in selected)
    mechanisms = spec.mechanisms[:4]
    change = direction.strip() or ", ".join(mechanisms)
    return ExperimentProposal(
        proposal_id=f"{spec.key}-{model}-{protocol_id.replace('.', '-')}",
        paper_key=spec.key, paper_title=spec.title, source_kind=source_kind,
        model=model, protocol_id=protocol.protocol_id,
        hypothesis=f"在冻结的 {protocol.reference_baseline} 基线上加入 {change}，改善 {protocol.primary_metric}",
        operators=selected, core_mechanisms=mechanisms,
        formula_notes=formula_notes or ("未从声明文件提取公式；执行前查阅本地论文详情页",),
        differences_from_baseline=tuple(
            f"{protocol.reference_baseline} 不包含：{mechanism}" for mechanism in mechanisms
        ),
        baseline=protocol.reference_baseline,
        ablations=tuple(["baseline", *[f"remove:{value}" for value in selected]]),
        search_space={"learning_rate": (1e-4, 3e-4, 1e-3), "layers": (2, 4, 6),
                      "seed": protocol.seeds},
        execution_plan=(
            f"按 {protocol.protocol_id} 冻结数据、划分、候选集合与预算",
            "运行冻结基线和逐项消融，使用完全相同的 paired seeds",
            "运行组合候选并交给统计决策器输出 promote/continue/reject",
            "人工确认后才允许进入 candidate promotion",
        ),
        executable=executable,
    )


def write_proposal(proposal: ExperimentProposal, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(proposal.to_dict(), ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")
    return path
