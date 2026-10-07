"""Curated metadata stored by domain and stable paper key, never intake date."""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path


@lru_cache(maxsize=1)
def catalog_records() -> tuple[dict, ...]:
    from ..reproductions.registry import get_adapter, list_adapters
    from ..reproductions.manifest import PaperManifest

    records = []
    seen = set()
    registered = set()
    for path in sorted(Path(__file__).with_suffix("").glob("*/*.json")):
        row = json.loads(path.read_text(encoding="utf-8"))
        identity = (row["domain"], row["key"])
        if identity in seen or path.stem != row["key"] or path.parent.name != row["domain"]:
            raise ValueError(f"duplicate/misplaced paper catalog row: {path}")
        seen.add(identity)
        binding = row.get("adapter")
        if isinstance(binding, dict) and "spec_key" in binding:
            adapter = get_adapter(binding["spec_key"])
            registered.add(adapter.key)
            row.update(
                title=adapter.paper.title,
                paper_url=adapter.paper.url,
                published=adapter.paper.published,
                code=adapter.paper.code_url,
                topic=list(adapter.paper.topics),
                adapter=PaperManifest.from_adapter(adapter).to_dict(),
            )
            # Preserve the public manifest's stable serialization order too.
            order = (
                "domain",
                "key",
                "title",
                "paper_url",
                "detail_path",
                "topic",
                "first_author",
                "first_author_affiliation",
                "published",
                "code",
                "adapter",
            )
            row = {
                **{name: row[name] for name in order if name in row},
                **{name: value for name, value in row.items() if name not in order},
            }
        for field in ("title", "paper_url", "detail_path", "domain", "key"):
            if not row.get(field):
                raise ValueError(f"{path}: missing {field}")
        records.append(row)
    missing = {a.key for a in list_adapters()} - registered
    if missing:
        raise ValueError("adapters missing a domain catalog spec: " + ", ".join(sorted(missing)))
    return tuple(sorted(records, key=lambda row: (row["domain"], row["key"])))


def legacy_records(selections):
    """Read-only historical import compatibility; not used by generators."""
    index = {(row["domain"], row["key"]): row for row in catalog_records()}
    return tuple(
        {key: {**index[identity], **overrides}[key] for key in fields}
        for identity, overrides, fields in selections
    )
