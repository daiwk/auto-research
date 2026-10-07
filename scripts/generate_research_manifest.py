#!/usr/bin/env python3
"""Generate the research manifest from packaged domain/key paper specifications."""
from __future__ import annotations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from auto_research.paper_specs.catalog import catalog_records

PATH = ROOT / "docs/research-manifest.json"

def synchronize(payload: dict | None = None) -> dict:
    # Input is accepted for backwards compatibility, never used as hidden state.
    papers = catalog_records()
    for paper in papers:
        if not (ROOT / "docs" / paper["detail_path"]).is_file():
            raise ValueError(f"missing detail page: {paper['detail_path']}")
    return {
        "schema_version": 1,
        "description": "Canonical metadata for all research domains; generated pages must not maintain paper tables.",
        "papers": list(papers),
    }

def main() -> None:
    PATH.write_text(json.dumps(synchronize(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
