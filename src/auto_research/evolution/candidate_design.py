from __future__ import annotations

import json
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path

from .models import PaperInspiration
from .promotion import CandidatePluginSpec, CandidatePromotionPipeline


@dataclass(frozen=True)
class PaperCandidateSpec:
    """Auditable bridge from paper retrieval to executable evolution code."""

    candidate_id: str
    paper_id: str
    paper_url: str
    provider: str
    origin: str
    hypothesis: str
    operator: str | None
    implementation_status: str
    required_contracts: tuple[str, ...]
    forbidden_claim: str


def candidate_specs(
    papers: list[PaperInspiration], provider: str
) -> list[PaperCandidateSpec]:
    contracts = (
        "shape-compatible model/operator implementation",
        "same-data same-budget baseline ablation",
        "deterministic unit test and multi-seed evaluator",
        "parameter/FLOP/runtime accounting",
    )
    return [
        PaperCandidateSpec(
            candidate_id=f"{provider}-{paper.arxiv_id.replace('.', '-')}",
            paper_id=paper.arxiv_id,
            paper_url=paper.url,
            provider=provider,
            origin=paper.candidate_origin,
            hypothesis=paper.method,
            operator=paper.architecture,
            implementation_status=(
                "installed-and-executable" if paper.executable
                else "retrieved-design-only"
            ),
            required_contracts=contracts,
            forbidden_claim=(
                "A retrieved paper is inspiration only until generated code passes "
                "verification and explicit promotion approval."
            ),
        )
        for paper in papers
    ]


def write_candidate_specs(
    path: Path, papers: list[PaperInspiration], provider: str
) -> Path:
    payload = {
        "schema_version": 1,
        "provider": provider,
        "candidates": [asdict(spec) for spec in candidate_specs(papers, provider)],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return path


def generate_and_verify_candidates(
    command: tuple[str, ...], specs_path: Path, project_dir: Path, timeout: int
) -> list[dict]:
    """Run an explicit external generator, then stage and verify its output.

    The command receives the candidate-spec path as its last argument and must
    print either one CandidatePluginSpec object or a JSON list.  This function
    never promotes code; promotion remains a separate human-approved command.
    """

    completed = subprocess.run(
        [*command, str(specs_path)], cwd=project_dir, capture_output=True,
        text=True, timeout=timeout, check=True,
    )
    payload = json.loads(completed.stdout)
    entries = payload if isinstance(payload, list) else [payload]
    pipeline = CandidatePromotionPipeline(project_dir)
    records = []
    for entry in entries:
        entry = dict(entry)
        if entry.get("verification_command"):
            raise ValueError(
                "external generators cannot choose commands that execute generated code; "
                "automatic verification is syntax-only"
            )
        entry["paper_ids"] = tuple(entry.get("paper_ids", ()))
        entry["verification_command"] = ()
        spec = CandidatePluginSpec(**entry)
        directory = pipeline.stage(spec)
        verification = pipeline.verify(spec.candidate_id, timeout)
        records.append({
            "candidate_id": spec.candidate_id,
            "staged_at": str(directory.relative_to(project_dir)),
            "verification": verification,
            "promoted": False,
        })
    return records
