"""UxSID binding: real public-data training, no synthetic result fallback."""
from pathlib import Path
import json

from auto_research.paper_specs.runtime import adapter_from_spec
from .experiment import render, run_uxsid


def reproduce(dataset_dir: Path, seed: int):
    config = dataset_dir / "uxsid.json"
    parameters = json.loads(config.read_text()) if config.is_file() else {}
    allowed = {"device", "encoder_path", "encoder_id", "encoder_revision", "epochs", "batch_size",
               "dimension", "anchors", "codebook_size", "max_users", "max_history", "learning_rate"}
    if not isinstance(parameters, dict) or set(parameters) - allowed:
        raise ValueError("uxsid.json contains unsupported public experiment arguments")
    if parameters.get("encoder_path"):
        parameters["encoder_path"] = Path(parameters["encoder_path"])
    return run_uxsid(dataset_dir, seed, **parameters)


ADAPTER = adapter_from_spec("uxsid", run=reproduce, render=render)
