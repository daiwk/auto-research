"""Explicit public-MRQA entrypoint for the checkpoint-based KuaFu diagnostic."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[4]


def reproduce(dataset_dir: Path, seed: int = 42) -> dict:
    checkpoint = os.environ.get("AUTO_RESEARCH_KUAFU_CHECKPOINT")
    if not checkpoint:
        raise RuntimeError(
            "set AUTO_RESEARCH_KUAFU_CHECKPOINT to a local, public "
            "Qwen3-4B-Instruct-2507 checkpoint before running KuaFu"
        )
    data = Path(dataset_dir) / "mrqa"
    train, dev = data / "SQuAD-train.jsonl.gz", data / "SQuAD-dev.jsonl.gz"
    if not train.is_file() or not dev.is_file():
        raise FileNotFoundError(
            "download the official MRQA 2019 SQuAD train/dev archives to "
            f"{data}; no synthetic fallback is permitted"
        )
    with tempfile.TemporaryDirectory(prefix="kuafu-mrqa-") as temporary:
        output = Path(temporary) / "result.json"
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "kuafu_public_mrqa.py"),
             "--checkpoint", checkpoint, "--mrqa-train", str(train),
             "--mrqa-dev", str(dev), "--seed", str(seed), "--output", str(output)],
            check=True,
        )
        return json.loads(output.read_text(encoding="utf-8"))
