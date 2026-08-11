from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location(
    "metric_migration", ROOT / "scripts/migrate_metric_schema_v2.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_migration_preserves_native_v2_protocol_and_provenance():
    path = ROOT / "docs" / "multimodal-models" / "metrics" / "result.json"
    payload = {
        "schema_version": 2,
        "manifest_ref": "multimodal-models:cifar10-qa",
        "evaluation_tier": "l1_public_images",
        "seeds": [42, 43, 44],
        "evaluation_protocol": {
            "tier": "l1_public_images",
            "claim_policy": "L1 result; not open-ended VQA",
        },
        "provenance": {
            "artifact_path": "old",
            "original_code_commit": "abc123",
            "dataset_fingerprint": "md5:example",
        },
    }
    migrated = MODULE.migrate_payload(path, payload)
    assert migrated["manifest_ref"] == payload["manifest_ref"]
    assert migrated["evaluation_protocol"]["tier"] == "l1_public_images"
    assert migrated["evaluation_protocol"]["claim_policy"] == "L1 result; not open-ended VQA"
    assert "historical_migration" not in migrated["provenance"]
    assert migrated["provenance"]["original_code_commit"] == "abc123"
