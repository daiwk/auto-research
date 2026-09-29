"""CLI adapter for the CUDA-only bounded DCE/SRCL reproduction path."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[4]


def reproduce(dataset_dir: Path, seed: int = 42) -> dict:
    checkpoint = os.environ.get("AUTO_RESEARCH_RECURSIVE_OPSD_CHECKPOINT")
    if not checkpoint:
        raise RuntimeError(
            "set AUTO_RESEARCH_RECURSIVE_OPSD_CHECKPOINT to a local "
            "Qwen3-4B-Instruct-2507 checkpoint"
        )
    data = Path(dataset_dir) / "gsm8k"
    if not all((data / name).is_file() for name in ("train.jsonl", "test.jsonl")):
        raise FileNotFoundError(
            f"official GSM8K train/test JSONL files are required in {data}; "
            "no synthetic fallback is permitted"
        )
    with tempfile.TemporaryDirectory(prefix="recursive-opsd-") as temporary:
        output = Path(temporary) / "metrics.json"
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "recursive_opsd_public_math.py"),
             "--checkpoint", checkpoint, "--data-dir", str(dataset_dir),
             "--output", str(output), "--seed", str(seed),
             "--steps", "2", "--max-new-tokens", "192"],
            check=True,
        )
        return json.loads(output.read_text(encoding="utf-8"))
