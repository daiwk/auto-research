from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any

from .base import ReproductionAdapter


def write_reproduction_result(
    adapter: ReproductionAdapter,
    result: dict[str, Any],
    output_root: Path,
    run_id: str | None = None,
) -> Path:
    """Write one paper to its own immutable, timestamped artifact directory."""
    run_id = run_id or dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    run_dir = output_root / f"{adapter.paper.arxiv_id}-{adapter.key}" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    result = _with_fidelity_payload(adapter, result)
    (run_dir / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    report = run_dir / "report.md"
    report.write_text(_with_fidelity_banner(adapter, adapter.render(result)), encoding="utf-8")
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
        rendered = _with_fidelity_banner(adapter, adapter.render(enriched))
        sections.append(rendered.removeprefix("# ").strip())
        sections.append("")
    output.write_text("\n".join(sections), encoding="utf-8")
    return output


def _with_fidelity_banner(adapter: ReproductionAdapter, rendered: str) -> str:
    omitted = ""
    if adapter.omitted_core_components:
        omitted = " Missing core: " + ", ".join(adapter.omitted_core_components) + "."
    banner = (
        f"> Reproduction fidelity: **{adapter.fidelity.label}**. "
        f"{adapter.fidelity.description}{omitted}"
    )
    lines = rendered.splitlines()
    insert_at = 1 if lines and lines[0].startswith("# ") else 0
    lines[insert_at:insert_at] = ["", banner]
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
