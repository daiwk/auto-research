from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time
from typing import Any


SMOLVLA_MODEL_ID = "lerobot/smolvla_base"
SMOLVLA_DATASET_ID = "lerobot/svla_so100_pickplace"
SMOLVLM_MODEL_ID = "HuggingFaceTB/SmolVLM2-500M-Video-Instruct"
SMOLVLA_MODEL_REVISION = "c83c3163b8ca9b7e67c509fffd9121e66cb96205"
SMOLVLA_DATASET_REVISION = "728583b5eaf9e739a7f119e2def466fa1d552402"
SMOLVLM_MODEL_REVISION = "7b375e1b73b11138ff12fe22c8f2822d8fe03467"
LEROBOT_REVISION = "713a409faedd73bb5597481b8885f17fbee23330"


@dataclass(frozen=True)
class EmbodiedPostTrainingConfig:
    output_dir: Path
    model_id: str = SMOLVLA_MODEL_ID
    model_revision: str = SMOLVLA_MODEL_REVISION
    dataset_id: str = SMOLVLA_DATASET_ID
    dataset_revision: str = SMOLVLA_DATASET_REVISION
    checkpoint_path: Path | None = None
    vlm_checkpoint_path: Path | None = None
    dataset_root: Path | None = None
    steps: int = 1
    batch_size: int = 1
    rename_map: str = (
        '{"observation.images.top":"observation.images.camera1",'
        '"observation.images.wrist":"observation.images.camera2"}'
    )
    empty_cameras: int = 1
    device: str = "cuda"
    offline: bool = False
    dry_run: bool = False
    executable: str = "lerobot-train"

    def validate(self) -> None:
        if self.steps < 1 or self.batch_size < 1 or self.empty_cameras < 0:
            raise ValueError("steps/batch-size must be positive and empty-cameras non-negative")
        json.loads(self.rename_map)
        if (
            self.offline and not self.dry_run
            and (
                self.dataset_root is None
                or self.checkpoint_path is None
                or self.vlm_checkpoint_path is None
            )
        ):
            raise ValueError(
                "offline embodied training requires --checkpoint-path, "
                "--vlm-checkpoint-path and --dataset-root"
            )


def build_lerobot_command(config: EmbodiedPostTrainingConfig) -> list[str]:
    config.validate()
    trainer_output = _available_trainer_output(config.output_dir)
    command = [
        config.executable,
        f"--policy.path={config.checkpoint_path or config.model_id}",
        f"--policy.vlm_model_name={config.vlm_checkpoint_path or SMOLVLM_MODEL_ID}",
        f"--dataset.repo_id={config.dataset_id}",
        f"--batch_size={config.batch_size}",
        f"--steps={config.steps}",
        f"--output_dir={trainer_output}",
        f"--job_name=auto-research-smolvla-{config.steps}step",
        f"--policy.device={config.device}",
        f"--policy.empty_cameras={config.empty_cameras}",
        f"--rename_map={config.rename_map}",
        "--policy.push_to_hub=false",
        "--wandb.enable=false",
        "--log_freq=1",
        f"--save_freq={config.steps}",
    ]
    if config.dataset_root is not None:
        command.append(f"--dataset.root={config.dataset_root.resolve()}")
    return command


def audit_dataset(root: Path) -> dict[str, Any]:
    root = root.resolve()
    if not root.exists():
        raise FileNotFoundError(root)
    files = sorted(path for path in root.rglob("*") if path.is_file())
    digest = hashlib.sha256()
    total_bytes = 0
    for path in files:
        stat = path.stat()
        digest.update(
            f"{path.relative_to(root).as_posix()}\0{stat.st_size}\n".encode()
        )
        total_bytes += stat.st_size
    metadata: dict[str, Any] = {}
    for name in ("meta/info.json", "meta/stats.json"):
        path = root / name
        if path.exists():
            metadata[name] = json.loads(path.read_text(encoding="utf-8"))
    return {
        "root": str(root),
        "files": len(files),
        "bytes": total_bytes,
        "manifest_sha256": digest.hexdigest(),
        "metadata": metadata,
    }


