"""Reanalyse author-published JEV predictions; benchmark-only, no model calls."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from auto_research.system_one.regional_transfer import (
    PUBLIC_FILES, UPSTREAM_REVISION, evaluate_transfer, file_receipt, read_parquet,
)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validation", required=True, type=Path)
    parser.add_argument("--test", required=True, type=Path)
    parser.add_argument("--fallback-test", type=Path)
    parser.add_argument("--fallback-validation", type=Path)
    parser.add_argument("--language")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    validation = read_parquet(args.validation, split="valid", language=args.language)
    test = read_parquet(args.test, split="test", language=args.language)
    fallback = read_parquet(args.fallback_test, split="test", language=args.language) if args.fallback_test else None
    fallback_valid = read_parquet(args.fallback_validation, split="valid", language=args.language) if args.fallback_validation else None
    result = evaluate_transfer(validation, test, fallback, fallback_validation=fallback_valid)
    result["source_files"] = {name: file_receipt(path) for name, path in
                              (("validation", args.validation), ("test", args.test), ("fallback_test", args.fallback_test),
                               ("fallback_validation", args.fallback_validation)) if path}
    known_blobs = {blob for _, blob in PUBLIC_FILES.values()}
    if all(r["git_blob_sha1"] in known_blobs for r in result["source_files"].values()):
        result["upstream_revision"] = UPSTREAM_REVISION
        result["source_kind"] = "verified_fixed_author_prediction_files"
    else:
        result["source_kind"] = "external_prediction_files; upstream origin unverified"
    seed_records = [{"role": "local_deterministic_reanalysis", "value": None}]
    if args.fallback_test and result["source_files"]["fallback_test"]["git_blob_sha1"] == PUBLIC_FILES["fallback-test.parquet"][1]:
        seed_records.append({"role": "upstream_published_IndoBERT_training", "value": 0})
    result["manifest_ref"] = "foundation-models:jev-regional-transfer"
    result["evaluation_protocol"] = {
        "tier": "public_prediction_reanalysis",
        "seeds": [record["value"] for record in seed_records if record["value"] is not None],
        "seed_roles": seed_records, "model_training_seeds": [], "formal_comparison": False,
        "claim_policy": "deterministic reanalysis of fixed predictions; upstream fallback seed is not a new local training seed",
        "selection_split": "valid", "evaluation_split": "test",
    }
    source_hashes = {name: receipt["sha256"] for name, receipt in sorted(result["source_files"].items())}
    fingerprint = hashlib.sha256(json.dumps(source_hashes, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    result["provenance"] = {
        "artifact_path": str(args.output), "dataset_fingerprint": f"sha256:{fingerprint}",
        "fingerprint_scope": "canonical mapping of role to source prediction file SHA256",
        "source_file_hashes": source_hashes,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
    print(f"{len(result['groups'])} language/dataset groups; accuracy {result['macro_accuracy']:.6f}")


if __name__ == "__main__":
    main()
