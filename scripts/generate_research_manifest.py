#!/usr/bin/env python3
"""Synchronize the unified research manifest with registered paper adapters."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PATH = DOCS / "research-manifest.json"
sys.path.insert(0, str(ROOT / "src"))

from auto_research.reproductions.manifest import PaperManifest
from auto_research.reproductions.registry import list_adapters


POST_TRAINING_KEYS = {"dynamic-rubric", "off-context-grpo", "sis"}


def _detail_path(adapter) -> str:
    matches = sorted((DOCS / "reproductions").glob(
        f"{adapter.paper.arxiv_id}-{adapter.key}/README.md"
    ))
    if len(matches) != 1:
        raise ValueError(
            f"expected one detail page for {adapter.key}, found {len(matches)}"
        )
    return str(matches[0].relative_to(DOCS))


def synchronize(payload: dict) -> dict:
    existing = {
        (paper["domain"], paper["key"]): paper
        for paper in payload.get("papers", [])
    }
    adapters = list_adapters()
    adapter_keys = {adapter.key for adapter in adapters}
    papers = [
        paper for paper in payload.get("papers", [])
        if not isinstance(paper.get("adapter"), dict)
        or paper["key"] in adapter_keys
    ]
    positions = {
        (paper["domain"], paper["key"]): index
        for index, paper in enumerate(papers)
    }
    for adapter in adapters:
        domain = (
            "post-training" if adapter.key in POST_TRAINING_KEYS
            else "recommendation" if adapter.paper.track == "recommendation"
            else "foundation-models"
        )
        identity = (domain, adapter.key)
        previous = existing.get(identity, {})
        record = {
            "domain": domain,
            "key": adapter.key,
            "title": adapter.paper.title,
            "paper_url": adapter.paper.url,
            "detail_path": _detail_path(adapter),
            "topic": list(adapter.paper.topics),
            "first_author": previous.get("first_author"),
            "first_author_affiliation": (
                previous.get("first_author_affiliation")
                or adapter.paper.organization
            ),
            "published": adapter.paper.published,
            "code": adapter.paper.code_url,
            "adapter": PaperManifest.from_adapter(adapter).to_dict(),
        }
        if identity in positions:
            papers[positions[identity]] = record
        else:
            positions[identity] = len(papers)
            papers.append(record)
    return {
        "schema_version": 1,
        "description": (
            "Canonical metadata for all research domains; generated pages must not "
            "maintain paper tables."
        ),
        "papers": sorted(papers, key=lambda paper: (paper["domain"], paper["key"])),
    }


def main() -> None:
    payload = json.loads(PATH.read_text(encoding="utf-8"))
    PATH.write_text(
        json.dumps(synchronize(payload), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
