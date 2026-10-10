"""Persistent query progress, distinct from transport cache and human review."""

from __future__ import annotations

from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import os
import tempfile
import uuid


def atomic_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix=path.name, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def prepare_scan(client, queries, *, start_date, end_date, page_size, maximum_results,
                 recall_mode="submission-window"):
    """Reject stale query matrices/windows rather than silently skipping work."""
    if not getattr(client, "checkpoint_dir", None):
        return
    identity = dict(
        schema_version=2,
        recall_mode=recall_mode,
        queries=[asdict(query) for query in queries],
        start_date=str(start_date),
        end_date=str(end_date),
        page_size=page_size,
        maximum_results=maximum_results,
    )
    identity = json.loads(json.dumps(identity))
    path = client.checkpoint_dir / "scan.json"
    fingerprint = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
    if client.resume:
        if not path.is_file():
            raise ValueError("no discovery checkpoint to resume; start a new scan")
        saved = json.loads(path.read_text())
        if saved.get("fingerprint") != fingerprint:
            raise ValueError("discovery window/query matrix/budget changed; start a new scan")
        client.scan_id = saved["scan_id"]
    else:
        client.scan_id = uuid.uuid4().hex
    atomic_json(path, {"fingerprint": fingerprint, "identity": identity, "scan_id": client.scan_id})


def coverage_summary(reports: list[dict]) -> dict:
    complete = bool(reports) and all(row.get("coverage_complete") for row in reports)
    return {
        "coverage_complete": complete,
        "transport_complete": bool(reports)
        and all(row.get("transport_complete") for row in reports),
        "query_count": len(reports),
        "capped_queries": sum(row.get("state") == "capped" for row in reports),
        "failed_queries": sum(row.get("state") == "failed" for row in reports),
        "cache_fallback_pages": sum(row.get("cache_fallback_pages", 0) for row in reports),
        "queries": reports,
        "scope": "configured arXiv API query matrix only; candidate date/identifier-month filtering is separate",
        "review_complete": False,
        "watermark_eligible": False,
        "note": "API retrieval coverage does not certify full-text review or all-source coverage; no review watermark is advanced automatically",
    }
