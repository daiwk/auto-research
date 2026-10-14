"""Audit user-supplied paired predictions, not checkpoint inference."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from auto_research.system_one.request_audit import audit_paired_predictions


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--predictions", required=True, type=Path)
    parser.add_argument("--threshold", type=float, default=0.5)
    parser.add_argument("--resamples", type=int, default=5000)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    content = args.predictions.read_bytes()
    rows = [json.loads(line) for line in content.decode().splitlines() if line.strip()]
    result = audit_paired_predictions(rows, threshold=args.threshold, resamples=args.resamples)
    result["input_sha256"] = hashlib.sha256(content).hexdigest()
    result["source_kind"] = "external_paired_predictions; source/checkpoint evidence supplied separately"
    result["manifest_ref"] = "foundation-models:jev-request-audit"
    result["evaluation_protocol"] = {
        "tier": "paired_prediction_protocol",
        "seeds": [result["bootstrap_seed"]],
        "seed_roles": [{"role": "query_cluster_bootstrap_rng", "value": result["bootstrap_seed"]}],
        "model_training_seeds": [], "formal_comparison": False,
        "claim_policy": "paired external prediction analysis; bootstrap seed is not a model/training seed and does not certify inference provenance",
    }
    result["provenance"] = {
        "artifact_path": str(args.output), "dataset_fingerprint": f"sha256:{result['input_sha256']}",
        "fingerprint_scope": "exact supplied paired-prediction JSONL bytes",
        "model_checkpoint_origin_verified": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