def run_embodied_post_training(
    config: EmbodiedPostTrainingConfig,
) -> tuple[dict[str, Any], Path]:
    config.validate()
    config.output_dir.mkdir(parents=True, exist_ok=True)
    command: list[str] = []
    dataset: dict[str, Any] = {
        "repo_id": config.dataset_id,
        "revision": config.dataset_revision,
        "local_audit": False,
    }
    started = time.monotonic()
    completed = None
    error: dict[str, str] | None = None
    try:
        if not config.dry_run and not config.offline:
            from huggingface_hub import snapshot_download
            config = replace(
                config,
                checkpoint_path=Path(snapshot_download(
                    config.model_id, revision=config.model_revision,
                )),
                vlm_checkpoint_path=Path(snapshot_download(
                    SMOLVLM_MODEL_ID,
                    revision=SMOLVLM_MODEL_REVISION,
                    allow_patterns=("*.json", "*.safetensors", "*.model", "*.txt"),
                )),
                dataset_root=Path(snapshot_download(
                    config.dataset_id, repo_type="dataset",
                    revision=config.dataset_revision,
                )),
            )
        command_config = config
        if not config.dry_run and config.checkpoint_path and config.vlm_checkpoint_path:
            command_config = replace(
                config,
                checkpoint_path=_prepare_policy_view(
                    config.checkpoint_path,
                    config.output_dir / "runtime-policy",
                    config.vlm_checkpoint_path,
                ),
            )
        command = build_lerobot_command(command_config)
        if config.dataset_root:
            dataset = audit_dataset(config.dataset_root)
        if config.dry_run:
            status = "planned"
        else:
            executable = shutil.which(config.executable)
            if executable is None:
                raise RuntimeError(
                    f"{config.executable} is not installed; install LeRobot or use "
                    "--dry-run to audit the invocation"
                )
            command[0] = executable
            environment = None
            if config.offline:
                environment = {
                    **os.environ,
                    "HF_HUB_OFFLINE": "1",
                    "TRANSFORMERS_OFFLINE": "1",
                    "HF_DATASETS_OFFLINE": "1",
                }
            completed = subprocess.run(
                command, text=True, capture_output=True, check=False, env=environment,
            )
            status = "completed" if completed.returncode == 0 else "failed"
    except Exception as exc:  # Persist materialization failures for auditability.
        status = "failed"
        error = {"type": type(exc).__name__, "message": str(exc)}
    combined_log = (
        (completed.stdout if completed else "")
        + "\n"
        + (completed.stderr if completed else "")
    )
    payload = {
        "schema_version": 2,
        "task": "mm-003-smolvla-post-training",
        "status": status,
        "config": {
            **asdict(config),
            "output_dir": str(config.output_dir),
            "dataset_root": str(config.dataset_root) if config.dataset_root else None,
            "checkpoint_path": str(config.checkpoint_path) if config.checkpoint_path else None,
            "vlm_checkpoint_path": (
                str(config.vlm_checkpoint_path) if config.vlm_checkpoint_path else None
            ),
        },
        "provenance": {
            "model_id": config.model_id,
            "model_revision": config.model_revision,
            "vlm_model_id": SMOLVLM_MODEL_ID,
            "vlm_model_revision": SMOLVLM_MODEL_REVISION,
            "dataset_id": config.dataset_id,
            "dataset_revision": config.dataset_revision,
            "lerobot_revision": LEROBOT_REVISION,
            "lerobot_package_version": _package_version("lerobot"),
            "dataset": dataset,
        },
        "execution": {
            "argv": command,
            "return_code": completed.returncode if completed else None,
            "duration_seconds": time.monotonic() - started,
            "stdout_tail": completed.stdout[-4000:] if completed else "",
            "stderr_tail": completed.stderr[-4000:] if completed else "",
            "error": error,
        },
        "metrics": _parse_training_metrics(combined_log),
        "claim_boundary": (
            "training invocation and public-dataset provenance only; success-rate requires "
            "a matching robot or simulator evaluation and is never inferred from train loss"
        ),
    }
    path = config.output_dir / "metrics.json"
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return payload, path


def _package_version(name: str) -> str | None:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def _prepare_policy_view(source: Path, destination: Path, vlm_path: Path) -> Path:
    """Create a lightweight local view with the tokenizer dependency pinned."""
    source = source.resolve()
    if not source.is_dir():
        raise FileNotFoundError(source)
    destination.mkdir(parents=True, exist_ok=True)
    for path in source.iterdir():
        if path.name == ".cache":
            continue
        target = destination / path.name
        if path.name != "policy_preprocessor.json":
            if target.is_symlink() or target.exists():
                target.unlink()
            target.symlink_to(path.resolve(), target_is_directory=path.is_dir())
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        for step in payload.get("steps", []):
            if step.get("registry_name") == "tokenizer_processor":
                step.setdefault("config", {})["tokenizer_name"] = str(vlm_path.resolve())
        target.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    return destination.resolve()


def _available_trainer_output(output_dir: Path) -> Path:
    candidate = output_dir / "trainer"
    suffix = 2
    while candidate.exists():
        candidate = output_dir / f"trainer-{suffix}"
        suffix += 1
    return candidate


def _parse_training_metrics(log: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    parameter_match = re.search(
        r"num_learnable_params=(\d+).*?num_total_params=(\d+)", log, re.DOTALL,
    )
    if parameter_match:
        result["learnable_parameters"] = int(parameter_match.group(1))
        result["total_parameters"] = int(parameter_match.group(2))
    steps = []
    for match in re.finditer(
        r"step:(\d+).*?loss:([0-9.eE+-]+).*?grdn:([0-9.eE+-]+).*?lr:([0-9.eE+-]+)",
        log,
    ):
        steps.append({
            "step": int(match.group(1)),
            "loss": float(match.group(2)),
            "gradient_norm": float(match.group(3)),
            "learning_rate": float(match.group(4)),
        })
    if steps:
        result["steps"] = steps
        result["final"] = steps[-1]
    return result
