"""Sanitized, reviewable evidence for implementations that require CUDA."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = (
    "schema_version", "adapter_key", "validated_at", "accelerator",
    "command", "dataset", "checkpoint", "result", "metrics", "provenance",
)
FORBIDDEN_FIELDS = (
    "hostname", "host", "driver_version", "torch_build", "cuda_build",
    "ssh_alias", "user", "ip_address",
)
STANDALONE_GPU_RECEIPTS = {
    "system-one-formal-evolve": (
        "docs/gpu-validations/system-one-formal-evolve-a100-20260926.json"
    ),
    "laya-checkpoint": (
        "docs/gpu-validations/laya-checkpoint-a100-20260921.json"
    ),
    "nimble-checkpoint": (
        "docs/gpu-validations/nimble-checkpoint-a100-20260921.json"
    ),
    "nanojev-checkpoint": (
        "docs/gpu-validations/nanojev-checkpoint-a100-20260921.json"
    ),
    "oda": "docs/gpu-validations/oda-a100-20260919.json",
    "dqwen35": "docs/gpu-validations/dqwen35-a100-20260919.json",
    "aspire": "docs/gpu-validations/aspire-a100-20260919.json",
    "echo": "docs/gpu-validations/echo-a100-20260916.json",
    "videomm": "docs/gpu-validations/videomm-a100-20260916.json",
    "tiao": "docs/gpu-validations/tiao-a100-20260916.json",
    "atomrec-checkpoint": (
        "docs/gpu-validations/atomrec-checkpoint-a100-20260910.json"
    ),
    "autolr-checkpoint": (
        "docs/gpu-validations/autolr-checkpoint-a100-20260910.json"
    ),
    "checkpoint-normalized-dpo": (
        "docs/gpu-validations/checkpoint-normalized-dpo-a100-20260901.json"
    ),
    "criticl-checkpoint": "docs/gpu-validations/criticl-checkpoint-a100-20260901.json",
    "coskill-checkpoint": (
        "docs/gpu-validations/coskill-checkpoint-a100-20260910.json"
    ),
    "rlvr-fusion-checkpoints": (
        "docs/gpu-validations/rlvr-fusion-checkpoints-a100-20260901.json"
    ),
    "video-opsd-checkpoint": (
        "docs/gpu-validations/video-opsd-checkpoint-a100-20260901.json"
    ),
}


def load_gpu_receipt(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    errors = validate_gpu_receipt(payload)
    if errors:
        raise ValueError(f"{path}: " + "; ".join(errors))
    return payload


def validate_gpu_receipt(payload: dict[str, Any]) -> list[str]:
    errors = [f"{field} is required" for field in REQUIRED_FIELDS if not payload.get(field)]
    if payload.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if payload.get("result") != "passed":
        errors.append("result must be passed")
    accelerator = payload.get("accelerator") or {}
    if accelerator.get("vendor") != "NVIDIA" or not accelerator.get("model"):
        errors.append("accelerator must declare an NVIDIA model")
    if not isinstance(payload.get("command"), list):
        errors.append("command must be an argv list")
    serialized = json.dumps(payload, ensure_ascii=False).lower()
    for field in FORBIDDEN_FIELDS:
        if f'"{field}"' in serialized:
            errors.append(f"machine-specific field is forbidden: {field}")
    provenance = payload.get("provenance") or {}
    if not provenance.get("commit") or not provenance.get("artifact_path"):
        errors.append("provenance requires commit and artifact_path")
    return errors
