"""Pinned offline author-code execution; never counts a registration as a run."""
from __future__ import annotations

import json
import math
import os
from pathlib import Path
import subprocess
import sys

from ..near.experiment import verify_provenance
from ..near.data import sha256_file

PINS = {"lewam": "22914305c15c5fab767ce4122a97b05338cd0bd0",
        "smolwam": "dde1e5bfe35c439499343c6d70e9cd32c96d0b36",
        "libero": "8f1084e3132a39270c3a13ebe37270a43ece2a01"}
SOURCE_IDS = {"lewam": "MinghaoFu/lewam", "smolwam": "iitimii/SmolWAM",
              "libero": "Lifelong-Robot-Learning/LIBERO"}


def _implementation_hashes(key: str) -> dict[str, str]:
    root = Path(__file__).resolve().parent.parent
    files = ("lewam/external.py", f"{key}/algorithm.py", f"{key}/training.py", f"{key}/worker.py")
    return {name: sha256_file(root / name) for name in files}


def _real_updates(metrics: dict) -> bool:
    updates, delta = metrics.get("nonzero_gradient_updates"), metrics.get("parameter_sample_delta_l2")
    return (type(updates) is int and updates > 0
            and type(delta) in {int, float} and math.isfinite(delta) and delta > 0)


def _finite(value) -> bool:
    return type(value) in {int, float} and math.isfinite(value)


def validate_training_evidence(key: str, metrics: dict, evidence: dict) -> None:
    """Require every defining loss/validation/update trace, including finite zeros."""
    if not isinstance(metrics, dict) or not isinstance(evidence, dict):
        raise ValueError("structured actual training evidence required")
    common = {"optimizer_updates", "nonzero_gradient_updates", "parameter_sample_delta_l2", "updated_parameter_tensors"}
    required = ({"train_batches", "validation_batches", "validation_action_loss", "train_action_loss",
                 "train_latent_loss", "train_sigreg_loss"} if key == "lewam" else
                {"teacher_layout_updates", "compact_layout_updates", "nonzero_parameter_updates",
                 "best_validation_action_l1", "real_teacher_target_rows", "teacher_vs_demo_action_l1",
                 "train_mean_action_l1", "train_mean_world_l1", "train_mean_kd_act_l1", "train_mean_kd_world_l1"})
    if not common.union(required).issubset(metrics) or not all(_finite(value) for value in metrics.values()):
        raise ValueError("complete finite defining training/validation metrics required")
    if not _real_updates(metrics):
        raise ValueError("trained candidate lacks actual update evidence")
    counters = common - {"parameter_sample_delta_l2"}
    counters |= ({"train_batches", "validation_batches"} if key == "lewam" else
                 {"teacher_layout_updates", "compact_layout_updates", "nonzero_parameter_updates", "real_teacher_target_rows"})
    if any(type(metrics[name]) is not int or metrics[name] < 1 for name in counters):
        raise ValueError("training evidence counters must be positive finite integers")
    rows = evidence.get("batches" if key == "lewam" else "losses", [])
    gradients = evidence.get("gradients", [])
    losses = ("loss", "act", "state", "reg") if key == "lewam" else ("total", "action_l1", "world_l1", "kd_act_l1", "kd_world_l1")
    if not isinstance(rows, list) or not isinstance(gradients, list) or not rows or not gradients:
        raise ValueError("actual training/validation and gradient traces required")
    for row in rows:
        if (not isinstance(row, dict) or type(row.get("training")) is not bool
                or not all(name in row and _finite(row[name]) for name in losses)
                or any(type(value) in {int, float} and not _finite(value) for value in row.values())):
            raise ValueError("complete finite defining training/validation loss traces required")
        if key == "smolwam" and row.get("tokens") not in {1764, 1008}:
            raise ValueError("actual native layout token count required")
    if not any(row["training"] for row in rows) or not any(not row["training"] for row in rows):
        raise ValueError("nonempty training and validation traces required")
    if key == "lewam":
        if not all(_finite(value) and value >= 0 for value in gradients):
            raise ValueError("finite gradient trace required")
        if (len(gradients) != metrics["optimizer_updates"]
                or sum(value > 0 for value in gradients) != metrics["nonzero_gradient_updates"]
                or sum(row["training"] for row in rows) != metrics["train_batches"]
                or sum(not row["training"] for row in rows) != metrics["validation_batches"]):
            raise ValueError("gradient trace and update metrics differ")
    else:
        for row in gradients:
            if (not isinstance(row, dict) or row.get("tokens") not in {1764, 1008}
                    or not all(name in row and _finite(row[name]) and row[name] >= 0
                               for name in ("norm", "parameter_sample_delta_l2"))):
                raise ValueError("finite native layout/gradient/parameter trace required")
        if ({row["tokens"] for row in rows if row["training"]} != {1764, 1008}
                or not any(not row["training"] and row["tokens"] == 1008 for row in rows)
                or {row["tokens"] for row in gradients if row["norm"] > 0 and row["parameter_sample_delta_l2"] > 0} != {1764, 1008}):
            raise ValueError("both layouts must have real finite updates and compact validation")
        if (len(gradients) != metrics["optimizer_updates"]
                or sum(row["norm"] > 0 for row in gradients) != metrics["nonzero_gradient_updates"]
                or sum(row["parameter_sample_delta_l2"] > 0 for row in gradients) != metrics["nonzero_parameter_updates"]
                or sum(row["tokens"] == 1764 for row in gradients) != metrics["teacher_layout_updates"]
                or sum(row["tokens"] == 1008 for row in gradients) != metrics["compact_layout_updates"]):
            raise ValueError("gradient trace and optimizer count differ")


def record_trained_candidate(root: Path, key: str, seed: int, files: tuple[str, ...],
                             dataset: dict, metrics: dict, evidence: dict | None = None) -> dict:
    """Bind real native training outputs; never label them as public releases."""
    if not _real_updates(metrics):
        raise ValueError("a trained candidate requires actual gradients and parameter updates")
    validate_training_evidence(key, metrics, evidence or {})
    manifest = {"kind": "local-trained-candidate", "paper": key, "seed": seed,
                "source_revision": PINS[key], "selection": "validation only",
                "dataset": dataset, "metrics": metrics, "training_evidence": evidence,
                "implementation_sha256": _implementation_hashes(key),
                "files": {name: sha256_file(root / name) for name in files}}
    path = root / "training-provenance.json"
    if path.exists():
        raise FileExistsError("immutable candidate provenance already exists")
    path.write_text(json.dumps(manifest, sort_keys=True, indent=2) + "\n")
    return manifest


def verify_trained_candidate(root: Path, key: str, seed: int, files: tuple[str, ...]) -> dict:
    manifest = json.loads((root / "training-provenance.json").read_text())
    if (manifest.get("kind") != "local-trained-candidate" or manifest.get("paper") != key
            or manifest.get("source_revision") != PINS[key] or manifest.get("seed") != seed
            or manifest.get("selection") != "validation only"):
        raise ValueError("trained candidate identity/seed/selection differs")
    metrics = manifest.get("metrics", {})
    if not _real_updates(metrics):
        raise ValueError("trained candidate lacks actual update evidence")
    validate_training_evidence(key, metrics, manifest.get("training_evidence") or {})
    if manifest.get("implementation_sha256") != _implementation_hashes(key):
        raise ValueError("trained candidate local implementation checksum differs")
    for name in files:
        if manifest.get("files", {}).get(name) != sha256_file(root / name):
            raise ValueError("trained candidate checksum differs")
    return manifest


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
