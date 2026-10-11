#!/usr/bin/env python3
"""Download ONLY official Banking77 training data and prepare a held-out split."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

from auto_research.post_training.pivot_intent import banking_holdout

REVISION = "9d081458ff52e53cf7e848f414e6e9344e4e6696"
BASE = f"https://raw.githubusercontent.com/PolyAI-LDN/task-specific-datasets/{REVISION}/banking_data"


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--shots", type=int, default=5)
    a = p.parse_args()
    with urlopen(BASE + "/train.csv", timeout=60) as response:
        source = response.read().decode()
    with urlopen(BASE + "/categories.json", timeout=60) as response:
        labels = json.load(response)
    train, valid, partition = banking_holdout(source, labels, seed=a.seed, shots=a.shots)
    a.output_dir.mkdir(parents=True, exist_ok=True)
    hashes = {}
    for name, rows in (("train", train), ("validation", valid)):
        payload = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
        (a.output_dir / f"{name}.jsonl").write_text(payload)
        hashes[name] = hashlib.sha256(payload.encode()).hexdigest()
    record = {"source_id": "PolyAI-LDN/task-specific-datasets/banking77", "source_split": "train",
              "source_revision": REVISION, "source_sha256": partition["source_sha256"],
              "test_opened": False, "counts": {"train": len(train), "validation": len(valid)},
              "partition_sha256": hashes, "partition": partition}
    (a.output_dir / "split.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record))


if __name__ == "__main__":
    main()
