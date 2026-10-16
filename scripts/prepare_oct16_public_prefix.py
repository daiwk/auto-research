#!/usr/bin/env python3
"""Export only a bounded public KuaiRand-Pure prefix; never copies a workspace."""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--rows", type=int, default=4096)
    args = parser.parse_args()
    if args.output.exists() or not 100 <= args.rows <= 8192:
        raise ValueError("use a fresh output path and bounded 100..8192 row prefix")
    fields = ("user_id", "video_id", "time_ms", "duration_ms", "hourmin", "is_click", "long_view")
    with args.source.open() as stream:
        rows = [{key: row[key] for key in fields} for row in itertools.islice(csv.DictReader(stream), args.rows)]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({"source": "https://zenodo.org/records/10439422", "rows": len(rows),
                      "csv_sha256": hashlib.sha256(args.output.read_bytes()).hexdigest()}))


if __name__ == "__main__":
    main()
