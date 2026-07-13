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
    (run_dir / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    report = run_dir / "report.md"
    report.write_text(adapter.render(result), encoding="utf-8")
    return report


def write_legacy_combined_report(
    entries: list[tuple[ReproductionAdapter, dict[str, Any]]], output: Path
) -> Path:
    """Compatibility writer for the old single-file --output option."""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.with_suffix(".json").write_text(
        json.dumps([result for _, result in entries], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    sections = ["# Paper Reproduction Report", ""]
    for adapter, result in entries:
        rendered = adapter.render(result)
        sections.append(rendered.removeprefix("# ").strip())
        sections.append("")
    output.write_text("\n".join(sections), encoding="utf-8")
    return output
