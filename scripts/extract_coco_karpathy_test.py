#!/usr/bin/env python3
"""Extract only the 5K COCO Karpathy test images needed by retrieval evaluation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import zipfile


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--annotations", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    payload = json.loads(args.annotations.read_text(encoding="utf-8"))
    rows = payload.get("images", payload)
    names = [
        str(Path(str(row.get("filepath", ""))) / str(row["filename"]))
        for row in rows
        if row.get("split") == "test"
    ]
    if len(names) != 5000 or len(set(names)) != 5000:
        raise ValueError("expected exactly 5,000 unique Karpathy test images")

    args.output.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.archive) as archive:
        available = set(archive.namelist())
        missing = sorted(set(names) - available)
        if missing:
            raise ValueError(f"COCO archive is missing {len(missing)} selected images")
        for name in names:
            archive.extract(name, args.output)
    print(f"extracted {len(names)} Karpathy test images to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
