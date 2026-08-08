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
