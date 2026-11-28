"""Bind the CPU-only Habitats diagnostic; never fabricate a CUDA receipt."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json

from oct18_frozen_sources import verify_sources
from run_nov28_habitats_component import AUDIT, ROOT, config, load, source_hashes, validate_raw

_spec = importlib.util.spec_from_file_location("_nov28_metric_base", ROOT / "scripts/curate_nov18_latest_evidence.py")
_base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_base)
_base.AUDIT = AUDIT


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    frozen = load(AUDIT / "frozen-sources.json")
    if frozen["source_sha256"] != source_hashes():
        raise ValueError("executed source drift")
    verify_sources(ROOT, frozen["commit"], frozen["source_sha256"], frozen["proof"])
    raw = load(AUDIT / "raw-cpu.json")
    validate_raw(raw, frozen)
    for key, item in config()["components"].items():
        spec = load(ROOT / f"src/auto_research/paper_specs/catalog/{item['domain']}/{key}.json")
        if item["cuda"] or spec["requires_gpu_validation"] or spec["evaluation_tier"] != "l1_mechanism":
            raise ValueError("CPU-only L1 scope changed")
        payload = _base.metric(key, item, spec, raw, frozen)
        payload["full_experiment_review_done"] = spec["full_experiment_review_done"]
        payload["dataset"]["id"] = "synthetic:nov28-habitats-component-v1"
        payload["provenance"]["dataset_fingerprint"] = "sha256:" + hashlib.sha256(json.dumps(payload["dataset"], sort_keys=True).encode()).hexdigest()
        _base.put(ROOT / payload["provenance"]["artifact_path"], payload, args.check)
    print(json.dumps({"cpu_components": 1, "cuda_components": 0, "capability_promotions": 0}))


if __name__ == "__main__":
    main()
