"""Verify a public training-only holdout before claiming test isolation."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def validate_holdout(manifest, train_path, validation_path, *, dataset_revision):
    if manifest is None:
        return {"verified": False, "test_read": None,
                "reason": "No verified split manifest; test isolation not claimed"}
    record = json.loads(Path(manifest).read_text())
    if (record.get("source_split") != "train" or record.get("test_opened") is not False
            or record.get("source_revision") != dataset_revision):
        raise ValueError("training-only source and matching dataset revision required")
    hashes = {}
    questions = []
    for name, path in (("train", train_path), ("validation", validation_path)):
        content = Path(path).read_bytes()
        hashes[name] = hashlib.sha256(content).hexdigest()
        if record.get("partition_sha256", {}).get(name) != hashes[name]:
            raise ValueError(f"{name} holdout digest mismatch")
        rows = [json.loads(line) for line in content.splitlines() if line.strip()]
        if not rows or record.get("counts", {}).get(name) != len(rows):
            raise ValueError(f"{name} holdout count mismatch")
        keys = [" ".join(r["question"].split()) for r in rows]
        if len(set(keys)) != len(keys):
            raise ValueError("duplicate normalized questions")
        questions.append(set(keys))
    if questions[0] & questions[1]:
        raise ValueError("normalized train/validation overlap")
    return {"verified": True, "test_read": False, "source_id": record["source_id"],
            "source_revision": record["source_revision"], "source_sha256": record["source_sha256"],
            "partition_sha256": hashes, "partition": record["partition"]}
