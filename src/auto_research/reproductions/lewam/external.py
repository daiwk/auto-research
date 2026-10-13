"""Pinned offline author-code execution; never counts a registration as a run."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

from ..near.experiment import verify_provenance

PINS = {"lewam": "22914305c15c5fab767ce4122a97b05338cd0bd0",
        "smolwam": "dde1e5bfe35c439499343c6d70e9cd32c96d0b36",
        "libero": "8f1084e3132a39270c3a13ebe37270a43ece2a01"}
SOURCE_IDS = {"lewam": "MinghaoFu/lewam", "smolwam": "iitimii/SmolWAM",
              "libero": "Lifelong-Robot-Learning/LIBERO"}


def verify_source(root: Path, key: str):
    expected = PINS[key]
    if not (root / "LICENSE").is_file():
        raise ValueError("upstream license is required")
    if not (root / ".git").exists():
        # A verified offline code mirror need not transport .git. Every
        # runtime/config/asset file must be covered, not just a claimed SHA.
        required = tuple(sorted(path.relative_to(root).as_posix() for path in root.rglob("*")
            if path.is_file() and path.name != "provenance.json"
            and not any(part.startswith(".") or part == "__pycache__" or part.endswith(".egg-info")
                        for part in path.relative_to(root).parts)
            and not any(part in {"build", "dist"} for part in path.relative_to(root).parts)))
        verify_provenance(root, SOURCE_IDS[key], expected, required)
        return
    revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True,
                              text=True, capture_output=True).stdout.strip()
    if revision != expected:
        raise ValueError(f"{key} author-code revision must be {expected}")
    dirty = subprocess.run(["git", "diff", "--name-only", "HEAD"], cwd=root, check=True,
                           text=True, capture_output=True).stdout.strip()
    if dirty:
        raise ValueError("modified upstream source must not use the original source pin")


def execute(config: dict, seed: int, key: str) -> dict:
    source = Path(config["source_root"]).resolve()
    verify_source(source, key)
    phase = config.get("phase", "eval")
    if phase not in {"eval", "train"}:
        raise ValueError("only actual eval or train phases are supported")
    run_dir = Path(config["output_dir"]).resolve() / f"{key}-{phase}-seed-{seed}"
    run_dir.mkdir(parents=True, exist_ok=False)
    request = run_dir / "request.json"
    result_path = run_dir / "worker-result.json"
    request.write_text(json.dumps({**config, "seed": seed, "result_path": str(result_path)}))
    command = [config.get("python", sys.executable), "-m",
               f"auto_research.reproductions.{key}.worker", "--request", str(request)]
    env = {**os.environ, "HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1",
           "PYTHONPATH": str(Path(__file__).resolve().parents[3]) + os.pathsep + str(source),
           "MUJOCO_GL": config.get("mujoco_gl", "egl")}
    with (run_dir / "worker.log").open("w") as log:
        subprocess.run(command, cwd=source, env=env, stdout=log, stderr=subprocess.STDOUT,
                       check=True, timeout=config.get("timeout_seconds", 1800))
    result = json.loads(result_path.read_text())
    if result.get("executed") is not True or result.get("source_revision") != PINS[key]:
        raise ValueError("worker did not attest actual execution of the pinned author implementation")
    return result


__all__ = ["PINS", "execute", "verify_provenance", "verify_source"]
