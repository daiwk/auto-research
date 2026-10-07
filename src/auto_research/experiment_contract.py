"""Versioned identities for resumable experiments; no runtime/model imports."""
from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
import hashlib
import json
from pathlib import Path
from typing import Any


def canonical(value: Any) -> Any:
    if is_dataclass(value):
        value = asdict(value)
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): canonical(item) for key, item in sorted(value.items())}
    if isinstance(value, (list, tuple)):
        return [canonical(item) for item in value]
    return value


def fingerprint(value: Any) -> str:
    return hashlib.sha256(json.dumps(canonical(value), sort_keys=True,
                                    ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def file_manifest(path: Path) -> str:
    """Hash file contents, not mtimes; never cache solely by directory name."""
    if not path.exists():
        return "missing"
    files = [path] if path.is_file() else sorted(p for p in path.rglob("*") if p.is_file())
    digest = hashlib.sha256()
    for item in files:
        digest.update((item.name if path.is_file() else item.relative_to(path).as_posix()).encode())
        digest.update(b"\0")
        with item.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        digest.update(b"\0")
    return digest.hexdigest()


def source_revision() -> str:
    # Works in a wheel too, and includes uncommitted implementation changes.
    root = Path(__file__).resolve().parent
    return fingerprint({p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(root.rglob("*.py"))})


EVOLUTION_RESUME_MUTABLE = frozenset({
    "generations", "output_dir", "resume_dir", "workers", "cpu_threads",
    "gpu_slots", "gpu_memory_per_trial_mb", "negative_memory_path",
})


def evolution_parameters(config) -> dict:
    return {key: value for key, value in canonical(config).items()
            if key not in EVOLUTION_RESUME_MUTABLE}


def validate_resume_config(saved, requested) -> None:
    before, after = evolution_parameters(saved), evolution_parameters(requested)
    changed = sorted(key for key in before.keys() | after.keys() if before.get(key) != after.get(key))
    if requested.generations < saved.generations:
        changed.append("generations (cannot decrease)")
    if changed:
        raise ValueError("Incompatible resume configuration: " + ", ".join(changed)
                         + ". Start a new run instead.")


@dataclass(frozen=True)
class ExperimentSpec:
    parameters: dict
    inputs: dict
    implementation: str
    schema_version: int = 1

    @property
    def fingerprint(self) -> str:
        return fingerprint(asdict(self))

    def to_dict(self) -> dict:
        return {**canonical(self), "fingerprint": self.fingerprint}

    def require_match(self, saved: dict) -> None:
        if not saved or saved.get("fingerprint") != self.fingerprint:
            raise ValueError("Experiment fingerprint mismatch (data, code or protocol changed, "
                             "or legacy run has no fingerprint). Start a new run; old results are retained.")


def evolution_spec(config, root: Path, dataset_summary: dict) -> ExperimentSpec:
    paths = {"dataset_dir": config.dataset_dir}
    for key, value in asdict(config).items():
        if isinstance(value, Path) and key not in {
            "output_dir", "resume_dir", "negative_memory_path", "dataset_dir",
        }:
            paths[key] = value
    inputs = {key: file_manifest(path if path.is_absolute() else root / path)
              for key, path in paths.items()}
    inputs["checkpoint_evidence"] = [file_manifest(path if path.is_absolute() else root / path)
                                     for path in config.checkpoint_evidence]
    # Ignore execution-only metadata; immutable inputs and parameters carry identity.
    inputs["dataset_summary"] = canonical({key: value for key, value in dataset_summary.items()
                                           if key not in {"runtime", "device", "resolved_device"}})
    return ExperimentSpec(evolution_parameters(config), inputs, source_revision())
