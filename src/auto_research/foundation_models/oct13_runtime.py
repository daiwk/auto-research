"""Explicit local-config execution for the four Oct-13 model paper scripts."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from auto_research.oct12_public_sources import verify_offline_manifest


def check_checkpoint_identity(path: Path, public_id: str, revision: str) -> dict:
    """Verify exact model/tokenizer/processor bytes, not only a declared label."""
    return verify_offline_manifest(path, public_id, revision, "checkpoint")


def check_dataset_identity(path: Path, public_id: str, revision: str,
                           required_files: tuple[str, ...] = ()) -> dict:
    """Hash verification is an integrity check; data is not fed to a policy."""
    manifest = verify_offline_manifest(path, public_id, revision, "dataset")
    if not set(required_files) <= set(manifest["files"]):
        raise ValueError("offline dataset provenance must cover every consumed input file")
    return manifest


def execute(key: str, script: str, dataset_dir: Path, seed: int) -> dict:
    root = Path(__file__).resolve().parents[3]
    config_path = Path(dataset_dir) / f"{key}.json"
    if not config_path.is_file():
        raise FileNotFoundError(f"{key} requires an explicit local config at {config_path}; see the paper README")
    config = json.loads(config_path.read_text())
    if not isinstance(config, dict) or any(key in config for key in ("seed", "output")):
        raise ValueError("config must be a scalar CLI-argument map; seed/output are controlled by the runner")
    with tempfile.TemporaryDirectory(prefix=f"{key}-") as temporary:
        output = Path(temporary) / "result.json"
        command = [sys.executable, str(root / "scripts" / script), "--seed", str(seed), "--output", str(output)]
        for name, value in config.items():
            flag = "--" + name.replace("_", "-")
            if isinstance(value, bool):
                command.append(flag if value else "--no-" + name.replace("_", "-"))
            elif isinstance(value, (str, int, float)):
                command.extend([flag, str(value)])
            else:
                raise ValueError(f"unsupported non-scalar argument: {name}")
        environment = {**os.environ, "PYTHONPATH": str(root / "src")}
        subprocess.run(command, cwd=root, env=environment, check=True, timeout=7200)
        result = json.loads(output.read_text())
        if result.get("diagnostic_only") is not True or result.get("promotion_eligible") is not False:
            raise ValueError("small-scope scripts must preserve diagnostic evidence designation")
        return result
