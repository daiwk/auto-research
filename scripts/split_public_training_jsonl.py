#!/usr/bin/env python3
"""Deterministic train/validation holdout from public *training* source only."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def split_rows(rows, fraction=.1):
    if not 0 < fraction < 1:
        raise ValueError("holdout fraction must be in (0,1)")
    unique = {}
    for row in rows:
        question = " ".join(row["question"].split())
        if question in unique and unique[question]["answer"] != row["answer"]:
            raise ValueError("conflicting labels for duplicate question")
        unique[question] = row
    train, valid = [], []
    for question, row in unique.items():
        value = int(hashlib.sha256(question.encode()).hexdigest()[:16], 16) / 2**64
        (valid if value < fraction else train).append(row)
    if not train or not valid:
        raise ValueError("empty split")
    return train, valid


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source-train", type=Path, required=True)
    p.add_argument("--source-id", required=True)
    p.add_argument("--source-revision", required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    rows = [json.loads(line) for line in args.source_train.read_text().splitlines() if line.strip()]
    train, valid = split_rows(rows)
    args.output.mkdir(parents=True, exist_ok=True)
    for name, records in (("train", train), ("validation", valid)):
        (args.output / f"{name}.jsonl").write_text("".join(json.dumps(r) + "\n" for r in records))
    (args.output / "split.json").write_text(json.dumps({
        "source_id": args.source_id, "source_revision": args.source_revision,
        "source_sha256": hashlib.sha256(args.source_train.read_bytes()).hexdigest(),
        "source_split": "train", "test_opened": False,
        "partition": "normalized-question sha256 unsigned-prefix / 2^64 < 0.1 validation",
        "counts": {"train": len(train), "validation": len(valid)},
        "partition_sha256": {name: hashlib.sha256((args.output / f"{name}.jsonl").read_bytes()).hexdigest()
                             for name in ("train", "validation")},
    }, indent=2) + "\n")


if __name__ == "__main__":
    main()
