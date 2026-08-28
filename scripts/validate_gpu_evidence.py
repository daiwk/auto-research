#!/usr/bin/env python3
"""Enforce GPU validation receipts declared by reproduction adapters."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auto_research.gpu_validation import load_gpu_receipt  # noqa: E402
from auto_research.reproductions.registry import list_adapters  # noqa: E402


def audit() -> list[str]:
    errors: list[str] = []
    for adapter in list_adapters():
        if not adapter.requires_gpu_validation:
            continue
        if "cuda" not in adapter.device_capabilities:
            errors.append(f"{adapter.key}: GPU validation requires cuda capability")
        if not adapter.gpu_validation_artifact:
            errors.append(f"{adapter.key}: GPU validation artifact is missing")
            continue
        path = ROOT / adapter.gpu_validation_artifact
        if not path.is_file():
            errors.append(f"{adapter.key}: GPU validation artifact does not exist: {path}")
            continue
        try:
            payload = load_gpu_receipt(path)
        except (OSError, ValueError) as exc:
            errors.append(str(exc))
            continue
        if payload["adapter_key"] != adapter.key:
            errors.append(f"{adapter.key}: receipt adapter_key differs")
        if payload["provenance"]["artifact_path"] != adapter.gpu_validation_artifact:
            errors.append(f"{adapter.key}: receipt artifact_path differs")
    return errors


def main() -> int:
    errors = audit()
    if errors:
        print("\n".join(errors))
        return 1
    print("GPU validation evidence passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
