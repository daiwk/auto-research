from __future__ import annotations

from auto_research.gpu_validation import validate_gpu_receipt


def test_gpu_receipt_rejects_machine_identity_and_accepts_sanitized_evidence():
    payload = {
        "schema_version": 1,
        "adapter_key": "demo",
        "validated_at": "2026-08-28",
        "accelerator": {"vendor": "NVIDIA", "model": "A100"},
        "command": ["auto-research", "demo"],
        "dataset": {"name": "public-mini"},
        "checkpoint": {"model_id": "public/model", "revision": "abc"},
        "result": "passed",
        "metrics": {"loss": 0.1},
        "provenance": {"commit": "abc", "artifact_path": "docs/gpu/demo.json"},
    }
    assert validate_gpu_receipt(payload) == []
    payload["hostname"] = "private-machine"
    assert "machine-specific field is forbidden: hostname" in validate_gpu_receipt(payload)
