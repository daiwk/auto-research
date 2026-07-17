from __future__ import annotations

from pathlib import Path
import os
import subprocess


ROOT = Path(__file__).parents[1]
DEMOS = (
    ROOT / "demo.sh",
    ROOT / "demo-mac.sh",
    ROOT / "demo-linux-cpu.sh",
    ROOT / "demo-linux-gpu.sh",
    ROOT / "scripts" / "run-platform-demo.sh",
)


def test_platform_demo_scripts_are_executable_and_valid_bash():
    for script in DEMOS:
        assert script.exists()
        assert os.access(script, os.X_OK)
        subprocess.run(["bash", "-n", str(script)], check=True)


def test_shared_demo_covers_both_tracks_and_all_runtime_controls():
    text = (ROOT / "scripts" / "run-platform-demo.sh").read_text(encoding="utf-8")
    for required in (
        "linux-cpu", "linux-gpu", "micro-llm", "rankmixer",
        "--device", "--cpu-threads", "DEMO_PROFILE", "DEMO_TRACK",
        "TORCH_INDEX_URL", "runtime_summary",
    ):
        assert required in text


def test_auto_demo_dispatches_to_each_explicit_platform_script():
    text = (ROOT / "demo.sh").read_text(encoding="utf-8")
    assert "demo-mac.sh" in text
    assert "demo-linux-cpu.sh" in text
    assert "demo-linux-gpu.sh" in text
