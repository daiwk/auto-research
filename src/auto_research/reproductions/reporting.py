from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any

from .base import ReproductionAdapter
from .schema import enrich_result


def write_reproduction_result(
    adapter: ReproductionAdapter,
    result: dict[str, Any],
    output_root: Path,
    run_id: str | None = None,
    seeds: tuple[int, ...] | None = None,
    dataset_dir: Path = Path("data"),
    budget: str = "paper-specific",
) -> Path:
    """Write one paper to its own immutable, timestamped artifact directory."""
    run_id = run_id or dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    run_dir = output_root / f"{adapter.paper.arxiv_id}-{adapter.key}" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    if "schema_version" not in result:
        result = enrich_result(
            adapter, result, seeds=seeds or adapter.default_seeds,
            dataset_dir=dataset_dir, budget=budget,
        )
    result = _with_fidelity_payload(adapter, result)
    (run_dir / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    report = run_dir / "report.md"
    report.write_text(
        _with_fidelity_banner(adapter, adapter.render(result), result), encoding="utf-8"
    )
    return report


def write_legacy_combined_report(
    entries: list[tuple[ReproductionAdapter, dict[str, Any]]], output: Path
) -> Path:
    """Compatibility writer for the old single-file --output option."""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.with_suffix(".json").write_text(
        json.dumps(
            [_with_fidelity_payload(adapter, result) for adapter, result in entries],
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    sections = ["# Paper Reproduction Report", ""]
    for adapter, result in entries:
        enriched = _with_fidelity_payload(adapter, result)
        rendered = _with_fidelity_banner(adapter, adapter.render(enriched), enriched)
        sections.append(rendered.removeprefix("# ").strip())
        sections.append("")
    output.write_text("\n".join(sections), encoding="utf-8")
    return output


def _with_fidelity_banner(
    adapter: ReproductionAdapter, rendered: str, result: dict[str, Any]
) -> str:
    omitted = ""
    if adapter.omitted_core_components:
        omitted = " Missing core: " + ", ".join(adapter.omitted_core_components) + "."
    banner = (
        f"> Reproduction fidelity: **{adapter.fidelity.label}**. "
        f"{adapter.fidelity.description}{omitted}"
    )
    protocol = result.get("evaluation_protocol", {})
    tier = protocol.get("tier_label", adapter.evaluation_tier.label)
    claim = protocol.get(
        "claim_policy", "legacy result; seed-level claim eligibility was not recorded"
    )
    evidence_banner = f"> Evaluation tier: **{tier}**. Claim policy: {claim}."
    lines = rendered.splitlines()
    insert_at = 1 if lines and lines[0].startswith("# ") else 0
    lines[insert_at:insert_at] = ["", banner, "", evidence_banner]
    return "\n".join(lines)


def _with_fidelity_payload(
    adapter: ReproductionAdapter, result: dict[str, Any]
) -> dict[str, Any]:
    enriched = dict(result)
    enriched["reproduction_fidelity"] = {
        "level": adapter.fidelity.value,
        "label": adapter.fidelity.label,
        "description": adapter.fidelity.description,
        "omitted_core_components": list(adapter.omitted_core_components),
    }
    return enriched
