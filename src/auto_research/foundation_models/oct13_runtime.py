"""Explicit local-config execution for the four Oct-13 model paper scripts."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def check_checkpoint_identity(path: Path, public_id: str, revision: str) -> None:
    """Require prepared public-source identity; a CLI label alone is not proof."""
    provenance = path / "provenance.json"
    if not provenance.is_file():
        raise ValueError("prepared checkpoint provenance.json is required")
    values = json.loads(provenance.read_text())
    identity = values.get("public_id", values.get("id"))
    if identity != public_id or values.get("revision") != revision:
        raise ValueError("checkpoint provenance differs from the declared public ID/revision")


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
