import json
import subprocess
import sys
from pathlib import Path


def test_latest_p0_p1_discovery_batch_is_closed():
    root = Path(__file__).resolve().parents[1]
    completed = subprocess.run(
        [sys.executable, str(root / "scripts/audit_paper_coverage.py"), "--strict"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert "closed" in completed.stdout


def test_global_discovery_batch_covers_declared_subtopics():
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "docs/paper-discovery-ledger.json").read_text(encoding="utf-8"))
    global_batches = [batch for batch in data["batches"] if batch.get("scope_kind") == "global"]
    assert global_batches, "the ledger must contain a cross-domain global audit"
    latest = global_batches[-1]
    required = {(item["track"], item["subtopic"]) for item in latest["required_subtopics"]}
    covered = {(item["track"], item["subtopic"]) for item in latest["candidates"]}
    assert required <= covered
