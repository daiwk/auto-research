"""Reconcile frozen review decisions with current, independently observed evidence.

Never edit review snapshots or infer implemented capability from acceptance,
catalog membership, a GPU receipt, or a seed count alone.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import json

from .papers import canonical_arxiv_id
from .gpu_validation import validate_gpu_receipt


def reconcile_review(register: dict, manifest: dict, root: Path) -> dict:
    by_id: dict[str, list[dict]] = {}
    for paper in manifest.get("papers", []):
        paper_id = canonical_arxiv_id(paper.get("paper_url", "").rstrip("/").rsplit("/", 1)[-1])
        if paper_id:
            by_id.setdefault(paper_id, []).append(paper)
    rows = []
    for reviewed in register.get("papers", []):
        paper_id = canonical_arxiv_id(reviewed["id"])
        entries = by_id.get(paper_id, [])
        observations = []
        for entry in entries:
            detail = root / "docs" / entry["detail_path"]
            # The manifest's string adapter denotes a standalone catalog entry;
            # only a dictionary is the registry's executable adapter contract.
            adapter = entry.get("adapter")
            receipt_path = entry.get("gpu_validation_artifact")
            receipt_valid = False
            if receipt_path:
                path = root / receipt_path
                if path.is_file():
                    try:
                        receipt = json.loads(path.read_text())
                        receipt_valid = (receipt.get("adapter_key") == entry["key"]
                                         and not validate_gpu_receipt(receipt))
                    except (ValueError, TypeError):
                        receipt_valid = False
            observations.append({
                "domain": entry["domain"], "key": entry["key"],
                "detail_path": entry["detail_path"], "document_exists": detail.is_file(),
                "registered_executable": isinstance(adapter, dict),
                "gpu_receipt": receipt_path, "gpu_receipt_valid": receipt_valid,
                "capability_claim_verified": False,
            })
        rows.append({
            "id": paper_id, "title": reviewed["title"],
            "review_decision": reviewed["status"],
            "frozen_implementation_status": reviewed.get("implementation_status"),
            "current_status": "catalogued" if observations else "not_catalogued",
            "observations": observations,
        })
    accepted = [row for row in rows if row["review_decision"] == "accepted"]
    return {
        "schema_version": 1,
        "review_window": register["requested_window"],
        "review_finalized_on": register["review_finalized_on"],
        "policy": "observed-catalog-and-evidence-not-capability-v1",
        "counts": dict(sorted(Counter(row["current_status"] for row in rows).items())),
        "accepted_counts": dict(sorted(Counter(row["current_status"] for row in accepted).items())),
        "review_snapshot_modified": False,
        "implementation_complete": False,
        "papers": rows,
    }


def render_reconciliation(payload: dict) -> str:
    counts = payload["accepted_counts"]
    lines = [
        "# 历史审查与当前实现状态", "",
        "本页由当前 manifest 与冻结审查登记自动对账。审查决定不随实现变化；",
        "目录登记、可执行注册、GPU 运行验证与能力比较是不同事实。", "",
        "| 已接受候选的当前状态 | 数量 |", "| --- | ---: |",
        f"| 已出现在目录 | {counts.get('catalogued', 0)} |",
        f"| 尚未出现在目录 | {counts.get('not_catalogued', 0)} |", "",
        "目录存在不等于论文完整实现，也不代表能力提升。GPU 回执只核验运行，",
        "不能替代公平 baseline、隔离 split、足够预算和结果审查。", "",
        "逐篇字段见 [机器可读对账](implementation-status.json)。",
        "当前审查水位以 [统一状态](../../paper-discovery-watermark.json) 为准；",
        "本页不复活已退休的全来源穷尽水位。", "",
        "重新生成：`python scripts/reconcile_discovery_implementation.py`。", "",
    ]
    return "\n".join(lines)
