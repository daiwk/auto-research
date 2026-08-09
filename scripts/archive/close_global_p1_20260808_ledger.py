#!/usr/bin/env python3
"""Close the 15 P1 rows after code, metrics and detail pages exist."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs/paper-discovery-ledger.json"
ROWS = {
    "2407.16357": ("twin-v2", "reproductions/2407.16357-twin-v2/README.md"),
    "2006.05639": ("sim", "reproductions/2006.05639-sim/README.md"),
    "2510.11056": ("crsd", "reproductions/2510.11056-crsd/README.md"),
    "2103.00020": ("clip", "reproductions/2103.00020-clip/README.md"),
    "2304.08485": ("llava", "reproductions/2304.08485-llava/README.md"),
    "2211.17192": ("speculative-decoding", "reproductions/2211.17192-speculative-decoding/README.md"),
    "2306.00978": ("awq", "reproductions/2306.00978-awq/README.md"),
    "2401.10774": ("medusa", "reproductions/2401.10774-medusa/README.md"),
    "2512.01374": ("minirl", "post-training/2512.01374-minirl/README.md"),
    "2605.12070": ("missing-old-logits", "post-training/2605.12070-missing-old-logits/README.md"),
    "2606.19236": ("stare", "post-training/2606.19236-stare/README.md"),
    "2511.14460": ("agent-r1", "agent-research/2511.14460-agent-r1/README.md"),
    "2303.17760": ("camel", "agent-research/2303.17760-camel/README.md"),
    "2305.16504": ("toolbench", "agent-research/2305.16504-toolbench/README.md"),
    "2311.12983": ("gaia", "agent-research/2311.12983-gaia/README.md"),
}

def main():
    data = json.loads(LEDGER.read_text())
    closed = set()
    for batch in data["batches"]:
        for row in batch.get("candidates", []):
            if row.get("id") in ROWS and row.get("priority") == "P1":
                key, doc = ROWS[row["id"]]
                row.update({"status": "implemented", "key": key, "doc": doc})
                row.pop("reason", None)
                closed.add(row["id"])
    missing = set(ROWS) - closed
    if missing:
        raise SystemExit(f"P1 ledger rows not found: {sorted(missing)}")
    LEDGER.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")

if __name__ == "__main__":
    main()
