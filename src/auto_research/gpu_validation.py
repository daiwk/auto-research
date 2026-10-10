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
    "dial-opd": "docs/gpu-validations/dial-opd-a100-20261010.json",
    "meta-opd": "docs/gpu-validations/meta-opd-a100-20261010.json",
    "semi-opd": "docs/gpu-validations/semi-opd-a100-20261010.json",
    "grpo-dropout": "docs/gpu-validations/grpo-dropout-a100-20261010.json",
    "residual-advantage": "docs/gpu-validations/residual-advantage-a100-20261010.json",
    "mass": "docs/gpu-validations/oct10-mass-a100.json",
    "race": "docs/gpu-validations/oct10-race-a100.json",
    "hippocam": "docs/gpu-validations/oct10-hippocam-a100.json",
    "evoalloc": "docs/gpu-validations/oct10-evoalloc-a100.json",
    "elastic-expert-routing": "docs/gpu-validations/elastic-expert-routing-a30-20261010.json",
    "vimod": "docs/gpu-validations/vimod-a100-20261010.json",
    "jev-capability": "docs/gpu-validations/jev-capability-a100-20261010.json",
    "oct07-agent-search": "docs/gpu-validations/oct07-agent-search-a100.json",
    "architecture-mrb-runtime": "docs/gpu-validations/architecture-mrb-a100-20261007.json",
    "experiment-integrity-runtime": "docs/gpu-validations/experiment-integrity-a100-20261007.json",
    "taco-optimizer": "docs/gpu-validations/taco-optimizer-a100-20261002.json",
    "veto": "docs/gpu-validations/veto-a100-20261002.json",
    "stepquant": "docs/gpu-validations/stepquant-a100-20260930.json",
    "leapquant": "docs/gpu-validations/leapquant-a100-20260930.json",
    "dr-opd": "docs/gpu-validations/dr-opd-a100-20260930.json",
    "sipo": "docs/gpu-validations/sipo-a100-20260930.json",
    "roft": "docs/gpu-validations/roft-a100-20260930.json",
    "lspd": "docs/gpu-validations/lspd-a100-20260930.json",
    "ms-gla": "docs/gpu-validations/ms-gla-a100-20260930.json",
    "kite-sst-gpu-latency": (
        "docs/gpu-validations/kite-sst-gpu-latency-a100-20260929.json"
    ),
    "mad-rl-qwen-choice": (
        "docs/gpu-validations/mad-rl-qwen-choice-a100-20260929.json"
    ),
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
